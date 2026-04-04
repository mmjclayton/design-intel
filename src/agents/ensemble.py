"""
Ensemble runner — runs the same critique across multiple LLM models
in parallel, then synthesises findings into a consensus report.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from src.agents.critique import CritiqueAgent
from src.analysis.wcag_checker import run_wcag_check, run_wcag_check_multi
from src.input.models import DesignInput
from src.providers.llm import call_llm, get_model_display_name
from src.config import settings


SYNTHESIS_PROMPT = """\
You are a design critique synthesis specialist. You have received independent \
design critiques from multiple AI models analysing the same interface. Your job \
is to merge these into a single, authoritative consensus report.

## Rules:

1. **Consensus findings** (all models agree) - Include with HIGH confidence. \
These are unchallengeable.

2. **Majority findings** (most models agree) - Include with MODERATE confidence. \
Note which models found it.

3. **Unique findings** (only one model caught) - Include in a separate "Unique \
Insights" section. These may be genuine catches the other models missed, or they \
may be hallucinations. Flag them for human review.

4. **Conflicts** (models disagree) - Include in a "Disputed Findings" section. \
Show both positions and let the reader decide.

5. **Scores** - Report the average score and the range. If scores are within 10 \
points, the consensus is strong. If the range exceeds 20 points, note the disagreement.

6. **Do NOT add your own findings.** Only synthesise what the models reported. \
Your job is editorial, not analytical.

7. **Preserve specificity.** If one model cited exact pixel values, contrast ratios, \
or CSS selectors, use those exact values in the consensus report.

8. **Credit sources.** When a finding came from a specific model, note it: \
"(identified by Model A)" or "(all models agree)".

## Output format:

### Consensus Summary
Overall assessment based on model agreement. Average score and range.

### Models Used
List each model and its individual score.

### Consensus Findings (all models agree)
Highest confidence findings.

### Majority Findings (most models agree)
Findings with broad but not universal agreement.

### Unique Insights (single model)
Findings only one model caught. Flagged for review.

### Disputed Findings (models disagree)
Where models reached different conclusions.

### Consolidated Score
Weighted breakdown with model agreement notes.

### Priority Fixes
Ranked by consensus level (unanimous first, then majority, then unique).
"""


class EnsembleRunner:
    def __init__(self, models: list[str], tone: str = "opinionated"):
        self.models = models
        self.tone = tone

    def run(self, design_input: DesignInput, context: str = "") -> str:
        """Run critique across all models in parallel, then synthesise."""

        # Run WCAG checker once (deterministic, same for all models)
        if design_input.pages and len(design_input.pages) > 1:
            wcag_report = run_wcag_check_multi(design_input.pages)
        else:
            wcag_report = run_wcag_check(design_input.dom_data)

        # Run each model in parallel
        model_results = {}

        def _run_model(model_id: str) -> tuple[str, str]:
            agent = CritiqueAgent(tone=self.tone)

            # Override the model for this run by patching the call
            original_run = agent.run

            def patched_run(di, ctx=""):
                knowledge = agent.retrieve_knowledge(di)
                user_prompt = agent.build_user_prompt(di, ctx)
                if knowledge:
                    user_prompt = f"## Relevant Design Principles\n\n{knowledge}\n\n---\n\n{user_prompt}"
                image_paths = agent.get_image_paths(di)
                return call_llm(
                    system_prompt=agent.system_prompt(),
                    user_prompt=user_prompt,
                    image_paths=image_paths,
                    model=model_id,
                )

            return model_id, patched_run(design_input, context)

        with ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            futures = {
                executor.submit(_run_model, model): model
                for model in self.models
            }
            for future in as_completed(futures):
                try:
                    model_id, output = future.result()
                    model_results[model_id] = output
                except Exception as e:
                    model_id = futures[future]
                    model_results[model_id] = f"ERROR: Model failed - {str(e)[:200]}"

        # Synthesise
        return self._synthesise(wcag_report, model_results)

    def _synthesise(self, wcag_report, model_results: dict) -> str:
        """Run the synthesis agent to merge all model outputs."""

        # Build the synthesis prompt with all model outputs
        parts = [
            "## Pre-Computed WCAG Audit (deterministic, all models received this same data)\n",
            wcag_report.to_markdown(),
            "\n---\n",
            f"## Individual Model Critiques ({len(model_results)} models)\n",
        ]

        for model_id, output in model_results.items():
            display = get_model_display_name(model_id)
            parts.append(f"\n### Critique from: {display}\n")
            parts.append(output[:8000])  # Cap per-model output to fit context
            parts.append("\n---\n")

        parts.append(
            "\nSynthesise these critiques into a single consensus report. "
            "Identify where models agree, disagree, and what unique findings each caught."
        )

        synthesis_input = "\n".join(parts)

        # Use the primary model for synthesis
        return call_llm(
            system_prompt=SYNTHESIS_PROMPT,
            user_prompt=synthesis_input,
            max_tokens=8000,
        )


def get_ensemble_models() -> list[str]:
    """Parse ENSEMBLE_MODELS from settings."""
    raw = settings.ensemble_models.strip()
    if not raw:
        return [_get_default_model()]
    return [m.strip() for m in raw.split(",") if m.strip()]


def _get_default_model() -> str:
    from src.providers.llm import _resolve_model
    return _resolve_model()

"""
Multi-agent orchestrator — runs specialized sub-agents in parallel,
reconciles contradictions, and merges into a unified report.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from src.agents.accessibility_agent import AccessibilityAgent
from src.agents.design_system_agent import DesignSystemAgent
from src.agents.visual_agent import VisualDesignAgent
from src.agents.interaction_agent import InteractionAgent
from src.analysis.wcag_checker import run_wcag_check, run_wcag_check_multi
from src.input.models import DesignInput
from src.providers.llm import call_llm


RECONCILIATION_PROMPT = """\
You are a technical editor reviewing a design critique report produced by \
four independent sub-agents. Your ONLY job is to find and fix contradictions \
between sections. Do NOT add new findings or change the substance.

Fix these specific problems:
1. If one section says "no active state" but another confirms active states \
exist with specific CSS changes, remove the false claim.
2. If one section says "no focus styles" but another documents focus styles \
working, remove the false claim.
3. If counts are impossible (e.g. "13/10 inputs missing labels"), fix the \
denominator to match the actual count.
4. If colours are described as "pure black #000000" or "pure white #FFFFFF" \
but the DOM data shows different values (#0f1117, #e1e4ed), use the DOM values.
5. If the same element appears multiple times as separate violations, \
deduplicate to count unique elements only.

Output the complete corrected report. Preserve all formatting, sections, and \
findings that are NOT contradictory. Only change what is factually inconsistent \
between sections.
"""


def run_multi_agent_critique(design_input: DesignInput, context: str = "") -> str:
    """Run all four specialized agents in parallel, reconcile, and merge."""

    agents = {
        "accessibility": AccessibilityAgent(),
        "design_system": DesignSystemAgent(),
        "visual": VisualDesignAgent(),
        "interaction": InteractionAgent(),
    }

    # Run WCAG checker (deterministic, instant)
    if design_input.pages and len(design_input.pages) > 1:
        wcag_report = run_wcag_check_multi(design_input.pages)
    else:
        wcag_report = run_wcag_check(design_input.dom_data)

    # Run all agents in parallel
    results = {}

    def _run_agent(name, agent):
        return name, agent.run(design_input, context)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(_run_agent, name, agent): name
            for name, agent in agents.items()
        }
        for future in as_completed(futures):
            name, output = future.result()
            results[name] = output

    # Merge into draft report
    draft = _merge_reports(wcag_report, results)

    # Reconciliation pass — fix contradictions between sub-agents
    reconciled = _reconcile(draft)

    return reconciled


def _merge_reports(wcag_report, agent_results: dict) -> str:
    """Merge WCAG checker and agent outputs into a unified report."""

    sections = []

    # Header
    sections.append("# Design Critique Report (Multi-Agent Analysis)\n")
    sections.append(
        "This report was produced by four specialized agents analysing the design "
        "in parallel, plus a deterministic WCAG 2.2 checker.\n"
    )

    # WCAG Checker (deterministic)
    sections.append("---\n")
    sections.append(wcag_report.to_markdown())

    # Visual Design
    if "visual" in agent_results:
        sections.append("---\n")
        sections.append("## Visual Design Analysis\n")
        sections.append(agent_results["visual"])

    # Accessibility Deep Dive
    if "accessibility" in agent_results:
        sections.append("\n---\n")
        sections.append("## Accessibility Deep Dive\n")
        sections.append(agent_results["accessibility"])

    # Design System
    if "design_system" in agent_results:
        sections.append("\n---\n")
        sections.append("## Design System Analysis\n")
        sections.append(agent_results["design_system"])

    # Interaction Quality
    if "interaction" in agent_results:
        sections.append("\n---\n")
        sections.append("## Interaction Quality Analysis\n")
        sections.append(agent_results["interaction"])

    return "\n".join(sections)


def _reconcile(draft: str) -> str:
    """Run a reconciliation pass to fix contradictions between sub-agents."""
    try:
        return call_llm(
            system_prompt=RECONCILIATION_PROMPT,
            user_prompt=draft,
            max_tokens=8000,
        )
    except Exception:
        # If reconciliation fails, return the draft as-is
        return draft

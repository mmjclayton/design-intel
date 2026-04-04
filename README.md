# Better Design Agent

An agent-based CLI that delivers expert-level UX/UI design critique, generates style guides, extracts design systems from live products, and writes design specifications - powered by a self-improving knowledge library of 37 design principles across 10 domains.

No static checklists. No vague suggestions. Specific, opinionated feedback grounded in established design principles, with every criticism backed by a concrete fix and a severity rating.

## What it does

| Command | Description | Status |
|---|---|---|
| `design-intel critique` | Expert design critique from a screenshot, URL, or description | Available |
| `design-intel critique --crawl` | Multi-page SPA crawl with cross-page analysis | Available |
| `design-intel generate-style` | Generate a complete style guide from a brief | Planned |
| `design-intel extract-style` | Reverse-engineer a style guide from a live site | Planned |
| `design-intel write-spec` | Write a UX/UI spec from feature requirements | Planned |
| `design-intel curate` | Discover and ingest new design knowledge | Planned |

## Quick start

```bash
# Clone
git clone https://github.com/mmjclayton/better-design-agent.git
cd better-design-agent

# Install (Python 3.11+ required)
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Install browser engine (for URL screenshots)
playwright install chromium

# Configure
cp .env.example .env
# Add your API key to .env

# Build the knowledge index
design-intel index-knowledge
```

## Usage

### Critique a single page

```bash
design-intel critique --url "https://example.com"
design-intel critique --image ./screenshot.png
design-intel critique --describe "A login page with tiny grey placeholder text and no form labels"
```

### Crawl an entire app (SPA-aware)

```bash
design-intel critique --url "http://localhost:3000" --crawl --save
design-intel critique --url "http://localhost:3000" --crawl --max-pages 15
```

The `--crawl` flag discovers navigation elements, clicks through each page, and extracts DOM metrics from every view. Works with SPAs (React, Vue, etc.) that use client-side routing.

### Options

```bash
# Set critique tone: opinionated (default), balanced, or gentle
design-intel critique --url "..." --tone balanced

# Add context about the design
design-intel critique --image ./dashboard.png --context "B2B analytics dashboard for enterprise finance teams"

# Save report to output/
design-intel critique --url "https://example.com" --save
```

## How it works

The critique agent combines three data sources for every analysis:

### 1. Visual analysis (screenshot)
The LLM analyses the screenshot for visual hierarchy, layout composition, and overall design quality.

### 2. DOM extraction (automated)
Playwright extracts exact computed values from the page:
- **Colours** - every text and background colour with frequency counts
- **Contrast ratios** - computed for all text/background pairs, checked against WCAG 2.2 AA
- **Non-text contrast** - UI component boundaries checked against WCAG 1.4.11 (3:1)
- **Font sizes** - all sizes in use, flagging arbitrary values outside a modular scale
- **Spacing values** - padding, margin, and gap values to identify systematic vs arbitrary spacing
- **Touch targets** - every interactive element measured against the 44x44px minimum
- **Focus styles** - which elements have custom focus-visible styles and which rely on browser defaults
- **CSS custom properties** - design tokens defined on `:root`, grouped by category
- **HTML structure** - landmarks, headings, skip links, form labels, ARIA attributes

### 3. Knowledge library (37 entries, 10 domains)
The critique is grounded in established design frameworks retrieved from the knowledge library. See [Knowledge Library](#knowledge-library) below.

## Evaluation frameworks

Every critique is grounded in these established frameworks:

- **Nielsen's 10 Usability Heuristics** - findings reference specific heuristics by name
- **Nielsen Severity Scale (0-4)** - every finding is rated: 0 (not a problem) to 4 (usability catastrophe)
- **WCAG 2.2 AA** - specific success criteria cited by number (e.g. WCAG 2.5.8, WCAG 1.4.11)
- **Gestalt Principles** - proximity, similarity, figure-ground applied to layout and grouping
- **Fitts's Law** - target size and distance analysis for interactive elements

## LLM providers

Works with any LLM provider via [LiteLLM](https://github.com/BerriAI/litellm). Configure in `.env`:

### Anthropic (default)

```env
LLM_PROVIDER=claude
LLM_MODEL=claude-sonnet-4-20250514
ANTHROPIC_API_KEY=sk-ant-...
```

### OpenAI

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-...
```

### Ollama (free, local)

```bash
brew install ollama
ollama pull llama3.2-vision
```

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2-vision
```

## Knowledge library

The critique agent is backed by a versioned, git-tracked knowledge library of design principles stored as structured markdown with YAML frontmatter. Each entry is sourced from authoritative references and tagged for retrieval.

### 37 entries across 10 domains

```
knowledge/
  accessibility/    # WCAG 2.2, ARIA, COGA, touch targets, inclusive design, annotations
  heuristics/       # Nielsen's 10, Shneiderman's 8, severity ratings
  typography/       # Type scales, typographic hierarchy, line length
  colour/           # Contrast, dark mode, colour psychology, ColorBrewer
  layout/           # Gestalt principles, F-pattern, spacing systems, whitespace
  interaction/      # Form design, microinteractions, navigation, IA, component states
  systems/          # Atomic design, design tokens, Material 3, Apple HIG, Carbon, Figma references
  critique/         # Liz Lerman CRP, five modes of design review
  motion/           # Animation principles, reduced motion, transition patterns
  mobile/           # Thumb zone, responsive design, platform conventions
```

### Entry format

Each knowledge entry follows this structure:

```yaml
---
id: acc-001
title: "WCAG Contrast Ratio Requirements"
category: accessibility
tags: [contrast, wcag, colour, accessibility]
source: "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html"
source_authority: canonical
ingested: 2026-04-04
validated: true
---

[Markdown content: the principle, when to apply it, exceptions, examples]
```

### Source corpus

The knowledge library is built from authoritative sources documented in `knowledge/CORPUS_SOURCES.md`. This file tracks all source references across the 10 domains, including free URLs, books, and academic papers, so contributors know where entries came from and what sources remain to be distilled.

### Contributing knowledge entries

1. Add a new `.md` file in the appropriate `knowledge/[category]/` directory
2. Include YAML frontmatter with `id`, `title`, `category`, `tags`, `source`, and `source_authority`
3. Write actionable content: the principle, when to apply it, common violations
4. Run `design-intel index-knowledge` to rebuild the tag index
5. Add the source to `knowledge/CORPUS_SOURCES.md` if it's a new reference

### Rebuild the knowledge index

```bash
design-intel index-knowledge
```

## Critique categories

Every critique evaluates across nine categories:

- **Visual hierarchy** - Can users identify the primary action within 3 seconds?
- **Typography** - Consistent type scale, readable line lengths (45-75 chars), appropriate fonts
- **Colour and contrast** - WCAG 2.2 AA compliance, non-text contrast (1.4.11), dark mode best practices
- **Spacing and rhythm** - Systematic spacing scale, Gestalt proximity grouping
- **Layout and composition** - Grid consistency, visual flow, responsive readiness
- **Accessibility (WCAG 2.2)** - Landmarks, headings, form labels, ARIA, touch targets, focus management, skip links
- **Interaction patterns** - Component states (8 required states per element), affordances, platform conventions
- **Consistency** - Design token usage, hardcoded vs tokenised values
- **Information architecture** - Progressive disclosure, navigation patterns, content organisation

## Project structure

```
better-design-agent/
├── src/
│   ├── cli.py                  # Typer CLI entry point
│   ├── config.py               # Pydantic Settings
│   ├── providers/llm.py        # LiteLLM wrapper (Claude, OpenAI, Ollama)
│   ├── input/
│   │   ├── processor.py        # Input normalisation (image, URL, text)
│   │   ├── screenshot.py       # Playwright: screenshots, DOM extraction, SPA crawl
│   │   └── models.py           # DesignInput, PageCapture dataclasses
│   ├── agents/
│   │   ├── base.py             # Base agent with knowledge retrieval
│   │   └── critique.py         # Critique agent with DOM formatting
│   ├── knowledge/
│   │   ├── store.py            # Read/write knowledge entries
│   │   ├── index.py            # Tag-based index (INDEX.yaml)
│   │   └── retriever.py        # Hybrid retrieval by tags/category
│   └── output/
│       └── formatter.py        # Report saving with timestamps
├── knowledge/                  # Design knowledge corpus (git-tracked)
│   ├── INDEX.yaml              # Auto-generated tag index
│   ├── CORPUS_SOURCES.md       # Source reference document
│   ├── accessibility/          # 7 entries
│   ├── heuristics/             # 3 entries
│   ├── interaction/            # 5 entries
│   ├── layout/                 # 4 entries
│   ├── systems/                # 6 entries
│   ├── colour/                 # 3 entries
│   ├── typography/             # 2 entries
│   ├── critique/               # 2 entries
│   ├── motion/                 # 2 entries
│   ├── mobile/                 # 3 entries
│   └── pending/                # Entries awaiting review
├── tests/
│   └── benchmark_critique.py   # Output quality benchmark
├── config/default.yaml         # Default configuration
└── output/                     # Generated reports (gitignored)
```

## Benchmarking

The `tests/benchmark_critique.py` script scores critique outputs across seven dimensions:

| Dimension | What it measures |
|---|---|
| Specificity | Hex colours, pixel values, contrast ratios, CSS selectors cited |
| Coverage | Design categories evaluated (9 possible) |
| Actionability | Findings with concrete fixes including specific values |
| Accessibility Depth | WCAG criteria referenced, semantic HTML analysis, focus audit |
| Design System Awareness | Existing token references, proposed token systems |
| Scope | Pages covered, empty/loading/responsive state analysis |
| Unique Findings | Issues found that other tools missed |

Run against the benchmark outputs:

```bash
python -m tests.benchmark_critique
```

## Roadmap

- [x] **Phase 1** - Critique Agent + knowledge library (37 entries, 10 domains)
- [x] **Phase 1.5** - DOM extraction, HTML audit, multi-page SPA crawl, benchmarking
- [ ] **Phase 2** - Style Guide Generator + Extractor, vector search (ChromaDB)
- [ ] **Phase 3** - Design Spec Writer, Figma input support
- [ ] **Phase 4** - Autonomous knowledge curation and validation
- [ ] **Phase 5** - API server mode (FastAPI), plugin system

## Configuration

All options can be set via `.env`, environment variables, or `config/default.yaml`:

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `claude` | `claude`, `openai`, or `ollama` |
| `LLM_MODEL` | `claude-sonnet-4-20250514` | Model identifier |
| `KNOWLEDGE_RETRIEVAL_LIMIT` | `2000` | Max tokens of knowledge context per call |
| `RETRIEVAL_TOP_K` | `5` | Number of knowledge chunks retrieved |
| `OUTPUT_FORMAT` | `markdown` | `markdown`, `json`, or `yaml` |
| `CRITIQUE_SEVERITY_THRESHOLD` | `low` | Minimum severity to include |

## License

MIT

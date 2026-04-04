# Better Design Agent

An agent-based CLI that delivers expert-level UX/UI design critique, generates style guides, extracts design systems from live products, and writes design specifications — powered by a self-improving knowledge library.

No static checklists. No vague suggestions. Specific, opinionated feedback grounded in established design principles, with every criticism backed by a concrete fix.

## What it does

| Command | Description | Status |
|---|---|---|
| `design-intel critique` | Expert design critique from a screenshot, URL, or description | Available |
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
```

## Usage

### Critique a design from a description

```bash
design-intel critique --describe "A login page with tiny grey placeholder text, no form labels, and a blue Submit button"
```

### Critique a screenshot

```bash
design-intel critique --image ./screenshot.png
```

### Critique a live URL

```bash
design-intel critique --url "https://example.com"
```

### Options

```bash
# Set critique tone: opinionated (default), balanced, or gentle
design-intel critique --describe "..." --tone balanced

# Add context about the design
design-intel critique --image ./dashboard.png --context "B2B analytics dashboard for enterprise finance teams"

# Save report to output/
design-intel critique --url "https://example.com" --save
```

## Example output

```
Summary

The login page has several critical issues that hinder usability and accessibility.
Immediate improvements are needed.

Critical Issues

1. Missing form labels — placeholder text disappears on focus, leaving users
   without context. Replace with visible labels above each input.

2. Insufficient contrast — grey placeholder text on white fails WCAG AA
   (4.5:1 minimum). Use #595959 or darker for body text.

3. No validation feedback — users get no indication of input errors.
   Add inline validation with specific error messages.

4. No password recovery — standard expectation for any login page.
   Add a "Forgot password?" link near the password field.
```

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
# Install and pull a model
brew install ollama
ollama pull llama3.2-vision
```

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2-vision
```

## Critique categories

Every critique evaluates across nine categories:

- **Visual hierarchy** — Can users identify the primary action within 3 seconds?
- **Typography** — Consistent type scale, readable line lengths (45-75 chars), appropriate fonts
- **Colour** — Cohesive palette, consistent meaning, WCAG contrast compliance
- **Spacing** — Systematic spacing scale, proper grouping of related elements
- **Layout** — Grid consistency, visual flow, responsive readiness
- **Accessibility** — WCAG 2.2 compliance, touch targets (44x44px min), keyboard navigation
- **Interaction patterns** — Clear affordances, visible states (hover, focus, error, loading)
- **Consistency** — Visual coherence across elements
- **Information architecture** — Logical content organisation, clear navigation

## Knowledge library

The critique agent is backed by a versioned knowledge library of design principles stored as structured markdown. The library ships with seed entries covering WCAG accessibility, typography scales, and spacing systems — and is designed to grow over time through automated curation.

```
knowledge/
  accessibility/    # WCAG guidelines, screen reader patterns
  typography/       # Type scales, font pairing, readability
  colour/           # Contrast ratios, colour theory
  layout/           # Grid systems, spacing, responsive breakpoints
  interaction/      # Form patterns, loading states
  systems/          # Material Design, Apple HIG, Carbon summaries
```

### Rebuild the knowledge index

```bash
design-intel index-knowledge
```

## Project structure

```
better-design-agent/
├── src/
│   ├── cli.py                  # Typer CLI entry point
│   ├── config.py               # Pydantic Settings
│   ├── providers/llm.py        # LiteLLM wrapper (Claude, OpenAI, Ollama)
│   ├── input/                  # Input processing (screenshots, URLs, text)
│   ├── agents/                 # Agent implementations
│   │   ├── base.py             # Base agent with knowledge retrieval
│   │   └── critique.py         # Critique agent
│   ├── knowledge/              # Knowledge store, index, retriever
│   └── output/                 # Report formatting and saving
├── knowledge/                  # Design knowledge corpus (git-tracked)
├── config/default.yaml         # Default configuration
└── output/                     # Generated reports (gitignored)
```

## Roadmap

- [x] **Phase 1** — Critique Agent + static knowledge library
- [ ] **Phase 2** — Style Guide Generator + Extractor, vector search (ChromaDB)
- [ ] **Phase 3** — Design Spec Writer, Figma input support
- [ ] **Phase 4** — Autonomous knowledge curation and validation
- [ ] **Phase 5** — API server mode (FastAPI), plugin system

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

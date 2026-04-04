---
id: sys-007
title: "Design System Documentation Standards"
category: systems
tags: [design-system, documentation, reference, components, patterns, rationale]
source: "Design System Documentation Sites Reference Corpus (2026)"
source_authority: canonical
ingested: 2026-04-04
validated: true
validator_notes: "Catalogue of publicly accessible design system documentation sites with quality assessment"
---

## Big Tech Platform Systems (Gold Standard)

These are the reference standard for design system documentation quality:

### Apple HIG
- **URL**: developer.apple.com/design/human-interface-guidelines
- **Platforms**: iOS, iPadOS, macOS, watchOS, tvOS, visionOS
- **Rationale quality**: Exceptional - explains *why* behind every guideline
- **Strongest on**: Decision rationale, writing/content guidelines, navigation patterns
- **Core principles**: Deference, clarity, depth

### Material Design 3
- **URL**: m3.material.io
- **Platforms**: Web, Android, iOS, Flutter
- **Rationale quality**: Strong - usage guidelines, do/don't examples, spec sheets per component
- **Strongest on**: Design tokens, motion/animation, accessible colour, cross-platform consistency

### Microsoft Fluent 2
- **URL**: fluent2.microsoft.design
- **Platforms**: Web (React), Windows, iOS, Android
- **Rationale quality**: Moderate-Strong - usage guidelines and accessibility notes per component
- **Strongest on**: Cross-platform alignment, Figma-to-code handoff

### IBM Carbon
- **URL**: carbondesignsystem.com
- **Platforms**: Web (React, Angular, Vue, Web Components)
- **Rationale quality**: Exceptional - four mandatory tabs per component (Usage, Style, Code, Accessibility)
- **Strongest on**: Accessibility at component level, pattern-level flows, content guidelines

## Documentation Quality Tiers

| Tier | What It Means | Examples |
|------|--------------|---------|
| Exceptional | Every component has rationale, usage rules, do/don't, accessibility, code | Carbon, Apple HIG |
| Strong | Components have usage guidelines, states, accessibility notes | Material 3, Fluent 2 |
| Moderate | Components documented but rationale is sparse | Polaris, Primer |
| Basic | Component catalogue with visual specs only | Most community systems |

## Best Practice: Four-Tab Component Documentation (Carbon Model)

Every component should document:

1. **Usage** - When to use, when not to use, variants, related components
2. **Style** - Visual specs, spacing, typography, colour tokens
3. **Code** - Implementation reference, props/API, framework-specific notes
4. **Accessibility** - ARIA roles, keyboard interaction, screen reader behaviour

## When to apply
- Evaluate whether a design follows documented platform conventions
- Reference specific platform guidelines when recommending patterns
- Assess design system documentation completeness
- Compare component implementations against platform standards

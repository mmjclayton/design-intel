---
id: acc-001
title: "WCAG Contrast Ratio Requirements"
category: accessibility
tags: [contrast, wcag, colour, accessibility]
source: "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html"
source_authority: canonical
ingested: 2026-04-04
validated: true
validator_notes: "Direct from W3C WCAG 2.2 specification"
---

## Minimum Contrast Ratios (WCAG 2.2)

**Level AA (minimum):**
- Normal text (<24px / <18.66px bold): 4.5:1 contrast ratio
- Large text (>=24px / >=18.66px bold): 3:1 contrast ratio
- UI components and graphical objects: 3:1 contrast ratio

**Level AAA (enhanced):**
- Normal text: 7:1 contrast ratio
- Large text: 4.5:1 contrast ratio

## When to apply
- All text content must meet AA minimum
- Interactive component boundaries (buttons, inputs) must meet 3:1 against adjacent colours
- Icons that convey meaning must meet 3:1
- Decorative elements are exempt
- Logos and brand text are exempt

## Common violations
- Light grey text on white backgrounds (placeholder text is a frequent offender)
- Coloured text on coloured backgrounds without checking computed contrast
- Focus indicators that don't meet 3:1 against both the component and the background
- Disabled states that are too low contrast to read (still need to be perceivable)

---
id: typ-001
title: "Type Scale Ratios for Interface Design"
category: typography
tags: [type-scale, modular-scale, readability, typography]
source: "https://type-scale.com"
source_authority: high
ingested: 2026-04-04
validated: true
validator_notes: "Cross-referenced with Material Design and Apple HIG type scales"
---

## Modular Type Scales

A type scale is a set of font sizes derived from a base size and a ratio. Consistent scales create visual rhythm and hierarchy.

**Common ratios for UI design:**
- 1.125 (Major Second): Tight scale, good for data-dense UIs and dashboards
- 1.200 (Minor Third): Balanced, works for most applications
- 1.250 (Major Third): More dramatic hierarchy, good for marketing and content sites
- 1.333 (Perfect Fourth): Strong hierarchy, editorial and long-form content
- 1.500 (Perfect Fifth): Very dramatic, use sparingly — hero sections, landing pages

**Recommended base sizes:**
- Desktop: 16px minimum body text (browser default)
- Mobile: 16px minimum (prevents iOS zoom on input focus)
- Data-dense UIs: 14px acceptable for secondary content, never for primary

## When to apply
- Choose one ratio and derive all sizes from it
- Limit to 5-7 distinct sizes in a type scale
- Use font weight and colour to create sub-hierarchy within a size level
- Line height should decrease proportionally as font size increases (1.5 for body, 1.2-1.3 for headings)

## Common violations
- Arbitrary font sizes (13px, 15px, 17px, 21px) with no mathematical relationship
- Too many distinct sizes (more than 7 creates visual noise)
- Body text below 16px on mobile
- Identical font sizes differentiated only by colour (fails accessibility)

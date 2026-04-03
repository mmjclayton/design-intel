---
id: lay-001
title: "Spacing Systems for Interface Design"
category: layout
tags: [spacing, grid, layout, consistency]
source: "https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62"
source_authority: high
ingested: 2026-04-04
validated: true
validator_notes: "Nathan Curtis / EightShapes, widely adopted approach"
---

## Spacing Scale

A spacing system uses a base unit multiplied by consistent increments. This creates visual rhythm and makes layouts feel intentional.

**Common approaches:**
- **4px base, linear:** 4, 8, 12, 16, 20, 24, 32, 40, 48, 64 — fine-grained control
- **8px base, linear:** 8, 16, 24, 32, 40, 48, 64 — simpler, works for most UIs
- **Geometric (×2):** 4, 8, 16, 32, 64 — dramatic jumps, strong visual hierarchy

**4px base is recommended** — it's granular enough for component internals (padding, gaps) while scaling cleanly for layout spacing (margins, sections).

## When to apply
- **Inset (padding):** Space inside a container. Use consistent values per component type.
- **Stack (vertical):** Space between stacked elements. Related items get tight spacing (8-12px), groups get loose spacing (24-32px).
- **Inline (horizontal):** Space between items in a row. Icon-to-text gap: 8px. Button gap in a group: 12-16px.
- **Section:** Space between major page sections: 48-64px minimum.

## Common violations
- Mixing spacing values with no relationship (7px here, 13px there, 22px elsewhere)
- Inconsistent padding within similar components
- Too-tight spacing between form labels and inputs (<8px)
- No visual separation between unrelated content groups

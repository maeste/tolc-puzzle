---
id: TOLC-55
title: TOLC-55 — Add Parameter Effect on Function Graphs
status: Done
assignee: []
created_date: '2026-03-13 11:27'
updated_date: '2026-03-13 13:19'
labels:
  - gap-G7
  - functions
  - graphs
milestone: m-4
dependencies: []
references:
  - exercises/graph_reader.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add templates testing how changing parameters affects function graphs. Syllabus: "Occorre avere presente come varia il comportamento e come si modifica il grafico delle funzioni di una certa famiglia al variare dei parametri."
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add 6+ templates in graph_reader.py: L1 (how does graph of y=ax² change as a changes?), L2 (match graph to f(x-a) vs f(x)+a), L3 (identify af(x) vs f(ax) from graph)
- [x] #2 Include parameter families: quadratic (a,b,c), exponential (base), logarithmic (base), sinusoidal (amplitude, frequency, phase)
- [x] #3 Transformation identification as standalone skill: 'Quale trasformazione è stata applicata al grafico di f per ottenere g?'
- [x] #4 Tests: ≥25 automated tests
- [x] #5 Update claudedocs/tolc-b-coverage-analysis.md §2.2
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added 8 parameter effect templates to graph_reader.py + _build_svg_multi helper:

- L1: _template_param_quadratic_a (effect of a on parabola width), _template_param_vertical_shift (f(x)+k)
- L2: _template_param_horizontal_shift (f(x-h) — tricky sign), _template_param_vertical_stretch (af(x)), _template_param_reflection (-f(x) vs f(-x))
- L3: _template_param_combined (af(x-h)+k formula), _template_param_family_effect (sin amplitude/frequency, exp base), _template_param_identify_formula (match transformed graph to formula)

38 automated tests in tests/test_parameter_effects.py. Multi-curve SVG with different colors. Integrated at ~18% probability. Coverage doc updated §2.2.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

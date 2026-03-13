---
id: TOLC-53
title: TOLC-53 — Add Functional Equations/Inequalities from Graphs
status: Done
assignee: []
created_date: '2026-03-13 11:27'
updated_date: '2026-03-13 13:19'
labels:
  - gap-G4
  - functions
  - graphs
  - syllabus-gap
milestone: m-4
dependencies: []
references:
  - exercises/graph_reader.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add templates for "from this graph, solve f(x)=a" and "for which x is f(x)>a?" — reading solutions of functional equations and inequalities directly from graphs. The syllabus explicitly lists "Equazioni e disequazioni espresse mediante funzioni, ad esempio del tipo f(x) = g(x), f(x) > a." We have some inverse reading templates but they don't systematically cover this.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add 6+ templates in graph_reader.py: L1 (f(x)=a, find x from graph), L2 (f(x)>a, find interval from graph), L3 (f(x)=g(x), find intersection from two graphs)
- [x] #2 SVG shows function graph with horizontal line y=a (dashed) for visual clarity
- [x] #3 For L3: SVG shows two function curves, student identifies intersection x-values
- [x] #4 Answers in interval notation or set of x-values
- [x] #5 Tests: ≥25 automated tests
- [x] #6 Update claudedocs/tolc-b-coverage-analysis.md §2.2 and §2.4
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented 7 functional equation/inequality templates in graph_reader.py:
- L1: _template_equation_simple (f(x)=a, find x), _template_equation_count (count solutions)
- L2: _template_inequality_interval (f(x)>a intervals), _template_inequality_sign (f(x)≥0)
- L3: _template_equation_two_functions (f(x)=g(x) intersections), _template_inequality_two_functions (f(x)>g(x)), _template_equation_solutions_range (solutions in [c,d])

SVG includes dashed horizontal line y=a and two-function plots. 64 automated tests in tests/test_graph_equations.py. Integrated into generate() at ~20% probability. Coverage doc updated §2.2.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

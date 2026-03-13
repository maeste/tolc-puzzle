---
id: TOLC-53
title: TOLC-53 — Add Functional Equations/Inequalities from Graphs
status: To Do
assignee: []
created_date: '2026-03-13 11:27'
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
- [ ] #1 Add 6+ templates in graph_reader.py: L1 (f(x)=a, find x from graph), L2 (f(x)>a, find interval from graph), L3 (f(x)=g(x), find intersection from two graphs)
- [ ] #2 SVG shows function graph with horizontal line y=a (dashed) for visual clarity
- [ ] #3 For L3: SVG shows two function curves, student identifies intersection x-values
- [ ] #4 Answers in interval notation or set of x-values
- [ ] #5 Tests: ≥25 automated tests
- [ ] #6 Update claudedocs/tolc-b-coverage-analysis.md §2.2 and §2.4
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

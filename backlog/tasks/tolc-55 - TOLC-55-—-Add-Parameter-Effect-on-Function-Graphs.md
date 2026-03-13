---
id: TOLC-55
title: TOLC-55 — Add Parameter Effect on Function Graphs
status: To Do
assignee: []
created_date: '2026-03-13 11:27'
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
- [ ] #1 Add 6+ templates in graph_reader.py: L1 (how does graph of y=ax² change as a changes?), L2 (match graph to f(x-a) vs f(x)+a), L3 (identify af(x) vs f(ax) from graph)
- [ ] #2 Include parameter families: quadratic (a,b,c), exponential (base), logarithmic (base), sinusoidal (amplitude, frequency, phase)
- [ ] #3 Transformation identification as standalone skill: 'Quale trasformazione è stata applicata al grafico di f per ottenere g?'
- [ ] #4 Tests: ≥25 automated tests
- [ ] #5 Update claudedocs/tolc-b-coverage-analysis.md §2.2
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

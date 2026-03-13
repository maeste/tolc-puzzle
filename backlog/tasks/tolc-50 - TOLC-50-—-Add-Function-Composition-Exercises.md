---
id: TOLC-50
title: TOLC-50 — Add Function Composition Exercises
status: To Do
assignee: []
created_date: '2026-03-13 11:27'
labels:
  - gap-G1
  - functions
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
Create templates for f(g(x)) evaluation, composition identification, and domain of composed functions. This is explicitly in the CISIA syllabus under "Composizione di funzioni" and completely missing from our app.

Implementation hints: Can extend GraphReader or create a new FunctionComposition module. Consider questions like "Se f(x)=2x+1 e g(x)=x², quanto vale f(g(3))?" and "Quale delle seguenti è f(g(x)) se f(x)=√x e g(x)=x+4?"
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add 6+ templates in graph_reader.py or a dedicated section: L1 (evaluate f(g(a)) with simple functions), L2 (identify f∘g from table/formula), L3 (domain restrictions of f(g(x)))
- [ ] #2 Templates use function families already in GraphReader (polynomial, exp, log, trig)
- [ ] #3 At least 20 parametric variations per template (no repetition)
- [ ] #4 5-option multiple choice format compatible with exam simulation
- [ ] #5 Tests: ≥30 automated tests covering all templates and edge cases
- [ ] #6 Update claudedocs/tolc-b-coverage-analysis.md §2.2 Funzioni: mark 'Composizione di funzioni' as IMPLEMENTATO
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

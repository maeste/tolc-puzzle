---
id: TOLC-50
title: TOLC-50 — Add Function Composition Exercises
status: Done
assignee: []
created_date: '2026-03-13 11:27'
updated_date: '2026-03-14 12:00'
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
- [x] #1 Add 6+ templates in graph_reader.py or a dedicated section: L1 (evaluate f(g(a)) with simple functions), L2 (identify f∘g from table/formula), L3 (domain restrictions of f(g(x)))
- [x] #2 Templates use function families already in GraphReader (polynomial, exp, log, trig)
- [x] #3 At least 20 parametric variations per template (no repetition)
- [x] #4 5-option multiple choice format compatible with exam simulation
- [x] #5 Tests: ≥30 automated tests covering all templates and edge cases
- [x] #6 Update claudedocs/tolc-b-coverage-analysis.md §2.2 Funzioni: mark 'Composizione di funzioni' as IMPLEMENTATO
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan — TOLC-50: Function Composition

### Approach
Create a new module `exercises/function_composition.py` (cleaner than extending graph_reader.py which is already large).

### Templates (7 total, 2+ per difficulty level):
**L1:**
1. `_evaluate_composition` — "Se f(x)=2x+1 e g(x)=x², quanto vale f(g(3))?" Direct numeric evaluation.
2. `_identify_composition_formula` — "Se f(x)=√x e g(x)=x+4, quale è f(g(x))?" Identify the composed formula.

**L2:**
3. `_composition_from_table` — Given tables for f and g, compute f(g(x)) for specific values.
4. `_order_matters` — "f(g(x)) vs g(f(x)) — quale è corretta?" Show both orders differ.
5. `_decompose_function` — "La funzione h(x)=√(2x+1) può essere scritta come f(g(x)) con..."

**L3:**
6. `_domain_of_composition` — "Qual è il dominio di f(g(x)) se f(x)=ln(x) e g(x)=x²-4?"
7. `_triple_composition` — "Calcola f(g(h(2))) con f, g, h date"

### Function families (reuse from GraphReader):
- Polynomial: linear, quadratic
- Transcendental: exp, log, sqrt
- Trig: sin, cos

### Registration:
- Add to app.py EXERCISE_TYPES as "composition"
- Add to REALISTIC_EXAM_WEIGHTS with weight 1 (steal from "graph" or "word" to stay at 20)

### Tests: tests/test_function_composition.py
- Parametrized over 20 runs per template
- Check method tests
- Validate 5 distinct options, Italian text

### Files to create/modify:
- CREATE: exercises/function_composition.py
- CREATE: tests/test_function_composition.py
- MODIFY: app.py (register + add to exam weights)
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented: exercises/function_composition.py (7 templates, 3 difficulty levels), tests/test_function_composition.py (162 tests), app.py (registered + added to exam weights, word reduced from 2→1 to compensate). All 1759 tests pass.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-50: Function Composition — Complete

### Changes
- **NEW** `exercises/function_composition.py`: 7 templates across 3 difficulty levels
  - L1: evaluate_composition, identify_composition_formula
  - L2: composition_from_table, order_matters, decompose_function
  - L3: domain_of_composition, triple_composition
- **NEW** `tests/test_function_composition.py`: 162 tests
- **MODIFIED** `app.py`: registered as "composition", added to EXERCISE_TYPES and REALISTIC_EXAM_WEIGHTS (weight 1)
- **MODIFIED** `claudedocs/tolc-b-coverage-analysis.md`: §2.2 updated, registro modifiche entry added

### Metrics
- Templates: 7 (target: 6+)
- Tests: 162 (target: 30+)
- Full suite: 1804 passed
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

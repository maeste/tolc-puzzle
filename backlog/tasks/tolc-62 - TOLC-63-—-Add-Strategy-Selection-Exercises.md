---
id: TOLC-62
title: TOLC-63 — Add Strategy Selection Exercises
status: Done
assignee: []
created_date: '2026-03-13 11:28'
updated_date: '2026-03-13 23:38'
labels:
  - gap-G13
  - mindset
  - strategy
milestone: m-4
dependencies: []
references:
  - claudedocs/tolc-b-coverage-analysis.md
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The CISIA syllabus emphasizes "scegliere una strategia di operazioni efficace" and "scegliere quelle [procedure] più efficienti e più semplici." We have no exercise that tests whether students can identify the BEST approach to solve a problem. This is a mindset skill, not just a knowledge skill.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add 4-6 templates (new module or integrated into existing): L1 (given an equation, which method solves it fastest: factoring vs formula vs substitution?), L2 (given an expression, which simplification path is shortest?), L3 (given a geometry problem, which approach works: coordinates vs synthetic vs trigonometric?)
- [x] #2 Question format: 'Quale strategia è più efficiente per risolvere...?' with 5 strategy options
- [x] #3 Include brief explanation of WHY one strategy is better (educational value)
- [x] #4 5-option multiple choice format
- [x] #5 Tests: ≥15 automated tests
- [x] #6 Update claudedocs/tolc-b-coverage-analysis.md §2.9: add new cognitive competency 'Scelta strategica'
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

1. Create `exercises/strategy_selection.py` with class `StrategySelection(Exercise)`
2. Implement 4-6 templates across 3 difficulty levels:
   - L1: Which method solves this equation fastest? (factoring vs formula vs substitution)
   - L2: Which simplification path is shortest for this expression?
   - L3: Which approach works best for this geometry problem? (coordinates vs synthetic vs trigonometric)
3. Question format: "Quale strategia è più efficiente per risolvere...?" with 5 options
4. Include explanation of WHY one strategy is better
5. Register in `app.py` (EXERCISE_TYPES + exercise_registry)
6. Create `tests/test_strategy_selection.py` with ≥15 tests
7. Update `claudedocs/tolc-b-coverage-analysis.md` §2.9
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-62 Complete — Strategy Selection Exercises

### Deliverables
- **`exercises/strategy_selection.py`**: `StrategySelection(Exercise)` with 12 templates across 3 difficulty levels:
  - L1 (4 templates): Equation solving strategy — simple linear, factorable quadratic, irrational roots quadratic, perfect square quadratic
  - L2 (4 templates): Expression simplification — common factor, difference of squares, sum/difference of cubes, completing the square
  - L3 (4 templates): Geometry approach — collinear points, angle from sides, polygon area, perpendicular bisector
- **`tests/test_strategy_selection.py`**: 28 tests (structure, options quality, difficulty clamping, approfondimento flags, check method, template coverage, question content, variation)
- **`app.py`**: Registered as `"strategy"` in EXERCISE_TYPES and exercise_registry
- **`claudedocs/tolc-b-coverage-analysis.md`**: §2.9 updated with 'Scelta strategica' competency

### Metrics
- 12 templates, 28 tests, all passing
- Question format: "Quale strategia è più efficiente per risolvere...?" with 5 strategy options
- Each answer includes explanation of WHY the strategy is best
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

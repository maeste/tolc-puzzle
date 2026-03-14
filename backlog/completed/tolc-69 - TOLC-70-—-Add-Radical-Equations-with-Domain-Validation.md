---
id: TOLC-69
title: TOLC-70 — Add Radical Equations with Domain Validation
status: Done
assignee: []
created_date: '2026-03-14 00:15'
updated_date: '2026-03-14 22:59'
labels:
  - gap-v5
  - algebra
  - radical-equations
milestone: m-5
dependencies: []
references:
  - exercises/solve_exercise.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add templates for radical equations that require domain checking and extraneous solution detection.

This gap was identified in Assessment v5 from question C8 (Ca' Foscari): "Risolvi √(2-x)=x" where squaring both sides introduces extraneous solutions that must be checked against the domain constraint.

**Implementation Plan:**
1. Add templates in `exercises/solve_exercise.py`:
   - L2: `_solve_radical_simple` — √(ax+b)=c, solve and verify c≥0. Simple domain check.
   - L2: `_solve_radical_linear` — √(ax+b)=cx+d, square both sides, solve quadratic, check both solutions against domain (radicand ≥ 0 AND right side ≥ 0)
   - L3: `_solve_radical_two_radicals` — √(ax+b)=√(cx+d)+e, isolate one radical, square, repeat if needed. Multiple domain constraints.
   - L3: `_solve_radical_extraneous` — deliberately generate equation where one solution is extraneous. Question: "Quante soluzioni ha l'equazione?"

2. Key pedagogical element: distractors include the extraneous solution as a trap option.

3. Add to appropriate template lists in SolveExercise class.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add 4 templates (2 L2, 2 L3) for radical equations in solve_exercise.py
- [x] #2 L2: simple radical + radical=linear, L3: two radicals + extraneous solution detection
- [x] #3 Include domain validation: radicand ≥ 0, right side ≥ 0 after squaring
- [x] #4 Distractors include extraneous solutions as trap options
- [x] #5 Integer coefficients ensuring at least one valid solution exists
- [x] #6 Tests: ≥20 automated tests covering valid solutions, extraneous detection, domain constraints
- [x] #7 Update claudedocs/tolc-b-coverage-analysis.md: update §2.1 Algebra, mark radical equations as IMPLEMENTATO
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-69: Radical Equations with Domain Validation — Complete\n\n### Changes\n- **MODIFIED** `exercises/solve_exercise.py`: Added 4 radical equation templates + _STRING_TEMPLATES_L3 list:\n  - L2: _t2_solve_radical_simple, _t2_solve_radical_linear\n  - L3: _t3_solve_radical_two_radicals, _t3_solve_radical_extraneous\n- **NEW** `tests/test_radical_equations.py`: 37 tests\n\n### Metrics\n- Tests: 37 new\n- Full suite: 2598 passed
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

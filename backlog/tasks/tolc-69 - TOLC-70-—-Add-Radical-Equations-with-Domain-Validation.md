---
id: TOLC-69
title: TOLC-70 — Add Radical Equations with Domain Validation
status: To Do
assignee: []
created_date: '2026-03-14 00:15'
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
- [ ] #1 Add 4 templates (2 L2, 2 L3) for radical equations in solve_exercise.py
- [ ] #2 L2: simple radical + radical=linear, L3: two radicals + extraneous solution detection
- [ ] #3 Include domain validation: radicand ≥ 0, right side ≥ 0 after squaring
- [ ] #4 Distractors include extraneous solutions as trap options
- [ ] #5 Integer coefficients ensuring at least one valid solution exists
- [ ] #6 Tests: ≥20 automated tests covering valid solutions, extraneous detection, domain constraints
- [ ] #7 Update claudedocs/tolc-b-coverage-analysis.md: update §2.1 Algebra, mark radical equations as IMPLEMENTATO
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

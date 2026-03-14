---
id: TOLC-65
title: TOLC-66 — Add Parametric Equation Analysis
status: Done
assignee: []
created_date: '2026-03-14 00:15'
updated_date: '2026-03-14 22:44'
labels:
  - gap-v5
  - algebra
  - parametric
milestone: m-5
dependencies: []
references:
  - exercises/which_satisfies.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add templates for parametric equation analysis: "For which value of parameter a does the equation have no solution / infinite solutions / exactly one solution?"

This gap was identified in Assessment v5 (§11.9) from question C9 (Ca' Foscari TOLC-E): "(2a-1)x=6, per quale valore di a l'equazione è impossibile?" and E4 (Test Ingegneria): "x²+(k+2)x+k²=0 senza soluzioni per...?"

**Implementation Plan:**
1. Add templates in `exercises/which_satisfies.py` (best fit — meta-format "which value makes..."):
   - L1: `_which_param_linear_impossible` — linear equation ax+b=c with parameter, find value making it impossible (coefficient of x = 0)
   - L1: `_which_param_linear_infinite` — linear equation with parameter, find value giving infinite solutions (0x = 0)
   - L2: `_which_param_quadratic_no_real` — quadratic with parameter in coefficients, find range of parameter making discriminant negative
   - L2: `_which_param_quadratic_one_solution` — find parameter making discriminant = 0
   - L3: `_which_param_quadratic_positive_roots` — find parameter range for both roots positive (Vieta's formulas)
   - L3: `_which_param_system_inconsistent` — 2x2 system with parameter, find value making determinant = 0

2. Each template generates 5 options (parameter values or ranges), with distractors based on common errors (forgetting domain, sign errors, confusing impossible vs indeterminate).

3. All questions in Italian: "Per quale valore di a l'equazione ... non ha soluzioni reali?"

4. Register no new type needed — templates added to existing WhichSatisfies module.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add 6 templates (2 per level) for parametric equation analysis in which_satisfies.py
- [x] #2 L1: linear parameter (impossible/infinite), L2: quadratic discriminant (no real / one solution), L3: root conditions (Vieta) + system consistency
- [x] #3 Distractors based on common student errors: sign mistakes, forgetting domain constraints, confusing impossible vs indeterminate
- [x] #4 All question text in Italian with clear mathematical notation
- [x] #5 5-option multiple choice format compatible with exam simulation
- [x] #6 Tests: ≥25 automated tests covering all templates, edge cases (a=0, negative parameters), and distractor uniqueness
- [x] #7 Update claudedocs/tolc-b-coverage-analysis.md §11.9: mark parametric equations gap as resolved
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-65: Parametric Equation Analysis — Complete

### Changes
- **MODIFIED** `exercises/which_satisfies.py`: Added 6 parametric equation templates:
  - L1: _which_param_linear_impossible, _which_param_linear_infinite
  - L2: _which_param_quadratic_no_real, _which_param_quadratic_one_solution
  - L3: _which_param_quadratic_positive_roots, _which_param_system_inconsistent
- **MODIFIED** `tests/test_which_satisfies.py`: Fixed overly strict test on option format
- **NEW** `tests/test_parametric_equations.py`: 59 tests

### Metrics
- Tests: 59 new
- Full suite: 2411 passed
- Gap §11.9 (parametric equations) resolved
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

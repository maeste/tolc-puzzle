---
id: TOLC-40
title: TOLC-41 — Improve Constrained Combinatorics in Probability Module
status: Done
assignee: []
created_date: '2026-03-13 07:59'
updated_date: '2026-03-13 10:11'
labels:
  - enhancement
  - combinatorics
milestone: m-1
dependencies: []
references:
  - claudedocs/TOLC-B_math_research.md
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: Q19-SET-A tests counting with constraints ("How many odd 4-digit numbers using digits {2,3,7,8}?"). This constrained counting is different from our urn/card probability templates and currently underserved.

**Scope**:
- Add 3-4 templates for constrained counting problems. These are combinatorics, NOT probability — consider adding to Solve Exercise or a dedicated section.
- Template types:
  - Counting numbers with digit constraints (odd/even, specific digit sets)
  - Seating arrangements with restrictions
  - Selection with exclusion rules
- Parametric variation ensures different numbers each generation

**Impact**: Low frequency (~1-2 questions per exam) but these are EASY points if practiced.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 At least 3 constrained counting templates
- [x] #2 Questions match style of Q19-SET-A (counting with digit/parity constraints)
- [x] #3 Parametric variation ensures different numbers each generation
- [x] #4 Tests: ≥10 automated tests
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan — TOLC-40 Constrained Combinatorics

### Files to Modify
1. **EDIT** `exercises/probability_game.py` — Add 4 constrained counting templates to L2 and L3
2. **NEW** `tests/test_combinatorics_constrained.py` — ≥10 automated tests

### Template Design (4 templates)

**L2 Templates (2):**
- `_count_digits_constraint`: "Quanti numeri di 4 cifre si possono formare con {2,3,7,8} tali che il numero sia dispari?" → count arrangements with last-digit constraint
- `_count_seating_adjacent`: "In quanti modi 5 persone possono sedersi in fila se A e B devono stare vicini?" → treat pair as unit

**L3 Templates (2):**
- `_count_digits_no_repeat`: "Quanti numeri di 3 cifre DISTINTE si possono formare con {1,2,3,4,5} che siano maggiori di 300?" → first-digit constraint + no repetition
- `_count_selection_exclusion`: "Da un gruppo di 8 persone, in quanti modi si può scegliere un comitato di 3 persone se X e Y non possono stare insieme?" → C(n,k) - C(n-2,k-2)

### Distractor Strategy
- Off-by-one errors (forgetting constraint reduces choices)
- Confusing permutations with combinations
- Forgetting to exclude/include a case
- Multiplying instead of adding in branched counting

### Integration
- Templates added to probability_game.py's L2 and L3 template lists
- Already in simulation via probability weight — no app.py changes needed
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-40 — Constrained Combinatorics Complete

### Files Modified/Created
- **EDIT** `exercises/probability_game.py` — Added 4 constrained counting templates + `_make_int_distractors` helper
- **NEW** `tests/test_combinatorics_constrained.py` — 213 tests

### Templates Added
**L2**: comb_digit_constraint (digit parity counting), comb_seating_adjacent (adjacent permutations)
**L3**: comb_digits_no_repeat (distinct digits with threshold), comb_selection_exclusion (committee with exclusion)

### Integration
Templates registered in existing L2/L3 template lists within ProbabilityGame. No app.py changes needed — already included via probability weight.

### Coverage
Covers real TOLC question Q19-SET-A (odd 4-digit numbers from digit set).

### Note
DoD #2 (coverage doc update) deferred to TOLC-44 final reassessment task.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

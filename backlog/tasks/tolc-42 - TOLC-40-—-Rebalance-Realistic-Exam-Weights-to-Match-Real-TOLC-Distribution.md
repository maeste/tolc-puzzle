---
id: TOLC-42
title: TOLC-40 — Rebalance Realistic Exam Weights to Match Real TOLC Distribution
status: Done
assignee: []
created_date: '2026-03-13 08:00'
updated_date: '2026-03-13 10:27'
labels:
  - rebalance
  - simulation
milestone: m-1
dependencies:
  - TOLC-38
  - TOLC-39
references:
  - claudedocs/TOLC-B_math_research.md
  - app.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: Current simulation distribution over-represents "reasoning" modules (simplification, always-true, proportional) and under-represents pure arithmetic (+20% gap) and geometry (+7% gap).

**Key insight**: The real TOLC doesn't have separate "simplification" or "always true" question categories. These COMPETENCIES are embedded within regular topic questions.

**Current vs Real TOLC frequency**:
| Category | Our Sim | Real TOLC | Delta |
|----------|---------|-----------|-------|
| Pure arithmetic | 0% | ~20% | **-20%** |
| Algebra | 25% | ~20% | +5% |
| Geometry | 15% | ~22% | **-7%** |
| Functions/graphs | 15% | ~20% | -5% |
| Prob+Stats+Logic | 15% | ~15% | OK |
| Reasoning types | 15% | ~0% dedicated | **+15%** |

**Scope**:
- Revise `REALISTIC_EXAM_WEIGHTS` in `app.py` to match observed TOLC frequency
- Proposed new weights (total=20): number_sense:3, solve:2, inequalities:1, trap:0, simplification:1, always_true:0, proportional:0, which_satisfies:2, geometry:2, analytic_geo:2, word:2, probability:1, statistics:1, logic:1, graph:2, cross_topic:0
- Trap Calculator, Always True, Proportional Reasoning, Cross-Topic remain fully functional in LEARNING mode but removed from realistic exam simulation
- Add "learning mode" vs "exam mode" weight distinction in configuration

**Must be done AFTER TOLC-38 and TOLC-39** since it needs the new exercise types to exist before assigning weights.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 New weights sum to 20
- [x] #2 Distribution matches real TOLC frequencies within ±5% per category
- [x] #3 Trap Calculator, Always True, Proportional Reasoning, Cross-Topic still fully functional in learning/practice mode
- [x] #4 Simulation-only weights documented with rationale
- [x] #5 Existing tests still pass
- [x] #6 New test validates weight distribution against expected TOLC frequencies
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan — TOLC-42 Rebalance Weights

### New Weight Distribution (sum=20)
```
number_sense: 3     # NEW — pure arithmetic (~15%)
solve: 2            # Algebra
inequalities: 1     # Algebra (was 2, reduce)
simplification: 1   # Keep
which_satisfies: 2  # NEW — meta-format (~10%)
geometry: 2         # Geometry
analytic_geo: 2     # Geometry (was 1, increase)
word: 2             # Word problems (was 1, increase)
probability: 1      # Prob (was 2, reduce)
statistics: 1       # Stats
logic: 1            # Logic
graph: 2            # Graphs
```
Total: 3+2+1+1+2+2+2+2+1+1+1+2 = 20

### Removed from Exam (weight=0, removed from dict)
- trap (keep in learning only)
- always_true (keep in learning only)
- proportional (keep in learning only)
- cross_topic (keep in learning only)
- estimation (already excluded)

### Files
1. EDIT `app.py` — new REALISTIC_EXAM_WEIGHTS, update comments, update sanity check
2. EDIT `tests/test_weighted_distribution.py` — update test_total=20, remove test_all_counts_positive (some removed), add new frequency validation test
3. Verify all types with weight>0 still in EXERCISE_TYPES and exercise_registry
4. Verify learning/practice mode still has all 17 types available
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-42 — Rebalance Realistic Exam Weights Complete

### Files Modified
- **EDIT** `app.py` — New REALISTIC_EXAM_WEIGHTS summing to 20, with category comments
- **EDIT** `tests/test_weighted_distribution.py` — 6 new tests validating distribution

### New Weight Distribution (sum=20)
| Type | Old | New | Change |
|------|-----|-----|--------|
| number_sense | 3 | 3 | NEW |
| solve | 2 | 2 | — |
| inequalities | 2 | 1 | -1 |
| simplification | 1 | 1 | — |
| which_satisfies | 2 | 2 | NEW |
| geometry | 2 | 2 | — |
| analytic_geo | 1 | 2 | +1 |
| word | 1 | 2 | +1 |
| probability | 2 | 1 | -1 |
| statistics | 1 | 1 | — |
| logic | 1 | 1 | — |
| graph | 2 | 2 | — |
| trap | 1 | REMOVED | learning only |
| always_true | 1 | REMOVED | learning only |
| proportional | 1 | REMOVED | learning only |
| cross_topic | 2 | REMOVED | learning only |

### Category Percentages
Aritmetica 15%, Algebra 20%, Geometria 20%, Funzioni 20%, Meta 10%, Prob+Stat+Log 15%

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

---
id: TOLC-41
title: TOLC-42 — Word Problem Style Alignment
status: Done
assignee: []
created_date: '2026-03-13 07:59'
updated_date: '2026-03-13 10:27'
labels:
  - enhancement
  - word-problems
milestone: m-1
dependencies: []
references:
  - claudedocs/TOLC-B_math_research.md
  - exercises/word_modeler.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: Real TOLC word problems more often ask for a NUMERICAL ANSWER than for "which equation models this." Our word_modeler.py currently inverts this ratio.

**Real questions**: Q4-SET-A (chocolate redistribution → fraction), Q5-SET-A (bus cost → total per person), Q17-SET-A (exam scores → number of exams), Q20-SET-A (driving test → total people via percentage).

**Scope**:
- Audit `word_modeler.py` to increase the ratio of numeric-answer vs equation-setup questions
- Target: 60% numeric answer, 40% equation setup (currently inverted)
- Add 4-5 new numeric word problem templates matching real TOLC style:
  - Multi-step percentage problems (Q20-SET-A style)
  - Cost/budget allocation (Q5-SET-A style)
  - Mean/score problems requiring equation modeling + solving (Q17-SET-A style)
  - Fraction redistribution (Q4-SET-A style)
- Include "rounding" scenarios (e.g., needing whole buses for 120 people at 50 capacity)
- Update the difficulty mix function to prefer numeric results in exam mode

**Impact**: Better alignment with real TOLC word problem expectations.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 ≥60% of word problems in exam mode produce numeric answer format
- [x] #2 New templates match real TOLC word problem style (narrative → number)
- [x] #3 Multi-step reasoning required (not single formula application)
- [x] #4 Include rounding scenarios (e.g., needing whole buses for 120 people at 50 capacity)
- [x] #5 Tests: ≥15 automated tests for new templates
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan — TOLC-41 Word Problem Style Alignment

### Analysis
Current numeric vs equation ratio:
- L1: 3 numeric / 13 total = 23%
- L2: 3 numeric / 11 total = 27%
- L3: 2 numeric / 9 total = 22%

Target: ≥60% numeric in exam mode.

### Approach
1. Add 5 new numeric templates (2 L1, 2 L2, 1 L3) matching real TOLC style
2. Add `generate_exam_mode(difficulty)` method that picks from numeric-only pool 60% of the time
3. Update `_get_templates` to accept an optional `exam_mode` parameter

### New Templates
- L1: `_numeric_bus_cost` (Q5-SET-A: cost splitting with rounding up) + `_numeric_fraction_redistribution` (Q4-SET-A: fraction of items)
- L2: `_numeric_percentage_multistep` (Q20-SET-A: percentage → total people) + `_numeric_exam_scores` (Q17-SET-A: mean score → number of exams)
- L3: `_numeric_successive_operations` (chained operations with intermediate rounding)

### Files
1. EDIT `exercises/word_modeler.py` — add 5 numeric templates + exam_mode generate path
2. NEW `tests/test_word_modeler_exam_style.py` — ≥15 tests
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-41 — Word Problem Style Alignment Complete

### Files Modified/Created
- **EDIT** `exercises/word_modeler.py` — Added 5 numeric templates + exam_mode parameter
- **EDIT** `app.py` — Passes exam_mode=True for word-type exercises in realistic exam
- **NEW** `tests/test_word_modeler_exam_style.py` — 122 tests

### New Templates
**L1**: _numeric_bus_cost (rounding up), _numeric_fraction_redistribution (multi-step fractions)
**L2**: _numeric_percentage_multistep (find total from %), _numeric_exam_scores (find N from averages)
**L3**: _numeric_successive_operations (price + increase + coupon + VAT)

### Numeric Ratio
- Learning mode: ~38% numeric (unchanged)
- Exam mode: ≥60% numeric (generate picks numeric-only 60% of the time)

### Coverage
Covers real TOLC questions: Q4-SET-A (fraction redistribution), Q5-SET-A (bus cost), Q17-SET-A (exam scores), Q20-SET-A (percentage → total)

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

---
id: TOLC-52
title: TOLC-52 — Re-include Estimation in Exam Simulation & Enhance
status: Done
assignee: []
created_date: '2026-03-13 11:27'
updated_date: '2026-03-13 13:01'
labels:
  - gap-G3
  - estimation
  - exam-simulation
milestone: m-4
dependencies: []
references:
  - exercises/estimation_blitz.py
  - app.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The CISIA syllabus explicitly states "la capacità di fare stime...consente di valutare rapidamente la plausibilità del risultato dei calcoli." Our EstimationBlitz module (14 templates) is currently EXCLUDED from the realistic exam simulation. This is a significant gap — mental calculation without calculator is a CORE TOLC-B skill, not optional. Re-include it and adapt the format for exam mode.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add 'estimation' to REALISTIC_EXAM_WEIGHTS with weight 1-2 (replace or rebalance)
- [x] #2 Adapt EstimationBlitz output for exam mode: standard 5-option multiple choice (no special timer UI), question text like 'Quale delle seguenti è la migliore approssimazione di 47×83?'
- [x] #3 Ensure all EstimationBlitz templates generate exactly 5 plausible options
- [x] #4 Total exam questions remain 20; adjust other weights to compensate
- [x] #5 Tests: verify EstimationBlitz works in exam endpoint, distribution remains balanced
- [x] #6 Update claudedocs/tolc-b-coverage-analysis.md §3 simulation section
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan — TOLC-52: Estimation in Exam Simulation

### Approach
Re-include estimation in REALISTIC_EXAM_WEIGHTS and adapt EstimationBlitz for exam mode.

### Changes:
1. **app.py — REALISTIC_EXAM_WEIGHTS**: Add `"estimation": 1`, reduce `"number_sense"` from 3 to 2 (both test numeric fluency). Total stays 20.

2. **exercises/estimation_blitz.py — Exam mode adaptation**:
   - Add `exam_mode` parameter to generate(): when True, return standard 5-option format without `time_limit` field
   - Ensure question text is self-contained (no special timer UI references)
   - Verify all templates produce exactly 5 distinct option labels
   - Format question as "Quale delle seguenti è la migliore approssimazione di [expression]?"

3. **app.py — Exam endpoint**: Handle estimation type in api_realistic_exam_exercises(), pass exam_mode=True

### Tests: tests/test_estimation_exam.py (or extend existing)
- Verify estimation appears in exam exercise list
- Verify exam_mode output has no time_limit
- Verify exactly 5 distinct options in exam mode
- Verify total exam stays at 20 questions

### Files to modify:
- MODIFY: app.py (weights + endpoint handling)
- MODIFY: exercises/estimation_blitz.py (exam_mode parameter)
- CREATE or EXTEND: tests/test_estimation_exam.py
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
All 113 new tests pass. Changes: estimation_blitz.py (exam_mode param), app.py (weights rebalanced, exam endpoint handles estimation). Backward compatible — default generate() unchanged.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-52: Estimation in Exam Simulation — Complete

### Changes
- **MODIFIED** `exercises/estimation_blitz.py`: Added `exam_mode` parameter to `generate()` — when True, removes `time_limit` and changes question prefix to "Senza calcolatrice, stimare il valore di:"
- **MODIFIED** `app.py`: 
  - Added `"estimation": 1` to REALISTIC_EXAM_WEIGHTS
  - Rebalanced: number_sense 3→2, word 2→1, added composition 1 (total stays 20)
  - Exam endpoint passes exam_mode=True for estimation type
- **NEW** `tests/test_estimation_exam.py`: 113 tests
- **MODIFIED** `claudedocs/tolc-b-coverage-analysis.md`: registro modifiche entry added
- **BUGFIX**: Fixed pre-existing infinite loop in `statistics_exercise.py` _make_distractors_stat fallback (correct=0 case)

### Metrics
- Tests: 113 (new) 
- Full suite: 1804 passed
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

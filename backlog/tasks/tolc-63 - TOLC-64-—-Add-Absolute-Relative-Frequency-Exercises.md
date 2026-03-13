---
id: TOLC-63
title: TOLC-64 — Add Absolute/Relative Frequency Exercises
status: Done
assignee: []
created_date: '2026-03-13 11:28'
updated_date: '2026-03-13 23:38'
labels:
  - gap-G14
  - statistics
  - syllabus-gap
milestone: m-4
dependencies: []
references:
  - exercises/statistics_exercise.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The CISIA syllabus lists "Frequenza assoluta e relativa" under the Statistics nucleus. We compute means and medians but don't explicitly test frequency concepts. Adding this completes the statistics syllabus coverage.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add 3-4 templates in statistics_exercise.py: L1 (compute absolute frequency from raw data), L2 (compute relative frequency and convert to percentage), L3 (given a frequency table, reconstruct the dataset or compute statistics)
- [x] #2 Include reading frequency from histograms/bar charts (using existing SVG infrastructure)
- [x] #3 5-option multiple choice format with distractors based on common errors (absolute↔relative confusion, percentage errors)
- [x] #4 Tests: ≥10 automated tests
- [x] #5 Update claudedocs/tolc-b-coverage-analysis.md §2.7: mark 'Frequenza assoluta e relativa' as IMPLEMENTATO
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

1. Add frequency templates to `exercises/statistics_exercise.py`:
   - L1: Compute absolute frequency from raw data
   - L2: Compute relative frequency and convert to percentage
   - L3: Given a frequency table, reconstruct dataset or compute statistics
2. Include reading frequency from histograms (text-based description, consistent with existing SVG infrastructure)
3. 5-option multiple choice with distractors based on common errors (absolute↔relative confusion, percentage errors)
4. Create `tests/test_frequency_exercises.py` with ≥10 tests
5. Update `claudedocs/tolc-b-coverage-analysis.md` §2.7: mark 'Frequenza assoluta e relativa' as IMPLEMENTATO
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-63 Complete — Absolute/Relative Frequency Exercises

### Deliverables
- **`exercises/statistics_exercise.py`**: 5 new frequency templates added:
  - L1: `_t_frequency_absolute_from_data` — compute absolute frequency from raw data
  - L1: `_t_frequency_from_histogram` — read frequency from text-described histogram
  - L2: `_t_frequency_relative_percentage` — compute relative frequency and percentage
  - L2: `_t_frequency_compare` — compare frequencies across categories
  - L3: `_t_frequency_reconstruct_stats` — compute statistics from frequency table
- **`tests/test_frequency_exercises.py`**: 18 tests (direct template tests, integration via generate(), check method)
- **`claudedocs/tolc-b-coverage-analysis.md`**: §2.7 updated — 'Frequenza assoluta e relativa' marked IMPLEMENTATO

### Bug Fixed
- Fixed infinite loop in `_make_distractors()` when correct value is negative (e.g., bar chart differences). The `d > 0` guard in while loops prevented generating any distractors for negative answers.

### Metrics
- 5 templates (2 L1, 2 L2, 1 L3), 18 tests, all passing
- Statistics module now has 23 templates total (was 18)
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

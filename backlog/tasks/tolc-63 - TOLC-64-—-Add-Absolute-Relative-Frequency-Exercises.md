---
id: TOLC-63
title: TOLC-64 — Add Absolute/Relative Frequency Exercises
status: To Do
assignee: []
created_date: '2026-03-13 11:28'
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
- [ ] #1 Add 3-4 templates in statistics_exercise.py: L1 (compute absolute frequency from raw data), L2 (compute relative frequency and convert to percentage), L3 (given a frequency table, reconstruct the dataset or compute statistics)
- [ ] #2 Include reading frequency from histograms/bar charts (using existing SVG infrastructure)
- [ ] #3 5-option multiple choice format with distractors based on common errors (absolute↔relative confusion, percentage errors)
- [ ] #4 Tests: ≥10 automated tests
- [ ] #5 Update claudedocs/tolc-b-coverage-analysis.md §2.7: mark 'Frequenza assoluta e relativa' as IMPLEMENTATO
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

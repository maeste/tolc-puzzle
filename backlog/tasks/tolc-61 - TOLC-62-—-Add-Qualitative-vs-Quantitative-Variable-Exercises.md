---
id: TOLC-61
title: TOLC-62 — Add Qualitative vs Quantitative Variable Exercises
status: To Do
assignee: []
created_date: '2026-03-13 11:28'
labels:
  - gap-G12
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
The CISIA syllabus lists "Variabili qualitative e quantitative (discrete e continue)" under the Statistics nucleus. We have no template that tests whether students can distinguish variable types. Basic but explicitly in syllabus.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add 3-4 templates in statistics_exercise.py: L1 (classify a variable as qualitative/quantitative), L2 (classify as discrete vs continuous + identify appropriate graph type), L3 (given a dataset description, identify all variable types and choose correct representation)
- [ ] #2 Use realistic Italian contexts (school grades, temperatures, eye color, height, city of origin)
- [ ] #3 5-option multiple choice format
- [ ] #4 Tests: ≥10 automated tests
- [ ] #5 Update claudedocs/tolc-b-coverage-analysis.md §2.7: mark 'Variabili qualitative e quantitative' as IMPLEMENTATO
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

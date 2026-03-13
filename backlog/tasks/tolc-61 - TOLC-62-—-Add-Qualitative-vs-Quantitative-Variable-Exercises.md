---
id: TOLC-61
title: TOLC-62 — Add Qualitative vs Quantitative Variable Exercises
status: Done
assignee: []
created_date: '2026-03-13 11:28'
updated_date: '2026-03-13 22:51'
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
- [x] #1 Add 3-4 templates in statistics_exercise.py: L1 (classify a variable as qualitative/quantitative), L2 (classify as discrete vs continuous + identify appropriate graph type), L3 (given a dataset description, identify all variable types and choose correct representation)
- [x] #2 Use realistic Italian contexts (school grades, temperatures, eye color, height, city of origin)
- [x] #3 5-option multiple choice format
- [x] #4 Tests: ≥10 automated tests
- [x] #5 Update claudedocs/tolc-b-coverage-analysis.md §2.7: mark 'Variabili qualitative e quantitative' as IMPLEMENTATO
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented 4 variable classification templates in statistics_exercise.py:\n- _t_variable_classification_basic (L1): classify variable as qualitativa/quantitativa\n- _t_variable_classification_with_graph (L2): classify + identify appropriate graph type\n- _t_discrete_vs_continuous (L2): distinguish discrete vs continuous quantitative\n- _t_variable_classification_dataset (L3): analyze dataset with multiple variables\n\nUses realistic Italian contexts (voti, temperatura, colore occhi, altezza, città). Returns full dicts bypassing numeric distractor pipeline via _DICT_TEMPLATES sentinel.\n26 automated tests in tests/test_variable_classification.py — all passing.\nCoverage doc updated in §2.7.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

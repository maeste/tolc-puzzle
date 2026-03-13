---
id: TOLC-60
title: TOLC-61 — Add Division with Remainder Exercises
status: To Do
assignee: []
created_date: '2026-03-13 11:28'
labels:
  - gap-G11
  - numbers
  - syllabus-gap
milestone: m-4
dependencies: []
references:
  - exercises/number_sense.py
  - exercises/solve_exercise.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The CISIA syllabus explicitly lists "Divisione con resto tra numeri interi" under the Numbers nucleus. We have no template covering integer division with remainder. While rare in real exams, it's a syllabus item and tests number fluency.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add 3-4 templates in number_sense.py or solve_exercise.py: L1 (what is the remainder of a÷b?), L2 (which number gives remainder r when divided by d?), L3 (word problem using division with remainder, e.g., '48 students in groups of 5, how many groups and how many left over?')
- [ ] #2 5-option multiple choice format
- [ ] #3 Include distractors based on common errors (confusing quotient with remainder, off-by-one)
- [ ] #4 Tests: ≥10 automated tests
- [ ] #5 Update claudedocs/tolc-b-coverage-analysis.md §2.1: mark 'Divisione con resto' as IMPLEMENTATO
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

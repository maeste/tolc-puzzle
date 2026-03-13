---
id: TOLC-54
title: TOLC-54 — Expand Similar Triangles & Trig Ratios
status: To Do
assignee: []
created_date: '2026-03-13 11:27'
labels:
  - gap-G5
  - gap-G6
  - geometry
  - trigonometry
milestone: m-4
dependencies: []
references:
  - exercises/geometry_sherlock.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Expand coverage of similar triangles (currently only 1 template) and add dedicated trigonometric ratios exercises. Syllabus explicitly lists "Proprietà dei triangoli simili" and "Seno, coseno e tangente di un angolo, ottenuti come rapporti fra i lati di un triangolo rettangolo."
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add 4+ similar triangle templates in geometry_sherlock.py: find unknown side via ratio, scale factor from two figures, area ratio from length ratio, real-world similarity problem
- [ ] #2 Add 4+ trig ratio templates: find sin/cos/tan given sides, find side given angle and one side, identify angle from ratio, apply to real-world scenario (height of building, etc.)
- [ ] #3 All with SVG diagrams for learning mode
- [ ] #4 Tests: ≥20 automated tests
- [ ] #5 Update claudedocs/tolc-b-coverage-analysis.md §2.3
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

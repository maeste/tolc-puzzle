---
id: TOLC-54
title: TOLC-54 — Expand Similar Triangles & Trig Ratios
status: Done
assignee: []
created_date: '2026-03-13 11:27'
updated_date: '2026-03-13 13:19'
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
- [x] #1 Add 4+ similar triangle templates in geometry_sherlock.py: find unknown side via ratio, scale factor from two figures, area ratio from length ratio, real-world similarity problem
- [x] #2 Add 4+ trig ratio templates: find sin/cos/tan given sides, find side given angle and one side, identify angle from ratio, apply to real-world scenario (height of building, etc.)
- [x] #3 All with SVG diagrams for learning mode
- [x] #4 Tests: ≥20 automated tests
- [x] #5 Update claudedocs/tolc-b-coverage-analysis.md §2.3
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added 8 templates to geometry_sherlock.py:

Similar Triangles (4):
- _t2_similar_find_side: unknown side via proportion
- _t2_similar_scale_factor: determine k from corresponding sides
- _t2_similar_area_ratio: area ratio from k²
- _t3_similar_real_world: shadow/height proportion problem

Trig Ratios (4):
- _t2_trig_find_ratio: sin/cos/tan given sides
- _t2_trig_find_side: side given angle (30/45/60) and one side
- _t3_trig_identify_angle: angle from two sides
- _t3_trig_real_world: building height with tan

71 automated tests in tests/test_similar_trig.py. All with SVG diagrams. Coverage doc updated §2.3.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

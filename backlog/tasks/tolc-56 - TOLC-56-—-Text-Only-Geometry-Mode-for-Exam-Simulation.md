---
id: TOLC-56
title: TOLC-56 — Text-Only Geometry Mode for Exam Simulation
status: Done
assignee: []
created_date: '2026-03-13 11:27'
updated_date: '2026-03-13 22:03'
labels:
  - gap-G8
  - geometry
  - exam-simulation
milestone: m-4
dependencies: []
references:
  - exercises/geometry_sherlock.py
  - app.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
In the real TOLC-B, most geometry problems are text-described without diagrams. Our simulation shows SVG diagrams which makes geometry EASIER than the real test. Add a text-only mode for geometry in exam simulation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add 'text_only' parameter to GeometrySherlock.generate() that suppresses SVG graph_data
- [x] #2 When called from exam simulation, geometry exercises use text-only mode (no SVG)
- [x] #3 SVG remains available in learning mode (the SVG is valuable for learning!)
- [x] #4 Question text must be self-contained (describe the figure verbally)
- [x] #5 Tests: verify exam endpoint returns geometry without graph_data, learning mode still has it
- [x] #6 Update claudedocs/tolc-b-coverage-analysis.md §10.7 simulation realism
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented text-only geometry mode for exam simulation. GeometrySherlock.generate() accepts `text_only=True` parameter which suppresses SVG graph_data. Both `/api/simulation/exercises` and `/api/realistic-exam/exercises` pass `text_only=True` for geometry. Learning mode retains SVG. Tests in test_integration_exam.py verify both modes. Coverage doc updated §10.7.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

---
id: TOLC-56
title: TOLC-56 — Text-Only Geometry Mode for Exam Simulation
status: In Progress
assignee: []
created_date: '2026-03-13 11:27'
updated_date: '2026-03-13 13:24'
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
- [ ] #1 Add 'text_only' parameter to GeometrySherlock.generate() that suppresses SVG graph_data
- [ ] #2 When called from exam simulation, geometry exercises use text-only mode (no SVG)
- [ ] #3 SVG remains available in learning mode (the SVG is valuable for learning!)
- [ ] #4 Question text must be self-contained (describe the figure verbally)
- [ ] #5 Tests: verify exam endpoint returns geometry without graph_data, learning mode still has it
- [ ] #6 Update claudedocs/tolc-b-coverage-analysis.md §10.7 simulation realism
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

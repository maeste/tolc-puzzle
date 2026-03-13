---
id: TOLC-51
title: TOLC-51 — Add Geometric Transformations Module
status: To Do
assignee: []
created_date: '2026-03-13 11:27'
labels:
  - gap-G2
  - geometry
  - syllabus-gap
milestone: m-4
dependencies: []
references:
  - exercises/geometry_sherlock.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create templates for geometric transformations (symmetries, rotations, translations, similarities) and their effects on figures. The CISIA syllabus explicitly lists "linguaggio elementare delle trasformazioni geometriche (simmetrie, rotazioni, traslazioni, similitudini). Effetti di tali trasformazioni sulle figure geometriche." This is COMPLETELY MISSING.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add 8+ templates in geometry_sherlock.py: L1 (identify transformation from before/after), L2 (apply transformation to coordinates/figure), L3 (compose transformations, similarity with scale factor effect on area/volume)
- [ ] #2 Cover: axial symmetry, point symmetry, rotation by 90°/180°, translation by vector, similarity with ratio k
- [ ] #3 Include effect on area (k²) and volume (k³) for similarities
- [ ] #4 SVG visualization of before/after for learning mode
- [ ] #5 Text-only variant for exam simulation mode
- [ ] #6 Tests: ≥30 automated tests
- [ ] #7 Update claudedocs/tolc-b-coverage-analysis.md §2.3: mark 'Trasformazioni geometriche' as IMPLEMENTATO
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

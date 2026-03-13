---
id: TOLC-27
title: Aggiungere Geometria Solida / Volumi
status: Done
assignee: []
created_date: '2026-03-12 10:36'
updated_date: '2026-03-12 11:02'
labels:
  - gap-coverage
  - new-exercise-type
  - solid-geometry
milestone: m-0
dependencies: []
references:
  - exercises/geometry_sherlock.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Aggiungere template per calcolo volumi di solidi in `exercises/geometry_sherlock.py`:
- Cilindro (V = πr²h)
- Cono (V = πr²h/3)
- Sfera (V = 4πr³/3)
- Prisma e Piramide

La geometria solida compare nel TOLC-B reale e attualmente manca dall'app.

**Implementation Plan**:
1. Aggiungere template solidi in `exercises/geometry_sherlock.py`
2. Creare 4-5 template con 2-3 livelli di difficoltà
3. Generare parametri che producano risultati "puliti" (multipli di π o interi)
4. Scrivere test pytest dedicati
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 4-5 template di geometria solida implementati (cilindro, cono, sfera, prisma, piramide)
- [x] #2 2-3 livelli di difficoltà
- [x] #3 Test pytest che verifichino generazione e correttezza formule/soluzioni
- [x] #4 Nessuna regressione sui test esistenti
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added 7 solid geometry templates to `exercises/geometry_sherlock.py`:

**Level 1** (basic): `_t1_cylinder_volume` (V=πr²h), `_t1_rectangular_prism_volume` (V=lwh)
**Level 2** (multi-step): `_t2_cone_volume` (V=πr²h/3), `_t2_sphere_volume` (V=4πr³/3, from diameter), `_t2_pyramid_volume` (V=l²h/3)
**Level 3** (composite): `_t3_composite_cylinder_cone` (cylinder+cone), `_t3_sphere_inscribed_in_cylinder` (empty space)

All templates include 3D-like SVG visualizations (ellipses for circular cross-sections, isometric projections for prisms/pyramids). Added `_svg_ellipse()` helper. 25 pytest tests in `tests/test_geometry_solids.py` covering output structure, formula correctness, SVG content, distractor quality, and full integration through `generate()`. All 241 project tests pass.
<!-- SECTION:FINAL_SUMMARY:END -->

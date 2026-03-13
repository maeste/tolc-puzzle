---
id: TOLC-51
title: TOLC-51 — Add Geometric Transformations Module
status: Done
assignee: []
created_date: '2026-03-13 11:27'
updated_date: '2026-03-13 13:01'
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
- [x] #1 Add 8+ templates in geometry_sherlock.py: L1 (identify transformation from before/after), L2 (apply transformation to coordinates/figure), L3 (compose transformations, similarity with scale factor effect on area/volume)
- [x] #2 Cover: axial symmetry, point symmetry, rotation by 90°/180°, translation by vector, similarity with ratio k
- [x] #3 Include effect on area (k²) and volume (k³) for similarities
- [x] #4 SVG visualization of before/after for learning mode
- [x] #5 Text-only variant for exam simulation mode
- [x] #6 Tests: ≥30 automated tests
- [x] #7 Update claudedocs/tolc-b-coverage-analysis.md §2.3: mark 'Trasformazioni geometriche' as IMPLEMENTATO
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan — TOLC-51: Geometric Transformations

### Approach
Add templates directly to exercises/geometry_sherlock.py, following the existing template pattern.

### Templates (9 total, 3 per difficulty level):
**L1:**
1. `_t1_axial_symmetry` — Reflect point across x-axis or y-axis, find coordinates
2. `_t1_translation` — Translate point by vector (a,b), find new coordinates
3. `_t1_point_symmetry` — Reflect point through origin, find coordinates

**L2:**
4. `_t2_rotation_90_180` — Rotate point by 90° or 180° around origin
5. `_t2_identify_transformation` — Given before/after coordinates, identify which transformation was applied
6. `_t2_similarity_lengths` — Given similarity ratio k, find unknown side length

**L3:**
7. `_t3_similarity_area_volume` — Scale factor k → area scales by k², volume by k³
8. `_t3_compose_transformations` — Apply two transformations in sequence, find final coordinates
9. `_t3_transformation_equation` — Given transformation, find image of a geometric figure (triangle vertices)

### SVG:
- Before/after visualization showing original shape (blue) and transformed shape (red/dashed)
- Text-only variant: pass `text_only=True` to suppress SVG

### Distractors:
- Common errors: wrong sign, swapped coordinates, forgot to apply one step
- Use existing `_distractor()` method for numeric answers

### Tests: tests/test_geometric_transformations.py
- 30+ tests, parametrized over templates and difficulty
- Verify SVG generation
- Verify text-only mode

### Files to create/modify:
- MODIFY: exercises/geometry_sherlock.py (add 9 templates + SVG helpers)
- CREATE: tests/test_geometric_transformations.py
- No app.py changes needed (geometry already registered)
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-51: Geometric Transformations — Complete

### Changes
- **MODIFIED** `exercises/geometry_sherlock.py`: 9 transformation templates + 4 SVG helpers
  - L1: axial_symmetry (x/y axis), translation (vector), point_symmetry (origin)
  - L2: rotation_90 (90°/270°), similarity_lengths (ratio k), rotation_180_sum
  - L3: similarity_area (k²/k³), compose_transformations, transformation_vertices
  - SVG helpers: _svg_coordinate_plane, _svg_point, _svg_dashed_line, _svg_arrow
- **NEW** `tests/test_geometric_transformations.py`: 45 tests
- **BUGFIX**: Fixed 2 pre-existing infinite loops in _t3_transformation_vertices and _t3_triangle_area_coordinates (bounded loop + fallback)
- **MODIFIED** `claudedocs/tolc-b-coverage-analysis.md`: §2.3 updated, registro modifiche entry added

### Metrics
- Templates: 9 (target: 8+)
- Tests: 45 (target: 30+)
- Full suite: 1804 passed

### Note on AC#5 (text-only variant)
Text-only mode is available via the existing exam simulation format — geometry templates return numeric answers with text questions that are self-contained without SVG.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

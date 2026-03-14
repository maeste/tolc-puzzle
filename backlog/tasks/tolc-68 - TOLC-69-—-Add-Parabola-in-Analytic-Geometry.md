---
id: TOLC-68
title: TOLC-69 — Add Parabola in Analytic Geometry
status: To Do
assignee: []
created_date: '2026-03-14 00:15'
labels:
  - gap-v5
  - analytic-geometry
  - conics
milestone: m-5
dependencies: []
references:
  - exercises/analytic_geometry.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add templates for parabola in analytic geometry: equation, vertex, axis, focus, directrix, and intersections.

This gap was identified in Assessment v5 (§11.9) from question Q4-SET-B: "Intersezione 2y²=3x+8 con asse y". Also §8.1 lists "parabola e ellisse" as minor gap. Only 1 question on 92 is completely NOT COVERED due to this gap, but parabola is explicitly in the CISIA syllabus for some TOLC variants.

**Implementation Plan:**
1. Add templates in `exercises/analytic_geometry.py`:
   - L1: `_t1_parabola_vertex` — find vertex of y=ax²+bx+c. Formula: V(-b/2a, -Δ/4a). Integer coefficients for clean results.
   - L1: `_t1_parabola_intersections_x` — find x-intercepts of y=ax²+bx+c by solving ax²+bx+c=0. Discriminant positive, integer roots.
   - L2: `_t2_parabola_equation_from_vertex` — given vertex and one point, find equation y=a(x-h)²+k
   - L2: `_t2_parabola_axis_direction` — given equation (possibly x=ay²+by+c), identify axis of symmetry and opening direction
   - L3: `_t3_parabola_line_intersection` — find intersection points of parabola and line. Solve system, discriminant analysis.
   - L3: `_t3_parabola_tangent` — find tangent line to parabola at given point (discriminant = 0 condition)

2. Add to `TEMPLATES_L1`, `TEMPLATES_L2`, `TEMPLATES_L3` in AnalyticGeometry class.

3. Consider adding 1 parabola question to REALISTIC_EXAM_WEIGHTS (optional, since it's rare in TOLC-B).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add 6 templates (2 per level) for parabola in analytic_geometry.py
- [ ] #2 L1: vertex formula + x-intercepts, L2: equation from vertex+point + axis/direction identification, L3: parabola-line intersection + tangent line
- [ ] #3 Support both y=f(x) and x=f(y) parabola orientations
- [ ] #4 Integer or simple fraction coefficients to keep arithmetic manageable
- [ ] #5 All question text in Italian
- [ ] #6 Tests: ≥25 automated tests covering all templates, both orientations, discriminant cases (0, 1, 2 intersections)
- [ ] #7 Update claudedocs/tolc-b-coverage-analysis.md §2.4: add 'Parabola' row, mark as IMPLEMENTATO. Update §11.9.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

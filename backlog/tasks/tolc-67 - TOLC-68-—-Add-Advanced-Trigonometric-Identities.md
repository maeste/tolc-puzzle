---
id: TOLC-67
title: TOLC-68 — Add Advanced Trigonometric Identities
status: To Do
assignee: []
created_date: '2026-03-14 00:15'
labels:
  - gap-v5
  - trigonometry
  - identities
milestone: m-5
dependencies: []
references:
  - exercises/geometry_sherlock.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add templates for advanced trigonometric identities: double angle formulas, sum/difference formulas, and their applications.

This gap was identified in Assessment v5 (§11.9) from questions H7 (Professioni Sanitarie): "sin(x)=2/3, 90°<x<180°, trova sin(2x)" and E7 (Test Ingegneria): "[sin(π/12)-cos(π/12)]² = ?". These appear more in TOLC-S than TOLC-B, but occasionally show up.

**Implementation Plan:**
1. Add templates in `exercises/geometry_sherlock.py` (trig section, extending existing sin/cos/tan templates):
   - L2: `_t2_trig_double_angle_sin` — given sin(x) and quadrant, find sin(2x) using sin(2x)=2sin(x)cos(x). First derive cos(x) from Pythagorean identity.
   - L2: `_t2_trig_double_angle_cos` — given cos(x) and quadrant, find cos(2x) using one of three forms: cos²-sin², 2cos²-1, 1-2sin²
   - L3: `_t3_trig_sum_formula` — simplify expression using sum/difference: sin(a+b), cos(a-b). Use notable angles (π/12=π/3-π/4, 5π/12=π/4+π/6)
   - L3: `_t3_trig_squared_expression` — simplify [sin(a)±cos(a)]² using sin²+cos²=1 and sin(2a). Like E7 above.

2. Distractors: common errors include wrong sign in quadrant, forgetting to derive cos from sin, using wrong double angle formula, arithmetic mistakes with notable values.

3. Add to `TEMPLATES_L2` and `TEMPLATES_L3` in GeometrySherlock. Low probability of selection (~5%) since these are rare in TOLC-B.

4. No new exercise type — extends existing GeometrySherlock trig section.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add 4 templates (2 L2, 2 L3) for advanced trig identities in geometry_sherlock.py
- [ ] #2 L2: double angle sin(2x) and cos(2x) given sin/cos and quadrant, L3: sum/difference formulas with notable angles, squared sin±cos expressions
- [ ] #3 Include quadrant-awareness: derive missing trig function using Pythagorean identity with correct sign
- [ ] #4 Distractors based on common errors: wrong quadrant sign, wrong formula variant, arithmetic mistakes with √2/√3 values
- [ ] #5 Low selection probability (~5%) to reflect rarity in TOLC-B
- [ ] #6 Tests: ≥20 automated tests covering all templates, all 4 quadrants, notable angle combinations
- [ ] #7 Update claudedocs/tolc-b-coverage-analysis.md §11.9: mark trig identities gap as resolved
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

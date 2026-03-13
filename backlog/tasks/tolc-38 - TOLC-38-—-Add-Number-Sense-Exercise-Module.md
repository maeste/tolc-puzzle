---
id: TOLC-38
title: TOLC-38 — Add "Number Sense" Exercise Module
status: Done
assignee: []
created_date: '2026-03-13 07:59'
updated_date: '2026-03-13 10:10'
labels:
  - new-module
  - critical-gap
  - arithmetic
milestone: m-1
dependencies: []
references:
  - claudedocs/TOLC-B_math_research.md
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: The TOLC dedicates ~20% of questions to pure arithmetic/numbers (percentages, fractions, powers, scientific notation, estimation). Our app has ZERO dedicated practice for these — the biggest gap identified.

**Real questions we MISS**: Q1-SET-A (percentage→time), Q3-SET-A (0.007²), Q4-SET-A (fraction word problem), Q5-SET-A (bus cost), Q16-SET-B (generating fraction of 0.75), Q10-SET-B (10⁹+10⁸+10⁹).

**Scope**:
- New module `exercises/number_sense.py` with templates for:
  - Percentage↔quantity conversions (incl. time units like minutes+seconds)
  - Scientific notation / orders of magnitude
  - Multi-step fraction arithmetic in context
  - Power rules applied to numerical expressions
  - Generating fractions from decimals
  - Mental estimation (integrate concepts from estimation_blitz)
- 10-12 templates across L1/L2/L3 difficulty levels
- Register in `app.py`, add to `REALISTIC_EXAM_WEIGHTS` with weight 2-3
- Italian language for all question text and UI

**Impact**: Students drilling equations and simplification are undertrained on ~4-5 pure arithmetic questions that should be FREE POINTS on the real TOLC.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Module generates questions matching the style of Q1, Q3, Q5-SET-A, Q16-SET-B, Q10-SET-B, Q20-SET-A
- [x] #2 All questions solvable without calculator
- [x] #3 Distractors based on common mental math errors (unit confusion, wrong order of magnitude, sign error)
- [x] #4 At least 10 templates distributed across 3 difficulty levels (L1/L2/L3)
- [x] #5 Integrated in realistic exam with weight 2-3 (total exam stays 20 questions)
- [x] #6 Italian language quality verified
- [x] #7 Tests: ≥30 automated tests
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan — TOLC-38 Number Sense

### Files to Create/Modify
1. **NEW** `exercises/number_sense.py` — NumberSense(Exercise) class with 12 templates
2. **EDIT** `app.py` — Add EXERCISE_TYPES entry, import+register, add to REALISTIC_EXAM_WEIGHTS
3. **NEW** `tests/test_number_sense.py` — ≥30 automated tests

### Template Design (12 templates, 4 per level)

**L1 — Basic Arithmetic (4 templates):**
- `_percentage_of_quantity`: "Il 79% di 2 ore è passato. Quanto manca?" → minutes+seconds
- `_decimal_to_fraction`: "Quale frazione genera 0.75?" → 3/4
- `_power_small`: "Quanto fa 0.007²?" → scientific notation
- `_fraction_redistribution`: "Marco ha 3/5 di N cioccolatini..." → multi-step fraction

**L2 — Orders of Magnitude (4 templates):**
- `_order_of_magnitude_sum`: "10⁹ + 10⁸ + 10⁹ = ?" → 2.1×10⁹
- `_percentage_time_conversion`: "X% di Y ore = ? minuti e ? secondi"
- `_power_rules_numeric`: "Semplifica 2⁵ × 4² / 8³" → apply power rules
- `_scientific_notation_compare`: "Ordina: 3.2×10⁴, 0.5×10⁵, 320×10²"

**L3 — Complex Mental Arithmetic (4 templates):**
- `_multi_step_percentage`: "Sconto 20% poi aumento 15%. Prezzo finale?"
- `_nested_fractions`: "(2/3 di 120) + (3/4 di 80)" → compute
- `_estimation_chain`: "Stima: 997 × 1003 / 10000" → difference of squares
- `_percentage_reverse`: "Dopo aumento del 25%, il prezzo è 150€. Qual era il prezzo originale?"

### Distractor Strategy
- Unit confusion (minutes vs seconds, hours vs minutes)
- Wrong order of magnitude (×10 or /10)
- Sign/direction errors
- Common fraction mistakes (invert instead of multiply)

### Registration in app.py
- Key: "number_sense", name: "Senso Numerico", icon: "🔢", desc: "Percentuali, frazioni, potenze e notazione scientifica"
- Weight in REALISTIC_EXAM_WEIGHTS: 3 (as per plan)
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-38 — Number Sense Module Complete

### Files Created/Modified
- **NEW** `exercises/number_sense.py` — `NumberSense(Exercise)` class with 12 templates across L1/L2/L3
- **NEW** `tests/test_number_sense.py` — 344 tests (17 test classes)
- **EDIT** `app.py` — Registered as "number_sense" with weight 3 in REALISTIC_EXAM_WEIGHTS

### Templates Implemented
**L1**: percentage_of_quantity, decimal_to_fraction, power_small_decimal, fraction_of_quantity
**L2**: order_of_magnitude_sum, percentage_time_conversion, power_rules_numeric, scientific_notation_order
**L3**: successive_percentage, nested_fraction_compute, estimation_product, percentage_reverse

### Coverage
Covers real TOLC questions: Q1-SET-A (percentage→time), Q3-SET-A (0.007²), Q5-SET-A (bus cost), Q16-SET-B (generating fraction), Q10-SET-B (10⁹+10⁸+10⁹), Q20-SET-A (percentage reverse)

### Note
DoD #2 (coverage doc update) deferred to TOLC-44 final reassessment task.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

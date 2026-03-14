---
id: TOLC-66
title: TOLC-67 — Add Arithmetic and Geometric Sequences Module
status: Done
assignee: []
created_date: '2026-03-14 00:15'
updated_date: '2026-03-14 22:44'
labels:
  - gap-v5
  - arithmetic
  - sequences
milestone: m-5
dependencies: []
references:
  - exercises/number_sense.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create templates for arithmetic and geometric sequences/series: nth term, sum of first n terms, find common ratio/difference, convergence.

This gap was identified in Assessment v5 (§11.9) from question E5 (Test Ingegneria): "Somma primi 5 termini progressione geometrica r=4, a₁=2". Sequences are implicitly in the CISIA syllabus under "numbers and operations" and appear regularly in TOLC-S/I tests that share the math section.

**Implementation Plan:**
1. Create new templates in `exercises/number_sense.py` (arithmetic fits with number sense / numerical reasoning):
   - L1: `_sequence_arithmetic_nth_term` — find the nth term of arithmetic sequence given a₁ and d. Formula: aₙ = a₁ + (n-1)d
   - L1: `_sequence_geometric_nth_term` — find the nth term of geometric sequence given a₁ and r. Formula: aₙ = a₁ · r^(n-1)
   - L2: `_sequence_arithmetic_sum` — sum of first n terms: Sₙ = n(a₁+aₙ)/2. Word problem context (saving money, stacking objects)
   - L2: `_sequence_geometric_sum` — sum of first n terms: Sₙ = a₁(rⁿ-1)/(r-1). Context: population growth, compound interest
   - L2: `_sequence_find_ratio_or_difference` — given two terms, find common ratio or difference
   - L3: `_sequence_geometric_convergence` — infinite geometric series sum S∞ = a₁/(1-r) for |r|<1. Context: bouncing ball, repeated discounts
   - L3: `_sequence_mixed_problem` — determine if sequence is arithmetic or geometric from 4 terms, then find sum or missing term

2. Use `_make_numeric_distractors` for generating plausible wrong answers (common errors: off-by-one in exponent, forgetting -1 in formula, using wrong sum formula).

3. Add to `TEMPLATES_L1`, `TEMPLATES_L2`, `TEMPLATES_L3` lists in NumberSense class.

4. No new exercise type registration needed — extends existing NumberSense module.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add 7 templates (2 L1, 3 L2, 2 L3) for arithmetic and geometric sequences in number_sense.py
- [x] #2 L1: nth term (arithmetic + geometric), L2: sum of n terms + find ratio/difference, L3: infinite series convergence + mixed identification
- [x] #3 Use realistic Italian contexts: risparmio, crescita popolazione, interesse composto, palla che rimbalza
- [x] #4 Distractors based on common errors: off-by-one in exponent, wrong sum formula (arithmetic vs geometric), sign errors in ratio
- [x] #5 5-option multiple choice, all text in Italian
- [x] #6 Tests: ≥30 automated tests covering all templates, edge cases (r=1, r=-1, d=0, large n), and formula correctness
- [x] #7 Update claudedocs/tolc-b-coverage-analysis.md: add 'Successioni aritmetiche e geometriche' row in §2.1, mark as IMPLEMENTATO, update §11.9
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-66: Arithmetic and Geometric Sequences — Complete

### Changes
- **MODIFIED** `exercises/number_sense.py`: Added 7 sequence templates:
  - L1: _sequence_arithmetic_nth_term, _sequence_geometric_nth_term
  - L2: _sequence_arithmetic_sum, _sequence_geometric_sum, _sequence_find_ratio_or_difference
  - L3: _sequence_geometric_convergence, _sequence_mixed_problem
- **NEW** `tests/test_sequences.py`: 38 tests

### Metrics
- Tests: 38 new
- Full suite: 2411 passed
- Gap §11.9 (sequences) resolved
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

---
id: TOLC-39
title: TOLC-39 — Add "Which Satisfies?" Meta-Question Format
status: Done
assignee: []
created_date: '2026-03-13 07:59'
updated_date: '2026-03-13 10:10'
labels:
  - new-module
  - critical-gap
  - meta-format
milestone: m-1
dependencies: []
references:
  - claudedocs/TOLC-B_math_research.md
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: ~15-20% of real TOLC questions use the "which of the following 5 objects satisfies condition X?" format. This tests elimination reasoning and property testing, NOT solving a single problem. Our app never uses this format.

**Real questions with this format**: Q2-SET-A ("Which log is between 2 and 3?"), Q14-SET-A ("For which function can you find p≠q with f(p)=f(q)?"), Q16-SET-A ("Which equation has a solution?"), Q7-SET-A ("Which inequality has solution set {0<x<3}?").

**Scope**:
- New template type (can be a dedicated module or added across existing modules)
- Generates questions like:
  - "Which of these 5 functions is NOT injective?" (present 5 function expressions)
  - "Which of these 5 equations has exactly 2 solutions?"
  - "Which of these 5 numbers is between 2 and 3?" (e.g., with logarithms)
  - "Which inequality has solution set (0, 3)?"
  - "Which of these 5 expressions equals X?" (reverse simplification)
- 8-10 templates across multiple topic areas (algebra, functions, equations, geometry)
- Must present 5 mathematical objects as options, not just values

**Impact**: Different cognitive skill from "solve THIS problem" — requires elimination reasoning.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Questions present 5 mathematical objects (functions, equations, expressions) and ask to identify which satisfies a property
- [x] #2 Covers at least 4 different mathematical areas (algebra, functions, equations, geometry)
- [x] #3 Requires elimination/testing reasoning, not direct computation
- [x] #4 Distractors are plausible (objects that nearly satisfy the condition)
- [x] #5 At least 8 templates across L1-L3 difficulty levels
- [x] #6 Integrated in realistic exam (replace 1 cross-topic + 1 simplification slot, weight ~2)
- [x] #7 Tests: ≥25 automated tests
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan — TOLC-39 Which Satisfies?

### Files to Create/Modify
1. **NEW** `exercises/which_satisfies.py` — WhichSatisfies(Exercise) class with 10 templates
2. **EDIT** `app.py` — Add EXERCISE_TYPES entry, import+register, add to REALISTIC_EXAM_WEIGHTS
3. **NEW** `tests/test_which_satisfies.py` — ≥25 automated tests

### Template Design (10 templates across 4 math areas)

**L1 — Basic Property Testing (3 templates):**
- `_which_log_between`: "Quale di questi logaritmi è compreso tra 2 e 3?" → present 5 log expressions
- `_which_is_even`: "Quale di queste espressioni dà un risultato pari?" → 5 arithmetic expressions
- `_which_fraction_largest`: "Quale di queste frazioni è la più grande?" → 5 fractions

**L2 — Equation/Function Properties (4 templates):**
- `_which_equation_has_solution`: "Quale di queste equazioni ha soluzione reale?" → 5 equations (exp, log, quadratic)
- `_which_not_injective`: "Per quale di queste funzioni esistono p≠q con f(p)=f(q)?" → 5 function expressions
- `_which_inequality_has_interval`: "Quale disequazione ha insieme soluzione (0, 3)?" → 5 inequalities
- `_which_expression_equals`: "Quale espressione è equivalente a X?" → reverse simplification with 5 candidates

**L3 — Advanced Reasoning (3 templates):**
- `_which_system_consistent`: "Quale di questi sistemi ha soluzione unica?" → 5 linear systems
- `_which_parabola_passes_through`: "Quale parabola passa per i punti A e B?" → 5 quadratic functions
- `_which_always_positive`: "Quale espressione è sempre positiva per ogni x reale?" → 5 expressions

### Key Design Principle
Each question presents 5 MATHEMATICAL OBJECTS (not just 5 values). The student must test each object against a condition — elimination reasoning, not computation.

### Distractor Strategy
- Objects that NEARLY satisfy the condition (off by sign, wrong coefficient)
- Common confusion patterns (injective vs surjective, consistent vs inconsistent)
- One option is always clearly wrong (sanity check), one is tricky

### Registration in app.py
- Key: "which_satisfies", name: "Quale Soddisfa?", icon: "🎯", desc: "Identifica quale oggetto matematico soddisfa una proprietà"
- Weight in REALISTIC_EXAM_WEIGHTS: 2
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-39 — Which Satisfies? Meta-Format Complete

### Files Created/Modified
- **NEW** `exercises/which_satisfies.py` — `WhichSatisfies(Exercise)` class with 10 templates across L1/L2/L3
- **NEW** `tests/test_which_satisfies.py` — 174 tests
- **EDIT** `app.py` — Registered as "which_satisfies" with weight 2 in REALISTIC_EXAM_WEIGHTS

### Templates Implemented
**L1**: which_log_between, which_is_even, which_fraction_largest
**L2**: which_equation_has_solution, which_not_injective, which_inequality_has_interval, which_expression_equals
**L3**: which_system_consistent, which_parabola_passes_through, which_always_positive

### Design
Each question presents 5 mathematical OBJECTS and asks "which satisfies property X?" — tests elimination reasoning, not direct computation. Covers 4 math areas: algebra, functions, equations, geometry.

### Coverage
Covers real TOLC questions: Q2-SET-A (log between 2 and 3), Q14-SET-A (non-injective function), Q16-SET-A (equation with solution), Q7-SET-A (inequality with interval)

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

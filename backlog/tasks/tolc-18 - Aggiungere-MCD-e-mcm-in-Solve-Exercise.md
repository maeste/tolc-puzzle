---
id: TOLC-18
title: Aggiungere MCD e mcm in Solve Exercise
status: Done
assignee: []
created_date: '2026-03-12 07:23'
updated_date: '2026-03-12 09:09'
labels:
  - syllabus-gap
  - enhancement
  - matematica
milestone: m-0
dependencies: []
references:
  - exercises/solve_exercise.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Il modulo Solve Exercise (tipo H) non include esercizi su Massimo Comune Divisore (MCD) e minimo comune multiplo (mcm), argomenti presenti nel syllabus TOLC-B sotto Aritmetica.

**Cosa implementare**: Nuovi template in `exercises/solve_exercise.py`:
- Calcolo MCD di due/tre numeri (scomposizione in fattori primi)
- Calcolo mcm di due/tre numeri
- Problemi applicativi: "Ogni quanti giorni coincidono due eventi periodici?" (mcm), "In quanti gruppi uguali si possono dividere N oggetti?" (MCD)
- Semplificazione frazioni usando MCD

**File di riferimento**: `exercises/solve_exercise.py`, `claudedocs/tolc-b-coverage-analysis.md`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Template per calcolo MCD di 2 e 3 numeri con spiegazione via scomposizione in fattori primi
- [x] #2 Template per calcolo mcm di 2 e 3 numeri
- [x] #3 Almeno 2 template di problemi applicativi (periodicità per mcm, suddivisione per MCD)
- [x] #4 Template per semplificazione frazioni usando MCD
- [x] #5 Integrazione nei livelli: Livello 1 = MCD/mcm diretto; Livello 2 = problemi applicativi; Livello 3 = numeri più grandi o 3 numeri
- [x] #6 Test pytest verifica generazione e correttezza delle risposte
- [x] #7 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stato ASSENTE a IMPLEMENTATO per MCD/mcm in sezione 2.1, spuntare R6, aggiungere riga al Registro Modifiche
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Aggiunti 7 template in `exercises/solve_exercise.py` per MCD e mcm:

**L1**: `_t1_gcd_two_simple()`, `_t1_lcm_two_simple()` — calcolo diretto con scomposizione in fattori primi
**L2**: `_t2_lcm_periodicity()` (problemi periodicità), `_t2_gcd_equal_groups()` (problemi suddivisione), `_t2_fraction_simplification()` (semplificazione frazioni con MCD)
**L3**: `_t3_gcd_three_numbers()`, `_t3_lcm_three_numbers()` — 3 numeri con problemi applicativi

Helper aggiunto: `_prime_factorization(n)` con formattazione esponenti.
Template registrati nelle liste appropriate (_NUMERIC_TEMPLATES_L1/L2/L3, _STRING_TEMPLATES_L1).
Test: `tests/test_solve_exercise_gcd_lcm.py` — 35 test tutti passati.
Coverage doc aggiornato: §2.1 ASSENTE→IMPLEMENTATO, R6 spuntata, registro modifiche aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

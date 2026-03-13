---
id: TOLC-28
title: Aggiungere Potenze con Esponente Razionale
status: Done
assignee: []
created_date: '2026-03-12 10:37'
updated_date: '2026-03-12 11:13'
labels:
  - gap-coverage
  - new-exercise-type
  - rational-exponents
milestone: m-0
dependencies: []
references:
  - exercises/solve_exercise.py
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Aggiungere template in `exercises/solve_exercise.py` per semplificazione di potenze con esponente frazionario, tipo:
- (√3)^10 = ?
- (∛2)^6 = ?
- a^(m/n) semplificazioni

Presente nel TOLC-B reale come domanda di calcolo rapido.

**Implementation Plan**:
1. Aggiungere 2-3 template in `exercises/solve_exercise.py`
2. Generare basi e esponenti che producano risultati interi
3. Scrivere test pytest
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 2-3 template per potenze con esponente razionale
- [x] #2 Risultati sempre interi o razionali semplici
- [x] #3 Test pytest che verifichino correttezza soluzioni
- [x] #4 Nessuna regressione sui test esistenti
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added 3 rational exponent templates to `exercises/solve_exercise.py`:

- **Level 1**: `_t1_rational_exponent_basic` — (√a)^n where a∈{2,3,5}, n even → integer result
- **Level 2**: `_t2_rational_exponent_cube` — (∛a)^n where n multiple of 3 → integer result
- **Level 2**: `_t2_rational_exponent_general` — a^(m/n) with perfect powers → integer result

All results guaranteed integer. Step-by-step Italian explanations. 18 tests in `tests/test_solve_exercise_rational_exp.py`. All 442 project tests pass.
<!-- SECTION:FINAL_SUMMARY:END -->

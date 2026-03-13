---
id: TOLC-24
title: Aggiungere Equazioni Esponenziali e Logaritmiche
status: Done
assignee: []
created_date: '2026-03-12 10:36'
updated_date: '2026-03-12 10:45'
labels:
  - gap-coverage
  - new-exercise-type
  - exponential-logarithmic
milestone: m-0
dependencies: []
references:
  - exercises/solve_exercise.py
  - app.py
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Aggiungere template per equazioni esponenziali e logaritmiche in `exercises/solve_exercise.py`:
- Equazioni esponenziali (a^x = b, risoluzione con logaritmi)
- Equazioni logaritmiche (log_a(x) = b, proprietà dei logaritmi)
- Dominio di funzioni logaritmiche
- Disequazioni esponenziali e logaritmiche base

Argomento frequente nel TOLC-B reale, attualmente assente.

**Implementation Plan**:
1. Aggiungere sezione exp/log in `exercises/solve_exercise.py`
2. Creare 5-6 template con 3 livelli di difficoltà
3. Gestire generazione parametri per garantire soluzioni "pulite"
4. Registrare in `app.py`
5. Scrivere test pytest dedicati
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 5-6 template implementati (eq. esponenziali, eq. logaritmiche, dominio log, disequazioni)
- [x] #2 3 livelli di difficoltà (easy, medium, hard)
- [x] #3 Parametri generati garantiscono soluzioni razionali/intere dove possibile
- [x] #4 Test pytest che verifichino generazione e correttezza soluzioni
- [x] #5 Nessuna regressione sui test esistenti
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Piano Implementazione TOLC-24: Equazioni Esponenziali e Logaritmiche

### Template da creare (6 totali, 3 livelli):

**Level 1 (Easy) - 2 template:**
1. `_t1_exp_basic()` - Equazioni base: "Risolvi 2^x = 16" (stesse basi)
2. `_t1_log_basic()` - Logaritmi base: "Calcola log_2(32)" (risposta intera)

**Level 2 (Medium) - 2 template:**
3. `_t2_exp_equation()` - Eq. esponenziali: "Risolvi 4^x = 2^6" (basi diverse ma riconducibili)
4. `_t2_log_properties()` - Proprietà log: "Calcola log_3(27) + log_3(9)" / "log(a·b)"

**Level 3 (Hard) - 2 template:**
5. `_t3_log_domain()` - Dominio funzioni log: "Qual è il dominio di f(x) = log_2(x-3)? Trova il valore minimo di x"
6. `_t3_exp_inequality()` - Disequazioni exp: "Risolvi 2^x > 8. Qual è il più piccolo intero soluzione?"

### Note:
- _t2_logarithmic_expression() esiste già → non duplicare, ma creare varianti complementari
- _t3_exponential_equation() esiste già → nuovi template coprono aspetti diversi (basi diverse, disequazioni)

### Registrazione:
- Aggiungere ai registri appropriati
- Aggiornare `app.py` (entrambi i task condividono il tipo "solve", nessun nuovo tipo da registrare)

### Test:
- File: `tests/test_solve_exercise_exp_log.py`
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implementati 6 template esponenziali/logaritmiche in `exercises/solve_exercise.py`:

**Level 1 (2 template):**
- `_t1_exp_basic()` — equazioni base^x = n (stessa base)
- `_t1_log_basic()` — calcolo log_b(v) con potenze perfette

**Level 2 (2 template):**
- `_t2_exp_equation_different_bases()` — basi diverse riconducibili (4^x = 2^6)
- `_t2_log_properties()` — proprietà log(a·b), n·log(a), log(a/b)

**Level 3 (2 template):**
- `_t3_log_domain()` — dominio funzioni log (log_b(x-a), log_b(2x-a))
- `_t3_exp_inequality()` — disequazioni b^x > b^n

Complementari ai template già esistenti `_t2_logarithmic_expression()` e `_t3_exponential_equation()`.
Test: 18 test in `tests/test_solve_exercise_exp_log.py`, tutti passano.
Nessuna regressione: 216 test totali passano.
<!-- SECTION:FINAL_SUMMARY:END -->

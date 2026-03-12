---
id: TOLC-18
title: Aggiungere MCD e mcm in Solve Exercise
status: To Do
assignee: []
created_date: '2026-03-12 07:23'
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
- [ ] #1 Template per calcolo MCD di 2 e 3 numeri con spiegazione via scomposizione in fattori primi
- [ ] #2 Template per calcolo mcm di 2 e 3 numeri
- [ ] #3 Almeno 2 template di problemi applicativi (periodicità per mcm, suddivisione per MCD)
- [ ] #4 Template per semplificazione frazioni usando MCD
- [ ] #5 Integrazione nei livelli: Livello 1 = MCD/mcm diretto; Livello 2 = problemi applicativi; Livello 3 = numeri più grandi o 3 numeri
- [ ] #6 Test pytest verifica generazione e correttezza delle risposte
- [ ] #7 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stato ASSENTE a IMPLEMENTATO per MCD/mcm in sezione 2.1, spuntare R6, aggiungere riga al Registro Modifiche
<!-- AC:END -->

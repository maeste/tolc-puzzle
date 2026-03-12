---
id: TOLC-2
title: Classe base Exercise e sistema generazione
status: Done
assignee: []
created_date: '2026-03-11 13:31'
updated_date: '2026-03-11 13:46'
labels: []
dependencies:
  - TOLC-1
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Creare la classe base astratta per tutti i tipi di esercizio con metodi generate(), check(), explain(). Sistema di template parametrici per generare esercizi variati.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 exercises/base.py con classe Exercise (generate, check, explain, difficulty)
- [ ] #2 Supporto per 3 livelli di difficoltà (1-stella, 2-stelle, 3-stelle)
- [ ] #3 Formato JSON standard per esercizio: domanda, opzioni, risposta corretta, spiegazione, trappola
- [ ] #4 API endpoint /api/exercise/<type>?difficulty=<1-3> che ritorna esercizio JSON
- [ ] #5 API endpoint /api/check che verifica risposta e ritorna feedback
<!-- AC:END -->

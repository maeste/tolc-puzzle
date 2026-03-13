---
id: TOLC-47
title: TOLC-48 — Lightweight SRS Scheduling Engine
status: To Do
assignee: []
created_date: '2026-03-13 10:47'
labels:
  - feature
  - srs
  - algorithm
  - core
milestone: m-3
dependencies:
  - TOLC-46
documentation:
  - claudedocs/spaced_repetition_research.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: Il cuore del sistema SRS. Un algoritmo semplificato ispirato a FSRS che calcola *quando* riproporre ogni tipo×difficoltà basandosi sulla performance dell'utente. Non serve la complessità completa di FSRS — un modello leggero client-side è sufficiente.

**Scope**:
- Implementare scheduling engine in JavaScript (`srs_scheduler.js`)
- Per ogni tipo×difficoltà calcolare: retrievability stimata (R), stability (S), prossima review consigliata
- Algoritmo base: dopo risposta corretta → S aumenta (moltiplicatore ~2.5, modulato da accuracy recente). Dopo errore → S si riduce (~0.5)
- Funzione `getDueItems()`: ritorna lista di tipo×difficoltà ordinati per urgenza (R più bassa = più urgente)
- Funzione `getRecommendedSession(n)`: ritorna N esercizi ottimali da fare oggi
- Retention target configurabile (default 85%)
- Il motore NON tocca la UI — solo logica di scheduling
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Modulo srs_scheduler.js con funzioni getDueItems() e getRecommendedSession(n)
- [ ] #2 Calcolo retrievability basato su tempo trascorso dall'ultima review e stability
- [ ] #3 Stability aumenta dopo risposte corrette, diminuisce dopo errori
- [ ] #4 getDueItems() ordina per urgenza (retrievability più bassa prima)
- [ ] #5 getRecommendedSession(n) applica interleaving — mai 2 esercizi consecutivi dello stesso tipo
- [ ] #6 Retention target configurabile (default 85%)
- [ ] #7 Test automatizzati ≥20 per logica di scheduling, edge cases (primo uso, tutti nuovi, tutti scaduti)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

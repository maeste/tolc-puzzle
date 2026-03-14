---
id: TOLC-47
title: TOLC-48 — Lightweight SRS Scheduling Engine
status: Done
assignee: []
created_date: '2026-03-13 10:47'
updated_date: '2026-03-14 22:11'
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
- [x] #1 Modulo srs_scheduler.js con funzioni getDueItems() e getRecommendedSession(n)
- [x] #2 Calcolo retrievability basato su tempo trascorso dall'ultima review e stability
- [x] #3 Stability aumenta dopo risposte corrette, diminuisce dopo errori
- [x] #4 getDueItems() ordina per urgenza (retrievability più bassa prima)
- [x] #5 getRecommendedSession(n) applica interleaving — mai 2 esercizi consecutivi dello stesso tipo
- [x] #6 Retention target configurabile (default 85%)
- [x] #7 Test automatizzati ≥20 per logica di scheduling, edge cases (primo uso, tutti nuovi, tutti scaduti)
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan\n\n1. Create `static/js/srs_scheduler.js` — pure scheduling logic module\n   - Uses SRSTracker data to compute retrievability and recommend exercises\n   - API: getDueItems(), getRecommendedSession(n), getRetention(type, difficulty)\n   - Interleaving: never 2 consecutive same-type exercises\n\n2. Load in base.html after srs_tracker.js\n\n3. Tests in `tests/test_srs_scheduler.py`\n\n4. Update coverage doc
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-47 Complete — Lightweight SRS Scheduling Engine\n\n- Created `static/js/srs_scheduler.js`: pure scheduling module with `window.SRSScheduler` API\n- Retrievability formula: R(t) = e^(-t/S) (FSRS-inspired)\n- `getDueItems()`: all type×difficulty pairs sorted by urgency, includes new items\n- `getRecommendedSession(n)`: interleaved session with priority order (overdue → new → approaching → practice)\n- `getSummary()`: dashboard stats (totalItems, overdueCount, newCount, avgRetention, nextDueIn)\n- Configurable retentionTarget (default 0.85)\n- Integrated into base.html after srs_tracker.js\n- 47 tests in `tests/test_srs_scheduler.py`
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

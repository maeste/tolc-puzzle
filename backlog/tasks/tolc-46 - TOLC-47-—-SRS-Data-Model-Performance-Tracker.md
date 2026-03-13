---
id: TOLC-46
title: TOLC-47 — SRS Data Model & Performance Tracker
status: To Do
assignee: []
created_date: '2026-03-13 10:46'
labels:
  - feature
  - srs
  - data-model
  - foundation
milestone: m-3
dependencies: []
documentation:
  - claudedocs/spaced_repetition_research.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: Per implementare qualsiasi forma di spaced repetition serve prima un modello dati che tracci la performance dell'utente con granularità sufficiente. Attualmente localStorage salva solo completed/accuracy/streak per tipo, senza storico temporale né per-difficulty tracking.

**Scope**:
- Progettare data model in localStorage per tracciare performance per **tipo × difficoltà**
- Per ogni coppia (tipo, difficoltà) salvare: ultimo tentativo (timestamp), numero tentativi, accuracy rolling (ultimi N), stability stimata (giorni), difficulty factor
- Salvare storico risposte recenti (ultime 50-100) con timestamp, tipo, difficoltà, corretto/sbagliato, tempo impiegato
- Migrare dati esistenti (`tolc_progress`, `tolc_wrong`) al nuovo formato senza perdere dati
- Esporre API JavaScript per leggere/scrivere questi dati (modulo `srs_tracker.js`)
- Il modulo deve essere indipendente dalla UI — solo data layer
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Data model localStorage traccia performance per tipo×difficoltà con timestamp
- [ ] #2 Storico ultime 50-100 risposte con tipo, difficoltà, corretto, tempo
- [ ] #3 Migrazione trasparente da tolc_progress/tolc_wrong esistenti al nuovo formato
- [ ] #4 Modulo srs_tracker.js con API pulita: getStats(type, difficulty), recordAnswer(type, difficulty, correct, timeMs), getHistory()
- [ ] #5 Backward-compatible: l'app esistente continua a funzionare durante/dopo migrazione
- [ ] #6 Test automatizzati ≥15 per il data model e la migrazione
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

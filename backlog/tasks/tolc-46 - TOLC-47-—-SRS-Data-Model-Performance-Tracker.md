---
id: TOLC-46
title: TOLC-47 — SRS Data Model & Performance Tracker
status: Done
assignee: []
created_date: '2026-03-13 10:46'
updated_date: '2026-03-14 22:08'
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
- [x] #1 Data model localStorage traccia performance per tipo×difficoltà con timestamp
- [x] #2 Storico ultime 50-100 risposte con tipo, difficoltà, corretto, tempo
- [x] #3 Migrazione trasparente da tolc_progress/tolc_wrong esistenti al nuovo formato
- [x] #4 Modulo srs_tracker.js con API pulita: getStats(type, difficulty), recordAnswer(type, difficulty, correct, timeMs), getHistory()
- [x] #5 Backward-compatible: l'app esistente continua a funzionare durante/dopo migrazione
- [x] #6 Test automatizzati ≥15 per il data model e la migrazione
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

1. Create `static/js/srs_tracker.js` — pure data layer module
   - Data model: `tolc_srs` key in localStorage with structure per type×difficulty
   - API: `SRSTracker.getStats(type, difficulty)`, `SRSTracker.recordAnswer(type, difficulty, correct, timeMs)`, `SRSTracker.getHistory()`, `SRSTracker.migrate()`
   - Migration: reads existing `tolc_progress` and `tolc_wrong`, builds initial SRS entries
   - History: ring buffer of last 100 answers with full metadata

2. Integrate into `templates/base.html` — load script after app.js

3. Hook into existing `Storage.recordAnswer()` in `app.js` — call `SRSTracker.recordAnswer()` in parallel

4. Tests in `tests/test_srs_tracker.py` — test migration logic, data model structure, API contract via Flask test client

5. Update coverage doc
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-46 Complete — SRS Data Model & Performance Tracker\n\n- Created `static/js/srs_tracker.js`: pure data-layer module with `window.SRSTracker` API (init, getStats, recordAnswer, getHistory, getAllStats, migrate, save)\n- Data model: `tolc_srs` localStorage key with per-type×difficulty stats (stability, difficulty factor, rolling accuracy, avg time) + 100-entry history ring buffer\n- Migration from existing `tolc_progress`/`tolc_wrong` without deleting old keys\n- Integrated into `app.js` (Storage.recordAnswer hook) and `base.html` (script tag)\n- 43 tests in `tests/test_srs_tracker.py`
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

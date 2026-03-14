---
id: TOLC-49
title: TOLC-50 — Smart Daily Session Mode
status: Done
assignee: []
created_date: '2026-03-13 10:48'
updated_date: '2026-03-14 22:28'
labels:
  - feature
  - srs
  - ui
  - daily-session
milestone: m-3
dependencies:
  - TOLC-47
  - TOLC-48
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: L'utente oggi deve decidere da solo cosa studiare. Una "Sessione Giornaliera" guidata dall'SRS riduce il carico decisionale e ottimizza l'apprendimento. È il touchpoint principale dove l'utente sperimenta il valore dello spaced repetition.

**Scope**:
- Nuova modalità "Sessione di Oggi" accessibile dal dashboard (accanto a Simulazione e Esame Realistico)
- Genera 15-20 esercizi usando getRecommendedSession() dallo scheduler
- Mix interleaved: mai 2 esercizi consecutivi dello stesso tipo, alternanza di difficoltà
- Feedback immediato dopo ogni risposta (come modalità practice, non come simulazione)
- Al termine: report con statistiche sessione (corrette, tempo, aree migliorate, prossima sessione consigliata)
- Badge/indicatore sul dashboard: "Hai N esercizi da ripassare oggi" con urgenza visuale
- Se non ci sono item scaduti: messaggio "Tutto ripassato! Prossima sessione tra X ore/giorni"
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Nuova modalità 'Sessione di Oggi' accessibile dal dashboard
- [x] #2 Genera 15-20 esercizi interleaved dallo SRS scheduler
- [x] #3 Mai 2 esercizi consecutivi dello stesso tipo nella sessione
- [x] #4 Feedback immediato dopo ogni risposta con spiegazione
- [x] #5 Report fine sessione: corrette, tempo medio, aree migliorate
- [x] #6 Badge dashboard mostra numero esercizi da ripassare oggi
- [x] #7 Messaggio 'tutto ripassato' quando non ci sono item scaduti
- [x] #8 Template Jinja2 + JavaScript per la nuova modalità
- [x] #9 Test automatizzati ≥15 per generazione sessione e UI logic
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-49: Smart Daily Session Mode — Complete

### Changes
- **NEW** `templates/daily_session.html`: Daily session template with progress bar, exercise area, feedback, end-of-session report
- **NEW** `static/js/daily_session.js`: Full session logic — SRS-driven exercise sequencing, immediate feedback, answer tracking, session report with score/time/areas/next session
- **NEW** `tests/test_daily_session.py`: 24 tests
- **MODIFIED** `app.py`: Added `/daily-session` route + `/api/daily-session/exercises` API endpoint (supports `count` + `session` JSON params, fallback to random)
- **MODIFIED** `templates/base.html`: Added "Sessione" nav link
- **MODIFIED** `templates/dashboard.html`: Added SRS daily badge showing overdue count or "tutto ripassato" message
- **MODIFIED** `static/css/style.css`: Added daily-badge, session-progress, session-report styles

### Metrics
- Tests: 24 new
- Full suite: 2274 passed
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

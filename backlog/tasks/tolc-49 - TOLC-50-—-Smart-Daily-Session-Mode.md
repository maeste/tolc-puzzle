---
id: TOLC-49
title: TOLC-50 — Smart Daily Session Mode
status: To Do
assignee: []
created_date: '2026-03-13 10:48'
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
- [ ] #1 Nuova modalità 'Sessione di Oggi' accessibile dal dashboard
- [ ] #2 Genera 15-20 esercizi interleaved dallo SRS scheduler
- [ ] #3 Mai 2 esercizi consecutivi dello stesso tipo nella sessione
- [ ] #4 Feedback immediato dopo ogni risposta con spiegazione
- [ ] #5 Report fine sessione: corrette, tempo medio, aree migliorate
- [ ] #6 Badge dashboard mostra numero esercizi da ripassare oggi
- [ ] #7 Messaggio 'tutto ripassato' quando non ci sono item scaduti
- [ ] #8 Template Jinja2 + JavaScript per la nuova modalità
- [ ] #9 Test automatizzati ≥15 per generazione sessione e UI logic
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

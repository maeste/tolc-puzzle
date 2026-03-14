---
id: TOLC-48
title: TOLC-49 — Wrong Answer Reconsolidation System
status: Done
assignee: []
created_date: '2026-03-13 10:47'
updated_date: '2026-03-14 22:22'
labels:
  - feature
  - srs
  - reconsolidation
  - errors
milestone: m-3
dependencies:
  - TOLC-46
  - TOLC-47
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: Gli errori sono il segnale più forte per il riapprendimento. Il sistema deve dare priorità ai tipi di esercizio dove l'utente ha sbagliato, riproponendoli con varianti diverse (sfruttando i template parametrici già esistenti) a intervalli ravvicinati.

**Scope**:
- Estendere srs_tracker.js per categorizzare gli errori per tipo e pattern
- Quando l'utente sbaglia, il sistema riduce la stability per quel tipo×difficoltà e lo marca come "da riconsolidare"
- Gli item da riconsolidare hanno priorità più alta nel scheduling (boost factor configurabile)
- Nella generazione della sessione, gli errori recenti vengono riproposti con **parametri diversi** (numeri, contesto) — già supportato dai template engine
- Tracking separato: quante volte un errore è stato riconsolidato con successo (3 risposte corrette consecutive → riconsolidazione completata)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Errori riducono stability e marcano tipo×difficoltà come 'da riconsolidare'
- [x] #2 Item da riconsolidare hanno priorità boost nel scheduling (configurabile, default 2x)
- [x] #3 Riconsolidazione usa varianti parametriche (stessa tipologia, numeri diversi)
- [x] #4 Riconsolidazione completata dopo 3 risposte corrette consecutive sullo stesso tipo×difficoltà
- [x] #5 Statistiche errori accessibili: tipo più sbagliato, pattern ricorrenti
- [ ] #6 Test automatizzati ≥12 per logica riconsolidazione e tracking
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-48: Wrong Answer Reconsolidation — Complete

### Changes
- **NEW** `static/js/srs_reconsolidation.js`: Reconsolidation module tracking wrong answers, requiring 3 consecutive correct to complete, 2x urgency boost for active items
- **MODIFIED** `static/js/srs_scheduler.js`: Integrated reconsolidation boost into retention calculation (divides by boost factor)
- **MODIFIED** `static/js/app.js`: Added reconsolidation hooks in Storage.recordAnswer()
- **MODIFIED** `templates/base.html`: Added srs_reconsolidation.js script tag
- **NEW** `tests/test_srs_reconsolidation.py`: 29 tests
- **FIX** `tests/test_srs_scheduler.py`: Updated allowed window dependencies to include SRSReconsolidation

### Metrics
- Tests: 29 new + 1 fixed = 30
- Full suite: 2250 passed
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

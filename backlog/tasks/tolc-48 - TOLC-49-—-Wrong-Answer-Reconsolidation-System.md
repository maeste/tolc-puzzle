---
id: TOLC-48
title: TOLC-49 — Wrong Answer Reconsolidation System
status: To Do
assignee: []
created_date: '2026-03-13 10:47'
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
- [ ] #1 Errori riducono stability e marcano tipo×difficoltà come 'da riconsolidare'
- [ ] #2 Item da riconsolidare hanno priorità boost nel scheduling (configurabile, default 2x)
- [ ] #3 Riconsolidazione usa varianti parametriche (stessa tipologia, numeri diversi)
- [ ] #4 Riconsolidazione completata dopo 3 risposte corrette consecutive sullo stesso tipo×difficoltà
- [ ] #5 Statistiche errori accessibili: tipo più sbagliato, pattern ricorrenti
- [ ] #6 Test automatizzati ≥12 per logica riconsolidazione e tracking
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

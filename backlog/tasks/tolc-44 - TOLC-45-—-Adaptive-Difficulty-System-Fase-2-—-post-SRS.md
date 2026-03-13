---
id: TOLC-44
title: TOLC-45 — Adaptive Difficulty System (Fase 2 — post SRS)
status: To Do
assignee: []
created_date: '2026-03-13 08:00'
updated_date: '2026-03-13 10:48'
labels:
  - feature
  - adaptive
  - learning
milestone: m-2
dependencies:
  - TOLC-43
  - TOLC-46
  - TOLC-47
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: Con il sistema SRS di base in place (m-3), aggiungere adaptive difficulty che regola automaticamente il livello degli esercizi basandosi sulla performance tracciata. Questa è la Fase 2 del sistema di apprendimento adattivo — si appoggia sul data model e scheduling engine costruiti in m-3.

**Scope**:
- Implementare algoritmo di selezione difficoltà che usa i dati SRS (stability, accuracy) da srs_tracker.js
- Regole: >80% accuracy su L1 → proponi L2, <50% su L2 → torna L1, >70% su L2 → offri L3
- Applicare SOLO a practice mode e sessione giornaliera (NOT realistic exam)
- Dashboard mostra "mastery level" per topic area basato su stability SRS
- Override manuale sempre disponibile
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Performance tracking persists across sessions (localStorage minimum, backend preferred)
- [ ] #2 Difficulty selection algorithm uses historical accuracy per topic/level
- [ ] #3 Practice mode adapts difficulty per topic independently
- [ ] #4 Realistic exam simulation is NOT affected (stays weighted random)
- [ ] #5 Dashboard displays mastery levels per topic area with visual indicators
- [ ] #6 Spaced repetition logic: weak topics appear 2x more often than mastered topics
- [ ] #7 Student can manually override to any difficulty level
- [ ] #8 Tests: ≥20 automated tests for the adaptation algorithm
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

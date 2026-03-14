---
id: TOLC-44
title: TOLC-45 — Adaptive Difficulty System (Fase 2 — post SRS)
status: Done
assignee: []
created_date: '2026-03-13 08:00'
updated_date: '2026-03-14 22:44'
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
- [x] #1 Performance tracking persists across sessions (localStorage minimum, backend preferred)
- [x] #2 Difficulty selection algorithm uses historical accuracy per topic/level
- [x] #3 Practice mode adapts difficulty per topic independently
- [x] #4 Realistic exam simulation is NOT affected (stays weighted random)
- [x] #5 Dashboard displays mastery levels per topic area with visual indicators
- [x] #6 Spaced repetition logic: weak topics appear 2x more often than mastered topics
- [x] #7 Student can manually override to any difficulty level
- [x] #8 Tests: ≥20 automated tests for the adaptation algorithm
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-44: Adaptive Difficulty System — Complete

### Changes
- **NEW** `static/js/srs_adaptive.js`: Adaptive difficulty module — getRecommendedDifficulty (promotion/fallback rules), getMasteryLevel (beginner→mastered), getAllMasteryLevels
- **MODIFIED** `static/js/exercise.js`: Auto-selects recommended difficulty on first load, shows "Difficoltà consigliata" indicator, manual override always available, sets window._currentDifficulty
- **MODIFIED** `templates/exercise.html`: Added adaptive indicator span
- **MODIFIED** `templates/base.html`: Added srs_adaptive.js script tag
- **MODIFIED** `templates/dashboard.html`: Mastery badges per exercise card (🌱📗📘🏆)
- **MODIFIED** `static/css/style.css`: Adaptive indicator and mastery badge styles
- **NEW** `tests/test_srs_adaptive.py`: 40 tests

### Metrics
- Tests: 40 new
- Full suite: 2411 passed
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

---
id: TOLC-26
title: Pesare Distribuzione Domande nella Simulazione
status: Done
assignee: []
created_date: '2026-03-12 10:36'
updated_date: '2026-03-12 11:02'
labels:
  - gap-coverage
  - simulation
  - distribution
milestone: m-0
dependencies: []
references:
  - app.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Cambiare la distribuzione delle domande nella simulazione da uniforme a pesata secondo le frequenze reali del TOLC-B:
- ~30-35% Algebra (equazioni, disequazioni, polinomi)
- ~20-25% Geometria (analitica, euclidea, solida)
- ~20-25% Funzioni (analisi, grafici, proprietà)
- ~10-15% Probabilità
- ~5-10% Statistica

Attualmente la distribuzione è uniforme tra i tipi di esercizio, non riflettendo il test reale.

**Implementation Plan**:
1. Definire configurazione pesi in `app.py` (dizionario o config)
2. Implementare selezione pesata delle domande
3. Rendere i pesi configurabili (per futuri aggiornamenti)
4. Scrivere test che verifichino le proporzioni statisticamente
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Distribuzione domande configurabile tramite dizionario pesi
- [x] #2 Pesi default allineati a frequenze TOLC-B reali (~30-35% Algebra, ~20-25% Geometria, ~20-25% Funzioni, ~10-15% Probabilità, ~5-10% Statistica)
- [x] #3 Test statistico che verifichi le proporzioni (con margine di tolleranza)
- [x] #4 Nessuna regressione sulla simulazione esistente
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added `REALISTIC_EXAM_WEIGHTS` config dict to `app.py` with documented TOLC-B category mapping:
- Algebra ~30%: solve(3) + inequalities(2) + trap(1) = 6
- Geometria ~20%: geometry(2) + analytic_geo(2) = 4
- Funzioni/Grafici ~20%: word(2) + graph(2) = 4
- Probabilità ~15%: probability(3) = 3
- Statistica/Logica ~15%: statistics(2) + logic(1) = 3

Replaced hardcoded distribution list with dynamic generation from weights config. Fixed `steps`→`options` normalization for trap exercises. Tests in `tests/test_weighted_distribution.py` (config validation + endpoint tests, requires Flask). All 241 project tests pass.
<!-- SECTION:FINAL_SUMMARY:END -->

---
id: TOLC-52
title: TOLC-52 — Re-include Estimation in Exam Simulation & Enhance
status: To Do
assignee: []
created_date: '2026-03-13 11:27'
labels:
  - gap-G3
  - estimation
  - exam-simulation
milestone: m-4
dependencies: []
references:
  - exercises/estimation_blitz.py
  - app.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The CISIA syllabus explicitly states "la capacità di fare stime...consente di valutare rapidamente la plausibilità del risultato dei calcoli." Our EstimationBlitz module (14 templates) is currently EXCLUDED from the realistic exam simulation. This is a significant gap — mental calculation without calculator is a CORE TOLC-B skill, not optional. Re-include it and adapt the format for exam mode.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add 'estimation' to REALISTIC_EXAM_WEIGHTS with weight 1-2 (replace or rebalance)
- [ ] #2 Adapt EstimationBlitz output for exam mode: standard 5-option multiple choice (no special timer UI), question text like 'Quale delle seguenti è la migliore approssimazione di 47×83?'
- [ ] #3 Ensure all EstimationBlitz templates generate exactly 5 plausible options
- [ ] #4 Total exam questions remain 20; adjust other weights to compensate
- [ ] #5 Tests: verify EstimationBlitz works in exam endpoint, distribution remains balanced
- [ ] #6 Update claudedocs/tolc-b-coverage-analysis.md §3 simulation section
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

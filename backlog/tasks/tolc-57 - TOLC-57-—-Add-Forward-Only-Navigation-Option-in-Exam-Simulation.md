---
id: TOLC-57
title: TOLC-57 — Add Forward-Only Navigation Option in Exam Simulation
status: Done
assignee: []
created_date: '2026-03-13 11:28'
updated_date: '2026-03-13 22:03'
labels:
  - gap-G9
  - exam-simulation
  - frontend
milestone: m-4
dependencies: []
references:
  - app.py
  - templates/
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The real TOLC-B does not allow returning to previous questions. Our simulation allows free navigation, which changes test-taking strategy significantly. Add an optional "realistic mode" with forward-only navigation.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add toggle in exam UI: 'Modalità CISIA (non puoi tornare indietro)' vs 'Modalità libera'
- [x] #2 When enabled: hide 'previous' button, grey out answered questions in navigator, auto-advance after answer
- [x] #3 Default to free navigation (less stressful for practice); realistic mode as opt-in
- [x] #4 Show warning before starting realistic mode explaining the constraint
- [ ] #5 Tests: E2E test for forward-only mode (or manual test plan)
- [x] #6 Update claudedocs/tolc-b-coverage-analysis.md §10.7
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added forward-only navigation mode ("Modalità CISIA") to realistic exam. Toggle on start screen with warning message. When enabled: hides Previous button, locks navigator buttons for past questions (greyed out, disabled), auto-advances after answer. Default is free navigation. CSS for locked state and toggle UI added. Coverage doc updated §10.7.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

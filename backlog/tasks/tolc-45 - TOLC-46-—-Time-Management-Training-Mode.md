---
id: TOLC-45
title: TOLC-46 — Time Management Training Mode
status: To Do
assignee: []
created_date: '2026-03-13 08:00'
labels:
  - feature
  - time-management
  - training
milestone: m-2
dependencies:
  - TOLC-43
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
**Why**: Time pressure is a major factor in real TOLC (2:30 per question). Students need to practice deciding WHEN to skip, WHEN to guess, and HOW to allocate time.

**Scope**:
- New "Time Training" mode accessible from dashboard
- Features:
  - Per-question timer with visual indicator (green/yellow/red at 1:30/2:00/2:30)
  - "Skip" button with strategy feedback ("Good skip — this was a hard question")
  - Post-session time analysis: time per question vs correctness graph
  - Guessing strategy training: "You eliminated 3 options — guessing is +EV here"
  - Expected value calculator for guess decisions displayed in review
- Time pressure simulation: questions auto-advance after configurable timeout (default: 3 min)
- Statistics: avg time per correct/incorrect answer, time wasted on wrong answers
- Does not interfere with existing practice/exam modes
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Per-question timer with color-coded visual indicator (green/yellow/red)
- [ ] #2 Skip button available with strategy feedback in review
- [ ] #3 Post-session report shows time-per-question scatter plot (time vs correct/incorrect)
- [ ] #4 Guessing EV feedback when student eliminates ≥2 options
- [ ] #5 Auto-advance option after configurable timeout
- [ ] #6 Time statistics tracked and displayed: avg time correct, avg time incorrect, total skips
- [ ] #7 Does not interfere with existing practice/exam modes
- [ ] #8 Tests: ≥15 automated tests
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

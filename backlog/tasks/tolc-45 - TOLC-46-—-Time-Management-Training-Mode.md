---
id: TOLC-45
title: TOLC-46 — Time Management Training Mode
status: Done
assignee: []
created_date: '2026-03-13 08:00'
updated_date: '2026-03-13 23:38'
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
- [x] #1 Per-question timer with color-coded visual indicator (green/yellow/red)
- [x] #2 Skip button available with strategy feedback in review
- [x] #3 Post-session report shows time-per-question scatter plot (time vs correct/incorrect)
- [x] #4 Guessing EV feedback when student eliminates ≥2 options
- [x] #5 Auto-advance option after configurable timeout
- [x] #6 Time statistics tracked and displayed: avg time correct, avg time incorrect, total skips
- [x] #7 Does not interfere with existing practice/exam modes
- [x] #8 Tests: ≥15 automated tests
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

1. Backend:
   - Add `/time-training` route in `app.py`
   - Create `templates/time_training.html` with timer UI
   - Reuse existing exercise generation API (`/api/exercise/<type>`)
2. Frontend (`static/js/time_training.js`):
   - Per-question timer with color-coded indicator (green <1:30, yellow <2:00, red <2:30)
   - Skip button with strategy feedback
   - Auto-advance after configurable timeout (default 3 min)
   - Post-session time analysis: time per question vs correctness
   - Guessing EV feedback when ≥2 options eliminated
   - Time statistics: avg time correct/incorrect, total skips
3. Dashboard: Add "Time Training" button in `templates/dashboard.html`
4. CSS: Add timer styles in `static/css/style.css`
5. Tests: ≥15 automated tests for time training logic
6. Ensure no interference with existing practice/exam modes
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## TOLC-45 Complete — Time Management Training Mode

### Deliverables
- **`templates/time_training.html`**: Three-screen template (setup → exercise → results) with configurable question count (10/15/20), timeout (2:00/2:30/3:00), and exercise type selection
- **`static/js/time_training.js`**: Vanilla JS with circular SVG countdown timer (green→yellow→red), option elimination via right-click/long-press, EV calculation and hint display, auto-advance on timeout, post-session scatter plot, time statistics, strategy feedback
- **`tests/test_time_training.py`**: 29 tests (route tests, exercise API integration, EV formula, TOLC scoring, strategy feedback, dashboard/nav links)
- **`app.py`**: Added `/time-training` route
- **`templates/base.html`**: Added "Tempo" nav link
- **`templates/dashboard.html`**: Added accent-styled CTA button for time training
- **`static/css/style.css`**: Added styles for timer, eliminated options, EV hint, scatter plot, time stats, strategy feedback

### Features
- Per-question circular SVG timer with color transitions (green <1:30, yellow <2:00, red <timeout)
- Skip button with contextual strategy feedback in results
- Post-session scatter plot (time vs correctness per question)
- Guessing EV feedback when ≥2 options eliminated (TOLC scoring: +1/-0.25/0)
- Auto-advance after configurable timeout
- Time statistics: avg time correct/incorrect, total skips, time wasted on wrong answers
- Session history persisted in localStorage
- No interference with existing practice/exam modes
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

---
id: TOLC-58
title: TOLC-58 — Improve Test Coverage for Under-Tested Modules
status: To Do
assignee: []
created_date: '2026-03-13 11:28'
labels:
  - quality
  - testing
milestone: m-4
dependencies: []
references:
  - tests/test_analytic_geometry.py
  - tests/test_statistics.py
  - tests/
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Our test suite has critical gaps: test_analytic_geometry.py has only 1 test, test_statistics.py has only 2 tests, and most exercise types don't test their check() methods. Improve coverage for the weakest areas.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 test_analytic_geometry.py: expand to ≥20 tests covering all 9 templates across 3 difficulty levels
- [ ] #2 test_statistics.py: expand to ≥15 tests covering all template types and graph reading
- [ ] #3 Add check() method tests for at least: analytic_geometry, statistics, inequalities, simplification
- [ ] #4 Add 1 integration test that generates a full 20-question exam and validates all exercises are well-formed
- [ ] #5 Total test count should increase by ≥50
- [ ] #6 Update claudedocs/tolc-b-coverage-analysis.md §7.2 test count
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

---
id: TOLC-62
title: TOLC-63 — Add Strategy Selection Exercises
status: To Do
assignee: []
created_date: '2026-03-13 11:28'
labels:
  - gap-G13
  - mindset
  - strategy
milestone: m-4
dependencies: []
references:
  - claudedocs/tolc-b-coverage-analysis.md
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The CISIA syllabus emphasizes "scegliere una strategia di operazioni efficace" and "scegliere quelle [procedure] più efficienti e più semplici." We have no exercise that tests whether students can identify the BEST approach to solve a problem. This is a mindset skill, not just a knowledge skill.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add 4-6 templates (new module or integrated into existing): L1 (given an equation, which method solves it fastest: factoring vs formula vs substitution?), L2 (given an expression, which simplification path is shortest?), L3 (given a geometry problem, which approach works: coordinates vs synthetic vs trigonometric?)
- [ ] #2 Question format: 'Quale strategia è più efficiente per risolvere...?' with 5 strategy options
- [ ] #3 Include brief explanation of WHY one strategy is better (educational value)
- [ ] #4 5-option multiple choice format
- [ ] #5 Tests: ≥15 automated tests
- [ ] #6 Update claudedocs/tolc-b-coverage-analysis.md §2.9: add new cognitive competency 'Scelta strategica'
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

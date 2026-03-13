---
id: TOLC-59
title: TOLC-60 — Add Multiple Representation Exercises
status: To Do
assignee: []
created_date: '2026-03-13 11:28'
labels:
  - gap-G10
  - functions
  - representations
milestone: m-4
dependencies: []
references:
  - exercises/graph_reader.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The CISIA syllabus cross-cutting skill "Comprendere e rappresentare" states: "A seconda delle situazioni e degli obiettivi, utilizzare diverse rappresentazioni di uno stesso oggetto matematico." Under Functions: "mettere in relazione tra di loro le informazioni che si ricavano da diverse rappresentazioni di una stessa funzione." Currently our GraphReader only has graph↔formula matching. Missing: table representations, verbal descriptions, formula-form conversions, and standalone transformation identification.

Current state in graph_reader.py: Only 1 true representation-matching template exists (the main generate() with bidirectional graph↔formula). All other 15 templates are property-analysis exercises, not representation matching.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Add table→formula templates (3+): Show a table of (x,y) values, ask 'Quale funzione genera questa tabella?' with 5 formula options. Use function families: linear, quadratic, exponential, logarithmic. L1: linear/quadratic tables. L2: exponential/log tables. L3: ambiguous tables requiring reasoning.
- [ ] #2 Add table→graph templates (2+): Show a table of values and 5 SVG graphs, ask 'Quale grafico corrisponde a questa tabella?' L2-L3.
- [ ] #3 Add verbal→formula templates (2+): 'Una funzione che raddoppia il suo valore ogni volta che x aumenta di 1' → identify f(x)=2^x among options. L1: simple verbal descriptions. L2: more complex descriptions involving domain/range constraints.
- [ ] #4 Add formula-form conversion templates (2+): Match standard form ax²+bx+c to vertex form a(x-h)²+k, or factored form. L2-L3.
- [ ] #5 All templates produce 5-option multiple choice compatible with exam simulation
- [ ] #6 Each representation type has at least 10 parametric variations (no repetition)
- [ ] #7 Tests: ≥30 automated tests covering all new template types
- [ ] #8 Update claudedocs/tolc-b-coverage-analysis.md §2.2 and §2.9: mark 'Rappresentazioni multiple' as IMPLEMENTATO
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Test automatizzati passano (pytest)
- [ ] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [ ] #3 Esercizi generati correttamente con distrattori sensati
- [ ] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

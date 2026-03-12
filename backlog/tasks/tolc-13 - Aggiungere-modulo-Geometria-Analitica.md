---
id: TOLC-13
title: Aggiungere modulo Geometria Analitica
status: To Do
assignee: []
created_date: '2026-03-12 07:22'
labels:
  - syllabus-gap
  - new-module
  - matematica
milestone: m-0
dependencies: []
references:
  - exercises/geometry_sherlock.py
  - exercises/solve_exercise.py
  - app.py
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Il TOLC-B Puzzle non ha alcun esercizio di geometria analitica, che è una macro-area chiave del syllabus CISIA. Serve un nuovo modulo (o estensione di Geometry Sherlock tipo F) che copra: equazione della retta (y=mx+q, forma implicita), distanza tra due punti, punto medio, condizioni di parallelismo e perpendicolarità, equazione della circonferenza (x-a)²+(y-b)²=r², asse di un segmento, intersezione retta-circonferenza.

**Contesto tecnico**: I moduli esercizio sono in `exercises/`, ereditano da una base class con metodo `generate(difficulty)`. Ogni esercizio restituisce question, options, correct_index, explanation, did_you_know. Il registry è in `app.py`. Seguire lo stesso pattern degli altri moduli (3 livelli di difficoltà, template parametrici con randomizzazione).

**File di riferimento**: `exercises/geometry_sherlock.py` (pattern geometria), `exercises/solve_exercise.py` (pattern calcolo), `app.py` (registry), `claudedocs/tolc-b-coverage-analysis.md` (tracciamento).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Nuovo file `exercises/analytic_geometry.py` (o estensione di geometry_sherlock.py) con classe che eredita dalla base class
- [ ] #2 Livello 1: equazione retta dato punto e pendenza, distanza tra due punti, punto medio
- [ ] #3 Livello 2: parallelismo/perpendicolarità tra rette, equazione retta per due punti, asse di un segmento
- [ ] #4 Livello 3: equazione circonferenza, intersezione retta-circonferenza, problemi combinati
- [ ] #5 Almeno 8 template parametrici distinti con randomizzazione
- [ ] #6 Registrato in app.py nel registry degli esercizi con tipo e metadata
- [ ] #7 Test pytest che verifica generazione senza errori per tutti e 3 i livelli (almeno 10 generazioni per livello)
- [ ] #8 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stati da ASSENTE a IMPLEMENTATO nella sezione 2.4, spuntare R1 in sezione 4, aggiungere riga al Registro Modifiche in sezione 5
<!-- AC:END -->

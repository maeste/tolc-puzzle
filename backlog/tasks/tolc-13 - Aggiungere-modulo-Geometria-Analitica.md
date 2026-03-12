---
id: TOLC-13
title: Aggiungere modulo Geometria Analitica
status: Done
assignee:
  - claude
created_date: '2026-03-12 07:22'
updated_date: '2026-03-12 08:09'
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
- [x] #1 Nuovo file `exercises/analytic_geometry.py` (o estensione di geometry_sherlock.py) con classe che eredita dalla base class
- [x] #2 Livello 1: equazione retta dato punto e pendenza, distanza tra due punti, punto medio
- [x] #3 Livello 2: parallelismo/perpendicolarità tra rette, equazione retta per due punti, asse di un segmento
- [x] #4 Livello 3: equazione circonferenza, intersezione retta-circonferenza, problemi combinati
- [x] #5 Almeno 8 template parametrici distinti con randomizzazione
- [x] #6 Registrato in app.py nel registry degli esercizi con tipo e metadata
- [x] #7 Test pytest che verifica generazione senza errori per tutti e 3 i livelli (almeno 10 generazioni per livello)
- [x] #8 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stati da ASSENTE a IMPLEMENTATO nella sezione 2.4, spuntare R1 in sezione 4, aggiungere riga al Registro Modifiche in sezione 5
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Nuovo file `exercises/analytic_geometry.py` con classe `AnalyticGeometry(Exercise)`\n2. L1 (3 template): equazione retta dato punto+pendenza, distanza tra punti, punto medio\n3. L2 (3 template): parallele/perpendicolari, retta per due punti, asse segmento\n4. L3 (3 template): equazione circonferenza, intersezione retta-circonferenza, problema combinato\n5. Registrare in `app.py` come tipo `analytic_geo` con metadata\n6. Test pytest in `tests/test_analytic_geometry.py`: 10 generazioni per livello\n7. Aggiornare `claudedocs/tolc-b-coverage-analysis.md` sezione 2.4, R1, Registro Modifiche
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Creato `exercises/analytic_geometry.py` con classe `AnalyticGeometry(Exercise)` — 9 template su 3 livelli:\n- L1: equazione retta (punto+pendenza), distanza tra punti, punto medio\n- L2: parallele/perpendicolari, retta per due punti, asse segmento\n- L3: equazione circonferenza, intersezione retta-circonferenza, problema combinato\n\nRegistrato in `app.py` come tipo `analytic_geo`. Test in `tests/test_analytic_geometry.py` (30 generazioni, tutti verdi). Coverage doc aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

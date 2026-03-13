---
id: TOLC-25
title: Includere Grafici nella Simulazione Esame
status: Done
assignee: []
created_date: '2026-03-12 10:36'
updated_date: '2026-03-12 11:02'
labels:
  - gap-coverage
  - simulation
  - svg-graphics
milestone: m-0
dependencies: []
references:
  - app.py
  - static/js/realistic_exam.js
  - templates/realistic_exam.html
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modificare la simulazione realistica per includere domande con grafici SVG, come nel TOLC-B reale dove molte domande presentano grafici di funzioni, figure geometriche, o diagrammi.

I moduli GraphReader e GeometrySherlock già generano SVG — serve integrarli nel flusso della simulazione esame.

**Implementation Plan**:
1. Modificare `app.py` per includere domande con grafici nella simulazione realistica
2. Aggiornare `static/js/realistic_exam.js` per rendering SVG inline
3. Aggiornare `templates/realistic_exam.html` per layout domande con grafici
4. Garantire almeno 3-4 domande con grafici su 20 totali
5. Testare rendering cross-browser
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Almeno 3-4 domande con grafici SVG su 20 nella simulazione esame
- [x] #2 Rendering SVG funzionante e leggibile in realistic_exam
- [x] #3 Domande grafiche provengono da GraphReader e/o GeometrySherlock
- [x] #4 Layout responsive per grafici su desktop e mobile
- [x] #5 Nessuna regressione sulla simulazione esistente
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Integrated SVG graph questions into the realistic exam simulation:

**Backend** (`app.py`): Added `graph: 2` to `REALISTIC_EXAM_WEIGHTS` (4 SVG questions total: 2 graph + 2 geometry). Removed `graph_data` stripping so SVG data passes to frontend.

**Frontend** (`static/js/realistic_exam.js`): Added `graph_data` check in `renderCurrentQuestion()` and `generateReview()` — inserts SVG into `.sim-graph-container` div when present.

**CSS** (`static/css/style.css`): Added `.sim-graph-container` styles — centered flex layout, max-width 500px, responsive SVG scaling, mobile breakpoint at 600px.

**HTML** (`templates/realistic_exam.html`): Updated rules text to indicate some questions include graphs.

All 241 project tests pass with no regressions.
<!-- SECTION:FINAL_SUMMARY:END -->

---
id: TOLC-37
title: Reassessment Critico Post-Implementazione Gap Cognitivi
status: Done
assignee: []
created_date: '2026-03-12 11:47'
updated_date: '2026-03-13 06:57'
labels:
  - assessment
  - quality-gate
milestone: TOLC-B Competenze Cognitive v3
dependencies:
  - TOLC-31
  - TOLC-32
  - TOLC-33
  - TOLC-34
  - TOLC-35
  - TOLC-36
references:
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contesto

Dopo l'implementazione di tutti i gap cognitivi (TOLC-31 → TOLC-36), serve un reassessment onesto confrontando le stesse 20 domande Alpha Test con l'app aggiornata.

## Obiettivo

Misurare il miglioramento EFFETTIVO della copertura per COMPETENZA (non solo per argomento). Il baseline attuale è: 35% coperto, 15% parziale, 50% non coperto.

## Implementation Plan

1. **Rifare l'analisi delle 20 domande Alpha Test** confrontando con l'app aggiornata
2. **Calcolare nuovo % di copertura** per competenza cognitiva:
   - "Risolvi/Calcola" (già coperto)
   - "Semplifica/Identifica equivalente" (TOLC-31)
   - "Sempre/Mai vero" (TOLC-32)
   - "Leggi il grafico" (TOLC-33)
   - "Ragiona su proporzionalità" (TOLC-34)
   - "Geometria avanzata" (TOLC-35)
   - "Cross-topic" (TOLC-36)
3. **Aggiornare `claudedocs/tolc-b-coverage-analysis.md`** con nuova sezione "Assessment v3"
4. **Report onesto** con metriche prima/dopo e gap residui

### Output atteso
- Tabella confronto 20 domande: prima vs dopo
- % copertura per competenza cognitiva
- Gap residui identificati e prioritizzati
- Raccomandazioni per iterazione successiva

### Dipendenze
Questo task può essere eseguito SOLO dopo il completamento di TOLC-31, TOLC-32, TOLC-33, TOLC-34, TOLC-35 e TOLC-36.

### File da modificare
- `claudedocs/tolc-b-coverage-analysis.md` — nuova sezione assessment v3
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Analisi delle stesse 20 domande Alpha Test confrontate con l'app aggiornata
- [x] #2 Tabella confronto prima/dopo per ogni domanda con stato aggiornato
- [x] #3 % copertura per competenza cognitiva (non solo per argomento)
- [x] #4 Metriche quantitative: % coperto / parziale / non coperto prima vs dopo
- [x] #5 Gap residui identificati e prioritizzati per eventuale iterazione successiva
- [x] #6 claudedocs/tolc-b-coverage-analysis.md aggiornato con sezione Assessment v3
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Assessment v3 Complete\n\nRe-analyzed the same 20 Alpha Test questions against the updated app.\n\n### Key Results\n- **Coverage: 35% → 75%** (15/20 questions fully covered, up from 7/20)\n- **Non-covered: 50% → 10%** (only 2 questions remain uncovered)\n- Simplification competency: 0/6 → 6/6 (biggest single improvement)\n- All 7 cognitive competencies now have at least partial coverage\n\n### Residual Gaps (low priority)\n- Q4: Parabola in analytic geometry (rare in TOLC-B)\n- Q14: Cone lateral surface development (very specific)\n\n### Files Modified\n- `claudedocs/tolc-b-coverage-analysis.md` — Added §9 Assessment v3 with full before/after comparison table, cognitive competency breakdown, residual gap analysis, and updated simulation realism scores"
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Tutti i task dipendenti (TOLC-31 attraverso TOLC-36) sono completati
- [x] #2 Report onesto senza marketing language
- [x] #3 Coverage doc aggiornato con metriche verificabili
<!-- DOD:END -->

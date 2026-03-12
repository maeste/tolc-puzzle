---
id: TOLC-20
title: Aggiungere modo esame realistico con formato diretto TOLC
status: Done
assignee: []
created_date: '2026-03-12 07:23'
updated_date: '2026-03-12 09:19'
labels:
  - new-feature
  - ux
  - exam-format
milestone: m-0
dependencies: []
references:
  - app.py
  - templates/simulation.html
  - exercises/
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
La simulazione TOLC-B esistente usa i mini-giochi come formato domanda. Nel TOLC-B reale le domande sono in formato diretto (testo + 5 opzioni di risposta). Serve una modalità aggiuntiva che presenti domande in formato più fedele all'esame reale, per familiarizzare lo studente con il formato effettivo.

**Cosa implementare**:
- Nuova modalità "Esame Realistico" accessibile dalla dashboard accanto alla simulazione esistente
- Le domande sono in formato testo diretto (non mini-gioco): "Risolvere l'equazione...", "Quale delle seguenti affermazioni è vera?", etc.
- 5 opzioni di risposta (come nel TOLC-B reale, non 4)
- Punteggio TOLC-B: +1 corretta, 0 non data, -0.25 errata
- Timer globale 50 minuti, 20 domande miste

**Differenza dalla simulazione esistente**: la simulazione attuale usa i mini-giochi (trova la trappola, detective logico, etc.). Questa modalità presenta domande "nude" in formato classico.

**File di riferimento**: `app.py` (route), `templates/simulation.html` (pattern UI), i moduli `exercises/` per la generazione delle domande, `claudedocs/tolc-b-coverage-analysis.md`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Nuova route `/realistic-exam` con template dedicato
- [x] #2 Domande in formato testo diretto senza elementi di mini-gioco (no SVG interattivi, no meccaniche di gioco)
- [x] #3 5 opzioni di risposta per domanda (non 4) come nel TOLC-B reale
- [x] #4 Punteggio: +1 corretta, 0 non data, -0.25 errata, con possibilità di saltare
- [x] #5 20 domande distribuite tra le aree del syllabus
- [x] #6 Timer globale 50 minuti
- [x] #7 Report finale con punteggio e breakdown per area
- [x] #8 Accessibile dalla dashboard principale con chiara distinzione dalla simulazione mini-gioco
- [x] #9 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: spuntare R8 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implementata modalità Esame Realistico completa:\n- Route `/realistic-exam` in `app.py` con template `templates/realistic_exam.html`\n- API `/api/realistic-exam/exercises` genera 20 domande text-only, 5 opzioni A-E, stripping graph_data\n- JS `static/js/realistic_exam.js` con selezione opzioni A-E, timer 50min, punteggio +1/0/-0.25, review domande post-consegna\n- Link in dashboard (secondo CTA in simulation-cta) e navbar (`templates/base.html`)\n- Stili `.exam-option`, `.exam-option-letter` in `static/css/style.css`
<!-- SECTION:FINAL_SUMMARY:END -->

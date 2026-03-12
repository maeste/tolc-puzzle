---
id: TOLC-20
title: Aggiungere modo esame realistico con formato diretto TOLC
status: To Do
assignee: []
created_date: '2026-03-12 07:23'
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
- [ ] #1 Nuova route `/realistic-exam` con template dedicato
- [ ] #2 Domande in formato testo diretto senza elementi di mini-gioco (no SVG interattivi, no meccaniche di gioco)
- [ ] #3 5 opzioni di risposta per domanda (non 4) come nel TOLC-B reale
- [ ] #4 Punteggio: +1 corretta, 0 non data, -0.25 errata, con possibilità di saltare
- [ ] #5 20 domande distribuite tra le aree del syllabus
- [ ] #6 Timer globale 50 minuti
- [ ] #7 Report finale con punteggio e breakdown per area
- [ ] #8 Accessibile dalla dashboard principale con chiara distinzione dalla simulazione mini-gioco
- [ ] #9 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: spuntare R8 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

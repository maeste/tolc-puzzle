---
id: TOLC-37
title: Reassessment Critico Post-Implementazione Gap Cognitivi
status: To Do
assignee: []
created_date: '2026-03-12 11:47'
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
- [ ] #1 Analisi delle stesse 20 domande Alpha Test confrontate con l'app aggiornata
- [ ] #2 Tabella confronto prima/dopo per ogni domanda con stato aggiornato
- [ ] #3 % copertura per competenza cognitiva (non solo per argomento)
- [ ] #4 Metriche quantitative: % coperto / parziale / non coperto prima vs dopo
- [ ] #5 Gap residui identificati e prioritizzati per eventuale iterazione successiva
- [ ] #6 claudedocs/tolc-b-coverage-analysis.md aggiornato con sezione Assessment v3
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Tutti i task dipendenti (TOLC-31 attraverso TOLC-36) sono completati
- [ ] #2 Report onesto senza marketing language
- [ ] #3 Coverage doc aggiornato con metriche verificabili
<!-- DOD:END -->

---
id: TOLC-22
title: Rivalutazione copertura TOLC-B post-implementazione
status: To Do
assignee: []
created_date: '2026-03-12 07:29'
labels:
  - valutazione
  - documentazione
milestone: m-0
dependencies:
  - TOLC-13
  - TOLC-14
  - TOLC-15
  - TOLC-16
  - TOLC-17
  - TOLC-18
  - TOLC-19
  - TOLC-20
  - TOLC-21
references:
  - claudedocs/tolc-b-coverage-analysis.md
  - exercises/
  - app.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Dopo il completamento di tutti i task del milestone "TOLC-B Coverage Alignment", eseguire una rivalutazione completa della copertura del syllabus TOLC-B. Confrontare lo stato iniziale (documentato in `claudedocs/tolc-b-coverage-analysis.md` sezione 2 e 3) con lo stato attuale verificando il codice effettivamente implementato.

**Cosa fare**:
1. Riesaminare ogni argomento nelle tabelle di copertura (sezione 2) verificando nel codice che gli stati IMPLEMENTATO siano corretti
2. Ricalcolare le percentuali di copertura (sezione 3)
3. Creare una nuova **sezione 7 — Confronto Copertura Pre/Post** nel documento di tracciamento con:
   - Tabella comparativa prima/dopo per ogni macro-area
   - Percentuali di copertura iniziali vs finali
   - Argomenti che restano scoperti (se presenti) con motivazione
   - Valutazione qualitativa dei miglioramenti
4. Aggiornare il Registro Modifiche (sezione 5) con questa rivalutazione finale

**Input**: Il documento `claudedocs/tolc-b-coverage-analysis.md` aggiornato dai task precedenti + il codice in `exercises/` e `app.py`.

**Baseline iniziale** (da sezione 3 del documento):
- COPERTO: 28 (68%)
- PARZIALE: 1 (2%)
- ASSENTE: 13 (32%)
- EXTRA: 4
- Copertura effettiva: ~70%

**File di riferimento**: `claudedocs/tolc-b-coverage-analysis.md`, tutti i file in `exercises/`, `app.py`, `templates/`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Verificato nel codice sorgente che ogni stato IMPLEMENTATO nel documento di tracciamento corrisponde a codice effettivamente funzionante
- [ ] #2 Ricalcolate le percentuali di copertura nella sezione 3 del documento
- [ ] #3 Creata nuova sezione 7 'Confronto Copertura Pre/Post' in `claudedocs/tolc-b-coverage-analysis.md` con tabella comparativa per macro-area (colonne: Macro-area, Coperti Prima, Coperti Dopo, Delta)
- [ ] #4 La sezione 7 include percentuali aggregate: copertura iniziale (~70%) vs copertura finale
- [ ] #5 La sezione 7 elenca eventuali argomenti ancora scoperti con motivazione
- [ ] #6 La sezione 7 include una valutazione qualitativa sintetica dei miglioramenti ottenuti
- [ ] #7 Aggiunta riga al Registro Modifiche (sezione 5) con data e descrizione della rivalutazione
<!-- AC:END -->

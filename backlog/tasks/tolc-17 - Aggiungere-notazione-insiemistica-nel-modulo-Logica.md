---
id: TOLC-17
title: Aggiungere notazione insiemistica nel modulo Logica
status: To Do
assignee: []
created_date: '2026-03-12 07:23'
labels:
  - syllabus-gap
  - enhancement
  - matematica
milestone: m-0
dependencies: []
references:
  - exercises/logic_puzzle.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Il modulo Logic Puzzle (tipo D) copre negazione, quantificatori e implicazioni ma manca di esercizi sulla notazione insiemistica (∈, ⊂, ⊆, ∪, ∩, complemento, differenza), che è parte del syllabus TOLC-B nella sezione Logica e Insiemi.

**Cosa implementare**: Nuovi template in `exercises/logic_puzzle.py` che chiedano:
- Interpretazione di espressioni insiemistiche: "Se A = {1,2,3} e B = {2,3,4}, quanto vale A ∩ B?"
- Operazioni tra insiemi: unione, intersezione, complemento, differenza
- Appartenenza e inclusione: "Quale affermazione è vera? a) 3 ∈ A  b) A ⊂ B ..."
- Diagrammi di Venn (descritti testualmente): "Dato il diagramma, quanti elementi ha A ∪ B?"

**File di riferimento**: `exercises/logic_puzzle.py`, `claudedocs/tolc-b-coverage-analysis.md`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Almeno 5 nuovi template per operazioni insiemistiche (∪, ∩, complemento, differenza, prodotto cartesiano)
- [ ] #2 Template per appartenenza (∈) e inclusione (⊂, ⊆) con domande vero/falso
- [ ] #3 Template per diagrammi di Venn descritti testualmente con domande di conteggio
- [ ] #4 Integrazione nei 3 livelli di difficoltà: Livello 1 = appartenenza e operazioni base; Livello 2 = operazioni composte; Livello 3 = problemi con 3 insiemi
- [ ] #5 Le spiegazioni usano notazione formale corretta
- [ ] #6 Test pytest verifica generazione senza errori
- [ ] #7 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stato ASSENTE a IMPLEMENTATO per notazione insiemistica in sezione 2.5, spuntare R5, aggiungere riga al Registro Modifiche
<!-- AC:END -->

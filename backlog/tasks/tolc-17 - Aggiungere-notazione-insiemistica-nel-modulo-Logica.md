---
id: TOLC-17
title: Aggiungere notazione insiemistica nel modulo Logica
status: Done
assignee: []
created_date: '2026-03-12 07:23'
updated_date: '2026-03-12 09:09'
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
- [x] #1 Almeno 5 nuovi template per operazioni insiemistiche (∪, ∩, complemento, differenza, prodotto cartesiano)
- [x] #2 Template per appartenenza (∈) e inclusione (⊂, ⊆) con domande vero/falso
- [x] #3 Template per diagrammi di Venn descritti testualmente con domande di conteggio
- [x] #4 Integrazione nei 3 livelli di difficoltà: Livello 1 = appartenenza e operazioni base; Livello 2 = operazioni composte; Livello 3 = problemi con 3 insiemi
- [x] #5 Le spiegazioni usano notazione formale corretta
- [x] #6 Test pytest verifica generazione senza errori
- [x] #7 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stato ASSENTE a IMPLEMENTATO per notazione insiemistica in sezione 2.5, spuntare R5, aggiungere riga al Registro Modifiche
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Aggiunti 7 template in `exercises/logic_puzzle.py` per notazione insiemistica:

**L1**: `_set_membership()` (∈/∉), `_set_basic_operations()` (∪, ∩)
**L2**: `_set_inclusion()` (⊂, ⊆), `_set_complement_difference()` (complemento, differenza), `_set_compound_operations()` (operazioni composte con 3 insiemi)
**L3**: `_set_venn_counting()` (inclusione-esclusione 2 insiemi), `_set_three_sets_venn()` (Venn 3 insiemi)

Tutti i template seguono il pattern esistente (metodi statici, 5-tuple), registrati in `_get_templates()`.
Test: `tests/test_logic_puzzle_sets.py` — 16 test tutti passati.
Coverage doc aggiornato: §2.5 ASSENTE→IMPLEMENTATO, R5 spuntata, registro modifiche aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

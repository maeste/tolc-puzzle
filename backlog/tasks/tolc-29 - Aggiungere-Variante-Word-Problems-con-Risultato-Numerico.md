---
id: TOLC-29
title: Aggiungere Variante Word Problems con Risultato Numerico
status: Done
assignee: []
created_date: '2026-03-12 10:37'
updated_date: '2026-03-12 11:13'
labels:
  - gap-coverage
  - enhancement
  - word-problems
milestone: m-0
dependencies: []
references:
  - exercises/word_modeler.py
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Aggiungere variante in `exercises/word_modeler.py` che chieda il risultato numerico finale (come nel TOLC-B reale) oltre alla traduzione in equazione.

Nel TOLC-B reale i word problem chiedono spesso direttamente "Quanti sono?" o "Qual è il valore?" — non solo la formulazione dell'equazione.

**Implementation Plan**:
1. Aggiungere modalità "risultato numerico" in `exercises/word_modeler.py`
2. Creare almeno 5 template con risposta numerica diretta
3. Mantenere compatibilità con modalità esistente (traduzione in equazione)
4. Scrivere test pytest dedicati
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Almeno 5 template con risposta numerica diretta
- [x] #2 Modalità compatibile con quella esistente (traduzione in equazione)
- [x] #3 Test pytest che verifichino generazione e correttezza risposte numeriche
- [x] #4 Nessuna regressione sui test esistenti
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added 8 numeric-result word problem templates to `exercises/word_modeler.py`:

- **Level 1** (3): age+sum, percentage discount, percentage of group
- **Level 2** (3): mean with added value, combined work rate, profit/markup
- **Level 3** (2): system of equations (ages), combined distance (travelers)

`generate()` randomly mixes equation and numeric templates via refactored `_get_templates()` merging `_get_equation_templates()` + `_get_numeric_templates()`. Full backward compatibility. `_numeric_distractors` helper generates plausible wrong answers. Tests in `tests/test_word_modeler_numeric.py`. All 442 project tests pass.
<!-- SECTION:FINAL_SUMMARY:END -->

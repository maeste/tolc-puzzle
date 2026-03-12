---
id: TOLC-21
title: Migliorare contestualizzazione word problems
status: Done
assignee: []
created_date: '2026-03-12 07:23'
updated_date: '2026-03-12 09:19'
labels:
  - enhancement
  - ux
  - matematica
milestone: m-0
dependencies: []
references:
  - exercises/word_modeler.py
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
I word problem nel Word Modeler (tipo B) usano contesti generici (serbatoi, miscele, investimenti). Il TOLC-B reale tende a usare contesti più quotidiani e realistici. Migliorare la varietà e il realismo dei contesti per avvicinarsi al formato dell'esame.

**Cosa implementare**:
- Rivedere i template esistenti in `exercises/word_modeler.py` per aggiungere varianti di contesto più realistiche
- Aggiungere contesti: spesa al supermercato, viaggi, abbonamenti, bollette, ricette di cucina, sport
- Mantenere la stessa struttura matematica ma variare i "vestiti" del problema
- Assicurarsi che i contesti siano culturalmente appropriati per studenti italiani

**File di riferimento**: `exercises/word_modeler.py`, `claudedocs/tolc-b-coverage-analysis.md`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Almeno 6 nuovi contesti realistici aggiunti ai template esistenti (es. spesa, viaggi, abbonamenti, sport, cucina, bollette)
- [x] #2 I contesti sono culturalmente appropriati per studenti italiani (prezzi in euro, riferimenti locali)
- [x] #3 La struttura matematica sottostante rimane invariata — cambiano solo i 'vestiti' del problema
- [x] #4 Ogni livello di difficoltà ha almeno 2 contesti nuovi
- [x] #5 I testi sono grammaticalmente corretti in italiano
- [x] #6 Test pytest verifica che i nuovi contesti generano correttamente
- [x] #7 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: spuntare R9 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Aggiunti 8 template in `exercises/word_modeler.py` con contesti realistici italiani:\n- L1: `_supermarket_shopping()`, `_phone_plan()`, `_cooking_recipe()`\n- L2: `_train_tickets()`, `_sports_training()`, `_electricity_bill()`\n- L3: `_travel_planning()`, `_shared_apartment()`\nTutti seguono il pattern 5-tupla standard e sono registrati in `_get_templates()`. Test: `tests/test_word_modeler_contexts.py` (89 test, tutti passati).
<!-- SECTION:FINAL_SUMMARY:END -->

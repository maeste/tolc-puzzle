---
id: TOLC-16
title: Aggiungere iniettività e invertibilità funzioni
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
  - exercises/graph_reader.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Il modulo Graph Reader (tipo C) copre riconoscimento famiglie, trasformazioni, dominio e segno, ma manca di esercizi su iniettività (test della retta orizzontale), suriettività e invertibilità delle funzioni — argomenti presenti nel syllabus TOLC-B.

**Cosa implementare**: Nuovi template in `exercises/graph_reader.py` che, dato un grafico di funzione (descritto parametricamente), chiedano:
- "Questa funzione è iniettiva?" (con spiegazione test retta orizzontale)
- "Questa funzione è invertibile?" (iniettiva + dominio/codominio)
- "Qual è il codominio/immagine di f?"
- "Per quali intervalli f è iniettiva?"

**File di riferimento**: `exercises/graph_reader.py`, `claudedocs/tolc-b-coverage-analysis.md`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Almeno 4 nuovi template in graph_reader.py per iniettività, suriettività e invertibilità
- [x] #2 Template 'iniettività': dato grafico, determinare se la funzione è iniettiva con spiegazione del test della retta orizzontale
- [x] #3 Template 'invertibilità': determinare se la funzione è invertibile e perché
- [x] #4 Template 'intervalli di iniettività': identificare su quali intervalli una funzione non iniettiva lo diventa
- [x] #5 Le spiegazioni includono definizioni formali e criterio grafico
- [x] #6 Test pytest verifica generazione corretta dei nuovi template
- [x] #7 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stati ASSENTE a IMPLEMENTATO per iniettività/invertibilità in sezione 2.2, spuntare R4 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Aggiunti 4 template in `exercises/graph_reader.py` per iniettività, invertibilità e codominio:

1. **`_template_injectivity()`**: dato un grafico, chiede se la funzione è iniettiva. Spiegazione con test della retta orizzontale. 9 famiglie di funzioni classificate.
2. **`_template_invertibility()`**: chiede se la funzione è invertibile (biiezione). Spiega condizioni e restrizione dominio.
3. **`_template_codomain()`**: chiede l'immagine di f. 6 varianti (lineare, quadratica a>0/a<0, esponenziale a>0/a<0, radice).
4. **`_template_injectivity_intervals()`**: per funzioni non iniettive, chiede su quali intervalli lo diventano.

Template integrati in `generate()`: iniettività/invertibilità/codominio a L2+, intervalli a L3.
Test: `tests/test_graph_reader_injectivity.py` — 22 test tutti passati.
Coverage doc aggiornato: §2.2 ASSENTE→IMPLEMENTATO, R4 spuntata, registro modifiche aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

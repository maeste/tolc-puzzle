---
id: TOLC-16
title: Aggiungere iniettività e invertibilità funzioni
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
- [ ] #1 Almeno 4 nuovi template in graph_reader.py per iniettività, suriettività e invertibilità
- [ ] #2 Template 'iniettività': dato grafico, determinare se la funzione è iniettiva con spiegazione del test della retta orizzontale
- [ ] #3 Template 'invertibilità': determinare se la funzione è invertibile e perché
- [ ] #4 Template 'intervalli di iniettività': identificare su quali intervalli una funzione non iniettiva lo diventa
- [ ] #5 Le spiegazioni includono definizioni formali e criterio grafico
- [ ] #6 Test pytest verifica generazione corretta dei nuovi template
- [ ] #7 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stati ASSENTE a IMPLEMENTATO per iniettività/invertibilità in sezione 2.2, spuntare R4 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

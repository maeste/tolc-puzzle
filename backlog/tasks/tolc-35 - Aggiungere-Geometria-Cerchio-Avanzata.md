---
id: TOLC-35
title: Aggiungere Geometria Cerchio Avanzata
status: Done
assignee: []
created_date: '2026-03-12 11:47'
updated_date: '2026-03-13 06:37'
labels:
  - gap-medio
  - estensione-modulo
milestone: TOLC-B Competenze Cognitive v3
dependencies: []
references:
  - exercises/geometry_sherlock.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contesto

~5% delle domande reali TOLC-B riguardano proprietà avanzate del cerchio: tangente da punto esterno, angolo inscritto, arco-corda. Sono domande di alta difficoltà. Riferimento: Q5, Q15 Alpha Test.

## Problema

GeometrySherlock copre triangoli, quadrilateri e cerchi base ma manca la geometria cerchio avanzata (tangente esterna, teoremi angoli, potenza di un punto).

## Implementation Plan

1. **Estendere GeometrySherlock con ~4 template**:
   - **Tangente da punto esterno**: dato punto P esterno al cerchio, calcolare lunghezza tangente (Pitagora con raggio e distanza centro-punto)
   - **Angolo inscritto**: relazione angolo inscritto = metà angolo al centro, dato uno trovare l'altro
   - **Arco-corda-angolo al centro**: relazioni tra corda, arco sotteso e angolo al centro
   - **Potenza di un punto**: PA·PB = PC·PD per secanti, o PA² per tangente

2. **SVG**: Cerchio con tangente, angoli evidenziati, archi colorati
3. **Spiegazione**: Enunciare il teorema usato e mostrare applicazione
4. **Distrattori**: Basati su confusione angolo inscritto/al centro, errori Pitagora

### File da modificare
- `exercises/geometry_sherlock.py` — aggiungere template cerchio avanzato
- `claudedocs/tolc-b-coverage-analysis.md`

### Complessità stimata
Media: geometria classica con formule note, SVG da generare con cura.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Almeno 4 template: tangente da punto esterno - angolo inscritto - arco-corda-angolo al centro - potenza di un punto
- [x] #2 SVG con cerchio - tangente - angoli evidenziati - archi colorati
- [x] #3 Spiegazione che enuncia il teorema usato e mostra l'applicazione
- [x] #4 Distrattori basati su errori comuni (confusione angolo inscritto/al centro)
- [x] #5 Aggiornare claudedocs/tolc-b-coverage-analysis.md con nuovi template e stato IMPLEMENTATO
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Aggiunti 4 template cerchio avanzato a GeometrySherlock: angolo inscritto, distanza corda, lunghezza arco, potenza di un punto. SVG con archi colorati e angoli evidenziati. 26 test passano. Coverage doc aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

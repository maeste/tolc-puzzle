---
id: TOLC-36
title: Aggiungere Domande Cross-Topic nella Simulazione Esame
status: Done
assignee: []
created_date: '2026-03-12 11:47'
updated_date: '2026-03-13 06:37'
labels:
  - gap-medio
  - simulazione-esame
  - competenza-cognitiva
milestone: TOLC-B Competenze Cognitive v3
dependencies: []
references:
  - app.py
  - static/js/realistic_exam.js
  - claudedocs/tolc-b-coverage-analysis.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contesto

~15% delle domande reali TOLC-B mescolano 2+ aree tematiche in una singola domanda (es: geometria+trigonometria, algebra+geometria analitica). La nostra simulazione genera solo domande mono-topic. Riferimento: Q4, Q5, Q14 Alpha Test.

## Problema

Il TOLC testa CONNESSIONI tra argomenti. Lo studente che studia i singoli topic separatamente non è preparato per domande che richiedono competenze trasversali.

## Implementation Plan

1. **Modificare il generatore di simulazione** per includere 2-3 domande "ibride" su 20:
   - **Algebra + Geometria analitica**: es. intersezione parabola con assi (richiede equazione quadratica + piano cartesiano)
   - **Geometria + Trigonometria**: es. cerchio con tangente e angolo (richiede teoremi cerchio + funzioni trig)
   - **Funzioni + Geometria**: es. area sotto curva stimata con trapezi (richiede lettura grafico + calcolo area)
   - **Probabilità + Combinatoria**: es. probabilità con disposizioni (richiede conteggio + calcolo prob)

2. **Approccio**: Template dedicati cross-topic OPPURE composizione intelligente di template esistenti
3. **Integrazione simulazione**: La simulazione include 2-3 domande cross-topic su 20 totali
4. **Distrattori**: Errori che derivano dal non collegare i due topic

### File da modificare
- `app.py` — logica selezione domande simulazione
- `static/js/realistic_exam.js` — se necessario per rendering
- Eventuale nuovo file `exercises/cross_topic.py`
- `claudedocs/tolc-b-coverage-analysis.md`

### Complessità stimata
Alta: richiede design di template che combinano sensatamente due aree e integrazione nel flusso simulazione.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Almeno 4 template cross-topic: algebra+geometria analitica - geometria+trigonometria - funzioni+geometria - probabilità+combinatoria
- [x] #2 La simulazione esame include 2-3 domande cross-topic su 20 totali
- [x] #3 Ogni domanda cross-topic richiede competenze da almeno 2 aree tematiche distinte
- [x] #4 Distrattori che derivano dal non collegare correttamente i due topic
- [x] #5 Spiegazione che evidenzia il collegamento tra le aree
- [x] #6 Aggiornare claudedocs/tolc-b-coverage-analysis.md con nuovi template e stato IMPLEMENTATO
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Creato `exercises/cross_topic.py` con 5 template cross-topic su 3 livelli. 2 domande su 20 nella simulazione. Ogni domanda richiede competenze da 2 aree distinte. Spiegazioni evidenziano il collegamento. 34 test passano. Coverage doc aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

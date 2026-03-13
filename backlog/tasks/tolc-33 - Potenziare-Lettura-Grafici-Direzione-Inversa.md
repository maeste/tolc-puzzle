---
id: TOLC-33
title: Potenziare Lettura Grafici (Direzione Inversa)
status: Done
assignee: []
created_date: '2026-03-12 11:46'
updated_date: '2026-03-13 06:37'
labels:
  - gap-critico
  - estensione-modulo
  - competenza-cognitiva
milestone: TOLC-B Competenze Cognitive v3
dependencies: []
references:
  - exercises/graph_reader.py
  - app.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contesto

L'attuale GraphReader chiede "quale grafico corrisponde a questa funzione?" — il TOLC chiede il contrario: "dato questo grafico, rispondi a questa domanda specifica". Competenza chiave nel syllabus CISIA "Funzioni e Grafici". Riferimento: Q18 Alpha Test.

## Problema

La direzione cognitiva è invertita. Lo studente deve saper LEGGERE un grafico e dedurre proprietà, non solo RICONOSCERE il grafico giusto.

## Implementation Plan

1. **Estendere GraphReader con ~6 template "dato il grafico, rispondi"**:
   - **Preimmagini**: "Trovare tutti gli a tali che f(3)=f(a)" — dato il grafico, identificare i punti con la stessa ordinata
   - **Segno**: "In quale intervallo f(x)<0?" — leggere dove il grafico è sotto l'asse x
   - **Crescenza/Decrescenza**: "In quale intervallo f è crescente?" — identificare tratti crescenti
   - **Max/Min**: "Qual è il massimo di f nell'intervallo [a,b]?" — leggere dal grafico
   - **Dominio/Codominio**: "Qual è il codominio di f?" — dedurre dal grafico
   - **Intersezioni**: "Quante soluzioni ha f(x)=k?" — contare intersezioni con retta orizzontale

2. **Il grafico è DATO** (generato come SVG con funzione nota internamente), la domanda è SULLA funzione
3. **SVG**: Generare grafici chiari con griglia, assi, punti notevoli evidenziati
4. **Opzioni**: 5 risposte plausibili basate su errori di lettura comuni

### File da modificare
- `exercises/graph_reader.py` — aggiungere template inversi
- `app.py` — se necessario aggiornare routing
- `claudedocs/tolc-b-coverage-analysis.md`

### Complessità stimata
Media-alta: richiede generazione SVG di grafici con proprietà note e formulazione domande coerenti.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Almeno 6 template inversi: preimmagini - segno - crescenza - max/min - dominio/codominio - intersezioni con retta
- [x] #2 Il grafico è generato come SVG e la domanda chiede di dedurre proprietà DAL grafico
- [x] #3 SVG con griglia - assi numerati - punti notevoli visibili
- [x] #4 5 opzioni di risposta con distrattori basati su errori comuni di lettura grafico
- [x] #5 Risposte verificabili internamente (la funzione è nota al generatore)
- [x] #6 Aggiornare claudedocs/tolc-b-coverage-analysis.md con nuovi template e stato IMPLEMENTATO
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Aggiunti 6 template inversi a GraphReader: preimmagini, segno, crescenza, max/min, codominio, intersezioni. SVG con linea tratteggiata y=k per intersezioni. Probabilità selezione 35%→45%. 33 test passano. Coverage doc aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

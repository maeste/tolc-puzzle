---
id: TOLC-31
title: Aggiungere Esercizi di Semplificazione Espressioni
status: Done
assignee: []
created_date: '2026-03-12 11:46'
updated_date: '2026-03-12 15:52'
labels:
  - gap-critico
  - nuovo-tipo-esercizio
  - competenza-cognitiva
milestone: TOLC-B Competenze Cognitive v3
dependencies: []
references:
  - exercises/solve_exercise.py
  - app.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contesto

Dall'analisi critica delle 20 domande Alpha Test reali, ~30% sono domande di tipo "L'espressione X è uguale a: A)... B)... C)... D)... E)..." — un formato cognitivo completamente assente dalla nostra app. Questo è il gap singolo più grande.

## Problema

L'app genera domande "risolvi/calcola" ma il TOLC chiede "semplifica e identifica l'equivalente". Lo studente deve manipolare espressioni, non risolvere equazioni. Riferimento: Q1 (log), Q3 (prodotti notevoli/cubo), Q7 (radicali nested), Q9 (frazioni algebriche), Q10 (raccoglimento), Q17 (esponenti negativi).

## Implementation Plan

### Nuovo modulo o estensione di SolveExercise

1. **Creare ~10 template su 3 livelli di difficoltà**:
   - **Facile**: semplificazione potenze/esponenti negativi (es: (2⁻¹+2⁻²)/(2⁻³-2⁻⁴)), raccoglimento fattore comune (es: 10⁹+10⁸+10⁹)
   - **Medio**: logaritmi (es: log₁₀60/log₁₀√10), prodotti notevoli/fattorizzazione (es: (2ab-b²-a²)·(b-a))
   - **Difficile**: radicali nested (es: √((√(a²+4)-2)(√(a²+4)+2))), frazioni algebriche composte (es: (a/b+c/d)/(b/d+a/c))

2. **Formato output**: "L'espressione X è uguale a:" con 5 opzioni
3. **Distrattori**: basati su errori comuni di semplificazione (segno sbagliato, esponente errato, fattorizzazione incompleta)
4. **Spiegazione**: mostrare i passaggi di semplificazione step-by-step

### File da modificare
- `exercises/solve_exercise.py` — aggiungere template semplificazione o creare nuovo modulo
- `app.py` — registrare nuovo tipo se modulo separato
- `claudedocs/tolc-b-coverage-analysis.md` — aggiornare copertura

### Complessità stimata
Media-alta: richiede generazione parametrica di espressioni equivalenti e calcolo simbolico per verificare correttezza.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Genera almeno 10 template di semplificazione su 3 livelli (facile/medio/difficile)
- [x] #2 Formato output: 'L'espressione X è uguale a:' con 5 opzioni
- [x] #3 Sotto-tipi coperti: logaritmi - radicali - potenze negative - frazioni algebriche - prodotti notevoli - raccoglimento
- [x] #4 Distrattori basati su errori comuni di semplificazione (non casuali)
- [x] #5 Spiegazione step-by-step dei passaggi di semplificazione
- [x] #6 Aggiornare claudedocs/tolc-b-coverage-analysis.md con nuovi template e stato IMPLEMENTATO
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Creato `exercises/simplification.py` con 10 template su 3 livelli. Formato "L'espressione X è uguale a:" con distrattori basati su errori comuni. Registrato in app.py come tipo "simplification", aggiunto a REALISTIC_EXAM_WEIGHTS (1 domanda su 20). 43 test passano. Coverage doc aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

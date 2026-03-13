---
id: TOLC-34
title: Aggiungere Ragionamento Proporzionale e Variazione Parametri
status: Done
assignee: []
created_date: '2026-03-12 11:47'
updated_date: '2026-03-12 15:52'
labels:
  - gap-critico
  - nuovo-tipo-esercizio
  - competenza-cognitiva
milestone: TOLC-B Competenze Cognitive v3
dependencies: []
references:
  - exercises/word_modeler.py
  - exercises/solve_exercise.py
  - app.py
  - claudedocs/tolc-b-coverage-analysis.md
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Contesto

~5-10% delle domande reali TOLC chiedono ragionamento proporzionale: "Se a=f(b,c) e raddoppi b, cosa succede a c per mantenere a costante?". Competenza trasversale "Modellizzare e risolvere" del syllabus CISIA. Riferimento: Q12 Alpha Test.

## Problema

L'app non genera domande dove lo studente deve ragionare su come cambiano le variabili in una relazione funzionale. Questo tipo di domanda non richiede calcolo ma comprensione delle dipendenze.

## Implementation Plan

1. **Creare ~5 template** (estensione di WordModeler o SolveExercise):
   - **Proporzionalità diretta**: "Se y=kx e x triplica, y..." → triplica
   - **Proporzionalità inversa**: "Se a=k/b² e b raddoppia, a..." → diventa 1/4
   - **Variazione parametri in formula**: "Se V=πr²h e r raddoppia, di quanto devi ridurre h per mantenere V?" → h diventa 1/4
   - **Percentuali composte**: "Se il prezzo aumenta del 20% e poi del 10%, di quanto è aumentato in totale?" → 32%
   - **Dipendenza funzionale**: "Se a=2b/c², raddoppi b, cosa fai a c per mantenere a costante?" → c·√2

2. **Formato**: Domanda testuale con formula, risposta numerica o qualitativa ("raddoppia"/"dimezza"/"resta uguale"/valore specifico)
3. **Spiegazione**: Mostrare il ragionamento proporzionale step-by-step
4. **Generazione parametrica**: Variare coefficienti, esponenti e tipo di variazione

### File da modificare
- `exercises/word_modeler.py` o `exercises/solve_exercise.py`
- `app.py`
- `claudedocs/tolc-b-coverage-analysis.md`

### Complessità stimata
Media: template relativamente semplici, la sfida è nella chiarezza delle spiegazioni.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Almeno 5 template: proporzionalità diretta - inversa - variazione parametri - percentuali composte - dipendenza funzionale
- [x] #2 Formato domanda con formula e variazione di un parametro
- [x] #3 Risposte sia numeriche che qualitative (raddoppia/dimezza/valore specifico)
- [x] #4 Spiegazione step-by-step del ragionamento proporzionale
- [x] #5 Generazione parametrica con variazione di coefficienti ed esponenti
- [x] #6 Aggiornare claudedocs/tolc-b-coverage-analysis.md con nuovi template e stato IMPLEMENTATO
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Creato `exercises/proportional_reasoning.py` con 6 template su 3 livelli. Formule fisiche/geometriche reali (area cerchio, volume cilindro, energia cinetica). Risposte qualitative e numeriche. Registrato in app.py come tipo "proportional", aggiunto a REALISTIC_EXAM_WEIGHTS (1 domanda su 20). 13 test passano. Coverage doc aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

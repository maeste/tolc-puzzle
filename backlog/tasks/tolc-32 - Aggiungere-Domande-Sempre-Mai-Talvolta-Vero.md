---
id: TOLC-32
title: Aggiungere Domande Sempre/Mai/Talvolta Vero
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

~10% delle domande reali TOLC-B sono di ragionamento teorico: "È vero che X, comunque scelti a e b?" con opzioni che specificano condizioni. Questo formato costruisce pensiero critico e capacità di costruire/invalidare controesempi — completamente assente dalla nostra app.

## Problema

L'app non genera MAI domande dove la risposta è "sempre vero", "mai vero", "vero solo se a>0", ecc. Lo studente non viene allenato a ragionare sulle proprietà matematiche. Riferimento: Q11 Alpha Test (a/b + b/a ≥ 2).

## Implementation Plan

1. **Creare ~6 template parametrici**:
   - Disuguaglianza AM-GM: a/b + b/a ≥ 2 (vero per a,b concordi)
   - Proprietà potenze: (a+b)² = a²+b² (mai vero se ab≠0)
   - Modulo: |a+b| = |a|+|b| (vero sse ab≥0)
   - Divisibilità: se a|bc allora a|b o a|c (falso in generale)
   - Frazioni: a/(b+c) = a/b + a/c (mai vero)
   - Radici: √(a²+b²) = a+b (mai vero se a,b>0)

2. **Formato**: Affermazione + "È sempre vera / Vera solo se [condizione] / Mai vera / Nessuna delle precedenti"
3. **Spiegazione**: Quando falso, fornire controesempio esplicito. Quando vero, fornire dimostrazione breve.
4. **Generazione parametrica**: Variare i valori e le espressioni mantenendo la struttura logica

### File da modificare
- Nuovo modulo o estensione di `exercises/solve_exercise.py`
- `app.py` — registrare tipo
- `claudedocs/tolc-b-coverage-analysis.md`

### Complessità stimata
Media: i template sono relativamente fissi, la sfida è nella generazione di varianti e spiegazioni.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Genera almeno 6 template: AM-GM - proprietà potenze - modulo - divisibilità - frazioni - radici
- [x] #2 Formato: affermazione + opzioni Sempre/Con condizione/Mai/Nessuna delle precedenti
- [x] #3 Quando la risposta è 'falso' la spiegazione include un controesempio numerico esplicito
- [x] #4 Quando la risposta è 'vero' la spiegazione include una dimostrazione o giustificazione breve
- [x] #5 Varianti parametriche per evitare ripetizioni
- [x] #6 Aggiornare claudedocs/tolc-b-coverage-analysis.md con nuovi template e stato IMPLEMENTATO
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Creato `exercises/always_true.py` con 8 template su 3 livelli. Formato "Sempre/Mai/Talvolta vero" con controesempi numerici espliciti e dimostrazioni brevi. Registrato in app.py come tipo "always_true", aggiunto a REALISTIC_EXAM_WEIGHTS (1 domanda su 20). 40 test passano. Coverage doc aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Test automatizzati passano (pytest)
- [x] #2 Coverage doc aggiornato (claudedocs/tolc-b-coverage-analysis.md)
- [x] #3 Esercizi generati correttamente con distrattori sensati
- [x] #4 Integrato nella simulazione esame se applicabile
<!-- DOD:END -->

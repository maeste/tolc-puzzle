---
id: TOLC-14
title: Aggiungere modulo Disequazioni
status: Done
assignee:
  - claude
created_date: '2026-03-12 07:22'
updated_date: '2026-03-12 08:10'
labels:
  - syllabus-gap
  - enhancement
  - matematica
milestone: m-0
dependencies: []
references:
  - exercises/solve_exercise.py
  - app.py
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Il modulo Solve Exercise (tipo H) ha solo disequazioni basilari (ax + b > c). Il syllabus TOLC-B richiede disequazioni di 1° grado complete, 2° grado e razionali con studio del segno. Serve estendere Solve Exercise o creare un modulo dedicato.

**Contesto tecnico**: `exercises/solve_exercise.py` contiene già il pattern per equazioni/disequazioni. I template sono organizzati per livello di difficoltà. Ogni template genera question, options (4 scelte), correct_index, explanation. Seguire il pattern esistente.

**Argomenti da coprire**:
- Disequazioni 1° grado: forma completa con frazioni e parentesi
- Disequazioni 2° grado: ax²+bx+c > 0, ≥ 0, < 0, ≤ 0 (con discriminante positivo, zero, negativo)
- Disequazioni razionali: P(x)/Q(x) > 0 con studio del segno
- Sistemi di disequazioni (livello 3)

**File di riferimento**: `exercises/solve_exercise.py`, `app.py`, `claudedocs/tolc-b-coverage-analysis.md`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Disequazioni 1° grado con frazioni e parentesi (non solo ax+b>c)
- [x] #2 Disequazioni 2° grado: ax²+bx+c con tutti e 4 i segni di confronto, gestione dei 3 casi di discriminante
- [x] #3 Disequazioni razionali con studio del segno (almeno numeratore e denominatore di 1° grado)
- [x] #4 Livello 1: disequazioni 1° grado complete; Livello 2: disequazioni 2° grado; Livello 3: razionali e sistemi
- [x] #5 Le spiegazioni mostrano il procedimento di risoluzione passo-passo
- [x] #6 Le risposte usano notazione intervallare corretta (es. x ∈ (-∞, 3) ∪ (5, +∞))
- [x] #7 Almeno 6 nuovi template parametrici
- [x] #8 Test pytest che verifica generazione corretta per tutti i livelli
- [x] #9 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stati ASSENTE/PARZIALE a IMPLEMENTATO per disequazioni in sezione 2.1, spuntare R2 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Nuovo file `exercises/inequalities.py` con classe `InequalitiesExercise(Exercise)`\n2. L1 (2 template): disequazioni 1° grado con frazioni/parentesi\n3. L2 (2 template): disequazioni 2° grado (delta>0, delta=0, delta<0, tutti i segni)\n4. L3 (2 template): disequazioni razionali con studio del segno, sistemi\n5. Risposte in notazione intervallare, spiegazioni passo-passo\n6. Registrare in `app.py` come tipo `inequalities`\n7. Test pytest in `tests/test_inequalities.py`\n8. Aggiornare `claudedocs/tolc-b-coverage-analysis.md` sezione 2.1, R2, Registro Modifiche
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Creato `exercises/inequalities.py` con classe `InequalitiesExercise(Exercise)` — 7 template su 3 livelli:\n- L1: disequazioni 1° grado con frazioni e parentesi (2 template)\n- L2: disequazioni 2° grado con gestione Δ>0, Δ=0, Δ<0 e tutti i segni di confronto (3 template)\n- L3: disequazioni razionali con studio del segno, sistemi di disequazioni (2 template)\n\nRisposte in notazione intervallare (∈, ∪, ∞). Spiegazioni passo-passo. Registrato in `app.py` come tipo `inequalities`. Test in `tests/test_inequalities.py` (6 test, tutti verdi). Coverage doc aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

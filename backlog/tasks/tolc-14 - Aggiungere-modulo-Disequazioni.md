---
id: TOLC-14
title: Aggiungere modulo Disequazioni
status: To Do
assignee: []
created_date: '2026-03-12 07:22'
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
- [ ] #1 Disequazioni 1° grado con frazioni e parentesi (non solo ax+b>c)
- [ ] #2 Disequazioni 2° grado: ax²+bx+c con tutti e 4 i segni di confronto, gestione dei 3 casi di discriminante
- [ ] #3 Disequazioni razionali con studio del segno (almeno numeratore e denominatore di 1° grado)
- [ ] #4 Livello 1: disequazioni 1° grado complete; Livello 2: disequazioni 2° grado; Livello 3: razionali e sistemi
- [ ] #5 Le spiegazioni mostrano il procedimento di risoluzione passo-passo
- [ ] #6 Le risposte usano notazione intervallare corretta (es. x ∈ (-∞, 3) ∪ (5, +∞))
- [ ] #7 Almeno 6 nuovi template parametrici
- [ ] #8 Test pytest che verifica generazione corretta per tutti i livelli
- [ ] #9 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: cambiare stati ASSENTE/PARZIALE a IMPLEMENTATO per disequazioni in sezione 2.1, spuntare R2 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

---
id: TOLC-23
title: Aggiungere Trigonometria
status: Done
assignee: []
created_date: '2026-03-12 10:36'
updated_date: '2026-03-12 10:45'
labels:
  - gap-coverage
  - new-exercise-type
  - trigonometry
milestone: m-0
dependencies: []
references:
  - exercises/solve_exercise.py
  - app.py
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Aggiungere template per esercizi di trigonometria in `exercises/solve_exercise.py`:
- Valori notevoli sin/cos/tan (30°, 45°, 60°, 90°, etc.)
- Equazioni trigonometriche base (sin(x)=k, cos(x)=k, tan(x)=k)
- Identità fondamentale sin²(x)+cos²(x)=1 e sue varianti

La trigonometria è un argomento frequente nel TOLC-B reale e attualmente non coperto dall'app.

**Implementation Plan**:
1. Aggiungere classe/sezione trigonometria in `exercises/solve_exercise.py`
2. Creare 5-7 template con 3 livelli di difficoltà (easy, medium, hard)
3. Registrare il nuovo tipo in `app.py` per inclusione nella simulazione
4. Scrivere test pytest dedicati
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 5-7 template di trigonometria implementati (valori notevoli, equazioni base, identità)
- [x] #2 3 livelli di difficoltà (easy, medium, hard)
- [x] #3 Test pytest che verifichino generazione e correttezza soluzioni
- [x] #4 Registrazione in app.py per inclusione nella simulazione esame
- [x] #5 Nessuna regressione sui test esistenti
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Piano Implementazione TOLC-23: Trigonometria

### Template da creare (7 totali, 3 livelli):

**Level 1 (Easy) - 2 template:**
1. `_t1_trig_notable_values()` - Valori notevoli: "Quanto vale sin(30°)?" / cos(60°) / tan(45°) etc.
2. `_t1_trig_basic_identity()` - Identità base: "Se sin(α) = 3/5, quanto vale cos(α)?" usando sin²+cos²=1

**Level 2 (Medium) - 3 template:**
3. `_t2_trig_equation_simple()` - Eq. trig base: "Risolvi sin(x) = 1/2 nell'intervallo [0°, 360°]. Quante soluzioni ci sono?"
4. `_t2_trig_expression()` - Espressioni: "Calcola sin²(30°) + cos²(30°)" / "sin(60°) · cos(30°) + cos(60°) · sin(30°)"
5. `_t2_trig_convert_deg_rad()` - Conversione gradi/radianti: "Converti 120° in radianti"

**Level 3 (Hard) - 2 template:**
6. `_t3_trig_equation_complex()` - Eq. trig parametriche: "Per quali valori di k l'equazione sin(x)=k ha soluzione?"
7. `_t3_trig_identity_proof()` - Verifiche identità: "Semplifica (1-cos²x)/sin(x)"

### Registrazione:
- Aggiungere template ai registri `_NUMERIC_TEMPLATES_L1/L2/L3`
- Alcuni template L1 saranno 5-tuple (string) → `_STRING_TEMPLATES_L1`

### Test:
- File: `tests/test_solve_exercise_trig.py`
- Test per ogni template + integrazione generate()
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implementati 7 template di trigonometria in `exercises/solve_exercise.py`:

**Level 1 (2 template):**
- `_t1_trig_notable_values()` — valori notevoli sin/cos/tan (0°, 30°, 45°, 60°, 90°)
- `_t1_trig_basic_identity()` — identità sin²+cos²=1 con terne pitagoriche

**Level 2 (3 template):**
- `_t2_trig_equation_simple()` — numero soluzioni sin(x)=k in [0°, 360°)
- `_t2_trig_expression()` — espressioni con formule addizione/duplicazione
- `_t2_trig_convert_deg_rad()` — conversione gradi↔radianti

**Level 3 (2 template):**
- `_t3_trig_equation_parametric()` — codominio sin/cos, equazioni con parametro
- `_t3_trig_simplification()` — semplificazioni identità (1-cos²)/sin, tan·cos, etc.

Test: 20 test in `tests/test_solve_exercise_trig.py`, tutti passano.
Simulazione: aggiornata distribuzione in `app.py` (4 slot "solve" su 20).
Nessuna regressione: 216 test totali passano.
<!-- SECTION:FINAL_SUMMARY:END -->

---
id: TOLC-15
title: Riallineare Statistica al syllabus TOLC-B
status: Done
assignee:
  - claude
created_date: '2026-03-12 07:23'
updated_date: '2026-03-12 08:10'
labels:
  - syllabus-alignment
  - enhancement
  - matematica
milestone: m-0
dependencies: []
references:
  - exercises/statistics_exercise.py
  - app.py
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Il modulo Statistics Exercise (tipo I) include contenuti extra rispetto al syllabus TOLC-B (varianza, deviazione standard, quartili, percentili, outlier detection) e manca di esercizi sulla lettura/interpretazione di grafici statistici (istogrammi, grafici a torta), che è invece richiesta dal TOLC-B.

**Cosa fare**:
1. Aggiungere template per lettura grafici: dato un istogramma/grafico a torta (descritto testualmente o con dati tabellari), rispondere a domande di interpretazione
2. Contrassegnare nell'UI i contenuti extra (varianza, dev.std, quartili, percentili, outlier) come "Approfondimento" — NON rimuoverli
3. Riordinare i livelli: Livello 1 = media, mediana, moda + lettura grafici; Livello 2 = interpretazione dati + confronti; Livello 3 = approfondimenti (varianza, quartili etc.)

**File di riferimento**: `exercises/statistics_exercise.py`, `templates/` (per eventuale rendering grafico), `claudedocs/tolc-b-coverage-analysis.md`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Almeno 3 template per lettura/interpretazione grafici statistici (istogrammi, torta, barre) descritti con dati tabellari
- [x] #2 I contenuti extra (varianza, deviazione standard, quartili, percentili, outlier) sono contrassegnati come 'Approfondimento' nei metadata dell'esercizio
- [x] #3 Livello 1 copre media, mediana, moda e lettura grafici base
- [x] #4 Livello 2 copre interpretazione dati comparativa e frequenze relative
- [x] #5 Livello 3 contiene approfondimenti (varianza, quartili, etc.) chiaramente marcati
- [x] #6 Test pytest verifica generazione per tutti i livelli senza errori
- [x] #7 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: aggiornare sezione 2.7 con stati corretti, spuntare R3 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Aggiungere 3 nuovi template L1 per lettura grafici (istogramma, torta, barre) con dati tabellari\n2. Riorganizzare livelli: L1=media,mediana,moda+grafici; L2=media ponderata,frequenza relativa,media frequenza; L3=varianza,dev.std,quartili,CV,media combinata,trasformazione\n3. Aggiungere campo `approfondimento: True` nei dict restituiti dai template L3\n4. Test pytest in `tests/test_statistics.py`\n5. Aggiornare `claudedocs/tolc-b-coverage-analysis.md` sezione 2.7, R3, Registro Modifiche
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Modificato `exercises/statistics_exercise.py`:\n- Aggiunti 3 template lettura grafici in L1: istogramma, torta, barre (dati tabellari)\n- Riorganizzati livelli: L1=base+grafici (8 template), L2=interpretazione (3 template), L3=approfondimenti (7 template)\n- Varianza e dev.std spostati da L2 a L3\n- Aggiunto campo `approfondimento: True/False` nei dict restituiti da `generate()`\n\nTest in `tests/test_statistics.py` (2 test, tutti verdi). Coverage doc aggiornato.
<!-- SECTION:FINAL_SUMMARY:END -->

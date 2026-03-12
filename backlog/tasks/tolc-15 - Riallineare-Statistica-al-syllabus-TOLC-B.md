---
id: TOLC-15
title: Riallineare Statistica al syllabus TOLC-B
status: To Do
assignee: []
created_date: '2026-03-12 07:23'
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
- [ ] #1 Almeno 3 template per lettura/interpretazione grafici statistici (istogrammi, torta, barre) descritti con dati tabellari
- [ ] #2 I contenuti extra (varianza, deviazione standard, quartili, percentili, outlier) sono contrassegnati come 'Approfondimento' nei metadata dell'esercizio
- [ ] #3 Livello 1 copre media, mediana, moda e lettura grafici base
- [ ] #4 Livello 2 copre interpretazione dati comparativa e frequenze relative
- [ ] #5 Livello 3 contiene approfondimenti (varianza, quartili, etc.) chiaramente marcati
- [ ] #6 Test pytest verifica generazione per tutti i livelli senza errori
- [ ] #7 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: aggiornare sezione 2.7 con stati corretti, spuntare R3 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

---
id: TOLC-9
title: Mini-gioco Stima Flash (Tipo G)
status: Done
assignee: []
created_date: '2026-03-11 13:32'
updated_date: '2026-03-11 18:22'
labels: []
dependencies:
  - TOLC-2
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Espressione numerica, tempo limitato per scegliere ordine di grandezza corretto. Allena senso del numero e capacità di escludere risposte impossibili (strategia anti -0.25).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 exercises/estimation_blitz.py con almeno 15 template
- [x] #2 Espressioni: operazioni con interi, frazioni, potenze, radici, logaritmi
- [x] #3 Timer breve integrato (5-10 secondi per risposta)
- [x] #4 4 opzioni con ordini di grandezza diversi
- [x] #5 3 livelli: interi/frazioni -> potenze/radici -> espressioni miste con log
- [x] #6 Feedback: mostra la stima rapida corretta (es. circa 100 perché 99 circa 100 e sqrt(100) = 10)
<!-- AC:END -->

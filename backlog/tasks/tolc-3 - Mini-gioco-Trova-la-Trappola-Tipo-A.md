---
id: TOLC-3
title: Mini-gioco Trova la Trappola (Tipo A)
status: Done
assignee: []
created_date: '2026-03-11 13:31'
updated_date: '2026-03-11 13:50'
labels: []
dependencies:
  - TOLC-2
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Generatore di esercizi dove viene mostrato un calcolo svolto con un errore nascosto. La studentessa deve trovare il passaggio sbagliato. Allena attenzione ai dettagli e conoscenza regole base.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 exercises/trap_calculator.py con almeno 15 template di trappole
- [ ] #2 Trappole: sqrt(a^2)=|a|, precedenze operatori, potenze con segni negativi, percentuali composte, prodotti notevoli errati, frazioni con segni, proprietà logaritmi errate
- [ ] #3 Ogni esercizio mostra 3-5 passaggi di calcolo, uno è sbagliato
- [ ] #4 3 livelli: errore ovvio -> errore in step intermedio -> errore sottile multi-step
- [ ] #5 Feedback spiega QUALE regola è stata violata e PERCHÉ
<!-- AC:END -->

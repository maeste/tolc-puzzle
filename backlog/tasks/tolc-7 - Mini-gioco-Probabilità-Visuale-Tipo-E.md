---
id: TOLC-7
title: Mini-gioco Probabilità Visuale (Tipo E)
status: Done
assignee: []
created_date: '2026-03-11 13:31'
updated_date: '2026-03-11 15:48'
labels: []
dependencies:
  - TOLC-2
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Scenari con dadi/carte/urne, con possibilità di costruire diagrammi ad albero. Visualizzare lo spazio campionario previene errori di probabilità condizionata.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 exercises/probability_game.py con almeno 12 template
- [ ] #2 Scenari: dadi, carte, urne, estrazioni con/senza reinserimento
- [ ] #3 Pattern: P(A e B), P(A|B), almeno uno = 1-P(nessuno), eventi indipendenti
- [ ] #4 Diagramma ad albero visualizzato come SVG/HTML
- [ ] #5 3 livelli: 1 evento -> 2 eventi sequenziali -> condizionata
- [ ] #6 Feedback: mostra lo spazio campionario completo e dove si annida l'errore
<!-- AC:END -->

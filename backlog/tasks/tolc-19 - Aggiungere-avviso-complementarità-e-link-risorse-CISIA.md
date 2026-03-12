---
id: TOLC-19
title: Aggiungere avviso complementarità e link risorse CISIA
status: Done
assignee: []
created_date: '2026-03-12 07:23'
updated_date: '2026-03-12 09:19'
labels:
  - ux
  - informational
milestone: m-0
dependencies: []
references:
  - templates/index.html
  - static/css/style.css
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
L'app copre solo la sezione Matematica del TOLC-B. L'utente potrebbe non sapere che il TOLC-B include anche Biologia, Chimica e Fisica. Serve un avviso chiaro nell'interfaccia con link alle risorse ufficiali CISIA.

**Cosa implementare**:
- Banner o sezione nella dashboard (`templates/`) che spieghi: "Questo strumento copre la sezione Matematica del TOLC-B. Il TOLC-B include anche: Biologia, Chimica, Fisica e Comprensione del testo."
- Link alla pagina ufficiale CISIA per esercitazioni complete
- Opzionale: breve lista di cosa NON è coperto con suggerimenti di risorse

**File di riferimento**: `templates/index.html` o template dashboard, `static/`, `claudedocs/tolc-b-coverage-analysis.md`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Banner visibile nella dashboard principale che indica le sezioni TOLC-B non coperte (Biologia, Chimica, Fisica, Comprensione del testo)
- [x] #2 Link funzionante alla pagina ufficiale CISIA per esercitazioni
- [x] #3 Il banner è stilisticamente coerente con il resto dell'interfaccia
- [x] #4 Il banner è dismissibile (l'utente può chiuderlo) con persistenza in localStorage
- [x] #5 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: spuntare R7 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Aggiunto banner informativo dismissibile in `templates/dashboard.html` tra la sezione hero e la griglia esercizi. Il banner elenca le sezioni TOLC-B non coperte dall'app (Biologia, Chimica, Fisica, Comprensione del testo) con link al sito CISIA. Stili in `static/css/style.css` con gradiente azzurro, layout flexbox a pills, pulsante chiudi. Persistenza dismiss via localStorage key `tolcBannerDismissed`.
<!-- SECTION:FINAL_SUMMARY:END -->

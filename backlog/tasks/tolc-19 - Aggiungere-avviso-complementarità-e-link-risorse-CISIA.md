---
id: TOLC-19
title: Aggiungere avviso complementarità e link risorse CISIA
status: To Do
assignee: []
created_date: '2026-03-12 07:23'
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
- [ ] #1 Banner visibile nella dashboard principale che indica le sezioni TOLC-B non coperte (Biologia, Chimica, Fisica, Comprensione del testo)
- [ ] #2 Link funzionante alla pagina ufficiale CISIA per esercitazioni
- [ ] #3 Il banner è stilisticamente coerente con il resto dell'interfaccia
- [ ] #4 Il banner è dismissibile (l'utente può chiuderlo) con persistenza in localStorage
- [ ] #5 Aggiornare `claudedocs/tolc-b-coverage-analysis.md`: spuntare R7 in sezione 4, aggiungere riga al Registro Modifiche
<!-- AC:END -->

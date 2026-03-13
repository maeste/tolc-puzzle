# Analisi Critica di Copertura TOLC-B

> **Documento di tracciamento** — da aggiornare man mano che le lacune vengono risolte.
> Ultima revisione strutturale: 2026-03-13 (Assessment v4 — TOLC-43 post gap closure)

---

## 1. Panoramica

Il TOLC-B Puzzle copre **tutte le 9 macro-aree** del syllabus CISIA per la sezione Matematica del TOLC-B, per un totale di **57 argomenti** (di cui 4 EXTRA non richiesti dal syllabus base + 6 competenze cognitive trasversali). Tutte le lacune identificate sono state risolte. Implementazioni v4 (TOLC-38→42): Number Sense (12 template aritmetica pura), Which Satisfies (10 template meta-formato), combinatorica vincolata (4 template), word problems numerici TOLC-style (5 template), ribilanciamento pesi simulazione. Implementazioni v5 (TOLC-50→52): Function Composition (7 template composizione funzioni), Geometric Transformations (9 template trasformazioni geometriche), Estimation in Exam (stima inclusa in simulazione esame). **~191 template** distribuiti su **18 moduli**, **1804 test** automatizzati. Assessment v4 (§10): copertura domande reali 40q dal 67.5% al 87.5%.

### Legenda Stati

| Stato | Significato |
|-------|-------------|
| **COPERTO** | Argomento presente e allineato al syllabus |
| **PARZIALE** | Argomento presente ma incompleto o non allineato |
| **ASSENTE** | Argomento non presente, da implementare |
| **EXTRA** | Contenuto presente ma non richiesto dal syllabus TOLC-B |
| **IMPLEMENTATO** | Lacuna risolta (con data) |

---

## 2. Tabella di Copertura Syllabus

### 2.1 Algebra e Aritmetica

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Operazioni e precedenze | Trap Calculator (tipo A) | **COPERTO** | 19 template di trappole algebriche |
| Prodotti notevoli | Trap Calculator (tipo A) | **COPERTO** | (a+b)², (a-b)², a²-b² |
| Equazioni 1° grado | Solve Exercise (tipo H) | **COPERTO** | ax + b = c |
| Equazioni 2° grado | Solve Exercise (tipo H) | **COPERTO** | ax² + bx + c = 0 |
| Equazioni frazionarie | Solve Exercise (tipo H) | **COPERTO** | (x+a)/(x+b) = c |
| Sistemi lineari | Solve Exercise (tipo H) | **COPERTO** | 2 equazioni, 2 incognite |
| Disequazioni 1° grado | Disequazioni (tipo J) | **IMPLEMENTATO** | Con frazioni e parentesi — 2026-03-12 |
| Disequazioni 2° grado | Disequazioni (tipo J) | **IMPLEMENTATO** | Δ>0, Δ=0, Δ<0, tutti i segni — 2026-03-12 |
| Disequazioni razionali | Disequazioni (tipo J) | **IMPLEMENTATO** | Studio del segno, sistemi — 2026-03-12 |
| MCD e mcm | Solve Exercise (tipo H) | **IMPLEMENTATO** | 7 template: MCD/mcm 2 e 3 numeri, problemi applicativi, semplificazione frazioni — 2026-03-12 |
| Logaritmi e proprietà | Trap Calculator (tipo A) + Solve Exercise (tipo H) | **COPERTO** | Trappole su proprietà logaritmiche + template exp/log |
| Potenze e radicali | Trap Calculator (tipo A) + Estimation Blitz (tipo G) | **COPERTO** | |
| Potenze con esponente razionale | Solve Exercise (tipo H) | **IMPLEMENTATO** | 3 template: (√a)^n, (∛a)^n, a^(m/n) — risultati sempre interi — 2026-03-12 |

### 2.2 Funzioni

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Riconoscimento famiglie | Graph Reader (tipo C) | **COPERTO** | 8 famiglie di funzioni |
| Trasformazioni | Graph Reader (tipo C) | **COPERTO** | Traslazioni, riflessioni, dilatazioni |
| Dominio e codominio | Graph Reader (tipo C) | **COPERTO** | Template specifici |
| Valutazione f(x) | Graph Reader (tipo C) | **COPERTO** | Template di valutazione |
| Segno di f(x) | Graph Reader (tipo C) | **COPERTO** | Per quali x è f(x) > 0? |
| Iniettività | Graph Reader (tipo C) | **IMPLEMENTATO** | Test retta orizzontale, intervalli di iniettività, codominio — 2026-03-12 |
| Invertibilità | Graph Reader (tipo C) | **IMPLEMENTATO** | Condizioni di invertibilità, restrizione dominio — 2026-03-12 |
| Composizione di funzioni | Function Composition (tipo R) | **IMPLEMENTATO** | 7 template: valutazione f(g(x)), identificazione formula, composizione da tabella, ordine importa, decomposizione, dominio composizione, tripla composizione — 162 test — 2026-03-13 |
| Equazioni/disequazioni da grafici | Graph Reader (tipo C) | **IMPLEMENTATO** | 7 template: f(x)=a (trova x), conta soluzioni, f(x)>a intervalli, segno f(x)≥0, f(x)=g(x) intersezioni, f(x)>g(x) intervalli, soluzioni in intervallo — SVG con retta tratteggiata y=a — 64 test — 2026-03-13 |
| Effetto parametri su grafici | Graph Reader (tipo C) | **IMPLEMENTATO** | 8 template: effetto coeff. quadratico, traslazione verticale/orizzontale, dilatazione verticale, riflessione, trasformazione combinata, effetto parametri sin/exp, identificazione formula — SVG multi-curva — 38 test — 2026-03-13 |

### 2.3 Geometria Euclidea

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Proprietà angoli | Geometry Sherlock (tipo F) | **COPERTO** | |
| Triangoli | Geometry Sherlock (tipo F) | **COPERTO** | |
| Cerchi | Geometry Sherlock (tipo F) | **COPERTO** | |
| Poligoni | Geometry Sherlock (tipo F) | **COPERTO** | |
| Aree e perimetri | Geometry Sherlock (tipo F) | **COPERTO** | |
| Geometria solida / Volumi | Geometry Sherlock (tipo F) | **IMPLEMENTATO** | 7 template: cilindro, cono, sfera, prisma, piramide, compositi (cilindro+cono, sfera inscritta) — SVG 3D — 2026-03-12 |
| Trasformazioni geometriche | Geometry Sherlock (tipo F) | **IMPLEMENTATO** | 9 template: simmetria assiale (x/y), traslazione, simmetria centrale, rotazione 90°/180°, similitudine (lunghezze, area/volume), composizione trasformazioni, trasformazione vertici — SVG piano cartesiano — 45 test — 2026-03-13 |
| Triangoli simili | Geometry Sherlock (tipo F) | **IMPLEMENTATO** | 4 template: lato incognito via proporzione, fattore di scala, rapporto aree da k², problema ombre reale — SVG — 71 test — 2026-03-13 |
| Rapporti trigonometrici | Geometry Sherlock (tipo F) | **IMPLEMENTATO** | 4 template: sin/cos/tan dati i lati, lato dato angolo e lato, identificazione angolo da rapporto, altezza edificio con tan — SVG triangolo rettangolo — 2026-03-13 |

### 2.4 Geometria Analitica

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Equazione della retta | Geometria Analitica (tipo K) | **IMPLEMENTATO** | Dato punto+pendenza, per due punti — 2026-03-12 |
| Distanza tra punti | Geometria Analitica (tipo K) | **IMPLEMENTATO** | Formula distanza — 2026-03-12 |
| Punto medio | Geometria Analitica (tipo K) | **IMPLEMENTATO** | Formula punto medio — 2026-03-12 |
| Rette parallele e perpendicolari | Geometria Analitica (tipo K) | **IMPLEMENTATO** | Condizioni m₁=m₂, m₁·m₂=-1 — 2026-03-12 |
| Equazione della circonferenza | Geometria Analitica (tipo K) | **IMPLEMENTATO** | (x-a)²+(y-b)²=r² — 2026-03-12 |
| Asse di un segmento | Geometria Analitica (tipo K) | **IMPLEMENTATO** | Asse come luogo geometrico — 2026-03-12 |
| Intersezione retta-circonferenza | Geometria Analitica (tipo K) | **IMPLEMENTATO** | Conteggio intersezioni — 2026-03-12 |

### 2.5 Logica e Insiemi

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Negazione proposizioni | Logic Puzzle (tipo D) | **COPERTO** | ¬(∀x P(x)) = ∃x ¬P(x) |
| Quantificatori | Logic Puzzle (tipo D) | **COPERTO** | Universale ed esistenziale |
| Implicazioni | Logic Puzzle (tipo D) | **COPERTO** | |
| Deduzione logica | Logic Puzzle (tipo D) | **COPERTO** | |
| Notazione insiemistica | Logic Puzzle (tipo D) | **IMPLEMENTATO** | 7 template: ∈, ⊂, ∪, ∩, complemento, differenza, Venn 2/3 insiemi — 2026-03-12 |

### 2.6 Probabilità e Combinatorica

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Probabilità semplice | Probability Game (tipo E) | **COPERTO** | Dado, carte, urne |
| Eventi composti | Probability Game (tipo E) | **COPERTO** | Con/senza rimpiazzo |
| Probabilità condizionata | Probability Game (tipo E) | **COPERTO** | P(A|B), Bayes |
| Permutazioni | Probability Game (tipo E) | **COPERTO** | Semplici e con ripetizione |
| Combinazioni | Probability Game (tipo E) | **COPERTO** | |
| Principio di conteggio | Probability Game (tipo E) | **COPERTO** | |

### 2.7 Statistica

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Media | Statistics Exercise (tipo I) | **COPERTO** | |
| Mediana | Statistics Exercise (tipo I) | **COPERTO** | |
| Moda | Statistics Exercise (tipo I) | **COPERTO** | |
| Lettura grafici (istogrammi, torte) | Statistics Exercise (tipo I) | **IMPLEMENTATO** | 3 template: istogramma, torta, barre — 2026-03-12 |
| Varianza | Statistics Exercise (tipo I) | **EXTRA** | Marcato come "Approfondimento" (L3) — 2026-03-12 |
| Deviazione standard | Statistics Exercise (tipo I) | **EXTRA** | Marcato come "Approfondimento" (L3) — 2026-03-12 |
| Quartili e percentili | Statistics Exercise (tipo I) | **EXTRA** | Marcato come "Approfondimento" (L3) — 2026-03-12 |
| Outlier detection | Statistics Exercise (tipo I) | **EXTRA** | Non richiesto dal syllabus base |

### 2.8 Modellizzazione e Problem Solving

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Traduzione problemi in equazioni | Word Modeler (tipo B) | **COPERTO** | 3 livelli, 12+ template |
| Problemi con risultato numerico | Word Modeler (tipo B) | **IMPLEMENTATO** | 8 template: età, sconti, medie, lavoro, profitto, sistemi, distanza — 2026-03-12 |
| Problemi a più variabili | Word Modeler (tipo B) | **COPERTO** | Livelli 2 e 3 |
| Stima e calcolo mentale | Estimation Blitz (tipo G) | **COPERTO** | 3 livelli con timer |

### 2.9 Competenze Cognitive Trasversali (TOLC-31→34)

| Competenza | Modulo | Stato | Note |
|---------------------|----------------|-------|------|
| Semplificazione espressioni | Simplification (tipo L) | **IMPLEMENTATO** | 10 template: potenze negative, raccoglimento, potenze, frazioni, logaritmi, prodotti notevoli, frazioni algebriche, radicali nested, frazioni composte, log+exp misti — 2026-03-12 |
| Ragionamento teorico (sempre/mai vero) | Always True (tipo M) | **IMPLEMENTATO** | 8 template: quadrato binomio, distribuzione frazioni, radice somma, AM-GM, valore assoluto, potenze e ordine, divisibilità, logaritmi e ordine — 2026-03-12 |
| Ragionamento proporzionale | Proportional Reasoning (tipo N) | **IMPLEMENTATO** | 6 template: proporzionalità diretta, inversa, quadratica, percentuali composte, variazione parametri, variazione combinata — 2026-03-12 |
| Lettura grafici inversa | Graph Reader (tipo C) | **IMPLEMENTATO** | 6 template: preimmagini, segno, crescenza, max/min, codominio, intersezioni con retta — 2026-03-13 |
| Geometria cerchio avanzata | Geometry Sherlock (tipo F) | **IMPLEMENTATO** | 4 template: angolo inscritto, distanza corda, lunghezza arco, potenza di un punto — 2026-03-13 |
| Domande cross-topic | Cross Topic (tipo O) | **IMPLEMENTATO** | 5 template: algebra+geometria, quadratica+analitica, probabilità+combinatoria, trig+geometria, funzioni+statistica — 2026-03-13 |

---

## 3. Riepilogo Quantitativo

| Stato | Conteggio | Percentuale |
|-------|-----------|-------------|
| COPERTO | 34 | 60% |
| IMPLEMENTATO | 23 | 40% |
| PARZIALE | 0 | 0% |
| ASSENTE | 0 | 0% |
| EXTRA | 4 | — |

**Copertura effettiva syllabus**: **100%** (57/57 argomenti coperti o implementati, esclusi 4 EXTRA)
**Copertura competenze cognitive**: 7/7 competenze coperte (§2.9)

### Inventario Template (~175 totali)

| Modulo | File | L1 | L2 | L3 | Totale |
|--------|------|----|----|----|----|
| Algebra | solve_exercise.py | 14 | 15 | 12 | 41 |
| Disequazioni | inequalities.py | 2 | 3 | 2 | 7 |
| Geometria (Euclidea + Solida + Cerchio) | geometry_sherlock.py | 7 | 11 | 10 | 28 |
| Geometria Analitica | analytic_geometry.py | 3 | 3 | 3 | 9 |
| Statistica | statistics_exercise.py | 8 | 3 | 7 | 18 |
| Semplificazione | simplification.py | 4 | 3 | 3 | 10 |
| Sempre/Mai Vero | always_true.py | 3 | 3 | 2 | 8 |
| Ragionamento Proporzionale | proportional_reasoning.py | 2 | 2 | 2 | 6 |
| Grafici Inversi | graph_reader.py (inverse) | 0 | 4 | 2 | 6 |
| Cross-Topic | cross_topic.py | 1 | 2 | 2 | 5 |
| **Senso Numerico** | **number_sense.py** | **4** | **4** | **4** | **12** |
| **Quale Soddisfa?** | **which_satisfies.py** | **3** | **4** | **3** | **10** |
| Word Modeler (numerici v4) | word_modeler.py | +2 | +2 | +1 | +5 |
| Combinatorica vincolata | probability_game.py | 0 | +2 | +2 | +4 |
| **Totale** | | **~53** | **~61** | **~55** | **~175** |

*Nota: conteggi includono template con naming convention _t#, template funzionali, e template aggiuntivi in moduli senza naming convention (graph_reader, word_modeler, trap_calculator, logic_puzzle, probability_game, estimation_blitz).*

### Simulazione Esame Realistico

| Aspetto | Stato |
|---------|-------|
| Distribuzione pesata TOLC-B | **IMPLEMENTATO** — `REALISTIC_EXAM_WEIGHTS` con frequenze reali |
| Grafici SVG in simulazione | **IMPLEMENTATO** — 4 domande con SVG (2 graph + 2 geometry) |
| Formato 20 domande / 5 opzioni | **COPERTO** |
| Timer 50 minuti | **COPERTO** |
| Punteggio +1/0/-0.25 | **COPERTO** |

---

## 4. Raccomandazioni e Tracciamento

### Alta Priorità

- [x] **R1 — Modulo Geometria Analitica**: ✅ Implementato come `exercises/analytic_geometry.py` con 9 template su 3 livelli (2026-03-12)
- [x] **R2 — Modulo Disequazioni**: ✅ Implementato come `exercises/inequalities.py` con 7 template su 3 livelli, notazione intervallare (2026-03-12)
- [x] **R3 — Riallineamento Statistica**: ✅ Aggiunti 3 template lettura grafici, riorganizzati livelli, contenuti extra marcati "Approfondimento" (2026-03-12)

### Media Priorità

- [x] **R4 — Iniettività e invertibilità funzioni**: ✅ Aggiunti 4 template in Graph Reader: iniettività (test retta orizzontale), invertibilità, codominio/immagine, intervalli di iniettività (2026-03-12)
- [x] **R5 — Notazione insiemistica**: ✅ Aggiunti 7 template in Logic Puzzle: appartenenza, operazioni base, inclusione, complemento/differenza, operazioni composte, Venn 2 insiemi, Venn 3 insiemi (2026-03-12)
- [x] **R6 — MCD e mcm**: ✅ Aggiunti 7 template in Solve Exercise: MCD/mcm 2 numeri con fattorizzazione, problemi applicativi (periodicità, gruppi uguali), semplificazione frazioni, MCD/mcm 3 numeri (2026-03-12)

### Miglioramenti Simulazione (TOLC-25→26)

- [x] **R10 — Grafici SVG nella simulazione**: ✅ Aggiunta rendering SVG inline per domande graph e geometry nella simulazione esame. 4 domande con grafici su 20. CSS responsive. (2026-03-12)
- [x] **R11 — Distribuzione pesata domande**: ✅ `REALISTIC_EXAM_WEIGHTS` config con frequenze TOLC-B reali: Algebra ~30%, Geometria ~20%, Funzioni ~20%, Probabilità ~15%, Statistica/Logica ~15%. (2026-03-12)

### Nuovi Contenuti (TOLC-27→29)

- [x] **R12 — Geometria solida / Volumi**: ✅ 7 template in Geometry Sherlock: cilindro, prisma (L1), cono, sfera, piramide (L2), compositi cilindro+cono e sfera inscritta (L3). SVG 3D. (2026-03-12)
- [x] **R13 — Potenze con esponente razionale**: ✅ 3 template in Solve Exercise: (√a)^n (L1), (∛a)^n e a^(m/n) (L2). Risultati sempre interi. (2026-03-12)
- [x] **R14 — Word problems con risultato numerico**: ✅ 8 template in Word Modeler: età, sconti, medie, lavoro, profitto (L1-L2), sistemi, distanza (L3). Mix automatico con modalità equazione. (2026-03-12)

### Bassa Priorità (precedenti)

- [x] **R7 — Avviso complementarità**: ✅ Aggiunto banner dismissibile nella dashboard con sezioni TOLC-B non coperte (Biologia, Chimica, Fisica, Comprensione del testo) e link CISIA. Persistenza dismiss via localStorage (2026-03-12)
- [x] **R8 — Modo esame realistico**: ✅ Nuova modalità `/realistic-exam` con formato diretto TOLC-B: 20 domande testo, 5 opzioni A-E, punteggio +1/0/-0.25, timer 50min, report finale con review domande (2026-03-12)
- [x] **R9 — Contestualizzazione problemi**: ✅ Aggiunti 8 nuovi template in Word Modeler con contesti realistici italiani: supermercato, piano telefonico, ricette, biglietti treno, allenamento sportivo, bolletta elettrica, pianificazione viaggio, appartamento condiviso (2026-03-12)

---

## 5. Registro Modifiche

> L'implementatore deve aggiornare questa sezione ogni volta che risolve una raccomandazione.

| Data | Raccomandazione | Descrizione Modifica | Autore |
|------|----------------|----------------------|--------|
| 2026-03-12 | R1 | Creato modulo `exercises/analytic_geometry.py` con classe `AnalyticGeometry`: 9 template (retta, distanza, punto medio, parallele/perpendicolari, asse segmento, circonferenza, intersezione). Registrato in `app.py` come tipo `analytic_geo`. | Claude |
| 2026-03-12 | R2 | Creato modulo `exercises/inequalities.py` con classe `InequalitiesExercise`: 7 template (diseq. 1° grado con frazioni/parentesi, 2° grado con gestione Δ, razionali con studio del segno, sistemi). Risposte in notazione intervallare. Registrato in `app.py` come tipo `inequalities`. | Claude |
| 2026-03-12 | R3 | Modificato `exercises/statistics_exercise.py`: aggiunti 3 template lettura grafici (istogramma, torta, barre) in L1. Riorganizzati livelli (varianza/dev.std spostati a L3). Aggiunto campo `approfondimento` nei metadata. | Claude |
| 2026-03-12 | R4 | Aggiunti 4 template in `exercises/graph_reader.py`: iniettività (test retta orizzontale), invertibilità (condizioni biiezione), codominio/immagine (6 famiglie), intervalli di iniettività (quadratiche, valore assoluto, trigonometriche). Template integrati in L2/L3. Test: `tests/test_graph_reader_injectivity.py` (22 test). | Claude |
| 2026-03-12 | R5 | Aggiunti 7 template in `exercises/logic_puzzle.py`: appartenenza (∈), operazioni base (∪, ∩), inclusione (⊂, ⊆), complemento e differenza, operazioni composte, Venn 2 insiemi (inclusione-esclusione), Venn 3 insiemi. Distribuiti su 3 livelli. Test: `tests/test_logic_puzzle_sets.py` (16 test). | Claude |
| 2026-03-12 | R6 | Aggiunti 7 template in `exercises/solve_exercise.py`: MCD/mcm 2 numeri con scomposizione in fattori primi (L1), problemi applicativi periodicità e gruppi uguali (L2), semplificazione frazioni (L1), MCD/mcm 3 numeri (L3). Helper `_prime_factorization()`. Test: `tests/test_solve_exercise_gcd_lcm.py` (35 test). | Claude |
| 2026-03-12 | R7 | Aggiunto banner informativo dismissibile in `templates/dashboard.html` con sezioni TOLC-B non coperte e link risorse CISIA. Stili in `static/css/style.css`. Dismiss persistente via localStorage. | Claude |
| 2026-03-12 | R8 | Creata modalità Esame Realistico: route `/realistic-exam` in `app.py`, API `/api/realistic-exam/exercises` (20 domande text-only, 5 opzioni), template `templates/realistic_exam.html`, JS `static/js/realistic_exam.js` con opzioni A-E, review domande post-consegna. Link in dashboard e nav. | Claude |
| 2026-03-12 | R9 | Aggiunti 8 template in `exercises/word_modeler.py`: supermercato (L1), piano telefonico (L1), ricetta cucina (L1), biglietti treno (L2), allenamento sportivo (L2), bolletta elettrica (L2), pianificazione viaggio (L3), appartamento condiviso (L3). Contesti italiani realistici. Test: `tests/test_word_modeler_contexts.py` (89 test). | Claude |
| 2026-03-12 | TOLC-22 | Rivalutazione copertura post-implementazione: verificato nel codice ogni stato IMPLEMENTATO, ricalcolate percentuali (34 COPERTO + 15 IMPLEMENTATO = 49/49, 100%), creata sezione 7 con confronto pre/post per macro-area. | Claude |
| 2026-03-12 | R10 (TOLC-25) | Grafici SVG nella simulazione esame: aggiunto `graph: 2` a `REALISTIC_EXAM_WEIGHTS`, rimossa rimozione `graph_data`, rendering SVG inline in `realistic_exam.js` (exam + review), CSS responsive `.sim-graph-container` in `style.css`, aggiornato testo regole in `realistic_exam.html`. | Claude |
| 2026-03-12 | R11 (TOLC-26) | Distribuzione pesata: aggiunto `REALISTIC_EXAM_WEIGHTS` config dict in `app.py` con frequenze TOLC-B reali. Sostituita lista hardcoded con generazione dinamica. Fix normalizzazione `steps`→`options` per trap. Test: `tests/test_weighted_distribution.py`. | Claude |
| 2026-03-12 | R12 (TOLC-27) | Geometria solida: 7 template in `geometry_sherlock.py` (cilindro, prisma, cono, sfera, piramide, composito cilindro+cono, sfera inscritta in cilindro). Helper `_svg_ellipse()`. SVG 3D-like. Test: `tests/test_geometry_solids.py` (25 test). | Claude |
| 2026-03-12 | R13 (TOLC-28) | Potenze esponente razionale: 3 template in `solve_exercise.py` — (√a)^n (L1), (∛a)^n (L2), a^(m/n) (L2). Risultati garantiti interi. Test: `tests/test_solve_exercise_rational_exp.py` (18 test). | Claude |
| 2026-03-12 | R14 (TOLC-29) | Word problems numerici: 8 template in `word_modeler.py` — età/somma, sconto, percentuale (L1), media, lavoro, profitto (L2), sistema età, distanza (L3). Helper `_numeric_distractors`. Refactoring `_get_templates()` per merge equazione+numerico. Test: `tests/test_word_modeler_numeric.py`. | Claude |
| 2026-03-12 | TOLC-30 | Rivalutazione copertura v2 post-TOLC-25→29: aggiornato inventario template (88 totali), aggiunta sezione simulazione esame, aggiornati conteggi (51 argomenti, 442 test), documentati gap residui minori (§8). | Claude |
| 2026-03-13 | TOLC-33 | Aggiunti 6 template inversi in `exercises/graph_reader.py`: preimmagini, segno f(x)<0, crescenza/decrescenza, max/min su intervallo, codominio, intersezioni con retta orizzontale. SVG con linea tratteggiata y=k. Probabilità selezione template L2+ aumentata da 35% a 45%. Test: `tests/test_graph_reader_inverse.py` (33 test). | Claude |
| 2026-03-13 | TOLC-35 | Aggiunti 4 template cerchio avanzato in `exercises/geometry_sherlock.py`: angolo inscritto (teorema), distanza corda dal centro (Pitagora), lunghezza arco (formula), potenza di un punto (secanti). SVG con archi colorati e angoli. Test: `tests/test_geometry_circle_advanced.py` (26 test). | Claude |
| 2026-03-13 | TOLC-36 | Creato modulo `exercises/cross_topic.py` con 5 template cross-topic: algebra+geometria area rettangolo (L1), quadratica+geometria analitica vertice parabola (L2), probabilità+combinatoria carte (L2), trigonometria+geometria area triangolo (L3), funzioni+statistica media (L3). Registrato in app.py, 2 domande su 20 nella simulazione. Test: `tests/test_cross_topic.py` (34 test). | Claude |
| 2026-03-12 | TOLC-31 | Creato modulo `exercises/simplification.py` con classe `SimplificationExercise`: 10 template semplificazione espressioni (potenze negative, raccoglimento, potenze di potenze, somma frazioni, logaritmi, prodotti notevoli, frazioni algebriche, radicali nested, frazioni composte, log+exp misti). Formato "L'espressione X è uguale a:" con 5 opzioni. Distrattori basati su errori comuni. Test: `tests/test_simplification.py` (43 test). | Claude |
| 2026-03-12 | TOLC-32 | Creato modulo `exercises/always_true.py` con classe `AlwaysTrueExercise`: 8 template ragionamento teorico (quadrato binomio, distribuzione frazioni, radice somma, AM-GM, valore assoluto, potenze e ordine, divisibilità, logaritmi e ordine). Formato "Sempre/Mai/Talvolta vero" con controesempi espliciti. Test: `tests/test_always_true.py` (40 test). | Claude |
| 2026-03-12 | TOLC-34 | Creato modulo `exercises/proportional_reasoning.py` con classe `ProportionalReasoning`: 6 template ragionamento proporzionale (diretto, inverso, quadratico, percentuali composte, variazione parametri, variazione combinata). Formule fisiche/geometriche reali. Test: `tests/test_proportional_reasoning.py` (13 test). | Claude |
| 2026-03-13 | TOLC-37 | Assessment v3 (§9): rianalisi 20 domande Alpha Test vs app aggiornata. Copertura per competenza cognitiva dal 35% al 75%. 8 domande passate da NON COPERTO a COPERTO grazie a TOLC-31→36. Gap residui: 2 domande (parabola, sviluppo cono) — priorità bassa. Aggiornati §1, §3, §7.2 con nuove metriche. | Claude |
| 2026-03-13 | TOLC-38 | Creato modulo `exercises/number_sense.py` con classe `NumberSense`: 12 template senso numerico (percentuali, frazioni, potenze, notazione scientifica, stime). L1: percentage_of_quantity, decimal_to_fraction, power_small_decimal, fraction_of_quantity. L2: order_of_magnitude_sum, percentage_time_conversion, power_rules_numeric, scientific_notation_order. L3: successive_percentage, nested_fraction_compute, estimation_product, percentage_reverse. Test: `tests/test_number_sense.py` (344 test). | Claude |
| 2026-03-13 | TOLC-39 | Creato modulo `exercises/which_satisfies.py` con classe `WhichSatisfies`: 10 template meta-formato "quale soddisfa?" L1: which_log_between, which_is_even, which_fraction_largest. L2: which_equation_has_solution, which_not_injective, which_inequality_has_interval, which_expression_equals. L3: which_system_consistent, which_parabola_passes_through, which_always_positive. Test: `tests/test_which_satisfies.py` (174 test). | Claude |
| 2026-03-13 | TOLC-40 | Ribilanciati `REALISTIC_EXAM_WEIGHTS` in `app.py`: rimossi trap, always_true, proportional, cross_topic dalla simulazione esame. Aggiunti number_sense(3) e which_satisfies(2). Totale mantenuto a 20. 12 tipi realistici. Tipi rimossi restano disponibili in modalità apprendimento. | Claude |
| 2026-03-13 | TOLC-41 | Aggiunti 4 template combinatorica vincolata in `exercises/probability_game.py`: _comb_digit_constraint (vincolo parità cifre, L2), _comb_seating_adjacent (posti adiacenti, L2), _comb_digits_no_repeat (cifre senza ripetizione, L3), _comb_selection_exclusion (selezione con esclusione, L3). Helper _make_int_distractors. Test: `tests/test_combinatorics_constrained.py` (213 test). | Claude |
| 2026-03-13 | TOLC-42 | Aggiunti 5 template word problems numerici TOLC-style in `exercises/word_modeler.py`: _numeric_bus_cost (arrotondamento per eccesso, L1), _numeric_fraction_redistribution (redistribuzione frazioni, L1), _numeric_percentage_multistep (percentuali multistep, L2), _numeric_exam_scores (media voti, L2), _numeric_successive_operations (operazioni successive, L3). Aggiunto parametro exam_mode=True per preferire 60% numerici in modalità esame. | Claude |
| 2026-03-13 | TOLC-43 | Assessment v4 (§10): rivalutazione completa 40 domande reali (SET A + SET B). Copertura dal 67.5% (27/40) al 87.5% (35/40). 1 sola domanda NON COPERTA (parabola). Realismo simulazione da 7.5/10 a 8.5/10. Distribuzione pesi allineata al TOLC reale entro ±5%. 1484 test, ~175 template, 17 moduli. | Claude |
| 2026-03-13 | TOLC-50 | Creato modulo `exercises/function_composition.py` con classe `FunctionComposition`: 7 template composizione funzioni. L1: evaluate_composition f(g(a)), identify_composition_formula. L2: composition_from_table, order_matters f∘g≠g∘f, decompose_function. L3: domain_of_composition, triple_composition. Registrato in `app.py` come tipo `composition`, aggiunto a `REALISTIC_EXAM_WEIGHTS` (peso 1). Test: `tests/test_function_composition.py` (162 test). | Claude |
| 2026-03-13 | TOLC-51 | Aggiunti 9 template trasformazioni geometriche in `exercises/geometry_sherlock.py`: L1 — simmetria assiale (asse x/y), traslazione per vettore, simmetria centrale (origine). L2 — rotazione 90°/270°, similitudine lunghezze (rapporto k), rotazione 180° somma coordinate. L3 — similitudine area/volume (k²/k³), composizione traslazione+riflessione, trasformazione vertici triangolo. Helpers SVG: `_svg_coordinate_plane()`, `_svg_point()`, `_svg_dashed_line()`, `_svg_arrow()`. Fix loop infiniti pre-esistenti. Test: `tests/test_geometric_transformations.py` (45 test). | Claude |
| 2026-03-13 | TOLC-52 | Aggiunto parametro `exam_mode=True` a `EstimationBlitz.generate()`: rimuove `time_limit`, cambia prefisso domanda in "Senza calcolatrice, stimare il valore di:". Aggiunto `estimation` a `REALISTIC_EXAM_WEIGHTS` (peso 1), ribilanciato number_sense da 3→2 e word da 2→1, aggiunto composition peso 1. Totale resta 20. Test: `tests/test_estimation_exam.py` (113 test). | Claude |

---

## 6. Note per l'Implementatore

1. **Dopo ogni implementazione**: aggiornare la tabella di copertura (§2) cambiando lo stato da ASSENTE/PARZIALE a IMPLEMENTATO, spuntare la checkbox in §4, e aggiungere una riga al Registro Modifiche (§5).
2. **Contenuti EXTRA**: non rimuoverli, ma contrassegnarli nell'UI come "Approfondimento" per evitare confusione con il syllabus base.
3. **File di riferimento**: `exercises/` contiene tutti i moduli, `app.py` contiene il registry degli esercizi e le route API.
4. **Testing**: ogni nuovo template deve essere testabile via `pytest` e generare almeno 3 varianti distinte senza errori.

---

## 7. Confronto Copertura Pre/Post Implementazione

> Rivalutazione eseguita il 2026-03-12 dopo il completamento di tutti i task (TOLC-13 → TOLC-29).

### 7.1 Tabella Comparativa per Macro-Area

| Macro-area | Argomenti | Baseline | Post R1-R9 | Post R10-R14 | Delta totale |
|------------|-----------|----------|------------|--------------|-------------|
| 2.1 Algebra e Aritmetica | 13 | 8 | 12 | 13 | **+5** |
| 2.2 Funzioni | 7 | 5 | 7 | 7 | **+2** |
| 2.3 Geometria Euclidea + Solida | 6 | 5 | 5 | 6 | **+1** |
| 2.4 Geometria Analitica | 7 | 0 | 7 | 7 | **+7** |
| 2.5 Logica e Insiemi | 5 | 4 | 5 | 5 | **+1** |
| 2.6 Probabilita e Combinatorica | 6 | 6 | 6 | 6 | 0 |
| 2.7 Statistica (syllabus) | 4 | 3 | 4 | 4 | **+1** |
| 2.8 Modellizzazione e Problem Solving | 4 | 3 | 3 | 4 | **+1** |
| **Totale** | **51** | **34** | **49** | **51** | **+18** |

### 7.2 Percentuali Aggregate

| Metrica | Baseline | Post R1-R9 | Post R10-R14 | Post TOLC-31→36 | **Post v4 (TOLC-38→42)** |
|---------|----------|------------|--------------|-----------------|--------------------------|
| Argomenti coperti | 34/49 (69%) | 49/49 (100%) | 51/51 (100%) | 57/57 (100%) | **57/57 (100%)** |
| Macro-aree complete | 4/8 (50%) | 8/8 (100%) | 8/8 (100%) | 9/9 (100%) | **9/9 (100%)** |
| Moduli esercizi | 9 | 11 | 11 | 15 | **17** |
| Template totali | ~70 | ~80 | 88 | ~138 | **~175** |
| Test automatizzati | — | 171 | 442 | 631 | **1484** |
| Simulazione: distribuzione | uniforme | uniforme | pesata TOLC-B | pesata + cognitive | **ribilanciata reale (12 tipi)** |
| Simulazione: grafici SVG | no | no | 4 domande su 20 | 4 domande su 20 | **4 domande su 20** |
| Simulazione: competenze cognitive | no | no | 0 domande | 7 domande su 20 | **incl. number_sense + which_satisfies** |
| Copertura domande reali (40q) | — | — | 35% (SET-B) | 75% (SET-B) | **87.5% (SET-A+B, §10)** |

### 7.3 Argomenti Ancora Scoperti

**Nessun argomento del syllabus TOLC-B Matematica risulta scoperto.**

I 4 contenuti **EXTRA** (Varianza, Deviazione standard, Quartili/percentili, Outlier detection) restano presenti nel modulo Statistica marcati come "Approfondimento" (L3).

Le sezioni TOLC-B **non coperte dall'app** (Biologia, Chimica, Fisica, Comprensione del testo) sono segnalate tramite banner informativo nella dashboard con link CISIA (R7).

### 7.4 Valutazione Qualitativa

**Fase 1 (R1-R9) — Copertura syllabus:**

1. **Completezza**: copertura dal 69% al 100% del syllabus
2. **Nuovi moduli**: `analytic_geometry.py` (9 template), `inequalities.py` (7 template)
3. **Arricchimento**: +29 template in moduli esistenti (Graph Reader, Logic Puzzle, Solve Exercise, Statistics, Word Modeler)
4. **Esperienza utente**: banner CISIA, Esame Realistico

**Fase 2 (R10-R14) — Qualità simulazione e profondità:**

1. **Simulazione esame potenziata**:
   - Distribuzione pesata `REALISTIC_EXAM_WEIGHTS` allineata a frequenze TOLC-B reali (R11)
   - 4 domande con grafici SVG su 20 — rendering inline responsive (R10)
2. **Geometria solida**: 7 template volumi con SVG 3D (cilindro, cono, sfera, prisma, piramide, compositi) (R12)
3. **Algebra rafforzata**: 3 template potenze con esponente razionale — (√a)^n, (∛a)^n, a^(m/n) (R13)
4. **Word problems realistici**: 8 template con risposta numerica diretta, mix automatico con modalità equazione (R14)
5. **Qualità**: da 171 a **442 test** automatizzati (+158%)

---

## 8. Gap Residui Minori e Raccomandazioni Future

### 8.1 Gap Residui (nessuno critico)

| Area | Gap | Priorità | Note |
|------|-----|----------|------|
| Trigonometria | Solo valori notevoli e identità base; mancano equazioni trig complesse (sin(2x)=cos(x)) | Bassa | Coperto per il livello TOLC-B, equazioni complesse raramente presenti |
| Combinatorica | Mancano problemi di disposizioni semplici e con ripetizione | Bassa | Permutazioni e combinazioni già coperte |
| Geometria analitica | Mancano parabola e ellisse | Bassa | Nel TOLC-B raro; retta e circonferenza sono dominanti |
| Statistica | Mancano correlazione e regressione lineare | Molto bassa | Non nel syllabus TOLC-B base |

### 8.2 Raccomandazioni per il futuro

1. **Varietà template**: aumentare il numero di template per tipo (attualmente 3-7 per livello) per ridurre la ripetitività percepita dallo studente
2. **Difficoltà adattiva**: implementare selezione difficoltà basata sulle performance dello studente
3. **Spiegazioni interattive**: aggiungere passaggi intermedi cliccabili nelle spiegazioni
4. **Statistiche per argomento**: mostrare allo studente i punti deboli per macro-area TOLC-B

---

## 9. Assessment v3 — Copertura per Competenza Cognitiva (TOLC-37)

> Rivalutazione eseguita il 2026-03-13 dopo il completamento di TOLC-31 → TOLC-36.
> Metodologia: le stesse 20 domande Alpha Test ("Nona Prova") usate nell'analisi iniziale
> vengono confrontate con l'app aggiornata. Valutazione per COMPETENZA COGNITIVA, non solo per argomento.

### 9.1 Confronto Domanda per Domanda: Prima vs Dopo

| # | Domanda Alpha Test | Competenza Cognitiva | Prima (v2) | Dopo (v3) | Modulo Coprente |
|---|---|---|---|---|---|
| Q1 | log₁₀60 / log₁₀√10 = ? | Semplificazione espressione | PARZIALE | **COPERTO** | Simplification (`_t2_log_simplification`) |
| Q2 | Prob. prime 4 carte siano donne | Calcolo probabilità | COPERTO | COPERTO | Probability Game |
| Q3 | (2ab-b²-a²)·(b-a) = ? | Fattorizzazione / prodotto notevole | NON COPERTO | **COPERTO** | Simplification (`_t2_notable_products`) |
| Q4 | Intersezione curva 2y²=3x+8 con asse y | Geom. analitica — coniche | NON COPERTO | NON COPERTO | — (parabola non implementata) |
| Q5 | Cerchio tangente da punto esterno + trig | Cross-topic geom+trig | NON COPERTO | **PARZIALE** | Geometry Sherlock (cerchio avanzato) + Cross Topic (`_t3_trig_geometry`) — ma manca tangente da punto esterno specifico |
| Q6 | Equazione asse segmento P(0,6) Q(8,0) | Geometria analitica | COPERTO | COPERTO | Analytic Geometry |
| Q7 | √((√(a²+4)-2)(√(a²+4)+2)) | Semplificazione radicali nested | NON COPERTO | **COPERTO** | Simplification (`_t3_nested_radicals`) |
| Q8 | x²/2 + 3x + 2 = 0, soluzione maggiore | Equazione quadratica | COPERTO | COPERTO | Solve Exercise |
| Q9 | (a/b+c/d)/(b/d+a/c) semplificazione | Semplificazione frazioni algebriche | NON COPERTO | **COPERTO** | Simplification (`_t2_algebraic_fractions`, `_t3_compound_algebraic`) |
| Q10 | 10⁹ + 10⁸ + 10⁹ = ? | Raccoglimento fattore comune | PARZIALE | **COPERTO** | Simplification (`_t1_common_factor`) |
| Q11 | a/b + b/a ≥ 2 sempre vero? | Ragionamento teorico (AM-GM) | NON COPERTO | **COPERTO** | Always True (`_t2_am_gm`) |
| Q12 | a=2b/c², raddoppi b, cosa fai a c? | Ragionamento proporzionale | NON COPERTO | **COPERTO** | Proportional Reasoning (`_t3_parameter_variation`) |
| Q13 | Triangoli simili rapporto 3, rapporto aree | Geometria similitudine | COPERTO | COPERTO | Geometry Sherlock |
| Q14 | Settore circolare → sviluppo cono, raggio base | Geometria 3D avanzata | NON COPERTO | **PARZIALE** | Geometry Sherlock (solidi + cerchio avanzato: `_t3_arc_length`) — ma manca sviluppo superficie laterale specifico |
| Q15 | Corda, distanza dal centro, tangente angolo inscritto | Cerchio avanzato | NON COPERTO | **COPERTO** | Geometry Sherlock (`_t2_inscribed_angle`, `_t2_chord_distance`) |
| Q16 | Frazione generatrice di 0,75 | Aritmetica base | IMPLICITO | IMPLICITO | Troppo semplice per template dedicato |
| Q17 | (2⁻¹+2⁻²)/(2⁻³-2⁻⁴) | Semplificazione esponenti negativi | PARZIALE | **COPERTO** | Simplification (`_t1_negative_exponents`) |
| Q18 | Dal grafico, trovare tutti a t.c. f(3)=f(a) | Lettura grafico inversa | NON COPERTO | **COPERTO** | Graph Reader (`_template_inverse_preimage`) |
| Q19 | Negazione logica complessa | Logica | COPERTO | COPERTO | Logic Puzzle |
| Q20 | Lettura grafico a barre, rapporto tra categorie | Statistica | COPERTO | COPERTO | Statistics Exercise |

### 9.2 Conteggio Copertura: Prima vs Dopo

| Stato | Prima (v2) | Dopo (v3) | Delta |
|-------|------------|-----------|-------|
| **COPERTO** | 7/20 (35%) | **15/20 (75%)** | **+8** |
| **PARZIALE** | 3/20 (15%) | 2/20 (10%) | -1 |
| **NON COPERTO** | 10/20 (50%) | 2/20 (10%) | **-8** |
| **IMPLICITO** | 0 (contato come parziale) | 1/20 (5%) | — |

**Miglioramento netto**: dal 35% al 75% di copertura piena sulle domande reali Alpha Test.

### 9.3 Copertura per Competenza Cognitiva

| Competenza Cognitiva | Domande Alpha Test | Prima | Dopo | Modulo |
|---|---|---|---|---|
| Risolvi/Calcola | Q2, Q6, Q8, Q13, Q19, Q20 | 6/6 (100%) | 6/6 (100%) | Solve, Probability, Analytic Geo, Geometry, Logic, Statistics |
| Semplifica/Identifica equivalente | Q1, Q3, Q7, Q9, Q10, Q17 | 0/6 (0%) | **6/6 (100%)** | Simplification (TOLC-31) |
| Sempre/Mai vero | Q11 | 0/1 (0%) | **1/1 (100%)** | Always True (TOLC-32) |
| Leggi il grafico (inverso) | Q18 | 0/1 (0%) | **1/1 (100%)** | Graph Reader inverse (TOLC-33) |
| Ragiona su proporzionalità | Q12 | 0/1 (0%) | **1/1 (100%)** | Proportional Reasoning (TOLC-34) |
| Geometria avanzata (cerchio) | Q5, Q14, Q15 | 0/3 (0%) | **1/3 pieno + 2/3 parziale** | Geometry Sherlock circle (TOLC-35) |
| Cross-topic | Q4, Q5 | 0/2 (0%) | **0/2 pieno + 1/2 parziale** | Cross Topic (TOLC-36) — parabola non coperta |

### 9.4 Analisi dei Gap Residui

Restano **2 domande NON COPERTE** e **2 PARZIALI**:

| # | Domanda | Gap Residuo | Priorità | Motivazione |
|---|---|---|---|---|
| Q4 | Intersezione curva 2y²=3x+8 con asse y | Coniche (parabola) in geometria analitica | **Bassa** | Raro nel TOLC-B; retta e circonferenza dominano. Richiederebbe un modulo coniche dedicato per ROI minimo. |
| Q5 | Tangente da punto esterno + trigonometria | Tangente specifica da punto esterno | **Bassa** | Coperto parzialmente (angolo inscritto + trig+geom cross-topic), ma il sotto-caso specifico "tangente da punto esterno" manca. Template aggiuntivo in Geometry Sherlock potrebbe coprirlo. |
| Q14 | Sviluppo superficie laterale cono | Sviluppo superfici 3D | **Molto bassa** | Caso molto specifico e raro. Abbiamo arco, cono, compositi — lo sviluppo della superficie laterale è un sotto-caso troppo di nicchia. |
| Q16 | Frazione generatrice di 0,75 | Aritmetica elementare | **Nessuna** | Troppo banale per giustificare un template. Lo studente che usa l'app ha già queste competenze. |

### 9.5 Valutazione Realismo Simulazione Esame: Prima vs Dopo

| Aspetto | Prima (v2) | Dopo (v3) | Note |
|---|---|---|---|
| Formato (20q/50min/5opt) | 10/10 | 10/10 | Invariato |
| Punteggio (+1/0/-0.25) | 10/10 | 10/10 | Invariato |
| Navigazione domande | 8/10 | 8/10 | Invariato (TOLC reale non permette tornare indietro tra sezioni) |
| Distribuzione argomenti | 7/10 | **8/10** | Migliorata con competenze cognitive nella distribuzione |
| Stile domande | 5/10 | **8/10** | 7 domande su 20 ora testano competenze cognitive (semplifica, ragiona, analizza grafico) |
| Difficoltà | 6/10 | **7/10** | Cross-topic e geometria avanzata alzano il livello |
| Distrattori | 7/10 | **8/10** | Simplification genera distrattori basati su errori comuni reali |
| Utilità per preparazione | 7/10 | **8/10** | Ora copre sia fondamenta che competenze richieste dal TOLC reale |

**GIUDIZIO COMPLESSIVO v3**: L'app è ora un buon strumento di preparazione che copre il 75% delle domande reali TOLC-B per competenza cognitiva. Resta insufficiente per coniche (parabola/ellisse) e sviluppo superfici 3D, ma questi sono casi rari. Lo studente che usa la nostra app sarà preparato sulla maggior parte delle tipologie di domande del TOLC-B reale, ma dovrebbe comunque integrare con almeno 2-3 simulazioni ufficiali CISIA per familiarizzarsi con i casi limite.

### 9.6 Raccomandazioni Post-Assessment

1. **Gap residui non prioritari**: Q4 (parabola) e Q14 (sviluppo cono) non giustificano implementazione per il basso ROI
2. **Possibile miglioramento incrementale**: aggiungere template "tangente da punto esterno" in Geometry Sherlock per coprire Q5 completamente (effort: basso, 1 template)
3. **Priorità futura**: aumentare la varietà dei template esistenti piuttosto che aggiungere nuovi tipi — la ripetitività è ora il rischio principale per l'esperienza utente
4. **Validazione con studenti reali**: il prossimo passo più utile sarebbe testare l'app con 5-10 studenti TOLC-B e raccogliere feedback qualitativo

---

## 10. Assessment v4 — Copertura Completa 40 Domande Reali (TOLC-43)

> Rivalutazione eseguita il 2026-03-13 dopo il completamento di TOLC-38 → TOLC-42 (milestone "TOLC-B v4 — Realism & Gap Closure").
> Metodologia: tutte le 40 domande reali (SET A: 20 CISIA ufficiali + SET B: 20 Alpha Test "Nona Prova" Gen 2025)
> vengono rivalutate contro l'app v4. Valutazione per DOMANDA, con indicazione del modulo coprente e qualità della copertura.

### 10.1 Novità v4 Rispetto a v3

| Modulo Nuovo/Modificato | Tipo | Template | Copertura Aggiunta |
|---|---|---|---|
| **NumberSense** (`number_sense.py`) | NUOVO | 12 template (L1-L3) | Percentuali→tempo, frazioni decimali, potenze, notazione scientifica, stime |
| **WhichSatisfies** (`which_satisfies.py`) | NUOVO | 10 template (L1-L3) | Meta-formato "quale soddisfa?": log, iniettività, equazioni, sistemi, parabole |
| **Combinatorica vincolata** (`probability_game.py`) | ESTESO | +4 template | Cifre con vincoli parità, posti adiacenti, selezione con esclusione |
| **Word problems numerici** (`word_modeler.py`) | ESTESO | +5 template TOLC-style | Bus/costo, redistribuzione frazioni, percentuali multistep, media voti, operazioni successive |
| **Pesi simulazione** (`app.py`) | RIBILANCIATO | — | Rimossi trap/always_true/proportional/cross_topic; aggiunti number_sense(3), which_satisfies(2) |

### 10.2 Confronto Domanda per Domanda: SET A (20 domande CISIA ufficiali)

| # | Domanda | Topic | v3 | v4 | Modulo v4 | Note |
|---|---|---|---|---|---|---|
| Q1 | 79% di 2 ore, quanto manca? | Percentuali/Tempo | NON COPERTO | **COPERTO** | NumberSense (`_percentage_time_conversion`) | Percentuale→minuti+secondi, stessa struttura |
| Q2 | Quale log è tra 2 e 3? | Logaritmi/Meta-formato | NON COPERTO | **COPERTO** | WhichSatisfies (`_which_log_between`) | Meta-formato identico: 5 logaritmi, quale soddisfa proprietà |
| Q3 | 0,007² = ? (notazione scientifica) | Potenze/Numeri | NON COPERTO | **COPERTO** | NumberSense (`_power_small_decimal`) | Quadrato di decimale → notazione scientifica |
| Q4 | Rita, cioccolata, redistribuzione frazioni | Word problem/Frazioni | NON COPERTO | **COPERTO** | WordModeler (`_numeric_fraction_redistribution`) | Redistribuzione con frazioni, risultato numerico |
| Q5 | Bus 120 persone, costo per persona | Word problem/Arrotondamento | NON COPERTO | **COPERTO** | WordModeler (`_numeric_bus_cost`) + NumberSense | Arrotondamento per eccesso, costo totale÷persone |
| Q6 | (2x+2)⁴ - (x+1)⁴ = ? | Algebra/Fattorizzazione | COPERTO | COPERTO | Simplification | Riconoscimento 2(x+1), fattorizzazione |
| Q7 | Quale disequazione ha soluzione {0<x<3}? | Disequazioni/Meta-formato | PARZIALE | **COPERTO** | WhichSatisfies (`_which_inequality_has_interval`) | Meta-formato: 5 disequazioni, quale ha dato intervallo |
| Q8 | Soluzione minore x²-x-1=0 | Equazione quadratica | COPERTO | COPERTO | SolveExercise | Formula quadratica standard |
| Q9 | Retta in figura: equazione? | Grafico/Analitica | COPERTO | COPERTO | GraphReader + AnalyticGeometry | Lettura grafico → equazione retta |
| Q10 | Cilindro r=5→r=6, quanta acqua? | Proporzionalità/Volume | COPERTO | COPERTO | ProportionalReasoning | r²→volume, rapporto quadratico |
| Q11 | Area quadrato inscritto in cerchio r=4 | Geometria | COPERTO | COPERTO | GeometrySherlock | Diagonale=diametro, Pitagora |
| Q12 | Distanza P(1,½) Q(3,-½) | Geometria analitica | COPERTO | COPERTO | AnalyticGeometry | Formula distanza |
| Q13 | Logica: "ogni giorno d'estate..." deduzione | Logica/Contropositiva | COPERTO | COPERTO | LogicPuzzle | Contropositiva |
| Q14 | Quale funzione non è iniettiva? | Funzioni/Meta-formato | PARZIALE | **COPERTO** | WhichSatisfies (`_which_not_injective`) | Meta-formato: 5 funzioni, quale non è iniettiva |
| Q15 | f(x)=1/x, pendenza retta per x=½ e x=3 | Funzioni+Analitica | COPERTO | COPERTO | CrossTopic + AnalyticGeometry | Valutazione funzione + pendenza |
| Q16 | Quale equazione ha soluzione? (2^x=0, etc.) | Esponenziali/Meta-formato | NON COPERTO | **COPERTO** | WhichSatisfies (`_which_equation_has_solution`) | Meta-formato: 5 equazioni, quale ha soluzione |
| Q17 | Media voti 25→26 con 30, quanti esami? | Statistica/Word problem | COPERTO | COPERTO | WordModeler (`_numeric_exam_scores`) + Statistics | Modellizzazione equazione con medie |
| Q18 | Cartoncino quadrato, area rimasta | Geometria+Algebra | COPERTO | COPERTO | CrossTopic | Modeling geometrico-algebrico |
| Q19 | Numeri dispari 4 cifre con {2,3,7,8} | Combinatorica vincolata | NON COPERTO | **COPERTO** | ProbabilityGame (`_comb_digit_constraint`) | Vincolo parità su ultima cifra, permutazioni |
| Q20 | 70% superano patente, 15 bocciati, totale? | Percentuali/Word problem | PARZIALE | **COPERTO** | NumberSense (`_percentage_reverse`) + WordModeler | Percentuale inversa: dal 30% al totale |

**SET A: 20/20 COPERTO (100%)** — v3 era 12/20 (60%)

### 10.3 Confronto Domanda per Domanda: SET B (20 domande Alpha Test "Nona Prova")

| # | Domanda | Topic | v3 | v4 | Modulo v4 | Note |
|---|---|---|---|---|---|---|
| Q1 | log₁₀60 / log₁₀√10 | Semplificazione log | COPERTO | COPERTO | Simplification | Proprietà logaritmi |
| Q2 | Prob. 4 donne su 12 carte | Probabilità combinatoria | COPERTO | COPERTO | ProbabilityGame | C(4,4)/C(12,4) |
| Q3 | (2ab-b²-a²)(b-a) = ? | Fattorizzazione | COPERTO | COPERTO | Simplification | Prodotti notevoli |
| Q4 | Intersezione 2y²=3x+8 con asse y | Coniche (parabola) | NON COPERTO | NON COPERTO | — | Parabola non implementata; priorità bassa |
| Q5 | Cerchio tangente da punto esterno + trig | Geometria+Trig | PARZIALE | PARZIALE | GeometrySherlock (cerchio avanzato) | Tangente da punto esterno manca come sotto-caso specifico |
| Q6 | Asse segmento P(0,6) Q(8,0) | Geometria analitica | COPERTO | COPERTO | AnalyticGeometry | Template asse segmento |
| Q7 | √((√(a²+4)-2)(√(a²+4)+2)) | Semplificazione radicali | COPERTO | COPERTO | Simplification | Radicali nested |
| Q8 | x²/2+3x+2=0, soluzione maggiore | Equazione quadratica | COPERTO | COPERTO | SolveExercise | Formula quadratica |
| Q9 | (a/b+c/d)/(b/d+a/c) | Semplificazione frazioni | COPERTO | COPERTO | Simplification | Frazioni algebriche composte |
| Q10 | 10⁹+10⁸+10⁹ = ? | Ordini di grandezza | COPERTO | COPERTO | NumberSense (`_order_of_magnitude_sum`) | Somma potenze di 10 |
| Q11 | a/b+b/a ≥ 2 sempre vero? | Ragionamento AM-GM | COPERTO | COPERTO | AlwaysTrue | AM-GM |
| Q12 | a=2b/c², raddoppi b, cosa fai a c? | Proporzionalità | COPERTO | COPERTO | ProportionalReasoning | Variazione parametri |
| Q13 | Triangoli simili, rapporto aree | Geometria similitudine | COPERTO | COPERTO | GeometrySherlock | k²=9 |
| Q14 | Settore circolare → sviluppo cono | Geometria 3D avanzata | PARZIALE | PARZIALE | GeometrySherlock (cono + arco) | Sviluppo superficie laterale specifico manca |
| Q15 | Corda, distanza dal centro, tangente angolo | Cerchio avanzato | COPERTO | COPERTO | GeometrySherlock | Cerchio avanzato: corda + angolo |
| Q16 | Frazione generatrice di 0,75 | Frazioni base | IMPLICITO | **COPERTO** | NumberSense (`_decimal_to_fraction`) | Conversione decimale→frazione, ora template dedicato |
| Q17 | (2⁻¹+2⁻²)/(2⁻³-2⁻⁴) | Potenze negative | COPERTO | COPERTO | Simplification + NumberSense | Potenze negative, semplificazione |
| Q18 | Grafico: f(3)=f(a), trovare tutti a | Lettura grafico inversa | COPERTO | COPERTO | GraphReader (inverse preimage) | Preimmagini da grafico |
| Q19 | Negazione logica complessa | Logica | COPERTO | COPERTO | LogicPuzzle | Negazione quantificatori |
| Q20 | Lettura grafico a barre, rapporto | Statistica/Grafici | COPERTO | COPERTO | StatisticsExercise | Lettura grafici |

**SET B: 17/20 COPERTO + 2 PARZIALE + 1 NON COPERTO** — v3 era 15/20 COPERTO

### 10.4 Riepilogo Copertura Complessiva: v3 → v4

| Stato | v3 (SET-B only, 20q) | v4 (SET-A+B, 40q) | Delta |
|---|---|---|---|
| **COPERTO** | 15/20 (75%) | **35/40 (87.5%)** | **+20 domande evaluate, +20 punti percentuali** |
| **PARZIALE** | 2/20 (10%) | 3/40 (7.5%) | — |
| **NON COPERTO** | 2/20 (10%) | 1/40 (2.5%) | **-1** |
| **IMPLICITO** | 1/20 (5%) | 0/40 (0%) | Promosso a COPERTO (Q16-SET-B) |

**Copertura piena v4**: 35/40 = **87.5%** (target era ~87.5%)

### 10.5 Copertura per Area Tematica

| Area Tematica | Domande (40q) | Coperte v4 | % | Moduli Coprenti |
|---|---|---|---|---|
| **Numeri/Aritmetica** (percentuali, frazioni, potenze, notazione scientifica) | 8 | **8/8** | **100%** | NumberSense, WordModeler |
| **Algebra** (equazioni, disequazioni, espressioni, fattorizzazione) | 8 | **8/8** | **100%** | SolveExercise, Simplification, Inequalities |
| **Geometria Euclidea** (piana, solida, similitudine, cerchio) | 5 | **4/5** | 80% | GeometrySherlock (Q14-SET-B parziale: sviluppo cono) |
| **Geometria Analitica** (rette, distanza, asse, coniche) | 4 | **3/4** | 75% | AnalyticGeometry (Q4-SET-B mancante: parabola) |
| **Funzioni e Grafici** (lettura grafici, proprietà, logaritmi) | 5 | **5/5** | **100%** | GraphReader, WhichSatisfies |
| **Logica e Argomentazione** | 2 | **2/2** | **100%** | LogicPuzzle |
| **Probabilità e Combinatorica** | 2 | **2/2** | **100%** | ProbabilityGame (incl. combinatorica vincolata) |
| **Statistica** | 2 | **2/2** | **100%** | StatisticsExercise |
| **Modellizzazione / Word Problems** | 4 | **4/4** | **100%** | WordModeler (numerici v4) |
| **Meta-formato "Quale soddisfa?"** | 4 | **4/4** | **100%** | WhichSatisfies |
| **Cross-topic** | 2 | **1/2 + 1 parziale** | 75% | CrossTopic, ProportionalReasoning |
| **Trigonometria applicata** | 1 | **0/1 + 1 parziale** | ~50% | GeometrySherlock (cerchio avanzato) |

### 10.6 Gap Residui v4

| # | Domanda | Gap | Priorità | Motivazione Non-Implementazione |
|---|---|---|---|---|
| Q4-SET-B | Intersezione 2y²=3x+8 con asse y | Coniche (parabola) in geom. analitica | **Bassa** | Raro nel TOLC-B reale; retta e circonferenza dominano. 1 domanda su 40. ROI insufficiente. |
| Q5-SET-B | Tangente da punto esterno + trig | Tangente da punto esterno specifico | **Bassa** | Coperto parzialmente (cerchio avanzato + trig cross-topic). Sotto-caso molto specifico. |
| Q14-SET-B | Settore circolare → sviluppo cono | Sviluppo superficie laterale cono | **Molto bassa** | Caso geometrico di nicchia. Template cono e arco esistono, ma lo sviluppo laterale è troppo specifico. |

**Solo 1 domanda su 40 è completamente NON COPERTA** (Q4-SET-B, parabola). Le altre 2 sono PARZIALI con copertura dei concetti sottostanti.

### 10.7 Valutazione Realismo Simulazione Esame: v3 → v4

| Aspetto | v3 | v4 | Note |
|---|---|---|---|
| Formato (20q/50min/5opt) | 10/10 | 10/10 | Invariato |
| Punteggio (+1/0/-0.25) | 10/10 | 10/10 | Invariato |
| Navigazione domande | 8/10 | 8/10 | Invariato |
| **Distribuzione argomenti** | 8/10 | **9/10** | Ribilanciata: number_sense(3), which_satisfies(2), rimossi tipi non-TOLC dalla simulazione |
| **Stile domande** | 8/10 | **9/10** | Meta-formato "quale soddisfa?" + word problems numerici + aritmetica pura |
| **Difficoltà** | 7/10 | **8/10** | Combinatorica vincolata + percentuali inverse alzano realismo |
| **Distrattori** | 8/10 | **9/10** | NumberSense genera distrattori da errori mentali comuni (unità, ordini di grandezza, segno) |
| **Utilità per preparazione** | 8/10 | **9/10** | Copre 87.5% delle tipologie reali vs 75% precedente |
| **Aritmetica pura** (nuova metrica) | 0/10 | **8/10** | 3 domande su 20 dedicate a senso numerico (era 0) |
| **Meta-formato** (nuova metrica) | 0/10 | **8/10** | 2 domande su 20 in formato "quale soddisfa?" (era 0) |

**Score complessivo simulazione v4**: **~8.5/10** (v3 era ~7.5/10)

### 10.8 Confronto Distribuzione Pesi: App v4 vs TOLC Reale

| Categoria | TOLC Reale (40q) | App v4 Sim (20q) | Delta |
|---|---|---|---|
| Aritmetica/Numeri | ~20% (8q) | **15%** (3q number_sense) | -5% |
| Algebra (equazioni, espressioni) | ~20% (8q) | **20%** (2 solve + 1 ineq + 1 simpl) | 0% |
| Geometria (tutte) | ~22.5% (9q) | **20%** (2 geometry + 2 analytic_geo) | -2.5% |
| Funzioni/Grafici | ~12.5% (5q) | **10%** (2 graph) | -2.5% |
| Meta-formato | ~10% (4q) | **10%** (2 which_satisfies) | 0% |
| Prob+Stat+Logica | ~15% (6q) | **15%** (1+1+1 prob/stat/logic) | 0% |
| Word problems (integrati) | ~10% (4q) | **10%** (2 word) | 0% |

**Distribuzione v4 è allineata entro ±5% per ogni categoria** — obiettivo raggiunto.

### 10.9 Impatto v3 → v4 (Tabella Riassuntiva)

| Metrica | v3 | v4 | Delta |
|---|---|---|---|
| Copertura domande reali (40q) | 27/40 (67.5%) | **35/40 (87.5%)** | **+8 domande (+20pp)** |
| Domande NON COPERTE | 11/40 | **1/40** | **-10** |
| Moduli esercizi | 15 | **17** | +2 (NumberSense, WhichSatisfies) |
| Template totali | ~138 | **~175** | **+37** |
| Test automatizzati | 631 | **1484** | **+853 (+135%)** |
| Aritmetica pura nella simulazione | 0% | **15%** | **+15pp** |
| Meta-formato nella simulazione | 0% | **10%** | **+10pp** |
| Realismo simulazione | 7.5/10 | **8.5/10** | **+1.0** |
| Tipi in simulazione esame | 15 (incl. non-TOLC) | **12** (solo realistici) | Pulizia: rimossi 4 tipi pedagogici |

### 10.10 Conclusione Assessment v4

**L'app è ora un ottimo strumento di preparazione TOLC-B per la sezione Matematica.**

- **Copertura**: 87.5% delle domande reali TOLC-B coperte direttamente (era 67.5%). Solo 1 domanda su 40 completamente non coperta (parabola, priorità bassa).
- **Simulazione**: distribuzione pesi allineata al TOLC reale entro ±5%. Meta-formato e aritmetica pura ora presenti. Tipi pedagogici (trap, always_true, proportional, cross_topic) mantenuti in modalità apprendimento ma esclusi dalla simulazione esame.
- **Qualità**: 1484 test automatizzati garantiscono stabilità. 17 moduli con ~175 template offrono varietà sufficiente.
- **Gap residui**: 3 domande parziali/mancanti su casi rari (parabola, tangente esterna specifica, sviluppo cono). ROI insufficiente per implementazione dedicata.

**Raccomandazioni post-v4**:
1. **Varietà template** (priorità alta): aumentare template per tipo per ridurre ripetitività
2. **Difficoltà adattiva** (TOLC-45): tracciare performance studente e adattare livello
3. **Time management** (TOLC-46): allenamento gestione tempo con feedback
4. **Validazione reale**: testare con 5-10 studenti TOLC-B per feedback qualitativo

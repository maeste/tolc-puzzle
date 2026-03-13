# Analisi Critica di Copertura TOLC-B

> **Documento di tracciamento** — da aggiornare man mano che le lacune vengono risolte.
> Ultima revisione strutturale: 2026-03-12 (rivalutazione v2 post-TOLC-25→29)

---

## 1. Panoramica

Il TOLC-B Puzzle copre **tutte le 8 macro-aree** del syllabus CISIA per la sezione Matematica del TOLC-B, per un totale di **51 argomenti** (di cui 4 EXTRA non richiesti dal syllabus base). Tutte le lacune identificate nell'analisi iniziale sono state risolte. Implementazioni recenti (TOLC-25→29): grafici SVG nella simulazione esame, distribuzione pesata domande, geometria solida/volumi, potenze con esponente razionale, word problems con risultato numerico. **127 template** distribuiti su 15 moduli, **631 test** automatizzati.

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

### 2.3 Geometria Euclidea

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Proprietà angoli | Geometry Sherlock (tipo F) | **COPERTO** | |
| Triangoli | Geometry Sherlock (tipo F) | **COPERTO** | |
| Cerchi | Geometry Sherlock (tipo F) | **COPERTO** | |
| Poligoni | Geometry Sherlock (tipo F) | **COPERTO** | |
| Aree e perimetri | Geometry Sherlock (tipo F) | **COPERTO** | |
| Geometria solida / Volumi | Geometry Sherlock (tipo F) | **IMPLEMENTATO** | 7 template: cilindro, cono, sfera, prisma, piramide, compositi (cilindro+cono, sfera inscritta) — SVG 3D — 2026-03-12 |

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
| IMPLEMENTATO | 27 | 40% |
| PARZIALE | 0 | 0% |
| ASSENTE | 0 | 0% |
| EXTRA | 4 | — |

**Copertura effettiva syllabus**: **100%** (57/57 argomenti coperti o implementati, esclusi 4 EXTRA)

### Inventario Template (127 totali)

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
| **Totale** | | **44** | **49** | **45** | **138** |

*Nota: 88 template con pattern _t#, più template aggiuntivi in moduli senza naming convention _t# (graph_reader, word_modeler, trap_calculator, logic_puzzle, probability_game, estimation_blitz).*

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

| Metrica | Baseline | Post R1-R9 | Post R10-R14 (attuale) |
|---------|----------|------------|------------------------|
| Argomenti coperti | 34/49 (69%) | 49/49 (100%) | 51/51 (100%) |
| Macro-aree complete | 4/8 (50%) | 8/8 (100%) | 8/8 (100%) |
| Moduli esercizi | 9 | 11 | 11 |
| Template totali | ~70 | ~80 | **88** (conteggio esatto) |
| Test automatizzati | — | 171 | **442** |
| Simulazione: distribuzione | uniforme | uniforme | **pesata TOLC-B** |
| Simulazione: grafici SVG | no | no | **4 domande su 20** |
| Simulazione: competenze cognitive | no | no | **5 domande su 20** (semplificazione, sempre/mai vero, proporzionale, 2 cross-topic) |

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

# Analisi Critica di Copertura TOLC-B

> **Documento di tracciamento** — da aggiornare man mano che le lacune vengono risolte.
> Ultima revisione strutturale: 2026-03-12 (rivalutazione post-implementazione)

---

## 1. Panoramica

Il TOLC-B Puzzle copre **tutte le 8 macro-aree** del syllabus CISIA per la sezione Matematica del TOLC-B, per un totale di **49 argomenti** (di cui 4 EXTRA non richiesti dal syllabus base). Tutte le lacune identificate nell'analisi iniziale sono state risolte: Geometria Analitica (nuovo modulo dedicato), Disequazioni (nuovo modulo dedicato), Statistica (aggiunti template lettura grafici), Funzioni (iniettività/invertibilità), Logica (notazione insiemistica) e Algebra (MCD/mcm).

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
| Logaritmi e proprietà | Trap Calculator (tipo A) | **COPERTO** | Trappole su proprietà logaritmiche |
| Potenze e radicali | Trap Calculator (tipo A) + Estimation Blitz (tipo G) | **COPERTO** | |

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
| Problemi a più variabili | Word Modeler (tipo B) | **COPERTO** | Livelli 2 e 3 |
| Stima e calcolo mentale | Estimation Blitz (tipo G) | **COPERTO** | 3 livelli con timer |

---

## 3. Riepilogo Quantitativo

| Stato | Conteggio | Percentuale |
|-------|-----------|-------------|
| COPERTO | 34 | 69% |
| IMPLEMENTATO | 15 | 31% |
| PARZIALE | 0 | 0% |
| ASSENTE | 0 | 0% |
| EXTRA | 4 | — |

**Copertura effettiva syllabus**: **100%** (49/49 argomenti coperti o implementati, esclusi 4 EXTRA)

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

### Bassa Priorità

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

---

## 6. Note per l'Implementatore

1. **Dopo ogni implementazione**: aggiornare la tabella di copertura (§2) cambiando lo stato da ASSENTE/PARZIALE a IMPLEMENTATO, spuntare la checkbox in §4, e aggiungere una riga al Registro Modifiche (§5).
2. **Contenuti EXTRA**: non rimuoverli, ma contrassegnarli nell'UI come "Approfondimento" per evitare confusione con il syllabus base.
3. **File di riferimento**: `exercises/` contiene tutti i moduli, `app.py` contiene il registry degli esercizi e le route API.
4. **Testing**: ogni nuovo template deve essere testabile via `pytest` e generare almeno 3 varianti distinte senza errori.

---

## 7. Confronto Copertura Pre/Post Implementazione

> Rivalutazione eseguita il 2026-03-12 dopo il completamento di tutti i task del milestone "TOLC-B Coverage Alignment" (TOLC-13 → TOLC-21).

### 7.1 Tabella Comparativa per Macro-Area

| Macro-area | Argomenti | Coperti Prima | Coperti Dopo | Delta |
|------------|-----------|---------------|--------------|-------|
| 2.1 Algebra e Aritmetica | 12 | 8 | 12 | **+4** |
| 2.2 Funzioni | 7 | 5 | 7 | **+2** |
| 2.3 Geometria Euclidea | 5 | 5 | 5 | 0 |
| 2.4 Geometria Analitica | 7 | 0 | 7 | **+7** |
| 2.5 Logica e Insiemi | 5 | 4 | 5 | **+1** |
| 2.6 Probabilita e Combinatorica | 6 | 6 | 6 | 0 |
| 2.7 Statistica (syllabus) | 4 | 3 | 4 | **+1** |
| 2.8 Modellizzazione e Problem Solving | 3 | 3 | 3 | 0 |
| **Totale** | **49** | **34** | **49** | **+15** |

### 7.2 Percentuali Aggregate

| Metrica | Prima | Dopo |
|---------|-------|------|
| Argomenti coperti (COPERTO + IMPLEMENTATO) | 34/49 (69%) | 49/49 (100%) |
| Macro-aree con copertura completa | 4/8 (50%) | 8/8 (100%) |
| Argomenti ASSENTE | 15 | 0 |
| Argomenti PARZIALE | 0 | 0 |
| Moduli esercizi totali | 9 | 11 |
| Template totali (stima) | ~80 | ~130+ |

> **Nota**: il conteggio pre-implementazione (34 coperti su 49) differisce dal baseline originale (28 su 42) perche la tabella di tracciamento e stata espansa durante l'implementazione, aggiungendo argomenti precedentemente non elencati individualmente (es. i 7 argomenti di Geometria Analitica non erano enumerati nella tabella originale).

### 7.3 Argomenti Ancora Scoperti

**Nessun argomento del syllabus TOLC-B Matematica risulta scoperto.**

I 4 contenuti **EXTRA** (Varianza, Deviazione standard, Quartili/percentili, Outlier detection) restano presenti nel modulo Statistica ma sono marcati come "Approfondimento" (livello L3) per distinguerli dal syllabus base. Non sono stati rimossi perche utili per studenti che vogliono approfondire.

Le sezioni TOLC-B **non coperte dall'app** (Biologia, Chimica, Fisica, Comprensione del testo) sono segnalate tramite un banner informativo nella dashboard con link alle risorse CISIA (R7).

### 7.4 Valutazione Qualitativa

**Miglioramenti principali:**

1. **Completezza**: la copertura e passata dal 69% al 100% del syllabus Matematica, eliminando tutte le lacune identificate.

2. **Nuovi moduli**: sono stati creati 2 moduli completamente nuovi:
   - `exercises/analytic_geometry.py` (9 template su 3 livelli): rette, distanze, punti medi, parallele/perpendicolari, asse del segmento, circonferenze, intersezioni retta-circonferenza.
   - `exercises/inequalities.py` (7 template su 3 livelli): disequazioni di 1° e 2° grado (con gestione completa di Delta>0, Delta=0, Delta<0), razionali con studio del segno, sistemi. Risposte in notazione intervallare.

3. **Arricchimento moduli esistenti**:
   - Graph Reader: +4 template (iniettivita, invertibilita, codominio, intervalli di iniettivita)
   - Logic Puzzle: +7 template (notazione insiemistica completa con operazioni, Venn 2/3 insiemi)
   - Solve Exercise: +7 template (MCD/mcm con scomposizione in fattori primi, problemi applicativi)
   - Statistics Exercise: +3 template (lettura istogrammi, torte, barre) + riorganizzazione livelli
   - Word Modeler: +8 template (contesti italiani realistici: supermercato, treno, bolletta, etc.)

4. **Esperienza utente**:
   - Banner informativo CISIA per sezioni non coperte (R7)
   - Modalita Esame Realistico con formato diretto TOLC-B: 20 domande, 5 opzioni A-E, punteggio +1/0/-0.25, timer 50 min (R8)

5. **Qualita**: 171 test automatizzati coprono tutti i nuovi template, verificando generazione corretta e variabilita.

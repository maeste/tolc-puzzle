# Analisi Critica di Copertura TOLC-B

> **Documento di tracciamento** — da aggiornare man mano che le lacune vengono risolte.
> Ultima revisione strutturale: 2026-03-12

---

## 1. Panoramica

Il TOLC-B Puzzle copre **7 delle 9 macro-aree** del syllabus CISIA per la sezione Matematica del TOLC-B. Le lacune principali riguardano **Geometria Analitica** (assente come modulo dedicato), **Disequazioni** (presenti solo in forma basilare in Solve Exercise) e **Statistica** (contenuti extra rispetto al syllabus, mancano lettura grafici).

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
| Disequazioni 1° grado | Solve Exercise (tipo H) | **PARZIALE** | Solo ax + b > c, manca formato completo |
| Disequazioni 2° grado | — | **ASSENTE** | Da implementare |
| Disequazioni razionali | — | **ASSENTE** | Da implementare |
| MCD e mcm | — | **ASSENTE** | Da aggiungere in Solve Exercise |
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
| Iniettività | — | **ASSENTE** | Da aggiungere in Graph Reader |
| Invertibilità | — | **ASSENTE** | Da aggiungere in Graph Reader |

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
| Equazione della retta | — | **ASSENTE** | Nessun modulo dedicato |
| Distanza tra punti | — | **ASSENTE** | |
| Punto medio | — | **ASSENTE** | |
| Rette parallele e perpendicolari | — | **ASSENTE** | |
| Equazione della circonferenza | — | **ASSENTE** | |
| Asse di un segmento | — | **ASSENTE** | |
| Intersezione retta-circonferenza | — | **ASSENTE** | |

### 2.5 Logica e Insiemi

| Argomento Syllabus | Modulo Attuale | Stato | Note |
|---------------------|----------------|-------|------|
| Negazione proposizioni | Logic Puzzle (tipo D) | **COPERTO** | ¬(∀x P(x)) = ∃x ¬P(x) |
| Quantificatori | Logic Puzzle (tipo D) | **COPERTO** | Universale ed esistenziale |
| Implicazioni | Logic Puzzle (tipo D) | **COPERTO** | |
| Deduzione logica | Logic Puzzle (tipo D) | **COPERTO** | |
| Notazione insiemistica | — | **ASSENTE** | ∈, ⊂, ∪, ∩, complemento |

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
| Lettura grafici (istogrammi, torte) | — | **ASSENTE** | Il TOLC-B chiede interpretazione visiva |
| Varianza | Statistics Exercise (tipo I) | **EXTRA** | Non richiesta esplicitamente dal syllabus base |
| Deviazione standard | Statistics Exercise (tipo I) | **EXTRA** | Non richiesta esplicitamente dal syllabus base |
| Quartili e percentili | Statistics Exercise (tipo I) | **EXTRA** | Non richiesti dal syllabus base |
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
| COPERTO | 28 | 68% |
| PARZIALE | 1 | 2% |
| ASSENTE | 13 | 32% |
| EXTRA | 4 | — |

**Copertura effettiva syllabus**: ~70% (28/41 argomenti coperti o parziali)

---

## 4. Raccomandazioni e Tracciamento

### Alta Priorità

- [ ] **R1 — Modulo Geometria Analitica**: Creare nuovo tipo di esercizio o estendere Geometry Sherlock con: equazione retta, distanza punti, punto medio, parallele/perpendicolari, circonferenza, asse segmento, intersezione retta-circonferenza
- [ ] **R2 — Modulo Disequazioni**: Aggiungere in Solve Exercise o come modulo separato: disequazioni 1° grado complete, 2° grado, razionali (con studio del segno)
- [ ] **R3 — Riallineamento Statistica**: Aggiungere lettura/interpretazione grafici (istogrammi, grafici a torta); segnalare contenuti extra come "approfondimento" nell'UI

### Media Priorità

- [ ] **R4 — Iniettività e invertibilità funzioni**: Aggiungere template in Graph Reader per riconoscere funzioni iniettive, suriettive, invertibili da grafico
- [ ] **R5 — Notazione insiemistica**: Aggiungere esercizi su ∈, ⊂, ∪, ∩, complemento nel modulo Logic Puzzle
- [ ] **R6 — MCD e mcm**: Aggiungere template in Solve Exercise per calcolo MCD e mcm

### Bassa Priorità

- [ ] **R7 — Avviso complementarità**: Aggiungere banner/sezione nell'app che spiega cosa il puzzle NON copre (Biologia, Chimica, Fisica) con link a risorse CISIA
- [ ] **R8 — Modo esame realistico**: Aggiungere modalità con domande in formato diretto TOLC (non mini-gioco) per familiarizzare con il formato reale
- [ ] **R9 — Contestualizzazione problemi**: Migliorare i word problem con contesti più realistici e vicini al formato TOLC-B

---

## 5. Registro Modifiche

> L'implementatore deve aggiornare questa sezione ogni volta che risolve una raccomandazione.

| Data | Raccomandazione | Descrizione Modifica | Autore |
|------|----------------|----------------------|--------|
| — | — | _Nessuna modifica ancora registrata_ | — |

---

## 6. Note per l'Implementatore

1. **Dopo ogni implementazione**: aggiornare la tabella di copertura (§2) cambiando lo stato da ASSENTE/PARZIALE a IMPLEMENTATO, spuntare la checkbox in §4, e aggiungere una riga al Registro Modifiche (§5).
2. **Contenuti EXTRA**: non rimuoverli, ma contrassegnarli nell'UI come "Approfondimento" per evitare confusione con il syllabus base.
3. **File di riferimento**: `exercises/` contiene tutti i moduli, `app.py` contiene il registry degli esercizi e le route API.
4. **Testing**: ogni nuovo template deve essere testabile via `pytest` e generare almeno 3 varianti distinte senza errori.

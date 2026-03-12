# TOLC Puzzle - Math Mindset Trainer

Applicazione web per prepararsi alla sezione di matematica del **TOLC-B** attraverso mini-giochi interattivi.

## Panoramica

7 tipologie di esercizi che allenano competenze diverse, 3 modalita timer e una simulazione completa d'esame.

| Mini-gioco | Tipo | Cosa allena |
|---|---|---|
| Trova la Trappola | A | Individuare errori nei calcoli |
| Traduci la Storia | B | Tradurre problemi in equazioni |
| Che Funzione Sono? | C | Associare funzioni e grafici |
| Detective Logico | D | Logica formale e implicazioni |
| Probabilita Visuale | E | Spazi campionari e probabilita |
| Sherlock Geometrico | F | Proprieta geometriche |
| Stima Flash | G | Ordini di grandezza e stima rapida |

### Modalita timer

- **Zen** — nessun timer, feedback immediato con spiegazione
- **Rilassato** — 4 min/domanda, barra colorata morbida
- **Esame** — 2.5 min/domanda, pressione visiva con barra rossa

### Simulazione TOLC-B

20 domande miste, 50 minuti, scoring reale (+1 corretta, 0 non data, -0.25 sbagliata) con report finale.

## Requisiti

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) (consigliato) oppure pip

## Installazione e avvio

### Con uv (consigliato)

```bash
# Clona il repo
git clone <repo-url>
cd tolc-puzzle

# Installa dipendenze e avvia
uv run flask --app app run --debug
```

### Con pip

```bash
cd tolc-puzzle
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -e .
flask --app app run --debug
```

Apri il browser su **http://localhost:5000**.

## Struttura del progetto

```
tolc-puzzle/
├── app.py                          # Flask app, route, registry esercizi
├── pyproject.toml                  # Metadati progetto e dipendenze
├── exercises/
│   ├── base.py                     # Classe astratta Exercise
│   ├── trap_calculator.py          # Tipo A — Trova la Trappola
│   ├── word_modeler.py             # Tipo B — Traduci la Storia
│   ├── graph_reader.py             # Tipo C — Che Funzione Sono?
│   ├── logic_puzzle.py             # Tipo D — Detective Logico
│   ├── probability_game.py         # Tipo E — Probabilita Visuale
│   ├── geometry_sherlock.py        # Tipo F — Sherlock Geometrico
│   └── estimation_blitz.py         # Tipo G — Stima Flash
├── templates/
│   ├── base.html                   # Layout principale
│   ├── dashboard.html              # Dashboard con card esercizi
│   ├── exercise.html               # Pagina esercizio singolo
│   ├── results.html                # Pagina progressi
│   ├── simulation.html             # Simulazione TOLC-B
│   └── 404.html                    # Pagina errore
└── static/
    ├── css/style.css               # Stili
    └── js/
        ├── app.js                  # Storage, Timer, logica dashboard
        ├── exercise.js             # Rendering esercizi e timer
        ├── results.js              # Pagina risultati
        └── simulation.js           # Logica simulazione TOLC-B
```

## API

| Endpoint | Metodo | Descrizione |
|---|---|---|
| `/api/exercise/<tipo>?difficulty=1-3` | GET | Genera un esercizio |
| `/api/check` | POST | Verifica risposta (`{type, answer, exercise}`) |
| `/api/types` | GET | Metadata tipi esercizio |
| `/api/simulation/exercises` | GET | 20 esercizi misti per simulazione |

## Aggiungere un nuovo esercizio

1. Crea `exercises/nuovo_esercizio.py` con una classe che eredita da `Exercise`
2. Implementa `generate(self, difficulty: int) -> dict` che ritorna:
   ```python
   {
       "question": str,
       "options": list[str],      # 4 opzioni (oppure "steps" per esercizi tipo trappola)
       "correct_index": int,
       "explanation": str,
       "did_you_know": str,
   }
   ```
3. In `app.py` aggiungi import, `register_exercise("chiave", NuovaClasse)` e voce in `EXERCISE_TYPES`

## Persistenza dati

I progressi sono salvati nel **localStorage** del browser (chiave `tolc_progress`). Non serve database.

## Licenza

MIT

import random

from exercises.base import Exercise


# --- Word pools for parametric variety ---
# Each entry is (plural, singular) to avoid broken Italian singularization.
_SOGGETTI = [
    ("gatti", "gatto"), ("cani", "cane"), ("studenti", "studente"),
    ("fiori", "fiore"), ("libri", "libro"), ("uccelli", "uccello"),
    ("pesci", "pesce"), ("alberi", "albero"), ("pianeti", "pianeta"),
    ("numeri", "numero"),
]
_PROPRIETA = [
    ("neri", "nero"), ("veloci", "veloce"), ("grandi", "grande"),
    ("piccoli", "piccolo"), ("rossi", "rosso"), ("intelligenti", "intelligente"),
    ("antichi", "antico"), ("rari", "raro"), ("pesanti", "pesante"),
    ("colorati", "colorato"),
]
_NOMI = ["Marco", "Luca", "Sara", "Giulia", "Andrea", "Elena", "Giovanni", "Chiara", "Paolo", "Anna"]
_CITTA = ["Roma", "Milano", "Napoli", "Torino", "Firenze", "Bologna", "Venezia", "Palermo", "Genova", "Bari"]
_MATERIE = ["matematica", "fisica", "chimica", "storia", "filosofia", "biologia", "informatica", "letteratura"]
_EVENTI_CAUSA = [
    ("piove", "il terreno e' bagnato"),
    ("nevica", "le strade sono ghiacciate"),
    ("studio", "supero l'esame"),
    ("mi alleno", "miglioro le prestazioni"),
    ("leggo molto", "amplio il mio vocabolario"),
    ("dormo bene", "sono riposato"),
    ("mangio sano", "sto in salute"),
    ("pratico sport", "sono in forma"),
]
_INSIEMI_AB = [
    ("studenti di matematica", "studenti di fisica"),
    ("atleti", "nuotatori"),
    ("musicisti", "pianisti"),
    ("medici", "chirurghi"),
    ("europei", "italiani"),
    ("mammiferi", "balene"),
    ("poligoni", "rettangoli"),
    ("numeri pari", "multipli di 4"),
]


def _pick(pool, n=1, exclude=None):
    available = [x for x in pool if x != exclude] if exclude else list(pool)
    if n == 1:
        return random.choice(available)
    return random.sample(available, min(n, len(available)))


def _pick_subj_prop():
    """Return (plural_subj, singular_subj, plural_prop, singular_prop)."""
    s_pl, s_sg = _pick(_SOGGETTI)
    p_pl, p_sg = _pick(_PROPRIETA)
    return s_pl, s_sg, p_pl, p_sg


class LogicPuzzle(Exercise):
    """Detective Logico -- formal logic puzzles."""

    @staticmethod
    def _build_result(question, correct, distractors, explanation, tip, difficulty):
        options = [correct] + distractors
        correct_index = 0
        options, correct_index = Exercise.shuffle_options(options, correct_index)
        return {
            "question": question,
            "options": options,
            "correct_index": correct_index,
            "explanation": explanation,
            "did_you_know": tip,
            "difficulty": difficulty,
        }

    # ================================================================
    #  LEVEL 1: Simple propositions, basic negation
    # ================================================================

    @staticmethod
    def _negation_all():
        """Negation of 'tutti i S sono P'."""
        s_pl, s_sg, p_pl, p_sg = _pick_subj_prop()
        question = (
            f"La negazione di 'Tutti i {s_pl} sono {p_pl}' e':"
        )
        correct = f"Esiste almeno un {s_sg} che non e' {p_sg}"
        d1 = f"Nessun {s_sg} e' {p_sg}"
        d2 = f"Tutti i {s_pl} non sono {p_pl}"
        d3 = f"Alcuni {s_pl} sono {p_pl}"
        d4 = f"Almeno un {s_sg} e' {p_sg}"
        explanation = (
            f"La negazione di 'Tutti i {s_pl} sono {p_pl}' (cioe' di una proposizione universale affermativa, "
            f"del tipo per ogni x, P(x)) e' 'Esiste almeno un x tale che NON P(x)'. "
            f"Non e' 'Nessuno e' P' (quella e' la contraria, non la negazione). "
            f"Non e' 'Tutti non sono P' (equivale a 'nessuno', che e' troppo forte)."
        )
        tip = "La negazione di 'per ogni' (tutti) e' 'esiste almeno uno che non'. Ricorda: neg(forall) = exists NOT."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _negation_none():
        """Negation of 'nessun S e' P'."""
        s_pl, s_sg, p_pl, p_sg = _pick_subj_prop()
        question = (
            f"La negazione di 'Nessun {s_sg} e' {p_sg}' e':"
        )
        correct = f"Esiste almeno un {s_sg} che e' {p_sg}"
        d1 = f"Tutti i {s_pl} sono {p_pl}"
        d2 = f"Nessun {s_sg} non e' {p_sg}"
        d3 = f"Alcuni {s_pl} non sono {p_pl}"
        d4 = f"Alcuni {s_pl} non sono {p_pl}"
        # d4 uses slightly different phrasing to avoid exact duplicate
        d4 = f"Non tutti i {s_pl} sono {p_pl}"
        explanation = (
            f"'Nessun {s_sg} e' {p_sg}' equivale a 'Per ogni x, x NON e' {p_sg}'. "
            f"La negazione e' 'Esiste almeno un x che E' {p_sg}'. "
            f"Attenzione: 'Tutti sono {p_pl}' e' la contraria, non la semplice negazione."
        )
        tip = "'Nessuno e' P' equivale a 'Tutti non sono P'. La negazione diventa 'Almeno uno e' P'."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _negation_some():
        """Negation of 'alcuni S sono P'."""
        s_pl, s_sg, p_pl, p_sg = _pick_subj_prop()
        question = (
            f"La negazione di 'Alcuni {s_pl} sono {p_pl}' e':"
        )
        correct = f"Nessun {s_sg} e' {p_sg}"
        d1 = f"Tutti i {s_pl} sono {p_pl}"
        d2 = f"Alcuni {s_pl} non sono {p_pl}"
        d3 = f"Esiste almeno un {s_sg} che e' {p_sg}"
        d4 = f"Esiste almeno un {s_sg} che non e' {p_sg}"
        explanation = (
            f"'Alcuni {s_pl} sono {p_pl}' equivale a 'Esiste almeno un x tale che P(x)'. "
            f"La negazione e' 'Per ogni x, NON P(x)', cioe' 'Nessun {s_sg} e' {p_sg}'. "
            f"neg(exists P) = forall NOT P."
        )
        tip = "La negazione di 'esiste almeno uno' (alcuni) e' 'nessuno'. Ricorda: neg(exists) = forall NOT."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _negation_simple_and():
        """Negation of 'A e B' (De Morgan)."""
        nome1, nome2 = _pick(_NOMI, 2)
        materia1, materia2 = _pick(_MATERIE, 2)
        question = (
            f"La negazione di '{nome1} studia {materia1} E {nome2} studia {materia2}' e':"
        )
        correct = f"{nome1} non studia {materia1} OPPURE {nome2} non studia {materia2}"
        d1 = f"{nome1} non studia {materia1} E {nome2} non studia {materia2}"
        d2 = f"{nome1} studia {materia1} OPPURE {nome2} studia {materia2}"
        d3 = f"Ne' {nome1} studia {materia1} ne' {nome2} studia {materia2}"
        d4 = f"{nome1} studia {materia1} E {nome2} non studia {materia2}"
        explanation = (
            f"Per le leggi di De Morgan, la negazione di 'A E B' e' 'NON A OPPURE NON B'. "
            f"Non e' 'NON A E NON B' (quella e' la negazione di 'A OPPURE B'). "
            f"Basta che UNA delle due condizioni sia falsa perche' la congiunzione sia falsa."
        )
        tip = "Leggi di De Morgan: neg(A AND B) = (NOT A) OR (NOT B); neg(A OR B) = (NOT A) AND (NOT B)."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _negation_simple_or():
        """Negation of 'A o B' (De Morgan)."""
        nome1, nome2 = _pick(_NOMI, 2)
        citta1, citta2 = _pick(_CITTA, 2)
        question = (
            f"La negazione di '{nome1} va a {citta1} OPPURE {nome2} va a {citta2}' e':"
        )
        correct = f"{nome1} non va a {citta1} E {nome2} non va a {citta2}"
        d1 = f"{nome1} non va a {citta1} OPPURE {nome2} non va a {citta2}"
        d2 = f"{nome1} va a {citta1} E {nome2} va a {citta2}"
        d3 = f"Ne' {nome1} va a {citta1} ne' {nome2} non va a {citta2}"
        d4 = f"{nome1} va a {citta1} E {nome2} non va a {citta2}"
        explanation = (
            f"Per le leggi di De Morgan, la negazione di 'A OPPURE B' e' 'NON A E NON B'. "
            f"Entrambe le condizioni devono essere false perche' la disgiunzione sia falsa."
        )
        tip = "Leggi di De Morgan: neg(A OR B) = (NOT A) AND (NOT B). Serve che entrambe siano false."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  LEVEL 2: Quantifiers, contrapositive
    # ================================================================

    @staticmethod
    def _contrapositive():
        """Find the contrapositive of an implication."""
        causa, effetto = _pick(_EVENTI_CAUSA)
        question = (
            f"Data l'implicazione 'Se {causa}, allora {effetto}', "
            f"qual e' la sua contropositiva?"
        )
        correct = f"Se non {effetto}, allora non {causa}"
        d1 = f"Se {effetto}, allora {causa}"
        d2 = f"Se non {causa}, allora non {effetto}"
        d3 = f"Se {causa}, allora non {effetto}"
        d4 = f"{causa} se e solo se {effetto}"
        explanation = (
            f"La contropositiva di 'Se A allora B' e' 'Se NON B allora NON A'. "
            f"Sono logicamente equivalenti. "
            f"'Se B allora A' e' l'inversa (non equivalente). "
            f"'Se NON A allora NON B' e' l'inversa della contropositiva (non equivalente)."
        )
        tip = "La contropositiva di 'A => B' e' 'NOT B => NOT A' ed e' SEMPRE equivalente all'originale."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _equivalent_implication():
        """Which statement is equivalent to an implication."""
        causa, effetto = _pick(_EVENTI_CAUSA)
        question = (
            f"L'affermazione 'Se {causa}, allora {effetto}' e' equivalente a:"
        )
        correct = f"Se non {effetto}, allora non {causa}"
        d1 = f"Se {effetto}, allora {causa}"
        d2 = f"Se non {causa}, allora non {effetto}"
        d3 = f"{causa} se e solo se {effetto}"
        d4 = f"Se non {causa}, allora {effetto}"
        explanation = (
            f"Un'implicazione 'Se A allora B' e' equivalente SOLO alla sua contropositiva 'Se NON B allora NON A'. "
            f"L'inversa 'Se B allora A' e la negazione dell'antecedente 'Se NON A allora NON B' "
            f"NON sono equivalenti. Il bicondizionale richiede entrambe le direzioni."
        )
        tip = "Un'implicazione ha 4 forme: originale (A=>B), inversa (B=>A), contraria (notA=>notB), contropositiva (notB=>notA). Solo originale e contropositiva sono equivalenti."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _necessary_condition():
        """Identify a necessary condition."""
        causa, effetto = _pick(_EVENTI_CAUSA)
        question = (
            f"Se '{causa}' e' condizione sufficiente per '{effetto}', "
            f"quale affermazione e' corretta?"
        )
        correct = f"'{effetto}' e' condizione necessaria per '{causa}'"
        d1 = f"'{causa}' e' condizione necessaria per '{effetto}'"
        d2 = f"'{effetto}' e' condizione sufficiente per '{causa}'"
        d3 = f"'{causa}' e' condizione necessaria e sufficiente per '{effetto}'"
        d4 = f"'{causa}' e' equivalente a '{effetto}'"
        explanation = (
            f"Se A e' condizione sufficiente per B (cioe' A => B), "
            f"allora B e' condizione necessaria per A. "
            f"Sufficiente = 'basta A per avere B'. Necessaria = 'senza B non puo' esserci A'. "
            f"Dalla contropositiva: NOT B => NOT A, cioe' senza B non c'e' A."
        )
        tip = "Se A e' sufficiente per B, allora B e' necessaria per A. Pensa alla contropositiva: NOT B => NOT A."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _sufficient_condition():
        """Identify what follows from a sufficient condition."""
        causa, effetto = _pick(_EVENTI_CAUSA)
        nome = _pick(_NOMI)
        question = (
            f"Sappiamo che 'Se {causa}, allora {effetto}'. "
            f"{nome} {causa}. Cosa possiamo concludere?"
        )
        correct = f"{effetto}"
        d1 = f"Non {effetto}"
        d2 = f"Non {causa}"
        d3 = f"Non possiamo concludere nulla"
        d4 = f"{causa} e {effetto} sono indipendenti"
        explanation = (
            f"Abbiamo 'Se A allora B' e sappiamo che A e' vero. "
            f"Per il Modus Ponens, possiamo concludere B: '{effetto}'. "
            f"Il Modus Ponens e' la regola fondamentale: se A => B e A e' vero, allora B e' vero."
        )
        tip = "Modus Ponens: da 'Se A allora B' e 'A vero' si deduce 'B vero'. E' la regola base della logica."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _negation_universal_quantifier():
        """Negation with universal quantifier in formal notation."""
        s_pl, s_sg, p_pl, p_sg = _pick_subj_prop()
        question = (
            f"La proposizione 'Per ogni x appartenente all'insieme dei {s_pl}, x e' {p_sg}' "
            f"si nega come:"
        )
        correct = f"Esiste almeno un x nell'insieme dei {s_pl} tale che x NON e' {p_sg}"
        d1 = f"Per ogni x nell'insieme dei {s_pl}, x NON e' {p_sg}"
        d2 = f"Non esiste x nell'insieme dei {s_pl} tale che x e' {p_sg}"
        d3 = f"Per ogni x fuori dall'insieme dei {s_pl}, x e' {p_sg}"
        d4 = f"Esiste almeno un x fuori dall'insieme dei {s_pl} tale che x e' {p_sg}"
        explanation = (
            f"La negazione del quantificatore universale (per ogni, simbolo: forall) diventa "
            f"il quantificatore esistenziale (esiste, simbolo: exists) con la proposizione negata. "
            f"neg(forall x, P(x)) = exists x, NOT P(x)."
        )
        tip = "Regola fondamentale: neg(forall x P(x)) = exists x NOT P(x). Il quantificatore si 'ribalta' e la proprieta' si nega."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _modus_tollens():
        """Apply modus tollens."""
        causa, effetto = _pick(_EVENTI_CAUSA)
        nome = _pick(_NOMI)
        question = (
            f"Sappiamo che 'Se {causa}, allora {effetto}'. "
            f"Osserviamo che {nome} non {effetto}. Cosa possiamo concludere?"
        )
        correct = f"{nome} non {causa}"
        d1 = f"{nome} {causa}"
        d2 = f"Non possiamo concludere nulla"
        d3 = f"{nome} {effetto}"
        d4 = f"{nome} potrebbe o non potrebbe {causa}"
        explanation = (
            f"Abbiamo 'Se A allora B' e sappiamo che B e' falso (NOT B). "
            f"Per il Modus Tollens (equivalente alla contropositiva), da NOT B deduciamo NOT A. "
            f"Quindi: '{nome} non {causa}'."
        )
        tip = "Modus Tollens: da 'Se A allora B' e 'NOT B' si deduce 'NOT A'. E' la contropositiva applicata."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  LEVEL 3: Logical chains, combined quantifiers
    # ================================================================

    @staticmethod
    def _implication_chain():
        """Transitivity of implications: A->B, B->C, therefore A->C."""
        e1, e2, e3 = _pick(_EVENTI_CAUSA, 3)
        causa1, effetto1 = e1
        _causa2, effetto2 = e2
        # Build chain: causa1 -> effetto1, effetto1 -> effetto2
        question = (
            f"Sappiamo che:\n"
            f"1) Se {causa1}, allora {effetto1}\n"
            f"2) Se {effetto1}, allora {effetto2}\n"
            f"Cosa possiamo concludere?"
        )
        correct = f"Se {causa1}, allora {effetto2}"
        d1 = f"Se {effetto2}, allora {causa1}"
        d2 = f"Se non {causa1}, allora non {effetto2}"
        d3 = f"Se {effetto1}, allora {causa1}"
        d4 = f"{causa1} se e solo se {effetto2}"
        explanation = (
            f"Per la transitivita' dell'implicazione: se A => B e B => C, allora A => C. "
            f"Questa e' la regola del sillogismo ipotetico. "
            f"L'inversa (C => A) NON e' valida. "
            f"'Se NOT A allora NOT C' e' l'inversa della contropositiva, non e' valida."
        )
        tip = "Sillogismo ipotetico: da A=>B e B=>C si deduce A=>C. La catena di implicazioni si 'comprime'."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _chain_with_modus_ponens():
        """Chain of implications with a known fact."""
        e1, e2 = _pick(_EVENTI_CAUSA, 2)
        causa1, effetto1 = e1
        _causa2, effetto2 = e2
        nome = _pick(_NOMI)
        question = (
            f"Sappiamo che:\n"
            f"1) Se {causa1}, allora {effetto1}\n"
            f"2) Se {effetto1}, allora {effetto2}\n"
            f"3) {nome} {causa1}\n"
            f"Cosa possiamo concludere su {nome}?"
        )
        correct = f"{nome} {effetto2} (e anche {effetto1})"
        d1 = f"Solo che {nome} {effetto1}"
        d2 = f"Non possiamo concludere nulla su {effetto2}"
        d3 = f"{nome} non {effetto2}"
        d4 = f"Solo che {nome} {causa1}"
        explanation = (
            f"Applicando il Modus Ponens alla premessa 1 con il fatto 3: {nome} {causa1} => {nome} {effetto1}. "
            f"Poi applicando il Modus Ponens alla premessa 2: {nome} {effetto1} => {nome} {effetto2}. "
            f"Quindi possiamo concludere sia {effetto1} che {effetto2}."
        )
        tip = "In una catena di implicazioni, il Modus Ponens si applica ripetutamente: ogni conclusione diventa premessa per il passo successivo."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _combined_quantifiers():
        """Negation of combined quantifier statement."""
        s1_pl, s1_sg, _p1_pl, _p1_sg = _pick_subj_prop()
        s2_pl, s2_sg, p2_pl, p2_sg = _pick_subj_prop()
        # Avoid same subject
        while s2_pl == s1_pl:
            s2_pl, s2_sg, p2_pl, p2_sg = _pick_subj_prop()
        question = (
            f"La negazione di 'Per ogni {s1_sg} esiste almeno un "
            f"{s2_sg} che e' {p2_sg}' e':"
        )
        correct = (
            f"Esiste almeno un {s1_sg} tale che per ogni {s2_sg}, "
            f"{s2_sg} NON e' {p2_sg}"
        )
        d1 = (
            f"Per ogni {s1_sg}, per ogni {s2_sg}, "
            f"{s2_sg} NON e' {p2_sg}"
        )
        d2 = (
            f"Esiste almeno un {s1_sg} tale che esiste almeno un {s2_sg} "
            f"che NON e' {p2_sg}"
        )
        d3 = (
            f"Per ogni {s1_sg}, nessun {s2_sg} e' {p2_sg}"
        )
        d4 = (
            f"Per ogni {s1_sg}, per ogni {s2_sg}, "
            f"{s2_sg} e' {p2_sg}"
        )
        explanation = (
            f"Per negare quantificatori annidati, si procede dall'esterno verso l'interno: "
            f"neg(forall x, exists y, P(y)) = exists x, forall y, NOT P(y). "
            f"Ogni quantificatore si 'ribalta': forall diventa exists e viceversa. "
            f"La proprieta' piu' interna viene negata."
        )
        tip = "Per negare quantificatori annidati: ribalta ogni quantificatore (forall<->exists) e nega la proprieta' finale."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _contrapositive_chain():
        """Contrapositive in a chain of implications."""
        e1, e2 = _pick(_EVENTI_CAUSA, 2)
        causa1, effetto1 = e1
        _causa2, effetto2 = e2
        nome = _pick(_NOMI)
        question = (
            f"Sappiamo che:\n"
            f"1) Se {causa1}, allora {effetto1}\n"
            f"2) Se {effetto1}, allora {effetto2}\n"
            f"3) {nome} non {effetto2}\n"
            f"Cosa possiamo concludere su {nome}?"
        )
        correct = f"{nome} non {causa1} (e anche non {effetto1})"
        d1 = f"Solo che {nome} non {effetto1}"
        d2 = f"Non possiamo concludere nulla su {causa1}"
        d3 = f"{nome} {causa1}"
        d4 = f"{nome} potrebbe {causa1}"
        explanation = (
            f"Applicando il Modus Tollens alla premessa 2: NOT {effetto2} => NOT {effetto1}. "
            f"Poi applicando il Modus Tollens alla premessa 1: NOT {effetto1} => NOT {causa1}. "
            f"Quindi possiamo concludere sia NOT {effetto1} che NOT {causa1}. "
            f"In pratica, la contropositiva della catena A=>B=>C e': NOT C => NOT B => NOT A."
        )
        tip = "Il Modus Tollens si applica 'a ritroso' nella catena: NOT C => NOT B => NOT A. Come un domino al contrario."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _necessary_and_sufficient():
        """Distinguish necessary from sufficient in a complex scenario."""
        set_a, set_b = _pick(_INSIEMI_AB)
        question = (
            f"Sappiamo che 'Tutti i {set_b} sono {set_a}' (ma non viceversa). "
            f"Quale delle seguenti affermazioni e' corretta?"
        )
        correct = f"Essere {set_b} e' sufficiente per essere {set_a}, e essere {set_a} e' necessario per essere {set_b}"
        d1 = f"Essere {set_a} e' sufficiente per essere {set_b}"
        d2 = f"Essere {set_b} e' necessario per essere {set_a}"
        d3 = f"Essere {set_b} e' necessario e sufficiente per essere {set_a}"
        d4 = f"Essere {set_a} e' equivalente a essere {set_b}"
        explanation = (
            f"'Tutti i {set_b} sono {set_a}' significa che B implica A (B => A). "
            f"Quindi B e' condizione sufficiente per A (basta essere B per essere A). "
            f"Equivalentemente, A e' condizione necessaria per B (senza A non si puo' essere B, "
            f"per la contropositiva: NOT A => NOT B)."
        )
        tip = "Se B => A: B e' sufficiente per A, e A e' necessaria per B. Esempio: essere quadrato e' sufficiente per essere rettangolo."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _fallacy_affirming_consequent():
        """Identify the fallacy of affirming the consequent."""
        causa, effetto = _pick(_EVENTI_CAUSA)
        nome = _pick(_NOMI)
        question = (
            f"Sappiamo che 'Se {causa}, allora {effetto}'. "
            f"Osserviamo che {nome} {effetto}. Cosa possiamo concludere?"
        )
        correct = f"Non possiamo concludere con certezza che {nome} {causa}"
        d1 = f"{nome} {causa}"
        d2 = f"{nome} non {causa}"
        d3 = f"L'implicazione originale e' falsa"
        d4 = f"{nome} potrebbe {causa} ma non necessariamente"
        explanation = (
            f"Affermare il conseguente e' una fallacia logica. "
            f"Da 'Se A allora B' e 'B vero' NON si puo' dedurre 'A vero'. "
            f"B potrebbe essere vero per altri motivi. "
            f"Esempio: 'Se piove il terreno e' bagnato' e 'il terreno e' bagnato' "
            f"non implica che piove (magari hanno innaffiato)."
        )
        tip = "Fallacia dell'affermazione del conseguente: da A=>B e B vero NON segue A. Il terreno bagnato non prova che piove."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _logical_equivalence_test():
        """Test understanding of logical equivalence between complex statements."""
        s_pl, s_sg, p_pl, p_sg = _pick_subj_prop()
        question = (
            f"Quale delle seguenti affermazioni e' equivalente a "
            f"'Non e' vero che tutti i {s_pl} sono {p_pl}'?"
        )
        correct = f"Esiste almeno un {s_sg} che non e' {p_sg}"
        d1 = f"Tutti i {s_pl} non sono {p_pl}"
        d2 = f"Nessun {s_sg} e' {p_sg}"
        d3 = f"Non esiste un {s_sg} che e' {p_sg}"
        d4 = f"Tutti i {s_pl} sono {p_pl} oppure non lo sono"
        explanation = (
            f"'Non e' vero che tutti i {s_pl} sono {p_pl}' e' la negazione di una proposizione universale. "
            f"neg(forall x, P(x)) = exists x, NOT P(x). "
            f"'Tutti non sono P' = 'Nessuno e' P', che e' piu' forte della semplice negazione."
        )
        tip = "'Non tutti sono P' e' MOLTO diverso da 'Nessuno e' P'. Il primo ammette eccezioni, il secondo le esclude tutte."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  SET NOTATION — LEVEL 1: membership, basic operations
    # ================================================================

    @staticmethod
    def _set_membership():
        """Which ∈ / ∉ statement is true for a given set."""
        size = random.randint(4, 6)
        pool = list(range(1, 20))
        elements = sorted(random.sample(pool, size))
        set_str = "{" + ", ".join(str(e) for e in elements) + "}"
        # pick one element that IS in A
        correct_elem = random.choice(elements)
        # pick 4 elements that are NOT in A
        outside = [x for x in pool if x not in elements]
        distractors_elems = random.sample(outside, min(4, len(outside)))

        question = (
            f"Dato l'insieme A = {set_str}, quale delle seguenti affermazioni e' vera?"
        )
        correct = f"{correct_elem} ∈ A"
        d1 = f"{distractors_elems[0]} ∈ A"
        d2 = f"{distractors_elems[1]} ∈ A"
        d3 = f"{correct_elem} ∉ A"
        d4 = f"{distractors_elems[2]} ∈ A" if len(distractors_elems) >= 3 else f"{distractors_elems[0]} ∉ A"
        explanation = (
            f"L'insieme A = {set_str} contiene gli elementi {', '.join(str(e) for e in elements)}. "
            f"Il simbolo ∈ significa 'appartiene a', quindi {correct_elem} ∈ A e' vero perche' "
            f"{correct_elem} e' un elemento di A. Gli altri elementi indicati non appartengono ad A."
        )
        tip = "Il simbolo ∈ indica l'appartenenza: x ∈ A si legge 'x appartiene ad A'. Il simbolo ∉ indica la non appartenenza."
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _set_basic_operations():
        """Compute A ∩ B or A ∪ B for two given sets."""
        pool = list(range(1, 15))
        # create two overlapping sets
        common = sorted(random.sample(pool, random.randint(1, 3)))
        only_a = sorted(random.sample([x for x in pool if x not in common], random.randint(1, 3)))
        only_b = sorted(random.sample([x for x in pool if x not in common and x not in only_a], random.randint(1, 3)))
        set_a = sorted(only_a + common)
        set_b = sorted(only_b + common)
        str_a = "{" + ", ".join(str(e) for e in set_a) + "}"
        str_b = "{" + ", ".join(str(e) for e in set_b) + "}"

        op = random.choice(["intersezione", "unione"])
        if op == "intersezione":
            result = sorted(common)
            symbol = "∩"
        else:
            result = sorted(set(set_a) | set(set_b))
            symbol = "∪"

        result_str = "{" + ", ".join(str(e) for e in result) + "}"

        question = (
            f"Dati A = {str_a} e B = {str_b}, calcola A {symbol} B."
        )
        correct = result_str

        # generate plausible wrong answers
        d1 = "{" + ", ".join(str(e) for e in sorted(only_a)) + "}"
        d2 = "{" + ", ".join(str(e) for e in sorted(only_b)) + "}"
        if op == "intersezione":
            d3 = "{" + ", ".join(str(e) for e in sorted(set(set_a) | set(set_b))) + "}"
        else:
            d3 = "{" + ", ".join(str(e) for e in sorted(common)) + "}"
        d4 = "{" + ", ".join(str(e) for e in sorted(set(set_a) - set(set_b))) + "}"

        explanation = (
            f"A = {str_a}, B = {str_b}. "
            f"L'intersezione A ∩ B contiene gli elementi comuni: "
            f"{'{' + ', '.join(str(e) for e in sorted(common)) + '}'}. "
            f"L'unione A ∪ B contiene tutti gli elementi di entrambi: "
            f"{'{' + ', '.join(str(e) for e in sorted(set(set_a) | set(set_b))) + '}'}. "
            f"Quindi A {symbol} B = {result_str}."
        )
        tip = (
            "A ∩ B (intersezione) = elementi comuni ad A e B. "
            "A ∪ B (unione) = tutti gli elementi che stanno in A o in B (o in entrambi)."
        )
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  SET NOTATION — LEVEL 2: inclusion, complement, compound ops
    # ================================================================

    @staticmethod
    def _set_inclusion():
        """Determine the correct inclusion relation between two sets."""
        pool = list(range(1, 15))
        # generate A ⊂ B (proper subset)
        size_b = random.randint(4, 6)
        set_b = sorted(random.sample(pool, size_b))
        size_a = random.randint(2, size_b - 1)
        set_a = sorted(random.sample(set_b, size_a))

        str_a = "{" + ", ".join(str(e) for e in set_a) + "}"
        str_b = "{" + ", ".join(str(e) for e in set_b) + "}"

        question = (
            f"Dati A = {str_a} e B = {str_b}, quale relazione e' corretta?"
        )
        correct = "A ⊂ B (A e' sottoinsieme proprio di B)"
        d1 = "B ⊂ A (B e' sottoinsieme proprio di A)"
        d2 = "A = B"
        d3 = "A ⊄ B (A non e' sottoinsieme di B)"
        d4 = "A ∩ B = ∅ (A e B sono disgiunti)"
        explanation = (
            f"A = {str_a} e B = {str_b}. Ogni elemento di A appartiene anche a B, "
            f"ma B contiene elementi non presenti in A. Quindi A ⊂ B (A e' sottoinsieme "
            f"proprio di B). Si scrive anche A ⊆ B (sottoinsieme, non necessariamente proprio) "
            f"poiche' A ≠ B."
        )
        tip = (
            "A ⊂ B significa che ogni elemento di A e' in B e A ≠ B (sottoinsieme proprio). "
            "A ⊆ B significa che ogni elemento di A e' in B (A potrebbe anche coincidere con B)."
        )
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _set_complement_difference():
        """Compute the complement of A in U, or A \\ B."""
        pool = list(range(1, 15))
        size_u = random.randint(6, 9)
        universal = sorted(random.sample(pool, size_u))
        size_a = random.randint(2, size_u - 2)
        set_a = sorted(random.sample(universal, size_a))
        complement_a = sorted(set(universal) - set(set_a))

        op = random.choice(["complemento", "differenza"])

        if op == "complemento":
            str_u = "{" + ", ".join(str(e) for e in universal) + "}"
            str_a = "{" + ", ".join(str(e) for e in set_a) + "}"
            result = complement_a
            result_str = "{" + ", ".join(str(e) for e in result) + "}"

            question = (
                f"Dato l'insieme universo U = {str_u} e A = {str_a}, "
                f"calcola il complementare di A (U \\ A)."
            )
            # distractors
            d1 = str_a  # A itself
            d2 = str_u  # U itself
            d3 = "{" + ", ".join(str(e) for e in sorted(random.sample(universal, min(3, size_u)))) + "}"
            d4 = "∅"
        else:
            remaining = [x for x in universal if x not in set_a]
            size_b = random.randint(2, size_u - 1)
            set_b_elems = random.sample(universal, size_b)
            set_b = sorted(set_b_elems)
            result = sorted(set(set_a) - set(set_b))
            result_str = "{" + ", ".join(str(e) for e in result) + "}" if result else "∅"
            str_a = "{" + ", ".join(str(e) for e in set_a) + "}"
            str_b = "{" + ", ".join(str(e) for e in set_b) + "}"

            question = (
                f"Dati A = {str_a} e B = {str_b}, calcola A \\ B (differenza)."
            )
            d1 = "{" + ", ".join(str(e) for e in sorted(set(set_b) - set(set_a))) + "}" if set(set_b) - set(set_a) else "∅"
            d2 = "{" + ", ".join(str(e) for e in sorted(set(set_a) & set(set_b))) + "}" if set(set_a) & set(set_b) else "∅"
            d3 = "{" + ", ".join(str(e) for e in sorted(set(set_a) | set(set_b))) + "}"
            d4 = str_a

        correct = result_str
        explanation = (
            f"La differenza A \\ B contiene gli elementi di A che NON appartengono a B. "
            f"Il complementare di A rispetto a U e' U \\ A, cioe' tutti gli elementi di U "
            f"che non stanno in A. In questo caso il risultato e' {result_str}."
        )
        tip = (
            "A \\ B = {x : x ∈ A e x ∉ B}. Il complementare di A (rispetto a U) e' "
            "U \\ A = {x ∈ U : x ∉ A}. Si indica anche con A^c o ∁A."
        )
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _set_compound_operations():
        """Compute (A ∪ B) ∩ C or (A ∩ B) ∪ C."""
        pool = list(range(1, 15))
        set_a = sorted(random.sample(pool, random.randint(3, 5)))
        set_b = sorted(random.sample(pool, random.randint(3, 5)))
        set_c = sorted(random.sample(pool, random.randint(3, 5)))

        str_a = "{" + ", ".join(str(e) for e in set_a) + "}"
        str_b = "{" + ", ".join(str(e) for e in set_b) + "}"
        str_c = "{" + ", ".join(str(e) for e in set_c) + "}"

        op = random.choice(["union_inter", "inter_union"])
        if op == "union_inter":
            intermediate = set(set_a) | set(set_b)
            result = sorted(intermediate & set(set_c))
            expr = f"(A ∪ B) ∩ C"
        else:
            intermediate = set(set_a) & set(set_b)
            result = sorted(intermediate | set(set_c))
            expr = f"(A ∩ B) ∪ C"

        result_str = "{" + ", ".join(str(e) for e in result) + "}" if result else "∅"

        question = (
            f"Dati A = {str_a}, B = {str_b}, C = {str_c}, calcola {expr}."
        )
        correct = result_str

        # generate plausible wrong answers
        wrong1 = sorted(set(set_a) | set(set_b) | set(set_c))
        wrong2 = sorted(set(set_a) & set(set_b) & set(set_c))
        wrong3 = sorted(set(set_a) & set(set_c))
        if op == "union_inter":
            wrong4 = sorted((set(set_a) & set(set_b)) | set(set_c))
        else:
            wrong4 = sorted((set(set_a) | set(set_b)) & set(set_c))

        d1 = "{" + ", ".join(str(e) for e in wrong1) + "}" if wrong1 else "∅"
        d2 = "{" + ", ".join(str(e) for e in wrong2) + "}" if wrong2 else "∅"
        d3 = "{" + ", ".join(str(e) for e in wrong3) + "}" if wrong3 else "∅"
        d4 = "{" + ", ".join(str(e) for e in wrong4) + "}" if wrong4 else "∅"

        explanation = (
            f"A = {str_a}, B = {str_b}, C = {str_c}. "
            f"Per calcolare {expr}, si procede per passi: prima si calcola l'operazione "
            f"tra parentesi, poi si applica l'operazione esterna. "
            f"Il risultato e' {result_str}."
        )
        tip = (
            "Nelle operazioni composte tra insiemi, si risolvono prima le parentesi "
            "(come in aritmetica). Attenzione: ∪ e ∩ NON sono distributive allo stesso modo "
            "di + e ×."
        )
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  SET NOTATION — LEVEL 3: Venn diagrams, inclusion-exclusion
    # ================================================================

    @staticmethod
    def _set_venn_counting():
        """Inclusion-exclusion with two sets: |A ∪ B| = |A| + |B| - |A ∩ B|."""
        both = random.randint(3, 10)
        only_a = random.randint(5, 20)
        only_b = random.randint(5, 20)
        tot_a = only_a + both
        tot_b = only_b + both
        union = only_a + only_b + both

        materia1, materia2 = _pick(_MATERIE, 2)
        question = (
            f"In una classe, {tot_a} studenti studiano {materia1}, "
            f"{tot_b} studiano {materia2} e {both} studiano entrambe le materie. "
            f"Quanti studenti studiano almeno una delle due materie?"
        )
        correct = str(union)
        d1 = str(tot_a + tot_b)  # forgetting to subtract intersection
        d2 = str(both)  # only the intersection
        d3 = str(union + both)  # adding intersection twice
        d4 = str(abs(tot_a - tot_b))  # difference
        explanation = (
            f"Per il principio di inclusione-esclusione: "
            f"|A ∪ B| = |A| + |B| - |A ∩ B| = {tot_a} + {tot_b} - {both} = {union}. "
            f"Si sottrae |A ∩ B| perche' gli studenti che studiano entrambe le materie "
            f"vengono contati due volte nella somma |A| + |B|."
        )
        tip = (
            "Principio di inclusione-esclusione per 2 insiemi: "
            "|A ∪ B| = |A| + |B| - |A ∩ B|. Si sottrae l'intersezione per evitare il doppio conteggio."
        )
        return question, correct, [d1, d2, d3, d4], explanation, tip

    @staticmethod
    def _set_three_sets_venn():
        """Three-set Venn diagram: how many in exactly one set?"""
        # generate consistent Venn regions
        # r1 = only A, r2 = only B, r3 = only C
        # r4 = A∩B only, r5 = A∩C only, r6 = B∩C only, r7 = A∩B∩C
        r1 = random.randint(3, 12)
        r2 = random.randint(3, 12)
        r3 = random.randint(3, 12)
        r4 = random.randint(1, 5)
        r5 = random.randint(1, 5)
        r6 = random.randint(1, 5)
        r7 = random.randint(1, 3)

        card_a = r1 + r4 + r5 + r7
        card_b = r2 + r4 + r6 + r7
        card_c = r3 + r5 + r6 + r7
        card_ab = r4 + r7
        card_ac = r5 + r7
        card_bc = r6 + r7
        card_abc = r7
        exactly_one = r1 + r2 + r3
        total = r1 + r2 + r3 + r4 + r5 + r6 + r7

        materia1, materia2, materia3 = _pick(_MATERIE, 3)
        question = (
            f"In un gruppo di {total} studenti:\n"
            f"- |A| = {card_a} studiano {materia1}\n"
            f"- |B| = {card_b} studiano {materia2}\n"
            f"- |C| = {card_c} studiano {materia3}\n"
            f"- |A ∩ B| = {card_ab}, |A ∩ C| = {card_ac}, |B ∩ C| = {card_bc}\n"
            f"- |A ∩ B ∩ C| = {card_abc}\n"
            f"Quanti studenti studiano esattamente una sola materia?"
        )
        correct = str(exactly_one)
        d1 = str(total)  # all students
        d2 = str(card_a + card_b + card_c)  # sum without exclusion
        d3 = str(exactly_one + r4 + r5 + r6)  # at least one but not all three
        d4 = str(r4 + r5 + r6 + r7)  # those in 2+ sets
        explanation = (
            f"Per trovare chi studia esattamente una materia, calcoliamo:\n"
            f"Solo A = |A| - |A ∩ B| - |A ∩ C| + |A ∩ B ∩ C| = {card_a} - {card_ab} - {card_ac} + {card_abc} = {r1}\n"
            f"Solo B = |B| - |A ∩ B| - |B ∩ C| + |A ∩ B ∩ C| = {card_b} - {card_ab} - {card_bc} + {card_abc} = {r2}\n"
            f"Solo C = |C| - |A ∩ C| - |B ∩ C| + |A ∩ B ∩ C| = {card_c} - {card_ac} - {card_bc} + {card_abc} = {r3}\n"
            f"Totale esattamente una = {r1} + {r2} + {r3} = {exactly_one}."
        )
        tip = (
            "Per trovare 'esattamente in un solo insieme' si usa: "
            "|solo A| = |A| - |A ∩ B| - |A ∩ C| + |A ∩ B ∩ C|. "
            "Si aggiunge |A ∩ B ∩ C| perche' viene sottratto due volte."
        )
        return question, correct, [d1, d2, d3, d4], explanation, tip

    # ================================================================
    #  Template registry by difficulty
    # ================================================================

    def _get_templates(self, difficulty):
        level_1 = [
            self._negation_all,
            self._negation_none,
            self._negation_some,
            self._negation_simple_and,
            self._negation_simple_or,
            self._set_membership,
            self._set_basic_operations,
        ]
        level_2 = [
            self._contrapositive,
            self._equivalent_implication,
            self._necessary_condition,
            self._sufficient_condition,
            self._negation_universal_quantifier,
            self._modus_tollens,
            self._set_inclusion,
            self._set_complement_difference,
            self._set_compound_operations,
        ]
        level_3 = [
            self._implication_chain,
            self._chain_with_modus_ponens,
            self._combined_quantifiers,
            self._contrapositive_chain,
            self._necessary_and_sufficient,
            self._fallacy_affirming_consequent,
            self._logical_equivalence_test,
            self._set_venn_counting,
            self._set_three_sets_venn,
        ]
        if difficulty == 1:
            return level_1
        elif difficulty == 2:
            return level_2
        else:
            return level_3

    def generate(self, difficulty: int) -> dict:
        difficulty = max(1, min(3, difficulty))
        templates = self._get_templates(difficulty)
        template_fn = random.choice(templates)
        question, correct, distractors, explanation, tip = template_fn()
        return self._build_result(question, correct, distractors, explanation, tip, difficulty)

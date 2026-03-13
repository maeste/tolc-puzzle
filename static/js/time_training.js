/* === TOLC-B Time Management Training Mode === */
document.addEventListener("DOMContentLoaded", () => {
    const EXERCISE_TYPES = window.EXERCISE_TYPES || {};
    const OPTION_LETTERS = ["A", "B", "C", "D", "E"];
    const CIRCUMFERENCE = 2 * Math.PI * 52; // matches SVG circle r=52

    const TYPE_NAMES = {};
    for (const [key, val] of Object.entries(EXERCISE_TYPES)) {
        TYPE_NAMES[key] = val.name || key;
    }

    // Screens
    const setupScreen = document.getElementById("tt-setup");
    const activeScreen = document.getElementById("tt-active");
    const resultsScreen = document.getElementById("tt-results");

    // Controls
    const btnStart = document.getElementById("btn-start-tt");
    const btnSkip = document.getElementById("btn-tt-skip");
    const btnAnswer = document.getElementById("btn-tt-answer");
    const btnRetry = document.getElementById("btn-retry-tt");

    // Display elements
    const progressDisplay = document.getElementById("tt-progress");
    const scoreDisplay = document.getElementById("tt-score-display");
    const questionArea = document.getElementById("tt-question-area");
    const timerText = document.getElementById("tt-timer-text");
    const timerIndicator = document.getElementById("tt-timer-indicator");
    const timerCircle = document.getElementById("tt-timer-circle");
    const evHint = document.getElementById("tt-ev-hint");

    // Settings
    let config = {
        numQuestions: 15,
        timeout: 150, // seconds
        types: [],
    };

    // State
    let questions = [];
    let questionData = []; // per-question tracking
    let currentIndex = 0;
    let timerInterval = null;
    let questionStartTime = 0;
    let remainingTime = 0;
    let runningScore = 0;
    let selectedAnswer = null;
    let eliminatedOptions = [];

    // ============ SCREEN MANAGEMENT ============

    function showScreen(screen) {
        setupScreen.classList.add("hidden");
        activeScreen.classList.add("hidden");
        resultsScreen.classList.add("hidden");
        screen.classList.remove("hidden");
        window.scrollTo(0, 0);
    }

    // ============ SETTINGS ============

    document.querySelectorAll(".tt-opt-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const setting = btn.dataset.setting;
            const value = parseInt(btn.dataset.value);
            // Deselect siblings
            btn.parentElement.querySelectorAll(".tt-opt-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            config[setting] = value;
        });
    });

    // ============ START ============

    btnStart.addEventListener("click", startTraining);
    if (btnRetry) btnRetry.addEventListener("click", () => {
        showScreen(setupScreen);
    });

    async function startTraining() {
        // Gather selected types
        const checkboxes = document.querySelectorAll("#tt-type-checkboxes input[type=checkbox]:checked");
        config.types = Array.from(checkboxes).map(cb => cb.value);

        if (config.types.length === 0) {
            alert("Seleziona almeno una tipologia di esercizio.");
            return;
        }

        showScreen(activeScreen);
        questionArea.innerHTML = '<div class="loading">Caricamento domande...</div>';

        // Load questions one at a time (fetch all upfront)
        questions = [];
        questionData = [];
        currentIndex = 0;
        runningScore = 0;

        try {
            for (let i = 0; i < config.numQuestions; i++) {
                const type = config.types[Math.floor(Math.random() * config.types.length)];
                // Weighted difficulty: mostly L2
                const diffRoll = Math.random();
                let difficulty;
                if (diffRoll < 0.2) difficulty = 1;
                else if (diffRoll < 0.8) difficulty = 2;
                else difficulty = 3;

                const res = await fetch(`/api/exercise/${type}?difficulty=${difficulty}`);
                if (!res.ok) throw new Error(`Errore nel caricamento domanda ${i + 1}`);
                const data = await res.json();
                data.type = type;
                data.difficulty = difficulty;

                // Normalize options
                if (!data.options && data.steps) {
                    data.options = data.steps;
                    delete data.steps;
                }
                if (!data.options) data.options = [];
                while (data.options.length < 5) {
                    data.options.push("Nessuna delle precedenti");
                }

                questions.push(data);
                questionData.push({
                    type: type,
                    difficulty: difficulty,
                    timeSpent: 0,
                    answer: null,
                    correctIndex: data.correct_index,
                    result: null, // 'correct', 'wrong', 'skip'
                    eliminated: [],
                });
            }
        } catch (err) {
            questionArea.innerHTML = `<div class="loading">Errore: ${err.message}</div>`;
            return;
        }

        updateScoreDisplay();
        loadQuestion();
    }

    // ============ QUESTION LOADING ============

    function loadQuestion() {
        if (currentIndex >= questions.length) {
            showResults();
            return;
        }

        const ex = questions[currentIndex];
        const qd = questionData[currentIndex];
        selectedAnswer = null;
        eliminatedOptions = qd.eliminated.slice(); // restore if revisited (shouldn't happen but safe)
        remainingTime = config.timeout;
        questionStartTime = Date.now();

        progressDisplay.textContent = `Domanda ${currentIndex + 1} di ${config.numQuestions}`;
        btnAnswer.disabled = true;
        evHint.classList.add("hidden");

        renderQuestion(ex);
        startTimer();
    }

    function renderQuestion(ex) {
        const typeName = TYPE_NAMES[ex.type] || ex.type;
        let html = "";

        html += `<div class="sim-question-meta">`;
        html += `<span class="sim-type-badge">${typeName}</span>`;
        html += `<span class="sim-difficulty-badge">`;
        for (let i = 0; i < (ex.difficulty || 1); i++) html += "&#9733;";
        html += `</span>`;
        html += `</div>`;

        html += `<div class="question exam-question">${ex.question}</div>`;

        if (ex.graph_data) {
            html += `<div class="sim-graph-container">${ex.graph_data}</div>`;
        }

        if (ex.options) {
            html += '<div class="options exam-options">';
            ex.options.forEach((opt, i) => {
                const letter = OPTION_LETTERS[i] || String.fromCharCode(65 + i);
                const elimClass = eliminatedOptions.includes(i) ? " tt-option-eliminated" : "";
                html += `<div class="option exam-option${elimClass}" data-index="${i}">`;
                html += `<span class="exam-option-letter">${letter}</span>`;
                html += `<span class="exam-option-text">${opt}</span>`;
                html += `</div>`;
            });
            html += "</div>";
        }

        questionArea.innerHTML = html;

        // Bind handlers
        const options = questionArea.querySelectorAll(".exam-option");
        options.forEach(el => {
            // Left click: select answer
            el.addEventListener("click", (e) => {
                const idx = parseInt(el.dataset.index);
                if (eliminatedOptions.includes(idx)) return;
                options.forEach(s => s.classList.remove("selected"));
                el.classList.add("selected");
                selectedAnswer = idx;
                btnAnswer.disabled = false;
            });

            // Right click: eliminate option
            el.addEventListener("contextmenu", (e) => {
                e.preventDefault();
                toggleElimination(parseInt(el.dataset.index), el);
            });

            // Long press for mobile
            let longPressTimer = null;
            el.addEventListener("touchstart", (e) => {
                longPressTimer = setTimeout(() => {
                    e.preventDefault();
                    toggleElimination(parseInt(el.dataset.index), el);
                }, 500);
            }, { passive: false });
            el.addEventListener("touchend", () => {
                if (longPressTimer) clearTimeout(longPressTimer);
            });
            el.addEventListener("touchmove", () => {
                if (longPressTimer) clearTimeout(longPressTimer);
            });
        });
    }

    function toggleElimination(index, el) {
        const pos = eliminatedOptions.indexOf(index);
        if (pos >= 0) {
            // Un-eliminate
            eliminatedOptions.splice(pos, 1);
            el.classList.remove("tt-option-eliminated");
        } else {
            // Cannot eliminate all options
            if (eliminatedOptions.length >= 4) return;
            // If this option is currently selected, deselect it
            if (selectedAnswer === index) {
                selectedAnswer = null;
                el.classList.remove("selected");
                btnAnswer.disabled = true;
            }
            eliminatedOptions.push(index);
            el.classList.add("tt-option-eliminated");
        }
        questionData[currentIndex].eliminated = eliminatedOptions.slice();
        updateEVHint();
    }

    function updateEVHint() {
        const remaining = 5 - eliminatedOptions.length;
        // EV = (1/remaining)*1 + ((remaining-1)/remaining)*(-0.25)
        const ev = (1 / remaining) * 1 + ((remaining - 1) / remaining) * (-0.25);
        if (ev > 0 && eliminatedOptions.length >= 2) {
            evHint.textContent = `Hai eliminato ${eliminatedOptions.length} opzioni. Indovinare ora ha valore atteso positivo (+${ev.toFixed(2)} punti)`;
            evHint.classList.remove("hidden");
        } else {
            evHint.classList.add("hidden");
        }
    }

    // ============ TIMER ============

    function startTimer() {
        if (timerInterval) clearInterval(timerInterval);
        updateTimerDisplay();

        // Set initial SVG state
        timerIndicator.style.strokeDasharray = `${CIRCUMFERENCE}`;
        timerIndicator.style.strokeDashoffset = "0";

        timerInterval = setInterval(() => {
            const elapsed = (Date.now() - questionStartTime) / 1000;
            remainingTime = Math.max(0, config.timeout - elapsed);
            updateTimerDisplay();

            if (remainingTime <= 0) {
                clearInterval(timerInterval);
                timerInterval = null;
                autoAdvance();
            }
        }, 100);
    }

    function updateTimerDisplay() {
        const minutes = Math.floor(remainingTime / 60);
        const seconds = Math.floor(remainingTime % 60);
        timerText.textContent = `${minutes}:${seconds.toString().padStart(2, "0")}`;

        // Update circular progress
        const pct = remainingTime / config.timeout;
        const offset = CIRCUMFERENCE * (1 - pct);
        timerIndicator.style.strokeDashoffset = offset;

        // Color transitions based on time thresholds
        // Green: > 50% time remaining
        // Yellow: 20-50% remaining
        // Red: < 20% remaining
        timerCircle.classList.remove("tt-timer-green", "tt-timer-yellow", "tt-timer-red");
        if (pct > 0.5) {
            timerCircle.classList.add("tt-timer-green");
        } else if (pct > 0.2) {
            timerCircle.classList.add("tt-timer-yellow");
        } else {
            timerCircle.classList.add("tt-timer-red");
        }
    }

    // ============ ANSWER / SKIP ============

    btnAnswer.addEventListener("click", () => {
        if (selectedAnswer === null) return;
        recordAnswer(selectedAnswer);
    });

    btnSkip.addEventListener("click", () => {
        skipQuestion();
    });

    function recordAnswer(answerIndex) {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }

        const elapsed = (Date.now() - questionStartTime) / 1000;
        const qd = questionData[currentIndex];
        qd.timeSpent = elapsed;
        qd.answer = answerIndex;

        if (answerIndex === questions[currentIndex].correct_index) {
            qd.result = "correct";
            runningScore += 1;
        } else {
            qd.result = "wrong";
            runningScore -= 0.25;
        }

        updateScoreDisplay();
        currentIndex++;
        loadQuestion();
    }

    function skipQuestion() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }

        const elapsed = (Date.now() - questionStartTime) / 1000;
        const qd = questionData[currentIndex];
        qd.timeSpent = elapsed;
        qd.result = "skip";

        currentIndex++;
        loadQuestion();
    }

    function autoAdvance() {
        const elapsed = config.timeout;
        const qd = questionData[currentIndex];
        qd.timeSpent = elapsed;
        qd.result = "skip";

        currentIndex++;
        loadQuestion();
    }

    function updateScoreDisplay() {
        scoreDisplay.textContent = `Punteggio: ${runningScore.toFixed(2)}`;
    }

    // ============ RESULTS ============

    function showResults() {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }

        showScreen(resultsScreen);

        let totalCorrect = 0;
        let totalWrong = 0;
        let totalSkipped = 0;
        let totalScore = 0;
        let totalTime = 0;
        let correctTimes = [];
        let wrongTimes = [];

        questionData.forEach(qd => {
            totalTime += qd.timeSpent;
            if (qd.result === "correct") {
                totalCorrect++;
                totalScore += 1;
                correctTimes.push(qd.timeSpent);
            } else if (qd.result === "wrong") {
                totalWrong++;
                totalScore -= 0.25;
                wrongTimes.push(qd.timeSpent);
            } else {
                totalSkipped++;
            }
        });

        const avgCorrectTime = correctTimes.length > 0
            ? correctTimes.reduce((a, b) => a + b, 0) / correctTimes.length : 0;
        const avgWrongTime = wrongTimes.length > 0
            ? wrongTimes.reduce((a, b) => a + b, 0) / wrongTimes.length : 0;
        const wastedTime = wrongTimes.reduce((a, b) => a + b, 0);
        const answeredCount = totalCorrect + totalWrong;
        const avgTime = answeredCount > 0 ? totalTime / answeredCount : 0;

        // Score card
        document.getElementById("tt-score-value").textContent = totalScore.toFixed(2);
        const scoreCard = document.getElementById("tt-score-card");
        scoreCard.classList.remove("sim-score-good", "sim-score-mid", "sim-score-low");
        if (totalScore >= config.numQuestions * 0.7) {
            scoreCard.classList.add("sim-score-good");
        } else if (totalScore >= config.numQuestions * 0.4) {
            scoreCard.classList.add("sim-score-mid");
        } else {
            scoreCard.classList.add("sim-score-low");
        }

        document.getElementById("tt-results-subtitle").textContent =
            `${config.numQuestions} domande, ${config.timeout}s per domanda — Tempo totale: ${formatTime(totalTime)}`;

        // Stats
        document.getElementById("tt-stat-correct").textContent = totalCorrect;
        document.getElementById("tt-stat-wrong").textContent = totalWrong;
        document.getElementById("tt-stat-skipped").textContent = totalSkipped;
        document.getElementById("tt-stat-avgtime").textContent = `${Math.round(avgTime)}s`;

        // Time stats
        document.getElementById("tt-avg-correct-time").textContent =
            correctTimes.length > 0 ? `${Math.round(avgCorrectTime)}s` : "--";
        document.getElementById("tt-avg-wrong-time").textContent =
            wrongTimes.length > 0 ? `${Math.round(avgWrongTime)}s` : "--";
        document.getElementById("tt-wasted-time").textContent =
            wrongTimes.length > 0 ? formatTime(wastedTime) : "--";

        // Scatter plot
        renderScatterPlot();

        // Breakdown table
        renderBreakdownTable();

        // Strategy feedback
        renderStrategyFeedback(avgCorrectTime, avgWrongTime);

        // Save to localStorage
        saveHistory(totalScore, totalCorrect, totalWrong, totalSkipped, avgTime);
    }

    function renderScatterPlot() {
        const area = document.getElementById("tt-scatter-area");
        area.innerHTML = "";

        const maxTime = Math.max(...questionData.map(qd => qd.timeSpent), config.timeout);
        const yMax = Math.ceil(maxTime / 30) * 30; // round up to nearest 30s

        document.getElementById("tt-scatter-y-max").textContent = `${yMax}s`;
        document.getElementById("tt-scatter-y-mid").textContent = `${Math.round(yMax / 2)}s`;

        questionData.forEach((qd, i) => {
            const dot = document.createElement("div");
            dot.className = `tt-scatter-dot ${qd.result}`;

            // Position
            const xPct = ((i + 0.5) / questionData.length) * 100;
            const yPct = (qd.timeSpent / yMax) * 100;

            dot.style.left = `${xPct}%`;
            dot.style.bottom = `${yPct}%`;
            dot.title = `#${i + 1}: ${Math.round(qd.timeSpent)}s — ${
                qd.result === "correct" ? "Corretta" : qd.result === "wrong" ? "Errata" : "Saltata"
            }`;

            area.appendChild(dot);
        });
    }

    function renderBreakdownTable() {
        const tbody = document.getElementById("tt-breakdown-body");
        tbody.innerHTML = "";

        questionData.forEach((qd, i) => {
            const row = document.createElement("tr");

            let resultIcon = "";
            let resultClass = "";
            if (qd.result === "correct") {
                resultIcon = "&#10003;";
                resultClass = "score-positive";
            } else if (qd.result === "wrong") {
                resultIcon = "&#10007;";
                resultClass = "score-negative";
            } else {
                resultIcon = "&#9193;";
                resultClass = "";
            }

            let diffStars = "";
            for (let d = 0; d < qd.difficulty; d++) diffStars += "&#9733;";

            const feedback = getQuestionFeedback(qd);

            row.innerHTML = `
                <td>${i + 1}</td>
                <td>${Math.round(qd.timeSpent)}s</td>
                <td class="${resultClass}">${resultIcon}</td>
                <td>${diffStars}</td>
                <td class="tt-feedback-cell">${feedback}</td>
            `;
            tbody.appendChild(row);
        });
    }

    function getQuestionFeedback(qd) {
        if (qd.result === "skip" && qd.difficulty === 3) {
            return "Buona scelta — domanda difficile (L3)";
        }
        if (qd.result === "correct" && qd.timeSpent < config.timeout * 0.4) {
            return "Ottimo ritmo!";
        }
        if (qd.result === "wrong" && qd.timeSpent > config.timeout * 0.7) {
            return "Troppo tempo su una risposta errata. Considera di saltare.";
        }
        if (qd.result === "correct" && qd.eliminated.length >= 2) {
            return "Eliminazione + risposta — strategia corretta!";
        }
        if (qd.result === "skip" && qd.timeSpent >= config.timeout * 0.95) {
            return "Tempo scaduto — prova a decidere prima.";
        }
        return "";
    }

    function renderStrategyFeedback(avgCorrectTime, avgWrongTime) {
        const list = document.getElementById("tt-strategy-list");
        list.innerHTML = "";
        const feedback = [];

        const totalCorrect = questionData.filter(q => q.result === "correct").length;
        const totalWrong = questionData.filter(q => q.result === "wrong").length;
        const totalSkipped = questionData.filter(q => q.result === "skip").length;
        const slowWrong = questionData.filter(q => q.result === "wrong" && q.timeSpent > config.timeout * 0.7).length;
        const elimGuesses = questionData.filter(q => q.result === "correct" && q.eliminated.length >= 2).length;
        const timedOut = questionData.filter(q => q.result === "skip" && q.timeSpent >= config.timeout * 0.95).length;

        if (slowWrong > 0) {
            feedback.push(
                `Hai speso troppo tempo su ${slowWrong} rispost${slowWrong === 1 ? "a" : "e"} errat${slowWrong === 1 ? "a" : "e"}. ` +
                `Dopo ${Math.round(config.timeout * 0.6)} secondi, considera di saltare o eliminare opzioni e indovinare.`
            );
        }

        if (elimGuesses > 0) {
            feedback.push(
                `Hai usato la strategia di eliminazione e indovinato correttamente ${elimGuesses} volt${elimGuesses === 1 ? "a" : "e"}. Ottima strategia!`
            );
        }

        if (timedOut > 1) {
            feedback.push(
                `Il timer e scaduto su ${timedOut} domande. Prova a prendere una decisione (anche saltare) prima dello scadere.`
            );
        }

        if (avgWrongTime > avgCorrectTime && avgWrongTime > 0 && avgCorrectTime > 0) {
            feedback.push(
                `Le risposte errate hanno richiesto in media ${Math.round(avgWrongTime)}s vs ${Math.round(avgCorrectTime)}s per le corrette. ` +
                `Se non sai la risposta dopo un minuto, probabilmente non la sai — meglio saltare.`
            );
        }

        if (totalSkipped > config.numQuestions * 0.5) {
            feedback.push(
                `Hai saltato piu della meta delle domande. Prova a eliminare opzioni e indovinare quando possibile.`
            );
        }

        if (totalCorrect >= config.numQuestions * 0.7) {
            feedback.push("Ottimo risultato! Il tuo ritmo e la tua strategia sono efficaci.");
        }

        if (totalWrong > totalCorrect && totalWrong > 2) {
            feedback.push(
                `Hai piu risposte errate che corrette. Ricorda: nel TOLC-B, ` +
                `saltare (0 punti) e meglio di sbagliare (-0,25 punti) se non sei sicuro.`
            );
        }

        if (feedback.length === 0) {
            feedback.push("Continua a esercitarti per migliorare la tua gestione del tempo!");
        }

        feedback.forEach(f => {
            const li = document.createElement("li");
            li.innerHTML = f;
            list.appendChild(li);
        });
    }

    function saveHistory(score, correct, wrong, skipped, avgTime) {
        try {
            const history = JSON.parse(localStorage.getItem("tolc_time_training_history") || "[]");
            history.push({
                date: new Date().toISOString(),
                score: score,
                correct: correct,
                wrong: wrong,
                skipped: skipped,
                avgTime: avgTime,
                numQuestions: config.numQuestions,
                timeout: config.timeout,
            });
            // Keep last 50 sessions
            if (history.length > 50) history.shift();
            localStorage.setItem("tolc_time_training_history", JSON.stringify(history));
        } catch (e) {
            // localStorage not available, ignore
        }
    }

    // ============ HELPERS ============

    function formatTime(seconds) {
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m}:${s.toString().padStart(2, "0")}`;
    }
});

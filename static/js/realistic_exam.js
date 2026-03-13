/* === TOLC-B Realistic Exam Mode === */
document.addEventListener("DOMContentLoaded", () => {
    const TOTAL_QUESTIONS = 20;
    const TOTAL_TIME = 50 * 60; // 50 minutes in seconds
    const EXERCISE_TYPES = window.EXERCISE_TYPES || {};
    const OPTION_LETTERS = ["A", "B", "C", "D", "E"];

    const TYPE_NAMES = {};
    for (const [key, val] of Object.entries(EXERCISE_TYPES)) {
        TYPE_NAMES[key] = val.name || key;
    }

    // Screens
    const startScreen = document.getElementById("sim-start");
    const activeScreen = document.getElementById("sim-active");
    const resultsScreen = document.getElementById("sim-results");

    // Controls
    const btnStart = document.getElementById("btn-start-sim");
    const btnSubmit = document.getElementById("btn-submit-sim");
    const btnPrev = document.getElementById("btn-prev");
    const btnNext = document.getElementById("btn-next");
    const btnSkip = document.getElementById("btn-skip");
    const btnAnswer = document.getElementById("btn-answer");
    const btnRetry = document.getElementById("btn-retry-sim");

    // Display elements
    const timerDisplay = document.getElementById("sim-timer");
    const timerFill = document.getElementById("sim-timer-fill");
    const progressDisplay = document.getElementById("sim-progress");
    const navigator = document.getElementById("sim-navigator");
    const questionArea = document.getElementById("sim-question-area");

    // State
    let exercises = [];
    let questionStates = []; // {answered, answer, correct, skipped, timeSpent, selectedAnswer}
    let currentIndex = 0;
    let timerInterval = null;
    let remainingTime = TOTAL_TIME;
    let questionStartTime = 0;

    // ============ SCREEN MANAGEMENT ============

    function showScreen(screen) {
        startScreen.classList.add("hidden");
        activeScreen.classList.add("hidden");
        resultsScreen.classList.add("hidden");
        screen.classList.remove("hidden");
    }

    // ============ START EXAM ============

    btnStart.addEventListener("click", startExam);
    if (btnRetry) btnRetry.addEventListener("click", startExam);

    async function startExam() {
        showScreen(activeScreen);
        questionArea.innerHTML = '<div class="loading">Caricamento domande...</div>';

        try {
            const res = await fetch("/api/realistic-exam/exercises");
            if (!res.ok) throw new Error("Errore nel caricamento delle domande");
            exercises = await res.json();
        } catch (err) {
            questionArea.innerHTML = `<div class="loading">Errore: ${err.message}</div>`;
            return;
        }

        // Initialize state
        questionStates = exercises.map(() => ({
            answered: false,
            answer: null,
            correct: null,
            skipped: false,
            timeSpent: 0,
            selectedAnswer: null,
        }));
        currentIndex = 0;
        remainingTime = TOTAL_TIME;

        buildNavigator();
        startTimer();
        renderCurrentQuestion();
    }

    // ============ TIMER ============

    function startTimer() {
        if (timerInterval) clearInterval(timerInterval);
        updateTimerDisplay();

        timerInterval = setInterval(() => {
            // Track time spent on current question
            const now = Date.now();
            if (questionStartTime > 0) {
                questionStates[currentIndex].timeSpent += (now - questionStartTime) / 1000;
                questionStartTime = now;
            }

            remainingTime--;
            updateTimerDisplay();

            if (remainingTime <= 0) {
                clearInterval(timerInterval);
                timerInterval = null;
                endExam();
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;
        timerDisplay.textContent = `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;

        const pct = (remainingTime / TOTAL_TIME) * 100;
        timerFill.style.width = `${pct}%`;

        // Color changes
        timerDisplay.classList.remove("sim-timer-warning", "sim-timer-danger");
        timerFill.classList.remove("warning", "danger");
        if (pct < 10) {
            timerDisplay.classList.add("sim-timer-danger");
            timerFill.classList.add("danger");
        } else if (pct < 25) {
            timerDisplay.classList.add("sim-timer-warning");
            timerFill.classList.add("warning");
        }
    }

    // ============ NAVIGATOR ============

    function buildNavigator() {
        navigator.innerHTML = "";
        for (let i = 0; i < TOTAL_QUESTIONS; i++) {
            const btn = document.createElement("button");
            btn.className = "sim-nav-btn";
            btn.textContent = i + 1;
            btn.setAttribute("aria-label", `Domanda ${i + 1}`);
            btn.addEventListener("click", () => goToQuestion(i));
            navigator.appendChild(btn);
        }
        updateNavigator();
    }

    function updateNavigator() {
        const buttons = navigator.querySelectorAll(".sim-nav-btn");
        buttons.forEach((btn, i) => {
            btn.classList.remove("sim-nav-current", "sim-nav-correct", "sim-nav-wrong", "sim-nav-skipped", "sim-nav-answered");
            const state = questionStates[i];
            if (i === currentIndex) {
                btn.classList.add("sim-nav-current");
            }
            if (state.answered) {
                btn.classList.add("sim-nav-answered");
            } else if (state.skipped) {
                btn.classList.add("sim-nav-skipped");
            }
        });
    }

    // ============ QUESTION RENDERING ============

    function goToQuestion(index) {
        // Save time for current question
        if (questionStartTime > 0) {
            const elapsed = (Date.now() - questionStartTime) / 1000;
            questionStates[currentIndex].timeSpent += elapsed;
        }

        currentIndex = index;
        renderCurrentQuestion();
    }

    function renderCurrentQuestion() {
        const ex = exercises[currentIndex];
        const state = questionStates[currentIndex];
        questionStartTime = Date.now();

        // Update progress
        progressDisplay.textContent = `Domanda ${currentIndex + 1} di ${TOTAL_QUESTIONS}`;

        // Update navigation buttons
        btnPrev.disabled = currentIndex === 0;
        btnNext.disabled = currentIndex === TOTAL_QUESTIONS - 1;

        // Build question HTML — clean exam-like format, text only
        let html = "";

        // Question number and type badge
        const typeName = TYPE_NAMES[ex.type] || ex.type;
        html += `<div class="sim-question-meta">`;
        html += `<span class="sim-type-badge">${typeName}</span>`;
        html += `<span class="sim-difficulty-badge">`;
        for (let i = 0; i < (ex.difficulty || 1); i++) html += "&#9733;";
        html += `</span>`;
        html += `</div>`;

        // Question text
        html += `<div class="question exam-question">${ex.question}</div>`;

        // SVG graph (if present for graph/geometry type questions)
        if (ex.graph_data) {
            html += `<div class="sim-graph-container">${ex.graph_data}</div>`;
        }

        // Options with letter labels (A, B, C, D, E) — always 5 options
        if (ex.options) {
            html += '<div class="options exam-options">';
            ex.options.forEach((opt, i) => {
                const letter = OPTION_LETTERS[i] || String.fromCharCode(65 + i);
                const isSelected = state.selectedAnswer === i;
                const selectedClass = isSelected ? " selected" : "";
                const lockedClass = state.answered ? " locked" : "";
                html += `<div class="option exam-option${selectedClass}${lockedClass}" data-index="${i}">`;
                html += `<span class="exam-option-letter">${letter}</span>`;
                html += `<span class="exam-option-text">${opt}</span>`;
                html += `</div>`;
            });
            html += "</div>";
        }

        questionArea.innerHTML = html;

        // Bind click handlers only if not yet answered
        if (!state.answered) {
            const options = questionArea.querySelectorAll(".exam-option");
            options.forEach(el => {
                el.addEventListener("click", () => {
                    if (state.answered) return;
                    options.forEach(s => s.classList.remove("selected"));
                    el.classList.add("selected");
                    state.selectedAnswer = parseInt(el.dataset.index);
                    btnAnswer.disabled = false;
                });
            });
        }

        // Update answer button state
        btnAnswer.disabled = state.answered || state.selectedAnswer === null;
        btnAnswer.textContent = state.answered ? "Risposta data" : "Rispondi";
        btnSkip.disabled = state.answered;

        updateNavigator();
    }

    // ============ ANSWER / SKIP / NAVIGATION ============

    btnAnswer.addEventListener("click", async () => {
        const state = questionStates[currentIndex];
        if (state.answered || state.selectedAnswer === null) return;

        // Lock in the answer by checking with backend
        const ex = exercises[currentIndex];
        try {
            const res = await fetch("/api/check", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    type: ex.type,
                    answer: state.selectedAnswer,
                    exercise: ex,
                }),
            });
            const result = await res.json();
            state.answered = true;
            state.answer = state.selectedAnswer;
            state.correct = result.correct;
            state.skipped = false;

            // Store extra info for the results report
            state.explanation = result.explanation || "";
            state.correct_index = result.correct_index;

            // Visual feedback: just dim the question and mark as answered (no green/red)
            btnAnswer.disabled = true;
            btnAnswer.textContent = "Risposta data";
            btnSkip.disabled = true;

            // Lock clicks on options
            questionArea.querySelectorAll(".exam-option").forEach(el => {
                el.classList.add("locked");
            });

            updateNavigator();

            // Auto-advance to next unanswered question
            autoAdvance();
        } catch (err) {
            console.error("Errore nella verifica:", err);
        }
    });

    btnSkip.addEventListener("click", () => {
        const state = questionStates[currentIndex];
        if (state.answered) return;
        state.skipped = true;
        state.selectedAnswer = null;
        updateNavigator();
        autoAdvance();
    });

    btnPrev.addEventListener("click", () => {
        if (currentIndex > 0) goToQuestion(currentIndex - 1);
    });

    btnNext.addEventListener("click", () => {
        if (currentIndex < TOTAL_QUESTIONS - 1) goToQuestion(currentIndex + 1);
    });

    function autoAdvance() {
        // Find next unanswered question
        for (let i = currentIndex + 1; i < TOTAL_QUESTIONS; i++) {
            if (!questionStates[i].answered) {
                goToQuestion(i);
                return;
            }
        }
        // Wrap around
        for (let i = 0; i < currentIndex; i++) {
            if (!questionStates[i].answered) {
                goToQuestion(i);
                return;
            }
        }
        // All answered, stay on current
        renderCurrentQuestion();
    }

    // ============ SUBMIT / END ============

    btnSubmit.addEventListener("click", () => {
        const unanswered = questionStates.filter(s => !s.answered && !s.skipped).length;
        let message = "Sei sicuro di voler consegnare?";
        if (unanswered > 0) {
            message += ` Hai ancora ${unanswered} domand${unanswered === 1 ? "a" : "e"} senza risposta.`;
        }
        if (confirm(message)) {
            endExam();
        }
    });

    function endExam() {
        // Stop timer
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }

        // Save final time for current question
        if (questionStartTime > 0) {
            questionStates[currentIndex].timeSpent += (Date.now() - questionStartTime) / 1000;
            questionStartTime = 0;
        }

        calculateResults();
        showScreen(resultsScreen);
    }

    // ============ RESULTS ============

    function calculateResults() {
        let totalCorrect = 0;
        let totalWrong = 0;
        let totalSkipped = 0;
        let totalScore = 0;
        let totalTime = 0;

        // Per-type aggregation
        const byType = {};

        questionStates.forEach((state, i) => {
            const type = exercises[i].type;
            if (!byType[type]) {
                byType[type] = { questions: 0, correct: 0, wrong: 0, skipped: 0, score: 0 };
            }
            byType[type].questions++;
            totalTime += state.timeSpent;

            if (state.answered) {
                if (state.correct) {
                    totalCorrect++;
                    totalScore += 1;
                    byType[type].correct++;
                    byType[type].score += 1;
                } else {
                    totalWrong++;
                    totalScore -= 0.25;
                    byType[type].wrong++;
                    byType[type].score -= 0.25;
                }
                // Record to global Storage for dashboard stats
                if (typeof Storage !== "undefined" && Storage.recordAnswer) {
                    Storage.recordAnswer(type, state.correct);
                }
            } else {
                totalSkipped++;
                byType[type].skipped++;
            }
        });

        const answeredCount = totalCorrect + totalWrong;
        const avgTime = answeredCount > 0 ? totalTime / answeredCount : 0;

        // Populate score
        document.getElementById("sim-score-value").textContent = totalScore.toFixed(2);
        const scoreCard = document.getElementById("sim-score-card");
        scoreCard.classList.remove("sim-score-good", "sim-score-mid", "sim-score-low");
        if (totalScore >= 14) {
            scoreCard.classList.add("sim-score-good");
        } else if (totalScore >= 8) {
            scoreCard.classList.add("sim-score-mid");
        } else {
            scoreCard.classList.add("sim-score-low");
        }

        document.getElementById("sim-results-subtitle").textContent =
            `Formato Esame Realistico — Tempo impiegato: ${formatTime(TOTAL_TIME - remainingTime)} su 50:00`;

        // Stats
        document.getElementById("sim-stat-correct").textContent = totalCorrect;
        document.getElementById("sim-stat-wrong").textContent = totalWrong;
        document.getElementById("sim-stat-skipped").textContent = totalSkipped;
        document.getElementById("sim-stat-avgtime").textContent = `${Math.round(avgTime)}s`;

        // Breakdown table
        const tbody = document.getElementById("sim-breakdown-body");
        tbody.innerHTML = "";
        for (const [type, data] of Object.entries(byType)) {
            const row = document.createElement("tr");
            const name = TYPE_NAMES[type] || type;
            row.innerHTML = `
                <td>${name}</td>
                <td>${data.questions}</td>
                <td>${data.correct}</td>
                <td>${data.wrong}</td>
                <td>${data.skipped}</td>
                <td class="${data.score >= 0 ? "score-positive" : "score-negative"}">${data.score.toFixed(2)}</td>
            `;
            tbody.appendChild(row);
        }

        // Total row
        const totalRow = document.createElement("tr");
        totalRow.className = "sim-breakdown-total";
        totalRow.innerHTML = `
            <td><strong>Totale</strong></td>
            <td><strong>${TOTAL_QUESTIONS}</strong></td>
            <td><strong>${totalCorrect}</strong></td>
            <td><strong>${totalWrong}</strong></td>
            <td><strong>${totalSkipped}</strong></td>
            <td class="${totalScore >= 0 ? "score-positive" : "score-negative"}"><strong>${totalScore.toFixed(2)}</strong></td>
        `;
        tbody.appendChild(totalRow);

        // Suggestions
        generateSuggestions(byType, totalScore, avgTime);

        // Review section
        generateReview();
    }

    function generateSuggestions(byType, totalScore, avgTime) {
        const list = document.getElementById("sim-suggestions-list");
        list.innerHTML = "";

        const suggestions = [];

        // Find weakest types (negative or lowest score)
        const typeScores = Object.entries(byType)
            .map(([type, data]) => ({
                type,
                name: TYPE_NAMES[type] || type,
                accuracy: data.questions > 0 ? data.correct / data.questions : 0,
                score: data.score,
                questions: data.questions,
                wrong: data.wrong,
                skipped: data.skipped,
            }))
            .sort((a, b) => a.accuracy - b.accuracy);

        // Worst types
        const weak = typeScores.filter(t => t.accuracy < 0.5);
        if (weak.length > 0) {
            weak.forEach(t => {
                suggestions.push(
                    `Concentrati su <strong>${t.name}</strong>: solo ${Math.round(t.accuracy * 100)}% di risposte corrette. ` +
                    `Pratica con il mini-gioco dedicato per migliorare.`
                );
            });
        }

        // Penalty alert
        const penaltyTypes = typeScores.filter(t => t.wrong > t.correct);
        if (penaltyTypes.length > 0) {
            penaltyTypes.forEach(t => {
                if (!weak.includes(t)) {
                    suggestions.push(
                        `In <strong>${t.name}</strong> le risposte errate superano quelle corrette. ` +
                        `Valuta di saltare le domande di cui non sei sicuro per evitare la penalita di -0,25.`
                    );
                }
            });
        }

        // Skipped questions
        const totalSkipped = typeScores.reduce((sum, t) => sum + t.skipped, 0);
        if (totalSkipped > 5) {
            suggestions.push(
                `Hai saltato ${totalSkipped} domande. Prova a praticare tutti i tipi di esercizio ` +
                `per sentirti piu sicuro durante l'esame.`
            );
        }

        // Time management
        if (avgTime > 180) {
            suggestions.push(
                `Il tempo medio per domanda e di ${Math.round(avgTime)} secondi (obiettivo: ~150s). ` +
                `Prova a gestire meglio il tempo nelle prossime prove.`
            );
        }

        // Score-based overall
        if (totalScore >= 16) {
            suggestions.push("Ottimo risultato! Sei ben preparato per il TOLC-B. Continua a esercitarti per mantenere il livello.");
        } else if (totalScore >= 10) {
            suggestions.push("Buon risultato, ma c'e margine di miglioramento. Concentrati sulle aree deboli identificate sopra.");
        } else if (totalScore >= 0) {
            suggestions.push("C'e ancora lavoro da fare. Pratica ogni tipo di esercizio separatamente prima di ripetere l'esame.");
        } else {
            suggestions.push(
                "Il punteggio negativo indica troppe risposte errate. " +
                "Strategia: meglio saltare una domanda che rischiare -0,25 su una risposta incerta."
            );
        }

        // Best type encouragement
        const best = typeScores[typeScores.length - 1];
        if (best && best.accuracy >= 0.8) {
            suggestions.push(
                `Eccellente in <strong>${best.name}</strong> (${Math.round(best.accuracy * 100)}%)! ` +
                `Questo e il tuo punto di forza.`
            );
        }

        suggestions.forEach(s => {
            const li = document.createElement("li");
            li.innerHTML = s;
            list.appendChild(li);
        });
    }

    function generateReview() {
        const reviewList = document.getElementById("sim-review-list");
        if (!reviewList) return;
        reviewList.innerHTML = "";

        questionStates.forEach((state, i) => {
            const ex = exercises[i];
            const typeName = TYPE_NAMES[ex.type] || ex.type;

            const div = document.createElement("div");
            div.className = "exam-review-item";

            // Status indicator
            let statusClass = "review-skipped";
            let statusText = "Saltata";
            if (state.answered) {
                statusClass = state.correct ? "review-correct" : "review-wrong";
                statusText = state.correct ? "Corretta" : "Errata";
            }

            let html = `<div class="exam-review-header ${statusClass}">`;
            html += `<span class="exam-review-number">Domanda ${i + 1}</span>`;
            html += `<span class="exam-review-type">${typeName}</span>`;
            html += `<span class="exam-review-status">${statusText}</span>`;
            html += `</div>`;

            html += `<div class="exam-review-question">${ex.question}</div>`;

            // SVG graph in review
            if (ex.graph_data) {
                html += `<div class="sim-graph-container">${ex.graph_data}</div>`;
            }

            // Show options with correct/wrong indicators
            if (ex.options) {
                html += '<div class="exam-review-options">';
                ex.options.forEach((opt, j) => {
                    const letter = OPTION_LETTERS[j] || String.fromCharCode(65 + j);
                    let optClass = "exam-review-option";
                    const correctIdx = state.correct_index !== undefined ? state.correct_index : ex.correct_index;
                    if (j === correctIdx) {
                        optClass += " exam-review-option-correct";
                    }
                    if (state.answered && j === state.answer && !state.correct) {
                        optClass += " exam-review-option-wrong";
                    }
                    html += `<div class="${optClass}"><span class="exam-option-letter">${letter}</span> ${opt}</div>`;
                });
                html += '</div>';
            }

            // Explanation
            if (state.explanation) {
                html += `<div class="exam-review-explanation">${state.explanation}</div>`;
            }

            // Did you know
            if (ex.did_you_know) {
                html += `<div class="exam-review-didyouknow"><strong>Lo sapevi?</strong> ${ex.did_you_know}</div>`;
            }

            div.innerHTML = html;
            reviewList.appendChild(div);
        });
    }

    // ============ HELPERS ============

    function formatTime(seconds) {
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
    }
});

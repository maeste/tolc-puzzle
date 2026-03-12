/* === Exercise page logic === */
document.addEventListener("DOMContentLoaded", () => {
    const type = window.EXERCISE_TYPE;
    let currentExercise = null;
    let selectedAnswer = null;
    let answered = false;
    let difficulty = 1;
    let timer = null;

    const exerciseArea = document.getElementById("exercise-area");
    const feedbackArea = document.getElementById("feedback-area");
    const btnCheck = document.getElementById("btn-check");
    const btnNext = document.getElementById("btn-next");
    const btnSkip = document.getElementById("btn-skip");
    const timerBar = document.getElementById("timer-bar");

    // Difficulty selector
    document.querySelectorAll(".diff-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".diff-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            difficulty = parseInt(btn.dataset.diff);
            loadExercise();
        });
    });

    // Timer setup
    function setupTimer(exerciseData) {
        const mode = Storage.getMode();
        if (timer) timer.stop();

        // Check if exercise has its own time_limit (e.g. Stima Flash)
        const hasTimeLimit = exerciseData && exerciseData.time_limit;

        if (mode === "zen" && !hasTimeLimit) {
            timerBar.classList.add("hidden");
            timerBar.classList.remove("timer-exam", "timer-relaxed");
            return;
        }

        timerBar.classList.remove("hidden", "timer-exam", "timer-relaxed");
        if (hasTimeLimit) {
            timerBar.classList.add("timer-exam");
        } else if (mode === "exam") {
            timerBar.classList.add("timer-exam");
        } else {
            timerBar.classList.add("timer-relaxed");
        }

        const fill = timerBar.querySelector(".timer-fill");
        const text = timerBar.querySelector(".timer-text");
        const isExamStyle = timerBar.classList.contains("timer-exam");

        timer = new Timer(mode,
            (remaining, pct) => {
                fill.style.width = `${pct}%`;
                let cls = "timer-fill";
                if (isExamStyle) {
                    cls += " exam-fill";
                    if (pct < 25) cls += " danger-pulse";
                    else if (pct < 50) cls += " danger";
                } else {
                    if (pct < 20) cls += " danger";
                    else if (pct < 40) cls += " warning";
                }
                fill.className = cls;
                const min = Math.floor(remaining / 60);
                const sec = remaining % 60;
                text.textContent = `${min}:${sec.toString().padStart(2, "0")}`;
            },
            () => {
                if (!answered) showFeedback(false, "⏰ Tempo scaduto! Non preoccuparti, ogni tentativo conta.");
            }
        );

        if (hasTimeLimit) {
            timer.setOverrideDuration(exerciseData.time_limit);
        }
    }

    window.addEventListener("modechange", () => { loadExercise(); });

    // Load exercise
    async function loadExercise() {
        answered = false;
        selectedAnswer = null;
        feedbackArea.classList.add("hidden");
        feedbackArea.classList.remove("correct", "wrong");
        btnCheck.disabled = true;
        btnCheck.classList.remove("hidden");
        btnNext.classList.add("hidden");
        exerciseArea.innerHTML = '<div class="loading">Caricamento...</div>';

        try {
            const res = await fetch(`/api/exercise/${type}?difficulty=${difficulty}`);
            if (!res.ok) throw new Error("Errore caricamento");
            currentExercise = await res.json();
            renderExercise(currentExercise);
            setupTimer(currentExercise);
            if (timer) timer.start();
        } catch (err) {
            exerciseArea.innerHTML = `<div class="loading">Errore: ${err.message}</div>`;
        }
    }

    // Render exercise
    function renderExercise(ex) {
        let html = `<div class="question">${ex.question}</div>`;

        if (ex.steps) {
            html += '<div class="steps">';
            ex.steps.forEach((step, i) => {
                html += `<div class="step" data-index="${i}">Passo ${i + 1}: ${step}</div>`;
            });
            html += '</div>';
        }

        if (ex.options) {
            html += '<div class="options">';
            ex.options.forEach((opt, i) => {
                html += `<div class="option" data-index="${i}">${opt}</div>`;
            });
            html += '</div>';
        }

        if (ex.graph_data) {
            html += `<div class="graph-container">${ex.graph_data}</div>`;
        }

        exerciseArea.innerHTML = html;

        // Bind click handlers
        if (ex.steps) {
            exerciseArea.querySelectorAll(".step").forEach(el => {
                el.addEventListener("click", () => {
                    if (answered) return;
                    exerciseArea.querySelectorAll(".step").forEach(s => s.classList.remove("selected"));
                    el.classList.add("selected");
                    selectedAnswer = parseInt(el.dataset.index);
                    btnCheck.disabled = false;
                });
            });
        }
        if (ex.options) {
            exerciseArea.querySelectorAll(".option").forEach(el => {
                el.addEventListener("click", () => {
                    if (answered) return;
                    exerciseArea.querySelectorAll(".option").forEach(o => o.classList.remove("selected"));
                    el.classList.add("selected");
                    selectedAnswer = parseInt(el.dataset.index);
                    btnCheck.disabled = false;
                });
            });
        }
    }

    // Check answer
    btnCheck.addEventListener("click", async () => {
        if (selectedAnswer === null || answered) return;
        if (timer) timer.stop();

        try {
            const res = await fetch("/api/check", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    type: type,
                    answer: selectedAnswer,
                    exercise: currentExercise
                })
            });
            const result = await res.json();
            showFeedback(result.correct, result.explanation, result.did_you_know);

            // Highlight correct/wrong in UI
            if (currentExercise.options) {
                exerciseArea.querySelectorAll(".option").forEach((el, i) => {
                    if (i === result.correct_index) el.classList.add("correct");
                    else if (i === selectedAnswer && !result.correct) el.classList.add("wrong");
                });
            }
            if (currentExercise.steps) {
                exerciseArea.querySelectorAll(".step").forEach((el, i) => {
                    if (i === result.correct_index) el.classList.add("selected", "correct");
                });
            }

            if (result.correct) {
                Storage.recordAnswer(type, true);
            } else {
                const givenLabel = currentExercise.options
                    ? currentExercise.options[selectedAnswer]
                    : currentExercise.steps
                        ? `Passo ${selectedAnswer + 1}: ${currentExercise.steps[selectedAnswer]}`
                        : String(selectedAnswer);
                const correctLabel = currentExercise.options
                    ? currentExercise.options[result.correct_index]
                    : currentExercise.steps
                        ? `Passo ${result.correct_index + 1}: ${currentExercise.steps[result.correct_index]}`
                        : String(result.correct_index);
                Storage.recordAnswer(type, false, {
                    question: currentExercise.question,
                    givenAnswer: givenLabel,
                    correctAnswer: correctLabel,
                    explanation: result.explanation || "",
                    didYouKnow: result.did_you_know || ""
                });
            }
        } catch (err) {
            showFeedback(false, "Errore nella verifica della risposta.");
        }
    });

    function showFeedback(correct, explanation, didYouKnow) {
        answered = true;
        feedbackArea.classList.remove("hidden", "correct", "wrong");
        feedbackArea.classList.add(correct ? "correct" : "wrong");

        let html = `<div class="feedback-title">${correct ? "✅ Perfetto!" : "💡 Quasi! Ecco la spiegazione:"}</div>`;
        html += `<div class="feedback-explanation">${explanation}</div>`;
        if (didYouKnow) {
            html += `<div class="did-you-know">💡 <strong>Lo sapevi che?</strong> ${didYouKnow}</div>`;
        }
        feedbackArea.innerHTML = html;

        btnCheck.classList.add("hidden");
        btnNext.classList.remove("hidden");
    }

    btnNext.addEventListener("click", loadExercise);
    btnSkip.addEventListener("click", loadExercise);

    // Initial load
    loadExercise();
});

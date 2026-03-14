/* === Daily Session Mode === */
/* SRS-driven daily review session with immediate feedback. */

document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    var sessionStatus = document.getElementById("session-status");
    var exerciseArea = document.getElementById("exercise-area");
    var feedbackArea = document.getElementById("feedback-area");
    var exerciseActions = document.getElementById("exercise-actions");
    var btnCheck = document.getElementById("btn-check");
    var btnNext = document.getElementById("btn-next");
    var sessionReport = document.getElementById("session-report");
    var progressBar = document.getElementById("session-progress");
    var progressFill = document.getElementById("session-progress-fill");
    var progressText = document.getElementById("session-progress-text");

    var exercises = [];
    var currentIndex = 0;
    var selectedAnswer = null;
    var answered = false;
    var currentExercise = null;
    var exerciseStartTime = 0;

    /* Per-exercise tracking */
    var results = []; /* {correct: bool, timeMs: number, type: string} */

    /* --- Initialize SRS --- */
    if (window.SRSTracker) { SRSTracker.init(); }
    if (window.SRSReconsolidation) { SRSReconsolidation.init(); }

    /* --- Start session --- */
    startSession();

    function startSession() {
        var sessionPlan = [];
        if (window.SRSScheduler) {
            sessionPlan = SRSScheduler.getRecommendedSession(15);
        }

        if (!sessionPlan || sessionPlan.length === 0) {
            showEmptySession();
            return;
        }

        sessionStatus.innerHTML = '<div class="loading">Caricamento esercizi...</div>';

        var url = "/api/daily-session/exercises?count=15&session=" + encodeURIComponent(JSON.stringify(sessionPlan));

        fetch(url)
            .then(function (res) {
                if (!res.ok) throw new Error("Errore caricamento");
                return res.json();
            })
            .then(function (data) {
                exercises = data;
                if (exercises.length === 0) {
                    showEmptySession();
                    return;
                }
                sessionStatus.classList.add("hidden");
                progressBar.classList.remove("hidden");
                exerciseActions.classList.remove("hidden");
                showExercise(0);
            })
            .catch(function (err) {
                sessionStatus.innerHTML = '<div class="loading">Errore: ' + err.message + '</div>';
            });
    }

    function showEmptySession() {
        var summary = null;
        if (window.SRSScheduler) {
            summary = SRSScheduler.getSummary();
        }
        var msg = "Tutto ripassato!";
        if (summary && summary.nextDueIn !== null) {
            msg += " Prossima sessione tra " + formatMinutes(summary.nextDueIn) + ".";
        }
        sessionStatus.innerHTML =
            '<div style="text-align:center;padding:3rem 1rem;">' +
            '<div style="font-size:3rem;margin-bottom:1rem;">&#10003;</div>' +
            '<h2>' + msg + '</h2>' +
            '<p style="color:var(--text-light);margin-top:0.5rem;">Torna piu tardi o esercitati liberamente dalla dashboard.</p>' +
            '<a href="/" class="btn btn-primary" style="margin-top:1.5rem;">Torna alla Dashboard</a>' +
            '</div>';
    }

    function showExercise(index) {
        currentIndex = index;
        currentExercise = exercises[index];
        selectedAnswer = null;
        answered = false;

        feedbackArea.classList.add("hidden");
        feedbackArea.classList.remove("correct", "wrong");
        btnCheck.disabled = true;
        btnCheck.classList.remove("hidden");
        btnNext.classList.add("hidden");
        exerciseArea.classList.remove("hidden");

        updateProgress();
        renderExercise(currentExercise);
        exerciseStartTime = Date.now();
    }

    function updateProgress() {
        var pct = ((currentIndex) / exercises.length) * 100;
        progressFill.style.width = pct + "%";
        progressText.textContent = (currentIndex + 1) + " / " + exercises.length;
    }

    function renderExercise(ex) {
        var html = '';

        /* Type and difficulty badge */
        var typeName = ex.type;
        if (window.EXERCISE_TYPES && window.EXERCISE_TYPES[ex.type]) {
            typeName = window.EXERCISE_TYPES[ex.type].icon + " " + window.EXERCISE_TYPES[ex.type].name;
        }
        html += '<div class="sim-question-meta">';
        html += '<span class="sim-type-badge">' + typeName + '</span>';
        var stars = "";
        for (var s = 0; s < (ex.difficulty || 1); s++) { stars += "\u2B50"; }
        html += '<span class="sim-difficulty-badge">' + stars + '</span>';
        if (ex.reason) {
            var reasonLabels = { "overdue": "Da ripassare", "new": "Nuovo", "review": "Ripasso", "practice": "Pratica" };
            html += '<span class="sim-type-badge" style="background:#fef3c7;color:#92400e;">' + (reasonLabels[ex.reason] || ex.reason) + '</span>';
        }
        html += '</div>';

        html += '<div class="question">' + ex.question + '</div>';

        if (ex.graph_data) {
            html += '<div class="graph-container">' + ex.graph_data + '</div>';
        }

        if (ex.steps) {
            html += '<div class="steps">';
            for (var i = 0; i < ex.steps.length; i++) {
                html += '<div class="step" data-index="' + i + '">Passo ' + (i + 1) + ': ' + ex.steps[i] + '</div>';
            }
            html += '</div>';
        }

        if (ex.options) {
            html += '<div class="options">';
            for (var j = 0; j < ex.options.length; j++) {
                html += '<div class="option" data-index="' + j + '">' + ex.options[j] + '</div>';
            }
            html += '</div>';
        }

        exerciseArea.innerHTML = html;

        /* Bind click handlers */
        if (ex.steps) {
            var steps = exerciseArea.querySelectorAll(".step");
            for (var si = 0; si < steps.length; si++) {
                (function (el) {
                    el.addEventListener("click", function () {
                        if (answered) return;
                        var allSteps = exerciseArea.querySelectorAll(".step");
                        for (var k = 0; k < allSteps.length; k++) { allSteps[k].classList.remove("selected"); }
                        el.classList.add("selected");
                        selectedAnswer = parseInt(el.dataset.index);
                        btnCheck.disabled = false;
                    });
                })(steps[si]);
            }
        }
        if (ex.options) {
            var opts = exerciseArea.querySelectorAll(".option");
            for (var oi = 0; oi < opts.length; oi++) {
                (function (el) {
                    el.addEventListener("click", function () {
                        if (answered) return;
                        var allOpts = exerciseArea.querySelectorAll(".option");
                        for (var k = 0; k < allOpts.length; k++) { allOpts[k].classList.remove("selected"); }
                        el.classList.add("selected");
                        selectedAnswer = parseInt(el.dataset.index);
                        btnCheck.disabled = false;
                    });
                })(opts[oi]);
            }
        }
    }

    /* --- Check answer --- */
    btnCheck.addEventListener("click", function () {
        if (selectedAnswer === null || answered) return;

        var timeMs = Date.now() - exerciseStartTime;

        fetch("/api/check", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                type: currentExercise.type,
                answer: selectedAnswer,
                exercise: currentExercise
            })
        })
        .then(function (res) { return res.json(); })
        .then(function (result) {
            answered = true;
            var correct = !!result.correct;

            /* Record in results */
            results.push({
                correct: correct,
                timeMs: timeMs,
                type: currentExercise.type,
                difficulty: currentExercise.difficulty || 2
            });

            /* Set globals for Storage.recordAnswer SRS hooks */
            window._currentDifficulty = currentExercise.difficulty || 2;
            window._currentTimeMs = timeMs;

            /* Record via Storage (fires SRSTracker + SRSReconsolidation) */
            if (correct) {
                Storage.recordAnswer(currentExercise.type, true);
            } else {
                var givenLabel = currentExercise.options
                    ? currentExercise.options[selectedAnswer]
                    : currentExercise.steps
                        ? "Passo " + (selectedAnswer + 1) + ": " + currentExercise.steps[selectedAnswer]
                        : String(selectedAnswer);
                var correctLabel = currentExercise.options
                    ? currentExercise.options[result.correct_index]
                    : currentExercise.steps
                        ? "Passo " + (result.correct_index + 1) + ": " + currentExercise.steps[result.correct_index]
                        : String(result.correct_index);
                Storage.recordAnswer(currentExercise.type, false, {
                    question: currentExercise.question,
                    givenAnswer: givenLabel,
                    correctAnswer: correctLabel,
                    explanation: result.explanation || "",
                    didYouKnow: result.did_you_know || ""
                });
            }

            /* Show feedback */
            showFeedback(correct, result.explanation, result.did_you_know, result.correct_index);
        })
        .catch(function () {
            showFeedback(false, "Errore nella verifica della risposta.", null, null);
        });
    });

    function showFeedback(correct, explanation, didYouKnow, correctIndex) {
        feedbackArea.classList.remove("hidden", "correct", "wrong");
        feedbackArea.classList.add(correct ? "correct" : "wrong");

        var html = '<div class="feedback-title">' + (correct ? "&#10004; Perfetto!" : "&#128161; Quasi! Ecco la spiegazione:") + '</div>';
        html += '<div class="feedback-explanation">' + (explanation || "") + '</div>';
        if (didYouKnow) {
            html += '<div class="did-you-know">&#128161; <strong>Lo sapevi che?</strong> ' + didYouKnow + '</div>';
        }
        feedbackArea.innerHTML = html;

        /* Highlight correct/wrong in exercise area */
        if (currentExercise.options && correctIndex !== null && correctIndex !== undefined) {
            var opts = exerciseArea.querySelectorAll(".option");
            for (var i = 0; i < opts.length; i++) {
                if (i === correctIndex) opts[i].classList.add("correct");
                else if (i === selectedAnswer && !correct) opts[i].classList.add("wrong");
            }
        }
        if (currentExercise.steps && correctIndex !== null && correctIndex !== undefined) {
            var steps = exerciseArea.querySelectorAll(".step");
            for (var j = 0; j < steps.length; j++) {
                if (j === correctIndex) steps[j].classList.add("selected", "correct");
            }
        }

        btnCheck.classList.add("hidden");

        if (currentIndex < exercises.length - 1) {
            btnNext.textContent = "Prossimo \u2192";
        } else {
            btnNext.textContent = "Vedi risultati \u2192";
        }
        btnNext.classList.remove("hidden");
    }

    /* --- Next exercise --- */
    btnNext.addEventListener("click", function () {
        if (currentIndex < exercises.length - 1) {
            showExercise(currentIndex + 1);
        } else {
            showReport();
        }
    });

    /* --- Session Report --- */
    function showReport() {
        exerciseArea.classList.add("hidden");
        feedbackArea.classList.add("hidden");
        exerciseActions.classList.add("hidden");
        progressBar.classList.add("hidden");
        sessionReport.classList.remove("hidden");

        var totalCorrect = 0;
        var totalTime = 0;
        var improvedTypes = {};

        for (var i = 0; i < results.length; i++) {
            if (results[i].correct) {
                totalCorrect++;
                improvedTypes[results[i].type] = true;
            }
            totalTime += results[i].timeMs;
        }

        var avgTime = results.length > 0 ? Math.round(totalTime / results.length / 1000) : 0;
        var accuracy = results.length > 0 ? Math.round((totalCorrect / results.length) * 100) : 0;

        var scoreClass = accuracy >= 70 ? "sim-score-good" : accuracy >= 50 ? "sim-score-mid" : "sim-score-low";

        var html = '';
        html += '<div class="sim-results-header"><h1>&#128202; Report Sessione</h1></div>';

        /* Score card */
        html += '<div class="sim-score-card ' + scoreClass + '">';
        html += '<div class="sim-score-value">' + totalCorrect + '/' + results.length + '</div>';
        html += '<div class="sim-score-label">' + accuracy + '% di precisione</div>';
        html += '</div>';

        /* Stats row */
        html += '<div class="sim-stats-row">';
        html += '<div class="sim-stat-card sim-stat-correct"><div class="sim-stat-number">' + totalCorrect + '</div><div class="sim-stat-label">Corrette</div></div>';
        html += '<div class="sim-stat-card sim-stat-wrong"><div class="sim-stat-number">' + (results.length - totalCorrect) + '</div><div class="sim-stat-label">Sbagliate</div></div>';
        html += '<div class="sim-stat-card sim-stat-time"><div class="sim-stat-number">' + avgTime + 's</div><div class="sim-stat-label">Tempo medio</div></div>';
        html += '<div class="sim-stat-card"><div class="sim-stat-number">' + Object.keys(improvedTypes).length + '</div><div class="sim-stat-label">Aree esercitate</div></div>';
        html += '</div>';

        /* Areas improved */
        var improvedKeys = Object.keys(improvedTypes);
        if (improvedKeys.length > 0) {
            html += '<div class="sim-suggestions" style="margin-top:1.5rem;"><h2>&#9989; Aree migliorate</h2><ul>';
            for (var t = 0; t < improvedKeys.length; t++) {
                var tName = improvedKeys[t];
                if (window.EXERCISE_TYPES && window.EXERCISE_TYPES[tName]) {
                    tName = window.EXERCISE_TYPES[tName].icon + " " + window.EXERCISE_TYPES[tName].name;
                }
                html += '<li>' + tName + '</li>';
            }
            html += '</ul></div>';
        }

        /* Next session info */
        if (window.SRSScheduler) {
            var summary = SRSScheduler.getSummary();
            html += '<div class="sim-suggestions" style="margin-top:1rem;"><h2>&#128197; Prossima sessione</h2><ul>';
            if (summary.overdueCount > 0) {
                html += '<li>Hai ancora ' + summary.overdueCount + ' esercizi da ripassare</li>';
            }
            if (summary.nextDueIn !== null) {
                html += '<li>Prossimo ripasso tra ' + formatMinutes(summary.nextDueIn) + '</li>';
            }
            if (summary.avgRetention > 0) {
                html += '<li>Ritenzione media: ' + Math.round(summary.avgRetention * 100) + '%</li>';
            }
            html += '</ul></div>';
        }

        /* Actions */
        html += '<div class="sim-results-actions" style="margin-top:1.5rem;">';
        html += '<a href="/" class="btn btn-primary">Torna alla Dashboard</a>';
        html += '<a href="/daily-session" class="btn btn-secondary">Nuova sessione</a>';
        html += '</div>';

        sessionReport.innerHTML = html;
    }

    function formatMinutes(minutes) {
        if (minutes === null || minutes === undefined) return "";
        if (minutes < 60) return Math.round(minutes) + " minuti";
        if (minutes < 1440) return Math.round(minutes / 60) + " ore";
        return Math.round(minutes / 1440) + " giorni";
    }
});

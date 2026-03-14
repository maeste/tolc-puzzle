/* === Storage helpers === */
const Storage = {
    getProgress() {
        try {
            return JSON.parse(localStorage.getItem("tolc_progress") || "{}");
        } catch { return {}; }
    },
    saveProgress(data) {
        localStorage.setItem("tolc_progress", JSON.stringify(data));
    },
    getMode() {
        return localStorage.getItem("tolc_mode") || "zen";
    },
    setMode(mode) {
        localStorage.setItem("tolc_mode", mode);
    },
    recordAnswer(type, correct, wrongDetail) {
        const progress = this.getProgress();
        if (!progress[type]) {
            progress[type] = { completed: 0, correct: 0, streak: 0, bestStreak: 0 };
        }
        const p = progress[type];
        p.completed++;
        if (correct) {
            p.correct++;
            p.streak++;
            if (p.streak > p.bestStreak) p.bestStreak = p.streak;
        } else {
            p.streak = 0;
            if (wrongDetail) this.recordWrong(type, wrongDetail);
        }
        this.saveProgress(progress);

        /* SRS Tracker integration */
        if (window.SRSTracker) {
            var diff = window._currentDifficulty || 2;
            var timeMs = window._currentTimeMs || 0;
            SRSTracker.recordAnswer(type, diff, correct, timeMs);
        }

        /* SRS Reconsolidation integration */
        if (window.SRSReconsolidation) {
            var reconDiff = window._currentDifficulty || 2;
            if (correct) {
                SRSReconsolidation.onCorrectAnswer(type, reconDiff);
            } else {
                SRSReconsolidation.onWrongAnswer(type, reconDiff);
            }
        }

        return p;
    },
    /* --- Wrong answers log --- */
    getWrongAnswers() {
        try {
            return JSON.parse(localStorage.getItem("tolc_wrong") || "{}");
        } catch { return {}; }
    },
    recordWrong(type, detail) {
        const wrong = this.getWrongAnswers();
        if (!wrong[type]) wrong[type] = [];
        /* Keep last 50 per type to avoid localStorage bloat */
        if (wrong[type].length >= 50) wrong[type].shift();
        detail.timestamp = Date.now();
        wrong[type].push(detail);
        localStorage.setItem("tolc_wrong", JSON.stringify(wrong));
    },
    clearWrongAnswers() {
        localStorage.removeItem("tolc_wrong");
    }
};

/* === Mode selector === */
document.addEventListener("DOMContentLoaded", () => {
    const currentMode = Storage.getMode();
    document.querySelectorAll(".mode-btn").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.mode === currentMode);
        btn.addEventListener("click", () => {
            document.querySelectorAll(".mode-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            Storage.setMode(btn.dataset.mode);
            window.dispatchEvent(new CustomEvent("modechange", { detail: btn.dataset.mode }));
        });
    });

    updateDashboardStats();
    updateSuggestion();
});

/* === Dashboard stats === */
function updateDashboardStats() {
    const progress = Storage.getProgress();
    document.querySelectorAll(".exercise-card").forEach(card => {
        const type = card.dataset.type;
        const p = progress[type];
        if (!p) return;
        const completed = card.querySelector('[data-stat="completed"]');
        const accuracy = card.querySelector('[data-stat="accuracy"]');
        const streak = card.querySelector('[data-stat="streak"]');
        const fill = card.querySelector(".progress-fill");
        if (completed) completed.textContent = `${p.completed} completati`;
        if (accuracy && p.completed > 0) {
            accuracy.textContent = `${Math.round(p.correct / p.completed * 100)}%`;
        }
        if (streak) streak.textContent = `🔥 ${p.bestStreak}`;
        if (fill) {
            const acc = p.completed > 0 ? p.correct / p.completed : 0;
            const mastered = p.completed >= 30 && acc >= 0.75;
            /* Bar shows accuracy %, but only fills to 100% if >= 30 completed */
            const pct = p.completed >= 30
                ? Math.round(acc * 100)
                : Math.min(Math.round(acc * 100), Math.round((p.completed / 30) * 100));
            fill.style.width = `${Math.min(100, pct)}%`;
            fill.classList.toggle("mastered", mastered);
            fill.classList.toggle("not-mastered", !mastered);
        }
    });
}

function updateSuggestion() {
    const progress = Storage.getProgress();
    const suggestion = document.getElementById("suggestion");
    if (!suggestion) return;

    const typeNames = window.EXERCISE_TYPES || {};
    const allTypes = Object.keys(typeNames);

    /* If no progress at all, show generic encouragement */
    if (Object.keys(progress).length === 0) {
        suggestion.textContent = "💡 Inizia con qualsiasi esercizio — non c'è un ordine obbligatorio!";
        suggestion.classList.add("visible");
        return;
    }

    /* Find types never attempted */
    const unpracticed = allTypes.filter(t => !progress[t] || progress[t].completed === 0);
    if (unpracticed.length > 0) {
        const name = typeNames[unpracticed[0]] ? typeNames[unpracticed[0]].name : unpracticed[0];
        suggestion.textContent = `💡 Non hai ancora provato: ${name} — inizia ora!`;
        suggestion.classList.add("visible");
        return;
    }

    /* Find type with lowest accuracy */
    let worst = null;
    let worstAcc = 1;
    for (const [type, p] of Object.entries(progress)) {
        if (p.completed > 0) {
            const acc = p.correct / p.completed;
            if (acc < worstAcc) { worstAcc = acc; worst = type; }
        }
    }
    if (worst && worstAcc < 0.7) {
        const name = typeNames[worst] ? typeNames[worst].name : worst;
        suggestion.textContent = `💡 Dovresti praticare di più: ${name} (${Math.round(worstAcc * 100)}% di precisione)`;
        suggestion.classList.add("visible");
    }
}

/* === Timer === */
class Timer {
    constructor(mode, onTick, onExpire) {
        this.mode = mode;
        this.onTick = onTick;
        this.onExpire = onExpire;
        this.interval = null;
        this.remaining = 0;
        this.total = 0;
        this.overrideDuration = null;
    }

    /** Allow exercise-specific time_limit to override mode duration. */
    setOverrideDuration(seconds) {
        this.overrideDuration = seconds;
    }

    start() {
        this.stop();
        if (this.mode === "zen" && !this.overrideDuration) return;
        if (this.overrideDuration) {
            this.total = this.overrideDuration;
        } else {
            this.total = this.mode === "relaxed" ? 240 : 150;
        }
        this.remaining = this.total;
        if (this.onTick) this.onTick(this.remaining, 100);
        this.interval = setInterval(() => {
            this.remaining--;
            const pct = (this.remaining / this.total) * 100;
            if (this.onTick) this.onTick(this.remaining, pct);
            if (this.remaining <= 0) {
                this.stop();
                if (this.onExpire) this.onExpire();
            }
        }, 1000);
    }

    stop() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
        this.overrideDuration = null;
    }
}

window.Storage = Storage;
window.Timer = Timer;

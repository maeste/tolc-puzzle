document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("results-content");
    const progress = Storage.getProgress();
    const wrong = Storage.getWrongAnswers();
    const types = window.EXERCISE_TYPES || {};

    if (Object.keys(progress).length === 0) {
        container.innerHTML = '<div class="result-card"><p>Nessun progresso ancora. Inizia a fare esercizi!</p></div>';
        return;
    }

    /* Build per-difficulty stats from SRS history */
    if (window.SRSTracker) { try { SRSTracker.init(); } catch(e) {} }
    const srsHistory = window.SRSTracker ? SRSTracker.getHistory() : [];
    const diffByType = {};
    srsHistory.forEach(h => {
        if (!diffByType[h.type]) diffByType[h.type] = {};
        const d = h.difficulty || 2;
        if (!diffByType[h.type][d]) diffByType[h.type][d] = { completed: 0, correct: 0 };
        diffByType[h.type][d].completed++;
        if (h.correct) diffByType[h.type][d].correct++;
    });

    let html = "";
    for (const [type, p] of Object.entries(progress)) {
        const meta = types[type] || { icon: "", name: type };
        const accRaw = p.completed > 0 ? p.correct / p.completed : 0;
        const acc = Math.round(accRaw * 100);
        const mastered = p.completed >= 30 && accRaw >= 0.75;
        const barClass = mastered ? "mastered" : "not-mastered";
        const wrongCount = (wrong[type] || []).length;

        /* Per-difficulty breakdown rows */
        let diffRows = "";
        const diffs = diffByType[type] || {};
        for (const d of [1, 2, 3]) {
            const ds = diffs[d];
            if (!ds || ds.completed === 0) continue;
            const dAcc = Math.round(ds.correct / ds.completed * 100);
            const stars = "⭐".repeat(d);
            diffRows += `<div class="diff-row">
                <span class="diff-stars">${stars}</span>
                <span>Completati: <strong>${ds.completed}</strong></span>
                <span>Corretti: <strong>${ds.correct}</strong></span>
                <span>Precisione: <strong>${dAcc}%</strong></span>
            </div>`;
        }

        html += `
        <div class="result-card">
            <div class="result-card-header">
                <span class="result-icon">${meta.icon}</span>
                <h3>${meta.name}</h3>
                ${mastered ? '<span class="mastery-badge">Padronanza raggiunta</span>' : `<span class="mastery-pending">Min. 30 esercizi e 75% precisione</span>`}
            </div>
            <div class="result-stats">
                <span>Completati: <strong>${p.completed}</strong></span>
                <span>Corretti: <strong>${p.correct}</strong></span>
                <span>Precisione: <strong>${acc}%</strong></span>
                <span>Streak migliore: <strong>🔥 ${p.bestStreak}</strong></span>
            </div>
            <div class="progress-bar"><div class="progress-fill ${barClass}" style="width:${acc}%"></div></div>
            ${diffRows ? `<div class="difficulty-breakdown">${diffRows}</div>` : ""}
            ${wrongCount > 0
                ? `<button class="btn btn-secondary btn-review" data-type="${type}">Rivedi ${wrongCount} errori</button>`
                : `<p class="no-errors">Nessun errore registrato</p>`
            }
        </div>`;
    }
    container.innerHTML = html;

    /* --- Modal logic --- */
    const modal = document.getElementById("wrong-modal");
    const modalTitle = document.getElementById("modal-title");
    const modalBody = document.getElementById("modal-body");
    const modalClose = document.getElementById("modal-close");

    /* Build a lookup: timestamp → difficulty from SRS history for old wrong entries */
    const tsToDiff = {};
    srsHistory.forEach(h => {
        if (!h.correct) tsToDiff[h.ts] = h.difficulty || 2;
    });

    function resolveDifficulty(item) {
        if (item.difficulty) return item.difficulty;
        /* Try matching by timestamp (within 2s tolerance) */
        const ts = item.timestamp;
        if (ts && tsToDiff[ts]) return tsToDiff[ts];
        for (const key of Object.keys(tsToDiff)) {
            if (Math.abs(Number(key) - ts) < 2000) return tsToDiff[key];
        }
        return 2;
    }

    function openModal(type) {
        const items = (wrong[type] || []).slice().reverse(); /* most recent first */
        const meta = types[type] || { icon: "", name: type };
        modalTitle.textContent = `${meta.icon} Errori — ${meta.name}`;

        if (items.length === 0) {
            modalBody.innerHTML = "<p>Nessun errore registrato per questa categoria.</p>";
        } else {
            modalBody.innerHTML = items.map((item, i) => {
                const diff = resolveDifficulty(item);
                return `
                <div class="wrong-item">
                    <div class="wrong-number">#${items.length - i} <span class="wrong-difficulty">${"⭐".repeat(diff)}</span></div>
                    <div class="wrong-question">${item.question}</div>
                    <div class="wrong-answers">
                        <div class="wrong-given">
                            <span class="wrong-label">La tua risposta:</span>
                            <span class="wrong-value bad">${item.givenAnswer}</span>
                        </div>
                        <div class="wrong-correct">
                            <span class="wrong-label">Risposta corretta:</span>
                            <span class="wrong-value good">${item.correctAnswer}</span>
                        </div>
                    </div>
                    <div class="wrong-explanation">${item.explanation}</div>
                    ${item.didYouKnow ? `<div class="did-you-know">💡 <strong>Lo sapevi che?</strong> ${item.didYouKnow}</div>` : ""}
                </div>
            `}).join("");
        }

        modal.classList.remove("hidden");
        document.body.style.overflow = "hidden";
    }

    function closeModal() {
        modal.classList.add("hidden");
        document.body.style.overflow = "";
    }

    modalClose.addEventListener("click", closeModal);
    modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !modal.classList.contains("hidden")) closeModal();
    });

    container.addEventListener("click", (e) => {
        const btn = e.target.closest(".btn-review");
        if (btn) openModal(btn.dataset.type);
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("results-content");
    const progress = Storage.getProgress();
    const wrong = Storage.getWrongAnswers();
    const types = window.EXERCISE_TYPES || {};

    if (Object.keys(progress).length === 0) {
        container.innerHTML = '<div class="result-card"><p>Nessun progresso ancora. Inizia a fare esercizi!</p></div>';
        return;
    }

    let html = "";
    for (const [type, p] of Object.entries(progress)) {
        const meta = types[type] || { icon: "", name: type };
        const accRaw = p.completed > 0 ? p.correct / p.completed : 0;
        const acc = Math.round(accRaw * 100);
        const mastered = p.completed >= 30 && accRaw >= 0.75;
        const barClass = mastered ? "mastered" : "not-mastered";
        const wrongCount = (wrong[type] || []).length;
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

    function openModal(type) {
        const items = (wrong[type] || []).slice().reverse(); /* most recent first */
        const meta = types[type] || { icon: "", name: type };
        modalTitle.textContent = `${meta.icon} Errori — ${meta.name}`;

        if (items.length === 0) {
            modalBody.innerHTML = "<p>Nessun errore registrato per questa categoria.</p>";
        } else {
            modalBody.innerHTML = items.map((item, i) => `
                <div class="wrong-item">
                    <div class="wrong-number">#${items.length - i}</div>
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
            `).join("");
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

/* === SRS Data Model & Performance Tracker === */
/* Pure data-layer module — no UI, no dependencies. */
/* Stored in localStorage key "tolc_srs". */

(function () {
    "use strict";

    var STORAGE_KEY = "tolc_srs";
    var MAX_HISTORY = 100;
    var ROLLING_WINDOW_SIZE = 10;
    var EMA_ALPHA = 0.3;

    /* --- Internal state --- */
    var _data = null;

    /* --- Helpers --- */
    function makeKey(type, difficulty) {
        return type + "_" + difficulty;
    }

    function clamp(val, lo, hi) {
        return Math.max(lo, Math.min(hi, val));
    }

    function loadFromStorage() {
        try {
            var raw = localStorage.getItem(STORAGE_KEY);
            if (raw) {
                return JSON.parse(raw);
            }
        } catch (e) {
            /* corrupt data — start fresh */
        }
        return null;
    }

    function createEmpty() {
        return {
            version: 1,
            migrated: false,
            stats: {},
            history: []
        };
    }

    function pushHistory(entry) {
        _data.history.push(entry);
        if (_data.history.length > MAX_HISTORY) {
            _data.history = _data.history.slice(_data.history.length - MAX_HISTORY);
        }
    }

    /* --- Public API --- */

    function init() {
        _data = loadFromStorage();
        if (!_data) {
            _data = createEmpty();
        }
        /* Ensure structural integrity after load */
        if (!_data.stats) _data.stats = {};
        if (!_data.history) _data.history = [];
        if (_data.version === undefined) _data.version = 1;

        if (!_data.migrated) {
            migrate();
        }
        save();
    }

    function getStats(type, difficulty) {
        var key = makeKey(type, difficulty);
        return _data.stats[key] || null;
    }

    function recordAnswer(type, difficulty, correct, timeMs) {
        var key = makeKey(type, difficulty);
        var s = _data.stats[key];
        var now = Date.now();
        var correctVal = correct ? 1 : 0;

        if (!s) {
            s = {
                lastReview: now,
                totalReviews: 0,
                correctCount: 0,
                rollingAccuracy: 0,
                rollingWindow: [],
                stability: 0.5,
                difficulty: 0.5,
                avgTimeMs: timeMs || 0
            };
            _data.stats[key] = s;
        }

        /* Update counters */
        s.totalReviews++;
        if (correct) {
            s.correctCount++;
        }
        s.lastReview = now;

        /* Rolling window */
        s.rollingWindow.push(correctVal);
        if (s.rollingWindow.length > ROLLING_WINDOW_SIZE) {
            s.rollingWindow = s.rollingWindow.slice(s.rollingWindow.length - ROLLING_WINDOW_SIZE);
        }

        /* Rolling accuracy */
        var sum = 0;
        for (var i = 0; i < s.rollingWindow.length; i++) {
            sum += s.rollingWindow[i];
        }
        s.rollingAccuracy = s.rollingWindow.length > 0 ? sum / s.rollingWindow.length : 0;

        /* Stability update */
        if (correct) {
            s.stability = Math.min(365, s.stability * (1.5 + (1 - s.difficulty) * 0.5));
        } else {
            s.stability = Math.max(0.5, s.stability * 0.5);
        }

        /* Difficulty factor update */
        s.difficulty = clamp(s.difficulty + 0.1 * (correct ? -1 : 1), 0.1, 0.9);

        /* Average time — exponential moving average */
        if (timeMs && timeMs > 0) {
            if (s.avgTimeMs === 0) {
                s.avgTimeMs = timeMs;
            } else {
                s.avgTimeMs = Math.round(EMA_ALPHA * timeMs + (1 - EMA_ALPHA) * s.avgTimeMs);
            }
        }

        /* History entry */
        pushHistory({
            ts: now,
            type: type,
            difficulty: difficulty,
            correct: !!correct,
            timeMs: timeMs || 0
        });

        save();
        return s;
    }

    function getHistory() {
        return _data.history.slice();
    }

    function getAllStats() {
        var result = {};
        var keys = Object.keys(_data.stats);
        for (var i = 0; i < keys.length; i++) {
            result[keys[i]] = _data.stats[keys[i]];
        }
        return result;
    }

    function migrate() {
        var progressRaw, wrongRaw, progress, wrong;

        try {
            progressRaw = localStorage.getItem("tolc_progress");
            progress = progressRaw ? JSON.parse(progressRaw) : {};
        } catch (e) {
            progress = {};
        }

        try {
            wrongRaw = localStorage.getItem("tolc_wrong");
            wrong = wrongRaw ? JSON.parse(wrongRaw) : {};
        } catch (e) {
            wrong = {};
        }

        var types = Object.keys(progress);
        for (var i = 0; i < types.length; i++) {
            var type = types[i];
            var p = progress[type];
            if (!p || !p.completed || p.completed <= 0) continue;

            var key = makeKey(type, 2); /* default difficulty 2 */
            var accuracy = p.correct / p.completed;
            var streak = p.streak || 0;

            _data.stats[key] = {
                lastReview: Date.now(),
                totalReviews: p.completed,
                correctCount: p.correct || 0,
                rollingAccuracy: accuracy,
                rollingWindow: [], /* cannot reconstruct from old data */
                stability: clamp(streak * 1.5, 0.5, 30),
                difficulty: clamp(1 - accuracy, 0.1, 0.9),
                avgTimeMs: 0
            };
        }

        /* Collect wrong-answer entries with timestamps for history */
        var historyEntries = [];
        var wrongTypes = Object.keys(wrong);
        for (var j = 0; j < wrongTypes.length; j++) {
            var wType = wrongTypes[j];
            var entries = wrong[wType];
            if (!Array.isArray(entries)) continue;
            for (var k = 0; k < entries.length; k++) {
                var entry = entries[k];
                if (entry && entry.timestamp) {
                    historyEntries.push({
                        ts: entry.timestamp,
                        type: wType,
                        difficulty: entry.difficulty || 2,
                        correct: false,
                        timeMs: 0
                    });
                }
            }
        }

        /* Sort by timestamp, keep most recent MAX_HISTORY */
        historyEntries.sort(function (a, b) { return a.ts - b.ts; });
        if (historyEntries.length > MAX_HISTORY) {
            historyEntries = historyEntries.slice(historyEntries.length - MAX_HISTORY);
        }

        /* Merge into existing history */
        for (var m = 0; m < historyEntries.length; m++) {
            pushHistory(historyEntries[m]);
        }

        _data.migrated = true;
        /* DO NOT delete old keys — keep backward compatibility */
    }

    function save() {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(_data));
        } catch (e) {
            /* localStorage full or unavailable — silently fail */
        }
    }

    /* --- Expose as window.SRSTracker --- */
    window.SRSTracker = {
        init: init,
        getStats: getStats,
        recordAnswer: recordAnswer,
        getHistory: getHistory,
        getAllStats: getAllStats,
        migrate: migrate,
        save: save
    };
})();

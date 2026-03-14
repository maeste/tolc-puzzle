/* === SRS Wrong-Answer Reconsolidation Module === */
/* Tracks items answered incorrectly and requires consecutive correct answers */
/* before marking them as reconsolidated. */
/* Depends on window.SRSTracker and window.SRSScheduler being present (optional). */

(function () {
    "use strict";

    var STORAGE_KEY = "tolc_srs_recon";

    /* --- Internal state --- */
    var _data = null;

    /* --- Helpers --- */
    function makeKey(type, difficulty) {
        return type + "_" + difficulty;
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
            items: {},
            errorStats: {}
        };
    }

    function extractType(key) {
        /* Key format: type_difficulty — type itself may contain underscores */
        var parts = key.split("_");
        if (parts.length < 2) return key;
        return parts.slice(0, parts.length - 1).join("_");
    }

    /* --- Public API --- */

    var SRSReconsolidation = {
        boostFactor: 2.0,
        requiredCorrect: 3,

        init: function () {
            _data = loadFromStorage();
            if (!_data) {
                _data = createEmpty();
            }
            if (!_data.items) _data.items = {};
            if (!_data.errorStats) _data.errorStats = {};
            this.save();
        },

        onWrongAnswer: function (type, difficulty) {
            if (!_data) this.init();

            var key = makeKey(type, difficulty);
            var item = _data.items[key];

            if (!item) {
                item = {
                    active: true,
                    triggeredAt: Date.now(),
                    consecutiveCorrect: 0,
                    totalAttempts: 0,
                    completedCount: 0
                };
                _data.items[key] = item;
            }

            item.active = true;
            item.consecutiveCorrect = 0;
            item.triggeredAt = Date.now();
            item.totalAttempts = (item.totalAttempts || 0) + 1;

            /* Update error stats by type */
            if (!_data.errorStats[type]) {
                _data.errorStats[type] = 0;
            }
            _data.errorStats[type]++;

            this.save();
        },

        onCorrectAnswer: function (type, difficulty) {
            if (!_data) this.init();

            var key = makeKey(type, difficulty);
            var item = _data.items[key];

            if (!item || !item.active) {
                return { reconsolidating: false, consecutiveCorrect: 0, completed: false };
            }

            item.consecutiveCorrect = (item.consecutiveCorrect || 0) + 1;
            item.totalAttempts = (item.totalAttempts || 0) + 1;

            if (item.consecutiveCorrect >= this.requiredCorrect) {
                item.active = false;
                item.completedCount = (item.completedCount || 0) + 1;
                this.save();
                return { reconsolidating: false, consecutiveCorrect: this.requiredCorrect, completed: true };
            }

            this.save();
            return { reconsolidating: true, consecutiveCorrect: item.consecutiveCorrect, completed: false };
        },

        getActiveItems: function () {
            if (!_data) this.init();

            var result = [];
            var keys = Object.keys(_data.items);
            for (var i = 0; i < keys.length; i++) {
                var key = keys[i];
                var item = _data.items[key];
                if (item && item.active) {
                    var parts = key.split("_");
                    var diff = parseInt(parts[parts.length - 1], 10);
                    var typ = parts.slice(0, parts.length - 1).join("_");

                    result.push({
                        type: typ,
                        difficulty: diff,
                        consecutiveCorrect: item.consecutiveCorrect || 0,
                        triggeredAt: item.triggeredAt,
                        totalAttempts: item.totalAttempts || 0
                    });
                }
            }
            return result;
        },

        isReconsolidating: function (type, difficulty) {
            if (!_data) this.init();

            var key = makeKey(type, difficulty);
            var item = _data.items[key];
            return !!(item && item.active);
        },

        getErrorStats: function () {
            if (!_data) this.init();

            var topErrors = [];
            var totalErrors = 0;
            var keys = Object.keys(_data.errorStats);

            for (var i = 0; i < keys.length; i++) {
                var count = _data.errorStats[keys[i]];
                totalErrors += count;
                topErrors.push({ type: keys[i], count: count });
            }

            topErrors.sort(function (a, b) {
                return b.count - a.count;
            });

            return { topErrors: topErrors, totalErrors: totalErrors };
        },

        getBoost: function (type, difficulty) {
            if (!_data) this.init();

            if (this.isReconsolidating(type, difficulty)) {
                return this.boostFactor;
            }
            return 1.0;
        },

        save: function () {
            if (!_data) return;
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(_data));
            } catch (e) {
                /* localStorage full or unavailable — silently fail */
            }
        }
    };

    /* --- Expose as window.SRSReconsolidation --- */
    window.SRSReconsolidation = SRSReconsolidation;
})();

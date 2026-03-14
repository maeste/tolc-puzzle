/* === SRS Scheduling Engine === */
/* Pure scheduling-logic module — no UI. */
/* Depends on window.SRSTracker being loaded first. */

(function () {
    "use strict";

    /* --- Constants --- */
    var DEFAULT_RETENTION_TARGET = 0.85;

    var FALLBACK_EXERCISE_TYPES = [
        "solve", "geometry", "graph", "word", "trap", "logic",
        "probability", "statistics", "always_true", "proportional",
        "cross_topic", "simplification", "inequalities", "analytic_geo",
        "number_sense", "which_satisfies", "estimation", "composition",
        "strategy"
    ];

    var DIFFICULTY_LEVELS = [1, 2, 3];

    /* --- Helpers --- */

    function getExerciseTypes() {
        if (window.EXERCISE_TYPES && Array.isArray(window.EXERCISE_TYPES) && window.EXERCISE_TYPES.length > 0) {
            return window.EXERCISE_TYPES;
        }
        return FALLBACK_EXERCISE_TYPES;
    }

    function daysSince(timestampMs) {
        if (!timestampMs || timestampMs <= 0) {
            return Infinity;
        }
        var elapsed = Date.now() - timestampMs;
        return Math.max(0, elapsed / (1000 * 60 * 60 * 24));
    }

    /**
     * FSRS-inspired retrievability formula: R(t) = e^(-t/S)
     * @param {number} elapsedDays - time since last review in days
     * @param {number} stability - stability in days
     * @returns {number} probability of recall 0-1
     */
    function computeRetention(elapsedDays, stability) {
        if (stability <= 0) {
            return 0;
        }
        if (elapsedDays <= 0) {
            return 1;
        }
        if (!isFinite(elapsedDays)) {
            return 0;
        }
        return Math.exp(-elapsedDays / stability);
    }

    /**
     * Solve for time until retention drops to target:
     * target = e^(-t/S)  =>  t = -S * ln(target)
     * Returns days.
     */
    function timeUntilThreshold(stability, target) {
        if (stability <= 0 || target <= 0 || target >= 1) {
            return 0;
        }
        return -stability * Math.log(target);
    }

    /* --- Public API --- */

    var SRSScheduler = {
        retentionTarget: DEFAULT_RETENTION_TARGET,

        /**
         * Get retrievability for a specific type x difficulty.
         * Returns 0-1 (1 = just reviewed, 0 = forgotten).
         * Returns 0 for never-attempted items.
         */
        getRetention: function (type, difficulty) {
            if (!window.SRSTracker) {
                return 0;
            }
            var stats = window.SRSTracker.getStats(type, difficulty);
            if (!stats) {
                return 0;
            }
            var elapsed = daysSince(stats.lastReview);
            return computeRetention(elapsed, stats.stability);
        },

        /**
         * Get all type x difficulty pairs sorted by urgency (lowest R first).
         * Includes all known pairs from stats plus "new" items never attempted.
         */
        getDueItems: function () {
            var items = [];
            var seen = {};
            var stats = {};
            var target = this.retentionTarget;

            if (window.SRSTracker) {
                stats = window.SRSTracker.getAllStats();
            }

            /* Process existing stats entries */
            var keys = Object.keys(stats);
            for (var i = 0; i < keys.length; i++) {
                var key = keys[i];
                var s = stats[key];
                var parts = key.split("_");
                /* Key format: type_difficulty, but type itself may contain underscores */
                if (parts.length < 2) continue;
                var diff = parseInt(parts[parts.length - 1], 10);
                var typ = parts.slice(0, parts.length - 1).join("_");

                if (isNaN(diff) || diff < 1 || diff > 3) continue;

                var elapsed = daysSince(s.lastReview);
                var retention = computeRetention(elapsed, s.stability);

                var itemEntry = {
                    type: typ,
                    difficulty: diff,
                    retention: retention,
                    stability: s.stability,
                    lastReview: s.lastReview,
                    overdue: retention < target
                };

                /* Apply reconsolidation boost: lower effective retention for items being reconsolidated */
                if (window.SRSReconsolidation) {
                    var boost = SRSReconsolidation.getBoost(typ, diff);
                    if (boost > 1) {
                        itemEntry.retention = itemEntry.retention / boost;
                        itemEntry.reconsolidating = true;
                        itemEntry.overdue = itemEntry.retention < target;
                    }
                }

                items.push(itemEntry);
                seen[key] = true;
            }

            /* Enumerate all exercise types x difficulties for "new" items */
            var types = getExerciseTypes();
            for (var t = 0; t < types.length; t++) {
                for (var d = 0; d < DIFFICULTY_LEVELS.length; d++) {
                    var newKey = types[t] + "_" + DIFFICULTY_LEVELS[d];
                    if (!seen[newKey]) {
                        items.push({
                            type: types[t],
                            difficulty: DIFFICULTY_LEVELS[d],
                            retention: 0,
                            stability: 0,
                            lastReview: null,
                            overdue: true
                        });
                    }
                }
            }

            /* Sort by retention ascending (most urgent first) */
            items.sort(function (a, b) {
                return a.retention - b.retention;
            });

            return items;
        },

        /**
         * Get recommended session of N exercises with interleaving.
         * Rules:
         * 1. Overdue items first (R < retentionTarget)
         * 2. New items mixed in
         * 3. Items approaching threshold (R < retentionTarget + 0.1)
         * 4. Never 2 consecutive same TYPE (unless unavoidable)
         * 5. Mix difficulties within a type
         */
        getRecommendedSession: function (n) {
            if (!n || n <= 0) return [];

            var allItems = this.getDueItems();
            var target = this.retentionTarget;

            /* Categorize items */
            var overdue = [];
            var newItems = [];
            var approaching = [];
            var remaining = [];

            for (var i = 0; i < allItems.length; i++) {
                var item = allItems[i];
                if (item.lastReview === null) {
                    newItems.push({ type: item.type, difficulty: item.difficulty, reason: "new" });
                } else if (item.retention < target) {
                    overdue.push({ type: item.type, difficulty: item.difficulty, reason: "overdue" });
                } else if (item.retention < target + 0.1) {
                    approaching.push({ type: item.type, difficulty: item.difficulty, reason: "review" });
                } else {
                    remaining.push({ type: item.type, difficulty: item.difficulty, reason: "practice" });
                }
            }

            /* Build candidate pool in priority order */
            var pool = overdue.concat(newItems, approaching, remaining);

            /* Apply interleaving: no 2 consecutive same type */
            var session = [];
            var used = [];
            for (var u = 0; u < pool.length; u++) {
                used.push(false);
            }

            while (session.length < n && session.length < pool.length) {
                var lastType = session.length > 0 ? session[session.length - 1].type : null;
                var picked = -1;

                /* First pass: find next unused item with different type */
                for (var p = 0; p < pool.length; p++) {
                    if (!used[p] && pool[p].type !== lastType) {
                        picked = p;
                        break;
                    }
                }

                /* Deadlock: only same type left, allow it */
                if (picked === -1) {
                    for (var q = 0; q < pool.length; q++) {
                        if (!used[q]) {
                            picked = q;
                            break;
                        }
                    }
                }

                if (picked === -1) break;

                used[picked] = true;
                session.push({
                    type: pool[picked].type,
                    difficulty: pool[picked].difficulty,
                    reason: pool[picked].reason
                });
            }

            return session;
        },

        /**
         * Get summary stats for dashboard display.
         */
        getSummary: function () {
            var allItems = this.getDueItems();
            var target = this.retentionTarget;

            var totalItems = allItems.length;
            var overdueCount = 0;
            var newCount = 0;
            var retentionSum = 0;
            var statsCount = 0;
            var nextDueIn = Infinity;

            for (var i = 0; i < allItems.length; i++) {
                var item = allItems[i];

                if (item.lastReview === null) {
                    newCount++;
                } else {
                    statsCount++;
                    retentionSum += item.retention;

                    if (item.retention < target) {
                        overdueCount++;
                    } else {
                        /* Compute time until this item becomes overdue */
                        var totalDaysToThreshold = timeUntilThreshold(item.stability, target);
                        var elapsedDays = daysSince(item.lastReview);
                        var daysRemaining = totalDaysToThreshold - elapsedDays;
                        var minutesRemaining = daysRemaining * 24 * 60;
                        if (minutesRemaining < nextDueIn) {
                            nextDueIn = minutesRemaining;
                        }
                    }
                }
            }

            var avgRetention = statsCount > 0 ? retentionSum / statsCount : 0;

            /* If nothing is approaching due, set nextDueIn to null */
            if (!isFinite(nextDueIn)) {
                nextDueIn = null;
            } else {
                nextDueIn = Math.max(0, Math.round(nextDueIn));
            }

            return {
                totalItems: totalItems,
                overdueCount: overdueCount,
                newCount: newCount,
                avgRetention: avgRetention,
                nextDueIn: nextDueIn
            };
        }
    };

    /* --- Expose as window.SRSScheduler --- */
    window.SRSScheduler = SRSScheduler;
})();

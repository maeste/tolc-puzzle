/* === SRS Adaptive Difficulty System === */
/* Pure logic module — no UI, no DOM manipulation. */
/* Depends on: window.SRSTracker (must be initialized). */

(function () {
    "use strict";

    var ACCURACY_THRESHOLD_L1_TO_L2 = 0.80;
    var ACCURACY_THRESHOLD_L2_TO_L3 = 0.70;
    var ACCURACY_FALLBACK_THRESHOLD = 0.50;
    var MIN_REVIEWS_FOR_PROMOTION = 5;
    var MASTERY_STABILITY_THRESHOLD = 5; // days

    /**
     * Get the recommended difficulty level for a given exercise type.
     * Returns 1, 2, or 3.
     */
    function getRecommendedDifficulty(type) {
        if (!window.SRSTracker) return 1;

        var stats1 = window.SRSTracker.getStats(type, 1);
        var stats2 = window.SRSTracker.getStats(type, 2);
        var stats3 = window.SRSTracker.getStats(type, 3);

        // Rule 1: No data at all → start at L1
        if (!stats1 && !stats2 && !stats3) return 1;

        // Rule 5: L3 accuracy < 0.50 → suggest L2
        if (stats3 && stats3.totalReviews >= MIN_REVIEWS_FOR_PROMOTION &&
            stats3.rollingAccuracy < ACCURACY_FALLBACK_THRESHOLD) {
            return 2;
        }

        // Rule 3: L2 accuracy > 0.70 AND totalReviews >= 5 → suggest L3
        if (stats2 && stats2.totalReviews >= MIN_REVIEWS_FOR_PROMOTION &&
            stats2.rollingAccuracy > ACCURACY_THRESHOLD_L2_TO_L3) {
            return 3;
        }

        // Rule 4: L2 accuracy < 0.50 → suggest L1
        if (stats2 && stats2.totalReviews >= MIN_REVIEWS_FOR_PROMOTION &&
            stats2.rollingAccuracy < ACCURACY_FALLBACK_THRESHOLD) {
            return 1;
        }

        // Rule 2: L1 accuracy > 0.80 AND totalReviews >= 5 → suggest L2
        if (stats1 && stats1.totalReviews >= MIN_REVIEWS_FOR_PROMOTION &&
            stats1.rollingAccuracy > ACCURACY_THRESHOLD_L1_TO_L2) {
            return 2;
        }

        // Default: if we have some stats but none of the rules trigger,
        // stay at the highest level that has data with decent accuracy
        if (stats2 && stats2.totalReviews > 0) return 2;
        return 1;
    }

    /**
     * Get the mastery level for a given exercise type.
     * Returns "beginner", "intermediate", "advanced", or "mastered".
     */
    function getMasteryLevel(type) {
        if (!window.SRSTracker) return "beginner";

        var stats1 = window.SRSTracker.getStats(type, 1);
        var stats2 = window.SRSTracker.getStats(type, 2);
        var stats3 = window.SRSTracker.getStats(type, 3);

        // No stats at all → beginner
        if (!stats1 && !stats2 && !stats3) return "beginner";

        // mastered: L3 accuracy >= 0.7 AND stability > 5 days
        if (stats3 && stats3.rollingAccuracy >= 0.7 &&
            stats3.stability > MASTERY_STABILITY_THRESHOLD) {
            return "mastered";
        }

        // advanced: L2 accuracy >= 0.7
        if (stats2 && stats2.rollingAccuracy >= 0.7) {
            return "advanced";
        }

        // intermediate: L1 accuracy >= 0.6
        if (stats1 && stats1.rollingAccuracy >= 0.6) {
            return "intermediate";
        }

        // beginner: default (no stats or L1 accuracy < 0.6)
        return "beginner";
    }

    /**
     * Get mastery levels for all exercise types.
     * Returns an object {type: masteryLevel}.
     */
    function getAllMasteryLevels() {
        var result = {};
        var types = [];

        // Try to get types from window.EXERCISE_TYPES (object with keys)
        if (window.EXERCISE_TYPES && typeof window.EXERCISE_TYPES === "object") {
            types = Object.keys(window.EXERCISE_TYPES);
        }

        for (var i = 0; i < types.length; i++) {
            result[types[i]] = getMasteryLevel(types[i]);
        }
        return result;
    }

    /* --- Expose as window.SRSAdaptive --- */
    window.SRSAdaptive = {
        getRecommendedDifficulty: getRecommendedDifficulty,
        getMasteryLevel: getMasteryLevel,
        getAllMasteryLevels: getAllMasteryLevels,
        // Expose constants for testing
        ACCURACY_THRESHOLD_L1_TO_L2: ACCURACY_THRESHOLD_L1_TO_L2,
        ACCURACY_THRESHOLD_L2_TO_L3: ACCURACY_THRESHOLD_L2_TO_L3,
        ACCURACY_FALLBACK_THRESHOLD: ACCURACY_FALLBACK_THRESHOLD,
        MIN_REVIEWS_FOR_PROMOTION: MIN_REVIEWS_FOR_PROMOTION,
        MASTERY_STABILITY_THRESHOLD: MASTERY_STABILITY_THRESHOLD
    };
})();

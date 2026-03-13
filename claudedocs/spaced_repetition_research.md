# Spaced Repetition & Memory Reconsolidation: Research Summary

**Research Date**: 2026-03-13
**Confidence Level**: High (well-established scientific domain with active ongoing research)

---

## 1. Memory Reconsolidation Theory

### What Is It?

Memory reconsolidation is the process by which previously consolidated (stable) long-term memories become temporarily **labile** (unstable) when reactivated through retrieval, and must then be **restabilized**. During this restabilization window, the memory trace can be strengthened, updated, or modified.

### Scientific Basis

**Ebbinghaus Forgetting Curve (1885)**
Hermann Ebbinghaus discovered that memory retention decays exponentially over time without reinforcement. His experiments showed that ~56% of learned material is forgotten within one hour, ~66% within one day, and ~75% within six days. This curve established the empirical foundation for why *when* you review matters as much as *what* you review.

**The Spacing Effect**
Also documented by Ebbinghaus, the spacing effect shows that information is retained more effectively when study sessions are distributed over time rather than massed together ("cramming"). Cepeda et al.'s (2006) meta-analysis of 254 studies confirmed spacing produces **10-30% better retention** compared to massed practice.

**Active Recall (Testing Effect)**
Roediger and Karpicke (2006) demonstrated that retrieval practice (actively recalling information) improves long-term recall by approximately **50%** compared to passive restudying. Each retrieval attempt strengthens the memory trace and creates additional retrieval pathways.

### How Anki Leverages Reconsolidation

Anki exploits the reconsolidation window by:

1. **Triggering retrieval** at calculated intervals -- each review forces active recall, destabilizing the memory trace
2. **Restabilizing with feedback** -- the card answer provides immediate reinforcement during the labile window
3. **Optimally spacing** the next retrieval -- scheduling the next review just before the predicted forgetting threshold, ensuring each reconsolidation cycle maximally strengthens the trace
4. **Adapting to individual performance** -- adjusting intervals based on recall difficulty, personalizing the reconsolidation schedule

The key insight from reconsolidation theory: the **second and subsequent presentations** are where the spacing effect operates. The memory must first be consolidated, then reactivated (retrieved), then reconsolidated at a stronger level.

---

## 2. Anki's Algorithms

### SM-2 Algorithm (Legacy)

Developed by Piotr Wozniak in the late 1980s, SM-2 (SuperMemo 2) was Anki's default algorithm until 2023.

**Core Mechanics:**

- **Ease Factor (EF)**: Each card starts at 250% (2.5x multiplier). Adjusted after each review:
  - `new_EF = old_EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))`
  - Quality 5 (perfect) increases EF; Quality < 4 decreases it
  - Minimum EF is 130% (below this, reviews become counterproductively frequent)

- **Interval Calculation**:
  - First review: 1 day
  - Second review: 6 days
  - Subsequent reviews: `previous_interval * ease_factor`
  - Small random noise added to prevent cards clustering on the same day

- **Response-Based Adjustment**:
  - **Again (Forgot)**: Interval multiplied by lapse factor (default 0.1x), ease decreased by 20 percentage points
  - **Hard**: Interval factor 1.2x, ease decreased by 15 percentage points
  - **Good**: Interval factor = current ease
  - **Easy**: Interval factor = ease * easy bonus, ease increased by 15 percentage points

**SM-2 Limitations:**
- No mathematical model of memory -- intervals are heuristic
- "Ease hell" -- cards with repeatedly low ratings spiral into very short intervals
- One-size-fits-all initial intervals
- No personalization based on user's overall memory patterns

### FSRS Algorithm (Current, since Anki 23.10)

FSRS (Free Spaced Repetition Scheduler), developed by Jarrett Ye, is now Anki's recommended algorithm.

**Three Component Model of Memory:**

| Component | Symbol | Description |
|-----------|--------|-------------|
| **Retrievability** | R | Probability of successful recall at a given moment; decays over time |
| **Stability** | S | Time (in days) for R to decay from 100% to 90% |
| **Difficulty** | D | Inherent complexity of the material; affects how easily stability grows |

**Key Improvements Over SM-2:**
- Uses **machine learning** to analyze the user's review history and find optimal parameters
- Users set a **desired retention rate** (e.g., 90%) and FSRS calculates intervals accordingly
- Produces **20-30% fewer reviews** for the same retention level compared to SM-2
- Mathematically grounded in memory models rather than heuristics
- Personalizes to individual memory patterns

---

## 3. Key Principles of Effective Spaced Repetition

### Active Recall vs. Passive Review

| Aspect | Active Recall | Passive Review |
|--------|--------------|----------------|
| **Mechanism** | Self-generated retrieval from memory | Re-reading/re-exposure to material |
| **Effort** | High (desirable difficulty) | Low (fluency illusion) |
| **Retention** | ~50% better long-term retention | Creates false sense of mastery |
| **Neural basis** | Recruits additional mental resources, creates multiple retrieval routes | Shallow processing, weak encoding |

Active recall is the **foundational principle** of Anki -- every card interaction requires the user to generate an answer before seeing the solution.

### Spacing Effect

Distributing practice over time produces substantially better long-term retention than massed practice:
- **Expanding intervals** (1 day, 3 days, 7 days, 21 days...) match the forgetting curve
- **Optimal gap** depends on the desired retention interval (longer target retention = longer optimal gaps)
- Spacing works because it forces **effortful retrieval** from long-term memory, strengthening the trace

### Interleaving

Mixing different types of problems/topics during practice, rather than blocking by type:
- Forces the learner to **discriminate** between problem types (not just execute a known procedure)
- Produces **slower initial learning** but significantly better transfer and long-term retention
- Particularly important for mathematics, where students must learn **when** to apply each technique, not just **how**

### Desirable Difficulty (Bjork & Bjork)

Robert Bjork identified four "desirable difficulties" that slow initial learning but enhance long-term retention:

1. **Spacing** -- distributing practice over time
2. **Interleaving** -- mixing problem types
3. **Retrieval practice** -- testing rather than restudying
4. **Generation** -- producing answers rather than recognizing them

Critical caveat: Not all difficulty is desirable. If the learner **cannot eventually succeed**, the difficulty becomes unproductive. The difficulty must be within the learner's zone of proximal development.

### Leitner System Comparison

| Feature | Leitner System | SM-2 / FSRS |
|---------|---------------|--------------|
| **Scheduling** | Fixed box intervals (Box 1: daily, Box 2: every 2 days, etc.) | Continuous, per-card adaptive intervals |
| **Granularity** | Coarse (3-5 boxes) | Fine (arbitrary day intervals per card) |
| **Difficulty adaptation** | Binary (pass/fail moves between boxes) | Multi-level (ease factor / difficulty parameter) |
| **Personalization** | None (same boxes for everyone) | SM-2: per-card ease; FSRS: per-user ML model |
| **Strengths** | Simple, physical, no technology needed | Highly optimized, scales to thousands of cards |
| **Weaknesses** | Cannot differentiate easy vs hard items within same box | Requires software; parameters can be opaque |

The Leitner system and SM-2 share the same core insight (increase intervals for known material, reset for forgotten material), but SM-2/FSRS provide **continuous, individualized scheduling** rather than discrete boxes.

---

## 4. Recent Research & Critiques (2024-2025)

### Evidence Supporting Spaced Repetition in STEM

- **Murray et al. (2024)**: Spacing increases retention of mathematics procedures among university students
- **Springer (2025)**: Retrieval practice narrows achievement gaps in higher mathematics
- **Educational Psychology Review (2022)**: Spaced retrieval practice imposes desirable difficulty in calculus learning, improving long-term retention

### Important Critiques and Nuances

**Inconsistent Effects in Complex Mathematics:**
- The spacing effect does **not emerge as reliably** for complex mathematical tasks as it does for vocabulary or simple facts
- Meta-analyses suggest the spacing effect is stronger for **simpler tasks** than for more complex ones
- In some studies, spacing effects in math appeared after 4 weeks but **not after 1 week**, suggesting different time dynamics

**Flashcard Model Limitations:**
- Current mathematical models for optimal review spacing are limited to **independent flashcard-like tasks**
- Mathematics has **hierarchical dependencies** -- understanding integral calculus depends on understanding limits, which depends on understanding functions
- Standard SRS algorithms do not account for these dependency chains

**The "Glass Half Empty" Perspective:**
- A 2024 meta-analysis across nine STEM courses found mixed results for spaced retrieval practice
- Effect sizes were often **small to moderate** rather than the large effects seen in vocabulary learning
- Transfer to novel problems (not just retention of practiced procedures) remains an open question

### Key Takeaway from Critiques

Spaced repetition is **not a silver bullet** for mathematics. Its effectiveness depends on:
- Task complexity (stronger effects for simpler, more procedural tasks)
- How cards are designed (atomized facts vs. problem-solving processes)
- Whether interleaving is incorporated alongside spacing
- The time intervals and retention targets chosen

---

## 5. Procedural vs. Declarative Knowledge: Adaptations Needed

### The Two Knowledge Types

| Dimension | Declarative Knowledge | Procedural Knowledge |
|-----------|----------------------|---------------------|
| **Nature** | "Knowing that" -- facts, concepts, definitions | "Knowing how" -- skills, procedures, algorithms |
| **Example** | "The quadratic formula is..." | "Apply the quadratic formula to solve..." |
| **Memory system** | Explicit/semantic memory | Implicit/procedural memory |
| **Learning mechanism** | Encoding and retrieval of associations | Repeated practice leading to automaticity |
| **SRS fit** | Excellent (classic flashcard model) | Requires adaptation |

### Why Standard SRS Struggles with Procedural Knowledge

1. **Atomization problem**: Mathematical procedures involve **multi-step chains** that are hard to break into independent flashcards without losing the procedural flow
2. **Transfer gap**: Recalling a formula (declarative) does not guarantee ability to apply it in novel contexts (procedural)
3. **Hierarchical dependencies**: Advanced math skills **implicitly practice** simpler skills -- standard SRS treats each card as independent
4. **Variability requirement**: Procedural fluency requires practice across **varied problem contexts**, not just repeated identical retrieval

### Adaptations for Mathematical/Procedural Knowledge

**Michael Nielsen's Approach (2019):**
- Use SRS not just for memorizing theorems but for **"pulling apart" proofs** -- atomizing the reasoning steps
- Create cards that ask "why" and "what if" questions, not just "what"
- Build **strong conceptual representations** through varied problem engagement
- The SRS process is secondary to the deep analytical work of decomposing mathematical structures

**Justin Skycak's Hierarchical Model:**
- Mathematics forms a **directed acyclic graph** of skill dependencies
- When a student practices an advanced skill, all prerequisite skills get **implicit spaced practice**
- Optimal scheduling must account for this "free" practice of foundational skills
- Individualized spacing based on the student's position in the skill graph

**Practical Recommendations for Math SRS:**

1. **Mix card types**: Combine declarative cards (formulas, definitions) with procedural cards (worked examples, problem-solving steps)
2. **Use problem variation**: Create multiple cards for the same concept with different numbers, contexts, or framings
3. **Include "discrimination" cards**: "Which technique applies here?" -- forcing selection of the right approach
4. **Incorporate worked examples**: Research (2025) shows worked examples can **boost the spacing effect** for procedural learning
5. **Build prerequisite chains**: Tag cards with dependencies and ensure foundational skills are solid before advancing
6. **Interleave by default**: Mix problem types within review sessions rather than grouping by topic
7. **Target understanding, not just recall**: Cards should test **application** ("Solve this...") not just recognition ("What is the formula for...")

---

## Summary for TOLC-B Application

For a math preparation tool like TOLC-B Puzzle, the research suggests:

1. **Spaced repetition is well-supported** for mathematical learning, but requires careful design beyond simple flashcards
2. **Problem variation is critical** -- students should encounter the same concept in different forms
3. **Interleaving problem types** during practice sessions is as important as spacing over time
4. **The FSRS model** (retrievability, stability, difficulty) provides a more principled framework than SM-2
5. **Hierarchical skill dependencies** should inform scheduling -- practicing advanced problems implicitly reviews fundamentals
6. **Desirable difficulty must be calibrated** -- problems should be challenging but solvable
7. **Active problem-solving** (not just formula recall) is the appropriate unit of practice for procedural math knowledge

---

## Sources

- [Background - Anki Manual](https://docs.ankiweb.net/background.html)
- [Spacing Repetitions Over Long Timescales: A Review and a Reconsolidation Explanation - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5476736/)
- [From Ebbinghaus to Anki: Why Spaced Repetition Works - Penn State](https://sites.psu.edu/psych256001fa2024/2024/09/15/blog-1-from-ebbinghaus-to-anki-why-spaced-repetition-works/)
- [SM-2 Algorithm Explained - Tegaru](https://tegaru.app/en/blog/sm2-algorithm-explained)
- [Anki SRS Algorithm - Julien Sobczak](https://juliensobczak.com/inspect/2022/05/30/anki-srs/)
- [FSRS vs SM-2: Complete Guide - MemoForge](https://memoforge.app/blog/fsrs-vs-sm2-anki-algorithm-guide-2025/)
- [ABC of FSRS - GitHub Wiki](https://github.com/open-spaced-repetition/fsrs4anki/wiki/abc-of-fsrs)
- [Desirable Difficulties - Structural Learning](https://www.structural-learning.com/post/desirable-difficulties)
- [Bjork & Bjork (2011) - Making Things Hard on Yourself](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/04/EBjork_RBjork_2011.pdf)
- [Spaced Retrieval Practice Imposes Desirable Difficulty in Calculus - Springer](https://link.springer.com/article/10.1007/s10648-022-09677-2)
- [Spacing Increases Retention of Mathematics Procedures - Murray et al. 2024](http://aidanhorner.org/papers/Murrayetal_PsyArXiv_2024.pdf)
- [Individualized Spaced Repetition in Hierarchical Knowledge Structures - Skycak](https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/)
- [Spaced Repetition Meta-analysis in STEM Courses - Springer 2024](https://stemeducationjournal.springeropen.com/articles/10.1186/s40594-024-00468-5)
- [Using Spaced Repetition Systems to See Through Mathematics - Michael Nielsen](https://cognitivemedium.com/srs-mathematics)
- [Spaced Repetition Algorithms Compared - QuizCat](https://www.quizcat.ai/blog/top-5-spaced-repetition-algorithms-compared)
- [Spaced Repetition - Gwern.net](https://gwern.net/spaced-repetition)
- [Top Spaced Repetition Algorithms - Brainscape](https://www.brainscape.com/academy/comparing-spaced-repetition-algorithms/)
- [What Spaced Repetition Algorithm Does Anki Use? - Anki FAQs](https://faqs.ankiweb.net/what-spaced-repetition-algorithm.html)
- [Do Worked Examples Boost the Spacing Effect? - ScienceDirect 2025](https://www.sciencedirect.com/science/article/abs/pii/S0959475225000271)
- [Retrieval Practice Narrows Achievement Gap in Higher Math - Springer 2025](https://link.springer.com/article/10.1007/s10763-025-10607-1)

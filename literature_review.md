# Literature Review: Beatty Sequences, C-finite Subsequences, and Related Topics

## Search Summary

The following web searches were conducted:

| # | Query | Key Findings |
|---|-------|-------------|
| (a) | Beatty sequence linear recurrence | Beatty sequences for rational r are C-finite; for irrational r, compositions can yield linear recurrences (Ballot 2017) |
| (b) | Sturmian word C-finite subsequence | Sturmian words are morphic iff slope is quadratic irrational (Allouche-Shallit); no direct C-finite subsequence characterization found |
| (c) | Fraenkel iterated floor function algebraic | Fraenkel (1994) proved identities for iterated floor functions on algebraic numbers; constructs Beatty subsequences |
| (d) | Wythoff array Fibonacci recurrence | Every row of the Wythoff array satisfies the Fibonacci recurrence; explicit formula involves golden ratio and Fibonacci numbers |
| (e) | Ostrowski numeration automatic sequence | Addition is automaton-recognizable for quadratic irrationals (Hieronymi-Terry 2018); Beatty sequences are synchronized automata (Schaeffer-Shallit-Zorcic 2024) |
| (f) | Skolem-Mahler-Lech theorem floor sequences | Zero set of C-finite sequences is eventually periodic; connects to structure of subsequences |
| (g) | Ballot Beatty compositions linear recurrence 2017 | Iterated compositions of complementary Beatty sequences yield C-finite sequences; seventh-order recurrence for cubic Pisot case |
| (h) | Schaeffer Shallit Zorcic decidability quadratic 2024 | First-order theory of quadratic Beatty sequences with addition is decidable; implemented in Walnut |

## Detailed Paper Reviews

### 1. Fraenkel (1994) — Iterated Floor Function
**Full title:** "Iterated Floor Function, Algebraic Numbers, Discrete Chaos, Beatty Subsequences, Semigroups"
**Journal:** Trans. Amer. Math. Soc. 341, 639–664.

**Key results:**
- For algebraic number α of degree ≤ n, the sum of iterated floor functionals A^i for 1 ≤ i ≤ n can be expressed in terms of A^1 = ⌊mα⌋, m, and a bounded error term.
- Explicit construction of nontrivial Beatty subsequences from algebraic numbers.
- Applications to discrete chaos and arithmetical semigroups.
**Relevance:** HIGH. Directly constructs C-finite subsequences from Beatty sequences of algebraic numbers. The degree of the algebraic number controls the recurrence order.

### 2. Ballot (2017) — Compositions of Beatty Sequences
**Full title:** "On Functions Expressible as Words on a Pair of Beatty Sequences"
**Journal:** J. Integer Sequences 20, Article 17.4.2.

**Key results:**
- For complementary Beatty pair (a, b) with a(n) = ⌊nα⌋ where α is an algebraic integer:
  - Compositions like b^y(n) satisfy linear recurrences
  - For α = golden ratio: second-order recurrence (Fibonacci)
  - For α = dominant root of x³ - x² - 1: seventh-order recurrence
- Characteristic polynomial of the recurrence relates to the minimal polynomial of α
- Open Problem 36: Characterize pairs (a,b) where iterated sequences satisfy linear recurrences
**Relevance:** CRITICAL. Provides the constructive direction for quadratic (and some cubic) irrationals. Open problems directly relevant to our characterization.

### 3. Schaeffer, Shallit, Zorcic (2024) — Decidability for Quadratic Beatty
**Full title:** "Beatty Sequences for a Quadratic Irrational: Decidability and Applications"
**arXiv:** 2402.08331.

**Key results:**
- Inhomogeneous Beatty sequence ⌊nα + β⌋ is synchronized in Ostrowski numeration when α is quadratic and β ∈ Q(α)
- First-order logical theory of these sequences with addition is decidable
- Implemented in Walnut theorem prover
- Solves open problems of Reble and Kimberling
**Relevance:** HIGH. The decidability result means that for quadratic irrationals, the existence of C-finite subsequences with any specified structure is algorithmically checkable.

### 4. Allouche and Shallit (2003) — Automatic Sequences
**Full title:** *Automatic Sequences: Theory, Applications, Generalizations*
**Publisher:** Cambridge University Press.

**Key results:**
- Sturmian word of slope α is morphic iff α is a quadratic irrational
- For irrational α, ⌊nα⌋ is never k-automatic for any k ≥ 2
- Comprehensive treatment of k-regular sequences, morphic sequences, and their closure properties
**Relevance:** CRITICAL. The morphic characterization is the key structural distinction between quadratic and non-quadratic irrationals.

### 5. Hieronymi and Terry (2018) — Ostrowski Numeration
**Full title:** "Ostrowski Numeration Systems, Addition, and Finite Automata"
**Journal:** Notre Dame J. Formal Logic 59(2).

**Key results:**
- Three-pass algorithm for addition in Ostrowski numeration systems
- When α is quadratic: addition is recognizable by finite automata
- Decidability of expansion of Presburger arithmetic by the Beatty function V_α
**Relevance:** HIGH. Foundational for the automata-theoretic approach to quadratic Beatty sequences.

### 6. Cassaigne (2001) — Recurrence in Infinite Words
**Full title:** "Recurrence in Infinite Words"
**Published in:** STACS 2001, LNCS 2010, Springer.

**Key results:**
- Sturmian word of slope α is linearly recurrent (in the symbolic dynamics sense) iff α has bounded partial quotients
- Recurrence quotient of Sturmian sequences relates to continued fraction structure
**Relevance:** MODERATE. "Linearly recurrent" in the symbolic dynamics sense ≠ "C-finite," but the connection to bounded CF quotients is important.

### 7. Russo and Schwiebert (2011) — Beatty Sequences and Fibonacci
**Full title:** "Beatty Sequences, Fibonacci Numbers, and the Golden Ratio"
**Journal:** Fibonacci Quarterly 49(2), 151–154.

**Key results:**
- Explicit connections between ⌊nφ⌋ and Fibonacci numbers
- Identities relating Beatty sequence values at Fibonacci indices to Fibonacci numbers
**Relevance:** MODERATE. Provides specific examples for the golden ratio case.

### 8. Kimberling (2011) — Generalized Wythoff
**Full title:** "Beatty Sequences and Wythoff Sequences, Generalized"
**Journal:** Fibonacci Quarterly 49(3), 195–200.

**Key results:**
- s-Wythoff sequences generalize classical Wythoff sequences
- Include pairs of complementary Beatty sequences (homogeneous and nonhomogeneous)
- Beatty discrepancy results for complementary equations
**Relevance:** MODERATE. Generalizes Wythoff-type constructions.

### 9. Tijdeman (2000) — Fraenkel's Conjecture
**Full title:** "Exact Covers of Balanced Sequences and Fraenkel's Conjecture"
**Published in:** Algebraic Number Theory and Diophantine Analysis (proceedings).

**Key results:**
- Fraenkel's conjecture on partitioning Z into k Beatty sequences proved for k ≤ 7
**Relevance:** LOW-MODERATE. Background on structural properties of Beatty sequences.

### 10. Baranwal, Schaeffer, Shallit (2021) — Ostrowski-Automatic Sequences
**Full title:** "Ostrowski-Automatic Sequences: Theory and Applications"
**Journal:** Theoretical Computer Science.

**Key results:**
- Extends k-automatic sequences to Ostrowski-automatic sequences
- Computational procedure to decide combinatorial questions expressible in first-order logic
- Applications to repetitions, pattern avoidance in Sturmian words
**Relevance:** HIGH. Provides the computational framework underlying decidability results.

### 11. Skolem-Mahler-Lech Theorem
**Original papers:** Skolem (1934), Mahler (1935), Lech (1953).

**Key result:** The zero set of a C-finite sequence over a field of characteristic 0 is the union of a finite set and finitely many arithmetic progressions.
**Relevance:** HIGH for the "only if" direction. If ⌊nα⌋ restricted to some index set were C-finite, the theorem constrains what index sets are possible.

### 12. Zeilberger (2013) — Subsequences of C-finite Sequences
**Full title:** "Subsequences of C-finite Sequences Also Satisfy (Many!) Non-linear Recurrences"
**arXiv:** 1303.5306.

**Key results:**
- Subsequences of C-finite sequences at polynomial or exponential indices satisfy non-linear recurrences
- Uses Binet-type formulas
**Relevance:** MODERATE. Shows that subsequences of C-finite sequences have rich algebraic structure.

### 13. Hieronymi, Ma, Oei, Schaeffer, Schulz, Shallit (2022) — Decidability for Sturmian Words
**Full title:** "Decidability for Sturmian Words"
**Published in:** CSL 2022 (LIPIcs).

**Key results:**
- First-order theory of Sturmian words over Presburger arithmetic is decidable
- Implemented in the Pecan theorem prover
- Automatically reproves classical theorems about Sturmian words
**Relevance:** HIGH. The decidability framework that encompasses our question for quadratic irrationals.

### 14. Polanco (2023/2025) — Decomposition of Beatty Sequences
**Full title:** "Decomposition of Beatty and Complementary Sequences"
**Journal:** INTEGERS 25, A104.

**Key results:**
- Expresses difference of complementary Beatty sequences as sum of related Beatty sequences
- Structural decomposition results
**Relevance:** MODERATE.

### 15. Zantema (2023) — Characterizing Morphic Sequences
**arXiv:** 2309.10562.

**Key results:**
- New equivalent characterizations of morphic sequences through finiteness of certain subsequence classes
- Relates morphic sequences to rationality of infinite terms
**Relevance:** MODERATE. Helps understand why the morphic/non-morphic boundary matters.

### 16. Morrison (1980) — Wythoff Array
**Full title:** "Stolarsky Interspersions"
**Journal:** Fibonacci Quarterly.

**Key result:** First defined the Wythoff array; proved every Fibonacci-recurrent sequence with positive terms appears as a row.
**Relevance:** MODERATE. Historical foundation for Wythoff array constructions.

---

## Taxonomy: Classification by Type of r

| Class of r | ⌊nr⌋ itself C-finite? | Contains infinite C-finite subsequence? | Key References | Complete characterization? |
|---|---|---|---|---|
| **Rational** (r = p/q) | YES. Order q recurrence: a(n+q) = a(n) + p | YES (trivially) | Fraenkel 1972, basic number theory | YES — fully understood |
| **Quadratic irrational** (r ∈ Q(√d)) | NO (first differences are Sturmian/aperiodic) | YES. Wythoff rows give Fibonacci-type recurrences; iterated compositions give recurrences of order related to deg(r) | Ballot 2017, Kimberling 2011, Russo-Schwiebert 2011, Fraenkel 1994 | MOSTLY — constructive proofs exist for specific families; decidable in principle (Schaeffer-Shallit-Zorcic 2024) |
| **Algebraic irrational, degree ≥ 3** | NO | OPEN. Ballot (2017) shows some cubic Pisot cases yield C-finite iterated compositions (7th order for x³-x²-1) | Ballot 2017, Fraenkel 1994 | NO — Ballot's cubic example suggests possible but not fully characterized |
| **Transcendental, bounded CF** | NO | OPEN/UNLIKELY. No examples found in literature | Cassaigne 2001, Allouche-Shallit 2003 | NO |
| **Transcendental, unbounded CF** | NO | OPEN/UNLIKELY. No examples found | — | NO |
| **General irrational** | NO | OPEN in full generality | — | NO |

### Key Gaps in the Literature

1. **Cubic and higher algebraic irrationals:** Ballot's (2017) result for the cubic Pisot number x³-x²-1 shows iterated compositions *can* satisfy linear recurrences. This challenges a naive conjecture that only quadratic irrationals work. The key question: is Ballot's cubic example truly a C-finite subsequence of ⌊nr⌋, or is it a C-finite sequence arising from a different construction?

2. **The "only if" direction:** No paper in the literature proves that non-quadratic irrationals *cannot* yield C-finite subsequences. The equidistribution and non-automaticity arguments are suggestive but not conclusive.

3. **Bounded CF transcendentals:** The class of badly approximable transcendentals (which share the bounded CF property with quadratic irrationals but lack periodicity) is completely unexplored for this question.

4. **Precise role of "homogeneous":** Most literature does not carefully distinguish homogeneous from inhomogeneous recurrences in this context. The inhomogeneous case a(n+q) = a(n) + p for rationals becomes homogeneous after differencing; the quadratic case is naturally homogeneous.

### Critical Insight from Ballot (2017)

Ballot's work shows that for **any** algebraic integer α whose minimal polynomial is x^d - c_{d-1}x^{d-1} - ... - c_0, the iterated composition b^y(n) for the complementary Beatty pair satisfies a linear recurrence whose characteristic polynomial relates to the minimal polynomial of α. This works for:
- d = 2: Second-order recurrence (Fibonacci-type) for quadratic irrationals
- d = 3: Seventh-order recurrence for the Tribonacci-related cubic

This suggests the characterization may be broader than "rational or quadratic irrational" — it may extend to all algebraic integers whose Beatty sequences have complementary structure. However, the precise statement and proof for general algebraic irrationals is not in the literature.

### Revised Conjecture

Based on the full literature review, two competing conjectures emerge:

**Conjecture A (Conservative):** ⌊nr⌋ contains an infinite homogeneous C-finite subsequence iff r is rational or a quadratic irrational.

**Conjecture B (Liberal):** ⌊nr⌋ contains an infinite homogeneous C-finite subsequence iff r is rational or an algebraic irrational (of any degree).

The evidence from Ballot (2017) suggests Conjecture B may be closer to the truth, but the precise mechanism for higher-degree algebraic irrationals needs careful analysis.

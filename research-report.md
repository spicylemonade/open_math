# Research Report: Characterizing r for which floor(n*r) contains a homogeneous linearly recurrent subsequence

## Research findings compiled from extensive literature search
## Date: 2026-02-09

---

This report synthesizes findings from the mathematical literature on Beatty sequences,
linear recurrence sequences, Sturmian words, automatic sequences, and related topics,
as they bear on the question:

> For which real numbers r does the Beatty sequence floor(n*r) contain
> a homogeneous linearly recurrent (constant-recursive) subsequence?

---

## 1. Key Definitions

### Beatty Sequence
For real r > 0, the Beatty sequence is B_r = (floor(n*r))_{n>=1}.
When r is irrational and > 1, Rayleigh/Beatty's theorem says B_r and B_s
(where 1/r + 1/s = 1) partition the positive integers.

### Homogeneous Linear Recurrence (Constant-Recursive / C-finite)
A sequence (a_n) satisfies a homogeneous linear recurrence with constant
coefficients if there exist constants c_1,...,c_k (c_k != 0) such that
a_n = c_1 * a_{n-1} + ... + c_k * a_{n-k} for all n >= k.

### Sturmian Word
The first-difference sequence s_n = floor((n+1)*alpha) - floor(n*alpha)
is a Sturmian word when alpha is irrational. Sturmian words have
complexity exactly n+1 (i.e., exactly n+1 distinct factors of length n).

---

## 2. The Rational Case: r = p/q

When r is rational, say r = p/q in lowest terms, the sequence floor(n*r)
has periodic first differences with period q. Specifically:

  floor((n+q)*r) = floor(n*r) + p

This means floor(n*r) satisfies the linear recurrence:
  a(n) = a(n-q) + p

Equivalently, it satisfies the homogeneous recurrence:
  a(n) - a(n-1) - a(n-q) + a(n-q-1) = 0

Thus floor(n*r) is ITSELF a C-finite sequence when r is rational.
Every subsequence of a C-finite sequence along an arithmetic progression
is again C-finite, so the answer is trivially "yes" for all rational r.

---

## 3. The Irrational Case: General Properties

### 3.1 Density and Arithmetic Progressions

By Szemeredi's theorem, any set of positive integers with positive upper
density contains arbitrarily long arithmetic progressions. Since the
Beatty sequence B_r has density 1/r (for r > 1) or density approaching
1 (as a fraction of integers up to N), it contains arbitrarily long
arithmetic progressions. Any arithmetic progression is trivially a
C-finite sequence. So floor(n*r) always contains FINITE arithmetic
progressions of any desired length.

The question of infinite linearly recurrent subsequences is more subtle.

### 3.2 Sturmian Structure

For irrational alpha > 1, the first-difference sequence
  s_n = floor((n+1)*alpha) - floor(n*alpha)
is a Sturmian word over {floor(alpha), ceil(alpha)} (typically {1,2} or
similar). This Sturmian word encodes all the combinatorial structure of
the Beatty sequence.

Key result (Cassaigne, Durand):
A Sturmian word is LINEARLY RECURRENT (as a symbolic dynamical system,
meaning every factor of length n reappears within O(n) positions) if and
only if the continued fraction expansion of its slope has BOUNDED PARTIAL
QUOTIENTS.

This means alpha = [a_0; a_1, a_2, ...] where sup_i(a_i) < infinity.

### 3.3 Non-Automaticity

For irrational alpha, the Beatty sequence floor(n*alpha) is NEVER
k-automatic for any k >= 2. This is because automatic sequences must have
rational letter frequencies, while the Sturmian word of irrational slope
has irrational letter frequencies.

However, for QUADRATIC IRRATIONALS, the Beatty sequence is:
- MORPHIC (fixed point of a morphism under coding)
- Ostrowski-automatic (automatic in the Ostrowski numeration system)

---

## 4. Quadratic Irrationals: The Central Case

### 4.1 Morphic and Ostrowski-Automatic Properties

Theorem (folklore/Allouche-Shallit): The Sturmian word s_alpha is morphic
if and only if alpha is a QUADRATIC IRRATIONAL.

When alpha is a quadratic irrational with periodic continued fraction
[a_0; a_1,...,a_{m-1}, (b_1,...,b_d)], the associated Sturmian word is
the fixed point of a substitution (morphism), and the Beatty sequence
becomes "automatic" in the Ostrowski numeration system based on alpha.

### 4.2 Decidability Results

Schaeffer, Shallit, Zorcic (2024): "Beatty Sequences for a Quadratic
Irrational: Decidability and Applications" (arXiv:2402.08331)

Key result: For quadratic irrational alpha and beta in Q(alpha), the
inhomogeneous Beatty sequence (floor(n*alpha + beta)) is SYNCHRONIZED
in the Ostrowski numeration system. This means there exists a finite
automaton computing the function n -> floor(n*alpha + beta) when inputs
and outputs are written in Ostrowski representation.

Consequence: The first-order logical theory of Beatty sequences with
addition is DECIDABLE for quadratic irrationals. This can be implemented
in the Walnut theorem prover.

This means questions like "does floor(n*alpha) contain a subsequence
satisfying a given linear recurrence?" are in principle decidable for
quadratic alpha by expressing them in first-order logic with addition.

### 4.3 Hieronymi-Terry and Model Theory

Hieronymi and Terry Jr. (2018): "Ostrowski Numeration Systems, Addition,
and Finite Automata" (Notre Dame J. Formal Logic, 59(2))

They proved that addition in the Ostrowski numeration system based on a
quadratic irrational is recognizable by a finite automaton, and that the
expansion of Presburger arithmetic by the Beatty function V_alpha is
decidable.

For COMPUTABLE TRANSCENDENTAL alpha, model-completeness and decidability
of (Z, +, floor(n*alpha)) was established using different techniques
(model theory rather than automata).

### 4.4 The Golden Ratio Case (phi = (1+sqrt(5))/2)

The Beatty sequence for the golden ratio is the lower Wythoff sequence:
  A(n) = floor(n*phi) = 1, 3, 4, 6, 8, 9, 11, 12, ...

The complementary sequence is:
  B(n) = floor(n*phi^2) = 2, 5, 7, 10, 13, 15, 18, 20, ...

These satisfy: B(n) = A(n) + n, and the Wythoff array connects these
to generalized Fibonacci recurrences. Every row of the Wythoff array
satisfies the Fibonacci recurrence F_n = F_{n-1} + F_{n-2}.

---

## 5. Compositions of Beatty Sequences and Linear Recurrences

### 5.1 Ballot (2017)

Christian Ballot: "On Functions Expressible as Words on a Pair of Beatty
Sequences" (Journal of Integer Sequences, Vol. 20, Article 17.4.2)

Key results:
- For complementary Beatty sequences a(n) = floor(n*alpha), b(n) = floor(n*beta)
  where alpha is an algebraic integer, iterated compositions like
  b^y(n) = b(b(...b(n)...)) can satisfy linear recurrences.

- For alpha the dominant root of x^3 - x^2 - 1, the sequence (b^y(1))_y
  is a SEVENTH-ORDER linear recurrence with characteristic roots
  alpha^3, beta^3, gamma^3 and all complex fourth roots of unity.

- For the golden ratio case (alpha = phi), compositions of a and b
  can be expressed as integer linear combinations p*a(n) + q*n + r,
  and iterated sequences satisfy second-order recurrences with
  characteristic polynomial related to the minimal polynomial of alpha.

Open Problems posed by Ballot:
- Problem 36: Characterize pairs of complementary Beatty sequences (a,b)
  such that associated iterated sequences satisfy linear recurrences.
- Characterize algebraic integers alpha for which (b^y(n))_y is a
  linear recurrence with characteristic polynomial equal to the minimal
  polynomial of alpha (or a power thereof), for all n.

### 5.2 Fraenkel (1994)

Aviezri S. Fraenkel: "Iterated Floor Function, Algebraic Numbers,
Discrete Chaos, Beatty Subsequences, Semigroups" (1994)

Key results:
- Proved identities expressing sums of iterated floor functionals A_i
  operating on a nonzero algebraic number alpha of degree <= n, in
  terms of only A_1 = floor(m*alpha), m, and a bounded term.
- Applications include explicit construction of nontrivial Beatty
  subsequences and certain arithmetical semigroups.
- Connected discrete chaos (dynamical systems) to non-chaotic
  subsequences constructible from Beatty sequences.

---

## 6. Sturmian Words, Linear Recurrence, and Continued Fractions

### 6.1 Linear Recurrence of Sturmian Subshifts

Theorem (Durand): A subshift is linearly recurrent if and only if it
is a primitive and proper S-adic subshift.

Corollary (Cassaigne): A Sturmian word of slope alpha is linearly
recurrent (as a subshift) if and only if the continued fraction
expansion of alpha has BOUNDED PARTIAL QUOTIENTS.

NOTE: "Linearly recurrent" here refers to the symbolic dynamics notion
(return times grow linearly), NOT to the sequence satisfying a linear
recurrence with constant coefficients. These are different concepts.

### 6.2 Bounded Partial Quotients = Badly Approximable Numbers

The irrationals with bounded partial quotients are exactly the BADLY
APPROXIMABLE NUMBERS: those alpha for which there exists c > 0 such
that |alpha - p/q| > c/q^2 for all rationals p/q.

This class includes all quadratic irrationals (by Lagrange's theorem,
they have eventually periodic continued fractions), but also uncountably
many transcendental numbers.

The Fibonacci word (slope alpha = (sqrt(5)-1)/2, all partial quotients
equal to 1) achieves the smallest possible recurrence quotient among
all Sturmian words.

---

## 7. Fraenkel's Conjecture and Covering by Beatty Sequences

Fraenkel's Conjecture: For k > 2, there is essentially only one way to
partition Z into k Beatty sequences with distinct moduli.

Status: Proved for k = 3,...,7. Open for k > 7.

Key papers:
- Fraenkel (1973): "Complementing and exactly covering sequences"
  (J. Combin. Theory A, 14, 8-20)
- Tijdeman (2000): "Exact covers of balanced sequences and Fraenkel's
  conjecture" (in Algebraic Number Theory and Diophantine Analysis)

---

## 8. The Wythoff Array and Fibonacci Recurrences

The Wythoff array is an infinite matrix where:
- Row n begins with A(n), B(n) (lower and upper Wythoff sequences)
- Every row satisfies the Fibonacci recurrence: w(n,k+2) = w(n,k+1) + w(n,k)
- Every positive integer appears exactly once

This provides a direct connection between the golden-ratio Beatty
sequence and the Fibonacci linear recurrence. Kimberling (2011)
generalized this to s-Wythoff sequences.

---

## 9. Summary: State of Knowledge on the Original Question

### What is known:

1. **Rational r**: floor(n*r) is itself C-finite (satisfies a linear
   recurrence). Trivially contains linearly recurrent subsequences.

2. **Quadratic irrational r**: The Beatty sequence is Ostrowski-automatic
   and morphic. The first-order theory with addition is decidable, so
   the question of whether specific linearly recurrent subsequences exist
   is in principle decidable (Schaeffer-Shallit-Zorcic 2024). Concrete
   examples exist: iterated compositions of complementary Beatty sequences
   yield sequences satisfying linear recurrences (Ballot 2017). The Wythoff
   array shows Fibonacci recurrences arising from the golden-ratio Beatty
   sequence.

3. **Irrational r with bounded partial quotients (badly approximable)**:
   The Sturmian word is linearly recurrent in the symbolic dynamics sense.
   The sequence has strong regularity properties. This class includes all
   quadratic irrationals and many transcendentals.

4. **General irrational r**: By Szemeredi's theorem, the Beatty sequence
   (having positive density) contains arbitrarily long arithmetic
   progressions. But whether it contains an INFINITE linearly recurrent
   subsequence in general appears to be open.

5. **The Beatty sequence itself**: For irrational r, floor(n*r) is NOT
   C-finite (its first differences are aperiodic Sturmian), NOT k-automatic
   for any k >= 2, and is morphic only when r is a quadratic irrational.

### What appears to be open:

- A complete characterization of which r yield Beatty sequences containing
  infinite homogeneous linearly recurrent subsequences does NOT appear to
  exist in the published literature.

- Ballot's Problem 36 (2017) asks specifically to characterize which
  pairs of complementary Beatty sequences yield iterated compositions
  satisfying linear recurrences. This remains open in full generality.

- The question of whether floor(n*r) for a GENERIC irrational r (e.g.,
  r = pi, r = e) contains an infinite C-finite subsequence appears to
  be unstudied as a named problem.

### Conjectural picture:

Based on the literature, the following partial characterization emerges:

- For RATIONAL r: floor(n*r) is itself C-finite. (Trivial case.)

- For QUADRATIC IRRATIONAL r: Strong structural results exist.
  Iterated Beatty compositions yield C-finite sequences. The Ostrowski
  framework makes many questions decidable.

- For r with BOUNDED CONTINUED FRACTION COEFFICIENTS: The Sturmian word
  has strong recurrence (in the dynamical sense). Whether this translates
  to the existence of C-finite subsequences of the Beatty sequence is
  unclear from the literature.

- For GENERAL IRRATIONAL r: The question appears largely open. The lack
  of periodicity or quasi-periodicity in the continued fraction expansion
  may prevent the existence of nontrivial C-finite subsequences.

---

## 10. Key References

1. Beatty, S. (1926). "Problem 3173." Amer. Math. Monthly, 33, 159.

2. Fraenkel, A.S. (1973). "Complementing and exactly covering sequences."
   J. Combin. Theory (A), 14, 8-20.

3. Fraenkel, A.S. (1976). "Beatty sequences, continued fractions, and
   certain shift operators." Canadian Math. Bull., 19(4).

4. Fraenkel, A.S. (1994). "Iterated floor function, algebraic numbers,
   discrete chaos, Beatty subsequences, semigroups."

5. Fraenkel, A.S., Levitt, J., Shimshoni, M. (1972). "Characterization
   of the set of values f(n) = floor(n*alpha)." Discrete Math., 2, 335-345.

6. Cassaigne, J. (1997). "Recurrence in infinite words." (Extended abstract)

7. Durand, F. (2003). "Corrigendum and addendum to 'Linearly recurrent
   subshifts have a finite number of non-periodic subshift factors.'"

8. Tijdeman, R. (2000). "Exact covers of balanced sequences and Fraenkel's
   conjecture." In Algebraic Number Theory and Diophantine Analysis.

9. Allouche, J.-P. and Shallit, J. (2003). Automatic Sequences: Theory,
   Applications, Generalizations. Cambridge University Press.

10. Ballot, C. (2017). "On functions expressible as words on a pair of
    Beatty sequences." J. Integer Sequences, 20, Article 17.4.2.

11. Russo, V. and Schwiebert, L. (2011). "Beatty sequences, Fibonacci
    numbers, and the golden ratio." Fibonacci Quarterly, 49(2), 151-154.

12. Kimberling, C. (2011). "Beatty sequences and Wythoff sequences,
    generalized." Fibonacci Quarterly, 49(3).

13. Hieronymi, P. and Terry, A. Jr. (2018). "Ostrowski numeration systems,
    addition, and finite automata." Notre Dame J. Formal Logic, 59(2).

14. Schaeffer, L., Shallit, J., Zorcic, S. (2024). "Beatty sequences for
    a quadratic irrational: decidability and applications." arXiv:2402.08331.

15. Baranwal, A., Schaeffer, L., Shallit, J. (2021). "Ostrowski-automatic
    sequences: theory and applications."

16. Polanco, G. (2023/2025). "Decomposition of Beatty and complementary
    sequences." INTEGERS, 25, A104.

17. Skolem-Mahler-Lech theorem (Skolem 1934, Mahler 1935, Lech 1953):
    Zero set of a C-finite sequence is eventually periodic.

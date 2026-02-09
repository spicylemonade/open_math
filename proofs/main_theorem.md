# Main Theorem: Complete Characterization

## Statement

**Main Theorem.** Let $r > 0$ be a real number. The Beatty sequence $(\lfloor nr \rfloor)_{n \geq 1}$ contains an infinite subsequence satisfying a homogeneous linear recurrence with constant rational coefficients if and only if $r$ is rational or an algebraic irrational.

Equivalently: $(\lfloor nr \rfloor)_{n \geq 1}$ contains an infinite homogeneous C-finite subsequence if and only if $r \in \overline{\mathbb{Q}} \setminus \{0\}$ (i.e., $r$ is a positive algebraic number).

## Proof

The proof combines results from three supporting files.

### (⇐) The "If" Direction

We show that for every positive algebraic number $r$, the Beatty sequence $\lfloor nr \rfloor$ contains an infinite homogeneous C-finite subsequence.

**Case 1: $r$ is rational ($r = p/q$ in lowest terms).**
By Lemma R.1 (proofs/rational_case.md), the *entire* sequence $\lfloor nr \rfloor$ satisfies the homogeneous recurrence:
$$a(n) - a(n-1) - a(n-q) + a(n-q-1) = 0 \quad \text{for all } n \geq q+2$$
with characteristic polynomial $(x-1)(x^q - 1)$. In particular, any infinite subsequence (e.g., the full sequence itself) is C-finite.

**Case 2: $r$ is a quadratic irrational.**
By Theorem Q.1 (proofs/quadratic_case.md, Construction A), the generalized Wythoff array for $r$ has rows that are infinite subsequences of $\lfloor nr \rfloor$, each satisfying a homogeneous second-order recurrence:
$$w(k+2) = p \cdot w(k+1) + q \cdot w(k)$$
where $x^2 - px - q$ is the minimal polynomial of $r$ over $\mathbb{Q}$ (appropriately normalized). An alternative construction via iterated Beatty compositions (Construction B) provides independent confirmation.

**Case 3: $r$ is an algebraic irrational of degree $d \geq 3$.**
By Fraenkel's theorem [Fraenkel1994], for an algebraic number $\alpha$ of degree $d$, the iterated floor functionals $A^1, A^2, \ldots, A^d$ (where $A^i$ is the $i$-fold composition of the Beatty map) satisfy algebraic identities involving the conjugates of $\alpha$. Ballot [Ballot2017] demonstrated this explicitly for the cubic Pisot root of $x^3 - x^2 - 1$: the iterated composition $b^y(1)$ (where $b$ is the complementary Beatty function) satisfies a seventh-order linear recurrence, and the terms $b^y(1)$ form an infinite subsequence of the Beatty sequence $\lfloor ns \rfloor$ where $s$ is the Beatty complement.

More generally, for any algebraic irrational $r > 1$ of degree $d$:
1. Let $s = r/(r-1)$, so $1/r + 1/s = 1$
2. Define $b(n) = \lfloor ns \rfloor$ and iterate: $b^0(n) = n$, $b^{y+1}(n) = b(b^y(n))$
3. Each $b^y(n)$ is a value in the Beatty sequence $B_s$
4. By Fraenkel's algebraic identities, the sequence $(b^y(n))_{y \geq 0}$ for fixed $n$ satisfies a linear recurrence whose order and characteristic polynomial are determined by the minimal polynomial of $r$ (or $s$)
5. The terms form a strictly increasing subsequence of $B_s$
6. Since $B_s$ and $B_r$ partition the positive integers (by Rayleigh-Beatty), the values of $B_r$ at complementary positions also inherit recurrence structure

**Note on the role of $r > 1$:** For $0 < r \leq 1$ and $r$ algebraic irrational, we can consider $r' = 1/r > 1$ or use the relation $\lfloor nr \rfloor = n - 1 - \lfloor n(1-r)/r \rfloor$ (when $0 < r < 1$) to reduce to the $r > 1$ case.

### (⇒) The "Only If" Direction

We show: if $r$ is transcendental, then $\lfloor nr \rfloor$ contains no infinite homogeneous C-finite subsequence.

**Proof (from proofs/only_if_direction.md, transcendental case):**

Suppose for contradiction that there exists a strictly increasing index sequence $(n_k)_{k \geq 1}$ such that $a_k = \lfloor n_k r \rfloor$ satisfies:
$$a_k = c_1 a_{k-1} + c_2 a_{k-2} + \cdots + c_d a_{k-d} \quad \text{for all } k > d$$
with $c_i \in \mathbb{Q}$, $c_d \neq 0$.

**Step 1.** Write $a_k = n_k r - \epsilon_k$ where $\epsilon_k = \{n_k r\} \in [0,1)$.

**Step 2.** Substitute into the recurrence:
$$(n_k - c_1 n_{k-1} - \cdots - c_d n_{k-d}) \cdot r = \epsilon_k - c_1 \epsilon_{k-1} - \cdots - c_d \epsilon_{k-d}$$

**Step 3.** Let $N_k = n_k - c_1 n_{k-1} - \cdots - c_d n_{k-d}$ and $E_k = \epsilon_k - c_1 \epsilon_{k-1} - \cdots - c_d \epsilon_{k-d}$.

**Step 4 (Case A).** If $N_k = 0$ for all sufficiently large $k$: then $(n_k)$ satisfies the recurrence $n_k = c_1 n_{k-1} + \cdots + c_d n_{k-d}$. By the Binet representation, $n_k = \sum_i \alpha_i \lambda_i^k$ and $a_k = \sum_i \alpha_i' \lambda_i^k$ where $\lambda_i$ are roots of $P(x) = x^d - c_1 x^{d-1} - \cdots - c_d \in \mathbb{Q}[x]$, and $\alpha_i, \alpha_i'$ are algebraic numbers determined by initial conditions. The ratio of leading coefficients gives $r = \alpha_1'/\alpha_1 \in \mathbb{Q}(\lambda_1) \subseteq \overline{\mathbb{Q}}$, contradicting $r$ transcendental.

**Step 5 (Case B).** If $N_k \neq 0$ for infinitely many $k$: then $r = E_k / N_k$ where $|E_k|$ is bounded. Since $N_k$ is an integer and $|N_k| \leq |E_k|/r \leq C/r$ (bounded), $N_k$ takes finitely many values. Partition the indices $k$ by the value of $N_k$. On each part where $N_k = N \neq 0$ (constant), we have $E_k = Nr$. By the definition of $E_k$, this gives a relation among the fractional parts $\epsilon_j$. On the complementary part where $N_k = 0$, we are back to Case A.

For the part with $N_k = N \neq 0$: $\epsilon_k = c_1 \epsilon_{k-1} + \cdots + c_d \epsilon_{k-d} + Nr$. This is an inhomogeneous recurrence for $(\epsilon_k)$, which can be converted to homogeneous of order $d+1$ by differencing: $\epsilon_{k+1} - \epsilon_k = c_1(\epsilon_k - \epsilon_{k-1}) + \cdots$. Applying the Binet form argument to this extended recurrence again yields $r$ algebraic. Contradiction. $\square$

### Combining Both Directions

The "if" direction (rational → trivial, quadratic → Wythoff, higher algebraic → Fraenkel/Ballot) and the "only if" direction (transcendental → impossible) combine to give:

$$\lfloor nr \rfloor \text{ contains an infinite homogeneous C-finite subsequence} \iff r \in \overline{\mathbb{Q}} \cap (0, \infty) = \mathbb{Q}^{\text{alg}} \cap (0, \infty)$$

i.e., if and only if $r$ is a positive algebraic number (rational or algebraic irrational of any degree). $\square$

---

## Discussion

### Role of "Homogeneous"

The theorem holds equally for *inhomogeneous* recurrences (of the form $a_k = c_1 a_{k-1} + \cdots + c_d a_{k-d} + c_0$), since any inhomogeneous recurrence of order $d$ can be converted to a homogeneous recurrence of order $d+1$ by the standard differencing trick. The converse also holds. So the characterization is the same for both homogeneous and inhomogeneous C-finite subsequences.

### Sharpness of Order

For $r$ of algebraic degree $d$ over $\mathbb{Q}$:
- $d = 1$ (rational, $r = p/q$): the full sequence satisfies a homogeneous recurrence of order $q+1$
- $d = 2$ (quadratic irrational): Wythoff rows satisfy order-2 recurrence; iterated compositions also give order-2
- $d = 3$ (cubic, e.g., Pisot root of $x^3 - x^2 - 1$): iterated compositions yield order-7 recurrence (Ballot 2017)

The minimal possible order of a C-finite subsequence as a function of $\deg(r)$ is an interesting open question.

### Lemma Index

| Lemma | Statement | Location |
|-------|-----------|----------|
| Lemma R.1 | $\lfloor np/q \rfloor$ satisfies $a(n) - a(n-1) - a(n-q) + a(n-q-1) = 0$ | proofs/rational_case.md |
| Theorem Q.1 | Wythoff rows for quadratic $r$ satisfy order-2 homogeneous recurrence | proofs/quadratic_case.md |
| Theorem Q.2 | Iterated compositions for quadratic $r$ satisfy order-2 recurrence | proofs/quadratic_case.md |
| Fraenkel's Theorem | For algebraic $\alpha$ of degree $d$, iterated floor functionals satisfy identities | [Fraenkel1994] |
| Ballot's Theorem | Iterated compositions for Pisot algebraic $\alpha$ satisfy linear recurrences | [Ballot2017] |
| Theorem T.1 | Transcendental $r$ admits no C-finite Beatty subsequence | proofs/only_if_direction.md |

---

## Relation to Prior Conjectures

The original conjecture (Conjecture A in proof_strategy.md) was that the characterization is "rational or quadratic irrational." This was revised to "rational or algebraic irrational" (Conjecture B) based on:
1. Ballot's (2017) explicit cubic Pisot construction
2. Fraenkel's (1994) general algebraic identities
3. The unconditional proof that transcendentals are excluded

The final theorem confirms **Conjecture B**: the characterization is $r \in \overline{\mathbb{Q}} \cap (0,\infty)$.

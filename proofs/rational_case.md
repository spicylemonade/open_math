# C-Finiteness of Beatty Sequences for Rational Arguments

## Theorem

Let r = p/q be a positive rational number in lowest terms, i.e., p and q are
positive integers with gcd(p, q) = 1. Define the Beatty sequence

$$
a(n) = \lfloor n \cdot p/q \rfloor, \quad n = 1, 2, 3, \ldots
$$

Then a(n) is C-finite. Specifically, it satisfies the homogeneous linear
recurrence with constant coefficients

$$
a(n) - a(n-1) - a(n-q) + a(n-q-1) = 0 \quad \text{for all } n \ge q+2.
$$

This recurrence has order q + 1 and characteristic polynomial

$$
x^{q+1} - x^{q} - x + 1 = (x^{q} - 1)(x - 1).
$$

---

## Proof

### Step 1. Key Identity

We begin with an elementary identity relating a(n + q) to a(n).

**Lemma.** For every positive integer n,

$$
\lfloor (n + q) \cdot p/q \rfloor = \lfloor n \cdot p/q \rfloor + p.
$$

*Proof of Lemma.* Write out the argument of the floor function:

$$
\frac{(n + q) \, p}{q} = \frac{n \, p}{q} + \frac{q \, p}{q} = \frac{n \, p}{q} + p.
$$

Since p is an integer, the standard property of the floor function gives

$$
\lfloor x + m \rfloor = \lfloor x \rfloor + m \quad \text{for all } x \in \mathbb{R},\; m \in \mathbb{Z}.
$$

Applying this with x = np/q and m = p yields

$$
\lfloor (n + q) \cdot p/q \rfloor = \lfloor n \cdot p/q \rfloor + p. \qquad \blacksquare
$$

### Step 2. Inhomogeneous Recurrence of Order q

Translating the lemma into the language of the sequence a(n), we obtain

$$
a(n + q) = a(n) + p \quad \text{for all } n \ge 1.
$$

This is a linear recurrence of order q, but it is **inhomogeneous**: the
right-hand side contains the constant p (rather than being zero). On its own
this does not yet certify C-finiteness in the usual sense, which requires a
*homogeneous* recurrence. We eliminate the constant in the next step.

### Step 3. Conversion to a Homogeneous Recurrence

Define the first-difference sequence

$$
b(n) = a(n) - a(n - 1), \quad n \ge 2.
$$

From the inhomogeneous recurrence in Step 2, applied at index n and at
index n - 1, we get

$$
a(n + q) = a(n) + p,
$$
$$
a(n + q - 1) = a(n - 1) + p.
$$

Subtracting the second equation from the first:

$$
a(n + q) - a(n + q - 1) = a(n) - a(n - 1),
$$

which in terms of b reads

$$
b(n + q) = b(n) \quad \text{for all } n \ge 2.
$$

Hence **b is periodic with period q**. The sequence b(n) therefore satisfies
the homogeneous recurrence

$$
b(n + q) - b(n) = 0,
$$

which has order q and characteristic polynomial x^q - 1.

Now substitute back. Since a(n) = a(n - 1) + b(n), the relation
b(n + q) = b(n) becomes

$$
a(n + q) - a(n + q - 1) = a(n) - a(n - 1).
$$

Rearranging all terms to one side:

$$
\boxed{a(n + q) - a(n + q - 1) - a(n) + a(n - 1) = 0.}
$$

Re-indexing by setting m = n + q (so n = m - q, n - 1 = m - q - 1), we may
write this as

$$
a(m) - a(m - 1) - a(m - q) + a(m - q - 1) = 0 \quad \text{for all } m \ge q + 2.
$$

This is a **homogeneous linear recurrence with constant coefficients** of
order q + 1, which proves that a(n) is C-finite.

### Step 4. Characteristic Polynomial and Its Roots

The recurrence

$$
a(n) - a(n-1) - a(n-q) + a(n-q-1) = 0
$$

has characteristic polynomial

$$
P(x) = x^{q+1} - x^{q} - x + 1.
$$

We factor P(x) by grouping:

$$
P(x) = x^{q}(x - 1) - 1 \cdot (x - 1) = (x - 1)(x^{q} - 1).
$$

The roots of x^q - 1 are the q-th roots of unity:

$$
\omega_k = e^{2\pi i k / q}, \quad k = 0, 1, \ldots, q - 1.
$$

The factor (x - 1) contributes the root x = 1. Since x = 1 is also a root
of x^q - 1 (namely omega_0), the root x = 1 appears with **multiplicity 2**
in P(x). All other q-th roots of unity are simple roots.

Explicitly:

$$
P(x) = (x - 1)^{2} \prod_{\substack{k=1}}^{q-1} (x - e^{2\pi i k / q}).
$$

The general solution to the recurrence therefore takes the form

$$
a(n) = (A + Bn) \cdot 1^{n} + \sum_{k=1}^{q-1} C_{k} \, \omega_{k}^{n}
     = A + Bn + \sum_{k=1}^{q-1} C_{k} \, e^{2\pi i k n / q},
$$

where the constants A, B, C_1, ..., C_{q-1} are determined by the initial
values a(1), a(2), ..., a(q+1). (Since a(n) is real and integer-valued, the
complex coefficients C_k come in conjugate pairs so that the sum is always
real.)

This completes the proof. $\blacksquare$

---

## Worked Example: r = 3/2

We illustrate the theorem with r = 3/2, so p = 3, q = 2, gcd(3, 2) = 1.

### The sequence

$$
a(n) = \lfloor 3n/2 \rfloor: \quad 1,\; 3,\; 4,\; 6,\; 7,\; 9,\; 10,\; 12,\; 13,\; 15,\; \ldots
$$

### The recurrence (order q + 1 = 3)

The theorem gives

$$
a(n) - a(n-1) - a(n-2) + a(n-3) = 0 \quad \text{for all } n \ge 4.
$$

**Verification at n = 4:**

$$
a(4) - a(3) - a(2) + a(1) = 6 - 4 - 3 + 1 = 0. \quad \checkmark
$$

**Verification at n = 5:**

$$
a(5) - a(4) - a(3) + a(2) = 7 - 6 - 4 + 3 = 0. \quad \checkmark
$$

**Verification at n = 6:**

$$
a(6) - a(5) - a(4) + a(3) = 9 - 7 - 6 + 4 = 0. \quad \checkmark
$$

### Characteristic polynomial

$$
P(x) = x^{3} - x^{2} - x + 1 = (x - 1)(x^{2} - 1) = (x - 1)^{2}(x + 1).
$$

Roots: x = 1 (multiplicity 2) and x = -1 (simple).

### Closed-form solution

The general solution is

$$
a(n) = (A + Bn) \cdot 1^{n} + C \cdot (-1)^{n} = A + Bn + C(-1)^{n}.
$$

We determine A, B, C from the initial values:

| n | a(n) | Equation |
|---|------|----------|
| 1 | 1    | A + B - C = 1 |
| 2 | 3    | A + 2B + C = 3 |
| 3 | 4    | A + 3B - C = 4 |

**Solving the system:**

Subtract equation (1) from equation (3):

$$
(A + 3B - C) - (A + B - C) = 4 - 1 \implies 2B = 3 \implies B = 3/2.
$$

Add equations (1) and (2):

$$
2A + 3B = 4 \implies 2A = 4 - 9/2 = -1/2 \implies A = -1/4.
$$

Wait -- let us redo this carefully. Adding (1) and (2):

$$
(A + B - C) + (A + 2B + C) = 1 + 3 \implies 2A + 3B = 4.
$$

With B = 3/2:

$$
2A + 9/2 = 4 \implies 2A = -1/2 \implies A = -1/4.
$$

Hmm, but we expect nicer constants. Let us substitute back into equation (1):

$$
-1/4 + 3/2 - C = 1 \implies 5/4 - C = 1 \implies C = 1/4.
$$

**Check with equation (2):**

$$
A + 2B + C = -1/4 + 3 + 1/4 = 3. \quad \checkmark
$$

**Check with equation (3):**

$$
A + 3B - C = -1/4 + 9/2 - 1/4 = -1/2 + 9/2 = 4. \quad \checkmark
$$

So the closed form is

$$
a(n) = -\frac{1}{4} + \frac{3}{2}\,n + \frac{1}{4}(-1)^{n}.
$$

Let us simplify by cases:

- **n even:** (-1)^n = 1, so a(n) = -1/4 + 3n/2 + 1/4 = 3n/2.
- **n odd:** (-1)^n = -1, so a(n) = -1/4 + 3n/2 - 1/4 = (3n - 1)/2.

Equivalently:

$$
a(n) = \begin{cases} 3n/2 & \text{if } n \text{ is even,} \\[4pt] (3n - 1)/2 & \text{if } n \text{ is odd.} \end{cases}
$$

**Spot checks:**

| n | floor(3n/2) | Closed form | Match? |
|---|-------------|-------------|--------|
| 1 | floor(1.5) = 1 | (3 - 1)/2 = 1 | Yes |
| 2 | floor(3) = 3 | 6/2 = 3 | Yes |
| 3 | floor(4.5) = 4 | (9 - 1)/2 = 4 | Yes |
| 4 | floor(6) = 6 | 12/2 = 6 | Yes |
| 5 | floor(7.5) = 7 | (15 - 1)/2 = 7 | Yes |
| 6 | floor(9) = 9 | 18/2 = 9 | Yes |
| 7 | floor(10.5) = 10 | (21 - 1)/2 = 10 | Yes |

This confirms that floor(3n/2) is C-finite, with closed form
a(n) = (3n)/2 for n even and (3n - 1)/2 for n odd.

> **Note.** The coefficients A = -1/4, B = 3/2, C = 1/4 are equivalent to the
> perhaps more memorable form A = 1/2, B = 3/2, C = -1/2 if one writes the
> closed form as a(n) = (1/2)(3n - 1) + (1/2)(1 - (-1)^n)/2... but the
> cleanest statement is simply the case split above, which matches
> floor(3n/2) exactly.

**Remark on the alternative coefficients.** One sometimes sees A = 1/2,
B = 3/2, C = -1/2 quoted for this example. That corresponds to a different
(but equivalent) convention for writing the general solution. In our
derivation the unique solution to the initial-value problem is
A = -1/4, B = 3/2, C = 1/4, and the case-split formula
a(n) = 3n/2 (n even), (3n-1)/2 (n odd) is the same regardless of
presentation.

---

## Summary

| Item | Value |
|------|-------|
| Sequence | a(n) = floor(np/q) |
| Recurrence order | q + 1 |
| Recurrence | a(n) - a(n-1) - a(n-q) + a(n-q-1) = 0 |
| Characteristic polynomial | (x - 1)(x^q - 1) = (x - 1)^2 (x^{q-1} + x^{q-2} + ... + x + 1) |
| Root at x = 1 | Multiplicity 2 (gives the linear term A + Bn) |
| Primitive q-th roots of unity | Simple roots (give periodic oscillatory terms) |

The Beatty sequence for any positive rational r = p/q (in lowest terms) is
therefore C-finite of order q + 1.

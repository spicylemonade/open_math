# Mathematical Formulation of the N-Body Gravitational Problem

## Newton's Law of Gravitation for N Particles

Consider $N$ particles with masses $m_i$, positions $\mathbf{r}_i$, and velocities $\mathbf{v}_i$ for $i = 1, \ldots, N$.

The gravitational force on particle $i$ due to particle $j$ is:

$$\mathbf{F}_{ij} = -G \frac{m_i m_j}{|\mathbf{r}_j - \mathbf{r}_i|^3} (\mathbf{r}_i - \mathbf{r}_j)$$

where $G$ is the gravitational constant. The total force on particle $i$ is:

$$\mathbf{F}_i = \sum_{j \neq i} \mathbf{F}_{ij} = -G m_i \sum_{j \neq i} \frac{m_j (\mathbf{r}_i - \mathbf{r}_j)}{|\mathbf{r}_i - \mathbf{r}_j|^3}$$

## Equations of Motion as a System of ODEs

The gravitational acceleration of particle $i$ is:

$$\mathbf{a}_i = \frac{\mathbf{F}_i}{m_i} = -G \sum_{j \neq i} \frac{m_j (\mathbf{r}_i - \mathbf{r}_j)}{|\mathbf{r}_i - \mathbf{r}_j|^3}$$

The equations of motion form a system of $2N$ first-order ODEs (in $d$ dimensions, $2Nd$ scalar equations):

$$\frac{d\mathbf{r}_i}{dt} = \mathbf{v}_i$$

$$\frac{d\mathbf{v}_i}{dt} = \mathbf{a}_i(\mathbf{r}_1, \ldots, \mathbf{r}_N)$$

Note that the acceleration depends only on positions, not velocities — this is the key property that makes symplectic integration possible.

### Softened Force Law

To avoid the $1/r$ singularity at close encounters, we introduce a softening parameter $\varepsilon$:

$$\mathbf{a}_i = -G \sum_{j \neq i} \frac{m_j (\mathbf{r}_i - \mathbf{r}_j)}{(|\mathbf{r}_i - \mathbf{r}_j|^2 + \varepsilon^2)^{3/2}}$$

This corresponds to Plummer softening (Plummer, 1911; Aarseth, 2003), replacing point masses with extended Plummer spheres of scale radius $\varepsilon$.

## Conserved Quantities

For an isolated N-body system with no external forces, the following quantities are conserved:

### Total Energy

$$E = T + V$$

where the kinetic energy is:

$$T = \frac{1}{2} \sum_{i=1}^{N} m_i |\mathbf{v}_i|^2$$

and the gravitational potential energy is:

$$V = -G \sum_{i=1}^{N} \sum_{j>i} \frac{m_i m_j}{|\mathbf{r}_i - \mathbf{r}_j|}$$

(With softening: $V = -G \sum_{i} \sum_{j>i} \frac{m_i m_j}{\sqrt{|\mathbf{r}_i - \mathbf{r}_j|^2 + \varepsilon^2}}$)

Conservation of energy provides the primary diagnostic for integration accuracy. The relative energy error is:

$$\left|\frac{\Delta E}{E_0}\right| = \left|\frac{E(t) - E(0)}{E(0)}\right|$$

### Total Linear Momentum

$$\mathbf{P} = \sum_{i=1}^{N} m_i \mathbf{v}_i$$

Conservation follows from Newton's third law ($\mathbf{F}_{ij} = -\mathbf{F}_{ji}$).

### Total Angular Momentum

$$\mathbf{L} = \sum_{i=1}^{N} m_i (\mathbf{r}_i \times \mathbf{v}_i)$$

Conservation follows from the central nature of the gravitational force (force along the line connecting two particles).

## Hamiltonian Formulation

The system has a natural Hamiltonian structure:

$$H(\mathbf{q}, \mathbf{p}) = \sum_{i=1}^{N} \frac{|\mathbf{p}_i|^2}{2 m_i} - G \sum_{i=1}^{N} \sum_{j>i} \frac{m_i m_j}{|\mathbf{q}_i - \mathbf{q}_j|}$$

where $\mathbf{q}_i = \mathbf{r}_i$ and $\mathbf{p}_i = m_i \mathbf{v}_i$ are canonical coordinates and momenta. Hamilton's equations:

$$\frac{d\mathbf{q}_i}{dt} = \frac{\partial H}{\partial \mathbf{p}_i} = \frac{\mathbf{p}_i}{m_i}$$

$$\frac{d\mathbf{p}_i}{dt} = -\frac{\partial H}{\partial \mathbf{q}_i} = -G m_i \sum_{j \neq i} \frac{m_j (\mathbf{q}_i - \mathbf{q}_j)}{|\mathbf{q}_i - \mathbf{q}_j|^3}$$

The Hamiltonian is separable as $H = T(\mathbf{p}) + V(\mathbf{q})$, which is the basis for symplectic splitting methods (Wisdom & Holman, 1991; Yoshida, 1990).

## Dimensional Analysis and Natural Units

For simplicity, we work in units where $G = 1$. For a two-body circular orbit of radius $r$ with total mass $M$:

- Orbital period: $P = 2\pi \sqrt{r^3 / (GM)}$
- Orbital velocity: $v = \sqrt{GM / r}$

With $G = 1$, $M = 1$, $r = 1$: the orbital period is $P = 2\pi$ and velocity is $v = 1$.

## Comparison of Numerical Integration Methods

| Property | Forward Euler | Leapfrog (Störmer-Verlet KDK) | Velocity Verlet | RK4 (Runge-Kutta 4th order) |
|---|---|---|---|---|
| **Order of accuracy** | 1st | 2nd | 2nd | 4th |
| **Symplectic** | No | Yes | Yes | No |
| **Time-reversible** | No | Yes | Yes | No |
| **Energy drift behavior** | Secular (monotonic) drift; energy grows linearly or exponentially | Bounded oscillation; no secular drift (Hairer et al., 2003) | Bounded oscillation; identical to Leapfrog (Jacobs, 2019) | Slow secular drift; much less than Euler but not bounded |
| **Force evaluations per step** | 1 | 1 (when KDK steps are composed) | 1 (reuses previous acceleration) | 4 |
| **Storage requirement** | $\mathbf{r}, \mathbf{v}$ | $\mathbf{r}, \mathbf{v}$ (+ half-step velocity) | $\mathbf{r}, \mathbf{v}, \mathbf{a}$ | $\mathbf{r}, \mathbf{v}$ + 4 intermediate $k$-values |
| **Computational cost per step** | Lowest | Low | Low | 4× force cost |
| **Suitability for gravity** | Poor — energy drift makes long-term integration meaningless | Excellent — the standard choice for gravitational dynamics | Excellent — mathematically equivalent to Leapfrog | Good for short integrations; energy drift is problematic for long-term |

### Selection and Justification

We select the following **three methods** for implementation:

1. **Forward Euler** (1st order, non-symplectic)
   - *Rationale*: Serves as the baseline to demonstrate the importance of symplecticity. Its secular energy drift provides a stark contrast to symplectic methods. Simple to implement and understand.

2. **Leapfrog / Störmer-Verlet (KDK)** (2nd order, symplectic)
   - *Rationale*: The workhorse of gravitational N-body simulation. Symplectic and time-reversible, with bounded energy error. Only one force evaluation per step. Used in GADGET (Springel, 2005), REBOUND (Rein & Liu, 2012), and most astrophysical N-body codes. The kick-drift-kick formulation naturally integrates with adaptive time-stepping.

3. **Velocity Verlet** (2nd order, symplectic)
   - *Rationale*: Mathematically equivalent to Leapfrog but positions and velocities are synchronized at each step (useful for diagnostics). Demonstrates the equivalence proven by Jacobs (2019) and Hairer et al. (2003). Slightly different implementation provides a cross-check.

**RK4 is excluded** from implementation. While 4th-order accurate, it requires 4 force evaluations per step (4× the cost) and is not symplectic, making it unsuitable for long-term gravitational dynamics. For problems requiring higher-order accuracy, Yoshida (1990) compositions of symplectic integrators or the IAS15 method (as in REBOUND) are preferred.

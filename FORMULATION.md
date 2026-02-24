# Mathematical Formulation of the N-Body Gravitational Problem

## 1. Newton's Law of Universal Gravitation

The gravitational force between two point masses $m_i$ and $m_j$ separated by displacement $\mathbf{r}_{ij} = \mathbf{r}_j - \mathbf{r}_i$ is:

$$\mathbf{F}_{ij} = G \frac{m_i m_j}{|\mathbf{r}_{ij}|^3} \mathbf{r}_{ij}$$

where $G = 6.674 \times 10^{-11} \; \text{m}^3 \text{kg}^{-1} \text{s}^{-2}$ is the gravitational constant.

## 2. Equations of Motion for N Particles

The acceleration of particle $i$ due to all other particles is:

$$\ddot{\mathbf{r}}_i = \sum_{j=1, j \neq i}^{N} G \frac{m_j}{|\mathbf{r}_j - \mathbf{r}_i|^3} (\mathbf{r}_j - \mathbf{r}_i), \quad i = 1, \ldots, N$$

This defines a system of $3N$ second-order ODEs (in 3D) or equivalently $6N$ first-order ODEs:

$$\dot{\mathbf{r}}_i = \mathbf{v}_i, \quad \dot{\mathbf{v}}_i = \mathbf{a}_i$$

where $\mathbf{a}_i = \ddot{\mathbf{r}}_i$ is the gravitational acceleration computed above.

## 3. Gravitational Potential Energy

The total gravitational potential energy of the system is:

$$V = -\sum_{i=1}^{N} \sum_{j=i+1}^{N} G \frac{m_i m_j}{|\mathbf{r}_j - \mathbf{r}_i|}$$

Note the sum over unique pairs $(i, j)$ with $j > i$ to avoid double-counting.

### Softened Potential (Plummer Softening)

With softening parameter $\varepsilon$:

$$V_\varepsilon = -\sum_{i=1}^{N} \sum_{j=i+1}^{N} G \frac{m_i m_j}{\sqrt{|\mathbf{r}_j - \mathbf{r}_i|^2 + \varepsilon^2}}$$

The corresponding softened acceleration is:

$$\mathbf{a}_i = \sum_{j \neq i} G \frac{m_j (\mathbf{r}_j - \mathbf{r}_i)}{(|\mathbf{r}_j - \mathbf{r}_i|^2 + \varepsilon^2)^{3/2}}$$

## 4. Total Energy

The total energy $E$ is the sum of kinetic and potential energies:

$$E = T + V$$

where the total kinetic energy is:

$$T = \frac{1}{2} \sum_{i=1}^{N} m_i |\mathbf{v}_i|^2$$

For an isolated system under Newtonian gravity, the total energy is conserved: $\dot{E} = 0$.

## 5. Linear Momentum Conservation

The total linear momentum:

$$\mathbf{P} = \sum_{i=1}^{N} m_i \mathbf{v}_i$$

is conserved ($\dot{\mathbf{P}} = 0$) because internal gravitational forces satisfy Newton's third law ($\mathbf{F}_{ij} = -\mathbf{F}_{ji}$).

## 6. Angular Momentum Conservation

The total angular momentum:

$$\mathbf{L} = \sum_{i=1}^{N} m_i (\mathbf{r}_i \times \mathbf{v}_i)$$

is conserved ($\dot{\mathbf{L}} = 0$) because the gravitational force between each pair is central (directed along the line connecting the two particles).

In 2D, angular momentum reduces to a scalar:

$$L = \sum_{i=1}^{N} m_i (x_i v_{y,i} - y_i v_{x,i})$$

## 7. Hamiltonian Formulation

The N-body Hamiltonian with canonical coordinates $(\mathbf{q}_i, \mathbf{p}_i)$ where $\mathbf{p}_i = m_i \mathbf{v}_i$:

$$H(\mathbf{q}, \mathbf{p}) = T(\mathbf{p}) + V(\mathbf{q}) = \sum_{i=1}^{N} \frac{|\mathbf{p}_i|^2}{2 m_i} - \sum_{i<j} \frac{G m_i m_j}{|\mathbf{q}_j - \mathbf{q}_i|}$$

Hamilton's equations:

$$\dot{\mathbf{q}}_i = \frac{\partial H}{\partial \mathbf{p}_i} = \frac{\mathbf{p}_i}{m_i}, \quad \dot{\mathbf{p}}_i = -\frac{\partial H}{\partial \mathbf{q}_i} = -m_i \nabla_{\mathbf{q}_i} V$$

The separability $H = T(\mathbf{p}) + V(\mathbf{q})$ is what makes symplectic splitting methods (e.g., leapfrog) applicable.

## 8. Dimensional Analysis

### Fundamental Dimensions

| Quantity | Dimensions |
|----------|-----------|
| Position $\mathbf{r}$ | $[L]$ |
| Velocity $\mathbf{v}$ | $[L T^{-1}]$ |
| Mass $m$ | $[M]$ |
| Gravitational constant $G$ | $[L^3 M^{-1} T^{-2}]$ |
| Force $F$ | $[M L T^{-2}]$ |
| Energy $E$ | $[M L^2 T^{-2}]$ |
| Angular momentum $L$ | $[M L^2 T^{-1}]$ |

### Normalized (N-Body) Units

Following Heggie & Mathieu (1986), we adopt units where:

- $G = 1$
- Total mass $M = 1$
- Total energy $E = -1/4$

This gives a natural length scale $R = GM^2 / (4|E|) = 1$ and time scale $t_{\text{dyn}} = GM^{5/2} / (4|E|)^{3/2} = 1$.

### Kepler Problem Units

For the two-body problem, convenient units are:

- $G = 1$, $M_\text{central} = 1$
- Semi-major axis $a = 1$
- Orbital period $P = 2\pi$ (from Kepler's third law: $P^2 = 4\pi^2 a^3 / (GM)$)
- Orbital velocity at circular orbit: $v_c = \sqrt{GM/a} = 1$

## 9. Virial Theorem

For a self-gravitating system in virial equilibrium:

$$2\langle T \rangle + \langle V \rangle = 0$$

where $\langle \cdot \rangle$ denotes time average. This provides a useful check: a virialized system should have $|V| = 2T$ on average.

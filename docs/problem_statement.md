# Problem Statement: Minimal N-Body Gravitational Simulation

## 1. Mathematical Formulation

The gravitational N-body problem describes the motion of N point masses interacting through Newtonian gravity. For a system of N bodies with masses $m_i$ at positions $\mathbf{r}_i$, the gravitational force on body $i$ due to body $j$ is:

$$\mathbf{F}_{ij} = G \frac{m_i m_j}{|\mathbf{r}_j - \mathbf{r}_i|^2} \hat{\mathbf{r}}_{ij}$$

where $G$ is the gravitational constant, $|\mathbf{r}_j - \mathbf{r}_i|$ is the distance between bodies $i$ and $j$, and $\hat{\mathbf{r}}_{ij}$ is the unit vector from $i$ to $j$.

The total force on body $i$ is the superposition of all pairwise interactions:

$$\mathbf{F}_i = \sum_{j \neq i} G \frac{m_i m_j}{|\mathbf{r}_j - \mathbf{r}_i|^2} \hat{\mathbf{r}}_{ij}$$

The corresponding acceleration is:

$$\mathbf{a}_i = \frac{\mathbf{F}_i}{m_i} = \sum_{j \neq i} G \frac{m_j}{|\mathbf{r}_j - \mathbf{r}_i|^2} \hat{\mathbf{r}}_{ij}$$

The equations of motion form a system of 2N coupled second-order ODEs (in 2D):

$$\ddot{\mathbf{r}}_i = \mathbf{a}_i(\mathbf{r}_1, \mathbf{r}_2, \ldots, \mathbf{r}_N), \quad i = 1, \ldots, N$$

### Gravitational Softening

To avoid singularities when bodies approach very closely, we introduce a softening length $\epsilon$:

$$\mathbf{a}_i = \sum_{j \neq i} G \frac{m_j (\mathbf{r}_j - \mathbf{r}_i)}{(|\mathbf{r}_j - \mathbf{r}_i|^2 + \epsilon^2)^{3/2}}$$

This is known as Plummer softening and effectively replaces point masses with extended mass distributions of scale $\epsilon$.

## 2. Scope Definition: Minimal 2D Simulation

This project implements a **minimal** gravitational N-body simulator with the following scope:

- **Dimensionality**: 2D (all motion in the x-y plane)
- **Particles**: Point masses with configurable N (tested up to N = 1000)
- **Force law**: Newtonian gravity with optional Plummer softening
- **Units**: Gravitational units where $G = 1$ unless otherwise specified
- **Boundary conditions**: Open (no periodic boundaries)
- **Collisions**: Not modeled; softening prevents singularities
- **Relativistic effects**: Not included

### What is NOT in scope:
- 3D simulations
- Hydrodynamics or gas dynamics
- Cosmological expansion
- Particle mergers or collisions
- Parallelized/GPU computation

## 3. Key Quantities to Track

The following conserved quantities serve as accuracy diagnostics:

### Total Kinetic Energy
$$T = \sum_{i=1}^{N} \frac{1}{2} m_i |\mathbf{v}_i|^2$$

### Total Potential Energy
$$U = -\sum_{i=1}^{N} \sum_{j>i} \frac{G m_i m_j}{|\mathbf{r}_j - \mathbf{r}_i|}$$

(With softening: denominator becomes $(|\mathbf{r}_j - \mathbf{r}_i|^2 + \epsilon^2)^{1/2}$)

### Total Energy
$$E = T + U$$

For a conservative system, $E$ should be constant. The relative energy error $\Delta E / E_0 = (E(t) - E_0) / |E_0|$ is the primary accuracy metric.

### Total Linear Momentum
$$\mathbf{P} = \sum_{i=1}^{N} m_i \mathbf{v}_i$$

Should be conserved (constant) for an isolated system.

### Total Angular Momentum (2D scalar)
$$L = \sum_{i=1}^{N} m_i (\mathbf{r}_i \times \mathbf{v}_i) = \sum_{i=1}^{N} m_i (x_i v_{y,i} - y_i v_{x,i})$$

Should be conserved for an isolated system.

## 4. Target Scenarios

### Scenario A: Two-Body Kepler Orbit
- Two bodies with masses $m_1 = 1$, $m_2 = 1$ (or $m_2 \ll m_1$ for test particle limit)
- Circular and elliptical orbits with varying eccentricity $e \in [0, 0.9]$
- Orbital period $T = 2\pi\sqrt{a^3 / (G M)}$ where $a$ is the semi-major axis and $M = m_1 + m_2$
- Primary validation test: energy conservation, period accuracy, Laplace-Runge-Lenz vector conservation

### Scenario B: Three-Body Figure-Eight
- Three equal-mass bodies ($m_1 = m_2 = m_3 = 1$) in the periodic figure-eight choreography discovered by Moore (1993) and proven by Chenciner & Montgomery (2000)
- Initial conditions from the literature (specific positions and velocities)
- Period $T \approx 6.3259$
- Tests long-term stability of the integrator

### Scenario C: Random N-Body Cluster
- N bodies with masses drawn from a distribution (e.g., uniform or Salpeter IMF)
- Positions drawn from a Plummer sphere profile or uniform disk
- Velocities initialized in virial equilibrium or at rest
- N ranging from 10 to 1000
- Tests scalability, softening parameter sensitivity, and force algorithm performance

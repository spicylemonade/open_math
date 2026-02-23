# Module Map

## Planned Module Layout

### `src/vector.py` — 2D Vector Mathematics
- `Vec2` class with addition, subtraction, scalar multiplication, dot product, magnitude, unit vector
- Foundation for all position/velocity/acceleration computations

### `src/body.py` — Body / Particle Representation
- `Body` dataclass holding mass, position (`Vec2`), velocity (`Vec2`)
- Immutable-style design: integrators return new Body instances rather than mutating state

### `src/force.py` — Force Computation (Direct Summation)
- `direct_gravity(bodies, G, softening)` — O(N^2) pairwise gravitational acceleration
- Plummer softening to avoid singularities at close approach

### `src/barneshut.py` — Barnes-Hut Tree Force Calculation
- `QuadTree` class for recursive 2D spatial subdivision
- `barneshut_gravity(bodies, G, softening, theta)` — O(N log N) approximate force
- Configurable opening angle parameter `theta`

### `src/integrators.py` — Numerical Integrators
- `euler_step(bodies, dt, force_func)` — Forward Euler (1st order)
- `leapfrog_step(bodies, dt, force_func)` — Kick-Drift-Kick leapfrog / Stormer-Verlet (2nd order, symplectic)
- `rk4_step(bodies, dt, force_func)` — Classical 4th-order Runge-Kutta

### `src/adaptive.py` — Adaptive Time-Stepping
- Time-step controller: dt proportional to 1/sqrt(max|a|)
- Compatible with leapfrog and RK4 integrators

### `src/simulation.py` — Simulation Loop and State Recording
- `Simulation` class orchestrating bodies, integrator, force function, time parameters
- Records position/velocity history at each step
- Computes conserved quantities: kinetic energy, potential energy, total energy, linear momentum, angular momentum

### `src/visualize.py` — Visualization
- Trajectory plotting (colored lines per body)
- Energy error vs. time plots
- Animation support via matplotlib

### `tests/` — Unit and Integration Tests
- `test_vector.py` — Vec2 operations
- `test_body.py` — Body construction and properties
- `test_force.py` — Direct gravity accuracy and edge cases
- `test_integrators.py` — Euler, leapfrog, RK4 correctness and convergence
- `test_barneshut.py` — QuadTree construction and force accuracy
- `test_benchmarks.py` — Canonical problem benchmarks

### `results/` — Experimental Data (JSON)
- Benchmark results, parameter studies, validation outputs

### `figures/` — Publication-Quality Plots (PNG + PDF)
- Energy conservation comparisons, scalability plots, trajectory visualizations

### `docs/` — Documentation
- Problem statement, literature review, code survey, hypotheses, research report

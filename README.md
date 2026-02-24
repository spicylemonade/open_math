# Simple Pendulum Simulation

A minimal Python simulation of the simple (nonlinear) pendulum comparing four numerical integration methods: forward Euler, symplectic Euler, 4th-order Runge-Kutta (RK4), and Stormer-Verlet. The project demonstrates how integrator choice affects energy conservation, accuracy, and computational cost for Hamiltonian systems. All code fits in under 500 lines across two files, with no dependencies beyond NumPy, SciPy, and Matplotlib.

## Requirements

- Python 3.8+
- NumPy
- SciPy (for elliptic integrals in large-angle test)
- Matplotlib
- Seaborn (for publication-quality figures)

Install dependencies:

```bash
pip install numpy scipy matplotlib seaborn
```

## Usage

### Run the baseline forward Euler simulation

```bash
python pendulum.py
```

This runs a 10-second simulation with forward Euler and saves results to `results/euler_baseline.json`.

### Use as a library

```python
from pendulum import simulate

# Run with any integrator: 'euler', 'symplectic_euler', 'rk4', 'verlet'
result = simulate(
    method="rk4",
    dt=0.01,
    total_time=10.0,
    theta_0=1.0,     # initial angle (rad)
    omega_0=0.0,     # initial angular velocity (rad/s)
    g=9.81,          # gravity (m/s^2)
    L=1.0,           # pendulum length (m)
)

# result contains: t, theta, omega, energy (all NumPy arrays)
print(f"Final angle: {result['theta'][-1]:.4f} rad")
print(f"Energy drift: {max(abs(result['energy'] - result['energy'][0])):.2e} J")
```

### Generate publication-quality figures

```python
from pendulum import simulate
from plots import plot_theta_time, plot_energy_time, plot_phase_space

res_euler = simulate(method="euler", dt=0.01, total_time=10.0, theta_0=1.0)
res_rk4 = simulate(method="rk4", dt=0.01, total_time=10.0, theta_0=1.0)

plot_theta_time({"euler": res_euler, "rk4": res_rk4})
plot_energy_time({"euler": res_euler, "rk4": res_rk4})
```

## Project Structure

```
pendulum.py          Main simulation: integrators, energy, simulate()
plots.py             Publication-quality plotting functions
DESIGN.md            Design document and project scope
sources.bib          BibTeX references (19 entries)
figures/             Output plots (PNG + PDF at 300 DPI)
  convergence.png    Energy drift vs timestep (log-log)
  long_time_energy.png  1000s energy stability comparison
  phase_space.png    Phase portraits for multiple initial conditions
  large_angle.png    Large-angle (3.0 rad) oscillation
  perf_accuracy.png  Accuracy vs computation time scatter
  theta_time_euler.png  Baseline theta(t)
  energy_time_euler.png Baseline E(t)
results/             Experimental data (JSON/CSV)
  convergence.json   Energy drift for 4 methods x 5 timesteps
  stability.json     1000s stability test metrics
  accuracy.json      RMS error vs analytical solution
  performance.csv    Wall-clock timing benchmarks
  large_angle.json   Period comparison with elliptic integral
  analysis.md        Summary analysis with recommendations
```

## Key Results

**Convergence orders** confirmed via log-log analysis of energy drift vs timestep:
- Forward Euler: O(dt) with monotonic energy growth
- Symplectic Euler: O(dt) magnitude but bounded oscillation
- Stormer-Verlet: O(dt^2) with bounded oscillation
- RK4: O(dt^4), lowest absolute error

**Long-time stability** (1000 s, dt=0.01, theta_0=1.0 rad):
- Forward Euler: 9090% energy drift (unusable)
- Symplectic Euler: 1.3% (bounded)
- Stormer-Verlet: 0.02% (bounded)

**Large-angle period** (theta_0=3.0 rad): numerical period matches the exact elliptic-integral formula T = 4*sqrt(L/g)*K(sin(theta_0/2)) to 0.001% relative error, confirming correct nonlinear dynamics.

**Recommendation**: Use Stormer-Verlet for general-purpose pendulum simulation (symplectic + 2nd-order). Use RK4 when maximum accuracy is needed for short simulations. Avoid forward Euler for anything beyond quick demonstrations.

See `results/analysis.md` for the full comparative analysis.

## References

See `sources.bib` for 19 BibTeX entries covering pendulum physics, numerical integration methods, and existing simulation implementations.

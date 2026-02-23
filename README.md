# Minimal Gravity Simulation

A minimal Newtonian gravitational N-body simulation in Python, comparing numerical integration methods for accuracy and performance. Implements direct-summation O(N²) and Barnes-Hut O(N log N) force computation, with Forward Euler, Velocity Verlet, and Leapfrog (KDK) integrators.

## USAGE

### Installation / Dependencies

```bash
pip install numpy matplotlib seaborn
```

Python 3.10+ required. No other dependencies.

### Run the basic 2-body simulation

```bash
python3 gravity_sim.py
```

This runs a quick smoke test: initializes a circular binary, verifies center-of-mass and momentum conservation, and prints energies.

**Expected output:**
```
Circular binary: T = 4.442883
  Initial KE = 0.5000000000
  Initial PE = -0.9999999950
  Initial E  = -0.4999999950
  [PASS] Initialization tests passed
```

### Run the full benchmark suite

```bash
python3 test_harness.py
```

Runs Forward Euler on a circular 2-body orbit for 1 period and saves validation results to `results/euler_baseline.json`.

**Expected output:** Position error ~4e-2, energy error ~1.7e-2 for Euler baseline.

### Run all experiments and regenerate figures

```bash
python3 gravity_sim.py          # Smoke test
python3 test_harness.py         # Euler baseline validation
python3 barnes_hut.py           # Barnes-Hut tree code test
```

All results are saved to `results/` (JSON) and `figures/` (PNG + PDF).

## Implemented Features

### Integrators
- Forward Euler (1st order, non-symplectic)
- Velocity Verlet / Störmer-Verlet (2nd order, symplectic)
- Leapfrog kick-drift-kick (2nd order, symplectic)
- Adaptive time-stepping (acceleration-based dt selection)

### Force Computation
- Direct pairwise summation O(N²) with Plummer softening
- Barnes-Hut 2D quad-tree O(N log N) with tunable opening angle θ

### Test Cases
- Circular and elliptical 2-body Keplerian orbits
- Chenciner-Montgomery figure-8 three-body orbit
- Inner solar system (Sun + Mercury, Venus, Earth, Mars)
- Random N-body cluster evolution

## Key Results

- **Energy conservation:** Verlet/Leapfrog achieve |ΔE/E₀| ~ 10⁻⁸ over 10k steps vs Euler's 0.58 (10⁸× improvement)
- **Scaling:** Direct summation confirmed O(N²) (slope=2.013, R²=1.000); Barnes-Hut O(N^1.6) with 13× speedup at N=500
- **Figure-8 orbit:** Position error 1.8×10⁻⁵ after 1 period, energy error 4.2×10⁻¹⁴
- **Solar system:** All planet positions within ~10⁻⁴ AU after 1 Earth year

## Project Structure

| File | Purpose |
|------|---------|
| `gravity_sim.py` | Core simulation: data structures, forces, integrators |
| `barnes_hut.py` | Barnes-Hut 2D quad-tree force computation |
| `test_harness.py` | Validation against analytical Keplerian orbits |
| `ANALYSIS.md` | Literature review, mathematical formulation, method comparison |
| `FINDINGS.md` | Experimental results, discussion, and conclusions |
| `sources.bib` | BibTeX bibliography (17 entries) |
| `results/` | Experimental data (JSON) |
| `figures/` | Publication-quality plots (PNG + PDF) |

## References

See `sources.bib` for the complete bibliography. Key references:

- Verlet (1967) — Velocity Verlet algorithm
- Barnes & Hut (1986) — Hierarchical O(N log N) force calculation
- Yoshida (1990) — Higher-order symplectic integrators
- Hairer, Lubich & Wanner (2006) — Geometric numerical integration
- Dehnen & Read (2011) — N-body simulations of gravitational dynamics
- Chenciner & Montgomery (2000) — Figure-8 three-body orbit

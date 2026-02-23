"""Baseline benchmarks on canonical test problems.

Runs:
  (a) Two-body circular orbit for 100 periods with Euler and leapfrog at dt=0.001
  (b) Three-body figure-eight (Chenciner & Montgomery 2000) for 10 periods

Records results to results/baseline_benchmarks.json.
"""

import json
import math
import os
import time

from src.vector import Vec2
from src.body import Body
from src.force import direct_gravity
from src.integrators import euler_step, leapfrog_step
from src.simulation import Simulation


def two_body_circular_orbit(integrator, integrator_name, dt=0.001, n_periods=100):
    """Run a two-body circular orbit benchmark."""
    # Two equal masses in circular orbit about center of mass
    # m1 = m2 = 0.5, total M = 1, G = 1
    # Separation = 2 (each at r=1 from center)
    # v_circular = sqrt(G*M / (4*a)) = sqrt(1/4) = 0.5
    m = 0.5
    r = 1.0
    v = 0.5
    bodies = [
        Body(m, Vec2(r, 0), Vec2(0, v)),
        Body(m, Vec2(-r, 0), Vec2(0, -v)),
    ]

    # Period T = 2*pi*sqrt(a^3/(G*M)) where a = separation/2 = r for equal mass
    # Wait, for two equal masses: T = 2*pi / omega, omega = v/r
    # T = 2*pi * r / v = 2*pi * 1 / 0.5 = 4*pi
    # Actually: reduced mass problem. a = separation = 2r = 2.
    # T = 2*pi*sqrt(a^3/(G*M)) = 2*pi*sqrt(8/1) = 2*pi*2*sqrt(2) ~ 17.77
    # Hmm, let me recalculate. For two bodies:
    # v = sqrt(G * m_other / (4*r)) where r = distance from CoM = half separation
    # Actually for circular orbit: v^2/r = G*m_other/(2r)^2
    # v^2 = G*m_other*r/(2r)^2 = G*m_other/(4r)
    # v = sqrt(G*0.5/(4*1)) = sqrt(0.125) = 0.3536...
    # Let me use a simpler setup.

    # Simpler: m1=1 (stationary), m2=epsilon (test particle) at r=1
    # v = sqrt(G*m1/r) = 1, T = 2*pi
    m1, m2 = 1.0, 1e-6
    r = 1.0
    v_circ = math.sqrt(1.0 / r)  # G=1, M=m1~1
    bodies = [
        Body(m1, Vec2(0, 0), Vec2(0, 0)),
        Body(m2, Vec2(r, 0), Vec2(0, v_circ)),
    ]
    period = 2 * math.pi

    total_time = period * n_periods
    sim = Simulation(bodies, integrator, direct_gravity, dt=dt,
                     total_time=total_time,
                     force_kwargs={'G': 1.0, 'softening': 0.0})

    t0 = time.time()
    sim.run()
    wall_time = time.time() - t0

    # Compute energy error at each period
    steps_per_period = int(period / dt)
    energy_errors_per_period = []
    E0 = sim.energies[0][2]
    for p in range(1, n_periods + 1):
        idx = min(p * steps_per_period, len(sim.energies) - 1)
        E = sim.energies[idx][2]
        energy_errors_per_period.append(abs((E - E0) / abs(E0)))

    return {
        'integrator': integrator_name,
        'dt': dt,
        'N': 2,
        'periods': n_periods,
        'final_energy_error': energy_errors_per_period[-1],
        'max_energy_error': max(energy_errors_per_period),
        'wall_time_seconds': round(wall_time, 3),
        'energy_errors_per_period': energy_errors_per_period[:10],  # first 10
    }


def figure_eight_benchmark(integrator, integrator_name, dt=0.001, n_periods=10):
    """Run the three-body figure-eight benchmark.

    Initial conditions from Chenciner & Montgomery (2000) / Simo (2000).
    """
    # Standard figure-eight ICs (Simo's values)
    # Three equal masses m=1, G=1
    # Period T ≈ 6.3259
    x1 = 0.97000436
    y1 = -0.24308753
    vx3 = -0.93240737
    vy3 = -0.86473146

    bodies = [
        Body(1.0, Vec2(x1, y1), Vec2(-vx3 / 2, -vy3 / 2)),
        Body(1.0, Vec2(-x1, -y1), Vec2(-vx3 / 2, -vy3 / 2)),
        Body(1.0, Vec2(0, 0), Vec2(vx3, vy3)),
    ]

    period = 6.3259
    total_time = period * n_periods

    sim = Simulation(bodies, integrator, direct_gravity, dt=dt,
                     total_time=total_time,
                     force_kwargs={'G': 1.0, 'softening': 0.0})

    t0 = time.time()
    sim.run()
    wall_time = time.time() - t0

    E0 = sim.energies[0][2]
    E_final = sim.energies[-1][2]
    final_error = abs((E_final - E0) / abs(E0))

    return {
        'integrator': integrator_name,
        'scenario': 'figure_eight',
        'dt': dt,
        'N': 3,
        'periods': n_periods,
        'final_energy_error': final_error,
        'wall_time_seconds': round(wall_time, 3),
    }


def test_baseline_benchmarks():
    """Run all baseline benchmarks and save results."""
    results = []

    # Two-body circular orbit
    results.append(two_body_circular_orbit(euler_step, 'euler', dt=0.001, n_periods=100))
    results.append(two_body_circular_orbit(leapfrog_step, 'leapfrog', dt=0.001, n_periods=100))

    # Figure-eight
    results.append(figure_eight_benchmark(leapfrog_step, 'leapfrog', dt=0.001, n_periods=10))

    # Save results
    os.makedirs('results', exist_ok=True)
    with open('results/baseline_benchmarks.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Verify: Euler energy error must be worse than leapfrog
    euler_err = results[0]['final_energy_error']
    lf_err = results[1]['final_energy_error']

    print(f"Euler final energy error:    {euler_err:.6e}")
    print(f"Leapfrog final energy error: {lf_err:.6e}")
    print(f"Ratio (Euler/Leapfrog):      {euler_err/max(lf_err, 1e-20):.1f}x")

    assert euler_err > lf_err, f"Euler ({euler_err}) should be worse than leapfrog ({lf_err})"

    # Figure-eight should maintain reasonable energy conservation
    fig8_err = results[2]['final_energy_error']
    print(f"Figure-eight energy error:   {fig8_err:.6e}")
    assert fig8_err < 0.01, f"Figure-eight energy error too large: {fig8_err}"

"""
Entry point for the minimal gravity simulator.

Usage:
    python -m src.main

Runs a demonstration simulation of the figure-eight three-body choreography
and a Kepler orbit benchmark, saving results and generating figures.
"""

import numpy as np
import json
import time
import os

from src.body import create_kepler_orbit, create_figure_eight
from src.integrators import run_simulation, leapfrog_kdk
from src.force import compute_accelerations
from src.diagnostics import total_energy, compute_energy_error, angular_momentum
from src.visualize import setup_style, plot_trajectories, plot_energy_error


def run_kepler_benchmark():
    """Run Kepler orbit benchmark comparing Euler and Leapfrog."""
    print("=" * 60)
    print("Kepler Orbit Benchmark")
    print("=" * 60)

    G = 1.0
    bodies = create_kepler_orbit(M_central=1.0, m_orbiter=1e-6, a=1.0, e=0.0, G=G)
    masses = np.array([b.mass for b in bodies])
    pos = np.array([b.pos for b in bodies])
    vel = np.array([b.vel for b in bodies])

    E0 = total_energy(masses, pos, vel, G=G)
    dt = 0.01
    n_steps = 5000

    print(f"Initial energy: {E0:.10e}")
    print(f"Running {n_steps} steps with dt={dt}...")

    # Leapfrog simulation
    result = run_simulation(masses, pos, vel, dt=dt, n_steps=n_steps,
                            integrator='leapfrog', G=G, store_every=10)

    E_final = total_energy(masses, result['positions'][-1], result['velocities'][-1], G=G)
    err = compute_energy_error(E_final, E0)
    print(f"Leapfrog final energy error: {err:.6e}")
    print(f"Orbit trajectory saved.")

    plot_trajectories(result, filename='figures/kepler_demo.png',
                      title='Kepler Orbit (Leapfrog Integrator)')

    return result


def run_figure_eight():
    """Run figure-eight three-body choreography."""
    print()
    print("=" * 60)
    print("Figure-Eight Three-Body Choreography")
    print("=" * 60)

    G = 1.0
    bodies = create_figure_eight(G=G)
    masses = np.array([b.mass for b in bodies])
    pos = np.array([b.pos for b in bodies])
    vel = np.array([b.vel for b in bodies])

    E0 = total_energy(masses, pos, vel, G=G)
    dt = 0.001
    T_period = 6.3259
    n_steps = int(3 * T_period / dt)

    print(f"Initial energy: {E0:.10e}")
    print(f"Running {n_steps} steps for 3 periods...")

    result = run_simulation(masses, pos, vel, dt=dt, n_steps=n_steps,
                            integrator='leapfrog', G=G, store_every=10)

    E_final = total_energy(masses, result['positions'][-1], result['velocities'][-1], G=G)
    err = compute_energy_error(E_final, E0)
    print(f"Final energy error: {err:.6e}")

    plot_trajectories(result, filename='figures/figure_eight_main.png',
                      title='Figure-Eight Three-Body Choreography')

    # Compute energy error history
    times_e = []
    errors_e = []
    for i, t in enumerate(result['times']):
        E = total_energy(masses, result['positions'][i], result['velocities'][i], G=G)
        times_e.append(t / T_period)
        errors_e.append(compute_energy_error(E, E0))

    plot_energy_error([times_e], [errors_e], labels=['Leapfrog'],
                      filename='figures/figure_eight_energy.png',
                      title='Figure-Eight Energy Conservation')

    return result


if __name__ == '__main__':
    os.makedirs('figures', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    start = time.time()
    run_kepler_benchmark()
    run_figure_eight()
    elapsed = time.time() - start

    print()
    print("=" * 60)
    print(f"Complete! Total time: {elapsed:.1f}s")
    print("Figures saved to figures/")
    print("=" * 60)

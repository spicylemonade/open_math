"""
Test harness for validating N-body simulation against known analytical
solutions (circular Keplerian orbit).

Runs one full orbital period with Forward Euler and records position
error and energy error. Results saved to results/ as JSON.
"""

import json
import numpy as np
from gravity_sim import (
    init_circular_binary, total_energy, run_simulation
)


def run_orbit_test(integrator='euler', dt=0.001, softening=1e-10):
    """
    Run a circular 2-body orbit for exactly 1 orbital period.

    Returns dict with position_error, energy_error, and trace.
    """
    state, T = init_circular_binary(m1=1.0, m2=1.0, a=1.0)

    # Record initial positions for comparison
    pos_initial = state['positions'].copy()
    E0 = total_energy(state, softening=softening)

    # Number of steps to cover one period
    n_steps = int(round(T / dt))

    state_final, energy_trace = run_simulation(
        state, dt=dt, n_steps=n_steps, integrator=integrator,
        softening=softening, record_energy_every=max(1, n_steps // 100)
    )

    E_final = total_energy(state_final, softening=softening)

    # Position error: distance from expected return position
    pos_error_0 = np.linalg.norm(state_final['positions'][0] - pos_initial[0])
    pos_error_1 = np.linalg.norm(state_final['positions'][1] - pos_initial[1])
    pos_error = max(pos_error_0, pos_error_1)

    # Relative energy error
    energy_error = abs((E_final - E0) / E0)

    return {
        'integrator': integrator,
        'dt': dt,
        'n_steps': n_steps,
        'orbital_period': T,
        'position_error': pos_error,
        'energy_error': energy_error,
        'E0': E0,
        'E_final': E_final,
        'energy_trace': [(s, float(e)) for s, e in energy_trace],
    }


def main():
    print("=" * 60)
    print("Test Harness: Circular 2-body Keplerian orbit validation")
    print("=" * 60)

    # Run with Forward Euler baseline
    result = run_orbit_test(integrator='euler', dt=0.001, softening=1e-10)

    print(f"\nIntegrator: {result['integrator']}")
    print(f"dt = {result['dt']}, n_steps = {result['n_steps']}")
    print(f"Orbital period T = {result['orbital_period']:.6f}")
    print(f"Position error after 1 orbit: {result['position_error']:.6e}")
    print(f"Relative energy error |dE/E0|: {result['energy_error']:.6e}")
    print(f"E0 = {result['E0']:.10f}, E_final = {result['E_final']:.10f}")

    # Save results
    output = {
        'test': 'circular_binary_1_orbit',
        'euler_baseline': {
            'dt': result['dt'],
            'n_steps': result['n_steps'],
            'orbital_period': result['orbital_period'],
            'position_error': result['position_error'],
            'energy_error': result['energy_error'],
            'E0': result['E0'],
            'E_final': result['E_final'],
        }
    }

    with open('results/euler_baseline.json', 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to results/euler_baseline.json")


if __name__ == '__main__':
    main()

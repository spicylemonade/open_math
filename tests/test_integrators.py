"""Tests for numerical integrators."""

import numpy as np
import pytest
from src.body import create_kepler_orbit, bodies_to_arrays
from src.integrators import forward_euler, leapfrog_kdk, velocity_verlet
from src.diagnostics import total_energy


class TestForwardEuler:
    def test_single_step_correctness(self):
        """Verify one Euler step matches hand calculation."""
        masses = np.array([1.0, 1.0])
        positions = np.array([[0.0, 0.0], [1.0, 0.0]])
        velocities = np.array([[0.0, 0.0], [0.0, 1.0]])
        dt = 0.1

        new_pos, new_vel = forward_euler(masses, positions, velocities, dt, G=1.0)

        # a[0] = G * m[1] / r^2 * rhat = 1 * [1,0] = [1, 0]
        # a[1] = G * m[0] / r^2 * (-rhat) = [-1, 0]
        expected_pos0 = np.array([0.0, 0.0])  # v=0, so no movement
        expected_vel0 = np.array([0.1, 0.0])   # a = [1,0], dt=0.1

        np.testing.assert_allclose(new_pos[0], expected_pos0, atol=1e-14)
        np.testing.assert_allclose(new_vel[0], expected_vel0, atol=1e-14)

    def test_energy_drift_kepler(self):
        """Forward Euler should show >1% energy drift over 1 orbit period."""
        bodies = create_kepler_orbit(M_central=1.0, m_orbiter=1e-6, a=1.0, e=0.0, G=1.0)
        masses, pos, vel, _ = (
            np.array([b.mass for b in bodies]),
            np.array([b.pos for b in bodies]),
            np.array([b.vel for b in bodies]),
            None,
        )

        E0 = total_energy(masses, pos, vel, G=1.0)
        dt = 0.001
        # 1 orbital period = 2*pi for a=1, M=1, G=1
        n_steps = int(2 * np.pi / dt)

        for _ in range(n_steps):
            pos, vel = forward_euler(masses, pos, vel, dt, G=1.0)

        E_final = total_energy(masses, pos, vel, G=1.0)
        rel_error = abs((E_final - E0) / E0)
        assert rel_error > 0.01, f"Expected >1% drift, got {rel_error:.4e}"


class TestLeapfrog:
    def test_energy_conservation_circular(self):
        """Leapfrog should conserve energy to < 1e-6 over 10 orbits."""
        bodies = create_kepler_orbit(M_central=1.0, m_orbiter=1e-6, a=1.0, e=0.0, G=1.0)
        masses = np.array([b.mass for b in bodies])
        pos = np.array([b.pos for b in bodies])
        vel = np.array([b.vel for b in bodies])

        E0 = total_energy(masses, pos, vel, G=1.0)
        dt = 0.001
        n_steps = int(10 * 2 * np.pi / dt)

        from src.force import compute_accelerations
        acc, _ = compute_accelerations(masses, pos, G=1.0)

        for _ in range(n_steps):
            pos, vel, acc = leapfrog_kdk(masses, pos, vel, dt, G=1.0, acc_prev=acc)

        E_final = total_energy(masses, pos, vel, G=1.0)
        rel_error = abs((E_final - E0) / E0)
        assert rel_error < 1e-6, f"Expected <1e-6 drift, got {rel_error:.4e}"


class TestVelocityVerlet:
    def test_matches_leapfrog(self):
        """Velocity Verlet and Leapfrog should produce identical results."""
        bodies = create_kepler_orbit(M_central=1.0, m_orbiter=1e-6, a=1.0, e=0.0, G=1.0)
        masses = np.array([b.mass for b in bodies])
        pos_lf = np.array([b.pos for b in bodies])
        vel_lf = np.array([b.vel for b in bodies])
        pos_vv = pos_lf.copy()
        vel_vv = vel_lf.copy()

        from src.force import compute_accelerations
        acc_lf, _ = compute_accelerations(masses, pos_lf, G=1.0)
        acc_vv = acc_lf.copy()

        dt = 0.01
        for _ in range(1000):
            pos_lf, vel_lf, acc_lf = leapfrog_kdk(masses, pos_lf, vel_lf, dt, G=1.0, acc_prev=acc_lf)
            pos_vv, vel_vv, acc_vv = velocity_verlet(masses, pos_vv, vel_vv, dt, G=1.0, acc_prev=acc_vv)

        np.testing.assert_allclose(pos_lf, pos_vv, atol=1e-14)
        np.testing.assert_allclose(vel_lf, vel_vv, atol=1e-14)

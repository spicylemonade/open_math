"""Unit tests for sim.integrators module."""

import numpy as np
import pytest
from sim.body import kepler_circular
from sim.forces import direct_summation
from sim.integrators import euler, leapfrog_kdk, velocity_verlet


class TestForwardEuler:
    def test_position_update(self):
        """Test that Euler correctly updates position: x_new = x + v*dt."""
        masses = np.array([1.0])
        pos = np.array([[0.0, 0.0]])
        vel = np.array([[1.0, 0.0]])
        dt = 0.1
        # Use zero-force function to isolate position update
        zero_force = lambda m, p, **kw: np.zeros_like(p)
        new_pos, new_vel = euler(masses, pos, vel, dt, force_func=zero_force)
        np.testing.assert_allclose(new_pos, [[0.1, 0.0]])
        np.testing.assert_allclose(new_vel, [[1.0, 0.0]])

    def test_velocity_update(self):
        """Test that Euler correctly updates velocity: v_new = v + a*dt."""
        masses = np.array([1.0, 1.0])
        pos = np.array([[0.0, 0.0], [1.0, 0.0]])
        vel = np.array([[0.0, 0.0], [0.0, 0.0]])
        dt = 0.01
        new_pos, new_vel = euler(masses, pos, vel, dt)
        # Particle 0 should gain positive x-velocity (attracted toward particle 1)
        assert new_vel[0, 0] > 0

    def test_energy_drift_on_kepler(self):
        """Verify that Euler shows energy drift on a circular orbit."""
        masses, pos, vel = kepler_circular()
        dt = 0.01
        # Run for ~1 orbit (2*pi / dt steps)
        n_steps = int(2 * np.pi / dt)
        for _ in range(n_steps):
            pos, vel = euler(masses, pos, vel, dt)
        # Compute energy
        T = 0.5 * np.sum(masses[:, None] * vel**2)
        dr = pos[1] - pos[0]
        r = np.linalg.norm(dr)
        V = -masses[0] * masses[1] / r
        E_final = T + V
        # Initial energy for circular orbit
        E_init = -0.25  # -G*m1*m2/(2*a) for m1=m2=0.5, a=1
        # Euler should show significant drift
        rel_error = abs((E_final - E_init) / E_init)
        assert rel_error > 1e-4, f"Expected energy drift, got relative error {rel_error}"


class TestLeapfrogKDK:
    def test_bounded_energy_error(self):
        """Leapfrog should have bounded (non-drifting) energy error over 10k steps."""
        from sim.diagnostics import total_energy
        masses, pos, vel = kepler_circular()
        E0 = total_energy(masses, pos, vel)
        dt = 0.01
        n_steps = 10000
        acc = None
        max_err = 0.0
        for _ in range(n_steps):
            pos, vel, acc = leapfrog_kdk(masses, pos, vel, dt, acc_prev=acc)
            E = total_energy(masses, pos, vel)
            rel_err = abs((E - E0) / E0)
            if rel_err > max_err:
                max_err = rel_err
        # Energy error should remain very small and bounded
        assert max_err < 1e-5, f"Expected bounded error < 1e-5, got {max_err:.2e}"

    def test_much_better_than_euler(self):
        """Leapfrog energy error should be orders of magnitude better than Euler."""
        from sim.diagnostics import total_energy
        masses, pos, vel = kepler_circular()
        E0 = total_energy(masses, pos, vel)
        dt = 0.01
        n_steps = 1000

        # Run Euler
        p_e, v_e = pos.copy(), vel.copy()
        for _ in range(n_steps):
            p_e, v_e = euler(masses, p_e, v_e, dt)
        euler_err = abs((total_energy(masses, p_e, v_e) - E0) / E0)

        # Run Leapfrog
        p_l, v_l = pos.copy(), vel.copy()
        acc = None
        max_lf_err = 0.0
        for _ in range(n_steps):
            p_l, v_l, acc = leapfrog_kdk(masses, p_l, v_l, dt, acc_prev=acc)
            err = abs((total_energy(masses, p_l, v_l) - E0) / E0)
            if err > max_lf_err:
                max_lf_err = err

        # Leapfrog should be at least 1000x better
        assert max_lf_err < euler_err / 1000, (
            f"Expected leapfrog >> Euler: LF={max_lf_err:.2e}, Euler={euler_err:.2e}"
        )

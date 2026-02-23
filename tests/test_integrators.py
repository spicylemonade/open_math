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

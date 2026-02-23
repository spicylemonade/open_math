"""Unit tests for the Simulation class."""

import math
from src.vector import Vec2
from src.body import Body
from src.force import direct_gravity
from src.integrators import leapfrog_step, euler_step
from src.simulation import Simulation


def _circular_orbit_bodies():
    """Create a two-body circular orbit configuration."""
    m = 0.5
    r = 1.0
    v = math.sqrt(1.0 / (4.0 * r))  # G=1, M=1, circular orbit
    return [
        Body(m, Vec2(r, 0), Vec2(0, v)),
        Body(m, Vec2(-r, 0), Vec2(0, -v)),
    ]


def test_simulation_runs():
    """Simulation runs without error."""
    bodies = _circular_orbit_bodies()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, dt=0.01, total_time=1.0,
                     force_kwargs={'G': 1.0, 'softening': 0.0})
    sim.run()
    assert len(sim.times) > 1


def test_energy_computed():
    """Simulation records energy at each step."""
    bodies = _circular_orbit_bodies()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, dt=0.01, total_time=0.1,
                     force_kwargs={'G': 1.0, 'softening': 0.0})
    sim.run()
    assert len(sim.energies) == len(sim.times)
    # Energy should be non-positive (bound or marginally bound system)
    assert sim.energies[0][2] <= 0


def test_kinetic_energy_value():
    """KE should match analytical value for the initial state."""
    bodies = _circular_orbit_bodies()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, dt=0.01, total_time=0.0,
                     force_kwargs={'G': 1.0, 'softening': 0.0})
    sim.run()
    ke = sim.energies[0][0]
    # KE = 2 * 0.5 * m * v^2 = m * v^2
    m = 0.5
    v = math.sqrt(1.0 / 4.0)
    expected = 2 * 0.5 * m * v * v
    assert abs(ke - expected) < 1e-10


def test_potential_energy_value():
    """PE should match analytical -G*m1*m2/r for the initial state."""
    bodies = _circular_orbit_bodies()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, dt=0.01, total_time=0.0,
                     force_kwargs={'G': 1.0, 'softening': 0.0})
    sim.run()
    pe = sim.energies[0][1]
    # PE = -G * m1 * m2 / r = -1.0 * 0.5 * 0.5 / 2.0 = -0.125
    assert abs(pe - (-0.125)) < 1e-10


def test_momentum_conservation():
    """Total linear momentum should be conserved (initially zero for symmetric config)."""
    bodies = _circular_orbit_bodies()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, dt=0.001, total_time=1.0,
                     force_kwargs={'G': 1.0, 'softening': 0.0})
    sim.run()
    for p in sim.momenta:
        assert abs(p.x) < 1e-10
        assert abs(p.y) < 1e-10


def test_angular_momentum_conservation():
    """Angular momentum should be approximately conserved."""
    bodies = _circular_orbit_bodies()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, dt=0.001, total_time=1.0,
                     force_kwargs={'G': 1.0, 'softening': 0.0})
    sim.run()
    L0 = sim.angular_momenta[0]
    for L in sim.angular_momenta:
        assert abs(L - L0) < 1e-6


def test_energy_conservation_leapfrog():
    """Leapfrog should approximately conserve energy over a short run."""
    bodies = _circular_orbit_bodies()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, dt=0.001, total_time=6.28,
                     force_kwargs={'G': 1.0, 'softening': 0.0})
    sim.run()
    errors = sim.relative_energy_error()
    assert max(errors) < 1e-4


def test_history_recorded():
    """Position and velocity history should be recorded."""
    bodies = _circular_orbit_bodies()
    sim = Simulation(bodies, leapfrog_step, direct_gravity, dt=0.1, total_time=1.0,
                     force_kwargs={'G': 1.0, 'softening': 0.0})
    sim.run()
    assert len(sim.history_pos) == len(sim.times)
    assert len(sim.history_pos[0]) == 2  # two bodies

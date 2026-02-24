"""
Particle/Body data structures and initialization routines for N-body simulation.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List


@dataclass
class Body:
    """A gravitational body with mass, position, velocity, and acceleration."""
    mass: float
    pos: np.ndarray  # 2D or 3D position vector
    vel: np.ndarray  # 2D or 3D velocity vector
    acc: np.ndarray = field(default=None)

    def __post_init__(self):
        self.pos = np.asarray(self.pos, dtype=np.float64)
        self.vel = np.asarray(self.vel, dtype=np.float64)
        if self.acc is None:
            self.acc = np.zeros_like(self.pos)
        else:
            self.acc = np.asarray(self.acc, dtype=np.float64)


def create_kepler_orbit(M_central=1.0, m_orbiter=1e-6, a=1.0, e=0.0, G=1.0):
    """
    Create a 2-body Kepler system (central mass + orbiter) in 2D.

    Parameters
    ----------
    M_central : float - Mass of the central body
    m_orbiter : float - Mass of the orbiting body
    a : float - Semi-major axis
    e : float - Eccentricity (0 = circular)
    G : float - Gravitational constant

    Returns
    -------
    list of Body - [central_body, orbiting_body]
    """
    # Start orbiter at pericenter
    r_peri = a * (1 - e)
    # Vis-viva equation for velocity at pericenter
    M_total = M_central + m_orbiter
    v_peri = np.sqrt(G * M_total * (2.0 / r_peri - 1.0 / a))

    # Center of mass correction
    mu = m_orbiter / M_total  # mass ratio

    central = Body(
        mass=M_central,
        pos=np.array([-mu * r_peri, 0.0]),
        vel=np.array([0.0, -mu * v_peri]),
    )
    orbiter = Body(
        mass=m_orbiter,
        pos=np.array([(1 - mu) * r_peri, 0.0]),
        vel=np.array([0.0, (1 - mu) * v_peri]),
    )
    return [central, orbiter]


def create_circular_orbit_simple(G=1.0):
    """
    Create a simple Sun-Earth-like circular Kepler orbit in normalized units.
    Central mass M=1 at origin, orbiter mass m=1e-6 at distance 1 with v_c = 1.

    Returns
    -------
    list of Body
    """
    return create_kepler_orbit(M_central=1.0, m_orbiter=1e-6, a=1.0, e=0.0, G=G)


def create_random_bodies(n, seed=42, box_size=10.0, max_vel=1.0, mass_range=(0.1, 10.0)):
    """
    Create N random bodies in 2D within a box.

    Parameters
    ----------
    n : int - Number of bodies
    seed : int - Random seed for reproducibility
    box_size : float - Half-width of the box
    max_vel : float - Maximum initial velocity component
    mass_range : tuple - (min_mass, max_mass)

    Returns
    -------
    list of Body
    """
    rng = np.random.default_rng(seed)
    bodies = []
    for _ in range(n):
        mass = rng.uniform(*mass_range)
        pos = rng.uniform(-box_size, box_size, size=2)
        vel = rng.uniform(-max_vel, max_vel, size=2)
        bodies.append(Body(mass=mass, pos=pos, vel=vel))
    return bodies


def create_figure_eight(G=1.0):
    """
    Create the Chenciner-Montgomery figure-eight three-body choreography.
    Uses initial conditions from Simó.

    Returns
    -------
    list of Body - Three equal-mass bodies
    """
    m = 1.0
    b1 = Body(
        mass=m,
        pos=np.array([-0.97000436, 0.24308753]),
        vel=np.array([0.4662036850, 0.4323657300]),
    )
    b2 = Body(
        mass=m,
        pos=np.array([0.97000436, -0.24308753]),
        vel=np.array([0.4662036850, 0.4323657300]),
    )
    b3 = Body(
        mass=m,
        pos=np.array([0.0, 0.0]),
        vel=np.array([-0.93240737, -0.86473146]),
    )
    return [b1, b2, b3]


def bodies_to_arrays(bodies):
    """Convert list of Body objects to arrays for vectorized computation."""
    n = len(bodies)
    masses = np.array([b.mass for b in bodies])
    positions = np.array([b.pos for b in bodies])
    velocities = np.array([b.vel for b in bodies])
    accelerations = np.array([b.acc for b in bodies])
    return masses, positions, velocities, accelerations


def arrays_to_bodies(masses, positions, velocities, accelerations=None):
    """Convert arrays back to list of Body objects."""
    n = len(masses)
    if accelerations is None:
        accelerations = np.zeros_like(positions)
    return [
        Body(mass=masses[i], pos=positions[i].copy(), vel=velocities[i].copy(), acc=accelerations[i].copy())
        for i in range(n)
    ]

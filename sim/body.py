"""Particle data structures and initialization routines for N-body simulation.

Uses NumPy arrays for vectorized computation. The system state is represented as:
  - masses: shape (N,)
  - positions: shape (N, dim)
  - velocities: shape (N, dim)

where dim is the spatial dimension (2 or 3) and N is the number of particles.
"""

import numpy as np


def kepler_circular(m1=0.5, m2=0.5, separation=1.0, dim=2):
    """Initialize a two-body circular Kepler orbit in the center-of-mass frame.

    Parameters
    ----------
    m1, m2 : float
        Masses of the two bodies. Default 0.5 each (total mass = 1).
    separation : float
        Distance between the two bodies. Default 1.0.
    dim : int
        Spatial dimension (2 or 3). Default 2.

    Returns
    -------
    masses : ndarray, shape (2,)
    positions : ndarray, shape (2, dim)
    velocities : ndarray, shape (2, dim)
    """
    M = m1 + m2
    # G = 1 in natural units
    # Positions in center-of-mass frame along x-axis
    r1 = -m2 / M * separation
    r2 = m1 / M * separation

    positions = np.zeros((2, dim))
    positions[0, 0] = r1
    positions[1, 0] = r2

    # Circular orbital velocity: v = sqrt(G * M / r) scaled to CoM frame
    v_orb = np.sqrt(M / separation)
    v1 = -m2 / M * v_orb
    v2 = m1 / M * v_orb

    velocities = np.zeros((2, dim))
    velocities[0, 1] = v1
    velocities[1, 1] = v2

    masses = np.array([m1, m2])
    return masses, positions, velocities


def kepler_elliptical(m1=0.5, m2=0.5, semi_major=1.0, eccentricity=0.5, dim=2):
    """Initialize a two-body elliptical Kepler orbit at pericenter.

    Parameters
    ----------
    m1, m2 : float
        Masses of the two bodies.
    semi_major : float
        Semi-major axis of the relative orbit.
    eccentricity : float
        Orbital eccentricity (0 <= e < 1).
    dim : int
        Spatial dimension (2 or 3).

    Returns
    -------
    masses : ndarray, shape (2,)
    positions : ndarray, shape (2, dim)
    velocities : ndarray, shape (2, dim)
    """
    M = m1 + m2
    r_peri = semi_major * (1 - eccentricity)

    # Positions at pericenter along x-axis
    r1 = -m2 / M * r_peri
    r2 = m1 / M * r_peri

    positions = np.zeros((2, dim))
    positions[0, 0] = r1
    positions[1, 0] = r2

    # Velocity at pericenter (vis-viva): v^2 = GM(2/r - 1/a)
    v_peri = np.sqrt(M * (2.0 / r_peri - 1.0 / semi_major))
    v1 = -m2 / M * v_peri
    v2 = m1 / M * v_peri

    velocities = np.zeros((2, dim))
    velocities[0, 1] = v1
    velocities[1, 1] = v2

    masses = np.array([m1, m2])
    return masses, positions, velocities


def random_system(n, dim=2, seed=42, mass_range=(0.1, 1.0),
                  pos_range=(-1.0, 1.0), vel_scale=0.1):
    """Initialize a random N-body system.

    Parameters
    ----------
    n : int
        Number of particles.
    dim : int
        Spatial dimension (2 or 3).
    seed : int
        Random seed for reproducibility.
    mass_range : tuple
        (min, max) mass range for uniform distribution.
    pos_range : tuple
        (min, max) position range for uniform distribution.
    vel_scale : float
        Standard deviation of velocity components (Gaussian).

    Returns
    -------
    masses : ndarray, shape (n,)
    positions : ndarray, shape (n, dim)
    velocities : ndarray, shape (n, dim)
    """
    rng = np.random.default_rng(seed)
    masses = rng.uniform(mass_range[0], mass_range[1], size=n)
    positions = rng.uniform(pos_range[0], pos_range[1], size=(n, dim))
    velocities = rng.normal(0, vel_scale, size=(n, dim))
    return masses, positions, velocities

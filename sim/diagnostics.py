"""Conservation diagnostics for N-body simulation.

Computes total kinetic energy, gravitational potential energy,
linear momentum, and angular momentum. Uses G = 1.
"""

import numpy as np


def kinetic_energy(masses, velocities):
    """Compute total kinetic energy T = sum(0.5 * m_i * |v_i|^2).

    Parameters
    ----------
    masses : ndarray, shape (N,)
    velocities : ndarray, shape (N, dim)

    Returns
    -------
    float
    """
    return 0.5 * np.sum(masses * np.sum(velocities**2, axis=1))


def potential_energy(masses, positions, softening=0.0):
    """Compute total gravitational potential energy V = -sum_{i<j} m_i*m_j / r_ij.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    softening : float
        Plummer softening length.

    Returns
    -------
    float
    """
    n = len(masses)
    eps2 = softening * softening
    V = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            dr = positions[j] - positions[i]
            r = np.sqrt(np.dot(dr, dr) + eps2)
            V -= masses[i] * masses[j] / r
    return V


def total_energy(masses, positions, velocities, softening=0.0):
    """Compute total energy E = T + V.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)
    softening : float

    Returns
    -------
    float
    """
    return kinetic_energy(masses, velocities) + potential_energy(masses, positions, softening)


def linear_momentum(masses, velocities):
    """Compute total linear momentum P = sum(m_i * v_i).

    Parameters
    ----------
    masses : ndarray, shape (N,)
    velocities : ndarray, shape (N, dim)

    Returns
    -------
    ndarray, shape (dim,)
    """
    return np.sum(masses[:, None] * velocities, axis=0)


def angular_momentum(masses, positions, velocities):
    """Compute total angular momentum L = sum(m_i * r_i x v_i).

    For 2D, returns scalar (z-component). For 3D, returns 3-vector.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    velocities : ndarray, shape (N, dim)

    Returns
    -------
    float or ndarray
    """
    dim = positions.shape[1]
    if dim == 2:
        # L_z = sum(m_i * (x_i * vy_i - y_i * vx_i))
        cross = positions[:, 0] * velocities[:, 1] - positions[:, 1] * velocities[:, 0]
        return np.sum(masses * cross)
    else:
        # 3D cross product
        L = np.zeros(3)
        for i in range(len(masses)):
            L += masses[i] * np.cross(positions[i], velocities[i])
        return L

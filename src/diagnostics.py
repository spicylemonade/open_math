"""
Conservation diagnostics for N-body simulation:
kinetic energy, potential energy, total energy, linear momentum, angular momentum.
"""

import numpy as np


def kinetic_energy(masses, velocities):
    """Compute total kinetic energy: T = 0.5 * sum(m_i * |v_i|^2)."""
    return 0.5 * np.sum(masses * np.sum(velocities ** 2, axis=1))


def potential_energy(masses, positions, G=1.0, softening=0.0):
    """Compute total gravitational potential energy: V = -G * sum_{i<j} m_i*m_j / r_ij."""
    n = len(masses)
    eps2 = softening * softening
    V = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            rij = positions[j] - positions[i]
            r = np.sqrt(np.dot(rij, rij) + eps2)
            V -= G * masses[i] * masses[j] / r
    return V


def total_energy(masses, positions, velocities, G=1.0, softening=0.0):
    """Compute total energy E = T + V."""
    T = kinetic_energy(masses, velocities)
    V = potential_energy(masses, positions, G=G, softening=softening)
    return T + V


def linear_momentum(masses, velocities):
    """Compute total linear momentum vector: P = sum(m_i * v_i)."""
    return np.sum(masses[:, np.newaxis] * velocities, axis=0)


def angular_momentum(masses, positions, velocities):
    """
    Compute total angular momentum.
    In 2D: L = sum(m_i * (x_i * vy_i - y_i * vx_i)) (scalar)
    In 3D: L = sum(m_i * (r_i x v_i)) (vector)
    """
    dim = positions.shape[1]
    if dim == 2:
        # Scalar angular momentum in 2D
        L = np.sum(masses * (positions[:, 0] * velocities[:, 1] -
                             positions[:, 1] * velocities[:, 0]))
        return L
    elif dim == 3:
        cross = np.cross(positions, velocities)
        L = np.sum(masses[:, np.newaxis] * cross, axis=0)
        return L
    else:
        raise ValueError(f"Unsupported dimension: {dim}")


def compute_energy_error(E_current, E_initial):
    """Compute relative energy error |dE/E0|."""
    if abs(E_initial) < 1e-30:
        return abs(E_current - E_initial)
    return abs((E_current - E_initial) / E_initial)

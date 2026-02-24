"""
Gravitational force computation via direct O(N^2) pairwise summation.
Supports Plummer softening for close encounters.
"""

import numpy as np


def compute_accelerations(masses, positions, G=1.0, softening=0.0):
    """
    Compute gravitational accelerations on all bodies via direct pairwise summation.
    Exploits Newton's third law: each pair computed once.

    Parameters
    ----------
    masses : ndarray, shape (N,) - Particle masses
    positions : ndarray, shape (N, dim) - Particle positions
    G : float - Gravitational constant
    softening : float - Plummer softening parameter epsilon

    Returns
    -------
    accelerations : ndarray, shape (N, dim) - Gravitational accelerations
    n_evaluations : int - Number of pairwise force evaluations
    """
    n = len(masses)
    dim = positions.shape[1]
    acc = np.zeros_like(positions)
    eps2 = softening * softening
    n_evals = 0

    for i in range(n):
        for j in range(i + 1, n):
            rij = positions[j] - positions[i]
            r2 = np.dot(rij, rij) + eps2
            r_inv3 = r2 ** (-1.5)

            # Force on i due to j
            f = G * r_inv3 * rij
            acc[i] += masses[j] * f
            acc[j] -= masses[i] * f  # Newton's third law

            n_evals += 1

    return acc, n_evals


def compute_accelerations_vectorized(masses, positions, G=1.0, softening=0.0):
    """
    Vectorized gravitational acceleration computation.
    More efficient for larger N but uses O(N^2) memory.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    G : float
    softening : float

    Returns
    -------
    accelerations : ndarray, shape (N, dim)
    """
    n = len(masses)
    eps2 = softening * softening

    # Displacement vectors: dx[i,j] = positions[j] - positions[i]
    dx = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]  # (N, N, dim)

    # Squared distances
    r2 = np.sum(dx ** 2, axis=2) + eps2  # (N, N)
    np.fill_diagonal(r2, 1.0)  # Avoid division by zero on diagonal

    # 1/r^3
    r_inv3 = r2 ** (-1.5)
    np.fill_diagonal(r_inv3, 0.0)  # No self-interaction

    # Accelerations: a_i = G * sum_j m_j * (r_j - r_i) / |r_ij|^3
    acc = G * np.einsum('j,ijk,ij->ik', masses, dx, r_inv3)

    return acc

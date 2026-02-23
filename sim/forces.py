"""Gravitational force computation routines.

Provides direct-summation O(N^2) pairwise gravitational acceleration.
Uses G = 1 (natural units).
"""

import numpy as np


def direct_summation(masses, positions, softening=0.0):
    """Compute gravitational acceleration on each particle via direct pairwise summation.

    Parameters
    ----------
    masses : ndarray, shape (N,)
        Particle masses.
    positions : ndarray, shape (N, dim)
        Particle positions.
    softening : float
        Plummer softening length epsilon. Default 0 (no softening).

    Returns
    -------
    accelerations : ndarray, shape (N, dim)
        Gravitational acceleration on each particle.
    """
    n = len(masses)
    dim = positions.shape[1]
    acc = np.zeros_like(positions)
    eps2 = softening * softening

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dr = positions[j] - positions[i]
            r2 = np.dot(dr, dr) + eps2
            r3_inv = r2 ** (-1.5)
            acc[i] += masses[j] * dr * r3_inv

    return acc

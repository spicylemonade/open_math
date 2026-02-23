"""Gravitational force computation via direct O(N^2) pairwise summation."""

import math
from src.vector import Vec2


def direct_gravity(bodies, G=1.0, softening=0.0):
    """Compute gravitational acceleration on each body via direct pairwise summation.

    Parameters
    ----------
    bodies : list of Body
        The gravitational bodies.
    G : float
        Gravitational constant (default 1.0).
    softening : float
        Plummer softening length epsilon (default 0.0).

    Returns
    -------
    list of Vec2
        Acceleration vector for each body.
    """
    n = len(bodies)
    accelerations = [Vec2(0.0, 0.0)] * n
    eps2 = softening * softening

    for i in range(n):
        ax, ay = 0.0, 0.0
        for j in range(n):
            if i == j:
                continue
            dx = bodies[j].pos.x - bodies[i].pos.x
            dy = bodies[j].pos.y - bodies[i].pos.y
            r2 = dx * dx + dy * dy + eps2
            inv_r3 = G * bodies[j].mass / (r2 * math.sqrt(r2))
            ax += inv_r3 * dx
            ay += inv_r3 * dy
        accelerations[i] = Vec2(ax, ay)

    return accelerations

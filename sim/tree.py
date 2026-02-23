"""Barnes-Hut quadtree (2D) / octree (3D) for O(N log N) force computation.

Implements the Barnes & Hut (1986) algorithm with configurable opening angle theta.
"""

import numpy as np


class TreeNode:
    """Node in a Barnes-Hut tree (quadtree for 2D, octree for 3D).

    Attributes
    ----------
    center : ndarray, shape (dim,)
        Center of the spatial region.
    half_size : float
        Half the side length of the region.
    mass : float
        Total mass in this node.
    com : ndarray, shape (dim,)
        Center of mass of particles in this node.
    particle_idx : int or None
        Index of single particle (leaf node), or None (internal node).
    children : list of TreeNode or None
    """

    __slots__ = ['center', 'half_size', 'mass', 'com', 'particle_idx', 'children', 'dim']

    def __init__(self, center, half_size, dim):
        self.center = center
        self.half_size = half_size
        self.dim = dim
        self.mass = 0.0
        self.com = np.zeros(dim)
        self.particle_idx = None
        self.children = None


def _get_quadrant(pos, center, dim):
    """Determine which child quadrant/octant a position falls into.

    Returns an integer index 0..2^dim-1.
    """
    idx = 0
    for d in range(dim):
        if pos[d] >= center[d]:
            idx |= (1 << d)
    return idx


def _child_center(parent_center, half_size, child_idx, dim):
    """Compute the center of a child node given the parent and child index."""
    new_center = parent_center.copy()
    new_half = half_size * 0.5
    for d in range(dim):
        if child_idx & (1 << d):
            new_center[d] += new_half
        else:
            new_center[d] -= new_half
    return new_center


def build_tree(masses, positions):
    """Build a Barnes-Hut tree from particle data.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)

    Returns
    -------
    TreeNode
        Root of the tree.
    """
    n, dim = positions.shape
    n_children = 1 << dim  # 4 for 2D, 8 for 3D

    # Compute bounding box
    pos_min = positions.min(axis=0)
    pos_max = positions.max(axis=0)
    center = 0.5 * (pos_min + pos_max)
    half_size = 0.5 * np.max(pos_max - pos_min) * 1.01  # Small margin

    root = TreeNode(center, half_size, dim)

    for i in range(n):
        _insert(root, i, masses[i], positions[i], dim, n_children)

    return root


def _insert(node, idx, mass, pos, dim, n_children):
    """Insert a particle into the tree."""
    if node.mass == 0.0 and node.particle_idx is None and node.children is None:
        # Empty leaf -> store particle here
        node.mass = mass
        node.com = pos.copy()
        node.particle_idx = idx
        return

    if node.children is None:
        # Single-particle leaf -> subdivide
        node.children = [None] * n_children
        # Re-insert the existing particle
        old_idx = node.particle_idx
        old_mass = node.mass
        old_com = node.com.copy()
        node.particle_idx = None

        q = _get_quadrant(old_com, node.center, dim)
        if node.children[q] is None:
            child_c = _child_center(node.center, node.half_size, q, dim)
            node.children[q] = TreeNode(child_c, node.half_size * 0.5, dim)
        _insert(node.children[q], old_idx, old_mass, old_com, dim, n_children)

    # Insert new particle into appropriate child
    q = _get_quadrant(pos, node.center, dim)
    if node.children[q] is None:
        child_c = _child_center(node.center, node.half_size, q, dim)
        node.children[q] = TreeNode(child_c, node.half_size * 0.5, dim)
    _insert(node.children[q], idx, mass, pos, dim, n_children)

    # Update center of mass
    total_mass = node.mass + mass
    node.com = (node.com * node.mass + pos * mass) / total_mass
    node.mass = total_mass


def _compute_acceleration(node, pos, theta, softening, dim):
    """Recursively compute acceleration on a particle from a tree node."""
    if node is None or node.mass == 0.0:
        return np.zeros(dim)

    dr = node.com - pos
    r2 = np.dot(dr, dr)

    if r2 < 1e-30:
        # Same particle or co-located -> skip
        if node.particle_idx is not None:
            return np.zeros(dim)

    # Check opening criterion: s/d < theta
    s = 2.0 * node.half_size
    d = np.sqrt(r2) if r2 > 0 else 0.0

    if node.children is None or (d > 0 and s / d < theta):
        # Use this node as a pseudo-particle
        r2_soft = r2 + softening * softening
        if r2_soft < 1e-30:
            return np.zeros(dim)
        return node.mass * dr * r2_soft ** (-1.5)
    else:
        # Recurse into children
        acc = np.zeros(dim)
        for child in node.children:
            if child is not None:
                acc += _compute_acceleration(child, pos, theta, softening, dim)
        return acc


def barnes_hut(masses, positions, theta=0.5, softening=0.0):
    """Compute gravitational acceleration using Barnes-Hut tree algorithm.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, dim)
    theta : float
        Opening angle parameter. Smaller = more accurate. Default 0.5.
    softening : float
        Plummer softening length.

    Returns
    -------
    accelerations : ndarray, shape (N, dim)
    """
    n, dim = positions.shape
    tree = build_tree(masses, positions)

    acc = np.zeros_like(positions)
    for i in range(n):
        acc[i] = _compute_acceleration_exclude(tree, positions[i], i, theta, softening, dim)

    return acc


def _compute_acceleration_exclude(node, pos, exclude_idx, theta, softening, dim):
    """Compute acceleration excluding a specific particle index."""
    if node is None or node.mass == 0.0:
        return np.zeros(dim)

    # If leaf node and it's the excluded particle, skip
    if node.particle_idx == exclude_idx:
        return np.zeros(dim)

    dr = node.com - pos
    r2 = np.dot(dr, dr)
    s = 2.0 * node.half_size
    d = np.sqrt(r2) if r2 > 0 else 0.0

    if node.children is None:
        # Leaf node (not excluded)
        r2_soft = r2 + softening * softening
        if r2_soft < 1e-30:
            return np.zeros(dim)
        return node.mass * dr * r2_soft ** (-1.5)

    if d > 0 and s / d < theta:
        # Use this node as pseudo-particle
        r2_soft = r2 + softening * softening
        if r2_soft < 1e-30:
            return np.zeros(dim)
        return node.mass * dr * r2_soft ** (-1.5)
    else:
        # Recurse
        acc = np.zeros(dim)
        for child in node.children:
            if child is not None:
                acc += _compute_acceleration_exclude(child, pos, exclude_idx, theta, softening, dim)
        return acc

"""
Barnes-Hut quadtree (2D) for O(N log N) approximate gravitational force computation.

References:
    Barnes & Hut (1986), Nature 324, 446-449
"""

import numpy as np


class QuadTreeNode:
    """A node in the Barnes-Hut quadtree."""

    __slots__ = ['center', 'size', 'mass', 'com', 'children', 'body_idx']

    def __init__(self, center, size):
        self.center = center      # Center of the cell (2D)
        self.size = size          # Half-width of the cell
        self.mass = 0.0           # Total mass in this node
        self.com = np.zeros(2)    # Center of mass
        self.children = [None, None, None, None]  # NW, NE, SW, SE
        self.body_idx = -1        # Index of body if leaf, -1 otherwise


def _quadrant(pos, center):
    """Determine which quadrant a position falls in relative to center."""
    if pos[0] <= center[0]:
        return 0 if pos[1] > center[1] else 2  # NW or SW
    else:
        return 1 if pos[1] > center[1] else 3  # NE or SE


def _child_center(parent_center, parent_size, quadrant):
    """Compute center of a child quadrant."""
    half = parent_size / 2.0
    offsets = [
        np.array([-half, half]),   # NW
        np.array([half, half]),    # NE
        np.array([-half, -half]),  # SW
        np.array([half, -half]),   # SE
    ]
    return parent_center + offsets[quadrant]


def build_tree(masses, positions):
    """
    Build a Barnes-Hut quadtree from particle positions.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, 2)

    Returns
    -------
    root : QuadTreeNode
    """
    n = len(masses)
    if n == 0:
        return None

    # Determine bounding box
    min_pos = positions.min(axis=0)
    max_pos = positions.max(axis=0)
    center = (min_pos + max_pos) / 2.0
    size = max(max_pos[0] - min_pos[0], max_pos[1] - min_pos[1]) / 2.0 * 1.01  # slight padding

    root = QuadTreeNode(center, size)

    for i in range(n):
        _insert(root, i, masses[i], positions[i])

    return root


def _insert(node, idx, mass, pos):
    """Insert a body into the quadtree."""
    if node.mass == 0.0 and node.body_idx == -1:
        # Empty node: just store the body
        node.mass = mass
        node.com = pos.copy()
        node.body_idx = idx
        return

    if node.body_idx != -1:
        # This is a leaf with one body; need to split
        old_idx = node.body_idx
        old_mass = node.mass
        old_com = node.com.copy()
        node.body_idx = -1

        # Re-insert the old body
        q = _quadrant(old_com, node.center)
        if node.children[q] is None:
            node.children[q] = QuadTreeNode(
                _child_center(node.center, node.size, q),
                node.size / 2.0
            )
        _insert(node.children[q], old_idx, old_mass, old_com)

    # Insert the new body
    q = _quadrant(pos, node.center)
    if node.children[q] is None:
        node.children[q] = QuadTreeNode(
            _child_center(node.center, node.size, q),
            node.size / 2.0
        )
    _insert(node.children[q], idx, mass, pos)

    # Update mass and center of mass
    total_mass = node.mass + mass
    node.com = (node.com * node.mass + pos * mass) / total_mass
    node.mass = total_mass


def compute_acceleration_bh(node, pos, G=1.0, theta=0.5, softening=0.0):
    """
    Compute gravitational acceleration on a body at position pos using the tree.

    Parameters
    ----------
    node : QuadTreeNode
    pos : ndarray, shape (2,)
    G : float
    theta : float - Opening angle parameter
    softening : float - Plummer softening

    Returns
    -------
    acc : ndarray, shape (2,) - Gravitational acceleration
    """
    if node is None or node.mass == 0.0:
        return np.zeros(2)

    dr = node.com - pos
    r2 = np.dot(dr, dr)

    if r2 < 1e-30:
        # Same position (self-interaction), skip
        if node.body_idx != -1:
            return np.zeros(2)

    # Check opening criterion: s/d < theta
    if node.body_idx != -1:
        # Leaf node — compute direct force
        if r2 < 1e-30:
            return np.zeros(2)
        eps2 = softening * softening
        r2_soft = r2 + eps2
        r_inv3 = r2_soft ** (-1.5)
        return G * node.mass * r_inv3 * dr

    # Internal node — check opening angle
    s = 2.0 * node.size
    d2 = r2
    if d2 > 0 and (s * s / d2) < (theta * theta):
        # Use monopole approximation
        eps2 = softening * softening
        r2_soft = r2 + eps2
        r_inv3 = r2_soft ** (-1.5)
        return G * node.mass * r_inv3 * dr

    # Open the node — recurse into children
    acc = np.zeros(2)
    for child in node.children:
        if child is not None:
            acc += compute_acceleration_bh(child, pos, G=G, theta=theta, softening=softening)
    return acc


def compute_accelerations_bh(masses, positions, G=1.0, theta=0.5, softening=0.0):
    """
    Compute gravitational accelerations on all bodies using Barnes-Hut algorithm.

    Parameters
    ----------
    masses : ndarray, shape (N,)
    positions : ndarray, shape (N, 2)
    G : float
    theta : float - Opening angle (0 = exact, higher = faster but less accurate)
    softening : float - Plummer softening parameter

    Returns
    -------
    accelerations : ndarray, shape (N, 2)
    """
    n = len(masses)
    tree = build_tree(masses, positions)
    acc = np.zeros_like(positions)

    for i in range(n):
        acc[i] = compute_acceleration_bh(tree, positions[i], G=G, theta=theta, softening=softening)

    return acc

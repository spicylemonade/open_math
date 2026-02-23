"""
Minimal 2D Barnes-Hut tree code for O(N log N) gravitational force
computation with monopole approximation.

Reference: Barnes & Hut (1986), Nature 324, 446-449.
"""

import numpy as np

# ---------------------------------------------------------------------------
# Quad-tree node
# ---------------------------------------------------------------------------

class QuadNode:
    """A node in the 2D quad-tree (Barnes-Hut)."""
    __slots__ = ('cx', 'cy', 'half', 'mass', 'com_x', 'com_y',
                 'children', 'body_idx')

    def __init__(self, cx, cy, half):
        self.cx = cx        # center x
        self.cy = cy        # center y
        self.half = half    # half-width of the square cell
        self.mass = 0.0     # total mass in cell
        self.com_x = 0.0    # center of mass x
        self.com_y = 0.0    # center of mass y
        self.children = None  # list of 4 children (or None if leaf)
        self.body_idx = -1   # index of single body (-1 if empty or internal)


def _quadrant(node, px, py):
    """Return quadrant index (0-3) for point (px, py) within node."""
    if px <= node.cx:
        return 2 if py <= node.cy else 0
    else:
        return 3 if py <= node.cy else 1


def _child_center(node, q):
    """Return (cx, cy, half) for child quadrant q."""
    h = node.half / 2.0
    if q == 0:
        return node.cx - h, node.cy + h, h
    elif q == 1:
        return node.cx + h, node.cy + h, h
    elif q == 2:
        return node.cx - h, node.cy - h, h
    else:
        return node.cx + h, node.cy - h, h


def build_tree(masses, positions):
    """
    Build a 2D quad-tree from particle positions.

    Parameters
    ----------
    masses : ndarray (N,)
    positions : ndarray (N, 2)

    Returns
    -------
    root : QuadNode
    """
    N = len(masses)
    if N == 0:
        return QuadNode(0, 0, 1)

    # Determine bounding box
    x_min, y_min = positions.min(axis=0)
    x_max, y_max = positions.max(axis=0)
    cx = (x_min + x_max) / 2.0
    cy = (y_min + y_max) / 2.0
    half = max(x_max - x_min, y_max - y_min) / 2.0 * 1.01  # slight margin

    root = QuadNode(cx, cy, half)

    for i in range(N):
        _insert(root, i, masses[i], positions[i, 0], positions[i, 1])

    return root


def _insert(node, idx, mass, px, py):
    """Insert body idx into the tree rooted at node."""
    if node.mass == 0.0 and node.body_idx == -1:
        # Empty leaf — place body here
        node.body_idx = idx
        node.mass = mass
        node.com_x = px
        node.com_y = py
        return

    if node.children is None:
        # Single-body leaf — subdivide
        node.children = [None, None, None, None]
        # Re-insert the existing body
        old_idx = node.body_idx
        old_mass = node.mass
        old_x = node.com_x
        old_y = node.com_y
        node.body_idx = -1

        q = _quadrant(node, old_x, old_y)
        if node.children[q] is None:
            cx, cy, h = _child_center(node, q)
            node.children[q] = QuadNode(cx, cy, h)
        _insert(node.children[q], old_idx, old_mass, old_x, old_y)

    # Insert new body into appropriate child
    q = _quadrant(node, px, py)
    if node.children[q] is None:
        cx, cy, h = _child_center(node, q)
        node.children[q] = QuadNode(cx, cy, h)
    _insert(node.children[q], idx, mass, px, py)

    # Update mass and COM (monopole approximation)
    total = node.mass + mass
    node.com_x = (node.mass * node.com_x + mass * px) / total
    node.com_y = (node.mass * node.com_y + mass * py) / total
    node.mass = total


# ---------------------------------------------------------------------------
# Force computation via tree walk
# ---------------------------------------------------------------------------

def compute_accelerations_bh(state, G=1.0, softening=1e-4, theta=0.5):
    """
    Compute gravitational accelerations using Barnes-Hut tree.

    Parameters
    ----------
    state : dict with 'masses', 'positions'
    G : float
    softening : float
    theta : float — opening angle parameter (0 = exact, larger = faster)

    Returns
    -------
    acc : ndarray (N, 2)
    """
    masses = state['masses']
    positions = state['positions']
    N = len(masses)

    tree = build_tree(masses, positions)
    acc = np.zeros((N, 2))

    for i in range(N):
        ax, ay = _tree_force(tree, i, positions[i, 0], positions[i, 1],
                             G, softening, theta)
        acc[i, 0] = ax
        acc[i, 1] = ay

    return acc


def _tree_force(node, idx, px, py, G, softening, theta):
    """Compute acceleration on particle idx from the tree node."""
    if node is None or node.mass == 0.0:
        return 0.0, 0.0

    dx = node.com_x - px
    dy = node.com_y - py
    dist_sq = dx * dx + dy * dy + softening * softening

    # If this is a leaf with a single body
    if node.children is None:
        if node.body_idx == idx:
            return 0.0, 0.0  # skip self
        inv_dist3 = dist_sq ** (-1.5)
        fx = G * node.mass * dx * inv_dist3
        fy = G * node.mass * dy * inv_dist3
        return fx, fy

    # Opening angle criterion: s/d < theta => treat as single body
    s = 2.0 * node.half
    d = np.sqrt(dx * dx + dy * dy)

    if d > 0 and s / d < theta:
        inv_dist3 = dist_sq ** (-1.5)
        fx = G * node.mass * dx * inv_dist3
        fy = G * node.mass * dy * inv_dist3
        return fx, fy

    # Otherwise recurse into children
    ax, ay = 0.0, 0.0
    for child in node.children:
        if child is not None:
            fx, fy = _tree_force(child, idx, px, py, G, softening, theta)
            ax += fx
            ay += fy
    return ax, ay


if __name__ == '__main__':
    # Quick test
    from gravity_sim import init_random_bodies, compute_accelerations

    np.random.seed(42)
    state = init_random_bodies(100, seed=42)

    acc_direct = compute_accelerations(state, G=1.0, softening=0.01)
    acc_bh = compute_accelerations_bh(state, G=1.0, softening=0.01, theta=0.5)

    # RMS relative error
    err = np.sqrt(np.mean(np.sum((acc_bh - acc_direct)**2, axis=1) /
                          (np.sum(acc_direct**2, axis=1) + 1e-30)))
    print(f"Barnes-Hut (theta=0.5) vs Direct: RMS relative error = {err:.6e}")

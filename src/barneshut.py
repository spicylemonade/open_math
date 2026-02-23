"""Barnes-Hut tree-based O(N log N) gravitational force calculation."""

import math
from src.vector import Vec2

_MAX_DEPTH = 64  # prevent infinite recursion for coincident bodies


class QuadTreeNode:
    """A node in the Barnes-Hut quadtree."""

    __slots__ = ('cx', 'cy', 'half_size', 'total_mass', 'com_x', 'com_y',
                 'body_indices', 'children', 'is_leaf', 'is_empty', 'depth')

    def __init__(self, cx, cy, half_size, depth=0):
        self.cx = cx
        self.cy = cy
        self.half_size = half_size
        self.depth = depth
        self.total_mass = 0.0
        self.com_x = 0.0
        self.com_y = 0.0
        self.body_indices = []  # indices of bodies in this leaf
        self.children = [None, None, None, None]  # NW, NE, SW, SE
        self.is_leaf = True
        self.is_empty = True

    def _quadrant(self, x, y):
        if y >= self.cy:
            return 1 if x >= self.cx else 0
        else:
            return 3 if x >= self.cx else 2

    def _child_center(self, quadrant):
        q = self.half_size / 2.0
        if quadrant == 0:
            return self.cx - q, self.cy + q
        elif quadrant == 1:
            return self.cx + q, self.cy + q
        elif quadrant == 2:
            return self.cx - q, self.cy - q
        else:
            return self.cx + q, self.cy - q

    def insert(self, idx, x, y, mass):
        """Insert a body into this node."""
        if self.is_empty:
            self.body_indices = [idx]
            self.total_mass = mass
            self.com_x = x
            self.com_y = y
            self.is_empty = False
            self.is_leaf = True
            return

        # Update center of mass
        new_total = self.total_mass + mass
        self.com_x = (self.com_x * self.total_mass + x * mass) / new_total
        self.com_y = (self.com_y * self.total_mass + y * mass) / new_total
        self.total_mass = new_total

        # At max depth, store multiple bodies in same leaf
        if self.depth >= _MAX_DEPTH:
            self.body_indices.append(idx)
            return

        if self.is_leaf:
            # Subdivide: move existing bodies to children
            old_indices = self.body_indices
            self.body_indices = []
            self.is_leaf = False
            for oi in old_indices:
                self._insert_into_child(oi, _body_positions[oi][0],
                                        _body_positions[oi][1],
                                        _body_masses[oi])

        self._insert_into_child(idx, x, y, mass)

    def _insert_into_child(self, idx, x, y, mass):
        q = self._quadrant(x, y)
        if self.children[q] is None:
            ccx, ccy = self._child_center(q)
            self.children[q] = QuadTreeNode(ccx, ccy, self.half_size / 2.0,
                                            self.depth + 1)
        self.children[q].insert(idx, x, y, mass)


# Module-level storage for body positions/masses during tree construction
_body_positions = []
_body_masses = []


def build_quadtree(bodies):
    """Build a quadtree from a list of bodies."""
    global _body_positions, _body_masses

    if not bodies:
        return QuadTreeNode(0, 0, 1)

    _body_positions = [(b.pos.x, b.pos.y) for b in bodies]
    _body_masses = [b.mass for b in bodies]

    min_x = min(p[0] for p in _body_positions)
    max_x = max(p[0] for p in _body_positions)
    min_y = min(p[1] for p in _body_positions)
    max_y = max(p[1] for p in _body_positions)

    cx = (min_x + max_x) / 2.0
    cy = (min_y + max_y) / 2.0
    half_size = max(max_x - min_x, max_y - min_y) / 2.0 + 1e-6

    root = QuadTreeNode(cx, cy, half_size)
    for i, (x, y) in enumerate(_body_positions):
        root.insert(i, x, y, _body_masses[i])

    return root


def _tree_force_on_body(node, body_idx, bx, by, G, eps2, theta):
    """Compute gravitational acceleration on body_idx at (bx, by) from tree node."""
    if node is None or node.is_empty:
        return 0.0, 0.0

    dx = node.com_x - bx
    dy = node.com_y - by
    r2 = dx * dx + dy * dy

    if node.is_leaf:
        # Leaf: sum over individual bodies, skipping self
        ax, ay = 0.0, 0.0
        for idx in node.body_indices:
            if idx == body_idx:
                continue
            ddx = _body_positions[idx][0] - bx
            ddy = _body_positions[idx][1] - by
            dr2 = ddx * ddx + ddy * ddy + eps2
            inv_r3 = G * _body_masses[idx] / (dr2 * math.sqrt(dr2))
            ax += inv_r3 * ddx
            ay += inv_r3 * ddy
        return ax, ay

    # Opening criterion: s/d < theta
    s = 2.0 * node.half_size
    if r2 > 0 and (s * s) / r2 < theta * theta:
        r2_soft = r2 + eps2
        inv_r3 = G * node.total_mass / (r2_soft * math.sqrt(r2_soft))
        return inv_r3 * dx, inv_r3 * dy

    # Recurse into children
    ax, ay = 0.0, 0.0
    for child in node.children:
        if child is not None and not child.is_empty:
            cax, cay = _tree_force_on_body(child, body_idx, bx, by, G, eps2, theta)
            ax += cax
            ay += cay
    return ax, ay


def barneshut_gravity(bodies, G=1.0, softening=0.0, theta=0.5):
    """Compute gravitational accelerations using the Barnes-Hut algorithm.

    Parameters
    ----------
    bodies : list of Body
    G : float
    softening : float
    theta : float
        Opening angle parameter (0 = exact, larger = more approximate).

    Returns
    -------
    list of Vec2
        Acceleration for each body.
    """
    if len(bodies) <= 1:
        return [Vec2(0, 0) for _ in bodies]

    root = build_quadtree(bodies)
    eps2 = softening * softening
    accelerations = []

    for i, b in enumerate(bodies):
        ax, ay = _tree_force_on_body(root, i, b.pos.x, b.pos.y, G, eps2, theta)
        accelerations.append(Vec2(ax, ay))

    return accelerations

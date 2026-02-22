"""NumPy-accelerated grid for cellular automata simulation.

Uses numpy arrays and scipy convolution for fast neighbor counting.
Provides the same interface as Grid for interchangeability.
"""

import numpy as np
from scipy.signal import convolve2d

from src.grid import Grid


# Convolution kernels
MOORE_KERNEL = np.array([[1, 1, 1],
                         [1, 0, 1],
                         [1, 1, 1]], dtype=np.int32)

VON_NEUMANN_KERNEL = np.array([[0, 1, 0],
                                [1, 0, 1],
                                [0, 1, 0]], dtype=np.int32)


class NumPyGrid:
    """A 2D grid using NumPy arrays for fast computation.

    Drop-in replacement for Grid with the same interface,
    plus fast vectorized neighbor counting via convolution.
    """

    def __init__(self, width, height, boundary="wrap"):
        """Initialize a grid with all cells set to 0.

        Args:
            width: Number of columns.
            height: Number of rows.
            boundary: Boundary condition - 'wrap' (toroidal) or 'fixed'.
        """
        if boundary not in ("wrap", "fixed"):
            raise ValueError(f"boundary must be 'wrap' or 'fixed', got '{boundary}'")
        self.width = width
        self.height = height
        self.boundary = boundary
        self.cells = np.zeros((height, width), dtype=np.int32)

    def get(self, x, y):
        """Get the state of cell at (x, y)."""
        if self.boundary == "wrap":
            return int(self.cells[y % self.height, x % self.width])
        else:
            if 0 <= x < self.width and 0 <= y < self.height:
                return int(self.cells[y, x])
            return 0

    def set(self, x, y, state):
        """Set the state of cell at (x, y)."""
        if self.boundary == "wrap":
            self.cells[y % self.height, x % self.width] = state
        else:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.cells[y, x] = state

    def neighbors_moore(self, x, y):
        """Get the 8 Moore neighbors of cell (x, y)."""
        offsets = [
            (0, -1), (1, -1), (1, 0), (1, 1),
            (0, 1), (-1, 1), (-1, 0), (-1, -1),
        ]
        return [self.get(x + dx, y + dy) for dx, dy in offsets]

    def neighbors_von_neumann(self, x, y):
        """Get the 4 von Neumann neighbors of cell (x, y)."""
        offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        return [self.get(x + dx, y + dy) for dx, dy in offsets]

    def count_moore(self, x, y):
        """Count the sum of Moore neighbor states."""
        return sum(self.neighbors_moore(x, y))

    def count_von_neumann(self, x, y):
        """Count the sum of von Neumann neighbor states."""
        return sum(self.neighbors_von_neumann(x, y))

    def moore_counts(self):
        """Compute Moore neighbor counts for all cells using convolution.

        Returns:
            NumPy array of neighbor counts with same shape as cells.
        """
        mode = "wrap" if self.boundary == "wrap" else "fill"
        return convolve2d(self.cells, MOORE_KERNEL, mode="same", boundary=mode)

    def copy(self):
        """Create a deep copy of this grid."""
        new_grid = NumPyGrid(self.width, self.height, self.boundary)
        new_grid.cells = self.cells.copy()
        return new_grid

    def snapshot(self):
        """Return a tuple-of-tuples snapshot of cell states."""
        return tuple(tuple(int(v) for v in row) for row in self.cells)

    def population(self):
        """Count non-zero cells."""
        return int(np.count_nonzero(self.cells))

    def clear(self):
        """Set all cells to 0."""
        self.cells.fill(0)

    def __eq__(self, other):
        """Check equality."""
        if isinstance(other, NumPyGrid):
            return (self.width == other.width and self.height == other.height
                    and np.array_equal(self.cells, other.cells))
        if isinstance(other, Grid):
            return self.snapshot() == other.snapshot()
        return NotImplemented

    def __repr__(self):
        return f"NumPyGrid({self.width}, {self.height}, boundary='{self.boundary}')"

    def to_string(self):
        """Render the grid as a string."""
        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                line += "O" if self.cells[y, x] else "."
            lines.append(line)
        return "\n".join(lines)

    @classmethod
    def from_grid(cls, grid):
        """Create a NumPyGrid from a regular Grid.

        Args:
            grid: Source Grid instance.

        Returns:
            NumPyGrid with same state.
        """
        ng = cls(grid.width, grid.height, grid.boundary)
        for y in range(grid.height):
            for x in range(grid.width):
                ng.cells[y, x] = grid.get(x, y)
        return ng

    def to_grid(self):
        """Convert to a regular Grid.

        Returns:
            Grid with same state.
        """
        g = Grid(self.width, self.height, self.boundary)
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y, x]:
                    g.set(x, y, int(self.cells[y, x]))
        return g


class NumPyLifeRule:
    """Vectorized Game of Life rule using NumPy convolution."""

    def apply(self, grid):
        """Apply Game of Life rules using vectorized convolution.

        Args:
            grid: NumPyGrid instance.

        Returns:
            New NumPyGrid with the next generation.
        """
        counts = grid.moore_counts()
        new_cells = ((grid.cells == 1) & ((counts == 2) | (counts == 3))) | \
                    ((grid.cells == 0) & (counts == 3))
        new_grid = NumPyGrid(grid.width, grid.height, grid.boundary)
        new_grid.cells = new_cells.astype(np.int32)
        return new_grid


class NumPyTotalisticRule:
    """Vectorized outer-totalistic rule using NumPy convolution."""

    def __init__(self, birth, survival):
        """Initialize with birth and survival sets."""
        self.birth = set(birth)
        self.survival = set(survival)

    def apply(self, grid):
        """Apply the rule using vectorized operations."""
        counts = grid.moore_counts()
        birth_mask = np.zeros_like(counts, dtype=bool)
        for b in self.birth:
            birth_mask |= (counts == b)
        survival_mask = np.zeros_like(counts, dtype=bool)
        for s in self.survival:
            survival_mask |= (counts == s)
        new_cells = ((grid.cells == 1) & survival_mask) | \
                    ((grid.cells == 0) & birth_mask)
        new_grid = NumPyGrid(grid.width, grid.height, grid.boundary)
        new_grid.cells = new_cells.astype(np.int32)
        return new_grid

"""Grid data structure for cellular automata simulation.

Provides a 2D grid with configurable boundary conditions and neighborhood lookups.
"""

import copy


class Grid:
    """A 2D grid of cell states for cellular automata.

    Supports toroidal (wrap-around) and fixed boundary conditions,
    Moore and von Neumann neighborhood lookups, and snapshot/copy.
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
        self._cells = [[0] * width for _ in range(height)]

    def get(self, x, y):
        """Get the state of cell at (x, y).

        Args:
            x: Column index.
            y: Row index.

        Returns:
            Cell state (int). Returns 0 for out-of-bounds cells with fixed boundary.
        """
        if self.boundary == "wrap":
            return self._cells[y % self.height][x % self.width]
        else:
            if 0 <= x < self.width and 0 <= y < self.height:
                return self._cells[y][x]
            return 0

    def set(self, x, y, state):
        """Set the state of cell at (x, y).

        Args:
            x: Column index.
            y: Row index.
            state: New cell state (int).
        """
        if self.boundary == "wrap":
            self._cells[y % self.height][x % self.width] = state
        else:
            if 0 <= x < self.width and 0 <= y < self.height:
                self._cells[y][x] = state

    def neighbors_moore(self, x, y):
        """Get the 8 Moore neighbors of cell (x, y).

        Args:
            x: Column index.
            y: Row index.

        Returns:
            List of 8 cell states (N, NE, E, SE, S, SW, W, NW).
        """
        offsets = [
            (0, -1), (1, -1), (1, 0), (1, 1),
            (0, 1), (-1, 1), (-1, 0), (-1, -1),
        ]
        return [self.get(x + dx, y + dy) for dx, dy in offsets]

    def neighbors_von_neumann(self, x, y):
        """Get the 4 von Neumann neighbors of cell (x, y).

        Args:
            x: Column index.
            y: Row index.

        Returns:
            List of 4 cell states (N, E, S, W).
        """
        offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        return [self.get(x + dx, y + dy) for dx, dy in offsets]

    def count_moore(self, x, y):
        """Count the sum of Moore neighbor states.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            Sum of the 8 Moore neighbor states.
        """
        return sum(self.neighbors_moore(x, y))

    def count_von_neumann(self, x, y):
        """Count the sum of von Neumann neighbor states.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            Sum of the 4 von Neumann neighbor states.
        """
        return sum(self.neighbors_von_neumann(x, y))

    def copy(self):
        """Create a deep copy of this grid.

        Returns:
            A new Grid with the same dimensions, boundary, and cell states.
        """
        new_grid = Grid(self.width, self.height, self.boundary)
        new_grid._cells = copy.deepcopy(self._cells)
        return new_grid

    def snapshot(self):
        """Return a tuple-of-tuples snapshot of the current cell states.

        Returns:
            Immutable snapshot of cell states for hashing or comparison.
        """
        return tuple(tuple(row) for row in self._cells)

    def population(self):
        """Count the number of live (non-zero) cells.

        Returns:
            Number of cells with state != 0.
        """
        return sum(cell for row in self._cells for cell in row)

    def clear(self):
        """Set all cells to 0."""
        self._cells = [[0] * self.width for _ in range(self.height)]

    def __eq__(self, other):
        """Check equality with another Grid."""
        if not isinstance(other, Grid):
            return NotImplemented
        return (self.width == other.width and self.height == other.height
                and self._cells == other._cells)

    def __repr__(self):
        """String representation showing dimensions and boundary."""
        return f"Grid({self.width}, {self.height}, boundary='{self.boundary}')"

    def to_string(self):
        """Render the grid as a string using . and O characters.

        Returns:
            Multi-line string representation.
        """
        lines = []
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                line += "O" if self._cells[y][x] else "."
            lines.append(line)
        return "\n".join(lines)

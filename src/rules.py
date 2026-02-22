"""Rule engines for cellular automata.

Implements elementary 1D rules (Wolfram), Conway's Game of Life,
and generic outer-totalistic 2D rules.
"""

from src.grid import Grid


class Elementary1DRule:
    """Wolfram elementary 1D cellular automaton rule (0-255).

    Operates on a Grid of height 1 (or the first row of a 2D grid),
    using 3-cell neighborhoods to produce the next generation.
    For multi-row grids, each row is treated as a separate generation
    and the rule fills successive rows from top to bottom.
    """

    def __init__(self, rule_number):
        """Initialize with a Wolfram rule number.

        Args:
            rule_number: Integer 0-255 specifying the rule.
        """
        if not 0 <= rule_number <= 255:
            raise ValueError(f"Rule number must be 0-255, got {rule_number}")
        self.rule_number = rule_number
        self._lookup = {}
        for i in range(8):
            pattern = ((i >> 2) & 1, (i >> 1) & 1, i & 1)
            self._lookup[pattern] = (rule_number >> i) & 1

    def apply(self, grid):
        """Apply the rule to produce the next generation.

        For a 1D grid (height=1), returns a new grid with the next state.
        Uses the grid's boundary conditions for edge cells.

        Args:
            grid: Input Grid (uses first row as current state).

        Returns:
            New Grid with the next generation in the first row.
        """
        new_grid = Grid(grid.width, grid.height, grid.boundary)
        for x in range(grid.width):
            left = grid.get(x - 1, 0)
            center = grid.get(x, 0)
            right = grid.get(x + 1, 0)
            new_grid.set(x, 0, self._lookup[(left, center, right)])
        return new_grid


class LifeRule:
    """Conway's Game of Life rule (B3/S23).

    Uses Moore neighborhood on a 2D grid.
    """

    def apply(self, grid):
        """Apply Game of Life rules to produce the next generation.

        Args:
            grid: Input Grid.

        Returns:
            New Grid with the next generation.
        """
        new_grid = Grid(grid.width, grid.height, grid.boundary)
        for y in range(grid.height):
            for x in range(grid.width):
                alive = grid.get(x, y)
                count = grid.count_moore(x, y)
                if alive:
                    new_grid.set(x, y, 1 if count in (2, 3) else 0)
                else:
                    new_grid.set(x, y, 1 if count == 3 else 0)
        return new_grid


class GenericTotalisticRule:
    """Generic outer-totalistic 2D rule with configurable birth/survival sets.

    Uses Moore neighborhood. Parameterized by birth and survival conditions.
    """

    def __init__(self, birth, survival):
        """Initialize with birth and survival neighbor counts.

        Args:
            birth: Set/list of neighbor counts that cause a dead cell to become alive.
            survival: Set/list of neighbor counts that keep a live cell alive.
        """
        self.birth = set(birth)
        self.survival = set(survival)

    def apply(self, grid):
        """Apply the outer-totalistic rule to produce the next generation.

        Args:
            grid: Input Grid.

        Returns:
            New Grid with the next generation.
        """
        new_grid = Grid(grid.width, grid.height, grid.boundary)
        for y in range(grid.height):
            for x in range(grid.width):
                alive = grid.get(x, y)
                count = grid.count_moore(x, y)
                if alive:
                    new_grid.set(x, y, 1 if count in self.survival else 0)
                else:
                    new_grid.set(x, y, 1 if count in self.birth else 0)
        return new_grid

    @classmethod
    def from_rulestring(cls, rulestring):
        """Create a rule from B/S notation (e.g., 'B3/S23').

        Args:
            rulestring: String in B{digits}/S{digits} format.

        Returns:
            GenericTotalisticRule instance.
        """
        parts = rulestring.upper().split("/")
        birth = set()
        survival = set()
        for part in parts:
            if part.startswith("B"):
                birth = {int(c) for c in part[1:]}
            elif part.startswith("S"):
                survival = {int(c) for c in part[1:]}
        return cls(birth, survival)

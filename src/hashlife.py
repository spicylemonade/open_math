"""HashLife algorithm for efficient large-pattern Game of Life simulation.

Implements the Gosper HashLife algorithm (Gosper, 1984) using:
  1. Quadtree node representation with memoization
  2. Canonical node caching (hash consing)
  3. Recursive macro-stepping for exponential time jumps

Reference: Gosper, R.W. (1984). "Exploiting regularities in large cellular
spaces." Physica D, 10(1-2), 75-80.
"""


class HashLifeNode:
    """Immutable quadtree node for HashLife.

    A level-k node represents a 2^k × 2^k region of cells.
    Level 0 nodes are single cells (0 or 1).
    Higher-level nodes contain four quadrant children (nw, ne, sw, se).
    """
    __slots__ = ("level", "nw", "ne", "sw", "se", "population", "_hash", "result")

    def __init__(self, level, nw=None, ne=None, sw=None, se=None, population=None):
        self.level = level
        self.nw = nw
        self.ne = ne
        self.sw = sw
        self.se = se
        self.result = None
        if level == 0:
            self.population = population if population is not None else 0
        else:
            self.population = nw.population + ne.population + sw.population + se.population
        self._hash = hash((level, id(nw), id(ne), id(sw), id(se), self.population))

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return self is other


class HashLife:
    """HashLife engine implementing the Gosper algorithm for Conway's Game of Life.

    Uses canonical node caching and memoized macro-stepping to achieve
    exponential speedup on patterns with spatial/temporal regularity.
    """

    def __init__(self):
        self._cache = {}  # (level, nw, ne, sw, se) -> node
        self._result_cache = {}  # node id -> result node
        # Canonical leaf nodes
        self.off = self._canonical_leaf(0)
        self.on = self._canonical_leaf(1)
        self._empty_cache = {}

    def _canonical_leaf(self, population):
        """Get or create a canonical level-0 (leaf) node."""
        key = (0, None, None, None, None, population)
        if key not in self._cache:
            node = HashLifeNode(0, population=population)
            self._cache[key] = node
        return self._cache[key]

    def make_node(self, nw, ne, sw, se):
        """Get or create a canonical node from four children.

        This is the hash-consing step: identical sub-patterns
        share a single node object.

        Args:
            nw, ne, sw, se: Four child nodes of level k-1.

        Returns:
            Canonical node of level k.
        """
        key = (nw.level + 1, id(nw), id(ne), id(sw), id(se))
        if key not in self._cache:
            node = HashLifeNode(nw.level + 1, nw, ne, sw, se)
            self._cache[key] = node
        return self._cache[key]

    def empty_node(self, level):
        """Get a canonical empty node at the given level."""
        if level in self._empty_cache:
            return self._empty_cache[level]
        if level == 0:
            node = self.off
        else:
            sub = self.empty_node(level - 1)
            node = self.make_node(sub, sub, sub, sub)
        self._empty_cache[level] = node
        return node

    def _life_4x4(self, node):
        """Compute the 2x2 center result of a 4x4 (level-2) node after 1 step.

        This is the base case for the recursive HashLife algorithm.
        """
        # Extract all 16 cells from the 4x4 region
        # Level-2 node has four level-1 children, each a 2x2 block
        # nw.nw nw.ne | ne.nw ne.ne
        # nw.sw nw.se | ne.sw ne.se
        # ------|------
        # sw.nw sw.ne | se.nw se.ne
        # sw.sw sw.se | se.sw se.se
        cells = [
            [node.nw.nw.population, node.nw.ne.population, node.ne.nw.population, node.ne.ne.population],
            [node.nw.sw.population, node.nw.se.population, node.ne.sw.population, node.ne.se.population],
            [node.sw.nw.population, node.sw.ne.population, node.se.nw.population, node.se.ne.population],
            [node.sw.sw.population, node.sw.se.population, node.se.sw.population, node.se.se.population],
        ]

        def next_cell(x, y):
            alive = cells[y][x]
            count = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < 4 and 0 <= nx < 4:
                        count += cells[ny][nx]
            if alive:
                return self.on if count in (2, 3) else self.off
            else:
                return self.on if count == 3 else self.off

        # The center 2x2 result
        return self.make_node(
            next_cell(1, 1), next_cell(2, 1),
            next_cell(1, 2), next_cell(2, 2)
        )

    def _center(self, node):
        """Get the center sub-node of a node (the inner 2^(k-1) x 2^(k-1))."""
        return self.make_node(
            node.nw.se, node.ne.sw,
            node.sw.ne, node.se.nw
        )

    def step(self, node):
        """Compute the result of a node: the center 2^(k-1) × 2^(k-1) region
        advanced by 2^(k-2) generations.

        For level 2: advance 1 step, return 2x2 center.
        For level k>2: advance 2^(k-2) steps, return level k-1 center.

        Args:
            node: A HashLife node of level >= 2.

        Returns:
            Result node of level k-1.
        """
        if node.result is not None:
            return node.result

        if node.level == 2:
            result = self._life_4x4(node)
        else:
            # Construct 9 overlapping sub-quadrants of level k-1
            n00 = node.nw
            n01 = self.make_node(node.nw.ne, node.ne.nw, node.nw.se, node.ne.sw)
            n02 = node.ne
            n10 = self.make_node(node.nw.sw, node.nw.se, node.sw.nw, node.sw.ne)
            n11 = self._center(node)
            n12 = self.make_node(node.ne.sw, node.ne.se, node.se.nw, node.se.ne)
            n20 = node.sw
            n21 = self.make_node(node.sw.ne, node.se.nw, node.sw.se, node.se.sw)
            n22 = node.se

            # Recursive step on each of the 9 sub-quadrants
            r00 = self.step(n00)
            r01 = self.step(n01)
            r02 = self.step(n02)
            r10 = self.step(n10)
            r11 = self.step(n11)
            r12 = self.step(n12)
            r20 = self.step(n20)
            r21 = self.step(n21)
            r22 = self.step(n22)

            # Combine into 4 overlapping nodes and recurse again
            result = self.make_node(
                self.step(self.make_node(r00, r01, r10, r11)),
                self.step(self.make_node(r01, r02, r11, r12)),
                self.step(self.make_node(r10, r11, r20, r21)),
                self.step(self.make_node(r11, r12, r21, r22)),
            )

        node.result = result
        return result

    def expand(self, node):
        """Expand a node by adding an empty border around it.

        Creates a level k+1 node with the original in the center.
        """
        empty = self.empty_node(node.level - 1)
        return self.make_node(
            self.make_node(empty, empty, empty, node.nw),
            self.make_node(empty, empty, node.ne, empty),
            self.make_node(empty, node.sw, empty, empty),
            self.make_node(node.se, empty, empty, empty),
        )

    def advance(self, node, steps):
        """Advance a pattern by exactly `steps` generations.

        Repeatedly expands and steps to cover the requested generation count.

        Args:
            node: Root HashLife node.
            steps: Number of generations to advance.

        Returns:
            Root node after advancing.
        """
        # Ensure the node is big enough
        while node.level < 3 or steps > 2 ** (node.level - 2):
            node = self.expand(node)

        if steps == 0:
            return node

        if steps == 2 ** (node.level - 2):
            # Full macro step
            result = self.step(node)
            # Pad result back up to maintain tree structure
            while result.level < node.level:
                result = self.expand(result)
            return result

        # Partial step: advance in smaller increments
        half = 2 ** (node.level - 3)
        if steps <= half:
            # Only need to step the sub-quadrants
            # Shrink, step, re-expand
            sub = self._center(node)
            sub = self.expand(sub)
            return self.advance(sub, steps)
        else:
            # Step fully, then step the remainder
            node = self.expand(node)
            full_step = 2 ** (node.level - 2)
            # Use binary decomposition
            result = node
            remaining = steps
            while remaining > 0:
                while result.level < 3 or 2 ** (result.level - 2) > remaining:
                    if result.level < 3:
                        result = self.expand(result)
                        break
                    # Need to work at a smaller scale
                    break
                step_size = 2 ** (result.level - 2)
                if step_size <= remaining:
                    while result.level < 3:
                        result = self.expand(result)
                    result = self.expand(result)
                    inner = self.step(result)
                    while inner.level < result.level:
                        inner = self.expand(inner)
                    result = inner
                    remaining -= step_size // 2  # step gives half the time
                    # This approach is complex; use simpler method
                    break
                else:
                    result = self.expand(result)

            # Fallback: simple repeated expansion and stepping
            return self._advance_simple(node, steps)

    def _advance_simple(self, node, steps):
        """Simple advancement by repeatedly stepping single generations.

        Used as fallback for non-power-of-2 step counts.
        """
        for _ in range(steps):
            while node.level < 3:
                node = self.expand(node)
            # Ensure enough room
            node = self.expand(node)
            node = self.step(node)
            # Re-expand to maintain proper structure
            while node.level < 3:
                node = self.expand(node)
        return node

    def advance_pow2(self, node, log2_steps):
        """Advance by exactly 2^log2_steps generations using a single macro-step.

        This is the most efficient mode: one recursive call.

        Args:
            node: Root node.
            log2_steps: Log base 2 of the number of steps.

        Returns:
            Root node after 2^log2_steps generations.
        """
        target_level = log2_steps + 2
        while node.level < target_level:
            node = self.expand(node)
        result = self.step(node)
        return result

    def from_cells(self, cells, width, height):
        """Create a HashLife node from a 2D list of cell states.

        Args:
            cells: 2D list/array of 0s and 1s.
            width: Grid width.
            height: Grid height.

        Returns:
            Root HashLife node containing the pattern.
        """
        # Find the required level (smallest power of 2 >= max(width, height))
        size = max(width, height)
        level = 0
        while (1 << level) < size:
            level += 1
        if level < 1:
            level = 1

        return self._build_node(cells, 0, 0, level, width, height)

    def _build_node(self, cells, x, y, level, width, height):
        """Recursively build a quadtree node from cell data."""
        if level == 0:
            if 0 <= y < height and 0 <= x < width:
                return self.on if cells[y][x] else self.off
            return self.off

        half = 1 << (level - 1)
        nw = self._build_node(cells, x, y, level - 1, width, height)
        ne = self._build_node(cells, x + half, y, level - 1, width, height)
        sw = self._build_node(cells, x, y + half, level - 1, width, height)
        se = self._build_node(cells, x + half, y + half, level - 1, width, height)
        return self.make_node(nw, ne, sw, se)

    def to_cells(self, node):
        """Extract cell states from a HashLife node.

        Returns:
            Dictionary mapping (x, y) -> 1 for all live cells.
        """
        cells = {}
        size = 1 << node.level
        self._extract_cells(node, 0, 0, cells)
        return cells

    def _extract_cells(self, node, x, y, cells):
        """Recursively extract live cells."""
        if node.population == 0:
            return
        if node.level == 0:
            if node.population:
                cells[(x, y)] = 1
            return
        half = 1 << (node.level - 1)
        self._extract_cells(node.nw, x, y, cells)
        self._extract_cells(node.ne, x + half, y, cells)
        self._extract_cells(node.sw, x, y + half, cells)
        self._extract_cells(node.se, x + half, y + half, cells)

    def to_grid_array(self, node, offset_x=0, offset_y=0, width=None, height=None):
        """Convert to a 2D list for comparison with Grid/NumPyGrid.

        Args:
            node: Root node.
            offset_x, offset_y: Offset to apply to cell coordinates.
            width, height: Output grid dimensions. If None, uses node size.

        Returns:
            2D list of 0s and 1s.
        """
        size = 1 << node.level
        if width is None:
            width = size
        if height is None:
            height = size
        grid = [[0] * width for _ in range(height)]
        cells = self.to_cells(node)
        for (cx, cy), val in cells.items():
            gx = cx + offset_x
            gy = cy + offset_y
            if 0 <= gx < width and 0 <= gy < height:
                grid[gy][gx] = val
        return grid

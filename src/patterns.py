"""Pattern I/O for cellular automata.

Supports RLE (Run Length Encoded) and plaintext (.cells) formats
for loading and saving CA patterns.
"""

import re

from src.grid import Grid


# --- Embedded test patterns ---

GLIDER_RLE = "x = 3, y = 3, rule = B3/S23\nbo$2bo$3o!"

GLIDER_CELLS = """.O.
..O
OOO"""

GOSPER_GLIDER_GUN_RLE = (
    "x = 36, y = 9, rule = B3/S23\n"
    "24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$"
    "2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!"
)

R_PENTOMINO_RLE = "x = 3, y = 3, rule = B3/S23\nb2o$2ob$bo!"

R_PENTOMINO_CELLS = """.OO
OO.
.O."""


def parse_rle(rle_string):
    """Parse an RLE-format pattern string.

    Args:
        rle_string: RLE format string.

    Returns:
        Tuple of (cells, width, height) where cells is a 2D list.
    """
    lines = rle_string.strip().split("\n")

    # Parse header
    width = 0
    height = 0
    for line in lines:
        line = line.strip()
        if line.startswith("x"):
            match = re.match(r"x\s*=\s*(\d+)\s*,\s*y\s*=\s*(\d+)", line)
            if match:
                width = int(match.group(1))
                height = int(match.group(2))
            break

    # Parse pattern data (everything after header, ignoring comments)
    pattern_data = ""
    header_found = False
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.startswith("x"):
            header_found = True
            continue
        if header_found:
            pattern_data += line

    # Decode RLE
    cells = [[0] * width for _ in range(height)]
    x, y = 0, 0
    i = 0
    while i < len(pattern_data):
        ch = pattern_data[i]
        if ch == "!":
            break
        if ch == "$":
            y += 1
            x = 0
            i += 1
            continue
        # Parse optional run count
        run = 0
        while i < len(pattern_data) and pattern_data[i].isdigit():
            run = run * 10 + int(pattern_data[i])
            i += 1
        if run == 0:
            run = 1
        if i >= len(pattern_data):
            break
        ch = pattern_data[i]
        i += 1
        if ch == "$":
            y += run
            x = 0
            continue
        if ch == "!":
            break
        state = 1 if ch == "o" else 0
        for _ in range(run):
            if y < height and x < width:
                cells[y][x] = state
            x += 1

    return cells, width, height


def write_rle(cells, width, height, rule="B3/S23"):
    """Write a 2D cell array to RLE format.

    Args:
        cells: 2D list of 0s and 1s.
        width: Pattern width.
        height: Pattern height.
        rule: Rule string (default B3/S23).

    Returns:
        RLE format string.
    """
    lines = [f"x = {width}, y = {height}, rule = {rule}"]
    pattern = ""

    for y in range(height):
        x = 0
        while x < width:
            state = cells[y][x]
            ch = "o" if state else "b"
            run = 1
            while x + run < width and cells[y][x + run] == state:
                run += 1
            # Skip trailing dead cells on a row
            if state == 0 and x + run >= width:
                break
            if run > 1:
                pattern += f"{run}{ch}"
            else:
                pattern += ch
            x += run
        if y < height - 1:
            pattern += "$"

    pattern += "!"
    lines.append(pattern)
    return "\n".join(lines)


def parse_cells(cells_string):
    """Parse a plaintext (.cells) format pattern string.

    Uses '.' for dead and 'O' (or '*') for alive.

    Args:
        cells_string: Plaintext format string.

    Returns:
        Tuple of (cells, width, height).
    """
    lines = []
    for line in cells_string.strip().split("\n"):
        line = line.rstrip()
        if line.startswith("!"):
            continue
        lines.append(line)

    if not lines:
        return [[]], 0, 0

    height = len(lines)
    width = max(len(line) for line in lines)
    cells = [[0] * width for _ in range(height)]

    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch in ("O", "*", "1"):
                cells[y][x] = 1

    return cells, width, height


def write_cells(cells, width, height):
    """Write a 2D cell array to plaintext (.cells) format.

    Args:
        cells: 2D list of 0s and 1s.
        width: Pattern width.
        height: Pattern height.

    Returns:
        Plaintext format string.
    """
    lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            line += "O" if cells[y][x] else "."
        lines.append(line)
    return "\n".join(lines)


def load_pattern_to_grid(cells, width, height, grid, offset_x=0, offset_y=0):
    """Place a pattern onto a grid at the given offset.

    Args:
        cells: 2D list of 0s and 1s.
        width: Pattern width.
        height: Pattern height.
        grid: Target Grid instance.
        offset_x: X offset on the grid.
        offset_y: Y offset on the grid.
    """
    for y in range(height):
        for x in range(width):
            if cells[y][x]:
                grid.set(x + offset_x, y + offset_y, 1)

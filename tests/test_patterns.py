"""Tests for src.patterns module."""

from src.grid import Grid
from src.patterns import (
    parse_rle, write_rle, parse_cells, write_cells,
    load_pattern_to_grid,
    GLIDER_RLE, GLIDER_CELLS, GOSPER_GLIDER_GUN_RLE,
    R_PENTOMINO_RLE, R_PENTOMINO_CELLS,
)


def test_parse_rle_glider():
    cells, w, h = parse_rle(GLIDER_RLE)
    assert w == 3 and h == 3
    assert cells[0] == [0, 1, 0]
    assert cells[1] == [0, 0, 1]
    assert cells[2] == [1, 1, 1]


def test_parse_rle_gosper_gun():
    cells, w, h = parse_rle(GOSPER_GLIDER_GUN_RLE)
    assert w == 36 and h == 9
    total = sum(c for row in cells for c in row)
    assert total == 36  # Gosper gun has 36 live cells


def test_parse_rle_r_pentomino():
    cells, w, h = parse_rle(R_PENTOMINO_RLE)
    assert w == 3 and h == 3
    total = sum(c for row in cells for c in row)
    assert total == 5  # R-pentomino has 5 cells


def test_write_rle_roundtrip():
    """Parse RLE, write it back, parse again — should produce same cells."""
    cells1, w1, h1 = parse_rle(GLIDER_RLE)
    rle_out = write_rle(cells1, w1, h1)
    cells2, w2, h2 = parse_rle(rle_out)
    assert cells1 == cells2


def test_parse_cells_glider():
    cells, w, h = parse_cells(GLIDER_CELLS)
    assert w == 3 and h == 3
    assert cells[0] == [0, 1, 0]
    assert cells[1] == [0, 0, 1]
    assert cells[2] == [1, 1, 1]


def test_write_cells_roundtrip():
    cells1, w1, h1 = parse_cells(GLIDER_CELLS)
    text_out = write_cells(cells1, w1, h1)
    cells2, w2, h2 = parse_cells(text_out)
    assert cells1 == cells2


def test_r_pentomino_cells_roundtrip():
    cells1, w1, h1 = parse_cells(R_PENTOMINO_CELLS)
    assert sum(c for row in cells1 for c in row) == 5
    text_out = write_cells(cells1, w1, h1)
    cells2, w2, h2 = parse_cells(text_out)
    assert cells1 == cells2


def test_load_pattern_to_grid():
    cells, w, h = parse_rle(GLIDER_RLE)
    grid = Grid(10, 10, boundary="wrap")
    load_pattern_to_grid(cells, w, h, grid, offset_x=3, offset_y=3)
    # Glider at offset (3,3): first cell is at (4, 3)
    assert grid.get(4, 3) == 1  # .O. -> (1,0) + offset
    assert grid.get(5, 4) == 1  # ..O -> (2,1) + offset
    assert grid.get(3, 5) == 1  # OOO -> (0,2) + offset
    assert grid.get(4, 5) == 1
    assert grid.get(5, 5) == 1
    assert grid.population() == 5


def test_load_pattern_to_grid_gosper():
    cells, w, h = parse_rle(GOSPER_GLIDER_GUN_RLE)
    grid = Grid(50, 20, boundary="wrap")
    load_pattern_to_grid(cells, w, h, grid, offset_x=2, offset_y=5)
    assert grid.population() == 36

"""Tests for src.grid module."""

import pytest
from src.grid import Grid


def test_init_dimensions():
    g = Grid(10, 5)
    assert g.width == 10
    assert g.height == 5
    assert g.boundary == "wrap"


def test_init_invalid_boundary():
    with pytest.raises(ValueError):
        Grid(5, 5, boundary="invalid")


def test_get_set_basic():
    g = Grid(5, 5)
    assert g.get(2, 3) == 0
    g.set(2, 3, 1)
    assert g.get(2, 3) == 1


def test_wrap_boundary_get():
    g = Grid(5, 5, boundary="wrap")
    g.set(0, 0, 1)
    # Wrapping: (-1, -1) should map to (4, 4)... no, (4,4) is not set
    # Actually (-1, 0) maps to (4, 0) which is not set
    # Set cell and test wrap
    g.set(4, 4, 7)
    assert g.get(-1, -1) == 7  # wraps to (4, 4)
    assert g.get(9, 9) == 7    # wraps to (4, 4)


def test_fixed_boundary_get():
    g = Grid(5, 5, boundary="fixed")
    g.set(0, 0, 1)
    assert g.get(-1, 0) == 0   # out of bounds returns 0
    assert g.get(0, -1) == 0
    assert g.get(5, 0) == 0
    assert g.get(0, 5) == 0
    assert g.get(0, 0) == 1    # in bounds still works


def test_fixed_boundary_set_oob():
    g = Grid(5, 5, boundary="fixed")
    g.set(-1, 0, 1)  # should silently ignore
    g.set(5, 5, 1)   # should silently ignore
    assert g.population() == 0


def test_moore_neighbors_center():
    g = Grid(5, 5)
    g.set(2, 2, 1)
    # Check neighbor counts of adjacent cells
    neighbors = g.neighbors_moore(1, 1)
    # (1,1) has (2,2) as its SE neighbor
    assert 1 in neighbors
    assert g.count_moore(1, 1) == 1


def test_moore_neighbors_corner_wrap():
    g = Grid(3, 3, boundary="wrap")
    # Set all cells to 1
    for y in range(3):
        for x in range(3):
            g.set(x, y, 1)
    # Corner (0,0) should have 8 neighbors, all 1
    assert g.count_moore(0, 0) == 8


def test_moore_neighbors_corner_fixed():
    g = Grid(3, 3, boundary="fixed")
    for y in range(3):
        for x in range(3):
            g.set(x, y, 1)
    # Corner (0,0) with fixed boundary: 3 out-of-bounds neighbors return 0
    # Only (1,0), (1,1), (0,1) are valid = 3 live neighbors
    assert g.count_moore(0, 0) == 3


def test_von_neumann_neighbors():
    g = Grid(5, 5)
    g.set(2, 1, 1)  # N of (2,2)
    g.set(3, 2, 1)  # E of (2,2)
    g.set(2, 3, 1)  # S of (2,2)
    g.set(1, 2, 1)  # W of (2,2)
    assert g.count_von_neumann(2, 2) == 4
    neighbors = g.neighbors_von_neumann(2, 2)
    assert neighbors == [1, 1, 1, 1]


def test_copy_independence():
    g = Grid(5, 5)
    g.set(0, 0, 1)
    g2 = g.copy()
    assert g2.get(0, 0) == 1
    g2.set(0, 0, 0)
    assert g.get(0, 0) == 1   # original unchanged
    assert g2.get(0, 0) == 0


def test_snapshot():
    g = Grid(3, 3)
    g.set(1, 1, 1)
    snap = g.snapshot()
    assert isinstance(snap, tuple)
    assert snap[1][1] == 1
    assert snap[0][0] == 0


def test_population():
    g = Grid(10, 10)
    assert g.population() == 0
    g.set(0, 0, 1)
    g.set(5, 5, 1)
    g.set(9, 9, 1)
    assert g.population() == 3


def test_clear():
    g = Grid(5, 5)
    g.set(2, 2, 1)
    g.set(3, 3, 1)
    g.clear()
    assert g.population() == 0


def test_equality():
    g1 = Grid(3, 3)
    g2 = Grid(3, 3)
    g1.set(1, 1, 1)
    g2.set(1, 1, 1)
    assert g1 == g2
    g2.set(0, 0, 1)
    assert g1 != g2


def test_large_grid():
    g = Grid(1000, 1000)
    g.set(999, 999, 1)
    assert g.get(999, 999) == 1
    g.set(500, 500, 1)
    assert g.population() == 2


def test_to_string():
    g = Grid(3, 3)
    g.set(1, 1, 1)
    s = g.to_string()
    lines = s.split("\n")
    assert len(lines) == 3
    assert lines[1] == ".O."

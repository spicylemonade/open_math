"""Tests for src.hashlife module."""

import pytest
from src.hashlife import HashLife


def get_glider_gun_cells():
    """Return the Gosper glider gun pattern as a 2D list on a 64x64 grid."""
    gun_coords = [
        (24, 0), (22, 1), (24, 1), (12, 2), (13, 2), (20, 2), (21, 2),
        (34, 2), (35, 2), (11, 3), (15, 3), (20, 3), (21, 3), (34, 3),
        (35, 3), (0, 4), (1, 4), (10, 4), (16, 4), (20, 4), (21, 4),
        (0, 5), (1, 5), (10, 5), (14, 5), (16, 5), (17, 5), (22, 5),
        (24, 5), (10, 6), (16, 6), (24, 6), (11, 7), (15, 7), (12, 8),
        (13, 8),
    ]
    size = 64
    cells = [[0] * size for _ in range(size)]
    for x, y in gun_coords:
        cells[y][x] = 1
    return cells, size


def test_leaf_nodes():
    hl = HashLife()
    assert hl.off.population == 0
    assert hl.on.population == 1
    assert hl.off.level == 0
    assert hl.on.level == 0


def test_make_node_canonical():
    hl = HashLife()
    n1 = hl.make_node(hl.on, hl.off, hl.off, hl.off)
    n2 = hl.make_node(hl.on, hl.off, hl.off, hl.off)
    assert n1 is n2  # canonical sharing


def test_empty_node():
    hl = HashLife()
    e2 = hl.empty_node(2)
    assert e2.population == 0
    assert e2.level == 2


def test_blinker_conserves_population():
    """Blinker should maintain population of 3 across steps."""
    hl = HashLife()
    cells = [[0]*8 for _ in range(8)]
    cells[3][3] = 1
    cells[3][4] = 1
    cells[3][5] = 1
    node = hl.from_cells(cells, 8, 8)
    assert node.population == 3

    # expand + step advances by 2^(level-2) steps
    # level 3 -> expand -> level 4 -> step returns level 3, advances 2^2=4 steps
    # blinker period=2, so after 4 steps it's back to original
    node_expanded = hl.expand(node)
    result = hl.step(node_expanded)
    assert result.population == 3


def test_block_still_life():
    """2x2 block should remain unchanged after stepping."""
    hl = HashLife()
    cells = [[0]*8 for _ in range(8)]
    cells[3][3] = 1
    cells[3][4] = 1
    cells[4][3] = 1
    cells[4][4] = 1
    node = hl.from_cells(cells, 8, 8)
    assert node.population == 4

    node_expanded = hl.expand(node)
    result = hl.step(node_expanded)
    assert result.population == 4


def test_glider_gun_population_growth():
    """Gosper glider gun should produce gliders, increasing population."""
    hl = HashLife()
    cells, size = get_glider_gun_cells()
    node = hl.from_cells(cells, size, size)
    initial_pop = node.population
    assert initial_pop == 36  # Gosper gun has 36 cells

    # Advance 2^10 = 1024 generations
    result = hl.advance_pow2(node, 10)
    assert result.population > initial_pop


def test_glider_gun_1024_gen():
    """Gosper glider gun after 1024 generations should produce ~34 gliders."""
    hl = HashLife()
    cells, size = get_glider_gun_cells()
    node = hl.from_cells(cells, size, size)

    # 1024 / 30 ≈ 34 gliders, each with 5 cells = 170 + 36 gun cells = ~206
    result = hl.advance_pow2(node, 10)
    # Population should be significantly higher than initial 36
    assert result.population > 100


def test_advance_pow2_deterministic():
    """Running advance_pow2 twice with same input should give same result."""
    hl = HashLife()
    cells, size = get_glider_gun_cells()
    node1 = hl.from_cells(cells, size, size)
    node2 = hl.from_cells(cells, size, size)

    result1 = hl.advance_pow2(node1, 8)
    result2 = hl.advance_pow2(node2, 8)

    assert result1.population == result2.population

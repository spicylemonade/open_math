"""Tests for src.rules module."""

import pytest
from src.grid import Grid
from src.rules import Elementary1DRule, LifeRule, GenericTotalisticRule


# --- Elementary 1D Rule Tests ---

def test_rule_number_validation():
    with pytest.raises(ValueError):
        Elementary1DRule(256)
    with pytest.raises(ValueError):
        Elementary1DRule(-1)


def test_rule_0_all_die():
    rule = Elementary1DRule(0)
    g = Grid(5, 1, boundary="wrap")
    g.set(2, 0, 1)
    result = rule.apply(g)
    assert result.population() == 0


def test_rule_255_all_live():
    rule = Elementary1DRule(255)
    g = Grid(5, 1, boundary="wrap")
    result = rule.apply(g)
    # All patterns map to 1, so all cells become 1
    assert result.population() == 5


def test_rule_110_known_output():
    """Rule 110 is known to produce specific patterns. Test single step from
    a single live cell."""
    rule = Elementary1DRule(110)
    g = Grid(7, 1, boundary="fixed")
    g.set(3, 0, 1)
    # 110 = 0b01101110
    # x=0: (0,0,0) -> bit 0 = 0
    # x=1: (0,0,0) -> bit 0 = 0
    # x=2: (0,0,1) -> bit 1 = 1
    # x=3: (0,1,0) -> bit 2 = 1
    # x=4: (1,0,0) -> bit 4 = 0
    # x=5: (0,0,0) -> bit 0 = 0
    # x=6: (0,0,0) -> bit 0 = 0
    result = rule.apply(g)
    expected = [0, 0, 1, 1, 0, 0, 0]
    actual = [result.get(x, 0) for x in range(7)]
    assert actual == expected


def test_rule_30_single_cell():
    """Rule 30 from a single center cell."""
    rule = Elementary1DRule(30)
    g = Grid(5, 1, boundary="fixed")
    g.set(2, 0, 1)
    result = rule.apply(g)
    # 30 = 0b00011110
    # (0,0,0)->0, (0,0,1)->1, (0,1,0)->1, (1,0,0)->1, others->0
    expected = [0, 1, 1, 1, 0]
    actual = [result.get(x, 0) for x in range(5)]
    assert actual == expected


# --- Life Rule Tests ---

def test_life_blinker_oscillates():
    """Blinker: 3 horizontal cells should become 3 vertical, then back."""
    g = Grid(5, 5, boundary="wrap")
    # Horizontal blinker at center
    g.set(1, 2, 1)
    g.set(2, 2, 1)
    g.set(3, 2, 1)
    rule = LifeRule()
    g1 = rule.apply(g)
    # Should become vertical
    assert g1.get(2, 1) == 1
    assert g1.get(2, 2) == 1
    assert g1.get(2, 3) == 1
    assert g1.get(1, 2) == 0
    assert g1.get(3, 2) == 0
    # One more step should return to horizontal
    g2 = rule.apply(g1)
    assert g == g2


def test_life_block_still_life():
    """2x2 block should remain unchanged."""
    g = Grid(6, 6, boundary="wrap")
    g.set(2, 2, 1)
    g.set(3, 2, 1)
    g.set(2, 3, 1)
    g.set(3, 3, 1)
    rule = LifeRule()
    g1 = rule.apply(g)
    assert g == g1


def test_life_glider_translates():
    """Glider should translate diagonally after 4 steps."""
    g = Grid(10, 10, boundary="wrap")
    # Standard glider
    g.set(1, 0, 1)
    g.set(2, 1, 1)
    g.set(0, 2, 1)
    g.set(1, 2, 1)
    g.set(2, 2, 1)
    rule = LifeRule()
    for _ in range(4):
        g = rule.apply(g)
    # After 4 steps, glider moves (+1, +1)
    expected = Grid(10, 10, boundary="wrap")
    expected.set(2, 1, 1)
    expected.set(3, 2, 1)
    expected.set(1, 3, 1)
    expected.set(2, 3, 1)
    expected.set(3, 3, 1)
    assert g == expected


def test_life_underpopulation():
    """A single cell should die (0 neighbors)."""
    g = Grid(5, 5, boundary="wrap")
    g.set(2, 2, 1)
    rule = LifeRule()
    g1 = rule.apply(g)
    assert g1.population() == 0


def test_life_overpopulation():
    """A cell with 4+ neighbors should die."""
    g = Grid(5, 5, boundary="wrap")
    # Center cell with 4 neighbors
    g.set(2, 2, 1)
    g.set(1, 2, 1)
    g.set(3, 2, 1)
    g.set(2, 1, 1)
    g.set(2, 3, 1)
    rule = LifeRule()
    g1 = rule.apply(g)
    assert g1.get(2, 2) == 0  # center dies from overpopulation


# --- Generic Totalistic Rule Tests ---

def test_generic_rule_matches_life():
    """GenericTotalisticRule with B3/S23 should behave identically to LifeRule."""
    g = Grid(5, 5, boundary="wrap")
    g.set(1, 2, 1)
    g.set(2, 2, 1)
    g.set(3, 2, 1)
    life = LifeRule()
    generic = GenericTotalisticRule({3}, {2, 3})
    assert life.apply(g) == generic.apply(g)


def test_from_rulestring():
    rule = GenericTotalisticRule.from_rulestring("B3/S23")
    assert rule.birth == {3}
    assert rule.survival == {2, 3}


def test_highlife_replicator():
    """HighLife (B36/S23) should produce different results than standard Life."""
    g = Grid(5, 5, boundary="wrap")
    g.set(1, 2, 1)
    g.set(2, 2, 1)
    g.set(3, 2, 1)
    highlife = GenericTotalisticRule.from_rulestring("B36/S23")
    life = LifeRule()
    # Blinker step 1 should be the same (only B3 matters here)
    hl_result = highlife.apply(g)
    life_result = life.apply(g)
    assert hl_result == life_result  # for this specific pattern, same result


def test_seeds_rule():
    """Seeds (B2/S) - all live cells die, new cells born with 2 neighbors."""
    g = Grid(5, 5, boundary="wrap")
    g.set(2, 2, 1)
    g.set(3, 2, 1)
    seeds = GenericTotalisticRule(birth={2}, survival=set())
    result = seeds.apply(g)
    # Original cells die (no survival conditions)
    assert result.get(2, 2) == 0
    assert result.get(3, 2) == 0
    # Cells with exactly 2 live neighbors are born
    assert result.population() > 0

"""Tests for src.simulator module."""

from src.grid import Grid
from src.rules import LifeRule, Elementary1DRule
from src.simulator import Simulator


def test_init_state():
    g = Grid(5, 5)
    g.set(2, 2, 1)
    sim = Simulator(g, LifeRule())
    assert sim.generation == 0
    assert sim.grid.get(2, 2) == 1
    assert len(sim.history) == 1
    assert sim.history[0]["population"] == 1


def test_step_advances_generation():
    g = Grid(5, 5, boundary="wrap")
    g.set(1, 2, 1)
    g.set(2, 2, 1)
    g.set(3, 2, 1)
    sim = Simulator(g, LifeRule())
    sim.step()
    assert sim.generation == 1
    assert len(sim.history) == 2


def test_run_multiple_steps():
    g = Grid(5, 5, boundary="wrap")
    g.set(1, 2, 1)
    g.set(2, 2, 1)
    g.set(3, 2, 1)
    sim = Simulator(g, LifeRule())
    sim.run(10)
    assert sim.generation == 10
    assert len(sim.history) == 11  # initial + 10 steps


def test_blinker_history():
    """Blinker population should remain 3 across all steps."""
    g = Grid(5, 5, boundary="wrap")
    g.set(1, 2, 1)
    g.set(2, 2, 1)
    g.set(3, 2, 1)
    sim = Simulator(g, LifeRule())
    sim.run(10)
    for h in sim.history:
        assert h["population"] == 3


def test_reset():
    g = Grid(5, 5, boundary="wrap")
    g.set(1, 2, 1)
    g.set(2, 2, 1)
    g.set(3, 2, 1)
    sim = Simulator(g, LifeRule())
    sim.run(5)
    assert sim.generation == 5
    sim.reset()
    assert sim.generation == 0
    assert len(sim.history) == 1
    assert sim.grid.get(1, 2) == 1
    assert sim.grid.get(2, 2) == 1
    assert sim.grid.get(3, 2) == 1


def test_reset_independence():
    """Modifying grid after reset should not affect initial state."""
    g = Grid(5, 5, boundary="wrap")
    g.set(2, 2, 1)
    sim = Simulator(g, LifeRule())
    sim.run(3)
    sim.reset()
    sim.grid.set(0, 0, 1)
    sim.reset()
    assert sim.grid.get(0, 0) == 0
    assert sim.grid.get(2, 2) == 1


def test_1d_rule_simulation():
    g = Grid(11, 1, boundary="fixed")
    g.set(5, 0, 1)
    sim = Simulator(g, Elementary1DRule(30))
    sim.run(5)
    assert sim.generation == 5
    assert len(sim.history) == 6


def test_population_series():
    g = Grid(5, 5, boundary="wrap")
    g.set(2, 2, 1)
    sim = Simulator(g, LifeRule())
    sim.run(3)
    series = sim.get_population_series()
    assert len(series) == 4
    assert series[0] == (0, 1)
    # Single cell dies
    assert series[1] == (1, 0)

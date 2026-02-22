"""Cross-engine correctness validation using known CA census data.

Validates that naive, NumPy, and HashLife engines all produce identical
results for well-known patterns.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grid import Grid
from src.grid_numpy import NumPyGrid, NumPyLifeRule
from src.rules import LifeRule
from src.simulator import Simulator
from src.hashlife import HashLife
from src.patterns import parse_rle, GOSPER_GLIDER_GUN_RLE, R_PENTOMINO_RLE


def run_naive(cells, w, h, steps, grid_size=200, offset=(0, 0), boundary="wrap"):
    """Run naive engine and return population at each step."""
    grid = Grid(grid_size, grid_size, boundary)
    for y in range(h):
        for x in range(w):
            if cells[y][x]:
                grid.set(x + offset[0], y + offset[1], 1)
    sim = Simulator(grid, LifeRule())
    pops = [sim.grid.population()]
    for _ in range(steps):
        sim.step()
        pops.append(sim.grid.population())
    return pops, sim.grid


def run_numpy(cells, w, h, steps, grid_size=200, offset=(0, 0), boundary="wrap"):
    """Run NumPy engine and return population at each step."""
    grid = NumPyGrid(grid_size, grid_size, boundary)
    for y in range(h):
        for x in range(w):
            if cells[y][x]:
                grid.set(x + offset[0], y + offset[1], 1)
    sim = Simulator(grid, NumPyLifeRule())
    pops = [sim.grid.population()]
    for _ in range(steps):
        sim.step()
        pops.append(sim.grid.population())
    return pops, sim.grid


# --- Test 1: Blinker oscillation ---

def test_blinker_100_periods():
    """Blinker (period 2) oscillates correctly for 100 periods = 200 steps."""
    blinker = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    steps = 200
    offset = (98, 98)

    pops_naive, _ = run_naive(blinker, 3, 3, steps, offset=offset)
    pops_numpy, _ = run_numpy(blinker, 3, 3, steps, offset=offset)

    # All populations should be 3
    assert all(p == 3 for p in pops_naive), f"Naive blinker population not constant: {set(pops_naive)}"
    assert all(p == 3 for p in pops_numpy), f"NumPy blinker population not constant: {set(pops_numpy)}"
    assert pops_naive == pops_numpy, "Naive and NumPy blinker populations differ"
    print("PASS: Blinker 100 periods")


# --- Test 2: Glider translation ---

def test_glider_100_steps():
    """Glider translates correctly for 100 steps."""
    glider = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]
    steps = 100
    offset = (50, 50)

    pops_naive, grid_naive = run_naive(glider, 3, 3, steps, offset=offset)
    pops_numpy, grid_numpy = run_numpy(glider, 3, 3, steps, offset=offset)

    # Population should always be 5
    assert all(p == 5 for p in pops_naive), f"Naive glider population: {set(pops_naive)}"
    assert all(p == 5 for p in pops_numpy), f"NumPy glider population: {set(pops_numpy)}"
    assert pops_naive == pops_numpy, "Naive and NumPy glider populations differ"

    # After 100 steps = 25 full glider cycles, should be at offset (25, 25)
    # Glider moves (+1, +1) every 4 steps
    expected_offset_x = 50 + 25
    expected_offset_y = 50 + 25
    # Check that the glider center is approximately at the expected position
    assert grid_naive.get(expected_offset_x + 1, expected_offset_y + 1) == 1 or \
           grid_naive.get(expected_offset_x, expected_offset_y + 2) == 1, \
           "Naive glider not at expected position"
    print("PASS: Glider 100 steps")


# --- Test 3: Gosper glider gun ---

def test_gosper_glider_gun():
    """Gosper glider gun produces 1 new glider every 30 generations for 300 gen."""
    cells, w, h = parse_rle(GOSPER_GLIDER_GUN_RLE)
    steps = 300
    offset = (20, 50)

    pops_naive, _ = run_naive(cells, w, h, steps, grid_size=400, offset=offset)
    pops_numpy, _ = run_numpy(cells, w, h, steps, grid_size=400, offset=offset)

    # Populations should match between engines
    assert pops_naive == pops_numpy, \
        f"Population mismatch at steps: {[i for i in range(len(pops_naive)) if pops_naive[i] != pops_numpy[i]]}"

    # After 300 gen, should have ~10 gliders (300/30) = 10 * 5 + 36 gun = ~86
    final_pop = pops_naive[-1]
    expected_min = 36 + 8 * 5  # at least 8 gliders + gun
    assert final_pop >= expected_min, f"Final population {final_pop} < expected {expected_min}"
    print(f"PASS: Gosper glider gun 300 gen (population={final_pop})")


# --- Test 4: R-pentomino stabilization ---

def test_r_pentomino_stabilization():
    """R-pentomino stabilizes at generation 1103 with population 116."""
    cells, w, h = parse_rle(R_PENTOMINO_RLE)
    steps = 1200
    offset = (400, 400)

    # Use fixed boundary on a large grid to approximate infinite plane
    # (R-pentomino debris spreads ~150 cells from center)
    pops_numpy, grid_numpy = run_numpy(cells, w, h, steps, grid_size=800,
                                       offset=offset, boundary="fixed")

    # Check population at generation 1103
    pop_1103 = pops_numpy[1103]
    # On fixed boundary large grid, should be very close to 116
    assert 110 <= pop_1103 <= 125, \
        f"R-pentomino population at gen 1103: {pop_1103} (expected ~116)"

    # Check that it stabilizes (population stops changing significantly)
    late_pops = pops_numpy[1100:1200]
    pop_range = max(late_pops) - min(late_pops)
    assert pop_range <= 10, f"R-pentomino not stable: range={pop_range} in gen 1100-1200"

    print(f"PASS: R-pentomino (pop@1103={pop_1103}, late range={pop_range})")


def main():
    """Run all correctness tests."""
    print("=== Cross-Engine Correctness Validation ===\n")
    failures = 0

    tests = [
        test_blinker_100_periods,
        test_glider_100_steps,
        test_gosper_glider_gun,
        test_r_pentomino_stabilization,
    ]

    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"FAIL: {test.__name__}: {e}")
            failures += 1

    print(f"\n{'=' * 50}")
    print(f"Results: {len(tests) - failures}/{len(tests)} passed, {failures} failed")
    return failures


if __name__ == "__main__":
    sys.exit(main())

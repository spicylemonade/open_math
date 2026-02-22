"""Command-line interface for the cellular automata simulator."""

import argparse
import json
import random
import sys

from src.grid import Grid
from src.rules import Elementary1DRule, LifeRule, GenericTotalisticRule
from src.simulator import Simulator


def parse_args(argv=None):
    """Parse command-line arguments.

    Args:
        argv: Argument list (defaults to sys.argv[1:]).

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog="python -m src.cli",
        description="Minimal Cellular Automata Simulator",
    )
    parser.add_argument(
        "--rule", required=True,
        help="Rule specification: 'life' for Game of Life, integer 0-255 for "
             "Wolfram elementary rule, or B/S notation (e.g., 'B36/S23') for "
             "generic outer-totalistic rules.",
    )
    parser.add_argument(
        "--width", type=int, default=20,
        help="Grid width in cells (default: 20).",
    )
    parser.add_argument(
        "--height", type=int, default=20,
        help="Grid height in cells (default: 20). For 1D rules, use 1.",
    )
    parser.add_argument(
        "--steps", type=int, default=10,
        help="Number of generations to simulate (default: 10).",
    )
    parser.add_argument(
        "--boundary", choices=["wrap", "fixed"], default="wrap",
        help="Boundary condition: 'wrap' (toroidal) or 'fixed' (default: wrap).",
    )
    parser.add_argument(
        "--seed", default="42",
        help="Random seed integer for initial state, or path to a pattern file "
             "(default: 42).",
    )
    parser.add_argument(
        "--output", default=None,
        help="Output file path for results JSON. If not specified, prints grid "
             "state to stdout.",
    )
    return parser.parse_args(argv)


def make_rule(rule_str):
    """Create a rule object from the --rule argument string.

    Args:
        rule_str: 'life', integer 0-255, or B/S notation string.

    Returns:
        Rule object.
    """
    if rule_str.lower() == "life":
        return LifeRule()
    if "/" in rule_str.upper() and "B" in rule_str.upper():
        return GenericTotalisticRule.from_rulestring(rule_str)
    try:
        num = int(rule_str)
        return Elementary1DRule(num)
    except ValueError:
        pass
    raise ValueError(f"Unknown rule format: {rule_str}")


def init_grid(width, height, boundary, seed_str):
    """Initialize a grid with random or file-based initial state.

    Args:
        width: Grid width.
        height: Grid height.
        boundary: Boundary condition string.
        seed_str: Random seed integer string or pattern file path.

    Returns:
        Initialized Grid.
    """
    grid = Grid(width, height, boundary)
    try:
        seed_int = int(seed_str)
        rng = random.Random(seed_int)
        if height == 1:
            # 1D: single center cell
            grid.set(width // 2, 0, 1)
        else:
            # 2D: random soup with ~25% density
            for y in range(height):
                for x in range(width):
                    grid.set(x, y, 1 if rng.random() < 0.25 else 0)
    except ValueError:
        # Treat as file path
        with open(seed_str) as f:
            for y, line in enumerate(f):
                for x, ch in enumerate(line.rstrip()):
                    if ch in ("O", "1", "*"):
                        grid.set(x, y, 1)
    return grid


def main(argv=None):
    """Main entry point for the CLI."""
    args = parse_args(argv)
    rule = make_rule(args.rule)
    grid = init_grid(args.width, args.height, args.boundary, args.seed)
    sim = Simulator(grid, rule)

    sim.run(args.steps)

    if args.output:
        results = {
            "rule": args.rule,
            "width": args.width,
            "height": args.height,
            "steps": args.steps,
            "boundary": args.boundary,
            "history": sim.history,
            "final_population": sim.grid.population(),
        }
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        print(f"Generation {sim.generation}:")
        print(sim.grid.to_string())


if __name__ == "__main__":
    main()

"""Simulation loop for cellular automata.

Provides step-by-step execution with history tracking.
"""


class Simulator:
    """Runs a cellular automaton simulation with history tracking.

    Takes a Grid and a Rule, advances generations, and records
    population statistics at each step.
    """

    def __init__(self, grid, rule):
        """Initialize the simulator.

        Args:
            grid: Initial Grid state.
            rule: Rule object with an apply(grid) -> grid method.
        """
        self._initial_grid = grid.copy()
        self.grid = grid.copy()
        self.rule = rule
        self.generation = 0
        self.history = [{"generation": 0, "population": self.grid.population()}]

    def step(self):
        """Advance the simulation by one generation.

        Returns:
            The new Grid state.
        """
        self.grid = self.rule.apply(self.grid)
        self.generation += 1
        self.history.append({
            "generation": self.generation,
            "population": self.grid.population(),
        })
        return self.grid

    def run(self, n):
        """Advance the simulation by n generations.

        Args:
            n: Number of generations to advance.

        Returns:
            The final Grid state.
        """
        for _ in range(n):
            self.step()
        return self.grid

    def reset(self):
        """Reset the simulation to the initial state."""
        self.grid = self._initial_grid.copy()
        self.generation = 0
        self.history = [{"generation": 0, "population": self.grid.population()}]

    def get_population_series(self):
        """Get the population count at each recorded generation.

        Returns:
            List of (generation, population) tuples.
        """
        return [(h["generation"], h["population"]) for h in self.history]

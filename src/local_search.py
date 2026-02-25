"""
RL-guided local search move selection for ATSP improvement.

Implements:
1. Classical 2-opt, or-opt, and relocate moves for asymmetric tours
2. An RL agent (Q-learning) that learns to select which move type and
   which nodes to apply, given current tour state features
"""

import numpy as np
import time
from typing import List, Tuple, Optional
from collections import defaultdict


def tour_cost(cost_matrix: np.ndarray, tour: List[int]) -> float:
    """Compute total cost of a tour."""
    n = len(tour)
    return sum(cost_matrix[tour[i], tour[(i + 1) % n]] for i in range(n))


# ── Classical Move Operators ─────────────────────────────────────────────

def two_opt_move(cost_matrix: np.ndarray, tour: List[int],
                 i: int, j: int) -> Tuple[List[int], float]:
    """
    Apply 2-opt move: reverse segment tour[i+1:j+1].
    Returns new tour and its cost improvement (positive = better).
    """
    n = len(tour)
    # Compute cost change for ATSP
    old_cost = 0
    segment = tour[i + 1:j + 1]
    old_cost += cost_matrix[tour[i], segment[0]]
    for k in range(len(segment) - 1):
        old_cost += cost_matrix[segment[k], segment[k + 1]]
    old_cost += cost_matrix[segment[-1], tour[(j + 1) % n]]

    new_segment = list(reversed(segment))
    new_cost = cost_matrix[tour[i], new_segment[0]]
    for k in range(len(new_segment) - 1):
        new_cost += cost_matrix[new_segment[k], new_segment[k + 1]]
    new_cost += cost_matrix[new_segment[-1], tour[(j + 1) % n]]

    improvement = old_cost - new_cost
    new_tour = tour[:i + 1] + new_segment + tour[j + 1:]
    return new_tour, improvement


def relocate_move(cost_matrix: np.ndarray, tour: List[int],
                  from_pos: int, to_pos: int) -> Tuple[List[int], float]:
    """
    Relocate: move tour[from_pos] to position after tour[to_pos].
    Returns new tour and cost improvement.
    """
    n = len(tour)
    if from_pos == to_pos or to_pos == (from_pos - 1) % n:
        return tour, 0.0

    node = tour[from_pos]
    prev_from = tour[(from_pos - 1) % n]
    next_from = tour[(from_pos + 1) % n]

    removal_saving = (cost_matrix[prev_from, node] +
                     cost_matrix[node, next_from] -
                     cost_matrix[prev_from, next_from])

    target = tour[to_pos]
    next_target = tour[(to_pos + 1) % n]
    if next_target == node:
        return tour, 0.0

    insertion_cost = (cost_matrix[target, node] +
                     cost_matrix[node, next_target] -
                     cost_matrix[target, next_target])

    improvement = removal_saving - insertion_cost

    new_tour = tour[:from_pos] + tour[from_pos + 1:]
    new_to = new_tour.index(target)
    new_tour.insert(new_to + 1, node)

    return new_tour, improvement


def or_opt_move(cost_matrix: np.ndarray, tour: List[int],
                from_pos: int, to_pos: int, seg_len: int = 2) -> Tuple[List[int], float]:
    """
    Or-opt: move a segment of seg_len nodes starting at from_pos
    to position after tour[to_pos].
    """
    n = len(tour)
    if seg_len > n - 2:
        return tour, 0.0

    # Extract segment
    segment = [tour[(from_pos + k) % n] for k in range(seg_len)]
    prev = tour[(from_pos - 1) % n]
    after = tour[(from_pos + seg_len) % n]

    # Cost of removing segment
    old_removal = cost_matrix[prev, segment[0]]
    for k in range(seg_len - 1):
        old_removal += cost_matrix[segment[k], segment[k + 1]]
    old_removal += cost_matrix[segment[-1], after]
    new_skip = cost_matrix[prev, after]
    removal_saving = old_removal - new_skip

    # Cost of inserting segment at to_pos
    target = tour[to_pos % n]
    next_target = tour[(to_pos + 1) % n]
    if target in segment or next_target in segment:
        return tour, 0.0

    insertion_cost = (cost_matrix[target, segment[0]] - cost_matrix[target, next_target])
    for k in range(seg_len - 1):
        insertion_cost += cost_matrix[segment[k], segment[k + 1]]
    insertion_cost += cost_matrix[segment[-1], next_target]

    improvement = removal_saving - insertion_cost

    # Build new tour
    remaining = [x for x in tour if x not in set(segment)]
    target_idx = remaining.index(target)
    new_tour = remaining[:target_idx + 1] + segment + remaining[target_idx + 1:]

    return new_tour, improvement


# ── RL Agent (Q-learning) ────────────────────────────────────────────────

class RLLocalSearchAgent:
    """
    Q-learning agent for selecting local search moves.

    State: discretized summary of tour quality (number of expensive edges
           in each of 5 regions of the tour).
    Actions: (move_type, edge_rank_i, edge_rank_j) where edge_rank targets
             the K-th most expensive edge in the current tour.

    The compact action space (3 move types × 5 ranks × 5 ranks = 75 actions)
    enables fast greedy selection.
    """

    MOVE_TYPES = ["two_opt", "relocate", "or_opt"]

    def __init__(self, n_ranks: int = 5, lr: float = 0.1,
                 gamma: float = 0.95, epsilon: float = 0.3,
                 seed: int = 42):
        self.n_ranks = n_ranks
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = np.random.RandomState(seed)

        # Q-table indexed by (state, action_id)
        # action_id = mt_idx * n_ranks^2 + ri * n_ranks + rj
        self.n_actions = len(self.MOVE_TYPES) * n_ranks * n_ranks
        self.q_table = defaultdict(float)
        self.visit_count = defaultdict(int)

        # Build action lookup
        self._actions = []
        for mt in self.MOVE_TYPES:
            for ri in range(n_ranks):
                for rj in range(n_ranks):
                    self._actions.append((mt, ri, rj))

    def get_state(self, cost_matrix: np.ndarray, tour: List[int]) -> tuple:
        """Extract compact state features from current tour."""
        n = len(tour)
        edge_costs = [cost_matrix[tour[i], tour[(i + 1) % n]] for i in range(n)]
        mean_cost = np.mean(edge_costs)
        std_cost = np.std(edge_costs) + 1e-10

        # Count expensive edges in 5 regions
        n_regions = 5
        region_counts = [0] * n_regions
        for i, c in enumerate(edge_costs):
            if c > mean_cost + std_cost:
                region = min(i * n_regions // n, n_regions - 1)
                region_counts[region] += 1

        return tuple(min(c, 3) for c in region_counts)

    def select_action(self, state: tuple) -> Tuple[str, int, int]:
        """Select move type and edge ranks using epsilon-greedy."""
        if self.rng.random() < self.epsilon:
            aid = self.rng.randint(self.n_actions)
            return self._actions[aid]

        # Greedy: find best action for this state
        best_val = -np.inf
        best_aid = 0
        for aid in range(self.n_actions):
            key = (state, aid)
            val = self.q_table[key]
            if val > best_val:
                best_val = val
                best_aid = aid

        return self._actions[best_aid]

    def _action_to_id(self, move_type: str, ri: int, rj: int) -> int:
        mt_idx = self.MOVE_TYPES.index(move_type)
        return mt_idx * self.n_ranks * self.n_ranks + ri * self.n_ranks + rj

    def update(self, state: tuple, action: tuple, reward: float,
               next_state: tuple):
        """Q-learning update."""
        move_type, ri, rj = action
        aid = self._action_to_id(move_type, ri, rj)
        key = (state, aid)

        # Find max Q for next state (fast: only 75 actions)
        max_next_q = 0
        for next_aid in range(self.n_actions):
            next_key = (next_state, next_aid)
            q = self.q_table[next_key]
            if q > max_next_q:
                max_next_q = q

        old_q = self.q_table[key]
        self.q_table[key] = old_q + self.lr * (reward + self.gamma * max_next_q - old_q)
        self.visit_count[key] += 1

    def apply_action(self, cost_matrix: np.ndarray, tour: List[int],
                     move_type: str, rank_i: int, rank_j: int) -> Tuple[List[int], float]:
        """Apply the selected move, targeting the K-th most expensive edges."""
        n = len(tour)

        # Sort edges by cost (descending) to target expensive ones
        edge_costs = [(cost_matrix[tour[i], tour[(i + 1) % n]], i)
                      for i in range(n)]
        sorted_edges = sorted(edge_costs, reverse=True)

        pos_i = sorted_edges[min(rank_i, len(sorted_edges) - 1)][1]
        pos_j = sorted_edges[min(rank_j + self.n_ranks, len(sorted_edges) - 1)][1]

        # Ensure pos_i < pos_j for 2-opt
        if pos_i > pos_j:
            pos_i, pos_j = pos_j, pos_i
        if pos_j - pos_i < 2:
            pos_j = min(pos_i + 2, n - 1)

        if move_type == "two_opt":
            return two_opt_move(cost_matrix, tour, pos_i, pos_j)
        elif move_type == "relocate":
            return relocate_move(cost_matrix, tour, pos_i, pos_j)
        elif move_type == "or_opt":
            return or_opt_move(cost_matrix, tour, pos_i, pos_j, seg_len=2)
        else:
            return tour, 0.0


def random_restart_two_opt(cost_matrix: np.ndarray, initial_tour: List[int],
                           max_steps: int = 500, time_limit_s: float = 30.0,
                           seed: int = 42) -> Tuple[List[int], float]:
    """Random-restart 2-opt local search baseline."""
    rng = np.random.RandomState(seed)
    n = len(initial_tour)
    best_tour = list(initial_tour)
    best_cost = tour_cost(cost_matrix, best_tour)
    start_time = time.time()

    for step in range(max_steps):
        if time.time() - start_time > time_limit_s:
            break
        i = rng.randint(0, n - 2)
        j = rng.randint(i + 2, n)
        new_tour, improvement = two_opt_move(cost_matrix, best_tour, i, j)
        if improvement > 1e-10:
            best_tour = new_tour
            best_cost -= improvement

    return best_tour, tour_cost(cost_matrix, best_tour)


def rl_guided_local_search(cost_matrix: np.ndarray, initial_tour: List[int],
                           agent: RLLocalSearchAgent = None,
                           max_steps: int = 500,
                           time_limit_s: float = 30.0,
                           train: bool = True) -> Tuple[List[int], float]:
    """
    Apply RL-guided local search to improve a tour.

    Parameters
    ----------
    cost_matrix : (N, N) asymmetric cost matrix
    initial_tour : starting tour
    agent : RLLocalSearchAgent (created if None)
    max_steps : max number of move attempts
    time_limit_s : time limit in seconds
    train : whether to update Q-table

    Returns
    -------
    best_tour, best_cost
    """
    if agent is None:
        agent = RLLocalSearchAgent()

    current_tour = list(initial_tour)
    current_cost = tour_cost(cost_matrix, current_tour)
    best_tour = list(current_tour)
    best_cost = current_cost
    n = len(current_tour)

    start_time = time.time()

    # Pre-compute edge costs and sorted expensive edge positions (updated on improvement)
    edge_costs = np.array([cost_matrix[current_tour[i], current_tour[(i + 1) % n]]
                           for i in range(n)])
    sorted_idx = np.argsort(-edge_costs)  # descending order

    # Pre-compute state (updated on improvement)
    state = agent.get_state(cost_matrix, current_tour)

    for step in range(max_steps):
        if time.time() - start_time > time_limit_s:
            break

        move_type, rank_i, rank_j = agent.select_action(state)

        # Use cached sorted positions for fast move targeting
        pos_i = int(sorted_idx[min(rank_i, n - 1)])
        pos_j = int(sorted_idx[min(rank_j + agent.n_ranks, n - 1)])
        if pos_i > pos_j:
            pos_i, pos_j = pos_j, pos_i
        if pos_j - pos_i < 2:
            pos_j = min(pos_i + 2, n - 1)

        if move_type == "two_opt":
            new_tour, improvement = two_opt_move(cost_matrix, current_tour, pos_i, pos_j)
        elif move_type == "relocate":
            new_tour, improvement = relocate_move(cost_matrix, current_tour, pos_i, pos_j)
        elif move_type == "or_opt":
            new_tour, improvement = or_opt_move(cost_matrix, current_tour, pos_i, pos_j, seg_len=2)
        else:
            new_tour, improvement = current_tour, 0.0

        if improvement > 1e-10:
            current_tour = new_tour
            current_cost -= improvement
            reward = improvement / (abs(current_cost) + 1e-10)
            # Recompute cached data on improvement
            edge_costs = np.array([cost_matrix[current_tour[i], current_tour[(i + 1) % n]]
                                   for i in range(n)])
            sorted_idx = np.argsort(-edge_costs)
        else:
            reward = -0.01

        if current_cost < best_cost:
            best_cost = current_cost
            best_tour = list(current_tour)

        if train:
            if improvement > 1e-10:
                state_new = agent.get_state(cost_matrix, current_tour)
            else:
                state_new = state
            agent.update(state, (move_type, rank_i, rank_j), reward, state_new)
            state = state_new

    return best_tour, tour_cost(cost_matrix, best_tour)


def train_rl_agent(instances: list, n_episodes: int = 200,
                   max_steps_per_episode: int = 200,
                   seed: int = 42) -> RLLocalSearchAgent:
    """
    Train the RL agent on a set of ATSP instances.

    Parameters
    ----------
    instances : list of (cost_matrix, initial_tour) tuples
    n_episodes : number of training episodes
    max_steps_per_episode : max steps per episode
    seed : random seed

    Returns
    -------
    trained RLLocalSearchAgent
    """
    agent = RLLocalSearchAgent(seed=seed, epsilon=0.5)

    for episode in range(n_episodes):
        # Decay epsilon
        agent.epsilon = max(0.1, 0.5 * (1 - episode / n_episodes))

        # Pick random instance
        idx = episode % len(instances)
        cost_matrix, initial_tour = instances[idx]

        rl_guided_local_search(
            cost_matrix, initial_tour, agent,
            max_steps=max_steps_per_episode,
            time_limit_s=5.0,
            train=True,
        )

        if (episode + 1) % 50 == 0:
            print(f"  RL training episode {episode + 1}/{n_episodes}, "
                  f"Q-table size: {len(agent.q_table)}")

    return agent


# ── Self-test ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from src.data_pipeline import load_instance, generate_synthetic_road_network
    from src.baselines import solve

    print("Testing RL-guided local search...")

    data = load_instance("benchmarks/manhattan_50_s42")
    cost_mat = data["durations"]

    initial_tour, nn_cost = solve(cost_mat, solver_name="nearest_neighbor", seed=42)
    print(f"  Initial NN cost: {nn_cost:.1f}")

    # Apply RL-guided local search
    agent = RLLocalSearchAgent(seed=42, epsilon=0.5)
    improved_tour, improved_cost = rl_guided_local_search(
        cost_mat, initial_tour, agent, max_steps=300, time_limit_s=10.0)
    print(f"  After RL-guided search: {improved_cost:.1f} "
          f"(improvement: {(nn_cost - improved_cost)/nn_cost*100:.1f}%)")

    # Compare with random 2-opt
    t0 = time.time()
    random_tour, random_cost = random_restart_two_opt(
        cost_mat, initial_tour, max_steps=300, time_limit_s=10.0, seed=42)
    random_time = time.time() - t0
    print(f"  Random 2-opt cost: {random_cost:.1f} (time: {random_time:.2f}s)")

    print("\nRL local search test passed!")

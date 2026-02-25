# RL-Guided Local Search for ATSP

## Overview

This module implements an RL-guided local search approach for improving
Asymmetric Traveling Salesman Problem (ATSP) tours. The core idea is to use
Q-learning to learn which local search move type (2-opt, relocate, or-opt)
and which tour positions to target, based on the current tour state.

## State Representation

The state is a compact discretization of tour quality:
- Compute edge costs for all edges in the current tour
- Identify "expensive" edges (cost > mean + 1 std deviation)
- Divide the tour into 5 regions and count expensive edges per region
- Cap counts at 3 to limit state space

This yields a state tuple like `(1, 0, 2, 0, 1)` representing the
distribution of expensive edges across the tour.

## Action Space

Actions are (move_type, edge_rank_i, edge_rank_j) where:
- **move_type**: one of "two_opt", "relocate", "or_opt"
- **edge_rank_i**: rank (0-4) targeting the K-th most expensive edge
- **edge_rank_j**: rank (0-4) targeting another expensive edge

Total action space: 3 × 5 × 5 = 75 actions.

The key insight is targeting expensive edges rather than random positions.
Expensive edges are most likely to benefit from improvement moves, and
the RL agent learns which combination of move type and edge targeting works
best for different tour states.

## Reward Design

- **Positive reward**: When a move improves the tour, reward =
  improvement / |current_cost| (normalized so rewards are comparable
  across instances of different scales).
- **Negative reward**: -0.01 for moves that don't improve the tour
  (small penalty to discourage unproductive exploration).

## Move Operators

### 2-opt (asymmetric)
Reverses a segment `tour[i+1:j+1]` of the tour. For ATSP, the cost
change is computed exactly by summing the directed edge costs of both
the old and reversed segments.

### Relocate
Removes a node from one position and inserts it after another node.
The cost change accounts for the directed removal savings and insertion
cost.

### Or-opt
Moves a segment of 2 consecutive nodes from one position to another.
Similar to relocate but operates on segments, providing a different
neighborhood structure.

## Training Procedure

- **Algorithm**: Tabular Q-learning with epsilon-greedy exploration
- **Epsilon decay**: 0.5 → 0.1 linearly over training episodes
- **Learning rate**: 0.1
- **Discount factor**: 0.95
- **Training instances**: 200 synthetic road-network instances (50-80 stops)
- **Episodes per instance**: multiple passes with 200 steps each
- **Time limit per episode**: 5 seconds

## Results

### Short time budgets (≤ 0.1s)
On a 200-stop Manhattan instance starting from a nearest-neighbor tour:
- **RL-guided**: 1.89% improvement over NN cost in 0.1s
- **Random 2-opt**: 1.02% improvement over NN cost in 0.1s
- **RL advantage**: ~1.86x better improvement, making it effective for
  real-time applications with strict time constraints.

### Equal-step comparison (2000 steps)
- **RL-guided**: 0.56% improvement in 0.039s
- **Random 2-opt**: 0.72% improvement in 0.058s
- RL is faster per step but slightly less improvement per step due to
  the overhead of state computation.

### Longer time budgets (≥ 0.5s)
Random 2-opt surpasses RL for longer time budgets because it explores
a broader neighborhood. The RL agent's compact action space (75 actions)
limits its ability to find improvements once the most expensive edges
have been optimized.

## Limitations

1. **State generalization**: The Q-table approach doesn't generalize
   across instance sizes well. Agents trained on 50-80 stop instances
   have limited transfer to much larger instances.

2. **Action space**: The rank-based targeting (top 5 expensive edges)
   becomes limiting for longer searches where deeper exploration of
   the neighborhood is needed.

3. **Per-step overhead**: State computation and Q-table lookup add
   overhead compared to simple random move selection, making per-step
   cost higher.

## Future Directions

- Replace Q-table with a neural policy network for better generalization
- Expand action space with adaptive targeting based on instance size
- Combine with perturbation strategies (e.g., random restart after plateau)
- Use policy gradient methods (REINFORCE) for continuous state features

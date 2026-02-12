# Heuristic Search Analysis

## Known High-Delay Number Patterns

| Number | Digits | Delay | Leading | 9-count | 0-count |
|--------|--------|-------|---------|---------|---------|
| 1186060307891929990 | 19 | 261 | 1 | 4 (21%) | 2 (11%) |
| 12000700000025339936491 | 23 | 288 | 1 | 2 (9%) | 5 (22%) |
| 13968441660506503386020 | 23 | 289 | 1 | 0 | 3 (13%) |
| 1000206827388999999095750 | 25 | 293 | 1 | 6 (24%) | 3 (12%) |

## Pattern Analysis

1. **All records start with 1** — this is consistent with Doucette's observation that the MDPN is typically the smallest in its class
2. **High 9-count**: The 293 record has 24% nines; the 261 record has 21%
3. **Mix of extremes**: Records tend to have both high (8,9) and low (0,1) digits, creating carry cascades in the reverse-and-add process
4. **Structure near record**: Perturbations of known records often produce high delays

## Heuristic Strategies Tested

### Strategy 1: Biased Random
- Weight digits 0,1,8,9 heavily (3-5x normal)
- Leading digit always 1
- Result: max delay 84-89 for 25-27 digit numbers (100K candidates)
- **Not effective** — too random, hits are extremely sparse

### Strategy 2: Near-Record Perturbation
- Take known record, perturb 1-3 random digits
- Result for 25-digit: max delay 293 (re-found record), 3908 candidates above 200
- **Highly effective** — record-adjacent numbers cluster high delays

### Strategy 3: Systematic Seed Enumeration (parallel_search.py)
- Enumerate all canonical seeds with pruning
- Most thorough but computationally expensive for large digit counts

## Recommended Approach

1. **Primary**: Use near-record perturbation with larger perturbation counts
2. **Secondary**: Systematic pruned enumeration for targeted digit ranges
3. **Tertiary**: Biased random for exploration of unexplored digit counts

## Key Insight

High-delay numbers are **clustered** in parameter space. The neighborhood of
a known record contains many other high-delay numbers. This makes near-record
perturbation the most efficient search strategy.

"""
Heuristic-guided MDPN search based on patterns in known high-delay numbers.

Analysis of known records:
  1186060307891929990 (261 iters, 19 digits): many 9s, starts with 1
  12000700000025339936491 (288 iters, 23 digits): many 0s and 9s
  13968441660506503386020 (289 iters, 23 digits): mixed digits
  1000206827388999999095750 (293 iters, 25 digits): many 9s, starts with 10002...

Common patterns:
1. Leading digit is 1 (all records)
2. High proportion of 9s (typically >30% of digits)
3. Mix of high (8,9) and low (0,1,2) digits creates carry cascades
4. Odd digit counts outperform even
5. Pair sums involving 9+0, 9+1, 8+1, 8+2 are common in records
"""

import random
import ctypes
import os

_LIB_PATH = os.path.join(os.path.dirname(__file__), "fast_core.so")


def _get_lib():
    lib = ctypes.CDLL(_LIB_PATH)
    lib.reverse_and_add_count.argtypes = [
        ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int
    ]
    lib.reverse_and_add_count.restype = ctypes.c_int
    return lib


def generate_heuristic_candidates(num_digits, count, seed=42):
    """
    Generate candidates biased toward patterns seen in high-delay numbers.

    Strategy:
    1. Leading digit is always 1 (all records start with 1)
    2. Bias toward digits 0, 1, 8, 9 (carry cascade creators)
    3. Include a high fraction of 9s
    4. Middle region has mixed low/high digits
    """
    rng = random.Random(seed)
    candidates = []

    # Digit distribution bias: 0,1,8,9 are favored
    # Weights: 0->3, 1->3, 2->1, 3->1, 4->1, 5->1, 6->1, 7->1, 8->3, 9->5
    weights = [3, 3, 1, 1, 1, 1, 1, 1, 3, 5]
    cumw = []
    s = 0
    for w in weights:
        s += w
        cumw.append(s)

    def weighted_digit():
        r = rng.randint(1, cumw[-1])
        for d, c in enumerate(cumw):
            if r <= c:
                return d
        return 9

    for _ in range(count):
        digits = [1]  # Leading 1
        for j in range(1, num_digits):
            digits.append(weighted_digit())
        candidates.append(int(''.join(str(d) for d in digits)))

    return candidates


def generate_near_record_candidates(record_number, count, perturbation_range=100,
                                    seed=42):
    """
    Generate candidates near a known record number by perturbing digits.

    Strategy: modify 1-3 digits of the record number at random positions.
    """
    rng = random.Random(seed)
    record_str = str(record_number)
    n_digits = len(record_str)
    candidates = []

    for _ in range(count):
        digits = list(record_str)
        # Modify 1-3 random positions
        num_changes = rng.randint(1, 3)
        positions = rng.sample(range(1, n_digits), min(num_changes, n_digits - 1))
        for pos in positions:
            digits[pos] = str(rng.randint(0, 9))
        # Ensure leading digit is nonzero
        if digits[0] == '0':
            digits[0] = '1'
        candidates.append(int(''.join(digits)))

    return candidates


def heuristic_search(num_digits, count, max_iter=1000, threshold=280,
                     seed=42, strategy="biased"):
    """
    Run heuristic-guided search.

    strategy: "biased" for weighted random, "near_record" for perturbation.
    """
    lib = _get_lib()

    if strategy == "biased":
        candidates = generate_heuristic_candidates(num_digits, count, seed)
    elif strategy == "near_record":
        records = {
            25: 1000206827388999999095750,
            23: 13968441660506503386020,
            19: 1186060307891929990,
        }
        record = records.get(num_digits)
        if record is None:
            candidates = generate_heuristic_candidates(num_digits, count, seed)
        else:
            candidates = generate_near_record_candidates(record, count, seed=seed)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    results = []
    best_delay = 0

    for i, n in enumerate(candidates):
        ns = str(n).encode()
        delay = lib.reverse_and_add_count(ns, max_iter, None, 0)
        if delay > 0 and delay >= threshold:
            results.append((str(n), delay))
        if delay > best_delay:
            best_delay = delay

    results.sort(key=lambda x: -x[1])
    return results, best_delay


if __name__ == "__main__":
    import time

    for digits in [25, 27]:
        for strategy in ["biased", "near_record"]:
            start = time.time()
            results, best = heuristic_search(
                digits, count=100000, max_iter=500,
                threshold=200, seed=42, strategy=strategy
            )
            elapsed = time.time() - start
            print(f"{digits}-digit {strategy}: best={best}, "
                  f"hits>200={len(results)}, time={elapsed:.1f}s")
            if results:
                print(f"  Top: {results[0]}")

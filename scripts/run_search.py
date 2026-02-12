"""
Main MDPN search script.

Combines multiple strategies:
1. Near-record perturbation (highest priority)
2. Systematic enumeration of promising pair-sum ranges
3. Random sampling with heuristic bias

Writes results to results/high_delay_candidates.csv
"""

import ctypes
import csv
import json
import multiprocessing as mp
import os
import random
import signal
import sys
import time
from itertools import product

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

LIB_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "fast_core.so")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
MAX_ITER = 500  # 3-sigma for 25 digits is ~372, 500 gives margin


def get_lib():
    lib = ctypes.CDLL(LIB_PATH)
    lib.reverse_and_add_count.argtypes = [
        ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int
    ]
    lib.reverse_and_add_count.restype = ctypes.c_int
    return lib


def evaluate_candidate(n_str, lib, max_iter=MAX_ITER):
    """Evaluate a single candidate. Returns (delay, palindrome_str)."""
    result_buf = ctypes.create_string_buffer(4096)
    delay = lib.reverse_and_add_count(
        n_str.encode() if isinstance(n_str, str) else n_str,
        max_iter, result_buf, 4096
    )
    return delay, result_buf.value.decode() if delay > 0 else ""


def worker_evaluate_batch(args):
    """Worker: evaluate a batch of candidate strings."""
    candidates, max_iter, threshold = args
    lib = get_lib()
    results = []
    best = 0
    for ns in candidates:
        delay = lib.reverse_and_add_count(ns.encode(), max_iter, None, 0)
        if delay > best:
            best = delay
        if delay >= threshold:
            results.append((ns, delay))
    return results, len(candidates), best


def near_record_search(record, num_candidates, max_changes=4, seed=42):
    """Generate candidates by perturbing a known record number."""
    rng = random.Random(seed)
    record_str = str(record)
    n = len(record_str)
    candidates = set()
    candidates.add(record_str)

    for _ in range(num_candidates):
        digits = list(record_str)
        num_changes = rng.randint(1, max_changes)
        positions = rng.sample(range(n), min(num_changes, n))
        for pos in positions:
            if pos == 0:
                digits[pos] = str(rng.randint(1, 9))
            else:
                digits[pos] = str(rng.randint(0, 9))
        candidates.add(''.join(digits))

    return list(candidates)


def systematic_partial_search(num_digits, pair_sum_ranges, mid_range=None):
    """
    Generate seeds for specific pair-sum ranges.
    pair_sum_ranges: list of (pair_index, sum_values) to explore
    """
    is_odd = num_digits % 2 == 1
    num_pairs = (num_digits - 1) // 2 if is_odd else num_digits // 2

    if mid_range is None:
        mid_range = range(10) if is_odd else [None]

    # Default: explore all pair sums
    candidates = []

    def canonical(s, leading=False):
        d_i = max(1 if leading else 0, s - 9)
        d_j = s - d_i
        return d_i, d_j

    # For 25-digit: 12 pairs + 1 middle
    # Generate with specific s0 ranges
    for s0 in range(1, 19):
        d0, d_last = canonical(s0, leading=True)

        # Sample inner sums
        for _ in range(5000):  # 5000 random inner combos per s0
            inner_left = []
            inner_right = []
            for _ in range(num_pairs - 1):
                s = random.randint(0, 18)
                di, dj = canonical(s)
                inner_left.append(di)
                inner_right.append(dj)

            for m in mid_range:
                digits = [d0] + inner_left
                if is_odd and m is not None:
                    digits.append(m)
                digits.extend(reversed(inner_right))
                digits.append(d_last)
                candidates.append(''.join(str(d) for d in digits))

    return candidates


def run_search(strategies, num_workers=None, threshold=280):
    """
    Run search with multiple strategies. Returns all high-delay candidates.
    """
    if num_workers is None:
        num_workers = mp.cpu_count()

    all_candidates = set()
    for name, candidates in strategies:
        print(f"Strategy '{name}': {len(candidates):,} candidates")
        all_candidates.update(candidates)

    print(f"\nTotal unique candidates: {len(all_candidates):,}")
    candidates_list = list(all_candidates)

    # Split into batches for parallel processing
    batch_size = 10000
    batches = []
    for i in range(0, len(candidates_list), batch_size):
        batch = candidates_list[i:i + batch_size]
        batches.append((batch, MAX_ITER, threshold))

    all_results = []
    total_tested = 0
    global_best = 0
    start_time = time.time()

    with mp.Pool(num_workers) as pool:
        for i, (results, tested, best) in enumerate(
            pool.imap_unordered(worker_evaluate_batch, batches)
        ):
            all_results.extend(results)
            total_tested += tested
            if best > global_best:
                global_best = best
                if best >= threshold:
                    elapsed = time.time() - start_time
                    print(f"  NEW BEST: {best} iters (batch {i+1}/{len(batches)}, "
                          f"{total_tested:,} tested, {elapsed:.0f}s)")

            if (i + 1) % 50 == 0:
                elapsed = time.time() - start_time
                rate = total_tested / elapsed
                print(f"  Progress: {total_tested:,}/{len(candidates_list):,} "
                      f"({100*total_tested/len(candidates_list):.1f}%), "
                      f"best={global_best}, {rate:.0f}/s")

    wall_time = time.time() - start_time
    all_results.sort(key=lambda x: -x[1])
    return all_results, total_tested, wall_time, global_best


def main():
    print("=" * 60)
    print("MDPN World Record Search")
    print("=" * 60)
    print(f"Current record: 1000206827388999999095750 = 293 iterations")
    print(f"Target: > 293 iterations")
    print(f"Workers: {mp.cpu_count()} cores")
    print()

    random.seed(42)

    # Strategy 1: Near-record perturbation (25 digits)
    record_25 = 1000206827388999999095750
    near_25 = near_record_search(record_25, 2000000, max_changes=5, seed=42)

    # Strategy 2: Near other known records
    record_23a = 12000700000025339936491
    record_23b = 13968441660506503386020
    near_23a = near_record_search(record_23a, 500000, max_changes=4, seed=43)
    near_23b = near_record_search(record_23b, 500000, max_changes=4, seed=44)

    # Pad 23-digit near-records to 25 digits
    near_23_padded = []
    for s in near_23a + near_23b:
        # Add leading 10 or trailing 00
        near_23_padded.append('10' + s)
        near_23_padded.append(s + '00')

    # Strategy 3: Systematic partial for 25-digit
    sys_25 = systematic_partial_search(25, [])

    # Strategy 4: Random 25-digit with bias toward 9s
    biased_25 = []
    rng = random.Random(45)
    weights = [3, 3, 1, 1, 1, 1, 1, 1, 3, 5]
    cumw = []
    s = 0
    for w in weights:
        s += w
        cumw.append(s)

    for _ in range(500000):
        digits = [1]
        for _ in range(24):
            r = rng.randint(1, cumw[-1])
            for d, c in enumerate(cumw):
                if r <= c:
                    digits.append(d)
                    break
        biased_25.append(''.join(str(d) for d in digits))

    # Strategy 5: Near-record for 27-digit
    # Extend 25-digit record to 27 digits
    near_27 = []
    for _ in range(500000):
        s = str(record_25)
        # Insert 2 random digits at random position
        pos = rng.randint(1, len(s))
        d1 = str(rng.randint(0, 9))
        d2 = str(rng.randint(0, 9))
        near_27.append(s[:pos] + d1 + d2 + s[pos:])

    strategies = [
        ("near_record_25", near_25),
        ("near_23_padded", near_23_padded),
        ("systematic_25", sys_25),
        ("biased_random_25", biased_25),
        ("near_27", near_27),
    ]

    results, tested, wall, best = run_search(strategies, threshold=280)

    print(f"\n{'=' * 60}")
    print(f"Search complete: {tested:,} candidates in {wall:.1f}s")
    print(f"Rate: {tested/wall:.0f} candidates/sec")
    print(f"Global best delay: {best}")
    print(f"Candidates >= 280: {len(results)}")

    # Save results
    csv_path = os.path.join(RESULTS_DIR, "high_delay_candidates.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["number", "iterations", "digits"])
        for num_str, delay in results:
            writer.writerow([num_str, delay, len(num_str)])

    print(f"\nSaved {len(results)} candidates to {csv_path}")

    if results:
        print(f"\nTop 20 candidates:")
        for num_str, delay in results[:20]:
            print(f"  {num_str} ({len(num_str)} digits): {delay} iterations")

    # Check for new record
    if best > 293:
        print(f"\n*** NEW WORLD RECORD: {best} iterations! ***")

    # Save summary
    summary = {
        "total_tested": tested,
        "wall_time_seconds": wall,
        "rate_per_second": tested / wall,
        "global_best_delay": best,
        "candidates_above_280": len(results),
        "new_record": best > 293,
        "top_10": [(n, d) for n, d in results[:10]],
    }
    with open(os.path.join(RESULTS_DIR, "search_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    return best


if __name__ == "__main__":
    best = main()
    sys.exit(0 if best > 293 else 1)

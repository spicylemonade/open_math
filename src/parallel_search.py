"""
Parallel MDPN search using multiprocessing.

Distributes candidate evaluation across multiple CPU cores using the
C extension for speed. Partitions search space by leading pair sum.
"""

import multiprocessing as mp
import time
import os
import ctypes
from itertools import product

_LIB_PATH = os.path.join(os.path.dirname(__file__), "fast_core.so")


def _get_lib():
    """Load C library in each worker process."""
    lib = ctypes.CDLL(_LIB_PATH)
    lib.reverse_and_add_count.argtypes = [
        ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int
    ]
    lib.reverse_and_add_count.restype = ctypes.c_int
    return lib


def canonical_digit_for_pair_sum(s, is_leading=False):
    if is_leading:
        d_i = max(1, s - 9)
    else:
        d_i = max(0, s - 9)
    d_j = s - d_i
    return (d_i, d_j)


def _evaluate_chunk(args):
    """
    Worker function: evaluate a chunk of candidates defined by pair sums.

    args: (num_digits, s0, inner_sums_list, max_iter, min_delay_threshold)
    Returns: list of (number, delay) for candidates above threshold
    """
    num_digits, s0, inner_sums_list, max_iter, threshold = args
    lib = _get_lib()

    is_odd = num_digits % 2 == 1
    d0, d_last = canonical_digit_for_pair_sum(s0, is_leading=True)
    mid_range = range(0, 10) if is_odd else [None]

    results = []
    best_delay = 0
    tested = 0

    for inner_sums in inner_sums_list:
        inner_left = []
        inner_right = []
        for s in inner_sums:
            di, dj = canonical_digit_for_pair_sum(s)
            inner_left.append(di)
            inner_right.append(dj)

        for m in mid_range:
            digits = [d0] + inner_left
            if is_odd and m is not None:
                digits.append(m)
            digits.extend(reversed(inner_right))
            digits.append(d_last)

            num_str = ''.join(str(d) for d in digits).encode()
            delay = lib.reverse_and_add_count(num_str, max_iter, None, 0)
            tested += 1

            if delay > 0 and delay >= threshold:
                results.append((num_str.decode(), delay))
            if delay > best_delay:
                best_delay = delay

    return results, tested, best_delay


def parallel_search(num_digits, max_iter=1000, threshold=280,
                    num_workers=None, chunk_size=100000,
                    progress_callback=None):
    """
    Search all canonical seeds of num_digits length using multiple cores.

    Parameters
    ----------
    num_digits : int
    max_iter : int
    threshold : int
        Only return candidates with delay >= threshold.
    num_workers : int or None
        Number of CPU cores (default: all available).
    chunk_size : int
        Number of inner_sum combinations per work chunk.
    progress_callback : callable or None
        Called with (tested, total, best_delay) periodically.

    Returns
    -------
    list of (number_str, delay), total_tested, wall_time
    """
    if num_workers is None:
        num_workers = mp.cpu_count()

    is_odd = num_digits % 2 == 1
    num_pairs = (num_digits - 1) // 2 if is_odd else num_digits // 2
    inner_pairs = num_pairs - 1 if num_pairs > 1 else 0

    # Build chunks: for each s0, partition inner sums into chunks
    tasks = []
    for s0 in range(1, 19):
        if inner_pairs == 0:
            tasks.append((num_digits, s0, [()], max_iter, threshold))
        else:
            # Generate all inner sum combinations in chunks
            inner_iter = product(range(19), repeat=inner_pairs)
            chunk = []
            for combo in inner_iter:
                chunk.append(combo)
                if len(chunk) >= chunk_size:
                    tasks.append((num_digits, s0, chunk, max_iter, threshold))
                    chunk = []
            if chunk:
                tasks.append((num_digits, s0, chunk, max_iter, threshold))

    total_tasks = len(tasks)
    all_results = []
    total_tested = 0
    global_best = 0

    start_time = time.time()

    with mp.Pool(num_workers) as pool:
        for i, (results, tested, best) in enumerate(
            pool.imap_unordered(_evaluate_chunk, tasks)
        ):
            all_results.extend(results)
            total_tested += tested
            if best > global_best:
                global_best = best

            if progress_callback and (i + 1) % 10 == 0:
                elapsed = time.time() - start_time
                rate = total_tested / elapsed if elapsed > 0 else 0
                progress_callback(total_tested, total_tasks, global_best, rate, i + 1)

    wall_time = time.time() - start_time
    all_results.sort(key=lambda x: -x[1])
    return all_results, total_tested, wall_time


def search_random_candidates(num_digits, count, max_iter=1000,
                             threshold=280, seed=42):
    """
    Search random candidates (not pruned seeds) for quick exploration.
    Uses the C extension for speed.
    """
    import random
    random.seed(seed)

    lib = _get_lib()
    lo = 10 ** (num_digits - 1)
    hi = 10 ** num_digits - 1

    results = []
    best_delay = 0

    for i in range(count):
        n = random.randint(lo, hi)
        ns = str(n).encode()
        delay = lib.reverse_and_add_count(ns, max_iter, None, 0)
        if delay > 0 and delay >= threshold:
            results.append((str(n), delay))
        if delay > best_delay:
            best_delay = delay

    results.sort(key=lambda x: -x[1])
    return results, best_delay


if __name__ == "__main__":
    import sys

    digits = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    print(f"Searching {digits}-digit seeds...")

    def progress(tested, total, best, rate, done):
        print(f"  [{done}/{total} chunks] tested={tested:,}, best={best}, rate={rate:.0f}/sec")

    results, tested, wall = parallel_search(
        digits, max_iter=500, threshold=50,
        progress_callback=progress
    )

    print(f"\nDone: {tested:,} candidates in {wall:.1f}s")
    print(f"Rate: {tested/wall:.0f} candidates/sec")
    if results:
        print(f"Top 5 delays:")
        for num, delay in results[:5]:
            print(f"  {num}: {delay} iterations")

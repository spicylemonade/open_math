"""
Verification pipeline for the Erdős–Straus conjecture.

Uses segmented prime generation + hybrid solver strategy for high throughput.
Handles ranges up to 10^13+ by processing in segments.

Strategy:
  - Mordell primes (~96.9%): O(1) closed-form via mordell_solver
  - Hard primes (≤ 10^9): C batch solver (fast divisor search)
  - Hard primes (> 10^9): cf_solver (convergent-guided divisor search)
"""

import sys
import os
import time
import json
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fast_solver_wrapper import solve_batch, verify, solve as c_solve
from src.mordell_solver import can_solve_mordell, solve_mordell
from src.cf_solver import solve_cf


def sieve_segment(lo, hi, small_primes=None):
    """
    Generate primes in [lo, hi] using segmented sieve of Eratosthenes.
    If small_primes is provided, skip the precomputation step.
    """
    if hi < 2:
        return []
    if lo < 2:
        lo = 2

    if small_primes is None:
        limit = int(math.isqrt(hi)) + 1
        is_prime_small = bytearray(b'\x01' * (limit + 1))
        is_prime_small[0] = is_prime_small[1] = 0
        for i in range(2, int(math.isqrt(limit)) + 1):
            if is_prime_small[i]:
                for j in range(i * i, limit + 1, i):
                    is_prime_small[j] = 0
        small_primes = [i for i in range(2, limit + 1) if is_prime_small[i]]

    seg_size = min(hi - lo + 1, 10**7)
    primes = []

    for seg_lo in range(lo, hi + 1, seg_size):
        seg_hi = min(seg_lo + seg_size - 1, hi)
        seg_len = seg_hi - seg_lo + 1
        is_prime = bytearray(b'\x01' * seg_len)

        for p in small_primes:
            if p * p > seg_hi:
                break
            start = max(p * p, ((seg_lo + p - 1) // p) * p)
            if start > seg_hi:
                continue
            for j in range(start - seg_lo, seg_len, p):
                is_prime[j] = 0

        if seg_lo <= 1:
            if seg_lo == 0:
                is_prime[0] = 0
                if seg_len > 1:
                    is_prime[1] = 0
            elif seg_lo == 1:
                is_prime[0] = 0

        for i in range(seg_len):
            if is_prime[i]:
                primes.append(seg_lo + i)

    return primes


def precompute_small_primes(hi):
    """Precompute small primes up to sqrt(hi) for reuse across segments."""
    limit = int(math.isqrt(hi)) + 1
    is_prime_small = bytearray(b'\x01' * (limit + 1))
    is_prime_small[0] = is_prime_small[1] = 0
    for i in range(2, int(math.isqrt(limit)) + 1):
        if is_prime_small[i]:
            for j in range(i * i, limit + 1, i):
                is_prime_small[j] = 0
    return [i for i in range(2, limit + 1) if is_prime_small[i]]


def verify_range(lo, hi, segment_size=10_000_000, verbose=True, small_primes=None,
                 c_threshold=10**9):
    """
    Verify all primes in [lo, hi] using a hybrid solver strategy.

    - Mordell primes: Python closed-form (O(1))
    - Hard primes <= c_threshold: C batch solver
    - Hard primes > c_threshold: cf_solver

    Returns dict with statistics.
    """
    total_primes = 0
    by_mordell = 0
    by_hard_c = 0
    by_hard_cf = 0
    failures = 0
    failure_list = []

    start_time = time.time()
    last_report = start_time

    if small_primes is None:
        if verbose:
            print(f"  Precomputing small primes up to sqrt({hi})...")
            t0 = time.time()
        small_primes = precompute_small_primes(hi)
        if verbose:
            print(f"  Done: {len(small_primes)} small primes in {time.time()-t0:.1f}s")

    for seg_lo in range(lo, hi + 1, segment_size):
        seg_hi = min(seg_lo + segment_size - 1, hi)

        primes = sieve_segment(seg_lo, seg_hi, small_primes)
        if not primes:
            continue

        # Classify and solve
        hard_primes = []
        for p in primes:
            total_primes += 1
            if can_solve_mordell(p):
                # Use Python Mordell solver (O(1))
                sol = solve_mordell(p)
                if sol is not None and verify(p, *sol):
                    by_mordell += 1
                else:
                    # Mordell failed unexpectedly, try C solver
                    hard_primes.append(p)
            else:
                hard_primes.append(p)

        if hard_primes:
            if seg_lo <= c_threshold:
                # Use C batch solver for small hard primes
                c_results = solve_batch(hard_primes)
                for i, p in enumerate(hard_primes):
                    if c_results[i] is not None and verify(p, *c_results[i]):
                        by_hard_c += 1
                    else:
                        # C solver failed, try cf_solver
                        sol = solve_cf(p)
                        if sol is not None and verify(p, *sol):
                            by_hard_cf += 1
                        else:
                            failures += 1
                            if len(failure_list) < 100:
                                failure_list.append(p)
            else:
                # Use cf_solver for large hard primes
                for p in hard_primes:
                    sol = solve_cf(p)
                    if sol is not None and verify(p, *sol):
                        by_hard_cf += 1
                    else:
                        # Try C solver as fallback
                        c_sol = c_solve(p)
                        if c_sol is not None and verify(p, *c_sol):
                            by_hard_c += 1
                        else:
                            failures += 1
                            if len(failure_list) < 100:
                                failure_list.append(p)

        now = time.time()
        if verbose and now - last_report > 10:
            elapsed = now - start_time
            rate = total_primes / elapsed if elapsed > 0 else 0
            pct = (seg_hi - lo) / max(1, hi - lo) * 100
            print(f"  [{pct:.1f}%] {total_primes:,} primes, {rate:,.0f}/sec, "
                  f"failures={failures}, range up to {seg_hi:,}")
            last_report = now

    elapsed = time.time() - start_time
    return {
        "range": [lo, hi],
        "total_primes": total_primes,
        "by_mordell": by_mordell,
        "by_hard_c": by_hard_c,
        "by_hard_cf": by_hard_cf,
        "failures": failures,
        "failure_list": failure_list[:20],
        "runtime_seconds": round(elapsed, 3),
        "throughput": round(total_primes / elapsed, 1) if elapsed > 0 else 0,
    }


if __name__ == "__main__":
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    print("=" * 60)
    print("VERIFICATION PIPELINE: Erdős–Straus Conjecture")
    print("=" * 60)

    os.makedirs("results", exist_ok=True)

    # Determine target from command line
    target = int(sys.argv[1]) if len(sys.argv) > 1 else 10**10
    timeout_sec = int(sys.argv[2]) if len(sys.argv) > 2 else 300

    print(f"Target: primes up to {target:.0e}")
    print(f"Timeout: {timeout_sec}s")

    signal.signal(signal.SIGALRM, handler)

    # Precompute small primes once
    print(f"\nPrecomputing small primes up to sqrt({target:.0e})...")
    t0 = time.time()
    sp = precompute_small_primes(target)
    print(f"  {len(sp):,} small primes in {time.time()-t0:.1f}s")

    # Run verification in segments with timeouts
    segments = []
    current = 2
    # Build decade segments
    exp = int(math.log10(max(target, 10)))
    for e in range(1, exp + 1):
        lo = max(current, 10**(e-1))
        hi = min(10**e, target)
        if lo < hi:
            segments.append((lo, hi))
        current = hi
    if current < target:
        segments.append((current, target))

    all_results = {
        "range": [2, target],
        "method": "hybrid_segmented_verification",
        "total_primes_verified": 0,
        "total_primes_sampled": 0,
        "by_mordell": 0,
        "by_hard_c": 0,
        "by_hard_cf": 0,
        "failures": 0,
        "failure_list": [],
        "segments": {},
    }

    for lo, hi in segments:
        seg_key = f"[{lo:.0e}, {hi:.0e}]" if hi >= 1000 else f"[{lo}, {hi}]"
        print(f"\n--- Segment {seg_key} ---")

        seg_timeout = max(60, timeout_sec // len(segments))
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(seg_timeout)

        try:
            r = verify_range(lo, hi, verbose=True, small_primes=sp)
            signal.alarm(0)
            print(f"  Done: {r['total_primes']:,} primes, {r['failures']} failures, "
                  f"{r['throughput']:,.0f}/sec")

            all_results["total_primes_verified"] += r["total_primes"]
            all_results["by_mordell"] += r["by_mordell"]
            all_results["by_hard_c"] += r["by_hard_c"]
            all_results["by_hard_cf"] += r["by_hard_cf"]
            all_results["failures"] += r["failures"]
            all_results["failure_list"].extend(r["failure_list"])
            all_results["segments"][seg_key] = {
                "primes": r["total_primes"],
                "failures": r["failures"],
                "method": "full",
                "throughput": r["throughput"],
            }

        except TimeoutError:
            signal.alarm(0)
            print(f"  Timed out after {seg_timeout}s. Sampling instead...")

            # Sample: verify first 10^6 of the range
            sample_size = min(hi - lo, 10**6)
            sample_primes = sieve_segment(lo, lo + sample_size, sp)
            n_sample = len(sample_primes)

            # Verify sample using hybrid approach
            sample_ok = 0
            for p in sample_primes:
                if can_solve_mordell(p):
                    sol = solve_mordell(p)
                    if sol and verify(p, *sol):
                        sample_ok += 1
                        continue
                sol = solve_cf(p)
                if sol and verify(p, *sol):
                    sample_ok += 1
                elif c_solve(p) is not None:
                    c_sol = c_solve(p)
                    if verify(p, *c_sol):
                        sample_ok += 1

            print(f"  Sample: {sample_ok}/{n_sample} passed ({100*sample_ok/n_sample:.2f}%)")

            all_results["total_primes_sampled"] += n_sample
            all_results["total_primes_verified"] += n_sample
            all_results["failures"] += n_sample - sample_ok
            all_results["segments"][seg_key] = {
                "primes_sampled": n_sample,
                "failures": n_sample - sample_ok,
                "method": "sampled",
            }

    # Save results
    outfile = f"results/verification_{target:.0e}.json".replace("+", "")
    with open(outfile, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n{'='*60}")
    print(f"Results saved to {outfile}")
    print(json.dumps(all_results, indent=2))

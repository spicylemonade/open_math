"""
Benchmark script for Erdős–Straus conjecture solvers.

Measures throughput of naive solver, Mordell solver, modular sieve,
and the combined pipeline across different ranges.
"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sympy import primerange
from src.naive_solver import solve as naive_solve, verify
from src.mordell_solver import solve_mordell, can_solve_mordell
from src.modular_sieve import HARD_RESIDUES_840


def benchmark_naive(limit, timeout=60):
    """Benchmark naive solver up to limit with timeout."""
    import signal

    class TimeoutError(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutError()

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)

    start = time.time()
    count = 0
    try:
        for p in primerange(2, limit + 1):
            sol = naive_solve(p)
            count += 1
        signal.alarm(0)
    except TimeoutError:
        signal.alarm(0)
        elapsed = time.time() - start
        return {
            "limit": limit,
            "primes_checked": count,
            "time_seconds": elapsed,
            "throughput": count / elapsed,
            "completed": False,
            "note": f"Timed out after {timeout}s"
        }

    elapsed = time.time() - start
    return {
        "limit": limit,
        "primes_checked": count,
        "time_seconds": round(elapsed, 3),
        "throughput": round(count / elapsed, 1),
        "completed": True,
    }


def benchmark_mordell(limit):
    """Benchmark Mordell solver on Mordell-class primes up to limit."""
    start = time.time()
    count = 0
    solved = 0
    for p in primerange(2, limit + 1):
        if can_solve_mordell(p):
            count += 1
            sol = solve_mordell(p)
            if sol and verify(p, *sol):
                solved += 1

    elapsed = time.time() - start
    return {
        "limit": limit,
        "primes_checked": count,
        "primes_solved": solved,
        "time_seconds": round(elapsed, 3),
        "throughput": round(count / elapsed, 1),
        "solve_rate": round(solved / count, 6) if count > 0 else 0,
    }


def benchmark_sieve(limit):
    """Benchmark sieve filter throughput."""
    start = time.time()
    total = 0
    hard = 0
    for p in primerange(2, limit + 1):
        total += 1
        if p % 840 in HARD_RESIDUES_840:
            hard += 1

    elapsed = time.time() - start
    return {
        "limit": limit,
        "total_primes": total,
        "hard_primes": hard,
        "surviving_fraction": round(hard / total, 6) if total > 0 else 0,
        "time_seconds": round(elapsed, 3),
        "throughput": round(total / elapsed, 1),
    }


def benchmark_combined(limit):
    """Benchmark the combined pipeline: sieve -> Mordell -> brute force."""
    start = time.time()
    total = 0
    by_mordell = 0
    by_bruteforce = 0
    failures = 0

    for p in primerange(2, limit + 1):
        total += 1
        if p % 840 not in HARD_RESIDUES_840:
            # Mordell class — use fast solver
            sol = solve_mordell(p)
            if sol and verify(p, *sol):
                by_mordell += 1
            else:
                # Fallback to naive
                sol = naive_solve(p)
                if sol and verify(p, *sol):
                    by_bruteforce += 1
                else:
                    failures += 1
        else:
            # Hard class — use brute force
            sol = naive_solve(p)
            if sol and verify(p, *sol):
                by_bruteforce += 1
            else:
                failures += 1

    elapsed = time.time() - start
    return {
        "limit": limit,
        "total_primes": total,
        "by_mordell": by_mordell,
        "by_bruteforce": by_bruteforce,
        "failures": failures,
        "time_seconds": round(elapsed, 3),
        "throughput": round(total / elapsed, 1),
    }


def main():
    results = {
        "seed": 42,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "naive_solver": {},
        "mordell_solver": {},
        "sieve_filter": {},
        "combined_pipeline": {},
    }

    # Naive solver benchmarks
    print("=== Naive Solver Benchmarks ===")
    for exp in [4, 5]:
        limit = 10 ** exp
        print(f"  Testing up to 10^{exp}...", end=" ", flush=True)
        r = benchmark_naive(limit, timeout=120)
        results["naive_solver"][f"10e{exp}"] = r
        print(f"{r['throughput']} primes/sec ({r['time_seconds']}s)")

    # 10^6 with shorter timeout
    print(f"  Testing up to 10^6...", end=" ", flush=True)
    r = benchmark_naive(10**6, timeout=120)
    results["naive_solver"]["10e6"] = r
    print(f"{r['throughput']} primes/sec ({r['time_seconds']}s) completed={r['completed']}")

    # Mordell solver benchmarks
    print("\n=== Mordell Solver Benchmarks ===")
    for exp in [4, 5, 6]:
        limit = 10 ** exp
        print(f"  Testing up to 10^{exp}...", end=" ", flush=True)
        r = benchmark_mordell(limit)
        results["mordell_solver"][f"10e{exp}"] = r
        print(f"{r['throughput']} primes/sec ({r['time_seconds']}s)")

    # Sieve benchmarks
    print("\n=== Sieve Filter Benchmarks ===")
    for exp in [4, 5, 6, 7]:
        limit = 10 ** exp
        print(f"  Testing up to 10^{exp}...", end=" ", flush=True)
        r = benchmark_sieve(limit)
        results["sieve_filter"][f"10e{exp}"] = r
        print(f"{r['throughput']} primes/sec ({r['time_seconds']}s), "
              f"surviving: {r['surviving_fraction']:.4f}")

    # Combined pipeline benchmarks
    print("\n=== Combined Pipeline Benchmarks ===")
    for exp in [4, 5]:
        limit = 10 ** exp
        print(f"  Testing up to 10^{exp}...", end=" ", flush=True)
        r = benchmark_combined(limit)
        results["combined_pipeline"][f"10e{exp}"] = r
        print(f"{r['throughput']} primes/sec ({r['time_seconds']}s), "
              f"failures: {r['failures']}")

    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/baseline_benchmarks.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to results/baseline_benchmarks.json")


if __name__ == "__main__":
    main()

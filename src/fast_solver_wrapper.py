"""
Python wrapper for the C fast_solver shared library.

Provides the same interface as optimized_solver.py but backed by C code
for maximum performance. Uses 128-bit output to handle large denominators.
"""

import ctypes
import os

# Load the shared library
_lib_path = os.path.join(os.path.dirname(__file__), 'fast_solver.so')
_lib = ctypes.CDLL(_lib_path)

# Define the Solution struct (matches C struct with hi/lo pairs)
class _Solution(ctypes.Structure):
    _fields_ = [
        ('a_lo', ctypes.c_uint64), ('a_hi', ctypes.c_uint64),
        ('b_lo', ctypes.c_uint64), ('b_hi', ctypes.c_uint64),
        ('c_lo', ctypes.c_uint64), ('c_hi', ctypes.c_uint64),
        ('found', ctypes.c_int),
    ]

_lib.solve_erdos_straus.argtypes = [ctypes.c_uint64]
_lib.solve_erdos_straus.restype = _Solution

_lib.solve_batch.argtypes = [
    ctypes.POINTER(ctypes.c_uint64),  # primes
    ctypes.c_int,                      # count
    ctypes.POINTER(ctypes.c_uint64),  # a_lo
    ctypes.POINTER(ctypes.c_uint64),  # a_hi
    ctypes.POINTER(ctypes.c_uint64),  # b_lo
    ctypes.POINTER(ctypes.c_uint64),  # b_hi
    ctypes.POINTER(ctypes.c_uint64),  # c_lo
    ctypes.POINTER(ctypes.c_uint64),  # c_hi
    ctypes.POINTER(ctypes.c_int),     # found
]
_lib.solve_batch.restype = None


def _from_hilo(hi, lo):
    """Convert (hi, lo) uint64 pair to Python int."""
    return (hi << 64) | lo


def verify(n, a, b, c):
    """Verify that 4/n = 1/a + 1/b + 1/c using exact integer arithmetic."""
    return 4 * a * b * c == n * (b * c + a * c + a * b)


def solve(n):
    """Solve 4/n = 1/a + 1/b + 1/c. Returns (a, b, c) or None."""
    sol = _lib.solve_erdos_straus(ctypes.c_uint64(n))
    if sol.found:
        a = _from_hilo(sol.a_hi, sol.a_lo)
        b = _from_hilo(sol.b_hi, sol.b_lo)
        c = _from_hilo(sol.c_hi, sol.c_lo)
        return (a, b, c)
    return None


def solve_batch(primes):
    """Solve for a batch of primes. Returns list of (a, b, c) or None for each."""
    n = len(primes)
    p_arr = (ctypes.c_uint64 * n)(*primes)
    a_lo = (ctypes.c_uint64 * n)()
    a_hi = (ctypes.c_uint64 * n)()
    b_lo = (ctypes.c_uint64 * n)()
    b_hi = (ctypes.c_uint64 * n)()
    c_lo = (ctypes.c_uint64 * n)()
    c_hi = (ctypes.c_uint64 * n)()
    f_arr = (ctypes.c_int * n)()

    _lib.solve_batch(p_arr, n, a_lo, a_hi, b_lo, b_hi, c_lo, c_hi, f_arr)

    results = []
    for i in range(n):
        if f_arr[i]:
            a = _from_hilo(a_hi[i], a_lo[i])
            b = _from_hilo(b_hi[i], b_lo[i])
            c = _from_hilo(c_hi[i], c_lo[i])
            results.append((a, b, c))
        else:
            results.append(None)
    return results


if __name__ == "__main__":
    import time
    import sys
    sys.path.insert(0, '.')
    from sympy import primerange
    from src.optimized_solver import solve_fast as python_solve

    # Correctness on primes up to 10^5
    print("Correctness test: C solver on primes up to 10^5...")
    primes = list(primerange(2, 100001))
    failures = []
    for p in primes:
        c_sol = solve(p)
        if c_sol is None:
            failures.append(('c_none', p))
        elif not verify(p, *c_sol):
            failures.append(('c_bad', p, c_sol))
    if failures:
        print(f"FAILURES ({len(failures)}): {failures[:20]}")
    else:
        print(f"All {len(primes)} primes passed!")

    # Speed comparison at 10^7
    test_primes = list(primerange(10**7, 10**7 + 100000))
    print(f"\nSpeed test on {len(test_primes)} primes near 10^7...")

    start = time.time()
    for p in test_primes[:1000]:
        python_solve(p)
    elapsed_py = time.time() - start
    py_rate = 1000 / elapsed_py
    print(f"  Python: 1000 primes in {elapsed_py:.3f}s = {py_rate:.1f} primes/sec")

    start = time.time()
    for p in test_primes[:1000]:
        solve(p)
    elapsed_c = time.time() - start
    c_rate = 1000 / elapsed_c
    print(f"  C (single): 1000 primes in {elapsed_c:.3f}s = {c_rate:.1f} primes/sec")

    start = time.time()
    solve_batch(test_primes)
    elapsed_batch = time.time() - start
    batch_rate = len(test_primes) / elapsed_batch
    print(f"  C (batch): {len(test_primes)} primes in {elapsed_batch:.3f}s = {batch_rate:.1f} primes/sec")

    print(f"\n  Speedup (C single vs Python): {c_rate/py_rate:.1f}x")
    print(f"  Speedup (C batch vs Python): {batch_rate/py_rate:.1f}x")

    # Cross-check 10,000 primes at 10^8
    print("\nCross-checking 10,000 primes near 10^8...")
    sample = list(primerange(10**8, 10**8 + 200000))[:10000]
    c_results = solve_batch(sample)
    mismatches = 0
    for i, p in enumerate(sample):
        if c_results[i] is None:
            mismatches += 1
        elif not verify(p, *c_results[i]):
            mismatches += 1
    print(f"  Mismatches: {mismatches} / {len(sample)}")

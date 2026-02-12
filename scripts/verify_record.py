#!/usr/bin/env python3
"""
Verify a palindrome delay claim for any number.

Usage:
    python scripts/verify_record.py <number> [max_iter]

Example:
    python scripts/verify_record.py 1000206827388999999095750
    # Output: 1000206827388999999095750 reaches palindrome in 293 iterations (132 digits)
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def verify_python(n, max_iter=10000):
    """Pure Python verification (independent of C extension)."""
    for i in range(1, max_iter + 1):
        s = str(n)
        n = n + int(s[::-1])
        s2 = str(n)
        if s2 == s2[::-1]:
            return True, i, n
    return False, max_iter, n


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/verify_record.py <number> [max_iter]")
        print("Example: python scripts/verify_record.py 1000206827388999999095750")
        sys.exit(1)

    num = int(sys.argv[1])
    max_iter = int(sys.argv[2]) if len(sys.argv) > 2 else 10000

    print(f"Verifying: {num}")
    print(f"Digits: {len(str(num))}")
    print(f"Max iterations: {max_iter}")
    print()

    start = time.time()
    found, iters, result = verify_python(num, max_iter)
    elapsed = time.time() - start

    if found:
        print(f"RESULT: Palindrome reached in {iters} iterations")
        print(f"Palindrome: {result}")
        print(f"Palindrome digits: {len(str(result))}")
    else:
        print(f"RESULT: No palindrome found in {max_iter} iterations")
        print(f"Final value has {len(str(result))} digits")

    print(f"Time: {elapsed:.4f} seconds")

    # Also verify with C extension if available
    try:
        import ctypes
        lib_path = os.path.join(os.path.dirname(__file__), "..", "src", "fast_core.so")
        lib = ctypes.CDLL(lib_path)
        lib.reverse_and_add_count.argtypes = [
            ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int
        ]
        lib.reverse_and_add_count.restype = ctypes.c_int
        result_buf = ctypes.create_string_buffer(4096)
        iters_c = lib.reverse_and_add_count(str(num).encode(), max_iter, result_buf, 4096)
        print(f"\nC extension verification: {iters_c} iterations")
        if found:
            print(f"Results match: {iters_c == iters}")
    except Exception as e:
        print(f"\nC extension not available: {e}")


if __name__ == "__main__":
    main()

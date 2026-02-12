"""
Digit-pair symmetry pruning for MDPN search.

Two numbers with the same digit-pair sums produce the same result after
the first reverse-and-add step. This module generates only canonical
representatives (seeds) for each equivalence class.
"""

from itertools import product


def canonical_digit_for_pair_sum(s, is_leading=False):
    """
    For a pair sum s = d_i + d_{N-1-i}, return the canonical (d_i, d_{N-1-i}).
    For the leading pair, d_i >= 1.
    """
    if is_leading:
        d_i = max(1, s - 9)
    else:
        d_i = max(0, s - 9)
    d_j = s - d_i
    return (d_i, d_j)


def generate_seeds(num_digits):
    """
    Generate all canonical seed numbers for a given digit length.

    For N-digit numbers (N odd): (N-1)/2 pairs + 1 middle digit
    For N-digit numbers (N even): N/2 pairs

    Yields integers (the canonical seed for each equivalence class).
    """
    if num_digits < 2:
        yield from range(1, 10) if num_digits == 1 else []
        return

    is_odd = num_digits % 2 == 1
    num_pairs = (num_digits - 1) // 2 if is_odd else num_digits // 2

    # Pair sum ranges
    # Leading pair: sum from 1 to 18 (d0 >= 1)
    # Other pairs: sum from 0 to 18
    lead_range = range(1, 19)   # s0 in [1, 18]
    other_range = range(0, 19)  # si in [0, 18]
    mid_range = range(0, 10) if is_odd else [None]

    for s0 in lead_range:
        d0, d_last = canonical_digit_for_pair_sum(s0, is_leading=True)

        if num_pairs == 1:
            # 2-digit or 3-digit
            for m in mid_range:
                if is_odd:
                    digits = [d0, m, d_last]
                else:
                    digits = [d0, d_last]
                yield int(''.join(str(d) for d in digits))
            continue

        # Generate inner pair sums
        for inner_sums in product(other_range, repeat=num_pairs - 1):
            inner_digits_left = []
            inner_digits_right = []
            for s in inner_sums:
                di, dj = canonical_digit_for_pair_sum(s, is_leading=False)
                inner_digits_left.append(di)
                inner_digits_right.append(dj)

            for m in mid_range:
                digits = [d0] + inner_digits_left
                if is_odd:
                    digits.append(m)
                digits.extend(reversed(inner_digits_right))
                digits.append(d_last)
                yield int(''.join(str(d) for d in digits))


def count_seeds(num_digits):
    """Count total seeds without generating them all."""
    if num_digits < 2:
        return 9 if num_digits == 1 else 0

    is_odd = num_digits % 2 == 1
    num_pairs = (num_digits - 1) // 2 if is_odd else num_digits // 2

    lead_count = 18  # pair sums 1..18
    inner_count = 19 ** (num_pairs - 1) if num_pairs > 1 else 1
    mid_count = 10 if is_odd else 1

    return lead_count * inner_count * mid_count


def reduction_factor(num_digits):
    """Compute the reduction factor vs raw search space."""
    raw = 9 * (10 ** (num_digits - 1))
    seeds = count_seeds(num_digits)
    return raw / seeds


def verify_pruning(num_digits, reverse_and_add_fn):
    """
    Verify that pruning preserves correctness for all N-digit numbers.
    For each equivalence class, check that all members have the same delay.
    Returns True if all checks pass.
    """
    from collections import defaultdict

    lo = 10 ** (num_digits - 1)
    hi = 10 ** num_digits

    # Build map: pair_sums_tuple -> list of numbers
    classes = defaultdict(list)
    for n in range(lo, hi):
        s = str(n)
        if num_digits % 2 == 1:
            pairs = tuple(int(s[i]) + int(s[num_digits - 1 - i])
                          for i in range(num_digits // 2))
            mid = int(s[num_digits // 2])
            key = pairs + (mid,)
        else:
            pairs = tuple(int(s[i]) + int(s[num_digits - 1 - i])
                          for i in range(num_digits // 2))
            key = pairs
        classes[key].append(n)

    # Verify each class has same delay
    for key, members in classes.items():
        delays = set()
        for n in members:
            d = reverse_and_add_fn(n)
            delays.add(d)
        if len(delays) > 1:
            print(f"FAIL: class {key} has multiple delays: {delays}")
            print(f"  Members: {members[:5]}...")
            return False

    print(f"PASS: {len(classes)} equivalence classes, all consistent")
    return True


if __name__ == "__main__":
    # Print reduction factors
    for d in [5, 6, 7, 10, 15, 20, 25, 27]:
        seeds = count_seeds(d)
        rf = reduction_factor(d)
        print(f"{d}-digit: {seeds:,} seeds, reduction factor: {rf:,.0f}x")

    # Verify for 5-digit numbers
    print("\nVerifying 5-digit numbers...")
    from src.reverse_add import reverse_and_add

    def delay_fn(n):
        found, iters, _ = reverse_and_add(n, max_iter=500)
        return iters if found else -1

    verify_pruning(5, delay_fn)

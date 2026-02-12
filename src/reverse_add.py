"""
Baseline reverse-and-add algorithm for palindrome search.

The reverse-and-add process takes a number, reverses its digits,
and adds the reversed number to the original. This is repeated
until a palindrome is reached (or a maximum iteration count).
"""


def is_palindrome(n):
    """Check if integer n is a palindrome via string comparison."""
    s = str(n)
    return s == s[::-1]


def reverse_digits(n):
    """Return the integer formed by reversing the digits of n."""
    return int(str(n)[::-1])


def reverse_and_add(n, max_iter=10000):
    """
    Apply the reverse-and-add process to n.

    Parameters
    ----------
    n : int
        Starting number (must be positive).
    max_iter : int
        Maximum iterations before giving up (Lychrel candidate).

    Returns
    -------
    tuple : (is_palindrome, iteration_count, final_value)
        is_palindrome: True if a palindrome was reached
        iteration_count: number of reverse-and-add steps taken
        final_value: the palindrome (or last value if max_iter exceeded)
    """
    for i in range(1, max_iter + 1):
        n = n + reverse_digits(n)
        if is_palindrome(n):
            return (True, i, n)
    return (False, max_iter, n)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python reverse_add.py <number> [max_iter]")
        sys.exit(1)

    num = int(sys.argv[1])
    max_it = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    found, iters, result = reverse_and_add(num, max_it)

    if found:
        print(f"{num} reaches palindrome {result} in {iters} iterations")
        print(f"Palindrome has {len(str(result))} digits")
    else:
        print(f"{num} did not reach palindrome in {max_it} iterations")
        print(f"Last value has {len(str(result))} digits")

/* Standalone benchmark for the C solver */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

typedef unsigned long long u64;
typedef unsigned __int128 u128;

/* Forward declare from fast_solver.c (we'll link) */
typedef struct {
    u64 a_lo, a_hi, b_lo, b_hi, c_lo, c_hi;
    int found;
} Solution;
extern Solution solve_erdos_straus(u64 n);

/* Simple prime sieve */
static int is_prime(u64 n) {
    if (n < 2) return 0;
    if (n < 4) return 1;
    if (n % 2 == 0 || n % 3 == 0) return 0;
    for (u64 i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i+2) == 0) return 0;
    }
    return 1;
}

int main() {
    u64 lo = 1000000000ULL; /* 10^9 */
    u64 hi = lo + 100000;

    printf("Benchmarking C solver on primes in [%llu, %llu]...\n", lo, hi);

    int count = 0, found = 0;
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    for (u64 n = lo + 1; n < hi; n += 2) {
        if (!is_prime(n)) continue;
        count++;
        Solution s = solve_erdos_straus(n);
        if (s.found) found++;
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double elapsed = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;

    printf("Tested %d primes in %.3f s = %.0f primes/sec\n", count, elapsed, count / elapsed);
    printf("Found solutions: %d/%d\n", found, count);
    return 0;
}

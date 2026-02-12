/*
 * Fast C solver for the Erdős–Straus conjecture.
 *
 * Uses divisor-based parametric search with 128-bit arithmetic.
 * Returns solutions as pairs of (hi, lo) uint64 to represent 128-bit values.
 *
 * Compile: gcc -O3 -shared -fPIC -o fast_solver.so fast_solver.c -lm
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef unsigned long long u64;
typedef __int128 i128;
typedef unsigned __int128 u128;

#define MAX_DIVS 16384

/* Result: each of a,b,c stored as (hi,lo) pair for 128-bit support */
typedef struct {
    u64 a_lo, a_hi;
    u64 b_lo, b_hi;
    u64 c_lo, c_hi;
    int found;
} Solution;

static void set_sol(Solution *s, u128 a, u128 b, u128 c) {
    /* Sort a <= b <= c */
    if (a > b) { u128 t = a; a = b; b = t; }
    if (b > c) { u128 t = b; b = c; c = t; }
    if (a > b) { u128 t = a; a = b; b = t; }

    s->a_lo = (u64)a; s->a_hi = (u64)(a >> 64);
    s->b_lo = (u64)b; s->b_hi = (u64)(b >> 64);
    s->c_lo = (u64)c; s->c_hi = (u64)(c >> 64);
    s->found = 1;
}

/* Verify using modular arithmetic with multiple large primes */
static int verify128(u64 n, u128 a, u128 b, u128 c) {
    static const u64 mods[] = {
        1000000007ULL,
        1000000009ULL,
        998244353ULL,
        999999937ULL,
    };

    for (int m = 0; m < 4; m++) {
        u64 mod = mods[m];
        u64 an = (u64)(a % mod);
        u64 bn = (u64)(b % mod);
        u64 cn = (u64)(c % mod);
        u64 nn = n % mod;

        /* lhs = 4*a*b*c mod p */
        u128 lhs = (u128)4 * an % mod;
        lhs = lhs * bn % mod;
        lhs = lhs * cn % mod;

        /* rhs = n*(b*c + a*c + a*b) mod p */
        u128 bc = (u128)bn * cn % mod;
        u128 ac = (u128)an * cn % mod;
        u128 ab = (u128)an * bn % mod;
        u128 sum = (bc + ac + ab) % mod;
        u128 rhs = (u128)nn * sum % mod;

        if ((u64)lhs != (u64)rhs) return 0;
    }
    return 1;
}

/* Get divisors of p^2 * x^2 efficiently */
static int get_divisors_p2x2(u64 p, u64 x, u64 *divs) {
    typedef struct { u64 prime; int exp; } Factor;
    Factor factors[64];
    int nfactors = 0;

    u64 temp = x;
    for (u64 d = 2; d * d <= temp && nfactors < 63; d++) {
        if (temp % d == 0) {
            factors[nfactors].prime = d;
            factors[nfactors].exp = 0;
            while (temp % d == 0) {
                factors[nfactors].exp++;
                temp /= d;
            }
            nfactors++;
        }
    }
    if (temp > 1 && nfactors < 63) {
        factors[nfactors].prime = temp;
        factors[nfactors].exp = 1;
        nfactors++;
    }

    Factor all_factors[64];
    int nall = 0;
    int p_found = 0;

    for (int i = 0; i < nfactors; i++) {
        all_factors[nall].prime = factors[i].prime;
        all_factors[nall].exp = 2 * factors[i].exp;
        if (factors[i].prime == p) {
            all_factors[nall].exp += 2;
            p_found = 1;
        }
        nall++;
    }
    if (!p_found) {
        all_factors[nall].prime = p;
        all_factors[nall].exp = 2;
        nall++;
    }

    divs[0] = 1;
    int count = 1;

    for (int i = 0; i < nall && count < MAX_DIVS; i++) {
        int prev_count = count;
        u64 pe = 1;
        for (int e = 0; e < all_factors[i].exp && count < MAX_DIVS; e++) {
            pe *= all_factors[i].prime;
            for (int j = 0; j < prev_count && count < MAX_DIVS; j++) {
                divs[count++] = divs[j] * pe;
            }
        }
    }

    return count;
}

Solution solve_erdos_straus(u64 n) {
    Solution sol;
    memset(&sol, 0, sizeof(sol));

    if (n <= 1) return sol;
    if (n == 2) { set_sol(&sol, 1, 2, 2); return sol; }
    if (n == 3) { set_sol(&sol, 1, 4, 12); return sol; }
    if (n == 4) { set_sol(&sol, 2, 4, 4); return sol; }
    if (n == 5) { set_sol(&sol, 2, 4, 20); return sol; }

    if (n % 2 == 0) {
        u128 m = n / 2;
        set_sol(&sol, m, 2 * m, 2 * m);
        return sol;
    }

    if (n % 4 == 3) {
        u128 q = (n + 1) / 4;
        u128 m = (u128)n * q;
        /* Always use (q, 2m, 2m): 4/p = 1/q + 1/(2m) + 1/(2m)
         * Proof: 1/q + 2/(2pq) = (2pq + 2q)/(2pq^2) ... simplifies to 4/p.
         * The m*(m+1) formula overflows u128 for large primes when m is odd. */
        set_sol(&sol, q, 2 * m, 2 * m);
        return sol;
    }

    /* n ≡ 1 mod 4: divisor-based search.
     * Empirically, solutions are always found within x_offset < 10 of x_min
     * even for primes up to 10^13. Cap at x_min + 50000 for safety. */
    u64 x_min = (n + 3) / 4;
    u64 x_max = x_min + 50000;

    u64 *divs = (u64 *)malloc(MAX_DIVS * sizeof(u64));
    if (!divs) return sol;

    for (u64 x = x_min; x <= x_max; x++) {
        u128 A = (u128)4 * x - n;
        if (A == 0) continue;

        u128 nx = (u128)n * x;
        u128 D = nx * nx;

        int ndivs = get_divisors_p2x2(n, x, divs);

        u64 A64 = (u64)A;
        u64 target_mod = (u64)((A64 - (u64)(nx % A)) % A64);

        for (int i = 0; i < ndivs; i++) {
            u64 d1 = divs[i];
            if ((u128)d1 > nx) continue;
            if (d1 % A64 != target_mod) continue;

            u128 d2 = D / d1;
            if ((d2 + nx) % A != 0) continue;

            u128 y = (d1 + nx) / A;
            u128 z = (d2 + nx) / A;

            if (y < x) continue;
            if (z < y) { u128 t = y; y = z; z = t; }
            if (y < x) continue;

            if (verify128(n, x, y, z)) {
                set_sol(&sol, x, y, z);
                free(divs);
                return sol;
            }
        }
    }

    free(divs);
    return sol;
}

void solve_batch(u64 *primes, int count,
                 u64 *a_lo, u64 *a_hi,
                 u64 *b_lo, u64 *b_hi,
                 u64 *c_lo, u64 *c_hi,
                 int *found) {
    for (int i = 0; i < count; i++) {
        Solution s = solve_erdos_straus(primes[i]);
        a_lo[i] = s.a_lo; a_hi[i] = s.a_hi;
        b_lo[i] = s.b_lo; b_hi[i] = s.b_hi;
        c_lo[i] = s.c_lo; c_hi[i] = s.c_hi;
        found[i] = s.found;
    }
}

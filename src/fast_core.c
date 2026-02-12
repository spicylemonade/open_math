/*
 * fast_core.c - High-performance reverse-and-add using digit arrays.
 *
 * Key insight: Instead of converting to/from GMP integers via strings,
 * work with Base-10 digit arrays directly. Addition, reversal, and
 * palindrome checking are all O(n) on digit arrays.
 *
 * Compile: gcc -O3 -shared -fPIC -o fast_core.so fast_core.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DIGITS 4096

/* Check palindrome on digit array of length len */
static int is_palindrome(const unsigned char *d, int len) {
    int i = 0, j = len - 1;
    while (i < j) {
        if (d[i] != d[j]) return 0;
        i++;
        j--;
    }
    return 1;
}

/*
 * Add digit array d[0..len-1] to its reverse, store in result.
 * d[0] is the most significant digit.
 * Returns new length (may be len or len+1 due to carry).
 */
static int add_reverse(const unsigned char *d, int len, unsigned char *result) {
    int carry = 0;
    /* Add from least significant end */
    for (int i = len - 1; i >= 0; i--) {
        int j = len - 1 - i;  /* reversed index */
        int sum = d[i] + d[j] + carry;
        carry = sum / 10;
        result[i + 1] = sum % 10;  /* +1 to leave room for carry */
    }
    if (carry) {
        result[0] = carry;
        return len + 1;
    } else {
        /* Shift result left by 1 */
        memmove(result, result + 1, len);
        return len;
    }
}

/*
 * reverse_and_add_count:
 *   Given a number as a decimal string, compute iterations to palindrome.
 *   Returns iteration count, or -1 if max_iter exceeded.
 *   If result_buf is not NULL, writes the final palindrome string.
 */
int reverse_and_add_count(const char *num_str, int max_iter,
                          char *result_buf, int result_buf_size) {
    unsigned char d1[MAX_DIGITS], d2[MAX_DIGITS];
    int len = strlen(num_str);

    if (len >= MAX_DIGITS) return -2;  /* too large */

    /* Convert string to digit array */
    for (int i = 0; i < len; i++) {
        d1[i] = num_str[i] - '0';
    }

    unsigned char *cur = d1, *next = d2;

    for (int iter = 1; iter <= max_iter; iter++) {
        len = add_reverse(cur, len, next);

        /* Check palindrome */
        if (is_palindrome(next, len)) {
            if (result_buf && result_buf_size > 0) {
                int copy_len = len < result_buf_size - 1 ? len : result_buf_size - 1;
                for (int i = 0; i < copy_len; i++) {
                    result_buf[i] = next[i] + '0';
                }
                result_buf[copy_len] = '\0';
            }
            return iter;
        }

        /* Swap buffers */
        unsigned char *tmp = cur;
        cur = next;
        next = tmp;
    }

    return -1;
}

/*
 * reverse_and_add_count_large:
 *   Same as above but with dynamic allocation for very large numbers.
 *   Supports up to 100000 digits.
 */
int reverse_and_add_count_large(const char *num_str, int max_iter,
                                char *result_buf, int result_buf_size) {
    int initial_len = strlen(num_str);
    /* Estimate max digits: each step can add at most 1 digit */
    int max_len = initial_len + max_iter + 10;
    if (max_len > 1000000) max_len = 1000000;

    unsigned char *d1 = (unsigned char *)malloc(max_len);
    unsigned char *d2 = (unsigned char *)malloc(max_len);
    if (!d1 || !d2) { free(d1); free(d2); return -2; }

    int len = initial_len;
    for (int i = 0; i < len; i++) {
        d1[i] = num_str[i] - '0';
    }

    unsigned char *cur = d1, *next = d2;

    int result = -1;
    for (int iter = 1; iter <= max_iter; iter++) {
        len = add_reverse(cur, len, next);

        if (is_palindrome(next, len)) {
            if (result_buf && result_buf_size > 0) {
                int copy_len = len < result_buf_size - 1 ? len : result_buf_size - 1;
                for (int i = 0; i < copy_len; i++) {
                    result_buf[i] = next[i] + '0';
                }
                result_buf[copy_len] = '\0';
            }
            result = iter;
            break;
        }

        unsigned char *tmp = cur;
        cur = next;
        next = tmp;
    }

    free(d1);
    free(d2);
    return result;
}

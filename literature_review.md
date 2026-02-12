# Literature Review: Most Delayed Palindromic Number (MDPN)

## 1. The Reverse-and-Add Problem

The reverse-and-add process takes a natural number, reverses its digits, and adds the result to the original. This is repeated until a palindrome is reached (or, potentially, forever). A number that never reaches a palindrome is called a **Lychrel number**. No base-10 Lychrel number has been proven to exist, though 196 is the smallest candidate, having been tested beyond 1 billion iterations without finding a palindrome [Walker1990, Wikipedia_Lychrel].

The **Most Delayed Palindromic Number (MDPN)** is the non-Lychrel number requiring the most reverse-and-add iterations before reaching a palindrome.

## 2. Key Sources

### 2.1 Wikipedia: Lychrel Numbers
The Wikipedia article on Lychrel numbers [Wikipedia_Lychrel] provides the definitive public summary of the problem, including the history of the 196 conjecture, known Lychrel candidates, and the MDPN records. It notes that the name "Lychrel" was coined by Wade Van Landingham in 2002.

### 2.2 Jason Doucette's World Records Page
Doucette's page [Doucette_WorldRecords] is the primary historical reference for MDPN records. Key contributions:
- Completed exhaustive search of all digit lengths up to 18 digits (completed Sept 25, 2005)
- Found the 261-iteration record: 1,186,060,307,891,929,990 (19 digits, Nov 30, 2005)
- Derived the statistical prediction formula: **Expected Max Delay = 14.256 × digit_length − 17.320** with standard deviation 11.088 and 98.96% correlation
- Observed that even-digit-length sets are unlikely to produce new records

### 2.3 Dmitry Maslov's MDPN Project
Maslov's MDPN project [Maslov_MDPN] hosts the current world record and a comprehensive database:
- Current world record: **1,000,206,827,388,999,999,095,750** (25 digits) → 293 iterations → 132-digit palindrome (Dec 14, 2021)
- The mdpn-db GitHub repository [Maslov_MDPN_DB] contains all delayed palindromes and statistics up to 20-digit numbers

### 2.4 OEIS Sequences
Several OEIS sequences are central to this research:
- **A033665** [OEIS_A033665]: Number of reverse-and-add steps to reach a palindrome (or -1 if never)
- **A065198** [OEIS_A065198]: Record-setting indices in A033665 (the MDPN sequence itself)
- **A281506** [OEIS_A281506]: All 108,864 numbers requiring exactly 261 steps (contributed by Shchebetov, 2017)
- **A281508** [OEIS_A281508]: The 125 newly-discovered 261-step numbers
- **A281509** [OEIS_A281509]: Intermediate values in the 261-step reverse-and-add trajectory

### 2.5 Robbie Rosati's Blog Post
Rosati's blog [Rosati_Blog] at UT-Austin Physics provides an accessible introduction to the MDPN problem with code examples and describes an attempt at finding higher-delay numbers.

### 2.6 Nishiyama 2012 Paper
Yutaka Nishiyama's paper "Numerical Palindromes and the 196 Problem" [Nishiyama2012] (IJPAM, Vol. 80, No. 3, pp. 375-384) provides:
- Mathematical treatment of the reverse-and-add process
- Classification of Lychrel candidate seeds (196 and 879 for 3-digit numbers)
- Discussion of "seed" vs "kin" distinction for Lychrel candidates

## 3. World Record Timeline

| Year | Discoverer | Number | Digits | Iterations | Palindrome Digits |
|------|-----------|--------|--------|------------|-------------------|
| 2005 | Jason Doucette | 1,186,060,307,891,929,990 | 19 | 261 | 119 |
| 2019 | Rob van Nobelen | 12,000,700,000,025,339,936,491 | 23 | 288 | 142 |
| 2021 | Anton Stefanov | 13,968,441,660,506,503,386,020 | 23 | 289 | 142 |
| 2021 | Dmitry Maslov | 1,000,206,827,388,999,999,095,750 | 25 | 293 | 132 |

No new record has been set since December 2021 — over 4 years of inactivity.

## 4. Existing Implementations

### 4.1 The p196_mpi Implementation
Dolbeau's p196_mpi [Dolbeau_p196] is the fastest known implementation of the reverse-and-add algorithm:
- Achieved 1.1 × 10¹² digits/second throughput
- Uses MPI for distributed computation with SIMD vectorization (SSE3/SSE4, AltiVec)
- Focused on extending the 196 sequence, not on MDPN search
- Scales linearly across 12+ nodes with InfiniBand interconnect

### 4.2 GitHub Repositories
- **aloncat/mdpn-db** [Maslov_MDPN_DB]: Maslov's MDPN database (Python)
- **aloncat/mdpn**: Core MDPN search tool
- Various implementations on GitHub Topics "most-delayed-palindromic-number" [GitHub_MDPN_Topic]

## 5. Key Optimization: Digit-Pair Symmetry Pruning
Doucette discovered that numbers can be grouped by their digit-pair sums. Two numbers with the same pair sums at positions (i, n-1-i) will have identical reverse-and-add behavior. This reduces the search space by orders of magnitude — for 17-digit numbers, the effective search space was reduced from 10^17 to ~187 billion candidates [Doucette_WorldRecords].

## 6. Statistical Predictions
Using Doucette's formula (Expected Max = 14.256 × digits − 17.320, σ = 11.088):

| Digits | Expected Max Delay | 3σ Upper Bound |
|--------|-------------------|----------------|
| 25 | 339 | 372 |
| 26 | 353 | 386 |
| 27 | 367 | 401 |
| 28 | 382 | 415 |
| 29 | 396 | 429 |
| 30 | 410 | 443 |

The current record of 293 for 25 digits is actually below the expected maximum for that digit length, suggesting that the 25-digit search space has not been exhaustively explored.

## 7. Research Opportunity
The field has been dormant for 4+ years. The statistical formula predicts that 25-digit numbers alone should contain records up to ~339 iterations. The 293-iteration record was found by targeted (non-exhaustive) search, meaning many unexplored regions remain. Modern hardware advances (faster CPUs, more cores) make deeper searches feasible.

## References
See `sources.bib` for complete BibTeX entries.

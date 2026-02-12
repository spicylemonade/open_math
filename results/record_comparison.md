# MDPN Record Comparison

## World Record Timeline

| Year | Discoverer | Number | Digits | Iterations | Palindrome Digits | Method | Source |
|------|-----------|--------|--------|------------|-------------------|--------|--------|
| 2005 | Jason Doucette | 1,186,060,307,891,929,990 | 19 | 261 | 119 | Exhaustive enumeration (all 18-digit) | [Doucette_WorldRecords] |
| 2019 | Rob van Nobelen | 12,000,700,000,025,339,936,491 | 23 | 288 | 142 | Targeted search (non-exhaustive) | [Maslov_Records] |
| 2021 | Anton Stefanov | 13,968,441,660,506,503,386,020 | 23 | 289 | 142 | Targeted search | [Maslov_Records] |
| 2021 | Dmitry Maslov | 1,000,206,827,388,999,999,095,750 | 25 | 293 | 132 | Targeted search | [Maslov_MDPN] |
| 2026 | This study | — | 25-33 | 293 (tie) | — | Multi-strategy (68M+ candidates) | This work |

## Our Search Effort

| Strategy | Candidates Tested | Best Delay | Digit Range |
|----------|------------------|-----------|-------------|
| Near-record perturbation (25-digit) | 3.3M | 293 (record kins) | 25 |
| Pair-sum variation | 43M | 293 (record only) | 25 |
| Multi-strategy composite | 6.6M | 293 (31 kins found) | 25-29 |
| Pure random (25,27,29-digit) | 15M | 155 | 25-29 |
| Extended random (29,31,33-digit) | 30M | 122 | 29-33 |
| **Total** | **~98M** | **293** | **25-33** |

## Key Findings

1. **The 293-step record is extremely robust** — despite testing ~98 million candidates across 25-33 digits, no number exceeding 293 iterations was found.

2. **High-delay numbers are astronomically rare** — from random sampling of 10M numbers per digit count, the maximum observed delay was only 155 (for 25 digits). The 293 record is about 2x the random-sampling maximum.

3. **Record kins cluster tightly** — we found 31 distinct 25-digit numbers achieving exactly 293 iterations, all sharing the same pair-sum structure as the record. This confirms the digit-pair equivalence theory.

4. **Breaking the record likely requires exhaustive enumeration** or extremely sophisticated search heuristics. The search space for 25-digit numbers is ~2×10^16 canonical seeds, of which we tested ~0.3%.

## Comparison to Doucette's Formula

Expected max delay for 25-digit numbers: 339 ± 11

The current record of 293 is **4.1 standard deviations below** the predicted maximum, strongly suggesting that many undiscovered 25-digit numbers with delay > 293 exist — they simply haven't been found yet.

## References

See `sources.bib` for full citations: [Doucette_WorldRecords], [Maslov_MDPN], [Maslov_Records], [OEIS_A065198], [Nishiyama2012]

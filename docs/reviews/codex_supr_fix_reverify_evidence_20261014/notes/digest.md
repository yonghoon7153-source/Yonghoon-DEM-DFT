# SUPR-01 / approved SHA / production194 registration recheck

Pin: `df647d4e31224e1a270dae01dd41f91af3048361`.

Disposition: **SUPR-01 closes against the prior verdict §4 minimum 1–3. No new defect found in this scoped review.** The production194 registration comparison remains an explicitly documented manual launch condition, not an implemented P0–P10 claim.

## Evidence and method

`probes/digest_probe.py` writes `evidence/digest_probe/results.json` and individual logs/receipts. The test uses actual `build_plan`, `plan_input_digest`, `print_preflight`, `_preflight_receipt_record`, `preflight_receipt_checks`, registration parsing, and manifest validators. CPU/memory/raw/generation/clean-git preflight statuses are explicitly synthetic fixtures: **no real preflight, WSL, production run, or numerical solver is executed by this probe**. Pin in the synthetic fixture is a test input, not proof of runtime authenticity. Source files remain untouched.

The five historical logs also run through the actual CLI `main` entry points in child Python processes. Baseline modules are loaded without changes and their repository paths are pointed at the current immutable source snapshot, whose unchanged input bytes and seal are the relevant baseline data. This is a code-before/after comparison, not a claim of having checked out or executed a full baseline repository.

## Observed results

- Normal supplement fixture passes P0–P10 and E1/E2; normal production194 fixture passes P0–P10.
- Normal receipt compared with changed registration n, ID hash, raw-table hash, or TSV hash fails E1. Changed registered code fingerprint fails E2.
- Historical `alternate_cohort.tsv` SHA is `8d5dcbd28061327f7c4f8c1a0b8915647c368236a78ced0c5ed7c3693100f1d4`; n/IDs/raw table remain identical. A new-format receipt from its actual plan/log is rejected by **E1 and P9 exactly**, without relying on a path override flag.
- Omission of each of the five digest keys, and an added unknown digest key, fail E1/P2/P9. Changing the cohort mapping key from lhss to lhs fails E1/P9.
- Receipt checked against the opposite registered set fails P6/P9 in both directions.
- Correct full SHA, seven-character prefix, and uppercase argument pass P10. Wrong SHA, nonhex, or six characters fail P10. Missing SHA leaves one explicit warning and no failure, as approved in the plan. Correct full/prefix manifest approval passes F7/G7; wrong/nonhex fails both.

| Historical raw log | Baseline process rc | Fixed process rc |
|---|---:|---:|
| wrong_tsv_full_log | 0 | 1 |
| wrong_tsv_registered_grep | 0 | 1 |
| observation_off_full_log | 1 | 1 |
| observation_off_truncated_before_stop | 0 | 1 |
| missing_three_prerequisite_lines | 0 | 1 |

Fixed rejection is E0, correctly ending acceptance of standalone/grep logs; separate new-format value tests above demonstrate that the TSV flaw is fixed beyond merely refusing the old format.

## production194 Q3

The actual pinned files recalculate to the approved registration §2 values for all five keys:

- `n = 194`, `missing_raw_sha = []`
- `ids_sha256 = a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf`
- `raw_sha256_table_sha256 = da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784`
- `cohort_tsv_sha256.lhs = 32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809`
- `cohort_tsv_sha256.lhsx = 0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45`

A controlled change of the default lhs TSV path to a copy with one extra newline leaves the exact IDs/raw table unchanged. With both receipt generation and verification reading those changed defaults, P0–P10 pass, while a comparison with the preregistered values fails `cohort_tsv_sha256`. A second fixture changes both that TSV and one raw SHA: P0–P10 again pass with matching changed defaults, while preregistration comparison fails `cohort_tsv_sha256` and `raw_sha256_table_sha256`. Against the actual pinned inputs, that latter receipt fails P9. This demonstrates the documented boundary, not a new bypass of a promised registration validator.

The current manual procedure is sufficient **if its result is retained as an explicit prerequisite to author launch approval**: compare the full raw-table SHA and both full cohort TSV SHAs from the verified `INPUT_DIGEST_JSON` line with registration §2, plus the code fingerprint with §3 (`e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`). Record the receipt/log hash or file identity and match outcome so the manual comparison refers to the same P0–P10-verified run. The five-key complete comparison is clearer than abbreviated values. `preflight-verify rc=0` alone is not production194 preregistration equality or launch authorization.

An automatic registration check is a useful future reduction of manual error, but not required to close these two prior findings under the explicit separate-comparison alternative. Do not silently drop the manual prerequisite.

## Locations

- Runner `INPUT_DIGEST_KEYS`: line 790; machine line producer: 1827–1829 and 1873–1876.
- Runner strict digest/receipt/log equality P2: 1985–1995; input recalculation P9: 2058–2076; approval SHA P10: 2077–2085.
- Supplement E1/E2 registered-value linkage: 192–212; F7/G7: 247–251.
- production194 registration §4 correction/manual condition: 226–243; plan §4 acknowledges the missing automatic document-value check.

The approved-SHA checks establish equality to the supplied string; they do not grant author approval, authenticate jointly edited evidence, substitute for final-pin WSL checks, or validate fast16+real4. Those limits are consistent with the request's stated scope.

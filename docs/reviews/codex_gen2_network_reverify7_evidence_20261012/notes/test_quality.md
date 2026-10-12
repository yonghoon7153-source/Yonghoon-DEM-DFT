# R7 independent test-quality review

Pin: `3cedd40a5911d0606bf33ed2085d5cb93c4db2e0`. Read-only source review against `parent/scripts/g2_network_reread.py` (parent `821f0e151`). No source edits, DEM/MPM run, 194 run, or code fixes.

## Conclusion

No blocking test-quality defect found for G2RR6-01 closure. The three new aggregate checks exercise the intended consumer path and reject missing output or ordinary CLI crashes. The checked-in mutation suite has 25 synthetic mutations, not 25 newly exposed parent false acceptances: 24 pass the parent predicate and one (`na_dup_row`) is an existing-rejection regression. The request's claim that all 25 passed the parent is inaccurate, but current rejection and the 23/26 aggregate-to-26/26 claim are not invalidated by that count correction.

## Assertion quality

- `source/scripts/g2_network_reread.py:1249`: `_sm` writes each input, invokes actual `main(['--smoke-root', ..., '--json', ...])`, then reads that invocation's distinct JSON pathname. It returns rc, complete S0/S0b metadata mapping, and output JSON. The new synthetic aggregate at lines 1360–1364 requires exact `(1, {'S0': True, 'S0b': False})`. It therefore checks S0 unchanged and S0b failed, not merely nonzero exit.
- `:1073`: `_main_rc` catches `SystemExit` only. A normal Python exception is not turned into successful test evidence; it escapes and fails the selftest. An argparse/SystemExit rejection without a result JSON yields missing metadata and fails the new assertions. Each result path is new within a fresh temporary directory, so another case's JSON cannot provide a stale success.
- `:337`: predicate exceptions are deliberately converted into a FAIL verdict. The new aggregate does not separately assert the predicate ID or forbid `판정 예외`, so reading its result alone cannot establish which predicate failed. Independent evaluation of all 25 exact checked-in mutations resolves this: every case fails only its intended ID and none uses the exception fallback. ID counts are SHA 10, negative-area cause 13, failed-stage 1, tau 1.
- `:1371–1385`: the seven imported-record cases assert `(rc, n_fail) == (0,0)` for positive and `(1,1)` for each negative. They do not separately assert S0/S0b in this aggregate. The imported positive cannot pass by a generic failure or missing output, and the synthetic aggregate separately protects S0. Parent agent owns the independent actual CLI verification of all seven.
- `:1305–1310`: the preceding positive synthetic check is substantial: exact S0/S0b, rc 0, n_fail 0, three normal published cases, every normal case check passing, stable ID order, seven producer PASS results, seven recomputed PASS results, and the fixed failure token. Thus failure of the producer child to yield the expected positive checks is visible.
- `:1386–1394`: the third new check compares four registered full SHA-256 values with the README table. This is a registry drift assertion; it is correctly distinct from the consumer's 12-digit record comparison. The README's extra attachment checksum is intentionally outside the four registered inputs.

## Independent before/after evidence

`probes/test_quality_probe.py` parses the current source AST and executes the exact synthetic fixture and V6/V6s construction statements. It imports current and parent modules separately, does not rewrite them, and runs their pure shared predicates. This is an independent predicate/source audit, not another claimed CLI/pipeline run. Output: `evidence/test_quality_predicates.json`.

| Exact current selftest group | Cases | Parent accepts | Current accepts |
|---|---:|---:|---:|
| V6 (Codex four) | 4 | 4 | 0 |
| V6s (same class) | 21 | 20 | 0 |
| Total | 25 | 24 | 0 |

Both synthetic positive fixtures pass. All seven imported `r6_s0b_*.input.json` files are byte-identical to the original R6 local review evidence under sibling `gen2_network_reverify6_20261011/evidence`. For current predicates, the positive passes; SHA missing/mismatch/false flag fail only `case15.raw_sha`; area positive/missing fail only `case15.nc3_cause`; the PermissionError control fails only `case15.nc5_attempt`. No case uses the predicate-exception fallback. Parent accepts the positive and the four original false acceptances, while rejecting the existing false-flag and PermissionError controls.

## Nonblocking documentation correction

`submitted/request.md:29` says Codex four plus same-class 21 were **all** old rc 0/S0b pass. But `source/scripts/g2_network_reread.py:1357` constructs the duplicate-row mutation as two `(31,29241)` pairs. The old parent `nc3` compares the sorted ID-pair list to the two distinct registered pairs, so it already rejects that mutation. Exact correction: **Codex four + same-class 20 = 24 false acceptances; duplicate row = one existing-rejection regression; new code rejects all 25**. This does not reopen G2RR6-01 and should not be treated as a 194 launch blocker.

The separate imported `probe_same_class.py` has a different 23-case set (including two old rejections, excluding the new duplicate-row case). Its 21 accepted / 2 rejected before and 23 rejected after are consistent with the archived JSON. Do not conflate that 23-case probe with the 25-case consumer selftest group.

## Producer compatibility

`source/scripts/wsl_network_smoke.py:218` produces exactly four cells per negative row: integer IDs, rounded area in µm², rounded delta in µm. `:370–371` records the two 12-digit prefixes after the producer's full checksum comparison. `:683–689` delegates the seven case15 checks to the shared current predicate. The two fixture additions align with the real producer's existing format. The imported 10-09 positive passes the strengthened predicates without conversion. Actual child pipeline behavior is being checked independently by the parent agent.

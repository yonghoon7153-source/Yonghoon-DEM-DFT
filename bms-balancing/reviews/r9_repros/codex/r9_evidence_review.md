# R9 focused adversarial evidence — `29ef5058e68c0c64dba840ecc5a7495644cb092e`

Scope: R8-06/07/08, `c6_04`, mutation classification, replay reachability, schedule counters. The target worktree was not edited. Mutation execution used `outputs/r9_evidence_clean_29ef5058/bms-balancing`.

## Findings

### E1 — P2 — replay accepts zero/unknown probes as a successful closure run

`reviews/r7_repros/replay_codex_r7.py:100-107` turns the user string into `want` without validating it. Lines 124-131 silently ignore an unknown ID, and line 136 returns 0 unconditionally. Therefore a typo is a successful run with no reachability evidence.

Executable counterexample (run from the clean copy):

```sh
python3 reviews/r7_repros/replay_codex_r7.py --target . --probes R7-DOES-NOT-EXIST
```

Observed: rc 0, requested target head `29ef5058e68c0c64dba840ecc5a7495644cb092e`, and `"probes": {}`.

Minimum closure: reject an empty list, every unknown ID, duplicates, and mixed valid+unknown lists; require `set(out["probes"]) == set(requested)` before returning 0. Add empty, typo, and mixed-selection regressions.

### E2 — P2 — replay records but does not enforce target SHA (or clean evidence source)

`replay_codex_r7.py:106-109` records `git rev-parse HEAD`, but never compares it with an expected target. `tests/test_r8_codex.py:292` only requires `target_head` to be truthy. The `PINNED` value at runner line 19 is the old R7 package SHA and is deliberately bypassed; it is not target validation.

Executable counterexample: the clean files were placed under a temporary Git repository with arbitrary empty HEAD `e6b10492adf0b0349950ef97c6f2d6f75bba937d`, then:

```sh
python3 reviews/r7_repros/replay_codex_r7.py --target . --probes R7-01
```

Observed: rc 0, the arbitrary `target_head`, and R7-01 reported `도달: true`, `상태: 반례 소멸`. Thus the JSON is not evidence that the named R9 SHA was replayed. Dirty/untracked probe code is likewise not reported or bound.

Minimum closure: require an explicit `--expected-head` and fail on mismatch; record/enforce cleanliness for the target code and replay package, or bind the replay package files by blob/hash. Test a wrong HEAD and dirty probe file.

### E3 — P2 — mutation classifier still maps pytest interruption/internal/usage exit codes to CAUGHT

`reviews/r6_repros/codex_r6_mutation_audit.py:18-34` receives only the last summary line. It special-cases rc 5 and text containing `error`, but otherwise any nonzero rc with a `passed|failed` count is CAUGHT. It does not require pytest's test-failure exit code 1 and cannot prove the intended assertion/exception killed the mutant. `tests/test_r8_codex.py:273-276` covers rc 0/1/2/5 but omits rc 3/4 and interruption summaries.

Read-only classifier probe observed:

```text
rc=1: CAUGHT
rc=2: CAUGHT
rc=3: CAUGHT
rc=4: CAUGHT
rc=5: 오류
```

for the identical last line `1 failed, 51 deselected in 1.4s`. Rc 2 is interruption, rc 3 is pytest internal error, and rc 4 is usage error—not mutation detection.

Reproducer: `python3 outputs/r9_evidence_classify_probe.py <path-to-bms-balancing>`.

Minimum closure: only rc 1 may be CAUGHT; rc 0 is MISSED; rc 2/3/4/5 and signals/timeouts are audit errors. Capture the full result (prefer structured/JUnit output), bind each mutant to expected selected node IDs, and for value-specific claims require the intended assertion/fingerprint rather than merely any test failure.

## Positive closures / execution evidence

- Focused R8 closures excluding the Git-dependent replay test: `8 passed, 1 deselected in 8.08s`.
- Full R6 audit in the isolated copy: baseline `7 passed`; all 8 listed mutants reported CAUGHT; restored baseline `7 passed`; `MISSED: 0`; process rc 0. The run took each mutant through a separate pytest invocation and did not edit the target.
- `c6_04` value claim is positively closed: the isolated audit reports its mutant CAUGHT, and `test_d8_08` passed. That test (`tests/test_r8_codex.py:320-333`) applies the two-site old-rule mutation to a separate module and directly observes key `100` consuming span `222.0`, rather than treating a `KeyError` as evidence.
- R8-08 schedule instrumentation is positively present and exercised: `_hook_open` separates reads (`v`) from callback invocations (`published`) at `tests/test_r6_internal.py:969-982`; `test_c6_01` checks `published == 1` for every enumerated schedule at line 1031 and binds each schedule's expected attempt B to observed B or explicit incomplete at lines 1033-1043. The focused R8 test also checks the 2-read/1-publication and unreachable-hook controls (`tests/test_r8_codex.py:301-319`).

## Exact run environment

Dependencies were installed only under `outputs/r9_evidence_pydeps`. Clean mutation copy: `outputs/r9_evidence_clean_29ef5058/bms-balancing`. The source worktree already had mode-only local modifications; all reviewed content was checked against the pinned commit object, and it was not mutated.

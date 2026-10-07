# GATE94 independent static code review

Date: 2026-10-07. Scope: G93-N1 only, with supporting test and mutation-source review. No received source import, execution, pytest, probe, replay, research calculation, COMSOL, restoration, or receipt generation was performed. GitHub reads and reviewer-owned text comparisons only.

## Verdict

G93-N1's narrow code correction is accepted by static inspection. No new blocking finding was identified in the submitted two production hunks. This conclusion does not independently attest to submitted runtime logs, does not close the whole stage-4/bundle-6 scope, and is not execution GO.

Target: `0ab2924f465461f1224d66c8f0a8c6013e857c6b`.
Baseline: `d7a97aa57ea926916d56c985ee4bc2bed96fa81a`.
Repository: `yonghoon7153-source/Yonghoon-DEM-DFT`.
Submitted source_digest: `044e4f5513011a9b`; this subreview did not invoke or independently recompute the repository digest algorithm.

## Pinned source evidence

All paths below are under `degradation-degeneracy/` and line numbers refer to the target commit.

| File | Fetched Git blob SHA |
|---|---|
| src/io.py | 53797cd3bce110ef9822532a000b29a564897f65 |
| tools/preserve.py | e8f3105b784fc8ff8e184b3e671a2d68d138ad9f |
| tests/test_gate93_n1_v3_envelope.py | 8541165758dc0490ae578867d20b4970a234cb0c |
| tests/test_gate92_stage4_linkage.py | 49d64dedcf7a752e2ac4104acbc1e22251e46742 |
| tests/test_gate82_residuals.py | b4dde3d6bd02c0811b34192506307da323337b22 |
| tests/test_gate85_closure_members.py | 0f6cb03fac947e739a817706f3df6068e44578a9 |
| docs/22p_gap/mutation_replay.py | 4e4a5cfccbaefc924bf504d5772c85c76cb52f0e |

The baseline io.py blob is `e0c56c78531a81e0426e0e7492b49d22a5af0d68`. Applying only the two submitted hunks as reviewer-owned string replacements to its fetched text reproduced the entire target io.py text exactly. The baseline and target preserve.py blob SHA and full fetched text are identical. This verifies the historical reader and axis helper were not altered by this change; it is not a substitute for the main review's RUN_SCOPE tree comparison.

## Control-flow proof

1. `validate_provenance` calls `_stage3_checks` only under declared `sig_version == 6` (io.py:2223–2229). Historical sig5 dispatch is unchanged.
2. `check_planned_envelope` still dispatches a v3 envelope to `check_envelope` (preserve.py:3275–3284); a valid closed v3 returns an empty error list under the unchanged v3 validation rules (3126–3163).
3. The independent `stage3_axis_from_envelope` helper rejects every non-v4 schema before reading any v4-specific nested field (preserve.py:6642–6645). A v4 value must additionally pass `check_envelope_v4` (6646–6649) before axis projection.
4. The changed code initializes `ax_err = None`, catches that helper's `PreserveError`, and preserves its diagnostic in both `ax_err` and the existing axis-failure list (io.py:1904–1910). The ordinary copied-axis mismatch list is distinct (1917–1919).
5. For a valid v3 under sig6, `ebad == []` but `ax_err` is a nonempty string. Therefore `v4_bad` is nonempty (io.py:2026), the four rederivation/recalculation checks are explicitly `(False, why)`, and the function returns (2027–2032). The only call to `_stage3_rederive` in this file is below that return (2039). The prior raw access at 1686 is consequently unreachable for the target fixture.
6. The four failed keys are `후보_재유도`, `실현_재계산`, `restart_예산_완주`, and `관측_roster_재구성`. The diagnostic names the planned-leg/v4 boundary (2029). The outer validator preserves failures and formats them with reasons (2576–2583); the legacy budget check cannot overwrite the sig6 result because it requires `_gen != 6` (2557–2559).
7. Before the new guard, `check_execution_record` rejects non-v4 plans as an ordinary list of problems (preserve.py:3306–3308). For the supplied otherwise-normal record/map/fits fixture, it does not dereference v4-only plan keys and does not prevent reaching the new guard.

Pinned links: [axis error capture](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0ab2924f465461f1224d66c8f0a8c6013e857c6b/degradation-degeneracy/src/io.py#L1904), [early-return gate](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0ab2924f465461f1224d66c8f0a8c6013e857c6b/degradation-degeneracy/src/io.py#L2026), [helper schema guard](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0ab2924f465461f1224d66c8f0a8c6013e857c6b/degradation-degeneracy/tools/preserve.py#L6640).

## Preserved behavior

- Normal v4: the unchanged reader and helper accept it; `ebad == []` and `ax_err is None`; the new guard is false. All downstream existing checks and rederivation remain reachable when map/fits are otherwise valid.
- planned_id-only mismatch: the mismatch is still handled only by the conjunction at io.py:1897–1900. The envelope is unchanged, so reader/helper success and the new gate are unaffected. `planned_id` is not among the nine copied-axis comparisons and is not read by `_stage3_rederive`; the record check compares record.planned_id against the envelope digest independently (preserve.py:3311–3312). The patch therefore does not convert this case into a v4-boundary block.
- Other copied-axis-only mismatches: `ax_bad` can be nonempty while `ax_err` stays None. Using only `ax_err` in the gate preserves the existing independent comparison meanings.
- Invalid v4 with reader errors, including the existing philox fixture, remains blocked because its errors remain in `v4_bad`.

## Regression and mutation review

- The new v3 fixture retains leg_id, protocol_generation, pairing_design_sha256, source_digest, candidate_mode and retention; it maps ordered objectives to sorted v3 objectives and sums the stage budgets (test_gate93_n1_v3_envelope.py:26–42). It explicitly asserts `check_planned_envelope(v3) == []` before installation.
- The test uses the shared real base output copy, rebinds s3.planned_id and record through `_forge_stage3` (test_gate82_residuals.py:51–67), then re-signs manifest/fits/seal using the existing helper (test_gate85_closure_members.py:69–83). The unchanged pairing design and matching design SHA let the old implementation reach io.py:1686 rather than fail earlier on an unrelated design mismatch.
- `_validate_no_rederive` spies on the real implementation and calls `IO.validate_provenance`; its spy returns the real function result and catches no exceptions (test_gate92_stage4_linkage.py:105–115). Thus an unexpected KeyError cannot be mistaken for a passing rejection.
- n1 asserts zero rederivation calls, stage3_planned_envelope failure, all four rederivation keys in fail, and a planned-leg/v4 diagnostic (test_gate93_n1_v3_envelope.py:45–54).
- c1 asserts no ordinary validation failures and a real rederivation call (57–61).
- c2 asserts envelope-check failure, a real rederivation call, and absence of the new boundary diagnostic (64–71). On its own c2 does not assert the exact failure set. That stronger existing invariant is covered by k06[planned_id] (test_gate92_stage4_linkage.py:392–410) and `_only` (95–102), which requires exactly stage3_planned_envelope. This is a nonblocking test-description precision point, not a missing product fix.
- The new mutation changes only `v4_bad = list(ebad) + ...` to `v4_bad = list(ebad)`, restoring the original gap, with `test_g93` selection (mutation_replay.py:2417–2421). EXPECT requires the exact n1 node and the specific `KeyError: 'parameter_order_sha256'` witness (7650–7657). c1/c2 are controls, not the expected failing nodes.
- The old failed-envelope mutation changes only its source anchor from `if ebad:` to `if v4_bad:` and still replaces it with `if False:` for the same k04_env witness (2393–2396).

These are source-inspection statements only. Actual RED/GREEN, targeted mutation, smoke and full-suite outcome acceptance belongs to the separate raw-log review.

## Scope limits and carry-forward

The fix proves the specific v3-envelope gap and preserves the requested controls. It is not a general claim that every combination of malformed record, optimizer, run_spec or other object now returns every named check. Existing earlier exits remain: for example missing/unreadable execution_record returns at io.py:1927–1929 and unknown record schema returns at 1932–1934, before the four-key guard. That behavior predates these hunks and is not a new G93-N1 blocker.

No request is made here to rerun or broaden tests. The 39 position mutations, C8 resumption, C7 envelope–ledger binding, the three excluded objects, and research/execution authorization remain outside this narrow acceptance.


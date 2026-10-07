# GATE94 regression / mutation static review

Date: 2026-10-07. Scope: G93-N1 narrow closure only. No repository code was imported or executed; no pytest, mutation replay, analysis program, or COMSOL was run by this reviewer. GitHub connector reads and local text/hash operations only.

Conclusion: no actionable blocker found in the requested G93-N1 regression coverage. The new valid-v3 regression, real-validator call-through spy, normal-v4 control, planned-ID control plus existing exact-set test, and preserved RED/mutation observations support the narrow closure. This is not execution GO and does not reopen the 39-location, C8, C7, or excluded-object scopes.

## Coordinates and sources

- Code target: `0ab2924f465461f1224d66c8f0a8c6013e857c6b`; prior target: `d7a97aa57ea926916d56c985ee4bc2bed96fa81a`.
- Original new test path, obtained from the target commit diff: `degradation-degeneracy/tests/test_gate93_n1_v3_envelope.py` (71 lines; blob `8541165758dc0490ae578867d20b4970a234cb0c`).
- Target commit changes the test, `docs/22p_gap/mutation_replay.py`, and the two stated sites in `src/io.py`. Historical reader and fixture helpers are not part of that commit's change.
- Reviewed raw development logs 00, 01, 02, 03, 04a, 04b at evidence commit `016e970f6`; exact UTF-8 copies and source excerpts are in `evidence/regression/`.
- Canonical new-test source: https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0ab2924f4/degradation-degeneracy/tests/test_gate93_n1_v3_envelope.py
- Canonical code change: https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/commit/0ab2924f465461f1224d66c8f0a8c6013e857c6b

## Fixture and real path

1. `_as_v3` (new test lines 25–42) starts with the base v6 run's existing v4 envelope, retains leg ID, protocol generation, pairing design SHA, source digest, candidate mode, and retention days, and derives sorted objectives and total budget from that envelope. It asserts `PV.check_planned_envelope(v3) == []` before installing the v3 replacement. The unchanged historical reader routes planned-leg/v3 to `check_envelope` (preserve.py 3275–3284); that reader checks the closed key set and the relevant value contracts (3126–3163).
2. `G82._forge_stage3` (51–67) recalculates `stage3.planned_id` from the replaced envelope and rewrites record planned_id/protocol_generation. `_rewrite_record` (43–47) recalculates record_digest. The design itself is not changed, so its SHA remains equal to the saved v3 value; the old rederivation reaches the specific missing-v4-key access.
3. `G85._resign` (69–83) recalculates the manifest signature, sets fits.run_sig to the same value, and invokes `_reseal_fits`; G82 33–40 updates the six fits-seal fields. The fixture is therefore self-consistent along the plan/record/signature/seal chain rather than failing at an unrelated stale hash.
4. `runs["base"]` comes from the existing real v6 writer fixture (G92 54–66, G81 601–622/714–719). This is a description of submitted test source, not a reviewer execution.
5. `_validate_no_rederive` (G92 105–115) saves the real `IO._stage3_rederive`, records each call, and calls the real function. It invokes actual `IO.validate_provenance(out)` and catches no exceptions. The spy observes; it does not itself prevent rederivation. The production early-return guard prevents it, and `assert calls == []` in n1 proves the expected observation in submitted GREEN runs.

A valid historical v3 envelope remains invalid for this v6 path by design. In particular `check_execution_record` independently returns its structured v4-boundary failure (preserve.py 3306–3308). Self-consistent does not mean the submitted v6 artifact should validate overall.

## Failure shape and controls

- With valid v3, historical `ebad` is empty, but `stage3_axis_from_envelope` rejects its schema with PreserveError (preserve.py 6640–6649). io.py 1905–1912 retains that as `ax_err`; io.py 2026–2032 adds it to `v4_bad`, records the same `(False, why)` under all four keys, and returns before rederivation.
- The four keys are exactly `후보_재유도`, `실현_재계산`, `restart_예산_완주`, and `관측_roster_재구성`. The reason prefix is exactly `planned_envelope 가 유효한 planned-leg/v4 가 아니어서 다시 유도 · 재계산하지 않는다: `, followed by the retained envelope/axis reason.
- n1 (45–54) requires no rederive calls, stage3_planned_envelope in fail, all four keys in fail, and the v4 boundary text in every corresponding check. It does not assert that these are the only failures or freeze the full reason literal. That is appropriate: stage3_축_유도 and execution_record also fail on this deliberate v3/v6 mismatch. The implementation supplies the uniform structured reasons directly.
- c1 (57–61) requires no substantive failure through `G81._fails` and a real rederive call. `_fails` excludes only clean_worktree and 코드_identity (G81 51, 722–723), which accommodates development/mutation checkouts; it does not suppress stage3 failures.
- c2 (64–71) changes only stage3.planned_id and resigns via `_edit_s3`. It requires stage3_planned_envelope failure, a rederive call, and absence of the boundary-blocking reason. Alone, c2 does not enforce the claimed exact singleton failure set.
- The existing `test_g92_k06_an_independently_recomputed_key_forged_alone_is_refused_by_its_own_check[planned_id]` fills that precision gap: _K06 identifies stage3_planned_envelope (392–410), and `_only` enforces the exact substantive failure set (93–102). It is in the submitted stage3 suite. Consequently no new blocking coverage gap is raised for c2.
- Static behavior agrees: a planned-ID-only mismatch does not change env, so both ebad and ax_err remain clear; the new guard does not inspect the planned-ID comparison. Normal v4 likewise retains the old rederive path.

## RED/GREEN and mutation observations

| Evidence | Observed result | Interpretation |
|---|---|---|
| 00 | head 3a7d68069; 1 failed, 2 passed; rc=1; failure at io.py:1686, KeyError parameter_order_sha256 | n1 reaches the real rederive via the spy; c1/c2 pass on the pre-fix code |
| 01 | head 3a7d68069, dirty 2; 204 passed; rc=0 | development GREEN before helper-only simplification |
| 02 | same head, dirty 2; helper-reuse annotation; 204 passed; rc=0 | development GREEN after simplification |
| 03 | G93 selector chooses 3 nodes; only n1 observed failed with KeyError parameter_order_sha256; rc=1 because EXPECT was not yet registered | EXPECT capture, not a successful verification run |
| 04a | one executable G93 scenario, 3 nodes, ran 1; expected call-stage failure; rc=0 | registered G93 mutation verified |
| 04b | one executable G92 envelope scenario, 1 node, ran 1; expected call-stage failure; rc=0 | updated guard-name preimage verified without changing its old witness |

The G93 mutation (mutation_replay.py 2417–2421) replaces only the new v4_bad expression with `list(ebad)`, restoring the old gate's semantic weakness. EXPECT 7648–7657 identifies only n1 and the deterministic `KeyError: 'parameter_order_sha256'` witness. The G92 mutation updates its preimage to `if v4_bad:` and still replaces the whole condition with False; its unchanged EXPECT 7572–7579 requires the existing call-spy assertion.

The runner checks a passing baseline, unchanged node inventory, mutant rc=1, call-stage failure, exact expected failed-node set, and per-node meaning witness (3090–3175). The witness is matched against the extracted failure meaning line, not arbitrary source text in a traceback (3233–3262). Thus the G93 declaration distinguishes the intended missing-key regression from collection/setup failures or unrelated failing controls.

Evidence precision limits: logs 01/02 contain aggregate 204 summaries but no full invocation or node-by-node inventory; 02 is a short preserved tail. They are explicitly dirty development observations, not proof of clean target identity. The later clean full validation and run-scope identity checks are handled by the main review. No independent reexecution claim is made here.

## Local byte verification

The six fetched log files were saved through apply_patch and then measured with PowerShell Get-FileHash; all sizes and full SHA-256 match gate94_evidence/README.md:

| File | Bytes | SHA-256 |
|---|---:|---|
| 00_red_test_g93_1failed_keyerror_io1686.log | 6228 | b0eca85bdd6c359ee407848e995bbebfac0265bb4a63b41d134d5b7b2d3002b2 |
| 01_green_204passed.log | 921 | b71250c704728b27fa46b14ae2c7a0ff520a3c89632f98bd0cba7c789cb89993 |
| 02_green_after_helper_reuse_204passed.log | 312 | 8899a63b17011500db1c242a00b9f5f76e574f9fc49770a9e559c1a9bbdeeb3b |
| 03_replay_g93_emit_expect.log | 944 | 7c390b9ce13ac232bda49cca186849b429144c8f94f12d39e1a74ad1d5491221 |
| 04a_replay_g93_rc0.log | 389 | 3ddc3e867be9623ad54a9614cb2dbfda8302e55f3cac42e812cd24767834b82e |
| 04b_replay_g92_k04_env_updated_rc0.log | 424 | ab722ad5ee6b757dac999df1b554e0e2c6384806873c31b0f20b20846c54ee52 |

No code/test changes or external writes were made. Full-regression, receipts, G93-N2 archive provenance, and final decision remain the main review's responsibility.

# Runner / restoration recheck — a30fe150e21f66aea2f1c360593e1cd781689b14

Scope: ULKR-05, ULKR-06, ULKR-08, ULKR-11; Q5 grammar prerequisite and Q6 UC retry. Read-only production review. No LIGGGHTS, MPI, WSL, SSH, SLURM, source edits, ledger edits, or Git writes.

## Executed independent file-to-restoration-to-next-gate checks

`probes/runner_recheck.py` constructs its own complete three-particle synthetic fixture using the new columns, S0/R_END timestamps, stage receipts, technical screens, original/G2 atom/contact/mesh comparisons, real previously accepted H0–H5/SYN verdict, and complete valid three-window UK evidence. It does not call the production `_mk_rj` selftest constructor. The unchanged production `kebase` creates a legitimate baseline; the unchanged `restore_verdict` writes a verdict that the unchanged `gate(..., UB)` then consumes. Per-case inputs and full verdicts are retained under the `run_dir` recorded in `evidence/runner_recheck.json`.

Positive baseline: RESTORED, UB allowed. Twenty-two negative cases reject as expected:

- Truncated PRE/POST; PRE NaN; duplicate POST ID; wrong UN identity.
- Wrong timestamp separately in PRE, POST, R_END, and UN.
- Nonzero stage receipt and ERROR screen separately for Ut0, R, and UN.
- G0 status FAIL; RJ final `fails=1`; missing final RJ line.
- Missing SYN, wrong sign, SYN FAIL, missing force-timing PASS, wrong history schema.

This independently closes the original ULKR-05 malformed/failed-UN counterexamples and the original ULKR-08 missing-SYN counterexample. Source locations: `ul_reader.py:994–1060`, `1061–1131`; `ul_gates.py:349–361`. Missing observations become UNCONFIRMED; runtime evidence failure becomes SYNTAX_FAIL; G0/value failures become VALUE_MISMATCH. The successful actual history verdict remains accepted.

## Residual R-1: captured reader failures are ignored by the next submission gate

Suggested new P1 (or a narrowly scoped remaining part of ULKR-05/11), not a claim that rc capture itself remains missing.

- `run_unload.sh:197–203`: `reader()` captures `reader_<command>_rc`, assigns nonzero RRC, but does not increment FAILS.
- `run_unload.sh:220–222`: restore is followed by kebase when the LMP prerequisites passed; a failing kebase sets aggregate RRC=2.
- `run_unload.sh:274–278`: job end records both `fails=$FAILS` and `reader_rc=$RRC`, then returns RRC.
- `ul_reader.py:863–875`: `_job_restored` examines only the last end line's `fails`; it never reads `reader_rc`. `gate` consumes it at lines 907–913 (also the 10:0 EXT path at 896–900).

The simple receipt mutation `end=x fails=0 reader_rc=1` produces RESTORED and UB allowed. A stronger probe demonstrates an actual production-process route without inventing a RESTORED status: invoke the unchanged restore CLI with its stdout pipe closed. `ul_reader.py:2387–2392` writes `restore_verdict.json` before stdout is flushed, then the process exits **120** on its output error. Invoke unchanged kebase the same way with the complete UK fixture; it newly writes `ul_base.in` (S2 = 2.24e-6), then also exits **120**. There is no previous base file: the probe removes only its own generated baseline before those calls. The source-defined runner bookkeeping is `reader_restore_rc=120`, `reader_kebase_rc=120`, `end=x fails=0 reader_rc=2`; the actual gate still allows UB. Stored case: `actual_restore_cli_closed_stdout`.

The entire Bash runner was not executed; only the unmodified production Python CLIs, real file output, and real next gate were executed. Aggregate runner fields are reconstructed exactly from the cited source. A closed output channel is one reachable technical failure after receipt publication, not a claim of a changed scientific result. The contract currently promises technical failure cannot be reused as approval. Minimal correction: require the final aggregate `reader_rc=0` as well as `fails=0` (missing/malformed/nonzero must refuse), and cover the actual persisted-artifact/nonzero-command case. Preserve ordinary arm `UNIDENTIFIED` with rc=0.

## Residual R-2: fractional atom IDs are silently converted to an existing integer ID

Suggested new P2 input-validation gap, distinct from the original wrong-integer-ID case now rejected.

`ul_lib.py:364` reads all fields as floats. `ul_reader.py:1027` converts observed IDs with `int()` before comparing to S0; `_hist_cols` at 1162–1163 repeats the conversion. Change only UN's first ID from `1` to `1.5`, leaving all three rows and all other data intact. The parser considers the frame finite and complete; `int(1.5)` aliases it to ID 1, and both restoration and UB gate pass (`fractional_un_id`). The preceding control `id=999` is rejected, so this is specifically truncation rather than absent identity validation.

Trusted LIGGGHTS custom dumps normally emit integer IDs, so this is a malformed-input defense gap, not a natural output of the normal simulator and not evidence that the accepted actual history test is wrong. The request nevertheless promises typed unique identity and failure-closed malformed observations. Require exact finite positive integer IDs before conversion in shared frame consumers, including S0. Do not expand this into a broad new scientific claim. Source contains the same conversion pattern in other consumers; the reader reviewer should assess their scope.

Two additional deliberately inconsistent inputs (`stage=G0 rc=1` paired with a PASS G0 JSON and final fails=0; and a UN receipt claiming a different screen/procs paired with a valid real screen) also pass. They are recorded for completeness but **not promoted to findings**: the ordinary runner does not produce those combinations, and no reachable path was shown.

## Source-only hardening subnote: EXT fallback and reader error classification

Not promoted to a separate finding or release blocker. `run_unload.sh:226–233` calls `reader s0p`, branches to EXT2 whenever RRC is *any* nonzero value and the end checkpoint exists, then explicitly resets RRC=0 before the second reader call. Consequently an unexpected first reader rc=1 (program error) followed by a successful EXT2/read leaves final `reader_rc=0` and a successful runner exit, although the manifest retains the earlier `reader_s0p_rc=1`. It also uses the program error to authorize the extension. The intended scientific first-window failure has CLI rc=2 (`ul_reader.py:2398–2401`); that should remain the registered fallback, whereas rc=1 or other unexpected process failures should stop and stay nonzero. This is a source branch observation, not an executed Bash or actual CLI rc1 counterexample, and its trigger requires a first-call program/I/O error that does not recur on the second call. A Linux mock should distinguish first `s0p` expected rc2 from first `s0p` exception rc1 and assert final behavior.

## ULKR-06 / ULKR-11 source recheck and execution limit

The original unsupported-RESUME replay is fixed in source: `run_unload.sh:50–54` rejects UTc, G_*, RJ, RJ2, EXT before kit copy/preflight; `75–85` requires the same bed/job, `resume=0`, `gate=ALLOW`, no previous `screen_a2.txt`, and no completed summary. The normal-arm branch `237–243` chooses its own last restart plus paired state; `161` compares the original copied deck; `169–171` writes the second screen/log separately; `140–149` and `150` append manifests. The original source claim is closed, with normal/second-attempt shell behavior still awaiting an executable environment here. A failed validation before starting LMP does not create screen_a2 and therefore does not consume the one actual resume; it can append an aborted attempt to the manifest, which is provenance rather than an overwritten record.

G0 failure now stops Ut0/R/UN/UK (`208–210`). Ut0 failure stops R/UN/UK (`211–213`). R/UN failure stops UK (`214–218`). Reader `arm`, `select`, `restore`, `kebase`, and `s0p` all use the rc-capturing wrapper. Normal scientific arm UNIDENTIFIED still has CLI rc=0 (`2402–2408`), preserving the intended distinction. The original ULKR-11 capture and short-circuit changes are present; the new receipt-consumption gap R-1 remains separate.

A harmless Git Bash startup attempt failed before any runner code: `C:/Program Files/Git/bin/bash.exe --noprofile --norc -c 'printf git_bash_ready'`, rc=1, `NtCreateDirectoryObject(\\BaseNamedObjects\\msys-2.0S5-1888ae32e00d56aa): 0xC0000022`. No escalation or real simulation was attempted. This is an environment limit, not a scientific or kit failure. Root owns aggregate baseline selftests; do not count this note as independently executed M7/M11–M17.

## Q5: grammar PASS can remain a procedural prerequisite

REG §14-9 (`dem_unloading_ps45_prereg_20261009.md:905–912`) explicitly requires the real grammar fixture PASS before main R and explicitly says the runner does not enforce it. This faithfully preserves the prior review §6/§10 prerequisite: neither section required that grammar be folded into the physical RESTORED JSON. It is therefore acceptable as a clearly maintained operational gate, provided the actual result, sealed kit, binary provenance and receipt are reviewed before GO. No native grammar PASS is present in this review task; Python/source checks are not a substitute.

A code preflight that requires a provenance-bound grammar PASS would reduce accidental omission and is reasonable if the author chooses it. It need not redefine RESTORED or rerun H0–H5. Its absence is not, by itself, a newly discovered violation of the agreed minimum. Any overall GO must remain conditional on the native prerequisite, not silently infer it from SYN.

## Q6: UC fresh attempt is coherent, but is not checkpoint resume

The actual `decks/ps_7_3_r45/in.UC.liggghts` has no `write_restart` / `restart_unload` output; it ends NOMOVE_DONE at line 196. Although the policy whitelist includes UC, `run_unload.sh:238–241` cannot find the required restart/state pair and fails before launching LMP. REG §14-4 lines 875–878 expressly records that limitation. This is safe and coherent: no need to invent checkpoint support for UC. A repeat is a fresh attempt from S0 after preserving the failed folder, passing normal gates, and retaining the technical-failure history. It must not be described as successful RESUME or used to reset the registered attempt/approval policy. Optional wording cleanup is to label UC as fresh-attempt-only in the supported-resume list.

## Reproduction

Run `python -X utf8 -B probes/runner_recheck.py` from any directory. It creates a new uniquely named synthetic evidence directory and updates only `evidence/runner_recheck.json`; prior inputs are retained. This writes no production source. The output records source SHA256 values and the pinned commit. Total: one positive control, 22 expected rejections, four additional integrity probes (two narrow residuals, two unpromoted), and one actual Python CLI publication/failure probe.

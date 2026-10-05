# G1 / Q1–Q2 independent review

Snapshot: `30c8205c5efb3873ae6fa856881fa184bd041d4d`. Read-only production audit; only this evidence directory was written. Small CPU fixtures and process-local mutations only. No real-grid replay, GPU, campaign, Git mutation, or production patch.

## Decision

**G1 HOLD on whole-result/fail-closed acceptance.** The thirteen claimed corrections materially address their original defects; the per-solve application-receipt contract is not, however, a per-solve numerical-validity contract. A new small actual-producer test publishes a collector result and `jb` from an unconverged auxiliary solve, marks the collector complete, and passes `check-arm`. Fix the two collector convergence gates and shared evidence contract before interpreting all four solves as accepted scientific results. Separately correct the tie-incorrect Spearman statistic in the RINT-03 evidence tool. Neither finding argues for reverting the AM ownership correction.

### F-G1-01 — P1: auxiliary CG failures are accepted as complete collector results

Locations (relative to `source/`):

- `scripts/mpm_webapp_payload.py:2309` and `:2313`: wetted/bare `solve_sigma_z` calls; receipts follow each call.
- `scripts/mpm_webapp_payload.py:2318`: bare `phi` is sufficient to emit particle `jb`; numerical convergence is not checked.
- `scripts/mpm_webapp_payload.py:2334`: only `reason` or nonpositive sigma prevents `R_geom`; `:2337` computes/clips it, `:2359` marks the collector complete whenever it is non-null.
- `scripts/run_contract.py:765`: explicitly but incorrectly treats collector as having no CG convergence. `:766`–`:787` checks its numeric result block then bypasses `conv_ok`; the other solve components use `conv_ok` at `:802`.
- `scripts/run_contract.py:824` and `:846`: application receipts intentionally contain no convergence tuple. `scripts/step3_sigma.py:1176` emits `solved=True` after CG even on the warning path.

Reproduction: `probe_adversarial.py` builds the production smoke raster, runs the actual payload producer, and changes only `CG_MAXITER` to 1 during either solve call 2 (wetted) or 3 (bare), restoring it immediately. No numeric result fields are forged. Normal, wetted-only, bare-only, and main-only controls are recorded.

| Actual producer case | Auxiliary sigma S/cm (raw) | CG info / residual | Published / collector / check-arm | R_geom ohm cm² |
|---|---:|---|---|---:|
| Normal | wetted = bare = 0.0009486874831110222 | 0 / 9.783687086144589e-9 | yes / complete / exit 0 | 0 |
| Wetted maxiter 1 | wetted = 0.007178713043478262 | 1 / 0.3464101615137754 | yes / complete / exit 0 | 3.8 |
| Bare maxiter 1 | bare = 0.007178713043478262 | 1 / 0.3464101615137754 | yes / complete / exit 0 | 0 (clipped) |
| Main maxiter 1 | main invalid | actual nonconvergence | **not published**, producer exit 3 | — |

The invalid auxiliary sigma is 7.57× the normal answer. Main sigma remains 0.0010352120036449418 with residual 9.561089107260143e-9 in the auxiliary mutations. The three electronic receipts remain `applied`, `solved:true`, and carry all 3,816 interface faces. The shared interface check returns `(True, None)`; actual producer and actual `sr01_stamp_compare.py --check-arm` both exit 0. Their logs contain the CG warning, so this is not a logging-only omission. Main-only failure proves the existing primary gate is working and isolates the missing auxiliary gate.

Affected conclusion: successful receipt validation proves application of the requested interface table, not that the collector correction or particle `jb` is usable. The same shared component-evidence logic is called by the final verifier (`sdcp_gain_verdict.py:741`), but this audit executed producer/check-arm directly, not a synthetic final-verdict campaign.

Minimal fix: preserve independent wetted and bare `cg_info`, `resid`, `unconverged` evidence; require the existing finite `conv_ok` conjunction for **both** before publishing `R_geom`, `jb`, or collector `complete`. Extend the shared evidence validator, not only a producer log check. Keep application receipts semantically distinct from convergence evidence. Test each auxiliary maxiter failure independently, main-only control, missing tuple, contradictory tuple, and nonfinite residual. This residual defect also exists without r_int; it is not a new same-sid/interface-law error. P1 is assigned to silent acceptance of an unreliable scientific result; if severity policy treats this opt-in diagnostic path as P2, the G1 acceptance condition is unchanged.

### F-G1-02 — P2: the evidence tool's “Spearman” is wrong with ties

Location: `scripts/rint03_je_compare.py:57`–`:62` uses double `argsort` (distinct ordinal ranks); `:97` publishes it as `spearman_old_new`.

Actual function: `[1,1,2]` versus `[1,2,2]` yields **1.0**, while average-tie Spearman is **0.5**. Five zero entries versus five zero entries yields **0.9999999999999999**, whereas Spearman is undefined for a constant vector. Zero/tied particle currents are valid inputs. Thus the tool can overstate ranking agreement and its constant-vector guard does not work except at length one. The existing nine tests all pass.

Minimal fix: average tied ranks (or `scipy.stats.spearmanr`), explicitly return JSON null/status for constant vectors, and add both examples. Include tie counts or retain per-particle vectors for audit. Top-decile selection at `:82`–`:85` also needs an explicit cutoff-tie convention if used for evidence. The three supplied historical JSONs do not include tie counts or vectors: this review **does not claim** their 0.270/0.954 statistics are numerically wrong; it cannot establish the no-tie prerequisite. Until checked, treat rank summaries as provisional. The ownership mask and contamination-count evidence do not depend on this statistic.

## Thirteen claimed fixes

“Closed” below is restricted to the original claim, not a proof of all surrounding physics or all future mutations.

| Item | Assessment | Evidence / scope |
|---|---|---|
| RINT-01 | Closed | AM-only same-sid owner set, parser/API/face enforcement in `step3_sigma.py:175,223,245,315`; actual RINT selftest and integration run pass. Non-AM pid inheritance is no longer accepted as same-material particle identity. |
| RINT-02 | Application-omission class closed; numerical acceptance **HOLD** | Independent requested tables and exact four named receipts in producer `:2946`–`:2959`; shared checker `run_contract.py:883`; all consumer call sites wired. Actual integration 49/49 includes original omission mutations. New maxiter mutation F-G1-01 survives. |
| RINT-03 | Ownership correction closed; historical ranking evidence qualified | `step3_sigma.py:1216` restricts current averaging to final sid 1/2 and valid AM pid; `PER_PARTICLE_CURRENT_DEF` at `:180`; producer `:2104`. Independent old tangent-raster counterexample rerun on new code: old/new ratios 126.5602 and 120.9457; new output equals explicit final-AM mask bitwise. See Q2. |
| RINT-04 | Closed as scope declaration, not full dissipation-map implementation | `step3_sigma.py:1626` bulk-only metadata and producer `:2216`–`:2219` excluded interface/plate terms and separate interface share. Integration F3 passes. Interface I²R is explicitly outside this map. |
| RINT-05 | Closed by explicit exclusion | Producer `:1384` rejects r-ON STEP4 grid export; `:2794` disables r-ON reaction solve. Integration tests exercise both. This does not implement interface resistance in STEP4/reaction and must not be advertised as such. |
| RINT-11 | Closed | Zero-table OFF regression includes sigma, n_dof and per-AM je bit identity; integration F4 and RINT selftest pass. r-OFF old-versus-v2 ownership remains the deliberate version exception. |
| RINT-12 | Closed | Strict sid/r numeric validation; no bool/string coercion into physics. RINT parser/API tests pass. |
| RINT-13 | Closed in inspected contract | `sdcp_gain_verdict.py:147` derives interface_model from both table axes; compare-dirs checks parent-axis change at `:2632`. Root owns final-verdict baselines; integration E2 confirms registry derivation. |
| RINT-14 | Closed | Producer `:1376` contradictory disabled-channel/STEP3 requests reject; actual-channel checks at `:1482`. Integration and RINT selftests pass. |
| RINT-17 | Closed for naming scope | Viewer terminal `R_int(셀 단자)` labels distinguish it from area-specific interface r_int. Static consumer inspection, not browser visual QA. |
| RINT-18 | Closed for inspected legend scope | Viewer `jouleScopeNote:85`, `rxnScopeNote:103`, and phase/interface headings `:5399`–`:5416`; main/compare scopes are annotated. No claim that excluded physics is solved. |
| RINT-19 | Closed for intended r-ON diagnostics | Context hashes final sid, pid and conductivity; `step3_sigma.py:183,358` validate. New direct sid mismatch and sigma mismatch probes both reject. Exact fingerprint checks protect context reuse, not an authenticity boundary against a forged entire payload. |
| RINT-20 | Closed | Integration E1 checks actual manifests for off/e_on/ei_on/rxn_on/joule_on/e_zero: no unclassified keys; independent requested/receipt fields classified. |

## Q1 — Does the receipt remedy close the class or just four mutations?

It closes a meaningful **application omission/mismatch class**, not merely four AST spellings: expected tables come from requests, every planned solve has an independently produced named receipt, and one shared validator checks exact keys, model/unit/table/face evidence, same-sid pid use, disabled plan and contradictory state. Dropping or changing a solver table cannot pass merely because another solve supplied a plausible model string.

It does not close every wetted/bare failure class. In particular it does not attest convergence, nor is a receipt a cryptographic binding of arbitrary downstream fields to a particular solved array. F-G1-01 is an actual producer counterexample within normal solver behavior, not an attacker forging both request and receipt. A failed receipt may legitimately describe a nonsolvable result; cross-field `failed` versus `component.complete` consistency is useful additional hardening, but numerical evidence must have its own gate.

## Q2 — Is r-OFF je change a justified declared exception? Remaining consumers?

**Yes.** The AM diagnostic must average cells finally owned by AM, not any cell retaining an AM slot number. An iid for interface identity alone cannot fix that unrelated diagnostic ownership error. The old same-raster counterexample against this new source gives:

- Old je `[0.03831624353328062, 0.037756103759881546]`.
- Actual new je `[0.0003027511154070284, 0.00031217396939968564]`.
- Exact equality with explicit sid-AM mask. All original fibre input points are outside the AM spheres; stamped overlap, not point-center overlap, is sufficient to expose the old defect.

Keep sigma/phi OFF invariants separate from **versioned je/jb semantics**. The integration OFF/zero-table identity test passes for the new definition. This correction changes a diagnostic, not the r-OFF transport equation.

`step4_dyn.py` does not consume particle `je`/`jb` (direct search); it reads the grid and makes its own currents/reaction surfaces. Thus the old per-AM averaging is not a STEP4 numerical input in the inspected path. Viewer v2/legacy/unknown labels exist (`viewer3d.js:63`) and A/B generation mismatch warnings are wired into je and delta comparisons (`:7031`, `:7052`); legacy payloads are not silently relabeled v2. Its CSV particle export (`:5441`) still exports raw je/jb without a definition metadata field: preserve `je_definition` in external exports when using them for quantitative comparisons. Also, pre-existing viewer wording calls canonical-main je “wetted” (`:3821`, `:5409`) even though producer je comes from the main solve, not the auxiliary wetted solve. These are provenance/label caveats, not evidence that the AM ownership fix failed.

### Historical three-grid evidence

The supplied JSON/README are author-pasted, voxel-0.4 data, not independently replayed grids. They support a directionally consistent magnitude observation: VGCF4 97.4142% old summed current mass from non-AM cells, median old/new 42.6079; VGCF1 6.3589%, median 1.0461; no-carbon control zero contamination and ratio 1. The reported “mass” is summed cell current proxy, not charge or material mass. These grid-dependent magnitudes should not be promoted to converged-resolution physical values.

The original tool had no CG tuple and could emit OK for nonconvergence. The supplied grep excerpts contain no `not converged` warning; this is supporting, conditional evidence, **not equivalent to an archived finite residual plus info=0 plus unconverged=false**. In the current solver the warning predicate also fails to flag NaN residual when info=0. A process-local NaN-CG injection confirms no warning and unconverged=false; it does **not** establish NaNs occurred in those historical runs (and NaN current comparison can fail separately). Current `run_grid:121`–`:126` now explicitly rejects nonfinite/high residual and records the tuple, with T5/T6 rerun passing. Do not retrofit that new guarantee onto old JSONs. Retain original complete logs/grid hashes and a tuple-bearing validated replay when authorized; absent that, describe the three old runs as reported/no-warning rather than independently certified converged.

## Reproduction and results

From workspace root in PowerShell:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'rint_g1_lhs_network_review_20261005/evidence_g1/run_baselines.py'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'rint_g1_lhs_network_review_20261005/evidence_g1/probe_adversarial.py'
```

Scripts explicitly put the pinned source scripts and the workspace NumPy/SciPy dependency directory on the import path. Final rerun results: step3 RINT **90 OK / PASS**, receipts **49 PASS / 0 FAIL**, rint03 **9 PASS / 0 FAIL**. No production file is patched by either harness. Logs and generated payloads are in this directory, especially `baselines.json`, `adversarial_results.json`, `wetted_unconverged_solver_records.json`, `wetted_unconverged.json`, and `wetted_unconverged_check_arm.log`. The initial missing dependency run was rerun after the pinned dependency became available; final logs are the successful rerun.

Limits: no browser render test, large-grid rerun, production batch, physical r_int calibration, or review of open RINT-06–10/15/16. Other G2–G6 gates belong to the parent/other reviewers.

# Reader / observer re-verification

Pinned source: `a30fe150e21f66aea2f1c360593e1cd781689b14` (2026-10-14). Target source and original review/probes were not edited. No DEM, MPI, SSH, scheduler, native simulation, or production record was run or altered.

Reproduction, from workspace:

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B dem_unloading_kit_reverify_20261014/probes/reader_recheck.py
```

The script uses standard-library synthetic data and calls the actual production `arm_verdict`, `selection_state`, `gate`, `report`, `_s3_at`, `kebase`, `separation`, and observer functions. Production `_mk_arm` / `_mk_utc` serialize files; they are not expected-result oracles. Expected values and mutations are specified independently. Full verdicts, exact returned `repr`, source function locations/signatures, source hashes, and retained fixture paths are in `evidence/reader_recheck.json`. `rc=0` means this probe recorded its findings; it does not mean every expected property passed.

Result: **56 cases; 52 expected properties pass; four observations below.** All of the old named reader/observer counterexamples have their intended corrected outcome, and positive controls pass. Observations 1–3 form two residual findings (P1 unauthorized supersession; P2 strict-parser handling). Observation 4 is a hardening candidate only, not a release blocker or failed closure of the named ULKR-07 fix.

## Closure scope

| ID | This reviewer's disposition | Evidence / limit |
|---|---|---|
| ULKR-01 | **Verified for the stated fix** | UNSTEADY, NaN, S3 failure, wrong kind/phase, missing confirmation reject primary and UVa. Valid no-wall-contact confirmations remain OK and permit the expected next arm. Record integrity still depends on ULKR-04 below. |
| ULKR-02 | **Verified** | First A and first B crossings, rebound and multiple crossings include the first bracket. Old false SEPARATED becomes OVERLAP. Nonfinite later pressure keeps the completed primary but suppresses the outer union. |
| ULKR-03 | **Verified for the stated fix** | Valid actual UT-parent/UTc layout yields t3 primary `0.3827035983143033`, continuation OK, DONE auxiliary. Changed parent screen or used atom bytes, manifest-digest mismatch, copied-history overlap, skipped first k/window, and missing RESUME reject continuation while final report preserves UT primary and marks auxiliary SEP_INCOMPLETE. |
| ULKR-04 | **Partial** | Old NaN-row salvage, wrong wall time, wrong atom/contact time, duplicate atom IDs, malformed CSV width and missing k reject. However duplicate rows can be silently superseded without any RESUME; fractional IDs are truncated; missing `id` column raises instead of returning missing-observation status. |
| ULKR-07 (reader half) | **Verified for the stated fix** | Same-k re-separation, last-budget declaration, four post windows outside budget, movement reset, declaration/event comparison, wall missing/recontact all behave as registered. A malformed-record hardening candidate is separately disclosed below, not promoted to a normal-generator-path defect. Generator half belongs to the other review. |
| ULKR-09 | **Verified for the stated fresh-output path** | Valid S0 unmoved three windows gives `S2=2.24e-6`; one/two/duplicate/gapped/moved/nonfinite/wrong-S0/technical-failure windows produce no baseline file. Probe does not claim revocation of a pre-existing stale baseline. |
| ULKR-10 B | **Verified** | Actual `_s3_at` with arm g: ordinary/UTc free-fall fixture R≈1e-6 PASS, all G_* R=1 FAIL. A separately nonpassing G restore cannot mask this tested S3 result. |
| ULKR-12 (reader/observer half) | **Verified** | Full fixed S0 volume, complete endpoint frames, interpolated ε_all-only M, S0→M W and final t1 report all pass. Missing ID/radius change makes that endpoint ε NOT_COMPUTED without shrinking C_all or erasing valid primary. Pre-crossing abnormal step suppresses W only. Bundle scope belongs to the runner review. |

## Residual 1 / P1 — duplicate invalid confirmation is erased without a resume

Source: `docs/data/ps45_unload_20261009/ul_reader.py:85` (`_supersede`), `:126` (unconditional use), `:562` (k continuity checked only after supersession). REG §14-10 `dem_unloading_ps45_prereg_20261009.md:918`–919 says broken observation records / discontinuous k must not produce a primary value.

Starting with the independently valid UB+UT fixture, insert one additional UT k=3 confirmation row at the same step immediately before the normal k=3 row, but `steady=0`. There is **no RESUME event**. The current reader discards the abnormal row before validating k uniqueness:

```text
arm_verdict(..., 'UT', ...):
  primary_status='OK'
  rho_pct=0.2026077873428664
  n_superseded_rows=1
  why=[]
read_run(...): resume_steps=[]
selection_state(...): stage='need_UV', delta_dt=0.0, next=['UVa']
gate(..., 'UVa', ...): (True, 'δ_dt 0.0 → dt* dt0 → UVa')
```

Evidence key: `duplicate_without_resume`. This is a file→reader→selection→gate result, not a fabricated verdict object. It is a parser-integrity residual in ULKR-04; it does not invalidate the independently verified ULKR-01 predicates for correctly parsed unique rows.

Minimum correction: permit rollback/supersession only at an explicitly validated resume boundary; otherwise reject duplicate/nonmonotone step or k records. Preserve a positive authorized-resume regression, and add this no-RESUME duplicate counterexample through selection/gate.

## Residual 2 / shared P2 strict-parser finding — nonintegral atom IDs are silently remapped

Source: `ul_reader.py:427` converts observed atom IDs with `int(...)`; the S3/observer downstream also uses integer IDs. `ul_lib.read_dump` treats numeric `2.5` as finite data. Replacing endpoint atom ID 2 by **2.5** leaves primary `OK`, rho `0.2026077873428664`, `why=[]`.

Evidence key: `parsing_fractional_atom_id`. The runner/restoration reviewer independently found the same class for UN IDs. Consolidate this as one all-path ID-integrity defect, not two scientific findings.

Minimum correction: validate finite positive integral IDs before conversion and set comparisons, including S0, current atoms, restoration observations and pair references. Reject fractional values instead of truncating them. This is input validation, not a change to S3 thresholds or legal spatial exclusion.

## Residual 3 / same P2 strict-parser finding — missing required column raises a program exception

Source: `ul_reader.py:423`–432. `_atom_frame` obtains parser problems, then dereferences `r['id']` before returning them. Replacing only the endpoint header `id` with `not_id` produces:

```text
arm_verdict(...): KeyError('id')
```

Evidence key: `parsing_missing_column`. This is **not a demonstrated false PASS**. The runner now has a route to record technical reader failure; however ordinary malformed-observation input does not obtain the promised `UNIDENTIFIED`/`NOT_COMPUTED` result. `_s0_dump` has the same ordering pattern at `:346`.

Minimum correction: return parser failure before accessing required columns; test missing `id` on both S0 and a required endpoint. Do not conceal unexpected program exceptions generally.

## Hardening candidate only — row adjacency can substitute for consecutive physical windows

Source: `ul_reader.py:262`–300 counts adjacent entries in the supplied list, not consecutive `w`/step records; `:721`–744 compares event times to those same counted entries. REG §14-7 `dem_unloading_ps45_prereg_20261009.md:894` requires two consecutive SEPARATE windows and four post-declaration windows.

Synthetic post-measurement records at the same k retain only `w=[1,2,4,5,6]` (w=3 removed), with SEPARATED at w2 and POST_DONE at w6. The reader calls w2,w4,w5,w6 four post windows:

```text
primary_status='OK'
trajectory_status='DONE'
separation={'declared_step':3345000, 'separated_final':True,
 'recontact_index':[], 'missing_index':[], 'moved_index':[],
 'n_post':4, 'declared_w':2}
why=[]
```

Evidence key: `separation_missing_csv_window`. This establishes a malformed-record acceptance gap. It is **not evidence that the fixed generator emits this record/event combination**: event timing is chosen to agree with the incomplete table. The original missing wall-dump and recontact counterexamples now correctly produce SEP_INCOMPLETE. No single-row-removal-only failure from an otherwise valid generated completed trace was demonstrated. Do not elevate this candidate to a finding or use it to keep ULKR-07 open.

Minimum correction: before counting separation/post windows, validate unique consecutive w and the arm's expected T_W step spacing within the hold, with missing intervals breaking separation. This also prevents S4 from silently treating a multi-window interval as one window. Valid last-budget declaration plus three further post windows must remain allowed.

## Answers to request Q1–Q3

**Q1:** REG §14-1 is a coherent clarification of C14/C15: endpoint contact is needed for the first crossing, while finite normal S3-valid B confirmations need not keep wall contact. Actual production-function positive and negative tests support that behavior. The parser's no-RESUME duplicate issue is a separate condition for overall closure.

**Q2:** Same-step SEPARATE windows, movement reset and matching SEPARATED/POST_DONE events are appropriate, and are not new physical thresholds. These checks close the original reader DONE contradictions. w/time completeness is useful additional hardening; the current completed-generator-path closure is not held on the malformed-record candidate alone.

**Q3:** S0→M W and S0/first-bracket/M ε agree with §12-9 as explicitly clarified by §14-8. `C_all` is invariant from S0, ε_inside remains distinct, M has ε_all only, incomplete endpoint frame gives a local missing value, and final t3 correctly keeps ε/W from UT because the interval precedes UTc. `W_proxy` is not actual wall work. Existing primary values need not be discarded when an auxiliary value is uncomputed.

Independent numerical check (`aux_full_report`): 105 equal-radius synthetic spheres, radius `0.0005` deck m and area `0.0025` deck m² give `C_all = 105 × (4π/3) × 0.0005³ / 0.0025 = 2.1991148575128552e-5` deck m. At `h0=0.111052`, ε_all=`0.9998019743131584`; at interpolated `hM=0.111277`, ε_all=`0.9998023747173708`, with ε_inside=null. Pressure-height points `(0.111052,0.16)`, `(0.111252,0.0012)`, `(0.111277,0.001)` in deck units give `W_proxy=4.036875e-8` report J by the registered trapezoidal integral; final t1 report carries that value.

Independent valid t3 report (`continuation_positive`): `primary_source='UT'`, `aux_source='UTc'`, `primary_status='OK'`, `rho_pct=0.3827035983143033`, `trajectory_status='DONE'`; ε/W are retained from the preceding UT interval, with `W_proxy_J=4.28687500000011e-8` for that distinct synthetic pressure ladder.

## Limits

No real unloading data exist in this review; values are synthetic. Hash-continuity probes validate used parents and final reporting, not binary restoration physics. The large raw dump/restart archive remains necessary for independent real-data rereading; a lightweight report archive is not a substitute. This review does not authorize production R/U or alter ledgers. Parent review integrates grammar, restoration, runner, and preregistration evidence before an overall decision.

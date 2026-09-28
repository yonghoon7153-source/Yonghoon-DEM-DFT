# Bounded launch / opaque-smoke review

Pin: `18787ab98a13361c37b2343bd07ae276142d0953`. Scope: HBR5-01, HBR5-02, Q1 reader-rule equivalence, Q5 outcome-blind smoke. Actual pinned `start_check.py` CLI/functions and extracted Python `rest` gate were executed against synthetic fixtures. Actual pinned reader `analyse()` supplied the genuine certificate and independent after-mutation diagnostics. No launcher, LIGGGHTS, MPI, sbatch, scancel, or simulation was run by this probe. Production sources were not modified.

Evidence: `probe_launch.py`, `probe_launch_output.json`. Fixture builders are loaded from the previously preserved `../mixer_highbo_round5_evidence_20260928/review_round5_probe.py`; its main is not run and all imported production modules come from this round-6 mirror. Runtime: bundled Python; NumPy/SciPy from the existing local pydeps. Temporary synthetic inputs are disposed after execution; output contains full gate stdout/stderr and return codes.

## Closure assessment

**HBR5-01: closed for the reported empty/non-object seal defect.** `start_check.py:65–90` rejects empty/non-dict records and missing/malformed mandatory fields. `check()` calls this at line 108 before normalizing non-dicts for safe comparisons; binary/deck/runner/checker/rank comparisons are unconditional at lines 114–137. `main()` writes only the refused record and returns 3 at lines 166–176. The valid control returns 0.

| Reproduction key | Actual | Expected | Evidence |
|---|---:|---:|---|
| `start_valid` | 0 | 0 | `job_start.json` exists |
| `start_empty_dict` | 3 | 3 | no success record; refused record exists |
| `start_null` | 3 | 3 | same |
| `start_list` | 3 | 3 | same |
| `start_string` | 3 | 3 | same |
| `shape_np_bool`, `shape_np_float`, `shape_np_zero`, `shape_no_binary_sha`, `shape_no_deck_sha`, `shape_bad_runner_sha`, `shape_relative_binary`, `shape_wrong_backend` | `ok=false` | `ok=false` | actual `check()` reasons preserved |

The independent probe does not itself run the shell runner or count mocked mpirun calls. Its statement is the actual checker return value and success/refusal artifact behavior. The repository's HS tests provide the runner integration layer.

**HBR5-02: closed for the reported post-certificate input-universe mutations, at this pin with an unedited genuine certificate.** `launch_highbo.sh:404–413` uses the same glob, basename regex, and integer-step construction as `measure_bed_aspect.py:34–44`. Gate lines 420–444 use the same bin formula and dump lattice as `measure_mixing_index.py:290–305,352–359`; duplicate, off-grid, missing, and changed bin-0 file sets fail. Gate lines 445–452 ensure the one reference frame remains unique. Existing hash verification still applies to all originally listed frames.

| Reproduction key | Actual gate rc | Expected | Reader after mutation |
|---|---:|---:|---|
| `smoke_normal` | 0 | 0 | original genuine certificate |
| `smoke_after_duplicate` | 1 | 1 | 24/25 bin-0 frames, complete=false, duplicate TECH |
| `smoke_after_offgrid` | 1 | 1 | 25/25 complete but off-grid TECH, hence smoke failure |
| `smoke_after_e0_duplicate` | 1 | 1 | reader refuses ambiguous reference t0 |
| `smoke_after_bin1_duplicate` | 0 | 0 | bin-0 complete=true, tech_smoke=[] |
| `smoke_with_later_bin_additions` | 0 | 0 | bin-0 certificate plus continuing later output is allowed |
| `fractional_smoke_normal` | 0 | 0 | 1000.2500000000001 steps/rev gives 26 bin-0 frames |
| `fractional_duplicate_1200` | 1 | 1 | last bin-0 frame duplicated; reader complete=false, 25/26 |
| `fractional_duplicate_1240` | 0 | 0 | first bin-1 frame duplicated; reader bin-0 complete=true |

No accidental current-file mutation bypass or false rejection was found in these cases. The later-bin duplicate control deliberately tests the stated bin-0 scope: later-bin problems remain final-window issues, not reasons to reject an otherwise unchanged smoke window.

## What regex equality does and does not establish

HL④o (`test_launcher.sh:365–374`) tests only `STEP_RE.pattern`. It does not test glob scope, directory/file filtering, step conversion, duplicate handling, t0 derivation, the bin formula/epsilon, or required-frame validation. Therefore it is not a sufficient stand-alone guarantee that the two implementations will remain equivalent. At this pin the relevant code is independently identical and semantic mutation controls pass, so this is not grounds to reopen HBR5-02 by itself.

NumPy installation or a second full M calculation at `rest` is not intrinsically necessary. A shared standard-library enumeration/bin-window helper plus behavioral tests would avoid drift. If duplication remains, use differential fixtures for duplicate/off-grid/missing/changed frames, E0 duplicate, a non-integer steps-per-revolution boundary, and later-bin additions. Pin/hash the reader's imported dependencies as part of the analysis policy; hashing only `measure_mixing_index.py` at gate line 361 does not bind `measure_bed_aspect.py` or other imported logic.

There is a separate certificate-trust boundary: gate lines 420–430 derive the validation window from the supplied certificate, rather than independently deriving it from the sealed deck. In `tampered_certificate_narrows_bin0`, changing only certificate `plan.steps_per_rev` from 1000 to 1.0 makes a newly introduced duplicate at step 400 fall outside the gate's alleged bin 0; the gate returns 0. This requires editing the certificate itself and is not claimed as the original ordinary-file-mutation defect. It demonstrates that provenance hashes are binding claims, not authentication of the certificate's derived fields. A frozen projection wrapper must copy these fields without recomputation or manual edits. Independently deriving/checking t0/plan from the sealed deck, or retaining a sealed full-certificate digest and projection identity, would harden that boundary.

## Q5: outcome-blind smoke is feasible, with a concrete projection contract

`opaque_allowlisted_certificate` uses the real reader result projected to exactly these fields and is accepted by the actual gate, rc 0:

```text
run, provenance, plan, t0_step
smoke.complete
smoke.tech_smoke
smoke.qc_repr.pass
```

The production result includes M values in `rows`, `by_rev`, `M_final`, `M_t0`, `planned`, and `smoke.M_mean`; it also includes S0/SR and variance-derived proxies (`measure_mixing_index.py:391–414`). The CLI's `report()` prints M and S0/SR before/alongside smoke at lines 419–445. Thus merely hiding or deleting the final JSON after a normal visible CLI run does not maintain outcome blindness. The wrapper must suppress stdout and stderr/exception text that may contain values, use an explicit output allowlist, and map errors to technical codes. It should be preregistered and tested on synthetic pass/fail/leak controls before processing new data. This probe inspected synthetic M only; it did not access any LH result.

The launcher certificate alone is not the complete §8 smoke. The registered manual requirements remain conservation/100,000 counts/id-type-radius preservation, the approved D-1 contact contract over t0→bin0, the 8×8×2 S0²/SR² floor test, and step/s (`mixer_highbo_prereg_20260927.md:250–260`). An outcome-blind wrapper can emit their predeclared booleans/reason codes rather than M or physical-effect estimates, with separate hashes/provenance for the 8×8×2 and 16×16×4 invocations. These booleans still reveal technical QC status, which is the intended disclosed information. Save execution/input/tool/projection identities and the gate decision for audit. A full result may be machine-hashed in memory or preserved under controlled access without exposing it to the decision maker; deleting every trace is unnecessary and weakens auditability.

This approach does not close D-1, the matching-rank phase validation, or the comparison-identification decision. The new Q8 registration should fix the policy before generating the new outcome-blind smoke, then restore first→smoke→rest. Historical `all` was an explicit authorized deviation, not a concealed defect. Because a nonempty generic `DEVIATION` still enables that command, a new frozen launch-policy ID/hash should specify allowed stages, and a strict first/rest policy should reject `all` even if the old environment variable is accidentally retained. That is a forward enforcement recommendation, not a retroactive claim that the authorized historical submission was unauthorized.

# Reader adversarial review (Q1, Q4, Q7)

Target: supplied source snapshot pinned to `2783061ead9f192ab742a2f0b14b0182a98a4966`. Read-only source review. No DEM, WSL, SLURM, production data mutation, or source modification.

Reproduction (PowerShell, from review root):

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B probes/reader_adversarial.py
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B probes/reader_continuation.py
```

Both commands return 0 when the independently specified counterexamples reproduce. They invoke production file readers, `arm_verdict`, `selection_state`, `gate`, `pair_table`, and `report`. `_mk_arm` is used as a fixture serializer, not as an expected-result oracle. Fixtures and full verdicts are retained under the `fixture_root` recorded in each JSON.

## P1: Invalid confirmation rows still authorize the next UV arm

Code: `ul_reader.py:378-395` counts `len(steps)-1-j` and validates only the two first-crossing endpoints (`362`). No check establishes that the following two registered confirmation steps were normal or even have finite pressure. `make_unload_decks.py:370-371,401` also increments confirmation after an exhausted hold marked UNSTEADY, so this is reachable with generated records.

Rule: preregistration `:725-729` makes the first crossing plus two registered confirmation steps the primary measurement and preserves it after they have completed normally; C14 `:808` disallows issuing a point estimate when confirmation is incomplete. Normality remains required by `:326-338`.

Counterexample: first crossing uses the CX2 four-point ladder (.20,1.2),(.25,.8),(.30,.6),(.35,.4), where height is µm and pressure MPa. In UT both confirmation rows k=3,4 exhaust 12 windows with `steady=0`; the fixture also makes their S3 residuals bad. The actual reader returns `primary_status=OK`, `rho_pct=0.2026077873428664`, `rank_eligible=true`, and no reason. With a valid UB, `selection_state` returns `need_UV`, delta_dt=0, next=UVa; `gate` returns ALLOW. Replacing only those two confirmation Pbar values by `nan` also returns OK.

Evidence: `evidence/reader_adversarial.json` keys `confirmation_invalid`, `confirmation_nan`. This is an endpoint-to-selection-to-submission fail-open, not a fabricated verdict object.

Minimum correction: validate the actual two confirmation records (registered phases/order and normal finite observations) before setting primary OK; invalidate the primary measurement and selection if either required confirmation cannot support the claim. Keep the valid post-measurement-timeout behavior.

## P1: Omitting the k=0→1 crossing can turn overlap into false separation

Code: first-crossing detection accepts the k=0→1 pair at `ul_reader.py:339-346`, but union construction calls `crossings(steps[1:], Pm)` at `397-403`. The first valid actual bracket is silently excluded. `pair_table:634-639` then uses the narrowed interval to issue SEPARATED.

Rule: preregistration `:768` and C15 `:809` require the actual first-crossing bracket and all crossing brackets; there is no exclusion of a first crossing at k=1.

Counterexample: k=0 has P=160; subsequent heights [.20,.25,.30,.35,.40] and pressures [.8,.6,.4,1.2,.7], all normal, finite, and contacted. The first movement is A=.20 and later movements are B=.05. Reader correctly computes first rho=0.1798695599526285 and first bracket [0,.20] µm, but reports union=[.30,.40] µm. An independently read 0:10 bed with bracket [.20,.25] µm then yields `SEPARATED`. Including the omitted first bracket gives union [0,.40] and `OVERLAP` for the same actual verdicts. Without a later rebound, the union is null and every pair involving the otherwise valid result becomes UNIDENTIFIED.

Evidence: `evidence/reader_adversarial.json` keys `first_step_cross`, `first_step_rebound`, including both actual pair output and output with the complete union. The latter holds all other verdict fields unchanged.

Minimum correction: include the k=0 pair in the set of actual crossings and ensure the union always includes the selected first bracket.

## P1: Normal UTc continuation loses the already valid UT primary measurement

Code: `run_unload.sh:194-202` copies only `ul_windows.csv`, `ul_steps.csv`, `ul_events.csv` from UT, then emits new continuation dumps and thermo into UTc. Reader `ul_reader.py:306,327,367-371` looks for every copied historical endpoint's wall, atom/contact, and sigma evidence under UTc; it does not resolve `continues=UT`. `report:872-875` chooses UTc rather than preserving UT's primary result.

Rule: preregistration `:771-772` defines t3 as the same UT trajectory continued from its R_M for auxiliary observations. CX2 ULR1-05 explicitly demands final follow-up artifacts, not just permission to submit UTc.

Counterexample: valid UB and UT have rho .2026077873428664 and .3827035983143033 respectively; valid UVb equals UT, so selection resolves t3. Build the runner's layout: historical CSV rows are copied into UTc, original endpoint dumps/thermo remain in UT, new post-R_M dumps/thermo exist in UTc, and continuation ends DONE with four separation windows. The actual UT verdict is OK. The UTc verdict is UNIDENTIFIED/rho null, citing both historical endpoint S3 NOT_COMPUTED and contact OBS_MISSING. `report()` remains t3 but emits the null UTc primary value.

Evidence: `evidence/reader_continuation.json` contains full source UT, UTc, selection, and report outputs. This does not rely on a DEM run; file layout follows the runner's explicit copies and output directory.

Minimum correction: resolve continuation observations through a verified source trajectory, or carry/copy the immutable required historical evidence, and assemble UT primary plus UTc auxiliary observations without discarding the original measurement. Test final `report()` for t3.

## P2 / status consistency: Reader-observed recontact or missing evidence still reports DONE

Code: `ul_reader.py:304` directly maps deck summary DONE into trajectory DONE; `454-455` only adds a why string when reader separation/post windows disagree. No trajectory correction occurs.

Rule: preregistration `:729,740` says incomplete auxiliary observations must not be called complete and recontact not followed by re-separation is trajectory separation incomplete; C6 `:804` says reader observation wins over geometric deck declaration.

Counterexamples: after the valid first crossing and confirmations, windows have wall contacts `[0,0,0,0,1]` or `[0,0,0,0,missing]`, while the deck summary is DONE. Reader clears separation/post-window observations (`separated_final=false`, n_post=0), leaves surface NOT_COMPUTED, but retains trajectory DONE. The reason string admits disagreement. The primary measurement is correctly preserved.

Evidence: `evidence/reader_adversarial.json` keys `done_recontact`, `done_missing`.

This does not fabricate a surface value: the narrower issue is the contradictory machine-readable trajectory completion label. If DONE is intended to mean execution ended only, the report must expose the required auxiliary-incomplete status distinctly and define that meaning; currently the documented two-axis status does not do so.

## Tested improvements / rejected candidate

- The exact CX2 valid four-point measurement followed by TIMEOUT is preserved as rho=.2026077873428664, primary OK, trajectory TIMEOUT, no spurious lower bound (`control`). Thus the original ULR1-02 numeric counterexample is fixed.
- Contact/zero/missing parsing and separation reset themselves work in the recontact/missing examples. The remaining DONE issue is downstream of those correct observations.
- A partially completed UV folder makes ordinary `gate(UVa)` refuse; this is **not a retry finding**, because `run_unload.sh:85` intentionally bypasses the normal gate for `RESUME=1`. The observation remains in evidence as a rejected candidate.
- C6's pressure rule uses the window's Ps_avg, not a last instantaneous wall-force net. C15 checks the first crossing's two endpoints for normality, S3, finite values and last-window contact; the newly demonstrated failure is confirmation validation and the bracket's subsequent use.
- Q7's ordinary branch restrictions structurally implement UB/UT before one chosen UV, t3→UTc rather than new 7:3 UT3, and final-tuple restriction for other beds. Their scientific precondition is undermined by invalid confirmations becoming OK; final t3 reporting is also broken.

## Closure recommendations in this reviewer scope

| Prior ID | Recommendation | Reason |
|---|---|---|
| ULR1-01 | Keep open / partial | Named invalid first endpoints are handled, but invalid required confirmations propagate to primary OK and next UV ALLOW. |
| ULR1-02 | Original counterexample verified fixed; broader closure qualified | Valid post-measurement TIMEOUT retains rho, but required confirmation completion is not actually validated. |
| ULR1-03 | Partial; machine status concern remains | Cancellation/contact/reset rules improved; recontact or missing evidence still leaves trajectory DONE. |
| ULR1-04 | Defer to generator/observer reviewer | No new counterexample from this reviewer. |
| ULR1-05 | Keep open | First-bracket union omission can claim false pair separation; t3 UTc final report loses its established main value. |

Scope limitations: these are semantic file-to-output probes of the exact source functions. They do not certify LIGGGHTS grammar, successful runtime execution, binary restoration, or physical validity of production beds.

# Q1 / Q5 independent resume and separation review

Pinned source: `eaecfba2a2dfbff6f13222f6afeb01d8ebeb5a84`. Source was read only. No LIGGGHTS, MPI, WSL, SSH, scheduler, production run, or Git mutation was performed by this probe.

Reproduction (review folder as working directory):

```text
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B probes/resume_recheck.py
```

Script: `probes/resume_recheck.py`. Main evidence: `evidence/resume_recheck.json`. The JSON contains the retained case directory, source hashes, full arm verdicts, selections and UVa gates. Every run uses a new `evidence/resume_cases_<UTC>/` folder. All frames and records are synthetic; no actual unloading observations are claimed. The submitted serializer is used for atoms/contacts/thermo; independent code constructs resume boundaries and adversarial mutations. A/B move duration and complete state-variable fields are retained. Old first-attempt dump files are preserved when the new attempt has not replaced them.

Final probe result: 37 cases, 32 expected outcomes, 5 failed expectations. Those five are **not five independent findings**: repeated-boundary reuse and its duplicate-event companion are one issue; fractional ordinal coercions are one hardening observation; longer completed hold is a separate false refusal.

## Narrow disposition

- Original ULKRR-02 no-RESUME duplicate counterexample: closed in the new code. Duplicate step and window records reject the primary and UVa.
- Auth checks for missing manifest marker/event/state, wrong event k/state k/state step, missing retained checkpoint, wrong first new k, and stale k at the boundary: reject as expected.
- Normal fresh, clean resume with no stale rows, partial-window resume, and completed-step resume: preserve `primary=OK`, rho `0.2026077873428664`, selection `need_UV`, UVa allowed.
- Q1 general closure: **still open**, with the two narrowed cases below. Neither is a blanket rejection of the implemented auth checks.
- UTc parent continuation: accepted without local `resume_from`/`state_unload`; missing/mismatched parent RESUME is rejected. Normal continuation remains `primary=OK`, `trajectory=DONE`, `continuation=OK`.
- Q5 W/deck fallback/gap behavior: **closed for the requested cases**. Actual generated deck W is used, all registered arm fallbacks agree (UTc→UT3; G_*→parent), missing window and wrong step interval break the earlier declaration, and a new valid declaration after the gap is allowed. Declaration w12 with completion w15 remains DONE. Primary value survives these auxiliary failures.
- Parent reviewer is auditing submitted Linux M23 and running the broader runner suite. This probe directly executes Python read_run→arm_verdict→selection_state→gate; it does not claim a new Bash or actual DEM execution.

## Finding A — one authorization can be multiplied by duplicate RESUME events

This is a remaining case of the existing ULKRR-02 malformed-record integrity contract, not a separate numerical/physics finding and not evidence that the unmodified runner naturally emits multiple RESUMEs.

Relevant source (`source/docs/data/ps45_unload_20261009/`):

- `ul_reader.py:126`: `_resume_auth` appends every matching event, allowing repeated `(k, step)` tuples for a single manifest `resume_from`.
- `ul_reader.py:140–150`: `_supersede` consumes the list **index** (`i in used`, `used.add(i)`), not the unique boundary. Two equal tuples are two grants.
- `ul_reader.py:193–195`: event rollback similarly reuses membership in `auth` without a unique consumption check.
- `run_unload.sh:88`: runner contract refuses a second resume when `screen_a2.txt` exists; normal registered scope is one resume.

Case `one_auth_two_rollbacks` has exactly one `resume_from=3310000`, one state file `(ul_k=1, ul_rstep=3310000)`, and two identical `RESUME,1,3310000,...` records, with two stale k2 segments. Each stale segment consists of four window rows followed by its step row (normal write ordering). The final k2+ records are the valid successful records.

Actual result:

```text
resume_auth = [[1,3310000],[1,3310000]]
n_superseded_rows = 10
problems = []
primary_status = OK
rho_pct = 0.2026077873428664
selection = need_UV / next [UVa]
gate(UVa) = ALLOW
```

Control `one_event_two_rollbacks` uses the same repeated CSV segments with only one RESUME event and rejects them. Thus the permissive result is specifically caused by converting a duplicate event into additional authority. `duplicate_event_only` also accepts duplicate RESUMEs with one actual rewind, without recording an integrity problem.

Minimal remedy: tie authorization and consumption to a unique boundary/attempt, reject duplicate/conflicting RESUME evidence rather than multiplying it, and apply consistent event rollback rules. Preserve the existing normal positive controls. Deduplicating tuples can prevent the extra CSV deletion; explicitly reporting duplicated resume evidence is preferable to silently accepting it.

## Finding B — longer valid repeated hold is not recognized as a rollback

Suggested P2: false refusal of an authorized normal record layout. This proves a reader limitation for a valid changed hold duration; **it does not prove an actual LIGGGHTS restart changes the window count**.

Relevant source:

- `ul_reader.py:138`: rollback detection requires `prev['step'] >= s` before it considers any authorization. Repetition of a step ordinal k at a later physical step is not considered.
- `ul_reader.py:692–695`: the remaining duplicate k makes the primary unidentified.
- `decks/ps_7_3_r45/in.UT.liggghts:267`: appends the completed step CSV row.
- Same deck `:290`: appends the CROSS event.
- Same deck `:319–330`: only later writes the restart binary and state file. A machine failure after the CSV/event but before line 319 leaves a fully written old k2 and only the previous k1 checkpoint.
- Same deck `:237–239`: hold duration depends on reaching two successful windows, so the protocol itself permits different completed hold lengths.
- `run_unload.sh:266–271`: chooses the last binary and its state, records the old checkpoint step, and resumes. This valid pre-checkpoint interruption is within that path.

The probe independently stores successful fresh 4- and 5-window k2 controls. Both are `primary=OK` and UVa allowed. **Actual pinned generated deck control flow** (`make_unload_decks.deck_sim`, no particle calculations) produces the CSV rows for these cases. For the 5-window hold, concrete pressure inputs are `[0.0010, 0.0009, 0.0008, 0.0008, 0.0008]` in deck units. The generated S1 sequence is `[0,0,0,1,1]`, S2 is always 1, and the deck ends the hold at w5 and later reaches RM_STOP. The 4-window control similarly ends at w4. This establishes that the extra window is consistent with the real producer's predicates rather than a serializer-only request for an impossible hold duration. The probe then places an interrupted old completed 4-window k2 before the authorized resumed trajectory. The boundary is `(k1, 3310000)`. The old k2 ends at 3360000; the resumed 5-window k2 ends at 3370000.

Actual:

```text
fresh_completed_hold_5_windows: OK -> UVa ALLOW
resume_completed_hold_4_windows: OK -> UVa ALLOW
resume_completed_hold_5_windows:
  resume_auth=[[1,3310000]], n_superseded_rows=4, read_run.problems=[]
  retained step k=[0,1,2,2,3,4]
  primary=UNIDENTIFIED, selection=SELECTION_UNRESOLVED, UVa denied
```

The four stale window rows are recognized and removed, since the new first window rewinds time. The stale step row is retained because its completed time is earlier than the new completed time. Old dump frames are retained in the test, so there is no missing-frame serializer artifact. The final `why` consists only of duplicate-k/confirmation-sequence consequences; no missing S3 file is present. The exact same fresh 5-window output passes before adding the first attempt.

Minimal remedy: recognize the new attempt at the authorized boundary using an explicit per-attempt segment/offset, or safely consume repeated k on step records with the same validated checkpoint structure even when the new end step is later. Do not globally erase duplicate k. Test valid old completed hold lengths shorter/equal/longer than the new hold and retain unauthorized duplicate negatives. Actual restart-induced changes in physical convergence remain unmeasured; the proven result is rejection of a producer-consistent authorized record layout.

## Additional nonblocking type-hardening observation

`fractional_resume_event_k` changes RESUME k from `1` to `1.4`; `_i` (`ul_reader.py:77–79`) rounds it to 1 and authorizes rollback. `fractional_confirmation_k` changes step k3 to 3.4; record conversion (`:209–211`) rounds it to 3 and still produces primary OK/UVa ALLOW. This is not the fixed ULKRR-04 **particle ID** path and is not counted as another blocking finding here. If the stated ordinal contract is intended to require exact integer k/w/step, exact parsing should be extended separately.

## Q5 detail

Cases `sep_positive`, `sep_no_deck`, `sep_gap_new_declaration`, `sep_declare_w12` return DONE with the primary preserved. `sep_missing_w3`, `sep_shifted_w3`, `sep_wrong_deck_W` return SEP_INCOMPLETE with the primary preserved. `registered_W_fallbacks` covers UB, UT, UVa, UVb, UT3, UTc, G_UB, G_UVa, G_UVb, G_UT3. The new-declaration case includes an earlier declaration, an omitted recontact window, a correctly timed RECONTACT event, and new phase-2 zero windows before the later declaration; it does not merely relabel phase-3 post windows as a new declaration.

The fallback remains a permissive policy when the deck file exists but contains no usable numeric W, not solely when the file is absent (`ul_reader.py:364–370`). No new false DONE was established from that policy here, because registered deck W and fallback W agree; this is a documented limit, not an invented failure.

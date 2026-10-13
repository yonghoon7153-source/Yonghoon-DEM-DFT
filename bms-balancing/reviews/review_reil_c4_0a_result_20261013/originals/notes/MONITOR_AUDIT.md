# C4-0a monitor audit (static only)

Frozen review ref: `c542e056b33d25100bc0519ce492c98d3bcce172` (provided by parent reviewer).
Sources are the captured files under `source/bms-balancing/`. This audit read source and requirements as text only. No supplied module was imported, no test was executed, and no scientific data, spreadsheet, pickle, notebook, or installation was opened/run.

## Findings

### M1 — P2: final recording can report COMPLETE after its time limit

- Location: `scripts/reil_c4_monitor.py:334-339` (the only time gate is at lines 317-320).
- `final_record(..., limit_s=...)` checks the time before each file. The last file's serialization, write, readback, SHA calculation, and the final `output_bytes(roots)` have no subsequent time check. The function returns `record_state="COMPLETE"` as long as the byte total fits, even if `final_snapshot_s > limit_s`.
- Concrete static trace: one small output part, `t0=0`, `limit_s=1`, injected clock returns `0` at line 317 and `2` at line 339. Successful write/read and a byte total below the limit produce `{record_state: COMPLETE, final_snapshot_s: 2}`. An ordinary slow last write/read or filesystem traversal causes the same result. This is not the excluded permanently blocked OS-query case.
- Requirement relevance: v2 approval request lines 127-130 require the stage budget to include final recording and incomplete preservation on time/size overrun. The stage-specific reserve values remain future C4-E/A/B decisions; this finding is about an explicit existing `limit_s` argument being ignored at the final boundary, not a claim that a production stage has already run over budget.
- Minimal correction: take one post-write/post-size-scan timestamp, compare it with the same absolute recording deadline, and set `RECORD_INCOMPLETE` (preserving hashes/files and the byte count) if exceeded. Return that same timestamp. Check before starting each subsequent write as today.
- Coverage: `tests/test_reil_c4_0a.py:146-162` covers byte overflow and successful hashing only; there is no late-final-write or late-final-scan case.

### M2 — P2: successful terminal disk sampling can leave an unreported RSS gap

- Location: `scripts/reil_c4_monitor.py:269-280`, especially the normal-completion branch at 276-280.
- RSS freshness is checked only inside the next `rss_w.observe(...)` (line 254). After the disk sampler returns, only the disk watch and the measurement deadline are checked. If all workers have ended, the loop then exits without checking how stale the RSS observation has become.
- Concrete static scenario using the default gap limits: a final `worker_end` event is handled at approximately t=5 s, fresh RSS arrives at t=5.01 s, and a due disk sample takes 6 s. The preceding disk sample arrived around t=0.02 s, so the new disk gap is about 10.99 s, below the 15 s disk limit. The 30 s measurement deadline is also still in the future. At t=11.01 s, the 5 s RSS gap has been exceeded, but line 276 observes all workers ended and returns `global_stop=None`. The parent process is part of the RSS set and the monitor is still running during that disk traversal.
- This is a terminal monitoring blind spot, not a request to promise OS hard limits or to interrupt a permanently blocked call. If work continues into another loop, the existing next RSS observation detects the gap; it is the successful terminal branch that loses it.
- Minimal correction: check current freshness of both watches after either potentially slow sampler and before declaring completion, without advancing either watch's last-valid timestamp on the freshness check. Record the stale gap as a stop reason. A helper separate from `observe()` would avoid inventing a sample.
- Coverage: tests at 68-83 and 109-122 delay RSS; there is no slow-disk terminal case or cross-monitor freshness case. A scripted clock/disk callback plus an end event can test this deterministically without using real research data.

### M3 — P2 diagnostic-loss candidate: Structural.partial is discarded at the worker boundary

- Location: `scripts/reil_c4_monitor.py:160-162`; producer `scripts/reil_c4_e3a.py:275`.
- `Structural` stores both `info` and `partial` (monitor lines 28-30). E3a explicitly raises it with the partially collected row/stats. The worker event serializes only `s.info`; the parent receives no `s.partial`. `_states` later emits only the interrupted task id/start/elapsed/reason and the shared lower-bound evaluation count (lines 178-181).
- Consequently a structural failure after several objective calls loses the partial nonfinite/extrapolation/box/G counters that E3a attached. The main error information is preserved in s.info and shared progress can retain n_eval; warnings are not included in that prepared partial payload, so they are not claimed as lost by this handoff. Requirement v2 says to preserve the first failure/intermediate state/records. This does not authorize turning a structural failure into a completed result row.
- Minimal correction: preserve `_jsonable(s.partial)` in the structural diagnostic event/record, while continuing to stop globally and keep the task interrupted. Add a synthetic worker-boundary test asserting the partial diagnostic survives.
- Scope qualification: current E3a CLI has no measurement/supervision command, and tests assert only that `run_e3a_call()` raises `Structural` (340-346). Thus no submitted real E3a measurement was shown to lose records; the loss is in the existing reusable worker helper when connected to the provided task function. Parent reviewer should coordinate with the E3a audit and avoid duplicating this finding.

## Verified implementation strengths

- `Watch.observe` (43-59) computes arrival-time gap before updating `last_valid`; a late successful sample cannot erase the previous gap. It separately labels first delay, missing value, and late success, and immediately stops for sampler exceptions.
- Parent supervision rechecks the absolute deadline after RSS and disk return (257-258, 272-273). Workers independently check it before beginning each loop task (145-149). Do not expand this into an OS scheduling/hard-stop guarantee.
- `output_bytes` resolves roots and removes overlapping ancestor/descendant roots before summing (91-104); tests cover distinct body/wrapper/temp roots and nested overlap (134-143).
- Final writes are included in the subsequent byte total; overflow returns `OUTPUT_LIMIT_EXCEEDED` and preserves files (334-337; test 146-153).
- Exact path or separator-delimited descendant ownership (70-72) fixes prefix-sibling confusion. Quoted/rename lines remain ambiguous and raw porcelain is preserved (75-88; tests 166-185).
- The frozen C5 implementation remains a reference. The C4 module defines replacements and does not silently alter C5 evidence behavior.

## Coverage and integration limits (not additional defect claims)

There are 12 monitor-focused tests at test file lines 39-185. They exercise the required nominal gap categories, a late RSS sample, the worker's independent deadline, completion, overlapping output roots, final byte overflow, and ownership ambiguity. The provided positive coverage does not cover M1/M2/M3.

The current C4 E3a CLI exposes identity, seal-arrays, and plan-only dryrun (`reil_c4_e3a.py:510-520`). It does not call `supervise` or `final_record` for real E3a work. Actual execution must later declare and pass the same complete body/wrapper/temp/final root list, reject bad monitor/record outcomes, fix one timing origin/reserves, and preserve diagnostics. These are execution-integration acceptance checks before C4-E, not proof of unauthorized or incorrect research execution in C4-0a.

No claim was made about symlink/hardlink security, Windows support, strict OS memory limits, permanently blocking samplers, or a specific C4-E budget: those would exceed the supplied requirements/evidence.

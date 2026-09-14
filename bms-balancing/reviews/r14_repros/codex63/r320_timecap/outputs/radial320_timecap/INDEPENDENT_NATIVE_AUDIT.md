# Independent source/native audit

Audit completed: 2026-09-14T19:45:07.629915+09:00

Source PASS: full baseline text after only two class/label replacements and two early-cap expression replacements equals the new source (line endings normalized).
- Baseline: `outputs/comsol63/radial320/Caps300R320H0250.java` / `837f8b03ff3381bb1aea6397935d0079b032f5e4aea007b32d1ebf7c40775b2e` / job `f0db6d080ad04045a2b43dc5a51d89b2`.
- New: `outputs/comsol63/radial320_timecap/Caps300R320H0125.java` / `8d35be8fab513f5e2def316c4d00e0fdc19983a5dd3bf492f4ffe47a58248be3` / job `18a00b03e38d4694b9ba30d88e7008f4`.
- Physical mesh 300 (120/60/120), radial mesh 320 per electrode, 187 requested times through 5 s, one runAll call. All other source content is unchanged.
- Atomic contract identity, source configurations and job records agree. No external read/process/network additions.
- Worker wall-clock budget 1200 s versus reference 1200 s is separate from physical 5 s and the explicitly reviewed COMSOL Time expression change.
- Four OCP/entropy functions retain extrapolation none. The two StopCondition guards are evaluated after time steps; they do not protect rejected Newton trials. Electrolyte positivity remains postprocessing only.
- Old failed job08e0fc5d41e147678f3940e98100ec12 remains failed/INCOMPLETE_RANGE_STOP with unchanged ledger-anchored evidence despite its batch rc0.

Native PASS: raw batch log, console property readback and decoded scalar CSVs were independently checked.
- Completed; compile/batch return codes 0. Actual native element counts [300, 320, 320]; transient DOFs 79485 plus 12 internal.
- 1143 readable Time/Variables properties; only maxstepexpressionbdf differs from the R320 H0250 baseline.
- 987 stored rows and 986 accepted intervals; all 187 requested times stored exactly.
- End time <= 0.1 s, including arrival: 807 intervals, 792 at cap; max h = 0.00012500000000001 s.
- Start time >= 0.1 s: 179 intervals; max h = 0.05 s. No unresolved crossing; all interval caps pass with 1e-12 s rounding tolerance.
- Consecutive stored times define h; native indices, printed times and printed h agree within displayed rounding. This does not establish the solver expression evaluation point.
- OCP guard remains zero and surface bounds pass. Minimum electrolyte concentration = 1194.4372136345676 mol/m³, checked only in postprocessing.
- Cap compliance is not true time-error validation or complete convergence. Reused R320 H0250 and new R320 H0125 adaptive histories are compared without assuming they are identical.
- Precise boundary intervals, input hashes and independent summary/CSV cross-checks are in INDEPENDENT_NATIVE_AUDIT.json.

The audit wrote only this report and its JSON companion; original source/raw result files were read only.

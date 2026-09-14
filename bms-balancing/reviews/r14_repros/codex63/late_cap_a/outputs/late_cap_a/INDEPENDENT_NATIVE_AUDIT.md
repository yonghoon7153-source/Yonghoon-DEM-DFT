# Independent source/native audit

Audit completed: 2026-09-14T20:54:05.320019+09:00

Source PASS: full baseline text after only two class/label replacements and two nested cap-expression replacements equals the new source (line endings normalized).
- Baseline: `outputs/comsol63/radial320_timecap/Caps300R320H0125.java` / `8d35be8fab513f5e2def316c4d00e0fdc19983a5dd3bf492f4ffe47a58248be3` / job `18a00b03e38d4694b9ba30d88e7008f4`.
- New: `outputs/comsol63/late_cap_a/Caps300R320LateCapA5s.java` / `a03abb905454de63b34b55e314ed09f3cb6414d58444e8b605962166a872531f` / job `c40c05d3cfb643a4b706345637b00f57`.
- Physical mesh 300 (120/60/120), radial mesh 320 per electrode, 187 requested times through 5 s, one runAll call. All other source content is unchanged.
- Atomic contract identity, source configurations and job records agree. No external read/process/network additions.
- Requested cores changed from 2 to 16. Actual core use is checked from both native batch logs; parallel arithmetic/roundoff is an additional execution difference.
- Worker wall-clock budget 1800 s versus reference 1200 s is separate from physical 5 s and the explicitly reviewed COMSOL Time expression change.
- Four OCP/entropy functions retain extrapolation none. The two StopCondition guards are evaluated after time steps; they do not protect rejected Newton trials. Electrolyte positivity remains postprocessing only.
- Old failed job08e0fc5d41e147678f3940e98100ec12 remains failed/INCOMPLETE_RANGE_STOP with unchanged ledger-anchored evidence despite its batch rc0.

Native PASS: raw batch log, console property readback and decoded scalar CSVs were independently checked.
- Completed; compile/batch return codes 0. Actual native element counts [300, 320, 320]; transient DOFs 79485 plus 12 internal.
- 1143 readable Time/Variables properties; only maxstepexpressionbdf differs from the R320 H0125 baseline.
- 1155 stored rows and 1154 accepted intervals; all 187 requested times stored exactly.
- Stage interval counts: {'initial_to_0p1': 807, 'middle_0p1_to_1': 185, 'final_1_to_5': 162}. Caps are 0.000125 s through arrival at 0.1 s, 0.005 s from 0.1 s through arrival at 1 s, and 0.025 s after 1 s.
- Arriving and departing intervals at both 0.1 and 1 s are recorded separately in JSON. No unresolved crossing; all caps pass with 1e-12 s rounding tolerance.
- Native core readbacks: baseline [2, 2]; new [16, 16]. Cap changes are not the only execution difference.
- Each electrode profile contains 241 finite points at every stored time, with exact time/domain alignment and invariant physical coordinates.
- Consecutive stored times define h; native indices, printed times and printed h agree within displayed rounding. This does not establish the solver expression evaluation point.
- OCP guard remains zero and surface bounds pass. Minimum electrolyte concentration = 1194.4372089762865 mol/m³, checked only in postprocessing.
- Cap compliance is not true time-error validation or complete convergence. Earlier state changes carry into later segments, and core count changed. Segment comparisons are not isolated causal tests; no identical adaptive histories are assumed.
- Precise boundary intervals, input hashes and independent summary/CSV cross-checks are in INDEPENDENT_NATIVE_AUDIT.json.

The audit wrote only this report and its JSON companion; original source/raw result files were read only.

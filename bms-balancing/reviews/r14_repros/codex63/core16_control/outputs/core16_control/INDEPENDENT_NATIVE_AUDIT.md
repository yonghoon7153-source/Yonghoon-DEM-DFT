# Independent source/native audit

Audit completed: 2026-09-14T21:44:05.704855+09:00

Preserved source PASS reused: the prior independent byte-level review found exactly two class/label identifier changes and all other bytes equal. The original H0125 cap expression is unchanged. That completed source audit was not repeated.
- Baseline: `outputs/comsol63/radial320_timecap/Caps300R320H0125.java` / `8d35be8fab513f5e2def316c4d00e0fdc19983a5dd3bf492f4ffe47a58248be3` / job `18a00b03e38d4694b9ba30d88e7008f4`.
- New: `outputs/comsol63/core16_control/Caps300R320H0125C16.java` / `4db47e27dcf0d8d2977dc786dab2c3ba40e98a6adf42d7201bf1c66ab802537e` / job `5d1a87652ed54e6a945d4f2af4aeda70`.
- Physical mesh 300 (120/60/120), radial mesh 320 per electrode, 187 requested times through 5 s, one runAll call. All other source content is unchanged.
- Atomic contract identity, source configurations and job records agree. No external read/process/network additions.
- Requested cores changed from 2 to 16. Actual core use is checked from both native batch logs; parallel arithmetic/roundoff may affect results despite identical model and solver settings.
- Worker wall-clock budget 1800 s versus reference 1200 s is separate from physical 5 s. The COMSOL Time expression is unchanged.
- Four OCP/entropy functions retain extrapolation none. The two StopCondition guards are evaluated after time steps; they do not protect rejected Newton trials. Electrolyte positivity remains postprocessing only.
- Old failed job08e0fc5d41e147678f3940e98100ec12 remains failed/INCOMPLETE_RANGE_STOP with unchanged ledger-anchored evidence despite its batch rc0.

Native PASS: raw batch log, console property readback and decoded scalar CSVs were independently checked.
- Completed; compile/batch return codes 0. Actual native element counts [300, 320, 320]; transient DOFs 79485 plus 12 internal.
- 1143 readable Time/Variables properties; zero differences from the R320 H0125 baseline, including maxstepexpressionbdf.
- Existing A and control both used 16 cores; their 1143 native Time/Variables properties differ only in maxstepexpressionbdf (A uses 0.005/0.025 s late caps).
- 987 stored rows and 986 accepted intervals; all 187 requested times stored exactly.
- Stage interval counts: {'initial_to_0p1': 807, 'middle_0p1_to_1': 98, 'final_1_to_5': 81}. Caps are 0.000125 s through arrival at 0.1 s and 0.1 s afterward. The 1 s split is reporting only and has no expression change.
- Arriving and departing intervals at both 0.1 and 1 s are recorded separately in JSON. No unresolved crossing; all caps pass with 1e-12 s rounding tolerance.
- Native core readbacks: baseline [2, 2]; new [16, 16]. The cap and all solver settings are unchanged.
- Each electrode profile contains 241 finite points at every stored time, with exact time/domain alignment and invariant physical coordinates.
- Consecutive stored times define h; native indices, printed times and printed h agree within displayed rounding. This does not establish the solver expression evaluation point.
- OCP guard remains zero and surface bounds pass. Minimum electrolyte concentration = 1194.4372136345673 mol/m³, checked only in postprocessing.
- This single execution control is not a true time-error bound, full-convergence proof, repeatability assessment, or performance benchmark. Identical accepted counts and histories are not assumed.
- Precise boundary intervals, input hashes and independent summary/CSV cross-checks are in INDEPENDENT_NATIVE_AUDIT.json.

The audit wrote only this report and its JSON companion; original source/raw result files were read only.

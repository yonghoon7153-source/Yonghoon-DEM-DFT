# Independent source/native audit

Audit completed: 2026-09-14T17:18:41.726108+09:00

Source PASS: full baseline text after only two class/label replacements and two Nel160-to-320 replacements equals the new source (line endings normalized).
- Baseline: `outputs/comsol63/radial160_timecap/Caps300R160H0250.java` / `4b4ff66bca7a161f6acffd5b125ddf695fee95fb82cdb4ded1e8b63391e1e5f0` / job `15e5d7433a6a4956b820cf6952330735`.
- New: `outputs/comsol63/radial320/Caps300R320H0250.java` / `837f8b03ff3381bb1aea6397935d0079b032f5e4aea007b32d1ebf7c40775b2e` / job `f0db6d080ad04045a2b43dc5a51d89b2`.
- Physical mesh 300 (120/60/120), radial mesh 320 per electrode, 187 requested times through 5 s, one runAll call. All other source content is unchanged.
- Atomic contract identity, source configurations and job records agree. No external read/process/network additions.
- Worker wall-clock budget 1200 s versus reference 600 s is separate from the unchanged physical 5 s and COMSOL Time settings.
- Four OCP/entropy functions retain extrapolation none. The two StopCondition guards are evaluated after time steps; they do not protect rejected Newton trials. Electrolyte positivity remains postprocessing only.
- Old failed job08e0fc5d41e147678f3940e98100ec12 remains failed/INCOMPLETE_RANGE_STOP with unchanged ledger-anchored evidence despite its batch rc0.

Native PASS: raw batch log, console property readback and decoded scalar CSVs were independently checked.
- Completed; compile/batch return codes 0. Actual native element counts [300, 320, 320]; transient DOFs 79485 plus 12 internal.
- 1143 readable Time/Variables properties; all agree with the R160 H0250 baseline, including the cap expression.
- 593 stored rows and 592 accepted intervals; all 187 requested times stored exactly.
- End time <= 0.1 s, including arrival: 414 intervals, 386 at cap; max h = 0.00025000000000001 s.
- Start time >= 0.1 s: 178 intervals; max h = 0.05 s. No unresolved crossing; all interval caps pass with 1e-12 s rounding tolerance.
- Consecutive stored times define h; native indices, printed times and printed h agree within displayed rounding. This does not establish the solver expression evaluation point.
- OCP guard remains zero and surface bounds pass. Minimum electrolyte concentration = 1194.4372136345733 mol/m³, checked only in postprocessing.
- Cap compliance is not true time-error validation or complete convergence. Reused R160 H0250 and new R320 H0250 adaptive histories are compared without assuming they are identical.
- Precise boundary intervals, input hashes and independent summary/CSV cross-checks are in INDEPENDENT_NATIVE_AUDIT.json.

The audit wrote only this report and its JSON companion; original source/raw result files were read only.

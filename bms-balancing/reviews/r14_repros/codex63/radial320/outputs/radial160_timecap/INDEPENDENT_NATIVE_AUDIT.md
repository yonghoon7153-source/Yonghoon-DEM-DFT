# Independent source/native audit

Audit completed: 2026-09-14T13:59:37.568395+09:00

Source PASS: full baseline text after only two class/label replacements and two cap-expression replacements equals the new source (line endings normalized).
- Baseline: `outputs/comsol63/radial160/Caps300R160H0500.java` / `874e70a9d6531a2a83ebd05f439d514c324b3ca79875494b1cf304797cc90e26` / job `450b46add79c439bbce5886454c4328a`.
- New: `outputs/comsol63/radial160_timecap/Caps300R160H0250.java` / `4b4ff66bca7a161f6acffd5b125ddf695fee95fb82cdb4ded1e8b63391e1e5f0` / job `15e5d7433a6a4956b820cf6952330735`.
- Physical mesh 300 (120/60/120), radial mesh 160 per electrode, 187 requested times through 5 s, one runAll call. All other source content is unchanged.
- Atomic contract identity, source configurations and job records agree. No external read/process/network additions.

Native PASS: raw batch log, console property readback and decoded scalar CSVs were independently checked.
- Completed; compile/batch return codes 0. Actual native element counts [300, 160, 160]; transient DOFs 40765 plus 12 internal.
- 1143 readable Time/Variables properties; only maxstepexpressionbdf differs from the H0500 baseline.
- 586 stored rows and 585 accepted intervals; all 187 requested times stored exactly.
- End time <= 0.1 s, including arrival: 407 intervals, 398 at cap; max h = 0.00025000000000001 s.
- Start time >= 0.1 s: 178 intervals; max h = 0.05 s. No unresolved crossing; all interval caps pass with 1e-12 s rounding tolerance.
- Consecutive stored times define h; native indices, printed times and printed h agree within displayed rounding. This does not establish the solver expression evaluation point.
- OCP guard remains zero and surface bounds pass. Minimum electrolyte concentration = 1194.4372147785807 mol/m³, checked only in postprocessing.
- Cap compliance is not true time-error validation or complete convergence. Reused H0500 and new H0250 adaptive histories are compared without assuming they are identical.
- Precise boundary intervals, input hashes and independent summary/CSV cross-checks are in INDEPENDENT_NATIVE_AUDIT.json.

The audit wrote only this report and its JSON companion; original source/raw result files were read only.

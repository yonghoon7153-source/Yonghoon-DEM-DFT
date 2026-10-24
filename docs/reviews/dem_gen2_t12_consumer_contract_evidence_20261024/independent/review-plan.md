# Independent T12 latest-consumer review plan

This is an implementation review plan, not physical qualification or authorization.

Sources read as exact Git objects:

- DEM historical readiness: `2443a63eaa87d52e385a35f8bab4225efa0d25fe`.
- Latest ULPR consumer: `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`.
- Historical ULPR comparison: `8347d32ea678c0174bd77d4c79cfbd7b0591e4a3`.

## Minimum useful implementation

Preserve historical readiness and its old pin. Add a separate latest-pin contract and executable synthetic seam tests against the actual pinned ULPR consumer, with source digests and exact observations. Do not implement a generic pass/fail schema that pretends to qualify P2. The source loader must not silently read the DEM checkout's older ULPR files while reporting the latest consumer pin.

From old to latest ULPR, consumer changes are confined to exact RESUME integer validation and associated records, tests, rule/seal documentation. P1 bed identities, h0, gravity, r8 head, G2/G2c and S0 semantics remain unchanged.

## Required observations / adversarial cases

1. Known P1 bed and unknown P2 bed: actual `gate` rejects unknown bed. Adding a params entry alone does not extend this gate.
2. Valid S0 file vs correct filename with wrong TIMESTEP: actual `_s0_dump` accepts/rejects respectively. An existing malformed `in/` candidate must block a valid lower-priority EXT copy.
3. Exact unique positive particle IDs; fractional, duplicate, nonfinite and unknown-to-S0 IDs. Use raw text mutation after fixture serialization where the helper writer coerces IDs to integers.
4. G2 mass-only mutation: **PASS**, a recorded coverage limitation. Type mutation: FAIL. G2 does not compare all atom inventory or rotation fields.
5. Same geometry but changed primitive-floor history: `_hist_equal` must be false for changed `f_history_zwall_bot[1]`. Do not call this a G2c delta_max test; G2c explicitly is not a standalone hidden-history proof.
6. G2c missing required contact column: NOT_COMPUTED; changed observed force: FAIL. Preserve the distinction in reported outcomes.
7. Same tiny total-force input at normal g=9.81 vs auxiliary g=9.81e-6: actual S3 residual can flip PASS/FAIL. Use actual `_arm_g` dispatch and `s3_residual`, not a duplicated formula-only validator.
8. Actual generator UB/UT dt and W maintain 0.005 deck-time windows. Keeping W fixed at dt/2 halves duration; this is an explicit counterexample, not a new P2 window choice.
9. Same pressure/lift bracket and doubled h0: actual `interp_rho` halves rho and percentage bracket, preserving micrometre bracket. h0 is not a display-only value.
10. Actual `_head` remains r8-based even with P2 metadata labels. This does not establish P2 history/material/active fixes.
11. Exact RESUME integer-valued decimal/scientific token is authorized when other evidence agrees. Fractional or ambiguous token is not; no raw CSV mutation or stale-row erasure follows.
12. Old partial tail after restart must not qualify a new attempt. Preserve primary/trajectory status separation.

## Physical boundaries

T12 starts from fixed-plate R-a completion, not servo stop. A synthetic file timestamp is not R-a convergence evidence. Real R-a pressure drop, window policy, S1-S3, active material/history/gravity, S0 inventory, producer/consumer deck identity, restart/mesh/state hashes, dt and physical-time scaling, h0 definition, transfer qualification and resume provenance remain required. Q12 legacy gravity/material exceptions must remain explicit.

`_s0_dump` validates parsed rows, exact unique IDs and requested step; it does not certify the params atom-count, mass or phase inventory. `_atom_frame` rejects extra IDs but does not itself reject same-ID type/mass mutation. These limits must be recorded rather than hidden by tests.

No P2 bed/arm registration, threshold/window selection, physical S0, Q7/Q8/Q9 measurement, LIGGGHTS/MPI run, restoration certificate or external review verdict may be manufactured. No executable P2 launch command exists until the real producer and registration are supplied. P1 run_unload is not a P2 execution substitute.

## Review scope after author freeze

- Inspect all added/changed files and source provenance.
- Execute only the new synthetic harness in independent scratch.
- Recompute source identity; exercise old pin and modified blob refusal where supported.
- Apply independent targeted mutations in scratch to test that claimed counterexamples matter.
- Report direct check counts separately from the repository's existing shared 155 checks; parent owns any full gate/integration run.

Initial review status: source comparison complete; author implementation not yet frozen; no execution or physical qualification performed by this reviewer.

# Solver-focused adversarial design review

Review pin: `1087a9b2f4a93aa6a3b0debc698a14fffa13488d`. Read-only source, no production or real-bed solve. The review ran 18 tiny synthetic actual-function solves, with 16 asserted expectations, using the unmodified pinned `source/scripts/network_conductivity.py`. Temporary fault injection only replaced SciPy call sites in memory and restored them after each solve. Source SHA-256: `da9ecfefd8dc4b84e222140e347e4a718381169f27c88bf56c71ec4a7c2749be`.

Executable evidence: `probes/solver_probe.py`; full strict JSON output: `evidence/solver_probe_results.json`. Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3; all thread settings 1; bytecode disabled. All 16 assertions passed (process exit 0). No source, ledger, registration, or production record was modified.

## Main judgment

The proposed distinction is conceptually correct but is safe only as a **positive, independently checked model-limit classification**. It must not become an allowlist that trusts a reason string, a missing number, a successful process exit, or a CG convergence code.

The pinned solver already distinguishes the lower-level guard internally. `solve_network` first adopts a numerically accepted solution, records its currents/residuals, and only then checks FULL q > 1.5 (`network_conductivity.py:1182–1209`, `:1222`, `:1249–1267`). It emits `status=over_conduction_guard`, `reason="sigma_ratio > 1.5"`. The information is collapsed by `_net_sigma_status` because that reason is absent from `NOT_COMPUTED_SOLVE_REASONS` (`:150`, `:242–246`); `_channel_solve_failure` then turns every FULL `not_computed` into a channel `failed` (`:1898–1910`). This is a model-output rejection being presented as numerical failure, as the source itself expressly explains (`:1225–1248`).

The submitted proposal is incomplete if “not_computed means no certificate needed” remains the downstream rule. Current `certificate_problem` rejects the guard status before checking its numeric fields (`network_conductivity.py:873–895`). Current `tau_flux._cert_unpublished_problem` rejects an absent-value branch with a finite `I_bottom` (`tau_flux.py:616–632`), while `certificate_binding_problems` returns `[]` early if `ion_record_problem` fails (`:747–754`). A model-rejected but numerically solved branch needs a dedicated validated state path; deleting its certificate or making all `not_computed` exempt would remove the evidence that distinguishes it from a solver failure.

## What the submitted run actually establishes

All 14 per-case `network_attempt.json` files were inspected, not only eight. Their reasons are the same collapsed `physics.ionic=fail ... solve_failed` and their worker wrapper exits are 1. All 14 worker `stage_plan` objects show **Network Solver (both modes) rc=0, ok=false** and Network Merge / Stage E rc=1. Their individual `log.txt` files are worker wrappers, not the internal channel solve logs. They show no lower-level q/certificate. All have `active_status=none`, `previous_generation_kept=false`, attempt 1 and no signal.

Consequently the supplied production evidence proves a common **publication-content rejection**, not a common numerical cause. The 13 cases other than the supplied lhsx_054 diagnostic cannot yet be individually classified as model over-conduction. The JSON evidence lists each case and its exact source file. The observed RSS range is 527.8–1937.9 MB; the request's lower endpoint 0.88 GB does not cover `lhss_011` (527.8 MB) or `lhss_003` (843.7 MB). The logs do not suggest a process kill/OOM, but RSS alone cannot prove the absence of a caught numerical-library/resource exception.

The standalone lhsx_054 Physics JSON does directly establish the guard for that diagnostic:

- `solve_certificate_full.status=over_conduction_guard`, reason `sigma_ratio > 1.5`, method CG, one attempt with outcome `pass` and Krylov info 0.
- `I_bottom=106.85001549443174`, `I_top=-106.85001548781166`; conservation residual `6.195679060858629e-11`, internal residual `9.071411744344477e-11`, both well below 1e-6.
- `g_to_q=0.014384959999999995`, delta_V=1, so reconstructed raw q is **approximately 1.53703319888678** (the JSON does not store rejected q directly). The public `sigma_full` remains null.
- Its boundary rule is L0, overlap count 0, percolating fraction 1.0. CF is 2.04783126 with `model_over_conduction`; constriction-only is separately `zero_resistance_requires_contraction` with 23,071 zero-resistance edges. Neither fact proves the FULL result by itself.
- The same diagnostic Hertz H0 FULL q is 0.66147876; Physics electronic FULL 0.00694247 and thermal FULL 3.82380707 are computed.

These are `submitted/lhs214_run_evidence_1014_1520/diag_lhsx054/network_conductivity_physics.json:21–62`, `:105–162`, and the Hertz companion `:21–62`, `:158`. The diagnostic file does not include raw atoms/contacts or their digests. Thus this review can confirm its internal guard/certificate, but cannot independently bind that standalone rerun to the original failed attempt's input digests. It is stronger than the request's “likely cause,” but not a substitute for the missing per-attempt certificates for all 14.

## Actual-function counterexamples and controls

The basic graph has nodes 0–1–2, bottom {0}, top {2}, two R_total=0.25 edges, unit scale and box dimensions. Its exact solution is V=(1,0.5,0), G=2, currents +2/-2, and both residuals 0; all-edge sum_g=8, so the parallel bound passes. With plate_z=1 its raw q=2.

| Probe | Actual pinned result | Consequence |
|---|---|---|
| FULL q=2 | Numeric attempt `pass`; `(None,None)`; internal `over_conduction_guard`; producer `not_computed/solve_failed` | Reproduces the exact conflation without a real bed |
| FULL q=1.5 | `(2,1.5)`, computed | Threshold is strict `>` |
| FULL q=1.49999998 / 1.50000002 | First retained, second withheld | Classify raw q before publication rounding |
| CF q=5 / constriction-only q=3.3333333333333335 | Values retained, `model_over_conduction/q_gt_1p5` | These are existing diagnostic branches, not the new FULL withheld-value state |
| Thermal FULL q=2 | Computed | Thermal is a multi-phase normalization; preserve its exemption |
| Same high-q graph; first direct-solve exception injected | `solve_failed`; one exception attempt | Do not infer guard merely from geometry or expected q |
| Same graph; wrong vectors injected into all rungs | `current_conservation_failed`; no adopted currents | Certificate failure takes precedence |
| Same graph; nonfinite vectors injected | First `not_converged`; later zero-accumulator certificate failures; final `current_conservation_failed` | Preserve attempt-level outcomes; final reason alone may not describe the first fault |
| Same graph; nonconvergence injected | `solve_failed` | Must still block |
| Zero-conductance graph | `parallel_bound` attempt; final `solve_failed` | G≤0 is not a model-output limit |
| Overlapping electrodes | `not_computed/boundary_overlap`, no solver method | Invalid boundary problem, not an accepted model-limit solution |
| No through path | `valid_zero/no_through_path` | Preserve graph-proven zero |
| Constriction-only R_c=0 | `not_computed/zero_resistance_requires_contraction` | Preserve its separate existing diagnostic policy |
| **plate_z=+Infinity, otherwise same valid circuit** | Numeric currents/residuals pass; raw q=Infinity; **same `over_conduction_guard` reason** | A reason-only exemption would misclassify nonfinite/invalid geometry as an acceptable model limit |
| plate_z=NaN | Returns G=2,q=NaN; producer `not_computed/non_finite` | Check conversion and q explicitly, not only linear solve |

For guarded records the existing certificate checker returns a status rejection. The JSON field `numeric_checker_on_status_normalized_copy` runs that checker on a **copy** whose status alone is changed to `computed` to isolate the numeric gate. It is an inspection technique, not a proposed production shortcut. The actual unmodified certificate and actual checker result are also recorded.

## Required decision order and evidence

1. Validate schema, channel/branch/mode role, run/input provenance and positive finite geometry/conversion inputs. Validate that the graph/edge data are admissible for the selected branch; malformed input cannot turn into model-limit success. Preserve existing independent topology/boundary checks.
2. A graph-proven absence of a bottom-to-top component remains `valid_zero/no_through_path`. Overlapping electrodes remain a rejected boundary problem. Existing constriction-only zero-resistance handling remains separate. None of these are evidence of a solved FULL network.
3. Run the existing numerical ladder unchanged. An exception, nonconvergence, nonfinite vector/current, failed conservation/residual, G≤0, or failed parallel bound remains a technical failure. Preserve every rung's outcome; a stable aggregate reason plus structured subreasons is preferable to discarding earlier faults. The stale `V_source≤0` phrase at line 212 is not a live branch in the exact-Dirichlet solver: delta_V is fixed to 1 at `:818` and `:956`; `V_source=1` is field compatibility output at `:1299`.
4. Only after an adopted certified solution, compute q with the existing exact expression/order (`:1218–1222`), reject nonfinite/nonpositive geometry factors, G, sum_g, conversion result or q, and apply the existing G/parallel checks. **Finite q>1.5**, FULL, ionic/electronic single-phase, numerical pass is the necessary model-limit predicate. q=1.5 remains computed; do not compare rounded q.
5. Emit public FULL sigma and dimensional sigma as null with structured `not_computed/full_over_conduction`; retain diagnostic raw q, immutable threshold/policy version and the accepted FULL numeric certificate and binding (branch, channel, role, contact_mode, delta_V, geometry, g_to_q, parent sigma0). Suggested explicit distinction: numeric solve status pass versus output/model status rejected. Include sum_g or parallel-bound evidence if downstream is expected to independently validate that bound; current certificates preserve the pass attempt but not sum_g.
6. At publication/re-read/τ/handover gates, verify this exact predicate using one shared validator. Require complete finite certificate/binding evidence for the **new model-limit state**, despite absent public sigma. Verify diagnostic q reconstructs from this certificate and that it really exceeds 1.5. Missing/unknown/mismatched reasons, forged model-limit status, absent certificate, wrong branch/channel/role, bad geometry or conservation must stay failures. Do not globally relax certificate requirements for other `not_computed` states.
7. Preserve derived-value semantics: no FULL τ, no FULL-dependent ratios or CPS value computed from the withheld q, no conversion to valid_zero, no fallback substitution into Physics. CPS currently receives the blanket failure string at `:1522–1523`; it needs an explicit model-limit unavailable reason. CF and constriction-only independently solved diagnostics can retain their existing values/states/certificates.

## Q1, Q2 and Q4 advice

**Q1:** Conditionally approve (가). C1-5's withheld FULL value remains withheld, and WEB-03 Q1's numerical-failure block remains intact. This is an explicit policy extension for a numerically solved, model-rejected value; current literal predicates do not already support it. Approval should include the strict guard/certificate requirements above, not just a renamed reason or channel allowlist.

**Q2:** Use one classifier across Physics, Hertz H0 and H12. Apply the q criterion to ionic/electronic single-phase FULL; preserve thermal's different bound. Classification and release eligibility are distinct: an H0 model-limit record can be retained with its explicit missing primary value, but it must not satisfy a v1.3 deliverable requiring the primary Hertz quantity. The main-value release gate should hold it; changing that eligibility requires an explicit registered release rule, not a mode-specific falsification of the solver status. H12 sensitivity is also explicit; it cannot be substituted for H0.

The outer producer currently copies electronic/thermal certificates but not their FULL sigma status/reason (`network_conductivity.py:1771–1797`, `:1821–1840`, `GEN2_CHANNEL_KEYS:1856–1857`). A common classifier therefore needs explicit reason/status propagation for those channels and their readers, not only ionic handling. `CHANNEL_STATES:1916–1917` does not currently include a model-limit channel state; preserve the difference between field-level and channel-level statuses.

**Q4:** In addition to registered fast16/real4 and campaign/receipt checks, require the new regression matrix to cover the actual 3-node guard, just below/at/above 1.5, Physics/H0/H12, electronic, thermal exemption, CF/constriction-only retention, no-through, overlap, first-rung exception, nonconvergence, bad/nonfinite certificate, nonfinite raw q/geometry and parallel-bound failure. Add serialized negative cases (reason-only forgery, missing/foreign certificate, wrong reconstructed q, unknown reason, stale valid-null/coerced-zero state), and cross-consumer agreement in both ordinary and stop paths. Unaffected numeric outputs must remain bit-identical under the same deterministic environment; metadata/schema additions should be compared separately.

Before claiming “14 Physics model limits,” retain each of the 14 actual FULL certificates, raw q and source/input binding from preserved per-attempt staging files, or from approved isolated diagnostics tied to the attempt digests. This review did not run those diagnostics. A fresh sealed all-214 campaign must evaluate each case from its own evidence; it must not assume exactly the historical 14 become model limits. The old failed attempts remain history. New registration/seal/receipts and approval must precede the next launch.

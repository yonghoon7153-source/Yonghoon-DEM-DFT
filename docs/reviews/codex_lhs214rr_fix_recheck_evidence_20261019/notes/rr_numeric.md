# R01 / R04 independent numerical review notes

Pin: `77d8fd44545c33cd10ab18fc250c7ad3023833ea`. Read-only source; no DEM, no 214 production run, no prior artifact modifications. All probes use bundled Python `-X utf8 -B`, OMP/OpenBLAS/MKL/NumExpr threads=1, existing dependency roots. Read `source/AGENTS.md`, `submitted/request.txt`, prior 10-17 report.

## Disposition

- R01 original numeric resurrection counterexample: closed in the tested contract. Raw certified q, not stored rounded q or guard diagnostic self-report, determines the strict FULL threshold. Producer `network_conductivity.py:1422` sets `G_eff = I_bot`; `:1435` computes `G_eff * T_um / A_um2`; `tau_flux.py:796` reconstructs `(float(I_bottom) / delta_V) * T / A` after enforcing delta_V=1 and producer geometry. `:807` uses strict `>` against producer `FULL_Q_GUARD_MAX`. Normal FULL equality is accepted, next representable q above is rejected.
- R04 stated ionic branch/certificate status+reason contract: closed in tested cases. `tau_flux.py:817–824` matches both branch and certificate tuples against raw-q semantics. High q CF/constriction remains numeric with `model_over_conduction/q_gt_1p5`; label changes are record corruption. Whole-record invalidation agrees with the pre-existing declared assembled/edited-record policy (`tau_flux.py:687–691`), even though FULL numeric values themselves have not changed in a label-only mutation.
- No new numeric bypass or normal-input overblocking reached the actual ionic contract in these probes. A new residual **channel-level metadata contradiction**, described below, does reach actual stop/content/record contracts; it does not falsify the narrower R01/R04 numerical closure or change tau values.
- Other-channel closure cannot be inferred. Thermal uses `network_conductivity.py:1467–1478`'s separate parallel-conductance bound and does not use the ionic CF q>1.5 label rule. Electronic uses the single-phase rule but is explicitly excluded from this ionic tau binding. Do not apply the ionic rule indiscriminately to thermal.

## Submitted tests, including the failure

`evidence/rr_numeric_submitted.json` and matching `.log` files:

- R01: **rc1, 23/26 PASS**, not 27/27. R, C, and B checks all pass. The submitted 21-node E fixture's hardcoded geometry (`test_l214r_r01_restored_full.py:61–64`, `:246–261`) gives raw q next/equal/previous `1.4999999999999962`, `1.4999999999999958`, `1.4999999999999956` here. All are below 1.5, so E1 and E3 fail; `restore()` then accesses nonexistent `q_withheld` at `:119` via `:273`, raises KeyError, and prevents E4/E5 from executing in that submitted invocation. The aggregate counts one exception, explaining 26 instead of 27 checks.
- R04: **rc0, 12/12 PASS**. Normal producer 18 computed FULL branches; CF/constriction 51 high-q plus 21 ordinary branches; 15 actual record verdict checks; exact equality/next boundary accepted with correct diagnostic label and rejected with flipped label. Its constriction `prev` input rounds raw q to equality, so it is not an exact predecessor-q test on this runtime.
- Runtime is Windows 11, Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3. Request states Linux/Python3.11. Thus the result does not disprove the submitted Linux log but does disprove an unqualified local “27/27 reproduced” statement.

Independent exact 3-node boundary proves expected q behavior without using the failed chain's assumed q. A separate **explicitly derived**, locally calibrated 21-node input also recovers all five original E assertions, retaining their expected values and production code: area `0.500000001001` instead of `0.500000001`, x `0.7281737983374794`, y next/eq/prev `0.7281737983380614`, `0.7281737983380615`, `0.7281737983380616`. Actual freshly solved q equals `1.5000000000000002`, `1.5`, `1.4999999999999998`. Original test failure remains recorded; it is not relabelled as passing. See `rr_numeric_chain_boundary.py`, `.json`, `.log`. Recommended nonblocking test improvement: explicit runtime/precondition handling and run exact 3-node boundary independently of chain failure; do not allow KeyError to skip the remaining boundary checks.

## Independent probes

`probes/rr_numeric_independent.py` -> `evidence/rr_numeric_independent.json`: rc0, failures=[]:

| Set | Count | Result |
|---|---:|---|
| Actual 3-node FULL / CF / constriction boundary and large-q retention | 12 | Expected producer and consumer behavior |
| Actual solves across finite unit scales/geometries, q .001/.4/1.4/1.6/20 | 75 | No overblocking; high-q FULL restoration refused |
| Branch + certificate status/reason permutations across H0/Physics/H12 | 1,008 | Exactly expected tuples accepted; no exceptions |
| Full scalar/parent/percolation NULL, NaN, infinities, huge integer, bool, string, containers, zero/negative | 144 | Technical rejection; tau NOT_COMPUTED, f blank |
| CF/constriction scalar and all three published certificate numeric-type corruptions | 594 | Binding rejection; tau NOT_COMPUTED; no exceptions |
| Invalid/extreme geometry before empty graph classification | 56 | Producer rejects invalid geometry first, no exception |
| Restored FULL guard diagnostic keys deleted or replaced | 36 | Raw q=2 still rejected by R01 |

Fresh normal record is independently produced from 21 SE grains with uneven contact areas/deltas at 60 C, Ea=.3 eV, box3x3, not a submitted fixture. It remains g2 and tau OK. This does not establish physical realism or all-input nonimpact.

`probes/rr_numeric_old_derivative.py` executes the old independent probe bytes with only explicit replacements recorded in `rr_numeric_legacy_derivative_manifest.json`: old fixture input read-only, new evidence output, new pin; current source imported. Result `rr_numeric_legacy.json`, rc0:

- H0 restored actual raw q=1.6231747351909995: record False, generation invalid, tau NOT_COMPUTED/f None. Physics restoration likewise rejected.
- 252 adoption mutations: accepted0/exceptions0. Ledger36: failures0.
- Known K1 getter infinity, K2 big-int temperature exception, K3 historical zero-meta infinity and unpublished-current nonfinite/bool/string permissiveness remain observable, unchanged. Do not describe those as repaired or new.
- The old probe's direct `v13_primary_model_limit_problems` can still return [] for the now invalid tau row. This is not a bypass: record/source/generation guards reject the row first. Do not quote that isolated helper as overall acceptance.

## Newly observed residual channel label contradiction (candidate P3, nonblocking numeric scope)

Actual fresh record baseline: H0 `sigma_full_status=computed`, sigma_full=0.09025782, valid positive certificate/percolating_fraction; `ionic_status=computed`. Baseline content, record, stop all return `[true, "ok"]` (content reason names modes), generation g2, tau OK/f=.09025782/tau2=5.4144027692937.

Change **only two semantic leaves** in H0: `ionic_status='valid_zero'`, `ionic_status_reason='no_through_path'`; propagate its required JSON copies and full_metrics projection. The numeric branches, every certificate, geometry, currents, residuals and scalar values remain unchanged. **Actual `network_content_verdict`, `network_record_verdict`, `network_stop_verdict` all accept**, generation g2, tau remains OK with identical f/tau2. `valid_null` and `no_result` variants also pass. Probe and all record folders are new review artifacts: `probes/rr_numeric_scope.py`, `evidence/rr_numeric_scope.json`, `tmp/rr_numeric_scope_*`.

Why contradictory: producer `network_conductivity.py:2034–2048` uses status_for_value for a positive value, and assigns channel valid_zero only to the genuine branch `valid_zero/no_through_path`; H12 equivalent at `:2119–2126`. `status_for_value` at `:2178–2185` returns computed for a positive numeric value and valid_zero for zero. Consumer `pipeline_service.py:776–780` permits these status vocabulary entries and `:818–819` accepts them without binding to computed FULL data. `tau_flux.py:252–280`'s computed path does not bind `ionic_status`; its valid_zero path does (`:292`). R04 only checks branch and solve-certificate tuples at `:817–824`, not channel status. This is an additional metadata-integrity hole, not a raw-q or numeric-adoption bypass.

The identical fixture and mutations were independently run in a second process against the immutable 10-17 `60ba39e22` source tree: `rr_numeric_scope.py <old-source-path>` -> `evidence/rr_numeric_scope_base.json`. Baseline and all three channel mutants again pass content/record/stop with identical g2, tau OK, f=.09025782/tau2=5.4144027692937. The producer and pipeline_service files are byte-identical between the two pins. Thus this is demonstrably pre-existing, not an introduced regression. The review has not yet demonstrated a user-visible display error; its established impact is contradictory accepted channel metadata.

Recommended disposition: report it as a separate P3 residual if the review claims channel-status consistency. Keep R04's explicitly stated branch/certificate scope closed; do not block ionic numerical GO solely on this metadata mismatch. Minimal future fix: for current/g2 records, bind ionic channel category to actual FULL branch category/value while preserving genuine no-through and model_limit cases. No need to enforce prose reason equality blindly, since producer reasons include descriptions.

Same scope probe flips thermal full/CF/constriction certificate status+reason to `model_over_conduction/q_gt_1p5`; actual stop still accepts, confirming the already declared other-channel exclusion. No electronic certificate exists in this all-SE fixture, and the probe does not claim to test an electronic label mutation.

## Exact limits for report

- Review supports explicit R01/R04 closure, not every status field or every numerical input.
- Test-portability failure is real and must be disclosed, even with successful independent boundary coverage.
- Full fresh-build/end-to-end derivative review belongs to the consumer agent; numerical notes do not independently claim release acceptance/refusal beyond the actual calls described.
- Registration/resealing/B7/214/S3 decisions remain outside these probes.

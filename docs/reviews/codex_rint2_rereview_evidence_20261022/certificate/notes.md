# RCA-07 certificate re-review — 2026-10-22

Scope: review pin `0b3012460fb8e8b7d53484b0efe399e2dc506aec`, compared with `5dc6f7f0b`. Read-only inspection and bounded synthetic probes; no real bed, S0 measurement, campaign, or production changes. Runtime: Python 3.12.14, NumPy 2.5.3, one OpenBLAS/OMP/MKL thread. Scripts imported from the pinned `source/scripts` tree. Parent intake independently verifies the ZIP/pin match.

## Verdict

**RCA-07's numerical sufficiency defect is closed for the declared passive edge ledger and floating-point model. Conditional GO for using certificate d as the numerical gate.** The three previous actual zero-start CG counterexamples still pass A/B/C in this environment, but d rejects every one and its interval contains the analytic conductance. The old A/B/C seal remains an empirical, execution-path-dependent diagnostic. The new theorem does not need the old calibration network or its BLAS path.

“Path independent” should mean the error guarantee is independent of how the candidate potential was obtained. It does **not** mean every platform must return identical intervals or the same acceptance at the tolerance boundary. The bound is a float64 roundoff analysis with explicit normal-range assumptions, not a machine-checked directed-rounding interval implementation. Its target is the positive resistor network reconstructed from upper-triangle off-diagonals plus plate conductances; it is not a certificate of physical geometry, constitutive correctness, or an arbitrary asymmetric/grounded matrix.

A new downstream defect, owned by the geometry reviewer, still prevents treating the SV decision as a guaranteed graph bracket: projection discards certificate endpoints and the chain compares nominal ratios without their numerical uncertainty. This does not invalidate d itself.

## Why the bound is mathematically sufficient

Let the true network voltage be v*, with bottom 1, top 0 and internal values in [0,1]. For any candidate p, Dirichlet gives G* <= U(p) = sum g(dp)^2. For any represented edge flow q, let d be internal incoming minus outgoing flow, FB and FT the bottom/top totals, and W = sum q^2/g. Discrete summation by parts gives sum q dv* = FB - sum v*d = FT + sum (1-v*)d. Therefore it is at least either FB-sum max(d,0) or FT-sum max(-d,0). Cauchy-Schwarz gives G* >= max(0,these expressions)^2/W. The implementation's Dp/Dm bound positive/negative residual defects of the **final represented q**, so the tree correction need not be exactly conservative. The tree improves tightness; the defect allowance establishes validity.

Relevant implementation: `step3_conv_cert.py:427` bracket, `:494`–`:517` tree correction, `:519`–`:532` final defect and W, `:541`–`:568` defect allowance and lower endpoint, `:572`–`:606` exact rational acceptance. The accepted condition is |Ghat-G*| <= 1e-4 Ghat, with the published Ghat as denominator, as the revised registration now explicitly states. Requiring literal Ghat inside the interval is unnecessary: any Ghat within the registered tolerance of both endpoints is safe.

The U rounding allowance covers the repeated voltage difference, multiplication terms, grouped fsum and endpoint arithmetic. W uses represented q directly, with division/multiplication allowance. The final node defect estimate includes the sequential summation allowance; the numerator uses an absolute subtraction allowance, which matters near cancellation. The acceptance comparison itself uses exact fractions. No unsoundness was found in the independent bounded stress set.

## Replayed previous counterexamples

Source: the prior `rint2_carbon_design_review_20261021/geometry/convergence_probes.py`, now bundled as `certificate/baseline_convergence_probes.py`. Its numerical function bodies are unchanged; only imports are made portable and the old standalone writer is omitted. The original remains untouched. The wrapper imports the bundled copy and directs it to the selected source modules. Exact values are retained in `results.json`.

| Case | Actual reported relative error (Ghat/G* - 1) | A/B/C | d | Certified interval |
|---|---:|---|---|---|
| main, 11 DOF, iterations 10 then 0 | -1.88593002408699e-4 | all true | false | [1.647535053651848e-9, 1.647535053652371e-9] |
| connected, 7 DOF | -9.03708616602072e-3 | all true | false | [2.10862372290885e-12, 2.10862625786561e-12] |
| original 23-iteration family, 24 DOF | +5.12087249354698e-4 | all true | false | [1.14082291548657e-5, 1.14082333591574e-5] |
| explanatory warm candidate, Ghat=.25, G*=1/3 | -.25 | all true | false | [0.333333333333329, 0.375000000000001] |

Exact disconnected-terminal zero is now `VALID_ZERO_TOPOLOGY`, ok true. A nonzero candidate current on the same zero topology is rejected. One finite-resistance node connected to both plates is correctly a positive solved network; it is not an ideal electrode short. Explicit `cjunc_electrode_short` remains nonpublishable. Floating internal components do not invalidate the bound; their energy can make the upper bound loose.

## Independent and native checks

`probe_certificate.py` generates 180 small networks with 2–7 nodes and exactly representable dyadic conductances spanning roughly 2^-44 to 2^44. Each is tested at its rationally solved potential rounded to float, an arbitrary potential in [-1,2], and a small perturbed potential. A separately implemented Fraction Gaussian elimination supplies exact G*. Exact rational candidate energy checks the upper bound independently.

- 540 candidates; 540 intervals produced.
- Zero intervals missed exact G*; zero upper endpoints fell below exact candidate energy.
- 192 candidates passed d; zero false passes against exact |Ghat-G*| <= Ghat/10000.
- Normal scales 1e-290 and 1e290 produced valid brackets; subnormal 1e-320 was rejected.
- Selected bounded native groups T1,T2,T3,T6,T7,T8,T10,T11,T13,T15,T16,T19,T21: **202/202 PASS**, 0.3 seconds reported test time. This includes native high-degree/duplicate arithmetic, knife-edge exact-comparison checks, topology, and solver/manifest binding. The full large-bed sealing/performance campaign was not run.

## Consumer enforcement and limitations

`step3_sigma.py:2282` calls the new certificate; `:2289`–`:2293` marks failures unconverged. `run_contract.py:865`–`:906` requires the new version, all four checks, exact sealed constants and rule version, positive topology, and Ibot*scale matching posted sigma; it reruns `target_judge` on lo/hi/Ibot. `:917`–`:986` binds grid and plan fingerprints to the manifest. Native T21 passes, including swapped zero/positive cases, plans and channels. `rint_r_chain.py:1347`–`:1352` recomputes the calibration protection-band error from the bracket; it does not trust the cached `target_err_bound_rel` field.

Own mutation checks reject old version, wide or reversed bracket, wrong grid/plan fingerprints, and short status. Diagnostic fields target_U, target_W, I_top and sigma_resolve can be changed inconsistently while the validator still accepts, provided the decision fields are unchanged. This is a record-consistency limitation, not an observed producer numerical failure or a bypass of the enforced d interval test. Tightening it would improve transported-record validation, but does not reopen the original RCA-07 theorem defect. For cj-only runs, fp_sig is format-checked rather than matched against a canonical sigma table; this is already explicitly documented at `run_contract.py:928`–`:930`. No claim of cryptographic authenticity or matrix L/b binding is justified.

## New narrow robustness observation (P3, nonblocking for registered physical range)

**Finite subtotals can overflow the uncaught final fsum.** At `step3_conv_cert.py:476`, `U = math.fsum([u1,u2,u3])` is outside an overflow handler. With five independent nodes, each gb=gt=8e307, phi=.5, all L diagonal entries are finite (1.6e308), each energy subtotal is finite (bottom 1e308 and top 1e308), but their final sum raises `OverflowError: intermediate overflow in fsum` before the intended NOT_CERTIFIABLE branch at :478. `results.json` contains `topology_scale.finite_subtotals_overflow`.

The same naked final summation appears for W at :553. Minimum fix: use the guarded summation helper or catch OverflowError/ValueError at both aggregate sums, then return structured NOT_CERTIFIABLE; include this exact five-node test. This is outside the registered conductivity range and fails by aborting rather than publishing an incorrect value. It should not be promoted to a production numerical-soundness blocker.

## Cross-check of the SV reviewer finding

In `geometry/geometry_results.json:951`, the actual producer/certifier pipeline accepts a small solver-potential perturbation (1e-8, no evidence fields edited). Full and cut certificates pass A–D. Recorded ratio 10.291249475344962 is below threshold 10.291251705345072 and the chain emits no SV flag. However, the certificate endpoints themselves yield:

    lower = 4.614912078629503 / 0.44843049327354356 = 10.2912539353438
    upper = 4.614912078630166 / 0.4484304932734833  = 10.2912539353466

The complete certified interval is above the threshold. Thus the contradiction does not depend on treating a floating direct solve as exact truth. This is an admissible-candidate sufficiency counterexample, not a claim that an unmodified zero-start CG run naturally produced that perturbation. Minimum fix belongs to the geometry finding: retain and validate each endpoint's interval, propagate full/cut interval ratios, and classify a crossing numerical interval as SV_UNCHECKED. A looser but safe fallback uses the sealed tau envelope, ratio*[(1-tau)/(1+tau),(1+tau)/(1-tau)], provided every relevant solve is actually certified. This may conservatively return unchecked even where tighter endpoints prove dependence.

## Reproduction

Use the Python runtime recorded by the parent. Set PYTHONPATH to the existing `lhs_coverage_review_20260930/deps` and `gen2_network_reverify3_20261007/deps`; set OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1 and PYTHONDONTWRITEBYTECODE=1. Run `certificate/probe_certificate.py`, then `certificate/run_selected_tests.py`. Outputs are confined to this certificate folder. No production source is patched.

Both tools accept `RINT_REVIEW_SOURCE` as the source root containing `scripts/`; the default is the review root's `source/` directory. No earlier review directory is needed for numerical replay: its baseline probe is included here. Dependencies can also be supplied by a normal environment with NumPy/SciPy.

After this portability change, the bounded probe was rerun: `results.json` is byte-identical to the previous run (SHA-256 `a2cef264f4c894223ce84ea0c06357a12643bb9c10ce4a8ecdd2ff56197e21fe`). The 540 interval checks and 192 accepted candidates retain zero misses/false passes. The selected native suite was rerun with explicit `RINT_REVIEW_SOURCE`: 202/202 PASS. The original prior probe retains SHA-256 `9bb6e340713cb6edaceaf422ba906de15072d5b528e5ca927d0821036e8dc579`.

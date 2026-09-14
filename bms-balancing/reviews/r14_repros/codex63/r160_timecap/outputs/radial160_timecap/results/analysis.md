# One new R160 H0250 time-cap comparison

One authorized new 300/R160 H0250 5 s run versus fixed existing 300/R160 H0500. Prior same-cap R80-to-R160 results are magnitude context only. No COMSOL execution by this analyzer.

Exact Decimal requested-grid and all-exact-common-native-stored-time comparisons are separate; native finite-element spatial interpolation on fixed 241-point electrode grids; no external spatial or temporal interpolation.

| Time basis | Window | Compared times | Max voltage difference (mV) | Time (s) | Max pointwise surface-x difference | Time / electrode / coordinate (m) | Within limits |
|---|---|---:|---:|---:|---:|---|---|
| requested_grid | 0–1 s | 107 | 0.002175461073 | 0.005 | 4.3003216e-08 | 0.002 / P / 0.000121 | True |
| requested_grid | 0–5 s | 187 | 0.002175461073 | 0.005 | 4.3003216e-08 | 0.002 / P / 0.000121 | True |
| all_exact_common_stored | 0–1 s | 282 | 0.002175461073 | 0.005 | 4.3003216e-08 | 0.002 / P / 0.000121 | True |
| all_exact_common_stored | 0–5 s | 363 | 0.002175461073 | 0.005 | 4.3003216e-08 | 0.002 / P / 0.000121 | True |

Only the same-R160 H0500-to-H0250 pair is the primary comparison. Both fixed requested windows and all exactly common stored windows are reported. Missing requested times cannot be replaced by other common times. The maximum-voltage row, maximum-surface-time row and signed component differences are stored together; component maxima at unrelated times must not be summed.

Snapshots preserve 0.01 s, 0.04 s and each new primary voltage/surface peak, with full same-coordinate profiles. Prior same-cap radial differences are read from unchanged old native CSVs only for magnitude and same-time context. No convergence order or mixed-cap radial claim is made.

- Pointwise maxima are maxima over specified common spatial and temporal samples, not continuous-space/time bounds.
- t=0 is after CDI and consistent initialization.
- Only t<0.1 s uses the tighter cap; later-time error is not independently controlled by this experiment. Actual step/binding checks are a separate native-log audit, not inferred from the configured expression.
- Exactly common stored times are an intersection, not the union of adaptive histories. Unmatched times are not compared or interpolated.
- Pairwise agreement does not prove a true-solution error bound or unrestricted radial/time convergence. Passing 1 mV alone does not establish smallness relative to the prior 1.2482181141973 mV radial difference.
- The maxstepbdf constant slot is inactive in expr mode.
- Source/native audits establish physical invariants absent from the CSVs. No threshold or OCP adjustment and no rewriting of failed states.
- A mixed R80H0500-to-R160H0250 difference is not a pure radial comparison and is not reported as one.

Caps300R160H0500: analyzed; physical checks=True; 

Caps300R160H0250: analyzed; physical checks=True; 

# One new R320 H0250 radial comparison

One authorized new 300/R320 H0250 5 s run versus fixed existing 300/R160 H0250. Only this radial pair is analyzed. No COMSOL execution by this analyzer.

Exact Decimal requested-grid and all-exact-common-native-stored-time comparisons are separate; native finite-element spatial interpolation on fixed 241-point electrode grids; no external spatial or temporal interpolation.

| Time basis | Window | Compared times | Max voltage difference (mV) | Time (s) | Max pointwise surface-x difference | Time / electrode / coordinate (m) | Within limits |
|---|---|---:|---:|---:|---:|---|---|
| requested_grid | 0–1 s | 107 | 0.6170341087 | 0.002 | 1.03619785e-05 | 0.002 / N / 0.000052 | True |
| requested_grid | 0–5 s | 187 | 0.6170341087 | 0.002 | 1.03619785e-05 | 0.002 / N / 0.000052 | True |
| all_exact_common_stored | 0–1 s | 490 | 0.6170341087 | 0.002 | 1.03619785e-05 | 0.002 / N / 0.000052 | True |
| all_exact_common_stored | 0–5 s | 571 | 0.6170341087 | 0.002 | 1.03619785e-05 | 0.002 / N / 0.000052 | True |

Only R160H0250-to-R320H0250 is the primary comparison. Both fixed requested windows and all exactly common stored windows are reported. Missing requested times cannot be replaced by other common times. The maximum-voltage row, maximum-surface-time row and signed component differences are stored together; component maxima at unrelated times must not be summed.

Snapshots preserve 0.005 s, 0.01 s, 0.04 s and each new primary voltage/surface peak, with full same-coordinate profiles. No convergence order is calculated and no R320 time-accuracy or global-convergence claim is made.

- Pointwise maxima are maxima over specified common spatial and temporal samples, not continuous-space/time bounds.
- t=0 is after CDI and consistent initialization.
- Both models retain the same early t<0.1 s cap 0.00025 s and later cap 0.1 s. Identical settings do not imply identical adaptive integration histories. Actual-step checks are a separate native-log audit.
- Exactly common stored times are an intersection, not the union of adaptive histories. Unmatched times are not compared or interpolated.
- At most this comparison establishes bounded sampled R160-to-R320 radial sensitivity. It does not establish R320 time accuracy, a true-solution error bound, unrestricted radial convergence or global convergence.
- The maxstepbdf constant slot is inactive in expr mode.
- Source/native audits establish physical invariants absent from the CSVs. No threshold or OCP adjustment and no rewriting of failed states.

Caps300R160H0250: analyzed; physical checks=True; 

Caps300R320H0250: analyzed; physical checks=True; 

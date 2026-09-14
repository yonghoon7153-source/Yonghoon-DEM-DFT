# R320 late-cap-A sampled comparison

One authorized new 300/R320 late-cap-A 5 s run against fixed existing R320 H0125. No COMSOL execution by this analyzer.

Exact Decimal requested-grid and all-exact-common-native-stored-time comparisons are separate. Native FE spatial evaluation at fixed 241-point electrode grids; no external spatial or temporal interpolation.

Value comparisons include both endpoints of each window. Thus t=1 appears in both adjacent value windows; this does not double-count native accepted intervals, which are audited separately.

| Time basis | Window(s) | Compared times | Max voltage difference(mV) | Time(s) | Max pointwise surface-x difference | Time / electrode / coordinate(m) | Within limits |
|---|---|---:|---:|---:|---:|---|---|
| requested_grid | 0.1–1 | 91 | 0.0020165373344 | 0.22 | 3.3690331476e-08 | 0.22 / N / 0.000052 | True |
| requested_grid | 1–5 | 81 | 0.0023442301413 | 1.7 | 3.8702635003e-08 | 1.7 / N / 0.000052 | True |
| requested_grid | 0–1 | 107 | 0.0020165373344 | 0.22 | 3.3690331476e-08 | 0.22 / N / 0.000052 | True |
| requested_grid | 0–5 | 187 | 0.0023442301413 | 1.7 | 3.8702635003e-08 | 1.7 / N / 0.000052 | True |
| all_exact_common_stored | 0.1–1 | 99 | 0.0020165373344 | 0.22 | 3.3690331476e-08 | 0.22 / N / 0.000052 | True |
| all_exact_common_stored | 1–5 | 81 | 0.0023442301413 | 1.7 | 3.8702635003e-08 | 1.7 / N / 0.000052 | True |
| all_exact_common_stored | 0–1 | 906 | 0.0020165373344 | 0.22 | 3.3690331476e-08 | 0.22 / N / 0.000052 | True |
| all_exact_common_stored | 0–5 | 986 | 0.0023442301413 | 1.7 | 3.8702635003e-08 | 1.7 / N / 0.000052 | True |

Component snapshots include all eight window V/x peak times plus 0.002, 0.1 and 1 s. Missing data or mandatory-check failure prevents a comparison pass. No rerun is initiated.

- Pointwise maxima are over the specified common space/time samples, not continuous-space/time error bounds.
- t=0 is after CDI and consistent initialization.
- The 1–5 s comparison carries earlier history from the changed 0.1–1 s cap. It does not isolate independent causal effects of the two late intervals.
- The user-authorized CPU parallelism change can affect floating-point roundoff/adaptive histories. Identical physics and Time/Variables settings apart from the cap do not imply bitwise one-factor isolation.
- Exactly common stored times are an intersection, not the union of adaptive histories. Unmatched times are explicitly excluded, never interpolated.
- At most sampled late-time-cap sensitivity; no true-error bound or unrestricted space/time convergence follows from pairwise agreement.
- The retained maxstepbdf constant slot is inactive in expr mode. Actual cap/step checks belong to a separate native-log audit.
- Electrolyte positivity is POSTPROCESSING_ONLY, not a StopCondition. Source/native audits establish physical invariants absent from CSVs.
- No OCP/threshold adjustment, rewriting of failed states, automatic rerun or additional simulation is performed.

Caps300R320H0125: analyzed; physical checks=True; 

Caps300R320LateCapA5s: analyzed; physical checks=True; 

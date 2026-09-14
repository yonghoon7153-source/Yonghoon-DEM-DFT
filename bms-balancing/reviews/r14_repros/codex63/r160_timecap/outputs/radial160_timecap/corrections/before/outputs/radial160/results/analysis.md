# One new R160 run: primary 80-to-160 and separate 40-to-80 reference

One authorized new 300/R160 H0500 5 s run versus fixed existing 300/R80 H0500. Existing 300/R40 H0500 is a separate trend reference. No COMSOL execution by this analyzer.

Exact Decimal requested-time selection; native finite-element spatial interpolation on fixed 241-point electrode grids; no external spatial or temporal interpolation.

| Comparison | Window | Max voltage difference (mV) | Time (s) | Max pointwise surface-x difference | Time / electrode / coordinate (m) | Within limits |
|---|---|---:|---:|---:|---|---|
| primary_radial_80_to_160 | 0–1 s | 1.248218114 | 0.01 | 2.091183902e-05 | 0.01 / N / 0.000052 | False |
| primary_radial_80_to_160 | 0–5 s | 1.248218114 | 0.01 | 2.091183902e-05 | 0.01 / N / 0.000052 | False |
| trend_reference_radial_40_to_80 | 0–1 s | 2.505981087 | 0.04 | 4.183542232e-05 | 0.04 / N / 0.000052 | False |
| trend_reference_radial_40_to_80 | 0–5 s | 2.505981087 | 0.04 | 4.183542232e-05 | 0.04 / N / 0.000052 | False |

Only the 80-to-160 pair is the new primary comparison. The 40-to-80 pair reuses historical references and is not a new run. Only complete requested windows can pass. The maximum-voltage row and its signed component differences are stored together in analysis.json; component maxima at unrelated times must not be summed.

Three-level snapshots contain the same-time 40/80/160 scalar values and full same-coordinate profiles at 0.04 s and each new primary voltage/surface peak. No convergence order is calculated.

- Pointwise maxima are maxima over specified common spatial and temporal samples, not continuous-space/time bounds.
- t=0 is after CDI and consistent initialization.
- Only t<0.1 s uses the tighter cap; later-time error is not independently controlled by this experiment. Actual step/binding checks are a separate native-log audit, not inferred from the configured expression.
- Identical requested times and same-cap controls do not imply identical adaptive internal steps. Pairwise agreement does not prove a true-solution error bound or unrestricted radial/time convergence.
- The maxstepbdf constant slot is inactive in expr mode.
- Source/native audits establish physical invariants absent from the CSVs. No threshold or OCP adjustment and no rewriting of failed states.

Caps300R160H0500: analyzed; physical checks=True; 

Caps300R40H0500: analyzed; physical checks=True; 

Caps300R80H0500: analyzed; physical checks=True; 

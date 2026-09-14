# Four fresh time-cap comparisons

Proposal A: only four explicitly mapped fresh 5 s jobs; primary comparisons never include old jobs; no COMSOL execution.

Exact Decimal requested-time selection; native finite-element spatial interpolation on fixed 241-point electrode grids; no external spatial or temporal interpolation.

| Comparison | Window | Max voltage difference (mV) | Time (s) | Max pointwise surface-x difference | Time / electrode / coordinate (m) | Within limits |
|---|---|---:|---:|---:|---|---|
| time_cap_at_R40 | 0–1 s | 0.0001926839399 | 0.06 | 2.19426633e-08 | 0.01 / P / 0.000121 | True |
| time_cap_at_R40 | 0–5 s | 0.0001926839399 | 0.06 | 2.19426633e-08 | 0.01 / P / 0.000121 | True |
| time_cap_at_R80 | 0–1 s | 0.001422421406 | 0.02 | 9.26174359e-08 | 0.005 / P / 0.000121 | True |
| time_cap_at_R80 | 0–5 s | 0.001422421406 | 0.02 | 9.26174359e-08 | 0.005 / P / 0.000121 | True |
| radial_at_H1000 | 0–1 s | 2.506696517 | 0.04 | 4.184745405e-05 | 0.04 / N / 0.000052 | False |
| radial_at_H1000 | 0–5 s | 2.506696517 | 0.04 | 4.184745405e-05 | 0.04 / N / 0.000052 | False |
| radial_at_H0500 | 0–1 s | 2.505981087 | 0.04 | 4.183542232e-05 | 0.04 / N / 0.000052 | False |
| radial_at_H0500 | 0–5 s | 2.505981087 | 0.04 | 4.183542232e-05 | 0.04 / N / 0.000052 | False |

Only complete requested windows can pass. The maximum-voltage row and its signed component differences are stored together in analysis.json; component maxima at unrelated times must not be summed.

- Pointwise maxima are maxima over specified common spatial and temporal samples, not continuous-space/time bounds.
- t=0 is after CDI and consistent initialization.
- Only t<0.1 s uses the tighter cap; later-time error is not independently controlled by this experiment. Actual step/binding checks are a separate native-log audit, not inferred from the configured expression.
- Identical requested times and same-cap controls do not imply identical adaptive internal steps. Pairwise agreement does not prove a true-solution error bound or unrestricted radial/time convergence.
- The maxstepbdf constant slot is inactive in expr mode.
- Source/native audits establish physical invariants absent from the CSVs. No threshold or OCP adjustment and no rewriting of failed states.

Caps300R40H1000: analyzed; physical checks=True; 

Caps300R40H0500: analyzed; physical checks=True; 

Caps300R80H1000: analyzed; physical checks=True; 

Caps300R80H0500: analyzed; physical checks=True; 

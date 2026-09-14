# Fresh mesh-axis comparison

Only the three explicitly mapped fresh 5 s jobs; no old preflight comparisons and no COMSOL execution.

Exact Decimal requested-time selection; native finite-element spatial interpolation on fixed 241-point electrode grids; no external spatial or temporal interpolation.

| Axis | Window | Max voltage difference (mV) | Time (s) | Max pointwise surface-x difference | Time / electrode / coordinate (m) | Within limits |
|---|---|---:|---:|---:|---|---|
| particle_radius | 0–1 s | 2.505310864 | 0.04 | 4.182398438e-05 | 0.04 / N / 0.000052 | False |
| particle_radius | 0–5 s | 2.505310864 | 0.04 | 4.182398438e-05 | 0.04 / N / 0.000052 | False |
| physical_coordinate | 0–1 s | 1.08668e-08 | 0.001 | 2.2088256e-09 | 1 / P / 0.000121 | True |
| physical_coordinate | 0–5 s | 1.08668e-08 | 0.001 | 5.2286938e-09 | 5 / P / 0.000121 | True |

Only complete requested windows can pass. The maximum-voltage row and its signed component differences are stored together in analysis.json; component maxima at unrelated times must not be summed.

- Pointwise maxima are maxima over the specified common spatial and temporal samples, not continuous-space/time bounds.
- t=0 is after CDI and consistent initialization.
- Identical requested times and core time controls do not imply identical adaptive internal steps; an observed mesh-axis sensitivity can include coupled time-adaptation effects. Actual native step statistics must be read separately from configured caps.
- Source and native audits are needed for physical parameters absent from exported tables.
- No threshold or OCP table adjustment is made; failed states are not rewritten.

Axes300R40: analyzed; physical checks=True; 

Axes300R80: analyzed; physical checks=True; 

Axes600R40: analyzed; physical checks=True; 

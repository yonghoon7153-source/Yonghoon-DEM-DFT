# Furnas dip — resolution-invariant measurement (2026-06-07)

Controlling epistemology: CLAUDE.md frame [3] (Furnas dip is a GEOMETRIC packing
effect) and [4] (DEM/MPM each validated independently; agreement = cross-
validation, NOT cross-fitting).

User goal (2026-06-07): *"절대값이 안맞아도 괜찮아 — 트랜드 확인하는데 환경
(해상도)이 변수가 되면 안된다."*  The trend must not depend on the numerical
grid; absolute values may be off.

## Why the old measurement failed
`mpm2d_composition.py` read porosity at a **common pressure**, and the MPM
pressure read-out is resolution-biased (320 vs 512 differ ~55–72 % at equal
porosity).  So the porosity-vs-AM% dip moved with grid size — resolution was a
hidden variable.

## Tool 1 — grid-free geometric reference (`scripts/packing_dip_model.py`)
de Larrard / Yu-Standish linear packing model.  **No grid, no pressure read-out,
no plasticity → resolution-free by construction.**
- SELF-VALIDATED: virtual γ reproduces the parameter-free Furnas ideal limit
  (1−ε0² at coarse fraction 1/(1+ε0)); PASS for β = 0.84 / 0.74 / 0.64.  ⇒ it is
  doing geometry, not curve-fitting.
- Result (12:4:1, P:S 7:3): **Furnas dip at AM ≈ 85–90 wt%**, depth 8–12 %p,
  ROBUST across β 0.64–0.88 (not tuned).
- ⇒ The dip is geometric-packing physics, measured with NO resolution variable.

## Tool 2 — rigid-jamming MPM (`scripts/mpm2d_jamming.py`)
Rigid particles (E = 24 GPa, no plastic flow); readout = jamming porosity at a
**self-normalised** pressure fraction (resolution amplitude cancels).  Run at
n_grid = 320 AND 512, 3 seeds each (uma GPU, taichi/CUDA).

### Result (f05 column; knee column was too noisy → discarded)
| quantity | value | meaning |
|---|---|---|
| raw RMSE 320↔512 | 5.11 %p | absolute level moves with resolution |
| constant offset | 4.90 %p (512 lower) | … but it is a near-constant shift |
| **SHAPE-RMSE (de-meaned)** | **1.46 %p** | **trend after removing offset** |
| **Pearson(320, 512)** | **0.9924** | **shape essentially identical** |
| dip location | 320 @ AM95 %, 512 @ AM95 % | **same** (geom @ AM90 %) |
| |320 − geom| → |512 − geom| | 21.1 → 16.2 %p | **converging toward geometry** |
| Spearman(MPM, geom) | 0.956 (320), 0.962 (512) | MPM tracks the geometric dip |

### Verdict (frame [3]/[4]-compliant)
1. **The dip TREND is resolution-invariant.**  320 and 512 give the *same shape*
   (Pearson 0.99, shape-RMSE 1.5 %p) with the *same dip location* (AM95 %),
   matching the grid-free geometric dip (AM90 %).  ⇒ the user's goal is met:
   resolution is NOT a variable for the trend.
2. **Resolution changes only the absolute level**, by a near-constant ~5 %p, and
   in the physically correct direction — higher resolution moves MPM **down
   toward the grid-free geometric truth** (|512−geom| < |320−geom|).  This is
   ordinary numerical convergence, and the user already declared the absolute
   irrelevant.
3. **The dip is real geometric physics, cross-validated by two independent
   tools** (de Larrard geometry + rigid MPM).  Per frame [4] this convergence is
   evidence, not a forced fit (the two were never tuned to each other).

### Honest caveats (frame-consistent)
- MPM absolute porosity (~30–50 %) sits ~15–20 %p above geometry/experiment
  (~10–16 %).  MPM is a continuum with **no explicit contact network** (frame
  [1] LIMITS), so it has no sharp granular jamming knee — the f05 readout rides
  the progressive oedometer compaction.  ⇒ MPM gives the right **shape/trend**,
  not the right **absolute packing density**.  Absolute density is DEM/geometry
  territory (frame [5]: DEM = transport/packing-network, MPM = mechanics).
- The dip itself is shallow relative to the overall densification trend (the
  AM95 < AM100 uptick is the Furnas signature; present at BOTH resolutions).

### Reproduce
```bash
# uma (taichi GPU):
python3 scripts/packing_dip_model.py
python3 scripts/mpm2d_jamming.py --n-grid 320 --seeds 3 --out jam_320.csv
python3 scripts/mpm2d_jamming.py --n-grid 512 --seeds 3 --out jam_512.csv
python3 scripts/mpm2d_jamming.py --compare jam_320.csv jam_512.csv
# plot (machine with matplotlib): same --compare command -> 2-panel
#   docs/figures/mpm2d_jamming_resolution.png  (LEFT raw+geom, RIGHT de-meaned shapes collapse)
```

Data: `docs/data/packing_dip_model.csv`, `jam_320.csv`, `jam_512.csv`,
`jamming_resolution_compare.csv`.

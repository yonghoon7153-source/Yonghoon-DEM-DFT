# 3D DEM composite over-shielding — exhaustive lever screen (2026-06-15)

## Finding
The resolved-grain 3D elasto-plastic DEM (`scripts/dem3d_plastic.py`) reproduces
pure-SE compaction (Minnmann 10% @ 300 MPa + multi-pressure Heckel) but the
COMPOSITE (CAM + SSE, 12:4:1) equilibrates at **34–41 % porosity** vs the measured
**9–19 %** (EA26-3669 FIB-SEM: 9.43 % @ 50 vol% CAM = 75 wt%, 18.93 % @ 60 vol% = 82 wt%).
Adding even ~8 vol% AM jumps porosity 9 → 39 %.

## Mechanism
Measured at the bulk axial virial σzz = ΣF_n·d·n_z²/V (the correct bulk stress,
boundary-free).  The rigid AM (real E = 140 GPa) carry the axial stress through
vertical force chains, so the servo stops when the AM bear 300 MPa while the soft
SE is still loose — the SE never densifies.  rigid (cap OFF) ≈ plastic (cap ON) in
the composite (both ~36 %), confirming the SE plasticity cannot help: the contact
cap flattens SE–SE contacts but cannot make the (rigid-sphere) SE FLOW into the
large AM voids.

## Exhaustive lever screen — ALL fail to reach the measured 9–19 %
| lever | sweep | result |
|---|---|---|
| AM modulus | e_am 140 → 40 → 12 → 4 | 36 → 37 → 38 → 32 %  (no real change; e_am=4 sphere/vox diverge = soft-AM over-overlap artifact) |
| friction | mu 0.3 → 0.0 | rigid 37.6 → 37.9, plastic 36.1 → 35.8  (no change) |
| cohesion (LJ-analog) | coh 0 → 1 → 2 → 4 → 8 GPa | 37.4 → 35.9 → **32.6** → 33.0 → 34.7  (only −5 %p, NON-monotonic: strong cohesion clumps the SE → inter-cluster voids) |

## Verdict — fundamental, not tunable
The composite over-porosity is the **rigid-sphere void-filling limit**.  Even the
IDEAL rigid packing (de Larrard geometric, ~20 % for 12:4:1) is already 2× the
measured plastic 9–19 %; reaching the measured value needs the SE to FLOW into the
AM voids (continuum plastic shape change), which a rigid-sphere DEM cannot do at any
calibration (AM stiffness / friction / cohesion all screened).  This is the
DEM↔MPM division (CLAUDE.md frame [5]) made quantitative:

  * DEM (this tool)  = pure-SE mechanics (Minnmann + Heckel ✓) + the contact NETWORK
    for transport (σ_ionic / σ_e / σ_thermal via Kirchhoff).  DOES NOT own composite
    absolute porosity.
  * MPM             = plastic shape-flow / morphology / void-fill.
  * de Larrard / experiment = composite porosity + the Furnas dip.

Also note: the equilibrated plastic porosity-vs-AM curve is MONOTONIC (no Furnas
dip — the earlier "dip" was a servo settling artifact), consistent with the
champion MPM.  → the dip is NOT a resolved-grain-plastic phenomenon.

## Do NOT re-try
AM softening, friction, and cohesion are all screened and fail.  The composite
absolute porosity is owned by de Larrard / MPM / experiment, NOT this DEM.  Use the
DEM for pure-SE + the transport network (its validated lane).

# DPC volumetric cap × resolved-grain MPM — cross-check (FINDING)

**Verdict: the Drucker-Prager/Cam-Clay VOLUMETRIC cap does NOT fit the
resolved-grain MPM.  It models unphysical particle shrinkage for the
incompressible SE solid, so it makes the bed compact MORE (collapse), not less.
The cap belongs in the HOMOGENIZED REV (`scripts/cap_compaction_heckel.py`).
For the resolved grain, the softened-E von Mises champion is the right particle
model, and the softening is FUNDAMENTAL (it lumps the granular jamming the
continuum cannot capture per-particle).**

This is the empirical confirmation of the long-standing CLAUDE.md note
*"cap doesn't fit resolved-grain: void-fill is isochoric shape-flow."*

## Why (physics)

- A volumetric cap lets each material point reduce its VOLUME plastically
  (particle shrinkage).  SE (Li₆PS₅Cl) is a solid with bulk modulus ≈ 24 GPa;
  at 300 MPa ≪ 24 GPa the particle volume change is ~1 %.  **SE particles do
  not densify internally.**
- Real powder densification = **rearrangement + isochoric shape change**
  (void-filling), not particle volume reduction.
- So turning the cap on admits unphysical shrinkage → the champion's natural
  isochoric resistance is removed → over-compaction / collapse.

## Data (pure-SE Heckel, n_grid=320, servo wall, cap_pb0=0.05, cap_fric=0.5)

DPC volumetric-cap model `--model dpc`, porosity % at 100 / 300 / 600 MPa:

| E_SE (GPa) | cap_avpmax | 100 MPa | 300 MPa | 600 MPa |
|-----------:|-----------:|--------:|--------:|--------:|
| 24 (real)  | 0.5        | 34.9    | 16.2    | 2.4     |
| 24         | 0.7        | 30.3    | 4.9     | 0.9     |
| 24         | 0.9        | 26.0    | 0.9     | 0.8     |
| 1.53 (soft)| 0.5        | 19.8    | 0.8     | 0.8     |
| 1.53       | 0.7        | 14.1    | 0.8     | 0.8     |
| 1.53       | 0.9        | 7.8     | 0.8     | 0.8     |

Reference points:
- **champion (no cap, E=1.53)**: pure-SE 300 MPa → **11 %** (dbg320).  Adding
  the cap drives 300 MPa → 0.8 % — i.e. the cap makes it WORSE (11 → 0.8).
- **homogenized DPC** (`cap_compaction_heckel.py`, REV, real E=24): clean
  Heckel **100/300/600 → 13.9 / 10.0 / 8.3 %** (φ0=0.5, φ_min=0.03, b=2.5).
  This is where the cap is physically correct (point = powder-with-voids,
  volumetric compaction = void reduction).
- **resolved-grain champion composite, SE-rich small-SE**: over-flows to
  ~0.9 % (the matcher result that started this) — the missing-jamming continuum
  limit, bracketed by rigid DEM (~21 %).

Two observations that pin the verdict:
1. **E=24 under-densifies at low P even with the cap** (100 MPa → 26-35 %, vs
   Heckel ~14 %): the continuum cap captures particle compaction but not the
   granular rearrangement the softening lumps in → real E too stiff.
2. **E=1.53 + cap collapses** (300 → 0.8 % vs champion's 11 %): the cap's
   volumetric plasticity over-compacts the soft particles.
Neither E baseline matches Heckel with the cap → the cap is the wrong tool here.

## Division of labour (frame [5], confirmed)

| quantity | tool |
|---|---|
| porosity **trend** (vs composition / SE size) | resolved-grain champion (softened-E, isochoric von Mises) |
| realistic **absolute** porosity (Heckel) | homogenized DPC `cap_compaction_heckel.py` |
| transport σ | DEM (Kirchhoff contact network) |

## Consequences

- **Softening (E_eff=1.53) is irreducible for the resolved grain** — it is the
  proxy for the contact-network jamming the continuum lacks, not a removable
  workaround.  "real E + cap = more correct physics" is NOT realised here.
- **NACC has the same volumetric-hardening flaw** → not worth building for the
  resolved grain (would shrink particles the same way).
- The small-SE trend is reported **bracketed**: [rigid DEM upper, plastic-
  continuum lower]; the gap quantifies the missing jamming (frame [1] LIMIT).
- The physically-correct way to stop the resolved-grain over-flow WITHOUT
  particle shrinkage is a **density-dependent deviatoric (shear) yield** that
  diverges as local packing → φ_max (isochoric jamming) — pursued separately as
  `--model jam`.

Cross-check tooling: `scripts/mpm_dem_match.py --model dpc --heckel`
(servo wall, divergent cap).  Data: `docs/data/mpm_dpc_heckel_sweep.csv`.

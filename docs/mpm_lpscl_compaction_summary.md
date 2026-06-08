# MPM LPSCl 2D compaction — consolidated summary (2026-06-08)

Paper-oriented synthesis of the MPM compaction study.  Working logs:
`CLAUDE.md` ("MPM cap/champion" timelog) + `docs/mpm_dip_resolution_invariance.md`.
Controlling epistemology: CLAUDE.md frame [1]–[5] (DEM↔MPM complementary).

## 1. Question
Can a 2D MPM faithfully depict **real LPSCl powder compaction** — the
plastic grain deformation, void-filling, morphology, porosity, and the
Furnas packing dip — and is the dip a **resolution-invariant** trend?

## 2. SE mechanical model — 3 layers (not one E_eff)
| layer | E | σ_y | role |
|---|---|---|---|
| real bulk | 24 GPa | 0.05–0.30 GPa | LPSCl single-crystal literature |
| DEM effective | 1.35 GPa | (Heckel σ_y_eff≈46 MPa) | 18× softened; transport network |
| **MPM champion** | **1.53 GPa** | **0.15 GPa** | softened-J2; this study |

The 18× softening (24→1.53) is the **physical proxy** for granular
rearrangement / GB-sliding / micro-fracture that a continuum MPM cannot
represent explicitly (frame [1] LIMITS, frame [2]).  Real E=24 in MPM
**under-densifies** (33–38 %, too stiff → builds pressure before flowing);
the softening is required to densify realistically and is triple cross-
validated (pure-SE Cronau overlap, plastic-vs-rigid, independent MPM).

## 3. Two compaction lines
- **(가) resolved-grain MPM** — `scripts/mpm2d_PS_pressure.py` (champion
  1.53/0.15, work-hardening, von-Mises J2, servo wall).  Keeps the Furnas
  dip; gives morphology + porosity.  ★ CHOSEN.
- **(나) homogenized REV cap** — `scripts/cap_compaction_heckel.py` (real
  E=24, Drucker-Prager cap, p_c→∞ at φ_min).  Clean multi-pressure Heckel
  (100→13.9 / 300→10.0 / 600→8.3 %, Minnmann anchor) but NO dip (0D).
  Companion reference for the target porosity curve.

## 4. Champion validation (가)
- **Morphology** — `viszoom_E1.53_sy0.15.png`: core-preserved + boundary-
  flattening = **matches SEM**.
- **Pure-SE porosity** — `dbg320.log`: AM0 @ 300 MPa = **11.4 %** ≈ Minnmann
  300→10 %.  (450/600 MPa read 0 = "pressure-not-reached" sentinels for soft
  SE, not real 0 %.)
- ⇒ champion reproduces BOTH the morphology and the experimental porosity
  anchor.

## 5. Furnas dip — RIGID (geometric) is resolution-INVARIANT
Two independent tools, `scripts/packing_dip_model.py` (grid-free de Larrard,
self-validated to the parameter-free Furnas ideal) and
`scripts/mpm2d_jamming.py` (rigid E=24, self-normalised readout):

| P:S | SHAPE-RMSE 320↔512 | Pearson | dip @320 | dip @512 | geom dip |
|-----|--------------------|---------|----------|----------|----------|
| 7:3 | 1.46 %p | 0.992 | AM95 % | AM95 % | AM90 % |
| 5:5 | 1.06 %p | 0.998 | AM95 % | AM95 % | AM90 % |
| 3:7 | 0.91 %p | 0.999 | AM95 % | AM95 % | AM85 % |

⇒ the **geometric packing dip is resolution-invariant** (shape identical,
dip location pinned), robust across composition; resolution shifts only a
~5 %p constant offset that **converges toward the grid-free geometry**.
Cross-validated by an independent rigid-jamming MPM run (`mpm2d_PS_rcp.npy`,
dip @ AM 70–80 %).

## 6. Furnas dip — PLASTIC (champion) attenuates it AND its invariance
`mpm2d_jamming.py --e-se 1.53 --yield-se 0.15`, f05 (early/geometric) vs
f50 (deep/plastic), 320 vs 512:

| readout | Pearson(320,512) | dip 320 / 512 | absolute porosity |
|---|---|---|---|
| rigid (geometry) | 0.99 | 95 / 95 | 30–50 % (too high) |
| plastic f05 (early) | 0.89 | 85 / 60 | 27–43 % |
| plastic f50 (deep) | 0.80 | 85 / 70 | **9–16 %** (512) ≈ exp |

Findings:
1. **Plasticity makes the porosity REALISTIC** — f50 512 = 9–16 % (AM90
   10.6 %) ≈ Minnmann/experiment, vs the rigid 30–50 %.
2. **Plasticity ATTENUATES the dip** (frame [3] "plastic flow partially
   erases the packing dip") AND **erodes its resolution-invariance**
   (Pearson 0.99 → 0.80); deeper compaction (f50) is less invariant than
   early (f05).  New finding: the clean resolution-invariant dip is a
   GEOMETRIC property; the plastic flow of the small (resolution-sensitive)
   SE grains both fills the dip and makes it grid-dependent.

## 7. Conclusion (frame [5] division of labour)
- **MPM champion (가)** = real LPSCl **mechanics / morphology / porosity**
  (validated against SEM + Minnmann); the softening is the physical proxy
  for the granular mechanisms a continuum cannot resolve.
- **geometry / rigid** = the **clean resolution-invariant dip trend**
  (de Larrard + rigid-jamming MPM, Pearson 0.99).
- the two are complementary, not competing: MPM shows the real plastic
  behaviour (with an attenuated, grid-sensitive dip), geometry shows the
  underlying packing dip cleanly.  Neither alone is the whole picture —
  exactly frame [5].

## 8. Open / next
- ① morphology @ 512 — sharpest 2D depiction (qualitative figure).
- plastic-dip @ 768 — does the plastic dip's resolution-sensitivity
  converge with grid (expected: better-resolved SE → more invariant)?
- resolved-grain volumetric cap (real E=24) — likely confirms the softening
  is necessary (MPM continuum lacks the granular mechanism); a negative
  result is itself a quantified MPM limit (frame [4]).

Figure: `scripts/plot_mpm_compaction_summary.py` →
`docs/figures/mpm_compaction_summary.png`.

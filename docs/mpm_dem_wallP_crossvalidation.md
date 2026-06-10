# DEM ↔ MPM per-case cross-validation @ 512 — wallP boundary-load readout (2026-06-10)

Resolves the long-standing **"PER-CASE 512 matcher PENDING"** item (CLAUDE.md
MPM section): the true-plastic champion MPM (E_SE=1.53 GPa, σ_y=0.15 GPa, AM
rigid) compared against the 132-case DEM corpus at the real 12:4:1 sizes,
n_grid=512, 3 seeds.  Tool: `scripts/mpm_dem_match.py --readout wallP`; analysis
`scripts/analyze_mpm_dem_match.py`.  **This is a frame [4] comparison — DEM and
MPM are each calibrated to EXPERIMENT independently, never to each other.**

## 1. The readout problem (why 512 needed a new readout)

The matcher servoed a wall to a target pressure read as `mean(prs)` — the
**volume average** of the per-particle stress.  That average is **resolution-
biased**: at 512 the well-resolved soft SE dilutes the mean, so the bed must
over-compress before the mean reaches 300 MPa.  Pure-SE collapsed:

| readout (pure-SE @ 300 MPa) | 320 | 512 | nature |
|---|---|---|---|
| `mean(prs)` (absP) | 7.2% | **0.8%** | **9× collapse** — volume-average artifact |
| **wallP** (boundary load) | 23.5% | **12.7%** | force balance → 512 ≈ Minnmann ~10% |
| f50 (self-normalised) | 25.9% | 22.1% | trend only, too loose (~22%) |

**wallP** = the wall **reaction stress** `Σ grid_m·(v+wall_vf)/(n_sub·dt·WIDTH)`
= boundary force / area.  By force balance this ≈ the constitutive stress (GPa)
with dx / n_sub / ρ cancelling → **resolution-invariant AND the TRUE
experimental boundary condition** (press the powder AT 300 MPa), unlike the
volume-average mean.  Pure-SE Heckel @ 512: 100/300/600 MPa → 54.6 / 12.7 /
5.1 %.  (The Heckel *shape* is too steep — resolved-grain MPM cannot reproduce
the experimental Heckel, already triple-confirmed; the matcher reads only the
single 300-MPa point, where wallP@512 ≈ experiment.)

NOTE the 320→512 wallP shift (23.5→12.7) is NOT the absP artifact — it is the
genuine small-SE plastic-flow under-resolution that **converges** with grid
(mpm2d_jamming 768 convergence).  512 is converged-enough (≈ experiment); 320
under-resolves the small SE and reads high.

## 2. Servo robustness — the force-chain divergence is GENUINE, not a bug

A 10-case sanity exposed two failures on big rigid-AM + soft-SE (rSE=0.5):
AM-rich froze at the initial ~56% porosity; SE-rich over-compacted (5.9±3.0%).
Two fixes were tried:

- **median/window sustained-stop — REJECTED.** It rejects *real* load
  fluctuations as transients, over-compressing every case and **inverting the
  good rSE=1.0 band** (Δ −2~−3 → −9, Pearson 0.35 → −0.22).  Wrong tool.
- **arm-after-compaction guard — KEPT.** Disarm the instantaneous stop until
  the bed actually compacts (por ≤ por0−2), so a first-contact transient can't
  freeze the wall early; normal cases (compact well past 2%p before pr) are
  unchanged.

The arm-guard left the big-AM rSE=0.5 cases **byte-identical** to the original
instantaneous stop (51.8/56.4%).  **That is the decisive diagnostic: arming
removes transients; it changed nothing → the 56% is NOT a servo artifact but
the MPM continuum's genuine answer** — big rigid AM (R≈0.072, ~13 blobs) forms
**force chains** that bear 300 MPa at high porosity without rearranging, while
DEM rearranges + SE-void-fills to 16–24%.  Porosity JUMPS with AM size in the
MPM (small AM rSE=1.0 → 14%; big AM rSE=0.5 → 56%); DEM does not.  **Genuine
continuum-vs-discrete divergence (frame [4]), not a readout bug.**  → servo
work is DONE; the readout (wallP instant-stop + arm-guard) is correct.

## 3. Full 132-case result (wallP / 512 / 3 seeds)

Overall 1:1 parity R² = −4.4, mean|Δ| = 7.8%p, Pearson = 0.49.  The single R²
is **misleading** (dominated by the force-chain corner); the per-r_SE band
decomposition is the real picture:

| band | n | meanΔ (bias) | mean\|Δ\| | Pearson | verdict |
|---|---|---|---|---|---|
| **rSE≈1.0** | 5 | **−0.0** | **1.5** | **+0.964** | ✅ continuum valid — zero bias, perfect trend |
| rSE≥1.5 | 15 | +5.1 | 5.1 | +0.774 | +5 offset, tracks DEM trend (big-SE) |
| rSE≤0.5 | 112 | +5.3 | 8.5 | +0.467 | bulk; force-chain outliers scatter ρ |

**Force-chain outliers: 22 of 112 rSE≤0.5 cases**, ALL small-SE (rSE=0.5, one
rSE=0.25) AND AM-rich (AM_wt 80–92) — the big-AM / small-SE corner, MPM 31–46%
vs DEM 16–27% (Δ +15~+27).  Removing them, the rSE≤0.5 bulk bias drops
**+5.3 → +1.5%p** (n=90).  The ~+5 systematic offset elsewhere = pure-SE
512 anchor (12.7 vs exp 10, +2.7) + 512 under-resolution (768 would shave it).

## 4. ★ Furnas dip co-locates — the headline cross-validation

porosity vs AM_wt (rSE≤0.5), DEM | MPM medians:

| AM_wt | DEM | MPM | note |
|---|---|---|---|
| <65 (SE-rich) | 19.7 | 4.9 | MPM over-compacts (extreme, n=3) |
| **72–78** | **13.4** | **12.7** | ★ **dip minimum — co-located, depth within 0.7%p** |
| 78–83 | 16.3 | 17.2 | ✓ agree |
| 83–88 | 19.0 | 22.8* | *inflated by force-chain cases |
| 88–95 | 22.8 | 25.4* | *force-chain |

**Both the DEM (elastic-softened, contact network) and the independent
true-plastic MPM (continuum) put the Furnas dip minimum at AM 72–78 wt% with
nearly identical depth (13.4 vs 12.7 %), rising on both flanks.**  The dip
minimum is BELOW the force-chain onset (AM≈80), so it is FC-free and clean.
→ the dip is a **real geometric-packing effect**, cross-validated by two
independent tools (frame [3]/[4]) — not an artifact of either model.

Size slice (AM 78–86): DEM is ~flat in r_SE (16.7/17.1/17.2); MPM 17.8/16.0/
22.1 adds the big-SE (+rSE≥1.5) offset.  The AM62↔AM82 size-crossover is not
captured by this single composition slice (DEM flat here) — pending a dedicated
AM62-vs-AM82 contrast.

## 5. Conclusion (frame [4] / [5])

**In the production-core composition (AM 72–83, the dip region) the
independently-calibrated DEM and champion MPM agree to within +1.5%p AND
reproduce the Furnas dip at the same composition and depth** — strong
cross-validation.  The MPM diverges only at the extremes, both quantified
continuum limits:
- **AM-rich / small-SE (22 cases): rigid-AM force chains** bear the load at
  high porosity (MPM over-predicts 2–3×) — the continuum lacks the discrete
  rearrangement DEM has.  DEM is right here; the matcher quantifies WHERE the
  continuum fails.
- **extreme SE-rich (AM<65): servo over-compaction** (few cases).

DEM = transport + discrete contact network; MPM champion = morphology + the
dip TREND.  Their agreement in the core (and the dip co-location) quantifies
model trust; their divergence at the size/composition extremes is information,
not failure.

Data: `docs/data/mpm_dem_match.csv` (132 cases).  Re-derive bands/dip/FC with
`python3 scripts/analyze_mpm_dem_match.py`.

# DEM post-compaction PERTURBATION LAYER (`scripts/dem_perturbation.py`)

The general "역산" layer the user asked for: take the REAL DEM particle geometry
(positions + radii from `atoms.csv`/`contacts.csv`) and adjust it by an
**independent physics driver** to represent states the single frozen 300-MPa DEM
snapshot cannot.  One engine, several drivers — reusable standalone AND after the
Phase-3 predictor / for inverse design.

## Engine (shared, verified)
A driver returns, per contact, the change in centre-to-centre **separation**
(overlap change) and, per atom, the new **radius**.  From those the layer computes
the **confined-uniaxial** macroscopic strain ε_zz — the DEM box is a periodic x,y
RVE with a free z platen (`boundary p p f`), so lateral strain ≈ 0 and all recovery
goes into z — by best fit `ε_zz·b_z·n_z = Δseparation` over the contact network.
Then porosity/thickness update (solid conserved, reuses the case's *validated*
loaded porosity: `ε_unloaded = 1 − (1−ε_loaded)/(1+ε_zz)`), contacts that open are
counted, and (`--write-csv`) perturbed `atoms.csv`+`contacts.csv` are written so the
EXISTING `network_conductivity.py` recomputes the perturbed σ (transport not
reinvented).  Self-test (`--selftest`) verifies ε_zz vs analytic on synthetic
chains, the plastic-depth branch, orthogonal contacts, and breathing.

## Driver A — springback (hooke/hysteresis ELASTIC UNLOAD) — LIVE
★ Read straight off `input_real_14.liggghts` fixes m1–m8 (NOT a generic COR²):
- The unload stiffness is **`coefficientMaxElasticStiffness` (m6 = k₂/k₁)**, NOT
  `coefficientRestitution` (m3 = viscous damping, which does **not** enter a
  quasi-static unload).  Linear-hysteretic recovery to F=0:
  **recovered overlap Δδ = δ·(k₁/k₂) = δ/(k₂/k₁)**, residual (plastic) = δ·(1−k₁/k₂).
- **Pair-dependent** (m6): AM-AM k₂/k₁=1.5 → recover **67 %**; AM-SE=3.0 → 33 %;
  SE-SE=5.0 → **20 %**.  ⇒ the SE matrix (stiff unload + strong adhesion m7 kc=1e6
  cold-weld) barely springs back and **stays compacted**, while the AM recover more
  and lose the most contact area (transport signature: σ_e/AM-AM weakens on unload,
  σ_ionic/SE-SE robust).
- **m8 `coefficientPlasticityDepth` φf**: a contact whose loaded overlap is below the
  plastic onset (δ/r_eff < φf) never went plastic → recovers **fully** (Δδ=δ).
- **m7 `coefficientAdhesionStiffness` kc**: reported for context; it makes this
  springback an **UPPER bound** (real ≤ this, SE-SE most suppressed).  Not applied as
  a fudge factor.
- Frame[4]-consistent: it is the DEM's OWN contact model run in reverse, using the
  DEM's OWN parameters — not an arbitrary expansion.  Extra real springback beyond
  the rigid-sphere contacts (SE viscoelastic / binder, Hong 2026) is a separate,
  quantified gap.

Example (synthetic AM-SE+SE-SE bed @ 15.6 %): ε_zz=1.4 % → porosity **15.6→16.8 %
(+1.2 %p)**, thickness 113.4→115.0 µm, contact area ×0.73 mean — a realistic
electrode springback magnitude.

## Driver B — breathing (chemo-mechanical cycling) — STUB wired to the engine
`r → r·(1+ΔV/3)` from the NCM SOC-volume curve (independent physics: charge=shrink
≈ −2..−6 %; AM_P single-crystal vs AM_S poly differ).  Overlaps shift, contacts with
δ_new<0 are **LOST** → σ_ionic/σ_e drop → cycle/SOC degradation.  The engine already
handles the resulting strain + contact loss (self-test [5]); Phase-B = supply the
SOC-volume curve as `--dvol` and re-solve σ on the perturbed contacts.

## Driver C — dilate (VGCF rod-network prop-open, Philipse rod jamming) — LIVE
The packing half of the additive porosity effect (frame[5] DEM domain) that
`--fibre-stiff` (frozen AM) could not reach — the VGCF "역산" the user asked for.
- **φ_jam = C_rod·D/L** (Philipse 1996 random-contact rod jamming, C_rod=5.4).  VGCF
  L/D≈67 → **φ_jam≈8.1 vol% ≈ 4 wt%** → low-wt% carbon has an OUTSIZED structural
  effect (explains Cho's small-wt% prop).  **NON-CIRCULAR: onset from fibre geometry,
  never a target porosity.**
- jamming ratio `x = φ_vgcf,bed/φ_jam`; prop gate `p = 1−exp(−x)`; bed expansion
  `ε_zz = p·φ_vgcf,bed·A`.  A = excluded-volume amplification, **BRACKETED**
  [1 (rods add own volume as height, conservative) … 1/φ_jam (full exclusion, capped
  at loose 0.40)].  The exact A = AM/SE fillability of the open rod mesh → pinned only
  by DEM co-compaction; reported as a bracket, A=1 as the nominal.

**Result — VGCF wt% sweep on the input_6mAh_real_4 baseline (ε₀=14.28 %):**

| VGCF | x (jam ratio) | volume-fill | dilate nominal (A=1) | bracket | no-additive |
|---|---|---|---|---|---|
| 0.5 wt% | 0.11 | 13.4 % | 13.5 % | [13.5, 14.4] | 14.3 % |
| 1 wt%   | 0.22 | 12.5 % | 12.8 % | [12.8, 16.1] | 14.3 % |
| 2 wt%   | 0.44 | 10.7 % | 11.8 % | [11.8, 22.7] | 14.3 % |
| 4 wt%   | 0.85 | 7.4 %  | 10.9 % | [10.9, 37.8] | 14.3 % |

- **Direction ✓**: dilate lifts porosity ABOVE volume-fill at every wt% (the prop), and
  the lift GROWS with wt% (x→jamming).  x reaches 0.85 at 4 wt% = right at the rod-
  jamming onset (jams at x=1 ≈ 4.7 wt%).
- **vs Cho (2 wt% → +1 %p, i.e. 14.3→15.3 %)**: the 2 wt% bracket [11.8, 22.7]
  CONTAINS 15.3 (Cho sits at A≈1.5–2).  So the model brackets Cho and matches its
  direction, non-circularly — but the nominal A=1 is conservative (below no-additive).
- **Honest**: the jamming ONSET + DIRECTION are non-circular (Philipse geometry); the
  exact porosity WITHIN the bracket = fillability = DEM co-compaction (VGCF rods in
  LIGGGHTS) pins it.  Combined with `--fibre-stiff` (+0.75 %p, direction+mechanism,
  MPM) this is the complete honest VGCF picture: MPM owns direction+mechanism, dilate
  gives the packing onset+bracket, DEM pins the single magnitude.

Usage: `python3 scripts/dem_perturbation.py --case <cid> --driver dilate --vgcf-vol-pct 8.06`

## Driver D — inverse-design (Phase-4/5) — same engine
Solve for the radius/position change that hits a predictor **target** (graded-z
electrodes, target-porosity synth).

## Rules (all drivers)
- **Non-circular**: every driver's magnitude comes from INDEPENDENT physics (m6/m7/m8,
  NCM SOC-volume, rod L/D) — never tuned to a target porosity.
- **Small-perturbation**: the position update is a first-order affine z-stretch; large
  rearrangements (overlaps opening a full diameter) need a real DEM re-run.

## Usage
```
python3 scripts/dem_perturbation.py --selftest
python3 scripts/dem_perturbation.py --case webapp/results/<cid> --driver springback
python3 scripts/dem_perturbation.py --case <cid> --driver springback --write-csv <out>
   # then rerun scripts/network_conductivity.py in <out> for the unloaded σ
python3 scripts/dem_perturbation.py --case <cid> --driver breathing --dvol "1:-0.04,2:-0.03,3:0"
```

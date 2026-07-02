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

## Driver C/D — dilate (VGCF rod-jamming, Philipse) / inverse-design
Same engine: a driver that expands by the rod-network jamming excluded volume
(φ·L/D≈5.4), or that solves for the radius/position change hitting a predictor
**target** (Phase-4/5 inverse design, graded-z electrodes).

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

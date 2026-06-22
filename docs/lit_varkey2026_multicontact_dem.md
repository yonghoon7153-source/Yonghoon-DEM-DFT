# Varkey 2026 (Adv. Powder Tech. 37, 105338) — multi-contact elasto-plastic DEM

**Citation:** C.A. Varkey, K. Giannis, S. Melzig, C. Schilde, S. Zellmer, "DEM simulation of
solid-electrolyte separator and cathode densification using a stress-based multi-contact
elasto-plastic model", Advanced Powder Technology 37 (2026) 105338 (open access CC-BY,
DEM10 special issue).  Fraunhofer IST + TU Braunschweig, HELENA project (halide SSBs).

**Material:** Li₃YBrCl₆ HALIDE SE (NOT our LPSCl Li₆PS₅Cl sulfide) + NMC-811 + SBR binder + CB.

DB companion: `docs/data/densification_porosity_db.csv` (their P-vs-porosity points for our
porosity-relation fit).

---

## ★ Verdict — does it REALLY describe plastic deformation?  NO (only CONTACT plasticity, not particle shape)

This is **still rigid-sphere DEM**.  The "elasto-plastic" is entirely at the **contact**
(the force–displacement law), **not the particle**.  Particles stay perfect spheres and
**never change shape**.  The paper says so explicitly (p.12):

> "Even though the halide solid electrolyte particles are irregular in shape, … a compromise
> on the choice of particle shape is made.  A new set of study employing more realistic
> particle shapes can be done in future."

⇒ "plastic deformation of the particle **STRUCTURE**" (the bed densifies) ✓  ≠
  "plastic deformation of the particle **SHAPE**" (morphology) ✗.  The overlap δ is a
  geometric **proxy** for plasticity, not real material flow.

---

## ★ How the elasto-plastic model is applied — the equations

### 1. Thornton–Ning normal contact (§2.2) — the per-contact elasto-plastic law
Effective modulus / radius (eq 3):
```
1/E* = (1−ν_i²)/E_i + (1−ν_j²)/E_j      1/R* = 1/r_i + 1/r_j
```
**Elastic (Hertz) regime**, while overlap δ < δ_y (eq 2):
```
F_el = (4/3)·E*·√(R*·δ³)
```
Contact radius (eq 4):  `a = ( 3·F·R* / (4·E*) )^(1/3)`.
**Yield onset** at critical yield pressure p_y → critical force/overlap (eq 5):
```
f_y = (1/6)·(R*/E*)²·(π·p_y)³        δ_y = (1/4)·(R*/E*²)·(π·p_y)²
```
**Plastic regime**, δ ≥ δ_y (eq 6) — note it goes **LINEAR** in overlap after yield:
```
F_el-pl = f_y + π·p_y·R*·(δ − δ_y)
```
**Unloading** with a flatter effective plastic radius R_p* and residual overlap δ_R (eq 7):
```
F_unloading = (4/3)·E*·√( R_p*·(δ − δ_R) )      → permanent deformation + energy dissipation
```
Tangential, Coulomb-coupled (eq 8):  `F_tangential = −μ·F_n·(s_t/|s_t|)`.
Calibrated **yield ratio = 0.0103** (plasticity starts at ~1.03 % overlap).

### 2. Stress-based multi-contact coupling (§2.3, Giannis [24]) — the NOVELTY
A particle's Poisson lateral expansion pushes into its OTHER contacts (confinement) — a
multi-body effect that classical **pairwise** DEM ignores.  Per-particle stress tensor from
the dyadic of branch vector lⁿ and contact force fⁿ over all NP contacts / particle volume Vᵖ
(eq 9):
```
σᵖ = (1/Vᵖ)·Σ_{n=1..NP} lⁿ ⊗ fⁿ
```
Multi-contact pressure from the trace (eq 10) and the extra normal force it adds (eq 11):
```
P_ij = ( tr(σ_i) + tr(σ_j) ) / 3        F_mc = (β·ν·a_ij)·P_ij        (β = 0.5 calibrated)
```
**Combined** normal force (eq 12–13):
```
loading:    F_{i-j} = F_el     + F_mc   (δ < δ_y)
            F_{i-j} = F_el-pl  + F_mc   (δ ≥ δ_y)
unloading:  F_{i-j} = F_unloading + F_mc (δ ≥ δ_y)
```
→ This term grows with confinement (more contacts ⇒ larger tr σ) so it matters only at
**relative density > 0.7** (dense regime); below that it is ~negligible.

### 3. Bond model (§2.4, Sangrós [38]) — the binder (SBR) + carbon black
Bond between i,j if (eq 14) `d_ij < (r_i+r_j)(1+f)`; bond radius (eq 15) `r_b = α_b·min(r_i,r_j)`.
Spring-dashpot force/moment rates (eq 16–19): `dF_b,n/dt = −v_n·S_n·A`, … with normal/tangential
bond stiffness S_n=2.5e13, S_t=1.875e13 N/m³, damping 0.9997; α_b regulated so bond volume =
experimental binder volume fraction (gradient α_b bottom/top: sep 0.45/0.2, cathode 0.35/0.25).

### 4. Porosity / readout
Porosity (eq 20): `ε = 1 − m/(ρ_eff·t·A)`.  Overlap % (eq 22): `δ% = δ/min(r_i,r_j)·100`.
Ionic conductivity from EIS (eq 21): `σ = l/(R·a)`; and a resistor network (Fig 3, Sangrós
[39]) of intra-particle R_p (length) + contact R_c (area) + bond R_b → solved for σ_ionic.

### Contact-model comparison result (Fig 6, 8) — why the multi-contact matters
- **Hertz** over-estimates force (no yield) → predicts hugely too-high thickness/pressure.
- **Thornton–Ning** deviates after yield (lower force, residual overlap) → better, estimates
  ~300 MPa for the experimental thickness.
- **Multi-contact elasto-plastic** adds confinement force at high overlap (>24 %) → matches
  the experimental thickness at the correct 350 MPa.  "Hertz / Thornton–Ning not recommended
  for relative density > 0.7; multi-contact needed."

---

## ★ 부족한 부분 — where it falls short vs OUR DEM+MPM framework

| # | Their model lacks | OUR model has it |
|---|---|---|
| 1 | **Particle SHAPE change** — spheres only, δ is a proxy | MPM: true plastic morphology (SEM core-preserved + boundary-flattening, ✓-matched) |
| 2 | **Volume-preserving void-fill FLOW** — densify by rearrange + overlap | MPM: SE plastically flows into voids (ν=0.49, K real) → below packing floor |
| 3 | **Sub-20 % porosity** — explicitly "not pursued" (cost); floors 21/37 % | We routinely reach 10–16 % (real ASSB >95 % density: Minnmann 10 %, real_14 15.6 %) |
| 4 | **Plastic-strain FIELD** — no spatial Σdg / damage onset | MPM Σdg field (chemo-mech degradation onset, fracture seeding) |
| 5 | **Transport TRIAD** — only σ_ionic | σ_ionic + σ_electronic + σ_thermal, validated scaling laws (LOOCV 0.97/0.95/0.90) |
| 6 | **Coverage** — only "surface area in contact %" (8–13 %), a contact-area fraction | AM-by-SE coverage, plastic(deformed) vs rigid(geometric) at Hertz/Tabor bands |
| 7 | **AM fracture / Auerbach** — only binder bond-break, no CAM particle fracture | DEM fracture-aware Holm (f_intact), Auerbach, force-chain, percolation |
| 8 | **Multi-contact is a pairwise CORRECTION** — mean-field P_mc per contact, semi-independent | MPM continuum couples ALL material points via the stress field NATIVELY (exact, not mean-field) |
| 9 | **Material = halide** (E=10.58 GPa) — numbers don't transfer to LPSCl | LPSCl-anchored (E_eff 1.35 / real 24, Minnmann/Cronau) |

Crux: items 1–4 are the SAME limit our **frame [1]/[2]** names for any rigid-sphere DEM.
Their multi-contact term (#8) is a clever DEM patch for dense-regime force, but it is still
an approximation of what a continuum (our MPM) does exactly — and it still cannot deform a
particle or flow into a void.  Their honest "spheres = compromise, <20 % = future work" is
**precisely the gap our resolved-grain plastic MPM fills**.

### Where THEY lead (worth adopting / studying)
- **Multi-contact confinement term F_mc** = a physically-transparent dense-regime force
  correction.  Our equivalent is the empirical 18× E softening.  Study: does our softening
  effectively reproduce P_mc?  (Same symptom — pairwise Hertz too stiff at ρ>0.7 — different
  mechanism.)
- **Explicit binder (SBR) + CB bond model** with its own ionic resistance R_b — we model no
  binder mechanically or electrochemically.  Relevant when we add SBR/CB.
- **Multi-pressure experimental validation** (100–350 MPa, both separator AND cathode,
  thickness matched < 1 %) — a template for extending our single-point (Minnmann) /
  Heckel anchoring into a full validated pressure sweep.
- **Thornton–Ning proper yield law** with residual overlap — a textbook elasto-plastic
  contact; our hooke/hysteresis is simpler (Stage-E adds the plastic AREA separately).

---

## ★ Frame [5] confirmation — a state-of-the-art DEM admits the gap our MPM fills

A 2026 peer-reviewed DEM, MORE sophisticated than ours on the contact law (Thornton–Ning +
multi-contact vs hooke/hysteresis + softening), is STILL on the **DEM / transport** side:
it owns the contact network, contact-area growth, **ionic conductivity** (R_p+R_c+R_b
network — our Kirchhoff/Holm analog), porosity-vs-pressure, packing — and explicitly names
its limits (sphere shape, no sub-20 % porosity, "realistic shapes = future work").  Cite as
**independent confirmation** that the resolved-grain plastic regime + sub-20 % porosity +
morphology require a method beyond rigid-sphere DEM.  Our DEM↔MPM split is not a crutch — a
leading group hits the same wall and labels it future work.

---

## ★ POROSITY-relation learnables (target: extract our porosity relation)

### Data (thickness = stated precisely in Fig 9/12 legends; porosity ≈ digitised Fig 10/13)
**Separator** (halide SE 97 wt% + SBR 3 wt%, unimodal, E_SE=10.58 GPa):

| P (MPa) | porosity ≈ | h_c sim/exp (µm) |
|---|---|---|
| 0 | 45 % | (h_a init) |
| 100 | 35 % | 188.2 / 186 |
| 200 | 31 % | 170.3 / 171 |
| 300 | 25 % | 152.7 / 154 |
| 350 | 21 % | 143.5 / 145 |

**Cathode** (NMC-811 77.6 + SE 17.43 + SBR 3 + CB 0.97 wt%, bimodal):

| P (MPa) | porosity ≈ | h_c sim/exp (µm) |
|---|---|---|
| 0 | 49 % | (h_a init) |
| 125 | 39 % | 146.6 / 145.2 |
| 200 | 38 % | 141.2 / 140.5 |
| 300 | 37.5 % | 137.7 / 137.1 |
| 350 | 37 % | 135.6 / 135.3 |

DoD = (h_a − h_c)/h_a.  Both curves show a **slope change ≈100 MPa = elastic→plastic
transition** (their words) — mirrors our DEM Heckel P_y = 138 MPa.

### The key insight: the porosity FLOOR is set by (E_SE, composition, flow mechanism)
| | their halide | OUR LPSCl |
|---|---|---|
| SE Young's E | 10.58 GPa | E_eff 1.35 (MPM 1.53), real 24 |
| separator / pure-SE floor | **21 %** @350 | **~10 %** @300 (Minnmann) |
| AM-rich cathode floor | **37 %** @350 | **15.6 %** (real_14 @300) |

Same pressure range, **~2× denser** for us — because (a) LPSCl E_eff is ~8× softer than the
halide (stiffer SE ⇒ higher residual porosity; exactly our MPM E-sweep E24→33-38 %,
E1.35→8 %), and (b) our DEM softening + MPM plastic **flow** reach below the rigid-sphere
packing floor that caps them at ~20 %.

⇒ **Our porosity relation MUST carry an E_SE (stiffness) term and a composition term**, and
~20 % is a hard rigid-sphere floor unless plastic flow is included.  Heckel
`ln(1/(1−D)) = K·P + A` is the candidate form (we have it for our DEM: R²=0.965,
P_y=138 MPa); their independent (stiffer-SE) data lets us cross-check K and the
elastic→plastic knee.

### Material anchors (Table 1)
- Halide SE: E=10.58 GPa, ν=0.3, ρ=2.6 g/cm³, d10/50/90 = 1.1/2.1/3.8 µm.
- NMC-811: E=140 GPa, ν=0.25, ρ=4.75 g/cm³, d=2.6/3.4/6.1 µm.  (our E_AM=140 ✓)
- NMC "elastic up to 0.10 % of radius, then plastic" — yield-onset anchor.
- Halide intrinsic ionic σ = 1.8 mS/cm → confined-separator effective 0.0025–0.005 mS/cm.

---

## Action items
1. **Porosity relation:** fit Heckel to the separator + cathode data
   (`docs/data/densification_porosity_db.csv`); compare K / P_y to our DEM (P_y 138 MPa) →
   confirm the elastic→plastic knee is material-general; add an **E_SE floor term** to our
   porosity scaling.
2. **Frame[5] citation:** Varkey 2026 = the independent DEM that names the sphere-shape /
   sub-20 % limit our MPM addresses.
3. **(Optional) multi-contact vs softening study** — does F_mc ≈ our 18× softening in the
   dense (ρ>0.7) regime?

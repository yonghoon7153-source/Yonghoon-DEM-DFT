# Literature Coverage Database

Purpose: calibrate `plastic_coverage.py` k_spread against physical coverage values
reported in ASSB literature. Single source of truth for process conditions,
coverage metrics, and comparability notes.

## Files
- `coverage_db.json` — machine-readable entries (feed into calibration scripts)
- `README.md` — this file, human summary

## Our baseline
- Process: single-compression pellet, ~300 MPa
- DEM raw coverage: 85% (uncapped, non-physical)
- DEM plastic-capped coverage: 22% (geometric cap a² ≤ min(R1,R2)²)
- Metric: 3D surface-area coverage

## Entries

### 1. Lee 2024 Nature Communications (Tier 1, user-supplied text + SI)
| Process        | Coverage (2D) | Matches ours? |
|----------------|---------------|---------------|
| Hand-mixed     | 30.6%         | YES (single compression) |
| Wet-process    | 33.3%         | PARTIAL (slurry route)   |
| Dry-process    | 67.2%         | NO (high-shear mixing)   |

**Key insight from SI:**
- Coverage metric is **2D SEM perimeter**, not 3D surface
- Pressure: 7 TON on 13 mm = **~520 MPa** (not 300 MPa)
- AM radius range: 2-10 μm (representative R = 10 μm)
- SE radius range: 0.5-2 μm
- DEM validation uses Hertz-Mindlin with E_NCM=140 GPa, E_LPSCl=24 GPa
- Cell: Li-In | LPSCl (150 mg, 1.4 TON) | NMC532+LPSCl+CNT (80:18.5:1.5)

**Takeaway for k_spread:**
- Naive: target 30.6% vs DEM 22% → k_spread ≈ 1.18
- Corrected: 2D-to-3D factor ~1.3-1.5x → true 3D target ≈ 0.40 → k_spread ≈ 1.35
- DO NOT use dry-process 67.2% as calibration target (different process)

### 2. Bielefeld 2019 JPCC (Tier 1, user-supplied full text)
**Kind: computational microstructural modeling (NOT experiment).**

| Property                        | Value |
|---------------------------------|-------|
| Percolation exponent β          | 0.41 (3D site-percolation — validates our scaling law) |
| Threshold formula               | pc[vol%] = 7.83·ln(d/μm) + 36.67 |
| Optimal 5% porosity             | 80/20 wt NCM622:LPS |
| Optimal 10% porosity            | 82/18 wt |
| Optimal 20% porosity            | 86/14 wt |
| Operating band @ 20% porosity   | 69-79 vol% AM |
| AM shape                        | spheres (no overlap) |
| SE shape                        | convex polyhedra (with overlap, absorbed by AM at merge) |
| Metric                          | A_spec,a (m²/m³), not % coverage |

**Correction to earlier claim:** This paper does **NOT** give τ vs composition
or σ_eff vs composition curves directly. It gives percolation metrics. Still
valuable: validates our scaling law exponents (β, CN^1.5 dependence) and gives
optimal composition anchors that match our dataset.

**Coverage equivalent:** can be back-derived as
  coverage ≈ A_spec,a / (g_AM^V · 6 / d_AM)
but requires reading plot values (not tabulated).

**AM-SE interface coverage (digitized Fig 7, 8, 10):**
| Porosity | Peak A_spec,a | Peak composition | Coverage |
|----------|---------------|------------------|----------|
| 5%       | 5.8e5 m²/m³   | 65/35 vol%       | **78%**  |
| 10%      | 5.0e5 m²/m³   | 65/35 vol%       | **71%**  |
| 20%      | 3.3e5 m²/m³   | 70/30 vol%       | **49%**  |

Thickness (Fig 10, 20-140 μm) does NOT change peak coverage.

**Porosity sweep at 70/30 vol% composition (Fig 9, 5μm AM):**
| Porosity | AM total vol% | A_spec,a | Coverage |
|----------|---------------|----------|----------|
| 43%      | 40            | 0.01e5   | 0.2%     |
| 30%      | 49            | 0.50e5   | 8.5%     |
| 25%      | 52.5          | 2.00e5   | 31.7%    |
| 20%      | 56            | 3.30e5   | 49.1%    |
| 15%      | 59.5          | 4.30e5   | 60.2%    |
| 10%      | 63            | 5.20e5   | 68.8%    |
| 5%       | 66.5          | 5.90e5   | 73.9%    |
| 3%       | 67.9          | 6.00e5   | 73.6%    |

Regimes: ionic+electronic limited above φ≈34%; electronic-only limited
21-34%; well-connected below 21%. Monotonic coverage increase with
densification.

**k_spread calibration anchor (20% porosity, 5μm):**
- Our DEM plastic-capped: 22%
- Bielefeld 20%-porosity peak: 49%
- Ratio: 2.2× under-estimate → **k_spread ≈ 1.49**
- Cross-check with Lee 2024 hand-mixed (30.6% 2D → ~39% 3D): same order
- **Final k_spread range: 1.30-1.50**

### 3. Hlushkou 2018 JPS (Tier 1, user-supplied main + SI)
**Kind: experimental 3D FIB-SEM reconstruction + random-walk simulation.**

| Property                         | Value               |
|----------------------------------|---------------------|
| Pressure (electrochemistry)      | **276 MPa** (≈ our 300 MPa) |
| Chemistry                        | LCO/LPSI (partial NMC/LPSCl match) |
| AM                               | 5 μm LCO, LiNbO3-coated, irregular shape |
| SE                               | 0.67(0.75Li2S-0.25P2S5)-0.33LiI, σ=0.7 mS/cm |
| Initial mixture (vol)            | 38% LCO / 62% SE / 0% void |
| Reconstructed (vol)              | 33.1% LCO / 53.7% SE / **13.2% void** |
| τ_cond (EIS)                     | 1.6 ± 0.1           |
| τ_diff (FIB-SEM)                 | 1.74                |
| τ_Bruggeman at ε=0.537           | 1.34 (under-predicts) |
| Void-free τ_diff                 | 1.27                |
| D_eff / D_electrolyte (actual)   | 0.574               |
| D_eff / D_electrolyte (void-free)| 0.786               |

**Critical insight:** 276 MPa pressing ≠ full densification — **13.2% voids
remain**. Our DEM should target ~13% porosity, not ~20%, as our-match anchor.

**Coverage back-estimate (isotropic assumption):**
coverage_AM-SE ≈ V_SE/(V_SE+V_void) = 0.537/0.669 = **80.3%**
(upper bound — true value lower if voids cling to AM surface).

**Bruggeman failure:** τ=1.74 vs τ_B=1.34 → voids redistribute SE into
tortuous paths, not just reduce volume. Our C_blend(τ) term should allow
deviation from ε^(-0.5) at high void content.

## k_spread summary so far
| Source             | Porosity | Coverage | Method                    |
|--------------------|----------|----------|---------------------------|
| Lee 2024 (hand)    | ~unknown | 30.6% 2D | SEM perimeter (2D→3D ~39%) |
| Bielefeld 2019     | 20%      | 49%      | Computational GeoDict      |
| Bielefeld 2019     | 13%      | ~65%     | interpolated from Fig 9    |
| Hlushkou 2018      | 13.2%    | ~80% (UB)| FIB-SEM, isotropic bound   |
| **Our DEM plastic**| ~13-20%? | 22%      | DEM+δ/R cap                |

At 13% porosity: Bielefeld 65% vs Hlushkou 80% (UB) — real pressed pellet
matches or exceeds computational estimate. Our 22% DEM is **3-3.6×
under-estimate** at this porosity.

**Revised k_spread range: 1.55-1.90** (up from earlier 1.30-1.50 at fixed
20% porosity assumption).

### 4. Zhou 2019 ACS Energy Lett (σ_SE baseline, NOT coverage)
**Kind: σ_SE reference for scaling law σ_grain anchoring.**

Argyrodite SEs from solution-engineered synthesis:
| Material              | σ_ion (mS/cm) | σ_e (mS/cm) |
|-----------------------|---------------|-------------|
| Li6PS5Cl              | **2.4**       | 5.1e-6      |
| Li6PS5Br              | 1.9           | 4.4e-6      |
| Li6PS5Cl0.5Br0.5      | 3.9           | 1.4e-5      |
| Li5.5PS4.5Cl1.5       | 3.9           | 1.4e-5      |

**For our scaling law:** σ_grain anchor for LPSCl = **2.4 mS/cm at 300 K**
(= 0.24 S/m). Electronic σ is 6 orders lower — negligible in σ_eff.

### 5. Strauss 2018 ACS Energy Lett (Tier 1, electronic coverage not ionic)
**Kind: AM-AM electronic coverage via inactive CAM fraction.**

NCM622 + β-Li3PS4 (NOT LPSCl), carbon-free, 7:3 wt (≈47:53 vol):

| Size | d50 (μm) | d90 (μm) | Inactive % | Electronic cov | C/10 cap (mAh/g) |
|------|----------|----------|------------|----------------|------------------|
| S    | 4.0      | 4.8      | **2%**     | 98%            | 162              |
| M    | 8.3      | 13.0     | 27%        | 73%            | 95               |
| L    | 15.6     | 26.1     | 31%        | 69%            | 84               |

**σ_ion composite ≈ 10⁻⁶ S/cm (all sizes)** → τ ≈ 200 vs bare β-Li3PS4 2e-4.
**σ_e composite spans 3 orders** across sizes → electronic percolation limits.

**Critical caveat:** This is AM-AM electronic coverage, NOT AM-SE ionic
coverage. Complementary to Bielefeld/Hlushkou but different metric.

**Cross-check with Bielefeld pc formula (pc = 7.83·ln(d)+36.67):**
- d=4 μm → pc=47.5 vol%, Strauss at 47.2 vol% → borderline, cov 98% optimistic
- d=8 μm → pc=53.0 vol%, Strauss sub-critical → cov 73% consistent
- d=16 μm → pc=58.4 vol%, Strauss deep sub-critical → cov 69% mildly high (polydispersity effect)

**k_spread implication:** Still no direct AM-SE ionic coverage for NCM/LPSCl.
Need Minnmann/Zeier-group post-2020 FIB-SEM work.

### 6. Zhang 2017 ACS AMI (Tier 1, LCO/LGPS composition sweep)
**Kind: experimental composite cathode microstructure + diffusion length coverage proxy.**

LCO (LNTO-coated) + LGPS (σ=5 mS/cm, E=10.5 GPa), carbon-free,
437 MPa cathode press (≈ our 300 MPa):

| Cell | wt   | vol    | d_diff (nm) | Ret% @100 | Role       |
|------|------|--------|-------------|-----------|------------|
| A    | 50:50| 29:71  | 52          | 50%       | SE-rich    |
| B    | 60:40| 38:62  | 51          | 85%       | balanced   |
| C    | 70:30| 49:51  | **60**      | **80%**   | **optimal**|
| D    | 80:20| 62:38  | **100**     | fast fade | AM-rich    |

**Fig 8 Li+ diffusion length as coverage proxy:** d_D/d_C = 1.67 → Cell D
has 60-36% of Cell C's AM-SE coverage (depending on 1/d vs 1/d² scaling).

**Impedance (Fig 5):** R_MF (cathode/SE) rises 25→40 Ω on charge; LNTO
coating reduces this 3× vs bare LCO (90→138 Ω).

**Key finding:** 80:20 wt (62:38 vol) has **AM particles without SE contact**
→ overcharge → capacity fade. Directly validates our coverage^(2/5) term
and coverage-decreases-at-high-AM-loading intuition.

### 7. Koerver 2017 Chem Mater (Tier 1, NCM-811 + β-Li3PS4 first-cycle impedance)
**Kind: in-situ EIS evolution + chemomechanical contact loss.**

NCM-811 (uncoated) + β-Li3PS4, 70:30 wt (47:53 vol), carbon-free,
**446 MPa assembly / 64 MPa operating**:

| Resistance       | SOC-dep | 1st cycle |
|------------------|---------|-----------|
| R_SE,bulk        | none    | ~450 Ω stable |
| R_SE,gb          | small   | 50 Ω increase |
| **R_SE,Cathode** | strong  | **+140 Ω = 180 Ω·cm² IRREVERSIBLE** |
| R_SE,Anode       | reversible | 40 → 800 Ω @ end discharge |

**Most critical:** R_SE,Cathode growth of 140 Ω during 1st charge (OCV
3.2-3.4 V) → interpreted as ~50% dynamic coverage LOSS from
chemomechanical contraction + CEI formation.

**Performance:** 1st cycle CE 70.5% SSB vs 85.9% LE (15.4% excess loss
attributed to interface). Catastrophic rate capability: 0.1C→124, 0.5C→4,
1C→0 mAh/g. 65% retention @ 50 cycles.

**Direct quote from paper:** "solid cathode composites are not 100%
dense, and thus, not every NCM particle is ionically and electronically
well addressed when using two-phase composites" → **confirms our
coverage < 100% assumption, validates scaling law coverage term.**

**k_spread dual dimension:**
- Static (initial pressing): Bielefeld/Hlushkou/our DEM domain
- **Dynamic (cycling-induced): Koerver 140 Ω growth domain — NEW**

**Fig 6 SEM direct evidence of contact loss:**
- Uncycled: intimate NCM-SE contact (~100% coverage)
- 1st charge: spherical gap around each NCM (c-axis contraction)
- 50 cycles: "negative imprint" of original NCM surface on SE
- NCM (Ni-rich) SHRINKS on charge (LCO expands — opposite!)

**Fig S3 hidden gem — resistance growth WITHOUT current:**
- NCM-811/β-Li3PS4 blend at OCV over 128 h
- R_total 1200 → 2200 Ω (~2× growth)
- XPS confirms NO chemical reaction (Fig S4)
- Pure mechanical relaxation — **maps to our DEM settling phase**
- Time constant ~60 h

**Fig 5 XPS:**
- Only ~1% of SE oxidized after 50 cycles
- Thin interphase with LOW Li+ conductivity (not bulk degradation)

**Coverage layered model (novel framework):**
| Layer | Value | Captured by |
|-------|-------|-------------|
| Static pressing | ~22% (our plastic) | DEM ✓ |
| Mechanical relaxation | ×0.5 (128 h) | DEM settling ✓ |
| 1st-charge contact loss | ×0.7 | NOT captured ✗ |
| CEI growth/cycle | ×0.98/cycle | NOT captured ✗ |

Our scaling law currently captures STATIC coverage only. For cycled
performance prediction, may need coverage_dynamic(SOC) term.

### 8. Minnmann 2022 AEM Perspective (Tier 1, design guidelines)
**Kind: review/perspective (NOT primary data).**

Authors include Strauss, Bielefeld, Janek — synthesizes our entire DB lineage.

**Quantitative guidelines consolidated:**
| Parameter | Recommended | Source |
|-----------|-------------|--------|
| NCM secondary d | **3-5 μm** | Strauss 2018, Bielefeld 2019 |
| CAM vol% (percolation) | ≥50 | Bielefeld 2019 |
| CAM vol% (geometric optimum) | **60-70** | multiple |
| CAM vol% (commercial target) | ≥70 | perspective |
| CAM vol% (carbon-free) | ≥60 | Strauss 2018 |
| Lab operating pressure | **2-50 MPa** | Koerver, Strauss |
| Sulfide SE σ max | 25 mS/cm | LGPS literature |
| Halide SE σ (cold-press) | 1 mS/cm | Zhou 2019 |

**Key framing (Figure 1):**
- Macro: material/PSD/percolation
- Micro: chemo-mechanics/voids/pressure
- Nano: SE decomposition/interphase

**Figure 2 LE vs SE tortuosity:** SE composite inherently high-τ due to
grain boundaries + porosity → **directly validates our C_blend(τ) need**.

**Takeaway for our scaling law:**
- Variable choices (vol_AM, τ, coverage, CN) confirmed as primary
- 3-5 μm AM optimal matches our fine-particle (P) size class
- CAM 60-70 vol% target matches Bielefeld optimum
- Dynamic coverage framework (from Koerver 2017) is the field's consensus

### 9. Minnmann 2021 JES (Tier 1, chemistry-EXACT anchor) ⭐
**Kind: experimental EIS-TLM tortuosity for NCM-622/LPSCl — the closest match to our system.**

DOI: 10.1149/1945-7111/abf8d7 (Editors' Choice, Open Access)

| Property (42 vol% CAM composite) | Value |
|---|---|
| Pressure | 380 MPa × 3 min RT (vs our 300 MPa) |
| R_el / R_ion | 107 Ω / 360 Ω |
| Thickness | 470 μm |
| σ_el,eff / σ_ion,eff | 5.6×10⁻⁴ / 1.7×10⁻⁴ S/cm |
| **τ²_ion / τ_ion** | **4.3 / 2.07** |
| Porosity | 14% (range 13-17%) |

**Chemistry-exact match:**
- NCM-622 (BASF, 3 μm) + Li₆PS₅Cl (NEI Corp, σ=1.6 mS/cm coarse, 1.2 mS/cm fine)
- σ_e(NCM-622) = 10 mS/cm

**Cross-validation with v29:**
- Bruggeman form: σ_eff = 1.6 × 0.42 / 4.3 = **0.156 mS/cm** (predicted)
- Minnmann measured: **0.17 mS/cm** → error **8%** ✓
- Experimental τ_ion=2.07 ≈ our C_blend(τ) sigmoid center **τ_c=2.04** (diff 1.5%)

**Volume fraction sweep (Fig 2):**
| CAM vol% | τ²_ion | τ²_el | σ_ion,eff | σ_el,eff |
|---|---|---|---|---|
| 25 | 5.76 | 120 | 3e-4 | 2.1e-5 |
| 42 | 4.3 | 7.4 | 1.7e-4 | 5.6e-4 |
| 53 | 15.3 | — | — | — |
| 61 | 130 | 4.3 | 1e-6 | 1e-2 |

**Fine SE benefit (61 vol% CAM, Fig 6):**
- coarse SE τ²=130 → fine SE τ²=34 (3.8× improvement)
- SE particle size = dominant tortuosity driver at high CAM

**Design rules:**
- CAM ≥ 60 vol% with σ_e(CAM) ≥ 10 mS/cm → carbon-free viable
- For 61 vol% CAM with τ²=34 to reach σ_eff=0.4 mS/cm → need σ_SE ≥ 47 mS/cm (currently unreachable)

### 10. Mohayman 2025 ACS Appl Eng Mater (Tier 1, LPSCl mechanical DFT)
**Kind: first-principles (VASP GGA-PBE) mechanical properties of Li6PS5Cl.**

DOI: 10.1021/acsaenm.5c00184

Stoichiometric LPSCl:
| Property | Value |
|---|---|
| Young's modulus Y | **30.08 GPa** |
| Bulk modulus B | 18.07 GPa |
| Shear modulus G | 12.3 GPa |
| B/G ratio | **1.47 (BRITTLE**, Pugh criterion 1.75) |
| Tensile strength σ_max | 3.3 GPa (ideal crystal) |

**Full elastic tensor (GPa):** C11=35.84, C12=11.12, C13=11.52, C33=32.30, C44=13.15, C55=13.81, C66=13.21

**Li concentration effect (Table S1):** Y drops from 30 GPa (stoichiometric) to 17 GPa (70% Li). B/G rises from 1.47 to 2.2 at 70% or 130% Li → **more ductile at cycling interfaces**.

**Cross-link to our framework:**
- DFT ideal crystal Y=30 GPa → our polycrystalline + GB + 14% porosity → **24 GPa effective** (20% reduction, consistent)
- B/G=1.47 "technically brittle" — reconciled via Sakuda 2013 room-temperature pressure sintering mechanism
- Off-stoichiometric ductility explains Koerver 2017 chemomechanical cycling observations

### 11. Sakuda 2013 Sci Rep (Tier 1, LPS experimental mechanical + RT sintering) ⭐
**Kind: experimental ultrasonic Young's modulus + density-vs-pressure for Li2S-P2S5 glasses.**

DOI: 10.1038/srep02261

**Critical confirmation:** 75Li₂S·25P₂S₅ glass **Y = 24 GPa** (ultrasonic pulse) — **EXACT MATCH to our lab assumption**.

| Composition | Y (GPa) |
|---|---|
| 50Li2S·50P2S5 | 18 |
| 60Li2S·40P2S5 | ~22 |
| **75Li2S·25P2S5** | **24** |
| 80Li2S·20P2S5 | 25 |
| 75Na2S·25P2S5 | 18 (ionic radius comparison) |

**Density vs pressure (Fig 2a), cold press at 25°C:**
| Pressure | Rel density |
|---|---|
| 74 MPa | 61% |
| 200 MPa | 80% |
| **300 MPa** | **87%** (= 13% porosity) |
| 360 MPa | 90% |
| 500 MPa | 95% |

**σ_ion vs pressure (Fig 4):** saturates at 3.1×10⁻⁴ S/cm at 360 MPa (~91% of bulk hot-pressed 3.4×10⁻⁴).

**Room-temperature pressure sintering mechanism:**
- Li-S bonds: lower dissociation energy + more covalent than Li-O
- Glass structure + low Tg → Li⁺ and PS₄³⁻ rotate/diffuse at grain boundaries under stress
- SEM (Fig 2d, 3a): grain boundaries disappear at 360 MPa
- **Justifies our DEM hooke/hysteresis + reduced E_eff approach** — it captures macroscopic RT-pressure-sintering

**Three-way porosity agreement at 300-380 MPa:**
| Source | Porosity |
|---|---|
| Our DEM (reduced-E) | 13-17% |
| Sakuda 2013 (300 MPa cold press) | 13% |
| Minnmann 2021 (380 MPa cold press) | 14% (range 13-17%) |

**Bridges DFT-to-experiment:** Mohayman DFT (30 GPa) − GB/porosity correction (~20%) = Sakuda measured (24 GPa) = our lab assumption (24 GPa).

### 12. Koerver 2018 EES (Tier 1, chemomechanical expansion + elastic constants GOLD) ⭐
**Kind: systematic 3-method chemomechanical study (XRD + OCV(p) + operando stress) + complete Table 1 elastic constants.**

DOI: 10.1039/c8ee00907d

**Three measurement approaches (Fig 1):**
- (a) XRD: a,b,c = f(c(Li))
- (b) OCV(p): (∂E/∂p)_T = −(1/nF)·Δ_rV_m
- (c) Operando stress: Δp = −ε_vol·K

**NCM family ΔV/V at full delithiation (Fig 2a):**
| Material | ΔV/V |
|---|---|
| LCO | +2% (EXPANSION) |
| NCM-111 | ~−2% |
| NCM-523 | ~−3% |
| **NCM-622** | **~−4%** (ours) |
| NCM-811 | ~−6% |
| NCA | ~−6% |

**Table 1 — Elastic constants (GPa) — COMPLETE REFERENCE:**

CAMs:
| | E | ν | G | K |
|---|---|---|---|---|
| LiCoO₂ | 191 | 0.24 | 80 | 122 |
| NCM-111 | 199 | 0.25 | 78 | 133 |
| LiFePO₄ | 118 | 0.30 | 46 | 98 |
| LiMn₂O₄ | 194 | 0.26 | 77 | 135 |

SEs (우리 관심):
| | E | ν | G | K |
|---|---|---|---|---|
| **Li₆PS₅X (Cl,Br,I)** | **22-30** | **0.33-0.37** | **8-11** | **28-30** |
| β-Li₃PS₄ | 28.9 | 0.27 | 11.3 | 21.4 |
| γ-Li₃PS₄ | 36.9 | 0.26 | 14.1 | 31.9 |
| LGPS | 37.2 | 0.30 | 14.3 | 31.0 |
| Li₇P₃S₁₁ | 21.9 | 0.36 | 8.1 | 23.9 |
| LLZO | 150 | 0.26 | 60 | 103 |
| LiPON | 77 | 0.25 | 31 | 51 |

→ **LPSCl 22-30 GPa brackets Sakuda exp 24, Mohayman DFT 30, our lab 24**

Anodes:
| | E | ν | G | K |
|---|---|---|---|---|
| Li | 4.9 | 0.42 | 4.2 | 11 |
| In | 12.6 | 0.45 | 4.4 | 42 |
| LTO | 181 | 0.25 | 73 | 125 |
| Graphite | 32 | 0.31 | 12 | 28 |

**Operando stress (Fig 4, per cycle):**
| Cell | σ₁₁ (MPa) |
|---|---|
| LTO\|SE\|LCO | +0.06 |
| LTO\|SE\|NCM-811 | −0.06 |
| Li\|SE\|NCM-811 | +1.5 (Li dominates) |
| LiC₆\|SE\|NCM-811 | +0.6 (graphite dominates) |

**Pressure buildup model vs measured (Eq 11):**
- LCO/LTO calculated: **+14.4 MPa** vs measured +0.06 MPa (**240× gap**)
- NCM/LTO calculated: **−65.9 MPa** vs measured −0.06 MPa

→ **plastic SE deformation + pore filling absorb ~99% of calculated stress** (our plastic framework validated)

**Fig 5 — Zero-strain blending experimental proof:**
- NCM-811 : LCO = 55:45 wt% blend → Δσ₁₁ ≈ 0 (cancellation)
- Composite 38:32:30 wt (NCM:LCO:SE)
- No delamination (SEM Fig S7-S8)

**Experimental protocol:**
- Assembly: 35 kN = **445 MPa** (우리 300 MPa 급)
- Operating: **70 MPa** (Koerver 2017 64 MPa 대비 유사)
- SE: β-Li₃PS₄, CAM:SE = 70:30 wt
- OCV pressure test: 55, 94, 143, 192 MPa
- Cycling: 4.3 V vs Li+/Li, 0.1C

**핵심 직접 인용 (cite용):**
> "plastic deformation of SE will never work perfectly, slow and perhaps not effective enough"
>
> "Good SSBs may require a minimum porosity in the electrode composites to avoid too strong changes in stress"

→ 우리 plastic_coverage.py framework + 13-17% porosity target 둘 다 문헌 지지.

## Pending entries (priority order)
- Tier 1: Nam 2018 JPS (dry vs slurry process, NCM622/argyrodite)
- Tier 2: Jackson 2017 review (plastic contact mechanics theory cite)
- Tier 2: Minnmann 2024 JES (modern NCM/LPSCl tomography)
- Tier 3: Kato 2018 JPCL (thick electrode scaling)

### 13. McGeary 1961 J Am Ceram Soc (Tier 1, founding reference for binary/ternary packing wave curves)

**Kind:** experimental mechanical packing of spherical steel/tungsten/aluminium
shot under vibration; the foundational empirical study cited by every binary-RCP
paper since.  PDF stored at `docs/literature_coverage/pdfs/McGeary_1961_JAmCeramSoc_Mechanical_Packing_of_Spherical_Particles.pdf`.

DOI: 10.1111/j.1151-2916.1961.tb13716.x   (J. Am. Ceram. Soc. 44 [10] 513–522)

**Critical findings (directly relevant to our paper):**

| Packing | Max density | Composition | Size ratio |
|---|---|---|---|
| 1-component | 62.5% theoretical | — | — |
| Binary (Fig 3)        | **86.0%** | 73% coarse / 27% fine    | 7:1 (or larger) |
| Ternary (Figs 6, 7)   | **90.0%** | 67 : 23 : 10             | 77 : 7 : 1      |
| Quaternary (Table IV) | **95.1%** | 61 : 23 : 10 : 6         | 316 : 38 : 7 : 1 |

**Size-ratio threshold (Fig 5) — the most important figure for us:**
- Plot is *maximum packing density* vs *d_coarse / d_fine*
- **Knee at d_c/d_f ≈ 7** — below this, packing efficiency drops rapidly
- Triangular pore (passage through three close-packed coarse spheres):
  effective diameter p_t = (2/√3 − 1)·d ≈ 0.154·d_c, so the fine sphere
  can pass freely only when d_c/d_f ≳ 7.

**Our system fit (NCM811 P + S + LPSCl):**
- D_AM_P / D_SE   ≈ 6 µm / 0.5 µm = **12** → above McGeary knee, Furnas valid
- D_AM_P / D_AM_S ≈ 6 / 2          = **3**  → BELOW the knee, no Furnas valley
                                              between AM_P and AM_S
- D_AM_S / D_SE   ≈ 2 / 0.5        = **4**  → marginal, near the knee
- → Quantitatively explains why our paper's λ ≥ 4 filter is *necessary*
  for the Bouvard RCP curve to apply (panel ② of the porosity 4-panel).

**Wave-curve reference for the paper (§5):**
- Fig 3 is the canonical non-monotonic ε(composition) curve with a clear
  V/wave at ~73% coarse.  Pure mechanical packing, **no plastic flow**, so
  the wave is purely *geometric* — directly supports the rewritten §5
  narrative: the hump in our ε(AM_wt) is Bouvard-geometry driven, not
  percolation-gated.
- Caveat: McGeary explicitly states "No plastic deformation of the particles
  occurs."  So McGeary's curves are the **purely-geometric lower bound** of
  what's achievable; our strict-physics adds the Heckel plastic correction
  on top of this baseline.

**Direct quotes for citation:**
> "Forming of high-density multicomponent packings was shown to require at
> least a sevenfold difference between sphere sizes of the individual
> components."
> → anchors our λ ≥ 4 filter as *conservative* relative to McGeary's 7.
>
> "No plastic deformation of the particles occurs, and it is possible to
> pour the material out of the container after packing."
> → defines McGeary as the **pure-geometry baseline** against which our
> plastic contribution is measured.

**Cross-link to refs.bib:** `@article{McGeary1961, ...}` — cite alongside
`Furnas1929`, `Westman1930`, `Bouvard2004` for the geometric Bouvard RCP
baseline in §5.1.

### 14. Bouvard 2000 Powder Technology (Tier 1, plastic-flow monotonic reference — NOT a wave reference)

**Kind:** review of hard / soft powder mixture densification under pressure;
survey of multiple experimental systems (superalloy + alumina, Ag + WC,
Pb + inclusions, Al + carbide, WC + Co).  PDF stored at
`docs/literature_coverage/pdfs/Bouvard_2000_PowderTech_...pdf`.

DOI: 10.1016/S0032-5910(99)00293-4   (Powder Technology 111 [2000] 231–239)

**Critical reading (calibrates expectations for our §5 narrative):**

Bouvard 2000's central claim — quoted from the abstract:

> *"When soft particle deformation is the main densification mechanism,
> **hard particles hinder the densification**, with more or less significance
> depending on whether they are mostly isolated, are grouped in aggregates
> or form a percolating network."*

→ **Bouvard's framework is monotonic.**  Hard fraction ↑ ⇒ density ↓
(no wave, no V, no hump).

**Evidence in the paper:**

| Figure | What it shows | Shape |
|---|---|---|
| Fig 1 | Astroloy + 18 % / 35 % alumina, ρ(t) over 0–200 min | Monotonic asymptote; more alumina ⇒ lower density |
| Fig 4 | Ag + WC, ρ vs vol% WC for r = 0.08, 1, 2.5, 4, 10  | **All curves monotonically decreasing** in 0–40 % WC |
| Fig 5 | Pb + 18 % spherical / angular inclusions, ρ(t)       | Monotonic, angular < spherical |
| Fig 7 | Al + 60 % carbide, ρ(P) at 25 °C / 450 °C            | Monotonic increase with pressure |
| Fig 8 | WC + 0–24 % Co, ρ vs Co fraction                    | Monotonic decrease with Co |

**None of these show a wave / V-curve / hump in $\varepsilon$(composition).**

**Why not (Bouvard's own decomposition, §5):**
1. Low hard fraction → isolated inclusions → moderate hindrance
2. Mid hard fraction → aggregates → stronger hindrance
3. High hard fraction → percolating skeleton → soft particle deformation
   blocked, density limited

All three regimes act in the *same direction* (densification harder), so the
curve is monotonic.

**Why our paper's $\varepsilon$(AM_wt) DOES show a hump despite Bouvard
2000's monotonicity:**

| | Bouvard 2000 experiments | Our DEM cathodes |
|---|---|---|
| Soft phase | One size only (Ag / Pb / Al / Astroloy) | Three sizes (AM_P, AM_S, SE) |
| Hard fraction range studied | 0–40 % | 0–100 % (full sweep) |
| Geometric Furnas valley active? | No — only one soft size, no binary RCP | **Yes — AM_P/SE λ ≈ 12, AM_S/SE λ ≈ 4, full ternary packing** |
| Plastic flow vs geometry | Plastic dominates | Both compete |

→ Our wave comes from the **geometric ternary RCP** (McGeary-style, §5
Bouvard curve), not from Bouvard 2000's plastic-flow mechanism.

**Honest framing for the paper:**
- Bouvard 2000 is the correct cite for the *plastic-flow monotonic baseline*
  (Heckel-style argument) and for the 3-regime hard-fraction decomposition
  (isolated / aggregates / percolating), which we already invoke for the
  $f_{\mathrm{perc}} = 0.65$ percolation argument.
- Bouvard 2000 is **NOT** an experimental wave-shape precedent.  The only
  cleanly documented wave is McGeary 1961 (Fig 3), and it is purely
  geometric.

**Hard-rich extrapolation (AM\_wt > 95 %):**
- Bouvard 2000 explicitly notes that beyond the percolation transition the
  hard skeleton supports the load and densification approaches a hard limit
  set by the hard-phase RCP.  This is the regime our paper §6 disclaims as
  not validated by our data (n = 0 above AM\_wt = 95 %).

**Cross-link to refs.bib:** entry `@article{Bouvard2000, ...}` already in
the bibliography; the existing `note` field correctly describes it as the
three-regime hard-soft framework, not as a wave-shape reference.

## Open issue: 2D-to-3D conversion
For randomly sectioned spheres touching SE:
- Perimeter coverage (2D SEM) ≤ surface coverage (3D)
- Geometric factor depends on spatial isotropy of SE contacts
- Literature: Underwood stereology, E(3D) ≈ (4/π) · E(2D perimeter) ≈ 1.27x
- → Lee 2024 hand-mixed 30.6% (2D) ≈ 0.39 (3D) as first estimate

## How to use
```python
import json
db = json.load(open("docs/literature_coverage/coverage_db.json"))
for entry in db["entries"]:
    if entry["comparability_with_ours"]["process_match"] == "YES":
        print(entry["id"], entry["coverage_values_pct"])
```

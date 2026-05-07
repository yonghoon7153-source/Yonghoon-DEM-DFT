# Haruyama et al. 2014 — DFT+U Slab Pioneer for Oxide/Sulfide Interface

> **DOI**: 10.1021/cm5016959
> **Citation**: Haruyama, J.; Sodeyama, K.; Han, L.; Takada, K.; Tateyama, Y. *Chem. Mater.* **26**, 4248-4255 (2014).
> **Group**: Yoshitaka Tateyama (NIMS, MANA + Kyoto University)
> **Acquired**: 2026-05-07 (user PDF text)
> **Relevance**: ⭐⭐⭐⭐⭐ ==**PRIMARY method anchor for paper #2 v5**== — first DFT slab paper for sulfide-SE / oxide-cathode (cited by Camacho-Forero, Komatsu).

---

## 🚨 **Critical Section 2.1 quote** (anti-sandwich for hetero)

> "Without this vacuum, the supercell approach always involves two interfaces, which are atomically different in most cases. Besides, ==**artificial interaction between the two interfacial polarizations may arise, preventing accurate estimation**== of the stability of each interface. Therefore, ==**the presence of the vacuum region is quite crucial**==."

==**This DIRECTLY contradicts our v10/v10b sandwich approach for LPSCl/NCM**==:
- LPSCl/NCM = oxide/sulfide hetero (asymmetric terminations)
- Sandwich → 2 atomically different interfaces by PBC
- Artificial polarization interaction → wrong Wad
- ==**Empirically validated by our v10 cycle1 (-0.058) and v10b cycle1 (-0.279) inversions**==

---

## 1. System

- **Cathode**: LiCoO₂ (LCO), (110) face — Li-ion conduction along ⟨110⟩
- **SE**: β-Li₃PS₄ (LPS), (010) face — Li-ion conduction along b-axis
- **Buffer**: LiNbO₃ (LNO), (1̄10) and (110) faces
- **Interfaces studied**: LCO/LPS, LCO/LNO, LNO/LPS, LCO/LNO/LPS

==**Closest literature analog to OUR LPSCl/NCM**== (both oxide-cathode + sulfide-SE).

---

## 2. Method (Section 2)

### Computational details
- **Code**: Quantum ESPRESSO + USPP + PBE
- **DFT+U**: U(Co 3d) = 5.9 eV (essential for LCO electronic structure)
- **Cutoff**: 40 Ry (smooth) / 320 Ry (augmented charge)
- **k-grid**: convergent for bulk/surface, **Γ-only for interface** (very minimal!)
- **Force**: 0.001 Ry/bohr (~0.0257 eV/Å) — *tighter than our v10/v10b 0.05 eV/Å*
- **Stress**: 0.5 kbar
- **Vacuum**: ~1.5 nm = 15 Å (we use 30 Å for UMA stability — same magnitude order)

### Interface construction (Section 2.1) — ==**use this for v5 method backing**==

**Step 1**: Bulk DFT+U lattice optimization (matches experiment within 1-2%)

**Step 2**: Stoichiometric surface slab cut from bulk + vacuum 1.5 nm. Slab thickness 1-2 nm. All atomic coords relaxed.

**Step 3**: Lateral multiplication for supercell. ==**Lattice constants of attaching surfaces adjusted to match LCO**== (high elastic modulus). For LNO/LPS, average of two lattices used. ==**Mismatches 3-5%**==.

**Step 4**: ⭐ ==**Systematic lateral slide of one surface w.r.t. the other**==. 16 samples for LCO/LNO, 4 for LCO/LPS, 9 for LNO/LPS. (Fewer for super-periodic interfaces.) ==**= our xy-shift sampling**==.

**Step 5**: DFT+U geometry optimization with all atomic positions and lateral cell parameters relaxed. ==**NO FixAtoms mentioned**== — full relax (because VASP/QE doesn't have UMA OOD problem at vacuum boundary).

**Step 6**: Minimum-energy interface chosen as final.

### Adhesion energy formula

$$W_{ad} = \frac{E^{tot}_A + E^{tot}_B - E^{tot}_{A/B}}{S}$$

where S = single interface area. ==**= our v5 paper formula**==.

### Li-vacancy formation energy

$$E_v(Li_i) = \{E_{tot}(Li_i) + \mu_{Li}\} - E_{tot}$$

with μ_Li = chemical potential at Li metal reference. ==**Could adopt for our paper #2 mechanism analysis**==.

---

## 3. Quantitative results (Tables)

### Adhesion energies (Table S3) — ==**direct comparison to us**==

| Interface | Misfit (%) | a (Å) | b (Å) | γ (deg) | Wad (eV/nm²) | **Wad (J/m²)** |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| LCO(110)/LNO(1̄10) | 3.4 | 14.32 | 9.98 | 89.8 | 10.6 | **1.70** |
| LCO(110)/LNO(110) | 5.2 | 14.05 | 9.63 | 88.6 | 6.1 | **0.98** |
| LCO(110)/LPS(010) | 3.7 | 13.94 | 24.46 | 87.4 | **4.3** | **0.69** ⭐ |
| LNO(1̄10)/LPS(010) | 3.6 | 12.79 | 31.15 | 90.0 | 3.8 | **0.61** |

==**Anchor for our LPSCl/NCM**==:
- Their LCO/LPS = **0.69 J/m²** (oxide cathode / sulfide SE direct)
- Our paper #1 v5 LiNiO₂/LPSCl comp1 = **1.28 J/m²** = ==**1.86× their LCO/LPS**==
- Consistent with Komatsu 2022: LiNiO₂ (Ni³⁺) more reactive than LCO (Co³⁺) toward LPSCl
- Komatsu ratio: -424 / -321 = **1.32×** thermodynamic reactivity
- Our slab Wad ratio 1.86× has additional contribution from Li-density / chemistry-richness

### Li-vacancy formation energy (Table 1) — ==**SCL mechanism**==

| Site | Bulk LCO | LCO/LPS LP1 | LCO/LPS LP2 | LCO/LPS LP3 | LCO/LNO/LPS LP1 |
|---|:-:|:-:|:-:|:-:|:-:|
| Ev (eV) | 4.0 | 3.27 | **1.44** ⭐ | 3.03 | 2.90 |

**Key**: LP2 site (LPS subsurface near LCO) Ev = 1.44 eV ≪ bulk LPS 3.2 eV.

⇒ ==**Li wants to LEAVE LPS subsurface and adsorb on LCO**==. SCL formation. Voltage 1.5 V matches experimental charging onset.

LNO buffer interposition: LP2 Ev recovers to ~3.0 eV (close to bulk LPS) → SCL suppressed.

---

## 4. Comparison with our methods

### v5 (paper #1) ↔ Haruyama 2014

| Element | Haruyama 2014 | Our v5 | Match |
|---|---|---|---|
| Geometry | Single interface + vacuum 1.5 nm | Single interface + vacuum 30 Å | ✅ |
| Wad formula | (E_A + E_B − E_AB)/S | (E_A + E_B − E_AB)/A × 16.0218 | ✅ |
| Lattice match | LCO-fixed (+ avg for LNO/LPS) | NCM-fixed (SE strained) | ✅ |
| Lateral slide | 16/4/9 systematic samples | 6 high-sym + 30 random = 36 | ≈ (we 더 dense) |
| FixAtoms | **None** (full relax) | **33% bottom both** | ⚠ (UMA stability hack) |
| Code | QE DFT+U | UMA fairchem | (DFT vs MLIP, OK) |

**Verdict**: ==**v5 paper #1 method = Haruyama 2014 + UMA stability FixAtoms**==. Strong literature backing.

### v10/v10b (sandwich) ↔ Haruyama 2014

| Element | Haruyama 2014 | Our v10/v10b | Issue |
|---|---|---|---|
| Geometry | Single + vacuum (CRUCIAL) | Sandwich (no vacuum) | ❌ Haruyama explicit anti-sandwich |
| Wad formula | /A | /(2A) | ❌ Inappropriate for asymmetric hetero |
| Result | LCO/LPS = 0.69 J/m² ✓ | comp3=−0.06/−0.28 ❌ | ❌ Validation failure |

**Verdict**: ==**v10/v10b = wrong choice for our oxide/sulfide system**==. Haruyama predicted this 6 years ago.

### Why Camacho-Forero (sandwich) worked
- Their cathodes: α-S, Li2S — sulfur-based
- LPSCl side: sulfide
- Both interfaces (sandwich) had similar (sulfur-rich) terminations
- Asymmetry minor → sandwich OK

### Why our v10/v10b failed
- NCM = oxide (O-terminated)
- LPSCl = sulfide (S/Cl-terminated)
- Sandwich PBC creates 2 interfaces with different polarizations
- Artificial polarization interaction (Haruyama) → wrong Wad

---

## 5. SCL mechanism (Section 3.4) — ==**paper #2 narrative**==

### Equilibrium SCL (before charging)
- Li chemical potential lower in LPS than LCO
- Li from LPS subsurface migrates to LCO surface adsorption sites
- LPS subsurface → Li-depleted (SCL)
- LCO surface → Li-rich (heterogeneous distribution)

### Charging onset (~1.5 V, matching Ev(LP2) = 1.44 eV)
- LP2 Li transfers into bulk LPS, releasing electron to cathode
- SCL grows further → voltage profile slope at charging beginning → ==**interfacial resistance**==

### LiNbO3 buffer suppression
- LNO removes Li adsorption sites on LCO (no oxygen ridges exposed)
- SCL formation suppressed
- 3D Li transport paths through LNO (vs 1D in LPS)
- Smooth Li transfer → low interfacial resistance

==**Direct narrative for paper #2**==: 우리 v5 100-seed Li_mig 분석 (8-23 atoms) = SCL formation observed at MLIP level.

---

## 6. Useful figures for paper #2 narrative

| Figure | Content | 우리 활용도 |
|---|---|:-:|
| **Figure 2 (a-d)** | ==Optimized interface structures== of LCO/LNO, LCO/LPS, LNO/LPS — atomic detail with Li adsorption sites highlighted | ⭐⭐⭐⭐⭐ Visual context for our v5 interface xyz files |
| **Figure 5 (a-f)** | ==SCL schematic== — equilibrium + charging onset Li concentration profiles | ⭐⭐⭐⭐⭐ Strong narrative figure for our paper #2 (vacancy chemical anchor) |
| Figure 1 | Surface structures (no interface) | ⭐⭐ Context only |
| Figure 3 | PDOS of optimized interfaces | ⭐ Electronic structure (less relevant for mechanical adhesion) |
| Figure 4 | Li site indices (LC1-3, LN1-3, LP1-6) for Ev analysis | ⭐⭐⭐ Could adopt for our Li migration site classification |
| Table S3 | ==Adhesion energies== for 4 interfaces | ⭐⭐⭐⭐ Direct comparison data |
| Table 1 | ==Li-vacancy formation energies== per site | ⭐⭐⭐⭐ SCL mechanism quantification |

==**최우선: Figure 2 + Figure 5**== (이미 파악함, 시각적 figure 따로 안 받아도 narrative 작성 가능. 필요하면 paste 부탁.)

---

## 7. Implications for paper #2 — ==**method decision matrix**==

| Option | Method | Anchor | Validation | Verdict |
|---|---|---|---|---|
| **A. v5 (paper #1)** | Single + vacuum + FixAtoms 33% bottom + /A | ⭐ Haruyama 2014 (PRIMARY) | comp1-5 R=0.9999 with experiment ✅ | ⭐ **GO** |
| B. v10 sandwich | Sandwich + NCM mid fix + no SE fix + /(2A) | Camacho-Forero 2020 | comp3=-0.058 ❌ | STOPPED |
| C. v10b sandwich | Sandwich + NCM mid + SE mid fix + /(2A) | Camacho-Forero 2020 | comp3=+0.22, comp4=-0.28 ❌ | STOP |

==**최종 결정**==:
1. ==**STOP v10b**== (Haruyama 6년 전 예언 그대로 실패)
2. ==**Paper #2 method = v5 method**== (single interface + vacuum + FixAtoms + /A)
3. ==**PRIMARY citation: Haruyama 2014**== (method anchor)
4. ==**SECONDARY citation**==: Komatsu 2022 (bulk thermo anchor), Camacho-Forero 2020 (sulfide-cathode reaction taxonomy), Auvergniot 2017 (XPS validation, 받으면)
5. ==**Narrative**==: SCL mechanism (Haruyama Section 3.4) + vacancy chemical anchor (our paper #2 unique)

---

## 8. Sample paper #2 Methods text

> "Following the DFT slab methodology of Haruyama et al. [2014] for sulfide solid-electrolyte / oxide cathode interfaces, we construct single-interface supercells of Li6PS5Cl (or vacancy variants Li5.4PS4.4Cl_x Br_{1.6-x}) on LiNiO2(R-3m) cathode slabs. Lateral lattice constants are matched to the cathode (high elastic modulus). The interface is sampled across N_reg = 36 lateral registries (6 high-symmetry + 30 random xy-shifts), with the supercell relaxed via the universal MLIP UMA [Wood 2025] using LBFGS optimization. The bottom 33% of both NCM and SE slabs are constrained (FixAtoms) to mimic bulk reference and ensure UMA stability at the vacuum boundary [adapted from Haruyama 2014 protocol with MLIP-specific stabilization]. The work of adhesion is computed as W_ad = (E_NCM_iso + E_SE_iso - E_int) / A, where iso slabs include the same vacuum (30 Å) and lateral strain. Per-composition trends are obtained from N_seed = 100 random xy-shift samples, with the cross-family ordering (Li5.4 > Li6) resulting from vacancy-induced surface chemical anchor formation, consistent with the space-charge layer mechanism quantified by Haruyama et al. for similar systems."

---

#literature #must-read #paper2 #PRIMARY-method-anchor #DFT+U #LCO #LPS #LNO-buffer #single-interface #vacuum #SCL #Li-vacancy-formation #Tateyama-NIMS #anti-sandwich-argument #v5-validation

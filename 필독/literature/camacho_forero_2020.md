# Camacho-Forero & Balbuena, Chem. Mater. 2020, 32, 360-373

> **DOI**: 10.1021/acs.chemmater.9b03880
> **Title**: Elucidating Interfacial Phenomena between Solid-State Electrolytes and the Sulfur-Cathode of Lithium−Sulfur Batteries
> **Authors**: Luis E. Camacho-Forero, Perla B. Balbuena (Texas A&M)
> **Funding**: DOE EERE Battery 500 Consortium (DE-EE0008210)
> **Why must-read**: Direct methodological precedent for our paper #2 SE/cathode adhesion. **LPSCl is our comp1.** Sandwich + no-fix + AIMD = literature standard we are deviating from.
> **Acquired**: 2026-05-07 (user-supplied PDF text + figures)

---

## 1. System overlap with us

| Their SSE | Our match |
|---|---|
| β-Li3PS4 (LPS) | reference end-member, no halogen |
| **Li6PS5Cl (LPSCl)** | **= our comp1 EXACTLY** |
| Li7P2S8I (LPSI) | iodide-doped, no overlap |

| Their cathode | Our cathode |
|---|---|
| α-S(001) | NCM811 / LiNiO2 (different chemistry, but same role) |
| Li2S(001) | — |
| Li2S(111) | — |

Most directly comparable to us: **LPSCl(001) / Li2S(001)** = sulfide SSE / lithiated cathode interface.

---

## 2. Method (Section 2.5 + 3.1)

### Computational details (Section 2.1)
- **Code**: VASP, PAW pseudopotentials, PBE
- **Cutoff**: 500 eV (production), reduced to 400 eV during AIMD (∼1 meV/atom diff)
- **Convergence**: SCF 1e-4 eV, forces 0.02 eV/Å
- **AIMD**: NVT, 300 K, dt=1 fs, Nose thermostat (m=0.5), 20 ps (some interfaces extended to 50 ps and tested at 750 K)
- **Charge**: Bader (Henkelman) using grid-based algorithm
- **vdW**: DFT-D3 only for systems containing S8 rings (cyclo-octa sulfur)
- **Visualization**: VESTA, Materials Studio, OVITO; RDF via VMD (Δr=0.01 Å)

### Interface construction (Section 2.5)
1. Build SE supercell + cathode supercell, lattice averaged → mismatch < 10% target (some up to ~13% for S(001), see Table S4)
2. **Each surface independently re-optimized** with new lattices (no vacuum sandwich yet at this stage)
3. **SANDWICH MODEL**: place two slabs at top and bottom of cell, in contact via PBC z-axis ⇒ **2 interfaces** auto-created
4. Equilibrium gap: **2.0 - 2.2 Å**
5. **FULL GEOMETRY RELAXATION (no atoms fixed!)** — this is the critical method choice
6. AIMD 300 K × 20 ps from Opt configuration
7. Property time-averaged over 5-20 ps (15 ps window)

### Wadh formula
```
W_adh = (E_SSE-slab + E_cath-slab − E_SSE/cath) / (2A)
                                                    ↑
                                            denominator 2A because PBC creates 2 interfaces
```

### Interfacial energy γ (Section 3.1)
```
γ = (E_cath/SSE − n_cath E_cath − n_SSE E_SSE − E_str) / (2A)
E_str = Σ [E_i(a_str) − E_i(a0)]   (strain energy from lattice match)
```

**Surface energy of SSE facets** (Table 3, meV/Å²):
| SSE | (001) | (100) | (010) | (110) | (111) |
|---|:-:|:-:|:-:|:-:|:-:|
| LPS | 27 | 49 | 28 | 27 | 24* |
| LPSCl | 1 | 1 | 1 | 10 | 25 |
| LPSI | 16 | 35 | 12 | 11 | 10* |
*non-orthorhombic (italic in original)

LPSCl(001)/(010)/(100) all 1 meV/Å² → highly degenerate due to F-43m symmetry.

---

## 3. Wadh results (Table 4) — full numerical table

Columns: Wadh (meV/Å²), γ (meV/Å²)
Conversion: meV/Å² × 0.01602 = J/m²

| Cathode | SSE | Facet | Wadh (meV/Å²) | γ (meV/Å²) | Wadh (J/m²) |
|---|---|---|:-:|:-:|:-:|
| **S(001)** | LPS | (001) | 17.47 | 25.18 | 0.28 |
| | LPS | (100) | 20.74 | 42.18 | 0.33 |
| | LPSCl | (001) | **2.86** | 19.07 | **0.046** |
| | LPSI | (001) | 26.73 | 2.68 | 0.43 |
| | LPSI | (100) | 44.19 | 15.45 | 0.71 |
| **Li2S(001)** | LPS | (001) | 69.57 | 88.62 | 1.11 |
| | LPS | (100) | 72.33 | 110.63 | 1.16 |
| | **LPSCl** | **(001)** | **89.69** | 73.74 | **1.44** ← ★ comp1-equivalent |
| | LPSI | (001) | **107.23** | 36.26 | 1.72 (max) |
| | LPSI | (100) | 83.30 | 90.52 | 1.33 |
| **Li2S(111)** | LPS | (001) | 9.13 | 39.37 | 0.146 |
| | LPS | (100) | 19.85 | 52.41 | 0.318 |
| | LPSCl | (001) | 10.76 | 11.16 | 0.172 |
| | LPSI | (001) | 10.95 | 25.16 | 0.175 |
| | LPSI | (100) | 30.64 | 25.16 | 0.491 |

**Key observations**:
- Cathode reactivity ordering: S(001) << Li2S(111) << Li2S(001) (Wadh, by SSE family)
- Li2S(001) is most reactive (high surface energy + charge polarization, Figure S9)
- Within Li2S(001): LPSI(001) > LPSCl(001) > LPS — iodide promotes adhesion
- Within Li2S(111): much weaker, LPSI(100) outlier (30.6) due to PS3I dissociation chemistry

**Quantitative anchor for our comp1**: their LPSCl(001)/Li2S(001) Wadh = **89.69 meV/Å² = 1.44 J/m²**. Our paper #1 v5 comp1/NCM = 1.28 J/m² (paper) or 1.15 J/m² (100-seed). **Same order of magnitude ✓**.

---

## 4. Reaction mechanisms (Section 3.2 + Figure 6)

> Critical insight: these are NOT artifacts. They're observed AIMD chemistry, fully characterized.
> Many of these reactions occur during DFT optimization (before AIMD), the rest within first few ps of AIMD.

### 9 canonical reactions (Figure 6a)

| # | Reaction | Where observed |
|---|---|---|
| 1 | PS4³⁻ → PS3(t)³⁻ + S²⁻ | Li-exposed Li2S(001), most common |
| 2 | PS4³⁻ + Sn → S3P-Sn³⁻ or (PS4+n)³⁻ | S-exposed Li2S(001), all S(001) interfaces |
| 3 | 2 PS4³⁻ → P2S7⁴⁻ + S²⁻ | LPSI(001)/S(001) at 6.2 ps |
| 4 | S8 + S²⁻ → S9²⁻ (ring opening) | LPSI(001)/S(001) |
| 5 | S²⁻ + S²⁻ → Sn²⁻ (n=2,3) | charge-depleted S on Li2S(001) |
| 6 | PS3I²⁻ → PS3³⁻ + I⁻ | LPSI all facets, P-I cleavage 25-50% by 20 ps |
| 7 | (S3P-S-S-PS3)⁴⁻ disproportionation → P2S7⁴⁻ + S⁰ | XPS-confirmed (Koerver 2017) |
| 8 | S3P-Sn → PS3(p)⁻ + Sn²⁻ (further reduction) | various |
| 9 | S²⁻ + I⁻ → SI⁻ (oxidative recombination) | Li2S(001)/LPSI(001) |

### Specific interface phenomena
- **Li2S(001)/LPSCl(001)** (Figure 6b): forms mixed Cl⁻/S²⁻ anion layer on Li-exposed face — interpretable as LiCl + Li2S interphase. On S-exposed face: 3 charge-depleted S oxidize → 2× S3²⁻.
- **Li2S(001)/LPSI(001)**: strongest Wadh (107 meV/Å²) due to S-I bond formation linking the two slabs. Most "interconnected" interface.
- **Li2S(111) facets**: chemically passive (S anions fully coordinated within Li-S-Li tri-layer); LPS(001), LPSCl(001), LPSI(001) show no anion changes. Only LPSI(100) shows PS3I dissociation due to PS3I bond strain.

### Charge analysis (Section 3.3, Figure 7-8)
- **At least 65% of total charge transfer happens during DFT optimization** (before AIMD), agreeing with extent of reactions there
- After ~5 ps AIMD, SSE charge stabilizes at constant value
- Time-averaged 5-20 ps: SSE charge per area characterizes redox direction
- **S(001) cathode oxidizes the SSE** (positive sign — SSE loses electrons)
- **Li2S(001) cathode reduces the SSE** (most strongly), Li2S(111) reduces less
- Atomic charges (Figure 8): Li species change <±2%; S/P change up to 10-20%; iodide most reduced (covalent → ionic shift)

---

## 5. Comparison to our paper #2 v4-v9 protocol

| Aspect | Camacho-Forero 2020 (literature std) | Our v4-v9 |
|---|---|---|
| Geometry | **Sandwich** (no vacuum, 2 interfaces) | Single interface + 30 Å vacuum (vs UMA limit) |
| Normalization | **/(2A)** | /A |
| Atomic constraints | **None** (full relax) | FixAtoms 33% bottom on both sides |
| Sampling | **AIMD 300 K × 20 ps**, average 5-20 ps | LBFGS only (v5) or 9 ps MQA (v8) |
| Lattice strain | up to 13% allowed (Table S4) | 0.2-3.3% (we are conservative) |
| Slab thickness | SE 15-25 Å, cathode 15-25 Å | SE 29-30 Å, NCM 1L (~7 Å) or 5L (~70 Å) |
| Reactions | **Allowed** (PS4 reduction, anion layer formation) | Suppressed by FixAtoms; Li migration flagged as "outlier" |

### Implications for v10
1. **Adopt sandwich** ⇒ vacancy chemistry (PS4 → PS3 + S, undercoordinated Li chemisorb to NCM-O) becomes physical, not artifact. Matches Figure 6 reactions exactly.
2. **Drop FixAtoms** ⇒ Li5.4 vacancy effect can express through surface relaxation + ionic-bond rearrangement.
3. **Switch to /(2A)** ⇒ values double if we keep current method (single interface), or stay if we adopt sandwich.
4. **Add 5-10 ps AIMD** if we want to capture chemistry quantitatively; if just structural relaxation, LBFGS may suffice.
5. Our scale already matches their LPSCl/Li2S(001) (1.28 J/m² vs 1.44 J/m²) — protocol switch unlikely to change scale 10×, more likely to fix cross-family ordering.

---

## 6. Key figures referenced (file location)

The user has supplied figure images in conversation (not stored as files in repo).

| Figure | Content | Use for |
|---|---|---|
| S1 | Bulk SSE crystal structures (LPS, LPSCl, LPSI) | reference structures |
| S4 | LPS cleaved facets (001, 010, 100, 110, 111) | surface model precedent |
| S5 | LPSCl cleaved facets — **most relevant for comp1** | **comp1 surface model precedent** |
| S6 | LPSI cleaved facets | iodide chemistry |
| S7 | Li2S(111) hex → orthorhombic (4.041 × 7.000 Å, 15 Å thick) | cathode lattice transformation method |
| S8 | Cathode slab models — S(001) ~25 Å, Li2S(001)/(111) ~15 Å thick | **slab thickness reference** |
| S10 | Optimized S(001)/SSE interfaces (5 panels) | **sandwich geometry visualization** |
| S11 | Optimized Li2S(001)/SSE interfaces (5 panels) | sandwich, reactive interface |
| S12 | Optimized Li2S(111)/SSE interfaces (5 panels) | sandwich, less reactive |
| 3 | Initial vs 20 ps AIMD comparison — S(001)/SSE | **method visual + reaction sites** |
| 4 | Initial vs 20 ps — Li2S(001)/SSE | reaction sites highlighted |
| S19 | Reaction mechanisms with Bader |e| at Initial/Opt(0ps)/20ps for S(001)/SSE | atomic-resolution reaction tracking |
| S21 | Same for Li2S(001)/SSE | — |
| S23 | Same for Li2S(111)/SSE | — |
| 6 | Anion reaction summary (1)-(9) + Li2S(001)/LPSCl(001) interface schematic | **9-reaction master figure** |
| 7 | Time-averaged SSE charge per area, by interface | redox direction |
| 8 | Atomic species charge change % at 20 ps | element-by-element redox |
| Table S4 | Strain along a, b for cathode and SSE | **lattice match tolerance reference** |

---

## 7. Quantitative reference points for paper #2

1. **Wadh order of magnitude**: 1-2 J/m² for Li2S/LPSCl-type sulfide-cathode → matches our v5 v=1.28 J/m². Our number is in literature range.
2. **Strain tolerance**: 13% allowed in their largest case (S(001)/LPS(001) εb=13.2%). Our +3.3% is fine.
3. **Slab thickness lower bound**: 15 Å for cathode (Li2S), 19-22 Å for SSE. Ours: SE 29 Å ✓, NCM 1L too thin (7 Å); 5L 70 Å way over.
4. **Reaction timescale**: most chemistry in DFT-opt + first ~5 ps. Suggests 5-10 ps AIMD enough; 20 ps for safety.
5. **FixAtoms not used** — we are the outlier in literature on this.

---

## 8. Action items (linked to v10)

- [ ] Add `stack_v10_sandwich(se_slab, cath_slab, gap=2.1)` to `db/inputs/adhesion_templates/`
- [ ] Replace v9 `(E_sep-E_int)/A` with `(E_se+E_cath-E_int)/(2A)` for sandwich
- [ ] Drop FixAtoms; full relaxation
- [ ] (optional) Add 5-10 ps NVT AIMD at 300 K via UMA — test stability vs known UMA-MD failure modes (refer to `kb/results/adhesion_troubleshooting.md` items 19-21)
- [ ] Cite this paper as method precedent in paper #2 Methods section
- [ ] Compare: their LPSCl/Li2S(001) = 1.44 J/m² ⟷ our comp1/NCM v10 result

---

#literature #must-read #paper2 #adhesion #sandwich #wadh #LPSCl #camacho-forero #2020

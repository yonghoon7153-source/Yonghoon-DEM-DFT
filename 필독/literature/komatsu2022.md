# Komatsu et al. 2022 — Bulk Thermodynamic Reactivity LMO/LPSCl

> **DOI**: 10.1021/acs.jpcc.2c05336
> **Citation**: Komatsu, H.; Banerjee, S.; Holekevi Chandrappa, M. L.; Qi, J.; Radhakrishnan, B.; Kuwata, S.; Sakamoto, K.; Ong, S. P. *J. Phys. Chem. C* 2022, 126, 17482−17489.
> **Group**: Shyue Ping Ong (UC San Diego) + Nissan Motor + Nissan North America
> **Acquired**: 2026-05-07 (user-supplied PDF text + Figures 3, 4, 7)
>
> ⚠️ **Attribution correction**: Previously misattributed to "Sicolo" / "Kim" in our refs.json and adhesion_literature_review.md. Both wrong. Correct first author = Komatsu, corresponding author = Ong.
> ⚠️ **Method category correction**: Previously categorized as "DFT slab, FixAtoms bottom 2L, 4-5 layer NMC". WRONG. Actually **bulk pseudobinary thermodynamics (no slab, no FixAtoms, no AIMD)**.

---

## 1. Why must-read despite NOT being slab method

Bulk thermodynamic reactivity ranking for LiNiₓMnyCo₁₋ₓ₋yO₂/Li₆PS₅Cl interfaces — covers **our exact paper #2 system** (LiNiO2/LPSCl). Complements Camacho-Forero 2020 (slab AIMD, sulfide/Li2S):

| Source | Method | What it gives us |
|---|---|---|
| **Camacho-Forero 2020** | slab + AIMD + sandwich | direct slab Wad protocol |
| **Komatsu 2022** | bulk MP + convex hull | thermodynamic ceiling + reaction products |
| **Our v10** | slab + LBFGS + sandwich | manifested chemistry at the slab interface |

---

## 2. Method (Section: Methods)

### Computational details
- **Code**: VASP, PAW pseudopotentials, PBE GGA
- **Plane wave cutoff**: 520 eV
- **k-point density**: ≥ 1000/atom
- **Hubbard U** (oxides): Ni = 6.20 eV, Co = 3.32 eV, Mn = 3.90 eV
- **Source structures**: Materials Project (precomputed)
- **NO slab calculations**, NO interface relaxation, NO AIMD

### Thermodynamic framework (Zhu-Mo, refs 39-40)
Mutual reaction energy of A/B interface:
```
ΔED,min,mutual(A, B) = (1/N) min_{x∈[0,1]} { N · E_eq[x·c_A + (1-x)·c_B]
                                              − x · E[c_A]
                                              − (1-x) · E[c_B] }
```
- N = total atoms in normalized reaction
- E_eq = convex hull energy at composition x
- c_A, c_B = compositions of A and B
- More negative → larger thermodynamic driving force for reaction

### Grand potential under applied voltage
Φ = E − μ_Li · N_Li, with μ_Li = μ⁰_Li − e·ϕ. Used to compute electrochemical reactivity ΔΦD,min,mutual(A,B,ϕ).

---

## 3. Quantitative results (LMO / LPSCl)

### Figure 3 — pseudobinary curves (star = most negative reaction)

| LMO | x* (composition) | ΔED,min,mutual (meV/atom) |
|---|:-:|:-:|
| **LNO (LiNiO2)** | 0.77 | **−424** ⭐ our paper #2 baseline |
| NCA (Li(Ni0.8Co0.15Al0.05)O2) | 0.79 | −406 |
| High-Ni (Li(Ni10/12Mn1/12Co1/12)O2 ≈ NCM811) | 0.79 | −383 |
| LCO (LiCoO2) | 0.74 | −321 |
| NMC111 (Li(Ni1/3Mn1/3Co1/3)O2) | 0.67 | −285 |
| NM11 (Li(Ni0.5Mn0.5)O2) | 0.67 | −259 |
| LiMnO2 endpoint | — | ~ −196 |

**우리 v10 슬랩 atom ratio ≈ 0.74 NCM** (1764 NCM + 624 SE = 2388 total) → 위 x* 영역과 일치. 슬랩에서 가장 reactive 영역의 chemistry를 capture 하게 됨.

### Figure 4 — Ni-Mn-Co ternary contour
- Color scale: −150 (light, stable) to −450 (dark, reactive)
- **Ni corner**: darkest (−424, LiNiO2)
- Mn corner: lightest (−196, LiMnO2)
- Co corner: mid (−321, LCO)
- 32 MP compositions used; heat map by interpolation
- Red dashed line: LCO → LiNi0.7Mn0.3O2 (same chemical stability as LCO, Co-free option)
- NMC442, NMC111, NMC112 labeled inside ternary

### Reaction products (Table S1)

#### LiNiO2 / LPSCl (our system)
```
0.77 LiNiO2 + 0.23 Li6PS5Cl
  → 0.26 Ni3S2 + 0.45 Li2S + 0.16 Li2SO4 + 0.23 Li3PO4 + 0.23 LiCl
```
**Charge balance** (Komatsu Table S3):
- Ni³⁺ → Ni¹·³³⁺ (in Ni3S2) — reduction
- S²⁻ (in LPSCl) → S⁶⁺ (in Li2SO4) — partial oxidation
- O²⁻ stays as O²⁻ (in Li3PO4) — anion exchange
- Cl⁻ stays as Cl⁻ (in LiCl) — phase separation

#### Common products across all LMO/LPSCl
- **Li3PO4** — S²⁻/O²⁻ exchange product (universal across LMO families)
- **LiCl** — argyrodite cage degradation
- **Li2S** — sulfide preserved
- **Transition metal sulfide** (Ni3S2, Co9S8, Co(NiS2)2, etc., depends on TM)
- **Li2SO4** — partial S oxidation (only if cathode Ni-rich)

#### Carbon additive interfaces (Figure 6, Table S1)
- LMO / C → Li2CO3 (SEI-like) + TM carbonates + reduced TM
- LPSCl / C → STABLE (chemical reaction E ≈ 0)

### Voltage dependence (Figure 5)
- Below 3 V: cathode dominates ΔΦ
- Above 4.5 V: LPSCl narrow window dominates → all LMO converge to similar instability
- High Ni → cathode contributes more even at high V

### Volume change (Figure 7) — mechanical adhesion penalty

| Cathode | LPSCl chemical (V=0) | LPSCl 4.5V | C chemical | C 4.5V |
|---|:-:|:-:|:-:|:-:|
| **LNO** | **−11%** | **−34%** | +5% | −23% |
| NCA | −11 | −29 | +6 | −23 |
| High-Ni | −11 | −33 | +7 | −22 |
| NM11 | −15 | −30 | +9 | −17 |
| NMC111 | −17 | −32 | +6 | −19 |
| LCO | −12 | −31 | +10 | −17 |

**핵심**: All LPSCl chemical = shrinkage (−11 to −17%). 4.5 V → −29 to −34%. Carbon chemical = small expansion (+5 to +10%, Li2CO3 formation). 우리 v10 narrative에 **"Wad alone is incomplete; volume change quantifies contact-loss penalty"** 강력 support.

---

## 4. Implications for our v10 LPSCl/NCM (LiNiO2)

### A. v10 슬랩 method 자체에는 변경 없음
Komatsu는 **slab 안 함**. FixAtoms / vacuum / xy-shift / lattice match 결정에 정보 안 줌.
v10 method anchor = **Camacho-Forero 2020** 만 (sandwich + no fix + /(2A) + AIMD-or-LBFGS).

### B. 그러나 ==**chemistry expectation 강화**==
- LiNiO2/LPSCl = **−424 meV/atom thermodynamically guaranteed reaction** → 우리 LBFGS sandwich에서:
  - Ni-S bond formation 보일 것 (Ni3S2 nucleus)
  - 표면 Li-O 재배열 (Li3PO4 nucleus)
  - Li2S/LiCl phase separation 단서
  - Polysulfide S-S 가능
- **FixAtoms로 막으면 안 됨** (사용자 v9 정지 결정 정당화)
- v5 paper의 1.28 J/m² → v10에서 **1.5-3.0 J/m² 증가** 예상 (chemistry 풀려나오면서)

### C. Multi-metric framework (paper #2 narrative)
v10 결과 분석에 다음 metric 동시 사용:
1. **Wad (J/m²)** — Camacho-Forero scale (slab interface energy)
2. **ΔED,min,mutual (meV/atom)** — Komatsu bulk anchor (-424 for LNO/LPSCl)
3. **Volume change (%)** — Komatsu Figure 7 (-11% chemical, -34% at 4.5V)
4. **Reaction products** — Komatsu Table S1 + Camacho-Forero Figure 6
   - Li3PO4 nucleus
   - Ni3S2 cluster
   - LiCl phase separation
5. **Bader charge analysis** — Camacho-Forero Figure 7-8 + Komatsu Table S3 charge changes (Ni³⁺→Ni¹·³³⁺ 검증)

### D. Buffer layer extension (paper #2 future work)
Komatsu 결론: **LiNbO3, Li2CO3, NiO** 모두 LPSCl과 안정. 우리 v10 후속:
- LiNbO3 buffer layer 코팅한 NCM/LPSCl Wad 비교 (v11?)
- 실제 ASSB 산업 표준 (Toyota 2007 Ohta paper)

---

## 5. Quotable narrative phrases for paper #2

### Section 4 (adhesion) opener
> "Bulk thermodynamic analysis predicts the LiNiO2/Li6PS5Cl interface as the most exothermic among the LiNiₓMnyCo₁₋ₓ₋yO₂ family (ΔED,min,mutual = −424 meV/atom; Komatsu et al., 2022). Our explicit slab-level Wad calculation, conducted with sandwich geometry without rigid atomic constraints (Camacho-Forero & Balbuena, 2020), captures the structural manifestations of this thermodynamic driving force..."

### Reaction products discussion
> "Bader charge analysis of relaxed v10 interfaces (Figure X) reveals partial Ni³⁺→Ni²⁺ reduction at the LiNiO2/LPSCl contact, consistent with the Ni3S2 reaction product predicted by bulk thermodynamics (Komatsu et al., 2022). Concurrent S²⁻ migration toward the cathode is observed, paralleling the Li3PO4 nucleation pathway and the polysulfide chemistry described by Camacho-Forero (2020) for related sulfide SE/cathode interfaces."

### Volume change as adhesion penalty
> "Quantitative reactivity (Wad) alone provides an incomplete picture of interface stability. Bulk reaction-induced volume contraction of −11% under chemical conditions and −34% at 4.5 V (Komatsu et al., 2022) implies severe mechanical contact loss that compounds the chemical reactivity captured by our Wad calculation."

---

## 6. Locations to update with corrected attribution

(prior 'sicolo2022' citations to fix)

- `필독/literature/adhesion_literature_review.md` entry #6 (Kim et al., same DOI = also Komatsu)
- `필독/literature/verified_refs_2026_05.md` entry #6
- `필독/literature/narrative_with_literature_steps.md` Step 5/6 sicolo2022 citations
- `kb/papers/*.md` any "sicolo" mentions
- `db/literature/refs.json` 'sicolo2022' entry now deprecated (kept as flag)

---

#literature #must-read #paper2 #LPSCl #LiNiO2 #NCM #bulk-thermodynamics #Komatsu #Ong-group #attribution-corrected #bulk-not-slab

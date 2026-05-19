# B2O3 Doping in LPSCl1.6 (BO-LPSC) — Chemistry Framework

**작성일**: 2026-05-19
**상태**: pre-enumeration design doc, awaiting lpscl16_verify champion
**대상**: paper #2 (BO-LPSC1.6, follow-up to paper #1 modelC family)

---

## 1. Question — B-at-P substitution은 정당한가?

User paper #2 Figure 1b는 "BO incorporation into the argyrodite framework"로
**B at 4b (P site) + O at 16e (PS4 corner S site)** 명시.

이 doping mechanism이 literature-supportable한지 확인.

---

## 2. Literature evidence — B-at-P substitution

### 2.1 Direct precedent: β-Li3PS4-B (sulfide system, 가장 가까운 analog)

US Patent 9142861 (Lithium ionic conductor, Li-P-B-S):
- Composition: **Li_{3+3/4x} B_x P_{1-3/4x} S4** (0.2 ≤ x ≤ 1.0)
- Crystal structure: β-Li3PS4 (orthorhombic Pnma)
- BS4 and PS4 tetrahedra coexist at 4b positions
- Charge compensation: 0.75 Li interstitial per B substitution
  (B³⁺ at P⁵⁺ → -2 acceptor; partial substitution averages to 0.75)

### 2.2 Si-analog argyrodite (Morscher 2024, 2022)

**Sulfide**: Li6+xP1-xSixS5Br ([PMC10911230](https://pmc.ncbi.nlm.nih.gov/articles/PMC10911230/))
- Si⁴⁺ at P⁵⁺ 4b site (confirmed XRD/NMR Rietveld)
- 1 Li interstitial per Si (acceptor +1)
- σ_Li enhanced by Li disorder

**Oxide**: Li6+xP1-xSixO5Cl ([JACS 2022](https://pubs.acs.org/doi/10.1021/jacs.2c09863))
- Full oxide argyrodite (all S → O)
- Si at P + O at S simultaneously
- σ_Li = 1.82×10⁻⁶ S/cm at x=0.75 (3 orders better than prior oxide argyrodites)
- 4 Li site disorder unlocked (T5, T5a, T3, T4 all partially occupied)

### 2.3 NASICON-type B@P (oxide phosphates, less direct but supportive)

**LATP + B2O3** ([RJIC 2024](https://link.springer.com/article/10.1134/S0036023624603271)):
- Li1.2Al0.2Zr0.1Ti1.7(PO4)3 + 2% B2O3 → σ = 2.9×10⁻⁴ S/cm (highest)
- **B2O3 precursor → P substitution** (direct relevance to user's chemistry)

**Na-V phosphate** ([PMC5157167](https://pmc.ncbi.nlm.nih.gov/articles/PMC5157167/)):
- Na3V2(P1-xBxO4)3 — B at P site with charge compensation
- Demonstrates aliovalent B substitution at P in phosphate framework

### 2.4 BS4 tetrahedral unit in Li2S-B2S3 glass (chemistry support)

- Raman 495 cm⁻¹ peak assigned to BS4 ([Sakai 1994](https://www.sciencedirect.com/science/article/abs/pii/0022309394900345))
- B prefers tetrahedral (sp³) coordination in sulfide environment
- B-S bond length 1.93 Å (typical)
- → B at tetrahedral P site (4b, PS4 framework) chemically natural

### 2.5 Control: B at Cl site (alternative mechanism, also literature-confirmed)

- LiBH4 (borohydride) doping: BH4⁻ at Cl⁻ 4d site
- [Wang 2025 Adv Mater](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.202506095) — anion substitution mechanism
- [Hu 2022 ACS AEM](https://pubs.acs.org/doi/10.1021/acsaem.1c02892) — Li6PS5Cl1-x(BH4)x
- σ_Li 0.12 mS/cm at x=0.1

**Note**: BH4 ≠ B³⁺. BH4 is molecular anion (B-H bonded unit), behaves as halide
analog. Our B2O3 precursor releases **bare B³⁺**, which prefers cation site.

---

## 3. Conclusion — B-at-P for argyrodite-Cl

| Question | Answer | Evidence strength |
|---|---|---|
| B³⁺ can substitute P⁵⁺ tetrahedrally? | **YES** | β-Li3PS4-B + Si-analog + NASICON + BS4 glass |
| In argyrodite framework specifically? | **PLAUSIBLE, novel for Cl-argyrodite** | Si-analog (S5Br + O5Cl) but no B-specific Cl-argyrodite paper |
| Charge compensation mechanism? | **Li interstitial OR vacancy-fill** (LPSCl1.6 has 0.6 vac/fu pre-existing) | β-Li3PS4-B + Morscher Si analog |
| Alternative B at Cl site? | Possible (BH4-style) but for B2O3 precursor unlikely (bare B³⁺ ≠ BH4⁻ molecular) | Wang 2025 LiBH4 paper |

**Verdict**: B-at-P in argyrodite-Cl is chemistry-supportable, novel mechanism
building on solid analog precedents. Paper #2의 핵심 claim으로 promotable.

---

## 4. Key insight — pre-existing vacancy advantage

**LPSCl1.6's Li5.4 stoichiometry (0.6 Li vacancy per fu) is advantageous for
B2O3 doping** vs Si@P Morscher (Li6 base, no vacancy).

### 4.1 Charge accounting per 1 B2O3 unit (10 fu cell, 124 atoms)

Pre-doping modelC × 1×1×2: Li54 P10 S44 Cl16
- Stoichiometric Li6PS5Cl × 10 fu = Li60 P10 S50 Cl10
- LPSCl1.6 has 6 S → 6 Cl (halogen-rich) + 6 Li vacancies (charge balance)

Add 1 B2O3 unit:
- 2 P → 2 B at 4b: -4 charge (acceptor)
- 3 S → 3 O at 16e: 0 charge (isovalent)
- **Need +4 → fill 4 of 6 existing Li vacancies**
- No true Li interstitial needed!

Post-doping: **Li58 P8 B2 S41 O3 Cl16** (2 Li vacancies remaining)
- Per fu: Li5.8 P0.8 B0.2 S4.1 O0.3 Cl1.6

### 4.2 Why this is better than Morscher Si@P (Li6 base)

Morscher Li6+xP1-xSixS5Br must create true Li interstitials at non-host positions
(T5, T3, T4 sites — generally higher-energy positions). This raises:
- Synthesis difficulty (kinetic barrier for Li insertion)
- Reviewer concern about structural validity (where exactly is interstitial Li?)

LPSCl1.6 avoids this entirely: existing 4a/4d/24g vacancies absorb the extra Li.

**Paper #2 selling point**:
> "The Cl-rich Li5.4 stoichiometry of modelC provides natural sites for charge
> compensation under aliovalent acceptor doping, removing the need for
> high-energy Li interstitial positions required in Li6 baseline materials."

---

## 5. Doping site enumeration

### 5.1 B placement at 4b (P site)

10 fu cell has 10 P atoms. Choose 2 for B:
- **C(10,2) = 45 B-B pair configurations**
- Distance between 2 B atoms varies (close pair vs far pair)
- B-B short distance might destabilize (electrostatic + steric)
- B-B far → "isolated dopant" limit

### 5.2 O placement at 16e (PS4 corner S)

10 fu cell has 44 S total = 40 PS4-corner-S + 4 free-S.
Choose 3 for O substitution:
- **C(44,3) = 13,244 total positions** if no chemistry bias (user's choice)
- C(8,3) = 56 if restricted to "near-B PS4 corners" (Hard-Hard bias, Nd-doped style)

### 5.3 Li vacancy distribution

After B2O3 doping: 2 vacancies remaining (was 6, B2O3 filled 4).
- Which 4 of 6 to fill: C(6,4) = 15
- Which 4a/4d/24g/48h Li site type: depends on UMA relax energetics

### 5.4 Total enumeration (no chemistry bias)

- 45 B pairs × C(44,3)=13,244 O positions × C(6,4)=15 Li fills = **8.94 million configs**
- Computationally absurd at full enumeration
- → **hierarchical screening** required (Stage 1 sample/select → Stage 2 refine → Stage 3 anneal)

### 5.5 Recommended hierarchical strategy

| Stage | Configs | Method | Time (1 GPU) |
|---|---|---|---|
| 1a — B pair only (1 random Li, 3 O random) | 45 | SCF single-point | ~10 min |
| 1b — Top 5 B pairs × full O enumerate × 1 random Li | 5 × 13,244 = 66,220 | SCF | ~12 h |
| 1c — Top 100 (B, O) × 15 Li fills | 100 × 15 = 1500 | SCF | ~30 min |
| 2  — Top 50 LBFGS relax | 50 | LBFGS fmax 0.05 | ~5 h |
| 3  — Top 5 MD anneal 500K 100ps | 5 | Langevin + LBFGS | ~3 h |
| **Total** | | | **~20 h** |

(Stage 1b is the bottleneck; can downsample to ~1000 random O placements
to drop to ~2 h if needed.)

---

## 6. Computational checklist before script generation

- [x] Literature confirms B-at-P chemistry
- [x] Si-analog precedent (Morscher 2024) verified
- [x] Charge balance accounting (vacancy-fill mode) derived
- [x] Enumeration scope (~9M configs) — hierarchical needed
- [ ] **lpscl16_verify champion** ready (gabia, ~22h after Li2O cascade ends)
- [ ] B2O3 enumerate script (lpscl16_champion + structure)
- [ ] DFT settings for B-doped LPSCl (likely same as Nd-doped but no ISPIN/U
      since B has no f-electrons)

---

## 7. References

- US Patent 9142861 — Lithium ionic conductor (Li-P-B-S, β-Li3PS4-B)
- Morscher et al., JACS 2022, 144:23, [10.1021/jacs.2c09863](https://pubs.acs.org/doi/10.1021/jacs.2c09863) — Li7SiO5Cl oxide argyrodite
- Morscher et al., Adv. Energy Mater. 2024, [PMC10911230](https://pmc.ncbi.nlm.nih.gov/articles/PMC10911230/) — Li6+xP1-xSixS5Br sulfide argyrodite
- Wang et al., Adv. Mater. 2025, [10.1002/adma.202506095](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.202506095) — LiBH4-LPSCl (Cl site, not P)
- Hu et al., ACS Appl. Energy Mater. 2022, [10.1021/acsaem.1c02892](https://pubs.acs.org/doi/10.1021/acsaem.1c02892) — Li6PS5Cl1-x(BH4)x
- Sakai et al., J. Non-Cryst. Solids 1994 — Li2S-B2S3 glass BS4 Raman
- Russ. J. Inorg. Chem. 2024 — LATP + B2O3 conductivity
- PMC5157167 — Na3V2(P1-xBxO4)3 cathode

---

## 변경 이력

| 날짜 | 변경 | 출처 |
|---|---|---|
| 2026-05-19 | v1 초안 (literature search + chemistry framework) | this session |
| (TODO) | enumerate script 생성 후 §5 update | future |
| (TODO) | lpscl16_verify champion 결정 후 §6 first checklist 완료 | future |

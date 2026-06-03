# Paper Figure / Table Plan — LPSCl vs LPSCl1.6 v3

진행 상황 정리 + paper figure / table 후보 + 캡션 초안.

마지막 업데이트: 2026-06-03

## 진행 상태 매트릭스

| §8 항목 | LPSCl (comp1_v3) | LPSCl1.6 (modelc_v3) | paper 활용 |
|---|---|---|---|
| 8a V0 relax | ✓ 1016.62 Å³ | ✓ 1216.44 Å³ | foundation |
| 8b/c/d bond/coord/Voronoi | ✓ | ✓ | Table 1 |
| 8d' per-site (4a/4d Cl, Li env) | ✓ 1 unique | ✓ 6 unique | Fig 2 |
| 8e BVSE (62/65 fu + 5×5×5 cubic) | ✓ ch frac 9.84% | ✓ ch frac 3.33% | Fig 3 |
| 8f Bader (AE plot_num=17) | **pending** | ✓ Li +0.882, Cl −0.916 | Table 2 |
| 8g DOS / PDOS | **pending** | ✓ Eg=1.80 eV | Fig 4 |
| 8h Bands (Hungarian) | **pending** | ✓ | Fig 4 |
| 8i Cij clamped-ion | ✓ E=52.31 | ✓ E=52.30 | (paradox setup) |
| 8i' Cij **relaxed-ion** | ✓ **E=22.33** (실험 ~23 ✓) | **GPU 진행 (3/12, ~22:30)** | **Fig 5 main result** |
| 8j MLIP UMA 600K | **pending** | ✓ E=52.72 | Fig 5 |
| 8k AIMD 600/800/1000K | **pending (5 fu input ready)** | ✓ Ea=0.224 eV | Fig 6 |
| 8l ELF | **pending** | ✓ | Fig SI |
| 8m LOBSTER ext basis | ✓ spilling 1.46% | ✓ spilling 1.16% | **Fig 1** |

## Main Figures (paper main body)

### Fig 1 — LOBSTER COHP (4-panel × 2 systems)

```
┌──────────────────────────────┬──────────────────────────────┐
│  LPSCl (a-d, ext)            │  LPSCl1.6 (a-d, ext)         │
│  P-S│S-S│Li-S│Li-Cl          │  P-S│S-S│Li-S│Li-Cl          │
│  ICOHP boxes                 │  ICOHP boxes                 │
└──────────────────────────────┴──────────────────────────────┘
```

**Caption draft**:
> "Crystal orbital Hamilton population (pCOHP, paper-grade extended
> basis, charge spilling <1.5%) for four representative bond classes
> in (top row) stoichiometric LPSCl and (bottom row) vacancy-bearing
> LPSCl1.6. The 4d-Cl anti-site site in LPSCl1.6 produces a distinct
> deeper bonding peak around −5 eV in panel d (Li–Cl), absent in LPSCl
> where all Cl atoms occupy the 4a octahedral site. Per-bond ICOHP
> integrals (boxes) quantify that ALL ionic bonds (Li–Cl +13.4%,
> Li–S +7.9%) are stronger in LPSCl1.6, while the covalent PS4
> backbone is unaffected (P–S +0.9%)."

소스: `cohp_ext_compare/{comp1,modelc}_V0_COHP_4panel_ext.png`

### Fig 2 — 결합환경 정량 (Per-site bonding)

3-panel: bond length histogram, Voronoi volumes, Li environment type distribution.

| panel | content |
|---|---|
| a | Li-Cl bond length histogram (LPSCl: 24 bonds at 2.61 ± 0.13. LPSCl1.6: 36 4a-Cl at 2.55 + 4 4d-Cl at 2.36) |
| b | Voronoi volume per species (LPSCl: 19.56/14.05/20.14/22.06. LPSCl1.6: 20.51/13.99/19.55/20.31) |
| c | Li environment type counts (1 vs 6 unique types) |

**Caption draft**:
> "Local structure differences. (a) Li–Cl bond length distribution
> showing 4d-Cl anti-site contribution (LPSCl1.6 only, 2.36 ± 0.04 Å);
> (b) species-resolved Voronoi polyhedral volumes — Cl polyhedra shrink
> by 1.7 Å³ in LPSCl1.6 due to anti-site mixing; (c) coordination-shell
> environment types per Li site, increased from one (LPSCl) to six
> (LPSCl1.6) by vacancy-induced disorder."

소스: 비교 doc §5, structural analysis §5–6

### Fig 3 — BVSE Li channel topology

2-panel cubic supercell visualization:
- panel a: LPSCl 5×5×5 BVSE iso surface (low-BVSE channel)
- panel b: LPSCl1.6 5×5×5 BVSE iso surface (more sparse)

**Caption draft**:
> "Bond-valence site-energy (BVSE) low-energy channel surface for Li
> migration in (a) LPSCl and (b) LPSCl1.6 5×5×5 supercells. The
> static channel volume (BVSE ≤ min + 0.5) drops from 9.84% (LPSCl)
> to 3.33% (LPSCl1.6) despite the formal addition of Li vacancies.
> This counter-intuitive static-channel contraction is recovered by
> finite-T atomic motion in AIMD (Fig 6)."

소스: `bvse_5x5x5_compare/{comp1,modelc}_V0_BVSE_iso_min030.png` (또는 VESTA cube)

### Fig 4 — Electronic structure (DOS + Bands) — pending comp1

```
┌──────────────┬──────────────┐
│ DOS / PDOS   │ Band along   │
│ LPSCl/LPSCl1.6│ X-Γ-L-W-K   │
└──────────────┴──────────────┘
```

(comp1 DOS/bands 아직 — modelc_v3는 ✓.)

### **Fig 5 — Vacancy paradox (Cij + experimental comparison)** ⭐ paper main message

|  | comp1 | modelc_v3 | 실험 LPSCl | 실험 LPSCl1.6 |
|---|---|---|---|---|
| clamped-ion DFT E_VRH | 52.31 | 52.30 | — | — |
| **relaxed-ion DFT E_VRH** | **22.33** | **TBD (~22:30)** | ~23 | LPSCl1.6 > LPSCl |
| MLIP 600K snapshot | pending | 52.72 | — | — |

bar chart 또는 grouped bar로 시각화. relaxed-ion 결과가 vacancy paradox 결정:
- modelc_v3 relaxed-ion E_VRH > 22.33 → paradox **해소**: DFT가 실험 추세 잡음
- ≈ 22.33 → 작은 차이지만 finite-T 효과 추가 필요
- < 22.33 → ion-relaxation도 부족, MLIP 600K + AIMD가 답

**Caption draft (TBD-마지막)**:
> "Mechanical response under different DFT protocols. Clamped-ion
> stress-strain (left bars) over-estimates the Young's modulus by
> ~2.3× and yields nearly identical values for both compositions —
> the apparent 'vacancy paradox'. Allowing ionic relaxation under
> strain (middle bars) recovers experimentally consistent values
> (LPSCl 22.33 GPa vs literature ~23 GPa) and [resolves/maintains —
> TBD] the experimental Young's modulus difference. Finite-T MLIP
> snapshots at 600 K (right) capture additional anharmonic stiffening
> [TBD]."

### Fig 6 — Li transport (AIMD Arrhenius) — pending comp1

X = 1000/T, Y = log D. Two lines (LPSCl, LPSCl1.6), Arrhenius fit, Ea extracted.

## Tables (paper main body)

### Table 1 — Local structure summary

| Property | LPSCl | LPSCl1.6 |
|---|---|---|
| Composition | Li6PS5Cl (4 fu) | Li5.4PS4.4Cl1.6 (5 fu) |
| V0 (Å³) | 1016.62 | 1216.44 |
| V/atom (Å³) | 19.55 | 19.62 |
| V/fu (Å³) | 254.16 | 243.29 (−4.3%) |
| d(P–S) (Å) | 2.073 ± 0.036 | 2.064 ± 0.011 |
| d(Li–S) (Å) | 2.461 ± 0.106 | 2.465 ± 0.094 |
| d(Li–Cl, all) (Å) | 2.607 ± 0.129 | 2.532 ± 0.119 |
| d(Li–Cl, 4a) (Å) | 2.607 (all) | 2.551 |
| d(Li–Cl, 4d) (Å) | — | **2.359** |
| 4d-Cl anti-site fraction | 0% | 12.5% (1/8) |
| Li environment types | 1 unique | 6 unique |

### Table 2 — Mechanical + electronic + bonding summary

| Quantity | LPSCl | LPSCl1.6 | Expt |
|---|---|---|---|
| B0 (BM-EOS, GPa) | 26.23 | 21.71 | — |
| E_VRH clamped-ion (GPa) | 52.31 | 52.30 | — |
| **E_VRH relaxed-ion (GPa)** | **22.33** | **TBD** | LPSCl ~23 |
| E_VRH MLIP 600K (GPa) | pending | 52.72 | — |
| Band gap (PBE, eV) | pending | 1.80 | — |
| Bader q(Li) (e) | pending | +0.882 | — |
| Bader q(Cl) (e) | pending | −0.916 | — |
| ICOHP P–S (eV/bond) | −5.944 | −6.000 | — |
| ICOHP Li–Cl (eV/bond) | −1.855 | **−2.103** | — |
| ICOHP Li–S (eV/bond) | −1.592 | **−1.717** | — |
| AIMD Ea (eV) | pending | 0.224 | 0.22–0.30 |

## SI (Supplementary) Figures

- SI Fig S1: 2D BVSE slices (3-axis × 2 systems), small fu cells
- SI Fig S2: ELF (ELF=0.85 iso + 2D slices), modelc_v3 only currently
- SI Fig S3: clamped-ion vs relaxed-ion Cij eigenvalue ratios
- SI Fig S4: per-Cl-atom ICOHP detail (4a vs 4d split)

## Paper outline에서 figure 배치

| Section | Figure / Table |
|---|---|
| Intro | (literature) |
| Methods | (pipeline schematic) |
| Results §1 Local structure | **Fig 1 (COHP), Fig 2 (per-site), Table 1** |
| Results §2 Channel topology | **Fig 3 (BVSE)** |
| Results §3 Electronic structure | Fig 4 (DOS/bands) |
| Results §4 Mechanical | **Fig 5 (vacancy paradox)** ⭐ |
| Results §5 Li transport | Fig 6 (AIMD) |
| Discussion | Table 2 (summary) |

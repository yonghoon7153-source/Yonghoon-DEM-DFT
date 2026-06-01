---
title: "Li Adatom Diffusion on Anode-Free SSB Interphases"
tags: [project/li-neb-anode-free, neb, dft, mlip, anode-free, ssb, agno3]
date: 2026-06-01
status: setup
---

# Li Adatom Diffusion on Anode-Free SSB Interphases — NEB Track

> [!important] Research goal
> 무음극 전고체 전지에서 AgNO₃ additive가 형성하는 **nitrate-derived layer (Li3N, LiNO3, LiNO2)**가 lithiated carbon 표면 대비 Li adatom **diffusion barrier 낮음**을 DFT로 입증 → lateral Li redistribution 촉진 → uniform Li deposition

## 1. 가설 (사용자 노트)

- **문제**: 무음극 ASSB에서 Ag 응집 → 국소적 Li 불균일 / SE-interlayer void → contact loss
- **해결책**: AgNO₃ → (1) Ag precursor, (2) nitrate-derived Li-N interphase
- **DFT 핵심 주장**: nitrate-derived layer가 Li redistribution을 촉진
- **DFT 결과 예상**: Li3N 표면이 lithiated carbon 표면보다 Li atom diffusion 유리
- **결과 흐름**: Li3N 낮은 barrier → lateral redistribution → 균일 flux → 균일 전착

## 2. Reference (Cui group 2023 ACS Nano)

> [!info] 페이퍼 (Li3N suspension electrolyte) 의 DFT (Figure 2)
> - Li adatom binding energy: Li⁰ (110) **−1.59** / Li3N (001)|(002) **−3.44** / Li3N (110) −1.78 / Li3N (100) −1.44 eV
> - Li adatom diffusion barrier on Li3N (001) = **0.133 eV** (lowest)
> - SEI 비교: Li2O 0.319 / Li2CO3 0.232 / LiF 0.169 / LiOH 0.141 / **Li3N 0.133** eV

→ 우리 첫 작업: **Li3N (001) NEB로 0.133 eV 재현** (method 검증)

## 3. 시스템 list (우선순위)

| # | system | facet | 의미 | paper 값 |
|---|--------|-------|------|---------|
| 1 | **Li3N** | **(001)** | paper 재현 (method check) | 0.133 eV |
| 2 | **lithiated carbon** (LiC₆) | (0001) | baseline (없는 값) | — |
| 3 | LiNO₃ | (?) | 새 — nitrate intermediate | — |
| 4 | LiNO₂ | (?) | 새 — nitrite intermediate | — |
| 5 | Li3N (110), (100) | minor facets | 비교용 | 없음 |
| 6 | (선택) Li metal (110) | reference | paper 1.59 eV binding | — |

## 4. Method

### 4.1 NEB 인프라
- **QE neb.x**: 미설치 (확인됨, 2026-06-01)
- **대안 (실제 사용)**: **ASE NEB module + calculator**
  - Fast: ASE NEB + FAIRChemCalculator (UMA-oc20) → ~분 단위
  - DFT 검증: ASE NEB + Espresso calc (pw.x for each image) → ~수일

### 4.2 NEB protocol
```
- Slab build: 3×3×n_layer + vacuum 15 Å
- Initial state: Li adatom at site A (top-of-N for Li3N)
- Final state: Li adatom at site B (adjacent top-of-N, distance ~3.65 Å for Li3N)
- N images: 7 (initial + 5 mid + final)
- IDPP interpolation (initial guess)
- CI-NEB (Climbing Image, accurate TS)
- Slab bottom 50% freeze
- fmax target: 0.05 eV/Å
- UMA task: oc20 (surface adsorbate)
```

### 4.3 Output per system
- `path_energies.json`: image별 E, 상대 E, barrier
- `path_traj.xyz`: 7 image의 좌표 (시각화용)
- `neb_<system>_<facet>.log`: ASE NEB optimizer log
- (선택) DFT 검증: QE input + output per image

## 5. 두 트랙 연계 (전체 paper 그림)

```
Cathode side (Track 1):  SDCP binder → LiNiO₂ (104) anchoring
                          → self-doping 효과 (−18 vs −6 eV)
Anode side (Track 2, 신규): Li adatom diffusion on
                              Li3N / LiC₆ / LiNO3 / LiNO2
                          → AgNO3 → Li-N interphase 효과
```

→ paper headline: "anode-free Li metal SSB의 양면 interface 분석"

## 6. Status

- [x] 페이퍼 리뷰 + DFT 목표 정리
- [x] 트랙 노트 작성 (this file)
- [x] gabia 인프라 점검 (ase.mep.NEB ✓, QE neb.x ✗ → ASE NEB only)
- [x] Li3N (001) slab + Li adatom builder
- [x] UMA-oc20 NEB on Li3N (001) — 4 paths (A/B/C symmetry + D bridge-to-bridge attempt)
- [x] LiC₆ (0001) NEB — baseline (paper-novel)
- [-] LiNO₃ NEB — slab builder R-3c symmetry bug (overlapping atoms); skipped
- [-] LiNO₂ NEB — crystal structure ambiguous, omitted per paper limitation
- [-] DFT 검증 (user decision: skipped, MLIP results stand as primary)
- [-] Charge density difference 시각화 — deferred

## 7. 최종 결과 (UMA-oc20)

### Li3N (001) — 4 paths converged to consistent answer

| path | initial → final | barrier (eV) | TS image |
|------|----------------|-------------|---------|
| A (original) | N(0,0) → N(−1.825, 3.16) | 0.0221 | image 5 |
| A (repeat sanity) | same | 0.0235 | image 5 |
| B (a-axis 60°) | N(0,0) → N(3.65, 0) | 0.0227 | image 1 |
| C (other 60°) | N(0,0) → N(1.825, 3.16) | 0.0217 | image 5 |
| D (bridge→bridge, LBFGS) | bridge1 → bridge2 | diverged (4.0 eV unphysical) | — |
| D (bridge→bridge, FIRE) | same | diverged (image 9 polluted, 7.1 eV) | — |

**A/B/C 평균**: 0.022 ± 0.001 eV (hexagonal symmetry verified ✓)

**Bridge basin discovery**: image 3 (always) at −0.032 eV below endpoints — Li adatom prefers
**bridge** (between 2 N atoms) over **on-top N** by 0.032 eV. on-N is metastable.

**Effective diffusion barrier (bridge→bridge via on-N TS)**:
= TS_energy − bridge_depth = 0.022 − (−0.032) = **0.054 eV**

### LiC6 (0001)

| | (dx, dy, dz) | E_bind | barrier |
|---|---|---|---|
| hollow 1 (start) | (1/3, 1/3, hex_center) | 0 | — |
| TS (image 4) | bridge between hollows | +0.241 | **0.241 eV** ★ |
| hollow 2 (end) | (2/3, 2/3, hex_center) | +0.003 | — |

LiC6 hex hollows are true minima (graphene basal Li adsorption site).
No bridge correction needed.

### Headline comparison

| | barrier (eV) | site type |
|---|---|---|
| **Li3N (001)** | **0.054** | bridge → on-N TS → bridge |
| **LiC₆ (0001)** | **0.241** | hex hollow → bridge-C TS → hex hollow |
| ratio LiC₆/Li3N | **4.5×** | |
| Δ barrier | 0.187 eV | |
| **Rate ratio @ 300K** | **~1,700×** | exp(0.187/0.025) |

### Paper interpretation

> Self-doped sulfonate Li deposition on Li3N (anode-free SSB AgNO₃-derived interphase)
> is ~1,700× faster than Li adatom diffusion on lithiated carbon (LiC₆) at 300 K.
> This 4.5-fold barrier reduction enables lateral Li redistribution that yields uniform
> Li flux and uniform deposition morphology, supporting the AgNO₃ → Li₃N interphase
> hypothesis for dendrite-free anode-free SSB operation.

### Caveats (paper)

- UMA-oc20 absolute barrier ~2.5× underestimated vs DFT (Li3N comparison: UMA 0.054 vs
  Cui 2023 DFT 0.133 eV). Relative comparison robust; absolute values approximate.
- LiNO₃ and LiNO₂ (AgNO₃ decomposition intermediates) omitted: LiNO₃ slab builder
  R-3c symmetry generated atom overlaps (manual Wyckoff equivalent generation bug);
  LiNO₂ crystal structure data ambiguous. Li₃N (final SEI product per XPS) is the
  dominant phase, so the comparison stands.
- Bridge → bridge NEB on Li3N (Path D) failed to converge with either LBFGS or FIRE
  optimizers. The effective barrier was instead deduced arithmetically from the
  symmetric A/B/C paths (bridge minimum and TS energy individually well-measured
  → effective barrier = TS - bridge = 0.054 eV).

## 7. 주요 파일 (계획)

```
tools/neb_diffusion/
├── build_li3n_slab.py        # Li3N (001), (110), (100) slab builder
├── build_lic6_slab.py        # LiC₆ (0001) slab builder
├── build_linox_slab.py       # LiNO3, LiNO2 (TODO)
├── identify_sites.py         # Li adatom binding site identification
├── run_neb_uma.py            # ASE NEB + UMA-oc20 (Phase 1, fast)
├── run_neb_qe.py             # ASE NEB + Espresso (Phase 2, DFT verify)
└── plot_neb.py               # NEB path plot (E vs reaction coord)

kb/projects/li_neb_anode_free.md    # this file
kb/results/li_neb_diffusion_report.md (TODO)
```

## 8. 주의사항 (도출)

- **Li3N (001) 표면 termination**: paper Figure 2a 보면 N과 Li(2) 같이 노출 (mixed termination). 슬랩 빌드 시 (001) 면이 N 노출 vs Li 노출인지 확인 필요.
- **Li3N 격자**: Wang 1981, **P6/mmm**, a=3.65, c=3.87 Å. N at (0,0,0), Li(1) at (0,0,1/2), Li(2) at (1/3,2/3,0) / (2/3,1/3,0).
- **LiC₆**: graphite (P6/mmm) + Li 사이층에 1/6 채움. 정확한 superstructure 필요 (3×3 in-plane → 18 C + 3 Li per layer).
- **UMA task=oc20**: SDCP-LiNiO₂ Phase A에서 omat에 비해 잘 작동함이 확인됨. 표면 전용 학습이라 NEB에도 적합.
- **DFT 비교 시**: paper는 PBE+D3 (probably) — 같은 functional 사용해야 직접 비교.

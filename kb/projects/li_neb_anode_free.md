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
- [ ] Li3N (001) slab + Li adatom builder
- [ ] UMA-oc20 NEB on Li3N (001) — paper 0.133 eV 재현 시도
- [ ] LiC₆ (0001) NEB — baseline 새 값
- [ ] LiNO₃, LiNO₂ NEB — 새 값
- [ ] (선택) DFT 검증 — best path만 QE PBE+D3
- [ ] Charge density difference 시각화 (Li-surface bonding mechanism)

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

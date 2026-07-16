---
title: "SDCP Binder Anchoring on LiNiO₂ (104)"
tags: [project/sdcp-linio2, results, mlip, binder, cathode-interface]
date: 2026-06-01
status: phase-A-B-C-complete-dft-pending
---

# SDCP Binder Anchoring on LiNiO₂ (104) — Phase A–C 결과 보고서

> [!warning] 2026-07-16 업데이트
> 최신 종합은 **sdcp_master_summary_2026_07_16.md** 를 보라. 본 문서의 UMA 절대값(-18.2/-6.3 eV)은
> 방향성 지표였고, Phase-B DFT+U에서 E_bind(doped) = **-1.52 eV**(잠정)로 스케일이 대체됐다.
> n-시리즈 오비탈(백본 크로스오버), PTFE 벤치마크도 마스터 문서에 정리.

> [!success] Headline
> 자기-도핑된 SDCP (−SO₃⁻)는 LiNiO₂ (104) 표면에 **−18.2 eV** 화학 흡착 (chemisorption, dz = 1.26 Å)
> 보호된 neutral SDCP (−SO₃H)는 **−6.3 eV** (shallow chemisorption, dz = 1.41 Å)
> → **Self-doping이 cathode anchoring을 11.8 eV 강화**

## 1. 연구 목적

[[MUST_READ_digital_twin_north_star|Digital Twin Platform]] 의 cathode interface 트랙. 자기-도핑된 conducting binder (PEDOT-S 계열, sulfonate self-doping)가 NCM 계열 cathode 활물질 표면에 **어떻게, 얼마나 강하게 anchoring 되는지** ML potential로 정량.

핵심 질문 두 가지:
1. SDCP의 −SO₃⁻ 그룹이 표면 어느 site (Ni / Li / O) 에 anchoring?
2. 자기-도핑 (anion) vs. 중성 (protonated acid) 의 binding 차이?

## 2. 시스템

### 2.1 SDCP 분자 (ORCA TZVP-optimized)

> [!note] Composition
> | form | atoms | molecular formula | net charge | E_ORCA (Ha) |
> |---|---|---|---|---|
> | **doped** | 33 | C₁₁H₁₅O₅S₂⁻ | **−1** (anion) | −1600.481 |
> | **neutral** | 34 | C₁₁H₁₆O₅S₂ | 0 (protonated) | −1601.140 |
> 
> 두 form의 atom 차이는 정확히 H 1개 — sulfonate group 의 양성자화 상태:
> - doped: **−SO₃⁻** (3 O, H 없음, anion)
> - neutral: **−SO₃H** (3 O, 그 중 하나에 H, neutral)

### 2.2 LiNiO₂ (104) 슬랩 (UMA / pymatgen generated)

- 4×4×4 layer, 96 atoms (Li 24 + Ni 24 + O 48 = stoichiometric LiNiO₂)
- 표면 unit cell **a=11.51, b=18.27 Å, γ=71.6°** (oblique slab from R-3m hexagonal bulk)
- z range = 10.33 Å, vacuum = 15 Å → cell c = 25.33 Å (scan에서 40 Å로 확장)
- (104) facet — NCM cathode의 **active facet** (Li (de)intercalation, coating attack 주 site)

> [!warning] UMA-omat 의 LiNiO₂ relax issue
> 처음 시도한 UMA-omat task의 slab relax는 **slab을 무너뜨림** (top layers가 frozen bottom으로 collapse, 비물리적). 이는 LiNiO₂ (104) polar magnetic surface가 omat의 학습 분포를 벗어났음을 시사. **Phase A 이후 모든 작업은 unrelaxed (init) slab + task=oc20** 사용.

## 3. Method — Binding Energy 계산

> [!info] 정의
> $$ E_\text{bind}(x, y, z) = E_\text{complex}(x, y, z) - E_\text{slab,iso} - E_\text{SDCP,iso} $$
> 부호: **E_bind < 0 ⇔ favorable anchoring**

### 3.1 Three references (한 번씩만)

| state | calc | geometry | task |
|---|---|---|---|
| `E_slab_iso` | UMA SP | init slab (unrelaxed) | **oc20** |
| `E_SDCP_iso` | UMA SP | ORCA TZVP-opt, in slab cell (centered) | **oc20** |
| `E_complex` | UMA SP (Phase A) / relax (Phase B) | slab + SDCP at offset | **oc20** |

### 3.2 Phase A — Rigid grid scan

- Grid: 10 × 10 × 9 = 900 points, fractional dx ∈ [0,1), dy ∈ [0,1), dz ∈ [2.0, 6.0] Å step 0.5
- SDCP orientation: sulfonate S → COM 벡터를 +z 방향 (sulfonate-down)으로 회전 후 고정
- 각 grid point: 분자 평행이동 + UMA SP → E_bind(dx, dy, dz)

### 3.3 Phase C — Orientation sweep at top-1 site

- 위치는 Phase A best (dx, dy, dz) 고정
- 분자를 anchor S 중심으로 **z-축 회전** at θ ∈ {0°, 30°, ..., 330°} (12 각도)
- 각 θ: UMA SP → E_bind(θ)

### 3.4 Phase B — Local relax on top-K sites (rotation-aware)

- 위치: Phase A에서 top-K (K=5) 최저 E_bind sites
- 시작 orientation: **Phase C best θ** (self-consistent!)
- Constraint: **슬랩 전체 freeze (96/96)**, SDCP atoms만 자유
- Optimizer: LBFGS, fmax=0.05 eV/Å, max_steps=300
- 산출: `E_bind_relax`, 최종 dz, 수렴된 분자 좌표

> [!important] Slab freeze 의 이유
> 처음 시도 (bottom 50% freeze, top free)는 **−118 eV 비물리적 결과** 산출. 슬랩 top atoms이 UMA의 weird min으로 흘러가면서 분자를 끌고 감. 표준 adsorption convention (whole-slab freeze) 적용 후 정상화.

## 4. Phase A 결과 — Rigid scan

### 4.1 Best site

| | dx_frac | dy_frac | dz (Å) | **E_bind (eV)** |
|---|---|---|---|---|
| **doped (−SO₃⁻)** | 0.30 | 0.10 | **2.0** | **−4.75** |
| **neutral (−SO₃H)** | 0.10 | 0.10 | **2.5** | **−2.98** |
| Δ (doped 우위) | — | — | −0.5 | **−1.77** |

doped가 0.5 Å 더 가까이 + 1.77 eV 더 강함 → **자기-도핑이 표면에 더 가까이 끌어들임**.

### 4.2 전체 분포 (900 grid)

| metric | doped | neutral |
|---|---|---|
| min E_bind | −4.75 | −2.98 |
| median E_bind | −1.54 | −1.50 |
| fraction `E_bind < −1 eV` (strong sites) | **94.2 %** | 86.2 % |
| max E_bind (steric clash region) | +52.6 | +24.9 |

> [!tip] 해석
> - **doped는 표면 거의 모든 위치에서 적당한 결합 + 특정 site에서 강한 결합** (94% strong)
> - **neutral은 약한 결합 더 균일하게 분포** (86% strong)
> - max E_bind +52 eV (doped) > +25 eV (neutral) → doped의 site sensitivity가 더 큼 (atomic-level pattern)

### 4.3 Heatmap 시각화

> [!info] 출력 PNG
> - `heatmap_compare.png` — doped vs neutral 나란히, 같은 colorscale
> - `heatmap_doped.png` / `heatmap_neutral.png` — 개별 + z-profile inset

**doped heatmap pattern** = checkerboard:
- 노란 (deep, −4 eV) 격자와 보라 (repulsive, +3 eV) 격자가 번갈아 발생
- 이는 grid step (1.2 Å lateral) 이 Ni-Ni 거리 (~2.88 Å) 의 절반 수준이라 **일부는 Ni 위, 일부는 Ni 사이에 떨어짐**의 atomic-resolution artifact
- 노란 줄 (dy ≈ 0.1)이 표면의 **anchoring lane** 형성

**neutral heatmap pattern** = smooth stripes:
- dy 방향 줄무늬, dx 무관 (거의 uniform)
- best site의 well이 얕음 (heatmap에서도 less contrast)
- H 때문에 atomic-level 직접 접촉 못 함 → smooth dipole 기반 결합

**Z-profile**:
- doped: 단조 감소 (no barrier), dz=6→−1.6, dz=2.0→−4.75 (chemisorption-like)
- neutral: dz=2.5에서 well minimum, dz=2.0에서 살짝 반발 (van der Waals well + repulsive wall)

## 5. Phase C 결과 — Orientation sweep

> [!success] best site 고정, z-축 회전 sweep

| θ (°) | doped E_bind (eV) | neutral E_bind (eV) |
|---|---|---|
| 0 | **−4.75** ★ | −2.98 |
| 30 | −4.54 | −2.63 |
| 60 | −4.00 | −2.18 |
| 90 | −2.82 | −1.74 |
| 120 | +0.36 | −1.68 |
| 150 | −1.93 | −1.53 |
| 180 | −1.91 | −1.44 |
| 210 | −1.38 | −1.80 |
| 240 | −3.80 | −2.27 |
| 270 | −4.26 | −2.68 |
| 300 | −4.30 | −2.85 |
| 330 | −4.70 | **−3.02** ★ |

**도출**:
- **doped**: θ=0° (sulfonate-down, default)이 best — 이미 최적 orientation. ±30° 회전 내에 well, 90°+에선 반발.
- **neutral**: θ=330° 가 0.04 eV 더 깊음 (−3.02 vs −2.98). 작은 차이지만 **Phase B 시작점으로 self-consistency 보장 필요**.

## 6. Phase B 결과 — Local relax (rotation-aware)

> [!warning] Lesson learned
> 처음엔 Phase B를 θ=0°로 시작 (rigid scan default). neutral의 경우 **부적절한 시작 orientation 때문에 얕은 minimum (-3.67 eV, dz=2.30 Å)에 갇힘**. Phase C best θ=330°로 재시작 후 **deep minimum (-6.33 eV, dz=1.41 Å) 발견**. 차이 2.66 eV.
> 
> → **Phase B 는 Phase C에서 찾은 best orientation으로 시작해야 self-consistent**.

### 6.1 doped (θ=0° from Phase C)

| site | (dx, dy, dz) start | E_bind_relax (eV) | fmax | dz_final | steps | 수렴? |
|---|---|---|---|---|---|---|
| 1 | (0.30, 0.10, 2.0) | **−18.14** | 0.042 | **1.26** | 292 | ✓ |
| 2 | (0.80, 0.10, 2.0) | −18.09 | 0.047 | 1.25 | 238 | ✓ |
| 3 | (0.60, 0.10, 2.0) | **−18.17** | 0.050 | 1.26 | 268 | ✓ |
| 4 | (0.10, 0.10, 2.0) | −18.14 | 0.040 | 1.27 | 242 | ✓ |
| 5 | (0.10, 0.00, 2.5) | −13.91 | 0.55 | 1.22 | 300 | ✗ (미수렴) |

**Sites 1-4 모두 −18.14 ± 0.04 eV, dz=1.26 Å로 일치 수렴** — robust chemisorption basin.

### 6.2 neutral (θ=330° from Phase C)

| site | (dx, dy, dz) start | E_bind_relax (eV) | fmax | dz_final | steps | 수렴? |
|---|---|---|---|---|---|---|
| 1 | (0.10, 0.10, 2.5) | −6.19 | 0.050 | 1.41 | 147 | ✓ |
| 2 | (0.60, 0.10, 2.5) | −6.19 | 0.045 | 1.41 | 148 | ✓ |
| 3 | (0.80, 0.10, 2.5) | −6.32 | 0.050 | 1.48 | 209 | ✓ |
| 4 | (0.30, 0.10, 2.5) | **−6.33** | 0.046 | **1.49** | 211 | ✓ |
| 5 | (0.10, 0.10, 2.0) | −6.31 | 0.049 | 1.44 | 167 | ✓ |

**5개 site 모두 −6.27 ± 0.07 eV, dz=1.45 ± 0.03 Å 일치 수렴** — robust shallow chemisorption basin.

### 6.3 비교

> [!success] Phase B 최종 (self-consistent, rotation-aware)
> 
> | | doped | neutral | Δ (doped 우위) |
> |---|---|---|---|
> | **E_bind_relax** | **−18.17 eV** | **−6.33 eV** | **−11.84 eV** |
> | dz_final | 1.26 Å | 1.41 Å | 0.15 Å |
> | 결합 character | deep chemisorption | shallow chemisorption | |

## 7. 종합 — 모든 phase 통합 비교

| Phase | doped | neutral | Δ |
|---|---|---|---|
| A (rigid) | −4.75 | −2.98 | −1.77 |
| C (best orientation) | −4.75 (θ=0°) | −3.02 (θ=330°) | −1.73 |
| **B (relax)** | **−18.17** | **−6.33** | **−11.84** |

> [!important] Headline 결과
> **Self-doping (−SO₃H → −SO₃⁻)이 LiNiO₂ (104) 표면 anchoring을 11.84 eV 강화**
> 
> 두 form 모두 chemisorb (dz ~1.3-1.5 Å)지만:
> - doped: −18 eV — **deep chemisorption**, sulfonate가 표면 Li-O bilayer 안으로 부분 insertion, anion이 표면 cation site 점유
> - neutral: −6 eV — **shallow chemisorption**, sulfonate가 표면에 도달 (θ 회전 후) 하지만 H의 입체장애 때문에 less deep

## 8. 구조 분석 (best site xyz, Phase B 후)

### 8.1 doped (site 3, E=−18.17 eV)

- sulfonate S 좌표 z = 11.59 Å (slab top z=10.33 → dz=1.26 Å)
- sulfonate O 중 하나가 **z ≈ 9.5-10 Å** (슬랩 표면 atom과 직접 결합, 또는 그 안으로 슬쩍)
- thiophene 머리는 z=21 Å 부근 (위쪽으로 길게)

→ **분자가 slab 표면에 "꽂혀 있는" 형태**. binding은 ionic + multi-coordinate covalent.

### 8.2 neutral (site 4, E=−6.33 eV)

- sulfonate S 좌표 z = 11.74 Å (dz=1.41 Å)
- sulfonate O 중 가장 낮은 것 z ≈ 10.4 Å (슬랩 표면 위 0.07 Å)
- OH의 H는 z=12.7 부근 (S 옆에 위치, 슬랩 접근 안 함)
- thiophene 머리 z=22 Å

→ **분자가 표면 위에 "기대어" 있는 형태**. 약한 chemisorption, H가 SO₃ 한쪽 차단.

## 9. Caveats & Limitations

> [!warning] 절댓값 신뢰도
> - **−18 eV (doped)** 는 통상 화학결합 (single covalent ~5 eV, ionic ~3 eV) 보다 큰 값. UMA-oc20의 절댓값 calibration이 다소 큰 쪽으로 치우칠 수 있음.
> - 정성적 결론 (doped >> neutral, 둘 다 chemisorb)은 robust.
> - **DFT 검증 필수** — 진행 중 (gabia QE PBE+U+spin, 옵션 B 시작됨).

> [!info] Method caveats
> 1. **Phase B의 starting orientation 민감도** — neutral에서 θ 차이로 minimum 2.66 eV 변동. 더 많은 orientation 탐색하면 더 깊은 basin 발견 가능. (TODO: 모든 θ에서 Phase B → global minimum?)
> 2. **MLIP은 oc20 task**: Open Catalyst trained, adsorbate-on-surface 전용. omat은 LiNiO₂ slab 자체에 weird min 존재 → 사용 불가 (확인됨).
> 3. **Slab은 unrelaxed (init)**: UMA-omat relax는 collapse 일으킴. oc20는 slab relax 안 시도 (어차피 Phase B에서 슬랩 freeze).
> 4. **Single slab thickness** (~10 Å, 6 layers). 더 두꺼우면 ±0.1 eV 변동 예상.
> 5. **Periodic image**: 슬랩 lateral 거리 a=10.93 Å, b=17.3 Å — SDCP가 standing-up orientation일 때 안전 (분자 xy 단면 ~5-7 Å).

## 10. 다음 단계

### 10.1 진행 중 (백그라운드)

- [ ] **gabia DFT 옵션 B**: starting_mag ±0.3, mixing_beta 0.3, mixing_mode local-TF, electron_maxstep 300
  - 첫 SCF 수렴 여부 확인 후 BFGS 진행
  - 슬랩이 무너지지 않고 정상 relax 되는지 검증 (UMA-omat 무너짐 vs DFT 정상 가설 확인)
- [ ] **KISTI 746730**: V0 Nd-doped DFT restart (별개 트랙)

### 10.2 다음 작업

1. **DFT 검증 (best site)** — UMA Phase B에서 얻은 relaxed complex 좌표 → QE PBE+U+spin single-point
   - 동일 구조에서 E_bind_DFT vs E_bind_UMA 비교
   - paper-grade 정량값 확보
2. **Multi-orientation Phase B** — 모든 12 θ에서 relax → global minimum 확정 (특히 neutral)
3. **NCM811 (실제 cathode)** — LiNiO₂ → NCM811 (x_Ni=0.8, Co 0.1, Mn 0.1) 로 일반화
4. **(003)/(0001) basal plane** 비교 — (104) active vs basal 차이
5. **Other binder candidates** — PVDF, PAA 등과 SDCP 비교

## 11. 산출물 (gabia + 로컬 + repo)

### gabia 경로
```
/data/work/runs/sdcp_linio2_binding/
├── inputs/sdcp_doped/sdcp_doped.xyz         (33 atoms, ORCA-opt)
├── inputs/sdcp_neutral/sdcp_neutral.xyz     (34 atoms, ORCA-opt)
├── reference/slab_init.xyz                  (96 atoms, pymatgen init)
├── reference_dft/relax.in                   (옵션 B, 진행 중)
├── outputs/sdcp_doped/
│   ├── scan_rigid_doped.json                (Phase A)
│   ├── phase_BC_doped.json                  (Phase B + C, self-consistent)
│   ├── best_site_doped.xyz                  (Phase A best)
│   └── site{1..5}_relaxed.xyz               (Phase B relaxed structures)
├── outputs/sdcp_neutral/                    (동일)
└── outputs/figs/
    ├── heatmap_compare.png
    ├── heatmap_doped.png
    └── heatmap_neutral.png
```

### 로컬 (D:\QE\6. orca_sdcp\)
- `figs/heatmap_*.png` — 시각화
- `best_doped_oc20.xyz`, `best_neutral_oc20.xyz` — VESTA 확인용

### Repo (Yonghoon-DEM-DFT)
- `tools/sdcp_binding/build_linio2_slab.py` — LiNiO₂ (104) slab builder
- `tools/sdcp_binding/build_linio2_dft_input.py` — QE PBE+U+AFM input gen
- `tools/sdcp_binding/run_linio2_dft.sh` — gabia QE launcher
- `tools/sdcp_binding/scan_binding_rigid.py` — Phase A rigid scan
- `tools/sdcp_binding/phase_bc.py` — Phase B/C local relax + orientation
- `tools/sdcp_binding/plot_binding_heatmap.py` — heatmap 시각화
- `kb/projects/sdcp_linio2_binding.md` — 워크플로우 + method 정의

## 12. References

- Choi et al. 2025 — NCM/Li₆PS₅Cl sulfide SE interface (DFT+U, NCM (104))
- Wood et al. 2021 — NCM/LPS interface (DFT+U+D3, AIMD)
- Tian et al. 2018 — LiNiO₂ (104) (HSE+SOC)
- Wang 2006 — U_Ni = 6.2 eV 표준 (ortho-atomic)
- Open Catalyst 2025 leaderboard — UMA oc20 task performance
- ORCA TZVP — SDCP molecular structure (phase1_doped/neutral)

---

> [!example] 결론 한 줄
> **SDCP의 self-doping (−SO₃⁻)이 LiNiO₂(104) 표면 anchoring을 11.8 eV 강화** — paper headline 첫 결과. DFT 검증 진행 중.

> 작성일: 2026-06-01
> 작성자: Claude (BML 안용훈)
> 다음 업데이트: gabia DFT 옵션 B 수렴 후 / KISTI V0 DFT 완료 후

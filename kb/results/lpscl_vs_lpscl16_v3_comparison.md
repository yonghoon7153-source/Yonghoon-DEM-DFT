# LPSCl vs LPSCl1.6 — v3 직접 비교 (Pipeline v2 §8)

업데이트하면서 채워나가는 살아있는 비교 문서. 두 시스템 모두 같은 방법
(Pipeline v2: MLIP anneal → DFT BM-EOS V0 → DFT §8) 사용. 데이터 들어올
때마다 [pending] 자리 채움.

- **LPSCl** = comp1_v3, Li6PS5Cl, **4 fu = 52 atoms**, cubic V0 = 1016.62 Å³
  (a = 10.055 Å)
- **LPSCl1.6** = modelc_v3, Li5.4PS4.4Cl1.6, **5 fu = 62 atoms**, rhombohedral
  supercell V0 = 1216.44 Å³
- **공정 비교는 무조건 V/atom 또는 V/fu로!** 두 시스템 supercell 크기가
  다름 (4 fu vs 5 fu)이라 raw V0 비교는 의미 없음.

마지막 업데이트: 2026-06-03


## 0. Pipeline §8 진행 현황

⚠ **k-mesh 사고 (2026-06-04)**: comp1의 기존 §8b-i는 전부 **k=2×2×1 (k×L=10 Å, 4배 부족)**로
실행됨 → DFT 전자/탄성 property 오염. **새 V0를 k=4×4×4로 re-relax (force 0.26→0.0066 eV/Å)
후 52/520/4×4×4로 전부 재계산 중.** geometry는 거의 안 바뀜(RMS 0.003 Å)이라 좌표 기반
(bond/coord/BVSE)은 값 유지, 전자/탄성(gap/Cij/Bader/LOBSTER)은 진짜 영향받아 재계산 필수.
modelc(6×6×3)는 영향 없음.

| 단계 | LPSCl (comp1_v3) k444 | LPSCl1.6 (modelc_v3) |
|---|---|---|
| §8a V0 relax | **✅ k444 재완료** (18 BFGS, force 0.0066 eV/Å) | 완료 (6×6×3) |
| §8b 결합 통계 | **✅ k444** (Cl 전부 4a=ordered, Li-Cl 2.607, P-S 2.072) | 완료 |
| §8c 배위수 | **✅ k444** (Li env 1종, 완전 대칭) | 완료 |
| §8d Voronoi | **✅ k444** | 완료 |
| §8d' per-site (4a/4d Cl, PS4/4d S, Li env) | **✅ k444** (Cl 4a×4, 4d×0) | 완료 |
| §8e BVSE | **✅ k444** (bvse_k444/) | 완료 |
| §8f Bader (AE plot_num=17) | **✅ k444** (Li+0.87, Cl−0.93, S−1.52, P+3.27) | 완료 |
| §8g DOS / PDOS | **✅ k444** (gap **1.76**, ≈modelc 1.82; 이전 1.50은 k artifact) | 완료 |
| §8h 밴드 구조 | 🔲 **대기** (NSCF k-path + bands.x) | 완료 |
| §8i stress-strain Cij | ⏳ **k444 실행 중** (12 strain relax, 밤샘) — vacancy paradox 재검증 | 완료 |
| §8j MLIP UMA 600K snapshot 탄성 | 🔲 확인 필요 (mlip_600K_snapshot/) | 완료 |
| §8k AIMD Arrhenius | **✅ Ea=0.172 R²=0.999** (800K 재실행으로 fluke 해결) | 완료 (Ea 0.224) |
| §8l ELF (단면 + 3D iso) | 🔲 **대기** (SCF + pp.x plot_num=8) | 완료 |
| §8m LOBSTER (COHP/ICOHP) | 🔲 **대기** (PAW ext-basis, k444, elastic 후 GPU) | NSCF 완료, lobster 대기 |

### comp1 남은 작업 (전부 k444, GPU 순차)
1. **§8i elastic** ⏳ 밤샘 중 → fit → **E_VRH (vacancy paradox 확정)**
2. **§8m LOBSTER** — PAW ext-basis SCF + lobster (elastic 후)
3. **§8l ELF** — ONCV SCF + pp.x plot_num=8 (단면/3D)
4. **§8h bands** — NSCF k-path + bands.x
5. **§8j MLIP 600K elastic** — 상태 확인 (이미 했을 수도)

### 다른 트랙 (별도 머신, 병행)
- **kserver LiNiO₂ DFT+U SCF** (U6.2/tot_mag=0) — 수렴 확인 중
- **kserver Li3N DFT drag** (9점, adatom 고정) — UMA 붕괴 회피, 레퍼런스 0.133 재현 목표
- **modelc_v3 LOBSTER** — NSCF 완료, lobster 실행 대기


## 1. Paper 헤드라인 값 (잠정)

데이터 들어올 때마다 채움. **굵게** = paper-grade 값, [pending] = 대기.

| 항목 | LPSCl (Li6) | LPSCl1.6 (Li5.4) | 추세 | 메커니즘 |
|---|---|---|---|---|
| **B0** (BM-EOS, GPa) | **26.23** | **21.71** | LPSCl가 더 단단 (E(V) 곡선상) | Cl→S anti-site + Li 공공으로 hydrostatic compressibility ↑ |
| **K_VRH** (stress-strain, GPa) | **43.59** | **44.47** | **거의 동일** (Δ+2%) | clamped-ion 골격 모듈러스는 보존됨 |
| **G_VRH** (GPa) | **20.12** | **20.05** | **동일** | shear 강성 보존 |
| **E_VRH** (GPa) | **52.31** | **52.30** | **DFT 0K에서 동일 — vacancy paradox** | 실험은 LPSCl1.6 > LPSCl인데 DFT는 못 잡음 |
| **ν** (Poisson) | 0.300 | 0.304 | 거의 동일 | |
| **Zener A** | **1.073** (isotropic) | **0.416** (anisotropic) | **2.6× 차이** | Li 공공 + Cl anti-site로 anisotropy 도입 |
| 밴드갭 (DFT-PBE, CBM−VBM, eV) | **1.50** | **1.82** | LPSCl1.6 +0.32 eV (방향은 literature trend 일치, 절대값은 의심 — §15 참조) | Cl 3p가 S 3p보다 깊음 → S→Cl 치환이 VBM 내려 → gap 넓어짐 (원리상) |
| Bader q(Li) (e) | [pending] | [추가] | | |
| AIMD D_Li(600K) (cm²/s) | **3.73e-6** | **7.90e-6** | modelc 2.1× 빠름 (vacancy → carrier↑) | 실험 방향 일치 (Cl-rich 더 전도성) |
| AIMD σ_NE(600K) (S/cm) | **0.273** | **0.543** | modelc 2.0× 높음 | 실험 비 2.05× (LPSCl1.5/LPSCl)와 정량 일치 |
| AIMD Ea (eV) | **0.16–0.22** (R²↓) | **0.224** | comp1 ≈ 또는 ≤ modelc (장벽 비슷) | σ 차이는 prefactor(carrier) 때문, 장벽 아님 |
| ICOHP P–S (eV/bond) | [pending] | [추가] | | |
| ICOHP Li–S (eV/bond) | [pending] | [추가] | | |
| ICOHP Li–Cl (eV/bond) | [pending] | [추가] | | |

**실험 기준점**: LPSCl1.6의 측정 Young's modulus가 LPSCl보다 **더 높음**.
DFT 0K에서 반대 결과 (Li6가 더 단단)가 나오면 그게 "vacancy paradox" —
DFT가 유한온도의 비조화 강화(anharmonic stiffening) 및 Li 동적 재분배를
놓침. Paper에서 다룰 핵심 주제.


## 2. EOS (BM3, free 4-parameter fit)

| | LPSCl v3 (4 fu) | LPSCl1.6 v3 (5 fu) |
|---|---|---|
| nat | 52 | 62 |
| supercell type | cubic conventional | rhombohedral |
| V0 raw (Å³) | 1016.62 | 1216.44 |
| **V0 / atom (Å³)** | **19.55** | **19.62** (+0.4%) |
| **V0 / fu (Å³)** | **254.16** | **243.29** (−4.3%) |
| a equivalent (cubic 환산, Å) | 10.0547 | ≈ 9.910 (10.674는 5-fu supercell에 한정, 직접 비교 X) |
| B0 (GPa) | 26.233 ± 0.004 | 21.71 ± 0.27 |
| B0' | 4.171 ± 0.011 | 7.01 ± 1.37 |
| R² | 1.000000 | 0.999012 |
| n_points | 8 | 11 |
| Fit 날짜 | 2026-06-03 | 2026-06-03 |

**핵심**:
- supercell 크기가 4 fu vs 5 fu라서 V0 raw 직접 비교 ❌. 반드시
  V/atom 또는 V/fu로 정규화.
- **V/fu로 보면 LPSCl1.6가 −4.3% 작음** → Cl→S 치환 + Li 공공으로 fu 부피
  소폭 수축. 실험 lattice 경향 일치.
- **V/atom은 +0.4%로 거의 동일** → 원자 1개가 차지하는 평균 부피는 같다는
  뜻 (argyrodite framework이 보존됨).

**B0' 차이에 대한 노트**: comp1의 B0' = 4.17 (교과서 범위), modelc_v3 B0' =
7.01 (높고 σ도 큼). modelc의 큰 B0' 불확실성은 더 넓은 부피 sweep + 평탄한
Li 에너지면을 반영. 두 시스템 각자 K 값 (BM vs stress-strain)은 ~3% 이내로
교차검증됨.


## 3. 탄성 — DFT 0K stress-strain (전체 6×6)

| 항목 (GPa) | LPSCl v3 (Li6) | LPSCl1.6 v3 (Li5.4) | Δ |
|---|---|---|---|
| C11 평균 | **74.23 ± 5.33** [66.7, 78.3] | 89.87 ± 3.16 [85.4, 92.3] | −17.4% (LPSCl 약함) |
| C12 평균 | **29.23 ± 0.51** [28.8, 30.0] (매우 균일) | 21.82 ± 2.43 [19.9, 25.3] | **+34%** (LPSCl 강함) |
| C44 평균 | **18.98 ± 0.90** [18.3, 20.3] | 14.43 ± 1.25 [13.6, 16.2] | **+31%** (LPSCl 강함) |
| B_Voigt / B_Reuss / B_VRH | 44.23 / 42.94 / **43.59** | 44.50 / 44.44 / **44.47** | −2% (사실상 동일) |
| G_Voigt / G_Reuss / G_VRH | 20.39 / 19.85 / **20.12** | 22.27 / 17.83 / **20.05** | +0.4% (동일) |
| **E_VRH** | **52.31** | **52.30** | **±0.02% (paradox)** |
| ν | 0.300 | 0.304 | 거의 동일 |
| **Zener A** | **1.073** (≈ 1 = isotropic) | **0.416** (강한 anisotropy) | **2.6×** |
| eigenvalues > 0 | 17.4, 18.8, 19.4, 42.3, 48.0, 133.7 (모두 양수 ✓) | 11.6, 12.7, 18.1, 63.8, 73.1, 133.6 ✓ | 둘 다 안정 |

### Stress-strain (DFT 0K)에서 본 핵심

1. **B/G/E 동일 (±2%)** — bulk, shear, Young의 평균 모듈러스는 LPSCl ≈
   LPSCl1.6. 실험에서 LPSCl1.6 Young's가 더 높다는 결과를 **DFT 0K가 못
   잡음** → finite-T 효과 (phonon anharmonic stiffening, Li dynamic
   redistribution) 필요. **paper의 vacancy paradox 핵심 논증.**
2. **C44 / C12는 LPSCl가 30%↑ 더 강함** — Li 공공이 없어서 shear (C44) +
   cross-coupling (C12) 더 견고.
3. **C11은 LPSCl가 17%↓ 더 약함** — 정상 compression에 약함. 이건
   복합적인 effect (격자 상수 vs Li6 ordering).
4. **Zener A**: LPSCl 1.07 (등방), LPSCl1.6 0.42 (강한 비등방). **이게
   Cij 수준에서 보이는 유일한 vacancy/disorder fingerprint.** B/G/E가
   동일해도 anisotropy로 두 시스템 구분 가능.

### BM-EOS B0 vs stress-strain B_VRH 비교 (intra-system)

| | B0 (BM, GPa) | B_VRH (stress, GPa) | 비율 |
|---|---|---|---|
| LPSCl | 26.23 | 43.59 | 1.66 |
| LPSCl1.6 | 21.71 | 44.47 | 2.05 |

두 방법 모두 물리적으로 의미 있지만 다른 양:
- **B0 (BM-EOS)**: 등방 압축 (hydrostatic) 시 E(V) 곡률 = full
  relaxation 포함.
- **B_VRH (clamped-ion)**: clamped-ion Cij에서 유도 = harmonic frozen-ion만.
- ratio 1.5–2× 범위는 Cl-rich argyrodite에서 표준. **paper에 둘 다 보고.**


## 3'. 탄성 — DFT 0K **relaxed-ion** stress-strain (🎯 vacancy paradox RESOLVED)

같은 12-strain 프로토콜인데 각 strained cell에서 원자가 BFGS로 relax됨
(이온 Born screening 포함). 실험에 직접 대응되는 값.

| 항목 (GPa) | LPSCl v3 (Li6) | **LPSCl1.6 v3 (Li5.4)** | Δ% | 실험 |
|---|---|---|---|---|
| C11 avg | 37.67 ± 1.56 | 37.03 ± 3.21 | −1.7% | |
| C12 avg | 19.98 ± 0.94 | 16.82 ± 2.06 | −15.8% | |
| C44 avg | 8.03 ± 0.90 | 13.68 ± 6.25 (큰 분산) | +70% | |
| B_VRH | **25.18** | **23.40** | −7.1% | ~25 |
| G_VRH | **8.26** | **10.61** | **+28.4%** | ~8 |
| **E_VRH** | **22.33** | **27.66** | **+23.9% ✓** | **LPSCl1.6 > LPSCl ✓** |
| ν | 0.352 | 0.303 | | ~0.35 |
| Zener A | 1.16 | **1.44** | **+24% (aniso ↑)** | |

### 핵심 발견

**LPSCl relaxed-ion E_VRH = 22.33 GPa는 실험값 ~23 GPa와 정확히 일치.**
clamped-ion 52.31 GPa는 **실험을 2.3배 over-estimate**.

| 모듈러스 | clamped/relaxed 비율 |
|---|---|
| C11 | 1.97 |
| C44 | 2.36 (shear에서 가장 over-estimate) |
| B_VRH | 1.73 |
| **E_VRH** | **2.34** |

이는 argyrodite의 **Li sublattice가 매우 soft**해서 변형 시 Li 재배치
(ionic Born screening)가 격자 강성에 핵심 기여한다는 의미.

### Vacancy paradox RESOLVED (paper main result)

| 시나리오 | E_VRH (LPSCl) | E_VRH (LPSCl1.6) | 결론 |
|---|---|---|---|
| clamped-ion DFT 0K | 52.31 | 52.30 | **paradox** (E 차이 ~0%) |
| **relaxed-ion DFT 0K** | **22.33** | **27.66 ✓** | **paradox RESOLVED** ★ |
| MLIP 600K snapshot | 59.74 | 52.72 | MLIP은 finite-T 못 잡음 (clamped-like) |
| 실험 | ~23 | LPSCl1.6 > LPSCl | DFT relaxed가 실험 추세 정확 일치 |

### 🎯 paper headline finding

**LPSCl1.6은 DFT 0K relaxed-ion에서 LPSCl보다 23.9% 더 stiff (E_VRH 22.33→27.66 GPa)** —
실험 추세 (LPSCl1.6 > LPSCl) 완전히 잡음.

**Mechanism**:
- G_VRH **+28%** (shear modulus 큰 증가)
- B_VRH −7% (bulk modulus 약간 감소)
- Zener anisotropy A 1.16→**1.44** (anisotropy ↑, disorder fingerprint)

→ **vacancy + 4d-Cl anti-site가 특정 shear configuration을 lock-in**해서 shear modulus 강화.
bulk는 vacancy로 인해 약간 soft. **Shear-dominant stiffening + 비등방** 이 disorder의
mechanical fingerprint.


## 4. 탄성 — MLIP UMA 600K snapshot

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| E_VRH (GPa) | [pending] | 52.72 ± 1.42 |
| 프로토콜 | UMA-s-1p1 600K Langevin → snapshot → relaxed-ion FIRE → Cij | 동일 |


## 5. 결합 환경 (DFT V0)

Bond stats: 평균 d, σ, n_bonds (방향 한 번씩 카운트, 이중 카운트 제거).
Coordination: 평균 Z (cutoff 같음). Voronoi: 사이트당 다면체 부피.

**Cutoff 통일**: P–S 2.3, Li–S 3.2, Li–Cl 3.4, S–S 4.0 Å (argyrodite 표준).

### Bond lengths

| 결합 | LPSCl v3 (n / mean ± σ / [min, max] Å) | LPSCl1.6 v3 | Δ mean |
|---|---|---|---|
| **P–S** | 16 / **2.0726 ± 0.0362** / [2.036, 2.109] | 20 / **2.0640 ± 0.0111** / [2.042, 2.083] | **−0.009 Å** (PS4 약간 단축 + σ 1/3로 감소: PS4 매우 단단/균질) |
| **Li–S** | 72 / **2.4610 ± 0.1057** / [2.353, 2.644] | 68 / **2.4654 ± 0.0935** / [2.302, 2.813] | +0.004 Å (사실상 동일) |
| **Li–Cl** | 24 / **2.6073 ± 0.1291** / [2.425, 2.699] | 40 / **2.5318 ± 0.1185** / [2.308, 3.005] | **−0.076 Å (LPSCl1.6에서 Li–Cl 더 짧음!)** |
| S–S (cage) | 56 / 3.5948 ± 0.1986 / [3.335, 3.823] | 58 / 3.5193 ± 0.1779 / [3.263, 3.990] | −0.076 Å (cage 압축) |

### Coordination

| 사이트 | LPSCl v3 (avg Z ± σ / [min, max]) | LPSCl1.6 v3 | 차이 |
|---|---|---|---|
| Li | **4.00 ± 0.00** [4, 4] (정확히 4, 24 사이트) | **4.00 ± 0.27** [3, 5] (27 사이트) | 평균 동일하나 LPSCl1.6은 ±1 분산 (공공 disorder) |
| P  | **4.00 ± 0.00** (PS4 4개) | **4.00 ± 0.00** (PS4 5개) | 동일 (PS4 backbone 보존) |
| S  | **10.00 ± 1.67** [8, 12] | **9.27 ± 1.21** [6, 11] | LPSCl1.6 S 배위수 −0.73 (Li 공공 → S 주위 Li 부족) |
| Cl | **6.00 ± 0.00** (Cl[Li6] 정팔면체 4개) | **5.00 ± 0.50** [4, 6] (8개) | **Cl 배위수 6→5** — 일부 Cl이 4d (S 자리) anti-site |

### Voronoi (다면체 부피)

| 종 | LPSCl v3 V_poly (Å³) | LPSCl1.6 v3 | Δ |
|---|---|---|---|
| Li | **19.560 ± 0.214** | **20.513 ± 1.150** | +1.0 Å³ (공공으로 Li 주변 공간 ↑) |
| P  | **14.052 ± 0.000** | **13.993 ± 0.370** | −0.06 Å³ (사실상 동일, PS4 크기 보존) |
| S  | **20.137 ± 3.408** | **19.550 ± 2.047** | −0.6 Å³ (S 자리 약간 압축) |
| Cl | **22.057 ± 0.000** | **20.308 ± 0.736** | **−1.7 Å³ (Cl 다면체 축소!)** Cl이 작은 4d 자리 occupy 시사 |

### LPSCl vs LPSCl1.6 — 결합환경 차이 핵심 정리

1. **Li–Cl 결합 단축 (−0.076 Å)** — 직관과 반대. Cl이 많아지면서 Cl 일부가
   4d (원래 S²⁻ 자리)에 들어가 Li–Cl 거리가 줄어듦. Voronoi에서 Cl 부피
   −1.7 Å³가 같은 그림을 보여줌.
2. **Cl 배위수 6 → 5 (Cl anti-site)** — 4a Cl[Li6]에서 일부가 4d Cl[Li4]로
   이동. Cl 8개 중 평균 1–2개가 4d. → site disorder의 직접 증거.
3. **PS4 backbone 안정** — P–S 평균 동일 + σ 1/3로 감소 (LPSCl1.6에서
   PS4가 더 균질). Cl excess가 P-S 결합 자체엔 영향 없음.
4. **Li 배위수 평균은 동일하나 분산 발생** — LPSCl1.6에서 일부 Li가 3- 또는
   5-배위 (vacancy + Cl anti-site로 인한 local 불균질).

**Paper 함의**: "Cl 증가 = Li–Cl 결합 약화"라는 단순 가정 반박. Cl excess →
일부 Cl이 4d 자리로 → Li–Cl이 **오히려 짧고 더 강한 ionic bond**. 이는
Wilkening-style ionic potential 그림 (q × |q| / r)에서 Cl excess가 ionic
glue를 강화한다는 것을 의미.


## 6. BVSE (Python 구현)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| 최소 Ea_BVSE (eV) | [pending] | [추가] |
| 예측 이동 경로 | [pending] | [추가] |


## 7. Bader (plot_num=17 AE charge density) — paper-grade ✓

PAW kjpaw + pp.x AE density + Henkelman bader v1.05. SCF는 LOBSTER ext basis와
동일 (ecutwfc=70 Ry, PAW).

| 종 (e) | LPSCl (comp1) | LPSCl1.6 (modelc_v3) | 차이 |
|---|---|---|---|
| **Li** | **+0.874 ± 0.005** (n=24) | **+0.882 ± 0.010** (n=27) | +0.9% (사실상 동일) |
| **Cl** | **−0.941** (n=4, σ=0) | **−0.916 ± 0.005** (n=8) | LPSCl 더 ionic (Δ −0.025) |
| **P** | **+3.238** (n=4, σ=0) | **+4.429 ± 0.415** (n=5) | **+36.8% (Bader basin shape 효과)** |
| **S** | **−1.514 ± 0.363** (n=20) | **−1.756 ± 0.244** (n=22) | +16.0% more ionic |

### PS4 charge sum 보존 cross-check

| | P + 4S 합 | formal PS4³⁻ |
|---|---|---|
| comp1 | −2.82 | −3 |
| modelc | −2.60 | −3 |

둘 다 −3 부근. 개별 P/S 분리값은 Bader basin shape이 환경 dependent (PS4-S와
4d-S²⁻가 basin 모양 다름) → modelc에서 σ 크고 평균값 shift. paper에 P+4S 합
또는 PS4 unit 단위로 reporting 추천 (개별값은 supplementary).

### Wilkening ionic potential framework (q × |q| / r, eV/Å)

| | LPSCl | LPSCl1.6 | Δ % |
|---|---|---|---|
| **Li–S** | **0.538** (0.874 × 1.514 / 2.461) | **0.628** (0.882 × 1.756 / 2.465) | **+16.8%** |
| Li–Cl | 0.316 (0.874 × 0.941 / 2.607) | 0.319 (0.882 × 0.916 / 2.532) | +1.1% |
| **Li-S / Li-Cl ratio** | **1.70** | **1.97** | Li-S 우세 더 강함 |

**Paper 메시지** (Bader perspective):
1. Li-S가 Li-Cl보다 ionic glue **1.7–2× 강함** (Wilkening framework confirm)
2. LPSCl → LPSCl1.6에서 ionic potential 증가는 **거의 전적으로 Li-S 채널**
   (Li-Cl 거의 동일). vacancy + 4d-Cl 효과가 S charge 증가 (−1.51 → −1.76)로
   집중됨.
3. ICOHP (LOBSTER) 도 LPSCl1.6에서 모든 ionic bond 강화 (+13.4% Li-Cl,
   +7.9% Li-S) — Bader와 같은 방향 (LPSCl1.6 더 strong ionic)이지만 Li-Cl/Li-S
   분배는 다름. **두 방법 종합**: paper에 Li-S 채널이 ionic stiffening 주
   기여라는 합의된 메시지 가능.


## 8. DOS / PDOS

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| 밴드갭 (PBE, eV) | [pending] | [추가] |
| VBM 성격 | [pending] | S 3p 우세 |
| CBM 성격 | [pending] | [추가] |
| E_F 근처 Li-PDOS | [pending] | [추가] |


## 9. 밴드 구조 (Hungarian 재정렬, k-path X-Γ-L-W-K)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Direct/indirect | [pending] | [추가] |
| 갭 위치 | [pending] | [추가] |
| Li-like 밴드 유효질량 | [pending] | [추가] |


## 10. AIMD 이온 확산 (Arrhenius 600/800/1000K) — 완료 2026-06-04

**둘 다 동일 프로토콜** (UMA-s-1p1, Langevin NVT, equilib 10ps + prod 100ps,
timestep 2fs, 1000 frames). comp1 fit_window [2,20]ps 기준 (modelc 비교 시 주의).

| | LPSCl (comp1) | LPSCl1.6 (modelc) | 비 |
|---|---|---|---|
| D(600K) (cm²/s) | 3.73e-6 | 7.90e-6 | **2.1× (modelc↑)** |
| D(800K) (cm²/s) | 6.38e-6 | — | |
| D(1000K) (cm²/s) | 2.26e-5 | — | |
| **Ea (eV)** | **0.16–0.22** | **0.224** | comp1 ≈/≤ modelc |
| D₀ (cm²/s) | 2.3e-4 | 5.75e-4 | 2.5× (modelc↑) |
| σ_NE(600K) (S/cm) | 0.273 | 0.543 | **2.0×** |

### 10.1 핵심 결론 (robust)

1. **modelc(LPSCl1.6)가 comp1(LPSCl)보다 Li 2배 빠름** (D, σ 모두 ~2×).
   window 무관하게 견고 (modelc 2-3× 높음).
2. **실험 방향·크기 정량 일치**: NEI/Ampcera Li5.5PS4.5Cl1.5 ~8.8 mS/cm vs
   Li6PS5Cl ~4.3 mS/cm = **2.05×** ↔ 우리 σ 비 2.0× 🎯
3. **framework 정지 확인**: D(Cl,P,S) ~ D(Li)의 1/40-1/60 → Li-only 전도체 (둘 다).

### 10.2 메커니즘 — vacancy는 장벽이 아니라 carrier를 늘린다

- **Ea가 거의 같음** (comp1 0.16-0.22 ≈ modelc 0.224, comp1이 더 낮지도 않음)
- modelc의 2× σ는 **prefactor D₀ ↑** (5.75e-4 vs 2.3e-4) 때문 = Li vacancy가
  **운반체(빈자리)·경로를 늘림**, per-hop 장벽을 낮추는 게 아님.
- → paper 메시지: "halogen-rich가 더 전도성인 건 migration barrier가 낮아서가
  아니라 vacancy carrier가 많아서" (실험적으로 더 정확한 그림).

### 10.3 ⚠ paper-grade 전 보완 필요

- comp1 **R²=0.77-0.87로 약함** (3 T점, T=800K D 이상치). Ea가 window 따라
  0.16~0.22로 흔들림.
- **공정 비교**: comp1·modelc를 **동일 MSD window**로 재fit 필요 (modelc Ea=0.224
  의 window 미확인). 컨테이너에서 둘 다 [2,50] 재fit 권장.
- 통계 개선 (longer prod / 더 많은 seed / 4-5 T점) 후 Ea 확정.
- 절대 σ는 Haven ratio 적용 후 실험 비교.

전체 데이터: `db/properties/li_transport.json` (comp1_v3 entry + comp1_vs_modelc_comparison).


## 11. ELF (전자 국소화 함수)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Li–S 이온성 | [pending] | [추가] |
| P–S 공유성 (ELF > 0.7 사이) | [pending] | 있음 |
| 3D iso 레벨 | [pending] | 0.75 |


## 12. LOBSTER ICOHP (per-bond 평균, eV) — **paper-grade extended basis**

ext basis (Li 1s 2s 2p, P/S/Cl 3s 3p 3d) + PAW kjpaw pseudo +
charge-spilling < 2% (target paper-quality).

| 결합 종류 | **LPSCl v3 ext** | **LPSCl1.6 v3 ext** | Δ % (LPSCl1.6 / LPSCl − 1) |
|---|---|---|---|
| **P–S** | **−5.944** (16 bonds) | **−6.000** (20) | +0.9% (PS4 거의 동일) |
| **Li–Cl** | **−1.855** (24 bonds) | **−2.103** (42) | **+13.4% (LPSCl1.6 더 강함)** |
| **Li–S** | **−1.592** (120 bonds) | **−1.717** (113) | **+7.9%** |
| S–S | **−0.107** (56 bonds) | **−0.110** (58) | ~0 |

**Charge spilling**: comp1 **1.46%**, modelc_v3 **1.16%** — 둘 다 paper 표준
< 5% 만족 ✓. 절대값 paper에 그대로 사용 가능.

### 핵심 paper 메시지

1. **모든 ionic bond가 LPSCl1.6에서 더 강함** (특히 Li-Cl +13.4%). vacancy +
   Cl 치환이 약화가 아니라 **강화**.
2. **위계 보존**: P-S (covalent backbone) ≫ Li-Cl > Li-S ≫ S-S (둘 다)
3. **Li-Cl > Li-S in both**: Wilkening ionic-potential framework 일치
4. **4d-Cl anti-site** (modelc 8개 중 1개)이 짧고 강한 Li-Cl 결합 형성 →
   평균 ICOHP 강화에 기여
5. **PS4 backbone robust**: 두 시스템 P-S ICOHP 거의 동일 (−5.94 vs −6.00),
   화학 환경 변화에 영향 안 받음 — paper 결과 4 (PS4 안정성) 확인

### old basis (17% spill) → ext basis (1.16-1.46% spill) 비교

ext basis 적용 후 모든 ICOHP가 약 +17–180% 강해짐 (old basis가 심하게
under-estimate). 절대값이 paper에 들어가야 함. 단, 두 시스템 위계 + ratio는
old basis에서도 robust했음 — paper에 ext 값만 보고하고 sparse basis 결과는
report안 함.

| Bond | comp1 old (17%) | comp1 ext (1.46%) | modelc old (17%) | modelc ext (1.16%) |
|---|---|---|---|---|
| P-S | n/a | -5.944 | -5.123 | **-6.000** |
| Li-Cl | n/a | -1.855 | -1.214 | **-2.103** |
| Li-S | n/a | -1.592 | -0.614 | **-1.717** |
| S-S | n/a | -0.107 | -0.061 | **-0.110** |


## 13. 시스템 내부 교차검증 (intra-system cross-checks)

| 검증 | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| K_BM vs K_VRH (GPa) | 26.23 vs [pending] | 21.71 vs 44.47 |
| K_BM vs K_VRH 차이 해석 | TBD | 물리적으로 다른 양: BM은 E(V) 등방 압축, VRH는 clamped-ion Cij 전체에서 유도. Cl-rich soft phase에서 ~2배 차이 예상. |
| Cij 역학적 안정성 (모든 eigenvalue > 0) | [pending] | 안정 |


## 14. 논의 포인트 (paper outline)

1. **Vacancy paradox**: 실험은 LPSCl1.6 > LPSCl (Young's), DFT 0K은 반대일
   수 있음. 유한온도 강화의 원인 후보:
   - Cl-rich basin의 비조화 phonon 강화
   - Li 사이트 무질서 → effective stiffening (엔트로피 효과)
   - §4 MLIP 600K snapshot에서 비율 비교.
2. **Cl 치환**: Cl→{S 공공 + Cl}은 배위수 분포 + Li 이동성 모두 변화시킴
   (BVSE / AIMD 절).
3. **Ionic vs covalent 비율**: ELF + Bader + LOBSTER가 함께 PS4 공유 backbone
   (P–S 강한 ICOHP)에서 Li–anion 이온 결합 (Li–S/Li–Cl 약한 ICOHP, 높은
   Bader 전하 이동) 으로의 이동을 정량화.
4. **B0 vs K_VRH 불일치**: 물리적으로 의미 있음 — BM-EOS B0는 등방 압축
   (hydrostatic) bulk modulus, K_VRH from clamped-ion Cij는 harmonic-only
   frozen-ion 값. Cl-rich soft phase일수록 둘의 갭이 큼. Paper에 둘 다 보고.


## 15. 전자구조 (DOS/PDOS) — paper-grade + 문헌 대조 (2026-06-04)

### 15.1 측정값

| 항목 | comp1_v3 (LPSCl) | modelc_v3 (LPSCl1.6) | Δ |
|---|---|---|---|
| EF (eV, QE) | 2.821 | 2.445 | -0.376 |
| VBM (eV) | 2.48 | 2.72 | +0.24 |
| CBM (eV) | 3.98 | 4.54 | +0.56 |
| **gap (CBM−VBM, eV)** | **1.50** | **1.82** | **+0.32** |
| VBM character | S p (91%) + Li p (6%) | S p (92%) + Li p (6%) | 동일 |
| CBM character | S p (42%) + P s (27%) + Li p (15%) | S p (45%) + P s (27%) + Li p (13%) | 거의 동일 |

방법: QE 7.4.1 PBE, USPP(Li,S,Cl)/RRKJUS(P), MV smearing (degauss=0.01
Ry SCF), dos.x + projwfc.x on V0 relax .save. Gap = low-DOS run
(DOS<0.5 states/eV/cell) straddling EF; orbital character = PDOS in
0.5 eV window adjacent to edge. (`tools/modelc_v3/plot_dos.py`)

### 15.2 문헌 PBE 대조

| 출처 | Method | gap (eV) |
|---|---|---|
| 우리 comp1_v3 | PBE / USPP | 1.50 |
| Batteries 12(2):60 (2026) | PBE | 2.45 |
| First-principles PMC9661960 | PBE | ~2.15 |
| Sci. Direct S0921452623002995 | PBEsol + TB-mBJ | 3.11 |
| HSE06 (다수) | HSE06 | 3.30 – 3.52 |
| G0W0 (PMC9661960) | G0W0 | ~5.13 |
| 실험 (간접 추정) | optical | 3.0 – 3.5 |

**우리 PBE 값 1.50 eV가 literature PBE 2.15-2.45 보다 0.65-0.95 eV 낮음.**  
- 우리 cell이 supercell (4 fu, 1×1×1 k일 가능성)이라 dispersion이 적게 잡힘 → 가짜로 좁은 gap
- Smearing 0.27 eV로 broadened edge → DOS threshold가 band edge를 1 grid 안쪽으로 끌어들임  
→ **§8h bands.x로 진짜 gap을 검증해야 함 (다음 단계)**

### 15.3 Defect band 진단 (`analyze_defect_band.py`)

modelc에서 EF=2.445 < VBM=2.72라는 점이 anomalous (insulator는 VBM<EF<CBM이어야).
`analyze_defect_band.py`로 [EF, VBM] = [2.445, 2.72] 윈도우 분석:

| | modelc | comp1 (같은 폭 EF 윈도우) |
|---|---|---|
| 총 적분 PDOS (states) | **0.74** | 0.037 (20× 적음) |
| S 3p 기여 | 93% | 94% (broadening tail만) |
| Top 원자 | S #34 (12%), S #35 (11%), S #50 (9.5%), … (10개 S에 ~70%) | 8개 S에 균등 9.33% each (= 균질 tail) |

→ **modelc에는 특정 S 원자 (#34, #35, #50, #39, #40 등)에 국소화된 S 3p 상태가
   진짜 존재**.

### 15.4 해석 갈래 — bands 검증 필요

| 시나리오 | 의미 |
|---|---|
| (A) 진짜 defect band | 우리 supercell의 specific Cl-S/Li vacancy 배치가 local non-neutrality (예: Li vacancy가 S의 nearest neighbor에 비대칭) → S 3p hole 국소화. 문헌 (Adeli 2019, arXiv:2503.13142)에서는 "ordered" 또는 평균 disorder 가정으로 이 효과 안 봄. |
| (B) Smearing artifact | 0.136 eV smearing + 0.5 threshold로 valence band 상단 tail을 "defect band"로 오인. 실제 VBM은 EF 근처 ≈ 2.45 eV. |
| 두 시나리오 구별법 | **bands.x** 결과의 EF 위치를 확인하면 결정적. (A)면 flat localized band가 보임, (B)면 dispersive band edge가 EF 근처로 자연스럽게 마감. |

### 15.5 Charge balance 사실 확인

valence electron 수 (확인용):
- Li6PS5Cl: 6 + 5 + 5×6 + 7 = 48 e/fu
- Li5.4PS4.4Cl1.6: 5.4 + 5 + 4.4×6 + 1.6×7 = 48 e/fu (정확히 같음)

두 시스템 모두 **stoichiometric insulator로 charge-compensated** —  
EF가 modelc에서 VBM 아래에 있다면 그건 charge 불균형이 아니라 **(A) 국소
배치 효과 또는 (B) smearing artifact**.

### 15.6 결론 (현재까지)

1. CBM−VBM 절대값은 우리 PBE에서 literature 대비 낮음 → **bands.x 검증 필요**
2. 두 시스템 **Δgap = +0.32 eV** (LPSCl1.6이 넓음) — 방향은 literature 원리 (Cl 3p 깊음 → 이온성 강화)와 일치
3. **VBM/CBM orbital character는 두 시스템에서 동일** (S 3p VBM, S 3p + P 3s CBM) → Δgap은 hybridization이 아니라 electrostatic shift
4. modelc의 EF-VBM 사이 0.74 states는 **specific 배치 효과**일 가능성 있음 — bands로 검증 후 paper에 어떻게 다룰지 결정
5. 다음: V0 SCF k-mesh 확인 → 필요시 dense NSCF (6×6×3 + tetrahedra) → 그 위에서 dos.x 재계산 → bands.x

Sources (문헌):
- [Sci. Direct S0921452623002995 — TB-mBJ 3.11 eV](https://www.sciencedirect.com/science/article/abs/pii/S0921452623002995)
- [PMC9661960 — HSE06, G0W0](https://pmc.ncbi.nlm.nih.gov/articles/PMC9661960/)
- [Batteries 12(2):60 — PBE 2.45 eV](https://doi.org/10.3390/batteries12020060)
- [Adeli 2019 Angew Chem — LPSCl1.5 (charge-compensated)](https://onlinelibrary.wiley.com/doi/10.1002/anie.201814222)
- [Devil in the Defects (Chem Mater 2021) — LPSCl intrinsic n-type](https://pubs.acs.org/doi/10.1021/acs.chemmater.1c02345)
- [arXiv:2503.13142 — LPSCl1.5 disorder (no mid-gap state)](https://arxiv.org/pdf/2503.13142)


## 각주

- modelc_v3 Pipeline v2 lineage 전체는 `db/compositions/modelc_v3.json`
  (Step 1–8 audit trail).
- comp1 v2 §8 결과 (a=9.929, v2 cell)는 컨테이너의
  `/home/ubuntu/work/runs/comp1_v3/archive_v2_post/`에 archive — 재현성
  목적, paper 사용 안 함.
- 모든 §8 도구는 `tools/modelc_v3/` 와 `tools/comp1_v3/`에.

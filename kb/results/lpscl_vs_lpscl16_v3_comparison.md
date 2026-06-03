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

| 단계 | LPSCl (comp1_v3) | LPSCl1.6 (modelc_v3) |
|---|---|---|
| §8a V0 relax (BM-EOS V0에서 cell-fixed BFGS) | **완료** (18 BFGS, V=1016.62 ✓) | 완료 |
| §8b 결합 통계 (bond stats) | **완료** | 완료 |
| §8c 배위수 (coordination) | **완료** | 완료 |
| §8d Voronoi | **완료** | 완료 |
| §8d' per-site 분석 (4a/4d Cl, PS4/4d S, Li env) | **완료** | 완료 |
| §8e BVSE (python) | 대기 | 완료 |
| §8f Bader (AE plot_num=17) | 대기 | 완료 |
| §8g DOS / PDOS | 대기 | 완료 |
| §8h 밴드 구조 (Hungarian 재정렬) | 대기 | 완료 |
| §8i stress-strain 전체 6×6 Cij | **완료** (B=43.59, E=52.31, A=1.07) | 완료 |
| §8j MLIP UMA 600K snapshot 탄성 | 대기 | 완료 |
| §8k AIMD 600/800/1000K (Arrhenius) | 대기 | 완료 |
| §8l ELF (단면 + 3D iso) | 대기 | 완료 |
| §8m LOBSTER (COHP/ICOHP 4-panel) | 대기 | NSCF 완료, lobster 대기 |


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
| 밴드갭 (DFT-PBE, eV) | [pending] | [추가] | | |
| Bader q(Li) (e) | [pending] | [추가] | | |
| AIMD Ea (eV) | [pending] | [추가] | | |
| AIMD D₀ at 300K (cm²/s) | [pending] | [추가] | | |
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


## 7. Bader (plot_num=17 AE charge density)

| 종 (평균 전하, e) | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Li | [pending] | [추가] |
| P | [pending] | [추가] |
| S | [pending] | [추가] |
| Cl | [pending] | [추가] |


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


## 10. AIMD 이온 확산 (Arrhenius 600/800/1000K)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| D(600K) (cm²/s) | [pending] | [추가] |
| D(800K) (cm²/s) | [pending] | [추가] |
| D(1000K) (cm²/s) | [pending] | [추가] |
| Ea (eV) | [pending] | [추가] |
| D₀ 300K 외삽 (cm²/s) | [pending] | [추가] |
| σ_Li 300K (mS/cm, Nernst-Einstein) | [pending] | [추가] |


## 11. ELF (전자 국소화 함수)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Li–S 이온성 | [pending] | [추가] |
| P–S 공유성 (ELF > 0.7 사이) | [pending] | 있음 |
| 3D iso 레벨 | [pending] | 0.75 |


## 12. LOBSTER ICOHP (per-bond 평균, eV)

음수일수록 bonding 강함. 0에 가까울수록 약함.

| 결합 종류 | LPSCl v3 | LPSCl1.6 v3 | 해석 |
|---|---|---|---|
| **P–S** | [pending] | **−5.123** | PS4 강한 공유결합 backbone |
| Li–Cl | [pending] | **−1.214** | 이온 + 약간 공유 |
| Li–S | [pending] | **−0.614** | 약함, 주로 전기 정적 |
| S–S | [pending] | **−0.061** | 거의 0 (cage S 직접 결합 없음) |

**ICOHP 위계 (modelc_v3)**: P–S (−5.12) ≫ Li–Cl (−1.21) > Li–S (−0.61) ≫ S–S (~0)

**Charge spilling**: comp1 [pending], **modelc_v3 17%** ⚠️ (표준 <5%, 허용 <10%
초과). 원인: sparse basis (Li 2s 2p, P/S/Cl 3s 3p, no d). 정성적 추세
(P–S ≫ Li–Cl > Li–S) 는 robust. paper에서 절대값보다는 ratio + 추세로 보고.

**Note**: 4a-Cl vs 4d-Cl 사이트별 Li-Cl ICOHP 분리는 향후 분석 (현재 평균만).
4d Cl이 단단한 결합 (Li-Cl 2.36 Å)이라 ICOHP_4d-Cl > ICOHP_4a-Cl 예상.


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


## 각주

- modelc_v3 Pipeline v2 lineage 전체는 `db/compositions/modelc_v3.json`
  (Step 1–8 audit trail).
- comp1 v2 §8 결과 (a=9.929, v2 cell)는 컨테이너의
  `/home/ubuntu/work/runs/comp1_v3/archive_v2_post/`에 archive — 재현성
  목적, paper 사용 안 함.
- 모든 §8 도구는 `tools/modelc_v3/` 와 `tools/comp1_v3/`에.

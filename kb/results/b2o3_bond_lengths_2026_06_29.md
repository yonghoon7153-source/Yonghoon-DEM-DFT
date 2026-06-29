# B₂O₃-doped LPSCl1.6 챔피언의 결합길이 분석 (+ 4a/4d Cl 부분별 Li–Cl)

**날짜** 2026-06-29 · **구조** `db/structures/b2o3_relaxV0.cif` (DFT V₀ 고정셀 relax, 128 atom Li₅₈P₈S₄₁Cl₁₆B₂O₃)
**데이터** `db/properties/b2o3_bond_lengths.json`(핵심), `db/properties/b2o3_bond_lengths_full.json`(전체) · **그림** `docs/figures/cascade/b2o3_licl_distribution.png`
**도구** `tools/comp1_v3/b2o3_all_bond_lengths.py` · **방법** pure-numpy 최근접쌍 거리 통계(정확 triclinic minimum-image, 격자병진 −1..1 탐색). Cl 4a/4d 분류 = 각 Cl의 Li 배위수 Z(≤3.4 Å) ≥5→4a(8면체), <5→4d(반자리 anti-site).

> **한 줄.** 도핑 챔피언의 **골격 결합길이(P–S 2.065, Li–Cl 2.525, S–S cage 3.436)는 무도핑 Cl-rich LPSCl1.6과 거의 동일** → B₂O₃가 argyrodite 골격을 망가뜨리지 않음. 동시에 **새 지문 B–S 1.827(삼각 BS₃)·P–O 1.556(phosphate)** 가 또렷이 등장. **부분별 Li–Cl: 4d(2.391)가 4a(2.559)보다 ~0.17 Å 짧음** — 슬라이드의 LPSCl1.6 4a/4d 패턴(2.55/2.36, Δ0.19)과 정량적으로 일치.

---

## 1. 결합길이 표 (슬라이드 LPSCl·LPSCl1.6 vs 우리 b2o3)

| 결합 | LPSCl (슬라이드) | LPSCl1.6 (슬라이드) | **b2o3 (우리)** | 비고 |
|---|---|---|---|---|
| P–S | 2.073 | 2.064 | **2.065 ± 0.011** (n=29) | LPSCl1.6와 사실상 동일 |
| Li–S | 2.461 | 2.465 | **2.486 ± 0.107** (n=151) | 미세하게 김(+0.02) |
| Li–Cl | 2.607 | 2.532 (−3%) | **2.525 ± 0.152** (n=80) | LPSCl1.6와 일치(Cl-rich 수축) |
| S–S (cage) | 3.595 | 3.519 (−2%) | **3.436 ± 0.137** (n=45) | 더 수축(−5% vs LPSCl) |
| **B–S** | — | — | **1.827 ± 0.014** (n=6) | **NEW · 삼각 BS₃ (std 극소 → 잘 정의된 motif)** |
| **P–O** | — | — | **1.556 ± 0.005** (n=3) | **NEW · phosphate PS₄₋ₓOₓ (std 극소)** |

- **골격은 LPSCl1.6 그대로**: P–S 2.065(vs 2.064), Li–Cl 2.525(vs 2.532) — 도핑이 PS₄/Li–Cl 골격을 보존. B₂O₃는 일부 S를 **BS₃ + free-S²⁻ + phosphate** motif로 치환할 뿐 host를 왜곡하지 않음.
- **S–S cage 추가 수축**(3.436): Cl-rich/anti-site 점유 + B·O 주변 국소 변형으로 cage가 LPSCl1.6보다 더 조여짐.
- **새 지문 2개**: B–S 1.827(삼각 BS₃)·P–O 1.556(phosphate). **둘 다 std 0.01~0.005로 극소** = 단일·잘 정의된 결합 = artifact가 아닌 진짜 motif. 무도핑엔 아예 없는 결합 → **배위·DOS·ESW에서 본 BS₃+phosphate 서사를 결합길이로 재확인**.

## 2. 부분별 Li–Cl (4a vs 4d Cl)

| | LPSCl (슬라이드) | LPSCl1.6 (슬라이드) | **b2o3 (우리)** |
|---|---|---|---|
| 4a Cl | 2.61 (100%) | 2.55 (90%) | **2.559 ± 0.151** (12/16 = 75%) |
| 4d Cl | — | 2.36 (10%) | **2.391 ± 0.044** (4/16 = 25%) |
| Δ(4a−4d) | — | 0.19 | **0.168** |

- **4d가 4a보다 ~0.17 Å 짧음** — 슬라이드 패턴(0.19)과 정량 일치. 4d는 **반자리(anti-site) 사면체** 자리(Li 배위 Z<5)라 Li를 더 바짝 끌어당김 → 짧은 Li–Cl. 4a는 8면체 Cl[Li₆](Z≥5)라 길다.
- **4d 분율이 더 큼**: 우리 25%(4/16) vs 슬라이드 LPSCl1.6 10%. **Cl-rich anti-site 점유가 더 진행된 배열** — 이건 잘 알려진 **4a/4d Cl/S 자리섞임(site-disorder)** 으로, **Li 이동장벽을 낮추는 전도 향상 메커니즘**. MD에서 b2o3가 modelc보다 더 잘 전도(Ea 0.207<0.226)한 것과 정합.
- 4d의 std(0.044)가 4a(0.151)보다 작음 = 4d Li–Cl이 더 균일(좁은 anti-site 기하).

## 2.5 전체 결합길이 데이터 (`b2o3_bond_lengths_full.json`)

### (a) 양이온–음이온 결합 (진짜 화학결합)
| 결합 | mean ± std (Å) | [min, max] | n | 귀속 |
|---|---|---|---|---|
| **P–O** | 1.556 ± 0.005 | [1.549, 1.560] | 3 | phosphate (가장 짧고 가장 균일) |
| **B–S** | 1.827 ± 0.014 | [1.801, 1.846] | 6 | 삼각 BS₃ (2 B × 3 S) |
| **Li–O** | 1.911 ± 0.055 | [1.849, 2.010] | 6 | **NEW** · 단단한 O²⁻ 주변 Li (O 1개당 Li 2개) |
| **P–S** | 2.065 ± 0.011 | [2.045, 2.103] | 29 | thiophosphate PS₄ |
| **Li–S** | 2.501 ± 0.142 | [2.338, 3.126] | 155 | Li 배위 |
| **Li–Cl** | 2.525 ± 0.152 | [2.303, 3.213] | 80 | Li 배위 |

### (b) 음이온–음이온 접촉 (골격 기하)
| 접촉 | mean ± std (Å) | n | 의미 |
|---|---|---|---|
| S–S (cage) | 3.434 ± 0.164 | 65 | argyrodite cage |
| S–Cl | 3.922 ± 0.155 | 102 | 음이온 부격자 |
| Cl–Cl | 4.059 ± 0.235 | 9 | Cl–Cl 간격 |
| Li–Li | 2.949 ± 0.190 | 34 | Li hopping network 최근접 |

### (c) P 사면체 환경별 (PS₄ / PS₃O / PS₂O₂)
| 환경 | n(P) | P–S (Å) | P–O (Å) |
|---|---|---|---|
| **PS₄** | 6 | 2.065 | — |
| **PS₃O** | 1 | 2.064 | 1.560 |
| **PS₂O₂** | 1 | 2.075 | 1.554 |

→ O 3개가 **2개 P에 (2+1)로 분배** = 1 P는 PS₂O₂, 1 P는 PS₃O, 나머지 6 P는 순수 PS₄. O 치환 시 P–S 거의 불변(2.064~2.075) → phosphate 산소가 골격을 거의 안 흔듦.

### (d) S 종류별 Li–S (free-S / B-S / P-S bridging)
| S 종류 | n(S) | Li–S mean ± std (Å) | 의미 |
|---|---|---|---|
| **free-S²⁻** | 6 | **2.409 ± 0.062** (가장 짧음) | 경쟁 양이온 없음 → Li 강하게 끌어당김 |
| B–S | 6 | 2.508 ± 0.141 | 중간 |
| P–S (bridge) | 29 | 2.537 ± 0.148 (가장 긺) | P⁵⁺와 공유 → Li 약하게 |

→ **free-S²⁻의 Li–S가 가장 짧음(2.409)** = free-S가 가장 강한 Li 끌개. 이는 **DOS(free-S 3p가 가장 얕음=가장 반응성)·ESW(free-S 먼저 산화)** 와 정확히 정합 — free-S가 화학적으로 가장 "노출/활성".

## 3. 다른 결과와의 연결
- **배위/Voronoi**(BS₃ 5중 확증): B–S 1.827·P–O 1.556 결합길이가 그 motif의 정량 backbone.
- **MD**(b2o3 D↑, Ea 0.207): 4d Cl anti-site 분율 25%(>LPSCl1.6 10%) = site-disorder↑ → 전도↑와 정합.
- **EOS·탄성**: §4에서 상세 (결합길이 → 모듈러스 직결).

---

## 4. 결합길이 ↔ 탄성(elastic) 연결 — **핵심**

> **왜 연결되나.** 탄성 모듈러스는 에너지의 변형률 2차 곡률(∂²E/∂ε²)이고, 그건 결국 **개별 결합의 힘상수 k = d²E/dr²** 와 결합각 굽힘의 합산이다. **짧고 공유결합성 큰 결합일수록 k가 크다** → 그 결합이 많거나 짧아지면 모듈러스↑. 그래서 **결합길이 표는 탄성텐서의 미시적 "재료명세서"** 다.

### 4.1 두 층 역학 모델 (rigid backbone + soft glue)
결합길이가 명확히 **두 부류**로 갈린다 — 이게 argyrodite 역학의 핵심:

| 층 | 결합 (길이 Å) | 성격 | 역학 역할 |
|---|---|---|---|
| **단단한 공유 골격** | P–O 1.556, B–S 1.827, P–S 2.065 | 짧음·강공유·std 극소 | **압축(bulk) 저항** = 높은 진동수(788–1013 cm⁻¹ P–O), 골격 강성 |
| **무른 이온 접착** | Li–O 1.911, Li–S 2.501, Li–Cl 2.525 | 김·이온성·std 큼 | **전단(shear)에서 재배열** = 낮은 G, soft 모드(~14 cm⁻¹), ductile |

→ **단단한 PS₄/BS₃/phosphate 단위가 "벽돌", 무른 Li–S/Li–Cl이 "모르타르".** 압축엔 벽돌이 버텨 B(부피탄성)가 어느 정도 유지되고, 전단엔 모르타르(Li 부격자)가 흘러 G(전단탄성)가 낮음 → **B/G 큼 = ductile** = ASSB에 이상적(냉간가압·접촉유지).

### 4.2 도핑이 결합 차원에서 한 일 → 탄성 예측
무도핑 대비 b2o3가 바꾼 것:
1. **단단한 공유결합 추가**: B–S 1.827·P–O 1.556·Li–O 1.911 — 무도핑엔 **아예 없던** 짧고 센 결합. 국소적으로 골격 강성↑.
2. **S–S cage 수축**: 3.434 (vs LPSCl1.6 3.519 −2.4%, vs LPSCl 3.595 −4.5%). cage가 조밀 = 단위부피당 결합밀도↑ = 강성↑.
3. **Li 부격자는 무른 채 유지**: Li–Cl 2.525 ≈ LPSCl1.6 2.532, soft 모드 ~14 cm⁻¹ 그대로.

→ **예측**: (a) **B(부피탄성) 상승** — 실제로 **EOS B₀ = 24.48 GPa, 무도핑 modelC 21.7 → +2.8 GPa(+13%) DFT 확정**(`b2o3_eos_dft_result.json`). cage 수축 + 단단한 B–O/P–O가 미시적 원인. (b) **G는 덜 오름**(Li 부격자 무름 유지) → **ductility(높은 B/G·ν) 보존**. = "더 단단해지되 안 부서짐" = 이상적 SE 거동.

### 4.3 정량 탄성텐서와의 cross-check (relaxed-ion Cij, KISTI 진행중)
이미 무도핑 두 계의 **DFT 0K relaxed-ion 풀 Cij**가 있음(`db/properties/elastic.json`):

| 계 | B_VRH | G_VRH | **E_VRH** | ν | Zener A |
|---|---|---|---|---|---|
| LPSCl (comp1_v3) | 25.51 | 8.13 | **22.06** | 0.356 | 1.144 |
| LPSCl1.6 (modelc_v3) | 23.40 | 10.61 | **27.66** | 0.303 | 1.441 |
| **b2o3 (진행중, KISTI)** | — | — | **예측 ≥ 27.66** | — | 예측 ↑(anti-site↑) |

- **"vacancy paradox"**: clamped-ion(원자고정)에선 LPSCl≈LPSCl1.6 E가 거의 같았으나(둘다 ~52), **relaxed-ion(원자 이완 허용 = Born 이온차폐 포함)에서 비로소 LPSCl1.6이 E 27.66 > LPSCl 22.06으로 갈라짐** — 실험적 LPSCl1.6 강성화가 relaxed-ion에서 재현됨. → **b2o3 탄성은 반드시 relaxed-ion으로 비교**(clamped-ion 직관은 함정).
- **b2o3 예측**: ① cage 수축·단단한 phosphate/thioborate → **B ≥ modelc**, EOS +13%와 정합. ② **rigid phosphate 단위가 이온차폐(전단시 재배열)에 저항** → relaxed-ion에서도 E를 덜 떨어뜨림 → **E ≥ 27.66 예상**. ③ **4d Cl 분율 25%(>modelc 10%)·B/O 무질서 → Zener A(이방성) 더 커질 것**(modelc도 vacancy+anti-site로 1.441로 이방). 
- **검증**: KISTI 4-job 체인(relaxed-ion, conv_thr 1e-8, ±0.005 12 strain) 완료 → `fit_elastic_cij_stress.py` → B/G/E/ν/Zener 나오면 위 ①②③를 **정량 확인/반증**. E≥27.66·B≥23.4면 결합길이 서사 확정.

### 4.4 한 줄 요약 (elastic용)
**짧고 센 새 결합(B–S·P–O·Li–O) + cage 수축 = 골격 강성↑(B +13% 확정), 무른 Li 부격자 유지 = G 억제·ductile 보존.** relaxed-ion Cij가 E≥27.66을 주면 "도핑이 더 단단하되 더 잘 휘는 SE를 만든다"가 정량 확정됨.

## 5. 정직한 한계
- **결합길이→모듈러스는 정성·상관**(force-constant 직관)이지 Cij 대체가 아님 — 정량값은 relaxed-ion 탄성계산이 답.
- **vacancy paradox 주의**: DFT 0K **clamped-ion**은 LPSCl1.6 강성화를 놓침. 반드시 **relaxed-ion**(이온차폐 포함)으로 비교.
- **단일 Li-config**: 챔피언 1개 배열의 기하. 4a/4d 분율·Li–Cl 평균·이방성은 배열마다 다름(Li-ordering 1162 meV 스프레드).
- **4a/4d 분류는 기하 기준**(Li 배위 Z 컷오프 3.4 Å). 결정학적 Wyckoff와 100% 일치는 아니나, 슬라이드와 같은 정의(8면체 vs 반자리 사면체)로 일관 비교.
- Voronoi 부피(슬라이드 22.06/20.31)는 미계산 — 필요시 pymatgen `VoronoiNN`으로 추가 가능.

## 참고
- 데이터: `db/properties/b2o3_bond_lengths.json`(핵심), `b2o3_bond_lengths_full.json`(전체), `b2o3_eos_dft_result.json`(B₀), `elastic.json`(무도핑 Cij)
- 그림: `docs/figures/cascade/b2o3_licl_distribution.png` · 도구: `tools/comp1_v3/b2o3_all_bond_lengths.py`
- 관련: `kb/results/b2o3_champion_coordination_2026_06_29.md`(BS₃ 5중 확증), `b2o3_convex_hull_2026_06_29.md`, `b2o3_phonon_stability_2026_06_30.md`(soft 모드 ~14 cm⁻¹), `db/properties/b2o3_md_arrhenius.json`

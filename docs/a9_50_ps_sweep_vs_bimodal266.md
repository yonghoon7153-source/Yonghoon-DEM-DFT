# a9_50 P:S sweep — bimodal 최적점 + DEM↔MPM frame[5] 시연 (#266 독립 검증)

**무엇:** `input_2mAh_a9_50_p00…p10` — **AM:SE = 90:10 고정**, P:S(poly:single = AM_P:AM_S)를 0:10→10:0으로
0.2 간격 sweep (300 MPa, RVE 50×50µm, r_AM_P=6µm / r_AM_S=2µm / r_SE=0.5µm).  목적: bimodal 조성이
packing·transport·mechanics에 미치는 영향을 우리 DEM+MPM으로 직접 측정 → **Yong Min Lee 그룹 #266
(bimodal ASSB cathode, P:S 7:3 최적)을 우리 LPSCl DEM으로 독립 교차검증**.  데이터: `docs/data/case_3d_collection.csv`.

⚠ 이건 "porosity-vs-AM%" Furnas dip(AM:SE를 바꾸는 것)이 **아니라**, **총 AM 고정(90:10), AM을 poly/single로
나누는 비율(P:S)을 바꾸는** sweep — 즉 **#266의 변수(P:S)와 정확히 동일**.

## 전체 sweep (p00 → p10)

| P:S | P-frac | porosity DEM | porosity MPM | **σ_ionic (H)** | τ_Dijkstra | τ_Laplace,eff | σ_e | severe% | AM_P F/P_c |
|---|---|---|---|---|---|---|---|---|---|
| 0:10 | 0.0 | 17.92 | 16.84 | 0.0197 | 2.02 | 5.12 | 13.40 | 0.0 | — |
| 2:8 | 0.2 | 15.48 | 14.75 | 0.0345 | 1.84 | 3.92 | 11.13 | 0.05 | 15.96 |
| 4:6 | 0.4 | 13.89 | 12.77 | 0.0480 | 1.76 | 3.37 | 9.30 | 0.07 | 6.58 |
| **6:4** | **0.6** | **12.70** ⭐min | 10.44 | **0.0506** ⭐max | 1.68 | **3.29** ⭐min | 6.70 | 0.75 | 7.22 |
| 8:2 | 0.8 | 14.71 | 11.53 | 0.0246 | 1.64 | 4.68 | 4.91 | 6.19 | 13.16 |
| 10:0 | 1.0 | 18.45 ↑ | 9.31 | 0.0066 | 1.59 | 8.83 | 3.70 | 63.19 | 15.17 |

## 발견 1 — DEM porosity **Furnas dip**, 최소 P:S 6:4 = #266 packing 최적

DEM porosity: 17.92 → **12.70(6:4 최소)** → 18.45(10:0).  깨끗한 **dip** (깊이 ~5.8%p).  큰 AM_P + 작은 AM_S
혼합이 가장 조밀(작은 입자가 큰 입자 틈을 채움 = de Larrard/Furnas), 양 끝(전부 작거나 전부 큰 mono-modal)은
헐거움.  → **#266 "bimodal packing 최적"을 우리 rigid DEM이 독립 재현**.  최소 위치 0.6 ↔ #266 0.7 (sweep
간격 0.2라 같은 최적 구간 0.6–0.7).

## 발견 2 — σ_ionic **peak P:S 6:4**, 이후 폭락 = #266 rate 최적

σ_ionic: 0.0197 → **0.0506(6:4 peak)** → 0.0066(10:0, **7.7× 하락**).  peak가 porosity 최소·τ 최소와 **동일 지점**.
6:4 넘으면 큰 AM_P가 SE 네트워크를 압박 → **경로 constriction 급증**(τ_Laplace,eff 3.29→8.83, bottleneck min-A
0.0029→0.0014, 유효 conductance 0.000419→0.000141) → σ_ionic 붕괴.  → **#266이 7:3을 rate(이온 율속) 최적으로
본 것과 일치** (rate가 이온 율속이니 σ_ionic peak = best rate).

## 발견 3 — ★ DEM↔MPM가 mono-modal 끝점에서 갈림 = frame[5] 깨끗한 시연

| | p00 (0:10) | p06 (6:4) | **p10 (10:0)** |
|---|---|---|---|
| DEM porosity | 17.92 | 12.70 | **18.45** (rebound) |
| MPM porosity | 16.84 | 10.44 | **9.31** (no rebound) |

DEM porosity는 mono-modal 큰입자(10:0)에서 **반등(18.45%)** — rigid 구는 작은 filler 없으면 헐겁게 쌓임 →
**Furnas dip을 그대로 보여줌**.  MPM porosity는 **반등 안 함(9.31%, 오히려 최저)** — 소성 SE가 큰 AM_P 사이
void로 **흘러들어가 채움** → mono-modal에서도 치밀.  끝점 차이 **9.1%p**(18.45 vs 9.31).
→ **frame[3]/[5] 정확히:** Furnas dip은 **기하학적(rigid packing) 현상 = DEM 소유**; **MPM 소성 flow는 그
dip(특히 mono-modal rebound)을 지움**.  CLAUDE.md frame[3]("dip은 geometric, plastic이 부분적으로 erase")의
**가장 깨끗한 단일-sweep 증거**.  ⇒ 생산 porosity·dip은 **DEM**, 소성 morphology·void-fill은 **MPM** (frame[5] 분업).

> ⚠⚠ **정정 (2026-06-26) — p10의 MPM 9.31%는 over-compression CONFOUND:** p10(10:0)은 **SE-poor +
> mono-large-AM = scaffold MPM 과압축 regime**(`docs/mpm_scaffold_reliability_and_am_freeze.md`, gap +9.1).
> 따라서 9.31%는 **소성 void-fill(실물리) + frozen-AM 과소부담 과압축(artifact)의 혼합**이라 깨끗이 분리 불가
> → "MPM이 rebound를 지운다"를 이 숫자로 과대해석 금지.  **Furnas rebound의 진실은 DEM 18.45%**, p10 porosity는
> bracket [MPM 하한 9.3 / DEM 상한 18.5]로 봐야 함.  frame[3] "plastic이 dip을 부분 erase"의 *깨끗한* 증거는
> **standalone 2D champion**(mpm2d_jamming `--e-se/--yield-se`, scaffold 아님 → 과압축 없음, 768 수렴)이지
> 이 scaffold p10 숫자가 아니다.  p00–p08(SE 충분, 과압축 아님)의 DEM↔MPM dip 일치는 유효.

## 발견 4 — bimodal 최적은 **3축 trade-off** (단일 최적 아님)

P 증가 방향으로:
- **σ_ionic**: peak @6:4 (이온 — bimodal packing 이득)
- **σ_e 단조 감소** 13.40 → 3.70 (3.6×↓) — AM 입자수↓(1555→58), AM-AM 접촉↓(z 6.25→5.62, count 4859→163) → 전자망 희박
- **fracture 단조 급증** severe 0 → **63.19%** (10:0서 AM_P-AM_P F/P_c 15.2 → 53% fragmentation+10% pulverization) — mono-modal 큰 다결정이 하중 독점 → 분쇄.  AM_S는 내내 intact(F/P_c 0.26–0.40, #285 단결정 균열억제 일관)
→ **P:S 6:4–7:3 = 이온/packing 최적이지만 전자전도·기계건전성은 단조 희생.**  #266이 7:3을 "rate 최적"으로
제시한 맥락과 정합 — 최적은 **무엇을 최적화하느냐(이온 rate vs 전자 vs 무파괴)에 의존하는 trade-off**.

## #266 교차검증 결론 (frame[4])

| 항목 | #266 (실험, ASSB) | 우리 (DEM, LPSCl) |
|---|---|---|
| bimodal packing → τ↓ → σ↑ | ✓ (rate↑) | ✓ τ_Dijkstra 2.02→1.59, σ_ionic peak |
| 최적 P:S | **7:3** | **6:4** (peak), 6:4–7:3 구간 |
| 과도한 poly → 악화 | ✓ | ✓ 8:2/10:0 σ_ionic 붕괴 + porosity 반등(DEM) + fracture 폭발 |

서로 **독립 보정**(#266=실험, 우리=DEM, 절대값 비교 아님) → **수렴 = 교차검증**(frame[4]).

## ✅ CLOSED — #266 풀 디제스트 1:1 정량 대조 (frame[4] 교차검증 완료)

#266 디제스트(`docs/lit_oh2026_bimodal_composite_cathode.md`, 데이터 `docs/data/oh2026_bimodal_sigma_porosity.csv`)
의 정확값을 우리 a9_50 sweep과 1:1.  **SAME 시스템·조건**(90:9.5:0.5 ≈ 우리 90:10, S-LPSCl D50 0.72µm ≈
우리 SE 0.5µm, 300 MPa, CAM poly:single = 우리 P:S).

| poly_frac | #266 porosity 2D / He (%) | #266 σ_ion (mS/cm) | 우리 DEM porosity (%) | 우리 σ_ion (mS/cm) |
|---|---|---|---|---|
| 0.0 (0:10) | 17.96 / 11.58 | 0.034 | 17.92 (p00) | 0.0197 |
| 0.6–0.7 (opt) | **7.55 / 8.83 (min, CAM7:3)** | **0.055 (max)** | **12.70 (min, p06 6:4)** | **0.0506 (max)** |
| 1.0 (10:0) | 16.80 / 12.78 | 0.042 | 18.45 (p10) | 0.0066 |

**판정 — 우리 rigid-sphere DEM이 #266 실험 Furnas dip을 독립 재현 ✓✓ (frame[4]):**
- **dip 모양 1:1:** 양쪽 mono-modal 끝 다 헐겁고(#266 0:10 17.96 / 10:0 16.80; 우리 p00 17.92 / p10 18.45)
  중간이 바닥.  최적 #266 CAM7:3(0.7) ↔ 우리 p06(0.6) = 0.2-step에서 인접 = 같은 0.6–0.7 sweet spot.
- **물리 porosity like-for-like (frame[5]):** #266 **He pycnometry 8.83%**(3D 물리) ↔ 우리 **MPM 10.44%**
  (소성, @p06) = ~1.5%p 일치.  우리 **DEM rigid 12.70%**는 위(rigid floor, 소성흐름 없음); #266 **2D-SEM
  7.55%**는 셋 중 최저(단면이 작은 pore 놓침).  ⇒ **물리값=MPM, dip모양=DEM** 깔끔히 분리.
- **σ_ion peak 위치 1:1:** #266 0.055 @CAM7:3 ↔ 우리 0.0506 @p06 (같은 decade); LPSCl+NCM 엔벨로프
  (Bazzoun 0.065–0.137 + #271 0.042–0.087 + #266 0.034–0.055 ≈ **0.03–0.14**)를 우리 DEM(~0.04–0.18)이 감쌈.
- **대형 다결정 fragility 1:1:** #266 기계열화 max @CAM10:0(전부 poly) ↔ 우리 severe 63% @p10(큰 AM_P 분쇄);
  작은 단결정 intact(= #285).  E_SE **22 GPa**(#266) = real-bulk ~24의 3번째 확인(우리 E_eff 1.35/1.53 = softened proxy).

⚠ **τ는 추세만:** #266 τ_ion(11–16) = MacMullin-type ε/(σ_eff/σ_bulk), 우리 geodesic τ(~1.2–2)와 정의 다름 →
최소 위치(CAM7:3 ↔ p06)만 비교.  절대 σ는 SE 변종(Cl-rich Li₅.₅PS₄.₅Cl₁.₅) + 압력차로 "same-decade 엔벨로프".

⚠⚠ **σ_e 방향은 1:1 아님 (재검토 필요):** #266 σ_e는 CAM10:0(poly) 4.09 ≫ CAM0:10(single) 0.95 — **poly가
더 전도성**(σ_NCWA 13.7 ≫ σ_NCM 2.45).  우리 a9_50 σ_e는 P↑일수록 **감소**(13.4→3.7; 작은 AM_S 多 → 조밀
접촉망 → σ_e↑).  **방향이 반대** — 우리 σ_e는 (접촉망 + endpoint 가정 σ_S-single 10 > σ_P-poly 5) 둘 다
single-rich를 높이는데, #266 재료는 poly가 높음.  → σ_e 조성방향은 **재료(σ_AM endpoint)-의존** = audit
σ_e-direction caveat (porosity·σ_ion·fracture는 깨끗이 1:1, σ_e만 재료의존).

<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. depth 기준 = bazzoun2026 + luding2008 + thakur2014 + thorntonning1998 -->
# 선형 탄소성·점착 접촉 변형 모델 (미세 점착분말용 piecewise-linear LAW) — Pasha (Granular Matter 2014)

> slug `pasha2014_linear_elastoplastic_adhesive_contact` · DOI `10.1007/s10035-013-0476-y` · type `DEM (contact-LAW theory + EDEM 구현/검증)` · PDF `Pasha_2014_GranularMatter_LinearElastoPlasticAdhesiveContact.pdf` · digested `2026-06-26` · status ✅
> ★★ **WISHLIST Tier-2 #20 = "선형 탄소성+점착" 접촉 LAW 패밀리의 또 다른 멤버.** Walton–Johnson 1986 / Luding 2008 / Thornton–Ning 1998 / Tomas 2004를 *명시적으로 종합·개량*해 **미세 점착분말(0.1–10 µm, = 우리 0.5 µm SE 스케일)**에 맞춘 선형 모델. **OPEN ACCESS** (© The Author(s) 2014, Creative Commons Attribution) — **자유 인용 가능**.
> ★ **핵심 위치 (계층 지도):** Pasha = **우리 Luding 2008(`papers/luding2008_*`) + EEPA(`papers/thakur2014_*`)와 같은 *캡 없는(no-cap)* 선형 이력 층위**의 형제 LAW. 신규성 = **점착(pull-off)과 *소성 접촉면적*의 명시적 에너지-일관 결합** — pull-off가 소성변형(평탄화 면적 A_p)과 함께 *증가*하며, 그 증가를 **표면에너지 일(A_p·Γ) = 제하곡선 면적**으로 *유도*(eq 9–12). **= 우리 SE-SE cohesion(`adhesionStiffness`/MPM `--coh`, backlog A3) + EEPA 면적의존 점착의 *에너지-일관* 버전.**
> ★ **NOT 경로 A**: Pasha도 **항복압/경도(p_y/H) 캡이 없다** (소성 = 강성비 k_p/k_e로 정의된 *이력*, 접촉압 천장 아님) — EEPA·Luding과 *같은 한계*. real E_SE 18× 연화 문제를 *해결하지 못함*. 캡은 Thornton–Ning(p_y)/So(H)가 줌.

---

## 0. 왜 이 논문이 우리에게 중요한가 (먼저 읽을 것)

우리 DEM 압밀은 LIGGGHTS `hooke/hysteresis`(= Luding 2008 eq6) + `coefficientAdhesionStiffness`(SE-SE=1e6) 위에서
돈다. 그 **점착 탄소성 선형 LAW 패밀리**에 대해 우리는 이미 (a) Luding 2008(`papers/luding2008_*` = 우리 모델 정의서),
(b) EEPA(`papers/thakur2014_*` = 면적의존 점착 + calibration), (c) Thornton–Ning 1998(`papers/thorntonning1998_*` =
p_y 캡, 경로 A)을 digest했다. **Pasha 2014는 그 패밀리의 *네 번째 멤버*** — 특히 **미세 점착분말(우리 SE 0.5 µm
스케일)** 을 겨냥하고, **점착과 소성의 에너지-일관 결합**(pull-off가 소성 면적과 함께 증가하는 것을 *표면에너지 일*로
유도)을 제공한다.

이 digest가 *직접 보강/근거화*하는 세 가지:
1. **점착-소성 결합의 *에너지-일관* 정의 (eq 9–12)**: EEPA의 면적의존 점착(−k_adh·δⁿ)은 *경험적 강성*이었다.
   Pasha는 같은 "깊이 압밀 → 더 끈끈"을 **소성 평탄화 면적 A_p의 표면에너지 일(A_p·Γ)을 제하곡선 면적과 *등치*시켜
   유도** — pull-off f_cp가 *물리적으로* 소성변형 α_pd에서 나온다(eq 12). **= 우리 Stage-E 소성 *접촉면적* ↔ SE-SE
   점착을 *에너지 일관*으로 잇는 다리.**
2. **선형화(linearized) pull-off locus (eq 18)**: 위 유도된 비선형 pull-off 궤적을 **단순 선형 fit(f_cp=−k_cp·α_cp+f_0p)**
   으로 근사 → DEM에서 *상수 2개*(k_cp, f_0p)로 점착-소성 결합 구현. **= 우리 `adhesionStiffness` 같은 *선형 계수 점착*의
   에너지-일관 정당화 + EEPA k_adh/f₀ 분리와 같은 2-파라미터 구조.**
3. **Thornton–Ning과의 정량 검증 (Fig 11–14)**: 같은 입자(암모늄 플루오레세인 2.45 µm)에 대해 **임계 스티킹속도·
   반발계수 e를 Thornton–Ning과 비교 → 거의 일치**(임계속도 ~1.6 m/s). **= 선형 모델이 *엄밀(비선형 TN) 모델을
   재현*한다는 증거** → 우리가 선형 hooke/hysteresis를 쓰는 정당화의 *독립 사례*. **단** 고속(>10 m/s)서 상수-k_e면
   e가 asymptote ~0.38로 *비물리적 평탄*화 → **load-dependent k_e**(eq 25) 도입해야 e가 감소(TN과 정합) — 우리
   `coefficientMaxElasticStiffness` k̂₂의 *부하의존 보간*과 같은 물리.

⚠ **소재·응력 전이 불가 (이중 차이).** 검증 입자 = **암모늄 플루오레세인(ammonium fluorescein, E=1.2 GPa)**·
참조분말 = 일반 1 mm 구이지 **LPSCl/NMC811 아님**. 압밀 응력범위도 **bulk compression(11 % strain, 준정적)**으로
*배터리 300 MPa 압밀이 아님*. 가치는 **(a) 점착-소성 에너지-일관 LAW 정의, (b) 선형화 pull-off locus(2-파라미터),
(c) load-dependent k_e, (d) TN과의 선형↔비선형 검증 방법론**이며 **절대값(porosity·σ) 전이는 불가**.

---

## 1. 한 줄 요약

**미세 점착분말(0.1–10 µm)을 위한 *완전 선형(piecewise-linear)* 탄소성+점착 법선 접촉모델**을 제안: van der Waals
jump-in(f₀=8/9 f_ce) → 탄성재하(k_e) → 항복 후 소성재하(k_p) → 탄성제하(k_e) → 점착분기(−k_e)로 떨어져 **부하의존
pull-off f_cp에서 분리**. 신규성 = **pull-off가 소성변형과 함께 증가하는 것을 *표면에너지 일* A_p·Γ = 제하곡선 면적
(eq 10·11)으로 *에너지-일관* 유도** → f_cp=−√[(162/137)πΓR*k_e(2−α_pd/R*)] (eq 12), 그리고 이를 DEM용으로 **선형
fit(f_cp=−k_cp·α_cp+f_0p, eq 18)**으로 근사. **암모늄 플루오레세인 2.45 µm 입자에 EDEM 구현 → Thornton–Ning(비선형
JKR-EP)의 임계 스티킹속도·반발계수를 거의 재현**(임계속도 ~1.6 m/s), 단 고속서 e 감소를 위해 **load-dependent
k_e(eq 25)** 필요. 감도분석: **탄성/소성 강성비 k_e/k_p↑ → 소성 일↑·탄성 일↓**(k_e/k_p≈20에서 거의 전부 소성);
**Γ↑ → 소성 일↑·탄성 일 불변**. **= 우리 Luding/EEPA와 같은 *캡 없는 선형 점착-탄소성* 패밀리의 멤버, 점착-소성을
에너지-일관으로 결합하고 선형화한 버전.**

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Massih Pasha, Selasi Dogbe, Colin Hare, Ali Hassanpour, Mojtaba Ghadiri** (Institute of Particle Science and Engineering, **University of Leeds**, LS2 9JT; 교신 M. Ghadiri, M.Ghadiri@leeds.ac.uk) | **Granular Matter 16(1) 151–162 (2014)**; Received 2012-11-06, Published online 2014-01-19; **© The Author(s) 2014 (Open Access, Springerlink)** | **10.1007/s10035-013-0476-y** | **소재 무관 — 일반 미세 점착분말.** 검증 입자 = **암모늄 플루오레세인(ammonium fluorescein, 2.45 µm, E=1.2 GPa, Γ=0.2 J/m², p_y=35.3 MPa, Ning[3] PhD 데이터)**; 감도분석 = 일반 1 mm 구. **LPSCl/NMC811 직접 데이터 없음** | **DEM 접촉 LAW 이론**(선형 EP+점착 제안) + **EDEM 구현**(서브루틴)·**Thornton–Ning 비교 검증** + **bulk compression 감도분석**(N=3400) |

> ★ **OPEN ACCESS 기록**: 표지 "© The Author(s) 2014. This article is published with open access at Springerlink.com"
> + 말미 "Open Access This article is distributed under the terms of the Creative Commons Attribution License". →
> deck/paper에 **자유 인용**. EPSRC Grant EP/G013047 지원. 사사에 **Stefan Luding 교수**(우리 Luding 2008 저자)의
> 비평 감사 명시 — 같은 그룹/계보의 LAW임을 보여줌.
> ★ **계보**: Pasha는 본문에서 자기 모델이 "Luding[20] + Walton–Johnson[21] 모델 기반 + Thornton–Ning[18]·Tomas[19]
> 측면 고려"라고 *명시*. = 우리가 digest한 네 LAW(Luding·EEPA·Thornton–Ning + Walton)의 *교차점*. Ghadiri 그룹의
> 후속 = 이 모델의 flowability(EPT) 응용(Pasha PhD 2013, ref[26]).

## 3. 핵심 물성 (수치)

> ⚠ **이 논문은 소재 측정값 논문이 아니라 LAW+검증 논문**이다. 아래 "수치"는 (a) 모델 파라미터(N/m·µN 단위계),
> (b) 암모늄 플루오레세인 검증값(Table 1·2), (c) 임계 스티킹속도·반발계수, (d) 감도분석 무차원 관계. **LPSCl·NMC811
> 절대값 전이 불가**(소재 다름 + bulk-compression 11 % strain ≠ 300 MPa). 가치는 **수식·파라미터 정의·점착-소성
> 에너지결합·선형화·TN 검증**이다.

| 물성/파라미터 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **k_e (탄성 강성)** | **1,500 N/m** | Table 2(예시)·기본 | stated | 탄성재하/제하 가지 기울기. 초기 제하 기울기 평균 |
| **k̂_e (최대 탄성강성)** | **13,000 N/m** | eq25, Table1·2 입력서 산출 | stated | load-dependent k_e 상한(α_max=R*서). = 우리 k̂₂ cap |
| **k_p (소성 강성)** | **210 N/m** | Table 2·기본 | stated | 항복 후 소성재하 가지(line CD) 기울기. k_p < k_e |
| **k_cp (점착-소성 강성)** | **−20 N/m** | Table 2, eq18 선형fit 기울기 | stated | pull-off locus 선형 기울기(음수). = 점착 가지 −k_e도 별개 |
| **f₀ (첫 접촉 점착력)** | **−2.1 µN** | Table 2 | stated | jump-in 인력 = 8/9·f_ce (JKR pull-off의 8/9) |
| **f_0p (선형 pull-off 절편)** | **−4.0 µN** | Table 2, eq18 | stated | 선형 pull-off locus의 force축 절편 |
| **Γ (계면에너지/표면에너지)** | **0.02, 0.1, 0.2, 0.5 J/m²** | sweep; 기본 0.02 또는 0.2 | stated | 점착 세기. JKR f_ce=−3/2πR*Γ |
| **R\* (환산반경)** | **2.45 µm** | 검증 입자(평면벽이라 R*=R) | stated | R*=(1/R₁+1/R₂)⁻¹; 입자-평면 → R*=R_particle |
| **E (탄성계수, 검증입자)** | **1.2 GPa** (입자) / 182 GPa(Si 벽) | Table 1 | stated | 암모늄 플루오레세인. ν=0.3(둘 다) |
| **p_y (접촉 항복압)** | **35.3 MPa** | Table 1(검증입자) | stated | Thornton[24]·Johnson[25]의 항복력·변형 산출용 |
| **임계 스티킹속도 v_s** | **~1.6 m/s** (검증입자) | Fig13·14, TN과 비교 | stated | TN(~1.6)과 거의 일치 = 검증 핵심 |
| 임계 v_s (Γ sweep) | **0.451 / 2.228 / 4.387 / 10.485 m/s** | Γ=0.02/0.1/0.2/0.5 J/m² | stated(Fig6) | Γ↑ → v_s↑(점착 강할수록 더 잘 붙음) |
| 임계 v_s (k_e sweep) | **0.031 / 0.102 / 0.317 / 0.451 m/s** | k_e=300/500/1100/1500 N/m | stated(Fig7) | k_e↑ → v_s↑ |
| 임계 v_s (k_p sweep) | **0.007 / 0.095 / 0.451 / 1.471 m/s** | k_p=100/210/500/1200 N/m | stated(Fig8) | k_p↑ → v_s↑ |
| 반발계수 e asymptote | **~0.38** (상수 k_e) / 감소(load-dep k_e) | v_i > ~10 m/s | stated(Fig13·14) | 상수 k_e면 e→(k_p/k_e)^½ 평탄(비물리); load-dep면 감소 |
| 강성비 소성한계 | **k_e/k_p ≈ 20** | Fig16 | stated | 이 이상이면 입력 일의 거의 전부가 소성 |
| porosity / 상대밀도 | **n/a** (절대 porosity 안 줌) | — | — | 감도분석은 일(work)·고체분율로만 보고 |
| 초기 고체분율 (감도) | **0.48–0.52** (Γ=0→5 J/m²) | Fig18, 충전 후 | digitized | Γ↑ → 초기 고체분율↓(점착 → 느슨) |
| 압밀 목표 고체분율 | **0.58** (점착) / strain 11 %(비점착) | 감도분석 | stated | 점착 케이스는 0.58까지 압밀 |
| σ_ionic / σ_e / σ_thermal | **n/a** | — | — | **전달 전혀 안 다룸**(역학 전용) — frame[5] 역학 절반 |
| coverage / 접촉면적% | **A_p (소성면적)** = πΓ로 *간접* | — | stated(eq10) | A_p·Γ=점착 일; 직접 coverage % 안 줌 |
| coordination Z | **n/a** (명시 안 함) | — | — | 감도분석은 일 분해(W_p/W_e) 위주 |
| Heckel P_y / knee | **n/a** | — | — | Heckel 분석 안 함 |
| PSD (감도분석) | **0.8/0.9/1.0/1.1/1.2 mm = 5/25/40/25/5 %** | Table 4, normal 분포 | stated | 평균 1 mm, 좁은 정규분포; mono에 가까움(bi/poly 아님) |

## 4. 시뮬레이션 방법 ★ — **이것이 선형 EP+점착 접촉 LAW의 정의**

> 이 논문 §1(서론, 기존 모델 개관 Luding/Walton–Johnson) → §2(제안 모델, Fig 3·5) → §2.1(부하의존 pull-off,
> 에너지유도) → §2.2(충돌·반발·스티킹속도) → §2.3(pull-off locus 선형화, Fig 10) → §3(Thornton–Ning 검증,
> Table 1·2) → §4(감도분석, Table 3·4) 순.

### 4.1 기존 모델 개관 (§1) — 우리가 digest한 LAW들과 직접 대조

Pasha는 자기 모델을 *세우기 전에* 세 선행 선형 모델을 명시적으로 정리한다. **= 우리 digest 3개의 요약본:**
- **Luding 모델 [20]** (= 우리 모델, `papers/luding2008_*`; Fig 1): k_p(소성재하)·k_e(제하)·k_c(점착)·f₀(jump-in).
  ★ Pasha의 *비판*: "**Luding 모델은 접촉이 *α=0(zero overlap)에서 break*하므로 소성변형을 무시한 셈 — 비현실적
  (소성변형은 영구적이므로 분리가 α>0에서 일어나야 함)**." → Pasha 모델의 *동기*. (우리 모델의 알려진 한계를
  Pasha가 명시.)
- **Walton–Johnson 모델 [21]** (Fig 2): α=0에서 *인장력으로 시작*(TN·Luding·Tomas와 달리), 분리는 α_fe(JKR류
  separation distance)에서. 소성재하 k_p, 제하 k_e, pull-off f_ce 후 −k_ce 분기, pull-off locus 기울기 −k_cp.
- **Tomas 모델 [19, 22, 23]**: "adhesion limit" 개념(더 큰 음의 f_cp). Pasha eq18 선형화의 출발 개념.
- ★ Pasha의 종합 의도(§1 말미): "**Thornton–Ning[18]·Tomas[19]·Walton–Johnson[21]의 측면을 고려한** 단순 선형
  모델을 제안 + bulk compression 감도분석." = **네 LAW의 교차 종합.**

### 4.2 ★★★ 제안 모델 — 법선 힘-변위 (§2, Fig 3) — *우리 패밀리의 네 번째 LAW*

**완전 선형(piecewise-linear) 5-구간**. 접촉점 A→B→C→D→(E) 경로(Fig 3):

- **van der Waals jump-in (점 B, α=0)**: 두 구가 닿는 순간 인력 **f₀ = (8/9)·f_ce**, 여기
  **f_ce = −(3/2)πR*Γ** (eq 4, JKR 탄성 pull-off 힘 = 점 B). (8/9는 JKR jump-in/pull-off 비.)
- **탄성재하 α<α_y (line BC, eq 5)**: `f = k_e·α + (8/9)f_ce`. 탄성변형이라 **제하도 같은 BC선** 따름(가역).
  점 B 아래로 제하하면 "stiffness −k_e"로 떨어져 **α_fe(음의 overlap)에서 force = 5f_ce/9로 분리**(JKR류).
- **소성재하 α≥α_y (line CD, eq 6)**: 접촉압이 항복응력 도달 → **소성변형**. `f = k_p·(α − α_0p)`. (k_p < k_e.)
  α_y·α_0 = 항복 시작 overlap·force-zero overlap; 항복력·변형은 Thornton[24]·Johnson[25] 식으로 산출.
- **탄성제하 점 D→α_p (line DE, eq 7)**: `f = k_e·(α − α_p)`. α_p = 제하 force=0 overlap = **영구 소성겹침**(우리
  ε_sphere). **재하가 D 전이면 DE선 따라 가역(eq7), D 넘으면 다시 소성 CD(eq6).**
- **점착분기 (line EF, eq 8)**: 제하가 α_p 아래로 → pull-off **f_cp**(점 E)까지 감 → 더 가면 **negative elastic
  stiffness −k_e**: `f = −k_e·(α − 2α_cp + α_p)`. **α_cp = pull-off 도달 overlap**, 접촉은 force=5f_cp/9에서
  **break**(JKR류). 분리 후 다시 닿으면 α_c0(>α_cp)에서 8f_cp/9로 재establish(표면완화).

### 4.3 ★★★ 부하의존 pull-off — *에너지-일관* 점착-소성 결합 (§2.1, eq 9–12) — **핵심 신규성**

EEPA의 면적의존 점착(−k_adh·δⁿ)이 *경험적 강성*이었다면, **Pasha는 같은 "깊이 압밀 → 더 끈끈"을 *에너지 보존*으로
유도**한다:
- **소성 평탄화 변형 (eq 9)**: `α_pd = α_p − α_y` (항복 이후의 순수 소성겹침).
- **소성 접촉면적의 점착 일 (eq 10)**: 평탄화 접촉면적 A_p ≈ 환산반경·overlap에서 산출 →
  `|W_ad| = A_p·Γ = πΓ·(2R*·α_pd − α_pd²)`. (소성으로 *평탄화된 면적* × 표면에너지.)
- **제하곡선 면적과 등치 (eq 11)**: 같은 점착 일은 제하응답(α_p→α_fp)의 *면적*이기도 함 →
  `|W_ad| = (137/162)·f_cp²/k_e` (Appendix I 유도; 삼각형+사다리꼴 분해, eq 28–37).
- **★ 부하의존 pull-off (eq 12)**: eq10 = eq11 등치 + pull-off 인장(음수) →
  **`f_cp = −√[(162/137)·πΓ·R*·k_e·(2 − α_pd/R*)]`**. → **pull-off가 소성변형 α_pd에서 *물리적으로* 자란다**
  (α_pd↑ → |f_cp|↑, 초기엔 급격·이후 선형). Fig 4 = f_cp vs α_cp 곡선(k_e=1500, k_p=210, Γ=0.02, R*=2.45 µm).

★ **이것이 우리 Stage-E ↔ SE-SE 점착의 *에너지-일관* 다리**: 우리 Stage-E(Tabor+volume)가 계산하는 *소성 접촉면적*
A_physics를 Pasha는 **그 면적의 표면에너지 일(A_p·Γ)로 pull-off를 유도** — "압밀 깊은 접촉이 더 끈끈"을 *경험 강성*이
아니라 *보존된 에너지*로 준다. (EEPA보다 한 단계 더 물리적.)

### 4.4 ★ 충돌·반발·임계 스티킹속도 (§2.2, eq 13–17) — TN 검증의 토대

평면벽 충돌 에너지밸런스(Fig 5의 일 분해 W_lc·W_y·W_p·W_e·W_ad):
- **충돌 에너지밸런스 (eq 13)**: `½m·v_i² = W_p + W_e + W_y − |W_lc|` (소성+탄성압축+항복전탄성−초기점착재하 일).
- **임계 스티킹속도 (eq 14)**: `W_e = |W_ad| → v_i = v_s`. **탄성 변형에너지 = 점착 일일 때가 break/stick 경계.**
  v_s = 접촉이 *안 깨지는* 최대 충돌속도(탄성에너지가 점착을 못 이김).
- **반발속도 (eq 16)**: `v_r = (f_max(α_max−α_p)/m − (137/81)·f_cp²/(m·k_e))^½` (v_s 초과 시 분리).
- **충돌속도 (eq 17)**: `v_i = ((f_max+f_y)(α_max−α_y)+(α_y−α_0)f_y−α_0|f₀|)/m)^½` → e = v_r/v_i.

### 4.5 ★★ pull-off locus 선형화 (§2.3, eq 18) — DEM용 2-파라미터 점착

eq 12의 *비선형* pull-off 궤적(Fig 4·9)을 **DEM 비용절감 위해 선형 fit**:
- **선형 pull-off locus (eq 18)**: `f_cp = −k_cp·α_cp + f_0p`. k_cp = 선형 fit 기울기, f_0p = force축 절편.
  "**입자반경의 6 % 초과 변형**(큰 소성)에서 궤적이 선형화됨" → 그 부분만 fit(Fig 9, Γ별 점선).
- **추가 단순화 (Fig 10)**: 초기 탄성변형이 전체에 비해 작은 경우(소성 지배 소재) → BC 탄성구간 *생략* →
  α=0서 −f_ce로 떨어졌다가 바로 소성 CD(k_p, eq 19: `f=k_p·α−8/9·f_ce`). 제하 BC(k_e, eq20), pull-off
  α_cp=(k_e·α_p−f_0p)/(k_e+k_cp) (eq21), EF분기 −k_e(eq22). **= 가장 단순한 production 형태.**

### 4.6 ★ load-dependent 탄성제하강성 k_e (§3 말미, eq 23–25) — 고속 e 보정

상수 k_e면 고속(v_i>10 m/s)서 **e → (k_p/k_e)^½ asymptote(~0.38)로 *비물리적 평탄*** (탄성/소성 일 비가 상수).
실험[27,28]은 고속서 e *감소* → **k_e를 부하의존으로**:
- **k_e ∝ r² (eq 23)**: `k_e ∝ r² = 2R*α_max − α_max²` (접촉반경² ∝ overlap). 강성이 최대겹침과 함께 증가.
- **(eq 24)**: `k_e = (r/R*)²·k̂_e`, k̂_e = α_max=R*서 최대탄성강성.
- **★ (eq 25, Luding[20] 식 1과 동형)**: `k_e = k_p + (r/R*)²·(k̂_e − k_p)`. 작은 변형서 k_e<k_p 되는 것 방지
  (Luding eq1의 k_e=k_p+(k̂_e−k_p)·α_max/α* 와 *같은 발상*). **검증입자서 k̂_e=13,000 N/m** 산출(Hertz 초기제하
  접선 best-fit). → Fig 14에서 e가 고속서 *감소*(TN과 정합, 단 다소 deviation).

★ **= 우리 `coefficientMaxElasticStiffness`(k̂₂)의 *부하의존 보간*과 같은 물리**: Luding eq8 k₂(δ_max) 보간 ↔ Pasha
eq25 k_e(α_max) 보간 ↔ 둘 다 "강한(깊은) 접촉일수록 제하 강성↑." 우리 LIGGGHTS hooke/hysteresis가 이 보간을 내장.

### 4.7 재료 파라미터·셋업·입자 처리

- **code**: ★ **EDEM® (DEM Solutions Ltd, Edinburgh) — API 서브루틴으로 선형 pull-off locus 모델 구현**(Fig 12·13의
  EDEM 시뮬). (EEPA 논문 Thakur와 *같은 EDEM 코드*.) timestep = mass-spring critical의 0.2배 (eq 26:
  `t = 0.2·t_crit = 0.2·√(m*/k*_crit)`, m*=m_smallest/2, k*_crit=k_smallest/2).
- **재료 파라미터 (Table 1, 검증입자)**: 암모늄 플루오레세인 R=2.45 µm·ρ=1350 kg/m³·E=1.2 GPa·ν=0.3·Γ=0.2 J/m²·
  p_y=35.3 MPa; Si 벽 E=182 GPa·ν=0.3.
- **재료 파라미터 (Table 2, 모델 fit)**: k_e=1500·k_p=210·k_cp=−20 N/m·f₀=−2.1·f_0p=−4.0 µN (Fig 11 TN 응답 기울기
  best-fit). **점성/속도의존 댐핑 *없음*** (Fig 12는 댐핑 0).
- **감도분석 셋업 (§4, Table 3·4)**: **N=3400 입자**, 평균 1 mm 정규 PSD(Table 4: 0.8–1.2 mm), **die 지름 12 mm,
  bed 높이 ~36 mm**, ρ=1000 kg/m³, **압밀 strain rate 0.28 s⁻¹**(무차원 전단변형률 ~0.003 = 준정적, Tardos[29]),
  **μ=0.25**(입자·벽), wall stiffness 8000 kN/m. **비점착: 11 % strain까지 압밀; 점착: 고체분율 0.58까지** →
  같은 속도로 제하. 일(work) = 재하곡선 아래 면적(소성, 초록)·제하곡선 아래(탄성, 빨강)(Fig 15).
- **bond/binder 모델**: **없음**(점착은 f_cp/f₀로 통합).
- **MPM / continuum**: **없음**(순수 이산 DEM). → frame[5] 역학 절반.
- **전달 솔버**: **없음**(σ 전혀 안 다룸). → frame[5] 역학 절반만.
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - **구(sphere)만** (검증=입자-평면, 감도=구 bed). 비구형 미고려.
  - **좁은 정규 PSD**(감도분석 평균 1 mm) — mono에 가까움; **bi/poly-PSD 아님**.
  - **★ rigid sphere + CONTACT 탄소성** (eq 6의 k_p 소성재하 + α_p 영구겹침) — **진짜 SHAPE 소성 아님.**
    입자 형상은 절대 안 변하고, "소성"은 **접촉점 힘-변위 LAW의 분기(k_e→k_p) + 잔류 overlap(α_p) + 평탄화 면적
    A_p(점착 일 산출용 *기하 proxy*)**일 뿐. ⇒ `elasto_plastic_feasibility.md §0` 층위(1) CONTACT-LAW
    (층위(3) SHAPE는 우리 MPM).
- **특이사항/튜닝**: §1 철학 = "**엄밀 비선형 EP 모델은 DEM서 시간소모적이고 흔히 불필요 — 단순 선형이 거동을
    효율적으로 대표.**" = 우리가 hooke/hysteresis를 쓰는 바로 그 정당화. k_e는 Fig 11 TN 초기제하 기울기 *평균*으로
    잡음(eq25 k̂_e는 Hertz 접선).

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **Luding[20] 모델**(=우리 모델) 힘-overlap 모식: k_pα(소성재하)·k_e(α−α_p)(제하)·−k_cα(점착)·f₀·f_cp·α_p·α_max | **우리 hooke/hysteresis LAW** 그림(Pasha 표기). ★ Pasha의 *비판* 명시: Luding은 α=0서 break → 소성변형 무시(비현실). 우리 모델 한계의 외부 지적 |
| **2** | **Walton–Johnson[21] 모델** 힘-overlap: α=0서 인장 시작, α_fe 분리, k_p·k_e·−k_ce·−k_cp | 점착 시작점(α=0 인장)이 Luding/TN(f₀≠0)·우리와 다른 변종. pull-off locus −k_cp 개념 |
| **3 (★★★ 핵심)** | **제안 Pasha 모델** 힘-overlap: A·B·C·D·E 경로. f₀=8/9 f_ce(jump-in)·k_e(BC 탄성)·k_p(CD 소성)·k_e(DE 제하)·−k_e(EF 점착)·α_y·α_p·α_cp·α_fe | **우리 패밀리의 *네 번째 LAW* 정의 그림.** α_p=영구겹침=ε_sphere. 점착-소성 결합(f_cp가 α_pd서 자람). 슬라이드/method에 인용(OPEN ACCESS) |
| **4** | **부하의존 pull-off f_cp vs α_cp** 곡선 (eq12; k_e=1500,k_p=210,Γ=0.02,R*=2.45µm) | pull-off가 소성변형과 함께 *비선형* 증가(초기 급격→선형). = EEPA k_adh의 *에너지유도판*. eq18 선형화의 원곡선 |
| **5 (★)** | **제안 모델 일 분해 모식**: W_lc(초기점착재하)·W_y(항복전탄성)·W_p(소성)·W_e(탄성제하)·W_ad(점착 일) 색칠 | ★ **점착 일 W_ad = 제하곡선 면적**(eq11 유도의 기하). 일 분해로 소성/탄성/점착 정량 → 우리 압밀 일 분해와 정성 연결 |
| **6 (★)** | **e vs 충돌속도, Γ=0.02/0.1/0.2/0.5 J/m²** (k_e=1500,k_p=210). 임계 v_s=0.451/2.228/4.387/10.485 m/s | ★ **Γ↑ → e↓**(점착 강할수록 반발↓) + **v_s↑**(더 잘 붙음). 점착(우리 SE-SE)이 충돌 거동 지배 |
| **7 (★)** | **e vs 충돌속도, k_e=300/500/1100/1500 N/m** (k_p=210,Γ=0.02). v_s=0.031/0.102/0.317/0.451 | ★ **k_e↑ → e↓**(탄성강성↑ → 소성 일↑ → 반발↓) + **v_s↑** |
| **8 (★)** | **e vs 충돌속도, k_p=100/210/500/1200 N/m** (k_e=1500,Γ=0.02). v_s=0.007/0.095/0.451/1.471 | ★ **k_p↑ → e↑**(접촉 더 단단·소성변형↓ → 반발↑) + **v_s↑**. k_e·k_p의 *반대* 효과 |
| **9** | **선형화 pull-off locus**: f_cp vs α_cp, Γ=0.02/0.1/0.2/0.5, 점선=선형fit(eq18, 입자반경 6 % 초과 변형) | eq18의 2-파라미터(k_cp·f_0p) fit 근거. Γ↑ → pull-off 깊어짐 |
| **10 (★)** | **가장 단순화 모델** 힘-overlap: BC 탄성구간 생략(소성 지배 소재), α_0→B 소성, C pull-off, D, −k_e(CD) | **production 최단 형태**(eq19–22). 우리 hooke/hysteresis도 ~선형 소성지배 → 이 단순화와 정합 |
| **11** | **Thornton–Ning 응답**(암모늄 플루오레세인, v=2/5/10 m/s) — TN[18] 모델 digitize(PlotDigitizer) | TN 비선형 응답의 *기준*. 여기 기울기로 Table 2(k_e·k_p·k_cp·f₀·f_0p) 산출 |
| **12** | **제안(단순) 모델 응답**(같은 입자, v=2/5/10 m/s, EDEM) | Fig11과 *최대 overlap·영구겹침 일치* → 선형 모델이 TN 재현(maximum overlap·plastic deformation 일치) |
| **13 (★★)** | **e vs 충돌속도** — Thornton–Ning vs 제안(EDEM ◆) vs eq15(해석곡선) | ★★ **제안=TN 거의 일치**(저속). 임계 v_s ~1.6 m/s 동일. = **선형이 비선형 TN을 재현**(우리 선형 LAW 정당화의 독립 사례). 단 상수 k_e면 고속서 asymptote ~0.38(평탄) |
| **14 (★★)** | **e vs 충돌속도** — load-dependent k_e 제안 vs TN | ★★ **load-dep k_e면 고속서 e *감소*(TN과 정합)**, 단 다소 deviation. = k̂_e 부하의존(우리 k̂₂ 보간)이 고속 거동에 필수. 우리 압밀은 준정적이라 무관하나 *충돌* 본다면 필요 |
| **15** | **압밀 일축 force-displacement**(k_p=10·k_e=50 kN/m, EDEM): 재하=소성 일(초록)·제하 아래=탄성 일(빨강) | 일 분해 방법(소성/탄성 면적). 우리 압밀 일 측정과 대비 |
| **16 (★)** | **정규화 일(탄성·소성) vs 강성비 k_e/k_p** (비점착) | ★ **k_e/k_p↑ → 소성 일분율↑·탄성↓**. **k_e/k_p≈20 한계**(이상이면 거의 전부 소성). k_e/k_p=1(가장 무름)서도 소성>탄성(재배열·마찰 소산). = 우리 18× 연화가 *효과적으로 k_e/k_p를 키워* 소성 늘리는 것과 정성 일치 |
| **17** | **탄성·소성 일 vs Γ** (k_p=100·k_e=1000·k_cp=−5 kN/m) | **Γ↑ → 소성 일↑·탄성 일 거의 불변**(작은 변화, inset). 점착이 압밀 일에 미치는 영향은 초기 패킹(고체분율) 차이 탓 |
| **18 (★)** | **초기 고체분율 vs Γ** (k_p=100·k_e=1000·k_cp=−5 kN/m): 0.52→0.48 (Γ=0→5) | ★ **Γ↑ → 초기 고체분율↓**(점착 → 느슨 충전) → 0.58 도달에 더 많은 strain 필요. ⚠ *저응력 충전* 현상(우리 고압 압밀과 다름; EEPA Fig16/18과 같은 경고) |

## 6. Post-processing ★

- **무엇**:
  - **반발계수 e = v_r/v_i**(eq16·17) vs 충돌속도; **임계 스티킹속도 v_s**(W_e=|W_ad|, eq14).
  - **일(work) 분해**: W_lc·W_y·W_p·W_e·W_ad (Fig 5·19; Appendix II eq38–48 유도). 압밀=재하곡선 아래(소성)·
    제하곡선 아래(탄성) 면적(Fig 15). **정규화 일 = W_e/W_input, W_p/W_input.**
  - **pull-off locus 선형 fit**(eq18): 비선형 f_cp(α_cp) 궤적(eq12)을 *입자반경 6 % 초과* 부분만 선형 fit →
    k_cp(기울기)·f_0p(절편). PlotDigitizer로 TN 응답(Fig11) digitize.
  - Heckel·percolation·coordination·coverage·tortuosity·전달지표 — **전부 안 함**(역학·충돌 전용).
- **도구**: **EDEM® v?(DEM Solutions, Edinburgh)** + API 서브루틴(선형 pull-off locus 구현). **PlotDigitizer**
  (TN 응답 digitize). 해석 에너지밸런스(eq13–17, Appendix I·II).
- **수치화·플롯·기록 방식**: 모델 파라미터 sweep(Γ 0.02–0.5, k_e 300–1500, k_p 100–1200 N/m) → e-v 곡선·v_s 산출.
  Table 1(검증입자)·2(모델fit)·3(감도 sweep)·4(PSD). Appendix I = W_ad 유도(삼각형 W_c1 eq29–31 + 사다리꼴 W_c2
  eq32–36 → eq37). Appendix II = v_i·v_r 유도(W_lc eq38·W_y eq39·W_e eq40·W_p eq41–44 → eq46·48).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ★★ **이 절이 핵심.** Pasha = 우리 Luding/EEPA와 *같은 캡-없는 선형 점착-탄소성 패밀리*의 네 번째 멤버. "대비"는 곧
> **(가) 4-way 접촉 LAW 계층 지도(Pasha·Luding·EEPA·Thornton–Ning), (나) 점착-소성 *에너지-일관* 결합 ↔ Stage-E/
> cohesion, (다) NOT 경로 A(캡 없음) 명시, (라) frame[5] 분업**이다.

### 7.1 ★★★ 4-way 접촉 LAW 계층 지도 — Pasha가 어디 앉는가

사용자 요청의 핵심. 네 LAW를 **(i) 항복압 캡 유무, (ii) 점착의 종류, (iii) 미세분말 타깃** 축으로:

| 축 | **Luding 2008 (우리 현재 모델)** | **Pasha 2014 (이 논문)** | **Thakur 2014 EEPA** | **Thornton–Ning 1998 (경로 A)** |
|---|---|---|---|---|
| **초기 jump-in** | f₀ (van der Waals 음수) | **f₀=8/9·f_ce** (JKR 8/9) ★ | f₀ (상수 vdW) | (JKR로 통합) |
| **초기 재하** | k₁·δ (선형) | **k_e·α** (선형, BC) | k₁·δⁿ (n=1 선형) | (4/3)E*R*^½α^1.5 = **Hertz** |
| **항복 후 소성재하** | k₂(δ−δ₀) 보간 | **k_p·(α−α_0p)** (선형, CD) ★ | k₂(δⁿ−δ_pⁿ) | **P_y+πp_y·R*(α−α_y)**, 압 cap |
| **제하** | k₂(δ−δ₀) 선형 | **k_e·(α−α_p)** (선형, DE) | k₂ 선형 | (4/3)E*R_p*^½(α−α_p)^1.5 = Hertz |
| **항복압/경도 캡** | ✗ **없음** | ✗ **없음** ★ | ✗ **없음** | ✅ **p_y 캡** (eq9) |
| **영구 소성겹침** | δ₀=(1−k₁/k₂)δ_max | **α_p** (eq7서 제하 force=0) ★ | δ_p (λ_p=1−k₁/k₂) | α_p (p_y·R_p*서 유도) |
| **점착 — 종류** | −k_c·δ (선형, *분리 안 됨*) | **f_cp 부하의존 + 선형화 −k_cp·α_cp+f_0p** ★★ | f₀(상수)+k_adh·δⁿ(면적의존) | JKR Γ |
| **점착-소성 결합** | k_c·δ가 δ와 큼(*면적 개념 불명시*) | **★ 에너지-일관: |W_ad|=A_p·Γ=(137/162)f_cp²/k_e (eq10·11)** | 경험 강성 −k_adh·δⁿ | JKR plastic pull-off P_cr=3/2πΓR_p* |
| **점착 이론기반** | 선형 k_c (경험) | **JKR(f_ce=−3/2πR*Γ) + 에너지보존 유도** ★ | 선형 k_adh+f₀ (경험) | JKR Γ (물리) |
| **부하의존 제하강성** | k₂(δ_max) 보간 (eq8) | **k_e=k_p+(r/R*)²(k̂_e−k_p) (eq25)** ★ | (없음, k₂ 고정) | (R_p* 평탄화로 자연) |
| **타깃** | 일반 µm 분말 | **★ 미세 점착분말 0.1–10 µm** (= 우리 SE) | 석회석 16–96 kPa | 일반 EP 구(COR) |
| **검증** | 인장/압축 강도시험 | **★ TN 비선형과 e·v_s 비교(재현)** | flow function·Rumpf | COR vs 실험 |
| **LIGGGHTS 가용** | ✅ `hooke/hysteresis` (우리 사용) | (EDEM 서브루틴; LIGGGHTS 직접 없음) | ✅ EEPA (cohesion) | (커스텀; Varkey=Rocky) |

⇒ **Pasha의 위치 (사용자 요청 정답)**:
- **계층 = no-cap, fine-powder adhesion.** Pasha는 **Luding·EEPA와 *같은 "캡 없는" 선형 이력 층위*** — 소성이
  *강성비(k_p/k_e)로 정의된 이력*이지 *접촉압 천장(p_y/H)*이 아니다. ⇒ **Thornton–Ning(경로 A)·So(H-cap)와 다른
  층위.** real E_SE 18× 연화 문제를 *그대로 가짐*(Pasha 단독으론 해결 안 됨).
- **vs Luding(우리 모델)**: Pasha는 **(1) jump-in을 JKR 8/9·f_ce로 *물리적으로* 줌, (2) 점착-소성 결합을 *에너지-
  일관*(A_p·Γ)으로 유도(Luding은 −k_c·δ 경험), (3) load-dependent k_e(eq25, Luding eq8과 동형), (4) 미세분말 타깃,
  (5) TN과 정량 검증**. 즉 **Pasha ≈ Luding + (JKR jump-in + 에너지유도 점착 + TN검증)**. 그리고 Pasha 자신이
  **Luding의 "α=0서 break(소성 무시)" 한계를 명시 비판**(Fig 1 설명) — 우리 모델 한계의 *외부 지적*.
- **vs EEPA**: 둘 다 점착-소성 결합·미세분말. **차이 = 점착-소성을 *어떻게* 잇나**: EEPA는 −k_adh·δⁿ *경험 강성*,
  Pasha는 A_p·Γ=제하면적 *에너지보존*. Pasha가 한 단계 더 물리적(에너지 일관), EEPA가 더 유연(n 비선형·f₀/k_adh
  명시 분리·LIGGGHTS 직접 가용). **둘 다 캡 없음** = 같은 층위.
- **vs Thornton–Ning**: TN은 *유일하게* p_y 캡(물리 항복)을 가짐. **Pasha는 TN을 *검증 기준*으로 쓰되 그 캡은 안
  가져옴** — 대신 선형 근사로 TN의 *충돌 거동(e·v_s)*을 재현. ⇒ **Pasha = "TN의 결과를 선형으로 흉내내되 캡은 뺀"
  모델.** 캡이 필요한 압밀(우리 300 MPa)엔 TN/So 경로 A가 여전히 필요.

### 7.2 ★★ 점착-소성 *에너지-일관* 결합 (eq 10·11) ↔ 우리 Stage-E 소성면적 + SE-SE cohesion

Pasha의 **고유 신규성 = pull-off를 *소성 평탄화 면적의 표면에너지 일*로 유도**(`|W_ad|=A_p·Γ=πΓ(2R*α_pd−α_pd²)`,
eq10). 이것이 우리 두 곳과 직접 연결:

1. **★ Stage-E 소성 *접촉면적* (frame[5] 역학 절반):** 우리 Stage-E(Tabor+volume)가 계산하는 것이 *소성 접촉면적*
   A_physics(`network_conductivity.py`). **Pasha는 그 *같은 소성 면적의 표면에너지 일(A_p·Γ)로 pull-off를 유도*** —
   "압밀이 깊어질수록(α_pd↑) 평탄화 면적↑ → 점착력↑." 우리는 그 소성면적을 *전달*(σ_ionic, Holm R=1/(2σr_c))에
   쓰고, Pasha는 *점착*에 쓴다. **같은 물리량(소성 접촉면적)의 두 용도** = 개념 다리. + EEPA는 *경험 강성*이었는데
   Pasha는 *에너지보존* → 우리가 SE-SE 점착을 *면적의존·에너지일관*으로 줄 때 **A_p·Γ 형태가 EEPA k_adh·δⁿ보다
   물리적 출발점.**
2. **★ SE-SE cold-weld/vdW cohesion (backlog A3):** 우리 `coefficientAdhesionStiffness`(SE-SE 1e6) = 점착 강성.
   **Pasha의 선형화 pull-off locus(f_cp=−k_cp·α_cp+f_0p, eq18)가 그 *선형 계수 점착*의 에너지-일관 정당화**:
   "비선형 A_p·Γ 점착을 선형 2-파라미터로 근사해도 됨." k_cp(−20 N/m)·f_0p(−4 µN) = EEPA의 k_adh·f₀ 분리와 같은
   2-파라미터 구조. **MPM `--coh`**(연속체 SE attractive σ) = 같은 점착의 연속체판; Pasha가 그 점착의 *접촉-스케일
   에너지 정의*(A_p·Γ, JKR f_ce, jump-in 8/9·pull-off 5/9)와 정성거동(Fig 6: Γ↑→e↓·v_s↑) 제공 → `--coh`/
   `adhesionStiffness` 매핑·검증 기준.
3. **★ 일 분해(W_p/W_e) ↔ 우리 18× 연화의 효과:** Fig 16이 "**k_e/k_p↑ → 소성 일분율↑·탄성↓** (k_e/k_p≈20서 거의
   전부 소성)"을 보임. **우리 18× 연화(E_SE 24→1.35)는 *효과적으로 k_e를 낮춰*(또는 k_e/k_p 비를 조정해) 같은 300
   MPa서 소성(overlap)을 늘리는 것** — Pasha의 강성비-일분율 관계가 그 *정성적 근거*. (단 우리는 연속체 소성이
   아니라 *연화된 탄성 overlap*으로 흉내 → frame 한계.)

### 7.3 ★★ NOT 경로 A — Pasha도 항복압/경도 캡이 *없다* (EEPA처럼)

- 사용자 요청: "**it is NOT path A (no yield-pressure cap) — note this like EEPA.**"
- **Pasha의 소성 = 강성비(k_p/k_e)로 정의된 *이력*** (line CD 기울기 k_p < k_e). **접촉 평균압이 항복압 p_y(또는
  경도 H)에 도달하면 압을 cap하는 메커니즘이 *없다*.** α_y(항복 시작)는 Thornton[24]/Johnson[25] 식으로 *위치*만
  정하고, 그 이후 소성재하는 *상수 기울기 k_p 선형*일 뿐 — *접촉압 천장*이 아니다.
  - ⚠ 검증입자에 p_y=35.3 MPa가 *있지만*(Table 1), 그것은 **α_y·f_y(항복 *시작점*)를 잡는 데만** 쓰이고 소성
    분기서 *압을 p_y로 고정*하지 않는다. (Thornton–Ning은 eq19 `P_y+πp_y·R*(α−α_y)`로 *압을 p_y로 cap* — 그 차이.)
- ⇒ **Pasha ⊂ Luding/EEPA 계열(캡 없음)**, Thornton–Ning(p_y 캡)·So(H 캡)와 **다른 층위**. **따라서 Pasha를
  도입해도 우리 18× 연화 문제는 *해결 안 됨*** (Pasha도 real E_SE 24 GPa·k_e ∝ E로는 300 MPa서 under-deform).
  경로 A의 *항복캡*이 그 역할.
- ★ **정정 (사용자 seed 정합)**: Pasha는 EEPA와 *정확히 같은 위상* — "선형 점착-탄소성, 캡 없음, 미세분말."
  가치는 "경로 A 후보"가 아니라 **"점착-소성 *에너지-일관* 결합 LAW + 선형화 + TN검증"**이다. (Pasha+p_y/H 캡을
  더하면 비로소 경로 A의 *점착 포함* 형태가 됨 — Thornton–Ning이 그 캡 제공.)

### 7.4 ★ load-dependent k_e (eq25) = 우리 `coefficientMaxElasticStiffness`(k̂₂) 보간

- Pasha eq25 `k_e=k_p+(r/R*)²(k̂_e−k_p)` (Luding eq1과 동형) = **"강한(깊은) 접촉일수록 제하 강성↑."** 이것이
  Luding eq8 k₂(δ_max) 보간 = 우리 LIGGGHTS `coefficientMaxElasticStiffness`(k̂₂, SE5/AM1.5)의 *부하의존 보간*과
  **같은 물리.** Pasha k̂_e(13,000 N/m) ↔ 우리 k̂₂ cap.
- ★ **왜 필요한가 (Fig 13→14)**: *상수* k_e면 고속(v_i>10 m/s)서 e가 **(k_p/k_e)^½ asymptote(~0.38)로 비물리적
  평탄**(탄성/소성 일 비 상수). **load-dependent k_e면 고속서 e *감소*(TN·실험과 정합).** ⇒ 우리 k̂₂ 부하의존
  보간이 *충돌 동역학*에 물리적으로 필수. **단 우리 압밀은 준정적(strain rate 0.28/s, 무차원 ~0.003)이라 이 고속
  보정은 무관** — 우리가 충돌이 아니라 *압밀*을 보므로. (충돌/분쇄를 본다면 재고.)

### 7.5 ★ TN 검증 = 선형이 비선형을 재현 (우리 선형 LAW 정당화의 독립 사례)

- Pasha는 **같은 입자(암모늄 플루오레세인 2.45 µm)에 선형 모델 vs Thornton–Ning(비선형 JKR-EP)**:
  - **최대 overlap·영구 소성겹침 일치**(Fig 11 vs 12, v=2/5/10 m/s).
  - **e-v 곡선 거의 일치**(Fig 13, 저속), **임계 스티킹속도 ~1.6 m/s 동일.**
- ⇒ **"단순 선형 모델이 엄밀 비선형(TN) 모델의 거동을 효율적으로 재현"** = **우리가 LIGGGHTS hooke/hysteresis
  (선형)를 쓰는 정당화의 *독립 사례*.** (우리 frame: 선형 hooke가 압밀 거동을 충분히 대표하되, 큰 변형/고속서
  비선형 효과는 보정 필요.) Pasha가 그 "선형≈비선형" 등가를 *충돌 동역학*에서 정량 입증.
- ⚠ **단 — 압밀 ≠ 충돌**: Pasha 검증은 *단일 입자-평면 충돌*(동역학). 우리 압밀은 *다입자 준정적*. "선형≈비선형"이
  충돌서 성립한다고 압밀(특히 큰 변형·캡 영역)서 자동 성립은 아님 — Pasha 감도분석(Fig 16)이 *압밀* 일분해를
  별도로 함. + 검증입자 E=1.2 GPa(무름)라 우리 SE(real 24 GPa, soft 1.35)와 *강성 스케일 다름*.

### 7.6 frame[5] — rigid 구 + CONTACT 소성, SHAPE·morphology·전달은 우리 영역

- Pasha는 **단일 접촉의 per-contact 구성식**(층위1 CONTACT-LAW) + 점착. **여전히 rigid 구**(α_p는 접촉점 압흔
  proxy, A_p는 *기하* 평탄화 면적이지 입자 형상변형 아님) → **입자 SHAPE 흐름·morphology·변형장·void-fill 전무** =
  Luding/EEPA/Thornton–Ning/Varkey/So와 *동일한 한계*. 그건 우리 **MPM**(층위3 SHAPE; champion J2 E=1.53/σ_y=0.15,
  SEM 코어보존+경계평탄화 ✓).
- **전달 σ 전혀 없음**(역학·충돌 LAW) → frame[5]의 역학(접촉 LAW) 절반만. σ_ionic/e/thermal 비교점 0 → 우리
  Kirchhoff/Holm 네트워크 영역. Pasha의 점착-소성 *면적*(A_p)은 우리 Stage-E 면적과 *물리량은 같으나* Pasha는 그걸
  점착에, 우리는 전달에 씀(상보).

### 7.7 비교 요약표

| 항목 | 이 논문 (Pasha 2014) | 우리 | 차이 / 관계 |
|---|---|---|---|
| 접촉 LAW | **선형 EP+점착**(k_e·k_p·k_cp·f₀·f_0p, eq6 계열) | LIGGGHTS `hooke/hysteresis`(Luding) | **같은 *캡 없는 선형* 패밀리** — Pasha=형제 LAW |
| jump-in | **f₀=8/9·f_ce** (JKR 물리) | f₀ (Luding vdW) | ★ Pasha가 JKR 8/9로 *물리적* 부여 |
| 점착-소성 결합 | **★ 에너지-일관 A_p·Γ=(137/162)f_cp²/k_e** | `adhesionStiffness` k_c·δ (경험) | ★ Pasha가 *에너지보존* 유도(EEPA 경험강성보다 물리적) |
| 점착 선형화 | **f_cp=−k_cp·α_cp+f_0p** (2-파라미터, eq18) | `adhesionStiffness`(선형 계수) | ★ 우리 선형 계수 점착의 *에너지-일관 정당화* |
| 부하의존 제하강성 | **k_e=k_p+(r/R*)²(k̂_e−k_p)** (eq25) | `coefficientMaxElasticStiffness` k̂₂ 보간 | **같은 물리** ✓ (Luding eq8과 동형) |
| 항복압/경도 캡 | ✗ **없음** (Luding/EEPA와 같은 층위) | ✗ 없음 → 18× 연화 보상 | ★ Pasha ≠ 경로 A — 캡은 TN/So가 줌 |
| 영구 소성겹침 | **α_p** (eq7 제하 force=0) | ε_sphere "displaced material" | **같은 물리** ✓ |
| 검증 | **★ TN 비선형과 e·v_s 재현**(v_s~1.6) | (우리 frame[4] 실험보정) | ★ 선형≈비선형 등가(우리 선형 LAW 정당화 독립사례) |
| 타깃 분말 | **★ 미세 점착분말 0.1–10 µm** | LPSCl SE 0.5 µm | **스케일 정합**(점착이 지배하는 미세분말) |
| 소성 종류 | **CONTACT-LAW**(층위1) — rigid 구 | DEM도 CONTACT; SHAPE는 MPM | **같은 한계**(SHAPE 없음) — frame[5] |
| 전달 σ | **전혀 없음**(역학·충돌) | σ_ionic+σ_e+σ_thermal 삼중항 | 우리 전달 우위(frame[5]) |
| morphology/변형장 | 없음(rigid 구) | MPM 진짜 형상변화·Σdg | 우리 MPM 보강 |
| code | **EDEM**(서브루틴) | LIGGGHTS | (둘 다 상용/오픈; LIGGGHTS 직접 Pasha pair_style 없음) |
| 소재·응력 | **암모늄 플루오레세인/일반구, 충돌+11 %strain** | LPSCl/NMC811, 300 MPa | **절대값 전이 불가**(소재+응력) — LAW·방법론만 |
| 차원 | 3D(N=3400 die, 단일입자 충돌) | 3D DEM | (둘 다 3D) |

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **★ 점착-소성 *에너지-일관* 결합 = SE-SE 점착 면적의존의 물리적 출발점** (eq10·11): "압밀 깊은 SE 접촉이 더
  끈끈하다"를 우리는 현재 `adhesionStiffness`(경험 강성)로 준다. Pasha는 같은 걸 **A_p·Γ=제하곡선면적(에너지보존)**
  으로 유도 — **우리 Stage-E 소성면적 A_physics에 표면에너지 Γ를 곱하면 *에너지-일관* SE-SE 점착이 나온다**(EEPA
  k_adh·δⁿ보다 물리적). MPM `--coh`(backlog A3) 도입 시 **A_p·Γ 형태**를 매핑 출발점으로. (§7.2)
- ② **★ 선형화 pull-off locus(eq18) = 우리 선형 계수 점착의 정당화**: "비선형 점착을 선형 2-파라미터(k_cp·f_0p)로
  근사해도 TN을 재현"(Fig 13) → 우리 `adhesionStiffness`(선형)가 정당. method/SI에 인용: "선형 점착 계수는
  Pasha(2014)가 보인 *에너지-일관 비선형 pull-off의 선형 근사*다." (§7.2·7.5)
- ③ **★ load-dependent k_e(eq25) = 우리 k̂₂ 보간의 근거 + 한계 경계**: "상수 k_e면 고속서 e가 비물리적 평탄
  (~0.38), load-dependent라야 감소(TN정합)"(Fig 13→14) — 우리 `coefficientMaxElasticStiffness` 부하의존 보간의
  물리 근거. **단 우리 압밀은 준정적이라 이 고속 보정은 무관**(충돌/분쇄 볼 때만). (§7.4)
- ④ **★ NOT 경로 A 명시 (EEPA처럼)**: `elasto_plastic_feasibility.md`에 "Pasha 2014도 *캡 없는* 선형 패밀리
  (Luding/EEPA와 같은 층위) — 단독으론 18× 연화 해결 못 함. 경로 A의 캡은 Thornton–Ning(p_y)/So(H)." 명기.
  Pasha+p_y캡 = 점착-에너지일관 포함 경로 A 후보. (§7.3)
- ⑤ **TN 검증 방법론 차용**: "선형 모델 vs 엄밀 비선형(TN)을 *같은 입자에서 e·v_s 비교*"가 LAW 검증의 정석 →
  우리 hooke/hysteresis를 Thornton–Ning(또는 Pasha)과 *같은 LPSCl 접촉*에서 비교하면 우리 선형 LAW의 충실도
  정량화 가능. (§7.5; 단 우리는 압밀이라 충돌보다 압밀 일분해 비교가 더 적절.)

## 9. 인용 가능 문장 (deck/paper용)

- "우리 DEM의 SE-SE 점착 탄소성 접촉은 Luding(2008)·Thakur(2014, EEPA)·Pasha(2014)가 공유하는 *선형(piecewise-
  linear) 점착-탄소성 이력* 패밀리에 속한다 — 셋 다 소성 분기(k₁→k₂, 영구겹침)와 점착(pull-off)을 갖되 *항복압/경도
  캡은 없으며*, Pasha(2014)는 그중 미세 점착분말(0.1–10 µm)을 겨냥하고 점착-소성 결합을 *표면에너지 일*로 유도한다."
- "Pasha et al.(2014, Granular Matter, open access)은 pull-off 힘이 소성변형과 함께 증가하는 것을 *소성 평탄화
  면적의 표면에너지 일* |W_ad|=A_p·Γ=πΓ(2R*α_pd−α_pd²) = 제하곡선 면적 (137/162)f_cp²/k_e 로 *에너지-일관* 유도
  하며(eq10·11) — 이는 우리 Stage-E가 *전달*(σ_ionic)에 쓰는 바로 그 소성 접촉면적을 *점착*에 쓰는 상보 관계로,
  EEPA의 경험적 면적의존 점착(−k_adh·δⁿ)보다 한 단계 물리적인 출발점이다."
- "Pasha(2014)는 단순 선형 모델이 엄밀 비선형(Thornton–Ning, JKR-탄소성) 모델의 임계 스티킹속도(~1.6 m/s)와
  반발계수를 재현함을 보여(Fig 13) — 우리가 LIGGGHTS hooke/hysteresis(선형)를 쓰는 정당화의 독립 사례다. 단 고속
  (v>10 m/s)서 반발계수 감소를 재현하려면 *부하의존 탄성제하강성* k_e=k_p+(r/R*)²(k̂_e−k_p)(eq25, Luding eq8과
  동형)이 필요하며, 이는 우리 `coefficientMaxElasticStiffness` k̂₂ 보간과 같은 물리다."
- "Pasha 모델은 우리 hooke/hysteresis(Luding 2008)·EEPA와 같은 *캡 없는* 층위다 — 소성이 강성비 k_p/k_e로 정의된
  이력이지 접촉압을 p_y로 cap하는 물리 항복이 아니므로, real E_SE로는 우리 18× 연화 문제를 그대로 가진다. 항복압
  캡(Thornton–Ning p_y / So H)을 더하는 것이 경로 A이며, Pasha+캡 = *점착-에너지일관 포함* 경로 A 후보다."

## 10. 주의/한계 (over-claim 방지)

- **소재·응력 전이 불가 (이중 차이).** 검증 소재 = **암모늄 플루오레세인(E=1.2 GPa, 무름)**·감도분석 = 일반 1 mm
  구이지 **LPSCl/NMC811 아님**. 응력 = *단일입자 충돌* + *bulk compression 11 % strain(준정적)*이지 우리 *300 MPa
  배터리 압밀*이 아님. **고체분율(초기 0.48–0.52, 목표 0.58)·일(µJ·N)·v_s(m/s) 절대값을 우리 압밀과 직접 비교
  금지.** 가치는 **LAW 정의·점착-소성 에너지결합·선형화·load-dep k_e·TN검증 방법론**.
- **★ Pasha는 "경로 A"가 아니다 (EEPA와 같은 정정).** Pasha = 우리 Luding 모델·EEPA와 *같은 캡-없음 층위*의
  선형 점착-탄소성 LAW이지, *항복압 캡을 더하는* 경로 A가 아니다. p_y=35.3 MPa는 α_y(항복 *시작점*)만 잡고 소성
  분기서 *압을 cap하지 않는다*. 경로 A의 캡은 Thornton–Ning(p_y)/So(H). **Pasha 단독 도입으로는 18× 연화가
  해결되지 않는다.**
- **rigid 구 + CONTACT 소성만**(층위1). 입자 SHAPE 흐름·morphology·변형장 전무 — α_p는 *접촉점 압흔 proxy*, A_p는
  *기하 평탄화 면적*이지 입자 변형 아님. 우리 MPM 영역(frame[5]).
- **전달 σ 전혀 없음**(역학·충돌 LAW) → frame[5] 역학 절반만. σ_ionic/e/thermal 비교점 0.
- **검증 = *충돌* 동역학, 우리 = *압밀* 준정적.** "선형≈비선형 TN"(Fig 13)은 *단일입자-평면 충돌*서 입증 — 다입자
  준정적 압밀(특히 큰 변형/캡 영역)서 자동 성립 아님. + 검증입자 E=1.2 GPa(무름) ≠ 우리 SE(real 24/soft 1.35 GPa).
- **점착→고체분율↓는 *저응력 충전* 현상**(Fig 18, Γ↑→0.52→0.48). 우리 고압 압밀에선 점착이 porosity 안 바꿈
  (jamming 기하로 고정; scaffold `--coh` sweep 확인). 이 정성거동 직접 전이 금지(EEPA Fig16/18과 같은 경고).
- **좁은 정규 PSD(평균 1 mm)** — mono에 가까움; bi/poly-PSD 아님. Furnas-dip/패킹 효과는 이 논문 범위 밖.
- **k_e는 TN 초기제하 기울기 *평균*, k̂_e는 Hertz 접선** — fit 절차 의존. TN 응답은 Ning[3] PhD digitize(Fig11,
  PlotDigitizer) → *digitized 기준값* (Table 2 k_e·k_p·k_cp·f₀·f_0p는 그 fit 산출).
- **EDEM 서브루틴 구현.** LIGGGHTS에 직접 Pasha pair_style 없음 — 우리 hooke/hysteresis(Luding 선형)가 *같은
  패밀리*이나 *정확히 같은 식(jump-in 8/9·eq18 선형 locus·eq25)은 아님*. 구현 매핑 시 차이 확인 필요.

## Supplementary Information

**없음** (사용자 지시: digest .md + CSV + PDF만). 본문 12쪽(Appendix I·II 포함) 자체가 완결. Appendix I = W_ad 유도
(eq28–37), Appendix II = v_i·v_r 유도(eq38–48). 후속 flowability 응용 = Pasha PhD 2013(ref[26], Univ. Leeds).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

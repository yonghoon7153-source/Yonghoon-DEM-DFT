<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.  깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md,
     τ 묶음 형식 기준 = landesfeind2016_tortuosity_eis_electrodes_separators.md · tjaden2018_… · taufactor_….
     이 논문은 시뮬레이션이 아니라 액체 전해질 LIB 의 *측정법 비교* 논문이다 → §4 를 두 측정 사슬 + 일반 전송선 모델 (TLM) 유도로 확장했다.
     값 표지: stated = 본문·캡션·표 원문 / 그림 인쇄값 = 그림 안에 숫자로 찍힌 값 / 판독 = 그림 막대·곡선에서 읽은 값 (TREND 전용, 정밀값으로 쓰지 않는다)
     / 파생 = 카드 작성자 계산 (식 명시) / 우리 유도 = 원문 식에서 카드 작성자가 끌어낸 극한·축약 (원문에 없음, 수치 검산 기록 §10-3). -->
# 두 τ 측정법의 실측 비교 — DC 편극-중단 (polarization-interrupt, 확산 · eRDM) vs 차단 전해질 EIS (blocking-electrolyte, 전도 · eSCM) + 접촉저항 · 전하이동 · 전자 레일을 넣은 일반 전송선 모델 — Pouraghajan (J. Electrochem. Soc. 2018)

> slug `pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte` · DOI `10.1149/2.0611811jes` · type `exp (liquid-LIB tortuosity 측정법 비교 — DC polarization-interrupt (eRDM) vs blocking-electrolyte EIS + generalized TLM (eSCM))` · PDF `10. Quantifying tortuosity of porous Li-ion battery electrodes Comparing polarization-interrupt and blocking-electrolyte methods.pdf` · digested `2026-10-03` · status ✅
>
> ★ **정의 판정 (이 카드의 목적)** — 이 논문의 **τ 는 제곱 없는 tortuosity factor** 다: `D_eff = (ε/τ)·D` (Eq 1) · `k_eff = (ε/τ)·k_int` (Eq 2) · `N_M = τ/ε` (A2644 · Eq 4) · Bruggeman `τ = ε^α`, α = −0.5 (Eq 3).
> 원문 낱말은 그냥 "tortuosity (τ)" 지만 양은 Tjaden κ = τ² · Landesfeind τ · COMSOL τ_F 와 같은 **tortuosity factor** → 우리 규약 **tau2** 척도다 (√ 아님).
> 단 **같은 기호 τ 가 두 방법에서 다른 양을 가리킨다**: 편극-중단 (PI) 의 τ 는 관통형 conventional τ (= 우리 **tau2** 의 정의), 차단 전해질 (BE) 의 τ 는 Nguyen 의 **electrode tortuosity factor τ_e** (우리 리포에 없음).
> 원문은 둘을 같은 τ 로 놓고 비교했고, 상용 전극 넷에서 (둘은 바로, 둘은 박리막 재시험 뒤) **측정 불확도 (BE 최대 5 % · PI 최대 12 %) 안에서 일치**를 보고했다 — 부호는 정해지지 않는다 (§8-0 결정 13).
>
> 출처 PDF = `litdb/inbox/10. ….pdf` (11 쪽, **SI 없음**).  **PDF 1 쪽 = IOP 표지 + "You may also like" 광고** (본문·인용 아님).
> 본문 = PDF 2–11 쪽 = 학술지 **A2644–A2653** (PDF 쪽 n ↔ 학술지 A(2642 + n)).  아래 쪽 표기는 전부 학술지 쪽 (A26xx) 이다.  식 · 표 · 그림 번호 = 원문 번호.

---

## 0. 결론 먼저 (정의 판정 + 핵심 수치)

| 질문 | 답 | 근거 (식·쪽) |
|---|---|---|
| 이 논문 τ 는 τ 인가 τ² (tortuosity factor) 인가? | **tortuosity factor (제곱 없음) — 우리 tau2 척도** | Eq 1–2 · N_M = τ/ε (A2644) · Eq 4 (A2646) · Bruggeman τ = ε^−0.5 (Eq 3) |
| 기하 τ (최단 경로/직선 거리) 인가? | **아니다** — 원문이 그 정의를 "가변 단면 효과를 무시한다" 며 **쓰지 않는다고** 적고, 그림 1 경로 c (단면이 변하는 통로) 도 τ > 1 로 둔다 | A2644 본문 · Fig 1 |
| 두 방법의 τ 는 같은 양인가? | 원문은 같은 τ 로 취급.  **우리 분류 (nguyen 카드 기준)**: PI = eRDM (관통 · conventional τ = tau2) · BE = eSCM (편측 접근 · τ_e) | A2645 · nguyen 카드 §4-A |
| 두 방법 차이의 크기 | 양극 1 · 2: **판독 분해능 (~1 %) 안에서 같음** · 양극 3 박리막: BE −3.6 % · 음극 박리막: BE −10 % (모두 판독·파생).  미박리 BE 는 양극 3 **+62 %** · 음극 **+14 %** | Fig 8 (A2649) |
| 차이의 원인 (원문) | 큰 차이 = **박리 (delamination) 팽창** (두께 +12 % 양극 3 · +5 % 음극) 인데 명목 건조 두께·다공도로 τ 를 계산했기 때문.  나노 기공 이중층 효과는 1–8 % 수준 추정 → 불확도 안이라 귀속 불가 | A2649 |
| 일반 TLM 의 핵심 | 고상 전자 레일 (β = k_eff/σ_eff) · 고상–집전체 접촉 (Z_cc) · 전해질–집전체 접촉 (Z₀) · 전하이동/이중층 (z_s = R ∥ CPE) 을 넣은 닫힌 해 **Eq 5** (차원형 Eq 12) | A2646–A2647 · 표 I · 그림 5 |
| 접촉저항은 어디에 들어가나 | β ≪ 1 · Z₀ ≫ 1 이면 **직렬 가산**: `Z_EL = R_ion·(Z_cc + 1/(λL·tanh λL))` (Eq 14) → R_ion·Z_cc = z_cc/A.  R ∥ CPE 로 두면 고주파 반원 (Al 집전체 양극에서만 관측) | Eq 14 (A2647) · Fig 6 · A2651 |
| 접촉 반원이 고주파를 가린 경우 | 같은 무캘린더 양극: Al 그대로 **τ = 3.13 ± 0.06** vs Cu 로 바꾼 박리막 **τ = 2.5 ± 0.1** (+25 %, 파생) — 원문은 이 차이를 논하지 않는다 | Fig 14 (A2652, 그림 인쇄값) |
| 빠른 추출법 편향 (한 스펙트럼) | 상세 모델 τ 2.53 대비 선형 외삽 2.27 (−10 %) · drop-down 2.64 (+4 %) · 원 맞춤 2.50 (−1 %) | Fig 4b (A2646, 그림 인쇄값) |
| Bruggeman 대비 | "Bruggeman 보다 크다" (원문).  파생 (τ/ε^−0.5): 양극 1 (ε 0.17) ≈ 1.05× (거의 Bruggeman) · 양극 2 ≈ 1.8× · 양극 3 ≈ 1.7× (박리막) / 2.8× (미박리 BE) · 음극 ≈ 3.8× (박리막) – 4.8× (미박리 BE) | A2649 · Table III · Fig 8 |

---

## 1. 한 줄 요약
같은 연구실 (BYU Wheeler) 이 만든 **DC 편극-중단법** (분리막 사이 free-standing 전극막의 염 농도 이완 → 유효 확산계수 → τ) 과 Gasteiger 군의 **차단 전해질 EIS 법** (비삽입 염 TBAPF₆ 대칭 파우치 → TLM 맞춤 → 유효 이온전도도 → τ) 을 **같은 상용 전극 넷 (양극 3 · 흑연 음극 1)** 에 적용해 비교한 논문.  BE 해석용으로 **고상 전자저항 · 고상–집전체 접촉저항 · 전해질–집전체 접촉 · 전하이동 (비이상 차단)** 을 넣은 **일반 TLM 닫힌 해 (Eq 5 / Eq 12)** 를 유도했다.  결과: 두 방법은 대체로 일치 (불확도 BE ≤ 5 % · PI ≤ 12 %) 하고, 어긋난 두 시료는 박리 팽창이 원인이었다 — 그 두 시료에서는 PI 의 필수 전처리인 박리가 τ 자체를 바꿨다 (BE 끼리 ≈ −40 % · −21 %, 판독).  우리에게는 **(i) "τ_e vs conventional τ" 의 유일한 실측 대조 (액체 LIB) 와 (ii) TLM 앵커를 읽을 때 걸리는 편향 목록 (접촉 반원 · 저주파 곡률 · 전자 레일)** 을 준다 — 수치는 액체 LIB 라 전이 불가.

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Fezzeh Pouraghajan**(1), Hannah Knight(1), Michael Wray(1), Brian Mazzeo(2), Ram Subbaraman(3), Jake Christensen(3), **Dean Wheeler**(1, 교신) — (1) BYU 화학공학과 · (2) BYU 전기·컴퓨터공학과 · (3) Robert Bosch LLC Research and Technology Center (Palo Alto) | **J. Electrochem. Soc. 165 (11) A2644–A2653 (2018)** | **10.1149/2.0611811jes** | 액체 전해질 LIB 상용 전극: 양극 1 = Hydro-Québec LCO (93 % AM · 4 % 탄소 · 3 % 바인더 wt) · 양극 2·3 = "TMO" (조성 n/a) · 흑연 음극 (조성 n/a) · 분리막 Celgard 3501 | **실험 (측정법 비교)** + 해석 모델 (일반 TLM 닫힌 해) — 수치 미세구조 시뮬레이션 없음 |

- 접수 2018-04-27 · 수정본 2018-08-02 · 게재 2018-08-22.  ECS 2017 New Orleans 학회 (5/28–6/1) Paper 135.  **Open access CC BY-NC-ND 4.0** (A2644).
- 연구비: 미국 DOE BMR 프로젝트 (DE-AC02-05CH11231).  전극 제공: Hydro-Québec (Chisu Kim) · Argonne CAMP (Bryant Polzin) — 시료별 출처는 양극 1 (Hydro-Québec LCO) 만 명시 (A2652).
- **SI 없음.**  PDF 1 쪽 광고 목록 (본문 아님) 에 같은 군의 후속 *"The Effects of Aging on the Tortuosity of Li-Ion Battery Electrodes"* (Knight, Pouraghajan, Wheeler et al.) 와 *"Reconstruction–Simulation Approach Verifies Impedance-Derived Ion Transport Tortuosity of a Graphite Battery Electrode"* (Kroll, Hlushkou, Schlabach et al.) 가 보인다 — **본문 인용 목록에는 없고 서지 [미확인]**.

---

## 3. 핵심 수치 ★

### 3-1. 시료 — Table III (A2648, stated)

| 전극 | 두께 [µm] | 다공도 [%] | 비고 |
|---|---|---|---|
| Cathode 1 (Hydro-Québec LCO) | 45 | 17 | 93/4/3 wt (AM/탄소/바인더) — A2648 |
| Cathode 2 (TMO) | 87 | 36 | 조성 n/a |
| Cathode 3 (TMO) | 60 | 36 | 조성 n/a · 박리 시 두께 +12 % (A2649) |
| Anode (Graphite) | 115 | 36 | 조성 n/a · 박리 시 두께 +5 % (A2649) |

- ⚠ 다공도는 *"either reported by the supplier or estimated using typical porosities for commercial electrodes (note that reported MacMullin numbers do not depend on these values)"* (A2648) — 어느 행이 공급사 값이고 어느 행이 "통상값" 추정인지 **원문이 밝히지 않는다**.  세 전극이 모두 36 % 다.
- 두께·다공도는 **명목 (건조) 값**을 썼다 — *"according to customary practice"* (A2649).

### 3-2. ★ 두 방법의 τ — Fig 8 (A2649)

원문은 τ 를 **표로 주지 않는다** — 막대그림뿐이다.  아래 τ 는 픽셀 스캔 **판독값** (막대 끝 분해능 ≈ ±0.02 · TREND 전용).  오차막대 = 95 % 신뢰구간 (BE 8 셀 · PI 5–7 셀, A2649); **BE 박리막 막대에는 신뢰구간이 없다** (캡션).

| 전극 | ε (stated) | PI τ (판독) | BE τ — 미박리 (판독) | BE τ — 박리막 (판독) | BE/PI − 1 (파생) | BE 박리막/PI − 1 (파생) |
|---|---|---|---|---|---|---|
| Cathode 1 | 0.17 | ≈ 2.56 (±≈0.20) | ≈ 2.54 (±≈0.04) | — | ≈ 0 (판독 분해능 안) | — |
| Cathode 2 | 0.36 | ≈ 3.02 (±≈0.39) | ≈ 3.03 (±≈0.06) | — | ≈ 0 (판독 분해능 안) | — |
| Cathode 3 | 0.36 | ≈ 2.88 (±≈0.35) | ≈ 4.66 (±≈0.24) | ≈ 2.78 (CI 없음) | **≈ +62 %** | ≈ −3.6 % |
| Anode | 0.36 | ≈ 6.96 (±≈0.41) | ≈ 7.93 (±≈0.18) | ≈ 6.26 (CI 없음) | **≈ +14 %** | ≈ −10 % |

- 오차막대의 상대 크기 (판독·파생): PI 6–13 % · BE 1.5–5 % — 원문 *"The maximum uncertainty in tortuosity values obtained for blocking-electrolyte and polarization-interrupt methods were 5% and 12%, respectively"* (A2649) 와 맞는다.
- ★ **박리 자체가 τ 를 바꿨다** (BE 끼리, 판독·파생): 양극 3 미박리 ≈ 4.66 → 박리막 ≈ 2.78 (**≈ −40 %**) · 음극 ≈ 7.93 → ≈ 6.26 (**≈ −21 %**).  양극 1 은 박리 영향이 CI 안 (Fig 15: −4.7 %).  원문 논리 (A2649): 박리 팽창 (두께 +12 % · +5 %) 으로 막이 바뀌었는데 명목 건조 두께·다공도로 계산했다 → PI (박리막 필수) 와 미박리 BE 는 **서로 다른 시료 상태**를 잰 셈이다.  어느 값이 "온전한 전극의 τ" 인지 원문은 판정하지 않는다 — 미박리 BE 가 집전체 위 원래 전극을 잰 값이다 (우리 판독).
- **두 방법의 비 (BE/PI) 는 ε 와 무관**하다 — 두 τ 모두 (측정 비) × ε 로 만들고 같은 ε 를 곱한다 (파생).  그래서 ε 가 "통상값" 이어도 **방법 비교 자체는 영향받지 않고**, τ 절대값만 ε 가정을 물려받는다.
- MacMullin 수 N_M = τ/ε (파생, 판독 τ 기준): 양극 1 ≈ 15 · 양극 2 ≈ 8.4 · 양극 3 ≈ 8.0 (PI) / 13 (BE 미박리) / 7.7 (BE 박리막) · 음극 ≈ 19 (PI) / 22 (BE 미박리) / 17 (BE 박리막).
- Bruggeman τ_B = ε^−0.5 (파생): ε 0.17 → 2.43 · ε 0.36 → 1.67.  τ/τ_B: 양극 1 ≈ 1.05 · 양극 2 ≈ 1.8 · 양극 3 ≈ 1.7 (PI) / 2.8 (BE 미박리) / 1.7 (BE 박리막) · 음극 ≈ 4.2 (PI) / 4.8 / 3.8.  원문 문장은 *"tortuosity values are larger than predicted by a conventional Bruggeman-type relationship"* (A2649) 뿐 — **양극 1 은 Bruggeman 에 거의 붙어 있다** (PI 의 신뢰구간은 2.43 을 포함).

### 3-3. 빠른 R_ion 추출법 vs 상세 모델 — Fig 4b (A2646, 그림 인쇄값)

| 방법 (원문 이름) | τ | 상세 모델 대비 (파생) | 원문 설명 (A2650) |
|---|---|---|---|
| Detailed model fit (Eq 5 · Eq 18 맞춤) | **2.53** | 기준 | — |
| Circular fit | **2.50** | −1.2 % | 저주파 가지를 직선 대신 **원**으로 맞춰 곡률 (비이상 차단) 을 반영한 실축 절편 |
| Drop-down | **2.64** | +4.3 % | Ogihara: "elbow" 의 실수부를 저주파 절편으로 — 어느 점을 내릴지 모호 |
| Linear fit | **2.27** | −10.3 % | Landesfeind: 저주파 가지 직선 외삽 — 곡률이 있으면 어긋남 |

- 공통 규칙 (그림 4a · A2650): **R_l − R_h ≈ R_ion/3** (R_h = 고주파 절편, R_l = 저주파 절편) → R_ion ≈ 3·(R_l − R_h).
- Fig 4b 의 **시료는 원문이 밝히지 않는다** (2.53 이 양극 1 BE ≈ 2.54 와 가깝지만 같은 시료라는 문장 없음).

### 3-4. 접촉저항 · 박리 대조 — Fig 14 · Fig 15 (A2652, 그림 인쇄값 · 각 3 회 시험, A2651)

| 그림 | 시료 · 조건 | τ (95 % CI) | 파생 |
|---|---|---|---|
| 14a | **무캘린더 양극**, Al 집전체 그대로 — 큰 고주파 반원 (접촉저항) | **3.13 ± 0.06** | — |
| 14b | 같은 양극을 박리해 **Cu 박 집전체**로 교체 — 작은 접촉저항 | **2.5 ± 0.1** | 14a/14b = **1.25** |
| 15a | Cathode 1 (Hydro-Québec LCO), Al 그대로 — 큰 반원 없음 | **2.54 ± 0.03** (= Fig 8 값) | — |
| 15b | Cathode 1 박리 → Cu 집전체 | **2.42 ± 0.3** (인쇄 그대로) | 15b/15a − 1 = −4.7 % (CI 안) |

- 원문 해석 (A2651): 큰 반원은 **Al 집전체 양극에서만** 보였고 Cu 집전체 음극에서는 없었다.  같은 슬러리를 Al 과 Cu 에 바르면 Al 쪽만 큰 접촉저항 → *"nonconductive oxidized aluminum at the interface"* 로 귀속 (Landesfeind [12] · Gaberscek [32] 와 같은 결론).
- 15 는 *"delamination does not have significant effect on the tortuosity"* 를 보이려는 대조 (양극 1 은 반원이 없어 박리 자체의 효과만 본다).
- ⚠ **14a vs 14b 의 25 % 차이를 원문은 설명하지 않는다** — 본문은 *"The resulting Nyquist plot can be used to reliably calculate tortuosity of the cathode"* (14b) 라고만 적는다.  두 신뢰구간이 겹치지 않으므로 표본 산포가 아니다.  "접촉 반원이 가린 스펙트럼에서 일반 TLM 맞춤이 τ 를 키웠다" 인지 "이 무캘린더 막은 박리로 바뀌었다" 인지 **가르지 못한다 (우리 판독)**.  원문 자신도 접촉저항을 모델로 처리하면 *"albeit with increased uncertainty"* (A2650) 라고 적었다.

### 3-5. 분리막 · 불확도 · 조건 (stated)

| 항목 | 값 | 쪽 |
|---|---|---|
| 분리막 τ (Celgard 3501) | **3.24** — 2 · 4 · 6 · 8 장 AC 임피던스 (Thorat 법 [24]) 의 선형 맞춤, 4 cm² 스테인리스 전극 · TBAPF₆ 전해질 | A2651 |
| 분리막 1 장 두께 · 다공도 | 25 µm · 55 % (보고값) | A2651 |
| ⇒ 분리막 N_M · ÷Bruggeman | N_M = 3.24/0.55 = 5.9 · τ/τ_B = 3.24/1.35 = 2.4 (파생) | — |
| 최대 불확도 (95 % CI) | BE 5 % · PI 12 % | A2649 |
| 반복 수 (Fig 8) | BE 8 셀 · PI 5–7 셀 (시험마다 새 파우치) | A2649 |
| 반복 수 (Fig 14a · 14b · 15b) | 각 3 | A2651 |
| 저전도 전해질 시험 (Fig 12) | 691 µS/cm vs 177 µS/cm (범례) — 낮추면 접촉 반원과 이온 TLM 이 고주파에서 덜 겹친다 | A2651 |
| 나노 기공 이중층 추정 | 최소 기공 ≈ 카본블랙 지름 ~50 nm · Debye 길이 0.3–2 nm → 그 기공 이온의 **1–8 %** 만 벽에서 Debye 길이 안 → 효과 작음 | A2649 |
| BE 전해질 k_int (표준 20 mM TBAPF₆) | **n/a** (본문에 값 없음 — Fig 12 의 두 값만) | — |

---

## 4. ★ 방법 — 두 측정 사슬 + 일반 TLM

### 4-1. 정의식 (원문 번호 · 쪽, 렌더 확인)

| 식 | 원문 형태 | 쪽 | 원문 단서 |
|---|---|---|---|
| (본문) | "ratio between the shortest pathway for mass transfer between two points and the straight distance" | A2644 | *"This definition disregards the effect of non-uniform cross-sectional area of the pathway (Figure 1, pathway c)"* — **이 논문은 쓰지 않는다** |
| **Eq 1** | `D_eff = (ε/τ)·D` | A2644 | ε = porosity, D_eff/D = 유효/고유 확산계수.  PI 가 이 식으로 τ (또는 N_M) 를 정한다 (A2645) |
| **Eq 2** | `k_eff = (ε/τ)·k_int` | A2644 | k_eff/k_int = 유효/고유 전도도.  *"'Intrinsic' means the property of the pure electrolyte (filling 100% of the volume) and 'effective' means the measured property of the electrolyte when it is filled within a porous structure"* |
| (본문) | `N_M = τ/ε` | A2644 | *"The ratio τ/ε is also known as the MacMullin number (N_M)"* |
| **Eq 3** | `τ = ε^α` | A2644 | α = Bruggeman 지수, *"commonly taken to be −0.5"* (refs 8, 9) → τ_B = ε^−0.5.  *"the Bruggeman relationship can significantly under predict tortuosity for porous battery electrodes"* (ref 10) |
| **Eq 4** | `N_M = τ/ε = R_ion·A·k_int / l` | A2646 | BE: A = 셀 단면적, l = 시료 두께, k_int = 전해질 고유 전도도.  R_ion 은 **전극 하나의** 이온 저항 (대칭셀은 Eq 18 에서 ×2) |

### 4-2. 편극-중단법 (PI — Nguyen 분류명 eRDM, 원조 = 이 군의 Thorat 2009 [24] · Zacharias 2013 [10])

| 단계 | 내용 | 쪽 |
|---|---|---|
| ① 셀 | 집전체에서 **박리한 free-standing 전극막**을 분리막 두 장 사이에, 다시 Cu 집전체에 눌러 붙인 **Li 박 두 장** 사이에 끼운 대칭셀 (Fig 2a).  저 τ 막은 **여러 장을 쌓아** 분리막 대비 확산저항을 키운다 (Fig 2b) | A2645 · A2651 |
| ② 형성 | Maccor 4300.  Li 위 SEI 형성 사이클 여러 번: 0.5 mA/cm² 10 분 + 3 분 이완, *"In every other cycle, the current direction is changed"* (한 사이클 걸러 방향 반전 — 대칭 유지) | A2649 |
| ③ 편극 | 고정 직류 0.75 · 1 · 1.25 mA/cm² 를 **2 분** → 한쪽 Li 전극에서 Li⁺ 생성 · 다른 쪽에서 소모 → 셀 관통 농도 구배 = 농도 과전압 | A2645 · A2649 |
| ④ 중단 · 이완 | 전류를 끊고 수 분 이완 → 셀 전위가 0 으로 접근.  반대 방향으로 반복, 이완 곡선 평균 | A2645 · A2649 |
| ⑤ 판독 | 전위의 **반로그 (log₁₀E vs t)** 에서 **선형 확산 구간**의 기울기 (Fig 10: 판독 ≈ 140–300 s).  너무 이르면 확산이 아직 완전히 시작 안 됨, 너무 늦으면 잡음·작은 DC 편향 | A2650 |
| ⑥ 모델 | COMSOL 1D **restricted-diffusion** 질량수송 모델 (Thorat [24]) 이 같은 기울기를 내는 τ = *"apparent tortuosity"*.  전해질 고유 수송 물성은 문헌값 [24] | A2645 · A2650 |
| 전해질 | 1 M LiPF₆ in EC:DEC 50/50 (v/v) | A2648 |
| 단점 (원문) | 얇은 막 박리 손상 (Fig 13) · 저 τ 막은 분리막 τ 와 구분 어려움 · 얇은 막은 확산 시간상수가 작아 선형 구간이 짧음 · 박리는 수용성 바인더 전극에 부적합 (PVDF 는 영향 없다고 봄) | A2648 · A2651 |

### 4-3. 차단 전해질법 (BE — Nguyen 분류명 eSCM, 원조 = Landesfeind 2016 [12])

| 단계 | 내용 | 쪽 |
|---|---|---|
| ① 셀 | 4 cm² 전극 + 더 큰 상대 전극 (정렬 편의) — 유효 면적 4 cm² 로 "사실상 대칭".  사이에 분리막 1 장, 파우치.  코팅 없는 집전체를 밖으로 빼 단자로 (Fig 3: 2 cm × 2 cm) | A2649 · A2645 |
| ② 차단 | **비삽입 염**: 20 mM **TBAPF₆** in EC:DMC 1:1 (w:w).  TBAPF₆ in PC/EC · TBAClO₄ in DMC/EC 도 시험 → τ 변화 "slight" 뿐.  이상분극 계면 = 고/액 계면에 패러데이 전하이동 없음 | A2649 · A2646 |
| ③ EIS | Bio-Logic SP-200, OCV 근처, **10 mV** 섭동, 보통 **0.5 Hz–500 kHz** (가장 넓게 0.1 Hz–3 MHz) | A2649 |
| ④ 맞춤 | 대칭 파우치 모델 **Z = 2·Z_EL + R_sep** (Eq 18) 를 목적함수 **F = Σ (\|Z_t − Z\|)² / \|Z_t\|^p** (Eq 17) 로 최소제곱.  p 를 바꿔 본 결과 **p = 0.01** 이 "elbow" (중주파) 를 잘 맞춰 R_ion 결정에 강건 | A2649–A2650 |
| ⑤ 환산 | R_ion → **Eq 4** → N_M → τ = ε·N_M (명목 ε) | A2646 |
| 비이상 차단 | 차단 전해질에서도 *"a slight faradaic reaction can often be observed"* — 저주파 가지가 약간 휜다.  원인 후보: 활물질에서 나온 Li · 비신품 전극의 잔류 Li 염 · 전해질 성분의 의도치 않은 삽입·반응.  일반 TLM 이 이것을 받는다 | A2648 |
| 내부 기준 | 증발로 인한 변동은 **고주파 절편 + 분리막 N_M** 으로 전해질 고유 전도도를 현장에서 정하면 정규화 **가능** (실제로 적용했는지는 명시 없음) | A2651 |
| 단점 (원문) | 사이클한 음극은 비정상 모양 (Fig 11) 이라 분석 불가 (DMC 세척 뒤에도) · 큰 접촉저항이 고주파를 가림 (Fig 6) → 대책: 모델의 Z_cc · 전해질 전도도 낮추기 (Fig 12) · 박리 후 집전체 교체 (Fig 14) | A2650–A2651 |

공통: 두 시험 모두 **≈24 h 방치** (완전 젖음) 후, 고무층 + 금속 추를 올려 **≈45 kPa** 외압 (A2649).  습윤량 · 전해질 누설 · 조립 중 증발에 두 방법 모두 민감 (A2651).

### 4-4. ★ 일반 TLM — 지배식 · 경계조건 · 해 (A2646–A2647, 렌더로 원문 대조)

**회로 (그림 5)**: 집전체 쪽 끝 Z_CC → 고상 레일 Z_El 직렬 → 가로대 Z_ct (전하이동) → 전해질 레일 Z_Ion 직렬 → 분리막 쪽 Z_sep.  *"While the diagram indicates discrete resistances, the model is solved as a differential system"* (A2646).  ⚠ 그림의 **Z_El (전자 레일 요소)** 은 표 I 의 **Z_EL (전극 임피던스)** 과 다른 양이다.

| 식 | 원문 형태 | 뜻 |
|---|---|---|
| **Eq 6** | `0 = σ_eff·d²φ₁/dx² + (φ₂ − φ₁)/z_s` (인쇄 표기 dφ₁²/dx²) | 고상 전하 보존.  φ₁ 고상 · φ₂ 전해질 전위, z_s = 두 상 사이 **선형화 전하이동 임피던스** |
| **Eq 7** | `0 = k_eff·d²φ₂/dx² + (φ₁ − φ₂)/z_s` | 전해질 (이온) 전하 보존 |
| **Eq 8 · 9** | `i₁ = −σ_eff·dφ₁/dx` · `i₂ = −k_eff·dφ₂/dx` | 전자 · 이온 표면 (superficial) 전류밀도 |
| **Eq 10** | `i₁ = −σ_eff·dφ₁/dx = (0 − φ₁)/z_c` | 집전체 (x = 0) 경계 — 기준 전위 0 |
| **Eq 11** | `i₂ = −k_eff·dφ₂/dx = (0 − φ₂ − U)/z_cc` | 같은 경계의 이온 전류.  U = 전해질–집전체 반응의 개방회로 전위 (활물질 반응 기준) — *"U is assumed to be zero hereafter"* (i₂ 가 집전체 면적이 작아 ≈ 0) |
| (본문 A2647) | x = L: `i₁ = 0` · 전해질 전위 고정 (인쇄 표기 "φ₁ = φ₂") | 분리막 쪽 경계 — 고상 전자 절연 |
| (본문 A2647) | 소섭동 · 큰 패러데이 반응 없음 | 임피던스 선형 · 농도 균일 가정 |
| (본문 A2647) | z_s · z_c · z_cc = 각각 **저항 ∥ CPE** · σ_eff · k_eff = 실수 | 계면 셋의 등가회로 형 |
| **Eq 12** | `Z_EL = (R_ion/L) · { c·k_eff·λ·[L(k_eff − σ_eff) − (k_eff² + σ_eff²)·z_c] − s·σ_eff·[ [L(z_c − z_cc) + (σ_eff + k_eff)·z_c·z_cc]·k_eff²·λ² + (σ_eff − k_eff) ] − 2·k_eff²·σ_eff·λ·z_c } / { λ·(σ_eff + k_eff)·[ s·λ·σ_eff·k_eff·(z_cc − z_c) + c·(k_eff − σ_eff) ] }` (c = cosh λL · s = sinh λL) | 차원형 전극 임피던스 |
| **Eq 5** | `Z_EL = R_ion · { [β(Z₀ − Z_cc) + (1+β)·Z₀·Z_cc + (1−β)·(λL)^−2]·λL·tanh(λL) + (1 + 2β·sech(λL) + β²)·Z₀ + β(1−β) } / { (1+β)(Z₀ − Z_cc)·λL·tanh(λL) + 1 − β² }` | 무차원 닫힌 해 — *"which reduces to Equation 5 by substituting the dimensionless ratios shown in Table I"* |
| **Eq 13** | `λ = √(1/(k_eff·z_s))` | β ≪ 1 (전자 ≫ 이온) |
| **Eq 14** | `Z_EL = R_ion·(Z_cc + 1/(λL·tanh(λL)))` | β ≪ 1 **그리고** Z₀ ≫ 1 (전해질–집전체 사이 유효 패러데이 반응·이중층 없음 — 평면 집전체–전해질 접촉 면적이 다공 전극 내부 면적보다 작다) |
| **Eq 15** | `Z_EL = R_ion / (λL·tanh(λL))` | 위 + 전자 접촉저항 무시 → **Landesfeind [12] · Ogihara [13, 14] 와 같은 꼴** |

**표 I** (A2646 — Eq 5 · Eq 12 의 기호):

| 기호 | 원문 정의 |
|---|---|
| Z_EL | Electrode Impedance |
| R_ion | Ionic Resistance |
| k_eff | Effective Ionic Conductivity |
| σ_eff | Effective Electronic Conductivity |
| z_cc | Contact Impedance of the **Solid** with the Current Collector |
| z_c | Contact Impedance of the **Electrolyte** with the Current Collector |
| z_s | Charge Transfer Impedance |
| L | Electrode Thickness |
| β | k_eff / σ_eff |
| Z₀ | z_c·k_eff / L |
| Z_cc | z_cc·k_eff / L |
| λL | L·√((σ_eff + k_eff)/(σ·k_eff·z_s)) = √((1+β)·R_ion/Z_s)  (인쇄 표기 그대로 — 분모의 σ 에 "eff" 첨자 누락) |
| Z_s | z_s / (L·area) |
| c · s | cosh(λL) · sinh(λL) |

- 차원: z_c · z_cc = 면적 비저항 [Ω·cm²], z_s = 부피 임피던스 [Ω·cm³] (Eq 6 차원), R_ion·A = L/k_eff ⇒ **Z₀ · Z_cc = 접촉 임피던스 ÷ 면적 이온저항 (무차원)** · R_ion·Z_cc = z_cc/A (파생).
- ⚠ **첨자 불일치 (원문 안)**: 표 I · 그림 5 · Eq 14 앞뒤 문장 (*"no … double-layer effect directly between electrolyte and the current collector (Z₀ ≫ 1)"* · *"significant electronic contact resistance between the electrode film and current collector it is useful to include Z_cc"*) 은 **z_cc = 고상–집전체, z_c = 전해질–집전체**.  그런데 Eq 10–11 과 A2647 첫 문장 (*"z_c is the contact impedance of the current collector in the solid phase, z_cc … in the electrolyte phase"*) 은 **반대**다.  **우리 검산 (§10-3)**: 닫힌 해 Eq 5 · Eq 12 는 표 I 의 뜻대로 움직인다 (Z₀ → ∞ 에서 de Levie 극한, Z_cc 는 직렬 가산).  ⇒ **표 I 의 뜻으로 읽는다.**
- 원문 대비: 집전체에 패러데이 반응이 없다고 두면 경계조건이 Tröltzsch–Kanoun [25] 과 가까워 결과가 비슷하다 · Warburg 확산 임피던스 모델 [29, 30] 도 물리는 다르지만 지배 미분방정식이 비슷해 스펙트럼이 비슷하다 (A2647).

### 4-5. 차단 조건 — Eq 16 · 표 II (A2647)
- **Eq 16** (일반 Li 표면 반응 Li⁺ + e⁻ + Γ ↔ LiΓ 의 Butler–Volmer 형): `i = i₀^ref·(C/C_ref)^α·(C_s/C_ref,s)^α·((C_max − C_s)/C_ref,s)^α × [exp(α_a·F·η_s/RT) − exp(−α_c·F·η_s/RT)]`.
- 차단 = 교환전류의 농도 인자가 0: Ogihara 는 **SOC 0 % (C_s/C_ref,s = 0) 또는 100 % ((C_max − C_s)/C_ref,s = 0)** 에서 시험; Landesfeind 는 **전해질 Li 농도 ≈ 0 (C/C_ref = 0)** → SOC 무관한 더 강건한 차단 (A2647–A2648).
- 표 II 는 i · i₀^ref · C · C_ref · C_s · C_ref,s · C_max · α_a · α_c · F · η_s · R · T 를 정의 (η_s 를 "Anodic overpotential" 로 표기).  ⚠ 농도 인자의 지수 α 는 표 II 에 없다.

### 4-6. 측정 조건 일람

| 항목 | 값 | 쪽 |
|---|---|---|
| 박리 | 양극: 45 wt % KOH 수용액 (Al 완전 용해 대기 · 1 차 세척 뒤 재도포로 Al 잔류 방지) · 음극: 1 M 질산 또는 1 M 염산.  2.5 × 2.5 cm 시료에 0.5 mL, 유리판으로 눌러 주름·균열 방지, 수 분 침지 → 증류수 세척 → 건조 | A2648 · Fig 7 |
| PI 셀 조립 | Ar 글러브박스 (수분 0.9 ppm · O₂ < 0.025 ppm, VAC) · Celgard 3501 두 장 · Li 박 ≈4 cm² (Alfa Aesar) 를 Cu 집전체에 압착, 작은 쪽 Li 가 면적 결정 · 금속 고분자 파우치 · 1 M LiPF₆ EC:DEC · 임펄스 실러 | A2648–A2649 |
| BE 셀 | 위 §4-3 | A2649 |
| 외압 · 방치 | ≈45 kPa · ≈24 h | A2649 |
| 분리막 τ 측정 | 4 cm² 스테인리스 전극 · TBAPF₆ · 2/4/6/8 장 | A2651 |

### 4-7. 시뮬레이션 · 입자 처리 ★
- **미세구조 시뮬레이션 없음** — DEM / MPM / FEM 미세구조 / RNM 없음.  모델은 둘뿐: PI 의 **1D restricted-diffusion 연속체** (COMSOL, Thorat) · BE 의 **1D 균질 2-레일 TLM** (닫힌 해).
- **입자 처리 ★** = 해당 없음 (실제 상용 전극, 3D 재구성도 없음).  TLM 은 전극을 **깊이 방향으로 균질한 두 연속 레일**로 본다 — 입자·접촉 단위가 없다.  ⇒ 원문 "contact resistance" 는 **전극막–집전체 거시 계면** (Al 산화막) 의 저항이지 **입자–입자 접촉 협착이 아니다** (§ τ 정의 대조 · §7).

### 4-8. 기법 미니 용어집

| 용어 | 뜻 (이 논문에서) |
|---|---|
| **polarization-interrupt (PI)** | 직류로 농도 구배를 만든 뒤 끊고 이완 기울기에서 D_eff → τ (Eq 1).  Nguyen 분류명 eRDM (restricted-diffusion method, 관통형) |
| **blocking-electrolyte (BE)** | 비삽입 염으로 계면 전하이동을 막은 대칭셀 EIS → TLM → R_ion → τ (Eq 4).  Nguyen 분류명 eSCM (symmetric cell method, 편측 접근형) |
| **apparent tortuosity** | PI 모델이 측정 기울기를 재현하는 τ (A2645) |
| **MacMullin 수 N_M** | τ/ε = k_int/k_eff.  ε 없이 정해진다 (BE: R_ion·A·k_int/l) |
| **일반 TLM (generalized transmission-line model)** | 전자 레일 (σ_eff) · 이온 레일 (k_eff) · 가로대 z_s · 집전체 쪽 접촉 둘 (z_cc 고상, z_c 전해질) 을 넣은 1D 미분계 (Eq 6–11) 의 닫힌 해 (Eq 5 / 12) |
| **β** | k_eff/σ_eff — 0 이면 전자 레일이 등전위 (Landesfeind 간이화) |
| **Z₀ · Z_cc** | 접촉 임피던스 ÷ 면적 이온저항 (L/k_eff) — 무차원 |
| **λL** | √((1+β)·R_ion/Z_s) — 전극 두께 대 침투 깊이 비 |
| **R_h · R_l** | Nyquist 고주파 · 저주파 실축 절편.  R_l − R_h ≈ R_ion/3 (Fig 4a, β ≪ 1) |
| **drop-down · linear · circular** | R_l 을 정하는 세 빠른 법 (§3-3) |
| **γ_s** | 원문 A2650 이 고주파·저주파 가지 각도가 기대는 매개변수로 언급 — 표 I 에 정의 없음 (z_s CPE 지수로 읽힘, 우리 판독) |
| **이중 각 관계** | 그림 4a: 저주파 가지 각 θ₂ = 2θ₁ (고주파 가지 각).  ⚠ 본문 문장은 반대로 적었다 (§10-2) |
| **delamination** | 집전체에서 전극막을 산/염기로 떼어 free-standing 막을 만드는 처리 — PI 필수, BE 접촉저항 대책 |

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 (A2644) | 굴곡 경로 모식: 곧은 통로 τ = 1 · 굽은 통로 τ > 1 · **단면이 변하는 통로 τ > 1** | 이 논문 τ 는 협착 (가변 단면) 을 포함하는 tortuosity factor — 기하 τ 가 아니다 |
| 2 (A2645) | (a) PI 셀: Li 박 \| 분리막 \| 전극막 \| 분리막 \| Li 박 (b) 저 τ 막용: 전극막 여러 장 적층 | ★ eRDM = **관통형** 배치 — 우리 두 띠 Dirichlet T 의 실험 대응 (액체) |
| 3 (A2645) | BE 파우치 도면 (정면·측면: 2 cm × 2 cm 전극 · 집전체 탭 · 접착 · 분리막) | eSCM = 집전체 위 전극, 이온은 분리막 쪽에서만 |
| 4 (A2646) | (a) Nyquist 모식: R_h · R_l · θ₂ = 2θ₁ (b) 한 실측 스펙트럼에서 원 맞춤 τ 2.50 · drop-down 2.64 · 선형 2.27 · 상세 모델 2.53 | ★ 빠른 추출법만으로 τ 가 −10 … +4 % 흔들린다 — 문헌 τ 앵커를 쓸 때 추출법 확인 |
| 5 (A2646) | 일반 TLM 회로도 (Z_CC · Z_El · Z_ct · Z_Ion · Z_sep) | ★ 접촉저항이 **집전체 쪽 고상 레일 끝**에 붙는 자리 — 우리 내부 Holm 협착과 다른 자리 |
| 6 (A2647) | 무캘린더 신품 양극 (비상용): 큰 접촉 반원이 고주파를 가림 (판독: 반원 끝 Re ≈ 235 Ω · 정점 ≈ 90 Ω) + 모델 맞춤 (캡션 "Equation 15") | 접촉 반원이 TLM 45° 영역을 덮는 전형 — 이런 앵커는 τ 불확도가 크다 |
| 7 (A2648) | 2.5 × 2.5 cm 음극 박리 과정 사진 (a–f) | — |
| 8 (A2649) | ★★ τ 비교 막대: (a) 양극 1–3 PI · BE · BE (박리막) (b) 흑연 음극.  95 % CI (BE 박리막 제외) | ★★ **eRDM vs eSCM 실측 대조** — 일치 (양극 1 · 2) · 박리 팽창으로 어긋남 (양극 3 · 음극) → 박리막끼리 다시 일치 |
| 9 (A2650) | 양극 BE 스펙트럼 + 권장 목적함수 (p = 0.01) 맞춤 | 중주파 elbow 가 R_ion 을 정한다 |
| 10 (A2650) | PI 이완 곡선 log₁₀E vs t (판독: 중단 ≈ 120 s · 선형 확산 구간 ≈ 140–300 s) | 맞춤 구간 선택 = 잡음·DC 편향 vs 확산 미개시 |
| 11 (A2651) | 사이클한 음극의 BE 스펙트럼 — 비정상 (판독: Re ≈ 700 Ω 까지 휘는 호) | 열화 전극에서는 BE 가 실패할 수 있다 → PI 가 보완 |
| 12 (A2651) | 같은 양극, 전해질 691 vs 177 µS/cm — 저전도가 접촉 반원과 이온 TLM 을 떼어 놓음.  ⚠ 축 라벨이 Re/−Im 서로 바뀌어 인쇄 | 접촉저항 (전도도 무관) vs 이온저항 (∝ 1/k) 을 전도도 스윕으로 가른다 |
| 13 (A2651) | 박리된 막: (a) 온전 (b) 박리로 손상 (1 cm 눈금) | PI 의 약점 |
| 14 (A2652) | ★ (a) Al 그대로 τ 3.13 ± 0.06 (반원 끝 판독 Re ≈ 170 Ω) (b) 박리 → Cu: τ 2.5 ± 0.1 | ★ 접촉 반원이 있는 스펙트럼과 없는 스펙트럼의 τ 차 **25 %** (원문 미논의) |
| 15 (A2652) | 양극 1: (a) Al 그대로 2.54 ± 0.03 (b) 박리 → Cu 2.42 ± 0.3 | 박리 자체의 영향이 작은 대조 사례 |

## 6. Post-processing ★
- **무엇**: PI = 반로그 이완 곡선의 선형 구간 기울기 → 1D restricted-diffusion 모델 역산 (apparent τ) · 양방향 · 여러 전류 평균.  BE = Eq 18 (Eq 5 를 넣은 대칭셀) 을 Eq 17 (p = 0.01) 로 최소제곱 → R_ion → Eq 4 → τ.  보조로 빠른 추출 셋 (선형 · drop-down · 원 맞춤) 을 상세 모델과 비교 (Fig 4b).  분리막 τ = 층수 2/4/6/8 선형 맞춤 (Thorat).  불확도 = 새 파우치 반복 → 95 % CI.
- **도구**: COMSOL (PI 모델) · Maccor 4300 · Bio-Logic SP-200.  맞춤 소프트웨어 이름 n/a.  *"the model was not considered as a significant source of uncertainty; … more uncertainty from one sample to the next rather than any particular model fit"* (A2649).
- **수치화 방식**: τ 는 막대그림 (Fig 8) 과 그림 안 인쇄값 (Fig 4b · 14 · 15) 으로만 보고 — **τ 표가 없다**.  N_M 은 보고하지 않는다 (τ 만).

### 6-bis. 논증 흐름 (절 순서)
1. τ 정의 둘 (기하 vs Eq 1–2) 중 Eq 1–2 채택, Bruggeman 은 과소 예측 (A2644).
2. PI (확산) 와 BE (전도) 를 *"direct measurement"* 둘로 놓고, BE 해석을 위해 일반 TLM 을 유도 (A2645–A2647).
3. 상용 전극 넷에서 두 방법 비교 → 일치, Bruggeman 보다 큼 (A2649).
4. 어긋남 = 박리 팽창 → 박리막 BE 로 재확인 → 다시 일치 (A2649).
5. 남는 차이의 물리 후보 (이중층) 는 크기상 불확도 안 (A2649).
6. 실무: 목적함수 가중 · 빠른 추출법 비교 · 이중 각 관계 · 접촉저항 대책 셋 (모델 · 저전도 · 집전체 교체) (A2650–A2652).
7. 결론: *"Both methods are helpful since neither method is useful for every type of electrode film"* (A2652).

---

## § τ 정의 대조 — 우리 규약 매핑

> 우리 규약 (CLAUDE.md τ 명명 규약, 1저자 비준 10-03): f = σ_eff/σ₀ · **tau2** = φ·σ₀/σ_eff = φ/f (= tortuosity factor) · tau = √tau2 · τ_geo = 최단 경로/두께 · τ_e = electrode tortuosity factor (우리에 없음).
> 우리 접촉망 tau2 = 간선 재료 σ₀ 3.0 mS/cm (펠릿값, `CL-91`) 위에 SE–SE Holm 협착 (hertz 면적 = LIGGGHTS c_cpl[22] 교차 원판 · 반공간 Maxwell R_c = 1/(2σa)) 을 직렬로 더한 **모델 tau2**.  CF 가지 = 모델 내부 기준선 · FULL/CF = 모델 내부 협착비.

| 이 논문 기호 | 원문 정의 (식 · 쪽) | 원문 이름 | 정규화 — 어느 부피 · 어느 단면 · 어느 σ₀ | 우리 다섯 양 중 | 비고 |
|---|---|---|---|---|---|
| **τ (PI)** | `D_eff = (ε/τ)·D` (Eq 1, A2644) → τ = ε·D/D_eff | tortuosity / apparent tortuosity | ε = 전극 다공도 (총, 명목 건조값, 공급사 또는 통상값) · 단면 = 작은 Li 박 면적 (≈4 cm²) · 두께 = 명목 건조 두께 · **D₀ = 순수 액체 전해질 고유 확산계수 (문헌 [24])** | **tau2** (관통형 conventional tortuosity factor) | 확산 (과도) 측정 · 액체 연속체 — 전도상 내부 접촉저항 없음 |
| **τ (BE)** | `k_eff = (ε/τ)·k_int` (Eq 2) · `N_M = τ/ε = R_ion·A·k_int/l` (Eq 4, A2646) | tortuosity | ε 같음 · A = 셀 단면 (4 cm²) · l = 명목 두께 · **σ₀ = k_int = 순수 차단 전해질 (20 mM TBAPF₆ EC:DMC) 고유 전도도** — 값 n/a | **τ_e** (eSCM, Nguyen τ_e/ε = R_ion·A·κ₀/L) — **우리에 없음** | R_ion 은 TLM 이온 레일 저항 (편측 접근 · 이중층 sink) |
| **N_M** | τ/ε (A2644 · Eq 4) | MacMullin number | ε 불필요 | 1/f (PI 쪽) · N_M,e (BE 쪽) | 원문은 N_M 값을 따로 보고하지 않는다 |
| **α (Bruggeman)** | `τ = ε^α`, α = −0.5 (Eq 3) | Bruggeman exponent | — | tau2_B = φ^−½ (우리 `sigma_bruggeman` = φ^1.5, `network_conductivity.py:1125`) | 같은 관계.  ⚠ 부호 관례: 이 논문 α = −0.5 · Landesfeind α = +0.5 (τ = ε^−α) · Tjaden α = 1.5 (f 지수) |
| (본문, 식 없음) | 최단 경로 / 직선 거리 | (이 논문이 쓰지 않는 정의) | — | τ_geo | 원문이 명시적으로 배제 (가변 단면 무시) |
| **k_int · D** | "pure electrolyte (filling 100% of the volume)" (A2644) | intrinsic | 미세구조 없는 벌크 액체 | **σ₀** — ⚠ 우리 σ₀ = SE 펠릿값 3.0 (펠릿 미세구조 포함) | 기준 상태가 다르다 (결정 4) |
| **k_eff** | 표 I "Effective Ionic Conductivity" — R_ion = L/(k_eff·A) | effective | 전체 단면 · 전체 두께 | σ_full (FULL) 의 자리 — 단 BE 의 k_eff 는 편측 접근 TLM 에서 뽑은 값 | — |
| **σ_eff** | 표 I "Effective Electronic Conductivity" | effective electronic | 같음 | 우리 AM 전자망 σ_e (tau2 와 별개 채널, `_el_`) | β = k_eff/σ_eff 가 우리 σ_ion,eff/σ_e,eff 에 대응 |
| **ε** | Table III | porosity | 액체가 채운 기공 부피분율 (총) | **φ_SE** (구-합/상자, 전 SE) | 전도상이 기공 ↔ 고체 SE 로 뒤집힌다 |
| **z_cc (Z_cc)** | 표 I: 고상–집전체 접촉 임피던스 (R ∥ CPE) | contact impedance | 면적 비저항 Ω·cm² | **대응 없음** (DEM 에 집전체 계면 없음) | ⚠ **우리 SE–SE Holm 협착 (망 내부, FULL 안) 과 다른 자리** — FULL/CF 비와 섞지 않는다 |
| **z_c (Z₀)** | 표 I: 전해질–집전체 접촉 | contact impedance | 같음 | 대응 없음 | Z₀ ≫ 1 로 소거 (Eq 14) |
| **z_s** | 표 I "Charge Transfer Impedance" (그림 5 의 Z_ct, R ∥ CPE) | charge transfer impedance | 부피 임피던스 Ω·cm³ | 대응 없음 — 메모 v2 §7 최소안의 AM–SE 축전 sink 가 이 자리 | 차단이면 R → ∞ (CPE 만) · 비이상 차단 = 유한 R_ct |

**판정**
1. 이 논문의 τ 는 **제곱 없는 tortuosity factor** 다 (N_M = τ/ε · Bruggeman τ = ε^−0.5).  원문 낱말이 "tortuosity" 여도 우리 규칙상 **'tortuosity factor' (tau2)** 로 부른다.  √ 값 (우리 tau, 웹앱 τ_Lap,eff) 과 맞대지 않는다 — 예: 음극 τ ≈ 7 은 tau2 척도의 7 (√ 로는 ≈ 2.6, 파생).
2. **PI 의 τ = 우리 tau2 의 정의** (관통 · 전체 단면 · 총 부피분율) 이고 **BE 의 τ = τ_e** 다.  원문은 두 τ 를 같은 양으로 두고 비교했고 결과가 일치했다 → *이 전극들에서는* τ ≈ τ_e (§8-0).
3. **σ₀ 기준**: 이 논문 = **순수 액체 전해질 벌크 (100 % 부피)** · 우리 = **SE 펠릿 3.0 mS/cm** (펠릿 자신의 입계·잔류기공 포함, `CL-91`).  액체는 전도상 내부 접촉저항이 0 이라 τ 가 순수 기하 효과 (가변 단면 포함) 인 반면, 우리 FULL tau2 는 **펠릿 대비 기하 + SE–SE 접촉 협착 묶음**이다.  값 대조는 결정 4 (순수 SE 기준 상태) 뒤에만.
4. 키 (새 규약): 이 논문 PI 형 양 ↔ `tau2_ion_<mode>` 의 정의 · BE 형 양 ↔ (없음 — 만들면 `tau2e_…` 처럼 따로, tjaden 카드 권고).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ⚠ `our_dem_baseline.md` 는 **자리표시 (값 0)** 다 — 비교는 코드 정의 (`claude/stoic-knuth-NObVQ` 작업 트리 HEAD `93587254f`, 읽기만) 와 판단 메모 v2 (`docs/reviews/tau_conventions_judgment_v2_20261003.md`) 로 한다.
> **frame [5]**: 이 논문은 **수송 반쪽의 측정법**만 가진다 (액체 기공상 τ).  역학·형상·압밀은 없다.  우리 쪽 대응은 DEM 접촉망 tau2 (Kirchhoff) 와 STEP3 복셀 tau2 (CONTACT_FREE 가지) — 둘 다 **관통형**이라 PI (eRDM) 쪽 정의다.
> **frame [4]**: 이 논문 수치로 우리 모델을 맞추지 않는다 (액체 LIB).  쓰는 것은 ① 정의 · ② 두 방법 차이의 실측 크기 · ③ TLM 앵커 판독 편향 목록뿐.

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 전도상 | 액체 전해질 (기공 연속체) | SE 고체 입자 (DEM 구 접촉망) / STEP3 복셀 | **다름** — 우리만 SE–SE 접촉 협착이 있다 |
| τ 정의 | τ = ε·(벌크/유효), 제곱 없음 | tau2 = φ·σ₀/σ_eff | **같은 꼴** (PI 쪽) |
| 경계조건 | PI: 관통 (분리막 양쪽 Li) · BE: 편측 (집전체 차단 + 이중층 sink) | 접촉망: 바닥·위 띠 관통 Dirichlet (`network_conductivity.py:225–249` 띠 정의 · `:588–593` 가상 source/sink) · STEP3 도 관통 | 우리 = **PI 형 (eRDM)** 만.  BE 형 (τ_e) 경로 없음 (메모 v2 §7) |
| σ₀ | 순수 액체 벌크 | SE 펠릿 3.0 (`CL-91`) | **성격 다름** (기준 상태, 결정 4) |
| "접촉저항" | **집전체–전극막 계면** (Al 산화, 직렬 경계 항) | **SE–SE 입자 접촉 Holm 협착** (망 내부, FULL 가지) | **다른 물리 · 다른 자리** — 이름 충돌 주의 |
| 전자 레일 | β 로 TLM 에 포함 (일반 TLM) · Landesfeind 는 무시 | 이온 망과 전자 망을 **따로** 푼다 (이온 tau2 에 전자 레일 없음 — 관통형이라 필요 없음) | τ_e 를 만들 때만 문제 (§8-0 ②) |
| ε 회계 | 명목 건조 다공도 (공급사 / 통상값) | 구-합 φ_SE (질량 보존) | 같은 "총 부피분율" 계열 — 단 이 논문 ε 는 측정이 아닐 수 있다 |
| 크기 감각 (tau2 척도) | 2.5–7.9 (판독, 액체 · 다공도 17–36 %) | (메모 v2 §1 유도: T_H 코퍼스 중앙 6.21) | **값 대조 금지** — 상 · σ₀ · 전도 기구가 다르다.  같은 **척도 (√ 아님)** 라는 것만 |
| 입자 처리 | 실제 전극 · TLM 균질 연속체 | 강체 구 + 연화 E (형상 소성 없음) | 이 논문은 미세구조를 풀지 않는다 |

---

## 8. 적용 인사이트 (내 연구에 어떻게)

### 8-0. 닫는 것 — 두 τ 측정법의 실측 비교 (polarization-interrupt = eRDM vs blocking-electrolyte EIS = eSCM) + 접촉저항 · R_ct 를 넣은 일반 TLM

**① 두 방법의 τ 정의 · 기호 · 정규화** — 같은 기호 τ, 같은 정규화 (τ = ε × 벌크/유효, N_M = τ/ε, 명목 ε · 명목 두께 · 전체 단면), 다른 수송량 (PI = 확산 D, Eq 1 · BE = 전도 k, Eq 2/4) 과 다른 경계조건 (PI 관통 · BE 편측 접근).  둘 다 **tortuosity factor (τ, 제곱 없음 = 우리 tau2 척도)** 이고, **N_M 이나 τ² 가 아니다**.  Nguyen 분류로 PI = eRDM (conventional τ) · BE = eSCM (τ_e).

**② 전극별 τ 값 표** — §3-2 (Fig 8 판독, 95 % CI) · §3-4 (Fig 14 · 15 인쇄값) · §3-5 (분리막 3.24 stated).

**③ 두 방법 차이의 크기 · 원인**
| 비교 | 크기 (판독·파생) | 원인 (원문) |
|---|---|---|
| 양극 1 · 2, BE (미박리) vs PI | ≈ 0 (판독 분해능 ~1 % 안), 둘 다 각자 CI 안 | — (일치) |
| 양극 3, BE 미박리 vs PI | ≈ +62 % | PI 시료 (박리막) 두께 +12 % → 다공도↑ 인데 명목값으로 계산 |
| 음극, BE 미박리 vs PI | ≈ +14 % | 박리막 두께 +5 % |
| 양극 3 · 음극, **BE 박리막** vs PI | ≈ −3.6 % · ≈ −10 % (BE 박리막은 CI 없음) | "reasonable agreement" — 둘 다 PI 최대 불확도 12 % 안 |
| 무캘린더 양극, Al (접촉 반원) vs Cu (박리) — BE 끼리 | +25 % (CI 비겹침) | **원문 미논의** — 맞춤 편향 vs 박리 변화 미분리 (§3-4) |
| 한 스펙트럼, 빠른 추출법 vs 상세 모델 | −10 % (선형) … +4 % (drop-down) | 저주파 곡률 (비이상 차단) · elbow 모호 |
| 나노 기공 이중층 (이론 추정) | 기공 이온의 1–8 % | 불확도 안 → 귀속 불가 |

→ **방법 고유 차이 (τ_e vs conventional τ) 는 이 전극들에서 측정 분해능 (5–12 %) 아래**이고, 관측된 큰 차이는 **두 방법이 서로 다른 시료 상태를 잰 데서** 왔다 (미박리 전극 vs 박리 팽창막 — 박리가 BE 끼리 τ 를 −40 % · −21 % 바꿈, §3-2) 또는 **해석 선택** (접촉 반원 · 빠른 추출법) 에서 왔다.  ⚠ 따라서 PI (eRDM) 의 필수 전처리인 박리가 **넷 중 둘에서 전극의 τ 자체를 바꿨다** — eRDM 값이 원래 전극을 대표하는지는 시료마다 확인해야 한다.  ⚠ 두께는 두 방법에 다른 거듭제곱으로 들어간다 — BE 는 N_M ∝ 1/l (Eq 4), PI 는 확산 시간상수 ∝ L²/D_eff 라 L 오차가 대략 제곱으로 들어간다 (우리 판독 — 원문은 PI 식과 이 전파를 제시하지 않는다).  그래서 박리 팽창이 두 방법을 **다르게** 흔든다.

**④ TLM 식 (원문 번호)** — 지배식 Eq 6–9 · 경계조건 Eq 10–11 · 닫힌 해 Eq 5 (무차원) / Eq 12 (차원) · 축약 Eq 13 (β ≪ 1) → Eq 14 (+ Z₀ ≫ 1) → Eq 15 (+ Z_cc → 0 = Landesfeind/Ogihara) · 맞춤 Eq 17–18 (§4-4 · §4-3).

**⑤ 접촉저항 · R_ct 가 들어가는 자리**
- **고상–집전체 접촉 z_cc** (표 I 뜻): β ≪ 1 · Z₀ ≫ 1 이면 **직렬 가산** R_ion·Z_cc = z_cc/A (Eq 14).  **우리 유도 (원문에 없음, §10-3 검산)**: Z₀ → ∞ 이면 β 가 유한해도 직렬 가산이 정확하다 —
  `Z_EL = z_cc/A + R_ion·[ β/(1+β) + (1 + 2β·sech λL + β²) / ((1+β)·λL·tanh λL) ]`.
  z_cc 를 R ∥ CPE 로 두면 고주파 반원으로 보인다 (Fig 6 · 14a — Al 집전체 양극에서만).
- **전해질–집전체 접촉 z_c (Z₀)**: 평면 집전체–전해질 면적이 작다는 이유로 Z₀ ≫ 1 → 소거.  ⚠ 유한 Z₀ 가지는 우리 독립 풀이와 맞지 않는다 (§10-3) — 원문도 쓰지 않는다.
- **R_ct (전하이동)**: 가로대 z_s = R_ct ∥ CPE.  이상 차단이면 R_ct → ∞ (CPE 만, Eq 15 의 de Levie 꼴).  비이상 차단 (미세 패러데이 반응) 은 유한 R_ct → 저주파 가지 곡률 → 선형 외삽이 τ 를 −10 % 로 준다 (Fig 4b).
- **전자 레일 (β)**: **우리 유도 (원문에 없음, §10-3 검산)** — Z₀ → ∞ 에서 저주파 실수부 → z_cc/A + (R_ion + R_el)/3, 고주파 → z_cc/A + R_ion·R_el/(R_ion + R_el) (R_el = β·R_ion).  ⇒ **그림 4a 의 "R_l − R_h ≈ R_ion/3" 은 β → 0 에서만 맞다.**  β 를 무시한 그래프법 3·(R_l − R_h) 는 R_ion × [(1+β) − 3β/(1+β)] 를 준다: β 0.1 → 0.83 · β 0.5 → 0.50 · 최소 ≈ 0.46 (β ≈ 0.73) · β 2 → 1.0 (우연한 상쇄).

**⑥ 결정 13 (τ_e: P2D 입력 열 보류 · 한정어 "부호 불정") — 이 실측으로 유지된다 (변경 없음).**
- (i) 같은 전극의 eSCM − eRDM 차이가 원문 최대 불확도 (BE 5 % · PI 12 %) 안이고 **부호가 섞인다** (양극 1 · 2 ≈ 0, 박리막 양극 3 −3.6 %, 박리막 음극 −10 % — 판독·파생).  부호를 정할 근거가 없다.
- (ii) 큰 차이 (+62 % · +14 %) 는 원문이 박리 팽창으로 돌렸다 — 두 방법이 **서로 다른 시료 상태** (미박리 vs 박리막) 를 잰 것이고, 그 **비교 인공물이 τ_e/τ 구분보다 컸다**.  Fig 14 의 +25 % 도 같은 부류 (접촉 반원 또는 박리).
- (iii) Nguyen 은 이 일치를 **dead-end 가 적은 잘 퍼콜된 상용 전극**으로 설명한다 (nguyen 카드 §6-bis ⑤, Nguyen p6–7).  우리 코퍼스는 비관통 24/130 (tau2 = ∞, τ_e 유한) · 위상 dead-end p90 2.86 % (메모 v2 §7) · 고체 SE 망 · sink = AM–SE 접촉 — **이 논문이 시험하지 않은 영역**이다.
- ⇒ 바꿀 것 없음.  더할 수 있는 것은 **크기 문장 하나**: *"잘 퍼콜된 액체 LIB 상용 전극 넷에서는 eSCM τ 와 eRDM τ 가 측정 분해능 (5–12 %) 안에서 같았다 (Pouraghajan 2018) — 부호는 정해지지 않았고, ASSB 전이는 검증되지 않았다."*

**⑦ 판단 메모 v2 §7 최소안 (SE 망 + AM–SE 축전 sink + AM 등전위 + 분리막 쪽 Dirichlet + 집전체 차단 → R_eff → R_ion = 3·R_eff → τ_e) 에 주는 것**
- 최소안의 가정 (AM 등전위 · 차단 · 집전체 쪽 이온 차단 · 접촉 0) 은 정확히 **Eq 15 의 조건** (β ≪ 1 · R_ct → ∞ · Z₀ ≫ 1 · Z_cc → 0) 이다 → **모델 쪽** R_ion = 3·R_eff (Nguyen Eq 5, 이 논문 Fig 4a 의 1/3 규칙) 는 그 가정 안에서 맞다.
- **실험 앵커 쪽**에서 걸리는 것 셋 (이 논문이 실측·유도로 준다):
  - **β**: 앵커 셀의 복합양극 전자 레일이 무시 못 할 크기면 β-무시 그래프법 · Eq 15 맞춤이 R_ion 을 최대 ≈ 0.46 배로 준다 (위 ⑤, 우리 유도).  메모 v2 가 이미 *"AM 등전위 (σ_e ≫ σ_ion 가정 — 저 CAM 에서 깨짐, Minnmann τ_el² 120 @25 vol%)"* 라고 적은 그 자리다.  ⇒ 앵커마다 **TLM 에 β 가 들어갔는지**를 기록하고, β 를 우리 망 출력 σ_ion,eff/σ_e,eff 로 침대마다 계산해 둔다 (⚠ σ_AM 50 이 측정값의 약 10 배인 모델 기준값이라 (`CL-92`) 모델 β 는 실제보다 작게 나올 수 있다).
  - **집전체 접촉 반원**: 직렬 z_cc/A 라 TLM 모양이 보이면 빼면 되지만, 반원이 고주파를 가리면 이 논문의 한 사례에서 τ 가 25 % 달랐다 (Fig 14).  원문 대책 = 전해질 전도도 낮추기 (Fig 12) · 집전체 교체 (Fig 14).  ASSB 앵커 (Bazzoun 완전 차단 대칭셀) 를 쓸 때 고주파 반원 유무를 본다.
  - **저주파 곡률 (유한 R_ct)**: 빠른 추출법이 −10 … +4 % — 앵커는 **전 스펙트럼 맞춤값**만 쓴다.
- **확장 아이디어 (미구현 · 우리 제안)**: 우리 망은 AM 전자망도 이미 푼다 → 최소안을 **두 레일 망** (SE 이온망 + AM 전자망 + AM–SE 축전 결합) 으로 바꾸면 β 를 모델 안에서 내고, Eq 5 와 같은 구조의 스펙트럼을 접촉망 판으로 얻는다.  sink 가중이 AM–SE 접촉 면적이라는 점 (LHS-25 선행) 은 그대로다 — 이 논문의 균질 TLM 은 z_s 를 부피당 균일로 두므로 그 문제를 돕지 않는다.
- Z₀ ≫ 1 의 ASSB 판: 복합양극 뒷면의 SE–집전체 접촉 (차단 이중층) 면적이 내부 AM–SE 면적보다 훨씬 작으면 같은 소거가 선다 (우리 판단, 미검증).

### 8-1. 그 밖의 인사이트
- ① **관통형 (eRDM) 실험 앵커의 존재**: PI 의 셀 배치 (막을 분리막 사이에 두고 양쪽 가역 전극) 는 우리 두 띠 Dirichlet tau2 와 같은 위상이다.  ASSB 에서 같은 위상은 메모 v2 가 "관통형에 가깝다" 고 읽은 Minnmann 셀 (양단 Li-In) 쪽이다 [판독 — nguyen 카드 ⑤].  이 논문은 잘 퍼콜된 액체 전극에서 관통형과 편측형이 같은 τ 를 준다는 실측이지, ASSB 에서 Bazzoun (편측형) ↔ Minnmann (관통형) 을 섞어 써도 된다는 근거는 아니다.
- ② **방법 비는 ε 와 무관** (§3-2) — 우리도 망 대조를 할 때 ε (φ) 정의 논쟁을 피하려면 **f (= 1/N_M) 끼리** 비교하면 된다 (Landesfeind 카드 §3-3 ⑥ 과 같은 교훈).
- ③ **내부 기준 정규화** (A2651): 분리막 N_M 을 알면 고주파 절편으로 전해질 고유 전도도를 현장에서 정한다 — "같은 셋업 안의 알려진 구조로 σ₀ 를 지운다" 는 논리가 결정 4 (순수 SE 침대로 T 를 정규화) 와 같다.
- ④ **두께 오차의 거듭제곱이 방법마다 다르다** (§8-0 ③) — 우리 판 간격 L_gap vs 질량보존 두께 L_mc 문제 (결정 1) 와 같은 부류: L 정의가 바뀌면 f 는 1 승, 확산 시간상수형 양은 2 승으로 움직인다.
- ⑤ **Bruggeman 편차의 크기는 시료마다 1.05× (LCO, ε 0.17) … 4.8× (흑연)** (파생) — "Bruggeman 은 과소" 라는 일반 문장이 저다공도 LCO 에서는 거의 0 이다.  우리 `R_bruggeman_over_full` (= N_M/N_M(B)) 을 문헌과 같은 축에서 말할 때 시료 의존 폭을 같이 적는다.

## 9. 인용 가능 문장 (deck/paper용)
- "Pouraghajan et al. (J. Electrochem. Soc. 165, A2644, 2018) measured the tortuosity of commercial liquid-electrolyte Li-ion electrodes with both a DC polarization-interrupt (restricted-diffusion) method and a blocking-electrolyte impedance method; the two agreed within the stated maximum uncertainties (5 % and 12 %) for two cathodes directly and, for a third cathode and a graphite anode, after the impedance test was repeated on delaminated films."
- "In their definition, D_eff = (ε/τ)D and k_eff = (ε/τ)k_int with N_M = τ/ε, so τ is a tortuosity factor (the square of a path-length tortuosity in the τ² convention), with the Bruggeman form τ = ε^−0.5."
- "In the generalized transmission-line model of Pouraghajan et al. (Eq. 14), an electronic contact resistance between the electrode film and the current collector enters in series, Z_EL = R_ion(Z_cc + 1/(λL tanh λL)), when the electronic conductivity greatly exceeds the ionic conductivity and the electrolyte/current-collector interface is blocking."
- "Quick graphical estimates of the pore ionic resistance from one blocking-electrolyte spectrum differed from the full-model value by −10 % (linear extrapolation of the low-frequency branch) to +4 % (drop-down method) (Pouraghajan et al., 2018, Fig. 4b)."

## 10. 주의/한계 (over-claim 방지)

### 10-1. 범위
- ⚠ **액체 전해질 LIB** (LiPF₆ EC:DEC · TBAPF₆ EC:DMC, PVDF 계 상용 전극).  LPSCl 전고체로 수치 **전이 불가** — 쓰는 것은 정의 · 방법 차이의 실측 크기 · 앵커 판독 편향 목록뿐.
- ⚠ **τ 표가 없다** — Fig 8 값은 판독 (TREND 전용).  양극 1 · 2 의 BE/PI 차이는 판독 분해능 (~1 %) 수준이라 부호를 말하지 않는다.
- ⚠ 다공도 3/4 이 36 % (공급사 또는 "통상값") — τ 절대값과 Bruggeman 배수 (파생) 는 그 가정을 물려받는다.  N_M · 방법 비는 무관.
- ⚠ "일치" 는 원문의 정성 표현 (*"reasonable agreement"*) 이다.  BE 박리막 값에는 CI 가 없다 (Fig 8 캡션) — 박리막 대조 (−3.6 % · −10 %) 는 PI CI 와만 겹친다.
- ⚠ 시료가 넷 (상용) 이고 τ 범위 ≈ 2.5–8 — dead-end 가 많은 구조 · 비관통 구조 · 구배 전극은 없다.  Nguyen 의 "구조 따라 −46 % … +61 %" (nguyen 카드) 영역은 이 실측이 덮지 않는다.
- ⚠ Fig 14 의 +25 % 는 원문 미논의 · 각 3 회 시험 · 한 시료 — 원인 귀속은 우리 판독.
- ⚠ 나노 기공 이중층 1–8 % 는 크기 추정 (기공 50 nm 가정) 이지 측정이 아니다.
- ⚠ 블로킹 전해질 k_int 값 미기재 · 분리막 내부 기준 정규화는 "가능" 이라고만 적혀 있다 (적용 여부 미상).

### 10-2. 원문 안의 불일치 · 오기 (렌더로 확인 — 인용 시 주의)
- **z_c / z_cc 뜻이 뒤바뀐 자리**: Eq 10–11 · A2647 첫 문장 (z_c = 고상, z_cc = 전해질) ↔ 표 I · 그림 5 · Eq 14 앞뒤 문장 (z_cc = 고상, z_c = 전해질).  닫힌 해는 표 I 뜻과 맞는다 (§10-3).
- **이중 각 관계 문장 반전**: A2650 *"the angle … in the high frequency region is twice the angle in the low frequency region"* ↔ 그림 4a (θ₁ 고주파 · θ₂ = 2θ₁ 저주파).  이상 TLM 은 고주파 45° · 저주파 90° (CPE 면 γ 배) 라 **그림이 맞다** (우리 판단).
- **그림 6 캡션 "model fit using Equation 15"** ↔ 본문은 그런 스펙트럼에 Z_cc 를 넣어야 한다고 적는다 (Eq 15 에는 Z_cc 가 없다) — Eq 14 의 오기로 보인다 (우리 판독).
- **그림 12 축 라벨** Re(Z) · −Im(Z) 가 서로 바뀌어 인쇄 (곡선 모양은 가로 = Re).
- **표 I λL** 분모의 σ 에 "eff" 첨자 누락 (= √((1+β)R_ion/Z_s) 와 같게 읽으면 σ_eff).
- **분리막 경계조건** "the electrolyte potential is fixed, φ₁ = φ₂" (A2647) — 전해질 전위 고정이면 φ₂ = 상수여야 한다 (φ₁ = φ₂ 를 네 번째 조건으로 두면 U = 0 에서 구동항이 없다 — 우리 판단).
- **그림 15b "2.42 ± 0.3"** — 인쇄 그대로 (다른 값들은 ±0.03–0.1 자리).
- **γ_s** (A2650) 와 **Eq 16 농도 지수 α** 는 표 I · 표 II 에 정의가 없다.  표 II 는 η_s 를 "Anodic overpotential" 로 적는다.
- 사소: 본문 "3 commercially supplied transition metal oxide (TMO) cathodes" + "Hydro-Quebec also provided a lithium cobalt oxide (LCO) cathode" ↔ 표 III 은 양극 셋 (LCO 1 + TMO 2) — LCO 를 셋 중 하나로 읽으면 맞다.

### 10-3. 우리 검산 (원문에 없는 계산 — 스크립트는 카드 밖 작업 공간, 값만 기록)
- **Eq 12 ≡ Eq 5** (표 I 의 무차원 정의로): 무작위 매개변수 6 조합에서 상대차 ≤ 1e-15 — 원문 *"reduces to Equation 5"* 확인.
- **첨자의 물리 뜻 (극한 검사)**: Eq 12 에서 z_c → ∞ · z_cc → 0 이면 de Levie 극한 R_ion·coth(λL)/λL 이 나오고, z_cc 를 키우면 정확히 z_cc/A 가 직렬로 더해진다 → 닫힌 해 안에서 **z_c = 전해질–집전체 (막히면 de Levie), z_cc = 고상–집전체 (직렬)** — 표 I 의 뜻이다.
- **독립 풀이 대조**: Eq 6–9 를 원문 경계조건 (집전체: 고상 접촉 · 전해질 접촉, U = 0 · 분리막: i₁ = 0 · φ₂ 고정) 으로 직접 푼 BVP 와 비교 — **Z₀ → ∞ 에서 Eq 12 와 일치** (β ≈ 0 과 β = 0.5, 실수·복소 z_s, 고상 접촉 유무 모두).  de Levie 극한 R_ion·coth(λL)/λL 재현 · z_cc 는 정확히 z_cc/A 직렬.
- **유한 Z₀ (전해질–집전체 접촉이 유한)**: Eq 12 가 우리 BVP 와 **어긋난다** (1 % 에서 부호 반전까지; Z_cc → ∞ 극한에서 Eq 5 는 −z_c/A 라는 음의 저항을 준다).  극한 하나 더: 전해질이 집전체에 단락 (z_c → 0) · 고상 단절 (z_cc → ∞) 이면 Eq 12 는 **0** 인데, BVP 는 **≈ R_ion** (용량성 z_s 저주파 5.00 Ω @ R_ion 5 Ω — 이온이 전해질 레일을 그대로 통과하므로 물리적으로 그래야 한다).  전해질 쪽 경계조건 부호를 뒤집어도 재현되지 않는다 → **원인 미규명**.  원문은 이 가지를 쓰지 않는다 (Z₀ ≫ 1) — **유한 Z₀ 가지는 재유도 없이 쓰지 말 것.**
- **유한 β 극한** (§8-0 ⑤ 의 식): Z₀ → ∞ 축약식이 Eq 5 와 상대차 2e-11 (유한 R_ct 가로대 포함) · 저주파 (R_ion + R_el)/3 은 Eq 5 와 BVP 가 각각 독립으로 재현 · 고주파 R_ion∥R_el 은 BVP 로 확인.

### 10-4. 판단 메모 v2 정정 후보
- **없음** — 메모 v2 의 이 논문 관련 문장 (§8-1 순위 10 *"eRDM vs eSCM 실측 비교 + 접촉저항 · R_ct 를 넣은 일반 TLM"* · §7 최소안 *"R_ion = 3·R_eff (Nguyen Eq 5)"* · §5-3 한정어 · 결정 13 의 "부호 불정") 중 원문과 어긋나는 것은 없다.
- 보강 후보 둘 (정정 아님): ① §8-1 순위 10 설명에 **고상 전자저항 (β = k_eff/σ_eff)** 이 빠져 있다 — 일반 TLM 의 세 번째 성분 (표 I · Eq 5; nguyen 카드 §4-B 는 이미 적었다).  ② §7 최소안의 R_ion = 3·R_eff 는 모델 쪽 (AM 등전위 = β 0) 에서 정확하고, **실험 앵커 판독에는 β 보정이 필요**하다 (이 카드 §8-0 ⑤ · ⑦, 우리 유도).
- 서지 표기: 메모 v2 §8-1 은 Nguyen 목록 문자열 그대로 "165, 2644–2653" 이다 (규칙대로) — 학술지 인쇄 쪽은 **A2644–A2653**.

---

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 원문 ref | 목록 서지 (그대로) | 왜 볼 만한가 |
|---|---|---|
| 24 | I. V. Thorat, D. E. Stephenson, N. A. Zacharias, K. Zaghib, J. N. Harb, and D. R. Wheeler, Journal of Power Sources, 188(2), 592 (2009). | PI (eRDM) 원조 · restricted-diffusion 모델 식과 두께 의존 (L² ?) 확인 · 분리막 AC 법 |
| 25 | U. Tröltzsch and O. Kanoun, Electrochimica Acta, 75, 347 (2012). | 일반 TLM 경계조건의 비교 대상 (원문 A2647) — 유한 Z₀ 가지 불일치 (§10-3) 판별에 필요 |
| 26 | H. Göhr, Advances in Electrochemical Applications of Impedance Spectroscopy, p. 2, ZAHNER-elecktrik GmbH & Co., Aug. (1997). | 같은 계열 TLM 원형 (원문 A2645) |
| 15 | S. Malifarge, B. Delobel, and C. Delacourt, Journal of The Electrochemical Society, 164(11), E3329 (2017). | 고상 전자저항 임의값 포함 대칭셀 TLM (nguyen 카드 ref 18) — β 보정의 독립 출처 |
| 32 | M. Gaberscek, J. Moskon, B. Erjavec, R. Dominko, and J. Jamnik, Electrochemical and Solid-State Letters, 11(10), A170 (2008). | 고주파 반원 = 전극–집전체 접촉 귀속의 원 근거 |
| 13 | N. Ogihara, Y. Itou, T. Sasaki, and Y. Takeuchi, The Journal of Physical Chemistry C, 119(9), 4612 (2015). | drop-down 법 · SOC 0/100 % 차단 |
| 14 | N. Ogihara, S. Kawauchi, C. Okuda, Y. Itou, Y. Takeuchi, and Y. Ukyo, Journal of The Electrochemical Society, 159(7), A1034 (2012). | TLM-C 대칭셀 원법 (Landesfeind 카드가 >30 % 과대 지적) |
| 10 | N. A. Zacharias, D. R. Nevers, C. Skelton, K. Knackstedt, D. E. Stephenson, and D. R. Wheeler, Journal of The Electrochemical Society, 160(2), A306 (2013). | PI 법 선행 + "Bruggeman 과소 예측" 근거 (원문 A2644) |
| 28 | B. J. Lanterman, A. A. Riet, N. S. Gates, J. D. Flygare, A. D. Cutler, J. E. Vogel, D. R. Wheeler, and B. A. Mazzeo, Journal of The Electrochemical Society, 162(10), A2145 (2015). | "전자저항이 이온저항보다 작다" 를 확인한 자체 실험 근거 후보 (원문 A2646 refs 27, 28) |
| 27 | S. W. Peterson and D. R. Wheeler, Journal of The Electrochemical Society, 161(14), A2175 (2014). | 같은 근거 후보 |
| 29 · 30 | J. Bisquert, G. Garcia-Belmonte, P. Bueno, E. Longo, and L. Bulhoes, Journal of Electroanalytical Chemistry, 452(2), 229 (1998). · J. Bisquert, The Journal of Physical Chemistry B, 106(2), 325 (2002). | Warburg 확산 TLM — 차단 스펙트럼과 같은 꼴 (원문 A2647) |
| 31 | A. Lasia, Electrochemical impedance spectroscopy and its applications, Springer (2014). | 목적함수 가중 (원문 A2650) |
| 19 | T. Hutzenlaub, A. Asthana, J. Becker, D. Wheeler, R. Zengerle, and S. Thiele, Electrochemistry Communications, 27, 77 (2013). | PI 이완 맞춤 "prior work" 로 인용 (A2649) · FIB-SEM + 단층촬영 결합 |
| 23 | L. Zielke, T. Hutzenlaub, D. R. Wheeler, I. Manke, T. Arlt, N. Paust, R. Zengerle, and S. Thiele, Advanced Energy Materials, 4(8), 1301617 (2014). | 탄소·바인더가 이온 수송에 큰 영향 (A2645) — 이미지 기반 τ 가 낮게 나오는 이유 |
| 11 | B. Tjaden, D. J. Brett, and P. R. Shearing, International Materials Reviews, 63(2), 47 (2018). | 정본 카드 있음 (`tjaden2018_tortuosity_review_calculation_approaches`) |
| 12 | J. Landesfeind, J. Hattendorff, A. Ehrl, W. A. Wall, and H. A. Gasteiger, Journal of The Electrochemical Society, 163(7), A1373 (2016). | 정본 카드 있음 (`landesfeind2016_tortuosity_eis_electrodes_separators`) |

## 12. 관련 카드
- `nguyen2020_electrode_tortuosity_factor` — 이 논문을 ref 20 으로 인용, eRDM/eSCM 분류와 τ_e 정의의 정본.  이 카드 §8-0 ⑥ 의 (iii) 은 그 카드 기록에 기댄다.
- `landesfeind2016_tortuosity_eis_electrodes_separators` — BE 법 원조 (이 논문 ref 12) · TLM-Q · 접촉 반원 귀속 (Fig 12) — 이 논문 Eq 15 와 같은 꼴.
- `tjaden2018_tortuosity_review_calculation_approaches` — 명명 정본 (κ = τ²) · 실험 τ 분류 (AC impedance / polarisation-interrupt).
- `taufactor_tortuosity_factor_tomography_tool` — mode 5 (eSCM) · mode 6 (τ_e) 구현.
- `bazzoun2026_dem_fem_rnm_ionic` — ASSB 완전 차단 대칭셀 TLM 앵커 (eSCM 형) — §8-0 ⑦ 의 β · 접촉 반원 점검 대상.
- `minnmann2021_jes_charge_transport_bottlenecks` — ASSB 전자 차단 + 양단 Li-In (관통형에 가까움) — §8-1 ①.
- 같은 묶음 (2026-10-03 inbox #7, 작성 중): Siroma 2015 TLM 해 모음 — 이 카드 §10-3 의 유한 Z₀ 가지 판별에 함께 볼 것 (링크 확정은 메인).

## Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

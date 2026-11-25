<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md.
     이 논문은 시뮬레이션이 아니라 *측정법·정의* 논문(액체 전해질 LIB)이다. 그래서 §4 '방법' 을 EIS 측정 사슬로,
     §8 을 'tortuosity 정의 대조표' 로 확장했다 (이번 묶음의 목적 = tortuosity 정의를 닫는다).
     값 표지: stated = 본문·캡션·표 원문 / 판독 = 그림에서 읽은 값 (TREND 전용, 정밀 인용 금지) / 파생 = 카드 작성자 계산 (식 명시). -->
# 전극·분리막 tortuosity 를 임피던스(EIS)로 측정 — 차단 전해질 대칭셀 + 전송선 모델(TLM-Q) · MacMullin 수 · Bruggeman 검증 — Landesfeind (J. Electrochem. Soc. 2016)

> slug `landesfeind2016_tortuosity_eis_electrodes_separators` · DOI `10.1149/2.1141607jes` · type `exp (EIS impedance — 분리막 HFR · 전극 차단 대칭셀 TLM-Q; liquid-LIB tortuosity/MacMullin 측정법)` · PDF `5. Tortuosity determination of battery electrodes and separators by impedance spectroscopy.pdf` · digested `2026-10-02` · status ✅
>
> ★ **정의 판정 (이 카드의 목적)** — 이 논문의 **τ 에는 제곱이 없다**. `N_M = κ/κ_eff` (Eq. 1) 과 `N_M = τ/ε` (Eq. 5) 에서
> **τ = ε·N_M = ε·κ/κ_eff** (Eq. 8 · 13) 이고, 이름은 *effective tortuosity* 지만 값은 **다른 문헌이 "tortuosity factor τ²" 라 부르는 양**이다
> (원문 p.A1374 가 직접: *"the tortuosity τ in Eq. 5 appears often as τ²"*).  ⇒ **이 논문 τ = COMSOL τ_F (f = ε/τ_F) = 우리 T = φ_SE·σ₀/σ_eff**.
> 웹앱 **τ_Lap,eff = √(φ·σ_grain/σ_full) 는 그 제곱근**이고, 기하 최단경로 계열(τ_Dijkstra · τ_Dij,all · 벽 τ)은 원문의 **τ_geo / τ_path** 로
> Eq. 5 의 τ 와 **다른 정의**다 (원문이 Holzer 를 들어 엄격 구분을 요구, p.A1374).  상세 = §8, 전고체 이전 조건 = §9.
>
> ⚠ **[미확인: 정오표 미열람]** — 이 논문에는 정오표가 있는 것으로 알려져 있다 (메인 전달: DOI `10.1149/2.0261706jes`, 이 카드에서 원문 확인 안 함).
> 이 카드의 모든 수치는 **본 논문 원문 그대로**이고 정오표 반영 여부는 모른다.  특히 §5-1 의 **Separion 행 내부 불일치**가 정오표 대상인지 미확인.
>
> 출처 PDF = `litdb/inbox/tortuosity_20261003/5. ….pdf` (16쪽).  **1쪽은 IOP 표지 + "You may also like" 광고**(본문·인용 아님).
> 본문 = PDF 2–16쪽 = 저널 **A1373–A1387** (PDF 쪽 p ↔ 저널 A(1371+p)).  아래 쪽 표기는 전부 저널 쪽(A13xx)이다.

---

## 0. 결론 먼저 (정의 판정 + 핵심 수치)

| 질문 | 답 | 근거 (식·쪽) |
|---|---|---|
| 이 논문의 τ 는 "제곱 들어간 양(tortuosity factor)" 인가 "기하 tortuosity" 인가? | **기하 τ 가 아니다.** 실험으로 정하는 *effective tortuosity* τ = ε·N_M 이고, 수치상 다른 문헌의 **τ² (tortuosity factor)** 와 같은 양 | Eq. 5 (A1374) · "appears often as τ²" (A1374) · Holzer 구분 (A1374) |
| COMSOL τ_F 와 같은 양인가? | **같다** | A1374: COMSOL 은 Bruggeman 을 *"ε/τ = ε^1.5"* 로 표현 · COMSOL 5.6 Eq. 6-6 `f_e = ε_p/τ_F` (메인 제공, 매뉴얼 원문은 이 카드에서 미열람) |
| 우리 T = φ_SE·σ₀/σ_eff 와 같은 양인가? | **정의식·정규화가 같다** (A = 전체 기하 단면, d = 전체 두께, ε = 총 부피 기준). 전고체로 옮길 때 같은 양이 되는 조건은 §9 | Eq. 8 (A1375) · 우리 망 `σ/σ_bulk = G·plate_z/(box_x·box_y)` |
| 웹앱 τ_Lap,eff 와 같은가? | **아니다 — 제곱근이다** (τ_Lap,eff² = T = 이 논문 τ) | §8 |
| Bruggeman (구형 입자) | τ = ε^−0.5 ⇔ N_M = ε^−1.5 (α = 0.5, Archie m = 1.5) | Eq. 6 (A1374) · Table II 캡션 (A1379) |
| 측정값 ÷ Bruggeman | 분리막 N_M **1.8–4.5×** · 전극 **~1.5–3×** (요약 문장; 판독상 일부 3–4×, §5-9) | A1379 · A1386 |
| 전극의 τ(ε) 함수형 | f = 1 인 Bruggeman 으로는 **안 맞는다** — τ = f·ε^−α 에 **f 3.0–4.7, α 0.1–0.6** 필요 | Fig. 19 · Fig. 20 (A1385) |

---

## 1. 한 줄 요약
액체 전해질 LIB 의 **분리막**(10종)과 **다공 전극**(LFP 2조성·LNMO·NMC111·LTO·흑연 2종)의 이온 저항 R_Ion 을 EIS 로 재서
**MacMullin 수 N_M = κ/κ_eff** 와 **tortuosity τ = ε·N_M** 로 바꾸는 표준 측정법을 세운 논문.  분리막은 **절연 둘레를 가진 Cu 블록 셀의 고주파 저항(HFR)**,
전극은 **비삽입 염(TBAClO₄)으로 만든 차단(blocking) 대칭셀 + CPE 를 쓴 전송선 모델(TLM-Q)** 로 잰다.  결과: 흔히 쓰는 **구형 입자 Bruggeman
(τ = ε^−0.5) 은 분리막·전극 모두 크게 과소평가**하고, 전극은 입자 형상(판상 흑연 ≈ 2× NMC)·입경(LNMO ~17 vs LTO ~8)·도전재 함량에 따라 N_M 이 크게 갈린다.
우리에게는 **τ 의 정의(제곱 없음)와 정규화**를 원문으로 못박아 주는 기준 논문이다 (수치 자체는 액체 LIB 라 전이 불가).

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Johannes Landesfeind**(교신, j.landesfeind@tum.de), Johannes Hattendorff, Andreas Ehrl, Wolfgang A. Wall, **Hubert A. Gasteiger** — TU München (Chair of Technical Electrochemistry · Institute for Computational Mechanics) | **J. Electrochem. Soc. 163 (7) A1373–A1387 (2016)** | **10.1149/2.1141607jes** | 액체 전해질 LIB: 분리막 (Celgard·Separion·Freudenberg·상용 HDPE) / 전극 LFP·LNMO·NMC111·LTO·흑연 (PVDF Kynar HSV 900 + Super C65) | **실험 (EIS 측정법)** — 시뮬레이션 없음 |

- 접수 2016-03-03 · 수정본 2016-04-08 · 게재 2016-04-28.  **Open access CC BY-NC-ND 4.0** (A1373).
- 연구비: EEBatt (바이에른 경제부) — J.L.·A.E. / BMBF ExZellTUM 03X4633A — J.H. (A1386).
- 공저자 Ehrl·Wall 은 계산역학 소속이지만 **이 논문에 수치 모델은 없다** (EIS 측정 + 등가회로 해석해만).
- PDF 1쪽 광고 목록(본문 아님)에 같은 저자군의 *"Effective Ionic Resistance in Battery Separators"* (Hattendorff, Landesfeind, Ehrl et al.) 이 보인다 — **본문 인용 목록에는 없고 서지 미확인**.
- 정오표: **[미확인: 정오표 미열람]** (위 머리말 참조).
- "Note added in proof" (A1386): Bruggeman 관계의 기원·적용 상세는 Ref. 50 (Tjaden, Cooper, Brett, Kramer 2016) 참조.

---

## 3. ★ 정의식 — 원문 식 번호·쪽 그대로

### 3-1. 정의 계열 (Eq. 1–7)

| 식 | 원문 형태 | 쪽 | 원문 이름 | 뜻 · 원문 단서 |
|---|---|---|---|---|
| **Eq. 1** | `N_M = κ / κ_eff` | A1373 | MacMullin number | κ = 전해질 용액 이온전도도, κ_eff = 다공 분리막·전극의 유효 이온전도도.  거시 관점 (Patel et al. [2] 인용) |
| **Eq. 2** | `N_M = ε^(−m)` | A1373 | Archie 의 경험식, m = Archie's exponent | 사암 다공도–N_M 멱법칙.  *"같은 지층(비슷한 미세구조) 시료군에서만 성립"* (Holzer [6] 인용) |
| **Eq. 3** | `τ_path = d_path / d` | A1373 | path-length tortuosity | **단면이 일정한 단일 채널**에 대해 정의 (d = 직선 거리) |
| (본문) | τ_el · τ_geo · τ̄_geo | A1373–A1374 | electronic(물리적) / geometrical / mean geometrical tortuosity | τ_el = 전위 구배 기반 경로 길이; τ_geo = 두 점 x₁·y₁ 의 **최단 연결 길이 ÷ 직선 길이**; τ̄_geo = 점쌍 최단 경로 d_ij 의 평균 (random walk [11] · graph theory [10]).  *"τ_path, τ_geo, τ_el 은 같지 않고 다른 수치를 줄 수 있다"* (A1373).  이 수치 알고리즘들은 **경로 늘어남만** 보고 가변 단면·표면 미세구조는 **포함하지 않는다** (A1374) |
| **Eq. 4** | `N_M ≡ τ̄_geo / (ε·β)` | A1374 | constriction factor β (Wiedenmann [10]) | 가변 단면을 β 로 보정.  ⚠ **인쇄형은 τ̄_geo 1승** — 원 출처의 지수(제곱 여부)는 **[미확인: Wiedenmann 2013 원문 미열람]**.  참고: Tjaden 2018 리뷰(같은 inbox #2) Eq. (4) `D_eff = (ε·δ/τ)·D_bulk` (van Brakel–Heertjes 의 constrictivity δ) 도 1승 꼴 |
| **Eq. 5** | `N_M = τ / ε` | A1374 | **effective tortuosity τ** | 미시 개념을 거시에 경험적으로 적용, τ 는 **시료마다 실험으로 결정**.  τ 는 경로 늘어남뿐 아니라 **가변 단면·표면 형상 등 "모든 기하 효과"를 자동 포함**; 단점 = 실험 아티팩트가 섞일 수 있고 **다른 기하(입자 형상·다공도)로 외삽 불가** (A1374).  같은 거시 개념을 3D 재구성 위 **Laplace 방정식 수치해**로 N_M 을 얻는 데도 쓴다 (Ender [35] · Joos [15] · Cooper [12], A1374) |
| **Eq. 6** | `τ = ε^(1−m) = ε^(−α)` | A1374 | "Bruggeman relation" (이 관례의 기원은 불명확하다고 원문이 적음) | Eq. 2 + Eq. 5.  **−α = 1 − m**.  구형 입자: **α = 0.5 ↔ m = 1.5** |
| **Eq. 7** | `τ = f·ε^(−α)` | A1374 | generalized Bruggeman, f = proportionality factor | 복잡 구조에서 다른 α 가 나오고 비례인자 f 를 붙이는 관례 (Thorat [18] · De La Rue–Tobias [19]).  이 논문의 전극 맞춤 식 |

### 3-2. 측정식 (Eq. 8–13)

| 식 | 원문 형태 | 쪽 | 용도 | 원문 단서 |
|---|---|---|---|---|
| **Eq. 8** | `N_M = τ/ε = R_Ion·A·κ / d` | A1375 | R_Ion → N_M, τ | Eq. 1 + 5 로 옴 법칙 재배열.  **N_M 은 다공도를 몰라도 되고, τ 는 다공도가 필요**하다 (A1375) |
| **Eq. 9** | `Z_CPE = 1 / (Q·(iω)^γ)` | A1375 | 차단 전극 계면 = CPE | γ = 1 이면 이상 축전기.  표면 거칠기 [37]·불균일 전류분포 [38] 때문에 CPE 로 기술 |
| **Eq. 10** | `Z_Sep = R_Ion + 1 / (Q_S·(iω)^γ)` | A1375 | 분리막 (전자 부도체) 차단 등가회로 = Fig. 1 | 두 CPE 를 하나로 묶음 → **고주파 외삽 (ω→∞) 으로 R_Ion** |
| **Eq. 11** | `Z_El = √(R_Ion·Z_S)·coth(√(R_Ion/Z_S)) = √(R_Ion/(Q_S·(iω)^γ))·coth(√(Q_S·(iω)^γ·R_Ion))` | A1376 | 전극 간이 TLM (Fig. 3) = **TLM-Q** | `R_Ion = Σ(r_Ion)`, `Q_S = Σ(q_S)`.  γ = 1 이면 **TLM-C** (Ogihara [26]) |
| **Eq. 12** | `Z_El(ω_low → ∞) = R_Ion/3 + R_HFR` | A1376 | 그래프법: 저주파 가지를 실축으로 외삽 | 원문 표기 그대로 ("ω_low → ∞").  이상 축전기 TLM 에서 Ogihara [26]·Liu [25] 가 보인 관계이고 **CPE 를 써도 같은 관계가 성립** (A1376) |
| **Eq. 13** | `τ = R_Ion·A·κ·ε / (2d)` | A1382 | 대칭셀 전극의 τ | **2 = 같은 전극 두 장의 임피던스 합**을 재기 때문.  ε = 면적 무게 + 두께로 산출 |

### 3-3. 원문이 직접 적은 관례 충돌 (정의 닫기의 1차 근거)

| # | 원문 문장 (요지) | 쪽 | 우리에게 뜻하는 것 |
|---|---|---|---|
| ① | *"the tortuosity τ in Eq. 5 appears often as τ², which is the result of different assumptions"* (Clennell [13], Djian [14]) | A1374 | 같은 N_M 을 `N_M = τ/ε` (이 논문) 로도, `N_M = τ²/ε` (다른 관례) 로도 쓴다 → **이 논문 τ = 다른 관례의 τ²** |
| ② | *"in some cases the tortuosity is also defined differently, e.g., as τ = ε^(1−α)"* (Thorat [18]) | A1374 | Thorat 의 α 는 **κ_eff = κ·ε^α 의 지수** (구형 1.5) → 이 논문 α(0.5) 와 **뜻이 다르다**.  "Bruggeman 지수 1.5" 와 "0.5" 는 같은 구형 Bruggeman 의 다른 표기 |
| ③ | *"The Bruggeman exponent relates to Archie's exponent by −α = 1 − m"*; 구형 α = 0.5 ↔ m = 1.5 | A1374 | m = 1 + α (= Thorat 의 α = COMSOL 의 1.5) |
| ④ | Bruggeman 근사가 *"commercial software packages (e.g., Comsol Multiphysics), where it is expressed terms of ε/τ = ε^1.5"* 로 구현 | A1374 | **COMSOL 의 τ = 이 논문 τ** (ε/τ = ε^1.5 ⇒ τ = ε^−0.5).  COMSOL f = ε/τ = κ_eff/κ = 1/N_M |
| ⑤ | *"it is important to strictly distinguish between the effective tortuosity τ and the geometrical tortuosity τ_geo, since they are based on different definitions"* (Holzer [6]) | A1374 | 우리 τ_Dijkstra · τ_Dij,all · 벽 τ (최단경로) 를 Eq. 5 의 τ 자리에 넣지 않는다 |
| ⑥ | N_M 은 쉽게 재는 두께만 필요 → *"more straightforward comparison with the literature"* | A1379 | 문헌 비교는 ε 정의에 덜 휘둘리는 **N_M (= 1/f)** 로 하는 것이 안전 |

### 3-4. 판정 — 이 논문의 "τ" 는 무엇인가
- **τ (Eq. 5 · 8 · 13) = ε·N_M = ε·κ/κ_eff — 제곱 없음.**  이름은 *effective tortuosity* 이지만 정의상 *tortuosity factor* 계열(= 다른 관례의 τ²)이다.
- **기하 tortuosity 가 아니다.**  기하 쪽은 τ_path (Eq. 3) · τ_geo · τ̄_geo (Eq. 4 문맥) 로 따로 이름 붙어 있고, 원문이 둘을 섞지 말라고 한다 (③⑤).
- **실험 τ 는 "모든 기하 효과" 를 묶는다** (가변 단면·표면 형상 포함).  다만 액체 전해질은 연속체라 **전도상 내부 계면저항이 없다** — 이것이 전고체로 옮길 때 첫 번째로 깨지는 가정이다 (§9).

---

## 4. ★ 측정법 — R_Ion 을 재서 τ 로 바꾸는 사슬

### 4-1. 공통 사슬

| 단계 | 분리막 | 전극 |
|---|---|---|
| ① 무엇을 재나 | 전해질 함침 분리막의 **R_Ion** | 전해질 함침 다공 전극의 **이온 레일 저항 R_Ion** (전자 레일은 무시 가능 조건) |
| ② 차단 조건 | 전자 부도체라 자동 — Cu 전극 사이에서 계면은 CPE (Eq. 10) | **비삽입 염 TBAClO₄** 로 전하이동 반응을 없앰 (±10 mV 창에서 안정, A1376) |
| ③ R_Ion 추출 | **HFR** = Nyquist 고주파 실축 외삽 (Eq. 10) | **TLM-Q 맞춤** (Eq. 11) 또는 **그래프법**: (저주파 가지 실축 절편 − HFR) × 3 (Eq. 12) |
| ④ 정규화 | `N_M = R_Ion·A·κ/d` (Eq. 8) | 대칭셀 `τ = R_Ion·A·κ·ε/(2d)` (Eq. 13), `N_M = τ/ε` |
| ⑤ A | 상부 Cu 전극 면적 (Ø 20 mm = 3.14 cm²; 둘레 절연 필수) | 전극 면적 (T-cell Ø 11 mm 원판; 파우치는 **이미지 분석**으로 활성 면적) |
| ⑥ d | 제조사 사양 두께 (자체 측정과 "excellent agreement", A1379) | **코팅 두께** (Mitutoyo Lifematic VL-50, 0.1 µm 분해능; 절대오차 ±2 µm) |
| ⑦ ε | **제조사 사양 다공도** (Table II) | **질량 수지 다공도** — 면적 무게 + 두께 + 벌크 밀도 (Table I 의 AM 밀도, 도전재 ~2.2 g/cm³) |
| ⑧ κ | 전해질 전도도 센서 (SI Analytics LF 1100+, 25 °C) | 같음 |

### 4-2. 분리막 — 절연 둘레 Cu 블록 셀 (Fig. 5 · Fig. 7 · Fig. 8 · Fig. 9)
- **셀**: 글러브박스 안 **개방형 Cu 블록 2개** + 능동 차폐 케이블로 밖의 포텐쇼스탯 연결.  상부 Cu: 높이 10 mm · **Ø 20 mm**; 하부 Cu: 높이 15 mm · Ø 50 mm,
  전해질 저장조 깊이 5 mm (보통 ~2 mm 채움) · 내경 45 mm; 분리막 Ø ≥ 25 mm (Fig. 5 캡션).  과량 전해질 → 젖음 양호, 측정이 수 분 안이면 용매 증발 무시 가능.
- **핵심 = 상부 전극 둘레 절연** (에폭시 EPO5.S200 를 날카로운 모서리로 연마).  절연이 없으면 **stray current 가 전해질로 우회해 측정 면적을 미지량만큼 늘린다** →
  큰 산포 (Fig. 7a); 절연하면 반복 3회가 동일 (Fig. 7b).  분리막 면내 전도 때문에 유효 지름은 ~분리막 두께 3배만큼 커지는데, 최대 두께 ~75 µm(3장)에서
  유효 3.28 vs 명목 3.14 cm² → **면저항 오차 < 5 %** (A1378).
- **선형성 검증 (Fig. 8)**: R_Ion·A 가 분리막 장수에 **완전히 선형**, 절편 **x₀ = 0.10 Ω·cm²** (R² = 0.998) = 분리막 1장 저항의 **<3 %** → 접촉저항·젖음 아티팩트 없음.
  Cu 블록(층수당 4회)과 파우치(층수당 1회, 25 mbar 진공 밀봉)가 일치.  층수별 SD < 3.5 %.
- **κ 불변 검증 (Fig. 9)**: Celgard 2325 한 장, **κ 0.41–12.5 mS/cm** (5 전해질) 에서 **τ = 4.03 ± 0.24** (SD ~6 %; 일부는 글러브박스 온도 ±1.0 °C).
  저 κ = 불순물 민감, 고 κ = 저항이 작아 케이블 인덕턴스·작은 접촉저항이 상대적으로 커짐 → **최적 κ 3–10 mS/cm, 시료 Ø 25 또는 40 mm** (A1378).

### 4-3. 전극 — 차단 대칭셀 + TLM-Q (Fig. 2 → Fig. 3 · Fig. 4 · Fig. 11 · Fig. 13 · Fig. 14)
- **일반 TLM (Fig. 2)**: 고체상 전자 저항 r_El 직렬 사슬 + 전해질상 이온 저항 r_Ion 직렬 사슬 + 두 레일 사이 표면 임피던스 z_S (패러데이/용량성).
  집전체에 붙은 전극은 전자 레일이 한쪽 끝, 이온 레일이 다른 끝(분리막 쪽)에서만 연결된다.
- **간이화 조건 (Fig. 3)**: ① **r_El ≪ r_Ion** — 도전재가 있으면 κ_el > 0.1 S/cm 대 κ_ion < 0.01 S/cm (A1376); ② **차단** — 패러데이 반응 없음 → z_S = CPE.
- **TLM-Q vs TLM-C (Fig. 4, 모의: R_Ion 300 Ω, Q 100 µF·s^(γ−1), γ = 1 또는 0.9)**: TLM-C 는 고주파 45°, 저주파 **수직선**;
  TLM-Q 는 고주파 45° 보다 낮고 저주파가 90° 보다 눕는다.  실측 저주파 가지는 수직이 아니므로 (이 논문 Fig. 11, Ogihara 의 Fig. 6 도) **TLM-C 맞춤은
  저주파 절단점 선택에 민감** → TLM-Q 채택 (A1380–A1381).
- **실측 차이 (Fig. 11, graphite-1)**: 두 전극 합 R_Ion = **31.6 Ω (그래프법) ≈ 31.0 Ω (TLM-Q 맞춤)**, 그러나 **TLM-C 맞춤 40.6 Ω (>30 % 과대)** (A1380).
- **차단 실현법 — 비삽입 염**: Ogihara [26,27] 은 Li 염 + SOC 0 %/100 % 로 차단을 가정했지만, 이 저자들의 예비 실험에서는 **SOC 0/100 % 에서도 일부 전극이 반원을 보였다**
  (불충분한 전하이동 억제 또는 전자 접촉저항).  TBAClO₄ 를 쓰면 **관측된 반원을 집전체–코팅 접촉저항에 명시적으로 귀속**할 수 있다 (A1381).
- **R_Ion → τ**: Eq. 13 (×1/2 대칭셀).  Fig. 15 의 N_M 은 **그래프법** (저주파·중주파 외삽 절편 차이 × 3) 으로 구했다 (A1382).
- **κ·면적 불변 검증 (Fig. 13 · Fig. 14)**: graphite-1 (ε 0.43 ± 0.02, d_coating 58 ± 2 µm), TBAClO₄ 10/50/200/700 mM (κ 0.46/1.74/5.22/9.56 mS/cm),
  T-cell 8개(농도당 2) + 파우치 4개 → **τ = 4.3 ± 0.6**.  이후 표준 전해질 = **10 mM** (r_El ≪ r_Ion 를 가장 잘 만족) 에서 τ = 4.2 ± 0.7 (A1382).
- 전극 τ 결정에는 **작지만 유한한 접촉저항이 영향을 주지 않는다** (분리막과 다른 점 — TLM 형상이 보이는 한 R_Ion 은 따로 읽힌다, A1381–A1382).

### 4-4. 측정 조건 일람

| 항목 | 값 | 쪽 |
|---|---|---|
| EIS (분리막) | 200 kHz – 1 kHz, 5 mV 섭동, OCV 근방 | A1377 |
| EIS (전극) | 200 kHz – 0.5 Hz, 10 mV 섭동 | A1377 |
| 포텐쇼스탯 | Biologic VMP3; 파우치는 4단자 연결 (접촉저항 회피) | A1377 |
| 온도 | 글러브박스 25 °C ± 1 °C (MBraun, O₂·H₂O < 0.1 ppm); T-cell 은 25 °C 항온조 | A1376–A1377 |
| 분리막 전해질 | LP572 (BASF): EC:EMC (3:7 w:w) + 1 M LiPF₆ + 2 % VC, κ = 9.25 mS/cm (Table II) | A1377 · A1379 |
| 전극 전해질 | TBAClO₄ in EC:DMC (1:1 w:w), 10/50/200/700 mM | A1376 · Fig. 13 |
| T-cell | Swagelok 대칭, 스프링 ≈1 bar, 전극 Ø 11 mm, 유리섬유 분리막 2장 (VWR, 250 µm, 붕규산, 바인더 없음, 기공 1.2 µm) | A1377 |
| 파우치 | 큰 전극 20×20 mm² / 분리막 30×40 mm² / 작은 전극 15×15 mm²; 전해질 ≈50–200 µL; 25 mbar 진공 밀봉; 활성 면적 = 이미지 분석 | A1377 |
| 전극 제조 | 닥터블레이드 (AM + Kynar HSV 900 + Super C65 + NMP, Thinky ARV-310), Cu 19 µm (음극) / Al 15 µm (양극), 50 °C 공기 건조 → Ø 11 mm 펀칭 → **유압 프레스 (Mauthe PE-011) 압축** → 진공 ≥95 °C ≥6 h | A1376 |
| 분리막 준비 | Ø ≥25 mm 펀칭, 70 °C 진공 하룻밤 | A1376 |

### 4-5. 오차 예산 (원문)
- 두께 절대오차 **±2 µm** → 20–50 µm 코팅에서 **4–10 %**; 무게 **±0.01 mg/cm²** (A1376).  → Fig. 15·19·20 의 가로 오차막대 (다공도).
- Fig. 15 세로 오차막대 = 두께 오차 (N_M 은 ε 와 무관하므로) (A1382).  Fig. 20 은 N_M × ε 이라 세로 오차가 커진다 (A1384–A1385).
- Fig. 14: T-cell 은 전해질당 2개의 SD, 파우치는 **고정 오차 0.3** (면적·κ·두께·다공도 편차의 가우스 전파로 추정).
- 분리막: Table II 전 항목 SD **< 8 %** (≥3 회 독립 반복); 층수 변화·셀 형식 변화 SD ~3 %, 전해질 변화 SD ~6 %.

### 4-6. 시뮬레이션 · 입자 처리
- **시뮬레이션 없음.**  DEM/MPM/FEM/RNM 어느 것도 쓰지 않는다 (Eq. 11 해석해와 맞춤만).
- **입자 처리 ★** = 실제 입자 (형상 그대로, 3D 재구성 없음).  SEM 으로 형상만 본다: 흑연 = **판상, 전류집전체와 수평 정렬** 10–30 µm;
  NMC = **구형** 10–30 µm; LNMO = 구형 경향 10–20 µm; LTO = 구/정육면체 1–2 µm; LFP = 1차 입자 <500 nm 의 **약한 응집체 4–20 µm** (압축 시 깨져 판상화);
  도전재 = 1차 ~40 nm 가 수백 nm 사슬로 융합 (A1383–A1384).  ⇒ "강체 구" 근사와 반대 극 — 형상 효과가 결과의 주인공이다.

### 4-7. 기법 미니 용어집

| 용어 | 뜻 (이 논문에서) |
|---|---|
| **MacMullin 수 N_M** | κ/κ_eff (Eq. 1).  ε 없이 잴 수 있음.  지질학의 formation factor 와 같은 꼴 |
| **effective tortuosity τ** | ε·N_M (Eq. 5).  모든 기하 효과를 묶은 실험량.  제곱 없음 |
| **Archie 지수 m** | N_M = ε^−m (Eq. 2).  m = 1 + α |
| **Bruggeman 지수 α** | τ = ε^−α (Eq. 6).  구형 0.5.  ⚠ 다른 문헌(Thorat)은 κ_eff = κ·ε^α 의 지수(구형 1.5)를 α 라 부른다 |
| **비례인자 f** | τ = f·ε^−α (Eq. 7).  ⚠ 우리 인계 계획의 f (= σ_eff/σ₀) 와 **이름만 같고 다른 양** |
| **constriction factor β** | N_M ≡ τ̄_geo/(εβ) (Eq. 4).  기하 경로 τ 에 가변 단면 보정 |
| **HFR** | 고주파 실축 절편.  분리막에서는 = R_Ion, 전극 셀에서는 = 분리막 저항 (+ 배선) |
| **차단 (blocking) 조건** | 고체/액체 계면에 전하이동이 없는 이상분극 상태.  계면 = CPE |
| **CPE** | Z = 1/(Q(iω)^γ).  γ < 1 = 표면 거칠기·불균일로 인한 비이상 용량 |
| **TLM (전송선 모델)** | 다공 전극의 이온·전자 레일 + 표면 임피던스 사다리 (de Levie 계열 — 이 이름은 원문에 없음).  이 논문 Eq. 11 의 해석해 출처 = Lasia [36] · Eikerling–Kornyshev [42] |
| **TLM-Q / TLM-C** | 표면 임피던스를 CPE (γ ≠ 1) / 이상 축전기 (γ = 1) 로 둔 TLM |
| **1/3 규칙 (Eq. 12)** | 저주파 가지 실축 절편 = R_HFR + R_Ion/3.  카드 보충 (원문 아님): Eq. 11 에서 x = √(R_Ion/Z_S) → 0 (저주파) 이면 coth x ≈ 1/x + x/3 이므로 Z_El ≈ Z_S + R_Ion/3 — 순수 용량성 Z_S 는 허수축 성분이라 실축 절편에 R_Ion/3 만 남는다 |
| **Gurley 수** | 공기 100 cm³ 통과 시간.  거친 비교용일 뿐 유효 이온저항과 정량 연결 불가 (A1374) |

---

## 5. ★ 보고 값

### 5-1. 분리막 — Table II (A1379; κ = 9.25 mS/cm LP572, 주로 1장, SD = ≥3회 반복)

| 분리막 | 종류 | ε [−] | d [µm] | τ (meas.) | N_M (meas.) | N_M(B) = ε^−1.5 | N_M(lit.) [원문 ref] | N_M ÷ N_M(B) (파생 = (τ/ε)/ε^−1.5) | τ_B = ε^−0.5 (파생) | Fig. 10 맞춤 무리 |
|---|---|---|---|---|---|---|---|---|---|---|
| commercial #1 | monolayer HDPE | 0.39 | 18.5 | 5.4 ± 0.4 | 14 ± 1.1 | 4.1 | — | 3.4 | 1.60 | α = 3.1 |
| commercial #2 | monolayer HDPE | 0.43 | 16 | 6.9 ± 0.1 | 16 ± 0.3 | 3.6 | — | **4.5** (최대) | 1.52 | α = 3.1 |
| Celgard H2013 | trilayer | 0.47 | 20 | 3.2 ± 0.2 | 6.9 ± 0.5 | 3.1 | — | 2.2 | 1.46 | α = 2.5 |
| Celgard 2320 | trilayer | 0.39 | 20 | 3.9 ± 0.0 | 10 ± 0.1 | 4.1 | 6.5* [23], 11* [44] | 2.4 | 1.60 | α = 2.5 |
| Celgard 2325 | trilayer | 0.39 | 25 | 4.1 ± 0.2 | 10 ± 0.6 | 4.1 | 7.0* [23] | 2.6 | 1.60 | α = 2.5 |
| Celgard 2500 | monolayer PP | 0.55 | 25 | 2.5 ± 0.2 | 4.5 ± 0.3 | 2.5 | 13* [14], 8.5 [2], 18* [22] | **1.8** (최소) | 1.35 | α = 2.5 |
| Celgard 3500 | coated PP | 0.55 | 25 | 3.4 ± 0.1 | 6.1 ± 0.2 | 2.5 | — | 2.5 | 1.35 | α = 3.1 |
| Celgard C480 | trilayer | 0.50 | 21.5 | 3.6 ± 0.3 | 7.3 ± 0.5 | 2.8 | — | 2.5 | 1.41 | α = 3.1 |
| Freudenberg FS-3001-30 | non-woven PET | 0.60 | 28 | 2.7 ± 0.0 | 4.6 ± 0.1 | 2.2 | 14 [43] | 2.1 | 1.29 | α = 3.1 |
| Separion S240P30 | non-woven PET | 0.46 ⚠ | 28.1 | 4.3 ± 0.2 ⚠ | 8.6 ± 0.3 | 2.8 ⚠ | — | 2.9 (ε 0.46 기준) | 1.47 | α = 3.1 |

- `*` = 원문 표 규약: *"separator parameters differing from the manufacturers' specification sheet are marked by an asterisk"* (Table II 캡션).
- 원문 요약: 최소 차이 Celgard 2500 **~1.8×**, 최대 **~4.5×** (A1379) — 위 파생 열과 일치.
- ⚠ **Separion 행 내부 불일치 (원문 표 그대로 옮김)**: ε = 0.46 이면 N_M(B) = 0.46^−1.5 = **3.2** 이고 τ/ε = 4.3/0.46 = **9.3** 이어야 하는데 표는 **2.8 · 8.6**
  (둘 다 ε ≈ 0.50 이면 맞는 값).  Fig. 10 에서는 Separion 이 ε 0.46 에 **τ ≈ 4.0 (판독)** 으로 찍혀 있고 4.0/0.46 = 8.7 ≈ N_M 8.6 과 맞는다.
  ⇒ 어느 칸이 오타인지 **[미확인: 정오표 미열람]**.  이 행의 숫자는 인용하지 않는다.
- **Fig. 10 맞춤 (A1380, f = 1 인 Eq. 6)**: H2013·2320·2325·2500 → **τ = ε^−2.5** (α 2.5 = Archie m 3.5); Freudenberg·Separion·상용 #1·#2·C480·3500 → **τ = ε^−3.1** (α 3.1 = m 4.1).
  두 무리의 차이 단서: Celgard 2500 과 3500 은 사양이 동일하고 3500 만 계면활성제 코팅 — 원인 규명엔 제조·형태·코팅 정보가 필요하다고만 적음.

### 5-2. 분리막 문헌값이 흩어진 이유 (A1379–A1380)

| 문헌 | 그 값 | 이 논문 값 | 원문이 지목한 원인 |
|---|---|---|---|
| Arora & Zhang [23] | Celgard 2320 ~6.5 · 2325 ~7.0 | 10 ± 0.1 · 10 ± 0.6 | (i) 측정 셀 기하의 **stray current** (셀 벽–분리막 사이 이온 우회) → 체계적으로 낮게 |
| Patel et al. [2] | Celgard 2500 8.5 | 4.5 ± 0.3 | (ii) 코인셀 **2단자 접촉저항** — Patel 은 0.35 Ω 을 빼는데, 기대 분리막 저항이 같은 자릿수 0.57 Ω |
| Djian et al. [14] | Celgard 2500 13 ± 1.5 | 4.5 ± 0.3 | 미세구조 차이 가능 — Djian 의 Celgard 2500 은 23 µm · 0.47, 이 논문 사양서는 25 µm · 0.55 |
| Abraham [22] | Celgard 2500 18 | 4.5 ± 0.3 | (iv) 전도도 셀의 **유효 면적 불확실** |
| Cannarella & Arnold [44] | Celgard 2320 11 | 10 ± 0.1 | (iii) **32장 적층** — 이방성 재료면 1장 측정과 다를 수 있음 |
| Freudenberg 사양서 [43] | 14 | 4.6 ± 0.1 | 사양서 옴저항이 3배 큰 N_M 에 해당 |

### 5-3. 전극 — Table I (A1377; LFP·LNMO·NMC 는 Al, LTO·흑연은 Cu 집전체; 적재량 = Fig. 15 전극들의 평균 ±10 %)

| 활물질 | 적재량 | AM 밀도 | wt% AM/binder/carbon | 이름 |
|---|---|---|---|---|
| LFP (commercial) | 8 mg_AM/cm² | 3.6 g/cm³ | 90/5/5 | LFP-lowC |
| LFP (commercial) | 3 mg_AM/cm² | 3.6 g/cm³ | 70/15/15 | LFP-highC |
| LNMO (commercial) | 7 mg_AM/cm² | 4.5 g/cm³ | 96/2/2 | LNMO |
| NMC 111 (commercial) | 18 mg_AM/cm² | 4.7 g/cm³ | 96/2/2 | NMC |
| LTO (commercial) | 9 mg_AM/cm² | 3.5 g/cm³ | 90/5/5 | LTO |
| graphite (SGL Carbon GmbH) | 6 mg_AM/cm² | 2.3 g/cm³ | 95/5/0 | graphite-1 |
| graphite (KS6L, Timcal) | 4 mg_AM/cm² | 2.3 g/cm³ | 91/9/0 | graphite-2 |

### 5-4. 방법 검증 — graphite-1 (A1380–A1382)

| 항목 | 값 | 조건 | 표지 |
|---|---|---|---|
| R_HFR (Fig. 11) | **6.35 Ω** (예측 6.1 Ω) | graphite-1 2장 (d 63.2 µm, ε 0.41, A 2.37 cm²), Celgard 2325 1장, 50 mM TBAClO₄ EC:DMC (1:1), κ 1.74 mS/cm | stated |
| 분리막 예측 검산 | N_M 10 × 25 µm ÷ (2.37 cm² × 1.74 mS/cm) = **6.06 Ω** | Table II 의 Celgard 2325 | 파생 (원문 6.1 Ω 과 일치) |
| R_Ion 두 전극 합 — 그래프법 (Eq. 12) | **31.6 Ω** | 위 | stated |
| R_Ion — TLM-Q 맞춤 (Eq. 11) | **31.0 Ω** | 위 | stated |
| R_Ion — TLM-C 맞춤 | **40.6 Ω** (>30 % 큼) | 위 | stated |
| ⇒ τ (Eq. 13) | **4.15** (TLM-Q) · 4.23 (그래프) · **5.43** (TLM-C) | d = 63.2 µm 를 *전극 1장 코팅 두께*로 읽음 | 파생 — TLM-Q 값이 graphite-1 평균 4.3 과 맞아 그 읽기가 정합적 |
| 전해질 κ | 10/50/200/700 mM → **0.46/1.74/5.22/9.56 mS/cm** | TBAClO₄ in EC:DMC (1:1 w:w) | stated (Fig. 13 범례) |
| 저주파 CPE 위상각 | 흑연 ~85°; 다른 활물질 88° (LTO) ~ 80° (LFP) | 활물질별로 체계적 → 전극 표면 형태 기인 | stated (A1382) |
| τ 평균 (Fig. 14) | **4.3 ± 0.6** | graphite-1, ε 0.43 ± 0.02, d_coating 58 ± 2 µm, T-cell 8 + 파우치 4 | stated |
| 10 mM 에서 τ | **4.2 ± 0.7** | 이후 전극 측정 표준 | stated |
| Bruggeman (ε 0.43) | τ = **1.5** — 측정이 ~3배 | | stated (파생 0.43^−0.5 = 1.52) |
| Fig. 14 개별점 | 파우치 ≈ 4.9/4.2/4.45/5.45, T-cell ≈ 3.8/4.05/4.3/4.9 @ κ 0.46/1.74/5.22/9.56 | | **판독** — 최고 κ 에서 높게 나오는 경향이 있으나 원문은 "reasonably good agreement" 로만 평가 |

### 5-5. 전극 N_M · τ @ ε ≈ 0.27–0.37 (Fig. 15, AM ≥ 90 wt%, 10 mM TBAClO₄)

| 전극 | 형상·입경 (A1383–A1384) | ε (판독) | N_M (본문 stated / 판독) | τ = ε·N_M (파생) | N_M(B) = ε^−1.5 (파생) | N_M ÷ N_M(B) (파생) |
|---|---|---|---|---|---|---|
| graphite-1 | 판상, 수평 정렬, 10–30 µm | ≈0.28 · 0.31 | **"18–19" @ ~29 %** / ≈18.2 · 18.6 | ≈5.1 · 5.7 | 6.7 · 5.9 | ≈2.7–3.2 |
| graphite-2 (KS6L) | (SEM 없음) | ≈0.35 · 0.36 | **"18–19" @ ~35 %** / ≈19.2 · 18.0 | ≈6.8 · 6.4 | 4.8 · 4.7 | ≈3.8–4.0 |
| NMC 111 | 구형, 10–30 µm | ≈0.34 | **"10–11"** (흑연보다 ~2배 낮음) / ≈11.0 · 10.1 | ≈3.8 · 3.5 | 5.0 | ≈2.0–2.2 ("two-fold", A1383) |
| LNMO | 구형 경향, 10–20 µm | ≈0.30 · 0.33 | **"~17"** / ≈16.1 · 17.4 | ≈4.8 · 5.7 | 6.2 · 5.3 | ≈2.6–3.3 |
| LTO | 구/정육면체, 1–2 µm | ≈0.30 · 0.31 | **"~8"** / ≈8.1 · 7.8 | ≈2.5 · 2.4 | 6.0 · 5.7 | ≈1.4 |
| LFP-lowC | 응집체 4–20 µm (1차 <500 nm) | ≈0.34 · 0.37 | (본문 수치 없음) / ≈20.4 · 15.0 | ≈7.0 · 5.6 | 5.0 · 4.4 | ≈3.4–4.1 |

- 원문 해석: ① **형상** — 판상 흑연이 수평 정렬해 관통 이온 전도를 막는다 → 구형 NMC 의 ~2배 (A1383).  FIB-SEM 기반 수치평가도 흑연 관통 τ 가 면내의 ~2배 [16].
  ② **입경** — LNMO (10–20 µm) ~17 vs LTO (1–2 µm) ~8: *"막힌 기공을 돌아가는 우회로가 큰 입자일수록 길다"* 는 **가설** (A1383–A1384).
- 3D 재구성 대비: 구형 NMC 의 재구성 기반 τ (Ebner [32]) 는 Bruggeman 에 매우 가깝지만 실측은 **2배** — 이미징 해상도가 도전재·바인더를 못 풀어 **빈 기공을 실제보다 많이 가정**했을 가능성 + 순수 기하 정의 차이 (A1383).

### 5-6. 다공도 스윕 — generalized Bruggeman 맞춤 (Fig. 19 · Fig. 20, A1384–A1385)

| 전극 | N_M 맞춤 (Fig. 19, stated) | τ 맞춤 (Fig. 20, stated) | f | α | 측정 ε 범위 (판독) | 본문 τ 변화 (stated) |
|---|---|---|---|---|---|---|
| graphite-1 (95/5/0) | **N_M = 4.7 ε^−1.1** | **τ = 4.7 ε^−0.1** | 4.7 | 0.1 | ≈0.28–0.65 | ~4.8 → ~5.2 (ε ~70 → 30 %); *"다공도 의존성 없음"* |
| LFP-lowC (90/5/5) | **N_M = 3.1 ε^−1.6** | **τ = 3.1 ε^−0.6** | 3.1 | 0.6 | ≈0.27–0.51 | **~4.5 (ε 50 %) → ~7 (30 %)** 급증 |
| LFP-highC (70/15/15) | **N_M = 3.0 ε^−1.2** | **τ = 3.0 ε^−0.2** | 3.0 | 0.2 | ≈0.27–0.71 | ~3.5 → ~4.2 (ε ~70 → 30 %) |
| Bruggeman (구) | N_M(B) = ε^−1.5 | τ = ε^−0.5 | 1 | 0.5 | — | — |

- ★ *"the experimental data of N_M or τ vs. ε could only be properly represented when a variable prefactor f was used … could not be represented by a generalized
  Bruggeman equation with the prefactor f = 1, contrary to what was reported in studies with 3D reconstructed electrodes"* (A1385).
- N_M 의 다공도 의존은 **대부분 기공 부피 감소(ε) 자체**이고 τ 는 약하게만 변한다 (그래서 N_M 지수 1.1–1.6 ≈ 1 + α).
- 기전 해석 (원문): 도전재는 경도가 높아 **비압축성 지지체**로 LFP 1차 응집체 사이를 벌려 이온 경로를 짧게 함; 높은 압축에서 LFP 응집체가 깨져 **판상화** →
  도전재가 적을수록 판이 넓어져 τ 급증 (LFP-lowC).  흑연은 수평 정렬 기공이 압축(집전체 수직)에도 그대로라 ε 감소는 **연한 흑연 입자 자체의 압축** (A1384–A1385).
- 3D 재구성 흑연 [32]: ε 0.4 에서 τ ~5.5 는 일치, ε 0.6 에서 τ 3 은 크게 다름 → 바인더·탄소 미해상 + 순수 기하 정의; *직접 비교는 조성·입경·형상이 같을 때만* (A1385).

### 5-7. 집전체–코팅 접촉저항 (Fig. 12, LFP-highC on Al, 10 mM TBAClO₄ κ 0.46 mS/cm, A1381)

| 압축 | ε | 고주파 반원 저항 | 반원 정점 주파수 |
|---|---|---|---|
| 50 MPa | 0.49 | ~40 Ω | ≈4 kHz |
| 150 MPa | 0.34 | ~20 Ω | ≈10 kHz |
| 400 MPa | 0.27 | 무시할 크기 | — |

- 귀속 근거: 반원은 **Al 집전체 전극에서만** 보였고 Cu (흑연·LTO) 에서는 한 번도 없음; LTO 고유 전자전도도 (10⁻¹³ S/cm [46]) 가 LFP (10⁻⁹ S/cm [47]) 보다
  낮은데도 Cu 위 LTO 에 반원이 없음; 반원 유효 용량 ~**1 µF** ÷ 이중층 ~10 µF/cm² = 유효 계면 ~**0.1 cm²** ≪ 전극 표면 ~**980 cm²**
  (2.58 mg_LFP/cm² × 24 m²/g BET + 0.58 mg_C/cm² × 62 m²/g) → **4 자릿수 작은 면적 = 집전체/코팅 계면**.  Gaberscek [48] 와 정합.
- **TLM 형상이 보이는 한 접촉저항(R_C/Q_DBL)이 직렬로 붙어도 R_Ion 은 여전히 결정 가능** (A1381).

### 5-8. LFP 문헌 대조 (Fig. 21, A1385–A1386)

| 출처 (원문 ref) | 재료·조성 | 방법 | N_M (stated) |
|---|---|---|---|
| 이 논문 | LFP-lowC 90/5/5 · LFP-highC 70/15/15 | EIS TLM-Q | Fig. 19 맞춤선 |
| Thorat et al. [18] | LFP 84/8/8, 감자형 300–600 nm | 분극-차단 확산 + Eq. 7 맞춤 | 곡선 (Bruggeman 보다 높음) |
| Cooper et al. [12] | LFP (조성 미상) | 싱크로트론 X선 단층촬영 + **열전달 시뮬레이션** | **6–10** |
| Ender et al. [34] | LFP 70/6/24, 감자형 200–600 nm | FIB-SEM 재구성 + **Laplace 해** | **~2.5** (랩 ~100 nm) · **~5** (상용, 2차 응집 ~1.2 µm) |
| Ebner & Wood [16] | LCO ~94/3/3, 비구형 10 µm | SEM 상·단면 → Bruggeman Estimator | 관통 **α = 0.83** (τ = ε^−0.83) 에서 N_M 계산 |
| Ebner et al. [32] | NMC 96/2/2, 구형 20 µm | 3D 재구성 기하 | ≈ Bruggeman |

- 범위: ε 60–70 % 에서 N_M **~3–7**, 상용 범위 ε ~30–35 % 에서 **~7–20**; Bruggeman 과의 차이 **~1.5–~3배**, 특히 저다공도 (A1385).
- 결론: 활물질 형태·도전재 함량 의존이 커서 **문헌 값과의 엄밀 비교는 불가능** (A1385–A1386).  LCO 의 도전재 3 wt% 는 이 논문 LFP-lowC 에서 ~2배 높은 N_M 에 해당 (A1386).

### 5-9. Bruggeman (α = 0.5) 대비 요약

| 대상 | 측정 ÷ Bruggeman | 표지 |
|---|---|---|
| 분리막 10종 (N_M) | **1.8 – 4.5×** | stated (A1379) |
| Celgard 2325 (τ, 5 전해질) | 1.6 ÷ 4.03 → Bruggeman 은 측정의 **40 %** | stated (A1379) |
| graphite-1 (τ, ε 0.43) | **~3×** (4.3 vs 1.5) | stated (A1382) |
| 전극 전반 (결론) | **~1.5 – 3×** | stated (A1386) |
| LFP 문헌 포함 (Fig. 21) | **~1.5 – ~3×** | stated (A1385) |
| graphite-2 · LFP-lowC @ ε 0.34–0.37 | ≈ **3.4 – 4.1×** | **판독 + 파생** — 요약 문장 범위 위쪽 |
| graphite-1 맞춤식 @ ε 0.5–0.7 | ≈ 3.6 – 4.1× | **파생** (Fig. 19 맞춤식 대입) — 고다공도에서는 Bruggeman 이 더 크게 어긋남 |

---

## 6. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | 분리막 차단 등가회로 = R_Ion + 묶인 CPE (Eq. 10) | 전자 부도체 매질의 R_Ion = HFR 하나로 끝난다 |
| 2 | 일반 TLM: 전자 레일 r_El (갈색) · 이온 레일 r_Ion (파랑) · 표면 z_S | ASSB 복합양극 TLM (Bazzoun·Minnmann) 의 원형; 두 레일 모두 필요한 경우를 기억 |
| 3 | 간이 TLM (r_El ≪ r_Ion · 차단) | 이 단순화가 성립하는 조건 = κ_el > 0.1 S/cm vs κ_ion < 0.01 S/cm — ASSB 에서 따로 확인 필요 (§9) |
| 4 | Eq. 11 모의 Nyquist (R_Ion 300 Ω, Q 100 µF·s^(γ−1), γ 1 · 0.9) + 45° 보조선 | TLM-C = 고주파 45°·저주파 수직, TLM-Q = 둘 다 눕는다 → 실측이 수직이 아니면 TLM-C 맞춤은 편향 |
| 5 | 절연 둘레 Cu 블록 셀 도면 (상부 Ø 20 mm, 하부 Ø 50 mm, 저장조 Ø 45 · 깊이 5 mm) | 측정 면적을 기하로 못박는 장치 — 면적 불확실이 문헌 N_M 산포의 주원인 |
| 6 | 대칭 파우치 셀 구성 (큰 전극 · 큰 분리막 · 작은 전극) | 활성 면적 = 작은 전극, 이미지 분석으로 측정 |
| 7 | 1–3장 분리막 HFR: (a) 비절연 = 큰 산포, (b) 절연 = 반복 동일 | **stray current 아티팩트**의 실증 — 우리 앵커 실험(EIS) 을 고를 때 셀 기하 확인 |
| 8 | 면저항 R·A vs 분리막 장수 — 직선, x₀ = 0.10 Ω·cm², R² 0.998 (Cu 블록 + 파우치) | ★ **두께(층수) 선형성 + 절편 ≈ 0** = 접촉·경계 기여를 벌크와 가르는 검사 — 우리 모델의 R·A ∝ d 검사로 그대로 옮길 수 있다 |
| 9 | Celgard 2325 τ vs κ (0.41–12.5 mS/cm, 5 전해질) — 평균 4.03, Bruggeman 1.6 | ★ **τ 는 κ 에 무관** = 순수 미세구조량.  우리 T 의 σ₀-불변성 검사 근거 (§11-③) |
| 10 | 분리막 τ vs ε + ε^−2.5 · ε^−3.1 · Bruggeman | 분리막은 f = 1 에 큰 α (2.5–3.1); Separion 점 τ ≈ 4.0 (판독) — Table II 불일치 판별 근거 |
| 11 | graphite-1 대칭 파우치 스펙트럼 + TLM-C·TLM-Q 맞춤 + 외삽선 (inset 고주파) | ★ TLM-C 가 R_Ion 을 **>30 % 과대** (40.6 vs 31.0 Ω) — 문헌 τ 를 앵커로 쓸 때 어떤 TLM 인지 확인 |
| 12 | LFP-highC (Al) 50/150/400 MPa 압축 후 스펙트럼 (HFR 뺀 것) — 고주파 반원 ~40 → ~20 Ω → 소멸 | 비삽입 염 차단이 접촉저항을 분리해 준다; 압축이 Al/코팅 접촉을 좋게 만든다 |
| 13 | graphite-1 대칭 파우치 4종 κ (0.46/1.74/5.22/9.56 mS/cm) 스펙트럼 + Eq. 11 맞춤 (5 kHz·50 Hz·5 Hz 표시) | 같은 전극에서 κ 만 바꿔 R_Ion ∝ 1/κ 확인 |
| 14 | graphite-1 τ vs κ — 파우치·T-cell, 평균 4.3 ± 0.6, Bruggeman (ε 42 %) | 전극에서도 τ 의 κ·면적 불변 (고 κ 에서 다소 높은 경향, 판독) |
| 15 | AM ≥90 % 전극 N_M @ ε 0.27–0.37: graphite 18–19 · LNMO ~17 · LFP-lowC · NMC 10–11 · LTO ~8 · Bruggeman | ★ 형상(판상 2×)·입경(큰 입자 ↑) 효과 — **구 DEM 이 표현 못 하는 축** |
| 16 | SEM 상면·단면: graphite-1 (ε ≈0.29) vs NMC (ε ≈0.34) + 입자 모식 | 판상 수평 정렬 vs 구형 — 형상 τ 의 시각 근거 |
| 17 | SEM: LNMO (ε ≈0.31) vs LTO (ε ≈0.30) | 입경 10–20 µm vs 1–2 µm |
| 18 | SEM: LFP-highC vs LFP-lowC (ε ≈0.27), inset 원료 분말 | 압축으로 깨진 LFP 응집체의 판상화 — 도전재 적을수록 넓은 판 |
| 19 | N_M vs ε (graphite-1 · LFP-lowC · LFP-highC) + 맞춤 4.7ε^−1.1 · 3.1ε^−1.6 · 3.0ε^−1.2 + Bruggeman | ★ f ≠ 1 이 필요하다는 직접 증거 |
| 20 | τ vs ε (같은 전극) + 맞춤 4.7ε^−0.1 · 3.1ε^−0.6 · 3.0ε^−0.2 + Bruggeman | τ 는 ε 에 약하게만 의존 (흑연 ≈ 상수), LFP-lowC 만 저 ε 에서 급증 |
| 21 | LFP N_M vs ε: 이 논문 vs Thorat · Cooper · Ender · Ebner&Wood (LCO) · Ebner (NMC) + Bruggeman | 이미지 기반 (Cooper 열전달 · Ender Laplace) 과 EIS 의 같은 축 비교 — 우리 복셀/망 T 와 실험 T 를 대조할 때의 선례 |

## 7. Post-processing ★
- **무엇**: 등가회로 맞춤 (Eq. 10 분리막 HFR · Eq. 11 TLM-Q 전극), 그래프법 (Eq. 12, ×3), N_M·τ 환산 (Eq. 8 · 13), 다공도 = 질량 수지,
  generalized Bruggeman 맞춤 (Eq. 6 with f = 1 for 분리막, Eq. 7 with free f 전극), 반원 정점 주파수·저항 → 유효 용량 → 유효 계면 면적 추정 (Fig. 12).
- **수치화 방식**: 분리막 = 표 (Table II: τ, N_M, N_M(B), 문헌값); 전극 = 그림 (N_M vs ε, τ vs ε) + 맞춤식 계수 (f, α) 를 캡션에 명시.
  N_M 그림의 세로 오차 = 두께, 가로 오차 = 다공도; τ 그림은 N_M × ε 이라 오차 증폭.
- **도구**: 맞춤 소프트웨어 이름은 원문에 없음 (n/a).  전도도 센서 SI Analytics LF 1100+ (맞춤 연마 유리 피팅, 온도센서 내장).
- **검증 설계 (재현성)**: 분리막 = 층수 1–3 · 셀 형식 2 (Cu 블록 · 파우치) · 전해질 5종; 전극 = κ 4종 · 셀 형식 2 (T-cell · 파우치, 면적 크게 다름).

---

## 8. ★ § tortuosity 정의 대조표 (이번 묶음의 목적)

### 8-1. 대조표 — 원문 기호 ↔ 우리 양

| 원문 기호 | 원문 정의식 (식·쪽) | 원문 이름 | 정규화 | 우리 쪽에서 같은 양 | 환산식 · 비고 |
|---|---|---|---|---|---|
| **N_M** | `N_M = κ/κ_eff` (Eq. 1, A1373); `= R_Ion·A·κ/d` (Eq. 8, A1375) | MacMullin number | A = 전체 기하 단면, d = 전체 두께; **ε 불필요** | **1/f** (f = σ_eff/σ₀).  망 출력 `sigma_full` (= σ_eff/σ_bulk) 의 역수 | `N_M = 1/f = σ_grain / sigma_full_mScm` |
| **τ** | `N_M = τ/ε` (Eq. 5, A1374) ⇒ `τ = ε·N_M`; 측정 `τ = R_Ion·A·κ·ε/d` (Eq. 8), 대칭셀 `/(2d)` (Eq. 13, A1382) | (effective) tortuosity | 위 + ε (총 부피 기준) | ★ **T = φ_SE·σ₀/σ_eff** = COMSOL **τ_F** = TauFactor τ (카드 `taufactor_tortuosity_factor_tomography_tool`) = Minnmann **τ_i²** = Tjaden **κ (= τ²)** | `τ_Landesfeind = T = (τ_Lap,eff)²` — 웹앱 값의 **제곱** |
| "τ" (τ² 관례) | *"τ in Eq. 5 appears often as τ²"* (A1374) → `N_M = τ²/ε` | — | 같음 | ★ **√T** = 웹앱 **τ_Lap,eff** = 인계 열 τ = Minnmann τ_ion (2.07) = Tjaden τ | `√T = √(τ_Landesfeind)` |
| **ε** | 다공도 = 전해질상 부피분율; 면적 무게 + 두께 + 벌크밀도 (A1376) | porosity | 총 부피 기준 · 막힌 기공 포함 | **φ_SE** (전도상 부피분율 — ⚠ 전고체에선 기공이 아니라 SE).  망 코드 `phi_se = Σ(SE 구 부피) / (box_x·box_y·plate_z)`, **전 SE** (퍼콜레이션 여부 무관, 구-합 = 질량보존 계열) | ε → φ_SE.  union 부피로 바꾸면 렌즈 겹침만큼 T 가 선형으로 달라진다 |
| **κ** | 전해질 용액 벌크 전도도, 센서 25 °C | electrolyte conductivity | 미세구조 없음 | **σ₀ = σ_grain** (3.0 mS/cm — 우리 원장 CL-91: Cronau 2021 SI Fig. S2c 펠릿 평탄값 하단) | ⚠ 펠릿 σ 는 펠릿 미세구조를 포함 (§9 ②) |
| **κ_eff** | 다공체 유효 전도도 | effective ionic conductivity | 전체 단면 | **σ_full** (FULL = bulk + Holm 협착) 또는 **σ_bulk_net** (CONTACT_FREE = 협착 0) | 같은 정규화: 망 `σ/σ_bulk = G_eff·plate_z/(box_x·box_y)` (`network_conductivity.py`) |
| **m** | `N_M = ε^−m` (Eq. 2, A1373) | Archie's exponent | — | `f = φ^m` 의 지수 | **m = 1 + α**; 구 m = 1.5 = Thorat 의 α = COMSOL Bruggeman "1.5" |
| **α** | `τ = ε^(1−m) = ε^−α` (Eq. 6, A1374) | Bruggeman exponent | — | `T = φ^−α` | 구 α = 0.5.  ⚠ **√T 관례로 맞추면 지수는 α/2** (구 0.25) |
| **f** (Eq. 7) | `τ = f·ε^−α` (A1374) | proportionality factor | — | ⚠ **우리 f (= σ_eff/σ₀) 와 다른 양 — 이름 충돌** | 이 논문 f = T·φ^α 의 전인자 (전극 3.0–4.7) |
| **N_M(B)** | `N_M(B) = ε^(−1−α)`, α = 0.5 → `ε^−1.5` (Table II 캡션, A1379) | Bruggeman prediction (spheres) | — | 망 코드 `sigma_bruggeman = phi_se ** 1.5` (σ/σ_bulk) | **N_M / N_M(B) = `R_bruggeman_over_full`** (= φ^1.5/f).  ⚠ `R_brug_over_full` 은 **CONTACT_FREE/FULL** 로 다른 양 (원장 L2-07) |
| **τ_path** | `τ_path = d_path/d` (Eq. 3, A1373) — 단면 일정 단일 채널 | path-length tortuosity | — | 벽 τ · τ_Dijkstra 계열 (경로 길이 비) | **Eq. 5 의 τ 아님** |
| **τ_geo, τ̄_geo** | 최단 연결 길이 ÷ 직선 길이; 그 평균 (A1373–A1374) | geometrical tortuosity | — | **τ_Dijkstra · τ_Dij,all · 벽 τ** (Dijkstra 최단경로) | Holzer: τ 와 **엄격 구분** (A1374) |
| **β** | `N_M ≡ τ̄_geo/(ε·β)` (Eq. 4, A1374; 인쇄형 τ̄_geo 1승) | constriction factor | — | 직접 대응 없음 (우리 협착 = 접촉별 Holm 저항이지 β 가 아님) | 인쇄형대로면 `β = τ̄_geo/T = τ_Dij / τ_Lap,eff²`.  τ_geo² 꼴이면 `β = τ_Dij²/τ_Lap,eff²` — **[미확인: Wiedenmann 원식의 지수]** |
| **τ_el** | 전위 구배 기반 경로 길이 (A1373, 식 없음) | electronic / physically motivated tortuosity | — | 대응 없음 (전류선 길이 τ 는 우리 출력에 없다) | n/a |
| COMSOL **τ_F**, **f_e** | (이 논문 A1374: COMSOL 은 Bruggeman 을 `ε/τ = ε^1.5` 로 표현) · COMSOL 5.6 Eq. 6-6 `f_e = ε_p/τ_F`, Bruggeman `τ_F = ε_p^(−1/2)` (메인 제공) | — | — | τ_F = **T**; f_e = **f** = 1/N_M | τ_F 칸에 √T 를 넣으면 σ_eff 가 √T 배 과대 |

### 8-2. 같은 N_M 을 다른 관례로 쓰는 문헌 (교차 확인, 원문 확인분만)

| 문헌 | 원문 식 (쪽) | 그 문헌의 "τ" | 이 논문 τ 와의 관계 |
|---|---|---|---|
| **Tjaden 2018 리뷰** (같은 inbox #2) | Eq. (2) `κ = τ²`, Eq. (3) `D_eff = (ε/κ)·D_bulk = (ε/τ²)·D_bulk`, Eq. (5) `N_M = σ_bulk/σ_eff = τ²/ε` — PDF 2–3쪽 (Eq. 5 의 N_M 문장에서 이 논문을 [24] 로 인용) | τ = √κ (기하 쪽), κ = tortuosity factor | **이 논문 τ = Tjaden κ = Tjaden τ²** |
| **Minnmann 2021 JES** (카드 `minnmann2021_jes_charge_transport_bottlenecks`) | Eq. 4 (PDF 5쪽): ⚠ **인쇄형 `τ_i² = (σ_i,eff/σ_i,0)·φ_i` — 역수가 빠져 있다** (그대로면 τ² < 1).  보고값 τ_ion² = 4.3 (42 vol% NCM) 은 `τ_i² = φ_i·σ_i,0/σ_i,eff` 를 따른다.  이 논문을 ref 42 로 인용 | τ_i² = tortuosity factor | **이 논문 τ = Minnmann τ_i²** (= T); Minnmann τ_ion 2.07 = √T |
| **TauFactor (Cooper 2016)** (카드 `taufactor_tortuosity_factor_tomography_tool`) | `D_eff = D·ε/τ` (그 카드 Eq. 1) | τ = tortuosity factor | **같은 양** (= T) |
| **Thorat 2009** [18] (이 논문 A1374 에서 재인용) | `τ = ε^(1−α)` | α = κ_eff ∝ ε^α 의 지수 | α_Thorat = 1 + α_Landesfeind = m |

### 8-3. 환산 사슬 (한 줄로)
```
f  = σ_eff/σ₀ = 1/N_M                                   (Eq. 1)       = COMSOL f_e
T  = φ/f = φ·N_M = τ_Landesfeind (Eq. 5·8·13)            = COMSOL τ_F = TauFactor τ = Tjaden κ = Minnmann τ_i²
√T = τ (τ² 관례)                                          = 웹앱 τ_Lap,eff = 인계 열 τ = Tjaden τ = Minnmann τ_ion
구형 Bruggeman:  f = φ^1.5  ⇔  N_M = φ^−1.5  ⇔  T = φ^−0.5  ⇔  √T = φ^−0.25      (α = 0.5, m = 1.5)
예 (파생): φ = 0.30 → f 0.164 · N_M 6.09 · T 1.83 · √T 1.35
```

### 8-4. 판정 — 이 논문 τ 는 COMSOL τ_F · 우리 T 와 같은 양인가?
1. **이 논문 τ = COMSOL τ_F = 우리 T — 같은 양이다.**  정의식이 같고 (`T = ε·κ/κ_eff`), 정규화도 같다 (A = 전체 기하 단면 · d = 전체 두께 · ε = 총 부피 기준 ·
   관통 방향).  우리 망은 `σ/σ_bulk = G_eff·plate_z/(box_x·box_y)` 로 Eq. 8 과 같은 정규화를 쓴다.  단서: ε → **φ_SE**, κ → **솔브에 쓴 바로 그 σ₀**, 관통 방향 — 전고체 조건은 §9.
2. **웹앱 τ_Lap,eff · 인계 열 τ (= √T) 는 이 논문 τ 의 제곱근이다.**  이 논문·Minnmann·TauFactor·COMSOL 값과 비교하거나 넘길 때는 **제곱(T)** 을 쓴다.
3. **τ_Dijkstra · τ_Dij,all · 벽 τ 는 이 논문의 τ_geo/τ_path** 이다 — Eq. 5 의 τ 와 **다른 정의**라 서로 대입하지 않는다.  둘을 잇는 것은 β (Eq. 4) 인데 그 식의 지수가 미확인이다.
4. **τ_Lap,geom (σ_bulk_net = CONTACT_FREE) 의 "geom" 은 이 논문 τ_geo 가 아니다** — 정의식은 Eq. 5 계열(√ 관례)이고, 협착을 뺀 망의 √T 다.  이름 충돌 주의.

### 8-5. 수치 감각
- graphite-1 τ = 4.3 (= T) → √ 관례 **2.07**; Celgard 2325 τ 4.1 → **2.02**; Bruggeman @ ε 0.43 τ 1.52 → √ **1.23** (파생).
- ⚠ 우연의 일치 주의: Minnmann 의 ASSB τ_ion² = **4.3** (42 vol% NCM) 과 이 논문 graphite-1 τ = **4.3** 은 **같은 관례(T)의 서로 무관한 두 값**이다.

### 8-6. 우리 리포의 표기 상태 (관찰 — `claude/stoic-knuth-NObVQ` 작업 트리, 2026-10-02, HEAD `1afd37a9a`; 이 카드에서 코드를 고치지 않았다)
- **선형 관례(T)를 명시한 곳** — 이 논문 A1374 와 정합: `scripts/comsol_export.py` §2 *"τ 관례 — 선형 (√ 함정 주의)"* (σ_eff = σ_bulk·φ/τ);
  `scripts/step3_sigma.py` `tau_from_solve()` docstring (*"COMSOL 의 tortuosity 입력은 통상 선형(σ_eff = σ·ε/τ)"*).
- **√T 를 "COMSOL/EIS input" 으로 표기한 곳**: `webapp/app.py` (τ_Lap_eff 행 라벨 · 주석 — 1947 · 2050–2051 · 2140–2141 · 2606 · 2615 · 2623 · 2740 · 2757 · 9544행),
  `scripts/export_comsol_2d.py:72 · 105` (+ 그 README 문구 *"σ_eff = σ_grain / (φ·tau_eff²)"* — 정의 τ_eff² = φσ_grain/σ_full 이면 σ_eff = σ_grain·φ/τ_eff² 라 **φ 위치도 반대**),
  `scripts/grade_engine.py:925`, `scripts/lhs_design_dataset.py:884 · 3192 · 3222`, `scripts/plot_section7_design_rules.py:106`.
- 같은 파일의 툴팁 `__tau_lap_bulk` (app.py 9545행) 는 τ_Lap,bulk (= τ_Lap,geom, CONTACT_FREE) 를 *"좁아짐 효과를 빼고 길이 순수하게 얼마나 돌아가는지"* 로 설명한다 —
  이 논문 기준으로는 그 양이 τ_path/τ_geo (경로 길이) 가 아니라 **협착 없는 망의 Eq. 5 계열 양** (가변 단면 효과는 남아 있음) 이다.
- ⇒ 이 논문 (EIS τ = Eq. 13) 과 COMSOL (A1374 + Eq. 6-6) 기준으로는 **"COMSOL/EIS input" 에 해당하는 양은 τ_Lap,eff² (= T)** 이다.
  √T 를 COMSOL τ_F 칸에 넣으면 f_e = ε/√T 가 되어 σ_eff 가 **√T 배 (T ≈ 4 면 약 2배) 과대**.  어느 쪽으로 정리할지는 저자 결정 (코드 → 웹앱 순차 규칙).

---

## 9. ★ 액체 LIB 관례 → 전고체 (SE = 전도상, σ₀ = SE 펠릿 전도도) 로 옮길 때

| # | 축 | 액체 LIB (이 논문) | 전고체 | 같은 양이 되는 조건 | 우리 코드 상태 |
|---|---|---|---|---|---|
| ① | 전도상 부피분율 ε | 기공 = 전해질 (막힌 기공도 ε 에 포함) | **φ_SE** — 기공은 AM 처럼 절연상 | ε → φ_SE, **총** SE 부피분율 (퍼콜레이션 SE 만이 아님) | 망 `phi_se` = 전 SE 구-합/상자 ✓ (union 으로 바꾸면 렌즈 겹침만큼 T 선형 변화) |
| ② | σ₀ (κ) | 독립 측정한 **벌크 용액** — 미세구조 없음 | **SE 펠릿 σ** — 펠릿 자신의 입자 접촉·입계·잔류 기공을 포함 | T 는 "**펠릿 대비**" 상대량이 된다.  모델과 실험이 **같은 σ₀ 기준**이어야 하고, 모델이 순수-SE 수준 접촉 효과를 다시 더하면 안 된다 | σ_grain 3.0 = 펠릿 평탄값 (원장 CL-91).  접촉망은 SE–SE 마다 Holm 협착을 더하므로 펠릿 σ 에 이미 든 접촉 효과와 **부분 이중계상** 가능 (방향 T↑, 크기 미상) |
| ③ | 전도상 내부 계면 | **없음** (액체 연속체).  τ 는 기하 효과만 (가변 단면·표면 형상, A1374) | SE–SE **입자 접촉 협착 + 입계** | 이 성분이 0 이어야 "액체와 같은 기하 τ".  있으면 T 는 기하 + 접촉을 묶은 양 | FULL (σ_full → τ_Lap,eff²) = 접촉 포함; CONTACT_FREE (σ_bulk_net → τ_Lap,geom²) 가 액체 쪽에 더 가깝다 (그래도 망 이산화).  Minnmann 도 Eq. 4 가 *"current constriction, CEI, interface polarization, space charge"* 를 무시한다고 명시 (PDF 5쪽) |
| ④ | σ₀ 불변성 | **실측 확인** (Fig. 9: 0.41–12.5, Fig. 14: 0.46–9.56 mS/cm) | 모든 저항이 1/σ₀ 로 비례하면 T 는 σ₀ 무관 | σ₀ 에 비례하지 않는 항 (면저항 Ω·cm² 꼴 계면저항 등) 이 없어야 | 망: bulk·Holm 모두 ∝ 1/σ ✓.  STEP3 계면저항 r_int (10-02 기구, 기본 OFF) 을 켜면 T 가 σ₀ 의존 → 더는 이 논문의 τ 가 아님.  웹앱 τ 식의 σ_grain ≠ 솔브 σ_grain (온도 등) 이면 T 가 그 비만큼 틀림 (app.py S-8 경고) |
| ⑤ | 정규화 | A 전체 기하 단면 · d 전체 두께 · 관통 방향 | 같음 | — | ✓ `G_eff·plate_z/(box_x·box_y)`, z 관통 |
| ⑥ | 추출 방식 | 교류 EIS, 차단 TLM 의 **균일 이온 레일** Σr_Ion | 계산 = 직류 Dirichlet 두 면 | 깊이 방향으로 균일한 전극이면 같은 R_Ion.  불균일(구배) 전극에서 TLM-균일 가정과 DC 관통 저항이 같은지는 **이 논문이 다루지 않음 [미확인]** | — |
| ⑦ | 간이 TLM 조건 | r_El ≪ r_Ion (κ_el > 0.1 S/cm vs κ_ion < 0.01 S/cm, A1376) + 차단 | ASSB 복합양극의 전자 σ_eff 는 조성에 따라 크게 변한다 (Minnmann τ_el² = 120 @ 25 vol% NCM) | 실험 앵커 (Bazzoun · Minnmann) 가 어떤 TLM·차단 방식을 썼는지 확인 후 사용 | 우리 계산은 이온만 직접 풀므로 해당 없음 |
| ⑧ | CPE 대 이상 축전기 | TLM-C 가 R_Ion **>30 % 과대** (Fig. 11) | ASSB TLM 도 CPE 지수가 1 에서 멀다 (카드 `bazzoun2026_dem_fem_rnm_ionic` Table S1: α 0.67–0.74) | TLM-C 계열 값은 T 과대 → 앵커로 쓰지 않는다 | — |
| ⑨ | 입자 형상 | 실제 형상 — 판상 흑연 N_M ≈ 2× 구형 NMC | 구 DEM — 형상 없음 | 형상·이방성 효과는 우리 T 에 **없다** | 구 근사는 NMC 같은 구형 쪽 |
| ⑩ | 바인더·도전재 | CBD 가 기공을 막음 (LFP-lowC vs highC; 이미지 기반 τ 가 낮게 나오는 이유로 지목) | 바인더·탄소가 SE 경로를 막음 | 모델에 CBD 차단이 있어야 | DEM 망엔 없음 → T **과소** 방향.  STEP3 는 PTFE centerline 스탬프로 일부 반영 (원장 CL-60) |
| ⑪ | 온도 | 25 ± 1 °C | — | σ₀ 와 σ_eff 같은 온도 | — |
| ⑫ | 압축 이력 | 전극을 **50–400 MPa** 로 유압 압축 후 액체 주입 | 300–400 MPa 냉간 압축 | 압력 범위는 겹치지만 기공-액체 망 ≠ SE 고체 망 | **수치 전이 불가** (LFP-highC 50/150/400 MPa → ε 0.49/0.34/0.27 은 액체 전극 데이터) |

**요약**: 정의식·정규화는 그대로 옮겨진다 (T = φ_SE·σ₀/σ_eff).  달라지는 것은 **σ₀ 의 성격(②)** 과 **전도상 내부 계면(③)** 이고, 이 둘 때문에
전고체 T 는 "기하 인자" 가 아니라 **펠릿 대비 기하 + 접촉 묶음**이다.  ④ 의 σ₀ 불변성은 우리 망에서 정확히 성립하므로 **검사로 쓸 수 있다** (§11-③).

---

## 10. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 전도상 | 액체 전해질 (연속체, 모든 기공 적심) | SE 입자 (DEM 구 · 접촉망) / STEP3 복셀 | **다름** — 우리만 SE–SE 접촉 협착이 있다 (§9 ③) |
| τ 정의 | τ = ε·N_M (제곱 없음) | T = φσ₀/σ_eff 는 같음; 웹앱은 √T 저장 | **정의 같음, 저장 관례 다름** (§8) |
| 정규화 | 전체 A · 전체 d · 관통 | 전체 box_x·box_y · plate_z · z | **같음** ✓ |
| σ₀ | 벌크 용액 κ | σ_grain = SE 펠릿 평탄값 | **성격 다름** (§9 ②) |
| ε 회계 | 질량 수지 (무게·두께·밀도) | 구 부피 합 / 상자 | **같은 계열** (질량 보존) — union 과는 다름 |
| Bruggeman 기준 | N_M(B) = ε^−1.5 | 망 `sigma_bruggeman = φ^1.5` | **같음** ✓ → `R_bruggeman_over_full` = N_M/N_M(B) 같은 축 |
| Bruggeman 대비 크기 | 분리막 1.8–4.5×, 전극 ~1.5–3× | 우리 코퍼스 `R_bruggeman_over_full` 값은 **이 카드에서 미확인** | 비교 가능한 축이 있다는 것만 확인 |
| 입자 처리 | 실제 형상 (판상·응집체·구) | 강체 구 + 연화 E (형상 없음) | **다름** — 형상 효과 (판상 2×) 는 우리 T 에 없다 |
| CBD | 있음 (기공 차단) | DEM 망 없음 / STEP3 PTFE 일부 | **다름** — 우리 T 과소 방향 |
| 방법 | EIS (실험) | Kirchhoff 망 (DEM) · 복셀 FV (STEP3) | 이 논문 = 우리 T 의 **실험 정의**; 값 대조 상대는 전고체 EIS (Bazzoun · Minnmann) |

- **frame [5]**: 이 논문은 **수송 절반만** 가진 측정 논문이다 (전도상 τ).  기계·형상 변화·압밀 물리는 없다.  우리 쪽에서는 DEM 접촉망 T 와 STEP3 복셀 T (CONTACT_FREE 가지) **둘 다** 이 정의로 읽힌다.
- **frame [4]**: 이 논문 수치로 우리 모델을 맞추지 않는다 (액체 LIB).  쓰는 것은 ① 정의·정규화, ② 측정 아티팩트 목록, ③ Bruggeman 편차의 크기 감각뿐.

## 11. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **인계·COMSOL 열은 T 로 넘긴다.**  f · T · √T 세 열을 둘 때 이름을 **원문 근거와 함께** 붙인다: `f = σ_eff/σ₀ = 1/N_M` (Eq. 1),
  `T = φ/f = τ_Landesfeind = τ_F(COMSOL)` (Eq. 5 · A1374), `√T = τ (τ² 관례)`.  웹앱의 "COMSOL/EIS input = τ_Lap,eff (√T)" 표기는 이 논문 기준으로 **제곱이 빠진 상태**다 (§8-6).
- ② ★ **Bruggeman 지수는 관례를 같이 적는다.**  같은 구형 Bruggeman 이 α = 0.5 (τ = ε^−α) · m = 1.5 (N_M = ε^−m, COMSOL·Thorat) · √T 관례 0.25 로 세 번 쓰인다.
  우리 T 를 φ 에 맞출 때 √T 로 맞추면 **지수가 반**이 된다.
- ③ ★ **σ₀ 불변성 자기검사** (Fig. 9 · Fig. 14 의 계산판): 같은 침대를 σ_grain 두 값으로 풀어 T 가 **비트 수준으로 같아야** 한다 (망의 모든 저항 ∝ 1/σ).
  다르면 σ₀ 에 비례하지 않는 항이 켜져 있거나 (STEP3 r_int), τ 식의 σ_grain 과 솔브 σ_grain 이 어긋난 것이다.
- ④ **두께 선형성 검사** (Fig. 8 의 계산판): 같은 조성에서 두께만 바꿔 R·A ∝ d (절편 ≈ 0) 인지 본다 → 절편 = 경계·접촉 기여, 기울기 = 벌크 T.  얇은 코너 (1 mAh) 에서 특히 의미.
- ⑤ **실험 앵커는 TLM-Q 계열만.**  ASSB EIS 값을 T 앵커로 쓸 때 이상 축전기 TLM 맞춤이면 R_Ion 이 >30 % 과대 (이 논문 실측) → T 과대.  Bazzoun 은 CPE (Z-type TLM) 라 이 기준을 통과한다.
- ⑥ **`R_bruggeman_over_full` = 이 논문의 N_M/N_M(B)** — 코퍼스에서 이 값을 꺼내면 "Bruggeman 대비 몇 배" 를 이 논문 (분리막 1.8–4.5, 전극 1.5–3) 과 **같은 축**에서 말할 수 있다.
  ⚠ `R_brug_over_full` (= CF/FULL) 과 섞지 않는다 (원장 L2-07).
- ⑦ **"f = 1 Bruggeman 은 안 맞는다" 는 우리 결과와 같은 방향** — 이 논문 전극은 f 3.0–4.7 이 필요했고, 우리 σ_thermal 에서도 2상 Bruggeman EMT 가 실패했다.
  (같은 물리라는 주장은 아니다 — 둘 다 "단일 멱법칙 Bruggeman 으로는 부족" 이라는 관찰만 공유.)

## 12. 인용 가능 문장 (deck/paper용)
- "Following Landesfeind et al. (J. Electrochem. Soc. 163, A1373, 2016; Eqs. 1, 5 and 8), we report the MacMullin number N_M = σ₀/σ_eff and the tortuosity τ = ε·N_M without a square; this τ is the quantity entered as τ_F in COMSOL's f = ε/τ_F, whereas values written in the τ² convention (N_M = τ²/ε) are its square root."
- "Impedance-derived tortuosities of liquid-electrolyte separators and electrodes exceed the Bruggeman estimate for spheres (τ = ε^−0.5) by factors of about 1.8–4.5 and 1.5–3, respectively, and electrode data could only be fitted with a prefactor f > 1 in τ = f·ε^−α (Landesfeind et al., 2016)."
- "Because an ideal-capacitor transmission-line fit overestimated the pore ionic resistance by more than 30 % relative to a constant-phase-element fit in the same spectrum (Landesfeind et al., 2016), only CPE-based TLM values are used as experimental tortuosity anchors."

## 13. 주의/한계 (over-claim 방지)
- ⚠ **액체 전해질 LIB** (LP572 · TBAClO₄/EC:DMC, PVDF + Super C65 전극).  LPSCl 전고체 수치로 **전이 불가** — 쓰는 것은 정의·정규화·측정 교훈뿐 (§9).
- ⚠ **[미확인: 정오표 미열람]** — 수치는 원문 그대로; 정오표 반영 여부 미상.  **Separion 행** (Table II) 은 내부 불일치 — 인용 금지 (§5-1).
- ⚠ 분리막 ε · d 는 **제조사 사양값** (d 는 자체 측정과 일치 확인, ε 는 아님) → 분리막 τ 는 사양 ε 에 의존 (N_M 은 무관).
- ⚠ **Eq. 4 는 τ̄_geo 1승으로 인쇄** — 원 출처 지수 [미확인].  β 를 우리 τ_Dij 와 T 로 계산하는 식은 그 지수에 따라 갈린다.
- ⚠ **Eq. 12 의 "ω_low → ∞"** 는 원문 표기 그대로 (뜻 = 저주파 가지의 실축 외삽).
- ⚠ 요약 "전극 ~1.5–3×" 보다 **판독상 큰 값**이 있다 (graphite-2 · LFP-lowC ≈3.4–4.1×, 흑연 맞춤식 고다공도 3.6–4.1×) — 판독·파생값이라 TREND 로만 쓴다.
- ⚠ 입경 효과 (LNMO vs LTO) 의 기전 (*막힌 기공 우회*) 은 원문이 **가설**로 적음.  3D 재구성이 τ 를 낮게 주는 이유 (CBD 미해상) 도 정량되지 않은 추론.
- ⚠ Fig. 12 집전체 접촉저항 귀속은 **유효 용량 → 면적 추정**에 의한 간접 추론 (직접 측정 아님).
- ⚠ 사소한 원문 불일치: Fig. 12 캡션 *"one glass fiber separator"* ↔ 본문 (A1381) *"two glass fiber separators"* · T-cell 기술 (A1377) 2장;
  graphite-1 ε 표기 0.42 ± 0.02 (Fig. 13 캡션) ↔ 0.43 ± 0.02 (Fig. 14 캡션·본문) ↔ Fig. 14 범례 "ε = 42 %".
- ⚠ 맞춤 소프트웨어·맞춤 주파수 창 등 맞춤 세부는 원문에 없음 (n/a).
- ⚠ 이 카드 §8-6 은 **우리 리포의 관찰**이지 논문 내용이 아니다 (날짜·커밋 명시).

## 14. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 원문 ref | 목록 서지 (그대로) | 왜 볼 만한가 |
|---|---|---|
| [6] | L. Holzer, D. Wiedenmann, B. Münch, L. Keller, M. Prestat, P. Gasser, I. Robertson, and B. Grobéty, J. Mater. Sci., 48, 2934 (2013). | effective τ ↔ 기하 τ_geo 엄격 구분 + constriction 의 원 출처 → 우리 τ_Dij 와 T 를 잇는 식을 확정 |
| [10] | D. Wiedenmann, L. Keller, L. Holzer, J. Stojadinović, B. Münch, L. Suarez, B. Fumey, H. Hagendorfer, R. Brönnimann, P. Modregger, M. Gorbar, U. F. Vogt, A. Züttel, F. La Mantia, R. Wepf, and B. Grobéty, AIChE J., 59, 1446 (2013). | Eq. 4 (N_M ≡ τ̄_geo/(εβ)) 원식 — **τ_geo 지수(제곱 여부) 확인**이 §8 의 남은 [미확인] |
| [13] | M. B. Clennell, Geol. Soc. London, Spec. Publ., 122, 299 (1997). | τ vs τ² 관례가 갈린 "다른 가정" 의 원 논의 |
| [14] | D. Djian, F. Alloin, S. Martinet, H. Lignier, and J. Y. Sanchez, J. Power Sources, 172, 416 (2007). | 같은 τ² 관례 논의 + 분리막 N_M 측정 (Celgard 2500 13) |
| [18] | I. V. Thorat, D. E. Stephenson, N. A. Zacharias, K. Zaghib, J. N. Harb, and D. R. Wheeler, J. Power Sources, 188, 592 (2009). | τ = ε^(1−α) 관례 (α 의 다른 뜻) + f·ε^−α 꼴의 출처, 분극-차단 확산법 |
| [12] | S. J. Cooper, D. S. Eastwood, J. Gelb, G. Damblanc, D. J. L. Brett, R. S. Bradley, P. J. Withers, P. D. Lee, P. D. A., J. Marquis, N. P. Brandon, and P. R. Shearing, J. Power Sources, 247, 1033 (2014). | 단층촬영 LFP 에서 열전달 계산으로 N_M 6–10 — 이미지 기반 T 와 EIS T 의 대조 선례 (RVE 크기 경고 포함) |
| [34] | M. Ender, J. Joos, T. Carraro, and E. Ivers-Tiffee, J. Electrochem. Soc., 159, A972 (2012). | FIB-SEM 재구성 + Laplace 로 N_M — 우리 복셀 Laplace T 와 같은 계산 계열 |
| [32] | M. Ebner, D. W. Chung, R. E. Garcı́a, and V. Wood, Adv. Energy Mater., 4, 1 (2014). | 입자 이방성 → 관통 τ 증가 (구형 NMC ≈ Bruggeman) — 구 DEM 이 놓치는 형상 효과의 정량 출처 |
| [26] | N. Ogihara, S. Kawauchi, C. Okuda, Y. Itou, Y. Takeuchi, and Y. Ukyo, J. Electrochem. Soc., 159, A1034 (2012). | TLM-C 대칭셀 원법 — 이 논문이 >30 % 과대를 지적한 대상; 문헌 τ 의 방법 확인용 |
| [42] | M. Eikerling and A. A. Kornyshev, J. Electroanal. Chem., 475, 107 (1999). | Eq. 11 TLM 해석해의 출처 (CPE 확장 근거) |
| [2] | K. K. Patel, J. M. Paulsen, and J. Desilvestro, J. Power Sources, 122, 144 (2003). | 구형 입자 Bruggeman 검증 + 분리막 N_M (접촉저항 차감 논쟁) |
| [21] | D.-W. Chung, M. Ebner, D. R. Ely, V. Wood, and R. Edwin Garcı́a, Model. Simul. Mater. Sci. Eng., 21, 074009 (2013). | Bruggeman 타당성의 수치 검토 (Bruggeman 과의 불일치 선행 보고) |
| [33] | L. Zielke, T. Hutzenlaub, D. R. Wheeler, I. Manke, T. Arlt, N. Paust, R. Zengerle, and S. Thiele, Adv. Energy Mater., 4, 1 (2014). | 단층촬영 + 탄소·바인더 모델링 결합 — 우리 망에 없는 CBD 차단을 보정하는 방법 아이디어 |
| [50] | B. Tjaden, S. J. Cooper, D. J. L. Brett, and D. Kramer, Nanotechnology, Sep. Eng., 12, 44 (2016). | Bruggeman 관계의 기원·적용 상세 (Note added in proof).  ⚠ 목록의 저널 표기가 학술지명이 아니라 섹션명처럼 보임 — **[미확인: 저널명]** |
| [17] | D. A. G. Bruggeman, Ann. Phys, 24, 636 (1935). | Bruggeman 원전 — α 관례의 원 형태 확인 |
| [20] | R. B. Macmullin and G. A. Muccini, AIChE J., 2, 393 (1956). | MacMullin 수 원전 |

- 이 논문 목록 밖의 후속: **Minnmann 2021 의 참고문헌 61** = *"J. Landesfeind, M. Ebner, A. Eldiven, V. Wood, and H. A. Gasteiger, J. Electrochem. Soc., 165, A469 (2018)."*
  (그 목록 표기 그대로, 제목 미확인) — 같은 저자의 후속으로 EIS τ 와 이미지 기반 τ 를 잇는 데 필요할 수 있다 (내용 미확인).

## 15. 🔗 이 방법·정의를 쓰는 corpus 카드
- `ngandjong2021_dem_calendering_digital_twin` — τ_EIS 를 **Landesfeind TLM** 으로 (그래프법 ×3) 구함: 1.3676 / 1.3808 / 1.7527 @ ε 41.6 / 31.5 / 27.2 % (그 카드 Table 3).  **같은 T 관례**.
- `duquesnoy2023_ml_multiobjective_manufacturing_optimization` — S4 의 `T = AεR_ion σ/2d` = 이 논문 Eq. 13.
- `minnmann2021_jes_charge_transport_bottlenecks` — 이 논문을 ref 42 로 인용; τ_i² = 이 논문 τ (= T).  ⚠ 그 논문 Eq. 4 인쇄형의 역수 누락 (§8-2).
- `taufactor_tortuosity_factor_tomography_tool` — TauFactor τ = 이 논문 τ (= T).
- `bazzoun2026_dem_fem_rnm_ionic` — ASSB Z-type TLM + CPE (α 0.67–0.74) 로 σ_eff,ion 추출 — §9 ⑦⑧ 의 실험 앵커.
- 같은 묶음 (2026-10-03 inbox, 카드 작성 중): Tjaden 2018 리뷰 (inbox #2) · `nguyen2020_electrode_tortuosity_factor` (inbox #6, 전극 tortuosity factor 재정의) — 이 카드 §8 과 함께 읽을 것.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

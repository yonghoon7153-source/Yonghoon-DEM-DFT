<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 기준 = 같은 1저자의 2016 카드 (landesfeind2016_tortuosity_eis_electrodes_separators) · tjaden2018 · taufactor 카드.
     이 논문은 시뮬레이션이 아니라 측정법 검증 + 영상 τ 대조 논문 (액체 전해질 LIB) 이다.  그래서 §4 = 검증 사슬 (전자 저항 → 강구 known-τ → XTM 대조 → 바인더),
     "§ τ 정의 대조 — 우리 규약 매핑" 절을 §7 뒤에 두고, §8 = 이 묶음이 닫는 항목 (같은 전극의 임피던스 τ ↔ 단층촬영 τ 직접 대조).
     2016 카드와 겹치는 정의 (N_M · 2016 Eq 1–13 · TLM-Q · 비삽입 염 차단) 는 그 카드를 참조만 하고 되풀이하지 않는다.
     쪽 표기 = 학술지 인쇄 쪽 A469–A476.  PDF 9 쪽 중 1 쪽은 IOP 표지 + 광고 (본문 아님) → PDF n 쪽 = 학술지 A(467+n).  SI 없음.
     식 · 표 · 그림 번호 = 원문.  식 · 표 · 그림은 원문 PDF 를 렌더해 읽었다 (텍스트 추출은 τ · ε · κ 를 깨뜨린다).
     값 표지: stated = 본문 · 캡션 · 표 원문 / 판독 = 그림에서 읽은 근사 (TREND 전용, 정밀 인용 금지) / 파생 = 카드 작성자 계산 (식 명시). -->
# 전극 tortuosity 의 임피던스 값 검증 — 일반 TLM 의 전자 저항 창 (R_El/R_Ion < 10⁻²) · 강구 충전 known-τ (1.56 vs Bruggeman 1.60–1.62) · 같은 코팅 X선 단층촬영 τ 의 약 2 배 (원인 = 미해상 바인더 · 탄소) — Landesfeind (J. Electrochem. Soc. 2018)

> slug `landesfeind2018_tortuosity_impedance_vs_tomography` · DOI `10.1149/2.0231803jes` · type `exp (EIS 차단 대칭셀 TLM 검증 · 강구 known-τ · 같은 코팅 XTM τ 대조; liquid-LIB tortuosity)` · PDF `3. Tortuosity of battery electrodes validation of impedance-derived values and critical comparison with 3D tomography.pdf` · digested `2026-10-03` · status ✅
>
> ★ **정의 판정 (이 카드의 목적)** — 이 논문의 τ 는 **Eq. 9 `τ = R_Ion·A·ε·κ / t` (A471) — 제곱 없음** 이고, Bruggeman 을 **`τ = ε^−0.5` (Eq. 10, A472)** 로 쓴다 ⇒ 2016 카드의 τ (= ε·N_M) 와 같은 척도 = 우리 **tau2**.
> 본문에 "tortuosity factor" · "effective tortuosity" · "MacMullin" 낱말은 **0 회** (전수 검색) — 정의는 Ref. 5 (= 2016 논문) 에 맡기고 이름은 그냥 "tortuosity (τ)" 다.
> ★ **측정 경로** — 차단 대칭셀 + 비삽입 염 (TBAClO₄) + 간이 전송선 모델 (TLM) = Nguyen 2020 분류의 **eSCM → τ_e 계열**.  저자는 이 값을 *"the true tortuosity"* 로 부르고 conventional (Bruggeman) τ 와 같은 양으로 다룬다 (Nguyen 이전 논문).
> 두 정의가 같다는 실측은 **균질 · 단분산 · 전부 관통한 강구 충전 한 기하** 뿐이다 (§8-4).
> ★ **핵심 결과** — 같은 코팅에서 자른 NMC · NCA · 흑연 전극의 τ_EIS / τ_XTM = **1.75 · 2.31 · 1.51** (tau2 척도, 파생 — 원문 *"~2-fold"* · *"largest discrepancy of a factor ~2.3 … NCA"*).  √ 척도 (tau) 로는 **1.32 · 1.52 · 1.23**.
> 저자 귀속 = **X선 단층촬영 (325 nm voxel) 이 못 푼 바인더 · 도전 탄소 (CBD)** — 바인더 1.5 → 10 wt% PVDF 만 바꿔도 τ_EIS 2.7 → 5.0 (A474–A475).
>
> 출처 PDF = `litdb/inbox/3. ….pdf` (9 쪽).  PDF 1 쪽 = IOP 표지 + "You may also like" + 장비 광고 (본문 · 인용 아님).  본문 = PDF 2–9 쪽 = **A469–A476**.  보충자료 (SI) 없음.

---

## 0. 결론 먼저

| 질문 | 답 | 근거 (식 · 쪽) |
|---|---|---|
| 이 논문의 τ 는 τ 인가 τ² 인가? | **제곱 없는 τ = ε·κ/κ_eff** (Eq. 9) = 2016 τ = 우리 **tau2** (= COMSOL τ_F = TauFactor τ = Minnmann τ²) | Eq. 9 (A471) · Bruggeman τ = ε^−0.5 (Eq. 10, A472) |
| EIS 값은 어느 측정법 계열인가? | 차단 대칭셀 EIS + 간이 TLM → Nguyen 분류상 **eSCM (τ_e 계열)**.  저자는 conventional τ 와 같은 양으로 취급 | A469 · A472–A473 · Conclusions A475 |
| XTM 값은? | 3D 재구성 위 **수치 확산 시뮬레이션 · 관통 방향 · 325 nm voxel · CBD 미해상**.  식은 원문에 없다 (Refs 2 · 11) → conventional flux tau2 로 읽는다 (판독) | Table II 캡션 · A474 |
| 같은 코팅 EIS ÷ XTM | NMC **1.75** · NCA **2.31** · 흑연 **1.51** (tau2, 파생) | Table II (A474) |
| 저자가 지목한 원인 | 미해상 **바인더 + 도전 탄소** — *"most likely cause"* | A474–A475 · Conclusions |
| 그 근거 실험 | 흑연 (T311) 1.5 % vs 10 % PVDF: R_Ion 145 ± 5 vs 213 ± 4 Ω → **τ 2.7 ± 0.1 vs 5.0 ± 0.2** (다공도 51 / 50 %) | Fig. 6 (A475) · A474–A475 |
| 배제된 후보 | 전극 전자 저항 (κ-불변 Fig. 3) · TLM 모형 (강구 1.56 vs 1.60–1.62) · 이온–기공벽 상호작용 (10 mM–1 M 불변 + 표면적 산술).  이방성은 원인으로 들지 않는다 (XTM 값도 관통 방향 — 방향 일치) | A471–A474 |
| 결정 13 (τ_e ↔ conventional) | 이 논문은 둘을 **분리하지 않는다**.  2 배는 정의 차가 아니라 CBD 해상도 차 (저자 귀속).  깨끗한 유일 사례 (강구) 에서 τ_EIS/τ_Brug = **0.962–0.974** → 정의 차 상한 ≈ 4 %.  **"P2D 입력 부호 불정" 한정어 유지** | §8-4 |
| Minnmann "LIB tortuosity factor 는 한 자릿수 낮다" 의 척도 | 이 논문 값은 **전부 tau2 척도** (= Minnmann τ²) → 같은 척도 비교면 성립.  단 "한 자릿수" 는 Minnmann **61 vol%** (130 · fine 33.8) 대비에서만 · 25–42 vol% (2.40–4.27) 와는 **같은 자릿수** | §8-6 |

## 1. 한 줄 요약
차단 대칭셀 EIS 로 구한 전극 tortuosity 가 3D 단층촬영 수치값보다 늘 크다는 문헌 불일치를 풀려고, EIS 법의 두 가정을 차례로 검증한다.
(i) **전극 전자 저항 무시** — 일반 TLM 모의로 R_El/R_Ion < 10⁻² 일 때만 R_Ion 이 정확함을 보이고 (10⁻²–10⁻¹ 이면 오차 최대 ~20 %), 실험 검사법 (**전해질 전도도 κ 를 바꿔도 R_Ion·κ 가 일정한가**) 을 NMC · 흑연에 적용한다.
(ii) **TLM 이 참 τ 를 준다** — 1 mm 강구를 채운 거시 대칭셀에서 τ_EIS = 1.56 이 Bruggeman 1.60–1.62 와 ~3 % 안에서 맞는다.
그 뒤 **같은 코팅**의 NMC · NCA · 흑연을 EIS 와 X선 단층촬영 (XTM) 으로 둘 다 재서 EIS 가 **~2 배** 큼을 확인하고, 원인을 **XTM 이 해상하지 못한 바인더 · 탄소 상** 으로 결론짓는다 (바인더만 1.5 → 10 wt% 로 바꾼 흑연에서 τ_EIS 2.7 → 5.0).
우리에게는 **(a) EIS τ 의 척도 = tau2 재확인 (b) 영상/모형 τ 가 차단상을 빼면 τ 를 과소평가하는 크기 (c) 균질 구 충전에서 차단 대칭셀 τ ≈ conventional τ 라는 실측 한 점** 을 준다.  수치는 액체 LIB 라 전이 불가.

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Johannes Landesfeind** (교신 · ECS student member), Martin Ebner, Askin Eldiven, Vanessa Wood, **Hubert A. Gasteiger** — ¹ TU München (Chair of Technical Electrochemistry, Dept. of Chemistry and Catalysis Research Center) · ² ETH Zürich (Dept. of Information Technology and Electrical Engineering) — Ebner · Wood = ETH | **J. Electrochem. Soc. 165 (3) A469–A476 (2018)** | **10.1149/2.0231803jes** | 액체 전해질 LIB: 흑연 (SGL T311) · Custom Cells 의 NMC111 · NCA · 흑연 전극 + 1 mm 강구 (1.3505) 모형 전극.  전해질 = TBAClO₄ in EC:DEC / EC:DMC / EC:DMC:DEC | **실험** (EIS · X선 단층촬영 대조) + 일반 TLM 해석식 모의 |

- 접수 2017-12-28 · 수정본 2018-01-26 · 게재 2018-02-10.  **Open access CC BY-NC-ND 4.0** (A469).
- 연구비: BMBF ExZellTUM II (03XP0081) — J.L. / ERC (680070) — M.E. · V.W.  사의: Andreas Ehrl (논의) · Patrick Pietsch (X선 단층촬영) (A475).
- 참고문헌 18 편 (A475–A476).  Ref. 5 = 2016 논문 (`landesfeind2016_tortuosity_eis_electrodes_separators`).  Refs 2 · 11 = Ebner (XTM τ 원 논문, 이 카드에서 미열람).
- 본문 끝 예고: *"Further experimental investigations about the influence of the binder … will soon be published in a detailed, separate study"* (A475) — 어느 논문인지 원문에 없다 [미확인].

## 3. 핵심 수치 (이 논문이 주는 것)
> 이 논문은 우리 소재 물성 앵커 (porosity@P · σ_ion/e/thermal · E_SE · coverage · Z · Heckel) 를 **주지 않는다** → 전부 n/a.  주는 것은 ① EIS τ 의 유효 조건, ② known-τ 검증 한 점, ③ 같은 코팅 EIS ↔ XTM 표, ④ 바인더 효과 크기.

| 양 | 값 | 조건 | 표지 | 쪽 |
|---|---|---|---|---|
| EIS 로 R_Ion 이 정확한 창 | **R_El/R_Ion < 10⁻²** · 10⁻²–10⁻¹ 이면 R_Ion 오차 **최대 ~20 %** | 일반 TLM 모의 (Eq. 1), 차단 (R_CT = ∞), γ = 1 | stated | A471 |
| R_El/R_Ion = 1/1 일 때 | R_HFR^app = 0.5·R_El · R_Ion^app = 0.5·R_Ion | 같음 | stated | A471 |
| R_El/R_Ion = 100/1 일 때 | 저주파 외삽 실축 절편 **~33 Ω** (Fig. 1 범위 밖) | 같음 | stated | A471 |
| Fig. 2 곡선의 닫힌 꼴 | **R_Ion^app/R_Ion = 1 + x − 3x/(1+x)** · **R_HFR^app/R_Ion = x/(1+x)** (x = R_El/R_Ion) · 최소 0.464 @ x = √3 − 1 = 0.732 | Eq. 1 의 ω→∞ · ω→0 극한 | **파생** (원문에 없음 · Eq. 1 수치 평가와 일치) | — |
| NMC τ_EIS (κ 스윕 평균) | **3.6 ± 0.3** | Custom Cells NMC111, ε 42 %, t 72 µm, 86 % AM, 2 mAh/cm² (13.8 mg/cm²) · κ **0.156–6.97 mS/cm** (~4 mM–1 M TBAClO₄, EC:DEC) | stated | A472 |
| 흑연 τ_EIS (κ 스윕 평균, 2016 Fig. 14 자료 재작도) | **5.1 ± 0.8** | ε 43 %, t 58 µm, 2.1 mAh/cm² (6 mg/cm²) · κ 0.46–9.56 mS/cm (10–700 mM, EC:DMC) | stated (⚠ 2016 원문 평균은 4.3 ± 0.6 — §10) | A472 |
| 강구 셀 다공도 → Bruggeman τ | ε **38 % · 39 %** → τ **1.62 · 1.60** | 1 mm 강구, Table I | stated | A473 |
| 강구 셀 EIS 적합 | R_HFR **37 Ω** · R_Ion **790 Ω (두 전극 합)** · R_CT **10200 Ω** · Q_S **2.8 mF·s^(α−1)** · α **0.88** | 10 mV, 200 kHz–20 mHz (적합 · 그림 1 kHz–30 mHz) | stated | A473 (Fig. 5) |
| 강구 τ_EIS | **1.56** (ε 38.5 ± 0.5 %, t 1.9 cm, κ 0.892 mS/cm) | Eq. 9 | stated | A473 |
| 강구 τ_EIS / τ_Brug | **0.962 – 0.974** (평균 ε 0.385 기준 0.968) | 원문 *"~3% lower"* | 파생 | — |
| 강구 전자 저항 | **8 Ω** (R_Ion 790 Ω 의 ~1/100 → x ≈ 0.0101) | 수동 클램프 압축 | stated | A472 |
| Table II — NMC | ε 40 %, 125 µm, 3.5 mAh/cm² / 24.1 mg/cm², 86 % AM · **XTM 1.77 ± 0.06 · EIS 3.1 ± 0.3 (n 4)** | XTM 325 nm voxel · 관통 | stated | A474 |
| Table II — NCA | ε 40 %, 115 µm, 3.5 / 21.6 mg/cm², 90 % AM · **XTM 1.73 ± 0.03 · EIS 4.0 ± 0.05 (n 2)** | 같음 | stated | A474 |
| Table II — 흑연 | ε 51 %, 110 µm, 3.8 / 10.9 mg/cm², 96 % AM · **XTM 2.18 ± 0.06 · EIS 3.3 ± 0.05 (n 2)** | 같음 | stated | A474 |
| EIS ÷ XTM | NMC **1.75 ± 0.18** · NCA **2.31 ± 0.05** · 흑연 **1.51 ± 0.05** (± = 표 SD 의 1차 전파, 참고용) | tau2 척도 | 파생 | — |
| 바인더 실험 | 1.5 % PVDF (109 ± 2 µm, 51 ± 0.5 %) R_Ion **145 ± 5 Ω → τ 2.7 ± 0.1** · 10 % PVDF (85 ± 2 µm, 50 ± 0.5 %) **213 ± 4 Ω → τ 5.0 ± 0.2** | T311 미압축, T-cell 0.95 cm², 10 mM TBAClO₄ EC:DEC κ 0.423 mS/cm, 20 mV, 200 kHz–100 mHz | stated | A474–A475 |
| 이온–기공벽 상호작용 반론 | 코팅 표면 **~100 cm²/cm²_El** vs 1 M 이온의 절반이 벽에 붙으려면 **> 2500 cm²/cm²_El** (80 µm · 기공 30 % · 이온 반경 0.3 nm, 빈틈 · 용매화 껍질 없이 쌓는 보수적 가정) | — | stated | A474 |
| 인용 문헌값 | MCMB 고해상 재구성 **2–7** (15 µm 큐브, 입자 ~8 µm — 비대표) · 가스 투과 (면내) 흑연 30 % · 50 µm **~6** ↔ 비슷하게 압축한 흑연 EIS **~5.5** · 흑연 XTM 도 낮게 나옴 (voxel 0.56 µm) | Refs 17 · 14 · 5 · 15 | stated (인용) | A474 |

## 4. 방법 ★

### 4-1. 정의식 — 원문 식 번호 · 쪽 그대로

| 식 | 원문 형태 | 쪽 | 뜻 · 원문 단서 |
|---|---|---|---|
| **Eq. 1** | `Z_El = Z_∥ + Z*·{1 + 2·p·s·[√(1 − tanh(ν)²) − 1]} / tanh(ν)` | A470 | **일반 TLM** — 고체상 전자 저항과 기공 이온 저항이 둘 다 45° 중주파 영역에 들어간다.  출처 = Ref. 7 (Göhr, ZAHNER 1997), *"Adopting the nomenclature of our previous work"* |
| Eq. 2 | `Z_∥ = Z₁·Z₂ / (Z₁ + Z₂)` | A470 | Z₁ ≡ R_El (전자 전도 고체상), Z₂ ≡ R_Ion (기공 전해질) |
| Eq. 3 | `Z* = √((Z₁ + Z₂)·Z_S)` | A470 | Z_S = 고/액 표면 임피던스 |
| Eq. 4 · 5 | `p = Z₂/(Z₁ + Z₂)` · `s = Z₁/(Z₁ + Z₂)` | A470 | — |
| Eq. 6 | `ν = √((Z₁ + Z₂)/Z_S)` | A470 | — |
| Eq. 7 | `Z_S = R_CT / (R_CT·(iω)^γ·Q_S + 1)` | A470 | R/Q 원소 (CPE 용량 Q_S + 전하이동 저항 R_CT) |
| Eq. 8 | `Z_S = 1 / ((iω)^γ·Q_S)` | A470 | R_CT → ∞ (비삽입 염 = 차단).  Eq. 1 은 R_El → 0 이고 R_CT → ∞ 일 때만 간이 TLM (2016 Eq. 11) 으로 줄어든다 |
| **Eq. 9** | `τ = R_Ion·A·ε·κ / t` | A471 | **전극 τ** — κ = 전해질 전도도, ε = 다공도 (*"easily determined by electrode thickness (t) and loading measurements"*), R_Ion = 기공 전해질의 유효 이온 저항, A = 면적, t = 전극 (코팅) 두께.  2016 Eq. 8 · 13 과 같은 꼴 (대칭셀 합이면 /2) |
| **Eq. 10** | `τ = ε^−0.5` | A472 | Bruggeman (구형 입자, Ref. 12 = Bruggeman 1935) — *"the mathematically derived Bruggeman relation"* |

- **원문 "1/3 규칙"** (A470): 간이 TLM 에서 45° 영역의 실축 절편과 저주파 가지 외삽 절편의 차 = **R_Ion/3** (Refs 5 · 8).  그 조건 (R_El → 0, R_CT → ∞) 이 아니면 같은 그래프법이 **겉보기 R_Ion^app** 를 준다.
- ⚠ **R_Ion 의 전극 수 규약이 절마다 다르다** (원문은 강구 절에만 *"for both electrodes"* 라 적는다) — Eq. 9 로 다시 계산하면 (파생):
  강구 790 Ω 은 **두 전극 합** 으로 읽어야 τ 1.56 이 나온다 (전극 하나 = 395 Ω → 1.563; 790 을 그대로 넣으면 3.13) · 바인더 실험 145 / 213 Ω 은 **전극 하나** 값으로 넣어야 2.7 / 5.0 이 나온다 (2.73 · 5.04; 합으로 읽으면 1.36 · 2.52).
  ⇒ 이 논문의 R_Ion 을 재사용할 때는 절마다 규약을 확인한다.

### 4-2. 검증 사슬 (논증 순서)

| 단계 | 질문 | 방법 | 결과 | 쪽 |
|---|---|---|---|---|
| ① | 전극 전자 저항을 무시해도 되나 | 일반 TLM (Eq. 1) 모의 → Fig. 1 · 2 | R_El/R_Ion < 10⁻² 이면 정확, 10⁻²–10⁻¹ 이면 R_Ion 오차 최대 ~20 % | A470–A471 |
| ② | 실제 전극이 그 창 안인가 | **κ 를 바꿔 R_Ion^app·κ 가 일정한지** 본다 (Fig. 3) | NMC (κ ×~45) · 흑연 (κ ×~21) 모두 일정 → R_El/R_Ion ≲ 1/100 | A471–A472 |
| ③ | TLM 으로 얻은 R_Ion 이 참 τ 를 주나 | τ 를 아는 기하 = **1 mm 강구 충전** 대칭셀 (Fig. 4 · 5 · Table I) | τ_EIS 1.56 vs Bruggeman 1.60–1.62 (~3 % 낮음, 벽 효과로 귀속) | A472–A474 |
| ④ | 왜 EIS > XTM 인가 | **같은 코팅**을 XTM 수치 확산 · EIS 로 둘 다 (Table II) | EIS ≈ 2 × XTM (1.5–2.3) | A474 |
| ⑤ | 원인 후보 배제 · 지목 | 이온–벽 상호작용 산술 · 해상도 · 문헌 | CBD (바인더 + 탄소) 미해상이 가장 유력 | A474 |
| ⑥ | 그 가설의 직접 시험 | 같은 흑연, 바인더 1.5 % vs 10 % (Fig. 6) | τ_EIS 2.7 → 5.0 | A474–A475 |

### 4-3. 일반 TLM 모의 (Fig. 1 · Fig. 2, A470–A471)
- 모의 조건: 10 MHz–1 Hz · R_CT = ∞ · γ = 1 · **Q_S = 1 mF** · R_El/R_Ion = 1/100 · 1/3 · 1/1 · 3/1 · 100/1 (Fig. 1).  축은 R_Ion 으로 정규화.  자홍 × = 100 kHz · 1 kHz · 100 Hz.
- 모형에 분리막 · 셀 접촉 직렬 저항이 없으므로 원래 HFR 은 0 이어야 하고, **겉보기 HFR 이 0 이 아닌 것은 R_El/R_Ion 의 효과뿐**이다 (A471).
- R_El/R_Ion = 1/100 에서 저주파 외삽 절편 = Re(Z)/R_Ion **0.33** (A471) — 참값 R_Ion/3.
- 경향 (Fig. 2): x = R_El/R_Ion 이 커지면 R_HFR^app ↑ (1/1 에서 0.5·R_El) · R_Ion^app 는 처음엔 ↓ (1/1 에서 0.5·R_Ion) → x ≫ 1 에서 R_HFR^app → R_Ion, R_Ion^app → R_El/3 근처로 발산 (100/1 에서 ~33 Ω) (A471).
- **발산의 해석** (A471): x ≫ 1 은 분리막처럼 순수 축전 응답이 기대되지만, 이 모형은 금속 집전체의 이중층 계면을 넣지 않아 발산한다.  집전체/코팅 계면을 넣은 일반화 (Ref. 7) 에서는 R-C 거동이 되고 R_Ion^app/R_Ion → 0.  **x ≤ 1 까지는 두 모형이 같은 결과** — 어느 쪽이든 일정한 R_Ion^app/R_Ion 은 R_El 이 무시될 때만 (초록 영역).
- **카드 유도 (파생 — 원문에 없음)**: Eq. 1 에서 ω → ∞ 이면 Z → Z_∥ = R_El·R_Ion/(R_El + R_Ion), ω → 0 이면 Re Z → (R_El + R_Ion)/3 ⇒ 그래프법 결과
  `R_Ion^app/R_Ion = 3·[(1+x)/3 − x/(1+x)] = 1 + x − 3x/(1+x)` · `R_HFR^app/R_Ion = x/(1+x)`.
  확인: x = 0.01 → 0.980 · x = 0.1 → 0.827 (원문 "~20 %" 와 정합) · x = 1 → 0.5 (원문 그대로) · 최소 0.464 @ x = 0.732 (Fig. 2 빨강 최저점 ≈ 0.46 판독과 일치).  Eq. 1 을 직접 수치 평가한 값과 3 자리에서 일치했다.
  ⚠ 방향: **x < ~1 에서 R_El 은 겉보기 R_Ion 을 줄인다 → EIS τ 를 낮추는 쪽**이다.

### 4-4. κ-불변 검사 (Fig. 3, A471–A472)
- 원리 (A471): 높은 κ 는 R_Ion 을 줄여 x = R_El/R_Ion 을 키운다.  **같은 전극에서 R_Ion^app·κ 가 mM 과 M 농도에서 같으면 x < 10⁻² 이다** (Fig. 2 의 평탄 구간).  ⇒ *"Demonstration of the invariance of (R_Ion·κ) over a wide range of electrolyte conductivities is thus a proof that electronic resistance contributions are negligible"*.
- 흑연 (2016 자료): κ 0.45–9.6 mS/cm 에서 불변 — 흑연 전극 전자 전도도 > S/cm (Ref. 9) 라 당연 (A472).
- NMC (Custom Cells 압축 전극): EC:DEC (1:1 w:w) + TBAClO₄ **~4 mM (0.156 mS/cm) – ~1 M (6.97 mS/cm)** — 두께 · 다공도 편차는 셀마다 반영 → **3.6 ± 0.3** 일정 ⇒ x ≲ 1/100 (A472).
- 형상: 구형 NMC 3.6 < 판상 흑연 **5.1 ± 0.8** — *"in accord with previous observations"* (Refs 5 · 11).
- 실용 한계 (A472): TBAClO₄ < 5 mM 은 불순물이 유효 전도도를 바꿀 수 있어 오차 ↑ · 통상 용매의 최대 κ ≈ 20 mS/cm.  R_HFR^app 도 x 가 작으면 κ 에 불변이어야 하지만, 유리섬유 분리막 압축이 셀마다 같아야 정량 비교 가능.
- 전자 저항이 무시되지 않는다면 *"the amount of conductive carbon additive is either insufficient or … poorly dispersed"* (A472).

### 4-5. 강구 거시 셀 — τ 를 아는 기하 (Fig. 4 · Fig. 5 · Table I, A472–A474)
- 강구 = 스테인리스 크롬강 (type 1.3505) 볼베어링 **지름 1 mm** (TIS Wälzkörpertechnologie GmbH, Gauting) 를 유리관에 조밀 충전 → 위 · 아래 Cu 박 집전체, **가운데 유리섬유 분리막 더미**로 나눠 사실상 **강구 전극 두 개** 의 대칭셀.  같은 기계 압력으로 전자 저항을 낮춘다 (수동 클램프) → **R_El 8 Ω** (≈ R_Ion 790 Ω 의 1/100) (A472–A473).
- 전해질: EC:DMC:DEC + **~30 mM TBAClO₄** — 이온 전도도가 강구 다공체의 전자 전도도보다 충분히 작도록 고른 농도 (A473).

**Table I (A473)** — 원문 값

| 항목 | 값 |
|---|---|
| 다공 전극 하나의 두께 | 1.9 cm |
| 전극 반지름 | 2.64 cm |
| 전극당 전해질 질량 | 16.8 g |
| 전극당 강구 질량 | 200.4 g |
| 전해질 밀도 | 1.065 g/cm³ (실험 직전 ~30 mM TBAClO₄ EC:DMC:DEC 10 ml 칭량) |
| 강 밀도 | 7.9 g/cm³ |
| 실험 온도의 전해질 벌크 전도도 | 0.892 mS/cm |

- 다공도 두 산정 (A473: 전체 기하 부피 + 전해질 부피 또는 강구 부피) → **38 % · 39 %**.  카드 재계산 (파생): V_geo = π·2.64²·1.9 = 41.60 cm³ · V_전해질 = 15.78 cm³ → ε 0.379 · V_강 = 25.37 cm³ → ε 0.390 — 원문과 일치.
- 적합 회로 (A473): 분리막 HFR + 직렬 TLM (전자 저항 무시 — 압축 + 낮은 κ 로 정당화).  **저주파에 큰 반원** → 표면 원소는 CPE 가 아니라 **R_CT ∥ Q_S** (Eq. 7).  큰 R_CT (10200 Ω) 는 *"minor parasitic reactions between the electrolyte and the stainless steel ball bearings"* 일 수 있으나, 고주파 45° 영역이 뚜렷해 R_Ion 결정에는 지장 없다.
- 결과: R_Ion 790 Ω (두 전극) · ε 38.5 ± 0.5 % · t 1.9 cm · κ 0.892 mS/cm → **τ 1.56** — *"excellent agreement with the theoretical prediction of τ = 1.60–1.62"* (A473).
- 원문 해석 (A473–A474): ~3 % 낮은 것은 **유리관 벽 근처의 덜 조밀한 충전 (edge effects)** 이 전체 이온 저항을 조금 낮춘 탓일 것.  결론: *"EIS is a robust method for measuring the tortuosity of porous lithium ion battery electrodes"*; Conclusions 는 *"unequivocally proves that the EIS-derived tortuosity values are indeed correct, as long as electronic resistance contributions can be neglected"* (A475).
- **카드 점검 (파생)**: x = 8/790 = 0.0101 이면 §4-3 닫힌 꼴로 R_Ion^app/R_Ion = 0.980 → **전자 저항 몫만으로 −2 %** 가 나올 수 있다 (8 Ω 에 집전체 접촉이 섞였다면 그보다 작다 — 상한).  ⇒ −3 % 의 일부는 벽 효과가 아니라 x 몫일 수 있다 (원문은 벽 효과만 든다).
- 기하 규모 (파생): 두께 1.9 cm = 강구 19 개, 반지름 2.64 cm = 26.4 개.  R_CT/R_Ion ≈ 12.9.

### 4-6. 같은 코팅 XTM ↔ EIS (Table II, A474)
- 전극 = Custom Cells (Itzehoe, Germany) 의 NMC111 · NCA · 흑연 (A470 Experimental: *"electrodes for the comparison of EIS and XTM tortuosities were obtained from Custom Cells (specifications in Table II)"*).
  표 캡션은 *"the same type of electrodes"*, 본문 A474 는 *"the tortuosity of the same porous electrode"*, Conclusions 는 *"identical electrodes cut from the same coating"*, 초록은 *"electrodes from the same coating"* — **같은 코팅의 다른 조각**으로 읽는다 (XTM 시편 ≠ EIS 원판).
- XTM 쪽: 3D 재구성 위 **수치 확산 시뮬레이션** · 보고값 = **관통 방향** (분리막 · Cu 박에 수직) · **voxel 325 nm** · 불확도 = 이진화 회색값 문턱 선택에서 온 것.  방법 상세는 Refs 2 · 11 로 넘긴다 — **이 논문에는 XTM τ 의 식이 없다**.
- EIS 쪽: 대칭셀 · 반복 측정의 SD (괄호 = 반복 수).  방법 상세는 Ref. 5.
- 일반 서술 (A474): 통계적으로 의미 있는 부피 (입자 수천 개) 를 재려면 **~1 mm³** 가 필요하고 그 장치로는 카본블랙 · 바인더를 해상할 수 없어 **마이크로미터급 활물질 형태만** 보인다.

### 4-7. 바인더 실험 (Fig. 6, A474–A475)
- 흑연 T311 (SGL Carbon, BET 3.0 m²/g, D50 19 µm) + PVDF (Kureha KF 1100) + NMP 슬러리 → Thinky ARV-310 행성식 혼합 (2000 rpm 5 min, 전 성분 동시 투입) → Cu 박 (MTI, 9 µm) 닥터블레이드 (A469–A470).  **미압축** 전극.
- 바인더 극단값을 일부러 골랐다: **1.5 wt%** (안정한 전극을 만드는 최소) · **10 wt%** (현실적 최대) (A474).
- 측정: 대칭 T-cell (0.95 cm²) · 10 mM TBAClO₄ in EC:DEC (κ 0.423 mS/cm) · 전극 종류당 2 셀 · 스펙트럼은 HFR 만큼 원점으로 이동 (Fig. 6 가로축 표기 "Re(Z − Z₁)").
- 결과: R_Ion **145 ± 5 Ω → τ 2.7 ± 0.1** (1.5 %, 109 ± 2 µm, 51 ± 0.5 %) · **213 ± 4 Ω → τ 5.0 ± 0.2** (10 %, 85 ± 2 µm, 50 ± 0.5 %) — Eq. 9 재계산 2.73 · 5.04 (파생, R_Ion = 전극 하나 값으로).
- 원문 결론 (A475): *"even though the binder is a small fraction of the coating mass and volume (1% – 5%), it has a pronounced effect on the effective ionic transport properties of the porous electrode and could explain the difference"*.
- 카드 보충 (파생): 같은 다공도 (51 vs 50 %) 에서 τ ×1.85 — **부피가 아니라 바인더가 놓이는 자리** (입자 목 · 다리) 가 기공망을 막는 효과로 읽힌다.  원문 "(1 % – 5 %)" 는 질량 분율 (1.5–10 wt%) 과는 맞지 않고, 코팅 부피 분율로는 카드 추정 ≈ 0.9–6 % (PVDF 1.78 · 흑연 2.26 g/cm³ **가정** — 원문에 밀도 없음).

### 4-8. 측정 조건 일람

| 항목 | 값 | 쪽 |
|---|---|---|
| 전해질 전도도 측정 | SI Analytics LF 1100+ (맞춤 연마 유리 피팅, 온도 센서 내장), 25 °C, 자가 조제 전해질 | A470 |
| T-cell | Swagelok 대칭 · 스프링 압축 ≈ 1 bar · **글러브박스 밖에서 조립** · 유리섬유 분리막 2 장 (VWR glass microfiber 691, 바인더 없음, 200 µm, 기공 > 90 %) · 25 °C 항온조 (Binder) | A470 |
| EIS (T-cell) | OCV 근방 · **≥ 12 h 휴지** 뒤 · 200 kHz–0.1 Hz · **20 mV** | A470 |
| EIS (강구) | 10 mV · 200 kHz–20 mHz (적합 · 그림 1 kHz–30 mHz) | A473 |
| 전해질 | TBAClO₄ (Sigma Aldrich, ≥ 99.0 %) in EC:DEC 1:1 (w) (EC 무수 99 %, DEC 무수 > 99 %) · EC:DMC 1:1 (흑연 2016 자료) · EC:DMC:DEC ~30 mM (강구) | A469–A473 |
| 흑연 바인더 시험 전극 (Experimental 서술) | ε 48 %, t 90 µm, ~3 mAh/cm² (8.6 mg/cm²) — ⚠ Fig. 6 본문 값 (51 % · 109 µm / 50 % · 85 µm) 과 다름 (§10) | A470 |
| XTM | voxel 325 nm (Table II) · 상세 = Refs 2 · 11 · 사의: Patrick Pietsch | A474–A475 |
| 적합 소프트웨어 · 맞춤 창 (전극) | 원문에 없음 (n/a) | — |

### 4-9. 시뮬레이션 · 입자 처리 ★
- **DEM · MPM · FEM · RNM 없음.**  "모의" 는 ① 일반 TLM 해석식 (Eq. 1) 의 값 계산 (Fig. 1 · 2) ② XTM 재구성 위 수치 확산 (Refs 2 · 11 의 방법, 이 논문에서 재기술 없음) 뿐이다.
- **입자 처리 ★** — 실제 입자 (흑연 판상 · NMC/NCA 구형 경향 — Custom Cells 전극의 SEM 은 이 논문에 없다).  XTM 은 활물질 입자만 해상하고 **CBD 를 기공으로 분류**한다 (저자의 원인 진단).
- **강구 = 물리적 강체 단분산 구** — 우리 DEM 의 강체 구와 같은 기하지만, **전도상은 구가 아니라 그 사이 기공 (전해질)** 이다.  Bruggeman ε^1.5 는 "전도 매질 속 절연 구" 의 결과라 이 기하에 맞는다.  우리 SE 접촉망은 **구 자신이 전도상** (보완 기하) 이라 이 known-τ 가 그대로 옮겨지지 않는다 (§7).

### 4-10. 기법 미니 용어집

| 용어 | 뜻 (이 논문에서) |
|---|---|
| **일반 TLM** (Eq. 1) | 전자 레일 (Z₁ = R_El) 과 이온 레일 (Z₂ = R_Ion) 을 둘 다 가진 전송선 모형.  출처 Ref. 7 |
| **간이 TLM** | R_El → 0 · R_CT → ∞ 극한.  2016 Eq. 11 |
| **겉보기 저항 R^app** | 간이 TLM 그래프법을 실제 (일반 TLM) 스펙트럼에 적용해 읽은 값 |
| **1/3 규칙** | 간이 TLM 에서 (저주파 외삽 절편 − HFR) = R_Ion/3 |
| **κ-불변 검사** | 같은 전극에서 κ 를 바꿔 R_Ion^app·κ (= τ 에 비례) 가 일정한지 → 일정하면 R_El 무시 가능 |
| **비삽입 염 (TBAClO₄)** | Li 를 삽입하지 않는 염 → 전하이동 없음 (차단) |
| **SBBPE** | stainless steel ball bearing porous electrode (강구 다공 전극) |
| **XTM** | X-ray tomographic microscopy (X선 단층촬영) |
| **through-plane** | 분리막 · 집전체에 수직 = 관통 방향 (EIS 와 같은 방향) |
| **CBD** | carbon-binder domain — 이 논문 낱말은 "binder/carbon matrix", "binder and carbon black phases" (CBD 약어는 원문에 없음) |
| **eSCM / τ_e** | Nguyen 2020 의 이름 (이 논문에는 없음) — 차단 대칭셀 EIS 로 정한 electrode tortuosity factor |

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 (A470) | 일반 TLM (Eq. 1) 모의 Nyquist, 10 MHz–1 Hz, R_El/R_Ion = 1/100 · 1/3 · 1/1 · 3/1 · 100/1, 축 R_Ion 정규화, R_CT = ∞ · γ = 1 · Q_S = 1 mF, 자홍 × = 100 kHz · 1 kHz · 100 Hz, 점선 = 저주파 가지 외삽 · 화살표 = R_Ion^app/R_Ion | 같은 그래프법이 x 에 따라 다른 값을 준다 — 문헌 EIS τ 를 앵커로 쓸 때 그 전극의 x 를 먼저 본다 |
| 2 (A471) | R_HFR^app/R_Ion (파랑 점선) · R_Ion^app/R_Ion (빨강) vs R_El/R_Ion (10⁻⁴–10³), 초록 = R_El ≪ R_Ion (< 10⁻²) | ★ **정확도 창**.  빨강 최저 ≈ 0.46 (판독) · 1/1 에서 둘 다 0.5 · x ≫ 1 발산.  닫힌 꼴 §4-3 |
| 3 (A472) | τ vs κ (로그 0.1–10 mS/cm): NMC 빨강 (EC:DEC 0.156–6.97) · 흑연 파랑 (2016 Fig. 14 자료, EC:DMC 0.46–9.56), 점선 = 평균 3.6 · 5.1, 오차막대 = 적합 5 % + κ 오차 | ★ **σ₀-불변 검사의 실측판** (우리 G4).  판독: NMC 점 ≈ 3.4 · 3.2 · 3.4 · 3.6 · 3.85 · 3.9 (κ 증가 순) — 고 κ 쪽이 ~0.5 높다.  전자 저항 효과라면 **반대** (낮아짐) 방향이라 다른 원인 — 원문 논의 없음 |
| 4 (A473) | 강구 대칭셀 사진: 유리관 · 위아래 Cu 박 · 강구 · 가운데 분리막 · 외부 압축 화살표 | known-τ 기준 기하의 실물 |
| 5 (A473) | 강구 셀 Nyquist (측정 빨강 × · 적합 검정 ○ · 점선 = 눈 가이드), 적합값 캡션 기재 | 판독: 45° 영역이 HFR (~37 Ω) 에서 실축으로 ≈ 260 Ω 뻗음 ≈ 790/3 (두 전극 합 R_Ion 과 정합) |
| 6 (A475) | 흑연 T311 대칭 T-cell, 1.5 % (파랑) vs 10 % (빨강) PVDF, 전극 종류당 2 셀, HFR 만큼 원점 이동 | ★ 같은 다공도에서 바인더만으로 45° 영역 (R_Ion) 이 길어진다 — 영상에서 안 보이는 상이 τ 를 ×1.85 바꾼다 |
| Table I (A473) | 강구 셀 매개변수 | 다공도 두 산정 재현 (§4-5) |
| Table II (A474) | XTM vs EIS — NMC · NCA · 흑연 | ★★ **이 묶음의 핵심 표** (§8-1) |

## 6. Post-processing ★
- **무엇**: 일반 TLM 극한 분석 (겉보기 HFR · R_Ion) · 간이 TLM 적합 (전극) · R_CT ∥ Q_S 를 넣은 TLM 적합 (강구) · 그래프법 (×3) · κ-불변 (τ ∝ R_Ion^app·κ, 셀별 두께 · 다공도 반영) · 다공도 = 질량 / 밀도 (강구) · 두께 + 적재량 (전극) · XTM 이진화 문턱 변화 → τ 불확도 · EIS 반복 SD.
- **수치화 방식**: τ vs κ 그림 (Fig. 3) · 단일 표 (Table II: 다공도 · 두께 · τ_XTM ± · τ_EIS ± (n)) · 적합 매개변수는 캡션 (Fig. 5).
- **도구**: 적합 소프트웨어 n/a (원문에 없음) · XTM 수치 확산 코드 n/a (Refs 2 · 11).
- **검증 설계**: κ 스윕 (NMC 6 점 · 흑연 4 κ × 여러 셀, 판독) · 기준 기하 1 개 (강구, κ 1 값) · 같은 코팅 3 전극 · 바인더 2 수준 × 2 셀.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⛔ 기준값 자리표시 상태 — 비교는 정의 · 코드 단위로)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 전도상 | 액체 전해질 (기공 연속체, 내부 계면 없음) | SE 입자 (DEM 접촉망, 접촉마다 Holm 1/(2σa)) · STEP3 복셀 FV | **다름** — 접촉 협착 항은 우리만 있다 (FULL/CF = "모델 내부 협착 비") |
| τ 정의 | τ = ε·κ/κ_eff (Eq. 9) | **tau2** = φ_SE·σ₀/σ_eff | **정의식 같음** |
| 경계조건 · 측정 | 교류 · 차단 대칭셀 · 기공벽 이중층 sink (eSCM — τ_e 계열) | 직류 · 두 띠 Dirichlet 관통 (conventional) | **다름** — 둘이 같아지는 것은 dead-end 없고 균질할 때 (강구 실측 ≲ 4 %, §8-4) |
| 정규화 | A = 전극 면적 · t = 코팅 두께 · ε = 두께 + 적재량 (질량 수지 · 전 기공) | box_x·box_y · plate_z · φ_SE = 전 SE 구 부피 합 | **같은 계열** (질량 보존 φ).  우리 φ 는 겹침 이중계상 |
| σ₀ | κ = 액체 벌크 전도도 (센서, 25 °C) — 미세구조 없음 | σ₀ = 3.0 mS/cm = **펠릿값** (원장 CL-91) | **성격 다름** — 우리 tau2 는 "펠릿 대비" 상대량 |
| σ₀-불변 | R_Ion·κ 불변 (κ ×21–45) 을 **실험으로 확인** | 모든 망 저항 ∝ 1/σ → tau2 는 σ₀ 에 **정확히** 무관 (메모 v2 §3-1) | **같은 논리** — 메모 v2 §5-2 G4 시험 (σ_grain 두 값 → 비트 동일) 이 그 계산판 |
| 기준 기하 검증 | 강구 충전 ↔ Bruggeman ε^−0.5 (기공상) | 곧은 사슬 T_CF = (4/3)(r/d) (메모 v2 §3-6) · 순수 SE 게이트 (결정 4) | **같은 철학 · 반대 상** — Bruggeman 은 "절연 구 둘레의 전도 매질" 이다.  우리 망은 구 자신이 전도상이라 **닫힌 꼴 known-τ 가 없다** → 기준은 같은 침대의 복셀 연속체 해 (CL-81 복셀 ÷ 접촉망 대조) 가 되어야 한다 |
| 차단상 (CBD · 바인더) | XTM 이 못 보면 τ 를 1.5–2.3× 과소 · 바인더 1.5 → 10 wt% 에서 ×1.85 | DEM 접촉망엔 CBD 없음 · STEP3 는 PTFE centerline 스탬프만 (원장 CL-60) | **같은 방향의 결손** — CBD 가 있는 실제 전극 대비 우리 tau2 는 **과소** 쪽.  ⚠ Minnmann 전도도 시료는 바인더 · 탄소 없음 (메모 v2 §3-8) → 그 대조에는 해당 없음 · Park (NBR 2 wt%) 에는 해당 |
| 해상도 ↔ 대표 부피 | ~1 mm³ 를 보려면 325 nm 로는 CBD 미해상 | DEM: 접촉을 명시 (해상도 문제 대신 1세대 협착식 문제) · STEP3: vox 0.15 µm · d_h/dx ≥ 3.5 규칙 | **STEP3 가 같은 트레이드오프**에 있다 |
| 방향 | 관통 (XTM 값도 관통 방향) | z 관통 | **같음** |
| 입자 형상 | 실제 (판상 흑연 5.1 vs 구형 NMC 3.6) | 강체 구 | **다름** — 형상 · 이방성 효과는 우리 tau2 에 없다 |
| 실험 vs 모형 | EIS 를 "참값" 으로 두고 영상 τ 의 결손을 찾는다 | 각 모형을 실험에 따로 보정 (frame[4]) | 이 논문의 판정 구도 = "모형 (영상) τ 가 실험보다 낮으면 빠진 상을 찾아라" — 우리 SE 많은 띠 "판정 불가" (메모 v2 §3-8) 와 같은 질문 |

- ⚠ **비판적 한정 (주장 전에 먼저 걸리는 것)**: ① 액체 LIB → 전고체 전이 불가 (전도상 · 계면 · σ₀ 성격이 다르다) ② 강구 known-τ 는 **기공상** 검증이라 우리 **입자상** 망의 기준이 아니다 ③ "EIS = 참 τ" 는 균질 구 충전 한 기하에서만 시험됐다 — 실제 전극에서 τ_e 와 conventional τ 가 같다는 검증이 아니다 ④ Table II 비 (~2) 는 **tau2 척도**에서의 값이다 (√ 로는 1.2–1.5).
- **frame[5]**: 수송 절반만 가진 측정 논문 — 압밀 · 형상 · 기계 물리 없음.  우리 쪽에서는 DEM 접촉망 tau2 와 STEP3 복셀 tau2 (CF 계열) **둘 다** 이 정의로 읽힌다.  MPM 기계 쪽 대응 없음.
- **frame[4]**: 이 논문 수치로 우리 모델을 맞추지 않는다.  쓰는 것은 ① 척도 (tau2) · 측정 계열 (τ_e) 판정 ② "차단상을 빼면 τ 과소" 의 방향과 크기 감각 ③ σ₀-불변 · 기준 기하 검사의 설계뿐.

---

## § τ 정의 대조 — 우리 규약 매핑

> **우리 규약** (메인 리포 CLAUDE.md ★★ τ 명명 규약, 1저자 비준 2026-10-03): f = σ_eff/σ₀ (`f_ion_<mode>`) · **tau2** = φ·σ₀/σ_eff = φ/f (`tau2_ion_<mode>`) · tau = √tau2 (`tau_ion_<mode>`, 웹앱 τ_Lap,eff) · τ_geo = 최단 경로 / 두께 (`tau_geo_SE_dij`, 수송 τ 아님) · τ_e = electrode tortuosity factor (우리에 없음).  'tortuosity factor' 는 tau2 에만 쓴다.
> **우리 tau2 의 정체**: 간선 재료 σ₀ 3.0 mS/cm (펠릿값) 위에 SE–SE Holm 협착을 직렬로 더한 **접촉망 모델 tau2** (hertz 면적 = LIGGGHTS c_cpl[22] 교차 원판 · 반공간 Maxwell R_c = 1/(2σa) — 1세대 협착식).  CF 가지 = "모델 내부 기준선", FULL/CF = "모델 내부 협착 비".

| 이 논문 기호 · 식 (쪽) | 정의 · 정규화 (어느 부피 · 어느 단면) | 원문 이름 | σ₀ (κ) 기준 | 우리 다섯 양 중 | 환산 · 비고 |
|---|---|---|---|---|---|
| **τ** — Eq. 9 (A471) | τ = R_Ion·A·ε·κ/t · R_Ion = 한 전극의 기공 전해질 이온 저항 (간이 TLM) · A = 전극 (기하) 면적 · t = 코팅 두께 · ε = 두께 + 적재량에서 (전 기공, 막힌 기공 포함) | "tortuosity (τ)" — "factor" · "effective" 낱말 없음 | κ = 자가 조제 액체 전해질의 **벌크** 전도도 (LF 1100+ 센서, 25 °C) — 미세구조 없음 | **tau2** (정의식) — 측정 경로는 **τ_e 계열** (Nguyen: 차단 대칭셀 = eSCM) | f = ε/τ (= 1/N_M) · tau = √τ.  대칭셀 합 R 을 넣으면 /2 (2016 Eq. 13) |
| **τ = ε^−0.5** — Eq. 10 (A472) | Bruggeman, 구형 입자 (Ref. 12) | "Bruggeman relation" | — | tau2_Brug = φ^−½ ⇔ f_Brug = φ^1.5 (우리 망 `sigma_bruggeman`) | √ 관례로는 φ^−¼ · 2016 의 α = 0.5 표기와 같다 |
| **τ from EIS** — Table II (A474) | Eq. 9 · 대칭셀 · 반복 SD | "τ from EIS" | κ (위) | tau2 정의식 · τ_e 측정 | 저자 해석 = "true tortuosity" (conventional 과 동일시) |
| **τ from XTM** — Table II (A474) | 3D 재구성 (325 nm voxel, 이진화) 위 수치 확산, **관통 방향** · 식 미인쇄 (Refs 2 · 11) · 계산에 쓴 ε (분할 기공 vs 질량 수지) 미기재 | "τ from XTM" | 상대 확산 (재료 σ₀ 와 무관) | **tau2 — conventional flux** (판독: 같은 표 · 같은 기호 · Bruggeman ε^−0.5 와 같은 축에서 1.09–1.56 배) | ≈ 우리 STEP3 복셀 CF 형 · TauFactor mode 1 짝.  CBD 미해상 → "차단상 없는 연속체" |
| **R_Ion·κ** (A471) | 전극 고정 시 κ 에 무관해야 하는 곱 | — | — | (t/A)·(1/f) 의 상수배 — tau2/φ 에 비례 | 우리 G4 σ₀-불변 시험과 같은 논리 |
| **R_Ion^app · R_HFR^app** (A470–A471) | 간이 TLM 그래프법으로 일반 TLM 스펙트럼을 읽은 겉보기 값 | apparent | — | 없음 | 닫힌 꼴 §4-3 (파생) |
| τ_geo (기하 경로) | **이 논문에 없다** (2016 Eq. 3 τ_path 도 안 나온다) | — | — | 우리 τ_geo 대응 없음 | "geometric" 낱말은 기하 부피 · 기하학적 이유 문맥 2 회뿐 |
| τ_e (Nguyen 2020 명명) | — (논문 시점 이전의 이름) | — | — | 이 논문 EIS τ 의 **방법 계열** | 저자는 τ_e / conventional 을 구분하지 않는다 |

**척도별 같은 비교 (Table II, 파생)** — 같은 비가 척도에 따라 달라 보인다

| 전극 | tau2 비 (원문 척도) | tau (√) 비 | N_M 비 | f 비 (EIS/XTM) | 단서 |
|---|---|---|---|---|---|
| NMC (ε 0.40) | **1.75** | 1.32 | 1.75 | 0.57 | N_M 비 = tau2 비는 **두 방법이 같은 ε 를 쓸 때만** — 표에는 다공도 열이 하나뿐 [XTM 분할 다공도 미기재] |
| NCA (ε 0.40) | **2.31** | 1.52 | 2.31 | 0.43 | 〃 |
| 흑연 (ε 0.51) | **1.51** | 1.23 | 1.51 | 0.66 | 〃 |

**판정**
1. 이 논문 τ (Eq. 9) = 2016 τ = 우리 **tau2** — 같은 정의식 · 같은 정규화 (전체 면적 · 전체 두께 · 질량 수지 ε · 관통).  Bruggeman 을 ε^−0.5 로 쓴 것이 척도를 확정한다.
2. 측정 경로는 **차단 대칭셀 EIS (eSCM)** = Nguyen 의 **τ_e 계열**이고, 우리 tau2 는 **conventional (두 띠 관통)** 이다.  균질 · 관통 구조에서만 같은 값이 된다 (§8-4).
3. Table II 의 "τ from XTM" 은 conventional flux tau2 로 읽는다 (판독 — 식이 원문에 없다).  ⇒ Table II 는 **τ_e-계열 실험 ↔ conventional 연속체 계산 (차단상 없음)** 의 대조다.
4. σ₀ 는 액체 벌크 κ — **미세구조 · 내부 계면이 없는 기준**.  우리 3.0 (펠릿) 과 성격이 달라 tau2 절대값을 맞대기 전에 기준 상태부터 맞춘다 (메모 v2 결정 4).
5. ⛔ "~2 배" 를 인용할 때는 **척도를 붙인다** — tau2 로 1.5–2.3, tau (√) 로 1.2–1.5.

---

## 8. ★ 같은 전극의 임피던스 τ ↔ 단층촬영 τ 직접 대조 (이 묶음이 닫는 항목) + 적용 인사이트

### 8-1. 실측 크기 — 전극별 표 (Table II, A474 · 파생 열은 카드 계산)

| 전극 (Custom Cells) | ε | t (µm) | 적재 · AM % | τ_XTM (tau2) | τ_EIS (tau2) | **EIS / XTM** | XTM / Brug | EIS / Brug | N_M XTM / EIS (같은 ε 가정) |
|---|---|---|---|---|---|---|---|---|---|
| NMC111 | 0.40 | 125 | 3.5 mAh/cm² · 24.1 mg/cm² · 86 % | 1.77 ± 0.06 | 3.1 ± 0.3 (4) | **1.75** (± 0.18) | 1.12 | 1.96 | 4.43 / 7.75 |
| NCA | 0.40 | 115 | 3.5 · 21.6 · 90 % | 1.73 ± 0.03 | 4.0 ± 0.05 (2) | **2.31** (± 0.05) | 1.09 | 2.53 | 4.33 / 10.0 |
| 흑연 | 0.51 | 110 | 3.8 · 10.9 · 96 % | 2.18 ± 0.06 | 3.3 ± 0.05 (2) | **1.51** (± 0.05) | 1.56 | 2.36 | 4.27 / 6.47 |

- Bruggeman tau2 = ε^−0.5: ε 0.40 → 1.581 · 0.51 → 1.400.  ± 는 표 SD 의 1차 전파 (XTM 은 문턱 불확도만 · EIS 는 n = 2–4) — **과소 추정된 불확도**, 참고용.
- 원문 요약 (A474): *"XTM-derived tortuosities are in the range of 1.7 to 2.2 for all electrode types, the EIS-derived values are ~2-fold larger, ranging between 3.1 and 4.0 (the largest discrepancy of a factor ~2.3 is found for the NCA electrodes)"*.
- 카드 관찰 (파생): ① XTM 은 구형 NMC · NCA 에서 Bruggeman 에 가깝고 (1.09–1.12×) 판상 흑연에서만 위 (1.56×) — **입자 형상 (이방성) 은 해상**하고 있다.  ② EIS 는 세 전극 모두 Bruggeman 의 ~2–2.5 배.  ③ EIS/XTM 비가 **비활성 분율과 단조 관계가 아니다** — 흑연 (4 %) 1.51 < NMC (14 %) 1.75 < NCA (10 %) 2.31.  바인더 : 탄소 구성이 원문에 없고 n = 3 이라 "CBD 양 ∝ 격차" 를 시험할 수 없다.
- 같은 묶음의 다른 값 (조건이 다른 전극, 비교용): Fig. 3 NMC (ε 0.42) EIS 3.6 = Bruggeman 의 2.33× · 흑연 (ε 0.43) 5.1 = 3.34× · 바인더 실험 1.5 % → 1.95× · 10 % → 3.56× (파생).

### 8-2. 어긋남의 원인 분석 — 후보별 증거와 판정

| 후보 | 이 논문의 증거 (쪽) | 저자 판정 | 카드 평가 |
|---|---|---|---|
| 전극 **전자 저항** | 일반 TLM (Fig. 1 · 2) + κ-불변 (Fig. 3; NMC κ ×45 · 흑연) (A470–A472) | 배제 (NMC · 흑연) | **방향상 EIS > XTM 을 만들 수 없다** — x < ~1 에서 R_El 은 겉보기 R_Ion 을 **줄인다** (§4-3).  ⚠ Table II 세 전극 자체의 κ-불변은 제시 안 됨 (Fig. 3 NMC 는 다른 NMC 전극 · NCA 는 시험 없음) |
| **TLM 모형** 오류 | 강구 τ 1.56 vs 1.60–1.62 (A473) | 배제 | 균질 · 단분산 · 관통 · 한 κ · 한 기하에서의 검증 — 실제 전극의 dead-end · 구배는 시험 밖 |
| **이온–기공벽 상호작용** (Ref. 13) | 10 mM–1 M 에서 τ 불변 (Fig. 3) · 표면 ~100 vs 필요 > 2500 cm²/cm²_El (A474) | 배제 — *"cannot account for the observed factor of ~2"* | 산술 정합: 1.5 µmol × π(0.3 nm)² ≈ 2.55×10³ cm² (파생 — 원문 "(1.5 µM)" 를 µmol/cm²_El 로 읽을 때; 원문 단위 표기 그대로 [판독]) |
| **XTM 해상도 → CBD 미해상** | 325 nm · ~1 mm³ · 문헌: 흑연 XTM 저 τ @0.56 µm (Ref. 15) · FIB-SEM 의 CBD 불균일 분포 (Ref. 16) · CBD 를 계산으로 넣으면 τ ↑ (Ref. 18) (A474) | **가장 유력** — *"the most likely reason for the underestimation"* | 바인더 실험은 **EIS 만** — 같은 바인더 시리즈의 XTM 을 재서 "XTM 은 바인더에 맹" 을 직접 보이지 않았다 (추론) |
| **바인더 분포** | 1.5 → 10 wt% PVDF: τ_EIS 2.7 → 5.0 at ε 51/50 % (A474–A475) | 지지 증거 — *"could explain the difference"* | 부피 1–5 % 로 ×1.85 → 바인더의 **위치** (목 · 다리) 효과.  1.5 % 전극 2.7 은 Table II 흑연 XTM 2.18 의 1.24× (다른 흑연 · 다른 시편 — 교차 비교, 참고만) |
| **이진화 문턱** | ±0.03–0.06 (Table II) | 작음 | 2 배를 못 만든다 |
| **대표 부피 (RVE)** | 고해상 FIB-SEM 의 MCMB 2–7 은 15 µm 큐브 (입자 ~8 µm) 라 비대표 (Ref. 17, A474) | 해상도 ↔ 부피 트레이드오프 | 우리 STEP3 와 같은 문제 (§7) |
| **이방성** | XTM 보고값 = 관통 (A474) · 흑연 판상 5.1 vs NMC 3.6 (A472) | Table II 격차의 원인으로 들지 않음 (방향 일치) | 가스 투과 (**면내**) τ ~6 을 EIS (**관통**) ~5.5 와의 "good agreement" 로 든 것은 방향 · 정의 (투과 모형) 가 다르다 — 판상 흑연은 면내 τ < 관통 τ (2016 카드: FIB-SEM 관통 ≈ 면내 2 배) 라 독립 확인으로 약하다 |
| **정의 차 τ_e vs conventional** (논문 밖 — Nguyen 2020) | 논문이 다루지 않음 · 강구에서 ≲ 4 % | — | CBD 가 기공 목을 막아 dead-end 를 만들면 실제 전극의 τ_e/τ 는 1 에서 벗어날 수 있다 (크기 · 부호 미상) → **2 배의 일부일 수 있으나 분리 불가** |
| **시편 차** (같은 코팅 · 다른 조각 · ~1 mm³ vs 원판) | — | — | 미정량 |

- 방향이 **반대**인 사례 (다른 카드): `taufactor_tortuosity_factor_tomography_tool` 역링크 절 — Duquesnoy 2020 (1 µm voxel 에 CBD 를 그림) 의 TauFactor τ 가 같은 그룹 EIS τ_TLM 의 2.4–2.7 배 (**영상 쪽이 높다**).  ⇒ 영상 τ 의 편향 부호는 CBD 를 **기공으로 세느냐 (이 논문 → 과소) · 굵은 voxel 로 그려 기공을 막느냐 (→ 과대)** 에 달려 있다 (카드 판단).  두 카드의 척도 · 상 정의를 맞추기 전에는 크기를 섞지 않는다.

### 8-3. 어느 τ 척도로 비교하는가
- **원문 비교 척도 = tau2** (τ = ε·N_M, Eq. 9 · Bruggeman ε^−0.5).  EIS 와 XTM 을 같은 기호 τ 로 한 표에 놓는다.
- 같은 결과를 √ 척도 (tau, τ² 관례의 τ) 로 쓰면 **1.23–1.52 배**, N_M 로 쓰면 tau2 와 같은 비 (같은 ε 일 때만), f 로 쓰면 역수 (0.43–0.66).
- ⇒ 인용 규약: *"tau2 (tortuosity factor) 척도에서 EIS/XTM 1.5–2.3"* — 척도 없이 "2 배" 라 쓰지 않는다.

### 8-4. 결정 13 (τ_e ↔ conventional τ) 에 대한 답
- **Q. τ_e ↔ conventional τ 의 차이를 실측으로 얼마로 보나?**
  - 이 논문은 둘을 **구분하지 않는다** (Nguyen 2020 이전) — EIS 값을 "true tortuosity" 로, XTM 값을 같은 양의 과소 추정으로 본다.
  - Table II 의 EIS/XTM = 1.51–2.31 은 **[τ_e/τ]_실제 × [τ_실제/τ_XTM]** 의 곱이고, 저자는 뒤 인자 (CBD 미해상) 에 귀속한다 ⇒ **τ_e/τ 의 실측값으로 쓸 수 없다**.
  - 유일한 깨끗한 실측 = **강구** (균질 · 단분산 · 전부 관통 · CBD 없음): τ_EIS/τ_Brug = **0.962–0.974**.  그 −3 % 안에는 정의 차 · Bruggeman 근사 오차 · 벽 효과 (원문) · 전자 저항 몫 (≤ −2 %, §4-5 파생) 이 섞여 있다 → **정의 차 상한 ≈ 4 %** 로만 쓴다.
  - Nguyen Fig. 5 (잘 퍼콜된 구 충전 모사 +0.8 / +3.9 %) 와 **크기는 정합, 부호는 반대** (−3 % vs +).
- **Q. "P2D 입력으로는 부호 불정" 한정어가 유지되는가?** → **유지된다.**  이 논문은 dead-end · 구배 · CBD 막힘 구조에서 τ_e 와 conventional τ 를 **같은 해상된 구조**로 비교한 값을 주지 않고, 유일한 깨끗한 점의 부호도 Nguyen 모사와 반대다.
- 덧붙일 문장 (권고를 바꾸지 않는 보강): *"균질 · 관통 구 충전에서는 차단 대칭셀 EIS τ (τ_e 계열) 가 conventional (Bruggeman) tau2 와 ≲ 4 % 안에서 같다 (실측 1 기하 · 액체 기공상)."*

### 8-5. 메모 v2 §7 (τ_e 공백) 에 주는 것
- ① §7 의 "τ_e = T 에는 dead-end 없음 + z 균질이 필요" 의 **실험 쪽 근거** — 그 조건이 충족된 기하 (강구) 에서 실측 일치 (≲ 4 %).  조건이 깨진 기하의 실측은 이 논문에 없다.
- ② ASSB 실험 앵커 분기 (Bazzoun = eSCM 형 · Minnmann = 관통형, 메모 §7 마지막 행): 이 논문의 **R_El/R_Ion < 10⁻² 창은 간이 TLM (eSCM 형) 앵커에 걸린다**.  ASSB 복합체에서 x = σ_ion,eff/σ_el,eff (같은 L · A 면 R_El/R_Ion = σ_ion,eff/σ_el,eff) — Minnmann SI Table S2 (`minnmann2021_…` 카드 §5) 로 계산하면 (카드 산술) **19.8 · 1.13 · 0.30 · 0.031 · 0.0021** @ 25/33/42/53/61 vol% NCM → 간이 TLM 이었다면 **61 vol% 만 창 안**.  Minnmann 자신은 두 레일 T-type TLM 으로 R_el · R_ion 을 함께 맞춰 이 함정을 피한다 (그 카드 기술).  ⇒ Bazzoun 같은 eSCM 형 앵커는 그 복합체의 σ_el,eff 를 함께 확인한 뒤에 쓴다.
- ③ κ-불변 검사는 **염 농도로 κ 를 바꿀 수 있는 액체에서만** 가능하다.  ASSB 에서 SE 의 σ 를 바꾸는 손잡이 (온도) 는 σ_el 도 바꾼다 (카드 판단) → ASSB eSCM 앵커는 전자 저항 창을 이 방식으로 확인하기 어렵다.

### 8-6. Minnmann 2021 "LIB tortuosity factor 는 한 자릿수 낮다" (p.9, ref 61 = 이 논문) — τ² 척도인가 τ 척도인가
- ⚠ Minnmann 원문 p.9 문장은 **이 카드에서 미열람** (PDF 가 이 작업 환경에 없다) — `minnmann2021_jes_charge_transport_bottlenecks` 카드 참고문헌 [61] 행의 요약을 기준으로 판단한다.
- 이 논문이 주는 LIB 값은 **전부 tau2 척도** — EIS 2.7–5.1 (Table II 3.1–4.0 · Fig. 3 3.6 / 5.1 · 바인더 2.7 / 5.0) · XTM 1.73–2.18.  Minnmann 의 τ_ion² 도 tau2 (= φσ₀/σ_eff, 보고값 꼴) ⇒ **이 논문 숫자를 그대로 가져와 Minnmann τ² 와 비교했다면 같은 척도 비교다.**
- 같은 척도에서 크기 (카드 산술, Minnmann τ_ion² ÷ 이 논문 EIS 2.7–5.1): 25 vol% 2.40 → **0.47–0.89** · 33 vol% 3.23 → 0.63–1.2 · 42 vol% 4.27 → 0.84–1.6 · 53 vol% 15.3 → **3.0–5.7** · 61 vol% 130 → **25–48** · 61 vol% fine SE 33.8 → **6.6–12.5**.
  ⇒ "한 자릿수" 는 **61 vol% 대비에서만** 성립한다.  25–42 vol% 와는 같은 자릿수 (EIS 값이 오히려 크다).
- 추가 한정: ① 전도상 분율이 다르다 (LIB ε 0.40–0.51 ↔ Minnmann φ_SE 0.25–0.61) — 같은 φ 비교가 아니다.  ② σ₀ 기준이 다르다 (액체 벌크 κ ↔ Minnmann 순수 SE 펠릿 1.6 mS/cm ≡ τ² 1).  ③ 만약 √ 값 (Minnmann τ_ion 1.55–11.4) 을 이 논문 tau2 와 맞댔다면 척도 혼합이다 — Minnmann 문장의 실제 대상 수치를 원문에서 확인할 것.

### 8-7. 결정 16 묶음에 주는 인사이트 (결정 번호 · 권고 변경 여부)

| 결정 | 인사이트 | 권고 변경 |
|---|---|---|
| **13** (τ_e) | 이 논문의 EIS ↔ XTM 2 배는 τ_e/τ 가 아니라 CBD 해상도 차 (저자 귀속).  깨끗한 점 (강구) 은 정의 차 ≲ 4 % · 부호는 Nguyen 모사와 반대 → "부호 불정" 유지 · "ML 기술자 문장으로만" 유지 | **no** (보강 문장만) |
| **4 · 11** (순수 SE 게이트 · CF 지위) | 이 논문의 설계 = **해석 전에 τ 를 아는 기준 기하로 측정 사슬을 검증**.  우리도 같은 순서가 맞다 (순수 SE 게이트 · 곧은 사슬).  단 Bruggeman 은 **기공상** 기준이라 우리 입자상 망의 known-τ 가 아니다 → 기준은 같은 침대 복셀 연속체 해 (CL-81 대조) 이고, 그 대조에 CF 과전도 (× 1/(0.6–0.8)) 를 사전등록하는 결정 11 이 그 자리다 | **no** (지지) |
| **5** (COMSOL/EIS 표기) | EIS τ 는 tau2 척도 (Eq. 9 · 10) 이고 측정 계열은 τ_e → √T 에 "EIS input" 은 척도도 계열도 틀린다.  tau2 열에도 "EIS 와 같다" 는 τ_e 한정어 없이 쓰지 않는다 | **no** (지지) |
| 3-4 한정어 (Park NBR 2 wt%) | 바인더 1.5 → 10 wt% 에서 τ ×1.85 (액체 흑연) — Park 실험 tau2 가 바인더로 올라가는 방향의 크기 감각 (액체 → ASSB 전이 불가) | no |
| **14** (전자 · 열) | Eq. 1 일반 TLM 에서 한 셀의 겉보기 HFR = R_El·R_Ion/(R_El + R_Ion) — 두 레일이 섞인다.  전자 f · tau2 의 실험 앵커는 이온 차단 셀 (Minnmann 식) 에서 따로 잰 값만 쓴다 | no |

### 8-8. 적용 인사이트 (일반)
- ① ★ **σ₀-불변 자기검사** (Fig. 3 의 계산판) — 같은 침대를 σ_grain 두 값으로 풀어 tau2 가 비트 수준으로 같아야 한다 (메모 v2 §5-2 G4).  이 논문은 액체에서 같은 원리를 **실험 검사**로 썼다.
- ② ★ **기준 기하 먼저** — 실제 전극을 해석하기 전에 τ 를 아는 기하에서 사슬을 검증한다.  우리 망에는 닫힌 꼴 known-τ 가 없으므로 같은 침대의 복셀 연속체 해 · 곧은 사슬 해석해가 그 자리다.
- ③ ★ **차단상을 빼면 τ 과소** — 영상/모형이 CBD 를 기공으로 세면 tau2 가 1.5–2.3× 낮아질 수 있다 (액체 LIB).  우리 DEM tau2 를 바인더 · 탄소가 있는 실험 전극과 맞댈 때 같은 방향의 결손을 먼저 적는다.
- ④ **ASSB EIS 앵커 선택** — 간이 TLM 값이면 x = σ_ion,eff/σ_el,eff < 10⁻² 를 확인한다 (§8-5 ②).  아니면 두 레일 TLM 값 (Minnmann) 을 쓴다.
- ⑤ **문헌 R_Ion 재사용 시 전극 수 규약** (전극 하나 vs 대칭셀 합) 을 확인한다 — 이 논문 안에서도 절마다 다르다 (§4-1).
- ⑥ **"~2 배" 류 인용엔 척도** — tau2 1.5–2.3 ↔ tau 1.2–1.5.

## 9. 인용 가능 문장 (deck/paper용)
- "Landesfeind et al. (J. Electrochem. Soc. 165, A469, 2018) validated the blocking-electrolyte symmetric-cell impedance method on a packing of 1 mm steel spheres (ε ≈ 0.385), obtaining τ = 1.56 against the Bruggeman value of 1.60–1.62; their τ = R_Ion·A·ε·κ/t carries no square, i.e. it is the tortuosity factor."
- "For electrodes cut from the same coatings, impedance-derived tortuosities (3.1–4.0) exceeded X-ray tomography values (1.73–2.18; 325 nm voxels, through-plane) by factors of about 1.5–2.3 on the tortuosity-factor scale; the authors attribute the gap mainly to binder and carbon phases not resolved by tomography, supported by an increase from τ = 2.7 to 5.0 when the PVDF content of a graphite electrode was raised from 1.5 to 10 wt%."
- "On the square-root (τ² convention) scale the same tomography-versus-impedance gap is only about 1.2–1.5, so such factors must be quoted together with the tortuosity scale."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **액체 전해질 LIB** (TBAClO₄ · EC 계 용매 · PVDF/탄소 전극).  LPSCl 전고체로 **수치 전이 불가** — 쓰는 것은 척도 · 측정 계열 판정 · 검사 설계 · 방향 감각뿐 (§7).
- ⚠ **"EIS = 참 τ" 의 검증 범위** — 강구 한 기하 (단분산 1 mm · ε 0.385 · 균질 · 전부 관통 · κ 한 값) 뿐.  실제 전극 (dead-end · 구배 · CBD) 에서 차단 대칭셀 τ 가 conventional τ 와 같다는 검증이 **아니다** (결정 13).
- ⚠ **원인 결론은 추론** — 바인더 실험은 EIS 만 했다 (같은 시리즈의 XTM 없음).  원문 표현도 *"most likely"* · *"could explain"* (A474–A475).
- ⚠ **XTM τ 의 식 · 계산 ε 가 원문에 없다** (Refs 2 · 11 미열람) → XTM 값을 tau2 로 읽은 것은 판독이다.  N_M 비 = tau2 비는 두 방법의 ε 가 같을 때만.
- ⚠ **Table II 세 전극 자체의 κ-불변 검사 미제시** — Fig. 3 의 NMC 는 다른 NMC 전극 (ε 42 % · 72 µm · 2 mAh/cm²) 이고 NCA 는 시험이 없다.  단 R_El 은 x < ~1 에서 EIS τ 를 **낮추는** 방향이라 EIS > XTM 결론을 뒤집지는 못한다 (§4-3).
- ⚠ **불확도 과소** — XTM ± 는 이진화 문턱만, EIS ± 는 n = 2–4 의 SD.  RVE · 시편 차 · 분할 모형 오차는 들어 있지 않다.
- ⚠ **2016 ↔ 2018 흑연 평균 불일치** — 2018 Fig. 3 은 흑연을 *"same as in Figure 14 of Ref. 5"* 라 적으면서 평균 **5.1 ± 0.8** 을 보고한다.  2016 원문 (2016 카드 §5-4) 의 Fig. 14 평균은 **4.3 ± 0.6** (1.19 배 차이), 그림의 점 수도 달라 보인다 (판독).  원인 [미확인] — 2016 카드 머리말이 적은 정오표 (미열람) 와의 관계도 [미확인].  **흑연 4.3 · 5.1 을 서로 바꿔 쓰지 않는다.**
- ⚠ **가스 투과 비교의 방향 불일치** — 면내 가스 투과 τ ~6 (Ref. 14) 을 관통 EIS ~5.5 의 "good agreement" 로 든 것은 방향 · 정의가 다르다 (§8-2).
- ⚠ **원문 표기 · 내부 불일치** (원문 그대로 두고 표지만):
  - 벽 효과 문장 (A473–A474) *"the porosity … is slightly lower close to the … walls where the packing is less dense"* — 덜 조밀한 충전이면 다공도는 **높다**.  뜻 (벽 근처 저항 ↓ → τ ↓) 으로는 "higher" 가 맞다.
  - Fig. 1 캡션 · A471 본문의 *"Z_S … described by Eq. 6"* — Z_S 식은 **Eq. 8** 이다 (Eq. 6 은 ν).
  - A474 *"indicated in Table III parentheses"* — 표는 **Table II** 뿐이다.
  - Experimental (A470) 흑연 바인더 시험 전극 *"ε = 48 %, t = 90 µm, ~3 mAh/cm² (8.6 mg/cm²)"* ↔ Fig. 6 본문 51 % · 109 µm / 50 % · 85 µm.
  - A472 *"changed over ~1.8 decades"* (NMC 문장) — NMC 범위 0.156–6.97 은 1.65 decade (×45), 흑연까지 합친 0.156–9.56 이 1.79 decade (파생).
  - A471 *"ratios of the ionic to electronic resistances (R_El/R_Ion)"* — 기호는 전자/이온 비.  A472 *"apparent ionic resistance d R^app_Ion·κ"* 의 "d" 는 오식으로 보인다.
  - Fig. 6 가로축 "Re(Z − Z₁)" 의 Z₁ = HFR 인데 Eq. 2 의 Z₁ = R_El — 기호 충돌.
  - 바인더 *"(1% – 5%)"* 는 질량 분율 (1.5–10 wt%) 과 맞지 않는다 (부피로는 카드 추정 ≈ 0.9–6 %, 밀도 가정).
  - R_Ion 의 전극 수 규약이 절마다 다르다 (§4-1).
- ⚠ Fig. 3 판독값 (NMC 고 κ 쪽 ~0.5 높음) 은 TREND 전용 — 원문은 평균 ± 만 적는다.
- **메모 v2 정정 후보** (`docs/reviews/tau_conventions_judgment_v2_20261003.md`, 메인 리포):
  1. **§8-1 상위 10 · 4 순위 "왜 필요한가"** 의 *"같은 전극의 임피던스 τ ↔ 단층촬영 τ — 정의 · 방법 차이의 실측 크기"* → **"방법 (해상도 · CBD) 차이의 실측 크기 — 정의 차 (τ_e vs conventional) 는 이 논문에서 분리되지 않음 (저자는 두 값을 같은 양으로 취급, A474 · 귀속 = 미해상 바인더 · 탄소 A474–A475)"**.  같은 행의 "같은 전극" → "같은 코팅에서 자른 전극 (Table II 캡션 'same type of electrodes', A474 · Conclusions A475)".
  2. **§8 머리 · 8-1 표 OA 칸** *"카드 기록 없음"* (이 서지) → **"CC BY-NC-ND 4.0 (A469)"** — 이 카드가 기록.
  3. (보강 · 정정 아님) **§3-5 Bruggeman 배수 행** *"액체 전극 ≈ 1.5–3× (Landesfeind A1386)"* 는 2016 문장으로 맞다.  같은 저자군 2018 값은 Table II **1.96–2.53×** · Fig. 3 흑연 **3.34×** · 10 % 바인더 **3.56×** (A472–A475, 파생) — 3× 를 넘는 값이 있다.
  4. (보강) **§7** "τ_e = T 조건" 행에 실험 근거 한 줄 — 강구 충전 τ_EIS/τ_Brug 0.962–0.974 (A473, 파생).
- **형제 카드 정정 후보** (이 카드는 수정하지 않았다): `nguyen2020_electrode_tortuosity_factor` §11 ref 29 행 *"정의 차의 실측 크기"* → 위 1 과 같은 이유로 "방법 (해상도 · CBD) 차의 실측 크기 — 정의 차 분리 안 됨".  `landesfeind2016_…` §14 끝 줄 *"(내용 미확인)"* · `minnmann2021_…` 참고문헌 [61] 행 "❌" → 이 카드로 해소 가능 (링크 갱신은 메인).

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 원문 ref | 목록 서지 (그대로) | 왜 볼 만한가 |
|---|---|---|
| 2 | M. Ebner, F. Geldmacher, F. Marone, M. Stampanoni, and V. Wood, Adv. Energy Mater., 3, 845 (2013). | Table II XTM τ 의 방법 — **XTM τ 의 식 · 척도 (tau2 인지) · 계산 ε 정의** 를 닫는다 (이 카드의 남은 판독) |
| 11 | M. Ebner, D. W. Chung, R. E. García, and V. Wood, Adv. Energy Mater., 4, 1 (2014). | 같은 목적 + 입자 이방성 → 관통 τ (2016 카드 ref [32] 와 같은 서지) |
| 7 | H. Göhr, in Electrochemical Applications, p. 2, ZAHNER-elektrik GmbH & Co. KG (1997). | Eq. 1 일반 TLM (두 레일) 의 출처 — ASSB 처럼 r_el ≪ r_ion 이 안 설 때 |
| 18 | L. Zielke, T. Hutzenlaub, D. R. Wheeler, I. Manke, T. Arlt, N. Paust, R. Zengerle, and S. Thiele, Adv. Energy Mater., 4, 1 (2014). | 재구성에 바인더/탄소를 **계산으로 넣으면** τ 가 EIS 쪽으로 오른다 — 우리 CBD 없는 망에 차단상을 더하는 방법 |
| 16 | L. Zielke, T. Hutzenlaub, D. R. Wheeler, C. Chao, I. Manke, A. Hilger, N. Paust, R. Zengerle, and S. Thiele, Adv. Energy Mater., 1 (2014). | 고해상 FIB-SEM 의 CBD **불균일 분포** — 균일 분포 가정의 위험 |
| 17 | F. Tariq, V. Yufit, M. Kishimoto, P. R. Shearing, S. Menkin, D. Golodnitsky, J. Gelb, E. Peled, and N. P. Brandon, J. Power Sources, 248, 1014 (2014). | MCMB 고해상 τ 2–7 · 15 µm 큐브 — RVE 부족의 경고 사례 |
| 15 | C. Lim, B. Yan, L. Yin, and L. Zhu, Energies, 7, 2558 (2014). | 흑연 XTM (0.56 µm voxel) 도 낮은 τ — 해상도 의존의 두 번째 점 |
| 14 | T. DuBeshter, P. K. Sinha, A. Sakars, G. W. Fly, and J. Jorne, J. Electrochem. Soc., 161, A599 (2014). | 가스 투과 (면내) τ — 다른 정의 · 방향의 τ (§8-2 의 방향 불일치 확인용) |
| 13 | M. F. Lagadec, M. Ebner, R. Zahn, and V. Wood, J. Electrochem. Soc., 163, A992 (2016). | 이온–기공벽 상호작용 주장 (이 논문이 반박) |
| 3 | J. Joos, T. Carraro, A. Weber, and E. Ivers-Tiffée, J. Power Sources, 196, 7302 (2011). | 3D 재구성 수치 τ 의 다른 계열 (Ref. 2 와 함께 "영상 τ" 쪽) |
| 6 | D. Cericola and M. E. Spahr, Electrochim. Acta, 191, 558 (2016). | EIS 대칭셀 τ 의 다른 그룹 (Ref. 4 · 5 와 함께 EIS 계열) |
| 4 | N. Ogihara, S. Kawauchi, C. Okuda, Y. Itou, Y. Takeuchi, and Y. Ukyo, J. Electrochem. Soc., 159, A1034 (2012). | 대칭셀 TLM 원법 (2016 카드 §14 와 같은 서지) |
| 5 | J. Landesfeind, J. Hattendorff, A. Ehrl, W. A. Wall, and H. A. Gasteiger, J. Electrochem. Soc., 163, A1373 (2016). | 정의 정본 — 카드 `landesfeind2016_tortuosity_eis_electrodes_separators` |
| 12 | D. A. G. Bruggeman, Ann. Phys., 416, 636 (1935). | Eq. 10 의 출처 (2016 카드 [17] 은 "Ann. Phys, 24, 636 (1935)" 로 권수 표기가 다르다 — 서지 표기 차 [미확인]) |

## 🔗 이 논문과 함께 읽을 corpus 카드
- `landesfeind2016_tortuosity_eis_electrodes_separators` — 정의 · 측정법 정본 (N_M · τ = ε·N_M · TLM-Q · 비삽입 염).  2018 Fig. 3 흑연 자료의 원본 (평균 불일치 §10).  그 카드 §5-5 의 "재구성 τ 는 CBD 미해상 탓에 낮을 수 있다" 가설을 이 논문이 같은 코팅으로 시험했다.
- `nguyen2020_electrode_tortuosity_factor` — 이 논문 = ref 29.  차단 대칭셀 = eSCM = τ_e 계열 분류 · 잘 퍼콜된 구 충전에서 τ_e ≈ τ (≤ 4 %) 모사 — 강구 실측 (§8-4) 과 크기 정합.
- `minnmann2021_jes_charge_transport_bottlenecks` — 이 논문 = ref [61] ("한 자릿수 낮다" 의 근거, §8-6) · 두 레일 T-type TLM (§8-5 ②).
- `tjaden2018_tortuosity_review_calculation_approaches` — 실험 τ 는 그 실험 모형의 적합 매개변수 · flux ≥ 기하.
- `taufactor_tortuosity_factor_tomography_tool` — 영상 기반 conventional tau2 의 도구 · Duquesnoy 역링크 (영상 τ 가 EIS 보다 **높았던** 반대 방향 사례, §8-2).
- `duquesnoy2020_calendering_ml_mesostructure_generator` · `ngandjong2021_dem_calendering_digital_twin` — 같은 EIS-TLM 계열 τ 를 쓰는 corpus 카드 (척도 확인은 각 카드에서).
- `bazzoun2026_dem_fem_rnm_ionic` — ASSB 완전 차단 대칭셀 앵커 (eSCM 형) — §8-5 ② 의 x 창 확인 대상.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

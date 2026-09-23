---
title: "Sinzig, Schmidt, Wall 2024 — Analysis of the Validity of P2D Models for Solid-State Batteries in a Large Parameter Range (J. Electrochem. Soc. 171, 120519)"
source_url: local-upload/26._Analysis_of_the_Validity_of_P2D_Models_for_Solid-State_Batteries_in_a_Large_Parameter_Range.pdf
source_url_note: "14쪽(IOP 표지 1 + 본문 13, 참고문헌 53편), SI 없음. 크로퍼가 본문 그림 15장을 잡았다(표는 크롭 안 됨) — 15장 전부 직접 봤다, 안 본 그림 0장. 식·표·부록은 쪽 렌더 26장(170 dpi 반쪽)으로 읽었다. Fig. 3b·7·9a·11a·14b 는 벡터 경로 좌표를 추출했다. PDF 는 커밋하지 않는다."
source_doi: 10.1149/1945-7111/ad9a05
source_license: "CC BY 4.0 (지면 표기)"
pdf_sha256: 17507c15ac7554443cb5d052ad6ed76e2a2d9c4dc129ccbe96938adabb160ee6
ingested: 2026-09-23
sha256: 5b9137e08c9a0457e2d684dc79b6903742e3ab5629d622585b3aced966fab489
---

# 수집 목적

`assb` 섹션 **27호**. 큐 **26번** (26호 = 큐 25 Iwakiri 2024, 25호 = 큐 24 Zhou 2025). 닻은 `questions/assb-contact-loss-vs-lampe.md`.
큐 문서(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-c)의 등록 축은 **"Q4 확인용"**이고, 25~29 낱말 지문 표는 이 편을 **"전역 민감도를 제대로 한다"** 로 적었다:
`identifiab` **0** · `uniqu` **0** · `sensitiv` 26 · `Sobol` **29** · `GITT` 0 · `OCV` **0**.

**원문 14 쪽(표지 1 + 본문 13)을 전수로 다시 셌다.** 원문 PDF 는 `ﬁ` **합자**(U+FB01)를 쓴다 — 추출 텍스트 그대로 세면 `identifiab` 는 0 이 맞지만, **NFKC 정규화 뒤에는 1** 이다.
그 1 회는 `[인쇄]` "As all relevant phenomena and interactions are already **identifiable** during the first discharge" — **현상**이 첫 방전에서 보인다는 뜻이지 파라미터 식별성이 아니다.
`identif*` 는 합자 그대로 3 · 정규화 뒤 **10** — 전부 "영역을 identify 한다" · "최적 셀을 identification" 류. 나머지 지문: `uniqu` 0 · `sensitiv` 26 · `Sobol` 29(참고문헌 51 의 저자명 1 포함 → 본문 28) ·
`GITT` 0 · `OCV` 0 · `open circuit` 1(Table VI 행 이름) · `Fisher`·`Hessian`·`Jacobian`·`covarian`·`correlat`·`profile`·`bootstrap`·`degenera`·`non-unique`·`Morris` **전수 0** ·
`confidence` 2(둘 다 Sobol 지수의 95 % CI) · `calibrat` 2 · `fit`(정규화 뒤, "profit" 제외) 1 — `[인쇄]` "Different studies are available to **fit** the parameters of the P2D model to experimental results.[27,28]" ·
`contact` **0** · `utilization` 6 · `degrad` 1 · `pressure` 1 · `experiment` 3(전부 "실험이 없는 영역" 류). ⇒ **큐 지문은 합자를 뺀 채로 맞다. 지문 도구의 맹점 하나: IOP/ECS 조판의 `ﬁ` 합자** (§11 끝).

> ★★★★ **Q4 판정을 먼저 적는다.**
> 1. **세 층 중 어디인가 — 첫 줄(설계 민감도)이다. 단 전역으로 제대로 한 첫 편이고, 표에 없던 줄 하나를 더 만든다.** 출력은 **`SOC_end`**(방전 끝 양극 SOC, 스칼라 하나) — 방전곡선도 오차도
>    데이터 적합도 아니다. 입력 4 개(`σ` 전자전도도 · `κ` SE 이온전도도 · `D` 양극 확산계수 · `N_ρ` 외부 전류)를 Table IV 의 **사전 상자**(log-uniform 3 · uniform 1)에서 뽑은 150 표본을
>    **두 모델 각각**에 넣고, 가우스 과정 대리모형(GP)을 학습시켜 2¹⁴ = 16 384 Monte Carlo 표본으로 **Sobol 1차 · 2차 · 전차 지수**(식 C·1–C·3, Saltelli 2010 추정기, QUEENS)를 **95 % CI 와 함께** 낸다.
>    ⇒ `[해석]` 26호가 세운 표로 **첫 줄(설계)의 전역판**이다 — 흔드는 것은 설계 상자이고, 출력은 설계 KPI 이며, **추정 데이터도 적합점도 없다.** 둘째 줄(추정 민감도)도 셋째 줄(식별성)도 아니다.
>    그리고 **새 줄 하나**: `[인쇄]` `d_SOC = SOC_end,res − SOC_end,P2D` 의 국소 기울기 크기 `m_SOC`(Fig. 13) — **"모델 불일치(model discrepancy)의 민감도"** 다. 이것은 식별성이 아니라 **모델 적합성(model adequacy)** 의 도구다.
> 2. **"P2D 유효성" 은 식별성이 아니다 — 이 편은 적합성의 질문이다.** `[인쇄]` "The assumption for these studies is that the resolved model captures the reality more accurately than the P2D model" —
>    3차원 미세구조 분해 모델(resolved)을 **참값으로 가정**하고, 균질화 P2D 가 **같은 입력에서 같은 출력을 내는 파라미터 영역**을 찾는다. "이 데이터로 이 파라미터가 정해지는가" 는 한 번도 묻지 않는다.
> 3. ★★★★ **그러나 식별성의 재료가 지면에 셋 있다 — 저자는 셋 다 적합성으로만 읽었다.**
>    **(a) `S_T(D | P2D) ≈ 0`** — `[도표]` Fig. 8a P2D 막대 ≈0.00(CI 폭도 ≈0). **전차 Sobol 지수 0 은 "출력이 그 입력에 (거의 모든 곳에서) 의존하지 않는다" 이고, 그것은 그 출력으로 그 입력을 못 정한다는 충분조건이다.**
>    저자는 이것을 `[인쇄]` "the P2D model predicts almost no influence of the diffusion coefficient, while the resolved model assigns a non-negligible influence" — **모델 결함**으로 읽는다.
>    **(b) 두 모델이 같은 값을 내는 영역** — `[재현]` Fig. 7 벡터 좌표 150 점 중 대각선 ±0.02 안이 17 점, Fig. 11b 는 `κ ≲ 0.03 S m⁻¹` 8 점 중 4 점이 ±0.01 안(나머지 ≤0.06). 거기서 `SOC_end` 는 **모델 구조(미세구조 효과가 있나 없나)를 가르지 못한다** —
>    구조적 비식별(model discrimination 불가)의 계산된 표본이다. 저자는 그 영역을 `[인쇄]` "the P2D model may be easily used" 로 읽는다.
>    **(c) `[인쇄]` "While a constant difference could still be corrected by an update of the homogenization parameters"** — 모델 구조 오차가 **균질화 파라미터의 재보정에 흡수될 수 있다**는 명제. 이것이 바로
>    "적합이 맞는다 ≠ 파라미터가 맞다" 의 모델 판이다. **인쇄된 명제이지 계산이 아니다.**
> 4. ★★★★ **그리고 (c) 의 "상수 차이" 를 우리가 재현하면 그것은 균질화 수송이 아니라 접촉(연결) 손실이다.** `[인쇄]` resolved 미세구조의 **utilization `u = 0.93`**(집전체에 전자적으로 연결된 입자 몫),
>    `[인쇄]` "the concentration in the non-connected particles remains at its initial value", `[인쇄]` SOC 는 **모든** 양극 입자에 대해 적분된다 ⇒ `[재현]` resolved 의 `SOC_end ≥ 1 − u = 0.07` 인 **바닥**이 있다.
>    벡터 좌표: Fig. 11a 큰 `κ` 평탄 resolved **0.111** ↔ P2D **0.043**, 차 **0.068**; Fig. 7 150 점 **평균 차 0.072 · 중앙값 0.063**, resolved 최소 **0.100**(0/150 이 0.07 아래) ↔ P2D 최소 0.038(54/150 이 0.07 아래).
>    저자는 큰 `κ` 의 오프셋을 `[인쇄]` "attributed to an **insufficient homogenization strategy**, as the effective transport properties of the P2D model do not match" 로 배정한다 — **크기는 `1 − u` 와 맞는다.**
>    그리고 `u` 를 넣은 P2D(`A = 0.320`)의 곡선은 `[인쇄]` "shown in Fig. 3b by the additional dashed line" 인데 **그림에 없다**(벡터 경로 전수: 색 경로 4 개 = 곡선 2 + 점선 표식 2, D1).
>    ⇒ **카드의 물음이 모델 대 모델로 재현된다**: 참값 모델에서 **물질은 그대로이고 연결만 끊긴** 7 % 가, P2D 와 대조되면 **용량 오프셋**으로 나타나고, 저자는 그것을 **다른 이름(균질화 수송)** 으로 부르며,
>    처방은 `[인쇄]` "artificially reducing the available capacity of the cathode by a modification of the specific interface area `A_el-c`" — **P2D 에서 접촉 손실의 자리는 용량(= `LAM_PE` 의 자리)과 면적을 함께 깎는 손잡이 하나뿐이다.**
> 5. **Q4 는 움직이지 않는다 — 0/27.** 기준(10호 이래): **"이 조합은 이 데이터로 유일하게 정해지지 않는다" 를 계산으로 보인 편.** 이 편에는 **데이터가 없다**(두 모델의 무잡음 출력뿐, 1차 실험 0).
>    (a) 는 계산이지만 대상이 **단일 파라미터 · 설계 KPI · 대리모형**이고 저자가 적합성으로 읽었다. (b) 는 계산이지만 **모델 구조**의 비식별이지 파라미터 조합의 비식별이 아니다. (c) 는 명제이고 계산이 아니며,
>    그 계산이 될 그림(Fig. 3b 점선)은 빠졌다. `u` ↔ 오프셋 대응은 **우리 `[재현]`** 이다(26호 구분: 우리 재계산 ≠ 논문이 보인 것). **반 칸을 검토하고 접었다.**
>    **Q4 스무 번째 성질 = "적합성을 전역으로 재고, 그 안에서 나온 비식별의 재료 셋 — 전차 지수 0 · 두 모델의 일치 · 보정이 흡수하는 상수 — 을 전부 모델 적합성으로만 읽었다. 그리고 상수의 정체는 접촉 손실이었다."**

⚠ **표기 규약** (사용자 지정): `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림에서 읽은 값(figure-read ≈) · `[재현]` = 원문 수치·식·**벡터 좌표**로 우리가 다시 계산한 것 · `[추론]` = 우리의 해석.
이 편의 그래프는 **벡터**(PGFPlots)라 Fig. 3b · 7 · 9a · 11a · 14b 는 경로 좌표를 직접 뽑았다(판독 오차 ≈±0.002 SOC · ±0.005 V). Fig. 8 막대 · Fig. 12–13 곡면은 래스터 판독(±0.005 · 3차원 원근).

⚠ **이 편은 모델 편이다.** 1차 실험 0 · 열화 0(`degrad` 1 회, 결론의 "could be the origin of degradation") · 접촉 낱말 0(`contact` 0 — 대신 `utilization`·"connected") · 압력 스윕 0(틀 강성 한 값).

---

# 판정 한 줄

**NMC622/LPS/Li 금속 전고체 셀을 3차원 입자 분해 FEM(≈1.8 M 미지수)과 균질화 P2D(≈600 미지수)로 같은 방정식에서 풀고, 4 입력 150 표본 + GP 대리모형으로 두 모델의 Sobol 지수를 비교해
"P2D 가 믿을 만한 파라미터 영역" 을 찾는 **모델 적합성 편**이다. 전역 민감도는 제대로 했다(CI 까지). 그러나 출력은 설계 KPI 하나(`SOC_end`)이고 데이터가 없어 식별성의 질문은 서지 않는다 —
그런데 지면에 비식별의 재료 셋이 있고, 그중 "보정이 흡수할 수 있는 상수 차이" 는 벡터 좌표로 재면 **`1 − u = 0.07`, 즉 연결이 끊긴 활물질의 몫**이다.** Q4 0/27 유지 — 성질이 스무 번째로 바뀐다. 채움표 누적 ≈15.5 → ≈15.5 (새 칸 0).

---

# 0. 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **GP 대리모형의 사양** — 커널 · 초모수 · 학습 방식 · **검증 오차(hold-out · LOO)** 전부 미기재. `[인쇄]` "a nonlinear meta-model based on a Gaussian process is trained with the 150 training samples" 뿐 | Sobol 지수는 **대리모형의** 지수다. 4차원 150 점으로 `SOC_end` 의 **문턱형 응답**(§4-4)을 얼마나 맞히는지 모른다 |
| G2 | **95 % CI 의 출처** — MC 추정 분산만인지, GP 사후 불확실성까지 넣었는지 미기재 | CI 가 대리모형 오차를 빼고 있으면 Fig. 8 의 CI 는 **과소**다 |
| G3 | **Fig. 12a · 12b · 13 곡면이 직접 계산인가 대리모형인가** — 미기재 | `[도표]` 곡면 격자가 한 변 수십 선. `[재현]` 직접 계산이면 격자점 × 평균 1601.7 CPU-h(Table V) — 40×40 이면 ≈2.6×10⁶ CPU-h. 대리모형이면 Fig. 13 의 도함수는 **대리모형의 도함수**이고, 작은 `κ` 쪽 톱니 봉우리(`[도표]`)는 대리 오차일 수 있다 |
| G4 | **스윕에서 `D` · `σ` 를 상수로 바꿨나** — 기준 사례는 `[인쇄]` Fig. 14a 의 리튬화 함수 `D(χ)` · `σ(χ)` 를 쓰는데, Table IV 는 스칼라 구간 | 스칼라로 바꿨다면 150 표본은 기준 사례(Fig. 3)와 **다른 모델**이다. 함수에 배수를 곱했다면 "D = 3.16e-14" 의 뜻이 달라진다 |
| G5 | **P2D 에서 `A_el-c` 가 용량을 정하는 식** — `[인쇄]` "the specific area is slightly changed to `A_el-c` = 0.344 µm²/µm³ such that the capacity of the SSB cell in both models is exactly the same" | 용량이 `A` 로 바뀐다는 것은 **P2D 의 활물질 부피가 `A·d̄/6` 로 정해진다**는 뜻으로 읽힌다(`[추론]`) — 그러면 `A` 는 면적 · 용량 **둘 다**다(§6-4). `[재현]` `0.344 × 6.85/6 = 0.393` ↔ `ε_c` 0.376 |
| G6 | **`A = 0.320`(utilization 반영) P2D 의 결과** — 곡선도 `SOC_end` 수치도 없음 | 저자의 두 원인 분리(① utilization ② 기하 정보 손실)의 **유일한 계산**이 지면에 없다(D1) |
| G7 | **미세구조 실현의 산포를 Sobol 에 넣었나** — 150 표본이 한 미세구조 위인지 미기재. `[인쇄]` Fig. 6 은 실현 3 개 추가(곡선만, `u` 미보고) | 미세구조 우연성(aleatory)과 파라미터 효과가 섞였는지 모른다 |
| G8 | **`u` 가 개수 분율인가 부피 분율인가** — `[인쇄]` "the share of the particles that are electronically conductively connected" | `SOC_end` 바닥은 **부피** 분율로 정해진다. 저자의 `A → 0.93 A` 는 부피(용량)로 썼다 |
| G9 | **`m_SOC` 의 미분 변수** — 선형인가 `lg` 인가(D3) | Fig. 13 의 크기(≤≈0.25)는 `lg` 미분이어야 나온다 |
| G10 | **코드 · 데이터** — `[인쇄]` 4C multiphysics · QUEENS(둘 다 공개 URL), 데이터 가용성 문장 없음 | 150 표본 · GP 를 받을 길이 없다 |

---

# 1. 서지·모델 사양

| 항목 | 값 |
|---|---|
| 서지 | **Stephan Sinzig**\*, Christoph P. Schmidt\*, **Wolfgang A. Wall** — "Analysis of the Validity of P2D Models for Solid-State Batteries in a Large Parameter Range", *J. Electrochem. Soc.* **171** (2024) **120519**. DOI `10.1149/1945-7111/ad9a05`. 접수 2024-08-11 · 수정 2024-11-13 · 게재 2024-12-18. 교신 Sinzig (\* ECS Student Member) |
| 소속 | TUM 공학물리·계산학과 **계산역학연구소** + **TUMint.Energy Research GmbH**(Garching) — 계산역학 그룹(전기화학 실험실 아님) |
| 라이선스 · 자금 | `[인쇄]` CC BY 4.0 · 바이에른 경제부 "Industrialisierbarkeit von Festkörperelektrolytzellen" + BMBF **FestBatt 2**(03XP0435B) |
| 셀 | 양극 **NMC-622 + LPS** 복합체 85 µm · 분리막 **LPS** 50 µm · 음극 **Li 금속** 20.4 µm · 집전체 10 µm · 측면 60 µm(계산 영역 축소) · 입자 **로그정규** `μ = 1.8189, σ = 0.4589` · `[인쇄]` AM:(AM+SE) 부피비 0.4 · "porosity" 0.2 (D9) |
| 미세구조 | 완전구를 상자에 넣고 **DEM 재배열**(ref 6·16) · `[인쇄]` utilization **`u = 0.93`** |
| 방정식 | 두 모델 **같은 보존식**(식 1a–1s): 질량(전극 내 Fick, SE 는 `c = c_el,0` 고정 — `t₊ = 1` 가정) · 전하(`σ`·`κ` 옴) · 선운동량(유한변형 + Li 성장 · NMC 부피 변화) · 계면 **BV(`i₀` 상수, 농도 비의존)** · 전극–집전체 계면 저항 `r_i` |
| resolved | 3차원 FEM · one-step-θ · 단일체(monolithic) 풀이 · **≈1.8 × 10⁶ 미지수** · 48 CPU **32.8 h** / 표본(Table V) |
| P2D | 균질화(ref 31 Goldin 2012 · ref 35 Pereira 2022) · 전하 2 상(식 10·11) + 입자 구 확산(식 13·14) · 역학은 병렬/직렬 평균(부록 B) · 순차 풀이 · **≈600 미지수** · 1 CPU **90 s** / 표본 · `[재현]` CPU 시간비 ≈**6.4 × 10⁴** |
| 균질화 값 | `[인쇄]` `ε_el = 0.424` · `ε_c = 0.376` · Bruggeman `τ_el = 1.54` · `τ_c = 1.63` · `d̄ = 6.85 µm` · `A_el-c = 0.329 → 0.344 µm²/µm³` · `κ̄ = (ε_el/τ_el)κ = 3.3×10⁻³ S m⁻¹` · `σ̄ = (ε_c/τ_c)σ = 0.23 σ(χ)` |
| 재료(Table VI) | NMC622: `D(χ)`·`σ(χ)` Fig. 14a(ref 36) · `i₀` 4.98 A m⁻² · `c_max` 5.19×10⁴ mol m⁻³ · 리튬화 범위 [1, 0.404] · OCV Fig. 14b(ref 44 Kremer). LPS: `κ` 1.2×10⁻² S m⁻¹(ref 41 Randau) · `t₊` = 1(가정). Li: `i₀` 8.87 A m⁻² · `σ` 10⁵ S m⁻¹ |
| 사이클 | 0.25 C · 298 K · 3.6–4.2 V · 만충에서 방전 시작(방전–충전–방전) · 틀 강성 `k = 500 MPa mm⁻¹` |
| 민감도 입력(Table IV) | `σ` 10⁻²–10 S m⁻¹(log) · `κ` 10⁻³–1 S m⁻¹(log) · `D` 10⁻¹⁵–10⁻¹² m² s⁻¹(log) · `N_ρ` 2.89–9.64 A m⁻²(uniform) · 전부 독립 · 출력 **`SOC_end`** (첫 방전 3.6 V 도달 시) |
| 우리 축과의 거리 | 열화 0 · 실험 0 · 기준극 해당 없음(Li 금속) · 압력은 출력(축 응력)뿐 · **접촉 손실 = 전자 연결 분율 `u` 로 계산돼 있다**(1호 Bielefeld 2019 의 `θ` 와 같은 종류) |

`[재현]` 셀 면용량(`ε_c · c_max · 0.596 · F · l_compc`) ≈ **26.5 Ah m⁻² = 2.65 mAh cm⁻²** ⇒ 0.25 C ≈ 6.6 A m⁻²; Table IV 의 `N_ρ` 2.89–9.64 A m⁻² ≈ **0.11–0.36 C**(평균 6.27 ≈ 0.24 C).
Fig. 3b 첫 방전 기울기(0.46 / 6600 s)도 ≈4 h 방전 = 0.25 C 와 맞는다. ⚠ 이 면용량은 `ε_c = 0.376` 기준 — G5 에 따라 P2D 의 실제 용량 식은 모른다.

---

# 2. 모델 — 식 단위 (§ Governing Equations · Geometrically homogenized P2D model)

## 2-1. 균질화 규칙 (`[인쇄]` 식 2–5)

- 상 평균 `φ̄_phase = (1/V_phase)∫Φ dΩ`, 체적 분율 `ε_i = V_i/V` ⇒ `φ̄ = ε_phase φ̄_phase`.
- 발산: `∇·N` 의 균질화 = `ε∇·N̄ + A N̄_i` — `A` 는 **비표면적**(다른 상과의 계면 면적 / 부피), 구면이면 `A = 6 ε_i / d_b`.
- 유속: `N̄ = N/τ`, `τ = ε^b`, `b = −0.5`(Bruggeman) ⇒ `[재현]` `τ_el = 0.424^−0.5 = 1.536` ✓ · `τ_c = 0.376^−0.5 = 1.631` ✓.
- ⚠ **이 편의 `τ` 는 "굴곡도 인자"** 다: `σ_eff = (ε/τ)σ = ε^1.5 σ`. 24호(Stavola 2023)의 `τ² = ε σ_bulk/σ_eff` 와 **같은 양**이다 — 이름이 `τ` ↔ `τ²` 로 다르다(`[재현]`, §6-4 ①).

## 2-2. P2D 식 (`[인쇄]` 식 6–14)

```
(10) ∂/∂x[(ε_el/τ_el) κ ∂Φ̄_el/∂x] + A_el-c N̄_q = 0          ← SE 상 전하
(11) ∂/∂x[(ε_c/τ_c)  σ ∂Φ̄_c/∂x]  + A_el-c N̄_q = 0           ← 활물질 상 전하
(13) ∂c/∂t − (1/r²)∂/∂r(r² D ∂c/∂r) = 0                      ← 점마다 구 하나
(14) D ∂c/∂r = −N̄_c = −N̄_q/(Fz)   at r = r_ed               ← 결합
(1p) i = i₀[exp(α_a Fη/RT) − exp(−(1−α_a)Fη/RT)]             ← BV, i₀ 상수
```

`[해석]` 데이터(여기서는 출력)가 보는 조합: `κ` 는 **`(ε_el/τ_el)κ`** 로만, `σ` 는 **`(ε_c/τ_c)σ`** 로만, 반응원은 **`A_el-c · i₀`** 로만(`i₀` 가 농도 비의존이라 정확한 곱), 구 확산은 `r_ed` 와 함께(시간척도 `r²/D`).
그리고 `[인쇄]` "a sphere is assumed at every point x" — **입자 크기는 `d̄` 하나**, 입자 사이 확산 **없음**(`[인쇄]` "non-connected particles as a central modeling assumption of the P2D model (c.f. Eqs. 13, 14)").

## 2-3. utilization 과 `A` (`[인쇄]` p5–6)

- `[인쇄]` "An analysis of the generated microstructure reveals a utilization of **u = 0.93** … This utilization is **not considered within the P2D model** as this information is typically not available if the microstructure is not explicitly resolved."
- `[인쇄]` "The utilization could be included within the P2D model by **artificially reducing the available capacity** of the cathode by a modification of the specific interface area `A_el-c` … However, artificially modifying one homogenization parameter **might be inconsistent with the other homogenization parameters**."
- `[인쇄]` `A_el-c` = **0.329**(= `6ε_c/d̄`, `[재현]` 6×0.376/6.85 = 0.3294 ✓) → **0.344**("such that the capacity … is exactly the same") → **0.320**(utilization 반영). `[재현]` 0.320/0.344 = **0.930** = `u` ✓.

---

# 3. 고정 파라미터 비교 (Fig. 3–6)

| 그림 | `[인쇄]` 서술 | `[도표]`/`[재현]` |
|---|---|---|
| **Fig. 3a** 전압–시간 | "In the resolved case, the voltage limits are reached earlier" | 첫 방전 끝 resolved ≈0.66×10⁴ s ↔ P2D ≈0.77×10⁴ s; 두 번째 방전 끝 ≈1.72 ↔ ≈2.00×10⁴ s |
| **Fig. 3b** SOC | `SOC_end` 상대편차 `ε = |(SOC_res − SOC_P2D)/(1 − SOC_res)| ≈ 13 %`; "the dashed line represents a P2D model in which the utilization is considered" | `[재현]` 벡터: resolved ≈0.53–0.54 · P2D ≈0.47 ⇒ 13–15 % ✓. ⚠ **점선 곡선 없음** — 색 경로 전수 4 개(파랑·주황 곡선 + 두 `SOC_end` 점선 표식). **D1** |
| **Fig. 4a** 두께 방향 평균 농도 | "sandwich lithiation … observable within the connected particles … In the P2D model … significantly less prominent but still observable" | resolved(전체) z ≈48 µm 에 **3.26×10⁴ 골** — 비연결 입자 군집; 연결 입자만(점선) 양끝 ≈3.72·3.73 ↔ 중앙 ≈3.53. P2D 는 3.85 → 3.40(z ≈72)로 **거의 단조**, 끝 상승 ≈0.01×10⁴(D11) |
| **Fig. 4b** 입자별 농도 | "the concentration in the non-connected particles remains at its initial value" | 청색(≈2.1×10⁴ = 초기값) 입자가 표면에 다수 — **물질은 그대로, 쓰이지 않는다**: 카드 질문의 3차원 그림 |
| Fig. 5 축 응력 | Li 음극 부피 변화가 지배, 두 모델 방전 끝까지 일치 | 0 → ≈3.0(resolved) / ≈3.5 MPa(P2D). **초기 응력 0**(예압 없음, `[도표]`) |
| Fig. 6 미세구조 실현 3 개 | "Only small deviations … especially in comparison to the deviations between the resolved model and the P2D model" | 첫 방전은 실현끼리 ≈0.01×10⁴ s 안. 두 번째 방전 끝은 한 실현(일점쇄선)이 ≈1.80 ↔ 1.72×10⁴ s — **모델 차(0.28)의 ≈30 %**(D14) |

**원인 분리의 논리.** `[인쇄]` 편차의 원인 둘: "(1) The reduced utilization in the resolved case … and (2) the loss of geometric information". ① 을 `A = 0.320` 으로 지운 뒤에도 "there is still a deviation" ⇒
"the remaining deviation is attributed to a different intercalation behavior". ⚠ 그 "뒤" 의 곡선이 그림에 없다(D1) — **분리는 서술로만 있다.**

---

# 4. 전역 민감도 (Table IV · Fig. 7 · Fig. 8 · 부록 C)

## 4-1. 식 — 출력이 무엇인가

- **출력** `Y = SOC_end` = 첫 방전이 3.6 V 에 닿을 때의 `[인쇄]` `SOC(t) = ∫_Ωc (c(t) − c_min)dΩ / ∫_Ωc (c_max − c_min)dΩ` — **모든 양극 입자**(비연결 포함)에 대한 적분.
  `[인쇄]` "One characteristic quantity is the amount of **unreachable capacity**, i.e. the SOC at the end of discharge."
- **입력** `X = (lg σ, lg κ, lg D, N_ρ)` — log-uniform 셋은 `lg(Ψ/Ψ₁)`, `Ψ₁` = 1 S m⁻¹ · 1 m² s⁻¹.
- **지수** `[인쇄]` 식 C·1 `S_i = V(E(Y|X_i))/V(Y)` · C·2 `S_ij = V(E(Y|X_i,X_j))/V(Y) − S_i − S_j` · C·3 `S_i^t = E(V(Y|X\X_i))/V(Y)`. 비용 `M(2D+2)` 평가(ref 52 Saltelli 2010), QUEENS 구현.
- **계산** 150 표본(두 모델 공통) → GP 대리모형 → 2¹⁴ = 16 384 MC 표본 → 지수 + 95 % CI.

`[해석]` 출력은 **각 모델의** `SOC_end` 다 — Sobol 은 모델마다 따로 돌렸다. **모델 간 차이(`d_SOC`)의 Sobol 은 없다**; 차이는 §5 의 국소 기울기(`m_SOC`)로만 본다.
그리고 **데이터 · 잔차 · 가능도가 없다** — 26호 표의 첫 줄이다.

## 4-2. Fig. 7 — 150 점 산점도 (`[재현]` 벡터 좌표 150 개 전수)

| 양 | 값 |
|---|---|
| 점 수 | **150** ✓(인쇄와 일치) |
| 대각선 아래(P2D < resolved − 0.02) / 위 / ±0.02 안 | **100 / 33 / 17** |
| resolved 최소 · P2D 최소 | **0.100** · 0.038 |
| 0.07 아래 | resolved **0/150** · P2D **54/150** |
| 차(resolved − P2D) 평균 · 중앙값 | **0.072 · 0.063** |
| 최대 비 resolved/P2D | **6.4**(0.324 / 0.051) — `[인쇄]` "up to factor five" 는 보수적 |
| 바닥 0.07 을 뺀 최대 비 | **5.0** |

`[재현]` resolved 의 `SOC_end` 에는 **`1 − u = 0.07` 바닥**이 있다(비연결 7 % 가 초기 SOC = 1 에 머문다). 150 점의 **평균 차가 그 바닥과 같다** ⇒ "P2D 가 전달 전하를 과대예측한다(대각선 아래 100 점)" 의 **대부분이 utilization** 이다.
극단(비 5–6)은 바닥을 빼도 남는다(5.0) — 그것은 §4-4 의 문턱 증폭 쪽이다.

## 4-3. Fig. 8 — Sobol 지수 (`[도표]`, 래스터 ±0.005)

| | resolved 1차 | resolved 전차 | P2D 1차 | P2D 전차 |
|---|---:|---:|---:|---:|
| `σ` (el. cond.) | ≈0.14 | ≈0.22 | ≈0.03 | ≈0.045 |
| `κ` (ion. cond.) | ≈0.65 | ≈0.76 | ≈0.875 | ≈0.91 |
| `N_ρ` (current) | ≈0.075 | ≈0.15 | ≈0.055 | ≈0.085 |
| `D` (diff. coeff.) | ≈0.008 | ≈0.037 | ≈0.00 | **≈0.00** |

2차(`[도표]`, resolved ↔ P2D, 괄호 = 95 % CI): `σκ` 0.033 [≈0, 0.066] ↔ 0.005 · `σN` ≈0.000 [−0.035, 0.035] ↔ **0.003** · `σD` −0.002 ↔ −0.001 · `κN` 0.034 **[−0.037, 0.104]** ↔ 0.018 [−0.047, 0.082] · `κD` 0.001 ↔ −0.001 · `DN` ≈0 ↔ ≈0.

`[인쇄]` 해석과 대조:
- "the ionic conductivity has the greatest influence within both models" — ✓.
- "the first-order index has almost the same value as the total-order index **for all parameters**" — resolved 에서 `σ` 0.14/0.22 · `N_ρ` 0.075/0.15 · `D` 0.008/0.037 은 **"거의 같다" 가 아니다**(D4). 바로 다음 문단이 "the difference between the first and total order indexes computed with the P2D model is smaller" 라 스스로 긴장.
- "the second-order Sobol-indexes computed with the P2D model are **smaller for all parameter combinations**" — `σN`·`σD` 는 점추정으로도 P2D 가 크거나 같고, **CI 6 쌍 중 다수가 0 을 포함**하며 음의 점추정(비물리)이 있다(D5).
- "The Sobol indexes of first and second order sum almost up to the total order indexes" — `[재현]` 행별 `S_i + Σ_j S_ij` ↔ `S_i^t`: resolved `σ` 0.17 ↔ 0.22 · `N_ρ` 0.11 ↔ 0.15 · **`D` 0.007 ↔ 0.037(≈80 % 가 3차 이상 또는 추정 오차)**(D6). 전체 합 `ΣS_i + ΣS_ij` ≈0.94(resolved) · ≈0.98(P2D).
- ⚠ **Sobol 지수는 사전 상자의 함수다** — "`κ` 가 가장 중요" 는 `κ` 3 자릿수 · `D` 3 자릿수 · `N_ρ` 3.3 배 라는 **상자 선택**의 진술이기도 하다(`[해석]`).

## 4-4. ★★★ `SOC_end` 는 OCP 평탄이 증폭하는 문턱 출력이다 (`[재현]` Fig. 14b 벡터)

`[재현]` NMC622 OCV(Fig. 14b, ref 44) 경로 좌표: `χ` 0.404 → **4.17 V**, 0.54 → 3.86 V, 0.72 → 3.73 V, **0.81–0.97 → 3.67–3.69 V 평탄**, 0.99 → 3.50 V, 1.0 → 급락.
하한 **3.6 V** 는 평탄보다 **70–90 mV 아래**다. `SOC_end` ↔ `χ = 1 − 0.596·SOC`: SOC 0.05 ↔ `χ` 0.97, SOC 0.32 ↔ `χ` 0.81 — **SOC 0.05–0.32 전체가 OCP 20 mV 안**이다.
⇒ `[추론]` 이 대역에서 `SOC_end` 는 "과전압이 ≈70–90 mV 를 언제 넘나" 의 **문턱 함수**이고, 수십 mV 의 임피던스 차가 `SOC_end` 를 최대 ≈0.27 움직인다.
Fig. 7 의 "factor five" 군집(P2D 0.04–0.06 ↔ resolved 0.2–0.34)이 **정확히 이 대역**에 있다. **출력 척도가 모델 차를 증폭한다** — 전압 차로 쟀다면 훨씬 작았을 것이다(이 편은 전압 차를 보고하지 않는다).
그리고 GP 대리모형(G1)은 이런 **문턱형 응답**에 약하다.

---

# 5. 단일 · 이중 파라미터 변화 (Fig. 9–13)

## 5-1. `D` 스윕 (Fig. 9, `κ = 0.032 S m⁻¹` · `σ = 0.32 S m⁻¹` · `N_ρ = 6.27 A m⁻²` 고정 — Table IV 상자의 로그 중앙)

`[재현]` 벡터 좌표(두 모델 각 **15 점**, 10⁻¹⁵–10⁻¹² 등간격 로그):

| `D` (m² s⁻¹) | resolved | P2D |
|---|---:|---:|
| 10⁻¹⁵ | **0.257** | 0.162 |
| ≈10⁻¹⁴ | ≈0.140 | ≈0.137 |
| 10⁻¹² | **0.117** | **0.135** |

- P2D 는 `D ≳ 10⁻¹⁴` 에서 **0.135 평탄**(1.6 자릿수 이상 0 열) — `[인쇄]` "the P2D model approaches a constant value … attributed to the non-connected particles as a central modeling assumption of the P2D model". resolved 는 계속 내려간다(입자 사이 확산, Fig. 10a).
- `[재현]` 큰 `D` 에서 resolved 의 **연결 입자만** 보면 `(0.117 − 0.07)/0.93 ≈ 0.05` ↔ P2D 0.135 — 여기서는 바닥을 빼도 차가 **커진다**. 입자 사이 확산 설명과 양립.
- 작은 `D` 에서 resolved 가 더 높다: `[인쇄]` "the diffusion within the differently sized particles is not sufficiently represented". `[재현]` P2D 의 `d̄ = 6.85 µm` 는 로그정규의 **개수 평균**(`exp(μ + σ²/2)` = 6.850 ✓, 최빈 4.99 ✓ Fig. 15)이다. 부피 가중 `d₄₃ = exp(μ + 3.5σ²)` = **12.9 µm** ⇒ 구 확산 시간척도 `(d₄₃/d̄)²` ≈ **3.5 배**.
  ⇒ `[추론]` 작은 `D` 쪽 차이의 일부는 **`D/d²` 한 조합의 선택**(어느 평균 지름을 쓰나)이다 — P2D 의 `D` 를 ≈1/3.5 로 옮기는 것과 같은 효과. 저자는 `d̄` 선택을 원인으로 들지 않는다.

## 5-2. `κ` 스윕 (Fig. 11, `D = 3.16×10⁻¹⁴` · `σ = 0.32` · `N_ρ = 6.27` 고정)

`[재현]` 벡터 좌표(15 점): `κ` = 10⁻³ 에서 resolved 0.970 · P2D 0.978; 1.6×10⁻³ 에서 0.867 · 0.915; … **`κ ≳ 0.05` 평탄 resolved 0.111 · P2D 0.043, 차 0.068**.
`[인쇄]` "an offset is present for large values of the ionic conductivity … attributed to an **insufficient homogenization strategy**" ↔ `[재현]` **차 0.068 ≈ `1 − u` = 0.07.**
⇒ 이 오프셋은 수송이 아니라 **바닥**이다(`[추론]` — 큰 `κ` 에서 두 모델 모두 이온 제한이 풀리면 연결 입자는 같은 깊이까지 방전되고, resolved 에만 비연결 7 % 가 남는다: `(0.111 − 0.07)/0.93 = 0.044` ↔ P2D **0.043**).
작은 `κ` 에서는 P2D 가 더 높다(`[인쇄]` 입자 사이 확산이 이온 전도 부족을 보완 못 함). `[재현]` `κ ≲ 0.03` 8 점의 P2D − resolved = +0.008 · +0.048 · +0.061 · +0.035 · +0.008 · −0.033 · −0.008 · +0.006 — **4 점이 ±0.01 안**, 이 쪽에서는 두 모델이 거의 같은 값을 낸다.

## 5-3. `κ × D` 평면 (Fig. 12–13)

- Fig. 12a resolved `SOC_end` 곡면 · Fig. 12b `d_SOC = SOC_end,res − SOC_end,P2D` — `[인쇄]` "Differences of |d_SOC| ≈ 0.15".
  `[도표]` 축 방향 확인: 12a 세 꼭짓점(`κ`=10⁻³ ≈0.9–1 · (`κ`=1, `D`=10⁻¹²) ≈0.05 · (`κ`=1, `D`=10⁻¹⁵) ≈0.25)이 Fig. 9a · 11a 와 맞는다.
- `[인쇄]` "While a constant difference could still be corrected by an update of the homogenization parameters, a correction of the homogenization parameters is non-trivial in this case."
- `[인쇄]` `m_SOC = sqrt((∂d_SOC/∂κ · κ₁)² + (∂d_SOC/∂D · D₁)²)` (Fig. 13) — "Regions are visible in which the value of the derivative is almost zero. In this region (**large ionic conductivity and small diffusion coefficient**), the P2D model may be easily used."
  ⚠ `[도표]` Fig. 13 의 ≈0 바닥(진청)은 **큰 `κ` · 큰 `D`** 꼭짓점 쪽이고, 작은 `D`(10⁻¹⁵) 쪽 모서리는 ≈0.1(청록)로 올라간다 — Fig. 12b 에서도 큰 `κ` 모서리가 `D` 를 따라 ≈0.05 → ≈0.2 로 변한다. **본문과 그림이 `D` 방향에서 반대**(D2).
  그리고 `m_SOC` 의 크기(≤≈0.25)는 **`lg` 미분이어야** 나온다 — 인쇄된 식대로 선형 미분 × 1 m² s⁻¹ 이면 `D` 항이 ~10¹³ 이다(D3).
- `[해석]` `m_SOC ≈ 0` 은 "차이가 **상수**라 보정으로 흡수된다" 는 뜻이지 "차이가 **없다**" 가 아니다. 큰 `κ` 영역이 바로 그곳이고, 그 상수가 `1 − u` 다(§5-2).
  ⇒ **저자가 "P2D 를 쉽게 쓸 수 있다" 고 한 영역은 "P2D 를 보정하면 접촉 손실이 용량 손잡이에 흡수되는 영역"** 과 같다(`[추론]`).

---

# 6. ★ Q4 본론

## 6-1. 세 층 중 어디인가 (사용자 체크리스트 1)

| 26호 표의 줄 | 이 편에서 | 판정 |
|---|---|---|
| **설계 민감도** | Table IV 사전 상자 × 설계 KPI `SOC_end` × **Sobol 1·2·전차 + 95 % CI** | ✅ **이 줄 — 전역판**(OAT 스윕이 아니다: 26호보다 한 단계 제대로) |
| 추정 민감도 | 데이터 · 적합점 · 잔차 야코비안 | ❌ 없음 |
| 식별성 | FIM · 조건수 · 프로파일 · 근최적 폭 · 사후분포 | ❌ 전수 0 — 지문 `Fisher`·`Hessian`·`profile`·`identifiab`(파라미터 뜻) 0 |
| **(새 줄) 모델 불일치 민감도** | `m_SOC = |∇ d_SOC|` (Fig. 13) | 적합성 도구 — 식별성 아님 |

⇒ 큐 지문 표의 "**전역 민감도를 제대로 한다**" 는 **맞다**(Sobol · 2차 · CI · 대리모형 · 추정기 원전까지). 그리고 **그것이 식별성이 아니라는 것도 맞다** — 대상이 데이터가 아니라 설계 KPI 다.

## 6-2. 적합성(model adequacy) ≠ 식별성 (사용자 체크리스트 2)

| | 모델 적합성 (이 편의 질문) | 파라미터 식별성 (Q4) |
|---|---|---|
| 물음 | 같은 입력에서 **두 모델**이 같은 출력을 내나 | 한 모델에서 **데이터**가 파라미터를 하나로 정하나 |
| 참값 | 상위 충실도 모델(resolved) | 데이터를 만든 파라미터 |
| 실패의 모양 | `d_SOC ≠ 0` | 손실 함수의 평탄 · null 방향 |
| 이 편의 도구 | Sobol 비교 · `d_SOC` · `m_SOC` | 없음 |

**그러나 두 질문이 만나는 자리가 셋 있다**(`[해석]`):
- **(b) 일치 = 구조적 비식별.** 두 모델이 같은 `SOC_end` 를 내는 곳(Fig. 7 ±0.02 안 17/150 · Fig. 11a 작은 `κ` 8 점 중 4 점이 ±0.01 안)에서는 **`SOC_end` 로 모델 구조를 못 가른다.** 저자는 일치를 "P2D 유효" 로 읽지만,
  같은 사실은 "그 영역의 데이터는 미세구조 효과(입자 사이 확산 · 비연결 7 %)가 **있는지** 말해 주지 않는다" 이기도 하다.
- **(c) 보정 흡수 = 파라미터가 구조 오차를 먹는다.** `[인쇄]` 상수 차이는 균질화 파라미터 재보정으로 교정된다 ⇒ **보정된 `ε/τ` · `A` 는 물성이 아니라 "구조 오차 + 물성" 의 합**이 된다. 우리 degeneracy 질문의 모델 판.
- **(a) `S_T ≈ 0` 은 비식별의 충분조건.** P2D 의 `D` 는 `SOC_end` 로 정해지지 않는다 — **P2D 로 적합하면 `D` 는 아무 데나 간다**(26호 `D_e⁻` 10 자릿수 표류와 같은 종류의 위험). 저자는 이것을 "P2D 가 `D` 의 영향을 과소평가" 로 읽는다.

## 6-3. 곱으로만 들어가는 쌍 — 이 편은 알아챘나 (사용자 체크리스트 3)

| 쌍 | 이 편에서 | 알아챘나 | 대질 |
|---|---|---|---|
| **① `κ`·`ε_el/τ_el`** | 식 (10) · Table III `κ̄ = (ε_el/τ_el)κ` 인쇄. Sobol 은 `κ` 만 흔든다 ⇒ **P2D 의 "ion. cond." 지수는 `κ̄` 의 지수**이고, `κ` ×1000 은 `ε_el/τ_el` ×1000 과 같다(`[재현]` 식 10) | **반쯤** — "상수 차이는 균질화 파라미터로 교정" 은 곱의 한 인자로 구조 오차를 흡수할 수 있음을 안다는 뜻. **곱이 식별을 막는다는 말은 없다** | 24호: `τ² = σ_bulk ε/σ_eff` 는 **측정 ÷ 가정** — 여기는 **전부 가정**(Bruggeman `b = −0.5`)이다. 그리고 이 편의 `τ` = 24호의 `τ²`(이름 충돌) |
| **② `D`·`r²`** | 식 (13)–(14): 구 하나 · `d̄` 하나 ⇒ 시간척도 `r²/D`. resolved 는 로그정규 분포. `[재현]` `d̄` = 개수 평균 6.85 ↔ `d₄₃` 12.9 µm, `(d₄₃/d̄)²` ≈ 3.5 | **아니다** — 작은 `D` 쪽 차이를 "complex diffusion paths · different sizes" 로 읽고, **어느 평균 지름을 쓰느냐가 `D` 축을 ≈0.55 자릿수 옮긴다**는 말은 없다 | 26호: `D_M⊕·a_max/I` 한 조합(박막 `x` 좌표). 여기는 `D/d²` — 같은 "수송 ↔ 기하" 곱의 입자판 |
| **③ `i₀`·`A`** — 그리고 **`A` 의 세 겹 짐** | 식 (10)–(11) 반응원 `A_el-c N̄_q`, BV `i₀` 상수 ⇒ **`A·i₀` 정확한 곱**. 그런데 `A` 는 **(i) 면적**(`6ε_c/d̄`) · **(ii) 용량**(0.329 → 0.344 "capacity … exactly the same") · **(iii) utilization**(→ 0.320 = 0.93×) 을 **한 손잡이로** 진다 | **반쯤** — `[인쇄]` "artificially modifying one homogenization parameter might be inconsistent with the other homogenization parameters" 는 결합을 안다. `i₀` 는 흔들지 않아 곱은 안 나타난다 | 9호 `A_eff·ε_p/R_s` · 16호 `j₀·ε_CAM/r_CAM` 와 **같은 자리**. ★ 새로운 것: **접촉 손실(`u`)이 들어갈 곳이 그 곱의 `A` 뿐**이라는 것을 저자가 처방으로 인쇄했다 |

`[재현]` ③ 의 크기: 로그정규 구의 실제 비표면적은 `6ε_c/d₃₂`(`d₃₂ = exp(μ + 2.5σ²)` = 10.44 µm) = **0.216** — P2D 의 0.329 는 그 **1.52 배**, 0.344 는 1.59 배다(resolved 입자가 분포를 따르고 상자 경계 절단을 무시할 때).
⇒ `[추론]` P2D 는 resolved 보다 반응 면적이 ≈1.5 배 크고(`A·i₀` 가 1.5 배), 용량을 맞추려 `A` 를 **더** 올렸다. "P2D 가 전달 전하를 과대예측" 의 원인 후보에 **면적 과대**가 하나 더 있다 — 저자는 들지 않는다.

## 6-4. 26호의 "스윕 그림 겹치기 = 공짜 야코비안" 을 이 편에 걸면

- **Fig. 9a P2D**: `D ≳ 10⁻¹⁴` 에서 0 열 — Sobol `S_T(D | P2D) ≈ 0` 과 **같은 사실의 두 판**(국소 · 전역).
- **Fig. 11a 두 모델**: `κ ≳ 0.05` 에서 0 열 — 큰 `κ` 는 `SOC_end` 로 안 정해진다(두 모델 공통).
- **Fig. 9a ↔ 11a**: 서로 다른 곡선족(겹치지 않는다) — `D` 와 `κ` 는 이 한 점 근방에서 평행 열이 아니다. ⚠ 곱 쌍(①–③)의 짝은 **흔들지 않았으므로** 겹쳐 볼 그림이 없다.

## 6-5. ★ Q4 판정 (사용자 체크리스트 4)

**0/27 — 움직이지 않는다.** 반 칸을 검토했다:
- **찬성 근거**: (a) `S_T(D | P2D) ≈ 0` 은 **저자가 스스로 계산**했고 CI 까지 있다 — 전차 지수 0 은 비식별의 **수학적 충분조건**이다. 26호(OAT 한 점 평탄)보다 강하다.
- **반대 근거(채택)**: ① **데이터가 없다** — 출력은 무잡음 모델 출력, 기준의 "이 데이터로" 가 성립하지 않는다. ② 대상이 **단일 파라미터**이고 기준은 **조합**이다. ③ 계산이 **대리모형** 위에 있고 그 검증이 없다(G1). ④ **저자가 그것을 식별성으로 읽지 않았다** — 모델 결함으로 읽었다(10호 구분: 인쇄된 명제 ↔ 계산된 판정; 둘 다 식별성 방향으로는 없다).
  ⑤ 가장 강한 재료(`u` ↔ 오프셋 ↔ `A` 손잡이)는 **우리 `[재현]`** 이고, 그것을 저자 쪽에서 보였을 그림(Fig. 3b 점선)은 **빠졌다**(26호 구분).
- **Q4 스무 번째 성질** = **"적합성을 전역으로 재고, 그 안에서 나온 비식별의 재료 셋 — 전차 지수 0 · 두 모델의 일치 · 보정이 흡수하는 상수 — 을 전부 모델 적합성으로만 읽었다. 그리고 상수의 정체는 접촉 손실이었다."**
  24호(열일곱 번째 "비식별을 물리로 읽었다") · 26호(열아홉 번째 "평탄을 스스로 계산해 놓고 물리로 읽었다") 와 같은 계열 — 다른 점은 **읽은 틀이 물리가 아니라 모델 적합성**이라는 것.

---

# 7. 이 모델 대 우리 `degradation-degeneracy/` PyBaMM 모델 (사용자 체크리스트 5)

- **구조는 같은 계열, 파라미터 범위는 안 겹친다.** 우리 합성 truth 는 PyBaMM **DFN**(`configs/base.yaml` 의 `model.type` · `parameter_set` 이 정본 — 값은 여기 옮기지 않는다) = **액체 전해질 P2D** 다.
  이 편의 P2D 는 같은 Doyle–Fuller–Newman 틀의 **고체 전해질판**(`t₊ = 1` · SE 농도 고정 · Li 금속 음극 · 역학 결합)이고, 입력 상자(SE `κ` 10⁻³–1 S m⁻¹ · NMC622 `D` 10⁻¹⁵–10⁻¹² · utilization)는 우리 truth 의 파라미터 공간과 **대응하는 축이 거의 없다**.
  ⇒ **"유효 범위" 가 우리 파라미터 범위와 겹치는가 — 겹치지 않는다**(화학 · 전해질 상 · 음극이 다르다).
- **겹치는 것은 설계다.** 이 편은 **"상위 충실도 모델 = 참값, 축약 모델을 채점"** 이다 — 우리 프로젝트의 **"PyBaMM 합성 truth, α·β fitting 을 채점"** 과 같은 모양이다. 차이 하나가 결정적이다:
  우리는 **truth 와 채점 대상이 같은 모델 계열**(DFN 곡선 → OCV 기반 적합)이라 **모델 구조 오차가 설계상 0** 이다. 이 편은 그 오차의 **크기를 보여 준다**(ASSB 에서 `SOC_end` 중앙 0.063 · 극단 5–6 배).
  ⇒ `[추론]` 실데이터에서는 이 크기의 구조 오차가 **보정 파라미터에 흡수**된다(`[인쇄]` "a constant difference could still be corrected by an update of the homogenization parameters"). 우리 degeneracy 판정은 **"모델 구조가 맞다는 조건 아래의 식별성"** 이라는 것을 이 편이 수치로 상기시킨다.
- ★★★ **ASSB 판으로 갈 때의 경고.** 카드가 언젠가 `degradation-degeneracy` 를 ASSB 로 옮긴다면, **P2D 합성 truth 에는 접촉 손실의 자리가 `A`(용량 · 면적) 하나뿐**이다(§6-3 ③ — 저자 스스로 인쇄한 처방).
  그러면 truth 에서 "접촉 손실" 과 "`LAM_PE`" 가 **같은 파라미터**로 생성되고, 적합이 둘을 가르느냐는 질문은 **truth 단계에서 이미 답이 "못 가른다" 로 고정**된다 — 시험이 아니라 동어반복이다.
  ⇒ **ASSB 판 truth 는 resolved(또는 `u` · 연결 분율을 `A` 와 독립인 자리로 가진) 모델이어야 한다.** 이 편의 4C resolved 모델이 그 후보의 한 예다(비용 ×6.4×10⁴).
- **가져올 것**: `m_SOC` 식의 **"모델 불일치 민감도" 지도** — 우리 쪽에서는 "truth 와 적합 모델이 달라지는 영역에서 fitted 라벨이 어떻게 편향되나" 를 재는 가드로 쓸 수 있다(`[추론]`, 미실행).

---

# 8. 곱 축퇴 처방 (사용자 체크리스트 6)

**모델 편이라 적용 대상 아님.** 이 편에는 실험 데이터가 없다(26호와 달리 빌린 데이터도 없다) — 처방 1–4단계(같은 상태축 `R`·`C` · 면적 대조군 · `Ea`/`C` 상한 · 시간 영역)가 걸 입력이 전부 없다.
기여는 처방이 아니라 **곱의 모델 쪽 세 번째 표본**이다(9호 P2D · 26호 박막 다음): P2D 에서 **`A_el-c` 한 손잡이가 면적 · 용량 · 연결 분율을 함께 진다**는 것을 저자가 처방(`A → u·A`)으로 인쇄했다.

---

# 9. 채움표 행 (Q1–Q8)

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **부분(계산) — 1호와 같은 층.** `[인쇄]` 전자 연결 분율 **`u = 0.93`**(생성 미세구조 1 개, DEM 재배열 · 개수/부피 미기재 G8). `contact` **0 회**. `θ(N)` **0/27**. `[재현]` resolved `SOC_end` 바닥 = `1 − u` — Fig. 11a 오프셋 0.068 · Fig. 7 평균 차 0.072 | **없다** — 실험 0, 두 모델의 출력뿐 | **model-vs-model reference** — 상위 충실도 모델을 `[인쇄]` "assumption" 으로 참값 삼음(= 우리 합성 truth 구조). ★ **민감도에 95 % CI 를 붙인 계보 첫 편**(단 GP 대리 · CI 출처 미기재) | **없다 (27/27 편 0).** 스무 번째 성질 — §6-5 | **해당 없음** — Li 금속 음극, 모델 편 | **없다** — 틀 강성 `k` = 500 MPa mm⁻¹ 한 값, 축 응력은 **출력**(`[도표]` 0 → ≈3.0–3.5 MPa, 예압 0), 스윕 0 | **해당 없음**(Li 금속 · 열화 0) | **NMC622 + LPS — 기존 화학**(22호 NCM622). OCV 는 ref 44(Kremer, 구조 분해 모델 논문)에서 빌림. `[재현]` 벡터: 평탄 **3.67–3.69 V @ `χ` 0.81–0.97**, 4.17 V @ 0.404. `OCV` 0 회 |

**누적 ≈15.5 → ≈15.5 (새 칸 0).** 안 움직인 칸: 전부. Q3 에 층 하나(모델 대 모델 참값 + CI 붙은 민감도).

---

# 10. 어긋남 (D-목록)

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | `[인쇄]` "The result is shown in Fig. 3b by the **additional dashed line**" · 캡션 "The dashed line represents a P2D model in which the utilization is considered" ↔ **그림에 그 곡선이 없다** | Fig. 3b 벡터 경로 전수 — 색 채움 경로 **4 개**(파랑 곡선 42 요소 · 주황 곡선 48 · 파랑 점선 표식 14 · 주황 점선 표식 12). 170 dpi 렌더로도 확인 |
| **D2** | `[인쇄]` "derivative is almost zero … (large ionic conductivity and **small** diffusion coefficient)" ↔ `[도표]` Fig. 13 의 ≈0 바닥은 큰 `κ` · **큰** `D` 꼭짓점 | 축 방향은 Fig. 12a 꼭짓점을 Fig. 9a · 11a 와 맞춰 확인(§5-3). ⚠ 3차원 원근 판독 |
| **D3** | `[인쇄]` `m_SOC` 식이 선형 미분 × `κ₁` (1 S m⁻¹) · `D₁` (1 m² s⁻¹) ↔ Fig. 13 크기 ≤≈0.25 | `[재현]` 선형이면 `∂d/∂D · 1 m² s⁻¹` ~ 0.1/10⁻¹⁴ = 10¹³. `lg` 미분이어야 맞는다 |
| **D4** | "the first-order index has almost the same value as the total-order index for all parameters" ↔ resolved `σ` 0.14/0.22 · `N_ρ` 0.075/0.15 · `D` 0.008/0.037 | Fig. 8a `[도표]` |
| **D5** | "second-order Sobol-indexes computed with the P2D model are smaller for **all** parameter combinations" ↔ `σN` P2D ≈0.003 > resolved ≈0.000 · `σD` −0.001 > −0.002 · 다수 CI 가 0 포함 · 음의 점추정 | Fig. 8b `[도표]` |
| **D6** | "first and second order sum almost up to the total order indexes" ↔ resolved `D`: `S₁ + ΣS₂` ≈0.007 ↔ `S_T` ≈0.037 | `[재현]` Fig. 8 판독 합 |
| **D7** | Fig. 14a 캡션 "dashed lines … `σ̄` = 0.205 S m⁻¹ and `D̄` = 2.313×10⁻¹⁴" ↔ **점선 색이 바뀌었다**: 주황(σ 색) 점선이 왼축 ≈0.97 = 오른축 **2.33×10⁻¹⁴**(= `D̄`), 파랑(D 색) 점선이 왼축 ≈0.20(= `σ̄`) | `[재현]` 0.97/2.5 × 6×10⁻¹⁴ = 2.33×10⁻¹⁴ |
| D8 | Fig. 14b 캡션 "Open circuit voltage of NMC-622 (**blue** line)" ↔ OCV 는 **주황**(오른축), 파랑은 부피 변화 `f(χ)` | 그림 |
| D9 | Table II "volumetric ratio of AM and SE … = **0.4**" · "porosity 0.2" ↔ `ε_c/(ε_c + ε_el)` = 0.376/0.800 = **0.47**; P2D 복합체는 **2 상**이고 `[인쇄]` "assuming the absence of voids" | 표 ↔ 본문 |
| D10 | "mean values" 가 두 뜻: 스윕 고정값 `σ = 0.32` · `D = 3.16×10⁻¹⁴`(Table IV 상자의 로그 중앙) ↔ Fig. 14a 평균 `σ̄ = 0.205` · `D̄ = 2.313×10⁻¹⁴`(기준 사례) · 기준 `κ` = 1.2×10⁻² ↔ 스윕 중앙 0.032 | 스윕의 중심은 Fig. 3 기준 사례가 **아니다**(G4) |
| D11 | Fig. 4a "In the P2D model, the sandwich lithiation is significantly less prominent but still observable" ↔ `[도표]` P2D 는 3.85 → 3.40×10⁴ **거의 단조**, 끝 상승 ≈0.01×10⁴ | 그림 |
| D12 | "within the solid electrolyte τ_el = 1.54, and within the active material **τ_el** = 1.63" — 둘째는 `τ_c` | 본문 p5 |
| D13 | "physically meaningful boundaries Γ_cc,a-o and **Γ_cc,a-o**" — 둘째는 `Γ_cc,c-o` | 본문 p3 |
| D14 | Fig. 6 "Only small deviations" ↔ 두 번째 방전에서 한 실현이 모델 차의 ≈30 % | `[도표]` |
| D15 | "up to factor five" ↔ `[재현]` 최대 비 **6.4** | Fig. 7 벡터 150 점 |

비고: Table V `n_CPU × t_run` = 48 × 32.8 = 1574 ↔ `t_CPU` 1601.7 h — 표본별 곱의 평균일 수 있어 어긋남으로 세지 않는다. `ε ≈ 13 %`(Fig. 3b)는 벡터 판독 13–15 % 로 정합.

---

# 11. 그림 — 무엇을 봤나

크로퍼(`wiki/tools/extract_figures.py`)가 본문 그림 **15 장**을 잡았다(SI 없음, 표는 크롭되지 않음). **15 장 전부 직접 봤다 — 안 본 그림 0 장.**
추가로 **쪽 렌더 26 장**(p2–p14 좌우 반쪽, 170 dpi)을 만들어 식 · Table II–VI · 부록 B·C · 참고문헌을 읽었고(텍스트 추출은 식과 표 숫자를 잃는다), 고정값 문장 2 곳은 220 dpi 조각으로 확인했다.
벡터 좌표 추출: Fig. 3b(경로 전수 — D1), **Fig. 7(표식 150 전수)**, Fig. 9a(15 + 15), Fig. 11a(15 + 15), Fig. 14b(OCV 경로).
⚠ 크롭 품질: `fig_1.png` 는 **오른쪽 끝이 잘렸다**(`Ω_cc,c` 라벨 · `Γ_cc,c-o`) — p3 렌더로 전체를 봤다. `fig_13.png` 는 위쪽에 Fig. 12b 가 **함께 들어 있다**(열 전체 크롭).
본문 서술과 어긋난 그림: **Fig. 3b**(점선 없음 — D1) · **Fig. 13**(≈0 영역의 `D` 방향 — D2) · Fig. 8(D4–D6) · Fig. 14a(점선 색 — D7) · Fig. 14b(캡션 색 — D8) · Fig. 4a(D11) · Fig. 6(D14).

**지문 도구의 맹점(이 편에서 드러난 것).** IOP/ECS 조판 PDF 는 `fi` 를 **합자 `ﬁ`(U+FB01)** 로 넣는다 — 추출 텍스트를 그대로 `grep identifiab` 하면 **0** 이 나온다. 이 편에서는 결과가 안 바뀌었지만(정규화 뒤 1, 뜻은 "현상이 보인다"),
**`identifiab`·`fit`·`coefficient`·`specific` 류의 지문은 NFKC 정규화 뒤에 세야 한다.** 25~29 지문 표의 다른 JES 행(28)도 같은 위험이 있다.

---

# 12. 참고문헌 중 후속 후보 (53 편 중)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Khalik, Donkers, Sturm, Bergveld 2021** — *J. Power Sources* **499**, 229901 | [27] | ★★★★ 이 편이 "P2D 파라미터를 실험에 맞추는 연구" 로 인용한 둘 중 하나 — (`[추론]` 제목 미인쇄, 원장 확인 필요) DFN 파라미터 **정규화 · 그룹화 · 민감도**로 식별 가능한 조합을 만드는 계보. **곱 쌍(①–③)을 그룹으로 묶는 도구의 원전 후보** | **Q4** |
| **Lu, Trimboli, Fan, Wang, Plett 2022** — *J. Electrochem. Soc.* **169**, 080504 | [28] | ★★★★ 같은 문장의 둘째 인용 — (`[추론]` 제목 미인쇄) Plett 계보의 **집약(lumped) 파라미터 추정**, 곱 쌍을 처음부터 묶어 추정하는 쪽 | **Q4** |
| **Ramadesigan, Northrop, De, Santhanagopalan, Braatz, Subramanian 2012** — *J. Electrochem. Soc.* **159**, R31 | [3] | ★★★ 시스템 공학 관점 리뷰 — 파라미터 추정 · 모델 축약 · 불확실성. "단순 모델의 예측력" 인용처 | Q4 |
| **Krewer, Röder, Harinath, Braatz, Bedürftig, Findeisen 2018** — *J. Electrochem. Soc.* **165**, A3656 | [5] | ★★★ 진단 · 운용용 동역학 모델 리뷰 — 파라미터화 · 관측 가능성 절이 있을 후보 | Q4 |
| **Goldin, Colclasure, Wiedemann, Kee 2012** — *Electrochim. Acta* **64**, 118 | [31] | ★★★ 입자 분해 3D 로 1D 모델의 **경험 파라미터(Bruggeman)** 를 평가한 원전 — 이 편의 균질화 규칙 출처. 24호 굴곡도 페이지의 "`ε·τ²` 분할은 가정" 과 직결 | Q1·Q3 |
| **Neumann, Randau, Becker-Steinberger, Danner, Hein, Ning, Marrow, Richter, Janek, Latz 2020** — *ACS Appl. Mater. Interfaces* **12**, 9277 | [36] | ★★★ NMC622 `D(χ)`·`σ(χ)`·`c_max` 의 출처이자 **sandwich 리튬화**의 선행 — resolved ASSB 모델의 재료 원전 | Q3·Q8 |
| **Schmidt, Sinzig, Wall 2024** — *J. Electrochem. Soc.* **171**, 100502 | [18] | ★★★ 같은 그룹의 **구성요소 사이 박리(delamination)** 확장 — resolved 모델에서 **접촉 손실을 기구로** 넣은 편 | **Q1** |
| **Wirthl, Brandstaeter, Nitzler, Schrefler, Wall 2023** — *Int. J. Numer. Methods Biomed. Eng.* **39** | [37] | ★★ GP 대리 + Sobol 방법 원전 — G1 · G2(대리 검증 · CI 출처) | Q4 방법 |
| **Saltelli, Annoni, Azzini, Campolongo, Ratto, Tarantola 2010** — *Comput. Phys. Commun.* **181**, 259 | [52] | ★★ Sobol 추정기 원전 | Q4 방법 |
| Sobol 2001 — *Math. Comput. Simul.* **55**, 271 | [51] | ★ 전역 민감도 지수 원전 | Q4 방법 |
| **Kirk, Please, Chapman 2021** — *J. Electrochem. Soc.* **168**, 060554 | [24] | ★★ P2D 에 **입자 크기 분포**를 넣은 확장 — §6-3 ② `D/d²` 의 교정 수단 | Q4 |
| **An, Zhou, Li 2021** — *Electrochim. Acta* **370**, 137775 | [29] | ★★ "P2D 로 최적 셀을 정량 식별하는 데 비판적" 인용(29–32) 중 하나 — 적합성 계보 | Q3 |
| A. Schmidt, Ramani, Carraro, Joos, Weber, Kamlah, Ivers-Tiffée 2021 — *Energy Technol.* **9** | [30] | ★★ 같은 인용 묶음 — 미세구조 분해 ↔ 균질화 비교(KIT) | Q3 |
| **Bielefeld 2023** — *Batteries & Supercaps* **6** | [2] | ★★ **원장에 있음**(26호 지목) — 이 편은 "복잡한 모델에서 일반 결론을 끌어내기 어렵다" 쪽으로 인용. **두 번째 지목** | Q4 |
| Neumann, Hamann, Danner, Hein, Becker-Steinberger, Wachsman, Latz 2021 — *ACS Appl. Energy Mater.* **4**, 4786 | [14] | ★ **원장에 있음**(02 지목) — 여기서는 공간전하층 확장의 예로만 | Q2 |
| Kremer, Hoffmann, Danner, Hein, Prifling, Westhoff, Dreer, Latz, Schmidt, Wohlfahrt-Mehrens 2020 — *Energy Technol.* **8**, 1900167 | [44] | ★ NMC622 OCV 출처(D8 곡선) | Q8 |
| Koerver, Zhang, de Biasi, Schweidler, Kondrakov, Kolling, Brezesinski, Hartmann, Zeier, Janek 2018 — *Energy Environ. Sci.* **11**, 2142 | [40] | ★ NMC 부피 변화 측정 — 23호(Koerver 2017 *Chem. Mater.*)와 **다른 논문** | Q1 기구 |
| Randau 외 2020 — *Nat. Energy* **5**, 259 | [41] | ★ LPS `κ` 1.2×10⁻² S m⁻¹ 출처 | 재료 |

⚠ **이 편이 인용하지 않는 것**: Bizeray 2019(**큐 27**, 액체셀 SPM 식별성) · Firouz 2020 · Kim 2019 · Danilov 2011 · Raijmakers 2020 · Naik 2022 · Minnmann 2021 · Bielefeld 2019/2020 · Shi 2020 *AEM* — **원장의 Q4 후보 어느 것도 인용하지 않는다.**
⚠ 식별성 · 역문제 쪽 인용은 **[27] · [28] 두 편을 한 문장("to fit the parameters")에** 쓰고, [3] · [5] 는 모델 복잡도 논쟁 쪽으로 쓴다. QUEENS([53])의 설명문에 "Inverse Problems" 가 있지만 이 편은 쓰지 않는다.
⚠ [27] 의 내용(정규화 · 그룹화)은 **이 편 지면에 없다** — 서지 항목에 제목이 없어서 우리가 붙인 설명은 **확인 전 `[추론]`** 이다.

---

# 13. 이 digest 가 주장하지 않는 것

1. **큰 `κ` 오프셋이 전부 utilization 이라고 단정하지 않는다** — 벡터 판독 차 0.068 과 `1 − u` = 0.07 의 일치, 바닥을 뺀 연결 입자 SOC 0.044 ↔ P2D 0.043 까지가 사실이고, `u` 가 부피 분율인지(G8)·A 로 인한 면적 과대(§6-3 ③)가 같은 자리에서 상쇄되는지는 모른다.
   Fig. 3b 점선(D1)이 있었다면 저자 쪽에서 판정됐을 것이다.
2. **"P2D 유효 영역" 이 틀렸다고 하지 않는다** — `m_SOC ≈ 0` 은 "상수 차이" 라는 뜻으로는 맞다. 주장은 **그 상수가 무엇인지**(접촉 손실)와 **보정이 그것을 용량 손잡이로 흡수한다**는 것까지다.
3. **Sobol 지수 값을 쓰지 않는다** — 래스터 판독(±0.005) · GP 대리 · CI 출처 미상(G1 · G2). D4–D6 은 **저자 문장과 저자 그림의 긴장**까지다.
4. **`D/d²` 선택이 작은 `D` 쪽 차이를 설명한다고 하지 않는다** — `(d₄₃/d̄)²` ≈ 3.5 는 **크기의 후보**이고 풀어 보지 않았다(코드 없음).
5. **Q4 가 움직였다고 하지 않는다** — 데이터가 없고, 저자는 식별성으로 읽지 않았다. 비식별로 읽은 것은 우리다.
6. **이 편의 결론을 액체셀 DFN(우리 truth)으로 옮기지 않는다** — 고체 전해질 · Li 금속 · utilization · 입자 사이 확산은 우리 모델에 없다. 옮긴 것은 **설계의 교훈**(구조 오차는 보정에 흡수된다)까지다.

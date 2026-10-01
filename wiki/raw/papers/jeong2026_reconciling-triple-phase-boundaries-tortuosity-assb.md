---
title: "Jeong et al. 2026 — Reconciling triple-phase boundaries and tortuosity in high-energy all-solid-state lithium-sulfur batteries (Joule 10, 102541)"
description: "탄소 호스트의 입자 크기(전극 스케일 수송)와 기공 크기(입자 스케일 TPB 밀도)를 분리하고 볼밀이 황을 재배치하는 것까지 추적한 PNNL 논문 — 전자 전도도가 6배 낮은 마이크론·마이크로포어 호스트가 율속·수명에서 이긴다, 탄소 21 wt% 복합양극의 σ_e 0.015–0.108 S cm⁻¹ 가 우리 AB 20 wt% 의 첫 외부 눈금"
source_url: local-upload/088387cf-reconciling_triple-phase_boundaries_and_tortuosity_in_high-energy_ASSLSBs.pdf (SI 미확보)
doi: 10.1016/j.joule.2026.102541
ingested: 2026-10-02
sha256: 3dada6f3ea7168958bf757caa2d15ae099257646da7686914dc97e71e8c9ac43
tags: [assb, sulfide-electrolyte, composite-cathode, carbon, mixing-process, units]
compare:
  system: "ASSB Li–S (sulfide, 펠릿). 활물질은 원소 황(S8, 멜트 함침). 음극 2종(Li–In N/P=2 · Li 금속 100 µm). 운전 스택 압력 50 MPa, constant-gap(정용적) 모드. 상온 22 °C(저로딩 수명) 와 60 °C(율속·고로딩·full cell)로 나뉜다"
  electrolyte: "glass-ceramic Li7P2S8Br0.5I0.5 (LPSBI) 자체 합성 — Li2S+P2S5+LiBr+LiI 를 시클로헥산 습식 planetary BM(PM 100, ZrO2, 600 rpm 40 h, BPR 10:1, Ar 밀봉) 후 160 °C 1 h Ar 어닐. 냉간압축 펠릿 5.2 mS cm⁻¹ @상온. 밀도·입도 미기재(→ vol% 환산 불가)"
  cathode: "S : C : SSE = 49 : 21 : 30 wt%, 바인더 없음. S/C 복합체(70:30)를 SE 와 7:3 으로 밀링. 성형 700 MPa 3 min (SE 펠릿은 100 MPa). 측정 양극 밀도 1.79 g cm⁻³. 탄소 호스트 4종 비교 — BP-2000(Mic-S, D50 140 nm, 마이크로포어) · Ketjenblack EC-600JD(Mes-S, 150 nm, 메조포어) · YP-80F(Mic-L, 5.89 µm, 마이크로포어, 승자) · CMK-3(Mes-L, 3.62 µm, 메조포어)"
  li2s_source: "해당 없음 — 활물질이 원소 황(Sigma-Aldrich 99.998 %)이다. Li2S 는 LPSBI 합성 전구체로만 등장한다"
  mixing: "two-step. ① S : 탄소 = 70:30 마노 유발 수동 혼합 → 155 °C 12 h 멜트 함침 → 55 °C 12 h 건조 ② S/C : LPSBI = 7:3, 총 1 g 을 50 mL ZrO2 jar + 3 mm ZrO2 볼 50 g(BPR 50:1), planetary PM 100, 450 rpm, 밀링 5 min + 휴지 10 min 을 48 사이클(순 밀링 4 h / 벽시계 12 h). ②의 분위기 미기재. one-step 대조군 없음"
  loading_mg_cm2: "1.5 (Li–In, 0.5C, 22 °C) · 2 / 4 / 6 (Li–In, 60 °C) · 4 (Li 금속 full cell, 60 °C) — 전부 황(S) 기준. 전극 면적이 본문에 없다(PEEK 몰드 10 mm vs Li 박 9 mm)"
  anode: "Li–In (Li0.5In; Li 박 6 mm 를 In 박 9 mm 아래, In 면이 SE 와 접촉, 100 MPa, 황 로딩에 맞춰 Li 량 조절해 N/P = 2) · Li 금속 (9 mm, 100 µm 박, 100 MPa) — [재현] 100 µm Li = 20.6 mAh cm⁻² 이므로 4 mg cm⁻² 셀의 N/P ≈ 3.4 (Li 과잉)"
  first_charge: "해당 없음 — S8 출발이라 첫 스텝이 방전. 모든 셀이 0.05C 활성화 사이클(Fig. 4D 캡션: 초기 2사이클)을 먼저 돌리는데 그 용량·CE 는 본문·그림 어디에도 없다"
  first_discharge_mAh_gS: "1535.6 (Li 금속, 4 mg cm⁻², 0.2C = 1.34 mA cm⁻², 60 °C, 활성화 2사이클 후) · 1164 (Mic-L, Li–In, 1.5 mg cm⁻², 0.5C, 22 °C) · 1103 (Mic-S 동일) · [도표] 0.2C 율속 Mic-L ≈1410 / Mic-S ≈1375 / Mes-L ≈1300 / Mes-S ≈1000"
  first_discharge_mAh_gLi2S: "[재현] ×0.698 — 1071.8 · 812 · 770 · ≈984 / ≈960 / ≈907 / ≈698"
  cycle_capacity_mAh_gS: "1447 @250 사이클 (94.24 %, Li 금속 4 mg cm⁻², 60 °C) · [도표] ≈1150 @1500 사이클 (Mic-L, Li–In, 1.5 mg cm⁻², 0.5C, 22 °C) · 2C 율속 1070 (Mic-L) vs 338 (Mes-S) — 3배 차"
  cycle_capacity_mAh_gLi2S: "[재현] ×0.698 — 1010 · ≈803 · 747 vs 236"
  areal_mAh_cm2: "9.0 @0.2C (6 mg cm⁻², 60 °C, Li–In) → [인쇄] 7.7 @500 사이클 ([도표] ≈7.1–7.2) · 6.14 @0.2C (4 mg cm⁻², Li 금속) → [도표] ≈5.8 @250 사이클 · [도표] ≈3.0 @1C (2 mg cm⁻²) 1000 사이클. 전극 기준 752.4 mAh g⁻¹(composite) = 1535.6 × 0.49"
  cycles: "1500 (Mic-L, 0.5C, 22 °C, 1.5 mg cm⁻², '무시할 만한 감쇠') vs 425 (Mic-S, 50 % 유지) · 500 (6 mg cm⁻², 60 °C) · 1000 (2 mg cm⁻², 1C) · 250 (Li 금속 full cell, 94.24 %, 0.023 %/사이클). 전부 단일 곡선, 셀 개수·오차막대 없음. 궤적은 비단조(중간 최저점 ≈85 %)"
  temperature_C: "22 (Fig. 4A–4C) · 60 (율속·고로딩·full cell)"
  mechanism: "두 길이 스케일 분리 — ① 호스트 입자 크기가 전극 스케일 수송을 정한다: 작으면 σ_eff,elec 0.104–0.108 S cm⁻¹ (큰 쪽 0.015–0.019, 6배), 크면 σ_eff,ion 4.34×10⁻⁵ S cm⁻¹ (작은 쪽 ≤1.37×10⁻⁵, 3.2배). 율속은 이온 쪽을 따라간다 (2C 유지 76 % vs 50 %). ② 기공 크기가 TPB 밀도를 정한다: 계산 TPB 밀도 [도표] ≈510 (마이크로포어) vs ≈285 µm⁻² (메조포어), 2C 비용량 1070 vs 338 mAh g⁻¹(S). ③ 볼밀이 황을 재배치한다: 수세 후 D50 이 작은 호스트에서 80–150배 증가(0.14→10.7, 0.15→22.3 µm), 밀링 후 결정질 황 XRD 피크 출현(Mic-L 만 예외), 황 없는 대조군은 응집 거의 없음. Young–Laplace 모세관압 마이크로포어 151–198 MPa vs 메조포어 59–64 MPa (2.5–3.4배). ④ 사이클 중 TPB 보존: 첫 방전 후 두께 +46.6 %(Mic-S) vs +36.8 %(Mic-L), 비가역 11.8 %, Δ(ΔP)_Q 와 EIS 성장. TPB 밀도·토르투오시티는 모두 합성 3D 미세구조 모델값(PoreSpy/OpenPNM)이고 측정이 아니다"
  our_axis: "탄소 함량이 21 wt% 로 우리 AB 20 wt% 와 거의 같은 복합양극에서 σ_eff,elec 을 실측했다(0.015–0.108 S cm⁻¹) — 우리 H2a(전자 퍼콜레이션)와 synthesis 반론 3(전자 고원)에 대한 첫 외부 눈금이다. 그리고 전자 전도도가 6배 낮은 쪽이 이김으로써 'σ_e 가 클수록 좋다'를 세 번째로 반증한다(Yu 200배↓·Huang 14배↑ 에 이어). 이식: DC 분극 프로토콜(시료 정체가 가장 명확함), 수세로 밀링 후 S/C 구조를 보는 진단, 전극 기준 용량(mAh g⁻¹_composite)을 1차 지표로 삼는 규율, micron 창 2.5–7 µm(Cronk 0.5–5 µm 와 교집합 2.5–5 µm). 이식 불가: 멜트 함침(Li2S 는 녹지 않는다), Li2S 첫 충전 활성화(S8 계라 무근거), full cell 250 사이클(N/P≈3.4 Li 과잉 + 요오드 SE 의 LiI interphase 기여를 저자가 인정), 성능 절대값"
---
# 수집 목적

M.-G. Jeong, M. Kindle, Y. Xu, J. Bao, J. Wu, U.-H. Kim, D. Jin, S. Jun, Z. Yu, H. Xu, J. Liu,
J. Xiao, **D. Lu**, **"Reconciling triple-phase boundaries and tortuosity in high-energy
all-solid-state lithium-sulfur batteries"**, *Joule* **10** (2026) 102541,
DOI 10.1016/j.joule.2026.102541 (PNNL) 의 **절별 해체분석**. **SI 미확보** (별도 파일).

이 위키가 이 논문을 흡수하는 이유는 셋이다.

1. **이 위키의 첫 synthesis 를 정면으로 시험한다.** 2026-10-01 에 세운 논지
   [[interface-quality-not-bulk-conductivity]] — "이용률을 올리는 것은 전자 네트워크의 벌크
   전도도도 이온 네트워크의 부피분율도 아니라 활물질–황화물 계면의 질이다" — 의 **반론 3**
   ("둘 다 전자 퍼콜레이션 고원 위일 수 있다; 우리 AB 20 wt% 가 그 고원 위인지 아래인지는
   측정되지 않았다")에 이 논문이 직접 답한다. 판정은 **§11** 에 따로 둔다.
2. **제목이 상충을 명시한다.** TPB(삼상 계면)를 늘리는 것과 토르투오시티(수송 경로)를 낮추는
   것이 서로 싸운다는 것이 이 논문의 출발점이다. 우리 [[li2s-assb-composite-cathode]] 의
   조성 선택(30:50:20)은 바로 그 상충 위에 있는 선택인데, 우리는 그 상충을 아직 숫자로
   본 적이 없다.
3. **교신저자 Dongping Lu 는 이 위키의 `raw/papers/qu2025_…`(Nano Energy, 부피변화·스택압)
   공저자다** — 같은 PNNL 계보의 두 번째 논문이다. 한쪽은 압력·부피를 쟀고 이쪽은
   TPB·토르투오시티를 다룬다. 접속은 **§12**.

**표기 규칙** (이 위키 관례 4구분):
- `[인쇄]` — 논문 본문/식/표/캡션에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값을 이 세션에서 산술로 옮긴 것 (계산식을 함께 적는다)

- 원본: `wiki/inbox/088387cf-reconciling_triple-phase_boundaries_and_tortuosity_in_high-energy_ASSLSBs.pdf`
  (14쪽, 9.3 MB). **SI 는 확보하지 않았다** — Joule 은 SI 가 별도 파일이고 본 수집에는 없다.
  본문이 "Figure S…"/"Table S…" 로 넘긴 지점은 **§14 에 전부 목록으로** 두고, 그 내용에 대해
  이 digest 는 **아무것도 추정하지 않는다**.
- 크로핑 그림: `raw/figures/jeong2026_reconciling-triple-phase-boundaries-tortuosity-assb/`
  — 본문 Fig. 1–5 는 `wiki/tools/extract_figures.py` 가 캡션 앵커로 잘랐고, **Scheme 1(p.10)과
  표지의 Graphical abstract(p.1)은 자동 탐지에서 "그래픽 없음" 으로 오판돼 제외됐다.**
  두 장은 bbox 를 수동 지정해 `fig_sch1.png` · `fig_ga.png` 로 다시 자르고 `figures.json` 에
  `note` 로 사유를 남겼다.
- **단위 규율**: 이 논문의 활물질은 **원소 황(S8)** 이다. 모든 비용량은 원문이 `mAh g⁻¹(S)` 로
  적고, 이 digest 는 우리 Li2S 계와 비교하기 위해 **`[재현]` ×0.698 = M(S)/M(Li2S) 환산값을
  항상 병기**한다. 전극 기준 용량(`mAh g⁻¹(electrode)`)은 우리 표기로 `mAh g⁻¹(composite)` 와
  같은 분모다(S+C+SSE 전부). 전압은 원문 표기 그대로 `vs Li/Li⁺` 또는 `vs Li–In` 을 붙인다.
- 페이지 참조는 **PDF 페이지**(1–14).

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

이 절이 이 digest 의 가장 중요한 산출물이다.

| # | 공백 | 왜 문제인가 |
|---|---|---|
| **G1** | **★ 제목에 있는 두 양 — TPB 밀도와 토르투오시티 — 의 숫자가 본문에 하나도 인쇄돼 있지 않다.** 토르투오시티는 Computational details 의 정의식 `τ = σ0/σeff · ε` 하나뿐이고 **τ 값이 본문·캡션 어디에도 없다** (모델 결과는 Figure S1, 미확보). TPB 밀도도 `[도표, Fig. 2B]` 막대 두 개뿐이고 인쇄 숫자가 없다. | **"Reconciling TPB and tortuosity" 라는 제목의 두 축이 모두 정성이다.** 우리가 이 논문을 인용해 "τ 가 얼마다/TPB 가 얼마다" 라고 쓸 수 있는 자리가 없다. 비교는 `[도표]` 비(ratio)로만 가능하다. |
| **G2** | **최적 입자창 "2.5–7 µm" 의 근거가 전부 SI 다** (`[인쇄]` "Particle-size-dependent conductivity modeling (Figure S1C) further defines an optimal host particle window of 2.5–7 μm"). 모델의 입력(입도분포·상 부피분율·벌크 전도도·공극률)도 SI. | 이 논문에서 우리에게 **가장 이식성 높은 한 줄**인데 그 근거를 볼 수 없다. 그리고 실험군 4개 중 이 창 안에 드는 것은 **Mic-L(D50 5.89 µm) 하나뿐**이다 — Mes-L 은 3.62 µm 로 창 안인데 성능이 나쁘다. 즉 **창만으로는 Mes-L 의 패배를 설명하지 못한다** (기공이 설명한다는 것이 논문의 논리). |
| **G3** | **탄소 함량을 변수로 두지 않았다.** 전 실험이 C 21 wt% 고정(S/C 70:30, S/C:SSE 70:30)이다. 바뀐 것은 **탄소의 종류(입자 크기·기공 크기)** 뿐. | σ_eff,elec 가 0.015 ↔ 0.108 S cm⁻¹ 로 **6배 갈리는데** 그것이 탄소 양이 아니라 탄소 형태 때문이다. **"탄소가 모자라면 어떻게 되는가" 는 이 논문에 없다** — 우리 [[reference-cell-500-600-mahg]] H2a 의 핵심 질문(퍼콜레이션 고원의 아래쪽 가장자리)이 비어 있다. §11 참조. |
| **G4** | **입자 크기와 기공 크기가 교락돼 있다.** 네 호스트는 상용품(BP-2000·KB EC-600JD·YP-80F·CMK-3)이고 제조사·합성법·표면화학·비표면적이 전부 다르다. 논문도 이를 인정해 `[인쇄]` Raman·XPS(Figure S10)와 상관분석(Figure S11)을 SI 에 두고 "pore size·particle size 보다 상관이 **far less pronounced**" 라고만 적는다 — **그 상관계수·산점도가 미확보**다. | 2×2 설계처럼 보이지만 **각 칸에 서로 다른 재료 하나씩**이다. "입자 크기가 수송을, 기공 크기가 TPB 를" 이라는 분리는 **4점 관측에 얹힌 귀속**이고, 교란변수 배제의 근거가 전부 SI 에 있다. |
| **G5** | **"small-particle hosts dropped to ∼75%" 가 그림과 맞지 않는다.** `[인쇄, p.4]` "At 0.5C, large-particle hosts retained ∼95% … while small-particle hosts dropped to ∼75%". 그런데 `[도표, Fig. 1F]` 0.5C 에서 **Mic-S(small)는 ≈95 %** 이고 ≈75 % 인 것은 **Mes-S 하나**다. | 본문이 "small vs large" 로 묶어 말하지만 **0.5C 에서 Mic-S 는 large 군과 구별되지 않는다.** 즉 이 조건에서 지배 변수는 입자 크기가 아니라 기공일 수 있다 — 논문 자신의 Fig. 2D/2E 분해와 일치하지만 §"Electrode-scale transport" 의 서술과는 어긋난다. |
| **G6** | **Fig. 3C 가 "큰 입자는 뭉치지 않는다" 와 어긋난다.** `[인쇄]` "large S/C composites such as Mic-L and Mes-L maintained their individual particle sizes without notable agglomeration." `[도표, Fig. 3C]` 밀링 후 D50 은 **Mic-L 5.89 → ≈7.5 µm**, **Mes-L 3.62 → ≈7.2 µm (약 2배)** 다. | Mes-L 의 2배 증가는 "notable" 하지 않다고 말하기 어렵다. 이 논문의 서사(작은 입자만 뭉친다)는 **80–150배 vs 1.3–2배** 라는 *정도*의 차이이지 유무의 차이가 아니다. |
| **G7** | **첫 사이클 용량·첫 CE 가 본문 어디에도 없다.** `[인쇄, Methods]` "Before cycling test, cells underwent **activation cycles at 0.05C**" 이고 `[인쇄, Fig. 4D 캡션]` "All electrodes were cycled at **0.05C for the initial two cycles**". 그 두 사이클의 용량·CE 는 **그림에도 본문에도 없다.** | Fig. 5A 의 "initial capacity 1,535.6 mAh gS⁻¹" 는 **활성화 2사이클 이후의 값**이다. 초기 비가역 손실(= anode-free 로 가면 그대로 Li 재고 손실)이 **측정되었는데 보고되지 않았다**. [[anode-free-li2s-assb]] 에 필요한 바로 그 숫자다. |
| **G8** | **전압창 상한 3.1 V vs Li/Li⁺ 에서의 SE 산화를 다루지 않는다.** SE 가 **요오드·브로민 함유** Li7P2S8Br0.5I0.5 인데, 본문은 LiI 를 `[인쇄]` "LiI-rich interphases that can stabilize Li/SSE contact" 라는 **음극 쪽 이점**으로만 언급하고 **양극 쪽 산화 기여는 검토하지 않는다.** SE-only 대조셀이 없다. | `[재현]` I⁻ 1 e⁻ 산화 몫의 상한은 **17.4 mAh g⁻¹(S)**(계산 §16-3) — 1,535.6 의 **1.1 %** 로 작다. 즉 이 논문은 이 위키의 "이론 초과 용량" 문제군(digest 10편 중 5편)에 **속하지 않는다**. 그러나 그 사실을 저자가 보인 것이 아니라 **우리가 계산해서 알아낸 것**이다. |
| **G9** | **전극 면적이 본문 어디에도 없다.** `[인쇄]` PEEK 몰드 **10 mm**, Li 금속 박 **9 mm**, Li–In 은 In 박 **9 mm** 아래 Li 박 **6 mm**. 복합양극은 "evenly spread on one side of the pellet" 뿐. | `mg cm⁻²`·`mA cm⁻²`·`mAh cm⁻²` 의 분모가 10 mm(0.785 cm²)인지 9 mm(0.636 cm²)인지 모른다. **23 % 차이다.** 또 `[해석]` **Li–In 의 Li 원판이 6 mm(0.283 cm²)로 양극보다 작다** — "N/P = 2" 가 면적당 비율로 성립하려면 양극 면적도 그만큼 작아야 한다. |
| **G10** | **"N/P ratio = 2" 의 계산 근거가 없다.** Li–In 에서 `[인쇄]` "The amount of Li was adjusted based on the sulfur loading to maintain an N/P ratio = 2" 가 전부 — Li 두께·질량·In 두께가 없다. Li 금속 full cell 은 **100 µm 고정**이라 N/P 가 로딩마다 달라지는데 수치가 없다. | `[재현]` Li 100 µm = 0.01 cm × 0.534 g cm⁻³ × 3,861 mAh g⁻¹ = **20.6 mAh cm⁻²**. 4 mg cm⁻² 셀의 6.14 mAh cm⁻² 에 대해 **N/P ≈ 3.4** — **Li 과잉 셀이다.** 250 사이클 94.24 % 는 Li-lean 조건의 결과가 아니다. |
| **G11** | **결론의 숫자 하나가 결과와 어긋난다.** `[인쇄, Conclusions]` "**>750 mAh g_electrode⁻¹ at 6 mg cm⁻²**". 그런데 752.4 mAh g_electrode⁻¹ 는 `[인쇄, p.9]` **4 mg cm⁻²** full cell 값이다(1,535.6 × 0.49 = 752.4 `[재현]`). 6 mg cm⁻² 조건의 값은 `[인쇄]` 9 mAh cm⁻² / 6 mg = 1,500 mAh g⁻¹(S) → `[재현]` ×0.49 = **735 mAh g_electrode⁻¹** 로 **750 미만**이다. | 서론도 같은 묶음을 쓴다(`[인쇄]` ">750 mAh g_electrode⁻¹; >9 mAh cm⁻² at a practical loading (6 mg cm⁻²)"). **두 다른 셀의 값이 한 문장에 묶였다.** 인용할 때 반드시 분리해야 한다. |
| **G12** | **Fig. 4D 의 500 사이클 값이 본문과 다르게 보인다.** `[인쇄]` "retains **7.7 mAh cm⁻²** over 500 cycles" vs `[도표, Fig. 4D]` 6 mg cm⁻² 곡선의 500 사이클 끝점 **≈7.1–7.2 mAh cm⁻²**. | 띠가 두꺼워 판독 오차가 있을 수 있으나 `[해석]` 7.7 은 **500 사이클 중 어느 시점**(예: 초기 안정 구간)의 값일 가능성이 있다. 세미나·인용 시 "500 사이클 후" 로 단정하지 않는다. |
| **G13** | **"stable cycling" 이 CE 인지 용량인지 가려야 하고, 그 궤적이 단조가 아니다.** `[도표, Fig. 4A]` Mic-L 은 1,164 → (≈100–200 사이클) ≈1,130 → (≈600–750 사이클) **≈1,280 상승** → (1,500 사이클) ≈1,150 으로 **올라갔다 내려온다**. `[도표, Fig. 5A]` full cell 도 1,535.6 → (≈75 사이클) **≈1,300 (≈85 %)** → (250 사이클) 1,447 로 **V 자**다. | **"94.24 % retention over 250 cycles" 는 양 끝점의 비일 뿐**이고 중간 최저점은 ≈85 % 다. 같은 셀이 왜 회복하는지(densification? 온도? 활성화 지연?)에 대한 설명이 Fig. 4B 의 초기 5사이클 densification 언급 외에는 없다. |
| **G14** | **셀 개수·오차막대가 전무하다.** Fig. 1E(전도도 막대)·1F·2B·2D·2E·4A–4D·5A 전부 **단일 값/단일 곡선**이고 반복 횟수 표기가 없다. Methods 에도 n 이 없다. | 이 논문의 모든 결론이 **조건당 셀 1개**일 가능성을 배제하지 못한다. 특히 Fig. 1E 의 σ_eff,ion 4.34×10⁻⁵ vs 1.37×10⁻⁵(3.2배)와 Fig. 2B 의 TPB 1.8배가 시료 간 분산보다 큰지 판정 불가. |
| **G15** | **복합양극 볼밀 ②단계의 분위기가 미기재다.** SE 합성(①)은 `[인쇄]` "A sealed and argon (Ar)-filled milling vessel was used" 라고 명시했는데, S/C + LPSBI 혼합 단계는 용기·볼·rpm·시간은 다 적고 **분위기만 빠졌다**. | 황화물 SE 는 미량 수분에 H2S 를 낸다. 재현하려면 Ar 밀봉 여부가 필요하다. 우리 [[composite-cathode-mixing-routes]] 표의 "분위기" 열이 또 비는 사례다 (Kim 2023 G1 과 같은 부류). |
| **G16** | **one-step 대조군이 없다.** 이 논문의 경로는 **two-step**(멜트 함침 → SE 와 볼밀)인데, 같은 조성을 **한 번에** 간 대조군이 없다. 즉 "멜트 함침이 필요하다" 는 이 논문 안에서 검증되지 않았다 — 인용(refs 24, 25)으로만 뒷받침된다. | [[one-step-vs-two-step-mixing]] 의 축에 직접 걸린다. Cronk 2026 은 같은 축에서 **one-step 이 이긴다**고 보고했다 (§13). 두 논문은 서로의 대조군을 갖고 있지 않다. |
| **G17** | **밀링이 만드는 계면상을 찾지 않았다.** 이 논문은 밀링의 효과를 **황의 물리적 재배치**(결정질 황 석출·응집·C/SSE passivation)로만 본다. 밀링이 황 표면에 **화학적 계면상**(예: 황 과잉 thiophosphate)을 만드는지에 대한 측정(Raman shift·XANES pre-edge·XPS)이 **하나도 없다**. | Cronk 2026 은 **정확히 그 계면상을 밀링의 이득**으로 제시한다. 두 논문이 같은 공정의 **반대 효과**를 보고 있는데 서로의 관측을 측정하지 않았다 — §13·§16-5. |
| **G18** | **Figure S17(단면 SEM)의 숫자가 본문에 흩어져 있고 귀속이 모호하다.** `[인쇄]` 첫 방전 후 두께 증가 Mic-S **46.6 %** vs Mic-L **36.8 %**; 이어 "This behavior is associated with the severe **irreversible thickness increase of 11.8 %** and the larger crack/void fraction after cycling". **11.8 % 가 어느 시료인지, 몇 사이클 후인지, crack/void 분율이 몇 %인지** 적혀 있지 않다. | 문맥상 Mic-S 로 읽히지만 확정 불가. void 분율은 `[인쇄]` ImageJ Trainable Weka 로 **분할했다고 적어놓고 수치를 주지 않는다.** |
| **G19** | **에너지밀도 추정(Fig. 5C)의 전제가 전부 Table S3(미확보)에 있다.** 본문이 주는 것은 `[인쇄]` "5-Ah ASSLSB design **including current collectors, tabs, and packaging but excluding external stack hardware**", 양극 밀도 **1.79 g cm⁻³**, 양극 지표 **4 mg cm⁻² · ~50 wt% S · 1,500 mAh g⁻¹(S)** 뿐. Li 두께·집전체 두께·N/P·SE 밀도가 없다. | ">350 Wh kg⁻¹ at ≤90 µm", ">500 Wh kg⁻¹ at <~40 µm" 라는 이 논문의 셀 수준 주장은 **재현도 반박도 불가**하다. 특히 **50 MPa 스택 압력을 유지하는 하드웨어가 분모에서 빠져 있다**(저자도 "excluding external stack hardware" 라고 명시). |
| **G20** | **50 MPa 운전 스택 압력의 근거·민감도가 없다.** `[인쇄]` "The relatively high pressures (**50 MPa**) used in this study were necessary to ensure sufficient densification … However, practical systems must ultimately operate at significantly lower pressures." 압력을 낮췄을 때 무엇이 먼저 깨지는지에 대한 데이터가 **없다**. | **같은 그룹 Qu 2025 는 운전 압력을 `[인쇄]` "approximately 7 MPa" 로 적는다** — 7배 차이다. 두 논문이 같은 저자를 공유하면서 운전 압력 기준이 다르다 (§12). |
| **G21** | **Li7P2S8Br0.5I0.5 의 밀도·입도가 없다.** SE 합성 조건과 전도도(5.2 mS cm⁻¹)는 있으나 밀도·D50 이 없다. | **wt% → vol% 환산을 할 수 없다.** 그래서 이 논문의 SSE 30 wt% 가 우리 LPSCl 50 wt%(= `[재현]` 48–52 vol%) 대비 부피로 얼마인지 **계산 불가**다 — Wang 2023 축(SE 부피분율)과 이 논문을 잇는 다리가 없다. |
| **G22** | **σ_eff 측정 펠릿과 셀 양극의 성형 압력이 다르다.** `[인쇄]` 셀 양극은 SE 펠릿 위에 **700 MPa 3 min**; 전도도용 ion-blocking 펠릿은 **700 MPa**, **electron-blocking 펠릿은 200 MPa** 로 먼저 누른 뒤 양면에 LPSBI 를 700 MPa 로 붙인다. | **σ_eff,elec 과 σ_eff,ion 이 서로 다른 밀도의 시료에서 측정됐다.** 200 MPa 쪽이 덜 치밀하므로 σ_eff,ion 은 셀 양극(700 MPa)보다 **낮게 나올 수 있다**. 두 전도도의 절대값을 같은 전극의 성질로 묶어 읽으면 안 된다. (Huang 2026 G6 · Yu 2024 G14 와 같은 부류의 공백이지만, **이 논문은 시료 정체 자체는 명시했다** — 그 점에서 둘보다 낫다.) |
| **G23** | **상온 1,500 사이클(Fig. 4A)은 로딩 1.5 mg cm⁻²** 다. 고로딩(6 mg cm⁻²) 데이터는 전부 **60 °C** 이고, 상온 고로딩 데이터는 없다. | 제목의 "high-energy" 와 "stable cycling" 이 **같은 셀의 성질이 아니다.** 상온 = 저로딩, 고로딩 = 60 °C. 우리 상온 셀에 옮길 때 반드시 구분해야 한다. |
| **G24** | **Mic-L(YP-80F)의 기공부피·비표면적이 본문에 없다.** `[인쇄]` "Based on the measured pore volumes and corresponding calculation (Figure S3), **70 wt % sulfur** was infiltrated into all S/C composites, representing the **maximum loading** that can be accommodated within the available pore volume of all four carbon hosts." Table S1(기공 제원)이 미확보. | **70 wt% 가 "네 호스트 중 가장 작은 기공부피" 에 맞춘 값**이라는 뜻이다. 즉 Mic-L 은 기공이 남았을 수도 있고 꽉 찼을 수도 있다 — "confinement" 서사의 정량 근거가 전부 SI 에 있다. |

---

## 0. 서지사항 (직접 확인)

| 항목 | 값 | 확인 위치 |
|---|---|---|
| 제목 | Reconciling triple-phase boundaries and tortuosity in high-energy all-solid-state lithium-sulfur batteries | p.1–2 표제 |
| 저자 | Min-Gi Jeong¹, Michael Kindle¹, Yaobin Xu¹, Jie Bao¹, Jing Wu¹, Un-Hyuck Kim¹, Dahee Jin¹, Seunggoo Jun¹, Zhaoxin Yu¹, Hongliang Xu¹, Jun Liu^{1,2}, Jie Xiao^{1,2}, **Dongping Lu**^{1,3} (교신·lead contact, dongping.lu@pnnl.gov) | p.2 |
| 소속 | 1 Energy and Environment Directorate, **Pacific Northwest National Laboratory**, Richland, WA 99354 · 2 Dept. of Mechanical Engineering, University of Washington, Seattle | p.2 |
| 저널 | **Joule** **10**, 102541, November 18, 2026 | p.1 꼬리글 |
| DOI | **10.1016/j.joule.2026.102541** | p.1–2 |
| 투고 이력 | Received **February 11, 2026** · Revised **April 29, 2026** · Accepted **June 2, 2026** | p.12 |
| 저작권 | © 2026 Elsevier Inc. All rights are reserved, **including those for text and data mining, AI training, and similar technologies** | p.1 |
| 지원 | DOE Office of Critical Minerals and Energy Innovation (CMEI) · Vehicle Technologies, Advanced Battery Materials Research (BMR), 계약 DE-AC02-5CH11231 · DE-AC02-98CH10886. TEM 은 EMSL(PNNL). PNNL 은 Battelle, DE-AC05-76RL01830 | p.12 |
| 데이터 | `[인쇄]` "All data … shared by the lead contact upon request." / "This paper **does not report original code**." | p.12 |
| 이해관계 | `[인쇄]` "The authors declare no competing interests." | p.12 |
| 생성형 AI | `[인쇄]` "the authors used Open AI for language and edit" (원문 표기 그대로) | p.12 |
| Highlights | `[인쇄]` ① "Two-length-scale carbon-host design for solid sulfur cathodes" ② "Micron-scale and microporous hosts identified as optimal cathodes" ③ "High sulfur utilization and stable cycling achieved at high sulfur loading" | p.1 |

---

## 1. 한 문단 요약

전고체 황 양극에서 반응은 **S/C/SSE 삼상 계면(TPB)에서만** 일어나는데, TPB 를 국소적으로
최대화하는 구조는 전극 전체의 이온 경로를 **더 구불구불하게(tortuous)** 만든다 — 이것이
이 논문이 세운 상충이다. 저자들은 그 상충을 **탄소 호스트의 두 길이 스케일로 분해**한다:
**이차입자 크기**가 전극 스케일 수송(퍼콜레이션·토르투오시티)을 정하고, **기공 크기**가
입자 스케일 TPB 밀도를 정한다는 것이다. 상용 다공성 탄소 4종을 2(입자) × 2(기공) 로 골라
(`[인쇄]` 마이크로포어·나노입자 **BP-2000 = Mic-S**, 메조포어·나노입자 **KB EC-600JD = Mes-S**,
마이크로포어·마이크론입자 **YP-80F = Mic-L**, 메조포어·마이크론입자 **CMK-3 = Mes-L**)
각각에 **70 wt% 황을 멜트 함침**하고 **S/C : SSE = 70 : 30** 으로 밀링해 최종 **S : C : SSE =
49 : 21 : 30 wt%** 양극을 만든다. 측정 결과 **작은 입자 쪽이 σ_eff,elec 이 6배 높고(0.104–0.108
vs 0.015–0.019 S cm⁻¹), 큰 입자 쪽이 σ_eff,ion 이 3배 높다(4.34×10⁻⁵ vs ≤1.37×10⁻⁵ S cm⁻¹)**.
율속은 **전자가 아니라 이온 쪽을 따라간다** — 2C 에서 큰 입자군 최고 76 % vs 작은 입자군 최고
50 % (`[인쇄]`). 기공 쪽에서는 마이크로포어가 황을 더 잘게 가둬 TPB 밀도를 `[도표]` ≈1.8배
올리고, 2C 비용량이 **1,070(Mic-L) vs 338(Mes-S) mAh g⁻¹(S)** 로 **3배** 벌어진다. 여기에
세 번째 축이 더해진다 — **볼밀이 황을 움직인다.** SSE 를 물로 씻어내고 본 S/C 구조에서
작은 입자군의 D50 이 **0.14 → 10.7 µm (≈80배)**, **0.15 → 22.3 µm (≈150배)** 로 뭉쳤고
XRD 에 **결정질 황이 새로 나타났다 — Mic-L 만 예외**다. 저자는 이것을 **Young–Laplace
모세관압**(마이크로포어 **151–198 MPa** vs 메조포어 **59–64 MPa**, 2.5–3.4배)과 확산거리로
설명하고, "선행 연구들의 기공 크기 효과가 서로 어긋난 이유가 바로 이 공정 유도 재배치"
라고 주장한다. 최종적으로 **Mic-L** 양극이 Li–In 상온 0.5C 에서 **1,500 사이클 거의 무감쇠**
(Mic-S 는 425 사이클에 50 %), 60 °C 6 mg(S) cm⁻² 에서 **9 mAh cm⁻²**, Li 금속 full cell
4 mg cm⁻²·0.2C·60 °C 에서 **1,535.6 mAh g⁻¹(S) = `[재현]` 1,071.8 mAh g⁻¹(Li2S) =
752.4 mAh g⁻¹(composite)** 와 **250 사이클 94.24 %** 를 낸다.

---

## 2. p.1–3 — Highlights / CONTEXT & SCALE / SUMMARY / INTRODUCTION

### 2.1 SUMMARY 의 명제 `[인쇄]`

> "their practical performance is limited by low-density triple-phase-boundaries (TPBs) and
> tortuous ionic/electronic paths. Here, we report a **two-length-scale architectural design**
> for a solid sulfur cathode. By **decoupling host particle size (electrode-scale transport)
> from pore size (particle-scale kinetics)** and **tracking processing-induced sulfur
> redistribution**, we show that microporous, micron-scale carbon hosts can satisfy these
> competing constraints."

> "The resulting cathodes deliver extremely high sulfur utilization (**>1,500 mAh gS⁻¹**),
> areal capacity (**>9 mAh cm⁻²**) with high sulfur content (**∼50 wt %**), and **94.2%
> capacity retention over 250 cycles at 6 mAh cm⁻²** in lithium-metal full cell."

`[해석]` 초록의 이 묶음이 **G11 의 출처**다 — ">1,500 mAh gS⁻¹" 과 ">9 mAh cm⁻²" 는 6 mg cm⁻²
Li–In 셀, "94.2 % over 250 cycles at 6 mAh cm⁻²" 는 **4 mg cm⁻² Li 금속** 셀이다. 초록은
세 셀의 값을 한 문장에 묶었다.

### 2.2 CONTEXT & SCALE 가 세운 상충 `[인쇄]`

> "Realizing practical high-sulfur-content cathodes … requires navigating a fundamental
> trade-off, i.e., achieving **dense sulfur/carbon/solid-electrolyte triple-phase boundaries
> (TPBs)** while maintaining **low-tortuosity ion and electron transport** through thick
> electrodes."

> "**particle size primarily dictates electrode-level ionic transport, whereas pore size
> determines TPB density**. Incorporating microporosity further **restricts sulfur
> redistribution during electrode processing**."

★ `[해석]` 이 두 문장이 이 논문 전체의 주장이고, 이 digest 가 §11 에서 우리 논지와 대조하는
대상이다. 주목할 것 — 저자는 입자 크기를 **"ionic transport"** 에 귀속시킨다. **전자 전도도는
작은 입자가 더 좋은데도 성능은 큰 입자가 좋다**는 관측이 이 귀속의 근거다 (§4.3).

### 2.3 INTRODUCTION 의 문제 설정 `[인쇄]`

- 액체계 Li–S 의 문제: polysulfide 용해·이동 → 황 손실·전해질 소모·Li 부식 (refs 3–6).
- ASSLSB 의 남은 문제: `[인쇄]` "short cycle life, the need for **high operating pressure**,
  and practically low energy."
- 음극 쪽: `[인쇄]` "thiophosphate solid electrolytes are vulnerable to **Li creeping along
  grain boundaries under high stack pressures** and when **ultrathin (<30 μm) separator
  layers** are used, which accelerates filament formation and leads to internal shorting"
  (refs 9, 10 = Doux 2020 · Ning 2023).
  `[해석]` **이 논문은 자기 셀을 50 MPa 로 돌리면서 서론에서 "높은 스택 압력이 Li creeping 을
  유발한다" 고 쓴다.** 그리고 Fig. 5C 의 에너지 추정은 **SE 분리막을 40–90 µm 로 얇게 하는
  것**에 의존한다 — 서론이 위험하다고 적은 바로 그 방향이다. 내부 긴장이다 (§16-2).
- 양극 쪽 핵심 문장: `[인쇄]` "In the absence of soluble intermediates, the sulfur conversion
  reaction is **largely confined to the triple-phase boundaries (TPBs)**… As the sulfur
  fraction increases to levels necessary for high energy density, the **effective S/C/SSE TPB
  density decreases** and **ionic transport pathways become increasingly tortuous**."
- 상충의 명시: `[인쇄]` "architectures that **locally maximize TPBs can increase tortuosity**
  and isolate SSE percolation globally, while architectures optimized for transport may
  **reduce TPB density** and slow conversion kinetics." (refs 15–18)
- 액체계 설계규칙의 비이식성: `[인쇄]` "design rules established for liquid-electrolyte Li-S
  batteries **do not translate directly to solid-state cathodes**." 액체계에서 마이크로포어는
  **Lennard-Jones 퍼텐셜 중첩에 의한 나노스케일 흡착**으로 polysulfide 를 가두고, 메조포어는
  **황 침투 부피와 수송 경로**를 준다 (refs 1, 19, 20).
  ★ `[해석]` **고체계에는 polysulfide 가 없으므로 마이크로포어의 "흡착" 이유가 사라진다.**
  이 논문이 마이크로포어에 주는 새 이유는 **① TPB 밀도 ② 모세관 구속(공정 중 황 고정)** 두 개다.
- 선행 연구의 불일치: `[인쇄]` "compared with that of their mesoporous counterparts, the
  performance of **microporous carbons tends to be less consistent across different research
  groups**" (refs 21, 30). 이 논문은 그 불일치를 **공정(밀링) 변수**로 설명한다고 주장한다.
- 이 논문이 쓰는 도구 4종 `[인쇄]`: "**mesoscale transport simulations**, **effective
  ionic/electronic conductivity measurements**, **computed TPB metrics**, and **operando
  chemo-mechanical diagnostics**."

---

## 3. p.10–12 — METHODS 전문 (재현에 필요한 전부)

★ 이 논문은 STAR Methods 가 **본문 PDF 안에** 있다. 아래는 전문을 옮긴 것이다.

### 3.1 고체전해질 LPSBI 합성 `[인쇄]`

| 항목 | 값 |
|---|---|
| 조성 | glass-ceramic **Li7P2S8Br0.5I0.5 (LPSBI)** |
| 전구체 | Li2S (Sigma-Aldrich, anhydrous, 99 %) · P2S5 (Sigma-Aldrich, 99 %) · LiBr (99.99 %) · LiI (99.99 %), 화학량론비 |
| 전처리 | 글러브박스 안 **마노 유발 수동 분쇄** |
| 밀링 | **planetary PM 100 (RETSCH)**, **지르코니아 볼**, **600 rpm, 40 h**, 용매 **시클로헥산(습식)**, **BPR 10 : 1** |
| 분위기 | **밀봉 Ar 충전 용기** (수분·공기 오염 방지 명시) |
| 후처리 | 건조 → **160 °C 1 h, Ar 어닐** |
| 전도도 | **5.2 mS cm⁻¹ @ 상온, 냉간압축 펠릿** |

`[해석]` 우리 LPSCl(상용)과 다르다. **요오드·브로민을 함유**하고, Cl 이 없다. Li–In 기준전위
환산이나 산화 개시 전위를 우리 LPSCl 과 같다고 가정하면 안 된다.

### 3.2 복합양극 (★ [[composite-cathode-mixing-routes]] 에 그대로 들어간다) `[인쇄]`

**① S/C 복합체 — 멜트 함침 (two-step 의 앞 단계)**

| 항목 | 값 |
|---|---|
| 탄소 호스트 4종 | **BP-2000** (Black Pearls, Cabot) · **KB EC-600JD** (Ketjen Black, Nouryon) · **YP-80F** (Kuraray) · **CMK-3** (ACS Material) |
| 탄소 전처리 | **진공 150 °C 12 h 건조** |
| 황 | Sigma-Aldrich **99.998 %** |
| 혼합 | S : C = **70 : 30 (w/w)**, **마노 유발 수동 혼합** |
| 함침 | **155 °C 12 h 열처리** |
| 건조 | **55 °C 12 h** |

**② 복합양극 — SE 와 볼밀 (two-step 의 뒤 단계)**

| 항목 | 값 |
|---|---|
| 조성 | S/C : LPSBI = **7 : 3 (w/w)**, **총 투입량 1 g** |
| 용기 | **50 mL 지르코니아 jar** |
| 볼 | **3 mm ZrO2, 50 g** → **BPR = 50 : 1** `[재현]` |
| 장비·속도 | **planetary PM 100 (RETSCH)**, **450 rpm** |
| 시간 | **48 사이클 (12 h)**, 1사이클 = **밀링 5 min + 휴지 10 min** → `[재현]` **순 밀링 4 h**, 휴지 8 h |
| 분위기 | **미기재 (G15)** |
| **최종 전극 조성** | **S : C : SSE = 49 : 21 : 30 (wt%)** |
| 황 무함유 대조 | C : LPSBI = **21 : 30**, 동일 밀링 조건 |

★★ `[해석]` 우리 설계와 대조:

| | 이 논문 (Jeong 2026) | 우리 reference cell |
|---|---|---|
| 활물질 | S8 **49 wt%** (= `[재현]` Li2S 환산 70 wt%) | Li2S **30 wt%** |
| 탄소 | 다공성 호스트 **21 wt%** | AB **20 wt%** |
| SE | LPSBI **30 wt%** | LPSCl **50 wt%** |
| 경로 | **two-step** (멜트 함침 → 밀링) | — |
| 밀링 | 450 rpm · **순 4 h** · BPR **50:1** · 간헐(5/10) | — |

**탄소 함량이 거의 같다 (21 vs 20 wt%).** 이것이 §11 판정의 핵심 근거다 — 이 논문의
σ_eff,elec 측정값이 **우리 탄소 함량대의 복합양극 전자 전도도에 대한 첫 외부 기준점**이 된다.

### 3.3 셀 조립 `[인쇄]`

| 층 | 조건 |
|---|---|
| SE 펠릿 | LPSBI **80 mg**, **PEEK 몰드 10 mm 지름**, **Ti 로드 집전체**, **100 MPa** 펠릿화 |
| 복합양극 | SE 펠릿 한쪽 면에 고르게 펴고 **700 MPa 3 min** 압착 |
| 황 로딩 | **1.5 – 6 mg(S) cm⁻²** 로 조절 |
| Li 금속 음극 | **9 mm Li 박, 100 µm 두께**, 반대면에 **100 MPa** |
| Li–In 음극 | **6 mm Li 박**을 **9 mm In 박** 아래 두고 가볍게 눌러 **Li0.5In** 형성. **황 로딩에 맞춰 Li 량 조절, N/P = 2.** **In 면이 SE 와 접촉**, **100 MPa** |
| 분위기 | **건조 Ar 글러브박스, H2O < 0.1 ppm, O2 < 0.1 ppm** |
| **운전 스택 압력** | **모든 셀 constant-gap(정용적) 모드, gap 을 조절해 50 MPa 인가** |

★ `[해석]` **성형 압력(700 MPa) 과 운전 스택 압력(50 MPa) 이 명확히 분리돼 적혀 있다** —
이 위키가 digest 마다 요구하는 구분이 이 논문에는 있다. 그리고 **구속 방식이 constant-gap
= 정용적**이다. Qu 2025 는 정용적이 정압보다 **나쁘다**고 보고했다 (§12).

### 3.4 전도도 측정 (★ 가장 이식성 높은 방법) `[인쇄]`

| 항목 | 값 |
|---|---|
| 시료량 | 복합체 **50 mg** 을 몰드 셀에 장입 |
| **ion-blocking 셀**(→ σ_eff,elec) | 펠릿을 **700 MPa** 로 압축 |
| **electron-blocking 셀**(→ σ_eff,ion) | 펠릿을 **200 MPa** 로 압축 후 **양면에 LPSBI 100 mg 씩을 700 MPa 로** 압착 |
| 양쪽 공통 | **Li–In 합금을 양면에 100 MPa 로 부착** |
| 측정 | **DC 분극**, VMP-3 (BioLogic). **−50 ~ +50 mV 정전압을 각 1 h 유지**해 정상상태 도달 |
| 계산 | **R = U/I** (옴의 법칙), **σ = L / (R × A)**, A = 전극 면적, L = 두께 |

★★ `[해석]` **이 위키의 세 번째 DC 분극 논문이고, 시료 정체를 가장 분명히 적은 논문이다.**
Huang 2026(G6)·Yu 2024(G14)는 "무엇을 쟀는지" 가 불명이어서 [[interface-quality-not-bulk-conductivity]]
반론 1 의 근거가 됐다. 이 논문은 **"복합체 50 mg", "ion-blocking", "electron-blocking",
인가 전압 ±50 mV, 유지 1 h** 를 전부 적는다. 다만 **두 측정의 성형 압력이 다르다(G22)** 는
새 공백이 생겼다.

### 3.5 전기화학 조건 `[인쇄]`

| 시험 | 음극 | 온도 | 전압창 | 로딩 | 전류 |
|---|---|---|---|---|---|
| **율속**(Fig. 1F·2D·2E) | **Li 금속** | **60 °C** | **1.3 – 3.1 V vs Li/Li⁺** | **4 mg(S) cm⁻²** | 방전 **0.1C → 2C 단계적**, **충전은 0.1C 고정**. **1C = 1,672 mA g⁻¹** |
| **구조 안정성**(Fig. 4A–4C) | **Li–In** | **상온 (22 °C)** | `[도표, Fig. 4A]` **0.7 – 2.5 V vs Li-In/Li⁺** (원문 축 표기 그대로) | **1.5 mg cm⁻²** | **1.25 mA cm⁻² (0.5C)** |
| **고로딩**(Fig. 4D) | **Li–In** | **60 °C** | **0.7 – 2.5 V (vs Li-In/Li⁺)** | **2 / 4 / 6 mg cm⁻²** | **0.2C – 1C** |
| **full cell**(Fig. 5A·5B) | **Li 금속** | **60 °C** | **1.3 – 3.1 V vs Li/Li⁺** | **4 mg cm⁻²** | **0.2C = 1.34 mA cm⁻²**, `[도표, Fig. 5B]` **CCCV** |
| 공통 | — | — | — | — | **사이클 전 0.05C 활성화 사이클**(Fig. 4D 캡션: **초기 2사이클**) |
| EIS | — | — | — | — | **7 MHz – 0.05 Hz**, 사이클 전/후 |
| operando 압력 | — | — | — | — | **RSB 2 로드셀 (Loadstar Sensors)** 를 셀 스택 아래, **LoadVUE Pro** 로 실시간 |

`[재현]` 전압창 일치 확인 — Li–In ≈ +0.62 V vs Li/Li⁺ 를 쓰면 0.7–2.5 V vs Li–In 은
**1.32 – 3.12 V vs Li/Li⁺** 로 Li 금속 셀의 1.3–3.1 V 와 **같은 창**이다. 두 셀이 같은
전위창에서 돌았다는 뜻이다. (Li–In 전위 0.62 V 의 출처는 이 논문이 아니라
`raw/papers/wang2023_…` 이다.)

`[재현]` C-rate ↔ 전류 일치 확인 — 1C = 1,672 mA g⁻¹ 기준:
- 6 mg cm⁻² × 0.2C → 1,672 × 0.2 × 0.006 = **2.006 mA cm⁻²** ✓ (Fig. 4D "2 mA cm⁻² (0.2C)")
- 4 mg cm⁻² × 0.5C → 1,672 × 0.5 × 0.004 = **3.344 mA cm⁻²** ✓ ("3.34 mA cm⁻² (0.5C)")
- 2 mg cm⁻² × 1C → 1,672 × 1 × 0.002 = **3.344 mA cm⁻²** ✓ ("3.34 mA cm⁻² (1C)")
- 4 mg cm⁻² × 0.2C → 1,672 × 0.2 × 0.004 = **1.338 mA cm⁻²** ✓ (Fig. 5A "1.34 mA cm⁻²")
- 1.5 mg cm⁻² × 0.5C → 1,672 × 0.5 × 0.0015 = **1.254 mA cm⁻²** ✓ (Fig. 4A "1.25 mA cm⁻²")
- 4 mg cm⁻² × 2C → 1,672 × 2 × 0.004 = **13.376 mA cm⁻²** ✓ (Conclusions "13.4 mA cm⁻²")

→ **전류 표기는 전부 내부 정합한다.** (로딩 계산의 면적이 무엇인지는 여전히 모른다 — G9.)

### 3.6 재료 분석 `[인쇄]`

| 도구 | 조건 |
|---|---|
| SEM | FE-SEM **JSM-IT200 (JEOL)** |
| **SSE 제거(수세)** | **탈이온수에 24 h 침지** → **2,000 rpm 10 min 원심분리** → **상온 진공건조** |
| 단면 | 기계적 파단; 고분해능은 **Ar 이온빔 cross-section polisher IB-19520CCP (JEOL)**, **극저온 −100 °C**, **기밀 이송 용기** |
| 공극·균열 정량 | **ImageJ/Fiji 의 Trainable Weka Segmentation** — 대표 영역 수동 라벨링으로 픽셀 분류기 학습 후 전 단면에 적용 |
| 입도 | **Malvern Mastersizer 3000E**, **IPA : 물 = 7 : 3 (v/v)** 에 분산, **초음파 3 min** |
| 기공 | **N2 흡착 77 K, Quadrasorb EVO**. 탈기: 탄소 호스트 **100 °C**, 복합양극 **30 °C**, 각 12 h. 전 기공부피·기공분포는 **DFT 법** |
| TEM | **300 kV FEI Titan** |
| XRD | **Rigaku MiniFlex II**, Cu Kα (λ = 1.5418 Å), 2θ **10–70°** |
| TGA | **STA 449 (Netzsch)**, **N2**, **10 °C min⁻¹, 600 °C 까지** |

★ `[해석]` **수세(물 24 h)로 SSE 를 녹여내고 남은 S/C 를 본다**는 아이디어가 이 논문에서 가장
값싸고 이식성 높은 실험이다. 황화물 SE 는 물에 분해되고 황·탄소는 남는다. **우리 복합양극에
그대로 적용 가능**하다 (단 H2S 발생 — 후드·중화 필요). §17 참조.

---

## 4. p.3–5 — 결과 ① 전극 스케일 수송은 **호스트 입자 크기**가 정한다 (Fig. 1)

### 4.1 메조스케일 시뮬레이션 (Fig. 1A–1C) `[인쇄 + 도표]`

`[인쇄]` "We first isolated this electrode-scale effect using **mesoscale simulations of coupled
ionic/electronic conduction** in composite electrodes with a **fixed S/C:SSE mass ratio** and
**varied S/C particle size**."

> `[인쇄]` "The simulations reveal a trade-off — **smaller S/C particles promote a more
> homogeneous electronic network, whereas larger S/C particles produce more continuous ionic
> current pathways through the SSE phase**" (Figures 1A–1C, S1A, S1B).

`[도표, Fig. 1B·1C]` 두 쌍의 12.8 µm 정육면체 미세구조에 전류밀도를 **0 – 0.20 A cm⁻²** 컬러
스케일로 칠했다. **Small** 쪽은 두 패널 모두 **거의 전부 진한 남색(≈0)** 이고 미세한 그물만
보인다. **Large** 쪽은 **주황–적색(0.15–0.20 A cm⁻²) 핫스팟이 뚜렷**하다.
`[해석]` 즉 "Large 가 좋다" 는 그림이 아니라 **"Large 는 전류가 소수의 굵은 경로에 집중되고
Small 은 넓고 가늘게 퍼진다"** 는 그림이다. 색 스케일이 같으므로 총 전류의 비교는
이 그림만으로는 할 수 없다 (그 수치가 Figure S1A·S1B 에 있고 미확보).

`[인쇄]` "Particle-size-dependent conductivity modeling (**Figure S1C**) further defines an
**optimal host particle window of 2.5–7 μm**, which balances robust electronic percolation
with continuous ionic pathways." → **G2** (근거 미확보).

### 4.2 호스트 4종의 제원 `[인쇄 + 도표]`

| 라벨 | 상용명 | 기공 | **D50** | 전자 전도도 군 |
|---|---|---|---|---|
| **Mic-S** | **BP-2000** (Black Pearls, Cabot) | 마이크로포어 **<2 nm** (`[도표, Fig. 2E]` ≈1.65 nm) | **140 nm** | small (높음) |
| **Mes-S** | **Ketjenblack EC-600JD** (Nouryon) | 메조포어 **2–10 nm** (`[도표]` ≈4.1 nm) | **150 nm** | small (높음) |
| **Mic-L** | **YP-80F** (Kuraray) | 마이크로포어 **<2 nm** (`[도표]` ≈1.3 nm) | **5.89 µm** | large (낮음) |
| **Mes-L** | **CMK-3** (ACS Material) | 메조포어 **2–10 nm** (`[도표]` ≈3.8 nm) | **3.62 µm** | large (낮음) |

★★ `[해석]` **Mes-S = Ketjen Black 이고, 이 논문의 네 호스트 중 가장 나쁘다.**
이 위키의 다른 두 digest 가 **바로 그 KB 를 쓴다** — `raw/papers/huang2026_…`(S/KB/LPSCl
대조군 S 이용률 **39 %**)와 `raw/papers/wang2023_…`(S/KB/LPB). 두 논문의 **낮은 기준선이
"탄소만으로는 부족하다" 가 아니라 "하필 가장 나쁜 호스트를 썼다" 일 수 있다**는 가능성이
이 논문에서 처음 열린다. 이것은 [[reference-cell-500-600-mahg]] H2a 의 해석을 바꾼다 (§11·§15).

`[인쇄]` 황 함침량: "Based on the measured pore volumes and corresponding calculation
(Figure S3), **70 wt % sulfur** was infiltrated into all S/C composites, representing the
**maximum loading that can be accommodated within the available pore volume of all four
carbon hosts**." 완전 함침 확인은 **XRD · BET (Figure S4) · TEM-EDS (Figure S5)** — 전부 SI.
`[도표, Fig. 3E]` TGA 가 네 시료 모두 **≈70 % 질량 손실**(100 → ≈31 %)을 보여 70 wt% 와 정합.

### 4.3 ★★ 측정된 유효 전도도 (Fig. 1E) — 이 digest 가 §11 에서 쓰는 수치

최종 전극 조성 **S : C : SSE = 49 : 21 : 30 wt%** (황 49 wt%) 에서 **DC 분극** 측정:

| 군 | **σ_eff,elec (S cm⁻¹)** | **σ_eff,ion (S cm⁻¹)** |
|---|---|---|
| **small** (Mic-S, Mes-S) | `[인쇄]` **0.104 – 0.108** | `[인쇄]` **≤ 1.37 × 10⁻⁵** |
| **large** (Mic-L, Mes-L) | `[인쇄]` **0.015 – 0.019** | `[인쇄]` **최대 4.34 × 10⁻⁵** |
| 비 | `[재현]` small / large ≈ **6.2배** | `[재현]` large / small ≈ **3.2배** |

`[도표, Fig. 1E]` 막대 그래프 — 실선 막대 = 이온(좌축 0–5×10⁻⁵), 빗금 막대 = 전자(우축
0–1.4×10⁻¹). 판독값: 이온 Mic-S ≈1.40 / Mes-S ≈1.35 / Mic-L ≈4.34 / Mes-L ≈4.20 (×10⁻⁵);
전자 Mic-S ≈0.108 / Mes-S ≈0.113 / Mic-L ≈0.021 / Mes-L ≈0.016 (S cm⁻¹).
→ 인쇄 범위와 대체로 맞는다 (Mes-S 전자는 판독이 인쇄 상한 0.108 보다 약간 높게 읽힌다).

저자의 귀속 `[인쇄]`:
- 전자: "consistent with **improved electronic percolation from finer hosts**"
- 이온: "consistent with **reduced ionic tortuosity and higher effective SSE connectivity when
  the S/C phase occupies a smaller volume fraction**" (ref 34)

`[재현]` **토르투오시티 역산 시도 (참고용, 가정이 많다).** 이 논문 자신의 정의
`τ = σ0/σ_eff · ε` 를 쓰고, σ0 = LPSBI 벌크 5.2×10⁻³ S cm⁻¹, SE 부피분율 ε 를 **질량분율
0.30 으로 대용**하면:
- large: τ = 0.30 × 5.2×10⁻³ / 4.34×10⁻⁵ = **≈36**
- small: τ = 0.30 × 5.2×10⁻³ / 1.37×10⁻⁵ = **≈114**

★ `[해석]` **이 값들은 Cronk 2026 의 τ ≈ 2–3.4 와 한 자리 이상 다르다.** 이유는 셋 —
(i) ε 를 vol% 가 아니라 wt% 로 대용했고 (LPSBI 밀도 미기재, G21), (ii) Cronk 의 τ 는
**SE 상만의 기하학적 모델값**인데 이것은 **계면저항·입자간 접촉까지 포함한 측정값**에서
역산한 것이며, (iii) 성형 압력이 다르다(G22). → **이 위키에 이제 "토르투오시티" 라는 이름의
양이 둘 있고 서로 비교할 수 없다.** 비교는 **각 논문 내부의 비**로만 한다.

### 4.4 율속 — 성능은 **이온 쪽**을 따라간다 (Fig. 1F) `[인쇄 + 도표]`

조건 `[인쇄]`: 49 wt% 황, **4 mg cm⁻²**, **60 °C**, Li 금속, 1.3–3.1 V vs Li/Li⁺.

| C-rate | `[인쇄]` large 군 | `[인쇄]` small 군 |
|---|---|---|
| **0.5C** | **≈95 %** (0.2C 대비) | **≈75 %** |
| **1C** | **92 % → 79 %** (범위) | **84 % → 53 %** |
| **2C** | 최고 **76 %**, 최저 ≈33 % | 최고 **50 %**, 최저 ≈33 % |

`[도표, Fig. 1F]` 개별 판독 (정규화 용량 %): 0.2C 전부 ≈100 → 0.5C **Mic-L ≈96 · Mes-L ≈95 ·
Mic-S ≈95 · Mes-S ≈75** → 1C **Mic-L ≈92 · Mes-L ≈84 · Mic-S ≈84 · Mes-S ≈53** →
2C **Mic-L ≈76 · Mic-S ≈50 · Mes-L ≈33 · Mes-S ≈33** → 0.1C 복귀 **전부 ≈95–97**.

★ **G5 의 근거가 여기다** — 0.5C 에서 "small 군이 75 % 로 떨어진다" 는 것은 **Mes-S 하나**이고
Mic-S 는 large 군과 같다. 2C 에서야 Mic-S(50)와 Mic-L(76)이 갈린다.

`[인쇄]` 저자의 결론: "These results identify **micron-scale host particles as an enabling
factor for thick, high-active-fraction cathodes at low to medium C rates where ionic
percolation is otherwise limiting**. As C rates continue to increase, **other factors begin
to dominate** reaction kinetics."

★★ `[해석]` **이 절이 이 논문의 가장 강한 주장이다** — 전자 전도도가 **6배 높은** 군이
율속에서 **진다**. 즉 이 조성대(탄소 21 wt%)에서는 **전자가 율속의 지배 변수가 아니다.**
우리 [[reference-cell-500-600-mahg]] H2a 와 [[interface-quality-not-bulk-conductivity]] ①에
직접 걸린다 (§11).

---

## 5. p.5 — 결과 ② **기공 크기**가 TPB 밀도를 정한다 (Fig. 2)

### 5.1 기공 분류 `[인쇄]`

"Nitrogen sorption and TEM analyses show that **Mic-S and Mic-L are dominated by micropores
(<2 nm)**, whereas **Mes-S and Mes-L contain predominantly mesopores (2–10 nm)**"
(Figures 2C and S8; **Table S1** — 미확보).

`[도표, Fig. 2C]` HAADF-STEM 4장. Mic-S·Mes-S·Mic-L 은 무질서한 다공 구조, **Mes-L(CMK-3)만
규칙적인 평행 줄무늬** — 주형 기반 정렬 메조포어 구조가 그대로 보인다. 스케일바 10 nm.

### 5.2 계산된 TPB 밀도 (Fig. 2B) `[도표]`

`[인쇄]` "This trend is captured by **computed TPB densities derived from synthetic
three-dimensional (3D) microstructures**" (Figure 2B; computational details).

`[도표, Fig. 2B]` **같은 입자 크기**로 고정한 두 막대, y축 **TPB density (µm⁻²)**:

| | TPB 밀도 `[도표]` |
|---|---|
| **Micropore** | **≈510 µm⁻²** |
| **Mesopore** | **≈285 µm⁻²** |
| 비 | `[재현]` **≈1.8배** |

★ **본문에 이 두 숫자가 인쇄돼 있지 않다 (G1).** 그림에서만 읽을 수 있다.

### 5.3 율속의 두 축 분해 (Fig. 2D·2E) — 이 논문의 핵심 그림 `[인쇄 + 도표]`

`[인쇄]` "although the **specific capacity shows no clear trend with particle size**, the
**capacity fading at high rates remains strongly dependent on particle size** (Fig. 2D).
In contrast, the specific capacity exhibits a **clear dependence on pore architecture**
(Fig. 2E) — **microporous hosts consistently deliver higher sulfur utilization than
mesoporous hosts across all C rates**. This capacity gap becomes even more pronounced at a
high rate, reaching **nearly a 3-fold difference (1,070 mAh gS⁻¹ for Mic-L and 338 mAh gS⁻¹
for Mes-S at 2C)**."

`[도표, Fig. 2D·2E]` 비용량 판독 (단위 **mAh g⁻¹(S)**, `[재현]` 괄호 안은 ×0.698 =
**mAh g⁻¹(Li2S)**):

| C-rate | **Mic-L** (5.89 µm, micro) | **Mic-S** (0.14 µm, micro) | **Mes-L** (3.62 µm, meso) | **Mes-S** (0.15 µm, meso) |
|---|---|---|---|---|
| **0.2C** | ≈**1,410** (984) | ≈**1,375** (960) | ≈**1,300** (907) | ≈**1,000** (698) |
| **0.5C** | ≈**1,385** (967) | ≈**1,310** (914) | ≈**1,250** (873) | ≈**750** (524) |
| **1C** | ≈**1,290** (900) | ≈**1,170** (817) | ≈**1,030** (719) | ≈**535** (373) |
| **2C** | **1,070** `[인쇄]` (747) | ≈**690** (482) | ≈**430** (300) | **338** `[인쇄]` (236) |

`[재현]` 이용률 (÷1,672): Mic-L 0.2C **84.3 %** · 2C **64.0 %**; Mes-S 0.2C **59.8 %** ·
2C **20.2 %**.

★ `[해석]` **Fig. 2E 가 이 논문의 결론을 가장 깔끔하게 보여준다** — x축이 기공 직경일 때
네 점이 **2 nm 경계에서 계단**을 이룬다(마이크로포어 둘이 위, 메조포어 둘이 아래). x축이
입자 크기일 때(Fig. 2D)는 그런 계단이 없고 **0.15 µm 자리에 1,375 와 1,000 이 함께 있다**.
→ **이용률(비용량)의 지배 변수는 기공, 율속 감쇠의 지배 변수는 입자 크기.** 두 축이
실제로 분리된다는 이 논문의 주장은 이 두 그림에서는 설득력이 있다.
단 **각 칸에 재료가 하나씩**이라는 G4 의 한계는 그대로다.

### 5.4 다른 물성은 상관이 약하다는 주장 `[인쇄]` — 근거는 SI

"they also exhibit variations in other intrinsic material properties, as revealed by Raman and
XPS analyses (**Figure S10**). However, correlations between electrochemical performance and
these physicochemical descriptors (**I_D/I_G ratio, O/C ratio, surface area, and total pore
volume**) are **far less pronounced** than those associated with pore size and particle size
(**Figure S11**)."
→ **SI 미확보. 이 digest 는 이 주장의 강도를 평가할 수 없다** (G4).

---

## 6. p.5–6 — 결과 ③ ★ **볼밀이 황을 옮긴다** (Fig. 3)

이 절이 이 논문의 가장 독창적인 부분이고, 우리 [[composite-cathode-mixing-routes]] 에 직접
걸린다.

### 6.1 방법 — SSE 를 물로 씻어내고 S/C 만 본다 `[인쇄]`

"we **removed the SSE from as-milled composites by water washing** and examined the remaining
S/C structure." (탈이온수 24 h → 원심 2,000 rpm 10 min → 상온 진공건조)

### 6.2 밀링 후 입도 (Fig. 3A·3C) `[인쇄 + 도표]`

| 시료 | 원래 D50 | **밀링+수세 후 D50** | 배수 |
|---|---|---|---|
| **Mic-S** | **0.14 µm** | **10.7 µm** `[인쇄]` | **≈80배** `[인쇄]` |
| **Mes-S** | **0.15 µm** | **22.3 µm** `[인쇄]` | **≈150배** `[인쇄]` |
| **Mic-L** | 5.89 µm | `[도표, Fig. 3C]` **≈7.5 µm** | ≈1.3배 |
| **Mes-L** | 3.62 µm | `[도표, Fig. 3C]` **≈7.2 µm** | ≈2.0배 |

`[인쇄]` "large S/C composites such as Mic-L and Mes-L **maintained their individual particle
sizes without notable agglomeration**." → **G6** (Mes-L 의 2배는 "notable" 하지 않다고 하기 어렵다).

### 6.3 황이 응집의 원인이다 — 황 없는 대조군 `[인쇄 + 도표]`

황을 뺀 **C/SSE = 21 : 30** 복합체를 **동일 밀링 조건**으로 만들어 비교 (Figures S12B, S12C):

| 시료 | 황 있음 D50 | **황 없음 D50** |
|---|---|---|
| **Mes-S** | **22.3 µm** | **3.7 µm** `[인쇄]` |
| **Mic-S** | **10.7 µm** | **4.5 µm** `[인쇄]` |
| Mic-L | `[도표]` ≈7.5 µm | `[도표, Fig. 3C]` ≈7.1 µm |
| Mes-L | `[도표]` ≈7.2 µm | `[도표, Fig. 3C]` ≈5.4 µm |

`[인쇄]` "In the absence of sulfur, **agglomeration was substantially reduced for all hosts**…
indicating that **sulfur participates in the aggregation process**."

★★ `[해석]` **이것이 이 논문에서 가장 깨끗한 대조 실험이다** — 같은 밀링, 같은 탄소,
같은 SE, 황만 뺐다. Mes-S 가 22.3 → 3.7 µm 로 **6배 줄어든다.** 응집의 원인이 황이라는 것은
이 한 쌍으로 설득력 있게 보인다. `[해석]` 반대로 **Mic-L 은 황 유무에 거의 무감**(7.5 ↔ 7.1)
이라는 것이 "Mic-L 이 황을 놓치지 않는다" 의 가장 직접적인 증거다.

### 6.4 황이 어디로 갔나 — STEM-EDS (Fig. 3B) `[인쇄 + 도표]`

`[도표, Fig. 3B]` S(노랑)·C(청록) 중첩 맵:
- **Mic-S**: 대부분 **청록(C) 우세**, 황은 아래쪽에 부분적. 겹침 불완전.
- **Mes-S**: **노랑 덩어리와 청록 영역이 뚜렷이 분리**. 황 과잉 도메인이 눈에 보인다.
- **Mic-L**: 입자들이 **고르게 노랑**(S 신호가 입자 전체에 균일) — 분리된 황 덩어리 없음.
- **Mes-L**: 노랑과 청록이 섞이되 **중앙에 밝은 황 덩어리** 하나가 보인다.

`[인쇄]` "the sulfur and carbon signals in **Mic-S and Mes-S exhibit incomplete spatial
overlap**… sulfur **partially redistributes from the carbon framework and forms sulfur-rich
domains during milling**. In **Mes-L**, sulfur relocation is **less pronounced but sulfur-rich
domains or discrete sulfur particles remain visible**. In contrast, **Mic-L largely preserves
its secondary-particle morphology and displays a relatively uniform sulfur distribution**."

### 6.5 XRD — 결정질 황의 재석출 (Fig. 3D) `[인쇄 + 도표]`

`[인쇄]` "although **as-prepared S/C composites show no crystalline sulfur** (Figure S4B),
**crystalline sulfur peaks appear after milling for all samples except Mic-L**."

`[도표, Fig. 3D]` 네 패턴 + 참조 S(78-1889). **Mes-L·Mes-S·Mic-S** 는 23° 부근과 25–30°에
**뾰족한 황 회절선**; **Mic-L(주황)은 넓은 비정질 혹만** 보이고 뾰족한 선이 없다.

★★ `[해석]` **"as-prepared 에는 결정질 황이 없다 → 밀링 후에 생긴다" 가 이 논문의 결정적
한 줄이다.** 멜트 함침으로 기공에 들어간 황은 비정질/구속 상태인데, **밀링이 그것을 꺼내
결정으로 다시 굳힌다.** 그 결정 황이 입자를 잇는 다리가 되고 C/SSE 접촉을 덮는다.

### 6.6 TGA — 황 손실 저항 (Fig. 3E) `[인쇄 + 도표]`

`[인쇄]` "Together with TGA (Figure 3E), these data support a processing mechanism in which
**local heating and mechanical agitation mobilize infiltrated sulfur**; the mobilized sulfur
**migrates and redeposits as a crystalline, bridge-forming phase that promotes S/C
agglomeration and can passivate carbon/SSE contact**." / "**Mic-L exhibits high resistance to
sulfur loss**" (캡션).

`[도표, Fig. 3E]` 네 곡선 모두 100 % → **≈31 %** (총 **70 %** 손실, 화살표로 표기). 손실 개시는
모두 **≈200 °C**, 종료는 **Mes-L(노랑)이 가장 빠르고(≈400 °C) Mic-L(주황)이 가장 늦다(≈470 °C)**.
Mic-S·Mes-S 는 중간(≈420–440 °C).

### 6.7 모세관압 — 저자의 기전 `[인쇄]`

"The calculated **capillary pressures based on the Young-Laplace equation** are summarized in
**Figure S15**. The **microporous hosts exert a higher capillary pressure (151–198 MPa)** on
liquid sulfur than **mesoporous hosts (59–64 MPa)**, corresponding to a **2.5- to 3.4-times
stronger confinement effect** (refs 37, 38). This stronger capillary pressure, **coupled with
increased diffusion paths**, renders microporous large-particle (**Mic-L**) hosts the **most
resistant to sulfur redistribution**."

★ `[해석]` 기전이 **두 항의 곱**이다 — (i) 모세관압(기공이 작을수록 큼) × (ii) 확산거리
(입자가 클수록 멂). **Mic-L 만이 두 항 모두에서 유리하다.** 이것이 2×2 설계에서 Mic-L 이
유일한 승자인 이유에 대한 논문의 답이다. 다만 Figure S15 가 미확보라 **151–198 MPa 가 어느
기공 반경에서 나온 값인지 모른다** (Young–Laplace `ΔP = 2γcosθ/r` 에 쓰인 γ·θ 미공개).

### 6.8 선행 연구 불일치의 해소 주장 `[인쇄]`

"This processing perspective **resolves a key inconsistency in prior reports on pore-size
effects in ASSLSBs**. Apparent 'intrinsic' advantages of certain pore structures can be
**masked or even reversed if sulfur redistribution during milling modifies TPB density and
transport connectivity** in the final composite."

★★★ `[해석]` **이 한 문단이 이 논문이 이 위키에 주는 가장 일반적인 교훈이다.**
"재료의 고유 성질" 로 보고된 것의 상당수가 **공정 후에 살아남지 못한다.** 같은 명제를
Cronk 2026 은 **반대 방향**으로 쓴다 — 밀링이 만드는 계면상이 **이득**이라고. 두 논문은
"밀링이 활물질 표면에 하는 일" 에 대해 정반대를 본다 (§13, §16-5).

---

## 7. p.6–7 — 결과 ④ 사이클 중 TPB 보존 (Fig. 4)

### 7.1 설계 `[인쇄]`

"long-term cycling in sulfur cathodes is challenged by the **∼80% volume change from S to
Li2S** (ref 39)… Given the superior rate capability of microporous S/C composites, we selected
**Mic-S and Mic-L** to explore the impact of **particle size** on electrode stability.
**To isolate cathode evolution from Li-metal anode effects**, we compared Mic-S and Mic-L in
all-solid-state cells using **Li-In anode**."

`[해석]` 좋은 설계다 — 기공을 마이크로포어로 **고정**하고 입자 크기만 비교한다. §4 의
교락(G4)이 이 비교에서는 하나 줄었다.

### 7.2 1,500 사이클 (Fig. 4A) `[인쇄 + 도표]`

조건 `[도표, Fig. 4A 그림 안]`: **0.7 – 2.5 V vs Li-In/Li⁺**, **1.5 mg_S cm⁻²**,
**Li0.5In 음극 (60 µm)**, **1.25 mA cm⁻² (0.5C)**, **RT (22 °C)**, **50 MPa**.

| | 첫 용량 `[인쇄]` | `[재현]` ×0.698 | 결과 |
|---|---|---|---|
| **Mic-S** | **1,103 mAh g⁻¹(S)** | **770 mAh g⁻¹(Li2S)** | `[인쇄]` **425 사이클에 50 % 유지** |
| **Mic-L** | **1,164 mAh g⁻¹(S)** | **812 mAh g⁻¹(Li2S)** | `[인쇄]` "**>1,500 cycles with negligible degradation**" |

`[재현]` 면적용량 = 1,164 × 0.0015 = **1.75 mAh cm⁻²** (Mic-L 첫 사이클).
`[재현]` 이용률 = 1,164 / 1,672 = **69.6 %**. (60 °C 율속의 84 % 보다 낮다 — 상온이기 때문.)

`[도표, Fig. 4A]` **궤적이 단조가 아니다 (G13)**: Mic-L 은 ≈1,180 에서 시작해 ≈100–250 사이클에
**≈1,130 으로 내려갔다가** ≈600–750 사이클에 **≈1,280 까지 올라가고** 그 뒤 서서히 내려와
1,500 사이클에 **≈1,150**. CE 는 양쪽 모두 **≈100 %** 로 산포가 있다. Mic-S 는 ≈1,100 에서
**직선적으로** 내려가 425 사이클에 ≈550.

★ `[해석]` **"negligible degradation" 은 양 끝점의 비교다.** 중간에 ±10 % 의 왕복이 있다.
그리고 **이 데이터는 1.5 mg cm⁻² = 1.75 mAh cm⁻²** 의 저로딩 셀이다 (G23).

### 7.3 operando 압력 (Fig. 4B) `[인쇄 + 도표]`

`[인쇄]` "operando pressure measurement was conducted during cell cycling using a
**constant-gap mode**… The **normalized pressure-capacity profile (Δ(ΔP)_Q)** was used to
**decouple the effects of absolute capacity between cells**. Compared with the Mic-L cathode,
**Mic-S showed a higher Δ(ΔP)_Q value, indicating a greater volume change** during cycling."

`[도표, Fig. 4B]` y축 **Δ(ΔP)_Q (MPa mAh⁻¹)**, x축 사이클 1–10 (1–5 = **0.1C**, 6–10 = **0.2C**):
- **Mic-S**: 9.8 → 8.4 (5사이클) → 9.1 (10사이클)
- **Mic-L**: 8.4 → 6.8 (5사이클) → 7.3 (10사이클)
→ Mic-S 가 항상 **≈1.4–1.8 MPa mAh⁻¹ 높다** (약 **20–25 %**).

`[인쇄]` "During the **first five cycles, a gradual increase in capacity coupled with reduced
pressure** aligns with a **typical electrode densification process**."

★ `[해석]` 이 지표는 **Qu 2025 와 같은 계열의 측정**이지만 **정규화 방식이 새롭다** —
용량으로 나눠서 셀 간 용량 차이를 제거했다. 우리가 같은 측정을 할 때 쓸 수 있는 형식이다.
단 **Δ(ΔP)_Q 의 정의식이 본문에 없다** (ΔP 가 사이클 내 최대–최소인지, Δ(ΔP) 가 방전–충전
차인지 불명).

### 7.4 단면 두께·균열 (Figure S17 — 미확보, 수치만 본문에) `[인쇄]`

| 지표 | **Mic-S** | **Mic-L** |
|---|---|---|
| 첫 방전 후 양극 두께 증가 | **46.6 %** | **36.8 %** |
| 사이클 후 **비가역** 두께 증가 | **11.8 %** (귀속 모호 — G18) | 미기재 |
| 균열/공극 | `[인쇄]` "more extensive crack/void formation in Mic-S, whereas **Mic-L largely retains a dense and compact morphology**" (수치 없음) | — |

`[재현]` 참고 — S → Li2S 부피 팽창 **≈80 %**(본문 인용). 황이 전극의 49 wt% 이므로 전극 전체의
팽창은 그보다 작아야 한다. 46.6 % 와 36.8 % 는 **둘 다 그 범위 안**이고, 둘의 차 **9.8 %p** 가
이 절 주장의 전부다.

### 7.5 EIS (Fig. 4C) `[인쇄 + 도표]`

`[인쇄]` "the **high-frequency semicircle (charge-transfer/interfacial contribution) grows more
strongly for Mic-S**, indicating faster contact loss and increasing interfacial resistance."

`[도표, Fig. 4C]` 두 패널 (위 = **After 300 cycles**, 아래 = **Before cycle**), Z′ 0–2,000 Ω:
- **사이클 전**: 둘 다 반원 없이 직선(확산 꼬리). 인셋(0–40 Ω)에서 **고주파 절편 Mic-L ≈15 Ω,
  Mic-S ≈28 Ω**.
- **300 사이클 후**: **Mic-S 가 Z′ ≈500 → 1,750 Ω 까지 뻗는 큰 저주파 꼬리**를 만든다.
  **Mic-L 은 Z′ ≈650 Ω 에서 끝난다.** → Mic-S 의 총 임피던스가 **≈2.7배**.

★ `[해석]` 그림에서 명확히 커지는 것은 **저주파 쪽**인데 본문은 **"high-frequency semicircle"**
이 커진다고 쓴다. `[해석]` 반원 피팅 결과가 없어(SI 도 해당 그림 없음) **어느 성분이 커졌는지
독자가 확인할 수 없다**. 또 **사이클 전부터 Mic-S 의 고주파 절편이 2배 높다**(28 vs 15 Ω)는
것은 본문이 언급하지 않는다 — 출발점이 이미 다르다.

### 7.6 고로딩 (Fig. 4D) `[인쇄 + 도표]`

조건 `[도표, 그림 안]`: **0.7–2.5 V vs Li-In/Li⁺**, **Li0.5In**, **60 °C**, **50 MPa**.

`[인쇄]` "At 60 °C, the Mic-L cathodes deliver high specific capacity at **∼1,550 mAh g⁻¹**
across loadings from **2 to 6 mg cm⁻²**… With a sulfur loading of **6 mg cm⁻²**, the Mic-L
cathode reaches an **areal capacity of 9 mAh cm⁻² at 0.2C** and **retains 7.7 mAh cm⁻² over
500 cycles**. Even at **1C (3.34 mA cm⁻²)**, stable cycling extends to **1,000 cycles without
measurable decay**."

| 로딩 | 전류 | `[도표]` 첫 면적용량 | `[도표]` 끝 | 사이클 |
|---|---|---|---|---|
| **6 mg cm⁻²** | **2 mA cm⁻² (0.2C)** | **≈9.0 mAh cm⁻²** | **≈7.1–7.2** (G12) | **500** |
| **4 mg cm⁻²** | **3.34 mA cm⁻² (0.5C)** | **≈6.2** | **≈5.4** | **≈400** |
| **2 mg cm⁻²** | **3.34 mA cm⁻² (1C)** | **≈3.0** | **≈2.8** | **1,000** |

`[재현]` 비용량 환산: 9.0 / 0.006 = **1,500 mAh g⁻¹(S)** = **1,047 mAh g⁻¹(Li2S)** =
**735 mAh g⁻¹(composite)**; 6.2 / 0.004 = **1,550 mAh g⁻¹(S)** = **1,082 (Li2S)**;
3.0 / 0.002 = **1,500 mAh g⁻¹(S)**. → 본문의 "∼1,550 across loadings" 와 정합.
`[재현]` 이용률 1,500 / 1,672 = **89.7 %**, 1,550 / 1,672 = **92.7 %**.
`[도표]` CE 는 세 곡선 모두 **≈100 %** 로 평평하다.

---

## 8. p.8–9 — 결과 ⑤ Li 금속 full cell 과 셀 수준 에너지 (Fig. 5)

### 8.1 저자가 내세우는 평가 기준 `[인쇄]` ★

"Because **increasing SSE and carbon fractions can inflate apparent sulfur utilization while
reducing cell-level energy**, we emphasize **electrode-level capacity (mAh g_electrode⁻¹)**
and areal capacity at a high sulfur fraction." / "previous research has reported high areal
capacity cathodes above 4 mAh cm⁻² (**Table S2**), it is important to note that **these
electrodes typically have a low sulfur fraction in the entire electrode**. Therefore,
**electrode-based specific capacity … should be used for performance assessment and
comparison**."

★★★ `[해석]` **이 문단은 이 위키의 [[capacity-normalization-li2s-vs-sulfur]] 와 정확히 같은
문제의식이고, 이 논문이 그 문제에 대해 가장 명시적인 논문이다.** 그리고 그 비판의 칼끝이
**우리 조성을 향한다** — 우리 30:50:20 은 활물질 30 wt%, SE 50 wt% 로 이 논문이 말하는
"SSE 분율을 올려 겉보기 이용률을 부풀린" 전형이다. `[재현]` 우리 셀에서 목표 500–600
mAh g⁻¹(Li2S) 를 달성해도 전극 기준으로는 **150–180 mAh g⁻¹(composite)** 이고, 이 논문의
**752.4** 와 **4–5배** 차이다. 분모를 바꾸면 "좋은 셀" 의 순위가 뒤집힌다.

### 8.2 full cell 결과 (Fig. 5A·5B) `[인쇄 + 도표]`

조건 `[인쇄 + 도표, Fig. 5A 그림 안]`: **Mic-L (S/C/SSE = 49/21/30)**, **S 로딩 4 mg cm⁻²**,
**SSE = Li7P2S8Br0.5I0.5**, **Li 금속 음극**, **0.2C = 1.34 mA cm⁻²**, **60 °C**, **50 MPa**,
**1.3–3.1 V vs Li/Li⁺**.

| 지표 | 값 | `[재현]` 다른 분모 |
|---|---|---|
| 첫 비용량 | `[인쇄]` **1,535.6 mAh g⁻¹(S)** | **1,071.8 mAh g⁻¹(Li2S)** (×0.698) |
| 전극 기준 | `[인쇄]` **752.4 mAh g⁻¹(electrode)** | = **mAh g⁻¹(composite)**; 검산 1,535.6 × 0.49 = **752.4** ✓ |
| 면적용량 | `[인쇄]` "**exceeding 6 mAh cm⁻²**" | 1,535.6 × 0.004 = **6.14 mAh cm⁻²** |
| 이용률 | — | 1,535.6 / 1,672 = **91.8 %** |
| 250 사이클 유지 | `[인쇄]` **94.24 %**, 감쇠율 **0.023 %/사이클** | 끝 용량 `[재현]` 1,535.6 × 0.9424 = **1,447 mAh g⁻¹(S)** = **1,010 (Li2S)** = **709 (composite)** = `[도표]` **≈5.8 mAh cm⁻²** |

`[도표, Fig. 5A]` **궤적이 V 자다 (G13)**: ≈1,570 → (≈40–80 사이클) **≈1,300 (≈85 %)** →
(250 사이클) ≈1,450. 우축이 둘 — 면적용량 2–7 mAh cm⁻², 전극용량 300–900 mAh g_electrode⁻¹.

`[도표, Fig. 5B]` 전압 곡선 (50·100·200·250 사이클 중첩, **0.2C, 1.34 mA cm⁻², CCCV, 60 °C**):
- 낮은 분지 **≈2.05 V vs Li/Li⁺** 에서 평탄, 끝에서 **1.3 V 로 급락** (≈5.4–5.9 mAh cm⁻²).
- 높은 분지 **≈2.3–2.45 V**, **3.1 V 에 수평 구간**이 **≈0.8 mAh cm⁻²** 길이로 보인다
  (`[해석]` CCCV 의 CV 유지 구간으로 읽힌다 — 총 면적용량의 **≈13 %**).
- 이력(hysteresis) **≈0.3 V**.
- `[인쇄]` "demonstrated **minimal polarization increase**" — `[도표]` 네 곡선이 거의 겹친다.

★ `[해석]` **CV 구간이 13 % 라는 것은 CC 만으로는 3.1 V 에서 충전이 끝나지 않는다는 뜻**이고,
3.1 V vs Li/Li⁺ 에 **머무는 시간이 길다**는 뜻이다. I 함유 SE 의 산화 창을 생각하면 무시할
조건이 아니다 (G8). 다만 `[재현]` I⁻ 산화의 용량 상한은 작다 (§16-3).

### 8.3 Li 금속 안정성에 대한 자기 단서 `[인쇄]`

"We note that **iodide-containing sulfide electrolytes have been reported to form LiI-rich
interphases that can stabilize Li/SSE contact**; such interphase chemistry **may also
contribute to the stable Li-metal cycling**." (refs 40, 41)

★ `[해석]` 저자 스스로 **"이 250 사이클의 일부는 양극 설계가 아니라 SE 조성(요오드) 덕일 수
있다"** 고 적었다. 즉 **이 full cell 결과를 "two-length-scale 설계의 증명" 으로 읽으면 안
된다** — 양극 설계와 SE 화학이 분리되지 않았다. Mic-S 로 같은 full cell 을 돌린 대조군이 없다.

### 8.4 셀 수준 에너지 추정 (Fig. 5C) `[인쇄 + 도표]`

`[인쇄]` 전제: "**5-Ah ASSLSB design including current collectors, tabs, and packaging but
excluding external stack hardware (Table S3)**", 입력 지표 "**4 mg cm⁻², ∼50 wt % sulfur,
1,500 mAh gS⁻¹**", 측정 **양극 밀도 1.79 g cm⁻³**.

| 주장 `[인쇄]` | 값 |
|---|---|
| **>350 Wh kg⁻¹** 달성 조건 | SSE 분리막 두께 **≤90 µm** |
| **>500 Wh kg⁻¹** 달성 조건 | SSE 분리막 두께 **<∼40 µm** |

`[도표, Fig. 5C]` 좌축 E_g (Wh kg⁻¹, 검은 ●), 우축 E_v (Wh L⁻¹, 주황 △), x축 SSE 두께 10–100 µm:
E_g 는 **10 µm ≈620 → 50 µm ≈455 → 100 µm ≈338**; E_v 는 **10 µm ≈1,090 → 100 µm ≈590**.
점선 두 개: **Li-ion (Si 음극) ≈345 Wh kg⁻¹**, **Li-ion (흑연 음극) ≈275 Wh kg⁻¹**.

★ `[해석]` **이 그래프의 메시지는 "양극이 아니라 분리막이 남은 병목" 이다** — 저자도
`[인쇄]` "highlighting **separator engineering as a remaining practical lever**" 라고 쓴다.
그런데 **서론에서 <30 µm 분리막이 Li creeping 으로 단락을 부른다고 인용**했다(§2.3).
40 µm 는 그 경계 바로 위다. 그리고 **50 MPa 가압 하드웨어가 분모에서 제외**돼 있다 (G19).

### 8.5 문헌 비교 (Fig. 5D, Table S2 — 미확보) `[인쇄 + 도표]`

`[도표, Fig. 5D]` x = 사이클 수(축이 500 에서 끊김), y = **전극용량 (mAh g_electrode⁻¹)**,
**원 크기 = 면적용량 (2/4/7/9 범례)**, **빨강 = 60 °C · 파랑 = <30 °C · ★ = Li 금속 음극**.
**This work** 는 **≈730–755 mAh g_electrode⁻¹** 대역에 **250·300·400·1,000 사이클** 네 점이
놓이고, 문헌은 대부분 **<650**, 다수가 **<450** 이다. 좌하단에 **16.3 mAh cm⁻² [13]** 큰 원
(전극용량 ≈250, 사이클 ≈40).

`[인쇄]` "most have **low electrode-based specific capacities below 650 mAh g_electrode⁻¹**…
sustained full-cell cycling of high areal capacity cathodes **beyond 200 cycles is rare,
especially when utilizing metallic Li anodes**."

★ `[해석]` 비교축을 저자가 고른 것이고(전극 기준 용량), 그 축에서 이 논문이 이긴다.
`[해석]` **면적용량 단독으로는 이 논문이 1등이 아니다** — Fig. 5D 에 16.3 mAh cm⁻² 점이 있다.
Table S2 미확보라 개별 비교는 불가.

---

## 9. p.9–10 — Scheme 1 (통합 설계 원리)

`[도표, fig_sch1.png]` **3열(Particle → Processing → Electrode) × 2행(Mic-L / Mes-S)** 도식.

| | **Mic-L (위, 파랑)** | **Mes-S (아래, 빨강)** |
|---|---|---|
| **Particle** | 큰 구에 미세 기공, 황(노랑)이 **작은 점으로 고르게** — "**Strong sulfur confinement**" | 작은 구에 큰 기공, 황이 **몇 개 큰 덩어리** — "**Weak sulfur confinement**" |
| **Processing** | 입자들이 SSE(회색 다면체)와 섞여도 **황이 안에 남음** — "**Minimal sulfur relocation**" | 황이 **입자 밖으로 나와 다리를 만들고 응집** — "**Sulfur relocation & loss of dispersion**" |
| **Electrode** | **초록 선이 SSE 입자들을 가로질러 연결** — "**Robust percolation network**" | **빨간 ✕ 표가 곳곳에 찍힘** — "**Blocked pathway**" |

`[인쇄, Scheme 1 캡션]` "microporous **micron-scale** hosts maintain **low-tortuosity ionic
pathways and stable ionic/electronic percolation**, thereby enabling high sulfur utilization,
structural stability, and practical full-cell performance."

★ `[해석]` **Scheme 1 의 초록 선은 이온 경로다** (SSE 입자를 잇는다). 즉 저자의 머릿속에서
최종 승부처는 **이온 퍼콜레이션**이고, 황 재배치가 그것을 막는 방식은 **"SSE 표면을 황으로
덮어 SSE–SSE 접촉을 끊는 것"** 이다. 이것이 §4.4(전자 6배 높은 군이 진다)와 일관된다.

---

## 10. p.11–12 — 계산 방법 (TPB·토르투오시티) ★ 전문

`[인쇄]`:

1. **합성 3D 미세구조 생성**: "random particle generation algorithm (ref 42) in the
   **PoreSpy package** (ref 43)". S/C 복합입자 + SSE 입자의 패킹을 **Fig. 1D·S2 의 탄소
   입도분포에 따라** 생성.
2. **멀티스케일 분리** (★ 이 논문의 계산상 핵심 트릭): "Because the pore size in carbon
   particles is mostly **below 10 nm (Figure S9)**, it is **impossible to generate the cathode
   structure that can capture the micron-scale particles and nanoscale pores in a single
   geometry**. Therefore, the **multi-scale packing method** was used for estimating the TPB."
   - **마이크론 스케일 패킹** → S/C 복합입자와 SSE 입자 사이의 **계면적**, 단위 **면적/부피**
     → "**SSE-carbon interface**"
   - **나노 스케일 패킹** (기공분포 Figure S2 기반) → 복합체 표면의 **황–탄소 계면 모서리**,
     단위 **길이/면적** → "**carbon-sulfur edge**"
   - **"The overall TPB density is the multiplication of the SSE-carbon interface and
     carbon-sulfur edge."**
     `[재현]` 단위 검산: (µm²/µm³) × (µm/µm²) = µm⁻¹ × µm⁻¹ = **µm⁻²** ✓ (Fig. 2B 의 축과 일치)
3. **수송 계산**: "**Fickian Diffusion algorithm (ref 44) in OpenPNM (ref 45) and PoreSpy**".
   한쪽 면에 **1 mV/µm 에 해당하는 전위**, 반대면 0 V.
4. **유효 전도도**: **σ_eff = I / (A ∂V)**, I = 모사 총 전류, A = 단면적, ∂V = 1 mV/µm.
5. **토르투오시티**: **τ = (σ0 / σ_eff) · ε**, σ0 = 벌크 전도도, ε = 공극률(해당 상의 분율).

★★ `[해석]` **TPB 밀도가 두 독립 계산의 "곱" 이라는 점이 중요하다.** 즉 이 논문의 TPB 밀도는
**실측이 아니고, 하나의 3D 구조에서 삼상선을 센 것도 아니다.** 두 스케일에서 따로 계산한 양을
곱한 **구성값**이다. 그러므로:
- **단위는 맞지만 물리적 삼상선 길이밀도와 같은 양이라는 보장이 없다.** 곱이 성립하려면
  "SSE–탄소 계면 위의 모든 지점에서 탄소–황 모서리 밀도가 동일" 이라는 가정이 필요한데,
  그 가정은 적혀 있지 않다.
- **기공이 황으로 꽉 찼을 때의 모서리**인지 빈 기공의 모서리인지 불명.
- 그래서 **Fig. 2B 의 1.8배는 "마이크로포어가 메조포어보다 황–탄소 모서리가 1.8배 많다" 는
  기하 진술**로 읽는 것이 안전하다.

`[인쇄]` "This paper does **not** report original code." → **재현 불가.**

---

## 11. ★★★ 이 위키의 논지 [[interface-quality-not-bulk-conductivity]] 에 대한 판정

이 절이 이 digest 를 쓴 가장 큰 이유다. 논지는 다음과 같았다:

> **"황화물 전고체 복합양극에서 활물질 이용률을 올리는 것은 전자 네트워크의 벌크 전도도도,
> 이온 네트워크의 부피분율도 아니다 — 활물질과 황화물 전해질이 맞닿는 계면의 '질' 이다."**

### 11.1 판정 요약

| 논지의 항 | 이 논문의 판정 | 근거 |
|---|---|---|
| ① **σ_e 가 클수록 좋다는 명제는 틀렸다** | **강하게 지지 — 세 번째 독립 사례** | 같은 조성·같은 탄소 함량(21 wt%)에서 σ_eff,elec 이 **6배 낮은** 군이 율속에서 **이긴다** (0.015–0.019 vs 0.104–0.108 S cm⁻¹; 2C 76 % vs 50 %) |
| ② **이온 네트워크의 "양"(부피분율)도 병목이 아니다** | **부분적 반증 — 양이 아니라 "연결성" 이 문제라고 말한다** | 이 논문은 SE 를 **30 wt% 밖에** 쓰지 않고(우리 50 wt%) **σ_eff,ion 이 3.2배 차이** 나는 것을 **토르투오시티·연결성** 탓으로 돌린다. 즉 "SE 의 양" 이 아니라 **"SE 상이 얼마나 이어져 있는가"** 가 변수다 |
| ③ **계면을 직접 건드린 사례가 싸게 이긴다** | **지지하되 "계면" 의 뜻이 다르다** | 이 논문의 처방도 **첨가제·촉매가 0** 이고 **호스트와 공정만 바꿨다**. 그러나 기전은 계면의 **화학적 질**이 아니라 **기하학적 양(TPB 선밀도)과 그 공정·사이클 중 보존**이다 |
| ④ 실험 순서(공정 변수로 가라) | **강하게 지지** | 이 논문의 세 번째 축이 **공정(볼밀)이 설계를 지운다**는 것이다 |

### 11.2 ★ 결론: **"논지는 살아남지만 이유를 바꿔 읽어야 한다"**

이 논문은 **지지도 반증도 아니고 "맞지만 이유가 다르다"** 에 가깝다. 정확히는:

- **논지의 부정절(전자 벌크 전도도가 아니다)은 세 번째로 독립 확인됐다.** Yu 2024(σ_e 200배 ↓,
  개선), Huang 2026(σ_e 14배 ↑, 개선), **Jeong 2026(σ_e 6배 ↓, 개선)**. 세 논문이 각각
  내린 방향이 ↓ ↑ ↓ 인데 셋 다 이겼다. **"σ_e 가 클수록 좋다" 는 이제 세 번 반증됐다.**
- **그러나 긍정절("계면의 질")은 이 논문에서 다른 이름으로 나타난다.** 이 논문이 지목하는
  지배 변수는 **① TPB 의 기하학적 밀도(µm⁻², 기공 크기가 결정) ② 이온 경로의 연결성
  (입자 크기가 결정) ③ 그 둘이 공정과 사이클을 견디는가** 이다. **화학적 친화·계면상·촉매는
  한 번도 등장하지 않는다.**
- 그러므로 논지를 다음처럼 **좁히거나 쪼개야 한다**:
  > 이용률을 정하는 것은 벌크 전도도가 아니라 **활물질–황화물 계면에서 일어나는 것**이다.
  > 그런데 그 "계면에서 일어나는 것" 에는 **적어도 두 갈래**가 있다 —
  > **(A) 계면의 화학**(Yu 의 CuS, Huang 의 HES, Cronk 의 Li3PS4+n interphase)과
  > **(B) 계면의 기하와 그 보존**(Jeong 의 TPB 밀도·토르투오시티·황 재배치 저항).
  > **이 위키는 아직 (A)와 (B)를 가르는 실험을 갖고 있지 않다.**

`[해석]` 이것은 논지 페이지의 **반론 5(계면파 vs 촉매파)** 를 더 날카롭게 만든다 — 대립 구도가
"계면 vs 촉매" 가 아니라 **"계면의 화학 vs 계면의 기하"** 였다.

### 11.3 ★★ 반론 3(전자 퍼콜레이션 고원)은 닫히는가 — **아니다. 그러나 크게 좁혀진다.**

반론 3 은 이랬다:

> "둘 다 전자 퍼콜레이션 고원 위일 수 있다. … **우리 AB 20 wt% 가 그 고원 위인지 아래인지는
> 측정되지 않았다** — 이 논지의 최대 미검증 전제다."

**이 논문이 주는 것 (전진):**

1. **우리 탄소 함량대의 외부 기준점이 처음 생겼다.** 이 논문의 탄소는 **21 wt%** 로 우리
   **AB 20 wt%** 와 거의 같고, 측정된 σ_eff,elec 은 **1.5×10⁻² ~ 1.1×10⁻¹ S cm⁻¹** 이다.
   참고로 Yu 2024 의 **승자**는 **2.9×10⁻⁴ S cm⁻¹** 였다 — `[재현]` **50–370배 낮다**.
   `[해석]` 즉 **탄소 ≈20 wt% 급 복합양극의 σ_e 는 "고원의 한참 위" 일 개연성이 높다.**
2. **고원의 위쪽 끝에서도 σ_e 를 더 올려봐야 소용없다는 것이 같은 계에서 보였다.** small 군은
   σ_e 가 6배 높은데도 졌다. **전자 전도도를 올리는 처방의 기대값이 이 조성대에서 0 에 가깝다.**
3. **DC 분극 프로토콜이 가장 완전하게 적혀 있다** (§3.4) — 우리가 반론 3 을 직접 닫기 위한
   실험(AB 10/20/30 wt% σ_e·σ_Li 측정)의 **이식 가능한 방법**이 생겼다.

**이 논문이 주지 못하는 것 (반론 3 이 살아 있는 이유):**

1. **탄소 함량을 한 번도 바꾸지 않았다 (G3).** 바뀐 것은 탄소의 *형태*다. 그러므로 **고원의
   아래쪽 가장자리(탄소를 줄이면 언제 무너지는가)는 여전히 미측정**이다. 반론 3 의 문장은
   "탄소가 **더 적은** 양극은 여전히 전자 제한일 수 있다" 였는데, 이 논문은 그 조건을 만들지
   않았다.
2. **σ_e 와 함께 σ_ion·TPB·황 재배치가 동시에 바뀐다.** 입자 크기 하나를 바꾸면 네 가지가
   같이 움직인다. 그래서 "σ_e 가 무관하다" 가 아니라 **"σ_e 의 6배 이득보다 σ_ion 의 3.2배
   이득 + TPB 1.8배 + 황 재배치 회피가 더 컸다"** 가 정확한 독법이다. 논지 페이지의 Gap
   ("σ_Li⁺ 와 계면 화학을 고정한 채 σ_e⁻ 만 바꾼 대조") 은 **이 논문도 하지 않았다.**
3. **활물질이 Li2S 가 아니라 S8 이다.** 절연체 Li2S 의 첫 충전(탈리튬화) 활성화는 전자 공급에
   대한 요구가 다를 수 있다. 이 논문에는 Li2S 가 **SE 합성 전구체로만** 나온다.
4. **온도·로딩이 우리와 다르다.** 전자 전도도 비교의 근거가 된 율속 데이터는 **60 °C**다.

**→ 판정: 반론 3 은 닫히지 않는다. 그러나 "우리 AB 20 wt% 가 고원 *위*" 라는 쪽으로
증거가 뚜렷이 기울었고, 반론 3 을 완전히 닫는 데 필요한 실험이 하나로 줄었다 —
`AB 10 / 20 / 30 wt% 에서 DC 분극 σ_e·σ_Li 측정` (논지 페이지 Gap 의 두 번째 항목).
이 논문은 그 실험의 *프로토콜*과 *기준값*을 동시에 준다.**

### 11.4 논지 페이지에 더해야 할 것 (이 digest 의 제안 — 반영은 사람이 한다)

- **Argument ①의 표에 세 번째 행**: Jeong 2026 (탄소 호스트 입자 크기, S8) — σ_e **6배 ↓**,
  σ_ion **3.2배 ↑**, 2C 이용률 **50 → 76 %**(정규화 유지율) / 2C 비용량 **338 → 1,070
  mAh g⁻¹(S)**. **세 논문 모두에서 같은 방향으로 움직인 것은 σ_Li⁺ 뿐**이라는 ①의 결론이
  더 강해진다 (Yu 1.8배 ↑ · Huang 270배 ↑ · Jeong 3.2배 ↑).
- **Argument ②는 수정이 필요하다.** "이온 네트워크의 *양* 은 병목이 아니다" 는 유지되지만,
  Jeong 은 **같은 양에서 연결성이 3.2배 차이** 날 수 있음을 보였다. 즉 **vol% 회계만으로는
  이온 경로의 충분성을 판정할 수 없다.** 우리 48–52 vol% 가 Wang 2023 기준을 넘는다는 것이
  "이온 경로가 충분하다" 를 뜻하지 않는다 — **토르투오시티는 재지 않았다.**
- **반론 1(전도도 절대값 비교 불가)의 완화**: Jeong 은 DC 분극 시료 정체를 명시했다
  (복합체 50 mg, ion-blocking / electron-blocking, ±50 mV, 1 h). 다만 **두 측정의 성형
  압력이 다르다**(700 vs 200 MPa, G22) 는 새 단서가 붙는다.
- **반론 5 의 재서술**: "계면파 vs 촉매파" → **"계면의 화학 vs 계면의 기하"**.
- **새 반론 후보 (이 digest 가 제안)**: **"개선의 일부가 공정 아티팩트 회피일 뿐일 수 있다."**
  Jeong 의 Mes-S 는 밀링으로 D50 이 **150배** 뭉쳤다. 그렇다면 그 셀의 낮은 이용률은
  "메조포어가 나쁘다" 가 아니라 **"그 시료가 밀링에서 망가졌다"** 이다. 같은 논법이 Yu·Huang·
  Wang 의 **대조군**에도 적용될 수 있다 — **세 논문 모두 대조군의 밀링 후 미세구조를 보지
  않았다.** 개선폭의 분모가 "제대로 만든 대조군" 이 아닐 수 있다.
- **Gap 에 추가**: **우리 복합양극의 밀링 후 수세-SEM 을 아무도(우리 포함) 본 적이 없다.**
  §3.6 의 수세법은 비용이 거의 0 이다.

---

## 12. 같은 PNNL 계보 — `raw/papers/qu2025_…` 와의 접속

교신저자 **Dongping Lu** 는 이 위키의 Qu 2025 (*Nano Energy* 138, 110887, DOI
10.1016/j.nanoen.2025.110887) 공저자다. 두 논문은 **같은 문제의 서로 다른 면**을 잰다.

> ⚠ `[해석]` **주의** — 이 digest 를 쓰는 시점(2026-10-02)에 `raw/papers/qu2025_…` 파일의
> **본문이 다른 논문(Lee 2026, KIST/CEJ)의 내용으로 보인다** (§0 서지사항 표가 Lee 저자진을
> 가리킨다). 그래서 아래 Qu 수치는 그 파일의 **frontmatter `compare:` 블록에서만** 가져왔고
> 본문 대조는 하지 않았다. 그 파일의 무결성은 별도로 확인해야 한다.

| 축 | **Qu 2025** (`compare:` 기준) | **Jeong 2026** (이 논문) |
|---|---|---|
| 무엇을 쟀나 | **수직 변위(LVDT)와 스택 압력** — 성분별 부피 기여 분리 | **TPB 밀도·토르투오시티·유효 전도도**와 그 공정·사이클 보존 |
| 구속 방식 | **정압(스프링+LVDT)** vs **정용적(나사+압력변환기)** 비교 | **정용적(constant-gap) 단일**, 로드셀로 압력 기록 |
| **운전 스택 압력** | **7 MPa** | **50 MPa** |
| 100사이클 유지 | 정압 ≈63 % vs 정용적 ≈50 % `[도표, Qu]` | — (이 논문은 정압 대조군이 없다) |
| 활물질 | **Li2S 또는 S**, 조성 **33.3 : 16.7 : 50.0 wt%** | **S8**, 조성 **49 : 21 : 30 wt%** |
| SE | 상용 **LPSCl** | 자체 합성 **LPSBI (Br·I 함유)** |
| 음극 | Li–In + **LTO zero-strain 대극** | Li–In (N/P 2) · **Li 금속** |

★★ `[해석]` **두 논문이 충돌하는 지점이 둘 있다.**

1. **운전 압력이 7배 다르다.** Qu 는 "ASSLB 장기 사이클에 필요한 운전 스택 압력 ≈7 MPa" 를
   인용값으로 제시했고, Jeong 은 50 MPa 를 쓰면서 `[인쇄]` "necessary to ensure sufficient
   densification … However, practical systems must ultimately operate at significantly lower
   pressures" 라고 적는다. **같은 그룹이 같은 해에 7 MPa 와 50 MPa 를 쓴다.** 우리가 "스택
   압력은 얼마가 맞나" 를 이 위키에서 답하려면 이 두 논문만으로는 안 된다.
2. **구속 방식의 평가가 반대다.** Qu 는 **정용적(constant-gap)이 정압보다 나쁘다**(100사이클
   유지 50 % vs 63 %, Ohmic +50 %)고 보고했다. Jeong 은 **전부 정용적**으로 돌리고 1,500
   사이클·250 사이클 결과를 낸다. `[해석]` 둘을 화해시키는 독법은 **"정용적의 문제는 압력이
   7 MPa 에서 더 떨어질 때 생기고, 50 MPa 에서는 여유가 있어 덜 문제된다"** 이지만, 그것은
   이 위키의 추측이고 어느 논문도 그렇게 말하지 않았다.

`[해석]` **공통점도 하나 있다** — 둘 다 **operando 압력 신호를 양극 미세구조 진단 도구로
쓴다**. Qu 는 성분 분리에, Jeong 은 **용량으로 정규화한 Δ(ΔP)_Q** 로 셀 간 비교에.
우리가 Qu 의 fixture 를 흉내 낸다면 Jeong 의 정규화 방식을 같이 가져오는 것이 좋다.

---

## 13. ★ Cronk 2026 과의 대조 — micron > sub-micron 은 **같은 결론, 다른(그리고 일부 상충하는) 이유**

`raw/papers/cronk2026_…` (UCSD·LG ES) 는 이 위키에서 유일하게 토르투오시티 모델을 쓴 다른
digest 이고, **micron 이 sub-micron 보다 낫다**는 같은 결론을 냈다.

### 13.1 겹치는 것

| | **Cronk 2026** | **Jeong 2026** |
|---|---|---|
| "작은 것이 항상 좋지 않다" | C/2 500사이클 유지 **micron 81 % > sub-micron 61 %** | 0.5C 상온 **Mic-L 1,500 사이클 무감쇠 > Mic-S 425 사이클 50 %** |
| 최적 크기대 | **micron 0.5–5 µm** | **모델 최적창 2.5–7 µm**, 승자 **D50 5.89 µm** |
| 토르투오시티 모델 | 합성 전극 생성 + **TauFactor**, τ(이온, LPSCl 상) **micron ≈2.0 < bulk ≈3.0 < sub-micron ≈3.4** (활물질 30 wt%) | 합성 3D 패킹(PoreSpy/OpenPNM) + Fickian diffusion, **τ 값은 본문에 없음 (G1)** |
| 이유의 1차 축 | **이온 수송(토르투오시티)** | **이온 수송(토르투오시티·연결성)** |
| 무게 대가 | 0 (입도만 바꿈) | 0 (상용 탄소 선택만 바꿈) |

★ `[해석]` **두 논문이 서로 다른 재료·다른 연구실·다른 모델링 도구로 같은 방향을 가리킨다.**
그리고 **크기 창이 겹친다** (Cronk 0.5–5 µm ∩ Jeong 2.5–7 µm = **2.5–5 µm**). 이것은 이 위키가
[[reference-cell-500-600-mahg]] H3 에 쓸 수 있는 **가장 수렴적인 숫자**다.

### 13.2 **어긋나는 것 — 그리고 이것이 더 중요하다**

| 축 | **Cronk 2026** | **Jeong 2026** |
|---|---|---|
| "작은 입자" 의 정체 | **활물질(S / Li2S) 입자** | **탄소 호스트 입자**(황은 그 안에 있다) |
| 혼합 경로 | **one-step** 고에너지(500 rpm 1 h, BPR 1:30) — one-step 이 multi-step 을 **2.5배** 이긴다 | **two-step**(멜트 함침 → 450 rpm 순 4 h, BPR 50:1, 간헐). **one-step 대조군 없음 (G16)** |
| **밀링이 활물질 표면에 하는 일** | **이득** — 황 과잉 thiophosphate **Li3PS4+n interphase** 가 리독스 매개체가 되어 Li2S 활성화 전위를 2.4 V 로 낮춘다 | **손해** — 국소 발열·기계적 교반이 **황을 기공 밖으로 꺼내 결정으로 재석출**시키고 C/SSE 접촉을 passivation 한다 |
| 그 주장의 증거 | Raman 152→149 cm⁻¹, XANES pre-edge, EDS 라인스캔, XRD **비정질화**, TGA | XRD **결정화**(밀링 후 황 피크 출현), 수세-SEM D50, STEM-EDS, TGA, 모세관압 |
| 상대의 관측을 쟀나 | **황 재배치·응집을 보지 않았다** | **계면상 화학을 보지 않았다 (G17)** |

★★★ `[해석]` **두 논문은 같은 공정(황화물 SE 와의 볼밀)에 대해 정반대의 서사를 갖고, 서로의
증거를 측정하지 않았다.** 심지어 XRD 증거가 반대 방향이다 — Cronk 는 one-step 밀링의 증거로
**비정질화**를, Jeong 은 밀링 손상의 증거로 **결정화**를 든다.

둘을 화해시킬 수 있는 독법 세 가지 (`[해석]`, 어느 것도 검증되지 않았다):

1. **활물질의 출발 상태가 다르다.** Cronk 의 황은 **벌크 결정 황**(as-received 또는 사전 밀링)
   이고, Jeong 의 황은 **이미 기공 안에 비정질로 구속된 황**이다. 밀링이 전자에게는
   "표면을 만들어 반응시키는" 일이고 후자에게는 "구속을 푸는" 일일 수 있다.
2. **밀링 강도·열이 다르다.** Jeong 은 **5 min 밀링 / 10 min 휴지**로 쪼갠다 — 황의 녹는점이
   115 °C 임을 의식한 설계로 보인다. Cronk 는 **1 h 연속**이다. 즉 **Cronk 조건에서는 황이
   더 많이 녹았을 것**이고, 그렇다면 Cronk 가 본 "계면상" 과 Jeong 이 본 "재석출 결정 황" 은
   **같은 사건의 두 결과**일 수 있다.
3. **둘 다 맞고 최적점이 있다.** [[one-step-vs-two-step-mixing]] **H4(밀링 에너지 총량의
   최적점)** 가 바로 이 가설이다. **이 논문은 H4 의 두 번째 근거다** — 다만 Jeong 은 밀링
   시간을 변수로 두지 않았으므로(그의 변수는 재료) 직접 근거는 아니다.

### 13.3 [[one-step-vs-two-step-mixing]] 에 대한 이 논문의 기여

- **H3(one-step 우세)의 반례는 아니다** — Jeong 은 one-step 대조군이 없다 (G16).
- **H1/H2(two-step 우세)의 지지도 아니다** — Jeong 의 two-step 앞 단계는 "탄소 골격을 먼저
  만드는 것" 이 아니라 **멜트 함침(황을 기공에 넣는 것)** 이다. 우리 카드가 정의한 two-step
  (탄소가 Li2S 를 먼저 감싼다)과 **다른 공정**이다.
- **새로 더해지는 것**: **"혼합 순서" 라는 축 옆에 "혼합이 활물질을 어디로 옮기는가" 라는 축이
  하나 더 있다.** 그리고 그것을 **수세 + 입도 + XRD** 로 값싸게 볼 수 있다 (§17).

---

## 14. SI 미확보 — 본문이 넘긴 지점 전수 목록

**이 digest 는 아래 항목의 내용에 대해 어떤 추정도 하지 않는다.**

| SI 항목 | 본문이 그것에 맡긴 것 | 왜 아쉬운가 |
|---|---|---|
| **Figure S1A, S1B** | 작은/큰 입자 복합체의 이온·전자 전류분포 시뮬레이션(추가 패널) | Fig. 1B·1C 의 정량 근거 |
| **Figure S1C** | ★ **최적 호스트 입자창 2.5–7 µm** | 이 논문에서 가장 이식성 높은 한 줄의 유일한 근거 (G2) |
| **Figure S2** | 네 탄소의 입도분포 (TPB 계산의 입력) | D50 외 분포 폭을 모른다 |
| **Figure S3** | 기공부피 기반 **70 wt% 황 함침량 계산** | 각 호스트의 기공부피를 모른다 (G24) |
| **Figure S4 / S4B** | 함침 확인 XRD·BET / **as-prepared 에 결정질 황 없음** | §6.5 의 "밀링 후에 생긴다" 논증의 전반부 |
| **Figure S5** | TEM-EDS 함침 확인 | — |
| **Figure S6** | **DC 분극 측정 원데이터** | 정상상태 도달 여부를 확인할 수 없다 (Huang 2026 G8 같은 함정) |
| **Figures S7, S8** | 율속 원곡선(Fig. 1F·2D·2E 의 출처), S8 은 기공 분석에도 인용 | Fig. 2D/2E 의 점들을 숫자로 못 읽는다 |
| **Figure S9** | 탄소 기공 크기 "mostly below 10 nm" | TPB 멀티스케일 계산의 입력 |
| **Figure S10** | 네 탄소의 **Raman·XPS** | 교란변수(I_D/I_G, O/C)의 실제 크기 (G4) |
| **Figure S11** | **성능 vs 물성 상관분석** | "상관이 far less pronounced" 주장의 유일한 근거 (G4) |
| **Figures S12B, S12C** | **황 없는 C/SSE 대조군**의 형태·입도 | §6.3 의 대조 실험 원자료 |
| **Figure S13** | 입도 분포 원자료(황 유무 비교) | — |
| **Figure S14** | 개별 C·S EDS 맵 | Fig. 3B 중첩 맵의 분해 |
| **Figure S15** | ★ **Young–Laplace 모세관압 계산 (151–198 vs 59–64 MPa)** | γ·θ·기공반경 입력을 모른다 (§6.7) |
| **Figure S16** | operando 압력 측정 셋업 | Δ(ΔP)_Q 의 정의 |
| **Figure S17** | ★ **단면 SEM**(두께 증가 46.6 / 36.8 %, 비가역 11.8 %, 균열·공극 분할) | 균열/공극 **분율 수치가 없다** (G18) |
| **Figure S18** | 고로딩 셀의 전류 프로토콜 | Fig. 4D 의 조건 |
| **Table S1** | 네 탄소의 **기공 제원**(표면적·기공부피·기공크기) | 모든 기공 논증의 기반 수치 |
| **Table S2** | ★ **선행 ASSLSB 성능 비교표** (Fig. 5D 의 데이터) | 문헌 비교를 우리가 재현할 수 없다 |
| **Table S3** | ★ **5 Ah 셀 에너지밀도 계산 전제** | Fig. 5C 의 >350 / >500 Wh kg⁻¹ 주장 전체 (G19) |

---

## 15. 우리 연구와의 접점

### 15.1 이식 가능 / 불가

| 이 논문의 것 | 우리에게 | 단서 |
|---|---|---|
| **DC 분극 σ_eff,elec / σ_eff,ion 측정 프로토콜** (§3.4 — 복합체 50 mg, ion-blocking 700 MPa / electron-blocking 200 MPa + 양면 LPSBI, Li–In 양면, ±50 mV 1 h) | **◎ 가장 값싼 이식.** 이 위키의 세 DC 분극 논문 중 **시료 정체를 가장 명확히 적은 것** | 두 측정의 성형 압력이 다르다(G22) — 우리는 **같은 압력으로 통일**해야 비교가 선다 |
| **σ_eff,elec 의 외부 기준값 0.015–0.108 S cm⁻¹ @ 탄소 21 wt%** | **◎** 우리 AB 20 wt% 가 전자 퍼콜레이션 고원 위인지 판단할 **첫 외부 눈금** | 탄소 종류가 다르다(다공성 호스트 vs AB) · 활물질이 S8 |
| **수세(탈이온수 24 h) + 원심 + 입도/XRD/SEM 로 밀링 후 S/C 구조를 본다** (§3.6) | **◎ 비용 거의 0.** 우리 30:50:20 에 그대로 적용 가능 | **Li2S 는 물과 반응해 H2S 를 낸다** — 황(S8)과 달리 **우리 계에서는 활물질도 같이 사라진다.** 그래서 우리에겐 "SE 와 Li2S 를 둘 다 씻어내고 **탄소 골격만** 본다" 는 다른 실험이 된다. 후드·중화 필수 |
| **operando 압력의 용량 정규화 Δ(ΔP)_Q (MPa mAh⁻¹)** | **○** 셀 간 비교 지표 | 정의식이 본문에 없다 |
| **micron 창 2.5–7 µm** (Cronk 0.5–5 µm 와 교집합 **2.5–5 µm**) | **○ 가설로** — [[reference-cell-500-600-mahg]] H3 | Jeong 의 크기는 **탄소 호스트**, Cronk 는 **활물질**. 우리 AB 는 호스트가 아니다 |
| **전극 기준 용량(mAh g⁻¹_electrode)을 1차 지표로 삼는 규율** (§8.1) | **◎ 즉시** — [[capacity-normalization-li2s-vs-sulfur]] 에 반영 | 이 기준에서 **우리 30:50:20 은 불리하다**(활물질 30 wt%). 그 사실 자체가 발견 |
| **밀링을 간헐(5 min / 10 min 휴지)로 쪼개 열을 제어한다** | **○** [[composite-cathode-mixing-routes]] 의 새 열 | Li2S 는 녹지 않는다(m.p. 938 °C) — **황 전용 이유**다. 우리 계에 같은 동기가 있는지는 불명 |
| 멜트 함침(155 °C 12 h) | **✕ 불가** — Li2S 는 녹지 않는다 | 우리 계에 대응되는 공정이 없다 |
| 1,535.6 mAh g⁻¹(S) · 9 mAh cm⁻² 같은 성능 수치 | **✕ 직접 비교 불가** — 활물질(S8 vs Li2S)·SE(LPSBI vs LPSCl)·조성·온도가 전부 다르다 | 비교는 **이용률(%)과 전극 기준 용량**으로만 |
| 250 사이클 94.24 % Li 금속 full cell | **✕** — `[재현]` **N/P ≈ 3.4 의 Li 과잉 셀**(G10)이고 **I 함유 SE 의 LiI interphase 기여를 저자가 인정**(§8.3) | [[anode-free-li2s-assb]] 에 주는 근거가 **없다** |

### 15.2 [[reference-cell-500-600-mahg]] 라우팅

| 가설 | 이 논문의 기여 | 방향 |
|---|---|---|
| **H1 (활성화 / 활성화 완료 전위 > SE 산화 전위)** | **근거 없음.** S8 출발이라 Li2S 첫 충전이 없다. 다만 `[재현]` **I⁻ 산화 용량 상한 17.4 mAh g⁻¹(S)** 계산과, **3.1 V vs Li/Li⁺ 까지 CCCV 로 올리고도 이론 초과 용량이 안 나온다**(최대 91.8 % 이용률)는 관측은 **SE 산화 기여가 조성에 따라 작을 수도 있다**는 참고 사례 | 중립 (참고) |
| **H2a (전자 네트워크)** | ★★ **강한 반증 추가.** 탄소 21 wt% 고정, σ_e **6배 차**, **낮은 쪽이 이긴다.** 그리고 탄소 ≈20 wt% 복합양극의 σ_e 절대값(10⁻²–10⁻¹ S cm⁻¹)이 처음 생겼다 | **약화** |
| **H2b (이온 네트워크 / SE 부피)** | ★ **수정.** "SE 를 더 넣을 필요 없다" 는 유지되지만, **같은 SE 양에서 연결성이 3.2배 차이** 날 수 있다. **우리는 토르투오시티를 잰 적이 없다** — vol% 회계로는 판정 불가 | **재정의** |
| **H3 (입자 제한)** | ★★ **강한 지지 + 방향 지정.** "작을수록 좋다" 가 아니라 **마이크론**이다(2.5–7 µm). Cronk 와 창이 겹친다. 단 여기서 크기는 **탄소 호스트**의 것 | **강화 (방향 반전 유지)** |
| **H4 (단위 착시)** | ★ **지지 + 새 규율.** 저자 스스로 `[인쇄]` "SSE·탄소 분율을 늘리면 겉보기 이용률이 부풀고 셀 에너지는 준다" 고 적고 **전극 기준 용량**을 1차 지표로 제안한다. `[재현]` 우리 목표는 **150–180 mAh g⁻¹(composite)**, 이 논문은 **752.4** | **강화** |
| **H5 (기계적 제한)** | ★ **지지.** 첫 방전 후 양극 두께 **+46.6 % / +36.8 %**, 비가역 **11.8 %**, Δ(ΔP)_Q 로 셀 간 부피변화 차이, EIS 성장. **입자 크기가 기계적 열화를 가른다** | **강화** |

★ **가장 값싼 다음 실험 (이 digest 의 제안)**: 논지 페이지 Gap 과 이 카드 3번이 가리키던
**DC 분극 σ_e·σ_Li 측정**에 **눈금이 생겼다.** AB **10 / 20 / 30 wt%** 로 재서,
우리 값이 **10⁻²–10⁻¹ S cm⁻¹ 대**(이 논문의 범위)에 있으면 **전자는 병목이 아니다**가 거의
확정되고, **10⁻⁴ 대 이하**로 나오면 반론 3 이 살아난다. **셀을 조립하지 않고 분말·펠릿만으로
끝난다.**

---

## 16. 비판 (이 digest 의 판단)

1. **★ 제목의 두 양이 본문에 숫자로 없다.** "Reconciling **triple-phase boundaries** and
   **tortuosity**" 인데, TPB 밀도는 Fig. 2B 막대 두 개뿐이고 **토르투오시티 값은 단 하나도
   인쇄돼 있지 않다** (정의식만 있다). 두 양 모두 **모델 산출물**이고 **측정이 아니다**.
   실측된 것은 σ_eff 두 개, 입도, XRD, TGA, 두께, 임피던스다. **제목이 약속하는 정량적
   화해(reconciling)는 본문에서 일어나지 않는다** (G1).
2. **서론과 결론이 자기 셀의 조건과 싸운다.** 서론은 `[인쇄]` "**high stack pressures**" 와
   "**ultrathin (<30 μm) separator**" 가 Li creeping·단락을 부른다고 인용하는데,
   이 논문은 **50 MPa** 로 돌리고 **40–90 µm 분리막**을 전제로 >350–500 Wh kg⁻¹ 을 주장한다.
   그리고 그 에너지 계산에서 **50 MPa 를 유지하는 하드웨어를 분모에서 뺐다**(저자가 명시).
   `[해석]` 즉 **에너지 주장과 압력 조건이 같은 셀에서 동시에 성립한다는 보장이 없다.**
3. **SE 산화 기여를 측정하지 않았다 — 다만 이번엔 상한이 작다.**
   `[재현]` **LPSBI 의 I⁻ 1 e⁻ 산화 몫 계산**:
   M(Li7P2S8Br0.5I0.5) = 7×6.94 + 2×30.974 + 8×32.06 + 0.5×79.904 + 0.5×126.904 =
   **470.4 g mol⁻¹**. I⁻ → ½I2 가 **0.5 mol e⁻ / mol SSE** →
   0.5 × 26,801 mAh mol⁻¹ ÷ 470.4 g mol⁻¹ = **28.5 mAh g⁻¹(SSE)**.
   SSE 가 전극의 30 wt% 이므로 **8.55 mAh g⁻¹(electrode)**, 황 기준으로 ÷0.49 =
   **17.4 mAh g⁻¹(S)** = **1,535.6 의 1.1 %**. (Br⁻ 까지 1 e⁻ 산화하면 2배인 34.9
   mAh g⁻¹(S) = 2.3 %, 단 Br⁻ 산화 전위는 더 높다.)
   → **이 논문은 이 위키의 "이론 초과 용량" 문제군(digest 10편 중 5편)에 속하지 않고,
   할로겐 산화로 설명 가능한 몫도 작다.** 그러나 **그것을 보인 것은 저자가 아니라 이 계산**
   이고, **SE-only 대조셀은 여전히 없다** (G8). 티오포스페이트 골격의 산화는 계산 범위 밖이다.
4. **2×2 설계가 재료 4개짜리 관찰이다 (G4).** 상용 탄소 넷은 입자·기공 말고도
   비표면적·표면 산소·흑연화도가 전부 다르다. "far less pronounced" 라는 저자의 방어는
   **Figure S10·S11 에 있고 미확보**다. 같은 호스트를 **분쇄해서 입자만 줄인** 대조군
   (= 기공·화학 고정)이 있었다면 논증이 훨씬 강했을 것이다 — 그 실험이 없다.
5. **밀링이 만드는 화학을 보지 않았다 (G17).** 이 논문은 밀링을 **순수한 물리 과정**(열 + 전단
   → 황 이동)으로만 다룬다. **Cronk 2026 은 같은 공정에서 황–SE 계면 화학반응(Li3PS4+n)을
   보고했고**, 황화물 SE 와 황을 함께 가는 한 그 반응은 Jeong 의 시료에서도 일어났을 것이다.
   "SSE 를 물로 씻어내고 남은 S/C" 를 보는 방법 자체가 **계면상을 씻어내 버린다.**
6. **"안정" 의 정체가 섞여 있다 (G13).** 1,500 사이클과 250 사이클 모두 **양 끝점의 비**이고
   중간에 **±10–15 % 의 비단조 궤적**이 있다. 그리고 **CE 는 세 그림 모두 ≈100 % 로 평평해서
   구별력이 없다** — "안정" 의 근거는 **용량**뿐이다. 저로딩 상온(1.5 mg cm⁻²)과 고로딩 60 °C
   (6 mg cm⁻²)가 **다른 셀**이라는 것(G23)도 초록에서는 구분되지 않는다.
7. **셀 개수·오차막대가 전무하다 (G14).** σ_eff 의 3.2배·6.2배, TPB 1.8배, 2C 용량 3배가
   전부 단일 측정으로 보인다. 이 위키 digest 11편이 모두 같은 문제를 갖는다.
8. **full cell 의 성과를 양극 설계에 귀속할 수 없다 (§8.3).** 저자 스스로 요오드 SE 의
   LiI interphase 기여 가능성을 적었고, **Mic-S 로 돌린 Li 금속 full cell 대조군이 없다.**
   게다가 `[재현]` **N/P ≈ 3.4 의 Li 과잉**(G10)이라 Li 재고 관점의 정보가 0 이다.
9. **전극 면적이 없다 (G9).** `mg cm⁻²`·`mAh cm⁻²` 의 분모가 10 mm 인지 9 mm 인지에 따라
   **23 % 가 움직인다.** 초록의 ">9 mAh cm⁻²" 가 이 불확실성 위에 있다.
10. **"two-length-scale" 이라는 틀 자체가 세 번째 축을 가린다.** 실제 이 논문에서 Mic-L 을
    이기게 한 가장 강한 단일 관측은 **밀링 후 황 재배치 저항**(XRD·수세 입도)인데, 제목과
    Highlights 는 그것을 **"two-length-scale"** 로만 말한다. `[해석]` **세 길이 스케일이 아니라
    두 스케일 + 하나의 공정 변수**이고, 공정 변수가 사실상 승부를 갈랐다.

---

## 17. 이 저장소가 가져갈 것

1. **★ DC 분극 프로토콜 + 기준 눈금** — §3.4 를 그대로 옮기되 **ion-blocking 과
   electron-blocking 의 성형 압력을 통일**한다(G22 회피). 우리 30:50:20 펠릿을
   **AB 10 / 20 / 30 wt%** 로 재면, [[interface-quality-not-bulk-conductivity]] 반론 3 이
   이 논문의 **0.015–0.108 S cm⁻¹** 눈금 위에서 직접 판정된다.
2. **★ 수세 진단** — 복합양극을 탈이온수 24 h → 원심 2,000 rpm 10 min → 진공건조 후
   **입도(Mastersizer) · XRD · SEM**. 우리 계에서는 Li2S 도 함께 사라지므로
   **"밀링 후 탄소 골격이 어떻게 뭉쳤는가"** 를 보는 실험이 된다. **H2S 대비 필수.**
   우리 복합양극의 밀링 후 미세구조를 **이 위키는 한 번도 본 적이 없다.**
3. **전극 기준 용량(mAh g⁻¹_composite)을 1차 지표로 병기하는 규율** —
   [[capacity-normalization-li2s-vs-sulfur]] 에 **다섯 번째 분모**로 명시한다.
   우리 목표 500–600 mAh g⁻¹(Li2S) = **150–180 mAh g⁻¹(composite)**; 이 논문 **752.4**.
4. **"공정이 설계를 지운다" 는 독법** — 앞으로 논문을 읽을 때 **"그 재료의 장점이 혼합 후에도
   살아 있다는 증거가 있는가"** 를 묻는다. 대부분의 논문은 **pristine 분말의 BET·TEM** 만
   보여준다. 이것은 [[composite-cathode-mixing-routes]] 에 새 열로 추가할 질문이다.
5. **Mes-S = Ketjen Black 이 네 호스트 중 꼴찌였다는 사실** — 이 위키의 Huang 2026·Wang 2023
   대조군이 KB 를 쓴다. 그 논문들의 **낮은 기준선 해석에 단서를 달아야 한다.**
6. **밀링 간헐화(5 min on / 10 min rest)와 BPR 50:1** — [[mixing-equipment-ball-mill-thinky]]
   양식에 **"연속 vs 간헐" 열**을 추가할 근거.
7. **Δ(ΔP)_Q 정규화** — Qu 2025 식 operando 압력 측정을 할 때의 비교 지표.
8. **새 열린 질문 후보**: **"황화물 SE 와의 볼밀은 활물질 표면에 유익한 계면상을 만드는가,
   활물질을 재배치해 망치는가?"** — Cronk 2026 vs Jeong 2026 이 정면으로 갈린다 (§13.2).
   [[one-step-vs-two-step-mixing]] H4(에너지 총량 최적점)의 구체적 시험 설계가 여기서 나온다.

---

## 18. 그림 판독 기록 (무엇을 보고 무엇을 안 봤는가)

크로핑 결과: **본문 Fig. 1–5 (5장) + Scheme 1 + Graphical abstract = 7장**.
Scheme 1(p.10)과 Graphical abstract(p.1)은 `extract_figures.py` 의 캡션 앵커 탐지에서
**"그래픽 없음(img0/draw0)" 으로 오판돼 제외**됐다 — 두 장 모두 페이지에 래스터 이미지가
1장씩 실제로 존재했다(p.1 xref 1326, 1190×1190; p.10 xref 74, 1346×809). **bbox 를 수동
지정해 400 dpi 로 재크롭**하고 `figures.json` 에 `note` 로 사유를 남겼다.

| 파일 | 무엇 | **봤나** | 이 digest 가 그림에서만 읽은 것 |
|---|---|---|---|
| `fig_1.png` | Fig. 1 — 입자 크기와 수송 | **○ 봤다** | 1B·1C 전류밀도 색분포(0–0.20 A cm⁻²) · **1E 전도도 막대 4종 판독** · **1F 율속 4종 개별 판독** · 1D SEM 스케일바 2 µm |
| `fig_2.png` | Fig. 2 — 기공과 TPB | **○ 봤다** | **2B TPB 밀도 ≈510 / ≈285 µm⁻²** · **2D·2E 비용량 16점 판독** · 2E 기공직경 1.3/1.65/3.8/4.1 nm · 2C HAADF(CMK-3 만 규칙 줄무늬) |
| `fig_3.png` | Fig. 3 — 공정 유도 황 재배치 | **○ 봤다** | **3C 입도 3구간 × 4시료 판독** · 3D XRD 에서 Mic-L 만 결정질 황 없음 · 3E TGA 70 % 손실·종료온도 순서 · 3B EDS 중첩 색 판독 |
| `fig_4.png` | Fig. 4 — 구조 안정성·장수명 | **○ 봤다** | **4A 비단조 궤적**·조건 텍스트(0.7–2.5 V vs Li-In/Li⁺, 1.5 mg cm⁻², 60 µm Li0.5In, RT, 50 MPa) · **4B Δ(ΔP)_Q 10점** · **4C EIS 절편 15/28 Ω, 300사이클 후 650/1750 Ω** · **4D 세 로딩 면적용량** |
| `fig_5.png` | Fig. 5 — full cell·에너지 | **○ 봤다** | **5A V 자 궤적·3축** · **5B 전압곡선(plateau 2.05 / 2.3–2.45 V, 3.1 V CV 구간 ≈0.8 mAh cm⁻², 이력 0.3 V)** · **5C E_g·E_v 10점 + Li-ion 기준선 345/275 Wh kg⁻¹** · **5D 산점도 배치** |
| `fig_sch1.png` | Scheme 1 — 통합 설계 원리 | **○ 봤다 (수동 재크롭)** | 3열 × 2행 구조, 전극 패널의 **초록 연결선 = 이온 경로 / 빨간 ✕ = 차단** |
| `fig_ga.png` | Graphical abstract (p.1) | **○ 봤다 (수동 재크롭)** | 셀 모식도에 **Li metal anode + 구리색 집전체**(Methods 는 Ti 로드라고 적는다 — 표기 불일치), 제목 문구 "balancing TPB density and tortuosity" |

**안 본 것 (존재 자체를 확인 못 함):**
- **SI 전체** — Figures S1–S18, Tables S1–S3. **별도 파일이고 이번 수집에 없다.** §14 에 본문이
  SI 에 맡긴 항목을 전수 목록으로 남겼다. **그 내용에 대한 추정은 이 digest 에 없다.**
- 본문 p.12–14 의 **참고문헌 1–45** 는 서지만 확인했고 내용 대조는 하지 않았다.

**이 digest 가 원문 숫자를 바꾼 곳은 없다.** `[재현]` 로 표시한 것은 전부 계산식을 병기했고,
원문 내부의 불일치(G5·G6·G11·G12·G13·G18)는 **양쪽을 모두 남기고 어느 쪽이 맞는지 단정하지
않았다**.

---

**이 digest 의 한 줄 결론** (`[해석]`):
> 이 논문은 "전자 전도도를 6배 낮춘 쪽이 이긴다" 는 세 번째 독립 사례를 우리 탄소 함량대
> (21 wt%)에서 보여줌으로써 [[interface-quality-not-bulk-conductivity]] 의 **부정절을
> 강화했다.** 그러나 그 긍정절이 가리키는 "계면" 은 이 논문에서 **화학이 아니라 기하와
> 그 공정 보존**이다. 그리고 **반론 3(전자 퍼콜레이션 고원)은 닫히지 않았다** — 이 논문도
> 탄소 **양**을 바꾸지 않았기 때문이다. 다만 그것을 닫는 데 필요한 실험은 이제 하나이고,
> 이 논문이 그 실험의 **프로토콜과 눈금을 동시에 준다.**

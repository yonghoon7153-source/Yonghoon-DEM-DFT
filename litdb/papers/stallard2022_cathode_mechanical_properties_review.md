<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. -->
# LIB 양극재 기계물성 **리뷰** — Berkovich indentation E·H 는 **압흔 크기 ÷ 결정립 크기 (A_P^½/d)** 로 접히고 0.1 을 넘으면 입계 파쇄로 떨어지며, 입자 인장강도는 H/3 보다 한 자릿수 이상 낮고, **σ_F = K_IC/√(π·d/2)** 로 다결정 NMC333 의 **K_IC ≈ 0.05–0.3 MPa·m^½ 를 추정** — Stallard, Wheatcroft, Booth, Boston, Corr, De Volder, Inkson, Fleck (*Joule* 6, 984–1007, 2022)

> slug `stallard2022_cathode_mechanical_properties_review` · DOI `10.1016/j.joule.2022.04.001` · type `review (compilation of published experimental data: Berkovich nanoindentation E·H vs indent size and grain size, particle compression + biaxial flexure strength vs grain size and porosity, K_IC estimate from σ_F ∝ d^-1/2 with a = d/2, operando XRD lattice data; no original experiments)` · PDF `2e77cdde-PIIS2542435122001398.pdf` (24 pp, SI 없음) · digested `2026-09-26` · status ✅

> elements: Li, Ni, Mn, Co, Al, Fe, P, O, V
> methods: elastic

> **읽은 범위**: PDF 24쪽 전부 (요약 · 본문 · 그림 13장 캡션 · 감사 · 저자 기여 · 참고문헌 139편 전수).  **표는 0장**, **SI 는 없다** — 본문 어디에도 Supplemental information 언급이 없다 (전수 검색).
> **쪽 표기**: 이 카드의 "p." 는 **저널 쪽 (984–1007)** 이다.  PDF 쪽 = 저널 쪽 − 983 (예: p. 997 = PDF 14쪽).
> **라벨 규약**: `stated` = 본문에 숫자로 인쇄 · `vector-read` = **PDF 벡터 경로 좌표를 축 눈금으로 환산한 판독값** (래스터 판독보다 훨씬 정밀하지만 여전히 digitized — TREND 전용, stated 처럼 인용하지 말 것) ·
> `derived(ours)` = 우리 산술 (§15 원장) · `2차 인용` = 리뷰가 **다른 논문 값을 다시 그리거나 옮긴 것** — **이 카드의 거의 모든 수치가 이 등급이다** (원문 미확인, 리뷰 자체 측정은 0건).
> 리뷰 저자 **자신의 계산·추정**은 따로 `리뷰 추정` 으로 적는다 (K_IC 0.05–0.3 · 결함 ×5 · σ_F–d^-½ 등고선).
> **그림**: 13장 전부 `litdb/figures/stallard2022_cathode_mechanical_properties_review/` — **자동 3 + 손 재크롭 9 + 수동 신규 1**, 13장 전부 열어서 확인 (§5.1).
> ★ 이 카드는 원장 **SELF-51** 뿌리 감사 (우리 AM 입력 E_AM · ν_AM · K_IC · H_AM 의 출처) 의 **리뷰 층 대조**로 만들었다 — §0 · §7.

---

## 0. ★ SELF-51 질문 1–6 — 결론 먼저

| # | 질문 (우리 값) | 이 리뷰가 주는 것 (쪽 · 그림 · 1차 문헌 번호) | 등급 | 판정 |
|---|---|---|---|---|
| 1 | **E_AM = 140 GPa** (AM_P · AM_S 공통) | NMC 는 **부류가 아니라 A_P^½/d 에 따라** 값이 갈린다 (Fig 9C, p. 996): 이차입자(결정립 ≤ 1 µm) **작은 압흔 ≈ 110–143 → 압흔 > 결정립에서 ≈ 50–97 GPa**, 소결 펠릿(결정립 3–10 µm) **166–210**, NMC333 펠릿 **181–203**.  Fig 7 NMC 6점 **E 113–200**.  **리뷰 문장**: 모든 양극재 E *"varies from 80 to 200 GPa"* (p. 993).  ★ Fig 9 의 NMC532 "1 µm" 계열 5점은 **Xu 2017 [75] 의 하중 스윕과 한 GPa 안에서 일치** (우리 대조, §3-3) | vector-read (2차) · stated (범위) | ✅ **라벨만, 재계산 불요.**  140 = **이차입자 응집체 · 작은 압흔 (A_P^½/d ≈ 0.3–0.5) 부류** — `xu2017` (142.5) · `sedlatschek2026` (138) 판정과 정합.  ⚠ NMC811 · 단결정 NMC 의 E 는 **이 리뷰에 없다** (AM_S 는 여전히 "Assumed") |
| 2 | **ν_AM = 0.25** | **값이 없다** — ν 는 식 2 의 기호로만 등장 (p. 992).  리뷰에는 DFT 도 없다 | — | ⛔ **출처 없음 유지 ("Assumed")**.  포인터 1개: `so2022_dem_compaction_coated_particles_assb` 카드가 So 2022 Table 1 의 ν_AM 0.25 를 **Cheng [37]** 에 귀속한다고 기록 — 이 리뷰의 [76] Cheng 2017 (NMC333, *J. Eur. Ceram. Soc.*) 과 같은 논문일 **가능성** (서지 대조 [미확인]) |
| 3 | **K_IC_AM_P = 0.3 · K_IC_AM_S = 1.0 MPa·m^½** (옛 출처 "Quinn 2020 Joule 4, 2466" · "Liu 2020 Nat. Energy 5, 304") | ★ **Sedlatschek 가 말한 "Stallard 추정" 의 실체**: σ_F = K_IC/√(πa) 에 **a = d/2 (결함 = 결정립 절반)** 를 넣어 Fig 10C 에 등-K_IC 등고선 (0.05 · 0.1 · 0.2 · 0.3) 을 긋고 강도 자료와 대조 → *"implies a fracture toughness K_IC between 0.05 and 0.3 MPa m^1/2 for polycrystalline samples of fully lithiated, layered NMC333"* (p. 997–998).  자료 = 이차입자 압축 [107] + 소결 펠릿 이축굽힘 [109].  단결정은 **LiCoO₂ 큰 결정립 압입 0.2–6.5 (방위 의존)** [66] 뿐.  **"Quinn 2020" · "Liu 2020" 은 참고문헌 139편 어디에도 없다** | 리뷰 추정 (stated) + vector-read | ⚠ **라벨 교체 가능, 재계산은 1저자 결정**.  우리 0.3 = 리뷰 추정 범위의 **상한** (= 이차입자 상자그림 윗수염이 정확히 0.300, derived).  리뷰 자신의 이차입자 자료 중앙은 **≈ 0.19** (IQR 0.16–0.22, derived) · Xu 2017 pop-in 0.10 · Sharma 0.271 ([Sedl26] 경유).  ⇒ **{0.10, 0.19, 0.30} 민감도 팔 등록 권고**.  K_IC_AM_S 1.0 = NMC 근거 **없음** (LCO 0.2–6.5 가 걸칠 뿐, 방향 "입내 ≫ 입계" 만 정성 지지) |
| 4 | **H_AM** — `fracture_model.py` **6.0 GPa** · `am_load_balance_jam.py` 사전등록 판정선 **"NCM811 압입 경도 문헌대 ≈ 3~6 GPa"** (역산 3.83–3.85 "밴드 안") | 두 부류가 갈린다: **작은 압흔 (stage I)** — Fig 7 NMC **7.1–14.0 GPa** (6점), 리뷰 문장 *"hardness varies from 6 to 18 GPa"* (p. 993, 전 양극재).  **압흔 ≥ 결정립 (stage III, "granular flow")** — Fig 9B/D 의 NMC532 이차입자 (결정립 0.1–1 µm) **5.5 → 3.2 GPa** (A_P^½ 0.59–2.59 µm, A_P^½/d 1.1–4.6), 1 µm 결정립 계열의 10 mN 점 **6.9 GPa** | vector-read (2차) | ⚠ **"3–6 GPa" 에 처음으로 문헌 짝이 생겼다 — 단 사후 부합이다.**  역산 3.83–3.85 는 자홍 계열의 **A_P^½ ≈ 1.72 µm (A_P^½/d ≈ 3.1)** 점과 같다 (derived).  한정어 4개: NMC**532** · **단일 계열** · 1차 출처 **미표기** (추정 [74]) · 값이 **크기 의존**이고 2.6 µm 까지 **포화 안 함**.  ⇒ 밴드를 *"stage-III (압흔 ≥ 결정립) 압입 경도 부류"* 로 **런 전에 재등록**하면 쓸 수 있다.  6.0 은 두 부류 사이의 무소속 값 — 라벨만 ("informational, 근거 없음") |
| 5 | **파괴강도 앵커** (Wheatcroft 2023 NMC811 207 MPa 등) | 방법 = **Brazil-nut 입자 압축, σ_F = 2.8 P_C/(π d_P²)** (식 4, Hiramatsu–Oka [108] · Yoshida [111]) + 이축굽힘 [109].  NMC333 이차입자 [107]: **pristine 중앙 185.6 MPa** (상자 156–216, 수염 128–289) · 전해질 침지 후 **158.9** · 첫 탈리튬화 후 **21.5** · 첫 사이클 후 **70.3** (= 침지값의 **44 %**, 본문).  NMC333 소결 펠릿 [109]: **20–48 MPa** (결정립 0.9–10.6 µm, 기공 4.7–38 %).  **리뷰 문장**: 인장강도는 σ_Y ≈ H/3 보다 *"an order of magnitude or more below"* (p. 996) | vector-read (2차) · stated (44 %, 결함 ×5) | ✅ **NMC333 앵커 확보 (2차)**.  ⚠ **Wheatcroft 2023 은 이 리뷰에 없다** (리뷰보다 나중 논문; 같은 그룹) — NMC811 207 MPa 는 [Sedl26] 의 2차 인용으로만 안다 ⇒ **원문 필요**.  σ_F 는 **결정립 크기 · 사이클 이력**의 함수라 단일 상수가 아니다 |
| 6 | **측정 부류별 차이** (우리 판정 "140 = 응집체 부류") | 리뷰의 정리 축은 부류 이름이 아니라 **A_P^½/d** 다: < 0.1 이면 E 가 거의 일정 (stage I, 입내 소성), > 0.1 이면 **입계 파쇄로 E·H 동반 하락** (stage II–III).  이차입자 (d 0.1–1 µm) 는 보통 압흔으로도 이미 0.25–4.6 구간 = 응집체 값, 펠릿·큰 결정립 (d 3–100 µm) 은 0.004–0.4 = 치밀체 값 (Fig 9C/D, vector-read).  **DFT 부류는 리뷰에 없다**.  단결정 NMC 도 없다 (LCO 큰 결정립만) | stated (메커니즘) + vector-read | ✅ **판정 정합 + 정밀화**: "응집체 부류" 의 E 는 **그 안에서도 A_P^½/d 의 함수**다 — 140 은 A_P^½/d ≈ 0.3–0.5 구간 값 (Xu 1–2 mN).  입자 스케일 접촉은 더 큰 A_P^½/d 로 가므로 **유효 E·H 가 더 낮을 수 있다** (§7-1, §7-4) |

**한 줄 판정**: 이 리뷰는 **새 1차 값을 주지 않는다** — 기존 문헌을 다시 그려 **하나의 축 (A_P^½/d)** 과 **하나의 추정 (K_IC 0.05–0.3)** 을 준다.
우리 입력 5개 중 **재계산이 필요한 것은 없다**. **라벨 교체 2개** (E_AM · K_IC_AM_P), **재등록 권고 1개** (H_AM 밴드), **출처 없음 유지 2개** (ν_AM · K_IC_AM_S).

---

## 1. 한 줄 요약

Cambridge (Fleck) · Sheffield (Inkson) · Faraday Institution "FutureCat" 그룹이 **LIB 양극재 (층상 NMC·LCO · 스피넬 LMO/LNMO · 올리빈 LFP/LCP)** 의
**탄성률 E · 압입 경도 H · 인장 파괴강도 σ_F** 측정 문헌을 모아 **공학 세라믹의 틀**로 다시 읽은 튜토리얼 리뷰 (자체 실험 0).
핵심 주장 넷: ① E·H 의 **압입 크기 효과는 결정립 크기가 길이척도**다 — A_P^½/d 로 자료가 한 곡선에 모이고 **0.1 을 넘으면 입계 파쇄로 E·H 가 함께 떨어진다** (Fig 8 · 9).
② 이차입자·펠릿의 **인장강도는 H/3 보다 한 자릿수 이상 낮고** 결정립 크기에 **σ_F ∝ d^−½** 로 따른다 = **결정립 크기의 기존 결함**에서 출발하는 취성 파괴 (Fig 10 · 11).
그 틀로 **다결정 NMC333 의 K_IC 를 0.05–0.3 MPa·m^½ 로 추정** — LCO 큰 결정립의 입내 인성 0.2–6.5 보다 훨씬 낮아 **"충전 시 입계 파괴"** 를 설명한다.
③ **전해질 침지는 기계물성을 거의 안 바꾸고** (Fig 12A), **탈리튬화·사이클은 입계 미세균열로 E·H·σ_F 를 함께 깎는다** — 첫 사이클이 가장 크고 (강도 44 %, 결함 ≈ ×5), H/H₀ ≈ E/E₀ (Fig 12D · 13D).
④ 격자 변화는 층상 = **비등방**, 스피넬 = **등방** (Fig 4) → 층상 이차입자가 첫 충전에서 입계로 부서지는 이유.  대책 6가지 (변형 억제 · 코어-셸 · 1차입자 미세화 · 방위 정렬 · **단결정** · 확산거리 단축).
★ 우리에게는 **SELF-51 의 K_IC "Stallard 추정" 원문**이고, **H_AM "3–6 GPa" 밴드에 처음 붙는 문헌 짝 (단 stage-III · NMC532 · 사후)** 이며, **"응집체 vs 치밀체" 부류 판정을 A_P^½/d 로 정밀화**하는 근거다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Joe C. Stallard**¹ · Laura Wheatcroft² · Samuel G. Booth² · Rebecca Boston² · Serena A. Corr² · Michaël F. L. De Volder¹ · Beverley J. Inkson² · **Norman A. Fleck**¹\* (교신) |
| 소속 | ¹ Department of Engineering, University of Cambridge (Trumpington St., Cambridge CB2 1PZ, UK) · ² Department of Materials Science and Engineering, University of Sheffield (Mappin St., Sheffield S1 3JD, UK) |
| 저널 | *Joule* **6**, 984–1007 (2022-05-18) — Cell Press **Review**.  © 2022 Elsevier Inc.  ⚠ 호수 "(5)" 는 PDF 에 인쇄돼 있지 않다 ([Sedl26] 참고문헌 [30] 의 표기) |
| DOI | `10.1016/j.joule.2022.04.001` (PII S2542-4351(22)00139-8 — 업로드 파일명 `PIIS2542435122001398`) |
| 접수·채택일 | **인쇄 없음** (n/a) |
| 자금 | Faraday Institution **"FutureCat"** (grant FIRG017) — 전 저자 |
| 저자 기여 (원문) | *"Data were collected by J.C.S., L.W., and S.G.B."* — ⇒ 그림의 자료점은 **리뷰 저자들이 문헌에서 다시 모은 값** (재디지타이즈 가능성) · 초고 J.C.S. · L.W. |
| 이해상충 | 없음 (stated) |
| SI · 데이터 | **없음** |
| 소재 | 층상 NMC (111/333 · 532 · 811 · 316) · LCO · NCA (언급만) · LNO · 스피넬 LMO · LNMO · 올리빈 LFP · LiCoPO₄ (LCP) · ε-LiVOPO₄ (Ragone 만) |
| 전해질 맥락 | **액체** LIB (1 M LiPF₆ 계).  황화물·고체전해질 **자료 0** — 격자 자료 [38] Strauss 2020 만 ASSB 논문 |
| 연구유형 | 리뷰 — 실험 문헌 종합 + 리뷰 저자 추정 (K_IC 등고선 · 결함 성장 배수 · 다공 경험식) |
| 같은 그룹 후속 | **Wheatcroft et al. 2023** (NMC811 이차입자 SEM in situ 파괴시험, *Batter. Supercaps*) — **이 리뷰에 없다** (시간상 뒤) · [Sedl26] 참고문헌 [38] 로만 안다 |

---

## 3. 핵심 수치 ★ (stated / vector-read / derived 구분 — **전부 2차 인용**)

### 3-1. 본문에 인쇄된 수치 (stated) — 쪽 · 1차 문헌

| 수치 | 원문 | 쪽 | 1차 문헌 (리뷰 번호) |
|---|---|---|---|
| NMC 이차입자 지름 **5–20 µm**, 결정립 (1차입자) **0.1–2 µm** | *"NMC cathodes comprise secondary particles of diameters 5–20 µm … grains of dimensions 0.1–2 µm"* | p. 987 | [22] |
| Berkovich 팁 반경 **≈ 1 µm** | *"the 3-sided diamond indenter has a tip radius R on the order of 1 µm"* | p. 993 | — |
| 양극재 **H 6–18 GPa · E 80–200 GPa** | *"The hardness varies from 6 to 18 GPa, whereas the Young's modulus varies from 80 to 200 GPa."* | p. 993 | [66–77] (Fig 7) |
| H ≈ 3σ_Y | *"the hardness is directly related to the yield strength σY, such that H≈3σY"* | p. 992 | [79] Tabor |
| Berkovich 면적 **A_P = 24.5 d_I²** (식 3, pile-up 없음) | — | p. 994 | [89] |
| 이차입자 결정립 **0.1–1 µm**, 열간가압 펠릿 결정립 **3–100 µm** | *"The grain size within the secondary particles lies between 0.1 and 1 µm, whereas the hot-pressed pellets are of larger grain sizes between 3 and 100 µm."* | p. 994 | [66, 74–77, 98] |
| **A_P^½/d > 0.1 이면 E·H 하락 (입계 파쇄), < 0.1 이면 E 거의 불변** | *"The decrease of both modulus and hardness with increasing A_P^1/2/d for (A_P^1/2/d) > 0.1 is associated with fragmentation by grain boundary fracture"* | p. 996 | [102, 103] |
| 이차입자 대표 지름 **10 µm** | *"of a typical diameter of 10 µm"* | p. 996 | — |
| Brazil-nut 식 **σ_F = 2.8 P_C/(π d_P²)** (식 4) | — | p. 996 | [108, 111] |
| 인장강도 ≪ H/3 | *"the tensile strengths are an order of magnitude or more below the uniaxial yield strength σY≈H/3 for all of the layered transition metal oxides"* | p. 996 | (Fig 7 · 10) |
| 결함 크기 ≈ 결정립 크기, **a = d/2** | *"the length of such pre-existing flaws is on the order of the grain size … relating the characteristic flaw dimension a to the grain size d according to a = d/2"* | p. 997 | [114, 115] |
| 기공 > 11 % 제외 시 펠릿 강도는 결정립↓ 에 따라 ↑ | *"With the exception of samples with porosity exceeding 11%, the measured fracture strength of NMC sintered pellets increases with decreasing grain size"* | p. 997 | [109] |
| ★ **K_IC 0.05–0.3 MPa·m^½** (리뷰 추정) | *"A comparison of the predictions with the experimental measurements implies a fracture toughness KIC between 0.05 and 0.3 MPa m1/2 for polycrystalline samples of fully lithiated, layered NMC333 (see Figure 8C)."* — ⚠ "Figure 8C" 는 **Fig 10C 의 오참조** | p. 997–998 | [107, 109] 자료 + 리뷰 계산 |
| 낮은 인성 = 입계 파괴의 전형 | *"This low value of toughness for a polycrystalline ceramic is typically associated with intergranular fracture."* | p. 998 | [109] |
| **LiCoO₂ 큰 결정립 입내 인성 0.2–6.5 MPa·m^½** (방위 의존) | *"the fracture toughness measured by indentation within large single grains of LiCoO2 lies between 0.2 and 6.5 MPa m1/2 and varies with the orientation"* | p. 998 | [66] Qu 2012 |
| 침지 영향 미미 | NMC532 펠릿·이차입자 E·H: *"low sensitivity to immersion"* [74] · NMC333 이차입자 강도: *"similarly unchanged by immersion"* [107] (1 M LiPF₆/EC 48 h → DMC 세척 → NMP 80 °C 30 min → 건조) | p. 998 | [74, 107] |
| 전형 상한전압 | NMC811 기계 연구의 **UCV 4.8 V** ↔ 실사용 **4.2–4.3 V** | p. 999 | [116] |
| 첫 사이클 강도 **44 %** · 결함 **≈ ×5** (리뷰 계산) | *"After a single cycle, secondary particles possess an average fracture strength only 44% of that measured for pristine particles"* · *"the flaw size a … increases by a factor of about 5 over the first cycle"* | p. 1000 | [107] |
| NMC811 이차입자 기공 **0.14 → 0.19 (5 사이클)** | *"the porosity of a LixNi0.8Mn0.1Co0.1O2 secondary particle increased from 0.14 to 0.19 over 5 cycles"* | p. 1001 | [121] Heenan 2020 |
| 다공 경험식 **H = H₀e^(−αf_P) · E = E₀e^(−βf_P)** | α · β 는 입계 강도 · 맞물림 정도에 민감 (값 없음) | p. 1001 | [118, 122] |
| 스피넬 (Ni 치환 · 무질서) 상전이 억제 → x > 0.13 에서 **셀 치수 1 % 이내** | — | p. 990 | [20] |
| LCO: 0.75 < x < 1 두 상 공존 · **x = 0.5 에서 육방 → 단사** → 추출 50 % 로 제한 | — | p. 990 | [45, 46, 40] |
| NMC: 초기 c 팽창 (전하 차폐 상실), **x < 0.4 에서 c 수축** (Ni 산화 · O–O 간격 축소) | — | p. 990 | [37, 41, 42] |
| LFP Ragone: 같은 에너지밀도에서 **출력 최대 100×** · 같은 입경에서 **×50** | — | p. 989 | [12–14, 23, 28–30] |

### 3-2. ★ 부류별 E · H · K_IC · σ_F — 이 리뷰가 모은 값 한 장 (사용자 요청 표)

> 값 = 리뷰 그림의 **vector-read** (§6-2 절차) 또는 stated.  "1차 문헌" 칸의 번호는 **리뷰가 캡션·본문에 단 번호**다.
> ⚠ Fig 7 · 9 는 캡션이 번호를 **묶어서** 달고 계열별로 나누지 않았다 — 계열 ↔ 문헌 대응 중 **"(식별)"** 은 우리 수치 대조로 확정한 것, **"(추정)"** 은 근거가 정황뿐인 것.

| 부류 | 재료 · 결정립 · 조건 | E (GPa) | H (GPa) | K_IC (MPa·m^½) | σ_F (MPa) | 1차 문헌 | 그림 · 쪽 | 등급 |
|---|---|---|---|---|---|---|---|---|
| **큰 결정립 (단결정급)** | LCO, 결정립 > 100 µm, 결정립 **안** 압입 | ≈ 175 (별표) | 11.8 [7.9, 15.5] | **0.2–6.5 (방위 의존)** | — | [66] Qu 2012 (K: stated · E/H 계열: 추정) | Fig 9 · p. 998 | stated + vector-read |
| 박막 | LCO, 결정립 ≈ 80 µm | 176 [173, 183] | 8.2 [7.8, 8.8] | — | — | [98] Swallow 2014 (본문 p. 1000 이 80 µm ↔ [98] 연결) | Fig 9 | vector-read |
| 소결체 | LCO, 8.5 ± 3.5 µm | 200 → 183 | 9.8 → 7.1 | — | — | [77] Cheng 2017b (추정) | Fig 9 | vector-read |
| **치밀 펠릿** | **NMC333**, 4.2 ± 1.5 µm (열간가압) | **181–203** | **9.2–11.8** | — | — | [76] Cheng 2017 (추정 — 유일한 NMC333 압입 인용) | Fig 9 | vector-read |
| **치밀 펠릿** | **NMC532**, 3–10 µm | **210 → 166** (A_P^½ 0.24 → 2.47 µm) | **11.2 → 6.8** (0.59 → 2.59 µm) | — | — | [74] de Vasconcelos 2019 (추정) | Fig 9 | vector-read |
| 치밀 펠릿 (건 · 침지) | NMC532 | 198 · 198 | 14.3 · 14.7 | — | — | [74] (stated 연결, p. 998) | Fig 12A | vector-read |
| **이차입자 (응집체)** | **NMC532**, 결정립 1 µm | **143 → 86** (1 → 10 mN) | **8.6 → 11.7 → 6.9** | — | — | ★ [75] **Xu 2017 (식별 — 5점 모두 ±1 GPa, §3-3)** | Fig 9 | vector-read |
| **이차입자 (응집체)** | **NMC532**, 결정립 0.1–1 µm | **126 → 51** (0.24 → 2.47 µm) | **5.5 → 3.2** (0.59 → 2.59 µm) | — | — | [74] (추정) | Fig 9 | vector-read |
| 이차입자 (건 · 침지) | NMC532 | 110 · 109 | 7.56 · 7.46 | — | — | [74] (stated 연결) | Fig 12A | vector-read |
| **이차입자 강도** | **NMC333**, 결정립 0.5–1 µm, pristine | — | — | **0.13–0.30** (중앙 **0.19**) ← derived | **185.6** (상자 156.3–216.0 · 수염 128.3–289.2) | [107] Dang 2019 | Fig 10C | vector-read + derived |
| 이차입자 강도 (이력) | NMC333: 침지 후 / 첫 탈리튬화 후 / 첫 사이클 후 | — | — | — | **158.9 / 21.5 / 70.3** (중앙) | [107] | Fig 13A · p. 1000 | vector-read (44 % 는 stated) |
| **펠릿 강도 (이축굽힘)** | NMC333, 결정립 0.9–10.6 µm, 기공 4.7–38 % | — | — | **0.025–0.141** ← derived | **20.4–48.2** | [109] Huddleston 2020 | Fig 10C | vector-read + derived |
| **리뷰 추정** | 다결정 NMC333 (펠릿 + 이차입자), 완전 리튬화 | — | — | ★ **0.05–0.3** | — | 리뷰 계산 (a = d/2) | Fig 10C · p. 997–998 | stated |
| 층상 NMC 전체 (Fig 7) | as-manufactured, 완전 리튬화, Berkovich | **113–200** (6점) | **7.1–14.0** | — | — | [66–77] 묶음 | Fig 7 | vector-read |
| 전 양극재 (리뷰 문장) | LCO · LMO · NMC · LCP | **80–200** | **6–18** | — | — | [66–77] | p. 993 | stated |
| **DFT** | — | **없음** | 없음 | 없음 | — | — | — | — |
| **단결정 NMC** | — | **없음** (구조 대책으로만 언급) | 없음 | 없음 | 없음 | [11, 137–139] (합성·전기화학) | p. 1002 | — |

### 3-3. Fig 9 — E · H vs 압흔 크기 A_P^½ (µm), **vector-read 전수** (괄호 = 오차막대)

| 계열 (범례 · 채움 여부) | 점 (A_P^½ µm → 값) |
|---|---|
| **NMC532, 1 µm** (이차입자, 채운 파란 원) — **E** | 0.341 → **143** [131, 154] · 0.447 → **141** [130, 152] · 0.506 → **121** [113, 129] · 0.829 → **101** [93.7, 109] · 1.20 → **86.1** [79.9, 92.3] |
| 〃 — **H** (막대 없음) | 0.341 → **8.60** · 0.447 → **10.0** · 0.506 → **11.7** · 0.829 → **8.74** · 1.20 → **6.91** |
| **NMC532, 0.1–1 µm** (이차입자, 채운 자홍 마름모) — **E** | 0.137 → 109 [82.3, 135] · 0.239 → **126** [103, 150] · 0.339 → 117 [100, 135] · 0.415 → 112 [96.7, 128] · 0.531 → 104 [91.2, 116] · 0.684 → 97.0 [85.3, 109] · 0.754 → 93.2 [82.1, 104] · 1.02 → 81.3 [72.4, 90.3] · 1.23 → 73.6 [66.1, 81.1] · 1.54 → 65.0 [58.3, 71.7] · 1.73 → 61.8 [55.1, 68.5] · 1.93 → 57.9 [51.2, 64.7] · 2.03 → 56.3 [49.3, 63.4] · 2.13 → 54.7 [47.4, 62.1] · 2.43 → 50.9 [44.7, 57.1] · 2.47 → **50.6** [44.7, 56.5] |
| 〃 — **H** (막대 없음) | 0.587 → **5.49** · 0.631 → 5.50 · 0.817 → 5.06 · 0.973 → 4.69 · 1.03 → 4.62 · 1.14 → 4.57 · 1.31 → 4.41 · 1.38 → 4.37 · 1.46 → 4.24 · 1.59 → 4.02 · 1.65 → 4.00 · 1.76 → 3.77 · 1.82 → 3.69 · 1.98 → 3.62 · 2.09 → 3.53 · 2.16 → 3.44 · 2.29 → 3.40 · 2.32 → 3.39 · 2.40 → 3.34 · 2.48 → 3.30 · 2.53 → 3.28 · 2.59 → **3.21** |
| **NMC532, 3–10 µm** (소결 펠릿, 빈 빨간 사각) — **E** | 0.137 → 153 [105, 202] · 0.239 → **210** [180, 239] · 0.339 → 209 [189, 228] · 0.415 → 205 [186, 224] · 0.531 → 201 [185, 217] · 0.684 → 200 [185, 214] · 0.754 → 199 [184, 214] · 1.02 → 190 [178, 203] · 1.23 → 188 [176, 200] · 1.54 → 180 [168, 192] · 1.73 → 177 [165, 190] · 1.93 → 177 [162, 192] · 2.03 → 173 [159, 187] · 2.13 → 172 [156, 188] · 2.43 → 166 [151, 182] · 2.47 → 168 [153, 182] |
| 〃 — **H** (막대 없음) | 0.587 → **11.2** · 0.631 → 10.3 · 0.817 → 10.7 · 0.973 → 10.3 · 1.03 → 9.42 · 1.14 → 9.56 · 1.31 → 9.10 · 1.38 → 8.51 · 1.46 → 8.57 · 1.59 → 8.27 · 1.65 → 8.37 · 1.76 → 8.47 · 1.82 → 8.46 · 1.98 → 8.58 · 2.09 → 8.05 · 2.16 → 8.03 · 2.29 → 7.37 · 2.32 → 7.39 · 2.40 → 7.34 · 2.48 → 7.07 · 2.53 → 7.10 · 2.59 → **6.84** |
| **NMC333, 4.2 ± 1.5 µm** (펠릿, 빈 검은 삼각) — E / H | 0.214 → 203 [190, 213] / 11.0 [10.2, 11.7] · 0.292 → 199 [184, 211] / 11.8 [10.7, 12.7] · 0.674 → 200 [186, 210] / 11.1 [10.0, 12.0] · 1.05 → 181 [172, 187] / 9.16 [8.46, 9.66] |
| LCO, 8.5 ± 3.5 µm (빈 회색 마름모) — E / H | 0.320 → 200 [191, 209] / 9.79 [8.69, 10.9] · 0.503 → 191 [181, 201] / 7.90 [6.80, 8.99] · 0.840 → 183 [177, 189] / 7.09 [6.29, 7.89] |
| LCO, 80 µm (빈 녹색 역삼각) — E / H | 0.380 → 176 [173, 183] / 8.2 [7.8, 8.8] |
| LCO, > 100 µm (회색 별 + 상자) — E / H | 0.413 → 175 (별) / 11.8 [7.9, 15.5] — 패널 A 의 회색 상자 (≈ 155–190, 수염 ≈ 150–235) 는 **판독 안 함** (그림으로만) |

- ★ **파란 계열 = Xu 2017 [75] (우리 식별)**: `xu2017_nmc532_…` 카드 §3-5 의 Fig 4c 준정적 판독 **1 · 2 · 3 · 6 · 10 mN → 142 · 141 · 121 · 102 · 86 GPa** 와
  이 리뷰의 **143 · 141 · 121 · 101 · 86** 이 모두 ±1 GPa 안.  게다가 리뷰의 x 값이 **A_P^½ = √(P/H)** 를 P = 1, 2, 3, 6, 10 mN 과 판독 H 로 **소수 셋째 자리까지** 재현한다
  (0.341 · 0.447 · 0.506 · 0.829 · 1.203, derived D8).  ⇒ 첫 점 (8.60 GPa · 143 GPa) 은 Xu 2017 Table 1 의 pristine (8.6 · 142.5) 과 같은 값 — 같은 1 mN 측정으로 읽힌다 (우리 추론).
  ⚠ 그 **H 계열 (2–10 mN 의 10.0 · 11.7 · 8.74 · 6.91)** 이 Xu 2017 의 어느 그림에서 왔는지는 `xu2017` 카드가 E–하중만 판독해 **확인 불가**.
- **정규화 d (Fig 9C/D 의 가로축)**: 리뷰는 표기 범위의 **중앙값**을 d 로 썼다 — 자홍 0.55 · 빨강 6.5 · 파랑 1.0 · 검정 4.2 · 회색 8.5 · 녹색 80 · "> 100" 은 100 µm (A_P^½ ÷ (A_P^½/d) 역산, derived D9).
  ⇒ 9C/D 의 가로 위치는 그 선택에 **로그로 ±0.3 (≈ ×2) 흔들릴 수 있다** (자홍 0.1–1 µm 범위의 끝을 쓰면).
- 자홍 H 계열은 **A_P^½ 0.59–2.59 µm 에서 log-log 기울기 −0.36** 으로 계속 떨어지고 **포화하지 않는다** (derived D10).

### 3-4. Fig 10C — σ_F vs d^−½ (NMC333), **vector-read** + 등고선 역산

| 시료 | d^−½ (µm^−½) → d (µm) | 기공 (라벨) | σ_F (MPa) [막대] | 가로 막대 (d^−½) | **K_IC 역산 (a = d/2)** derived D1 |
|---|---|---|---|---|---|
| 펠릿 [109] | 0.307 → 10.6 | 5.8 % | 34.6 [32.3, 37.0] | [0.297, 0.317] | **0.141** [0.132, 0.151] |
| 펠릿 | 0.381 → 6.9 | 4.7 % | 40.5 [38.5, 42.8] | [0.348, 0.427] | **0.133** |
| 펠릿 | 0.546 → 3.35 | 7.9 % | 43.9 [41.2, 46.7] | [0.528, 0.565] | **0.101** |
| 펠릿 | 0.650 → 2.37 | 11 % | 48.2 [43.9, 53.0] | [0.621, 0.683] | **0.093** |
| 펠릿 | 0.718 → 1.94 | 17 % | 39.4 [36.2, 43.1] | — | 0.069 |
| 펠릿 | 0.861 → 1.35 | 28 % | 27.0 [25.0, 29.0] | — | 0.039 |
| 펠릿 | 1.041 → 0.92 | 38 % | 20.4 [17.8, 23.6] | — | 0.025 |
| **이차입자** [107] | **1.208 → 0.685** | — | 상자그림: 수염 **128.3** · 상자 **156.3** · 중앙 **185.6** · 상자 **216.0** · 수염 **289.2** | — | **0.133 · 0.162 · 0.193 · 0.224 · 0.300** |

- **등고선 검증** (derived D2): 파선 경로 기울기 238.8 · 160.0 · 81.0 · 41.5 MPa/µm^−½ ↔ **√(2/π)·K·1000 = 239.4 · 159.6 · 79.8 · 39.9** (K = 0.3 · 0.2 · 0.1 · 0.05).
  ⇒ 그림의 등고선은 본문 식 **σ_F = K_IC/√(π·d/2)** 그대로다.
- 이차입자 가로 위치 1.208 = **(√2 + 1)/2 = 1.207** — 결정립 0.5 · 1 µm 양 끝의 d^−½ 평균 (우리 재구성, D3).
- ★ **리뷰의 "0.05–0.3" 이 어디서 왔나** (우리 판독): **상한 0.3 = 이차입자 윗수염** (정확히 0.300).  하한 0.05 는 기공 17 % 펠릿 (0.069) 과 28 % (0.039) 사이 — 본문이
  *"porosity exceeding 11%"* 를 결정립 추세에서 **뺀다고 말한 그 시료들**이 하한을 정한다.  치밀 펠릿 (≤ 11 %) 만 보면 **0.09–0.14**, 이차입자만 보면 **0.13–0.30 (중앙 0.19)**.
- ⚠ **a = d/2 는 가정이다** — a = d 로 두면 모든 K 가 **×√2 (= 1.41)** 커진다 (중앙 0.19 → 0.27).  즉 "0.05–0.3" 에는 **최소 ×1.4 의 가정 불확도**가 얹혀 있다.

### 3-5. Fig 12 · 13 — 침지 · 탈리튬화 · 사이클 (**vector-read**)

| 그림 | 계열 | 점 (x → 값) | 1차 문헌 |
|---|---|---|---|
| 12A | NMC532 이차입자 건 / 침지 | **E 110 [105, 118] · H 7.56 [6.74, 8.88]** / E 109 [101, 118] · H 7.46 [6.01, 9.74] | [74] (stated) |
| 12A | NMC532 소결 펠릿 건 / 침지 | **E 198 [192, 211] · H 14.3 [13.5, 15.2]** / E 198 [181, 234] · H 14.7 [12.2, 15.7] | [74] |
| 12B · 12C | **NMC532** (파란 마름모) vs x (Li_xMO_y) | x = 1 → **E 145** [135, 155] · **H 8.92** [8.12, 9.72] · 0.835 → 131 · 8.02 · 0.67 → 116 · 7.62 · **0.5 → 112** [106, 119] · **7.11** [6.33, 7.88] | [75] Xu 2017 (식별 — `xu2017` Fig 5a 판독 145.1/131.1/116.0/111.6 · 8.9/8.0/7.65/7.1 과 일치) |
| 12B · 12C | LMO (빨간 원, 두 계열) | x 0.35–0.65: **E 80.6–104 · H 6.51–7.95** (가로 막대 ±0.15–0.25) | [69] · [73] |
| 12B · 12C | LCO 박막 ("Middle" / "Top") | x = 1 에서 E 178 · 163, H 8.3 · 7.5 → x 0.975 급락 → x 0.507: **Middle E 125 · H 5.5 / Top E 89 · H 3.5** | [98] |
| 13A | NMC333 이차입자 (결정립 0.5–1 µm) σ_F | **침지 · 무사이클 (x = 1)**: 수염 107.6 · 상자 134.0 · **중앙 158.9** · 상자 192.2 · 수염 241.8 / **첫 탈리튬화+재리튬화 (x ≈ 0.92)**: 30.0 · 53.8 · **70.3** · 82.5 · 118.0 / **첫 탈리튬화 (x ≈ 0.33)**: 9.4 · 17.1 · **21.5** · 28.2 · 33.8 | [107] (stated) |
| 13B · 13C | **NMC532** vs 사이클 | 0 → **E 146 · H 8.87** · 1 → 125 [112, 139] · 8.08 · 30 → 115 · 7.12 · 50 → 116 · 7.01 · **100 → 108 [94.5, 121] · 6.44** | [75] (식별 — `xu2017` Fig 5b 판독 144.9/125.4/114.5/115.1/107.3 · 8.9/8.1/7.1/7.0/6.5) |
| 13B · 13C | NMC333 박막 | 0 → E 161 [146, 176] · H 7.10 · 10 → 104 · 5.33 · 50 → 82 · 4.01 · **100 → 80 · 3.28** | [71] Zeng & Zhu 2015 |
| 13B · 13C | LMO 박막 | 0 → E 203 · H 10.8 · 10 → 140 · 6.85 · 50 → 143/128/124/93/76 · 6.79/6.57/4.76/4.22 (**C-rate ↑ 일수록 ↓**) · 100 → 113 · 6.82 | [71] |

- ★ **44 % 의 분모는 "침지 후" 다**: 70.3/158.9 = **0.442** (derived D4).  건조 pristine (Fig 10C 중앙 185.6) 을 분모로 하면 **0.379 (38 %)**, 결함 배수 (1/0.379)² = **7.0** (리뷰의 "≈ 5" 는 (1/0.44)² = 5.1).
- ⚠ **"침지해도 불변"** (p. 998) ↔ 리뷰 자신의 두 그림: 중앙 185.6 (Fig 10C) → 158.9 (Fig 13A) = **−14 %** (IQR 156–216 vs 134–192 는 겹친다, derived D5).  "변화가 산포 안" 이지 "불변" 은 아니다.
- 첫 탈리튬화 직후 21.5/158.9 = **0.135** → K 일정이면 결함 **×55**, K 가 Xu 의 SOC100 비율 (×0.57) 만큼 떨어졌다면 **×18** (derived D6, 예시).  리뷰는 이 값을 계산하지 않았다.
- Fig 12B/C 의 NMC532 가로 위치 **1 · 0.835 · 0.67 · 0.5** = **x = 1 − SOC/2** — Xu 2017 의 SOC 0/33/66/100 % 를 **"SOC 100 % = Li₀.₅"** 표기 그대로 옮긴 것 (`xu2017` §8-4 는 실제 Li ≤ 0.41 로 봤다).

### 3-6. Fig 7 — E vs H (log-log), 층상 NMC 6점 **vector-read** (자홍 링 = NMC 영역 외곽선이 그 오차막대를 감싼다)

| H (GPa) [막대] | E (GPa) [막대] | 우리 대조 (식별 / 추정) |
|---|---|---|
| **7.10** [5.84, 8.36] | **161** [146, 176] | NMC333 박막 0 사이클 [71] 과 같은 값 (Fig 13B/C: 161 · 7.10) — 추정 |
| **7.80** (막대 없음) | **113** (막대 없음) | [Sedl26] 이 전한 de Vasconcelos 2019 [74] **113 · 7.8** 과 정확히 같다 — 추정 (2차 대 2차) |
| **8.60** [7.30, 9.90] | **142** [131, 154] | ★ **Xu 2017 이차입자 pristine 8.6 · 142.5** — 식별 |
| **10.40** [9.10, 11.70] | **190** [179, 201] | [미확인] (Cheng 2017 NMC333 [76] 후보 — So 2022 가 옮긴 199 · 11.2 와는 안 맞는다) |
| **12.60** [11.20, 14.00] | **178** [158, 197] | ★ **Xu 2017 소결 펠릿 12.6 · 177.5** — 식별 |
| **13.99** [12.82, 14.16] | **200** (막대 없음) | [74] 펠릿 (Fig 12A 건 198 · 14.3) 과 근접 — 추정 |

- NMC 영역 외곽선의 bbox = **H 5.78–14.58 · E 110–208** (vector) — 위 6점의 오차막대 끝 (5.84 · 14.16 · 113 · 201) 을 감싸도록 그린 **손 그림 영역**이다.
- 다른 재료: LCO (빨강) 8.2/191 · 8.3/178 · 11.7/174 · LMO (주황, 11점) H 6.5–13.5 · E 87–203 · LCP (검정) 9.1/137 · 9.2/106 · 파란 링 1점 8.9/93 (LMO 영역 안, 미식별).
- 공학재료 영역 (Ashby [83, 84]): 알루미나 · 지르코니아 · 질화규소 · 실리콘 · 유리 · 유리세라믹 — **양극재는 유리세라믹 ↔ 지르코니아 사이**.

### 3-7. Fig 4 — 격자상수 (첫 충전, **vector-read**) · NMC811 부피 변화 (derived)

| 계열 (범례) | a/a₀ 최소 | c/c₀ 최대 (x) | c/c₀ 최저 (x) | V/V₀ = (a/a₀)²(c/c₀) — derived D16 |
|---|---|---|---|---|
| **NMC811 (남색 마름모)** | 0.9814 (x 0.15–0.20) | **1.0207** (0.45) | **0.9645** (0.11) | x 0.45 **−1.0 %** · 0.25 −3.4 % · 0.20 **−4.8 %** · 0.15 −6.2 % · **0.11 −7.0 %** |
| NMC811 (연청 사각) — ⚠ C 패널 라벨은 "NMC111" | 0.9860 (0.40) | 1.0211 (0.45) | 1.0035 (0.21, 끝점) | x 0.45 −0.7 % · 0.25 −1.8 % · 0.21 −2.2 % |
| NMC316 (파란 원) | ≈ 0.989 (x ≈ 0.5) | 1.025 (0.44–0.47) | 0.9988 (0.23, 끝점) | — |
| LCO (청록 삼각) | 0.9964 (0.43) · x 0.11 에서 1.0017 | 1.026 (0.40–0.47) | **0.958** (0.11) | — |
| LNMO · LMO (× · +) | — | — | — | 등방 수축 선 위 (Fig 4C) |

- ⚠ **범례의 x = 0.505 · 0.710 점은 범례 마커**다 — 판독에서 뺐다.
- 같은 "NMC811" 두 계열이 **같은 x = 0.25 에서 부피 −1.8 % vs −3.4 %** — 출처·x 보정에 따라 1.6 %p 다르다 (1차 문헌 [37, 42] 어느 쪽인지 리뷰가 안 나눔).
- 우리 A10 의 "격자 −5.1 %" 는 남색 NMC811 의 **x ≈ 0.19** 에 해당 (보간, derived D17) — 충전 깊이가 정해져야 비교가 된다.

### 3-8. ★ 1차 문헌 — 이 카드가 수치를 옮긴 참고문헌 (**참고문헌 목록 원문 그대로**; 아래첨자·기호는 평문)

- [9] Miller, D.J., Proff, C., Wen, J.G., Abraham, D.P., and Bareño, J. (2013). Observation of microstructural evolution in li battery cathode oxide particles by in situ electron microscopy. Adv. Energy Mater. 3, 1098–1103. https://doi.org/10.1002/aenm.201300015.
- [20] Zheng, J., Xiao, J., Yu, X., Kovarik, L., Gu, M., Omenya, F., Chen, X., Yang, X.Q., Liu, J., Graff, G.L., et al. (2012). Enhanced Li+ ion transport in LiNi0.5Mn1.5O4 through control of site disorder. Phys. Chem. Chem. Phys. 14, 13515–13521. https://doi.org/10.1039/c2cp43007j.
- [22] Noh, H.J., Youn, S., Yoon, C.S., and Sun, Y.-K. (2013). Comparison of the structural and electrochemical properties of layered Li[NixCoyMnz]O2 (x = 1/3, 0.5, 0.6, 0.7, 0.8 and 0.85) cathode material for lithium-ion batteries. J. Power Sources 233, 121–130. https://doi.org/10.1016/j.jpowsour.2013.01.063.
- [37] De Biasi, L., Kondrakov, A.O., Geßwein, H., Brezesinski, T., Hartmann, P., and Janek, J. (2017). Between Scylla and Charybdis: balancing among structural stability and energy density of layered NCM cathode materials for advanced lithium-ion batteries. J. Phys. Chem. C 121, 26163–26171. https://doi.org/10.1021/acs.jpcc.7b06363.
- [38] Strauss, F., De Biasi, L., Kim, A.-Y., Hertle, J., Schweidler, S., Janek, J., Hartmann, P., and Brezesinski, T. (2020). Rational design of quasi-zero-strain NCM cathode materials for minimizing volume change effects in all-solid-state batteries. ACS Mater. Lett. 2, 84–88. https://doi.org/10.1021/acsmaterialslett.9b00441.
- [42] Kondrakov, A.O., Geßwein, H., Galdina, K., De Biasi, L., Meded, V., Filatova, E.O., Schumacher, G., Wenzel, W., Hartmann, P., Brezesinski, T., and Janek, J. (2017). Charge-transfer-induced lattice collapse in Ni-rich NCM cathode materials during delithiation. J. Phys. Chem. C 121, 24381–24388. https://doi.org/10.1021/acs.jpcc.7b06598.
- [66] Qu, M., Woodford, W.H., Maloney, J.M., Carter, W.C., Chiang, Y.-M., and Van Vliet, K.J. (2012). Nanomechanical quantification of elastic, plastic, and fracture properties of LiCoO2. Adv. Energy Mater. 2, 940–944. https://doi.org/10.1002/aenm.201200107.
- [67] Mughal, M.Z., Amanieu, H.-Y., Moscatelli, R., and Sebastiani, M. (2017). A comparison of microscale techniques for determining fracture toughness of LiMn2O4 particles. Materials (Basel) 10, 403. https://doi.org/10.3390/ma10040403.
- [68] Wolfenstine, J., Allen, J.L., Jow, T.R., Thompson, T., Sakamoto, J., Jo, H., and Choe, H. (2014). LiCoPO4 mechanical properties evaluated by nanoindentation. Ceram. Int. 40, 13673–13677. https://doi.org/10.1016/j.ceramint.2014.04.122.
- [69] Mughal, M.Z., Moscatelli, R., Amanieu, H.-Y., and Sebastiani, M. (2016). Effect of lithiation on micro-scale fracture toughness of LixMn2O4 cathode. Scr. Mater. 116, 62–66. https://doi.org/10.1016/j.scriptamat.2016.01.023.
- [70] Amanieu, H.-Y., Rosato, D., Sebastiani, M., Massimi, F., and Lupascu, D.C. (2014). Mechanical property measurements of heterogeneous materials by selective nanoindentation: application to LiMn2O4 cathode. Mater. Sci. Eng. A 593, 92–102. https://doi.org/10.1016/j.msea.2013.11.044.
- [71] Zeng, K., and Zhu, J. (2015). Surface morphology, elastic modulus and hardness of thin film cathodes for Li-ion rechargeable batteries. Mech. Mater. 91, 323–332. https://doi.org/10.1016/j.mechmat.2015.05.005.
- [72] McGrogan, F.P., Chiang, Y.-M., and Van Vliet, K.J. (2017). Effect of transition metal substitution on the elastoplastic properties of LiMn2O4 spinel. J. Electroceram. 38, 215–221. https://doi.org/10.1007/s10832-016-0057-7.
- [73] Amanieu, H.-Y., Aramfard, M., Rosato, D., Batista, L., Rabe, U., and Lupascu, D.C. (2015). Mechanical properties of commercial LixMn2O4 cathode under different states of charge. Acta Mater. 89, 153–162. https://doi.org/10.1016/j.actamat.2015.01.074.
- [74] de Vasconcelos, L.S., Sharma, N., Xu, R., and Zhao, K. (2019). In-situ nanoindentation measurement of local mechanical behavior of a Li-ion battery cathode in liquid electrolyte. Exp. Mech. 59, 337–347. https://doi.org/10.1007/s11340-018-00451-6.
- [75] Xu, R., Sun, H., de Vasconcelos, L.S., and Zhao, K. (2017). Mechanical and structural degradation of LiNixMnyCozO2 cathode in Li-ion batteries: an experimental study. J. Electrochem. Soc. 164, A3333–A3341. https://doi.org/10.1149/2.1751713jes.  ← 정본 카드 `xu2017_nmc532_nanoindentation_modulus_hardness_toughness`
- [76] Cheng, E.J., Hong, K., Taylor, N.J., Choe, H., Wolfenstine, J., and Sakamoto, J. (2017). Mechanical and physical properties of LiNi0.33Mn0.33Co0.33O2 (NMC). J. Eur. Ceram. Soc. 37, 3213–3217. https://doi.org/10.1016/j.jeurceramsoc.2017.03.048.
- [77] Cheng, E.J., Taylor, N.J., Wolfenstine, J., and Sakamoto, J. (2017). Elastic properties of lithium cobalt oxide (LiCoO2). J. Asian Ceram. Soc. 5, 113–117. https://doi.org/10.1016/j.jascer.2017.03.001.
- [79] Tabor, D. (1951). The Hardness of Metals (Clarendon Press).
- [82] Oliver, W.C., and Pharr, G.M. (1992). An Improved technique for determining hardness and elastic modulus using load and displacement sensing indentation experiments. J. Mater. Res. 7, 1564–1583. https://doi.org/10.1557/JMR.1992.1564.
- [89] Sakharova, N.A., Fernandes, J.V., Antunes, J.M., and Oliveira, M.C. (2009). Comparison between Berkovich, Vickers and conical indentation tests: a three-dimensional numerical simulation study. Int. J. Solids Struct. 46, 1095–1104. https://doi.org/10.1016/j.ijsolstr.2008.10.032.
- [98] Swallow, J.G., Woodford, W.H., McGrogan, F.P., Ferralis, N., Chiang, Y.-M., and Van Vliet, K.J. (2014). Effect of electrochemical charging on elastoplastic properties and fracture toughness of LixCoO2. J. Electrochem. Soc. 161, F3084–F3090. https://doi.org/10.1149/2.0141411jes.
- [107] Dang, D., Wang, Y., and Cheng, Y.-T. (2019). Communication—fracture behavior of single LiNi0.33Mn0.33Co0.33O2 particles studied by flat punch indentation. J. Electrochem. Soc. 166, A2749–A2751. https://doi.org/10.1149/2.0331913jes.
- [108] Hiramatsu, Y., and Oka, Y. (1966). Determination of the tensile strength of rock by a compression test of an irregular test piece. Int. J. Rock Mech. Min. Sci. Geomech. Abstr. 3, 89–90. https://doi.org/10.1016/0148-9062(66)90002-7.
- [109] Huddleston, W., Dynys, F., and Sehirlioglu, A. (2020). Effects of microstructure on fracture strength and conductivity of sintered NMC333. J. Am. Ceram. Soc. 103, 1527–1535. https://doi.org/10.1111/jace.16829.
- [111] Yoshida, M., Ogiso, H., Nakano, S., and Akedo, J. (2005). Compression test system for a single submicrometer particle. Rev. Sci. Instrum. 76, 093905. https://doi.org/10.1063/1.2038187.
- [114] Orowan, E. (1949). Fracture and strength of solids. Rep. Prog. Phys. 12, 185–232. https://doi.org/10.1088/0034-4885/12/1/309.
- [115] Rice, R.W. (1997). Ceramic tensile strength-grain size relations: grain sizes, slopes, and branch intersections. J. Mater. Sci. 32, 1673–1692. https://doi.org/10.1023/A:1018511613779.
- [116] Ryu, H.-H., Park, K.-J., Yoon, C.S., and Sun, Y.-K. (2018). Capacity fading of Ni-rich Li[NixCoyMn1–x–y]O2 (0.6 ≤ x ≤ 0.95) cathodes for high-energy-density lithium-ion batteries: bulk or surface degradation? Chem. Mater. 30, 1155–1163. https://doi.org/10.1021/acs.chemmater.7b05269.
- [117] Ruess, R., Schweidler, S., Hemmelmann, H., Conforto, G., Bielefeld, A., Weber, D.A., Sann, J., Elm, M.T., and Janek, J. (2020). Influence of NCM particle cracking on kinetics of lithium-ion batteries with liquid or solid electrolyte. J. Electrochem. Soc. 167, 100532. https://doi.org/10.1149/1945-7111/ab9a2c.
- [118] Soroka, I., and Sereda, P.J. (1968). Interrelation of hardness, modulus of elasticity, and porosity in various gypsum systems. J. Am. Ceram. Soc. 51, 337–340. https://doi.org/10.1111/j.1151-2916.1968.tb15949.x.
- [121] Heenan, T.M.M., Wade, A., Tan, C., Parker, J.E., Matras, D., Leach, A.S., Robinson, J.B., Llewellyn, A., Dimitrijevic, A., Jervis, R., et al. (2020). Identifying the origins of microstructural defects such as cracking within Ni-rich NMC811 cathode particles for lithium-ion batteries. Adv. Energy Mater. 10, 2002655. https://doi.org/10.1002/aenm.202002655.
- [122] Phani, K.K., and Niyogi, S.K. (1987). Young's modulus of porous brittle solids. J. Mater. Sci. 22, 257–263. https://doi.org/10.1007/BF01160581.

⚠ **이 리뷰에 없는 것 (전수 확인)**: *"Liu 2020, Nat. Energy 5, 304"* · *"Quinn 2020, Joule 4, 2466"* (우리 K_IC 주석의 옛 출처) — 참고문헌 139편에 **없다**.  "Liu" 는 [14] Liu H. 2014 (*Science*, LFP) 뿐, "Quinn" 은 0건.
*"Wheatcroft 2023"* (NMC811 207 MPa) · *"Sharma 2023"* (NMC811 0.271) — **리뷰보다 나중 논문이라 없다**.  NMC811 의 E · H · K_IC · σ_F **실측값도 없다** (NMC811 은 격자 [37, 42] · 기공 [121] · UCV [116] 에서만).

---

## 4. 방법 ★ (리뷰가 정리한 측정법 + 리뷰 자신의 추정)

### 4-1. 압입 E · H (p. 991–993, Fig 6)
- **식 1**: H = P_I / A_P (P_I 하중, A_P 압흔 **투영** 면적).  소성 영역이 생기면 **H ≈ 3σ_Y** [79] — 팁 기하 의존은 약하다.
- **식 2 (인쇄 그대로)**: *E_R = (1 − ν²)/E + (1 − ν_I²)/E_I* — ⚠ **좌변 역수가 빠진 인쇄 오류** (차원이 안 맞는다; 올바른 식은 1/E_R = …).  *"In terms of the Poisson ration"* (오탈자) 로 이어진다.
- 제하 강성 **S = 2E_R(A_P/π)^½** [82 Oliver–Pharr].  E 는 제하 곡선 초기 기울기에서 [80, 81].
- Berkovich 팁 반경 ≈ 1 µm → 이차입자 단면 (수지에 박아 연마, Fig 6C) · 큰 결정립 한 알 · 소결 펠릿 연마면 (Fig 6D, [76]) 을 잴 수 있다.
- **크기 효과 원인들** [85, 86]: 연마 가공경화 [87] · 산화막 [88] · 팁 끝 둥글림 (식 3 보정 실패) [89].

### 4-2. 다결정 압입의 3단계 (p. 994–996, Fig 8)
- **Stage I** — 압흔 ≪ 결정립: 결정립 안 **전위 소성** (+ 쌍정) [93, 99].  작은 압흔에서 H 만 오르고 E 는 안 오르면 **변형률 구배 (GND) 효과** [100, 101].
- **Stage II** — 소성역이 커져 **압자 근처 입계가 균열** [90, 91].
- **Stage III** — 부서진 결정립의 **입상 유동 (granular flow)** — 임계상태의 입상체처럼 **팽창 (dilatancy)** [95, 96] 이 필요, *"reminiscent of the 'plastic' response of an over-consolidated soil"* [94, 97] — **H 는 입상체의 응집 강도에 비례**.
- **식 3**: A_P = 24.5 d_I² (Berkovich, pile-up 없음) [89].  → A_P^½ 로 크기를 표기 (Fig 9A/B), **A_P^½/d 로 정규화** (Fig 9C/D).
- 큰 결정립에서는 압흔 아래 **방사형 균열**이 결정립 안에서 먼저 생긴다 [66, 104] → 인성 추정 가능 [105, 106].  균열은 유효 E 를 낮춘다 (제하 강성 ↓).

### 4-3. 인장 파괴강도 (p. 996–998, Fig 10 · 11)
- **Brazil-nut (입자 압축)** [107, 108]: 두 판 사이에서 구를 누르면 횡방향 인장 [110] → **식 4 σ_F = 2.8 P_C/(π d_P²)** [108, 111] (P_C 파괴 하중, d_P 입자 지름).
- **이축굽힘 (ring-on-ring)** [109]: 원판을 바깥 링으로 받치고 안쪽 링으로 누름 → 아랫면 중앙 최대 인장 → 탄성해 [112 ASTM C1499].
- 결정립 크기 = ASTM E112 [113].
- ★ **Griffith + 결함 = 결정립 절반**: K_IC = σ_F √(πa) [p. 996], 결함은 결정립 **안** 또는 **입계** (Fig 11B), 길이 ≈ 결정립 [114, 115] → **a = d/2** →
  **σ_F = K_IC/√(π·d/2)** 를 등-K_IC 등고선으로 Fig 10C 에 긋고 자료와 대조 → **0.05–0.3** (리뷰 추정).
- 논리의 짝: 결함이 충분히 작으면 σ_Y ≈ H/3 < σ_F 가 되어 **연성 파괴** (금속) — 양극재는 반대 (σ_F ≪ H/3) = **취성**.

### 4-4. 침지 · 탈리튬화 · 사이클 (p. 998–1001, Fig 12 · 13)
- 침지: NMC532 **1 M LiPF₆ "in polypropylene carbonate"** (인쇄 그대로 — 고분자 PPC 가 아니라 propylene carbonate 로 보인다, [74] 원문 미확인) 속 E·H [74] · NMC333 이차입자 강도 (EC 48 h 등) [107].
- 탈리튬화 E·H vs x [69, 73, 75, 98] · E·H vs 사이클 [71, 75] · σ_F 첫 사이클 [107].
- **주의 문구 둘** (리뷰 자신): UCV 를 과장해 균열을 키우는 연구가 있다 (NMC811 4.8 V vs 실사용 4.2–4.3 V, [116]) · 결과는 **셀 구성 (전/반쪽셀) · 전해질 · 입자 구조**에 민감 — *"single-crystal cathode particles can avoid cracking from differential straining between grains"* · *"Results obtained from the study of polycrystalline layered cathode particles cannot be extrapolated to all cathode materials or particle architectures"* (p. 1000).
- 기공 의존: **H = H₀e^(−αf_P) · E = E₀e^(−βf_P)** [118, 122] — 사이클 중 E·H 의 연속 감소는 이차입자 기공 증가 (NMC811 0.14 → 0.19 / 5 사이클 [121]) 를 시사.

### 4-5. ★ 입자 처리 (우리 DEM 의 "무질서 처리" 대응 항목) — 이 리뷰가 말하는 "입자" 는 무엇인가
- 리뷰의 입자 = **이차입자 (다결정 응집체, 지름 5–20 µm, 결정립 0.1–2 µm)** · **단결정 입자 (구조 대책으로만)** · **판상 · 나노 입자 (LFP)** (Fig 2D–G).
- 역학 해석은 **연속체 파괴역학 + 입상체 소성** 의 혼합이다: 결정립 = 탄성·전위 소성, 입계 = 결함 (a = d/2) · 균열 경로, 큰 압흔 = 부서진 결정립의 **입상 유동**.
  ⇒ 이 리뷰의 "입자" 는 **우리 DEM 구 하나의 안쪽 구조** (결정립 + 입계) 를 다룬다 — `comparison_vs_ours_DEM.md` **§G (sub-particle)** 축.
- **모델 없음**: 리뷰는 수치 모델을 돌리지 않는다.  형상 소성 · 입자 파쇄의 **이론적 틀** (Griffith · 3단계 · 다공 경험식) 만 준다.
- 우리 DEM: AM = **탄성 강체구** (E 140, ν 0.25, 내부 구조 없음) + **사후 Auerbach 파괴 분류** (K_IC_S/P) · 우리 MPM: AM = **동결 scaffold** · `am_load_balance_jam`: AM 크라운이 **H_AM** 으로 하중 분담.
  ⇒ 이 리뷰는 세 입력 (E · K_IC · H) 의 **물리적 의미를 A_P^½/d 로 규정**한다 — 입자 스케일 접촉은 결정립보다 큰 "압흔" 이므로 **stage II–III 부류**에 속할 수 있다 (§7-4).

---

## 5. Figure set ★ (본문 Fig 1–13, 표 0 — **전부 크롭 · 육안 확인 2026-09-26**)

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | (p. 985) Li 이온 셀 모식: 양극 집전체 · 전해질 침윤 양극 (구형 활물질 + 바인더·도전재) · 다공 분리막 · 음극 (판상 흑연) · 음극 집전체 | 액체 LIB 기준 그림 — ASSB 와 달리 **전해질이 기공을 채운다** (우리 SE 입자망과 다름) |
| **2** | (p. 986) (A) 올리빈 (B) 층상 (C) 스피넬 결정구조 (팔면체 전이금속 · Li · 음이온 사면체) · 입자 구조 (D) 이차입자 (1차입자 표시, 1 µm) (E) 분리된 단결정 [11] (F) 판상 (두께 30–60 nm) [12] (G) 나노입자 (50 nm) [13] | ★ (D)↔(E) = 우리 **AM_P ↔ AM_S** 규약의 그림 정의.  DEM 은 (D) 도 (E) 도 **구 하나**로 본다 |
| **3** | (p. 987) (A) 양극재별 Ragone (비출력 vs 비에너지) (B) LFP 입자 구조별 Ragone (C) LFP 비출력 vs 입경 (비에너지 < 350 Wh kg⁻¹; 기울기 −1 등고선) | 기계 논의와 무관 — 입경이 출력의 **유일 변수가 아님** (같은 입경에서 ×50) · 활물질 질량 기준 정규화 주의 |
| **4** | (p. 988; 캡션 p. 989) (A) a/a₀ = b/b₀ vs x (B) c/c₀ vs x (C) c/c₀ vs ab/(a₀b₀) — 등부피선 (빨강 실선) · 등방선 (빨강 일점쇄선).  NMC811 ×2 · NMC316 · LCO · LNMO · LMO, 첫 충전 [37–43] | ★ **층상 = 비등방 (c 먼저 팽창 → x < 0.4 붕괴), 스피넬 = 등방** — 입계 균열의 원인.  NMC811 부피 x 0.11 에서 −7 % (§3-7).  ⚠ 범례 오류 2개 (§8-3) |
| **5** | (p. 991) 이차입자 안 1차입자 (c 축 화살표 방위 제각각) 의 **비등방 변형 → 입계 균열 → 전해질이 채운 균열** 모식 | ★ **액체 전용 그림** — ASSB 에서는 SE 가 균열로 **못 들어간다** → 새 표면 대신 **접촉 상실 · 내부 공극** (우리 A10 `--poly-mode expand-void` 가정과 같은 방향) |
| **6** | (p. 992) (A) Berkovich 압입 모식 (국소 항복역) (B) 하중–변위 (적재 · 제하 · 기울기 S) (C) 수지에 박은 **다결정 이차입자** 압입 (D) **다결정 펠릿** 압입 — **압흔 A_P^½ ↔ 결정립 d 비**를 그림으로 대조 | ★★ **부류 차이의 기하학적 원인**을 한 장에 — 같은 압자라도 이차입자에선 압흔이 결정립 여러 개를, 펠릿에선 한 개 안을 누른다 |
| **7** | (p. 993) **E vs H (log-log)**: LCO (층상, 빨강) · NMC (층상, 초록) · LMO (스피넬, 파랑) · LCP (올리빈, 짙은 회색) 영역 + 알루미나 · 지르코니아 · 질화규소 · 실리콘 · 유리 · 유리세라믹 영역 [83, 84] | ★ NMC 6점 **E 113–200 · H 7.1–14.0** (§3-6) — "stage I" 부류의 **H 하한 ≈ 7** · 우리 E_AM 140 은 NMC 영역 안 · H 밴드 3–6 은 NMC **자료점 (H ≥ 7.1) 아래** (6.0 은 손 그림 영역의 왼쪽 경계 근처) |
| **8** | (p. 994) 다결정 세라믹 압입의 **Stage I (전위 소성, 결정립 안) · II (입계 파괴 · 결정립 간 전단 · wing crack) · III (입상 유동 · 결정립 pile-up)** | ★★ **H 가 "재료 상수" 가 아닌 이유**의 그림.  Stage III = 입자 스케일 접촉의 부류 (우리 H_AM 의 해석 틀, §7-4) |
| **9** | (p. 995) (A) E vs A_P^½ (B) H vs A_P^½ (C) E vs A_P^½/d (D) H vs A_P^½/d — NMC532 (1 µm · 0.1–1 µm 이차입자 / 3–10 µm 펠릿) · NMC333 4.2 µm 펠릿 · LCO 3종 [66, 74–77, 98].  채운 기호 = 이차입자, 빈 기호 = 펠릿 | ★★★ **이 카드의 중심 그림** — (C) 에서 모든 E 가 A_P^½/d 로 접히고 **> 0.1 에서 하락**.  (B)/(D) 의 자홍 계열 = **stage-III H 3.2–5.5 GPa** (우리 3–6 밴드의 짝).  파랑 = Xu 2017 식별 (§3-3) |
| **10** | (p. 997) (A) 입자 압축 (Brazil-nut) 모식 — 횡방향 인장 σ (B) 이축굽힘 (링-온-링) 모식 (C) **σ_F vs d^−½** (NMC333: 펠릿 7점 + 기공 % 라벨, 이차입자 상자그림) + **K_IC = 0.05 · 0.1 · 0.2 · 0.3 등고선** [107, 109] | ★★★ **K_IC 추정 (0.05–0.3) 의 원천** (§3-4).  이차입자 중앙 185.6 MPa = 강도 기준 파쇄 앵커 (NMC333) |
| **11** | (p. 998) (A) 길이 2a 균열이 있는 취성체의 인장 (B) 다결정의 **결정립 안 결함 vs 입계 결함** (결정립 크기급) | Griffith a = d/2 가정의 그림 근거 |
| **12** | (p. 999) (A) NMC532 펠릿 · 이차입자의 **건 vs 침지** E–H [74] (B) E vs x (C) H vs x — NMC532 · LMO · LCO 박막 (중간/표면) [69, 73, 75, 98] (D) H/H₀ vs E/E₀ | 침지 효과 미미 (액체) · **층상은 탈리튬화로 E·H ↓, LMO 는 둔감** · H/H₀ ≈ E/E₀ (미세균열이 둘을 같이 깎는다) |
| **13** | (p. 1001) (A) NMC333 이차입자 σ_F: 침지 후 · 첫 탈리튬화 후 · 첫 사이클 후 (상자그림) [107] (B) E vs 사이클 (C) H vs 사이클 — NMC532 · NMC333 박막 · LMO 박막 (C-rate ↑ 일수록 ↓) [71, 75] (D) H/H₀ vs E/E₀ | 첫 사이클 강도 44 % · 결함 ×5 (리뷰 계산) · **첫 사이클이 최대 계단** — 우리 A10 poly 입계 열화의 **형태** 참고 (크기 전이 금지 — 액체) |

### 5.1 크롭 색인 — `litdb/figures/stallard2022_cathode_mechanical_properties_review/`

자동 크롭 (`tools/litdb/extract_figures.py`, 300 dpi) 12장 → **13장 전부 열어 확인**.  결함: **머리말 ("Joule / Review" 로고 · CellPress 탭) 혼입 7장** (Fig 1 · 5 · 7 · 8 · 9 · 10 · 12),
**패널 A–B 윗부분 잘림 2장** (Fig 3 · 13 — 자동 bbox 가 y 159.2 · 137.5 pt 에서 시작), **누락 1장** (Fig 4 — 캡션이 **다음 쪽** p. 989 에 있고 그림 쪽 p. 988 에는 캡션이 없어 "그래픽 없음" 으로 제외).
⇒ 10장을 **그래픽 경계 (벡터 경로 + 이미지 + 그림 안 글자) 의 합집합 + 여백 3–4 pt** 로 손 클립 → 흰 여백 trim (흰색 = 세 채널 > 244, 여백 8 px).
Fig 8 은 첫 손 클립이 Stage I 표면선 왼끝 (x 62.5 pt, 높이 0 인 선이라 합집합 계산에서 빠짐) 을 ≈ 2 pt 잘라 **다시** 넓혔다.  **표는 없다** (표 크롭 대상 0).

| 파일 | PDF 쪽 | bbox (pt) | px | 처리 | 확인 |
|---|---|---|---|---|---|
| `fig_1.png` | 2 | 55.9, 103.4, 378.9, 390.2 | 1346 × 1195 | 손 재크롭 (머리말 제거) | ✅ 라벨 12개 전부 |
| `fig_2.png` | 3 | 51.7, 97.6, 384.8, 446.0 | 1389 × 1453 | 자동 | ✅ A–G · 범례 3 · 척도 1 µm/30–60 nm/50 nm |
| `fig_3.png` | 4 | 57.3, 103.6, 382.1, 437.7 | 1353 × 1392 | 손 재크롭 (A–B 상단 복원) | ✅ A/B/C · 축 10¹–10⁶ · 범례 |
| `fig_4.png` | 5 | 102.6, 102.9, 330.4, 702.4 | 949 × 2498 | **수동 신규** | ✅ A/B/C · 범례 2 · 등부피/등방선 |
| `fig_5.png` | 8 | 55.7, 101.7, 381.6, 260.5 | 1358 × 662 | 손 재크롭 (머리말 제거) | ✅ "Electrolyte-filled fractures" |
| `fig_6.png` | 9 | 51.7, 98.7, 390.2, 465.0 | 1411 × 1527 | 자동 | ✅ A–D · A_P^½ · d |
| `fig_7.png` | 10 | 56.9, 103.1, 378.5, 402.6 | 1340 × 1248 | 손 재크롭 (머리말 제거) | ✅ 축 E 50–300 · H 3–30 · 영역 라벨 10 |
| `fig_8.png` | 11 | 60.6, 102.8, 543.0, 262.0 | 2010 × 663 | 손 재크롭 ×2 (머리말 "Review" 조각 제거 → 왼끝 복원) | ✅ Stage I–III · 부제 3 |
| `fig_9.png` | 12 | 57.6, 102.9, 381.4, 425.9 | 1349 × 1346 | 손 재크롭 (머리말 제거) | ✅ A–D · 계열 라벨 7 |
| `fig_10.png` | 14 | 56.9, 102.9, 376.6, 537.5 | 1332 × 1811 | 손 재크롭 (머리말 제거) | ✅ A/B/C · 등고선 라벨 4 · 기공 라벨 7 |
| `fig_11.png` | 15 | 51.7, 98.2, 382.5, 295.5 | 1379 × 823 | 자동 | ✅ A/B · 2a · 결함 라벨 2 |
| `fig_12.png` | 16 | 57.6, 102.9, 377.3, 428.6 | 1332 × 1357 | 손 재크롭 (머리말 제거) | ✅ A–D · 범례 Dry/Immersed |
| `fig_13.png` | 18 | 57.1, 103.4, 377.1, 425.9 | 1333 × 1344 | 손 재크롭 (A–B 상단 복원) | ✅ A–D · "NMC333 secondary particles, grain size 0.5 µm to 1 µm." |

⚠ **`--slug stallard2022_cathode_mechanical_properties_review --clean` 을 다시 돌리면 손 크롭 10장이 사라지고** 머리말 섞인 7장 · 잘린 2장 · Fig 4 없음으로 돌아간다
(`figures.json` 의 `recrop` / `manual_crop` 필드 · `pdf_map.tsv` 주석).  `--inbox --run --skip-done` 은 안전.

---

## 6. Post-processing ★ (그들이 한 것 + 우리가 한 것)

### 6-1. 리뷰의 수치화
- **자료 수집**: 저자 기여 문장상 J.C.S. · L.W. · S.G.B. 가 문헌 값을 모았다 — 그림의 점은 **원 논문 그림의 재판독일 수 있다** (방법 미기재).
- **정규화 두 가지**: 크기 → **A_P^½/d** (Fig 9C/D; d = 표기 범위 중앙, 우리 역산) · 열화 → **H/H₀ vs E/E₀** (Fig 12D · 13D, 1 : 1 선 대조).
- **등-K_IC 등고선**: σ_F = K_IC/√(π·d/2) 를 d^−½ 축에 직선으로 (Fig 10C).
- **상자그림**: 이차입자 강도는 상자 (IQR) + 수염 + 중앙 (Fig 10C · 13A; 수염 정의 미기재).
- **결함 성장 배수**: (σ_F,0/σ_F,1)² — K 일정 가정 (p. 1000).
- 플롯: MATLAB 풍 (회색 격자, 로그 축 소눈금 점선), 영역은 손으로 그린 반투명 윤곽 (Fig 7 · Ashby 도표 양식).

### 6-2. 우리 판독 절차 — **PDF 벡터 경로** (재현용)
1. 그림 13장 중 자료 그림 (Fig 4 · 7 · 9 · 10 · 12 · 13) 은 **래스터가 아닌 벡터**다 (그 쪽의 `get_images` 0개).  PyMuPDF `page.get_drawings()` 로 경로를 뽑았다.
2. **축 보정**: 패널마다 흰 축상자 (채움 1,1,1) 와 **격자선 · 눈금 사각형** (채움 0.2 회색) 의 좌표로 선형/로그 사상을 세웠다 — 예: Fig 9A x 0 → 92.11 pt · 3 → 218.24 pt (0.5 간격 21.02 pt, 격자선과 일치), Fig 9C 로그축 10진 38.01 pt (소눈금 0.009 → 110.08 pt 재현).
   Fig 4 는 축상자가 없어 **검은 테두리선 + 1.00 기준선**으로 보정.
3. **마커**: 계열 색 (예: 자홍 0.99, 0.17, 0.99) 의 채움 경로 중 크기 2.5–9 pt 인 것의 bbox 중심 · 겹친 두 경로 (속 빈 기호) 는 0.6 pt 안이면 하나로.
   **오차막대**: 같은 색 **세로 선분** 중 마커 중심을 지나는 가장 긴 것 (가로 막대도 같은 방식).
4. **걸러낸 것**: 범례 안 마커 (Fig 4 의 x = 0.505 · 0.710) · 라벨 화살촉 (검은 작은 삼각형 'relll' 모양) · 등고선 라벨 글리프 (Fig 10C 의 폭 3.9–4.9 pt 검은 채움).
5. **검증**: ① Fig 10C 등고선 기울기가 식과 **±4 %** 안 (파선 조각 bbox 라 끝점 오차) ② 파란 계열이 A_P^½ = √(P/H) 를 **3자리** 재현 ③ Fig 12B/C · 13B/C 의 NMC532 가 `xu2017` 카드의 **래스터 판독과 ±1 GPa · ±0.1 GPa** 안 ④ Fig 13A 비 0.442 가 본문 "44 %" 재현.
   ⇒ **위치 정밀도 ≈ 0.1 pt (축 범위의 ≈ 0.1 %)** — 그러나 그 점들이 1차 논문 값을 얼마나 정확히 옮겼는지는 **모른다** (리뷰 저자의 재판독 가능성).
6. 스크립트는 세션 스크래치에서 돌렸다 (리포에 넣지 않음 — 필요하면 `tools/litdb/` 로 승격).

---

## 7. 우리 DEM+MPM 대비 ★ (기준 = 작업 브랜치 `claude/stoic-knuth-NObVQ` 코드, 2026-09-26 읽기 전용 확인 — `our_dem_baseline.md` 는 아직 자리표시)

| 항목 | 이 리뷰 | 우리 (작업 브랜치 파일:줄) | 같은 점 / 다른 점 / 왜 |
|---|---|---|---|
| **E_AM** | NMC E 는 A_P^½/d 의 함수: 작은 압흔 이차입자 ≈ 110–143, 큰 압흔 (A_P^½/d > 1) ≈ 50–97, 펠릿 166–210 · Fig 7 NMC 113–200 | **140 GPa** (`scripts/dem_input_values.py:47` `E_AM_PA 1.40e11` · `scripts/fracture_model.py:20, 63` · LIGGGHTS `youngsModulus peratomtype 1.4e8 1.4e8 0.135e7` = AM_P · AM_S · SE, 예 `dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts:57` · `dem_scripts/thin6_seed.liggghts:32`) | ✅ **이차입자 · 작은 압흔 부류** (파란 계열 = Xu 2017 첫 점 143).  AM_P 에 대해 [Sedl26] · [Xu17] 판정과 같은 결론.  ⚠ AM_S 는 이 리뷰에도 대응 값 없음 |
| **ν_AM** | **없음** | **0.25** (`dem_input_values.py:48` · `fracture_model.py:21, 64` · LIGGGHTS `poissonsRatio peratomtype 0.25 0.25 0.30`, 예 `in.ps_7_3_r45.liggghts:58` · `thin6_seed.liggghts:33`) | ⛔ 이 리뷰로 방어 불가.  E/(1−ν²) 로 보면 ν 0.25↔0.32 차는 −2.9 % ([Sedl26] D11) — 영향 작음 |
| **K_IC_AM_P** | **0.05–0.3 (리뷰 추정, NMC333 다결정)** · 이차입자 자료 중앙 0.19 (derived) | **0.3** (`fracture_model.py:19, 62`; 주석 *"Quinn 2020"* :43) | ✅ **값은 추정 범위의 상한과 같다** — 라벨을 *"Stallard 2022 추정 범위 (0.05–0.3) 의 상한"* 으로 바꿀 수 있다.  ⚠ 상한 = 가장 강한 입자 (윗수염) 에 맞춘 값 → 우리 파괴 분류는 **덜 깨지는 쪽** |
| **K_IC_AM_S** | NMC 단결정 **없음** · LCO 큰 결정립 0.2–6.5 (방위 의존) [66] | **1.0** (`fracture_model.py:18, 61`; 주석 *"Liu 2020"* :42) | ⚠ **방향 (입내 ≫ 입계) 만 정성 지지**, 값 근거 없음.  σ_F 186 MPa 에서 K 1.0 은 결함 반길이 **9.2 µm** (입자 크기급) 를 요구 (derived D15) — PC 입자 강도로는 성립 안 함, SC 강도 자료 필요 |
| **H_AM (DEM 파괴 · Tabor)** | 작은 압흔 NMC 7.1–14.0 · stage III 3.2–5.5 | **6.0 GPa** (`fracture_model.py:22, 65` "informational" · `scripts/analyze_tabor_regime.py:79-81` σ_y,AM = H/3 = 2.0 GPa) | ⚠ 두 부류 사이 무소속.  ⚠ **H/3 는 압축 소성의 대용**이다 — 리뷰는 인장강도가 H/3 보다 **10× 이상 낮다**고 강조 (NMC 는 인장에서 "항복" 하지 않고 깨진다) |
| **H_AM (하중분담 · MPM ②)** | stage III (압흔 ≥ 결정립) NMC532 이차입자 **3.2–5.5** | 기본 **4.0** · 사전등록 밴드 **(3.0, 6.0)** (`scripts/am_load_balance_jam.py:28` 주석 · `:323` `scan_h_am(band=(3.0, 6.0))` · `:391` `run_cases(band=(3.0, 6.0))`) · 역산 **3.85** (`docs/am_load_balance_and_se_curve_20260805.md:40` "문헌대 3–6 안 ✓") | ⚠ **사후 부합 (post hoc)** — 등록 당시 출처가 없었다.  이 리뷰로 밴드를 *"stage-III 압입 경도 부류"* 로 **다시 등록**하면 앞으로는 출처 있는 판정선이 된다 (§7-4).  한정어: NMC532 · 단일 계열 · 포화 안 함 |
| **입자 파쇄 기준 (강도)** | NMC333 이차입자 σ_F 중앙 186 MPa (건) · 159 (침지) · 21.5 (첫 탈리튬화) · 70 (첫 사이클) · 식 4 | 없음 — 파괴는 **Auerbach 원뿔균열 개시** P_c = A·K²·R/E\* (`fracture_model.py`) 사후 분류 | 층이 다르다: Auerbach = **균열 개시**, Brazil-nut = **입자 쪼개짐**.  d 5 µm 입자의 쪼개짐 하중 **5.2 mN** vs Auerbach 개시 (K 0.3) **0.60 mN** → 8.6× (derived D14, 예시) |
| **입자 내부 기공** | NMC811 이차입자 **0.14 → 0.19** (5 사이클) [121] | DEM 구 = **치밀체**, ε_sphere 에 입자 내부 기공 없음 | ⚠ 실험 기공률 (진밀도 기준) 과 대조할 때 **입자 내부 기공 몫이 우리 쪽에서 빠진다** — 크기는 AM 부피분율 × 0.14 급 (확인 필요, §9-5) |
| **전해질** | **액체** 전용 (침지 · Fig 5 전해질 채운 균열) | **황화물 LPSCl ASSB** | ⛔ 침지 · 사이클 열화 **크기** 전이 금지.  건식 기계물성 (E · H · σ_F · K) 은 전해질 무관이라 넘어온다 |
| **격자 변화** | NMC811 V/V₀ x 0.11 에서 −7.0 % (derived) · 두 데이터셋 1.6 %p 차 | A10 `cycle_contact_ledger` 격자 −5.1 % | 충전 깊이 x 를 맞춰야 비교 가능 (−5.1 % ≈ x 0.19) |

### 7-1. E_AM = 140 — **정합 · 라벨만**
- 이 리뷰의 요점은 **"NMC 의 E" 가 하나가 아니다**는 것 — 같은 NMC532 가 압흔/결정립 비에 따라 **210 → 50 GPa** 를 오간다 (Fig 9C).
- 우리 140 은 파란 계열 (Xu 2017) 의 **1–2 mN 점 (143 · 141, A_P^½/d 0.34–0.45)** = "이차입자 응집체 · 작은 압흔" 값이다.  [Sedl26] 의 138 ± 24 (5 mN · 150 nm) 도 같은 칸.
- ⚠ **DEM AM–AM 접촉의 "압흔 크기"**: 헤르츠 접촉 반경 a = (3FR\*/4E\*)^⅓ (R\* 2.5 µm, E\* 74.7 GPa) 은 F = 0.1 · 1 · 10 mN 에서 **0.14 · 0.29 · 0.63 µm**,
  √π·a = 0.24 · 0.52 · 1.12 µm (derived D13) → 결정립 0.5–1 µm 대비 **A_P^½/d ≈ 0.25–2** — 리뷰 틀로는 stage I–III 에 걸친다.
  즉 **큰 힘의 AM–AM 접촉일수록 유효 E 가 140 보다 낮을 수 있다** (Fig 9C: A_P^½/d ≈ 1 에서 ≈ 100).  ⚠ 헤르츠 (둥근 탄성 접촉) 와 Berkovich (날카로운 소성 압입) 는 **응력장이 다르다** — 스케일 비교용 산술이지 기전 전이가 아니다.
- 영향 범위: AM–SE 접촉 E\* 는 연화 SE (1.35 GPa) 가 지배해 AM 값에 **0.03 %** 만 민감 ([Sedl26] D12) ⇒ 압밀·수송 결과는 안 움직인다.  남는 것은 **AM–AM 힘사슬 · Auerbach P_c** (∝ 1/E\*).

### 7-2. ν_AM = 0.25 — **이 리뷰는 아무것도 주지 않는다**
- ν 는 식 2 의 기호로만 나온다.  그러니 "Stallard 2022" 를 ν 의 출처로 **달 수 없다**.
- 유일한 단서는 다른 카드: `so2022_dem_compaction_coated_particles_assb` §3 이 **So 2022 Table 1 의 ν_AM 0.25 ← Cheng [37]** 을 기록 — 그 Cheng 이 이 리뷰의 [76] Cheng 2017
  (*J. Eur. Ceram. Soc.* 37, 3213, NMC333 열간가압) 과 같은 논문인지는 **[미확인]** (so2022 카드에 [37] 서지 원문이 없다).  ⇒ **Cheng 2017 원문 digest 가 다음 후보**.

### 7-3. K_IC — **"Stallard 추정" 의 실체와 우리 두 값**
- **추정 방법** (원문 그대로 요약): 결함 길이 ≈ 결정립 크기 [114, 115] → **a = d/2** → σ_F = K_IC/√(πa) 등고선 (K_IC 0.05 · 0.1 · 0.2 · 0.3) 을 NMC333 강도 자료 (펠릿 [109] + 이차입자 [107]) 위에 그어
  *"implies a fracture toughness K_IC between 0.05 and 0.3 MPa m^1/2"* (p. 997–998).  **측정이 아니라 강도 자료 + 결함 가정에서 역산한 범위**다.
- [Sedl26] 의 *"0.271 MPa√m … in good agreement with an estimation made by Stallard et al."* = 0.271 이 이 **0.05–0.3 범위 안 (상단)** 이라는 뜻이다 — 이 리뷰가 0.271 에 가까운 **점 추정**을 낸 것은 아니다.
- **K_IC_AM_P 0.3**: 범위의 **상한** = 이차입자 윗수염 (derived: 289.2 MPa → 0.300).  이차입자 자료의 **중앙 0.19**, 치밀 펠릿 0.09–0.14, Xu pop-in 0.10 (NMC532).
  ⇒ "0.3 은 가장 강한 입자에 맞춘 값" — 파괴 분류가 **덜 깨지는 쪽**으로 치우칠 수 있다.  Auerbach P_c ∝ K² 이라 0.19 이면 P_c ×0.40, 0.10 이면 ×0.11.
  ⚠ 바꾸면 `fracture_aware_excluded_pct` (σ_ionic T1 β_F) · `frac_severe_force_pct` (σ_e 22.5 β_Fe) 가 흔들린다 → **분류 재실행 + 폼 재적합** = 1저자 결정 (`xu2017` §7-3 과 같은 경고).
- **K_IC_AM_S 1.0**: NMC 단결정 값은 이 리뷰에 **없다**.  LCO 큰 결정립 0.2–6.5 가 1.0 을 **걸칠 뿐** (재료 다름 · 32배 폭).  리뷰의 정성 논거 *"The fact that the intergranular toughness is much below the transgranular toughness explains the observation that an intergranular fracture is observed upon cell charging"* 는 **K_S > K_P 의 방향**만 지지한다.
- 옛 주석 *"Quinn 2020 Joule 4, 2466"* 을 이 리뷰 (*Joule* 6, 984) 로 **"고쳐 다는"** 것은 안 된다 — 이 리뷰는 0.3 을 **상한으로만** 주고, 1.0 은 주지 않는다.  라벨은 *"Stallard 2022 추정 범위 0.05–0.3 (NMC333, a = d/2 가정) 의 상한"* 처럼 **추정·가정·재료**를 함께 적을 것.

### 7-4. H_AM — **"3–6 GPa" 에 처음 생긴 짝, 그리고 그 짝이 무엇을 뜻하나**
- 지금까지 [Sedl26] · [Xu17] 카드는 *"문헌 NMC 경도 7.8–14.2 가 3–6 과 하나도 안 겹친다"* 로 판정했다 — 그 판정은 **작은 압흔 (stage I) 값**에 대해서는 이 리뷰로도 그대로다 (Fig 7 NMC 7.1–14.0).
- 이 리뷰가 새로 보이는 것: **같은 NMC532 이차입자**라도 압흔이 결정립보다 커지면 (A_P^½/d > 1) H 가 **5.5 → 3.2 GPa** 로 내려간다 (Fig 9B/D 자홍) — **stage III 입상 유동의 응집 강도**.
  우리 역산 **3.83–3.85** 는 그 곡선의 **A_P^½ ≈ 1.72 µm (A_P^½/d ≈ 3.1)** 점과 같다 (derived D11).
- **물리적 해석 (우리)**: `am_load_balance_jam` 의 H_AM = *"AM 크라운이 버티는 접촉 평균압"* — 플래튼–AM 접촉 패치는 결정립 (0.1–1 µm) 보다 크므로 **stage III 부류가 맞는 부류**다.
  [Sedl26] §7.5 가 추측으로 남겨 둔 *"입자 스케일 유효 지지압 (입계 파쇄 포함)"* 해석에 **처음으로 문헌 자료점이 붙은 것**이다.
- ⚠ **그러나 이것은 사후 부합이다** — 사전등록 (`am_load_balance_jam.py:28` · `:323` · `:391`) 당시 밴드에는 출처가 없었다.  규율상:
  ① 과거의 *"역산값 = 문헌대 안 ✓"* 를 **소급 정당화로 쓰지 않는다**.  ② 밴드를 쓰려면 **런 전에** *"stage-III (A_P^½/d ≳ 1) 압입 경도, NMC532 이차입자 3.2–5.5 GPa (Stallard 2022 Fig 9B, vector-read; 1차 출처 미표기)"* 로 **재등록**한다.
  ③ 한정어: **NMC532** (811 아님) · **단일 계열** · **2.6 µm 까지 포화 없음** (기울기 −0.36 — 더 큰 접촉이면 더 낮을 수 있다) · 1차 출처 [74] **추정**.
- 그 모듈 자신의 기록대로 두께 검정은 H_AM 0.5–40 GPa 에서 전부 PASS (**VACUOUS**) — 수치 결과는 안 움직이고 **논거 층**만 바뀐다.  이 H_AM 은 CLAUDE.md 의 **AM 하중분담 ② (유일 병목)** 에 걸린 양이므로, 문헌 부류를 바로 세워 두는 것 자체가 ② 의 전제 정리다 (값 교체는 1저자 결정).
- `fracture_model.py` 의 **6.0** 은 stage I 하한 (≈ 7) 과 stage III 상한 (≈ 5.5) 사이 — **어느 부류에도 안 속한다** ⇒ "informational · 근거 없음" 라벨 유지.

### 7-5. 강도 앵커 — **NMC333 은 있다, NMC811 은 원문이 필요하다**
- 이 리뷰의 강도 자료는 **전부 NMC333** (Dang 2019 이차입자 · Huddleston 2020 펠릿).  NMC811 207 MPa (Wheatcroft 2023) 는 **리뷰보다 뒤** — [Sedl26] 의 2차 인용으로만 안다.
- 강도 기준 입자 파쇄를 DEM 에 넣는다면 필요한 양은 **입자 단위 σ_F** 이고, 이 리뷰의 틀로는 **σ_F 가 결정립 크기 (∝ d^−½) · 이력 (첫 사이클 ×0.44) · 기공**에 따라 움직인다 — 상수 하나로 두면 안 된다.
- ⚠ Brazil-nut 식 (2.8 인자) 은 **불규칙 암석 조각**에서 나온 근사다 [108] — 구형 이차입자에서 응력 상태 · 접촉 조건이 다르면 인자가 바뀐다 (리뷰는 논의 안 함).

### 7-6. frame [5] 로 본 자리
- 이 리뷰는 **DEM 도 MPM 도 아니다** — 우리 두 모델의 **AM 재료 입력의 해석 틀**이다.
  · DEM 쪽: E_AM · ν_AM (압밀엔 영향 작음) · **K_IC (파괴 분류에 큼)** · 강도 (미래의 입자 파쇄 기준).
  · MPM 쪽: AM 은 동결 scaffold 라 E 를 안 쓰지만, **AM 하중분담 ② 의 H_AM** 이 이 리뷰의 stage-III 부류와 만난다.
- **가진 반쪽**: 입자 **안** (결정립 · 입계 · 결함) 의 역학 틀.  **없는 반쪽**: 입자들이 모인 **전극** (접촉망 · 압밀 · 수송) — 전부 우리 쪽.  게다가 **고체전해질 맥락 0**.
- 이 리뷰의 3단계 (전위 소성 → 입계 균열 → 입상 유동) 는 우리 frame [2] 의 *"DEM 18× 연화 = 재배열 · 입계 미끄럼 · 미세파괴의 lumping"* 과 **같은 기전 목록**을 한 입자 안에서 말한다 — 스케일이 한 칸 아래일 뿐이다.

---

## 8. ★★ 비판적 검토 — 원고에 옮기기 전 확인할 것

1. **새 1차 값 0** — 모든 수치가 2차 인용 · 대부분 그림 속 값.  원고에는 **1차 논문** (Xu 2017 · Dang 2019 · Huddleston 2020 …) 을 인용하고, 이 리뷰는 **틀 (A_P^½/d · a = d/2 추정)** 에만 인용할 것.
2. **계열 ↔ 문헌 대응 미표기** — Fig 7 · 9 캡션이 [66–77] · [66, 74–77, 98] 을 **묶어서** 단다.  우리가 식별한 것은 파란 계열 (Xu 2017) 과 Fig 7 의 두 점뿐, 나머지는 정황 추정.
3. **그림·범례 오류** (우리 확인):
   - Fig 4A/B 범례가 **LCO 를 "Spinels" 괄호로 묶었다** — 본문 p. 986 은 LCO 를 층상으로 분류.
   - 연청 사각 계열이 **A/B 범례 "NMC811" ↔ C 패널 라벨 "NMC111"** — 같은 자료 (ab 최소 0.972 · c 최대 1.021 이 일치) 에 두 이름.  "NMC811" 이 **두 번** 나온다 (서로 다른 연구 [37, 42] 추정).
   - 본문 상호참조 오류 **4곳**: *"contours of constant KIC in Figure 8C"* · *"(see Figure 8C)"* (p. 997–998) → **Fig 10C** · *"see the plot of H/H0 versus E/E0 in Figure 12D"* (사이클, p. 1000) → **Fig 13D** · *"(see Figures 12B and 12C)"* (사이클 수, p. 1001) → **Fig 13B/C**.
   - **식 2 좌변 역수 누락** (E_R = … 로 인쇄) · *"Poisson ration"* 오탈자 (p. 992) · Fig 9 캡션은 A_I^½, 본문은 A_P^½.
   - *"1 M LiPF6, in polypropylene carbonate"* (p. 998) — 고분자 PPC 로 읽히는 표기 (propylene carbonate 의 오기 추정, [74] 원문 미확인).
4. **K_IC 추정의 가정 의존** — ① a = d/2 (a = d 면 ×1.41) ② Hiramatsu–Oka 2.8 인자 (불규칙 조각용 근사) ③ 펠릿 (이축굽힘, 다공) 과 입자 (압축) 를 한 판에 ④ 하한 0.05 는 본문이 추세에서 **제외한** 고기공 펠릿이 정한다.
   ⇒ "0.05–0.3" 을 **측정 인성처럼** 인용하지 말 것 — *"strength-derived estimate assuming flaw = half grain size"* 한정어 필수.
5. **"침지해도 불변" 의 과장** — 리뷰 자신의 두 그림 사이 중앙값 **−14 %** (185.6 → 158.9).  IQR 겹침이라 *"산포 안"* 이 정확한 표현.  그리고 **44 % 의 분모는 침지 후 값** (건조 pristine 기준이면 38 %).
6. **SOC 축의 상속 오류** — Fig 12B/C 의 NMC532 x = 0.5 는 Xu 2017 의 **표기** "Li₀.₅" (`xu2017` §8-4: 4.3 V 충전 Li ≤ 0.41) 를 그대로 쓴 것.
7. **정규화 d 의 임의성** — 범위의 중앙 (0.55 · 6.5 µm) · "> 100" → 100.  로그축 위치가 ×2 까지 움직일 수 있다 — 9C/D 의 "한 곡선으로 모인다" 는 이 선택에 기댄다.
8. **H 계열 없음 구간** — 자홍 (이차입자 0.1–1 µm) 의 H 는 A_P^½ < 0.59 µm 에서 **그려지지 않았다** (E 는 0.14 부터).  작은 압흔 H (≈ 7.8, [Sedl26] 경유) 와의 연결이 그림에 없다.
9. **액체 LIB 전용** — 침지 · 사이클 · Fig 5 (전해질 채운 균열) 모두 액체.  황화물 ASSB 에서는 균열이 **공극**으로 남는다 (기전이 다르다).
10. **NMC811 역학값 0** — 우리 생산 조성 (NCM811) 에 대해서는 격자 · 기공 · UCV 만 준다.

---

## 9. 적용 인사이트 — 우리 연구에 어떻게

1. **E_AM 인용 문장에 "부류 + 크기" 를 적는다** — *"140 GPa lies in the secondary-particle (aggregate) class at small indentation size (A_P^1/2/d ≈ 0.3–0.5), cf. 142.5 ± 11.3 GPa [Xu 2017]; E decreases for A_P^1/2/d > 0.1 because of grain-boundary fragmentation [Stallard 2022]"*.  재계산 0.
2. **K_IC_AM_P 는 라벨 교체 + 민감도 팔 등록** — 라벨: *"upper bound of the strength-derived estimate 0.05–0.3 MPa m^1/2 for polycrystalline NMC333 (a = d/2) [Stallard 2022]"*.
   팔: **{0.10 (Xu pop-in) · 0.19 (리뷰 자료 중앙) · 0.30 (생산)}** — `fracture_aware_excluded_pct` 가 얼마나 움직이는지 먼저 본다 (같은 코퍼스 · 같은 분류기).  생산값 교체는 1저자 결정.
3. **H_AM 밴드를 "stage-III 부류" 로 재등록** — 런 전에 문구와 출처를 바꾼다: *"3.2–5.5 GPa: Berkovich hardness of NMC532 secondary particles at indent sizes ≥ grain size (stage III granular flow), Stallard 2022 Fig 9B (vector-read), primary source unlabelled"*.
   과거 PASS 는 **출처 없는 판정선의 결과**로 기록을 남긴다 (소급 정당화 금지).
4. **입자 파쇄를 강도 기준으로 넣을 때의 식과 값** — P_C(d) = σ_F π d²/2.8 → NMC333 중앙 185.6 MPa 면 **0.208 mN × (d/µm)²** (d 5 µm → 5.2 mN, 10 µm → 20.8 mN; derived D14).
   Auerbach 개시 (K 0.3, R 2.5 µm) 0.60 mN 과 **한 자릿수 차** — 두 기준은 **다른 사건** (개시 vs 쪼개짐) 이라 둘 다 필요할 수 있다.  NMC811 값은 Wheatcroft 2023 원문 후.
5. **(질문) 실험 기공률 대조에 입자 내부 기공이 빠져 있지 않은가** — 이 리뷰가 옮긴 NMC811 이차입자 기공 **0.14** (pristine, [121]) 가 진밀도 기준 실험 기공률에 들어간다면,
   치밀 구로 세는 우리 ε_sphere 는 그 몫 (AM 외피 부피분율 × 0.14) 만큼 **낮게** 나온다.  우리 AM 밀도·부피 환산 규약에 따라 이미 흡수됐을 수도 있다 — **확인 필요** (주장 아님).
6. **A10 사이클 모델의 "형태" 앵커** — 첫 사이클 강도 −56 % (침지 기준) · E·H 의 첫 사이클 계단 · H/H₀ ≈ E/E₀ 동행.  ⚠ 크기는 액체 · NMC333/532 라 **옮기지 않는다**.  UCV 주의 (4.8 V 자료 배제).
7. **격자 부피는 충전 깊이와 함께** — NMC811 −7.0 % @ x 0.11 · −4.8 % @ 0.20 (derived, 한 데이터셋).  우리 −5.1 % 를 인용할 때 **x 를 병기**.
8. **frame [2] 의 기전 목록에 한 칸 아래 근거** — "재배열 · 입계 미끄럼 · 미세파괴" 가 SE 분말에서 연화 E 로 lumping 되듯, NMC 한 입자 안에서도 **입계 파쇄가 E·H 를 깎는다** (A_P^½/d > 0.1).  원고 서술에서 *"AM = 강체"* 가정의 한계 문장으로 쓸 수 있다.

---

## 10. 한계

### 10-1. 저자가 밝힌 것
- 기계 연구가 **UCV 를 과장**하는 경향 (NMC811 4.8 V vs 4.2–4.3 V) — 실사용 거동을 대표하지 않을 수 있다.
- 결과는 **전기화학 조건 (UCV · 전/반쪽셀 · 전해질)** 과 **입자 구조**에 민감 — 다결정 층상 결과를 **모든 재료·구조로 외삽하지 말 것**.
- 액체 전해질 비율이 큰 전극은 셀 수준 출력·에너지가 활물질 기준보다 낮다 (Ragone 정규화 주의).

### 10-2. 우리가 추가하는 것
- **2차 인용 · 그림 속 값 · 계열-문헌 미대응** (§8-1, 8-2).
- **NMC811 역학값 없음 · 단결정 NMC 없음 · DFT 없음 · ν 없음 · 황화물 ASSB 없음**.
- **K_IC 는 추정** (가정 2개에 ×1.4 이상 민감).
- **크기 의존 값의 "대표값" 은 없다** — H·E 는 A_P^½/d 를 적지 않으면 의미가 없다.
- SI 없음 · 자료 공개 없음.

---

## 11. 논증 흐름 (절별)

1. **서론 (p. 984–988)** — 셀 구조 (Fig 1) · 양극재 3계열 (올리빈 · 층상 · 스피넬, Fig 2A–C) · 입자 구조 (이차입자 · 단결정 · 판상 · 나노, Fig 2D–G) · Ragone (Fig 3): 입경만으로 출력이 안 정해진다.
2. **격자 변화 (p. 989–990)** — operando XRD 자료 [37–43] (Fig 4): 층상 = 비등방 (c 팽창 후 x < 0.4 붕괴), LCO = 두 상 → x 0.5 단사 전이, 스피넬 = 등방 · 상전이 계단.
3. **화학-기계 열화 (p. 990–991)** — 용량 손실 3기전 (부동태층 · 활물질 손실 · 균열) · 계산상 응력이 파괴에 충분 [56–58] · 다결정의 **비등방 변형 → 입계 균열 → 전해질 침투** (Fig 5).
4. **건식 E · H · σ_F (p. 991–998)** — 압입법 (식 1–3, Fig 6) · 양극재 E·H 지도 (Fig 7, 세라믹과 같은 영역) · **3단계 크기 효과** (Fig 8) · **A_P^½/d 로 자료 접힘** (Fig 9) ·
   강도 시험 (식 4, Fig 10A/B) · **σ_F ∝ d^−½ 와 K_IC 0.05–0.3 추정** (Fig 10C · 11) · 입계 인성 ≪ 입내 인성 (LCO 0.2–6.5) → 충전 시 입계 파괴.
5. **침지 · 탈리튬화 · 사이클 (p. 998–1001)** — 침지 영향 미미 (Fig 12A) · 층상은 탈리튬화로 E·H ↓, LMO 둔감 (Fig 12B/C) · LCO 초기 급락은 **상분리 기원 가능** · H/H₀ ≈ E/E₀ (Fig 12D) ·
   첫 사이클 강도 44 %, 결함 ×5 (Fig 13A) · 사이클 E·H 감소, C-rate 의존 (Fig 13B/C) · 기공 경험식 · NMC811 기공 0.14 → 0.19.
6. **완화 전략 (p. 1001–1002)** — ① 변형 억제 (전압 창 · 조성 · 도핑) ② 코어-셸/농도구배 ③ **1차입자 미세화** (결함 크기 ↓) ④ 결정립 방위 정렬 ⑤ **단결정** ⑥ 이차입자 크기 ↓ (확산 거리).
7. **결론 (p. 1002–1003)** — E·H 는 압흔/결정립 비에 민감 (입계 균열) · 입자 인장강도는 H 보다 한 자릿수 이상 낮음 (기존 입계 균열) · σ_F ∝ d^−½ · 층상의 비등방 변형이 첫 충전 입계 파쇄를 설명 · 미세균열이 E·H 를 같이 깎는다 · 대책은 균열 원인 (빠른 충전 vs 비등방 팽창) 에 따라 고른다.

---

## 12. 기법 미니 용어집

| 용어 | 뜻 | 이 리뷰에서 |
|---|---|---|
| **A_P · A_P^½** | 압흔 **투영** 면적과 그 제곱근 (길이 척도) | Berkovich A_P = 24.5 d_I² (식 3) |
| **A_P^½/d** | 압흔 크기 ÷ 결정립 크기 — 압자가 결정립 몇 개를 누르나 | < 0.1 E 불변 · > 0.1 입계 파쇄로 E·H ↓ (Fig 9C/D) |
| **Stage I / II / III** | 결정립 안 전위 소성 / 압자 근처 입계 균열 / 부서진 결정립의 입상 유동 | Fig 8 · p. 994 |
| **입상 유동 (granular flow) · dilatancy** | 부서진 알갱이가 서로 미끄러지며 흐를 때 부피가 늘어나는 성질 | Stage III 의 H = 입상체 응집 강도 [94–97] |
| **GND · 변형률 구배 소성** | 작은 압흔일수록 기하학적으로 필요한 전위가 많아 H 만 오르는 효과 | Stage I 크기 효과 [100, 101] |
| **환산탄성률 E_R** | 1/E_R = (1−ν²)/E + (1−ν_I²)/E_I (시료 + 압자 직렬) | 식 2 (⚠ 인쇄본은 역수 누락) |
| **Tabor 관계 H ≈ 3σ_Y** | 완전 소성 압입에서 경도 ≈ 항복응력의 3배 | [79] · 인장강도는 이보다 10× 이상 낮다 |
| **Brazil-nut 시험** | 입자를 두 판으로 눌러 횡방향 인장으로 쪼갬 | σ_F = 2.8 P_C/(π d_P²) (식 4, Hiramatsu–Oka) |
| **이축굽힘 (ring-on-ring)** | 원판을 두 동심 링으로 굽혀 아랫면 중앙 인장 최대 | 펠릿 강도 [109] · ASTM C1499 [112] |
| **Griffith 관계** | K_IC = σ_F √(πa) — 기존 결함 a 에서 빠른 파괴 | a = d/2 로 K_IC 추정 (Fig 10C) |
| **입계 / 입내 파괴** | 균열이 결정립 경계를 / 결정립을 가로질러 | 다결정 NMC 는 입계 (낮은 K) · LCO 입내 0.2–6.5 |
| **등-K_IC 등고선** | 같은 K 를 σ_F–d^−½ 평면의 원점 직선으로 | 기울기 √(2/π)·K |
| **다공 경험식** | H = H₀e^(−αf_P) · E = E₀e^(−βf_P) | α, β = 입계 강도 · 맞물림에 민감 [118, 122] |
| **UCV** | 충전 상한 전압 | 4.8 V 과장 연구 주의 (4.2–4.3 V 실사용) |
| **Ashby 도표** | 재료 부류를 물성 쌍 평면의 영역으로 | Fig 7 (E–H) |

---

## 13. 인용 가능 문장 (deck / 원고용)

- **K_IC (SELF-51 라벨)**:
  *"Stallard et al. estimated K_IC ≈ 0.05–0.3 MPa m^1/2 for fully lithiated polycrystalline NMC333 by comparing particle-compression and biaxial-flexure strengths with σ_F = K_IC/(π d/2)^1/2, i.e. assuming a flaw size of half the grain size (Joule 6, 984 (2022)); our K_IC,AM_P = 0.3 MPa m^1/2 corresponds to the upper bound of that estimate."*
- **크기 효과 (원고 한계 서술)**:
  *"Nanoindentation modulus and hardness of NMC secondary particles decrease once the indent exceeds about one tenth of the primary-grain size, owing to grain-boundary fragmentation (Stallard et al., Joule 2022); single-valued E and H for NMC are therefore meaningful only together with the indent-size-to-grain-size ratio."*
- **강도 ≪ 경도**:
  *"The tensile strength of NMC secondary particles (median ≈ 186 MPa for NMC333, as re-plotted by Stallard et al.) is more than an order of magnitude below H/3, so the particles fail by brittle fracture from grain-size flaws rather than by yielding."*  (⚠ 186 은 Fig 10C 상자그림의 vector-read 값 — "≈" 필수, 1차 출처 Dang 2019 를 함께 적을 것)
- 한국어: *"NMC 이차입자의 E·H 는 압흔 크기가 결정립 크기의 약 1/10 을 넘으면 입계 파쇄로 함께 낮아진다 (Stallard 2022). 따라서 NMC 의 E·H 는 압흔/결정립 비와 함께 적어야 의미가 있다."*
- ⛔ **쓰면 안 되는 문장**: *"K_IC = 0.3 MPa m^1/2 (Stallard 2022, measured)"* (측정 아님 · 상한) · *"K_IC,single crystal = 1.0 (Stallard 2022)"* (없음) · *"ν = 0.25 (Stallard 2022)"* (없음) ·
  *"H_NCM811 = 3–6 GPa (Stallard 2022)"* (NMC532 · stage III · 그림 판독) · *"electrolyte immersion does not change the fracture strength"* 를 황화물 ASSB 근거로 · 그림 판독값을 stated 처럼.

---

## 14. 관련 카드 (litdb 내부 교차참조)

- ★ `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` — **[75] 의 원문**.  이 리뷰 Fig 9 파란 계열 · Fig 7 의 두 점 · Fig 12B/C · 13B/C 의 NMC532 = 그 논문 (우리 식별).
- ★ `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` — 이 리뷰를 [30] 으로 인용 (*"good agreement with an estimation made by Stallard et al."*) · NMC811 강도·E · Sharma/Wheatcroft/Dang/de Vasconcelos 의 2차 인용 목록.
- `so2022_dem_compaction_coated_particles_assb` — So 2022 Table 1: E_AM 199 · H_AM 11.2 · **ν_AM 0.25 ← Cheng [37]** (ν 출처 포인터, §7-2).
- `jung2023_single_crystal_ncm_morphology` — SC vs PC 입자 압축 (다른 양 — 피크 압축응력).
- `trevisanello2021_sc_pc_ncm_cracking_diffusion` — SC/PC 균열 · 액체 침투 (이 리뷰 Fig 5 의 액체 전제와 같은 계열).
- `kang2025_toughened_bimodal_nca_lzo` · `intergranular_cracking_nmc811_jmca2023` — 입계 해상 모델 (Voronoi CZM · phase-field) — 입자 **안**을 푸는 쪽.
- `bucci2017_chemomech_failure_assb_cycling_czm` — 황화물 SE G_c (ASSB 쪽 인성 앵커).
- (동시 작업 중) Sharma 2023 *Extreme Mech. Lett.* 58, 101920 — NMC811 0.271 · 단결정 여부 판정 (이 카드 작성 시점 정본에 **없음**).

---

## 15. 🧮 파생 계산 원장 (`derived(ours)` — 리뷰 숫자만으로 한 우리 산술)

| # | 계산 | 결과 | 비고 |
|---|---|---|---|
| D1 | Fig 10C 각 점의 K = σ_F/(√(2/π)·d^−½·1000) (a = d/2) | 펠릿 0.141 · 0.133 · 0.101 · 0.093 · 0.069 · 0.039 · 0.025 · 이차입자 수염/상자/중앙/상자/수염 **0.133 · 0.162 · 0.193 · 0.224 · 0.300** | a = d 면 전부 ×1.414 |
| D2 | 등고선 기울기 (파선 bbox) vs √(2/π)·K·1000 | 238.8/239.4 · 160.0/159.6 · 81.0/79.8 · 41.5/39.9 | ±4 % (파선 끝 오차) |
| D3 | 이차입자 가로 위치 1.208 vs (1/√0.5 + 1/√1)/2 | **1.2071** → d_eff 0.685 µm | 우리 재구성 |
| D4 | 70.3/158.9 · (158.9/70.3)² · 70.3/185.6 · (185.6/70.3)² | **0.442** · 5.11 · 0.379 · 6.97 | 리뷰 "44 %" · "≈ 5" 재현 |
| D5 | 158.9/185.6 | **0.856 (−14 %)** | "침지 불변" 대조 |
| D6 | 21.5/158.9 · 결함 배수 (K 일정 / K ×0.57) | 0.135 · ×55 / ×18 | 예시 (리뷰 계산 아님) |
| D7 | σ_F 185.6 MPa ÷ H/3 (H 7.10 · 13.99) | 1/12.8 · 1/25.1 | "order of magnitude or more" |
| D8 | √(P/H) (P 1, 2, 3, 6, 10 mN; H 8.60, 10.0, 11.7, 8.74, 6.91) | **0.341 · 0.447 · 0.506 · 0.829 · 1.203 µm** | 파란 계열 x 재현 = Xu 2017 식별 |
| D9 | Fig 9C/D 정규화 d = A_P^½ ÷ (A_P^½/d) | 자홍 0.55 · 빨강 6.5 · 파랑 1.0 · 검정 4.2 · 회색 8.5 · 녹색 80 · ">100" 100 µm | 범위 중앙 |
| D10 | 자홍 H 계열 log-log 기울기 (0.587 → 2.59 µm) | **−0.36** | 포화 없음 |
| D11 | 역산 H_AM 3.85 · 3.83 의 자홍 곡선 위치 (1.65 ↔ 1.76 µm 선형보간) | A_P^½ **1.722 · 1.731 µm** → A_P^½/d **3.13 · 3.15** | 사후 대조 |
| D12 | Fig 9C 에서 A_P^½/d ≈ 1 의 E | 자홍 0.966 → 104 · 파랑 0.829 → 101 GPa | "입자 스케일 E" 의 예 |
| D13 | 헤르츠 접촉 반경 a = (3FR\*/4E\*)^⅓ (R\* 2.5 µm, E\* 74.7 GPa) | F 0.1 · 1 · 10 mN → a 0.136 · 0.293 · 0.631 µm, √π·a 0.24 · 0.52 · 1.12 µm | 스케일 비교용 (기전 전이 아님) |
| D14 | 쪼개짐 하중 P_C = σ_F π d²/2.8 (σ_F 185.6) vs Auerbach P_c = A·K²·R/E\* (A 200, R 2.5 µm, E\* 74.67 GPa) | 0.208 mN/µm² → d 5 µm **5.21 mN** · 10 µm 20.8 mN / P_c K 0.3 **0.603** · 0.19 0.242 · 0.10 0.067 · 1.0 6.70 mN → 비 8.6 · 21.5 · 77.7 · 0.8 | 다른 사건 (쪼개짐 vs 개시) — 예시 |
| D15 | σ_F 185.6 MPa 를 설명하는 결함 a = (K/σ_F)²/π | K 0.3 → 0.83 µm · 0.19 → 0.33 · 0.10 → 0.09 · **1.0 → 9.2 µm** | K 1.0 은 입자 크기급 결함 요구 |
| D16 | Fig 4 V/V₀ = (a/a₀)²(c/c₀) (b/b₀ = a/a₀, 리뷰 명시) | NMC811 남색: x 0.45 −1.0 % · 0.25 −3.4 % · 0.20 −4.8 % · 0.15 −6.2 % · 0.11 −7.0 % / 연청: 0.45 −0.7 % · 0.25 −1.8 % · 0.21 −2.2 % | 두 데이터셋 1.6 %p 차 @ x 0.25 |
| D17 | 우리 A10 −5.1 % 의 x 위치 (남색 NMC811, 0.20 (−4.81 %) ↔ 0.15 (−6.18 %) 선형보간) | **x ≈ 0.19** (0.189) | 보간 |
| D18 | G = K²(1−ν²)/E (E 140, ν 0.25) | K 0.05 → 0.017 · 0.10 → 0.067 · 0.19 → 0.242 · 0.30 → 0.603 J m⁻² | 평면변형 |
| D19 | Xu 2017 이차입자/펠릿 E 비 (`xu2017` Table 1) vs 이 리뷰 Fig 9 작은 압흔 (파랑 143 ÷ 빨강 210) | 0.80 vs 0.68 | 부류 비는 압흔 크기·연구에 따라 달라진다 (Fig 9 쪽은 **다른 연구끼리**의 비 — 예시) |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

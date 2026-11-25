<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-12 신규 작성:
       ① 1저자 지정: "양극 코팅 계산 계보 8편" 세트의 **#2**. #1 = aykol2014_cathode_coating_thermodynamics.md.
       ② #1 digest 가 내린 판정("우리 2.256 V 의 계보는 Aykol 이 아니다")을 #2 가 유지하는지 뒤집는지 확인 —
          결론: **환원축은 뒤집히고(부분), 산화축은 오히려 더 강하게 유지된다** (§6b·§7b).
       ③ 크로핑 그림 14장 중 **본문 Fig 1–6 전량 + SI Fig S1·S3·S4** 를 실제로 봤다 (Fig 6 은 자동추출이
          "영역 없음"으로 버려서 손으로 잘라 등록). SI Fig S2 는 안 봤다 — §0 에 명시.
       ④ ★ 이 논문의 진짜 자산은 본문이 아니라 **CSV 2본**이다. 본 digest 가 그 스키마를 확정하고
          논문의 깔때기(5,225→2,229→1,315→1,315/411/583)와 weighted-sum 랭킹을 **독립 재현**했다(§15).
          재현 과정에서 **Fig 1 에 안 적힌 숨은 필터 1개**(HF-scavenger 의 E_d(products) < 3 V)를 찾아냈다.
       ⑤ ⚠ 무대는 **액체 LiPF₆ LIB** 다. 우리 황화물 SE 축과 범위가 다르다 — §0·§7·§13 에서 반복 명시. -->

# High-throughput computational design of cathode coatings for Li-ion batteries — Aykol, Kim, Hegde, Snydacker, Lu, Hao, Kirklin, Morgan, Wolverton (*Nat. Commun.* **2016**, 7, 13779)

> slug `aykol2016_ht_cathode_coating_design` · DOI `10.1038/ncomms13779` · type `DFT 전용 HT 스크리닝 (OQMD 반응열역학 + MOOP 다목적 최적화; 자체 실험 0)` · PDF `litdb/inbox/107. Aykol2016_HT_Computational_Design_Cathode_Coatings_ncomms13779.pdf` (본문 12 pp) + `107. Sup) …pdf` (SI 6 pp: Fig S1–S4 + Table S1·S2) + **`107. Sup2) …csv`(Supplementary Data 1 — 속성 5,225행)** + **`107. Sup3) …csv`(Supplementary Data 2 — weighted-sum top-100 × 3역할)** · digested `2026-09-12` · status ✅ · 태그 **[외부]**

> elements: H, Li, Be, B, C, N, O, F, Na, Mg, Al, Si, P, S, Cl, K, Ca, Sc, Ti, V, Cr, Mn, Fe, Co, Ni, Zn, Ga, Ge, Se, Br, Rb, Sr, Zr, Nb, Mo, Ru, Rh, Pd, In, Sn, Sb, Te, I, Cs, Ba, Hf, Ta, W, Re, Hg, Tl, Pb, Bi
> methods: DFT, ESW

> **저자**: **Muratahan Aykol**, **Soo Kim**, **Vinay I. Hegde**, **David Snydacker**, **Zhi Lu**, **Shiqiang Hao**, **Scott Kirklin**, **Dane Morgan**(UW-Madison), **C. Wolverton\*** (Northwestern MSE) — 2기관 9인 · 수신 2016-04-20 / 수락 2016-10-31 / **출판 2016-12-14** · **OPEN ACCESS** · 계산 프레임 = **OQMD**(Open Quantum Materials Database, 같은 그룹, 약 300,000 무기물)
>
> **계보 (1저자 지정 "양극 코팅 계산 계보" 8편 세트의 #2)**: [Aykol 2014 AENM](aykol2014_cathode_coating_thermodynamics.md)(#1, 이원 81쌍·닫힌계 ΔH) → **본 논문**(#2, 13만종·ΔG(298 K)·역할 3분할·MOOP) → **[Xiao19]** `xiao2019_cathode_coating_screening.md`(#3, **SSB 축으로 전환**) → Nolan 2019 / Nolan 2021 / Honrao 2021 / 리뷰 2편. 승계·수정 대조는 **§6**.

---

## 0. 이 digest 를 읽는 법 — ⚠ 범위부터, 그리고 **이 논문의 본체는 CSV 다**

**이 논문에도 고체 전해질이 한 번도 안 나온다.** 무대는 **LiPF₆ 유기 액체 LIB**, 적(敵)은 **HF**.
우리 계(황화물 argyrodite SE)에는 HF 가 없다. 그런데 #1 과 달리 #2 에는 **우리가 바로 쓸 수 있는 것이 하나 있다**:
**기계판독 CSV 2본**. 5,225종의 4속성 + 공급위험 지수가 통째로 들어 있고, 우리 스크리닝
(`tools/…/convex_hull_ehull.py` · `db/properties/oxidation_stability.json`)과 **열 단위로 대조 가능**하다.

| 가져올 수 있는 것 | 가져오면 안 되는 것 |
|---|---|
| 🟢 **CSV 스키마와 그 조작적 정의**(§3c) — 우리 스크리닝 대조표의 문헌 열로 바로 붙는다 | 🔴 `G_s-HF` 값 — HF 가 없는 계에 의미 없음. **#1 의 −ΔH_s-HF 와도 다른 양**(기준상태 교체, §6a) |
| 🟢 **E_d 의 정의**(hull 상 첫 상영역의 최고 리튬화 전압 = **환원 개시**) — 우리 red onset 과 **같은 종류의 양** | 🔴 **E_c 를 우리 산화 onset 2.256 V 옆에 놓기** — E_c 는 *액체로의 양이온 용출* 전압이다(§7e) |
| 🟢 **깔때기 구조와 그 숨은 필터**(§15 재현) — "안정" 을 어떻게 기계화했는지의 완전한 레시피 | 🔴 추천 목록(WO₃·Sc₂O₃·Li₂CaGeO₄ …) 을 우리 SE 코팅 후보로 이식 |
| 🟢 **"평형 후에도 기능하나"** 라는 질문(Eq 5–6) — 우리 `interface_reactivity` 에 없는 질문 | 🔴 HHI 를 "합성가능성" 으로 읽기 — **공급망 집중도**지 물성이 아니다 |
| 🟢 **weighted-sum 의 재현 레시피**(§15b) — 우리 cascade 랭킹에 그대로 쓸 수 있는 형식 | 🔴 F(x) 순위 차이를 물리적 우열로 읽기 — **해상도가 없다**(§10-3) |

> **본 digest 에서 실제로 본 그림 (2026-09-12)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` (본문 6장 **전량**) + `Fig. S1` `Fig. S3` `Fig. S4`.
> **안 본 것**: `Fig. S2`(LiMn₂O₄ 버전 매트릭스 — `Fig. S1`(LiCoO₂)과 같은 양식이라 구조 판독이 중복된다. 그래서 **LiMn₂O₄ 축 서술은 본문·CSV 근거만** 쓴다).
> 표 4장(`Table 1` `Table 2` `Table S1` `Table S2`)은 크로핑 PNG 가 있지만 **이미지로 읽지 않았다** — 글자는 PDF 텍스트가 정확하다. 전량 §3 에 옮겼다.
> ⚠ `Fig. 6` 은 자동 크로핑이 "영역 없음"으로 버렸다(캡션 바로 위 블록이 짧은 축 라벨이라 경계 판정 실패) → **손으로 잘라 `fig_6.png` 로 등록**했다.
> 그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했다.

---

## 0.5 처음 읽는 사람을 위한 배경 (#1 을 안 읽었다면 여기부터)

**① HF 가 어디서 오나** — LiPF₆ 는 미량의 물과 만나면 HF 를 만든다. 그 HF 가 양극에서 전이금속을 녹여낸다.
실험적으로 **전해질 HF 농도 ∝ 전이금속 용출량**이 LiCoO₂·LiMn₂O₄ 에서 관측돼 있다.
LiMn₂O₄ 는 특히 표면 Mn³⁺ 의 불균등화(2Mn³⁺ → Mn²⁺ + Mn⁴⁺)가 **H⁺ 이온(산성 환경)에 의해 촉발**되고,
녹아나온 Mn²⁺ 이 음극에 석출돼 열화를 가속한다.

**② 그래서 코팅을 씌운다 — 그런데 코팅의 "역할" 이 하나가 아니다**
#1(2014)은 코팅의 역할을 **HF-scavenger**(HF 를 대신 먹는 희생층) 하나로만 봤다.
#2 는 Chen 2010 의 기능 분류를 받아 **역할을 셋으로 가른다**(§2.5) — 그리고 **역할마다 요구 부등호가 반대다**.
HF 와 잘 반응해야 하는 역할(scavenger)과 **절대 반응하면 안 되는 역할**(HF-barrier)이 같은 표에 공존한다.

**③ 왜 "고속(HT)" 이 필요했나 — #1 의 자기 한계**
#1 은 반응식을 **사람이 가정**했다(`MₓO₁⸝₂ + HF → MₓF + ½H₂O`). 그래서 **이원 금속 산화물밖에** 못 다뤘다.
본 논문 서론이 이걸 명시적으로 자기비판한다: *"reactions that had predefined forms … could not be extended to
other more complex materials."* #2 는 산물을 **OQMD hull 위의 최저에너지 상 조합으로 자동 결정**한다
→ 삼원·사원 화합물까지 확장 가능해졌고, 그 결과 후보가 81 → **약 130,000** 이 됐다.

**④ 읽을 때 주의 — 이 논문의 "안정" 은 한 가지 양이 아니다**
열역학적 안정(hull 위인가) · 전기화학적 안정(E_d, E_c) · HF 반응성(G_s-HF) 이 **서로 다른 세 계산**이고,
그중 E_c 는 **DFT 가 아니라 수용액 표준전극전위표(NBS)** 에서 온다. 섞어 읽으면 바로 틀린다(§3a).

---

## 1. 한 줄 요약

**OQMD 의 산소 함유 화합물 약 13만 종을 대상으로, 코팅의 ⓐ 열역학 안정(hull 위) ⓑ 전기화학 안정(방전측 E_d·충전측 E_c) ⓒ HF 반응성(G_s-HF) 을 전부 "산물을 가정하지 않고 hull 최소화로 자동 결정하는" 반응 모델로 계산하고, 코팅의 역할을 물리장벽/HF-장벽/HF-scavenger 셋으로 갈라 다목적 최적화(weighted-sum + rank aggregation)로 순위를 매긴 논문.** 깔때기는 `130,000 → (hull) 5,225 → (E_d<3 V & −E_c>3.5 V) 2,229 → (비방사성 & HHI<9000) 1,315 → 물리장벽 1,315 / HF-장벽 411 / HF-scavenger 583` (`Fig. 1`). 결과: 물리·HF-장벽은 **4d·5d 금속 인산염**이 새 물질군으로 떠오르고(WO₃·TaPO₅·ZrP₂O₇·Hf₂P₂O₉·NbPO₅·CaSn₄(PO₄)₆), HF-scavenger 는 **규산염·붕산염**이 통계적으로 유리하며(PCA 창 안에서 실리케이트 비중 4.1 %→약 24 %, 보레이트 3.8 %→약 14.5 %, `Fig. 6c` figure-read), 기존 코팅 Al₂O₃(128위)·TiO₂(139위)·ZnO(313위)·AlPO₄(물리장벽 68위)가 **탈락하지 않고 상위권에 재현**되는 것으로 틀을 검증한다. 🔑 두 번째 절반이 더 중요하다 — **양극을 화학공간에 넣으면 결론이 바뀐다**: `LiCoO₂ + αAl₂O₃ → (1−4α)LiCoO₂ + 2αLiAlO₂ + αCo₃O₄ + αLi₂CoO₃` 로 평형된 혼합물은 HF 공격에서 **LiAlO₂ 는 그대로이고 LiCoO₂ 만 소모된다** ⇒ *"완전히 반응한 Al₂O₃ 코팅은 더 이상 HF-scavenger 가 아니다"*(저자 표현 **counter-intuitive**). 그래서 양극별 최적 코팅을 따로 낸다(LiCoO₂ → Li₂SrSiO₄·Li₂CaSiO₄·CaIn₂O₄ / LiMn₂O₄ → Li₂GeO₃·Li₄NiTeO₆·Li₂MnO₃).

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 저자/기관 | Aykol·Kim·Hegde·Snydacker·Lu·Hao·Kirklin (Northwestern MSE) + **D. Morgan** (UW-Madison) + **C. Wolverton\*** |
| 저널 | *Nature Communications* **7**, 13779 (2016), 12 pp · Received 2016-04-20 / Accepted 2016-10-31 / **Published 2016-12-14** · **OPEN** |
| DOI | 10.1038/ncomms13779 |
| 유형 | **순수 계산 HT**. DFT 총에너지는 전부 **OQMD 재사용**(신규 DFT 수행 기술 없음) + 실험 열화학·전기화학 표(JANAF·NBS) 결합. 자체 실험 0, 계면 슬랩 0, kinetics 0, 이온전도 0 |
| 대상 | OQMD 의 **산소 함유 화합물 약 130,000종**(금속 산화물 + 옥시음이온 화합물). 그중 hull 위 **5,225종**이 전 속성 계산 대상 |
| 전해질 | **LiPF₆ 유기 액체** (고체 전해질 언급 0) |
| 핵심 질문 | #1 이 "사람이 가정한 반응식" 때문에 이원 산화물에 갇혔다. **산물을 자동으로 뽑으면** 임의 조성으로 확장되나? 그리고 **코팅 역할을 나누면** 후보 집합이 달라지나? |
| 답 | 둘 다 그렇다. 특히 **역할을 나누면 #1 에서 탈락했던 물질이 다른 역할로 부활**한다(WO₃·Ta₂O₅·Nb₂O₅). |
| 선행 대비 | #1(ref 37) = 이원 산화물/불화물 81쌍·가정 반응식. Chen 2010(ref 22) = 코팅 기능 분류의 실험 리뷰(물리장벽·scavenger). 본 논문 = **HF-barrier 를 새로 제안** + HT 화 + MOOP |
| 자금·COI | 본문에 별도 자금 절이 표시되지 않음(Nat Commun 표준 배치). OQMD 는 같은 그룹 자산 |

## 2.5 ★ 역할 3분할 — **판정 규칙이 역할마다 다르다** (1저자 질문 #2 의 답)

`Table 1` 이 요구 수준을, `Fig. 1` 이 **기계 부등호**를 준다. 둘을 합치면 이렇다.

| 역할 | 언제 쓰나 (저자의 물리적 시나리오) | 열역학 | 전기화학 | **HF 반응성 — 이게 역할을 가른다** | MOOP 속성 집합 | 통과 수 |
|---|---|---|---|---|---|---|
| **Physical barrier** (물리장벽) | **HF 가 지배적 열화 기전이 아닌 계**(저수분 전해질). 양극–전해질 사이를 물리적으로 막기만 하면 됨. 기존 예: ZrO₂·Al₂O₃·ZnO·AlPO₄ | High (hull 위) | High (`E_d<3` & `−E_c>3.5`) | **—** (조건 없음) | {E_c, E_d} | **1,315** |
| **HF-barrier** (HF-장벽) ⬅ **본 논문이 새로 제안** | **HF 가 있고 + ALD 등으로 핀홀 없는 완전 피복이 되는 계**. 코팅이 HF 에 **불활성**이어야 피복·무결성을 유지한다 (scavenger 는 계속 소모되니까) | High | High | **Low** = `G_s-HF ≥ 0` (HF 와 반응이 **비자발적**) | {E_c, E_d, G_s-HF} | **411** |
| **HF-scavenger** (HF 포획) | **HF 가 있고 + 피복이 성기고 불균일한 계**. 양극이 노출된 곳에서 코팅이 **희생적으로** HF 를 먼저 먹는다. 기존 예: Al₂O₃·ZnO·MgO·Sc₂O₃ | High | High | **High** = `G′_s-HF < G_s-HF < 0`, `G′` = **CaO 의 값(−1.285 eV/HF)** = *과잉 반응성 하한* | {E_c, E_d, E_d(products), G_s-HF} | **583** |

- **부등호 방향이 반대**인 것이 핵심이다: HF-barrier 는 `G ≥ 0`(안 먹어야 한다), HF-scavenger 는 `G < 0`(먹어야 한다).
  그래서 `Fig. 5` 캡션이 굳이 못 박는다 — *"f(x) of G_s-HF denotes opposite ideal limits for HF-barrier and HF-scavengers."*
- **HF-scavenger 에만 네 번째 속성 `E_d(products)`** 가 붙는다. 이유: HF 를 먹으면 **불화물이 생기고**, 불화물은
  모(母)산화물보다 리튬화 전압이 높다(#1 의 결과, `Fig. 4d` 에서 대규모 재확인). 즉 **코팅이 HF 를 먹는 순간
  가역 Li 를 훔치는 물질로 바뀔 수 있다** → 그 산물의 리튬화 전압도 같이 걸어야 한다.
- ⚠ **`Fig. 1` 은 HF-scavenger 칸에 `G′ < G < 0` 만 적었지만, 그것만으로는 583 이 안 나온다(902 가 나온다).
  `E_d(products) < 3 V` 를 같이 걸어야 582 가 된다** — 본 digest 의 재현으로 찾은 **숨은 필터**다(§15a).

---

## 3. 핵심 수치 총정리 ★

### 3a. 네 속성의 정확한 정의 (식 번호 그대로) — **"안정" 의 조작적 정의** (1저자 질문 #1 의 답)

| 기호 | 무엇인가 | 반응식 | 산물 결정 | 에너지 출처 | 단위·기준 |
|---|---|---|---|---|---|
| **열역학 안정** | OQMD **convex hull 위인가**(그 화합물을 이루는 원소들의 화학공간에서). 양극·HF 는 공간에 넣지 않는다 | — | — | OQMD ΔfH(0 K) + 기체 엔트로피 보정 | **불리언**. hull 위/아래 |
| **E_d** (방전/리튬화 전압) | `(A_aB_bC_c…)O_x + δLi⁺ + δe⁻ → [aA, bB, cC, …, xO, δLi]_min`. δ 는 **희박량** — 코팅에서 Li 꼭짓점 쪽 **첫 상영역 안에** 머문다. 그 영역에서 μ_Li 가 최저 ⇒ **가능한 가장 높은 E_d** 를 얻는다 | **Eq 1** | **hull 최소화**(`min`) | OQMD ΔG(298 K) | **V vs Li/Li⁺**. ⚠ **평균이 아니라 "최고 계단" = 리튬화 개시 전압** (`Fig. 2b`) |
| **E_c** (충전/용출 전압) | `(A_aB_bC_c…)O_x → δA^{n+} + nδe⁻ + [(a−δ)A, bB, cC, …, xO]_min`. **어느 원소가 녹아나가나**는 모든 구성원소에 대해 계산해 **가장 높은 것**을 채택 | **Eq 2** | 고체 산물만 hull 최소화; **용매화 이온은 실험 전위표** | OQMD + **NBS 수용액 표준산화전위** + Nernst(활동도 10⁻⁶) | **V vs Li/Li⁺**, 음수로 보고. 게이트는 `−E_c > 3.5 V` |
| **G_s-HF** (HF 반응성) | `(A_aB_bC_c…)O_x + δHF → [aA, bB, cC, …, xO, δH, δF]_min` 의 **자유에너지** | **Eq 3** | **hull 최소화** | OQMD + JANAF 기체 엔트로피 + **액체 H₂O·희박 HF 실험값** | **eV per HF** (음수 = HF 를 먹는다) |
| **E_d(products)** | Eq 3 의 **산물 혼합물**을 Eq 1 의 반응물 자리에 넣어 다시 계산한 리튬화 전압 | (Eq 1 재적용) | hull 최소화 | 동일 | **V vs Li/Li⁺** |
| **HHI_R / HHI_P** | 구성 원소의 **Herfindahl–Hirschman 지수** — 매장량(Reserve)·생산(Production)의 **국가 집중도**. 공급위험 프록시 | — | — | ref 75 (문헌표) | 무차원 500–10,000. 게이트 `< 9,000` |

> **🔑 "안정" 은 구간인가 개시점인가 평균인가 — 정확히 이렇다.**
> · **E_d 는 "개시점"이다.** `Fig. 2b` 에서 화살표가 가리키는 것은 첫 계단(가장 높은 계단)이고, 평균이 아니다.
>   ⇒ **#1 의 "평균 전환전압" 이 #2 에서 개시 전압으로 바뀌었다.** (§6b — 1저자 질문의 핵심)
> · **E_c 도 "개시점" 형식이지만 다른 반응이다** — 고체 분해가 아니라 **양이온이 전해질로 용출**되는 전위.
>   그 절대값은 **수용액 표준전극전위**(예: Li 3.04 V)에서 오고, DFT 로 계산된 양이 아니다.
> · **따라서 [E_d, −E_c] 를 "전기화학 창(window)"이라 부르지만**(`Fig. 3`), 이 창은 **두 개의 서로 다른
>   반응 모델을 위아래로 붙여 만든 창**이다. 한 번의 μ_Li 스캔에서 나온 창이 아니다. ⇒ **우리 ESW 와 형식만 같다**(§7).
> · **기준 전극은 vs Li/Li⁺** (Eq 13, 명시). **DB 는 OQMD** (우리는 MP).

### 3b. 깔때기 — 논문의 조작적 스크리닝 전량 (`Fig. 1` 실독)

```
OQMD 산소 함유 화합물            ~130,000
  └ 열역학 안정: convex hull 위인가?          →  5,225
      └ 전기화학 안정: E_d < 3 V  &  −E_c > 3.5 V →  2,229
          └ 비방사성 & HHI < 9000 ?             →  1,315
              ├ Physical barrier   (HF 조건 없음)        → 1,315
              ├ HF-barrier         G_s-HF > 0            →   411
              └ HF-scavenger       G′_s-HF < G_s-HF < 0  →   583   (+ 숨은 E_d(products)<3 V, §15a)
                    └ MOOP: weighted-sum & rank aggregation → 각 역할 top-30 (`Fig. 5`)
```

- **순서가 중요하다**: 전기화학 게이트가 **HHI·방사성 게이트보다 먼저**다. 본 digest 의 재현이 이 순서를 확인한다
  (전기화학 먼저 걸면 2,228 = 논문의 2,229; HHI 를 먼저 걸면 3,276 이 되어 `Fig. 1` 의 어떤 수와도 안 맞는다). §15a.
- **HHI 는 두 지수 모두**에 걸어야 한다(`HHI_R < 9000` **AND** `HHI_P < 9000`). R 만 걸면 수가 안 맞는다. §15a.
- 게이트 `E_d < 3 V`·`−E_c > 3.5 V` 의 의미: 코팅이 **방전 하한(3 V)에서 리튬화되지 않고**, **충전 상한(3.5 V)에서
  용출되지 않아야** 한다. ⚠ 실제 LiCoO₂ 는 4.2 V 까지 충전한다 — **3.5 V 상한은 느슨한 게이트**다(§10-1).

### 3c. ★★ CSV 두 개의 스키마 — **우리 스크리닝에 바로 붙는 열** (1저자 질문 #3 의 답)

#### `107. Sup2) …csv` = **Supplementary Data 1** — 속성 원장

| 열 이름 (원문 그대로) | 내용 | 값 범위 (본 digest 실측) | 우리 대조 상대 |
|---|---|---|---|
| `Material` | 화학식 문자열. **원소 순서가 정규화돼 있지 않다**(예: 본문의 `Li₂SrSiO₄` 가 CSV 에서는 `SrLi2SiO4`) | 5,225행 / **고유식 5,200종** | 우리 후보 조성 문자열 — ⚠ **조성 정규화 후 매칭 필수** |
| `E_d (V)` | 리튬화 **개시** 전압 (Eq 1) | 0.000 – 7.456, 중앙값 **1.996** (E_d = 0 인 것 122종) | 🟢 **우리 `reduction_limit_V`(comp1/modelc **1.242 V**)와 같은 종류의 양** (§7b) |
| `E_d (products) (V)` | HF 반응 **산물 혼합물**의 리튬화 개시 전압 | −3.654 – 7.837, 중앙값 2.782 | 🟡 우리에 대응물 없음. **"1차 분해산물의 2차 반응성"** 이라는 개념만 이식 가능 |
| `E_c (V)` | 양이온 용출(충전측) 전위. **음수 보고** | −16.416 – +4.182, 중앙값 **−3.660** | 🔴 **대조 금지.** 우리 `oxidation_limit`(2.256 V)와 **다른 물리**(§7e) |
| `G_{s-HF} (eV/HF)` | HF 포획 자유에너지. **음수 = HF 를 먹는다** | −3.644 – +0.573, 중앙값 −0.511 · **G>0 982종 / G<0 4,242종** | 🔴 우리 계에 HF 없음. ⚠ **#1 의 −ΔH_s-HF 와도 다른 양**(§6a) |
| `HHI_R` | 매장량 집중도 | 500 – 10,000, 중앙값 4,900 | 🟢 **바로 이식 가능** — 우리 도펀트 스크리닝에 공급위험 열이 아직 없다 |
| `HHI_P` | 생산 집중도 | 1,000 – 10,000, 중앙값 5,500 | 🟢 동일 |

- **행 수 5,225 = 본문의 "5,225 thermodynamically stable" 과 정확히 일치.** 단 **고유 화학식은 5,200종**이고
  **18개 화학식이 중복**(총 25행 초과) — 대부분 `Li₄MTcO₆`·`Li₄MOsO₆` 계열의 **다형(polymorph)** 으로 보이며
  값이 미세하게 다르다(예: `Li₄MnTcO₆` E_d = 1.650 / 1.752 두 행). 본문은 5,225 를 "화합물 수"로 쓴다 — **한 칸의 오차**(§10-5).
- **⚠ 이 목록에 SiO₂·B₂O₃·P₂O₅·SO₃ 가 없다.** 금속 양이온이 없는 "망목형성 산화물"이 후보에서 빠진 것으로 보인다
  (논문이 명시하진 않는다). **#1 의 최대 소득(SiO₂→SiF₄ 기체 실패)이 #2 의 후보 공간에는 아예 없다**는 뜻이다(§10-4).
- 원소 84종 등장. Li 함유 **541종**, Cl 315 · F 229 · S 221 · Si 267 · B 258. 원소수 분포: 2원 143 · 3원 2,491 · 4원 2,230 · 5원 338 · 6원 22 · 7원 1.

#### `107. Sup3) …csv` = **Supplementary Data 2** — 랭킹

| 열 | 내용 |
|---|---|
| `Rank` | 1 – **100** |
| `Physical barrier` | 물리장벽 **weighted-sum** 순위 1–100 |
| `HF-barrier` | HF-장벽 weighted-sum 순위 1–100 |
| `HF-scavenger` | HF-scavenger weighted-sum 순위 1–100 |

- **행 100개 × 3역할 = 300 후보.** `Rank` 는 **역할마다 독립**이다(같은 행의 세 물질은 서로 무관).
- **"무엇이 랭킹인가" = weighted-sum 의 전역목적함수 `F(x) = Σᵢ wᵢ fᵢ(x)` 내림차순**이다.
  **rank-aggregation 순위는 CSV 에 없다** — `Fig. 5` 아래쪽 6패널에만 있다.
  본 digest 가 이것을 **두 갈래로 확정**했다: ① `Fig. 5` 상단 3패널(weighted-sum)의 top-30 순서가
  Sup3 의 1–30행과 **전부 일치** ② 본문이 준 Al₂O₃ 128위·TiO₂ 139위·ZnO 313위·AlPO₄ 68위를
  **재현하면 각각 127·139·313·68위**가 나온다(§15b).
- ⚠ **Sup3 는 순위만 있고 값(F(x))이 없다.** 그래서 "1위와 100위가 얼마나 다른가"를 CSV 만으로는 알 수 없다 —
  본 digest 가 Sup2 에서 F(x) 를 복원해 답했다: **HF-scavenger 는 1위 0.5540, 30위 0.5157, 100위 0.4926**
  = 100칸 내려가는 동안 0.06(눈금 [0,1])밖에 안 떨어진다(§10-3).

#### 🔧 우리 스크리닝 대조표에 **바로 붙일 수 있는 열** (실용 결론)

| 우리 파이프라인 | 붙일 문헌 열 | 붙이는 방식 | 주의 |
|---|---|---|---|
| `convex_hull_ehull.py` (E_hull) | Sup2 의 **행 존재 여부** | Sup2 에 있다 = OQMD hull 위. `E_hull = 0` 의 **독립 DB 교차확인** | ⚠ OQMD vs MP 는 **hull 이 다르다**. "MP 에서 hull 위인데 OQMD 엔 없다" 는 **불일치 신호**로만 쓰고 값으로 안 쓴다 |
| `oxidation_stability.json` 의 **`reduction_limit_V`** | **`E_d (V)`** | 같은 종류의 양(리튬화 개시). **대상이 코팅 산화물 ↔ 우리 SE** 라 물질이 다르지만 **정의는 정렬된다** | ⚠ ΔG(298 K)+기체엔트로피 vs 우리 0 K. 그리고 OQMD vs MP. **절대 비교 금지, 정의 대조만** |
| `oxidation_stability.json` 의 **`oxidation_limit_V`** | ❌ **없음** | — | 🔴 `E_c` 는 대응물이 **아니다**(§7e) |
| 도펀트/코팅 후보 표 | **`HHI_R`·`HHI_P`** | 조성 → 원소 → 최대 HHI. **추가 계산 0** | 🟢 유일하게 값 그대로 이식 가능한 열 (물성이 아니라 경제지표라 우리 db 규율과 충돌하지 않는다) |
| cascade 랭킹 | **weighted-sum 레시피**(§15b) | 우리 속성으로 갈아끼워 같은 형식 사용 | ⚠ 정규화 모집단을 **어디로 잡느냐가 순위를 바꾼다**(§15b 실측) |

### 3d. 추천 결과 전량 — `Fig. 5` weighted-sum top-30 (Sup3 1–30행과 동일)

| 순위 | **Physical barrier** | **HF-barrier** | **HF-scavenger** |
|---|---|---|---|
| 1–5 | TaBO₄ · TaPO₅ · HfO₂ · Ta₂O₅ · WO₃ | WO₃ · WCl₂O₂ · NbPO₅ · ReO₃ · ZrP₂O₇ | **Sc₂O₃** · **MgO** · TaBO₄ · Ca₅B₃O₉F · HfO₂ |
| 6–10 | ZrO₂ · HfSiO₄ · WCl₂O₂ · Sc₂O₃ · BeO | RePO₅ · NbBO₄ · Hf₂P₂O₉ · BaSO₄ · GeP₂O₇ | TaPO₅ · Sr₂Ta₂O₇ · Mg₃B₂O₆ · Sr₂MgB₂O₆ · Ca₂Ta₂O₇ |
| 11–15 | NbPO₅ · ZrSiO₄ · ZrP₂O₇ · ScOF · NbBO₄ | WBr₄O · CaSn₄P₆O₂₄ · Nb₂O₅ · MoCl₄O · SrSO₄ | Ca₂TaAlO₆ · Ta₂O₅ · ScOF · Li₂CaGeO₄ · Li₂MgSiO₄ |
| 16–20 | Hf₂P₂O₉ · CaTi₄P₆O₂₄ · MgO · Ta₉VO₂₅ · ReO₃ | Cr₂O₃ · SnO₂ · MoPO₅ · MoBr₂O₂ · InP₃O₉ | Ca₂BClO₃ · **ZrO₂** · Ca₂MgWO₆ · CaMgSiO₄ · MgAl₂O₄ |
| 21–25 | RePO₅ · ScTaO₄ · Sr₃P₂O₈ · Nb₂O₅ · LiAl₅O₈ | GeO₂ · CsReO₄ · NbCl₃O · RbReO₄ · NaSn₂P₃O₁₂ | Sr₂SiCl₂O₃ · CaAlBO₄ · MgScBO₄ · CaTiO₃ · Li₂SiO₃ |
| 26–30 | CaSn₄P₆O₂₄ · ScPO₄ · ScBrO · Ba₃P₂O₈ · GeP₂O₇ | BiPO₄ · Sb₂PbO₆ · Mn₂PO₄F · SnSe₂O₆ · VSbO₄ | CaMgSi₂O₆ · Li₃NbO₄ · BaBe₂B₂O₆ · LiBO₂ · Ba₂TiSi₂O₈ |

**기존 코팅의 위치 (틀 검증)** — 전부 **모든 스크린을 통과**했고 순위만 낮다. 본문 표현: *"considering the size of the candidate pool, these are still predicted to be near top of the list."*

| 물질 | 본문이 준 순위 | 본 digest 재현 | E_d | E_d(prod) | E_c | G_s-HF |
|---|---|---|---|---|---|---|
| **Al₂O₃** | HF-scav **128위** | **127위** | 1.487 | 2.558 | −5.396 | −0.380 |
| **TiO₂** | HF-scav **139위** | **139위** ✅ | 2.084 | 2.492 | −7.668 | −0.190 |
| **ZnO** | HF-scav **313위** | **313위** ✅ | 1.401 | 2.455 | −4.149 | −0.150 |
| **AlPO₄** | 물리장벽 **68위** | **68위** ✅ | 1.889 | 2.774 | −7.020 | −0.024 |
| MgO | HF-scav top-30 (2위) | 2위 | 0.050 | 1.898 | −3.683 | −0.772 |
| ZrO₂ | HF-scav top-30 (17위) | 17위 | 0.535 | 2.747 | −7.153 | −0.210 |
| **Sc₂O₃** (= #1 의 신규 예측) | HF-scav **1위** | **1위** | 0.254 | 2.067 | −5.482 | −0.602 |

### 3e. 양극을 화학공간에 넣은 "결정론적" 설계 (`Table 2` 전량 + 본문 통계)

**절차**: ① `Cathode + α(coating) → [Cathode, α(…)]_min` (**Eq 4**) 로 평형 혼합물을 구하고
② 그 혼합물을 Eq 1–3 의 반응물 자리에 넣는다. ③ pass/fail 세 조건:
  (i) **코팅과 양극이 반응하지 않는가**(tie-line 이 있는가) (ii) **HF 공격에서 양극이 소모되지 않는가**
  (iii) **코팅이 충·방전 전기화학에 끼어들지 않는가**. + HHI·방사성·과잉반응성 screen 만 추가.

| 양극 | 코팅과 **함께 안정**(tie-line) | **HF 로부터 양극 보호** | **둘 다** | 최종 (전기화학 안정까지) |
|---|---|---|---|---|
| **LiCoO₂** (5,225 중) | 1,792 | 1,237 | **405** | `Li₂SrSiO₄ · Li₂CaSiO₄ · CaIn₂O₄ · SrHClO · SrBrOH · SrHfO₃` (**optimal**) / `Li₅ReO₆ · Sr₂MgWO₆ · Li₄H₃BrO₃ · Li₄H₃ClO₃ · Sr₂LiReO₆ · Sr₂CaWO₆ · SrZrO₃` (**nearly optimal**) |
| **LiMn₂O₄** | 1,003 | 2,841 | **81** (저자 표현 *"surprisingly"*) | `Li₂GeO₃ · Sr₂Nb₂O₇ · Pb₃Cl₂O₂ · Pb₃Br₂O₂ · Li₂TiGeO₅ · Li₂TiSiO₅ · Li₄NiTeO₆ · Ca₂Mn₃O₈ · Li₂MnO₃ · Pb₂SO₂ · PbHClO · PbBrOH · Ba₂Hg₃Pd₇O₁₄` / `CaTa₂O₆ · Pb₃O₄ · SrBrOH · Ba₂TiSi₂O₈ · Ba₂Ti₄Fe₂O₁₄ · Sr₂TaFeO₆ · SrPd₃O₄ · SrHClO · Sr₂NbFeO₆ · CaPd₃O₄` |

- **"nearly optimal" = E_c 게이트를 ±0.12 V 완화한 것.** 근거: 전해질 내 이온 활동도의 **2 자릿수 편차**가
  1전자 반응 전위를 `0.0592/z · log K` 만큼 움직인다(25 °C Nernst). *"reactions with Ec values up to 0.12 V
  higher than that of the cathode material are still allowed to pass."*
- 🔑 **여기서 "안정" 의 기준이 바뀐다** — 일반 MOOP 의 절대 문턱(`−E_c > 3.5 V`)이 아니라
  **양극 자신의 E_c 와의 상대 비교**다. 실제로 `Table 2` 의 LiCoO₂ 최적 코팅 **전부가 일반 MOOP 의
  `−E_c > 3.5 V` 를 통과하지 못한다**(본 digest 실측: Li₂CaSiO₄ 3.362 · CaIn₂O₄ 3.361 · SrHClO 3.465 ·
  SrHfO₃ 3.324 · SrZrO₃ 3.185 …). LiCoO₂ 자신의 E_c 가 **−3.152 V** 이기 때문이다. ⇒ **`Fig. 5` 와 `Table 2` 는
  서로 다른 판정 규칙의 산물이고, 저자도 "not necessarily similar materials" 라고 인정한다.**
- **HF 보호의 필요조건**: 코팅이 **양극보다 HF 와 더 세게 반응**해야 한다. `G_s-HF(LiCoO₂) = −0.87`,
  `G_s-HF(LiMn₂O₄) = −0.49`. 본문: *"more negative than that of about 70 % of candidate coatings"*(LiCoO₂),
  *"about 50 %"*(LiMn₂O₄). **본 digest 재현: 정확히 69.6 % / 49.1 %** (§15c).
  ⇒ **LiCoO₂ 는 보호하기 어려운 양극이고, 그래서 s-block(Li·Mg·Ca·Sr·Ba) 함유 화합물만 남는다.**

### 3f. SI 표 전량 (`Table S1` · `Table S2`)

**`Table S1` — 양극 자신의 반응(자동 탐색 결과)**

| 양극 | 전기화학 반응 | E (V) |
|---|---|---|
| LiCoO₂ | `3LiCoO₂ + 2Li → Li₅CoO₄ + 2CoO` | **2.07** |
| | `Co₃O₄ + Li → LiCoO₂ + 2CoO` | 2.27 |
| | `Co₃O₄ + 2Li₂CoO₃ + Li → 5LiCoO₂` | 3.15 |
| LiMn₂O₄ | `2MnO₂ + Li → LiMn₂O₄` | **3.52** |
| | `3LiMn₂O₄ + 2H₂O + Li → Li₂MnO₃ + 4MnOOH` | 3.35 |
| | `Mn₅O₈ + Li → Mn₃O₄ + LiMn₂O₄` | 3.27 |
| | `5LiMn₂O₄ + 3Li → 4Li₂MnO₃ + 2Mn₃O₄` | 2.22 |

| 양극 | HF 공격 반응 | ΔG_s-HF (eV/HF) |
|---|---|---|
| LiCoO₂ | `4LiCoO₂ + 2HF → Co₃O₄ + 2LiF + Li₂CoO₃ + H₂O` | **−0.87** |
| LiMn₂O₄ | `LiMn₂O₄ + HF → MnO₂ + LiF + MnOOH` | **−0.49** |

**`Table S2` — 프레임워크가 쓴 실험 열화학 데이터** (⚠ *이 표가 #1 과 #2 의 값 차이의 원인이다*)

| 화학종 | `298 × S°_exp` (eV/atom) | `ΔfG°_exp` (eV/atom) |
|---|---|---|
| O₂ (g) | **0.317** | — |
| F₂ (g) | 0.313 | — |
| Cl₂ (g) | 0.345 | — |
| H₂ (g) | 0.202 | — |
| N₂ (g) | 0.296 | — |
| **HF, 수용액(무한희석)** | — | **−1.444** |
| **H₂O (액체)** | 0.072 | — |

- HF 에는 추가로 **활동도 항 `298R·ln[activity]`** 를 농도 10⁻⁶ 로 더한다.
- SI 가 직접 밝히는 중요한 단서: *"the absolute value of the free energy of HF is only a constant in all
  HF-scavenging reactions, and therefore does not alter the relative rankings"* — 즉 **HF 기준상태 선택은
  순위를 안 바꾼다**. 반면 **H₂O 는 다르다**: OQMD 의 H·O 함유 상과 **경쟁**하므로 산물 결정에 직접 개입한다.
  그래서 H₂O(액체)는 *OQMD 안정 다형의 자유에너지 + 실험 융해엔탈피(~0.02 eV/atom) + 상온 엔트로피 항*으로 맞췄다.

---

## 4. DFT / 계산 방법 ★

| 항목 | 내용 |
|---|---|
| **코드** | **VASP** (ref 70·71). ⚠ **본 논문이 직접 돌린 것이 아니다** — 전부 **OQMD 에 이미 있는 형성에너지 재사용** |
| **범함수 / +U** | OQMD 표준: **PBE(GGA) + 최적 U**(ref 63–65 = Wang/Maxisch/Ceder 계보) + **화학퍼텐셜 보정**(GGA 와 GGA+U 를 잇는 fitted elemental reference). 세부 설정은 **Kirklin et al.(ref 46)에 위임**하고 본문에 재기술하지 않는다 |
| **PAW / cutoff / k-mesh** | **본문 미기재** (OQMD 표준에 위임) — ⚠ 이 논문만 읽고는 알 수 없다 |
| **구조 출처** | **ICSD 의 계산 가능한 화합물 거의 전부** + **가설 구조**(흔한 결정구조에 원소를 갈아끼운 decoration). 저자는 가설 구조가 **핵심**이라고 명시 — H·F 를 포함한 미탐색 화학공간의 hull 을 메워 **반응에너지 정확도를 올린다** |
| **온도·압력** | 고체는 **pV 무시**, `ΔfH°(298 K) ≈ ΔfH_OQMD(0 K)` (0↔298 K 차이가 수 meV/atom, ref 65). **고체 엔트로피 S° ≈ 0** |
| **자유에너지 구성 (Eq 7–13)** | `ΔfG°(compound) ≈ ΔfH_OQMD + T·Σ_gas xⱼ S°ⱼ(exp)` (**Eq 9**) — **기체 기준상태(O₂·F₂·Cl₂·H₂·N₂)의 실험 엔트로피만** 넣는다 · `ΔfG°(ion^n+) = −nFε(ion^n+)` (**Eq 10**, NBS 표준산화전위, SHE 기준) · `ΔfG°(원소 기준상태) = 0` (Eq 11) · `ΔrG = ΔrG° + RT·ln(Πa^ν/Πa^ν)` (**Eq 12**) · `E_r = −ΔrG / zF` (**Eq 13**) |
| **활동도** | 고체 = 1. **Li⁺ = 1**. 그 외 용출 이온 = **10⁻⁶** (전해질 희박 근사) |
| **형식 계보** | **Persson 2012 Pourbaix 형식**(ref 72)을 비수계 LIB 로 옮긴 것 — DFT 고체 + 실험 용매화 이온을 한 자유에너지 사다리에 올리는 방식 |
| **산물 결정** | **전면 자동**: 주어진 조성에서 **OQMD 상들의 최저에너지 조합**(ref 48). #1 의 "가정된 반응식" 을 대체한 것이 이 논문의 방법론적 핵심 |
| **무질서 처리** | **없음**(정렬 상만, SQS·enumerate 없음). 다형은 OQMD 안정 다형 1개 |
| **AIMD / MLIP / NEB / DOS / 포논** | **전부 0.** 이온전도·전자전도는 계산하지 않는다(저자 자인, §5.6) |
| **MOOP** | ① **weighted-sum** `F(x) = Σ wᵢ fᵢ(x)` (Eq 14), **wᵢ 균등**, **min-max 정규화** `fᵢ = (f′ᵢ − f′_min)/(f′_max − f′_min)`, 0=최악·1=최선 ② **rank aggregation** — 속성별 순위 리스트를 만든 뒤 **Spearman footrule 거리** `d(a,b) = Σₓ|rᵃₓ − rᵇₓ|` 를 최소화하는 super-list. 완전탐색은 10–15개만 돼도 불가능 → **cross-entropy Monte Carlo**(R 패키지 `RankAggreg`, Pihur et al., ref 77) |
| **PCA** | HF-scavenger 4차원 속성공간 → 2차원. **pca1 78 % + pca2 16 % = 94 %** 설명 |

> **🔑 방법론적으로 이 논문에서 가장 재사용성 높은 한 줄**: *"reactions become complex and non-intuitive even
> for ternary candidate coatings, and the whole procedure described here is fully-automated."*
> **사람이 반응식을 쓰는 순간 화학공간이 이원으로 잘린다** — 우리 `interface_reactivity` 가 이미 이 교훈을
> 따르고 있다(pymatgen hull 최소화). 즉 **#2 의 이 교정은 우리가 이미 통과한 관문**이다.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 깔때기와 역할 분할 (`Fig. 1`, `Table 1`) ★★

`Fig. 1` 은 상자 5단 + 3갈래 분기의 흐름도다. 각 상자 옆에 **통과 수**가 붙는다(§3b).
**실독으로 확인한 것 3개**:
1. **순서**: hull → **전기화학** → HHI/방사성 → 역할 분기. (텍스트 추출만으로는 순서가 뒤섞여 보인다 — 그림을 봐야 확정된다.)
2. **물리장벽 상자에는 부등호 자리에 `–` 만 있다** = HF 조건이 아예 없다. 그래서 1,315 가 그대로 내려온다.
3. **HF-scavenger 상자에는 `G′_s-HF < G_s-HF < 0` 만 적혀 있다** — 그런데 이 조건만으로는 583 이 안 된다(§15a).

`Table 1` 은 역할 × 속성의 **정성 매트릭스**(High/Low/—)다. 숫자가 없다 — 숫자는 `Fig. 1` 에 있다.

### 5.2 E_d 의 정의 — `Fig. 2` (Li₂TiO₃ 예제) ★★★ **우리 축과 제일 가까운 그림**

- **(a)** OQMD Li–Ti–O 삼원 상도. **파란 원 = hull 위(안정)**, **빨간 ×** = 불안정. 표시: a=Li₂TiO₃, b=Li₄Ti₅O₁₂,
  c=Li₄TiO₄, d=LiTi₂O₄, e=LiTiO₂. **점선**이 Li₂TiO₃ 에서 Li 꼭짓점으로 가는 리튬화 경로,
  그 경로의 **첫 상영역**(굵은 파란 tie-line 삼각형)은 **{Li₂TiO₃(a) – LiTiO₂(e) – Li₄TiO₄(c)}** 다.
  캡션: *"The O₂ chemical potential corresponds to T = 298 K and P = 1 atm."*
- **(b)** `Li₂₊ₓTiO₃` 의 리튬화 전압 프로파일. x 축 0–4, y 축 0–1.0 V.
  **figure-read**: 계단이 `≈0.75 V`(x ≈ 0–0.5) → `≈0.34`(–0.85) → `≈0.25`(–0.9) → `≈0.17`(–3.3) → `0`.
  **화살표가 첫 계단을 가리키며 `E_d` 라고 라벨한다.**
  ✅ **교차검증**: CSV 의 `Li2TiO3 → E_d = 0.748 V`. figure-read 0.75 와 일치.
- 대응 반응(본문): `Li₂TiO₃ + ½Li → ½LiTiO₂ + ½Li₄TiO₄`.
- 🔑 **판독 결론**: **E_d 는 평균이 아니라 최고 계단 = 리튬화 개시 전압**이다.
  그리고 그 계단은 **hull 위 첫 상영역**에서 나온다 — 이것은 **grand-potential 환원 개시와 같은 구성**이다(§7b).

### 5.3 "전기화학 창" 의 그림 — `Fig. 3` ★★

세로축 `Potential vs Li/Li⁺` 하나. 왼쪽에 **양극의 작동 창**(파랑↓Discharge / 빨강↑Charge 그라디언트 상자),
오른쪽에 **코팅의 두 준위**: 아래 파란 선 = **E_d**(← `Li⁺, e⁻` 점선 화살표가 들어온다),
위 빨간 선 = **−E_c**(→ `Aⁿ⁺, e⁻` 점선 화살표가 나간다). 둘을 세로 막대가 잇는다.
**읽히는 명제**: *안정한 코팅이란, 양극의 작동 창이 코팅의 [E_d, −E_c] 안에 들어가는 것.*

> ⚠ **그림이 숨기는 것**(본 digest 의 지적): 이 두 선은 **같은 계산에서 나오지 않는다.**
> 아래 선은 **고체 리튬화**(순수 DFT hull), 위 선은 **액체로의 양이온 용출**(수용액 표준전극전위 + Nernst).
> 한 장의 축에 그려 놓아서 **한 번의 μ 스캔으로 얻은 창처럼 보이지만 아니다.** §7e 의 금지 근거다.

### 5.4 속성 간 상충 — `Fig. 4` (6패널 매트릭스) ★★

축(실독): **a** E_c[0..−15 V] vs E_d[0–6 V] · **b** E_c vs E_d(products)[0–6] · **c** E_c vs G_s-HF[−4..+1] ·
**d** E_d vs E_d(products) (**x=y 점선 있음**) · **e** E_d vs G_s-HF · **f** E_d(products) vs G_s-HF.
범례 6종: 회색 점 = 전체 · 빈 사각 = Pareto HF-barrier · 파란 원 = Pareto HF-scavenger · 빈 삼각 = Pareto 물리장벽 ·
**분홍 원 = weighted-sum HF-scavenger** · **주황 사각 = weighted-sum HF-barrier** · **초록 삼각 = weighted-sum 물리장벽**.

실독으로 읽히는 것:
1. **패널 a 는 뚜렷한 음의 상관**이다 — E_d 가 낮아지면 E_c 가 **덜 음수**가 된다. 본문이 말하는 *"mostly conflicting"*.
   이유를 우리 말로 옮기면: **환원에 강한 물질(낮은 E_d)은 대개 산화·용출에도 약하다.**
2. **초록 삼각(물리장벽 top-30)은 E_c ≈ −7 ~ −12 V** 의 깊은 곳에 있다(figure-read). E_d 는 0.5–2.5 V.
   → 물리장벽의 승부처는 **E_c 의 깊이**다(Ta·W·Hf·Zr·Nb 조기 d-block 이 왜 이기는지의 답).
3. **주황 사각(HF-barrier top-30)은 G_s-HF 축의 오른쪽 끝**(> 0)에 모여 있다 — 정의상 당연.
4. **분홍 원(HF-scavenger top-30)은 E_c ≈ −3 ~ −5 V** 로 얕다. → **scavenger 는 E_c 를 희생하고 G 를 얻는다.**
5. **패널 d 가 이 논문에서 가장 깨끗한 물리**: 거의 모든 점이 **x=y 선 아래**, 즉 **E_d < E_d(products)**.
   **불화된 산물이 모(母)산화물보다 높은 전압에서 리튬화된다** — #1 의 결론(F 의 전기음성도)이 5,225종 규모로 재확인된다.
   본문도 *"consistent with the findings in Aykol et al.³⁷"* 로 명시.
6. **패널 c/f 에서 G_s-HF 하한이 약 −3.6**, 상한 약 **+0.6** (CSV 실측 −3.644 / +0.573 과 일치).

### 5.5 랭킹 — `Fig. 5` (6패널) ★★★

상단 3패널 = **weighted-sum**, 하단 3패널 = **rank aggregation**. 열 = 물리장벽 / HF-barrier / HF-scavenger.
각 패널은 세로로 1위(위) → 30위(아래), 가로축은 `fᵢ(x)`(속성별 정규화 값)와 `F(x)`(전역 목적).
마커: 주황 원 E_d · 초록 ◀ E_c · 연두 원 E_d(products) · 파랑 ▶ G_s-HF · **남색 ■ F(x)**.

실독으로 읽히는 것:
1. **남색 ■(F(x))가 거의 수직선**이다 — 특히 HF-scavenger 패널. 즉 **1위와 30위의 전역점수 차이가 거의 없다.**
   (본문도 인정: *"The variation of weighted-sum F(x) within the top 30 HF-scavengers list … is relatively slow."*)
   **본 digest 정량화: F 1위 0.5540 → 30위 0.5157 (Δ0.038) → 100위 0.4926 (Δ0.061).** §10-3.
2. **weighted-sum 과 rank-aggregation 의 상위 집합이 크게 겹친다** — 저자의 강건성 논거.
   다만 **순서는 다르다**(예: 물리장벽 weighted-sum 1위 TaBO₄ ↔ rank-agg 1위 MgO).
3. **HF-barrier 의 rank-agg 리스트에만** `MnFeH₄O₂F₅`·`MnGaH₄O₂F₅`·`MnTl₂H₂OF₅` 같은
   **H·F 동시 함유 상**이 상위에 들어온다 — weighted-sum 리스트엔 없다. ⇒ **방법 의존성의 실물 증거**(§10-3).
4. 상단 물리장벽 패널의 30개 순서가 **Sup3 CSV 의 1–30행과 문자 단위로 일치** → **Sup3 = weighted-sum** 확정.

### 5.6 물질군 통계 — `Fig. 6` (PCA) ★★

- **(a)** 4차원 속성(E_c, E_d, E_d(products), G_s-HF)의 PCA. x = pca1(−8 ~ +7), y = pca2(−4 ~ +4).
  점 색 = 물질군(컬러바: O 부터 Others 까지 21분류). **검은 `+` = `Fig. 5` 의 유망 HF-scavenger**.
  실독: `+` 들이 **pca1 ≈ −1.0 ~ −0.1, pca2 ≈ 1.1 ~ 1.6** 의 작은 상자에 몰려 있고, 상자 밖 outlier 가 **약 5–6개**
  (pca1 ≈ +2 ~ +7, pca2 ≈ 2.3 ~ 3.6)로 보인다(figure-read).
- **(b)** 그 상자의 확대. 이 창 안에 **241종**이 들어간다.
- **(c)** 막대그래프. **파랑 = 전체 5,225 / 빨강 = 창 안 241.** x 축은 창 안에 실제로 나타난 분류만:
  `O, O-Si, O-B, O-P, O-H, O-Cl-B, O-Cl-Si, O-H-Br, O-H-Cl, O-I, O-F-B, O-F-Si, O-S, O-B-Si, O-F-C, O-Si-Br, O-B-Br`.
  **figure-read + 전체값은 CSV 로 정확히 계산**:

| 분류 | 전체 5,225 (**CSV 정확값**) | 창 241 (figure-read) | 배율 |
|---|---|---|---|
| **O** (순수 금속 산화물) | **58.4 %** (3,050종) | ≈ 42 % | 0.7× (**줄어든다**) |
| **O–Si** (규산염) | **4.10 %** (214종) | ≈ 24 % | **≈ 5.9×** |
| **O–B** (붕산염) | **3.77 %** (197종) | ≈ 14.5 % | **≈ 3.8×** |
| O–P (인산염) | 6.26 % (327종) | ≈ 5 % | ≈ 0.8× |
| O–S (황산염) | 2.76 % (144종) | ≈ 0 % | — |
| O–Cl (옥시염화물) | 3.89 % (203종) | **창에 없음** | — |

  ⚠ 본문은 *"5–10 times larger"* 라고 쓰는데, **그림에서 읽으면 규산염 ≈ 6×, 붕산염 ≈ 4×** 다.
  **붕산염 쪽은 "5–10배" 에 못 미친다** — 본문 서술이 관대하다(§10-6).
  🔑 **순수 금속 산화물(O)은 오히려 비중이 준다** = *"plain oxides 가 최선이 아니다"* 가 이 그림의 본론.
- **기전 (`Fig. S3` 실독)**: 규산염·붕산염이 이기는 이유는 **G_s-HF 도, E_c 도, E_d(products) 도 아니다**.
  네 히스토그램 중 **E_d 분포만 확연히 다르다** — 산화물(파란 채움)은 E_d 가 1.9–2.1 V 에 큰 봉우리를 갖는데,
  붕산염·규산염(초록·빨강 외곽선)은 **0.8–1.5 V 쪽에 질량이 크다**. 즉 **환원에 더 강하다.**
  ⇒ **"규산염·붕산염이 좋은 HF-scavenger 인 이유는 HF 를 더 잘 먹어서가 아니라 리튬화 저항이 커서다."**
  (E_c·E_d(prod) 축은 게이트 경계 −3.5 V / 3.0 V 에 질량이 몰려 있어 변별력이 거의 없다 — 이것도 실독 소득.)

### 5.7 양극을 넣으면 무슨 일이 일어나나 — `Fig. S1` 실독 ★★★ **우리 `interface_reactivity` 와 같은 자리**

`Fig. S1`(LiCoO₂ 포함 공간)은 `Fig. 4` 와 같은 6패널인데 **모양이 완전히 다르다.**
- 축 범위가 **양극 자신의 값에 갇힌다**: E_d 축 **2.0–3.2 V**, E_c 축 **0 ~ −3.5 V**, G_s-HF 축 **−2.1 ~ −0.85**.
- **점선 격자가 정확히 `Table S1` 의 값**에 서 있다 — 세로 점선 **2.07 · 2.27 · 3.15 V**(LiCoO₂ 의 세 리튬화 반응),
  가로 점선 **−3.15 V**(LiCoO₂ 의 E_c), 그리고 G 축 오른쪽 끝 점선 **≈ −0.87**(LiCoO₂ 의 HF 공격 ΔG).
- 빨간 빈 사각 = *"Coating stable & cathode protected"*. **이 빨간 점들이 그 점선 위에 띠를 이루며 눕는다**
  (특히 E_d = 2.05 선과 E_c = −3.15 선).

🔑 **판독 결론 (본 digest 의 해석)**: **양극을 화학공간에 넣는 순간, 희박(α→0) 코팅의 "속성"은 대부분
양극 자신의 속성으로 붕괴한다.** 코팅이 양극과 tie-line 을 갖고(반응 안 하고) 자기가 HF 를 먼저 먹지 않는 한,
혼합물의 E_d·E_c·G 는 **양극이 정한다**. 이것이 Eq 5–6 의 "완전 반응한 Al₂O₃ 는 더 이상 scavenger 가 아니다"의
그림 버전이다. ⇒ **우리 `interface_reactivity` 도 같은 성질을 가진다** — SE+양극 혼합물의 반응에너지는
**두 물질 중 더 불안정한 쪽이 지배**한다. §7c.

### 5.8 저자가 스스로 그은 경계 (Discussion 후반) ⚠

1. **탈리튬(충전) 상태 양극과의 반응성을 안 봤다.** 이유가 솔직하다 — *"cathodes themselves become unstable
   against decomposition into other phases under such conditions, and therefore the ground state thermodynamic
   mixture would not include even the cathode itself."* 대신 *"층상→스피넬 변태는 자발적이지 않고 느리다"* 는
   실험적 관찰로 **완전 리튬화 상태만 다루는 것을 정당화**한다.
   ⚠ 이 자리에서 **[Xiao19] 는 정반대로 간다** — 만충·반충 양극 **둘 다** 계산한다. §6c.
2. **유기 전해질 자체와의 반응성을 못 다뤘다.** 부분 대응이 "과잉 반응성" 하한(CaO)뿐.
   실제로 `Table 2` 에 H 함유 상(SrHClO·SrHBrO)이 남아 있고, 저자는 *"may further trigger acid production by
   supplying protons"* 라고 **위험을 인정하면서도 제외하지 않았다**(근거: 수산화물도 산화물만큼 효과적이라는 ref 58).
3. **전자전도·Li⁺ 전도를 전혀 안 봤다.** 이유: 형태·미세구조·합성조건 의존이 커서 모델링이 어렵다.
   Xu et al.(ref 60) 인용 — *"most of the common coating materials do not allow adequate Li ion transport in
   crystalline form whereas their amorphous counterparts often provide fast enough Li⁺ diffusion."*
   그리고 **초박 ALD 는 벌크가 안 되더라도 충분한 전도를 공급할 수 있다**(ref 22·47).
   자기 위치 설정: *"If it becomes available in the future, Li-ion diffusivity data can easily be added as a
   screen/attribute … our screening strategy will reduce the number of compounds for which these computations
   would need to be done."*
4. **두 설계 결과(`Fig. 5` vs `Table 2`)가 다른 것을 형태로 설명한다** — **두꺼운 코팅**(벌크가 공칭 조성을 유지)에는
   `Fig. 5`, **얇거나 양극과 반응하는 코팅**에는 `Table 2` 가 맞다.

---

## 6. 계보 ★★★ — 1저자 질문: **#1 의 판정이 유지되나 뒤집히나**

### 6a. #1 → #2 의 승계·수정 (값이 바뀐 곳까지)

| 층위 | **Aykol 2014 (#1)** | **Aykol 2016 (#2)** | 판정 |
|---|---|---|---|
| 후보 공간 | 이원 금속 산화물/불화물 **81쌍** | OQMD 산소 함유 **~130,000** → hull **5,225** | 1,600배 |
| 반응식 | **사람이 가정**(`MₓO₁⸝₂ + HF → MₓF + ½H₂O`) | **hull 최소화로 자동 결정**(Eq 1–3 의 `[…]_min`) | 🔴 **수정** — #1 의 자기비판 그대로 |
| HF 반응성 기호 | `−ΔH_s-HF` (양수로 보고) | `G_s-HF` (**음수로 보고**) | ⚠ **부호 규약 반전** |
| HF 반응성 기준상태 | **ΔH(0 K)**, HF·H₂O = **고립분자 DFT 총에너지** | **ΔG°(298 K)**, **액체 H₂O + 희박(10⁻⁶) HF 실험 열화학값** | 🔴 **다른 양**. Al₂O₃ 0.76 → 0.380 · CaO 1.50 → 1.285 · MgO 1.15 → 0.772 · ZrO₂ 0.59 → 0.210 · TiO₂ 0.41 → 0.190 · Li₂O 1.70 → 1.582 · Sc₂O₃ 0.89 → 0.602 (부호 맞춰 크기) — **비율도 차이도 일정하지 않다** ⛔ **세대 혼용 금지** |
| 전압 정의 | **평균 전환전압** `V = −ΔH/ne` | **E_d = 리튬화 개시(최고 계단)**, **E_c = 용출 개시** | 🔴 **수정 — 평균에서 개시로 갔다** (`Fig. 2b`) |
| 전압의 대상 | **불화물**(`V(MₓF)`) | **코팅 자신**(E_d) + **HF 산물**(E_d(products)) | 🟡 확장 |
| 산화측 | **없음**(Li 손실만 봄) | **E_c 신설** — 액체로의 양이온 용출 | 🟡 추가(단, 우리 축과 무관, §7e) |
| 역할 | **HF-scavenger 하나** | **물리장벽 / HF-barrier / HF-scavenger** | 🟡 **분할** — 그래서 #1 탈락자가 부활 |
| 선택 방식 | 사람이 **조합 설계도표**(`Fig. 5`)에서 성질 사각형을 긋는다 | **MOOP**(weighted-sum + rank aggregation) | 🟡 기계화 |
| 추가 축 | — | **HHI**(공급위험), **방사성 배제** | 🟢 신설 |
| 산물 물리상태 검사 | **있다(손으로)** — SiF₄·BF₃·PF₅ 기체 제거, MF₅ 저융점 제거 | **없다** ⬅ 🔴 **#2 에서 사라졌다** | 🔴 **퇴보**(§10-4) |
| 평형 후 기능 | **없음**(pristine 만) | **있다** — Eq 4–6 | 🟢 **#2 의 최대 신규 기여** |

**#1 의 신규 예측이 #2 에서 적중한다**: #1 이 *"Al₂O₃·MgO 에 가장 근접한 미탐색 후보"* 로 지목한 **Sc₂O₃ 가
#2 의 HF-scavenger weighted-sum 1위**(2위 MgO). 그리고 **#1 에서 탈락했던 물질이 다른 역할로 부활**한다 —
Ta₂O₅(#1: TaF₅ 저융점으로 제거) → **물리장벽 4위**, WO₃(#1: −ΔH 0.22 로 하한 미달) → **HF-barrier 1위**,
Nb₂O₅ → HF-barrier 13위. **물리장벽·HF-barrier 는 불화물을 만들 필요가 없으므로 #1 의 탈락 사유가 적용되지 않는다.**

### 6b. 🔑🔑 **1저자 질문의 직접 답** — #1 digest 의 판정은 **반쯤 뒤집히고 반쯤 강화된다**

> #1 digest §7b 의 판정: *"우리 산화 onset 2.256 V 의 계보는 Aykol 이 아니다 — Aykol 은 닫힌계·산물 가정·
> eV per HF 정규화·평균 전환전압이고, 우리는 grand-potential 개시 전압이다."*
> **#2 를 읽고 나서 이 네 근거를 하나씩 다시 판정하면 이렇다.**

| #1 판정의 근거 | #2 에서도 유효한가 | 근거 |
|---|---|---|
| ① **산물을 가정한다** | ❌ **더 이상 아니다** | #2 는 Eq 1–3 전부 `[…]_min` = **hull 최소화**. 우리 `InterfacialReactivity(use_hull_energy=True)` 와 **같은 원리** |
| ② **eV per HF 로 정규화한다** | 🟡 **G_s-HF 만 그렇다** | E_d·E_c·E_d(products)는 **V vs Li/Li⁺** 다. 전압 축은 우리와 같은 단위 |
| ③ **평균 전환전압이다** | ❌ **더 이상 아니다** | **E_d 는 개시 전압**이다 — hull 상 첫 상영역의 최고 계단(`Fig. 2b`, CSV 교차검증 0.748 V) |
| ④ **μ 를 열지 않는 닫힌계다** | 🟡 **E_d 는 사실상 열려 있다** | Eq 1 은 `δLi⁺ + δe⁻` 를 **외부에서 공급**받고 δ→0 극한을 취한다 = **Li 저장소를 연 것과 같은 구성**. 저자 스스로 *"the Li chemical potential will be at its lowest value among all possible values along the composition path"* 라고 **μ_Li 로 설명**한다 |

**⇒ 결론 (두 갈래로 나뉜다).**

- 🟢 **환원축**: **#1 판정은 부분적으로 뒤집힌다.** **`E_d` 는 우리 `reduction_limit_V`(1.242 V)와 *같은 종류의 양*이다** —
  둘 다 "hull 위에서 Li 를 조금 넣었을 때 가장 먼저 일어나는 반응의 전압" 이다. Mo/Ong/Ceder → [Zhu15] 의
  grand-potential 환원 한계와 **구성이 같다**. 남은 차이는 **DB(OQMD vs MP)** 와 **ΔG(298 K, 기체엔트로피) vs 0 K**,
  그리고 **대상 물질**(코팅 산화물 vs 우리 SE)뿐이다.
- 🔴 **산화축**: **#1 판정이 오히려 더 강해진다.** **`E_c` 는 우리 `oxidation_limit_V`(2.256 V)와 *다른 양*이다.**
  우리 것은 **Li 를 빼서(탈리튬) 고체가 분해되는** grand-potential 개시 전압이고,
  `E_c` 는 **양이온이 액체 전해질로 용출되는** 전위로, 그 절대값이 **NBS 수용액 표준산화전위 + 활동도 10⁻⁶ Nernst**
  에서 온다. **우리 계에는 용매가 없다** ⇒ **대응물이 존재하지 않는다.**
- 🟡 **[Xiao19] 의 자리는 그대로다.** [Xiao19] 는 `V_ox` 를 **grand-potential 로** 계산한다 —
  **#2 는 산화측을 grand-potential 로 안 간다.** 그래서 **우리 2.256 V 의 직계 조상은 여전히 [Zhu15]/[Xiao19]** 다.
  다만 **환원측 1.242 V 에 대해서는 Aykol 2016 도 "같은 과(科)" 로 인정할 수 있다.**

### 6c. #2 → [Xiao19] (#3) — 무엇이 넘어가고 무엇이 갈라졌나

| 개념 | **Aykol 2016 (#2)** | **[Xiao19] (#3)** | **우리** |
|---|---|---|---|
| 무대 | 액체 LiPF₆ · 적 = **HF** | **SSB** · 적 = **양극 + 황화물 SE 자신** | 황화물 SE |
| 후보 수 | 130,000 → hull 5,225 | 104,082 (Li 함유) → E_hull<5 meV **1,600** | 우리 cascade |
| 열역학 게이트 | **hull 위(E_hull = 0)** — 엄격 | **E_hull < 5 meV/atom** — 살짝 완화 | E_hull |
| 산화측 | **E_c = 용출 전위**(수용액 표준전위) | **V_ox ≥ 4.0 V** (grand potential) | **grand potential onset 2.256 V** |
| 환원측 | **E_d < 3 V** (리튬화 개시) | **V_red ≤ 2.7 V** (grand potential) | **1.242 V** |
| 계면 반응성 | **Eq 4** (희박 α, 양극 + 코팅) | **pseudo-binary `\|ΔE_rxt\| < 100 meV/atom`**(Richards, 전 혼합비 스캔) | **동일**(pymatgen `InterfacialReactivity`) |
| 양극 상태 | **완전 리튬화만**(자인) | **만충 + 반충 둘 다** | 만충 LiCoO₂ (⚠ 반충 미실행 — [Xiao19] digest 가 이미 지적) |
| 이온전도 | **없음**(자인) | **CI-NEB 최종 6종** | MLIP-MD |
| 전자구조 | **없음** | **E_g > 0.5 eV 게이트** | gap 계산 있음 |
| 경제성 | **HHI** | 없음 | 없음 |
| 선택 방식 | **MOOP**(weighted-sum + rank-agg) | **순차 깔때기**(비용 순서 = 단 순서) | 순차 깔때기 |

🔑 **#2 와 #3 은 "같은 문제의 다른 무대" 가 아니라 *다른 문제*다.**
#2 의 축은 **산(酸) 화학**이고 #3 의 축은 **고체-고체 상평형**이다. 겹치는 것은 **열역학 안정 + 전기화학 창 + 계면 반응성**
이라는 **세 칸의 틀**뿐이고, 그 칸을 채우는 계산은 전부 다르다.
**우리 cascade 의 직계 조상은 #3 이고, #2 는 그 형식을 만든 중간 세대**다.

---

## 7. 우리 DFT 와의 대조 ★★ (`../our_dft_baseline.md`, `db/properties/`)

### 7a. 먼저 못 박을 것

| 층위 | Aykol 2016 | 우리 |
|---|---|---|
| 전해질 | **LiPF₆ 유기 액체** | **황화물 고체**(Li₆PS₅Cl / Li₅.₄PS₄.₄Cl₁.₆) |
| 열화 경로 | **HF 산 공격 + 금속 용출 + 산성 불균등화** | **전기화학 산화**(μ_Li 낮춤) + **고체-고체 계면 반응** |
| 에너지 DB | **OQMD** | **Materials Project** GGA/GGA+U hull |
| 자유에너지 | **ΔG(298 K)** = ΔfH_OQMD + 기체 엔트로피(JANAF) + 용매화 이온(NBS) | **0 K hull**, 엔트로피 없음 |
| 산화측 앙상블 | **용출**(액체, 활동도 10⁻⁶) | **μ_Li 개방** grand potential |
| 환원측 앙상블 | **Li 희박 삽입**(δ→0) — 사실상 μ_Li 개방 | **μ_Li 개방** grand potential |
| 무질서 | **없음** | **있다**(argyrodite S/Cl 무질서) |

### 7b. 축별 판정 — **어디까지가 같은 양인가**

| 우리 양 | Aykol 2016 의 대응 | 판정 |
|---|---|---|
| **`reduction_limit_V` = 1.242 V** (`Li₆PS₅Cl + 5Li → 5Li₂S + LiCl + P`) | **`E_d`** | 🟢 **같은 종류의 양**(hull 첫 상영역 리튬화 개시). ⚠ 값 비교는 금지 — DB·온도기준·대상물질 셋 다 다르다. **정의 대조까지만** |
| **`oxidation_limit_V` = 2.256 V** (`Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻`) | ❌ **없다** | 🔴 **대응물 없음.** E_c 는 용출 전위 |
| **`ocv_self_decomposition_V` = 1.717 V** | ❌ 없다 | 🔴 없음 |
| **`interface_reactivity` min ΔE = −0.3227 eV/atom** (comp1/LiCoO₂) | **Eq 4** (희박 α 평형) | 🟡 **질문은 같고 정규화가 다르다** — 저자는 `α→0` 희박 극한 1점, 우리(Richards/pymatgen)는 **전 혼합비 스캔 후 최악점**. #2 가 더 **보수적이지 않다** |
| **`E_hull`** | **hull 위 불리언** | 🟡 같은 개념, **DB 가 다르다**(OQMD vs MP) |
| **band gap** | ❌ 없음 | — |
| **HHI** | **있다** | 🟢 **우리에 없는 축.** 값 그대로 이식 가능(물성이 아님) |

### 7c. 🔑 우리 파이프라인에 **없는 질문** — #2 가 주는 실질 소득 3개

| # | #2 의 형태 | 우리 현황 | 이식했을 때 |
|---|---|---|---|
| ① **"평형 후에도 기능하나"** (Eq 5–6, `Fig. S1`) | `LiCoO₂ + αAl₂O₃` 평형 혼합물에 HF 를 때리면 **LiAlO₂ 는 안 줄고 LiCoO₂ 만 소모** ⇒ 완전 반응한 Al₂O₃ 는 scavenger 가 아니다 | **없다.** 우리 `interface_reactivity` 는 **1회 반응의 ΔE 와 산물까지**만 낸다 | comp1/LCO 평형 산물 `Co₉S₈ + Li₃PO₄ + Li₂S + LiCl + Li₂SO₄` 중 **Li₃PO₄·LiCl 은 절연 보호막 후보**, **Co₉S₈ 은 전자전도체**. *"이 CEI 가 스스로 passivate 하나, 전자경로를 깔아 분해를 잇나"* 는 **아직 우리 표에 없는 질문**. ([Xiao19] SI 의 *"기존 3원 산화물 코팅 분해산물이 전자전도성 TM 황화물"* 행과 **동일 질문**) |
| ② **"보호자가 피보호자보다 더 반응성이어야 한다"** 라는 상대 기준 | `G_s-HF(coating) < G_s-HF(cathode)`. LiCoO₂ −0.87 → **후보의 30 %만 자격** / LiMn₂O₄ −0.49 → **51 %** (본 digest 재현) | **없다.** 우리는 `interface_reactivity` 를 **절대 문턱 없이** 순위로만 본다 | 우리 축으로: *"도펀트/코팅이 SE 자신보다 양극과 더 세게 반응해야 희생층이 된다"* — `interface_reactivity` 표에 **SE 자신의 값을 기준선으로 그린 열**을 추가하면 추가 계산 0 으로 붙는다 |
| ③ **HHI(공급위험) 게이트** | `HHI_R < 9000 & HHI_P < 9000` + 방사성 배제. **5,225 → 2,229 → 1,315 단계에서 40 % 를 잘라낸다** | **없다.** 우리 도펀트 스크리닝에 경제성 축이 0 | 값이 CSV 에 통째로 있다. 조성→원소→max(HHI) 한 열. ⚠ **물성이 아니므로 `canonical_registry.json` 에 넣지 않고 스크리닝 보조열로만** |

### 7d. 항목별 대조 — 같은가 다른가

| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| **DFT 코드/범함수** | VASP · PBE(+최적 U) — **OQMD 재사용**, 설정은 ref 46 에 위임 | QE · PBE (계별 pseudo); hull 은 MP VASP-PBE(+U) | 🟡 같은 범함수 계열, **다른 DB 세대** |
| **DFT+U** | Wang/Maxisch/Ceder 계보 U **사용**(OQMD 표준) | MP GGA/GGA+U 혼합 hull (같은 U 계보) | 🟢 **U 출처 동일** (⚠ #1 은 시험 후 미채택 — 세 문서가 다르다) |
| **온도** | **298 K 근사**(기체 엔트로피만) | **0 K** | 🔴 다르다. #2 쪽이 한 칸 더 정교하지만 고체 엔트로피는 여전히 0 |
| **산물 결정** | **hull 최소화** | **hull 최소화** | 🟢 **같다** |
| **환원 전압 정의** | **개시**(첫 상영역 최고 계단) | **개시**(μ_Li 스캔 첫 분기) | 🟢 **같은 구성** |
| **산화 전압 정의** | **용출**(수용액 전위표) | **탈리튬 분해**(grand potential) | 🔴 **다르다 — 비교 금지** |
| **무질서** | 없음 | 있다(±0.2–0.3 eV 흔들림) | 🔴 비교 불가 |
| **정확도 자기선언** | **없다** — MAE·불확도를 한 번도 안 쓴다. ⚠ #1 은 MAE 0.125 eV/HF·전압 ±0.20 V 를 선언했다 | 우리도 ESW 절대정확도 미선언 | 🔴 **#1 대비 퇴보**(§10-2) |
| **B₂O₃ / SiO₂ / P₂O₅** | **후보 목록에 없음**(금속 없는 산화물) | `b2o3_esw.json`: LPSCl+B₂O₃ 는 창이 양쪽에서 좁아짐(red 1.72 / ox 2.03) · gap 1.9671 eV | 🔴 **#2 로는 B₂O₃ 를 논할 수 없다** — 후보 공간에 없다 |
| **Li₃PO₄** | 물리장벽 **51위** · HF-scav **117위** (E_d 0.675 · E_c −3.936 · G −0.162) | 우리 comp1/LCO **계면 산물**로 나온다 | 🟡 **재미있는 교차**: 우리 CEI 산물이 저쪽에선 **코팅 후보**다. 단 축이 달라 논거로 못 쓴다 |
| **LiNbO₃ / Li₂ZrO₃ / LiAlO₂ / Li₄SiO₄ / Li₃BO₃** (고체계 대표 코팅) | LiNbO₃ 만 통과(HF-scav 243위). **Li₂ZrO₃(−E_c 3.150)·LiAlO₂(3.409)·Li₄SiO₄(3.105)·Li₃BO₃(3.305)·LiInO₂(3.072)는 전부 `−E_c > 3.5 V` 에서 탈락** | 우리 계에서는 SSB 코팅 후보군 | 🔴 **구조적 편향**: Li 를 많이 든 화합물은 **Li⁺ 용출 전위(3.04 V)** 때문에 −E_c 가 3.0–3.7 V 에 몰려 **게이트에 걸린다** ⇒ **이 프레임워크는 Li 이온전도성 코팅에 체계적으로 불리하다**(§10-7) |

### 7e. ⚠ 유혹 — **절대 하면 안 되는 비교**

`−E_c` 는 `V vs Li/Li⁺` 이고 값이 3.0–12 V 라, 우리 산화 onset **2.256 V** 와 **겉보기 같은 축**에 있다.
그래서 *"LPSCl 의 2.256 V 는 Al₂O₃ 의 5.396 V 보다 훨씬 낮다"* 같은 문장을 쓰고 싶어진다.
**⛔ 쓰지 마라.** 이유 넷:
① **물리가 다르다** — 하나는 *고체가 Li 를 잃고 분해*, 하나는 *양이온이 액체로 녹아나감*.
② **에너지 출처가 다르다** — `E_c` 의 뼈대는 **DFT 가 아니라 NBS 수용액 표준전극전위표**다.
③ **활동도 가정이 들어 있다** — `10⁻⁶`. 이 숫자를 바꾸면 값이 바뀐다(저자 자신이 ±0.12 V 버퍼로 인정).
④ **우리 계에는 용매가 없다** — 용출할 곳이 없다.
같은 이유로 `E_d` 도 **정의만 대조하고 값은 비교하지 않는다**(DB·온도기준·대상 물질이 다르다).

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | HT 깔때기 흐름도. 130,000 → 5,225(hull) → 2,229(E_d<3 & −E_c>3.5) → 1,315(비방사성 & HHI<9000) → 물리장벽 1,315 / HF-barrier 411 / HF-scavenger 583 → MOOP → top-30 | **"안정" 의 조작적 정의 원본.** 단 계수 순서를 그림에서만 확정할 수 있다. ⚠ HF-scavenger 칸의 조건이 불완전하다(§15a) |
| 2a | OQMD Li–Ti–O 삼원 상도. 파란 원 = hull 위, 빨간 × = 불안정. 점선 = Li₂TiO₃ 리튬화 경로, 굵은 tie-line = 첫 상영역 {Li₂TiO₃, LiTiO₂, Li₄TiO₄} | 우리 grand-potential 환원 한계와 **같은 기하**. 설명 그림으로 인용 가능 |
| 2b | Li₂₊ₓTiO₃ 리튬화 전압 프로파일(x 0–4, V 0–1.0). 화살표가 첫 계단 `E_d ≈ 0.75 V` 를 가리킨다 (CSV 0.748 과 일치) | 🔑 **E_d = 평균이 아니라 개시**임을 확정하는 그림. §6b 판정의 근거 |
| 3 | 코팅의 전기화학 창 모식도. 세로축 V vs Li/Li⁺, 아래 E_d(Li⁺·e⁻ 유입) 위 −E_c(Aⁿ⁺·e⁻ 유출), 왼쪽에 양극 작동창 | ⚠ **두 개의 다른 반응 모델을 한 축에 붙인 창**임을 보여 준다 — §7e 금지 규율의 그림 근거 |
| 4a–f | 5,225종의 4속성 짝별 산점도 6패널 + Pareto/weighted-sum 마커 | **d 패널이 핵심**: 거의 전 점이 x=y 아래 = **E_d < E_d(products)** (불화 산물이 더 높은 전압에서 리튬화). #1 의 결론을 5,000종 규모로 재확인 |
| 5 | 역할 3종 × 방법 2종 = 6패널, 각 top-30 과 fᵢ(x)·F(x) | ① Sup3 CSV 가 **weighted-sum** 임을 확정 ② **F(x)가 거의 수직선** = 순위 해상도 없음(§10-3) ③ rank-agg 에만 H·F 상이 상위 = 방법 의존성 |
| 6a,b | HF-scavenger 4속성 → PCA (pca1 78 % + pca2 16 % = 94 %). 유망 후보(`+`)가 pca1 −1.0~−0.1, pca2 1.1~1.6 창에 밀집, 창 안 241종 | 차원축소로 "유망 영역" 을 정의하는 형식 — 우리 cascade 후보 지도에 그대로 쓸 수 있는 양식 |
| 6c | 물질군 비중 막대(파랑 전체 5,225 / 빨강 창 241). O 58.4→≈42 %, O–Si 4.1→≈24 %, O–B 3.8→≈14.5 % | 🔑 **"순수 산화물이 최선이 아니다"**. ⚠ 본문 "5–10배" 는 그림상 Si ≈6× · B ≈4× 로 **관대**(§10-6) |
| S1 | LiCoO₂ 를 화학공간에 넣은 6패널. 축이 **양극 자신의 값(2.07·2.27·3.15 V, E_c −3.15, G −0.87)** 에 갇히고 빨간 점(안정&보호)이 그 선 위에 눕는다 | 🔑🔑 **양극을 넣으면 코팅 속성이 양극 속성으로 붕괴한다** — 우리 `interface_reactivity` 의 같은 성질을 가리킨다(§5.7·§7c①) |
| S2 | LiMn₂O₄ 버전 매트릭스 | ⬜ **안 봤다**(S1 과 같은 양식). LiMn₂O₄ 축은 본문·CSV 근거만 사용 |
| S3 | 산화물·붕산염·규산염의 4속성 히스토그램 | 🔑 **E_d 분포만 다르다** — 붕산염·규산염이 이기는 이유는 *HF 를 더 잘 먹어서가 아니라 리튬화 저항이 커서*다. E_c·E_d(prod) 는 게이트 경계에 몰려 변별력 없음 |
| S4 | min-max 정규화된 4속성의 빈도 분포 (HF-scavenging / Discharge Pot. / Discharge Pot.[HF-products] / Charge Pot.) | 🔑 **균등 가중 weighted-sum 의 내재 편향**을 보여 준다. ⚠ **SI 캡션이 틀렸다** — 고쪽으로 치우친 것은 *charge* 가 아니라 *discharge* potential 이다(§10-8, 본 digest 실측 f 평균 E_d 0.735 vs E_c 0.380) |
| Table 1 | 역할 × 속성 요구 매트릭스(High/Low/—) | 역할 판정 규칙의 정성 원본. 숫자는 `Fig. 1` |
| Table 2 | LiCoO₂·LiMn₂O₄ 별 optimal / nearly-optimal 코팅 목록 | ⚠ **일반 MOOP 와 판정 규칙이 다르다**(절대 문턱 → 양극 상대 문턱 + ±0.12 V 버퍼). §3e |
| Table S1 | LiCoO₂·LiMn₂O₄ 자신의 전기화학·HF 반응식과 값 | `Fig. S1` 의 점선 격자가 이 값들이다. **양극 자신의 G_s-HF 가 코팅 자격의 문턱**(−0.87 / −0.49) |
| Table S2 | 프레임워크가 쓴 실험 열화학값(기체 엔트로피·HF(aq)·H₂O(liq)) | 🔑 **#1↔#2 값 차이의 원인**. HF 기준은 순위를 안 바꾸고, **H₂O 는 산물 결정에 개입한다**(SI 명시) |

## 9. Post-processing ★

| 무엇을 | 어떻게 | 도구 |
|---|---|---|
| 상안정(hull) | OQMD 상도에서 hull 위/아래 판정. `Fig. 2a` 가 그 예시 | OQMD 내부(본문 미기술) |
| 반응 산물 | 주어진 조성에서 **OQMD 상들의 최저에너지 조합**(ref 48) | 자체(자동화), 도구명 미기재 |
| 전압 | `E_r = −ΔrG / zF` (Eq 13), 기준 Li/Li⁺ | 자체 |
| 용매화 이온 | `ΔfG°(ion) = −nFε` (NBS 표), 활동도 10⁻⁶ Nernst | 자체 (Persson 2012 Pourbaix 형식) |
| 기체 엔트로피 | JANAF 3rd ed. (ref 73) | 표 조회 |
| 다목적 최적화 | weighted-sum(균등 가중 + min-max) / rank aggregation(Spearman footrule + cross-entropy MC) | **R `RankAggreg`**(Pihur et al., ref 77) |
| 차원축소 | PCA 4D → 2D, 78 %+16 % | 미기재 |
| **재현성** | **Supplementary Data 1(속성 5,225행) + Data 2(랭킹 top-100×3) 공개**. *"All other relevant data are available from the authors."* | CSV |

⚠ **없는 것**: NEB·DOS·COHP·Bader·포논·탄성·AIMD·MLIP — 전부 0.

---

## 10. 비판 — 이 논문의 약한 곳 ★

1. **전기화학 게이트가 실제 셀보다 느슨하다.** `−E_c > 3.5 V` 는 "충전 상한 3.5 V" 를 뜻하는데,
   LiCoO₂/NCM 은 **4.2–4.3 V 까지** 충전한다. 즉 **실제 충전 상한에서 용출될 물질이 게이트를 통과**한다.
   `Table 2` 에서는 양극 상대 기준으로 바꾸면서 이 문제를 **부분적으로만** 우회한다(LiCoO₂ E_c = −3.152 V 기준).
   ⇒ **"전기화학적으로 안정" 이라는 라벨의 담보 범위가 3.5 V 까지다.** 본문은 이 한계를 명시하지 않는다.
2. **정확도 선언이 없다.** #1 은 DFT–실험 MAE(0.125 eV/HF)·전압 오차(±0.20 V)를 **표로 제시**하고 실험 불확도(CSU)와
   나란히 놓았다. #2 는 **그 절을 통째로 들어냈다.** 유일한 불확도 언급이 `E_c` 의 ±0.12 V 버퍼인데,
   그것도 *"활동도 2자릿수"* 라는 **가정에서 유도된 수**지 검증된 오차가 아니다.
   ⇒ **후보 수가 1,600배 커진 논문에서 오차 서술이 오히려 줄었다.**
3. **랭킹에 해상도가 없다.** 본 digest 재현 결과 HF-scavenger 의 `F(x)` 는 **1위 0.5540 → 30위 0.5157 → 100위 0.4926**.
   **1위에서 0.05 이내에 64종**이 들어온다. Al₂O₃(127위)조차 1위와 **0.066** 차이다.
   ⇒ *"Sc₂O₃ 가 1위, MgO 가 2위"* 같은 서술은 **유효숫자가 없는 순위**다. 저자도 *"variation … is relatively slow"*
   라고 인정하지만, 그렇다면 **top-30 목록을 제시하는 형식 자체가 과잉 해석을 유도**한다.
   (rank-aggregation 과 weighted-sum 의 **순서가 다른 것**도 같은 증상이다 — 물리장벽 1위가 TaBO₄ ↔ MgO 로 갈린다.)
4. **#1 의 최대 소득이 사라졌다 — 산물의 물리상태 검사.** #1 은 SiF₄·BF₃·PF₅ 가 **기체**라서 SiO₂·B₂O₃·P₂O₅ 코팅이
   실험에서 실패한다는 것을 **손으로** 걸러냈다. #2 는 전면 자동화하면서 **이 검사를 넣지 않았다.**
   게다가 **SiO₂·B₂O₃·P₂O₅ 자체가 후보 목록(CSV)에 없다** — 그래서 "이 문제가 없다"가 아니라 **"이 문제가 안 보인다"** 다.
   실제로 top-30 에 `WBr₄O`·`MoCl₄O`·`WCl₂O₂`·`NbCl₃O`·`MoBr₂O₂` 같은 **옥시할라이드**가 대거 들어 있는데,
   이들은 **휘발성이 높기로 유명한 화합물군**이다(WCl₄O·MoCl₄O 등은 승화·저융점). **물리상태 게이트가 있었다면
   걸러졌을 후보들이 상위에 앉아 있다.**
5. **"5,225 compounds" 는 화합물 수가 아니라 행 수다.** CSV 에 **18개 화학식이 중복**(총 25행 초과)돼 있고
   값이 미세하게 다르다(다형으로 보임). **고유 화학식은 5,200종.** 본문·`Fig. 1`·Discussion 이 모두 5,225 를
   "compounds" 로 쓴다. 큰 오류는 아니지만 **CSV 를 기계로 쓰는 쪽에는 실질적**이다(중복 제거 없이 통계를 내면 어긋난다).
6. **`Fig. 6c` 의 "5–10배" 가 그림보다 관대하다.** figure-read 로 규산염 ≈5.9×, 붕산염 ≈3.8× 다
   (전체 비중은 CSV 로 정확히 4.10 % / 3.77 % 확인). 붕산염은 "5–10배" 에 미달한다.
   그리고 **창(241종)의 경계가 `Fig. 6a` 에서 손으로 그은 사각형**이다 — 창을 조금만 옮기면 비율이 바뀐다.
   **민감도 분석이 없다.**
7. **Li 함유 코팅에 구조적으로 불리한 프레임워크다.** `E_c` 는 "가장 잘 녹아나가는 원소" 로 정해지는데,
   Li 의 표준산화전위가 3.04 V 로 원소 중 최상위권이라 **Li 를 든 화합물은 −E_c 가 3.0–3.7 V 대에 몰린다.**
   실측: `Li₂ZrO₃ 3.150 · LiInO₂ 3.072 · Li₄SiO₄ 3.105 · Li₃BO₃ 3.305 · LiAlO₂ 3.409 · SrLi₂SiO₄ 3.352` — **전부 탈락.**
   그런데 **Li 를 든 코팅이야말로 Li⁺ 전도 가능성이 있는 코팅**이다(저자도 *"such compounds are more likely to be
   good Li-ion conductors"* 라고 쓴다). ⇒ **이온전도를 안 보는 대가가 게이트에 그대로 반영된다**: 전도성 후보를
   먼저 잘라 놓고 "이온전도는 나중에 붙이면 된다" 고 말하는 구조.
8. **`Fig. S4` 캡션이 그림과 어긋난다.** 캡션은 *"charge potential is emphasized more … since it skewed more
   towards higher f(x) values"* 라고 하는데, 그림에서 고(高) f(x) 쪽으로 치우친 것은 **주황색 Discharge Pot.** 이다.
   **본 digest 실측(5,225종 min-max)**: f 평균 — **E_d 0.735** · E_d(prod) 0.431 · **E_c 0.380** · G_s-HF 0.274.
   ⇒ 균등 가중 F(x) 에서 **상수처럼 밀어 올리는 것은 discharge potential** 이고,
   **변별에 기여하는 것은 오히려 분산이 큰 G_s-HF(σ 0.150)** 다. 캡션의 진단이 반대다.
9. **양극이 탈리튬 상태일 때를 안 본다** — 저자가 자인하지만, 그 정당화(*"층상→스피넬 변태는 느리다"*)는
   **열역학 논문이 동역학 논거로 범위를 방어**하는 형태다. [Xiao19] 는 같은 문제를 **만충·반충 둘 다 계산**하는 것으로 푼다.
10. **H 함유 상을 위험하다고 인정하면서 목록에 남긴다.** `Table 2` 의 `SrHClO`·`SrHBrO`·`Li₄H₃ClO₃`·`Li₄H₃BrO₃`·
    `PbHClO`·`PbBrOH` — 저자 스스로 *"may further trigger acid production by supplying protons"* 라고 쓴다.
    **HF 를 막으려는 논문이 양성자 공급원을 추천 목록에 남기는 것**은 내부 긴장이다.

---

## 11. 적용 인사이트 (우리 캠페인에 어떻게 쓰나)

1. **🔑 우리 `interface_reactivity` 표에 "기준선 열" 을 추가한다 (추가 계산 0).**
   #2 의 자격 조건은 절대값이 아니라 **상대 비교**였다 — *코팅은 양극보다 HF 와 더 세게 반응해야 한다*.
   우리 축 번역: **`interface_reactivity(도펀트계/LCO)` 를 `interface_reactivity(host/LCO) = −0.3227 eV/atom` 기준선과
   같은 표에 놓는다.** 지금은 순위만 보는데, **"host 보다 나아졌나" 가 판정이 되어야 한다.**
2. **🔑 "평형 후 산물이 무엇을 하는가" 를 우리 표의 열로 만든다.**
   comp1/LCO 산물 중 **Co₉S₈ = 전자전도체 / Li₃PO₄·LiCl = 절연체**. #2 의 Eq 5–6 이 보여준 것은
   *"1차 반응 산물이 2차 보호기능을 하는지 따로 물어야 한다"* 이고, 이 질문은 [Xiao19] SI 의
   *"기존 3원 코팅 분해산물이 전자전도성 TM 황화물"* 행과 **정확히 같은 질문**이다.
   ⇒ **산물 목록에 `전자전도성 여부` 열**(문헌 판정으로 채울 수 있음)을 붙인다.
3. **🔑 HHI 열을 도펀트 스크리닝에 붙인다.** CSV 에 원소별 값이 사실상 다 들어 있다(조성→원소→max).
   우리 cascade 는 **경제성 축이 0** 이다. ⚠ 물성이 아니므로 `db/properties/canonical_registry.json` 에 넣지 않고
   **스크리닝 보조열**로만 쓴다.
4. **weighted-sum 랭킹의 정규화 모집단을 명시하는 규율.** 본 digest 재현이 보여준 것:
   **min-max 를 "전체 5,225" 로 잡느냐 "걸러낸 풀" 로 잡느냐에 따라 상위 20 의 순서가 크게 바뀐다**
   (전체 기준이면 논문과 top-20 중 11–14개 위치 일치, 풀 기준이면 1–5개). ⇒ **우리 cascade 가 점수를 낼 때
   "정규화 모집단" 을 기록하지 않으면 순위를 재현할 수 없다.** (§15b)
5. **우리 환원 한계(1.242 V)의 계보 서술을 정정한다.** #1 digest 는 *"Aykol 은 평균 전환전압"* 이라고 썼는데
   **#2 는 개시 전압**이다. 원고에서 *"우리 ESW 는 문헌 코팅 스크리닝과 같은 틀"* 이라고 쓰려면
   **환원측에 한해 Aykol 2016 을 같이 인용할 수 있다** — 산화측은 여전히 [Zhu15]/[Xiao19] 다.
6. **⚠ 우리 도펀트 후보에 "휘발성/저융점 산물" 표시 열이 필요하다는 근거가 하나 더 늘었다.**
   #2 는 옥시할라이드(WCl₂O₂·MoCl₄O·WBr₄O·NbCl₃O)를 상위에 올리면서 **휘발성을 전혀 검사하지 않는다**.
   우리 계에도 같은 구멍이 있다(hull 이 전부 고체로 취급, [Zuo] DEMS 는 SO₂ 기체 실측).

---

## 12. 인용 가능 문장 (초안 — 영문/국문)

- EN: "Aykol *et al.* screened >130,000 oxygen-bearing compounds in the OQMD by combining convex-hull stability with
  reaction models for lithiation, cation dissolution and HF attack, and classified candidate cathode coatings into
  physical barriers, HF barriers and HF scavengers [Aykol 2016]."
- EN: "In their framework the discharge potential *E*_d is defined as the **highest** lithiation voltage obtained in
  the first phase region along the path toward the Li corner of the OQMD phase diagram, i.e. an **onset** rather than
  an average conversion voltage [Aykol 2016, Fig. 2]."
- EN: "Notably, when the cathode is included in the chemical space, a nominal Al₂O₃ coating fully equilibrated with
  LiCoO₂ (forming LiAlO₂, Co₃O₄ and Li₂CoO₃) no longer provides HF-scavenging protection, indicating that the
  protective function of an interphase must be evaluated **after**, not before, interfacial equilibration
  [Aykol 2016, Eqs 5–6]."
- KO: "Aykol 등은 OQMD 의 산소 함유 화합물 13만여 종을 대상으로 hull 안정성 + 리튬화·양이온 용출·HF 공격 반응모델을
  결합해 코팅을 물리장벽 / HF-장벽 / HF-scavenger 로 분류했다."
- KO: "다만 이 프레임워크의 산화측 지표(E_c)는 **액체 전해질로의 양이온 용출** 전위이므로, 고체 전해질의
  grand-potential 산화 한계와는 같은 양이 아니다."
- ⛔ **쓰면 안 되는 문장**: *"Aykol 2016 의 계산에서 LPSCl 보다 안정한 코팅이 …"* — LPSCl 은 이 논문의 후보 공간에 없다.
  *"우리 2.256 V 는 Aykol 의 3.5 V 기준보다 …"* — 두 수는 같은 축이 아니다.

---

## 13. 주의 / 한계 (인용 규율) ⛔

| 값 | 왜 위험한가 | 규율 |
|---|---|---|
| **`E_c` / `−E_c` (V)** | **액체로의 양이온 용출** 전위. NBS 수용액 표준전극전위 + 활동도 10⁻⁶ 에서 온다 | ⛔ **우리 `oxidation_limit_V` 2.256 V 와 같은 표 금지.** 우리 계에 대응물 없음 |
| **`G_s-HF` (eV/HF)** | 우리 계에 HF 가 없다. **#1 의 −ΔH_s-HF 와도 다른 양**(0 K 고립분자 → 298 K 액체 H₂O·희박 HF) | ⛔ 우리 db 어디에도 넣지 않는다. **#1 값과 한 표에 섞는 것도 금지** |
| **`E_d` (V)** | **정의는 우리 환원 한계와 같은 종류**지만, DB(OQMD≠MP)·온도기준(298 K≠0 K)·대상물질이 다르다 | ⚠ **정의 대조까지만.** 값을 우리 1.242 V 옆에 쓰지 않는다 |
| **top-30/top-100 순위** | `F(x)` 해상도가 없다(1위 대비 0.05 이내 64종) | ⚠ **"상위권에 있다" 까지만.** 1위·2위 서열을 논거로 쓰지 않는다 |
| **`Table 2` 목록** | 일반 MOOP 와 **판정 규칙이 다르다**(양극 상대 문턱 + ±0.12 V 버퍼). `Fig. 5` 목록과 같은 성격이 아니다 | ⚠ 인용 시 **어느 규칙의 산물인지 반드시 명시** |
| **"5,225 compounds"** | 행 수. 고유 화학식은 **5,200** | ⚠ CSV 로 통계 낼 때 중복 제거 |
| **HHI** | 물성이 아니라 **공급망 집중도** | 🟢 이식 가능하지만 `canonical_registry.json` 에 **넣지 않는다** |
| **`Fig. 6c` "5–10배"** | 그림에서는 Si ≈6× · B ≈4× | ⚠ 본문 문구 대신 **그림 판독값 + figure-read 표기**로 |
| **`Fig. S4` 캡션** | *"charge potential is emphasized"* 는 그림·수치와 반대 | ⛔ 그 문장을 인용하지 않는다 |

---

## 14. 기법 용어 미니사전

- **OQMD** (Open Quantum Materials Database) — Wolverton 그룹의 고속 DFT 형성에너지 DB(약 30만 종).
  ICSD 실존 상 + **가설 구조**(흔한 구조형에 원소 치환)를 포함하는 것이 특징. Materials Project 와 **다른 DB** 다.
- **convex hull / hull 위** — 어떤 조성에서 가능한 모든 상 조합 중 최저 에너지를 잇는 볼록 껍질.
  그 위에 있으면 "다른 상들로 분해되지 않는다" = 열역학적으로 안정.
- **`[…]_min` (하한 첨자)** — 이 논문의 표기. *"주어진 조성에서 OQMD 상들의 최저에너지 조합"* 을 뜻한다.
  **사람이 반응식을 쓰지 않는다**는 선언. 우리 pymatgen `use_hull_energy=True` 와 같은 발상.
- **δ / α (희박량)** — Li 를 "조금" 넣거나 코팅을 "조금" 얹는 극한. **첫 상영역을 벗어나지 않을 만큼 작은 양**.
  이 극한 덕분에 개시 전압(가장 높은 계단)이 자동으로 잡힌다.
- **E_d / E_c** — 방전(리튬화) 전압 / 충전(용출) 전압. **부호 규약 주의**: E_c 는 음수로 보고하고 게이트는 `−E_c > 3.5 V`.
- **G_s-HF** — HF-scavenging 반응의 자유에너지. **음수 = HF 를 먹는다.** 단위 **eV per HF**(공격 분자 1몰당).
- **과잉 반응성 하한 `G′_s-HF`** — "너무 세게 반응하는" 물질을 빼는 하한. **CaO 의 값(−1.285 eV/HF)** 으로 잡았다.
  (#1 도 CaO 를 상한으로 썼다 — 값만 1.50 → 1.285 로 바뀌었다.)
- **HHI** (Herfindahl–Hirschman Index) — 시장 집중도 지표를 원소 공급에 적용한 것.
  `HHI_R` = 매장량, `HHI_P` = 생산. 클수록 **한 나라에 몰려 있다** = 공급위험 크다. 게이트 < 9,000.
- **MOOP** (multi-objective optimization problem) — 목표가 여러 개이고 서로 충돌해 **단일 최적해가 없는** 문제.
  해는 **Pareto front**(어느 목표도 희생 없이는 못 개선하는 점들의 집합)로 나온다.
- **weighted-sum** — 여러 목표를 `F = Σ wᵢfᵢ` 한 개 점수로 합치는 방법. **간단하지만 가중치와 정규화에 민감**하다.
- **rank aggregation** — 속성별 순위 리스트들을 하나의 "합의 순위" 로 합치는 방법.
  거리 척도는 **Spearman footrule** `Σₓ|rᵃₓ − rᵇₓ|`. 완전탐색이 불가능해 **cross-entropy Monte Carlo** 로 푼다.
- **PCA** (주성분 분석) — 상관된 여러 축을 분산이 큰 소수의 축으로 갈아끼우는 선형 변환.
  여기서는 4속성 → 2축으로 94 % 설명.
- **Pourbaix 형식(Persson 2012)** — DFT 고체 에너지와 **실험 용매화 이온 자유에너지**를 한 사다리에 올려
  수용액 안정 상도를 그리는 방법론. #2 는 이 형식을 **비수계 LIB** 로 옮겼다.

---

## 15. 재현 로그 — **CSV 2본으로 논문의 깔때기·랭킹을 독립 재현** (2026-09-12) ★★

> 목적: ① `Fig. 1` 의 부등호가 **정말 그 수를 만드는지** ② Sup3 가 **weighted-sum 인지 rank-agg 인지**
> ③ 우리가 그 레시피를 **우리 속성으로 갈아끼울 수 있는지**. 전부 `Sup2`(5,225행)에서만 시작했다.

### 15a. 깔때기 재현 — **숨은 필터 1개를 찾았다**

| 단계 | 논문 (`Fig. 1`) | **본 digest 재현** | 판정 |
|---|---|---|---|
| hull 통과 | **5,225** | 5,225 행 (고유 5,200) | ✅ |
| `E_d < 3 V` & `−E_c > 3.5 V` | **2,229** | **2,228** | ✅ (−1) |
| 비방사성 & `HHI_R<9000` & `HHI_P<9000` | **1,315** | **1,314** | ✅ (−1) |
| 물리장벽 | **1,315** | **1,314** | ✅ (−1) |
| HF-barrier `G_s-HF ≥ 0` | **411** | **411** | ✅ **정확 일치** |
| HF-scavenger `−1.285 < G < 0` **만** | **583** | **902** ❌ | 🔴 **안 맞는다** |
| HF-scavenger `−1.285 < G < 0` **+ `E_d(products) < 3 V`** | **583** | **582** | ✅ (−1) |

- 🔑 **결론 ①**: `Fig. 1` 의 HF-scavenger 칸은 **조건이 불완전하다.** 본문이 "HF-scavenger 설계에는
  `E_d(products)` 도 기준으로 포함한다" 고 말한 그 조건이 **흐름도에는 안 그려져 있고, 그 조건이 있어야 583 이 된다.**
- 🔑 **결론 ②**: **게이트 순서가 확정된다** — 전기화학이 HHI/방사성보다 **먼저**다(HHI 를 먼저 걸면 3,276 이 되어
  `Fig. 1` 의 어떤 수와도 안 맞는다). 그리고 HHI 는 **R·P 둘 다** 걸어야 한다(R 만 걸면 4,670 → 수 불일치).
- **−1 의 정체**: 전 단계에 균일하게 나타나므로 **CSV 에서 빠진 화합물 1종**으로 보인다(경계값 후보 없음 —
  `E_d = 3.000`·`−E_c = 3.500`·`HHI = 9000`·`E_d(prod) = 3.000` 인 행이 **하나도 없다**).
  `G = 0` 인 행은 `GeTe₂O₆` 단 하나이고, `G ≥ 0` 으로 잡아야 411 이 맞는다 ⇒ **HF-barrier 조건은 `≥ 0`**.
- **과잉 반응성 하한 `G′` = CaO 의 값 = −1.285 eV/HF** 임을 수치로 확인(CSV 의 `CaO` 행).
  이 하한에 걸려 떨어지는 것은 1,314 중 **단 1종** — ⇒ **사실상 비구속(non-binding) 게이트**다(§10 보강 사실).

### 15b. 랭킹 재현 — **Sup3 = weighted-sum** 확정 + 레시피 확보

**복원한 레시피** (이대로 하면 논문 순위가 나온다):
```
fᵢ(x) = (원값 − min) / (max − min)            ← min/max 는 **전체 5,225종** 에서 잡는다 (걸러낸 풀이 아니다)
        "좋은 쪽" 이 1 이 되도록 뒤집는다:
          E_c        : 낮을수록(더 음수) 좋다   → f = 1 − 정규화값
          E_d        : 낮을수록 좋다            → f = 1 − 정규화값
          E_d(products): 낮을수록 좋다          → f = 1 − 정규화값
          G_s-HF     : HF-scavenger 는 **낮을수록**, HF-barrier 는 **높을수록** 좋다
F(x) = 평균(fᵢ)   (wᵢ 균등)
속성 집합: 물리장벽 {E_c, E_d} · HF-barrier {E_c, E_d, G} · HF-scavenger {E_c, E_d, E_d(prod), G}
```

| 검증 | 결과 |
|---|---|
| 물리장벽 top-100 집합 일치 | **96 / 100** |
| HF-barrier top-100 집합 일치 | **99 / 100** |
| HF-scavenger top-100 집합 일치 | **99 / 100** |
| 본문이 준 개별 순위 | **TiO₂ 139위 ✅ 정확 · ZnO 313위 ✅ 정확 · AlPO₄(물리장벽) 68위 ✅ 정확 · Al₂O₃ 128위 → 재현 127위** (−1, 위의 결측 1종과 일관) |
| `Fig. 5` 상단 3패널의 top-30 순서 ↔ Sup3 1–30행 | **문자 단위 일치** ⇒ **Sup3 = weighted-sum** |

- **정규화 모집단이 순위를 바꾼다(중요)**: min-max 를 **걸러낸 풀**에서 잡으면 top-20 위치 일치가
  물리장벽 1/20 · HF-barrier 5/20 · HF-scavenger 4/20 로 **무너진다**. **전체 5,225** 로 잡아야 11–14/20 이 맞는다.
  ⇒ 우리 cascade 가 점수를 낼 때 **"정규화 모집단" 을 기록하지 않으면 재현 불가**(§11-4).
- **복원한 F(x) 값** (논문에 숫자로 없다): 물리장벽 1위 0.7745 / 30위 0.6663 / 100위 0.6347 ·
  HF-barrier 1위 0.7973 / 30위 0.7251 / 100위 0.6931 · **HF-scavenger 1위 0.5540 / 30위 0.5157 / 100위 0.4926**
  ⇒ §10-3 해상도 비판의 근거.

### 15c. 본문 통계 재현

| 본문 진술 | 본 digest 재현 | 판정 |
|---|---|---|
| *"reaction free energy of LiCoO₂ with HF is more negative than **about 70 %** of candidate coatings"* | `G < −0.871` 인 후보 **30.3 %** ⇒ 더 약한 쪽 **69.6 %** | ✅ |
| *"for LiMn₂O₄ the same number is **about 50 %**"* | `G < −0.493` 인 후보 **50.9 %** ⇒ **49.1 %** | ✅ |
| `Fig. 6c` 전체 5,225 의 물질군 비중 | **O 58.37 % · O–P 6.26 % · O–Si 4.10 % · O–Cl 3.89 % · O–B 3.77 % · O–S 2.76 %** (파란 막대 판독값과 일치) | ✅ |
| `Fig. 2b` 의 `E_d` (figure-read ≈ 0.75 V) | CSV `Li2TiO3 E_d = 0.748` | ✅ |
| `Fig. S4` 캡션 *"charge potential is emphasized"* | f 평균 **E_d 0.735** > E_d(prod) 0.431 > **E_c 0.380** > G 0.274 | ❌ **캡션이 틀렸다** (§10-8) |
| `Table 2` LiCoO₂ 최적 코팅이 일반 MOOP 게이트를 통과하는가 | **전원 `−E_c > 3.5 V` 탈락**(3.185–3.493) | ⚠ **두 분석의 판정 규칙이 다름을 확증** (§3e) |

### 15d. 재현 과정에서 확인한 CSV 사용상 주의 (기계로 쓸 사람용)

1. **화학식 표기가 정규화돼 있지 않다.** 본문 `Li₂SrSiO₄` = CSV `SrLi2SiO4`, 본문 `SrBrOH` = CSV `SrHBrO`,
   본문 `PbHClO` = CSV `HPbClO`. **조성 벡터로 매칭**해야 한다.
2. **본문 `Table 2` 의 일부 물질은 CSV 에 아예 없다**: `Pb₂SO₂` · `Li₂TiGeO₅` · `Ba₂Ti₄Fe₂O₁₄`
   (조성 정규화 후에도 없음). ⇒ `Table 2` 는 CSV 와 **완전히 정합하지 않는다**.
3. **중복 18식 / 초과 25행** — 통계 전 중복 제거 필요.
4. **`E_d = 0` 인 행이 122종** 있다(CaO·BeO 등). 이는 "리튬화가 0 V 에서만 일어난다" = **환원에 매우 강하다** 는 뜻이고
   결측이 아니다.
5. **금속 없는 산화물(SiO₂·B₂O₃·P₂O₅·SO₃)이 목록에 없다** — 후보 정의에 "금속 함유" 가 암묵적으로 들어 있다.

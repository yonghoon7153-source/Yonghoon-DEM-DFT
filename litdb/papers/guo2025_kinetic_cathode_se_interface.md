<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-22 신규 작성. 1저자 지정 읽기축:
       🔴 "이 논문은 우리 방법(0 K hull 평형)을 정면으로 비판한 근거다."
          `wu2026_ml_driven_electrolyte_interface_design_review` §4.3 이 이 편을 근거로 대고
          *"계면 열화의 속도와 최종 형태는 열역학 구동력만이 아니라 운동학 인자에 의해 더 지배된다"* 라고 썼다.
       ⇒ 이 digest 의 1번 임무는 **그 문장이 원문의 무엇에 근거하는지 확인하고, 우리한테 유효한지 판정**하는 것이다.
          리뷰가 과장했을 수도 있고 정확할 수도 있다 — 둘 다 가능하다고 보고 읽었다. 결론은 §3.
       ⇒ 불리한 것을 먼저 적고(§3·§9·§13a), 방어 가능한 자리를 그 다음에 적는다(§13b). 순서를 바꾸지 않았다.
     크로핑 7장(그림 6 + 표 1) 중 **그림 6장 전부 + SI 페이지 렌더 8장을 실제로 봤다** — 목록은 §0b. -->

# Kinetic analysis of cathode–solid electrolyte interface in all-solid-state batteries — X. Guo (*J. Mater. Chem. A* **13**, 38919–38927, 2025)

> slug `guo2025_kinetic_cathode_se_interface` · DOI `10.1039/d5ta07200j` · type `MLIP-MD (MACE-MP-0 · LAMMPS) + AIMD 검증` · PDF `litdb/inbox/126. JMaterChemA_2025_Guo_Kinetic_analysis_cathode_SE_interface_ASSB_MAIN.pdf` (본문 **9 pp** · Fig 1–6 · Table 1 · refs **43**) + SI 2 종(`126. Sup1)` 9 pp = Table S1–S3 · Fig S1–S4 / `126. Sup2)` 10 pp = Fig S5–S13 + refs 7) · digested `2026-09-22` · status ✅ · 태그 **[외부·계산 100 %]**

> elements: Li, Co, O, P, S, Ge, Y, Cl, In, La, Zr, Ti
> methods: DFT, AIMD, MD, MLIP

> ⛔ **이 논문에는 임피던스 측정이 한 건도 없다.** `EIS`·`DRT`·`등가회로`·`Ω cm²` 가 전문에 **0회**다.
> "impedance" 는 **동기와 해석의 언어**로만 15회 나오고, 계산된 임피던스 값은 없다. §3c·§12-①
> ⛔ **실험 0건 · 단독저자 · 공저 검증 없음.** SI 에 캡션 뒤바뀜 2건(Fig S4↔S5)·본문↔SI 수치 불일치 2건이 남아 있다.
> ⛔ **문헌 수치는 소환값이다.** `db/properties/*` 와 같은 표에 놓지 않는다. 우리 계(Li₆PS₅Cl)는 **이 논문의 계면 6종에 없다**
> (SI Table S1 의 **0 K 격자 벤치마크에만** 한 줄 등장하고, 300 K 표 S2 에도 없고 MD 도 안 돌렸다 — §4c).
> ✅ **talk 역링크 점검함**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `lee2026_skku_mlip_materials_design.md`
> 하나뿐이고 **이 논문은 그 대기열(#1–#9)에 없다**. ⇒ 역링크 작업 없음.

> **저자**: **Xingyu Guo\*** (**단독저자**) · Department of **Data Science**, City University of Hong Kong, Kowloon, Hong Kong
> 교신 `xingyguo@cityu.edu.hk` · 접수 **2025-09-03** / 수락 **2025-10-22** / 온라인 2025-10-23
> ⚠ **연구비·감사 절이 없다.** 이해충돌 "없음". Data availability = "SI 가 전부" (**궤적·입력파일 공개 없음** — §12-⑨)

---

# 0a. 이 digest 를 읽는 법

이 편은 **9 쪽짜리 단독저자 계산 논문**이다. 그 자체로는 litdb 의 큰 편이 아니다.
digest 가 긴 이유는 하나다 — **이 편이 우리 §B(계면 반응성)·§2b(보호율)의 방법론적 정당성을
겨누는 인용의 원전**이기 때문이고, 그러면 *"그 인용이 원문에서 무엇에 근거하는가"* 를
문장 단위로 확인해야 하기 때문이다.

그래서 이 digest 의 본체는 두 개다:

1. **§3 — 리뷰가 옮긴 3건을 원문과 대조한 결과** (정확 1 · 과장 1 · **없는 것 1**).
2. **§12 — 이 논문 자체의 방법론 감사.** 우리를 때리는 근거가 얼마나 단단한지는
   그 논문이 얼마나 단단한지에 달려 있다. 결과는 **꽤 무르다** — 특히 유일한 정량 축(Fig 2 / Table S3)이
   **혼합 평균 인공물**로 설명된다(§12-②). 그러나 **정성 관측(Fig 3–6)은 살아남고, 그 부분은 우리한테 유효하다.**

⚠ **결론을 미리 적는다 (§13 의 요약)**: 리뷰의 인용은 **부분적으로만 옳고**, 원문은 우리가 걱정한 것보다
**덜 치명적이며 오히려 hull 열역학을 세 군데서 명시적으로 추인**한다. 하지만 **우리 §H(못 하는 것) 목록은
줄지 않는다** — 속도·두께·연속성·Li 고갈·양이온 상호확산은 여전히 0 이고, 이 논문은 **그 5개 중 3개를
실제로 보여 준다**. 즉 *"비판은 약해졌지만 공백은 그대로다."*

# 0b. ★ 본 그림 / 안 본 그림 (정직 목록)

| 무엇 | 본 것 | 안 본 것 |
|---|---|---|
| **본문 그림 6장** | **Fig. 2 · Fig. 3 · Fig. 4 · Fig. 5 · Fig. 6** (5/6) | `Fig. 1`(모델 도식) — 본문·캡션이 기하를 전부 문장으로 적어서 생략. §4a 는 텍스트 근거다 |
| **본문 표** | `Table 1` — PDF 텍스트로 읽음(이미지보다 정확) | — |
| **SI 1 (9 pp)** | p1 표지 · p2 MACE 검증 산문 · **p3 `Table S1`** · **p4 `Table S2`** · **p5 `Table S3`** · p6 `Fig. S1` · p8 `Fig. S3` · p9 `Fig. S4` | p7 `Fig. S2`(총에너지, 나머지 6계 — S1 과 동종이라 생략) |
| **SI 2 (10 pp)** | p1 `Fig. S5` · p2 `Fig. S6` · p3 `Fig. S7` · p10 참고문헌 | **p4–p9 = `Fig. S8`–`Fig. S13` 의 대부분** (RDF 참조화합물 묶음 S8–S12) — 단 **p9 `Fig. S13`(산화물/방전 계면)은 봤다** |
| **크로핑 도구** | `tools/litdb/extract_figures.py --slug guo2025_kinetic_cathode_se_interface` → 7장 (본문 6 + 표 1). **SI 는 크로핑이 안 됐다** — SI PDF 는 **텍스트가 벡터 아웃라인**이라 캡션 앵커가 없다(추출 0자) ⇒ 페이지를 통째로 렌더해 읽었다 | |

> 그림에서만 읽은 값은 전부 **`figure-read ≈`** 로 표시했다. `Table S3` 에 있는 값은 표 값을 쓴다
> (내 figure-read 와 `Table S3` 를 8개 항목에서 대조했고 **전부 ±10 % 안에서 일치**했다 — §7a 각주).

---

# 1. 한 줄 요약

**단독저자가 범용 MLIP(MACE-MP-0)로 LiCoO₂(101)‖SE 계면 6종 × 충·방전 2상태 = 12계를 300 K · 1 ns NpT-MD 로
돌려, 양극/SE 계면 임피던스를 낳는 운동학 기전 3가지 — (1) 계면 반응(황화물), (2) Li 고갈층, (3) 양이온 상호확산 —
을 "직접 관측했다" 고 주장한다.** 결론 문장은 *"열역학 예측만으로는 계면 안정성을 평가하기에 불충분하다"* 이고,
그것이 이 편이 인용되는 이유다. **그러나 임피던스는 한 번도 계산되지 않았고, 반응속도도 최종상태도 측정되지 않았으며
(에너지가 1 ns 에서 아직 내려가는 중이다), 정량 축은 혼합 평균 인공물로 설명된다.**
살아남는 것은 **정성 기전 3개의 존재 증명**이고 — 그것만으로도 우리 §H 공백을 정확히 겨눈다.

# 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Xingyu Guo** (단독) |
| 소속 | City University of Hong Kong, **Department of Data Science** (재료·화학과가 아니다) |
| 저널 / 연 | *J. Mater. Chem. A* **13**, 38919–38927 (**2025**) · RSC |
| DOI | `10.1039/d5ta07200j` |
| 계 (양극) | **Li_xCoO₂ (101)**, x = **0.5**(충전) / **1.0**(방전) — ⛔ NMC·LiNiO₂ 없음 |
| 계 (SE) 6종 | **황화물** Li₁₀GeP₂S₁₂(LGPS)(011) · Li₇P₃S₁₁(LPS)(100) / **염화물** Li₃YCl₆(LYC)(100) · Li₃InCl₆(LIC)(010) / **산화물** Li₇La₃Zr₂O₁₂(LLZO)(110) · Li₀.₃₃La₀.₅₆TiO₃(LLTO)(100) |
| 연구유형 | **계산 100 %** (MLIP-MD 본체 + 소규모 AIMD 검증). **실험 0건 · 임피던스 측정 0건** |
| 규모 | nat **656–1320** · **1 ns** · 300 K · 단일 궤적 |
| 분량 | 본문 9 pp · 그림 6 · 표 1 · refs 43 · SI 19 pp(2 파일) |

# 3. 🔴 1번 임무 — **리뷰가 옮긴 것이 원문과 맞나**

`wu2026_ml_driven_electrolyte_interface_design_review` 가 이 편([132])을 근거로 세 가지를 주장했다.
셋을 원문과 한 줄씩 대조했다. **하나는 정확하고, 하나는 강화됐고, 하나는 원문에 없다.**

## 3a. ✅ **임피던스 3기전 — 리뷰가 정확하다** (거의 축자 번역)

리뷰: *"양극/SE 계면 임피던스는 세 운동학 기전으로 분해된다 — 저전도 계면상 형성 · **Li 고갈 영역** · 양이온 상호확산."*

원문 **Abstract**:
> *"Our simulations reveal three primary kinetic mechanisms driving impedance: (1) **interfacial reactions**, especially
> with sulfide SEs, **forming poorly conducting interphases**; (2) the formation of **lithium-depleted regions** that
> reduce available Li⁺ pathways; and (3) **cation inter-diffusion**, which obstructs lithium transport channels and
> degrades the cathode."*

원문 **Discussion** (같은 3분법을 번호 달아 반복):
1. **Interfacial reactions** — 황화물이 충전 Li₀.₅CoO₂ 와 반응해 **황·인·각종 산화물**을 포함한 계면상을 만든다.
   *"Most of these byproducts are **poor ionic and electronic conductors**"*. 단서 하나: **Li₃PO₄** 는
   *"전자절연이면서 이온전도"* 라 **부동태화 가능성**이 있다 (ref 43).
2. **Lithium depletion** — *"a lithium-depleted region, **also known as a space-charge layer**, forms at the interface."*
   두 경로: ① **전기화학 퍼텐셜 불일치**로 SE → 충전 양극의 공공으로 Li⁺ 이동 ② 양극 표면 **흡착**.
   결과: Li⁺ 경로 수 감소 + **활성 Li 의 비가역 손실**(용량 감소).
3. **Cation inter-diffusion** — SE 양이온이 Li₀.₅CoO₂ 의 **Li 층으로** 확산 + 양극 표층의 **Co 이동**.

### 🔑 각 기전이 **어떤 관측량으로 분리되나** (1저자 질문)

| 기전 | 원문에서의 관측량 | 분리 가능한가 |
|---|---|---|
| ① 계면 반응 | **RDF 시간전개 히트맵** r(S–S) · r(P–P) (`Fig. 4c,d`) + 원소 z-프로파일의 **무질서화** (`Fig. 4a,b`) | 🟡 **부분.** 종 동정이 **MP 참조화합물 RDF 와의 눈대중 일치**뿐 (§12-③) |
| ② Li 고갈 | **Li 수 밀도 z-프로파일**의 t=0 vs t=0.9–1.0 ns 비교 (`Fig. 3`) | 🟢 **된다.** 이게 이 논문에서 제일 깨끗한 관측이다 |
| ③ 양이온 상호확산 | **원소별 z-프로파일 겹침** + 1 ns 후 스냅샷 (`Fig. 4a,b`·`Fig. 5`·`Fig. 6`) | 🟡 **정성.** 확산계수·개수·깊이를 **하나도 수치화하지 않았다** |

⇒ **세 기전은 서로 다른 관측량으로 분리되기는 한다. 그러나 임피던스로는 아무도 환산되지 않는다** —
"impedance" 는 세 기전의 **이름표**일 뿐이고, 어느 기전이 얼마를 기여하는지는 논문 어디에도 없다.

## 3b. ⛔ **"운동학이 열역학보다 더 지배한다" — 리뷰가 강화했다**

| | 문장 | 어디 |
|---|---|---|
| **리뷰** | *"계면 열화의 **속도와 최종 형태**는 열역학 구동력만이 아니라 **운동학 인자에 의해 더 지배된다**"* | wu2026 §4.3 |
| **원문(초록)** | *"While thermodynamic analyses offer stability insights, they **overlook the kinetic effects that dominate during operation**."* | Abstract 2행 |
| **원문(서론)** | *"While effective at describing equilibrium phenomena, these thermodynamic approaches **inherently neglect the kinetic processes** that govern interfacial degradation during battery cycling."* | Intro |
| **원문(결론)** | *"This study underscores that **thermodynamic predictions alone are insufficient** for assessing interfacial stability and highlights the **critical role of kinetics**."* | Conclusion |

**판정: 리뷰는 원문의 수사를 한 단계 올렸다.**

- ✅ *"열역학만으로는 불충분"* — **원문에 그대로 있다.**
- 🟡 *"운동학이 지배한다"* — 원문 **초록에 "dominate" 가 있다**. 단 그것은 **결과가 아니라 서론적 주장**이고,
  결론절에서는 "critical role" 로 톤이 내려간다.
- ⛔ *"**속도와 최종 형태**"* — **원문에 없다.** 그리고 **원문이 그것을 잴 수 없다**:
  - **속도**: `rate` 라는 단어가 논문 전체에서 **승온율 0.25 K fs⁻¹ 한 번**만 쓰인다. **시간법칙 적합 0 · 온도열 0 ·
    활성화에너지 0 · 반응 진행도 정의 0.** 300 K 단일 온도다.
  - **최종 형태**: `Fig. S1` 의 총에너지가 **Li₀.₅CoO₂/Li₇P₃S₁₁ 에서 1 ns 끝까지 단조 감소 중**이다
    (figure-read ≈ −5.062 → −5.090 eV/atom, **마지막 100 ps 에도 기울기가 살아 있다**).
    `Fig. S3` 의 부피도 같은 계에서 **계속 팽창**한다 (figure-read ≈ 16.0 → 16.5 Å³/atom).
    ⇒ **반응이 안 끝났다. "최종 형태" 를 말할 자격이 이 계산에는 없다.**

> ⚠ **우리가 이번 묶음에서 여러 번 본 2차 인용 왜곡이 여기서도 나왔다.**
> 원고·발표에서 이 문장을 쓸 때는 **리뷰가 아니라 원문 문장**(*"thermodynamic predictions alone are insufficient"*)을 쓴다.
> *"속도와 최종 형태"* 는 **인용하지 않는다** — 원전이 그것을 재지 않았다.

## 3c. ⛔⛔ **"코팅 4조건" — 원문에 없다**

리뷰: *"성공적인 계면 코팅은 네 조건을 **동시에** 만족해야 한다 — 분해의 열역학 구동력 제거 · Li 수송경로 보존 ·
양이온 상호확산 차단 · 전자절연 유지."* (§4.6, **원전 [132] Guo** 로 표기)

**원문 검색 결과** (`grep -i` 전문):

| 단어 | 출현 |
|---|---|
| `coating` / `coat` | **0회** |
| `buffer` / `interlayer`(완충층 뜻) | **0회** (`interlayer migration of Co` 1회 = 양극 층간 이동, 다른 뜻) |
| `design rule` / `criteria` | **0회** |

**Guo 는 코팅을 한 번도 논하지 않는다.** 이 논문에 코팅 계도, 코팅 조건도, 설계 규칙 목록도 없다.

**그럼 리뷰의 4조건은 어디서 왔나** — 재구성하면 이렇다:

| 리뷰의 조건 | Guo 의 대응 문장 | 성격 |
|---|---|---|
| 분해 구동력 제거 | 기전 ①(계면 반응)의 **역** | 리뷰의 추론 |
| **Li 수송경로 보존** | 기전 ②(Li 고갈이 *"reduce available Li⁺ pathways"*)의 **역** | 리뷰의 추론 |
| 양이온 상호확산 차단 | 기전 ③의 **역** | 리뷰의 추론 |
| **전자절연 유지** | Discussion 의 Li₃PO₄ 단서 — *"an **electronically insulating but ionically conductive** material, could potentially passivate and stabilize the interface"* | **유일하게 원문 근거가 있는 칸** |

⇒ **리뷰가 Guo 의 3기전을 뒤집어 코팅 사양으로 재서술한 것**이고, 그 자체는 합리적 종합이지만
**"[132] Guo" 로 귀속한 것은 사실과 다르다**. 원고에서 4조건을 쓰려면 **리뷰를 인용**하거나
**우리 문장으로 다시 쓰고 Guo 는 3기전에만 붙인다.**

## 3d. ⭐ **그래서 hull 열역학은 무용이라 하나** — **아니다. 세 군데서 명시적으로 추인한다**

이게 1저자 질문 4번이고, **우리 방어 문장이 여기서 나온다.** Guo 는 열역학을 **버리지 않고 쓴다**:

| # | 원문 | 무엇을 뜻하나 |
|---|---|---|
| **1** | *"The formation of **S_n in the highly charged state agrees with previous thermodynamic analysis**."* (refs **9 = Zhu 2015** · **40 = Zhu 2016**) | **황화물 계면 산물 예측에서 MD 가 hull 열역학과 일치**한다고 스스로 적는다. ⚠ ref 9 = 우리 `zhu2015_esw_grand_potential_origin` digest 의 그 논문이다 |
| **2** | *"This is **in line with both thermodynamic analysis and experimental observations** that both Li₃YCl₆ and Li₃InCl₆ exhibit high electrochemical stability toward LiCoO₂ cathode **up to 4.2 V**."* (refs 4·6·41) | **염화물 고전압 안정성**에서도 MD = 열역학 = 실험 **3자 일치** |
| **3** | *"the **reaction energies** between Li₃YCl₆ and LiCoO₂, and between Li₃InCl₆ and LiCoO₂, are **23 meV per atom** and **21 meV per atom**, respectively, **indicating high chemical stability**."* | **자기 결론의 근거로 계면 반응에너지(= 우리가 쓰는 바로 그 양)를 든다.** ⚠ 출처 표기 없음 — 자체 계산 추정 |
| (+) | `Fig. 4c,d` 의 참조 RDF = *"retrieved from the **Materials Project** for phases with **energy above hull less than 20 meV per atom**"* | **종 동정의 후보 집합 자체를 MP hull 로 자른다.** hull 없이는 이 논문의 §"Interfacial reaction" 절이 성립하지 않는다 |

> **🔑 판정: Guo 의 주장은 "hull 을 버려라" 가 아니라 "hull 로는 *언제·얼마나·어떤 모양으로* 를 못 본다" 이다.**
> 그리고 **그가 하는 종 동정·안정성 판정은 hull 위에 서 있다.** 즉 그의 논문 자신이
> **"hull 은 필요조건이지 충분조건이 아니다"** 의 실례다. 우리 방어 문장의 원문 근거는 §13b.

---

# 4. DFT / 계산 방법 ★ (전량)

## 4a. 계면 모델 구축

| 항목 | 값 |
|---|---|
| 양극 | **Li_xCoO₂**, 벽개면 **(101) 또는 (1̄01)** — Wulff 구성의 저에너지 면이고 Li 확산 채널이 열려 있다 (refs 7·13) |
| SE 슬랩 배향 | **격자변형 최소화** + **MCIA(minimal coincident interface area) < 400 Å²** 조건으로 선택 (ref 18 Ding 2016) |
| 격자 정합 알고리즘 | **Zur–McGill** (ref 19, *J. Appl. Phys.* **55**, 378 (1984)) |
| 슬랩 두께 | 계면 수직축 전체 길이 **> 50 Å** (벌크 유사 영역 확보) |
| 초기 간격 | **2.5 Å** |
| 종단 2종 | **region A = LiCoO₂-종단 (`P2m2`)** · **region B = Li-종단 (`C2m1`)** ⚠ 기호는 PDF 표기 그대로. 평면군 `p2mm`/`c2mm` 의 오식으로 보이나 **원문 확인 불가** — 인용 시 그대로 옮기지 말 것 |
| 주기성 | 셀 안에 **A·B 두 계면이 동시에** 들어간다 (SE‖양극‖SE 샌드위치) ⇒ 한 궤적에서 **종단 2종을 동시에** 본다 |

### `Table 1` — 계면 모델 제원 (**PDF 텍스트 직독**)

| 계면 | nat (x=0.5) | nat (x=1.0) | Strain | MCIA (Å²) |
|---|---|---|---|---|
| Li_xCoO₂(101)/**LGPS**(011) | 1004 | 1076 | 0.011 | 381.87 |
| Li_xCoO₂(101)/**Li₇P₃S₁₁**(100) | 1092 | 1176 | 0.018 | 290.01 |
| Li_xCoO₂(101)/**Li₃YCl₆**(100) | 1260 | 1320 | 0.005 | 276.20 |
| Li_xCoO₂(101)/**Li₃InCl₆**(010) | 824 | 896 | 0.010 | 317.58 |
| Li_xCoO₂(101)/**LLZO**(110) | 1049 | 1116 | 0.013 | 239.00 |
| Li_xCoO₂(101)/**LLTO**(100) | 656 | 704 | 0.015 | 270.49 |

⚠ **변형률 0.005–0.018 (0.5–1.8 %)** — 낮게 유지했다. 이건 잘한 부분이다.

## 4b. MD 사양 (본체)

| 항목 | 값 | 우리 규약과 대조 |
|---|---|---|
| **퍼텐셜** | **MACE-MP-0** (ref 22, arXiv:2401.00096 = foundation model 원판) | 우리는 **UMA-s-1p1(omat)**. ⚠ MACE-MP-0 는 **MPtrj 학습 1세대**로, 후속 벤치에서 과도한 평활화(soft PES)가 지적돼 온 모델이다 |
| **엔진** | **LAMMPS** (ref 27) | 우리는 ASE |
| **앙상블** | **NpT** (Parrinello–Rahman, refs 20·21) — **부피·셀 형상 모두 자유** | 우리는 **Langevin NVT** |
| **온도** | **300 K 단 하나** | 우리는 600/800/1000 K 아레니우스 3점 |
| **승온** | 0 K → 300 K, **0.25 K fs⁻¹** | — |
| **평형화** | **≥ 30 ps** (에너지·부피 수렴, `Fig. S1–S3`) | 우리 5 ps |
| **생산** | **≥ 1 ns**, dt **1 fs** | 우리 200 ps (단 온도가 훨씬 높다) |
| **전기장 / 전위** | ⛔ **없다.** *"carried out **without an applied electric field**, focusing on the intrinsic kinetic stability … through the spontaneous transport of Li⁺"* | 우리 grand-potential 은 μ_Li 를 전압으로 준다 — **층위가 다르다**(§9) |
| **충전 상태 구현** | **Li 화학량론만** (x = 0.5 vs 1.0). 전자 보상·전하 상태 없음 | — |
| **시드 / 반복** | ⛔ **없다. 계당 단일 궤적, 오차막대 0** | 우리 modelc 3-seed 0.197 ± 0.032 eV |
| **D 정의** | `D = ⟨Δr(t)⟩²/(2dt) = MSD/(2dt)`, **d = 3** | ⚠ **적합창을 안 밝혔다.** 식 형태가 **원점 통과 단일점 추정**이다. 우리 규약은 **MSD 창 2–50 ps 고정 + 자유절편** |
| **"계면" D 의 정의** | 🔴 *"The Li⁺ diffusivity across the cathode/SE interface is calculated from the **MSD of all Li⁺ ions within the entire simulation cell**."* | 🔴 **여기가 이 논문 최대의 약점이다 — §12-②** |

## 4c. AIMD 검증 (SI 전용)

| 항목 | 값 |
|---|---|
| 코드 | **VASP** (ref SI-1 Kresse 1996) · **PAW** · **PBE** |
| k-점 | **Γ 점 1개** |
| dt | **2 fs** |
| 스핀 | **비스핀분극** — *"a necessary approximation to ensure the AIMD simulations can be performed at a reasonable cost"* ⚠ **Co³⁺/Co⁴⁺ 산화물에서 비스핀분극은 강한 근사**다 |
| +U | 본문은 *"PBE + U"* 라 쓰고 (refs 23–25, **Wang–Maxisch–Ceder**), **U 값을 안 적었다** ⚠ |
| 300 K 평균 | **30 ps NpT MD 의 마지막 10 ps 평균** |

### 🔴 격자 벤치마크 — **본문 주장과 SI 표가 어긋난다**

본문: *"deviations remaining **below 5 %** at both 0 K and 300 K (see Tables S1 and S2)."*

`Table S2` (300 K, MACE vs DFT) 의 실제 값:

| 물질 | a (%) | b (%) | c (%) | **부피 (%)** |
|---|---|---|---|---|
| LiCoO₂ | +0.76 | +1.05 | −2.33 | +3.54 |
| Li₀.₅CoO₂ | −2.48 | −2.48 | **+4.07** | −1.87 |
| LLTO | −1.82 | +1.97 | −2.65 | −2.51 |
| LLZO | −0.49 | +0.04 | +0.20 | −0.36 |
| Li₇P₃S₁₁ | −0.58 | +0.48 | −1.12 | −0.69 |
| LGPS | −0.78 | −0.22 | −0.46 | −1.50 |
| **Li₃YCl₆** | −2.67 | −3.62 | −2.89 | 🔴 **−7.95** |
| **Li₃InCl₆** | 🔴 **−18.89** | −2.16 | 🔴 **+5.06** | +2.26 |

⇒ **"below 5 %" 는 거짓이다.** 3개 항목(Li₃InCl₆ a −18.89 % · c +5.06 % · Li₃YCl₆ 부피 −7.95 %)이 넘는다.

SI 는 이를 **스스로 자백하고 변호**한다:
> *"We note that **despite the significant errors observed in simulating Li₃InCl₆ at 300 K**, the lattice parameters
> predicted by MACE (a = 6.78, b = 11.63, c = 6.6 Å) is **closer to experimental results** (a = 6.41, b = 11.08, c = 6.39 Å)
> than those obtained from DFT calculations (a = 8.36, b = 11.88, c = 6.28 Å)."* (실험 = ref SI-4 Molaiyan 2023)

⚠ **그런데 이 변호는 검증의 성립을 무너뜨린다** — 기준(DFT, a = 8.36 Å)이 실험(6.41 Å)에서 **+30 %** 벗어나 있으면
그 기준으로는 아무것도 검증할 수 없다. 0 K DFT 는 a = 6.63 Å 이었으므로 **30 ps Γ-점 비스핀 AIMD 가 6.63 → 8.36 Å 로
26 % 팽창**한 것이다 — 그 AIMD 가 깨졌다는 뜻이다. ⇒ **Li₃InCl₆ 계면(2계)은 어느 쪽 300 K 기준도 없이 돌아갔다.**

### `Table S1` (0 K, MACE vs DFT) — 여기는 훨씬 좋다

| 물질 | a/b/c 오차 (%) | 부피 오차 (%) |
|---|---|---|
| LiCoO₂ | −0.15 / −0.15 / **+2.35** | +2.04 |
| Li₀.₅CoO₂ | −2.48 / −2.48 / **+4.07** | −1.26 |
| LLTO | −1.24 / −0.99 / +0.42 | −1.81 |
| LLZO | −0.15 / +0.18 / −0.38 | −0.36 |
| Li₇P₃S₁₁ | **−3.66** / +1.88 / +1.32 | −0.69 |
| LGPS | +0.16 / +0.33 / −0.7 | −0.25 |
| ⭐ **Li₆PS₅Cl** | **−0.16 / +0.05 / +0.1** | ⭐ **+0.05** |
| Li₃YCl₆ | +0.56 / +0.21 / −0.19 | +0.56 |
| Li₃InCl₆ | +0.26 / +0.8 / +0.47 | +1.47 |

> ⭐⭐ **우리 계가 여기 있다.** **Li₆PS₅Cl 은 이 표에서 MACE-MP-0 오차가 가장 작은 물질**이다
> (DFT a/b/c = 10.13 / 9.81 / 9.90 Å · MACE = 10.11 / 9.82 / 9.91 Å · **부피 오차 0.05 %**).
> ⛔ **그런데 계면 6종에 Li₆PS₅Cl 은 없다.** 벤치마크만 하고 안 돌렸다 — 왜인지 논문은 말하지 않는다.
> ⛔ 그리고 `Table S2`(300 K)에도 **Li₆PS₅Cl 이 없다.** ⇒ **우리 계의 300 K MACE 신뢰도는 이 논문에서 답이 안 나온다.**

### 계면에너지 정확도의 유일한 근거

> *"The ability of the MACE model to accurately predict interface energies is further supported by the work of **Xie et al.**,
> who reported a **mean absolute error of 0.79 J m⁻²** relative to DFT results."* (ref 26 = **InterOptimus**, *J. Energy Chem.* **106**, 631 (2025))

🔴 **0.79 J m⁻² 는 "정확하다" 는 근거가 못 된다.** 같은 InterOptimus 데이터를 우리 `wu2026…` digest §11c 가
`Fig. 11` 에서 읽었는데 **ORB/SevenNet 의 MAE 는 0.1–0.61 J m⁻²** 였고, 그중 최악(LiF|NCM ORB 0.61)보다도
이 값이 크다. 그리고 계면형성에너지의 전형적 크기가 **O(0.1–1 J m⁻²)** 이므로 **MAE 가 신호와 같은 자릿수**다.
⇒ **이 논문은 계면에너지를 보고하지 않으므로 직접 피해는 없지만, "MACE 가 계면을 잘 한다" 는 문장의 근거는 없다.**

---

# 5. 핵심 수치 — **소환값 전량** (⛔ 우리 `db/properties/*` 와 같은 표에 놓지 말 것)

## 5a. ⭐ `Table S3` — Li⁺ 확산계수 전표 (SI p5, **표 직독**)

> **주의**: `Overall D` = 셀 전체 Li 의 등방 MSD. `D_z` = z 축(계면 수직) 성분. **`Fig. 2` 가 그리는 것은 `D_z` 열이다.**
> **"(ref N)" 이 붙은 3개 값은 실험 문헌값**이고 나머지는 MACE-MD 값이다 — **한 축에 섞여 있다**(§12-②).

| 물질 또는 계면 | Overall D (cm² s⁻¹) | **D_z** (cm² s⁻¹) | 계면/벌크 D_z 비 |
|---|---|---|---|
| **Li₁₀GeP₂S₁₂** (벌크) | 6.20 × 10⁻⁷ | 2.99 × 10⁻⁷ | — |
| Li₀.₅CoO₂/LGPS | 4.16 × 10⁻⁷ | 1.50 × 10⁻⁷ | **0.50** |
| LiCoO₂/LGPS | 1.33 × 10⁻⁷ | 6.00 × 10⁻⁸ | **0.20** |
| **Li₇P₃S₁₁** (벌크) | 3.00 × 10⁻⁶ | 5.95 × 10⁻⁷ | — |
| Li₀.₅CoO₂/Li₇P₃S₁₁ | 5.90 × 10⁻⁷ | 2.53 × 10⁻⁷ | **0.43** |
| LiCoO₂/Li₇P₃S₁₁ | 1.95 × 10⁻⁷ | 7.14 × 10⁻⁸ | **0.12** |
| **Li₃YCl₆** (벌크) | 6.07 × 10⁻⁷ | 2.18 × 10⁻⁷ | — |
| Li₀.₅CoO₂/Li₃YCl₆ | 1.17 × 10⁻⁶ | 4.70 × 10⁻⁷ | 🔺 **2.16** |
| LiCoO₂/Li₃YCl₆ | 1.96 × 10⁻⁷ | 9.43 × 10⁻⁸ | **0.43** |
| **Li₃InCl₆** (벌크) | 4.05 × 10⁻⁷ | 3.12 × 10⁻⁷ | — |
| Li₀.₅CoO₂/Li₃InCl₆ | 6.98 × 10⁻⁷ | 2.24 × 10⁻⁷ | **0.72** |
| LiCoO₂/Li₃InCl₆ | 4.23 × 10⁻⁷ | 7.83 × 10⁻⁸ | **0.25** |
| **LLZO** (벌크) | **5.00 × 10⁻⁹ (ref 5 = 실험)** | – | — |
| Li₀.₅CoO₂/LLZO | 1.39 × 10⁻⁶ | 2.69 × 10⁻⁷ | 🔺 **53.8** |
| LiCoO₂/LLZO | – | – | **측정 불가** |
| **LLTO** (벌크) | **9.20 × 10⁻⁸ (ref 6 = 실험)** | – | — |
| Li₀.₅CoO₂/LLTO | 2.00 × 10⁻⁶ | 7.46 × 10⁻⁷ | 🔺 **8.1** |
| LiCoO₂/LLTO | – | – | **측정 불가** |
| **Li₀.₅CoO₂** (양극) | – | **1.1 × 10⁻⁶** | — |
| **LiCoO₂** (양극) | – | **1.6 × 10⁻¹² (ref 7 = 실험)** | — |

> ⚠ **SI ref 5/6/7** = Hasegawa 2023 PFG-NMR(LLTO) · **Brugge 2021 FIB-SIMS 동위원소교환(LLZO)** · Uxa 2023(LiCoO₂).
> ⚠ **본문↔표 불일치 2건**:
> ① 본문 *"Our calculated diffusivity for the charged cathode (Li₀.₅CoO₂) is **∼8 × 10⁻⁷**"* vs `Table S3` **1.1 × 10⁻⁶** (**1.4배 차이**).
>   `Fig. 2` 의 막대는 **표 쪽과 맞는다** ⇒ 본문 숫자가 이상값이다.
> ② 본문 *"For sulfide and chloride SEs, the interfacial Li⁺ diffusivities are in the range of **6–7 × 10⁻⁸**"* vs
>   실제 표 값 **6.00 / 7.14 / 9.43 / 7.83 × 10⁻⁸** ⇒ 실제 범위는 **6.0–9.4 × 10⁻⁸**.

## 5b. 열역학 값 (Guo 가 **자기 결론의 보강으로** 든 것)

| 양 | 값 | 비고 |
|---|---|---|
| 반응에너지 Li₃YCl₆ + LiCoO₂ | **23 meV atom⁻¹** | ⚠ **출처 표기 없음** — 자체 계산으로 추정 |
| 반응에너지 Li₃InCl₆ + LiCoO₂ | **21 meV atom⁻¹** | 같음 |
| 염화물 대 LiCoO₂ 전기화학 안정 상한 | **4.2 V** | refs 4(Asano 2018)·6(Wang/Mo 2019)·41(Park/Nazar 2020) — **문헌 소환** |
| MP 참조상 선별 기준 | **e_above_hull < 20 meV atom⁻¹** | `Fig. 4c,d` 의 참조 RDF 후보 집합 |

## 5c. 관측된 반응 생성종 (RDF 기반 **정성** 동정)

| 계면 | 종 | 판별 근거 | 시간창 |
|---|---|---|---|
| Li₇P₃S₁₁ · LGPS / **Li₀.₅CoO₂** | **S_n**, **P₂S₇** | r(S–S) 최소 **≈ 2 Å** 피크 | **t = 0 부터** 존재 |
| Li₇P₃S₁₁ · LGPS / **LiCoO₂** | 같은 종 | 같은 피크, **세기 훨씬 약함** (`Fig. S8a`) | — |
| **Li₇P₃S₁₁**/Li₀.₅CoO₂ | **P_xS_yO_z** | r(P–P) **≈ 3 Å** 피크 | **t = 0.1 → 0.8 ns** |
| Li₇P₃S₁₁/LiCoO₂ | **P_xS_yO_z** | 같은 피크 | **t = 0.6 → 0.7 ns** (훨씬 짧다) |
| **LGPS**/Li₀.₅CoO₂ | **Li₃P**, **Li₃PO₄** | r(P–P) 벌크 피크(5–6 Å)가 **t ≈ 0.3 ns 에 분열** → 4–7 Å 새 피크 | t ≥ 0.3 ns |
| LGPS/LiCoO₂ | **없음** — 벌크 피크가 1 ns 내내 유지 | — | — |
| 모든 계면 | ⛔ **P_n 없음** (r(P–P) < 3 Å 밀도 무시할 수준) | — | — |
| **Li₃InCl₆**/Li₀.₅CoO₂ | **In_xCl_y** (저배위 양이온 부동태화) | `Fig. S9–S12` | — |
| 염화물 전반 | ⛔ **기상종 없음** — O₂ · Cl₂ · Cl_xO_y **관측 안 됨** | — | — |

---

# 6. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 대표 계면 모델 도식. 양극 슬랩의 **두 종단**: region A (LiCoO₂-종단, `P2m2`) · region B (Li-종단, `C2m1`) | ⛔ **안 봤다**(§0b). **종단 2종을 한 셀에 넣는 설계**는 우리가 향후 계면 슬랩을 만들 때 그대로 쓸 수 있다 — 한 궤적에서 종단 의존성을 본다 |
| 2 | **본 그림.** D_z(Li⁺) 막대, 6 SE × {oriented bulk / 충전계면 / 방전계면}. y 로그 **10⁻⁹–10⁻⁵ cm²/s**, 우측 별도 패널(**10⁻¹³–10⁻⁵**)에 양극 2종. 회색 ⊠ = "Unavailable" 2칸(LiCoO₂/LLZO·LLTO) | 🔴 **이 논문의 유일한 정량 축이고, §12-② 에서 무너진다.** 단 **"방전(Li-full) 양극과 맞물리면 계면 D 가 전 화학계에서 내려간다"** 는 경향 자체는 `Table S3` 에서 예외 없이 성립한다 |
| 3 | **본 그림.** Li⁺ z-분포, **t = 0 (검정, 스냅샷)** vs **t = 0.9–1.0 ns (색, 100 ps 시간평균)**, 6 계면 (전부 Li₀.₅CoO₂). 회색 띠 = 영역 A·B | 🟢 **이 논문에서 제일 깨끗한 관측이다.** (a) Li₇P₃S₁₁: z ≈ 26–30 Å 에 **완전 고갈 골**, 양극 내부 피크가 `figure-read ≈` 0.04 → **0.077 Å⁻¹** 로 상승 = SE→양극 Li 이동. (e) LLZO 는 두 곡선이 사실상 겹친다 |
| 4 | **본 그림.** (a,b) Li₇P₃S₁₁·LGPS / Li₀.₅CoO₂ 의 원소 z-프로파일(마지막 100 ps 평균) + 1 ns 스냅샷. (c,d) **r(S–S)·r(P–P) RDF 의 시간전개 히트맵**(세로축 0–1 ns, 가로 0–10 Å) + 위에 **MP 참조화합물 RDF 18종 스택** | 🟡 **기법은 배울 만하다** — "RDF 시간전개 히트맵 + 참조상 스택" 은 우리가 산물 생성 시점을 볼 때 쓸 수 있는 싼 도구다. ⛔ **그러나 종 동정 근거로는 약하다**(§12-③). (a) 에서 S(노랑)가 SE 쪽에서 **평탄화**(무질서), P(연보라)는 진동 유지 = **음이온 무질서가 S 에서 먼저** |
| 5 | **본 그림.** 염화물 4종 (a) LYC/Li₀.₅CoO₂ (b) LYC/LiCoO₂ (c) LIC/Li₀.₅CoO₂ (d) LIC/LiCoO₂ 의 원소 프로파일 + 스냅샷 | 🟢 **(a) vs (b) 대비가 육안으로 확실하다** — 충전(a)의 Co·O 피크가 **너덜너덜**(`figure-read ≈` 0.04–0.055 Å⁻¹, 들쭉날쭉)이고 방전(b)은 **날카롭고 균일**(≈0.08). **"충전 상태가 계면 열화의 스위치"** 라는 이 논문 최대 메시지의 가장 강한 시각 증거 |
| 6 | **본 그림.** 산화물 (a) LLZO/Li₀.₅CoO₂ (b) LLTO/Li₀.₅CoO₂ 원소 프로파일 + 스냅샷 | 🟡 (b) 에서 **La(하늘색) 피크가 z ≈ 28.5 Å 양극 가장자리에 `figure-read ≈` 0.075 Å⁻¹ 로 서 있다** = La 가 계면면까지 왔다. ⚠ (a) 에서 **선그래프 범례와 다면체 범례의 색이 뒤집혀 있다**(선: La=연두/Zr=주황 ↔ 다면체: LaO₈=주황/ZrO₆=연두) — 원 그림의 결함. §12-⑧ |
| Table 1 | 계면 6종 제원 (nat · strain · MCIA) | §4a 에 전량 전사 |
| Table S1 | **0 K** 격자 MACE vs DFT, **9 물질** (⭐ Li₆PS₅Cl 포함) | §4c. ⭐ **우리 계에서 MACE-MP-0 부피오차 0.05 %** |
| Table S2 | **300 K** 격자 MACE vs DFT, 8 물질 (⛔ Li₆PS₅Cl 없음) | §4c. 🔴 **"below 5 %" 반증** |
| Table S3 | Li⁺ D 전표 (Overall + D_z), 20 행 | §5a 에 전량 전사 |
| S1 | **본 그림(SI p6).** 충전 계면 6종 총에너지 vs 1 ns | 🔴 **§3b 의 결정적 근거** — Li₇P₃S₁₁ 계가 1 ns 끝까지 감소 중. ⚠ **캡션이 "discharged" 라 적혀 있는데 패널은 전부 Li₀.₅CoO₂** = 캡션 오류 |
| S3 | **본 그림(SI p8).** 부피/원자 vs 1 ns, 12계 | Li₇P₃S₁₁ 계만 `figure-read ≈` +0.4–0.5 Å³/atom 팽창, 나머지 평탄. 산화물은 ≈10.5–11 Å³/atom |
| S4 | **본 그림(SI p9).** MSD(총/x/y/z), 실제로는 **충전** 계면 | `figure-read ≈` 1 ns 총 MSD: Li₇P₃S₁₁ **51** · LGPS **36** · LYC **105** · LLZO **67** · LLTO **95** Å². **x ≫ z ≫ y 강한 이방성** · LLZO/LLTO 는 **계단형**(개별 홉 몇 개) |
| S5 | **본 그림(SI p1).** MSD, 실제로는 **방전** 계면 | `figure-read ≈` Li₇P₃S₁₁ **29** · LGPS **9.5** · LYC **16** · LIC **27** · **LLZO 1.4** · **LLTO 0.15 Å²**(순수 진동) ⇒ `Table S3` 의 "–" 는 **정직한 표기**다 |
| S6 | **본 그림(SI p2).** 방전 계면 6종 Li 분포 | 🟢 **여섯 계 전부 t=0 과 최종이 겹친다** — Li 재분배가 **충전 상태에서만** 일어난다 |
| S7 | **본 그림(SI p3).** 황화물/방전 원소 프로파일 | `Fig. 4a` 와 대비: 여기선 **S(노랑)도 진동 유지** = 무질서 없음 |
| S13 | **본 그림(SI p9).** LLZO/LiCoO₂ · LLTO/LiCoO₂ | (b) 에서 La 피크가 양극 가장자리 z ≈ 28 Å 에 `figure-read ≈` 0.075 |
| S2, S8–S12 | ⛔ **안 봤다** (총에너지 나머지 · RDF 참조상 묶음) | §0b |

---

# 7. 결과 절별 정독 — 본문 순서대로

## 7a. "Interfacial Li-ion dynamics" (Fig 2)

**벌크 기준선**:
- 충전 양극 Li₀.₅CoO₂ **≈ 8 × 10⁻⁷ cm² s⁻¹** (본문) — *"previously reported AIMD values 와 잘 일치"* (ref 31 Van der Ven–Ceder 2001). ⚠ `Table S3` 는 **1.1 × 10⁻⁶**.
- 황화물·염화물 SE **10⁻⁷–10⁻⁶** (refs 4·32–37) ✅ 문헌 대역과 일치.
- 산화물 SE **10⁻⁹–10⁻⁸** (refs 38·39) ✅.

**충전 양극(Li₀.₅CoO₂)과 맞물렸을 때** — SE 화학에 따라 방향이 갈린다:
- 황화물 2종: **벌크의 약 절반** (0.50 / 0.43) ⇒ *"계면에 추가 이동장벽이 있다"*
- Li₃InCl₆: 비슷하게 억제 (0.72)
- **Li₃YCl₆: 거의 2배 증가** (2.16)
- **LLZO: 50배 이상 증가** (53.8) · **LLTO: 8배** (8.1)

> ⚠ 본문은 LLZO·LLTO 를 묶어 *"oxide interfaces 에서 더 두드러진다"* 고 쓰는데,
> **LLTO 는 8.1배로 한 자릿수를 못 넘는다.** 표현이 한 단계 세다.

**방전 양극(LiCoO₂)과 맞물렸을 때** — **예외 없이 전부 억제**:
- 황화물·염화물: **6.0–9.4 × 10⁻⁸** (본문은 "6–7 × 10⁻⁸" 이라 적었다 — §5a 각주)
- 산화물 2종: **MD 로 신뢰성 있게 못 잼** ⇒ `Table S3` "–", `Fig. 2` 회색 ⊠

> ✅ **figure-read 검증**: `Fig. 2` 막대에서 내가 읽은 8개 값(LPS 벌크 ≈5.8e−7 · LGPS 벌크 ≈2.9e−7 ·
> LYC 벌크 ≈2.1e−7 · LYC 충전 ≈4.5e−7 · LIC 벌크 ≈3.0e−7 · LLZO 벌크 ≈5e−9 · LLTO 벌크 ≈9.5e−8 ·
> LLTO 충전 ≈7.5e−7)이 `Table S3` D_z 열과 **전부 ±10 % 안에서 일치**했다. ⇒ `Fig. 2` = D_z 열. 확인 완료.

## 7b. "Spatial distribution of Li⁺ at interface" (Fig 3, Fig S6)

**황화물 / 충전**:
- Li₇P₃S₁₁: Li 이 **SE → 양극**으로 이동, 양극 내 Li 농도 상승, **z ≈ 28 Å 에 Li 고갈 영역**.
  `figure-read`: 최종 곡선이 z ≈ 25–31 Å 구간에서 **0 에 닿는다**. 양극 내부 피크 **0.04 → 0.077 Å⁻¹**.
- LGPS: **"minor" 재분배**, z ≈ **45 Å**·**72 Å** 근처에서 Li 농도 감소.
- 선행 귀속: 같은 Li 고갈이 **Li₃PS₄/LiCoO₂** 에서 보고됐고(ref 7 **Haruyama 2014 공간전하층**),
  원인은 *"황화물 SE 쪽에서 Li⁺ 의 전기화학 퍼텐셜이 낮고 Li 공공 생성이 더 유리하기 때문"* (ref 11 Tateyama 2019).

**염화물 / 충전** — **종단 의존성이 나온다**:
- LYC region A: **SE·양극 양쪽에서** Li 감소, **z ≈ 32 Å** 이 가장 뚜렷.
- LYC region B: **Li 밀도가 양극 벌크의 거의 2배로 증가** — MD 궤적에서 **CoO₆·LiO₆ 다면체 위 Li 흡착** 확인.
  원인 추정: *"O²⁻ 의 전기음성도가 Cl⁻ 보다 높아서"*.
- LIC region A: **감소가 주로 SE 안**에서. region B: 같은 흡착.
  `figure-read`: (d) 의 region B 피크가 **≈0.07 Å⁻¹** 로 초기(≈0.025–0.03) 대비 뚜렷이 커진다 — **6 패널 중 시간 변화가 제일 크다**.

**산화물 / 충전**: t=0 과 0.9–1.0 ns 프로파일이 *"거의 구분되지 않는다"* ⇒ **Li 재분배 구동력 없음**.
> ⚠ **그림은 (f) LLTO 에서 약간 다르게 보인다** — region B(z ≈ 49–56 Å)에서 최종 곡선이 `figure-read ≈` **0.081 Å⁻¹**
> 로 그림 전체 최고점을 찍고, 초기(≈0.06)보다 뚜렷이 높다. **(e) LLZO 는 본문대로 완전히 겹친다.**
> ⇒ *"산화물 2종 모두 변화 없음"* 은 **LLTO 에서 과장**이다. §12-⑦

**방전 전 계면 (`Fig. S6`)**: **여섯 계 전부** 초기·최종이 겹친다 ⇒ *"kinetic interfacial stability 가 높다"*.
> 🔑 **그런데 물리적 이유가 한 줄로 설명된다**: 방전 LiCoO₂ 는 **Li 공공이 없고 D_z = 1.6 × 10⁻¹²** 로 사실상 부동이다.
> **갈 자리가 없어서 안 간 것**이지 계면이 화학적으로 온순해서가 아니다. 논문은 이 구분을 하지 않는다. §12-⑥

## 7c. "Interfacial reaction and stability" (Fig 4, Fig 5)

**황화물**:
- `Fig. 4a,b` 원소 프로파일에서 **음이온 무질서** 관측 ⇒ *"저배위 Co^n⁺ 가 관여하는 반응 + SE 분해 가능성"*.
- 방전 쪽은 **더 안정** — 원소 분포 무질서가 덜하다 (`Fig. S7`). ✅ 내가 본 그림과 일치한다.
- **RDF 시간전개**(§5c 표) — S_n·P₂S₇ 가 **t = 0 부터** 있고, P_xS_yO_z 가 0.1–0.8 ns, LGPS 에서 Li₃P·Li₃PO₄ 가 0.3 ns 이후.
- ✅ **S_n 생성이 "previous thermodynamic analysis" 와 일치**(refs 9·40 = Zhu 2015/2016).
- ⇒ *"황화물 SE 와 층상 산화물 양극 사이의 반응성이 높다."*

**염화물**:
- LYC/**LiCoO₂**: 비교적 안정. 예외는 **Cl⁻ ↔ 저배위 Co^n⁺** 반응 가능성.
- LYC/**Li₀.₅CoO₂**: 훨씬 불안정. **Y·Cl 의 주기 배열이 A·B 양쪽에서 깨진다.**
  - region A: **Co 가 Li 층으로 이동**(양극 표면).
  - region B: Co 층간 이동은 **없고**, 대신 **Y 가 Li 층에 삽입되거나 CoO₆ 팔면체에 흡착**.
- LIC/양쪽 모두: **Li₃InCl₆ 분해 발생.** 충전 쪽에서는 **Co·In 이 Li 층으로 이동**.
- ⛔ **기상종(O₂·Cl₂·Cl_xO_y) 없음** ⇒ 열역학·실험의 **4.2 V 안정성**과 일치 (refs 4·6·41).
- 반응에너지 **23 / 21 meV atom⁻¹** ⇒ *"high chemical stability"*.
- 결론: *"염화물 SE + 층상 산화물, 특히 고충전 상태에서는 **양극 표면 열화 · SE 내 양이온 확산**이
  **계면 임피던스 증가와 구조 열화**로 이어질 수 있다."*

> 🟢 **`Fig. 5a` vs `Fig. 5b` 는 육안으로 확실하다** (§6 표). 충전 LYC 계의 Co/O 프로파일이 너덜해지고
> 방전 계는 날카롭다. **"충전 상태가 스위치"** 가 이 논문의 가장 견고한 정성 결과다.

## 7d. "Cation inter-diffusion at the interface" (Fig 4, 5, 6, S13)

| 계면 | 관측된 양이온 이동 |
|---|---|
| 황화물 / **충전** | **Co → 인접 Li 층** (양극 격자 이탈) + **Ge → 양극 Li 층** (LGPS 쪽) |
| LYC / 충전 | **Y → 양극 Li 층 삽입** |
| **LLZO·LLTO / 방전** | **La → LiCoO₂ Li 층** 확산 |
| 산화물 / 방전 | **La↔Zr · La↔Ti** 소규모 상호확산 (`Fig. S13`) |
| **전 화학계 공통** | **충전 Li₀.₅CoO₂ 표면에서 Co → Li 층** — *"a recurring phenomenon across these different interface chemistries"* |

선행 귀속: ref 42 = **Haruyama 2017, "Cation mixing properties toward Co diffusion at the LiCoO₂/sulfide interface"**
(= 우리 inbox 의 `10. Cation_Mixing_Properties_toward_Co_Diffusion…` 과 같은 논문).

> ⚠ 본문은 *"we observe **La ion diffusion** from the SE into the Li layers of the **LiCoO₂** cathode (`Fig. 6`)"* 라 쓰는데
> **`Fig. 6` 은 Li₀.₅CoO₂(충전) 계면 2장**이다. 방전판은 `Fig. S13` 이다. **그림 지시가 틀렸다.** §12-⑧

## 7e. Discussion / Conclusion

3기전 재진술(§3a) + 종결 문장:
> *"These kinetic processes, **which are particularly pronounced when the cathode is in a highly charged state**,
> collectively lead to the formation of resistive interphases, the obstruction of ion transport pathways, and the
> **loss of active lithium**. This study underscores that **thermodynamic predictions alone are insufficient** …
> The methods demonstrated here provide a powerful framework for the future design and **high-throughput
> computational screening** of more robust and efficient solid-state battery interfaces."*

---

# 8. Post-processing ★

| 무엇 | 도구 / 방식 | 수치화 | 우리 대응 |
|---|---|---|---|
| **격자 정합 / 계면 생성** | **Zur–McGill** 알고리즘 + MCIA < 400 Å² 게이트 (ref 18) | strain · MCIA (`Table 1`) | ⛔ 없음. 우리가 계면 슬랩으로 갈 때 **이 게이트를 그대로 채택할 수 있다** |
| **확산계수** | MSD → `D = MSD/(2dt)`, d=3, **셀 전체 Li** | `Table S3` (Overall + D_z) | 우리 `tools/ionic/` MSD 창 2–50 ps 고정 · 자유절편 · Nernst–Einstein |
| **공간 분포** | **Li 수 밀도 z-프로파일**, t=0 스냅샷 vs 0.9–1.0 ns **100 ps 시간평균** | `Fig. 3`·`Fig. S6` (단위 **Å⁻¹**, 정규화 Li count) | ⛔ 없음 — **가장 싸게 흉내낼 수 있는 항목**(§10-②) |
| **원소 분포** | 원소별 z-프로파일, 마지막 100 ps 평균 | `Fig. 4a,b`·`Fig. 5`·`Fig. 6` | ⛔ 없음 |
| **종 동정** | **RDF 시간전개 히트맵** r(S–S)·r(P–P) vs **MP 참조상 RDF 스택**(e_above_hull < 20 meV/atom) | `Fig. 4c,d` — **정성 매칭만** | 🟡 우리는 산물을 **hull 반응식**으로 낸다 — 층위가 다르다(§9) |
| **구조 시각화** | 다면체(PS₄·GeS₄·CoO₆·YCl₆·InCl₆·LaO₈·ZrO₆·TiO₆) 스냅샷 | `Fig. 4`–`Fig. 6` 하단 | VESTA 관례와 동일 |
| ⛔ **안 한 것** | NEB · Bader · COHP · DOS/PDOS · ELF · 계면에너지 · W_ad · 탄성 · 포논 · **임피던스** · 자유에너지 · 배위수 통계 | — | — |

---

# 9. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md`

> ⚠ **직접 수치 비교가 성립하는 칸이 거의 없다.** 계(양극·SE), 온도, 방법, 보고량이 전부 다르다.
> 🔴 **진짜 차이 / 🟡 방법 인공물 / ⚪ 비교 불가** 를 칸마다 명시했다.

| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| **계 (SE)** | LGPS · Li₇P₃S₁₁ · Li₃YCl₆ · Li₃InCl₆ · LLZO · LLTO | **Li₆PS₅Cl / Li₅.₄PS₄.₄Cl₁.₆ (아지로다이트)** | ⚪ **겹치지 않는다.** 아지로다이트는 `Table S1` 0 K 벤치마크에만 있고 **MD 를 안 돌렸다** — *"황화물이니까 우리한테도 적용된다"* 는 **논증 없이 못 한다** |
| **계 (양극)** | LiCoO₂ / Li₀.₅CoO₂ **단 하나** | LiCoO₂ · LiNiO₂ · LiMnO₂ · **NMC811** (4종) | 🟢 **LiCoO₂ 는 겹친다.** Guo 는 Ni·Mn 계를 전혀 안 본다 |
| **계면 판정의 층위** | **300 K · 1 ns · 전기장 없음 · 자발 접촉**의 운동학 | **0 K hull grand-potential**, μ_Li = 외부 스칼라(2.5–4.5 V) | 🔴 **진짜 차이. 우리 급소가 맞다.** 우리는 시간축이 없다 |
| **산화 분해 산물** | MD 로 **S_n · P₂S₇** 관측, *"thermodynamic analysis 와 일치"* | grand-potential onset **2.256 V**: `Li₆PS₅Cl → Li₃PS₄ + LiCl + **S** + 2Li⁺ + 2e⁻` · 2.385 V: **P₂S₇ + S** | 🟢 **같은 종이다.** 우리 반응식 2단계가 내놓는 **S 와 P₂S₇** 을 Guo 의 MD 가 **독립적으로 관측**했다 — **§G(우리가 문헌을 검증하는 지점) 자산** |
| **Li 고갈층 / 공간전하** | **직접 관측** — Li₇P₃S₁₁ 에서 z ≈ 28 Å 완전 고갈, 폭 `figure-read ≈` **5 Å** | ⛔ **0.** μ_Li 가 **공간 무관 스칼라**라 원리적으로 이 항이 없다 | 🔴 **진짜 차이, 그리고 우리한테 없는 물리** |
| **양이온 상호확산** | **관측** (Co·Ge·Y·In·La 이동) — 단 **정량 0** | ⛔ **0** | 🔴 **진짜 차이** (단 Guo 도 수치가 없다 — §12-④) |
| **Li⁺ D** | **MACE-MP-0 · 300 K · NpT · 1 ns · 단일시드** · D_z 6.0×10⁻⁸ – 7.5×10⁻⁷ | **UMA-s-1p1 · 600–1000 K · Langevin NVT · 200 ps** · D(600 K) comp1 3.09×10⁻⁶ / modelc 7.90×10⁻⁶ | 🟡 **비교 금지.** 온도·모델·앙상블·MSD 창·시드 수가 전부 다르다. ⭐ 1저자 인용정책(2026-09-18)상 우리 D 는 **상대차로만** 쓰므로 애초에 교차 인용 대상이 아니다 |
| **활성화에너지** | ⛔ **없다** (300 K 단일 온도) | comp1 0.253 / modelc 0.224 eV (3-seed 0.197 ± 0.032) | ⚪ 비교 불가 |
| **MLIP 선택** | **MACE-MP-0** — 검증 = **격자상수만**, 300 K 에서 **3항목 5 % 초과**(§4c) | **UMA-s-1p1(omat)** — Li₃PS₄ 힘 **MAE 30.0 meV/Å** (`db/properties/mlip_bench_li3ps4_uma.json`) | 🟢 **우리 검증이 더 강하다.** 격자만 맞추는 것은 힘 정확도를 보증하지 않는다. ⭐ 다만 **Li₆PS₅Cl 0 K 격자에서 MACE-MP-0 부피오차 0.05 %** 는 우리 계에 대한 **외부 독립 근거**로 쓸 수 있다(`Table S1`) |
| **무질서 처리** | ⛔ **전혀 없음.** 각 SE 단일 배열 · LLTO 의 Li/La 무질서·아지로다이트형 S/Cl 무질서 논의 0 | 우리는 배열 앙상블 · 3-seed | 🟢 **우리가 낫다** |
| **통계 / 오차** | ⛔ **시드 1 · 오차막대 0 · 블록평균 0** | modelc 3-seed(600 K) Ea 오차막대 | 🟢 **우리가 낫다.** 우리 litdb 는 `mccluskey2025`·`pranami2015`·`zaby2026` 3편으로 이 규율을 명문화해 뒀다 |
| **band gap / 전자구조** | ⛔ 없음 (MLIP 은 전자구조를 안 낸다) | comp1 2.066 / modelc 2.099 eV (fixed-occ nscf) | ⚪ 비교 불가. ⚠ **단 Guo 의 Li₃PO₄ 단서**(*"전자절연 + 이온전도 = 부동태 가능"*)가 **우리 gap 축에 기능적 의미**를 준다 — §10-① |
| **hull 열역학의 위상** | *"불충분하다"* 라고 쓰면서 **자기 결론의 보강으로 3회 사용**(§3d) | 우리 §B 전체가 hull 위 | 🟢 **우리가 걱정한 것보다 유리하다.** §13b |

---

# 10. 적용 인사이트 — 우리 연구에 어떻게

## ① 🟢 **우리 gap 축이 "기능" 을 얻는다 (비용 0)**

Guo Discussion: *"Li₃PO₄, an **electronically insulating but ionically conductive** material, could potentially
**passivate and stabilize** the interface."*

우리 CEI 산물 후보가 **Nd 인산염**이다. 같은 논리가 그대로 걸린다 —
*"우리가 예측하는 CEI 산물은 인산염계이고, 인산염 CEI 는 문헌에서 **전자절연 + 이온전도**로 부동태 기능이 기대되는 부류다"* 라고
쓸 수 있고, 근거가 **이 논문 + ref 43(Takahashi 2013)** 이다. **추가 계산 0.**
⇒ 여기에 우리가 이미 가진 gap(comp1 2.066 / modelc 2.099 eV, wide-gap)이 **"전자절연" 칸의 우리 쪽 증거**로 붙는다.
⚠ 단 **NdPO₄ 자체의 gap 은 우리가 아직 안 냈다** — 쓰려면 그 계산이 하나 필요하다(§13c-③).

## ② 🟢 **"Li 수 밀도 z-프로파일" 은 우리가 당장 흉내낼 수 있는 유일한 운동학 관측량**

Guo 의 세 기전 중 **② Li 고갈**은 관측 방법이 제일 싸다 — **MD 궤적의 Li 수 밀도를 z 로 히스토그램**하고
t=0 과 마지막 100 ps 평균을 겹쳐 그리는 것이 전부다. 우리는 **이미 MD 궤적을 갖고 있다**(`tools/ionic/`).
⛔ 단 우리 궤적은 **벌크 단결정**이라 계면이 없다 ⇒ 계면 슬랩을 만들어야 비로소 의미가 생긴다.
🔑 **그전에 벌크에서도 할 수 있는 것**: **도핑 계(Nd·O)에서 Li 수 밀도의 공간 불균일성**을 같은 방식으로 재면,
*"도펀트 주변에 Li 이 고이거나 비는가"* 라는 물음에 답할 수 있다 — **새 MD 없이 기존 궤적으로**.

## ③ 🟡 **계면 슬랩을 만들 때의 사양이 통째로 있다**

Zur–McGill + **MCIA < 400 Å²** + **총길이 > 50 Å** + **초기 간격 2.5 Å** + **종단 2종을 한 셀에**.
우리가 §H 의 계면 축을 열 때 이 네 줄을 **기본값으로 채택**하면 설계 논쟁 한 라운드를 건너뛴다.
⚠ 다만 **strain 0.5–1.8 %** 를 지키려면 아지로다이트(입방 a ≈ 9.86 Å) × LiCoO₂(101) 조합에서
MCIA 가 400 Å² 안에 들어오는지 **따로 확인**해야 한다.

## ④ 🔴 **"충전 상태가 스위치" 는 우리 전압축과 같은 말을 다른 언어로 한다**

Guo 의 최대 정성 결과는 *"열화가 고충전(Li₀.₅CoO₂)에서만 두드러진다"* 이다.
우리 §B 는 **전압 6점(2.5–4.5 V)** 으로 같은 축을 훑는다 — **우리 쪽이 해상도가 높다**(6점 vs 2점).
⇒ 원고에서 *"운동학 연구도 충전 상태 의존성을 보지만 두 점뿐이고, 우리는 전압 격자로 그 축을 채운다"* 라고
**우리 강점으로 되돌릴 수 있다.** (⚠ 단 우리 것은 0 K 평형이라 "열화 속도" 가 아니라 "구동력" 이다 — 말을 섞지 말 것.)

## ⑤ 🟠 **우리 보호율 식이 다루지 않는 실패 모드 2개를 이 논문이 이름 붙여 준다**

우리 §2b 보호율 `min(1, k·x/(1−x))` 는 **면적 피복**만 말한다. Guo 가 보여 주는 것 중 **피복으로 막을 수 없는 것**:
- **Li 고갈 / 공간전하** — CEI 가 덮여 있어도 μ_Li 불일치는 남는다.
- **양이온 상호확산** — 오히려 CEI 가 확산 매질이 될 수도 있다.
⇒ **§Limitations 에 이 두 줄을 먼저 쓴다.** 리뷰어가 먼저 말하게 두지 않는다.

---

# 11. 인용 가능 문장 (원고 / 덱)

> ⚠ 아래는 **원문에 실제로 있는 문장**만이다. §3b·§3c 에서 걸러낸 것은 넣지 않았다.

- *"열역학 예측만으로는 계면 안정성을 평가하기에 불충분하다."*
  (원문 Conclusion: *"thermodynamic predictions alone are insufficient for assessing interfacial stability"* — **우리 한계를 우리가 먼저 말하는 문장**)
- *"양극/SE 계면 임피던스를 낳는 운동학 기전은 셋이다 — 저전도 계면상 형성 · Li 고갈 영역 · 양이온 상호확산."* (Abstract / Discussion)
- *"이 운동학 과정들은 **양극이 고충전 상태일 때 특히 두드러진다**."* (Conclusion)
- *"Li₃PO₄ 처럼 **전자절연이면서 이온전도**인 상은 계면을 부동태화·안정화할 가능성이 있다."* (Discussion, ref 43)
- *"고충전 상태에서 S_n 이 생성된다는 것은 **기존 열역학 해석과 일치한다**."* (refs 9·40 = **Zhu 2015/2016** — 🟢 **hull 을 추인하는 문장**)
- *"Li₃YCl₆·Li₃InCl₆ 는 LiCoO₂ 에 대해 **4.2 V 까지** 전기화학적으로 안정하다는 **열역학 해석 및 실험 관측과 일치**한다. 반응에너지는 각각 **23 · 21 meV/atom** 이다."* (🟢 **계면 반응에너지를 안정성 판정에 쓰는 원문 선례**)
- ⛔ **쓰지 말 것**: *"운동학이 열역학보다 더 지배한다"*, *"열화의 속도와 최종 형태"*, *"코팅 4조건"* — §3b·§3c.
- ⛔ **쓰지 말 것**: 이 논문의 **D 절대값** — 혼합 평균이다(§12-②).

---

# 12. 🔴 주의 / 한계 — 비판적 감사

> 이 절이 길다. 이유는 §0a 에 적었다 — **우리를 때리는 근거의 강도를 재려면 그 근거의 품질을 재야 한다.**

## ① ⛔⛔ **"임피던스" 가 한 번도 계산되지 않았다**

제목이 *"Kinetic analysis of cathode–solid electrolyte **interface**"* 이고 초록 첫 문장이
*"**High interfacial impedance** hinders the development of ASSBs"* 인데:

- `impedance` **15회** 등장 — 전부 **동기·해석의 언어**.
- `EIS` · `DRT` · `equivalent circuit` · `resistance` · `Ω` · `Ω cm²` — **0회**.
- **임피던스를 계산하는 어떤 절차도 없다.** 전도도조차 안 냈다 (D 만 있고 Nernst–Einstein 변환도 없다).

⇒ **1저자 질문 5번(임피던스 해석 방법)의 답: 이 논문에는 임피던스 해석이 없다.**
세 기전은 *"임피던스를 올릴 것이다"* 라는 **정성 추론**으로만 임피던스와 연결된다.
⇒ 우리가 *"우리는 임피던스를 못 한다"* 고 비교당할 때, **이 논문도 못 한다.** 인용의 원전이 그 축을 안 갖고 있다.

## ② 🔴🔴 **"계면 확산계수" 가 계면의 양이 아니다 — 혼합 평균 인공물**

본문 그대로: *"The Li⁺ diffusivity across the cathode/SE interface is calculated from the **MSD of all Li⁺ ions
within the entire simulation cell**."*

셀은 **SE + 계면 + 양극** 3상이고, 각 상의 D 가 **5–6 자릿수** 다르다:

| 상 | D_z (cm² s⁻¹) |
|---|---|
| Li₀.₅CoO₂ (충전 양극) | **1.1 × 10⁻⁶** |
| LLZO (벌크, 실험) | **5.0 × 10⁻⁹** |
| LiCoO₂ (방전 양극, 실험) | **1.6 × 10⁻¹²** |

⇒ 셀 평균은 **가장 빠른 상이 지배**한다. 검산:

| 주장 | 혼합 평균만으로 설명되나 |
|---|---|
| *"Li₀.₅CoO₂/LLZO 계면 D 가 벌크 LLZO 대비 **50배 이상**"* | 🔴 **완전히 설명된다.** 계면값 D_z = 2.69×10⁻⁷ 은 **양극값 1.1×10⁻⁶ 의 24 %** 다 — **셀 Li 의 24 % 가 양극에 있기만 하면, LLZO 쪽 기여가 0 이어도** 이 값이 나온다 |
| *"Li₀.₅CoO₂/LLTO 가 8배"* | 🔴 같은 방식. 7.46×10⁻⁷ = 양극값의 **68 %** — LLTO 모델은 nat 656 로 가장 작아 양극 Li 분율이 높다 |
| *"Li₀.₅CoO₂/Li₃YCl₆ 이 2배"* | 🔴 벌크 LYC 2.18×10⁻⁷ 과 양극 1.1×10⁻⁶ 의 **가중평균이 4.7×10⁻⁷** 이 되려면 양극 Li 분율 ≈ 28 % — **아주 그럴듯하다** |
| *"방전 계면은 전부 억제"* | 🟡 **일부만.** 방전 양극 Li 은 사실상 부동이므로 **희석으로 내려가는 것이 당연**하다. 다만 Li₇P₃S₁₁ 은 벌크의 **0.12배**까지 내려가는데, 이는 양극 Li 분율이 88 % 여야 희석으로 설명된다 — **비현실적** ⇒ **여기엔 진짜 계면 억제가 있다** |

**결론**: `Fig. 2` 의 "증가" 는 **전부 양극 Li 이 섞여 들어온 인공물로 설명 가능**하고,
"감소" 중 황화물/방전 쪽 일부만 실재 신호로 보인다.
**계면 D 를 보려면 z-분해 국소 D 를 내야 하는데, 이 논문은 안 냈다** (Li 수 밀도는 z-분해하면서 D 는 안 했다).

> 🔑 **이것이 §3b 판정의 물리적 뿌리다.** 리뷰가 *"운동학이 더 지배"* 라고 옮긴 주장의 **유일한 정량 축이 이것**인데,
> 그 축이 계면을 재고 있지 않다. **정성 관측(Fig 3–6)은 이 문제의 영향을 받지 않는다** — 거기는 살아 있다.

## ③ 🔴 **종 동정이 "RDF 눈대중" 이다**

`Fig. 4c,d` 는 계면의 시간의존 RDF 위에 **MP 참조 화합물 18종의 RDF 를 스택**해 놓고,
*"이 피크가 P_xS_yO_z 에 해당한다"*, *"Li₃P·Li₃PO₄ 형성에 해당한다"* 라고 읽는다.

**왜 약한가**:
- RDF 는 **다체 상관을 1차원으로 뭉갠** 양이다. 서로 다른 상이 같은 peak position 을 준다 — 참조 스택에서
  P₂S₅·P₄S₅·P₄S₇·P₄S₉ 의 첫 피크가 **모두 2.9–3.4 Å 에 몰려 있다**(figure-read).
- 참조는 **결정 벌크**(0 K MP 구조), 관측은 **300 K 계면 국소** — 열 확폭만으로 구분이 사라진다.
- **배위수 분석 · 국소환경 군집 · 화학식량 계수 · 생성량 없음.** *"얼마나 생겼나"* 를 못 말한다.
- ⛔ *"minimum r(S–S) ≈ 4 Å 이 Li₃P, Li₃PO₄ 에 해당"* — **Li₃P·Li₃PO₄ 는 S 를 포함하지 않는다.**
  본문이 P–P 그래프(`Fig. 4d`)를 논하면서 **r(S–S)** 라고 쓴 오기로 보인다. 같은 오기가 S_n/P₂S₇ 문장에도 있다.

⇒ **"Li₃PO₄ 가 생겨 부동태화할 수 있다"(§10-①의 근거)는 이 논문에서 가장 약한 관측 위에 서 있다.**
쓸 때 *"MD 에서 Li₃PO₄ 형성이 제안되었고(RDF 기반)"* 처럼 **판별 수준을 밝혀서** 쓴다.

## ④ 🔴 **기전 ③(양이온 상호확산)에 수치가 하나도 없다**

이동한 양이온의 **개수 · 침투 깊이 · 확산계수 · 시간의존성** — 전부 없다.
근거는 *"프로파일이 겹친다"* 와 *"스냅샷에 보인다"* 뿐이다.
⇒ **우리가 이 기전에서 "뒤졌다" 고 할 근거가 없다** — 이 논문도 정량하지 않았다.
(대조: `ncube2026_ionic_interdiffusion_lco_lgps_multiscale` 은 같은 축에서 **원소별 계면 D 를 6개 냈다** —
Li 3e−12 / P 7e−12 / O 2e−12 / S 6e−13 / Ge 4e−14 / **Co 8e−15 m²/s** — 그쪽이 정량 원전이다.)

## ⑤ 🔴 **반응이 안 끝났는데 결론을 낸다**

`Fig. S1`: Li₀.₅CoO₂/Li₇P₃S₁₁ 총에너지가 **1 ns 끝까지 단조 감소** (figure-read ≈ −5.062 → −5.090 eV/atom).
`Fig. S3`: 같은 계 부피가 **계속 팽창** (figure-read ≈ 16.0 → 16.5 Å³/atom).
⇒ **정상상태가 아니다.** 계면상의 **두께·조성·연속성**을 말할 수 없고, 논문도 실제로 말하지 않는다.
**"최종 형태" 는 리뷰가 얹은 말이다**(§3b).

## ⑥ 🟡 **"방전 계면이 안정하다" 의 인과가 모호하다**

방전 LiCoO₂ 는 **D_z = 1.6 × 10⁻¹²** 로 부동이고 **Li 공공이 없다**.
⇒ Li 이 안 움직인 것은 **계면이 온순해서가 아니라 받을 자리가 없어서**일 수 있다.
논문은 이를 *"high kinetic interfacial stability"* 라고만 부르고 두 원인을 분리하지 않는다.
🔑 **실전 함의**: 실제 셀은 **충전 상태에서 오래 머문다** ⇒ *"방전 상태에서는 안정"* 은 위안이 안 된다.
이건 오히려 **Guo 결론을 강화**하는 쪽이다.

## ⑦ 🟡 **본문 서술과 그림이 어긋나는 곳 (내가 직접 본 것)**

| # | 본문 | 그림에서 보이는 것 |
|---|---|---|
| a | *"산화물 계면(LLZO·LLTO)의 Li 분포는 초기와 최종이 **거의 구분되지 않는다**"* | 🟡 **LLZO(`Fig. 3e`)는 맞다.** **LLTO(`Fig. 3f`)는 region B(z ≈ 49–56 Å)에서 최종 피크가 `figure-read ≈` 0.081 Å⁻¹ 로 그림 전체 최고점**이고 초기(≈0.06)보다 뚜렷이 높다 |
| b | *"oxide interfaces 에서 증가가 **더 두드러진다**"* | LLZO 54배는 맞지만 **LLTO 는 8.1배** — 한 자릿수 미만 |
| c | *"Li₃YCl₆ region B 에서 Li 밀도가 **양극 벌크의 거의 2배로 증가**"* | 🟡 **`Fig. 3c` 에서 t=0 (검정)도 같은 위치에 ≈0.05 Å⁻¹ 피크가 이미 있다.** "양극 벌크 대비" 는 맞지만 **"시간에 따라 생겼다"** 로 읽히면 과장이다. (반면 `Fig. 3d` Li₃InCl₆ 는 **진짜로 시간에 따라 커진다** — ≈0.03 → ≈0.07) |
| d | 방전 산화물의 La 확산을 *"(`Fig. 6`)"* 로 지시 | `Fig. 6` 은 **충전** 계면 2장. 방전판은 `Fig. S13` |
| e | *"deviations remaining below 5 % at both 0 K and 300 K"* | `Table S2` 에 **3항목이 5 % 초과**(§4c) |

## ⑧ 🟡 **SI 품질 — 단독저자의 대가가 보인다**

- `Fig. S1` 캡션 *"**discharged** cathode/SE"* — 패널 6개 전부 **Li₀.₅CoO₂(충전)**.
- `Fig. S4` 캡션 *"**discharged**"* — 5/6 패널이 **Li₀.₅CoO₂(충전)**, 1개만 LiCoO₂.
- `Fig. S5` 캡션 *"**charged**"* — 패널 전부 **LiCoO₂(방전)**. ⇒ **S4 와 S5 의 캡션이 뒤바뀌었다.**
- `Fig. 6a`·`Fig. S13a`: **선 범례(La=연두/Zr=주황) ↔ 다면체 범례(LaO₈=주황/ZrO₆=연두) 색 반전.**
- 본문 ↔ `Table S3` 수치 불일치 2건(§5a 각주).
- `Fig. 3b` 만 y 축이 **0–0.06**, 나머지 5개는 **0–0.10** — 같은 그림 안에서 스케일이 다르다.
- AIMD 의 **U 값 미기재**.

⇒ 개별로는 사소하지만 **합치면 "공저자 검증이 없었다" 는 신호**다. 인용할 때는 **그림을 직접 확인**한다.

## ⑨ 🟡 **재현성 자산 없음**

Data availability = *"SI 가 전부"*. **궤적 · LAMMPS 입력 · 구조 파일 · 코드 저장소 없음.**
`Table S3` 의 D 를 **어느 시간창으로 적합했는지**도 안 밝혔다 (식은 `MSD/(2dt)` 단일점 형태인데
`Fig. S4/S5` 끝점에서 내가 역산한 값과 **0.7–1.2배 범위로 엇갈린다** ⇒ 어떤 적합을 했지만 문서화 안 됨).
⇒ **우리 규율(`--selftest`, 규약 고정, 창 명시)로 보면 통과 못 한다.**

## ⑩ 🟡 **MACE-MP-0 세대 문제**

ref 22 는 **MACE-MP-0 원판**(arXiv:2401.00096, MPtrj 학습)이다. 검증은 **격자상수뿐**이고
**힘·응력·반응장벽 정확도는 한 줄도 없다.** 그런데 이 논문의 결론은 전부 **반응·확산**, 즉 **힘 정확도에 걸린 양**이다.
⚠ 특히 **반응 생성물**은 PES 의 얕은 골짜기 구조에 민감한데, foundation MLIP 의 과평활(over-smoothing)은
**없는 반응을 만들거나 있는 반응을 놓치는** 방향 둘 다로 작동할 수 있다.
⇒ *"MACE 가 이 반응을 봤다"* 를 **"이 반응이 일어난다"** 로 옮기면 안 된다.

---

# 13. ★★ 결론 — 1저자 4문항 정면 답변

## 13a. ① **이 논문의 비판이 우리한테 유효한 범위** (불리한 것 먼저)

| 비판 | 유효한가 | 이유 |
|---|---|---|
| *"0 K 평형 열역학은 시간축이 없다"* | 🔴 **완전 유효** | 반박 불가. 우리 `GrandPotentialInterfacialReactivity` 는 **반응에너지 하나**를 낸다 |
| *"Li 고갈층(공간전하)을 못 본다"* | 🔴 **완전 유효** | 우리 μ_Li 는 **공간 무관 스칼라**다. 이 물리가 원리적으로 없다. **Guo 는 실제로 봤다**(`Fig. 3a`, z ≈ 28 Å, 폭 ≈5 Å) |
| *"양이온 상호확산을 못 본다"* | 🟡 **유효하되 상대방도 정량 못 했다** | Guo 도 개수·깊이·D 가 0 (§12-④). **정량 원전은 `ncube2026…`** 이지 이 편이 아니다 |
| *"계면상의 두께·연속성·성장속도를 못 본다"* | 🟡 **유효하되 상대방도 못 했다** | Guo 는 1 ns 에 **반응이 안 끝났다**(§12-⑤). 속도 측정 0 · 온도열 0 · 시간법칙 0 |
| *"정적 계면형성에너지만으로 계면의 실용성을 못 정한다"* | 🔴 **유효** | 우리는 **어떤 반응이 일어나는가**만 답한다. 그것이 우리 주장의 전부여야 한다 |
| *"운동학이 열역학보다 **더** 지배한다"* | ⛔ **이 논문에서 입증되지 않았다** | §3b. 원문은 *"불충분"* 까지만 말하고, **유일한 정량 축이 혼합 평균 인공물**이다(§12-②) |
| *"코팅 4조건"* | ⛔ **원문에 없다** | §3c. 리뷰의 종합이지 Guo 의 주장이 아니다 |
| *"hull 은 무용하다"* | ⛔ **원문이 정반대를 한다** | §3d. **hull 을 3회 명시적으로 추인**하고, 종 후보 집합 자체를 hull 로 자른다 |

**⇒ 한 줄 판정**: **비판은 "우리 도구의 적용범위" 에 대해서는 전면 유효하고, "우리 도구의 타당성" 에 대해서는
유효하지 않다.** 그리고 **리뷰가 옮기면서 세졌다** — 원전은 우리를 반증하지 않고 **보완을 요구**한다.

## 13b. ② **우리가 쓸 수 있는 방어 문장 (원문 근거와 함께)**

> **방어 1 — 도구의 자기 선언** (정공법)
> *"우리 계면 해석은 **어떤 분해 반응이 열역학적으로 열리는가**까지를 주장하며, 그 반응이 **얼마나 빨리 · 얼마나 두껍게 ·
> 어떤 형태로** 진행하는지는 주장하지 않는다."*
> 근거: 이 논문 Conclusion *"thermodynamic predictions alone are insufficient"* — **우리가 먼저 인용해 한계를 선언**한다.

> **방어 2 — 🔑 상대방이 우리 도구를 쓴다** (가장 강한 카드)
> *"운동학 연구 자신도 계면 안정성 판정에 **계면 반응에너지**를 근거로 든다 (Li₃YCl₆·Li₃InCl₆ / LiCoO₂ 에 대해
> **23 · 21 meV atom⁻¹**, *"indicating high chemical stability"*), 그리고 MD 가 관측한 **S_n 생성이 기존 열역학 해석과
> 일치한다**고 스스로 적는다. 즉 열역학 스크리닝은 **폐기 대상이 아니라 필요조건**이다."*
> 근거: 원문 §"Interfacial reaction and stability" 2문단 + §"Interfacial reaction" 의 refs 9·40 (Zhu 2015/2016).
> ⭐ **이 문장 하나가 §3d 의 결실이고, 우리 §B 의 위상을 지킨다.**

> **방어 3 — 산물 예측의 독립 검증**
> *"우리 grand-potential 이 Li₆PS₅Cl 산화경로에서 내놓는 **S**(2.256 V)와 **P₂S₇**(2.385 V)는,
> 같은 종이 독립적인 MLIP-MD 계면 시뮬레이션에서 황화물/충전 LiCoO₂ 계면의 생성종으로 관측된다."*
> 근거: 원문 `Fig. 4c` + *"agrees with previous thermodynamic analysis"*.
> ⚠ **계가 다르다**(Li₇P₃S₁₁·LGPS vs 우리 아지로다이트) — *"같은 화학공간의 황화물에서"* 로 한정해 쓴다.

> **방어 4 — 우리 축이 더 촘촘한 지점**
> *"운동학 연구는 충전 상태를 **두 점**(x = 0.5, 1.0)으로 본다. 우리는 **2.5–4.5 V 6점**으로 같은 축을 훑는다."*
> ⚠ 단 층위가 다르다 — 우리 것은 **구동력의 전압 의존**이지 열화 속도가 아니다. 반드시 이 단서를 단다.

> **방어 5 — 이미 우리가 그 격차를 재고 있다**
> *"계산 산화 onset **2.256 V** 와 실측 kinetic onset **2.5–2.9 V** 사이의 격차 자체가 운동학 여유의 크기다."*
> (`comparison_vs_ours.md` §B — **우리 자산**이고, 이 논문은 그 격차를 **메우지 않는다**)

> ⛔ **쓰면 안 되는 방어**: *"hull 이 맞다"*, *"운동학은 아직 신뢰할 수 없다"* —
> 첫째는 논점 이탈이고, 둘째는 §12 의 비판을 상대 논문 하나에서 일반화하는 것이라 방어가 안 된다.

## 13c. ③ **우리가 당장 할 수 있는 것** (비용 순)

| # | 할 일 | 비용 | 소득 |
|---|---|---|---|
| ① | **§Limitations 문단을 이 digest 로 쓴다** — "속도·두께·연속성·**Li 고갈**·**양이온 상호확산**" 5개를 이름 붙여 선언 | **0** | 리뷰어가 먼저 말하는 것을 막는다. §10-⑤ |
| ② | **§B 서술에 방어 2 를 삽입** (*"운동학 연구도 반응에너지를 쓴다"* + 23/21 meV/atom) | **0** | hull 방법의 위상 방어 |
| ③ | **NdPO₄ (및 우리가 예측한 CEI 산물)의 band gap 을 낸다** | **낮음** (기존 파이프라인) | Guo 의 *"전자절연 + 이온전도 = 부동태"* 칸을 **우리 숫자로** 채운다. §10-① |
| ④ | **기존 MD 궤적으로 Li 수 밀도 공간 히스토그램** (도핑계 vs 무도핑) | **낮음** (후처리만, `tools/ionic/` 확장) | 기전 ②를 **벌크 수준에서라도** 흉내내는 유일한 길. §10-② |
| ⑤ | **보호율 식의 두께 환산** — 생성 몰수 × 몰부피 ÷ 비표면적 → nm | **낮음** (산수) | `wu2026…` §J-20-4 가 이미 요구한 것. 이 편의 "계면상 두께" 공백과 같은 칸 |
| ⑥ | **계면 슬랩 파일럿 1건** (Li₆PS₅Cl(?) ‖ LiCoO₂(101), Zur–McGill + MCIA < 400 Å²) | **중간** | §H 계면 축을 여는 최소 단위. ⚠ **여는 순간 오차막대·시드·창 규약을 우리 표준으로 박아야 한다** (이 논문이 안 한 것) |
| ⑦ | ⛔ **하지 말 것**: 이 논문의 D 값을 우리 표에 넣는 것 · MACE-MP-0 로 갈아타는 것 | — | §12-② · §12-⑩ |

## 13d. ④ **추가로 구해야 할 논문**

| 우선 | 무엇 | 왜 |
|---|---|---|
| 🔴 **1** | **ref 7 — Haruyama, Sodeyama, Han, Takada, Tateyama, "Space–charge layer effect at interface between oxide cathode and sulfide electrolyte in ASSB", *Chem. Mater.* 26, 4248 (2014)** | **Li 고갈/공간전하의 원전**이다. Guo 의 기전 ② 는 이 논문의 재발견이고, `wu2026…` §4.6 이 *"ref 를 안 붙였다"* 고 우리가 표시해 둔 **Δμ_Li↔공간전하 원전 자리**가 바로 여기일 가능성이 높다 |
| 🔴 **2** | **ref 11 — Tateyama, Gao, Jalem, Haruyama, "Theoretical picture of positive electrode–solid electrolyte interface … from electrochemistry and semiconductor physics viewpoints", *Curr. Opin. Electrochem.* 17, 149 (2019)** | 공간전하 + 반도체물리 관점의 **리뷰**. 우리가 "Li 예산" 을 공간전하와 분리해 이름 붙이려면(§J-20-5) 이 편이 기준선 |
| 🟠 **3** | **ref 42 — Haruyama, Sodeyama, Tateyama, "Cation mixing properties toward Co diffusion at the LiCoO₂/sulfide interface", *ACS AMI* 9, 286 (2017)** | 양이온 상호확산의 **정량 원전**. ⭐ **이미 inbox 에 있다**: `8de8d802-10._Cation_Mixing_Properties…pdf` — **digest 미작성**. 우선 처리 대상 |
| 🟠 **4** | **ref 12 — Swift & Qi, "First-principles prediction of potentials and space-charge layers in ASSB", *PRL* 122, 167701 (2019)** | 공간전하를 **제1원리로 계산하는 방법**의 원전. 우리가 이 축을 열 때의 방법 사양 |
| 🟡 **5** | **ref 26 — Xie et al., "InterOptimus", *J. Energy Chem.* 106, 631 (2025)** | Guo 의 MACE 계면 정확도 주장(0.79 J m⁻²)의 출처이자, `wu2026…` `Fig. 11` 의 원전. **두 인용이 서로 다른 값을 말한다** — 원전에서 확정해야 한다 |
| 🟡 **6** | **ref 43 — Takahashi et al., *J. Power Sources* 226, 61 (2013)** | Li₃PO₄ 가 *"전자절연 + 이온전도"* 라는 §10-① 근거의 원전 |
| 🟡 **7** | **ref 8 — Kaeli, …, Chueh, "Decoupling first-cycle capacity loss mechanisms in sulfide solid-state batteries", *EES* 18, 1452 (2025)** | **실험 쪽**에서 계면 손실을 분해한 최신 편. 우리 §H 의 "실험축 요구사항" 을 아는 데 필요 |
| ⚪ **8** | ref 13 Tang/Ong 2018 (Na-ASSB 계면 제1원리) · ref 18 Ding 2016 (에피택시 기판 선택) | 계면 모델 구축 방법 원전 (우리가 슬랩을 만들 때) |

---

# 14. 우리 litdb 안에서의 자리

| 이웃 digest | 관계 |
|---|---|
| `wu2026_ml_driven_electrolyte_interface_design_review` | **이 편을 [132] 로 인용한 리뷰.** §3 이 그 인용을 검증했다 — **3건 중 1 정확 · 1 과장 · 1 없음** |
| `ncube2026_ionic_interdiffusion_lco_lgps_multiscale` | **같은 운동학 축의 정량 원전.** LCO‖LGPS 를 5층 사다리(DFT→AIMD→DeePMD→MLMD→phase-field)로 풀어 **원소별 계면 D 6개 + 두께 시간법칙 `0.265·t^0.155`** 를 냈다. ⇒ **Guo 가 정성으로 본 것을 Ncube 가 정량으로 낸다.** 기전 ③ 인용은 Ncube 로 간다 |
| `richards2016_interface_stability_pseudobinary` · `zhu2015_esw_grand_potential_origin` | **우리 §B 방법의 원전.** Guo 가 refs 10·9 로 **인용하고 추인**한다 (§3d) |
| `wang2026_interface_stability_kinetics_sulfide_assb` | 같은 해의 **대규모 hull 스크리닝 + AIMD 1계**. Guo 와 정반대 배분(열역학 다수 + 운동학 1계) |
| `kim2025_impedance_decoupling_tlm_assb` | **임피던스를 실제로 분해하는 편**(TLM). Guo 가 못 하는 축이 여기 있다 |
| `haruyama 2017` (inbox `10.` , **미digest**) | ref 42 원전 — §13d-3 |

---

**digest 작성**: 2026-09-22 · litdb-curator · 본 그림 목록 §0b

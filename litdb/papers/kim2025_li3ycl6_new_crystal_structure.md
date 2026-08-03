# New crystal structure of Li₃YCl₆: structural relationship and ionic conductivity for solid-state electrolytes — Ji Hoon Kim (Rare Metals 2025)

> slug `kim2025_li3ycl6_new_crystal_structure` · DOI `10.1007/s12598-024-03069-x` · type `순수 DFT + AIMD + CSP(CALYPSO/PSO)` ·
> *Rare Met.* 2025, **44**(4), 2366–2378 · 본문 13 pp + **SI(업로드 .docx = Supporting Information 실물)** · digested `2026-07-28` · status ✅ (본문 + SI Note S1–S3 + Table S1 전문 정독)
> elements: Li, Y, Cl, Ge, P, S
> methods: DFT, AIMD
>
> **저자** Ji Hoon Kim¹, Byeongsun Jun², Yong Jun Jang², **Chi Ho Lee**³*, **Sang Uck Lee**¹*
> ¹성균관대 화학공학(suleechem@skku.edu) · ²현대자동차 (Hwasung/Suwon) · ³Texas A&M Artie McFerrin ChemE (cmsholee@tamu.edu)
> 접수 2024-07-11 · 수정 2024-09-10 · 수리 2024-09-21 · 온라인 2025-02-25 · © Youke Publishing
> 자금: **MOTIE P0022336** + RS-2024-00437260 + **현대자동차**
>
> ⚠⚠ **이 논문은 우리 축이 아니다.** Li₃YCl₆ = **할라이드** SE, 우리 캠페인 = **황화물 argyrodite(Li₆PS₅Cl)**.
> `kb/open_items.md` 이상욱 랩 위시리스트 **6순위(낮음, "CSP 보조")**. 따라서 이 digest는
> **물성값 수확이 아니라 방법론·구조 개념 수확**이 목적이고, **모든 수치는 우리 물성 4축에 수치로 편입 금지**다
> (`litdb/INDEX.md` ⚠EXTERNAL 규율 준용).

---

## 0. 이 digest를 읽는 법 — 우선순위 지도

사용자가 지정한 5개 질문에 맞춰 분량을 배분했다.

| 질문 | 답이 있는 절 | 한 줄 답 |
|---|---|---|
| ① CSP 방법 — MTP 썼나? 랩 JACS 2025와 같은 파이프라인? | **§5** | **아니다. CALYPSO + PSO + 직접 DFT.** MTP·USPEX·active-learning 전부 **없음** → 심포지엄 덱 표가 틀렸다(두 번째 덱 오류) |
| ② "structural relationship"이 정확히 무엇인가 | **§6** | **군-부분군(Bärnighausen) 관계가 아니다.** [YCl₆]³⁻ 팔면체의 **회전·틸트·이동**으로 서로를 오가는 **정성적 변위형 변환 지도**(hcp_2를 허브로) |
| ③ σ 방법과 신뢰도 | **§8** | **AIMD**(VASP/PBE/Γ/2 fs/NVT-NH/600–1000 K 5점/NE Haven=1). **바로 그 "27배 틀리는" 계**다 — 논문 스스로 hcp_1에서 계산 12.6 vs 실험 0.03–0.5(=**25–420×**)를 인정하고, 그 원인을 **antisite**로 돌린다. 오차막대 0·시드 1 |
| ④ 무질서/점유율 처리 | **§10·§11** | **enumlib(Hart–Forcade) 열거 → DFT 완화 → 안정성으로 배열 1개 선택**(앙상블 없음). 무질서는 별도로 **점결함(Li↔Y antisite) 2배열**로만 재도입. 우리 음이온 무질서와 **부격자·부호가 반대** |
| ⑤ 이식 가능/금지 | **§15** | 가능 = 열거 레시피·**차원성×결함내성(퍼콜레이션)**·Li–Li 거리 서술자·자동 실행길이·표 양식 / 금지 = **모든 σ·E_hull·E_anti 절대값**·"hcp>ccp" 명제·antisite 서사 |

---

## 1. 한 줄 요약

**"조성을 Li₃YCl₆로 고정하고 골격만 5개로 바꿔 보니, 할라이드 SE 분야의 통념인 'ccp 골격이 hcp보다 전도가 좋다'가 뒤집힌다"** —
기보고 hcp 3종 + ccp 1종을 모두 Li₃YCl₆로 표준화해 AIMD로 재평가하니 ccp가 최하위였고,
CALYPSO/PSO 결정구조예측(CSP)으로 찾은 **새 C2 골격(hcp_4)** 이 **2D Li 확산**을 가져 최고 σ를 준다.
덤으로 **hcp_1의 이론–실험 괴리(계산 ≫ 실험)를 Li–Y antisite가 1D 채널을 막는 것으로 설명**한다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 물질 | **Li₃YCl₆ (LYC)** 단일 조성, 골격 5종 |
| 연구유형 | **순수 계산**(자체 실험 0). DFT 정적 + AIMD + CSP |
| 실험 대조 | 전부 **문헌 소환값**(Asano 2018 hcp_1 σ 0.51 mS/cm; Park 2020 hcp_3 1.1 mS/cm; LGPS 12 mS/cm) |
| 랩 정체 | **이상욱(SKKU) 랩 = 우리 위시리스트 그 랩.** 제1저자 **Ji Hoon Kim = `kim2026_hts_li3sc2po43_coating_midni_ncm` 제1저자 동일인**, 자금 **MOTIE P0022336 동일 과제** |
| 산업 파트너 | **현대자동차** 공저(Byeongsun Jun, Yong Jun Jang) — 랩의 ASSB 과제가 완성차 연계임을 보여주는 증거 |
| SI 정체 | 업로드된 `.docx`는 원고가 아니라 **Supporting Information 실물**(Note S1–S3, Table S1, Fig S1–S12 캡션, ref [1]–[7]). 본문 PDF만으로는 못 읽는 **무질서 처리·σ 식·antisite 정의**가 전부 여기 있다 → 이 digest의 §8·§10·§11은 SI 기반 |

**우리 litdb 안 위치**: 같은 물질(Li₃YCl₆)을 다루는 **직계 형제 digest가 이미 있다** —
`papers/schlem2020_li3mcl6_cation_site_disorder.md`(Zeier, 실험 + 정적 DFT). §10에서 이 둘이 **정면 충돌**한다.
우리 그룹 `papers/cha2024_dualcompatible_halide_ncm_lpscl_interface.md`의 **LYC 코팅**도 같은 물질이다.

---

## 3. 문제 설정 — 무엇을 반박하는가 (§1 Introduction)

### 3.1 통념

할라이드 SE Li₃MX₆(M = Y³⁺, Sc³⁺, In³⁺, Er³⁺; X = Cl⁻, Br⁻, I⁻)는 **σ ~1 mS/cm급 + 산화 안정성 우수**로 급부상했고,
그 구조는 **halide 음이온의 조밀쌓임 방식**으로 두 부류로 갈린다.

- **ccp** (cubic close packed) = **ABCABC** 스택
- **hcp** (hexagonal close packed) = **ABAB** 스택

> 통념: **"ccp가 hcp보다 σ가 높다"** — 근거로 인용되는 것들:
> - **Asano 2018 [29]**: Li₃YCl₆(hcp) **0.51** vs Li₃Y**Br**₆(ccp) **1 mS/cm** → "ccp가 Li 경로 수가 많아 유리"
> - **Liang/Sun 2020 JACS [31]**: Li_xScCl_{3+x}(ccp)의 우수한 σ를 제1원리+실험으로 확인
> - **Park/Jung 2021 CEJ [36]**: Li₃InCl₆의 높은 σ = ccp의 **3D 채널** 덕
> - **Qiu 2021 JPCC [50]**: 이론 시뮬레이션 — **ccp = 3D 경로, hcp = 1D 경로**

### 3.2 저자들의 반박 논리 (그리고 이건 실제로 옳은 지적이다)

> *"these findings primarily reflect the characteristics of the synthesized material rather than prove the inherent superiority of the ccp configuration over the hcp"*

**핵심 = 교란변수(confounding)**. Asano의 비교는 packing만 바꾼 게 아니라 **음이온까지 Cl→Br로 바꿨다**.
Li₃InCl₆은 packing만이 아니라 **양이온까지 In**이다. 즉 통념의 근거는 전부 **조성과 골격이 함께 움직인 비교**다.

→ 이 논문의 설계: **조성을 Li₃YCl₆ 하나로 못박고 골격만 5개로 바꾼다.** 이건 방법론적으로 정직한 설계이고,
우리 db가 늘 강조하는 "**변수 하나만 바꿔라**"(comp1↔modelc가 Cl·Li공공·S를 동시에 바꾸는 비통제 쌍이라는 자기비판,
`kb/concepts/ordered_vs_disordered.md` §우리캠페인적용)와 정확히 같은 규율이다.

> ⚠ 단 이 설계는 **교란을 하나 없애고 다른 하나를 들여온다**: hcp_2·hcp_3·ccp_1을 Li₃YCl₆로 표준화한 순간
> 그 셋은 **실제로 합성된 물질이 아닌 가상 구조**가 된다. Table 1의 "hcp_3 = 18.8 mS/cm"는
> Li₂.₅₃Er₀.₅₃Zr₀.₄₇Cl₆(실측 1.1)의 σ가 **아니다.** 논문이 이걸 §3.4 끝에서 한 번 흐린다(§16-6).

---

## 4. 다섯 골격 카탈로그 (Fig 1, Fig S1, Fig 2b, Table S1) ★ 우선순위 ②의 기초

| 라벨 | 원 출처 물질 | 공간군 (번호) | packing | Wyckoff (Fig 1) | 이 논문의 계산 셀 (SI Note S1) |
|---|---|---|---|---|---|
| **hcp_1** | Li₃YCl₆ (**Asano 2018**) | **P3̄m1** (164) | hcp | Li⁺ 6h, 6g · Y³⁺ **1a, 2d** · Cl⁻ 6i | **3Y + 9Li** = Li₉Y₃Cl₁₈ (3 f.u., 30원자 — 유도) |
| **hcp_2** | Li₃**Yb**Cl₆ | **Pnma** (62) | hcp | Li⁺ 8d · Yb³⁺ 4c · Cl⁻ 4c, 8d | Yb→Y, **8d Li 16자리 중 12개 선택** (4 f.u.) |
| **hcp_3** | Li₂.₅₃**Er**₀.₅₃**Zr**₀.₄₇Cl₆ (**Park**) | **Pnma** (62) | hcp | Li⁺ 8d · Er³⁺/Zr⁴⁺ 4c · Cl⁻ 4c, 8d | Er·Zr→Y, occ 0.770 만점유 / occ 0.193 제거 / 8d(0.3) 절반 선택 → **12Li** |
| **ccp_1** | Li₃**Sc**Cl₆ (**Liang/Sun 2020**) | **C2/m** (12) | **ccp** | Li⁺ 2d, 4g, 4h · Sc³⁺ 2a · Cl⁻ 4i, 8j | Sc→Y, 부분점유 2d 4개 + **4h Li 제거 → 6Li** (2 f.u.) |
| **hcp_4** ★신규 | **CALYPSO 예측** | **C2** (5) | **hcp** (Fig S2 AB 스택 확인) | Li 4c×2, 2b×2, 2a×2 · Y 4c, 2a · Cl 4c×9 | **Table S1 전좌표 공개** (아래) |

**hcp_4 격자 (Table S1)**: a = **13.9336** / b = **11.3456** / c = **8.9487 Å**, α = γ = 90°, **β = 105.15°**, 공간군 **C2**.
Li 6자리·Y 2자리·Cl 9자리 전부 occ = 1.

> ⚠ **Table S1 자체 검산 불일치**: 표에 인쇄된 다중도를 그대로 더하면 **Li 16 · Y 6 · Cl 36** = Li₂.₆₇YCl₆ 로
> Li₃YCl₆(18:6:36)와 맞지 않는다. Li3(0.1806, 0.9300, 0.5000)이 **일반위치인데 "2b"로 표기**돼 있어,
> 이것을 4c로 읽으면 정확히 **Li 18 · Y 6 · Cl 36 = Li₃YCl₆ × 6 f.u.(60원자)** 가 된다.
> **표기 오류로 보이나 원문만으로 확정 불가** — 재현하려면 저자 CIF 요청 필요. (Cl4 행에도 "0 0.6372" 중복 0 오타)

### 골격별 구조 특징 (본문 §3.1)

- **hcp_1**: [YCl₆]³⁻ 팔면체(Y³⁺ + Cl⁻ 6개)가 hcp 음이온 부격자에. **Y·Li 점유율이 합성조건에 따라 변한다**([53] Schlem 2021 Chem Mater 인용). 같은 삼방 골격이 Zr 치환[51]·Tb–Tm[33,34,75]에서도 나타남 = 골격 범용성.
- **hcp_2**: Yb³⁺/Lu³⁺/Y³⁺/Er³⁺/Zr⁴⁺를 금속자리에 수용. **팔면체가 c 방향으로 균등 정렬** — hcp_1과 구별되는 배열.
- **hcp_3**: hcp_2와 유사하나 **팔면체가 약간 틸트**되고 **팔면체 골격 안에 Li 자리가 추가**로 있어 σ 1.1 mS/cm(실측)로 hcp 중 최고.
- **ccp_1**: C2/m, ccp 부격자.
- **hcp_4**: [YCl₆]³⁻ 팔면체가 **모두 같은 방향으로 정렬**하고 그 사이에 Li가 들어가 **Li-layered 배열**(층상)을 이룬다.

---

## 5. ★우선순위 ① — CSP 방법 (본문 §2 끝, Fig 2a)

### 5.1 실물 명세 (원문 그대로)

> *"To predict the crystal structure of Li₃YCl₆, we used the **particle swarm optimization (CALYPSO)** methodology [69, 70]
> applied in various structural systems such as surfaces [71,72], three-dimensional crystals [69], battery interface systems [73]
> and crystal structure prediction [74]. The number of **structural generations and population per generation were determined to be 50 and 100**, respectively."*

**Fig 2a 캡션**: *"crystal structure prediction is conducted up to 50 generations **with DFT calculation**"*

| 항목 | 실물 |
|---|---|
| CSP 엔진 | **CALYPSO** (Y. Wang / Y. Ma, PRB 2010 + CPC 2012) · **PSO(입자군집최적화)** |
| 평가 엔진 | **직접 DFT** (VASP) — Fig 2a 캡션 명시 |
| 세대 × 개체 | **50 × 100** (= 최대 5,000 구조) |
| **MLIP(MTP/SevenNet)** | **없음** |
| **USPEX / GA** | **없음** |
| **active learning / γ_select** | **없음** |
| 선별 기준 | *"the structure that exhibited the **lowest enthalpy** over 50 generations"* |
| 후처리 | **RDF**(원자쌍별)로 신규성 판정(Fig S3) + **E_hull**(Table 1) + AIMD |

### 5.2 ★ 판정: 심포지엄 덱이 **틀렸다** (두 번째 덱 오류)

`litdb/talks/lee2026_skku_mlip_materials_design.md` 의 5갈래 표는 이렇게 적혀 있다:

| 갈래 | 엔진 | 내용 | 출처 |
|---|---|---|---|
| Designing novel materials | **MTP** | **CSP (USPEX + GA + active learning)** | JACS 2025, 147, 47381; **Rare Metals 2025, 44, 2366** |

**실물은 CALYPSO/PSO + 직접 DFT다.** MTP도 USPEX도 GA도 active learning도 이 논문엔 한 글자도 없다.

**해석(추론, 증거 병기)**: 덱의 "USPEX+MTP+active learning" 플랫폼은 **JACS 2025(Li₂SiS₃) 쪽 서술**이고,
덱이 같은 셀에 Rare Metals를 함께 묶으면서 파이프라인까지 한 덩어리로 표기된 것으로 보인다.
시점도 정합한다 — 이 논문은 **2024-07 투고**로 MTP-CSP 플랫폼(JACS 2025)보다 앞선다.
→ **랩이 CSP 파이프라인을 최소 2개 운영**한다는 것이 실물이 말해주는 사실:
**(구) CALYPSO/PSO + 직접 DFT** ↔ **(신) USPEX/GA + MTP + active learning**.

> 🔑 이건 **현재 유효한 덱-vs-실물 불일치 중 하나**다(2026-08-03 기준).
> ⚠ 이전에 함께 세던 `kim2026` digest §2의 "덱 17,233 Li-P-S-O → 실물 17,230 Li·O" 건은 **철회**됐다 —
> 덱 원문이 `17,230 Li, O` 로 논문과 일치했고, 틀린 쪽은 우리 저해상도 전사였다
> (`litdb/talks/lee2026_skku_mlip_materials_design.md` §15b). **"덱은 정본이 아니다"** 규율
> (`litdb/talks/README.md`)의 실증 사례로는 이 CSP 엔진 건이 남는다.
> 우리가 T1(외삽 등급 대리지표)을 설계할 때 "이상욱 랩은 CSP에도 MTP를 쓴다"를 전제로 삼으면 안 된다 —
> **적어도 이 논문에서는 안 썼다.**

### 5.3 CSP 결과의 자기평가 (그리고 그 논증의 약점)

- hcp_4는 **"metastable"** 로 규정된다. 그 근거로 논문이 드는 것: *"attributed to its **low space group number (5)**"*.
  > ⚠ **비논리.** 공간군 번호(대칭성 낮음)는 준안정성의 근거가 아니다. 저대칭 바닥상태는 흔하다.
  > 실제 준안정 근거는 **E_hull 27 meV/atom**(Table 1)이지 공간군 번호가 아니다. 문장 자체가 느슨하다.
- **신규성 검증 = RDF**(Fig S3): 모든 골격에서 **Cl–Cl 쌍 분포는 거의 동일**(= 다 [MCl₆]³⁻ 팔면체니 당연),
  그러나 **Y–Y·Li–Li 쌍에서 hcp_4가 유의하게 이탈** → "이건 다른 구조다"를 정량화.
  > 🔑 **이 RDF-차분 신규성 판정은 우리가 그대로 쓸 수 있는 값싼 절차다.** 구조 두 개가 "정말 다른가"를
  > 공간군 라벨이 아니라 **어느 원자쌍이 다른가**로 답한다 — 우리 disorder cfg 앙상블에서
  > "cfg0과 cfg2가 실질적으로 다른 배열인가"를 판정하는 데 즉시 전용 가능.

---

## 6. ★우선순위 ② — "structural relationship"의 실체 (Fig 3)

### 6.1 이것은 **군-부분군 관계가 아니다**

논문에 **Bärnighausen 트리·지표(index)·변환행렬·distortion mode(ISODISTORT/AMPLIMODES) 분석은 없다.**
있는 것은 **[YCl₆]³⁻ 팔면체를 강체(rigid body)로 보고, 그 회전·틸트·평행이동으로 골격을 서로 옮기는 정성적 지도**다.
**허브(기준 구조) = hcp_2 (Pnma)**, 나머지 넷이 각각 hcp_2로 가는 경로를 그린다.

### 6.2 변환 지도 4개 (Fig 3a–d)

Fig 3의 삼각형 색 = **[YCl₆]³⁻의 배향**(위/아래).

| 경로 | 필요한 조작 | 난이도(논문 서술) |
|---|---|---|
| **(a) hcp_1 → hcp_2** | [YCl₆]³⁻ 팔면체를 **반대 배향으로 회전**(노랑·파랑 원 → 빨강·파랑 삼각형) + 그 결과 삼각형들을 **c 방향으로 위/아래 이동** | 회전 + shift |
| **(b) hcp_3 → hcp_2** | 팔면체를 **약간 틸트**(초록·주황 삼각형 → 파랑·빨강) + hcp_1과 **같은 방식의 [YCl₆]³⁻ shift** | **가장 쉬움** — *"slight and simple changes are plausible due to the same anion-packing type and Pnma space group"* |
| **(c) ccp_1 → hcp_2** | **회전 → shift(top view 정렬) → side view에서 아래로 이동해 지그재그 생성 → 격자 자체가 사방정으로 mutate** | **가장 어려움** — *"more extensive modifications"*, packing이 ccp↔hcp로 바뀌는 **재구성형(reconstructive)** |
| **(d) hcp_4 → hcp_2** | 보라→파랑 팔면체 **회전** + **아래로 이동해 hcp_2의 지그재그 패턴에 정렬** — *"similar to the adjustments observed in ccp_1"* | 중간 |

### 6.3 이 지도로 논문이 주장하는 것 — 그리고 그 한계

> *"This transformation clearly underscores the **feasibility of synthesizing** the novel hcp_4 structure based on
> **relatively minor modifications to existing frameworks**."*

**논지 구조**: "hcp_4는 기존 hcp_2에서 회전+이동 몇 번이면 닿는다 → 그러니 합성 가능하다."

> ⚠⚠ **여기가 이 논문에서 가장 약한 논증이다.**
> 1. **에너지 장벽이 계산되지 않았다.** 다형 간 전이 NEB도, phonon(동적 안정성)도, nudged solid-state NEB(SS-NEB)도 없다.
>    "기하학적으로 가깝다"는 **운동학적 근접성**이지 **열역학·동역학적 접근성**이 아니다.
>    강체 회전은 종종 **에너지 상 매우 비싼** 협동 운동이다.
> 2. **합성 경로가 제안되지 않았다.** 어떤 전구체·온도·압력에서 hcp_4로 갈지 한 줄도 없다.
> 3. 그럼에도 **정합적으로 남는 부분**: (b) hcp_3↔hcp_2가 "같은 Pnma·같은 packing"이라 쉽다는 판단은 옳고,
>    (c) ccp↔hcp가 **음이온 스택 자체를 바꾸는 재구성형**이라 어렵다는 판단도 결정화학적으로 옳다.
>    **즉 지도의 위상(topology)은 신뢰할 만하고, 그 위에 얹은 "합성 가능" 결론이 과하다.**

### 6.4 우리가 가져갈 형식

**"공통 구성단위(building block)를 고정하고, 그 단위의 배향·연결 방식으로 다형을 계층화한다"** — 이 문법 자체는 유용하다.
같은 랩 심포지엄 덱의 **Li₂SiS₃ corner-sharing(안정, 10⁻⁴) vs edge-sharing(준안정, 2.4 mS/cm)** 서사와 **완전히 같은 문법**이고,
`kim2026` digest의 **Li₃Sc₂(PO₄)₃ α vs γ (σ 30배)** 와도 같다.

> 🔑 **랩 전체를 관통하는 단일 명제가 확인된다: "Composition ≠ Structure — 같은 조성 안에서 다형/연결방식이 σ를 자릿수로 가른다."**
> 이 논문은 그 명제의 **할라이드 판**이고, JACS 2025는 **황화물 판**, Nano Convergence 2026은 **인산염 판**이다.
> 우리 캠페인(host 고정 + 도핑)은 이 축과 **직교**한다 — 열위가 아니라 문제설정이 다름(덱 분석 §10 판정 유지).

---

## 7. 열역학·전자구조 (Table 1, Fig S4)

### Table 1 — 5골격 전수 (동일 Li₃YCl₆ 조성)

| 파라미터 | hcp_1 (P3̄m1) | hcp_2 (Pnma) | hcp_3 (Pnma) | ccp_1 (C2/m) | **hcp_4 (C2)** |
|---|---:|---:|---:|---:|---:|
| Energy/atom (eV/atom) | −4.32 | −4.32 | −4.32 | −4.32 | **−4.31** |
| **E_hull (meV/atom)** | 24 | 23 | **17** | 21 | **27** |
| Close packing | hcp | hcp | hcp | **ccp** | hcp |
| σ_300K (mS/cm) ⛔ | 12.6 | 10.2 | 18.8 | **3.4** | **38.5** |

**논문의 읽기**: 모든 구조가 E_hull < 30 meV/atom → *"potential synthesizability under specific experimental conditions"*;
실험 합성된 hcp_1(24)과 예측 hcp_4(27)의 차이가 **3 meV/atom뿐** → hcp_4도 만들 수 있을 것.

> ⚠ **우리 읽기 (더 엄격)**:
> 1. **E_hull 전 범위가 17–27 meV/atom = 스팬 10 meV/atom.** 이는 PBE 다형 랭킹 정확도와 상온 kT(25.9 meV) **양쪽 아래**다.
>    → "hcp_4가 hcp_1보다 3 meV/atom 불안정"은 **의미 있는 차이가 아니다**(저자 주장과 같은 방향, 더 강하게).
>    동시에 **"hcp_3가 가장 안정(17)"도 마찬가지로 주장 불가**.
> 2. **역설이 하나 남는다**: 실제로 가장 널리 합성되는 건 hcp_1(24)인데 그들 표에선 **hcp_3(17)가 최저**다.
>    논문은 이 불일치를 **논의하지 않는다.**
> 3. E_hull의 **참조 hull 출처(MP 버전·엔트리 집합)가 미기재** → 재현 불가.

### 전자구조 (Fig S4)

- 본문 서술: *"the structures examined show **wide bandgaps**, primarily attributed to **chlorine's high standard reduction potential**"*;
  CBM/VBM ↔ 환원/산화 전위 관계가 전기화학창을 지배; **hcp_4가 후보 중 gap 최소이나 차이는 미미**하고 할라이드 특유의 높은 전기화학 안정성은 유지.
- **⛔ 수치는 본문·Table에 없다.** Fig S4(그림)에만 있고 우리는 그 그림을 못 봤다 → **gap 값 = n/a**.
- ⚠ 오타 2건: 본문 *"valence band **minimum** (VBM)"*, Fig S4 캡션 *"CBM: conduction band **maximum**"* — 둘 다 반대말.

> **우리 규율 적용**: 우리 canonical gap(comp1 2.066 / modelc 2.099 eV, fixed-occ nscf)과 **비교 자체가 불가**하다
> — 값이 없고, 물질군이 다르고, 우리 PBE gap은 과소평가·무질서 민감이다. "**둘 다 wide-gap 절연체**" 수준만 서술 가능.

---

## 8. ★우선순위 ③ — σ 방법과 신뢰도 (§2, SI Note S2, Fig S5)

### 8.1 파이프라인 전문 (SI Note S2 eq 1–4)

```
AIMD 궤적
  → MSD(t) = (1/N) Σᵢ ⟨|rᵢ(t+t₀) − rᵢ(t₀)|²⟩                     (eq 1)
  → D = MSD / (2·d·t)          [d = 차원수]                        (eq 2)
  → D(T) = D₀·exp(−Ea/kT), Ea = log D vs 1/T 선형회귀 기울기        (eq 3)
  → 300 K로 외삽
  → σ(T) = ρ·z²·F² /(R·T) · D(T)     ← Nernst–Einstein, Haven 보정 없음 (eq 4)
```

### 8.2 AIMD 셋업 전수

| 항목 | 값 | 출처 |
|---|---|---|
| code | **VASP 5.4.4** | §2 |
| functional | **GGA-PBE**, PAW | §2 |
| **vdW 보정** | **없음** (언급 없음) | §2 |
| ecut (정적 완화) | **500 eV** | §2 |
| k-mesh (정적 완화) | **Monkhorst, "64 Å ≤ k-point mesh" 규약**(역격자 각 축) | §2 |
| 힘 수렴 | **< 0.04 eV/Å**, 격자·내부좌표 **모두** 완화 | §2 |
| **AIMD k-mesh** | **Γ-centered 1×1×1** | §2 |
| **AIMD 앙상블** | **NVT, Nosé–Hoover** | §2 |
| **Δt** | **2 fs** | §2 |
| **온도** | **600–1000 K, 100 K 간격 = 5점** → 300 K 외삽 | §3.4, Fig S5 |
| **총 시뮬레이션 길이** | **미보고** — *"determined **automatically** using our own convergence criteria, such as the **total effective ion hops** and **moving standard deviation**"* [67 = He/Zhu/Epstein/**Mo**, npj Comput Mater 2018] | §2 |
| **셀 크기** | **미보고** ("we followed the guidelines of other computational studies [11,64–66] for cell size, spin, time step, temperatures") | §2 |
| **시드 수 / 오차막대** | **1 / 없음** (표·그림 어디에도 ±) | 전체 |
| **부피** | 완화 부피(fully relaxed geometry) 고정 NVT | §2 |
| MSD 창 | 미보고 (Fig 4·5의 MSD는 **0–200 ps** 전 구간 표시) | Fig 4, 5 |

> 🔑 **형식은 우리와 같다.** 우리도 MSD → D → Arrhenius → **NE(Haven=1)** → 300 K다.
> **온도창도 사실상 같다** — 우리 600/800/1000 K 3점 ⊂ 그들 600–1000 K 5점.
> 다른 것은 **힘 엔진 하나**: 그들 **AIMD(PBE)** ↔ 우리 **MLIP-MD(UMA-s-1p1 omat)**.
> → `our_dft_baseline.md`의 "우리 Ea·D는 AIMD가 아니라 MLIP-MD" 경고를 그대로 적용해 **"둘 다 AIMD"라 부르지 말 것.**

### 8.3 ★ 신뢰도 해부 — "AIMD가 27배 틀리는 계"가 맞다

**논문 스스로 괴리를 인정한다** (§3.5, Table 2):

| | E_anti (meV/atom) | **σ 실험 (mS/cm)** | **σ 계산 (mS/cm)** | 배율 |
|---|---:|---:|---:|---:|
| **Li₃YCl₆ (hcp_1)** | 17.6 | **0.03–0.5** | **12.6** (blocked-c 시 0.6) | **25–420×** 과대 |
| **LGPS** | 32.2 | 12 | 12–13 | ~1× (일치) |

이건 사용자가 준 교차참조 — **`lee2024` ESI Table S1: Li₃YCl₆ AIMD 14 / MTP_optB88 0.56 / 실험 0.51** — 와 **정확히 같은 현상**이다
(⚠ 그 표는 우리 repo `kb/open_items.md` 기록값이고 이 PDF에는 없다 — 출처 분리).

**두 설명이 같은 랩 안에서 충돌한다:**

| 설명 | 주장 | 근거 | 문제 |
|---|---|---|---|
| **A. 이 논문 (2025)** | **antisite가 원인.** 실물 결정엔 Li–Y antisite가 있어 1D 채널이 막힌다 → 실험 σ가 낮은 것이지 계산이 틀린 게 아니다 | E_anti 17.6 ≪ LGPS 32.2; antisite 1개 넣으면 12.6→3.6, c 완전차단 시 0.6 ≈ 실험 0.5 | ①**hcp_4엔 E_anti를 계산조차 안 했다**(§10.4) ②"c 완전차단"은 **모델이 아니라 손으로 끈 것** ③Schlem Rietveld와 충돌(§10.5) |
| **B. `lee2024` (같은 랩)** | **방법이 원인.** 같은 pristine 구조에 **MTP_optB88**을 쓰면 **0.56 ≈ 실험 0.51**이 그냥 나온다 | 8개 계에서 MTP_optB88이 실험과 정합, 크게 틀리는 쪽은 AIMD | 그렇다면 **A의 antisite 설명은 불필요**해진다 — pristine에서 이미 맞으니까 |

> 🔑🔑 **논리적 귀결**: B가 옳다면 A의 결함 서사는 **과잉설명**이다. A가 옳다면 B의 MTP는 **우연히 맞은 것**이 된다
> (결함 없는 구조로 실험값을 재현했으므로). **둘 다 참일 수는 없다** — 적어도 "AIMD-PBE의 12.6이 물리적으로 옳고
> 실험 0.5는 결함 탓"이라는 A의 강한 형태는 B와 양립하지 않는다.
> **이 논문 단독으로는 판정 불가**이며, 우리는 **미판정으로 기록**한다.

**추가로 우리가 짚는 통계 문제:**

1. **He/Mo(2018)를 실행길이 결정에만 쓰고, 그 논문의 본론인 *불확실도*는 보고하지 않았다.**
   그 방법론의 요지 자체가 "AIMD 확산계수는 통계 분산이 크다"인데, 채택한 것은 수렴 판정뿐이고
   **σ에 오차막대가 하나도 없다.** → 헤드라인인 **hcp_4 38.5 vs hcp_3 18.8 = 2.05×** 가 통계 잡음 밖이라는 증거가 **없다**.
2. **5점 Arrhenius를 600→300 K로 외삽** = 온도 2배 밖. `kim2026`에서 같은 랩이 800–1200 K 외삽에
   **신뢰구간 0.01–2.4 mS/cm(2자릿수 반)** 를 붙인 바로 그 절차다. **여기엔 그 구간이 아예 없다.**
3. **Γ-only + (아마도) 30–60원자 셀 + Li 9–18개.** 셀 크기 미보고라 확정 못 하지만,
   SI Note S1의 관계셀을 그대로 썼다면 **hcp_1은 Li 9개**로 MSD를 낸 것이 된다 — 극도로 얇은 통계.
4. **단일 배열·단일 시드.** 우리 규율("단일 config 판정 금지", `ordered_vs_disordered.md` §8)에 정면으로 걸린다.

> ⛔⛔ **결론: 이 논문의 σ 절대값은 인용 금지.** 비율도 오차막대가 없어 조심해야 하며,
> **"ccp_1 3.4 → hcp_4 38.5 = 11×"** 같은 큰 비율만 **정성 방향**으로 인용 가능하다.

---

## 9. Li 확률밀도·MSD·채널 기하 (Fig 4, S6–S11)

### 9.1 Fig 4 — 5골격 × (구조 / Li 확률밀도 등가면 / 방향분해 MSD), **600 K, 200 ps**

| 골격 | Li 확산 차원 | 관찰 (본문 §3.4) |
|---|---|---|
| **hcp_1** | **1D (c축)** | a·b 방향은 **같은 층의 [YCl₆]³⁻ 2개가 정렬해 막는다** — 큰 팔면체 때문에 격간 자리가 작음. MSD도 c가 압도. [50]과 일치 |
| **hcp_2** | **준-2D (b, c)** | a 방향은 hcp_1처럼 막힘. **b·c는 Li–Li 반발이 완화돼 더 잘 흐름**. 단 총량은 hcp_1의 1D 채널보다 **적어** σ 10.2 < 12.6 |
| **hcp_3** | 다방향 | 같은 층 [YCl₆]³⁻ 2개 구조라 낮을 것 같은데, **팔면체 틸트 + 추가 사면체 Li 자리**가 경로를 살림 → hcp 중 최고 |
| **ccp_1** | **1D (c축)** + **trapped** | a·b는 **완전 차단**(Fig 4d에 "Trapped" 표시된 붉은 원). c로만 1D. → **최하 3.4** |
| **hcp_4** | **2D (a–c 면)** | Fig 4e·S10. 이 논문의 결론 |

> 🔑 **최대 반전**: 통념이 "ccp = 3D"라 했는데, 이들 계산에선 **ccp_1이 오히려 1D + 트랩**이다.
> 그리고 "hcp = 1D"라 했는데 hcp_2는 준-2D, hcp_4는 2D다. **packing 라벨이 차원성을 결정하지 않는다**는 것이
> 이 논문의 진짜 물리적 메시지이며, 이 부분은 σ 절대값과 무관하게 살아남는다.

### 9.2 채널 기하 (Fig S11) — **정의가 SI 캡션으로 확정됨** ★

> Fig S11 캡션: *"Li-ion diffusion channels of a hcp_1 … e hcp_4. **The closer distances between Li-ion enable easy migration
> due to reduced activation energy** in the crystal structures"*

→ 본문이 "channel size"라 부르는 값은 **병목(window) 직경이 아니라 인접 Li 자리 사이 거리(=점프 거리)** 다.
**가까울수록 좋다**(장벽↓). 본문만 읽으면 "큰 채널이 나쁘다"로 읽혀 혼란스러운데, SI 캡션이 이를 정리한다.

| 골격 | Li–Li 거리 | 논문 해석 |
|---|---|---|
| hcp_1 | **3.0 Å** (c축 1D 채널) / 다른 방향 **3.8 Å** | 3.0은 통하고 3.8은 안 통함 |
| hcp_2 / hcp_3 | 전 방향 짧음; **hcp_3가 최단 2.2 Å** | 같은 Pnma인데 hcp_3가 σ 크게 높은 이유 |
| ccp_1 | **전 방향 3.8 Å** | *"larger size complicates overcoming the activation barrier"* → ccp 최하위의 기하학적 원인 |
| hcp_4 | **3.2 Å** | ccp_1보다 짧아 2D 확산 가속 |

> 🔑🔑 **같은 랩 `kim2026`의 "Li–Li 네트워크 ≤ 3.5 Å 연결" 게이트와 같은 서술자 가족이다.**
> 두 논문 교차로 **랩 내부 문턱이 ~3.2–3.5 Å** 임이 확인된다(3.8 Å = 나쁨 / 2.2–3.2 Å = 좋음 / 게이트 3.5 Å).
> `kim2026` digest §10-2에 이미 "채택 검토"로 등록한 항목의 **두 번째 독립 데이터점**이다.

---

## 10. ★우선순위 ④-a — antisite (§3.5, Fig 5, Table 2, SI Note S3 + Fig S12)

### 10.1 문제 제기

hcp_1: 실험 **0.51 mS/cm** (Asano) vs 계산 **12.6**. 이 괴리는 P3̄m1 Li₃YCl₆에서 여러 연구가 공통으로 본 것[76,78,79].
논문의 가설: **원자 종이 자리를 맞바꾸는 antisite가 확산 채널을 바꾼다.**
특히 **Y³⁺가 Li 자리에 들어오면 정전 반발로 Li를 밀어내 1D 채널을 끊는다**(Fig 5b).

### 10.2 antisite 구성 방법 (SI Note S3) — 정확한 레시피

- 대상 Li 자리: **hcp_1 = 6h**, **LGPS = 8h**.
- 그 Li에서 **가장 가까운 양이온 2개**를 골라 각각 교환 → **계당 antisite 1개짜리 구조 2개**, 총 **4구조**(2계 × 2배열).
- **Fig S12 실물**: hcp_1 = Li(6h)↔**Y(1a)** 와 Li(6h)↔**Y(2d)** / LGPS = Li(8h)↔**P(2a)** 와 Li(8h)↔**Ge(2b)**.
- 형성에너지 (SI eq 5): **두 antisite 배열의 형성에너지 평균**, **"energy per atom" 기준**으로 계산.
  > (docx 수식이 평문화되며 분수선·부호가 소실 — 부호 규약은 판독 불가. 값이 양수인 것으로 보아 "결함이 드는 비용"의 절대값.)

### 10.3 결과 (Table 2, Fig 5c·5d)

| | E_anti (meV/atom) | 해석 |
|---|---:|---|
| **Li₃YCl₆ (hcp_1)** | **17.6** | antisite가 **쉽게 생긴다** |
| **LGPS** | **32.2** | antisite가 **잘 안 생긴다** → 그래서 계산 12–13 ≈ 실험 12 |

**Fig 5d — antisite를 실제로 넣고 AIMD (MSD 0–200 ps)**:

| 상태 | σ (mS/cm) | MSD 관찰 |
|---|---:|---|
| hcp_1 원본 (P3̄m1) | **12.6** | c가 압도적 |
| **antisite 1개** | **3.6** | **c 성분이 ~150 ps 부근에서 선형에서 꺾여 내려감**(빨간 점선 + 파란 하향 화살표로 표시) |
| **c 방향 완전 차단** | **0.6** | 실험 0.5와 근접 |

### 10.4 ⚠ 비판 — 이 논증의 4가지 구멍

1. **hcp_4에 대해 antisite를 계산하지 않았다.** 결론부는 이렇게 쓴다:
   > *"From this analysis, we **anticipate** that hcp_4, benefiting from 2D Li-ion diffusion and being relatively
   > unimpeded by antisites, should exhibit experimental ionic conductivities close to the calculated value of 38.5 mS/cm."*
   **anticipate = 계산하지 않았다는 뜻이다.** 논문 헤드라인("실측도 38 mS/cm 나올 것")이 **미계산 기대**에 걸려 있다.
   E_anti(hcp_4)도, antisite 넣은 hcp_4 AIMD도 없다.
2. **"c 완전 차단"은 물리 모델이 아니다.** 유한 antisite 농도의 결과가 아니라 **손으로 c 확산을 0으로 만든 극한**이다.
   그 극한에서 실험값이 재현되는 건 **검증이 아니라 정의**에 가깝다. 논문 자신의 표현도
   *"we **hypothesized that introducing antisites would intentionally reduce** the calculated ionic conductivity,
   **aligning it closer to the experimental results**"* — **목표값을 정해놓고 맞춘 절차**임을 자인한다.
3. **E_anti의 단위가 부적절하다.** 점결함 형성에너지를 **per atom**으로 정규화하면 **셀 크기에 의존**한다.
   두 계의 셀이 다르면(hcp_1 30원자(유도) vs LGPS 관례 50원자) 같은 결함이라도 per-atom 값이 달라진다.
   > 🔎 우리 검산(**셀 크기는 추정**): 결함당 절대값으로 환산하면 17.6×30 ≈ **0.53 eV** vs 32.2×50 ≈ **1.61 eV** → **3.0×**.
   > per-atom 비(1.83×)보다 **오히려 격차가 커진다** → **주장의 *방향*은 살아남는다.**
   > 그러나 **수치 자체는 셀 크기를 모르면 재현·이식 불가**다.
4. **비교 상대가 공정하지 않다.** LGPS의 antisite는 **Li↔P / Li↔Ge** — 즉 **공유결합 PS₄/GeS₄ 사면체를 깨는 일**이다.
   Li₃YCl₆의 Li↔Y는 **이온성 염화물 팔면체 안의 교환**이다. LGPS가 비싼 건 "1D 채널이 튼튼해서"가 아니라
   **골격 화학이 공유결합이라서**일 수 있다. "1D 채널을 가진 두 SE의 antisite 내성 비교"라는 프레임이 이 차이를 가린다.

### 10.5 ★ 문헌 충돌 — Schlem 2020과 정면으로 부딪친다

| | 이 논문 (Kim 2025) | `schlem2020_li3mcl6_cation_site_disorder.md` (Zeier) |
|---|---|---|
| 무질서의 정체 | **Li↔Y antisite** (Y가 Li 자리로) | **M2–M3 양이온 자리 교환**(양이온 부격자 *내부*) |
| M-on-Li antisite | **있다고 가정**(근거 = Asano 2018 인용) | **XRD Rietveld로 기각** — 다른 Wyckoff(1b,2c,3e,3f) 점유와 **Er-on-Li antisite 전부 시험 후 전자밀도 유의성 없음** |
| 무질서의 부호 | **유해**(채널 차단) | **유익**(σ 18×, Ea 0.49→0.41 eV) |
| 근거 | DFT E_anti + 문헌 인용 | 자체 실험(XRD + PDF 이중 정량, 시료 4종) |

**우리 판정**: Y(39 e⁻)가 Li(3 e⁻) 자리에 들어가면 **X선에 매우 잘 보인다** — Schlem이 명시적으로 그 모델을 시험하고 기각했다는 사실은
가볍지 않다. 반면 Kim 2025는 antisite의 **실험적 존재를 자기 데이터로 보이지 않고** Asano 2018을 인용할 뿐이다
(⚠ Asano의 "Y·Li 점유율이 합성조건에 따라 변한다"는 **Y의 1a/2d 분배·Li 부분점유**를 뜻할 수도 있어,
"Li 자리에 Y가 앉는다"와 **같은 진술이 아닐 수 있다** — Asano 원문 미확보라 확정 불가).
Kim 2025는 Schlem을 [34]·[53]으로 **인용은 하지만 이 충돌을 다루지 않는다.**

> 🔑 **이 충돌 자체가 우리에게 유용하다**: "halide는 무질서가 좋다/나쁘다"를 뭉뚱그리면 틀린다는
> Schlem digest §10-5의 경고가 **정확히 실현된 사례**다. 무질서를 말할 땐 항상 **어느 부격자의 어떤 교환인지**를 붙여야 한다.

---

## 11. ★우선순위 ④-b — 무질서/점유율 처리 (SI Note S1) 와 우리 개념과의 대응

### 11.1 실물 레시피 (SI Note S1 전문 요지)

> *"Theoretically, the atoms in a crystal structure should be **fully occupied**. Therefore, we designed **fully occupied**
> crystal structures based on their intrinsic occupancies. Initially, Li sites were generated using **"enumlib" code**
> [Hart & Forcade 2008/2009/2012, Morgan 2017], which generates the **derivative symmetry distinct superstructures** of a
> parent lattice. The derivative structures were subjected to **DFT relaxation**, with the eliminated Li sites determined by
> **structural stability based on the DFT results**."*

**절차 = 열거 → DFT 완화 → 최저에너지 배열 1개 채택.**

자리별 처리(원문):

| 골격 | 처리 |
|---|---|
| hcp_1 | **점유 최저 Y³⁺(occ 0.229) 제거** + **6h Li 자리의 절반 제거** → 3Y·9Li |
| hcp_2 | Yb³⁺ → Y³⁺; **8d Li 16자리 중 12개 선택** |
| hcp_3 | Er³⁺·Zr⁴⁺ → Y³⁺; **occ 0.770 자리는 만점유**, **occ 0.193 자리는 제거**, **8d(occ 0.3)는 절반 선택** → 12Li |
| ccp_1 | Liang/Sun 2020 JACS의 Li₃ScCl₆ 기반, Sc³⁺ → Y³⁺; 부분점유 2d 4개 + **4h Li 제거** → 6Li |

### 11.2 ★ 우리 개념(`kb/concepts/ordered_vs_disordered.md`)과의 대응 — **여기가 이 논문의 최대 수확**

| 축 | 이 논문 (할라이드) | 우리 (argyrodite) | 대응 판정 |
|---|---|---|---|
| **무질서의 부격자** | **양이온** (Li / Y) | **음이온** (S²⁻/Cl⁻ @ 4a·4d) + Li 공공 | **다름** — 전하캐리어 망에 직접 앉느냐(그들) vs 케이지 창을 변조하느냐(우리) |
| **무질서의 부호** | **유해**: antisite 1개로 12.6→3.6 | **유익**: F* 0.191→0.078 eV, Ea 0.253→0.224 | **정반대** |
| **왜 반대인가** | Y³⁺가 **Li 경로 위에** 앉아 정전 반발로 차단 | S/Cl 섞임이 **inter-cage 병목을 평탄화**(Li 경로엔 안 앉음) | **부격자 차이가 부호를 만든다** |
| **차원성** | **1D**(hcp_1)·1D(ccp_1) → blocker 1개로 절단 | **3D**(cage + inter-cage) → 국소 blocker는 우회됨 | **이게 진짜 결정 요인**(§11.3) |
| **처리 방법** | **enumlib 열거 → DFT → 최저 1개** | **enumerate → lowest-Ewald → DFT**(comp2 cfg 앙상블) | **계보 동일** — [Schlem]·[Liu2022]와 같은 노선, **SQS 아님** |
| **앙상블** | **없음** (배열 1개로 전 물성) | **있음** (d=0.5/1.0 × cfg0/1/2, 평균·산포로만 판정) | **우리 우위** — 단일 config 판정 금지 규율 |
| **anneal+relax 전처리** | **없음**(직접 DFT 완화) | **UMA anneal 700 K 20 ps + relax fmax 0.03** (라벨 스왑 v1 폐기 사례) | **우리 우위** — 그들은 라벨 배치 그대로 완화 |
| **무질서 = 공정변수** | 암묵 (실험 점유율을 "표준화" 대상으로만 취급) | 명시적 프레임 | [Schlem]이 이 자리를 채운다(이 논문 아님) |

### 11.3 🔑🔑 가장 값진 개념 전이 — **차원성 × 결함 내성 = 퍼콜레이션**

이 논문이 (의도했든 아니든) 보여준 것은 **퍼콜레이션 이론의 교과서적 사례**다.

- **1D 사슬의 site-percolation 임계는 p_c = 1** — 즉 **자리 하나만 막혀도 장거리 경로가 끊긴다.**
  hcp_1에서 antisite 1개가 σ를 12.6 → 3.6 → (완전차단) 0.6으로 떨어뜨리는 것이 바로 이것이다.
- **2D/3D는 p_c < 1** — blocker가 있어도 우회로가 남는다. hcp_4가 "antisite에 상대적으로 둔감할 것"이라는
  그들의 (미계산) 기대는 **이 논리로는 옳다.**

우리 자산과의 접속:
- `papers/ishikawa2025_site_percolation_cooperative_ion_conduction.md` — **site-percolation 임계·운반망** 이론 백본.
- `papers/dyre2004_hopping_models_ion_conduction_noncrystals.md` — **dc Ea = percolation 병목**.
- 우리 tier2 서술자 **`dopant_blocking_fraction`** — "도펀트가 Li 망에서 자리를 뺀다".
- 우리 **Nd σ-drop 0.52×(Ea 0.224≈0.227 불변)** = "장벽이 아니라 연결성/prefactor를 막는다".

> 🔑 **이 논문이 우리에게 주는 문장**: *"우리 argyrodite에서 도펀트 blocking이 **점진적**으로만 σ를 깎는 이유는
> Li 망이 **3D**이기 때문이다. 같은 blocking이 **1D 할라이드에서는 자릿수로 절단**된다."*
> — 이건 우리 `dopant_blocking_fraction`의 **작동 범위를 설명하는 물리**이고, 문헌 사례가 붙는다.
> ⚠ 단 **수치 이식은 0** (그들 12.6→3.6은 할라이드 1D의 값).

---

## 12. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1a–d** | 4개 기보고 골격의 c축 투영 + **Wyckoff 라벨** (hcp_1 P3̄m1 / hcp_2 Pnma / hcp_3 Pnma / ccp_1 C2/m) | 할라이드 구조 문법 카탈로그. [Cha] LYC 코팅·[Schlem] LYC 배경 |
| **2a** | **CSP 수렴도** — 세대(0–50) vs 에너지 산점, 초록 = stable, 우하단 회색 박스에서 후보 추출 → 확대 패널에 최종 후보 6종 | **CSP 결과 제시 양식**(세대별 산점 + 후보 갤러리). 우리 cascade 스코어 산점에 차용 가능 |
| **2b** | **hcp_4(C2) 신규 구조** 2방향 도해 (보라 Li / 파랑 Y / 초록 Cl) | Li-layered 배열 시각화 |
| **3a–d** | ★**구조 변환 지도** — hcp_1·hcp_3·ccp_1·hcp_4 각각 → hcp_2로 가는 **회전/틸트/shift/격자 mutation** 연산, 삼각형 색 = [YCl₆]³⁻ 배향 | **다형 계층을 "빌딩블록 배향 연산"으로 그리는 문법.** 우리 disorder cfg 간 관계 도해에 전용 가능 |
| **4a–e** | ★5골격 × [구조 / **Li 확률밀도 등가면**(600 K) / **방향분해 MSD**(0–200 ps, overall·a·b·c)] | **방향분해 MSD가 이 논문의 핵심 관측량.** 우리 MSD는 등방 총합만 — **축별 분해는 우리 공백**(채택 후보) |
| **5a** | antisite 개념도 (빨강·파랑 원 2종 교환) | — |
| **5b** | Li↔Y 교환과 **1D 확산 blocking** 모식 | 퍼콜레이션 서사 그림 |
| **5c** | **E_anti 비교** hcp_1 17.6 vs LGPS 32.2 meV/atom (구조 도해 병치) | ⚠ per-atom 단위 문제(§10.4-3) |
| **5d** | ★**antisite 3단계 MSD** — 원본 12.6 → 1 antisite 3.6 → c차단 0.6 mS/cm | **"결함 하나가 1D를 끊는다"의 시각 증거.** ⚠ 중간 패널의 c-MSD 비선형 꺾임 주목 |
| **S1** | 4골격 방향별 추가 도해 | — |
| **S2** | **hcp_4의 음이온 packing 부격자** — *"AB stacking implies hcp"* | **packing 판정 절차**(스택 순서로 hcp/ccp 확정) |
| **S3** | **RDF 원자쌍별 비교** — Cl–Cl은 동일, **Y–Y·Li–Li가 hcp_4에서 이탈** | ★**"구조가 정말 다른가"를 RDF 차분으로 판정** — 우리 cfg 앙상블 신규성 판정에 즉시 전용 |
| **S4** | **에너지 준위 정렬 + band gap** (CBM/VBM, 막대색 = 본문색) | ⛔ **수치 미보유** — gap = n/a. (캡션 "CBM: conduction band maximum" 오타) |
| **S5** | **Arrhenius plot** — 5골격, **600–1000 K → 300 K 외삽** | 우리 온도창과 동일. ⚠ 오차막대 없음 |
| **S6–S10** | 골격별 Li 확률밀도 축별 등가면 (600 K) — 순서대로 hcp_1/hcp_2/hcp_3/ccp_1/**hcp_4** | 확률밀도 = pymatgen-diffusion 산출 |
| **S11** | ★**Li 확산 채널** 5종 + 캡션이 정의를 확정: *"closer distances between Li-ion enable easy migration"* | ★**Li–Li 거리 서술자**(3.0/2.2/3.2/3.8 Å). `kim2026`의 ≤3.5 Å 게이트와 같은 가족 |
| **S12** | antisite 배열 실물 — hcp_1: Y(1a)↔Li(6h), Y(2d)↔Li(6h) / LGPS: P(2a)↔Li(8h), Ge(2b)↔Li(8h) | ⚠ **비교 상대가 공유결합 사면체**(§10.4-4) |
| **Table S1** | hcp_4 **원자좌표 전값** + 격자 | 재현 가능성의 유일한 통로. ⚠ 다중도 검산 불일치(§4) |

---

## 13. Post-processing ★

| 무엇 | 도구 | 어떻게 수치화/기록 |
|---|---|---|
| **CSP** | **CALYPSO** (PSO) + VASP | 50세대 × 100개체, **lowest enthalpy** 선택. Fig 2a에 세대별 에너지 산점 |
| **구조 열거(무질서 처리)** | **enumlib** (Hart–Forcade derivative structures) | 부분점유 → 대칭구별 초격자 열거 → DFT 완화 → 안정성으로 1개 선택 (SI Note S1) |
| **확산 통계** | **pymatgen-analysis-diffusion** [65 = Deng/Ong CM 2017] on **pymatgen** [68] | MSD → D → Arrhenius → **NE(Haven=1)** (SI eq 1–4) |
| **Li 확률밀도** | **pymatgen diffusion** (probability density) | 등가면(isosurface) 그림, 600 K (Fig 4, S6–S10) |
| **van Hove 상관함수** | **pymatgen diffusion** | §2에 "determined"라 명시되나 **본문·SI에 결과 그림이 없다** — 계산했으나 미게재로 보임(⚠ 확정 불가) |
| **RDF** | (미명시; pymatgen 계열 추정) | 원자쌍별 g(r) 비교로 신규성 판정 (Fig S3) |
| **E_hull** | (참조 hull 출처 **미기재**) | meV/atom (Table 1) |
| **밴드 정렬/gap** | VASP | Fig S4 그림만, **수치 없음** |
| **AIMD 실행길이** | 자체 기준 — **total effective ion hops + moving standard deviation** [67 = He/Zhu/Epstein/Mo 2018] | **자동 종료**. 실제 길이·통계 불확실도 **미보고** |
| **NEB / ICOHP / Bader / ELF / BVSE / 탄성 / phonon / ESW(grand-potential)** | — | **전부 없음** |

> 🔑 **T12 관련**: `kb/open_items.md` T12("van Hove 상관함수 도입")의 근거는 `lee2024` Fig 3e였는데,
> **이 논문도 van Hove를 계산했다고 §2에 적어 놓고 결과를 싣지 않았다.** 랩 표준 툴체인에
> van Hove가 상시 포함돼 있다는 방증(우리 T12 채택 근거 보강).

---

## 14. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`

> ⛔ **이 표는 "방법 대조표"다. 수치 대조표가 아니다.** 물질군(할라이드 vs 황화물)이 달라
> 어떤 값도 우리 물성 4축에 편입하지 않는다.

| 항목 | 이 논문 (Li₃YCl₆) | 우리 (comp1 / modelc) | 판정 |
|---|---|---|---|
| **물질군** | 할라이드 Li₃YCl₆, [YCl₆]³⁻ 팔면체 + hcp/ccp Cl 부격자 | 황화물 argyrodite Li₆PS₅Cl, PS₄³⁻ 사면체 + Li cage | **비교 불가** — 골격 화학·자리 기하 전부 다름 |
| **σ 파이프라인** | MSD → D → Arrhenius → **NE(Haven=1)** → 300 K | **동일** | **✓ 형식 완전 일치** |
| **온도창** | **600–1000 K, 5점** | **600/800/1000 K, 3점** | **✓ 같은 창** — 우리 창 선택의 외부 선례 |
| **힘 엔진** | **AIMD** (VASP/PBE/Γ/2 fs) | **MLIP-MD** (UMA-s-1p1 omat, Langevin NVT, dt 2 fs, friction 0.02) | **다름** — "둘 다 AIMD" 표현 금지(baseline 경고) |
| **실행길이** | **자동**(effective hops + moving SD, He/Mo 2018) | **고정**(equilib 5 ps / prod 200 ps, MSD 창 2–50 ps) | **그들 절차가 더 원리적** — 채택 검토 대상 |
| **시드/오차막대** | **1 / 없음** | modelc **3-seed**(Ea 0.197±0.032), config 산포 관리 | **우리 우위 (명확)** |
| **σ 절대값 취급** | 초록·결론에 **"38 mS/cm" 단언**, 구간 없음 | **인용 금지 규율** | **우리 우위.** 같은 랩 `kim2026`은 구간(0.01–2.4)을 캡션에 넣기라도 했다 |
| **무질서 처리** | **enumlib 열거 → DFT 최저 1개**, 앙상블 없음 | enumerate → lowest-Ewald → **anneal+relax → cfg 앙상블** | **계보 동일, 우리가 한 단계 위** |
| **무질서의 부호** | **유해**(Li–Y antisite가 1D 차단) | **유익**(음이온 무질서가 inter-cage 평탄화) | **부격자·차원성 차이** — §11.2 |
| **정적 완화** | 500 eV, 힘 < 0.04 eV/Å, 격자+좌표 완화, k "64 Å" 규약 | QE 계열, 완화격자 | ○ 동급 셋업 |
| **band gap** | **수치 없음**(Fig S4 그림만) | comp1 **2.066** / modelc **2.099** eV (fixed-occ nscf) | **비교 불가** — 값 자체가 없음. "둘 다 wide-gap" 정성만 |
| **산화 onset / ESW** | **없음** (grand-potential 미수행) | 2.256 V (S²⁻-limited, 축①) | 그들 축 아님 |
| **기계 물성** | **없음** | E_VRH 22.06 / 27.66 GPa, 전 C_ij | **우리 우위** |
| **NEB / BVSE / COHP / Bader** | **전부 없음** | 전부 보유 | **우리 우위** |
| **CSP** | **있음** (CALYPSO/PSO) | **없음** (host 고정 문제설정) | **문제설정이 다름** — 열위 아님(덱 분석 판정 유지) |
| **방향분해 MSD** | **있음** (a/b/c 분해가 핵심 관측량) | **없음** (등방 총합) | ⚠ **우리 공백** — 채택 후보 |
| **Li–Li 거리 서술자** | **있음** (2.2–3.8 Å) | BVSE 채널%·`migration_volume_fraction`·F* | ○ 상보 — 그들 것이 값싸고 우리 것이 물리적 |

---

## 15. ★우선순위 ⑤ — 이식 가능 / 이식 금지

### 15.1 ✅ 이식 가능 (방법·개념)

1. **부분점유 CIF → 완전점유 계산셀 표준화 레시피** (SI Note S1). **enumlib(Hart–Forcade) → DFT 완화 → 안정성으로 선택**,
   자리별 처리(최저 점유 자리 제거 / 최고 점유 만점유 / 중간 점유 절반 선택)까지 문서화돼 있다.
   우리가 문헌 CIF를 셀로 바꿀 때 쓰는 **문서화 템플릿**으로 그대로 쓸 수 있다. ⚠ 단 **앙상블은 우리가 추가해야 한다**.
2. **차원성 × 결함 내성 (퍼콜레이션)** — §11.3. 우리 `dopant_blocking_fraction`·`li_percolation` F*·[ishikawa2025]의
   **가장 선명한 문헌 사례**. "3D라서 우리 blocking이 점진적"이라는 설명을 문헌으로 받칠 수 있다.
3. **Li–Li 인접거리 서술자** (Fig S11: 2.2 / 3.0 / 3.2 / 3.8 Å, 가까울수록 좋음) — 같은 랩 `kim2026`의
   **≤3.5 Å 네트워크 게이트**와 같은 가족. 두 논문 교차로 **문턱 3.2–3.5 Å**가 확인된다.
   우리 BVSE·F*와 **독립인 값싼 2차 서술자**(kim2026 §10-2에 이미 등록, 이번이 **두 번째 데이터점**).
4. **방향분해 MSD (a/b/c)** — 우리 MSD 파이프라인은 등방 총합만 낸다. 축별 분해는 코드 몇 줄이고,
   **이방성 있는 셀(modelc rhombo-62, 슬랩, GB)에서 즉시 정보가 된다.** 채택 후보.
5. **RDF 차분으로 "정말 다른 구조인가" 판정** (Fig S3) — 원자쌍별 g(r)에서 **어느 쌍이 다른지**로 답한다.
   우리 disorder cfg0/1/2가 실질적으로 다른 배열인지 판정하는 데 전용 가능.
6. **자동 실행길이 결정** (effective hop 수 + moving SD, He/Mo 2018) — 우리 고정 200 ps보다 원리적.
   ⚠ 단 채택한다면 **He/Mo의 불확실도 추정까지 함께** 가져와야 한다(그들은 안 했다 — 그 점이 §8.3 비판).
7. **"조성 고정, 골격만 변주" 비교 설계 + Table 1 양식**(Energy/atom · E_hull · packing · σ 4행).
   우리 disorder/도핑 비교표에 쓰기 좋은 압축 양식.
8. **덱 ≠ 정본 규율의 두 번째 실증** (§5.2) — `litdb/talks/README.md` 규율 강화 근거.

### 15.2 ⛔ 이식 금지

1. **모든 σ 절대값** (38.5 / 18.8 / 12.6 / 10.2 / 3.4 mS/cm). 논문 스스로 hcp_1에서 **25–420× 과대**를 인정한다.
   오차막대 0·시드 1·셀 크기 미보고. **큰 비율의 정성 방향**(ccp 최하 ↔ hcp_4 최상)만 조건부 인용.
2. **E_hull 17–27 meV/atom** — 할라이드 hull, 참조 hull 출처 미기재. 우리 6원소 hull(Cl-Li-Nd-O-P-S) 밖(**Y 없음**).
3. **E_anti 17.6 / 32.2 meV/atom** — per-atom 정규화 = 셀 크기 의존, 셀 크기 미보고. **수치 이식 불가**.
4. **band gap** — 애초에 **수치가 없다**(Fig S4 그림만). 우리 canonical gap과 병치 금지.
5. **"hcp > ccp" 명제 자체** — 조성 1개·골격당 배열 1개·오차막대 0. 게다가 황화물 argyrodite는
   **packing 축으로 분류되는 물질이 아니다**(F4̄3m, cage 구조). 우리 문맥으로 옮기면 무의미.
6. **"antisite가 이론–실험 괴리의 주원인"** — 같은 랩 `lee2024`의 MTP 결과와 충돌, [Schlem] Rietveld와 충돌,
   hcp_4엔 미계산, "c 완전차단"은 목표값 맞추기. **미판정으로 보관.**
7. **Li–Y antisite ↔ argyrodite 음이온 무질서 등치** — 부격자(양이온 vs 음이온)·부호(유해 vs 유익)·
   차원성(1D vs 3D) 셋 다 반대. **개념 대응만, 수치·서사 전이 0.**
8. **"구조가 기하학적으로 가까우니 합성 가능"** (§6.3) — 장벽 미계산. 우리 준안정 논의에 인용하면 같은 구멍을 물려받는다.

---

## 16. 주의 / 한계 (over-claim 방지) — 비판적으로

1. **헤드라인이 미계산 기대에 걸려 있다.** "실측도 38 mS/cm 근처일 것"의 근거는 *"we anticipate"* 뿐 —
   hcp_4의 E_anti도, antisite를 넣은 hcp_4 AIMD도 **없다**(§10.4-1). 초록의 *"impressive ionic conductivity (38 mS/cm)"*·
   *"breakthrough"* 는 **오차막대 없는 단일 AIMD 외삽값**이다.
2. **σ에 오차막대가 하나도 없다.** He/Mo 프레임(불확실도가 본론)을 실행길이 결정에만 쓰고 불확실도는 버렸다.
   **38.5 vs 18.8 = 2.05×** 가 잡음 밖이라는 증거 없음(§8.3).
3. **AIMD 셀 크기·시뮬레이션 길이 미보고.** SI Note S1의 관계셀을 그대로 썼다면 hcp_1은 **Li 9개**로 MSD를 낸 것 —
   확정 불가지만, 보고가 없다는 것 자체가 재현성 결함.
4. **E_hull 스팬(10 meV/atom)이 PBE 다형 랭킹 정확도·kT 아래**라 안정성 서열 주장이 성립하지 않는다.
   게다가 **실제로 합성되는 hcp_1이 최저가 아닌** 역설을 논의하지 않는다(§7).
5. **"metastable = 공간군 번호가 낮아서"** 는 비논리다(§5.3).
6. **표준화가 새 교란을 만든다.** hcp_2/hcp_3/ccp_1을 Li₃YCl₆로 바꾼 순간 **합성된 물질이 아니다.**
   그런데 §3.4 말미에서 *"these findings are consistent with the experimental data on aliovalent substitution [33,38]"*
   라며 **Y-표준화한 hcp_3의 계산값을 Er/Zr 실측 경향에 맞춰 읽는다** — 논리적으로 미끄러진 문장.
7. **Table S1 다중도 검산이 안 맞는다**(§4) — 유일한 재현 통로인 좌표표에 표기 오류로 보이는 불일치.
8. **문헌 충돌 미처리** — [Schlem 2020]을 인용하면서 그 논문이 **M-on-Li antisite를 실험적으로 기각**한 사실을 다루지 않는다(§10.5).
9. **결함 비교 상대가 공정하지 않다** — LGPS의 Li↔P/Ge는 **공유결합 사면체 파괴**다(§10.4-4).
10. **1 antisite MSD의 c 성분이 비선형**(Fig 5d 중간 패널, 빨간 점선 + 하향 화살표)인데 선형 fit으로 D를 뽑은 것으로 보인다
    — sub-diffusive 구간을 포함하면 D가 계통적으로 왜곡된다. (그림 판독 기반 지적 — 확정 불가)
11. **PBE + vdW 보정 없음.** 할라이드는 이온성이라 치명적이진 않지만, 같은 랩 `lee2024`가 **optB88(vdW)** MTP로
    실험을 맞췄다는 사실이 **functional 선택이 이 계에서 결정적일 수 있음**을 시사한다.
12. **자체 실험 0.** 신규 구조 hcp_4는 **합성되지 않았다.**

---

## 17. 인용 가능 문장 (deck/paper용)

- "Kim et al. (Rare Met. 2025) fixed the composition at Li₃YCl₆ and varied only the anion framework, finding that
  the widely held ccp > hcp ordering does not survive a composition-controlled comparison — the ccp framework was
  the **lowest**-conducting of the five, and Li-ion pathway **dimensionality** (1D vs 2D), not the packing label,
  tracked the computed conductivity." *(⛔ 절대값 없이)*
- "In a **1D** Li channel a single Li–Y antisite is sufficient to collapse long-range transport, whereas 2D/3D networks
  retain bypass routes — a textbook consequence of the site-percolation threshold being p_c = 1 in one dimension
  [Kim 2025 + ishikawa2025]." — **우리 `dopant_blocking_fraction` 작동범위 설명용**
- "Antisite-type cation disorder in halides and anion-site disorder in argyrodites are **not the same phenomenon**:
  the former places a trivalent cation directly in the carrier path (detrimental), the latter modulates cage windows
  without occupying Li sites (beneficial)." — **무질서 뭉뚱그리기 방지**
- ⚠ **사용 금지**: "Li₃YCl₆의 새 구조는 38 mS/cm에 도달한다" — **오차막대 없는 AIMD 외삽 + 미합성 + 같은 논문이 인정하는
  25–420× 과대 이력**. 우리 문서 어디에도 이 수치를 쓰지 않는다.

---

## 18. 용어 미니사전

- **ccp / hcp**: 음이온 조밀쌓임 방식. ccp = **ABCABC**(입방), hcp = **ABAB**(육방). 같은 조성이라도 이 스택이 다르면 다른 다형.
- **CALYPSO / PSO**: 결정구조예측(CSP) 코드. **입자군집최적화** — 후보 구조 집단이 서로의 최적점을 참조하며 이동.
  GA(USPEX 계열)와 다른 계열의 전역 탐색.
- **enumlib (Hart–Forcade)**: 모(parent) 격자의 부분점유를 **대칭적으로 구별되는 초격자(derivative structure)** 로 전수 열거.
  우리 cfg-enumeration과 같은 도구 계열.
- **E_hull (energy above hull)**: convex hull 위 형성에너지 초과분. 0 = 열역학적 안정. 통상 <30–50 meV/atom을 "합성 가능(준안정)"의 느슨한 기준으로 씀.
- **antisite**: 서로 다른 원자종이 자리를 맞바꾼 점결함. 여기선 **Li ↔ Y**. `M-on-Li`처럼 어느 종이 어디로 갔는지 명시해야 한다.
- **Nernst–Einstein (Haven = 1)**: σ = ρz²F²D/(RT). 이온 간 상관을 무시하는 근사 — 협동 운동이 있으면 **σ를 과소평가**한다
  (우리 [Adeli] Haven 0.23–0.3 참조). 이 논문·우리 둘 다 Haven 보정 없음.
- **effective ion hops / moving standard deviation**: AIMD가 D를 신뢰할 만큼 돌았는지 판정하는 통계 기준
  (He/Zhu/Epstein/Mo 2018). **유효 점프 수**가 충분하고 MSD 기울기의 이동표준편차가 안정되면 종료.
- **van Hove 상관함수 G(r,t)**: "시각 0에 r=0에 있던 입자가 시각 t에 거리 r에 있을 확률" — self/distinct 부분으로
  갇힘 vs 자유확산·knock-on을 구별. (이 논문은 계산했다고만 하고 결과 미게재)
- **probability density isosurface**: AIMD 궤적에서 Li의 시간평균 존재확률을 3D 격자에 쌓아 등가면으로 그린 것.
  "Li가 실제로 어디를 지나는가"의 그림. 우리 BVSE 등가면과 시각적으로 유사하나 **BVSE는 정적 퍼텐셜, 이건 동역학 통계**.
- **displacive vs reconstructive 전이**: 결합을 끊지 않고 원자가 조금 움직이는 전이(변위형) vs 결합·쌓임을 재편하는 전이(재구성형).
  hcp↔ccp는 후자에 가깝다.

---

## 19. 미해결 질문 (후속 확보 시 채울 것)

| # | 질문 | 어디서 |
|---|---|---|
| Q1 | **AIMD 셀 크기와 실제 시뮬레이션 길이**는 얼마인가 (Li 개수 = MSD 통계의 핵심) | 저자 문의 / 후속 논문 |
| Q2 | hcp_4의 **E_anti와 antisite-AIMD** — 헤드라인 주장의 유일한 결정적 검증 | 미수행 |
| Q3 | Fig S4의 **band gap 실수치** 5개 | SI 그림 원본 |
| Q4 | Table S1 **Li3 자리(2b vs 4c)** 및 조성 검산 불일치 | 저자 CIF |
| Q5 | 같은 랩 `lee2024`가 Li₃YCl₆를 **MTP_optB88로 0.56**(≈실험)을 냈다면, 이 논문의 antisite 설명과 **어느 쪽이 랩의 현재 입장**인가 | `lee2024` 실물 + 후속 |
| Q6 | Asano 2018의 "Y·Li disordering"이 **정말 Li 자리에 Y가 앉는 것**인지, Y의 1a/2d 분배·Li 부분점유를 말하는 것인지 | Asano Adv Mater 2018 원문 |
| Q7 | van Hove 결과는 왜 실리지 않았나 (T12 참고 자료가 될 수 있음) | 저자 / 후속 |

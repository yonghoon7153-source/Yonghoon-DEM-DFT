<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/nolan2021_garnet_cathode_coating.md
     2026-09-12 신규 작성:
       ① 1저자 지정: "양극 코팅 계산 계보 8편" 세트의 **#7 (리뷰)**. #4 nolan2019 · #5 nolan2021 의 **방법 교과서**.
       ② ★★ 계보 카드가 #4·#5 끝에 남긴 물음 — *"anodic/cathodic limit 의 정의가 활자로 적혀 있는가"* —
          에 **이 편이 답한다. 문장이 있다.** 저널 **p. 2022**, Equation 4 바로 다음 문장:
          *"The cathodic and anodic limits of a material are the potentials at which the reduction
          and the oxidation reactions become thermodynamically favorable, respectively."*
          ⚠ 단 **"E_D^open 이 0 을 벗어나는 φ"** 라는 *연산적* 표현은 아니다 — 그건 여전히 어디에도 없다 (§4c·§4e).
       ③ 크로핑 그림 11장 중 **9장을 실제로 봤다**: `Fig. 2`·`4`·`5`·`6`·`7`·`8`·`9`·`10`·`11`.
          ⛔ 안 본 것: `Fig. 1`(ASB 모식도) · `Fig. 3`(LGPS 확산경로 — 우리 축과 무관).
          `Fig. 9B`·`9D`, `Fig. 11B`, `Fig. 6B`, `Fig. 8A` 는 **2–2.4× 확대 재판독**해서 막대 끝·마커를 수치화했다.
       ④ 🔧 **도구 결함 1건 수정**: `extract_figures.py` 의 자동 bbox 가 `Fig. 10` 의 **오른쪽 1/3(Type 3 SEI 패널)을
          잘라냈다**. 3단 폭 그림을 1단으로 잡은 것. 원문 p. 2037 을 직접 렌더해 `fig_10.png` 를 교체하고
          `figures.json` 의 bbox·note 를 갱신했다. (도구 자체는 안 고쳤다 — 다른 논문 영향 미지수)
       ⑤ ⚠ **이 편은 리뷰다. 자체 계산 0 · 자체 실험 0 · SI 0.** 모든 수치가 2차 인용이다.
          그래서 이 digest 의 자산은 수치가 아니라 **"어떤 정의를 어떤 문장으로 고정했나"** + **원출처 귀속표**(§12).
       ⑥ 본문↔그림 어긋남 **6건** 발견(§10). 그중 2건은 우리가 이 리뷰를 인용할 때 실제로 걸린다. -->

# Computation-Accelerated Design of Materials and Interfaces for All-Solid-State Lithium-Ion Batteries — Nolan, Zhu, He, Bai, Mo (*Joule* **2** (2018) 2016–2046) [Review]

> slug `nolan2018_computation_accelerated_design_review` · DOI `10.1016/j.joule.2018.08.017` · type `리뷰 (자체 DFT 0 · 자체 실험 0 · SI 0; AIMD + 데이터베이스 열역학 방법론 교과서 + 2차 인용 수치)` · PDF `litdb/inbox/111. Nolan2018_Computation_Accelerated_Design_Materials_Interfaces_ASSB_REVIEW.pdf` (31 pp = 본문 26 pp + 참고문헌 5 pp) · **SI 없음** · digested `2026-09-12` · status ✅ · 태그 **[외부·리뷰]**

> elements: Li, P, S, Cl, O, N, F, Ge, Si, Sn, Ti, Zr, La, Al, Nb, Ta, Co, Ni, Mn, Zn, Y
> methods: DFT, AIMD, NEB, ESW, XPS

> **저자**: **Adelaide M. Nolan**¹, **Yizhou Zhu**¹, **Xingfeng He**¹, **Qiang Bai**¹, **Yifei Mo\***^1,2 (¹ University of Maryland, College Park — MSE · ² Maryland Energy Innovation Institute; 단일기관 5인) · 교신 `yfmo@umd.edu` · 게재 2018-10-17 · 지원 **DOE-EERE DE-EE0006860 + DE-EE0007807** · 계산자원 UMD + **MARCC** · 참고문헌 **156편** · 그림 **11장**(표 0장) · **SI 없음**
>
> **⚠ 서지 확인 결과 — 파일명과 다르다.** inbox 파일명이 `Nolan2018_…_ASSB_REVIEW` 라 연도만 맞고, 실제 서지는
> ***Joule* 2, 2016–2046 (2018년 10월 17일), DOI 10.1016/j.joule.2018.08.017** 이다. 저자 순서는 계보 카드의
> 잠정 기재 **"Nolan/Zhu/He/Bai/Mo"** 와 **정확히 일치**한다(PDF 메타데이터 author 필드 = "Adelaide M. Nolan").
> 즉 계보 카드의 잠정 기재를 그대로 확정하면 된다.
> **인용 시 저널 페이지 = PDF 페이지 + 2015** (PDF p.1 = 저널 p.2016). 이 digest 의 모든 `p. 20xx` 는 **저널 페이지**다.
>
> **계보 (1저자 지정 "양극 코팅 계산 계보" 8편 세트의 #7)**: [Aykol 2014](aykol2014_cathode_coating_thermodynamics.md)(#1) → [Aykol 2016](aykol2016_ht_cathode_coating_design.md)(#2) → [Xiao 2019](xiao2019_cathode_coating_screening.md)(#3) → [Nolan 2019](nolan2019_chemistries_stable_high_energy_cathodes.md)(#4) → [Nolan 2021](nolan2021_garnet_cathode_coating.md)(#5) → [Honrao 2021](honrao2021_interpretable_ml_sse_anode_coatings.md)(#6) → **본 편(#7, 리뷰)** → Banerjee 2020(#8, 리뷰).
> **연대 주의**: 이 편은 **2018년** 이고 #4(2019)·#5(2021)보다 **먼저** 나왔다. 따라서 "#4·#5 의 방법 교과서" 라는 계보 카드의
> 규정은 *시간순 선행* 이라는 뜻으로 맞고, *후속 요약* 이라는 뜻으로는 틀리다 — **이 편은 #4·#5 를 인용하지 않는다**(있을 수 없다).
> 이 편이 인용하는 것은 그 **공통 조상**: [Zhu15](zhu2015_esw_grand_potential_origin.md)(ref 63) · [Zhu16] JMCA(ref 70) ·
> [Rich16](richards2016_interface_stability_pseudobinary.md)(ref 71) · [Ong08] Chem Mater(ref 56).

---

## 0. 이 digest 를 읽는 법 — 범위부터

### 0a. 1저자가 이 편에 물은 네 가지 — 답 먼저

| # | 물음 | 답 (근거 절) |
|---|---|---|
| **1** | **anodic/cathodic limit 의 정의가 활자로 적혀 있는가** | 🟢 **있다. 문장으로 있다.** 저널 **p. 2022**, `Fig. 2` 설명 직후 **Equation 4 바로 다음 문장**: *"The cathodic and anodic limits of a material are the potentials at which the reduction and the oxidation reactions become thermodynamically favorable, respectively (Section 4)."* 같은 문단이 창까지 정의한다: *"The electrochemical window is the gap between the reduction and oxidation potentials based on the Gibbs free energy difference of the reactants and products."* ⚠ **단 연산적 표현은 아니다** — *"E_D^open(φ) ≠ 0 이 되는 최초의 φ"* 라는 형태는 **이 편에도 없다**. 이 편은 "반응이 열역학적으로 유리해지는 전위" 라는 **물리적** 정의를 준다 (§4c) |
| **2** | `E_d` / `E_D^open` / ESW / hull 위 거리 — 네 양의 정의와 관계 | 🟡 **관계는 한 문단으로 정리돼 있지만, 식은 4개 중 1개만 인쇄돼 있다.** 이 리뷰에 번호 붙은 식은 **딱 4개**이고 (1) MSD·(2) Nernst–Einstein·(3) Arrhenius·(4) `μ_Li(φ)=μ⁰_Li−eφ` 뿐이다. **`E_hull` 은 문장으로**(p. 2020), **pseudo-binary `ΔH_D` 는 `Fig. 2C` 캡션 한 줄로만**(p. 2021) 정의된다. 네 양의 재구성은 §4e — **결론: hull 거리 ⊂ 닫힌계 반응에너지 ⊂ 개방계, ESW 는 개방계를 φ 축으로 훑은 것** |
| **3** | 우리 값(−0.3227 eV/atom · 2.256 V · 1.242 / 1.717 V)이 **같은 양인가** | 🟢 **−0.3227 eV/atom 은 같은 양이다** — 이 편의 `ΔH_D`(= `Fig. 2C`·`Fig. 9B` 의 세로축, eV/atom, 혼합분율 최소화)와 **정의·단위·부호 규약이 모두 같다**. 직접 비교 가능한 소환값: **LPS\|LCO = −0.41 eV/atom**, 산물 `Li₃PO₄ + Li₂SO₄ + Li₂S + Co₉S₈`. 🟡 **2.256 V 는 같은 축의 양이지만 우리가 더 좁은 정의를 쓴다**(phase-set 고정·LiS₄ 제외). 🔴 **1.717 V 는 다른 양이다 — 이 편에 대응 개념이 없다**(§7b). ⚠ **함정 하나**: 이 편의 `Fig. 6A` 가 LGPS 에 대해 **1.72 V** 를 인쇄하는데 그건 **LGPS 의 환원한계**이고 우리 **1.717 V 는 Li₆PS₅Cl 의 중성 자기분해 OCV** 다. **숫자가 우연히 같다 — 절대 나란히 놓지 말 것** |
| **4** | ⛔ **황화물·염화물 SE 가 이 리뷰의 대상에 포함되는가** | 🟢 **황화물은 완전히 포함된다 — 오히려 주인공이다.** LGPS 가 전편의 중심이고, **argyrodite `Li₆PS₅Cl` 가 본문에 3회 명시**되며(p. 2031 창 · p. 2036 계면산물 · p. 2040 Li 금속 type 3), `Fig. 7A`·`Fig. 8`·`Fig. 9`·`Fig. 11B` 전부 황화물을 싣는다. 이것은 **#4(Ed 데이터셋 황화물 0)·#5(무대가 가넷)와 결정적으로 다른 점**이다. 🔴 **염화물 SE 는 포함되지 않는다** — `Li₃InCl₆`·`Li₃YCl₆` 류 할라이드 SE 는 **본문에 0회**다(2018년엔 아직 무대에 없었다). `Fig. 8` 의 "halides" 는 **X = N, O, S, F** 이므로 사실상 **불화물**이고, Cl 은 `Li₆PS₅Cl`·`LiCl`·`Li₃OCl` 안의 원소로만 등장한다 (§7c) |

### 0b. 본 그림 / 안 본 그림 (크로핑 11장 중 **9장 실독**)

- ✅ **본 것 (9장)**: `Fig. 2`(hull·GPPD·pseudo-binary 3연작 — 이 편의 **정의 그림**) · `Fig. 4`(단일 vs 협동 이동 NEB + bcc) · `Fig. 5`(설계 워크플로 + E_hull 히트맵 + Arrhenius + σ/Ea 표) · `Fig. 6`(LGPS ESW + CV + XPS + 임피던스, **6B 확대 재판독**) · `Fig. 7`(ESW 막대 — 우리 축 B 직결) · `Fig. 8`(Li-M-X 삼원 cathodic/anodic limit 산점도, **8A 왼쪽 2.4× 확대**) · `Fig. 9`(계면 — **9B·9D 2× 확대 재판독**, 우리 `interface_reactivity` 직결) · `Fig. 10`(계면 3유형, **bbox 수정 후 재판독**) · `Fig. 11`(코팅 창 vs LCO 전위, **11B 1.9× 확대**)
- ⛔ **안 본 것 (2장)**: `Fig. 1`(ASB 모식도 — 정보 0) · `Fig. 3`(LGPS Li 확산경로 AIMD/중성자 대조 — 우리 4축 어디에도 안 걸린다. 본문 서술로 충분)
- 📄 **표 그림 없음**: 이 리뷰에는 번호 붙은 표가 **하나도 없다**. 표처럼 보이는 것은 `Fig. 5D`(σ·Ea 3행)와 `Fig. 7A` 좌우의 상평형 상자뿐이고, 둘 다 그림 안이라 이미지로 읽었다.

### 0c. 가져올 수 있는 것 / 없는 것

| 🟢 가져올 수 있는 것 | 🔴 가져오면 안 되는 것 |
|---|---|
| **p. 2022 의 limit 정의 문장** — 우리 `oxidation_limit_V`·`reduction_limit_V` 가 *무엇인지* 를 문헌 문장으로 고정 | **이 리뷰의 수치를 1차 출처처럼** — 전부 2차 인용이다. LGPS 1.72/2.42 는 [Han16](ref 64), Li₆PS₅Cl 1.7/2.4 는 [Zhu15]·[Rich16], `Fig. 8` 은 [Zhu17] 것이다 (§12) |
| **`ΔH_D` 소환값 −0.41(LPS\|LCO) / −0.56(LPS\|Li₀.₅CoO₂) / −1.27(5 V)** — 우리 −0.3227 과 **같은 양**이라 차이의 원인(계·hull 세대)을 논할 수 있다 | **`Fig. 9B` 의 x축(mole fraction)과 우리 `x_atomic_frac` 을 같은 축으로** — 정규화가 다르다. 최솟값만 비교 가능 |
| **"창 ≠ HOMO–LUMO gap, HOMO–LUMO 는 상한"** (p. 2022, ref 65–67) — 우리 gap 2.066/2.099 eV 를 ESW 와 섞지 말라는 **문헌 근거** | **`Fig. 7`·`Fig. 11B` 막대 끝 수치를 우리 db 에** — 2015–2016 MP hull 세대다. 우리 2026 hull 과 0.1–0.3 V 어긋나는 것이 이미 확인돼 있다([Zhu15] digest §17) |
| **type 1/2/3 계면 분류** (p. 2037, `Fig. 10`) — 우리 `sei_products` 전자구조 판정이 "왜" 중요한지의 프레임 | **"코팅 창 2–4 V 이므로 양극에 안정" (p. 2039) 을 그대로** — **자기 `Fig. 11B` 가 반증한다**. 5종 중 4종의 anodic limit 이 LiCoO₂ 선(3.90 V) **아래**다 (§10-2) |
| **AIMD 규율 3문장**: ① RT σ 외삽 오차 **최대 2 자릿수** ② 창 한계 ③ **Haven 비를 고려해야 한다** (p. 2020) — 우리 MLIP-MD 규율(절대 σ 인용 금지 · Haven=1)의 **문헌 정당화** | **AIMD 수치를 우리 MLIP-MD 와 같은 표에** — `Fig. 5D` 의 10/23/6 mS cm⁻¹ 은 AIMD(VASP 힘)이고 우리는 UMA 힘이다. CLAUDE.md 규율 |
| **"에너지 장벽만으로 고전도를 주장하는 것은 부적절하다"** (p. 2019) — 우리 BVSE/NEB 단독 서술을 막는 인용문 | **`Fig. 8` 에서 La³⁺·Nd³⁺ 를 읽어 오는 것** — **두 칸 모두 데이터가 없다**(마커 0개). Nd 도핑 논거로 쓸 수 없다 (§7d) |

---

## 1. 한 줄 요약

**"고체전해질은 0–5 V 에서 안정하다" 는 통념은 측정 아티팩트이고, 실제 열역학적 창은 황화물 기준 1.7–2.4 V 로 훨씬 좁다 — 그럼에도 전지가 도는 이유는 전해질이 안정해서가 아니라 *분해산물이 만드는 계면층(interphase)* 이 전자를 막아 주기 때문이다.** 이 리뷰는 그 결론에 이르는 **두 도구**(AIMD · 데이터베이스 기반 열역학)의 정의·규약·한계를 한곳에 모으고, 계면을 **type 1(본질 안정) / type 2(MIEC — 계속 분해) / type 3(SEI — 부동태화)** 로 분류해 *"코팅의 역할은 공간전하층 억제가 아니라 계면 분해 억제"* 라는 재해석을 못박는다.

---

## 2. 메타

| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| A.M. Nolan, Y. Zhu, X. He, Q. Bai, **Y. Mo\*** (UMD) | *Joule* **2**, 2016–2046 (2018) | `10.1016/j.joule.2018.08.017` | SE = `Li₁₀GeP₂S₁₂`·`Li₃PS₄`·`Li₇P₃S₁₁`·**`Li₆PS₅Cl`**·`Li₇La₃Zr₂O₁₂`·`LLTO`·`LATP`·`LiPON`·`Li₃OCl` · 양극 = `LiCoO₂`·`Li₀.₅CoO₂`·`LiNi₀.₅Mn₁.₅O₄`·`LiFePO₄` · 코팅 = `Li₂SiO₃`·`LiTaO₃`·`Li₃PO₄`·`Li₄Ti₅O₁₂`·`LiNbO₃` · Li binary = `LiF`·`Li₂O`·`Li₂S`·`Li₃N` | **리뷰** — 자체 DFT 0회, 자체 실험 0회, SI 0. 전량 2차 인용 |

**이 편이 (2018년 시점에) 정리한 것**
1. **AIMD 의 정의와 한계를 규약으로 만들었다** — MSD·Nernst–Einstein·Arrhenius 세 식 + 통계 오차·Haven 비·carrier 형성에너지 경고.
2. **데이터베이스 열역학 3층 구조를 한 절에 세웠다** — 상안정(2.2.1) → 외부조건 하 안정(2.2.2, GPPD) → **계면 평형(2.2.3)**.
3. **"0–5 V 창" 신화의 사인(死因)을 규명했다** — semi-blocking CV 의 접촉면적·kinetics 제약. 처방까지 준다(SE+C 복합전극).
4. **계면 3유형 분류(`Fig. 10`)** — 이 리뷰가 가장 널리 인용되는 부분이고, 원출처는 ref 63·70·120 이다.
5. **음극측 처방으로 "질화물 화학"을 내세웠다** — 질화물은 cathodic limit 이 가장 낮고(≈ 0 V 이하) 다수가 Li 금속에 본질 안정([Zhu17], ref 101). *"계면에 질소를 국소적으로 농축해 type 2 → type 3 로 바꾼다"*.

---

## 3. 핵심 물성 (수치) — ⚠ **전부 소환값(2차 인용)**

> ⚠ 이 리뷰는 값을 **생산하지 않는다**. 아래는 전부 다른 논문에서 가져온 것이고, 원출처는 §12 에 귀속해 두었다.
> ⛔ **우리 `db/properties/` 에 넣지 않는다.** 대조·문맥용이다.

### 3a. 전기화학 창 (ESW) — 우리 축 B 직결

| 물질 | 환원(cathodic) | 산화(anodic) | 출처(ref) | 비고 |
|---|---|---|---|---|
| **LGPS** | **1.72 V** | **2.42 V** | `Fig. 6A`, ref 64 [Han16] | 그림에 소수 둘째자리까지 인쇄 (**figure-read** 로 확인). 본문은 "1.7 / 약 2.4" |
| `Li₃PS₄` | 1.7 V | 2.4 V | 본문 p. 2031, ref 63·71 | `Fig. 11B` 막대 **figure-read ≈ 1.71 → 2.41 V** |
| **`Li₆PS₅Cl`** (argyrodite) | **1.7 V** | **2.4 V** | 본문 p. 2031, ref 63·71 | ⚠ **그림에는 없다** — 본문 문장으로만. `Fig. 7`·`Fig. 11B` 막대에 argyrodite 는 그려져 있지 않다 |
| `Li₇PS₁₁` | 1.7 V | 2.4 V | 본문 p. 2031 | ⚠ **오타** — `Li₇P₃S₁₁` 이어야 한다 (§10-5) |
| `LLZO` | ≈ 0 V (**figure-read ≈ 0.05**) | **figure-read ≈ 2.91 V** | `Fig. 7A`·`Fig. 11B` | 본문: *"oxide SE 중 LLZO 가 Li 에 대해 가장 낮은 환원전위, 0 V 에 가깝다"* |
| `LLTO` | figure-read ≈ 1.8 V | figure-read ≈ 3.7 V | `Fig. 7A` | 본문: Ti⁴⁺ 환원 **1.8 V** |
| `LATP` | figure-read ≈ 2.2 V | figure-read ≈ 4.2 V | `Fig. 7A` | 본문: Ti⁴⁺ 환원 **2.2 V** |
| `LiPON` | figure-read ≈ 0.68 V | figure-read ≈ 2.63 V | `Fig. 7A` | 0 V 상평형 `Li₂O + Li₃N + Li₃P` |
| **산화물 SE 전반** | — | **2.9 – 4.3 V** | 본문 p. 2031, ref 63·71 | *"O²⁻ 산화 = O₂ 방출"* |
| `Li₂S` | 0 V | figure-read ≈ **2.1 V** | `Fig. 7A` | ★ 우리 axis ① (S-limited onset) 의 문헌 앵커 |
| `Li₂O` | 0 V | figure-read ≈ 2.9 V | `Fig. 7A` | |
| `LiF` | 0 V | figure-read ≈ 4.9 V (**"To 6.36 V"** 로 축 절단 표기) | `Fig. 7A` | 5 V 상평형 = `LiF`, F₂ 는 6.36 V |
| `Li₃N` | 0 V | figure-read ≈ 0.6 V | `Fig. 7A` | 4종 중 최저 |

**★ 음이온 서열 (이 편의 핵심 정성 결론)**: **anodic limit — F ≫ O > S > N** / **cathodic limit — N 이 가장 낮다**. 그래서 *"고 anodic limit 화학과 저 cathodic limit 화학은 서로 모순되고, 단일 SE 로 0–5 V 창을 만드는 것은 어렵다"* (p. 2032). **Li 함량이 올라가면 anodic limit 이 내려간다**(같은 양이온·음이온 기준).

### 3b. 코팅 재료의 창 (`Fig. 11B`, **figure-read**) — ★ 우리 코팅 논의 직결

| 코팅 | 환원 | 산화 | LiCoO₂ 전위(≈ **3.90 V**) 대비 |
|---|---|---|---|
| `Li₄Ti₅O₁₂` | ≈ 1.72 | ≈ **3.61** | ✖ **0.29 V 부족** |
| `LiNbO₃` | ≈ 1.72 | ≈ **3.86** | ✖ **0.04 V 부족**(선 바로 아래) |
| `Li₂SiO₃` | ≈ 0.77 | ≈ **3.70** | ✖ 0.20 V 부족 |
| `LiTaO₃` | ≈ 1.16 | ≈ **3.83** (dashed ≈ 3.93) | ✖ 0.07 V 부족 |
| **`Li₃PO₄`** | ≈ 0.68 | ≈ **4.21** (dashed ≈ 5.0) | ✅ **유일하게 넘는다 (+0.31 V)** |

🔑 본문은 이것을 *"창이 2–4 V 이므로 코팅은 양극에 안정하다"* 라고 요약하는데 **그림은 그 말을 지지하지 않는다**(§10-2).
정직한 요약은 **"코팅은 황화물 SE(2.42 V) 대비 anodic 여유를 +1.2 ~ +1.8 V 벌어 주지만, LCO 전위에서는 `Li₃PO₄` 외에는
여전히 (근소하게) 열역학적 한계를 넘어서 있다"** 다. — 이 문장은 우리 코팅 서사에 **그대로 쓸 수 있다.**
(⚠ `Fig. 11B` 의 `Li₃PO₄` **0.68 → 4.21 V** 는 [Nolan21] SI XLSX 의 `0.69 / 4.20` 및 [Zhu15] 인쇄값과 **셋이 일치**한다
— 이 축의 수치 체계가 세 문헌에서 동일함을 다시 확인해 준다.)

### 3c. 계면 반응 열역학 `ΔH_D` (eV/atom) — ★★ 우리 `interface_reactivity` 와 **같은 양**

`Fig. 9B`(**figure-read**, 2× 확대 판독) — x축 = **mole fraction of SE in SE–LCO**, y축 = `ΔH_D` (eV/atom):

| SE \| LiCoO₂ | 최솟값 `ΔH_D` | 최솟값 위치 x | 최저점 상평형 (그림 상자) |
|---|---|---|---|
| **LPS (`Li₃PS₄`)** | **−0.41** (본문 명시값) | ≈ 0.41 – 0.48 | **`Li₃PO₄`, `Li₂SO₄`, `Li₂S`, `Co₉S₈`** |
| `LiPON` | figure-read ≈ **−0.098** | ≈ 0.78 – 0.82 | `Li₃PO₄`, `Li₂O`, `CoN` |
| `LATP` | figure-read ≈ **−0.053** | ≈ 0.30 – 0.35 | `Li₃PO₄`, `LiCo₂O₄`, `TiO₂`, `LiAl₅O₈`, `Co₃O₄` |
| **`LLZO`** | figure-read ≈ **−0.005 (사실상 0)** | ≈ 0.96 | `La₂O₃`, `Li₆Zr₂O₇`, `Li₅CoO₄` |

**서열: LPS (−0.41) ≪ LiPON (−0.10) < LATP (−0.05) < LLZO (≈ 0).** 황화물이 다른 셋보다 **4–80배** 더 반응성이다.

전압/SOC 의존 (본문 p. 2035):

| 조합 | `ΔH_D` (eV/atom) |
|---|---|
| `Li₃PS₄` + **`LiCoO₂`** | **−0.41** |
| `Li₃PS₄` + **`Li₀.₅CoO₂`**(탈리튬) | **−0.56** |
| `Li₃PS₄` **@ 5 V** (개방계) | **−1.27** |

🔑 **탈리튬(−0.41 → −0.56, 1.37×)보다 전압 인가(−0.41 → −1.27, 3.1×)가 훨씬 세다.** 우리 `interface_reactivity` 는 ⚠ **2026-11-10 정정** — 이 '3.1 배' 는 잣대가 다른 두 수를 나눈 값이다 (−0.41 = mutual · 원자당 / −1.27 = total · 비-Li 원자당). 같은 잣대로는 mutual 1.3 배 · total 2.2 배다 (원전 `zhu2016_first_principles_interface_stability_assb` §20-2 — 정규화 판독은 그 digest 의 근거 수준).
현재 **닫힌계(OCV)** 만 돌린다 — 개방계 확장의 정량적 동기가 여기 있다 (§8-①).

### 3d. μ_S / μ_O 안정범위 (`Fig. 9D`, **figure-read**, 2× 확대) — ★ "왜 황화물\|산화물이 원리적으로 안 맞는가"

| 물질 | μ_S 범위 (eV) | 물질 | μ_O 범위 (eV) |
|---|---|---|---|
| `LiCoO₂` | **≲ −2.68** (아래로 열림) | `LiCoO₂` | **−2.68 … −0.42** |
| `Li₀.₅CoO₂` | **≲ −7.35** | `Li₀.₅CoO₂` | **−0.72 … 0** |
| `Li₂S` | −4.65 … 0 | `LLZO` | −6.1 … **−0.42** |
| `Li₃PS₄` | **−1.20 … 0** | `LLTO` · `LATP` | −3.85 … 0 |
| `LGPS` | **−1.25 … 0** | `LPS` · `LGPS` · `Li₂S` | ≲ −3.05 (−6.2 축 끝까지) |
| | | `LiPON` | −4.8 … −4.12 |

🔑 **황화물 SE 의 μ_S 창(−1.2…0)과 `LiCoO₂` 의 μ_S 창(≲ −2.68)은 겹치지 않는다** → 같은 μ_S 를 가질 수 없으므로 평형 자체가 불가능.
μ_O 도 마찬가지(`LPS` ≲ −3.05 vs `LiCoO₂` −2.68…−0.42). 본문 p. 2036 이 그대로 서술한다.
🔑 **내부 정합성 검산(본 digest)**: `LLZO`(μ_O 상한 −0.42)와 `LiCoO₂`(μ_O 상한 −0.42)가 **같은 값에서 맞닿는다** →
`Fig. 9B` 에서 LLZO–LCO 의 `ΔH_D ≈ 0` 인 것과 정확히 일치한다. 반대로 `LiPON`(−4.8…−4.12)은 `LiCoO₂` 와 전혀 안 겹쳐
`ΔH_D = −0.098` 로 반응한다. **두 패널이 서로를 검증한다.**

### 3e. 이온전도 (AIMD 소환값, `Fig. 5`)

| M in `Li₁₀MP₂S₁₂` | σ@300 K AIMD | σ@300 K 실험 | Ea AIMD | Ea 실험 |
|---|---|---|---|---|
| **Ge (LGPS)** | 10 mS cm⁻¹ | 12 (ref 1) | 0.23 eV | **0.25** (ref 1) |
| **Si** | **23** | 25 (ref 2, `LiSiPSCl` 조성) | **0.20** | 0.23 |
| **Sn** | 6 | 7 (ref 82) | 0.24 | 0.27 |

`E_hull` (`Fig. 5B`, meV/atom): **S 계 — Si 17 · Ge 15(LGPS) · Sn 13** / **O 계 — Si 92 · Ge 70 · Sn 97.**
→ *"알려진·예측 성공한 SIC 는 전부 `E_hull < 20 meV/atom`"* (p. 2028).

기타: **bcc 음이온 격자의 Li 이동 장벽 ≈ 0.2 eV**(본문 p. 2024; `Fig. 4D` 곡선은 **figure-read ≈ 0.15 eV**) ·
**LATP 단일이온 0.48 eV → 협동이동 0.28 eV**(`Fig. 4B`, figure-read) ·
`Li₁.₂₅Ta₀.₇₅Zr₀.₂₅SiO₅` **σ ~10⁻³ S cm⁻¹ · Ea 0.23 ± 0.01 eV**(ref 34).

---

## 4. DFT/계산 방법 ★ — **이 리뷰의 본체. 정의가 자산이다**

> ⚠ **이 편은 계산 파라미터를 하나도 적지 않는다.** cutoff·k-mesh·pseudopotential·supercell·DFT+U·SQS —
> **전부 0회**다. 리뷰라서가 아니라 *"방법론을 개념 수준에서 정리하는 글"* 로 설계됐기 때문이다.
> 파라미터가 필요하면 원출처(§12)로 가야 한다.

### 4a. 번호 붙은 식은 **딱 4개**다

| 식 | 내용 | 페이지 | 우리 대응 |
|---|---|---|---|
| **(1)** | `D = (1/2dΔt)(1/N) Σᵢ ⟨\|rᵢ(t+Δt) − rᵢ(t)\|²⟩`, d = 3 | p. 2018 | `tools/ionic/` MSD·D (창 2–50 ps 고정) |
| **(2)** | `σ = (N q² / V k T) D` — Nernst–Einstein | p. 2019 | 우리 σ (Haven = 1) |
| **(3)** | `D = D₀ exp(−Ea / kT)` — Arrhenius | p. 2019 | 우리 600/800/1000 K 3점 |
| **(4)** | **`μ_Li(φ) = μ⁰_Li − eφ`** (기준 = **Li 금속**) | **p. 2022** | ★ 우리 `esw_grand_potential.py` 의 `V = μ_Li(metal) − μ_Li`, `mu_Li_ref_eV = −1.9089` |

★ **식 (2) 에 대한 저자의 주석이 우리 규율과 정확히 같다** (p. 2019):
*"…the number of mobile ions N is canceled out by the 1/N in the expression for D (Equation 1), so that σ can be directly obtained from the total MSD of all ions with no explicit definition of mobile carriers."*
→ **"mobile carrier 를 따로 정의하지 않아도 된다"** 는 것이 이 규약의 장점이자 한계다. 저자 스스로 p. 2020 에서
**Haven 비를 고려해야 한다**고 단서를 단다.

⛔ **`E_d`·`E_D^open`·`ΔH_D`·`E_hull` 에는 번호 붙은 식이 없다.** 전부 산문·캡션이다. 이것이 이 편의 한계다.

### 4b. `E_hull` — 문장 정의 (p. 2020, §2.2.1)

> *"The energy above hull of a compound, `E_hull`, is obtained by comparing the compound's energy with the energy convex hull, and corresponds to **the absolute value of the decomposition energy of the compound at its thermodynamic phase equilibria** (Figure 2A). A compound with `E_hull` = 0 lies on the energy convex hull and is a thermodynamically stable phase at 0 K."*

- `E_hull > 0` = 준안정. **`> 100 meV/atom` 이면 합성이 어려울 수 있다**(ref 57 Sun 2016).
- ★ **경고 문장**: *"many compounds with a high `E_hull` may nevertheless exhibit highly negative formation energies from their elementary state reactants. Thus, **this formation energy of a compound is not suitable for describing the compound's phase stability**."* → 형성에너지와 hull 거리를 혼동하지 말라.
- **0 K 한계 자인**: 엔트로피 `S`·`PV` 무시. LGPS·LLZO 는 **고온 합성에서 엔트로피 안정화**된다(ref 38·58) → cluster expansion + MC(ref 16·36) 또는 phonon(ref 59·60)이 필요하지만 **보통 비용 때문에 안 한다**.
- ⚠ 우리 관련: **"무질서 이동 부격자의 배치 엔트로피가 다른 고체상보다 훨씬 클 수 있다"** 는 문장이 있다 — 우리 SQS/무질서 처리 논의의 문헌 근거다. (단 이 편은 SQS·enumerate 같은 **무질서 처리 기법을 하나도 언급하지 않는다**.)

### 4c. ★★ GPPD 와 **anodic/cathodic limit 의 정의 문장** (p. 2022, §2.2.2)

**계보 카드가 #4·#5 에 걸어 둔 물음의 답이 여기 있다.** 원문 순서 그대로:

1. *"The grand potential phase diagram (GPPD) was developed to evaluate the stability of materials as a function of external conditions, such as applied potential or O₂ partial pressure.⁵⁶'⁶² **A GPPD describes a system that is open to one or more external components.**"* (p. 2021)
2. *"In LiBs,⁶²⁻⁶⁴ the equilibrium under an applied potential φ referenced to Li metal μ⁰_Li can be described by an equilibrium at Li chemical potential* **`μ_Li(φ) = μ⁰_Li − eφ`** *(Equation 4)."* (p. 2022)
3. *"Therefore, the GPPD evaluated with respect to μ_Li describes the electrochemical lithiation and delithiation of materials under applied potential φ (Figure 2B)."*
4. ★★ ***"The cathodic and anodic limits of a material are the potentials at which the reduction and the oxidation reactions become thermodynamically favorable, respectively (Section 4)."*** ← **찾던 문장**
5. *"**The electrochemical window is the gap between the reduction and oxidation potentials based on the Gibbs free energy difference of the reactants and products**, and is different from the band gap or the gap between the levels of highest occupied molecular orbital (HOMO) and lowest unoccupied molecular orbital (LUMO).⁶⁵ The proper alignment of HOMO and LUMO levels is only a necessary condition of the electrochemical stability. Computational studies have shown that that the gap between HOMO and LUMO is **an upper bound** of the electrochemical window.⁶⁶'⁶⁷"* (원문에 `that that` 오타)

**이 정의가 #5(Nolan 2021)보다 나은 점 / 못한 점**

| | [Nolan21] (#5) | **본 편 (#7)** |
|---|---|---|
| `μ_Li(φ) = μ⁰_Li − eφ` | ✅ Methods 식 (5) | ✅ **Equation 4** (3년 먼저) |
| `E_D^open` 의 **식** | ✅ 식 (6) 인쇄 | ❌ **없다** |
| limit 이 **무엇인지** 한 문장 | ❌ 없다 | ✅ **있다 (p. 2022)** |
| limit 의 **연산적** 판정 규칙 | ❌ | ❌ **여전히 없다** |
| φ 를 **연속으로** 훑는가 | ❌ 3 V·5 V 두 점 | ✅ **`Fig. 6A`·`Fig. 7` 이 연속 staircase** |

⇒ **결론: 두 편을 합쳐야 정의가 완성된다.** #7 이 *"limit 이 무엇인지"*(물리적 정의)를 주고, #5 가 *"어떤 식으로 재는지"*(`E_D^open`)를 준다. **`limit ≡ E_D^open(φ) 이 0 을 벗어나는 φ`** 라는 **연산 규칙은 이 계보 8편 어디에도 활자로 없다** — 우리가 쓰는 pymatgen `get_element_profile` 의 구현(상평형이 바뀌는 μ_Li 경계)은 **[Zhu15] 의 staircase 그림과 이 두 문장으로부터 재구성한 것**이지, 인용 가능한 한 문장이 있는 게 아니다. ★ **그래서 우리 원고에서는 우리 정의를 우리가 명시해야 한다 — 문헌에 떠넘길 수 없다.**

### 4d. 계면 열역학 (p. 2022, §2.2.3) — **식 없음, 문장만**

> *"The thermodynamic equilibrium of two mixing materials can be determined from **the phase diagram comprising all the elements in these two materials** using the materials database. **If the phase equilibria contain phases other than the two original materials, these two materials are not in equilibrium with each other, and may react exothermically to form other phases** (Figure 2C)… This calculation therefore identifies the chemical stability of two materials at their interface. **Similarly, GPPDs can also be used to evaluate the equilibrium between two materials in contact under an applied potential, which is the electrochemical stability of the interface.**"*

- 원출처 명시: *"These calculations of interface equilibria were proposed and described in previous studies.**⁶⁹⁻⁷¹**"* = **[Miara15] Chem Mater 27, 4040 · [Zhu16] JMCA 4, 3253 · [Rich16] Chem Mater 28, 266**.
- **혼합분율 최소화(우리 `x_atomic_frac` 스캔)는 여기 산문에 없다** — `Fig. 2C` 캡션과 `Fig. 9B` 의 x축이 그것을 **그림으로만** 말한다. 정의의 원본은 [Rich16] eq 2 다.
- **정당화 문장** (우리도 쓸 수 있다): *"these phase diagrams are high dimensional in composition (e.g., quaternary or beyond) and involve a large number of compounds, which often do not have experimentally measured energies. These thermodynamic calculations **could not be performed before the advent of computational materials databases**."*

### 4e. ★★ 네 양의 정의와 관계 — **한 절로 재구성** (1저자 물음 #2)

이 리뷰가 네 양을 한자리에 모으긴 하지만 **관계를 명시적으로 쓰진 않는다.** 아래는 본 digest 의 재구성이고,
각 줄의 근거 문장을 이 편에서 뽑아 붙였다.

```
                조성공간 어디서 재나          계는 닫혀 있나          단위        우리 파일
① E_hull        한 점(그 화합물)             닫힘                  eV/atom     (cascade 게이트)
② ΔH_D (=E_d)   두 점을 잇는 선 위 x 스캔     닫힘                  eV/atom     interface_reactivity_results.json
③ E_D^open      두 점 + Li 저수지            Li 에 열림 (μ_Li 고정)  eV/atom     (미구현 — §8-①)
④ ESW 한계      한 점 + Li 저수지            Li 에 열림 (μ_Li 스캔)  V           oxidation_stability*.json
```

**포함 관계 — 세 개의 부등식**

1. **`ΔH_D ≤ 0` 이고, 두 끝점이 각각 hull 위에 있으면 `ΔH_D` 는 *순수한 혼합* 구동력이다.**
   이 편의 표현: *"If the phase equilibria contain phases other than the two original materials, these two materials are not in equilibrium"* — 즉 `ΔH_D = 0` ⇔ **type 1 계면**. `Fig. 9B` 의 LLZO 곡선이 그 실례다(전 구간 ≈ 0).
   ⚠ 끝점이 준안정이면(`E_hull > 0`) 그만큼이 `ΔH_D` 에 섞여 들어온다 — **#4/#5 가 "끝점 준안정성 제거" 를 넣은 이유**이고, 이 편에는 그 처리가 **적혀 있지 않다.**
2. **`|E_D^open| ≥ |ΔH_D|`** — Li 저수지를 열면 반응 경로가 늘어나므로 구동력은 커지기만 한다.
   이 편의 수치 실례: `Li₃PS₄|LiCoO₂` **닫힌계 −0.41 → 5 V 개방계 −1.27 eV/atom** (p. 2035). **3.1배.** ⚠ **2026-11-10 정정** — 이 '3.1 배' 는 잣대가 다른 두 수를 나눈 값이다 (−0.41 = mutual · 원자당 / −1.27 = total · 비-Li 원자당). 같은 잣대로는 mutual 1.3 배 · total 2.2 배다 (원전 `zhu2016_first_principles_interface_stability_assb` §20-2 — 정규화 판독은 그 digest 의 근거 수준).
   본문 설명: *"The reactions for delithiated cathodes at high voltage are more favorable because **lower Li chemical potential drives the delithiation and oxidation of SEs**."*
3. **ESW 한계 = ③ 을 한 물질(상대 없음)에 대해 φ 축으로 훑었을 때 상평형이 자기 자신을 벗어나는 경계.**
   `Fig. 6A` 가 이 관계를 **그림으로** 보여 주는 유일한 자리다 — 왼쪽 staircase(전압–용량)와 오른쪽 상평형 띠가 짝을 이루고,
   **1.72–2.42 V 구간에서만 오른쪽 띠가 `LGPS` 자신**이며 그 구간에 *"Stability Window"* 라는 라벨이 붙어 있다.
   ⇒ **`Fig. 6A` 가 사실상 "limit 의 연산적 정의" 를 그림으로 제공한다.** 문장이 아니라 그림이라는 게 이 계보의 특징이다.

**네 양 사이에서 우리가 자주 틀리는 지점 3개** (우리 쪽 사고 사고 방지용)

- ❌ `E_hull` 과 `ΔH_D` 의 **부호 규약이 반대다**: `E_hull ≥ 0`(클수록 불안정), `ΔH_D ≤ 0`(음수일수록 불안정). 한 표에 넣을 때 반드시 명시.
- ❌ **ESW 창 폭(V)과 반응에너지(eV/atom)는 서로 변환되지 않는다.** 창이 좁다고 `ΔH_D` 가 크다는 보장이 없다 — `LiPON` 이 반례다(창 0.68–2.63 V 로 좁은데 `ΔH_D` 는 −0.098 로 작다).
- ❌ **HOMO–LUMO gap ≠ ESW.** 이 편이 명시적으로 *"upper bound"* 라고 쓴다 → 우리 gap 2.066/2.099 eV 를 ESW 폭 0.898/1.014 V 와 나란히 두면 **1.2 eV 가 설명 안 되는 게 아니라 원래 그런 것**이다.

### 4f. AIMD 규약과 자인한 한계 (p. 2018–2020) — ★ 우리 MLIP-MD 규율의 문헌 짝

| 항목 | 이 편의 서술 | 우리 규율 (CLAUDE.md) | 판정 |
|---|---|---|---|
| 온도 | *"often performed at high temperatures, **typically 600 K or higher**"* | 600/800/1000 K (400/500 K 제외 판정) | ✅ 동일 |
| 시간 | *"tens of picoseconds to a few nanoseconds"* · 셀 *"a few hundred atoms"* | prod 200 ps (MLIP 라 더 길다) | 🟢 우리가 유리 |
| RT σ 외삽 오차 | ★ *"the error bound of extrapolated RT ionic conductivity **can be as large as two orders of magnitude**"* (ref 39 He 2018) | **σ 절대값 인용 금지** | ✅ **우리 규율의 정확한 근거** |
| 오차 악화 요인 | *"if **fewer data points** are used to fit the Arrhenius plot, **fewer ion migration events** are sampled, and if the **fitting procedures are improperly performed**"* | 3점 Arrhenius · 자유절편 D | ⚠ **3점은 "fewer data points" 에 해당한다** — 이 문장은 우리에게 불리한 쪽으로도 읽힌다. `Fig. 5C` 의 AIMD 는 **8점(1000/T = 0.8–2.0, 즉 500–1250 K)** 이다 |
| Haven 비 | *"the quantification of ionic conductivity should consider the correlation factor, such as the Haven ratio"* | Haven = 1 로 고정 | ⚠ **우리가 단순화한 쪽** — 원고에 단서 필요 |
| carrier 형성에너지 | *"may or may not fully capture the formation energy of mobile carriers… significant for pristine, non-doped materials with highly ordered Li sublattices"* | argyrodite 는 무질서라 덜 걸림 | 🟢 우리 계에 유리 |
| 고온 기전 ≠ RT 기전 | *"The diffusion mechanisms at the high temperatures… may not be identical to those at RT"* (LLZO 자리점유 온도의존, ref 46–48) | 600 K 기준 상대비교만 | ✅ |
| NEB 의 한계 | *"NEB calculations only provide the migration energy barrier for specific migration pathways and **do not provide ionic conductivity or the pre-exponential factor**"* + *"**knowledge of the energy barriers alone is inadequate to support claims about high ionic conductivity**"* (p. 2019) | 우리 BVSE/NEB 단독 주장 금지 | ✅ **그대로 인용 가능** |
| 실험 대비 | *"computational results are based on bulk single crystals"* vs 실험은 불순물·입계·미세조직 | 우리도 벌크 단결정 | ✅ |

---

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | ASB 모식도 (Li 수송이 SE 내부·계면 양쪽에서 중요) | ⛔ 정보 0. **안 봤다** |
| 2a–c | **정의 3연작**: (A) convex hull + `E_hull` + `γ → AₓB + A_yB` (B) GPPD — `x_Li` 축 + 오른쪽에 μ_Li↑/φ↓ 이중축과 상평형 띠(Li / Li_yA / Li_xA / A) (C) **pseudo-binary `ΔH_D` vs `Li₃PS₄` 분율**, 별표 = **−0.41 eV/atom**, 산물 `Li₂SO₄·Li₂S·Li₃PO₄·Co₉S₈` | ★★ **우리 `interface_reactivity` 설명용 1순위 그림**. (B) 의 **μ_Li↑ / φ↓ 반대방향 이중축**이 식 (4) 의 시각화 — 우리 ESW 그림 양식으로 그대로 차용 가능 |
| 3a–f | LGPS Li 확산경로 — AIMD 궤적(c 채널·ab 면) vs 중성자 MEM 핵밀도(⟨001⟩·⟨110⟩) + 협동이동 NEB 프로파일 | ⛔ **안 봤다** (우리 4축 비해당). 필요해지면 `figures.json` 으로 재소환 |
| 4a–d | (A) 단일 vs 협동 이동 모식 (B) **LATP NEB — 단일 `figure-read ≈ 0.48 eV` vs 협동 `≈ 0.28 eV`** (C) LGPS S 부격자 ↔ bcc 대조 (D) bcc T–T 경로 **figure-read ≈ 0.15 eV** | 협동이동 = 우리 `jeon2026`·`ishikawa2025` 축의 2018년 정본. (B) 의 **협동 경로가 시작·끝 에너지가 다르다**(끝 ≈ 0.04 eV)는 점이 중요 — 우리 NEB 해석 시 "왕복 대칭이 아닐 수 있다" |
| 5a–d | 설계 워크플로: (A) 원소치환 (B) **`E_hull` 히트맵 — S계 13/15/17 vs O계 70/92/97 meV/atom** (C) **Arrhenius 8점(500–1250 K) + 오차막대** (D) σ·Ea 3×4 표 | (B) = "`E_hull < 20 meV/atom` 이 합성가능성 게이트" 의 원그림. **(C) 의 8점·오차막대가 우리 3점 Arrhenius 의 대조 기준** (§4f) |
| 6a–d | (A) **LGPS 전압–용량 staircase + 상평형 띠, `Stability Window` 1.72↔2.42 V 라벨** (B) Li/LGPS/LGPS+C CV 2장 (C) Ge 3d·P 2p·S 2p XPS 전후 (D) Li–LGPS–Li 임피던스 0→24 h | ★★ (A) = **"limit 의 연산적 정의" 를 그림으로 보여 주는 유일한 자리** (§4e-3). (B)(C)(D) = *"계산 창이 좁다"* 의 실험 3중 검증 — 우리 ESW 주장 방어용 |
| 7a,b | (A) Li binary 4종 + SE 7종 창 막대 + **0 V/5 V 상평형 상자 좌우 배치** (B) Li 삼원 산화물 18종, Li-Ti/Nb/Si/Ta/P-O 색분류, **위 μ_Li(0→−5 eV) / 아래 φ(0→5 V) 이중축** | ★ 우리 `Fig.` 양식의 원형. **`Li₂S` 상한 figure-read ≈ 2.1 V = axis ① S-limited 의 문헌 앵커**. `LiF` 가 4.9 V 에서 축이 끊기고 "To 6.36 V" 로 표기된 것도 작도 참고 |
| 8a,b | Li-M-X 삼원(X = N,O,S,F) 양이온 M 40칸 산점도 — (A) cathodic limit −1…4.6 V (B) anodic limit 0…8 V. 마커 = 불화물 5각/황화물 ○/산화물 △/질화물 ◇ | ★ **음이온 서열의 정량 그림**: anodic — 불화물 ≈ **6–7.2 V** ≫ 산화물 **2.8–5.0** > 황화물 **1.9–2.7** > 질화물 **0.3–1.5 V**. **황화물 밴드 1.9–2.7 V 안에 우리 2.14/2.256 V 가 들어간다** = 외부 정합 1건. ⛔ **La³⁺·Nd³⁺·Eu³⁺·Cu²⁺·Yb³⁺ 칸은 두 패널 모두 마커 0개** — Nd 논거로 쓸 수 없다 |
| 9a–d | (A) LiPON O1s/N1s/P2p XPS (B) **`ΔH_D` vs mole fraction, SE 4종(LLZO/LATP/LiPON/LPS) + 최저점 상평형 상자** (C) LCO\|Li₂S–P₂S₅ HAADF-STEM + Co/S/P EDX 선프로파일(계면층 ≈ 40–50 nm) (D) **μ_S·μ_O 안정범위 막대** | ★★ (B) = 우리 `interface_reactivity` 의 **직접 대조군**(§3c). (D) = *"음이온 화학이 다르면 평형 자체가 불가"* 의 정량 근거(§3d). (C) 는 계면층 두께의 실측 스케일(~10 nm 급) |
| 10 | **계면 3유형**: type 1 Ideal(Li\|Li-binary, e⁻ 차단 ✗, 분해 없음) / type 2 MIEC(Li\|Li–Ge 합금\|LGPS, Li⁺·e⁻ 둘 다 통과 → 계속 두꺼워짐) / type 3 SEI(Li\|`Li₃P,Li₂O,Li₃N`\|LiPON, e⁻ 차단·Li⁺ 통과) | ★ 우리 `sei_products` 전자구조 판정의 **프레임**. 🔧 **자동 크롭이 type 3 패널을 잘라냈던 것을 수정했다**(digest 머리 ④) |
| 11a–c | (A) 성공 셀 2종 모식(Li\|LiPON\|LCO · C\|Li-P-S\|coated LCO) (B) **코팅 5종 + SE 3종 창 vs `LiCoO₂` 전위선 3.90 V** (C) 코팅 두께 0–20 nm 별 임피던스(ref 7 Takada) | ★★ (B) = **§3b 표의 원그림. 본문 주장과 어긋나는 자리**(§10-2). (C) = 코팅 **1–2 nm 에서 저항이 이미 10배 이상 떨어진다**(0 nm ~1000 Ω → 2 nm ~60 Ω, figure-read) — "얇아도 된다" 의 실측 |

---

## 6. Post-processing ★

이 편은 **후처리를 직접 수행하지 않는다**(리뷰). 대신 **어떤 후처리가 표준인지**를 목록화한다.

| 도구/기법 | 이 편에서의 위치 | 우리 대응 |
|---|---|---|
| **AIMD → MSD → Einstein 적합** | 식 (1), 절차는 **ref 39 (He et al. 2018)** 에 위임 | `tools/ionic/` · MSD 창 2–50 ps |
| **Nernst–Einstein → σ** | 식 (2) | 동일 (Haven = 1) |
| **Arrhenius 적합** | 식 (3) · `Fig. 5C` | 600/800/1000 K 3점 |
| **NEB / CI-NEB** | §2.1 서두 (ref 22 Henkelman) · `Fig. 4B,D` | `tools/…/neb` |
| **kinetic Monte Carlo** (NEB 결과 → 비희박 농도의 총 확산) | ref 29–32 | ⛔ 우리는 안 쓴다 — **비어 있는 도구** |
| **convex hull / `E_hull`** | §2.2.1 · `Fig. 2A`·`Fig. 5B` | cascade 게이트 |
| **GPPD (grand potential phase diagram)** | §2.2.2 · `Fig. 2B` | `esw_grand_potential.py`(pymatgen `get_element_profile`) |
| **pseudo-binary 계면 평형** | §2.2.3 · `Fig. 2C`·`Fig. 9B` | `interface_reactivity*.py`(pymatgen `InterfacialReactivity`) |
| **cluster expansion + Monte Carlo**(배치 엔트로피) | ref 16·36 — *"보통 비용 때문에 안 한다"* | ⛔ 미구현 |
| **phonon (진동 엔트로피)** | ref 59·60 | 🟡 b2o3 에만 있다 |
| **XPS (in situ / ex situ)** | `Fig. 6C`·`Fig. 9A` — 계산 예측의 **1차 검증 수단** | 우리 `whitten2023` 축 |
| **임피던스 시분해** | `Fig. 6D`·`Fig. 11C` — type 2 성장의 관측량 | 우리 `kim2025_impedance_decoupling_tlm_assb` |
| **CV (semi-blocking vs 복합전극)** | `Fig. 6B` — ⚠ **semi-blocking 은 창을 과대평가한다**는 것이 이 편의 결론 | 실험 협업 시 반드시 SE+C 복합전극 |
| **pymatgen** | ⚠ **이름이 본문에 없다** — [Rich16]·[Zhu15] 원출처에서만 | 우리 전 공정 |
| **MLIP** | ⚠ **없다.** p. 2041 이 *"current interatomic potentials may not be adequate"* 라고 쓴다(2018년) | 🟢 우리 UMA 는 이 문장 **이후의 기술** — 우리가 앞서 있는 유일한 축 |

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md`

### 7a. 양(quantity) 대조표

| 우리 값 | 이 편의 대응 개념 | 같은 양인가 | 근거 |
|---|---|---|---|
| **`interface_reactivity` −0.3227 eV/atom** (comp1\|LiCoO₂) | **`ΔH_D`** (`Fig. 2C`·`Fig. 9B`) | 🟢 **같은 양** — 단위(eV/atom)·부호(음수=반응)·혼합분율 최소화·MP hull 전부 동일 | 소환 대조: **LPS\|LCO −0.41** |
| **modelc −0.3308 / nd −0.3285** | 동 | 🟢 같은 양 | |
| **`oxidation_limit_V` 2.14 / 2.256 V** | **anodic limit** (p. 2022 정의 · p. 2031 값) | 🟡 **같은 축, 더 좁은 정의** — 우리는 phase-set 을 해시로 고정하고 `LiS₄`·`SCl₃`·`Li₅PS₄Cl₂` 를 제외한다. 이 편은 제외 개념 자체가 없다 | 소환 대조: **Li₆PS₅Cl 2.4 V** |
| **`reduction_limit_V` 1.242 V** | **cathodic limit** | 🟡 같은 축. 우리 1.242 는 `Li₆PS₅Cl + 5 Li → 5 Li₂S + LiCl + P`(P⁰) | 소환 대조: **1.7 V** ([Zhu15] 1.71 과 같은 계열) — **0.47 V 차이**는 hull 세대 + 상 roster |
| **`ocv_self_decomposition_V` 1.717 V** | ❌ **대응 개념 없음** | 🔴 **다른 양** — 이 편에 "Li 유출입이 0 인 중성 자기분해 전위" 라는 개념이 **없다** | ⚠ 함정 §7b |
| **`window_V` 0.898 V** (2.14−1.242) | *"electrochemical window is the gap between the reduction and oxidation potentials"* (p. 2022) | 🟢 정의 동일 | LGPS 창 **0.70 V**(2.42−1.72) |
| **gap 2.066 / 2.099 eV** | ❌ **ESW 와 다른 양이라고 이 편이 명시** | 🔴 절대 섞지 말 것 | *"HOMO–LUMO gap 은 ESW 의 **상한**"* |
| **`E_VRH` 22.06 / 27.66 GPa** | ❌ 이 편에 탄성 **0건** | 🔴 | p. 2041 에 *"the SE may need particular mechanical properties"* 라는 전망 한 줄뿐 |
| **Ea 0.253 / 0.224 eV (MLIP-MD)** | AIMD Ea (`Fig. 5D`) | 🔴 **힘 계산 축이 다르다** (UMA vs VASP) | CLAUDE.md 규율 |

### 7b. ★ **1.717 V 함정** — 이 digest 에서 가장 중요한 경고

- 이 편의 `Fig. 6A` 는 **LGPS 의 환원한계로 `1.72 V`** 를 인쇄한다(소수 둘째자리까지).
- 우리 `ocv_self_decomposition_V` 는 **`1.717 V`** 다.
- **두 수는 소수 셋째자리까지 같지만 완전히 다른 양이다:**

| | 이 편 `1.72 V` | 우리 `1.717 V` |
|---|---|---|
| 물질 | `Li₁₀GeP₂S₁₂` | `Li₆PS₅Cl` / `Li₅.₄PS₄.₄Cl₁.₆` |
| 무엇 | **cathodic limit** — 첫 리튬화 plateau (P⁵⁺ 환원 개시) | **중성 자기분해** — Li 유출입 = 0 인 전위 (`Li₆PS₅Cl → Li₃PS₄ + Li₂S + LiCl`) |
| 우리 쪽 같은 자리의 값 | — | **`reduction_limit_V` = 1.242 V** |

⇒ ⛔ **"Nolan 2018 도 1.72 V 라고 했다" 는 문장을 우리 1.717 V 옆에 쓰면 그것은 잘못된 문헌 지지다.**
우리 환원한계와 비교할 소환값은 **1.7 V**(argyrodite, p. 2031)이고 우리 값은 **1.242 V** 로 **0.46 V 낮다**.
그 차이는 [Rich16] digest 가 이미 진단한 것과 같은 구조다 — **hull roster 에 `Li₄P₂S₆`(P⁴⁺ 중간체)가 있느냐**에 따라
첫 환원 단계가 P⁵⁺→P⁴⁺(2.06 V)냐 P⁵⁺→P⁰(1.71/1.242 V)냐로 갈린다. **어느 쪽이 맞다고 단정하지 않는다.**

### 7c. ⛔ 황화물·염화물 스코프 판정 (1저자 물음 #4)

| | 포함? | 근거 |
|---|---|---|
| **황화물 SE** | 🟢 **완전 포함 — 사실상 주인공** | LGPS 가 §2.1·§3.1·§3.3·§4.1·§5.1·§5.3 전부의 중심. `Li₃PS₄`·`Li₇P₃S₁₁`·**`Li₆PS₅Cl`** 명시. `Fig. 6` 전체 · `Fig. 7A`(LGPS·Li₃PS₄) · `Fig. 8`(황화물 마커 40칸) · `Fig. 9B,D`(LPS) · `Fig. 11B`(LGPS·Li₃PS₄) |
| **argyrodite `Li₆PS₅Cl`** | 🟢 **본문 3회** | ① p. 2031 *"other sulfide SEs, such as Li₃PS₄, Li₇PS₁₁, and argyrodite Li₆PS₅Cl, show similarly narrow…undergoing reduction at 1.7 V and oxidation at 2.4 V"* ② p. 2036 *"the formation of elementary sulfur, polysulfides, P₂Sₓ species (x > 5), and LiCl at the Li₆PS₅Cl and oxide cathode interface"*(ref 111 Auvergniot) ③ p. 2040 *"A type 3 interface forms between the Li metal anode and SE materials with no metal cations, such as LiPON, Li₇P₃S₁₁, or Li₆PS₅Cl"* |
| **염화물 SE**(`Li₃InCl₆`·`Li₃YCl₆`·`Li₂ZrCl₆`) | 🔴 **0회. 전혀 없다** | 2018년엔 아직 무대에 없다. `Fig. 8` 의 X 는 **N, O, S, F** — "halides" 라 쓰지만 **불화물뿐** |
| **Cl 원소** | 🟡 화합물 구성원으로만 | `Li₆PS₅Cl`·`LiCl`·`Li₃OCl`·`Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃`·`Li₅PS₄Cl₂`(ref 96 제목). **Cl 의 산화한계·Cl 치환 효과는 한 줄도 없다** |

⇒ **#4(황화물 0·염화물 0) · #5(무대 가넷) 와 달리, 이 편은 우리 계(황화물 argyrodite)를 직접 다룬다.**
⇒ 그러나 **Cl-rich 축(comp1 vs modelc)은 여전히 문헌 공백**이다. 이 편도 Cl 함량 효과는 말하지 않는다.

### 7d. ⛔ 우리 db 절대값과 섞으면 안 되는 값

| 값 | 이유 |
|---|---|
| `Fig. 7`·`Fig. 11B` 의 모든 막대 끝 (LGPS 1.72/2.42 · LLZO 0.05/2.91 · `Li₃PO₄` 0.68/4.21 …) | **2015–2016 MP hull 세대**. 우리 2026 pinned GGA_GGA+U 와 0.1–0.3 V 차이가 이미 [Zhu15] digest §17 에 기록돼 있다 |
| `ΔH_D` −0.41 / −0.56 / −1.27 | **같은 양이지만 다른 계**(`Li₃PS₄` vs `Li₆PS₅Cl`) + **다른 hull 세대**. "우리 −0.3227 이 그들 −0.41 보다 덜 반응성" 이라고 쓰면 **조성 차이와 DB 차이가 뒤섞인다** |
| `Fig. 8` 의 La³⁺·Nd³⁺ 칸 | **데이터가 없다**(마커 0개, 두 패널 모두). Nd 도핑 논거로 **인용 불가** |
| `Fig. 5D` 의 σ·Ea | **AIMD(VASP 힘)** — 우리 MLIP-MD 와 다른 축 |
| `Fig. 9C` 의 계면층 두께 ≈ 40–50 nm | 다른 SE(`Li₂S–P₂S₅` glass)·다른 시편·EDX 공간분해능 한계 |
| `Fig. 11C` 의 임피던스 절대값 | ref 7(Takada 2008) 셀 기하 의존 |

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

**① ★ 개방계 `interface_reactivity` 확장 — 이 편이 준 가장 실행 가능한 숫자**
우리는 지금 `interface_reactivity_results.json` 을 **닫힌계(OCV)** 로만 돌린다(−0.3227). 이 편이 같은 계에서
**닫힌 −0.41 → 5 V 개방 −1.27 eV/atom (3.1×)** 를 인쇄한다. 즉 **우리가 보고 있는 −0.32 는 충전 상태의 계면 구동력을 ⚠ **2026-11-10 정정** — 이 '3.1 배' 는 잣대가 다른 두 수를 나눈 값이다 (−0.41 = mutual · 원자당 / −1.27 = total · 비-Li 원자당). 같은 잣대로는 mutual 1.3 배 · total 2.2 배다 (원전 `zhu2016_first_principles_interface_stability_assb` §20-2 — 정규화 판독은 그 digest 의 근거 수준).
크게 과소평가한 값일 가능성이 높다.** pymatgen `InterfacialReactivity` 에는 이미 grand-potential 모드가 있으므로
**추가 계산 비용 거의 0 으로 `μ_Li` 를 LCO 전위(≈ 3.9 V)에 고정한 판을 만들 수 있다.** → 보고량 카드 대상.
⚠ 단 **먼저 `kb/templates/estimand_card.md` §1–3**: "어떤 φ 에서 재는가"(OCV / 3.9 V / 4.3 V)가 **선택 규칙**이고,
규칙 없이 스칼라 하나를 보고하면 회신 N 의 판정("admissible state 가 여럿인데 집계 규칙이 없으면 정의되지 않는다")에 걸린다.

**② ★ `Fig. 11B` 의 반증을 우리 코팅 서사의 *강점* 으로 쓴다**
본문은 *"코팅 창 2–4 V 라서 양극에 안정"* 이라 쓰지만 자기 그림이 그것을 부정한다(§10-2). 우리가 쓸 정직한 문장:
> *"표준 산화물 코팅(LiNbO₃·LiTaO₃·Li₄Ti₅O₁₂·Li₂SiO₃)은 황화물 SE 대비 anodic 여유를 +1.2 ~ +1.8 V 벌어 주지만,
> LiCoO₂ 전위(≈3.9 V)에서는 `Li₃PO₄` 를 제외하면 여전히 열역학적 한계를 근소하게 넘어선다 — 즉 코팅의 작동 원리도
> '완전 안정' 이 아니라 '더 느린 분해 + 부동태화' 다."*
이것은 **[Xiao19] 의 "기존 코팅 3종이 자기 게이트를 못 넘는다"** 와 **정확히 같은 결론의 다른 경로**다.
두 문헌을 나란히 쓰면 우리 코팅 논의가 훨씬 단단해진다.

**③ ★ 우리 AIMD/MLIP 규율에 이 편의 문장을 붙인다**
`kb/` 의 "σ 절대값 인용 금지" 는 지금까지 **우리 내부 판정**으로만 서 있다. 이 편 p. 2020 이 **같은 그룹(Mo)이 같은 말을
2018년에 활자로** 해 두었다: *"the error bound of extrapolated RT ionic conductivity can be as large as two orders of magnitude."*
→ 리뷰어 방어 문장 확보. ⚠ **동시에 우리에게 불리한 문장도 같이 있다** — *"fewer data points … improperly performed"*.
3점 Arrhenius 를 쓰는 한 이 문장은 우리를 겨눈다. 원고에 **3점을 쓴 이유**(400/500 K 제외 판정)를 명시해야 한다.

**④ `Fig. 2B` 의 이중축 작도를 우리 ESW 그림에 차용**
μ_Li 축은 위로, φ 축은 아래로(반대 방향) 그리고 오른쪽에 상평형 띠를 세로로 붙이는 양식 — 식 (4) 를 그림으로
설명하는 가장 간결한 방법이다. `Fig. 7A`·`Fig. 7B`·`Fig. 11B` 가 전부 이 양식이다. `tools/figures/house_style.py` 와 호환.

**⑤ 질화물 축 — 우리가 아직 안 건드린 곳**
p. 2040: *"metal cations in the presence of high nitrogen content form nitride compounds, which are stable against Li metal"*
+ *"local enriching of nitrogen content can be achieved through **surface nitriding treatments**, or by the incorporation of
nitrogen-rich materials as electrolyte additives"* (ref 101 [Zhu17], ref 154 lithium azide). **우리 Li₃N 축과 직결**이지만
⛔ CLAUDE.md 규율상 **UMA 는 Li₃N 에 사용 금지** — 이 방향은 DFT 로만 간다.

---

## 9. 인용 가능 문장 (deck/paper용) — **페이지 포함**

> ⚠ 전부 **리뷰의 서술**이다. 수치를 인용할 때는 §12 의 **원출처**를 함께 달아야 한다.

1. **[정의 — anodic/cathodic limit]** *"The cathodic and anodic limits of a material are the potentials at which the reduction and the oxidation reactions become thermodynamically favorable, respectively."* — Nolan et al., *Joule* **2**, **p. 2022** (2018).
2. **[정의 — ESW]** *"The electrochemical window is the gap between the reduction and oxidation potentials based on the Gibbs free energy difference of the reactants and products, and is different from the band gap or the gap between the levels of HOMO and LUMO… the gap between HOMO and LUMO is an upper bound of the electrochemical window."* — **p. 2022** (근거 ref 65 Peljo & Girault 2018 · ref 66 Ong 2011 · ref 67 Han 2017).
3. **[정의 — μ_Li(φ)]** *"the equilibrium under an applied potential φ referenced to Li metal μ⁰_Li can be described by an equilibrium at Li chemical potential μ_Li(φ) = μ⁰_Li − eφ"* (Equation 4) — **p. 2022**.
4. **[정의 — `E_hull`]** *"The energy above hull of a compound, E_hull … corresponds to the absolute value of the decomposition energy of the compound at its thermodynamic phase equilibria."* — **p. 2020**.
5. **[정의 — 계면 평형]** *"If the phase equilibria contain phases other than the two original materials, these two materials are not in equilibrium with each other, and may react exothermically to form other phases."* — **p. 2022**.
6. **[우리 계]** *"other sulfide SEs, such as Li₃PS₄, Li₇PS₁₁, and argyrodite Li₆PS₅Cl, show similarly narrow thermodynamic electrochemical windows, undergoing reduction at 1.7 V and oxidation at 2.4 V."* — **p. 2031** (원출처 ref 63 [Zhu15] · ref 71 [Rich16]).
7. **[우리 계면 산물]** *"the formation of elementary sulfur, polysulfides, P₂Sₓ species (x > 5), and LiCl at the Li₆PS₅Cl and oxide cathode interface."* — **p. 2036** (원출처 **ref 111 = Auvergniot et al., Chem. Mater. 2017, 29, 3883**).
8. **[CV 아티팩트]** *"CV measurements using the semi-blocking electrode setup overestimate the true electrochemical window governed by the intrinsic thermodynamics of SEs. The reported wide electrochemical windows of SEs are largely an artifact of the semi-blocking electrode setup."* — **p. 2030**.
9. **[코팅의 역할 재정의]** *"the role of the coating layer is to limit interfacial decomposition rather than to suppress the formation of space charge layers as previously speculated."* — **p. 2039**.
10. **[음이온 모순]** *"Fluoride-based compounds with low Li content would have high anodic limits, and nitride-based materials with high Li content would have low cathodic limits. Therefore, the materials chemistries for high anodic limits contradict those for low cathodic limits. It would be challenging to develop a single SE material with a thermodynamic intrinsic electrochemical window of 0–5 V."* — **p. 2032**.
11. **[AIMD 오차]** *"the error bound of extrapolated RT ionic conductivity can be as large as two orders of magnitude."* — **p. 2020** (원출처 ref 39 = He, Zhu, Mo, *J. Mater. Chem. A* 2018).
12. **[NEB 한계]** *"knowledge of the energy barriers alone is inadequate to support claims about high ionic conductivity within a material."* — **p. 2019**.
13. **[Haven]** *"Since the ion hoppings in many fast ion conductor materials are strongly correlated, the quantification of ionic conductivity should consider the correlation factor, such as the Haven ratio."* — **p. 2020**.
14. **[SOC/전압 의존]** *"Li₃PS₄ reacts much more favorably with Li₀.₅CoO₂ (ΔH_D = −0.56 eV/atom) or at 5 V (ΔH_D = −1.27 eV/atom) than with LCO (ΔH_D = −0.41 eV/atom)."* — **p. 2035** (원출처 ref 70 = [Zhu16] JMCA 4, 3253).
15. **[MLIP 전망 — 2018년의 공백]** *"current interatomic potentials may not be adequate, because describing complex atomistic configurations and diverse chemical environments in amorphous materials and interfaces may require the accuracy and versatility of DFT methods."* — **p. 2041**. ★ **우리 UMA 작업이 정확히 이 공백을 메운다** — 도입부에 쓰기 좋다.

---

## 10. 주의/한계 (over-claim 방지) — **본문↔그림 어긋남 6건 포함**

**[리뷰 자체의 구조적 한계]**
- **자체 계산 0 · 자체 실험 0 · SI 0 · 계산 파라미터 0.** 모든 수치가 2차 인용이다. 재현 불가.
- **2018년이다.** 할라이드 SE(`Li₃InCl₆` 계열) 부재 · MLIP 부재 · 기계적 물성 부재 · 무질서 처리(SQS/enumerate) 부재.
- 계면 논의가 전부 **벌크 에너지 근사**다. 저자 자신이 p. 2041 에서 인정: *"these approaches still rely on bulk-phase energetics and properties to approximate interfaces… may not fully reflect the actual atomic structure, stoichiometry, chemistry, defects, or microstructures at the interface."*

**[본문↔그림 어긋남 — 본 digest 가 확인한 6건]**

| # | 어긋남 | 확인 방법 | 우리에게 걸리나 |
|---|---|---|---|
| **1** | **`Fig. 9` 패널 라벨이 본문에서 뒤바뀌었다.** 본문 p. 2034 은 `ΔH_D` 계산을 *"(Figure 9C)"*, EDX 를 *"(Figure 9B)"* 라 쓰는데, **캡션과 실제 그림은 정반대**((B) = 계산, (C) = STEM/EDX) | `fig_9.png` 직접 판독 | 🟡 인용 시 **캡션 기준(9B = 계산)** 으로 써야 한다 |
| **2** | ★ **"코팅 창 2–4 V 이므로 양극에 안정" 이 자기 그림과 어긋난다.** p. 2039 본문 vs `Fig. 11B`: 코팅 5종의 **cathodic limit 은 0.68–1.72 V**(2 V 아님), **anodic limit 은 3.61–4.21 V**, 그리고 **5종 중 4종이 `LiCoO₂` 전위선(figure-read ≈ 3.90 V) 아래**다 | `f11_B.png` 1.9× 확대 판독 | 🔴 **걸린다.** 이 문장을 그대로 인용하면 안 된다. 우리 대체 문장 = §8-② |
| **3** | **`Fig. 9B` 캡션이 그림보다 좁다.** 캡션은 *"Calculated enthalpy of decomposition of **LCO-LPS**"* 라고 한 계만 말하는데, 그림에는 **LLZO·LATP·LiPON·LPS 네 계**가 그려져 있다 | 그림 판독 | 🟢 무해(캡션이 덜 말한 것) |
| **4** | **`Fig. 6B` 의 화살표 위치가 본문 수치와 다르다.** 본문 p. 2030: *"reduction … start at 1.6 V, and the oxidation … at 2.7 V"*. 그림: 환원 화살표 **figure-read ≈ 1.0 V**, 산화 화살표 **≈ 2.25 V**(피크 **≈ 2.9 V**) | `f6_B.png` 1.8× 확대 | 🟡 **1.6/2.7 은 원출처 [Han16] 의 onset 해석값**으로 보인다. 그림에서 직접 읽히지 않으므로 **"그림에서 읽었다" 고 쓰면 안 된다** |
| **5** | **`Li₇PS₁₁` 오타** (p. 2031) — `Li₇P₃S₁₁` 이어야 한다. 같은 문단에서 다른 곳은 올바르다 | 본문 대조 | 🟢 무해하지만 그대로 복사하지 말 것 |
| **6** | **`Fig. 5D` 표 vs 본문의 실험 Ea 불일치.** 본문 p. 2023: LGPS 실험값 *"12 mS cm⁻¹ and 0.24 eV"*(ref 1). 표: Expt **12 mS cm⁻¹**, Ea **0.25 eV**. 같은 ref 1 을 가리키면서 0.24 vs 0.25 | `fig_5.png` 판독 | 🟢 0.01 eV — 무해하나 인용 시 표 값(0.25) 사용 |

**[그 밖의 주의]**
- `Fig. 7` 캡션은 *"Reproduced from Zhu et al.⁷⁰"* 로 **ref 70 (Zhu 2016 JMCA)만** 표시하는데, **패널 (A) 의 내용(Li binary + SE 창 + 0 V/5 V 상평형)은 [Zhu15](ref 63)의 대표 그림 형식**이다. 본문은 창 값을 **ref 63·71** 로 인용한다. ⇒ **패널별 원출처 귀속이 불명확** — 우리가 이 그림을 재인용할 때 **ref 63 과 70 을 함께** 달아야 안전하다.
- `Fig. 8` 의 x축에 **La³⁺·Nd³⁺·Eu³⁺·Cu²⁺·Yb³⁺ 칸이 있는데 마커가 없다**(두 패널 모두). 빈 칸의 의미(데이터 없음 vs 값 0)가 그림·캡션 어디에도 설명돼 있지 않다 ⇒ **빈 칸을 "안정하다"로 읽으면 안 된다**.
- p. 2022 원문에 **`"that that"` 중복 오타**가 있다(*"Computational studies have shown that that the gap…"*). 그대로 인용할 때 `[sic]` 또는 정정 표기.
- 🔧 **도구 결함(우리 쪽)**: `tools/litdb/extract_figures.py` 의 자동 bbox 가 `Fig. 10` 을 **1단 폭으로 잡아 type 3 패널을 잘랐다**. 이 digest 작성 중 `fig_10.png` 를 **저널 p. 2037 원본에서 재렌더해 교체**하고 `figures.json` 의 `bbox`·`note` 를 갱신했다. **다른 논문에도 같은 종류의 잘림이 있을 수 있다** — `--audit` 로 점검 대상.

---

## 11. 용어 미니사전 (이 편을 읽는 데 필요한 것만)

- **GPPD (grand potential phase diagram)** — 계를 **한 원소(여기선 Li)에 열어 두고** 그 원소의 화학퍼텐셜 μ 를 외부 변수로 잡아 그린 상태도. 닫힌 상태도가 "조성 vs 에너지" 라면 GPPD 는 "**μ vs 상평형**" 이다. 전지에서는 식 (4) 로 μ_Li ↔ 전압 φ 가 1:1 대응하므로, GPPD 는 곧 **전압별 상평형표**가 된다. 원전 = ref 56 (Ong, Wang, Kang, Ceder, *Chem. Mater.* **20**, 1798, 2008).
- **anodic limit / cathodic limit** — 각각 **산화/환원 반응이 열역학적으로 유리해지기 시작하는 전위**(p. 2022 정의). 우리 `oxidation_limit_V` / `reduction_limit_V`.
- **intrinsic electrochemical window** — 그 물질 **자체의** 열역학적 안정 전압 구간. "실험에서 보이는 창" 과 구별하기 위한 말 — 실험 창은 kinetics + interphase 덕분에 더 넓게 보인다.
- **pseudo-binary** — 두 고정 조성(전해질·전극)을 잇는 **조성 직선 위에서만** 반응을 허용하는 구성. "계면에서는 두 상만 만난다" 를 조성공간에 투영한 것. 혼합분율 `x` 를 훑어 가장 음수인 `ΔH_D` 를 그 계면의 구동력으로 본다.
- **`ΔH_D` (decomposition enthalpy)** — 위 pseudo-binary 에서 얻는 **원자당 반응 엔탈피**. 음수 = 발열 = 반응성. 이 편의 표기이고, #4·#5 의 `E_d` 와 같은 양.
- **MIEC (mixed ionic-electronic conductor)** — Li⁺ 와 e⁻ 를 **둘 다** 통과시키는 상. 계면에 MIEC 가 생기면 전자가 계속 공급돼 분해가 멈추지 않는다 → **type 2**.
- **type 1 / 2 / 3 계면** — 1 = 본질적으로 안정(반응 없음) · 2 = MIEC interphase(계속 두꺼워짐, **피해야 함**) · 3 = 전자절연·이온전도 interphase(= SEI, **바람직함**). `Fig. 10`.
- **semi-blocking electrode** — CV 에서 SE 한쪽에 붙이는 전자전도성 금속(Pt 등). **SE 와의 접촉면적이 작아** 분해 전류가 작게 나오고, 그 때문에 창이 넓어 보인다. 처방 = SE 에 흑연 ~25 wt% 를 섞은 **복합전극**(ref 64).
- **concerted migration (협동 이동)** — 여러 Li 가 ~1 ps 안에 동시에 이웃 자리로 뛰는 것. 높은 자리에 있던 Li 가 내려오며 **에너지를 상쇄**해 총 장벽이 단일이온보다 낮아진다(`Fig. 4A,B`).
- **bcc 음이온 부격자 설계원리** — 음이온이 bcc 로 배열되면 사면체 자리들이 **면공유**해 Li 가 사면체 → 사면체로 바로 이동한다(장벽 ≈ 0.2 eV). fcc·hcp 는 중간에 팔면체를 거쳐야 해서 훨씬 높다. 원전 = ref 23 (Wang et al., *Nat. Mater.* 2015).
- **Haven ratio** — 전하 확산과 자기확산의 비. 홉이 상관돼 있으면 1 이 아니다. 우리는 1 로 두고 있고, 이 편이 "고려해야 한다" 고 단서를 단다.

---

## 12. ★ 원출처 귀속표 — **리뷰의 요약을 원출처의 주장으로 둔갑시키지 않기 위해**

> 이 리뷰에서 우리가 쓰고 싶은 수치·주장은 **전부 남의 것**이다. 아래가 그 지도다.
> ⛔ **인용 규칙**: "Nolan 2018 에 따르면 Li₆PS₅Cl 창이 1.7–2.4 V" ❌ → "Nolan et al. (*Joule* 2018, p. 2031)이 요약한 바,
> [Zhu15]·[Rich16] 의 계산에서 Li₆PS₅Cl 창은 1.7–2.4 V" ⭕

| 리뷰의 내용 | ref | 원출처 서지 | 우리 litdb |
|---|---|---|---|
| **GPPD 기법 자체** | **56** | Ong, S.P., Wang, L., Kang, B., Ceder, G. (2008) *Chem. Mater.* **20**, 1798–1807 — "Li–Fe–P–O₂ phase diagram from first principles" | ⛔ 없음 (**방법의 진짜 조상 — digest 후보**) |
| `E_hull` 임계 100 meV/atom | 57 | Sun, W. et al. (2016) *Sci. Adv.* **2**, e1600225 | ⛔ 없음 |
| LGPS 치환체 예측(Si/Sn), `E_hull` 히트맵, `Fig. 5` | **62** | Ong, S.P., Mo, Y., Richards, W.D., Miara, L., Lee, H.S., Ceder, G. (2013) *Energy Environ. Sci.* **6**, 148–156 | ✅ `ong2013_lgps_family_substitution.md` |
| **ESW / Li binary·SE 창 / type 분류** | **63** | **Zhu, Y., He, X., Mo, Y. (2015) *ACS Appl. Mater. Interfaces* **7**, 23685–23693** | ✅ **`zhu2015_esw_grand_potential_origin.md` — 우리 ESW 방법 원전** |
| **LGPS 1.72/2.42 V · CV 실험 · `Fig. 6`** | **64** | **Han, F., Zhu, Y., He, X., Mo, Y., Wang, C. (2016) *Adv. Energy Mater.* **6**, 1–9** | ⛔ 없음 (**digest 후보 — 우리 ESW 의 실험 검증 원전**) |
| "HOMO–LUMO ≠ ESW" | 65 | Peljo, P., Girault, H. (2018) *Energy Environ. Sci.* — "The HOMO-LUMO misconception" | ⛔ 없음 (**우리 gap↔ESW 규율의 원전**) |
| HOMO–LUMO 가 **상한** | 66·67 | Ong et al. (2011) *Chem. Mater.* **23**, 2979 · Han, Y.-K. et al. (2017) *RSC Adv.* **7**, 20049 | ⛔ 없음 |
| 계면 평형 계산의 제안 | **69–71** | Miara, Richards, Wang, Ceder (2015) *Chem. Mater.* **27**, 4040 · **Zhu, He, Mo (2016) *JMCA* **4**, 3253–3266** · **Richards, Miara, Wang, Kim, Ceder (2016) *Chem. Mater.* **28**, 266–273** | 70 = ⛔ 없음(**[Zhu16] — `ΔH_D` −0.41/−0.56/−1.27 과 `Fig. 7`·`Fig. 9B,D` 의 실제 주인. 최우선 digest 후보**) · 71 = ✅ `richards2016_interface_stability_pseudobinary.md` |
| **`Fig. 8` (Li-M-X 삼원 cathodic/anodic limit)** · 질화물 전략 | **101** | **Zhu, Y., He, X., Mo, Y. (2017) *Adv. Sci.* **4**, 1–11 — "Strategies based on nitride materials chemistry to stabilize Li metal anode"** | ⛔ 없음 (**digest 후보**) |
| bcc 음이온 부격자 설계원리 | 23 | Wang, Y., Richards, W.D., Ong, S.P., Miara, L. et al. — *Nat. Mater.* 2015 | ⛔ 없음 |
| **협동 이동 (concerted migration)** | **34** | He, X., Zhu, Y., Mo, Y. (2017) *Nat. Commun.* — "Origin of fast ion diffusion in super-ionic conductors" | ⛔ 없음 (**우리 `jeon2026`·`ishikawa2025` 축의 원전**) |
| **AIMD 통계오차 · 2 자릿수 · 적합 절차** | **39** | **He, X., Zhu, Y., Epstein, A., Mo, Y. (2018) *J. Mater. Chem. A* (본 리뷰 인용 형식)** — AIMD 확산 통계 | ⛔ 없음 (**우리 MSD/Arrhenius 규율의 원전 — digest 후보**) |
| LGPS AIMD 최초 | 38 | Mo, Y., Ong, S.P., Ceder, G. (2013) *Chem. Mater.* | ⛔ 없음 |
| LGPS\|Li 계면 in situ XPS·임피던스 (`Fig. 6D`) | 100 | Wenzel, S. et al. (2016) *Chem. Mater.* **28**, 2400–2407 (Janek 그룹) | ⛔ 없음 |
| **`Li₆PS₅Cl`\|산화물 양극 계면 산물 (S, 폴리설파이드, P₂Sₓ, LiCl)** | **111** | **Auvergniot, J., Cassel, A., Ledeuil, J.-B., Viallet, V., Seznec, V., Dedryvère, R. (2017) *Chem. Mater.* **29**, 3883–3890** — "Interface stability of argyrodite Li₆PS₅Cl toward LiCoO₂, LiNi₁/₃Co₁/₃Mn₁/₃O₂, and LiMn₂O₄" | ⛔ 없음 (**★ 우리 계에 가장 직접적인 실험 원전. digest 최우선**) |
| LiPON\|Li in situ XPS (`Fig. 9A`) | 121 | Schwöbel, A. et al. (2015) *Surf. Sci.* (Elsevier, 2015) | ⛔ 없음 |
| LCO\|Li₂S–P₂S₅ STEM/EDX (`Fig. 9C`) · Li₂SiO₃ 코팅 | 6 | Sakuda, A., Hayashi, A., Tatsumisago, M. (2010) *Chem. Mater.* (ACS 2010) | ⛔ 없음 |
| LiTaO₃ 코팅 두께별 임피던스 (`Fig. 11C`) | 7 | Takada, K. et al. (2008) *Solid State Ionics* (Elsevier 2008) | ⛔ 없음 |
| 코팅 후보 예측 (계산) | 148·149 | Tian, Y. et al. (2017) *Energy Environ. Sci.* **10**, 1150 · Tang, H. et al. (2018) *Chem. Mater.* **30**, 163 (Na 계) | ⛔ 없음 |
| `Li₃Y(PS₄)₂`·**`Li₅PS₄Cl₂`** 예측 | 96 | Zhu, Z., Chu, I.-H., Ong, S.P. (2017) *Chem. Mater.* **29**, 2474–2484 | ⚠ **우리 ESW phase set 에서 `Li₅PS₄Cl₂` 를 제외한다** — 그 상의 출처가 여기다 |
| 12,000 후보 ML 스크리닝 | 93 | Sendek, A.D. et al. (2017) *Energy Environ. Sci.* **10**, 306 | ✅ `sendek2017_ml_screening_12k_conductors.md` |
| LiZnPS₄ 계열 예측 | 36 | (본 리뷰 ref 36) | ⛔ 없음 |
| 화학-기계 팽창 | 156 | Koerver, R. et al. (2018) *Energy Environ. Sci.* **11**, 2142 | ⛔ 없음 |

🔑 **이 표가 말하는 것**: 이 리뷰가 인용하는 **핵심 6편이 우리 litdb 에 없다** — **ref 70 [Zhu16] JMCA**(계면 `ΔH_D` 와
`Fig. 7`·`Fig. 9` 의 실제 주인) · **ref 111 [Auvergniot17]**(우리 계의 실험 계면 산물) · **ref 64 [Han16]**(ESW 의 실험 검증) ·
**ref 101 [Zhu17]**(`Fig. 8` 의 주인) · **ref 39 [He18]**(AIMD 통계 규약) · **ref 56 [Ong08]**(GPPD 원전).
⇒ **리뷰를 읽은 진짜 소득은 "다음에 읽을 6편의 목록"이다.**

---

## 13. 한 줄 결론

**#7 은 새 결과가 아니라 *어휘* 를 준다 — 그리고 계보 카드가 두 편에 걸쳐 찾던 문장이 실제로 여기 있다:
저널 p. 2022, *"cathodic/anodic limit = 환원/산화 반응이 열역학적으로 유리해지는 전위"*.**
다만 그 문장은 **물리적 정의**일 뿐 **연산 규칙**이 아니어서, *"limit ≡ E_D^open 이 0 을 벗어나는 φ"* 는 이 계보 8편
어디에도 활자로 없다 — **우리 원고는 우리 정의를 스스로 써야 한다.** 대신 이 편은 다른 것을 준다:
**① 우리 −0.3227 eV/atom 과 *같은 양* 인 소환값 −0.41 / −0.56 / −1.27 eV/atom(닫힌→탈리튬→5 V 개방),
② 우리 계(황화물 argyrodite)를 계보 8편 중 처음으로 정면에 놓은 편, ③ 우리 MLIP-MD 규율(σ 절대값 금지·Haven)의
문헌 정당화, ④ 그리고 자기 그림이 자기 본문을 반증하는 자리 하나 — `Fig. 11B`.** 그 반증이 오히려 우리 코팅 서사를
더 정직하게 만들어 준다.

---

<!-- MERGE-BLOCK — 공유 파일 수정 금지 지시(2026-09-12)에 따라 여기에 보관. 다른 두 편이 끝나면 사람이 옮긴다.
     ⚠ 옮길 때 확인: ① INDEX.md 는 "## ✅ Digest 완료 (paper-level)" 표에 넣는다 (열 3개: slug / 논문 / 축)
                    ② comparison_vs_ours.md 는 **물성 4축 표에 넣지 않는다** — 이 편은 자체 물성값이 0 이다.
                       "### J-7. 🔧 방법 원전" 절 아래에 블록으로 붙인다.
                    ③ 계보 카드는 kb/syntheses/cathode_coating_computational_lineage.md 의 #7 행 litdb 칸만 교체.

=== (a) litdb/INDEX.md — "## ✅ Digest 완료 (paper-level)" 표에 추가할 행 ===

| `papers/nolan2018_computation_accelerated_design_review.md` | **[외부·리뷰·⭐⭐⭐ 코팅 계산 계보 #7 = 계보 전체의 *어휘집* · ★ `anodic/cathodic limit` 의 **정의 문장**이 실제로 있는 유일한 편(p. 2022) · ★ 우리 계(황화물 argyrodite)를 계보 8편 중 처음 정면에 놓은 편]** ✅ **Adelaide M. Nolan**/**Yizhou Zhu**/**Xingfeng He**/**Qiang Bai**/**Yifei Mo\*** (UMD MSE + Maryland Energy Innovation Inst. 단일기관 5인), "**Computation-Accelerated Design of Materials and Interfaces for All-Solid-State Lithium-Ion Batteries**" (***Joule* 2, 2016–2046 (2018)**, DOI 10.1016/j.joule.2018.08.017; DOE-EERE **DE-EE0006860 + DE-EE0007807**; MARCC; inbox #111 본문 26 pp + 참고문헌 5 pp, **SI 없음**, refs **156**, 그림 **11장**·표 0장). ⚠⚠ **자체 DFT 0 · 자체 실험 0 · 계산 파라미터 0** — 전량 2차 인용이다. **⚠ 연대 주의: 2018년이라 #4(2019)·#5(2021)보다 먼저다** — "교과서" 는 *선행* 의 뜻이고, 이 편은 #4·#5 를 인용하지 않는다(공통 조상 [Zhu15] ref 63 · [Zhu16] ref 70 · [Rich16] ref 71 · [Ong08] ref 56 을 인용). **★★ 계보 카드가 #4·#5 끝에 남긴 물음의 답이 여기 있다**: **p. 2022**, Equation 4 (`μ_Li(φ)=μ⁰_Li−eφ`) 바로 다음 문장 — *"The cathodic and anodic limits of a material are the potentials at which the reduction and the oxidation reactions become thermodynamically favorable, respectively."* + *"The electrochemical window is the gap between the reduction and oxidation potentials… different from the band gap or HOMO–LUMO gap… HOMO–LUMO is an **upper bound**."* ⛔ **단 연산적 표현(“E_D^open 이 0 을 벗어나는 φ”)은 이 편에도 없다** — 계보 8편 통틀어 없다. 번호 붙은 식은 **딱 4개**(MSD·Nernst–Einstein·Arrhenius·μ_Li(φ))이고 `E_hull` 은 문장, `ΔH_D` 는 `Fig. 2C` 캡션으로만 정의된다. **소환값(⛔ 우리 db 이식 금지·전부 2차 인용)**: 황화물 창 **1.7–2.4 V**(`Li₃PS₄`·`Li₇P₃S₁₁`·**`Li₆PS₅Cl`** 명시, p. 2031, 원출처 ref 63·71) · LGPS **1.72/2.42 V**(`Fig. 6A`, ref 64 Han16) · 산화물 SE 산화 **2.9–4.3 V** · **`ΔH_D`: `Li₃PS₄`\|LCO −0.41 → \|`Li₀.₅CoO₂` −0.56 → @5 V −1.27 eV/atom**(p. 2035, ref 70 Zhu16; 산물 `Li₃PO₄+Li₂SO₄+Li₂S+Co₉S₈`) · `Fig. 9B` figure-read **LiPON −0.098 · LATP −0.053 · LLZO ≈0** · `Fig. 8` 음이온 서열 **anodic 불화물 6–7.2 ≫ 산화물 2.8–5.0 > 황화물 1.9–2.7 > 질화물 0.3–1.5 V**(우리 2.14/2.256 이 황화물 밴드 안) · `Fig. 11B` figure-read 코팅 창 `Li₄Ti₅O₁₂` 1.72–3.61 · `LiNbO₃` 1.72–**3.86** · `Li₂SiO₃` 0.77–3.70 · `LiTaO₃` 1.16–3.83 · **`Li₃PO₄` 0.68–4.21**(vs `LiCoO₂` 선 **3.90 V**). **★ 우리와 닿는 판정 3건**: ① **−0.3227 eV/atom 은 이 편 `ΔH_D` 와 *같은 양*** (정의·단위·부호·혼합분율 최소화 동일) ② **2.256 V 는 같은 축·더 좁은 정의**(우리는 phase-set 해시 고정 + LiS₄/SCl₃/Li₅PS₄Cl₂ 제외) ③ ⛔⛔ **`1.717 V` 함정** — `Fig. 6A` 의 **1.72 V** 는 *LGPS 의 환원한계*이고 우리 1.717 은 *Li₆PS₅Cl 의 중성 자기분해 OCV* 다. **숫자만 같고 다른 양** — 나란히 쓰면 잘못된 문헌 지지가 된다(우리 환원한계 대응값은 1.242 V, 소환값 1.7 V 와 0.46 V 차 = [Rich16] digest 가 진단한 `Li₄P₂S₆` roster 문제와 같은 구조). **⛔ 스코프**: 황화물 **완전 포함(주인공)** · argyrodite `Li₆PS₅Cl` **본문 3회** · **염화물 SE 0회**(`Fig. 8` 의 "halides" = X∈{N,O,S,F} 즉 불화물) · Cl 치환 효과 **0줄** · 기계적 물성 0 · MLIP 0(p. 2041 이 *"current interatomic potentials may not be adequate"* — 우리 UMA 가 메우는 공백) · 무질서 처리(SQS/enumerate) 0. **본문↔그림 어긋남 6건**(§10): ⚠ **`Fig. 11B` 가 "코팅 창 2–4 V → 양극에 안정"(p. 2039)을 반증** — 5종 중 4종 anodic limit 이 LCO 선 아래(⇒ 우리 대체 문장: *"코팅은 황화물 대비 +1.2~1.8 V 여유를 벌지만 LCO 전위에선 `Li₃PO₄` 외 여전히 근소 초과"*, [Xiao19] 결론과 동형) · **`Fig. 9` 패널 라벨이 본문에서 B↔C 뒤바뀜** · `Fig. 6B` 화살표(≈1.0/2.25 V)가 본문 1.6/2.7 V 와 불일치 · `Li₇PS₁₁` 오타 · `Fig. 5D` Ea 0.25 vs 본문 0.24 · `Fig. 9B` 캡션이 4계 중 1계만 언급. **🔑 최대 소득 = §12 원출처 귀속표** — 우리 litdb 에 없는 핵심 6편 확정: **ref 70 [Zhu16] JMCA 4, 3253**(`ΔH_D` 와 `Fig. 7`·`Fig. 9` 의 실제 주인·최우선) · **ref 111 [Auvergniot17] Chem Mater 29, 3883**(`Li₆PS₅Cl`\|LCO/NMC/LMO 실험 계면 — 우리 계 직격) · **ref 64 [Han16] AEM 6**(ESW 실험 검증) · **ref 101 [Zhu17] Adv Sci 4**(`Fig. 8` 주인) · **ref 39 [He18] JMCA**(AIMD 통계 2 자릿수 규약) · **ref 56 [Ong08] Chem Mater 20, 1798**(GPPD 원전). 🔧 **도구 결함 1건 수정**: `extract_figures.py` 자동 bbox 가 `Fig. 10`(3단 폭)의 **type 3 SEI 패널을 잘라내** p. 2037 원본에서 재렌더 교체 + `figures.json` bbox·note 갱신 | `papers/nolan2018_computation_accelerated_design_review.md` ✅ (2026-09-12, 본문 26 pp 전독 · **그림 11장 중 9장 실독**(`Fig. 2`·`4`·`5`·`6`·`7`·`8`·`9`·`10`·`11`; 안 본 것 = `Fig. 1` 모식도 · `Fig. 3` LGPS 확산경로) · `Fig. 6B`·`8A`·`9B`·`9D`·`11B` **1.8–2.4× 확대 재판독**) | **[외부·리뷰]** 방법론 정의 원장 (자체 계산 0 · 자체 실험 0 · SI 0) |

=== (b) litdb/comparison_vs_ours.md — "### J-7. 🔧 방법 원전" 절에 추가할 블록 (⛔ A–D 물성 4축 표에는 넣지 않는다) ===

**[Nolan18Rev] `nolan2018_computation_accelerated_design_review` — anodic/cathodic limit 의 *정의 문장* · 계면 `ΔH_D` 의 계 대조**
(⚠ 이 논문은 **자체 물성값이 0** 이다. 아래 수치는 전부 **소환값(2차 인용)** 이라 4축 표 행을 만들 수 없다.)

| 항목 | [Nolan18Rev] *Joule* 2, 2016–2046 | 우리 | 판정 |
|---|---|---|---|
| **`anodic/cathodic limit` 의 정의** | ★ **p. 2022 문장**: *"the potentials at which the reduction and the oxidation reactions become thermodynamically favorable, respectively"* (Equation 4 `μ_Li(φ)=μ⁰_Li−eφ` 직후) | `oxidation_limit_V` / `reduction_limit_V` (pymatgen `get_element_profile` 의 상평형 전이 경계) | ✅ **정의 확보** — 계보 8편 중 이 문장이 있는 유일한 편. ⛔ 단 **연산 규칙(`E_D^open ≠ 0` 인 최초 φ)은 여전히 어디에도 없다** → 우리 원고는 우리 정의를 스스로 명시해야 한다 |
| **ESW 의 정의** | *"the gap between the reduction and oxidation potentials based on the Gibbs free energy difference"* + *"different from the band gap or HOMO–LUMO gap; HOMO–LUMO is an **upper bound**"* (p. 2022, ref 65–67) | `window_V` 0.898 V (2.14−1.242) · gap 2.066/2.099 eV | ✅ **우리 "gap 과 ESW 를 섞지 말라" 규율의 문헌 근거**. gap(2.07–2.10 eV) ≫ 창(0.90–1.01 V)인 것은 결함이 아니라 정의상 당연 |
| **계면 `ΔH_D`(= `E_d`) 의 양** | `Fig. 2C`·`Fig. 9B`: 두 상 pseudo-binary 를 혼합분율로 최소화한 **eV/atom**, 음수 = 반응성 | `interface_reactivity_results.json` `min_reaction_energy_eV_per_atom` | ✅ **같은 양** (단위·부호·구성 동일) |
| **소환 대조값** (⛔ 우리 값 옆에 나란히 쓰지 말 것 — 계·hull 세대가 다르다) | `Li₃PS₄`\|`LiCoO₂` **−0.41** → \|`Li₀.₅CoO₂` **−0.56** → **@5 V −1.27** eV/atom (p. 2035, 원출처 ref 70 [Zhu16]) · 산물 `Li₃PO₄+Li₂SO₄+Li₂S+Co₉S₈` | comp1\|`LiCoO₂` **−0.3227** · modelc **−0.3308** · nd **−0.3285** · 산물 `Co₉S₈+Li₂SO₄+Li₃PO₄+Li₂S+LiCl` | 🟢 **산물 4종 완전 일치**(우리 쪽에 `LiCl` 추가 = Cl 이 있어서) ⚠ 값 비교 금지 |
| ★ **개방계 확장의 정량 동기** | **닫힌 −0.41 → 5 V 개방 −1.27 = 3.1×** | 우리는 **닫힌계(OCV)만** 돌린다 | 🔴 **공백**. pymatgen 에 grand-potential 모드가 이미 있으므로 비용 ≈ 0 → **보고량 카드 대상**(φ 선택 규칙을 먼저 선언해야 함, 회신 N) ⚠ **2026-11-10 정정** — 이 '3.1 배' 는 잣대가 다른 두 수를 나눈 값이다 (−0.41 = mutual · 원자당 / −1.27 = total · 비-Li 원자당). 같은 잣대로는 mutual 1.3 배 · total 2.2 배다 (원전 `zhu2016_first_principles_interface_stability_assb` §20-2 — 정규화 판독은 그 digest 의 근거 수준). |
| ⛔ **`1.717 V` 함정** | `Fig. 6A` 의 **1.72 V = LGPS 의 환원한계**(첫 리튬화 plateau, P⁵⁺ 환원) | 우리 **1.717 V = `Li₆PS₅Cl` 의 중성 자기분해 OCV** (`→ Li₃PS₄+Li₂S+LiCl`) | 🔴 **숫자만 같고 다른 양·다른 물질.** 나란히 쓰면 **잘못된 문헌 지지**. 우리 환원한계 1.242 V 와 비교할 소환값은 **1.7 V**(argyrodite, p. 2031) — 0.46 V 차, [Rich16] 의 `Li₄P₂S₆` roster 문제와 같은 구조 |
| **AIMD/MD 통계 규율** | *"the error bound of extrapolated RT ionic conductivity can be as large as **two orders of magnitude**"* + *"…significantly larger if **fewer data points** are used to fit the Arrhenius plot"* + *"should consider… the **Haven ratio**"* (p. 2020, 원출처 ref 39) | σ 절대값 인용 금지 · Arrhenius **3점**(600/800/1000 K) · Haven = 1 | ✅ **금지 규율의 문헌 정당화 확보** ⚠ **동시에 우리를 겨눈다** — `Fig. 5C` 의 AIMD 는 **8점(500–1250 K)** 이다. 3점을 쓴 이유(400/500 K 제외 판정)를 원고에 명시할 것 |
| **NEB 단독 주장 금지** | *"knowledge of the energy barriers alone is **inadequate to support claims** about high ionic conductivity"* (p. 2019) | 우리 BVSE·NEB 단독 서술 | ✅ 그대로 인용 가능 |
| **코팅의 anodic 여유** | `Fig. 11B` figure-read: `LiNbO₃` 3.86 · `LiTaO₃` 3.83 · `Li₂SiO₃` 3.70 · `Li₄Ti₅O₁₂` 3.61 · **`Li₃PO₄` 4.21** vs `LiCoO₂` 선 **3.90 V** | 우리 코팅 논의 | 🔴 ⛔ **본문의 "창 2–4 V → 양극에 안정"(p. 2039)은 인용 금지 — 자기 그림이 반증한다.** 대체 문장: *"코팅은 황화물 SE(2.42 V) 대비 +1.2~1.8 V 여유를 벌지만 LCO 전위에선 `Li₃PO₄` 외 여전히 근소 초과"* ⇒ **[Xiao19] 의 "기존 코팅 3종이 자기 게이트 탈락" 과 동형 결론, 다른 경로** |
| **type 1/2/3 계면 분류** | `Fig. 10`(p. 2037; 원출처 ref 63·70·120) — 1 본질안정 / 2 MIEC(계속 성장, 회피) / 3 SEI(e⁻ 절연·Li⁺ 전도, 목표) | 우리 `sei_products` 전자구조 판정 | ✅ **프레임 확보** — "왜 산물의 밴드갭을 보는가" 의 상위 서사 |
| ⛔ **Nd/La 논거 불가** | `Fig. 8` 의 **La³⁺·Nd³⁺·Eu³⁺·Cu²⁺·Yb³⁺ 칸은 두 패널 모두 마커 0개** | 우리 Nd 도핑 축 | 🔴 **이 그림에서 Nd 를 읽어 오면 안 된다** — 데이터가 없다 |
| **스코프** | 황화물 **완전 포함**(LGPS 주인공, `Li₆PS₅Cl` 본문 3회) · **염화물 SE 0회** · Cl 치환 효과 0줄 · 탄성 0 · MLIP 0 | comp1/modelc (Cl-rich 축) | 🟡 **#4·#5 와 달리 우리 계를 직접 다룬다**. 그러나 **Cl-rich 축은 여전히 문헌 공백** |

=== (c) kb/syntheses/cathode_coating_computational_lineage.md — #7 행의 litdb 칸 (마지막 열 `⏳ 대기` 를 아래로 교체) ===

✅ **`nolan2018_computation_accelerated_design_review`** (2026-09-12) — *Joule* **2**, 2016–2046 (2018), DOI 10.1016/j.joule.2018.08.017. 저자 **Nolan/Zhu/He/Bai/Mo** (카드의 잠정 기재와 **일치, 확정**). ⚠ **연대 정정: 2018년이라 #4(2019)·#5(2021)보다 *먼저*다** — "방법 교과서" 는 *선행* 의 뜻이고 이 편은 #4·#5 를 인용하지 않는다(공통 조상 ref 63 [Zhu15]·70 [Zhu16]·71 [Rich16]·56 [Ong08] 을 인용). **★★ 카드가 #4·#5 끝에 남긴 물음 — "anodic limit 의 정의가 활자로 있는가" — 의 답: 있다.** 저널 **p. 2022**, Equation 4 (`μ_Li(φ)=μ⁰_Li−eφ`) 직후: *"The cathodic and anodic limits of a material are the potentials at which the reduction and the oxidation reactions become thermodynamically favorable, respectively."* + 같은 문단에 ESW 정의(*"gap between the reduction and oxidation potentials based on the Gibbs free energy difference"*) 와 **"HOMO–LUMO 는 상한"**. ⛔ **그러나 연산 규칙(`E_D^open(φ) ≠ 0` 인 최초 φ)은 이 편에도 없다 — 계보 8편 통틀어 없다.** 번호 붙은 식은 **딱 4개**(MSD·Nernst–Einstein·Arrhenius·μ_Li(φ)); `E_hull` 은 문장, `ΔH_D` 는 `Fig. 2C` 캡션으로만. ⇒ **#5 와 #7 을 합쳐야 정의가 완성된다**(#7 = "limit 이 무엇인가", #5 = "`E_D^open` 을 어떤 식으로 재는가"). **★ 카드 물음 ②(스코프)의 답**: **황화물 완전 포함 — 주인공이다**(LGPS 가 전편 중심, `Li₆PS₅Cl` 본문 3회: p. 2031 창 1.7–2.4 V · p. 2036 계면산물 S/폴리설파이드/P₂Sₓ/LiCl(ref 111) · p. 2040 Li 금속 type 3). **염화물 SE 는 0회**(`Fig. 8` 의 "halides" = X∈{N,O,S,F} = 불화물). ⇒ **#4(황화물 0·염화물 0)·#5(무대 가넷)의 공백을 이 편이 메운다.** **★ 우리 값 판정 3건**: ① `−0.3227 eV/atom` 은 이 편 `ΔH_D` 와 **같은 양**(대조 소환값 `Li₃PS₄`\|LCO **−0.41**, 산물 4종 일치) ② `2.256 V` 는 **같은 축·우리가 더 좁은 정의**(phase-set 고정·LiS₄ 제외) ③ ⛔ **`1.717 V` 는 다른 양** — `Fig. 6A` 의 **1.72 V** 는 *LGPS 환원한계*, 우리 1.717 은 *`Li₆PS₅Cl` 중성 자기분해 OCV*. **숫자 일치는 우연이다.** **★ 카드에 남기는 새 물음 2개**: ⓐ **ref 70 [Zhu16] *JMCA* 4, 3253 이 이 계보의 진짜 결절점이다** — `ΔH_D` −0.41/−0.56/−1.27 과 `Fig. 7`·`Fig. 9B,D` 가 전부 그 논문 것인데 **우리 litdb 에 없다**(#5 Methods 도 ref 30 = [Zhu16] 을 가리켰다). **세트 밖 최우선 digest 후보.** ⓑ **ref 111 [Auvergniot17] *Chem. Mater.* 29, 3883** = `Li₆PS₅Cl` vs LCO/NMC111/LMO 의 **실험** 계면 산물 — 우리 계 직격인데 없다. **본문↔그림 어긋남 6건** 중 우리에게 걸리는 것: **`Fig. 11B` 가 본문의 "코팅 창 2–4 V → 양극에 안정"(p. 2039)을 반증**(5종 중 4종의 anodic limit 이 `LiCoO₂` 선 3.90 V 아래; `Li₃PO₄` 4.21 만 통과) ⇒ **[Xiao19] 의 "기존 코팅 3종이 자기 게이트 탈락" 과 동형 결론**. **#1 의 산물 물리상태 게이트 복원 여부** = ❌ **이 편도 복원하지 않는다**(기체/고체 구분 0회) — 그러나 **다른 게이트를 대신 준다: 산물의 *전자전도성*(type 2 vs type 3)**. 즉 Mo 라인은 [Aykol14] 의 "물리상태" 축을 "전자구조" 축으로 **치환**했다. (#8 에서 최종 확인.) 그림 **11장 중 9장 실독**(안 본 것 = `Fig. 1` 모식도·`Fig. 3` LGPS 확산경로).

-->

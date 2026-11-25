<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-12 신규 작성:
       ① 1저자 지정 "양극 코팅 계산 계보 8편" 세트의 **#6**. #1 aykol2014 / #2 aykol2016 / #3 xiao2019 /
          #4 nolan2019 / #5 nolan2021 기존. ⚠ 이 편만 **음극(anode) 코팅**이고, 게다가 **양극이 아예 안 나온다**.
       ② 계보 카드가 이 편에 물은 다섯을 §0a 에 답부터 적었다.
       ③ 크로핑 그림 18장(본문 4 + 표 3 + SI 11) 중 **12장을 실제로 봤다**:
          본문 `Fig. 1`·`2`·`3`·`4` **전량(4/4)** + SI `Fig. S2`·`S3`·`S4`·`S5`·`S6`·`S8`·`S10`·`S11` **(8/11)**.
          ⛔ 안 본 것: `Fig. S1`·`S7`(둘 다 softBV 경로 *삽화*)·`Fig. S9`(SHAP 3장, 본문이 값을 다 적는다).
          표(`tab_*.png`)는 PDF 텍스트가 더 정확해서 이미지로 안 읽었다.
       ④ ★ 이 편은 **공개 기계판독 데이터가 0 본**이다(#2 는 CSV 2본, #4·#5 는 XLSX). 그래서 §12 의
          독립 재분석은 **XLSX 재집계가 아니라 픽셀 캘리브레이션**으로 했다 — `Fig. S2` 의 상전이 전압
          8개, `Fig. 1` 의 마커 43개 좌표, `Fig. S3–S6` 의 마커 개수.
       ⑤ 그 픽셀 판독에서 **본문↔그림 어긋남 12건**이 나왔다(§10). 그중 인용에 실제로 걸리는 것은 4건.
       ⑥ 🔑 우리에게 가장 큰 소득은 ML 이 아니라 **`Fig. S2`** 다 — 계보 6편 중 처음으로
          *"cathodic limit 이 무엇인가"* 를 **그림으로 정의**한다(Li uptake = 0 평탄구간의 아랫변).
          그 정의로 재면 우리 `reduction_limit_V` 1.242 V 는 그 양이 **아니고** `ocv_self_decomposition_V`
          1.717 V 가 그 양이다 — `comparison_vs_ours.md` 의 미해결 **digest Q3** 에 증거 1건 추가. -->

# Discovery of novel Li SSE and anode coatings using interpretable machine learning and high-throughput multi-property screening — Honrao, Yang, Radhakrishnan, Kuwata, Komatsu, Ohma, Sierhuis, Lawson (*Scientific Reports* **11** (2021) 16484)

> slug `honrao2021_interpretable_ml_sse_anode_coatings` · DOI `10.1038/s41598-021-94275-5` · type `HT 다물성 스크리닝 + 해석가능 ML (자체 DFT 0 · 자체 실험 0; 에너지는 전부 Materials Project, 이동장벽은 경험적 softBV)` · PDF `litdb/inbox/110. Honrao2021_Interpretable_ML_HT_Screening_Li_SSE_Anode_Coatings.PDF` (본문 14 pp) + `110. Sup) …PDF` (SI 19 pp: Fig S1–S11 + Table S1 + 특징 정의 S1.1–S1.22) · digested `2026-09-12` · status ✅ · 태그 **[외부]**

> elements: Li, H, Be, B, C, N, O, F, Na, Mg, Al, Si, P, S, Cl, K, Ca, Sc, Ti, Zn, Ga, Ge, As, Se, Br, Rb, Sr, Y, Zr, In, Sn, Sb, I, Cs, Ba, La, Pr, Sm, Tb, Dy, Ho, Er, Hf, Ta, Pb, Bi
> methods: DFT, BVSE, ESW

> **저자**: **Shreyas J. Honrao**¹, Xin Yang², **Balachandran Radhakrishnan\***¹, Shigemasa Kuwata², Hideyuki Komatsu³, Atsushi Ohma³, Maarten Sierhuis², **John W. Lawson\***⁴ (¹ KBR Wyle, Intelligent Systems Division, **NASA Ames** · ² **Nissan North America** Research Division, Santa Clara · ³ **Nissan Motor Company** Research Division, 요코스카 · ⁴ Intelligent Systems Division, **NASA Ames**) · 수신 2021-05-11 / 수락 2021-07-08 · **OA (Sci Rep)** · 계산 프레임 **Materials Project** (⚠ OQMD 가 아니다 — [Aykol] 두 편과 다르고 [Nolan] 두 편과 같다) · 도구 **softBV**(Chen/Wong/Adams 2019) · **Zeo++** · **pymatgen** · **scikit-learn** · **shap** · **rfpimp**
> **저자 기여 명시**: *"S.H. and B.R. computed the migration barriers and electrochemical windows, respectively."* — 즉 **자체 제1원리 계산은 한 줄도 없다**. 이동장벽 = 경험적 본드밸런스, 창 = MP 에너지 위의 상평형 연산.
>
> **계보 (1저자 지정 "양극 코팅 계산 계보" 8편 세트의 #6)**: [Aykol 2014 AENM](aykol2014_cathode_coating_thermodynamics.md)(#1) → [Aykol 2016 Nat Commun](aykol2016_ht_cathode_coating_design.md)(#2) → [Xiao 2019 Joule](xiao2019_cathode_coating_screening.md)(#3) → [Nolan 2019 ACS Energy Lett](nolan2019_chemistries_stable_high_energy_cathodes.md)(#4) → [Nolan 2021 ENSM](nolan2021_garnet_cathode_coating.md)(#5) → **본 논문**(#6) · 리뷰 2편(#7·#8).
> ⚠⚠ **이 편은 세트의 이단아다.** ① 무대가 **음극(Li 금속)** 이고 ② **양극이라는 단어가 결론에 한 번도 안 나오며** ③ 계보 #3–#5 가 세운 **계면 반응에너지(`E_d` / pseudo-binary)를 아예 쓰지 않는다**. 인용(ref 54·55·56 = [Xiao19]·[Aykol16]·[Nolan19])은 서론 한 문단뿐이고, **방법은 계승하지 않는다.** 계승한 것은 **grand-potential 창**([Zhu15] ref 53, [Richards16] ref 52) 하나다.

---

## 0. 이 digest 를 읽는 법 — 범위부터

### 0a. 1저자가 이 편에 물은 다섯 가지 — 답 먼저

| # | 물음 | 답 (근거 절) |
|---|---|---|
| **1** | **음극 코팅이면 양극 넷과 무엇이 뒤집히나. 환원 한계(우리 1.242 V)가 주역이 되나** | **축은 뒤집힌다, 그러나 절반만이다.** ✅ 스크리닝 그림 **5장 전부의 x축이 `Reduction potential (V)`** 이고(`Fig. 1`·`S3`–`S6`), 코팅 판정은 **`V_red = 0 V` 정확히**(문턱이 아니라 **불리언**)다. 산화한계는 *"창 폭 ≥ 1 V"* 라는 곁다리 제약으로 **강등**된다. ⛔ 그러나 **주역이 되는 것은 "환원 한계" 이지 우리 1.242 V 가 아니다** — §7c 에서 보듯 그들 정의(= `Fig. S2` 의 Li-uptake 0 평탄구간 **아랫변**)에 대응하는 우리 필드는 **`ocv_self_decomposition_V` 1.717 V** 쪽이다. ⛔ 그리고 가장 큰 뒤집힘은 **계면이 사라진 것**이다: 이 편에는 `E_d` 도 pseudo-binary 도 **없다**. 코팅↔Li, 코팅↔SE **두 계면 중 어느 것도 계산하지 않는다**(§10-6) → §7b |
| **2** | **"Interpretable ML" 이 정확히 무엇인가. 해석가능성이 검증됐나** | **모델 = scikit-learn `GradientBoostingRegressor`(+비교군 RF).** 표적 3개(3D 장벽 / 환원전위 / 산화전위)에 **독립 모델 3개**. 특징은 **장벽용 구조특징 22개**(Li 분율·이웃수·SPF·DLFS·XRD PCA 5개 등, `Table 1`)와 **전위용 조성특징 28개**(원소물성 8종 × {평균·최대·범위} = 24 + **신설 산화상태 특징 4개**, `Table 2`). 해석 = **SHAP**(개별 예측 분해, `Fig. 2`·`S9`) + **PFI**(모델 전역 중요도, `Fig. 3`·`4`). **검증은 사실상 안 됐다** — 논문 스스로 *"PFI analysis and Shapley explanations do not necessarily provide causality"* 라고 적고, 인과 주장의 근거로 든 것은 **치환 일화 2건**(LSiPO→LSnPO 0.305→0.518 eV, LSiPO→LSiPS 0.457 eV)뿐이며 그마저 *"**by simply changing the SPF**"* 라고 적어 **나머지 21개 특징을 고정한 채 한 특징만 바꾼 것**임을 자백한다(§7d-3) → §7d |
| **3** | **훈련 표적이 DFT 로 계산한 무엇인가. 우리 축과 대응되나** | **표적 3개 중 DFT 기반은 2개뿐이다.** ⓐ **3D 이동장벽** — **DFT 가 아니다**. 경험적 **softBV**(본드밸런스 미스매치 → Morse 포텐셜 → 3방향 침투 등에너지면)의 출력이고, 논문 스스로 *"softBV barriers should not be used to directly estimate the ionic conductivity"* 라고 적는다 ⇒ 우리 `Ea`(MLIP-MD 아레니우스, comp1 0.253 / modelc 0.224 eV)와 **같은 양이 아니다**. ⓑ·ⓒ **산화·환원전위** — **MP 의 DFT(GGA/GGA+U) 에너지 위의 Li grand-potential 상평형**. 이것은 우리 `oxidation_stability.json` 과 **같은 기계**다(같은 DB·같은 기준 vs Li/Li⁺·같은 개방계). ⇒ **대응되는 것은 ⓑⓒ 뿐**이고 ⓐ 는 대응 안 된다 → §7a |
| **4** | **게이트가 Li 전도체를 배제하나** | **반대다 — 이 편은 전도체를 *요구*한다**(SE 게이트 `3D 장벽 ≤ 0.5 eV`, 코팅 게이트 `≤ 1 eV`). 계보 6편 중 **전도도 축을 1차 게이트로 세운 유일한 편**이고, 그 점에서 [Aykol16](`−E_c>3.5 V` 로 `Li₂ZrO₃`·`LiAlO₂` 절단)·[Nolan21](전도도 아예 안 봄)의 **함정을 둘 다 피한다**. ⛔ **그런데 우리 계를 배제한다** — 다른 두 게이트로: ① **`E_hull ≤ 30 meV/atom`** 이 **`Li₆PS₅Cl`·`Li₆PS₅Br` 을 잘라낸다**(본문 명시; `Li₆PS₅I` 는 통과, LGPS 는 32 meV 로 탈락) ② **`0.5 eV` softBV 문턱**이 **현대 할라이드 SE 를 통째로** 자른다(`Li₃YBr₆` 0.55 · `Li₃ScCl₆` 0.56 · `Li₃InCl₆` 0.59 — 셋 다 *"just above"*). 즉 **"전도체를 배제하는 게이트"가 아니라 "전도체를 *잘못 재는* 프록시 + 무질서 준안정성"이 배제한다** → §7e |
| **5** | **⛔ 우리 db 절대값과 섞으면 안 되는 값** | **7종**: ① 모든 **3D 장벽**(softBV ≠ 우리 MLIP-MD Ea, 논문 자신이 전도도 환산 금지) ② `Table S1` 의 **창 폭(V)** (그들 정의는 `V_ox − 0`) ③ `Fig. S2` 의 **Li₃PS₄ 창** (우리 계는 LPSCl 이고, 게다가 그들 산물에 **우리가 배제하는 `LiS₄` 가 들어 있다**) ④ **ML 예측 장벽**(`Table 4` 의 `d` 표시 5종, SHAP `f(x)`) — 모델 출력이지 계산값이 아니다 ⑤ `Table 3`·`Table 5` 의 **R²** (자기 데이터셋 내부 랜덤 분할 — 우리 cascade 의 LODO 와 규약이 다르다) ⑥ **`E_hull`·`E_g`** (MP 조회값, 세대 미기재) ⑦ **`Table 4` 의 DFT-MD 판정**(ref 60 Sendek 2018 의 2차 인용) → §7f |

### 0b. 본 그림 / 안 본 그림 (크로핑 18장 중 **12장 실독**)

| 상태 | 그림 |
|---|---|
| ✅ **봤다 (본문 4/4)** | `Fig. 1`(스크리닝 결과 산점) · `Fig. 2`(SHAP 4패널) · `Fig. 3`(장벽 PFI) · `Fig. 4`(전위 PFI a·b) |
| ✅ **봤다 (SI 8/11)** | `Fig. S2`(Li₃PS₄ 전압 프로파일 — **픽셀 캘리브레이션**) · `Fig. S3`(황화물) · `Fig. S4`(할라이드) · `Fig. S5`(산화물) · `Fig. S6`(기타·질화물) · `Fig. S8`(장벽 parity) · `Fig. S10`(Pearson 히트맵) · `Fig. S11`(전위 parity, **좌하단 3.2× 확대 재판독**) |
| ⛔ **안 봤다** | `Fig. S1`·`Fig. S7` — 둘 다 softBV 경로 **삽화**(정량 정보 0) · `Fig. S9` — SHAP 3장인데 본문이 여섯 특징 값을 **전부 활자로** 적는다 |
| ⚪ **이미지로 안 읽음(의도)** | `tab_2.png`·`tab_3.png`·`tab_S1.png` — 글자라 PDF 텍스트가 정확하다. `Table S1` 26행은 **전수 전사**했다(§3a) |

### 0c. 가져올 수 있는 것 / 없는 것

- ✅ **가져온다**: ① `Fig. S2` 가 그림으로 정의한 **cathodic limit 의 조작적 정의**(§4c·§7c) ② `Fig. 1` 의 **좌표 43개**(우리 계 인접 물질의 문헌 소환값, §12b) ③ **깔때기 설계 문법**(전도도를 1차 게이트로 쓰는 법) ④ **특징 22개 정의**(우리 cascade 기술자 후보, §8-3) ⑤ **폴리모프 민감도 실측**(같은 `LiCl` 이 0.349 ↔ 0.735 eV, §12c).
- ⛔ **못 가져온다**: 모든 **절대 장벽값**(프록시), 양극 관련 결론(**양극이 없다**), 계면 반응에너지(**없다**), 기계판독 데이터(**공개 0본**).

---

## 1. 한 줄 요약

**MP 의 Li 화합물 15,446종에 대해 ⓐ 경험적 softBV 3D 이동장벽 ⓑ Li grand-potential 전기화학 창 ⓒ `E_hull`·`E_g` 를 붙인 물성 DB 를 만들고, 다물성 깔때기로 SE 후보 250+ 종과 *Li 금속 음극 코팅* 26종을 뽑은 뒤, 같은 DB 위에 GB 회귀 3개(장벽 R² 0.86 / 환원전위 0.95 / 산화전위 0.92)를 얹고 SHAP·PFI 로 특징 기여를 보여 준 편.** 계보 #1–#5 와 달리 **양극도, 계면 반응에너지도 없다** — 남은 공통분모는 **grand-potential 창** 하나다.

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저널·권호 | *Scientific Reports* **11**, 16484 (2021) |
| DOI | `10.1038/s41598-021-94275-5` (OA) |
| 소속 구성 | **NASA Ames(계산·ML) + Nissan(문제 정의·자금)** — 산학 2기관 4소속 |
| 계산 프레임 | **Materials Project** (DFT 에너지·`E_hull`·`E_g` 전부 조회) |
| 자체 DFT | **0회** |
| 자체 실험 | **0회** |
| DB 규모 | Li 화합물 **15,446** 종 (전수 softBV) / 그중 **8,924** 종만 창 보유 |
| 공개 데이터 | **없음.** *"Data not found in the main text or SI is available from the corresponding authors upon request."* 특징 생성 스크립트도 *"available upon request"* |
| 핵심 결과물 | SE 후보 **>250** (목록 미공개, `Fig. S3–S6` 에 ~137개만 표시) · 음극 코팅 **26** (`Table S1` 전수 공개) |

---

## 3. 핵심 물성 (수치)

> ⚠ 이 논문에는 **σ·탄성계수·밴드갭 값이 하나도 인쇄돼 있지 않다**. 있는 물성은 (i) softBV **3D 장벽** (ii) **환원/산화 전위**와 그 차인 **창** (iii) `E_hull`·`E_g` (게이트로만 쓰이고 값은 안 나옴) 셋뿐이다.

### 3a. `Table S1` — **음극 코팅 후보 26종 전수** (이 논문 유일의 완전 공개 표)

> 표제: *"Compounds identified as promising candidates for coatings on Li metal anode, arranged in order of increasing 3D barriers. [Reduction potential (vs. Li) = 0 V, electrochemical window ≥1 V, 3D barrier ≤1 eV, E_hull ≤30 meV, E_g ≥1 eV]"*

| # | mp id | 조성 | 3D 장벽 (eV) | 전기화학 창 (V) | 족 |
|---|---|---|---|---|---|
| 1 | mp-9723 | **Sr₄Li(BN₂)₃** | **0.109** | 1.39 | 질화물 |
| 2 | mp-1960 | **Li₂O** | 0.259 | 2.90 | 산화물 |
| 3 | mp-1153 | **Li₂S** | 0.262 | 2.13 | 황화물 |
| 4 | mp-2286 | Li₂Se | 0.327 | 1.89 | 셀렌화물 |
| 5 | mp-1185319 | **LiCl** | 0.349 | **4.25** | 할라이드 |
| 6 | mp-976280 | LiBr | 0.350 | 3.14 | 할라이드 |
| 7 | mp-570935 | LiI | 0.352 | 2.47 | 할라이드 |
| 8 | mp-756544 | LiLaO₂ | 0.354 | 2.90 | 산화물 |
| 9 | mp-7020 | **LiYO₂** | 0.411 | 2.92 | 산화물 |
| 10 | mp-752922 | Li₈HfO₆ | 0.419 | 2.90 | 산화물 |
| 11 | mp-10970 | LiErO₂ | 0.428 | 3.00 | 산화물 |
| 12 | mp-1222669 | Li₂IBr | 0.454 | 2.47 | 할라이드 |
| 13 | mp-1198622 | **Li₇La₃Hf₂O₁₂** | 0.470 | 3.02 | 가넷 |
| 14 | mp-1181918 | Cs₃Li₂I₅ | 0.471 | 2.35 | 할라이드 |
| 15 | mp-1190687 | CsLi₂Cl₃ | 0.486 | 4.25 | 할라이드 |
| 16 | mp-1185301 | **LiF** | **0.536** ⚠ | **6.36** | 할라이드 |
| 17 | mp-1080534 | Cs₂Li₃I₅ | 0.544 | 2.35 | 할라이드 |
| 18 | mp-28237 | RbLiBr₂ | 0.590 | 3.14 | 할라이드 |
| 19 | mp-1190087 | CsLiI₂ | 0.601 | 2.35 | 할라이드 |
| 20 | mp-1184020 | CsLi₃I₄ | 0.668 | 2.35 | 할라이드 |
| 21 | mp-28243 | RbLiCl₂ | 0.703 | 4.25 | 할라이드 |
| 22 | mp-606680 | CsLi₂Br₃ | 0.774 | 2.96 | 할라이드 |
| 23 | mp-569055 | CsLi₂I₃ | 0.817 | 2.35 | 할라이드 |
| 24 | mp-770805 | Li₆Hf₂O₇ | 0.845 | 3.22 | 산화물 |
| 25 | mp-23057 | CsLiBr₂ | 0.882 | 2.96 | 할라이드 |
| 26 | mp-9610 | Li₂CN₂ | 0.982 | 2.12 | 질화물 |

**본 digest 가 이 표에서 읽은 것 (논문이 안 적는다)**
- **할라이드가 26 중 15종(58 %)** 이다. 산화물 6 · 질화물 2 · 칼코겐 3. *"음극 코팅 = 질화물"* 이라는 서론의 방향(ref 57 Zhu 2017)과 **결과가 반대**다(§10-4).
- 창 상위 3종이 전부 **F·Cl 계**(LiF 6.36 · LiCl/CsLi₂Cl₃/RbLiCl₂ 4.25) — **같은 음이온이면 창이 같다**(LiCl·CsLi₂Cl₃·RbLiCl₂ 전부 4.25, I 계 5종 전부 2.35, Br 계 2.96/3.14). ⇒ **창을 정하는 것은 양이온이 아니라 음이온**이라는 규칙이 표 안에 그대로 보인다. ⚠ 이것은 *"준안정 화합물의 창은 분해산물의 창으로 대신한다"* 는 그들 규약(§4c)의 직접 귀결이기도 하다 — 같은 산물(LiCl 등)로 분해되면 창이 같아진다.
- **`Li₂S` 창 2.13 V** — 우리 계의 산화 onset 을 정하는 바로 그 상이다(§7c).
- ⚠ **`LiF` 행이 그림 2장과 어긋난다**(0.536 ↔ `Fig. 1`·`Fig. S4` 의 **0.241**) → §10-2.

### 3b. `Table 4` — Sendek 모델이 지목한 21종을 softBV 로 다시 줄 세운 표 (검증용)

> 표제: *"… arranged in increasing order of their softBV 3D barriers. Where calculated barriers are missing, ML predictions are used instead. … `d` ML prediction"*

| # | mp id | 조성 | 3D 장벽 (eV) | DFT-MD σ > 10⁻⁴ S/cm? |
|---|---|---|---|---|
| 1 | mp-558219 | SrLi(BS₂)₃ | 0.340 | No |
| 2 | mp-532413 | Li₅B₇S₁₃ | 0.487 | **Yes** |
| 3 | mp-643069 | Li₂HIO | 0.519 | **Yes** |
| 4 | mp-7744 | LiSO₃F | 0.529 | **Yes** |
| 5 | mp-569782 | Sr₂LiCBr₃N₂ | 0.548 | Marginal |
| 6 | mp-676109 | **Li₃InCl₆** | 0.595 | **Yes** |
| 7 | mp-676361 | LiErCl₆ | 0.664 | **Yes** |
| 8 | mp-22905 | **LiCl** | **0.735** ⚠ | No |
| 9 | mp-559238 | CsLi₂BS₃ | 0.780 | **Yes** |
| 10 | mp-29410 | Li₂B₂S₅ | 0.972 ᵈ | **Yes** |
| 11 | mp-34477 | LiSmS₂ | 0.977 | No |
| 12 | mp-8430 | KLiS | 1.720 ᵈ | No |
| 13 | mp-8751 | RbLiS | 1.727 ᵈ | No |
| 14 | mp-554076 | BaLiBS₃ | 2.035 | No |
| 15 | mp-866665 | LiMgB₃(H₉N)₂ | 2.330 ᵈ | **Yes** |
| 16 | mp-19896 | Li₂GePbS₄ | 2.835 | No |
| 17 | mp-561095 | LiHo₃Ge₂(O₄F)₂ | 3.259 | No |
| 18 | mp-15791 | LiErS₂ | 4.698 ᵈ | No |
| 19 | mp-15790 | LiHoS₂ | 4.749 ᵈ | No |
| 20 | mp-15789 | LiDyS₂ | 4.872 | No |
| 21 | mp-15797 | LiErSe₂ | 4.884 | Marginal |

> ᵈ = **ML 예측값**(softBV 미산출). 5종(#10·12·13·15·18)이 여기 해당 — ⛔ 계산값과 같은 열에 섞여 있다.
> ⚠ **같은 `LiCl` 이 이 표에서 0.735 eV, `Table S1` 에서 0.349 eV** 다. 본문이 이유를 적는다: *"the LiCl structure identified by us is the DFT ground state structure, and slightly differs from the one identified by the Sendek model"* (mp-1185319 vs **mp-22905**). ⇒ **softBV 3D 장벽은 같은 조성에서 폴리모프에 따라 2.1× 흔들린다**(§12c). 이것이 이 논문 전체에서 가장 값어치 있는 오차 실측이고, 논문은 이것을 **오차로 취급하지 않는다**.

### 3c. `Table 3`·`Table 5` — ML 성능 (전부 held-out test set, 20회 90:10 랜덤분할 평균)

| 표 | 특징 + 모델 | R² | 벡터 길이 |
|---|---|---|---|
| `Table 3` (3D 장벽) | **본 논문 22특징 + GB** | **0.86** | 22 |
| | 본 논문 22특징 + RF | 0.84 | 22 |
| | Sendek 전도도 특징 + GB | 0.76 | 20 |
| | Coulomb matrix + GB | 0.72 | 200 |
| | Powder XRD 패턴 + GB | 0.70 | 128 |

| 표 | 특징 + 모델 | 환원전위 R² | 산화전위 R² | 벡터 길이 |
|---|---|---|---|---|
| `Table 5` | **본 논문 28특징 + GB** | **0.95** | **0.92** | 28 |
| | 본 논문 28특징 + RF | 0.93 | 0.91 | 28 |
| | Roost + 신경망 | 0.92 | 0.92 | 64 |
| | Magpie 원소특징 + GB | 0.89 | 0.84 | 132 |
| | 원소 분율 + GB | 0.87 | 0.87 | 103 |

> ⚠⚠ **초록과 `Table 5` 가 서로 뒤집혀 있다.** 초록: *"achieve R² values of **0.95 and 0.92 on the oxidation and reduction** potential prediction tasks, respectively"*. `Table 5`: **환원 0.95 / 산화 0.92**. 어느 쪽이 맞는지 논문 안에서 결정할 수 없다(`Fig. S11` parity 두 장의 산포가 눈으로 구분 안 된다) → §10-1. **인용할 때는 "환원·산화 각각 0.95·0.92 (논문 내부 불일치)" 로 쓰거나, 축을 지정하지 말 것.**

### 3d. 본문이 인쇄한 개별 수치 (전부 softBV 또는 GB 출력)

| 물질 | 값 | 종류 | 맥락 |
|---|---|---|---|
| `Li₉S₃N` | 3D 장벽 **0.198 eV** (SHAP `f(x)`) / 그림 마커 **0.185**(figure-read) | GB 예측 / softBV | SPF = 0.082, Li 분율 = 0.692 |
| `Li₂CO₃` | **0.182 eV**(GB) / **0.176**(figure-read) | GB / softBV | SPF = 0.068, Li = 0.333, ENS = 3.218 |
| `LiBF₄` | **0.134 eV**(GB) / **0.122**(figure-read) | GB / softBV | SPF = 0.058, ENS = 3.592, SNC = 17.20 |
| `Sr₄Li(BN₂)₃` | **0.127 eV**(GB) / **0.109**(Table S1) | GB / softBV | SPF = **0.707**(높여 미는 유일 특징), SNC = 18.615, Li = 0.071 |
| `LiAlB₂O₅` | **0.175 eV** | softBV | *"best performing oxide identified through screening"* |
| `Li₃YBr₆` / `Li₃InCl₆` / `Li₃ScCl₆` | **0.55 / 0.59 / 0.56 eV** | softBV | **0.5 eV 게이트 바로 위에서 탈락** ★ |
| `Li₁₀GeP₂S₁₂`(LGPS) | `E_hull` = **32 meV/atom** | MP | **30 meV 게이트 바로 위에서 탈락**; `Li₁₀SiP₂S₁₂` 는 통과 |
| `Li₆PS₅Cl`·`Li₆PS₅Br` | 값 미기재 | MP `E_hull` | *"excluded due to their higher E_hull values"* ★ **우리 계** |
| `Li₆PS₅I` | 3D 장벽 **0.251 eV**(figure-read), `V_red` **1.722 V**(figure-read) | softBV / grand-potential | 계에서 유일하게 통과한 아지로다이트 |
| `Li₃PS₄` | 창 **1.7 – 2.2 V**(본문) ↔ **1.70 – 2.36 V**(`Fig. S2` 픽셀) | grand-potential | ⚠ 본문↔그림 불일치 §10-3 |
| `Li₁₀SiP₂O₁₂`(LSiPO) | **0.305 eV** | softBV | 치환 일화의 기준점 |
| `Li₁₀SnP₂O₁₂`(LSnPO) | **0.518 eV** | *"SPF 만 바꿔서"* 얻은 값 | §7d-3 ⚠ |
| `Li₁₀SiP₂S₁₂`(LSiPS) | **0.457 eV** | softBV (`Fig. 1` 마커 0.456 과 일치) | §7d-3 |
| GB 모델 평균 예측 | **1.490 eV** | SHAP base value | 전체 훈련셋 평균 = 15,446종의 평균 3D 장벽 수준 |

---

## 4. DFT/계산 방법 ★

> **핵심: 이 논문에 제1원리 계산은 없다.** 두 축이 각각 다른 근거 위에 서 있고, 그 **비대칭이 논문 전체의 약점**이다.

### 4a. 이온이동 축 — **softBV (경험적 본드밸런스), DFT 아님**

1. **본드밸런스 합 규칙**: 원자 *i* 주위 결합가 합 `V_i = Σ_j S_ij` 가 형식 산화수 `V_i^id` 와 같아야 한다.
2. **결합가**: `S_ij = exp[(R₀ − R_ij)/b]` — `R₀`·`b` 는 원소쌍별 피팅 상수. (⚠ 논문의 식 (2) 조판이 깨져 지수함수 기호가 빠져 있다.)
3. **미스매치**: `|ΔV_i| = |V_i − V_i^id|`. `|ΔV_i| ≈ 0` 인 자리가 접근 가능 자리.
4. **에너지 환산**: Chen/Wong/Adams(ref 45)의 **Morse 형 BV force-field** 로 `|ΔV_i|` → eV. 고정 `|ΔV_i|` 등치면 = 그 활성화에너지로 도달 가능한 영역.
5. **차원별 장벽**: 단위셀 마주보는 면을 잇는 최저에너지 침투 등치면 → **1D ≤ 2D ≤ 3D**. **본 연구는 3D 만 쓴다.**
6. **bond softness 보정**: 1차 배위껍질만 쓰는 원래 BV 대신 고차 껍질 정보로 `R₀`·`b` 를 재피팅한 것이 **softBV**.

> 🔑 **우리 `tools/comp1_v3/` BVSE 와 같은 계열의 도구**다(우리: softBV Li–X `R₀` = S 2.105 / Cl 2.249 / O 1.466, `b` = 0.37, BVSE = (BVS−1)², ~0.25 Å voxel). ⚠ **다만 우리는 BVSE 를 "채널 % / 순위" 로만 쓰고 활성화에너지로 환산하지 않는다.** 이 논문은 **환산한다** — 그래서 값이 eV 로 나오고, 그 eV 를 곧바로 게이트(0.5 / 1.0 eV)로 쓴다.
> ⚠ 논문 자신의 경고 2개(그대로 인용 가치 있음): ① *"materials with potential for fast migration may not necessarily show high ionic conductivity unless there is a high concentration of mobile ions"* ② *"since the BV approach does not allow for the structural relaxation of neighboring atoms that accompanies migration, softBV barriers tend to be overestimated in some cases"* ⇒ **완화가 중요한 계(무질서 아지로다이트·할라이드 SE)에서 체계적으로 불리하다** — §7e 의 판정 근거.

### 4b. 열역학·전자 게이트 — MP 조회값 2개

- **`E_hull`** (0 K 볼록껍질 위 수직거리, eV/atom). 게이트 **≤ 30 meV/atom**. 논문의 방어논리: *"limiting our search to candidates with E_hull ≤30 meV ensures that the stabilities of all identified compounds at a given composition are fairly similar"* — 즉 창을 **조성당 최저에너지 상 하나**로만 계산한 근사를 정당화하는 장치다.
- **`E_g`** (MP 밴드갭). 게이트 **≥ 1 eV**, *"a relatively safe lower bound … accounting for the fact that local and semi-local DFT functionals tend to underestimate band gaps"*(ref 68 Chan & Ceder 2010). ⇒ **우리 규율(PBE 과소평가, 절대 비교 금지)과 같은 인식**이고, 그들도 **문턱으로만** 쓴다.
- **d·f-block 필터**: *"compounds with transition metal atoms are generally known to be susceptible to reactions with Li … We, therefore, filter out **most** compounds with d- and f-block elements."* ⛔ **"most" 의 규칙이 없다** — §10-5.

### 4c. 전기화학 창 축 — **Li grand-potential (우리와 같은 기계)** ★

논문 식 (4):

```
eφ = E − μ_Li · N_Li
```

> *"where, e is the elementary charge, φ is the electrode potential, E is the total energy computed using DFT, and N_Li is the number of Li atoms in the system."* (ref 66 Ong 2008 · ref 67 Aydinol/Ceder 1997)

⚠ **이 식은 그대로 읽으면 틀렸다.** 우변은 **Li grand potential Φ(μ_Li)** 이고(에너지 차원), 좌변 `eφ` 는 전극전위 × 전하다. 표준 계보는 두 식이 **따로** 있어야 한다 — `Φ = E − μ_Li N_Li` 와 `μ_Li(φ) = μ⁰_Li − eφ`(Li 금속 기준). **[Nolan21] Methods 식 (5)(6) 은 이 둘을 정확히 분리해 인쇄한다.** ⇒ **계보 안에서 전압축 정의는 #5(2021 ENSM)에서 가장 선명했고 #6(본 편)에서 오히려 흐려진다** — 우리가 원고에서 *"정의의 활자"* 로 가리킬 곳은 여전히 **[Nolan21] 식 (5)(6)** 이다(§7c).

**절차 (본문 + `Fig. S2`)**
1. 대상 화합물이 속한 화학계(예 Li–P–S)의 **Li 개방 상평형**을 μ_Li 를 훑으며 푼다.
2. 각 φ 에서 평형상 집합과 **f.u. 당 Li uptake** 를 얻는다 → **전압 프로파일**.
3. **창 = Li uptake 가 0 인 구간.** `Fig. S2` 캡션이 이것을 문장으로 적는다: *"the voltage range corresponding to zero Li uptake."*
   - **cathodic limit = 그 평탄구간의 아랫변** (그 아래로는 Li 를 먹는다 = 환원)
   - **anodic limit = 윗변** (그 위로는 Li 를 뱉는다 = 산화)
4. **준안정 화합물**(`E_hull > 0`) 처리: *"the stability window is represented by the oxidation and reduction potentials of their decomposition components in the grand potential phase diagram."* ⇒ **자기 자신이 아니라 분해산물의 창**을 쓴다. (§3a 에서 I 계 5종의 창이 전부 2.35 로 같은 이유.)
5. **범위**: 조성당 **최저에너지 상 하나만** → 15,446 중 **8,924 종**만 창을 갖는다.

> 🔑 **계보 6편 중 cathodic limit 의 조작적 정의를 *그림으로* 보여 주는 첫 편이자 유일한 편**이다. [Nolan19] 는 boxplot 만, [Nolan21] 은 식과 XLSX 열만 있었다. `Fig. S2` 는 **계단 하나하나의 산물까지** 적는다 → §7c.

### 4d. 스크리닝 게이트 (두 갈래) ★

| | **고체전해질(SE) 후보** | **Li 금속 음극 코팅 후보** |
|---|---|---|
| 이온이동 | **3D 장벽 ≤ 0.5 eV** (*"arbitrary cutoff"* — 본문 표현) | **3D 장벽 ≤ 1 eV** (*"Because coatings are generally applied as thin-films, they allow for a comparatively low ionic conductivity"*) |
| Li 금속 안정성 | — | **환원전위(vs Li/Li⁺) = 0 V** ← **불리언** |
| 창 | — | **> 1 V** (본문) / **≥ 1 V** (`Table S1` 캡션) ⚠ 미세 불일치 |
| 열역학 | `E_hull ≤ 30 meV/atom` | 같음 |
| 전자전도 | `E_g ≥ 1 eV` | 같음 |
| 원소 | *"filter out **most** compounds with d- and f-block elements"* ⛔ 규칙 없음 | 같음 |
| 결과 | **> 250 종** (목록 미공개) | **26 종** (`Table S1` 전수) |

### 4e. ML — 모델·특징·평가 ★

- **알고리즘**: scikit-learn **Gradient Boosting**(주) + **Random Forest**(비교). *"Ensemble methods combine predictions from several base estimators to reduce bias and variance"*. 특징 스케일링 불필요, 소·중규모 혼합형 데이터에 적합하다는 이유를 명시.
- **하이퍼파라미터**: 격자탐색 + **10-fold CV**.
- **성능 보고**: **20회 랜덤 90:10 분할 평균**, **held-out test set 만**.
- **표적 3개 = 독립 모델 3개**: ⓐ 3D 장벽(구조특징 22), ⓑ 환원전위(조성특징 28), ⓒ 산화전위(같은 28).
- **이상치 처리**: 장벽 모델은 **≤ 5 eV** 만 학습.
- **장벽 특징 22개** (`Table 1` / SI §S1): `Li`(Li 원자분율) · `LNC`·`LLB`·`SNC`(4 Å 이웃수 3종) · `SBI`(부격자 결합 이온성) · `ENS`(부격자 평균 전기음성도) · `LLSD`·`LASD`·`AASD`(최근접거리 3종) · `NDV`(Voronoi 면적가중 결합길이 표준편차) · `OP_1..3`(Warren–Cowley 유사 정렬도 1–3 껍질) · **`DLFS`**(최대 자유구 지름, **Zeo++**) · `SLPW`(직선경로 원기둥 반경) · **`SPF`**(부격자 충전율 = 비-Li 원자 부피 / 셀 부피) · `MPE`(최대 충전효율) · **`XRD_1..5`**(pymatgen 분말 XRD 패턴의 PCA 주성분 5개; 5개 합쳐 분산의 **0.65** 설명). 출처: Sendek 2017(ref 59) 9개 + Ward 2017(ref 83) 5개 + 신설/도구 8개.
- **전위 특징 28개** (`Table 2`): 조성가중 원소물성 **8종**(원자번호·전기음성도·원자가 d 전자·미충전 d 전자·미충전 p 전자·밴드갭·자기모멘트·녹는점) × **3통계**(평균·최대·범위) = 24, **+ 신설 산화상태 특징 4개**:
  - `oxid.state − min.oxid.state (X) = Σ_i |V_i^X − min{V_i}|` (더 환원될 여지)
  - `max.oxid.state − oxid.state (X) = Σ_i |max{V_i} − V_i^X|` (더 산화될 여지)
  - 위 둘에 각각 **Pauling 전기음성도를 곱한** 2개.
  🔑 **이 4개가 이 논문의 진짜 발명이다** — 화학자가 손으로 하는 *"이 원소가 더 산화될 수 있나"* 판단을 숫자로 만든 것이고, `Fig. 4` 에서 전기음성도 다음가는 2위(산화 0.203)로 올라온다.
- **해석 도구 2종**:
  - **SHAP**(ref 85 Lundberg & Lee 2017, `shap` 패키지) — **개별 예측**을 base value(1.490 eV)에서 출발해 특징별 기여로 분해. 훈련·시험 데이터 모두에 보고.
  - **PFI**(ref 79 Breiman, `rfpimp` 패키지) — 특징 벡터를 무작위 치환했을 때 **R² 하락폭**. **시험셋에서만** 측정.
  - **불순도 기반 중요도를 명시적으로 거부**한다: *"they are always computed on the training set … strongly biased towards high cardinality features."* ✅ 이 판단은 옳고, 우리 cascade 감사에도 그대로 적용된다.
  - **상관 특징 문제도 인지**: 전위 모델은 같은 물성의 3통계가 서로 상관돼 있어 **클러스터링 후** PFI 를 잰다(`Fig. 4` 의 묶인 라벨이 그 결과).

---

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1** | 스크리닝 통과 후보 **43개 마커**를 `x = 환원전위(V)` · `y = softBV 3D 장벽(eV)` 평면에 족(황화물 보라/산화물 초록/할라이드 분홍/기타 올리브)으로 표시. 캡션 게이트 `[3D ≤0.5 eV, E_hull ≤30 meV, E_g ≥1 eV]` | ★ **이 편의 좌표계 자체가 "음극 축"** — 양극 넷과의 차이를 한 장으로 보여 준다. 본 digest 가 **43개 좌표를 픽셀 복원**(§12b): `Li₆PS₅I`(1.722, 0.251) · `Li₃PS₄`(1.722, 0.308) · `Li₇P₃S₁₁`(2.279, 0.294) · **`Li₆PClO₅`(0.690, 0.467)** · `Li₃PO₄`(0.690, 0.375) · LLZO(0.050, 0.495). 우리 인접 물질의 **문헌 소환값 표**로 쓴다 |
| **2** | **SHAP** 워터폴 4장 (위→아래 `Li₉S₃N` 0.198 / `Li₂CO₃` 0.182 / `LiBF₄` 0.134 / `Sr₄Li(BN₂)₃` 0.127 eV). base value **1.490 eV** 공통. 빨강=예측을 올림, 파랑=내림 | "해석가능" 주장의 실체가 이것이다 — **개별 예측의 특징 기여 분해**. 우리 cascade 가 후보를 설명할 때 그대로 쓸 수 있는 양식. ⚠ `Sr₄Li(BN₂)₃` 패널에는 본문이 말하는 `Li = 0.071` 이 **표시돼 있지 않다**(§10-9) |
| **3** | **PFI**(3D 장벽 GB, 시험셋) 상위 10. **SPF 0.31** 압도적 1위, 이하 `Li` 0.134 · `XRD_1` 0.098 · `DLFS` 0.096 · `SNC` 0.093 · `ENS` 0.066 · `LNC`·`SBI`·`XRD_2`·`LLB` ≈0.05 | ★ **"Li 이동은 부격자가 얼마나 공간을 먹었나로 결정된다"** 는 한 장. 우리 BVSE 채널% 와 **같은 물리**를 다른 언어로 말한다 → §8-3 |
| **4** | **PFI** (a) 환원전위 · (b) 산화전위. (a) `E_neg` **0.52** 압도 → `Oxid.state*E_neg` 0.12 → `Valence d-elec` 0.11 → `Oxid.state` 0.095 … (b) `E_neg` **0.372** → **`Oxid.state` 0.203** → `Oxid.state*E_neg` 0.125 → `Unfilled p-elec` 0.053 → `Band gap` 0.048 | ★ **산화축에서 "산화상태 여유" 특징이 2위로 올라온다**(환원축에서는 4위) — 산화한계는 *"더 산화될 수 있나"*, 환원한계는 *"얼마나 전자를 당기나"* 라는 **비대칭**이 데이터에서 나온다. 우리 4축 서술(axis ①: S²⁻ 가 pin) 과 같은 방향 |
| **S2** | **`Li₃PS₄` 전압 프로파일** — `x = φ vs Li/Li⁺ (0–5 V)`, `y = f.u. 당 Li uptake`. 계단과 각 구간 산물이 활자로 붙어 있다 | 🔑🔑 **계보 6편 중 cathodic limit 을 그림으로 정의하는 유일한 자리.** 본 digest 픽셀 판독(§12a): 평탄구간 **1.702 – 2.360 V**(uptake 0), 그 아래 `Li₂S + P`(1.26–1.70, uptake 5) → `Li₂S + Li₃P`(0–0.87, uptake **8**), 그 위 **`LiS₄ + P₂S₇`**(2.36–3.78) → `P₂S₇ + S`(3.78–5.0). ⛔ 본문은 창을 **1.7–2.2 V** 라고 두 번 적는다 → §10-3. ⛔ 산화산물에 **우리가 phase set 에서 배제하는 `LiS₄`** 가 들어 있다 → §7f-③ |
| **S3** | 통과한 **황화물 23 마커**. 캡션: *"Apart from `Li₂S` and `Li₉S₃N`, all other sulfides have high reduction potentials and are thus unstable against Li metal"* | ★ **황화물은 음극 코팅이 못 된다**는 이 논문의 판정이 그림 한 장에 있다. `Li₃PS₄`·`Li₇P₃S₁₁`·`Li₄GeS₄` 전부 `V_red` 1.6–2.3 V. ⚠ 그런데 `Li₉S₃N` 은 `Table S1` 에 **없다**(§10-8) |
| **S4** | 통과한 **할라이드 36 마커** | ★ 우리 Cl 축. **`LiCl`·`LiBr`·`LiI` 가 한 점으로 겹쳐 그려져 있다**(0, ≈0.352) — 세 값이 0.349/0.350/0.352 로 사실상 같다. `Li₆PS₅I`(1.72, 0.251) 이 유일한 아지로다이트. ⚠ **`LiF` 가 여기서도 0.241** (`Table S1` 0.536 과 불일치) |
| **S5** | 통과한 **산화물 59 마커** (가장 큰 족) | ★ **`Li₆PClO₅`(= Li₆PO₅Cl, 산소 아지로다이트) 가 `V_red` 0.690 V** — 황화물 아지로다이트(1.722)보다 **1.03 V 낮다**. 우리 `LPSOCl(+O)` 방향의 **문헌 근거 1점**(⚠ 단일점·다른 조성) → §8-4. `Li₂SO₄`(1.55, 0.331)·`Li₃PO₄`(0.69, 0.377)·LLZO(0.05, 0.497)·`Li₂CO₃`+`LiAlB₂O₅`(≈1.29, 0.176) |
| **S6** | 통과한 **기타 19 마커**. 캡션: *"Nitrides have the lowest reduction potentials among other compounds"* | ⚠⚠ **이 논문 최대의 자기모순 자리.** `V_red = 0` 에 질화물이 **6종**(`Li₃YN₂` 0.465 · `Li₃ScN₂` 0.438 · `Li₃AlN₂` 0.415 · `Li₂SiN₂` 0.405 · `Li₃N` 0.284 · `Li₃BN₂` 0.267) 있는데 **`Table S1` 에는 하나도 없다** → §10-4 |
| **S8** | GB 예측 ↔ softBV 장벽 **parity**(0–5 eV). 저장벽 영역은 조밀, **2 eV 이상에서 ±1.5 eV 로 벌어진다** | ⚠ 캡션은 *"Good agreement … in the 0−1 eV range"* 라고 하지만, 우리가 본 바로는 **0–0.5 eV 구름이 y=x 보다 체계적으로 위**에 있다(SHAP `f(x)` 가 softBV 보다 늘 큰 것과 같은 방향: 0.198>0.185, 0.134>0.122, 0.127>0.109) ⇒ **저장벽 쪽 양의 편향**. 게이트가 0.5 eV 라서 **경계에서 위양성보다 위음성이 는다** |
| **S10** | 22특징 + `E^b` 의 **Pearson 상관 히트맵** (숫자 미인쇄, 색만) | ⚠ **PFI 1위 `SPF` 의 `E^b` 상관이 옅은 파랑(약한 양)** 에 그친다 — 색 어디에도 진한 칸이 없다(figure-read). 즉 **선형 상관은 약한데 트리 모델은 SPF 에 크게 기댄다** = 비선형·상호작용. 논문은 *"the same positive and negative correlations"* 라고만 하고 이 괴리를 언급하지 않는다 → §7d-4 |
| **S11** | 전위 parity (a) 환원 (b) 산화, 0–6 V, 밀도 색 | ⚠⚠ 좌하단 3.2× 확대에서 **`DFT = 0 V` 에 수직 띠**가 보인다 — 진짜 `V_red = 0`(= 코팅 판정의 전부)인 화합물들이 **최대 ≈0.8 V 까지 예측**된다. ⇒ **이 회귀 모델로는 코팅 스크리닝(불리언 0 V)을 재현할 수 없다** → §7d-5 |
| `Table S1` | 음극 코팅 후보 **26종** (mp id·장벽·창) | ★ 이 논문의 유일한 완전 데이터. §3a 에 전수 전사 + 본 digest 의 족·창 규칙 분석 |
| `Table 4` | Sendek 21종 ↔ softBV/ML 장벽 ↔ DFT-MD 판정 | ★ **폴리모프 민감도 2.1×** 의 근거(`LiCl` 0.349 vs 0.735) + ML 예측이 계산값과 같은 열에 섞이는 관행의 사례 |
| `Fig. S1`·`S7` | softBV 3D 경로 삽화 (`Li₃PS₄` / `Li₉S₃N`·`Li₁₀SiP₂S₁₂`·`LiAlB₂O₅`·`LiYO₂`) | ⛔ **안 봤다** — 정량 정보 없음 |
| `Fig. S9` | SHAP 3장 (`LiErSe₂`·`LiMgB₃(H₉N)₂`·`SrLi(BS₂)₃`) | ⛔ **안 봤다** — 본문이 여섯 특징 값을 전부 활자로 적는다(SPF 0.384/0.126/0.279, MPE 0.522, ENS 2.113/2.213, SNC 34.5/10.30, Li 0.04/0.09, LNC 11.0, DLFS 1.111) |

---

## 6. Post-processing ★

| 무엇 | 도구 | 어떻게 숫자·그림이 됐나 |
|---|---|---|
| **3D 이동장벽** | **softBV** (Chen/Wong/Adams 2019, ref 45) | BV 미스매치 등치면 → Morse force-field 로 eV 환산 → x/y/z 침투 최저 등치면 → **3D 장벽** 하나의 스칼라. 15,446종 전수 |
| **자유공간 기술자** | **Zeo++** (ref 84) | `DLFS` (최대 자유구 지름) — Voronoi 기반 공극 해석 |
| **Voronoi 기술자** | Ward 2017 구현(ref 83) | `NDV`·`OP_1..3`·`MPE` — 면적가중 정렬도 |
| **구조 지문** | **pymatgen** `XRDCalculator` + **PCA** | 분말 XRD 패턴 → 주성분 5개(`XRD_1..5`), 누적 분산 **0.65** |
| **전기화학 창** | **grand-potential 상평형** (Ong 2008 방법; MP 에너지) | μ_Li 스캔 → Li uptake 프로파일(`Fig. S2`) → **uptake = 0 구간 = 창**. 조성당 최저에너지 상만 → 8,924종 |
| **회귀** | **scikit-learn** GB·RF | 격자탐색 + 10-fold CV → 20× 90:10 랜덤분할 → test R² 평균 |
| **개별 설명** | **`shap`** (ref 85) | 워터폴 플롯(`Fig. 2`·`S9`), base value 1.490 eV |
| **전역 중요도** | **`rfpimp`** (ref 86) | 시험셋 **R² 하락폭**(`Fig. 3`·`4`). 전위 모델은 상관 특징 **클러스터링 후** 측정 |
| **상관 진단** | (미기재, 아마 pandas/seaborn) | `Fig. S10` Pearson 히트맵 — **숫자 없이 색만** |

> ⛔ **없는 것**: NEB 0 · AIMD 0 · 계면 반응에너지 0 · 탄성 0 · 포논 0 · 전하분석 0 · 실험 0.
> ⛔ **불확실도 정량 없음**: 오차막대·신뢰구간·앙상블 분산이 **단 한 곳도 없다**. R² 는 20회 분할 평균인데 **표준편차를 안 적는다**.

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md`

### 7a. 양(quantity) 대조표 — **무엇이 같고 무엇이 다른가**

| 그들 양 | 정의 | 우리 대응 | 판정 |
|---|---|---|---|
| **3D barrier (eV)** | softBV 등치면 침투 활성화에너지, 0 K, 무완화, 단일 폴리모프 | `Ea` **comp1 0.253 / modelc 0.224 eV** (UMA-s-1p1 MLIP-MD, 600/800/1000 K 아레니우스, MSD 2–50 ps) | 🔴 **다른 양.** 그들은 정적·경험적 경로에너지, 우리는 유한온도 동역학. 논문 자신이 σ 환산을 금지. **순위 비교조차 조심** — 폴리모프로 2.1× 흔들린다(§12c) |
| **3D barrier (채널 개념)** | BV 미스매치 낮은 영역의 3방향 침투 | 우리 **BVSE 채널 %** (`tools/comp1_v3/`, above-min ≤ iso) | 🟡 **같은 계열 도구·다른 출력.** 우리는 % 로, 그들은 eV 로 낸다. **환산은 하지 않는다** — 우리 규율(정량·순위는 원본 주기셀 값만) 유지 |
| **Reduction potential (vs Li/Li⁺)** | Li uptake = 0 평탄구간의 **아랫변** (`Fig. S2`) | `reduction_limit_V` **1.242 V** ↔ `ocv_self_decomposition_V` **1.717 V** | 🟡 **같은 기계, 그러나 우리 어느 필드인지가 미확정** → §7c. **증거는 1.717 쪽** |
| **Oxidation potential (vs Li/Li⁺)** | 같은 평탄구간의 **윗변** | `oxidation_limit_V` **2.14 V**(LiS₄ 포함) / **2.256 V**(LiS₄ 제외, canonical) | 🟢 **같은 양·같은 기준·같은 DB(MP).** ⛔ 절대값 비교는 금지(다른 조성) — **정의 대조까지만** |
| **Electrochemical window (V)** | `V_ox − V_red`, 준안정이면 **분해산물의 창** | 우리는 창 폭을 헤드라인으로 안 쓴다(양끝을 쓴다) | 🟡 그들 정의가 **준안정 치환**을 포함한다는 점을 명시하지 않으면 비교 불가 |
| **`E_hull` ≤ 30 meV** | MP 조회 | 우리는 무질서 배열을 직접 만든다(SQS/enumerate 계열) | 🔴 **이 게이트가 우리 계를 자른다** — §7e |
| **`E_g` ≥ 1 eV** | MP 조회 | comp1 **2.066** / modelc **2.099** eV (fixed-occ nscf VBM/CBM) | 🟢 **게이트로만 쓰면 정합** (우리 둘 다 통과). ⛔ **절대 gap 비교 금지** — 우리 규율대로 *"wide-gap"* 수준까지만. ⚠ modelc 2.099 는 레지스트리 `method_integrity_flag` = *"방법 불일치 의심"* 이므로 문헌 옆에 나란히 놓을 때 그 단서를 밝힌다 |
| **`E_d` / pseudo-binary 계면 반응에너지** | — | `interface_reactivity` **−0.3227 eV/atom** (comp1 vs LiCoO₂) | ⛔ **이 논문에 없다.** 계보 #3·#4·#5 가 가진 양을 #6 은 버렸다 |

### 7b. ★ 음극 코팅 — 양극 넷과 무엇이 뒤집히는가 (1저자 물음 #1)

**뒤집히는 것 3가지**

1. **좌표축이 바뀐다.** [Nolan19]·[Nolan21] 의 헤드라인 축은 `E_d`(eV/atom), [Aykol16] 은 `E_d`(V, 리튬화 개시)·`E_c`(용출), [Xiao19] 는 `V_ox ≥ 4.0 V`. **본 편은 스크리닝 그림 5장 전부가 `x = Reduction potential`** 이다. 산화한계는 *"창 ≥ 1 V"* 로 **강등**된다 — 고전압 양극이 없으니 지켜야 할 상한이 없다.
2. **판정이 문턱에서 불리언으로 되돌아간다.** [Nolan21] 이 `E_d = 0` → `|E_d| < 0.05 eV/atom` 으로 **완화**했던 흐름과 반대로, 본 편은 **`V_red = 0 V` 정확히** 를 요구한다. `Fig. 1` 픽셀에서 LLZO 가 **0.050 V** 라서 코팅 목록에서 빠지는 것이 그 엄격함의 실증이다(§12b).
3. **실패 모드의 화학이 바뀐다.** 양극 쪽 넷의 적은 *산화·산소 방출·TM 환원*이었다. 여기서 적은 **Li 금속의 환원력**이고, 산물은 `Li₂S`·`Li₃P`·`LiCl` 처럼 **우리 SEI 목록과 같은 것들**이다(`Fig. S2`).

**그런데 뒤집히지 *않는* 것, 그리고 오히려 후퇴한 것**

4. ⛔ **우리 1.242 V 가 주역이 되지는 않는다.** 그들의 "환원전위" 는 §4c 정의상 **Li uptake 0 평탄구간의 아랫변**이고, 우리 쪽에서 그 자리에 있는 값은 **1.717 V**(§7c). 1.242 V 는 다른 브레이크포인트다.
5. ⛔ **계면이 사라졌다.** 본문은 *"For protective coatings on the anode, stability against Li metal on one side, and **the electrolyte on the other**, is more important"* 라고 코팅의 요건을 **양면**으로 선언해 놓고, **전해질 쪽 면은 한 번도 계산하지 않는다.** 코팅↔SE 반응에너지도, 코팅↔Li 반응에너지(`E_d`)도 없다 — Li 쪽조차 *"자기 창의 아랫변이 0인가"* 라는 **단독 물성**으로 대신한다. ⇒ **계보가 #3→#5 에서 쌓아 올린 계면 열역학이 #6 에서 통째로 빠진다.** 이것이 이 편의 가장 큰 구조적 약점이고, 우리가 이 편을 *"코팅 선정 방법"* 으로 인용할 수 없는 이유다.
6. ⛔ **산물 물리상태 게이트는 여기서도 복원되지 않는다**([Aykol14] 이후 6편 연속). `Fig. S2` 는 Li–P–S 계라 기체가 안 나오지만, 15,446종 중 산화물·질화물의 grand-potential 산물에는 `O₂`·`N₂` 가 고체와 같은 자격으로 들어갔을 것이고 **논문은 물리상태를 한 번도 언급하지 않는다**. 게다가 본 편은 **`LiS₄`** 라는, 우리가 명시적으로 배제하는 MP 상까지 산물로 인쇄한다(§7f-③).

### 7c. ★ cathodic limit 의 정의 — **우리 두 필드 중 어느 것인가** (미해결 digest Q3 에 증거 1건)

`comparison_vs_ours.md` 축 B 에 **미해결로 걸려 있던 물음**: 우리 `reduction_limit_V` **1.242 V** 와 `ocv_self_decomposition_V` **1.717 V** 중 문헌의 *"cathodic limit"* 과 같은 양은 어느 쪽인가. ([Zhu15] 1.71 · [Wang26IF] 1.78 · [Gil-González K_eff=0] 1.70 이 모두 **1.7 자리**에 있었다.)

**본 편이 더하는 것 — 정의(그림)와 수치(픽셀) 둘 다:**

| 근거 | 값 | 성격 |
|---|---|---|
| `Fig. S2` 캡션·본문 | *"the voltage range corresponding to zero Li uptake"* | ★ **정의가 그림으로 확정**된다 — cathodic limit = **Li uptake 0 평탄구간의 아랫변** |
| `Fig. S2` 픽셀 (본 digest) | `Li₃PS₄` 아랫변 **1.702 V** | figure-read ≈, ±0.02 V |
| `Fig. 1` 픽셀 (본 digest) | `Li₃PS₄` `V_red` **1.722 V** | figure-read ≈ (같은 값의 다른 그림, 0.02 V 일치) |
| `Fig. 1`·`S4` 픽셀 | **`Li₆PS₅I` `V_red` 1.722 V** ← **아지로다이트** | figure-read ≈ |

⇒ **판정(잠정)**: 그들 정의로 잰 아지로다이트/티오인산염의 cathodic limit 은 **1.70–1.72 V** 자리다. 우리 `ocv_self_decomposition_V` = **1.717 V** 가 그 자리이고, `reduction_limit_V` = **1.242 V** 는 **그 양이 아니다**.
⚠ **아직 판정이 아니다**, 이유 셋: ① `Li₆PS₅I` ≠ `Li₆PS₅Cl`(할로겐이 다르다) ② MP hull 세대가 다르다 ③ **우리 코드에서 `reduction_limit_V` 가 어떤 브레이크포인트로 정의됐는지 아직 안 열어 봤다**. ⇒ **작업거리(추가 DFT 0)**: `tools/oxidation` 의 `get_element_profile` 출력에서 comp1 의 **Li uptake 프로파일 전체**를 찍어 `Fig. S2` 형식으로 그려 본다. 1.242 V 가 uptake 계단 어디에 해당하는지 한 눈에 갈린다.

**그리고 정의의 *활자*는 여전히 [Nolan21] 이다.** 본 편의 식 (4) 는 grand potential 과 전극전위를 한 줄에 뭉개 놓았고(§4c), `μ_Li = μ⁰_Li − eφ` 를 안 적는다. ⇒ **계보 판정 불변: 우리 2.256 V 의 직계 원전은 [Zhu15] → Mo/Ong/Ceder 2012 이고, 식의 활자는 [Nolan21] 식 (5)(6).** 본 편은 **그 정의의 *그림판*** 을 제공하는 편이다.

### 7d. ★ "Interpretable ML" 의 실체와 검증 여부 (1저자 물음 #2)

**1) 무엇을 해석하나 — 두 층뿐이다**
- **SHAP** = *이 화합물의 예측이 왜 평균(1.490 eV)에서 그만큼 내려갔나* 를 특징별 화살표로 분해. (`Fig. 2`·`S9`)
- **PFI** = *이 특징을 섞으면 시험 R² 가 얼마나 떨어지나*. (`Fig. 3`·`4`)
둘 다 **모델에 대한 설명**이지 **물질에 대한 설명이 아니다.** 논문도 그렇게 적는다: *"PFI and SHAP values are not intrinsic predictors of feature importance. They are model dependent."*

**2) 특징이 물리적으로 읽히긴 한다 (이 부분은 진짜 강점)**
`SPF`(부격자 충전율)·`DLFS`(최대 자유구)·`Li`(Li 분율)·`SNC`(부격자 이웃수)는 **물리적 의미가 자명한 스칼라**다. 그래서 `Fig. 3` 의 결론 — *"낮은 SPF 또는 큰 DLFS = 낮은 장벽"* — 은 **읽을 수 있는 문장**이 된다. Coulomb matrix(200차원)·XRD 패턴(128차원)을 쓴 비교군보다 **성능이 더 좋으면서 해석까지 된다**는 것이 논문의 핵심 주장이고, `Table 3`(0.86 vs 0.72/0.70)이 그 근거다. ✅ 이 주장 자체는 데이터가 뒷받침한다.

**3) ⛔ 그러나 인과 검증은 *두 건의 일화*뿐이고, 그 두 건도 절차가 깨져 있다**
본문의 유일한 인과 시험:
> *"We can test this by substituting Sn for Si in the structure … **By simply changing the SPF**, we find that the 3D barrier of LSnPO increases to 0.518 eV."*

- ⛔ **"SPF 만 바꿨다"** — Si→Sn 치환은 실제로 `SPF` 뿐 아니라 `ENS`·`SNC`·`AASD`·`MPE`·`XRD_1..5` 를 전부 바꾼다. 한 특징만 바꾼 벡터는 **물리적으로 존재할 수 없는 입력**이고, 그 위의 예측은 모델 내부 민감도이지 물질 예측이 아니다.
- ⛔ **두 번째 사례는 아예 모델 출력이 아니다**: `LSiPS = 0.457 eV` 는 `Fig. 1` 마커 **0.456**(figure-read)과 일치한다 ⇒ **softBV 계산값**이다. 즉 "시험" 두 건 중 하나는 모델 예측, 하나는 계산값인데 **본문이 구분하지 않는다.**
- ⛔ **n = 2, 통계 없음, 반례 탐색 없음.** 그리고 표적이 softBV 이므로, 설령 맞아도 *"모델이 softBV 를 잘 흉내 낸다"* 를 보일 뿐 **물리적 인과는 아니다.**
- ✅ 공정하게: 논문은 마지막에 **스스로 물러선다** — *"even though PFI analysis and Shapley explanations do not necessarily provide causality, they can still serve as a useful guide for designing new compounds."* ⇒ **주장의 크기는 정직하다. 검증이 없을 뿐이다.**

**4) ⚠ 자기 SI 에 약한 반증이 있다** — `Fig. S10` 의 Pearson 히트맵에서 **`SPF`–`E^b` 상관이 옅다**(진한 칸이 `E^b` 행 어디에도 없다, figure-read). PFI 0.31 로 압도적인 특징의 **선형 상관이 약하다**는 것은 *"SPF 가 곧 장벽"* 이 아니라 *"SPF 가 다른 특징들과의 상호작용 속에서 분기에 많이 쓰인다"* 는 뜻이다. 본문은 *"We observe the same positive and negative correlations"* 라고 **부호만** 확인하고 넘어간다.

**5) ⛔⛔ 그리고 가장 아픈 곳 — ML 이 정작 *이 논문의 스크리닝 작업*을 못 한다**
코팅 판정은 **`V_red = 0 V` 라는 불리언**이다. 그런데 훈련된 것은 **회귀**이고, `Fig. S11a` 를 3.2× 확대해 보면 **`DFT = 0` 축에 수직 띠**가 있다 — 진짜 0 V 인 화합물들이 **최대 ≈0.8 V 까지 예측**된다. 즉 *"DB 밖 물질로 검색을 넓힌다"* 는 ML 의 존재 이유를 **코팅 과제에서는 달성할 수 없다**. 논문은 **분류 성능(정밀도·재현율)을 한 번도 보고하지 않고**, 26종에 대한 재현 시험도 하지 않는다.
> 🔑 **우리 cascade 에 그대로 옮겨지는 교훈**: 게이트가 불리언이면 **회귀 R² 는 그 게이트의 성능을 보증하지 않는다.** 우리도 후보 선별 지표를 낼 때 **선별 과제 그 자체의 지표**(재현율/정밀도, 혹은 순위상관)를 따로 내야 한다.

### 7e. ★ 게이트가 Li 전도체를 배제하는가 (1저자 물음 #4)

**계보 안에서 이 편의 위치 — 세 번째 유형이다**

| 편 | 전도도 축 | 결과 |
|---|---|---|
| **[Aykol16]** | 없음. 대신 `−E_c > 3.5 V`(액체 용출) | **전도체를 잘랐다** — `Li₂ZrO₃`·`LiAlO₂` 탈락 |
| **[Nolan21]** | **아예 안 본다**. `Table S4` 가 스스로 `LiAlO₂ 10⁻¹⁵`·`γ-Li₃PO₄ 10⁻¹⁸` 를 싣고 방어는 *"nm 두께면 된다"* 한 줄 | **전도 절벽을 못 본다** |
| **[Honrao21]**(본 편) | **1차 게이트가 전도도다** (`≤0.5` / `≤1 eV`) | ✅ 위 두 함정을 **둘 다 피한다** — 계보 6편 중 유일 |

**⛔ 그런데 우리 계는 그래도 탈락한다. 잘라내는 칼이 둘이다.**

1. **`E_hull ≤ 30 meV/atom`** — 본문 명시: *"the argyrodite `Li₆PS₅I` is identified, but **`Li₆PS₅Br` and `Li₆PS₅Cl` are excluded due to their higher E_hull values**."* 그리고 LGPS 는 **32 meV** 로 탈락(`Li₁₀SiP₂S₁₂` 는 통과). ⇒ **`comp1`(Li₆PS₅Cl) 과 `modelc`(Li₅.₄PS₄.₄Cl₁.₆) 는 이 논문의 후보 목록에 없다.** 이유가 "나쁜 물질이라서" 가 아니라 **MP 에 올라간 *정렬* 구조의 hull 거리가 크기 때문**이다 — 아지로다이트는 본질적으로 **Cl/S 자리무질서 물질**이고, 정렬 근사는 hull 위로 올라간다. ⇒ **무질서 물질에 `E_hull` 문턱을 그대로 쓰면 그 물질군이 통째로 탈락한다.** ★ 이것이 [Nolan19]/[Nolan21] 의 *"우리 계가 목록에 없다"* 와 **원인이 다른, 세 번째 형태의 배제**다(그쪽은 목록 자체에 황화물이 0종이었고, 여기는 **목록에 있는데 게이트에서 잘린다**).
2. **`0.5 eV` softBV 문턱** — `Li₃YBr₆` 0.55 · `Li₃ScCl₆` 0.56 · `Li₃InCl₆` 0.59. **현대 할라이드 SE 3종이 전부 문턱 바로 위**에서 잘린다. 그런데 논문 자신이 *"softBV barriers tend to be overestimated"*(구조 완화를 못 하므로) 라고 적는다 ⇒ **완화·회전이 중요한 계일수록 체계적으로 불리한 프록시** 위에 임의 문턱(*"arbitrary cutoff"* — 본문 표현)을 얹은 것이다. `Li₃InCl₆` 는 **같은 논문의 `Table 4` 에서 DFT-MD 가 σ > 10⁻⁴ S/cm 라고 판정한 물질**이다 — **자기 데이터 안에 위음성이 인쇄돼 있다.**

⇒ **최종 답**: *"게이트가 Li 전도체를 배제하는가?"* → **아니다, 이 편은 전도체를 요구한다.** 그러나 **우리 계와 현대 할라이드 SE 는 배제된다** — 배제의 원인은 **전도도 기준이 아니라 ① 무질서를 못 담는 `E_hull` ② 완화를 못 담는 softBV 프록시**다. 원고에서 *"문헌 스크리닝이 우리 물질을 빠뜨린다"* 를 쓸 때 **이 두 원인을 이름으로 대는 것이 정확한 서술**이다.

### 7f. ⛔ 우리 db 절대값과 섞으면 안 되는 값 (1저자 물음 #5) — **7종**

| # | 값 | 왜 금지 |
|---|---|---|
| ① | **모든 3D 장벽**(`Table S1`·`Table 4`·`Fig. 1`·`S3`–`S6` 전부) | softBV 경험값. 논문 자신이 σ 환산 금지를 명시. 우리 `Ea`(MLIP-MD)·`D`·`σ` 와 **같은 표 금지**. 폴리모프로 **2.1× 변동**(§12c) |
| ② | `Table S1` 의 **창 폭(V)** | 그들 창은 `V_ox − V_red` 이고 **준안정이면 분해산물의 창으로 치환**된다(§4c-4). 우리는 양끝을 따로 쓴다 — 폭끼리 비교 불가 |
| ③ | `Fig. S2` 의 **`Li₃PS₄` 1.70–2.36 V** | ㉠ 조성이 다르다(우리는 LPSCl) ㉡ **그들 산화산물에 `LiS₄` 가 들어 있다** — 우리 canonical 2.256 V 는 **`LiS₄`·`SCl₃`·`Li₅PS₄Cl₂` 를 제외한 GG phase set** 값이다(포함 시 2.14). **phase set 이 다른 두 숫자를 나란히 놓으면 안 된다** |
| ④ | **ML 예측 장벽** — `Table 4` 의 `d` 표시 5종(0.972·1.720·1.727·2.330·4.698)과 `Fig. 2`·`S9` 의 `f(x)` | 모델 출력이지 계산값이 아니다. 논문이 **같은 열에 섞어 놓았으므로** 우리가 인용할 때 반드시 분리 표기 |
| ⑤ | `Table 3`·`Table 5` 의 **R²** | 자기 DB 내부 **랜덤 90:10** 분할. 우리 cascade 는 **LODO**(leave-one-dopant-out) 규약이고 [Tu27ML] R²=0.99 ↔ 우리 −0.18 선례가 이미 있다. **같은 표에 올리면 규약 혼동** |
| ⑥ | **`E_hull`·`E_g`** | MP 조회값, **세대 미기재**. 특히 `E_g` 는 그들도 문턱으로만 쓴다 — 우리 canonical gap(comp1 2.066 / modelc 2.099)과 **절대 비교 금지** |
| ⑦ | `Table 4` 의 **DFT-MD σ 판정** | ref 60(Sendek 2018)의 **2차 인용**. 원전을 안 읽은 상태로 우리 db 에 들이지 않는다 |

> ✅ **반대로, 섞어도 되는 것**: `Fig. 1`·`S3`–`S6` 의 **환원전위 좌표**(같은 grand-potential·같은 MP·같은 기준) — 단 **정의 대조·방향 서술까지만**, 절대값은 **문헌 소환값 표**에 따로 둔다(§12b).

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

1. **★ `reduction_limit_V` 정의 감사 (추가 계산 0).** `Fig. S2` 가 cathodic limit 을 *"Li uptake 0 평탄구간의 아랫변"* 으로 그림 정의했다. 우리 `tools/oxidation` 으로 comp1 의 **Li uptake 프로파일 전체**를 `Fig. S2` 형식으로 그려, 1.242 V 와 1.717 V 가 그 계단의 어디인지 확정한다. → §7c. (`comparison_vs_ours.md` 축 B 의 **digest Q3** 를 닫을 수 있는 첫 실행 가능 작업)
2. **★ 우리 계 배제 원인을 이름으로 대는 문장을 확보했다.** *"문헌 HT 스크리닝은 `Li₆PS₅Cl` 을 `E_hull` 문턱에서, 할라이드 SE 를 softBV 문턱에서 잃는다"* — 본문 인용 가능(§7e). 우리 원고에서 *"왜 우리가 직접 계산해야 하는가"* 의 **문헌 근거**가 된다.
3. **cascade 기술자 후보 4개 (추가 계산 0~1).** `SPF`(부격자 충전율)·`DLFS`(Zeo++ 최대 자유구)·`Li` 분율·`SNC`. 우리 BVSE 채널% 와 **같은 물리를 다른 축으로** 재는 스칼라라, cascade predictor 의 **구조 기술자 열**로 바로 붙는다. ⚠ 단, 우리 계는 무질서라 **배열 평균**이 필요하다(그들은 단일 폴리모프).
4. **`Li₆PClO₅`(= Li₆PO₅Cl) 좌표 1점 확보.** `V_red` **0.690 V**(figure-read) vs 황화물 아지로다이트 **1.722 V** ⇒ **O 치환이 cathodic limit 을 ~1 V 내린다**는 방향. 우리 `LPSOCl(+O)` 계(canonical gap 2.2309 eV)의 **음극쪽 이점**에 대한 문헌 단서. ⚠ **단일점·다른 조성(전 O 치환)** — 방향만, 값은 못 옮긴다.
5. **불리언 게이트에는 불리언 지표를 (즉시 적용).** §7d-5 의 교훈. 우리 cascade 가 후보를 "통과/탈락" 으로 거를 때 **회귀 R² 를 성능 근거로 쓰지 않는다** — 선별 재현율/정밀도를 따로 낸다. (`kb/` 의 CV 규약 카드에 붙일 항목)
6. **`Li₂S` 창 2.13 V 라는 문헌 소환값** — 우리 산화 onset 이 **S²⁻-limited** 라는 서술의 **외부 보강 1점**. ⚠ `Table S1` 기준 `Li₂S` 는 0–2.13 V 이고, 우리 comp1 onset 2.256 V 가 그 근방이다. **같은 표 금지, 서술 보강만**(우리 축 ①).
7. **폴리모프 민감도 2.1× 를 방법 한계로 인용.** `LiCl` 0.349(mp-1185319) ↔ 0.735(mp-22905). BV 계열 지표를 우리가 쓸 때 **구조 출처를 반드시 박는다**는 규율의 문헌 근거.

---

## 9. 인용 가능 문장 (deck/paper용)

- *"High-throughput screening of 15,446 Li-containing compounds in the Materials Project — combining softBV migration barriers, grand-potential electrochemical windows, `E_hull` and band gap — yields 26 candidate coatings for the Li-metal anode, of which 15 are halides and only 2 are nitrides [Honrao 2021]."*
- *"In that screen, the argyrodite `Li₆PS₅I` passes, while **`Li₆PS₅Cl` and `Li₆PS₅Br` are excluded by the `E_hull ≤ 30 meV/atom` gate**, and `Li₃InCl₆`/`Li₃YBr₆`/`Li₃ScCl₆` fall just above the 0.5 eV softBV cutoff [Honrao 2021] — i.e. the two families most relevant to modern solid electrolytes are lost to a metastability threshold and to an empirical barrier proxy that the authors themselves note 'tends to be overestimated' because it omits structural relaxation."*
- *"`Li₃PS₄` is reported stable only between ~1.7 V and ~2.2–2.4 V vs Li/Li⁺, reducing to `Li₂S + P` and finally `Li₂S + Li₃P` at low potential [Honrao 2021, `Fig. S2`]"* — ⚠ **본문 2.2 / 그림 2.36 의 불일치를 반드시 함께 표기**하거나 *"~2.2–2.4 V"* 로 묶어 쓴다.
- *"Gradient-boosted regression on 22 physically interpretable structural descriptors reaches R² = 0.86 for softBV 3D migration barriers, outperforming 200-dimensional Coulomb-matrix (0.72) and 128-bin XRD (0.70) representations [Honrao 2021]."*
- *"Permutation-feature-importance analysis identifies the sublattice packing fraction as the single dominant descriptor of Li⁺ migration barriers (ΔR² ≈ 0.31), followed by Li fraction, largest-free-sphere diameter and sublattice neighbour count [Honrao 2021, `Fig. 3`]."*
- ⛔ **쓰면 안 되는 문장**: *"Honrao 2021 이 코팅 후보를 계면 안정성으로 골랐다"* — **계면 계산이 없다.** *"ML 이 스크리닝을 대체했다"* — **분류 성능 보고가 없다.**

---

## 10. 주의/한계 (over-claim 방지) — **본문↔그림/데이터 어긋남 12건**

> ⚠ 인용에 **실제로 걸리는** 것은 ①②③④ 넷이다. 나머지는 방법 신뢰도 평가에 쓴다.

1. ⚠⚠ **초록 ↔ `Table 5` R² 가 뒤집혀 있다.** 초록 *"0.95 and 0.92 on the **oxidation and reduction**"* ↔ `Table 5` **환원 0.95 / 산화 0.92**. `Fig. S11` 두 parity 로는 구분 불가. **축을 지정해 인용하면 50 % 확률로 틀린다.**
2. ⚠⚠ **`LiF` 3D 장벽이 그림 2장과 표 1개에서 다르다.** `Fig. 1`·`Fig. S4` 픽셀 **0.241 eV** ↔ `Table S1` **0.536 eV**(mp-1185301). 게다가 두 그림의 캡션 게이트가 **≤ 0.5 eV** 이므로, `Table S1` 값이 맞다면 **`LiF` 는 그 그림들에 있으면 안 된다.** (같은 상황인 `LiCl` 은 본문이 폴리모프 차이를 **적어 두었는데**, `LiF` 는 아무 말이 없다.) ⇒ **`LiF` 장벽은 인용 금지.**
3. ⚠⚠ **`Li₃PS₄` 창의 윗변: 본문 2.2 V ↔ `Fig. S2` 픽셀 2.360 V** (0.16 V 차). 본문·SI 캡션 **두 곳 모두** 1.7–2.2 로 적혀 있어 오타로 보기 어렵다. 아랫변은 1.702(그림) ↔ 1.7(본문) 로 일치하므로 **윗변만 어긋난다.**
4. ⚠⚠ **질화물 서사와 결과가 반대다.** 서론이 ref 57(Zhu 2017)을 들어 *"nitrides have a significantly lower reduction potential … making them more suitable for anode coatings"* 라 하고 `Fig. S6` 캡션도 *"Nitrides have the lowest reduction potentials"* 라 하는데, **`Table S1` 26종 중 질화물은 `Sr₄Li(BN₂)₃`·`Li₂CN₂` 둘뿐**이고 `Fig. S6` 에서 `V_red = 0` 에 서 있는 질화물 **6종**(`Li₃N`·`Li₃BN₂`·`Li₃AlN₂`·`Li₂SiN₂`·`Li₃ScN₂`·`Li₃YN₂`)이 **전부 코팅 목록에 없다**. 원인은 *"창 ≥ 1 V"* 게이트일 것이 거의 확실하지만(질화물은 산화한계가 ~1 V) **논문이 한 줄도 설명하지 않는다.** ⇒ *"이 논문은 질화물 코팅을 지지한다"* 로 인용하면 **틀린다.**
5. ⚠ **정의 없는 원소 필터 (계보 반복 패턴).** *"we filter out **most** compounds with d- and f-block elements"* — 규칙 없음. 실제로는 **Ti·Sc·Zn·Y·Zr·Hf·Ta·La·Pr·Tb·Er·Bi 가 살아남는다**(`Li₈HfO₆`·`LiErO₂`·`Li₇La₃Hf₂O₁₂`·`Li₆Hf₂O₇` 는 `Table S1` 안에 있고, `Fig. S4` 에는 `Li₂Ta₂(OF₂)₃`·`Li₄ZrF₈`·`Li₂CaHfF₈`·`Cs₂LiPrI₆` 가 있다). ⇒ **깔때기를 재현할 수 없다.** [Aykol16] `Fig. 1`·[Nolan21] `Fig. 1` 과 **같은 종류의 숨은 필터**다.
6. ⚠⚠ **코팅의 요건을 양면으로 선언하고 한 면만 계산한다.** *"stability against Li metal on one side, and the electrolyte on the other"* → **전해질 쪽은 끝까지 계산되지 않는다.** 계면 반응에너지가 논문 전체에 **0건**이다.
7. ⚠ **"expanded results" 가 전부가 아니다.** 본문 *"over 250 promising solid electrolyte candidates … Supplementary Figs. S3–S6 show expanded results for each class"* ↔ 본 digest 의 마커 계수: S3 **23** + S4 **36** + S5 **59** + S6 **19** = **137개**(`LiCl,LiBr,LiI` 한 점 포함이라 실제 화합물은 139). ⇒ **>250 중 절반 남짓만 보인다.** 나머지 목록·15,446행 DB·특징 스크립트 전부 *"available upon request"* — **계보 6편 중 기계판독 데이터가 0본인 유일한 편**([Aykol16] CSV 2본, [Nolan19]·[Nolan21] XLSX).
8. ⚠ **`Li₉S₃N` 이 헤드라인 후보인데 코팅 목록에 없다.** 초록·요약이 신규 후보로 앞세우고 `Fig. S3` 캡션이 *"황화물 중 Li 금속에 안정한 둘 중 하나"* 라 하는데, `Fig. 1` 픽셀로 `V_red` = **0.000 V**, 장벽 0.185 eV 로 **코팅 게이트를 다 만족하는 것처럼 보이는데 `Table S1` 26종에 없다.** (창 < 1 V 가 이유로 추정되나 미기재.) `Li₃BN₂`(0.001 V, 0.266 eV)도 같은 상황.
9. ⚠ **`Fig. 2` 넷째 패널과 본문 불일치(figure-read).** 본문은 `Sr₄Li(BN₂)₃` 에 대해 *"A small Li fraction = 0.071 … drives the prediction higher"* 라 하는데, **그 패널에 표시된 특징은 SPF·SNC·OP_1·NDV·XRD_3·LNC 뿐이고 `Li` 가 없다.** (0.071 = 1/14 로 **조성상으로는 맞는 값**이다 — 즉 값은 옳고 **그림의 근거가 없다**.)
10. ⚠ **식 (4) 가 grand potential 과 전극전위를 한 줄에 뭉갠다** (§4c). `μ_Li = μ⁰_Li − eφ` 가 없다. 또 식 (2) 는 **지수 기호가 조판에서 빠져** `S_ij = (R₀−R_ij)/b` 처럼 인쇄돼 있다(실제는 `exp[(R₀−R_ij)/b]`). ⇒ **이 논문에서 식을 그대로 베끼면 안 된다.**
11. ⚠ **`Table 4` 의 "all but one" 이 수사적이다.** DFT-MD 가 느리다고 한 11종 중 장벽이 낮은 것은 `SrLi(BS₂)₃`(0.340) **과 `LiCl`(0.735)** 둘인데, `LiCl` 은 *"already identified as a promising anode coating candidate"* 라는 서술로 넘어간다. 0.735 는 그들 **코팅 게이트(≤1 eV) 안**이다.
12. ⚠ **`Fig. 4b` 서술 미세 어긋남.** 본문 *"Other input features that have a noticeable impact include the number of **valence d-electrons** and unfilled p-electrons"* — 산화전위 패널에서 `Valence d-elec` 는 **7위(≈0.026)** 로 `Band gap`·`Melting Temp.` 보다 아래다. 환원 패널에서는 3위(0.11)라 맞다.

**그 밖의 구조적 한계 (어긋남은 아니지만 인용 범위를 좁힌다)**
- **불확실도가 한 곳도 없다** — R² 표준편차·장벽 오차·창 오차 전부 없음.
- **실험 검증 0** — *"Future work will involve … accurate DFT simulations and experiments to perform rigorous validation."* 즉 **DFT 검증조차 미래형**이다.
- **창은 8,924종에만 있다** — 15,446종 DB 라고 하지만 전기화학 축은 **58 %** 커버리지. 조성당 최저에너지 상 하나만.
- **온도·엔트로피 0 K** — `E_hull` 도 창도 0 K. 논문이 *"they may be stabilized at higher temperatures through entropic contributions"* 라고 인정.
- **MP 의존성 자백**: *"the grand potential phase diagram … is prone to change when new phases are discovered or get added to Materials Project"* ⇒ **우리 hull 세대차 논의와 같은 문제를 그들도 안다.**

---

## 11. 용어 미니사전 (이 편을 읽는 데 필요한 것만)

| 용어 | 뜻 | 우리 맥락 |
|---|---|---|
| **BV / softBV** | 본드밸런스. 결합가 합 = 형식 산화수여야 한다는 규칙. **softBV** 는 고차 배위껍질까지 써서 `R₀`·`b` 를 재피팅한 판 | 우리 `tools/comp1_v3/` BVSE 와 같은 계열. ⚠ 우리는 eV 환산을 **안 한다** |
| **3D 장벽** | 단위셀의 **세 방향 모두**로 침투하는 최저에너지 등치면의 활성화에너지. 1D ≤ 2D ≤ 3D | 이방성 전도체(LiFePO₄·LiCoO₂)는 1D/2D 가 훨씬 낮지만, 결함이 그 경로를 막으므로 3D 가 **보수적 지표** — 저자들의 논리 |
| **`SPF` (sublattice packing fraction)** | 비-Li 원자들의 부피 합 / 셀 부피 | 이 논문의 최강 기술자(PFI 0.31). *"부격자가 공간을 덜 먹을수록 Li 가 잘 움직인다"* |
| **`DLFS`** | 격자를 한 방향으로 통과할 수 있는 **최대 자유구 지름**(Zeo++) | 우리 BVSE 채널% 와 가장 가까운 개념 |
| **`ENS`** | 부격자 원자들의 Pauling 전기음성도 평균 | 높을수록 Li–음이온 결합이 이온성 → 장벽 낮음 (그들 해석) |
| **grand potential (Li 개방계)** | `Φ = E − μ_Li·N_Li`. μ_Li 를 외부 변수로 열어 두고 상평형을 푼다 | **우리 ESW 와 같은 기계.** μ_Li ↔ φ 변환은 `μ_Li = μ⁰_Li − eφ`(Li 금속 기준) — ⚠ **이 논문은 그 식을 안 적는다** |
| **Li uptake** | 주어진 φ 에서 평형상들이 f.u. 당 흡수(+)/방출(−)하는 Li 수 | `Fig. S2` 의 y 축. **uptake = 0 인 φ 구간 = 전기화학 창** |
| **cathodic / anodic limit** | 그 평탄구간의 **아랫변 / 윗변** | 우리 `reduction_limit_V` / `oxidation_limit_V` 의 대응물 — **어느 필드인지가 §7c 의 쟁점** |
| **`E_hull`** | 볼록껍질 위 수직거리(eV/atom). 0 = 열역학 안정 | 게이트 30 meV. **우리 무질서 계가 여기서 잘린다** |
| **GB (gradient boosting)** | 잔차를 순차적으로 학습하는 얕은 결정트리 앙상블 | RF(배깅)와 달리 **부스팅**. 표 형식 데이터의 기본기 |
| **SHAP** | 게임이론 Shapley 값으로 **개별 예측**을 특징 기여로 분해. 기준선(base value) 대비 | `Fig. 2` 의 화살표 길이 = SHAP 값. base = 1.490 eV |
| **PFI** | 특징 벡터를 무작위로 섞었을 때의 **시험 점수 하락폭** | 불순도 기반 중요도와 달리 **시험셋**·**고카디널리티 편향 없음**. ⚠ 상관 특징이 있으면 서로 중요도를 깎아먹어 **클러스터링 필요** |
| **parity plot** | 예측 vs 참값 산점 + y=x | `Fig. S8`·`S11`. **잔차의 *구조*를 보는 도구** — R² 하나로는 안 보이는 `x=0` 수직 띠가 여기서 보인다 |

---

## 12. ★ 본 digest 의 독립 재분석 — **논문에 인쇄돼 있지 않은 것**

> 이 편은 **공개 기계판독 데이터가 0본**이라 [Nolan21] 때처럼 XLSX 를 재집계할 수 없다.
> 대신 **PNG 픽셀 캘리브레이션**으로 그림에서 수치를 복원했다. 아래 숫자는 **논문의 어느 표·본문에도 없다.**
> 방법: `litdb/figures/<slug>/*.png` → 축 프레임·눈금 픽셀 검출 → 선형 변환 → 마커/계단 좌표. 오차는 눈금 간격 대비 **≤ 0.5 %**.

### 12a. `Fig. S2` 의 상전이 전압 8개 — **본문은 두 개만 적는다**

| φ (V, figure-read ≈) | Li uptake 변화 | 구간 평형상 (그림 활자) |
|---|---|---|
| — | **8.01** | `Li₂S, Li₃P` (0 – 0.867) |
| **0.867** | 8 → 5.99 | (라벨 없음) |
| **0.926** | 5.99 → 5.41 | (라벨 없음) |
| **1.156** | 5.41 → 5.14 | (라벨 없음) |
| **1.262** | 5.14 → 5.01 | `Li₂S, P` (1.262 – 1.702) |
| **1.702** ★ | 5.01 → **0.00** | ← **cathodic limit** |
| — | **0.00** | **`Li₃PS₄`** (1.702 – 2.360) ← **전기화학 창** |
| **2.360** ★ | 0 → −2.88 | ← **anodic limit**; `LiS₄, P₂S₇` (2.360 – 3.775) |
| **3.775** | −2.88 → −3.01 | `P₂S₇, S` (3.775 – 5.0) |

**읽히는 것 3가지**
- **창 = 1.702 – 2.360 V (폭 0.658 V)**. 본문의 *"1.7−2.2 V"* 는 **윗변이 0.16 V 낮다**(§10-3).
- **환원이 4단계**(0.867 / 0.926 / 1.156 / 1.262)로 잘게 쪼개져 있다 — 본문은 *"Li₃PS₄ undergoes reduction and uptakes Li to form Li₂S and P"* 라고 **한 문장으로 뭉갠다**. 실제로는 `Li₂S+P` → … → `Li₂S+Li₃P` 로 **P 의 단계적 리튬화**(P → LiP → Li₃P)가 계단으로 보인다. ⇒ 우리 `oxidation_stability.json` 의 `reduction_identical` 주석(*"P⁵⁺ → P³⁻/P⁰ (Li₃PS₄ → P → LiP → Li₃P)"*)과 **정확히 같은 순서**다. ✅ **우리 환원 경로 서술의 외부 확인 1건.**
- **산화 첫 산물이 `LiS₄`** 다 — 우리가 Gil-González 2022 phase set 을 따라 **명시적으로 제외**하는 바로 그 MP 상. ⇒ *"phase set 선택이 anodic limit 을 바꾼다"* 는 우리 규율의 **문헌 실물 사례**(§7f-③).

### 12b. `Fig. 1` 마커 **43개 좌표 복원** — 우리 계 인접 물질만 발췌

> 축 눈금 픽셀(x: 0 V @136 px, 1 V @339 px, 3 V @747 px / y: 0.0 @582 px, 0.5 @37 px)로 캘리브레이션.

| 물질 | `V_red` (V) | 3D 장벽 (eV) | 족 | 우리와의 접점 |
|---|---|---|---|---|
| **`Li₆PS₅I`** | **1.722** | **0.251** | 할라이드 | ★ 유일하게 통과한 아지로다이트. `Li₆PS₅Cl`·`Br` 은 `E_hull` 로 탈락 |
| `Li₃PS₄` | **1.722** | 0.308 | 황화물 | `Fig. S2` 의 1.702 와 0.02 V 일치 |
| `Li₇P₃S₁₁` | 2.279 | 0.294 | 황화물 | |
| **`Li₆PClO₅`** (= Li₆PO₅Cl) | **0.690** | 0.467 | 산화물 | ★ **산소 아지로다이트 — 우리 LPSOCl 방향**. 황화물 대비 `V_red` 1.03 V 낮다 |
| `Li₃PO₄` | **0.690** | 0.375 | 산화물 | ★ [Nolan21] XLSX **0.69 V**·[Zhu15] **0.68 V** 와 **일치** → 독립 재현 |
| `Li₂SO₄` (`Fig. S5`) | ≈**1.55** | 0.331 | 산화물 | ★ [Nolan21] XLSX **1.57 V** 와 일치 → 독립 재현 |
| `Li₂S` (`Fig. S3`) | **0.000** | 0.262 | 황화물 | 창 2.13 V (`Table S1`) |
| `Li₉S₃N` | **0.000** | 0.185 | 황화물 | 헤드라인 후보인데 `Table S1` 에 없다(§10-8) |
| LLZO `Li₇La₃Zr₂O₁₂` | **0.050** | 0.495 | 산화물 | ★ **0 이 아니라서 코팅 목록에서 빠진다** — 불리언 게이트의 엄격함 실증 |
| `Li₇La₃Hf₂O₁₂` | 0.000 | 0.469 | 산화물 | `Table S1` #13 (0.470 과 일치) |
| `LiF` | 0.000 | **0.241** ⚠ | 할라이드 | `Table S1` 0.536 과 불일치(§10-2) |
| `Li₂Se` / `Li₃BN₂` / `Sr₄Li(BN₂)₃` | 0.001 / 0.001 / 0.001 | 0.327 / 0.266 / 0.109 | 기타 | `Table S1` 0.327 / — / 0.109 |
| `LiAlB₂O₅` + `Li₂CO₃` (겹침) | ≈1.29 | 0.176 | 산화물 | 본문 0.175 / SHAP 0.182 |
| `Li₁₀Si(PS₆)₂` (= LSiPS) | 1.706 | 0.456 | 황화물 | 본문의 치환 일화 값 **0.457 과 일치** → 그 값은 **softBV 계산값**이다(§7d-3) |

> ✅ **교차검증 3건이 전부 맞았다**: `Li₃PO₄` 0.690 ↔ [Nolan21] 0.69 ↔ [Zhu15] 0.68 · `Li₂SO₄` ≈1.55 ↔ [Nolan21] 1.57 · `Li₇La₃Hf₂O₁₂` 0.469 ↔ `Table S1` 0.470.
> ⇒ **서로 다른 논문·다른 구현·다른 hull 세대의 grand-potential 결과가 0.02 V 안에서 일치한다.** 이것은 **우리 2.256 V 가 "같은 기계에서 나온 값"** 이라는 주장에 대한 **세 번째 독립 보강**이다(⚠ 값을 옮겨오는 것은 여전히 금지, 기계의 재현성만).

### 12c. ★ **폴리모프 민감도 2.1×** — 논문이 오차로 취급하지 않는 것

| 조성 | mp id | 3D 장벽 (eV) | 출처 |
|---|---|---|---|
| **LiCl** | mp-1185319 (DFT 바닥상태) | **0.349** | `Table S1` #5, `Fig. S4` |
| **LiCl** | mp-22905 (Sendek 구조) | **0.735** | `Table 4` #8 |
| 비 | | **2.11×** | |

같은 조성·같은 도구·같은 논문인데 **구조 하나 바뀌면 2.1×**다. 그리고 **SE 게이트가 0.5 eV** 이므로 이 한 물질은 **구조 선택에 따라 통과/탈락이 갈린다**. 논문은 이것을 각주 한 줄로 처리한다.
⇒ **우리 규율에 직접 붙는다**: BV 계열 지표를 인용·산출할 때 **구조 출처(mp id / 배열)를 반드시 박는다.** 우리 BVSE 규율(*"정량·순위는 원본 주기셀 값만"*)이 왜 필요한지의 외부 실증.

### 12d. 스크리닝 그림의 마커 계수 — *"expanded results"* 의 실제 크기

| 그림 | 마커 수 | 비고 |
|---|---|---|
| `Fig. S3` 황화물 | **23** | |
| `Fig. S4` 할라이드 | **36** | `LiCl,LiBr,LiI` 한 점으로 겹침 → 화합물 38 |
| `Fig. S5` 산화물 | **59** | 가장 큰 족 |
| `Fig. S6` 기타 | **19** | 질화물·셀렌화물·보로하이드라이드 |
| **합계** | **137 (화합물 139)** | ↔ 본문 *"over 250"* ⇒ **표시된 것은 절반 남짓** |
| `Fig. 1` (본문) | **43** | 네 족 합본의 하이라이트 |

### 12e. `Table S1` 26종의 족·창 분포 — 논문이 안 세는 것

| 족 | 개수 | 창 범위 (V) | 장벽 범위 (eV) |
|---|---|---|---|
| 할라이드 | **15 (58 %)** | 2.35 – **6.36** | 0.349 – 0.882 |
| 산화물 | 6 | 2.90 – 3.22 | 0.354 – 0.845 |
| 질화물 | 2 | 1.39 · 2.12 | 0.109 · 0.982 |
| 칼코겐 (`Li₂O`·`Li₂S`·`Li₂Se`) | 3 | 1.89 – 2.90 | 0.259 – 0.327 |

- **창 최대 `LiF` 6.36 V / 최소 `Sr₄Li(BN₂)₃` 1.39 V.**
- **같은 할로겐이면 창이 같다**: Cl 계 3종 전부 **4.25**, I 계 5종 전부 **2.35**, Br 계 `LiBr`·`RbLiBr₂` **3.14** / `CsLi₂Br₃`·`CsLiBr₂` **2.96**. ⇒ §4c-4 의 **준안정 치환 규약**이 표면에 드러난 것. **창은 음이온이 정한다.**
- **장벽과 창이 상충한다**: 장벽 최저 4종(`Sr₄Li(BN₂)₃` 0.109 · `Li₂O` 0.259 · `Li₂S` 0.262 · `Li₂Se` 0.327)의 창은 1.39–2.90 인 반면, 창 최대 `LiF`(6.36)의 장벽은 **0.536 으로 SE 게이트 밖**이다. ⇒ **"통하면서 넓은" 코팅은 이 데이터에 없다** — 논문이 명시하지 않는 트레이드오프.

---

## 13. 한 줄 결론

**계보 #6 은 코팅 계산의 *직선적 후속*이 아니라 *분기*다** — 무대를 음극으로 옮기면서 계면 열역학(`E_d`)을 버리고 **전도도 프록시(softBV)를 1차 게이트로** 세웠고, 그 대가로 **우리 계(`Li₆PS₅Cl`)와 현대 할라이드 SE 를 `E_hull`·`0.5 eV` 두 문턱에서 잃는다**. 우리가 이 편에서 실제로 가져오는 것은 후보 목록이 아니라 **`Fig. S2` 의 cathodic-limit 그림 정의**(우리 `reduction_limit_V` 1.242 V 의 정체를 가를 실마리), **`Fig. 3` 의 SPF 우위**(cascade 기술자 후보), 그리고 **"불리언 게이트에 회귀 R² 는 증거가 아니다"** 라는 방법 규율이다.

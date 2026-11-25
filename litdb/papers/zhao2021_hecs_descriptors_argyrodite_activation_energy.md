# Machine learning prediction of activation energy in cubic Li-argyrodites with hierarchically encoding crystal structure-based (HECS) descriptors — Zhao et al. (Science Bulletin 2021)

> slug `zhao2021_hecs_descriptors_argyrodite_activation_energy` · DOI `10.1016/j.scib.2021.04.029` · type `ML (PLS) + BVSE — ⛔ DFT 0건` · PDF `5cc7c283-106._Machine_learning…HECS_descriptors.pdf` + SI `e0f1efc4-106._Sup_….docx` · digested `2026-09-09` · status ✅
> **저자**: Qian Zhao¹, Maxim Avdeev²·³, Liquan Chen¹·⁴, **Siqi Shi**¹·⁵\* (¹Materials Genome Institute, Shanghai Univ · ²ANSTO · ³Univ. of Sydney · ⁴IOP-CAS · ⁵SMSE Shanghai Univ) · 교신 `sqshi@shu.edu.cn`
> **서지 표지 대조 완료**: *Science Bulletin* **66** (2021) 1401–1408. 접수 2021-02-28 / 수정 2021-03-22 / 수락 2021-04-12 / 온라인 2021-04-23. © Science China Press + Elsevier, **All rights reserved (OA 아님)**. ⚠ 화면에 적혀 있던 "인용 126" 은 **오프라인이라 확인 못 했다** — 인용수는 쓰지 않는다.

> elements: Li, P, As, Si, Ge, Sn, S, Se, Cl, Br, I, B, Al, Ga, Sb
> methods: BVSE

---

## 0. 이 digest를 읽는 법 — 우리가 왜 이걸 먹었나

우리는 **Cl-rich argyrodite 도펀트 스크리닝 cascade** 를 재설계 중인데 **descriptor 를 하나도 안 정했다**. 이 논문은 "argyrodite Ea 예측 descriptor 집합" 의 **원전 후보 1순위**다 — argyrodite 전용으로 32개 descriptor 를 체계적으로 정의한 유일한 편이고, 우리 modelc 조성족(`Li₆₋ₓPS₅₋ₓCl₁₊ₓ`)을 **이름 그대로** 설계 추천 1번으로 뽑는다.

**결론부터 — 세 문장.**

> ① **descriptor 목록(32개 이름·정의·분류)은 가져올 만하다.** argyrodite 자리(4a/4b/4c/16e/48h)를 명시적으로 쓰는 유일한 공개 목록이고, 우리 O-자리 분석축과 1:1로 붙는다 (§9).
> ② **그런데 계산식이 하나도 없다.** 병목 크기 BN 도, 배위 엔트로피 Sconf 도, 이온반경 표도 정의가 없다 — **논문만 보고는 32개 중 어느 것도 우리 구조에서 재현할 수 없다** (§5, ★1).
> ③ **가장 중요한 건 타깃이다. 라벨 50개가 전부 BVSE 다** — 실험 0, DFT 0, AIMD 0, NEB 0. 그리고 **우리는 이미 BVSE 가 우리 조성축(comp1↔modelc)에서 순위를 뒤집는다는 것을 실측으로 갖고 있다** (`db/properties/bvse_bvlain_ev_4sys.json`). ⇒ 이 모델을 우리 Cl-rich 랭킹에 쓰면 **우리가 이미 틀린 줄 아는 답을 학습한 대리모델**을 쓰는 것이 된다 (§13).

그래서 이 digest 는 논문의 성과보다 **"descriptor 는 빌리고 라벨은 버린다"** 는 분리 판정에 무게를 둔다.

---

## 1. 한 줄 요약

입방 Li-argyrodite 50종의 **BVSE 활성화에너지**를 타깃으로, 단위셀(CIF)에서 뽑은 **32개 HECS descriptor**(조성/구조/전도경로/이온분포/특수이온 5범주 × global·local 2계층)를 **PLS 회귀**(4성분)에 넣어 R² 0.887(훈련)·0.820(시험, ⚠ §11-1 참조)·RMSE 0.02 eV 를 얻고, **VIP 점수**로 `r_anion` 이 1위임을 보인 뒤, "작은 음이온 치환 · 자리무질서 유도 · 협동전도 활성화" 세 전략과 6개 조성족을 제안한다.

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저널/년 | Science Bulletin **66**, 1401–1408 (2021) |
| DOI | `10.1016/j.scib.2021.04.029` |
| 유형 | **ML(PLS) + BVSE 라벨**. ⛔ **DFT·AIMD·NEB·MLIP·실험 전부 0건** |
| 조성계 | `Li⁺₍₇₋ₓ₊ᵧ₎ (M⁵⁺₍₁₋ᵧ₎N⁴⁺ᵧ Y(1)²⁻₄) Y(2)²⁻₍₂₋ₓ₎ X⁻ₓ` · Y = S, Se · X = Cl, Br, I · M = P, As · N = Si, Ge, Sn · 0 ≤ x ≤ 2, 0 ≤ y ≤ 1 |
| 데이터 크기 | **50종** (훈련 40 / 시험 10) |
| descriptor | **32개** (Table S2) |
| 소프트웨어 | **SPSE** 고속스크리닝 플랫폼(BVSE 계산, ref [28] He et al. *Sci Data* 2020, 7, 151; 웹 `https://matgen.nscc-gz.cn/solidElectrolyte/`) + **JMP**(PLS·VIP, SAS Institute 상용, ref [32,33]) |
| 계산자원 | Shanghai University HPC |
| 본문/SI | 본문 8 pp (Fig 1–7 + Table 1) · SI docx (Fig S1–S4 + Table S1–S2 + ref 1) |

---

## 3. 핵심 수치 총정리

### 3.1 모델 성능 (논문 인쇄값)

| 지표 | 훈련 (n=40) | 시험 (n=10) |
|---|---|---|
| R² | **0.887** | **0.820** |
| RMSE | **0.02 eV** | **0.02 eV** |

### 3.2 우리가 Table S1 원자료로 재계산한 값 (⭐ 논문과 어긋난다 — §11-1)

| 지표 | 훈련 | 시험 |
|---|---|---|
| R² = 1 − SSE/SST (**논문 Eq. (5) 정의 그대로**) | 0.8869 ✅ 일치 | **0.7661 ❌ 불일치** |
| Pearson r² | 0.8869 | **0.8203** ← 인쇄된 0.820 은 **이것**이다 |
| RMSE | 0.0241 eV | 0.0238 eV |
| 평균예측 기준선 RMSE (훈련평균으로 시험셋 예측) | — | 0.0531 eV |

⇒ 모델의 실제 이득은 **기준선 대비 오차 2.2배 감소**다.

### 3.3 교차검증 (Fig. S3 — 논문이 계산했지만 성능으로는 한 번도 안 쓴 값)

| 지표 | 값 |
|---|---|
| PRESS 최소 | **0.58415** (성분 4개) |
| **Q² 최대 (LOOCV)** | **0.65877** ← ⭐ 가장 방어 가능한 일반화 수치 |

### 3.4 라벨 자체의 성질 (Table S1 50행 전수 분석 — 논문이 언급 안 함)

| 항목 | 값 |
|---|---|
| Ea 범위 | 0.2441 – 0.5664 eV (폭 0.322 eV) |
| 평균 / 표준편차 | 0.3314 / 0.0689 eV |
| **라벨 양자화 격자** | **정확히 10/1024 = 0.009765625 eV** (50개 전부 이 격자 위, 예외 0) |
| 서로 다른 라벨 값 개수 | **18개** (50행이 18개 값을 공유) |
| 시험 RMSE / 격자 | 0.0238 / 0.00977 = **2.44 격자칸** |
| 훈련 y 범위·sd | 0.2539 – 0.5664 · 0.0725 |
| **시험 y 범위·sd** | **0.2441 – 0.3711 · 0.0519** ← 고-Ea 구간이 시험셋에 **없다** |

> 격자 10/1024 은 BVSE 에너지창을 1024 등분한 스캔의 흔적으로 보인다 (0–10 eV / 1024 = 0.009766 eV). **논문은 이 격자를 한 번도 안 밝힌다.** 라벨 분해능이 9.8 meV 인데 모델 RMSE 가 24 meV 라, 성능 논의는 "격자 2.4칸" 스케일에서 이뤄지고 있다.

### 3.5 설계 제안 6족 (Fig. 7 표 · 초록과 동일)

| 전략 | 조성족 | Ea 상한 |
|---|---|---|
| **작은 음이온 치환** | **`Li₆₋ₓPS₅₋ₓCl₁₊ₓ`** ← ⭐ **우리 modelc 족** | **< 0.322 eV** |
| | `Li₆₊ₓPS₅₊ₓBr₁₋ₓ` | < 0.273 eV |
| | `Li₆₊ₓPS₅₊ₓBr₀.₂₅I₀.₇₅₋ₓ` | < 0.352 eV |
| **양이온 치환** (N: Si, Ge, Sn; B, Al, Ga) | `Li₆₊₍₅₋ₙ₎ᵧP₁₋ᵧNᵧS₅I` | < 0.420 eV |
| | `Li₆₊₍₅₋ₙ₎ᵧAs₁₋ᵧNᵧS₅I` | < 0.371 eV |
| | `Li₆₊₍₅₋ₙ₎ᵧAs₁₋ᵧNᵧSe₅I` | < 0.450 eV |
| **협동 Li⁺ 전도 활성화** | — **예시 없음** | — |

> ⚠ **우리 추론(논문이 명시하지 않음)**: 6개 상한값이 **전부 Table S1 의 라벨 격자값과 정확히 일치**한다 (0.322265625 · 0.2734375 · 0.35156 · 0.419921875 · 0.37109375 · 0.44921875). ⇒ 이 "< X eV" 는 모델 예측이 아니라 **그 족의 모체(x=0 또는 y=0)의 BVSE 라벨**이고, 주장은 "치환하면 모체보다 내려간다" 는 **방향 주장**이다. **새 조성의 예측 Ea 는 논문 어디에도 숫자로 없다.**

---

## 4. 계산 방법 ★ — DFT 항목은 전부 "해당 없음"

우리 템플릿의 DFT 칸을 그대로 채우면 이렇게 된다. **빈칸이 정보다.**

- **code / version**: ⛔ **DFT 코드 없음**. BVSE = **SPSE 플랫폼**(ref [28]) 내장. ML = **JMP** (버전 미기재; ref [32] 은 "JMP 13 Multivariate Methods")
- **functional (+vdW)**: **n/a** — 전자구조 계산이 없다
- **pseudo / PAW**: **n/a**
- **k-points / ecut / supercell / nat**: **n/a**. 구조는 **단위셀(CIF) 한 장**씩
- **DFT+U**: **n/a**
- **AIMD**: **n/a**
- **MLIP**: **n/a**
- **무질서 처리**: ⭐ **SQS 도 enumerate 도 아니다.** 무질서를 **부분점유 CIF 그대로** 두고, 그 점유율을 descriptor 로 인코딩한다 — `OCC_Li-48h`, `OCC_Li-24g`, `OCC_Li`, `Sconf_Li`, `Sconf_A`, `Sconf_C`, `Sconf_anion`. 즉 **초격자를 만들지 않고 "무질서도" 라는 스칼라로 압축**한다. 이건 우리와 정반대 노선이다 (우리는 단일배열 또는 disorder ensemble 로 실제 배치를 만든다).
- **Ea 계산법 (=라벨 생성)**: **BVSE (Bond-Valence Site Energy)**, SPSE 내장. 본문 인용: *"To preserve the experimentally determined structure information and achieve high-efficiency calculation, Ea is uniformly calculated by the Bond-Valence Site Energy (BVSE) method embedded in the SPSE [28] **instead of density functional theory (DFT) method**."*
  ⚠ **BVSE 세부 파라미터 전무** — R₀ / b / soft-BV 판본 / voxel 해상도 / percolation 차원(1D·2D·3D 중 무엇인지) / 문턱 규칙 **전부 미기재**. 우리 규약(softBV Li–S 2.105 / Li–Cl 2.249 / b 0.37 / 0.25 Å voxel)과 같은지 **알 수 없다**.
- **ML**: **PLS(부분최소제곱) 회귀**, 성분 4개. 성분 수는 **LOOCV PRESS 최소 + Q² 최대**로 선택 (Fig. S3). 스케일링·표준화 여부 미기재. 난수 시드 미기재.
- **분할**: 훈련 80 % / 시험 20 % (40/10). **분할 방식(무작위? 층화? 조성족 기준?) 미기재**.

---

## 5. ★1 — HECS descriptor 32개 전수 + "계층적 인코딩" 의 정확한 뜻 + 재현 가능성 판정

### 5.1 "계층적 인코딩" 은 몇 층인가 (Fig. 1, Fig. 2b)

깊은 트리가 아니다. **공간 범위 2층 × 범주 5개**의 2차원 분류표다.

| 층 (Fig. 2b 가 셀 그림 위에 파란 박스 / 빨간 박스로 그린다) | 감싸는 것 | 범주 |
|---|---|---|
| **Global** (파란 박스 = 단위셀 전체) | 셀 전체 평균·격자 | ① Composition ② Structure |
| **Local** (빨간 박스 = 셀 안 한 케이지/경로 영역) | Li 케이지·경로·자유음이온 | ③ Conduction pathway ④ Ion distribution ⑤ Special ions |

즉 **"global 이 local 을 감싼다"** 가 전부다. 5범주 → 32개 스칼라로 전개된다.

### 5.2 argyrodite 자리 라벨 (본문 §2.1.2) — 이걸 먼저 고정해야 표가 읽힌다

| 라벨 | Wyckoff | 무엇 |
|---|---|---|
| **A** | **4a** | 음이온(X 또는 Y) — FCC 골격 자리 |
| **B** | **4b** | 중심 양이온 P⁵⁺/As⁵⁺ (또는 N⁴⁺) |
| **C** | **4c** (다른 공간군 setting 에서 4d) | **자유 음이온**(X 또는 Y) — 사면체 공동의 절반 |
| **E** | **16e** | `[BE₄]³⁻` 사면체를 이루는 음이온 (= PS₄ 의 S) |
| Li | **48h, 24g** | 나머지 사면체 공동에 무작위 분포 → **4c 자유음이온 둘레에 Li⁺ 케이지 형성** |

### 5.3 32개 전수 (Table S2 원문 + 우리의 재현 가능성 판정)

범례 — 재현: 🟢 우리 구조에서 지금 바로 계산 가능 / 🟡 규약을 우리가 정해야 함 / 🔴 논문 정의 없이는 불가

| # | descriptor | 논문 설명 (Table S2 원문) | 범주 | VIP `figure-read ≈` | 재현 |
|---|---|---|---|---|---|
| 1 | **r_anion** | Average ionic radius (r) for the anions | Composition | **1.50** ⭐1위 | 🟡 반경표 미기재 |
| 2 | EN_anion | Average Pauling electronegativity for the anions | Composition | 1.22 | 🟢 |
| 3 | PL_anion | Average ionic polarizability (PL) for the anions | Composition | 1.28 | 🟡 분극률표 미기재 |
| 4 | r_cation | Average ionic radius for the cations | Composition | 0.78 ⛔컷 | 🟡 |
| 5 | EN_cation | Average Pauling electronegativity for the cations | Composition | 0.98 | 🟢 |
| 6 | PL_cation | Average ionic polarizability for the cations | Composition | 0.71 ⛔컷 | 🟡 |
| 7 | C_Li | Lithium content | Composition | 0.72 ⛔컷 | 🟢 |
| 8 | **a** | lattice parameter | Structure | 1.29 | 🟢 |
| 9 | **v** | unit cell volume | Structure | 1.29 | 🟢 (⚠ `a` 와 r=1.00, §11-4) |
| 10 | V[LiACE₂]³⁻ | Volume (V) for Frank–Kasper polyhedral `[LiACE₂]³⁻` | Structure | 0.79 ⛔컷(칼끝) | 🔴 다면체 정의 없음 |
| 11 | **V[BE₄]³⁻** | Volume (V) for tetrahedra `[BE₄]³⁻` | Structure | 1.06 | 🟢 (PS₄ 사면체 부피) |
| 12 | D_Li-A | interatomic distance between Li and nearest neighboring ions on Wyckoff **4a** | Structure | 0.73 ⛔컷 | 🟡 "nearest" 집계규칙 미기재 |
| 13 | **D_Li-B** | 〃 on Wyckoff **4b** | Structure | **1.40** ⭐2위 | 🟡 |
| 14 | D_Li-C | 〃 on Wyckoff **4c** | Structure | 1.15 | 🟡 |
| 15 | **D_Li-E** | 〃 on Wyckoff **4d** ⚠ | Structure | **1.32** ⭐3위 | 🟡 ⚠ **본문은 E=16e** — SI 표기 오류 의심 (§11-5) |
| 16 | **BN_intra** | **bottleneck size (BN)** for the **intra-cage** pathway | Pathway | 1.10 | 🔴 **계산식 없음** |
| 17 | BN_doublet | BN for the **doublet** pathway | Pathway | 0.74 ⛔컷 | 🔴 |
| 18 | **BN_inter** | BN for the **inter-cage** pathway | Pathway | 1.01 | 🔴 **계산식 없음** |
| 19 | D_Li-Li intra | Li–최근접Li 거리, intra-cage 경로 | Pathway | 0.73 ⛔컷 | 🟡 |
| 20 | D_Li-Li doublet | 〃 doublet 경로 | Pathway | 0.60 ⛔컷(최저) | 🟡 |
| 21 | D_Li-Li inter | 〃 inter-cage 경로 | Pathway | 0.72 ⛔컷 | 🟡 |
| 22 | OCC_Li-48h | Lithium ion occupancy on Wyckoff **48h** | Ion distribution | 0.73 ⛔컷 | 🟢 |
| 23 | OCC_Li-24g | 〃 (원문 *"on Wyckoff 48h site, Wyckoff 24g site"* — **문장이 깨져 있다**) | Ion distribution | 0.64 ⛔컷 | 🟢 |
| 24 | OCC_Li | Lithium ion occupancy on **all** sites | Ion distribution | 0.60 ⛔컷(최저) | 🟢 |
| 25 | Sconf_Li | configurational entropy for the **mobile Li** | Ion distribution | 0.73 ⛔컷 | 🔴 **식 없음** |
| 26 | **Sconf_A** | Sconf for ions on **4a** | Ion distribution | 0.90 | 🔴 |
| 27 | **Sconf_C** | Sconf for ions on **4c/4d** | Ion distribution | 0.85 | 🔴 |
| 28 | **Sconf_anion** | Sconf for the **anions** | Ion distribution | 0.81 (컷 턱걸이) | 🔴 |
| 29 | **r_A** | Average ionic radius for ions on **4a** | Special ions | 0.99 | 🟡 |
| 30 | **EN_A** | Average Pauling EN for ions on **4a** | Special ions | 1.17 | 🟢 |
| 31 | **r_C** | Average ionic radius for ions on **4c/4d** | Special ions | **1.29** | 🟡 |
| 32 | **EN_C** | Average Pauling EN for ions on **4c/4d** | Special ions | 1.05 | 🟢 |

**범주별 개수**: Composition 7 · Structure 8 · Conduction pathway 6 · Ion distribution 7 · Special ions 4 = **32** ✅

### 5.4 ★1 직답 — "우리가 재현 가능한 수준인가?"

**입력**: **CIF 한 장**. 이완된 구조가 아니라 **실험 정련 구조(부분점유 포함)** 다 — 본문이 *"To preserve the experimentally determined structure information"* 이라고 명시한다. ⇒ 우리처럼 DFT-이완한 셀을 넣으면 **논문과 다른 축**의 값이 나온다.

**필요한 코드**: 논문은 안 밝힌다. 우리 손으로 하면 —
- 🟢 **13개** (EN·OCC·C_Li·a·v·V[BE₄]): `pymatgen` `Structure` + `SpacegroupAnalyzer` 로 즉시.
- 🟡 **11개** (반경/분극률 평균, D_Li-X 거리): 계산은 쉽지만 **표(어느 반경·어느 분극률)와 집계규칙(최근접 하나? 평균? 컷오프?)을 우리가 정해야** 한다 ⇒ **논문 값과 절대 비교 불가, 우리 내부 일관성만 가능**.
- 🔴 **8개** (BN×3, Sconf×4, V[LiACE₂]): **논문 정의 없이는 불가**. 특히 **BN 은 이 논문의 서사 전체(전략 ① "broaden bottleneck size")를 떠받치는 양인데 계산법이 없다.**

> **판정: ★1 은 "절반만 재현 가능"이다.** 이름과 분류 체계는 완전히 가져올 수 있지만, **VIP 상위 19개 중 6개(BN_intra·BN_inter·Sconf_A·Sconf_C·Sconf_anion·D_Li-E 의 자리 모호성)가 정의 부재 또는 표기 충돌**이다. 그대로 이식하면 우리 값과 논문 값이 왜 다른지 영원히 못 가린다.

---

## 6. ★2 — 어느 descriptor 가 중요했나, 무엇으로 쟀나, 함정은 있나

### 6.1 무엇으로 쟀나 — **VIP (Variable Importance in Projection)**

- **SHAP 아니다. permutation importance 아니다. 회귀계수도 아니다.** PLS 내부의 **가중치 기반** 지표다.
- 식 (본문 Eq. (2)): `VIPᵢ = sqrt( Σⱼ wᵢⱼ² · SSYⱼ · I / (SSY_total · J) )` — `w` 는 i번째 변수·j번째 성분의 가중치, `SSYⱼ` 는 j번째 성분이 설명한 y 제곱합, `I` = 변수 수(32), `J` = 성분 수(4).
- 컷오프 **0.8** — 본문이 *"the default cut-off value of the JMP software"* 라고 밝힌다. ⚠ **화학계량학 표준 관례는 VIP > 1** 이다 (VIP² 의 평균이 정확히 1이 되도록 정규화돼 있어서). §11-3 참조.
- 도구: **JMP** (SAS Institute, 상용).

### 6.2 중요도 순위 (Fig. 4 `figure-read ≈` — 논문 본문은 값을 인쇄하지 않는다)

**VIP > 0.8 인 19개** (본문이 범주별로 열거한 것과 우리 figure-read 가 **완전히 일치**한다):

| 순위 | descriptor | VIP ≈ | 범주 |
|---|---|---|---|
| 1 | **r_anion** | **1.50** | 조성 |
| 2 | **D_Li-B** | **1.40** | 구조 |
| 3 | **D_Li-E** | **1.32** | 구조 |
| 4 | a | 1.29 | 구조 |
| 4 | v | 1.29 | 구조 |
| 4 | **r_C** | 1.29 | 특수이온 |
| 7 | PL_anion | 1.28 | 조성 |
| 8 | EN_anion | 1.22 | 조성 |
| 9 | EN_A | 1.17 | 특수이온 |
| 10 | D_Li-C | 1.15 | 구조 |
| 11 | BN_intra | 1.10 | 경로 |
| 12 | V[BE₄] | 1.06 | 구조 |
| 13 | EN_C | 1.05 | 특수이온 |
| 14 | BN_inter | 1.01 | 경로 |
| — | ↑ 여기까지가 **VIP > 1** (14개) | | |
| 15 | r_A | 0.99 | 특수이온 |
| 16 | EN_cation | 0.98 | 조성 |
| 17 | **Sconf_A** | 0.90 | 이온분포 |
| 18 | **Sconf_C** | 0.85 | 이온분포 |
| 19 | **Sconf_anion** | 0.81 | 이온분포 |
| — | ↑ 여기까지가 **VIP > 0.8** (19개, 논문 기준) | | |

**탈락 13개**: V[LiACE₂] 0.79 · r_cation 0.78 · BN_doublet 0.74 · D_Li-A 0.73 · D_Li-Li intra 0.73 · OCC_Li-48h 0.73 · Sconf_Li 0.73 · C_Li 0.72 · D_Li-Li inter 0.72 · PL_cation 0.71 · OCC_Li-24g 0.64 · D_Li-Li doublet 0.60 · OCC_Li 0.60

### 6.3 ⭐ 이 순위표에서 진짜로 읽어야 할 것 — **Li 관련 descriptor 5개가 전부 바닥이다**

`C_Li` 0.72 · `OCC_Li-48h` 0.73 · `OCC_Li-24g` 0.64 · `OCC_Li` 0.60 · `Sconf_Li` 0.73 — **5개 전부 컷 아래**, 그중 둘이 32개 중 **최하위**다. 그리고 `D_Li-Li` 3종(intra/doublet/inter)도 전부 컷 아래. 즉 **Li 농도·Li 점유·Li–Li 거리 8개가 통째로 무의미하다고 나왔다.**

논문은 이걸 물리로 읽는다: *"lithium content has minor influence on Ea in the regime of uncorrelated ion conduction"*.

> ⛔ **우리 판정: 그건 물리가 아니라 라벨의 성질이다.**
> BVSE 는 **정지된 골격 위에 Li⁺ 탐침 하나**를 굴린다 — Li 부분점유는 골격 형식전하 균형으로만 들어가고, **자리 막힘·Li–Li 상관·협동 점프는 지도에 아예 없다**. 우리 `kb/concepts/bvse.md` §8 이 이걸 *"빈 격자 정적 프로브 — Li–Li 상관·협동 점프·vacancy 농도·프리팩터 전부 없음"* 이라고 못박아 놨다.
> ⇒ **Li descriptor 가 낮은 게 아니라, 선생(BVSE)이 Li 를 못 본다.** 학생(PLS)이 볼 수 있을 리 없다.
> 이건 자기부정적 결과다 — 논문 스스로 전략 ③("협동 Li⁺ 전도 활성화")을 내놓는데, **그 전략은 자기 모델이 원리적으로 못 보는 축**이라 Fig. 7 에서 **예시 조성 칸이 비어 있다**(§8 참조).

### 6.4 ★2 함정 점검 — **"특징이 타깃의 선형합성인가?"**

우리 선례(`kb/methodology/computational_methods_canonical.md`): `cascade v23 score` 를 그 점수를 만든 16개 특징으로 ridge 회귀했더니 LOOCV R² **0.9998** 이 나왔고, 그건 *"점수를 만든 특징들로 그 점수를 되맞춘"* **항등식 복원**이지 예측력이 아니었다.

**이 논문은 그 극단 사례는 아니다. 하지만 깨끗하지도 않다.** 세 층으로 갈라 본다.

| 층 | 판정 | 근거 |
|---|---|---|
| ① **엄밀한 항등식 복원인가** | ❌ **아니다** | 타깃 BVSE Ea 는 32개 descriptor 의 함수로 정의된 합성지표가 아니다. 독립적인 bond-valence 절차의 출력이다. 그렇다면 R² 가 ~1 이어야 하는데 **0.89/0.77 이고 Q² 는 0.66** 이다. |
| ② **그러나 같은 입력·같은 물리인가** | ⭕ **그렇다** | 라벨과 특징이 **같은 CIF + 같은 원자반경/원자가 표**에서 나온다. BVSE 장벽은 본질적으로 *"병목에서의 Li–음이온 거리와 음이온 종"* 의 함수이고, 특징에는 **BN_intra/BN_inter(병목 크기) · D_Li-A/B/C/E(Li–이온 거리) · r_anion/r_A/r_C(음이온 반경)** 가 그대로 들어 있다. ⇒ **독립 물리의 예측이 아니라, 해석적으로 거의 결정된 양의 선형 근사**다. |
| ③ **그래서 뭐가 문제인가** | ⭐ **비용 논거가 무너진다** | 이 모델의 존재 이유는 "BVSE 보다 싸다" 인데, **BVSE 는 이미 초 단위**다. 우리 실측(`bvse_bvlain_ev_4sys.json`, bvlain Morse-BVEL, 0.25 Å voxel): comp1 **7.4 s** · modelc **23.9 s** · lpsocl 22.6 s · b2o3 **58.8 s**. 반면 32개 descriptor 를 뽑으려면 병목 크기·Frank–Kasper 다면체 부피·자리별 Sconf 를 구현해야 한다 — **descriptor 만드는 비용이 라벨 만드는 비용보다 크다.** |

> **★2 종합**: 항등식 복원은 아니지만, **"싼 대리모델의 더 싼 대리모델"** 이다. R² 0.82 는 "물리를 예측했다" 가 아니라 **"해석적으로 결정된 양을 선형으로 33 % 잃으면서 근사했다"** 로 읽어야 한다. 우리 v23 선례의 보고 형식(*"성능이 아니라 해부로 보고한다"*)이 여기에도 그대로 적용된다 — **이 R² 는 성능이 아니라 "BVSE 장벽이 어떤 기하량들의 매끄러운 함수인가" 의 해부다.**

---

## 7. ★3 — 학습셋: Ea 가 몇 개이고 어디서 왔나

| 물음 | 답 |
|---|---|
| 몇 개인가 | **50개** (훈련 40 / 시험 10) |
| **어디서 왔나** | ⭐ **전부 BVSE 계산값이다.** 실험 0 · DFT 0 · AIMD 0 · NEB 0. 본문 §2.1.1 이 명시: *"Ea is uniformly calculated by the Bond-Valence Site Energy (BVSE) method embedded in the SPSE [28] **instead of density functional theory (DFT) method**"* |
| 어느 BVSE 인가 | SPSE 플랫폼 (He B, Chi S, Ye A, et al. *Sci Data* **2020**, 7, 151). 파라미터·차원·문턱 **전부 미기재** |
| 조성 범위 | `Li₍₇₋ₓ₊ᵧ₎(M₍₁₋ᵧ₎NᵧY(1)₄)Y(2)₍₂₋ₓ₎Xₓ` · **0 ≤ x ≤ 2** · 0 ≤ y ≤ 1 |
| 원소 팔레트 (Fig. 2a 주기율표) | Li(이동) · **Si, Ge**(N) · **P, As**(M) · **S, Se**(Y) · **Cl, Br, I**(X). ⚠ **Sn 은 본문 정의에 있으나 Fig. 2a 에서 색칠돼 있지 않다** — 실제 샘플링에 들어갔는지 불명 |
| **50개 조성이 무엇인가** | ⛔ **논문 어디에도 없다.** Table S1 은 `No. 1–40` / `No. 1–10` 인덱스와 Ea 3열뿐이고, Fig. 2a 는 (x, y) 격자가 아니라 **원소 팔레트**다. **조성-라벨 대응표가 존재하지 않는다.** |

### 7.1 ★3 핵심 — **우리 계(Cl-rich, x>1)가 범위 안인가 밖인가**

세 층으로 나눠 답한다. **답이 층마다 다르다.**

**① 명목 설계공간: ⭕ 안이다.**
그들의 마스터 식에서 `x` 를 halide 계수로 읽으면 `Li₍₇₋ₓ₎(PS₄)S₍₂₋ₓ₎Clₓ` 이고, `x = 1` → `Li₆PS₅Cl` = **comp1**, `x = 1.6` → `Li₅.₄PS₄.₄Cl₁.₆` = **modelc** 다. `0 ≤ x ≤ 2` 가 **modelc 를 정확히 포함**한다. 게다가 Fig. 7 의 설계 추천 1번 `Li₆₋ₓPS₅₋ₓCl₁₊ₓ` 는 (그들 x 표기로 1+x) **문자 그대로 우리 modelc 족**이다.

**② 실제 훈련셋: ❓ 확인 불가.** 조성 목록이 없어서(위) **x=1.6 이 50개 안에 있었는지 알 수 없다.** 다만 Fig. 7 이 이 족을 *"promising compositions"* (= 아직 안 만든 것)로 내놓으므로 **훈련셋 밖일 가능성이 높다** — 우리 추론이지 논문 진술이 아니다.

**③ ⭐ 지배 descriptor 축(r_anion): ⛔ 사실상 밖이다 — 이게 결정적이다.**

`figure-read`: **Fig. 5a 의 r_anion 축은 1.84 → 2.00 Å**, **Fig. S4 는 1.855 → 2.01 Å**. 그리고 표본 점(검은 마커)은 **연속이 아니라 세로 줄무늬**로 뭉쳐 있다 — 대략 **≈1.855–1.86**, **≈1.89–1.90**, **≈1.96–1.98**, **≈2.01** 네 군데. 줄무늬 사이는 전부 보간이다.

표준 Shannon/Pauling 음이온 반경(S²⁻ 1.84 · Cl⁻ 1.81 · Br⁻ 1.96 · I⁻ 2.20 · Se²⁻ 1.98)으로 우리가 되짚으면:

| 조성 | r_anion 재구성 | 그들 축 대비 |
|---|---|---|
| Li₇PS₆ (x=0) | (6×1.84)/6 = **1.840** | 축 왼쪽 끝 |
| **comp1 Li₆PS₅Cl** | (5×1.84+1.81)/6 = **1.835** | ⚠ **왼쪽 끝 바깥/경계** |
| **modelc Li₅.₄PS₄.₄Cl₁.₆** | (4.4×1.84+1.6×1.81)/6 = **1.832** | ⛔ **바깥** |
| Li₅PS₄Cl₂ (x=2) | (4×1.84+2×1.81)/6 = **1.830** | ⛔ **바깥** |
| Li₆PS₅Br | (5×1.84+1.96)/6 = **1.860** | ⭕ 왼쪽 줄무늬와 일치 |
| Li₆PS₅I | (5×1.84+2.20)/6 = **1.900** | ⭕ 두 번째 줄무늬와 일치 |
| **LPSOCl (O 1개 치환)** | (4×1.84+1.40+1.81)/6 = **1.762** | ⛔⛔ **한참 바깥** |

> ⚠ 반경표가 논문에 없으므로 위 숫자는 **우리 재구성**이다. 하지만 **방향은 표에 안 걸린다**: Cl 이 S 를 대체하면 r_anion 은 **반드시 내려간다**. 그리고 Br/I 조성이 그들 축의 왼쪽 두 줄무늬(1.860/1.900)와 **정확히 맞아떨어지는 것**이 이 재구성의 자기검증이다.
>
> **⇒ ★3 판정: 우리 Cl-rich 계는 이 모델의 1위 descriptor 축에서 훈련 범위의 왼쪽 경계이거나 그 바깥이다. 그리고 하필 그 방향이 모델이 "Ea 가 계속 내려간다" 고 말하는 방향이다 — 즉 검증되지 않은 외삽 위에 우리가 쓰고 싶은 규칙이 얹혀 있다.**
> Nd·O 공도핑까지 가면(LPSOCl r_anion ≈ 1.76, 게다가 **Nd 는 팔레트에 아예 없다**) 외삽 폭이 훈련 전체 폭(0.16 Å)의 **절반 가까이**가 된다 ⇒ **정량 사용 불가**.

---

## 8. ★4 — 검증: hold-out 인가 CV 인가, 누수는 없나, 외삽은 봤나

| 물음 | 답 |
|---|---|
| **hold-out 인가 CV 인가** | **둘 다.** ① 80/20 hold-out (40/10) 으로 R²·RMSE 보고. ② **LOOCV** 로 PRESS·Q² 를 계산해 **성분 수 4개를 선택** (Fig. S3) |
| **조성 단위인가 행 단위인가** | ⭐ **이 데이터셋은 한 조성 = 한 행**이다 (50 조성 → 50행). ⇒ **고전적 행 단위 누수(같은 조성이 훈련·시험에 동시에)는 구조적으로 불가능**하다 ✅ |
| **그럼 누수가 없나** | ⛔ **다른 종류의 누수가 둘 있다** (아래) |
| **외삽(훈련범위 밖) 성능을 보고했나** | ⛔ **안 했다.** 훈련범위 밖 조성에 대한 검증은 **0건**이다. Fig. 7 의 6개 설계족은 전부 외삽이지만 **예측 Ea 숫자조차 없고**(§3.5) 어떤 사후 검증도 없다. |
| 분할 난수시드 | 미기재 |
| 반복 분할 / 앙상블 | **없다** — 단일 분할 1회 |

### 8.1 누수 ① — **성분 수(4)를 어느 셋에서 골랐는지 논문이 안 밝힌다**

본문 순서는 *"원 데이터셋을 훈련(80 %)·시험(20 %)으로 나눈다"* → *"Fig. S3 가 성분 수에 대한 PRESS·Q² 를 보여준다"* 다. **그 LOOCV 가 훈련 40개에서만 돌았는지, 전체 50개에서 돌았는지 한 문장도 없다.** 후자라면 **모델 선택에 시험셋이 들어간 것**이다.
⇒ **논문에 없다.** 재현하려면 저자에게 묻거나 우리가 다시 짜야 한다.

### 8.2 누수 ② — **근접중복(near-duplicate) 누수**

50 조성은 무작위 재료가 아니라 **하나의 격자에서 파생된 준-중복**이다 (`X` 만 Cl→Br, `Y` 만 S→Se 식). 무작위 80/20 을 하면 시험셋의 이웃이 거의 확실히 훈련셋에 있다. 이건 우리가 이미 정면으로 다룬 문제다 — `comparison_vs_ours.md` 에 우리 실측이 있다: **쌍 LOOCV 0.0892 → LODO −0.1805 → L2DO −0.2548** (group-out 으로 바꾸면 R² 가 0.27 낙차). ⇒ **이 논문의 0.82 는 group-out 이 아니라 무작위 분할 값이고, group-out 이면 크게 내려갈 것으로 보아야 한다.**

### 8.3 ⭐ 이 논문 자신이 계산한 정직한 수치가 있다 — Q² = 0.659

Fig. S3 이 **LOOCV Q² 최대 = 0.65877** 을 인쇄한다. 그런데 논문은 이 값을 **성분 개수 고르는 데만 쓰고, 성능으로는 한 번도 언급하지 않는다** — 초록·결론·Fig. 3 은 전부 R² 0.887/0.820 만 말한다.

> **판정: 이 모델의 가장 방어 가능한 일반화 수치는 R² 0.820 이 아니라 Q² ≈ 0.66 이다.** (그리고 그 0.820 마저 §11-1 처럼 정의가 틀렸다.)

---

## 9. ★5 — 4c/4a 자리와 48h 케이지를 descriptor 가 어떻게 다루나 ⇒ 우리 O 자리 분석축과의 대응

### 9.1 논문의 자리 취급

본문 §2.1.2 원문: *"The lithium ions are randomly distributed over the remaining tetrahedral cavities (Wyckoff site **48h**), forming **Li⁺ cages around the free anions on the Wyckoff site 4c**."*

- **4a (A)** 와 **4c (C)** 는 **"special ions"** 라는 **독립 범주**로 승격돼 있다 — 32개 중 4개(`r_A`, `EN_A`, `r_C`, `EN_C`)가 오직 이 두 자리만을 위한 것이다. 그리고 **넷 다 VIP > 0.8** 이고 `r_C` 는 **공동 4위(1.29)** 다.
- **자리별 무질서**는 `Sconf_A`(4a) / `Sconf_C`(4c) 로 **따로** 인코딩된다.
- **48h Li 케이지**는 세 갈래로 들어간다: 점유 `OCC_Li-48h` · 케이지 안 이동 `BN_intra` + `D_Li-Li intra` · 케이지 간 이동 `BN_inter` + `D_Li-Li inter` · 케이지 중심(4c 자유음이온)까지 거리 `D_Li-C`.
- 본문 기전(§3.2 (2)): *"with chemical substitutions at the **4a and 4c** sites, the competing effects of lattice space and bottleneck size become crucial for controlling Ea"* + *"the bottleneck of the inter-cage conduction narrows when site disorder is reduced"*.

⇒ **argyrodite 를 "4a/4c 를 무엇이 차지하는가 + 그 자리가 얼마나 섞였는가" 로 요약하는 체계**다. 이건 우리가 필요한 바로 그 골격이다.

### 9.2 ⭐ 우리 Nd–O 공도핑 O-자리 축과의 1:1 대응

우리 실측(`db/properties/ndo_lpscl16_o_motif_estimand_2026_09_09.json` 위험요인 ⑨, 2026-09-09): 어닐본 6구조 전수에서 O 최근접이웃을 재니 **화학적으로 다른 두 종류**였다 —

| 우리 라벨 | 실측 O 환경 | ⇒ Zhao 자리 라벨 | ⇒ 걸리는 HECS descriptor (VIP) |
|---|---|---|---|
| `O-distributed` | **3/3 이 P 와 1.53–1.58 Å 결합** (O 가 PS₄ 사면체 안으로 = PO_xS₄₋ₓ) | **E 자리 (16e)** | `V[BE₄]` **1.06** · `D_Li-E` **1.32** · `r_anion` 1.50 |
| `O-bo4` | **0/3 이 P 와 결합** — O 가 **Li 1.82–2.05 Å · Nd 2.19–2.26 Å 양이온 케이지에만** | **A(4a) 또는 C(4c) 자유음이온 자리** | `r_C` **1.29** · `EN_C` 1.05 · `r_A` 0.99 · `EN_A` 1.17 · `Sconf_A/C` 0.90/0.85 · `D_Li-C` 1.15 |
| `O-free_s` | **1/3** (혼합) | 두 자리의 혼합 | 위 둘의 혼합 |

> **⭐ 이게 이 논문에서 우리가 건진 가장 실용적인 것이다.** 우리 O-모티프 세 배열은 **Zhao 의 descriptor 공간에서 서로 다른 방향으로 움직인다** — 사면체 O(E)는 `V[BE₄]`·`D_Li-E` 를 움직이고, 케이지 O(A/C)는 `r_C`·`EN_C`·`Sconf_C` 를 움직인다. **즉 HECS 표현은 우리 두 모티프를 구분할 수 있다.** (반대로, 조성만 쓰는 descriptor 는 둘 다 `Li…PS₄OCl…` 로 같아서 원리적으로 구분 못 한다.)
>
> ⚠ 단서 둘: ① 그 어느 것도 이 논문에서 **O 나 Nd 로 시험된 적이 없다** — 팔레트에 O·Nd 가 아예 없다. ② 우리 O-모티프 순위 자체가 아직 **UMA 내부 순위**이고 DFT 재채점 전이다 (`HZ-nd-anneal-uma-rank`, PREVIEW).

---

## 10. ★6 — 예측 Ea 를 실험·AIMD 와 대조했나

**⛔ 안 했다. 한 건도 없다.**

- 실험 Ea 와의 대조: **0건**. 실험 Ea 를 인용한 표조차 없다.
- DFT/AIMD/NEB 와의 대조: **0건**.
- 유일한 대조축은 **PLS 예측 vs BVSE 계산** (Fig. 3, Table S1) — 즉 **모델이 자기 선생을 얼마나 잘 흉내내는가**뿐이다.
- 오차: 훈련 RMSE 0.0241 · 시험 RMSE 0.0238 eV (우리 재계산). 잔차는 *"about 0.01 eV for most of the compounds"* (본문). 최악 잔차는 **+0.0718 eV** (훈련 #31, BVSE 0.5664 → 예측 0.4946) 와 **+0.0594 eV** (훈련 #3, 0.2637 → 0.2043).
- `figure-read` (Fig. 3): 파랑 사각형=훈련, 빨강 빈삼각형=시험. **Ea > 0.40 eV 인 점 3개(0.42 · 0.45 · 0.507 · 0.566)는 전부 훈련셋**이고 **시험셋 10점은 0.244–0.371 구간에만** 있다. 0.566 점이 눈에 띄게 이상선 아래로 처져 있다.

### 10.1 우리 값과 나란히 — ⛔ **인용 조건을 반드시 같이 읽는다**

| 계 | 이 논문(BVSE 라벨) | 우리 값 | ⛔ 인용 조건 (`citation_hazards.json` / `canonical_registry.json`) |
|---|---|---|---|
| **Li₆PS₅Cl = comp1** | **≈ 0.322 eV** (Fig. 7 상한값 — **우리 추론**: Table S1 격자값 0.322265625) | **MLIP-MD Ea 0.2532 eV** (`MD_Ea_eV_singleseed@comp1`) | ⛔ **status `provisional` · `blocking_gate: diffusive_regime_gate`**. `HZ-comp1-Ea-diffusive-gate` **HOLD**. 금지: `cross_composition_ranking` · `cite_until_beta_gate_passes` · `absolute_sigma` · `single_trajectory_CI` · `long_time_convergence`. 레지스트리 주석: *"legacy deck 앵커로만 쓴다"* (확산영역 게이트 **6/6 탈락**) |
| | | **BVSE E_3D 0.2734 eV** (bvlain, `bvse_bvlain_ev_4sys.json`) | ⛔ **`⚠_VERDICT_ranking_forbidden`** — 절대 스케일은 그럴듯하나 **가족 내 랭킹 인용 금지** |
| **Li₅.₄PS₄.₄Cl₁.₆ = modelc** | (그들 설계 추천 1번 족, **예측값 없음**) | **MLIP-MD Ea 0.2235 eV** (`MD_Ea_eV_singleseed@modelc`, canonical) | ⛔ 금지: `cross_composition_ranking` · `absolute_sigma` · `single_trajectory_CI` · `long_time_convergence`. 주석: *"deck 앵커. **같은 창의 단일 궤적끼리 짝지을 때만** 쓴다"* |
| | | **MLIP-MD Ea 0.197 ± 0.032 eV** (3-seed, canonical) | ⛔ 금지 동일 + `single_seed_ratio`. `uncertainty_kind` = run-to-run 산포(평균 CI 아님) · `protocol_generation: gen0_pre_gate` |
| | | **BVSE E_3D 0.4785 eV** (bvlain) | ⛔ 랭킹 금지 (위와 같은 사유) |
| 실험 앵커 | — | **argyrodite 실험 Ea ≈ 0.28–0.32 eV** (4편 수렴: [Ling26] 0.288/0.325 재정정 · [LiGaF] 0.28 · [LiInF] 0.303/0.29 · [Wu26] 0.32) | 문헌 소환값 — 우리 db 절대값과 같은 표에 섞지 않는다 |

> ⛔⛔ **`HZ-cross-system-Ea` (BLOCKED)**: 세 계(LPSOCl·modelc·b2o3) Ea **직접 비교는 철회·보류**다. 위 표는 **논문 vs 우리** 대조이지 **우리 계끼리 순위표가 아니다** — comp1 0.2532 와 modelc 0.2235 를 나란히 놓고 "modelc 가 낮다" 고 쓰면 두 항목 모두의 `cross_composition_ranking` 금지를 어긴다.

### 10.2 ⭐ 유일하게 방법론적으로 정당한 숫자 비교 — **BVSE ↔ BVSE**

우리 comp1 BVSE E_3D **0.2734 eV** vs 이 논문의 Li₆PS₅Cl BVSE **≈0.322 eV**. **같은 축(BVSE 장벽)** 이므로 이 한 쌍만은 비교가 성립한다 — 차이 **≈49 meV**.
⚠ 단서: 코드(bvlain vs SPSE)·파라미터셋·구조(우리 DFT-이완 V0 셀 vs 그들 실험 정련 CIF)·percolation 차원 정의가 전부 다르다. 그리고 그들 값 0.322 는 **우리 추론**이다. ⇒ **"같은 자릿수" 까지만.**

---

## 11. ★ 비판 — 실제로 어긋난 것들 (전부 우리가 원자료로 검산했다)

### 11-1 ⭐ **시험 R² 0.820 은 논문 자신의 Eq. (5) 정의를 만족하지 않는다**

본문 Eq. (5) 는 `R² = 1 − Σ(yᵢ−y′ᵢ)² / Σ(yᵢ−ȳ)²` 다. Table S1 의 시험 10행으로 그대로 계산하면 **0.7661** 이다. 인쇄된 **0.820** 은 **Pearson 상관계수의 제곱(0.8203)** 이다 — 두 값이 소수 셋째 자리까지 맞는다. 훈련셋은 0.8869 로 두 정의가 일치해서(PLS 훈련 적합은 무편향) 안 걸렸고, **시험셋에서만 갈렸다**. 편향이 있는 예측에서 r² 는 R² 보다 항상 크다.
⇒ **초록·Fig. 3·결론의 "test set R² 0.820" 은 정의가 틀린 수치다. 정정값은 0.766.**

### 11-2 ⭐ **자기 LOOCV 결과(Q² 0.659)를 성능에서 숨겼다**

Fig. S3 에서 계산해 놓고 성분 선택에만 쓴다. R² 0.887/0.820 만 반복 인쇄한다. §8.3.

### 11-3 ⭐ **VIP 컷 0.8 은 표준(1.0)보다 느슨하고, 헤드라인이 그 틈에 들어 있다**

초록: *"especially the anion size **and the resultant structural changes associated with anion site disorder**"*. 그런데 자리무질서 3인방의 VIP 는 `figure-read ≈` **Sconf_A 0.90 · Sconf_C 0.85 · Sconf_anion 0.81** 로 **19개 중 하위 3위**이고, **표준 관례인 VIP > 1 을 쓰면 셋 다 탈락한다** (VIP>1 은 14개만 남는다). 즉 **논문의 두 헤드라인 중 하나가 JMP 기본값 0.8 에 의존한다.** 논문은 컷이 JMP 기본값임을 밝히긴 하지만, 결론의 강도가 그 선택에 걸려 있다는 언급은 없다.

### 11-4 ⭐ **`a` 와 `v` 는 같은 정보다 (Fig. S2 에서 r = 1.00)**

입방 셀이므로 `v = a³`. `figure-read` (Fig. S2 히트맵): **a↔v = 1.00**. 그런데 둘 다 "중요 19개" 에 **각각** 들어가 있고 VIP 도 똑같이 ≈1.29 다. 상위 descriptor 개수를 세는 서술(*"six structural descriptors"*)이 실질보다 하나 부풀어 있다. 더 넓게는 `r_anion↔a` ≈0.95 · `r_anion↔v` ≈0.95 · `r_anion↔D_Li-B` ≈0.92 라 **상위 4개가 사실상 한 변수**다. ⇒ **VIP 를 개별 descriptor 의 인과 기여로 읽으면 안 된다** (PLS-VIP 는 상관군 안에서 중요도를 나눠 갖는다).

### 11-5 ⭐ **Fig. 2a 의 M/N 범례 색이 뒤바뀌어 있다 + Table S2 의 자리 표기 충돌**

- `figure-read` (Fig. 2a): 분홍 = *"Non-mobile cation elements M"* 인데 **Si, Ge 가 분홍**이고, 연파랑 = *"N"* 인데 **P, As 가 연파랑**이다. 본문 정의는 **M = P⁵⁺, As⁵⁺ / N = Si⁴⁺, Ge⁴⁺, Sn⁴⁺** 이므로 **정반대**다. **Fig. 7 의 같은 주기율표는 올바르게(연파랑=M=P/As/Sb, 분홍=N=B/Al/Ga/Si/Ge/Sn) 칠해져 있다** — 즉 Fig. 2a 쪽이 틀렸다.
- Fig. 2a 에 **Sn 이 색칠돼 있지 않다** (본문 정의에는 있다).
- **Table S2 #15**: `D_Li-E` 를 *"nearest neighboring ions on Wyckoff **4d**"* 라고 적었다. 본문은 **E = 16e** 다. `4d` 는 C 자리(4c 의 대체 setting)라 **C 와 E 가 같은 자리를 가리키게 된다** — 표기 오류로 보인다.
- **Table S2 #23**: `OCC_Li-24g` 설명이 *"Lithium ion occupancy on Wyckoff 48h site, Wyckoff 24g site"* — **#22 문장이 잘려 붙은 편집 오류**.

### 11-6 ⭐ **Fig. 5 의 등고선은 모델의 부분의존도가 아니라 원자료 2D 보간이다 — 그리고 데이터 껍질 밖에서 색을 칠한다**

본문이 스스로 *"two-dimensional **projections**"* 라고 부른다. 즉 나머지 30개 descriptor 가 자유롭게 변하는 채로 2축에 투영한 뒤 보간한 것이라, 여기서 읽은 "기전" 은 **전부 교락(confounded)** 이다.
결정적 증거 — `figure-read` (Fig. 5d, BN_inter vs BN_intra): 컬러바 **최소가 0.2440 eV**(= 데이터셋 전체 최소)인데, 패널 중앙 상부에 **그보다 낮은 값을 뜻하는 검은 영역이 넓게** 있다. **관측된 어떤 Ea 보다도 낮은 값을 보간이 만들어냈다.** 그런데 본문은 바로 그 영역을 근거로 *"there is an optimal combination of BNinter and BNintra to achieve lower Ea"* 라고 쓴다. ⇒ **논문의 "최적 병목 조합" 은 보간 인공물 위에 서 있다.**

### 11-7 ⭐ **"r_anion 이 1위" 는 새 기전이 아니라 화학 라벨의 재진술일 수 있다**

`figure-read` (Fig. S4 여섯 패널): 표본 마커가 r_anion 축을 따라 **연속 분포가 아니라 네 개의 세로 줄무늬**(≈1.855 / ≈1.89 / ≈1.96–1.98 / ≈2.01)로 뭉쳐 있다. 우리 재구성(§7.1)으로 이 줄무늬는 각각 **Br계 / I계 / …** 처럼 **halide·chalcogen 종에 대응**한다. 즉 `r_anion` 은 사실상 *"S 계인가 Se 계인가, Cl 인가 Br 인가 I 인가"* 를 하나의 실수로 코딩한 **범주형 화학 라벨**이다.
⇒ *"r_anion 이 가장 중요하다"* = *"어느 할로겐·칼코겐을 골랐는지가 가장 중요하다"* 로, argyrodite 문헌(Deiseroth 2008 [34], Kraft 2017 [35])이 이미 아는 것이다. 그리고 **"r_anion = 1.9 Å 에서 급격한 경계"** 는 물리적 문턱이 아니라 **두 화학군 사이의 빈 구간을 보간이 메운 자리**일 수 있다. 논문은 이 가능성을 검토하지 않는다.

### 11-8 **전략 ③(협동 전도)은 자기 모델이 지지하지 않는다**

Fig. 7 의 화살표는 ①broaden bottleneck ②order→disorder ③activate concerted Li⁺ conduction 인데, **①과 ②에만 "Example" 화살표와 조성 표가 달려 있고 ③은 비어 있다.** 본문도 근거를 외부 문헌 [6,40,41] 로만 댄다. §6.3 에서 본 대로 **BVSE 라벨이 협동운동을 원리적으로 못 본다** — 그래서 예시를 못 만든 것이다. **그런데 초록은 세 전략을 동등하게 나열한다.**

### 11-9 **재현성: 데이터셋이 공개돼 있지 않다**

Table S1 은 라벨만, Table S2 는 정의만 준다. **50개 조성 목록 없음 · descriptor 32×50 값 행렬 없음 · BVSE 설정 없음 · 반경/분극률 표 없음 · Sconf/BN 계산식 없음 · 코드 없음 · 시드 없음.** ⇒ **이 논문의 결과는 논문만으로 재현 불가능하다.** (§12)

### 11-10 **표본 크기 대비 자유도**

n=40 훈련, p=32 descriptor. PLS 4성분이라 실효 자유도는 줄지만, **descriptor 가 표본과 같은 자릿수**다. 부트스트랩·반복분할·X-randomization(우리가 Sendek 2017 에서 이식한 소표본 방어) 중 **아무것도 없다**.

### 11-11 **라벨 격자를 안 밝힌다**

§3.4 — 라벨 50개가 전부 10/1024 eV 격자 위에 있고 서로 다른 값이 **18개뿐**이다. 즉 회귀의 응답변수가 사실상 **18단계 순서형**이다. RMSE 0.02 eV = 격자 2.4칸. 이 사실을 알면 "RMSE 0.02 eV" 의 의미가 달라지는데 논문은 언급하지 않는다.

---

## 12. ★7 — 코드·데이터 공개, 라이선스, SI 에만 있는 것

### 12.1 공개 여부

| 항목 | 상태 |
|---|---|
| **Data availability 문구** | ⛔ **없다** (전문 검색 0건) |
| **Code availability 문구** | ⛔ **없다** |
| 저장소(GitHub/Zenodo/…) | ⛔ **없다** |
| 있는 것 | `Appendix A. Supplementary materials` → `https://doi.org/10.1016/j.scib.2021.04.029` 한 줄뿐 |
| **BVSE 도구** | **SPSE** — ref [28] He B, Chi S, Ye A, et al. *Sci Data* **2020**, 7, 151. **공개 웹 플랫폼** `https://matgen.nscc-gz.cn/solidElectrolyte/` (논문이 직접 URL 제공). ⇒ **라벨 재생성 경로는 원리적으로 열려 있다** (단 어떤 설정을 썼는지는 모른다) |
| **ML 도구** | **JMP** (SAS Institute) — **상용 라이선스**. ref [32] *JMP 13 Multivariate Methods* (2017), [33] Cox & Gaudard, *Discovering Partial Least Squares with JMP* (2013) |
| **라이선스** | © 2021 Science China Press, Elsevier. **All rights reserved** — OA 아님, CC 라이선스 없음 |
| 이해충돌 | 없음 선언 |
| 자금 | 중국 국가중점 R&D 2017YFB0701600 · NSFC 11874254, 51622207, U1630134 |

### 12.2 **SI 에만 있는 것** (본문에 없다)

| SI 항목 | 내용 | 우리에게 중요한가 |
|---|---|---|
| **Table S1** | 50행 Ea 3열 (BVSE / PLS / 잔차). **훈련 40 + 시험 10 구분됨** | ⭐⭐ **이 digest 의 §3.2·§3.4 검산이 전부 여기서 나왔다.** 조성은 없음 |
| **Table S2** | **32개 descriptor 의 이름·설명·범주** | ⭐⭐⭐ **★1 의 유일한 출처.** 본문은 개수(32)만 말한다 |
| **Fig. S1** | PLS 방법 개요 도식 (출처: SI ref [1] R.D. Tobias, SAS Institute, Cary NC, 1995) | 일반 교과서 그림 — 우리에게 새 정보 없음 |
| **Fig. S2** | **32×32 Pearson 상관 히트맵** (숫자 인쇄됨) | ⭐⭐ **§11-4 다중공선성 판정의 유일한 근거.** `a↔v = 1.00` 등 |
| **Fig. S3** | PRESS·Q² vs 성분 수 (0–15). 캡션에 **PRESS 0.58415 · Q² 0.65877 @ 4성분** | ⭐⭐ **§8.3 — 가장 정직한 일반화 수치가 여기 있다.** 본문은 성분 수 선택 근거로만 인용 |
| **Fig. S4** | r_anion vs 6개 descriptor 등고선 6패널 | ⭐ **§7.1 외삽 판정 · §11-7 줄무늬 관찰의 근거** |
| SI ref [1] | R.D. Tobias, SAS Institute Inc., Cary NC, 1995 (PLS 튜토리얼) | — |

> ⚠ SI 는 **docx** 다. `word/media/` 안에 이미지 30개가 들어 있지만 **문서가 실제로 참조하는 것은 4개**(rId6–9 = Fig S1–S4)뿐이다 — 나머지 26개는 편집 잔재다. 우리는 참조된 4개만 `litdb/figures/<slug>/fig_S1..S4.png` 로 옮겼다.

---

## 13. ⭐ §우리 cascade 에 주는 것 — descriptor 를 무엇으로 정할 것인가 + 외삽 판정

### 13.1 먼저 판정: **라벨은 버리고 descriptor 만 빌린다**

가장 중요한 사실 하나를 놓고 시작한다.

> **이 논문의 타깃(BVSE Ea)은, 우리 조성축에서 이미 순위가 뒤집힌 것으로 실측돼 있다.**
> `db/properties/bvse_bvlain_ev_4sys.json` → **comp1 E_3D 0.2734 < modelc 0.4785** (BVSE)
> 반면 **MD 는 modelc 0.197±0.032 < comp1 0.2532** — **완전 역전**.
> 그 파일의 판정: *"가족 내 랭킹은 MD와 역전 … vacancy paradox(점유-무관 지도)가 eV 단위에서도 그대로 재현된 것. → σ/Ea 순위 인용 금지."*

그리고 §6.3 에서 본 대로 **Zhao 의 VIP 는 그 실패를 그대로 물려받는다** — Li 농도·Li 점유·Li–Li 거리 8개가 전부 컷 아래다. 우리 `kb/concepts/bvse.md` §9 는 이 실패의 이름까지 갖고 있다: **comp1→modelc 는 "채널부피 −15 % 인데 σ ×4 ↑" 이고 원인은 vacancy/무질서 — 점유-무관 지도의 원리적 사각**.

> ⛔ **따라서: Zhao 모델(또는 그 재구현)을 우리 Cl-rich 도펀트 랭킹의 채점 함수로 쓰지 않는다.** 쓰면 우리가 이미 틀린 줄 아는 답을 학습한 대리모델을 쓰는 것이다.
> ⭕ **그러나 descriptor **표현**은 다르다.** 표현은 라벨과 무관하게 재사용 가능하고, 우리 라벨(MLIP-MD Ea, BVSE 채널%, ICOHP, gap …)에 다시 붙일 수 있다.

### 13.2 구체안 — 우리 cascade 의 descriptor 집합 v0 초안 (**제안이지 판정 아님** — 보고량 카드로 올려야 한다)

Zhao 의 5범주 골격을 유지하되, **① 정의 없는 것은 뺀다 ② 우리 축(Cl-rich·O·Nd)에서 실제로 움직이는 것만 남긴다 ③ Li 를 보는 축을 우리가 추가한다.**

**A군 — Zhao 에서 그대로 가져올 수 있는 것 (🟢, 정의 명확 + 우리가 지금 계산 가능)**

| # | descriptor | Zhao VIP ≈ | 왜 남기나 |
|---|---|---|---|
| A1 | `a` (또는 `v`, **둘 중 하나만**) | 1.29 | 격자 크기. ⚠ §11-4 — **둘 다 넣지 않는다** |
| A2 | `V[PS₄]` (= `V[BE₄]`) | 1.06 | ⭐ **우리 O-모티프가 직접 움직이는 양** (P–O 결합 시 사면체 부피 변화) |
| A3 | `EN_A`, `EN_C` | 1.17 / 1.05 | 4a·4c 를 무엇이 차지하는지의 화학 축 |
| A4 | `Sconf_A`, `Sconf_C` — **단 우리 식으로 재정의** | 0.90 / 0.85 | ⭐ Cl-rich 의 핵심(자리무질서). Zhao 식이 없으므로 **우리가 `S = −R Σ pᵢ ln pᵢ` × (자리당 원자수) 로 못박고 그 규약을 기록** |
| A5 | `OCC_Li-48h`, `C_Li` | 0.73 / 0.72 (Zhao 는 버림) | ⭐⭐ **Zhao 가 버린 것을 우리는 살린다** — 그가 버린 이유는 BVSE 라벨이 못 봐서이고, **우리 라벨(MLIP-MD)은 본다** |

**B군 — 우리가 이미 갖고 있어 Zhao 보다 강한 것 (새로 만들 필요 없음)**

| # | descriptor | 출처 | Zhao 대응 |
|---|---|---|---|
| B1 | **BVSE 채널 %** (above-min ≤ iso, 0.25 Å voxel, 원본 주기셀) | `tools/comp1_v3/` | `BN_intra`/`BN_inter` 를 대체 — **정의가 문서화돼 있다** (Zhao 것은 없다) |
| B2 | **BVSE percolation E_1D/2D/3D** | `bvse_bvlain_ev_4sys.json` | Zhao 의 **타깃 그 자체**. ⇒ 우리 쪽에서는 **특징으로 강등**해서 쓴다 (라벨 아님) |
| B3 | **ICOHP (P–S, Li–Cl …)** | `db/properties/nd_icohp.json`·`bonds.json` | Zhao 에 **대응물 없음** — 결합강도 축을 우리가 추가 |
| B4 | **O 배위 모티프 (P–O 결합 유무)** | `ndo_lpscl16_o_motif_estimand_2026_09_09.json` ⑨ | §9.2 — Zhao 의 A/C vs E 자리 구분의 **우리 실측판** |

**C군 — 빼는 것과 그 이유**

| 뺄 것 | 이유 |
|---|---|
| `r_anion`, `r_A`, `r_C`, `PL_*` | 반경·분극률 **표가 논문에 없다** → 우리가 정하면 Zhao 값과 비교 불가. 그리고 §11-7 대로 **화학 라벨의 재진술**이라 one-hot(할로겐 종)으로 넣는 편이 정직하다 |
| `BN_doublet`, `V[LiACE₂]` | 정의 없음 + Zhao 에서도 컷 아래 |
| `v` (A1 에서 `a` 를 골랐으면) | r = 1.00 중복 |
| `D_Li-Li *` 3종 | Zhao 전부 컷 아래이고, 우리는 같은 정보를 MD 궤적에서 직접 본다 |

**D군 — 반드시 같이 정해야 하는 규약 (이걸 안 정하면 A4·A5 가 무의미해진다)**
1. **입력 구조가 무엇인가**: Zhao 는 **실험 정련 CIF**, 우리는 **DFT-이완 V0 셀**. 섞으면 안 된다 — 하나로 못박고 기록한다.
2. **부분점유를 어떻게 다루나**: Zhao 는 점유율을 스칼라로 압축, 우리는 실제 배열을 만든다. **descriptor 를 배열마다 계산해 앙상블로 낼지, 점유율에서 직접 낼지** 정해야 한다.
3. **Sconf 의 단위**: per site / per formula unit / per cell — Zhao 축은 0–33 J/(K·mol) 인데 어느 것인지 모른다 (`figure-read` Fig. 5e). 우리는 명시한다.

### 13.3 ⭐ 외삽 판정 (★3 종합)

| 축 | 우리 계 | Zhao 훈련 범위 | 판정 |
|---|---|---|---|
| 조성 명목식 | modelc = 그들 x=1.6 | 0 ≤ x ≤ 2 | ⭕ **안** |
| 실제 50 조성 목록 | ? | **목록이 공개 안 됨** | ❓ **확인 불가 — 논문에 없다** |
| **r_anion (1위 descriptor)** | comp1 ≈1.835 · **modelc ≈1.832** (우리 재구성) | **≈1.84–2.00** (`figure-read`) | ⛔ **경계 또는 바깥** |
| r_anion — **+O 계 (LPSOCl)** | ≈**1.762** | 같음 | ⛔⛔ **훈련 폭의 절반만큼 바깥** |
| 원소 팔레트 | **O, Nd, B** | Li·Si·Ge·P·As·S·Se·Cl·Br·I | ⛔ **O·Nd·B 전부 없음** |
| 라벨 종류 | MLIP-MD Ea (동역학) | BVSE (정적·점유무관) | ⛔ **다른 양** |

> **판정 한 줄: 우리 Cl-rich 계는 조성식으로는 안이지만, 이 모델이 실제로 학습한 축(r_anion)에서는 왼쪽 경계 밖이고, O/Nd 를 넣는 순간 화학적으로도 밖이다. ⇒ Zhao 모델의 예측 Ea 를 우리 계에 숫자로 쓰는 것은 금지. 쓸 수 있는 것은 ① descriptor 이름·자리 분류 체계 ② "Cl 을 늘리면 r_anion 이 내려간다" 는 방향 서술 ③ 4a/4c/16e 자리 구분 틀 — 이 셋뿐이다.**

### 13.4 다음 행동 3개 (제안)

1. **보고량 카드를 먼저 쓴다** (`kb/templates/estimand_card.md`) — *"cascade 채점 descriptor 벡터"* 가 우리 계에서 잘 정의되는가. 특히 **부분점유·무질서 배열이 여럿인데 집계 규칙이 없으면 스칼라 descriptor 는 정의되지 않는다** (회신 N 기준). Zhao 는 이 문제를 "점유율 스칼라로 압축" 으로 회피했는데, 우리는 배열을 만들어 쓰므로 **집계 규칙(최저? 앙상블 평균? 분포?)을 미리 적어야 한다**.
2. **A군+B군으로 우리 4계(comp1·modelc·lpsocl·b2o3)의 descriptor 행렬을 만들고, 우리 라벨(MLIP-MD Ea)에 대해 상관만 본다** — 회귀는 아직 하지 않는다 (n=4).
3. **BN 을 우리 정의로 못박는다** — Zhao 서사의 중심(전략 ①)인데 계산식이 없다. 우리 BVSE 채널 % 가 이미 그 자리를 대신할 수 있고 **정의가 문서화돼 있다는 점에서 더 낫다**.

---

## 14. Figure set ★

우리가 **실제로 이미지를 열어 본 것**과 **안 본 것**을 구분해 적는다.

| Fig | 내용 (무엇을 보여주나) | 우리 활용 | 봤나 |
|---|---|---|---|
| 1 | ML 전체 흐름: Database → SSE(unit cell) → {Ea 라벨 · descriptor} → ①Dataset → ML → ②Ea 예측모델 → ③모델 해석 → 새 조성 → Database 되먹임. 하단에 HECS 5범주 원통(Composition/Structure/Conduction pathway/Ion distribution/Special ions)과 각 범주 항목 | **"계층적 인코딩" 의 정의 그림.** 우리 cascade 흐름도의 원형으로 그대로 차용 가능 | ✅ |
| 2a | 단위셀 + 자리 범례(M/N 4b · Y 16e · X/Y 4a · X/Y 4c · Li 24g,48h) + **샘플링 원소 주기율표** | ★3 판정의 근거. ⚠ **(x,y) 격자가 아니라 원소 팔레트라 50 조성을 복원할 수 없다.** ⚠ **M/N 범례 색이 뒤바뀌어 있다**(§11-5) | ✅ |
| 2b | 셀 그림 위 **파란 박스=Global / 빨간 박스=Local** + 노란 Li 확산 등가면 | **"2층 × 5범주" 의 시각적 정의.** 우리 descriptor 문서의 그림 틀 | ✅ |
| 3 | BVSE 계산 Ea vs PLS 예측 Ea 산점 (축 0.20–0.60 eV). 파랑■=훈련 40, 빨강△=시험 10 | ★4·★6. `figure-read`: **Ea>0.40 인 4점이 전부 훈련셋**, 시험 10점은 **0.244–0.371 에만** ⇒ 시험셋이 고-Ea 를 안 본다. 0.566 점이 크게 처짐 | ✅ |
| 4 | **32개 descriptor 의 VIP 막대** + 5범주 색 + 0.8 점선 | ★2 순위표의 유일한 출처(본문에 값 없음). §6.2 표가 이 그림의 `figure-read`. ⭐ **Li 관련 8개가 전부 컷 아래**라는 §6.3 판정의 근거 | ✅ |
| 5a–f | Ea 등고선 6쌍: (a) r_anion×EN_cation (b) V×V[BE₄] (c) D_Li-B×D_Li-E (d) BN_intra×BN_inter (e) Sconf_A×Sconf_C (f) r_A×r_C | 축 범위를 우리 계와 맞대는 데 필수. ⭐ **(d) 에 데이터 최소(0.2440 eV)보다 낮은 검은 보간 영역** = §11-6. ⚠ (e) 는 본문의 *"positive effect of larger Sconf"* 와 달리 **비단조**(Sconf_A≈16 에 고-Ea 붉은 띠) | ✅ |
| 6 | 기전 도식 — 치환 → 결정구조 변화 → {상호작용·격자공간·자리무질서} → coupling → **병목 크기** → Ea. 중앙에 5범주 톱니바퀴 | 서사 구조만. **숫자 없음** | ✅ |
| 7 | 설계 전략 3개(①병목 확대 ②질서→무질서 ③협동전도) + **6개 조성족과 Ea 상한 표** + 확장된 원소 팔레트 | ⭐⭐ **우리 modelc 족 `Li₆₋ₓPS₅₋ₓCl₁₊ₓ < 0.322 eV` 가 여기 있다.** ⭐ **전략 ③에만 예시가 비어 있다**(§11-8). 팔레트가 Fig. 2a 보다 넓다(B·Al·Ga·Sn·Sb 추가) = **설계공간 ≠ 훈련공간** | ✅ |
| S1 | PLS 방법 개요 (Tobias SAS 튜토리얼 인용) | 교과서 도식 — 우리에게 새 정보 없음 | ⛔ **안 봤다** |
| S2 | **32×32 Pearson 상관 히트맵** (셀에 숫자 인쇄) | ⭐ §11-4. `figure-read`: **a↔v = 1.00** · r_anion↔a ≈0.95 · r_anion↔v ≈0.95 · r_anion↔D_Li-B ≈0.92 · EN_anion↔PL_anion ≈−0.95 · D_Li-A↔D_Li-Li intra ≈0.98 ⇒ **상위 4개가 사실상 한 변수** | ✅ |
| S3 | PRESS(좌축)·Q²(우축) vs 성분 수 0–15 | ⭐ §8.3. `figure-read`: PRESS 0성분 ≈1.02 → **4성분 최소 ≈0.58** → 11성분 ≈1.22 로 되오름. Q² 는 4에서 ≈0.66 → 11에서 ≈−0.5 | ✅ |
| S4 a–f | r_anion 을 x축 고정하고 y축에 BN_intra/BN_inter/Sconf_A/Sconf_C/r_A/r_C | ⭐ §7.1·§11-7. `figure-read`: **6패널 전부 저-Ea(진파랑) 영역이 왼쪽 끝(r_anion ≈1.855–1.89)** + 표본이 **네 개 세로 줄무늬**로만 존재 | ✅ |
| Table 1 | 선행 ML-SSE 연구 7건의 descriptor 비교 (LiSICON/올리빈/tavorite/garnet/multi-type/Na·Li 초이온/Li 함유) | 문헌 위치잡기용. `tab_1.png` 로 잘라 뒀지만 **PDF 텍스트가 더 정확해 이미지로는 안 읽었다** | ⛔(텍스트로 읽음) |

> **본 그림 요약: 크로핑 12장 중 10장을 실제로 열어 봤다** (Fig. 1·2·3·4·5·6·7 + S2·S3·S4). **안 본 것 2장** — `fig_S1.png`(PLS 교과서 도식, 정보 없음) · `tab_1.png`(표라서 PDF 텍스트로 읽음).
> **본문 서술과 어긋난 것 3건**: Fig. 2a 범례 색(§11-5) · Fig. 5d 검은 보간영역 vs "최적 조합" 주장(§11-6) · Fig. 5e 비단조 vs "positive effect of larger Sconf"(§11-6 주석).

---

## 15. Post-processing ★

| 항목 | 내용 |
|---|---|
| **무엇** | ① **BVSE** (라벨 생성) ② **PLS 회귀** ③ **VIP** 변수중요도 ④ **LOOCV/PRESS/Q²** 성분선택 ⑤ **Pearson 상관 히트맵** ⑥ **2D 등고선 보간** |
| **도구** | **SPSE** 웹 플랫폼(BVSE) · **JMP**(PLS·VIP·PRESS·Q²; 상용). 히트맵·등고선은 도구 미기재(스타일상 Origin/파이썬 혼용으로 보이나 **논문에 없다**) |
| **수치화** | Ea 는 eV, **10/1024 eV 격자**(§3.4, 논문 미언급). 성능은 R²·RMSE 두 개. 중요도는 VIP 단일 스칼라, 컷 0.8 |
| **플롯** | 파리티(Fig. 3) · VIP 막대(Fig. 4) · 등고선 12장(Fig. 5 6패널 + Fig. S4 6패널) · 상관 히트맵(Fig. S2) · PRESS/Q² 곡선(Fig. S3) |
| **기록** | Table S1 에 50행 (계산·예측·잔차). **descriptor 값 행렬은 기록되지 않았다** |
| ⛔ **안 한 것** | NEB · AIMD · DOS/PDOS · COHP · Bader · ELF · 탄성 · phonon · ESW — **전부 0건** |

---

## 16. 인용 가능 문장 (deck/paper 용)

- "Zhao et al. 은 입방 Li-argyrodite 50종에 대해 **단위셀 정보만으로 뽑히는 32개 HECS descriptor**(조성·구조·전도경로·이온분포·특수이온 5범주)를 정의하고 PLS 로 활성화에너지를 회귀해, **음이온 평균반경 `r_anion` 이 VIP 1위**임을 보였다."
- "그 데이터셋의 활성화에너지 라벨 50개는 **전부 bond-valence site energy(BVSE) 계산값**이며, **실험·DFT·AIMD 대조는 한 건도 수행되지 않았다.**"
- "이 프레임워크는 argyrodite 의 **4a·4c 자유음이온 자리를 독립 descriptor 범주('special ions')로 승격**시키고, 자리별 배위 엔트로피(`Sconf_A`, `Sconf_C`)로 음이온 자리무질서를 인코딩한다."
- "제안된 설계 조성족 중 첫 번째가 **`Li₆₋ₓPS₅₋ₓCl₁₊ₓ`** 로, 우리 modelc `Li₅.₄PS₄.₄Cl₁.₆` 와 같은 족이다."
- (내부 전용) "그 모델의 타깃인 BVSE 장벽은 **우리 계에서 comp1↔modelc 순위를 MLIP-MD 와 반대로 준다**(`bvse_bvlain_ev_4sys.json`) — 따라서 descriptor 체계는 차용하되 **라벨은 우리 것으로 교체해야 한다**."

⛔ **쓰면 안 되는 문장**
- ✗ "Zhao 모델이 Li₅.₄PS₄.₄Cl₁.₆ 의 Ea 를 예측했다" — **그런 숫자가 논문에 없다** (족의 상한만 있고 그마저 모체 라벨값이다)
- ✗ "테스트 R² 0.82 로 검증됐다" — **정의가 틀렸다**(정정 0.766) 그리고 **LOOCV Q² 는 0.66** 이다
- ✗ "Li 함량은 Ea 에 영향이 적다" — **BVSE 라벨의 한계**이지 물리 결론이 아니다
- ✗ Zhao 의 Ea 값(0.322 등)을 우리 MLIP-MD Ea(0.2532 / 0.2235 / 0.197)와 같은 표·같은 축에 놓기 — **다른 양이다**

---

## 17. 주의/한계 요약 (over-claim 방지)

1. **DFT 논문이 아니다.** 방법 비교표에 넣을 때 "DFT 계산" 칸은 전부 n/a.
2. **라벨이 BVSE 다** — 그리고 우리는 그 축이 우리 조성축에서 뒤집힌다는 실측을 이미 갖고 있다.
3. **재현 불가**: 50 조성 목록 · descriptor 값 · BVSE 설정 · BN/Sconf 식 · 반경/분극률 표 전부 없음.
4. **시험 R² 0.820 은 Pearson r²** 다 (논문 Eq. (5) 기준 정정값 **0.766**). 가장 방어 가능한 값은 **Q² 0.659**.
5. **등고선은 모델 부분의존도가 아니라 원자료 보간**이고, 데이터 껍질 밖에서도 색을 칠한다(Fig. 5d 검은 영역).
6. **우리 계는 1위 descriptor 축에서 외삽**이다. O·Nd 를 넣으면 화학적으로도 팔레트 밖.
7. **우리 comp1/modelc Ea 는 인용 조건이 붙어 있다** — comp1 0.2532 는 `provisional` + 확산영역 게이트 미통과(6/6 탈락) · modelc 0.2235 는 `canonical` 이나 **`cross_composition_ranking` 금지** · 계간 Ea 직접 비교는 `HZ-cross-system-Ea` **BLOCKED**. 이 논문과의 대조는 **"우리 값 vs 문헌 값"** 형식으로만 쓰고 **우리 계끼리 순위표를 만들지 않는다**.

---

## 18. 기법 용어 미니사전

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **BVSE** (Bond-Valence Site Energy) | 결합원자가 합(BVS)이 이상값에서 벗어난 정도를 에너지로 환산해, 정지된 골격 위에서 Li⁺ 탐침이 느끼는 퍼텐셜 지도를 만드는 경험적 방법. 그 지도에서 침투(percolation)가 생기는 최저 에너지가 "장벽" | **50개 라벨 전부의 출처.** ⚠ **Li–Li 상호작용·공공 농도·협동 점프·프리팩터가 원리적으로 없다** |
| **PLS** (Partial Least Squares) | 설명변수를 y 와의 공분산이 최대가 되는 **직교 잠재성분**으로 압축한 뒤 최소제곱 회귀. 변수끼리 강하게 상관될 때(다중공선성) OLS 대신 쓴다 | 32개 descriptor → **4성분** |
| **VIP** (Variable Importance in Projection) | PLS 잠재성분의 가중치를 변수별로 모은 중요도. VIP² 평균 = 1 이 되게 정규화 → **관례 컷은 1.0** | 컷 **0.8**(JMP 기본값) 사용 → 19개 채택 |
| **PRESS / Q²** | LOOCV 예측잔차 제곱합 / `Q² = 1 − PRESS/SSY`. Q² 는 **교차검증된 R²** | PRESS 최소 0.58415, **Q² 최대 0.65877** @4성분 |
| **Wyckoff 자리** | 공간군에서 대칭적으로 동등한 원자 위치의 부류 | argyrodite F-43m: **4a**(A 음이온) **4b**(B 양이온) **4c/4d**(C 자유음이온) **16e**(E, BE₄ 의 음이온) **48h/24g**(Li) |
| **Sconf** (배위 엔트로피) | 한 자리를 여러 화학종이 무작위로 나눠 가질 때의 혼합 엔트로피 `−R Σ pᵢ ln pᵢ` | `Sconf_A`, `Sconf_C`, `Sconf_anion`, `Sconf_Li`. ⚠ **정확한 식·단위 규약 논문에 없음** |
| **Bottleneck size (BN)** | Li 확산 경로에서 가장 좁은 통로의 유효 반경 | `BN_intra`(케이지 안), `BN_doublet`, `BN_inter`(케이지 간). ⚠ **계산법 논문에 없음**. 축 범위 `figure-read` ≈0.44–0.72 Å(intra) / ≈0.487–0.62 Å(inter) ⇒ Li⁺ 반경보다 작으므로 **음이온 반경을 뺀 여유반경**으로 보인다 (우리 해석) |
| **intra-cage / inter-cage / doublet 경로** | argyrodite Li 수송의 세 갈래 — 48h 케이지 **안** 회전, 케이지 **사이** 점프, 48h 쌍(doublet) 사이 짧은 점프. 문헌 합의는 **inter-cage 가 율속** | Zhao 는 셋 다 BN·D_Li-Li 로 인코딩. **inter-cage 만 VIP>0.8** (BN_inter 1.01) |

---

## 19. 관련 digest / 우리 db 링크

| 대상 | 관계 |
|---|---|
| `kb/concepts/bvse.md` §8–9 | ⭐ **이 논문 라벨의 한계를 우리가 이미 문서화한 카드.** "문헌은 왜 BVSE 를 쓰나 / 우리가 안 쓰는 이유 4" + 실패 3사례 |
| `db/properties/bvse_bvlain_ev_4sys.json` | ⭐ 우리 4계 BVSE 장벽 + **`⚠_VERDICT_ranking_forbidden`** (comp1 0.2734 vs modelc 0.4785 = MD 와 역전) |
| `db/properties/ndo_lpscl16_o_motif_estimand_2026_09_09.json` | ⭐ 위험요인 ⑨ = **O 배위 실측** → §9.2 자리 대응 |
| `db/properties/canonical_registry.json` | comp1/modelc Ea 정본값 + `prohibitions` |
| `db/properties/citation_hazards.json` | `HZ-comp1-Ea-diffusive-gate`(HOLD) · `HZ-cross-system-Ea`(BLOCKED) · `HZ-nd-anneal-uma-rank`(PREVIEW) |
| `papers/kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md` | 이 논문 ref **[35]**. `PL_anion` descriptor 의 물리적 근거 |
| `papers/adeli2019_halide_substitution_boosting_argyrodite.md` | Cl-rich 3중 기작(정전·공공·무질서) 실험 원판 — Zhao 가 못 보는 vacancy 축 |
| `papers/deklerk2016_diffusion_site_disorder_argyrodite.md` | inter-cage 율속 + 자리무질서 기전의 계산 원판 |
| `papers/basu2026_multifidelity_bandit_dopant_screening_funnel.md` | cascade 재설계 짝. 저기는 **예산 배분**, 여기는 **표현(descriptor)** |
| `papers/fujimura2013_ml_conductivity_origin.md` | 이 논문 ref **[20]** (Table 1 첫 행) |
| `papers/sendek2017_ml_screening_12k_conductors.md` | 이 논문 ref **[25]**. 소표본 방어 절차(X-randomization 등) 는 Sendek 쪽이 우월 |
| `kb/methodology/computational_methods_canonical.md` | `cascade v23 score` LOOCV R² 0.9998 = **항등식 복원 선례** → §6.4 판정 기준 |

---

## 20. 이 digest 의 서지·판독 이력

- 본문 PDF 8쪽 전문 텍스트 추출 + **Fig 1–7, Table 1 캡션 앵커 크로핑**(`tools/litdb/extract_figures.py --slug … --clean`).
- SI 는 **docx** 라 도구가 안 먹는다 → `word/document.xml` 을 직접 파싱해 본문·표를 복원하고, `word/_rels/document.xml.rels` 에서 **실제 참조된 이미지 4개(rId6–9)** 만 골라 `fig_S1..S4.png` 로 등록. `figures.json` 에 `extracted_by: "docx word/media (embedded raster, not caption-crop)"` 로 표시.
- **크로핑 버그 2건 점검 결과: 이번 편에는 없다.** 2단 조판 혼입 없음 — Fig. 3·4 만 단단폭(1097 px)으로 잘렸고 이는 원문에서 실제로 단단 그림이다. 캡션 위 판형 밀림 없음 — 8장 모두 그림 본체가 온전하다. 쪽 좌표 재렌더 불필요.
- Table S1 50행·Table S2 32행은 **이미지가 아니라 docx 표 구조에서 직접** 읽었다 (더 정확).
- 검산은 전부 Table S1 원자료로 자체 재계산: R²(두 정의)·RMSE·라벨 격자·기준선.

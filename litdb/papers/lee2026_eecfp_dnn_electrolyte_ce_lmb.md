# Interpretable Enhanced-ECFP-Guided Deep Learning for Rational Electrolyte Design and Coulombic Efficiency Prediction in Lithium Metal Batteries — Lee et al. (Energy Storage Materials 2026)

> slug `lee2026_eecfp_dnn_electrolyte_ce_lmb` · DOI `10.1016/j.ensm.2026.104972` · type `exp(셀·Raman·SEM·XPS) + ML(e-ECFP/DNN/SHAP) — **자체 DFT/MD 0**` · PDF 업로드 `82ea256b/6526d3fe-LMB_________.pdf` (**사용자 직접 업로드 2026-07-17**; 업로드 경로 휘발성 → 이 digest가 self-contained 정본, inbox 복사 안 함) · digested `2026-07-17` · status ✅ · 분류 `cascade-참고/LMB`
> **저자**: Doo Bong Lee(고려대 Battery-Smart Factory, 공동1저)/**Jinwoo Park**(가천대 화공·바이오·배터리공학, 공동1저)/Eunji Kim(가천대)/**Woong Kim**(교신, 고려대 신소재 woongkim@korea.ac.kr) — Energy Storage Materials 86 (2026) 104972 (접수 2025-12-04 / 수정 2026-01-23 / 게재확정 2026-02-06 / 온라인 2026-02-07)
> **⚠ 정체 주의**: **액체 전해질 리튬금속전지(LMB) 논문** — 황화물 SE/argyrodite/ASSB 아님. litdb 보관 이유 = ① **해석가능 ML 스크리닝 워크플로**(우리 47-dopant cascade의 방법 참고) ② **LiF/Li₂O-rich 무기 SEI = 우리 wide-gap 절연 interphase 패밀리의 액체-LMB 실험판**. 물성 4축(A–D) 수치 비교 대상 아님.

---

## 0. 이 digest를 읽는 법
이 논문은 **"리튬금속전지의 쿨롱효율(CE)을 전해질 '분자 구조'로부터 예측하고, 그 예측 모델을 해석해 새 전해질을 설계할 수 있나?"** 에 답한다. 답: (a) 문헌에서 모은 **168개 Li–Cu 반쪽셀 CE 데이터**를 (b) **e-ECFP**(기존 ECFP 분자지문에 ①salt/solvent 구분 ②substructure 빈도 ③농도 가중 3가지를 추가한 표현)로 인코딩해 (c) **DNN**으로 학습(RMSE 0.16, R² 0.86)하고, (d) **SHAP**으로 열어 보니 "**용매는 불소-rich + 고리형 에터가 CE↑, 카보네이트가 CE↓; 염(salt)은 저불소화(LiFSI)가 유리**"라는 설계 규칙이 나옴 → (e) 이 규칙대로 **1 M LiFSI / MeTHF:TTE (1:3 v/v)** 를 조합하니 **CE 99.72 %**(Aurbach, Li–Cu)로 전 시험군 최고 + LFP 풀셀 1C 500사이클 97 % 유지.
핵심 기여는 새 화학이 아니라 **표현(representation)**: 기존 AI-전해질 연구가 원소 비율이나 salt:diluent 비만 쓰던 것을, "분자 substructure 단위 + 농도 가중"으로 끌어올려 **해석 가능한 구조–성능 관계**를 만든 것. 우리 입장에선 (i) cascade 위에 얹을 "surrogate+SHAP 해석 레이어"의 워크플로 견본, (ii) **음이온(FSI⁻)-유래 LiF/Li₂O 무기 SEI = 좋은 Li 계면**이라는 우리 SEI-gap 축 원리의 액체계 실험 앵커로 읽으면 된다. **자체 DFT/MD/분자시뮬레이션은 0건**(§7).

## 1. 한 줄 요약
Li–Cu 반쪽셀 CE 168건을 **농도-가중 분자지문(e-ECFP, 2×1025차원)** 으로 인코딩해 DNN(테스트 RMSE 0.16·R² 0.86)으로 학습하고 SHAP으로 해석 → **"용매 F-rich·고리형 에터 = CE↑ / 카보네이트·salt 과불소화 = CE↓"** 규칙 도출 → 규칙 최적 조합 **1 M LiFSI/MeTHF:TTE(1:3)** 가 예측 99.63 vs 실측 **99.72 %** 로 검증되고, 무 free-FSI⁻(CIP/AGG 지배 = LHCE형) 용매화 → **LiF/Li₂O-rich 무기 SEI** → 치밀·균일 Li 석출 → LFP 풀셀 1C **500사이클 97 %**·평균 CE 99.97 %로 닫힘.

## 2. 메타
| 저자 | 저널/년 | DOI | 시스템 | 연구유형 |
|---|---|---|---|---|
| D.B. Lee/J. Park(공동1)/E. Kim/**W. Kim**(교신) — 고려대(Battery-Smart Factory·신소재)+가천대 | Energy Storage Materials 86 (2026) 104972 | 10.1016/j.ensm.2026.104972 | **액체 전해질 LMB**: 1 M LiFSI(or LiPF₆/LiTFSI) in DME / MTBE:Toluene(1:1) / DBE:Toluene(1:1) / **MeTHF:TTE(1:3)**; Li–Cu 반쪽셀 + Li–LFP 풀셀 | ML(e-ECFP+Linear/RF/XGBoost/DNN+SHAP) + exp(Aurbach CE·Raman·SEM·XPS·풀셀); **DFT 0** |

- **동기/갭**: LMB는 3860 mAh/g·−3.04 V vs SHE·이론 >400 Wh/kg이지만 dead Li·덴드라이트·저CE가 병목. SEI를 좌우하는 전해질 설계는 시행착오 의존. 선행 AI 연구는 **원소 조성비**[ref 26,29]나 **LHCE의 salt:diluent 비**[ref 30]만 입력으로 써서 분자 구조·농도 효과를 놓침 → 이 논문이 그 표현 한계를 겨냥.
- **차별점(저자 주장)**: ECFP를 전해질용으로 확장(e-ECFP) — salt/solvent 카테고리 구분 + substructure **빈도**(기존 ECFP는 유/무 1/0) + **농도 가중**.

## 3. 핵심 수치 (전부)
| 항목 | 값 | 조건/비고 |
|---|---|---|
| 데이터셋 | **168개** Li–Cu 반쪽셀 CE (문헌 수집; salt+solvent+CE) | Li–Cu = cathode 효과 배제 목적 명시 |
| 표현 차원 | ECFP r=2·1024-bit → **e-ECFP 1025차원/분자**(카테고리 1 + substructure 1024, 빈도×농도 가중) → 168 × 2(salt·solvent) × 1025 | Fig 1c |
| 타깃 | **LCE = −log₁₀(1−CE)** (로그 쿨롱효율) | CE가 100 % 근방에 몰리는 것을 펼침 |
| 모델 RMSE (train/test) | Linear **0.16/3.05**(과적합 붕괴) · RF 0.21/0.22 · XGBoost 0.20/0.21 · **DNN 0.18/0.16** | 8:2 분할·grid search(Table S2)·5-fold CV(S3/S4) |
| DNN R² | train **0.83** / test **0.86** | Fig 1f |
| DNN 구조 | 은닉 8층 (256-128-64-32-16-8-4-2) + 출력 1; Leaky ReLU + BatchNorm | Python 3.11·TensorFlow |
| SHAP 선별 | 전체 2050 피처 → 용매 **22개**(양 8 + 음 14), 염 **10개**(양 5 + 음 5) | Fig 2a,b·S2·S3 |
| 예측 CE (DNN) | DME 97.41 / MTBE:Tol 99.35 / DBE:Tol 99.53 / **MeTHF:TTE 99.63 %** | RF·XGB보다 4계 모두 실측에 근접 |
| **실측 CE (Aurbach)** | DME 97.25 / MTBE:Tol 99.21 / DBE:Tol 99.44 / **MeTHF:TTE 99.72 %** | Li–Cu; Fig 3 |
| (참고) RF/XGB 예측 | DME 98.22/98.11 · MTBE 99.09/99.24 · DBE 99.04/99.22 · MeTHF:TTE 99.2/99.27 | Fig 3a |
| σ (전해질, RT) | **MeTHF:TTE(1:3) 0.816 mS/cm** ≫ DBE:Toluene **0.029 mS/cm**; TTE 분율↑→σ↓(Fig S5b) | "RT 유기전해질 전형 범위 10⁻³–10⁻² S/cm" 인용 |
| 용해도 제약 | 1 M LiFSI가 MeTHF:TTE **1:4에선 불완전 용해** → DNN 최적(1:4, Table S5) 대신 **1:3 채택** | AI 예측 밖의 실무 제약 |
| Raman FSI⁻ 배정 | free FSI⁻ **719** / CIP **731**(Li⁺ 1개) / AGG-I **745**(2개) / AGG-II **754 cm⁻¹**(>2개) — S–N–S bending | Fig 4a,b |
| 용매화 분율 | DME: free FSI⁻ **≈86 %**; MTBE·DBE:Tol: CIP+AGG 지배; **MeTHF:TTE: free FSI⁻ 0** (CIP+AGG만 = LHCE형) | Fig 4b·S7 |
| SEI 저항 | MeTHF:TTE **2.1 Ω** vs DBE:Toluene **6.9 Ω** | Fig S6 (Li–Cu) |
| Li 석출 형상 | DME 침상·다공 / MTBE·DBE 치밀화 / **MeTHF:TTE 최치밀·최균일** | SEM, 2 mAh/cm²@0.5 mA/cm² on Cu |
| SEI 조성 (XPS, 10 cyc Li) | F 1s: **LiF 전 계 공통**(FSI⁻ 유래)+C–F; O 1s: Li₂O가 DME엔 희박·**MeTHF:TTE 최강 Li₂O** (+C–O/C=O) | Fig 4d,e·S9–S11 |
| 풀셀 rate (LFP, mAh/g) | MeTHF:TTE **156/144/132/115/91** vs DME 140/132/122/107/87 @0.2/0.5/1/2/4C; DBE:Tol 143.6(0.2C)·132.2(0.5C)→1C 105.9·**2C/4C 작동 불가** | LFP 3.01 mg/cm²·3.0–3.8 V |
| 풀셀 계면저항 | DBE:Toluene **152.4 Ω** vs DME 51.1 Ω | Fig S13 (EIS) |
| 풀셀 1C 장기 | **MeTHF:TTE 133→130 mAh/g (500 cyc, 97 %)**; DME 119→109(300 cyc, 92 %)→103(500 cyc, 86 %); DBE:Tol 초기 100·**20 cyc만에 80 %**; MTBE:Tol 초기 127·74 cyc에 80 % | Fig 5d |
| 풀셀 평균 CE (50–450 cyc) | **MeTHF:TTE 99.97 > DBE:Tol 99.88 > MTBE:Tol 99.84 > DME 99.69 %** | Li–Cu 예측 서열과 동일 (저자 강조) |

## 4. 방법의 핵심 — e-ECFP 표현 (이 논문의 기여 본체)
- **바탕**: ECFP(extended-connectivity fingerprint; Morgan 지문 계열) — SMILES에서 반경 r 안의 원자 환경을 해시해 1024-bit 벡터로. 여기선 **r=2**(중심 원자에서 결합 2개까지). 케모인포매틱스/신약 표준 기법[ref 31–35]의 배터리 전용 개조.
- **기존 ECFP의 3가지 한계 → 3가지 확장**:
  1. salt와 solvent를 구분 못함 → **카테고리 피처 1개** 추가(salt/solvent 플래그).
  2. substructure **유/무(1/0)만** 기록 → **빈도(개수)** 인코딩 (반복 모티프·분자 내 중복 환경 반영).
  3. **농도 정보 없음** → 각 피처 벡터에 **해당 salt/solvent 농도를 곱함**(조성 효과).
- 결과: 분자당 1025차원, 전해질 = (salt 벡터, solvent 벡터) 쌍 → 데이터셋 168×2×1025.
- **타깃 변환**: CE(%) 대신 **LCE = −log₁₀(1−CE)** — CE가 100 %에 붙어 dynamic range가 죽는 것을 로그로 펼침(선행 [ref 26,30] 관례). 고CE 영역 분해능↑.
- **피처 표기법**: "P5. C [CCC ring] (r = 1)" = 양(positive) 5위, 중심 원자 C, 반경 1 내 SMILES 모티프 CCC(고리 내). 이 표기가 Fig 2 전체의 문법.
- ⚠ **이진/다성분 용매 인코딩**: MeTHF:TTE처럼 용매 2종인 계를 "solvent 벡터 1개"로 어떻게 합치는지(농도 가중 합으로 추정) 본문에 명시가 얇음 — 세부는 SI Table S1 의존(§13).

## 5. 결과 — 섹션별 상세

### 5.1 데이터 구축·모델 훈련·평가 (§2.1, Fig 1)
- 168개 전해질(문헌)을 SMILES→ECFP→e-ECFP로 전처리. **Li–Cu 반쪽셀만** 수집한 이유: cathode 기여를 제거해 "전해질→Li 도금/탈리 가역성" 인과만 남기기 위해(명시).
- 4개 모델 비교: **Linear는 train 0.16→test 3.05로 붕괴**(심한 과적합·일반화 실패), 트리 앙상블(RF 0.21/0.22·XGB 0.20/0.21)은 균형, **DNN이 0.18/0.16·R² 0.83/0.86으로 최고**. 하이퍼파라미터 grid search(Table S2), 5-fold 교차검증(Table S3/S4)으로 강건성 확인. 이후 예측·설계는 전부 DNN.
- (비판 메모: test RMSE(0.16) < train(0.18)은 소표본에서 분할 운/강한 정규화 신호 — 5-fold가 방어이긴 함. §13.)

### 5.2 SHAP 해석 → 설계 규칙 (§2.2, Fig 2)
**용매 (2050 피처 중 상관 최강 22개: 양 8 / 음 14)**
- **양(Fig 2a,c,d)**: P1. F [F] (r=0) **최상위**; P2. F [CF] C with 0 H (r=1); P3. C [C] with 0 H (r=0); P4. F [CF] C with 1 H (r=1) — **불소 계열**. P5. C [CCC ring] (r=1); P7. O [COC ring] (r=1) — **고리형 에터**. P6. O [COC] (r=1); P8. O [COC] C with 2 H (r=1) — 선형 에터 모티프(양이지만 약함/때로 음).
- **음(Fig 2b)**: N1. O [O] double bond O (r=0); N2. O [CCOC(=O)O ring] (r=2) 등 **카보네이트 모티프(N1·N2·N4·N7·N8·N12·N13)가 최음(最陰)**; N5·N6·N7·N9는 **선형 에터** 유래, N11·N14는 고리형 에터 유래지만 덜 해로움.
- **기전 해석(저자)**: F의 강한 전자당김이 배위 자리 극성↓ → **Li⁺–용매 상호작용 약화** → Li⁺가 음이온과 더 배위 → **음이온 유래 무기 SEI(LiF·Li₂O) 형성 촉진**[refs 16,37–40].
- **설계 규칙 2줄**: (i) **불소-rich 구조 = CE에 크게 유리**, (ii) **고리형 에터 > 선형 에터 > 카보네이트**.
- **용매 선정**: 규칙 (i)→ **TTE**(1,1,2,2-tetrafluoroethyl 2,2,3,3-tetrafluoropropyl ether; F 8개 불소화 에터 희석제), 규칙 (ii)→ **MeTHF**(2-methyltetrahydrofuran; 고리형 에터).

**염 (10개: 양 5 / 음 5; LiPF₆ vs LiTFSI vs LiFSI)**
- 양: S-P1. O [O=S] (r=1)·S-P2. O [O] (r=0) — **산소 모티프**(LiFSI·LiTFSI에 있고 LiPF₆에 없음); LiFSI 고유 S-P3. F [FS] (r=1)·S-P4. S [O=S(=O)(F)[N⁻]S] (r=2)·S-P5. S [S(=O)(=O)F] (r=1).
- 음: **S-N1. F [F] (r=0)의 빈도** — F 6개짜리 염(LiPF₆·LiTFSI)이 F 2개인 LiFSI보다 해로움; S-N3. F [FP] (r=1)=LiPF₆; S-N2. F [CF]·S-N4(TFSI의 CF₃)·S-N5=LiTFSI.
- **🔑 뉘앙스**: **용매의 F는 많을수록 좋고, 염의 F는 적을수록 좋다** — 같은 원소가 역할(비배위 희석 vs 음이온 안정성/분해화학)에 따라 부호가 뒤집힘. SHAP이 이 비대칭을 자동으로 잡아냈다는 게 표현력의 증거. → **염 = LiFSI** 선정.

**조성 확정**: DNN 최적은 MeTHF:TTE **1:4**(Table S5)였으나 **1 M LiFSI가 1:4에선 완전 용해 안 됨**(Fig S5a) → 용해되는 최대 TTE 분율 **1:3** 채택. σ는 TTE↑에 따라 감소(Fig S5b)하나 1:3에서 **0.816 mS/cm** — MTBE:Toluene(1:1)·DBE:Toluene(1:1)류 고CE 전해질보다 높고 RT 유기전해질 전형 범위(10⁻³–10⁻² S/cm) 내.

### 5.3 Li–Cu 검증 + 계면 분석 (§2.3, Fig 3·4)
- **Aurbach CE**(프로토콜 §6): 실측 서열 MeTHF:TTE **99.72** > DBE:Tol 99.44 > MTBE:Tol 99.21 > DME 97.25 % — DNN 예측 서열·수치와 정합(DNN이 RF/XGB보다 저RMSE·고R²; DBE>MTBE 서열도 DNN만 맞힘).
- **Raman 용매화**(FSI⁻ S–N–S 밴드 4분해, 719/731/745/754 cm⁻¹): DME는 free FSI⁻ ≈86 %(강용매화) ↔ **MeTHF:TTE는 free FSI⁻ 0·CIP+AGG 지배** = **약용매화/LHCE형**(TTE=약배위 희석제, MeTHF 내 LiFSI 국소 농축 도메인). "free 음이온 부재 + CIP/AGG 고분율"이 우선적 음이온 환원→**음이온 유래 SEI**→고CE의 기전 설명.
- **SEM**(Cu 위 2 mAh/cm²@0.5 mA/cm²): DME 침상·다공(불균일 Li⁺ flux) → MTBE/DBE 치밀화 → **MeTHF:TTE 최치밀·최균일**. "치밀·평탄 석출 = 전해질 분해 억제·계면 안정"[refs 7,45,46].
- **XPS**(10사이클 Li 표면): F 1s에서 **LiF 전 계 공통**(FSI⁻가 LiF-rich SEI의 공통 원천[refs 50,51]); O 1s에서 **Li₂O가 MeTHF:TTE 최강**(DME엔 희박) — CIP/AGG 고분율이 FSI⁻ 환원→Li₂O-rich SEI를 촉진[refs 16,52]. **LiF+Li₂O 공존 SEI = 기계적 견고 + 균일 Li⁺ 수송 → 덴드라이트·기생반응 억제**[refs 3,53–56].

### 5.4 Li–LFP 풀셀 (§2.4, Fig 5)
- LFP 3.01 mg/cm²(LFP:SuperP:PVDF 8:1:1), 3.0–3.8 V, 0.1C 활성화 2사이클.
- **Rate**: MeTHF:TTE가 전 C-rate 최고(156→91 mAh/g @0.2→4C). DBE:Toluene은 저율(0.2/0.5C)에선 DME보다 낫지만 **1C부터 붕괴·2C/4C 작동 불가** — 원인 = σ 0.029 mS/cm + 풀셀 계면저항 152.4 Ω(vs DME 51.1 Ω).
- **1C 500사이클**: MeTHF:TTE **97 % 유지**(133→130) ≫ DME 86 % > MTBE:Tol(74 cyc에 80 %)·DBE:Tol(20 cyc에 80 %). 평균 CE(50–450 cyc) 서열 **99.97/99.88/99.84/99.69 %** = Li–Cu 예측 서열 재현(저자: "모델은 Li–Cu만 배웠는데 풀셀 CE 서열이 재현됨").
- **🔑 비판적 관찰(우리 메모)**: **CE 서열 ≠ 용량 유지 서열** — DBE:Tol(CE 99.88)이 유지율 꼴찌, DME(CE 99.69)가 2위. 톨루엔 희석 계는 CE는 높아도 σ·계면저항이 rate/분극을 죽임. **MeTHF:TTE만 CE와 σ를 동시에 잡아서 이김** — "CE 단일 타깃 최적화는 불충분, 전도도 제약 동시 필요"가 이 논문 데이터 자체가 주는 교훈(저자는 명시적으로 일반화하지 않음). §11 cascade 시사점.

## 6. 실험 방법 (재현용)
- **Aurbach CE 프로토콜**[ref 42]: ① Cu에 Li 0.5 mA/cm²로 5 mAh/cm² 도금→1.0 V까지 탈리(전처리) ② 다시 5 mAh/cm² 도금 ③ 0.5 mA/cm²·1 mAh/cm²로 10회 도금/탈리 ④ 최종 1.0 V까지 전량 탈리 → CE = 총 탈리량/초기 도금량(전처리 제외).
- **재료**: LiFSI 99.9 %·DME 99.5 %·MeTHF 99 %·TTE 99 %·LFP·NMP·PVDF(Sigma-Aldrich); DBE 99 %·MTBE 99 %(TCI); Super P(Alfa Aesar); Toluene 99.5 %(Duksan). 유기용매 4 Å 분자체 48 h 건조. Ar 글러브박스(O₂·H₂O <0.1 ppm)에서 조액.
- **셀**: CR2032; Celgard 2325; 전해질 50 μL; Li foil 150 μm/Cu 25 μm/Al 15 μm. Li–Cu: Li φ14+Cu φ16; Li–LFP: Li φ16+LFP φ14. LFP 전극 = 슬러리 doctor blade 100 μm→60 °C 건조, 3.01 mg/cm².
- **분석**: σ = 전도도미터 CPC-511; Raman = Renishaw Invia 532 nm·500–2000 cm⁻¹; FE-SEM = Hitachi SU5000(밀폐 이송); XPS = ULVAC-PHI VersaProbe 5000, Al Kα 1486.6 eV, C 1s 284.8 eV 보정.
- **ML 구현**: Python 3.11 — scikit-learn/XGBoost/Pandas/NumPy/TensorFlow/Matplotlib; RMSE·R² 정의 명시; SHAP으로 해석.

## 7. DFT/계산 방법 ★ (정직 버전)
- **code/functional/pseudo/k-points/ecut/supercell/DFT+U/AIMD/MLIP/무질서 처리: 전부 없음 (n/a)** — 제일원리·고전 MD·용매화 시뮬레이션 0건. 용매화 구조 주장은 전적으로 Raman 분해(실험), SEI 주장은 XPS(실험) 기반.
- "계산"의 실체 = **데이터 기반 통계 학습**: e-ECFP 인코딩(§4) + Linear/RF/XGBoost/DNN 회귀 + SHAP 사후 해석. 물리 시뮬레이션이 아니라 **표현공학 + surrogate 모델**.
- 따라서 이 논문의 수치는 전부 **실험 소환값 또는 ML 예측값** — 우리 DFT db와 어떤 축에서도 수치 혼용 금지.

## 8. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1a–c | 데이터 구축 도식: 168 Li–Cu → SMILES → 표준 ECFP(1024 binary) → **e-ECFP(2×1025; salt/solvent 구분·빈도·농도 가중)** | **"표현 3확장" 도식** — cascade 피처 설계(카테고리+농도 가중) 발상의 시각 견본 |
| 1d–f | 모델 4종 훈련 → RMSE 비교(Linear test 3.05 붕괴) → DNN 산점도(R² 0.83/0.86) | **소표본(n=168) 모델 선택 교훈**: Linear 붕괴·트리 준수·DNN 소폭 우위 — 우리 n=47엔 트리+SHAP이 현실적이라는 반면교사 |
| 2a,b | SHAP beeswarm: 용매 양 8(P1–P8)/음 14(N1–N14) substructure | **SHAP 서열화 플롯 양식** — cascade design-rule 추출 그림의 표준 포맷 |
| 2c,d | CE-증진 substructure 구조식: F-계열(P1/P2/P4) vs 고리형 vs 선형(P5/P7 vs P6/P8) | "피처→화학 직관" 번역 패널 — 해석가능성 주장의 핵심 |
| 2e,f | 선정 용매 구조: TTE(F-rich 에터)·MeTHF(고리형 에터) | 규칙→분자 선정의 연결 고리 |
| 3a | 4계 × (RF/XGB/DNN/실측) CE 막대 | DNN만 DBE>MTBE 서열 정답 — 모델 간 차이가 서열 수준에서 드러나는 사례 |
| 3b | Aurbach 전압–시간 곡선(4계 중첩, CE 라벨) | Aurbach 프로토콜 시각화 |
| 4a,b | Raman FSI⁻ S–N–S 4분해(719/731/745/754 cm⁻¹) + 면적 분율 막대 | **free FSI⁻/CIP/AGG-I/AGG-II 배정표** — 용매화 정량의 관례; DME 86 % free vs MeTHF:TTE 0 |
| 4c | Li 석출 SEM(50 μm 스케일, 3계): 침상·다공 → 치밀 → 최치밀 | 형상–CE 상관의 직관 증거 |
| 4d,e | XPS F 1s(LiF/C–F)·O 1s(Li₂O/C–O/C=O) 3계 비교 | **LiF+Li₂O-rich SEI = 좋은 Li 계면** — 우리 wide-gap 절연 interphase 패밀리의 액체판 실험 앵커 |
| 5a–c | LFP 풀셀 rate(0.2–4C) + 충방전 프로파일(DME vs MeTHF:TTE) | DBE 계 1C 붕괴 = "CE만으론 부족, σ 동시 필요"의 데이터 |
| 5d | 1C 500사이클 용량+CE(4계) | MeTHF:TTE 97 %·평균 CE 99.97 % — 헤드라인 |
| SI(언급) | S1 데이터셋·S2 하이퍼파라미터·S3/S4 5-fold·S5 용해도/σ/조성별 예측 CE·S6 SEI 저항·S7 Raman 분율·S8 SEM·S9–S11 XPS·S12 MTBE/DBE 풀셀·S13 풀셀 EIS | SI 미보유 시 수치 인용은 본문 언급분까지만 |

## 9. Post-processing ★
- **SHAP (SHapley Additive exPlanations)**: 학습된 DNN의 피처 기여도를 게임이론적으로 분해 — beeswarm(피처값 색·SHAP값 x축)으로 양/음 substructure 서열화. 2050 피처→22(용매)+10(염) 선별.
- **LCE 변환**: −log₁₀(1−CE) — 상한 포화 지표의 로그 펼침(회귀 타깃 공학).
- **Raman 곡선분해**: FSI⁻ S–N–S bending 700–780 cm⁻¹를 4밴드(719/731/745/754)로 피팅→면적 분율(용매화 상태 정량). (피팅 제약조건 미기재 — §13.)
- **XPS 피팅**: F 1s(LiF/C–F), O 1s(Li₂O/C–O/C=O) 성분 분해; C 1s 284.8 eV 보정.
- **Aurbach 정량**: 전처리 제외 총탈리/초기도금 비 — CE 측정의 표준화 프로토콜.
- 도구: Python 3.11 스택(§6); 분광 피팅 소프트웨어 미명시.

## 10. 우리 DFT 대비 (comp1/modelc/+B₂O₃/LPSOCl) → `../our_dft_baseline.md`
| 항목 | 이 논문 (액체 LMB) | 우리 (황화물 SE DFT) | 판정 |
|---|---|---|---|
| **시스템** | 액체 유기 전해질 + Li 금속 | 황화물 SE(comp1 Li₆PS₅Cl/modelc Cl1.6/+B₂O₃/LPSOCl) 결정 | **직접 비교 불가** — 물성 4축(A–D) 어느 행에도 수치로 넣지 않음 |
| **SEI 설계 원리** | **음이온(FSI⁻) 유래 LiF+Li₂O-rich 무기 SEI → 치밀 Li·덴드라이트 억제·CE 99.72 %** (XPS+SEM 실측) | sei_products.json: **wide-gap 절연 산물(LiCl 6.65·Li₃PO₄ 5.73·Li₂O 5.24 ≫ Li₂S 3.90 eV)이 좋은 interphase** — B₂O₃/O-doping cascade의 SEI-gap 축 | **✓ 같은 설계 원리의 두 시스템**: 그들 = 액체 처방(용매화 제어)으로 LiF/Li₂O를 *만들고*, 우리 = 도펀트로 분해산물을 wide-gap 쪽으로 *조향*. [KimICCF](FEC→LiF)·[Li25](LiCl/LiBr)·[Lu](LiCl)·[Ke](Li₂O)에 이은 **패밀리 +1(액체-LMB판)**. 단 gap 수치는 우리 계산값이고 이 논문엔 gap 개념 자체가 없음 — 개념 정렬만 |
| band gap / VBM / ESW / σ_e | n/a (전자구조 0) | comp1 2.066/modelc 2.099/+B₂O₃ 1.9671/LPSOCl 2.2309 eV (fixed-occ nscf) | 비교 대상 없음 |
| 산화 onset (축 B①) | n/a — 대신 **저전압 LFP(3.0–3.8 V) 한정** 시스템(에터 전해질의 산화 한계는 논의 자체가 없음) | grand-potential onset 2.256 V (S²⁻-limited) | 비교 불가. 단 "에터계가 고전압 양극 못 가는 것"과 "황화물이 S-limited인 것"은 각자 시스템의 산화 천장 — 등치 금지 |
| σ (이온전도) | 전해질 σ 0.816 mS/cm(RT 실측, 액체) | 우리 σ는 MLIP-MD **비율만**(절대값 인용 금지 규율) | 수치 비교 금지. 소환용 한 줄: "액체 LHCE급 0.8 mS/cm ↔ argyrodite 실측 1–10 mS/cm(문헌)"처럼 **문헌끼리** 차수 비교만 가능 |
| **CE 지표** | Li–Cu Aurbach CE 99.72 %·풀셀 평균 99.97 % | 대응 계산량 없음(셀 지표) — 우리 cascade엔 CE 축 없음 | **벤치마크 소환값**: ASSB(우리 재료가 갈 곳)가 넘어야 할 액체 최고급 수준의 감각 앵커 |
| **방법 철학** | Li–Cu 반쪽셀로 **cathode 변수 배제**(전해질→Li 인과 고립) | 우리 "축 분리" 규율(산화 4축 명명·ESW는 S-limited 축① 명시) | ✓ **변수 고립 철학 공유** — 인용 시 "그들도 축을 분리해 측정" 정도의 방법 유비만 |
| **스크리닝 방법** | 데이터(n=168) 기반 **통계 surrogate + SHAP 해석** — 입력=분자 구조·농도, 물리 없음 | **DFT 계산 물리 지표 기반 결정론적 cascade**(47 dopant × 산화 onset/SEI gap/σ/blocking) — 데이터 불요, 물리 있음 | **상보적**: 그들의 약점(물리 부재·데이터 노이즈)=우리의 강점, 그들의 강점(해석 레이어·표현공학)=우리가 이식 가능(§11a). "AI가 DFT를 대체"가 아니라 "cascade 출력 위 해석층" |
| 무질서/열/수분 축 | n/a | BVSE·Th′([Wang22])·ΔG_hyd([Zhu20]) 등 | 이 논문은 무기여 |

## 11. 적용 인사이트 (내 연구에 어떻게)

### 11a. ★ cascade 적용성 평가 (특별 주문 — a/b/c)
**(a) cascade에 넣을 만한 새 축/서술자가 있나? → 물리 축으론 없음, '메타 레이어' 2개는 있음.**
- **새 물리 축 없음**: CE는 액체 셀 수준 지표라 SE 벌크/계면 서술자로 환산 불가. "SEI 무기물 분율(LiF/Li₂O-rich)"이라는 관측량 개념은 있지만, 우리 cascade의 **SEI/분해상 gap 축이 이미 그 계산 대리(proxy)** — 새 축이 아니라 기존 축의 개념 보강으로 흡수.
- **메타 레이어 ①: surrogate+SHAP 해석층**. cascade가 이미 산출한 47-dopant × 축별 점수를 훈련 데이터로, 도펀트 원소 서술자(전기음성도·이온반경·산화수·HSAB softness·ICOHP류)를 입력으로 하는 가벼운 모델(RF/XGBoost)을 학습하고 SHAP으로 열면 → **"어떤 도펀트 성질이 어떤 축을 끌어올리나"의 정량 design rule**이 나옴. 이 논문의 Fig 2 워크플로 그대로. 논문/deck에서 "cascade 결과의 해석 가능한 요약"으로 쓸 수 있는 부가 산출물.
- **메타 레이어 ②: LCE형 로그 변환**. 상한 포화 지표(0~1 경계의 blocking fraction, 유지율 %, 채널 % 등)를 회귀/시각화할 때 −log₁₀(1−x) 변환 검토 — 이 논문이 CE 100 % 포화를 다룬 방식.
- **부수 교훈(축 설계)**: §5.4의 "CE 서열 ≠ 유지율 서열"(DBE:Tol CE 2위·유지율 꼴찌) = **단일 축 최적화의 함정** 실증 — 우리 cascade가 σ축을 안정성 축들과 *동시에* 들고 가는 설계(다축 동시 스크리닝)의 외부 정당화 사례로 인용 가능.

**(b) 기존 축의 문헌 anchor로 쓸 값 → 전부 '개념/벤치마크' 수준, 축 수치 anchor는 없음.**
- **SEI/분해상 gap 축 (개념 anchor)**: "FSI⁻ 유래 **LiF+Li₂O-rich 무기 SEI → 치밀·균일 Li, CE 99.72 %, 덴드라이트 억제**"(Fig 4d,e+SEM) — 우리 wide-gap 절연 interphase 패밀리(LiCl/Li₂O/Li₃PO₄/LiF)의 **액체-LMB 실험판**. 정성 인용 전용(액체계·gap 수치 없음).
- **CE 벤치마크 (소환값)**: Li–Cu Aurbach **99.72 %**·LFP 풀셀 평균 **99.97 %**(50–450 cyc) — "액체 LMB 최고급 CE 수준"의 숫자 감각용. ASSB 셀 성능 논의 시 대조 기준으로만.
- **σ 소환값**: LHCE급 액체 **0.816 mS/cm**(RT)·"RT 유기전해질 전형 범위 10⁻³–10⁻² S/cm" — 황화물 SE(문헌 실측 1–10 mS/cm)와 **문헌끼리** 차수 비교하는 서사("SE가 액체와 같은 차수")에 사용 가능. 우리 MLIP 절대 σ와는 혼용 금지.
- **산화 onset·열·수분·Li-blocking 축**: 이 논문에서 얻을 anchor **없음**(전부 n/a).

**(c) 방법 이식 비용 → SHAP 레이어는 ~0, e-ECFP 자체는 이식 불가.**
- **surrogate+SHAP 레이어**: 입력 = **이미 계산된 cascade 산출물 + 조성/원소 서술자(추가 DFT 0)** → 비용 사실상 0(로컬 Python 몇 시간; shap 패키지). 단 **n=47 ≪ 168** — 이 논문의 Linear 붕괴(test RMSE 3.05)가 경고: 소표본엔 DNN 비권장, **트리 기반(RF/XGB)+SHAP** 또는 SHAP 대신 permutation importance가 현실적. 교차검증 필수.
- **e-ECFP 자체**: SMILES 기반 **분자 전용** 지문이라 무기 결정 도펀트에 직접 적용 **불가**. 무기판 대응물은 이미 우리가 보유한 원소/자리 서술자 벡터([Wang22] Th′류 다면체 카운팅·ICOHP 가중이 같은 정신). 다만 e-ECFP의 3확장 중 **"카테고리 구분(양이온/음이온 도펀트) + 농도(x) 가중"** 발상은 우리 피처 설계에 이식 가능.
- **실험 CE DB 구축**(그들의 168개에 해당): 우리 파이프라인 범위 밖·불필요. 만약 언젠가 "argyrodite 도핑 문헌 σ/CCD DB → ML" 방향을 열면 이 논문이 워크플로 원형이 되지만, 그건 별도 프로젝트.

### 11b. 그 외
1. **wide-gap SEI 패밀리 서사 완성도↑**: 우리 "전자절연 분해산물 = 좋은 interphase" 주장이 이제 ASSB 실험([KimICCF]/[Li25]/[Lu])+계산([Sundar])에 더해 **액체 LMB 최적화의 도착점도 같다**(LiF/Li₂O)는 교차-시스템 수렴 증거를 가짐 — deck 한 줄: "액체든 고체든, 좋은 Li 계면의 답은 무기 wide-gap SEI로 수렴한다."
2. **해석가능성 프레임 차용**: 우리 cascade 논문/deck에서 "blackbox AI 스크리닝 대비 우리는 물리 지표 기반"이라고 대비시킬 때, 이 논문처럼 **AI 쪽도 SHAP으로 해석층을 얹는 추세**임을 인지하고 서술(일방적 폄하 금지) — 정확한 대비는 "데이터-표현 학습 vs 제일원리 지표", 둘 다 해석 가능.
3. **국내(고려대·가천대) AI-배터리 그룹 좌표**: Woong Kim 그룹 — 향후 AI-스크리닝 관련 국내 협력/인용 맥락에서 참조점.

## 12. 인용 가능 문장 (deck/paper용)
- "An interpretable deep-learning study on 168 Li–Cu half-cell datasets (Lee et al., Energy Storage Mater. 2026) converged on the same interface design principle we compute for sulfide SEs: fluorine-rich, weakly solvating electrolytes win because they template an anion-derived, LiF/Li₂O-rich inorganic SEI — the liquid-electrolyte counterpart of our wide-gap decomposition-product criterion."
- "SHAP analysis of the trained model recovered chemically transparent rules — fluorinated and cyclic-ether motifs raise Coulombic efficiency while carbonate motifs and over-fluorinated salts lower it — demonstrating that surrogate-model interpretation layers can turn screening outputs into design rules (a workflow directly transferable to our 47-dopant cascade results)."
- "Their best AI-designed electrolyte (1 M LiFSI in MeTHF:TTE 1:3) reached 99.72 % Li–Cu CE, but the runner-up in CE (DBE:toluene, 99.44 %) failed fastest in full cells due to 0.029 mS/cm conductivity — an experimental reminder that single-objective screening without a transport axis is insufficient."

## 13. 주의/한계 (over-claim 방지) — 비판적으로
- **⚠ 시스템 불일치(최우선)**: 액체 전해질 LMB — 우리 황화물 SE 4축(A–D) 어디에도 수치 편입 금지. SEI 논의도 "개념 패밀리" 수준까지만.
- **데이터 라벨 노이즈**: 168개 CE가 **문헌 수집값** — CE는 전류밀도·면적용량·Cu 전처리·프로토콜(Aurbach 여부)에 강하게 의존하는데, **프로토콜 정규화/필터링 언급이 없음**. 서로 다른 조건의 CE를 한 타깃으로 섞었을 가능성 → 모델이 배운 것의 일부는 측정 관례일 수 있음.
- **피처 누락 변수**: 입력이 salt+solvent 구조·농도뿐 — **첨가제(FEC 등)·온도·전류밀도·염 농도 외 조건**이 전부 빠짐. "전해질 조성만으로 CE 결정"이라는 암묵 가정.
- **다성분 용매 인코딩 불투명**: MeTHF:TTE 같은 2용매계를 "solvent 벡터 1개"로 합치는 규칙이 본문에 불명(농도 가중 합 추정) — 재현하려면 SI Table S1 필요.
- **소표본 대비 과대 모델**: 훈련 ~134개에 은닉 8층 DNN — 트리(0.21–0.22) 대비 이득이 0.05–0.06 RMSE 수준으로 **소폭**. test(0.16)<train(0.18)도 분할 운 가능성(5-fold가 부분 방어). "DNN이 최고"보다 "표현(e-ECFP)이 본체, 모델 선택은 부차"가 공정한 독해.
- **설계 규칙의 신규성 제한**: F-rich 희석제(TTE)·약용매화 에터·LiFSI·LHCE는 **이미 확립된 커뮤니티 지식**(refs 8–19; MTBE/DBE도 선행 ref 26) — SHAP은 이를 *재발견+정량 서열화*한 것. "AI가 새 화학을 발견"이 아니라 "알려진 규칙의 데이터 기반 확인"으로 인용해야 안전. 최종 전해질도 기지 성분의 재조합.
- **용해도는 모델 밖**: DNN 최적 1:4가 실제론 용해 불가 — AI 설계가 물성 제약(용해도·점도·안전성)을 못 보므로 수동 보정 필요(저자도 정직하게 보고). 스크리닝 파이프라인 일반의 교훈.
- **풀셀 검증의 관대함**: LFP 3.01 mg/cm²(~0.5 mAh/cm²급 저로딩)·저전압창(3.0–3.8 V)·**Li 150 μm 대과잉**(N/P 미보고·lean 조건 없음) — CE 99.72 %로도 Li 과잉이면 500사이클은 쉬움. 고로딩·제한-Li·고전압(에터 산화 한계) 일반화는 미검증.
- **CE↔유지율 불일치**: DBE:Tol(CE 99.88 %)이 유지율 최악, DME(99.69 %)가 2위 — CE 단일 지표의 한계를 저자 데이터가 스스로 보임(§5.4). "CE 서열 재현" 강조 문장을 유지율까지 확장 인용하지 말 것.
- **분광 정량 관례**: Raman 4밴드 분해(719–754 cm⁻¹ 중첩 창)의 피팅 제약 미기재; XPS "LiF 최고 상대강도" 류는 반정량. free FSI⁻ 86 % 같은 분율은 피팅 의존.
- **계산 0**: 용매화 구조·SEI 형성 기전의 원자단위 검증(MD/DFT) 없음 — 기전 서술은 문헌 인용+분광 정합 수준.

## 14. 기법 용어 미니사전
- **CE / LCE**: 쿨롱효율(탈리 전하/도금 전하) / LCE=−log₁₀(1−CE) — 100 % 포화를 로그로 펼친 회귀 타깃 (CE 99 %→LCE 2, 99.9 %→3).
- **Aurbach 프로토콜**: 전처리 도금-탈리 후 "저장분 도금→부분 사이클 n회→전량 탈리"로 평균 CE를 표준화 측정하는 방법(ref 42).
- **ECFP / e-ECFP**: extended-connectivity fingerprint — SMILES에서 반경 r 내 원자 환경을 해시한 고정길이 분자지문(케모인포매틱스 표준) / 여기에 salt-solvent 카테고리·substructure 빈도·농도 가중을 더한 이 논문의 확장판(1025차원/분자).
- **SHAP**: SHapley Additive exPlanations — 학습 모델의 예측을 피처별 기여로 가법 분해하는 게임이론적 해석법; beeswarm 플롯으로 피처 서열화.
- **LHCE**: localized high-concentration electrolyte — 약배위 희석제(TTE 등)로 국소 고농축 염 도메인을 만드는 전해질; 겉보기 농도는 낮아도 음이온 배위 유지.
- **free FSI⁻ / CIP / AGG-I / AGG-II**: FSI⁻ 음이온의 배위 상태(Li⁺ 0/1/2/>2개) — Raman S–N–S bending 719/731/745/754 cm⁻¹로 판별. free↓·AGG↑일수록 음이온 유래(무기) SEI 형성에 유리.
- **음이온 유래 SEI (anion-derived SEI)**: 용매 대신 음이온(FSI⁻)이 우선 환원돼 만든 LiF/Li₂O 등 무기물 위주 SEI — 기계적 견고·전자절연·균일 Li⁺ 수송으로 고CE의 통설적 기반.
- **dead Li**: 탈리 중 전기적으로 고립된 Li 조각 — CE 손실의 주범.
- **RMSE / R²**: 회귀 표준 지표(잔차 제곱평균 제곱근 / 결정계수).

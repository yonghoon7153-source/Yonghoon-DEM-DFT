# Machine learning pipelines for the design of solid-state electrolytes — Jain, Wang & You (Materials Horizons 2026)

> slug `jain2026_ml_pipelines_solid_state_electrolyte_design` · DOI `10.1039/d5mh01525a` · type `review (자체 계산 0 · 실험 0)` · PDF `386c01ae-77…pdf` + SI `4b4d549e-77. Sup…pdf` · digested `2026-09-09` · status ✅
> elements: Li, Na, Mg, Ca, Zn, Al, P, S, Cl, O
> methods: DFT, AIMD, MD, MLIP, NEB, DOS, BVSE, elastic, phonon, ESW
> **저자**: Vinamr Jain, Zhilong Wang, **Fengqi You\*** (Cornell — College of Engineering / AI for Science Institute / CAISI) · *Mater. Horiz.* **13**(1), 15–44 (2026) · 접수 2025-08-09 / 수락 2025-11-14 / 게재 2025-11-15 · CC-BY 4.0
> 🧭 **읽는 용도**: 우리 273 도펀트 캐스케이드(Stage 00–12) 재설계의 **구조 대조 기준**. 물성값 소환용이 **아니다**.

---

## 0. 이 digest 를 읽는 법 — ⚠ 리뷰 논문 규율

이 논문은 **리뷰다.** 자체 DFT·MD·실험이 **0건**이고, 아래 수치는 전부 **원 논문에서 리뷰가 옮겨 적은 2차 인용**이다.
그래서 이 digest 는 두 층을 **문법으로 분리**한다:

| 표기 | 뜻 | 우리 쪽 취급 |
|---|---|---|
| **[리뷰 경유]** | 리뷰가 원 논문에서 옮긴 수치 | ⛔ **우리 표에 1차 근거로 못 쓴다.** 쓰려면 원 논문 PDF 를 따로 먹여야 한다 |
| **[리뷰 주장]** | 리뷰 저자가 직접 세운 판단·권고·분류 | ⭕ 인용 가능 — 단 *"You 그룹의 리뷰 판단"* 이라고 귀속 |
| **figure-read ≈** | 내가 그림 눈금에서 읽은 값 | ⭕ 단 근사 표기 유지 |

⚠ **이 논문에 σ·Ea·gap 의 "이 논문 값" 은 하나도 없다.** 그래서 §3(핵심 물성) 은 **역할이 다르다** — 물성표가 아니라
**"이 분야가 무엇을 보고량으로 삼는가" 의 목록**이다. `comparison_vs_ours.md` 의 A–D 물성 4축 표에는 **넣지 않는다**
(→ `J-7 방법 원전` 블록 행).

---

## 1. 한 줄 요약

SSE 발견의 ML 파이프라인을 **데이터 → 서술자 → 모델 → 응용** 4단으로 정리하고, 그 위에 저자들이 세운
**다섯 가지 상호연결 난제**(① 데이터 부족 ② 다목적 최적화 ③ 해석가능성 ④ 전이·일반화 ⑤ 생성 설계)를 얹어
각각에 대응하는 ML 해법을 매핑한 **로드맵형 리뷰**다. 우리에게 값진 것은 결론이 아니라 **그 안에 나열된
20편 남짓의 실제 스크리닝 캠페인의 깔때기 모양(입력수 → 각 단 → 최종 후보수)** 이다.

**우리 결론 한 줄**: 이 리뷰는 **깔때기의 *모양*은 표준화했지만 깔때기의 *성능*(단별 제거율·순서 정당화·hit rate·
group-out 검증)은 하나도 표준화하지 못했다.** 정확히 그 빈칸이 우리가 설 자리다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 유형 | **Review** (RSC *Materials Horizons*, "Review Article" 표지 논문) |
| 분량 | 본문 30 pp (15–44) · Fig **5장 전부 개념도** · Table **4** · refs **226** · SI 9 pp (Table S1–S3, refs 41) |
| 자체 계산/실험 | **0건** |
| 선언한 차별점 [리뷰 주장] | ① 난제↔AI해법의 **첫 체계적 매핑** ② Li 편중을 깨고 **다가이온(Mg²⁺·Ca²⁺·Zn²⁺·Al³⁺) 데이터 공백**을 정면으로 다룸 ③ 전통 계산(DFT/MD/KMC) ↔ ML **하이브리드 워크플로** ④ 기법 나열이 아니라 **실행 권고**(데이터 수집 우선순위·검증 전략·XAI 적용법) |
| 자금 | Eric and Wendy Schmidt AI in Science Postdoctoral Fellowship (Schmidt Sciences) |
| ⚠ 명시 | *"Claude 4.5 and Gemini 2.5 were used to improve the clarity of selected manuscript sections"* — 저자 검토 선언 있음. §10 에서 이것과 실제 결함의 관계를 다룬다 |

---

## 3. 이 분야가 무엇을 "보고량" 으로 삼는가 ★ (사용자 질문 5)

### 3.1 리뷰가 명시한 SSE 합격 기준 [리뷰 주장, §4.1 + §5.2]

| 물성 | 리뷰가 적은 목표값 | 어디 |
|---|---|---|
| **이온전도도 σ** | *"often targeting **>1 mS cm⁻¹** at room temperature"* (§4.1 서두) | §4.1 |
| **이온전도도 σ** (다른 곳) | *"typically targeted to be **≥10⁻⁴ S cm⁻¹** at room temperature"* (§5.2) | §5.2 |
| **ESW** | *"ideally **>5.5 V** vs. Li/Li⁺ for high-voltage applications"* | §5.2 |
| **전극 적합성** | 정성 — 음극(Li 금속)·양극 양쪽에 화학/전기화학 반응 최소 | §5.2 |
| **기계** | dendrite 억제 + 전극 부피변화 견딤 + 계면 접촉 유지 (수치 없음) | §5.2 |
| **전달수 t_Li⁺** | *"ideally close to unity"* | §5.2 |
| 기타 | 공정성·확장성·비용·환경영향 | §5.2 |

⚠ **§4.1 의 `>1 mS/cm` 와 §5.2 의 `≥10⁻⁴ S/cm` 는 10배 차이인데 같은 리뷰 안에서 조정 없이 병기된다.**
Fig. 3 깔때기는 **`σ > 10⁻⁴ S/cm`** 쪽을 그린다(figure-read). ⇒ **이 리뷰는 σ 게이트 값에 대한 합의를 못 만든다.**

### 3.2 σ 냐 D 냐 Ea 냐 — 사용자 질문 5 의 직답

- **보고량의 표준은 압도적으로 `σ_RT` (실온 이온전도도)** 다. 데이터셋 두 개(LiIon·OBELiX)가 둘 다 **실험 실온 σ**
  라벨이고, Fig. 3 깔때기의 마지막 물성 게이트도 σ 다. Ea·D 는 **σ 로 가는 중간 서술자**로 다뤄진다
  (§3.2.1 "Kinetic/dynamic descriptors": Ea, D, attempt frequency, phonon feature).
- **300 K 외삽을 하냐 고온에서 멈추냐** → **리뷰는 외삽을 표준으로 서술하되, 그 위험을 두 곳에서 명시적으로 경고한다.**
  - §2.3.2: *"AIMD simulations of SSEs are often run at very high temperatures, with room-temperature properties
    extrapolated via the Arrhenius relation, **which can be unreliable if diffusion mechanisms change, or phase
    transitions occur**."*
  - SI §S1.5: 고온→RT Arrhenius 외삽은 **Ea 가 온도에 무관하다고 가정**하는데, 확산 기구가 바뀌거나 상전이
    근처면 깨진다.
  - §4.3 [리뷰 경유, Dai 2022 = ref 164]: 가넷은 **Arrhenius 가 아니라 VTF** 다.
  - 초록 [리뷰 주장]: MLIP 가 *"non-Arrhenius transport behavior"* 를 드러냈다 — 리뷰가 스스로 내세운 4대 성과 중 하나.
- ⇒ **문헌 표준 = "고온 AIMD/MLMD → Arrhenius 외삽 → σ_300K 보고"** 이고, 리뷰는 그 표준의 **전제 조건
  (기구 불변)을 명시하라**고 요구한다. 그 이상의 프로토콜(창·시간원점·수렴판정)은 **리뷰 본문에 없다.**

### 3.3 통계적 유의성 — SI 에만 있는 실무 수치 ★ [리뷰 경유, He 2018 = SI ref 13]

우리 MD 규율과 직접 겹치는 유일한 정량 지침이라 따로 뽑는다 (SI §S1.6):

| 목표 정밀도 | 필요 TMSD | 대략 유효 hop 수 |
|---|---|---|
| RSD **~50 %** | **≳ 450 Å²** | ~**50** hops |
| RSD **~20 %** | **> 4150 Å²** | ~**460** hops |

- Ea **0.2–0.3 eV** 계 → 1 ns 시뮬레이션 기준 **450–700 K 이상** 필요.
- Ea **> 0.5 eV** 계 → **1150 K 초과** 필요.
- 예시: LATP(Li₁.₃₃Ti₁.₆₇Al₀.₃₃(PO₄)₃) **1200 K / 200 ps** 에서 RSD ~50 % 수준.
- ⚠ 동시 경고: 600–1000 K 고온 시뮬은 **작동온도에서 무관한 경로를 활성화**할 수 있고, 작은 셀은 확산을
  인위적으로 구속하거나 집단운동을 놓친다 [리뷰 경유, ref 14 = Morgan & Madden 2014].

---

## 4. DFT/계산 방법 ★ — 리뷰가 정리한 "전통 계산 4종" 의 사양표

**이 논문 자체는 계산을 하지 않는다.** 아래는 리뷰가 Table S1 로 정리한 비교표의 요지다 [리뷰 주장].

| 방법 | 주 용도 | 전형 규모 / 시간 | 리뷰가 적은 한계 |
|---|---|---|---|
| **DFT** | 상안정성(생성E·상도), 전자구조(gap·DOS), **ESW**, 결함형성E, 계면 에너지·반응생성물, 기계물성 | ~10s–1000s 원자 / **정적**(포논은 ps) | 대계 비쌈 · **XC 범함수 의존** · 기본 0 K 정적 · 장시간 동역학 불가 |
| **NEB** | 이동 장벽 Ea · MEP · Ea 기반 스크리닝 · KMC 입력 | ~10s–100s 원자 / 정적 경로 | 경로당 DFT 다회 · **초기/최종 상태를 미리 알아야** · **0 K 법**(엔트로피 없음) · 초기경로 나쁘면 local MEP 로 수렴 |
| **KMC** | 장거리 확산·σ · SEI 성장 · 결함 kinetics · 입계 확산 · **조성 무질서 효과** | 수백만 site / **µs–ms 이상** | **사전 event catalog + 정확한 rate 필요** · 상관운동 포착 약함 · 장거리장 처리 난이도 |
| **Classical MD** | 유한 T 벌크 확산·σ · 비정질/무질서 · 입계·계면 · 기계 · RDF | 10³–10⁶⁺ 원자 / **ns–µs** | **force field 가 전부** · FF 개발이 계-특이적 · 전자 없음(반응 불가, reactive FF 제외) |
| **AIMD** | 전자효과 포함 이온동역학 · 신물질(FF 불요) · 단시간 계면반응 · FF/MLIP 벤치마크 | ~10s–100s 원자 / **ps–ns** | 극도로 비쌈 · **고온 시뮬 + 외삽 필요** · XC 의존 |

**NEB 실무 (SI §S1.1)** [리뷰 경유]: 이미지 **5–10장** 권장, 정량 Ea 를 원하면 **force tolerance ≤ 0.01 eV/Å**.
선형보간 초기추정은 비물리 고에너지 경로로 수렴하기 쉽다. CI-NEB 가 안장점 정밀도 해법.

**KMC 실무 (SI §S1.2)**: catalog 완전성이 급소 — 저확률 event 누락이 장시간 거동을 뒤집는다.
보편 attempt frequency **10¹²–10¹³ Hz** 가정은 물리를 단순화하며 계-특이 포논 계산이 필요할 수 있다.

**소프트웨어 (SI §S1.3–S1.4)**: DFT = VASP · Quantum ESPRESSO · Gaussian · ORCA. MD = AMBER · GROMACS · LAMMPS.

**MLIP 프레임 (본문 §3.4)** [리뷰 주장 + 경유]: SGPR / GAP / DeePMD / **CHGNet** / **M3GNet** / **GPTFF**.
- GNN 계열은 **CIF 정밀 원자좌표 필요** + 하이퍼파라미터 많아 **>10³ 표본** 필요.
- SGPR 은 inducing set 저랭크 근사로 **소데이터 영역에서 유리**하고 **불확실도 내장**(→ 능동학습에 바로 붙는다).
- ⛔ **무질서 처리(SQS/enumerate/단일배열) 에 대한 리뷰 차원의 처방은 없다.** 유일한 언급이 §4.1.2 의
  Ataya(LLTO) 사례다 (§5.4 참조).

---

## 5. Figure set ★

**본 그림 = 5장 전부 (fig_1 · fig_2 · fig_3 · fig_4 · fig_5).** 이 논문의 그림은 **전부 개념도**이고 데이터 그림이
**0장**이라 5장 모두 봐도 맥락이 안 터진다. 표 7장(`tab_*.png`)은 **이미지로 안 봤다** — PDF 텍스트가 정확하다.

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 4단 파이프라인 개념도: **(a) Data collection**(MP·ICSD·AFLOW·OQMD + 실험/문헌 큐레이션) → **(b) Feature engineering**(조성/구조/전자 서술자 · Matminer · pymatgen) → **(c) ML models**(지도: RF·XGBoost·SVM·GPR / 딥: CGCNN·MEGNet·CrabNet·ElemNet / 비지도: PCA·HDBSCAN·KMeans·AHC) → **(d) Applications**(물성예측 σ·전기화학안정·기계 / HTVS: optimal doping·원소치환·구조섭동 / MLIP: 확산모델링·대규모 MD·가속 스크리닝) | ★ **우리 Stage 00–12 를 이 4칸에 얹으면 03·04·06 이 어느 칸에도 안 들어간다.** §11 매핑표의 뼈대 |
| 2 | 딥러닝 아키텍처 3종 도해: (a) FFN/MLP(고정길이 특징벡터→물성) (b) GNN — (i) **CGCNN**(원자특징 vᵢ 를 이웃 집계로 갱신 → 풀링 → ŷ) (ii) **MEGNet**(bond eₖ → atom vᵢ → global u 3단 갱신) (c) **CrabNet** 트랜스포머(EDM → attention block ×N → residual → 물성 + **aleatoric uncertainty**) | 우리는 GNN 을 안 쓴다. 다만 **CrabNet 이 불확실도를 출력으로 내는 구조**라는 점이 09c 예측기에 능동학습을 붙일 때 참고 |
| 3 ★★ | **HTVS 깔때기 — 이 논문에서 우리에게 가장 중요한 그림.** (a) 화학공간 생성 = 원소치환 + 결함 (b) ML 물성예측(σ·생성E·전단탄성률) (c) **6단 순차 깔때기**: 열역학 안정 → 전자전도(gap) → 전기화학 안정 → 기계 안정 → 이온전도 → 최종 DFT/AIMD 검증. 각 단에 임계값이 **적혀 있다**(아래) | ★★★ **우리 캐스케이드 순서와 정면 대조.** §7·§11 의 기준 |
| 4 | MLIP 폐루프: (a) ab initio 데이터 생성 → (b) MLIP 학습 → (c) PES 예측·대규모 MD → (d) 설계공간 탐색(조성·도펀트·결정/비정질) → (e) **후보 식별 + 초기 스크리닝(작은 깔때기 아이콘)** → (f) 표적 ab-initio 또는 실험 검증 → **(a) 로 되돌아가는 화살표** | ★ 우리 Stage 12/12b 재학습이 이 (f)→(a) 화살표에 해당. 다만 우리 루프에는 **실험 노드가 없다** |
| 5 | 5대 난제 × 해법 매트릭스. (a) 데이터 부족 → (i) 능동학습 루프(Training Pool ↔ Unlabeled Pool ↔ annotate) (ii) 전이학습(Li⁺ Model 1 → Na⁺ Model 2) (iii) 비지도 (b) 다목적 → (i) 진화알고리즘(mutation/crossover/selection) (ii) **베이지안 최적화**(GP → acquisition 최대 → 목적함수 평가 → GP 갱신) (c) 해석가능성 → (i) **SHAP**(서술자별 기여 % ) (ii) **LIME** (d) 전이/일반화 → (i) 도메인 적응(source/target → cross-domain classifier) (ii) **PINN**(은닉층에 PHY 물리층) (e) 생성 → (i) VAE (ii) GAN (iii) **확산모형** (iv) **생성모형 ⇄ DFT/AIMD 하이브리드 루프** | ★★ **우리에게 (a)-(i)·(a)-(ii)·(c)·(d)·(e) 가 전부 없다.** §11 의 "문헌에 있는데 우리에게 없는 것" 목록이 이 그림이다 |
| Table 1 | 서술자 5범주 × 예시 × 인코딩 정보 × 생성법 × 장단 | §6.1 에 전사 |
| Table 2 | MLIP 6편의 이온동역학 기여 요약 | §6.5 |
| Table 3 | 데이터 난제 4종 × 영향 × 완화전략 | §6.6 — **여기 `LOGO-CV` 가 들어 있다** |
| Table 4 | 생성모형 6종 비교 | §6.7 |
| Table S1 | 전통 계산 5종 사양표 | §4 표 |
| Table S2 | 데이터셋 12종(A: 6 주요 / B: 6 보조) | §6.2 |
| Table S3 | Li/Na/Mg/Al 계 시스템별 요구사항 대비표 | §6.8 |

### 5.1 Fig. 3 깔때기 임계값 — **figure-read** ★★

그림 안에 인쇄된 값을 그대로 옮긴다 (본문에는 이 값들이 **없다**):

| 순서 | 게이트 이름 | figure-read 임계값 |
|---|---|---|
| 1 | Thermodynamic stability | **E_f < 0.1 eV/atom** · **E_hull < 0.2 eV/atom** |
| 2 | Electronic conductivity | **E_gap < 0.5 eV/atom** ⚠ (아래) |
| 3 | Electrochemical stability | **μ < 4.0 eV** ⚠ |
| 4 | Mechanical stability | **G > 8.5 GPa** |
| 5 | Ionic conductivity | **σ > 10⁻⁴ S/cm** |
| 6 | Final evaluation | DFT/AIMD validation |

🔴 **2단은 명백한 오류다** (내가 그림을 직접 보고 판독): SSE 는 **넓은** gap 이 필요한데 부등호가 `<` 이고,
단위가 **`eV/atom`** 이다 — 밴드갭은 원자당 양이 아니다. 앞줄 두 개(E_f·E_hull)의 `eV/atom` 이 그대로
복사된 것으로 보인다. 3단 `μ < 4.0 eV` 도 μ 가 무엇의 화학퍼텐셜인지·왜 부등호가 `<` 인지 그림에도 본문에도
정의가 없다. ⇒ **이 그림의 임계값은 "이런 종류의 게이트가 이 순서로 온다" 는 구조 근거로만 쓰고,
숫자 자체를 우리 게이트 값으로 이식하지 않는다.**

---

## 6. 본문 절별 정리 — 수치 전부 [출처 층위 표기]

### 6.1 서술자 5범주 (§3.2.1 + Table 1) [리뷰 주장]

| 범주 | 예시 | 인코딩하는 정보 | 생성법 | 리뷰가 적은 장단 |
|---|---|---|---|---|
| **조성** | 평균 전기음성도 · 원소 분율 · 평균 원자량 · 원자반경 분산 · 화학량비 | 결합 경향 · 화학량 | 화학식만 | 매우 쌈 / **구조 무시** |
| **구조** | 원자당 부피 · 공간군 번호 · **RDF** · 배위수 · 결합각 · 다면체 부피 · Voronoi motif · 위상지수 | 기하 배열 | CIF 분석 | 이동도/강성과 직결 / **구조 필요** |
| **전자** | **밴드갭 E_g** · VBM/CBM 위치 · E_F 근처 DOS · 일함수 · 전자친화도 · 이온화퍼텐셜 · 결합 이온성/공유성 | 전자구조 | **DFT** | 전자절연 판정 핵심 / **비쌈** |
| **물리화학·열역학** | 생성E · **E_hull** · 밀도 · 이온반경 · 융점 · **K·G** | 안정성·가공성·기계강건성 | DFT DB / ML | 표준 스크리닝 축 / 계산 필요 |
| **운동학** | **Ea(Eb)** · **D** · attempt frequency · **포논 특성**(vDOS·포논밴드) | 이온수송 | NEB / MD / 포논 DFT | σ 와 직결 / **가장 비쌈** |

- 조성 서술자 실사례 [리뷰 경유, ref 93]: **145개 "Chemical Descriptor"** 특징(화학량 + 원소물성).
- 구조 서술자 실사례: **Voronoi tessellation** 으로 GNN 개선 [ref 94] · **SOAP** 로 국소환경 표현 [ref 95].
- **포논 유래 특징이 σ 의 중요 예측자**로 최근 확인 [리뷰 경유, ref 96].
- 도구: **pymatgen**(핵심 자료구조) · **Matminer**(조성/구조/전자 서술자 일괄) · **DeepChem**(그래프 표현).

### 6.2 데이터 자원 (§3.1 + Table S2)

**계산 DB**: Materials Project(생성E·gap·탄성텐서·구조) · **ICSD >300,000 실험 구조**(구독) ·
AFLOW(AFLOWLIB REST API) · OQMD(convex hull 중심) · NIST-JARVIS(탄성·유전·포논) ·
CMR/C2DB/QPOD · Materials Cloud(AiiDA provenance) · **COD >520,000 구조** ·
**GNoME**(DeepMind, **>200만** 무기결정 안정성 예측) · **Alexandria**(수백만, 대규모 ML 학습용).

**실험 큐레이션 DB** [리뷰 경유]:

| 데이터셋 | 규모 | 내용 |
|---|---|---|
| **LiIon** [ref 87 = Hargreaves 2023] | **820 entries / 214 문헌** · **403 unique 조성**이 실온 근처 σ 보유 | 조성 + 구조라벨(garnet·LISICON…) + AC 임피던스 σ(온도 명기). **CrabNet 고/저 전도 분류기 학습에 사용** |
| **OBELiX** [ref 88 = Therrien 2025, arXiv 2502.14234] | **~600** 합성 SE | 실험 실온 σ + 조성 + 공간군 + 격자상수, **약 절반은 CIF 완비**. **ML 벤치마크 목적으로 설계** |
| 문헌 마이닝 [ref 90 = Shon & Min 2023] | **>4,000 σ 측정 / ~1,500 논문** | NLP 추출. 이질성·조건 불일치·추출 정확도 문제 |

**데이터 난제 (§3.1.3 + Table 3)** [리뷰 주장]: 실온 σ 희소 · 이질성(계산 vs 실험, 프로토콜 차이, 포맷 차이) ·
불확실성/오류 · **결측값 + 심한 클래스 불균형(고성능 SE 가 극소수)**. 완화책으로 **imputation** 과
**SMOTE** 리샘플링 [ref 92] 을 든다.

🔑 **Table 3 의 마지막 행이 사용자 질문 4 의 핵심이다**:
> *"Small sample sizes for truly novel chemistries → 과적합 위험·미탐사 공간 예측력 저하 →
> 완화: 생성모형[186] · 광역 화학도메인 전이학습[187] · **LOGO-CV for realistic performance assessment[188]**"*

### 6.3 고전 ML 알고리즘 응용 (§3.2.2) [전부 리뷰 경유]

| 유형 | 사례 | 수치 |
|---|---|---|
| 회귀 | Ahmad — GBR + KRR 로 **>12,000** 무기고체의 G·K 예측 [ref 98] | — |
| 회귀 | Zhao — GPR 기반 BO 로 LATP 실험합성 유도 [ref 99] | — |
| 분류 | **Xu 2020** — 로지스틱 회귀로 SICON 계 초이온전도체 양/불량 분류 [ref 47] | — |
| 분류 | Chen 2021 — SVM 으로 제조조건↔SE 필름 성능 [ref 100] | — |
| 분류 | Adhyatma 2022 — LightGBM 으로 **도핑 LLZO** 의 σ 고/저 분류 [ref 101] | — |
| 앙상블 | Pereznieto 2023 — RF 로 신규 Na SE 발굴 [ref 102] | — |
| 앙상블 | Kim 2023 — GB 앙상블로 **>3,500** NASICON 분류 [ref 103] | — |
| 앙상블 | **Tang 2024** — XGBoost 로 **>6,000** 구조에서 **194** 이상적 SSE 후보 [ref 104] | **6000 → 194** |
| 앙상블 | Zhang 2024 — RF + NN 로 NASICON σ, **Na 화학량 수**가 지배인자 [ref 105] | — |
| 군집 | **Park 2024** — HDBSCAN 으로 **>12,000** Na 함유 물질 → **12 군집**, 고전도 군집이 **XO₄ 사면체 다수 + 넓은 이온채널** 공유 [ref 106] | **12,000 → 12 군집** |
| 군집 | **Laskowski 2023** — agglomerative 로 **~26,000** Li 함유 구조 군집화 후 소수 실험 σ 로 라벨링 → 고확률 군집 → **Li₃BS₃ 실험 확인** [ref 95] | **26,000 → 1 신물질** |
| 이상탐지 | **Gallo-Bueno 2022** — 비지도 outlier 탐지로 계산된 **Li-argyrodite 결정구조를 구조 왜곡 기준으로 자동 분류** [ref 107] | ★ argyrodite 직결 |

### 6.4 물성별 ML (§4.1) [전부 리뷰 경유]

**σ 예측**

| 연구 | 규모 | 수치 |
|---|---|---|
| **Sendek 2017** [ref 143] | 학습 **40** 화합물, 로지스틱 회귀. 서술자 = **Li–Li 배위수 · 부격자 결합 이온성 · 음이온 배위환경** | **MP 12,000 스크리닝 → 21 fast-conductor 후보**. 후속 DFT-MD 로 여럿 초이온 확인, 특히 **Li₃InCl₆** 는 **실험 검증**까지 [ref 143,144] |
| Mishra 2023 [ref 110] | **8종 예측기** 비교(RF·SVM·shallow NN), 특징 = Ea + 작동온도 + 격자상수 | 앙상블(RF) 강건, **model stacking 이 과적합 방지** |
| **Jaafreh 2024** [ref 145] | Mg 전해질, **PhDOS → "total phonon band center"** 를 σ 대리로 | **Extra Random Trees R² = 0.964**, **~9,000 Mg 화합물** 예측. Mg–Se 중앙 band center **27.5 meV** < Mg–S **40.5** < Mg–O **55.5 meV** |
| **Dong (2025)** [ref 146] | Na·Mg·Al 가넷, XGBoost | **열안정성 94 % · 밴드갭 89 %** 정확도, **43,732** 화합물. → **1,764** (열안정+전자기준 동시) → **44** 경제성 후보. **평균 전기음성도**가 열안정 최중요, **원자반경 범위**가 갭 지배 |
| Kharbouch 2024 [ref 147] | LLZO 가넷, CatBoost + Optuna | **σ R² = 0.85**. 화학량 검증 + KNN imputation 강조 |
| **Maevskiy 2025** [ref 148] | **M3GNet PES · frozen-framework 근사**에서 유도한 휴리스틱 이동도 서술자 | **MLIP-MD 대비 ~50× · AIMD 대비 >3,000× 빠름**. **상위 10 중 8이 제1원리로 초이온 확인** ★ |

**전기화학 안정성**

| 연구 | 핵심 |
|---|---|
| **Ataya** [ref 150] ★★ | **LLTO 무질서 배열 문제.** 종래 Coulomb 법이 **DFT 완화 후의 최저에너지 배열을 못 찾는다** → ESW 를 **3.1 V 로 과대**(정답 **2.5 V**), 예측오차 **최대 0.67 eV**. 해법: **SOAP-KRR 을 DFT 완화 구조 40개**로만 학습시켜 에너지 순위를 정확히 예측 |
| **Chen 2025** [ref 51] | **20,717** MP Li 화합물 → 열역학 안정 + 밴드갭 사전스크린 → **468 표본**으로 학습한 ML 분류+회귀 → ESW 평가 → AIMD → **3 후보**(Li₃BiS₃, Li₅BiS₄, **Li₁₀ZnP₄S₁₆**) |
| Kireeva [ref 151] | LLZO 가넷 최적 격자상수 **12.950–12.965 Å**. SVM·LSTM·GP·XGBoost. 영향인자 = Li·La 함량, C 자리 원자산란인자, **도펀트 Shannon 이온반경** |

**기계 물성**

| 연구 | 핵심 |
|---|---|
| **Ahmad** [ref 98] | CGCNN 을 **2,041** DFT 탄성 구조로 학습 → **>12,000** 무기고체 예측 → **Monroe–Newman 안정성 파라미터 χ** 로 dendrite 개시 평가 → **>20 기계이방성 계면 / 6 SE** 가 dendrite 억제 예측 |
| **Choi** [ref 152] ★ | LightGBM, **14,238** 탄성 구조. 초기 **G 의 R² = 0.633** → **능동학습**(고불확실도 우선 추가) → **R² = 0.802**. **1,600 전략적 추가** vs **무작위 2,800** (≈1.75× 데이터 효율) |
| **Sun** [ref 50] | 2단 워크플로: LGBM 기계 스크리닝 **5,329** LLZO 파생 → 초이온 분류 → AIMD → **10** 신규 정방정 물질 |
| Wang [ref 153] | LGBM **R² ≈ 0.86–0.87**(G·K), **8,920** MP 표본. **SHAP: 원자당 부피 + VBM 이 핵심 예측자**. Mg·Al·K·Ni 부재 데이터로 **외삽 실험** — 다양한 표본 전략적 추가로 전이성 개선 |

### 6.5 HTVS 캠페인 — **깔때기 실측치** ★★★ (사용자 질문 1)

**리뷰 본문에서 단계별 수를 복원할 수 있는 캠페인 전부** [전부 리뷰 경유]:

| # | 연구 | 시작 | 중간 단계 (리뷰가 적은 만큼) | 최종 | 총 생존율 |
|---|---|---:|---|---:|---|
| 1 | **Chen 2024** [ref 154=218] JACS | **32,000,000** | → **~589,000** (M3GNet 열역학 안정, **98.2 % 제거**) → ML **밴드갭 >3 eV** + 전기화학 안정 (단별 수 **미보고**) → 고정밀 DFT | **18** | **5.6×10⁻⁷** |
| 2 | **Wang AI-IMAE** [ref 160] | **144,595** | CGCNN Ea 예측 (9종 이온, **~10⁵× 가속**) | **316 SE + 129 양극** | 2.2×10⁻³ |
| 3 | **Dong 2025** [ref 146] | **43,732** | → **1,764** (열안정 + 전자, **96.0 % 제거**) → 경제성 | **44** | 1.0×10⁻³ |
| 4 | **Xie** [ref 158] ★ | **~50,000** | **BV-KMC**(bond-valence kinetic MC)로 안정성 + σ 임계 → **329**. 별도로 등원자가 치환 **979** 추가 → **239** 초이온 후보 | **329 (+239)** | 6.6×10⁻³ |
| 5 | **Chen 2025** [ref 51] | **20,717** | 열역학 + 밴드갭 사전스크린 → ML 분류/회귀(**468** 학습) → ESW → AIMD | **3** | 1.4×10⁻⁴ |
| 6 | **Lee 2024** [ref 156] antiperovskite | **18,133** | GA + BO(GPR) **능동학습** → **DFT 단 144회** → **4차원 Pareto**(열역학·갭·ESW·σ) | **22** (그중 **7**이 σ_RT **>4 mS/cm**) | 1.2×10⁻³ |
| 7 | **Ahmad** [ref 98] | **>12,000** | CGCNN G·K → Monroe–Newman χ | **>20 계면 / 6 SE** | ~5×10⁻⁴ |
| 8 | **Tang 2024** [ref 104] | **>6,000** | XGBoost(밴드구조·안정성) | **194** | 3.2×10⁻² |
| 9 | **Sun** [ref 50] | **5,329** | LGBM 기계 → 초이온 분류 → AIMD | **10** | 1.9×10⁻³ |
| 10 | **Lee 2025** [ref 155] **Na-argyrodite** ★★ | **4,375** | DFT 로 **E_hull · 생성E · 밴드갭 · ESW** 전부 계산 → **4차원 Pareto sorting → 15** → AIMD | **5** (Na₆SiS₄Cl₂, Na₇.₇₅SiS₅.₇₅Cl₀.₂₅ 등) | 1.1×10⁻³ |
| 11 | **Wan DopNetFC** [ref 159] ★★ | **2,208 치환** (Li₁₀GeP₂S₁₂ 도핑) | DopNetFC(RF·GBDT 능가) → **다단 DFT**(열역학·전자·기계 안정) | 수 미보고 | — |
| 12 | **Sendek 2017** [ref 143] | **12,000** | 로지스틱 회귀 1단 | **21** | 1.8×10⁻³ |
| 13 | **Sewak** [ref 157] NASICON | **170 실험** | 로지스틱 회귀 + PCA → **9 핵심 특징** → **BVSE 로 도펀트 이동장벽 추정** | **Li₂Mg₀.₅Ge₁.₅(PO₄)₃**, DFT 검증 장벽 **0.261 eV** | — |

🔴 **사용자 질문 1 의 직답 — 단별 제거율은 거의 아무도 보고하지 않는다.**
위 13건 중 **단 하나의 게이트에 대해서라도 "몇 개 들어가 몇 개 나왔다"를 리뷰가 옮겨 적은 것은 2건뿐**이다:
- Chen 2024: **32 M → 589 k** (열역학 안정 단, **98.2 % 제거**) — 그 뒤 갭·ESW 단의 수는 **없다**.
- Dong 2025: **43,732 → 1,764** (열안정+전자 **합쳐서**, **96.0 % 제거**) → 44.

나머지 11건은 **입력수와 최종 후보수만** 있다. **Xiao 2019 · Kim 2026 식의 "ECW 94.3 % → 계면 41.9 % →
Li–Li 네트워크 41.3 % → 밴드갭 2.6 %" 같은 단별 감쇄 프로파일은 이 리뷰 어디에도 없다.**
⇒ **우리 좌표에서 이건 나쁜 소식이 아니라 좋은 소식이다.** 문헌 최전선조차 자기 깔때기의 단별 효율을
공개하지 않는다 ⇒ **우리가 Stage 00–12 의 단별 제거율을 공개하면 그 자체가 새 보고형식이 된다.**

### 6.6 게이트 순서의 정당화 (사용자 질문 2)

🔴 **직답: 이 리뷰에는 게이트 순서를 정당화하는 논증이 없다. 순서 민감도 분석은 0건이다.**

리뷰가 순서에 대해 실제로 말하는 것 전부:

1. **"싼 것 먼저"** [리뷰 주장, §3.1.3 마지막 문단] —
   > *"This often leads to a **multi-stage ML workflow**: initial screening using models trained on large
   > computational datasets to identify stable and electronically suitable candidates, **followed by**
   > conductivity prediction for the down-selected candidates using models trained on experimental data."*
   근거는 **비용**뿐이다 (σ 예측용 실험 학습 데이터가 희소하고 MD 가 비싸므로 뒤로).
2. **"ML 은 싸고 빠른 필터"** [§4.2 서두] —
   > *"ML plays a crucial role in making HTVS more efficient by acting as **fast and inexpensive filters**,
   > prioritizing the most promising materials for further, more accurate investigation."*
3. **Fig. 3 의 6단 순서** (figure-read) = 열역학 → 전자 → 전기화학 → 기계 → 이온전도 → DFT/AIMD.
   이 순서에 대한 **본문 설명이 전혀 없다.** 그림 캡션도 *"filtered through a sequential funnel based on
   physical criteria"* 라고만 한다.
4. **[리뷰 경유] Chen 2024** 만이 유일하게 "funnel-based" 라는 말을 쓰며 실제로 **가장 싼 것(M3GNet 안정성)을
   맨 앞**에 둔다.

**⇒ 정리**: 문헌 표준은 **"싼 것 먼저"** 이지 **"많이 자르는 것 먼저"** 가 아니다. 그리고
**둘 중 어느 것이 옳은지 비교한 연구가 이 리뷰 안에 하나도 없다.** 순서를 바꿔 최종 후보 집합이
얼마나 달라지는지 본 사례 **0건**.

⚠ 그런데 두 원칙은 **충돌할 수 있다** — Chen 2024 에서 가장 많이 자르는 단(98.2 %)이 마침 가장 싼 단이라
충돌이 안 드러났을 뿐이다. **우리 캐스케이드는 정확히 이 충돌 지점에 있다**: Stage 07+08(EOS·탄성)이
no-MD 예산의 75–85 % 를 먹으면서 자르는 양은 0 이다.

### 6.7 MLIP 로 밝힌 이온동역학 (§4.3 + Table 2) [전부 리뷰 경유]

| 연구 | MLIP | 계 | 핵심 수치·발견 |
|---|---|---|---|
| Behler & Parrinello 2007 [162] | HDNNP(대칭함수) | bulk Si | 총에너지를 국소 원자기여로 분해 → 임의 크기 계 시뮬 가능. **현대 MLIP 의 방법론 원전** |
| **Gigli 2024** [163] ★★ | **GAP ×3 (PBEsol / r²SCAN / PBE0)** | **Li₃PS₄ α·β·γ 전 다형** | **768 원자 · 최대 6 ns.** 초이온성 = γ → 혼합 α-β **구조전이**, 상관된 **PS₄ flip** 이 Li Ea 를 **최대 6배** 낮춤. **paddle-wheel 반박** — PS₄ flip(ns) 과 Li hop(ps) 이 자릿수로 분리. **Nernst–Einstein 이 σ 를 2배 넘게 과소평가**(강한 이온 상관) |
| **Dai 2022** [164] ★ | ANN (SIMPLE-NN) | Li_xLa₃Zr_{x−5}Ta_{7−x}O₁₂ 가넷 | **Arrhenius 아니라 VTF.** σ 최대는 **Li 함량 6.6–6.8**. **Haven ratio 0.1–0.4** ⇒ 강한 협동운동 |
| **Seth 2025** [165] | **NequIP** (E(3)-equivariant), **>13,000** DFT 구조 학습 | 비정질 **LiPON** + Li‖LiPON 계면 | 벌크 실온 σ 실험 재현. **계면 수송이 벌크보다 한 자릿수 느림** |
| **Yang 2025** [166] | DeePMD | 비정질 Li_xAlO_yCl_{3+x−2y} | Li⁺ 수송이 **Al 사슬 골격 안 Cl 회전**으로 촉진. **O 도핑이 비정질화는 돕지만 가동 Cl 을 줄인다 → 최적 O/Cl 비 존재** |
| **Guo 2022** [167] | ANN + **유전알고리즘** 샘플링 | (Li₂S)ₓ(P₂S₅)₁₋ₓ 유리세라믹 | **x ≈ 0.725** 에서 초이온 β-Li₃PS₄ 유사 국소 Li 환경이 에너지적으로 유리. 비정질 상도 + 혼화갭. **σ > 10⁻² S/cm** 예측 조성 설계 |
| **Ha 2022** [168] | **SGPR on-the-fly** | Al 도핑 Li-과잉 층상산화물 Li₁.₂₂Ru₀.₆₁Ni₀.₁₁Al₀.₀₆O₂ | Al 도핑이 Li 확산 Ea **0.48 → 0.40 eV**, 고온 D **약 2배**. Al–O 결합 강화가 산소 산화 억제 |
| **Du 2025** [178] ★★ | uMLIP | **Li₆PS₅Cl** | uMLIP 은 **학습 화학공간 밖으로 일반화 실패**. 그리고 **적절한 S/Cl 무질서가 확산경로 연결성을 높여 σ 개선** |

**MLIP 검증 실무** [리뷰 주장, §4.3 말미]: 에너지·힘 비교를 넘어 **AIMD 대비 D·상안정성·열수송 벤치마크** →
**앙상블/gradient/committee 불확실도 정량** → 능동학습 반복 → **rare event·장시간 동역학 도메인 검증**.
*"standardized validation protocols and uncertainty reporting will be essential"* — 즉 **아직 표준이 없다**고 선언.

**⚠ 리뷰 스스로 적은 MLIP 의 한계**: *"current MLMD simulations still remain **far from** capturing the
experimentally relevant timescales (seconds to minutes)"* → 실험 스케일까지 가려면 **MLMD + adaptive KMC 하이브리드**가
필요하다는 것이 리뷰의 처방.

### 6.8 다가이온 대비표 (Table S3) [리뷰 주장]

| 축 | Li⁺ | Na⁺ | Mg²⁺ | Al³⁺ |
|---|---|---|---|---|
| 수송기구 | 사면체 자리 간 직접 hopping | Li 유사 + 큰 반경 효과 | **협동적 구조완화 · 일시적 배위변화 필요** | 높은 전하밀도 · 골격 수용 필요 |
| Ea | 기준(중간) | 중~높음 | **현저히 높음** | **매우 높음** |
| dendrite | **치명적 관심사** | 중간 | **낮음**(2가라 자연 억제) | 가변 |
| 데이터 | **풍부 — 수천** | 중간 — 수백~저千 | **희소 — 수십~저百** | **매우 희소 — 수십~저百** |
| ML 전이성 | 학습 기준 | Li 로부터 중간 전이 | **전이 나쁨** | **전이 매우 나쁨** |
| 온도의존 | 표준 Arrhenius | 표준 Arrhenius | **기구변화로 Arrhenius 이탈 가능** | **이탈 가능** |
| 핵심 서술자 | 배위환경 · 다면체 packing · 골격 연결성 | Li + 이온채널 치수 | 양이온 배위 유연성 · 골격 완화능 · 용매화 | 양이온 전하밀도 · 골격 강성 · void 부피 |

### 6.9 전이학습 / 능동학습 — 실제 사례 (사용자 질문 6)

**전이학습 (§5.1 Solution 1 + §5.4 Solution 1)** [리뷰 경유]:
- 유일한 SSE 내 정면 사례: **Xu 2020** [ref 47] — *"models trained **exclusively on Na⁺-based NASICON**
  compounds accurately predicted **Li⁺-based** materials"* (분류 과제).
  ⚠ 리뷰가 **스스로 깎아내린다**: *"However, the **chemical similarity between Na⁺ and Li⁺ likely enabled
  this success**. Extending transfer learning to multivalent systems ... may require sophisticated domain
  adaptation techniques or physics-informed constraints."*
- **정량 성능 수치(전이 전/후 R²·MAE)는 리뷰에 없다.**
- 도메인 적응 사례는 **SSE 가 아니라 전기촉매** [ref 209] 에서 빌려온다 — *"demonstrating a concept
  **directly transferable** to SSE research"* 라고만.
- 사전학습 파운데이션 모델(MEGNet·M3GNet·CHGNet·GPTFF)의 **fine-tuning** 을 전이학습의 실질 경로로 제시.

**능동학습 (§5.1 Solution 3 + §5.5 Solution 3)** [리뷰 경유]:

| 사례 | 정량 성능 |
|---|---|
| **Choi** [ref 152] — LightGBM G 예측 | **R² 0.633 → 0.802**, 추가 표본 **1,600(AL) vs 2,800(무작위)** ★ 유일하게 숫자가 붙은 AL 효율 |
| **Verduzco 2021** [ref 57] — **LLZO 도핑 전략** 최적화 | 불확실도 정량 + AL 로 조성공간 탐색, *"minimizing required simulations and experiments"* — **수치 없음** |
| **Lee 2024** [ref 156] — antiperovskite | GA + BO 로 **DFT 단 144회**(18,133 중) — 사실상 **99.2 % 계산 절감** |
| **Tawfik 2025** [ref 58] — BO | Li 확산도 최대화 + 갭·Li 금속 계면 안정 체크를 순차 유도 평가로 |
| **Harada** [ref 195] — BO | NASICON LiZr₂(PO₄)₃ 의 **Ca·Y 공도핑** 조성 최적화 — σ·상안정·치밀화 동시 향상 |
| **CAMEO** [ref 216] | 싱크로트론 빔라인과 결합한 실시간 폐루프 베이지안 능동학습 상도 매핑 |
| **DiffMix** [ref 211] | 미분가능 GDL 이 로봇 실험 유도, *"significant conductivity improvements in **a few experimental steps**"* — 수치 없음 |
| **NaₓLi₃₋ₓYCl₆** [ref 218=154] | AI + 클라우드 HPC 물리시뮬 + 실험합성 폐루프. **실험 검증 성공** |
| MLIP 반복학습 [ref 210] | 불확실도 높은 구조에 DFT 를 던지는 폐루프 |

⇒ **AL 이 붙는 자리는 두 곳이다**: ① **비싼 라벨 획득**(DFT 탄성·DFT ESW) ② **다목적 Pareto 탐색**(GA+BO).
**깔때기 게이트 자체를 AL 로 대체한 사례는 없다.**

### 6.10 다목적 최적화 (§5.2)

- 리뷰의 진단 [리뷰 주장]: *"Traditional **single-objective** ML approaches, predominantly focused on
  maximizing ionic conductivity, **fail to capture these trade-offs and produce materials unsuitable for
  practical applications**."*
- 해법 1 = **BO** (GP 대리모형 + 목적별 acquisition, 계별 가중치).
- 해법 2 = **진화알고리즘 / Pareto front**. *"direct applications to comprehensive inorganic SSE discovery
  remain limited"* — SSE 에 대한 EA 직접 적용은 아직 드물다고 스스로 인정. 사례는 페로브스카이트용
  **EVAPD**(VAE+GA) [ref 196].
- 실제 SSE Pareto 사례 2건 [리뷰 경유]: **Lee 2025 Na-argyrodite 4차원 Pareto sorting** [155],
  **Lee 2024 antiperovskite 4차원 Pareto frontier** [156]. **둘 다 "가중합 스칼라" 가 아니라 Pareto 다.**
- 해법 3 = ML 전문가 ↔ 배터리 전문가 협업으로 응용별 가중·제약 위계 정의 (EV = 안전/기계/ESW 우선,
  휴대기기 = σ 우선).

### 6.11 해석가능성 XAI (§5.3)

- 도구: **SHAP** · **LIME** · **XpertAI**(XAI + LLM 으로 자연어 설명 자동생성) [ref 198].
- 얻어낸 설계원리 사례 [리뷰 경유]: 강성은 **질량밀도**와 **Li/부격자 결합 이온성 비**에 따라 증가,
  **원자당 부피**와 **부격자 전기음성도**에 따라 감소 [ref 202].
- 물리내장 아키텍처: 고분자 SE 모델이 **readout layer 에 Arrhenius 식을 명시 인코딩**해 Ea·A 를
  물리적으로 해석 가능한 출력으로 [ref 201].
- 신흥: **인과 ML**(상관 vs 인과 구분) [204] · **기호회귀**(닫힌형 지배방정식 발견) [205].
- 🔴 **리뷰가 적은 XAI 한계** [리뷰 주장, 중요]:
  - **SHAP 은 강한 상관 특징공간에서 불안정** — 재료 데이터셋이 정확히 그렇다 [206].
  - **LIME 의 국소 근사는 전역 거동을 대변 못 할 수 있다** [207].
  - **둘 다 특징 독립성을 가정**하는데 원자좌표·배위·결합은 본질적으로 결합돼 있다.
  - 권고: 복수 XAI 교차검증 + **해석 전에 특징 상관행렬 확인** + 실험/물리 원리 대조.

### 6.12 전이·일반화 (§5.4) — **사용자 질문 4 의 정본 문단** ★★★

리뷰 원문 (§5.4 서두):
> *"The core issue is that ML models excel at **interpolation** within their training data domain but
> struggle with **extrapolation** to chemically distinct regions. **Conventional cross-validation
> techniques, which randomly split data into training and test sets, often overestimate a model's true
> extrapolative power because test sets usually contain materials chemically similar to training data.**
> More rigorous **'leave-one-group-out cross-validation' (LOGO-CV), where entire chemical families are
> held out for testing, has demonstrated that conventional ML methods can fail when predicting properties
> of completely novel compound classes.**¹⁸⁸ This presents a critical concern for SSE discovery, where the
> goal is often to identify entirely new material families with breakthrough properties."*

🔴 **직답 (사용자 질문 4): 이 리뷰 전체에서 group-out 검증을 *실제로 수행한 SSE 연구 사례는 0건이다.**

근거 3중:
1. **LOGO-CV 를 뒷받침하는 유일한 인용 [ref 188] 은 SSE 논문이 아니다** —
   **Z.-W. Zhao, M. del Cueto, A. Troisi, *Digital Discovery* 1, 266–276 (2022)** = Troisi 그룹의
   **분자·유기 재료** ML 방법론 논문. 즉 **리뷰는 SSE 밖에서 규범을 빌려온다.**
2. **본문·SI 전수 검색 (내가 직접 돌린 결과, SI 는 전 항목 0)**:

   | 검색어 | 본문 | 어디 |
   |---|---:|---|
   | `LOGO-CV` | **2** | Table 3 셀 1 + §5.4 본문 1 — **끝** |
   | `leave-one-group-out` | **1** | §5.4 (위 LOGO-CV 의 풀네임, 줄바꿈으로 갈라짐) |
   | `randomly split` | **1** | §5.4 — 종래 CV 를 **비판하는** 문장 |
   | `cross-validation` | 4 | 그중 **2회가 중복 인쇄된 같은 문단** (§10-1) |
   | `computational holdouts` | 2 | 역시 그 **중복 문단** |
   | `scaffold` · `k-fold` · `random split`(정확 문자열) | **0** | — |

   ⇒ **group-out 관련 어휘가 이 30 pp 리뷰 전체에서 실질 2군데(§5.4 한 문단 + Table 3 한 셀)에만 존재한다.**
3. §6.5 표의 13개 캠페인 중 **CV 형식을 리뷰가 명시한 것은 1건도 없다.** R² 를 보고한 5건
   (Jaafreh 0.964 · Kharbouch 0.85 · Choi 0.633→0.802 · Wang 0.86–0.87 · Dong 94 %/89 %)
   **전부 분할 방식 미기재**다.

**리뷰가 대신 권고하는 검증 형식** [리뷰 주장, §3.4 + §4.1.1 — **동일 문단이 두 번 인쇄돼 있다**, §10 참조]:
> *"Effective validation strategies require testing against **independent experimental datasets rather than
> computational holdouts**, implementing cross-validation with available experimental data, and developing
> calibration methods that account for temperature-dependent Arrhenius behavior and experimental
> measurement uncertainties."*

⇒ 리뷰의 검증 철학은 **"계산 holdout 말고 독립 실험 데이터로 재라"** 이지 **"그룹을 통째로 빼라"** 가 아니다.
LOGO-CV 는 Table 3 한 셀과 §5.4 한 문단에 **권고로만** 있고, **어떻게 그룹을 정의할지(화학족? 구조 프로토타입?
모구조? 도펀트?)에 대한 처방이 없다.**

**해법 3종** [리뷰 주장]: ① 도메인 적응 ② **PIML**(물리법칙·대칭을 아키텍처/손실/특징에 내장; 사례는
액체 전해질 uMLP [210] 과 **DiffMix — VFT 식을 GDL 학습 계수로 확장** [211]) ③ 보편 표현학습(미해결 프론티어).

### 6.13 생성 설계 (§5.5 + Table 4)

VAE(Noh, 역설계 [55]) · GAN(MatGAN [54], 결정구조 예측 [128]) · **확산모형**(**MatterGen** [213] —
안정·다양한 무기물 생성 + 화학/대칭/물성 조건부 fine-tune, **1개 구조 실제 합성 검증**) ·
EA(**XtalOpt** [214]; 비지도 ML 이 원소 상장 우선순위를 정해 **신규 4원계 Li SE 발견** [215]) ·
하이브리드(EVAPD) · **통합 폐루프**(CAMEO · Electrolytomics · NaₓLi₃₋ₓYCl₆ · DiffMix).

**생성모형 검증 다층 필터** [리뷰 주장]:
① DFT hull 거리 — **물질군별 metastability 척도에 근거한 화학의존 임계값** [220]
② **kinetic accessibility** — polymorph 합성가능성의 열역학 상한(amorphous limit) [221]
③ 자동 특성화 신속검증 — XRD 상동정 + 임피던스 [222–224].

**자율 실험실의 장벽** [리뷰 주장]: 무기 고체 합성은 고온·분위기 제어·다단 공정이라
**액상 배합처럼 자동화가 쉽지 않다** — 표준화·자동화·신속 합성/특성화 프로토콜 부재가 최대 난관.

---

## 7. 우리 DFT/캐스케이드 대비 ★

> ⚠ 이 논문에는 우리와 **같은 척도로 비교할 물성값이 하나도 없다.** 아래는 **구조 대조**다.

| 항목 | 이 리뷰가 정리한 문헌 표준 | 우리 (Stage 00–12) | 판정 |
|---|---|---|---|
| **깔때기 순서** | 열역학 → 전자(갭) → 전기화학 → 기계 → σ → DFT/AIMD (Fig. 3) | 02 UMA → 03 ΔV → 05 BVSE → 07 EOS → 08 탄성 → 09e hull → (09f=ESW 아님) → 10 σ MD | 🔴 **거의 역순.** 우리는 안정성 축이 맨 뒤이고 그나마 09e 는 탈락 0종, 09f 는 ESW 가 아니다 |
| **순서 정당화** | **"싼 것 먼저"** (비용 근거). 순서 민감도 분석 **0건** | 근거 문서 없음 | ⚪ **양쪽 다 없다** — 우리가 뒤진 게 아니다 |
| **집계 방식** | **Pareto front** (Lee 2024 · Lee 2025 둘 다 4차원 Pareto) | **Stage 09a = 3축 가중합 스칼라** | 🔴 **우리가 낡았다.** 리뷰가 명시적으로 *"single-objective … fail to capture trade-offs"* 라고 때리는 그 형태다 |
| **σ 보고량** | **σ_RT** (고온 → Arrhenius 외삽), 게이트 `σ > 10⁻⁴ S/cm` | Stage 10 은 **D_rel_vs_host ≥ 0.90** (상대비), 절대 σ 인용 금지 | 🟡 **다른 형식.** 우리 상대비는 문헌 형식이 아니라 같은 표에 못 올린다. 단 회신 AL 판정(600 K 조건부 tracer)이 리뷰의 외삽 경고와 **같은 편** |
| **MD 통계 판정** | **TMSD ≥ 450 Å² (RSD 50 %) / > 4150 Å² (RSD 20 %)** [He 2018 경유] | 우리 정본 = MSD 창 2–50 ps · 200 ps prod · 다중원점. **TMSD/hop 수 판정 없음** · Stage 10 은 창 이탈(`fit_start=n/2`, 단일 원점) | 🔴 **우리에게 검출하한·수렴 판정이 없다.** 이식 가치 최상 |
| **Haven / 상관** | **Dai 2022 H_R = 0.1–0.4** · **Gigli 2024: NE 가 σ 를 2배 넘게 과소평가** | **H_R = 1 못박힘** (`computational_methods_canonical.md` L151) | 🔴 **우리 규약이 문헌과 어긋나 있다.** 단 우리는 절대 σ 인용을 금지해 두어 즉각적 오류로는 안 번진다 |
| **무질서 처리** | 리뷰 차원 처방 **없음**. 단 **Ataya**: Coulomb 배열선택이 **DFT 완화 후 최저에너지를 놓쳐 ESW 를 3.1 vs 2.5 V 로 과대**, 오차 최대 **0.67 eV**. 해법 = **SOAP-KRR 을 DFT 완화 구조 40개로** 학습해 순위 예측 | Stage 01 이 20 구조 생성 → Stage 03 이 **per-group Top-1** 로 배열 다양성을 죽인다 | 🔴 **Ataya 가 정확히 우리 병을 기술한다.** 게다가 우리는 완화 전 판정(`screen_dV_over_V0` 무효축 판정)까지 겹쳐 있다 |
| **argyrodite S/Cl 무질서** | **Du 2025** [178]: 적절한 S/Cl 무질서가 확산경로 **연결성**을 높여 σ 개선. 동시에 **uMLIP 은 학습공간 밖 일반화 실패** | Stage 02–10 이 전부 **UMA-s-1p1(omat)** 위. UMA 의 argyrodite 무질서 방향 검증 **미실행**(Task #30 pending) | 🔴 **리뷰가 우리 미검증 항목을 정면으로 지적하는 인용을 갖고 있다.** Du 2025 원문 확보 우선순위 ★ |
| **CV 형식** | **LOGO-CV 를 권고만.** SSE 내 수행 사례 **0건**. 근거 인용은 유기재료 논문 | **LODO −0.1805 / 쌍 LOOCV 0.0892 / L2DO −0.2548** 실측 보유 | ⭕⭕ **우리가 앞선다.** §11-B 참조 |
| **surrogate hit rate** | **Maevskiy: 상위 10 중 8 확인** — 리뷰 통틀어 유일한 hit rate | Stage 02↔10 hit rate **미보고** | 🔴 우리 없음. 단 문헌도 1건뿐이라 **격차가 작다** |
| **기계 게이트 비중** | Fig. 3 에서 기계는 **4번째** 게이트 (G > 8.5 GPa, figure-read). 기계를 **1차 게이트**로 쓰는 캠페인은 §6.5 표 13건 중 **Sun [50] · Ahmad [98] 2건**뿐 | **07+08 = no-MD 예산의 75–85 %** 를 앞단에서 소비 | 🔴 **문헌 배치와 어긋난다.** 리뷰가 기계를 앞에 두지 않는다 |
| **BVSE 위상** | **Xie [158]: BV-KMC 로 ~50,000 → 329** — bond-valence 를 **1차 대량 게이트**로 쓴 정면 사례. GCN 을 **BVEL 위에** 학습시키면 원자구조만 쓴 모델보다 **낫다** | Stage 05 BVSE 를 랭킹축으로. 단 **R0 파라미터가 정본과 다름**(Li–Cl exp 항 2.50배) · 자체 재검사 **ρ≈0.22** | 🟡 **개념은 문헌 표준과 일치.** 우리 문제는 개념이 아니라 **파라미터와 단일 서술자 사용법** |
| **도펀트 캐스케이드 선례** | **Wan DopNetFC [159]: LGPS 에 2,208 치환** → ML → 다단 DFT(열역학·전자·기계) | **91 화합물 × 3 농도 = 273** | 🟡 규모는 문헌 대비 1/8. **단 우리는 실제 MD 까지 간다** |
| **능동학습** | 게이트가 아니라 **비싼 라벨 획득**과 **Pareto 탐색**에 붙는다. Lee 2024 = 18,133 → **DFT 144회** | **없음** | 🔴 **우리에게 0.** Stage 02 에 acquisition 하나 얹는 것이 문헌 표준 진입 최단거리 |
| **폐루프에 실험** | Fig. 4(f) · Fig. 5(e-iv) · CAMEO · Electrolytomics · NaₓLi₃₋ₓYCl₆ 전부 **실험 노드 포함** | Stage 12/12b 는 **계산 내부 폐루프** | 🟡 우리 여건상 당장 불가 — **한계로 명시**할 것 |

---

## 8. 적용 인사이트 — 우리 캐스케이드 재설계에 바로 쓰는 것

① **Pareto 로 갈아탄다 (Stage 09a).** 리뷰가 SSE 다목적 최적화의 **표준으로 제시하는 것은 4차원 Pareto**
   (Lee 2024 antiperovskite · Lee 2025 Na-argyrodite 둘 다). 우리 3축 가중합 스칼라는
   CLAUDE.md 의 *"admissible state 여럿 + 집계 규칙 없음 → 스칼라 보고량 미정의"* 판정에 직접 걸리고,
   리뷰의 §5.2 비판에도 정면으로 걸린다. **비용 0 — 기존 CSV 재집계.**

② **단별 제거율을 보고형식으로 만든다.** §6.5 표가 보이듯 **문헌 13건 중 단별 감쇄를 공개한 것은 2건**이고
   그나마 1–2 단뿐이다. 우리가 Stage 00–12 각 단의 (입력수, 통과수, 통과율, GPU-h) 를 표로 내면
   **문헌에 없는 보고형식**이 된다. `kb/reviews/litdb_dopant_sota_2026_09_09.md` §3.2 가 이미 게이트별
   생존수(91 → 45 → 36 → 13)를 계산해 뒀다 — **형식만 맞추면 된다.**

③ **LOGO-CV 를 우리 이름으로 선점한다.** 리뷰가 LOGO-CV 를 권고하면서 근거로 든 유일한 인용이
   **유기재료 논문**이다. **SSE 도메인에서 group-out 낙차를 실측 보고한 사례가 이 리뷰 범위(refs 226편) 안에 없다.**
   우리 **쌍 LOOCV 0.0892 → LODO −0.1805 (낙차 0.27)** 은 그 자리에 정확히 들어간다.
   ⚠ 단 발표할 때 **그룹 정의(도펀트 통째 / 도펀트쌍)** 를 명시해야 한다 — 리뷰조차 그룹 정의를 안 준다.

④ **MD 검출하한을 He 2018 형식으로 선언한다.** TMSD ≥ 450 Å²(RSD 50 %) / > 4150 Å²(RSD 20 %) 가
   **리뷰가 SI 에 넣은 유일한 정량 실무 기준**이다. 우리 200 ps 궤적에서 TMSD 를 후처리로 뽑는 것은
   **추가 계산 0** 이고, 이걸 못 넘는 후보는 *"확산을 못 봤다"* 로 분리하면 kahle2020 관례와도 맞는다.

⑤ **Ataya 를 우리 무질서 처리의 인용 근거로 쓴다.** *"Coulomb 기반 배열선택이 DFT 완화 후 최저에너지를
   놓쳐 ESW 를 0.6 eV 과대평가한다"* 는 우리 Stage 03 의 per-group Top-1 문제를 **문헌 언어로** 말해 준다.
   해법 형식(SOAP-KRR, DFT 완화 구조 40개)도 우리 규모에 맞는다.

⑥ **능동학습은 Stage 02 가 아니라 "비싼 라벨" 에 붙인다.** 문헌 사례 3건 모두 AL 을 게이트가 아니라
   **DFT 탄성 · DFT ESW · Pareto 탐색** 같은 비싼 라벨 획득에 쓴다. 우리 07+08(예산 75–85 %)이
   정확히 그 자리다 — 전수 273 대신 **AL 로 고른 부분집합**만 돌리는 것이 문헌 표준.

⑦ **Haven=1 규약에 문헌 반증 두 건이 붙었다.** Dai 2022 (H_R 0.1–0.4) · Gigli 2024 (NE 가 σ 를 2배 이상
   과소평가). 우리 `adeli2019` digest 의 H_R 0.235–0.315 와 방향이 일치한다.
   ⇒ **규약 자체를 바꾸자는 게 아니라, 우리 σ 에 "H_R=1 가정" 을 라벨로 달아야 한다**는 근거가 3중이 됐다.

---

## 9. 인용 가능 문장 (deck/paper 용)

- *"A 2026 Materials Horizons review of ML pipelines for solid-state electrolytes recommends leave-one-group-out
  cross-validation as the realistic performance assessment for novel chemistries, but the only supporting
  demonstration it cites is from molecular materials — **no SSE screening study in its 226 references reports a
  group-out validation result**."*  ⭕ (전수 검색 근거 §6.12)
- *"The same review reports that state-of-the-art SSE screening funnels span 32 million to 4,375 input
  candidates, yet **only two of the thirteen campaigns it summarises disclose the survival fraction of any
  individual gate**."*  ⭕
- *"Multi-objective SSE screening in the current literature is done with **Pareto fronts** (4-dimensional in both
  Lee 2024 and Lee 2025), and the review explicitly states that single-objective, conductivity-maximising
  approaches 'fail to capture these trade-offs and produce materials unsuitable for practical applications.'"* ⭕
- *"Gate ordering in published SSE funnels is justified by **cost** ('fast and inexpensive filters first'), and
  **no ordering-sensitivity study appears in the review**."*  ⭕
- ⛔ *"Fig. 3 의 임계값(E_hull < 0.2 eV/atom, G > 8.5 GPa, σ > 10⁻⁴ S/cm)이 이 분야의 합의 기준이다"* —
  **쓰면 안 된다.** 그림에만 있고 본문 근거가 없으며, 같은 그림의 밴드갭 항목이 부호·단위 모두 틀려 있다.

---

## 10. 주의 / 한계 — 이 리뷰의 결함 (비판)

🔴 **1. 동일 문단이 두 번 인쇄돼 있다.** §3.4 말미(p. 24)와 §4.1.1 말미(p. 26)에 *"Models trained
predominantly on computational data face inherent challenges … experimental measurement uncertainties.¹⁴²"*
가 **4문장 그대로 중복**된다(뒤 절만 다름). 편집 실수이지만 **하필 그 문단이 이 리뷰의 검증 철학 문단**이라,
"강조" 로 오독하기 쉽다.

🔴 **2. 참고문헌 154 와 218 이 동일 논문이다.** 둘 다 `C. Chen, D. T. Nguyen, … M. Troyer, J. Am. Chem. Soc.,
2024, 146, 20009–20018`. 같은 캠페인이 §4.2 에서는 "Chen et al. 32 M 스크리닝", §5.5 에서는
"a computational-experimental pipeline … NaₓLi₃₋ₓYCl₆" 로 **서로 다른 사례처럼** 등장한다.
⇒ **리뷰의 "폐루프 성공사례 5건" 중 1건은 앞서 센 것과 같은 것이다.**

🔴 **3. CHGNet 이 잘못 인용돼 있다.** §3.4 의 CHGNet 설명이 **ref 106** 을 단다. ref 106 =
`D. Park, W. Chung, B. Min, U. Lee, S. Yu, K. Kim, npj Comput. Mater. 2024, 10, 226` = **HDBSCAN Na 군집화 논문**이다.
CHGNet 원전(Deng et al.)이 아니다. ⇒ **CHGNet 관련 서술을 이 리뷰 경유로 인용하면 안 된다.**

🔴 **4. ref 221 이 깨져 있다.** `A. M, D. Ss, S. W and P. Ka, PubMed.` — 저자 이니셜만 남고 제목·저널·연도가
없다. 그런데 이 인용이 **생성모형 검증 3층 필터의 2층(kinetic accessibility / amorphous limit)** 을 떠받친다.

🔴 **5. Fig. 3 의 밴드갭 게이트가 물리적으로 틀렸다** (figure-read, §5.1). `E_gap < 0.5 eV/atom` — 부등호 방향이
SSE 요구(넓은 갭)와 반대이고 단위가 원자당이다. **이 리뷰의 유일한 정량 깔때기 그림에서 우리 축(전자절연)에
해당하는 칸이 틀렸다.**

🟡 **6. 연도 불일치.** Seth = 본문 "2025" / Table 2 "2024" / ref 165 "2025". Yang = 본문 "2025" /
ref 166 "J. Mater. Chem. A, **2024**, 13, 2309". Maevskiy 는 ref 148(PRR 2025)과 ref 203(arXiv 2411.06804)이
같은 작업의 저널판/프리프린트로 보이는데 **다른 사례처럼** 인용된다.

🟡 **7. σ 목표값이 리뷰 안에서 10배 갈린다** (§3.1: `>1 mS/cm` vs §5.2: `≥10⁻⁴ S/cm` vs Fig. 3: `>10⁻⁴ S/cm`).

🟡 **8. 정량 성능 보고가 극히 얕다.** §6.5 의 13개 캠페인 중 **CV 형식 명시 0건**, **hit rate 보고 1건**
(Maevskiy 8/10), **단별 제거율 2건**, **베이스라인 대비 0건**. 리뷰가 스스로
*"lack of standardized evaluation metrics have hindered systematic progress"* 라고 쓰면서
**자기 표에서도 그 지표를 요구하지 않는다.**

🟡 **9. "다가이온을 정면으로 다룬다" 는 차별점이 대부분 정성이다.** Table S3 는 전부 서술형 등급
(ABUNDANT / SCARCE / POOR TRANSFER)이고, 다가이온 σ·Ea 의 정량 분포는 **[ref 225 = Yang 2024] 한 편에
"tens to low hundreds" 로만** 걸려 있다.

⚪ **10. AI 사용 선언.** *"Claude 4.5 and Gemini 2.5 were used to improve the clarity of selected manuscript
sections; all content was reviewed and verified by the authors."* 위 1–4 (중복 문단 · 중복 참고문헌 ·
CHGNet 오인용 · 깨진 참고문헌)은 **저자 검토가 그 선언만큼 촘촘하지 않았다**는 신호로 읽는 것이 정직하다.
⛔ 다만 이것을 **"AI 가 썼으니 틀렸다"** 로 확대하지 않는다 — 위 결함들은 AI 없이도 흔한 리뷰 편집 결함이다.

⛔ **11. 이 논문 값 인용 금지 규율.** 이 digest 의 모든 수치는 [리뷰 경유]다.
`comparison_vs_ours.md` 의 **A–D 물성 4축 표에 넣지 않는다** (σ·ESW·탄성·gap 자체값이 0건).
쓰려면 원 논문 PDF(Xie 158 · Lee 155 · Wan 159 · Du 178 · Gigli 163 · Ataya 150 · Maevskiy 148)를
**따로 먹여야** 한다.

---

## 11. ★ 우리 좌표 — Stage 00–12 ↔ Jain 파이프라인 어휘 한 줄씩 매핑

### 11-A. 우리 스테이지 → 문헌 어휘

| 우리 Stage | Jain 어휘 (Fig. 번호) | 대응 | 문헌 최전선과의 거리 |
|---|---|---|---|
| **00 preflight** | (없음) | ❌ **문헌에 대응 없음** | 위생 절차. 리뷰에 개념 자체가 없다 |
| **01 substitute** (91 화합물 × 3 농도 = 273) | **Fig. 3(a) Chemical space generation — elemental substitution + defects** | ✅ **정확히 대응** | 규모: 문헌 2,208(Wan, LGPS 도핑) · 4,375(Lee, Na-argyrodite) · 18,133 · 43,732 · 32 M. **우리 273 은 문헌 최소치의 1/8** |
| **02 UMA 스크린** | **Fig. 3(b) ML-based property prediction** (대리모형 1차 필터) | ✅ 대응 | 문헌은 이 자리에 **M3GNet / CGCNN / XGBoost**. **hit rate 를 보고하는 곳이 Maevskiy 1건뿐** |
| **03 winners** (수렴 + ΔV<25 %) | 🟡 부분 — Fig. 3 깔때기의 **어느 단에도 없다** | ⚠ **문헌에 없는 단** | Ataya[150] 가 "완화 후 배열 순위" 문제를 다루지만 **게이트가 아니라 샘플링 방법론**으로 다룬다 |
| **04 anneal** (500 K 50 ps FIRE) | ❌ 없음 | ⚠ **문헌에 없는 단** | Fig. 4(c) MLIP-accelerated simulation 의 일부로 뭉뚱그려짐 |
| **05 BVSE** | **Fig. 1(b) Structural descriptor** + **Xie[158] 의 BV-KMC 게이트** | ✅ 대응 | ★ **Xie 가 정면 선례**: BVEL 위에 GCN 을 학습시키면 원자구조만 쓴 모델보다 낫다. **우리는 BVSE 를 단일 스칼라로만 쓴다** |
| **06 rerank** (랭킹 플립 탐지) | ❌ **없음** | ⚠⚠ **문헌에 전혀 없는 단** ★ | 리뷰 226 refs 어디에도 랭킹 안정성/플립 개념 없음. **우리 고유** |
| **07 MLIP EOS** | **Fig. 1(b) Structural / Fig. 3(b)** | 🟡 부분 | V₀ 를 랭킹축으로 안 쓴다 → 문헌 어휘로는 "서술자를 만들고 버리는" 상태 |
| **08 MLIP 탄성** | **Fig. 3(c) 4단 Mechanical stability (G > 8.5 GPa)** | ✅ 대응하되 **위치가 다르다** | 문헌은 **4번째** 게이트. 우리는 사실상 1–2번째이고 예산의 75–85 % |
| **09a combine** (3축 가중합) | **Fig. 5(b) Multi-objective optimization** | 🔴 **대응하되 형식이 낡음** | 문헌 표준 = **Pareto front**(4D ×2건). 리뷰가 스칼라 단일목적을 명시적으로 비판 |
| **09b collect** | (파이프라인 위생) | ❌ 없음 | — |
| **09c ML 예측기** | **Fig. 1(c) ML models** + **Fig. 3(b)** | ✅ 대응 | **검증 형식에서 우리가 앞선다** (§11-B) |
| **09d DFT 입력 Top-10** | **Fig. 3(c) 6단 Final evaluation — DFT/AIMD validation** | ✅ 대응 | 문헌은 여기서 **AIMD 로 σ 를 다시 잰다**(Chen 2025 · Lee 2025 · Sun 50). 우리는 DFT 정적 |
| **09e ehull (MP)** | **Fig. 3(c) 1단 Thermodynamic stability** (E_f < 0.1 · E_hull < 0.2 eV/atom) | ✅ 대응하되 **순서가 반대 + 무력** | 문헌은 이걸 **맨 앞**에 두고 Chen 2024 에서 **98.2 %** 를 자른다. 우리는 맨 뒤 + **탈락 0종** |
| **09f "ESW"** | **Fig. 3(c) 3단 Electrochemical stability** | 🔴 **이름만 대응** | `esw_check.py` 가 스스로 *"NOT real ESW"* 선언. ⇒ **우리 캐스케이드에 문헌 3단이 없다** |
| **(없음)** | **Fig. 3(c) 2단 Electronic conductivity (밴드갭)** | ❌ **우리에게 없다** | gap 은 진단용. anderson2024 가 Co·Ru·Cu·Ir 의 σ_e 상승을 지적하는데 우리 91종에 그 산화물들이 있다 |
| **10 σ_Li MD** | **Fig. 3(c) 5단 Ionic conductivity (σ > 10⁻⁴ S/cm)** + **Fig. 4(c)** | ✅ 대응하되 **보고량이 다르다** | 문헌 = 절대 σ_RT 임계. 우리 = 상대비 D_rel ≥ 0.90. **문헌 표와 같은 칸에 못 놓는다** |
| **11 NCM 접착 W_ad** | 🟡 §5.2 *"Good electrode compatibility"* 요구사항에 있으나 **Fig. 3 깔때기에는 없다** | ⚠ | 문헌 깔때기가 계면을 **게이트로 안 쓴다**. 리뷰 §6 은 계면 데이터 부족을 최우선 공백으로 지목 |
| **12 / 12b 재학습** | **Fig. 4(f) → (a) 폐루프** · **Fig. 5(e-iv)** | ✅ 대응하되 **노드 하나가 빠짐** | 문헌 폐루프는 **실험 노드**를 포함(CAMEO · Electrolytomics · NaₓLi₃₋ₓYCl₆). 우리는 계산 내부 루프 |

### 11-B. **문헌에 없는데 우리에게 있는 것** ★★ (사용자 요청 핵심)

| # | 우리 것 | 리뷰 226 refs 에서의 상태 | 왜 우리 자리인가 |
|---|---|---|---|
| **1** | **Stage 06 rerank — 랭킹 플립 탐지** | **개념 자체가 0건.** `ranking stability` · `rank flip` · `ordering` 어느 것도 안 나온다 | 스크리닝의 **자기 감사 장치**. 문헌 깔때기는 한 번 자르고 안 돌아본다 |
| **2** | **LODO / L2DO 실측 낙차** (쌍 LOOCV **0.0892** → LODO **−0.1805** → L2DO **−0.2548**) | LOGO-CV 를 **권고만** 하고 SSE 수행 사례 **0건**. 근거 인용[188]은 **유기재료 논문** | ⭐ **가장 확실한 선두 자리.** 리뷰가 스스로 필요하다고 쓴 것을 아무도 안 했다 |
| **3** | **게이트별 생존수 실측** (91 → SE‖LPSCl 45 → +양극 36 → +Li 음극 13, Xiao 100 meV 컷) | 단별 제거율 보고 **2건뿐**(그나마 1–2 단) | §6.5 표가 증명. **보고형식 자체가 기여** |
| **4** | **계면 반응성 ΔE_rxt pseudo-binary 데이터 89종** (`cascade_stability_axes.csv`) | Fig. 3 깔때기에 **계면 게이트 없음.** §6 결론이 *"interfacial properties … systematically underrepresented"* 라고 공백 선언 | ⭐ **리뷰가 직접 "여기가 비었다" 고 쓴 칸에 우리는 데이터가 이미 있다** |
| **5** | **PS₄ libration/재배향 통계** (T16: 500–1000 K 재배향 **0/71**) | 리뷰의 다원자 음이온 회전 서술은 **Gigli 의 PS₄ flip 반박**과 **Yang 의 Cl 회전** 2건뿐. 도펀트가 회전자유도를 어떻게 바꾸는지는 **0건** | 인접 공백. shin2026·tu2026 digest 에서 이미 두 번 확인됐다 |
| **6** | **BVSE 채널 퍼콜레이션 개념** (`migration_volume_fraction`) | Xie[158] 의 BVEL 은 **에너지 지형 자체**를 GCN 입력으로 넣지만 **퍼콜레이션/병목반지름 서술자는 없다** | 우리 쪽이 물리적으로 더 명시적. 단 **R0 파라미터 오류를 먼저 고쳐야** 주장 가능 |
| **7** | **단일 host 안의 무질서 배열 다양성 정량** (jun2022 실측: 같은 50 % 점유, 다른 배열 σ 23.3 vs 37.1) | Ataya[150] 가 **배열 선택이 ESW 를 0.67 eV 틀리게 한다**고만. 배열 다양성을 **깔때기 축으로** 쓰는 사례 0 | 우리 Stage 03 이 지금 이걸 **죽이고 있다** — 고치면 문헌에 없는 축이 된다 |

### 11-C. **우리에게 없는데 문헌에 있는 것** (반대 방향)

| # | 문헌 것 | 우리 상태 | 최단 진입 경로 |
|---|---|---|---|
| 1 | **Pareto front 다목적 집계** (4D ×2건) | Stage 09a = 가중합 스칼라 | 기존 CSV 재집계, **계산 0** |
| 2 | **능동학습**(라벨 획득 + Pareto 탐색) | 0 | Stage 07/08 을 전수 → AL 부분집합으로. Lee 2024 형식(18,133 → DFT 144) |
| 3 | **전자절연 게이트(밴드갭)** | 진단용만 | 09c 예측기에 gap 축 추가 (문헌은 `>3 eV`, Chen 2024) |
| 4 | **실제 ESW 게이트** | 09f 는 ESW 아님 | comp1/modelc 의 grand-potential 절차를 도펀트계로 확장 |
| 5 | **AIMD 최종 검증** | 09d 는 DFT 정적 | Chen 2025 · Lee 2025 · Sun 50 이 전부 마지막에 AIMD |
| 6 | **MD 통계 수렴 판정** (TMSD/hop 수) | 없음 | He 2018 기준을 기존 궤적에 **후처리**, 계산 0 |
| 7 | **Haven ratio 비-1 처리** | H_R = 1 못박힘 | 기존 200 ps 궤적에서 후처리 가능, 계산 0 |
| 8 | **XAI(SHAP) 특징 중요도** | 0 | 09c 예측기에 SHAP 붙이기. ⚠ 리뷰가 경고한 **상관 특징공간 불안정** 주의 |
| 9 | **전이학습** | 0 | 현 규모에서는 우선순위 낮음 |
| 10 | **생성모형 / 폐루프 실험** | 0 | 여건상 불가 — **한계로 명시** |
| 11 | **surrogate hit rate** | 0 | Stage 02 순위 4분위 × Stage 10 결과, **계산 0** |

---

## 12. 🚧 이 논문이 못 하는 것 / 내가 확인 못 한 것 (필수 절)

### 12-A. 이 논문이 구조적으로 못 하는 것

1. **1차 근거가 될 수 없다.** 자체 계산·실험 0건. 모든 수치가 2차 인용이고, 원 논문의 방법 조건
   (범함수·k-mesh·창·무질서 처리)이 **거의 전부 소실**돼 있다.
2. **단별 제거율·게이트 순서 근거·CV 형식 — 셋 다 못 준다.** (§6.5·§6.6·§6.12)
3. **argyrodite 전용 처방이 없다.** 전수 검색으로 나온 관련 언급 **5건이 전부**이고 **전부 한두 문장**이다 —
   ① Gallo-Bueno[107] Li-argyrodite 구조왜곡 비지도 자동분류 ② **Du[178] Li₆PS₅Cl 의 S/Cl 무질서 ↔ 확산경로
   연결성** ③ Lee[155] Na-argyrodite 4,375 스크리닝 ④ Chen[SI ref 23] 폴리머–argyrodite 계면 classical MD
   ⑤ Cheng[SI ref 27 / 본문 75] Li/Li₆PS₅Cl 계면 AIMD.
   (`hit rate` · `success rate` · `rank flip` · `ranking stability` 는 본문·SI **전부 0건**.)
4. **무질서(SQS/enumerate/배열 다양성) 처리 규범을 못 준다.** Ataya 1건이 전부.
5. **MLIP 검증 표준을 못 준다** — 스스로 *"standardized validation protocols … will be essential"* 이라고
   미래형으로 쓴다.
6. **다가이온의 정량 근거가 얇다** (Table S3 전부 정성 등급).
7. **비용/시간 회계가 없다.** 어느 단이 몇 GPU-h 인지, 예산이 어디로 가는지 **한 줄도 없다.**
   우리가 §3.1 에서 계산한 "07+08 = 예산 75–85 %" 같은 논의를 문헌에서 지원받을 수 없다.

### 12-B. 내가 확인하지 못한 것

- **그림**: 크로핑 12장 중 **fig_1 · fig_2 · fig_3 · fig_4 · fig_5 = 5장 전부 실제로 봤다.**
  **표 7장(tab_1–4, tab_S1–S3)은 이미지로 안 봤다** — PDF 텍스트로 전문을 읽었고 표는 글자라 텍스트가 정확하다.
  그림 5장 중 **본문 서술과 어긋난 것은 Fig. 3 하나**(밴드갭 게이트 부호·단위, §5.1·§10-5).
  나머지 4장은 캡션·본문과 일치했다.
- **원 논문을 하나도 안 열었다.** 위 수치는 전부 리뷰 텍스트 기준이다. 특히 우리에게 중요한
  **Xie[158](BV-KMC) · Lee[155](Na-argyrodite 4D Pareto) · Wan[159](LGPS 2,208 치환) · Du[178](S/Cl 무질서
  + uMLIP 일반화 실패) · Ataya[150](배열 샘플링) · Maevskiy[148](hit rate 8/10) · Gigli[163](NE 2배 과소)**
  7편은 **원문 확보 우선순위 ★** 다.
- **ref 188 (Zhao/del Cueto/Troisi, Digital Discovery 2022)** 을 안 읽었다. LOGO-CV 의 정확한 프로토콜
  (그룹 정의·낙차 크기)은 **그 논문을 봐야** 안다. 우리가 "SSE 최초" 를 주장하려면 이 편은 **필독**이다.
- **§6.5 표의 "총 생존율" 은 내가 계산한 파생값**이다(최종/시작). 리뷰에는 없다.
  단계 사이 수가 비어 있어 **단별 제거율로 분해할 수 없다** — 그래서 §6.5 에 "미보고" 로 남겨 뒀다.
- **Table S3 의 정성 등급을 정량으로 바꾸지 않았다** — 리뷰가 그대로 정성이라 옮길 근거가 없다.
- **`comparison_vs_ours.md` · `INDEX.md` 를 갱신하지 않았다** (동시 작업 충돌 회피 지시).
  초안은 `litdb/_pending_index_jain2026.md` 에 있다.
- **talk 역링크 없음** — `litdb/talks/lee2026_skku_mlip_materials_design.md` 의 인입 대기열(9건)을 확인했고
  **이 논문은 그 표에 없다.** 따라서 역링크 단계는 해당 없음.

---

## 13. 한 문장 정리

> **이 리뷰는 SSE 스크리닝 깔때기의 *모양*(열역학 → 전자 → 전기화학 → 기계 → σ → DFT/AIMD)을 표준화했지만,
> 그 깔때기의 *성능 회계*(단별 제거율 · 순서의 근거 · surrogate hit rate · group-out 검증)는 하나도 표준화하지
> 못했다 — 그리고 그 네 칸이 정확히 우리 Stage 00–12 재설계가 채울 수 있는 칸이다.**

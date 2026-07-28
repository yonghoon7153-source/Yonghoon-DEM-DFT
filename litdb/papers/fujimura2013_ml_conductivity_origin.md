# Accelerated Materials Design of Lithium Superionic Conductors Based on First-Principles Calculations and Machine Learning Algorithms — Fujimura & Seko et al. (Adv. Energy Mater. 2013)

> slug `fujimura2013_ml_conductivity_origin` · DOI `10.1002/aenm.201300060` · type `DFT+AIMD(FPMD)+ML(SVR); 자체 실험 0 — 실험 σ 95점은 문헌 소환 라벨` · PDF `82ea256b/b4d7eb81 (inbox #42, 본문 6 pp = 980–985; SI 미보유 — Fig S1/S2·FPMD/SA 상세는 n/a)` · digested `2026-07-28` · status ✅
> elements: Li, O, Zn, Mg, Al, Ga, Si, Ge, P, As
> methods: DFT, AIMD
> **저자**: Koji Fujimura⁺ / **Atsuto Seko**⁺(공동1저자, [†] equal) / Yukinori Koyama / Akihide Kuwabara / Ippei Kishida / Kazuki Shitara / Craig A. J. Fisher / Hiroki Moriwake / **Isao Tanaka***(교신, tanaka@cms.mtl.kyoto-u.ac.jp) — Kyoto Univ. 재료공학 + JFCC(Japan Fine Ceramics Center) 나노구조연구소 + Osaka City Univ. 기계공학 · Communication · Received 2013-01-16 / online 2013-04-19 · MEXT Grant-in-Aid(Challenging Exploratory Research)

---

## 0. 이 digest를 읽는 법 — ML×이온전도 예측의 1세대 앵커(2013)
이 논문은 **"고온 FPMD(AIMD) 기술자 + 실험 σ 라벨을 하나의 커널 회귀(SVR)로 묶어, 아직 안 재본 조성의 *저온*(373 K) 전도도 지도를 그린다"** 는 설계의 역사적 원조격(2013). 물질은 우리와 다른 **LISICON 산화물**(γ-Li₈₋c A_a B_b O₄)이지만, 우리가 2026년에 TabPFN/ICL로 하려는 것의 **1세대 조상**이라 계보·방법론 교훈용으로 필수. 동시대에 Jalem 2012 NN(ref [9])도 있었으므로 "최초의 ML×배터리"가 아니라 **"HT-AIMD 고온 확산계수를 *기술자*로, 실험 σ를 *라벨*로 쓰는 이론-실험 혼합 회귀"의 원조**로 특정해서 인용할 것. 핵심 물리 기여는 ML 이전에 두 개: ① **저온 외삽이 왜 실패하는가 = Li 팔면체-자리 질서화(Tc)** 를 DFT로 정량화, ② **"부피가 크면 확산 빠르다" 통념을 92조성 스크리닝으로 반증**하고 팔면체 Li 점유율 p_Oct를 1차 인자로 제시.

## 1. 한 줄 요약
γ-LISICON(Li₈₋c A_a B_b O₄; A=Zn/Mg/Al/Ga/P/As, B=Ge/Si) 92조성에 대해 **1600 K FPMD 확산계수 D₁₆₀₀ + 질서-무질서 전이온도 Tc + 무질서 부피 V_dis**를 전수 계산(정적 2684회)하고, 이를 **실험 전도도 95점**과 함께 **가우시안-커널 SVR**에 넣어 **372조성 아닌 72조성의 σ(373 K) 지도**를 예측(log σ 오차 0.373) — **γ-Li₄GeO₄가 전체 1위**(단 γ상 미합성), LISICON 원조 Li₃.₅Zn₀.₂₅GeO₄가 왜 최고였는지(고 D₁₆₀₀·저 Tc)를 재현.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 시스템 | LISICON: LiO₁/₂–AO_m/₂–BO_n/₂, 일반식 **Li₈₋c A_a B_b O₄ (c = ma + nb)** [ref 1 Robertson/West 1997] |
| 역사 | 원조 LISICON **Li₃.₅Zn₀.₂₅GeO₄** σ > 10⁻¹ S/cm @ 673 K [ref 2 Hong 1978] — 이후 수십 년 데이터 축적에도 **설계 원리 부재** |
| 문제 | 그룹 간 실험값 산포 큼(refs 2–6, SI Fig S1); 복잡 무질서 고용체라 NEB식 saddle-point 탐색 곤란(협동 이동 [17,18]) → **FPMD가 대안**(경로 선험 지정 불필요) |
| 그러나 | FPMD는 **고온에서만** 통계적으로 유효(짧은 시간창에 점프 수 확보) — 저온 σ는 직접 못 구함 [ref 30 = Mo/Ong/Ceder 2012 LGPS 계열도 고온만] |
| 해법 | 고온 이론 기술자 + 실험 라벨을 **ML(SVR)** 로 연결해 373 K 예측 |
| 선행 ML | HT+ML 배터리 탐색 [7–9] (Mueller/Hautier/Ceder 2011, Jalem 2012 NN) — 인용만, 본 논문이 "AIMD-기술자+실험-라벨" 혼합 설계 |

## 3. 구조·상평형 배경 (Fig 1a,b)
- 의사이원계 **Li₂ZnGeO₄–Li₄GeO₄** 상도 [ref 21 Bruce & West 1980]: α(l-Li₄GeO₄)·β·γ 3다형 — 모두 **hcp 산소 부격자**, Ge/Zn은 사면체 자리, 다형 차이는 [GeO₄] 사면체 배향 [23]. γ 고용체 영역이 중앙 광역(Fig 1a 노랑).
- **Li 자리** [중성자, ref 22 Abrahams/Bruce/West]: 결정학적 비등가 4곳 — Li_A = 4c(1)/4c(2)(c축 교대), Li_B = 4a/4b(c축 교대). 일부 Li는 남은 사면체 자리, **나머지는 팔면체 자리** — **팔면체 부분점유가 전도의 열쇠**라는 가설(ref 22)이 이 논문 Tc·p_Oct 설계의 출발점.
- 고전도 LISICON은 대부분 γ상 → 스크리닝은 **γ 골격 고정** 전제(§5.3의 한계이기도).

## 4. DFT/계산 방법 ★
- **code**: VASP [27] · **PAW** [24,25] · **GGA(PBE)** [26]. vdW 없음, DFT+U 없음.
- **ecut 300 eV** · 총에너지 수렴 < 10⁻² meV/cell · **k = Γ-point only** (2013 HT 규모 타협 — ⚠ 우리 기준으론 soft).
- **FPMD(AIMD)**: **NVT, Nosé thermostat** [28] · **셀 = γ 단위셀 2×1×2 = 16 f.u.** (Li₁₆₋₂c… 규모, 원자수 ~112±) · **dt = 2 fs** · 격자부피 = "무작위 분포 Li"의 **0 K DFT 부피 고정**(NpT 아님 — 열팽창 무시) · 시뮬레이션 시간·잔여 상세 SI(미보유, n/a).
- **온도**: Zn-Ge 계 3조성(x=0.25/0.5/0.75)은 **고온 4점**(Fig 2 축 판독 ≈1250–2000 K 창; 정확 목록 SI n/a) → Arrhenius; 92조성 전수 스크리닝은 **1600 K 단일점**(D₁₆₀₀).
- **무질서 처리** (cluster-expansion형, 우리 template 항목의 "enumerate+평균" 계열):
  - A/B 골격 양이온 배열: **simulated annealing + 단순 점전하 모델**(상세 SI n/a).
  - **질서 구조**: 에너지 극값(최대/최소) 배열 탐색 — cluster expansion 형식에서 **correlation function RMS가 큰 구조**를 후보로 [31 Hart 2007, 32 Seko & Tanaka 2011]. 최소값 = 그 조성의 바닥상태.
  - **무질서 구조**: 팔면체 Li 배열이 다른 **무작위 2×1×2 초셀 20개 에너지 평균**.
  - **엔트로피**: 점근사(point approximation) **TΔS = −k_B T[x ln x + (1−x)ln(1−x)]**, x = 팔면체 자리 Li 점유율. 진동 자유에너지·단거리질서 무시(저자 자인: "quantitative Tc는 overly ambitious").
  - **Tc 정의**: ΔE(무질서 평균 − 질서 바닥) = Tc·ΔS 되는 온도.
- **규모**: FPMD **92조성**(1600 K) + Tc·ΔF^S₁₆₀₀·V_dis **72조성**(셀 크기가 허용하는 순열 수 기준) + 이를 위한 **정적 계산 총 2684회** — 2013년의 HT-AIMD 최전선.
- **D→σ 연결**: 실험 σ ↔ D 비교는 **Nernst–Einstein**(ref [2,29] 실험 σ를 D로 환산해 Fig 2에 병기) — Haven 보정 없음(우리 NE Haven=1 규약과 동일 계열).

## 5. 결과 — 섹션별 상세

### 5.1 Zn-Ge 의사이원계의 질서-무질서 (Fig 1c,d)
- **Tc** (γ상, 4조성): **Li₂.₅Zn₀.₇₅GeO₄ 1150 K / Li₃Zn₀.₅GeO₄ 750 K / Li₃.₅Zn₀.₂₅GeO₄ 380 K** (본문 수치) + x=1(Li₄GeO₄) ≈350 K(figure-read, 본문 수치 없음) → **Zn 감소 = Tc 급감** = 저온까지 무질서(전도 유리) 유지.
- **E^mix₀**(질서 바닥, γ 양끝단 기준): 전 조성 ~0(약음, figure-read −0.1~0 eV/unit cell) — γ끼리는 거의 이상용액.
- **F^mix₁₂₀₀**(무질서 γ, 1200 K, 팔면체 Li 배열 엔트로피만): 최대 ≈−0.65 eV/unit cell(x=1 쪽, figure-read). γ-Li₂ZnGeO₄는 Li가 사면체만 점유 → 배열 엔트로피 0.
- **실험 기지상 대비**: β-Li₂ZnGeO₄ ≈−0.2, α-Li₄GeO₄ ≈**−0.8 eV/unit cell**(figure-read) → **저온 바닥은 β+α 상분리**(상도 Fig 1a와 정합); γ는 고온서 엔트로피로 안정화. α(−0.8) vs 무질서 γ 1200 K(−0.65) 차 ≈0.15 eV/unit cell — 뒤의 "γ-Li₄GeO₄ 합성 희망" 논거.

### 5.2 Arrhenius 검증과 저온 외삽의 실패 지점 (Fig 2)
- FPMD D(고온 4점, x=0.25 청/0.5 적/0.75 흑) vs 실험 σ→NE 환산 D(open circle [2 Hong], open triangle [29 Takai 2004]).
- **x=0.75(원조 LISICON)**: 고온 FPMD 외삽선이 **실험 523–673 K 구간과 잘 맞음** → 이 구간까지는 **동일 전도 메커니즘**(상변화 없음).
- **<523 K**: 실험 Ea 증가(굴절) — 논문 해석 = **팔면체 Li 질서화**(기존엔 막연히 "상전이" [5]; x=0.5는 굴절점 550 K 보고 [6] 기반으로 Fig 2 저온 연장선을 x=0.25와 0.75의 중간 기울기로 그림). **→ 단순 고온 외삽은 저온서 부정확** = ML 도입의 물리적 근거.
- 계산 Tc(380 K, x=0.75)는 실험 굴절(~523 K)보다 낮음 — 점근사 한계(방향은 재현, 절대값 과소).

### 5.3 92조성 HT 스크리닝 (Fig 3) — 이 논문의 물리 하이라이트
- 3계열: **II-IV**(A=Zn,Mg) / **III-IV**(A=Al,Ga) / **V-IV**(A=P,As), B=Ge,Si. 각 계열 **tie line 1**(Li₈₋c A_a BO₄–Li₄BO₄: A가 Li₄BO₄의 Li 치환), **tie line 2**(Li₄BO₄–Li₈₋c AO₄: A가 B 치환). **V-IV는 tie line 2만**(5가 이온의 Li-자리 치환은 에너지적으로 금지적).
- 산출 4종: **D₁₆₀₀**(FPMD) · **Tc** · **ΔF^S₁₆₀₀**(1600 K 고용체 형성자유에너지; 기준 = 끝단 x=0·y=1·x=1=y=0 최저에너지 상 — Fig 1d와 기준 다름 주의) · **V_dis**(무질서 구조 평균 부피). D₁₆₀₀ 범위 ≈(1–8)×10⁻⁹ m²/s(figure-read).
- **🔑 부정 결과 1**: **D₁₆₀₀는 A·B 원소 선택에 둔감**. **🔑 부정 결과 2**: **D₁₆₀₀는 V_dis(격자부피)와 거의 무관** — "부피 크면 확산 빠르다"는 통념을 92조성 규모로 반증.
- **🔑 양성 결과**: 평균 팔면체 Li 점유율 **p_Oct = [(8−c+a+b)−4]/4** 가 확산 크기의 **1차 인자**(tie line 1 전부 + A=5가의 tie line 2). 단 **A=2가/3가의 tie line 2에선 p_Oct 단독으로 설명 안 됨**(예외 명시 — 정직).
- ΔF^S₁₆₀₀: tie line 1은 대체로 ≤0(고용 가능), II-IV tie line 2는 큰 양수(inset ~+1–3 eV/unit cell, Li₆AO₄ 쪽 비혼화) — 합성 가능성 필터로 뒤에서 사용.

### 5.4 ML: SVR로 이론+실험 연결 (본문 984)
- 전제(명문): "**Assuming that the theoretical data are complementary to and consistent with the experimental data**" — 이론-실험 정합성은 *가정*.
- **훈련 데이터**: 실험 전도도 **95 측정점**(여러 조성×여러 온도; 분포는 SI Fig S1 — 미보유라 조성별 커버리지 n/a) = **라벨** / 이론 기술자 D₁₆₀₀·Tc·V_dis = **특징**.
- **모델**: **support-vector regression + Gaussian kernel** [35 = LIBSVM Chang & Lin 2011]. 종속변수 **log σ**; 독립변수 **D₁₆₀₀, Tc, V_dis, (실험)온도 T** — 4특징. 변수 유의도는 SI(n/a).
- **HPO**: 커널 분산·정규화 상수·**독립변수의 함수형**(변환 형태)을 **bootstrap** [36 Efron & Tibshirani]으로 예측오차 최소화. 오차 곡선 SI Fig S2(n/a).
- **성능**: 최적 SVR의 **log σ 예측오차 0.373** ≈ σ로 **×2.36 배** 수준. hold-out/외부검증 없음(부트스트랩 내부 추정).
- Fig 4 캡션의 "**iterative analysis** of calculated and experimental datasets" — 반복 절차의 정체는 본문 미상술(불투명성, §10).

### 5.5 σ₃₇₃ 예측 지도와 최적 조성 (Fig 4)
- **72조성**(Tc·V_dis 가용분)의 373 K 예측 σ 막대지도, 범위 ≈10⁻⁶–5×10⁻⁴ S/cm(figure-read).
- **학습된 물리**: 특징에 Ea가 없는데도 **고 D₁₆₀₀ + 저 Tc → 고 σ₃₇₃** 경향 재현. 저-Zn Li₂₊₂ₓZn₁₋ₓGeO₄(x=0.75, 고D·저Tc) > 고-Zn(x=0.25, 고Tc) → **원조 LISICON Li₃.₅Zn₀.₂₅GeO₄가 왜 역대 최고급인지 설명** = 회귀가 실험 트렌드를 내재화했다는 sanity check.
- **1위: γ-Li₄GeO₄** — 전 72조성 중 최고 σ₃₇₃(figure-read ≈4–5×10⁻⁴ S/cm), **원조 LISICON의 "a few times higher"**(본문). ⚠ 단 실제론 α상으로 결정화(γ 미합성); Fig 1d상 α↔γ의 F^mix₁₂₀₀ 차가 크지 않아 "합성 가능할지도"가 논거.
- **차상위 후보군**(σ₃₇₃ > 원조 LISICON & **ΔF^S₁₆₀₀ < 0**, 본문 명시 리스트): **Li₄SiO₄**, **Li₂₊₂ₓZn₁₋ₓSiO₄(x=0.5, 0.75)**(=Li₃Zn₀.₅SiO₄, Li₃.₅Zn₀.₂₅SiO₄), **Li₃.₅Mg₀.₂₅SiO₄**, **Li₃.₂₅Al₀.₂₅SiO₄**, **Li₄.₂₅A₀.₂₅Si₀.₇₅O₄(A=Al,Ga)**, **Li₃.₅P₀.₅Si₀.₅O₄**, **Li₃.₇₅A₀.₂₅B₀.₇₅O₄(A=P,As; B=Ge,Si)**.
- **검증**: "Focused experiments … currently being performed" — **논문 내 실험 검증 없음**(2013 시점 진행 중 선언만). ⚠ 큐레이터 주(논문 밖 지식, 수치 인용 금지): 후보 중 P–Si 계열(Li₄SiO₄–Li₃PO₄ 고용체, 예: Li₃.₅P₀.₅Si₀.₅O₄)은 원래부터 알려진 LISICON 고전도 조성족과 겹침 — "재발견" 성격도 있음.
- 결론부: 방법은 의사이원계에 국한 안 됨 — "systematic first-principles DB만 있으면 더 복잡한 화학에도" = HT-DB+ML 시대 선언(2013).

## 6. ★ ML 모델 스펙 카드 (요청 최우선 항목 — 한 표로)
| 항목 | 내용 |
|---|---|
| 기법 | **SVR(support-vector regression) + Gaussian kernel** (LIBSVM [35]) |
| 타깃(라벨) | **log σ** — *실험* 전도도 (여러 온도) |
| 특징(입력) 4개 | **D₁₆₀₀**(FPMD 1600 K 확산계수) · **Tc**(질서-무질서 전이온도, DFT+점근사 엔트로피) · **V_dis**(무질서 평균 부피) · **T**(측정 온도) — *이론 3 + 조건 1* |
| 훈련 표본 | **실험 95 측정점**(조성×온도; 조성 수 본문 미명시, SI Fig S1 n/a) |
| 이론 데이터 규모 | FPMD 92조성(1600 K) · Tc/ΔF^S/V_dis 72조성 · 정적 2684회 |
| HPO/검증 | 커널 분산·정규화·**특징 함수형**을 **bootstrap 오차 최소화**로 — hold-out/외부 검증 없음 |
| 성능 | **RMSE(log₁₀ σ) = 0.373** (≈ ×2.36 배) |
| 예측 산출 | **σ₃₇₃ 지도, 72조성**(Fig 4) — 대상족 = γ-LISICON 산화물 **단일 구조족 내 보간** |
| 최적 조성 | **γ-Li₄GeO₄**(1위, 미합성 γ상) + Li₄SiO₄·Li₃.₅P₀.₅Si₀.₅O₄ 등 8종(§5.5) |
| 검증 여부 | 논문 내 없음("focused experiments in progress"만) |

## 7. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1a | Li₂ZnGeO₄–Li₄GeO₄ 상도(ref 21 재게재): β/γ/α(α')·liquid | 고용체 스크리닝 전에 상도로 "γ 영역" 고정하는 프레임 |
| 1b | γ-LISICON 구조(c축 투영): [GeO₄]/[ZnO₄]/[LiO₄] 사면체 + 팔면체 Li(파선 원), Li_A(4c)·Li_B(4a/4b) | "전도 부격자(팔면체) vs 골격" 분리 그림 — 우리 cage/48h 그림 문법의 산화물판 |
| 1c | 계산 Tc vs 조성(1150/750/380 K + x=1 ≈350) | **무질서 지속온도를 조성의 함수로** — 우리 disorder ensemble의 "조성→무질서 경향" 정량화 아이디어 |
| 1d | E^mix₀(질서)·F^mix₁₂₀₀(무질서)·실험상(β, α) 상대에너지 | 준안정 γ 고용체 vs 진짜 바닥(상분리) 구분 — E_above_hull 사고의 2013판 |
| 2 | Arrhenius: FPMD 4점(고온) vs 실험 NE-환산 D; 523–673 K 일치, <523 K 굴절 | **"고온 MD 외삽은 질서화 온도 아래서 무효"** — 우리 600–1000 K 3점 규율·400/500 K 제외와 같은 물리 |
| 3 | 92조성: V_dis / ΔF^S₁₆₀₀ / Tc / D₁₆₀₀ / p_Oct 5단 패널 ×3계열 | HT 스크리닝 결과를 "기술자 대시보드"로 쌓는 시각화 — cascade 축별 패널과 동형 |
| 4 | 예측 σ₃₇₃ 막대지도(72조성) | ML 산출을 "조성 지도"로 제시 — TabPFN 산출물 포맷 참고 |
| S1 | 실험 σ 95점 Arrhenius(문헌 취합) | **라벨 데이터의 산포 공개** 관행(우리도 문헌 소환값 산포 명시) — 미보유 |
| S2 | bootstrap 오차 vs 변수 | 특징 중요도·HPO 투명화 — 미보유 |

## 8. Post-processing ★
- **MSD→D**(FPMD; 창·통계 상세 SI n/a) → Arrhenius(3조성만) / 단일 1600 K(92조성).
- **Nernst–Einstein**: 실험 σ↔D 환산(비교용; Haven 보정 없음).
- **Cluster-expansion 유틸**: correlation-function RMS로 극값 배열 선별 [31,32] + SA(점전하) — 오늘날 pymatgen enumerate/SQS+Ewald 사전선별의 조상격.
- **점근사 배열 엔트로피** → Tc, ΔF^S₁₆₀₀ (자유에너지 = 20-배열 평균 에너지 − T·S_point).
- **SVR(LIBSVM) + bootstrap HPO** → σ₃₇₃ 지도. 도구 시대상: VASP + LIBSVM(2013) — pymatgen/자동화 프레임워크 이전 수작업 HT.

## 9. 우리 DFT/캠페인 대비 → `../our_dft_baseline.md`
| 항목 | Fujimura 2013 | 우리 (comp1/modelc, 2026) | 판정 |
|---|---|---|---|
| 재료 | γ-LISICON **산화물**(Li-O 골격) | argyrodite **황화물**(Li₆PS₅Cl 계) | **물성 수치 직접 비교 전면 금지** — 방법·설계 계보만 |
| 고온 D 엔진 | **FPMD**(VASP·Γ·300 eV·16 f.u.·NVT Nosé·2 fs·0 K 부피 고정) | **MLIP-MD**(UMA-s-1p1, Langevin NVT, 2 fs, 5+200 ps, MSD 2–50 ps) | 같은 목적(고온 D), **힘 계산 축 다름**(AIMD vs MLIP) — "둘 다 AIMD" 표현 금지. 2013 한계(짧은 시간·Γ·단일 배열)를 2026 MLIP가 시간·규모로 해소 |
| 저온 외삽 규율 | **Tc 아래 외삽 금지**(질서화가 Ea 올림; Fig 2) | **Arrhenius 600/800/1000 K 3점, 400/500 K 제외**; 절대 σ 인용 금지(비율·멀티시드만) | **✓ 같은 물리 본능** — 저온·희귀사건 구간을 피팅에서 배제. 그들의 해법=ML 다리, 우리 해법=비율 규율(+장차 TabPFN) |
| 무질서 처리 | 무작위 20배열 평균(에너지) + 점근사 S + FPMD는 **단일 무작위 배열** | disorder ensemble(comp2 d-level·배열별 MD)·enumerate 계열; "ordered=frozen artifact" 확인 | **✓ 방향 일치**: 그들 Tc 서사 = "질서상은 느리다"의 1세대 정량화. 단 그들 동역학은 배열 1개(배열-분산 미정량) — 우리 멀티시드/멀티배열 규율이 후계 |
| D↔σ | NE(Haven=1)로 실험 σ 환산 비교 | NE(Haven=1) σ — 절대값 인용 금지 규율 | ✓ 같은 규약, 우리가 인용 규율만 더 보수적([Adeli] Haven 0.23–0.3 근거) |
| "부피→σ" 통념 | **V_dis와 D₁₆₀₀ 무관**(92조성 반증) | BVSE `migration_volume_fraction`·[Rao] Li Voronoi 부피는 σ와 상관 | **모순 아님** — 그들 V_dis=**전역 격자부피**, 우리/[Rao]=**국소 채널·이동경로 부피**. "부피" 주장할 땐 전역/국소 구분 필수(⚠ [Ma24] 격자팽창 서사에도 같은 경고) |
| 1차 인자 | **p_Oct**(전도 부격자의 운반자/공공 농도) | Cl-rich Li-공공([Adeli] 48h 0.456)·carrier 레버; [Perc] "carrier > pc" | **✓✓ 개념 선례**: p_Oct = "전도 부격자 점유율이 D를 지배" = site-percolation 운반자 논리의 2013 실물. 단 그들도 예외 명시(2·3가 tie line 2) = 단일 기술자 과신 금지 |
| ML 설계 | **이론=특징 / 실험=라벨** 혼합 SVR(95점, 오차 0.373) | 데이터 layer 분리 규율(문헌값=소환, 우리값과 혼합 금지; UMA 절대 σ 금지) + TabPFN ICL 구상 | **긴장이자 교훈**: 혼합은 "학습된 다리"로만 허용(특징/라벨 층 분리 명시) — §11-③ 상세 |
| 스크리닝 범위 | γ-LISICON **단일 구조족 내 보간**(72조성, A/B 8쌍) | 47-dopant cascade(단일 host에 **원소 횡단** 도핑) + DEM 코퍼스 | 서로 다른 축의 "族내": 그들=조성족, 우리=host 고정+도펀트 횡단. 구조족 횡단은 [Sendek17] 세대에서 시작 |

## 10. 주의/한계 (over-claim 방지 — 비판적으로)
- **γ-Li₄GeO₄ 1위는 "합성 안 된 상"에 대한 예측** — α로 결정화(저자 자인). "ML이 신물질 발견" 화법 금지: 논문 내 실험 검증 0, 최상위 후보는 합성 장벽, 차상위엔 기지 조성족 재발견 포함.
- **라벨 이질성**: 95점은 여러 그룹 문헌값 취합 — 저자들 스스로 "그룹 간 산포 큼"(refs 2–6)이라 했으면서 라벨 정규화·불확도 가중 없음. 오차 0.373엔 이 산포가 녹아 있음.
- **검증 설계 약함**: bootstrap 내부 오차만; 조성족 leave-out 없음 → **미측정 계열(V-IV As 등)로의 일반화는 검증 안 된 보간**. "iterative analysis"(Fig 4 캡션) 절차 불투명.
- **기술자 자체의 방법 의존**: D₁₆₀₀는 Γ-only·300 eV·단일 배열·0 K 고정부피 FPMD; Tc는 점근사 엔트로피(진동·단거리질서 무시, 절대값 과소 — 380 vs 굴절 ~523 K). 특징의 계통오차가 조성별로 다르면 SVR이 조용히 흡수(감지 불가).
- **p_Oct 만능 아님**: 2·3가 tie line 2 예외를 저자도 명시 — 단일 기술자 랭킹 인용 금지.
- **γ 골격 고정 스크리닝**: 조성별 실제 바닥상(β/α/상분리)은 ΔF^S·Fig 1d로 부분 점검하지만, FPMD·예측은 전부 γ 가정 — 합성 가능성은 별도 문제.
- **1600 K 단일점 D**: Ea 정보 없음(모델이 Tc로 간접 보완) — D₁₆₀₀ 높아도 저온 급락 가능성은 Tc가 다 못 잡음.
- 시대적 소프트 셋업(Γ, 300 eV, 짧은 MD)은 **비난이 아니라 맥락** — 2013 HT-AIMD 천장. 절대값 재사용 금지, 설계·계보만 인용.

## 11. 적용 인사이트 (내 연구에 어떻게)
1. **ML 세대 계보 한 줄(deck용)**: "σ-예측 ML 3세대 — **Fujimura 2013**(가우시안-커널 SVR·특징 4개(D₁₆₀₀/Tc/V_dis/T)·실험 라벨 95점·γ-LISICON *조성족 내* 보간·log σ 오차 0.37) → **Sendek 2017**(로지스틱 분류, *물질군 횡단* 스크리닝 — `[Sendek17]` digest) → **우리 2026**(TabPFN ICL — 사전학습 prior 소표본 표형 회귀, 47-dopant cascade/DEM 코퍼스)". 1세대의 본질 = *물리 기술자를 사람이 설계*(D₁₆₀₀·Tc)하고 ML은 다리만.
2. **"고온 MD + 저온 다리" 구조는 2013이나 지금이나 동일** — 그들: FPMD 1600 K→SVR→373 K; 우리: UMA 600–1000 K→비율/Arrhenius(→장차 TabPFN 잔차). 우리 deck에서 "왜 RT σ를 직접 안 재나"의 역사적 정당화로 인용.
3. **layer-혼합 교훈(우리 규율과의 긴장 해소)**: Fujimura 혼합은 **특징=이론 / 라벨=실험으로 층이 분리된 '학습된 다리'** — 우리 "문헌값·우리값 혼합 금지"는 *같은 층에 두 출처를 섞지 말라*는 뜻이고, Fujimura형 다리는 허용 가능한 예외 형식. 단 그들이 안 한 것(라벨 출처 가중·조성족 leave-out·특징 계통오차 명시)을 우리가 TabPFN에서 반드시 추가할 것.
4. **p_Oct 선례**: "전도 부격자 점유율(운반자·공공)이 1차, 전역 부피는 허수" — 우리 cascade 서술자 우선순위(공공/blocking > 격자상수)와 [Perc]·[Adeli] 서사의 1세대 인용처.
5. **Tc라는 관측가능한 무질서 지표**: 우리 disorder ensemble에 "질서화 온도" 축을 붙이면(배열 에너지차 + 점근사 S로 즉석 Tc 추정) 문헌과 대화 가능한 숫자가 하나 생김 — 단 점근사 과소 경고 동봉.
6. **부정 결과 공개 관행**: "V_dis 무관·p_Oct 예외 있음"을 본문에 명시한 것이 이 논문의 수명(12년 인용)을 늘림 — 우리 cascade 보고서도 실패 서술자를 지우지 말 것.

## 12. 인용 가능 문장 (deck/paper용)
- "The theory-as-features / experiment-as-labels bridge for ionic conductivity dates back to Fujimura et al. (2013): high-T FPMD diffusivity, order-disorder Tc and cell volume of 72 LISICON compositions fed into a Gaussian-kernel SVR trained on 95 experimental conductivities (log-σ error 0.373) to map σ at 373 K."
- "Already in 2013, high-throughput FPMD screening showed that global cell volume is a poor predictor of Li diffusivity — occupancy of the conducting (octahedral) sublattice, p_Oct, was the principal factor."
- "Fujimura et al.'s Tc analysis formalized why high-temperature MD must not be extrapolated below the Li ordering transition — the same physics behind our 600–1000 K-only Arrhenius discipline."
- "Generation 1 (Fujimura 2013, kernel regression within one structure family) → generation 2 (Sendek 2017, logistic screening across families) → generation 3 (tabular foundation models, in-context learning on small curated corpora)."

## 13. 기법 용어 미니사전
- **LISICON**: Li SuperIonic CONductor — γ-Li₃PO₄형 골격의 Li₈₋c A_a B_b O₄ 산화물 고용체족(원조 Li₃.₅Zn₀.₂₅GeO₄, Hong 1978).
- **FPMD**: first-principles MD = AIMD. 경로 선험 지정 없이 확산 관찰 — 단 고온에서만 점프 통계 확보.
- **cluster expansion / correlation function**: 배열 자유도를 클러스터 함수 전개로 표현; RMS 큰 배열 = 극값 후보(질서상 탐색용) [Hart 2007, Seko 2011].
- **point approximation(Bragg-Williams류)**: 배열 엔트로피를 자리당 −k_B[x ln x+(1−x)ln(1−x)]로 근사 — 단거리질서 무시, Tc 과소 경향.
- **order-disorder Tc**: 질서 바닥과 무질서 평균의 자유에너지 교차 온도 — Arrhenius 굴절(저온 Ea 증가)의 구조적 해석.
- **p_Oct**: 팔면체(전도) 부격자의 평균 Li 점유율 = [(8−c+a+b)−4]/4 — 운반자 농도형 기술자.
- **SVR + Gaussian kernel**: ε-불감 손실의 커널 회귀; 커널 폭·정규화가 유효 복잡도 결정 — 소표본에서 보간엔 강하나 외삽 취약.
- **bootstrap**: 재표집으로 예측오차 추정(Efron) — hold-out 없이 HPO 하는 2013식 절충.
- **Nernst–Einstein**: σ = c q² D / (k_B T)(Haven=1 가정) — 실험 σ↔D 환산 규약.

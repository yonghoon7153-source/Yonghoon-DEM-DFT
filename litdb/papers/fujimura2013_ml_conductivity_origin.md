# Accelerated Materials Design of Lithium Superionic Conductors Based on First-Principles Calculations and Machine Learning Algorithms — Fujimura & Seko et al. (Adv. Energy Mater. 2013)

> slug `fujimura2013_ml_conductivity_origin` · DOI `10.1002/aenm.201300060` · type `DFT+AIMD(FPMD)+ML(SVR); 자체 실험 0 — 실험 σ 95점은 문헌 소환 라벨` · PDF **본문 `litdb/inbox/42. Accelerated Materials Design of Lithium Superionic Conductors Based on First-Principles Calculations and Machine Learning Algorithms.pdf`(6 pp = 980–985)** · **SI 미보유**(Fig S1/S2·FPMD 시간규모·SA 상세·변수 유의도는 n/a) · (inbox #42) · **사용자 분류 폴더 `DFT`** · digested `2026-07-28` · **본문 실물 독립 검증 `2026-08-03`(§14 — 전문 텍스트 추출 + Fig 1/2/3/4 이미지 판독(600–700 dpi 크롭 4매); 교정 6건·신규 적발 5건·미결 0)** · status ✅ **(본문 실물 대조 완료 — SI만 미보유)**
> elements: Li, O, Zn, Mg, Al, Ga, Si, Ge, P, As
> methods: DFT, AIMD
> **저자**: Koji Fujimura⁺ / **Atsuto Seko**⁺(공동1저자, [†] equal) / Yukinori Koyama / Akihide Kuwabara / Ippei Kishida / Kazuki Shitara / Craig A. J. Fisher / Hiroki Moriwake / **Isao Tanaka***(교신, tanaka@cms.mtl.kyoto-u.ac.jp) — Kyoto Univ. 재료공학 + JFCC(Japan Fine Ceramics Center) 나노구조연구소 + Osaka City Univ. 기계공학 · Communication · Received 2013-01-16 / online 2013-04-19 · MEXT Grant-in-Aid(Challenging Exploratory Research)

---

## 0. 이 digest를 읽는 법 — ML×이온전도 예측의 1세대 앵커(2013)
이 논문은 **"고온 FPMD(AIMD) 기술자 + 실험 σ 라벨을 하나의 커널 회귀(SVR)로 묶어, 아직 안 재본 조성의 *저온*(373 K) 전도도 지도를 그린다"** 는 설계의 역사적 원조격(2013). 물질은 우리와 다른 **LISICON 산화물**(γ-Li₈₋c A_a B_b O₄)이지만, 우리가 2026년에 TabPFN/ICL로 하려는 것의 **1세대 조상**이라 계보·방법론 교훈용으로 필수. 동시대에 Jalem 2012 NN(ref [9])도 있었으므로 "최초의 ML×배터리"가 아니라 **"HT-AIMD 고온 확산계수를 *기술자*로, 실험 σ를 *라벨*로 쓰는 이론-실험 혼합 회귀"의 원조**로 특정해서 인용할 것. 핵심 물리 기여는 ML 이전에 두 개: ① **저온 외삽이 왜 실패하는가 = Li 팔면체-자리 질서화(Tc)** 를 DFT로 정량화, ② **"부피가 크면 확산 빠르다" 통념을 92조성 스크리닝으로 반증**하고 팔면체 Li 점유율 p_Oct를 1차 인자로 제시.

## 0.5 처음 읽는 사람을 위한 배경 (이 논문이 전제하는 것들)

**2013년이라는 시점**
지금은 MLIP(기계학습 퍼텐셜)로 MD 를 대신 돌리지만, 2013년엔 그런 게 없었다.
이 논문은 **"비싼 AIMD 를 몇 개만 돌리고 나머지는 회귀로 채운다"** 는 발상 자체를 처음
제대로 보인 것이고, 지금의 MLIP 스크리닝이 하는 일의 **개념적 원형**이다.

**SVR(support vector regression)이 여기서 하는 일**
커널 회귀의 일종이다. 어렵게 볼 것 없이 — **"비슷한 조성끼리는 전도도도 비슷하다"** 는 가정을
수학으로 쓴 것이다. '비슷하다'의 정의가 커널이고, 무엇을 기술자로 넣느냐가 그 정의를 만든다.
여기선 고온 AIMD 에서 뽑은 값들(확산계수·활성화에너지 등)을 기술자로 넣었다.

**왜 고온에서 재고 저온을 예측하나 — 이 논문의 트릭**
MD 로 확산을 재려면 이온이 실제로 움직여야 하는데, 상온에서는 계산 가능한 시간(수백 ps) 안에
Li 가 거의 안 뛴다. 그래서 **1000 K 근처에서 재고** 아레니우스로 373 K 로 외삽한다.
우리 캠페인의 600/800/1000 K 3점 아레니우스가 정확히 같은 이유로 그렇게 생겼다.
⚠ 외삽이므로 고온에서 상전이가 일어나면 그 외삽이 통째로 틀린다 — 항상 확인할 지점.

**라벨의 출처를 보라**
실험 σ 95점은 **문헌에서 긁어온 값**이다. 측정 조건(소결 온도·입계·전극)이 제각각인 값을
하나의 회귀에 넣은 것이라, 절대값이 아니라 **경향**으로만 읽어야 한다.
우리 규율("문헌 수치는 소환값 — 우리 db 절대값과 섞지 않는다")이 여기서도 그대로 적용된다.

---

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
- 의사이원계 **Li₂ZnGeO₄–Li₄GeO₄** 상도 [ref 21 Bruce & West 1980]: α(l-Li₄GeO₄)·β·γ 3다형 — 모두 **hcp 산소 부격자**, Ge/Zn은 사면체 자리, 다형 차이는 [GeO₄] 사면체 배향 [23]. γ 고용체 영역이 중앙 광역(Fig 1a 노랑, 600–1750 K 축). ✎2026-08-03 보완: Fig 1a에는 본문이 안 세는 **α′(고온형, x≈0.9–1 · ~1030 K 이상, 분홍)** 도 표기돼 있다 — 본문의 "three structures"는 α/β/γ를 뜻하고 α′는 α의 고온 변태. β는 좌단(x ≲0.1, ~870 K 이하, 하늘)로 좁다.
- **Li 자리** [중성자, ref 22 Abrahams/Bruce/West]: 결정학적 비등가 4곳 — Li_A = 4c(1)/4c(2)(c축 교대), Li_B = 4a/4b(c축 교대). 일부 Li는 남은 사면체 자리, **나머지는 팔면체 자리** — **팔면체 부분점유가 전도의 열쇠**라는 가설(ref 22)이 이 논문 Tc·p_Oct 설계의 출발점.
- 고전도 LISICON은 대부분 γ상 → 스크리닝은 **γ 골격 고정** 전제(§5.3의 한계이기도).

## 3.5 계산 방법 절에서 확인할 것

방법 절은 재현을 위한 정보지만, 처음 읽을 때는 **딱 네 가지만** 확인하면 된다.
1. **범함수** (PBE/r2SCAN 등) — 어떤 근사로 에너지를 구했나. 계열이 다르면 절대값 비교 불가.
2. **컷오프·k점** — 수치 수렴 조건. 이게 얕으면 뒤 숫자가 다 흔들린다.
3. **셀 크기·원자 수** — MD 는 셀이 작으면 이온이 자기 이미지와 상호작용한다.
4. **시간 규모** (MD 인 경우) — 몇 ps 돌았나. 짧으면 확산 영역에 못 들어간다(우리 게이트의 그 문제).
⚠ 이 넷이 다르면 **다른 논문의 절대값과 나란히 놓을 수 없다.** 경향만 비교한다.

---

## 4. DFT/계산 방법 ★
- **code**: VASP [27] · **PAW** [24,25] · **GGA(PBE)** [26]. vdW 없음, DFT+U 없음.
- **ecut 300 eV** · 총에너지 수렴 < 10⁻² meV/cell · **k = Γ-point only** (2013 HT 규모 타협 — ⚠ 우리 기준으론 soft).
- **FPMD(AIMD)**: **NVT, Nosé thermostat** [28] · **셀 = γ 단위셀 2×1×2 = 16 f.u.** (원자수 **128–144**: Li₂ZnGeO₄ 8 atom/f.u.×16 = 128 ↔ Li₄GeO₄ 9 atom/f.u.×16 = 144 — ✎2026-08-03 교정, 이전 "~112±"는 오산) · **dt = 2 fs** · 격자부피 = "무작위 분포 Li"의 **0 K DFT 부피 고정**(NpT 아님 — 열팽창 무시) · 시뮬레이션 시간·잔여 상세 SI(미보유, n/a).
- **온도**: Zn-Ge 계 3조성(x=0.25/0.5/0.75)은 **고온 4점**(Fig 2 축 판독 **≈1200–2000 K** 창 = 1000/T ≈ 0.50/0.60/0.70/0.83; 정확 목록 SI n/a — ✎2026-08-03 하한 1250→1200 정밀화. 1600 K는 1000/T=0.625로 이 창 안) → Arrhenius; 92조성 전수 스크리닝은 **1600 K 단일점**(D₁₆₀₀).
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
- **Tc** (γ상, 4조성): **Li₂.₅Zn₀.₇₅GeO₄ 1150 K / Li₃Zn₀.₅GeO₄ 750 K / Li₃.₅Zn₀.₂₅GeO₄ 380 K** (본문 수치) + x=1(Li₄GeO₄) **≈340 K**(figure-read, 본문 수치 없음 — 본문이 "four compositions"라 해놓고 세 개만 적은 그 네 번째) → **Zn 감소 = Tc 급감** = 저온까지 무질서(전도 유리) 유지.
- **E^mix₀**(질서 바닥, γ 양끝단 기준): 전 조성 ~0(약음, figure-read −0.1~0 eV/unit cell) — γ끼리는 거의 이상용액.
- **F^mix₁₂₀₀**(무질서 γ, 1200 K, 팔면체 Li 배열 엔트로피만): 최대 ≈−0.65 eV/unit cell(x=1 쪽, figure-read). γ-Li₂ZnGeO₄는 Li가 사면체만 점유 → 배열 엔트로피 0.
- **실험 기지상 대비**: β-Li₂ZnGeO₄ ≈−0.2, α-Li₄GeO₄ ≈**−0.8 eV/unit cell**(figure-read) → **저온 바닥은 β+α 상분리**(상도 Fig 1a와 정합); γ는 고온서 엔트로피로 안정화. α(**−0.80**) vs 무질서 γ 1200 K(**−0.67**) 차 **≈0.13 eV/unit cell**(✎2026-08-03 정밀화, 이전 −0.65/0.15) — 뒤의 "γ-Li₄GeO₄ 합성 희망" 논거.

### 5.2 Arrhenius 검증과 저온 외삽의 실패 지점 (Fig 2)
- FPMD D(고온 4점, x=0.25 청/0.5 적/0.75 흑) vs 실험 σ→NE 환산 D(open circle [2 Hong], open triangle [29 Takai 2004]).
- **x=0.75(원조 LISICON)**: 고온 FPMD 외삽선이 **실험 523–673 K 구간과 잘 맞음** → 이 구간까지는 **동일 전도 메커니즘**(상변화 없음).
- **<523 K**: 실험 Ea 증가(굴절) — 논문 해석 = **팔면체 Li 질서화**(기존엔 막연히 "상전이" [5]; x=0.5는 굴절점 550 K 보고 [6] 기반으로 Fig 2 저온 연장선을 x=0.25와 0.75의 중간 기울기로 그림). **→ 단순 고온 외삽은 저온서 부정확** = ML 도입의 물리적 근거.
- 계산 Tc(380 K, x=0.75)는 실험 굴절(~523 K)보다 낮음 — 점근사 한계(방향은 재현, 절대값 과소).

### 5.3 92조성 HT 스크리닝 (Fig 3) — 이 논문의 물리 하이라이트
- 3계열: **II-IV**(A=Zn,Mg) / **III-IV**(A=Al,Ga) / **V-IV**(A=P,As), B=Ge,Si. 각 계열 **tie line 1**(Li₈₋c A_a BO₄–Li₄BO₄: A가 Li₄BO₄의 Li 치환), **tie line 2**(Li₄BO₄–Li₈₋c AO₄: A가 B 치환). **V-IV는 tie line 2만**(5가 이온의 Li-자리 치환은 에너지적으로 금지적).
- 산출 4종: **D₁₆₀₀**(FPMD) · **Tc** · **ΔF^S₁₆₀₀**(1600 K 고용체 형성자유에너지; 기준 = 끝단 x=0·y=1·x=1=y=0 최저에너지 상 — Fig 1d와 기준 다름 주의) · **V_dis**(무질서 구조 평균 부피). D₁₆₀₀ 범위 **≈0.1–8.4 ×10⁻⁹ m²/s**(600 dpi 크롭 판독 — ✎2026-08-03 교정, 이전 "(1–8)"은 하한이 한 자릿수 틀림). **하한이 ~0인 것이 핵심 증거**: TL1의 x=0(Li₂ABO₄ = p_Oct 0)에서 D₁₆₀₀ ≈0.1–0.5로 사실상 정지, V-IV TL2의 y=1(p_Oct 0)에서도 ≈0.4–1.3. V_dis는 같은 구간에서 330→415 Å³/unit cell로 25 % 변하는데 D는 무상관.
- **🔑 부정 결과 1**: **D₁₆₀₀는 A·B 원소 선택에 둔감**. **🔑 부정 결과 2**: **D₁₆₀₀는 V_dis(격자부피)와 거의 무관** — "부피 크면 확산 빠르다"는 통념을 92조성 규모로 반증.
- **🔑 양성 결과**: 평균 팔면체 Li 점유율 **p_Oct = [(8−c+a+b)−4]/4** 가 확산 크기의 **1차 인자**(tie line 1 전부 + A=5가의 tie line 2). 단 **A=2가/3가의 tie line 2에선 p_Oct 단독으로 설명 안 됨**(예외 명시 — 정직).
- **🔑🔑 신규(2026-08-03 그림 판독, 논문 미서술)**: 예외의 정체는 **포화**다. p_Oct가 **0을 지나는 구간에서만** 상관이 강하고(II-IV TL1 p_Oct 0→0.25 ⇒ D 0.3→6; III-IV TL1 0→0.25 ⇒ 1.2→6; V-IV TL2 0.25→**0** ⇒ 6→0.8, 유일한 감소 구간), **이미 p_Oct ≥0.25인 채 더 올라가는 구간에선 무상관**(II-IV TL2 p_Oct 0.25→**0.75**(3배) ⇒ D 6→7.5 거의 평탄; III-IV TL2 0.25→0.50 ⇒ 6→6.5). 즉 **p_Oct는 단조 구동인자가 아니라 운반자 "점화(onset)" 기술자**이고, D₁₆₀₀는 p_Oct ≳0.25에서 **6–8×10⁻⁹ m²/s로 포화**한다. → 우리 cascade 서술자 해석에 직결(§11-④).
- ΔF^S₁₆₀₀: tie line 1은 대체로 ≤0(고용 가능), II-IV tie line 2는 큰 양수(inset ~+1–3 eV/unit cell, Li₆AO₄ 쪽 비혼화) — 합성 가능성 필터로 뒤에서 사용.

### 5.4 ML: SVR로 이론+실험 연결 (본문 984)
- 전제(명문): "**Assuming that the theoretical data are complementary to and consistent with the experimental data**" — 이론-실험 정합성은 *가정*.
- **훈련 데이터**: 실험 전도도 **95 측정점**(여러 조성×여러 온도; 분포는 SI Fig S1 — 미보유라 조성별 커버리지 n/a) = **라벨** / 이론 기술자 D₁₆₀₀·Tc·V_dis = **특징**.
- **모델**: **support-vector regression + Gaussian kernel** [35 = LIBSVM Chang & Lin 2011]. 종속변수 **log σ**; 독립변수 **D₁₆₀₀, Tc, V_dis, (실험)온도 T** — 4특징. 변수 유의도는 SI(n/a).
- **HPO**: 커널 분산·정규화 상수·**독립변수의 함수형**(변환 형태)을 **bootstrap** [36 Efron & Tibshirani]으로 예측오차 최소화. 오차 곡선 SI Fig S2(n/a).
- **성능**: 최적 SVR의 **log σ 예측오차 0.373** ≈ σ로 **×2.36 배** 수준. hold-out/외부검증 없음(부트스트랩 내부 추정).
- Fig 4 캡션의 "**iterative analysis** of calculated and experimental datasets" — 반복 절차의 정체는 본문 미상술(불투명성, §10).

### 5.5 σ₃₇₃ 예측 지도와 최적 조성 (Fig 4)
- **72조성**(Tc·V_dis 가용분)의 373 K 예측 σ 막대지도. 범위 **≈7×10⁻⁶ – 4.7×10⁻⁴ S/cm**(650 dpi 크롭 판독 — ✎2026-08-03 교정: 이전 "10⁻⁶–5×10⁻⁴"의 하한 10⁻⁶은 **축 바닥일 뿐 실제 막대는 거기 닿지 않는다**. 최저 막대 = II-IV TL1 x=0.25의 Mg,Ge ≈7×10⁻⁶). **전체 폭 = 1.83 decade뿐**.
- **✅ 막대 수 실물 재계수 = 정확히 72**: II-IV TL1 4군×4 + II-IV TL2 4군×4 + III-IV TL1 **2군**×4 + III-IV TL2 4군×4 + V-IV TL2 4군×4 = 16+16+8+16+16 = **72** ✓ 본문 주장과 일치.
- **🔑 신규(2026-08-03): 72 막대에 끝단 중복이 섞여 있다.** 끝단에서 A(또는 B)가 소거되므로 서로 다른 계열의 막대가 **같은 화합물**이 된다 — 실제로 막대 높이가 정확히 일치하는 것으로 확인: **Li₄GeO₄ 6번**(II-IV TL1 x=1의 Zn,Ge·Mg,Ge / III-IV TL1 x=1의 Al,Ge·Ga,Ge / V-IV TL2 y=0의 P,Ge·As,Ge — 6개 모두 ≈4.7×10⁻⁴), **Li₄SiO₄ 6번**(모두 ≈3.0×10⁻⁴), Li₆ZnO₄·Li₆MgO₄·Li₅AlO₄·Li₅GaO₄ 각 2번. 끝단 막대 20개 중 서로 다른 화합물은 6개 → **화학적으로 구별되는 조성은 72가 아니라 58종**(큐레이터 셈: 72−20+6). 인용할 때 "72 compositions"는 논문 표현 그대로 쓰되, **독립 조성 수로 오독하지 말 것**. (부수 효과: 같은 화합물이 6번 같은 값으로 나온 것 = SVR 파이프라인의 내부 정합성 확인.)
- **학습된 물리**: 특징에 Ea가 없는데도 **고 D₁₆₀₀ + 저 Tc → 고 σ₃₇₃** 경향 재현. 저-Zn Li₂₊₂ₓZn₁₋ₓGeO₄(x=0.75, 고D·저Tc) > 고-Zn(x=0.25, 고Tc) → **원조 LISICON Li₃.₅Zn₀.₂₅GeO₄가 왜 역대 최고급인지 설명** = 회귀가 실험 트렌드를 내재화했다는 sanity check.
- **1위: γ-Li₄GeO₄** — 전 72조성 중 최고 σ₃₇₃ **≈4.7×10⁻⁴ S/cm**, **원조 LISICON의 "a few times higher"**(본문). ✅ **실물 검산**: 원조 LISICON Li₃.₅Zn₀.₂₅GeO₄ = II-IV TL1 x=0.75의 Zn,Ge 막대 **≈1.15×10⁻⁴** → 비 **≈3.9배** = 본문 "a few times higher"와 정합. ⚠ 단 실제론 α상으로 결정화(γ 미합성); Fig 1d상 α↔γ의 F^mix₁₂₀₀ 차가 크지 않아(α −0.80 vs 무질서 γ −0.67, Δ≈0.13 eV/unit cell) "합성 가능할지도"가 논거.
- **⚠🔑 신규(2026-08-03): 1·2위 격차가 모델 자체 오차보다 작다.** SVR 예측오차 0.373 decade인데 **Li₄GeO₄(4.7×10⁻⁴) vs Li₄SiO₄(3.0×10⁻⁴) 차이는 0.19 decade** — 자기 오차의 절반. 즉 **"Li₄GeO₄가 72조성 중 1위"라는 순위 자체는 논문의 자기 오차로 분해되지 않는다**(Li₄SiO₄와 통계적 동률). 반면 vs 원조 LISICON은 **0.61 decade**로 오차 밖(≈1.6×오차) → **"원조보다 몇 배 높다"는 방어 가능, "Ge가 Si보다 낫다"는 방어 불가**. 더 일반적으로 전체 예측 폭 1.83 decade ÷ 오차 0.373 decade ≈ **4.9** — 이 지도가 실제로 분해하는 것은 5단계 정도의 조야한 등급뿐이고, 이웃 조성 간 랭킹은 대부분 노이즈 안이다. 우리가 이 그림을 인용할 땐 **개별 순위가 아니라 "고/중/저 등급"으로만** 쓸 것.
- **차상위 후보군**(σ₃₇₃ > 원조 LISICON & **ΔF^S₁₆₀₀ < 0**, 본문 명시 리스트): **Li₄SiO₄**, **Li₂₊₂ₓZn₁₋ₓSiO₄(x=0.5, 0.75)**(=Li₃Zn₀.₅SiO₄, Li₃.₅Zn₀.₂₅SiO₄), **Li₃.₅Mg₀.₂₅SiO₄**, **Li₃.₂₅Al₀.₂₅SiO₄**, **Li₄.₂₅A₀.₂₅Si₀.₇₅O₄(A=Al,Ga)**, **Li₃.₅P₀.₅Si₀.₅O₄**, **Li₃.₇₅A₀.₂₅B₀.₇₅O₄(A=P,As; B=Ge,Si)** — **7개 화학식군 = 서로 다른 12조성**(+1위 Li₄GeO₄ = 13). ✎2026-08-03: §6 스펙카드의 "8종"은 오기.
- **✅✅ 신규 검증(2026-08-03) — 후보 리스트가 Fig 3+4의 이중기준과 전수 일치한다.** 본문은 기준만 말하고 검산을 안 보여주는데, Fig 4(σ₃₇₃)와 Fig 3(ΔF^S₁₆₀₀)를 직접 교차 판독하니 **탈락 사례까지 정확히 설명된다**:
  - Li₄.₂₅A₀.₂₅**Si**₀.₇₅O₄(A=Al,Ga)는 리스트에 있는데 **Ge 유사체(Al,Ge·Ga,Ge)는 없다** — Ge 쪽도 σ₃₇₃ ≈2.3–3.7×10⁻⁴로 원조 LISICON보다 높지만 **ΔF^S₁₆₀₀ ≈+0.17~+0.20 (양수)** 라서 탈락 ✓ (Si 쪽은 ≈−0.10, 음수 ✓).
  - V-IV TL2 y=0.50에서 **P,Ge(σ ≈1.75×10⁻⁴ > LISICON)는 탈락, P,Si(σ ≈1.8×10⁻⁴)만 채택** — ΔF^S가 P,Ge ≈+0.22 vs P,Si ≈−0.02 ✓.
  - III-IV TL1 x=0.50에서 **Al,Ge는 ΔF^S ≈−0.17로 음수인데도 탈락** — σ₃₇₃ ≈3×10⁻⁵로 LISICON 미달 ✓ (Al,Si는 σ ≈1.5×10⁻⁴로 통과 ✓).
  - Li₃.₇₅A₀.₂₅B₀.₇₅O₄는 A=P,As × B=Ge,Si **네 조합 전부** ΔF^S ≈−0.03~−0.30 (음수) & σ₃₇₃ ≈3.7–4.2×10⁻⁴ (전부 LISICON 초과) ✓ — 그래서 리스트가 4조합을 통째로 담았다.
  - ⚠ 단 **Li₃.₅P₀.₅Si₀.₅O₄의 ΔF^S ≈−0.02는 사실상 0** — 이 항목만 경계 사례라 "고용 가능"으로 단정하면 안 된다.
  - 📌 부수 관찰: 후보 13조성 중 **11개가 Si계**(Ge계는 Li₄GeO₄와 Li₃.₇₅A₀.₂₅Ge₀.₇₅O₄ 2종뿐). 리스트의 실질적 메시지는 "Ge를 Si로 바꿔라"에 가깝고, 이는 합성성(ΔF^S) 게이트가 만든 결과지 D₁₆₀₀가 만든 결과가 아니다(D₁₆₀₀는 A·B에 둔감).
- **검증**: "Focused experiments … currently being performed" — **논문 내 실험 검증 없음**(2013 시점 진행 중 선언만). ⚠ 큐레이터 주(논문 밖 지식, 수치 인용 금지): 후보 중 P–Si 계열(Li₄SiO₄–Li₃PO₄ 고용체, 예: Li₃.₅P₀.₅Si₀.₅O₄)은 원래부터 알려진 LISICON 고전도 조성족과 겹침 — "재발견" 성격도 있음.
- 결론부: 방법은 의사이원계에 국한 안 됨 — "systematic first-principles DB만 있으면 더 복잡한 화학에도" = HT-DB+ML 시대 선언(2013).

## 5.5 회귀 스펙 카드를 읽는 법

- **커널(kernel)** — "두 조성이 얼마나 비슷한가"를 정하는 함수. RBF(가우시안)가 기본값이다.
- **하이퍼파라미터 (C, γ, ε)** — 모델이 데이터를 얼마나 세게 따라갈지 조절하는 손잡이.
  C 가 크면 학습 데이터에 딱 맞추고(과적합 위험), 작으면 뭉갠다.
- **이 손잡이를 무엇으로 정했나가 핵심이다.** 시험셋 성능으로 정하면 그 성능은 부풀려진 값이다
  (시험셋을 학습에 쓴 셈). 제대로 하려면 학습셋 안에서 다시 쪼개 정해야 한다.
스펙 카드를 볼 때 **"하이퍼파라미터를 어디서 정했나"** 한 줄을 찾는 습관이 중요하다.

---

## 6. ★ ML 모델 스펙 카드 (요청 최우선 항목 — 한 표로)
| 항목 | 내용 |
|---|---|
| 기법 | **SVR(support-vector regression) + Gaussian kernel** (LIBSVM [35]) |
| 타깃(라벨) | **log σ** — *실험* 전도도 (여러 온도) |
| 특징(입력) 4개 | **D₁₆₀₀**(FPMD 1600 K 확산계수) · **Tc**(질서-무질서 전이온도, DFT+점근사 엔트로피) · **V_dis**(무질서 평균 부피) · **T**(측정 온도) — *이론 3 + 조건 1* |
| 훈련 표본 | **실험 95 측정점**(조성×온도; 조성 수 본문 미명시, SI Fig S1 n/a) |
| 이론 데이터 규모 | FPMD 92조성(1600 K) · Tc/ΔF^S/V_dis 72조성 · 정적 2684회 |
| HPO/검증 | 커널 분산·정규화·**특징 함수형**을 **bootstrap 오차 최소화**로 — hold-out/외부 검증 없음 |
| 성능 | **"prediction error … for log σ is 0.373"**(본문 표현 그대로) ≈ σ로 **×2.36 배**. ⚠ 논문은 **RMSE라고도, log₁₀이라고도 명시하지 않음** — 둘 다 우리 추정(σ 값 범위로 보아 상용로그가 자연스러움). ✎2026-08-03: 이전 "RMSE(log₁₀ σ)" 단정 표기를 완화 |
| 예측 산출 | **σ₃₇₃ 지도, 72 막대**(Fig 4) — 대상족 = γ-LISICON 산화물 **단일 구조족 내 보간**. ⚠ 끝단 중복 포함이라 **화학적 독립 조성은 58종**(§5.5 실물 재계수) |
| 최적 조성 | **γ-Li₄GeO₄**(1위 ≈4.7×10⁻⁴ S/cm, 미합성 γ상) + 차상위 **7화학식군 = 12조성**(§5.5; ✎2026-08-03 교정, 이전 "8종"은 오기). 단 1위–2위 격차 0.19 decade < 자기 오차 0.373 → **순위 비분해** |
| 검증 여부 | 논문 내 없음("focused experiments in progress"만) |

## 7. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1a | Li₂ZnGeO₄–Li₄GeO₄ 상도(ref 21 재게재): β/γ/α(α')·liquid | 고용체 스크리닝 전에 상도로 "γ 영역" 고정하는 프레임 |
| 1b | γ-LISICON 구조(c축 투영): [GeO₄]/[ZnO₄]/[LiO₄] 사면체 + 팔면체 Li(파선 원), Li_A(4c)·Li_B(4a/4b) | "전도 부격자(팔면체) vs 골격" 분리 그림 — 우리 cage/48h 그림 문법의 산화물판 |
| 1c | 계산 Tc vs 조성(1150/750/380 K + x=1 ≈350) | **무질서 지속온도를 조성의 함수로** — 우리 disorder ensemble의 "조성→무질서 경향" 정량화 아이디어 |
| 1d | E^mix₀(질서)·F^mix₁₂₀₀(무질서)·실험상(β, α) 상대에너지 | 준안정 γ 고용체 vs 진짜 바닥(상분리) 구분 — E_above_hull 사고의 2013판 |
| 2 | Arrhenius: FPMD 4점(고온) vs 실험 NE-환산 D; 523–673 K 일치, <523 K 굴절 | **"고온 MD 외삽은 질서화 온도 아래서 무효"** — 우리 600–1000 K 3점 규율·400/500 K 제외와 같은 물리 |
| 3 | 92조성: **V_dis(330–415 Å³/uc) / ΔF^S₁₆₀₀(−0.5~+0.65, II-IV TL2만 inset 1.15–2.75) / Tc(~250–1750 K) / D₁₆₀₀(0.1–8.4×10⁻⁹ m²/s) / p_Oct** 5단 패널 × 5열(II-IV TL1·TL2, III-IV TL1·TL2, V-IV TL2) | HT 스크리닝 결과를 "기술자 대시보드"로 쌓는 시각화 — cascade 축별 패널과 동형. **off-scale 구간을 inset으로 빼는 처리**도 우리 cascade 그림에 쓸 만함 |
| 4 | 예측 σ₃₇₃ 막대지도(**72 막대 = 58 독립조성**, 7×10⁻⁶–4.7×10⁻⁴ S/cm) | ML 산출을 "조성 지도"로 제시 — TabPFN 산출물 포맷 참고. ⚠ **반면교사**: 예측폭(1.83 dec)을 모델 오차(0.373 dec)와 함께 그리지 않아 순위가 과해석됨 — 우리 지도엔 **오차막대/등급 밴드를 반드시 동봉** |
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
- **⚠🔑 신호 대 잡음이 낮다(2026-08-03 실물 판독)**: Fig 4의 예측 σ₃₇₃ 전체 폭이 **1.83 decade**(7×10⁻⁶–4.7×10⁻⁴)뿐인데 모델 자기 오차가 **0.373 decade** — 비 ≈4.9. 이 지도가 실제로 분해하는 건 **대여섯 등급**이고 이웃 조성 간 순위는 대부분 오차 안이다. 특히 **1위 Li₄GeO₄ vs 2위 Li₄SiO₄ = 0.19 decade로 자기 오차의 절반** → **"Li₄GeO₄가 최고"는 논문 자신의 오차로 분해 불가**(Li₄SiO₄와 동률로 읽어야 함). 원조 LISICON 대비 0.61 decade는 오차 밖이라 "a few times higher"만 살아남는다. 인용 시 **개별 랭킹 금지, 등급으로만**.
- **⚠ "72 compositions"의 실질은 58조성**(2026-08-03 재계수): 끝단에서 A/B가 소거돼 **Li₄GeO₄가 6번, Li₄SiO₄가 6번** 같은 값으로 중복 등장(막대 높이 일치로 확인). 논문 표현을 그대로 옮기되 독립 조성 수로 오독 금지 — 스크리닝 규모를 인용할 땐 **FPMD 92 / 예측 72막대(58조성)** 로 분리해 쓸 것.
- **p_Oct는 "점화" 기술자지 구동인자가 아니다**(§5.3 신규): p_Oct ≳0.25에서 D₁₆₀₀가 6–8×10⁻⁹으로 포화하므로, 논문이 예외로 남긴 II-IV/III-IV tie line 2는 "예외"가 아니라 **포화 영역**이다. "p_Oct 높이면 빨라진다"로 인용하면 틀린다 — **"p_Oct=0이면 죽는다"** 가 실제 내용.
- **기술자 자체의 방법 의존**: D₁₆₀₀는 Γ-only·300 eV·단일 배열·0 K 고정부피 FPMD; Tc는 점근사 엔트로피(진동·단거리질서 무시, 절대값 과소 — 380 vs 굴절 ~523 K). 특징의 계통오차가 조성별로 다르면 SVR이 조용히 흡수(감지 불가).
- **p_Oct 만능 아님**: 2·3가 tie line 2 예외를 저자도 명시 — 단일 기술자 랭킹 인용 금지.
- **γ 골격 고정 스크리닝**: 조성별 실제 바닥상(β/α/상분리)은 ΔF^S·Fig 1d로 부분 점검하지만, FPMD·예측은 전부 γ 가정 — 합성 가능성은 별도 문제.
- **1600 K 단일점 D**: Ea 정보 없음(모델이 Tc로 간접 보완) — D₁₆₀₀ 높아도 저온 급락 가능성은 Tc가 다 못 잡음.
- 시대적 소프트 셋업(Γ, 300 eV, 짧은 MD)은 **비난이 아니라 맥락** — 2013 HT-AIMD 천장. 절대값 재사용 금지, 설계·계보만 인용.

## 11. 적용 인사이트 (내 연구에 어떻게)
1. **ML 세대 계보 한 줄(deck용)**: "σ-예측 ML 3세대 — **Fujimura 2013**(가우시안-커널 SVR·특징 4개(D₁₆₀₀/Tc/V_dis/T)·실험 라벨 95점·γ-LISICON *조성족 내* 보간·log σ 오차 0.37) → **Sendek 2017**(로지스틱 분류, *물질군 횡단* 스크리닝 — `[Sendek17]` digest) → **우리 2026**(TabPFN ICL — 사전학습 prior 소표본 표형 회귀, 47-dopant cascade/DEM 코퍼스)". 1세대의 본질 = *물리 기술자를 사람이 설계*(D₁₆₀₀·Tc)하고 ML은 다리만.
2. **"고온 MD + 저온 다리" 구조는 2013이나 지금이나 동일** — 그들: FPMD 1600 K→SVR→373 K; 우리: UMA 600–1000 K→비율/Arrhenius(→장차 TabPFN 잔차). 우리 deck에서 "왜 RT σ를 직접 안 재나"의 역사적 정당화로 인용.
3. **layer-혼합 교훈(우리 규율과의 긴장 해소)**: Fujimura 혼합은 **특징=이론 / 라벨=실험으로 층이 분리된 '학습된 다리'** — 우리 "문헌값·우리값 혼합 금지"는 *같은 층에 두 출처를 섞지 말라*는 뜻이고, Fujimura형 다리는 허용 가능한 예외 형식. 단 그들이 안 한 것(라벨 출처 가중·조성족 leave-out·특징 계통오차 명시)을 우리가 TabPFN에서 반드시 추가할 것.
4. **p_Oct 선례 — 단, "onset"으로 인용할 것**(2026-08-03 그림 판독 반영): "전도 부격자 점유율이 1차, 전역 부피는 허수"는 맞지만 실물은 **p_Oct=0 → D≈0 / p_Oct ≳0.25 → 6–8×10⁻⁹로 포화**인 계단형이다. 우리 cascade 서술자 우선순위(공공/blocking > 격자상수)와 [Perc]·[Adeli] 서사의 1세대 인용처로 쓰되, **"운반자를 더 넣으면 더 빨라진다"가 아니라 "운반자가 없으면 죽는다"** 로 서술 — 우리 [Perc] "carrier > pc" 논지와 이 형태가 더 정확히 맞물린다.
7. **오차와 함께 그려라(반면교사)**: 이 논문은 예측 σ 지도를 오차막대 없이 막대그래프로 냈고, 그 결과 **자기 오차(0.373 dec)보다 작은 1위–2위 격차(0.19 dec)** 가 12년간 "γ-Li₄GeO₄ 최적"으로 인용됐다. 우리 TabPFN/cascade 산출물은 **예측폭 대비 모델 오차를 같은 축에 표시**하고, 순위 대신 **등급 밴드**로 보고할 것.
5. **Tc라는 관측가능한 무질서 지표**: 우리 disorder ensemble에 "질서화 온도" 축을 붙이면(배열 에너지차 + 점근사 S로 즉석 Tc 추정) 문헌과 대화 가능한 숫자가 하나 생김 — 단 점근사 과소 경고 동봉.
6. **부정 결과 공개 관행**: "V_dis 무관·p_Oct 예외 있음"을 본문에 명시한 것이 이 논문의 수명(12년 인용)을 늘림 — 우리 cascade 보고서도 실패 서술자를 지우지 말 것.

## 12. 인용 가능 문장 (deck/paper용)
- "The theory-as-features / experiment-as-labels bridge for ionic conductivity dates back to Fujimura et al. (2013): high-T FPMD diffusivity, order-disorder Tc and cell volume of 72 LISICON compositions fed into a Gaussian-kernel SVR trained on 95 experimental conductivities (log-σ error 0.373) to map σ at 373 K."
- "Already in 2013, high-throughput FPMD screening showed that global cell volume is a poor predictor of Li diffusivity — occupancy of the conducting (octahedral) sublattice, p_Oct, was the principal factor."
- "Fujimura et al.'s Tc analysis formalized why high-temperature MD must not be extrapolated below the Li ordering transition — the same physics behind our 600–1000 K-only Arrhenius discipline."
- "Generation 1 (Fujimura 2013, kernel regression within one structure family) → generation 2 (Sendek 2017, logistic screening across families) → generation 3 (tabular foundation models, in-context learning on small curated corpora)."
- *(우리 재판독에 근거한 문장 — 논문 자신은 이렇게 쓰지 않았으므로 "our reading of their Figure 3/4"로 귀속해 인용)*: "Re-reading Fujimura et al.'s screening data, octahedral occupancy acts as an **onset** descriptor rather than a monotonic driver: D₁₆₀₀ collapses to ~0 when p_Oct → 0 but saturates at 6–8 × 10⁻⁹ m² s⁻¹ once p_Oct ≳ 0.25 — which is precisely why their p_Oct correlation holds along the tie lines that cross p_Oct = 0 and fails along those that do not."
- *(동)*: "The predicted σ₃₇₃ map spans only 1.8 decades while the model's own log-σ error is 0.373 — so its composition ranking resolves broad tiers, not individual compounds; the reported first-place margin over the runner-up (0.19 decades) lies inside that error."

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

---

## 14. 본문 실물 독립 검증 (2026-08-03)

**방법**: `litdb/inbox/42. …pdf`(6 pp) 전문을 `pdftotext -layout`으로 추출해 §1–13 전 주장과 1:1 대조 + **PyMuPDF로 Fig 1/2/3/4를 200 dpi 전면·600–700 dpi 크롭 4매**(Fig 3 D₁₆₀₀+p_Oct 행, Fig 3 ΔF^S 행+inset, Fig 4 σ 지도)로 재판독. digest 초판(2026-07-28)은 **첫 페이지만 실물 대조**된 상태였음. **SI는 여전히 미보유** — Fig S1(실험 σ 95점 산포)·S2(bootstrap 오차 vs 변수)·FPMD 시간규모·SA 상세·변수 유의도는 이번에도 확인 불가.

### 14.1 교정 6건
| # | 위치 | 초판 | 실물 | 성격 |
|---|---|---|---|---|
| 1 | §5.5 | σ₃₇₃ 범위 **10⁻⁶**–5×10⁻⁴ | **7×10⁻⁶**–4.7×10⁻⁴ (최저 막대 = II-IV TL1 x=0.25 Mg,Ge) | **하한 오독** — 10⁻⁶은 축 바닥일 뿐 막대가 안 닿음. 전체 폭이 1.8 decade밖에 안 된다는 §10 비판의 근거 |
| 2 | §5.3 | D₁₆₀₀ **(1–8)**×10⁻⁹ m²/s | **0.1–8.4**×10⁻⁹ | **하한이 한 자릿수 틀림**. p_Oct=0에서 D≈0인 것이 p_Oct 논지의 핵심 증거인데 초판이 이를 가림 |
| 3 | §4 | 셀 원자수 **~112±** | **128–144** (16 f.u.×8–9 atom/f.u.) | 오산 (Li₂ZnGeO₄ 128 ↔ Li₄GeO₄ 144) |
| 4 | §6 | 차상위 후보 **8종** | **7 화학식군 = 12조성** (+Li₄GeO₄ = 13) | 계수 오기 |
| 5 | §6 | **RMSE(log₁₀ σ)** = 0.373 | 본문은 "prediction error … for log σ is 0.373"뿐 | **과잉 특정** — RMSE도 상용로그도 논문 미명시 |
| 6 | §4·§5.1 | FPMD 창 ≈1250–2000 K / F^mix 차 0.15 | **≈1200–2000 K**(1000/T 0.50–0.83) / **0.13** eV/uc | 정밀화 |

### 14.2 신규 적발 5건 (논문 미서술 또는 초판 누락)
1. **Fig 4의 72 막대에 끝단 중복** — Li₄GeO₄ 6회·Li₄SiO₄ 6회·Li₆ZnO₄/Li₆MgO₄/Li₅AlO₄/Li₅GaO₄ 각 2회. **독립 조성 58종**. 막대 높이가 정확히 일치하는 것으로 확인(= SVR 파이프라인 내부 정합성도 동시에 확인됨). → §5.5·§10
2. **1위 랭킹이 자기 오차로 분해 안 됨** — Li₄GeO₄ vs Li₄SiO₄ 0.19 decade < 오차 0.373. vs 원조 LISICON은 0.61 decade로 유효. → §5.5·§10
3. **p_Oct 포화** — p_Oct ≳0.25에서 D₁₆₀₀ 6–8×10⁻⁹ 포화. 논문이 "예외"라 부른 II-IV/III-IV tie line 2는 예외가 아니라 포화 영역. p_Oct는 **onset 기술자**. → §5.3·§10·§11
4. **92→72 탈락 경로 규명** — tie line 1의 x=0(Li₂ABO₄·Li₂.₅A₀.₅BO₄)은 **p_Oct=0 ⇒ 팔면체 Li 배열 엔트로피 0 ⇒ Tc 정의 불가**라 SVR 입력에서 빠진다. Fig 4에서 해당 x=0 그룹이 통째로 없는 것이 근거(II-IV TL1은 x=0.25부터, III-IV TL1은 x=0.50·1.00만).
5. **Fig 1a의 α′ 고온상** 표기 — 초판 §3의 "3다형"은 α/β/γ를 뜻하고 α′는 α의 고온 변태.

### 14.3 확인만 되고 변경 없음 (주요 항목)
- 서지·저자·소속·투고일(2013-01-16 / online 2013-04-19)·MEXT Grant-in-Aid·공동1저자 [†] ✓
- 계산 셋업 전부: VASP[27]·PAW[24,25]·GGA(PBE)[26]·**300 eV**·수렴 <10⁻² meV/cell·**Γ-only**·NVT Nosé[28]·**2×1×2 = 16 f.u.**·**dt 2 fs**·0 K 무작위-Li 부피 고정 ✓
- **Tc = 1150 / 750 / 380 K**(x=0.25/0.5/0.75) ✓ · 무질서 = **무작위 20 초셀 평균** ✓ · 점근사 엔트로피 식 ✓ · Tc 정의(ΔE = TcΔS) ✓
- 규모 **FPMD 92조성 / Tc·ΔF^S·V_dis 72조성 / 정적 2684회** ✓ · **Fig 4 막대 실물 재계수 = 16+16+8+16+16 = 72** ✓
- SVR+가우시안 커널[35]·타깃 log σ·특징 4개(D₁₆₀₀·Tc·V_dis·T)·실험 95점·bootstrap[36] HPO·오차 0.373 ✓
- p_Oct 식과 **예외 서술**(A=2가/3가의 tie line 2) ✓ · V_dis 무관 주장 ✓
- Fig 1d figure-read: E^mix₀ ≈−0.1~0 ✓ / F^mix₁₂₀₀(x=1) ≈−0.67 / β-Li₂ZnGeO₄ ≈−0.23 / α-Li₄GeO₄ ≈−0.80 ✓
- Fig 2 캡션 세부(청/적/흑 = x=0.25/0.5/0.75, open circle[2]·triangle[29], x=0.5 저온 연장선은 굴절점 550 K[6] 기반) ✓
- ΔF^S₁₆₀₀ inset(II-IV tie line 2) 범위 ≈**1.15–2.75** eV/unit cell ✓ (초판 "~1–3" 유지)
- **차상위 후보 리스트 전수 교차검증 통과** — σ₃₇₃>LISICON **AND** ΔF^S₁₆₀₀<0 이중기준이 채택·탈락 양쪽을 정확히 설명(Ge 유사체 탈락·Al,Ge 탈락·P,Ge 탈락 3사례 확인). 유일한 경계 사례는 **Li₃.₅P₀.₅Si₀.₅O₄ (ΔF^S ≈−0.02 ≈ 0)**. → §5.5

### 14.4 미결 (SI 확보 시에만 종결 가능)
- FPMD **시뮬레이션 시간 길이**·MSD 창·D 통계오차 — 전부 SI. **D₁₆₀₀ 절대값의 신뢰구간을 모른 채** 그 값이 SVR 특징으로 들어갔다는 점이 이 논문 최대의 미확인 리스크.
- FPMD 4점의 **정확한 온도 목록**(축 판독 ≈1200/1670/1430/2000 K 추정).
- SA(점전하) 상세 · **변수 유의도**(어느 특징이 실제로 일했는지) · Fig S2 bootstrap 오차 곡선 · Fig S1 실험 95점의 조성별 커버리지.

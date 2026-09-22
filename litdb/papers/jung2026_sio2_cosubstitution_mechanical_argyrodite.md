# Enhancing the Mechanical Properties of Solid Electrolytes for Crack-Resistant Cathodes in All-Solid-State Batteries — Jung et al. (*Adv. Funct. Mater.* 2026)

> slug `jung2026_sio2_cosubstitution_mechanical_argyrodite` · DOI `10.1002/adfm.78249` · type `mixed (exp 주도 + DFT EOS 보조)` · PDF `litdb/inbox/122. AdvFunctMater_2026_Jung_SiO2_cosubstitution_LPSiSOCl_mechanical_MAIN.pdf` (본문 12 pp) + docx SI (Fig. S1–S15 · Table S1) · digested `2026-09-22` · status ✅

> elements: Li, P, S, Cl, Si, O, Ni, Co, Mn
> methods: DFT, EOS, elastic, XPS

> **저자**: Jae Yup Jung¹˒², **Seung Ho Choi**¹˒³\*, Mansang Ha⁴, Chang Hoon Baek¹, Seung Woo Nam⁵, **Yeokyung Lee⁶**, **Jong-Won Lee⁶**, Dong-Joo Yoo⁵, **Haesun Park**⁴\*, **Min-Sik Park**²\*, **Woosuk Cho**¹\*
> ¹KETI 차세대전지연구센터 · ²경희대 신소재 · ³가천대 화공생명배터리 · ⁴중앙대 융합공학 (**DFT 담당**) · ⁵고려대 기계 · ⁶**한양대 신소재**
> Received 2026-06-05 / Revised 2026-08-12 / Accepted 2026-08-31 · *Adv. Funct. Mater.* 2026, e78249
>
> 🤝 **[공저 인접 — 한양대 참여, 그러나 우리 랩 저자는 없다]** — **Yeokyung Lee·Jong-Won Lee(한양대)** 가 공저자다.
> 두 사람은 `papers/lee2026_mechanical_halogen_argyrodite_drycoating.md`(ACS Nano 2026, 안용훈 제2저자·계산 담당,
> 교신 Jong-Won Lee)의 저자와 같다. **다만 이 논문에는 안용훈이 없고 교신도 한양이 아니다**(KETI/중앙대/경희대).
> ⇒ `[자체]` 가 아니라 **`[공저 인접]`** 으로 읽는다. 기여 부위는 논문에 명시되지 않는다(추정 금지).

---

## 0. 이 digest를 읽는 법 — 우리에게 왜 걸리는가

우리 기계 물성 digest 는 이미 7편이 있다(§11 에 중복/신규 판정을 표로 정리). 이 논문이 **새로 더하는 것은 딱 셋**이다.

> **🔑 세 줄 판정 (먼저 결론)**
> 1. **★★ 우리 `lpsocl`(O-도핑) B₀ 결과의 *독립 외부 확증*.** 그들 O-only 치환 **23.66 → 26.48 GPa (+11.9 %)**,
>    우리 modelc → lpsocl **21.71 → 24.71 GPa (+13.8 %)**. 둘 다 PBE·EOS·단일 O·argyrodite.
>    **절대값이 아니라 상대 stiffening 이 맞는다** — 우리 인용정책(2026-09-18, 상대차만)과 정확히 같은 결의 일치다.
> 2. **★ B₀ functional 사다리에 새 칸이 생긴다**: **Jung PBE 23.66 < 우리 PBE 25.51(VRH)–26.23(EOS)
>    < [Deng16] PBEsol 28.7 < [Torii] PBE-D3 34.7 GPa**. 우리 값이 사다리 **안쪽**에 있다는 것이 또 확인된다.
> 3. **⛔ 그러나 논문의 헤드라인("Si/O 공치환이 골격을 보강한다")은 그들 자신의 Fig. 2a 가 온전히 받쳐 주지 않는다.**
>    ① 공치환(26.70)이 **Si 단독(27.79)보다 무르다** — "공치환이 최적" 은 DFT 가 말한 적 없다.
>    ② O 단독의 stiffening 은 **부피 축소만으로 거의 전부 설명된다**(B·V₀ 곱이 pristine 과 0.6 % 이내).
>    ③ 네 패널의 **V₀ 와 E₀ 가 서로 정합하지 않는다**(§10-①·②). 자세한 것은 §10.

그리고 **우리가 지금 gabia 에서 돌리(다 멈춰 놓)은 `modelc_2x` relaxed-ion 탄성**과 직결된다 — 이 논문은
**Cij 텐서를 계산하지 않았다**(B₀ 만). 즉 우리가 하려는 것이 문헌에 아직 비어 있다는 뜻이다(§7·§8).

---

## 1. 한 줄 요약

**Li₆PS₅Cl 합성 시 비정질 SiO₂ 를 같이 넣어 Si⁴⁺→P⁵⁺(4b) · O²⁻→S²⁻(16e) **공치환**된
**Li₆.₁P₀.₉Si₀.₁S₄.₈O₀.₂Cl (LPSiSOCl)** 를 만들었더니, **DFT 체적탄성률 B₀ 이 23.66 → 26.70 GPa** 로 오르고
**AFM Young's modulus 가 16.6 → 21.2 GPa** 로 올랐으며, 그 "덜 무른" SE 를 쓴 NCM 복합 양극이
**500 사이클 후 용량유지율 83.9 → 90.8 %**, **CAM–SE 접촉 피복률 57.6 → 72.8 %**, **전극 내부 공극률 16.2 → 8.7 %**
로 좋아졌다 — 즉 **"SE 의 탄성률을 적당히 올리면 양극 부피변화가 만드는 기계열화를 줄인다"** 는 명제를,
계산(B₀) → 국소측정(AFM/나노인덴테이션) → 셀(500 cy) → 미세구조(SEM 피복률·나노-XCT 공극률) 의
**네 층으로 이어 붙인** 논문. **대가는 이온전도도 −25 %(1.63 → 1.23 mS cm⁻¹)** 다.

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 조성 (실험) | **Li₆₊ₓP₁₋ₓSiₓS₅₋₂ₓO₂ₓCl**, x = 0 / 0.1 / 0.2 / 0.3. 최적 **x = 0.1 = Li₆.₁P₀.₉Si₀.₁S₄.₈O₀.₂Cl (LPSiSOCl)** |
| 조성 (DFT) | ⚠ **실험 조성과 다르다** — Li₆PS₅Cl · Li₆Si₀.₂₅P₀.₇₅S₅Cl · Li₆PS₄.₇₅O₀.₂₅Cl · Li₆Si₀.₂₅P₀.₇₅S₄.₇₅O₀.₂₅Cl (전부 **Li₆ 고정**) |
| CAM | **LiNi₀.₇Co₀.₁₅Mn₀.₁₅O₂ (NCM)**, **LiNbO₃ 코팅** (화학열화를 의도적으로 억제 → 기계 항만 남기려는 설계) |
| 셀 | Li–In \| SE \| 복합양극. 양극 **80 : 19 : 1** (NCM : SE : Super-P), 로딩 **11.4 mg cm⁻²** |
| 가압 이력 | SE 펠릿 **312 MPa** → 양극 적층 후 **437 MPa** 냉간압 → 조립 후 **6.5 N·m ≈ 65 MPa** 스택압 (별도로 **7 MPa** 저압 시험) |
| 연구유형 | **실험 주도 + DFT 보조**. DFT 는 그림 1장(`Fig. 2a`)·방법 1문단이 전부다 |
| 동기 | NCM 은 충전 중 **~8 vol% 수축** → 국소응력 → 미세균열·계면박리. SE 의 낮은 탄성률은 *압밀*엔 좋지만 *사이클 응력*엔 취약 ⇒ **"변형능 ↔ 기계강건성" 사이의 최적점**이 있어야 한다 |
| 갭 주장 | *"SE 의 기계 물성이 셀 성능에 미치는 영향은 상대적으로 덜 탐구됐다"* — 조성공학으로 **modulus 를 의도적으로 올린** 사례가 적다는 위치 |

---

## 3. 핵심 물성 (수치 전량)

### 3.1 DFT 체적탄성률 — `Fig. 2a` (Murnaghan EOS)

| 모델 (논문 표기 그대로) | **B₀ [GPa]** | V₀ [Å³] (**figure-read ≈**) | vs pristine |
|---|---|---|---|
| **Pristine Li₆PS₅Cl** | **23.66** | ≈ **1035** | — |
| **Si 단독** Li₆Si₀.₂₅P₀.₇₅S₅Cl | **27.79** | ≈ **990** | **+17.5 %** |
| **O 단독** Li₆PS₄.₇₅O₀.₂₅Cl | **26.48** | ≈ **919** | **+11.9 %** |
| **Si–O 공치환** Li₆Si₀.₂₅P₀.₇₅S₄.₇₅O₀.₂₅Cl | **26.70** | ≈ **966** | **+12.8 %** |

- B₀ 값 넷은 **본문·`Fig. 2a` 패널 안 라벨에 활자로** 있다. **V₀ 는 x축 점선 위치를 읽은 것**(±5 Å³) — 논문에 V₀ 표가 없다.
- ⚠ **서열**: Si 단독 > Si–O 공치환 > O 단독 > pristine. **공치환이 최댓값이 아니다** (§10-③).
- E₀(최소점 에너지) figure-read ≈ **−215.53 / −216.85 / −230.84 / −220.30 eV** (±0.03) — 네 패널이 서로 안 맞는다(§10-②).

### 3.2 실험 기계 물성

| 양 | LPSCl | LPSiSOCl | 방법 | 출처 |
|---|---|---|---|---|
| **Young's modulus** | **16.6 GPa** | **21.2 GPa** (+27.7 %) | AFM **PeakForce QNM / force-spectroscopy 모듈러스 매핑**, 256×256 px | `Fig. 2b` |
| **Young's modulus** | **28.6 GPa** | **37.6 GPa** (+31.5 %) | **다이아몬드 팁 나노인덴테이션 + Oliver–Pharr**, **ν = 0.30 가정** | `Fig. S6c` |
| **Hardness** | **1.34 GPa** | **1.56 GPa** (+16.4 %) | 같은 나노인덴테이션 / Oliver–Pharr | `Fig. S6d` |
| **잔류압입깊이** (하중 제거 후) | **46.4 nm** | **35.7 nm** | 최대하중 **70 µN (7.5 V)** | `Fig. S6b` |
| 비가역변형 감소 | — | **−10.7 nm ≈ −23 %** | 위 두 값의 차 | 본문 |

> ⚠⚠ **같은 재료·같은 논문 안에서 E 가 16.6 vs 28.6 GPa (1.72×)** 로 갈린다. 두 값은 **다른 측정량**이다
> (QNM = 얕은 접촉강성 맵, Oliver–Pharr = 깊은 압입 언로딩 기울기 + ν 가정). **어느 쪽도 우리 C_ij 와 같은 양이 아니다.**

### 3.3 이온전도도 — `Fig. 1c` + `Table S1` (Ti\|SE\|Ti, AC 임피던스 7 MHz–0.1 Hz, 15 mV)

| x | 조성 | 비저항 [Ω cm] | **σ [mS cm⁻¹]** | vs x=0 |
|---|---|---|---|---|
| 0 | Li₆PS₅Cl | 613.50 | **1.63** | — |
| **0.1** | **Li₆.₁P₀.₉Si₀.₁S₄.₈O₀.₂Cl** | 812.94 | **1.23** | **−24.5 %** |
| 0.2 | Li₆.₂P₀.₈Si₀.₂S₄.₆O₀.₄Cl | 854.70 | **1.17** | −28.2 % |
| 0.3 | Li₆.₃P₀.₇Si₀.₃S₄.₄O₀.₆Cl | 1520.31 | **0.66** | −59.5 % |

- **할로겐-rich 판**: **Li₅.₈P₀.₉Si₀.₁S₄.₅O₀.₂Cl₁.₃ = 3.8 mS cm⁻¹ (RT)** (`Fig. S2`) — SiO₂ 도입이 Cl-rich 조성과도 양립.
- x = 0.3 에서 **Li₃PO₄ (22.3°, 23.1°) + LiCl (34.9°)** 2차상 (`Fig. 1b`) ⇒ **고용한계 초과**.
- 활성화에너지 **Ea: 보고 없음 (n/a)** — 온도 의존 임피던스를 안 쟀다.

### 3.4 구조·화학 상태

| 분석 | 결과 |
|---|---|
| **XRD** (`Fig. 1b`) | x = 0 / 0.1 / 0.2 상순수 argyrodite (기준 **ICSD no. 418490**). x = 0.3 만 Li₃PO₄ + LiCl |
| **XPS P 2p** (`Fig. 1g`) | LPSCl: PS₄³⁻ **132.2 · 133.0 eV**. LPSiSOCl: 위 + **134.2 eV = PS₃O³⁻** |
| **XPS Si 2p** (`Fig. 1h`) | **Si–O 101.6 eV · Si–S 102.4 eV** (비정질 SiO₂ 는 통상 **104.5 eV** — 즉 미반응 SiO₂ 가 아니다) |
| **XPS S 2p / Li 1s** (`Fig. S5`) | 변화 없음 |
| **³¹P MAS NMR** (`Fig. 1i`) | LPSCl = P1 단일 봉우리. LPSiSOCl = **P1 + P2 + P3** ⇒ P 주변 **S²⁻/Cl⁻ 무질서 증가** |
| **SEM / PSA** (`Fig. 1d–f`) | D₅₀ **1.60 µm (LPSCl) / 1.62 µm (LPSiSOCl)** — 형상·입도 동일(교란변수 제거) |

### 3.5 전기화학 (Li–In 반쪽셀, 65 MPa 스택압)

| 항목 | LPSCl | LPSiSOCl |
|---|---|---|
| 1st 충/방전 (0.1 C) | **232.8 / 180.0** mAh g⁻¹ | **227.0 / 182.1** mAh g⁻¹ |
| 200th 방전 (0.5 C) | **151.8** | **157.5** |
| 500th 방전 (0.5 C) | **137.8** | **151.6** |
| **500 cy 용량유지율** | **83.9 %** | **90.8 %** |
| 500 cy 평균 CE | 99.8 % | 99.9 % |
| 100 cy @1 C 방전용량 | 128.1 | 148.2 |
| 100 cy @2 C 방전용량 | 112.8 | 136.2 |
| 100 cy @3 C 유지율 | **75.3 %** | **91.3 %** |
| 100 cy @5 C 유지율 | **64.5 %** | **85.5 %** |
| 율속(0.1–2.0 C) | **유의차 없음** (`Fig. S9`) | 동 |

**저스택압 7 MPa** (`Fig. 4`): 1st 방전 **175.5 / 176.1** mAh g⁻¹(0.1 C) → 100 cy @0.5 C 유지율 **88.8 % vs 97.5 %**
(`Fig. 4c` 라벨 **88.84 % / 97.49 %**).

**대조실험 — 상한 3.8 V** (`Fig. S10`, 7 MPa): 두 셀이 **거의 동일**, 50 cy 무감쇠.
4.3 V 에서만 차이가 벌어진다 ⇒ **차이는 NCM 의 큰 수축(기계)이 있을 때만 나온다**는 저자의 핵심 논증.

### 3.6 임피던스 / DRT — `Fig. 3e–g`

- LPSCl: 1st → 500th 에 **총 임피던스 뚜렷 증가**; LPSiSOCl: **거의 불변**.
- DRT(500 cy 후): 음극(τ ~10⁰–10² s)과 양극(τ ~10¹–10⁴ Hz = 논문 정의) 영역 분리.
  **figure-read ≈** 양극 피크 γ(τ) **LPSCl ≈ 60 Ω @ τ≈10⁻³ s** vs **LPSiSOCl ≈ 22 Ω @ τ≈10⁻⁴ s**.
  ⚠ **음극 영역 피크도 같이 갈린다 (figure-read ≈ 50 vs 32 Ω @ τ≈20 s)** — 본문은 이걸 논하지 않는다(§10-⑥).

### 3.7 미세구조 (기계열화의 직접 증거)

| 양 | LPSCl | LPSiSOCl | 방법 |
|---|---|---|---|
| **CAM 피복률, 사이클 전** | **76.8 %** | **75.7 %** | 단면 SEM 이미지 분할 (`Fig. S14`) |
| **CAM 피복률, 500 cy 후** | **57.6 %** | **72.8 %** | 같은 방법 (`Fig. 5c–f`) |
| 피복률 손실 | **−19.2 %p** | **−2.9 %p** | 위 두 행의 차 |
| **내부 공극률, 50 cy 후** | **≈16.2 %** | **≈8.7 %** | **3D nano-XCT / XRM**, voxel **0.3 µm** (`Fig. 6a,b`) |
| NCM 입자 내 균열 | 심함(`Fig. 5c` inset) | 경미(`Fig. 5d` inset) | 단면 SEM |
| 50 cy 후 XPS (S 2p·P 2p·Li 1s·Ni 2p) | **두 셀 거의 동일** (`Fig. S15`) | 동 | ⇒ 화학열화 기여 무시 가능이라는 근거 |

### 3.8 대기/수분 안정성 (부수 결과)

50 % RH · 1 h 노출 (100 mg 펠릿, 2 L 밀폐, IR H₂S 검출기, `Fig. S11`):

| 양 | LPSCl | LPSiSOCl |
|---|---|---|
| **H₂S 발생** | **120.8 ppm** | **76.3 ppm** (−37 %) |
| **노출 후 σ** | **0.13 mS cm⁻¹** | **0.57 mS cm⁻¹** (4.4×) |

---

## 4. DFT / 계산 방법 ★

| 항목 | 이 논문 |
|---|---|
| **code** | **VASP** (버전 미기재) |
| **functional** | **PBE-GGA**. **vdW 보정 없음** (D3 언급 없음) |
| **pseudo** | **PAW** |
| **ecut** | **520 eV** (일반) → **E–V 계산은 700 eV** (본문이 두 값을 따로 준다) |
| **k-points** | **Monkhorst–Pack 3 × 3 × 3** |
| **SCF 수렴** | **1 × 10⁻⁸ eV** |
| **셀 / nat** | **52 원자** (= Li₆PS₅Cl 4 f.u.), 출발 구조 **Materials Project `mp-985592`** (F4̄3m) |
| **무질서 처리** ★ | **S²⁻(4d)/Cl⁻(4a) 점유율 50 % 로 설정 → pymatgen 으로 *전수 열거(enumerate)* → 회전·반전·c축 반사 대칭등가 제거 → 전부 완전완화 → *최저에너지 배열 1개* 채택**. 후속 계산은 전부 그 단일 배열 위에서 |
| **치환 방식** | Si → P(4b) 1개, O → S(**Wyckoff 16e**, PS₄³⁻ 안) **1개** |
| **EOS** | **Murnaghan**, `E(V) = (B₀V/B₀′(B₀′−1))[B₀′(1−V₀/V) + (V₀/V)^{B₀′} − 1] + E₀`. **B₀′ 값은 미보고** |
| **E–V 격자** | **6점**, **V/V₀ = 0.96 – 1.02** (⚠ **비대칭** — 압축 4 % / 팽창 2 %) |
| **각 점의 완화** | **격자상수 고정 + 원자위치 완전완화** ⇒ **relaxed-ion 정의** ✅ (우리 relaxed-ion 과 비교 가능) |
| **DFT+U** | 없음 |
| **AIMD / MLIP / NEB / phonon** | **전부 없음** |
| **스핀** | 미기재 |
| **전하보상** | ⛔ **미기재** — 식이 전부 Li₆ 고정이라 Si 함유 두 모델은 52원자 셀당 **형식전하 −1** 이다(§10-④) |

### 4.1 우리 규약과 나란히

| 항목 | **Jung 2026** | **우리 comp1 (QE)** | 판정 |
|---|---|---|---|
| code / PP | VASP PAW | QE (USPP/PAW 계열) | 다름 — B₀ 에 몇 % 기여 가능 |
| functional | **PBE** | **PBE** | ✅ **같다** |
| ecut | 700 eV (E–V) | (계별 상이, `computational_methods_canonical.md`) | — |
| k-mesh | **3×3×3** | **4×4×4 (k×L = 40)** | 그들이 성김 |
| nat | **52** | **52** (comp1) | ✅ 같다 |
| 무질서 | enumerate 전수 → 최저에너지 **단일** 배열 | 같은 계열(enumerate/annealed) 단일 배열 | ✅ **같은 급** |
| EOS 형태 | **Murnaghan**, 6점, V/V₀ 0.96–1.02 | **BM3**, 8점 (comp1) | 형태·점수 다름 |
| ion relax | **relaxed-ion** | **relaxed-ion** | ✅ 같다 |
| 산출 | **B₀ 만** | **B₀ + full 6×6 C_ij + E/G/ν/A** | **그들이 훨씬 얕다** |

---

## 5. Figure set ★  — 봤음/안 봤음 구분

크로핑 **6장 전부 실제로 Read 로 봤다** (`litdb/figures/jung2026_sio2_cosubstitution_mechanical_argyrodite/`).
**SI(Fig. S1–S15) 는 PDF 가 없다** — docx 의 **캡션과 Table S1 만** 읽었고 **SI 그림 자체는 못 봤다**.

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a | argyrodite 셀 도식. 범례 `SiS₄ (4b, 16e)` 짙은 사면체 + `O (16e)` 살구색 구 | Si 가 **4b(PS₄ 중심)**, O 가 **16e(사면체 꼭짓점 S)** 라는 자리 지정이 그림으로 명시 — 우리 O-도핑 자리 선택(lpsocl)과 같은 자리인지 대조할 근거 |
| 1b | XRD x=0/0.1/0.2/0.3 + ICSD 418490 스틱. x=0.3 만 Li₃PO₄(22.3°,23.1°)·LiCl(34.9°) 표시 | **고용한계 x < 0.3** 의 실험 경계. 우리 O 도핑 농도 상한의 문헌 앵커 |
| 1c | Nyquist (Z_re 0–200 Ω). x=0.3 만 반원이 크게 벌어진다. **figure-read ≈** 고주파 절편 x=0 이 최소 | σ 표(Table S1)의 그림 근거. 절편 차이가 작다 = 벌크 저항 차이는 크지 않다 |
| 1d–f | SEM LPSCl/LPSiSOCl + PSD (**D₅₀ = 1.62 µm**) | **입도·형상이 같다**는 교란변수 통제 — 우리가 DEM/미세구조 논문을 볼 때 항상 묻는 것 |
| 1g,h | XPS P 2p (PS₃O³⁻ 134.2 eV 신규) · Si 2p (Si–O 101.6 / Si–S 102.4 eV) | **O 가 PS₄ 안으로 들어갔다**는 직접 증거. 우리 lpsocl 모델(PS₃O 단위)의 실험 정당화 |
| 1i | ³¹P MAS NMR. LPSiSOCl 에서 P2·P3 신규 | **치환이 S/Cl 무질서를 키운다** — 우리 disorder↔C_ij(Zener A) 서사의 실험 다리 |
| **2a** | **★ 핵심.** 4개 E–V 곡선 + Murnaghan B₀. 축: Energy (eV) vs Volume (Å³), 빨간 점 6개 + 곡선 + V₀ 점선 | **우리 B₀ 사다리의 새 칸**. 동시에 **V₀ 가 11 % 까지 벌어지고 E₀ 가 서로 안 맞는다** — §10 비판의 근거 |
| **2b** | AFM: (좌) 힘–거리 곡선 Force 0–300 nN vs Distance 0–80 nm — LPSiSOCl ≈240 nN / LPSCl ≈180 nN 최대, 둘 다 ≈−30 nN 흡착 딥 @≈20 nm. (우) 모듈러스 맵 2장, **로그 컬러바 10⁰–10² GPa** | ⚠ **맵에서 16.6 vs 21.2 를 눈으로 가릴 수 없다** — 컬러바가 2 decade 로그다. 본문이 말한 **히스토그램이 이 그림에 없다**. 우리가 AFM 값을 인용할 때의 주의 |
| 3a–c | 1st / 200th / 500th 전압곡선 (V vs InLi/Li⁺ 1.5–4.0). 1st·200th 거의 겹치고 **500th 에서만 LPSCl 분극이 확 커진다** | **"차이는 늦게 나타난다"** — 단기 시험으로는 기계열화를 못 본다는 실험적 교훈 |
| 3d | 2–500 cy 용량+CE. **figure-read ≈** LPSiSOCl 169 → 149, LPSCl 163 → 138 mAh g⁻¹. CE 둘 다 ≈99.8–100 % | 두 곡선이 **처음부터 평행하지 않다**(시작 6 mAh g⁻¹ 차). 유지율은 각자 정규화라 무방하나 인용 시 명시 |
| 3e,f | Nyquist 1st vs 500th. LPSCl 은 반원이 크게 자라고 LPSiSOCl 은 거의 안 자란다 | 기계열화 → 계면저항 증가의 직접 지표 |
| 3g | DRT γ(τ) 0–80 Ω, τ 10⁻⁷–10² s. 양극/음극 영역 음영 | **figure-read ≈** 양극 60 vs 22 Ω. ⚠ **음극 피크도 50 vs 32 로 갈린다** — 분리층 SE 도 다르기 때문(§10-⑥) |
| 4a–c | 7 MPa 저압. 100 cy @0.5 C 유지율 **88.84 % vs 97.49 %** (그림 안 라벨) | **저스택압에서 차이가 더 크다** — 우리 DEM 축(스택압 ↔ 접촉유지)에 곧장 걸리는 결과 |
| 5a,b | 사이클 전 단면 SEM + EDS(노란색 = S) | 출발 접촉이 같다는 대조 |
| 5c,d | 500 cy 후 단면 SEM + **green=CAM / red=void** 분할. inset 에 NCM 2차입자 1개 — LPSCl 은 입자내 균열선이 뚜렷 | **분할 방식이 명시적**(perimeter 기준 피복률). 우리 DEM coverage 정의와 대조 가능 |
| 5e,f | 피복률 히스토그램 (x: Coverage of each CAM %, y: Ratio 0–0.20). LPSCl 평균 **57.6 %**(봉우리 ≈45–55 %), LPSiSOCl **72.8 %**(봉우리 ≈55–90 %) | ★ **분포가 크게 겹친다**. 평균차 15 %p 는 분명하나 **N·오차막대 없음** — 인용 시 "평균" 임을 밝힐 것 |
| 6a,b | 3D XRM 볼륨 + 공극 분할(주황). LPSCl 은 크고 많고, LPSiSOCl 은 드문드문. 스케일바 5 µm | **16.2 % vs 8.7 %** 의 그림 근거. 컬러바에 **수치 눈금 없음**(Low/Medium/High) — 값은 Avizo 정량에서만 |
| 6c,d | 개념도: low/high Young's modulus → poor/intimate contact | 저자 서사 요약. **데이터 아님** |
| Table S1 | 4조성 비저항·σ | **LPSCl 1.63 mS cm⁻¹** — 본문이 안 준 기준값이 여기 있다 |
| Fig. S6 | 나노인덴테이션 P–h, Oliver–Pharr E·H | **⚠ 그림 못 봄** (SI PDF 미보유). 값 28.6/37.6 GPa·1.34/1.56 GPa 는 본문 활자에서만 |

---

## 6. Post-processing ★

| 무엇 | 도구 | 어떻게 수치화·기록했나 |
|---|---|---|
| **무질서 배열 생성** | **pymatgen** (전수 열거 + 대칭 등가 제거) | 최저에너지 1개만 채택. **배열 개수·에너지 분포 미보고** |
| **B₀** | **Murnaghan EOS 피팅** (도구 미기재 — 자체 스크립트 추정) | `Fig. 2a` 패널 안 텍스트로만. **표 없음 · V₀/B₀′/R² 없음** |
| **결정상 동정** | XRD vs **ICSD 418490** | 정성 (Rietveld·격자상수 정밀화 **없음**) |
| **XPS 피팅** | (도구 미기재) | 성분별 결합에너지만. **면적비·정량 조성 없음** |
| **DRT** | Nyquist → **distribution of relaxation time** 변환 (정규화·λ 미기재) | γ(τ) 곡선만, 피크 면적 정량 없음 |
| **피복률 정량** | 단면 SEM **대비·밝기 조정 → 색분할(green=CAM, red=void) → 둘레(perimeter) 비율** | 입자별 피복률 히스토그램 + **평균**. "이전에 개발된 image analysis technique" 을 인용(refs 62–64) |
| **공극률 정량** | **XRM** (SKYSCAN 2214, 70 kV/110 µA, 0.3 µm voxel, 360°/0.2°, 3-frame avg, ~16 h/시료) → **NRecon** 재구성 → **Avizo** 분할·정량 | "sub-micrometer-scale pores" 의 체적분율 % |
| **NEB / Bader / COHP / DOS / ELF / ESW** | **전부 없음** | — |

---

## 7. 우리 DFT 대비 ★  → `our_dft_baseline.md` · `db/properties/{eos,elastic}.json`

### 7.1 ★★ 가장 중요한 한 줄 — O 치환의 **상대 stiffening** 이 우리와 맞는다

| | **Jung 2026** | **우리** |
|---|---|---|
| 모체 | Li₆PS₅Cl (52 at) | **modelc** = Li₅.₄PS₄.₄Cl₁.₆ (62 at) |
| O 넣은 계 | Li₆PS₄.₇₅O₀.₂₅Cl (**O 1개**) | **lpsocl** = Li₂₇P₅S₂₁OCl₈ (**O 1개**) |
| f.u.당 O | **0.25** | **0.20** |
| 방법 | VASP PBE · Murnaghan · relaxed-ion | QE PBE · BM(ASE) · fixed-cell relax |
| 모체 B₀ | **23.66 GPa** | **21.71 GPa** |
| O 치환 B₀ | **26.48 GPa** | **24.71 GPa** |
| **ΔB₀** | **+2.82 GPa / +11.9 %** | **+3.00 GPa / +13.8 %** |

> ✅✅ **판정: 독립 확증이다.** 코드·모체·셀크기가 다른데 **O 1개가 argyrodite B₀ 를 +12–14 % 올린다**는
> *상대차*가 같다. 우리 `lpsocl_eos_dft_result.json` 의 `interpretation`("Direct O substitution stiffens B0 by
> +3.0 GPa (+13.9 %)")이 **외부 독립 계산으로 처음 뒷받침된다.**
> ⚠ **절대값을 나란히 쓰지 말 것** — 모체가 다르다(그들 Cl=1, 우리 Cl=1.6). 우리 두 값은
> `comparison_group: b0-dft-bm3-v1` 안이라 서로 비교 가능하지만, **그들 값은 그 그룹 밖의 소환값**이다.
> ⚠ 우리 lpsocl 의 `B0_prime = 0.5` 는 *"좁은 ±6 % 격자라 B′ 가 제약되지 않는다 — B₀ 만 인용"* 이라고
> 원장이 이미 경고하고 있다. 그들도 **B₀′ 를 아예 보고하지 않는다**. **양쪽 다 B₀ 만 쓴다.**

### 7.2 B₀ functional / 코드 사다리

| 출처 | 방법 | **Li₆PS₅Cl B₀ [GPa]** |
|---|---|---|
| **[Jung26]** ← 이 논문 | VASP **PBE**, Murnaghan EOS, relaxed-ion, k 3×3×3 | **23.66** |
| **우리 comp1** | QE **PBE**, **relaxed-ion 응력–변형 C_ij → B_VRH** | **25.51** |
| **우리 comp1** | QE **PBE**, **BM3 EOS** (8점) | **26.23** |
| **[Deng16]** | VASP **PBEsol**, 응력–변형 C_ij | **28.7** |
| **[Torii]** | VASP **PBE-D3**, 응력–변형 C_ij | **34.7** |

> **판정: 실질 차이가 아니라 방법 산포다.** 우리와 Jung 은 **같은 PBE · 같은 relaxed-ion 정의**인데 **Δ −10 %** 다.
> 설명 가능한 몫: ① 그들 V₀ ≈ 1035 Å³ vs 우리 1016.6 Å³ (**+1.8 %**, B ∝ 1/V 이면 ≈ −1.8 %),
> ② **EOS 형태**(Murnaghan vs BM3) 와 **비대칭 6점 격자**(0.96–1.02, 압축 쪽에 4점) — B₀ 를 계통적으로 흔든다,
> ③ 코드·PAW·k-mesh(3×3×3 vs 4×4×4). ⇒ **"우리 값이 문헌보다 높다" 같은 방향성 주장 금지.**
> 사다리 순서(PBE < PBEsol < PBE-D3)는 이번에도 유지된다.

### 7.3 항목별 대조

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **B₀ (LPSCl)** | 23.66 GPa (PBE, Murnaghan) | comp1 **26.23**(EOS BM3) / **25.51**(B_VRH) | **−10 %** = EOS 형태 + V₀ + k-mesh. 방법 산포 |
| **O 치환 ΔB₀** | **+11.9 %** | modelc→lpsocl **+13.8 %** | ✅ **일치 (독립 확증)** |
| **Si 치환 ΔB₀** | **+17.5 %** | **우리 Si 계 없음** | 🆕 **문헌이 우리에게 주는 새 정보.** 단 §10-④ 전하보상 문제로 유보 |
| **C_ij / G / E (DFT)** | **없음** (B₀ 만) | comp1 full 6×6 C_ij · E_VRH 22.06 · G_VRH 8.13 · ν 0.356 · A 1.144 | **우리가 훨씬 깊다.** 지금 gabia 에서 멈춰 있는 `modelc_2x` relaxed-ion 탄성은 **문헌에 대응물이 없다** |
| **Young's modulus** | **실험만** AFM-QNM 16.6/21.2 · O-P 28.6/37.6 GPa | comp1 **E_VRH 22.06 GPa** (DFT relaxed-ion) | ⚠ **그들 두 실험값이 우리 DFT 를 사이에 두고 갈린다**(16.6 < 22.06 < 28.6). ⇒ 우리 값의 검증도 반증도 아니다. 측정량이 다르다 |
| **무질서 처리** | pymatgen 전수열거 → 최저에너지 단일 배열 | 같은 계열(enumerate/annealed 단일 배열) | ✅ **규약 동급** — 둘 다 무질서 **앙상블**은 안 한다 |
| **Ea / σ (계산)** | **없음** | MLIP-MD Ea comp1 0.253 / modelc 0.224 eV | 겹치는 계산 축 **없음** |
| **σ (실험)** | 1.63 → 1.23 mS cm⁻¹ (**−24.5 %**) | 우리 실험 없음. lpsocl MD Ea 0.2867 eV(provisional) | ⚠ **우리 Ea 로 이 실험을 설명하면 안 된다** — lpsocl(`md-ea-multiseed-v1`) 과 modelc(`md-ea-singleseed-anchor-v1`) 는 **다른 `comparison_group`** 이라 원장이 직접 순위비교를 금지한다 |
| **band gap / ESW / 계면** | **없음** | comp1 2.066 / modelc 2.099 eV, onset 2.256 V | 축 없음 |

### 7.4 DEM 축 — 값은 못 넘기고 **정성 앵커만**

`our_dem_baseline.md` 는 **값 0개 자리표시(placeholder)** 다 ⇒ 수치 대조는 **지금 불가**. 다만 다음 세 값은
나중에 DEM 기준값이 정본 승격될 때 **바로 쓰일 실측 앵커**다(그때까지는 `comparison_vs_ours_DEM.md` §A 의 기록으로만):

- **사이클 후 전극 내부 공극률 16.2 % → 8.7 %** (nano-XCT, 50 cy, voxel 0.3 µm) — 우리 압밀·공극 축의 *사이클 후* 값. 우리 DEM 은 **초기 압밀**만 다룬다.
- **CAM 피복률 76.8/75.7 % (초기) → 57.6/72.8 % (500 cy)** — 우리 coverage 모델의 시간의존 표적.
- **7 MPa 저스택압에서 차이가 더 벌어진다** — 우리 스택압 sweep 의 방향성 근거.

---

## 8. 적용 인사이트

① **★ 우리 lpsocl B₀ 결과를 이제 "외부 독립 확증 있음" 으로 쓸 수 있다.** 지금까지 `+3.0 GPa (+13.9 %)` 는
   우리 계산 하나뿐이었다. 같은 PBE·같은 relaxed-ion·같은 "O 1개" 로 **+11.9 %** 가 외부에서 나왔다.
   ⇒ 원고/덱에서 O 도핑의 **경화 방향**은 이제 방어 가능하다(**절대값은 여전히 각자 계 안에서만**).

② **★ 우리가 비어 있는 칸이 어디인지가 선명해졌다.** 이 논문은 **B₀ 하나**로 "mechanical reinforcement" 를 주장한다.
   **C_ij·G·ν·Zener A 가 없다** ⇒ `modelc_2x` relaxed-ion 탄성(현재 gabia 에서 LOBSTER 뒤로 밀려 정지)이
   끝나면 **문헌이 못 한 것**을 갖게 된다. 특히 *"O/Cl 이 B 는 올리는데 G 는 어떻게 하나"* 는 아무도 답을 안 했다
   (우리 lpsocl 은 이미 **K_VRH 27.82 / G_VRH 13.58 / E_VRH 35.04** 를 갖고 있다 —
   `comparison_group: elastic-dft-relaxedion-lpsocl-standalone` 이라 계 간 순위화는 금지).

③ **★ "부피 축소 vs 결합 강화" 를 가르는 값싼 진단 하나를 얻었다.** B₀ × V₀ 곱을 보면
   O 단독은 pristine 과 **0.6 % 이내**(순수 부피효과), Si 단독은 **+12 %**(진짜 결합 강화)다.
   ⇒ **우리 도핑 계열(Nd·O·B₂O₃)에도 같은 진단을 붙이자** — "왜 단단해졌나" 를 한 줄로 가른다.
   (⚠ B ∝ 1/V 는 엄밀한 법칙이 아니라 이온결정에서의 어림이다. **진단이지 증명이 아니다**.)

④ **실험 설계에서 배울 것 — 3.8 V 대조실험.** 상한을 3.8 V 로 낮춰 NCM 수축을 없애면 두 셀이 같아진다는
   대조군 하나로 "화학열화 아님, 기계열화 맞음" 을 가른다. **우리가 계면 서사를 쓸 때 요구할 대조군의 표준형.**

⑤ **트레이드오프의 정량 좌표 하나** — B₀ **+12.8 %** / E_AFM **+27.7 %** 를 사는 데 **σ −24.5 %** 를 냈다.
   우리 §E(기계 ↔ 이온 상충) 서사에 **실측 교환비**가 들어온다.

---

## 9. 인용 가능 문장 (deck / paper 용)

- *"O 를 PS₄³⁻ 사면체에 넣으면 argyrodite 의 체적탄성률이 올라간다 — 우리 DFT(modelc → lpsocl, PBE, +13.8 %)와
  독립 외부 DFT([Jung26], PBE, +11.9 %)가 같은 크기의 상대 변화를 준다."*
- *"Li₆PS₅Cl 의 PBE B₀ 는 코드·EOS 형태·k-mesh 에 따라 23.7–26.2 GPa 로 흩어진다 — 절대값 비교 전에
  functional 과 ion-relaxation 을 맞춰야 한다."*
- *"SE 의 탄성률을 올리는 것이 복합 양극의 사이클 수명을 늘린다는 명제는, 500 사이클 유지율(83.9 → 90.8 %)과
  사이클 후 CAM 피복률(57.6 → 72.8 %)·전극 내부 공극률(16.2 → 8.7 %)로 실험적으로 이어져 있다."* (소환값)
- *"그 이득의 대가는 이온전도도 −25 % (1.63 → 1.23 mS cm⁻¹) 였다."* (소환값)
- ⛔ **쓰면 안 되는 문장**: *"Si/O 공치환이 골격을 가장 강하게 보강한다"* — **그들 DFT 는 Si 단독(27.79)이
  공치환(26.70)보다 크다고 말한다.**

---

## 10. 주의 / 한계 — 비판 ★

### ① **V₀ 가 단일원자 치환으로 설명 안 되는 크기로 움직인다** (figure-read)

52원자 셀에서 **S 20개 중 1개**를 O 로 바꿨는데 V₀ 가 **1035 → 919 Å³ (−11.2 %)** 다.
음이온 부피 어림으로 기대되는 값은 **−2 % 남짓**이다(O²⁻ 1.40 Å / S²⁻ 1.84 Å, 24 음이온 중 1개).
게다가 **919 Å³ 는 순수 LPSCl 의 실험 부피(a = 9.86 Å → 958 Å³)보다도 작다** — PBE 가 통상 **과대팽창**하는
계에서 나오기 어려운 값이다. Si 단독도 **−4.4 %** 인데, **Si⁴⁺(r_IV 0.26 Å)는 P⁵⁺(0.17 Å)보다 크므로
부피는 늘어야 한다.** ⇒ **방향과 크기가 둘 다 이상하다.**

### ② **네 패널의 E₀ 가 서로 정합하지 않는다** (figure-read, ±0.03 eV)

같은 "O 1개 추가" 인데:
- pristine → O 단독: **−215.53 → −230.84 eV = −15.31 eV**
- Si 단독 → Si–O: **−216.85 → −220.30 eV = −3.45 eV**

**같은 조작인데 ≈12 eV 차이**다. 읽기오차(0.03 eV)의 400배다.
⇒ 네 셀이 라벨대로의 동일 52원자 조성이 아니거나, 패널 간 계산 조건이 다르다.
**논문에 V₀·E₀·B₀′ 표가 없어 확인할 방법이 없다.** ⚠ *figure-read 기반 지적이므로 "논문이 틀렸다" 가 아니라
**"공개된 정보로는 검증 불가"** 로 쓴다.* SI 에도 이 표는 없다(캡션 확인).

### ③ **DFT 는 "공치환이 최적" 이라고 말하지 않는다**

`Fig. 2a` 서열은 **Si 단독 27.79 > Si–O 26.70 > O 단독 26.48 > pristine 23.66**.
본문은 *"co-substitution … effectively reinforces"* 라고 쓰지만, **공치환은 Si 단독보다 1.1 GPa 무르다.**
초록은 공치환만 부각한다. ⇒ **DFT 가 실험 선택(x=0.1 공치환)을 정당화하는 구조가 아니다** —
실험이 공치환을 고른 이유는 **σ 와 상순도**(§3.3) 이지 B₀ 가 아니다. 그 논리를 논문이 명시하지 않는다.

### ④ **⛔ 알리오발런트 Si⁴⁺ → P⁵⁺ 의 전하보상이 기재되어 있지 않다**

논문 표기대로 `Li₆Si₀.₂₅P₀.₇₅S₅Cl` 을 형식전하로 세면 f.u.당 **−0.25**, 52원자 셀당 **−1** 이다
(Li₆⁺ + Si⁰·²⁵×4⁺ + P₀.₇₅×5⁺ − S₅×2⁻ − Cl⁻). `Li₆Si₀.₂₅P₀.₇₅S₄.₇₅O₀.₂₅Cl` 도 같다.
**즉 중성 셀로 돌리면 가전자대에 정공 1개가 생긴다** — 그게 S 3p 결합을 강화해 격자를 수축·경화시킬 수 있다.
그러면 §10-① 의 "부피가 줄었다"와 **Si 계 두 모델만 B·V₀ 곱이 커진 것**(아래 표)이 한꺼번에 설명된다.

| 모델 | B₀ × V₀ (figure-read) | pristine 대비 |
|---|---|---|
| pristine | 24,490 | — |
| **O 단독** | 24,340 | **−0.6 %** (= 순수 부피효과) |
| **Si–O** | 25,790 | +5.3 % |
| **Si 단독** | 27,510 | **+12.3 %** |

**결정적으로, 실험 조성은 `Li₆.₁`** — 여분 Li 로 전하를 맞춘다. **DFT 모델은 그 Li 를 안 넣었다.**
게다가 실험의 O:Si 비는 **2:1**(x 당 O 2개), DFT 는 **1:1** 이다.
⇒ **DFT 가 계산한 것은 실험이 만든 물질이 아니다.** 방향성 논증으로만 읽어야 한다.
*(이건 우리에게도 거울이다 — Nd 도핑 때 전하보상 규약을 명시해 두지 않으면 같은 지적을 받는다.)*

### ⑤ **AFM 모듈러스 두 값이 1.72× 갈리는데 화해시키지 않는다**

같은 시료에 **QNM 16.6 GPa** 와 **Oliver–Pharr 28.6 GPa**. 논문은 *"reproducing the same relative trend"* 로
넘어간다 — 맞는 말이지만 **절대값은 둘 다 인용하면서 어느 쪽이 무엇인지 구분하지 않는다.**
게다가 **팁 반경·캔틸레버 스프링상수·접촉모델(Hertz/DMT/JKR)·시료 밀도·기공률이 전부 미기재**,
Oliver–Pharr 는 **ν = 0.30 가정**(문헌 argyrodite ν 는 **0.35–0.37**, [Deng16]/[Torii]/우리 0.356)이다.
ν 를 0.37 로 바꾸면 E 는 **수 % 더 내려간다**. ⇒ **절대 E 는 우리 표에 넣지 않는다.**
`Fig. 2b` 의 맵 컬러바는 **10⁰–10² GPa 로그** 라 16.6 과 21.2 를 눈으로 가릴 수 없고,
본문이 근거로 든 **히스토그램은 그 그림에 없다**(캡션에도 "mapping results" 뿐).

### ⑥ **셀 비교가 양극만 바꾼 것이 아니다 — 분리층 SE 도 같이 바뀌었다**

Methods: *"90 mg 의 고체전해질 분말(LPSCl / LPSiSOCl)을 먼저 PEEK 셀에 넣고 312 MPa 로 압착한 뒤 양극을 올렸다."*
⇒ **분리층(separator)까지 각자의 SE** 다. 따라서 이 실험은 *"복합 양극 안의 SE 만 바꿨을 때"* 를 격리하지 못한다.
실제로 `Fig. 3g` DRT 에서 **음극 영역 피크도 50 → 32 Ω 로 같이 갈린다**(figure-read) — 본문은 이걸 언급하지 않고
양극–전해질 계면만 지목한다. LPSiSOCl 의 **수분 안정성 우위**(§3.8)와 **Li–In 계면 거동 차이**가 섞여 있을 수 있다.

### ⑦ **σ −24.5 % 를 "slightly lower" 라고 쓴다**

`Table S1` 에서 1.63 → 1.23 mS cm⁻¹ 은 **4분의 1이 날아간 것**이다. 본문의 *"slightly lower"* 는 과소서술이다.
율속 시험(0.1–2 C)에서 차이가 안 난 것은 사실이나(`Fig. S9`), 그건 이 셀이 **전도도 율속이 아니었다**는 뜻이지
σ 손실이 작다는 뜻이 아니다. **Ea 를 안 쟀기 때문에 σ 가 왜 떨어졌는지도 미해결**이다.

### ⑧ 그 밖에

- **반복수·오차막대가 전 논문에 없다.** 500 cy 유지율 83.9 vs 90.8 %, 공극률 16.2 vs 8.7 %, 피복률 57.6 vs 72.8 %
  — 전부 **셀/시료 1개** 로 읽힌다. 피복률 히스토그램(`Fig. 5e,f`)은 **분포가 크게 겹친다**.
- **XRM 은 50 cy, SEM 피복률은 500 cy** 로 **시점이 다르다.** 두 값을 한 서사로 이을 때 명시해야 한다.
- **Si 의 자리가 실험적으로 확정되지 않았다.** XPS 는 Si–O·Si–S 결합만 말한다. **4b(P 자리) 점유의 직접 증거
  (Rietveld / ²⁹Si NMR)가 없다.** `Fig. 1a` 의 자리 배정은 **가정**이다.
- **k = 3×3×3 · 6점 · 비대칭(0.96–1.02) 격자**는 B₀ 로는 최소한이다. **B₀′ 미보고**라 피팅 품질을 볼 수 없다.
- **DFT 가 전부 0 K · 단일 배열.** 무질서 앙상블·유한온도 없음 — 우리와 같은 한계지만, 우리는 그걸 문서화한다.

---

## 11. 기존 기계 물성 digest 7편과의 **중복 / 신규** 판정 ★

| 기존 digest | 겹치는 것 | **이 논문이 새로 더하는 것** |
|---|---|---|
| `torii2025_lpscl_mechanical_anisotropy_dft` | LPSCl 의 DFT 탄성, relaxed-ion 정의 | 🆕 **치환(Si/O) 계열의 B₀ 비교**. Torii 는 pristine 단일조성만. 🔻 **반대로 이 논문엔 C_ij·이방성·전단파괴가 전혀 없다** — Torii 가 훨씬 깊다 |
| `deng2016_elastic_superionic_electrolytes_dft` | Li₆PS₅Cl B₀ 기준값 | 🆕 **PBE(no vdW) 칸**을 사다리에 추가. Deng 은 PBEsol. 🔻 물질군 스캔·G/B 없음 |
| `sakuda2013_sulfide_mechanical_property` | "황화물은 무르고 냉간가압된다" | 🆕 **무르게가 아니라 *덜 무르게* 만드는 쪽의 정량 사례**. Sakuda 는 무름을 *장점*으로 제시, 이 논문은 **과도한 무름이 사이클에서 단점**이라는 반대편 |
| `bucci2018_mechanical_instability_interface_delamination` | 계면 박리 / 접촉 손실 | 🆕 **박리를 SE *조성*으로 줄인 실험**. Bucci 는 모델(CZM). 🔻 이 논문엔 파괴역학 파라미터(K_IC·G_c)가 없다 |
| `lee2026_mechanical_halogen_argyrodite_drycoating` | argyrodite 기계물성 ↔ 전극 성능, **AFM** | 🆕 **할로겐이 아니라 *중심양이온/음이온*(Si/O) 축**. 같은 한양 저자군의 자매 축으로 읽으면 좋다. 🔻 W_ad·FEM 없음 |
| `deysher2022_transport_mechanical_aspects_assb_review` · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` | "부피변화 → 응력 → 접촉손실" 서사 | 🆕 **그 서사의 *조성 처방* 1차 사례 + 사이클 후 3D 공극률 실측**. 리뷰들은 2차 인용 |
| `song2025_electrochemo_mechanical_microelectrode_ees` | 전기화학–기계 결합 측정 | 🆕 **실제 복합 양극(11.4 mg cm⁻², 500 cy)** 스케일. 🔻 단일입자 수준 응력 측정은 없음 |

> **한 줄 요약**: 기계 물성의 **DFT 깊이**로는 기존 digest 들(Torii/Deng)이 이 논문보다 **훨씬 낫다**.
> 이 논문의 고유 가치는 **① 치환 계열 B₀ 비교(특히 O)** 와 **② 계산 → AFM → 500 cy 셀 → 3D 미세구조까지
> 한 논문에서 이어 붙였다**는 점이다. 우리 관점에서는 **①만 정량적으로 쓰고, ②는 서사·설계 참고**로 쓴다.

---

## 12. 기법 미니 용어집 (이 논문을 읽는 데 필요한 것만)

- **Murnaghan EOS** — 체적탄성률이 압력에 **선형**으로 변한다(B(P) = B₀ + B₀′P)고 가정한 상태방정식.
  **Birch–Murnaghan 3차(BM3)** 는 유한변형 이론에서 유도된 것으로 큰 압축에서 더 정확하다. 우리는 BM3 를 쓴다.
  좁은 부피 구간에서는 둘의 B₀ 가 보통 **1–3 %** 안에서 일치한다.
- **relaxed-ion vs clamped-ion** — 변형을 걸 때 원자를 **놓아주면(relaxed)** 이온이 재배치하며 응력을 풀어 줘
  탄성률이 낮게, **얼려두면(clamped)** 높게 나온다. argyrodite 에서 그 차이가 **2배**다(우리 `elastic.json`).
  이 논문은 *"격자상수 고정 + 원자위치 완전완화"* 라 **relaxed-ion** 이다 → 우리 값과 비교 가능.
- **PeakForce QNM / force-spectroscopy 모듈러스 매핑** — AFM 캔틸레버를 픽셀마다 찍었다 떼면서
  힘–거리 곡선을 얻고, 접촉역학 모델(DMT/Hertz)로 국소 탄성률을 뽑아 **이미지**로 만든다.
  **얕은 접촉**이라 표면·산화층·거칠기에 민감하다.
- **Oliver–Pharr 법** — 나노인덴테이션 **언로딩 곡선의 초기 기울기(접촉강성 S)** 에서 환산탄성률 E_r 을 구하고,
  팁과 시료의 ν 로 시료 E 를 분리한다. **ν 를 가정해야 한다** — 이 논문은 0.30 을 썼다.
- **DRT (distribution of relaxation time)** — 임피던스 스펙트럼을 **완화시간 τ 의 분포**로 역변환해
  겹친 반원들을 분리한다. 정규화 파라미터(λ) 선택에 결과가 의존하는데, 이 논문은 밝히지 않는다.
- **nano-XCT / XRM** — X선 단층촬영. 이 논문은 **voxel 0.3 µm**, 360°/0.2° step, 시료당 ~16 h.
  SEM 단면과 달리 **내부 공극을 3D 로 세므로** 절단면 선택 편향이 없다.
- **Wyckoff 4a / 4b / 4d / 16e (F4̄3m argyrodite)** — 4b = PS₄ 사면체 중심(P), 16e = 그 사면체 꼭짓점(S),
  4a·4d = **자유 음이온 자리(S²⁻/Cl⁻ 가 섞이는 곳)**. 이 논문은 Si→4b, O→16e 로 넣고,
  무질서는 **4a/4d 를 50:50 으로 열거**해서 다뤘다.

---

## 13. 원문 근거 (직접 인용)

- 계산 방법: *"All DFT calculations were performed using the Vienna Ab Initio Simulation Package (VASP) … PAW …
  plane-wave cutoff energy of 520 eV … PBE form of the GGA."* (Experimental §4.5)
- 무질서: *"the bulk structure with 52 atoms was generated by setting the occupancies of the S²⁻ (4d) and
  Cl⁻ (4a) sites to 50%, using … pymatgen … to enumerate all possible configurations. Symmetry-equivalent
  structures were removed … the lowest-energy 50% S²⁻/Cl⁻ configuration was adopted."*
- EOS 격자: *"For each composition, the E–V model comprised six uniformly strained volumes with V/V₀ ranging
  from 0.96 to 1.02 … plane-wave cutoff of 700 eV … 1 × 10⁻⁸ eV … Monkhorst–Pack 3 × 3 × 3 mesh, and
  structural relaxations were performed with fixed lattice parameters and fully relaxed atomic positions."*
- O 치환 자리: *"a single oxygen atom was substituted at the Wyckoff 16e site of the PS₄³⁻ tetrahedra."*
- 기계-전기화학 연결의 대조군: *"we performed a control experiment with the upper cutoff voltage limited to
  3.8 V … In this voltage range, pronounced NCM contraction is largely suppressed, while oxidative
  decomposition of the sulfide solid electrolyte and associated CEI formation can still occur."*
- 저자 자신의 유보: *"Therefore, Young's modulus should be considered together with other mechanical
  properties and interfacial compliance."*

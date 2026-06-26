# Studies of lithium argyrodite solid electrolytes for all-solid-state batteries — Rao & Adams (Phys. Status Solidi A 2011)

> slug `rao2011_argyrodite_se_studies_bvse` · DOI `10.1002/pssa.201001117` · type `exp (합성·XRD·EIS) + bond-valence(BVSE) 경험적 force-field 수송분석` · PDF `9d3bb39a-23._Studies_of_lithium_argyrodite_solid_electrolytes…pdf` · digested `2026-06-26` · status ✅
> **저자**: R. P. Rao*, S. Adams** — Department of Materials Science and Engineering, **National University of Singapore (NUS)**. 교신 둘 다 (mserp@nus.edu.sg / mseasn@nus.edu.sg). Phys. Status Solidi A **208, No. 8, 1804–1807 (2011)**. Received 29 Sep 2010, accepted 4 Jan 2011, online 4 Jul 2011.
> **태그**: `[외부]` — NUS Singapore (Hanyang/J-W Lee/Y.M.Lee/Cho/Kang/Cha 그룹 **아님**). 연구유형 = **Original Paper(연구논문)**, 리뷰·학위논문 아님. 짧은 4쪽 정통 연구논문.

---

## 0. 이 digest를 읽는 법 (가장 중요)

이 논문은 **argyrodite 분야의 "기원 문헌" 중 하나**다(2010 투고, 2011 출판). 두 가지를 한다:
1. **합성·물성 보고**: Li₆PS₅X (X = Cl, Br, I)를 **고에너지 볼밀 + 550 °C/5 h 짧은 어닐링**으로 만들어 σ(RT)·Ea를 측정. *핵심 합성 메시지* = Deiseroth의 원전(7일 장시간 합성)을 **밀링+짧은 어닐링으로 극적 단축**.
2. **이온수송 경로 분석**: DFT/AIMD가 *아니라* **bond-valence(BV) 경험적 force-field**(Adams 본인 방법)로 Li⁺의 *3차원 이동 경로 네트워크*를 시각화·정량. cage 안(intra-cage)·cage 간(inter-cage) hop의 **경로별 활성화에너지(0.15–0.35 eV)**를 단계별로 매긴다.

> 🔑 **우리에게 왜 중요한가 (3가지)**:
> 1. **할라이드 3종(Cl/Br/I) Ea·σ 정본값** — 한 논문이 같은 합성·같은 측정으로 Cl, Br, I를 *동시에* 보고. 우리 modelc/comp1(Cl계만)을 **Cl→Br→I 트렌드의 어디에 놓이는지** 외부 좌표로 잡아줌.
> 2. **inter-cage hop = dc 율속**의 *경로 해부* — 우리 AIMD `li_transport.json`/inter-cage 서사의 **structural 대응물**. BV가 "intra-cage(Li1 hexagon, 낮은 장벽) → inter-cage(cage 간 interstitial, 가장 높은 장벽 = dc 율속)" 위계를 직접 보여줌. 우리 percolation/migration_volume 멘탈모델의 **2011년 1차 출처**.
> 3. **Adams BVSE = 우리 AIMD의 *0 K 경험적 사촌*** — 같은 "Li가 어디로 어떤 장벽으로 가나"를 *다른 방법*으로 묻는다. 방법 위계(BVSE < NEB < AIMD)를 명시할 때 BVSE가 가장 싼 끝. 우리가 더 엄밀(AIMD relaxation·correlated motion)임을 정직하게 말하는 근거.
>
> ⚠ **정직하게**: 이 논문의 Ea는 **경험적 BV force-field 상의 *isosurface 임계*에서 읽은 값**이라 **격자 relaxation을 무시**(저자 명시: "neglects relaxation"). 절대 Ea는 NEB/AIMD와 다를 수 있고, 실제로 *실험 NMR*(0.04 eV)·*임피던스*(0.32 eV)·*MD*(0.30 eV)가 서로 크게 갈린다(아래 §3·§5). **BV Ea를 우리 AIMD Ea(0.253/0.224)와 절대 등치 금지** — 같은 *물리(inter-cage 율속)*, 다른 *척도*. 또 X=I는 σ가 ~10⁻⁷ S/cm로 *매우 낮아* Cl/Br과 **수송 메커니즘 자체가 다름**(disordered Li1 triplet).

## 1. 한 줄 요약
Li₆PS₅X (X = Cl, Br, I)를 **볼밀 + 550 °C 짧은 어닐**로 합성(Deiseroth 7일 → 극적 단축)하고, **bond-valence 경험적 force-field**로 Li⁺ 3D 이동망을 해부 → **Cl·Br은 anion disorder 덕에 inter-cage 율속 장벽 ~0.3 eV·σ ~10⁻³ S/cm(LiPF₆ 액체급)** 인 반면 **I는 Li1-triplet disorder로 σ ~10⁻⁷ S/cm(3–4 자릿수 낮음)** → "halide disorder가 inter-cage 연결을 만들어 superionic을 켠다"는 분야의 **초기 정본**.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 조성 | **Li₆PS₅Cl, Li₆PS₅Br, Li₆PS₅I** (X = Cl, Br, I 전 할라이드) — 화학량론(stoichiometric, Cl-rich 아님) |
| 공간군 | **F-43m**(cubic argyrodite aristotype), Z 표준 |
| 핵심 질문 | (a) Deiseroth 장시간 합성을 *어떻게 단축*하나 (b) Li⁺ 3D 이동 경로가 **할라이드별로 어떻게 다른가**(왜 I가 느린가) |
| 방법 | **합성**: 고에너지 볼밀(Agate, 45 mL pot, 10 mm ball ×15) 20 h → 550 °C/5 h 어닐(Ar). **구조**: XRD(Cu Kα, PANalytical X'Pert PRO) + **Rietveld(GSAS/EXPGUI)**. **σ**: 임피던스(Solartron SI1260, 1 Hz–10 MHz, SS 전극). **수송이론**: **bond-valence(BV) 경험적 force-field + Morse-type 에너지 스케일** → E(Li) isosurface로 이동망. |
| 동기·갭 | Ag⁺/Cu⁺ thiophosphate(Ag₈GeS₆ 광물류)는 *anharmonic 정밀 구조*가 있어 수송분석 가능하나, **Li 화합물은 Li 산란이 약하고 저온 상전이로 단결정 연구가 어려워** 상세 모델이 없었음 → BV로 우회. |
| 선행 | **Deiseroth([2], Angew 2008 = INDEX DFT-관련 #1 계열)**: Li₆PS₅X 최초 합성·구조(단결정 X-ray). **Pecher([11], Chem. Eur. J. 2010)**: ⁷Li NMR·차이 Fourier로 Li 분포. 이 둘의 데이터를 BV 모델 검증에 사용. |
| 위치 | **분야 origin 클러스터(2008–2011)**: Deiseroth(합성·구조) → Rao&Adams(빠른 합성 + BV 수송경로) → 이후 Kraft/Minafra(분극률·σ trend)·Schlem(disorder)·우리(AIMD/grand-potential). |

## 3. 핵심 물성 (수치 총정리) ★

### 3a. 이온전도도 σ + 활성화에너지 Ea (임피던스, Arrhenius)
| 조성 | σ (ball-milled) | Ea (ball-milled) | σ (어닐 결정질) | 격자상수 a (Å, Rietveld) |
|---|---|---|---|---|
| **Li₆PS₅Cl** | **3.3 × 10⁻⁵ S/cm** | **0.38 eV** | **1.9 × 10⁻³ S/cm** | **9.850(4)** |
| **Li₆PS₅Br** | **3.2 × 10⁻⁵ S/cm** | **0.32 eV** | **6.8 × 10⁻³ S/cm** | **9.980(8)** |
| **Li₆PS₅I** | **2.2 × 10⁻⁴ S/cm** | **0.26 eV** | **4.6 × 10⁻⁷ S/cm** | **10.142(3)** |

> 🔑 **읽는 법(매우 중요)**:
> - **결정질(어닐) σ**: **Cl 1.9 / Br 6.8 (둘 다 10⁻³ S/cm = "LiPF₆ in carbonate" 액체급) ≫ I 4.6×10⁻⁷** (Cl/Br보다 **3–4 자릿수 낮음**). → **I = "느린 할라이드"**. 본문: "이것이 oxide argyrodite(Li₆PO₅X)가 ~10⁻⁹ S/cm로 *훨씬* 낮은 이유와 같은 부류"로 논의.
> - **ball-milled(어닐 전) σ**: 역설적으로 **I(2.2×10⁻⁴)가 Cl/Br(~3×10⁻⁵)보다 높게** 측정 — 단 이건 *부분 결정질·비정질 혼합*의 값이라 결정질 trend(I 최저)와 반대. 저자는 어닐 결정질 값이 본질이라고 해석.
> - **Ea(ball-milled, 임피던스 Arrhenius)**: Cl 0.38 > Br 0.32 > I 0.26 eV. **격자 클수록(a↑: Cl 9.85 < Br 9.98 < I 10.14) Ea↓** 경향.

### 3b. Bond-valence 경로별 활성화에너지 Ea (BV isosurface 임계, relaxation 무시)
> ⚠ 이 값들은 **§3a의 임피던스 Ea와 별개** — BV force-field 상에서 E(Li) isosurface 임계를 올리며 *연결되는 경로*의 장벽을 읽은 것. "intra-cage 저장벽 → inter-cage 고장벽(dc 율속)" 위계를 보여줌.

| 조성 | 경로 위계 (낮은 → 높은 임계) | dc 율속 (long-range) Ea | 특이 |
|---|---|---|---|
| **Li₆PS₅Cl** | 3개 반점유 Li 자리 잇는 **hexagon(육각) 경로 Eₐ=0.18 eV** → interstitial로 cage 확장 **0.22 eV** → cage 간 직접 연결 **0.35 eV** | **0.35 eV** | 사이트가 실험 반점유 Li1과 일치(BV 검증 OK) |
| **Li₆PS₅I** | Li1–Li2–Li1 **triplet** disorder(Pecher) → Li2 매개 dumbbell 국소 hop **0.09 eV** → 비국소 hop **0.043 eV(NMR)** → S2 주위 cage **0.15 eV** → cage 간 interstitial **0.33 eV** | **0.33 eV** | dc 0.33 = 저온 임피던스 0.32·MD 0.30과 *현저히 일치* / MD는 0.14 eV 국소운동도 시사 |
| **Li₆PS₅Br** | Cl·I의 **혼합 특성**(Klerk: Li1–Li2–Li1 triplet) → Li1 잇는 **hexagon(3 Li1 + 3 interstitial) Eₐ=0.15 eV** → cage(S2/Br 주위, 84% S/16% Br) **0.25 eV** → cage 간 interstitial **0.27 eV** | **0.27 eV** | S2/Br2·Br3/S3 무질서로 BV 모델 정확도 낮을 수 있음(저자 명시) |

> 🔑 **핵심 메시지**: 세 할라이드 *모두* long-range(dc) 율속 장벽이 **ca. 0.27–0.35 eV로 비슷**한데(*경로 위상은 다름*), 그런데도 **σ는 I만 3–4 자릿수 낮다**. 저자 해석: **NMR이 보는 낮은 Ea(0.04 eV)는 *extended local cage 안의 hop*이라 dc 전도와 무관** — dc는 cage *간* 연결 장벽이 지배. 또 oxide(Li₆PO₅X)는 O2 위치가 S2와 달라 cage·long-range 경로가 *근본적으로 다르고* local 0.4 eV/long-range 0.57 eV로 더 높아 σ ~10⁻⁹로 더 낮음.

### 3c. 그 외
| 항목 | 값 | 비고 |
|---|---|---|
| SEM 입자 | **~100 nm** 나노결정 (Li₆PS₅Br) | 볼밀 산물 |
| Rietveld 정밀화 변수 | **49개** (12 background + 7 profile + 1 cell + 24 atomic coord + 3 ADP + 1 prefer-orient + 1 scale) | GSAS, single-crystal 출발모델(Deiseroth) |
| BV 식 (자리 식별) | S_{Li–X} = exp[(R₀−R)/b] | bond length R ↔ bond valence S |
| Morse-type 에너지 | E = D₀{s_rel² − 2 s_rel}, s_rel = s/s_min | BV mismatch를 *절대 에너지*로 환산 → 활성화E의 경험적 상관 |
| 합성 단축 | Deiseroth **7일** → 본 연구 **20 h 밀 + 5 h 어닐** | 핵심 실용 메시지 |

## 4. DFT/계산 방법 ★ — (DFT 아님: bond-valence 경험적 force-field)
- **code / 방법**: **bond-valence(BV) site energy + Morse-type interaction energy**. Adams 본인의 BVSE 계열 방법(EXGUI/이전 논문[10]에서 구현). **DFT·AIMD·MLIP·NEB 전부 아님.**
- **수송 모델**: 이동 Li⁺를 **E(Li) isosurface(constant bond-valence energy)로 둘러싼 영역**으로 표현. 격자 0.1 Å 미만 해상도 grid에서 E(Li) 계산. isosurface 임계를 올리며 *연결되는 경로*(occupied + vacant Li 자리 포함하는 연속 migration pathway)가 처음 percolate하는 임계값 = **그 경로의 활성화에너지의 경험적 추정**.
- **BV 파라미터**: R₀·b를 *softness 보정* + 1차 배위 너머 상호작용 포함 → 비평형 자리 BV를 더 정확히. Morse D₀로 절대 에너지 스케일화.
- **구조 입력**: 자체 Rietveld(밀·어닐 시료) + Deiseroth single-crystal 모델[2] + Pecher NMR/difference-Fourier Li 분포[11].
- **무질서 처리**: **실험 점유(half-occupied Li, S²⁻/halide 무질서)를 BV grid에 그대로 반영** — SQS/enumerate 아님. I는 Pecher의 Li1-triplet disordered 분포를 사용.
- **핵심 한계(저자 명시)**: "**이 접근은 relaxation을 무시한다**(neglects relaxation)" — 활성화E 추정은 "광범위한 Li 전도체에서 관찰된 *경험적 상관*"에 기반. → 절대 Ea는 first-principles(NEB/AIMD)와 어긋날 수 있음.
- **장점(저자 주장)**: "단순·신뢰할 만한 경로 식별 방법, *국소 구조 모델*이 본질적 구조 특징을 담으면 됨" — 즉 **싸고 빠른 경로 스크리너**.

## 5. 결과 — 섹션별 상세

### 5.1 합성·상순도 (XRD/Rietveld, Fig 1)
볼밀만(24 h)으로는 **부분 결정질** — Li₂S, P₂S₅, LiX 출발물질 피크 + argyrodite 일부. **24 h 후 대부분 상이 broad해지고 Li₂S만 남는** 경향. **어닐(550 °C/5 h) 후** 두 시료 모두 argyrodite 결정질로 수렴. **Fig 1 = Li₆PS₅I의 Rietveld fit**(Obs/Cal/Bkg/Diff, 2θ 8–100°). 최종 격자상수 Cl 9.850(4)/Br 9.980(8)/I 10.142(3) Å — 보고값과 잘 일치. → **합성 시간 7일 → 25 h 극적 단축**이 실용적 핵심.

### 5.2 전도도·활성화에너지 (임피던스, §3a)
임피던스 Nyquist를 C_b·R_b·Warburg 등가회로로 피팅. **Arrhenius 거동** 확인. 결정질 σ: Cl 1.9·Br 6.8 (10⁻³ 줄)·I 4.6×10⁻⁷. **결론: Cl·Br = 액체전해질급 superionic, I = 3–4 자릿수 느림.** (저온 Ea 측정은 "in progress"라 후속 약속.)

### 5.3 Bond-valence 경로 해부 (Fig 2, §3b) — 논문의 이론적 심장
**Fig 2**는 X=Cl/Br/I(좌→우) 각각에 대해 isosurface 임계를 4단계(행)로 올리며 경로망을 시각화:
- **1행(가장 낮은 임계)**: 평형 자리(equilibrium sites) — Cl은 실험 반점유 Li1과 일치.
- **2행**: 첫 local Li⁺ 경로(short-range).
- **3행**: extended local pathway *cage* (cage 안에서 닫힌 통로).
- **4행(가장 높은 임계)**: **long-range(dc) 경로** — cage *간* 연결, 이게 dc σ를 결정.

**Cl(좌)**: 3개 반점유 Li1을 잇는 **hexagon Eₐ=0.18 eV** → 4개 hexagon이 2차 interstitial(공칭 Cl 자리)로 **확장 cage Eₐ=0.22 eV** → cage 간 직접 연결로 **3D 망 Eₐ=0.35 eV** 완성.

**I(우)**: Pecher가 제안한 **Li1–Li2–Li1 triplet** disordered 분포 사용. Li2 매개 dumbbell **국소 hop 0.09 eV**(P 자리는 E(Li) 극소 아님, difference-Fourier와 일치). NMR **0.043 eV**(비국소 hop). 6개 dumbbell이 **S2 주위 cage 0.15 eV** 형성 → cage 간 interstitial **Eₐ=0.33 eV**. → **dc 0.33 ≈ 저온 임피던스 0.32 ≈ MD 0.30** *현저히 일치* (MD는 0.14 eV 국소운동도).

**Br(중)**: **Cl·I의 혼합 특성**. Klerk의 Li1–Li2–Li1 triplet. Li1 잇는 **hexagon 0.15 eV** → cage(84% S/16% Br) **0.25 eV** → cage 간 interstitial **0.27 eV**. (단 Br의 S2/Br2·Br3/S3 무질서로 BV 모델 정확도가 Cl보다 낮을 수 있다고 저자가 *직접 경고*.)

### 5.4 oxide argyrodite 비교 (§4 끝, §5)
Li₆PO₅X(O가 S 자리)는 **O2 위치가 S2와 달라** cage·long-range 경로가 *근본적으로 다름*. BV: local **0.4 eV**·long-range **0.57 eV**(둘 다 sulfide보다 높음) + interstitial 자리 부재 → 왜 oxide가 σ ~10⁻⁹ S/cm(실험 Ea 0.66 eV)로 *훨씬 낮은지* 설명. → **"anion(S vs O)·interstitial 가용성이 long-range 경로를 켜고 끈다."**

## 6. 메커니즘 종합
1. **합성**: 볼밀이 반응을 일으키고(부분 결정질) 짧은 어닐이 결정화 완성 → 7일→25 h.
2. **수송 위계**: Li⁺ 전도는 **intra-cage(낮은 장벽 0.09–0.18 eV) → extended cage(0.15–0.25 eV) → inter-cage(0.27–0.35 eV)** 의 3단 위계. **dc(거시) σ는 *가장 높은* inter-cage 연결 장벽이 율속.**
3. **왜 I가 느린가**: dc 율속 장벽 자체는 0.33 eV로 Cl(0.35)·Br(0.27)과 비슷한데 σ는 3–4 자릿수 낮음 → 저자는 **경로 *위상(topology)*과 자리 *연결성*·attempt frequency·carrier 분포 차이**로 귀속(단순 장벽 높이로 환원 안 됨). I는 Li1-triplet disorder라 *연결 통로*가 Cl/Br의 hexagon보다 비효율.
4. **NMR Ea(0.04 eV)의 함정**: NMR 저Ea는 *cage 안 hop*이라 **dc와 무관** — "낮은 NMR Ea ≠ 빠른 거시 전도"를 명확히.

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
> ⚠ 이 논문은 **화학량론 Li₆PS₅X**(Cl-rich 아님)·**BV 경험적 force-field(relaxation 무시)**·**0 K isosurface**. 우리 comp1=Li₆PS₅Cl(동일 조성!)·modelc=Li₅.₄PS₄.₄Cl₁.₆(Cl-rich)·**AIMD(relaxation 포함)**. **방법·척도가 달라 절대 Ea 등치 금지** — 같은 *물리(inter-cage 율속)* 확인용.

| 항목 | Rao&Adams 2011 | 우리 (comp1 / modelc) | 일치 / 차이 + 이유 |
|---|---|---|---|
| **조성 comp1 직접 대응** | **Li₆PS₅Cl** (화학량론, 동일!) | **comp1 = Li₆PS₅Cl** | ✓ *조성 정확 일치* — comp1의 외부 실험·경로 좌표 |
| **dc σ (LPSCl, RT)** | **1.9 × 10⁻³ S/cm** (어닐 결정질) | AIMD 600K 외삽 RT ~**3.35 mS/cm**(comp1 4fu) — 3–5× 과대 | **✓ 같은 차수(10⁻³)** — 우리 UMA 과대(MLIP overshoot+bulk vs pellet)는 알려진 한계. Rao 1.9 mS/cm = 실측 anchor |
| **Ea (LPSCl)** | **0.38 eV**(임피던스, ball-milled) / **0.35 eV**(BV inter-cage dc) | **0.2532 eV**(AIMD Arrhenius, 4fu natural, PAPER_GRADE) | △ **우리가 낮음** — (a) Rao 임피던스 0.38=ball-milled(결함·입계 포함, 결정질은 더 낮을 수 있음) (b) BV 0.35=relaxation 무시(과대 경향) (c) 우리 AIMD=relaxation+correlated motion(낮춤). **방법 차이로 0.1 eV gap은 예상 범위** — Schlem 2020 ordered LPSCl(우리 0.253 match)과 정합. *절대 등치 금지* |
| **σ↑·Ea↓ 레버** | **anion disorder(S²⁻/X⁻) + interstitial 가용성**이 inter-cage 연결을 켬 | Cl-rich(modelc)서 disorder↑ → D 2.6×↑·Ea 0.253→0.224 | **✓✓ 같은 기전** — Rao는 X종류로(Cl/Br/I), 우리는 Cl *증량*으로 같은 "disorder→inter-cage 연결→σ↑" 레버. 우리 modelc는 Rao 틀의 *Cl축 연장* |
| **inter-cage = dc 율속** | BV 4행: cage 간 연결(0.27–0.35 eV)이 long-range σ 지배, intra-cage(0.09–0.18) 빠름·non-limiting | 우리 inter-cage 서사·`migration_volume_fraction`(BVSE 병목 부피)·percolation 멘탈모델 | **✓✓ 우리 inter-cage 서사의 *2011 1차 출처·structural 대응물*** — [GG]/[Liu] Li 확률밀도와 같은 그림을 *BV 경로*로 |
| **할라이드 trend (Cl/Br/I)** | 결정질 σ: Br 6.8 > Cl 1.9 ≫ I 4.6e-7 (10⁻³ vs 10⁻⁷); Ea(BV dc) Br 0.27 < I 0.33 < Cl 0.35 | 우리 Cl계만(comp1/modelc); [Rao2025]가 Cl–I AIMD로 보완 | **✓ 외부 trend 좌표** — 우리 Cl계를 "Cl≈Br ≫ I" 위계에 위치. [Rao2025] AIMD(I=전도 아니라 상안정/계면 레버)와 결론 결: I는 dc σ 약함 |
| **방법 위계** | BVSE = 0 K 경험적 force-field(relaxation 무시, isosurface) | AIMD = BO-MD relaxation + correlated motion (Haven<1) | **우리가 더 엄밀** — BVSE는 *싼 경로 스크리너*(NEB/AIMD의 사촌). 우리 AIMD가 relaxation·협동운동을 잡음(BV는 못 잡음). 정직한 위계 명시 |
| **band gap / 산화 onset** | n/a (논문에 없음) | gap 2.066/2.098 eV(PBE); onset 2.256 V | — Rao는 전자구조·산화 미다룸. 비교 불가 |
| **기계적** | n/a | E_VRH 22.06/27.66 GPa | — Rao는 elastic 미다룸 |

## 8. Figure / Table set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **Fig 1** | **Li₆PS₅I Rietveld fit**(Obs/Cal/Bkg/Diff, 2θ 8–100°) — 어닐 후 결정질 argyrodite 확인 | 합성·상순도 reference. 우리 구조검증(comp1/modelc V0) 출발모델 계열(Deiseroth) |
| **Fig 2** | **BV Li⁺ 이동경로 (X=Cl/Br/I × 4 isosurface 임계 행)** — 1행 평형자리 → 2행 local → 3행 extended cage → 4행 **long-range inter-cage** | **🔑 우리 inter-cage 서사의 그림 원형**. "intra-cage 빠름·non-limiting / inter-cage=dc 율속" 위계를 직접 시각화. deck에서 "이동망 위계"를 설명할 때 인용 가능(2011 origin) |
| Eq.1 | S_{Li–X} = exp[(R₀−R)/b] (bond-valence) | BV로 *자리 식별*하는 식 — 우리 BVSE/migration_volume의 정의식 출처 |
| Eq.2 | E = D₀{s_rel²−2 s_rel} (Morse-type) | BV mismatch → 절대 에너지(eV) 환산 — 우리 BVSE 에너지화의 방법론 |

## 9. Post-processing ★
- **무엇**: **bond-valence isosurface mapping**(E(Li) constant-energy 표면으로 이동망 추출 + 임계 percolation으로 경로별 Ea 추정). NEB/Bader/COHP/grand-potential **아님**.
- **도구**: Adams 자체 BV 코드(EXGUI 계열, [9][10]) + **GSAS/EXPGUI**(Rietveld). VESTA류 시각화는 미명시.
- **수치화·기록**: (a) Rietveld → 격자상수·49 변수·원자좌표. (b) BV grid(<0.1 Å) → E(Li) isosurface → 임계 올리며 경로 percolation → **경로별 Ea(eV)**. (c) 임피던스 Arrhenius → σ(RT)·Ea.
> 우리 적용: **BVSE isosurface = 우리 `migration_volume_fraction`(BVSE 병목 부피)의 방법론 출처**. 단 우리는 AIMD가 main이고 BVSE는 보조 스크리너 — Rao가 BVSE를 *경로 위계 해부*에 쓴 방식을 차용하되, *절대 Ea는 AIMD로* 확정.

## 10. 적용 인사이트 (내 연구에 어떻게)
1. **comp1의 외부 실험 anchor 확보**: Rao **LPSCl σ=1.9×10⁻³ S/cm**(어닐 결정질)는 우리 comp1과 *동일 조성*의 외부 실측 → 우리 AIMD RT 외삽(~3.35 mS/cm, 3–5× 과대)의 검증점. "우리 UMA가 차수는 맞고 절대값은 과대"를 정량 확인.
2. **inter-cage 서사의 origin 인용**: 우리 "dc σ는 inter-cage 연결이 율속, intra-cage는 빠름" 서사를 **2011 BV 경로 해부**로 1차 출처화. [GG]/[Liu] AIMD 확률밀도와 *방법은 다르나 같은 위계*를 보임 → 서사 견고화.
3. **할라이드 trend 좌표**: 우리 Cl계(comp1/modelc)를 "**Cl≈Br(10⁻³) ≫ I(10⁻⁷)**" 위계에 위치. I는 dc σ가 약하다(Rao)는 점이 [Rao2025](I=상안정/계면 레버지 전도 레버 아님)와 일관 → "I 치환은 σ↑가 목적이 아님"을 두 외부 논문이 지지.
4. **방법 위계 정직화**: BVSE(Rao) < NEB < AIMD(우리). BVSE는 relaxation·correlated motion을 못 잡아 절대 Ea가 어긋남(NMR 0.04 / 임피던스 0.32 / MD 0.30 / BV 0.33–0.35로 *제각각*) → 우리 AIMD가 더 엄밀함의 근거. *단 BVSE는 싸고 빠른 경로 스크리너로 유효*.
5. **disorder=레버의 일반화**: Rao(X종류로 disorder 조절) + 우리(Cl 증량으로 disorder 조절)가 같은 "anion disorder→inter-cage 연결→σ↑" 레버 → **수단(할라이드 교환 vs Cl 증량)은 달라도 물리는 하나**. percolation framework([Perc])·hopping vocabulary([Dyre])와도 정합.

## 11. 인용 가능 문장 (deck/paper용)
- "Rao & Adams (2011) reduced the argyrodite synthesis time from Deiseroth's 7 days to a 20 h mill + 5 h anneal, while bond-valence pathway analysis resolved the Li⁺ transport hierarchy: fast intra-cage hops (0.09–0.18 eV) gated by the rate-limiting inter-cage connection (0.27–0.35 eV) that sets the dc conductivity."
- "Crystalline Li₆PS₅Cl reaches σ ≈ 1.9×10⁻³ S/cm — the same 10⁻³ S/cm order our AIMD predicts for comp1 (3.35 mS/cm), with our value 3–5× high as expected from foundation-MLIP overshoot."
- "Across X = Cl, Br, I the dc rate-limiting inter-cage barrier is similar (~0.3 eV), yet σ(I) is 3–4 orders lower — long-range conduction is governed by pathway *topology* and carrier connectivity, not barrier height alone."
- "Our AIMD (with full relaxation and correlated motion, H_R<1) supersedes the 0 K bond-valence estimate, which by construction neglects relaxation — explaining the spread among NMR (0.04 eV), impedance (0.32 eV) and BV (0.33–0.35 eV)."

## 12. 주의 / 한계 (over-claim 방지)
- **BV Ea ≠ AIMD Ea (척도 다름)**: 경험적 force-field·isosurface·**relaxation 무시**(저자 명시). 절대 Ea를 우리 0.253/0.224와 등치 금지 — 같은 *물리(inter-cage 율속)*만.
- **Ea 값들이 방법마다 크게 갈림**: 같은 LPSI에서 NMR 0.04 / 국소 MD 0.14 / 임피던스 0.32 / MD 0.30 / BV dc 0.33 — "낮은 NMR Ea ≠ 빠른 dc σ"(cage 안 hop). 한 숫자만 떼어 인용 금지.
- **조성 = 화학량론 Li₆PS₅X (Cl-rich 아님)**: modelc(Cl₁.₆)와 직접 비교 시 "Cl 증량 효과"는 Rao에 없음 — Rao는 *할라이드 종류* 축, 우리 modelc는 *Cl 함량* 축.
- **ball-milled σ trend(I 최고)는 결정질 trend(I 최저)와 반대** — *결정질*이 본질. ball-milled 값을 σ 결론으로 쓰지 말 것.
- **Br BV 모델 정확도 낮음(저자 경고)**: S2/Br2·Br3/S3 무질서로 Br 경로 Ea는 Cl보다 불확실.
- **2011 origin 논문**: 이후 분극률(Kraft 2017)·disorder 정량(Schlem 2020)·grand-potential(Mo 2015)이 더 정밀화 → Rao는 *초기 정본·경로 해부*로 인용하되 최신 σ/disorder 정량은 후속 문헌으로.
- **전자구조·산화·기계 = 미다룸(n/a)** — 이 논문으로 그 축 비교 금지.

## 13. 기법 용어 미니사전
- **Bond valence (BV)**: 결합길이 R ↔ 결합가 S = exp[(R₀−R)/b]. 한 원자의 BV 합이 산화수와 맞는 자리 = 그 이온이 앉기 좋은 평형 자리. *자리 식별*에 씀.
- **BVSE (BV site energy)**: BV mismatch를 Morse-type으로 *절대 에너지(eV)* 화 → 이동 이온의 **에너지 지형(E(Li))** 을 grid로 계산. NEB/AIMD보다 *훨씬 싼* 경로 스크리너(단 relaxation 무시).
- **Isosurface percolation**: E(Li) 등에너지 표면을 점점 높이며 *연결되는 경로*가 처음 시료를 가로지르는(percolate) 임계 에너지 = 그 경로의 활성화E 추정.
- **intra-cage / inter-cage hop**: argyrodite의 Li₆X cage *안* 빠른 hop(낮은 장벽) vs cage *사이* 느린 hop(높은 장벽 = dc 율속). σ는 inter-cage가 지배.
- **Li1 / Li2 자리, triplet**: argyrodite Li 부분점유 자리. I/Br은 Li1–Li2–Li1 "triplet"(Pecher/Klerk) 분포 — Cl의 단순 반점유 hexagon과 다른 위상.
- **anion disorder (S²⁻/X⁻)**: S와 halide가 4a/4c(또는 4d) 자리를 공유 점유 → 이게 inter-cage 통로를 열어 σ↑. Cl이 disorder 최대, I 최소(이 trend가 σ 위계와 연결).
- **Rietveld refinement**: 분말 XRD 전체 패턴을 구조모델로 최소제곱 피팅(여기 GSAS, 49 변수) → 격자상수·점유·원자좌표.

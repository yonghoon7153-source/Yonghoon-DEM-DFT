# High-voltage stability of sulfide-based all-solid-state batteries: benefit of the parasitic reaction — Kang et al. (Chem. Commun. 2025) — **[우리 그룹]**

> slug `kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb` · DOI `10.1039/d5cc04349b` · type `exp (계산 無)` · PDF `8517b4f7-…parasitic_reaction.pdf` · digested `2026-06-26` · status ✅
> **저자**: Junhee Kang†, Yeokyung Lee†, Youngjin Bae, **Jong-Won Lee** (corresponding) — Hanyang University, Dept. of Materials Science & Engineering + Dept. of Battery Engineering (†동등기여). Chem. Commun. **2025, 61, 16850–16853**. Received 30 Jul 2025, Accepted 26 Sep 2025.
> **[우리 그룹]** = 안용훈 그룹 계보(한양대 황화물 argyrodite SE). Kim ICCF / Kim conductive-agent / intertwined-review digest와 동일 태그.

---

## 0. 이 digest를 읽는 법 (먼저 읽으세요 — 흔한 오해 방지)

이 논문 제목의 "benefit of the parasitic reaction"은 **직관에 반하는** 주장이다. 보통 "기생반응(parasitic reaction) = SE가 고전압서 분해 = 나쁨"인데, 이 논문은 **그 분해가 (조건만 맞으면) 오히려 양극을 보호한다**고 말한다. 하지만 **메커니즘을 정확히 잡는 것이 핵심**이다 — 흔히 오해하는 "분해산물(LiCl·sulfate 등)이 passivating CEI를 만들어서 좋다"가 **이 논문의 1차 메커니즘이 아니다.**

이 논문에서 "기생반응이 이롭다"의 진짜 의미는 다음 두 단계다:

1. **무엇이 일어나나**: 고전압(충전, SOC 100 %, 4.25 V vs Li/Li⁺)서 LPSCl이 산화분해(식 1)하면서 **Li⁺를 방출**한다. 이 Li⁺가 인접한 **탈리튬(delithiated)된 Ni-rich NCM 속으로 다시 들어가(=chemical lithiation, 화학적 리튬화)** NCM의 **SOC를 낮춘다**. 즉 "기생반응 = SE 분해가 양극을 부분적으로 *방전*시키는 self-discharge".

2. **왜 이로운가 + 코팅의 역할**: 탈리튬된 Ni-rich NCM(고-SOC, Ni⁴⁺ 많음)은 **구조적으로 불안정**(격자 O 방출 → layered→rock-salt 상전이). 기생반응이 이 NCM을 **다시 리튬화 = SOC를 내려** 불안정한 상태에서 빼내준다 → 구조 붕괴를 늦춘다. **단, bare NCM은 SE 접촉이 불균일**해서 이 리튬화가 **국소적·불균일**하게 일어나(어떤 입자는 과리튬화, 어떤 입자는 여전히 고-SOC) 오히려 응력·열화를 키운다. **conformal SE 코팅**(LPSCl을 NCM 입자에 dry-coating)을 하면 **NCM 표면 전체에서 균일하게 chemical lithiation**이 일어나 → **균질한 SOC 강하 → 균일한 구조 안정화 → 셀 수명↑**.

> 🔑 **한 문장**: "기생반응(SE 산화분해→Li⁺ 방출→NCM 재리튬화)은 피할 수 없지만, **conformal SE 코팅이 그것을 *균일*하게 만들면** 탈리튬 NCM을 균질하게 SOC-강하시켜 구조붕괴를 늦추는 **이로운** 반응이 된다." → 이로움의 핵심은 **"분해를 막는 것"이 아니라 "분해를 균일하게 분배(homogenize)"하는 것**.

> ⚠ **우리 repo와의 연결에서 가장 중요한 구분**: 이 논문의 주 메커니즘은 **"SOC 강하(chemical lithiation)"** 이지, 우리 Nd-passivation 스토리의 **"wide-gap 절연 CEI 형성"**이 *아니다*. 둘은 **다른 물리**다 (자세히는 §7·§12). 다만 (a) 분해 stoichiometry(식 1)는 우리 grand-potential 산화분해와 **정확히 같은 화학**이고, (b) "고전압 계면반응을 *어떻게 관리*하느냐가 수명을 좌우"라는 **상위 프레임**은 공유한다. **"같은 physics"라고 over-claim 하지 말 것.**

---

## 1. 한 줄 요약

Ni-rich NCM(LiNi₀.₈Co₀.₁Mn₀.₁O₂) 입자에 **Li₆PS₅Cl(LPSCl)을 무용매 dry-coating** 하면, 고-SOC 저장(4.25 V 충전 후 100 % SOC calendar aging) 중 일어나는 **LPSCl↔NCM 기생반응(SE 산화분해→Li⁺→NCM chemical lithiation)이 입자 표면 전체에서 *균일*하게 진행**되어 → NCM의 SOC를 균질하게 낮추고(=불안정한 탈리튬 상태 완화) → **layered→rock-salt 상전이를 표면에 국한**시키고 → 계면저항(R_int 4.3 vs bare 더 큼)·warburg 저항을 줄여 → **200 사이클 용량유지율 격차 15.0 %** 만큼 SE-coated가 우수하게 만든다. **"기생반응을 없애지 못하면 균일하게 만들어라"**가 결론.

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 비교 | **Bare NCM** vs **SE-coated NCM** (LPSCl을 NCM에 dry-coating). *조성 변화가 아니라 양극 표면처리 비교* (cf. Zuo는 Cl 함량 비교) |
| 양극활물질(CAM) | **LiNi₀.₈Co₀.₁Mn₀.₁O₂ (NCM811, Ni-rich)** — 고-SOC서 격자 O 방출·상전이로 불안정 |
| SE | **Li₆PS₅Cl (LPSCl = 우리 comp1)** — argyrodite, σ ≈ liquid 수준, 좁은 전기화학창(<2.5 V vs Li/Li⁺ 본문 표현) |
| 음극 | **Li–In** (전위 0.62 V vs Li/Li⁺ 고정 → OCV 모니터링 기준) |
| 핵심 질문 | Ni-rich CAM–SE 계면의 **불가피한 기생반응**을 어떻게 *관리*해 고전압 수명을 얻나? |
| 답 | SE 코팅으로 기생반응(chemical lithiation)을 **균일화** → 균질 SOC 강하 → 구조보존 |
| 선행맥락 | Song et al.(ref 19, dry mechanofusion SE 코팅) = 초기 CE·수명↑(void·tortuosity↓). 본 논문은 그 위에 **"코팅이 *화학·전기화학* 계면반응(기생반응)까지 균일화"**를 더함 |
| 공정 강점 | **dry coating**(planetary centrifugal mixer, 무용매·무바인더) → wet coating 대비 scalability·공정효율 우위 (ref 24,25) |

## 3. 핵심 물성 (수치 총정리)

> ⚠ 전압 기준: 셀은 **Li–In 대극**. 충전 상한 **4.25 V vs Li/Li⁺** (Li–In 0.62 V 보정). "high voltage / high SOC"는 이 4.25 V·100 % SOC 충전 상태를 가리킴.

| 물성 | Bare NCM | SE-coated NCM | 조건/출처 |
|---|---|---|---|
| 코팅 비율 (NCM:LPSCl) | — | **100 : 2 wt%** | dry coating (Fig S1) |
| 코팅 두께(추정) | — | **~44 nm** (완전 균일 가정) | 본문 (잔류 LPSCl 미검출 → 전량 코팅) |
| 양극복합체 비율 (NCM:LPSCl:C) | **72 : 27 : 1** wt% | 72 : 27 : 1 (코팅분 차감해 SE 총량 동일하게 맞춤) | ball-mill |
| 복합체 압연압 / 두께 | 450 MPa / **0.19 mm** (거의 동일) | 450 MPa / 0.19 mm | SEM 단면 |
| LPSCl 탄성계수 | — | **22.1 GPa** | 본문 (vs NCM **175 GPa**) → 연성이 void 채움 |
| 셀 운전압력 / 온도 | 120 MPa stack / 30 °C | 동일 | 전기화학 시험 |
| 초기 용량 (0.5C, 5cyc 후) | 더 낮음 (정성) | **더 높음** | Fig 2a (CAM 활용↑) |
| OCV 강하 (저장 200 h) | 작음 | **10.1 mV 더 큼** | Fig 2b (SE-coated가 self-discharge↑ = 기생반응↑) |
| **R_int (point 3, 200 h 저장 후)** | bare > | **4.3 Ω cm²** | Fig 2d, EIS+TLM (SE-coated가 더 낮음) |
| R_w (Warburg) 추이 | 더 크게 증가 | **유의하게 낮음** (후기) | Fig 2e |
| aged 후 0.5C 용량강하 | **26.4 mAh/g** | **24.4 mAh/g** (덜 떨어짐) | Fig 2f |
| 평균 쿨롱효율 (초기 70 cyc) | **94.2 %** (낮음) | 더 높음 | Fig 2g |
| **200 cyc 용량유지율 격차** | — | **SE-coated가 15.0 % 더 높음** | Fig 2g (핵심 수명 수치) |
| **기생분해 반응식 (식 1)** | `2 Li₆PS₅Cl → P₂S₅ + 5 S + 2 LiCl + 10 e⁻ + 10 Li⁺` | 동일 | 본문 식 (1) |
| 저장 후 표면상 (TEM) | **rock-salt (Fm-3m), 깊이 침투** | **표면 rock-salt + 내부 layered 보존** | Fig 3c,d |
| XRD (003)/(104) 시프트 | 저각 이동(Li↑=SOC↓) + (003) **이질적 분리** | 저각 이동 **더 큼 + 균일** | Fig 3a,b |

> 📌 **σ(이온전도도) 수치는 이 논문에 명시 안 됨** → "n/a". LPSCl을 σ≈액체급 superionic이라고 정성 기술만. (우리 comp1 AIMD D(600K)=3.09e-6와 직접 대조할 σ 절대값 없음.)
> 📌 **XPS 없음** → "n/a". 이 논문은 분해산물을 **XPS가 아니라 XRD·TEM·EIS**로 추적. (LiCl·sulfate binding energy 등 직접 측정값 없음 → 우리 xps_reference_sei.csv와는 *예측↔간접* 연결만, §7.)
> 📌 P₂S₅·S·LiCl은 **식(1)의 화학식상 산물**이지 분광학으로 검출한 것이 아님 — 구분 필요.

## 4. 재료 & 방법

- **SE 코팅 (핵심 공정)**: **dry coating**, planetary centrifugal mixer. NCM:LPSCl = **100:2 wt%**, 무바인더·무용매. 고원심력 → **무른 LPSCl(E 22.1 GPa)이 NCM 충돌 시 소성변형**해 conformal 코팅 형성 (Fig S1). 잔류 LPSCl 없음 → 코팅두께 ~44 nm 추정.
- **양극복합체**: NCM(or SE-NCM) + LPSCl + 탄소 = **72:27:1 wt%** ball-mill. SE-coated는 코팅분만큼 **추가 SE를 줄여 총 SE량을 bare와 동일하게** 맞춤 (공정한 비교). 450 MPa 압연, 두께 0.19 mm.
- **셀**: NCM | LPSCl(분리막) | **Li–In**. 30 °C, **stack 120 MPa**. 0.1C pre-conditioning 1회 → 0.5C 사이클. **4.25 V vs Li/Li⁺ 충전 → SOC 100 %에서 calendar aging**(고-SOC 저장) → aged 후 0.5C 사이클.
- **특성분석**:
  - **SEM/EDS** (코팅 형상·P/Cl 원소맵, Fig 1a,b)
  - **XRD** (상순도·저장 전후 격자변화, Fig 1c·3a,b)
  - **단면 SEM** (복합체 void/접촉, Fig 1d,e)
  - **OCV 모니터링** (저장 중 self-discharge → 기생반응 정량, Fig 2b)
  - **EIS + 수정 TLM**(modified transmission-line model, Fig S3) → R_int·R_w 분해 (Fig 2c–e)
  - **cross-sectional TEM + FFT** (저장 후 NCM 표면 상전이 layered vs rock-salt, Fig 3c,d)
  - **사이클링** (aged 후 용량유지·CE, Fig 2f,g)
- **이론/DFT**: **없음**. 분해 메커니즘은 **식(1) 화학량론**만 (실험 논문). → 우리 grand-potential이 이 화학을 *계산으로 보강·검증*(§7).

## 5. 결과 — 섹션별 상세

### 5.1 코팅 형상·상순도 (Fig 1a–c)
- SEM/EDS: SE-coated NCM은 **원형 형상 보존**(표면 손상 없음) + **P·Cl 균일 분포** = homogeneous LPSCl 코팅 확인 (Fig 1a,b, Fig S2).
- XRD (Fig 1c): bare·SE-coated 모두 **NCM 특성피크(18.6°, 44.6°)**만. **LPSCl 피크 미검출** (코팅량 2 %로 미소) → 잔류 LPSCl 없음 → 전량 conformal 코팅으로 해석, 두께 **~44 nm** 추정.

### 5.2 복합체 미세구조 — void·접촉 (Fig 1d,e)
- 단면 SEM: **SE-coated가 void 더 작고 적음 + 더 긴밀한 SE/CAM 접촉**. 원인 = **LPSCl 연성(E 22.1 ≪ NCM 175 GPa)**이 압연 시 void를 채우고 인접 catholyte와 밀착 → **계면저항·tortuosity↓**.
- 추가: CAM 입자 *사이* SE가 없어 생기는 단절(red/green 점선)을 conformal 코팅이 보존 → 이온전도 경로 유지.

### 5.3 초기 전기화학 + 저장 중 OCV (Fig 2a,b)
- **Fig 2a (전압 프로파일)**: 0.1C 1회 후 0.5C서 **SE-coated가 더 높은 초기 용량** → void↓·접촉↑로 **CAM 활용도↑**.
- **Fig 2b (저장 OCV)**: 4.25 V 충전→SOC 100 % 저장. **SE-coated의 OCV가 더 빨리 강하 (200 h서 10.1 mV 더 큼)**.
  - 해석: Li–In 음극 전위 고정(0.62 V) → 저장 중 전압강하 = **양극 쪽 self-discharge(=고전압 LPSCl 산화 → 기생반응)**. **더 큰 강하 = SE-coated서 기생반응이 *더 많이/더 균일하게* 일어남.**
  - 🔑 여기서 "기생반응 ↑"가 **나쁜 게 아니라 오히려 양극을 SOC-강하**시켜 좋다는 게 논문 thesis. (ref 15: 이 반응이 CAM의 SOC를 낮춰 구조안정성↑.)

### 5.4 임피던스 (Fig 2c–e, Table S1)
- 저장 중 **3개 시점(point 1,2,3)** EIS → **수정 TLM**(Fig S3) 피팅 → **R_int**(계면), **R_w**(Warburg) 분해.
- **R_int**: SE-coated가 **유의하게 낮음** → 고-에너지 ball-mill로 인한 SE 손상 무시 가능. 저장이 길어지며 둘 다 증가하나 **SE-coated가 후기에 유의하게 낮음**. **point 3(200 h): SE-coated R_int = 4.3 Ω cm²** (bare보다 낮음).
- **R_w**도 동일 경향(SE-coated 후기↓).
- 해석: SE 코팅이 **고-SOC 저장 중 계면열화를 완화**. (단 저항 절대증가는 표면 rock-salt화에 기인 — 5.6.)

### 5.5 aged 후 사이클 (Fig 2f,g)
- 고-SOC 저장 후 0.5C: 용량강하 bare **26.4** vs SE-coated **24.4 mAh/g** (SE-coated 덜 손실).
- **bare 평균 CE 94.2 %**(초기 70 cyc, 낮음=비가역반응↑). **200 cyc 후 용량유지율 격차 = SE-coated가 15.0 % 더 높음** (Fig 2g, **핵심 수명 수치**).
- 용량손실 원인 = **고전압 저장 중 Ni-rich CAM 표면열화의 비가역 반응**.

### 5.6 저장 후 구조분석 — XRD (Fig 3a,b)
- 저장 후 **XRD 피크가 저각으로 이동** = **Li 농도↑ (즉 SOC↓)** → 저장 중 chemical lithiation이 NCM을 재리튬화한 직접 증거. **이 이동이 SE-coated서 더 큼** = 리튬화 더 진행.
- **bare는 (003) 피크 분리(splitting)가 더 뚜렷** = **Li 농도가 입자마다 불균일(heterogeneous)** → 불균일 계면접촉 탓. **SE-coated는 균일**.
- 🔑 = "코팅이 chemical lithiation을 *균일*하게" 의 XRD 증거. (저장 중 SOC 강하 = self-discharge = 기생반응.)

### 5.7 저장 후 구조분석 — TEM/FFT (Fig 3c,d)
- **bare NCM (Fig 3c)**: 표면이 **layered → rock-salt(Fm-3m)로 상전이**, **깊이 침투**. (FFT: Fm-3m → Fm-3m+R-3m → R-3m 변화.)
- **SE-coated NCM (Fig 3d)**: **최외곽만 rock-salt, 내부는 layered 보존**. (얇은 rock-salt 표층.)
- 메커니즘: rock-salt 형성 = **격자 O 손실** → 이것이 **LPSCl 분해를 가속**(O가 SE와 반응) → R_int↑. SE-coated는 표면 rock-salt를 얇게 국한 → O 손실·분해 억제 → Fig 2c 저항추이 설명.

### 5.8 핵심 분해 반응 (식 1)
```
2 Li₆PS₅Cl → P₂S₅ + 5 S + 2 LiCl + 10 e⁻ + 10 Li⁺      (식 1)
```
- 고전압서 LPSCl 산화분해 → **Li⁺ 방출** → SE/NCM 계면 통해 **NCM으로 확산 → Ni-rich CAM 화학적 리튬화**.
- 저자 주: 이 반응이 **CAM의 SOC를 낮춰 구조안정성↑** (ref 15 인용, "이전 보고"). **Li⁺ 이동은 접촉영역에 국한** → conformal 코팅이 **표면 전체에서 균일한 lithiation**을 가능케 함 (낮은 stack pressure서도).
- 🔑 식(1) 산물 = **P₂S₅(폴리설파이드계) + 원소 S + LiCl** — **우리 grand-potential 산화분해 산물과 동일 패밀리**(§7). 단 본 논문은 이것을 *분광검출*이 아니라 *화학량론*으로 제시.

### 5.9 종합 모식도 (Fig 4)
- **bare**: 큰 void·접촉손실(전극레벨) + **불균일 chemical lithiation**(입자레벨) → 응력집중·열화.
- **SE-coated**: 작은 void·긴밀접촉 + **균일 chemical lithiation** → 낮은 저항·낮은 tortuosity + **균질 SOC 강하로 구조안정**.
- 결정성 메시지: "**LPSCl–NCM 조합서 특히 중요** — LPSCl의 낮은 산화안정성이 NCM의 고전압 구조불안정과 겹치는 지점."

## 6. 메커니즘 종합 (the chain)

```
고전압 충전(4.25 V, SOC 100%)
   │
   ▼  NCM 탈리튬 → Ni⁴⁺↑ → 구조불안정 (격자 O 방출 경향, layered→rock-salt)
   │
   ▼  LPSCl 산화분해 [식 1]: 2Li₆PS₅Cl → P₂S₅ + 5S + 2LiCl + 10e⁻ + 10Li⁺   ← "parasitic reaction"
   │
   ▼  방출된 Li⁺ 이 SE/NCM 계면 통해 NCM으로 확산 → NCM **chemical lithiation** (재리튬화)
   │
   ▼  NCM **SOC 강하** (XRD 저각이동으로 검증) = 불안정한 탈리튬 상태에서 빠져나옴
   │
   ├─[bare]  SE 접촉 불균일 → lithiation 국소·불균일 ((003) splitting) → 일부 입자 과리튬화·일부 고-SOC
   │          → rock-salt 깊이 침투 → 격자 O 손실 → LPSCl 분해 가속 → R_int↑ → 수명↓
   │
   └─[SE-coated] conformal 코팅 → **표면 전체 균일 lithiation** → 균질 SOC 강하
              → rock-salt 표층 얇게 국한 → O 손실·분해 억제 → R_int 4.3 Ω cm² (낮음) → **200cyc 유지율 +15.0 %**
```

> **"이로운 기생반응"의 정확한 정의**: 기생반응 자체가 (a) NCM을 균질하게 *재리튬화/SOC-강하* 시켜 고-SOC 구조붕괴를 늦추고, (b) 그 효과는 **반응이 균일할 때만** 순이득 — bare처럼 불균일하면 (003) splitting·국소 rock-salt로 오히려 해롭다. **conformal SE 코팅이 "불균일한 해로운 기생반응"을 "균일한 이로운 기생반응"으로 전환**시키는 것이 논문의 진짜 기여.

## 7. 우리 DFT 대비 (comp1 / modelc / Nd) → `../our_dft_baseline.md`, `db/properties/*`

> ⚠ **방법론 비대칭 먼저**: 이 논문 = **순수 실험**(DFT 0), SE = **Li₆PS₅Cl = 우리 comp1**, Cl-rich(modelc) 없음. 우리 기여 = 이 논문이 *화학량론으로만* 던진 식(1)을 **grand-potential 계산으로 검증·세분화**하고, 분해산물의 **전자절연성(band gap)**을 부여하는 것. 절대값(σ·gap) 직접 대조는 부적절(논문에 수치 없음).

| 항목 | Kang 2025 (exp) | 우리 (DFT) | 일치/차이 + 이유 |
|---|---|---|---|
| **분해 stoichiometry** | 식(1) `2Li₆PS₅Cl→P₂S₅+5S+2LiCl+10e⁻+10Li⁺` (완전산화) | comp1 grand-potential 단계분해: 2.14 V `→Li₃PS₄+LiS4+LiCl+Li`(S²⁻→폴리설파이드) → 2.36 V `→P₂S₇+…` → 3.06 V `→P₂S₇+S(원소)` | **✓✓ 같은 화학 패밀리**. 우리 고전압 종착산물 = **P₂S₇/P₂S₅계 + 원소 S + LiCl** = Kang 식(1) 우변과 일치. 우리는 *전압별 단계*까지 분해(P-S 산화·S elemental 출현 voltage), Kang은 *완전산화 1식*. **우리가 Kang의 식(1)을 voltage-resolved로 검증**. |
| **산화 onset (S-limited)** | "LPSCl 낮은 산화안정성(<~2.5 V 정성)" | comp1 **oxidation onset 2.14 V**(LiS4 포함)/**2.256 V**(제외), S²⁻→폴리설파이드 | **✓ 정합** — Kang의 "low oxidative stability of LPSCl"이 우리 S-limited onset(2.1–2.3 V)과 같은 결. Kang은 정성, 우리는 정량+산물. |
| **Li⁺ 방출 → cathode 리튬화** | self-discharge로 NCM 재리튬화 (OCV·XRD 증거) | 산화분해 = `…+ n Li⁺ + n e⁻` (Li를 *anode reservoir로 방출*) | **✓ 같은 방향** — 우리 grand-potential의 "oxidation = Li 방출(evolution<0)"이 Kang의 "분해→Li⁺→NCM 확산"과 동일 부호. 우리는 Li가 *어디로* 가는지(NCM 격자) 모델 안 함 → Kang이 실험으로 destination 제공. |
| **분해산물 전자물성** | n/a (XPS·gap 측정 없음) | LiCl gap **6.65 eV**(절연), P₂S₇/S/폴리설파이드=전도성(<2 eV) | **△ 보완관계** — Kang 산물 중 LiCl만 wide-gap; P₂S₅·S·폴리설파이드는 전도성 → **이 논문의 산물은 "passivating wide-gap CEI"가 아님**. 이로움은 *passivation*이 아니라 *SOC 강하(균일 lithiation)*. (우리 sei_products.json이 이 산물별 gap을 제공.) |
| **interface reactivity** | 정성(고전압 분해 가속) | comp1 vs LiCoO₂ min dE = **−0.3227 eV/atom**, 산물 `Co₉S₈+Li₃PO₄+Li₂S+LiCl+Li₂SO₄` | **✓ 같은 화학** (sulfate/phosphate/TM-sulfide). 단 우리 LiCoO₂ proxy ≠ Kang NCM811. O가 cathode서 옴(Li₃PO₄ O출처=양극) = Kang "격자 O 손실→분해 가속"의 계산 카운터파트. |
| **Nd-passivation (다른 physics!)** | 해당 없음 (조성·도핑 아님) | Nd3+ 고전압 생존 → NdPO₄(5.55)/NdCl₃(4.30) **wide-gap CEI**; modelc는 전도성 산물만 | **✗ 다른 메커니즘** — Nd 스토리 = "wide-gap *절연* CEI로 e⁻ 차단(passivation)". Kang = "*SOC 강하*(chemical lithiation)". **둘 다 '고전압 cathode 보호'지만 경로가 다름** → over-claim 금지(§12). |
| **무질서/k-mesh 의존성** | n/a (실험) | onset은 S-limited라 조성무관, gap은 PBE 과소·±0.2–0.3 scatter | (방법의존성 플래그는 우리 쪽 — Kang엔 해당없음) |

### 7.1 우리 narrative를 **검증**하는 지점 (강점)
1. **식(1) = 우리 grand-potential 산화분해와 동일 화학** (P₂S₅계+S+LiCl). **같은 그룹 실험**이 우리 계산 산물을 *간접* 뒷받침.
2. **"LPSCl 저-산화안정성 + Ni-rich 고전압 불안정"의 위험 중첩** = 우리가 "고전압 cathode 계면이 황화물 ASSB의 병목" 이라 본 전제를 실험으로 확인.
3. **"고전압 계면반응을 *관리*하면 수명↑"** 상위 프레임 = 우리 Nd-passivation·oxidation-stability 4축 narrative의 동기와 정렬.

### 7.2 우리 DFT가 **메커니즘을 추가**하는 지점
1. Kang의 식(1)은 *완전산화 1식* → 우리가 **전압별 단계(2.14→2.36→3.06→3.33 V)·S²⁻ 우선산화·P-S 후산화·Cl 최후산화**까지 분해 → "왜 S부터, 어느 전압서 무엇이" 를 계산으로 설명.
2. 산물별 **band gap**(LiCl 6.65 절연 / P₂S₇·S 전도성) → **이 논문 산물은 wide-gap 절연막을 *못* 만든다**는 것을 우리가 정량화 → "이로움은 passivation이 아니라 SOC-강하"라는 Kang 해석을 *지지*.
3. **Cl-rich(modelc) 예측**: Kang은 comp1만. 우리 modelc = 같은 onset(2.14 V)·LiCl 2배(1.6 vs 1.0)·방출 Li 적음(0.7 vs 1.75) → **만약 Kang이 Cl-rich로 코팅하면 더 많은 inert LiCl·더 약한 산화extent** 예측 (Zuo 축③와 연결).

## 8. DFT/계산 방법 ★

**없음.** 순수 실험 논문. 유일한 "이론"은 분해 화학량론 **식(1)** 1개. functional·k-points·supercell·AIMD·무질서처리 모두 **n/a**. → 우리 grand-potential·interface_reactivity·sei_product_gaps가 이 화학을 *계산으로 채워 검증·세분화*(§7).

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a,b | SEM/EDS — bare vs SE-coated 형상 + P/Cl 맵 (균일 코팅) | 코팅 형상(균일성)의 시각증거 |
| 1c | XRD — NCM 피크만, LPSCl 미검출(2 %) | 상순도; 코팅량 정량 근거(~44 nm) |
| 1d,e | 복합체 단면 SEM — void·접촉 (SE-coated 우수) | 연성 SE(22.1 GPa)가 void 채움 = "왜 황화물 연성이 이득" |
| 2a | 전압 프로파일(0.5C) — SE-coated 초기용량↑ | CAM 활용도(접촉) |
| **2b** | **저장 OCV — SE-coated 10.1 mV 더 강하** | **기생반응(self-discharge)을 OCV로 정량** = 우리 grand-potential "Li 방출 산화"의 실험 관찰 |
| 2c | Nyquist (3 시점) | TLM 입력 |
| 2d,e | TLM 분해 R_int(4.3)·R_w √t 추이 | 계면열화 속도 정량(SE-coated↓) |
| 2f | aged 후 용량강하 26.4 vs 24.4 | 고-SOC 저장 영향 |
| **2g** | **사이클·CE — 유지율 격차 15.0 %, bare CE 94.2 %** | **핵심 수명 수치** (deck) |
| **3a,b** | **저장 후 XRD — 저각이동(SOC↓)·(003) splitting(bare 불균일)** | **chemical lithiation 균일성의 직접 증거** |
| **3c,d** | **TEM/FFT — bare rock-salt 깊이침투 vs SE-coated 표면국한** | **layered→rock-salt 상전이·O 손실 시각화** |
| 4 | 모식도 — void/접촉 + 균일 vs 불균일 lithiation | 메커니즘 도식(deck) |

## 10. Post-processing ★

- **OCV 모니터링** (저장): 음극 전위 고정(Li–In) → 전압강하 = 양극 self-discharge = 기생반응. 기록 = ΔV(mV) @시간.
- **EIS → 수정 TLM**(Fig S3): 다공성 복합양극 임피던스를 **R_int(계면) + R_w(Warburg/확산)** 로 분해. 3 시점 추이. 기록 = Ω cm²·√t.
- **XRD (저장 전후)**: 피크 시프트 = Li 농도(SOC) 변화; (003) splitting = Li 분포 불균일. 기록 = 2θ 이동·피크분리.
- **TEM + FFT**: 표면 상(layered R-3m vs rock-salt Fm-3m) 식별·rock-salt 침투깊이. 기록 = FFT 패턴·표층두께.
- **SEM/EDS**: 형상·원소맵(코팅 균일성). 단면 = void·접촉.
> **우리 적용**: ① **OCV self-discharge = 기생반응 정량 틀** (우리 grand-potential "Li 방출" 의 실험 proxy). ② **(003) splitting = lithiation 불균일 지표** — 우리가 "균일 vs 불균일 계면반응"을 논할 때 차용. ③ TEM rock-salt 침투깊이 = O 손실·분해 가속의 형태학 지표.

## 11. 적용 인사이트 (deck/paper용, 깊게)

1. **"이로운 기생반응"의 정확한 프레이밍 확정**: *기생반응을 없애는 게 아니라 **균일화**한다*. SE 코팅이 chemical lithiation을 표면 전체에 분배 → 균질 SOC 강하 → 구조보존. 우리 deck "고전압 계면관리" 슬라이드에 **같은 그룹의 실험 사례**로 인용 가능.
2. **우리 grand-potential의 직접 검증**: 식(1)의 P₂S₅계+S+LiCl = 우리 산화분해 산물. "**같은 그룹 실험이 우리 계산 분해화학을 (간접) 확인**." (Zuo가 Cl 함량축에서 한 것을, Kang이 *코팅·SOC축*에서 보강.)
3. **메커니즘 구분(중요)**: Kang "SOC-강하" ≠ Nd "wide-gap 절연 CEI". **둘은 고전압 cathode 보호의 *서로 다른 두 경로*** → 우리 Nd 논문서 "passivation"을 말할 때 Kang을 "passivation 사례"로 잘못 끌어오면 안 됨. 오히려 **상보적**: 코팅(SOC 관리) + 도핑(절연 CEen) = 두 레버.
4. **Cl-rich 확장 예측**: Kang은 comp1만. 우리 modelc(산화 onset 동일·LiCl 2배·산화extent 작음)로 "**Cl-rich SE 코팅이면 더 inert·더 약한 분해**" 예측 → Kang 후속/우리 도핑전략 연결.
5. **공정 정렬**: Kang의 **dry coating**(무용매·scalable) = 우리 그룹 KimCA(SE@CAM dry)·KimICCF와 같은 *건식·계면공정* 계보. "bulk 격자(우리 DFT) ↔ 코팅·계면(실험)" 분업 구도에 한 칸 더.
6. **정직한 한계 명시**: 이 논문 산물(P₂S₅·S·폴리설파이드)은 **전도성** → "분해산물이 passivating CEI" 라는 흔한 서사는 **이 논문엔 부적용**. 이로움은 SOC-강하. 우리가 산물 gap(sei_products.json)으로 이 구분을 *뒷받침*.

## 12. 우리 4축 oxidation narrative & Nd-passivation 와의 정밀 정렬 (over-claim 방지)

> `db/properties/oxidation_stability.json`의 **4축 분류**와 `sei_products.json`의 **Nd passivation**에 이 논문을 정확히 꽂는다.

- **이 논문의 축 = "고전압 cathode 계면 *cycling/calendar* 안정성"** (Zuo의 축③ + Wu의 축④ 사이). **단 변수는 Cl 함량이 아니라 *SE 코팅 유무***. → 4축 표에 "Cl-rich vs Cl-poor"로 넣으면 **틀림**. 별도로 "**계면관리 레버: SE 코팅**"으로 기록.
- **B① intrinsic onset**: Kang "LPSCl 저-산화안정성" = 우리 S-limited 2.14 V와 정합(정성). Kang은 onset을 *비교*하지 않음(코팅 유무는 onset 안 바꿈) → 축① 무관.
- **B③ cathode 계면 cycling**: Kang의 R_int↓·유지율 +15 % = 우리 "고전압 계면 관리가 수명 좌우" 와 같은 축. Zuo(Cl산물 질)와 **병렬**: Zuo=*산물의 질*(gas/polysulfide↑·solid sulfate↓), Kang=*반응의 균일성*(homogeneous lithiation). **둘 다 "계면반응의 *질/분포*가 *양*보다 중요"** 라는 공통 교훈.
- **Nd-passivation 과의 구분 (sei_products.json)**:
  | | Kang 2025 (이 논문) | 우리 Nd 스토리 |
  |---|---|---|
  | 보호 경로 | NCM **SOC 강하**(chemical lithiation 균일화) | **wide-gap 절연 CEI**(NdPO₄/NdCl₃/Li₃PO₄)로 e⁻ 차단 |
  | 핵심 산물 | P₂S₅·S·LiCl (LiCl만 절연) | NdPO₄(5.55)·NdCl₃(4.30)·Li₃PO₄(5.73) 절연 |
  | 레버 | **양극 표면 SE 코팅**(공정) | **SE 격자 도핑**(Nd+O) |
  | 물리 | 열역학적 SOC 이동 + kinetics(균일성) | 산물 *전자구조*(절연) → kinetic passivation |
  | 공통 | **고전압 Ni-rich cathode를 보호** / 같은 grand-potential 분해화학 출발 | 동일 |
  → **"같은 목표·다른 메커니즘".** deck에서 둘을 묶을 땐 "**코팅(SOC 관리) + 도핑(절연 CEI) = 상보적 두 레버**"로. "Kang = Nd passivation의 실험 증거" 라고 **하면 안 됨**(physics 다름).
- **XPS 연결 (xps_reference_sei.csv)**: Kang은 **XPS 없음**. 만약 후속이 식(1) 산물을 XPS로 본다면 우리 anchor와 대조 가능: **LiCl Cl 2p₃/₂ 198.6 eV**, **원소 S/폴리설파이드 S 2p ~163–164**(우리 표엔 host 161.6·sulfate 168.0·Li₂S 160.2가 anchor), **sulfate S 2p₃/₂ 168.0**(O 관여 시). 단 **현재 논문엔 이 peak들이 측정되지 않음** → "예측↔미래검증" 연결만, 현 시점 매칭 주장 불가.

## 13. 인용 가능 문장 (deck/paper용)

- "Kang et al. (우리 그룹, ChemComm 2025) show the *parasitic* LPSCl oxidation [식 1: 2Li₆PS₅Cl→P₂S₅+5S+2LiCl+10e⁻+10Li⁺] is **beneficial when homogenized** by a conformal SE coating: the released Li⁺ re-lithiates the delithiated Ni-rich NCM uniformly, lowering its SOC and suppressing the layered→rock-salt transition (200-cyc retention +15.0 %)."
- "Their decomposition stoichiometry (식 1) matches our grand-potential oxidation products (P₂S₇/P₂S₅-type + elemental S + LiCl), cross-validating our computed chemistry with the same group's experiment."
- "Crucially the benefit is **SOC-lowering (chemical lithiation), not a passivating wide-gap CEI** — distinct physics from our Nd³⁺ → NdPO₄/NdCl₃ electron-blocking passivation; the two are complementary cathode-protection levers (coating vs doping)."
- "The (003) peak splitting (heterogeneous Li in bare NCM) vs uniform shift (SE-coated) is the direct evidence that the SE coating *distributes* the parasitic reaction over the whole particle surface."

## 14. 주의 / 한계 (over-claim 방지)

- **메커니즘 혼동 금지**: 이로움 = **균일 chemical lithiation(SOC↓)**, *not* passivating CEI. 분해산물(P₂S₅·S·폴리설파이드)은 대부분 **전도성**(LiCl만 절연) → "분해→passivation" 서사 부적용. ↔ 우리 Nd(절연 CEI)와 **다른 physics**.
- **Kang ≠ Zuo**: 동일 화학(LPSCl/Ni-rich)이나 **변수가 다름** — Zuo=Cl 함량, Kang=SE 코팅 유무. 4축 표에 Cl축으로 넣지 말 것.
- **DFT 없음·정량 σ/gap/XPS 없음**: σ·band gap·binding energy 절대값 **이 논문에 없음**(n/a). 우리 수치와 *절대 대조* 불가; 화학·프레임 정렬만.
- **식(1)은 화학량론**: P₂S₅·S·LiCl은 *식상* 산물이지 분광검출 아님 (XRD·TEM·EIS만 측정).
- **전압기준 혼용**: 셀 = Li–In(0.62 V). "4.25 V"·"high SOC"는 vs Li/Li⁺. self-discharge 해석은 음극 전위 고정 가정에 의존.
- **NCM811 특정**: 효과는 Ni-rich(격자 O 방출) 특유 — LCO 등 안정 cathode면 기생반응 이득 작아질 수 있음 (cf. Wu: LCO가 NCM811보다 안정).
- **proxy 한계(우리 쪽)**: 우리 interface_reactivity는 LiCoO₂ proxy·solid-hull(기체상 없음) → Kang NCM811·O 방출 동역학과 1:1 아님.
- **"우리 그룹" 태그**: 안용훈 그룹 계보(Jong-Won Lee, 한양대). KimICCF/KimCA와 동일 — bulk DFT(우리)와 *분업* 관계, 격자 도핑 논문 아님.

## 15. 기법 용어 미니사전

- **Parasitic reaction (기생반응)**: 의도한 충방전 외에 일어나는 부반응. 여기선 고전압서 **LPSCl 산화분해 → Li⁺ 방출 → NCM 화학적 리튬화**. 보통 해롭지만, *균일하면* SOC를 낮춰 이로움.
- **Chemical lithiation (화학적 리튬화)**: 외부 전류 없이 **화학적으로**(여기선 SE 분해 Li⁺이) 양극에 Li가 삽입되는 것. = self-discharge의 화학적 표현. NCM SOC↓.
- **High-SOC calendar aging**: 충전 상태(SOC 100 %)로 **방치 저장**하며 열화 관찰. 사이클이 아닌 *시간* 변수.
- **Self-discharge / OCV decay**: 저장 중 전압 자연강하 = 내부 부반응(기생반응)의 척도. Li–In 음극 고정 → 강하 = 양극 쪽.
- **Layered → rock-salt 상전이**: Ni-rich NCM이 고전압서 **격자 O 손실**하며 층상(R-3m)→암염(Fm-3m, 전기화학 비활성)으로 변함 = 비가역 용량손실·저항원.
- **(003) peak splitting**: XRD (003) 반사가 갈라짐 = 입자마다 Li 농도(SOC) **불균일**.
- **TLM (transmission-line model)**: 다공성 복합전극 임피던스를 계면(R_int)·확산(R_w)·이온/전자 경로로 분해.
- **Dry coating (건식 코팅)**: 무용매·무바인더, 기계적 충돌로 코팅. scalable·친환경 (vs wet/용매).
- **Conformal coating**: 입자 표면을 균일·연속으로 덮는 코팅 → 균일 계면반응의 전제.
- **Ni-rich CAM**: 고-Ni 양극활물질(NCM811). 고용량이나 고전압 구조불안정.

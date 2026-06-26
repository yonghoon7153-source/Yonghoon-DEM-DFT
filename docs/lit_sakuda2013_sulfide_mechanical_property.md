# 황화물 SE의 "유리한 기계적 물성" — 상온 가압소결·Young's modulus·이온전도도 — Sakuda (Sci. Rep. 2013)

> slug `sakuda2013_sulfide_mechanical_property` · DOI `10.1038/srep02261` · type `exp` (압축시험 + 초음파 E + EIS + 셀) ·
> PDF `48827b6a-05._Sulfide_Solid_Electrolyte_with_Favorable_Mechanical_Property_for_AllSolidState_Lithium_Battery.pdf` ·
> digested `2026-06-26` · status ✅ (본문 5쪽 전체; SI = Supplementary Fig S1–S3은 PDF에 미첨부 — 본문 인용만 존재)
>
> ★ **이 논문은 우리의 두 가지 토대 앵커의 원전(原典)이다:**
> (1) "황화물 SE는 **상온 냉간가압만으로 치밀화**(room-temperature pressure sintering)" — 우리 cold-press @300 MPa +
>     MPM 소성 void-fill 의 물리적 근거.
> (2) **황화물 유리의 Young's modulus ≈ 18–25 GPa** (75Li₂S·25P₂S₅ = **24 GPa**) — 우리 real-bulk E_SE ≈ 22–24 GPa
>     앵커의 원전. 우리 E_eff 1.35(DEM)/1.53(MPM)은 이 24 GPa의 *연화된 프록시*.
>
> ⚠⚠ **PROVENANCE 핵심 정정 (먼저 읽을 것):** 우리가 인용해 온 "**87 % 상대밀도 @ 300 MPa (= porosity 13 %)**"는
> **이 논문 본문에 stated 되어 있지 않다.** 본문이 명시하는 밀도 앵커는 "**relative density가 350 MPa 초과 압력에서 90 %를
> 넘는다(exceeds 90 % at over 350 MPa)**" 뿐이다. "87 % @ 300 MPa"는 **Fig 2a 곡선에서 눈으로 읽은(digitized) 추세값**으로,
> ±몇 %p 오차의 **추세(TREND)** 일 뿐 정밀 stated 값이 아니다. + 소재는 **75Li₂S·25P₂S₅ glass** (Li₃PS₄ 조성의 *유리*,
> glass-ceramic 아님), **우리 LPSCl argyrodite(Li₆PS₅Cl) 아님.** 자세한 판정은 §11.

---

## 1. 한 줄 요약
황화물 유리 SE(Li₂S–P₂S₅ 계, 대표 75Li₂S·25P₂S₅)가 **상온 냉간가압만으로** 산화물(LLZO)과 달리 치밀한 펠릿이 되고
(Fig 2a: 압력↑ → 상대밀도↑, >350 MPa서 >90 %), 그 **Young's modulus가 18–25 GPa** (산화물 ~50 GPa과 유기폴리머 사이의
"중간값")로 **계면응력 완화에 유리**함을 처음으로 정량 제시한 황화물-기계물성의 고전. 치밀화 기구를 "room-temperature
pressure sintering"(Li⁺·PS₄³⁻ 이온이 입계로 확산·회전)으로 명명하고, 이것이 우리 DEM/MPM 냉간압밀·소성흐름 모델링의 물리적 토대.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **A. Sakuda, A. Hayashi, M. Tatsumisago** (Osaka Prefecture University, Dept. Applied Chemistry; 제1저자 현 AIST) | **Sci. Rep. 3, 2261 (2013)**, OPEN (CC BY-NC-ND 3.0) | 10.1038/srep02261 | **Li₂S–P₂S₅ glass SE** (xLi₂S·(100−x)P₂S₅, x=50–80; 대표 **75Li₂S·25P₂S₅** = Li₃PS₄ 조성 *유리*) + 비교용 산화물 **Li₇La₃Zr₂O₁₂ (LLZO)**; 셀 CAM = **LiCoO₂**, 음극 graphite | **실험**: 압축시험(밀도-압력) + 초음파 펄스 E + EIS(σ-압력) + 단면 SEM + ASSB 셀. 시뮬레이션 없음 |
| 접수/게재 | 2013-03-27 접수 / 2013-07-23 게재 | | ⚠ **NOT LPSCl, NOT NMC** | |

## 3. 핵심 물성 (수치) — 전부 추출
| 물성 | 값 | 조건 (P, 소재) | stated/digitized | 비고 |
|---|---|---|---|---|
| ★ 상대밀도 vs 압력 (본문 stated) | **"exceeds 90 % at over 350 MPa"** | 75Li₂S·25P₂S₅ glass, 상온 단축압축, 10 mm 몰드, 500 mg | **stated (본문)** | **유일한 stated 밀도 앵커**; "thus … remarkably high relative density … without heat treatment" |
| ★ 상대밀도 @ 300 MPa | **≈ 85–88 % (≈87 %)** → porosity **≈ 12–15 %** | 동상 (Fig 2a 곡선 읽음) | **digitized (Fig 2a)** ⚠ **추세만** | **본문에 300 MPa 정밀값 없음**; 곡선이 ~80 %대 plateau에서 350+서 90 % 교차 |
| 상대밀도 vs 압력 (Fig 2a 곡선 전체) | ~0 MPa near 0 → ~30 %(저압) → ~50 %(~30 MPa) → ~60–65 %(~75 MPa) → ~75 %(~150) → ~80 %(~200) → ~85–88 %(~300) → ~90 %(~350) → ~93–95 %(~450) | 동상 | **digitized** | 전형적 가압 치밀화 곡선(저압 급상승→고압 수확체감), Heckel류 |
| 상대밀도 기준 밀도(분모) | **ρ_glass = 1.88 g/cm³** | 75Li₂S·25P₂S₅ 투명유리(~200 ℃ 열간프레스, Ref 9) | **stated** | rel.density = ρ_coldpress / ρ_glass(완전치밀 유리 근사) |
| ★ Young's modulus (범위) | **18–25 GPa** | xLi₂S·(100−x)P₂S₅ glass, x=50–80 mol% | **stated** | Li₂S 함량↑ → E↑; **산화물(~50 GPa)과 유기폴리머 사이 "중간값"** |
| ★ E (75Li₂S·25P₂S₅) | **24 GPa** | Li 티오포스페이트 유리(우리 LPSCl과 같은 sulfide계) | **stated (본문)** | ★ **우리 real-bulk E_SE 24 의 원전** |
| E (50Li₂S·50P₂S₅) | **18 GPa** | sulfide glass | **stated** | cf. 50Li₂O·50P₂O₅ 산화물 = **50 GPa** (≈1/3) |
| E (75Na₂S·25P₂S₅) | **18 GPa** | Na 티오포스페이트 유리 | **stated** | Na(큰 이온반경) < Li(24) — 큰 이온 → E↓ |
| Young's modulus (Fig 5 점들) | **~17.5 / ~22 / ~23.5 / ~25 GPa** @ Li₂S **50 / 70 / 72 / 80 mol%** | hot-press 고밀도 펠릿, 각 Tg서 | **digitized (Fig 5)** | 4점 단조증가; 25 GPa(x=80)이 최고 |
| E 측정법 | **초음파 펄스(ultrasonic pulse) 법** | Tg서 열간프레스한 *고밀도 펠릿*(공극영향 배제) | **stated (Methods, Ref 15 McSkimin)** | 시료 10 mm φ × 수 mm, dry Ar |
| ★ 이온전도도 (75Li₂S·25P₂S₅, 냉간프레스) | **3.1 × 10⁻⁴ S/cm = 0.31 mS/cm** @ **360 MPa**, 상온 | 냉간프레스 펠릿 | **stated (본문)** | bulk(열간프레스) **3.4 × 10⁻⁴ = 0.34 mS/cm**에 근접 |
| σ vs 압력 (Fig 4) | ~10⁻⁵서 시작 → **70 MPa서 ~10⁻⁴로 급상승** → 360 MPa서 3.1 × 10⁻⁴로 점진 | 75Li₂S·25P₂S₅, 상온 EIS | **digitized + stated** | "increases dramatically to 10⁻⁴ at 70 MPa then gradually" — σ-vs-P가 밀도-vs-P와 같은 형태 |
| bulk σ (열간프레스, 점선) | **3.4 × 10⁻⁴ S/cm** | hot-pressed 투명 펠릿 | **stated** | Fig 4 점선 기준 |
| LLZO(산화물) σ (냉간프레스) | "측정 어려울 만큼 낮음(GB저항 매우 큼)" | Li₇La₃Zr₂O₁₂, 상온 가압 | **stated (정성)** | 황화물과 대비 — 산화물은 1000 ℃+ 소결 필요 |
| ASSB 셀 용량 | **133 mAh g⁻¹** | LiCoO₂(SE-코팅) / graphite / Li₂S–P₂S₅, 11 mA g⁻¹, 360 MPa 셀 | **stated** | "relatively good cycle performance"(SI Fig S3) |
| 셀 시험 조건 | 0.13 mA cm⁻² (≈11 mA g⁻¹), 2.8–4.6 V, 상온, Ar | 셀 = 360 MPa 가압 3층 펠릿 | **stated (Methods)** | 양극=PLD로 80Li₂S·20P₂S₅ 코팅한 LiCoO₂ |
| PSD (입자크기) | 유리 분말 **수~수십 µm** ("several to ten micrometers") | 75Li₂S·25P₂S₅ glass powder | **stated (정성)** | D10/D50/D90 수치 **없음** — 정성만 |
| porosity / coverage / Z / Heckel P_y | **n/a** | — | — | 이 논문은 porosity·coordination·coverage·Heckel **수치 안 줌**(밀도 곡선만) |

## 4. 시뮬레이션 방법 ★
**시뮬레이션 없음 — 순수 실험 논문.** (우리 DEM/MPM의 frame[4] **외부 실험 앵커** + 물리 토대.) 실험 방법:
- **분말 제조**: Li₂S–P₂S₅, Na₂S–P₂S₅ 유리를 **유성볼밀**(Fritsch P7, ZrO₂ 45 mL 용기 + 500개 4 mmφ ZrO₂ 볼, 510 rpm, 10 h)
  = mechanochemical milling. 75Na₂S·25P₂S₅는 Na₂S(Nagao)로 별도 제조. 전 과정 dry Ar.
- **압밀(밀도-압력 곡선)**: 상온 **단축 냉간프레스** 또는 ~200 ℃ 열간프레스, **10 mm φ 몰드**, 75Li₂S·25P₂S₅ **500 mg**.
  bulk(분모) 밀도 = 측정 어려워 *유리 결정 추정밀도 ≈ 열간프레스 펠릿 밀도*로 잡고, rel.density = ρ_coldpress / ρ_hotpress.
- **E 측정**: **초음파 펄스법**(McSkimin Ref 15), Tg서 열간프레스한 **고밀도 펠릿**(공극 영향 제거) 10 mmφ × 수 mm, dry Ar.
  (Japan Fine Ceramics Center 기술지원.)
- **σ 측정**: 임피던스 분석기(Solartron 147055BEC), 10 Hz–1 MHz, ~10 mV, dry Ar.
- **셀**: LiCoO₂(D10, Toda Kogyo) + 80Li₂S·20P₂S₅ + graphite(Timrex SLP50). 양극 = **PLD로 80Li₂S·20P₂S₅ 박막을 LiCoO₂에 코팅**
  (Ref 14). 무탄소 양극(80:20), 음극 90:10. 3층을 **360 MPa**로 가압한 펠릿, dry Ar 글러브박스.
- **단면 SEM**: Ar 이온밀링(E-3500, Hitachi)으로 매끈 단면 또는 파단면; 시료는 inert로 봉인 후 노출.
- **입자 처리** ★ (우리 DEM판 "무질서 처리"에 해당하는 항목): **해당 없음(실험).** 단, *물리적 결론*이 우리 모델의
  입자 처리와 직결 — Sakuda는 입자가 가압 시 **"서로 자라나 입자크기 증가, 입계·공극 감소"**(Fig 2c→2d, Fig 3)를 SEM으로
  관찰. 이는 **rigid-sphere가 아니라 진짜 SHAPE 소성/유합(coalescence)** 임을 보여줌 → 우리 **MPM 소성 void-fill / SEM
  코어보존+경계평탄화** morphology가 모사하려는 *바로 그 현상*. (우리 DEM 강체 구는 이를 못 잡아 18× 연화 프록시로 럼핑.)

## 5. Figure set ★ (각 그림 수치와 함께)
| Fig | 내용 (무엇을 보여주나) | 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1** | 상온 펠릿화한 **산화물 LLZO**(a) vs **황화물 80Li₂S·20P₂S₅ glass**(b) 파단면 SEM 대비 | 둘 다 20 µm scale; LLZO는 입자 간 공극·각진 입계 뚜렷, 황화물은 상대적으로 치밀 | **산화물=가압만으로 안 치밀(소결 필요) / 황화물=가압만으로 치밀** — 우리 cold-press 가정의 시각적 근거 |
| **2a** | ★ **75Li₂S·25P₂S₅ glass 상대밀도 vs 몰딩 압력** (핵심 앵커 그림) | x축 0–500 MPa, y축 0–100 %; ~30 %(저압)→~50 %(~30)→~65 %(~75)→~80 %(~200)→**~87 %(~300, 읽음)**→**>90 %(>350, stated)**→~95 %(~450) | ★ **우리 "87 %@300 / >90 %@350" 앵커의 원천 곡선** — 단 300값은 digitized(추세), 350+ 90 %만 stated |
| **2b/c/d** | 75Li₂S·25P₂S₅ glass 분말 SEM: **가압 전(b)** / **74 MPa(c)** / **360 MPa(d)** 파단면 | 입자 수~수십 µm; **압력↑ → 입자크기 증가**(유합) | **가압이 입자를 *물리적으로 합친다*(SHAPE 변화)** = 우리 MPM void-fill / 강체 구 한계의 시각 증거 |
| **3a/b** | **80Li₂S·20P₂S₅ glass, 360 MPa 냉간프레스** 매끈 단면(이온밀링) @ **25 ℃(a)** vs **200 ℃(b)** | "**입계 거의 안 보임**(grain boundaries hardly visible), 입자 유합, 공극 매우 적음"; inset = 펠릿 사진(투명) | **상온 가압만으로 입계가 사라질 만큼 치밀** — "room-temperature pressure sintering" 직접 증거; 200 ℃(≈Tg)는 더 치밀(투명) |
| **4** | ★ **75Li₂S·25P₂S₅ σ vs 몰딩 압력** | ~10⁻⁵서 시작 → **70 MPa서 ~10⁻⁴로 급상승** → 360 MPa서 **3.1 × 10⁻⁴**; 점선 = 열간프레스 bulk **3.4 × 10⁻⁴** | ★ **σ-vs-P가 밀도-vs-P와 같은 무릎 형태**(저압 급상승→고압 포화) = 우리 Heckel knee / Bazzoun σ-포화@400 / Doux 접촉포화@~25 MPa 와 같은 계열 |
| **5** | ★ **Li₂S–P₂S₅ glass Young's modulus vs Li₂S 함량** | x축 30–100 mol% Li₂S, y축 0–30 GPa; **4점 ~17.5/~22/~23.5/~25 GPa @ x=50/70/72/80**; 본문: 50→18, 75→**24**, Na 75→18 | ★ **우리 real-bulk E_SE 24 의 원천** + "Li₂S↑→E↑" 추세 + 산화물(50) 대비 ~½ |
| **6a** | 복합 양극 모식: SE-코팅 전극입자 | 회색=전극입자, 노랑=SE 코팅; 부피변화 시 SE가 *버퍼*로 균열억제 | 우리 CBD/계면 morphology 개념(SE가 AM을 감싸 응력완화) |
| **6b** | **LiCoO₂ + 80Li₂S·20P₂S₅ PLD코팅** 양극 단면 SEM | "매우 치밀, 공극 거의 없음", SE가 LiCoO₂와 밀착 | SE-코팅 = 계면접촉↑ = 우리 coverage 개념의 정성 근거 |
| **6c** | 셀 충방전 곡선(LiCoO₂/graphite/Li₂S–P₂S₅, 11 mA g⁻¹) | **133 mAh g⁻¹**, 1–5 V 영역 | 황화물 SE 셀이 상온 가압 제작만으로 동작 — 우리 소재계 동작성 |

## 6. Post-processing ★
- **무엇**: (1) **상대밀도** = ρ_coldpress / ρ_glass(완전치밀 근사, ρ_glass=1.88 g/cm³) vs 압력 — *Heckel·porosity convention*의
  실험판(공극 = 1 − rel.density). (2) **초음파 펄스 E** (McSkimin). (3) **EIS σ** (Nyquist → bulk σ). (4) **Raman**(SI S1: 가압
  전후 국소환경 거의 불변) + **XRD**(SI S2: 가압 후 비정질 유지 = 저온 소결, Tg보다 훨씬 낮은 온도서 치밀화). (5) **단면 SEM**(이온밀링).
- **도구**: Fritsch P7 볼밀, Solartron 147055BEC, 초음파 장비(JFCC), Hitachi E-3500 이온밀, PLD(양극 코팅).
- **수치화·플롯**: 밀도-vs-P / σ-vs-P / E-vs-Li₂S% 3개 곡선. **porosity·coordination·coverage·tortuosity·Heckel-fit 수치 없음**
  (우리가 이 논문에서 가져올 수 있는 *직접* 수치는 **밀도-vs-P 곡선 + E 18–25/24 + σ 0.31/0.34 mS/cm** 뿐).

## 7. 핵심 메커니즘·논증 흐름 (논문 전체 서사 — paper-level)
1. **문제**: ASSB는 안전하나, SE의 *이온전도도*뿐 아니라 *기계물성*(탄성률·치밀화 거동)이 실용성에 결정적인데 그간 황화물의
   기계물성이 정량화 안 됨(측정 어려움 — 대기 불안정 → inert 취급 필요).
2. **현상**: 황화물 Li₂S–P₂S₅ glass는 **상온 냉간가압만으로** 치밀 펠릿이 됨(Fig 1·2). 산화물 LLZO는 1000 ℃+ 소결 필요. →
   저자들이 이를 **"room-temperature pressure sintering(상온 가압소결)"**으로 명명.
3. **치밀화 기구**: 가압 시 **Li⁺와 PS₄³⁻ 이온이 입계로 확산·회전**하여 인접입자가 유합(coalesce) → 입계·공극 감소(Fig 2b→d,
   Fig 3 입계 소멸). XRD(가압 후 비정질 유지)·Raman(국소환경 불변)이 *상전이가 아닌* 물리적 치밀화임을 확인.
4. **왜 황화물만 되나(결합에너지 논증)**: Li–S 결합에너지 < Li–O → 결합이 약하고 **공유결합성(covalent)**이 강함 → 정전반발↓ →
   응력 하에 Li⁺·PS₄³⁻가 **회전·확산하기 쉬움**(small-scale plasticity) → 상온 소결 가능. 유리구조(큰 자유부피, 낮은 Tg)도 유리.
5. **탄성률(Fig 5)**: 황화물 E = **18–25 GPa**, 산화물(~50)의 절반·유기폴리머보다 높은 **중간값**. 이것이 ASSB에 **유리**한 이유 —
   너무 단단하면(산화물) 충방전 부피변화 시 SE가 균열을 못 메워 응력집중·파단; 너무 무르면 구조유지 실패. **중간 E = 부피변화에
   탄성적으로 대응 + 계면접촉 유지**. (Li₂S↑→E↑; 큰 이온 Na→E↓.)
6. **이온전도도(Fig 4)**: 냉간프레스 σ = 3.1 × 10⁻⁴ S/cm @360 MPa, 열간프레스 bulk(3.4 × 10⁻⁴)에 근접 = **상온 가압만으로 거의
   bulk 수준 전도** 달성. σ-vs-P가 밀도-vs-P와 같은 무릎(70 MPa서 급상승→포화) = **밀도(접촉)↑가 σ↑를 견인**.
7. **응용(Fig 6)**: SE-코팅 복합양극(PLD) → 계면 밀착 → 상온 가압 제작 셀이 133 mAh g⁻¹ 동작. SE가 부피변화 *버퍼*.
8. **결론**: 황화물 SE = 높은 σ + (낮은 결합E·유리구조 덕의) **상온 가공성** + **중간 E** → ASSB에 이상적.

## 8. 기술 미니용어집
- **Room-temperature pressure sintering(상온 가압소결)**: 가열 없이 가압만으로 입자가 유합·치밀화하는 현상(이 논문 명명). 이온
  확산/회전이 입계서 일어나 입계·공극 감소. = 우리 cold-press @300 MPa 의 물리 명칭.
- **Relative density(상대밀도)**: ρ_실측 / ρ_완전치밀. = 1 − porosity. 이 논문은 ρ_glass=1.88로 정규화.
- **초음파 펄스법(ultrasonic pulse method)**: 종/횡파 음속 → 탄성계수. 공극이 음속을 왜곡하므로 **고밀도(열간프레스) 시료**서 측정.
- **Small-scale plasticity(소규모 소성)**: 약한 결합·공유성 덕에 응력 하에 이온이 국소적으로 재배열 → 황화물의 "무름". = 우리
  σ_y 0.05–0.30 GPa(soft sulfide) / E_eff 연화의 물리 근원.
- **글래스 vs 글래스세라믹**: 이 논문 밀도/σ는 **glass**(비정질). glass-ceramic(결정화)은 별개 — 여기 밀도-vs-P는 *유리* 기준.

## 9. 우리 DEM+MPM 대비 → `our_dem_baseline.md`
| 항목 | 이 논문 (Sakuda 2013) | 우리 | 차이 / 이유 (same-family vs LPSCl / 실험 vs 모델) |
|---|---|---|---|
| **밀도-vs-P 앵커** | "**>90 % @ >350 MPa**" (stated) + ~87 %@300(digitized 추세) | DEM pure-SE ~10 % porosity(=90 %) @300; real_14 15.6 % | **같은 황화물-유리 family 거동(가압 치밀화)**; 단 소재·압력 조건 다름 → §11 판정 |
| **E_SE** | **18–25 GPa**, 75Li₂S·25P₂S₅ = **24 GPa** (초음파, stated) | real-bulk **22–24** / E_eff **1.35**(DEM)·**1.53**(MPM) | ★ **우리 real 24의 원전.** 1.35/1.53 = 이 24의 *연화 프록시*(granular 재배열 럼핑) — Sakuda가 real E가 뻣뻣함을 *측정*으로 확정 |
| **냉간 치밀화 물리** | "상온 가압소결"(이온 확산·유합, Fig 2·3 입계소멸) | DEM cold-press @300 + MPM 소성 void-fill·morphology | ★ **우리 모델 전제의 실험 토대.** Sakuda SEM(입자 유합)= 우리 MPM SHAPE 소성이 모사하려는 현상 |
| **입자 거동** | 가압 시 입자 *유합·성장*(SHAPE 변화, SEM) | DEM=강체 구(형상 불변, δ 프록시) / MPM=진짜 SHAPE 소성 | **Sakuda는 진짜 SHAPE 변화를 관찰** → 우리 강체-구 DEM 한계를 *실험이 직접 지적* → MPM이 메우는 것이 옳음(frame[5]) |
| **σ** | 냉간 0.31 / bulk 0.34 mS/cm (75Li₂S·25P₂S₅) | σ_grain **3.0 mS/cm**(Cronau LPSCl 단결정) | **소재가 다름**: Li₃PS₄ glass σ(~0.3) ≪ LPSCl(~1–3) — σ는 argyrodite가 ~10× 높음. **σ 절대값 전이 금지**, σ-vs-P *형태*만 |
| **σ-vs-P 형태** | 70 MPa 급상승→포화(Fig 4) | Heckel knee P_y 138; Bazzoun σ-포화@400; Doux 접촉@~25 MPa | **같은 계열**(접촉↑→σ↑→수확체감) — frame[4] 추세 교차검증 |
| **porosity floor / Heckel 수치** | n/a (밀도곡선만, fit·floor 수치 없음) | rigid-sphere floor ~20 %; Heckel R²0.965 | Sakuda는 fit 안 함 — 곡선 자체가 우리 Heckel/DPC 타깃 *형태* 제공 |

## 10. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **E_SE 24 GPa의 1차 출처로 인용**: 우리 "real-bulk E_SE ≈ 22–24 GPa, E_eff 1.35/1.53은 연화 프록시" 서사의 **literature
  origin**. Sakuda(24, 초음파 측정) + Bazzoun(22.1, LPSCl)이 우리 24를 양쪽에서 고정. "E_eff는 임의가 아니라 *측정된* 24의
  연화"라는 frame[2] 논거를 **measurement로 뒷받침**.
- ② ★ **"황화물은 상온 가압만으로 치밀화"의 1차 출처**: 우리 DEM cold-press @300 + MPM 소성 void-fill 전제의 **물리적
  정당화**(산화물처럼 소결 불필요). Fig 2·3(입자 유합·입계소멸 SEM) = 우리 MPM morphology(코어보존+경계평탄화)가 모사하는
  바로 그 현상의 실험 증거 → MPM이 frame[5]의 "역학/morphology 절반"을 정당하게 소유.
- ③ **밀도-vs-P 곡선을 우리 Heckel/DPC 타깃 *형태*로**: Fig 2a(저압 급상승→고압 포화)는 우리 Heckel `ln(1/(1−D))=K·P+A` /
  homogenized-REV DPC가 재현해야 할 곡선 형태. 단 **소재가 Li₃PS₄ glass라 절대 porosity는 LPSCl과 다름** → *형태/추세*만
  (`docs/data/densification_porosity_db.csv`에 same-family 데이터점으로 추가, precision=trend_digitized).
- ④ **σ-vs-P 무릎**: Fig 4(70 MPa 급상승→포화)를 Bazzoun(σ@400 포화)·우리 P_y 138 과 같은 계열로 묶어 "압력↑→접촉↑→σ↑→
  수확체감"의 소재-일반성 증거로.

## 11. ★ DENSITY / E-MODULUS ANCHOR-PROVENANCE 판정 (먼저 봐야 할 §)
**A. "87 % 상대밀도 @ 300 MPa (= porosity 13 %)" — 부분 정정.**
- 본 논문 PDF 본문에 **stated 되어 있는 밀도 앵커는 단 하나**: *"The relative density … exceeds 90 % when the 75Li₂S·25P₂S₅
  glass powder is compressed by a pressure of **over 350 MPa**."* (p.2). → **stated = ">90 % @ >350 MPa"** (porosity <10 %).
- **"87 % @ 300 MPa"는 본문에 없다.** Fig 2a 곡선을 **눈으로 읽은(digitized) 추세값**이며, 300 MPa 지점은 곡선상 대략 **85–88 %**
  (porosity ≈ 12–15 %)에 해당. ±몇 %p 오차의 **TREND** 로만 인용 가능, **stated 정밀값으로 인용 금지.**
- **소재 확정**: 밀도-vs-P 곡선(Fig 2a)의 소재 = **75Li₂S·25P₂S₅ (mol%) glass** (= Li₃PS₄ 조성의 *유리*, glass-ceramic 아님).
  단면 SEM(Fig 3)은 **80Li₂S·20P₂S₅ glass**. **둘 다 우리 LPSCl argyrodite(Li₆PS₅Cl) 아님.**
- **압력 확정**: 곡선 x축 0–500 MPa, 본문 명시 압력 = **350 MPa(>90 %), 360 MPa(σ·셀), 74 MPa(SEM), 70 MPa(σ 급상승)**.
  **300 MPa는 본문에 특정값으로 등장하지 않음.**
- ⇒ **판정**: 우리 "87 %@300 (porosity 13 %)"는 **이 논문 Fig 2a에서 digitized 한 추세값이며, stated 앵커는 ">90 %@>350 MPa"**.
  Minnmann/Trevisanello provenance 엄밀성과 동일하게: **"Sakuda 2013 Fig 2a (75Li₂S·25P₂S₅ glass, digitized): rel.density ~87 %
  @ ~300 MPa (TREND); stated: >90 % @ >350 MPa"** 로 표기. (우리 DEM pure-SE 90 %는 **>350 MPa stated 와 정합** — 300 MPa
  digitized 87 %와도 추세 일치하나, *압력이 다름*에 주의.)

**B. Young's modulus ~20 GPa — 확정(stated).**
- **18–25 GPa** (초음파, x=50–80 mol% Li₂S) **stated**, **75Li₂S·25P₂S₅ = 24 GPa stated**, 50Li₂S·50P₂S₅ = 18 stated,
  산화물 50Li₂O·50P₂O₅ = 50 GPa. → ★ **"sulfide E ~18–25 GPa, 우리 real 24"는 *이 논문이 정확한 1차 출처*. 확정.**
- 매핑: 우리 real-bulk **22–24 GPa** = Sakuda 24(이 논문) ∩ Bazzoun 22.1(LPSCl). 우리 **E_eff 1.35(DEM)/1.53(MPM)**는 이
  24의 **18× 연화 프록시**(강체-구/단상-연속체가 못 잡는 granular 재배열·GB-slide·micro-fracture 럼핑) — Sakuda가 **real E가
  뻣뻣함을 측정으로 확정**해 줌으로써 "1.35는 임의 아니라 *측정된 24의 연화*"라는 우리 논거가 성립.

**C. "Three-way agreement" 재서술(정직).**
- 우리가 말해 온 "DEM ~13–17 % ↔ Sakuda ↔ Minnmann" 3-way porosity 일치는 **압력·소재가 각기 다름**을 명시해야 정직:
  - **DEM/우리**: LPSCl, **300 MPa**, pure-SE ~10 % / composite 15.6 %.
  - **Minnmann 2021 JES**: NCM622+LPSCl 복합, 압밀 **380 MPa**, porosity **13–17 %**(복합, *pure-SE 아님*).
  - **Sakuda 2013**: 75Li₂S·25P₂S₅ **glass**(≠LPSCl), **stated >90 %(porosity<10 %)@>350 MPa** / digitized ~87 %@~300.
- ⇒ 세 값은 **"황화물-유리계가 수백 MPa 냉간가압서 porosity ~10–17 %로 치밀화"**라는 **거동(추세)의 3중 정합**이지,
  **같은 소재·같은 압력의 byte-identical 수치 일치가 아니다.** Sakuda의 기여 = **same-family 거동·E·물리** 앵커 (절대 porosity의
  소재-특정 정밀값은 LPSCl 쪽 Minnmann/Doux/우리 DEM이 소유).

## 12. 주의/한계 (over-claim 방지)
- ⚠ **소재가 LPSCl argyrodite 아님**: 75/80Li₂S·25/20P₂S₅ **glass**(= Li₃PS₄ 조성 유리). 우리 Li₆PS₅Cl과 **다른 황화물.**
  → **σ 절대값(0.3 mS/cm) 전이 절대 금지**(LPSCl는 ~1–3으로 ~10× 높음); **밀도 절대값도 소재-특정**. **기계물성·치밀화 물리·
  E 추세는 same sulfide family 라 전이 가능**(soft, 상온 치밀, 중간 E).
- ⚠ **밀도 "87 %@300"은 digitized(추세)** — stated 는 ">90 %@>350 MPa"뿐(§11). 정밀 cite 금지.
- ⚠ **glass ≠ glass-ceramic**: 밀도/σ는 *유리* 기준. 결정화(glass-ceramic)는 σ 더 높을 수 있으나 이 곡선과 별개.
- ⚠ **E는 hot-press 고밀도 펠릿서 초음파 측정**(공극 배제) = *재료 고유 E*. 우리 *압밀용 E_eff* (granular bed의 유효강성)와는
  **층위가 다름**(real-material E vs effective-bed E) — Sakuda 24는 우리 *real-bulk* 칸에만 매핑, E_eff 1.35와 직접 동일시 금지.
- ⚠ **porosity·coordination·coverage·tortuosity·Heckel-fit 수치 없음** — 우리가 가져올 직접 수치는 밀도-vs-P 곡선 + E + σ 뿐.
- ⚠ **2013년 초기 황화물 논문** — PSD(D10/50/90) 수치 없음(정성 "수~수십 µm"), SI(S1–S3) PDF 미첨부(본문 인용만).
- ⚠ **시뮬레이션 없음** — frame[4] **외부 실험/물리 앵커**로만(우리 Kirchhoff/Holm·삼중항·MPM 변형장 우위 유지).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

# Intertwined Nature of Electrochemical Reactions and Mechanical Instability in Sulfide-Based All-Solid-State Batteries — Kang, Shin, Lee & **Jong-Won Lee** (Chem. Commun. *Feature Article* 2026)

> slug `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` · DOI `10.1039/d5cc06309d` · type `review (Feature Article; exp+DFT+FEM 문헌 종합, 자체 신규 데이터 無)` · PDF `c0c4fd29-…Intertwined_nature…ASSB.pdf` · digested `2026-06-26` · status ✅
> **저자**: **Junhee Kang**ᵃ, **Hong Rim Shin**ᵃ, **Yeokyung Lee**ᵃ, **Jong-Won Lee**\*ᵃᵇ — ᵃ Division of Materials Science and Engineering, **Hanyang University** (222 Wangsimni-ro, Seongdong-gu, Seoul 04763, Korea); ᵇ Department of Battery Engineering, Hanyang University. 교신 jongwonlee@hanyang.ac.kr.
> *Chem. Commun.* **2026**, 62, 10277–10294 (18 pp). Received 6 Nov 2025 / Accepted 24 Apr 2026. 지원: NRF Korea RS-2025-25441254, RS-2025-25418010.

---

## 0. 이 digest를 읽는 법 — **[우리 그룹] 리뷰, "왜 우리 DFT를 하는가"의 상위 프레임**

**이 논문은 우리 그룹(한양대 Jong-Won Lee 연구실)이 직접 쓴 review(Feature Article)다.** 앞서 digest한 [KimICCF](ICCF cavity filler)·[KimCA](도전재 차원)가 *같은 그룹 계열의 실험* 논문이었다면, 이건 **우리 그룹이 황화물 ASSB 분야 전체를 어떻게 바라보는가**를 보여주는 *우리 자신의 세계관(world-view)* 문서다. 따라서 이 digest의 목적은 단순 "외부 문헌 정렬"이 아니라:

1. **우리 연구실의 연구 방향·내러티브를 코드화**한다 — 이 리뷰의 조직 틀(taxonomy)·인과사슬(cause→effect)·미래 방향이 곧 우리(나, 박사과정/연구원)가 따라야 할 연구 지도다.
2. **우리 DFT(comp1/modelc/Nd2O3 cascade/ESW/elastic/XPS)가 이 큰 그림의 어디에 꽂히는가**를 명시한다. 리뷰는 "electrochemo-mechanical coupling이 핵심 병목"이라고 선언하는데, 우리 DFT는 그 coupling의 *electrochemical 절반*(산화/환원 분해 화학, SEI 산물의 전자절연성)과 *mechanical 절반*(elastic, EOS, 연성)을 **bulk·atomistic 레벨에서 정량화**하는 일을 한다.

> 🔑 **리뷰의 중심 thesis (한 문장)**: 황화물 ASSB의 진짜 문제는 "전기화학 분해" 하나도, "기계 파괴" 하나도 아니라 — **둘이 서로를 *유발하고 가속*하는 양방향 되먹임 고리(electrochemo-mechanical feedback loop)** 이며, 따라서 지속가능한 계면 안정성은 *화학 passivation 또는 기계 보강 한쪽*이 아니라 **둘을 동시에** 다뤄야 달성된다. (Abstract 마지막 문장: "sustainable interfacial stability is **not simply a matter of chemical passivation *or* mechanical reinforcement**, but requires strategies that address **both issues simultaneously**.")

> 🔗 **litdb 내 위치**: **리뷰·우리그룹·electrochemo-mechanical coupling 축**. [Rupp]리뷰(`kim2021_review…`)가 "oxide vs sulfide + 계면 landscape"의 *외부* 지도였다면, 이 리뷰는 **우리 그룹이 직접 그린 sulfide-전용 chemo-mechanical 지도**다. 두 리뷰의 차이: Rupp는 *물질 패밀리 비교*(어떤 SE를 쓸까)에 무게, 이 리뷰는 *열화 메커니즘의 coupling*(왜 망가지나, 어떻게 막나)에 무게. reference key `[Kang]` ⭐우리그룹 으로 등록.

---

## 1. 한 줄 요약

황화물 SE(Li₆PS₅Cl·LGPS) ASSB는 σ·연성·가공성은 좋지만, **(A) 좁은 전기화학창(~2.0–2.5 V vs Li⁺/Li)에서 일어나는 산화/환원/CA-유발/대기 분해**와 **(B) 활물질 부피변화·접촉손실·균열·dendrite 같은 기계 열화**가 **하나의 되먹임 고리**로 얽혀(reaction→fragility→fracture→fresh surface→more reaction) 셀을 죽인다. 이 Feature Article은 그 coupling의 기원·증거(operando XPS/ToF-SIMS/XCT/cryo-TEM + DFT/FEM)·세 갈래 완화전략(① **SE 도핑/치환**, ② **양극 CAM 표면 코팅**, ③ **음극 계면공학**)을 정리하고, "**한 변수를 고치면 다른 변수가 따라 바뀐다 → 통합 chemo-mechanical 설계가 필요**"라는 로드맵으로 닫는다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자/소속 | **Junhee Kang · Hong Rim Shin · Yeokyung Lee · Jong-Won Lee\*** (전원 한양대 MSE; J.-W. Lee는 Battery Eng. 겸직) |
| 저널/년/형식 | *Chem. Commun.* **62**, 10277–10294 (**2026**), **Feature Article (리뷰형)**, 18 pp |
| DOI | **10.1039/d5cc06309d** |
| 대상 | **황화물 SE 기반 ASSB 전용** (argyrodite Li₆PS₅X·LGPS·Li₃PS₄ + Ni-rich NCM/NCA 양극 + Li metal/Li–In 음극) |
| 핵심 주제 | **electrochemo-mechanical degradation = 전기화학 분해 × 기계 불안정의 양방향 coupling** |
| 우리 관심 조성 | **Li₆PS₅Cl(=comp1), Cl-rich(=modelc 계열), O-doped 옥시설파이드(=우리 Nd2O3 oxysulfide와 직접 연결), BH₄/halogen 도핑** |
| 연구유형 | 종합 리뷰 — 모든 수치·그림이 2차 인용. **자체 신규 계산/실험 없음**(Data availability: "No primary research results … and no new data were generated or analysed") |
| 핵심 표 | **Table 1** = electrochemo-mechanical 열화 메커니즘 × 기원 × 결과 × 완화전략 마스터 매트릭스 |
| 핵심 그림 | **Fig 16** = coupling 고리 + 3대 완화전략 한 장 요약 (deck용); Fig 1·5·6 = 전기화학창/SEI/dendrite |

---

## 3. 리뷰의 조직 틀 (taxonomy) — **이 구조가 곧 우리 연구의 지도**

리뷰는 §2→§3→§4→§5→§6의 **사다리 구조**로, "전기화학 분해 → 기계 분해 → 둘의 coupling → 완화 → 전망"을 쌓아 올린다. (Intro 마지막 문단에서 저자가 직접 이 구조를 예고.) **각 절이 어떤 인과사슬을 다루는지**를 먼저 지도로:

| § | 제목 | 다루는 것 | 핵심 인과사슬 (cause→effect) |
|---|---|---|---|
| **2** | Electrochemical degradation | 양극·음극에서의 *전기화학적* 분해 4종(양극)+3종(음극) | 좁은 ECW → P–S 결합 산화/환원 → 분해산물(Li₂Sₓ/P₂Sₓ/LiCl/Li₃PO₄/sulfate/Li₂S/Li₃P) → CEI/SEI 형성 → 저항↑ |
| **3** | Mechanical degradation | 전극 내부 *기계적* 열화 (공동·접촉손실·균열·dendrite) | 부피변화·입자크기 불일치 → 공동/접촉손실/균열 → 전도경로 끊김 → 국소 전류집중 |
| **4** | Electrochemo-mechanical **interplay** | **둘의 coupling = 되먹임 고리** (핵심 절) | 분해→취약화→파괴→새 표면 노출→재분해 (self-amplifying) |
| **5** | Mitigation strategies | 3대 완화: ① SE 도핑 ② CAM 코팅 ③ 음극 공학 | 화학+기계를 *동시에* 안정화하는 interphase 설계 |
| **6** | Summary & outlook | 통합 chemo-mechanical 설계 로드맵 | "한 변수 바꾸면 다른 변수 바뀜 → 통합 설계 필요" |

**리뷰가 기존 리뷰와 차별화하는 지점**(§2 끝, 저자 명시): "Previous reviews have addressed interfacial chemistry, SE design, and electrode optimization; however, **a dedicated emphasis on the origins, manifestations, and mitigation strategies of the *coupled* evolution of electrochemical reactions and mechanical instability … remains under-explored.**" → 즉 이 리뷰의 신규성 = **coupling 자체를 주인공으로** 삼은 것.

---

## 4. §2 전기화학 분해 ★ — 양극 4종 + 음극 3종

### 4.0 출발점: 좁은 전기화학창 (Fig 1)
- 황화물 SE의 **본질적 산화한계 = ~2.0–2.5 V vs Li⁺/Li** — Ni-rich 층상 산화물 작동전압(>4.2 V)보다 **한참 낮음** → 양극에서 필연적 산화 분해. (Fig 1a = 여러 SE의 전기화학창 막대, ref 49 Zhu/He/Mo; LiPON/LLZO/LATP/LAGP/LISICON 등과 비교.)
- **Fig 1b (ref 50)**: full cell의 **thermodynamic / kinetic / predicted ECW**를 구분 — "operation window"가 "thermodynamic window"보다 넓게 보이는 이유 = **kinetic passivation**. 평가 접근법(Approaches) 박스: anionic framework·molecular structure·crystal structure·high-valent cation·terminal groups·lithium salts (조성 레버) + test protocols·redox-derived reactions·catalytic reactions·charge transfer layer (kinetic 레버) + phase stability·thermodynamic stability·redox potential·local coordination (열역학 레버).
> 🔑 우리 연결: 이 Fig 1b의 "thermodynamic ECW vs kinetic ECW" 구분이 곧 **우리 grand-potential ESW(=thermodynamic, intrinsic onset)** 와 **실험창(=kinetic, passivation 포함)** 의 차이를 설명하는 그림. 우리 onset 2.256 V = thermodynamic 쪽.

### 4.1 양극 §2.1 — 복합양극 분해 4 카테고리
복합양극(CAM+SE+CA 공존)에서 "side reactions are inevitable and often strongly coupled". **4종 대표 메커니즘**:

**(i) 산화 분해 of SE (§2.1.1, Fig 2)**
- argyrodite Li₆PS₅X의 산화한계 ~2.0–2.5 V — 충전 시 **P–S 결합과 free S²⁻가 산화** → Li₂Sₓ, P₂Sₓ, LiCl, sulfate(Li₂SO₄) 혼합 CEI 형성 (Fig 2a = S 2p / P 2p XPS 진화, ref 51; Fig 2b = ToF-SIMS PO₂⁻/PO₃⁻ fragment 분포, ref 33).
- **미시 메커니즘 (Cao et al., ref 54, XAS+DFT)**: 산화 분해 시작 = "**Li atom이 이웃 S에 대한 affinity가 감소** → Li–S 배위 약화 → **S–S 결합 형성 촉진**" → 그 다음 **PS₄ 모티프가 PS₃로 붕괴** → 계면 저항↑.
- **self-passivation**: CEI의 poor electrical conductivity가 정적(static) 조건에서 추가 분해를 kinetically 억제 → 자기제한적. **단, 산화 분해의 정도·경로는 *국소 구조 무질서*에 의존** → electrode-scale로 보면 *전도경로·반응의 heterogeneity*로 이어짐 (ref 14). ⭐
> 🔑 이 마지막 문장("oxidative decomposition … depends on the *local structural disorder* of the SE particles … leading to electrode-scale disruption of conduction pathways and evolution of reaction heterogeneity")이 **무질서→불균일 분해** 인과의 핵심이고, 우리 SQS/무질서 처리·국소 배위 논의와 직결.

**(ii) CAM/SE 계면 반응 (§2.1.2, Fig 3)**
- Ni-rich NCM/NCA는 **O와 S의 화학퍼텐셜 불일치** → space-charge layer + parasitic 계면 반응. 고전압·고SOC(>~4.2 V)서 **격자 산소 방출** → 방출된 O가 SE의 S를 산화 → **SOₓ(전자절연) 형성** + **Ni⁴⁺→Ni²⁺ 부분환원**(TM dissolution) → CAM 표면 구조 붕괴 + rock-salt 상 형성 (Fig 3a 모식).
- **Banerjee et al. (ref 51, first-principles)**: Ni-rich NCA와 LPSCl은 **화학적으로 비호환** → **LiCl, Li₃PO₄, NiS₂**가 지배적 계면 산물로 자발 형성 (Fig 3b = pseudo-binary phase diagram LPSCl–delithiated NCA; Fig 3c = AIMD 50 ps 후 원자구조, LiCl·Li₃PO₄·NiS₂ 형성 가시화).
- TEM+EELS(ref 64)·synchrotron XAS(refs 51,65): TM 환원·산소 손실·SE 분해가 **동시 발생** → 화학·구조 열화의 강한 coupling.
- **열폭주**: Kim et al. (ref 66) — 황화물 ASSB도 Ni-rich NCM–LPSCl 복합에서 **~150 °C에서 thermal runaway/폭발** (inert Ar 분위기에서도) → CAM 산소 방출의 위험성. 반대로 **LiFePO₄는 P–O 결합(polyanion)이 강해 350 °C까지 산소 방출 억제** → LPSCl과 발열반응 안 함. ⭐(P–O > P–S 결합 강도 = O-doping 동기)

**(iii) CA-유발 분해 (§2.1.3, Fig 4)**
- 도전재(carbon)는 전자전도엔 필수지만 **새 분해경로**를 연다 — 특히 **TPB(triple-phase boundary, CAM+SE+CA 3상 접점)** 에서 carbon이 SE로 전자 누출 → 분해 촉진. 산물 = 전자전도성 C–S/polysulfide + 저항성 Li₂S/P₂Sₓ/Li₃PO₄ 혼재 → 전자/이온 균형 깨고 **국소 전류 불균일**.
- ToF-SIMS(ref 71, Fig 4a): carbon 함유 양극에서 cycling 후 **phosphate fragment(POₓ⁻) 유의하게 증가** → carbon의 SE 분해 촉매 역할.
- **Kim et al. (ref 69) dilemma (Fig 4b)**: 저carbon = Li⁺ 경로 유지되나 CAM 활용↓; 과carbon = 분해부산물↑ + carbon이 Li⁺ 전도 *방해* → **carbon 함량 trade-off**. 해법 = 전자전도성 코팅 / engineered carbon architecture / **1D carbon nanofiber(VGCF)로 TPB 노출 최소화** (Wang et al.). ⭐⭐
> 🔑 이 §2.1.3 전체 = **우리 그룹 [KimCA] 논문의 리뷰 내 압축**. "0D Super P 과잉(TPB↑)이 나쁘고 1D VGCF(TPB↓)가 좋다"가 바로 ref 69(=Kim/…/Cho/Lee, *Adv. Funct. Mater.* 2024 self-cite). 우리 그룹이 자기 실험을 자기 리뷰에 박아 넣은 자리.

**(iv) 대기 노출 분해 (§2.1.4, Fig 5 일부)**
- 습한 공기에 잠깐만 노출돼도 급속 가수분해 → **독성·부식성 H₂S 발생** + 결정성 SE 파괴. 대표 반응: **Li₂S + H₂O → H₂S(g) + 2 LiOH** (Eq 1).
- 가수분해는 SE 골격만 깨는 게 아니라 **2차 phosphate/sulfate/oxysulfide 형성** → Li⁺ 확산경로 막고 mobile carrier↓. TGA/DSC = H₂S 발생 동반 발열·질량손실. FT-IR(Chen et al., ref 79): O–H/C=O/PO₄³⁻ band 등장(산화 불순물 도입), air-exposed LPSCl XRD = **비가역 구조변화**(가열로 단거리 질서는 회복돼도 영구 격자결함·비정질화 잔존).
> 🔑 우리 연결: 이 "대기 취약 → H₂S → 가수분해 phosphate/oxysulfide" 가 **O-doping이 대기안정성도 올린다**는 동기(P–O 결합)와 연결되고, 우리 Nd2O3/O-doping의 부수 이점 논거.

### 4.2 음극 §2.2 — Li 금속 계면 3종
Li metal(3860 mAh/g, −3.04 V vs SHE)은 에너지밀도 최강이나 황화물과 만나면:

**(i) 환원 분해 of SE (§2.2.1, Fig 5)**
- argyrodite는 **~1.7 V vs Li⁺/Li 이하서 열역학 불안정** → Li 금속 직접접촉 시 격렬 환원. **P–S·S–S 결합 단계적 환원** → **Li₂S, Li₃P, LiCl**이 지배 계면산물 (Fig 5a,b = LPS의 S 2p/P 2p XPS, Li 증착 전후, ref 81 — "reduced phosphorus species" 등장).
- 액체 SEI와 달리 황화물 SEI는 **불균일**: Li₂S는 약간의 이온전도성, **Li₃P·LiCl은 대체로 저항성** → mixed interphase가 두께 불균일·저항↑.
- **Nolan et al. (ref 47) 3분류 (Fig 5c)** — 우리에게 가장 중요한 프레임:
  - **Type 1 (Ideal)**: 열역학 안정 Li-binary(Li₃N, LiF, Li₂O, Li₂S, LiCl 등) → **분해 없음, passivating**.
  - **Type 2 (MIEC, mixed ionic-electronic conductor)**: LGPS처럼 **전자 누출 지속** → SEI가 *계속 성장*(grow & thicken) → 비가역 Li 손실.
  - **Type 3 (SEI)**: LPSCl/argyrodite — 분해는 일어나나 **전자절연 SEI**가 형성돼 **kinetic하게 추가환원 차단**(열역학적으론 불안정하지만 시간이 지나며 stabilize). LiPON이 대표.
> 🔑 **이 Type 1/2/3 분류 = 우리 SEI 패시베이션 논리의 정확한 프레임**. 우리 Nd2O3 cascade의 핵심 주장("doped interphase는 wide-gap 전자절연이라 e⁻ leak 차단")이 곧 **Type 3(또는 Type 1 강화)로 SEI를 밀어 넣자**는 것. 우리 sei_products.json의 gap 분류(insulator≥4 / marginal 2–4 / conductor<2 eV)가 이 Type 분류의 *정량판*.

**(ii) Dendrite 형성 (§2.2.2, Fig 6)**
- 액체에선 dendrite가 주로 확산제어지만, **황화물에선 계면 분해·불균일 Li⁺ 전도가 좌우**. LPSCl 환원이 만든 **화학적으로 취약·이온적으로 불균일한 interphase**가 전류를 국소 hotspot으로 몰아 → filament 핵생성 → 입계/결함 따라 Li 침투.
- **filamentary conduction onset → 급격한 전압 불안정 → 단락** (Fig 6a = Li|LPSCl|Li, 3.0 mA/cm²서 전압 급강하; Fig 6b = operando XCT로 균열 통한 Li 침투 가시화, ref 89; Fig 6c = SEI layer 형성, ref 90).
- **Hao et al. (ref 90, 계산)**: Li⁰ 증착의 에너지적 선호 상태 분석 → **환원이 만든 heterogeneous interphase가 Li 핵생성을 결정**, 균일 전류분포 방해. dendrite 핵생성은 *pristine bulk SE의 전자구조*가 아니라 **부분환원된 SEI의 ionization 특성**에서 비롯 (Fig 6c).
> 🔑 우리 연결: "dendrite는 bulk SE가 아니라 *환원 SEI*가 좌우" → 우리가 bulk σ_e(gap 2.07 eV wide insulator)만 보는 것의 한계를 명시하고, **SEI 산물의 전자절연성(우리 sei_products.json)이 dendrite 억제의 진짜 레버**임을 뒷받침.

---

## 5. §3 기계 분해 ★ — 양극 3종 + 음극(고변형) 2종

기계 열화의 근원(§3 도입): 액체와 달리 ASSB는 **전적으로 고체-고체 접촉**에 의존 → "intrinsic structural dependency" → 공정유발 미세결함에 극도로 민감 + cycling 중 (de)lithiation 부피변화가 응력 생성.

### 5.1 양극 기계 §3.1 — 3종
**(i) 공정 후 공동 형성 (§3.1.1, Fig 7)**
- 복합양극 제조(고압 냉간가압 or slurry casting)에도 **나노~마이크로 공동이 필연 잔존**. 원인 4가지:
  1. **CAM(5–15 µm) vs SE(1–5 µm) 입자크기 불일치** → 작은 SE가 큰 CAM 사이 틈을 부분만 채움 → 계면 void.
  2. **불균일 가압** → 국소 force concentration + 가압방향 수직 persistent void (Doux et al., ref 100: 370 MPa 고압에서도 3D tomography로 비-무시 불규칙 공동 확인).
  3. **변형거동 불일치**: 단단한 oxide CAM(E=150–200 GPa) vs 부드러운 sulfide SE(E=20–30 GPa) → SE는 소성변형하나 CAM 강성 수용 못 함 → 구조 불균일 잔존.
  4. wet-process 시 잔류용매 증발 → 나노공동.
- **Fig 7b**: 가압↑ → porosity↓·contact area↑·성능↑ (저율속서). 공동은 CAM/SE 접촉 불균일 → 전류 불균일(접촉 좋은 곳만 활성) → 국소 hotspot.

**(ii) CAM/SE 접촉손실 (§3.1.2, Fig 8)**
- 최적가압으로 제조해도 cycling 중 접촉유지 어려움. 주원인 = **CAM 부피변화**: Ni-rich 산화물은 Li 추출 시 **6–8% 격자 수축**(ref 103), 인접 ceramic SE는 거의 무변형 → 기계 비호환 → delamination·접촉손실.
- **이방성 격자팽창**(c축 따라) → shear stress → delamination·계면 void 가속. H2–H3 상전이서 더 심화.
- **Fig 8a (ref 105)**: 연속 cycling → 누적 접촉손실 → 방전용량 급감; **300 MPa로 re-press하면 용량 상당부분 회복** → 접촉손실이 가역(접촉만 복구하면 됨). **Fig 8b**: 30 cycle 후 저주파 저항 급증 → re-press로 ~1/3로 감소.
- **Shi et al. (ref 106)**: CAM/SE 입자크기 비가 접촉의 핵심 — 비↑ → 활용·로딩↑. SE 입자가 CAM에 근접하면 percolation 급락. 실험: 12 µm NCM + 1.5 µm SE → ~50 vol% CAM 로딩서 거의 완전 용량유지 → cold-press만으로 액체급 에너지밀도 가능.

**(iii) CAM 입자 균열 (§3.1.3, Fig 9)**
- Ni-rich 산화물의 **이방성 격자변형**이 dominant 기계파괴. delithiation 시 **c축 수축이 a/b축보다 훨씬 큼** → 내부 응력 heterogeneity → H2–H3 상전이서 체적 불일치 증폭 → **CAM 항복강도(σᵧ ~100 MPa) 초과** → intergranular/intragranular 균열 핵생성·전파 (Fig 9a = 3D tomography 균열, ref 111; Fig 9b = Li 농도·입계 손상; ref 111 계산: 수 GPa 응력이 불균일 delithiation서 발생).
- **균열-표면화학 coupling (Li et al., ref 112)**: 표면 격자 재구성이 subsurface 균열밀도와 강한 상관 → bulk 파괴 ↔ 표면 열화 상호변조. surface Ni 산화 ↔ 내부 porosity 음의 상관.
- **단결정 vs 다결정 (Fig 9c, ref 114)**: 다결정 NCM811은 1차입자 입계서 심한 균열, **단결정은 균일 부피변화·구조탄성 우수** → 단결정 = 기계해법.

### 5.2 음극 기계 §3.2 — 고변형 음극 2종
**(i) Li 도금/벗김 부피변화 (§3.2.1, Fig 10)**
- Li metal = 완전 도금/벗김 시 **~100% 부피변화** → 가장 기계 불안정. **Li–In 합금(LPSCl과 호환성으로 널리 사용)은 In→Li–In 전환 시 105.6% 팽창** (ref 116) → 반복 도금서 void·protrusion → Li/SE 불안정.
- **벗김(stripping) 시 Li vacancy가 Li/SE 경계 축적 → void 핵생성·성장·합체** (Fig 10a, ref 117) → 유효접촉면적↓ → 적은 활성점으로 전류 재분배 → 국소 전류밀도 증폭.
- **Kasemchainan et al. (ref 118)**: stripping void가 다음 cycle에서 occluded void 형성 → 작은 void 합체 → 접촉손실·void 성장의 **악순환 sequence**. Fig 10b = 모식, Fig 10c = Li/LPSCl SEM 단면(cycling 따라 void·균열·심한 계면열화).

**(ii) 응력-보조 dendrite 전파 (§3.2.2)**
- 부피변화 외에 **응력 자체가 dendrite 핵생성·성장에 결정적**. 불균일 Li 증착 → 결함/공동/입계에 응력 집중. 황화물은 (oxide보다 낮은 shear modulus라) 응력유발 Li 침투에 더 취약.
- **핵심 통찰 (ref 119, in situ X-ray + phase-contrast tomography)**: **균열이 Li filament *앞서* 전파** → "stress-induced fracture가 전기화학 침투에 *선행*할 수 있다" → dendrite는 금속이 밀고 들어가는 게 아니라 **응력이 먼저 길을 낸다**.
- Li의 **점성거동(diffusional creep)**: 느린 율속선 응력완화, 고전류서는 국소 큰 변형 → crack-driven filament 전파 가속 → "전기화학 구동력 × 응력-보조 균열"의 coupling이 황화물에서 dendrite 빠른 침투를 설명.

---

## 6. §4 Electrochemo-mechanical interplay ★★ — **리뷰의 심장 (되먹임 고리)**

§4 도입: "electrochemical decomposition and mechanical instability **reinforce each other in a feedback loop**, where reaction-induced fragility leads to fracture, and the exposed surfaces accelerate ongoing interfacial degradation." → **이 절이 리뷰의 thesis를 증명하는 곳.**

### 6.1 표면 불균일-유발 기계파괴 (§4.1, Fig 11) — **화학→기계 방향**
인과사슬(명시적):
1. CAM/SE 계면 전기화학 분해 → **화학적으로 heterogeneous한 interphase**(Li₂S/Li₂SO₄/Li₃PO₄/halide 혼합, 각각 다른 전도·기계 물성).
2. 취성·저항성 상(Li₂SO₄)은 cycling 응력에 **쉽게 균열**; 전도성이나 기계약한 영역은 **delamination 악화**.
3. 균열 → 연속 Li⁺/e⁻ percolation 끊김 → 활물질 활용↓.
4. 새로 노출된 pristine CAM facet → SE와 **재반응** → 저항성 interphase 점진 성장(thicken over time).
5. **fracture → interphase evolution → contact loss**가 **self-amplifying feedback loop** 형성 → 순수 전기화학 분해보다 훨씬 빠른 용량감소.
- **Fig 11a (ref 37)**: NCM:SE 비별 80% 방전상태 stress map — NCM 비↑ → stress 국소화·tensile/compressive sharp gradient. **Fig 11b**: cycling 양극 FIB-SEM 균열망 = 조성 불균일 hot spot서 기원. **Fig 11c (ref 39, phase-field)**: case 1(무작위 배향 grain=inhomogeneity) → 이방성 Li 전도 → 불균일 volumetric strain/von Mises stress → **균열 조기 핵생성·전파(crack order↑)**; case 2(homogeneous) → stress gradient·균열 억제. ⭐
> 🔑 Fig 11c(ref 39 = S. Kim/J. H. Park/J.-W. Lee, *Electrochim. Acta* 2025, **self-cite**)가 우리 그룹의 phase-field 기여. "구조 불균일이 불균일 응력·균열을 낳는다" → 우리 무질서 처리(SQS)·국소배위 논의의 거시판.

### 6.2 기계 불안정-유발 분해 (§4.2, Fig 12) — **기계→화학 방향**
인과사슬(반대 방향):
1. SE 막이 양극·음극을 기계적으로 **연결(couple)** → 한쪽 응력이 다른 쪽으로 전달.
2. **고변형 음극(Li–In) → 전체 stack pressure 변동** → 양극의 기계안정성 교란 (Kang et al., ref 120, **self-cite**): Li–In 셀은 **~3.8 MPa 압력 excursion**(LTO 셀 ~0.2 MPa보다 한 자릿수↑) → NCA 양극에 반복 tension-compression → 입자 피로.
3. 이 기계 불안정 → CAM/SE 계면 전기화학 반응 집중(이온/전자 전도 방해) → SE **산화 분해 가속**.
4. XPS(Fig 12b): Li–In 셀 양극은 200 cycle 후 **저항성 species 많이 형성**, LTO 셀은 비교적 온전. SEM(Fig 12c): LTO는 다결정 온전 유지, Li–In은 150 cycle 후 NCA 2차입자 **입계균열·분쇄**. Fig 12d 모식 = anode-side chemo-mech 열화의 본질(dynamic contact → 불균일 Li⁺ 분포 → 국소 응력 → 입계균열 → 새 표면 → 가속).
- **양방향성(bidirectional coupling)**: anode→cathode뿐 아니라 **cathode→anode**도 작동 — Huang et al.(ref 124): 양극 내부 기계손상이 electrode-level 반응 heterogeneity → 불균일 Li⁺ flux·SE막 응력 → 불균일 Li 증착. Moradi et al.(ref 125): CAM의 (de)lithiation volumetric strain이 ASSB 내부압력 거동 변화 → SE/음극 계면 무결성 영향. 양극 net stress 양수(예 LiCoO₂) → SE/음극 계면 voiding → 방전 시 특징적 전압 급강하.
> 🔑 §4.2 = **우리 그룹 ref 120(Kang)·39(Kim/Park/Lee)의 압축**. "기계 불안정이 화학 분해를 *역으로* 가속" = 리뷰가 강조하는 *되먹임의 닫힘*. 우리 DFT는 이 고리의 화학 절반(분해산물)과 기계 절반(elastic) 각각을 줄 수 있으나, **coupling(동적 응력↔반응) 자체는 우리 정적 bulk DFT 밖** → 정직한 한계.

> **§4 한 줄 종합**: **"부서지지도 반응하지도 않는다 — 그것들의 *heterogeneity*가 문제다"** (§6에서 재진술: "it is **not the decomposition or stress itself but their heterogeneities** that trigger and accelerate the degradation"). 균일하면 둘 다 self-limiting, 불균일하면 되먹임 폭주.

---

## 7. §5 완화 전략 ★ — 3대 갈래 (Fig 16 요약)

§5 도입: 열화가 화학+기계 양쪽에서 오므로 완화도 **둘을 동시에** 안정화해야 → 3 갈래.

### 7.1 ① SE 도핑/치환 (§5.1, Fig 13) — **우리 DFT의 본진**
"SEs are *uniquely positioned* to address electrochemo-mechanical degradation across the *entire* ASSB system" — SE는 양극·음극 양쪽과 동시에 접하므로 **bulk 조성/화학 수정이 모든 junction에 영향** → 가장 강력한 단일 레버.

**(a) Borohydride(BH₄⁻) 도핑 (Fig 13a,b, ref 127)**: LPSCl에 BH₄⁻ → **CCD 7.3 mA/cm²** (baseline LPSCl 2.6의 ~3배). 개선의 본질 = σ가 아니라 **얇고 기계순응적·전자절연인 tri-layer SEI(Li₃P/LiBH₄(LBH)/Li₂S)** 형성 → 응력축적·void 억제. (이온전도 >2.5 mS/cm 유지.)
**(b) O²⁻ 치환 (옥시설파이드, Fig 13c,d, refs 128–130)**: PS₄³⁻에 O 도입 → **Li₆.₂₅PS₄.₂₅Cl₀.₇₅** 같은 mixed 옥시설파이드 골격 (Fig 13c = Li₆PS₄OCl 구조). 효과: **전자누출↓ + 균일 이온전도 interphase** → Li⁺ flux 균질화·cycling 응력 buffer. CV(Fig 13d, ref 128): C+SE|SE|Li에서 **전기화학창 확대**(2.5 V/2.9 V/4.2 V 분해 onset이 도핑으로 늘어남, ΔV≈0.4 V), 환원·산화 분해 모두 억제. **O가 만든 O–P 결합이 원래 S–P보다 강해** → 전기화학 안정성 + 대기내성↑. 이온전도 ≥2.5 mS/cm 유지.
**(c) Li₃PO₄ buffer (Fig 13e, ref 128)**: 황화물 SE와 층상 산화물 사이 보호층 → 고전압서 parasitic 반응 최소화 + **CAM 산소방출 억제 + mechanically 약한 sulfate 형성 방지** → 화학·구조 안정.
**(d) 광범위 치환 (§5.1 끝)**: halogen(F,Br,I)·pnictogen(Sb,Bi)·chalcogen(Se,Te)이 이온전도·band gap·계면안정 튜닝에 보고됨. **Wang et al. (ref 136)**: Li₅.₅PS₄.₅Cl₀.₇₅Br₀.₇₅ **1 kg batch** 합성하며 13 mS/cm 유지 → 도핑 SE의 **상용 대량생산 가능성**.
> 🔑🔑 **이 §5.1(a)(b)(c)가 우리 그룹 DFT 작업의 정확한 표적이다**:
> - **(b) O²⁻ 옥시설파이드 (Li₆.₂₅PS₄.₂₅Cl₀.₇₅, 전자누출↓·ECW 확대·O–P>S–P)** = **우리 Nd2O3-doping/O-doping cascade의 리뷰 내 정당화**. 우리 sei_products.json이 정확히 이걸 정량화: O-derived Li₃PO₄(gap 5.73 eV)·Li₂O(5.24)·NdPO₄(5.55)가 conductive Li₃P(0.70)를 대체해 e⁻ leak 차단. 리뷰의 "reduced electron leakage + O–P 결합 강화"가 곧 우리 결론.
> - **(c) Li₃PO₄ buffer (산소방출 억제·sulfate 방지)** = 우리 Nd cascade에서 Li₃PO₄가 bulk-GB·cathode passivation으로 persist(0.69–3.06 V)하는 것과 동일 역할.
> - **(a) BH₄ tri-layer SEI / (b) doping이 ECW 확대** = 우리 grand-potential ESW·constrained ESW·doping cascade(47 dopant 스크리닝)의 직접 동기.

### 7.2 ② 양극 CAM 표면 코팅 (§5.2, Fig 14)
- Ni-rich 산화물 표면 코팅 = 산화 분해 억제 + diffusion-유발 응력 완화의 **가장 직접적·효과적** 전략.
- **Cha et al. (ref 137) NCM@LZC**: 단순 물리혼합으로 Li–Zr–Cl(LZC) halide 층 형성 → 균일 캡슐화, 화학안정·이온전도 barrier. bare NCM은 저항성 interlayer, LZC-코팅은 clean 계면 유지 → 용량유지 우수.
- 실제 적용 코팅: **LiNbO₃(LNO)·Li₂ZrO₃(LZO)·LiTaO₃** — ALD/CVD/sol-gel로 CAM 표면 증착. Fig 14d = ALD LNO-코팅 NCM811의 ~5 nm 균일 비정질막 HR-TEM; Fig 14e = operando Co K-edge XANES — bare NCM은 cycling 중 TM 환원·구조붕괴 전자구조 변화, **LNO-코팅은 안정한 전자 signature 유지**. ⭐(LNO-NCM = [KimCA]의 양극과 동일!)

### 7.3 ③ 음극 계면 공학 (§5.3, Fig 15)
- Li/SE 계면 도금/벗김 거동 조절 → 형태 불안정 방지.
- **LiPON 박막 코팅 (Su et al., ref 149, Fig 15a)**: 계면저항 ~1.3 Ω·cm²로↓, 0.5 mA/cm²서 >1000 h 안정 도금/벗김, **CCD 4.1 mA/cm²**. 비정질·이온전도·전자절연 → 균일 Li⁺ flux + 전자누출 차단 → 국소 응력축적·dendrite 억제.
- **Li 합금·anode-free (Fig 15b)**: Ag/Zn/Sn/Al 합금 원소가 핵생성 장벽↓. **Lee et al. (ref 152) Ag–C nanocomposite interlayer**: anode-free ASSB, >900 mAh/cm³, 1000 cycle 우수 — Ag가 transient Li–Ag로 lithiophilic 핵생성, carbon이 mechanically robust scaffold로 Li 균일분배. **Sohn et al. (ref 155) ZnO–Ag dual-seed**: 다중 핵생성 경로 → 응력 buffer.
- **인공 SEI**: Li₃N / LiF 기반 (refs 156–158) → 이온전도·전자절연 barrier로 직접 화학반응 decouple + 기계변형 수용. **Gao et al. (ref 156)**: 전기화학생성 Li₃N–LiF-rich interphase → **CCD 3.3 mA/cm²**, >1200 h 안정.
- **한계 명시**: 이 코팅/interlayer/인공SEI는 전부 **새 계면을 ASSB에 도입** → 제조비·시스템 복잡도↑, 계면 heterogeneity 해소 과제 남김 (lab-scale 데모 단계).
> 🔑 우리 연결: ③의 Li₃N·LiF·LiPON·Li₂O 인공SEI = 전부 **wide-gap 전자절연 패밀리** → 우리 sei_products.json·Nd cascade의 "e⁻-blocking interphase"와 같은 family. 우리 Li₃N 음극 interphase 연구가 여기 직결.

---

## 8. §6 Summary & Outlook ★ — **연구 트렌드 / 미래 방향 (사용자가 가장 원하는 부분)**

리뷰의 결론·전망 = **우리 그룹이 보는 "이 분야가 어디로 가야 하는가"**. 핵심 메시지를 트렌드 순으로:

**(트렌드 1) 패러다임 전환: 단일 문제 → coupling 문제.**
"degradation processes … often evolve **concurrently rather than independently**." 더 이상 "산화창을 넓히자" 또는 "modulus를 올리자"가 아니라 **둘의 동적 상호작용을 설계 변수로** 삼아야 한다. → **electrochemo-mechanical = 하나의 통합 설계 대상.**

**(트렌드 2) heterogeneity가 진짜 적.**
"it is **not the decomposition or stress itself but their *heterogeneities*** that trigger and accelerate the degradation." → 미래 설계는 **전기화학 반응·기계응력의 *공간적 균질성*(spatial homogeneity)** 을 최우선해야. (조성 균일·입자 배향 균일·접촉 균일.)

**(트렌드 3) "한 변수 고치면 다른 변수 바뀐다" → 통합 설계 원칙 필요.**
"**Modifying one parameter inevitably alters others**, often producing unintended consequences." → 도핑으로 σ 올리면 기계물성·ECW·SEI가 동시에 바뀜. 따라서 **chemical + mechanical + electrostatic 상호의존을 동시에 다루는 robust 설계원칙** 요구. ⭐ (이게 우리 cascade가 "stability↔Li-mobility blocking trade-off"를 동시에 보는 이유와 정확히 일치.)

**(트렌드 4) 미래 방법론 4가지 (구체 로드맵)**:
1. **in situ/operando** 특성화 고도화 → 미세구조·화학 진화를 *전기화학 거동과 동시* 모니터링.
2. **multi-scale 실험 × 계산 모델링 결합**으로 degradation↔전기화학 거동 상관 체계화. ⭐(우리 DFT/MD가 들어갈 자리)
3. **각 열화 메커니즘의 성능기여를 *decoupling*하는 방법** 개발 → 어느 메커니즘이 얼마나 기여하는지 정량분리.
4. **electrochemo-mechanical degradation의 mechanistic *threshold* 규명** → 언제 되먹임이 폭주하는지 임계조건.

**(트렌드 5) 음극·고변형 특화 방향**: 고변형 음극의 부피변화는 **strain-induced 기계손상 완화** 관점에서 다뤄야; interlayer + **porous host architecture** 결합; stack pressure 최적화(소성변형 유도로 접촉↑·응력gradient↓); Li creep deformation kinetics가 침투 결정 → **황화물 + oxide/polymer 하이브리드**(σ·안정성·유연성 균형).

**(트렌드 6) lab → 상용 다리**: scalable·manufacturable 아키텍처 = 물질혁신 + 공정적응성. **>5 mAh/cm² 후막 복합전극을 slurry로** + multilayer pouch stack pressure 최적화. "bridging fundamental lab advances with industrially viable engineering practices."

> 🔑🔑 **사용자를 위한 트렌드 한 줄**: 우리 그룹은 "조성 하나·물성 하나를 최적화하는 시대는 끝났고, **전기화학-기계 되먹임을 *통합적으로*, 그리고 *균질성*을 중심으로 설계하는 시대**"로 분야를 끌고 가려 한다. 그리고 그 통합 설계를 **multi-scale 계산(DFT/MD/phase-field/FEM) × operando 실험**으로 받치자는 것 — 즉 **우리 DFT가 이 큰 그림의 'atomistic 기둥'** 이다.

---

## 9. 정량값 총정리 ★ (리뷰가 인용한 모든 숫자 — 출처 ref 표기)

> ⚠ 전부 **2차 인용**(리뷰 자체 측정 아님). 절대값은 원전 조건 의존. n/a = 리뷰에 없음.

| 분류 | 값 | 조건/물질 | 출처(ref) |
|---|---|---|---|
| **σ (황화물 일반)** | **10⁻³–10⁻² S/cm** | RT, 액체급 | 본문 §1 |
| 산화한계(ECW) | **~2.0–2.5 V vs Li⁺/Li** | argyrodite Li₆PS₅X 본질 | §2.1.1, Fig 1, ref 49 |
| Ni-rich 작동전압 | **>4.2 V vs Li⁺/Li** | NCM/NCA | §2.1.1 |
| 격자 O 방출 onset | **>~4.2 V (고SOC)** | Ni-rich NCM/NCA | §2.1.2, ref 58 |
| 황화물 열폭주 T | **~150 °C** | Ni-rich NCM–LPSCl (Ar 중에도) | §2.1.2, ref 66 (Kim) |
| LiFePO₄ O-안정 T | **350 °C까지 산소방출 억제** | P–O polyanion | §2.1.2, ref 66 |
| 환원한계(열역학) | **~1.7 V vs Li⁺/Li** | argyrodite Li 접촉 | §2.2.1, ref 81 |
| Li 비용량 | **3860 mAh/g** | Li metal | §2.2 |
| Li 전위 | **−3.04 V vs SHE** | Li metal | §2.2 |
| Li 부피변화 | **~100%** | 완전 도금/벗김 | §3.2.1 |
| **Li–In 부피팽창** | **105.6%** | In→Li–In 전환 | §3.2.1, ref 116 |
| CAM 격자수축 | **6–8%** | Ni-rich 산화물 delithiation | §3.1.2/§3.1.3, ref 103 |
| CAM 항복강도 σᵧ | **~100 MPa** | Ni-rich 산화물 | §3.1.3 |
| CAM 균열 응력 | **수 GPa** (불균일 delithiation서) | 계산 | §3.1.3, ref 111 |
| **CAM Young's E** | **150–200 GPa** | oxide CAM | §3.1.1, ref 101/102 |
| **SE Young's E** | **20–30 GPa** | sulfide SE | §3.1.1 |
| 고압 제조 잔류공동 | 370 MPa서도 비-무시 | 3D tomography | §3.1.1, ref 100 (Doux) |
| **stack pressure 변동 (Li–In)** | **~3.8 MPa** | Li–In 셀 (LTO 셀 ~0.2 MPa) | §4.2, ref 120 (**Kang, self-cite**) |
| stack pressure 변동 (LTO) | **~0.2 MPa** | LTO 셀 | §4.2, ref 120 |
| dendrite 단락 전류 | **3.0 mA/cm²** | Li|LPSCl|Li 전압급강하 | Fig 6a, ref 89 |
| **CCD (BH₄ 도핑)** | **7.3 mA/cm²** | 5LBH-LPSCl (baseline 2.6) | §5.1, ref 127 |
| CCD (baseline LPSCl) | **2.6 mA/cm²** | symmetric cell | §5.1, ref 127 |
| 옥시설파이드 σ | **≥2.5 mS/cm** | O-doped 유지 | §5.1, ref 128 |
| 옥시설파이드 ECW 확대 | **ΔV≈0.4 V** (2.5/2.9/4.2 V) | CV C+SE\|SE\|Li | §5.1, Fig 13d, ref 128 |
| **대량합성 σ** | **13 mS/cm @ 1 kg batch** | Li₅.₅PS₄.₅Cl₀.₇₅Br₀.₇₅ | §5.1, ref 136 (Wang) |
| CCD (LiPON 코팅) | **4.1 mA/cm²**, >1000 h @0.5 mA/cm² | Li/SE 계면 | §5.3, ref 149 (Su) |
| 계면저항 (LiPON) | **~1.3 Ω·cm²** | Li/SE | §5.3, ref 149 |
| anode-free 성능 | **>900 mAh/cm³, 1000 cycle** | Ag–C interlayer | §5.3, ref 152 (Lee) |
| CCD (Li₃N–LiF SEI) | **3.3 mA/cm², >1200 h** | 인공 SEI | §5.3, ref 156 (Gao) |
| 후막 목표 | **>5 mAh/cm²** | scalable 복합전극 | §6, refs 159/160 |
| CAM/SE 입자크기 | CAM 5–15 µm / SE 1–5 µm | 불일치 = 공동 원인 | §3.1.1 |
| 액체급 로딩 데모 | **~50 vol% CAM, 거의 완전 용량유지** | 12 µm NCM+1.5 µm SE, cold-press | §3.1.2, ref 106 (Shi) |

---

## 10. Figure / Table set ★ (전 16 그림 + Table 1 — 우리 활용 표시)

| Fig/Table | 내용 (무엇을 보여주나) | 우리가 참고/활용할 점 |
|---|---|---|
| **Fig 1a** | 여러 SE 전기화학창 막대(LiPON/LLZO/LATP/LAGP/LISICON…) vs 전압·μ_Li | **우리 ESW(2.26 V)를 SE landscape에 정렬** (ref 49 = Zhu/He/Mo grand-potential, 우리와 동일 방법) |
| **Fig 1b** | full cell의 **thermodynamic / kinetic / predicted ECW** + 평가 approaches 박스 | **우리 grand-potential(=thermodynamic) vs 실험창(=kinetic) 구분의 정확한 그림** |
| Fig 2a | LPSCl S 2p/P 2p XPS 산화 진화(PSₓ⁻/sulfate) | 산화 분해산물 XPS — 우리 xps_reference_sei.csv 검증축 |
| Fig 2b | ToF-SIMS PO₂⁻/PO₃⁻ fragment 공간분포(cycling) | phosphate 분해종 누적 |
| **Fig 3a** | NCA 고SOC 산소방출 → SE 산화 → rock-salt + LPSCl 산화층 모식 | CAM 산소-SE 반응 인과 도식(deck) |
| **Fig 3b,c** | LPSCl–delithiated NCA pseudo-binary phase diagram + **AIMD 50 ps → LiCl·Li₃PO₄·NiS₂** | **계면 비호환 산물 = 우리 interface_reactivity·Banerjee와 비교**(LiCl/Li₃PO₄ 공통) |
| Fig 4a | carbon 유/무 양극 ToF-SIMS POₓ⁻(carbon이 phosphate↑) | CA가 SE 분해 촉매 |
| **Fig 4b** | **carbon 함량 dilemma** 모식 (저C=활용↓ / 과C=분해↑·Li⁺ 방해) | **[KimCA] 0D/1D 결과의 리뷰 도식** (ref 69=우리그룹) |
| **Fig 5a,b** | LPS S 2p/P 2p XPS, Li 증착 전후(Li₂S/Li₃P/LiCl, reduced P) | 환원 분해산물 — 우리 grand-potential 환원산물(Li₃P+Li₂S+LiCl) 검증 |
| **Fig 5c** | **Nolan Type 1(ideal)/2(MIEC)/3(SEI)** Li/SE 계면 3분류 | **우리 SEI 패시베이션 논리의 표준 프레임**(Type 3로 밀자 = Nd cascade) |
| **Fig 6a-c** | Li|LPSCl|Li 단락(3 mA/cm²) + operando XCT 균열 Li침투 + SEI(ref 89,90) | dendrite가 *환원 SEI* 좌우 = bulk σ_e 한계 |
| **Fig 7a,b** | 복합양극 공동 형성(입자불일치·force concentration) + 가압별 porosity/contact/용량 | 공동→접촉불균일→전류국소화 |
| **Fig 8a,b** | 접촉손실 용량감소 + **300 MPa re-press 회복** + 저항 급증/회복 | 접촉손실 가역성(기계 문제) |
| **Fig 9a-c** | NCM 균열 3D tomography + Li농도/입계손상 + **단결정 vs 다결정** | 단결정=기계해법 |
| Fig 10a-c | Li stripping void 핵생성·합체 + occluded void 악순환 + Li/LPSCl SEM | 음극 void→접촉손실→전류증폭 |
| **Fig 11a-c** | NCM:SE비별 stress map + FIB-SEM 균열망 + **phase-field case1(불균일)/case2(균일)** strain/stress/crack | **화학→기계: 불균일이 균열 핵생성**(Fig11c ref 39=우리그룹) |
| **Fig 12a-d** | Li–In(~3.8 MPa) vs LTO(~0.2 MPa) 압력변동 + XPS 저항종 + SEM 입계균열 + 모식 | **기계→화학: stack pressure 변동이 양극 분해 가속**(ref 120=Kang) |
| **Fig 13a-e** | BH₄ CCD 7.3 + tri-layer SEI + **Li₆PS₄OCl 구조** + **CV ECW 확대** + Li₃PO₄ buffer | **우리 O-doping/Nd cascade·ESW·doping cascade의 직접 동기** (refs 127,128) |
| **Fig 14a-e** | NCM@LZC + 코팅 계면 + 용량유지 + **ALD LNO-NCM811** + operando Co XANES | LNO-NCM = [KimCA] 양극; 코팅으로 TM환원 억제 |
| **Fig 15a,b** | LiPON 코팅 Li 계면(접촉↑) + **Ag–C interlayer** 균일 Li | 음극 e⁻-절연 interphase = 우리 Li₃N family |
| **Fig 16** | **electrochemo-mechanical coupling 고리 + 3대 완화전략 한 장** | **deck "우리 그룹 세계관" 1슬라이드 — 가장 중요** |
| **Table 1** | **열화 메커니즘 × 기원 × 결과 × 완화전략 마스터 매트릭스** (아래 §11) | **리뷰 전체의 1페이지 요약 — 우리 작업 매핑용** |

---

## 11. Table 1 전사 — **열화 메커니즘 마스터 매트릭스** (리뷰의 1페이지 핵심)

| 열화 메커니즘 | 주요 기계론적 기원 | 결과적 열화 현상 | 완화전략 |
|---|---|---|---|
| **양극 계면 heterogeneity** | 황화물 SE **산화 분해** | interphase 내 heterogeneity; 취성상 균열/debonding; 전기/이온 전도경로 손실; 불균일 전기화학 반응 | **SE 조성 튜닝; CAM 표면 코팅** |
| **미세구조 불균일 / 양극 계면** | SE·CAM 입자 **불균일 분포** | 불균일 volumetric strain·von Mises stress; 계면 debonding / CAM 균열 | **미세구조 최적화; 입자크기 제어** |
| **음극/SE heterogeneity** | 황화물 SE **환원 분해** | interphase heterogeneity; 불균일 전기화학 반응; 국소 응력축적; dendrite 침투 | **음극/SE에 인공 SEI/interphase** |
| **전극 간 응력 전달** | 고변형 음극 **부피변화** | 구조 피로; CAM 균열; 전기/이온 전도경로 손실; 불균일 전기화학 반응 | **저변형 음극; stack pressure 최적화** |
| **동적 계면 진화** | 입자접촉 **반복 형성·파괴** | 접촉손실; 국소 응력축적 | **CAM 표면 코팅; mechanically compliant 계면** |

> 🔑 이 표가 곧 **우리 그룹의 "해야 할 일 목록"**. 우리 DFT는 1행(산화분해→SE조성튜닝/코팅)·3행(환원분해→인공SEI)·일부 2행(SQS 무질서)에 직접 기여한다.

---

## 12. DFT / 계산 콘텐츠 ★ (리뷰가 인용한 계산 — 우리 방법과 직결)

리뷰는 **자체 계산 없음**이나(리뷰형), 인용된 계산 작업이 우리 방법론과 맞물림:

- **Fig 1a ECW (ref 49 Zhu/He/Mo 2015)**: grand-potential phase-stability 전기화학창 = **우리 esw_grand_potential.py와 동일 방법**(get_element_profile). 우리 comp1 onset 2.256 V가 이 막대그래프 줄에 정렬.
- **Fig 1b thermodynamic/kinetic ECW (ref 50)**: 우리 grand-potential(thermodynamic)과 실험창(kinetic passivation)의 차이 프레임 — 우리 ESW가 실험보다 낮은 이유의 그림.
- **Fig 3b,c Banerjee AIMD (ref 51)**: LPSCl–NCA 계면 **AIMD 50 ps** → LiCl/Li₃PO₄/NiS₂ 자발형성. 우리 interface_reactivity.py(GrandPotentialInterfacialReactivity)·sei_products.json의 계면 산물 예측과 **같은 종류·일부 같은 산물**(LiCl, Li₃PO₄).
- **§2.1.1 Cao XAS+DFT (ref 54)**: 산화 분해 = "Li의 S affinity 감소 → S–S 결합 → PS₄→PS₃ 붕괴" — 우리 ICOHP/bonds·CDD(전하재분배)·국소배위 논의와 연결.
- **Fig 6c Hao 계산 (ref 90)**: Li⁰ 증착 에너지·ionization → dendrite 핵생성은 *부분환원 SEI*가 좌우 → 우리 SEI 전자구조(sei_products.json gap) 강조.
- **Fig 11c phase-field (ref 39 = 우리그룹 Kim/Park/Lee)**: 구조 불균일→불균일 strain/von Mises stress/crack order. **우리 무질서(SQS) 거시판** — chemo-mechanical 모델링.
- **§3.1.3 균열 계산 (ref 111)**: 불균일 delithiation서 수 GPa 응력 → CAM 항복 초과. 우리 elastic(C_ij·E·B·G)이 SE 측 응력 수용을 다룸.
- **인용 계산 그룹/방법**: grand-potential ESW·계면반응(Ceder/Mo 계열), AIMD 계면(Banerjee/Meng), phase-field/FEM(우리 그룹 + ref 39 등), XAS+DFT(Cao). → **우리 DFT(grand-potential ESW + elastic/EOS + AIMD 확산 + cascade 스크리닝)는 리뷰가 인용한 계산 종류의 *argyrodite 조성-해상도 정밀판*.**

---

## 13. 우리 연구와의 연결 ★★★ — **comparison_vs_ours.md `[Kang]` 등록 + repo 작업 매핑**

> 이 절이 사용자가 명시 요청한 "dedicated connection to OUR work". 리뷰의 프레임이 우리 계산을 **validate / contextualize**하는 지점과, **우리 DFT가 리뷰 내러티브에 *더하는* 것**을 분리.

### 13.1 리뷰가 우리 작업을 **정당화/맥락화(validate)**하는 지점

| 우리 repo 작업 (파일) | 리뷰의 어느 부분이 validate/contextualize | 관계 |
|---|---|---|
| **ESW / grand-potential 산화창** (`db/properties/oxidation_stability.json`, comp1/modelc onset 2.256 V) | §2.1.1 + Fig 1a (산화 ~2.0–2.5 V, ref 49 동일 방법) + Fig 1b (thermo vs kinetic ECW) | **✓ 같은 방법·같은 band**. 우리 2.256 V = 리뷰 Fig 1a 막대의 argyrodite 줄. "왜 실험창이 넓나"=Fig 1b kinetic passivation |
| **환원 분해산물** (grand-potential 0 V → Li₃P+Li₂S+LiCl) | §2.2.1 Fig 5a-c (Li₂S/Li₃P/LiCl, ref 81) + Nolan Type 1/2/3 | **✓ 동일 chemistry**. 우리가 Type 3(전자절연 SEI)로 미는 게 목표 |
| **SEI 산물 band gap** (`db/properties/sei_products.json`: LiCl 6.65, Li₃PO₄ 5.73, Li₂O 5.24, NdPO₄ 5.55 vs Li₃P 0.70, Li₂S 3.90) | §2.2.1 Fig 5c Type 분류 + §5.1(b) O-doping "reduced electron leakage" + §5.3 인공SEI(Li₃N/LiF) | **✓ 정량판**. 리뷰의 "전자절연 interphase가 passivation 관건"을 우리가 gap 수치로 분류(insulator≥4/conductor<2) |
| **Nd2O3 / O-doping 옥시설파이드** (`db/properties/sei_products.json`, oxidation_stability.json nd_doped, eos modelc_nd_doped B0=18.9) | **§5.1(b) Fig 13c,d** (Li₆.₂₅PS₄.₂₅Cl₀.₇₅ 옥시설파이드, 전자누출↓·ECW 확대·O–P>S–P) + **§5.1(c)** Li₃PO₄ buffer | **✓✓ 직접 표적**. 우리 Nd cascade = 리뷰가 추천한 O-doping 전략의 atomistic 구현. O-derived Li₃PO₄/Li₂O/NdPO₄가 conductive Li₃P 대체 = 리뷰 "reduced electron leakage" |
| **XPS SEI reference** (`db/properties/xps_reference_sei.csv`) | §2.1 Fig 2a + §2.2.1 Fig 5a,b (S 2p/P 2p XPS 분해산물) | **✓ 검증축**. 리뷰가 인용한 XPS 분해종(PS₄ 161.6 / Li₂S 160.2 / Li₃PO₄ 133.3 / LiCl 198.6)의 BE 기준 — 우리 ORCA dSCF 검증 앵커 |
| **doping cascade v23** (`cascade_v23_*.csv`, 47 dopant 기계+안정성 스크리닝) | §5.1 (SE 도핑이 ECW·기계·SEI 동시 튜닝) + §6 트렌드3("한 변수 바꾸면 다른 변수 바뀜") | **✓✓ 방법 일치**. 우리 cascade의 "stability↔Li-mobility blocking trade-off"가 곧 리뷰의 "modifying one parameter alters others" |
| **elastic / EOS** (`elastic.json` E_VRH·B/G·vacancy paradox, `eos.json` B0 comp1 26.2/modelc 21.7) | §3.1.1 (sulfide E 20–30 GPa, 연성으로 소성변형 수용) + §3.1.3 (SE가 CAM 응력 수용) | **✓ landscape 정렬**. 우리 E_VRH·B/G = 리뷰의 "soft, plastically deformable SE" 줄. 단 절대값 functional/정의 의존 |

### 13.2 우리 DFT가 리뷰 내러티브에 **더하는 것 (our contribution beyond the review)**

리뷰는 argyrodite를 **Li₆PS₅X 일반**으로만 다루고 **Cl-rich(LPSCl1.5/1.6) vs LPSCl 비교를 따로 하지 않으며**, 모든 수치가 2차 인용이다. 우리 DFT가 *그 너머* 주는 것:

1. **조성-해상도 ESW**: 리뷰는 "argyrodite 산화 ~2.0–2.5 V"로 뭉뚱그리나, 우리는 **comp1 vs modelc onset이 *동일* 2.256 V (S²⁻-limited)** 임을 grand-potential로 분리 — Cl은 onset이 아니라 *분해 양·산물*(더 많은 LiCl)에 작용. → 리뷰 §2.1.1의 "조성·결합특성이 산화안정성 좌우"를 **Cl 자유도로 정량 분해**.
2. **vacancy paradox (DFT 한계의 정직한 노출)**: 리뷰는 "sulfide E 20–30 GPa·연성"으로만 말하나, 우리는 **DFT 0K에서 comp1≈modelc E_VRH(52.3 GPa 동일)** = DFT가 실험적 Cl-rich 강성을 못 잡음을 발견 → 리뷰가 추상화한 "기계물성"의 *방법 의존성*을 우리가 명시(finite-T phonon·Li 동적 재분배 필요). → 리뷰 §3을 *비판적으로 보강*.
3. **SEI 산물 전자절연성의 정량 분류**: 리뷰 Fig 5c는 Type 1/2/3을 *개념*으로 주나, 우리 sei_products.json은 **각 산물 gap을 수치화**(insulator/marginal/conductor 임계) → "어떤 도핑이 conductive Li₃P를 wide-gap Li₂O/Li₃PO₄로 바꾸나"를 *예측·스크리닝 가능*하게 함. → 리뷰의 정성 프레임을 *설계 도구*로.
4. **Nd2O3 cascade의 직접 hull staircase**: 리뷰는 O-doping을 "전자누출↓"로 일반 서술하나, 우리는 **6원소(Cl-Li-Nd-O-P-S) hull에서 전압별 분해 staircase**를 직접 계산 — 양극(>2.45 V NdPO₄/NdCl₃ wide-gap) vs 음극(0 V Li₂O+Li₃P 부분치환) 분리, **intrinsic 창은 오히려 좁아짐**(passivation은 kinetic이지 thermodynamic 아님)까지 정직하게. → 리뷰 §5.1(b)를 *조성-구체·전압-분해능*으로 실증.

### 13.3 정직한 한계 — 우리 DFT가 *못 잡는* 리뷰의 핵심

리뷰의 thesis 자체(**electrochemo-mechanical *coupling*, 되먹임 고리**)는 **우리 정적 bulk DFT의 사정권 밖**이다:
- **§4 동적 응력↔반응 coupling**: 우리는 화학(분해산물)과 기계(elastic) 각각은 줄 수 있으나, **"응력이 반응을 가속하고 반응이 균열을 만드는 시간발전 되먹임"** 은 phase-field/FEM(ref 39·우리그룹) 영역.
- **§3 미세구조·접촉손실·공동·dendrite**: 전부 device/microstructure 스케일 → 우리 bulk 단결정 DFT/AIMD 밖 ([KimICCF] GeoDict / phase-field가 다리).
- **heterogeneity**(리뷰의 진짜 적): 우리 SQS는 *통계적* 무질서는 잡으나 *공간적 reaction/stress heterogeneity*는 못 잡음.
> → **deck 프레이밍**: "우리 DFT = 리뷰 coupling 고리의 *두 끝점*(전기화학 분해 화학 + bulk 기계물성)을 atomistic으로 고정하는 닻. 고리의 *동역학*은 우리 그룹의 phase-field/FEM(ref 39·120)과 operando 실험이 잇는다. 셋을 합치면 리뷰가 부른 multi-scale 통합 설계가 완성."

---

## 14. 인용 가능 문장 (deck/paper용)

- "Our own group's review (Kang, Shin, Lee & Lee, *Chem. Commun.* 2026) frames the central problem of sulfide ASSBs as an **electrochemo-mechanical feedback loop** — reaction-induced fragility → fracture → fresh-surface re-reaction — so that interfacial stability is **not chemical passivation *or* mechanical reinforcement, but both simultaneously**."
- "The review localizes the real culprit not in decomposition or stress *per se* but in their **spatial heterogeneity**; our SQS/disorder treatment and grand-potential decomposition give the atomistic counterpart, while the group's phase-field work (ref 39) supplies the meso-scale heterogeneity that triggers crack nucleation."
- "Among the review's three mitigation axes — **SE doping, CAM coating, anode engineering** — our DFT directly serves the first: oxysulfide (O²⁻) doping toward a wide-gap, electron-blocking interphase (Li₃PO₄ 5.7 eV, Li₂O 5.2 eV replacing conductive Li₃P 0.7 eV) is exactly the §5.1 strategy, made composition- and voltage-resolved by our Nd₂O₃ cascade and ESW staircase."
- "The review places argyrodite oxidation at ~2.0–2.5 V vs Li⁺/Li (grand-potential, ref 49); our same-method onset of 2.256 V for both Li₆PS₅Cl and Li₅.₄PS₄.₄Cl₁.₆ refines this to show **Cl acts on the decomposition *products* (more inert LiCl), not the thermodynamic onset (S²⁻-limited, composition-invariant)**."
- "Nolan's Type 1/2/3 Li/SE interphase classification (review Fig 5c) is the conceptual frame; our `sei_products.json` band-gap thresholds (insulator ≥4 eV / conductor <2 eV) turn it into a **predictive screening tool** for pushing the SEI into the passivating Type-3/Type-1 regime."

---

## 15. 주의 / 한계 (over-claim 방지 · 비판적)

- **리뷰형 = 전부 2차 인용**: 자체 신규 데이터 없음(Data availability 명시). 모든 수치는 원전 조건 의존 → 단일 숫자 인용보다 "~2.0–2.5 V band"처럼 범위로. 절대 비교 시 원전(ref 49·51·81·127·128 등) 확인.
- **우리 DFT는 coupling을 *못 본다***: 이 리뷰의 *핵심*(되먹임 고리·heterogeneity)은 phase-field/FEM/operando 영역. 우리 grand-potential ESW·elastic을 "chemo-mechanical coupling을 풀었다"고 **절대 말하지 말 것** — 우리는 고리의 *끝점*(분해 화학 + bulk 기계물성)만 닻을 내린다.
- **Cl-rich 비교는 리뷰에 없음**: 리뷰는 argyrodite를 Li₆PS₅X 일반으로만. 우리 comp1 vs modelc 비교는 리뷰 너머의 *우리 기여*지, 리뷰가 뒷받침하는 게 아님(혼동 금지).
- **기계물성 vacancy paradox**: 리뷰의 "sulfide E 20–30 GPa·연성"과 우리 DFT 0K E_VRH(52.3 GPa, comp1≈modelc)는 *정의/방법*이 다름(clamped-ion harmonic vs 실험 다결정). 연성(B/G) 결론만 robust, 절대 E 직접비교 금지.
- **O-doping 이점은 kinetic**: 리뷰 §5.1(b)는 O-doping을 "전자누출↓·ECW 확대"로 *긍정* 서술하나, 우리 Nd hull staircase는 **intrinsic 창이 오히려 좁아짐**(passivation은 산물 전자절연=kinetic, thermodynamic 창 확대 아님)을 보임 → 리뷰의 "ECW 확대(CV 관찰)"와 우리 "intrinsic 창 narrows"는 *다른 축*(kinetic vs thermodynamic)이니 둘 다 맞음. 명명 필수.
- **band gap PBE 과소**: 우리 comp1 2.066 eV는 PBE 과소평가·무질서·Γ-only로 ±0.2–0.3 scatter. 리뷰의 "wide-gap"과 "wide-gap insulator" 수준만 일치, 절대 gap 비교 금지.
- **self-citation 밀도 높음**: refs 31·39·40·56·67·68·69·70·73·120 등 다수가 Jong-Won Lee 그룹 자기인용 — 리뷰의 강조점이 *우리 그룹 강점*(phase-field 39, stack pressure 120, CA 차원 69, calendar/계면 등)에 편향됨을 인지(이게 곧 우리 연구 방향이라는 점에선 오히려 유용).
- **음극 환원 전위 절대값**: 리뷰 ~1.7 V vs 우리 grand-potential 1.24 V — 방법차(우리 0-pressure direct vs 리뷰 인용 indirect/실험). chemistry(Li₃P+Li₂S+LiCl)는 동일, 전위 절대값은 직접비교 주의.

---

## 16. 기법 / 용어 미니사전

- **electrochemo-mechanical degradation**: 전기화학 분해와 기계 불안정이 *서로 유발·가속*하는 결합 열화. 이 리뷰의 주인공.
- **feedback loop (되먹임 고리)**: 분해→취약화→파괴→새표면노출→재분해의 self-amplifying 순환. §4 핵심.
- **heterogeneity**: 반응·응력의 *공간적 불균일*. 리뷰가 지목한 진짜 적("not decomposition or stress itself but their heterogeneities").
- **ECW (electrochemical window)**: SE가 분해 없이 견디는 전압창. **thermodynamic ECW**(=우리 grand-potential, 좁음) vs **kinetic ECW**(=passivation 포함 관찰창, 넓음) 구분(Fig 1b).
- **TPB (triple-phase boundary)**: CAM+SE+CA 3상 접점. carbon이 SE로 전자 누출해 분해 촉진하는 가장 취약점(§2.1.3).
- **MIEC (mixed ionic-electronic conductor)**: 이온·전자 동시전도 interphase. 전자누출 지속 → SEI 계속 성장(Nolan Type 2, LGPS).
- **Nolan Type 1/2/3**: Li/SE 계면 분류 — 1=열역학안정 passivating(Li-binary), 2=MIEC 성장형(나쁨), 3=전자절연 kinetic passivating SEI(LPSCl, 목표). Fig 5c.
- **CEI / SEI**: cathode / solid electrolyte interphase. 양극·음극 계면 분해층.
- **CCD (critical current density)**: dendrite 단락 없이 견디는 최대 전류밀도. 높을수록 좋음(목표 >1–3 mA/cm²).
- **stack pressure**: ASSB 셀에 가하는 외부 압력. 고변형 음극(Li–In)이 cycling 중 변동(~3.8 MPa) → 양극 교란(§4.2).
- **anode-free / Ag–C interlayer**: Li 무여분, 충전 시 양극 Li가 음극에 증착. Ag가 lithiophilic 핵생성, C가 scaffold(Fig 15b).
- **옥시설파이드 (oxysulfide, O-doped sulfide)**: PS₄³⁻ 일부를 PO₄로 치환(Li₆PS₄OCl류). O–P>S–P 결합으로 ECW·대기내성↑, 전자누출↓(§5.1b). **우리 Nd2O3/O-doping 표적.**
- **chemo-mechanical coupling (cathode)**: CAM 부피변화 → SE microgap/균열 → 접촉손실·재반응. 연성 SE(황화물)가 수용 유리하나 cycling서 한계.
- **phase-field / FEM**: 미세구조 strain/stress/crack 시간발전 모델링. 리뷰 Fig 11c(ref 39=우리그룹)·Fig 3b 등. 우리 DFT가 *못 보는* coupling 동역학을 잇는 다리.
- **Feature Article**: Chem. Commun.의 초청 리뷰형 논문(저자 연구 중심으로 분야 조망). 자기인용 밀도 높음이 정상.

# AI를 활용한 전극 미세구조 디지털화 기술과 물리 기반 배터리 시뮬레이션 — 이용민 (연세대 DTBL)

> slug `lee2026_yonsei_dtbl_ai_electrode_digitaltwin` · type `talk` · **사용자 분류 폴더 `(미분류)`** ·
> 발표 2026-08-21 (**2026 Korean Battery Symposium** / 2026년도 전지기술 심포지엄) ·
> 발표자 **YONG MIN LEE (이용민)**, **Digital Twin Battery Laboratory (DTBL)**,
> Dept. of Chemical and Biomolecular Engineering · Dept. of Battery Engineering (Graduate),
> **Yonsei University** (yongmin@yonsei.ac.kr · http://batterylab.yonsei.ac.kr) ·
> PDF 20 pp (자료집 pp. **259–278**, 2-up 인쇄) · **인쇄 슬라이드 39장** (덱 표기는 `/44`) ·
> 원본 파일 `litdb/inbox/이용민 교수님.pdf` (Print-To-PDF 이미지 전용 = 텍스트 레이어 0, **전 페이지 이미지 판독**) ·
> digested 2026-08-03 · status ✅ (덱), ⏳ 구술 txt 미보유
>
> ⚠ **덱 인용 규율**: `litdb/talks/README.md` 참조. **이 덱의 결과는 거의 전부 이미 `papers/` 에 정본이 있다** —
> `park2020_digitaltwin_assb_foundational.md` (AEM 10, 2001563) · `kim2024_digital_twin_acsenergyletters.md`
> (ACS EL 9, 5225) · `lim2025_virtual_calendering_framework.md` (Small 21, 2410485) ·
> `song2025_electrochemo_mechanical_microelectrode_ees.md` (EES 18, 3129).
> **덱과 논문이 충돌하면 논문이 이긴다.** 덱 고유 정보는 §8(2nd solvent/DEM 슬러리)·§10(challenges)·§11 뿐이다.
> ⚠ **이 덱은 우리 캠페인의 DFT 축이 아니라 DEM/미세구조 축**이다 → 물성 4축 비교표(`comparison_vs_ours.md` A–F)
> 에 수치로 넣지 않는다. 대조는 `comparison_vs_ours_DEM.md`.

---

## 1. 한 줄 요약

**"1D/P2D의 *평균 파라미터*가 배터리 물성을 가려왔다(Blinded Scale·Blinded Parameters) — 3D 미세구조
디지털트윈으로 그 가림을 걷되, 지금 그 길을 막는 것은 ① 이미지 처리 노동 ② 미시 파라미터 측정 ③ 계산량이며,
그 셋을 **AI로** 뚫겠다"** 가 전체 서사.
5부 구성: **①왜 디지털트윈 ②구조획득(재구성, top-down) ③구조생성(generation, bottom-up)+검증
④제조공정 시뮬(mixing→coating→drying→calendering) ⑤남은 과제(양방향·실시간)**.

**우리와의 관계**: `lee2026_skku`(MLIP·원자스케일 = *정면 경쟁*)와 달리 이 덱은 **우리 DEM+MPM 축 그 자체**다.
계보상 우리 프로그램의 **상류 정본 그룹**(`INDEX.md` §🏛️ 디지털트윈 전극 계보)이며, 이 덱은 그 계보의
**2026년 자기 요약본 + 자기 한계 목록**이다. → 우리 positioning(`positioning_vs_geodict.md`)을
그들 스스로의 언어로 다시 확인해주는 문서.

---

## 2. 덱 구조 (PDF 페이지 → 슬라이드 → 내용)

2-up 인쇄라 **PDF p → 슬라이드 2장**. 섹션 표지에만 `n/44` 번호가 보이고(3·10·17·25), 본문 슬라이드는
번호가 인쇄되지 않는다. 인쇄된 슬라이드는 39장 = **덱 44장 중 최소 1장이 인쇄에서 빠졌다**(§13-1).

| PDF p. | 자료집 p. | 슬라이드 | 내용 |
|---|---|---|---|
| 1 | 259 | 1 / 2(2/44) | 표지 / **Outline 5부** |
| 2 | 260 | **3/44** / 4 | [섹션1] Why DT / **From Particle to Pack** (4 스케일 × 자사 논문) |
| 3 | 261 | 5 / 6 | **Why DT ①** 1D/P2D vs 3D·**Parameter/Governing Eq./Geometry 3구** / **Why DT ② "Blinded Scale"·"Blinded Parameters"** |
| 4 | 262 | 7 / 8 | **ACS Energy Lett. 리뷰**(supplementary cover) / **How to Create DT Structures** (top-down ↔ bottom-up) |
| 5 | 263 | **10/44** / 11 | [섹션2] 3D Reconstruction / **Overview: 현행 3대 한계** |
| 6 | 264 | 12 / 13 | Domain volume × voxel size 지도(FIB-SEM vs XCT) / **3D 재구성 절차(FIB-SEM, voxel 100 nm, 100회 반복)** |
| 7 | 265 | 14 / 15 | **Labor-intensive segmentation**(BSE/SE/watershed/ground-truth) / **XCT 저해상도** |
| 8 | 266 | 16 / **17/44** | **AI-assisted 이미지처리**(AI segmentation + super-resolution) / [섹션3] Generation & Validation |
| 9 | 267 | 18 / 19 | **★ ASSE 설계 파라미터 + 생성 규칙**(=park2020) / **★ voxel·domain 수렴 + 계산비용** |
| 10 | 268 | 20 / 21 | Structural information(AM/SE/CA 분해, 50 µm³·voxel 0.50 µm) / **검증: C-rate별 전압곡선·리튬화 맵** |
| 11 | 269 | 22 / 23 | **Limitation I: 측정 중 구조 왜곡**(공기·열) / **AI 2D→3D 확장(GAN)** |
| 12 | 270 | 24 / **25/44** | **Limitation II: 미시 파라미터 측정**(단일입자·마이크로전극·접촉불안정) / [섹션4] 제조공정 시뮬 |
| 13 | 271 | 26 / 27 | 제조공정 디지털트윈의 의미(Ayerbe/Franco) / **현황: Mixing·Coating·Drying** |
| 14 | 272 | 28 / 29 | **현황: Pressing·Electrolyte infiltration** / **캘린더링 공정 개관**(=lim2025) |
| 15 | 273 | 30 / 31 | **★ 가상 캘린더링 검증(밀도 2.3–4.0 sweep)** / **★ PNM + 응력분포·crackable volume** |
| 16 | 274 | 32 / 33 | **★ CBD migration + 2nd solvent 억제** / **★ OWRK 표면에너지·work of adhesion** |
| 17 | 275 | 34 / 35 | **★★ DEM 기반 슬러리 믹싱 시뮬** / 공정모델 한계: 계산량 |
| 18 | 276 | 36 / 37 | **Physics-Embedded AI(하이브리드)** / **Summary: 3한계 → 3 AI 해법** |
| 19 | 277 | 38 / 39 | **ARTISTIC 프로젝트**(Franco) / **★ Goal: 양방향·실시간 — 4대 과제** |
| 20 | 278 | 40 | Thank you (하단 절반 공백) |

---

## 3. 서사 축 ① — "왜 디지털트윈인가" (p.3 슬 5–6)

### 3a. 디지털트윈 모델의 3구성 (슬 5)
```
Parameter (material property)  +  Governing Equation (physics)  +  Geometry (microstructure)
```
1D/P2D는 `Geometry`를 평균으로 뭉개므로 → **국소 문제를 못 본다 / 평균 파라미터를 쓸 수밖에 없다**.
3D 디지털트윈은 그 둘을 되찾아 **Simulation Reliability↑**.

> 🔑 이 3구 분해가 **우리 repo의 DFT(Parameter) ↔ DEM/MPM(Geometry) ↔ PyBaMM/Kirchhoff(Governing Eq.)
> 분업을 그대로 서술한다.** 발표·원고 서론에 그대로 쓸 수 있는 프레임.

### 3b. "Blinded Scale" / "Blinded Parameters" (슬 6) ★ 이 덱 최고의 한 장
```
Atomic Scale (LLZO 분자구조)  →  [Blinded Scale]  →  Macro Scale (cell)
      Electrochem 2, 390–414 (2021)                 Nano Energy 79, 10545 (2021)
```
- **이온전도도**: **소재 물성 5.4 × 10⁻⁴ S/cm** → **셀 내부(전극) 물성 7.9 × 10⁻⁷ S/cm**
  = **약 3자릿수 강하**. 슬라이드 문구 *"To fill the gap b/w materials and devices (or systems)"*.
- 두 번째 층: 입자 그림에서 뽑아야 할 **유효 파라미터**들 — 활성표면적 `a`, 굴곡도 `τ`,
  유효확산 `D_eff`, 유효이온전도 `σ_Li⁺,eff`, 유효전자전도 `σ_e⁻,eff` → **"Blinded Parameters"**
  → 전기화학 해석(Butler–Volmer, Ohm, Fick, 질량/전하 보존).

> 🔑🔑 **우리에게 직결**: 이게 바로 우리 `σ 삼중항`(σ_ionic/σ_e/σ_thermal)이 채우는 칸이고,
> **"소재 σ ≠ 전극 σ"** 라는 우리 규율(문헌 σ와 우리 σ_eff를 같은 표에 넣지 않기)의 그룹 자체 근거다.
> ⚠ 단 **5.4e-4 / 7.9e-7 은 LLZO(산화물) 계열 인용값**이고 우리 LPSCl 수치가 아니다 — *비율·논리만* 쓰고
> 절대값은 우리 표에 넣지 않는다. 인용 표기(`Nano Energy 79, 10545`)도 자릿수가 의심스럽다(§13-4).

---

## 4. 서사 축 ② — 구조를 얻는 두 길 (p.2 슬 4, p.4 슬 7–8)

### 4a. Particle → Pack 4 스케일 (슬 4) — 그룹 자체 논문 지도
| 스케일 | 크기 | 덱이 붙인 자사 논문 |
|---|---|---|
| Particle | nm ~ µm | **Adv. Energy Mater. 13 (2023) 2204328** · **Nat. Commun., *Under Review*** (Y.M.Lee, S.-Y.Lee) |
| Electrode / Separator | µm ~ mm | **Small 21 (2025) 2410485** · **Nat. Commun. 15 (2024) 10134** |
| Cell | mm ~ m | **J. Energy Chem. 105 (2025) 87–95** (원통형 ⌀10.5 × 70 mm) |
| Module / Pack | ~ m | **eTransportation 22 (2024) 100370** |

제조 체인 축(하단): `MIXING → COATING → CALENDERING → CUTTING → STACKING → FILLING → FORMATION`
(*Adv. Energy Mater.* 12 (2022) 2102696).

> ⚠ **미보유 4편**: Nat. Commun. 15 (2024) 10134 · Nat. Commun. *Under Review* · J. Energy Chem. 105 (2025) 87–95 ·
> eTransportation 22 (2024) 100370. §15 위시리스트.

### 4b. Top-down ↔ Bottom-up (슬 8) — positioning의 원문
```
Top-down (Reconstruction)                Bottom-up (Generation)
XCT / FIB-SEM / TEM tomo / APT   ──►  [Reliable Structure]  ◄──  Structural Information
                                       (design parameters)        (composition/density/loading)
```
가운데 **설계 변수 5종**: particle size & shape · coating thickness · electrode mass loading ·
electrode density · composition. 출력: morphology(shape, crack) + **집전체 거리별 분포**(NMC/pores/CBD/cracks).
Bottom-up 쪽엔 **검증(1C/2C/4C/8C 전압곡선 exp vs sim)** 과 **LPSCl+NCM 70 wt% 모델 박스**가 붙어 있다.
출처: **S. Kim, Y. M. Lee\* et al., ACS Energy Lett. 9 (2024) 5225-5239**.

> 🔑 **우리 positioning 문장의 peer-reviewed 원문이 이 슬라이드의 출처다** —
> `papers/kim2024_digital_twin_acsenergyletters.md` 정본. 우리 = **bottom-up(공정 물리로 구조를 *예측*)**,
> GeoDict 계열 = **top-down 재구성 + 규칙 배치**. 덱은 이 구분을 다시 확인해줄 뿐 새 근거가 아니다.

### 4c. ACS EL 리뷰 표지 슬라이드 (슬 7) — "Unraveling Hidden Parameters"
4열: **Structural**(contact area, percolation pathway) · **Electrochemical**(Li concentration, ionic flux) ·
**Mechanical**(stress, strain) · **Thermal**(붉은 점선 빈 칸).

> ⚠ **Thermal 칸이 비어 있는 것은 "그 그룹이 열을 안 한다"는 증거가 아니다**(talks/README 규율 #3 —
> 덱은 부재의 증거가 아님; 발표 시점 그림 구성일 뿐). **다만 우리 σ 삼중항이 `σ_thermal`을 포함한다**는
> 사실은 그와 무관하게 유효하며, 부재 주장을 하려면 `papers/kim2024_...` 실물로만 해야 한다.

---

## 5. 3D 재구성(top-down)의 실제와 병목 (p.5–8 슬 11–16)

### 5a. 현행 3대 한계 (슬 11) ★ 이 덱의 문제 정의
| 단계 | 대표 그림 출처 | 한계 |
|---|---|---|
| **Structural Characterization** | Small 21 (2025) 2410485 | **Labor-intensive Image Processing** — 저해상도·watershed 분할. *시간·인력 부담↑ / watershed 특성에서 오는 불확실성 / 구조별 적용성 제한* (그림 제공: **Math2Market**) |
| **Structure Formation & Performance Analysis** | EES 18 (2025) 3129-3147 | **Model Validation** — 미세구조 생성·검증에 필요한 *파라미터와 거동을 얻기 어렵다*(단일입자·마이크로전극) |
| **Design & Process Optimization** | ACS EL 9 (2024) 5225-5239 | **Limited Bidirectional Feedback Loop** — 물리↔디지털 *실시간 통신 제한*(높은 계산부하로 속도 낮음). (Renew. Sustain. Energy Rev. 179 (2023) 113280) |

### 5b. 이미징 기법의 자리 (슬 12–15)
- **domain volume × voxel size 지도**: APT ≪ TEM tomography < FIB tomography < nano X-ray CT < X-ray CT.
- **FIB-SEM**: 고해상도 / 작은 domain / **구조 왜곡(열 손상)**.
- **XCT**: 비파괴 / 큰 domain / **저해상도**.
- 3D 재구성 절차(슬 13): **voxel 100 nm**, **FIB-SEM 토모그래피 100회 반복**, tomography ↔ digital twinning
  분할 이미지 대조 (**J. Song, Y. M. Lee\*, Adv. Energy Mater. 2204328 (2023)**).
- 분할 노동(슬 14): **BSE 기반**(배경 입자 검출) vs **SE 기반**(표면 디테일, 조성 민감도 없음) → *같은 영역이
  다르게 분할*; watershed도 **여전히 오분할**; **ground truth(수동 분할)조차 mislabeling 가능성**
  (J. Li, X. Yu, *Appl. Phys. Lett.* 125 (2024) 173902).
- XCT(슬 15): raw XCT / raw FIB-SEMt / optimal-threshold 분할 / FIB-SEMt 기준 비교
  (S. Thiele, *Sci. Rep.* 6 (2016) 30109) + **Y. M. Lee\*, *In preparation***.

### 5c. AI 해법 (슬 16) — 이 덱 제목의 "AI"
- **Segmentation**: FIB-SEM 이미지 → **clustering**(모호한 경계/유사 grayscale 전처리, optional) → **labeling**
  → **AI segmentation** ("fast segmentation"). 도구: **GeoDict Import & Image Processing, Math2Market**.
- **Super-resolution**: **SRCNN** / **RED-NET**(encoder–decoder + skip) — 저해상도 → 해상도 향상
  (**M. Kodama, *Energy and AI* 14 (2023) 100305**; S. J. Cooper, *ACS Energy Lett.* 7 (2022) 4368-4378).

---

## 6. 구조 생성(bottom-up) + 검증 (p.9–10 슬 18–21) ★★ park2020 정본과 완전 일치

### 6a. ASSE 설계 파라미터 (슬 18) — **덱↔논문 대조 결과 전값 일치**
| 항목 | 덱 표기 | `papers/park2020_...` 정본 | 판정 |
|---|---|---|---|
| Active material | LiNi₀.₇Co₀.₁₅Mn₀.₁₅O₂–LiNbO₃ (**NCM711**), **4.44 g cm⁻³** | LiNbO₃-coated NCM711, 4.44 | ✅ |
| Solid electrolyte | Li₆PS₅Cl (**LPSCl**), **2.07 g cm⁻³** | 2.07 | ✅ |
| Binder | NBR, **1.00 g cm⁻³** | 1.00 | ✅ |
| Loading | **10 mg cm⁻²** | 10 | ✅ |
| Porosity | **12.0 / 19.3 / 28.2 %** (활물질 자체 porosity **32.7 %**) | 12.0/19.3/28.2, 32.7 | ✅ |
| 온도 | **30 °C (303.15 K)** | 30 °C | ✅ |
| 조성 AM:SE:BD | **60:38:2 / 70:28:2 / 80:18:2 wt%** | 60:38:2/70:28:2/80:18:2 (+90:8:2) | ✅ (덱은 90 생략) |

**생성 규칙**(=GeoDict GrainGeo 규칙 배치, *압축 물리 아님*):
- NCM711 → **2차 입자 = 구(PSA 기반)**, **1차 입자 = convex polyhedron (0.5–1.5 µm, SEM 참조)**
- LPSCl → **구 (PSA 기반)**
- NBR → **"Add Binder Function"** (Contact Angle **0**, Binder Anisotropy Factor **1**)
- 전 재료 **"Periodicity"** 조건, **random seed 1–5**
- 출처 **J. Park, Y. M. Lee\*, Adv. Energy Mater. 10 (2020) 2001563**

> 🔑🔑 **positioning 재확인**: 2026년 발표에서도 생성은 여전히 **PSA/SEM 측정치 → 규칙 배치**다.
> **압력을 주어 구조가 *흐르는* 계산은 이 파이프라인에 없다**(캘린더링은 §9처럼 *재구성된 구조를 압축*하는
> ElastoDict 경로로 따로 간다). ⇒ 우리 **DEM+MPM = 분말에서 공정으로 구조를 예측(predict-from-powder)** 이라는
> 상향식 차별점이 이 덱으로 다시 확인된다. ⚠ 단 이는 **덱의 그림 구성**에서 읽은 것이고, 정본 근거는
> `papers/park2020_...`(규칙 배치 명시)·`papers/lim2025_...`(reconstruct-then-compress)다.

### 6b. voxel·domain 수렴과 계산 비용 (슬 19) ★ 우리에게 실무적으로 가장 유용
- **Voxel Size Control** (domain 30 × 30 × 30 µm 고정): voxel **50 / 75 / 150 / 300 / 600 nm**
  → **비접촉면적(specific contact area)** 이 voxel↓에서 급상승 후 포화, **계산시간(min)** 은 voxel↓에서 급증.
  슬라이드 문구: *"Voxel size ↓ → Accuracy ↑ / computational load ↑"*, **빨간 밴드가 ~50–75 nm 구간을 표시**.
- **Domain Size Control** (voxel 75 nm 고정): **15×15×30 / 30×30×30 / 60×60×30 / 90×90×30 µm³**
  → **접촉면적은 30×30×30 이상에서 거의 평탄**(REV 도달), **계산시간은 domain volume에 선형 급증**.
  문구: *"Domain volume ↑ → Accuracy ↑ / Computational load ↑"* (파란 밴드 = 부담 구간).
- **Performance Estimation**(Math2Market 제공): 격자 **256×1000×1000 / 256×750×750 / 256×512×512 / 256×256×256**
  → **voxel 수(백만) 대 메모리(GB)와 계산시간(day)** 이 둘 다 거의 선형. 최대점 **~250–280 M voxel에서
  메모리 ~45–57 GB, 계산시간 ~2.5–3 day**(figure-read).

> 🔑 **우리가 즉시 쓸 수 있는 것 = "REV/voxel 수렴을 *비용축과 같이* 보고하는 그림 양식"**.
> 우리 DEM/MPM 파이프라인은 domain·voxel 선택 근거를 수치로 남기지 않는다.
> ⚠ 절대 시간·메모리는 **그들 하드웨어·GeoDict 기준**이라 우리 벤치마크로 쓰면 안 된다(추세·형상만).

### 6c. 구조정보 분해 (슬 20)
AM(회색) / SE(노랑) / CA(초록) 3상 분해. **domain 50 × 50 × 50 µm, voxel 0.50 µm, 총 voxel 1,000,000**
(= 100³ ✓ 자체 정합). 나열된 입력: composition · loading level · density · porosity · material information · particle size.

### 6d. 검증: C-rate별 전압곡선 (슬 21)
- NCM 80 wt% 충전곡선 **0.1C / 0.5C / 1C** + SOC별 **리튬화(%) 3D 맵 6장** → *"고전류일수록 불균일 충전"*.
- **Simulation vs Experiment**: 용량 vs C-rate. 본 연구 **NCM711:LPSCl:NBR = 70:28:2, 10 mg cm⁻²** 와
  문헌 4계열(NCM622 기반, 3.77 / 20 / 15 / 23 mg cm⁻²) 비교, **시뮬레이션 3점(60:38:2 / 70:28:2 / 80:18:2)**.
  운전온도 30 °C. 결론 문구: *"Simulated capacity is closely matched with experimentally measured capacity"*,
  *"Unveiled non-uniform charged state of NCM cathodes as increasing the c-rate."*
  (J. Park, Y. M. Lee\*, AEM 10, 2001563 (2020))

---

## 7. 두 개의 Limitation (p.11–12 슬 22, 24)

### 7a. Limitation I — 측정 중 구조가 망가진다 (슬 22)
- **공기 민감(황화물 SE)**: LSPSC / LPS / LSS / LSAS 4계열의 **morphology evolution** 사진열 + 파단면 SEM.
  *"Structure distortion by side-reactions with (humid) air"* (**Q. Wang, *Chem. Eng. J.* 522 (2025) 167791**).
- **열 민감(폴리머)**: 분리막 SEP-1 **(Porosity 35 %)**, SEP-2 **(Porosity 48 %)** 인데 이미지 분할 결과는
  각각 **8.4 %**, **4.5 %** 로 나온다 → *"Structure distortion by thermal damage"*
  (**Y. Shin†, S. Kim†, W.-K. Kim\*, Y. M. Lee\*, Adv. Energy Mater. 10, e05319 (2026)**).
- 요약 문구: *"Reactive or less heat-tolerant materials … are easily deformed during measurements,
  requiring time- and cost-intensive techniques under anti-air or cryogenic conditions,
  while yielding only limited information."*

> 🔑🔑 **우리 프로그램에 대한 가장 강한 논거**: 황화물 SE는 **측정으로 얻은 미세구조 자체가 못 믿을 수 있다**.
> ⇒ **재구성(top-down)이 원천적으로 취약한 소재계에서 bottom-up 생성/예측의 가치가 커진다** — 이건
> 우리 DEM+MPM positioning의 *소재-특이적* 정당화이고, 지금까지 우리 문서에 없던 각도다.
> ⚠ **35 % → 8.4 %** 는 "진짜 porosity vs 이미지에서 잰 porosity"의 대비로 읽었다(그림 라벨 판독).
> 정확한 정의는 원논문 확인 전까지 **비율로도 인용 금지**(§13-3).

### 7b. Limitation II — 미시 파라미터를 정밀하게 못 잰다 (슬 24)
- **Open electrolyte system**: 전해액 증발 → **염 농도 변화**(반응속도·열역학 변화) + **타 성분 오염**.
- **단일입자·마이크로전극 측정**: 광학현미경 + **Au 필라멘트 ⌀10 µm** → NCM711 단일입자, glass frit, Li metal;
  **펨토초 레이저로 28 µm × 30 µm 마이크로전극 배열 가공**; 1C/2C/4C/8C 전압-시간 exp vs sim
  (**AEM 13 (2023) 2204328**; **EES 18 (2025) 3129-3147**).
- **Contact instability**: 입자 부피변화로 인한 접촉 불량·탈리 (*Electrochemistry* 84 (2016) 759-765).

> 🔑 **우리 최대 급소(i0·D_s 앵커)의 해법이 이 슬라이드다** — 정본은 `papers/song2025_...` (EES 18, 3129).
> 덱은 그 논문의 존재 위치를 알려줄 뿐, 수치는 논문에서 가져온다.

---

## 8. 제조공정 시뮬레이션 (p.13–17 슬 26–35) ★ 덱 고유 정보가 가장 많은 구역

### 8a. 현황 지도 (슬 26–28)
- **Mixing**: Wet vs Dry 2축 스크류 도해 (**KOZO KEIKAKU Eng. Inc., 64th Battery Symposium in Japan (2023)**)
- **Coating**: 슬롯다이 라인 + **갭 252 / 280 / 308 µm 압력장(Pa·s)** (*Chem. Eng. Sci.* 222 (2020) 115716;
  M. Ouyang, *J. Power Sources* 610 (2024) 234717)
- **Drying**: 첨가제 migration + CBD1/2/3 층 + AM 직경 **2.5 / 3.5 / 4.5 / 5.86 / 8.28 / 10.35 µm**
  (A. A. Franco, *Energy Storage Mater.* 43 (2021) 337)
- **Pressing**: dried **ε_dry = 35 %** (41 × 41 × **46 µm**) → calendered **ε_cal = 15 %** (41 × 41 × **23 µm**)
  (Franco, *JPS* 580 (2023) 233427)
- **Electrolyte infiltration**: 시간에 따른 전해액 침투 3단계 (Franco, *JPS* 511 (2021) 230384; NCM 94 % + CBD 6 %)
- 자인한 한계: *"Challenges: Difficult to reflect realistic particle morphology; high computational power is required."*

> 🔑 **"현실적 입자 형상을 반영하기 어렵다"** = **우리 MPM 소성 SHAPE morphology 축이 정확히 그 칸**이다.
> 그리고 §8a 전체가 **ARTISTIC(Franco) 인용 일색** = 그들도 제조공정 물리는 **외부 문헌 지도** 단계임을 보여준다.
> ⚠ 단 "그들은 제조공정 시뮬을 안 한다"고 쓰면 안 된다(§13-2) — 실제로 슬 34에서 **자체 DEM 결과**를 낸다.

### 8b. 캘린더링 = 우리 압축의 형제 (슬 29) — 정본 `lim2025`
설계변수(composition/**density**/loading level) → 셀/모듈/팩. 캘린더링 출력 5종:
**porosity · ionic tortuosity · electronic conductivity · contact area · particle deformation**.
before/after 3쌍 도해: **이온 경로 차단 / 새 전자 경로 생성 / 활물질 균열**
(**J. Lim†, J. Song†, J. Park, Y. M. Lee et al., *Small* 21 (2025) 2410485**).

### 8c. ★ CBD migration과 "2nd solvent" — 덱 고유(정본 미보유)
슬 32:
- 건조 3단계: **Step 1 Aggregation → Step 2 Film consolidation → Step 3 Pore emptying** (*AEM* 2022, 12, 2102233)
- 강조 문구(형광): *"As the solvent evaporates, it carries the binder and conductive additives toward the
  upper region, results in a non-uniform distribution."* 실측 근거: 바닥→표면 깊이별
  **도전재 함량**(as-mixed 6.0 wt% 대비 상부 7.7까지 상승)·**바인더 함량**(as-mixed ~1.5 → 상부 ~4.9)
  (*J. Electrochem. Soc.* 158 (2011) A1361) — figure-read.
- **핵심 주장(파란 박스)**: *"A small amount of **2nd solvent, immiscible with the bulk solvent**, can interact
  with the particles to **form a capillary structure**. These interactions, **beyond conventional van der Waals
  forces**, can **suppress the CBD migration**."* 계: NCM811 / Super P / PVDF, PVDF-in-NMP(bulk) + 2nd solvent.
  출처 **Y. M. Lee\*, S.-Y. Lee\* et al., *ACS Energy Lett.* 10, 6223-6235 (2025)**.

슬 33 — **OWRK 표면에너지 정량**(같은 논문):
```
γ_sl = γ_s + γ_l − 2( √(γ_s^d γ_l^d) + √(γ_s^p γ_l^p) )        W_sl = 2( √(γ_s^d γ_l^d) + √(γ_s^p γ_l^p) )
```
- 접촉각 측정 액체: **DIW(극성) 23.6 mN m⁻¹**, **디아이오도메탄(비극성) 37.82 mN m⁻¹**
- **NMP–2nd solvent 액/액 계면에너지 2.61 mN m⁻¹**, **NMP–공기 액체 표면자유에너지 38.58 mN m⁻¹**
- 고체 표면자유에너지(분산/극성/합, figure-read): **NCM ≈ 38 / 23.5 / 61.5**, **CB ≈ 45 / 11 / 56**,
  **PVDF ≈ 28.5 / 3 / 31.5 mN m⁻¹**
- **work of adhesion**(with NMP → with 2nd solvent, figure-read): NCM ≈ **97 → 60**, CB ≈ **90.5 → 67**,
  PVDF ≈ **64 → 53 mN m⁻¹**
- **interfacial surface energy**(with NMP → with 2nd solvent): NCM ≈ **2.5 → 25**, CB ≈ **4 → 14**,
  PVDF ≈ **5 → 3 mN m⁻¹**

### 8d. ★★ DEM 기반 슬러리 믹싱 (슬 34) — **우리 도구와 같은 도구**
- 계: **NCM(회색) / NMP(빨강) / 2nd solvent(초록)** 입자, **w/o 2nd solvent** vs **w/ 2nd solvent** 두 케이스.
- 단면 분석: NCM 입자 3개 사이 좁은 간극(domain a) 에 **2nd solvent가 집중**.
  부피분율 맵 스케일 — **NMP 20–70 %**, **2nd solvent 0–10 %** (깊이 0–7.5 µm × 폭 0–30+ µm).
- **@domain a 상대두께별 상대 부피분율**: 양 표면(0, 1)에 **NMP**, 가운데(≈0.2–0.7)에 **2nd solvent 우세**.
- 결론 문구: *"the 2nd was located between active material particles, thereby confirming the formation of
  capillary structures."* (ACS EL 10, 6223-6235 (2025))

> 🔑🔑🔑 **이게 이 덱에서 우리에게 가장 값진 슬라이드다.**
> ① **그들도 DEM을 쓴다** — 단 **슬러리 믹싱(액체 매개·모세관)** 축이고, 우리 DEM은 **건식 분말 압밀·접촉망 σ** 축이다
>   ⇒ **같은 도구, 겹치지 않는 물리**. 우리 positioning에 "DEM은 그들도 쓴다"는 사실을 반영해야 하고
>   (기존 `positioning_vs_geodict.md` 는 GeoDict 규칙배치만 상대해 왔다), 차별점을 **건식 ASSB 압밀 + 소성 MPM +
>   granular constriction σ** 로 다시 좁혀 서술해야 한다.
> ② 액상 가교(capillary bridge)로 입자 간 힘을 바꾸는 발상은 우리 **DEM 접촉모델의 미보유 항**(우리는 DMT/JKR
>   부착 + 소성만) — 흡수 후보.
> ⚠ **정본 논문 미보유**(ACS EL 10, 6223-6235) — 위 수치는 전부 **덱 figure-read**다. §15 위시리스트 1순위.

### 8e. 공정모델의 한계와 하이브리드 AI (슬 35–36)
- **양방향 데이터 전송 기반 제조 디지털트윈** 도해(Ayerbe/Franco, *AEM* 12 (2022) 2102696):
  *"physics-based models of manufacturing process **must be accelerated** due to their computational cost
  for continuous data exchange and optimization."*
- **Physics-Embedded AI (Hybrid)** — 물리모델 vs ML 비교표(M. Borah, *Comms. Eng.* 3 (2024) 134):

| 지표 | Physics-based | Machine learning |
|---|---|---|
| Accuracy | Medium | Medium |
| **Computation cost** | **High** | Low |
| **Interpretation** | **High** | Low |
| **Extrapolation** | **Medium** | Low |
| Interpolation | Medium | Medium |
| **Data requirement** | Low | **High** |

  두 결합 위상(Z. Sun, *J. Energy Storage* 56 (2022) 105992): **(a) 물리 → 중간변수 → ML → 예측**,
  **(b) ML → 중간변수 → 물리(제약) → 예측**.

### 8f. Summary (슬 37) — 3한계 → 3해법
| 한계 | AI 해법 | 덱의 평가 |
|---|---|---|
| Labor-intensive Image Processing | **CNN 기반 고급 특성화**(분할·생성·초해상·차원확장; ACS EL 7 (2022) 4368) | 빠른 분할 & 해상도 향상, 적용성↑ |
| Model Validation | **Generative AI**(*Matter* 7 (2024) 4260-4269) | DT 구조를 쉽게 얻음(빠른 예측) **단 적용범위 제한 가능성 큼** |
| Limited Bidirectional Feedback | **Physics-embedded AI (hybrid)** | 높은 정확도 · (상대적) 빠른 예측 · **새 전극/셀 설계에 넓은 적용성** |

---

## 9. 가상 캘린더링 정량 (p.15 슬 30–31) — 정본 `lim2025`, 덱은 figure-read

밀도 sweep **2.3 / 2.4 / 2.5 / 2.7 / 2.8 / 3.0 / 3.3 / 3.4 / 3.5 / 3.6 / 3.8 / 4.0 g cm⁻³**
(재구성 uncalendered → 가상 캘린더링), **실제 캘린더링(3.6 g cm⁻³, 재구성)** 과 1점 대조.

| 지표 | 저밀도(2.3) → 고밀도(4.0) | 비고 |
|---|---|---|
| Porosity (sim vs theoretical) | **≈ 49 → ≈ 10 %** | 두 계열이 전 구간 근접 |
| Effective electronic conductivity (sim vs exp) | **≈ 0.9 → ≈ 2.2 S m⁻¹** | |
| Ionic tortuosity | **≈ 1.4 → ≈ 3.5** | 3.5 g/cm³ 이후 급상승 |
| NCM \| pore 비표면적 | **≈ 9.5 → ≈ 7 × 10⁶ m² m⁻³** | 단조 감소 |
| NCM \| CBD 비접촉면적 | **≈ 4.4 → ≈ 10.3 × 10⁶ m² m⁻³** | 단조 증가 |
| **3.6 g cm⁻³ virtual ↔ actual** | porosity ≈ 18 %, σ_e ≈ 1.87 S m⁻¹ 에서 **일치** | 모델 검증점 |

**PNM + 응력**(슬 31):
- 등가 공극반경 지도(0.08–3.08 µm), **평균 등가반경 0.83 / 0.67 / 0.63 µm** @ 3.4 / 3.6 / 3.8 g cm⁻³
- **평균 배위수 4.1 / 3.5 / 3.15** @ 3.4 / 3.6 / 3.8
- **von Mises 응력 0–150 MPa** 분포(2.8–4.0 g cm⁻³) + **crackable volume %**(>100 MPa, >150 MPa)가
  **3.4 g cm⁻³ 부근부터 급격히 증가**해 4.0에서 >100 MPa ≈ 14 %, >150 MPa ≈ 8 %(figure-read)

> ✅ **정본 대조 결과 정합**: `papers/lim2025_virtual_calendering_framework.md` 의
> "porosity 49→10 %, σ_e +130 %, crack VMS>150 MPa 3.4–3.6 지수급증, 최적 3.4–3.6" 과 덱 그림이 일치한다.
> σ_e 0.9→2.2 S/m = **+144 %** 로 정본의 "+130 %"와 figure-read 오차 범위. **인용은 정본에서.**

---

## 10. 남은 과제 (p.19 슬 38–39) ★ 덱 고유

### 10a. ARTISTIC 프로젝트 (슬 38)
역설계 플랫폼: **파일럿 라인**(Mixing&Slurry / Coating&Drying / Calendering / Electrolyte filling / Performance)
↔ **공정모델**(**CGMD / CGMD / DEM / LBM / FEM**) → Dataset → **Surrogate Model Y = f(x)** →
**Bayesian optimizer**(maximize/minimize properties) → 채택할 제조 파라미터.
(**A. A. Franco et al., *Batteries & Supercaps* 8 (2025) e202400385**)
> *"A pioneering project … **However, most applications remain at the 'digital model' stage**, whereas the
> realization of a **true digital twin** through bidirectional real-time data exchange is **still at an early
> stage** in battery manufacturing."*

### 10b. Goal: 양방향·실시간 — 4대 과제 (슬 39)
| # | 과제 | 현상 | 요구 |
|---|---|---|---|
| 1 | **Computational Acceleration** | **높은 계산부하 — 슈퍼컴퓨터로도 2~3일** (*Batteries Supercaps* 8 (2025) e202400385) | 실시간 제조 제어를 위한 **빠른 근사 또는 AI 지원** |
| 2 | **Multiscale/Multiphysics Coupling** | 제조공정→전기화학 성능까지 연속 해석 필요 | **단계별 모델 간 정보 전달·경계조건 정합** |
| 3 | **Experiment-Model Integration** | 파라미터화·검증용 **데이터셋 부족** | 실험데이터 **자동 취득** |
| 4 | **Data Standardization** | 제조 데이터 **접근성 제한** | 모델 검증·학습용 **표준화 데이터** |

> 🔑 **①②는 우리 로드맵과 정확히 같은 병목**이고, 우리 **스케일링 법칙(σ 삼중항 폼)** 은 ①의
> "fast approximation" 에 해당하는 자산이다. ②는 우리 `DEM → MPM → Kirchhoff → PyBaMM` 인계에서 이미
> 겪고 있는 문제(경계조건·구조 인계)라 **덱이 우리 문제를 학회 언어로 명명해준다**.

---

## 11. 우리 대비 — 축별 판정 ★★

| 축 | 그들 (덱 + `papers/` 정본) | 우리 (DEM+MPM 캠페인) | 판정 |
|---|---|---|---|
| **구조 획득** | top-down 재구성(FIB-SEM 100회·voxel 100 nm, XCT) + AI 분할/초해상 | 없음(실험 재구성 인프라 없음) | **완패 — 우리 공백**. 단 §7a(황화물 왜곡)가 그 공백의 가치를 깎아준다 |
| **구조 생성** | PSA/SEM 기반 **규칙 배치**(GrainGeo, seed 1–5) | **분말→공정 물리로 예측**(DEM 압밀 + MPM 소성) | **우리 우위(방법 신규성)** — 2026 발표에서도 규칙 배치가 유지됨을 확인 |
| **캘린더링/압축** | reconstruct-then-compress(ElastoDict), 밀도 sweep 2.3–4.0, PNM·응력·균열 | predict-from-powder, Heckel P_y·소성 morphology·fracture | **형제·직교** — 출력 지표(porosity/τ/σ_e/접촉면적/응력)가 1:1로 대조 가능 |
| **전달 물성 σ** | GeoDict 연속체 유효물성(σ_e, τ) — *덱은 σ_ionic 절대값 미제시* | **σ 삼중항**(Kirchhoff/Holm granular constriction: σ_ionic + σ_e + σ_thermal) | **우리 우위(물리 깊이)**. ⚠ "그들은 σ_ionic이 없다"고 쓰지 말 것 — 덱 미표시일 뿐 |
| **슬러리/습식 DEM** | **DEM 슬러리 믹싱 + 2nd solvent 모세관 구조**(ACS EL 10, 6223) | 없음(건식 압밀 DEM만) | **완패 — 새로 드러난 공백**. 같은 도구·다른 물리 |
| **표면에너지/부착 물성** | OWRK로 W_ad·γ_sl 실측(NCM/CB/PVDF × NMP/2nd solvent) | DMT/JKR 부착 파라미터는 문헌 차용 | **완패** — 우리 DEM 접촉모델 입력의 실측 경로 |
| **전기화학 결합** | BV+질량보존 3D 결합, C-rate 검증, 리튬화 맵(park2020) | Phase-4 계획(PyBaMM DFN) | **완패 — 우리 미완**. 정본이 레시피까지 공개 |
| **미시 파라미터 실측** | 단일입자·마이크로전극(Au ⌀10 µm, fs-laser 28×30 µm) | 없음(i0·D_s 앵커 = 우리 최대 급소) | **완패**. 정본 `song2025_...` 가 해법 |
| **REV/수렴·비용 보고** | voxel·domain 수렴 + 메모리/시간 곡선을 **한 장에** | 수렴 근거 문서화 부족 | **완패(경미) — 저비용으로 흡수 가능** |
| **소재계** | NCM711+LPSCl+NBR (**우리와 동일**) · 일부는 LIB 액체계(NCM622/811) | NCM+LPSCl 황화물 ASSB | **동일 소재계** = 대조가 성립하는 근거 |
| **데이터 정직성 장치** | 덱에서 확인 안 됨 (부재 주장 금지) | 인용금지 규율·figure-read 표시·순서민감도 | **우리 우위(단 §13-2 주의)** |

---

## 12. 우리가 가져올 것 (실행 항목)

1. **REV/voxel 수렴 + 비용 곡선 그림 양식**(슬 19) — 우리 DEM/MPM domain·voxel 선택 근거를 **정확도-비용 2축**으로
   1장에 남긴다. 비용 ≈ 0, 리뷰어 방어력 큼. **1순위.**
2. **"Blinded Scale" 프레임**(슬 6) — 소재 σ ↔ 전극 σ 격차를 우리 σ 삼중항으로 메운다는 서론 문장.
   ⚠ LLZO 수치(5.4e-4/7.9e-7)는 인용하지 말고 **우리 LPSCl 값으로 같은 그림**을 만든다.
3. **황화물 = 재구성이 원천적으로 취약**(슬 22) → **bottom-up 생성의 소재-특이 정당화**를
   `positioning_vs_geodict.md` 에 새 절로 추가. **정본(Chem. Eng. J. 522, 167791 / AEM e05319) 확보 후.**
4. **DEM 슬러리/모세관 축을 positioning에 반영**(슬 34) — "DEM은 그들도 쓴다(습식 믹싱), 우리는 건식 압밀+
   granular σ+소성 MPM" 으로 차별 문장을 **좁혀서** 다시 쓴다. 지금 문서는 이 사실을 모른다.
5. **캘린더링 5축 대조표**(슬 30) — 우리 MPM 압축 출력(porosity/τ/σ_e/비표면적/접촉면적)을
   `lim2025` 정본 값과 같은 표에 놓는 대조 그림. ⚠ 그들은 LIB 액체계라 **수치 앵커가 아니라 형상/추세 대조**.
6. **PNM(pore network) 지표 도입 검토**(슬 31) — 평균 등가공극반경·배위수는 우리 DEM 구조에서 산출 가능한
   저비용 신규 descriptor. 우리 σ 스케일링의 잔차 사냥 후보.
7. **OWRK/W_ad 실측 경로**(슬 33) — 우리 DEM 부착 파라미터의 문헌 차용을 **측정 가능한 양**으로 바꾸는 길.
   실험 협업 제안 소재.

---

## 13. 주의 / 한계 (over-claim 방지)

1. **슬라이드 번호가 안 맞는다.** 섹션 표지 번호는 **3 / 10 / 17 / 25 (/44)** 인데 인쇄본은 **39장**이다.
   3↔10 사이에 인쇄되지 않은 슬라이드가 **1장** 있고(표지 3 다음 본문 5장만 인쇄), 뒤쪽도 44에 미달한다.
   ⇒ **"덱에 X가 없다"는 서술 금지** — 인쇄 누락·발표시간 편집 가능성(talks/README #3).
2. **덱은 부재의 증거가 아니다.** 특히 (a) ACS EL 리뷰 그림의 **빈 Thermal 칸**, (b) σ_ionic 절대값 미표시,
   (c) 데이터 정직성 장치 미확인 — 셋 다 **논문 실물로만** 판정한다.
3. **§7a의 35 % → 8.4 % / 48 % → 4.5 %** 는 그림 라벨 판독이고 정의(실측 porosity vs 이미지 porosity)가
   슬라이드에 명시돼 있지 않다. **정본(AEM e05319) 확인 전 인용 금지 — 비율도 금지.**
4. **인용 표기 의심 2건**: (a) `Nano Energy 79, 10545 (2021)` — Nano Energy 79권 논문번호는 통상 6자리(105545 등)
   → **자릿수 누락 의심**; (b) `Adv. Energy Mater. 10, e05319 (2026)` — 2026년 AEM은 16권대라
   **권 번호 오기 의심**. 둘 다 **레퍼런스 리스트에 그대로 옮기지 말 것**(CLAUDE.md 원고 규율: 로컬 PDF 기준).
5. **§9·§8c의 수치는 전부 figure-read**다. `lim2025` 항목은 정본이 있으므로 **정본 인용**,
   2nd solvent(ACS EL 10, 6223) 항목은 **정본 미보유이므로 "덱 소환값"으로만** 쓰고 원고 인용 금지.
6. **소재계 혼재**: 캘린더링·CBD migration·OWRK·DEM 믹싱은 **LIB 액체계(NCM622/811 + PVDF/NMP)**,
   §6의 생성/검증만 **황화물 ASSB(NCM711+LPSCl+NBR)** 다. **두 군을 같은 표에 섞지 말 것.**
7. **계산 비용 수치(2~3일 슈퍼컴퓨터, 45–57 GB / 2.5–3 day)** 는 하드웨어·소프트웨어 의존이라
   우리 벤치마크가 아니다. "우리가 더 빠르다/느리다" 주장 금지.
8. **`Nat. Commun., Under Review`** 는 미출판 — 존재만 기록하고 결과를 인용하지 않는다.

---

## 14. 인용 가능 문장 (원고/발표용)

- **(프레임)** "디지털트윈 전극 모델은 **파라미터(소재 물성)·지배방정식(물리)·기하(미세구조)** 세 축으로 서고,
  1D/P2D가 잃는 것은 세 번째 축이다" (슬 5의 명제)
- **(우리 서론 후크)** "소재 수준 이온전도도와 셀 내부에서 실현되는 이온전도도 사이에는 자릿수 격차가 있고,
  그 격차를 만드는 것이 미세구조다" (슬 6 "Blinded Scale"의 명제 — **수치는 우리 것으로 대체해 쓸 것**)
- **(positioning)** "전극 디지털트윈 구조는 **top-down 재구성**과 **bottom-up 생성** 두 길로 얻으며,
  후자는 설계 파라미터에서 구조를 만든다" (peer-reviewed 원문 = **Kim, S.; Lee, H.; Lim, J.; Park, J.;
  Lee, Y. M. *ACS Energy Lett.* **2024**, *9*, 5225–5239** — `papers/kim2024_digital_twin_acsenergyletters.md`)
- **(우리 신규 논거)** "황화물 전해질과 폴리머는 **측정 과정 자체가 구조를 왜곡**하므로, 재구성 기반 디지털트윈이
  구조적으로 불리하다" (슬 22의 명제; ⚠ **정본 확보 후에만 인용**)
- **(과제)** "물리 기반 제조공정 모델은 슈퍼컴퓨터에서도 수일이 걸려, 실시간 양방향 디지털트윈에는
  **가속(빠른 근사 또는 AI)** 이 전제조건이다" (슬 39; 원출처 *Batteries & Supercaps* 8 (2025) e202400385)
- ⛔ **인용 금지**: 2nd solvent 계열 수치(§8c) 전부 — 정본 미보유 figure-read.
- ⛔ **인용 금지**: §7a 분리막 porosity 35→8.4 % — 정의 미확인.

---

## 15. 미해결 질문 / 위시리스트

| # | 질문 | 닫는 방법 |
|---|---|---|
| Q1 | **2nd solvent DEM 믹싱**의 접촉모델(모세관 가교 힘 형태·파라미터·입자 수·시간)은? | **ACS Energy Lett. 10 (2025) 6223-6235 PDF — 위시리스트 1순위** |
| Q2 | 분리막 porosity 35 % vs 이미지 8.4 % 의 정확한 정의와 열손상 조건은? | **Adv. Energy Mater. (2026) e05319** (권 번호 확인 포함) |
| Q3 | 황화물 SE의 공기 노출 구조 왜곡 정량(시간·습도 vs 형태 변화)은? | **Chem. Eng. J. 522 (2025) 167791** (외부, Q. Wang) |
| Q4 | 셀·팩 스케일 모델의 구조 인계 방식(전극 미세구조 → 셀 모델 경계조건)은? | **J. Energy Chem. 105 (2025) 87-95** · **eTransportation 22 (2024) 100370** |
| Q5 | Nat. Commun. 15 (2024) 10134 는 전극/분리막 중 어느 축인가? | 해당 PDF |
| Q6 | AI segmentation의 정확도 지표(ground truth 대비 IoU 등)와 학습 데이터 규모는? | 구술 / GeoDict-Math2Market 문서 |
| Q7 | 그들의 σ_ionic,eff 산출은 연속체(ε/τ)인가 네트워크인가 — 우리 Kirchhoff/Holm과의 위상 차이 재확인 | `papers/park2020_...`·`papers/lim2025_...` 재독(이미 보유) |

---

## 99. ⏳ 발표 구술 내용

`talks/lee2026_skku`·`talks/moon2026_cau` 와 마찬가지로 구술 txt를 받으면 여기에 정리하고 §15의 Q6를 닫는다.

_(비어 있음 — 2026-08-03 기준 미보유)_

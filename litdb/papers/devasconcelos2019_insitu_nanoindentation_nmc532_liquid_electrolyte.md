<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-24) 에서 꼭 뽑으라고 한 항목.
     본 = sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile.md (NCM 기계 물성 · 나노압입 카드의 꼴 · 2 차 인용 매핑 · 우리 E_AM / H_AM 대조) ·
     같은 그룹 짝 카드 = devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode.md (같은 절 번호 · 두 필수 절 §0-1 고른 의도 대조 · §8 자세한 분석).
     원문 = 출판본 (Experimental Mechanics (2019) 59:337–347 · 11 쪽 · © Society for Experimental Mechanics 2018) + ESM (Electronic Supplementary Material) docx 10 개 (그림 S1–S8 · 표 S1–S2 · 한 파일에 한 항목).
     쪽 표기 = "p.n" = PDF 쪽 n (학술지 쪽 = 336 + n · p.1 = 337 … p.11 = 347).  크롭 파일 이름의 pN · figures.json 의 page 는 PDF 쪽이다 (SI 는 각 docx 를 LibreOffice 로 PDF 바꾼 것의 1 쪽).
     값 표지: [인쇄] = 본문 · 그림 안 글자 · 표로 적힌 값 · [판독 · 벡터] = 그림 3 · 5 · 7 · 8 (본문) · S4 (SI) 는 **벡터 경로**라 좌표를 눈금 선으로 환산한 값 (재현 = litdb/figures/<slug>/digitized.csv 1,322 행) ·
     [카드 판독] = 원문에 없는 양을 이 카드가 그림에서 끌어낸 값 (예: 점 개수 N) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기 · §14) ·
     [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본 다른 카드에 적힌 값 (slug 병기) · [우리] = 우리 쪽 값 (작업 트리 파일 · CLAUDE.md 출처 — 정본 카드가 옮긴 것) · [미확인] = 본문 11 쪽 + ESM 10 개 전수에 없음.
     ★ 그림 8 의 값 (113 · 108 · 200 · 201 …) 은 **평균만 그림 안 글자로 인쇄**되고 ± (SD) 는 원문 어디에도 숫자로 없다 — 이 카드의 SD · N · 중앙 · 사분위는 그림 8 의 점 · 상자 · 선을 벡터로 읽은 값이다 (12 묶음 모두 점 평균 = 인쇄 평균 · 흰 사각형 위치 = 점 평균 4 자리까지 → 점 집합이 빠짐 · 겹침 없이 완전함을 확인).
     원문 11 쪽은 글자 층 (PyMuPDF) + 전 쪽 렌더로 읽었다.  ESM docx 는 zipfile 로 word/document.xml 을 읽고 (OMML 수식 m:t 포함) · 그림 · 표는 LibreOffice PDF 변환본에서 잘랐다 (변환본은 scratch · 커밋하지 않음).
     계산 · 모델은 없다 — 실험 (Berkovich · cube-corner 나노압입 · 무게-치수 기공) + Rumpf 모세관 강도 어림 하나. -->

# NMC532 이차입자 응집체 · 소결 펠릿 · PVDF · CB/PVDF 의 건조 ↔ 액체 전해질 (1 M LiPF₆-PC · 1 h) 속 나노압입 — 응집체 E 113 → 108 · H 7.8 → 7.8 GPa · 펠릿 200 → 201 · 14.0 → 13.9 GPa (깊이 85 nm · 평균 · 차이 없음) · 응집체 압입 인성 K_c 0.104 → 0.212 MPa m^½ (t-검정 p 0.007 · 펠릿 0.298 → 0.291 그대로) · PVDF 부피 +30 % · E · H 약 −50 % · CB/PVDF −80 % 넘게 — de Vasconcelos · Sharma · Xu · Zhao (Exp. Mech. 59 (2019) 337–347)

> slug `devasconcelos2019_insitu_nanoindentation_nmc532_liquid_electrolyte` · DOI `10.1007/s11340-018-00451-6` · type `exp (instrumented nanoindentation inside an Ar glovebox, dry vs immersed in 1 M LiPF6-PC (1 h soak, stainless-steel coin-cell case): Keysight G200, Berkovich with CSM (2 nm, 45 Hz), constant Pdot/P 0.05 1/s, Oliver-Pharr, nu 0.3 (NMC) / 0.4 (PVDF, CB/PVDF) assumed, NMC values read at 85 nm; cube-corner pop-in fracture toughness (Lawn/Anstis formula + Field crack length, automated Q3+3IQR pop-in detector, h_min 100 nm); NMC532 (MTI) as-received secondary particles in a polystyrene matrix + sintered pellet; PVDF and CB/PVDF (50:50) films at 3 porosities; Rumpf capillary-bridge estimate - no simulation)` · PDF `bc731081-24._In-situ_nanoindentation_measurement_of_local_mechanical_behavior_of_a_Li-ion_battery_cathode_in_liquid_electrolyte.pdf` (11 쪽) + ESM docx 10 개 (`74921154-24._SupZ_00…09_11340_2018_451_MOESM10…1_ESM.docx`) · digested `2026-11-12` · status ✅

> elements: Li, Ni, Mn, Co, O

> **저자**: **L.S. de Vasconcelos** · N. Sharma · R. Xu · **K. Zhao\*** — 모두 School of Mechanical Engineering, Purdue University (West Lafayette, IN 47907, USA) — \* 교신 (kjzhao@purdue.edu) · *Experimental Mechanics* (2019) **59**:**337–347** · 접수 2018-06-03 · 승인 2018-10-29 · **온라인 2018-11-28** (p.1) · © Society for Experimental Mechanics 2018 · 키워드 Nanoindentation · In situ · NMC · Mechanical properties · Li-ion batteries · 연구비 = NSF DMR-1832707 · CMMI-1726392 (p.9) · 쪽 머리글 *"Exp Mech (2019) 59:337–347"* · **호 (issue) 번호는 PDF 어디에도 인쇄돼 있지 않다**.  (제1 저자 전체 이름 Luize Scalco de Vasconcelos = 같은 사람의 2016 카드.)
> **이웃 카드 (링크만)**: [`devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode`](devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode.md) (같은 그룹 · 같은 NMC532 · 2016 EML · targeted 138.73) · [`sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`](sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile.md) (참고 [27] = 이 논문 · "113 GPa · H 7.8") · [`stallard2022_cathode_mechanical_properties_review`](stallard2022_cathode_mechanical_properties_review.md) ([74] = 이 논문 · 그림 7 · 9 · 12A) · [`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`](wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn.md) ([25] = 이 논문 · 가리킨 카드) · [`kalnaus2023_ssb_critical_role_of_mechanics_stress_relief_review`](kalnaus2023_ssb_critical_role_of_mechanics_stress_relief_review.md) ((55) = 이 논문 · K 0.3 · 0.1) · [`sharma2023_nmc_single_crystal_anisotropic_nanoindentation`](sharma2023_nmc_single_crystal_anisotropic_nanoindentation.md) ([23] = 이 논문 · "재수록") · [`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`](xu2017_nmc532_nanoindentation_modulus_hardness_toughness.md) (이 논문의 [44] · 같은 압입 · K_c 방법의 선행) · LPSCl 쪽 압입 = [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md).
> **판독 원자료**: `litdb/figures/devasconcelos2019_insitu_nanoindentation_nmc532_liquid_electrolyte/digitized.csv` (1,322 행 — 그림 8 점 · 상자 · 수염 · 중앙선 · 평균 표지 343 · 그림 7 곡선 꼭짓점 831 · 그림 5 (PS 기지) 118 · 그림 3 막대 · 표지 + SD 18 · 그림 S4 유효 시험 비 12) · 그림 크롭 **63 장** (도구 14 → 그대로 3 · 다시 자름 11 + 손 49 = 그림 5 · 패널 15 · 식 9 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: Purdue (Zhao 그룹) 이 상용 NMC532 분말 (MTI) 을 두 꼴 — ① **받은 그대로의 이차입자** (일차입자 0.1–1 µm 의 응집체 · *"agglomerate"*) 를 폴리스티렌 (PS) 기지에 박아 연마한 것 ② 볼밀 → 13 mm 다이 · 5 톤 → **1000 °C 10 h 소결 펠릿** (결정립 3–10 µm) — 으로 만들고, **Ar 글로브박스 (O₂ · H₂O < 0.5 ppm) 안** Keysight G200 으로 **건조** 와 **1 M LiPF₆-PC 에 1 h 담근 (wet)** 상태를 Berkovich (CSM) 로 눌러 **깊이 85 nm 의 E · H** 를, cube-corner 팝인으로 **압입 인성 K_c** 를 냈다 — 그림 8 안 글자 (= 평균): 응집체 **E 113 → 108 · H 7.8 → 7.8 GPa** · 펠릿 **200 → 201 · 14.0 → 13.9 GPa** (건조 → wet · *"no apparent difference"*) · 응집체 **K_c 0.104 → 0.212 MPa m^½** (t-검정 p = 0.007) · 펠릿 **0.298 → 0.291** (그대로).  저자 해석 = 일차입자 사이로 빨려 든 전해질의 **모세관 다리**가 계면 결합을 더한다 (Rumpf 식 → +0.044 MPa m^½ ↔ 측정 평균 차 0.108 · 중앙 차 0.085).  바인더 쪽: PVDF 는 전해질에서 **부피 +30 %** · E · H **약 −50 %** (건조 E 590 MPa) · CB/PVDF (50:50 wt%) 는 기공 3.8 · 27.5 · 50.8 % 에서 E 2.45 · 1.22 · 0.50 GPa [판독 · 벡터] → wet 에서 −81 ~ −87 %.
⇒ **"113 GPa" = 이 논문 그림 8a 의 *응집체 (as-received NMC532 이차입자) · 건조 · 깊이 85 nm · 평균* (N 20 [카드 판독]) 이다 — 같은 조건 wet 은 108 · 같은 그림의 소결 펠릿은 200.  리튬화 · 충전 상태 · 사이클 변화는 이 논문에 없다 (pristine 분말만 · "in-situ" = 전해질 속 · 전기화학 없음).**

| 1저자가 꼭 뽑으라고 한 것 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 전극 · NCM 조성 | **NMC532** (*"commercial LiNi0.5Mn0.3Co0.2O2 (NMC532)"* p.2) · 분말 = **MTI Co.** (p.2) · ⚠ 제목 · 서론의 *"cathode … electrode"* 와 달리 **실제 시료는 전극이 아니다**: (a) 분말을 245 °C 로 녹인 PS 위에 눌러 박은 응집체 (b) 볼밀 서브마이크론 분말 ≈1 g · 13 mm 다이 · *"5 tons"* · 1000 °C 10 h (10 °C/min) 소결 펠릿 (c) PVDF (HSV900 · MW 600,000) 필름 ≈45 µm (d) CB (Super P) : PVDF = 50 : 50 wt% 필름 ≈400 µm → 롤 프레스로 기공 50.8 · 27.5 · 3.8 % · 연마 = 0.05 µm 콜로이드 실리카 ≈30 min → 진공 80 °C 하룻밤 → 거칠기 ≈4 nm [44] | [인쇄] p.2–3 |
| ② ★ 리튬화 상태 | **없음** — as-received (pristine) 분말 · 충방전 · 탈리튬화 이력 없음 · 화학량 · SOC 미기재.  서론만 *"The mechanical properties evolve with the state of charge and the cycle number."* (p.2) · SOC 측정은 같은 그룹 operando 플랫폼 [42] 의 몫 | [인쇄] p.2 · [미확인] |
| ③ ★ 액체 전해질 안 압입 — 장비 · 셀 · 압자 · 깊이 | **Keysight G200** · **Ar 글로브박스 (O₂ · H₂O < 0.5 ppm)** · wet = **스테인리스 코인셀 케이스**에 시료를 넣고 전해질에 잠근 채 · 압입 전 **1 h 담금** · 전해질 = **1 M LiPF₆ in propylene carbonate (PC)** (비휘발 → 액면 · 염 농도 일정) · **Berkovich** (E · H, Oliver–Pharr · CSM 2 nm · 45 Hz · Ṗ/P 0.05 s⁻¹ · β 1.034 · E_i 1141 GPa · ν_i 0.07 · 최대 깊이 NMC 500 nm · 고분자 2000 nm) · NMC 값 = **85 nm** · **cube-corner** (K_c · 중심선-면 35.3°) · targeted = 지름 ≥ 15 µm 입자 한가운데 · 필름 = 200 µm 간격 격자 | [인쇄] p.3–4 · p.7 |
| ④ ★ E · H ± (상태별 · 건조 ↔ 액체 안 · 충전 상태별) | 아래 §3-3 표 — **평균만 인쇄** (그림 8 안 글자) · **± 는 원문에 숫자 없음** → 점 판독으로 SD · N · 중앙 · 사분위를 냈다 [카드 산술 · 판독 · 벡터]: E 응집체 **113 (SD 13.3 · N 20) → 108 (12.8 · 15)** · 펠릿 **200 (17.2 · 26) → 201 (32.8 · 23)** · H **7.8 (1.66) → 7.8 (1.87)** · **14.0 (2.04) → 13.9 (2.63)** · K_c **0.104 (0.073 · N 17) → 0.212 (0.143 · 22)** · **0.298 (0.150 · 19) → 0.291 (0.142 · 21)** · **충전 상태별 = 없음** | [인쇄] 그림 8 · p.7 · [판독 · 벡터] |
| ⑤ ★ 113 GPa 는 원문의 어떤 값인가 | 그림 8a 안 글자 **"113"** = 응집체 · 건조 · 85 nm · **평균** (흰 사각형 = 점 평균 112.8 [판독 · 벡터]) · 중앙 110.2 [105.1, 118.0] · 같은 응집체 wet 108 · 펠릿 200 / 201.  [Sedl26] [27] → *"113 GPa · H 7.8"* = 맞다 (H 7.8 은 건조 · wet 둘 다) · [Stallard22] 그림 12A *"110 [105, 118]"* = 이 논문의 **중앙 [Q1, Q3]** (평균 아님) | [인쇄] 그림 8a · [판독 · 벡터] |
| ⑥ ESM 의 그림 · 표 | 그림 S1 (시험마다 S̄ 상자 그림 · 시험 수 19 · 25 · 19 · 21) · S2 · S3 (PVDF · CB/PVDF E · H vs 깊이) · S4 (h_min 50 · 100 · 150 nm 민감도 + 유효 시험 비) · S5–S8 (시험마다 팝인 검출 · K_c 다섯 점) · 표 S1 (CB/PVDF 기공) · 표 S2 (PVDF 부피 팽창 30.8 · 30.5 %) — 전부 크롭 | [인쇄] ESM |
| ⑦ 저자 한계 | ① 식 4 의 α 는 방위 · 이방성에 따라 달라 *"effective" toughness* 로만 (p.4) ② 깊으면 E 감소 = 기판 효과 + 깊은 압입 손상 → 85 nm (p.7) ③ 응집체 값은 다짐 · 기공 · 일차입자 상호작용에 좌우 · 합성법이 영향 (p.7) ④ wet 산포 큼 = 액 포화도 불균일 (p.7) ⑤ Rumpf = 균일 구 이상화 · 강도 과소 가능 [64] · 다른 기전 (표면층) 가능 · *"Further experiments are necessary"* (p.9) | [인쇄] |
| ⑧ DEM · 소성 · 2D/3D · 탈압 | DEM · 입자 모델 **없음** · 모델 관련 문장 = Rumpf 의 이상화 경고 (p.9 · §4-3) · 소성 = 압입 경도만 (일축 항복 환산 없음) · 2D/3D 말 없음 · 탈압 = 압입 제하 곡선만 (그림 7a: h_f/h_max ≈0.69 펠릿 · ≈0.47 응집체 [판독 · 벡터]) | [인쇄] · [판독 · 벡터] |

⛔ **한정어 (떼지 말 것)**: ① **NMC532 · 액체계 (LiPF₆-PC)** — 고체전해질 (LPSCl) 없음 · NCM811 아님 ② **pristine 분말 · 리튬화 · SOC · 사이클 변화 없음** ③ E · H 는 **표면 국소 Berkovich · 85 nm** — 같은 응집체가 49 nm 128.5 → 508 nm 50.4 GPa [판독 · 벡터] (입자 전체 · 접촉 강성 아님) ④ **ν 0.3 가정** ⑤ **± 미인쇄** (SD · N 은 판독) ⑥ K_c = *"effective"* (α 0.036 고정 · 균열 길이는 팝인 변위로 추정 · 측정 아님) ⑦ 펠릿 = **소결 다결정** (결정립 3–10 µm) — 결론의 *"large single particles"* 는 **단결정 시료가 아니다** ⑧ wet = **1 h 담금 · 포화도 미측정** (S 0.95 는 Rumpf 계산의 가정).
⇒ **절대값 전이**: NMC 이차입자 (응집체) · 치밀 결정립의 국소 E · H · K_c **자릿수** 는 같은 층상 산화물 양극 값이라 우리 AM (NCM811) 쪽 근거로 **"NMC532 · 응집체 / 소결 펠릿 · 85 nm · 건조 (Ar)"** 꼬리표를 달고 나란히 놓을 수 있다.  **wet 값 · 모세관 해석 · PVDF · CB/PVDF 값은 우리 계 (황화물 ASSB · 액체 없음 · PTFE) 로 전이 0 건.**

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-24 의 '왜' 칸)

의도 원문: *"c (AM) — ★ NCM E 의 1 차 출처 후보 (정본 Sedlatschek · Stallard 카드가 2019 · NMC532 113 GPa 로 2 차 인용)"* (가리킨 카드 = `wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn` L417 · L424)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "c (AM)" (질문 c: AM 의 항복 · 경도 · 크리프 값과 정의, 일축 항복과 견줄 환산) | **일부** | 경도 **있음** — 응집체 **7.8 · 7.8** · 펠릿 **14.0 · 13.9 GPa** (건조 · wet · 85 nm · Berkovich · 그림 8b) · 정의 = Oliver–Pharr H = P/A (식 2) · 압입 인성 K_c **있음** (그림 8c) · **일축 항복 환산 · 크리프 값 없음** (최대 하중 유지 · 크리프 미보고) · 조건 = Ar 글로브박스 · 상온 (온도 [미확인]) · pristine · 시편 압밀 없음 (펠릿은 소결체) |
| "NCM E 의 1 차 출처 후보" | **채움 (조성 · 시료 한정)** | 이 논문의 **자체 측정** (2 차 인용 아님): 응집체 **113 (건조) · 108 (wet)** · 소결 펠릿 **200 · 201 GPa** (그림 8a 안 글자 · p.7 · 85 nm · ν 0.3 가정 · Berkovich CSM).  ⚠ "NCM" = **NMC532** (MTI) · NCM811 값 **없음** · 우리 E_AM **140 은 이 논문에 없다** (113 과 200 사이) |
| "정본 Sedlatschek · Stallard 카드가 … 2 차 인용" | **채움** | [Sedl26] [27] → *"113 GPa · H 7.8 GPa · NMC532 다결정 2차입자"* = 그림 8 응집체 건조 평균 ✓ · [Stallard22] [74] → 그림 7 의 점 *"113 · 7.80 (막대 없음)"* ✓ · 그림 12A *"110 · 109 · 198 · 198"* = 이 논문 그림 8 의 **중앙** ✓ (아래 표) |
| "2019" | **채움 (온라인 2018)** | 머리글 *"Experimental Mechanics (2019) 59:337–347"* · *"Published online: 28 November 2018"* (p.1) — 가리킨 카드의 *"59 (3) (2018)"* 은 온라인 연도 · **호 "(3)" 은 PDF 에 없다** [미확인] |
| "NMC532" | **채움** | *"commercial LiNi0.5Mn0.3Co0.2O2 (NMC532)"* (p.2) · *"Commercial NMC532 powder (MTI Co.)"* (p.2) |
| "113 GPa" | **채움 (조건 한정)** | 그림 8a *"113"* = **응집체 · 건조 · 85 nm · 평균** (N 20 · SD 13.3 [카드 판독 · 산술]) — 같은 그림 wet 108 · 펠릿 200 / 201 · 49 nm 에서는 128.5 [판독 · 벡터] |

**가리킨 카드 · 같은 논문을 옮긴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `wang2027_…` L417 | 서지 *"Exp. Mech. 59 (3) (2018) 337–347"* · *"정본 Sedlatschek · Stallard 카드가 2019 · NMC532 113 GPa 로 2차 인용"* | 2019 (인쇄) · 온라인 2018-11-28 · 호 미인쇄 · 113 = 응집체 건조 평균 ✓ | **일부** — 값 ✓ · 서지 연도 · 호 ≠ 원문 (카드 문제 ①) |
| `wang2027_…` L28 · L89 · L316 | Wang 2027 원문이 *"138.73 ± 18.78 GPa (NCM) · 1.78 ± 0.35 GPa (CB/PVDF)"* 의 근거로 **[25, 26]** 을 함께 듦 | 이 논문 ([25]) 에 **138.73 · 1.78 없다** (응집체 113 · 108 · 펠릿 200 · 201 · CB/PVDF 필름 2.45 · 1.22 · 0.50 [판독] · PVDF 0.59) — 두 값은 [26] (`devasconcelos2016_…`) 의 targeted 값 | **없음 ([25] 에서)** — 카드 기록은 Wang 원문 그대로 (카드 문제 아님 · Wang 2027 의 인용 범위 과대) |
| `wang2027_…` L316 | *"[25] (Exp. Mech.) 의 값을 113 GPa · H 7.8 로 전한다"* ([Sedl26] 경유) | ✓ (응집체 · 건조 · 85 nm · 평균) | **채움** |
| `sedlatschek2026_…` L138 | [27] → **113 GPa · H 7.8 GPa · NMC532 다결정 2차입자** | ✓ — E 113 = 건조 (wet 108) · H 7.8 = 건조 · wet 둘 다 · "다결정 2차입자" = *"as-received hierarchical particles (small grains)"* (p.2) | **채움** |
| `stallard2022_…` L191 (그림 7) | *"7.80 (막대 없음) · 113 (막대 없음) — [Sedl26] 이 전한 [74] 113 · 7.8 과 정확히 같다 — 추정"* | 그림 8 응집체 건조 평균 (113 · 7.8) ✓ | **채움 (추정 → 확정)** |
| `stallard2022_…` L195 (그림 7) | *"13.99 [12.82, 14.16] · 200 (막대 없음) — [74] 펠릿과 근접 — 추정"* | 펠릿 건조 평균 E 200 · H 14.0 (점 평균 13.98 [판독]) ✓ · 괄호 [12.82, 14.16] 은 이 논문 상자 (Q1 13.62 · Q3 15.09) 와 다르다 | **일부** — 점 ✓ · 막대 출처 미상 |
| `stallard2022_…` L111 · L114 · L171–172 (그림 12A) | 이차입자 건 / 침지 **E 110 [105, 118] · H 7.56 [6.74, 8.88] / 109 [101, 118] · 7.46 [6.01, 9.74]** · 펠릿 **198 [192, 211] · 14.3 [13.5, 15.2] / 198 [181, 234] · 14.7 [12.2, 15.7]** · [74] (stated) | 이 논문 그림 8 의 **중앙 [Q1, Q3]** [판독 · 벡터]: 응집체 E **110.2 [105.1, 118.0] / 109.0 [101.3, 117.7]** · H **7.56 [6.72, 8.81] / 7.44 [6.01, 9.65]** · 펠릿 E **197.9 [192.8, 209.5] / 198.1 [181.7, 233.1]** · H **14.34 [13.62, 15.09] / 14.72 [12.27, 15.62]** | **채움** — ⚠ Stallard 그림 12A 는 **평균이 아니라 중앙 · 사분위** 를 옮겼다 (리뷰가 말하지 않음 [카드 해석]) |
| `stallard2022_…` L110 · L113 (그림 9) | NMC532 치밀 펠릿 **E 210 → 166** (A_P^½ 0.24 → 2.47 µm) · 이차입자 **126 → 51** · H 11.2 → 6.8 · 5.5 → 3.2 (0.59 → 2.59 µm) · [74] (추정) | **E = 이 논문 그림 7b** — 펠릿 211.3 (49 nm) → 167.2 (490 nm) · 입자 128.5 (49 nm) → 50.4 (508 nm) [판독 · 벡터] · A_P^½ = √24.5·h = 4.95 h 로 49 → 500 nm = **0.24 → 2.47 µm** [카드 산술] ✓ · **H 깊이 곡선은 이 논문에 없다** (그림 7 = 하중–변위 · E 만) | **E 채움 (추정 → 확정) · H 없음** (카드 문제 ②) |
| `stallard2022_…` L89 · L281 | *"low sensitivity to immersion"* [74] · *"1 M LiPF₆ in polypropylene carbonate"* (인쇄 그대로 · [74] 원문 미확인) | *"no apparent difference"* (p.7) ✓ · 전해질 = **"1 M LiPF6 in propylene carbonate (PC)"** (p.3) — 고분자 아님 | **채움** — 카드의 의심 (PPC 아닌 PC) 확정 |
| `kalnaus2023_…` L206 · L290 · L346 · L389 | *"single-crystal … 0.3 MPa m1/2 and … polycrystalline agglomerate particles … 0.1 MPa m1/2 (55)"* — 카드가 라벨 의심 · *"ref 55 원문으로 닫는다"* | 0.3 = **소결 다결정 펠릿** (결정립 3–10 µm) 건조 **0.298** (wet 0.291) · 0.1 = 응집체 건조 **0.104** (wet 0.212) — 값 ✓ · **"single-crystal" ✗** (원문 결론의 *"sintered pellet (large single particles)"* · *"within a single particle (sintered NMC pellet)"* p.6 가 그 낱말의 뿌리로 보인다 [카드 해석]) | **일부** — 값 채움 · 라벨 닫음 (단결정 아님) (카드 문제 ④) |
| `sharma2023_…` L109 · L188 | NMC532 **M 200.81 ± 33.61 (N 25) · H 14.29 ± 2.53 · K_c 0.296** — *"reproduced from our prior work"* [23] | 이 논문에 **그 수 그대로는 없다** — 가장 가까운 것 = 펠릿 E **200 · 201** (점 N 26 · 23 · SD 17.2 · 32.8 [판독]) · H **14.0 · 13.9** · K_c **0.298 · 0.291** (N 19 · 21) | **일부 (근접 · 같지 않음)** (카드 문제 ⑤) |
| `xu2017_…` L348 | *"7.8 · 8.9 는 같은 Zhao 그룹의 de Vasconcelos 2019 Exp. Mech. · 2016 EML"* | 7.8 = 응집체 건조 · wet 평균 ✓ | **채움** |
| `devasconcelos2016_…` L68 | *"[Sedl26] 의 매핑 (7.8 → [27] 2019) 이 맞는지는 [27] 원문이 필요 (이 논문으로 판정 불가)"* | 7.8 = [27] 그림 8b 응집체 평균 ✓ | **채움 (판정 가능해짐)** |
| `comparison_vs_ours_DEM.md` L4497 | *"[27]–[29] 원문이 7.8–8.9 GPa 를 확인하면 역산 3.85 는 그 규칙으로 기각"* | [27] = **7.8 확인** (응집체 · NMC532) · [28] = 8.89 (2016 카드) · [29] = 8.6 (`xu2017_…`) → 원전 셋 모두 7.8–8.9 확인 (단 **NMC532** · NCM811 2 차입자 값은 이 셋에 없음) | **채움 (조건 하나 남음: NCM811)** |

⇒ **의도 대조 결과: 채움 (113 GPa = 응집체 · 건조 · 85 nm 평균 · NMC532 · 1 차 측정 · Sedlatschek · Stallard 의 2 차 인용 값 맞음) · 일부 (c 의 일축 항복 · 크리프 없음 · 리튬화 · SOC 없음 · "NCM" = NMC532 · ± 미인쇄) · 2 차 인용 = wang2027 서지 연도 · 호, Stallard 그림 9 의 H 곡선 귀속, Kalnaus 의 "single-crystal", Sharma 2023 의 "재수록" 값이 원문과 다르다.**

---

## 1. 한 줄 요약
상용 NMC532 를 **응집체 (as-received 이차입자)** 와 **소결 펠릿 (결정립 3–10 µm)** 두 꼴로, 바인더 · 도전 기지를 **PVDF · CB/PVDF 필름** 으로 따로 만들어 Ar 글로브박스 안에서 **건조 ↔ 1 M LiPF₆-PC 에 담근 상태** 로 눌러 본 결과, NMC 의 E · H 는 전해질에 무관하고 (응집체 113 / 108 · 펠릿 200 / 201 GPa) 응집체의 *압입 인성* 만 두 배가 되며 (0.104 → 0.212 MPa m^½ · 모세관 다리 가설), 고분자 기지는 부풀고 크게 물러진다 (PVDF −50 % · CB/PVDF −80 %+) — 액체계 LIB 양극 구성 상의 "환경 속" 국소 물성 측정 논문이다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 · 소속 | 위 머리 상자 (Purdue 4) |
| 학술지 | *Experimental Mechanics* (2019) **59**:**337–347** (11 쪽) · © Society for Experimental Mechanics 2018 · 호 번호 인쇄 없음 |
| DOI | `10.1007/s11340-018-00451-6` (p.1 · PDF 메타데이터 *"Exp Mech, doi:10.1007/s11340-018-00451-6"*) |
| 이력 | 접수 2018-06-03 · 승인 2018-10-29 · 온라인 2018-11-28 |
| 연구유형 | 실험 (나노압입 · 환경 제어) + Rumpf 모세관 강도 어림 — 시뮬레이션 없음 |
| 시료 | NMC532 응집체 (PS 기지) · NMC532 소결 펠릿 · PVDF 필름 · CB/PVDF 필름 (기공 3 수준) · PS 기지 (대조) |
| 보충 자료 | ESM docx 10 개 (그림 S1–S8 · 표 S1–S2) — 전부 열람 · 크롭 · 원자료 공개 진술 없음 |
| 서지 메모와의 차이 | 후보 표 · `wang2027_…` L417 *"Exp. Mech. 59 (3) (2018) 337–347"* ↔ 원문 **(2019) 59:337–347 · 온라인 2018-11-28 · 호 미인쇄** · 원문 제목은 *"In-Situ Nanoindentation Measurement of Local Mechanical Behavior of a Li-Ion Battery Cathode in Liquid Electrolyte"* (대소문자만 다름) · 저자 · 쪽 · DOI 같음 |

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 시료 (p.2–3 · `txt_p2_p3_sample_prep_polish.png` · `txt_p3_pvdf_cbpvdf_films.png` · 그림 4 · 6 · 표 S1 · S2)
- **NMC 기지 선택**: *"The PVDF binder used in commercial batteries is known to soften in the electrolyte [43] and thus it is not suitable as the matrix for indentation tests on wet NMC. Hence, the inert polystyrene (PS) plastic is selected"* (p.2) — PS 를 ≈245 °C 로 녹이고 as-received NMC532 분말을 유리판으로 가볍게 눌러 박은 뒤 상온 냉각 (p.3).  PS 기지 E **3.8 GPa** · H **0.25 GPa** 가 전해질에서 그대로 (그림 5 · p.6) → 응집체 E 의 **1/30** [카드 산술].
- **펠릿**: as-received 분말을 볼밀 (스테인리스 용기 · 공 = NMC 전용 · 아세톤 · IPA 세척) 로 서브마이크론 일차입자로 → ≈1 g · 13 mm 다이 · *"applied compressive load of 5 tons (model 4350, Carvar)"* → **1000 °C 10 h** (10 °C/min · 노에서 냉각) (p.3).  5 톤을 미터 톤으로 읽으면 다이 면적 132.7 mm² 에 **≈370 MPa** (미국 톤이면 ≈335 MPa) [카드 산술 · 단위 [미확인]] — 소결 전 성형압일 뿐 소결체 밀도 · 기공 **미기재**.  XRD (Cu Kα · 2θ 10–80° · 40 mA · 45 kV) 가 기준 패턴과 맞음 = 조성 · 결정 구조 유지 (그림 4c · p.6).
- **결정립 · 일차입자**: *"The final grain size of the pellet (3–10 μm, Figure 4(a)) is significantly larger than the size of the primary particles in the as-received NMC sample (0.1–1 μm, Figure 4(b))."* (p.6 · `txt_p6_grain_size_ps_matrix.png`) · 이차입자 반지름 *"~10 μm"* (p.5) · *"(8–10 μm)"* (p.7) · targeted 대상 = 지름 ≥ 15 µm (p.3).
- **연마**: 두 시료 모두 0.05 µm 콜로이드 실리카 · imperial cloth (LECO) ≈30 min → 진공 80 °C 하룻밤 → 거칠기 ≈4 nm (이전 측정 [44]) (p.3).
- **PVDF · CB/PVDF 필름** (p.3): PVDF HSV900 (MTI · MW 600,000) 6 wt% / NMP → 순수 PVDF 필름 · 나머지에 CB (Super P · MTI) **50 : 50 wt%** → 진공 80 °C 며칠 → 두께 ≈**45 µm** (PVDF) · ≈**400 µm** (CB/PVDF) · 마이크로미터 (1 µm) · 저울 (0.1 mg) · 각 치수 ≥ 3 회 평균 → 밀도 **1.43 · 0.80 g/cm³** · CB/PVDF 셋을 롤 프레스로 기공 **50.8 · 27.5 · 3.8 %** (식 1: ε = [V_m − (w_m/2)(1/ρ_PVDF + 1/ρ_CB)]/V_m · ρ_PVDF **1.45** · ρ_CB **1.90 g/cm³**).

| 표 S1 (CB/PVDF) [인쇄] | 무게 mg | 처음 두께 µm | 누른 두께 µm | 처음 넓이 mm² | 나중 넓이 mm² | 나중 부피 mm³ | 이론 부피 mm³ | 기공 % |
|---|---|---|---|---|---|---|---|---|
| 1 | 20.5 | 336.7 | − | 75.3 | − | 25.4 | 12.5 | **50.8** |
| 2 | 22.1 | 398.8 | 200.0 | 81.0 | 92.7 | 18.5 | 13.4 | **27.5** |
| 3 | 47.1 | 421.4 | 185.3 | 124.8 | 160.6 | 29.8 | 28.6 | **3.8** |

| 표 S2 (PVDF · 1 h 담금) [인쇄] | 건조 무게 mg | 건조 두께 µm | 건조 넓이 mm² | 건조 부피 mm³ | 건조 밀도 mg/mm³ | 젖은 두께 µm | 젖은 넓이 mm² | 젖은 부피 mm³ | 부피 팽창 % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 11.1 | 49.6 | 157.0 | 7.8 | 1.43 | 54.3 | 187.8 | 10.2 | **30.8** |
| 2 | 6.1 | 69.0 | 62.5 | 4.3 | 1.42 | 75.4 | 74.6 | 5.6 | **30.5** |

- ⚠ **표 S1 캡션은 ρ_PVDF = 1.49 g/cm³** 라 적지만 본문 · 표 값은 **1.45** 로 계산됐다 — 1.45 이면 이론 부피 **12.46 · 13.44 · 28.64** (인쇄 12.5 · 13.4 · 28.6) · 기공 (넓이 × 두께 그대로) **50.84 · 27.53 · 3.77 %** (인쇄 50.8 · 27.5 · 3.8) · 1.49 이면 12.27 · 13.23 · 28.20 · **51.6 · 28.6 · 5.2 %** [카드 산술 §14 D18].  3.8 % 는 ρ_PVDF 0.04 차이로 ≈1.5 %p 움직인다.
- 표 S2 부피 팽창의 넓이 · 두께 몫 [카드 산술]: 넓이 **+19.6 · +19.4 %** · 두께 **+9.5 · +9.3 %** — 선 변형 ≈9.4 % 의 **등방 팽창** ((1.094)³ = 1.309) 과 맞는다.

### 3-2. ★ 압입 조건 (p.3–4 · `txt_p3_glovebox_electrolyte_soak.png` · `txt_p3_oliver_pharr_settings_targeted.png` · 식 2 · 3)
- **환경**: *"Nanoindentation (Keysight G200) tests are performed in an argon-filled glovebox (O2 and H2O < 0.5 ppm). Samples are tested in dry and wet conditions. In wet condition, a stainless-steel coin cell case is used as a container and samples are kept immersed in electrolyte. All samples are allowed to soak in the electrolyte for 1 h before indentation tests. The selected electrolyte, 1 M LiPF6 in propylene carbonate (PC) is nonvolatile, enabling a constant fluid level and salt concentration during tests."* (p.3) · 정확도 영향 없음은 이전 연구 [42].
- **Berkovich · Oliver–Pharr** (식 2 H = P/A · 식 3 2β√A_c/(S√π) = (1−ν²)/E + (1−ν_i²)/E_i): β **1.034** · E_i **1141 GPa** · ν_i **0.07** · CSM (조화 변위 **2 nm** · **45 Hz**) · *"The Poisson ratio of the sample, v, is assumed 0.3 for NMC and 0.4 for PVDF and CB/PVDF"* · 일정 Ṗ/P **0.05 s⁻¹** · 최대 깊이 **500 nm (NMC) · 2000 nm (PVDF · CB/PVDF)** · 필름 = 200 µm 간격 격자 · NMC = *"targeted indentations are conducted at the center of large NMC particles (minimum diameter of 15μm) to minimize the boundary effects"* (p.3).
- **보고 깊이 85 nm**: *"The dashed line in Figure 7(b) indicates the selected indentation depth (85 nm) to minimize material damage. This value represents the lowest indentation depth where the surface roughness is negligible while the area function calibration and surface contact detection remains accurate in our experiments."* (p.7 · `txt_p7_min15_depth_85nm.png`) — Berkovich 이상 면적이면 접촉 너비 √A ≈ **0.42 µm** [카드 산술] = 응집체 일차입자 (0.1–1 µm) 몇 개 · 펠릿 결정립 (3–10 µm) 하나 안.
- **시험 수**: *"a minimum of 15 indentations are performed for each configuration"* (p.7) — 그림 8 점 = 응집체 건조 **20** · wet **15** · 펠릿 건조 **26** · wet **23** (E · H 같은 점) [카드 판독].
- **깊이 의존 원인 (저자)**: *"(i) the substrate effect, and (ii) deep indentation induced material damage"* · 기지 무관 조건 = 경계에서 멀고 깊이 ≪ 이차입자 반지름 (8–10 µm) [44] (p.7).

### 3-3. ★ NMC E · H · K_c — 그림 8 (p.8 · `fig_8.png` · `fig_8a`–`8c` · `txt_p7_agglomerate_lower_kendall.png` · `txt_p7_no_difference_kc_ttest_hmin.png`)
그림 범례 (p.7): *"The grey circles represent individual indentations, the box indicates the 25–75% range, the white line is the median, and the average values are shown in the labels and indicated by the white squares."* · 수염 = 1.5 IQR (그림 안 범례).

| 양 | 시료 · 상태 | **평균 [인쇄]** | N [카드 판독] | SD [카드 산술] | 중앙 [Q1, Q3] [판독 · 벡터] | 최소–최대 [판독 · 벡터] |
|---|---|---|---|---|---|---|
| **E (GPa)** | 응집체 · 건조 | **113** | 20 | 13.3 | 110.2 [105.1, 118.0] | 93.3–152.3 |
| | 응집체 · wet | **108** | 15 | 12.8 | 109.0 [101.3, 117.7] | 86.8–128.4 |
| | 펠릿 · 건조 | **200** | 26 | 17.2 | 197.9 [192.8, 209.5] | 168.0–235.6 |
| | 펠릿 · wet | **201** | 23 | 32.8 | 198.1 [181.7, 233.1] | 142.2–258.6 |
| **H (GPa)** | 응집체 · 건조 | **7.8** | 20 | 1.66 | 7.56 [6.72, 8.81] | 5.22–11.11 |
| | 응집체 · wet | **7.8** | 15 | 1.87 | 7.44 [6.01, 9.65] | 5.44–10.60 |
| | 펠릿 · 건조 | **14.0** | 26 | 2.04 | 14.34 [13.62, 15.09] | 6.85–16.85 |
| | 펠릿 · wet | **13.9** | 23 | 2.63 | 14.72 [12.27, 15.62] | 8.46–18.19 |
| **K_c (MPa m^½)** | 응집체 · 건조 | **0.104** | 17 | 0.073 | 0.083 [0.054, 0.134] | 0.003–0.247 |
| | 응집체 · wet | **0.212** | 22 | 0.143 | 0.168 [0.085, 0.310] | 0.015–0.507 |
| | 펠릿 · 건조 | **0.298** | 19 | 0.150 | 0.226 [0.176, 0.429] | 0.124–0.635 |
| | 펠릿 · wet | **0.291** | 21 | 0.142 | 0.295 [0.173, 0.349] | 0.035–0.581 |

- 점 평균 ↔ 인쇄 평균 [카드 산술]: 112.8 · 107.8 · 200.3 · 200.9 · 7.80 · 7.77 · 13.98 · 13.87 · 0.1034 · 0.2119 · 0.2979 · 0.2908 — 12 묶음 모두 인쇄 값으로 반올림되고 흰 사각형 위치 (평균 표지) 와 4 자리까지 같다 ⇒ 판독 점 집합 완전.
- ★ 저자 문장: *"There is no apparent difference between the elastic modulus and hardness of NMC samples in dry versus wet condition. However, while the properties of sintered pellets remain mostly unchanged in the electrolyte, the average fracture toughness of the secondary particles is improved from 0.104 MPa m½ in the dry condition to 0.212 MPa m½ in the liquid environment. This difference is statistically significant according to the standard t-test (p value = 0.007)."* (p.7).
- t-검정 재현 [카드 산술 — 판독 점]: K_c 응집체 **합동 분산 p = 0.0072** (t −2.84 · 자유도 37 = 인쇄 0.007) · Welch p 0.0043 · 펠릿 K_c p 0.88 (그림 S4b 인쇄 *"p=0.88"* 과 같음) · E 응집체 p 0.27 · 펠릿 0.94 · H 0.96 · 0.87 → "차이 없음" 과 맞는다.
- 응집체 ÷ 펠릿 [카드 산술]: E **0.565** (건조) · 0.537 (wet) · H **0.557** · K_c (건조) **0.349** · H/E 는 둘 다 **≈0.069–0.070**.
- 저자 해석: *"Regardless of the environment effect, the mechanical properties of the agglomerated secondary particles are generally lower than those of sintered pellets. This difference is attributed to the weak interfaces between the primary particles in the NMC agglomerate."* · Kendall [64]: 응집체 안 입자 접촉이 유연성을 더해 집합체 E 를 낮춘다 — *"The modulus of the agglomerate is dependent on the packing ratio, the diameter of the primary particles, and the interfacial energy"* · 합성법 (형태 · 내부 기공 [65, 66]) 이 크게 영향 (p.7).
- *"The pellet experiment is approximate to the intrinsic properties of NMC in the bulk form, while the measurement of NMC secondary particles is dependent on the packing arrangement of the agglomerate, porosity, and physical interactions between the primary particles."* (p.7 · `txt_p6_p7_within_vs_across_intrinsic.png`) — 85 nm 압입이 펠릿에서는 **결정립 하나 안** · 응집체에서는 **일차입자 계면을 가로질러** 잰다 (p.6).
- wet 산포: *"for the secondary particles, the variation in the data is significantly higher in wet condition than in dry state. This variation is not observed for the pellet measurements. The large deviation is likely a result of heterogeneity in liquid saturation rather than random noise in the experiments."* (p.7) — K_c SD 0.073 → 0.143 (×1.96) [카드 산술].

### 3-4. ★ 깊이 의존 — 그림 7 (p.8 · `fig_7a.png` · `fig_7b.png` · `txt_p7_min15_depth_85nm.png`)

| 깊이 (nm) [판독 · 벡터] | 49 | 69 | 90 | 110 | 130 | 149 | 210 | 290 | 350 | 410 | 470 | 490 | 508 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 응집체 E 평균 (GPa) | **128.5** | 118.1 | 111.8 | 104.2 | 99.8 | 95.2 | — | 68.5 | — | — | 52.9 | 51.4 | **50.4** |
| 펠릿 E 평균 (GPa) | **211.3** | 209.3 | 204.2 | 201.6 | — | — | 190.8 | 183.8 | 178.2 | 173.9 | 169.3 | 167.2 | 169.3 |

(빈칸 = 그 깊이에 꺾은선 꼭짓점이 없음 — 곡선은 직선 조각.  28 nm 의 첫 꼭짓점 109.5 · 153.2 는 시작 구간.)
- 85 nm 내삽 [카드 산술]: 응집체 **113.3** (= 그림 8 의 113) · 펠릿 **205.4** (그림 8 의 200 보다 2.5 % 큼 — 그림 7 이 어느 상태 · 몇 회의 평균인지 원문 없음 [미확인]).
- 508 nm ÷ 85 nm: 응집체 **0.445** · 펠릿 **0.824** [카드 산술] — 응집체가 깊이에 훨씬 민감 (일차입자 계면 · 내부 기공 · 손상).
- 그림 7a (각 한 시험) [판독 · 벡터]: 펠릿 최대 **46.2 mN** (523 nm) → 제하 끝 361 nm (0.28 mN) ⇒ h_f/h_max **≈0.69** · 응집체 최대 **21.8 mN** (525 nm · 최대 깊이 530 nm) → 251 nm (0.21 mN) ⇒ **≈0.47** [카드 산술].
- ★ [Stallard22] 그림 9 의 NMC532 E 두 곡선 (210 → 166 · 126 → 51, A_P^½ 0.24 → 2.47 µm) = 이 그림 7b 를 A_P^½ = 4.95 h (Berkovich 이상 면적 24.5 h²) 로 다시 그린 것 [카드 산술 — 49 nm → 0.243 µm · 500 nm → 2.47 µm].

### 3-5. ★ K_c — 방법 · 자동 검출 · 버림 · 민감도 (p.3–5 · 그림 2 · S1 · S4–S8 · 식 4–6 · `txt_p3_p4_cube_corner_kc_effective.png` · `txt_p4_popin_field_method.png` · `txt_p4_hmin_100nm.png` · `txt_p5_outliers_crack_length_discard.png`)
- **식 4** (Lawn [46] · *"Antis"* [47] 인쇄 그대로, 반원 (half-penny) 균열): K_c = α (E/H)^½ P/c^{3/2} · α **0.036** (cube corner [48]) · *"equation (4) is still useful in the determination of an "effective" toughness, which allows for a quantitative comparison between the NMC materials in the dry and wet states, as the crack pattern is not expected to change from one state to the other"* (p.4).
- **식 5** (Field et al. [53] — 균열 길이를 팝인 변위로): c = √2 h_m + (Q E′/H − √2) h_x · Q **4.55** (cube corner) · h_x = h_m − h_t · h_t = 팝인 전 하중–변위를 **2 차 다항식** 으로 외삽 · E′ · H 는 Berkovich 값 (p.4–5).
- **식 6** (Morris et al. [54]): S̄ = S/S₁ (CSM 접촉 강성 ÷ 하중 곡선 순간 기울기) — 팝인 = S̄ 의 봉우리.  *"We define any observations above Q3 + 3 IQR or below Q1 − 3 IQR as outliers … all pop-in events (outliers) are detected above the upper boundary"* (p.5) · 그 아래 h_min (*"We choose hmin = 100nm"* p.4) — 얕은 구간의 탄소성 팝인 [55] 을 거름.
- 계산: 첫 팝인 뒤 **다섯 점**의 h_x → c → K_c 다섯 개 평균 · *"the average crack length in our experiments (~1 μm) is much smaller than the radius of the secondary particles (~10 μm)"* · *"only 6% of the total number of tests were automatically discarded by the following criteria: the extrapolated load-displacement curve yields a negative crack length (hx < 0), or no pop-in events are detected."* (p.5).
- ★ 버림 사슬 [카드 산술]: 그림 S1 의 시험 번호 = 응집체 건조 **19** · wet **25** · 펠릿 건조 **19** · wet **21** = **84** 회 [인쇄 (그림 축)] · 그림 S4 유효 비 (h_min 100 nm) **0.893 · 0.878 · 1.00 · 1.00** [판독 · 벡터] → 남은 수 **17 · 22 · 19 · 21** = 그림 8c 점 개수와 같다 · 버림 **5 / 84 = 5.95 %** = 인쇄 "6%".
- **그림 S4 (h_min 민감도)** [인쇄 — 그림 안 글자 · 유효 비는 판독 · 벡터]:

| h_min | 응집체 건조 | 응집체 wet | p | 펠릿 건조 | 펠릿 wet | p | 남은 수 (19 · 25 · 19 · 21 중) [카드 산술] |
|---|---|---|---|---|---|---|---|
| 50 nm | 0.096 | 0.192 | 0.027 | 0.289 | 0.248 | 0.46 | 16 · 21 · 18 · 21 (버림 8) |
| **100 nm** | **0.104** | **0.212** | **0.007** | **0.298** | **0.291** | **0.88** | 17 · 22 · 19 · 21 (버림 5) |
| 150 nm | 0.126 | 0.291 | 0.011 | 0.360 | 0.321 | 0.48 | 18 · 21 · 19 · 20 (버림 6) |

  *"The trend is the same, however, hmin = 100 nm results in the least number of discarded tests and at the same time, the least spread in the data."* (p.7) — ⚠ h_min 은 결과를 본 뒤 고른 값이다 (세 값 모두 같은 결론이라는 민감도로 막았다).  펠릿 K_c 자체는 h_min 50 → 150 에서 0.289 → 0.360 (**+25 %**) [카드 산술].

### 3-6. 액체 효과의 해석 — Rumpf 식 (p.7–9 · 식 7 · 8 · LEFM 줄 · `txt_p8_p9_capillary_estimate.png` · `txt_p9_model_caveats.png`)
- 결합 부류 (Rumpf & Schubert [68]): 물질 다리 없는 결합 (반데르발스 · 정전 · 자기) · 다리 있는 결합 (액체 · 고체) (p.7) · NMC 일차입자 (수백 nm) 는 반데르발스가 의미 있고 소성 조건에 따라 입계 화학 결합 가능 (p.8).
- **식 7**: σ_t = nF = 1.1 ((1−ε)/ε)(1/D²) F · **식 8** (모세관): σ_t = 6S ((1−ε)/ε)(γ/D) cosθ · PC 표면장력 **41.1 mN/m** [70] · θ **0** · S **0.95** · ε **0.028** [71] → *"~16 MPa for NMC primary particles bonded only by the capillary forces"* · K_IC = σ_t √(πa)/Y (a **1 µm** · Y **0.64**) → **+0.044 MPa m^½** ↔ 측정 *"median difference of 0.085 MPa m1/2 and average difference of 0.108 MPa m1/2"* (p.8–9).
- 카드 산술: 식 8 에 넣은 D 는 원문에 없다 → 16 MPa 를 내려면 **D ≈ 0.51 µm** (응집체 일차입자 0.1–1 µm 안) · ΔK = 16 × √(π·10⁻⁶)/0.64 = **0.0443** ✓ · 같은 a · Y 로 측정 K_c 를 거꾸로 하면 응집체 건조 **37.6 MPa** · wet **76.5** · 펠릿 **107.6** (§14 D23 · 원문에 없는 환산).  ε 0.028 의 출처 [71] 은 NCA (LiAlyNi1−x−yCoxO2) 사이클 시험 논문 — NMC532 측정값이 아니다 [카드 해석 · 참고문헌 제목].
- 저자 경고: *"It is worth noting that the analysis is based on an idealized model of spherical primary particles of a uniform size, while the as-synthesized NMC particles are polydisperse and of irregular shapes. In addition, previous work has shown that the Rumpf model may largely underestimate the strength of granular materials [64]."* · 다른 기전 가능 (LiPF₆ 분해물 (PF₅ · HF) 이 표면층을 만들어 *"nano-filler"* 로 작용 — Si 의 SiOx → SiOyFz 예 [29]) · *"Further experiments are necessary to fully understand the bonding nature of NMC agglomerates in the liquid environment."* (p.9).

### 3-7. 바인더 · 도전 기지 — 그림 3 · S2 · S3 (p.5–6 · `txt_p5_p6_pvdf_cbpvdf_swelling.png` · `txt_p6_binder_matrix_moduli_wet.png`)

| 시료 | 건조 E (GPa) [판독 · 벡터 ± SD] | wet E | 건조 H (GPa) | wet H | 비고 |
|---|---|---|---|---|---|
| PVDF 필름 | **0.594 ± 0.174** (인쇄 590 MPa) | 0.269 ± 0.070 (**−54.6 %**) | 0.0263 ± 0.0073 | 0.0129 ± 0.0052 (**−51.2 %**) | 부피 131.1 ± 7.7 % of dry (그림 3a) · 표 S2 30.8 · 30.5 % |
| CB/PVDF 3.8 % | **2.45 ± 0.11** | 0.318 ± 0.019 (−87.0 %) | 0.0720 ± 0.0053 | 0.0110 ± 0.0004 (−84.7 %) | |
| CB/PVDF 27.5 % | 1.22 ± 0.15 | 0.173 ± 0.010 (−85.8 %) | 0.0361 ± 0.0062 | 0.0072 ± 0.0004 (−80.0 %) | |
| CB/PVDF 50.8 % | 0.497 ± 0.016 | 0.096 ± 0.014 (−80.7 %) | 0.0156 ± 0.0007 | 0.0051 ± 0.0010 (**−67.1 %**) | |

- 인쇄: *"Electrolyte uptake causes a volume strain of roughly 30% in the PVDF film"* · CB/PVDF 는 *"the dense film expands 30% in volume as compared to 15% volume expansion for the porous film (50% porosity)"* (p.5 — 그림 없음) · PVDF 건조 590 MPa ≈ 인장 400–650 MPa [56, 59] · wet E · H *"drop by about 50%"* · CB/PVDF *"(2.5–2 GPa, Figure 3(d)) is about four times that of pure PVDF (0.59 GPa, Figure 3(b))"* · wet *"a decrease of over 80% in both modulus and hardness"* · *"In the wet state, the mechanical properties of PVDF and CB/PVDF are roughly the same, indicating that the carbon black loses most of its role"* (p.6).
- ⚠ 판독과의 차이 [카드 산술]: CB/PVDF 건조 E 는 **2.45 · 1.22 · 0.50** — 본문 *"2.5–2 GPa"* 는 가장 치밀한 필름 하나만 맞는다 (4 배 = 2.45 / 0.594 = **4.13**) · *"over 80% in both"* 은 50.8 % 필름의 H (−67 %) 에서 성립하지 않는다.
- 필름 두께는 깊이에 따른 기판 효과가 없을 만큼 (PVDF 50 · CB/PVDF 185–420 µm · 그림 S2 · S3) (p.6).

### 3-8. PS 기지 대조 — 그림 5 (p.7 · `fig_5.png`)
E **3.72–4.08 (건조) · 3.66–3.93 (1 h) · 3.74–3.97 GPa (6 일)** · H **0.23–0.28 · 0.24–0.26 · 0.22–0.30 GPa** (깊이 ≈45–1960 nm) [판독 · 벡터 · 범례 기호 3 개 제외] — 인쇄 *"the elastic modulus (3.8 GPa) and the hardness (0.25 GPa) of the PS matrix remain unchanged"* (p.6).

### 3-9. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (인쇄)**: ① α 의 방위 · 이방성 의존 → *"effective"* 인성 (p.4) ② 팝인 판정의 모호함 → 자동 알고리즘 · h_min · 민감도 (p.4–5 · p.7) ③ 깊이 의존 (기판 + 손상) → 85 nm (p.7) ④ 응집체 값 = 다짐 · 기공 · 상호작용 · 합성법 의존 (p.7) ⑤ wet 산포 = 포화도 불균일 (p.7) ⑥ Rumpf 이상화 · 과소 · 다른 기전 · 추가 실험 필요 (p.9) ⑦ 그림 6a 해상도 낮음 = PS 의 전기 전도 부족 (p.6) ⑧ 물성은 SOC · 사이클에 따라 변한다 (서론 · 이 논문은 재지 않음) (p.2).
**원문 안 어긋남 · 빈 곳 (이 카드가 찾은 것)**:
1. 표 S1 캡션 ρ_PVDF **1.49** ↔ 본문 · 표 계산 **1.45** (§3-1 · D18) [카드 산술].
2. 본문 CB/PVDF *"2.5–2 GPa"* ↔ 그림 3d 2.45 · 1.22 · 0.50 GPa · *"over 80 % in both"* ↔ 50.8 % H −67 % (§3-7) [판독 · 카드 산술].
3. 그림 4 캡션 *"reference pattern [58]"* ([58] = PVDF-HFP 고분자 전해질 논문) ↔ 본문 *"reference pattern [61]"* (Gu 2015 · Li1+xNi0.5Co0.2Mn0.3O2) [인쇄].
4. 그림 S1 캡션 *"(c) dry NMC pellet and (b) wet NMC pellet"* — 넷째 패널이 그림에서는 (d) [인쇄].
5. PVDF 필름 두께 *"approximately 45 μm"* (p.3) ↔ *"50"* (p.6) ↔ 표 S2 **49.6 · 69.0 µm** [인쇄].
6. *"Three CB/PVDF film samples are compressed … 50.8%, 27.5%, and 3.8%"* (p.3) ↔ 표 S1 시료 1 의 누른 두께 **"−"** (안 누름) [인쇄].
7. 식 4 의 출처 *"Lawn et al. [46] and Antis et al. [47]"* — [46] = Marshall · Lawn · Evans 1982 (측면 균열) · [47] = Chantikul · Anstis · … 1981 (II. strength method) · 직접 균열 측정 (I) 은 [49] 이고 [49] 는 **학술지 이름이 빠지고 권 "46"** 으로 인쇄 (짝 [47] 은 64:539–543) · [52] 제1 저자가 *"il JJ"* 로 잘려 인쇄 · 펠릿 프레스 *"Carvar"* (인쇄 그대로) [인쇄].
8. 제목 · 서론의 *"cathode … electrode"* (*"individual phases in a commercial … NMC532 electrode"* p.2) ↔ 실제 시료 = PS 에 박은 분말 · 소결 펠릿 · 따로 만든 필름 — 전극을 누른 측정은 없다 [카드 해석].
9. 그림 8 값의 ± · N **미인쇄** · 그림 7 이 어느 상태 · 몇 회 평균인지 미기재 (85 nm 펠릿 205 ↔ 그림 8 의 200) [미확인].
10. 결론 *"sintered pellet (large single particles)"* — 결정립 3–10 µm 의 **다결정 소결체** 를 "single" 로 부름 (2 차 인용에서 "single-crystal" 로 바뀐 뿌리 [카드 해석]).

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
NMC532 분말 (MTI) → (a) PS 에 박음 · 연마 (b) 볼밀 · 성형 · 1000 °C 소결 · 연마 → 진공 건조 → Ar 글로브박스 → 건조 압입 / 코인셀 케이스 속 1 M LiPF₆-PC 1 h 담금 뒤 압입 → Berkovich CSM (500 nm 까지 · 값은 85 nm) → E · H · cube-corner → 하중–변위 + S̄ → 자동 팝인 검출 (Q3 + 3IQR · h_min 100 nm) → h_t 외삽 · h_x → 식 5 c → 식 4 K_c (다섯 점 평균) → t-검정 · Rumpf 어림.  병행: PVDF · CB/PVDF 필름 (무게 · 치수 · 식 1 기공 · 1 h 담금 팽창) → 격자 압입 (2000 nm).

### 4-2. 입자 처리
- 측정 대상 = **우리 DEM 구 하나의 표면 근처 국소 물성** — 응집체 85 nm 압입은 일차입자 몇 개와 그 계면을 품는 부피 · 펠릿은 결정립 하나 안 (p.6).
- **입자 전체 (whole-particle) 유효 탄성률 · 입자 압축 · 접촉 강성 · 파쇄 하중은 재지 않았다.**  응집체의 K_c 는 *이차입자 안 일차입자 계면* 을 따라 가는 ≈1 µm 균열의 값이다.
- 우리 DEM: AM = **탄성 구** E **140 GPa** · ν **0.25** (AM_P · AM_S 같은 값) [우리 — `docs/data/real14_reference_20260928/input_real_14.liggghts` 29–30 행 · `devasconcelos2016_…` §4-2 가 옮김] · 우리 MPM: AM = 동결 scaffold.  우리 모델 해석: AM_P = 다결정 이차입자 · AM_S = 단결정 소입자 [우리 — CLAUDE.md A1 정정].

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
| 질문 | 원문 | 위치 |
|---|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계 | **말 없음** — DEM 을 쓰지 않는다.  입자 집합 모델에 대한 유일한 문장 = Rumpf (균일 구 집합의 결합 강도) 경고: *"the analysis is based on an idealized model of spherical primary particles of a uniform size, while the as-synthesized NMC particles are polydisperse and of irregular shapes. In addition, previous work has shown that the Rumpf model may largely underestimate the strength of granular materials [64]."* · 모델 쪽 쓰임: *"Results … will feed chemomechanical models"* (p.1) | p.9 (`txt_p9_model_caveats.png`) · p.1 |
| (ii) 입자 소성 · 큰 변형이 어려운 이유 · 우회 · 비용 | **말 없음 (모델 관점)** — 측정 쪽: 깊은 압입의 손상 (*"Potential crack formation and propagation in a brittle material induced by deep indentation is another reason of the decrease of modulus [62, 63]"*) · 얕은 쪽의 탄소성 팝인 [55] · 경도 (소성 저항) 를 재지만 일축 항복 · 입자 계산으로의 환산은 없다 | p.7 · p.4 |
| (iii) 2D 인가 3D 인가 · 2D → 3D | 말 없음 — 연마 단면 위 targeted 압입 (지름 ≥ 15 µm 입자 한가운데) · 깊이 ≪ 반지름 규칙 [44] | p.3 · p.7 |
| (iv) 압력을 뺄 때의 거동 | 전극 수준 탈압 **없음** — 압입 제하 곡선만 (그림 7a): 펠릿 h_f/h_max ≈0.69 · 응집체 ≈0.47 [판독 · 벡터] (응집체가 더 많이 되돌아옴 — 깊이 500 nm 의 E 가 펠릿의 0.30 배라 E/H 가 작아진 것과 맞는 방향 [카드 해석]) | 그림 7a · p.8 |

### 4-4. 기법 미니 용어집
- **in-situ (이 논문)**: 시료를 **전해질 속에 담근 채** (Ar 글로브박스) 누르는 것 — 전류를 흘리는 operando 가 아니다 (그것은 [42]).
- **CSM (continuous stiffness measurement)**: 하중에 작은 진동 (2 nm · 45 Hz) 을 얹어 깊이마다 접촉 강성 S 를 연속으로 재는 법 — E · H 를 깊이의 함수로 준다 (그림 7b · S2 · S3).
- **응집체 (agglomerate) · 이차입자**: 일차입자 (0.1–1 µm) 가 뭉친 '미트볼' 입자 · 85 nm 압입은 계면을 가로지른다.
- **소결 펠릿**: 볼밀 → 성형 → 1000 °C 로 결정립을 3–10 µm 로 키운 치밀체 — 85 nm 압입이 결정립 하나 안에 든다 ("intrinsic" 에 가까움).
- **팝인 (pop-in)**: 하중 중 압자가 갑자기 더 들어가는 사건 — 반원 균열이 생긴 표지 (Field [53]).
- **S̄ (reduced stiffness)**: S/S₁ — 팝인에서 봉우리가 서는 무차원 양 (Morris [54]).
- **Q3 + 3IQR**: 사분위 범위의 3 배를 넘는 값 = 이상치 = 팝인 (자동 · 사람 손 없음).
- **h_min**: 그보다 얕으면 균열이 없다고 보는 문턱 (100 nm).
- **effective toughness**: 식 4 의 α 를 고정해 얻은 비교용 인성 — 절대값이 아니라 같은 균열 꼴끼리의 비교값.
- **Rumpf 식**: 균일 구 집합의 인장 강도 = 단면 접촉 수 × 결합력 (식 7) · 모세관 다리면 식 8.

## 5. Figure set ★

| 그림 · 표 | 무엇을 보여주나 | 우리가 쓸 점 |
|---|---|---|
| **그림 1** (`fig_1.png`) | 전해질 속 복합 전극 도식 — 고분자 기지 팽창 · 연화, 일차입자 계면의 액체 다리가 계면 강도 증가 | 논문 가설 한 장 |
| **그림 2** (`fig_2.png` · `fig_2a` · `fig_2b`) | (a) 한 시험의 하중 (0–3 mN) · S̄ (0–100) vs 변위 (0–400 nm) — h_min · 팝인 (≈150 nm) · h_t 외삽 · h_x · h_m · P (b) 그 S̄ 의 분포 + Q3 + 3IQR (≈16) | ★ 자동 판정 규칙의 그림 — 우리 판정 기준 등록 (단계 0) 의 실례 |
| **그림 3** (`fig_3.png` · `fig_3a`–`fig_3e`) | PVDF 부피 · E · H 건조 ↔ wet · CB/PVDF E · H vs 기공 (3.8 · 27.5 · 50.8 %) | 액체계 바인더 연화 — 우리 계 (PTFE · 건식) 로 전이 없음 |
| **그림 4** (`fig_4.png` · `fig_4a`–`fig_4c`) | SEM 펠릿 (결정립 3–10 µm) · as-received 이차입자 (일차입자 0.1–1 µm) · XRD | 응집체 ↔ 치밀 결정립 구조 차이의 그림 |
| **그림 5** (`fig_5.png`) | PS 기지 E · H vs 깊이 — 건조 · 1 h · 6 일 | 기지 불변 대조 (측정 설계) |
| **그림 6** (`fig_6.png`) | 연마된 응집체 (PS 속) · 펠릿 위 압흔 SEM | targeted 압입 위치 |
| **그림 7** (`fig_7.png` · `fig_7a` · `fig_7b`) | (a) 펠릿 · 입자 하중–변위 (≤ 46 mN · ≈520 nm) (b) E vs 깊이 (평균 ± SD 띠) · 85 nm 점선 | ★ 국소 E 의 깊이 의존 (응집체 128.5 → 50.4) · [Stallard22] 그림 9 의 원자료 |
| **그림 8** (`fig_8.png` · `fig_8a`–`fig_8c`) | E · H · K_c 상자 그림 — 응집체 · 펠릿 × 건조 · wet · 평균 글자 113 · 108 · 200 · 201 · 7.8 · 7.8 · 14.0 · 13.9 · 0.104 · 0.212 · 0.298 · 0.291 | ★★ 이 카드의 숫자 원천 |
| **그림 9** (`fig_9.png`) | 일차입자 상호작용 도식 — 건조 (a) · 액체 다리 (b) | 모세관 가설 |
| **그림 S1** (`fig_S1.png`) | 시험마다 S̄ 상자 · 이상치 (+) — 19 · 25 · 19 · 21 시험 | 버림 사슬의 분모 |
| **그림 S2 · S3** (`fig_S2.png` · `fig_S3.png`) | PVDF · CB/PVDF E · H vs 깊이 (건조 · wet · ± 띠) | 기판 효과 없음 근거 |
| **그림 S4** (`fig_S4.png`) | h_min 50 · 100 · 150 nm 의 K_c 상자 + p 값 + 유효 시험 비 | ★ 판정 문턱 민감도 보고의 실례 |
| **그림 S5–S8** (`fig_S5.png`–`fig_S8.png`) | 시험마다 (a) S̄ · 하중 · 컷오프 (b) 팝인 뒤 다섯 점 K_c — 건조 펠릿 · wet 펠릿 · 건조 입자 · wet 입자 | 개별 시험 추적 (판독하지 않음) |
| **표 S1 · S2** (`tab_S1.png` · `tab_S2.png`) | CB/PVDF 기공 산출 · PVDF 1 h 팽창 | 무게-치수 기공 연산자 · ρ 1.45 ↔ 1.49 |
| 식 1–8 + LEFM 줄 (`eq_01`–`eq_09`) | 기공 · H · E_r · K_c · 균열 길이 · S̄ · Rumpf · 모세관 · K_IC | 보고서 붙임용 |

### 5-1. 크롭 색인 — `litdb/figures/devasconcelos2019_insitu_nanoindentation_nmc532_liquid_electrolyte/`
- 도구 (`tools/litdb/extract_figures.py`, 300 dpi) 14 장 — **그대로 3** (`fig_1` · `fig_6` · `tab_S2` (캡션만 정리)) · **다시 자름 11**: `fig_3` (위 줄 일부만 · 패널 d · e 잘림) · `fig_5` (틀 윗변 · 범례 잘림) · `fig_9` (패널 글자 (a)(b) 잘림 + 캡션에 본문이 이어 붙음) · `fig_S2`–`fig_S8` (쪽 폭 상자 · 여백 넓고 고르지 않음) · `tab_S1` (docx 머리 "Supplementary Information" 포함 + 표 글자 전체가 캡션).
- 도구가 놓친 번호 5 (그림 2 · 4 · 7 · 8 = 옆 캡션 · S1 = docx 쪽에 그래픽 없음) → **손 그림 크롭 5**.  손 크롭 합 49 = 그림 5 + 패널 15 (`fig_2a` `2b` · `3a`–`3e` · `4a` `4b` `4c` · `7a` `7b` · `8a` `8b` `8c`) + 식 9 (`eq_01`–`eq_08` = 식 1–8 · `eq_09` = 번호 없는 LEFM 줄) + 근거 문단 20 (`txt_p1_…` – `txt_p9_…`).
- `fig_8b` 는 이웃 패널 (c) 축 제목의 'F' 한 글자가 클립 안에 들어와 그 3.6 × 12 pt 를 흰색으로 지웠다 (figures.json manual_crop 에 기록).  `eq_05` · `eq_06` 은 첫 재단이 정의 줄 · 분모 S₁ 을 잘라 다시 잘랐다.
- ESM 그림 · 표 = docx 의 EMF · TIFF 를 LibreOffice 로 PDF 바꾼 1 쪽에서 자름 — 변환에서 OMML 수식 (Q1 · Q3 · S̄ · h_min · µm 단위) 이 빠져 캡션 · note 에 document.xml 의 글자로 되살렸다.
- 63 장 전부 Read 로 열어 확인 (잘림 · 이웃 문단 · 쪽 머리글 없음).  여백 = 흰 화소를 덧붙여 만듦 (클립을 넓히지 않음).

## 6. Post-processing ★
- E · H: Oliver–Pharr [45] · CSM · ν 0.3 / 0.4 가정 · 면적 함수 = *"experimentally calibrated function"* · 값 = 85 nm (NMC) · 필름은 깊이 평균 (그림 S2 · S3 · 방식 미기재).
- K_c: 자체 알고리즘 (S̄ 이상치 · h_min · 2 차 다항 외삽 · 다섯 점 평균 · 자동 버림 두 기준) · 소프트웨어 이름 · 코드 공개 **없음**.
- 통계: 표준 t-검정 (등분산 여부 미기재 — 판독 점으로 합동 분산 0.0072 · Welch 0.0043 [카드 산술]).
- 기공 · 팽창: 마이크로미터 · 저울 (≥ 3 회 평균) · 식 1.
- 이 카드의 판독: 그림 3 · 5 · 7 · 8 은 PDF 벡터 경로 (PyMuPDF `get_drawings`) — 눈금 선 위치와 인쇄 눈금 글자로 최소제곱 선형 환산 · 그림 8 = 회색 원 중심 (채움 · 획이 따로 그려진 원 포함 · 범례 기호 제외) · 상자 · 중앙선 · 흰 사각형 · 수염 · 그림 3 = 막대 윗변 · 원 중심 · SD 뚜껑 선 (길이 3–12.5 pt) · 그림 7 = 꺾은선 꼭짓점 · 그림 S4 = 초록 사각형 중심 ↔ 초록 눈금 글자.  재현 = `digitized.csv` 의 note 칸 (경로 번호 · pt 좌표 · 축 눈금).

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 정본 카드 · CLAUDE.md 가 적은 출처를 그 자리에 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 상태가 다르다** — 이 논문 = NMC532 · pristine · 액체계 · 국소 압입)

| 항목 | 이 논문 | 우리 | 판정 (판정 없이 나란히 · 차이의 이유) |
|---|---|---|---|
| **E_AM** | 응집체 **113** (건조) · 108 (wet) · 소결 펠릿 **200** · 201 GPa (85 nm) · 응집체 49 → 508 nm 128.5 → 50.4 [판독] | DEM **140 GPa** (AM_P · AM_S) [우리 — `input_real_14.liggghts` L29] | 140 = 응집체의 **+23.9 %** · 펠릿의 **−30.0 %** [카드 산술] — 두 시료 사이.  우리 해석상 AM_P (다결정 이차입자) ↔ 응집체 · AM_S (단결정) ↔ 결정립 (펠릿) 이면 **한 값 140 이 둘 다에서 비켜 있다** (⚠ NMC532 ↔ NCM811) |
| **E/(1−ν²)** · AM–AM 접촉 E* (같은 두 구 = E/(2(1−ν²))) | 113 (ν 0.3) → **124.2** · E* 62.1 · 200 → **219.8** · E* 109.9 | 140 (ν 0.25) → **149.3** · E* **74.7** | 우리 E* = 응집체의 **+20.3 %** · 펠릿의 **−32.1 %** [카드 산술] (AM–SE 접촉은 SE 연화가 지배 — [Sedl26] §7.2) |
| **ν_AM** | **0.3 가정** | 0.25 [우리 — L30] | 이 논문은 ν 의 출처가 될 수 없다 |
| **H_AM** | 응집체 **7.8** · 펠릿 **14.0** (85 nm) | `am_load_balance_jam.py` `--h-am` 기본 **4.0** (*"NCM811 계 문헌대 ≈ 3~6"*) · `fracture_model.py` H_AM **6.0** [우리 — `devasconcelos2016_…` §7-1 이 옮김] | 응집체 ÷ 4.0 = **1.95** · 펠릿 ÷ 4.0 = **3.5** · 응집체 ÷ 6.0 = 1.30 [카드 산술] — **우리 "3–6 GPa" 밴드 밖 (위)** · [Sedl26] §8 ② · [Xu17-NMC] §7-2 · [deVasc16] 의 결론을 세 번째 원전에서 확인 |
| **K_IC_AM** | 응집체 (일차입자 계면) **0.104** (건조) · 0.212 (wet) · 펠릿 **0.298** · 0.291 MPa m^½ (*"effective"*) | `fracture_model.py` **K_IC_AM_P 0.3** (*"polycryst secondary NCM, Quinn 2020"* — 출처 미확인) · **K_IC_AM_S 1.0** (*"Liu 2020"* — 출처 미확인) [다른 카드 — `xu2017_…` §7 · `kalnaus2023_…` L346] | ★ 0.3 = **펠릿 (결정립 안) 값 0.298** 과 같고 **응집체 계면 0.104 의 2.9 배** [카드 산술] — 우리 AM_P 가 다결정 이차입자라면 같은 그룹 [Xu17-NMC] (0.102) 에 이어 **두 번째 원전** 이 "AM_P 0.3 은 펠릿 라벨" 을 가리킨다 · 1.0 의 짝은 이 논문에 없다 (펠릿 0.298 의 3.4 배) |
| AM : SE 강성 대비 | (SE 없음) | LPSCl 압입 E 27.6 · H 1.41 [다른 카드 `lee2025_…`] · DEM E_eff 1.35 · MPM E 1.53 [우리 CLAUDE.md] | E 113 ÷ 27.6 = **4.1** · 200 ÷ 27.6 = **7.2** · ÷ 1.35 = 84 · 148 · ÷ 1.53 = 74 · 131 · H 7.8 ÷ 1.41 = **5.5** · 14.0 ÷ 1.41 = **9.9** [카드 산술] |
| 바인더 강성 | PVDF **0.59 → 0.27 GPa** (wet) · CB/PVDF 0.50–2.45 → 0.10–0.32 GPa | MPM 첨가제 표 PTFE **1.80** GPa (*"사용자 지정 · 근거 미기재"*) [우리 — `devasconcelos2016_…` §7-1 이 옮김] | PTFE 값 없음 · 액체 팽창은 우리 계에 없음 — 비교 0 |
| 전해질 영향 | NMC E · H 불변 · 응집체 K_c ×2.04 (모세관) | 황화물 ASSB — 액체 없음 | ★ 우리 쪽에 맞는 값 = **건조 (Ar 글로브박스) 값** · wet 증가분은 옮기지 않는다 |
| 시료 상태 | pristine 분말 · 리튬화 · SOC · 사이클 없음 · 펠릿 = 1000 °C 소결체 (성형 ≈370 MPa [카드 산술 · 단위 미확인]) | 300 MPa 냉간 압밀 복합 · 사이클 원장 (A10) | 같은 표에 넣지 않는 조건 · SOC 의존은 [Xu17-NMC] (E 145 → 112 · SOC 0 → 100 %) [다른 카드] |

### 7-2. ★ 정의 대조 — "같은 이름 · 다른 양"
- **"E_NCM ≈ 113 GPa"** = as-received NMC532 이차입자 응집체 한가운데 · **깊이 85 nm** · ν 0.3 가정 · Berkovich CSM — 입자 전체 압축 탄성률 · DEM 접촉 E* 가 **아니다**.  같은 응집체를 500 nm 로 누르면 50 GPa.
- **"E ≈ 200 GPa (펠릿)"** = 소결 결정립 하나 안 (3–10 µm) — *"intrinsic … bulk form"* 에 가까운 값 · 단결정 시료 측정이 아니다.
- **"H_AM"** = Oliver–Pharr 압입 경도 — 우리 `am_load_balance_jam.py` 의 H_AM (*"AM 크라운이 버티는 접촉 평균압"*) 과 이름만 같다 ([Sedl26] §7.5).
- **"K_c"** = cube-corner 팝인 · α 고정 · 균열 길이 추정의 *effective* 압입 인성 — 응집체에서는 **일차입자 계면** 의 값 · 우리 Auerbach 의 K_IC (입자 파쇄 문턱) 와 같은 양으로 쓰려면 라벨 (계면 · 결정립 안) 을 먼저 정한다.
- **"in-situ"** = 전해질 속 (operando 아님).
- **"wet"** = 1 h 담금 · 포화도 미측정.

### 7-3. 나란히 놓을 정본 카드 (값 · 조건 그대로 · 기존 카드는 고치지 않는다)

| 카드 | 재료 · 방법 | E (GPa) | H (GPa) | K_c (MPa m^½) | 이 카드와의 관계 |
|---|---|---|---|---|---|
| **이 카드** | NMC532 응집체 · 건조 / wet · 85 nm · ν 0.3 | **113 / 108** | **7.8 / 7.8** | **0.104 / 0.212** | — |
| 이 카드 (펠릿) | NMC532 소결 펠릿 (3–10 µm) | 200 / 201 | 14.0 / 13.9 | 0.298 / 0.291 | 같은 논문 |
| `devasconcelos2016_…` | NMC532 (Toda) 전극 속 이차입자 · targeted 75–150 nm | 138.73 ± 18.78 (격자 123.02) | 8.89 (격자 7.78) | — | 같은 그룹 · 같은 조성 — 비슷한 깊이 (90 ↔ 97 nm) 에서 이 카드가 **0.79 배** (111.8 ↔ 141.2) [카드 산술] · 차이 원인 원문 없음 (분말 · 기지 · CSM) |
| `xu2017_…` | NMC532 이차입자 · Berkovich 1 mN · 소결 펠릿 | 142.5 ± 11.3 · 펠릿 177.5 ± 19.5 | 8.6 ± 1.3 · 12.6 ± 1.4 | 0.102 ± 0.03 · 0.309 ± 0.04 | 이 논문의 [44] · K_c 는 건조 값과 같은 자릿수 (0.104 · 0.298) |
| `sedlatschek2026_…` | NCM811 2 차입자 단면 · Berkovich CSM 5 mN · ν 0.32 · n 29 | 138 ± 24 | — | — | 다른 조성 · [27] 로 이 논문 인용 |
| `sharma2023_…` | NMC811 소결 펠릿 · NMC532 "재수록" | 229.9 ± 40.55 · (532) 200.81 ± 33.61 | 14.17 · (532) 14.29 | 0.271 · (532) 0.296 | 532 값 = 이 논문 펠릿과 근접 · 같지 않음 |
| `stallard2022_…` | 리뷰 그림 7 · 9 · 12A | 113 · 200 · 110 / 198 (중앙) | 7.8 · 14.0 | — | 이 논문 그림 7b · 8 을 옮김 |
| `lee2025_…` | Li₆PS₅Cl 펠릿 나노압입 | 27.6 | 1.41 ± 0.24 | — | SE 쪽 짝 (다른 재료) |
| `dang2019_…` | NMC111 이차입자 평판 압축 강도 | — | — | (강도 188 MPa · c 2.8/π) | 입자 전체 파쇄 층 (이 논문은 계면 압입 층) |

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **AM 국소 기계 물성 (E · H · 계면 인성) 측정 + 환경 (전해질) 효과** — 우리 분업으로는 DEM 접촉 E* · Auerbach K_IC · MPM AM 탄성 (A′ · B 에서) 의 **입력 물성 쪽**.
- 없는 반쪽: 입자 전체 압축 · 접촉 강성 · 고체전해질 · 압밀 · 탈압 · 수송 · 리튬화.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = NMC532 (응집체 · 소결 펠릿) + PVDF · CB/PVDF — **SE 가 없고** · 압밀이 없고 · AM 조성도 다르다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **판정 규칙을 기계적으로 고정한 실례** — 팝인 = S̄ > Q3 + 3IQR · h_min 100 nm · 첫 팝인 뒤 다섯 점 · 자동 버림 두 기준 (h_x < 0 · 팝인 없음) · *"load-displacements curves not are manually selected or removed by the user"* (p.5) · ★ **문턱 민감도 보고** (그림 S4: h_min 50 · 100 · 150 nm 에서 결론 같음 · 버림 8 · 5 · 6) — ⚠ 단 h_min · 85 nm 는 **결과를 본 뒤** 골랐다 (최소 버림 · 최소 산포) → 우리는 문턱을 결과 전에 적고 민감도는 덧붙임으로 · ★ **무게-치수 기공 연산자** (식 1) 와 **밀도 하나 (1.45 ↔ 1.49) 가 3.8 % 기공을 ≈1.5 %p 움직인 실례** [카드 산술] → 기공 칸에 진밀도 출처를 항마다 적는다 | 진밀도 · 압력 의존 · SE 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 (모델 없음) | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | **측정 설계 하나**: 시료를 붙잡는 기지가 시험 환경에서 변하지 않음을 **먼저** 확인 (PS · 건조 · 1 h · 6 일 · 그림 5) 한 뒤에야 변화를 입자 탓으로 돌린다 — 우리 SE 압입 앵커 (`lee2025_…`) 에 수분 · 시간 노출 대조를 붙일 때의 꼴 | SE 숫자 0 · LPSCl 아님 |
| **단계 5** (3D 복합 압밀) | AM 탄성 입력의 **띠** — NMC532 응집체 **113** · 결정립 **200 GPa** (85 nm) · AM : 실제 SE 강성 **4.1–7.2** (E) · **5.5–9.9** (H) [카드 산술] · 응집체 E 의 깊이 의존 128.5 → 50.4 (49 → 508 nm) | 입자 전체 E · 압밀 응력 · AM 하중 몫 없음 |
| **단계 6** (탈압 · 되돌아옴) | 압입 수준의 되돌아옴 두 곡선 — h_f/h_max 펠릿 ≈0.69 · 응집체 ≈0.47 (≈520 nm · Berkovich) [판독 · 벡터] — AM 쪽 국소 되돌아옴의 크기 | 전극 수준 탈압 · 두께 회복 없음 |
| **단계 7** (형상 · 피복 · 수송) | 없음 (액체계 바인더 팽창이 기공을 메운다는 정성 — *"would occupy pore spaces … could affect the ion transport"* p.5 · 우리 계에 없음) | 수송 값 없음 |
| **후보 D0** (지금 DEM) | ★ **E_AM 140 의 원전 쪽 위치** — NMC532 응집체 113 (+23.9 %) ↔ 결정립 200 (−30 %) 사이 · AM–AM E* 로 +20.3 % · −32.1 % [카드 산술] · AM_P (다결정) ↔ AM_S (단결정) 를 한 E 로 둔 것의 문헌 폭 · ★ **H_AM "3–6 GPa" 밴드에 원전 반례 셋째** (7.8 · 14.0) · ★ **K_IC_AM_P 0.3 = 펠릿 라벨** (응집체 계면 0.104) | 입자 전체 · 접촉 강성 측정 아님 · NMC532 · ν 가정 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | — |
| **후보 A** (MPM 강체 AM · SE 한 속도장) | AM 을 강체로 둘 근거의 숫자 — AM : SE 경도 비 5.5–9.9 · 탄성 비 4.1–7.2 (실제 SE) · 우리 MPM SE (E 1.53) 대비 74–131 [카드 산술] | 강체 근사 오차 · 접촉 응력 분포 없음 |
| **후보 A′** (입자별 속도장 · 다물체 마찰 접촉) | AM 을 탄성체로 풀 때 응집체 ↔ 결정립 두 E (113 · 200) · ν 미측정 (0.3 가정) | 마찰 · 접촉 법칙 · NCM811 없음 |
| **후보 B** (입자별 FE + 접촉) | ★ 다결정 이차입자를 **균질 탄성 구** 로 둘 때의 경고 — 같은 입자가 85 nm 113 · 508 nm 50 GPa (응집체) vs 205 → 169 (결정립) · 저자 원인 = 기판 효과 + 손상 · 응집체 E 는 *"packing ratio, the diameter of the primary particles, and the interfacial energy"* 에 의존 (Kendall [64]) → 입자 FE 의 균질 E 는 "국소 압입값" 이 아니라 **입자 전체 유연성** (일차입자 계면 포함) 으로 정해야 하고 그 값은 이 논문에 없다 | 입자 전체 압축 곡선 없음 |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | AM (E, H) 쌍 — H/E ≈**0.069** (응집체 · 펠릿 같음) · LPSCl 0.051 [다른 카드] · 경도 → 항복 환산은 원문 없음 (H/3 은 취성 세라믹 항복 아님 — [StallardJES22] 독립 슬립계 조건) | 일축 항복 · 크리프 · 큰 변형 없음 |
| **후보 C′** (항복 캡 탄소성 접촉 DEM · Thornton–Ning 류) | AM–AM 접촉 항복압 자릿수 = 압입 경도 **7.8 (응집체) – 14.0 GPa (결정립)** — 300 MPa 압밀의 평균 접촉압은 이보다 한참 아래 [카드 해석] | 접촉 수준 항복 측정 아님 |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 없음 | — |
| **U0–U6** | **U3** (단단한 압자로 눌렀다 떼기) 의 **실측 형태 둘** — Berkovich · NMC532 · 펠릿 46.2 mN / 523 nm → h_f 361 nm · 응집체 21.8 mN / 525 nm → 251 nm [판독 · 벡터] (압자 · 재료 모두 U3 와 다름 — 형태 대조만) · **U1 · U6** 유비: *"indentation depth is chosen much less than the secondary particle radius"* · 균열 ≈1 µm ≪ 반지름 ≈10 µm = "탐침 ≪ 입자" 규칙 (우리 지름당 셀 수 · d_h/dx 규칙과 같은 꼴 [카드 해석]) | U0 · U2 · U4 · U5 없음 |
| **R1–R7** | **R7** (AM 파괴) — ★ 다결정 이차입자의 파괴 단위 = **일차입자 계면** (K_c 0.104 · 결정립 안 0.298 의 1/3) · 같은 a = 1 µm · Y 0.64 로 거꾸로 하면 계면 응력 37.6 MPa (건조) [카드 산술 · 원문 없음] · **R4** — 압입 수준 되돌아옴 두 곡선 · **R1** — 없음 (액체계 · 단일 입자 압입) · **R5** — 맞춘 값 = 식 5 의 Q · 식 4 의 α (문헌 상수 고정 · 이 논문이 맞추지 않음) · h_min · 85 nm (결과 보고 고름) | R2 · R3 · R6 없음 |
| **결과 전 대조 항목** | ① AM 국소 E 띠 **113 (응집체) – 200 GPa (결정립)** (NMC532 · 85 nm · 건조 Ar) — 우리 E_AM 입력 · AM_P/AM_S 구분 여부를 이 띠에 대고 적는다 (맞추지 않음) ② AM 압입 경도 **7.8 – 14.0 GPa** — H_AM 을 "압입 경도" 라 부를 때의 기준 (우리 4.0 · 6.0 밖) ③ AM 계면 · 결정립 인성 **0.104 · 0.298 MPa m^½** — K_IC_AM_P 라벨 결정의 기준 (같은 그룹 [Xu17-NMC] 0.102 · 0.309 와 함께) ④ wet 값 · PVDF · CB/PVDF 는 **넣지 않는다** | LPSCl · NCM811 값 아님 · 우리 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: AM (NMC532 ↔ NCM811) · 계 (액체계 ↔ 황화물 ASSB) · 환경 (Ar 건조 / LiPF₆-PC ↔ 건조 · 황화물) · 상태 (pristine 분말 · 소결체 ↔ 300 MPa 압밀 복합) · 측정 (표면 국소 85 nm ↔ 입자 전체 접촉) · ν (0.3 가정 ↔ 0.25).
- **사이클 원장 (cycle_contact_ledger · A10) 의 AM 강성 가정과 견줄 자리** [우리 — CLAUDE.md A10]: 원장은 AM 을 수축만 하는 **강체** 로 두고 (AM–AM 은 재폐합 · CZM 은 AM–SE · SE–SE 만) poly AM 의 입계 void 를 `poly_internal_void_frac` (ASSUMED-FORM · 앵커 대기) 로 따로 적는다 — 이 논문은 ① 응집체가 결정립보다 **E 0.57 배 · K 0.35 배** 로 무르고 약하다 (일차입자 계면 탓 · 저자) 는 pristine 앵커 ② 계면 인성 0.104 MPa m^½ (건조) 를 준다.  **리튬화 · 사이클에 따른 변화는 없다** — 그쪽 앵커는 [Xu17-NMC] (K_c 0.102 → 0.058 (SOC 100 %) → 0.036 (100 사이클)) [다른 카드].  ⚠ 액체 속 K_c 증가 (모세관) 는 ASSB 사이클 원장에 옮기지 않는다 (액체 없음).

## 9. 적용 인사이트 (행동)
1. **E_AM 140 GPa 출처 문장 (D0 · 표 S2) 에 NMC532 의 두 층을 함께 적는다**: *"NMC532 (as-received secondary particles, Berkovich at 85 nm, Ar glovebox): 113 GPa (dry) / 108 GPa (in 1 M LiPF6-PC); sintered pellet (grains 3–10 µm): 200 / 201 GPa (de Vasconcelos et al., Exp. Mech. 59 (2019) 337–347)"* — ⛔ *"140 GPa (de Vasconcelos 2019)"* 금지 (140 은 이 논문에 없다).
2. **K_IC_AM_P 0.3 의 라벨 (R7 · `fracture_model.py`)**: 이 논문과 [Xu17-NMC] 가 같은 수 짝 (0.30 결정립 · 0.10 계면) 을 준다 — 0.3 을 "다결정 이차입자" 라 부르면 원전 둘과 어긋난다.  처방 (재명명 또는 값 · 근거 재등록) 은 런 전 등록으로 — 이 카드는 코드를 바꾸지 않는다.
3. **H_AM "3–6 GPa" 문구 (D0 · `am_load_balance_jam.py`)**: 원전 셋째 (7.8 · 14.0) 도 밴드 밖 — [Sedl26] §8 ② 의 등록 규칙 (*"역산값이 그 밴드 밖이면 모델이 틀린 것"*) 조건 가운데 'NMC532 원전 확인' 은 [27] [28] [29] 셋 모두 채움 · 'NCM811 이차입자 값' 만 남는다.
4. **판정 문턱의 꼴 (단계 0)**: 이 논문의 자동 판정 (Q3 + 3IQR · h_min · 다섯 점 · 버림 기준 두 개) + 민감도 표 (S4) 는 우리 등록 문서의 "판정 규칙 + 민감도" 칸의 좋은 본 — 단 문턱은 결과 전에 적는다 (이 논문은 결과 뒤 골랐다).
5. **2 차 인용 정리**: Stallard 그림 12A = 이 논문의 **중앙** (평균 아님) · Stallard 그림 9 의 NMC532 E 곡선 = 이 논문 그림 7b · 같은 그림의 H 곡선은 이 논문 아님 · Kalnaus 의 "single-crystal 0.3" = 소결 펠릿 · Sharma 2023 의 NMC532 "재수록" 값은 이 논문에 그대로 없음 — 비교 문서 §G [deVasc19] 에 적었다 (기존 줄은 그대로).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Berkovich nanoindentation (85 nm, Ar glovebox) of as-received NMC532 secondary particles embedded in polystyrene gave E = 113 GPa and H = 7.8 GPa (mean of 20 indents), and of a sintered NMC532 pellet (grains 3–10 µm) E = 200 GPa and H = 14.0 GPa; soaking in 1 M LiPF6-PC for 1 h left both unchanged (108 / 7.8 and 201 / 13.9 GPa) (de Vasconcelos et al., *Exp. Mech.* 59 (2019) 337–347)."
- "Cube-corner pop-in indentation gave an effective toughness of 0.104 MPa m^1/2 for the primary-particle interfaces of dry NMC532 agglomerates versus 0.298 MPa m^1/2 within sintered grains; in the liquid electrolyte the agglomerate value doubled to 0.212 MPa m^1/2 (t-test p = 0.007), which the authors attribute to capillary bridging."
- 국문 (한정어와 함께): *"NMC532 이차입자 (응집체) 의 국소 탄성률은 Berkovich 85 nm 에서 113 GPa · 경도 7.8 GPa 이고 같은 조성의 소결 결정립은 200 · 14.0 GPa 다 (de Vasconcelos 2019 · 건조 Ar · ν 0.3 가정 · 평균 · ± 미인쇄) — 응집체가 무른 원인은 일차입자 계면 (저자)."*
- ⛔ 쓰지 말 것: *"NCM 의 탄성률 113 GPa"* 를 NCM811 · 입자 전체 값처럼 · *"NMC532 single-crystal K_IC 0.3"* (소결 펠릿) · *"전해질이 NMC 를 강하게 한다"* 를 ASSB 에 (액체 모세관 · 1 h 담금 · 응집체 계면 인성만).

## 11. 주의/한계 (over-claim 방지)
1. **NMC532 · pristine · 액체계 환경** — NCM811 · 압밀 ASSB · 리튬화 상태와 다르다.
2. **국소 압입 값 (85 nm)** — 입자 전체 · 접촉 강성이 아니다 · 깊이에 강하게 의존 (응집체 128.5 → 50.4).
3. **ν 0.3 가정 · ± 미인쇄** — SD · N 은 판독값.
4. **K_c = effective** (α · Q 문헌 상수 · 균열 길이 추정) · h_min · 85 nm 는 결과 뒤 선택 (민감도로 보완).
5. **wet = 1 h 담금 · 포화도 미측정** · 모세관 해석은 균일 구 Rumpf (D 미기재 · ε 0.028 은 NCA 논문 값).
6. **펠릿 = 소결 다결정** — "single particles" 를 단결정으로 옮기지 않는다.
7. 표 S1 ρ · 본문 2.5–2 GPa · 80 % · 참고문헌 번호 어긋남 (§3-9).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [42] | de Vasconcelos LS, Xu R, Zhao K (2017) Operando nanoindentation: a new platform to measure the mechanical properties of electrodes during electrochemical reactions. J Electrochem Soc 164:A3840–A3847. https://doi.org/10.1149/2.1411714jes | 같은 그룹 operando 압입 — **리튬화 · SOC 에 따른 E · H** (이 논문에 없는 축) · 질문 c · 카드 없음 |
| [64] | Kendall K, McN Alford N, Birchall JD et al (1987) Elasticity of Particle Assemblies as a Measure of the Surface Energy of Solids. Source Proc R Soc London Ser A, Math Phys Sci 412:269–283. https://doi.org/10.2307/2398151 | 입자 집합 (응집체 · 압분체) 의 탄성률 = 다짐 · 입경 · 계면 에너지 — 입자 전체 E (후보 B) · 다공 SE 압분체 탄성 · 카드 없음 |
| [68] | Rumpf H, Schubert H (1974) The behavior of agglomerates under tensile strain. J Chem Eng Japan 7:294–298. https://doi.org/10.1252/jcej.7.294 | 응집체 인장 강도 (식 7 · 8) 원전 — R7 · 카드 없음 |
| [53] | Field JS, Swain MV, Dukino JD (2003) Determination of fracture toughness from the extra penetration produced by indentation pop-in. J Mater Res 18:1412–1416. https://doi.org/10.1557/jmr.2003.0194 | 팝인 변위 → 균열 길이 (식 5 · Q 4.55) — 질문 c · R7 · 카드 없음 |
| [35] | Kim D, Shim HC, Yun TG et al (2016) High throughput combinatorial analysis of mechanical and electrochemical properties of Li[NixCoyMnz]O2 cathode. Extrem Mech Lett 9:439–448. https://doi.org/10.1016/j.eml.2016.03.019 | NMC 조성 · NMC811 박막 E · H (`sharma2023_…` 이 *"E 150 ± 12 · 미확인"* 으로 인용) — 질문 c · 카드 없음 |
| [24] | Xu R, de Vasconcelos LS, Shi J et al (2018) Disintegration of Meatball Electrodes for LiNixMnyCozO2 Cathode Materials. Exp Mech 58:549–559. https://doi.org/10.1007/s11340-017-0292-0 | 이차입자 계면 분리 (`wheatcroft2023_…` 가 인용) — R7 · 카드 없음 |
| [45] | Oliver WC, Pharr GM (1992) An improved technique for determining hardness and elastic modulus using load and displacement sensing indentation experiments. J Mater Res 7:1564–1583 | H · E_r 정의 원전 (`devasconcelos2016_…` §12 에도 후보) · 카드 없음 |
| [44] | Xu R, Sun H, de Vasconcelos LS, Zhao K (2017) Mechanical and Structural Degradation of LiNixMnyCozO2 Cathode in Li-Ion Batteries: An Experimental Study. J Electrochem Soc 164:A3333–A3341. https://doi.org/10.1149/2.1751713jes | **카드 있음** (`xu2017_…`) — 거칠기 4 nm · 식 5 검증 · 깊이 규칙의 출처 |
| [71] | Watanabe S, Kinoshita M, Hosokawa Tet al (2014) Capacity fading of LiAlyNi1-x-yCoxO2 cathode for lithium-ion batteries during accelerated calendar and cycle life tests (effect of depth of discharge in charge-discharge cycling on the suppression of the micro-c). J Power Sources 260:50–56. https://doi.org/10.1016/j.jpowsour.2014.02.103 | Rumpf 계산의 ε 0.028 출처 (NCA) — 값 확인용 |

## 13. [미확인] 목록 (본문 11 쪽 + ESM 10 개 전수에 없음)
1. 호 (issue) 번호 (가리킨 카드의 "(3)").
2. 그림 8 값의 SD · N (카드 판독 N 20 · 15 · 26 · 23 · K_c 17 · 22 · 19 · 21) · 그림 7 이 어느 상태 · 몇 회의 평균인지.
3. 펠릿 밀도 · 기공 · 결정립 분포 (3–10 µm 범위만) · 응집체 내부 기공률 · 일차입자 · 이차입자 크기 분포.
4. NMC532 의 화학량 · 리튬화 상태 · 잔류 리튬 (as-received 만).
5. wet 시료의 실제 포화도 (Rumpf 의 S 0.95 는 가정) · 담금 시간 1 h 의 근거.
6. 개별 시험의 h_x · c · P (그림 S5–S8 은 그림뿐).
7. 온도 · 습도 (글로브박스 O₂ · H₂O 만).
8. 식 8 에 넣은 D (카드 역산 0.51 µm).
9. *"5 tons"* 의 단위 (미터 톤 · 미국 톤) · 성형압.
10. Berkovich 최대 하중 유지 · 열 표류 보정 · 면적 함수 세부.
11. t-검정의 등분산 가정 여부.

## 14. 🧮 카드 산술 원장 (원문 숫자 · 판독값만으로 · 재현 = 식 그대로)

| # | 계산 | 결과 | 비고 |
|---|---|---|---|
| D1 | 그림 8 판독 점 평균 (E · H · K_c, 응집체 건조 / wet · 펠릿 건조 / wet) | 112.8 · 107.8 · 200.3 · 200.9 · 7.80 · 7.77 · 13.98 · 13.87 · 0.1034 · 0.2119 · 0.2979 · 0.2908 | ↔ 인쇄 113 · 108 · 200 · 201 · 7.8 · 7.8 · 14.0 · 13.9 · 0.104 · 0.212 · 0.298 · 0.291 |
| D2 | 판독 점 SD (n−1) | E 13.3 · 12.8 · 17.2 · 32.8 · H 1.66 · 1.87 · 2.04 · 2.63 · K 0.073 · 0.143 · 0.150 · 0.142 | 원문에 없음 |
| D3 | t-검정 (판독 점) | K 응집체 합동 t −2.84 (df 37) p **0.0072** · Welch p 0.0043 · K 펠릿 p 0.88 · E 0.27 · 0.94 · H 0.96 · 0.87 | 인쇄 0.007 · S4b 0.88 |
| D4 | 버림 | 시험 19 + 25 + 19 + 21 = 84 · 남음 17 + 22 + 19 + 21 = 79 · 5/84 = **5.95 %** · h_min 50: 8/84 = 9.5 % · 150: 6/84 = 7.1 % | 인쇄 "6%" · 유효 비 [판독 · 벡터] × 시험 수 |
| D5 | K_c wet ÷ 건조 (응집체) · 평균 차 · 중앙 차 | 2.04 · 0.108 · 0.1679 − 0.0827 = 0.085 | 인쇄 0.108 · 0.085 |
| D6 | 응집체 ÷ 펠릿 | E 0.565 (건조) · 0.537 (wet) · H 0.557 · K 0.349 (건조) | |
| D7 | H/E | 응집체 0.069 (건조) · 0.072 (wet) · 펠릿 0.070 · 0.069 | |
| D8 | E/(1−ν²) (ν 0.3) · 우리 (140, ν 0.25) | 124.2 · 118.7 · 219.8 · 220.9 · 우리 149.3 → 우리 ÷ 응집체 1.203 · ÷ 펠릿 0.679 | |
| D9 | AM–AM E* = E/(2(1−ν²)) | 우리 74.7 · 응집체 62.1 · 펠릿 109.9 GPa | 같은 두 구 |
| D10 | E 비 | 140/113 = 1.239 · 140/200 = 0.700 | |
| D11 | H 비 | 7.8/4.0 = 1.95 · 14.0/4.0 = 3.5 · 7.8/6.0 = 1.30 · 14.0/6.0 = 2.33 | 우리 H_AM |
| D12 | K 비 | 0.3/0.104 = 2.88 · 0.3/0.298 = 1.01 · 1.0/0.298 = 3.36 | 우리 K_IC_AM_P · AM_S |
| D13 | AM : SE | E 113/27.6 = 4.1 · 200/27.6 = 7.2 · ÷ 22.06 (우리 DFT E_VRH) = 5.1 · 9.1 · ÷ 1.35 = 84 · 148 · ÷ 1.53 = 74 · 131 · H 7.8/1.41 = 5.5 · 14.0/1.41 = 9.9 | [다른 카드] lee2025 · [우리] |
| D14 | 그림 7b 85 nm 내삽 | 응집체 118.1 + (85−69.1)/(90−69.1)·(111.8−118.1) = **113.3** · 펠릿 **205.4** | ↔ 그림 8 113 · 200 |
| D15 | 깊이 비 | 응집체 50.4/113.3 = 0.445 · 펠릿 169.3/205.4 = 0.824 | |
| D16 | Berkovich √A = √24.5·h | 49 nm → 0.243 µm · 85 nm → 0.421 µm · 500 nm → 2.47 µm | [Stallard22] 그림 9 x 범위 |
| D17 | 그림 7a h_f/h_max | 펠릿 361.3/523.4 = 0.690 · 응집체 250.9/529.8 = 0.474 | [판독 · 벡터] 입력 |
| D18 | 표 S1 이론 부피 (w/2)(1/ρ_PVDF + 1/1.90) | ρ 1.45: 12.46 · 13.44 · 28.64 · 기공 (넓이×두께) 50.84 · 27.53 · 3.77 % · ρ 1.49: 12.27 · 13.23 · 28.20 · 51.59 · 28.63 · 5.24 % | 인쇄 12.5 · 13.4 · 28.6 · 50.8 · 27.5 · 3.8 → 1.45 |
| D19 | 표 S1 나중 부피 = 넓이 × 두께 | 75.3 × 0.3367 = 25.35 · 92.7 × 0.2000 = 18.54 · 160.6 × 0.1853 = 29.76 | 인쇄 25.4 · 18.5 · 29.8 |
| D20 | 표 S2 재계산 | 건조 부피 7.787 · 4.313 · 밀도 1.425 · 1.414 · 젖은 부피 10.198 · 5.625 · 팽창 30.95 · 30.43 % · 넓이 +19.6 · +19.4 % · 두께 +9.5 · +9.3 % | 인쇄 30.8 · 30.5 (평균의 곱 ≠ 곱의 평균) · 등방 (1.094³ = 1.309) |
| D21 | PVDF 필름 공극 1 − 1.43/ρ | ρ 1.45: 1.4 % · 1.49: 4.0 % | 거의 치밀 |
| D22 | Rumpf 식 8 → D | D = 6·0.95·(0.972/0.028)·0.0411 N/m ÷ 16 MPa = **0.508 µm** · D 1 µm 이면 8.1 MPa · 0.1 µm 이면 81 MPa | 원문에 D 없음 |
| D23 | LEFM K = σ√(πa)/Y (a 1 µm · Y 0.64) | 16 MPa → **0.0443** · 거꾸로 σ = K·Y/√(πa): 0.104 → 37.6 · 0.212 → 76.5 · 0.298 → 107.6 MPa | 인쇄 0.044 · 거꾸로는 원문에 없음 |
| D24 | G = K²(1−ν²)/E (ν 0.3) | 응집체 건조 (0.104, 113) **0.087 J/m²** · wet (0.212, 108) 0.379 · 펠릿 (0.298, 200) 0.404 · 우리 K_IC_AM_P (0.3, 140, ν 0.25) 0.603 | 비교만 |
| D25 | 식 5 예시 (응집체 · h_m 150 nm · h_x 10 nm) | √2·150 + (4.55·124.2/7.8 − √2)·10 = 922 nm | *"~1 μm"* 와 맞는 자릿수 (h_x 는 원문에 없음 · 예시) |
| D26 | 성형압 | 5 t × 9.81 m/s² ÷ π(6.5 mm)² = 370 MPa (미터 톤) · 335 MPa (미국 톤) | 단위 미확인 |
| D27 | PS ÷ 응집체 E | 3.8/113 = 0.034 (응집체가 30 배) | |
| D28 | CB/PVDF · PVDF 판독 변화율 | PVDF E −54.6 % · H −51.2 % · CB/PVDF E −87.0 · −85.8 · −80.7 % · H −84.7 · −80.0 · −67.1 % · 2.45/0.594 = 4.13 | 인쇄 "about 50%" · "over 80% in both" · "four times" |
| D29 | 같은 그룹 2016 ↔ 2019 | 113/138.73 = 0.815 · 111.8 (90 nm) / 141.2 (97 nm) = 0.792 · 113/123.02 = 0.919 | [다른 카드] devasconcelos2016 |
| D30 | 펠릿 K_c 의 h_min 민감도 | 0.289 (50) → 0.298 (100) → 0.360 (150) — 50 → 150 nm +24.6 % | 그림 S4 인쇄 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 11 쪽을 글자 층 (PyMuPDF) + 렌더로 읽음.  서지 = PDF 1 쪽 (제목 · 저자 · 소속 · 이력 · 키워드 · DOI · © 줄) + PDF 메타데이터 (*"Exp Mech, doi:10.1007/s11340-018-00451-6"* · 작성 2018-11-26 · 수정 2019-05-03) + 쪽 머리글 *"Exp Mech (2019) 59:337–347"*.  호 번호는 어디에도 없음.
- ESM docx 10 개를 zipfile 로 열어 word/document.xml (OMML m:t 포함) 로 캡션 · 표 글자를 읽고, 그림 · 표는 LibreOffice (headless · 격리 프로필) PDF 변환본에서 렌더 · 크롭 (EMF 는 벡터로 변환됨 — 그림 S4 를 벡터로 판독).  docx 메타데이터 작성자 "Rong" · 2018-10-31.
- 그림 판독: 그림 3 · 5 · 7 · 8 (본문) · S4 는 **벡터** (PyMuPDF `get_drawings`) — 눈금 선 좌표 ↔ 인쇄 눈금 글자의 최소제곱 (예: 그림 8a x 237.093 → 330.197 pt = 80 → 280 GPa · 그림 7b x 422.225 → 539.086 pt = 0 → 500 nm, y 156.981 → 74.537 pt = 0 → 250 GPa).  검증: 그림 8 의 12 묶음 점 평균 = 인쇄 평균 = 흰 사각형 · 판독 t-검정 p 0.0072 = 인쇄 0.007 · 그림 S4 유효 비 × 그림 S1 시험 수 = 그림 8c 점 개수 (17 · 22 · 19 · 21) · 그림 7b 85 nm 내삽 113.3 = 인쇄 113.
- 크롭 63 장 (§5-1) · 전부 열어 확인.
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (ls-tree · 545 개) + DOI (`s11340-018`) · "Vasconcelos" · "In-situ nanoindentation measurement" grep — **이 논문 카드 없음** (sedlatschek2026 [27] · stallard2022 [74] · wang2027 [25] · kalnaus2023 (55) · sharma2023 [23] · xu2017 · dang2019 에 인용만).

## 🔗 관련 카드
- 같은 그룹 · 같은 조성 2016 카드: [`devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode`](devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode.md) — 전극 속 NMC532 targeted 138.73 ± 18.78 · H 8.89 (75–150 nm) · 격자 123.02 · CB/PVDF 필름 1.78 — 이 카드의 응집체 113 은 비슷한 깊이에서 그 값의 약 0.8 배 (분말 · 기지 · 방법 차이 · 원문 설명 없음).
- 이 논문을 인용 · 사용한 정본 카드: [`sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`](sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile.md) ([27]) · [`stallard2022_cathode_mechanical_properties_review`](stallard2022_cathode_mechanical_properties_review.md) ([74] · 그림 7 · 9 · 12A) · [`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`](wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn.md) ([25]) · [`kalnaus2023_ssb_critical_role_of_mechanics_stress_relief_review`](kalnaus2023_ssb_critical_role_of_mechanics_stress_relief_review.md) ((55)) · [`sharma2023_nmc_single_crystal_anisotropic_nanoindentation`](sharma2023_nmc_single_crystal_anisotropic_nanoindentation.md) ([23]) · [`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`](xu2017_nmc532_nanoindentation_modulus_hardness_toughness.md) (이 논문의 [44] · 같은 K_c 짝 0.102 · 0.309).
- NCM 입자 강도 · 파괴 사슬: [`dang2019_nmc111_secondary_particle_flat_punch_fracture_strength`](dang2019_nmc111_secondary_particle_flat_punch_fracture_strength.md) · [`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`](wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem.md) · [`stallard2022_nmc811_single_crystal_shear_strength_lithiation`](stallard2022_nmc811_single_crystal_shear_strength_lithiation.md).
- SE 압입 짝: [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) · [`papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation`](papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

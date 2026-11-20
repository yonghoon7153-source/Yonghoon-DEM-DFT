# 입자크기·압력이 빠른 이온전도체 t-Li₇SiPS₈ 의 수송물성에 미치는 영향 — DEM 압밀 + Heckel + FVA σ — Schneider (Adv. Energy Mater. 2023)

> slug `schneider2023_particle_size_pressure_transport` · DOI `10.1002/aenm.202203873` · type `DEM+FVA(continuum) + exp(EIS) + AIMD · SI 46쪽 반영 11-18` · PDF `Schneider_2023_AdvEnergyMater_ParticleSize_Pressure_TransportProperties_FastConductor.pdf` · SI `34._Sup_Advanced_Energy_Materials_-_2023_-_Schneider_-_Effect_of_Particle_Size_and_Pressure_on_the_Transport_Properties_of_the_Fast.pdf` · digested `2026-06-26` · SI 보강 `2026-11-18` · status ✅
>
> ⛔⛔ **SI 보강 2026-11-18 — 2026-06-26 digest 는 본문만 읽었다** (§4 · §5 · §10 이 접촉 법칙 · 입력값 · 그림 S9 / S13 / S17 을 "SI 참조" 로 미뤄 두었다).
> SI 46 쪽 (출판사 표지 1 + S-1 – S-45) 을 **전부** 읽고 SI 크롭 **56 개** (그림 19 · 표 7 · 식 16 · 근거 글 14) 를 더했다. 도구 크롭 26 개는 **전부 다시 잘랐다** (이웃 글 · 절 제목 섞임 8 · 표 범위 6 · 여백만 정리 12 — `figures.json` 의 `recrop`).
> 새 절 = **§S 보충 자료 (SI) 절별 정리** · **§세미나 준비** · 끝 **고친 것 (11-18 SI)** (옛 문장은 지우지 않고 ⛔ 표지). 그림 판독값 = `litdb/figures/schneider2023_particle_size_pressure_transport/si_digitized.csv`. 요지:
> - **DEM = 강체 구 (Cundall–Strack) + 선형 스프링–대시포트 법선 (식 S10) + Coulomb 마찰 (식 S12)** · 소성 · 점착 · 구름 저항 없음 · **k_N = 0.01 N/m** (*"we are not interested in the resulting global reaction force"*, 표 S5) · μ 1.0 (문헌 범위 0.05–2.0 의 "middle") · c_COR 0.1 · ν 0.3 · g = 0 ⇒ DEM 의 힘은 쓰지 않았고 압력 축은 **실험 두께에 맞춘 이름표**다 (SI p.S-29 · 본문 Fig. 6b 캡션) [카드 해석]. §4 의 "c_cor = 접촉보정 · c_cor·k_N 으로 캘리브 · ρ·μ 실험 매칭 튜닝" 은 **틀렸다** (그 자리에 정정 표지).
> - **FV = 복셀 1 µm · BEST · U = 1 V · σ_eff = l·j/U (식 S15) · σ_eff,max 로 정규화** · *"homogeneous phase without any additional grain boundary resistances"* (p.S-29–S-30) · 활성화 부피는 bulk σ 를 압력에 따라 줄이는 식 S16 으로만 들어간다.
> - **"in die" ↔ "out of die" Heckel (그림 S9d)** — out of die = 각 압력으로 누른 뒤 **10 MPa** 적층압에서 잰 값 · 1.7 GPa 에서 상대밀도 96.5 → 92.8 % (<50 µm) · 91.7 → 89.0 % (>50 µm) [판독] = 탈압 회복 3.7 · 2.7 %p.
> - **SI 안의 어긋남** (§S.3 · 아홉 가운데 주요 여섯): 표 S5 감마 b = 1.944 (본문 Fig. 6a 7.048 · 표 S1/S2 와 맞는 쪽은 7.048 [카드 산술]) · ρ_DEM 1980 kg/m³ ↔ 비중병 2.008 g/cm³ · Pugh "B/G < 0.5" (표 S7 의 열은 G/B) · 식 S4 의 ln r (식 S3 은 r²) · 표 S6 Cij 로 다시 낸 B ≈ 25.5 GPa ↔ 표 S7 23.5 · 그림 S6 의 SEM 곡선이 ≈ 6 µm 에서 100 % (표 S1 D90 60 µm 와 10 배).
> - **절대값 전이 안 됨**: t-Li₇SiPS₈ 값 (σ · ΔV · P_y · 밀도 · 진밀도) 은 LPSCl 로 옮기지 않는다. 저자 자신은 B · E · G/B 가 비슷하니 *"similar high pressure densification behavior"* 를 **기대**한다고만 썼다 (p.S-38 · 측정 아님) — 같은 표의 G/B 는 LPSCl 0.28 ↔ t-Li₇SiPS₈ 0.49.



> elements: Li Na P S Si
> methods: md, msd

---

## ⚠️ 0. 가장 먼저 — 소재 정정 (위시리스트 제목 추정과 다름)

위시리스트 #34 추정 제목은 "fast [Li-Ion Conductor / argyrodite]"였으나, **PDF 전수 정독 결과 실제
소재는 argyrodite(Li₆PS₅X)가 아니라 tetragonal LGPS-계열 thiophosphate `t-Li₇SiPS₈` (t-LiSiPS)** 이다.
- **t-Li₇SiPS₈** = Li₁₀GeP₂S₁₂(LGPS)-like 정방정(tetragonal) 황화물, c축 1D 빠른 전도 채널. glass-ceramic
  (비정질 side phase 8.2–9.0 wt% 함유).
- **우리 LPSCl(Li₆PS₅Cl, argyrodite)과 같은 *황화물(thiophosphate) 패밀리*지만 *다른 결정구조·다른 조성***.
  → **물리·압력거동·방법론은 직접 비교 가능**(같은 sulfide cold-press 거동), **σ 절대값·E·ΔV 등 소재고유
  수치는 transfer 금지**(Cronau/Sakuda/Doux 와 동일한 same-family-but-not-LPSCl 주의).

★ **그럼에도 이 논문이 #34로서 핵심인 이유:** 위시리스트가 노린 두 축 — **σ(입자크기)** 와 **σ(압력)** —
을 **실험 EIS + DEM 압밀 + Heckel + FVA(연속체 σ)** 로 *동시에* 다룬, **우리 DEM→미세구조→σ 파이프라인과
가장 직접적으로 평행한 실험+시뮬 논문**이다. 심지어 Bazzoun/Varkey 보다 *압밀 역학(Heckel P_y, 압력영역
분해)* 측면에서 우리와 더 겹친다.

---

## 1. 한 줄 요약
**황화물 SE 펠릿의 이온전도도는 "상대밀도(porosity)"보다 *입자크기분포(PSD)*에 더 강하게 지배되며,
압밀압력(pelletizing) 은 두 개의 분리된 영역 — (I) 저압 미세구조(입자 재배열·파편화·접촉면적) 와
(II) 고압 원자수준(활성화부피 ΔV 에 의한 격자압축) — 으로 σ 에 *반대 방향*으로 작용한다.** 저자들은
이를 **Heckel 압밀해석 + DEM 압밀시뮬 + FVA 연속체 σ + AIMD** 의 다중스케일로 분해. → 우리에게는
**σ-vs-압력**(우리 Heckel P_y·σ-vs-porosity)과 **σ-vs-입자크기**(우리 Cronau(r_SE)/packing) 의 *실험+시뮬*
앵커이자, "**porosity 는 σ 의 약한 descriptor, PSD 가 강한 descriptor**" 라는 우리 σ_ionic 형태(φ_eff·CN²·
cov·packing 이 porosity 단독보다 강함)와 정합하는 핵심 frame[4] 외부 근거.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| Christian Schneider, Christoph P. Schmidt, Anton Neumann, Moritz Clausnitzer, Marcel Sadowski, Sascha Harm, Christoph Meier, Timo Danner, Karsten Albe, Arnulf Latz, Wolfgang A. Wall, **Bettina V. Lotsch\*** (Max Planck FKF Stuttgart + TU München + DLR/HIU Ulm + TU Darmstadt + LMU) | Adv. Energy Mater. **13**, 2203873 (2023); Received 2022-11-14, Published 2023-03-03 | 10.1002/aenm.202203873 | **t-Li₇SiPS₈** (tetragonal LGPS-like thiophosphate; glass-ceramic). **CAM 없음 — SE-only blocking-electrode 펠릿** | DEM(압밀) + FVA(연속체 σ) + EIS(실험) + AIMD; open access |
| **SI (11-18 반입)** | *"Supporting Information for Adv. Energy Mater., DOI: 10.1002/aenm.202203873"* (SI PDF 1 쪽 출판사 표지) · **46 쪽** = 표지 1 + S-1 – S-45 (PDF 쪽 = SI 쪽 번호 + 1) · 그림 S1–S19 · 표 S1–S7 · 식 (1)–(16) (이 카드는 SI 식을 **식 S1–S16** 으로 부른다) · 참고문헌 S1–S49 | 같은 DOI | SI 머리 (S-1) 의 저자 12 명 · 순서 · 교신 b.lotsch@fkf.mpg.de = 위 칸과 같다 (11-18 대조 · 어긋남 0) · 소속은 여섯 (MPI Stuttgart · TUM 계산역학 · DLR Stuttgart · HIU Ulm · TU Darmstadt · LMU) — 위 칸은 DLR/HIU 를 한 칸으로 묶었다 | **SI 크롭 56 개** (그림 19 · 표 7 · 식 16 · 글 14) · 본문 크롭 6 장은 그대로 (본문 PDF 는 이번에 없었다) |

> ★ **SE-only 논문**(CAM/composite 아님). σ 는 모두 **순-SE 펠릿의 유효 이온전도도**(blocking electrode EIS).
> Bazzoun/Minnmann 의 *composite* σ_eff,ion 과는 층위가 다름 — 이 논문은 **SE 재료 자체의 σ(압력·크기) 거동**.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **σ_ionic (압축, 1차)** | max **4.1 mS/cm** (<50µm) / **5.7 mS/cm** (>50µm) | @ ~0.5 GPa pelletizing | stated | 압축 sweep 최대 |
| σ_ionic @ 최저압 (압축) | **0.3 mS/cm** (<50µm) / **0.7 mS/cm** (>50µm) | @ 0.01 GPa | stated | 미압축 분체 → 접촉불량 |
| **σ_ionic (release, 1차)** | max **5.3 mS/cm** (<50µm) / **6.6 mS/cm** (>50µm) | @ ~0.1–0.2 GPa (release) | stated | 압력해제 sweep 최대 |
| σ_ionic @ 0.01 GPa (release) | **4.4 mS/cm** (<50µm) / **2.1 mS/cm** (>50µm) | @ 0.01 GPa release | stated | >50µm 가 release 더 민감 (역전) |
| σ_total (무압) | **2 mS/cm**, E_a **0.27 eV** | Harm et al. (ref 38) | stated | 재료 고유 |
| **활성화부피 ΔV** | **~1.4 cm³/mol** (exp: 1.39 / 1.41) | release fit (Fig 4c) | stated | **입자크기·morphology 무관 = intrinsic** |
| ΔV (AIMD) | **1.7–2.0 cm³/mol** (f=0.99→1.7, f=0.98→2.0) | 격자 scaling 계산 | stated | 양수 → 압축시 host 국소팽창 필요 |
| 이온 migration 장벽 | **0.22 eV (c축 1D)** / **0.28 eV (3D)** | bond-valence + AIMD | stated | 이방성 D_c ≈ 4× D_a/b |
| ⛔ ↳ 정정 (11-18 SI p.S-33) | 0.22 / 0.28 eV 는 **bond valence sum 만**의 값 · **AIMD** 장벽은 따로: c **127(13) meV** · a/b **≈155 meV** (그림 S18 인쇄 146(19) · 165(15)) · 전체 MSD **136(13) meV** | AIMD 500–900 K · 2×2×1 (12 f.u.) · 단결정 | SI 인쇄 | 저자: AIMD 장벽이 측정값보다 낮은 것은 *"shortcomings of extracting activation barriers from AIMD simulations at high temperatures"* · *"do not consider grain boundiers or (amorphous) side phases"* |
| **Heckel P_y ("in die")** | **0.95(3) GPa** (<50µm) / **1.65(3) GPa** (>50µm) | 압축, regime II 기울기 | stated | 작은 PSD → 낮은 P_y → 소성변형 쉬움 |
| ρ_rel (상대밀도) | regime III 에서 **90–95 %** (porosity 5–10 %) | 고압(>~1 GPa) | stated | release 시 약 **−4 %** 복원 |
| 펠릿두께 | ~**1600 → 1000 µm** (압축); release 시 ~4% 증가 | 0→1.7 GPa | digitized(Fig 2d) | <50µm 가 더 치밀(낮은 두께) |
| ρ_rel @ 저압 비교 | <50µm > >50µm (작은 입자 초기 더 치밀) | Fig 2e | stated | 단, σ 는 반대(>50µm 가 높음) |
| **비정질 side phase** | **8.2–9.0 wt%** (pristine) → **9.7–10.2 wt%** (@1.7 GPa) | ³¹P MAS NMR | stated | 압력이 결정도 일부 손상 (소성흐름→격자무질서) |
| PSD (<50µm) | monomodal; gamma fit a=1.944, b=7.048 | sieve 통과분 | stated | DEM 입력 |
| ⛔ ↳ SI 대조 (11-18) | 표 S5 (p.S-28) 는 **b = 1.944** 로 인쇄 (a 와 같은 수) · 감마 (모양 a · 척도 b) 로 b = 7.048 µm 이면 수 기준 중앙 11.4 · 10 % 3.6 · 90 % 26.8 µm ≈ **표 S2 (<50 µm) 11 · 3 · 27 µm** · 부피 가중 (모양 a+3) 16.9 · 32.5 · 55.8 µm ≈ **표 S1 17 · 35 · 60 µm** · b = 1.944 이면 중앙 3.2 µm [카드 산술] | — | SI 인쇄 + 카드 산술 | ⇒ **7.048 이 DEM 에 쓴 값** · 표 S5 의 1.944 는 옮겨 적기 오기로 보인다 (원문 정정 여부 [미확인]) |
| PSD (>50µm) | bimodal; **D50(vol) = 89 µm** | sieve 잔류분 | stated | number-PSD 는 작은입자 우세나 vol 은 >50µm 우세 |
| ⛔ ↳ 정정 (11-18 SI 표 S1) | **부피 기준 D10 / D50 / D90 = 89 / 138 / 240 µm** (>50 µm) · 17 / 35 / 60 µm (<50 µm) · **수 기준** (표 S2) 9 / 17 / 98 µm (>50) · 3 / 11 / 27 µm (<50) — Feret 지름에서 계산 | SEM 영상 (>50 µm 5118 입자 · <50 µm 3475 입자) | SI 인쇄 | 위 "D50(vol) 89 µm" 는 표 S1 의 **D10** 과 같은 수 · 본문 Fig. 2c 파란 점선도 50 % 를 ≈ 130–140 µm 에서 지난다 [판독 `fig_2.png`] ⇒ 89 µm = D10 (본문 글 대조는 못 함 — 본문 PDF 없음) |
| E_SE / σ_y / ν | **n/a** (논문이 E·σ_y 수치 미명시 — DEM 은 c_cor·k_N 으로 캘리브) | — | — | ⚠ Heckel P_y 0.95/1.65 GPa = 유효 항복(σ_y proxy) |
| ⛔ ↳ 정정 (11-18 SI) | **DFT (VRH)**: B **23.5 GPa** (Birch–Murnaghan 22.8) · E **29.5** · G **11.4** · ν **0.29** · G/B **0.49** (표 S7 · 강성 텐서 표 S6) · **DEM 입력**: ν **0.3** (*"Typical value for argyrodite and LGPS-type"*) · 영률 없음 — 법선 강성 **k_N 0.01 N/m** 를 *"for reasons of numerical efficiency"* 줄인 값으로 씀 · **σ_y = SI 에도 없음** | DFT PBE · 4 구조 평균 | SI 인쇄 | "c_cor·k_N 으로 캘리브" 는 틀렸다 — c_COR 0.1 은 에너지 소산용 · k_N 은 반력에 관심 없다며 임의로 둔 값 (표 S5) · 보정 대상 없음 |
| coverage / Z / σ_e / σ_thermal | **n/a** (SE-only, 측정 안 함) | — | — | composite·전자·열 채널 없음 |
| ↳ SI 의 접촉 수치 (11-18) | **DEM 접촉면 합** 0.08 (0.01 GPa) → 0.70 (0.1) → 1.42 (0.5) → 1.70 (1.0) → **1.80 × 10⁶ µm²** (1.5 GPa) | 그림 S13 · 9591 입자 상자 (본문) | 판독 (`si_digitized.csv`) | 배위수 Z · 피복 = SI 에도 없음 · 접촉면을 한 번 세는지 두 번 세는지 미기재 |
| **진밀도 (SI)** | 비중병 **2.008(6) g/cm³** (He · 4 시료 평균) ↔ 결정학 **1.923(9)** (+4.4 %) · DEM ρ **1980 kg/m³** | p.S-23 · 표 S5 | SI 인쇄 | 상대밀도의 분모 = 2.008 · 저자: *"This difference is small"* — 그러나 1.923 을 쓰면 상대밀도가 ×1.044 (95 → 99 %) [카드 산술] |
| **탈압 회복 (SI)** | 1.7 GPa: in die 96.5 → out of die **92.8 %** (<50) · 91.7 → **89.0 %** (>50) · 0.3 GPa 에선 두 값이 마커 크기 안 (≈ 81.5 · 79.5 %) | 그림 S9d · out of die = **10 MPa** 적층압에서 | 판독 | 1.7 GPa 기공률 3.5 → 7.2 % (×2.1) · 8.3 → 11.0 % (×1.3) [카드 산술] |
| ³¹P NMR 선폭 (SI) | FWHM 94 ppm: 2.02 → 2.38 (<50) · 2.10 → 2.41 (>50) · 73 ppm: 1.82 → 2.17 · 1.91 → 2.22 ppm (누르기 전 → 뒤) | 그림 S12b · '뒤' 의 압력은 SI 캡션에 없음 | 판독 | 비정질 상 wt% 는 그림 S12a 에 인쇄된 값 (8.2 → 9.7 · 9.0 → 10.2) |

## 4. 시뮬레이션 방법 ★
- **code / version**: **DEM = in-house multi-physics 코드 `BACI`** (TU München Wall 그룹; ref 51). **FVA(연속체
  σ) = `BEST`** (Battery and Electrochemistry Simulation Tool, DLR/HIU; ref 52,53). **AIMD = 별도(VASP류, ref 38·48)**.
  → **3개 솔버 + 실험 EIS** 의 multiscale.
  ↳ (11-18 SI p.S-31) DFT · AIMD = **VASP** (PBE · PAW) — §S.2.11.  SI 는 DEM 코드 이름을 다시 적지 않고 *"based on our previous work in the field of additive manufacturing"* [S18, S19] 라고만 쓴다 (p.S-25).
- **DEM 접촉법칙**: 논문 본문에 contact law 정식 미상술(SI 참조). 입력 파라미터로 **ρ, ν, k_N(법선강성),
  c_cor(접촉보정), μ(마찰), g(중력)** 명시(Fig 6a insert). **구형 입자 + 접촉 overlap = 더 큰 접촉면적 → 더 나은
  transport path** 로 모델링("larger contact surface modeled by particle overlapping"). ⚠ **항복캡·SHAPE 소성
  명시 없음** → Bazzoun/Varkey 와 같은 **rigid-sphere + CONTACT(overlap) 모델 계열**로 추정(아래 §10).
  ⛔ **정정 (11-18 SI p.S-25 – S-28)**: 접촉 법칙은 SI 에 있다 — **강체 구** (*"the particles are described as rigid spheres"*, Cundall–Strack [S20]) ·
  병진 · 회전 운동량 식 S8 · S9 (m = 4/3 π r³ ρ · I_G = 0.4 m r²) · **법선 = 선형 스프링–대시포트** f_CN = min(0, k_N g_N + d_N ġ_N) n (g_N ≤ 0, 식 S10 — 인력 차단) ·
  d_N 은 반발 계수에서 (식 S11 · c_COR 0.1 → 감쇠비 0.59 [카드 산술]) · **접선 = Coulomb 마찰 + 접선 스프링–대시포트** (식 S12 – S14 · k_T = (1−ν)/(1−0.5ν) k_N = 0.82 k_N [카드 산술] · d_T = d_N) ·
  **점착 · 구름 저항 · 항복 (Thornton–Ning 같은 소성 접촉) 없음** — Varkey 2026 의 탄소성 접촉 법칙과 다르다 (선형 탄성 겹침뿐).
  "c_cor(접촉보정)" 은 오기 — **c_cor = 반발 계수** (coefficient of restitution, 표 S5).
- **재료 파라미터**: E_SE/σ_y/ν 의 *수치* 는 본문 미제공(SI). 대신 거시 **Heckel P_y = 0.95/1.65 GPa** 가
  유효 소성항복(σ_y proxy). 밀도 ρ, 마찰 μ 등은 실험 매칭으로 튜닝.
  ⛔ **정정 (11-18 SI 표 S5)**: 튜닝된 값은 **하나도 없다**. ρ **1980 kg/m³** (*"Averaged value from four batches"* — 같은 SI 의 비중병 값 2.008 g/cm³ 와 1.4 % 다르다) ·
  ν **0.3** (*"Typical value"*) · **k_N 0.01 N/m** (*"we are not interested in the resulting global reaction force, but only in the resulting particle morphology. However, this is not affected by the exact value of the stiffness."*) ·
  c_COR **0.1** (*"chosen non-zero to dissipate energy … to save computational resources"*) · μ **1.0** (*"Since we do not have further information on that we used a value from the middle of the range"* 0.05–2.0) ·
  g **= 0** (50 mg · Ø6 mm 의 중력 압력 17.3 Pa ≪ 0.01 GPa) · 감마 a = 1.944 · b (표 S5 는 1.944 로 인쇄 — §3 정정 행).
  ★ k_N 0.01 N/m 로 힘 제어를 했다면 1 GPa · 지름 ≈ 14 µm 입자의 접촉력 ≈ P·d² ≈ 0.19 N → 겹침 ≈ 19 m [카드 산술] ⇒ **두께 (변위) 를 실험에 맞춰 누른 것으로만 읽힌다** [카드 추론 — 압축 방식 (벽 변위 · 속도 · 단계) 은 SI 에도 없음].
  선형 스프링 + Coulomb 마찰 + 점착 0 + g 0 이면 정해진 두께의 정적 평형 형상은 k_N 배율과 무관하다 (힘이 모두 k_N 에 비례) [카드 해석] — 저자의 "not affected" 문장이 서는 조건.
- **bond/binder 모델**: **없음**(SE-only, 바인더·CAM 미포함).
- **MPM/continuum**: **MPM 아님 — FVA(finite volume analysis)** 가 연속체 역할. DEM 이 만든 입자 위치·반지름
  → **voxel 구조 생성** → BEST 로 **정상상태 전류분포**(인가전압 ΔV, ∇·J=0, J=−σ∇φ) 풀어 **유효 σ** 산출.
  = Bazzoun 의 FEM 와 같은 *연속체 전달 readout*(단 voxel-FVM). **점접촉 constriction 명시 없음** → σ 는
  접촉면적(overlap)으로 들어감.
  ↳ (11-18 SI p.S-29 – S-30) **복셀 1 µm** (입자 위치 · 지름에서) · BEST [S27, S28] · 전해질 상의 Poisson 식 · **U = 1 V** · 경계 평균 전류밀도 j → **σ_eff,i = l_i · j / U** (식 S15) ·
  **σ_eff,max 로 정규화** · 계면 항 = *"the electrolyte material was treated as a homogeneous phase without any additional grain boundary resistances between individual particles"* ⇒ 우리 말로 **CONTACT_FREE 가지** (겹친 구의 합집합 고체 · 계면 저항 0) [카드 해석].
  복셀 1 µm 는 수 기준 D10 3 µm 입자를 지름 3 복셀로 그린다 (표 S2) · 복셀 크기 수렴 시험 = SI 에도 없음.
  겹친 구를 복셀로 칠하면 고체 = 합집합이라, 같은 두께에서 복셀 고체 분율은 구 부피 합 (질량 보존 · 실험 상대밀도의 짝) 보다 겹침만큼 작다 [카드 해석] — 그 차이를 어떻게 다뤘는지 = SI 에도 없음.
- **전달 솔버 ★**: FVA(BEST) 가 유효 σ. **두 시나리오로 분해(핵심 설계):**
  - **Scenario I** = bulk σ 를 **활성화부피 효과(ΔV)로 감소**시킨 채 일정 stack pressure → **0.1 GPa stack
    실험 모사**.
  - **Scenario II** = bulk σ 를 **증가하는 외부압력에 따라 감소**(ΔV 격자압축) → **variable pelletizing 실험 모사**.
  - σ 값은 **정규화**(σ/σ₀ 또는 σ/σ_0.5GPa) — 절대 bulk σ 가정에 무관, **기하(미세구조)만의 효과** 추출.
- **입자 처리 ★** (DEM판 "무질서 처리"):
  - **구형 입자만**(perfect spheres). 논문이 §결론에서 **"DEM 의 perfect spheres ↔ 실제 비구형 분말 차이가
    저압 regime I 의 과대평가 원인"** 을 *명시*("difference between the DEM model consisting of perfect spheres
    and the powder, which consists of particles that are not perfectly spherical").
  - **실측 PSD 반영**: <50µm = gamma(a=1.944,b=7.048) **다분산(poly)**, >50µm = bimodal. → **mono/bi/poly-PSD
    실측 일치**가 이 논문의 강점(우리 12:4:1 bimodal 과 같은 정신).
  - **rigid vs CONTACT-소성 vs SHAPE-소성**: **CONTACT(overlap) 계열** — 입자 형상은 안 변하고 overlap 이 접촉면적·
    transport 를 키움(="δ-overlap 프록시"). **진짜 SHAPE 소성(입자 형상흐름) 아님** → 우리 MPM 이 메우는 칸과 동일.
    (단 Heckel 해석은 *거시 소성*을 인정 — regime II 가 "plastic deformation" — 그러나 *입자 단위 형상변화*는 DEM 에 없음.)
  - ↳ (11-18 SI p.S-21 — 저자의 DEM 한계 문장 원문) *"In the DEM simulation the compaction of perfect spheres attributed with friction effects, form the pellet. The solid electrolyte powder, however, consists of particles that are far from spherical. They rather have various morphological features, such as holes, jags, dips, and bulges, which contribute to surface roughness (see for example Figure S7). This can increase friction by causing the particles to coalesce into larger agglomerates that require higher stress to break up. Additionally, surface roughness can introduce current constriction effects at the inter-particle contacts, especially, when the particles are not allowed to connect at low pressure."*
    ⇒ SI 가 든 저압 과대평가 원인 = ① 거칠기 → 마찰 · 응집체 (기계 쪽) ② 접점의 전류 협착 (전달 쪽 — FV 에 없는 항). 형상 (S7 · S8: solidity · convexity 대부분 1 근처 · sphericity 낮음) 은 2D 영상으로만 쟀다.
- **도메인/RVE / servo / seeds / 압력범위**: base **210×210 µm²** × height **1700 µm**, **9591 입자**, **측방 주기경계**
  (실험 펠릿은 측방이 훨씬 크나, 모든 상호작용 포착되도록 측방을 PBC). 압력범위 **0.01 → ~1.7 GPa**(실험과 동일).
  ⚠ **우리 300 MPa cold-press 보다 ~5× 높은 압력대까지**(GPa 영역) — 이 논문은 고압 ΔV 효과를 보려고 일부러 고압.
- **특이사항/튜닝**: DEM 측방 치수를 실험보다 작게 잡되 "PSD 가 실험과 충분히 가깝고 모든 상호작용이 표현되도록"
  선택. σ 는 정규화로만 — **절대 bulk σ 캘리브 회피**(기하효과만 분리하는 영리한 설계).
  ↳ (11-18 SI) ① 압력 ↔ 두께: *"For each pressure level p_i corresponding to a certain pellet thickness"* (p.S-29) + 본문 Fig. 6b 캡션 ("pressure axis relates to the experimental pellet thickness") ⇒ **DEM 은 실험 두께를 받아 미세구조를 만든다 — 압력–밀도 곡선을 예측하지 않는다** [카드 해석].
  ② 상자 고체량 점검 [카드 산술]: 감마 (1.944, 7.048 µm) 구 9591 개의 부피 합 = 3.97 × 10⁷ µm³ → 210 × 210 µm² 위 꽉 찬 두께 **899.9 µm** · ρ 1.98 g/cm³ 면 면적당 질량 1.782 mg/mm² ↔ 실험 50 mg / Ø6 mm = **1.769 mg/mm²** (0.7 % 차) ⇒ 입자 수는 실험 면적 질량에 맞춘 것으로 보인다 · 같은 계산을 b = 1.944 로 하면 꽉 찬 두께 19 µm (실험 두께 ≈ 920 µm 의 2 %) 로 불가능 — b = 7.048 의 둘째 근거.
  ③ 압축 방식 · 속도 · 시간 간격 · 시드 수 · 실행 시간 = **SI 에도 없음**.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **문헌 σ-vs-P 종합**(Na₃PS₄/Na₃SbS₄/Na₂S·P₂S₅ glass/β-AgI/LiBH₄/Li-β-alumina/LLTO). 미압축 분체(hollow)는 비선형 급상승→포화; 압축펠릿(filled)은 ln(σ)-P 선형. | **압력↑→σ↑→포화** 의 *재료-일반성* + 분체 vs 펠릿 거동차 = 우리 σ-vs-porosity/Heckel knee 의 문헌 맥락 |
| **2 (a–f)** | **압밀 역학·밀도·Heckel.** (a) 두 sieve 분율 SEM, (b) number-PSD, (c) cumulative number/volume PSD(D50_vol=89µm ⛔ 11-18: SI 표 S1 = D10 89 · D50 138 · D90 240 µm (>50 µm) — §3 정정 행), (d) 펠릿두께-vs-P + 압력 protocol scheme, (e) **ρ_rel-vs-P**(<50µm 가 더 치밀), (f) **"in die" Heckel plot** (regime I 재배열·파편화 / II 소성 / 회색띠) | ★ **Heckel ln(1/(1−ρ))=Kp+A** = 우리 Heckel(P_y=138)과 *동일 식*. regime I/II 분해 = 우리 압밀 단계. **작은 PSD → 더 치밀 BUT σ 는 더 낮음**(역설) |
| **3** | **σ_ionic-vs-pelletizing pressure (1차 cycle)**, 압축(filled)+release(hollow), <50/>50µm. max 4.1/5.7 @0.5GPa; release max 5.3/6.6. 압력 protocol insert. | ★★ **σ-vs-압력 핵심 데이터.** 저압 미세구조-지배(상승) ↔ 고압 ΔV-지배(하강), ~0.5 GPa 최대. release hysteresis = 비가역 소성(우리 Heckel·Doux 비가역) |
| **4 (a–c)** | **원자수준 ΔV.** (a) t-Li₇SiPS₈ 결정구조 + bond-valence iso-energy(c축 1D 채널), (b) AIMD MSD(f=1.0/0.99/0.98 격자scaling) → 압축시 확산↓, (c) **ln(σ)-vs-P 에서 ΔV≈1.4 cm³/mol** 추출(입자크기 무관) | ΔV = **압력이 σ 를 *낮추는* 원자기구**(격자압축→migration 부피 부족). 우리엔 없는 *원자축* — frame[5] 밖(우리 DEM/MPM 은 입자스케일) |
| **5** | **σ-vs-stack pressure** (고정 pelletizing 후 0.01 vs 0.1 GPa stack 에서 EIS). 0.1 GPa stack 이 0.01 보다 높은 σ — 표면균열·접촉저항 영향. | ★ **stack pressure 분리**(우리 운전압 40–70 / Cronau stack 구분). 0.1 GPa stack 권장 = 표면균열 닫기 |
| **6 (a,b)** | **DEM+FVA 시뮬 ↔ 실험 대조.** (a) <50µm Feret 히스토그램 + gamma fit(a=1.944,b=7.048) + DEM/FVA workflow(Scenario I/II), (b) **정규화 σ-vs-P: 실험(원) vs DEM/FVA(삼각) 2 시나리오** — regime II 잘 맞음, **regime I(저압)은 시뮬이 과대평가**(구형 가정 탓) | ★★ **우리 DEM→FVA→σ 파이프라인의 직접 평행 사례.** 시뮬이 *기하만으로* σ-vs-P 추세 재현. 저압 과대평가 = **구형 한계**(우리도 동일) |
| **S1** · `fig_S1.png` (SI p.S-2) | XRD (Debye–Scherrer 모세관 · Cu-Kα1) — <50 · >50 µm 두 분율 전 범위 (10–50°) + 23–30° · 46–48° 확대 | <50 µm 가 피크가 *조금* 넓다 → 영역 (결정자) 이 조금 작다 · 기기 넓어짐이 시료 FWHM 과 같은 자릿수라 크기 숫자는 못 낸다 (p.S-2) |
| **S2** · `fig_S2.png` (p.S-4) | SEM 영상 → 입경 · 형상 ImageJ 흐름도 (사용자 판단 마름모 넷) | 우리 SEM 이진 지도 정량 순서의 본 (흐림 → 문턱 → 분수령 → 채우기 → 분석) |
| **S3** · `fig_S3.png` (p.S-6) | (a) 원 SEM (b) Gaussian 흐림 (c) 이진 가면 (d) 거리 변환 분수령 (e) LUT glasbey (f) 거짓색 합성 | 분수령 연결 4 · 8 이 작은 입자의 둥글기 · 분리에 오차 (p.S-5) |
| **S4** · `fig_S4.png` (p.S-7) | <50 µm 거짓색 SEM 셋 (축척 200 µm) · 3475 입자 | 배율 때문에 작은 쪽이 잘린 PSD (p.S-7) |
| **S5** · `fig_S5.png` (p.S-8) | >50 µm 거짓색 SEM 다섯 (1000 µm) + (f) 큰 입자 표면 (50 µm) · 5118 입자 | 큰 입자의 거친 표면 = §S.2.9 DEM 한계 문장의 근거 그림 |
| **S6** · `fig_S6.png` (p.S-8) | <50 µm 누적 부피 % — LUMiSizer (원심 침강) vs SEM 영상 (수 분포에서 계산) | LUMiSizer D50 ≈ 10 µm [판독] · ⚠ SEM 곡선이 ≈ 6 µm 에서 100 % [판독] — 표 S1 (D90 60 µm) · 본문 Fig. 2c 와 10 배 어긋남 · 원문 설명 없음 |
| **S7** · `fig_S7.png` (p.S-11) | <50 µm 형상 산점 (solidity × convexity · 색 = sphericity (a) / Feret (b)) + 입자 윤곽 넷 | 대부분 convexity · solidity ≈ 0.9–1 · sphericity 낮음 (≈ 0.2–0.5) [판독] · 작은 입자일수록 convexity 가 높게 나오는 해상도 인공물 (p.S-11) |
| **S8** · `fig_S8.png` (p.S-12) | >50 µm 같은 그림 — convexity 0.6 · solidity 0.5 까지 퍼짐 (p.S-12) | ⚠ 캡션은 S7 과 같은 문장 ("2D-representations of four particles") 인데 그림에 윤곽이 없다 [판독] |
| **S9** · `fig_S9.png` (p.S-15) | (a) Heckel 모식 — 영역 I 재배열 · II 입자 소성 · III **압분체 탄성 변형** · IV **압분체 탄성 회복** (b) 소성 = 격자면 미끄럼 (c) 탄성 = 단위포 압축 (d) **"in die" (채움) vs "out of die" (빈 원 · 10 MPa 적층압)** | ★★ 탈압 회복의 크기 (§3 SI 행) · P_y 는 맞춤 구간에 따라 0.80–0.97 GPa (<50 in die) [판독 산술] |
| **S10** · `fig_S10.png` (p.S-16) | 펠릿 SEM — (a) 깬 단면 (200 µm) (b) 윗면 (50 µm) (c) 윗면 가까운 단면 (d) 가운데 단면 (20 µm) | 윗면 · 표면 근처에 금, 가운데는 치밀 [판독] · 압력 미기재 |
| **S11** · `fig_S11.png` (p.S-17) | Nyquist — (a) 0.01 · 0.05 · 0.1 GPa (kΩ) (b) 0.5 · 1.0 · 1.5 GPa (Ω) · 원 <50 · 삼각 >50 µm | 반원 없이 경사선만 (R + CPE 맞춤) · 저압은 압력↑ 절편↓, 고압 (b) 은 압력↑ 절편↑ (화살표) [판독] |
| **S12** · `fig_S12.png` (p.S-20) | ³¹P MAS NMR (a) 결정 (주황) · 비정질 곁상 (파랑) 맞춤 — 인쇄 8.2 → 9.7 wt% (<50) · 9.0 → 10.2 wt% (>50) (b) 94 · 73 ppm FWHM | 누르면 곁상 +1.2–1.5 wt%p · 선폭 +15–20 % [판독] — σ 영향은 정량 안 함 |
| **S13** · `fig_S13.png` (p.S-21) | ★ DEM 접촉면 합 vs 압력 (0.01–1.5 GPa) | 0.08 → 1.80 × 10⁶ µm² [판독] · 0.5 → 1.5 GPa 는 +27 % 뿐 — σ 가 고압에서 꺾일 때 기하는 포화 쪽 |
| **S14** · `fig_S14.png` (p.S-26) | 접촉 법칙 모식 — (a) 법선 스프링 k_N + 대시포트 d_N (b) 접선 스프링 k_T + 대시포트 d_T + Coulomb 미끄럼 | 우리 LIGGGHTS hooke/hysteresis 와 같은 집안의 선형 법칙 (단 그들은 이력 · 연화 없음) |
| **S15** · `fig_S15.png` (p.S-32) | DFT · AIMD 구조 모형 (a)–(g) — PS₄³⁻ (보라) · SiS₄⁴⁻ (파랑) 배치 일곱 | 탄성 텐서는 넷의 평균 (표 S6) · AIMD 는 일곱 배치 (p.S-31) |
| **S16** · `fig_S16.png` (p.S-34) | AIMD Li MSD 500–900 K — (a) 전체 (b) z (c) x (d) y · 0–80 ps | 900 K 80 ps MSD: 전체 ≈ 155 · z ≈ 95 · x ≈ 27 · y ≈ 30 Å² [판독] |
| **S17** · `fig_S17.png` (p.S-34) | 같은 MSD 를 온도별로 (a) 500 (b) 700 (c) 900 K — x · y · z 겹쳐 | z (= c) 가 x · y 의 ≈ 4 배 (p.S-33 *"on average four times higher"*) |
| **S18** · `fig_S18.png` (p.S-35) | Arrhenius — D* (전체) 136(13) · D*_a 146(19) · D*_b 165(15) · D*_c 127(13) meV (그림 인쇄) | 단결정 AIMD 값 — 측정 장벽 (0.27 eV, 본문) 보다 낮다 (저자 설명 = 고온 외삽 한계) |
| **S19** · `fig_S19.png` (p.S-39) | 아지로다이트 다섯 조성 펠릿 상대밀도 vs 압력 (Ohno 2020 [S49] ESI 재정리) + 평균 (점선) · ±1 SD 띠 | 평균 ≈ 84.3 % · 띠 ≈ 78.0–90.6 % [판독] · 압력과 양의 경향 없음 · ⚠ Li₆PS₅Cl 만 따로 못 뽑는다 (기호 구분 없음) |
| **표 S1** · `tab_S1.png` (p.S-9) | 부피 기준 D10 / D50 / D90 (Feret 에서 계산) — <50 µm 17 / 35 / 60 · >50 µm 89 / 138 / 240 µm | §3 정정 행의 근거 |
| **표 S2** · `tab_S2.png` (p.S-9) | 수 기준 D10 / D50 / D90 — <50 µm 3 / 11 / 27 · >50 µm 9 / 17 / 98 µm | 감마 b = 7.048 의 근거 (§3) |
| **표 S3** · `tab_S3.png` (p.S-13) | ImageJ 치수 변수 여덟 (A · p · D_Feret · D_Breadth · R_max · R_min · p_hull · A_hull, 단위 px) | 형상 서술자의 재료 |
| **표 S4** · `tab_S4.png` (p.S-14) | 무차원 형상 서술자 — AR · circularity 4πA/p² · solidity A/A_hull · convexity p_hull/p · sphericity R_min/R_max · compactness √(4A/π)/D_Feret | 우리 SEM 정량 (SE 형상) 의 정의표로 바로 쓸 수 있다 |
| **표 S5** · `tab_S5.png` (p.S-28 · 옆으로 누운 표 → 세움) | ★ DEM 입력 — ρ 1980 kg/m³ · ν 0.3 · k_N 0.01 N/m · c_cor 0.1 · μ 1.0 · g = 0 · 감마 a 1.944 · b 1.944 (인쇄) | §4 정정의 근거 · 값마다 저자 이유가 붙어 있다 |
| **표 S6** · `tab_S6.png` (p.S-36) | t-Li₇SiPS₈ 평균 강성 텐서 C_ij (GPa) — C11 38.5 · C22 41.7 · C33 40.5 · C12 26.4 · C13 13.5 · C23 15.4 · C44 11.4 · C55 9.6 · C66 17.8 (괄호 = 대칭상 0 이어야 할 항 < 1 GPa) | VRH 다시 계산: B 25.5 · G 11.5 · E 29.9 GPa · ν 0.30 [카드 산술] — 표 S7 의 B 23.5 와 2 GPa 어긋남 |
| **표 S7** · `tab_S7.png` (p.S-37) | B · E · G · ν · G/B — t-Li₇SiPS₈ (이 논문) · LGPS 둘 · Li₁₀SiP₂S₁₂ · Li₁₀SnP₂S₁₂ · **Li₆PS₅Cl 28.7 / 22.1 / 8.1 / 0.37 / 0.28** · Li₆PS₅Br · Li₆PS₅I ([S46] · [S47] 값) | LPSCl 행 = Deng 2016 [S47] 의 재인용 (2 차) · 같은 화합물 LGPS 의 E 가 37.19 ↔ 21.7 GPa 로 문헌 사이에 갈린다 |

> **Figure S (SI, 본 digest 범위 밖이나 본문 인용):** S9 = "in die" vs "out of die" Heckel(탄성 기여 분리),
> S10 = 1.7 GPa SEM(표면균열 수십 µm), S11 = Nyquist, S12 = ³¹P NMR(side phase·peak broadening),
> S13 = DEM contact surface, S17 = AIMD 이방성. SI 입수 시 §3 표 보강 가능.
>
> ⛔ **11-18 SI 반입 — 위 줄은 이력이다.** SI 그림 · 표는 아래 표 (SI 줄) 와 **§S** 에 전부 있다. 고친 것 둘: ① AIMD 이방성은 S17 한 장이 아니라 **S16 (온도별 MSD) · S17 (방향별 MSD) · S18 (Arrhenius · 장벽)** 셋 ② S10 · S12 의 "1.7 GPa" 는 **SI 캡션에 없다** (본문 값으로 보인다 — 본문 대조 불가). S10 의 균열 크기 "수십 µm" 도 SI 글에 수치가 없다 (그림의 축척 막대 50 µm 판 (b) 에서 길이 ≈ 10–20 µm 금들 [판독]).

## 6. Post-processing ★
- **무엇**:
  - ★ **Heckel 압밀해석** `ln(1/(1−ρ_rel)) = K·p + A` (eq 1) — **우리 Heckel 과 완전 동일 식**. 기울기 K 의
    역수 = **평균 항복압 P_y**(소성흐름 stress). **"in die"**(압축중 측정) vs **"out of die"**(해제후 측정) 구분 —
    탄성복원 분리. **3 영역 분류**: I(재배열·파편화, <0.5 GPa) / II(소성변형, 선형, >0.5 GPa) / III(공극소멸, ρ→90–95%).
    ↳ (11-18 SI 그림 S9a 캡션) SI 의 정의는 **넷**: I *particle rearrangement* · II *particle plastic deformation* · III ***compact elastic deformation*** · IV *compact elastic recovery* (탈압 가지) —
    III 의 이름은 "공극 소멸" 이 아니라 "압분체 탄성 변형" 이다 (본문 표현은 대조 못 함). "out of die" = *"extracted from stack (constant) pressure experiments at 10 MPa"* (S9 캡션) — 압력을 다 뺀 0 이 아니라 **10 MPa** 에서 잰 값.
    두 항 모형 (재배열 + 고체 압축) 원전 = Cooper–Eaton [S5] · Wünsch [S6] (p.S-15).
  - **활성화부피 ΔV** = `−k_B·T·(∂lnσ/∂p)` (eq 3, eq 2 의 단순화) — release sweep 의 ln(σ)-vs-P 선형기울기에서 추출.
    `ΔV = V_m − V_f`(eq 4, migration 부피 − free 부피).
    ↳ (11-18 SI p.S-18 – S-19 · 식 S1 – S7) 유도 전문: Arrhenius σT = σ₀ e^(−ΔG/k_BT) (S1) → ΔG = k_BT(ln σ₀ − ln σ) (S2) → σ₀ = z n q² r² ν₀ / k_B (S3) →
    ΔV ≡ (∂ΔG/∂p)_T,Ni (S5) → ΔV = k_BT[(∂ln σ₀/∂p) − (∂ln σ/∂p)] (S6) → 입방정 보정 ΔV = k_BT[β(γ − 2/3) − (∂ln σ/∂p)] (S7, β 압축률 · γ Grüneisen) — 본문은 앞 항을 버린 단순식을 쓴다 (본문 *"less than 10%"*, 카드 §5 Fig. 4 캡션).
    ⚠ SI 는 식 S16 의 출처를 *"equation (4) in main publication"* 이라 적는다 — 위 줄의 본문 식 번호 (eq 3 = 단순식) 와 어긋난다 · 본문 PDF 없이 못 가린다 [미확인].
  - **FVA 유효 σ**: DEM 입자 → voxel → 정상상태 전류분포 → σ_eff(정규화).
  - **NMR side-phase 정량**(³¹P MAS): 비정질 부상(side phase) wt% + peak broadening(압력유발 무질서).
  - **AIMD MSD → D → σ** (Nernst-Einstein), 격자 scaling f=0.98–1.00 로 압축효과.
- **도구**: ImageJ(+Legland/Landini plugins; ref 23–25) 로 SEM → PSD(Feret diameter). gamma 분포 fit. BACI(DEM),
  BEST(FVA), AIMD. RELAXIS-류 EIS fit(Nyquist).
  ↳ (11-18 SI) SEM: ImageJ [S14] + MorphoLibJ 거리 변환 분수령 [S1] + Landini *Morphology* (particles8) [S2] (그림 S2 · S3 · 표 S3 · S4) · 부피 PSD 교차 = LUMiSizer 원심 침강 (p-xylene + 4.5 wt% HNBR · 300→4000 rpm · 870 nm) ·
  EIS = RelaxIS 3 · Kramers–Kronig 시험 · 비례 가중 · 대개 1 MHz – 1 kHz 맞춤 · **등가 회로 = 저항 + CPE 직렬** (*"accounting for the ionic resistance and the polarization spike"*) — 입계 반원을 따로 맞추지 않았다 ·
  NMR = Bruker Avance-III 9.4 T · 4 mm · 10 kHz MAS · Bloch decay 512–4096 회 · Dmfit [S17] · DFT/AIMD = VASP (PBE · PAW).
- **수치화·플롯·기록 방식**: σ-vs-P 를 압축/release 두 가지로(hysteresis loop). Heckel 을 in-die/out-die 두 가지로.
  σ 정규화(σ/σ_0.5GPa, σ/σ₀)로 절대 bulk 가정 회피. DEM/FVA 와 실험을 **같은 정규화 축**에 겹쳐 그림(Fig 6b).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **소재** | t-Li₇SiPS₈ (LGPS-계 정방정 황화물) | LPSCl(argyrodite) | **같은 sulfide 패밀리·다른 구조** → 물리·압력거동 비교 OK, **σ/E/ΔV 절대값 transfer 금지** |
| **Heckel 식** | `ln(1/(1−ρ))=Kp+A` (eq 1) | **동일 식** | ✓ 같음 (P_y = 1/K) |
| **Heckel P_y** | **0.95 GPa(<50µm) / 1.65 GPa(>50µm)** ("in die") | **0.138 GPa(138 MPa)**, σ_y_eff≈46 MPa (pure-SE 4압력) | ⚠ **그들이 7–12× 높음** — *압력대 다름*(그들 GPa 영역 측정, 우리 ≤300 MPa) + *소재 다름* + *in-die vs out-die*. **추세(작은 입자→낮은 P_y→소성쉬움)는 같은 방향** |
| **압밀 압력대** | **0.01 → 1.7 GPa** (고압 ΔV 보려 일부러) | **300 MPa cold-press** | 우리 제조압 = 그들 *저압 regime I/II 경계*(0.3–0.5 GPa) 근방. 그들 GPa 고압은 우리 범위 밖 |
| **ρ_rel @ 고압** | **90–95 %** (porosity 5–10 %) @ >~1 GPa | pure-SE **~90 %**(porosity 10 %) @300 MPa | ⚠ 우리가 *훨씬 낮은 압력*에서 같은 밀도 — 소재·측정·convention 차. **추세만** |
| **입자 처리** | **구형 + overlap(CONTACT)**, 형상변화 없음 | DEM 구형+overlap / **MPM 진짜 SHAPE 소성** | 우리 MPM 이 그들(+Bazzoun/Varkey) 못 가진 *형상흐름* 보유 (frame[5]) |
| **σ readout** | **FVA(voxel-FVM) 연속체**, constriction 명시 없음 | **Kirchhoff/Holm 점접촉 constriction** | 우리 = 명시적 contact-network constriction; 그들 FVA = 연속체(Bielefeld2020 처럼 *상한*에 가까움) |
| **σ 절대 캘리브** | **회피**(정규화 σ/σ₀ — 기하효과만) | σ_grain=3.0·Cronau 절대 캘리브 | 그들은 *상대추세* 전용 설계, 우리는 절대값 예측 — **목적 다름** |
| **σ 채널** | **σ_ionic 만** (SE-only) | σ_ionic + σ_e + σ_thermal | 우리 삼중항 우위 |
| **σ vs porosity** | ★ **"porosity 는 σ 의 *약한* descriptor, PSD 가 *강한* descriptor"**(명시 결론) | σ_ionic = f(φ_eff, CN², cov, packing) — **porosity 단독 아님** | ★ **정합!** 우리도 porosity 외 CN/cov/packing 이 σ 지배 — 그들이 *실험으로* 같은 결론 |
| **σ vs 입자크기** | **작은 입자(<50µm) → σ *낮음***(grain contact 불량·misorientation) | Cronau(r_SE): sub-µm → σ↓; packing: 작은 SE → σ↑(접촉多) | ⚠ **부호 주의**(아래 §A 상세) — 그들 50µm vs sub-µm 의 두 효과 분리 필요 |
| **활성화부피 ΔV** | **1.4 cm³/mol** (압력↑→σ↓ 원자기구) | **n/a**(우리 입자스케일, 원자 ΔV 없음) | 그들 고유 — frame[5] 밖(원자축) |
| **DEM/FVA 저압 과대평가** | **regime I 시뮬>실험**(구형 탓) | 우리도 구형 한계 동일 | ★ **공통 한계** — 우리 MPM(형상)·de Larrard(packing)이 보완 방향 |
| **DEM 접촉 법칙 (11-18 SI)** | 강체 구 · 선형 스프링–대시포트 + Coulomb 마찰 (식 S10 – S14) · **k_N 0.01 N/m (반력을 안 씀)** · 점착 · 소성 · 구름 저항 없음 | LIGGGHTS hooke/hysteresis · E_eff 1.35 GPa (18 배 연화 — 압력이 물리량) | 그들은 **두께를 실험에서 받는다** = DEM 이 압밀을 예측하지 않음 · 우리는 압력 → 기공을 내고 실험과 맞춘다 ⇒ 그들 DEM 에서는 Heckel P_y 가 나올 수 없다 [카드 해석] |
| **탈압 (11-18 SI)** | 실험 out of die (10 MPa) 회복 3.7 · 2.7 %p @ 1.7 GPa [판독 S9d] · **DEM 탈압 없음** (SI 에도 없음) | DEM 언로딩 (진행 중) | 크기 감각만 — 재료 · 압력대 · 측정 상태 다름 |
| **σ 읽기의 가지 (11-18 SI)** | FV = 균질상 · 입계 저항 0 (p.S-29 – S-30) | 접촉망 (Holm 협착) + 복셀 FV (STEP3 = CONTACT_FREE 가지, 원장 CL-81) | 그들의 저압 과대평가 = 계면 · 협착 항이 없는 가지가 내는 방향과 같다 [카드 해석] |
| **랩 표준과 나란히 (11-18 SI)** | 0.3 GPa ρ_rel ≈ 81.5 % (<50) · 79.5 % (>50) = 기공 18.5 · 20.5 % [판독 S9d · 진밀도 2.008 기준 · in/out 겹침] | 순수 SE 기공률 10–13 % · 진밀도 1.64 g/cm³ (랩 표준 · 고정) | **랩 표준과 다른 문헌 값** — 재료 (t-Li₇SiPS₈) · 진밀도 기준이 다르다 · 판정하지 않는다 (진밀도를 1.923 으로 바꾸면 기공 ≈ 15 · 17 % [카드 산술]) |

> ⛔ **11-18 표지 (지위 정정 — SI 와 무관하게 원장을 따른다)**: 위 '우리' 열의 *"pure-SE ~90 %(porosity 10 %) @300 MPa"* 는 우리 MPM 보정 수렴값이다 (출처 [미확인] · 원장 `CL-94` — 외부 앵커 아님).
> *"σ_grain=3.0·Cronau 절대 캘리브"* 의 Cronau(r_SE) 인자는 출처 없는 모델 가정 (원장 `SELF-51`) · 3.0 mS/cm 은 Cronau 2021 SI 그림 S2c 의 펠릿 평탄값 하단 (`CL-91`). 이 카드의 SI 보강은 두 지위를 바꾸지 않는다.

## A. 우리 DEM+MPM 대비 (comparison vs ours) — σ(입자크기) & σ(압력)

### A-1. σ(입자크기) — ⚠ 부호 충돌 주의: **두 개의 *반대* 크기효과를 분리해야 한다**
이 논문의 핵심 역설: **작은 입자(<50µm)가 *더 치밀*(ρ_rel↑, Fig 2e)인데도 σ 는 *더 낮다*(Fig 3, 3.8 vs 5.7 mS/cm).**
저자 해석(본문): "<50µm 는 같은 질량에 입자수가 많아 **grain-to-grain 접촉이 많고**, 그 접촉들이 **불리한
grain 방위(misorientation)** 를 가져 **intergranular 저항↑**. Harm et al.(ref 38): t-Li₇SiPS₈ 는 intra-/inter-grain
확산이 섞이며 **inter(grain-boundary) 길이스케일에서 확산이 더 빠름** → 작은입자=GB 많음=병목." 즉 **"작을수록 σ↓"
는 *GB(입계) 저항* 메커니즘**.

우리 모델의 두 크기항과 대조:
- **(i) 우리 Cronau(r_SE) sub-µm σ_grain 감쇠**(작은 r_SE → σ↓): **부호 일치 + 메커니즘 일치!** Cronau digest
  (`docs/lit_cronau2021_*.md` §0(B))가 이미 판정했듯, Cronau(r_SE)의 진짜 물리는 "입자가 작아서"가 아니라
  **"미세결정·소결불량 → grain-contact/GB 불량 → σ↓"** 이다. **이 Schneider 논문이 바로 그 GB 메커니즘을
  *같은 황화물에서 실험으로* 보여줌**("작은입자=GB多=σ↓") → ★ **Cronau(r_SE) 인자의 *부호*에 대한 두 번째
  same-family 실험 근거.** (단 그들 크기축은 **<50µm vs >50µm**(수십 µm 영역), 우리 Cronau breakpoint 는
  **sub-µm(0.03–0.5µm)** — *스케일이 다름* → 부호·메커니즘만 지지, breakpoint 수치 미지지. Cronau 와 동일.)
- **(ii) 우리 packing "size=PACKING"(작은 SE → 접촉多 → σ↑)**: **부호 반대**. 우리·Bazzoun·Minnmann2021 의
  composite "작은 SE → σ_eff↑" 는 *composite 에서 SE 가 CAM 공극을 채우는 packing/percolation* 효과. **Schneider
  는 SE-only 펠릿** → packing-percolation 이득이 없고 **GB 저항만 남아** σ↓. ⇒ **모순 아님, 층위 분리**:
  *composite packing*(우리 σ↑) ≠ *SE-only GB*(Schneider σ↓). 우리 σ_ionic 식이 **둘 다** 담아야 함:
  packing/CN 은 σ↑(composite), Cronau/GB 는 σ↓(미세결정) — **이미 우리 식에 둘 다 있음**(CN²·cov ↑, Cronau ↓).
  Schneider 가 **GB 항(Cronau)** 의 실험 정당성을 SE-only 에서 깨끗이 보여준 것.

> ⛔ **11-18 SI 대조 — "GB 기전을 실험으로 보여줌" 은 과장이다** (옛 문장은 이력으로 둔다).
> ① EIS 맞춤 회로 = **저항 하나 + CPE** (*"a resistor in series with a constant phase element, accounting for the ionic resistance and the polarization spike"*, p.S-25) — 입계 저항을 따로 재지 않았다 (그림 S11 에 반원이 없다).
> ② FV 는 *"without any additional grain boundary resistances"* (p.S-29 – S-30) — 시뮬레이션은 이 가설을 시험하지 못한다.
> ③ XRD 는 <50 µm 영역이 "조금 작다" 까지 (*"a precise domain size determination by XRD is not feasible"*, p.S-2).
> ④ SI 의 협착 문장 (Fleig [S11] — 접점이 많을수록 협착 · 입계 저항이 작다, p.S-21) 은 **압력 축** (저압에서 접점이 적다) 설명이지 크기 축 설명이 아니다.
> ⇒ 이 논문이 **잰 것** = "<50 µm 분율의 펠릿 σ 가 낮다". 입계 · 방위 기전은 **저자 해석** (디커플링 안 됨).
> 또 우리 `Cronau(r_SE)` 는 출처 없는 모델 가정이다 (원장 `SELF-51` · Cronau 2022 원문에 그 구간값 없음) — 이 논문을 그 인자의 *부호 근거* 로 인용하지 않는다 (크기 축도 수십 µm ↔ sub-µm).

### A-2. σ(압력) — 우리 σ-vs-porosity(compaction) 와 정합 + ΔV 라는 *추가* 고압 반전
이 논문은 σ-vs-P 를 **두 영역**으로 분해(우리에게 직접 매핑):
- **저압 regime I/II (≤0.5 GPa): 압력↑ → 미세구조 개선(접촉면적↑·공극↓) → σ↑.** = ★ **우리 σ-vs-porosity
  (porosity↓→σ↑)·Heckel knee 와 *정확히 같은 물리***. 그들 σ 가 0.01→0.5 GPa 에서 0.3→4.1 mS/cm(<50µm) 급상승 =
  우리 "압밀↑→contact-network↑→σ↑"·Bazzoun "σ-vs-P 상승"·Doux "접촉@~25 MPa 포화"·우리 Heckel P_y=138 와 같은 계열.
- ★ **고압 regime (>0.5–0.7 GPa): 압력↑ → 격자압축(ΔV) → σ↓.** = **우리엔 *없는* 반전.** 우리 DEM/MPM 은 입자스케일
  (porosity↓→σ↑ 단조)이라 **격자압축이 σ 를 *낮추는*** 원자효과를 못 본다. → **우리 σ-vs-P 는 ~0.5 GPa 아래(우리
  제조 300 MPa 는 여기)에서만 단조 상승으로 유효**; 그 이상은 ΔV 반전이 시작. **우리 작동범위(300 MPa)에서는 ΔV
  무시 가능**(저자도 "stack pressure 0.1 GPa 에선 ΔV 무시" 명시) → **우리 σ-vs-porosity 모델은 우리 압력대에서 안전**.
  ⛔ **11-18 SI 식 S16 으로 크기를 잰다 [카드 산술]**: ΔV 1.4 cm³/mol · 25 °C (EIS 온도, p.S-24) 면 bulk σ 배율 = exp(−ΔV·Δp/(k_B T)) = exp(−0.565 × Δp[GPa]) →
  0.1 GPa **0.945 (−5.5 %)** · **0.3 GPa 0.84 (−16 %)** · 0.5 → 1.7 GPa **0.51**. ⇒ "300 MPa 에서 무시 가능" 은 **σ 를 그 압력을 건 채 잴 때** 맞지 않는다.
  효과는 **가역**이다 — 누른 뒤 낮은 적층압에서 재면 그 압력 값만 남는다 (0.01 GPa → −0.6 %). 저자 문장 ("0.1 GPa 에선 거의 무시", 본문 Fig. 6 캡션) 과는 맞다 (−5.5 %). **LPSCl 의 ΔV 는 이 논문에 없다.**
- **σ-vs-porosity 강도**: ★ 저자 결론 **"relative density(porosity)는 σ 의 *약한* descriptor, PSD 가 *강한*
  descriptor"** → 우리 σ_ionic 가 porosity 단독이 아니라 **φ_eff·CN²·cov·packing(=PSD 의존)** 으로 짜인 것과
  **정합**. "porosity 만으로 σ 예측 불가"는 우리 5-항 형태(LOOCV 0.975)의 실험적 정당화.

### A-3. DEM/FVA 파이프라인 — 우리와 가장 직접적인 평행 + 공통 한계
Fig 6b: 그들 **DEM(입자압밀) → voxel → FVA(연속체 σ)** 가 **정규화 σ-vs-P 추세를 *기하만으로* 재현**(regime II
잘 맞음). = ★ **우리 DEM→네트워크 σ 와 같은 정신.** 차이: 그들 readout 은 **FVA 연속체**(constriction 없음 →
Bielefeld2020 처럼 *상한*), 우리는 **Kirchhoff/Holm 점접촉 constriction**(더 물리적). **공통 한계: 둘 다 구형 →
저압 regime I 과대평가**(그들 명시) → 우리 MPM(형상)·de Larrard(packing)이 메우는 방향.

## B. 적용가능성 (applicability to our model)

### B-1. ★ backlog B6 (우리 Heckel P_y / σ-vs-P) 직접 앵커
- **Heckel 식 동일**: 그들 `ln(1/(1−ρ))=Kp+A` = 우리 식. **P_y(작은 PSD)=0.95 < P_y(큰 PSD)=1.65 GPa** →
  **"작은 입자 → 낮은 P_y → 소성변형 쉬움(더 치밀)"** 가 *같은 황화물에서 실측*. ⇒ 우리 DEM Heckel(P_y=138 MPa,
  pure-SE)·MPM σ_y_eff 의 **PSD-의존성** 검증 후보: 우리도 **bimodal vs monomodal Heckel P_y 를 비교**하면 같은
  부호가 나와야 함(우리는 아직 *조성*만 Heckel, *PSD* Heckel 미수행). **frame[3] universal compaction physics 확장**.
  ⚠ 절대 P_y(0.95/1.65 GPa)는 *그들 GPa 측정·다른 소재* → **부호·PSD-순서만 transfer**, 138 MPa 와 절대대조 금지.
- **σ-vs-P 영역분해**: 우리 σ-vs-porosity 는 **regime I/II(≤0.5 GPa)** 에 해당 → 우리 300 MPa 제조압은 그들
  **저압 미세구조-지배 영역**(σ↑) 안 → **우리 σ-vs-porosity 단조성은 우리 압력대에서 유효**(ΔV 반전 전). 이를
  명시하면 우리 모델의 *유효 압력범위*를 정직하게 bound 할 수 있다.

### B-2. ★ backlog B5 (우리 Cronau(r_SE) σ_grain 크기/GB 인자 — 이중계상 점검)
- Schneider 의 **"작은입자 → GB 많음 → σ↓"** (SE-only, 실험) = **Cronau(r_SE) 의 *부호*에 대한 두 번째 same-family
  근거**(Cronau 는 Br-argyrodite, Schneider 는 LGPS-계 — 둘 다 sulfide, 둘 다 GB 메커니즘). ⇒ Cronau digest 의
  "Cronau(r_SE) 를 *결정도/grain-contact 효율 인자*로 재명명" 권고를 **강화**: GB 가 σ 병목이라는 게 *두 황화물에서
  독립 확인*. **흡수 후보**: 우리 σ_grain prefactor 의 GB 항을 *입자수밀도(grain contact 수)* 로 재파라미터화하면
  Schneider 의 "<50 vs >50µm" 거동까지 설명 가능(현재 우리 Cronau 는 sub-µm 만).
- ⚠ **이중계상(double-count) 주의**: 우리 σ_ionic 에 **CN²(접촉수 → σ↑)** 와 **Cronau(GB → σ↓)** 가 *둘 다* 있다.
  Schneider 는 "접촉 *수*↑ 인데 σ↓"(작은입자) — 즉 **접촉수와 GB-품질이 *반대로* 작용**. 우리 CN² 가 접촉수만 보고
  Cronau 가 품질을 보므로 **개념적으로 분리돼 있어 이중계상은 아님**. 단 *작은 입자에서 CN²↑ 와 Cronau↓ 가
  상쇄*되는지 우리 corpus 로 점검할 가치(Schneider 가 SE-only 에서 GB↓ 가 이긴다고 보임 → 우리 SE-rich 코너에서
  같은 상쇄가 나오나 확인).
- ⛔ **11-18 표지**: 위 두 줄의 "GB 메커니즘 독립 확인" · "두 번째 same-family 근거" 는 **성립하지 않는다** — ① GB 저항은 이 논문에서 따로 재지 않았다 (EIS = R + CPE 하나 · FV 계면 저항 0 — §A-1 SI 대조) ② `Cronau(r_SE)` 자체가 출처 없는 모델 가정이다 (원장 `SELF-51`).
  남는 것: "SE-only 펠릿에서 큰 분율이 σ 가 높다" 는 **관찰** 하나 (크기 축 = 수십 µm 의 두 체 분율). 재파라미터화 제안은 근거가 생길 때까지 보류.

### C. frame[4] 위치 (experimental anchor)
- **이 논문 = frame[4] 외부 실험+시뮬 앵커, DEM 경쟁자 아님.**
  - **experiment(EIS σ-vs-P/크기) → 앵커**: σ_ionic max 4.1/5.7 mS/cm @0.5 GPa, ΔV 1.4 cm³/mol, Heckel P_y
    0.95/1.65 GPa, ρ_rel 90–95% — *t-Li₇SiPS₈ 고유*. **우리 LPSCl 모델의 *추세·물리* 검증점**(절대값 transfer 금지).
  - **우리 SIMULATION 이 *더하는* 것**: (1) **명시적 3D contact-network σ**(Kirchhoff/Holm constriction) — 그들
    FVA 는 연속체(constriction 없음 → σ 상한); (2) **σ_e + σ_thermal 삼중항**(그들 ionic-only); (3) **진짜 SHAPE
    소성 morphology**(MPM) — 그들 구형 한계(저압 과대평가)를 메움; (4) **composite(CAM+SE) packing/Furnas dip**
    (그들 SE-only); (5) **fracture-Holm/Auerbach**(그들 없음). ⇒ 그들이 *측정/연속체-시뮬* 한 σ(P,size)를, 우리는
    *접촉역학에서 emergent 하게* + *composite·삼중항·morphology* 로 확장.
  - **소재 transferability caveat**: t-Li₇SiPS₈ ≠ LPSCl(다른 구조·다른 σ 절대값·다른 ΔV·다른 E). **같은 황화물
    cold-press 물리**(Heckel 영역, σ-vs-P 형태, GB-vs-크기 부호, 구형-DEM 한계)는 transfer OK; **절대 σ/P_y/ΔV/밀도
    수치는 LPSCl 쪽 앵커(Minnmann/Doux/Cronau/우리 DEM)** 가 소유. ⇒ densification/σ DB 에 넣되 *별도 material 태그*.

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **σ-vs-porosity 의 "약한 descriptor" 정당화 + 유효 압력범위 bound**: Schneider 의 "porosity 는 약한
  descriptor, PSD 가 강한" 실험결론 → 우리 σ_ionic 5-항(porosity 외 CN/cov/packing) 형태의 *실험 정당화*. 동시에
  **고압 ΔV 반전**(>0.5 GPa σ↓)을 근거로 **우리 σ-vs-porosity 단조모델의 유효범위 = ≤~0.5 GPa(우리 300 MPa 포함)**
  를 명시 → over-claim 방지(우리는 ΔV 원자효과를 안 다룬다고 정직 표기).
- ② ★ **Cronau(r_SE) GB 인자의 두 번째 same-family 부호근거 + 접촉수↔GB 분리**: "작은입자→GB多→σ↓" 가 LGPS-계
  황화물에서도 성립 → Cronau(r_SE) *부호* 재확인. 우리 CN²(접촉수↑→σ↑) vs Cronau(GB↓) 의 *반대작용*을 우리 SE-rich
  코너에서 점검(Schneider 는 SE-only 에서 GB 가 이김). **backlog B5(이중계상 점검) 의 실험 레퍼런스**.
  ⛔ 11-18: "부호근거" · "GB 가 이김" 은 철회 쪽 — GB 는 따로 재지 않았고 (§A-1 SI 대조) `Cronau(r_SE)` 는 출처 없는 모델 가정 (원장 `SELF-51`). 남는 것 = 관찰 ("<50 µm 분율 σ 가 낮다") 뿐.
- ③ ★ **PSD-의존 Heckel 비교(우리가 아직 안 한 것)**: 우리 Heckel 은 *조성*만(P_y=138). Schneider 처럼 **monomodal
  vs bimodal PSD 의 P_y 차이**(작은 PSD→낮은 P_y)를 우리 DEM/MPM 으로 재현하면 frame[3] universal-compaction 을
  *PSD 축*으로 확장. **DEM/FVA→σ 파이프라인 자체가 우리와 평행**(Fig 6) → positioning 근거(우리는 contact-network
  constriction + 삼중항 + MPM morphology 로 그들 FVA-연속체-ionic-only-구형 을 넘어선다).
  ⛔ 11-18: 그들 DEM 은 두께를 실험에서 받으므로 (SI 표 S5 · p.S-29) **DEM 쪽 P_y 를 내지 못한다** — "PSD 의존 Heckel" 비교는 그들 **실험** P_y (0.95 · 1.65 GPa, in die) 와만 할 수 있다 · P_y 는 맞춤 구간에 따라 움직인다 (그림 S9d 판독 산술: <50 µm 0.80–0.97 · >50 µm 1.25–2.39 GPa) — 비교할 때 구간을 같이 적는다.

## 9. 인용 가능 문장 (deck/paper용)
- "For the LGPS-type sulfide t-Li₇SiPS₈, Schneider et al. (2023) showed by combined EIS, DEM compaction and
  finite-volume σ analysis that the ionic conductivity of a pressed pellet is governed *more strongly by the
  particle-size distribution than by relative density (porosity)* — an experimental justification for casting
  σ_ionic as a function of coordination, coverage and packing rather than porosity alone."
- "Their Heckel analysis (ln[1/(1−ρ)] = Kp + A, identical to ours) yields a mean yield pressure P_y of 0.95 GPa
  for the small PSD versus 1.65 GPa for the large PSD, confirming — in a sulfide of the same family as our LPSCl —
  that a finer powder plastically densifies more easily (lower P_y), the same size-ordering our DEM Heckel exhibits."
- "Their DEM→FVA pipeline reproduces the σ-vs-pressure trend from geometry alone but *over-predicts the low-pressure
  (regime I) conductivity because the model uses perfect spheres* — the very rigid-sphere limit our MPM (true plastic
  shape change) and de Larrard packing are designed to fill (frame [5])."
- "Above ~0.5 GPa the conductivity *decreases* with pressure through a positive activation volume (ΔV ≈ 1.4 cm³/mol,
  lattice compression), an atomistic effect outside the particle-scale DEM/MPM picture; below it (our 300 MPa
  fabrication regime) σ rises monotonically with densification, where our σ-vs-porosity model is valid."

## 10. 주의/한계 (over-claim 방지)
- ★ **소재 = t-Li₇SiPS₈(LGPS-계 정방정), NOT argyrodite LPSCl.** 위시리스트 추정 제목과 다름. **같은 황화물
  패밀리**라 *물리·압력거동·방법론*은 비교 가능하나, **σ 절대값(4.1/5.7 mS/cm), Heckel P_y(0.95/1.65 GPa),
  ΔV(1.4 cm³/mol), 밀도(90–95%)는 소재고유 → LPSCl 로 transfer 금지**. (Cronau Br-argyrodite·Sakuda glass 와
  동일한 same-family-not-LPSCl 주의.)
- **SE-only 펠릿**(CAM/composite 아님). σ 는 *재료 자체* σ(blocking electrode) → **composite σ_eff,ion**
  (Bazzoun/Minnmann/우리)과 **층위 다름**. 그들 "작은입자→σ↓"(SE-only GB) 를 우리 *composite* "작은 SE→σ↑"
  (packing)와 *직접* 충돌시키면 안 됨(§A-1: 다른 층위).
- **DEM = 구형 + overlap(CONTACT) 계열**, 형상변화 없음 — Bazzoun/Varkey 와 동일. 저자 *스스로* "perfect spheres
  ↔ 실제 비구형 분말 차이가 저압 과대평가 원인"·"grain boundary 저항은 FV 시뮬에 미포함"·"마찰·접촉저항이 DEM 에
  완전히 반영 안 됨" 명시 → **frame[5] 전달 절반(우리 MPM morphology 미보유)** 의 또 하나의 독립 확증.
- **σ = 정규화(σ/σ₀) — 상대추세 전용.** 절대 bulk σ 캘리브를 *의도적으로 회피* → **그들 시뮬 σ 절대값과 우리
  절대 σ 를 직접 대조 금지**(우리 Cronau σ_grain 절대값과 다른 철학). 추세·물리만.
- **압력대 다름**: 그들 측정 **0.01–1.7 GPa**(고압 ΔV 보려), 우리 제조 **0.3 GPa**. **Heckel P_y·ρ_rel·σ 절대값을
  우리 300 MPa 값과 직접 동일시 금지** — 그들 GPa 영역은 우리 범위 밖(regime III·ΔV 반전).
- **ΔV(활성화부피)·AIMD·NMR = 원자/결정 스케일** — 우리 DEM/MPM(입자스케일) 의 frame[5] *밖*. 우리가 "검증"하는
  게 아니라 *우리가 안 다루는 축*을 그들이 보여줌(정직히).
- **digitized vs stated**: σ max(4.1/5.7/5.3/6.6), P_y(0.95/1.65), ΔV(1.4), ρ_rel(90–95%), side-phase(8.2–10.2 wt%),
  gamma(a=1.944,b=7.048), D50_vol(89µm) = **stated**. 펠릿두께(1600→1000µm)·Fig3/Fig6 곡선 형태 = digitized(추세).
  E_SE/σ_y/ν 수치·coverage/Z/σ_e/σ_thermal = **본 논문에 없음(n/a)** — SE-only·SI-only.
  ⛔ **11-18 SI 반입 뒤 고침**: ① "D50_vol(89µm) = stated" → SI 표 S1 로 **D10 89 · D50 138 µm** (§3 정정 행) ② "gamma b = 7.048" 은 본문 값 · SI 표 S5 는 1.944 로 인쇄 (오기로 보임 · §S.3) ③ "E · ν = SI-only" → SI 에 있다: DFT E 29.5 · B 23.5 · G 11.4 GPa · ν 0.29 (표 S7) · DEM ν 0.3 · k_N 0.01 N/m (표 S5) · **σ_y 는 SI 에도 없다** ④ 새 SI 판독값 (S9d · S12b · S13 · S19) = `si_digitized.csv` · 모두 [판독] — 추세 · 크기 감각 전용.
- ⛔ **11-18 SI 로 더해진 한계 (저자 원문)**: DEM *"perfect spheres"* ↔ *"particles that are far from spherical"* (p.S-21) · FV *"without any additional grain boundary resistances"* (p.S-29 – S-30) · AIMD *"represent the single crystal properties and do not consider grain boundiers or (amorphous) side phases"* (p.S-33) · XRD *"a precise domain size determination by XRD is not feasible"* (p.S-2) · PSD *"truncated at smaller particle sizes, as a consequence of the chosen image magnification"* (p.S-7) · 마찰 *"Since we do not have further information on that we used a value from the middle of the range"* (표 S5). 세미나용 정리 = §세미나 준비 (e).

## S. 보충 자료 (SI) 절별 정리 (2026-11-18 반입 · 46 쪽)

> 원문 = SI PDF (`litdb/inbox/34._Sup_…pdf`, 46 쪽 · 1 쪽 = 출판사 표지 · 2 쪽 = S-1) — **이 절의 쪽 표기는 SI 인쇄 쪽 (S-n) · PDF 쪽 = n + 1**.
> 값 표지: **[SI 인쇄]** = SI 글 · 표 · 그림 안에 인쇄된 수 · **[판독]** = 그림에서 읽은 값 (방법 = `si_digitized.csv` 머리 · 추세 전용) · **[카드 산술]** = 이 카드가 계산 (식 같이) · **[미확인]** = SI 를 다 보고도 없음.
> SI 식 번호 (1)–(16) 을 이 카드는 **식 S1–S16** 으로 부른다 (본문 식 (1)–(4) 와 섞이지 않게).

### S.1 SI 지도 (쪽 → 내용 → 크롭)

| SI 쪽 | 절 (SI 제목) | 그림 · 표 · 식 | 크롭 (`litdb/figures/schneider2023_particle_size_pressure_transport/`) |
|---|---|---|---|
| S-1 | 표제 · 저자 · 소속 | — | — |
| S-2 | Crystallite Size of pristine Li₇SiPS₈ | 그림 S1 | `fig_S1.png` · `txt_S2_xrd_domain_size_not_feasible.png` |
| S-3 – S-6 | Process of SEM image analysis using ImageJ | 그림 S2 · S3 | `fig_S2.png` · `fig_S3.png` |
| S-7 – S-9 | Particle size distribution | 그림 S4 – S6 · 표 S1 · S2 | `fig_S4.png` – `fig_S6.png` · `tab_S1.png` · `tab_S2.png` |
| S-10 – S-14 | Morphology of t-Li₇SiPS₈ particles | 그림 S7 · S8 · 표 S3 · S4 | `fig_S7.png` · `fig_S8.png` · `tab_S3.png` · `tab_S4.png` |
| S-15 – S-16 | Pellet densification · Comment on pellet recovery | 그림 S9 · S10 | `fig_S9.png` · `fig_S10.png` · `txt_S15_S16_pellet_recovery_cracks_ejection.png` |
| S-17 | Nyquist plots | 그림 S11 | `fig_S11.png` |
| S-18 – S-19 | Derivation of Activation Volume | 식 S1 – S7 | `eq_S01_…` – `eq_S07_…` |
| S-20 | ³¹P-NMR of pristine and pressed | 그림 S12 | `fig_S12.png` |
| S-21 | Discrete element method simulation | 그림 S13 | `fig_S13.png` · `txt_S21_dem_perfect_spheres_roughness_constriction.png` |
| S-22 – S-25 | Methods — 합성 · 체 · SEM · 비중병 · NMR · 가변 압력 · EIS | — | `txt_S22_…` · `txt_S23_…` · `txt_S24_variable_pressure_cell.png` · `txt_S24_S25_eis_conditions_fit_r_cpe.png` |
| S-25 – S-28 | DEM and FV Simulation (DEM 부분) | 식 S8 – S14 · 그림 S14 · 표 S5 | `eq_S08_…` – `eq_S14_…` · `fig_S14.png` · `tab_S5.png` · `txt_S25_dem_purpose_rigid_spheres.png` |
| S-29 – S-30 | (같은 절 · FV 부분) | 식 S15 · S16 | `eq_S15_…` · `eq_S16_…` · `txt_S29_…` ×2 · `txt_S29_S30_fv_homogeneous_no_gb_resistance.png` |
| S-31 – S-35 | DFT and AIMD Simulations · Structural Models · Molecular dynamics | 그림 S15 – S18 | `fig_S15.png` – `fig_S18.png` · `txt_S33_aimd_anisotropy_barriers_limits.png` |
| S-36 – S-37 | Elastic properties | 표 S6 · S7 | `tab_S6.png` · `tab_S7.png` |
| S-38 – S-39 | Densities of Pressed Argyrodite Pellets — A Metadata Analysis | 그림 S19 | `fig_S19.png` · `txt_S38_…` ×2 |
| S-40 – S-45 | References S1 – S49 | — | — |

### S.2 절별 정리

#### S.2.1 결정자 크기 — 그림 S1 (S-2)
- **무엇**: 두 체 분율 XRD (STOE StadiP · Debye–Scherrer 모세관 · Cu-Kα1) · 10–50° 전 범위 + 피크 확대 (`fig_S1.png`).
- **숫자**: FWHM · integral breadth 의 **값은 인쇄 안 됨** ("slightly broader" 뿐) [미확인] · 기기 넓어짐 기준 = Si NIST 640d · *"instrumental broadening … is almost on the same order as the FWHM or integral breadth of the t-Li₇SiPS₈ sample"*.
- **받치는 주장**: 본문의 "<50 µm 는 입계가 많다" 쪽 — 단 *"a precise domain size determination by XRD is not feasible, the slightly larger FWHM of the <50 um sample indicates slightly smaller domain sizes"* 까지만 (`txt_S2_…`). 정량 근거가 아니다.

#### S.2.2 SEM 영상 분석 절차 — 그림 S2 · S3 (S-3 – S-6)
- **무엇**: ImageJ 흐름도 (입력 · 처리 · 사용자 판단 세 칸 — 영상 질 · 과노출 · 배경 분리 · 입자 분리) 와 그 단계 그림 여섯 (원 · Gaussian 흐림 · 문턱 가면 · 거리 변환 분수령 · LUT glasbey · 거짓색).
- **숫자**: 없음 (절차).
- **판단 근거로 적힌 오차원** (S-3, S-5): 흐림은 경계를 흐린다 · 분수령 선의 4 · 8 연결 선택이 작은 입자 둥글기와 분리 판정에 영향 · 단일 조성이라 SE 영상 (지형) 을 썼고 복합 양극이면 BSE (조성) 를 함께 쓰라고 권한다.
- **받치는 주장**: 본문 Fig. 2a 거짓색 영상 · 2b–c PSD 의 출처. ★ 우리 SEM 이진 지도 정량 (`docs/lab_ai_workflow_conventions.md` 의 SEM binary-map) 에 그대로 옮길 수 있는 절차.

#### S.2.3 입경 분포 — 그림 S4 – S6 · 표 S1 · S2 (S-7 – S-9)
- **무엇**: <50 µm 거짓색 3 장 (축척 200 µm · **3475 입자**) · >50 µm 5 장 (1000 µm · **5118 입자**) + 큰 입자 표면 (50 µm) · <50 µm 의 부피 PSD 를 **LUMiSizer** (원심 침강 · p-xylene + 4.5 wt% HNBR · 300 → 4000 rpm · 870 nm) 와 SEM 계산값으로 비교.
- **숫자** [SI 인쇄 · 표 S1 · S2 · Feret 지름]:

  | 분율 | 부피 D10 / D50 / D90 (µm) | 수 D10 / D50 / D90 (µm) |
  |---|---|---|
  | <50 µm | 17 / 35 / 60 | 3 / 11 / 27 |
  | >50 µm | 89 / 138 / 240 | 9 / 17 / 98 |

  그림 S6 [판독]: LUMiSizer 10 · 50 · 90 · 99 % ≈ 1.2 · 8.8 · 80 · 137 µm ↔ SEM 계산 곡선 ≈ 1.3 · 2.8 · 4.8 · 6.2 µm.
- **⚠ 어긋남**: 그림 S6 의 SEM 곡선 (D50 ≈ 2.8 µm) 은 표 S1 (D50 35 µm) · 본문 Fig. 2c 주황 점선 (≈ 35 µm 에서 50 % [판독 `fig_2.png`]) 과 ≈ 12 배 다르다 — 원문 설명 없음 [미확인]. LUMiSizer D50 ≈ 8.8 µm 도 표 S1 의 Feret 부피 D50 35 µm 와 4 배 — Feret 은 최대 캘리퍼 지름이라 크게 나오는 쪽이지만 SI 는 이 차이를 논하지 않는다.
- **저자 한정**: *"The PSD, as shown in this work, is truncated at smaller particle sizes, as a consequence of the chosen image magnification. This effect is more pronounced for the >50 µm sample"* (S-7) · >50 µm 분율은 *"a greater number of particles below 50 µm"* 를 갖지만 부피는 50 µm 위가 지배 (S-22).
- **받치는 주장**: 본문 Fig. 2b–c · Fig. 6a 감마 맞춤 (a 1.944 · b 7.048) — 표 S2 와 감마 (a, b = 7.048 µm) 의 수 기준 중앙 11.4 µm 가 맞는다 [카드 산술 · §3].

#### S.2.4 입자 형상 — 그림 S7 · S8 · 표 S3 · S4 (S-10 – S-14)
- **무엇**: 2D 형상 서술자 (표 S4: AR = D_Feret/D_Breadth · circularity 4πA/p² · **solidity A/A_hull** · **convexity p_hull/p** · **sphericity R_min/R_max** · compactness √(4A/π)/D_Feret) 의 산점 + 주변 히스토그램.
- **숫자** [판독]: <50 µm (S7) — convexity · solidity 대부분 0.8–1.0 · sphericity 는 대부분 0.2–0.5 (색) · >50 µm (S8) — convexity 0.6 · solidity 0.5 까지 넓게 (S-12 인쇄 *"values as low as 0.6 for convexity and 0.5 for solidity"*) · 낮은 sphericity 입자가 더 많다.
- **해상도 인공물** (S-11): *"Feret diameter correlates negatively with convexity"* — 작은 입자는 픽셀이 거칠어 거칠기가 안 보여 convexity 가 높게 나온다 · solidity 는 덜 민감.
- **받치는 주장**: S-21 의 DEM 한계 문장 ("particles that are far from spherical … holes, jags, dips, and bulges") 의 근거 그림. ⚠ 그림 S8 캡션은 S7 과 같은 문장 (*"2D-representations of four particles are depicted as filled outlines"*) 인데 S8 에는 윤곽이 없다 [판독].

#### S.2.5 펠릿 치밀화 · Heckel in die / out of die · 회수 — 그림 S9 · S10 (S-15 – S-16)
- **무엇**: (a) Heckel 모식 — 영역 **I 입자 재배열 · II 입자 소성 변형 · III 압분체 탄성 변형 · IV 압분체 탄성 회복 (탈압)** · 주황 점선 = 선형 영역 (기울기 K) (b) 소성 = 격자면 미끄럼 (비가역) (c) 탄성 = 단위포 압축 (가역) (d) 두 분율의 **in die (채움 · 누르는 중) vs out of die (빈 원 · 각 압력으로 누른 뒤 10 MPa 적층압에서)**.
- **숫자** [판독 · `si_digitized.csv` · 상대밀도 분모 = 비중병 2.008 g/cm³]:

  | 압력 (GPa) | <50 µm in die | <50 µm out of die | >50 µm in die | >50 µm out of die |
  |---|---|---|---|---|
  | 0.3 | 81.5 % | (in die 와 겹침) | 79.5 % | (겹침) |
  | 0.5 | 86.2 % | 84.8 % | 83.4 % | (겹침) |
  | 1.0 | 92.6 % | 89.8 % | 88.7 % | 86.7 % |
  | 1.5 | 95.4 % | 92.2 % | 90.9 % | 88.4 % |
  | 1.7 | **96.5 %** | **92.8 %** | **91.7 %** | **89.0 %** |

  탈압 회복 (in − out, 1.7 GPa) = **3.7 %p (<50) · 2.7 %p (>50)** · 기공률로 3.5 → 7.2 % (×2.1) · 8.3 → 11.0 % (×1.3) [카드 산술].
  Heckel 기울기를 판독점으로 다시 맞추면 [판독 산술]: <50 µm in die P_y = 1/K ≈ **0.80 (0.5–1.0 GPa) · 0.94 (0.6–1.4) · 0.97 (1.0–1.7) GPa** — 본문 0.95(3) GPa 는 이 범위 안 · >50 µm in die ≈ 1.25 · 1.76 · 2.39 GPa (본문 1.65(3)) · out of die 는 기울기가 더 작다 (<50 µm ≈ 1.5 GPa · >50 µm ≈ 3–4 GPa — **본문 · SI 에 인쇄 안 된 값**, 구간에 따라 ±30 %).
- **회수 문단** (S-15 – S-16 · `txt_S15_S16_…`): *"Upon pressure release, the cracks, observed in S10, may be introduced, which could increase the tortuosity for ion conduction"* · 다이가 축 방향 팽창을 막아 벽에 응력이 남는다 · 밀어낼 때 벽 마찰 → *"most often the pellet broke into many pieces"* · 천천히 빼면 일부 해결 · 티오인산염 아닌 일부 SE 는 낮은 압력이 더 단단한 펠릿 (*"large elastic recovery … building up internal stress"*).
- **그림 S10** (깬 단면 · 윗면 · 윗면 가까운 단면 · 가운데 단면): 윗면에 금 (판 (b) 의 금 길이 ≈ 10–20 µm [판독]) · 윗면 근처 단면에 층상 금 · 가운데는 치밀 [판독] — **압력은 SI 캡션에 없다**.
- **두 항 모형** 원전 = Cooper–Eaton [S5] · Wünsch [S6] (재배열 + 고체 압축).
- **받치는 주장**: 본문 Fig. 2f 의 영역 분해 · Fig. 3 의 탈압 이력 · Fig. 5 의 0.01 ↔ 0.1 GPa 적층압 차이 (금 · 접촉).

#### S.2.6 Nyquist · EIS 방법 — 그림 S11 · S-24 – S-25
- **무엇**: (a) 0.01 · 0.05 · 0.1 GPa (kΩ 축) (b) 0.5 · 1.0 · 1.5 GPa (Ω 축) · 원 = <50 · 삼각 = >50 µm · 색 농도 = 압력.
- **숫자** [판독 · 대략]: 고주파 절편 (a) <50 µm ≈ 1.8 → 0.38 → 0.2 kΩ · >50 µm ≈ 0.83 → ≈ 0.2 → ≈ 0.1 kΩ (0.01 → 0.1 GPa) · (b) >50 µm ≈ 64 → 73 → 100 Ω · <50 µm ≈ 90 → 98 → 124 Ω (0.5 → 1.5 GPa — 화살표 방향이 (a) 와 반대) · 반원 없음 = 경사 스파이크만.
- **방법** [SI 인쇄]: 25 °C · 1 MHz – 100 Hz · V_RMS 10 mV · 100 Ω load-short 보정 · RelaxIS 3 · Kramers–Kronig 시험 · 비례 가중 · 대개 1 MHz – 1 kHz 맞춤 (압력에 따라 조정) · **등가 회로 = 저항 + CPE 직렬** · 오차 막대 = 두께 불확도 + 맞춤 오차의 전파.
- **받치는 주장**: 본문 Fig. 3 · 5 의 σ 값. ⚠ 입계 반원을 따로 맞추지 않았다 → σ 는 **총 이온 저항** — 본문의 입계 해석은 이 자료로 분리되지 않는다.

#### S.2.7 활성화 부피 유도 — 식 S1 – S7 (S-18 – S-19)
- **식** (크롭 `eq_S01` – `eq_S07`): σT = σ₀ e^(−ΔG/k_BT) (S1) · ΔG = k_BT(ln σ₀ − ln σ)_T,Ni (S2) · σ₀ = z n q² r² ν₀ / k_B (S3 · z 기하 인자 · n 운반자 밀도 · q 전하 · r 도약 거리 · ν₀ 시도 진동수) · ΔG = k_BT(ln r + ln ν₀ − ln σ) (S4 · z · n · q 압력 무관 가정) · ΔV ≡ (∂ΔG/∂p)_T,Ni (S5) · ΔV = k_BT[(∂ln σ₀/∂p) − (∂ln σ/∂p)] (S6) · 입방정 근사 ΔV = k_BT[β(γ − 2/3) − (∂ln σ/∂p)] (S7 · β 압축률 · γ Grüneisen · [S7–S10]).
- **⚠ 인쇄 그대로의 문제** [카드 판단]: S4 는 ln(r) 인데 S3 에는 r² 가 있다 → 2 ln r 이어야 하고 상수 ln(z n q²/k_B) 도 빠졌다 (상수는 압력 미분에서 사라짐 · 2 는 앞 항 보정의 크기를 바꾼다) · S2 는 S1 의 ln T 항을 적지 않았다 (등온 미분에선 무해).
- **받치는 주장**: 본문 Fig. 4c 의 ΔV 1.41(2) · 1.39(2) cm³/mol (그림 인쇄) — 본문은 앞 항 (σ₀ 의 압력 의존) 을 *"less than 10% of the second term"* 로 버린다 (본문 Fig. 4 캡션 · `figures.json` f4).

#### S.2.8 ³¹P MAS NMR — 그림 S12 (S-20)
- **무엇**: (a) 누르기 전 · 뒤 두 분율 스펙트럼 · 결정 (주황) / 비정질 곁상 (파랑) 맞춤 (Dmfit) (b) 94 · 73 ppm 선의 FWHM.
- **숫자**: 곁상 **8.2 → 9.7 wt% (<50) · 9.0 → 10.2 wt% (>50)** [SI 그림 인쇄] · FWHM [판독] 94 ppm 2.02 → 2.38 · 2.10 → 2.41 ppm · 73 ppm 1.82 → 2.17 · 1.91 → 2.22 ppm (+15–20 %) · 누르기 전에도 >50 µm 가 선폭 · 곁상이 조금 크다.
- **조건**: 9.4 T · 161.9 MHz · 4 mm ZrO₂ 회전자 (pyrex 삽입관 밀봉) · 10 kHz MAS · Bloch decay 512–4096 회 · 85 % H₃PO₄ 기준 · "after pressing" 의 압력은 **SI 캡션에 없다** (본문 값 1.7 GPa — 카드 §3 · 대조 못 함).
- **받치는 주장**: 본문의 "압력이 결정성을 일부 해친다 · 국소 무질서" — σ 에 대한 효과 크기는 **정량하지 않았다** [미확인].

#### S.2.9 DEM — 그림 S13 · S14 · 식 S8 – S14 · 표 S5 (S-21 · S-25 – S-28)
- **목적** (S-25 · `txt_S25_…`): *"we decided to employ DEM simulations to verify the hypothesis that powder compaction is indeed the dominant effect in this pressure regime"* (저압).
- **모형**: Cundall–Strack 강체 구 · 병진 (S8) · 회전 (S9) 운동량 · **법선 = 선형 스프링–대시포트 + 인력 차단** (S10, g_N = 중심거리 − 반지름 합) · d_N 을 반발 계수로 (S11) · **접선 = Coulomb 마찰 상한 + 접선 스프링–대시포트** (S12 · k_T = (1−ν)/(1−0.5ν) k_N · d_T = d_N) · 접선 틈 g_T = 적분 이력 변수 (S13 · *"not uniquely defined by the geometric configuration"*) · 접선 단위 벡터 (S14).
- **입력** (표 S5 · 이유 원문은 §4 정정 줄): ρ 1980 kg/m³ · ν 0.3 · **k_N 0.01 N/m** · c_COR 0.1 · μ 1.0 · g = (0, 0, 0) · 감마 a 1.944 · b "1.944" (오기로 보임 — §3).
- **카드 산술**: 감쇠비 ζ = abs(ln c)/√((ln c)² + π²) = **0.59** · k_T/k_N = **0.82** · 중력 압력 17.3 Pa 재계산 = 17.35 Pa ✓ · 1 GPa · 지름 13.7 µm (감마 평균) 에서 접촉력 ≈ 0.19 N 이면 k_N 0.01 N/m 의 겹침 ≈ 19 m → 힘 제어가 아니라 **두께 제어** [카드 추론].
- **결과 (그림 S13)** [판독]: 접촉면 합 0.08 (0.01 GPa) · 0.44 (0.05) · 0.70 (0.1) · 1.01 (0.2) · 1.19 (0.3) · 1.42 (0.5) · 1.70 (1.0) · **1.80 × 10⁶ µm²** (1.5 GPa) — 0.01 → 0.5 GPa 에 ×18 · 0.5 → 1.5 GPa 에 ×1.27. 9591 입자 (본문) 로 나누면 1.5 GPa 에서 입자당 ≈ 188 µm² ≈ 감마 구 평균 겉넓이 893 µm² 의 21 % [카드 산술 · 접촉면을 한 번 세는지 미기재].
- **저자의 한계 문장** (S-21 · `txt_S21_…`): *"In the DEM simulation the compaction of perfect spheres attributed with friction effects, form the pellet. The solid electrolyte powder, however, consists of particles that are far from spherical."* + 거칠기 → 마찰 증가 · 응집체 (깨려면 더 큰 응력) + *"surface roughness can introduce current constriction effects at the inter-particle contacts, especially, when the particles are not allowed to connect at low pressure"* + Fleig [S11]: 접점이 많을수록 협착 · 입계 저항이 작다 → *"At a higher compression stage, the number of contact surface increases, as shown in Figure S13."*
- **받치는 주장**: 본문 Fig. 6b — 정규화 σ 의 추세가 기하만으로 재현 (영역 II) · 저압 영역 I 과대평가의 원인 설명.
- **SI 에도 없음**: 압축 방식 (벽 변위 · 속도 · 단계) · 시간 간격 · 시드 수 · 계산 시간 · 접촉면의 정의 (한 번 / 두 번) · 탈압 계산.

#### S.2.10 FV 전달 — 식 S15 · S16 (S-29 – S-30)
- **방법** (`txt_S29_fv_voxel_1um_best_setup.png`): DEM 의 입자 위치 · 지름 → **복셀 1 µm** 구조 → BEST [S27, S28] 로 전해질 상 Poisson 식 · 정상 전류 j · U = 1 V → **σ_eff,i = l_i · j / U** (S15) → **σ_eff,max 로 정규화**.
- **활성화 부피** (`txt_S29_fv_normalization_activation_volume.png`): 압력 p_i (= 두께 l_i 에 대응) 마다 bulk σ_i = exp(ln σ_ref − ΔV/(k_B T) · (p_i − p_ref)) (S16) · *"due to the normalization of the simulated conductivities, the values in Figure 6b in the main text do not depend on the assumed bulk conductivity but only on the geometric properties of the pellet microstructure."*
- **계면** (`txt_S29_S30_…`): *"In the FV-simulations the electrolyte material was treated as a homogeneous phase without any additional grain boundary resistances between individual particles."*
- **카드 산술**: ΔV 1.4 cm³/mol · 298 K → ΔV/(k_B T) = **0.565 GPa⁻¹** → bulk σ 배율 0.945 (0.1 GPa) · 0.84 (0.3) · 0.76 (0.01 → 0.5) · **0.51 (0.5 → 1.7 GPa)**.
- **받치는 주장**: 본문 Fig. 6b 의 두 시나리오 (0.1 GPa 적층압 · 가변 압력). ⚠ SI 는 S16 의 출처를 *"equation (4) in main publication"* 이라 적는다 (카드 §6 의 본문 식 번호와 다름 · [미확인]).

#### S.2.11 DFT · AIMD — 그림 S15 – S18 (S-31 – S-35)
- **설정** [SI 인쇄]: VASP · PBE · PAW · k 간격 0.25 Å⁻¹ · 600 eV (탄성 900 eV) · 수렴 10⁻⁵ eV · 0.01 eV/Å · AIMD NVT · 499 eV · Γ 점 · 1 fs · Nosé–Hoover · MSD → tracer D · 2×2×1 초격자 (12 화학식) · supercell 프로그램으로 Si/P 자리 일곱 배치 (그림 S15 a–g) · Li 부분 점유 (Li2 · Li4 87.5 · 62.5 % · Li3 87.5 %).
- **숫자**: BVS 장벽 **0.22 eV (c 1D) · 0.28 eV (3D)** · AIMD **D_c ≈ 4 × D_a/b** (*"on average four times higher"*) · 장벽 **127(13) meV (c) · ≈155 meV (a/b · 그림 146(19) · 165(15)) · 136(13) meV (전체)** [SI 인쇄] · 500–900 K · 0–80 ps · 900 K 80 ps MSD 전체 ≈ 155 · z ≈ 95 Å² [판독] → D* ≈ 155/(6 × 80) ≈ 0.32 Å²/ps (그림 S18 의 900 K D* 와 같은 자릿수) [카드 산술].
- **저자 한정** (`txt_S33_…`): 단결정 LGPS 임피던스 [S38] 의 [001]/[110] 4 배와 맞는다 · *"The AIMD activation barriers are lower than measured barriers in other sulfide solid electrolytes and we attribute this discrepancy to the shortcomings of extracting activation barriers from AIMD simulations at high temperatures"* · *"the simulations represent the single crystal properties and do not consider grain boundiers or (amorphous) side phases."*
- **받치는 주장**: 본문 Fig. 4a (c 축 1D 통로) · 다결정 펠릿에서 결정 방위가 섞이면 입계 저항이 생긴다는 해석의 재료 쪽 근거. 격자를 줄인 (f 0.99 · 0.98) AIMD 설정은 SI 에 따로 없다 [미확인].

#### S.2.12 탄성 — 표 S6 · S7 (S-36 – S-37)
- **숫자** [SI 인쇄]: 표 S6 평균 강성 텐서 (네 구조 평균 · GPa) C11 38.5 · C22 41.7 · C33 40.5 · C12 26.4 · C13 13.5 · C23 15.4 · C44 11.4 · C55 9.6 · C66 17.8 (괄호 항 < 1 GPa) · 표 S7 t-Li₇SiPS₈ **B 23.5 (BM 22.8) · E 29.5 · G 11.4 GPa · ν 0.29 · G/B 0.49** · 비교 행 (다른 논문 값의 재인용): Li₁₀GeP₂S₁₂ 30.36 / 37.19 / 14.35 / 0.30 / 0.47 [S46] · 27.3 / 21.7 / 7.9 / 0.37 / 0.29 [S47] · Li₁₀SiP₂S₁₂ 27.8 / 24.8 / 9.2 / 0.35 / 0.33 · Li₁₀SnP₂S₁₂ 23.5 / 29.1 / 11.2 / 0.29 / 0.48 · **Li₆PS₅Cl 28.7 / 22.1 / 8.1 / 0.37 / 0.28** · Li₆PS₅Br 29.0 / 25.3 / 9.3 / 0.35 / 0.32 · Li₆PS₅I 29.9 / 30.0 / 11.3 / 0.33 / 0.38 ([S47]).
- **카드 산술**: 표 S6 의 C_ij 로 Voigt–Reuss–Hill 을 다시 내면 B_V 25.7 · B_R 25.3 → **B_H 25.5** · G_H 11.5 · E 29.9 GPa · ν 0.30 · G/B 0.45 — G · E 는 표 S7 과 맞고 **B 만 2 GPa (8 %) 다르다** (표 S7 의 B 23.5 · G 11.4 는 E 29.4 · ν 0.29 를 서로 맞게 낸다) · 원인 미기재 [미확인]. 같은 LGPS 의 E 가 문헌 사이에서 37.19 ↔ 21.7 GPa 로 갈린다 (표 S7 안).
- **우리 값과** [카드 대조]: 표 S7 의 Li₆PS₅Cl 행 (Deng 2016 [S47] 재인용) E 22.1 · ν 0.37 = Bazzoun 2026 DEM 입력과 같은 수 · 우리 DFT (CLAUDE.md: E_VRH 22.06 · B₀ 26.23 GPa · ν 0.360) 와 E 0.2 % · B −9 % [카드 산술].

#### S.2.13 아지로다이트 펠릿 밀도 메타 분석 — 그림 S19 (S-38 – S-39)
- **무엇**: Ohno 2020 실험실 간 연구 [S49] ESI 의 펠릿 상대밀도를 압력에 대해 — Li₆.₆P₀.₄Ge₀.₆PS₅I (인쇄 그대로) · **Li₆PS₅Cl** · Li₆PS₅Br₀.₇₅I₀.₂₅ · Li₆PS₅Br₀.₂₅I₀.₇₅ · Li₆PS₅I (다섯 조성 한 기호).
- **숫자**: *"pellet density fluctuates around an average value of about 85%, with outliers > 100% (nonphysical value) and < 70%"* [SI 인쇄] · 평균 ≈ **84.3 %** · ±1 SD 띠 ≈ **78.0 – 90.6 %** [판독] · 압력 ≈ 0.25 – 2 GPa.
- **저자 결론**: *"applied pelletizing pressure is not an appropriate descriptor of the achievable pellet density"* · 일부 재료는 σ 가 밀도와는 양의 경향, 압력과는 없음.
- **이어지는 문단** (`txt_S38_pugh_…`): *"Since the bulk (B) and elastic (E) modulus, as well as the G/B ratio of aryrodites, such as Li₆PS₅Cl, and the t-Li₇SiPS₈ prototype, Li₁₀GeP₂S₁₂, is comparable (see Table S7), we expect similar high pressure densification behavior of the two classes of materials. Both materials meet Pugh's criterion for a ductile material (B/G < 0.5), undergoing plastic deformation rather than fragmentation under stress."*
- **⚠** [카드 판단]: 표 S7 의 열은 **G/B** 다 (0.28 · 0.49 가 0.5 아래) — 인쇄된 "B/G < 0.5" 는 G/B 의 오기로 읽힌다 · t-Li₇SiPS₈ 의 0.49 는 그 문턱 바로 아래 · LPSCl 0.28 과 75 % 차이 — "comparable" 은 B · E 쪽 이야기이고 이 결론은 **기대** (측정 아님).
- **받치는 주장**: 본문의 "상대밀도는 약한 descriptor" 결론의 문헌 쪽 보조.

#### S.2.14 Methods — 합성 · 체 · SEM · 비중병 · 가변 압력 셀 (S-22 – S-25)
- **합성** (`txt_S22_…`): Li₂S (99.98 %) · 적린 (99 %) · 황 (승화) + 황 5 wt% 과잉 · 10 g · PM 200 · 50 mL ZrO₂ 단지 · 10 mm 볼 10 개 · 500 rpm 24 h (5 분 밀링 + 1 분 쉼) · 유리질 탄소 도가니 → 석영 앰플 진공 봉입 · 50 K/min 로 525 °C · 100 h · 노냉 · ⚠ **Si 원료가 목록에 없다** (인쇄 그대로 — 원문 누락으로 보임 [카드 판단]).
- **체**: 50 µm 체 + 와류 혼합기 진동 · 통과 = <50 µm · 남은 것 = >50 µm.
- **SEM**: Vega TS 5130 MM (Oxford X-MaxN 20) 또는 TESCAN VEGA4 LMU · 탄소 테이프 위에 흩뿌림.
- **비중병** (`txt_S23_…`): AccuPyc II 1340 · He · 10 회 퍼지 · 10 회 측정 · **2.008(6) g/cm³** (4 시료 평균 = 상대밀도의 분모) ↔ 결정학 **1.923(9)** [S15] · *"by 4.4 % larger … This difference is small and might originate from measurement and weighting uncertainties."*
- **가변 압력 셀** (`txt_S24_variable_pressure_cell.png`): CompreCell (rhd) · Al₂O₃ 원통 + 스테인리스 라이너 · **Ø6 mm 경질 금속 피스톤 = 전극** · **50 mg** · 이중 O-링 · CompreDrive 프레스 (힘 감시 · 능동 제어) · 모터 위치로 두께 · **시료 없는 기준 실행으로 장치 변형을 뺀다** · Julabo 항온.
- **받치는 주장**: 본문 Fig. 2d–f · 3 · 5 의 두께 · 밀도 · σ.

### S.3 SI 안에서 서로 맞지 않는 것 (원문 그대로 · 카드는 고치지 않는다)

| # | 자리 | 인쇄된 것 | 맞지 않는 상대 | 판단 [표지] |
|---|---|---|---|---|
| 1 | 표 S5 (S-28) | 감마 **b = 1.944** | 본문 Fig. 6a b = 7.048 · 표 S1 · S2 | 7.048 이 맞는 쪽 — 수 · 부피 D 들과 면적 질량 (0.7 %) 이 맞는다 [카드 산술] · 1.944 는 a 를 옮겨 적은 오기로 보인다 |
| 2 | 표 S5 · S-23 | DEM ρ **1980 kg/m³** ("four batches", 비중병 절 참조) | 비중병 절 **2.008(6) g/cm³** | 1.4 % 차 — DEM 정적 결과에는 거의 무관 (질량은 관성에만) [카드 판단] |
| 3 | S-38 | "Pugh's criterion … (**B/G** < 0.5)" | 표 S7 의 열 = **G/B** (0.28 – 0.49) | G/B 의 오기 [카드 판단] |
| 4 | 식 S4 (S-18) | ln(**r**) | 식 S3 의 **r²** | 2 ln r 이어야 한다 [카드 판단] |
| 5 | 표 S6 ↔ 표 S7 | B (VRH) **23.5 GPa** | 표 S6 C_ij 로 다시 낸 B_H **25.5** | 8 % 차 · G · E 는 맞음 [카드 산술] |
| 6 | 그림 S6 (S-8) | SEM 계산 부피 곡선 D50 ≈ **2.8 µm** [판독] | 표 S1 D50 **35 µm** · 본문 Fig. 2c | ≈ 12 배 — 원인 미기재 [미확인] |
| 7 | 그림 S8 캡션 (S-12) | "2D-representations of four particles" | 그림 S8 에 윤곽 없음 [판독] | 캡션을 S7 에서 복사한 것으로 보인다 |
| 8 | S-22 | 원료 Li₂S · 적린 · 황 | 생성물 t-Li₇**Si**PS₈ | Si 원료 누락 [카드 판단] |
| 9 | S-29 | S16 = *"equation (4) in main publication"* 의 단순식 | 카드 §6: 본문 eq 3 = 단순식 · eq 4 = V_m − V_f | 본문 PDF 없이 못 가림 [미확인] |
| (작음) | 표 S5 | "m_Smaple / A_Smaple" | — | 철자 (Sample) |

### S.4 이 묶음의 필수 네 항목 (CURATOR_BRIEF 5 번) — SI 로 채운 것

| 항목 | SI 의 답 | 위치 |
|---|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장 | *"the particles are described as rigid spheres"* · *"the compaction of perfect spheres attributed with friction effects … particles that are far from spherical"* · 거칠기 → 마찰 · 응집체 · 접점 전류 협착 | S-25 · S-21 |
| (ii) 소성 · 큰 변형을 넣기 어려운 이유와 우회 · 비용 | 소성 접촉 법칙을 **아예 안 넣었다** — 선형 탄성 겹침 + 실험 두께로 미세구조만 얻는 우회 · 비용 쪽 이유는 둘: k_N 을 *"for reasons of numerical efficiency"* 줄임 · c_COR 을 *"to save computational resources"* 0 이 아니게 · 계산 시간 · 비용 수치는 SI 에도 없음 | 표 S5 |
| (iii) 2D / 3D 와 전이 | DEM · FV = 3D (구 · 측방 주기 — 본문) · 형상 서술자 = **2D 영상** (*"Parameters describing the (2D) shape of a particle"*, S-10) · 2D 형상 → 3D 모형 전이에 대한 말 = **없음** (구로 대신했다) | S-10 · S-21 |
| (iv) 압력을 뺄 때 | 실험: out of die (10 MPa) Heckel · 탈압 회복 2.7–3.7 %p (1.7 GPa) [판독] · 탈압 때 금 → tortuosity 증가 가능 · 다이에서 빼다 깨짐 · 시뮬레이션: **탈압 계산 없음** | 그림 S9d · S-15 – S-16 · 그림 S10 |

### S.5 식 · 근거 글 크롭 목록 (그림 · 표 크롭은 §5 표)

| 크롭 | SI 쪽 | 한 줄 뜻 |
|---|---|---|
| `eq_S01_arrhenius_sigmaT.png` | S-18 | σT = σ₀ e^(−ΔG/k_BT) — Arrhenius 꼴 |
| `eq_S02_gibbs_from_sigma.png` | S-18 | ΔG 를 σ₀ · σ 로 (등온) |
| `eq_S03_prefactor_sigma0.png` | S-18 | σ₀ = z n q² r² ν₀ / k_B |
| `eq_S04_gibbs_jump_distance_attempt_freq.png` | S-18 | ΔG = k_BT(ln r + ln ν₀ − ln σ) (인쇄 ln r — §S.3 #4) |
| `eq_S05_activation_volume_definition.png` | S-19 | ΔV ≡ (∂ΔG/∂p)_T,Ni |
| `eq_S06_activation_volume_full.png` | S-19 | ΔV = k_BT[(∂ln σ₀/∂p) − (∂ln σ/∂p)] |
| `eq_S07_activation_volume_compressibility_gruneisen.png` | S-19 | 입방정 보정 β(γ − 2/3) |
| `eq_S08_dem_linear_momentum.png` | S-25 | 강체 구 병진 운동량 (중력 + 법선 + 접선 접촉력) |
| `eq_S09_dem_angular_momentum.png` | S-25 | 회전 운동량 (접선력의 모멘트) |
| `eq_S10_normal_spring_dashpot.png` | S-26 | 선형 스프링–대시포트 법선력 · 인력 차단 min(0, ·) |
| `eq_S11_normal_damping_from_cor.png` | S-26 | 반발 계수 → 법선 감쇠 d_N |
| `eq_S12_tangential_coulomb_friction.png` | S-27 | Coulomb 상한이 걸린 접선 스프링–대시포트 |
| `eq_S13_tangential_gap_rate.png` | S-27 | 접선 틈 속도 (적분 이력 변수) |
| `eq_S14_tangent_unit_vector.png` | S-27 | 접선 단위 벡터 |
| `eq_S15_fv_effective_conductivity.png` | S-29 | σ_eff = l · j / U (FV · U = 1 V) |
| `eq_S16_bulk_sigma_activation_volume_pressure.png` | S-29 | bulk σ 를 ΔV 로 압력에 따라 줄임 |
| `txt_S2_xrd_domain_size_not_feasible.png` | S-2 | XRD 로 결정자 크기 정량 불가 · <50 µm 가 조금 작다 |
| `txt_S15_S16_pellet_recovery_cracks_ejection.png` | S-15 – S-16 | 탈압 금 · 벽 응력 · 빼다 깨짐 |
| `txt_S21_dem_perfect_spheres_roughness_constriction.png` | S-21 | 저자의 DEM 한계 (완전 구 ↔ 거친 비구형) |
| `txt_S22_synthesis_sieving_fractions.png` | S-22 | 합성 · 체 (Si 원료 누락 그대로) |
| `txt_S23_gas_pycnometer_density_2008_vs_1923.png` | S-23 | 진밀도 2.008 vs 1.923 (+4.4 %) |
| `txt_S24_variable_pressure_cell.png` | S-24 | Ø6 mm · 50 mg · 두께 = 모터 위치 · 장치 변형 보정 |
| `txt_S24_S25_eis_conditions_fit_r_cpe.png` | S-24 – S-25 | EIS 조건 · 등가 회로 R + CPE |
| `txt_S25_dem_purpose_rigid_spheres.png` | S-25 | DEM 의 목적 · 강체 구 |
| `txt_S29_fv_voxel_1um_best_setup.png` | S-29 | 복셀 1 µm · BEST · U = 1 V |
| `txt_S29_fv_normalization_activation_volume.png` | S-29 | 정규화 · bulk σ 무관 · ΔV 반영 |
| `txt_S29_S30_fv_homogeneous_no_gb_resistance.png` | S-29 – S-30 | FV 계면 (입계) 저항 0 |
| `txt_S33_aimd_anisotropy_barriers_limits.png` | S-33 | AIMD 이방성 · 장벽 · 한계 |
| `txt_S38_metadata_density_not_pressure.png` | S-38 | 압력은 펠릿 밀도의 좋은 descriptor 가 아니다 |
| `txt_S38_pugh_ductile_similar_densification.png` | S-38 | 아지로다이트 · LGPS 비슷한 치밀화 기대 · Pugh |

### S.6 SI 까지 보고도 없는 것 [미확인]
- DEM 압축 방식 (벽 변위 · 속도 · 단계 · 정적 평형 판정) · 시간 간격 · 시드 수 · 계산 시간 · 탈압 계산.
- 복셀 1 µm 수렴 시험 · 겹침으로 생기는 고체 부피 차 (구 부피 합 ↔ 복셀 합집합) 를 어떻게 다뤘는지 · 접촉면 합의 정의.
- XRD FWHM · integral breadth 의 수치 · 격자를 줄인 AIMD (f 0.99 · 0.98) 의 설정.
- SI 캡션의 "after pressing" (그림 S12) · 그림 S10 의 압력 · out of die P_y 의 인쇄값.
- 그림 S6 SEM 곡선 ↔ 표 S1 차이의 이유 · 표 S5 b 오기의 정정 여부.
- LPSCl 의 활성화 부피 · LPSCl 펠릿 값 (이 논문은 t-Li₇SiPS₈ 만 쟀다 · 그림 S19 의 LPSCl 은 다른 조성과 기호가 같다).

## 세미나 준비 (랩 논문 세미나용 · 2026-11-18)

> 본문 숫자 = 이 카드 §3 · §5 의 본문 값 (2026-06-26 본문 정독 · **이번에 본문 PDF 로 다시 대조하지 않았다**) · SI 숫자 = §S (이번에 SI 로 대조).
> 크롭 = `litdb/figures/schneider2023_particle_size_pressure_transport/` 의 파일 이름. [판독] 값은 슬라이드에 "≈" 와 함께만 쓴다.

### (a) 한 줄 메시지 + 3 분 요약

**한 줄**: 황화물 SE 펠릿의 이온전도도는 압력에 대해 **두 기구가 반대로** 움직인다 — 낮은 압력 (≲ 0.5 GPa) 에선 입자 재배열 · 접촉이 σ 를 올리고, 높은 압력에선 격자 압축 (활성화 부피 ΔV ≈ 1.4 cm³/mol) 이 σ 를 내린다 — 그리고 같은 재료라도 **입경 분포가 상대밀도보다 σ 를 더 잘 가른다**.

**3 분 요약** (이 순서로 말한다):
1. 재료는 LGPS 형 정방정 황화물 **t-Li₇SiPS₈** 하나 (LPSCl 아님) · 체로 나눈 두 분율 (부피 D50 **35 µm** vs **138 µm** — SI 표 S1) 의 **단일상 SE 펠릿** (활물질 없음).
2. 0.01 → 1.7 GPa 로 누르며 두께 · EIS 를 잰다 (Ø6 mm · 50 mg · CompreCell — SI p.S-24). 작은 분율이 **더 치밀**한데 σ 는 **더 낮다** (압축 최대 4.1 vs 5.7 mS/cm @ ≈ 0.5 GPa · 본문).
3. 0.5 GPa 위에서 σ 가 떨어지는 것은 미세구조가 아니라 격자다 — 탈압 가지의 ln σ–p 기울기로 ΔV **1.41(2) · 1.39(2) cm³/mol** (두 분율 같음 · 본문 Fig. 4c 인쇄) · AIMD 도 압축하면 확산이 준다.
4. Heckel 해석 (in die) 으로 P_y **0.95 vs 1.65 GPa** (본문) · SI 그림 S9d 는 **누른 뒤 10 MPa (out of die)** 값을 함께 준다 — 1.7 GPa 에서 상대밀도가 3.7 · 2.7 %p 돌아온다 [판독].
5. 강체 구 DEM (선형 스프링 · Coulomb 마찰 · k_N 0.01 N/m — SI 표 S5) 으로 **실험 두께에서의 미세구조**를 만들고, 복셀 FV (1 µm · 계면 저항 0) 로 σ 를 풀어 **정규화 σ–p 추세** 를 재현한다. 저압에선 시뮬레이션이 높다 — 저자 설명은 완전 구 ↔ 거친 비구형 입자 (SI p.S-21).
6. 우리에게: (i) σ 가 압력에 대해 **가역 · 비가역 두 몫**으로 갈린다는 틀 (ii) **in die / out of die 표지** 의 필요 (iii) DEM–FV 사슬의 한계 (두께를 실험에서 받음 · 계면 항 0) 가 우리 접촉망 (Holm) · MPM (형상 소성) 이 채우는 칸이다. 절대값은 옮기지 않는다.

### (b) 발표 흐름 (16 장 · 15–18 분)

| # | 장 (분) | 쓸 크롭 | 말할 것 | 꼭 말할 숫자 (원문 위치) |
|---|---|---|---|---|
| 1 | 제목 · 질문 (0.5) | — | 압력과 입경이 펠릿 σ 를 어떻게 바꾸나 · 실험 + DEM/FV + AIMD 세 축 | — |
| 2 | 배경: 압력 하의 σ (1) | `fig_1.png` | 분체 (빈 기호) 는 누르면 σ 가 급히 오른 뒤 포화 · 압분 펠릿 (채움) 은 ln σ 가 압력에 선형으로 준다 → 두 기구 가설 | σ/σ₀ 축 (여러 재료 · 정규화 — 본문 Fig. 1) |
| 3 | 재료 · 두 체 분율 (1.5) | `fig_2.png` (a–c) · `tab_S1.png` · `tab_S2.png` · `fig_S5.png` (f) | t-Li₇SiPS₈ 유리–세라믹 · 50 µm 체 · 통과 / 남은 것 · 큰 분율도 **수** 로는 50 µm 아래가 많다 | 부피 D50 35 · 138 µm · 수 D50 11 · 17 µm (SI 표 S1 · S2) · 곁상 8.2–9.0 wt% (그림 S12) |
| 4 | 입자 형상 (1) | `fig_S3.png` · `fig_S7.png` | SEM → ImageJ 분수령 → 형상 서술자 · 구가 아니다 (sphericity 낮음) · 작은 입자 convexity 는 해상도 인공물 | solidity · convexity 대부분 0.8–1 · sphericity ≈ 0.2–0.5 [판독 S7] · 3475 · 5118 입자 (SI) |
| 5 | 압밀 곡선 · Heckel (1.5) | `fig_2.png` (d–f) | 두께 · 상대밀도 · ln(1/(1−ρ)) · 영역 I (재배열) → II (소성 · 선형) | P_y 0.95(3) · 1.65(3) GPa (in die · 본문) · 고압 ρ_rel 90–95 % (본문) |
| 6 | 누른 채 ↔ 뺀 뒤 (1.5) | `fig_S9.png` · `txt_S15_S16_pellet_recovery_cracks_ejection.png` | out of die = 각 압력으로 누른 뒤 **10 MPa** · 탈압하면 밀도가 돌아오고 금이 생길 수 있다 · 다이에서 빼다 깨짐 | 1.7 GPa: 96.5 → 92.8 % (<50) · 91.7 → 89.0 % (>50) [판독 S9d] |
| 7 | σ(p) 1 차 사이클 (1.5) | `fig_3.png` · `fig_S11.png` | 압축 가지: 저압 급상승 → ≈ 0.5 GPa 최대 → 고압 감소 · 탈압 가지가 더 높다 · Nyquist 에 반원 없음 = 총 저항 하나 | 0.3 / 0.7 → 4.1 / 5.7 mS/cm (압축) · 탈압 최대 5.3 / 6.6 (본문) · 회로 R + CPE (SI p.S-25) |
| 8 | 활성화 부피 (1.5) | `fig_4.png` · `eq_S05_…` · `eq_S07_…` · `eq_S16_…` | 탈압 가지의 기울기 → ΔV · 앞 항 (σ₀ 의 압력 의존) 은 작다고 버림 · AIMD 격자 축소 → 확산 감소 | ΔV 1.41(2) · 1.39(2) cm³/mol (본문 Fig. 4c 인쇄) · AIMD 1.7–2.0 (본문) · bulk σ × exp(−0.565 p[GPa]) [카드 산술 · 식 S16] |
| 9 | 적층압 분리 (1) | `fig_5.png` | 같은 누름 이력을 0.01 · 0.1 GPa 적층압에서 따로 잰다 — 0.1 GPa 가 높고 포화가 빠르다 · 뺀 뒤의 접촉 · 금 | 숫자는 그림 축으로만 (본문 Fig. 5) |
| 10 | 결정 이방성 (1) | `fig_S17.png` · `fig_S18.png` · `txt_S33_aimd_anisotropy_barriers_limits.png` | c 축 1D 통로 · 다결정 펠릿에서 방위가 섞인다 → 저자의 입계 해석 | D_c ≈ 4 × D_a/b · AIMD 127(13) / ≈155 / 136(13) meV · BVS 0.22 / 0.28 eV (SI p.S-33) |
| 11 | DEM 모형 (1.5) | `fig_S14.png` · `eq_S10_…` · `eq_S12_…` · `tab_S5.png` · `txt_S25_dem_purpose_rigid_spheres.png` | 강체 구 · 선형 스프링–대시포트 + Coulomb · 소성 없음 · 강성을 일부러 낮게 — 반력은 안 쓴다 | k_N 0.01 N/m · μ 1.0 · c_COR 0.1 · ν 0.3 · g 0 (SI 표 S5) · 9591 입자 · 210 × 210 × 1700 µm³ (본문) |
| 12 | DEM → FV 결과 (1.5) | `fig_S13.png` · `fig_6.png` · `eq_S15_…` · `txt_S29_S30_fv_homogeneous_no_gb_resistance.png` | 접촉면은 저압에서 급증 후 포화 · 복셀 1 µm FV · 계면 저항 0 · σ_eff,max 로 정규화 → 추세 재현 · 저압 과대평가 | 접촉면 0.08 → 1.80 × 10⁶ µm² (0.01 → 1.5 GPa) [판독 S13] |
| 13 | 저자가 적은 DEM 한계 (0.5) | `txt_S21_dem_perfect_spheres_roughness_constriction.png` | 원문 한 문단을 그대로 띄운다 | — |
| 14 | 구조 손상 (1) | `fig_S12.png` · `fig_S10.png` | 누르면 비정질 곁상 · 선폭이 는다 · 표면 근처 금 — σ 영향은 정량하지 않았다 | 8.2 → 9.7 · 9.0 → 10.2 wt% (그림 S12 인쇄) |
| 15 | 아지로다이트로 옮길 수 있나 (1) | `tab_S7.png` · `fig_S19.png` · `txt_S38_pugh_ductile_similar_densification.png` | 저자는 B · E · G/B 가 비슷하니 "비슷한 치밀화를 기대" · Ohno 메타 자료에선 압력이 밀도를 못 가른다 | LPSCl G/B 0.28 vs t-Li₇SiPS₈ 0.49 · 메타 평균 ≈ 84 % (SI 글 "about 85%") |
| 16 | 정리 · 우리 일 (1) | — | (f) 의 세 줄 + (e) 의 한계 두 줄 | — |

### (c) 그림마다 읽는 법

| 그림 | 축 · 기호 | 볼 곳 | 함정 |
|---|---|---|---|
| 본문 Fig. 1 (`fig_1.png`) | 압력 (MPa · 2000 에서 축 끊김) · σ/σ₀ (로그) · 빈 기호 = 분체 · 채움 = 압분체 | 분체의 급상승–포화 ↔ 펠릿의 단조 감소 | 재료마다 σ₀ (최저 압력 값) 가 다르다 — 정규화라 절대값 비교 불가 · 문헌 자료 모음 |
| Fig. 2 d–f (`fig_2.png`) | (d) 두께 µm (e) ρ_rel % (f) ln(1/(1−ρ_rel)) + 오른쪽 ρ_rel 눈금 · 채움 = 압축 · 빈 원 = 탈압 (IV) · 회색 띠 = 영역 I | (f) 의 선형 구간 기울기 K = 1/P_y · 탈압 가지가 위에 남는 것 (비가역) | (f) 의 빈 원은 **누른 채 압력을 내리는 중** (in die 탈압) — SI S9d 의 빈 원 (out of die · 10 MPa) 과 다른 양 |
| Fig. 3 (`fig_3.png`) | 압력 GPa · σ mS/cm (로그) · 주황 <50 · 파랑 >50 · 채움 압축 · 빈 원 탈압 | 압축 최대의 위치 (≈ 0.5 GPa) · 탈압 가지가 압축보다 높음 · 맨 끝 0.01 GPa 탈압 값 | 1 차 사이클만 — 반복 사이클 값은 Fig. 4c 의 평균 · 막대 |
| Fig. 4c (`fig_4.png`) | 압력 · ln(σ / S cm⁻¹) · 두 분율 · 기울기 삼각형 | 0.5 GPa 위의 직선 기울기가 두 분율에서 같다 (ΔV 1.41 · 1.39) | 탈압 가지 3 · 2 회 평균 · ΔV 는 σ₀ 의 압력 의존을 버린 단순식 (SI 식 S7 의 앞 항 생략) |
| Fig. 5 (`fig_5.png`) | 누른 압력 (가로) · 그 뒤 잰 σ (로그) · 빈 원 0.01 GPa · 채움 0.1 GPa 적층압 | 0.1 GPa 적층압 값이 일찍 포화 · 0.01 GPa 값은 누른 압력과 함께 계속 오른다 | 가로축은 측정 압력이 아니다 (누른 이력) |
| Fig. 6b (`fig_6.png`) | 압력 · σ/σ_0.5GPa (로그) · 원 = 실험 · 삼각 = DEM/FVA (▼ = 가변 압력 = 시나리오 II · ▲ = 0.1 GPa 적층압 = 시나리오 I) | 영역 II 에서 삼각이 원에 붙는다 · 영역 I 저압에서 삼각이 위 | DEM/FVA 의 압력 축 = **실험 두께에 맞춘 이름** (DEM 힘 아님 · SI 표 S5 · p.S-29) · 정규화 — 절대 σ 비교 아님 |
| 그림 S6 (`fig_S6.png`) | 입경 µm (로그) · 누적 부피 % · 주황 LUMiSizer · 파랑 SEM | 두 방법의 D50 | 파랑 곡선이 표 S1 과 ≈ 12 배 어긋남 (§S.3 #6) — 이 그림을 PSD 근거로 쓰지 않는다 |
| 그림 S7 · S8 (`fig_S7.png` · `fig_S8.png`) | 가로 solidity · 세로 convexity · 색 = sphericity (a) / Feret µm (b) · 주변 히스토그램 | 1 근처에 몰린 점 · S8 의 넓은 퍼짐 | 2D 투영 · 작은 입자 convexity 과대 (해상도) · S8 캡션의 '윤곽 넷' 은 그림에 없다 |
| 그림 S9d (`fig_S9.png`) | 압력 GPa · ln(1/(1−ρ_rel)) + ρ_rel 점선 (70–98 %) · 채움 in die · 빈 원 out of die | 1 GPa 위에서 채움과 빈 원이 벌어지는 폭 = 탄성 회복 | out of die = 0 MPa 가 아니라 10 MPa · 상대밀도 분모 = 비중병 2.008 (결정학 1.923 이면 +4.4 %) |
| 그림 S11 (`fig_S11.png`) | Z′ · −Z″ (a) kΩ (b) Ω · 원 <50 · 삼각 >50 · 농도 = 압력 | 고주파 절편 (= 저항) 의 이동 방향 — (a) 왼쪽 · (b) 오른쪽 | 반원이 없다 — 입계 저항을 따로 못 본다 · 절편은 두께가 다른 펠릿의 값 |
| 그림 S12 (`fig_S12.png`) | ³¹P 화학 이동 ppm · 주황 결정 · 파랑 곁상 · (b) FWHM 막대 | 87 ppm 근처 파랑의 키 · 선폭 증가 | "after pressing" 의 압력이 캡션에 없다 · wt% 는 맞춤 결과 |
| 그림 S13 (`fig_S13.png`) | 압력 GPa · 접촉면 10⁶ µm² · DEM | 0.3 GPa 아래의 급증 · 1 GPa 위 포화 | 압력 = 실험 두께 대응 · 접촉면 정의 (한 번 / 두 번) 미기재 · 9591 개 구 상자 하나 |
| 그림 S16 – S18 (`fig_S16.png` – `fig_S18.png`) | MSD Å² · 시간 ps · 방향 x y z · Arrhenius 1/T · D* | z 가 x · y 의 ≈ 4 배 · 기울기 삼각형의 meV | 500–900 K 외삽 · 단결정 · 12 화학식 초격자 |
| 그림 S19 (`fig_S19.png`) | 압력 GPa · 상대밀도 % · 위 · 오른쪽 히스토그램 · 점선 평균 · 띠 ±1 SD | 압력과 밀도 사이 경향 없음 | 다섯 조성 · 여러 실험실이 한 기호 — LPSCl 만 못 뽑는다 · >100 % 점 (비물리) 포함 |

### (d) 예상 질문과 답 (12)

1. **작은 입자가 더 치밀한데 왜 σ 가 낮나?** — 저자 해석은 입자 · 입계가 많고 결정 방위가 불리하다는 것 (본문 · AIMD 이방성 D_c ≈ 4 × D_a/b · SI p.S-33). 그러나 **입계 저항을 따로 재지는 않았다**: EIS 회로가 R + CPE 하나 (SI p.S-25) · 그림 S11 에 반원이 없다 · FV 는 계면 저항 0 (p.S-29–S-30) · XRD 는 "조금 작다" 까지 (p.S-2). → "잰 것은 σ 차이, 기전은 해석" 으로 답한다.
2. **DEM 의 압력은 진짜 힘인가?** — 아니다. k_N 을 0.01 N/m 로 줄였고 *"we are not interested in the resulting global reaction force"* (표 S5) · *"For each pressure level p_i corresponding to a certain pellet thickness"* (p.S-29) · 본문 Fig. 6b 캡션도 같은 말. 0.01 N/m 로 힘을 걸면 겹침이 수 m 가 된다 [카드 산술] → 실험 두께에 맞춰 누른 기하로 읽힌다.
3. **왜 저압에서 시뮬레이션이 높은가?** — 저자 (p.S-21): 완전 구 ↔ 거친 비구형 입자 · 거칠기가 마찰과 응집체를 키우고 저압에서 접점 전류 협착을 만든다. 우리 해석을 더하면 FV 가 계면 저항 0 인 가지라 협착 · 입계 항이 빠진 만큼 높게 나오는 방향이다 [카드 해석].
4. **ΔV 1.4 cm³/mol 은 얼마나 큰가?** — 25 °C 에서 bulk σ × exp(−0.565 × Δp[GPa]) [카드 산술 · 식 S16]: 0.1 GPa 에서 −5.5 % · 0.3 GPa 에서 −16 % · 0.5 → 1.7 GPa 에서 절반. 가역이라 누른 뒤 낮은 압력에서 재면 거의 사라진다.
5. **in die 와 out of die 는 무엇이 다른가?** — in die = 누르는 압력에서 잰 두께 · out of die = 그 압력으로 누른 뒤 10 MPa 적층압에서 잰 두께 (S9 캡션). 1.7 GPa 에서 3.7 · 2.7 %p 차이 [판독] = 압분체 탄성 회복 (영역 IV).
6. **탈압 가지의 σ 가 왜 압축 가지보다 높나?** — 치밀해진 미세구조는 남고 (비가역 소성 · 본문) 격자 압축은 풀린다 (가역 ΔV). 맨 끝 0.01 GPa 에서 다시 떨어지는 것은 접촉 · 금 쪽 (SI p.S-15: 탈압 금이 tortuosity 를 키울 수 있다) — 정량 분리는 논문에 없음.
7. **곁상 (비정질) 증가가 σ 에 영향을 주나?** — 늘어난 양 (8.2 → 9.7 · 9.0 → 10.2 wt%) 과 선폭 증가는 보였지만 σ 에 대한 몫은 **논문에 없음**.
8. **P_y 0.95 GPa 와 우리 DEM 138 MPa 는 왜 다른가?** — 재료 · 압력대 (그들 GPa 영역의 영역 II · 우리 ≤ 300 MPa) · 모형 (그들 실험 in die · 우리 DEM 순수 SE 4 압력) 이 다 다르다. 게다가 P_y 는 맞춤 구간에 따라 0.80 – 0.97 GPa 로 움직인다 (그림 S9d 판독 산술). 같은 식 이름일 뿐 같은 양으로 비교하지 않는다.
9. **이 결과를 LPSCl 에 옮길 수 있나?** — 추세 (두 기구 · 입경 > 밀도 · 탈압 회복) 는 같은 황화물 냉간 압밀이라 질문으로 옮길 수 있다. 숫자는 못 옮긴다 — σ · ΔV · P_y · 진밀도 모두 재료 고유. 저자도 LPSCl 쪽은 "기대" 로만 썼다 (p.S-38 · G/B 0.28 vs 0.49).
10. **진밀도 2.008 과 1.923 의 4.4 % 는 중요한가?** — 상대밀도를 ×1.044 바꾼다 — 95 % 가 99 % 가 되고 ln(1/(1−ρ)) 는 1 에 가까울수록 민감하다 [카드 산술]. 저자는 "small" 이라 했지만 영역 III 해석에는 작지 않다.
11. **DEM 상자는 실험을 얼마나 닮았나?** — 9591 개 구 · 210 × 210 µm² 측방 주기 (본문) · 감마 (1.944, 7.048 µm) 구의 부피 합으로 면적당 질량이 실험 (50 mg / Ø6 mm) 과 0.7 % 안에서 맞는다 [카드 산술] · 측방 길이는 실험 지름의 ≈ 1/29 [카드 산술: 210 µm / 6 mm] · 복셀 1 µm 는 D10 3 µm 입자를 3 복셀로 그린다.
12. **AIMD 장벽이 왜 측정 (0.27 eV) 보다 낮나?** — 저자: 고온 AIMD 에서 장벽을 뽑는 한계 [S42] · 단결정 · 입계 · 곁상 없음 (p.S-33). 이방성 (4 배) 은 LGPS 단결정 임피던스 [S38] 와 맞는다.

### (e) 한계 · 비판할 점

**저자 스스로 적은 한계 (원문)**
- *"In the DEM simulation the compaction of perfect spheres attributed with friction effects, form the pellet. The solid electrolyte powder, however, consists of particles that are far from spherical."* (SI p.S-21)
- *"In the FV-simulations the electrolyte material was treated as a homogeneous phase without any additional grain boundary resistances between individual particles."* (SI p.S-29 – S-30)
- *"we are not interested in the resulting global reaction force, but only in the resulting particle morphology"* (표 S5 · k_N)
- *"Since we do not have further information on that we used a value from the middle of the range."* (표 S5 · μ)
- *"Although, a precise domain size determination by XRD is not feasible"* (p.S-2)
- *"The PSD, as shown in this work, is truncated at smaller particle sizes, as a consequence of the chosen image magnification."* (p.S-7)
- *"the simulations represent the single crystal properties and do not consider grain boundiers or (amorphous) side phases."* (p.S-33)
- *"Upon pressure release, the cracks, observed in S10, may be introduced, which could increase the tortuosity for ion conduction."* (p.S-15)

**우리가 짚을 점** [카드 판단]
1. **DEM 이 압밀을 예측하지 않는다** — 두께를 실험에서 받으니 DEM/FV 일치는 "이 두께에서의 기하 → σ 추세" 검증이지 "압력 → 기하" 검증이 아니다. 강체 구 · 탄성 겹침만 있고 소성 접촉 법칙도 없다.
2. **입계 기전이 분리되지 않았다** — R + CPE 하나 · FV 계면 0 · XRD 정성 — 크기 효과의 기전은 해석이다.
3. **크기 축이 두 점** (체 분율 둘) · 재료 하나 · 1 차 사이클 위주 — 크기 의존의 꼴 (함수) 은 알 수 없다.
4. **SI 안의 어긋남 아홉** (§S.3) — b 오기 · ρ · Pugh · 식 S4 · B 값 · 그림 S6 · 캡션 · Si 원료 · 식 번호.
5. **겹친 구 → 복셀** — 복셀 고체는 합집합이라 구 부피 합 (실험 상대밀도의 짝) 과 겹침만큼 다른데 그 처리가 없다 · 복셀 1 µm 수렴 시험도 없다 — 저압 (작은 겹침) 의 접촉 넓이 · 연결이 복셀 크기에 민감할 수 있다.
6. **ΔV 를 균일 bulk 감소로만** 넣었다 (식 S16) — 응력이 입자마다 다른 것은 무시 · σ₀ 의 압력 의존도 버렸다.
7. **진밀도 기준** (2.008 vs 1.923, 4.4 %) 이 영역 III 의 상대밀도를 크게 흔드는데 "small" 로 넘겼다.
8. **메타 자료 (그림 S19)** 는 다섯 조성 · 여러 실험실을 한 기호로 섞었다 — LPSCl 결론을 끌어낼 수 없다.

### (f) 우리 일과의 연결

> 우리 쪽 값 = CLAUDE.md 프레임 문장 (DEM E_eff 1.35 GPa · Heckel P_y 138 MPa · MPM E 1.53 · σ_y 0.30 · ν 0.49 · 랩 표준 순수 SE 기공률 10–13 % · 진밀도 1.64) — `litdb/our_dem_baseline.md` 는 이 브랜치에서 자리표시다.

| 우리 축 | 이 논문이 주는 것 | 못 주는 것 · 주의 |
|---|---|---|
| **Ⓐ DEM 신뢰성 — 언로딩** | 황화물 SE 펠릿의 탈압 회복 크기 감각 (1.7 GPa 에서 2.7–3.7 %p [판독 S9d]) · "가압 중 / 뺀 뒤 (10 MPa)" 를 **같은 장치**에서 잰 꼴 · 탈압 금 · 다이에서 빼다 깨짐 (p.S-15) | 0.3 GPa 에선 두 값이 마커 크기 안 — 우리 300 MPa 근처의 회복 크기는 이 그림으로 못 가른다 · t-Li₇SiPS₈ · 단일상 · DEM 탈압 계산은 없다 |
| **Ⓑ DEM → MPM 연계 (형상 소성)** | 강체 구 DEM 이 저압에서 실험보다 높게 나오는 사례 + 원인 문장 (p.S-21) = 우리 MPM 형상 소성이 채울 칸의 외부 근거 · 형상 서술자 정의표 (표 S4) 와 영상 절차 (그림 S2 · S3) 는 우리 SEM 단면 정량에 그대로 | 그들 DEM 은 두께를 받는다 — 우리 DEM 처럼 압력 → 기공을 내는 모형과 성격이 다르다 · 형상 값은 2D |
| **전달 (접촉망 · 복셀 FV)** | FV = 계면 저항 0 · 균질상 (p.S-29 – S-30) — 우리 복셀 FV (STEP3) 와 같은 CONTACT_FREE 가지 (원장 `CL-81`) · 그 가지가 저압에서 과대평가한다는 실험 대조 한 건 | 정규화 σ 만 — 절대 σ 대조 없음 · 우리 접촉망 (Holm 협착) 과 직접 견줄 수치 없음 |
| **Heckel · 압밀** | 같은 식 · P_y 가 맞춤 구간에 따라 움직인다 (<50 µm 0.80–0.97 · >50 µm 1.25–2.39 GPa [판독 산술 S9d]) — 우리 P_y 를 인용할 때 구간 · in die / out of die 표지 · 영역 I–IV 정의 (그림 S9a) | 압력대 · 재료가 다르다 — P_y 절대 대조 금지 |
| **랩 표준과 나란히** | t-Li₇SiPS₈ 0.3 GPa ≈ 기공 18.5 · 20.5 % [판독 · 진밀도 2.008] · Ohno 아지로다이트 메타 평균 ≈ 84 % (±6 %p) | 랩 표준 (순수 SE 10–13 % · 1.64) 과 **다른 문헌 값** — 판정 · 맞춤에 안 쓴다 · 진밀도 기준을 같이 적는다 |
| **압력 의존 bulk σ** | ΔV 로 σ 가 가역적으로 준다는 틀 · 식 S16 의 꼴 | LPSCl ΔV 없음 · 우리 σ 모형은 압력 의존 bulk σ 를 안 넣는다 — 누른 채 잰 실험 σ 와 견줄 때만 문제 |
| **탄성 (DFT)** | 표 S7 의 LPSCl 행 (Deng 2016 재인용) E 22.1 · ν 0.37 — 우리 DFT E_VRH 22.06 · ν 0.360 와 같은 자릿수 | 2 차 인용 · B 는 28.7 vs 우리 26.23 |
| **입경 축** | 체 분율 둘의 PSD (표 S1 · S2) · 감마 맞춤 | 수십 µm ↔ 우리 SE ≈ 1 µm — 크기 효과 숫자 전이 금지 · `Cronau(r_SE)` 근거로 쓰지 않는다 (원장 `SELF-51`) |

### (g) 발표에서 쓰지 말 말

| 하지 않을 말 | 이유 · 대신 |
|---|---|
| "작은 입자는 입계 저항 때문에 σ 가 낮다 (보였다)" | 입계 저항을 따로 재지 않았다 → "작은 분율의 σ 가 낮다 · 저자는 입계 · 방위로 해석" |
| "DEM 이 압밀 거동을 재현 · 예측했다" | 두께를 실험에서 받았다 → "실험 두께에서 만든 구 배열로 정규화 σ 추세를 재현" |
| "DEM/FV 가 실험과 일치한다" (한정어 없이) | 정규화 · 영역 II 한정 · 저압은 과대평가 |
| "0.5 GPa 가 황화물 SE 의 최적 압력" · "LPSCl 도 ≈ 0.5 GPa 에서 최대" | t-Li₇SiPS₈ 한 재료 · 측정 압력에 따른 값 |
| "ΔV 효과는 무시할 수 있다" | 측정 압력에 달렸다 (0.3 GPa 에서 −16 % [카드 산술]) |
| "Pugh 기준으로 연성 → 소성 변형이 지배한다 (증명)" | 저자의 기대 · 인쇄된 기준식도 G/B 를 B/G 로 오기 · 0.49 는 문턱 바로 아래 |
| "가장 · 최초 · 완벽" | 최상급 금지 (보고자료 원칙) |
| out of die P_y (≈ 1.5 · 3–4 GPa) 를 논문 값처럼 | 본문 · SI 에 인쇄 안 된 판독 산술 — 쓰려면 [판독] 표지 |
| 그림 S19 로 "LPSCl 펠릿은 ≈ 85 %" | 다섯 조성 · 여러 실험실이 섞인 값 |
| 그림 S6 의 SEM 곡선을 PSD 근거로 | 표 S1 과 ≈ 12 배 어긋남 (§S.3 #6) |

## 고친 것 (11-18 SI)

> 옛 문장은 지우지 않고 그 자리에 ⛔ 표지를 달았다. 근거 = SI 46 쪽 (§S) · 판독값 = `si_digitized.csv`.

1. **§3 이온 이동 장벽 행** — "bond-valence + AIMD" → 0.22 · 0.28 eV 는 **BVS 만** · AIMD 는 127(13) / ≈155 / 136(13) meV (SI p.S-33 · 그림 S18).
2. **§3 PSD >50 µm 행 · §5 Fig. 2 행 · §10** — "D50(vol) = 89 µm" → SI 표 S1 **D10 89 · D50 138 · D90 240 µm** (본문 Fig. 2c 파란 점선도 ≈ 130–140 µm 에서 50 % [판독]) — 본문 글은 대조 못 함.
3. **§3 감마 행** — 값 (b = 7.048) 은 그대로 · SI 표 S5 의 b = 1.944 인쇄를 오기로 표지 (표 S1 · S2 · 면적 질량으로 7.048 확인 [카드 산술]).
4. **§3 E · σ_y · ν 행** — "n/a · DEM 은 c_cor·k_N 으로 캘리브" → DFT B 23.5 · E 29.5 · G 11.4 GPa · ν 0.29 (표 S7) · DEM ν 0.3 · k_N 0.01 N/m (반력 안 씀 · 보정 없음) · σ_y = SI 에도 없음.
5. **§4 DEM 접촉 법칙** — "SI 참조 · rigid-sphere + overlap 계열로 추정" → 확인: 강체 구 · 선형 스프링–대시포트 · Coulomb (식 S8 – S14) · 소성 · 점착 없음 · "c_cor(접촉보정)" → **반발 계수**.
6. **§4 재료 파라미터** — "밀도 ρ, 마찰 μ 등은 실험 매칭으로 튜닝" → 튜닝 없음 (ρ = 배치 평균 · μ = 문헌 범위 가운데 · 표 S5).
7. **§5 SI 인용 블록** — "S17 = AIMD 이방성" → S16 – S18 · "S10 · S12 = 1.7 GPa" 는 SI 캡션에 없음 · S10 "균열 수십 µm" 는 SI 글에 수치 없음 (판 (b) 금 ≈ 10–20 µm [판독]).
8. **§6 영역 분류** — III = "공극 소멸" → SI 정의 **III 압분체 탄성 변형 · IV 압분체 탄성 회복** · out of die = 10 MPa 에서 잰 값.
9. **§A-1 · §B-2 · §8 ②** — "GB 기전을 같은 황화물에서 실험으로 보여줌 · Cronau(r_SE) 의 두 번째 부호 근거" → 입계 저항은 따로 재지 않았다 (EIS R + CPE · FV 계면 0 · XRD 정성) · `Cronau(r_SE)` = 출처 없는 모델 가정 (원장 `SELF-51`).
10. **§A-2** — "우리 작동범위 (300 MPa) 에서 ΔV 무시 가능" → 누른 채 재면 0.3 GPa 에서 bulk σ −16 % [카드 산술 · 식 S16] · 가역 · LPSCl ΔV 없음.
11. **§7** — SI 행 넷 (접촉 법칙 · 탈압 · σ 읽기 가지 · 랩 표준) + 지위 표지 ("pure-SE ~90 % @300 MPa" = 우리 MPM 보정 값 · `CL-94` / Cronau(r_SE) = `SELF-51`).
12. **§8 ③** — "PSD 의존 Heckel 을 우리 DEM 과" → 그들 DEM 은 P_y 를 못 낸다 · 실험 P_y 와만 · 맞춤 구간 표지.

**고치지 못하고 남긴 것** (본문 PDF 가 이번에 없었다): §A-1 첫 줄 "Fig 3, 3.8 vs 5.7 mS/cm" 와 §3 "4.1 / 5.7" 의 차이 · §6 본문 식 번호 (eq 3 = 단순식) 와 SI p.S-29 의 *"equation (4) in main publication"* 의 차이 — 둘 다 [미확인].

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

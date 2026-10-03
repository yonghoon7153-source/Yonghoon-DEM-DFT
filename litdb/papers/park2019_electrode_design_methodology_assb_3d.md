<!-- 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · τ 묶음 형식 기준 = tjaden2018 · landesfeind2016 · taufactor 카드.
     이 논문은 실험이 없는 설계 방법론 시뮬레이션이다 (GeoDict 복셀 구조 → 구조 기술자 → COMSOL P2D).
     §4 = 3 단계 흐름 정독 · §7 뒤 "§ τ 정의 대조 — 우리 규약 매핑" · §8-1 = 이번 묶음이 닫으려는 항목.
     쪽 표기 = 학술지 인쇄 쪽: PDF n 쪽 = 인쇄 (123 + n) 쪽, p.124–129.  SI 에는 쪽 번호가 인쇄돼 있지 않다 → "SI p.n" = SI PDF n 쪽 (전 9 쪽).
     표 · 그림 번호 = 원문 번호.  본문에 번호 붙은 식은 없다 — 식은 SI Fig. S4 · S5 그림 안 글자를 그대로 옮겼다.
     수식 · 표 · 그림은 PDF 를 렌더해서 읽었다 (텍스트층이 마이너스 기호를 깨뜨린다 — 맨 아래 원문 대조 기록).
     값 표지: stated = 본문 · 캡션 · 표 원문 / 판독 = 그림에서 읽은 값 (TREND 전용) / (우리 산술) = 원문 수치로 계산 / (추론) / [미확인]. -->
# 전고체 전극 설계 방법론 — GeoDict 복셀 3D 구조 (GrainGeo) → 접촉면적 (PoroDict) · 유효전도도 · MacMullin 수 N_m = τ/ε (ConductoDict FVM) → COMSOL P2D 성능 예측 (흑연 NG + 산화물 LSTP 음극 · 실험 없음) — Park (Energy Storage Mater. 2019)

> slug `park2019_electrode_design_methodology_assb_3d` · DOI `10.1016/j.ensm.2019.03.012` · type `sim (GeoDict voxel microstructure → ConductoDict FVM · MacMullin N_m = τ/ε tortuosity → COMSOL P2D) — NG/LSTP 산화물 ASSB 음극 · 실험 없음` · PDF `4. Electrode design methodology for all-solid-state batteries 3D structural analysis and performance prediction.pdf` · digested `2026-10-03` · status ✅
>
> ★ **이 카드의 역할 = Park 디지털 트윈 계보의 τ 관례 원형.**  같은 그룹 (DGIST Y. M. Lee) 의 `park2020_digitaltwin_assb_foundational` (Adv. Energy Mater. 2020) 이 SI Fig S9 (Ohm 식 · 6 면 Dirichlet) 캡션과 Table S2 각주 b 에서 이 논문을 **[12a]** 로 인용한다.
> - **τ 정의**: *"the MacMullin number (N_m = τ/ε) [13,14]"* (p.124 — [13] Thorat 2009 · [14] Landesfeind 2016) + 균질화 Ohm 식 **j = (σ/N_m)∇φ** (SI p.3 Fig. S4) ⇒ **N_m = σ₀/σ_eff = 우리 1/f** · 원문 τ = ε·N_m = **우리 tau2** (tortuosity factor 자리 · 원문 이름은 "tortuosity" 뿐, "factor" 0 회).
> - **τ 수치는 하나도 없다** — 보고되는 것은 N_m (LSTP 47 · 178 · 28,556 @ 40 · 30 · 20 wt%, stated · NG 는 그림만) 과 σ_eff 뿐.
> - **σ₀ = Table S3 문헌 입력값** (LSTP 이온 9.9×10⁻⁴ S cm⁻¹ [31, 32] · NG 전자 2.5 S cm⁻¹ [30]) — 조성 무관 상수 · 저자 측정 아님.
> - ⚠ **재료계가 다르다**: 흑연 (NG, 평균 14 µm) + 산화물 LSTP (Li₂O–SiO₂–TiO₂–P₂O₅, 250–500 nm) **음극** — LPSCl · NCM 이 아니다.  압밀 물리 없음 (확률 배치 + *"열처리로 1D·2D 접촉이 생긴다"* 가정, p.125).  **실험 검증 없음** (p.128).
> - ⚠ **원문 내부 불일치 (우리 산술)**: 전자상은 N_m × σ_eff = 2.50 S cm⁻¹ = Table S3 σ₀ 로 정확히 맞는데, 이온상은 N_m × σ_eff (본문) = 7.94–7.97×10⁻⁴ S cm⁻¹ 로 Table S3 의 **0.80 배**다.  40 wt% σ_eff,ion 은 본문 · Table S4 1.69×10⁻⁵ 인데 SI 그림 (Fig. S3 평균 · Fig. S7d) 은 ≈1.94–1.95×10⁻⁵ 다 (§ τ 정의 대조 (4)).
> - ⇒ 이 원문이 **닫는 것**: Park 계보의 τ 산출 경로 (복셀 FVM 해 → σ_eff → N_m 역산 · 6 면 Dirichlet).  **못 닫는 것**: park2020 의 τ 원값 · LPSCl/NCM σ₀ 출처 (이 원문에 없다) → 메모 v2 §3-4 의 "T_Park ∝ 가정 σ₀ · 추세 전용" 한정어는 **그대로** (§8-1).
>
> 출처 PDF = `litdb/inbox/` 의 위 파일 (본문 6 쪽) + SI `4. Sup) Electrode design methodology for all-solid-state batteries 3D structural analysis and performance prediction.pdf` (9 쪽) — **둘 다 끝까지 읽음**.

---

## 0. 결론 먼저 (이번 묶음이 물은 것 → 답)

| # | 질문 | 답 | 근거 |
|---|---|---|---|
| ① | 미세구조 생성 도구 · 모듈 | **GeoDict GrainGeo** (voxel array formation) — 그림 워터마크 "GeoDict 2018".  NG = Gaussian 타원체 볼록다면체 (등방 배향) → LSTP 구 (250–500 nm 균일) 를 overlap mode **isolation distance −0.1 µm** 로 추가 → SBR/CMC 바인더를 "Added binder" 기능으로 입자 사이에 바름 | p.125–126 · SI p.1 Table S2 |
| ② | τ 를 어떻게 계산하나 (방정식 · 경계조건) | **τ 를 따로 계산하지 않는다.**  ConductoDict (유한체적법) 에 상별 고유 σ (Table S3) 를 넣고 마주 보는 면에 φ = 1 / φ = 0 (x · y · z) Dirichlet 을 걸어 σ_eff 를 풀고, 그 결과를 균질화 Ohm 식 j = (σ/N_m)∇φ 의 **N_m** 으로 적는다.  τ 는 정의 (N_m = τ/ε) 로만 나온다 | p.124 · p.126 · SI p.3 Fig. S4 |
| ③ | 어느 상 | 이온 = **LSTP 상** (NG · 바인더 이온 σ = 0) · 전자 = **NG 상** (LSTP 1×10⁻¹⁵ · 바인더 0).  기공 σ 는 표에 없음 (0 으로 읽힘 [미확인]) | SI p.3 Table S3 |
| ④ | 정규화 | ε = **전극 전체 부피** 대비 상 부피분율 (Table S1 vol% = Table S4 ε_e · ε_s, 기공 ≈ 30 % · 바인더 포함) · 단면 = 도메인 전체 면 (추론: Dirichlet 이 도메인 면에 걸리고 σ_eff 가 P2D 의 겉보기 σ_eff 로 들어간다) · **보고값의 방향 미기술** | SI p.1 · p.3 · p.4 · p.5 |
| ⑤ | 보고된 τ 값 | **없음.**  N_m 만: LSTP **47 · 178 · 28,556** (40 · 30 · 20 %; 10 % 는 결과 없음 "No Results Calculated") · NG ≈ 12.2 · 7.45 · 4.95 · 3.8 (40 · 30 · 20 · 10 %, 판독) | p.127 · p.126 Fig. 2c · p.127 Fig. 3h |
| ⑥ | σ_eff | 이온 **1.69×10⁻⁵ · 4.48×10⁻⁶ S cm⁻¹** (40 · 30 %, 본문 · Table S4) · Fig. S3 평균 1.95×10⁻⁵ (60:40, SD 1.66×10⁻⁷) · 1.81×10⁻⁸ (80:20, SD 9.61×10⁻⁹).  전자 **0.205 · 0.335 S cm⁻¹** (Table S4) · ≈0.505 · ≈0.655 (20 · 10 %, 판독 Fig. S7d) | p.127 · SI p.2 · p.5 · p.6 |
| ⑦ | σ₀ 규약 | **Table S3 문헌 입력값, 조성 무관**: LSTP 이온 9.9×10⁻⁴ [31, 32] · NG 전자 2.5 [30] S cm⁻¹.  저자 측정 아님.  ⚠ 이온 N_m 은 이 σ₀ 로 재현되지 않는다 (× 0.80, 머리말) | SI p.3 · (우리 산술) |
| ⑧ | 조성 · 입경 · 두께 · 바인더 | NG:LSTP = 60:40 · 70:30 · 80:20 · 90:10 wt% (바인더 5 wt%, SBR:CMC 1:1) · NG 평균 지름 14 µm (Gaussian 축지름 15 · 10 · 10 µm, SD 5) · LSTP 250–500 nm · 두께 46 · 43 · 37 · 33 µm · 설계 기공 30 % · 1.2 mAh cm⁻² · **NCM 없음** | p.125 · SI p.1 |
| ⑨ | 메모 v2 §3-4 한정어가 좁혀지나 | **아니다 — 그대로 둔다.**  park2020 의 σ₀ (NCM 8.5×10⁻⁴ · LPSCl 조성식) 도 τ 원값도 이 원문에 없다.  같은 계보 선행에서도 σ₀ 는 문헌 입력이고 이온 N_m 이 자기 σ₀ 로 재현되지 않는다 → 한정어의 근거가 하나 늘었다.  좁혀지는 것은 **산출 경로 (역산) 하나뿐** | §8-1 |

## 1. 한 줄 요약
GeoDict 의 GrainGeo 로 흑연 (NG) · 산화물 고체전해질 (LSTP) · 바인더 복셀 전극을 그리고, PoroDict 로 NG–LSTP 비접촉면적을,
ConductoDict (유한체적법) 로 상별 유효전도도와 MacMullin 수 (N_m = σ₀/σ_eff = τ/ε) 를 뽑아 **COMSOL P2D 반쪽셀 모델에 그대로 넣어**
율특성 · SOC · 과전압을 예측하는 "구조 → 구조 기술자 → 성능" 3 단계 설계 방법론 (실험 없음).  LSTP 30 → 20 wt% 에서 이온 N_m 이
**178 → 28,556** 으로 뛰어 이온 경로가 끊기고 (10 % 는 계산 결과 없음), 40 % 와 30 % 사이에서 충전 용량 · SOC · 과전압이 갈린다.
우리에게 가치는 **Park 디지털 트윈 (2020) 의 τ 관례 · 경계조건 · 산출 경로의 원형**을 원문으로 주는 것이고, 수치는 재료
(NG/LSTP 음극) · 해상도 (LSTP 지름 2.5–5 voxel) · 내부 불일치 때문에 옮기지 않는다.

## 2. 메타

| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **Joonam Park** (1저자) · Dohwan Kim · Williams A. Appiah · Jihun Song · Kyung Taek Bae · Kang Taek Lee (DGIST 에너지공학) · Jimin Oh · Ju Young Kim · Young-Gi Lee (ETRI) · **Myung-Hyun Ryou** (한밭대, 교신) · **Yong Min Lee** (DGIST, 교신 · yongmin.lee@dgist.ac.kr) | **Energy Storage Materials 19 (2019) 124–129** | **10.1016/j.ensm.2019.03.012** | 음극 = 천연흑연 NG + LSTP (Li₂O–SiO₂–TiO₂–P₂O₅ 산화물 SE) + SBR/CMC · 반쪽셀 상대극 = Li 금속, 분리막 = LPS (Li₂S–P₂S₅) | **시뮬레이션** (GeoDict 복셀 구조 + COMSOL P2D) — 실험 없음 |

- 접수 2019-01-20 · 수정본 2019-03-02 · 게재 승인 2019-03-14 · 온라인 2019-03-19 (p.124).  © 2019 Elsevier — OA 문구 없음.
- 연구비: NRF 기후변화대응기술개발 (NRF-2017M1A2A2044493) · DGIST R&D (19-01-HRHR-02) · DGIST 슈퍼컴퓨팅 · 빅데이터센터 (p.128).
- 소프트웨어: GEODICT® (Math2Market, Germany — 그림 워터마크 "GeoDict 2018") · COMSOL Multiphysics 5.3a, Batteries & Fuel Cells 모듈 (p.125–126).
- 본문 결론의 자기 한정: *"Although the reliability is not confirmed by experimental data, we believe that this modeling and simulation approach is quite meaningful"* (p.128).
- 같은 그룹 후속 = `park2020_digitaltwin_assb_foundational` (NCM711 + LPSCl + NBR, 실험 대조 있음).  같은 [12] 의 b) = Park 2020 Chem. Eng. J. 391, 123528 (같은 inbox 5 번 파일 — 이 카드 범위 밖).

## 3. 핵심 수치

### 3-A. 설계 조성 — Table S1 (SI p.1, stated) + 두께 (p.125)

| LSTP ratio in NG+LSTP (wt%) | 40 | 30 | 20 | 10 |
|---|---|---|---|---|
| NG / LSTP / 바인더 (wt%) | 57.0 / 38.0 / 5.0 | 66.5 / 28.5 / 5.0 | 76.0 / 19.0 / 5.0 | 85.5 / 9.5 / 5.0 |
| NG (vol%) | 39.70 | 46.03 | 52.31 | 58.03 |
| LSTP (vol%) | 23.70 | 17.66 | 11.71 | 5.77 |
| 바인더 (vol%) | 5.85 | 5.81 | 5.78 | 5.70 |
| 기공 = 100 − 합 (우리 산술) | 30.75 | 30.50 | 30.20 | 30.50 |
| SE/고체 vol (우리 산술) | 34.2 % | 25.4 % | 16.8 % | 8.3 % |
| 두께 (본문 · voxel 수) | 46 µm (460) | 43 µm (430) | 37 µm (370) | 33 µm (330) |
| NG 부피 = vol% × 50 × 50 µm² × 두께 (우리 산술) | 45,655 µm³ | 49,482 µm³ | 48,387 µm³ | 47,875 µm³ |

- 진밀도: NG 2.1 · LSTP 2.345 · 바인더 1.25 g cm⁻³ (Table S1).  두께는 *"to maintain the same areal capacity and porosity"* 로 조성마다 바꿨다 (p.125) — NG 부피가 조성 간 ±4 % 안이라 (우리 산술) 정합.
- 면적 용량 1.2 mAh cm⁻² (흑연 300 mAh g⁻¹ 기준) · 설계 기공 30 % (p.125).

### 3-B. 구조 생성 파라미터 (stated)

| 항목 | 값 | 쪽 |
|---|---|---|
| voxel | **0.1 µm** — *"which should be approximately a third of the smallest LSTP particle"* | p.125 |
| 도메인 | 50 × 50 µm (500 × 500 voxel) × 두께 (3-A) | p.125 |
| NG 형상 | *"ellipsoid convex polyhedra, under the Gaussian with isotropic orientation condition"* · 축지름 x 평균 15 (SD 5 · bound 5) · y 10 (SD 5 · bound 7.5) · z 10 (SD 5 · bound 5) µm · "Random Points: 30" (의미 미기술) | p.125 · SI p.1 Table S2 |
| NG 크기 (본문 · P2D) | avg. diameter 14 µm · P2D 입자 반경 R_s = 7.0 µm | p.125 · SI p.5 |
| LSTP | 구 · 지름 250–500 nm 균일 ("Uniformly in interval") | p.126 |
| NG–LSTP 겹침 | overlap mode · isolation distance **−0.1 µm** → NG 에 겹친 부피 < 0.35 % 를 LSTP 부피로 재배정 | p.126 |
| 바인더 | SBR/CMC 를 "Added binder" 기능으로 *"plastered with the interspace between particles"* [27] | p.126 |
| 접촉 가정 | *"we assumed that 1D or 2D contacts in the ASSEs could be formed by the heat treatment process"* | p.125 |
| GeoDict 재료 ID (Fig. 2a 범례) | 00 Air (invis.) · 01 Graphite · 02 LSTP · 03 SBR1CMC1 [Binder] | p.126 |
| 해상도 (우리 산술) | LSTP 지름 = **2.5–5 voxel** · r_SE/r_AM = 0.125–0.25 / 7 = **0.018–0.036** | — |

### 3-C. 고유 σ (= σ₀) — Table S3 (SI p.3, stated)

| 재료 | 전자 σ (S cm⁻¹) | 이온 σ (S cm⁻¹) |
|---|---|---|
| 천연흑연 NG | 2.5 [30] | 0 |
| 바인더 (SBR:CMC) | 0 | 0 |
| LSTP | 1×10⁻¹⁵ [31, 32] | **9.9×10⁻⁴** [31, 32] |

- [30] = He · Habte · Jiang, Solid State Ionics 296 (2016) — 제목상 **LBM 예측 (시뮬레이션) 논문**이 NG σ₀ 의 인용원이다 (2.5 의 원 출처는 [미확인]).  [31] = Goharian 외, Ceram. Int. 41 (2015) (LSTP 유리세라믹) · [32] = Li 외, Russ. J. Electrochem. 43 (2007).  값이 그 원문에 있는지 · 어떤 시료 (펠릿 · 유리세라믹 · 온도) 인지 **[미확인]**.
- 기공 (Air) 은 표에 없다 → 0 으로 읽힌다 [미확인].
- 조성마다 같은 값 (park2020 의 LPSCl σ₀ 는 조성식이었다 — §8-1).

### 3-D. 구조 해석 결과

| 양 | 40 % | 30 % | 20 % | 10 % | 쪽 | 표지 |
|---|---|---|---|---|---|---|
| N_m, LSTP 상 (이온) | **47** | **178** | **28,556** | 결과 없음 | p.127 (Fig. 2c) | stated · 그림 위치는 20 % 점 ≈ 2.6×10⁴ (판독) |
| N_m, NG 상 (전자) | ≈12.2 | ≈7.45 | ≈4.95 | ≈3.8 | p.126 Fig. 2c | 판독 |
| σ_eff,ion (S cm⁻¹) | **1.69×10⁻⁵** | **4.48×10⁻⁶** | *"close to zero"* | 0 | p.127 · SI p.5 Table S4 | stated |
| σ_eff,ion — SI 그림 | ≈1.94×10⁻⁵ (S7d) · 평균 1.95×10⁻⁵, SD 1.66×10⁻⁷ (S3) | ≈4.6×10⁻⁶ (S7d) | 평균 1.81×10⁻⁸, SD 9.61×10⁻⁹ (S3) | 0 (S7d) | SI p.2 · p.6 | S3 = 그림 안 stated 주석 · S7d = 판독 |
| σ_eff,e (S cm⁻¹) | **0.205** | **0.335** | ≈0.505 | ≈0.655 | Table S4 · Fig. S7d | stated (40 · 30) / 판독 |
| NG–LSTP 접촉면적 A_c (m²) | ≈5.5×10⁻⁹ | ≈4.45×10⁻⁹ | ≈3.0×10⁻⁹ | ≈1.5×10⁻⁹ | p.126 Fig. 2b | 판독 |
| 비접촉면적 a_s (m⁻¹) | **47,892** | **41,485** | ≈32,500 | ≈18,000 | p.127 · Table S4 · Fig. 2b | stated (40 · 30) / 판독 |
| a_s — 도메인 5 개 평균 | 48,035 (SD 937) | — | 31,779 (SD 452) | — | SI p.2 Fig. S3 | 그림 안 stated 주석 |

- 본문 서술 (stated): LSTP 10 → 40 % 에서 접촉면적 **×4**, 비접촉면적 **×3** (p.126–127) · 같은 전극을 LSTP 없이 액체 전해질로 적시면 활성 면적 **244,286 m⁻¹ = LSTP 40 % 의 5 배** (p.127) · LSTP 40 % 의 N_m 47 은 액체계의 **≈20 배** (p.127 — 액체 N_M ≈ 47/20 ≈ 2.4, 우리 산술 · 원문은 배수만) · *"LSTP 20% or less cannot form ion conductive channels within ASSEs"* (p.127) · 10 % 는 *"no 3D structural results are obtained, probably due to a too deficient or discontinuous solid electrolyte phase"* (p.127).

### 3-E. P2D 결과 (COMSOL, 25 °C)

| 충전 용량 (mAh cm⁻²) | 0.05C | 0.1C | 0.2C | 0.5C | 쪽 |
|---|---|---|---|---|---|
| LSTP 40 % | 1.233 | 0.993 | 0.775 | 0.2953 | p.127 (Fig. 4a) |
| LSTP 30 % | 1.038 | 0.761 | 0.429 | 0.189 | p.127 (Fig. 4b) |

- 방전: LSTP 40 % 는 모든 율에서 설계 용량 1.2 mAh cm⁻² 에 닿고 전압 평탄부만 오른다 (p.127 · Fig. S8a).  LSTP 30 % 는 ≈1.0 mAh cm⁻² 에서 끝난다 (판독 Fig. S8b).  *"the intercalation of lithium ion into graphite is more difficult than the de-intercalation process, which supports its reliability"* (p.127).
- 0.1C 충전 끝 평균 SOC: **≈58 %** (40 %) vs **≈40 %** (30 %) (p.127).  계면 쪽 SOC 가 늘 높다 — *"the effective lithium ion conductivity is not sufficiently high to achieve the reaction rate of 0.1C"* (p.127).
- 0.1C 충전 끝 계면 최대 과전압: **≈ −20 mV** (40 %) vs **≈ −40 mV** (30 %) (p.128).  그림은 ≈ −17 · ≈ −39 mV (판독 Fig. 4e,f).
- 0.1C 방전 계면 과전압 (판독 Fig. S8e,f): 40 % ≈ 10 · 14 · 23 · 29 mV (10k · 20k · 30k · 35k s) · 30 % ≈ 30 · 57 · 95 mV (10k · 20k · 30k s).
- 30 % 가 나쁜 원인 = 유효 이온 σ 감소 1.69×10⁻⁵ → 4.48×10⁻⁶ S cm⁻¹ (p.127) · *"the enhancement of the effective electric conductivity does not seem critical under this mild operating condition"* (p.127).

### 3-F. P2D 매개변수 — Table S4 (SI p.5, stated · 각주 a = 설계 · 실험 설정 · b = COMSOL 라이브러리 · c = 문헌 [36–41])

| 매개변수 | 값 | 각주 |
|---|---|---|
| L_n (음극 두께) | 46×10⁻⁶ or 43×10⁻⁶ m | a |
| L_e (LPS 분리막) | 1400×10⁻⁶ m | a |
| R_s | 7.0×10⁻⁶ m | a |
| D_s | 1.45×10⁻¹³ m² s⁻¹ | b |
| D_e,LSTP | 4.0×10⁻¹⁶ m² s⁻¹ | c |
| D_e,LPS | 4.58×10⁻¹² m² s⁻¹ | c |
| k | 2.0×10⁻¹¹ m s⁻¹ | b |
| i_0 | 10 A m⁻² | c |
| σ_s | 0.205 or 0.335 S cm⁻¹ | a |
| σ_e,LSTP | 1.69×10⁻⁵ or 4.48×10⁻⁶ S cm⁻¹ | a |
| σ_e,LPS | 1.81×10⁻³ S cm⁻¹ | a |
| ε_s | 0.397 or 0.46 | a |
| ε_e | 0.237 or 0.177 | a |
| a_s | 47892 or 41485 (표에 단위 없음 · nomenclature m⁻¹) | a |
| c_s,max | 31507 mol m⁻³ | b |
| c⁰_e,LSTP | 15045 mol m⁻³ | a |
| c⁰_e,LPS | 16322 mol m⁻³ | a |
| t₊ | 0.99 | c |
| A | 1.131×10⁻⁴ m² | a |
| I | 10 A m⁻² | a |
| T | 298.15 K | a |
| E_eq | 0.2033 + 0.6613 exp(−68.63 soc) − 0.006943 tanh((soc − 0.4895)/0.0854) − 0.0925 tanh((soc − 0.0317)/0.053) − 0.075 tanh((soc − 0.5692)/0.875) + 0.02675 tanh(−(soc − 0.1814)/0.03031) | c |

- "or" 앞 = LSTP 40 %, 뒤 = 30 % (L_n 46/43 µm 가 3-A 두께와 같다).
- ⚠ σ_s · σ_e,LSTP 칸 이름에 "eff" 가 없지만 **값은 3D 유효값**이다 (Fig. S7d · 본문 p.127 과 같은 수) — P2D 식 (Fig. S5) 은 σ_s,eff · σ_e,eff 로 쓴다.
- (우리 산술) A = 1.131 cm² = 지름 12 mm 원판 · LPS 분리막 1.4 mm ÷ 1.81 mS cm⁻¹ = 77 Ω cm² (0.1C = 0.12 mA cm⁻² 에서 IR 9.3 mV) · 1.2 mAh cm⁻² 의 1C = 12 A m⁻² → Table S4 의 I = 10 A m⁻² 는 ≈0.83C 로, C-rate 스윕 (0.05–0.5C) 과 어떻게 이어지는지 **원문 미기술**.

## 4. 방법 ★ — 3 단계 흐름 (구조 → 구조 기술자 → P2D)

### 4-1. 1 단계 — 3D 구조 (GeoDict GrainGeo, p.125–126)
1. 도메인 50 × 50 µm × 두께 (조성별), voxel 0.1 µm.
2. NG 를 먼저 무작위로 채운다 — Gaussian 축지름 (Table S2) 의 타원체 볼록다면체, 등방 배향.
3. 같은 도메인에 LSTP 구 (250–500 nm 균일) 를 overlap mode · isolation distance −0.1 µm 로 추가 — *"which allows LSTP particles to be located around NG and leads to real contact between the NG and LSTP particles while minimizing the deformation of NG particles"*.  NG 와 겹친 < 0.35 % 부피는 LSTP 로 재배정.
4. "Added binder" 로 SBR/CMC 를 입자 사이 공간에 바른다 [27].
5. 각 상 부피 = Table S1 (진밀도로 wt% → vol%).
- **원문에 없는 것**: LSTP–LSTP 겹침 규칙 · 부피분율 목표 오차 · 실현 (seed) 반복 수 — 반복은 도메인 크기 변형 (§4-6) 뿐이다 [미확인].  같은 GeoDict 를 쓴 Bielefeld 2019 (이 논문 ref [26] · 정본 카드 `bielefeld2019_microstructural_modeling_composite_cathode`) 는 전이영역에서 조성당 **10 실현**을 평균했다.

### 4-2. 2 단계 (a) — 접촉면적 (PoroDict [28], p.125–126)
- 정의: *"the real specific contact area (a_s = A_c/V_a) [15,16], which is defined as the contact area (A_c) between the active material and solid electrolyte divided by the bulk volume (V_a) of the active materials"* (p.125) · *"obtained by dividing the calculated contact area by the occupied volume of NG"* (p.126).  ⇒ **분모 = 활물질 (NG) 부피** (전극 부피 아님).
- 정의의 인용원 [15] (Hansen · Anderko 1958, 금속학 총서 p.51) · [16] (Tiggelaar 2009, 다공 실리콘 LC 칩) 은 배터리 문헌이 아니다.  면적 계산 알고리즘 (Minkowski 측도 등) 미기술 [미확인].
- ⚠ (우리 산술) Fig. 2b 의 두 축은 이 정의와 Table S1 부피로 **서로 재현되지 않는다**: A_c/V_NG = 1.2×10⁵ m⁻¹ (40 %) vs 보고 a_s 47,892 · 10 → 40 % 증가비 A_c 3.7 배 vs a_s 2.7 배 (NG 부피는 조성 간 ±4 % 로 거의 일정, 3-A).  어느 축이 맞는지 판정 불가.

### 4-3. 2 단계 (b) — 전도 해석 (ConductoDict [29–32], 유한체적법)
**원문 전사 (SI p.3 Fig. S4 — 그림 안 글자 그대로)**:
- 도메인: `Domain: j = (σ/N_m)∇φ` (부호 없음).
- 경계: `φ|₊ₓ = 1` · `φ|₋ₓ = 0` · `φ|₊ᵧ = 1` · `φ|₋ᵧ = 0` · `φ|₊z = 1` · `φ|₋z = 0` (정육면체 6 면, 단위 없음).
- 캡션: *"Domain with governing equations and its boundary conditions (Ohm's Law)."*
- 본문 (p.126): *"The electric and ionic conduction pathways in their 3D microstructure are simulated using the ConductoDict module (based on the finite volume method) in GEODICT® (Fig. S4 and Table S3) [29–32]."*
- 입력 = Table S3 상별 σ.  출력 = *"effective electric and ionic conductivities"* (p.127) · *"MacMullin numbers of NG and LSTP structures"* (Fig. 2c 캡션).
- 본문 p.127: *"These 3D structural properties can simply be expressed using the effective electric and ionic conductivities by combining each conductivity value with the morphological connectivity."*

**읽기**:
- Fig. S4 의 식은 복셀 단위 지배식 (∇·(σ(x)∇φ) = 0) 이 아니라 **균질화된 유효 Ohm 식**이다 — 그 식이 N_m 을 σ/σ_eff 로 **조작적으로 정의**한다.  복셀 단위 식은 원문에 적혀 있지 않다 (추론: 상별 σ 를 단 복셀 FVM).
- 6 면에 값이 한꺼번에 적혀 있다 — 방향 전도도를 정의하려면 방향별 3 회 계산이어야 한다 (추론).  각 회의 측면 경계 (주기 · 대칭 · 절연) · 보고값의 방향 · 솔버 이름 · 수렴 기준은 **미기술** ("periodic" · "symmetric" 0 회).  park2020 은 같은 꼴의 그림 (Fig S9) 에 EJ 솔버를 명시했다.
- 전위차 단위: 그림은 무차원 1/0.  (우리 산술) 1 V / 46 µm 이면 평균 전류밀도 전자 ≈ 4.5×10⁵ · 이온 ≈ 37 A m⁻² — Fig. 3 색 막대 (전자 0–1.00×10⁷ · 이온 0–1.00×10³ A m⁻², data max 1.92×10⁸ · 6.51×10³) 와 모순 없음 (정합 확인용일 뿐).
- ★ **산출 경로 확인 (우리 산술)**: NG 의 N_m (Fig. 2c 판독 12.2 · 7.45 · 4.95 · 3.8) = 2.5 / σ_eff,e (Table S4 · Fig. S7d → 12.20 · 7.46 · 4.95 · 3.82).  ⇒ N_m 은 **풀린 σ_eff 와 입력 σ₀ 의 비 (역산)** 이지 따로 계산한 기하 τ 가 아니다 — 적어도 전자상에서는 수치로 선다.  이온상은 § τ 정의 대조 (4).
- 계면 항: "contact resistance" · "grain boundary" 낱말 0 회.  접촉은 *"heat treatment"* 로 생긴다고 가정한다 (p.125) → 복셀이 면을 공유하면 고유 σ 그대로 이어진다 = **접촉 저항 0 (CONTACT_FREE)**.

### 4-4. 3 단계 — 전기화학 (COMSOL Multiphysics 5.3a, Batteries & Fuel Cells, Newman P2D)
**원문 전사 (SI p.4 Fig. S5)**:
- 1D 기하: `Composite Anode | Li₂S-P₂S₅ electrolyte | Li Metal` (x →).
- 경계: 복합 음극 바깥 끝 `−σ_s,eff ∂φ_s/∂x = I/A` · `∇c_e = 0` · `∇φ_e = 0` / 음극–LPS 계면 `−σ_s,eff ∂φ_s/∂x = 0` / Li 금속 `φ_s = 0` · `∇c_e = 0` · `∇φ_e = 0` (인쇄 그대로).
- 입자: `∂c_s/∂t = ∇(D_s∇c_s)` · `∂c_s/∂r|_{r=0} = 0` · `D_s ∂c_s/∂r|_{r=Rs} = j/F`.
- 반응: `η = φ_s − φ_e − E_eq` · `j = i_0(exp(α_a F η/RT) − exp(−α_c F η/RT))` · `i_0 = F k (c_s,max − c_s)^0.5 (c_s)^0.5 (c_e/c_e,ref)^0.5` ("At surface of active materials").
- 전해질: `ε_e ∂c_e/∂t + ∇(−D_e,eff ∇c_e + t₊ (−σ_e,eff ∇φ_e + (2σ_e,eff RT/F)(1−t₊)∇ln c_e)/F) = a_s j/F` · `∇(−σ_e,eff ∇φ_e + (2σ_e,eff RT/F)(1−t₊)∇ln c_e) = a_s j`.
- 고체: `∇(σ_s,eff ∇φ_s) = a_s j`.
- 셀: 반쪽셀 ASSE (LSTP 40 또는 30 %) | LPS | Li 금속 (p.126).

**읽기**:
- 3D 구조에서 온 값 = σ_s,eff · σ_e,eff (Table S4 의 σ_s · σ_e,LSTP) · a_s · ε_s · ε_e — *"the specific contact area, and effective electric and ionic conductivities from the 3D structural model are used for building the electrochemical model"* (p.126).
- ★ **τ · Bruggeman 은 P2D 에 들어가지 않는다** — 유효 전도도가 식의 σ_eff 자리에 바로 들어간다 ("Bruggeman" 0 회 · COMSOL 의 tortuosity 보정 선택지 언급 없음).
- ⚠ a_s 는 활물질 부피 기준 (4-2) 인데 P2D 원천항 a_s j 는 통상 전극 부피 기준이다 — 환산 (× ε_s = 0.397 · 0.46) 여부 미기술 [미확인].
- ⚠ D_e,LSTP (4.0×10⁻¹⁶, 각주 c 문헌) 는 구조 보정 근거가 없다 — σ 는 3D 로 보정하고 D 는 안 했을 수 있다 (추론 · t₊ = 0.99 라 영향은 작을 것).
- ⚠ i_0 = 10 A m⁻² (c) 와 k = 2.0×10⁻¹¹ m s⁻¹ (b) 가 함께 적혀 있다 — 어느 반응 규격을 썼는지 미기술.
- ⚠ Li 금속 경계의 `∇φ_e = 0` 은 전류가 흐르는 경계와 맞지 않는다 — 도식 표기로 보인다 (BV 화살표가 Li 금속에도 그려져 있다).
- ⚠ nomenclature 는 κ 를 *"ionic conductivity, S m⁻¹"* 로 정의하지만 (SI p.9) 식 · 표는 σ_e 를 쓴다.  N_m · τ 는 nomenclature 에 없다.

### 4-5. 입자 처리 ★ (DEM 양식 항목)

| 항목 | 이 논문 |
|---|---|
| 입자 기술 | DEM 없음 — GeoDict 규칙 기반 확률 배치 |
| 형상 | NG = 타원체 볼록다면체 (강체) · LSTP = 구 (강체) |
| PSD | NG Gaussian (SD 5 µm) · LSTP 균일 250–500 nm — 사실상 2 분산 (NG ≫ LSTP) |
| 접촉 | 복셀 면 공유 + NG–LSTP 의도적 겹침 −0.1 µm · 열처리 접촉 가정 |
| 소성 | **없음** — CONTACT 소성도 SHAPE 소성도 아니다 (압력 · 압밀 축 자체가 없다) |
| 기계 | 응력 · 변형 · 압력 0 — Fig. 1 의 "Mechanical Stress ↑" · 서론의 사이클 응력은 동기 서술뿐 (p.125) |
| 바인더 | Added binder (형상 규칙만 · 전도 0) |

### 4-6. 대표성 · 해상도 · 반복
- **도메인 크기 시험** (p.126 · SI p.2 Fig. S2–S3): LSTP 40 · 20 % 를 25 / 50 / 75 / 100 / 200 µm 정사각 도메인으로.
  - a_s: 60:40 평균 48,035 (SD 937 → CV 2.0 %) · 80:20 평균 31,779 (SD 452 → CV 1.4 %) — 5 도메인 (CV = 우리 산술).
  - σ_eff,ion: **3 도메인만** (25 · 50 · 75 µm, 판독) — 60:40 평균 1.95×10⁻⁵ (SD 1.66×10⁻⁷ → CV 0.85 %) · 80:20 평균 1.81×10⁻⁸ (SD 9.61×10⁻⁹ → **CV 53 %**).
  - ⇒ 본문 *"we confirmed that similar results came out from all the domains ... So, the domain size of 50 μm × 50 μm is large enough to calculate reliable results"* (p.126) 은 a_s 와 40 % σ 에는 서지만 **20 % σ_ion (문턱 근처) 에는 서지 않는다**.
- **격자 수렴 시험 없음** — LSTP 지름 2.5–5 voxel (우리 산술).  입자 사이 목 (neck) 이 1 voxel 수준이라 N_m 의 격자 의존이 클 수 있다 (우리 STEP3 격자 미수렴 실측 — 메인 리포 CLAUDE.md `CL-41` · `CL-25`).  voxel 크기를 보고한 덕에 **감사는 가능하다** (같은 GeoDict 계열 Weitze 2024 는 voxel 미보고 — `comparison_vs_ours_DEM.md`).
- **실현 반복 없음** — 조성당 구조 1 개로 읽힌다 [미확인].  오차 막대 0.  후속 park2020 은 seed 1–5 로 반복했다 (그 카드 Fig S5 행) — 이 한계를 다음 논문이 메웠다.

### 4-7. 기법 미니 용어집
- **GeoDict (GEODICT®, Math2Market)** — 복셀 기반 미세구조 생성 · 분석 상용 패키지.  **GrainGeo** = 입자 배치 · **PoroDict** = 기공 · 면적 분석 · **ConductoDict** = 전도 (Ohm/Laplace) 해석 모듈.
- **voxel array formation** — 정규 격자에 상 번호를 채워 구조를 만드는 방식 (2D 픽셀의 3D 판).
- **isolation distance (overlap mode)** — 새 입자를 놓을 때 기존 입자와의 최소 거리.  음수면 그만큼 겹침 허용 (원문 −0.1 µm).
- **MacMullin number N_m** — σ₀/σ_eff (≥ 1).  N_m = τ/ε 로 쓰면 그 τ 는 tortuosity factor (우리 tau2).
- **specific contact area a_s** — 이 논문 정의 = 접촉면적 ÷ 활물질 부피 (m⁻¹).
- **P2D (pseudo-two-dimensional)** — Newman 다공 전극 모델: 두께 방향 1D × 입자 반경 방향 1D.
- **LSTP** — Li₂O–SiO₂–TiO₂–P₂O₅ 산화물 고체전해질 (유리세라믹 계열 · [31]).  **LPS** — Li₂S–P₂S₅ 황화물 (이 논문에서는 분리막).  **ASSE** — all-solid-state electrode.

## 5. Figure set ★

| Fig | 쪽 | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|---|
| 1 | p.125 | 모식: 액체 전극 (이온 전도 ↑ · 표면적 ↑) vs 전고체 전극 (표면적 ↓ · 이온 전도 ↓ · 기계 응력 ↑) | 문제 설정 3 축 (경로 · 계면 면적 · 사이클 응력) — 정성 |
| 2a | p.126 | 60:40 · 90:10 3D 구조 + 단면 (적 = NG · 녹 = LSTP · 황 = 바인더 · 백 = 기공) | 극단 입경비 (NG ≫ LSTP) 시각 |
| 2b | p.126 | A_c (왼축 0–1×10⁻⁸ m²) · a_s (오른축 0–50,000 m⁻¹) vs LSTP % | a_s = A_c/V_NG — 두 축이 서로 재현되지 않는다 (4-2) |
| **2c** ★ | p.126 | N_m — NG (왼축 0–16) · LSTP (오른축, 끊긴 축 0–400 / 10,000–50,000) vs LSTP % · 10 % LSTP 점 없음 · 축 이름 오기 "Structue" (원문 그대로) | ★ 이 논문의 유일한 τ 계열 그림 — **크롭** |
| 2d | p.126 | LSTP 상만 (40 · 10 %) 3D + 단면 | 10 % 끊김 시각 |
| 3 | p.127 | (a–d) 전자 · (e–h) 이온 전류밀도 3D 장, 60:40 → 90:10 · (h) "No Results Calculated" · 색 막대 A m⁻² (전자 0–1.00×10⁷, data max 1.92×10⁸ · 이온 0–1.00×10³, data max 6.51×10³) | 퍼콜 끊김의 장 그림 · data range 가 어느 패널 것인지 미표기 |
| 4 | p.128 | (a,b) 충전 전압 0.05–0.5C · (c,d) NG SOC 깊이 분포 (0–35,000 s, 0.1C) · (e,f) 과전압 깊이 분포, 40 vs 30 % | 우리 STEP4 반응분포 · φ(z) 출력과 같은 형식 |
| S1 | SI p.2 | 70:30 · 80:20 3D 구조 | — |
| S2 | SI p.2 | 도메인 25–200 µm 구조 (60:40 높이 46 µm · 80:20 높이 37 µm) | RVE 시험 설계 |
| **S3** ★ | SI p.2 | a_s · σ_eff,ion vs 도메인 부피 (60:40 · 80:20) + 평균 · SD 주석 · "Present domain size" 화살표 | ★ 본문 1.69×10⁻⁵ 과 다른 평균 1.95×10⁻⁵ · 20 % CV 53 % — **크롭** |
| **Table S3 + S4** ★★ | SI p.3 | σ₀ 표 · 지배식 j = (σ/N_m)∇φ · 6 면 Dirichlet | ★★ park2020 Fig S9 의 원형 · τ 관례 원문 — **크롭** |
| S5 | SI p.4 | P2D 도메인 · 식 · 경계조건 | σ_eff 직접 투입 (τ 칸 우회) |
| Table S4 | SI p.5 | P2D 매개변수 22 행 | 크롭 후보 (결정 5 선례) |
| S6 | SI p.6 | LSTP 40 % 상만, − / 무 / + 원근 단면 | — |
| **S7** ★ | SI p.6 | (a–c) 이온 전류 3D + 단면 40/30/20 % · (d) σ_eff 전자 (왼축 0–1.0) · 이온 (오른축 0–2.5×10⁻⁵) vs LSTP % · 색 막대 0–1.00×10³ A m⁻² (data max 2.38×10⁴) | ★ (d) = N_m 의 원천 σ_eff · 40 % 이온 점 ≈1.94×10⁻⁵ — **크롭** |
| S8 | SI p.7 | Fig. 4 의 방전판 (전압 · SOC · 과전압) | — |

## 6. Post-processing ★
- **무엇**: (i) PoroDict 접촉면적 A_c → a_s = A_c/V_NG · (ii) ConductoDict σ_eff → N_m = σ₀/σ_eff · (iii) 전류밀도 3D 장 · 임의 축 단면 스캔 (Fig. 3 · S7a–c) · (iv) P2D 출력 = 전압 곡선 · 깊이별 SOC · 과전압 · 율특성.
- **도구**: GeoDict 2018 (GrainGeo · PoroDict · ConductoDict) · COMSOL 5.3a.
- **수치화 · 그림**: N_m vs 조성 (끊긴 이중 축) · σ_eff vs 조성 (이중 축) · A_c · a_s vs 조성 (이중 축) · 도메인 부피 vs a_s · σ (평균 ± SD 주석) · 시간별 깊이 분포.
- **하지 않은 것**: τ 자체 · 기하 τ · Bruggeman 대조 · 연결 (percolating) 분율 정량 · 퍼콜 문턱 정량 · seed 오차 막대 · 실험 대조.

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

> ⚠ `our_dem_baseline.md` 는 이 브랜치에서 **자리표시 (값 0 개)** 다.  아래 우리 쪽 수치는 판단 메모 v2 (메인 리포 `docs/reviews/tau_conventions_judgment_v2_20261003.md`) 의 (유도) 값과
> 메인 리포 CLAUDE.md 정본 서술에서 가져왔고, 그 지위 (1 세대 협착식 · ML 기술자 전용 · 실험 절대 대조 HOLD) 를 그대로 단다.

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 미세구조 생성 | GeoDict 규칙 기반 확률 배치 · 압밀 없음 | LIGGGHTS DEM 300 MPa 압밀 (+ MPM scaffold) | **다름** — 압밀 물리 없음 (park2020 과 같은 계보 한계) |
| 재료 | NG + LSTP 산화물 (음극) | NCM811 + LPSCl (양극) | **다름** — 수치 전이 불가 |
| 입경비 r_SE/r_AM | 0.018–0.036 (우리 산술) | 중앙 ≈ 0.13 (메모 v2 §3-8) | 극단적으로 작은 SE — 문턱 · 연결성 다름 |
| 기공 | 30 % (설계) | ε_sphere 띠 중앙 4.7–18.7 % (메모 v2 §3-3) · real_14 15.6 % | **다름** |
| 수송 솔버 | 복셀 FVM (ConductoDict) — 접촉 · 입계 저항 없음 | 접촉망 Kirchhoff + SE–SE Holm (FULL) · CF 가지 (접촉 저항 0, 원기둥 bulk) · STEP3 복셀 FV (CONTACT_FREE) | Park = 우리 **STEP3 복셀 계열 (CONTACT_FREE)** · FULL 과 다른 양 |
| σ₀ | 문헌 입력 (LSTP 9.9×10⁻⁴ · NG 2.5 S cm⁻¹) | 간선 재료 σ₀ 3.0 mS cm⁻¹ (펠릿값, `CL-91`) | 성격 같음 (입력값) · 재료 · 값 다름 |
| 기준 상태 (순수 SE 의 tau2) | 치밀 고유 σ₀ = 1 (복셀 연속체 · 구성상) | 펠릿 σ₀ + Holm → T_pure,ours ≈ 1.4–2.0 (hertz 외삽 · 측정 아님, 메모 v2 §3-2) | **다름** — 절대 대조 전에 맞춰야 할 축 (결정 4) |
| φ 회계 | ε = 전체 부피 상 분율 (GeoDict 복셀 합집합) | φ_SE = 전 SE 구 부피 합 ÷ 상자 (겹침 이중계상) | 같은 '전체 상' 계열 · 겹침만큼 다름 |
| tau2 ≥ 1? | 전부 ≥ 1 (이온 11–3,344 · 전자 2.2–4.8, 우리 산술 § τ 정의 대조 (3)) | FULL 157/157 ≥ 1 · CF 26/157 < 1 (메모 v2 §3-6) | 복셀 연속체 = Wiener 준수 · 우리 CF 는 원기둥 bulk 성질 |
| 같은 φ 근처 tau2 | LSTP 40 % (ε 0.237): 11.1 (N_m 기준) · 13.9 (본문 σ_eff + Table S3 σ₀) | φ_SE 0.248 ± 0.04 띠 T_H 중앙 13.5 [6.21–26.6] · T_P 19.7 (n 46, 메모 v2 §3-3 유도) | 같은 자릿수 — **판정 아님** (다른 양 · 다른 미세구조 · 우리 쪽 1 세대 협착식) |
| 이온 퍼콜 문턱 | ε_LSTP 0.058 (끊김) 과 0.117 (거의 0) 사이 | 모델 φ_c 0.195–0.200 (σ_ionic 폼 · 동결) | **다름** — 극단 입경비 · 복셀 융합 둘 다 문턱을 낮추는 방향, 분리 불가 → 우리 φ_c 재선별 근거 아님 |
| 해상도 | voxel 0.1 µm = LSTP 지름 2.5–5 voxel · 격자 시험 없음 | STEP3 격자 미수렴 실측 (`CL-41`) | Park 수치는 격자 미검증 |
| 접촉면적 | PoroDict 기하 A_c · a_s = A_c/V_AM → P2D 반응 면적 | coverage 기하면적만 인계 (J20-m) · physics 면적 HOLD (`LHS-25`) | 같은 '기하' 계열 · **분모 규약을 명시**해야 같은 양 |
| P2D 연결 | σ_eff · a_s 를 P2D 식에 직접 | STEP4 (BV 반응분포) · COMSOL 내보내기 (`TAU-01` — 정정 방침 비준 10-03, 결정 5) | Park = τ 칸을 비켜 간 선례 (결정 5) |
| 실험 | 없음 (p.128) | 절대 대조는 순수 SE 게이트 뒤 (결정 4) | 이 논문은 앵커가 될 수 없다 |

- **frame [5]**: 이 논문은 **수송 (복셀 · 접촉 저항 0) + 전기화학 (P2D)** 만 가진다.  압밀 · 형상 소성 · 응력 (MPM 절반) 도, 접촉 단위 협착 (DEM 접촉망 절반) 도 없다.
- **frame [4]**: 이 논문 수치로 우리 모델을 맞추지 않는다 (다른 재료 · 실험 없음).  가져오는 것은 ① τ 관례 · 경계조건 원형 ② 구조 → P2D 연결 관행 ③ 해상도 · RVE · 실현 수 보고의 반면교사.

## § τ 정의 대조 — 우리 규약 매핑

### (1) 원문이 말하는 것 / 말하지 않는 것

| 항목 | 원문 | 위치 | 판정 |
|---|---|---|---|
| τ 정의 | *"increasing the volume fraction (ε) of the solid electrolyte and decreasing its tortuosity (τ) ... The ratio of these two parameters is the MacMullin number (N_m = τ/ε) [13,14]"* | p.124 | ✅ N_m = τ/ε — Landesfeind Eq 5 와 같은 꼴 ([14] = Landesfeind 2016) |
| σ_eff ↔ N_m | *"the conductivity is inversely proportional to the MacMullin number"* (p.124) · `Domain: j = (σ/N_m)∇φ` (SI p.3 Fig. S4) | p.124 · SI p.3 | ✅ σ_eff = σ/N_m ⇒ **N_m = σ₀/σ_eff** |
| τ 이름 | *"tortuosity (τ)"* — "tortuosity factor" 0 회 (전문 검색 "factor" = *"by a factor of four"* 1 회뿐) | p.124 | 이름은 "tortuosity" 뿐 (park2020 과 같음) |
| τ 값 | — | — | **보고 없음** (본문 · SI 전수) |
| τ 산출 | *"all contact areas between components, electric or ionic conductivity, and tortuosity can be easily calculated from the 3D virtual microstructures"* (p.125) — 그러나 결과는 N_m · σ_eff 만 | p.125 | τ 는 정의 · 서술에만 나온다 |
| N_m 산출 경로 | NG: N_m (Fig. 2c) = 2.5 / σ_eff,e (Fig. S7d · Table S4) | p.126 · SI p.3 · p.5 · p.6 | ✅ (우리 산술) — **풀린 σ_eff 에서 역산** |
| | LSTP: N_m × σ_eff (본문) = 7.94–7.97×10⁻⁴ S cm⁻¹ | p.127 · SI p.5 | ⚠ Table S3 σ₀ 로 재현 안 됨 (4) |
| ε | ε_e = 0.237 · 0.177 = Table S1 LSTP vol% · nomenclature *"volume fraction of electrolyte"* | SI p.1 · p.5 · p.8 | ✅ 전극 전체 부피 기준 (기공 30 % · 바인더 포함) |
| 정규화 단면 | 명시 문장 없음 | — | 도메인 전체 면 (추론) |
| 방향 | Fig. S4 = x · y · z 마주 보는 면 Dirichlet | SI p.3 | 보고값의 방향 **미기술** |
| σ₀ | Table S3 | SI p.3 | 문헌 입력 · 조성 무관 |
| 계면 저항 | "contact resistance" · "grain boundary" 0 회 · 접촉 = 열처리 가정 | p.125 | 복셀 융합 = **CONTACT_FREE** |
| Bruggeman · 기하 τ · τ_e | 0 회 | — | 없음 |

### (2) 매핑표 — 우리 다섯 양 기준

| 우리 양 | 우리 식 · 키 | 이 논문의 대응 | 원문 위치 | 환산 · 비고 |
|---|---|---|---|---|
| **f** | σ_eff/σ₀ · `f_ion_<mode>` | **1/N_m** | p.124 · SI p.3 | f = 1/N_m — LSTP 40 % 0.0213 · 30 % 0.0056 (우리 산술) |
| **tau2** | φσ₀/σ_eff = φ/f · `tau2_ion_<mode>` | **원문 τ** (N_m = τ/ε ⇒ τ = ε·N_m) · 이름 "tortuosity" · tortuosity factor 자리 | p.124 | tau2 = ε·N_m — **원문 수치 없음** · (3) 에 우리 산술 |
| **tau** | √tau2 · `tau_ion_<mode>` | 없음 | — | √(ε·N_m) |
| **τ_geo** | 최단경로 / 두께 · `tau_geo_SE_dij` | 없음 (기하 τ 계산 · 보고 없음) | — | — |
| **τ_e** | (우리에 없음) | 없음 — P2D 에 관통형 Dirichlet σ_eff (conventional) 를 그대로 넣음 | SI p.4–5 | Nguyen 의 P2D 권고 (τ_e) 와 다른 관행 |

| 원문 기호 | 원문 정의 (쪽) | 원문 이름 | 정규화 · σ₀ | 우리 양 |
|---|---|---|---|---|
| N_m | N_m = τ/ε (p.124) · j = (σ/N_m)∇φ (SI p.3) | MacMullin number | 전체 단면 (추론) · σ = Table S3 | 1/f |
| τ | τ = ε·N_m (p.124 의 대수) | tortuosity | ε = 전체 부피 상 분율 | tau2 |
| ε_e · ε_s | 상 부피분율 (SI p.8–9) | volume fraction of electrolyte / active material | 전체 부피 | φ_SE · φ_AM |
| σ_s,eff · σ_e,eff | P2D 식 (SI p.4) · Table S4 값 | effective (conductivity) | 겉보기 (추론) | σ_eff (우리 σ_full · σ_bulk_net) |
| σ (Table S3) | intrinsic | intrinsic electric / ionic conductivity | 문헌 입력 | σ₀ |
| (park2020) τ_e · τ_s | j = (εσ/τ)∇φ (그 카드 §4) | tortuosity of electrolyte / active material | — | tau2 — park2020 Fig S9 = 이 논문 Fig. S4 를 N_m = τ/ε 로 고쳐 쓴 꼴 (σ/N_m = εσ/τ) |

- **σ₀ 기준**: Park = 문헌 입력 고유값 (재료값으로 보이나 [31, 32] 원문 미확인).  복셀 연속체이므로 기공 없는 순수 LSTP 블록은 **구성상 N_m = 1 · τ = 1** — 기준 상태 = "치밀 고유 σ₀ = 1".
  Minnmann = "순수 SE 펠릿 = 1" (σ₀ 1.6 mS cm⁻¹, 펠릿) · 우리 = 펠릿 σ₀ 3.0 위에 SE–SE Holm 직렬 (T_pure,ours > 1 외삽).  ⇒ **같은 "tau2" 이름 아래 기준 상태가 셋**이다.

### (3) 우리 규약으로 다시 쓴 값 — **우리 산술 · 원문 값 아님 · TREND 전용**

| 상 · 조성 | ε (Table S1) | N_m (원문) | f = 1/N_m | tau2 = ε·N_m | tau = √tau2 | tau2 (본문 σ_eff + Table S3 σ₀) | Bruggeman tau2 = ε^−0.5 | tau2 / Bruggeman |
|---|---|---|---|---|---|---|---|---|
| LSTP 40 % | 0.2370 | 47 | 0.0213 | **11.1** | 3.34 | 13.9 | 2.05 | 5.4 (σ 기준 6.8) |
| LSTP 30 % | 0.1766 | 178 | 0.0056 | **31.4** | 5.61 | 39.0 | 2.38 | 13.2 (σ 기준 16.4) |
| LSTP 20 % | 0.1171 | 28,556 | 3.5×10⁻⁵ | **≈3,300** | ≈58 | — | 2.92 | ≈1,100 |
| LSTP 10 % | 0.0577 | 결과 없음 | 0 | ∞ (비관통) | — | — | — | — |
| NG 40 % (전자) | 0.3970 | 12.20 (= 2.5/0.205) | 0.082 | 4.84 | 2.20 | = | 1.59 | 3.05 |
| NG 30 % | 0.4603 | 7.46 (= 2.5/0.335) | 0.134 | 3.44 | 1.85 | = | 1.47 | 2.33 |
| NG 20 % | 0.5231 | ≈4.95 (판독) | ≈0.20 | ≈2.6 | ≈1.6 | = | 1.38 | ≈1.9 |
| NG 10 % | 0.5803 | ≈3.82 (판독) | ≈0.26 | ≈2.2 | ≈1.5 | = | 1.31 | ≈1.7 |

- Fig. S3 평균 σ (1.95×10⁻⁵) 로 쓰면 LSTP 40 % tau2 = 12.0 · tau 3.47.  ⇒ 이온 40 % 의 tau2 는 σ₀ · σ_eff 를 어느 것으로 두느냐에 따라 **11.1 ↔ 12.0 ↔ 13.9 (25 % 폭)** — 한 숫자로 옮기지 말 것.
- 20 % 는 도메인 실현값 의존 (Fig. S3 CV 53 %) · 문턱 근처 — 자릿수 감각만.
- "=" = 전자상은 N_m 이 이미 σ₀/σ_eff 와 같다.
- Bruggeman 배수 (이온 5–16 · 전자 1.7–3.1) 는 액체 전극 측정 (Landesfeind ≈ 1.5–3×) 보다 크고, 퍼콜 문턱으로 갈수록 발산한다 — 방향만 참고.

### (4) 원문 내부 불일치 — 이온 N_m 의 σ₀

| 상 · 조성 | N_m (원문) | σ_eff (원문) | N_m × σ_eff (우리 산술) | Table S3 σ₀ | 비 |
|---|---|---|---|---|---|
| NG 40 % | ≈12.2 (판독) | 0.205 (Table S4) | ≈2.50 S cm⁻¹ | 2.5 | **1.00** |
| NG 30 % | ≈7.45 (판독) | 0.335 (Table S4) | ≈2.50 S cm⁻¹ | 2.5 | **1.00** |
| LSTP 40 % | 47 | 1.69×10⁻⁵ (본문 · Table S4) | 7.94×10⁻⁴ | 9.9×10⁻⁴ | **0.802** |
| LSTP 30 % | 178 | 4.48×10⁻⁶ (본문 · Table S4) | 7.97×10⁻⁴ | 9.9×10⁻⁴ | **0.805** |
| LSTP 40 % | 47 | 1.95×10⁻⁵ (Fig. S3 평균) | 9.17×10⁻⁴ | 9.9×10⁻⁴ | 0.93 |

- 두 조성의 LSTP 곱이 **0.4 % 안에서 같다** → 우연보다는 체계적 관계로 보인다 (추론).  그러나 그 값 (≈7.95×10⁻⁴) 은 Table S3 σ₀ 가 아니다.
- 원인 후보 (원문 근거 없음 · **판정하지 않는다**): ① N_m 계산에 다른 σ₀ (≈7.95×10⁻⁴) 를 썼다 ② 본문 σ_eff 를 다른 σ₀ 로 N_m 에서 되계산했다 ③ 방향 · 실현이 다른 두 계산을 섞었다 ④ 오기 (1.69 ↔ 1.96 자리바꿈이면 40 % 는 그림과 맞지만 30 % 의 0.80 배가 남는다).
- 본문 (p.127) 은 1.69×10⁻⁵ 을 *"(Figs. S7d and S8b)"* 로 인용하는데, Fig. S7d 의 40 % 이온 점은 ≈1.94×10⁻⁵ (판독) 이고 Fig. S3 평균은 1.95×10⁻⁵ 다 — **본문이 인용한 그림과 본문 수가 13–15 % 어긋난다**.
- ⇒ **이온 N_m 뒤의 σ₀ 는 원문에서 재구성할 수 없다.**  전자 N_m 은 재구성된다 (σ₀ = Table S3 2.5 S cm⁻¹).

### (5) park2020 과의 관계 (그 카드의 열린 질문에 대한 답)

| park2020 카드 (`park2020_digitaltwin_assb_foundational`) 의 열린 칸 | 이 원문이 주는 것 | 닫히나 |
|---|---|---|
| §4-T "τ 산출법 미기술 — EJ 해에서 역산한 양인지, GeoDict 가 따로 낸 τ 를 식에 넣은 것인지" | 선행 (이 논문) 에서는 **해 → σ_eff → N_m 역산** (전자상 수치 확인) | ◐ park2020 에 대해서는 **개연성 상승 (추론 등급 그대로)** — park2020 원문 근거는 여전히 없다 |
| §4 경계조건 (Fig S9 = 6 면 Dirichlet, 각 면 값) | 이 논문 Fig. S4 = **같은 6 면 Dirichlet (1/0)** + j = (σ/N_m)∇φ | ✅ Fig S9 의 원형 확인 (park2020 은 N_m → τ/ε 로 고쳐 씀) |
| §4-T 방향 · 측면 경계 미기술 | 이 논문도 미기술 | ✗ 그대로 |
| §4-T σ_eff 정규화 = 전체 단면 (추론) | 이 논문도 명시 없음 · σ_eff 를 P2D 겉보기 σ_eff 로 투입 | ◐ 같은 추론의 근거 하나 추가 |
| §4-T τ 값 · "tortuosity factor" 이름 | τ 값 없음 (N_m 만, 다른 재료계) · 이름 "tortuosity" 뿐 | ✗ 그대로 |
| Table S2 각주 b — σ_s · σ_e 출처 [12, 16d, 18] | 이 논문 Table S3 = NG 2.5 · LSTP 9.9×10⁻⁴ · 바인더 0 뿐 — **NCM 8.5×10⁻⁴ 도 LPSCl 조성식도 없다** | ✅ **[12a] 는 park2020 σ₀ 의 출처가 아니다** ([12b] · [16d] · [18] 은 이 카드 범위 밖) |
| §5 specific contact area 분모 부피 미기술 | 선행 정의 a_s = A_c/V_a (V_a = 활물질 bulk 부피, p.125) | ◐ park2020 에 같은 정의였을 개연성 (추론) — 단 이 논문 안에서도 Fig. 2b 두 축이 그 정의로 재현되지 않는다 |

## 8. 적용 인사이트 (내 연구에 어떻게)

### 8-1. Park 디지털 트윈 τ 의 산출법 · σ₀ 규약

| 물은 것 | 이 원문의 답 | 쪽 | park2020 에 대해 |
|---|---|---|---|
| 미세구조 생성 도구 | GeoDict (2018 판 화면) **GrainGeo** — NG Gaussian 타원체 볼록다면체 → LSTP 구 overlap −0.1 µm → Added binder · voxel 0.1 µm · 50 × 50 µm × 46–33 µm | p.125–126 · SI p.1 | 같은 GrainGeo (park2020 = GeoDict 2020) — 계보 확인 |
| τ 계산 방정식 | **ConductoDict (FVM)** 정상 Ohm 전도 · 인쇄된 식은 균질화형 j = (σ/N_m)∇φ 뿐 | p.126 · SI p.3 | park2020 Fig S9 의 j = (εσ/τ)∇φ 와 대수적으로 같다 |
| 경계조건 | **6 면 Dirichlet** φ = 1 (+x · +y · +z) / 0 (−x · −y · −z) · 측면 경계 · 방향 · 솔버 미기술 | SI p.3 | 같음 — 미기술 항목도 같다 |
| 어느 상 | 이온 = LSTP (NG · 바인더 0) · 전자 = NG (LSTP 1×10⁻¹⁵ · 바인더 0) | SI p.3 | park2020 = LPSCl · NCM 상 — 같은 상별 방식 (추론) |
| 정규화 | ε = 전체 부피 분율 (Table S1 = S4) · 단면 = 전체 면 (추론) | SI p.1 · p.5 | park2020 카드의 "전체 단면 (추론)" 과 같은 결론 |
| 보고된 τ 값 | **없음 — N_m 만** (LSTP 47 · 178 · 28,556 · NG 판독) | p.127 | park2020 τ 값은 이 원문에 없다 (다른 재료계) |
| 산출 경로 | 해 → σ_eff → **N_m = σ₀/σ_eff 역산** (전자상 정확) · 이온상은 × 0.80 불일치 | (우리 산술) | "역산" 쪽 개연성 ↑ — 증명은 아님 |
| σ_eff | 이온 1.69×10⁻⁵ · 4.48×10⁻⁶ (본문) · 1.95×10⁻⁵ (S3) · 전자 0.205 · 0.335 S cm⁻¹ | p.127 · SI p.2 · p.5 | — |
| σ₀ 출처 | **Table S3 문헌 입력** — [31, 32] (LSTP 9.9×10⁻⁴) · [30] (NG 2.5, 제목상 LBM 예측 논문) · 조성 무관 상수 · 측정 아님 | SI p.3 | **park2020 σ₀ (NCM 8.5×10⁻⁴ · LPSCl 조성식) 는 이 원문에 없다 → 출처 미해결** |
| 조성 · 입경 · 두께 · 바인더 | NG:LSTP 60:40–90:10 wt% · NG 14 µm · LSTP 0.25–0.5 µm · 46–33 µm · SBR:CMC 5 wt% · 기공 30 % · **NCM 없음** | p.125 · SI p.1 | park2020 (NCM711 + LPSCl + NBR 2 wt%) 와 재료가 다르다 |

**판정 — 메모 v2 §3-4 한정어 "Park 역산 T = 추세 전용 · T_Park ∝ 가정 σ₀"**:
- **"T_Park ∝ 가정 σ₀" → 유지 (좁혀지지 않는다).**  park2020 σ₀ 의 출처를 이 원문이 주지 않는다.  오히려 같은 계보의 선행에서도 σ₀ 는 문헌 입력값이고, 이온 N_m 은 그 입력 σ₀ 로 재현되지 않는다 (0.80 배) → 한정어의 근거가 하나 늘었다.
- **"추세 전용" → 유지.**  τ 원값 없음 (N_m 만 · 다른 재료계) · 실험 없음 · 격자 미검증 · 실현 1 개.
- **좁혀지는 것 = 산출법의 "역산 vs 대입" 질문 하나** — 선행에서는 해에서 역산 (전자상 수치 확인).  park2020 τ 도 역산이었을 개연성이 올라간다 (추론 등급 그대로 · 증거 1 단계 상승).
- 메모 v2 §8-1 #5 의 기대 *"(역산 대신 원값)"* 은 이 원문으로 **충족되지 않는다** — 원값이 있을 남은 후보는 [12b] Park 2020 Chem. Eng. J. (이 카드 범위 밖).

### 8-2. 결정 16 (메모 v2 §0-2) 에 주는 것

| 결정 | 이 원문이 주는 것 | 권고 변경 |
|---|---|---|
| **4** 순수 SE 기준 상태 | Park 형 복셀 N_m 의 기준 = "치밀 고유 σ₀ = 1" (구성상 · 계면 항 없음 · 열처리 접촉 가정 p.125).  Minnmann (순수 펠릿 = 1) · 우리 (펠릿 σ₀ + Holm, T_pure,ours > 1 외삽) 와 함께 **같은 tau2 이름 아래 기준 상태가 셋** | **아니오** — 기준 상태를 맞춘 뒤 대조한다는 권고를 지지 |
| **5** COMSOL 표기 | P2D 에 τ 를 넣지 않고 3D σ_eff 를 σ_eff 자리에 바로 넣었다 (SI p.4 Fig. S5 · SI p.5 Table S4 · p.126) — τ ↔ √τ 모호성 자체를 비켜 간 선례 | **아니오** — 보강: COMSOL 용 열을 σ_eff (또는 f) + σ₀ 짝으로도 주면 GUI 확인 전에도 안전 (σ₀ 짝 명기 권고와 같은 방향) |
| **9** LHS-25 접촉 면적 | PoroDict 기하 A_c 를 활물질 부피로 나눈 a_s 를 P2D 반응 면적으로 직접 투입 — 역학 없는 기하 면적이 이 계보의 관행 · 분모 규약 (AM 부피 vs 전극 부피) 이 ε_s 배 (0.40–0.46) 를 가른다 | **아니오** — 면적 열 사전에 분모 부피를 명기할 근거 |
| **11** CF 지위 · 협착 비 | Park 복셀 값은 전부 tau2 ≥ 1 (우리 산술) = 연속체 Wiener 준수 — 우리 CF 의 T < 1 (26/157) 이 원기둥 bulk 성질이라는 메모 판정과 정합 · "이상 접촉" 의 문헌형 대응은 복셀 연속체 (Park · 우리 STEP3) 쪽.  단 Park 은 LSTP 2.5–5 voxel · 격자 시험 없음 | **아니오** — 보강: 복셀 ÷ 접촉망 대조 사전등록에 **복셀 쪽 격자 수렴 조건**을 함께 등록 |
| **13** τ_e | P2D 에 관통형 Dirichlet σ_eff (conventional) 를 그대로 썼다 — Nguyen 이 P2D 에 τ_e 를 권하는 바로 그 관행 | **아니오** — "P2D 입력 열 보류 · 부호 불정" 지지 |
| **14** 전자 · 열 | 전자 N_m 이 단일 σ₀ (NG 2.5 S cm⁻¹) 대비 σ_eff 로 정확히 정의된다 (우리 산술로 확인) — "단일 σ₀ 기준 f · T" 권고의 문헌 선례 | **아니오** |

### 8-3. 그 밖
- ① **반면교사 3 개 (우리 인계 · 원고에 그대로 적용)**: (a) τ 계열 값을 낼 때 **σ₀ 를 숫자와 같은 줄에** 적는다 — Park 은 표에 σ₀ 를 적어 놓고도 이온 N_m 이 그 σ₀ 와 어긋났다 (b) RVE 시험은 **문턱 근처 조성**에서 해야 의미가 있다 — 40 % 는 CV 0.85 % 인데 20 % 는 53 % (c) 복셀 σ 에는 **격자 수렴**과 **실현 수**를 붙인다.
- ② "LSTP 20 % 이하 = 이온 경로 끊김" (ε_LSTP 0.117) 은 우리 φ_c 0.195–0.200 보다 낮다 — 원인 후보 (극단 입경비 · 복셀 융합 · 단일 실현) 를 분리할 수 없으므로 우리 σ_ionic 폼의 φ_c 동결 (재선별 금지) 에 **영향 없음**.
- ③ 3 단계 흐름 (구조 → 구조 기술자 → P2D) 은 우리 DEM/MPM → STEP3/접촉망 → STEP4 와 같은 골격이다.  우리가 더하는 것 = 압밀 물리 · 접촉 단위 협착 · 격자 수렴 감사 · 실험 대조 게이트.
- ④ park2020 카드의 §13 [12] 행 (*"τ 의 정의·산출법·수치가 있을 1순위"*) 은 이 원문으로 **정의 · 경계조건 · 산출 경로 = 있음 / 수치 = NG · LSTP 의 N_m 뿐 / σ₀ = 없음** 으로 갱신할 수 있다 (갱신 여부는 메인 판단 — 이 카드는 그 카드를 고치지 않는다).

## 9. 인용 가능 문장 (deck/paper용)
- "Park et al. (Energy Storage Mater. 2019) define the MacMullin number as N_m = τ/ε and impose it through an effective Ohm's law j = (σ/N_m)∇φ with Dirichlet potentials on opposing faces of a GeoDict voxel domain (SI Fig. S4); their τ therefore occupies the tortuosity-factor slot (ε·σ₀/σ_eff), but only N_m — not τ — is reported."
- "In that voxel model (graphite + 250–500 nm LSTP oxide electrolyte; no contact resistance; no experimental validation), the ionic MacMullin number rises from 47 to 178 to 28,556 as the LSTP content drops from 40 to 30 to 20 wt%."
- "The structure-derived effective conductivities were passed to the P2D model directly, bypassing any tortuosity input — a precedent for exporting σ_eff together with σ₀ rather than a tortuosity value."

## 10. 주의/한계 (over-claim 방지)

### 10-1. 이 논문의 한계
- **재료계**: NG + 산화물 LSTP **음극** ≠ LPSCl/NCM 양극 — 수치 전이 불가.  입경비 0.018–0.036 은 우리 (≈ 0.13) 보다 한 자릿수 작다.
- **실험 없음** (p.128 자기 한정).  Table S4 각주 a 의 "experimental" 은 설계값 표기일 뿐 측정 보고가 없다.
- **압밀 · 기계 없음** — 확률 배치 + 열처리 접촉 가정.  frame[5] 의 기계 절반이 비어 있다.
- **해상도**: LSTP 2.5–5 voxel · 격자 시험 없음 → N_m 격자 의존 가능.
- **대표성**: 20 % σ_ion 의 도메인 간 CV 53 % · σ_ion 은 5 도메인 중 3 개만 → *"모든 도메인에서 비슷"* (p.126) 은 a_s 와 40 % σ 에만 선다.  실현 (seed) 반복 없음 [미확인].
- **내부 불일치** (전부 우리 산술 · 판정 없음): ① 이온 N_m ↔ Table S3 σ₀ (× 0.80) ② σ_eff,ion 40 % 본문 1.69×10⁻⁵ vs 그림 1.94–1.95×10⁻⁵ (본문이 그 그림을 인용) ③ Fig. 2b A_c ↔ a_s 가 원문 정의로 재현 안 됨 (A_c/V_NG ≈ 1.2×10⁵ vs 4.8×10⁴ m⁻¹ · 증가비 3.7 vs 2.7) ④ Table S4 I = 10 A m⁻² (≈ 0.83C) vs C-rate 스윕 ⑤ i_0 · k 병기 ⑥ Fig. 4c 의 0.1C 35,000 s 곡선 vs 0.1C 충전 용량 0.993 mAh cm⁻² (= 0.12 mA cm⁻² 로 ≈ 29,800 s) — CV · 휴지 단계 미기술 ⑦ nomenclature κ ↔ 식 σ_e ⑧ Fig. 2c 20 % 점 위치 ≈ 2.6×10⁴ vs 본문 28,556 (판독 오차일 수 있음).
- **P2D**: a_s 분모 (AM 부피) ↔ 원천항 (전극 부피) 환산 미기술 · D_e,LSTP 구조 보정 근거 없음 · Li 금속 경계 ∇φ_e = 0 인쇄 (도식 표기로 보임).
- **정의상 주의**: N_m = τ/ε 의 τ 는 tortuosity factor (우리 tau2) 자리다 — 원문은 "tortuosity" 라고만 부른다.  √ 값 (우리 tau) 과 섞지 말 것.
- **σ₀ 출처**: [30] 은 제목상 LBM 예측 논문 · [31, 32] 는 원문 미대조 → "재료 측정값" 으로 부르지 않는다.

### 10-2. 메모 v2 정정 후보 (쪽 번호 = 이 논문 인쇄 쪽 · SI 쪽)
- (a) **§8-1 #5 의 기대 "(역산 대신 원값)"** — 이 원문 ([12a]) 은 NG/LSTP 산화물 계이고 τ 를 보고하지 않으며 (N_m 만, p.126–127) LPSCl · NCM σ₀ 가 없다 (SI p.3 Table S3) → 기대 미충족 표지 후보.  원값 후보는 [12b] 로 넘어간다.
- (b) **§3-4 "Park τ 값 · 산출법은 원문에 보고되지 않았다"** — park2020 원문 기준으로 **참** (오류 아님).  보강 후보: *"선행 [12a] 는 같은 6 면 Dirichlet ConductoDict FVM 해에서 N_m = σ₀/σ_eff 를 역산한다 (SI p.3 Fig. S4 · p.126–127) — park2020 에도 같은 경로였을 개연성 (추론)"*.
- (c) **§1 대조표 N_M 행의 Park 칸 "—"** — park2020 기준으로 참.  Park 계보 칸 추가 후보: *"N_m = τ/ε 'MacMullin number' (park2019 p.124 · 지배식 j = (σ/N_m)∇φ SI p.3)"*.
- 정면으로 어긋나는 문장은 찾지 못했다.

### 10-3. park2020 카드 보강 후보 (메인 판단 — 이 카드는 그 카드를 고치지 않는다)
- §4-T "τ 산출법 미기술" 칸에 선행 경로 (§ τ 정의 대조 (5)) 를 덧붙일 수 있다 — park2020 자신에 대해서는 여전히 (추론).
- Table S2 각주 b 의 [12] 는 **σ₀ 값의 출처가 될 수 없다** ([12a] 기준 — 위 (5)).
- §13 [12] 행의 기대 갱신 (§8-3 ④).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
- **렌더해서 읽은 쪽**: 본문 6 쪽 전부 · SI 9 쪽 전부.  확대 렌더로 판독한 것 = Fig. 2b · 2c (20 % · 40 % 점 정밀) · Fig. 3 색 막대 두 개 · Fig. 4 · Fig. S3 두 패널 · Fig. S7d 와 색 막대 · Fig. S8.
- **텍스트층 함정**: p.126 의 *"isolation distance −0.1 μm"* 마이너스가 텍스트층에서 깨진 글리프로 나온다 (렌더로 확인).  p.128 의 *"−20 mV"* · *"−40 mV"* 도 같다.  "ﬁ" 합자 때문에 *"finite volume"* 이 텍스트 검색에 안 걸린다 (렌더로 확인).
- **전문 검색 (본문 + SI 텍스트층)**: "tortuos" = p.124 · p.125 + 참고문헌 2 건 · "factor" = *"by a factor of four"* 1 회 · "MacMullin" = p.124 · p.126 캡션 · p.127 · "Bruggeman" · "periodic" · "symmetric" · "contact resistance" · "grain boundar" · "seed" = 0 회 · "heat treatment" = p.125 1 회.
- **산술 재현 (우리 산술)**: N_m(NG) = 2.5/σ_eff 4 점 · N_m(LSTP) × σ_eff 3 점 · 기공 = 100 − Σvol% 4 점 · NG 부피 4 점 · Fig. 2b 일관성 4 점 · 도메인 CV 4 점 · tau2 · Bruggeman 표 (3).
- **그림 판독 정밀도**: 반 눈금 수준.  Fig. 2c 오른축은 끊긴 축 (아래 0–400 · 위 10,000–50,000, 위 구간 선형) — 20 % 점은 ≈ 2.6×10⁴ 위치 (본문값 28,556 을 쓴다).

## 참고문헌 — 우리가 더 볼 것 (원 목록 서지 그대로)

| 원 목록 | 이유 | 정본 카드 |
|---|---|---|
| [13] I.V. Thorat, D.E. Stephenson, N.A. Zacharias, K. Zaghib, J.N. Harb, D.R. Wheeler, Quantifying tortuosity in porous Li-ion battery materials, J. Power Sources 188 (2009) 592–600. | N_m = τ/ε 정의의 인용원 (α 관례) | 없음 (메모 v2 §8-2 목록에 있음) |
| [14] J. Landesfeind, J. Hattendorff, A. Ehrl, W.A. Wall, H.A. Gasteiger, Tortuosity determination of battery electrodes and separators by impedance spectroscopy, J. Electrochem. Soc. 163 (2016) A1373–A1387. | N_m = τ/ε 정의 (Eq 5) | ✅ `landesfeind2016_tortuosity_eis_electrodes_separators` |
| [18] D. Hlushkou, A.E. Reising, N. Kaiser, S. Spannenberger, S. Schlabach, Y. Kato, B. Roling, U. Tallarek, The influence of void space on ion transport in a composite cathode for all-solid-state batteries, J. Power Sources 396 (2018) 363–370. | 재구성 ASSB 이온 수송 — 같은 묶음 | 같은 묶음 `hlushkou2018_void_space_ion_transport_assb_cathode` (10-03 작성 중) |
| [19] M. Finsterbusch, T. Danner, C.-L. Tsai, S. Uhlenbruck, A. Latz, O. Guillon, High capacity garnet-based all-solid-state lithium batteries: fabrication and 3D-microstructure resolved modeling, ACS Appl. Mater. Interfaces 10 (2018) 22329–22339. | LCO/LLZO 3D 분해 모델 — 산화물 ASSB 의 구조 분해 수송 | 없음 (다른 카드에서 언급만) |
| [26] A. Bielefeld, D.A. Weber, J. Janek, Microstructural modeling of composite cathodes for all-solid-state batteries, J. Phys. Chem. C 123 (2019) 1626–1634. | 같은 GeoDict · 조성당 10 실현 · 퍼콜 문턱의 입경 의존 | ✅ `bielefeld2019_microstructural_modeling_composite_cathode` |
| [30] S. He, B.T. Habte, F. Jiang, LBM prediction of effective electric and species transport properties of lithium-ion battery graphite anode, Solid State Ionics 296 (2016) 146–153. | NG σ₀ 2.5 S cm⁻¹ 의 출처 (시뮬레이션 논문) — 그 값의 성격 확인 | 없음 |
| [31] P. Goharian, A. Aghaei, B.E. Yekta, S. Banijamali, Ionic conductivity and microstructural evaluation of Li2O–TiO2–P2O5–SiO2 glass-ceramics, Ceram. Int. 41 (2015) 1757–1763. · [32] W. Li, M. Wang, Z. Li, X. Shang, H. Wang, Y. Wang, Y. Xu, Synthesis and characterization of inorganic solid electrolytes of Li 2 O-SiO 2-P 2 O 5 and Li 2 O-TiO 2-SiO 2-P 2 O 5 systems, Russ. J. Electrochem. 43 (2007) 1279–1283. | LSTP σ₀ 9.9×10⁻⁴ 의 출처 — 값 · 시료 형태 · 온도 확인 | 없음 |
| [28] F. Hegge, R. Moroni, P. Trinke, B. Bensmann, R. Hanke-Rauschenbach, S. Thiele, S. Vierrath, Three-dimensional microstructure analysis of a polymer electrolyte membrane water electrolyzer anode, J. Power Sources 393 (2018) 62–66. · [29] M. Klingele, R. Zengerle, S. Thiele, Quantification of artifacts in scanning electron microscopy tomography: improving the reliability of calculated transport parameters in energy applications such as fuel cell and battery electrodes, J. Power Sources 275 (2015) 852–859. | PoroDict · ConductoDict 인용 — ConductoDict 의 경계 · 솔버 관행 확인 후보 | 없음 |
| [35] Y. Kato, S. Shiotani, K. Morita, K. Suzuki, M. Hirayama, R. Kanno, All-solid-state batteries with thick electrode configurations, J. Phys. Chem. Lett. 9 (2018) 607–613. | ASSB P2D 구성 인용 [33–35] | 없음 (메모 v2 §8-2 목록에 있음) |
| [27] B.L. Trembacki, A.N. Mistry, D.R. Noble, M.E. Ferraro, P.P. Mukherjee, S.A. Roberts, Editors', choice—mesoscale analysis of conductive binder domain morphology in lithium-ion battery electrodes, J. Electrochem. Soc. 165 (2018) E725–E736. | "Added binder" 형상 규칙의 인용원 | 없음 (낮음) |
| (park2020 [12b]) J. Park, J. Y. Kim, D. O. Shin, J. Oh, J. Kim, M. J. Lee, Y.-G. Lee, M.-H. Ryou, Y. M. Lee, Chem. Eng. J. 2020, 391, 123528. | park2020 τ 원값 · σ₀ 의 남은 후보 (이 논문 목록에는 없음 — park2020 [12] 의 b) | 같은 inbox 5 번 — 카드 유무는 메인 확인 |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

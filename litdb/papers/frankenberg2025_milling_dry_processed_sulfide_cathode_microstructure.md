<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = kawaguchi2017_dry_coating_parametric_na2so4_model_se.md · nakamura2020_dry_coating_ncm_li3ps4_core_shell.md (같은 날 묶음).
     쪽 표기 = 본문 "p.N" (학술지 e07279 (N of 16) = PDF N 쪽) · SI "SI p.N" (SI PDF N 쪽).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 숫자 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 300 dpi 원본 래스터 · 표지 색 덩어리 중심 →
     축 · 정밀도는 파일 머리) · [우리 산술] = 인쇄값으로 우리가 다시 한 계산 · [추정] = 우리 해석 · [미확인] = 본문 16 쪽 + SI 9 쪽 전수에 없음.
     ⚠ 기호 충돌: 이 논문의 "SE" = stress energy (충돌 에너지) — 이 카드에서는 그것을 **E_col** 로 적고 "SE" 는 우리 뜻 (고체전해질) 으로만 쓴다.
     SF (stress frequency) → **f_col** · SN (stress number) → **N_col** · E_m (specific energy input) 은 그대로.
     원문 본문 16 쪽 · SI 9 쪽 텍스트 층 전수 + 그림 8 · SI 그림 12 · SI 표 6 = 크롭 26 장 전부 렌더로 열람. -->

# 유성 볼밀로 단결정 NCM83–LPSCl 복합양극을 만들 때 "얼마나 세게 · 얼마나 오래" 가 미세구조를 정한다 — 볼 DEM (Rocky 2024) 으로 충돌 에너지 E_col · 빈도 f_col · 비에너지 E_m 을 구하고 공정–구조–성능을 잇는다: 에너지 ↑ = LPSCl 분쇄 + NCM–LPSCl 융합 응집체 + 기공 ↓ → σ_ion ↑ · 용량 ↑ (E_m ≈ 500 ± 100 J/g 에서 ≈165 mAh/g) · 그 위는 LPSCl 결정자 축소 + NCM 격자 변형 → 용량 ↓ (4,700 J/g 에서 ≈90) · σ_e 는 LPSCl 분쇄로 전반적으로 ↓ · PTFE 3 wt% 건식 막 (30 mg/cm²) 은 덜 간 복합체를 부분적으로만 보상 — Frankenberg … Zeier · Janek · Kwade (TU Braunschweig · Gießen · Münster · Jülich, Small 2025)

> slug `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` · DOI `10.1002/smll.202507279` · type `exp + DEM (유성 볼밀 공정 매개변수 · 볼만 푼 Rocky DEM → E_col · f_col · E_m · PSD · FIB-SEM · μ-CT · 압분 기공 · DC 분극 σ_ion/σ_e · XRD Rietveld · 반쪽 셀 · PTFE 건식 막)` · PDF `8e444bcc-22._Tailoring_Composite_Microstructure_Through_Milling_for_Dry-Processed_Sulfide-Based_Solid-State_Battery_Cathodes.pdf` · SI `97805094-22._Sup_Tailoring_Composite_Microstructure_Through_Milling_for_Dry-Processed_Sulfide-Based_Solid-State_Battery_Cathodes.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Tailoring Composite Microstructure Through Milling for Dry-Processed Sulfide-Based Solid-State Battery Cathodes* (p.1)
> **저자 · 소속 (p.1 · SI p.1 같음)**: **Finn Frankenberg\*** · Carina A. Heck · Maximilian Kissel · Martin A. Lange · Vasiliki Faka · Alexander Diener · Philipp Haase · Peter Michalowski · Wolfgang G. Zeier · Jürgen Janek · Arno Kwade — TU Braunschweig Institute for Particle Technology (Frankenberg · Heck · Diener · Haase · Michalowski · Kwade) · JLU Gießen Institute of Physical Chemistry & Center for Materials Research (Kissel · Janek) · Universität Münster Institute of Inorganic and Analytical Chemistry (Faka · Zeier) · Forschungszentrum Jülich IMD-4 Helmholtz-Institut Münster (Lange · Zeier) (\* 교신 finn.frankenberg@tu-braunschweig.de)
> *Small* **2025**, 21, e07279 · 접수 2025-06-18 · 수정 2025-08-05 · 온라인 2025-09-05 (p.15) · 오픈 액세스 CC BY · 연구비 DFG (46247012 · 514726960) · 이해상충 없음 · 데이터 = 교신저자 요청 시 (p.15)
> **같은 그룹 · 같은 축 카드 (링크만)**: [`frankenberg2024_dem_high_intensity_mixer_assb`](frankenberg2024_dem_high_intensity_mixer_assb.md) (같은 1저자 · 같은 응력 모델 (E_col · f_col · E_m) 을 고강도 믹서 DEM 에 — 이 논문 ref 8) · [`kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable`](kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable.md) (같은 그룹 · 메카노퓨전 복합양극) · [`faka2026_particle_size_consolidation_strain_lpscl`](faka2026_particle_size_consolidation_strain_lpscl.md) (공저자 Faka · Lange · Zeier — LPSCl 입경 · 변형 · 압밀) · [`cronau2022_wet_milling_particle_size_ionic_conductivity`](cronau2022_wet_milling_particle_size_ionic_conductivity.md) (ref 26 — 밀링 손상이 σ 를 낮춘다) · [`schlautmann2023_se_particle_size_composite_transport`](schlautmann2023_se_particle_size_composite_transport.md) (ref 21 — 복합체 안 SE 입경) · [`lee2024_shear_force_dry_process_cathode_coverage`](lee2024_shear_force_dry_process_cathode_coverage.md) (ref 35 — 건식 공정 전단 · coverage) · [`kawaguchi2017_dry_coating_parametric_na2so4_model_se`](kawaguchi2017_dry_coating_parametric_na2so4_model_se.md) (ref 62 — 건식 충격 코팅 공정 창) · [`heck2026_densification_sulfide_se_binder_scalable`](heck2026_densification_sulfide_se_binder_scalable.md) (공저자 Heck — 바인더 SE 치밀화).
> **판독 원자료**: `litdb/figures/frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure/digitized.csv` (118 행 — Fig 5b 기공 · Fig 5d σ_ion · σ_e · Fig 6a 평균 방전 용량 · Fig 7d 율속 시험) · 크롭 26 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: NCM83 (단결정 · 1 차 3–5 µm) 70 wt% 와 굵은 LPSCl (x50 17 µm) 30 wt% (부피 50:50) 를 유성 볼밀 (Pulverisette 7 · 5 mm 볼 · 충전율 0.5 · 200–1000 rpm · 5–300 min) 로 갈면, 볼 DEM 이 주는 비에너지 **E_m = E_col · f_col · t / m** 이 커질수록 LPSCl 이 부서지고 NCM 과 **융합된 응집체**가 생겨 기공이 37.6 → 26.5 % 로 줄고 σ_ion 과 용량이 오르지만 (≈500 ± 100 J/g 에서 ≈165 mAh/g), 너무 세게 · 오래 갈면 LPSCl 결정자가 25 nm 아래로 줄고 NCM 격자 변형이 커져 용량이 떨어진다 (4,700 J/g 에서 ≈90) — 그리고 이 차이는 PTFE 건식 막으로 옮겨진 뒤에도 대부분 남는다 (p.1 · p.6–11).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 공정 변수 (장치 · 속도 · 시간 · 에너지 · 온도) | **Fritsch Pulverisette 7** · 해 바퀴 n = **200 · 400 · 600 · 800 · 1000 rpm** · 속도비 k = −n_MC/n = **−2** · 시간 **5 · 10 · 20 · 30 min** (200 rpm 은 **60 · 300 min** 추가 · 800 · 1000 rpm 은 **20 min 까지** — 발열 · LPSCl 열화) · 볼 **5 mm** (이트륨 보강) · 충전율 **φ = 0.5** · 한 통에 **NCM 12.25 g + LPSCl 5.25 g** (70:30 wt% = 50:50 vol%) · 아르곤 글러브박스 · 온도 측정 [미확인].  [우리 산술] E_m = **11 J/g (200 rpm 5 min) → 4,737 J/g (1000 rpm 20 min)** (§3-3) | [인쇄] p.12–13 · SI 표 S1 · [우리 산술] |
| ② 피복 · 코팅을 어떻게 쟀나 · 값 | **코팅은 없다** — *"This fusion process can also result in the NCM particles being coated with a thick layer of the solid electrolyte. Although this is not observed in the present case, as confirmed by the EDX images"* (p.9).  생기는 것 = **NCM–LPSCl 융합 응집체** (SEM 거짓 색 · FIB-SEM · EDS 정성) · 피복률 · 막 두께 정량 없음 | [인쇄] p.4 · p.9 · Fig 2 · 7b–c |
| ③ 코팅이 SE 를 얼마나 쓰나 | n/a (코팅 없음 · 조성 고정 70:30) | — |
| ④ σ_ion · σ_e · 기공 · 용량 | 기공 (380 MPa 압분) **0.376 → 0.265** · σ_ion **0.072 → 최대 0.155 mS/cm (600 rpm 10 min)** → 0.124 (1000 rpm 20 min) · σ_e **0.73 → 0.23 mS/cm** (중간 비단조) · 평균 방전 용량 (0.1C, 20 사이클, 2 셀) **110 → ≈164 → ≈90 mAh/g** · 정적 CAM 이용률 200 rpm 5 min = 600 rpm 10 min = **≈88 %** | [인쇄] p.6–7 · [판독] Fig 5b · 5d · 6a |
| ⑤ DEM · 모델 | **Rocky 2024 — 분체가 아니라 볼만 푼다** (분체 효과 = 분체 묻은 볼의 접촉 매개변수로 보정: 반발계수 0.15 · 구름마찰 0.045 · 동마찰 0.5 · 정마찰 0.55 · ρ 6.1 g/cm³ · E 210 GPa) · 1 s 모사 → 충돌당 평균 에너지 E_col · 빈도 f_col 분포 → E_m (Kwade 응력 모델) · 축척식 E_col ∝ n^2.3–2.6 · d^3.1–3.9 · f_col ∝ n^0.3–0.7 · d^−3.6–−4.2 (식 2–7) | [인쇄] p.4–6 · p.13 · SI 표 S1–S3 |
| ⑥ "같은 총 SE 에서 코팅 상태" 실험에 주는 것 | ★ **공정 에너지 자체가 교락 변수다** — 같은 조성에서 E_m 하나로 SE 입경 · 융합 응집 · 기공 · SE 결정자 · NCM 변형 · σ_ion · σ_e · 용량이 다 움직인다.  코팅 팔 · 비코팅 팔의 **공정 에너지 (E_m · E_col · N_col) 를 같이 적고**, SE 입경 · 결정자 (XRD) · NCM 변형을 함께 재야 "코팅 상태" 몫을 가를 수 있다 [추정] | [인쇄] p.6–9 · [추정] §7-3 |
| ⑦ PTFE 건식 막 | PTFE 3 wt% · 링 전단 믹서 5 min 5,000 rpm · 캘린더 8 kN · 100 °C · 속도차 60 % → 150 % · 30 mg/cm² · ε 0.3 — 섬유화 단계는 미리 간 구조를 거의 안 바꾼다 · 캘린더 전단이 이종 접촉을 늘려 CAM 이용률 88 → 96–99 % · 0.1C 165 / 180 mAh/g · 고율은 미리 간 구조가 정한다 | [인쇄] p.9–11 · p.14 · [판독] Fig 7d |

⛔ **한정어 (떼지 말 것)**: ① 공정 = **유성 볼밀 (고에너지 · 분쇄 + 소성 융합)** — 저전단 혼합 · 드럼 · 충격 코팅과 다른 영역 ② NCM = 단결정 NCM83 (MSE Supplies) · LPSCl = NEI "fine" (원료 x50 17 µm — **SE 가 NCM 보다 큰** 출발점) · 탄소 없음 ③ σ_ion · σ_e = DC 분극 (온도 · LPSCl 벌크 σ₀ **[미확인]**) — 조건 다섯 개만 · 기공과 같은 조건은 둘뿐 ④ 용량 = 2 셀 평균 · E_m 최적 창 "500 ± 100 J/g" 은 판독상 넓다 (§10-6) ⑤ DEM 은 **볼 운동**이지 전극 미세구조가 아니다 ⑥ 정량 피복 · 코팅 두께 없음.

---

## 1. 한 줄 요약

SSB 복합양극 연구가 소재에 몰려 있고 공정의 몫은 잘 모른다는 문제에서 출발해, 같은 그룹의 응력 모델 (충돌 한 번의 평균 에너지 E_col · 1 초당 충돌 수 f_col · 그 둘과 시간 · 질량으로 만든 비에너지 E_m, 식 1) 을 유성 볼밀에 적용한 논문.  볼을 분체 묻은 상태로 보정한 Rocky DEM 으로 속도 · 볼 크기 · 충전율별 E_col · f_col 표를 만들고 (SI 표 S1–S3 · 식 2–7), 200–1000 rpm · 5–300 min 으로 간 NCM83–LPSCl 복합체의 입도 · SEM · FIB-SEM · μ-CT · 압분 기공 · σ_ion · σ_e · XRD (결정자 · 변형) · 반쪽 셀 성능을 E_m 축 위에 올렸다.  E_m 이 커지면 굵은 LPSCl 이 부서지고 NCM 과 융합해 응집체가 되며 (Fig 2) 기공이 줄고 (Fig 5b) σ_ion 이 600 rpm 10 min 까지 오르고 (Fig 5d) 용량이 ≈500 J/g 근처에서 최대가 되지만 (Fig 6a), 그 위로는 LPSCl 결정자 축소 · NCM 격자 변형 · 첫 사이클 LPSCl 산화 · 응집체 균열로 떨어진다 (Fig 6 · SI S7 · S8).  최적 (600 rpm 10 min) 과 덜 간 (200 rpm 5 min) 복합체를 PTFE 3 wt% 건식 막 (30 mg/cm²) 으로 옮기면 캘린더 전단이 CAM 이용률을 올려 저율 용량을 끌어올리지만 고율 차이는 대부분 남는다 (Fig 7).  결론: 밀링은 재료 설계의 일부로 다뤄야 하고, 큰 장치로 옮길 때는 **E_col 을 같게 두고 시간으로 E_m 을 맞추라** (p.11).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (AM / SE / 바인더) | 연구유형 |
|---|---|---|---|---|
| F. Frankenberg\* · C. A. Heck · M. Kissel · M. A. Lange · V. Faka · A. Diener · P. Haase · P. Michalowski · W. G. Zeier · J. Janek · A. Kwade (TU-BS IPAT · JLU Gießen · Münster · FZJ IMD-4) | *Small* 21 (2025) e07279 | 10.1002/smll.202507279 | 단결정 LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂ (MSE Supplies) / Li₆PS₅Cl (NEI, fine) / PTFE (Daikin) 3 wt% (막만) · 탄소 없음 | 실험 + DEM (볼밀 볼 운동) — 공정–구조–성능 |

- 키워드 (p.15): chemical process engineering · DEM simulation · microstructure · process–structure–property · solid-state battery.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 장치 · 조건 (p.4 · p.12–13 · Fig 1)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| NCM | 단결정 NCM83 (MSE Supplies LLC) · 제조사 1 차 입경 **3–5 µm** · 측정 x50 **8 ± 2 µm** (= 원료 응집체) · 진밀도 **4.75 g/cm³** | [인쇄] p.4 · p.12 |
| LPSCl | Li₆PS₅Cl "fine" (NEI Corporation) · 측정 x50 **17 ± 2 µm** · 진밀도 **1.87 g/cm³** · 벌크 σ₀ **[미확인]** (서론의 일반값 *"1–10 mS cm−1"* 뿐) | [인쇄] p.1 · p.4 · p.12 |
| 장입 | 한 통에 NCM **12.25 g** + LPSCl **5.25 g** = 70:30 wt% = **50:50 vol%** · 볼 사이 채움 **33.7 %** (밀링 전에는 탭 밀도 때문에 ≈100 %) · 혼합 밀도 ρ₀ = **3.25 g/cm³** (식 10) | [인쇄] p.12–13 |
| [우리 산술] 장입 확인 | 12.25/4.75 = 2.579 cm³ · 5.25/1.87 = 2.807 cm³ → NCM 47.9 : LPSCl 52.1 vol% (≈50:50 ✓) · ρ₀ = 17.5 g / 5.386 cm³ = **3.249** (✓) | [우리 산술] |
| 장치 | 유성 볼밀 **Fritsch Pulverisette 7** · 해 바퀴 n · 통 회전 n_MC · k = −n_MC/n = **−2** · 이트륨 보강 볼 **5 mm** · 충전율 φ = **0.5** | [인쇄] p.12–13 |
| 조건 | n = 200 · 400 · 600 · 800 · 1000 rpm × 5 · 10 · 20 · 30 min (대부분) · 200 rpm 60 · 300 min 추가 (DEM 으로 최적 E_m 에 닿는 시간 계산) · 800 · 1000 rpm 은 20 min 까지 (*"strong heat development and degradation of the LPSCl"*) · 시료 채취 · 장입 = Ar 글러브박스 (H₂O · O₂ < 1 ppm) | [인쇄] p.7 · p.13 |

### 3-2. ★ 볼 DEM (p.4–6 · p.13 · Fig 3–4 · SI 표 S1–S3 · S10)

- **코드 · 범위**: Rocky 2024 · 200–1000 rpm 각 **1 s** 모사 · 0.5–1 s 구간의 볼별 평균 충돌 일률 P_i 와 충돌 빈도 c_i 를 **Δt = 0.5 ms** 마다 내보내 충돌당 평균 에너지 E_col = P_i / c_i (식 9 — 법선 · 전단 · 소산 몫) → E_col–f_col 곡선 → E_m [인쇄 p.13].
- **분체는 입자로 넣지 않는다** — 분체가 묻은 볼 (600 rpm 5 min 공정에서 꺼낸 것) 로 보정 [인쇄 p.13]:

| 매개변수 | 값 | 보정 방법 | 표지 |
|---|---|---|---|
| 반발계수 e_MB | **0.15** | 분체층 위 낙하 시험 20 회 (평균 층 높이 0.94 mm · 고속 카메라 v₂/v₁, 식 8) — e 는 층 높이에 강하게 걸린다 (SI Fig S10a: 층 0 mm ≈0.9 → 1.4 mm ≈0.1 [판독]) | [인쇄] p.13 |
| 구름마찰 μ_r | **0.045** | 분체 든 통 안 진자 운동 높이를 DEM 과 맞춤 | [인쇄] p.13 |
| 동마찰 μ_d | **0.5** | 같은 진자 시험 | [인쇄] p.13 |
| 정마찰 μ_s | **0.55** | 원통 들어올림 안식각 (볼 더미) | [인쇄] p.13 |
| 볼 밀도 · 영률 | **6.1 g/cm³ · 210 GPa** | 제조사 값 | [인쇄] p.13 |

- **운동 양식**: 200 rpm = 캐스케이딩 (볼이 벽을 따라 미끄러져 굴러내림) → 400–1000 rpm = 벽 구름 + **캐터랙팅** (볼이 벽에서 떨어져 날아감 — 반경 힘 F_r < 0) → 충돌 에너지 분포가 고르다가 넓어진다 (Fig 3) [인쇄 p.4–5].
- **축척식 (5 mm 기준 실험 외 크기 · 충전율로 옮기기 위함)** [인쇄 p.5 · 식 2–7]:

| φ | E_col ∝ | f_col ∝ |
|---|---|---|
| 0.1 | n^2.31 · d_MB^3.11 | n^0.71 · d_MB^−3.6 |
| 0.3 | n^2.39 · d_MB^3.86 | n^0.62 · d_MB^−4.21 |
| 0.5 | n^2.62 · d_MB^3.81 | n^0.29 · d_MB^−4.02 |

- **SI 표 S1 (φ = 0.5) 핵심 값** [인쇄 SI p.2]:

| n (rpm) | 5 mm E_col (J) | 5 mm f_col (s⁻¹) | 3 mm E_col | 3 mm f_col | 1.75 mm E_col | 1.75 mm f_col |
|---|---|---|---|---|---|---|
| 200 | 5.38478E-07 | 1232846 | 9.06932E-08 | 10135490 | 1.18E-08 | 89957880 |
| 400 | 3.25615E-06 | 1471680 | 4.63296E-07 | 10923396 | 6.24E-08 | 93135940 |
| 600 | 9.876E-06 | 1671156 | 1.29752E-06 | 12790754 | 1.67E-07 | 110175704 |
| 800 | 2.05545E-05 | 1990424 | 2.96358E-06 | 14166094 | 3.64E-07 | 124078208 |
| 1000 | 3.7592E-05 | 1837780 | 4.88483E-06 | 15534152 | 6.74E-07 | 139648252 |

- [우리 산술] 5 mm 의 E_col 은 200 → 1000 rpm 에 **×69.8** = n^2.64 (식 6 의 2.62 와 맞음) · f_col 은 **×1.49 이고 단조가 아니다** (800 rpm 1,990,424 > 1000 rpm 1,837,780) — 식 7 의 n^0.29 는 세 볼 크기를 묶은 맞춤.
- [우리 산술] 본문의 *"stress frequency being increased … by a factor of ≈4"* · *"stress energy … decreases by a factor of ≈3.8"* (p.5–6) 는 **배수가 아니라 d_MB 의 지수**다 — 실제 5 → 3 mm 한 단계 배수는 200 rpm 에서 f_col **×8.2** · E_col **÷5.9**, 1000 rpm 에서 ×8.5 · ÷7.7 (표 S1) · Fig 8 도 *"SF ∝ n^0.5 · d_MB^−4"* · *"SE ∝ n^2.5 · d_MB^3.8"* 로 적는다.
- 충전율 효과는 복잡 — 저속은 f_col 이 충전율과 함께 ↑, 800–1000 rpm 은 오르다 약간 ↓ (볼끼리 방해) · E_col 은 저속에서 충전율 ↑ → ↓, 고속은 0.3 까지 ↑ 뒤 0.5 에서 ↓ (SI Fig S4) [인쇄 p.6].

### 3-3. ★ 비에너지 E_m (식 1) — [우리 산술] SI 표 S1 (φ 0.5 · 5 mm) · m_total = 17.5 g (한 통)

E_m = E_col · f_col · t / m_total — 논문의 인쇄값 (*"Em = 10 J g−1 (200 rpm, 5 min)"* · *"≈45 J g−1 (200 rpm, 20 min)"* · *"4700 J g−1 (1000 rpm and 20 min)"*) 과 Fig 5 · 6 의 그림 속 x 위치 (판독) 를 **1 % 안에서** 다시 낸다 → 표의 행은 **해 바퀴 속도 n** 이다 (표 머리 "n_MC" 는 오기 — §10-3).

| n (rpm) | E_col·f_col (J/s) | 5 min | 10 min | 20 min | 30 min | 60 min | 300 min |
|---|---|---|---|---|---|---|---|
| 200 | 0.664 | 11.4 | 22.8 | 45.5 | 68.3 | 136.6 | 682.8 |
| 400 | 4.792 | 82.1 | 164.3 | 328.6 | 492.9 | — | — |
| 600 | 16.50 | 282.9 | 565.9 | 1,131.7 | 1,697.6 | — | — |
| 800 | 40.91 | 701.4 | 1,402.7 | 2,805.4 | — | — | — |
| 1000 | 69.09 | 1,184.3 | 2,368.7 | 4,737.3 | — | — | — |

(단위 J/g.  [우리 산술] 충돌 수 N_col = f_col · t: 200 rpm 300 min = 2.2 × 10¹⁰ · 800 rpm 5 min = 6.0 × 10⁸ · 1000 rpm 5 min = 5.5 × 10⁸ — SI Fig S7b 의 x 위치와 맞음.)

### 3-4. ★ 미세구조 — 분쇄 · 융합 응집 · 기공 (p.4 · p.6 · Fig 2 · 5a–c · SI S1 · S2)

- **200 rpm**: NCM 1 차 입자 + **굵은 LPSCl** (FIB-SEM 에서 ≈30 µm = 원료 크기) · 분쇄 · 응집 거의 없음 · 레이저 x50 은 처음 **≈44 µm** 까지 커졌다가 (LPSCl 끼리 · NCM 과 뭉침) 해체로 다시 준다 [인쇄 p.4 · p.6].
- **600 rpm**: 분쇄된 LPSCl ↑ + **NCM–LPSCl 응집체** 등장 · 순수 상도 남음 → 입도 분포 **쌍봉** (400 rpm 에서도 일부) [인쇄 p.4].
- **1000 rpm**: 대부분 응집체 · 굵은 LPSCl 거의 없음 · 입도 안정 [인쇄 p.4].
- 기전 서술: LPSCl 이 무르므로 (*"low hardness"*, ref 43 · 44) NCM 과 **융합 (fuse)** — 레이저 회절은 분쇄 · 응집을 섞어 재므로 LPSCl 분쇄 추적에 부적합하다고 저자 스스로 적음 [인쇄 p.4].
- 입도 vs E_m: ≈45 J/g 넘으면 x50 이 지수적으로 감소 → **≈10 µm** (4,700 J/g) · 낮은 E_col (200 · 400 rpm) = 넓은 분포 (굵은 LPSCl 이 덜 부서지고 *"tend to agglomerate due to low-energetic collisions, forming large and uneven agglomerates"*) · 높은 E_col (600–1000 rpm) = 균일한 응집체 · 좁은 분포 [인쇄 p.6].
- **기공 (380 MPa · 1 min · 100 mg 압분 · 높이 · 무게 → 식 10)** [판독 Fig 5b · 인쇄 p.6 *"from 37.6% to 26.5%"*]:

| 조건 | E_m (J/g) | 기공 |
|---|---|---|
| 200 rpm 30 min | 68 | **0.376** |
| 400 rpm 30 min | 493 | 0.285 |
| 600 rpm 30 min | 1,698 | 0.284 |
| 800 rpm 20 min | 2,805 | 0.266 |
| 1000 rpm 20 min | 4,737 | **0.265** |

- μ-CT (0.5992 µm 화소): 200 rpm 30 min 은 큰 공극이 많고 800 rpm 20 min 은 균일 (Fig 5c 정성) [인쇄 p.6 · p.13].

### 3-5. ★ 유효 전도도 (Fig 5d · p.6) [판독 · 정밀도 σ_ion ±0.0005 · σ_e ±0.002 mS/cm]

| 조건 | E_m (J/g) | σ_ion (mS/cm) | σ_e (mS/cm) |
|---|---|---|---|
| 200 rpm 30 min | 68 | 0.072 | **0.73** |
| 400 rpm 20 min | 329 | 0.104 | 0.39 |
| 600 rpm 10 min | 566 | **0.155** | 0.49 |
| 800 rpm 5 min | 701 | 0.093 | 0.36 |
| 1000 rpm 20 min | 4,737 | 0.124 | 0.23 |

- 측정 (p.14): σ_ion = In/InLi | LPSCl | 복합체 80 mg | LPSCl | In/InLi (전자 차단) · σ_e = 강철 | 복합체 80 mg | 강철 (이온 차단) — 380 MPa 3 min 치밀화 → Al 틀 **50 MPa** · 6 h 대기 → PEIS 7 MHz–10 mHz (10 mV) → **DC 1–50 mV 각 1 h** · 평형 전류로 I–U 직선 (Ohm) · LPSCl 층 저항 빼고 기하 보정 [인쇄].
- 저자 해석: σ_ion 은 LPSCl 분쇄 · 기공 ↓ 로 600 rpm 10 min 까지 ↑ 뒤 결정자 축소 · 열화로 ↓ · 800 rpm (5 min) 은 충돌 수가 적고 배열이 덜 잡혀 더 낮다 · σ_e 는 *"decreases continuously"* — 절연 LPSCl 분쇄가 NCM 전자 경로를 끊는다 [인쇄 p.6].
- ⚠ [판독] σ_e 는 **엄밀히 단조가 아니다** — 600 rpm 10 min (0.49) > 400 rpm 20 min (0.39) (§10-5).

### 3-6. ★ 셀 성능 vs E_m (Fig 6a · p.6–8) [판독 · ±1 mAh/g · 2 셀 × 20 사이클 0.1C/0.1C 평균]

| n \ t | 5 min | 10 min | 20 min | 30 min | 60 min | 300 min |
|---|---|---|---|---|---|---|
| 200 rpm | **110** (11 J/g) | 123 (23) | 139 (46) | 143 (68) | 158 (137) | 148 (683) |
| 400 rpm | 127 (82) | 151 (164) | 153 (329) | **164** (493) | — | — |
| 600 rpm | 145 (283) | **164** (566) | 144 (1,132) | ≈134 (1,698 · 표지가 반쯤 가려짐 ±2) | — | — |
| 800 rpm | 156 (701) | 137 (1,403) | 136 (2,805) | — | — | — |
| 1000 rpm | 160 (1,184) | 127 (2,369) | **90** (4,737) | — | — | — |

- 인쇄값: 110 mAh/g (10 J/g) → *"≈165 mAh g−1 after an energy input of ≈500 ± 100 J g−1"* (600 rpm 10 min · 400 rpm 30 min — SI Fig S5 에서 둘이 거의 같다: 정적 CAM 이용률 87.7 · 88.1 %) · 1000 rpm 20 min **≈90** · > 1000 J/g 에서 열화 [인쇄 p.6–8 · SI p.4].
- 200 rpm 5 min 과 600 rpm 10 min 의 **정적 CAM 이용률은 둘 다 ≈88 %** (이론 200 mAh/g 이면 176 상당) — 그런데 0.1C 용량이 110 vs 165 = **동역학 제한** (dQ/dU 과전압이 200 rpm 에서 크다, Fig 6b) + 낮은 σ_ion [인쇄 p.7].
- 열화 근거: 높은 E_m · E_col 복합체는 첫 충전 **낮은 전압에서 전하** (Fig 6b 에서 800 · 1000 rpm 20 min 곡선이 ≈1.7–2.8 V 부터 뜬다 [판독]) — LPSCl 산화 (refs 52 · 53) · 첫 사이클에 가장 크고 이후 안정 · 충방전 곡선 평탄화 = 활물질 일부 비활성 [인쇄 p.8].
- 사후 분석 (1000 rpm 20 min): dQ/dU 열화 20 사이클에서 더 큼 · 라만 피크 폭 FWHM **14.6 (순수 LPSCl) → 15.8 (복합체) → 18.9 (1 사이클 뒤)** [인쇄 — SI Fig S8c 그림 안 · 단위 표기 없음] · **응집체 안 균열** 1 사이클 뒤 · 20 사이클 뒤 전면 균열 (부피 변화 수용 부족 → 접촉 상실) [인쇄 p.9].
- 저자들이 그린 세 영역 (Fig 6a 아래 띠): *Large LPSCl particles* → *Optimized microstructure* → *Structural disorder*.

### 3-7. ★ XRD — LPSCl 결정자 · NCM 변형 (SI 표 S6 · Fig 6c–d · p.8–9) [인쇄 SI p.9]

| n (rpm) | t (min) | e₀(NCM) (%) | e₀(LPSCl) (%) | L_Vol(LPSCl) (nm) | R_wp | GoF |
|---|---|---|---|---|---|---|
| 200 | 30 | 0.0427(5) | 0.026(9) | 178(17) | 4.8 | 2.2 |
| 200 | 60 | 0.0417(5) | 0.03(9) | 137(12) | 4.0 | 2.1 |
| 200 | 300 | 0.0608(7) | 0.05(1) | 78(17) | 4.5 | 2.6 |
| 400 | 20 | 0.0487(1) | 0.05(1) | 86(17) | 4.5 | 2.5 |
| 400 | 30 | 0.0537(2) | 0.0004(9) | 37(13) | 7.3 | 1.1 |
| 600 | 10 | 0.062(8) | 0.05(2) | 58(17) | 4.6 | 2.3 |
| 800 | 5 | 0.0434(1) | 0.04(1) | 99(12) | 4.1 | 2.2 |
| 800 | 10 | 0.076(8) | 0.004(9) | 27(13) | 5.2 | 2.6 |
| 800 | 20 | 0.14(4) | 0.0004(9) | 16(8) | 6.0 | 3.1 |
| 1000 | 5 | 0.0437(1) | 0.04(2) | 76(16) | 4.9 | 3.6 |
| 1000 | 10 | 0.11(3) | 0.0004(9) | 17(7) | 6.6 | 1.4 |
| 1000 | 20 | 0.12(4) | 0.0005(8) | 12(6) | 6.6 | 3.3 |

- LPSCl 결정자 (적분 폭 L_Vol) 는 E_m 과 함께 ↓ · NCM 미세 변형 e₀ 는 ↑ · NCM 은 결정자 축소 넓어짐이 없어 L_Vol 없음 [인쇄 SI p.9 · p.9].
- 예외: 800 · 1000 rpm **5 min** 은 E_m 이 커도 NCM 변형이 안 늘었다 (충돌 수가 적어서) · 200 rpm 300 min 은 충돌 수가 가장 많아도 변형이 작다 (E_col 이 작아서) ⇒ *"not only the total energy input, but also its individual components, stress number, and stress energy, must be considered separately"* [인쇄 p.9].
- 결론 (Fig 6d): NCM 변형은 줄이고, LPSCl 결정자는 **35–40 nm** 까지 줄이는 쪽이 최고 용량 · **25 nm 아래** 는 용량 하락의 한 원인 [인쇄 p.9].
- 큰 장치로 옮길 때: **E_col 을 이 연구와 같게** 두고 (LPSCl 결정성 · NCM 변형을 정하는 결정 변수) 시간으로 N_col → E_m 을 맞추라 [인쇄 p.11].

### 3-8. ★ PTFE 건식 막 (Fig 7 · p.9–11 · p.14 · SI S9 · S12)

- **공정** [인쇄 p.14]: 미리 간 70:30 복합체 + **PTFE 3 wt%** (Daikin) → **고강도 링 전단 믹서 (Hosokawa Alpine) 5 min · 5,000 rpm** (예비 섬유화) → 2 롤 캘린더 (Saueressig GK300L) **힘 제어 8 kN · 0.5 m/min · 롤 100 °C · 둘째 롤 60 % 속도 (0.3 m/min)** → 자립 막을 **150 % 속도차 (0.75 m/min)** 로 다시 캘린더 → 탄소 코팅 Al (En'safe 91) 에 0.1 m/min 로 붙임 · 건조실 20 °C · RH < 0.1 % · 이슬점 −60 °C.
- 막: 질량 로딩 **30 mg/cm²** (분체 셀의 1.5 배) · 기공 **ε = 0.3** (혼합 밀도 3.20 g/cm³ — PTFE 포함) — 두 막 같음 [인쇄 p.9 · p.13].
- 단면 (EDS): 200 rpm 5 min 막 = LPSCl · NCM 1 차 입자 그대로 · 600 rpm 10 min 막 = 융합 응집체 — 두꺼운 SE 코팅은 **관찰되지 않음** · 코팅을 만들면 NCM 을 전자망에서 가리지 않도록 **도전재가 필요**하다고 적음 [인쇄 p.9].
- 섬유화 단계: 미리 간 구조를 거의 안 바꾼다 (FIB-SEM 같은 입자 종 · 형태 + 성능 차 작음) · 바인더 첨가로 용량이 약간 안정 [인쇄 p.11].
- 율속 시험 (Fig 7d) [판독 · 단계 평균 · ±1 mAh/g]:

| 단계 | 미리 간 조건 | 0.1C | 0.3C | 1C | 0.1C 복귀 |
|---|---|---|---|---|---|
| 미리 간 복합체 (분체 셀) | 200 rpm 5 min | 125 | 84 | 28 | 120 |
| 〃 | 600 rpm 10 min | 161 | 129 | 68 | 158 |
| 섬유화 혼합물 (+PTFE) | 200 rpm 5 min | 127 | 91 | 33 | 124 |
| 〃 | 600 rpm 10 min | 160 | 126 | 64 | 158 |
| 건식 막 (30 mg/cm²) | 200 rpm 5 min | 166 | 122 | 38 | 168 |
| 〃 | 600 rpm 10 min | 181 | 149 | 66 | 182 |

- 인쇄값: 건식 막 CAM 이용률 **88 → ≈99 %** (200 rpm 5 min 기반) · **96 %** (600 rpm 10 min 기반) · 저율 용량 **180 / 165 mAh/g** · 60 사이클 0.1C 유지율 **94 % (600 rpm) vs 97 % (200 rpm)** — 이종 접촉이 많을수록 계면 열화가 커질 수 있다는 해석 · 막 기공 ≈30 % 가 고율 한계 → 더 치밀화 필요 [인쇄 p.11 · Fig 7f].
- 해석: 캘린더 좁은 틈의 **전단**이 입자를 눌러 새 NCM–LPSCl 이종 접촉 → 더 많은 NCM 이 이온망에 들어감 (dQ/dU 과전압 ↓, 특히 200 rpm 기반 막) · 그러나 굵은 LPSCl 이 남고 (SI S9) 미리 간 구조가 크게 안 바뀌므로 *"a comparable tortuosity … i.e., a similar secondary degree of mixing"* → 고율 차이는 그대로 [인쇄 p.11 — tortuosity 는 재지 않은 서술].

### 3-9. 셀 · 측정 조건 (p.13–14 · SI S12)

- 셀: LPSCl 80 mg 380 MPa 1 min → 복합체 **15 mg** 380 MPa 1 min → In · Li 9 mm → 셀 프레스 **≈80 MPa** · **2.2–3.7 V vs In/InLi · 25 °C** · 율속 0.1/0.3/1C · 20 사이클 0.1C · 조건마다 셀 ≥ 2 [인쇄 p.14].
- 활물질 질량 = Kissel (ref 31) 방식 — 액체 코인셀 (PVDF:CB:NCM 3:2:95, 0.02C) 기준과 맞춘 정적 이용률 [인쇄 p.14 · SI Fig S12b].
- XRD: Mo Kα₁ (70.930 pm) · 4–70° · 0.015° · 90 s/스텝 · 5 회 합 · TOPAS 7.25 · LaB₆ 기기 폭 · Balzar 크기 · 변형 [인쇄 p.14].
- SEM Phenom XL (건조실 이슬점 −27 °C · 사내 particleOS.ai 입자 검출) · FIB-SEM Xe 플라스마 (TESCAN · 380 MPa 압분) · 막 단면 = −100 °C 3 빔 Ar 이온 연마 + GeminiSEM 560 · EDS AzTec [인쇄 p.13].

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
원료 (NCM 8 µm 응집 · LPSCl 17 µm) → 유성 볼밀 (n × t, 5 mm, φ 0.5) → (i) SEM (거짓 색 분할) · 레이저 PSD (p-자일렌, LPSCl 굴절률) (ii) 380 MPa 압분 → FIB-SEM · μ-CT · 기공 (iii) 전자/이온 차단 셀 DC 분극 → σ_e · σ_ion (iv) XRD Rietveld → L_Vol(LPSCl) · e₀(NCM) (v) 반쪽 셀 → 평균 방전 용량 · dQ/dU · 정적 CAM 이용률 (vi) 라만 · 사후 SEM.  병행: 볼 DEM → E_col · f_col → E_m (모든 조건을 하나의 x 축으로).  그다음 두 조건 (200/5 · 600/10) 만 PTFE 건식 막으로.

### 4-2. ★ 입자 처리 (우리 축 언어로)
- **실험**: SE (LPSCl) 는 **진짜 분쇄 + 소성 융합** (NCM 과 붙어 응집체) · NCM 은 원료 응집 해체 + 고에너지에서 **격자 변형** (깨짐은 정성 언급) · 결정자 축소는 SE 의 입계 증가.  모두 **입자 형상 · 내부 상태의 변화** — 접촉 법칙 수준이 아니다.
- **DEM**: 볼 (5 mm 강체 구) 만 · 분체는 볼 접촉 매개변수 (e · μ_r · μ_d · μ_s) 안에 묻힘 — 분체 입자도 미세구조도 없다 ⇒ DEM 의 역할은 **공정 강도 지표 (E_col · f_col)** 를 주는 것뿐.
- **우리 대응**: 우리 믹서 DEM (저-Fr 회전 드럼 · CED 점착 · 강체 구) 과 압축 DEM (강체 구 · 연화 E · 겹침 δ) 에는 **분쇄 · 융합 · 결정자 축소 · 격자 변형이 없다** ⇒ 이 논문의 미세구조 변화는 우리 모델에서 **입력** (SE 크기 · 응집 상태) 이지 결과가 아니다.

### 4-3. 기법 미니 용어집
- **E_col (논문 SE, stress energy)**: 볼–볼 · 볼–벽 충돌 한 번에 소산되는 평균 에너지 (J) — 충돌 세기.
- **f_col (논문 SF, stress frequency)**: 1 초당 충돌 수 (s⁻¹).  **N_col (SN)** = f_col · t.  **응력 강도 SI** = E_col / 갇힌 질량 (J/kg — 이 논문은 갇힌 질량이 같다고 보고 E_col 로 대신).
- **E_m (specific energy input)**: E_col · f_col · t / m_total (J/g) — 전체 투입 에너지.  ⚠ 같은 E_m 이라도 E_col (세기) · N_col (횟수) 배분이 다르면 결과가 다르다 (§3-7).
- **캐스케이딩 / 캐터랙팅**: 볼이 벽을 타고 굴러내림 / 벽에서 떨어져 날아가 부딪힘.
- **이종 접촉 (heterocontact)**: NCM–SE 접촉.  **2 차 혼합도 (secondary degree of mixing, ref 31)**: 응집체 수준의 혼합 상태.
- **정적 CAM 이용률**: 아주 느린 조건에서 전기화학적으로 닿는 활물질 몫 (동역학 미포함).
- **L_Vol · e₀**: Rietveld (Balzar) 의 부피 가중 결정자 크기 · 미세 변형.
- **링 전단 믹서**: 고속 회전 링 틈에서 전단으로 PTFE 를 섬유화하는 혼합기.  **속도차 캘린더**: 두 롤 속도를 달리해 막에 전단을 거는 압연.

---

## 5. Figure set ★ (크롭 26 장 = `litdb/figures/frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) 원료 NCM · LPSCl SEM (b) 유성 볼밀 모식 (n · n_MC · t · d_MB · φ · k = −2) | 원료 크기 관계 (SE > NCM) 확인 |
| 2 | (a) 200 · 600 · 1000 rpm 20 min SEM (거짓 색: 노랑 = LPSCl · 분홍 = 응집체) (b) 속도별 PSD (c) FIB-SEM (200/30 · 600/10 · 1000/20) | ★ 에너지에 따른 "SE 따로 ↔ 이종 응집" 상태 지도 (정성) |
| 3 | (a) 속도별 E_col–f_col 분포 (5 mm · φ 0.5) (b) 볼 운동 양식 | 공정 강도 스펙트럼 — 우리 믹서 DEM 에서 같은 양을 뽑는 본보기 |
| 4 | 볼 크기 효과: (a) f_col (b) E_col (⚠ 세로축 단위 오기 §10-4) | 축척 규칙 |
| 5 | (a) 입도 vs E_m (b) 압분 기공 vs E_m (c) μ-CT (d) σ_ion · σ_e vs E_m + 측정 셀 모식 | ★ 기공 · σ 원자료 (판독) |
| 6 | (a) 평균 방전 용량 vs E_m (세 영역) (b) 첫 사이클 dQ/dU (c) NCM 변형 · LPSCl 결정자 vs E_m (d) 용량 지도 (결정자 × 변형) | ★ 최적 창 · 열화 축 |
| 7 | (a) 섬유화 · 건식 막 공정 (b · c) 막 단면 EDS (d) 율속: 분체 → 섬유화 → 막 (e) dQ/dU (f) 60 사이클 | ★ 미리 간 구조가 건식 막에서 살아남는다 |
| 8 | 공정–구조–성능 요약 (기호 정의 표) | 용어 정의 |
| S1 | 400 · 800 rpm PSD + SEM | 쌍봉 |
| S2 | 600 rpm 10 min 압분 윗면 SEM (LPSCl · NCM · 응집체 표지) | 순수 상이 남는다 |
| S3 · S4 | 속도 · 충전율에 따른 f_col · E_col (볼 크기 셋) | 축척 |
| S5 | 600/10 vs 400/30 상세 비교 (사이클 · 곡선 · CAM 이용률 87.7 · 88.1 % · dQ/dU · 율속) | 같은 E_m = 같은 성능 사례 |
| S6 | 다섯 조건 20 사이클 dQ/dU | 첫 사이클 산화 |
| S7 | (a) XRD 패턴 (b) N_col 대 변형 · 결정자 | 세기 vs 횟수 |
| S8 | 1000 rpm 20 min 사후: dQ/dU · 라만 FWHM · SEM 균열 | 열화 증거 |
| S9 | 건식 막 단면 SEM (PTFE 섬유 · 굵은 LPSCl) | 막 안 구조 |
| S10 | 볼 보정: 낙하 (e vs 층 높이) · 구름 진자 · 안식각 | ★ DEM 보정 절차 본보기 |
| S11 | Rietveld 예 (400 rpm 20 min) | — |
| S12 | (a) 셀 구조 (b) 활물질 질량 결정 곡선 | — |
| 표 S1–S3 | φ 0.5 · 0.3 · 0.1 × 볼 1.75 · 3 · 5 mm × 속도 다섯의 E_col · f_col | ★ E_m 다시 계산 원자료 (§3-3) |
| 표 S4–S6 | Rietveld 모델 · 정제값 · 결정자 · 변형 | §3-7 |

## 6. Post-processing ★
- **무엇을**: PSD (x10 · x50 · x90) · 기공 (기하 밀도 / 혼합 밀도) · DC 분극 (I–U 직선, LPSCl 층 저항 빼기) · Rietveld (Balzar) · dQ/dU · 정적 CAM 이용률 (Python 도구) · DEM 충돌 자료 → E_col–f_col → E_m · 거짓 색 SEM 분할 (사내 도구).
- **안 한 것**: 피복률 · 접촉 면적 · tortuosity 측정 (서술만) · 같은 조건의 기공 ↔ σ 짝 (둘뿐) · LPSCl 벌크 σ₀ · 측정 온도 · 오차 막대 (σ 는 단일 값) · 미세구조 시뮬레이션.
- **우리 후처리 (이 카드)**: E_m 전 조건 재계산 (SI 표 S1) 과 그림 x 위치 대조 (1 % 안) · Fig 5b · 5d · 6a · 7d 표지 판독 (118 행) · E_col 지수 · 배수 확인 · ps45 와 조건부 대조 (§7-1).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 `docs/data/` 출처를 병기해 적는다)

### 7-1. 비교표

| 항목 | 이 논문 | 우리 (ps45 침대 · 메인 리포 `docs/data/ps45_r45_network_g2_20261007/README.md` · `docs/data/ps45_sigmae_factor_off_20261013/README.md`) | 같음 / 다름 · 왜 |
|---|---|---|---|
| 조성 | NCM83 70 : LPSCl 30 wt% (50:50 vol) | NCM 81.6 : LPSCl 18.4 wt% (SE ≈ 35 vol% of solid [우리 산술 φ_SE / (1 − ε)]) | 이 논문이 SE 가 더 많다 |
| 입경 | NCM 1 차 3–5 µm (x50 8) · LPSCl 17 µm → 갈수록 ≈10 µm 응집체 | PC 9 · SC 4 · LPSCl 1 µm (강체 구) | 우리 SE 는 처음부터 작다 — 이 논문의 "많이 간" 쪽에 가깝다 [추정] |
| 압력 | 380 MPa (펠릿) · 셀 ≈80 MPa · 측정 셀 50 MPa | 300 MPa (DEM 성형) | 비슷 |
| 기공 | 0.265–0.376 (기하 밀도) | ε_sphere 0.150–0.192 · union 0.165–0.206 | ⛔ 이 논문 쪽이 SE 가 많은데도 기공이 크다 — 굵은 LPSCl · 응집체 · 기하 밀도 방식 (가장자리 포함) 이 겹친 결과 [추정] · 1:1 비교 아님 |
| σ_ion | 0.072–0.155 mS/cm (DC · σ₀ [미확인]) | Hertz 0.0587–0.0893 · Tabor 0.103–0.162 mS/cm (σ₀ = 1.5 mS/cm 보고 기준) | 같은 자릿수 — 우리 README 가 이미 같은 그룹 Minnmann 2021 (73 wt% · 380 MPa 0.17) 과 자릿수 정합을 적었다 |
| f · 수송 tortuosity (tau2) | 원문 계산 없음 · [우리 산술 · σ₀ = 1.5 은 **우리 보고 기준이지 원문 값 아님**] 기공과 짝이 맞는 두 조건만: 200/30 φ_SE = 0.5·(1 − 0.376) = 0.312 · f = 0.072/1.5 = 0.048 → tau2 ≈ 6.5 · 1000/20 φ_SE = 0.368 · f = 0.083 → tau2 ≈ 4.5 | Hertz tau2 7.24–5.03 (f 0.039–0.060) | 같은 범위 — 단 밀링으로 σ₀ 가 내려갔다면 (결정자 12 nm) 1000/20 의 실제 tau2 는 이보다 작다 · 50:50 vol 이 압분 뒤에도 유지된다고 가정 |
| σ_e | 0.23–0.73 mS/cm (탄소 없음 · NCM83) | 0.375–0.467 mS/cm (Hertz H0 · PC 인자 끔 · σ_AM 4.1 mS/cm 기준) | 같은 자릿수 — 이 논문은 NCM 부피가 더 적은데 (50 vs ≈65 %) 비슷하거나 높다 → NCM83 고유 σ · 접촉 차이일 수 있으나 가를 수 없다 [추정] |
| 에너지 축 | E_m 11–4,737 J/g 가 σ_ion · σ_e · 용량을 움직인다 | 우리 침대에는 공정 에너지 축이 없다 (혼합 DEM 은 별도 · 압축 DEM 입력은 고정 크기 구) | 우리에게 없는 축 |
| DEM 역할 | 볼만 · 공정 강도 지표 | 입자 접촉망 · 수송 | 같은 "DEM" 이 다른 반쪽 |

### 7-2. 이종기술 논지 (`docs/hetero_thesis.md` 비준 블록 2026-10-05) 와의 관계
- 논지 P1 (비코팅 침대는 혼합 시간을 늘려도 SE–SE 응집이 무작위보다 크게 남는다) 의 **실험 쪽 정성 단서**: 낮은 E_col (200 · 400 rpm) 에서 굵은 LPSCl 이 *"tend to agglomerate due to low-energetic collisions, forming large and uneven agglomerates"* · 200 rpm 에서 x50 이 ≈44 µm 까지 커진다 · 600 rpm 에서도 순수 LPSCl 상이 남아 PSD 가 쌍봉 (p.4 · p.6).  ⚠ 그러나 **같은 축이 아니다** — 여기 응집 해체 · 이종 응집은 **분쇄 + 소성 융합** (고에너지) 이 만들고, 논지는 **표면 에너지 차 × 크기** (저에너지 혼합) 를 말한다.  게다가 원료 SE (17 µm) 가 NCM 보다 커서 우리 모델 (SE 1 µm) 과 크기 관계가 반대다.  P1 의 증거로 쓰지 않는다 [추정].
- 논지 P2 (코팅하면 응집이 사라진다): 이 논문은 코팅을 만들지 않았다 (p.9) — 시험하지 않음.
- 논지 P3 (혼합 상태 차이 → 압축 뒤 SE 경로 차이): **방향은 같다** — 이종 응집 · 분쇄가 늘수록 σ_ion ↑ (600/10 까지).  그러나 같은 E_m 이 기공 (0.376 → 0.285) · SE 입경 · 결정자를 함께 바꾸므로 "혼합 상태" 몫을 가를 수 없다.
- 논지의 "하지 않는 말" (계면 면적 · 보호막) 과의 거리: 이 논문 설명 축 = 이종 접촉 수 · 기공 · 결정자 · 변형 · 첫 사이클 산화 — 이종 접촉이 많을수록 계면 열화도 클 수 있다는 해석 (60 사이클 94 vs 97 %) 까지 포함.  이온 경로 (σ_ion) 몫만 빌린다.

### 7-3. ★ "같은 총 SE 에서 코팅 상태" 실험 (`docs/mixer_paper_pipeline_draft_20261013.md` V1 · V2 · V3) 에 주는 것
1. **공정 에너지를 같이 적는다** — 코팅 팔 (메카노퓨전 · 충격 코팅) 과 비코팅 팔 (단순 혼합) 은 들어가는 기계 에너지가 다르다.  이 논문에서 E_m 하나가 SE 입경 · 응집 · 기공 · SE 결정자 · NCM 변형 · σ 를 다 바꿨다 ⇒ 각 팔의 E_m (또는 장치별 등가 지표) · E_col · 처리 시간을 기록하고 XRD 결정자 · 변형, 세척 · 분리 뒤 입도를 함께 잰다 [추정].
2. **"같은 E_m = 같은 결과" 가 아니다** — 세기 (E_col) 와 횟수 (N_col) 가 따로 작용한다 (§3-7) ⇒ V2 (혼합 시간) 를 늘리는 것과 세기를 올리는 것을 같은 축으로 두지 않는다.
3. **미리 만든 혼합 · 코팅 상태는 PTFE 섬유화를 거의 그대로 통과한다** (p.11) — 우리 건식 후막 바이모달 계획에서 "혼합 상태가 막까지 전달된다" 는 가정의 실험 근거 한 개 (단 이 논문 조건: 링 전단 5 min · 3 wt%).  캘린더 전단은 저율 이용률을 올리지만 (88 → 96–99 %) 고율 차이는 남는다.
4. **코팅하면 도전재가 필요** — 저자들도 SE 코팅이 NCM 을 전자망에서 가린다고 적는다 (p.9) · σ_e 가 SE 분쇄만으로도 0.73 → 0.23 으로 떨어졌다 ⇒ 코팅 팔 · 비코팅 팔의 σ_e 차이를 함께 재고, 탄소 유무를 맞춘다 (Kawaguchi 2017 의 R_inc · Nakamura 2020 의 σ_e −94 % 와 같은 축).
5. **SE 원료 크기**: 굵은 SE (17 µm) 로 시작하면 혼합 단계가 분쇄를 겸한다 — 실험 SE 의 D50 을 먼저 정해야 모델 침대 (SE 1 µm) 와 맞는다 (`docs/symmetric_cell_ionic_plan_20261013.md` 의 *"실험 분말의 D50 이 다르면 알려 주시면"* 과 같은 요청).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 공정 → 구조 (실험) · 공정 강도 (볼 DEM) · 구조 → 성능 (실험).
- **없는 것**: 미세구조를 푸는 모델 (입자 · 접촉망 · 복셀) — 그래서 σ_ion 변화의 몫 (기공 · 경로 · 결정자 · 접촉) 을 가를 수 없다.  ⇒ 우리 압축 DEM + 접촉망 (수송) · MPM (소성 형상) 이 채울 수 있는 자리가 바로 그 몫 가르기다 [추정] — 단 우리 모델은 분쇄 · 융합 · 결정자 축소를 입력으로만 받는다.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. 공정 에너지는 숨은 공변량이다.**
- 논문: 같은 70:30 조성에서 E_m 11 → 4,737 J/g 만으로 기공 0.376 → 0.265 · σ_ion 0.072 → 0.155 → 0.124 · σ_e 0.73 → 0.23 · 용량 110 → 164 → 90.
- 뜻: 우리 계획의 코팅 · 비코팅 비교에서 공정이 다르면 이 모든 축이 같이 움직인다.
- 할 일: 실험 담당과 조건을 정할 때 (파이프라인 Q4) 장치 · 속도 · 시간 · 볼 (있다면) 을 적고, XRD 결정자 · 변형과 기공을 결과 전 측정 항목에 넣는다.

**8-2. 우리 믹서 DEM 에서 "충돌 에너지 스펙트럼" 을 뽑을 수 있다.**
- 논문: 볼 충돌 자료 → E_col–f_col 곡선 (Fig 3a) → E_m — 같은 1저자의 고강도 믹서 DEM 카드도 같은 틀.
- 뜻: 우리 드럼 믹서 DEM (LIGGGHTS) 도 입자–입자 · 입자–벽 충돌 에너지 분포를 내보내면 실제 혼합기 (V-블렌더 · 메카노퓨전 · 볼밀) 와 **강도를 같은 단위로** 비교할 수 있다 [추정].
- 할 일 (제안): 믹서 판독기에 충돌 에너지 히스토그램 (상 쌍별) 을 보고 전용으로 추가 검토 — 판정에는 쓰지 않는다.

**8-3. 분체 묻은 볼 보정 = DEM 보정의 본보기.**
- 논문: 반발계수를 분체층 높이에 따라 재고 (0.9 → 0.1) 평균 층 높이 0.94 mm 의 0.15 를 썼다 · 구름 · 동마찰은 진자, 정마찰은 안식각.
- 뜻: 분체가 접촉 매개변수를 크게 바꾼다 — 우리 믹서 · 압축 DEM 의 반발계수 · 마찰도 "깨끗한 표면" 값이 아닐 수 있다.

**8-4. "최적 E_m 창" 은 생각보다 넓고, SE 결정자가 숨은 축이다.**
- 논문: 저자 최적 500 ± 100 J/g 이지만 [판독] 150 mAh/g 이상이 137 J/g (200/60) 에서 1,184 J/g (1000/5) 까지 퍼져 있다 · 결정자 35–40 nm 가 최고 용량 · 25 nm 아래 하락.
- 뜻: 펠릿 σ₀ (우리 보고 기준 1.5) 는 공정 이력에 따라 달라질 수 있다 — Cronau 2022 의 밀링 손상과 같은 축.  우리 모델에 들어가는 σ₀ 를 "실험 SE 의 공정 뒤 값" 으로 맞춰야 절대 비교가 선다.

**8-5. 미리 만든 구조는 건식 막 공정을 통과한다 — 단 고율 차이로.**
- 논문: 섬유화는 구조를 거의 안 바꾸고 캘린더가 저율 이용률만 올린다 · 1C 에서 600/10 막 66 vs 200/5 막 38 mAh/g [판독].
- 뜻: 건식 후막에서 혼합 · 코팅 상태의 차이는 **고율 · 수송 쪽**에서 드러난다 — 논지 P3 를 실험으로 볼 때 0.1C 용량보다 σ_ion · 고율 용량이 판별력이 크다 [추정].

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Frankenberg et al. (*Small* 2025) showed that, at a fixed NCM83:Li₆PS₅Cl ratio (70:30 wt%), the planetary-milling energy alone (specific energy input 11–4,737 J g⁻¹, computed from DEM collision statistics) moves the pellet porosity from 37.6 % to 26.5 %, the effective ionic conductivity through a maximum at 600 rpm/10 min, and the 0.1C capacity from 110 to ≈165 and back to ≈90 mAh g⁻¹; excessive milling shrank the Li₆PS₅Cl crystallites below 25 nm and strained the NCM lattice."
- 국문: *"같은 조성이라도 혼합 · 밀링 에너지가 SE 입경 · 응집 · 결정자 · 활물질 변형을 함께 바꾼다 — 코팅 상태를 비교할 때 공정 에너지를 같이 적어야 한다 (Frankenberg 2025, 유성 볼밀)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **차단 셀 이름이 실험 절에서 뒤바뀌었다**: *"For electron blocking conditions, 80 mg of the prepared composites were layered directly between two steel stamps. For ion blocking conditions, 80 mg of the composite powder was layered between 80 mg of LPSCl with In–Li-alloy"* (p.14) — 강철 사이는 **이온 차단 (σ_e)**, LPSCl 사이는 **전자 차단 (σ_ion)** 이다.  Fig 5d 의 셀 모식과 같은 문단의 *"no transport limitations in the electron blocking layer"* 는 올바른 쪽 — 오기는 앞 두 문장.  (Nakamura 2020 SI 에도 같은 부류의 뒤바뀜이 있었다.)
2. **1000 rpm 기공 시간**: 본문 *"dropping from 37.6% to 26.5% after 30 min of milling at 1000 rpm"* (p.6) ↔ Fig 5b 범례 1000 rpm **20 min** · 실험 절 *"for 800 and 1000 rpm, only 20 min of milling were used"* (p.13) — 본문 오기 [판독 위치 E_m 4,720 J/g = 20 min 계산값 4,737 과 맞음].
3. **SI 표 S1–S3 · Fig S3 의 속도 이름**: 표 머리 "n_MC" · 그림 *"rotational speed of the milling chamber"* 인데 본문 정의는 n = 해 바퀴, n_MC = −2n — 표 값으로 E_m 을 다시 내면 **해 바퀴 속도** 로 읽어야 본문 · 그림 값과 맞는다 [우리 산술].
4. **단위 오기**: Fig 4b 세로축 *"Mean stress energy [s⁻¹]"* (J 이어야) · Fig 8 색 막대 *"SF [J]"* (s⁻¹ 이어야) · Fig 6d 가로축 *"Strain in NCM [-]"* 인데 값은 % (표 S6).
5. **σ_e "continuously" 감소**: [판독] 600/10 (0.49) > 400/20 (0.39) · 다섯 조건 단일 값 · 오차 없음.
6. **최적 창 "500 ± 100 J/g"**: [판독] 200/60 (137 J/g) 158 · 1000/5 (1,184 J/g) 160 · 800/5 (701 J/g) 156 mAh/g — 창 밖에서도 거의 최적이고 셀은 조건당 2 개 ⇒ 창은 뾰족하지 않다.  저자도 결정자 · 변형 단에서는 E_col 과 N_col 을 따로 봐야 한다고 적는다.
7. **"고율에서 개선이 거의 안 보인다"** (p.11) ↔ [판독] 0.3C 에서 200/5 막 122 vs 분체 셀 84 · 600/10 막 149 vs 129 mAh/g — 0.3C 에서는 개선이 보인다 (1C 에서는 600/10 이 66 vs 68 로 없음).  단 막 로딩이 1.5 배.
8. **표 S5 의 LPSCl x_S (200 rpm 60 min) = 0.1993(2)** — 나머지는 모두 ≈0.12 → 오기로 보인다 [추정].  표 S6 의 e₀(LPSCl) 는 L_Vol 이 작은 시료에서 0.0004 로 무너진다 (0.05 → 0.0004) — 크기 · 변형 정제의 상관일 수 있다 [추정] · 200/60 의 0.03(9) 는 불확도가 값보다 크다.
9. **"factor ≈4 / ≈3.8"** 은 지수 (§3-2) — 배수로 읽으면 볼 크기 효과를 2 배 이상 과소평가한다.
10. **측정 조건 결손**: σ 측정 온도 · LPSCl 벌크 σ₀ · 볼 재질 이름 (*"yttrium-reinforced"* 만) · 통 부피 · 33.7 % 의 근거 계산 [미확인].
11. **tortuosity 는 재지 않았다** — *"a comparable tortuosity is still present"* (p.11) 는 해석.
12. **전이 한계**: 유성 볼밀 · 50:50 vol · 탄소 없음 · 단결정 NCM83 · In/InLi 반쪽 셀 · 0.1C 20 사이클 · 셀 2 개 — 저에너지 혼합 · 우리 바이모달 (PC + SC) · 18.4 wt% SE 로 그대로 옮기지 않는다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 8 | F. Frankenberg, M. Kissel, C. F. Burmeister, M. Lippke, J. Janek, A. Kwade, Powder Technol. 2024, 435, 119403. | 정본 카드 `frankenberg2024_dem_high_intensity_mixer_assb` — 같은 응력 모델의 믹서 DEM |
| 21 | E. Schlautmann, A. Weiß, O. Maus, L. Ketter, M. Rana, S. Puls, V. Nickel, C. Gabbey, C. Hartnig, A. Bielefeld, W. G. Zeier, Adv. Energy Mater. 2023, 13, 2302309. | 정본 카드 `schlautmann2023_se_particle_size_composite_transport` |
| 26 | M. Cronau, M. Duchardt, M. Szabo, B. Roling, Batteries Supercaps 2022, 5, 202200041. | 정본 카드 `cronau2022_wet_milling_particle_size_ionic_conductivity` — 밀링 손상 ↔ σ |
| 27 | O. Maus, M. A. Lange, F. Frankenberg, F. Stainer, V. Faka, E. Schlautmann, C. Rosenbach, A. Jodlbauer, J. Schubert, J. Janek, C. Li, P. Michalowski, H. M. R. Wilkening, A. Kwade, W. G. Zeier, Adv. Energy Mater. 2024, 15, 2403291. | 카드 없음 — LPSCl 단독 건식 분쇄 · DEM E_m ↔ 결맞음 길이 (이 논문의 선행) |
| 31 | M. Kissel, M. Schosland, J. Töws, D. Kalita, Y. Schneider, J. Kessler-Kühn, S. Schröder, J. Schubert, F. Frankenberg, A. Kwade, A. Bielefeld, F. H. Richter, J. Janek, Adv. Energy Mater. 2025, 15, 2405405. | 카드 없음 — 정적 CAM 이용률 · 2 차 혼합도 정의 |
| 35 | D. Lee, Y. Shim, Y. Kim, G. Kwon, S. H. Choi, K. Kim, D.-J. Yoo, Nat. Commun. 2024, 15, 4763. | 정본 카드 `lee2024_shear_force_dry_process_cathode_coverage` |
| 37 | F. Hippauf, B. Schumm, S. Doerfler, H. Althues, S. Fujiki, T. Shiratsuchi, T. Tsujimura, Y. Aihara, S. Kaskel, Energy Storage Mater. 2019, 21, 390. | 정본 카드 `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` (같은 날 묶음 · PTFE 건식 막 원전) |
| 52 | P. Minnmann, F. Strauss, A. Bielefeld, R. Ruess, P. Adelhelm, S. Burkhardt, S. L. Dreyer, E. Trevisanello, H. Ehrenberg, T. Brezesinski, F. H. Richter, J. Janek, Adv. Energy Mater. 2022, 12, 2201425. | 정본 카드 `minnmann2022_designing_cathodes_solidstate` |
| 62 | T. Kawaguchi, H. Nakamura, S. Watano, Powder Technol. 2017, 305, 241. | 정본 카드 `kawaguchi2017_dry_coating_parametric_na2so4_model_se` |
| 69 | A. Bielefeld, D. A. Weber, J. Janek, J. Phys. Chem. C 2019, 123, 1626. | 정본 카드 `bielefeld2019_microstructural_modeling_composite_cathode` |
| 71 | P. Minnmann, L. Quillman, S. Burkhardt, F. H. Richter, J. Janek, J. Electrochem. Soc. 2021, 168, 040537. | 정본 카드 `minnmann2021_jes_charge_transport_bottlenecks` — 같은 그룹 σ_ion 앵커 (73 wt% · 380 MPa) |
| 63 · 64 | E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, J. Power Sources 2023, 555, 232379. · E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Adv. Powder Technol. 2022, 33, 103705. | 카드 없음 — 고강도 혼합 코팅 (오사카 그룹) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 16 쪽 · SI 9 쪽 텍스트 층 전수 · 저자 · 소속 · 날짜 · DOI = p.1 · p.15 · 실험 조건 = p.12–14 · 표 S1–S6 = 텍스트 층 + 크롭 영상 대조.
- 그림 · 표 26 장 = 본문 그림 8 (래스터 원본 300 dpi 경계) · SI 그림 12 (래스터 합집합 ≈220 dpi) · SI 표 6 (벡터 300 dpi · 표 S3 은 SI p.2 · p.3 두 조각을 이어 붙임) — 크롭마다 렌더로 열어 축 제목 · 범례 · 패널 표지 확인 · 자동 추출의 표 S1 · S2 bbox 는 다음 표까지 먹어 다시 잘랐다.
- 판독: 같은 조건이 겹치는 그림 사이 (Fig 5b ↔ 5d 의 200/30 · 1000/20) x 위치가 같고, 모든 표지의 x 가 SI 표 S1 로 다시 낸 E_m 과 1 % 안에서 맞는다 (digitized.csv 의 Em_calc 열).
- 교차 확인: Kawaguchi 2017 (ref 62) · Lee 2024 (ref 35) 서지가 정본 카드의 서지와 같음.
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 전수 + DOI · 제목 낱말 grep — 이 논문 카드 없음 (같은 1저자의 2024 믹서 DEM 카드만).

## 🔗 관련 카드
- 같은 그룹 · 공정: `frankenberg2024_dem_high_intensity_mixer_assb` · `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` · `heck2026_densification_sulfide_se_binder_scalable`.
- SE 입경 · 밀링 · 결정자: `cronau2022_wet_milling_particle_size_ionic_conductivity` · `schlautmann2023_se_particle_size_composite_transport` · `faka2026_particle_size_consolidation_strain_lpscl`.
- 건식 공정 · 코팅: `lee2024_shear_force_dry_process_cathode_coverage` · `kawaguchi2017_dry_coating_parametric_na2so4_model_se` · `nakamura2020_dry_coating_ncm_li3ps4_core_shell` · `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps` · `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` · `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` · `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` · `lee2026_unveiling_ptfe_dry_electrode_digital_twin`.
- 같은 그룹 수송 앵커: `minnmann2021_jes_charge_transport_bottlenecks` · `minnmann2022_designing_cathodes_solidstate` · `bielefeld2019_microstructural_modeling_composite_cathode`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

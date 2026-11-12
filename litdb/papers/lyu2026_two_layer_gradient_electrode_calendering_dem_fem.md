<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-41 · 정독 82) 에서 꼭 뽑으라고 한 항목.
     본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (절 번호 · 머리 상자 · 메타 줄 · 서지 표 · 그림 표 꼴) · 같은 분야 이웃 = du2025_dem_fem_force_chain_collector_damage_calendering.md
     (액체 LIB 양극 압연 DEM → FEM 한 방향 넘김 · 역학 쪽) · 같은 그룹 앞 논문 = lyu2025_3d_dem_drying_calendering_lib.md (이 논문 ref [82] · 다른 논문) · 이 논문을 인용한 카드 = qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode.md (그 논문 ref [45]).
     원문 = 출판본 (Int. J. Mech. Sci. 322 (2026) 111716 · 14 쪽 · 보충 자료 없음 — 부록 A–E 가 본문 안 p.9–12).  쪽 표기 "p.n" = PDF 쪽 n = 논문 쪽 (머리글 "International Journal of Mechanical Sciences 322 (2026) 111716" 아래 쪽 번호 1–14).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (그림은 전부 300 dpi 내장 래스터 · 재현 = litdb/figures/<slug>/digitized.csv 210 행 · 방법 = 행마다 note — 큰 눈금 직선 맞춤 ·
     표식 중심 · 가려진 표식은 보이는 가장자리 + 범례 크기 · 그리는 순서로 가림 판정) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] · [카드 관찰] = 이 카드의 해석 ·
     [다른 카드] = 정본 다른 카드에 적힌 값 (slug · 줄 병기) · [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 본문 14 쪽 전수에 없음.
     원문 14 쪽은 글자 층 (PyMuPDF) + 쪽 렌더 + 내장 래스터로 읽었다.  계산 = 상용 DEM (PFC3D · 판 번호 미인쇄) + 상용 FEM (COMSOL Multiphysics 6.2) + 자체 Java 기하 재구성 ([68]) · 코드 · 입력 공개 없음 (p.13 "Data will be made available on request."). -->
# 이중층 경사 양극 (NCM + 탄소-바인더 CBD 92 : 8 · 큰 입자 반지름 6 µm / 작은 입자 3 µm 를 두 층으로) 의 캘린더링을 3D DEM (PFC3D · 단단한 구 · 평판 0–250 MPa · 50 × 50 × 150 µm) 으로 누르고 AM 중심 · 반지름만 COMSOL 반쪽 전지 FEM (20 × 20 × 175 µm) 으로 넘겨 방전 — 작은 입자 층이 늘 더 성기게 남는다 (층 기공 차 100 MPa 11.6 %p → 250 MPa 1.7 %p [판독]) · 작은 입자를 분리막 쪽에 둔 쪽 5C 98 ↔ 54 mAh g⁻¹ · 두 단계 압연 (250 MPa → 뺌 → 새 층 → 다시) 의 기공 경사 5C 120 ↔ 97 · 응력 축 없음 · 뺀 뒤 되돌아옴은 3D 렌더 한 장 — Lyu · Dong · Guo (Int. J. Mech. Sci. 2026)

> slug `lyu2026_two_layer_gradient_electrode_calendering_dem_fem` · DOI `10.1016/j.ijmecsci.2026.111716` · type `DEM (PFC3D, 3D RVE 50 x 50 x 150 um periodic x-y, rigid spheres NCM AM + CBD 2 um, nonlinear Hertz-Mindlin AM-AM without yield, parallel bond CBD-CBD/CBD-AM with Mohr-Coulomb failure, constant-velocity top plate 0-250/300 MPa, two-layer + two-step calendering) + one-way geometric DEM to FEM handover (AM centres + radii, in-house Java reconstruction) + FEM half-cell discharge (COMSOL 6.2, 20 x 20 x 175 um, Li metal, CBD+electrolyte mixed phase, Butler-Volmer, 0.5-5C) + validation against literature data (SEM, synchrotron thickness, rate capacity); liquid-electrolyte LIB cathode, no SE` · PDF `cda04b06-41._Calendering_behavior_of_two-layer_electrodes_A_coupled_DEM_FEM_framework.pdf` (14 쪽 · 보충 자료 없음 · 부록 A–E 본문 안) · digested `2026-11-12` · status ✅
>
> **저자**: **Yuhang Lyu** · **Shaohai Dong** · **Zhan-Sheng Guo\*** (교신) — Shanghai Institute of Applied Mathematics and Mechanics · School of Mechanics and Engineering Science · Shanghai Key Laboratory of Mechanics in Energy Engineering · Shanghai University (Shanghai 200072, China) · *Int. J. Mech. Sci.* **322** (2026) 111716 (14 쪽) · 접수 2026-01-06 · 수정 05-07 · 승인 05-09 · 온라인 05-10 · 연구비 NSFC 12572202 · 12172206 · 기여 (p.9): Lyu = 초고 · 시각화 · 검증 · 소프트웨어 · 방법 · 조사 · 분석 / Dong = 검토 · 편집 · 시각화 · 방법 · 분석 / Guo = 검토 · 편집 · 시각화 · 지도 · 자원 · 과제 관리 · 방법 · 연구비 · 착상.
> **이웃 카드 (링크만)**: [`qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode`](qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode.md) (그 논문 ref [45] = 이 논문 · 직접 경쟁작) · [`lyu2025_3d_dem_drying_calendering_lib`](lyu2025_3d_dem_drying_calendering_lib.md) (같은 그룹 2025 · 이 논문 ref [82] · **다른 논문**) · [`du2025_dem_fem_force_chain_collector_damage_calendering`](du2025_dem_fem_force_chain_collector_damage_calendering.md) (DEM → FEM 한 방향 · 역학 쪽 · 이 논문이 인용하지 않음) · [`lu2020_insitu_nanoct_calendering_microstructural_evolution`](lu2020_insitu_nanoct_calendering_microstructural_evolution.md) (ref [59] · 전기화학 검증 자료) · [`sangros2019_dem_calendering_lib_electrode`](sangros2019_dem_calendering_lib_electrode.md) (ref [62] · E_AM 142 · ρ 4.75 출처) · [`so2021_dem_mold_pressure_assb_coldpress`](so2021_dem_mold_pressure_assb_coldpress.md) (ref [85] · Hertz–Mindlin 인용) · [`song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage`](song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage.md) (ref [61]) · [`lim2025_virtual_calendering_framework`](lim2025_virtual_calendering_framework.md) (ref [13]) · [`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`](alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md) (ref [54]) · [`aminchiang2016_nmc_electronic_ionic_transport_vs_li`](aminchiang2016_nmc_electronic_ionic_transport_vs_li.md) (ref [71] · σ_p 출처).
> **판독 원자료**: `litdb/figures/lyu2026_two_layer_gradient_electrode_calendering_dem_fem/digitized.csv` (210 행 — Fig 2e · 2f · 3e · 3f · 3 의 행 순서 점검 · 4a · 4b · 4d · 4f · 5i · 6 렌더 높이 · 7b · 7c · 8i · D1b · E1b–d) · 그림 크롭 64 장 (그림 8 + 부록 그림 4 · 패널 16 · 표 2 · 식 12 + 묶음 2 · 근거 문단 20) — `figures.json`.

> elements: Li, Ni, Co, Mn, O, C, Cu

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: NCM 양극 (AM : CBD = 92 : 8 질량 · 처음 기공 48 % · 큰 입자 반지름 평균 6 µm / 작은 입자 3 µm · 둘 다 σ 0.5 µm 정규 분포) 을 두 층 (각 75 µm [카드 추론]) 으로 쌓아 PFC3D 3D RVE (50 × 50 × 150 µm · x–y 주기) 에서 위판을 일정 속도로 내려 250 MPa 까지 누르고 (배치 C1–C4), 그 AM 중심 · 반지름만 자체 Java 재구성으로 구를 만들어 COMSOL 반쪽 전지 (Li 금속 · 분리막 25 µm · CBD + 전해질 = 한 혼합상) 의 양극으로 넣어 0.5–5C 방전을 푼다 — **같은 압력에서 큰 입자 층이 더 치밀해지고 (저자 해석 = 재배열이 쉽다) 작은 입자 층이 더 성기게 남는다**; 그래서 작은 입자를 분리막 쪽에 둔 C2 가 5C 에서 98 mAh g⁻¹ (C3 54); 첫 층을 250 MPa 로 누르고 뺀 뒤 새 층을 얹어 다시 누르는 두 단계 압연이 위 48 → 41.6 % · 아래 39.4 → 35.2 % (0 → 150 MPa [판독]) 의 기공 경사를 만들고 5C 120 ↔ 97 mAh g⁻¹ (같은 두께 · 평균 기공의 균일 대조) — **넘김은 기하 (구) 만이고 응력 · 접촉 · 겹침은 넘기지 않는다** · 결과에 응력 축이 없다 · 뺀 뒤 되돌아옴은 3D 렌더 한 장 (Fig 6c) 뿐.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① DEM → FEM 넘김 (무엇을 · 언제 · 어떻게) | AM 공간 좌표 + 반지름 → 자체 Java 기하 재구성 [68] → 구 → COMSOL 양극 영역 그대로 · *"Microstructural descriptors, including spatially resolved porosity gradients, are mapped onto the FEM mesh"* (방법 [미확인]) · CBD 는 형상으로 넘기지 않음 (전해질과 한 혼합상) · 한 방향 · 시점 = 압연 끝 (C2 · C3 · 두 단계) · 누른 채인지 뺀 뒤인지 · 50 × 50 µm DEM 에서 20 × 20 µm 창을 고른 법 [미확인] | [인쇄] p.2 §2.1 · §2.3 · Fig 1(d) |
| ② 이중층의 압력 축 | 층별 기공 · 두께 · AM 배위수 vs 압력 (0 · 20 · 50 · 100 · 150 · 200 · 250 MPa) — C2 위 (작은) 48 → 29.0 · 아래 (큰) 48 → 27.3 % · C3 위 (큰) → 26.5 · 아래 (작은) → 28.8 % · 층 기공 차 최대 = 100 MPa (C2 11.6 · C3 8.2 %p) → 250 MPa 1.7 · 2.3 %p · 두 단계 압연의 두 번째 0 → 150 MPa | [판독 · 카드 산술] Fig 4a–b · 7b–c · [인쇄] p.6–7 |
| ③ 이중층의 응력 축 | **없음** — 응력장 · 힘 사슬 세기 · 층별 하중 · 판 반력 곡선 · 잔류 응력 0 ('stress' = 결합 식 A4–A5 와 참고문헌 제목뿐 · Fig 4c · 4e 의 접촉망은 접촉 종류 색만) | 14 쪽 전수 |
| ④ 압력을 뺀 뒤 | 두 단계 압연 1 단계 뒤 *"After pressure removal, partial elastic recovery ("springback") occurred"* — 숫자는 '아래 층 처음 39.4 % · 64.4 µm' 뿐 · 되돌아옴 크기 = 렌더 높이 ≈ +19–22 % [판독 · 원근 렌더 · 낮은 신뢰] · 단일 압연 (Fig 2–4) 값이 누른 채인지 뺀 뒤인지 [미확인] | [인쇄] p.7 · Fig 6 · §3-4 |
| ⑤ 접촉 법칙 · 매개변수 · 맞춘 값 | AM–AM = 비선형 Hertz–Mindlin (A3 · **항복 없음**) · CBD–CBD · CBD–AM = 평행 결합 (A4–A5 · Mohr–Coulomb 파단 → 선형 탄성 접촉) · 표 1: E 142 / 0.76 GPa · ν 0.3 · ρ 4.75 / 2.2 g/cm³ · 마찰 0.25 · 결합 강성 1.35 × 10¹¹ N/m³ (전부 문헌값) · **맞춘 값 0** · 민감도 두 팔 (E_AM 75 GPa · 결합 강성 0.8 × 10¹¹) · 결합 세기 · 감쇠 · 판 속도 · 시간 간격 [미확인] | [인쇄] 표 1 · 식 A1–A5 · Fig E1 · p.10 · p.12 |
| ⑥ 검증 | 형상 = SEM 단면 넷 (Wood [37]) 정성 · 두께 = Ademmer [49] (얇은 80 → 54 · 두꺼운 183 → 110 µm @ 300 MPa) · 용량 = Lu [59] (0.2–3C · 3C 계산 ÷ 실험 1.18) — **이중층 결과 자체 (층 기공 · 두 단계 압연) 의 실험 대조는 없다** | [인쇄] p.3–4 · [판독 · 카드 산술] Fig 2e–f · D1b |
| ⑦ DEM 한계 문장 | *"using either method alone is insufficient to capture both mechanical and electrochemical aspects"* (p.2) · *"the application of the PBM model ignores the viscoelastic and adhesive properties introduced by the binder in actual electrodes, which may influence the microstructural evolution of the electrodes"* (p.10) — 단단한 구 · 형상 고정 · 소성 · 파괴에 대한 말은 없음 | [인쇄] |
| ⑧ 차원 | 3D DEM + 3D FEM · 같은 그룹 2D DEM ([83]) 을 '이론 세부' 로만 인용 · 2D → 3D 전이 진술 없음 | [인쇄] p.9 부록 A |
| ⑨ 저자가 적은 한계 · 다음 | PBM 이 바인더 점탄성 · 점착을 무시 (p.10) · *"Future work can build upon this framework to systematically quantify the effects of actual calendering process parameters on electrode properties"* (p.9) | [인쇄] |

⛔ **한정어 (떼지 말 것)**: ① **액체 전해질 LIB 양극 (NCM + CBD · SE 없음)** — 무른 상 = 다공 탄소-바인더 덩어리 (DEM 에서는 지름 2 µm 구 + 결합) · NCM 조성 [미확인] ② **평판 압축** (롤 아님 · 판 속도 [미확인]) ③ **AM = 탄성 구** (항복 · 소성 · 파괴 없음) — 치밀화 = 재배열 + CBD 결합 변형 · 파단 ④ **응력 · 하중 몫 숫자 0** ⑤ 압력 · 두께 · 층 기공 · 배위수의 정의와 누른 채 / 뺀 뒤 [미확인] — 이 카드의 고체 보존 점검은 층 기공과 두께가 ±1 % 안에서 맞는다 (§3-3) ⑥ FEM 은 **20 × 20 µm 창** (큰 입자 지름 12 µm 의 1.7 배 · 큰 입자 ≈14 개 [카드 산술]) · CBD 는 혼합상 ⑦ 검증 셋은 서로 다른 전극 — 이중층 결과의 직접 실험 대조 없음.
⇒ **절대값 전이**: 기공 · 두께 · 배위수 · 용량 숫자는 우리 재료 (LPSCl + NCM · 300 MPa) 로 **옮기지 않는다** (LIB 양극 · CBD 무른 상 · 평판 · 액체 전해질 · 랩 표준과 다른 문헌 값).  옮길 수 있는 것은 (a) DEM 구 → FEM 기하 넘김의 꼴과 그 빈칸 목록 (b) 층별 기공 · 두께의 고체 보존 점검 (c) '압력을 뺀 뒤 새 층을 얹고 다시 누르는' 두 단계 시험 꼴 (d) '같은 압력에서 큰 입자 층이 더 치밀해진다' 는 모델 안 주장 (결과 전 대조 항목 후보 · 기전은 단정 아님).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-41 의 '왜' 칸)

의도 원문: *"h — 이중층 캘린더링 DEM–FEM 결합 = DEM → FEM 넘김 선례 · "이 논문의 직접 경쟁작인데 정본에 없다 (정본 lyu2025_3d_dem_drying_calendering_lib 는 다른 논문) · 확보 권고" · 이중층의 응력 · 압력 축 후보 · "정본 카드화 권고""* (근거 = `qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode` L36 · L40 · L438 · L506 · L652)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| (h) "이중층 캘린더링 DEM–FEM 결합" | **채움** | §2.1 (p.2): AM 중심 · 반지름 → Java 재구성 [68] → 구 → COMSOL 양극 영역 · Fig 1 · 이중층 = 큰 / 작은 입자 두 층 (C2 · C3) + 두 단계 압연의 기공 경사 (Fig 6–8) |
| "= DEM → FEM 넘김 선례" | **채움 (한정)** — 넘김 = **기하만 · 한 방향 · 전기화학 FEM** | 넘기는 것 = AM 중심 + 반지름 (+ *"spatially resolved porosity gradients"* 를 망에 사상 — 방법 [미확인]) · 넘기지 않는 것 = 접촉력 · 응력 · 결합 상태 · 겹침 처리 · CBD 위치 (혼합상) · 시점 = 압연 끝 (C2 · C3 = 250 MPa 로 읽힘 [카드 추론 — 본문 "calendered C2 and C3 electrodes"] · 기공 경사 = 두 번째 압연 끝 (Fig 7 축 끝 150 MPa · 쓴 압력 [미확인])) · 누른 채 / 뺀 뒤 [미확인] · **역학 FEM 으로 넘긴 것이 아니다** (우리 'DEM → MPM 압밀' 넘김과 다른 갈래 — 역학 쪽 선례는 `du2025_…` (접촉력 → Al 박 FEM)) |
| "이 논문의 직접 경쟁작" | **채움** | qin2026 (CGMD → DEM 이중층 양극 · 경사 후막) 과 같은 질문 = 이중층 양극의 제조 (압연) → 성능.  이 논문은 qin2026 을 인용하지 않고 qin2026 은 이 논문을 [45] 로 인용 |
| "정본에 없다 (정본 lyu2025 는 다른 논문)" | **채움** | papers/ 목록 · DOI · '111716' · 제목 낱말 grep → 카드 없음 (qin2026 인용만) · `lyu2025_3d_dem_drying_calendering_lib` = Int. J. Electr. Power Energy Syst. 165, 110521 (2025) = 이 논문 ref [82] (같은 그룹 · 건조 + 압연 DEM) — **다른 논문 맞다** · 같은 저자 같은 해 (2026) 다른 카드 없음 |
| "이중층의 압력 축 후보" | **채움** | Fig 3e–f (두께 · 압축률 · C1–C4) · Fig 4a–b (층 기공) · 4d · 4f (AM 배위수) · Fig 7b–c (두 번째 압연 층 기공 · 두께) — 압력 = *"calendering pressure"* (정의 [미확인]) · 상태 = 압력별 점 (누른 채로 읽힘 [카드 추론]) · 온도 · 진밀도 기준 없음 (DEM 기공 · 구 부피) |
| "이중층의 응력 축 후보" | **없음** | 응력 · 하중 · 힘 사슬 세기 · 잔류 응력의 그림 · 숫자 0 — qin2026 L438 *"응력·압력 축이 있을 가능성"* 의 응력 쪽은 원문에 없다 (가능성으로 적힌 문장이라 카드 문제는 아님) |
| "확보 권고 · 정본 카드화 권고" | **채움** | 이 카드 |
| qin2026 L40 서지 | **채움 (같음)** | *"Lyu·Dong·Guo 2026 (IJMS 322, 111716, "Calendering behavior of two-layer electrodes: A coupled DEM–FEM framework")"* = 원문 첫 쪽 · 저자 이름 전체 = Yuhang Lyu · Shaohai Dong · Zhan-Sheng Guo · DOI 10.1016/j.ijmecsci.2026.111716 (qin2026 카드에 없던 것) |
| qin2026 L506 "같은 해 ref [45] Lyu 2026 이 이중층 캘린더링 DEM–FEM 을 냈다" | **채움** | 온라인 2026-05-10 (p.1) · 이 논문도 초록 · 결론에서 *"for the first time"* 을 주장 (p.1 · p.9) — 범위 한정이 필요하다 (§11-1) |
| 가리킨 카드의 **2 차 인용 값** | **해당 없음** | qin2026 카드는 이 논문에서 숫자를 옮기지 않았다 (서지 · 주제 표기뿐) |

⇒ **의도 대조 결과: 일부** — DEM → FEM 넘김 선례 · 이중층 압력 축 · 정본 부재 확인은 **채움**; 넘김은 **기하만 (전기화학 FEM · 역학 아님)** 이고 **응력 축은 없다**.

---

## 1. 한 줄 요약
경사 전극 (분리막 쪽 작은 입자 · 높은 기공) 이 고율에 좋다는 실험들은 있지만 압연이 그 구조를 어떻게 만드는지는 모른다는 동기 (p.1–2) 에서, PFC3D 3D DEM 으로 이중층 양극을 평판 압연하고 그 AM 구를 COMSOL 반쪽 전지로 넘겨 방전한다 — 큰 입자 층이 (저자 해석으로) 재배열이 쉬워 더 치밀해지므로 (압축률 C1 29.1 > C4 25.9 % @ 250 MPa [판독]) 작은 입자를 분리막 쪽에 두면 압연이 저절로 '분리막 쪽 높은 기공' 을 만들고 (C2) 5C 용량이 C3 의 ≈1.8 배 (98 ↔ 54 mAh g⁻¹); 또 첫 층을 250 MPa 로 누르고 뺀 뒤 새 층을 얹어 다시 누르는 두 단계 압연은 위 층 기공이 늘 더 높은 경사를 만들어 5C 120 ↔ 97 mAh g⁻¹ (같은 두께 · 평균 기공의 균일 대조).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| Yuhang Lyu · Shaohai Dong · Zhan-Sheng Guo\* (Shanghai University) | Int. J. Mech. Sci. 322 (2026) 111716 · 14 쪽 | 10.1016/j.ijmecsci.2026.111716 | **SE 없음** — 액체 전해질 LIB 양극: NCM (조성 [미확인] · FEM 물성 출처 = NMC532 [70] · NMC333 / 523 [71]) + CBD (탄소-바인더 덩어리 · 92 : 8 질량) · 반쪽 전지 Li 금속 · 전해질 이름 미인쇄 ([73] 제목 = LiPF₆–EC–EMC) | 계산 — DEM (압연) + 한 방향 기하 넘김 + FEM (방전) · 문헌 실험 자료와 대조 (자체 실험 없음) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. DEM 모형 · 입력 (표 1 · §2.2 · 부록 A · C)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 코드 | PFC3D (판 번호 [미확인]) | [인쇄] p.2 |
| RVE | 50 × 50 × 150 µm (Fig 1c 캡션) · 처음 두께 150 µm (C1–C4 · p.4) · x–y 주기 · 아래 = 집전체 (고정) · 위 = 판 (*"a constant downward velocity"* [56, 60, 62] · 값 [미확인]) | [인쇄] p.2 · p.3 · p.4 |
| 처음 기공 | 48 % (모든 RVE · *"identical initial porosities (48%) and thicknesses"* · 이중층은 두 층 두께 · 기공 같음) — DEM 구 (AM + CBD) 를 고체로 센 값으로 읽힘 [카드 추론] | [인쇄] p.2 · p.3 |
| 조성 | AM : CBD = 92 : 8 (질량 · [49] 와 같게) · 고체 부피 중 AM 84.2 % [카드 산술: (92/4.75) ÷ (92/4.75 + 8/2.2)] | [인쇄] p.2 · [카드 산술] |
| AM 입경 | 반지름 정규 분포 μ_S = 3.0 µm · μ_L = 6.0 µm · σ = 0.5 µm (Fig C1 그림 안 글자 · 캡션 *"mean radius of 6 μm … 3 μm"*) · 수 / 부피 가중 [미확인] | [인쇄] p.11 Fig C1 |
| CBD | 지름 2 µm 구 (분포 미인쇄 → 단분산으로 읽힘) | [인쇄] p.2 |
| 배치 | C1 = 큰 입자 한 층 · C2 = 아래 (집전체 쪽) 큰 / 위 작은 · C3 = 아래 작은 / 위 큰 · C4 = 작은 입자 한 층 (Fig 3 캡션) | [인쇄] p.5 |
| 운동 | 뉴턴 병진 · 회전 (A1 · A2 · 중력 m_i g 포함) | [인쇄] p.10 |
| AM–AM 접촉 | *"The contact between AM particles follows the nonlinear Hertz–Mindlin model [69,85]"* · F_c = (k_n δ_n − γ_n v_n) + (k_t δ_t − γ_t v_t) (A3) · k · γ 의 식 · 값 [미확인] · **항복 · 소성 없음** | [인쇄] p.10 |
| CBD–CBD · CBD–AM | 평행 결합 모형 (PBM) [82, 86, 87] — *"a uniform cylindrical bond at each contact, providing constant normal and shear stiffness and resisting relative motion via force and moment generation"* · 결합 둘레 최대 인장 · 전단 응력 (A4 · A5 · 인쇄 짝지음 문제 §11-4) · *"Bond failure is determined using the Mohr–Coulomb criterion [84]. Once a bond fails, the interaction reverts to a linear elastic contact."* · 결합 세기 · 반지름 배수 · 결합이 생기는 거리 [미확인] | [인쇄] p.10 |
| 표 1 | E 142 (AM) / 0.76 (CBD) GPa [56, 62] · ν 0.3 / 0.3 [69] · ρ 4.75 / 2.2 g/cm³ [56, 62] · 마찰 0.25 / 0.25 [60] · 결합 강성 — / 1.35 × 10¹¹ N/m³ [69] | [인쇄] 표 1 p.3 |
| 입자 수 · 시간 간격 · 감쇠 · 계산 시간 · 반복 (시드) 수 · 처음 충전을 만든 법 | [미확인] — 어림 ≈8 × 10³ 개 (C2: CBD ≈7,360 · AM ≈760 = 큰 ≈89 + 작은 ≈670) [카드 산술: 고체 부피 0.52 × 50 × 50 × 150 µm³ · AM 84.2 % · 두 층 반씩 · 정규 반지름의 ⟨r³⟩ = μ³ + 3μσ² · CBD 4.19 µm³] | [미확인] · [카드 산술] |
| 같은 그룹 2025 와 다른 입력 | `lyu2025_…` (= ref [82]) 표 1: E_CBD 0.65 GPa · ν 0.25 / 0.2 · 마찰 AM 0.12 / CBD 0.1 · ρ_AM 4.74 · AM : CBD 94 : 6 [다른 카드 L38–L42 · L58 · L20] ↔ 이 논문 0.76 · 0.3 · 0.25 · 4.75 · 92 : 8 — 차이 설명 없음 [카드 관찰] | [다른 카드] |
| 원 출처 대조 | E_AM 142 · ρ 4.75 = `sangros2019_…` (= [62]) 표 2 와 같다 [다른 카드 L34 · L37] · 그 논문 ν 0.25 · AM 접촉 = Thornton–Ning (항복 · 나노압입 보정) [다른 카드 L35 · L49] — **이 논문은 E 만 빌리고 항복을 뺐다** [카드 관찰] · E_CBD 0.76 은 [62] 카드에 없음 · [56] 정본 카드 없음 → 대조 못 함 · 결합 강성: [62] = 6 × 10¹² N m⁻³ (보정값) [다른 카드 L41 · L85] ↔ 이 논문 1.35 × 10¹¹ ([69] · 카드 없음) | [다른 카드] |

### 3-2. FEM 반쪽 전지 (표 2 · §2.3 · 부록 B)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 코드 | COMSOL Multiphysics 6.2 | [인쇄] p.2 |
| RVE | 20 × 20 × 175 µm (Fig 1d 캡션) · 분리막 t_sep 25 µm · x–y 주기 · Li 금속 음극 · *"copper foil as the CC"* (어느 쪽 집전체인지 [미확인]) · *"The electrolyte and CBD are treated as a mixed phase"* | [인쇄] p.2 · p.3 |
| 높이 175 µm | = 분리막 25 + 150 µm (압연 **전** 두께) [카드 산술] — 압연 뒤 106–113 µm 와 다르다 (그림이 대표인지 · 실제 높이 [미확인]) | [카드 산술] |
| 방전 | 정전류 0.5 · 1 · 3 · 5C · 2.8 V 끝 (본문) · 검증 Fig D1 = 0.2 · 0.5 · 1 · 2 · 3C · 1C 정의 [미확인] | [인쇄] p.2 · Fig D1 |
| 지배식 | 고체 확산 (B1) · 고체 전하 (B2) · 전해질 물질 (B3) · 전해질 전하 보존 (B4) · 농축 용액 전류 (B5) · Butler–Volmer (B6 · 인쇄 부호 결함 §11-5) · CBD 전하 (B7) — 계면 (AM–AM · AM–CBD) 접촉 저항 항 없음 [카드 관찰] | [인쇄] p.10–11 |
| 표 2 | D_p = f(c_p/c_p,max) [70] · σ_p = f(c_p/c_p,max) [71] · c_p,max 50,061 mol m⁻³ [72] · c_p0 12,515 mol m⁻³ [72] · D_e · σ_e · t⁺ · ∂lnf/∂lnc_e = f(c_e) [66] · [73] · [74] · σ_c 375 S m⁻¹ [74] · α_a = α_c = 0.5 · F · R · T 293.15 K | [인쇄] 표 2 p.3 |
| 처음 리튬화 | c_p0 / c_p,max = 0.250 [카드 산술] → 방전 = 0.25 에서 리튬화 · SOL 색 막대 0.5–1 (그 아래는 같은 파랑) | [카드 산술] · Fig 5 · 8 |
| 미인쇄 | i₀ · 처음 c_e · 유효 물성 보정 (D_e^eff · σ_e^eff · σ_c^eff 의 꼴) · 망 · 요소 수 · 풀이기 · 시간 · 메모리 · 상한 전압 (곡선은 ≈4.25 V 에서 시작 [판독 · 눈대중]) | [미확인] |

### 3-3. ★ 단일 압연 — 두께 · 압축률 · 층 기공 · 배위수 (Fig 3 · 4 · p.4–7)
- 인쇄: *"All electrodes had an initial uncalendered thickness of 150 μm … At 250 MPa, the final thicknesses fell within 106–113 μm, corresponding to compression ratios of approximately 25–30%"* (p.4 · p.6) · *"The single-layer small-particle electrode (C4) retained the greatest thickness, whereas the single-layer large-particle electrode (C1) underwent the greatest compression"* (p.6).

| 압력 (MPa) | C1 두께 | C2 | C3 | C4 | C1 압축률 % | C2 | C3 | C4 |
|---|---|---|---|---|---|---|---|---|
| 0 | 150 | 150 | 150 | 150 | 0 | 0 | 0 | 0 |
| 20 | 145.0 | 146.5 | 146.5 | 147.9 | 3.4 | (가림) | 2.3 | 1.4 |
| 50 | 127.8 | 139.0 | 141.4 | 145.2 | 14.8 | 7.2 | 5.7 | 3.1 |
| 100 | 119.1 | 124.1 | 125.0 | 126.6 | 20.6 | 17.3 | 16.8 | 15.6 |
| 150 | 112.6 | 114.6 | 115.8 | 117.9 | 24.9 | 23.6 | 22.8 | 21.4 |
| 200 | 109.5 | 110.7 | 110.9 | 113.7 | 27.0 | 26.2 | 26.2 | 24.3 |
| 250 | 106.6 | 107.8 | 108.8 | 111.1 | 29.1 | 28.3 | 27.5 | 25.9 |
- [판독] Fig 3e (µm) · 3f (%) — 두 패널 교차 대조 (150 − t)/1.5 ↔ 3f ±0.1 %p.  전체 기공 @ 250 MPa [카드 산술: ε = 1 − 0.52 × 150 / t]: C1 26.8 · C2 27.6 · C3 28.3 · C4 29.8 %.
- ⚠ Fig 3(a)–(d) 의 3D 네 줄은 캡션 순서 (C1 · C2 · C3 · C4) 가 아니라 **C4 · C1 · C2 · C3** 로 읽힌다 — 입자 크기 + 50 MPa 렌더 높이 비 0.967 · 0.842 · 0.925 · 0.938 ↔ Fig 3e 의 50 MPa t/150 = C4 0.968 · C1 0.852 · C2 0.927 · C3 0.943 [판독 · 카드 산술] (§11-3).

**층 기공 (Fig 4a · 4b [판독] · %)**
| 압력 (MPa) | C2 위 (작은) | C2 아래 (큰) | 차 | C3 위 (큰) | C3 아래 (작은) | 차 |
|---|---|---|---|---|---|---|
| 0 | 48 (인쇄) | 48.0 | 0 | 48 (인쇄) | 48.0 | 0 |
| 20 | 47.0 | 46.5 | 0.5 | 46.4 | 46.8 | 0.4 |
| 50 | 46.2 | 43.6 | 2.7 | 42.3 | 45.1 | 2.8 |
| 100 | 42.5 | 31.0 | **11.6** | 33.5 | 41.7 | **8.2** |
| 150 | 34.4 | 28.8 | 5.6 | 30.6 | 33.0 | 2.4 |
| 200 | 30.7 | 27.6 | 3.1 | 27.9 | 30.7 | 2.8 |
| 250 | 29.0 | 27.3 | **1.7** | 26.5 | 28.8 | **2.3** |
- 인쇄: *"Initially, both layers exhibited 48% porosity … The porosity difference reached a maximum near 100 MPa and then gradually decreased. The final porosity ranged from 26 to 30%."* · *"calendering inherently induces a porosity gradient in two-layer electrodes, where the small-particle layers remain more porous and the large-particle layers become denser"* (p.6).
- **고체 보존 점검** [카드 산술]: 층마다 처음 75 µm × 0.52 = 39.0 µm 의 고체 (두 층 같은 두께 · 기공 — p.3) → t_층 = 39.0 / (1 − ε_층) 의 합 ↔ Fig 3e 두께: C2 100 MPa 124.3 ↔ 124.1 (+0.2 %) · 250 MPa 108.6 ↔ 107.8 (+0.8 %) · C3 100 MPa 125.5 ↔ 125.0 (+0.4 %) · 250 MPa 107.8 ↔ 108.8 (−0.9 %) ⇒ 층 기공 = 층 고체 (입자 소속) ÷ 층 두께 꼴로 읽히고 두 그림이 ±1 % 안에서 서로 맞는다 [카드 추론].
- **AM 배위수 (Fig 4d · 4f [판독])**: C2 0.13 · 0.99 · 1.23 · 1.68 · 2.34 · 2.53 · 2.70 / C3 0.11 · 0.95 · 1.26 · 1.66 · 2.24 · 2.56 · 2.71 (0 · 20 · 50 · 100 · 150 · 200 · 250 MPa) ↔ 인쇄 *"increased from 0.15 (uncalendered) to 2.7 at 250 MPa for both designs"* (p.7) · *"Before calendering, contact predominantly involved CBD–CBD and CBD–AM interactions, with few AM–AM interactions"* — 배위수 정의 (AM–AM 만 · AM 한 개당) · 층별 값 [미확인].
- **민감도 (Fig E1 · C2 배치 [판독])**: 250 MPa 위 / 아래 = 기준 (E_AM 142 · k_b 1.35 × 10¹¹) 29.0 / 27.3 · E_AM 75 GPa 26.2 / 24.1 · k_b 0.8 × 10¹¹ 27.7 / 25.4 % · 100 MPa 층 차 11.5 · 9.8 · 6.8 %p · 원문 *"the final porosity of the large-particle layer is consistently lower than that of the small-particle layer, and the qualitative trend of porosity evolution remains unchanged"* (p.12) — 크기는 E_AM 반으로 ≈3 %p · 결합 강성 0.59 배로 ≈1.5 %p 낮아진다 [카드 산술] · Fig E1(b) = Fig 4a 와 같은 자료 (차 ≤ 0.03 %p) [카드 관찰].

### 3-4. ★ 두 단계 압연 · 되돌아옴 (Fig 6 · 7 · p.7)
- 순서 (p.7): (a) 압연 전 한 층 → (b) **250 MPa** 첫 압연 → (c) 압력 제거 · *"partial elastic recovery ("springback")"* → (d) 그 위에 압연 전 새 층 → (e) 두 번째 압연.  *"This first calendering enhances the adhesion at the coating–CC interface and improves electronic conductivity [56]"* (문헌 인용 · 이 논문에서 계산 안 함).
- 두 번째 압연 전 (인쇄 p.7): 아래 층 기공 **39.4 %** · 두께 **64.4 µm** · 위 층 **48 %** · **75 µm**.
- 고체 보존 [카드 산술]: 75 × 0.52 = 39.0 µm = 64.4 × (1 − 0.394) = 39.0 µm → 첫 층도 75 µm · 48 % 에서 출발했다고 읽힌다 (렌더 높이와도 맞음 — 아래).
- **되돌아옴 (b → c)** [판독 · 원근 3D 렌더 · 낮은 신뢰 · 높이 = 집전체 윗면 ~ 가장 높은 입자 화소]: (a) 228 · (b) 165 · (c) 201 · (d) 437 · (e) 391 px → (c) = 64.4 µm 로 맞추면 (a) 73.1 · (b) 52.9 · (d) 140.0 · (e) 125.3 µm · (a) = 75 µm 로 맞추면 (b) 54.3 · (c) 66.1 µm ⇒ 두께 되돌아옴 **≈ +19–22 %** (201/165 = 1.22 · 64.4/54.3 = 1.19) · 250 MPa 누른 채 기공 ≈ 28 % (1 − 39.0/54.3) [카드 산술] — 단일 압연 250 MPa 의 26.8–29.8 % 와 같은 자리.  **원문은 이 크기를 숫자로 적지 않았다.**
- **두 번째 압연 (Fig 7b–c [판독])**:

| 압력 (MPa) | 위 기공 % | 아래 기공 % | 위 두께 µm | 아래 두께 µm | 전체 µm [카드 산술] | 두께 가중 평균 기공 % [카드 산술] |
|---|---|---|---|---|---|---|
| 0 | 48.0 | 39.4 | 75.0 | 64.4 | 139.4 | 44.0 |
| 50 | 46.2 | 38.4 | 72.5 | 63.3 | 135.8 | 42.6 |
| 100 | 44.1 | 36.9 | 69.5 | 62.0 | 131.5 | 40.7 |
| 150 | 41.6 | 35.2 | 66.4 | 60.5 | 126.9 | 38.5 |
- 고체 보존 점검 (층마다) ±0.6 % [카드 산술] · 경사 (위 − 아래) 8.6 → 6.4 %p · 인쇄 *"the top layer always retained a higher porosity than the bottom layer"* · *"the top layer experienced a more pronounced thickness reduction"* (p.7).
- 두 번째 압연을 150 MPa 에서 멈춘 이유 · 그 전극을 FEM 에 넣을 때의 압력 · 두 층의 입경 [미확인] (Fig 7a · 8 렌더로는 두 층 입경이 비슷하고 여러 크기가 섞여 보인다 [카드 관찰]).

### 3-5. ★ 방전 (Fig 5 · 8 · D1)
| 율 | C2 [인쇄] | C2 [판독] | C3 [인쇄] | C3 [판독] | 경사 기공 [인쇄] | 경사 [판독] | 균일 [인쇄] | 균일 [판독] |
|---|---|---|---|---|---|---|---|---|
| 0.5C | 149 | 148.8 | 146 | 146.2 | ≈148 | 148.5 | ≈148 | (가림) |
| 1C | — | 145.5 | — | 142.2 | ≈148 | 146.7 | ≈148 | (가림) |
| 3C | — | 127.3 | — | 111.1 | — | 139.8 | — | 129.1 |
| 5C | **98** | 95.9 | **54** | 53.9 | **~120** | 119.4 | **97** | 96.1 |
- 단위 mAh g⁻¹ · 2.8 V 끝 · 판독 = Fig 5i · 8i 곡선이 2.8 V 틀 바닥에 닿는 x.  5C 비: C2/C3 = 1.81 (인쇄) · 1.78 (판독) ↔ 본문 *"approximately twice"* (p.7) · 결론 *">70% higher capacity at 5C"* (p.9) · 경사/균일 = 1.24 [카드 산술].
- SOL 지도 (Fig 5 · 8 a–h · 색 막대 0.5–1): 고율에서 큰 입자 SOL 낮음 · 기공 경사 / 균일 모두 5C 에서 집전체 쪽 AM SOL 낮음 — SOL 숫자 [미확인].
- 대조 전극: *"A control electrode with the same total thickness and average porosity but with a uniform porosity distribution"* (p.7) — 만든 법 [미확인].
- ⚠ Fig 5 와 Fig 8 의 전극은 서로 다르다 — C2 · C3 (≈108 µm · ≈28 %) ↔ 기공 경사 (≈127 µm · ≈38.5 % · 150 MPa 가정 [카드 산술]) → 두 그림의 용량을 서로 견주지 않는다.

### 3-6. 검증 (Fig 2 · C2 · D1 · p.3–4 · p.11–12)
- **형상**: SEM 단면 넷 (Wood [37]) ↔ DEM 정면 투영 (Fig 2a–d) — 정량 없음 · *"which used the same material system and NCM particle size"* (p.3) · NCM 조성 [미확인].
- **두께 (Fig 2e–f [판독] · 0 / 100 / 200 / 300 MPa)**:

| 전극 | 실험 두께 µm | 계산 두께 µm | 실험 압축률 % | 계산 압축률 % |
|---|---|---|---|---|
| 얇은 (80 µm) | 80.0 · 61.0 · 57.2 · 53.7 | — · 61.6 · 57.4 · 54.2 | 0 · 23.7 · 28.5 · 32.2 | — · 23.0 · 28.2 · (가림) |
| 두꺼운 (183 µm) | 183.1 · 151.0 · 116.0 · 107.1 | — · 149.4 · 114.3 · 110.5 | 0 · 17.5 · 36.6 · 41.5 | — · 18.4 · 37.6 · 39.5 |
- 인쇄 (p.3): *"For the thin electrode, the initial thickness of 80 μm decreased to 54 μm after calendering … the thick electrode, the thickness decreased from 183 μm to 110 μm … the thick electrode exhibited a consistently larger compression ratio—approximately 5% higher than that of the thin electrode at 300 MPa"* — 인쇄값으로 39.9 − 32.5 = **7.4 %p** [카드 산술] · 100 MPa 에서는 두꺼운 쪽이 **작다** (계산 18.4 ↔ 23.0 · 실험 17.5 ↔ 23.7 [판독]) → 'consistently' 는 그림과 어긋남 (§11-7).  계산 ÷ 실험 두께 (300 MPa) 얇은 1.009 · 두꺼운 1.032 [카드 산술].
- 부록 C (p.11): 처음 구조 = Ademmer [49] 싱크로트론 단층촬영의 *"material system, composition, thickness, porosity, and AM particle size distribution"* 와 같게 · *"applying 300 MPa pressure to the RVE also aligns with the experimental data"* — 그 값들 · 실험 두께의 상태 (누른 채 / 뺀 뒤) [미확인].
- **용량 (Fig D1b [판독] · mAh g⁻¹)**: 0.2C 167.0 ↔ 165.1 (1.011) · 0.5C 156.9 ↔ 153.0 (1.026) · 1C 142.9 ↔ 138.1 (1.035) · 2C 108.9 ↔ 103.1 (1.056) · 3C 64.9 ↔ 55.0 (**1.181**) (계산 ↔ 실험 [59] · 괄호 = 비 [카드 산술]) ↔ 본문 *"The simulated specific capacity at four discharge rates shows excellent agreement"* (p.4 · 그림은 다섯 율 §11-6).  Lu [59] 의 어느 전극 · 그림 자료인지 · 그 두께 · 기공 숫자 [미확인] (`lu2020_…` 카드: 실험 자료 = AM_LH NMC622 2 mAh cm⁻² (Fig 5E · F) · 1 · 2 · 3 mAh cm⁻² (Fig 8) — 율별 실험 용량 표 없음 [다른 카드 L31 · L214]).

---

## 4. ★ 방법 — 계산 사슬 · 넘김 · 수치

### 4-1. 계산 사슬 (재구성)
DEM RVE 생성 (방법 [미확인] — 같은 그룹 2025 는 건조 DEM 끝 구조를 썼다 [다른 카드 lyu2025 L22]) → 위판 일정 속도 하강 → 압력 단계 20 · 50 · 100 · 150 · 200 · 250 MPa 의 상태 (한 번의 연속 압축 중 순간인지 단계별 따로인지 [미확인]) → 두께 · 압축률 · 층 기공 · 배위수 → C2 · C3 압연 끝 구조의 AM 중심 · 반지름 → Java 재구성 [68] → 구 → COMSOL 반쪽 전지 (20 × 20 × 175 µm) → 0.5–5C 방전 → SOL 지도 · 전압–용량.
두 단계: 한 층 → 250 MPa → 압력 제거 (springback) → 새 층 얹음 → 두 번째 압연 (0–150 MPa) → FEM (같은 두께 · 평균 기공의 균일 대조와 견줌).
- **압력을 뺄 때 (탈압)**: 두 단계 압연 1 단계 뒤 한 번뿐 · 되돌아옴 숫자 미인쇄 (§3-4) · 단일 압연 결과는 압력별 점만.

### 4-2. ★ DEM → FEM 넘김 (§2.1 · p.2)
| 항목 | 내용 | 표지 |
|---|---|---|
| 넘기는 것 | *"the spatial coordinates and radii of all AM particles are exported from the DEM simulation to fully define the 3D electrode microstructure"* · *"Microstructural descriptors, including spatially resolved porosity gradients, are mapped onto the FEM mesh"* (사상 방법 [미확인]) | [인쇄] p.2 |
| 만드는 법 | *"processed through an in-house geometric reconstruction algorithm implemented in Java [68] to generate the corresponding spherical particle geometry"* → *"directly used as the cathode domain"* | [인쇄] p.2 |
| 넘기지 않는 것 | 접촉력 · 응력 · 결합 상태 · CBD 구의 위치 (CBD + 전해질 = 혼합상) · 겹침 (구가 겹친 채인지 · 깎았는지 · 합쳤는지 [미확인]) | [인쇄] p.2 · [미확인] |
| 창 | DEM 50 × 50 µm ↔ FEM 20 × 20 µm — 고른 법 · 몇 군데 [미확인] · 창 안 AM ≈14 (큰) + ≈107 (작은) 개 [카드 산술: 층 고체 39.0 µm × 400 µm² × 0.842 ÷ ⟨V⟩ · 큰 923.6 · 작은 122.5 µm³] · 옆 크기 = 큰 입자 지름 12 µm 의 1.7 배 | [카드 산술] |
| 시점 · 상태 | 압연 끝 (C2 · C3 · 두 단계) · 누른 채 / 뺀 뒤 [미확인] | [미확인] |
| 방향 | 한 방향 (FEM → DEM 되먹임 없음 · 사이클 · 팽창 없음) | [인쇄] |
| 우리와 | 우리 DEM 덤프 → 접촉망 Kirchhoff · MPM 상 격자 → 복셀 FV (STEP3) 와 같은 '한 방향 기하 넘김' 부류 — 다른 점: 그들은 AM 만 구로 넘기고 무른 상 (CBD) 을 혼합상으로 녹인다 (우리 SE 는 수송 상이라 그렇게 못 한다) | [카드 관찰] |

### 4-3. 수치 · 비용 · 재현
| 항목 | 내용 | 표지 |
|---|---|---|
| DEM 수치 | 판 속도 · 시간 간격 · 감쇠 계수 (γ_n · γ_t) · 결합 세기 · 반복 (시드) 수 · 계산 시간 [미확인] · 입자 수 어림 ≈8 × 10³ | [미확인] · [카드 산술] |
| FEM 수치 | 망 · 요소 수 · 풀이기 · 시간 · 메모리 [미확인] | [미확인] |
| 맞춘 값 | **0** — 입력 전부 문헌값 (표 1 · 2) · 민감도 두 팔 (E_AM · 결합 강성 · Fig E1) · 검증 셋 (서로 다른 전극) | [인쇄] |
| 공개 | *"Data will be made available on request."* (p.13) · 코드 없음 | [인쇄] |

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 문장**: *"Among these, the DEM is well-suited for simulating particle rearrangement [60,61] and contact evolution [62,63] during calendering, and the FEM is widely used to analyze electrochemical behavior at the particle [64] and electrode [65–67] scale. However, using either method alone is insufficient to capture both mechanical and electrochemical aspects."* (p.2) · *"Moreover, the application of the PBM model ignores the viscoelastic and adhesive properties introduced by the binder in actual electrodes, which may influence the microstructural evolution of the electrodes. Future improvements could incorporate more realistic binder behavior to enhance predictive accuracy."* (p.10).  단단한 구 · 형상 고정 · 소성 · 점접촉 독립 · 겹침 상한에 대한 말은 **없다** (AM 파괴 문헌 [14, 15, 84] 를 서론에서 인용만 · [84] = 같은 그룹 압연 균열 DEM).
- **(ii) 소성 · 큰 변형** = **넣지 않았다 · 이유 · 비용 논의 없음**.  AM 은 탄성 Hertz–Mindlin 구 (항복 · 소성 · 파괴 없음) — 원 출처 [62] (`sangros2019_…`) 의 Thornton–Ning 항복을 쓰지 않음 [다른 카드 · 카드 관찰] · ref [85] (So 2021) 은 Hertz + 이력 + 경도 H 캡 (접촉 소성) 인데 이 논문은 Hertz–Mindlin 꼴만 인용 [다른 카드 so2021 L52–L64].  치밀화 기전 = *"it is concluded that AM particle rearrangement driven by contact mechanics is the primary dominant mechanism leading to higher compression ratio of electrodes composed of larger particles. That is, larger particles can more easily overcome friction to achieve particle rearrangement [56,59], whereas smaller particles facilitate the formation of a more uniform contact network, thereby enhancing structural stability and hindering particle rearrangement."* (p.6) + CBD 결합의 변형 · 파단 · *"consistent with that of Liao et al. [75], who reported that electrodes comprising large AM particles experienced a higher structural strain"* (입자별 FE · p.6).  '소성' 낱말 = 참고문헌 제목 한 번 ([78]) 뿐.
- **(iii) 차원**: 3D (DEM · FEM) · 같은 그룹 2D DEM [83] (Energy Technol. 2024) 은 *"additional theoretical details can be found in our previous work [82–84]"* (p.9) 로만 · 2D → 3D 진술 없음.
- **(iv) 탈압**: *"After pressure removal, partial elastic recovery ("springback") occurred (Fig. 6(c))."* (p.7) · 숫자 = 아래 층 39.4 % · 64.4 µm (뺀 뒤 · 두 번째 압연 전) 뿐 · 되돌아옴 ≈ +19–22 % 는 렌더 판독 · 접촉 항복이 없으므로 이 되돌아옴은 탄성 (AM Hertz · CBD 결합 · 파단 뒤 선형 접촉) 에서만 나온다 [카드 추론] · 단일 압연 결과의 상태 [미확인].

### 4-5. 기법 미니 용어집
- **캘린더링 (calendering · 압연)** = 롤 사이로 전극 도막을 눌러 두께 · 기공을 줄이는 공정 — 이 논문은 평판 하강으로 근사.
- **CBD (탄소-바인더 덩어리)** = 도전재 + 바인더 (+ 그 안 작은 기공) 를 한 상으로 본 것 — 여기서는 지름 2 µm 구.
- **PBM (평행 결합 모형)** = 두 입자 사이 원기둥 결합이 힘과 모멘트를 전달하고 세기를 넘으면 끊어지는 DEM 결합 (Potyondy–Cundall 류).
- **Mohr–Coulomb 파단 기준** = 전단 세기가 법선 응력에 따라 선형으로 커지는 파단 규칙.
- **RVE (대표 체적 요소)** = 전체 거동을 대표한다고 보는 작은 상자.
- **SOL (리튬화 상태)** = c_p / c_p,max.
- **반쪽 전지 (half-cell)** = 양극 + 분리막 + Li 금속 음극.
- **두 단계 압연** = 첫 층을 압연한 뒤 둘째 층을 덮고 다시 압연 → 아래 층이 두 번 눌려 더 치밀.
- **springback (되돌아옴)** = 압력을 뺀 뒤 두께가 늘어나는 탄성 회복.
- **압축률 (compression ratio)** = (처음 두께 − 두께) ÷ 처음 두께 (Fig 3f · 2e–f 축 이름 'compression rate').

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 (a–d) `fig_1` | 롤 압연 모식 · 이중층 모식 · DEM RVE (50 × 50 × 150 µm) · FEM 반쪽 전지 (20 × 20 × 175 µm) — (b) · (c) 의 큰 / 작은 입자 자리가 본문과 반대 (§11-2) | 넘김의 꼴 |
| 2 (a–f) `fig_2` · 패널 `fig_2e` · `fig_2f` | SEM ↔ DEM 형상 넷 · ★ 얇은 · 두꺼운 전극 두께 · 압축률 vs 압력 (실험 [49] 실선 · 계산 점선) | 압력–두께 검증의 꼴 (LIB) |
| 3 (a–f) `fig_3` · 패널 `fig_3e` · `fig_3f` | 3D 네 줄 (압연 전 · 50 · 100 · 150 · 250 MPa) · ★ 두께 · 압축률 vs 압력 (0 · 20 · 50 · 100 · 150 · 200 · 250 MPa · C1–C4) — 3D 줄 순서가 캡션과 어긋남 (그림으로 읽으면 (a) 작은 입자 한 층 · (b) 큰 한 층 · (c) 아래 큰 / 위 작은 · (d) 아래 작은 / 위 큰 = C4 · C1 · C2 · C3 · §11-3) | 큰 / 작은 입자 침대의 압축 차 (모델 안) |
| 4 (a–f) `fig_4` · 패널 `fig_4a` · `fig_4b` · `fig_4d` · `fig_4f` | ★ C2 · C3 층 기공 vs 압력 · 접촉망 3D (빨강 AM–AM · 파랑 AM–CBD · CBD–CBD) · AM 배위수 막대 | 층별 기공 · 고체 보존 점검 |
| 5 (a–i) `fig_5` · 패널 `fig_5i` | C2 · C3 SOL 지도 (0.5 · 1 · 3 · 5C · 색 0.5–1) · ★ 전압–용량 | 입자 배치의 고율 효과 (액체) |
| 6 (a–e) `fig_6` | 두 단계 압연 순서 (한 층 → 250 MPa → springback → 새 층 → 두 번째 압연) | ★ 단계 6 의 '뺀 뒤 다시 누르기' 시험 꼴 · 되돌아옴 렌더 판독 |
| 7 (a–c) `fig_7` · 패널 `fig_7b` · `fig_7c` | 두 번째 압연 3D (50 · 100 · 150 MPa) · ★ 층 기공 · 층 두께 vs 압력 | 다시 누를 때 이미 눌린 층의 추가 치밀화 |
| 8 (a–i) `fig_8` · 패널 `fig_8i` | 기공 경사 ↔ 균일 SOL 지도 · ★ 전압–용량 (5C 균일 곡선은 범례와 다른 청록) | — |
| C1 `fig_C1` | AM 반지름 분포 (정규 · μ 3 · 6 µm · σ 0.5 µm) | 입도 입력 꼴 |
| C2 `fig_C2` | 얇은 (80 µm) · 두꺼운 (183 µm) RVE 압연 전 / 뒤 (300 MPa) | — |
| D1 (a–b) `fig_D1` · 패널 `fig_D1b` | 반쪽 전지 RVE · ★ 용량 vs 율 (계산 ↔ 실험 [59] · 0.2–3C) | — |
| E1 (a–d) `fig_E1` · 패널 `fig_E1b` · `fig_E1c` · `fig_E1d` | ★ 민감도 (E_AM 142 / 75 GPa · 결합 강성 1.35 / 0.8 × 10¹¹ N/m³) 의 층 기공 vs 압력 | 매개변수 민감도 표의 꼴 |
| 표 1 `tab_1` · 표 2 `tab_2` | DEM 입력 (재구성 렌더) · FEM 입력 | 입력값 · 출처 칸 |
| 식 크롭 12 + 묶음 2 | `eq_A1_translational_motion` · `eq_A2_rotational_motion` · `eq_A3_hertz_mindlin_spring_dashpot` · `eq_A4_pbm_max_tensile_stress_as_printed` · `eq_A5_pbm_max_shear_stress_as_printed` · `eq_B1_solid_diffusion` · `eq_B2_solid_charge_conservation` · `eq_B3_electrolyte_mass_balance` · `eq_B4_electrolyte_charge_conservation` · `eq_B5_electrolyte_current_density` · `eq_B6_butler_volmer_as_printed` · `eq_B7_cbd_charge_conservation` · `eq_A1_A5_dem_set` · `eq_B1_B7_electrochem_set` | 보고서에 붙일 DEM · 전기화학 지배식 (A4 · A5 · B6 은 '인쇄 그대로' — §11) |
| 근거 문단 20 | `txt_p1_*` (초록 · 처음 · 검증 주장) · `txt_p2_*` (DEM/FEM 단독 불충분 · 넘김 · RVE 입력 · 반쪽 전지) · `txt_p3_*` (두께 검증 · 5 %) · `txt_p4_*` (네 율 검증 · 150 → 106–113 µm) · `txt_p6_*` (재배열 기전 · 층 기공) · `txt_p7_*` (배위수 · 용량 · 두 단계 · springback · 층 처음값) · `txt_p7_p9_*` (기공 경사 용량) · `txt_p9_*` (결론 · 70 %) · `txt_p10_*` (접촉 법칙 · PBM 한계) · `txt_p11_*` (부록 C) · `txt_p12_*` (부록 E) | 원문 인용용 |

## 6. Post-processing ★
- **무엇을**: 판 위치 → 두께 · 압축률 · 층 기공 (층 소속 입자) · AM 배위수 · 접촉망 3D · SOL 지도 · 전압–용량 (2.8 V 끝 용량).
- **안 한 것**: 응력 · 하중 · 힘 사슬 · 판 반력 · 접촉 면적 · 겹침 분포 · 결합 파단 수 · 전기 · 이온 전도도 (*"a denser contact network enhances electrical conductivity"* p.7 은 문헌 근거 문장 · 계산 없음) · tortuosity · 층별 배위수 · 반복 (시드) · RVE 크기 · 창 크기 시험 · 단일 압연의 탈압 · 두 단계 압연의 실험 대조.
- **이 카드의 후처리**: 원 래스터 판독 210 행 (Fig 2e–f · 3e–f · 4a–b · 4d · 4f · 5i · 7b–c · 8i · D1b · E1b–d) · Fig 3 3D 줄 순서 점검 (렌더 높이 비) · Fig 6 렌더 높이 → 되돌아옴 · 고체 보존 점검 (층 · 전체) · 입자 수 · 창 안 입자 수 어림 · 비 · 차.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 계 | 액체 LIB 양극 NCM + CBD (92 : 8) · SE 없음 | ASSB 복합 양극 NCM + LPSCl (+ 첨가제) | 수송 상 · 무른 상이 다르다 |
| 무른 상 | CBD 지름 2 µm 구 · E 0.76 GPa · 결합 (PBM) | SE (DEM E_eff 1.35 GPa · 18 배 연화 · hooke/hysteresis) | E 는 같은 자리 (≈1 GPa) 지만 **같은 양 아님** — CBD = 문헌값 (출처 대조 못 함) · 우리 = 기공에 맞춘 보정 매개변수 (frame [2]) |
| AM | E 142 GPa · ν 0.3 · 탄성 Hertz–Mindlin (항복 없음) | E_CAM 140 GPa (DEM) · MPM 에서는 고정 골격 | 같은 자리 |
| 압력 · 상태 | 평판 0–250 MPa (검증 300) · 누른 채로 읽힘 | 300 MPa · 판 고정 이완 | 범위 비슷 · 상태 정의 [미확인] |
| 기공 | 48 → 26–30 % (250 MPa · DEM 구) | 랩 표준 순수 SE 10–13 % (300 MPa · 1.64 g/cm³) · 우리 복합 15.6 % (real_14) | 견줄 수 없다 (§7-2) |
| 넘김 | DEM AM 구 → FEM 전기화학 (기하 · 한 방향) | DEM 덤프 → 접촉망 σ · MPM 상 → STEP3 복셀 σ · DEM AM → MPM 골격 (scaffold) | 같은 '한 방향 기하 넘김' — 우리는 응력 · 접촉 (Holm) 을 넘기는 쪽이 따로 있다 |
| 탈압 | 두 단계 압연의 렌더 한 장 (≈ +19–22 % [판독]) | DEM 언로딩 키트 (진행) · MPM 제하 없음 | 되돌아옴 표적은 못 준다 |
| 형상 | 구 고정 · 소성 없음 | MPM 소성 형상 변화 (SE) | MPM 고유 쪽은 이 논문에 없다 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 압력 · 상태 | 기공 기준 | 기공 |
|---|---|---|---|---|
| **랩 표준** | 순수 LPSCl | 300 MPa | 진밀도 **1.64** (고정) | **10–13 %** |
| 이 논문 (단일 압연) | NCM + CBD 92 : 8 (LIB) | 250 MPa · 누른 채로 읽힘 | DEM 구 부피 (AM + CBD = 고체) | 26.8–29.8 % (전체 [카드 산술]) · 층 26.5–29.0 % [판독] |
| 이 논문 (두 단계 · 두 번째) | 같음 | 150 MPa | 같음 | 위 41.6 · 아래 35.2 % [판독] |
| 이 논문 (검증 · 얇은 / 두꺼운) | NCM 양극 ([49]) | 300 MPa | 두께만 | 기공 숫자 없음 |
- 이 표는 **"랩 표준과 다른 문헌 값"** 의 자리다 — 재료 (LIB · CBD) · 무른 상 · 기공 정의 (CBD 를 고체로) · 상태가 다 다르다.  CBD 안 나노 기공 · 전해질 혼합상은 FEM 쪽에서도 따로 세지 않는다.

### 7-3. '같은 압력에서 큰 입자 층이 더 치밀' ↔ 우리 결과
- 이 논문: AM 만의 침대 (+ 무른 CBD) 에서 큰 AM (반지름 6 µm) 침대가 작은 AM (3 µm) 보다 더 눌린다 (압축률 29.1 ↔ 25.9 % @ 250 MPa [판독]) · 해석 = 재배열 (마찰을 넘기 쉬움) ↔ 작은 입자의 고른 접촉망 (p.6) — 다른 해석 (입자 수 · 접촉 수 차이 · 판 경계 효과 · CBD 몫) 을 가르는 계산은 없다 [카드 관찰].
- 우리 (CLAUDE.md 2026-06-09 · DEM 코퍼스): **SE 입경** 이 클수록 SE 많은 쪽에서 기공 ↓ · AM 많은 쪽에서 ↑ (조성에 따라 교차) — 해석 = 충전 (packing) 기하.  ⇒ 같은 '입경 → 치밀화' 질문이지만 **축이 다르다** (그들 = AM 입경 · 무른 상 8 % · 우리 = SE 입경 · 복합) — 값 · 방향을 옮기지 않는다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: DEM 압연 (구 · 재배열 · 결합) 의 층별 압력 축 · 그 구조 위의 전기화학 (FEM) — DEM 쪽 일 + 수송 쪽 일 (액체).
- **없는 것**: 입자 형상 변화 · 소성 · 파괴 · 응력 · 하중 몫 · 접촉 면적 · 전도도 · 탈압 숫자.  ⇒ 우리 MPM 고유 (소성 형상 · 공극 메움) 쪽에는 아무것도 주지 않고, 우리 DEM 쪽에 '층별 압력 축 · 두 단계 시험 꼴 · 넘김의 빈칸 목록' 을 준다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) **층 기공 = 층 소속 입자 고체 ÷ 층 두께** 꼴과 그 **고체 보존 점검** (두 그림이 ±1 % 안에서 맞음 — §3-3) → 우리 층상 · 경사 침대의 층 연산자를 등록할 때 '층 경계 = 입자 소속 (처음 층) 인가 z 고정인가' 칸 + 고체 보존 점검을 같이 (2) 무른 상 (CBD) 을 고체로 세는 기공 ↔ 실험 기공 (CBD 안 기공 포함 여부) 의 정의 차이를 칸으로 | 압력 · 두께 · 층 기공의 정의 원문 [미확인] · 진밀도 분모 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 (DEM ≈8 × 10³ 입자 [카드 산술] · FEM 메모리 [미확인]) | — |
| **단계 2 · 3** (2D MPM · 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (SE 없음) | — |
| **단계 5** (3D 복합 압밀) | ★ 이중층 (층마다 입경이 다른) 침대의 압력 축 꼴 — 층 기공 차가 중간 압력 (100 MPa) 에서 최대 · 끝 (250 MPa) 에서 작아진다 (C2 11.6 → 1.7 %p [판독]) → 우리 층상 · 경사 복합 (믹서 층상 캠페인 · 경사 후막) 을 누를 때 '끝 상태 경사는 중간 경사보다 작을 수 있다' 를 결과 전 대조 항목 후보로 | LIB · 무른 상 8 % · AM 탄성 구 — 값 전이 없음 |
| **단계 6** (탈압 · 되돌아옴) | ★ (1) **두 단계 시험 꼴** = 누름 → 뺌 (되돌아옴) → 새 층 얹음 → 다시 누름 (Fig 6) — 우리 DEM 언로딩 키트 다음의 '다시 누르기' 점검 (뺀 뒤 구조가 다시 눌릴 때 어디까지 따라가나) 으로 (2) 되돌아옴 ≈ +19–22 % (두께 · 렌더 판독) 는 **항복 없는 탄성 구 + 무른 결합** 의 값 — 우리 hooke/hysteresis (이력) DEM 의 되돌아옴과 같은 양이 아니다 | 숫자 미인쇄 · 렌더 판독 낮은 신뢰 · 단일 압연 탈압 없음 |
| **단계 7** (형상 · 피복 · 수송) | 흐름 밖: DEM 구 → 전기화학 FEM 넘김의 빈칸 목록 (겹침 처리 · 무른 상 혼합 · 창 크기 · 누른 채 / 뺀 뒤) — 우리 STEP2 → STEP3 · DEM → 접촉망 넘김의 등록 칸과 같다 · 고율 용량에 입자 배치 (분리막 쪽 작은 입자) 가 크게 걸린다는 액체 쪽 결과 (5C 1.8 배) | 액체 전해질 · 전도도 숫자 없음 · 창 20 µm |
| **후보 D0** (지금의 DEM) | 같은 꼴 (구 · 점접촉 · 탄성) 의 LIB 판 — 결합 (PBM) 으로 무른 상을 잇는 것 · 큰 / 작은 AM 침대 압축 차 (모델 안) · 매개변수 민감도 (E_AM 반 → 층 기공 ≈ −3 %p · 결합 강성 0.59 배 → ≈ −1.5 %p [카드 산술]) | 연화 (18 배) 같은 보정 없음 · 맞춘 값 0 (문헌값) |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 판 = 일정 속도 하강 · 집전체 고정 — 판 접촉 매개변수 (마찰 · 결합) [미확인] | — |
| **후보 A · A′ · B** | 없음 · B 쪽 근거 인용 하나 ([75] Liao 2024 입자별 FE: 큰 AM 침대의 변형률이 크다) | 원문 미확인 (§12) |
| **후보 C · C′** (큰 변형 · 항복 캡 DEM) | 없음 — 오히려 [62] 의 Thornton–Ning 항복을 **뺀** 예 (§4-4) | — |
| **후보 M0** (균질화 압밀) | 두께 · 압축률 vs 압력 곡선 (C1–C4 · 얇은 / 두꺼운) — LIB 침대의 균질화 곡선 맞춤 자료로만 | 상태 · 정의 [미확인] |
| **U0–U6** | **U4** (판 분리) 쪽 꼴 하나: 두 단계 압연의 '압력 제거' (판이 침대에서 떨어지는 순간은 그리지 않음) | 해상도 · 수렴 시험 없음 |
| **R1–R7** | **R1** AM 이 움직이고 접촉망이 생김 (AM 배위수 0.15 → 2.7) — 하중 몫 숫자 없음 · **R2** 마찰 0.25 · 결합 파단 → 선형 접촉 · **R4** 두 단계의 springback (렌더) · **R5** 맞춘 값 0 (문헌값 · 민감도만) | R3 · R6 (형상) · R7 (AM 파괴) 없음 |
| **결과 전 대조 항목** | (1) 같은 압력에서 큰 AM 침대가 작은 AM 침대보다 더 눌린다 (압축률 29.1 ↔ 25.9 % · LIB) — 모델 안 주장 · 기전 미분리 (2) 이중층의 층 기공 차가 중간 압력에서 최대 (3) 다시 누를 때 이미 눌린 층도 더 치밀해진다 (39.4 → 35.2 % @ 150 MPa) — 전부 [판독] · 'LIB · CBD · 평판 · 상태 미상' 표지와 함께 | 값 비교 금지 (계 · 재료 다름) |

- **재료 · 차원 · 조건 차이**: 재료 NCM + CBD (LIB) ↔ 우리 NCM + LPSCl · 무른 상 8 % 질량 ↔ SE 15–30 % · 3D = 같음 · 평판 = 같음 (우리도 판) · 0–250 MPa ↔ 300 MPa · AM 반지름 3 · 6 µm ↔ 우리 AM_S · AM_P · 액체 전해질 반쪽 전지 ↔ 고체 전해질.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **넘김 등록 칸 넷** — DEM 구조를 다른 계산 (MPM · 복셀 FV · FEM) 으로 넘길 때 (a) 누른 채 / 뺀 뒤 (b) 겹침 처리 (겹친 채 · 깎음 · 합침) (c) 무른 상을 형상으로 넘기나 혼합상으로 녹이나 (d) 창 크기 · 위치 · 반복 — 이 논문은 넷 다 미기재 (§4-2) · 우리 STEP2 → STEP3 · DEM → 접촉망 manifest 에 칸이 있는지 점검 (단계 7).
2. **층 연산자 + 고체 보존 점검** — 층별 기공을 낼 때 '층 고체 × 층 두께' 가 전체 두께와 맞는지 (이 논문 ±1 %) 를 결과 전에 등록 (단계 0 · 믹서 층상 · 경사 전극).
3. **두 단계 시험** — 누름 → 뺌 → (새 층) → 다시 누름 은 언로딩 키트 다음 검증 꼴 · 다시 누를 때 첫 압력보다 낮은 압력에서도 아래 층이 더 치밀해진다 (39.4 → 35.2 % @ 150 MPa) → 뺀 뒤 구조의 '기억' 을 보는 값 (단계 6 · R4).
4. **창 크기** — FEM 창 20 µm = 큰 입자 지름의 1.7 배 (큰 입자 ≈14 개) 로 5C 용량을 비교한 것은 창 의존을 따로 재지 않으면 위험 → 우리 STEP3 · STEP4 의 RVE · 창 크기 보고에 '큰 입자 지름당 창 길이' 칸 (흐름 밖: 수송 · 반응 계산).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "A coupled DEM–FEM framework (PFC3D plate calendering of a 3D two-layer NCM/CBD RVE; AM centres and radii exported to a COMSOL half-cell) shows that, under the same pressure, the large-particle layer densifies more than the small-particle layer (layer porosity difference 11.6 %p at 100 MPa, 1.7 %p at 250 MPa, digitized) (Lyu et al., Int. J. Mech. Sci. 322 (2026) 111716)."
- "In that framework only the active-material geometry is handed over: contact forces, stresses and the binder-domain positions are not transferred; the carbon–binder domain and electrolyte are lumped into one mixed phase."
- 국문: *"Lyu 2026 의 DEM → FEM 결합은 AM 구 (중심 · 반지름) 만 넘기는 한 방향 기하 넘김이다 — 응력 · 접촉은 넘기지 않는다."*
- 국문: *"두 단계 압연 (250 MPa → 뺌 → 새 층 → 다시) 의 되돌아옴은 원문에 숫자가 없다 (3D 렌더 판독 ≈ +20 %)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **'for the first time'** (초록 p.1 · 결론 p.9) — 자기 참고문헌 [16] (Ge 외 2023 · DEM + 전기화학 모델 · XCT) · 정본 `du2025_…` (DEM → FEM · 2025 · 이 논문 미인용) · [13] (Lim 2025 가상 압연 → 설계) 가 앞선다 → '이중층 경사 전극의 압연 → 방전' 으로 범위를 좁혀야 성립.
2. **Fig 1(b)–(c)** 캡션 · 그림 = 작은 입자가 집전체 쪽 · 큰 입자가 판 쪽 ↔ §2.2 본문 *"Large AM particles are placed near the CC side, and smaller particles are placed near the separator side"* — 그림 1 은 C3 꼴 · 본문은 C2 꼴.
3. **Fig 3(a)–(d) 3D 줄 순서** = 캡션 (C1 · C2 · C3 · C4) 이 아니라 C4 · C1 · C2 · C3 로 읽힌다 (§3-3).
4. **식 (A4)–(A5)** 인쇄: σ_max = F_n/A + M_t·R/J · τ_max = F_s/A + M_b·R/I — 인장에 비틀림 (J) · 전단에 굽힘 (I) 을 붙였다.  표준 PBM 과 같은 그룹 2025 (식 21–22) 는 인장 = 굽힘 / I · 전단 = 비틀림 / J [다른 카드 lyu2025 L60] → 바뀐 것으로 읽힌다.  크롭 이름에 '_as_printed'.
5. **식 (B6)** Butler–Volmer 인쇄 = i₀ (exp(α_a F η/RT) − exp(α_c F η/RT)) — 둘째 지수의 음부호가 없다 (α_a = α_c = 0.5 면 인쇄식은 0).
6. **'four discharge rates'** (§3.1.3 p.4) ↔ Fig D1(b) 다섯 율 (0.2–3C) · 3C 계산 ÷ 실험 1.18 을 *"excellent agreement"* 로 적음.
7. **'thick … consistently larger compression ratio — approximately 5% higher … at 300 MPa'** (p.3) ↔ 인쇄값 7.4 %p · 100 MPa 에서는 두꺼운 쪽이 작다 (§3-6).
8. **'calendering naturally forms a favorable gradient'** — 끝 상태 (250 MPa) 의 층 기공 차는 C2 1.7 %p [판독] · C2 ↔ C3 5C 차 (98 ↔ 54) 에는 기공 경사보다 입자 배치 (분리막 쪽 작은 입자 = 짧은 확산 거리) 몫이 클 수 있다 — 저자도 SOL 로 입경 몫을 말한다 (p.7) · 두 몫을 가르는 계산 (같은 기공 · 배치만 바꾼 FEM) 없음 [카드 추론].
9. **Fig 5 ↔ Fig 8 전극이 다르다** — C2 · C3 (≈108 µm · ≈28 %) ↔ 기공 경사 (≈127 µm · ≈38.5 %) · 대조 전극 (같은 두께 · 평균 기공 · 균일) 만든 법 · 두 단계 전극의 입경 [미확인].
10. **검증 셋이 서로 다른 전극** — 이중층 결과 (층 기공 · 두 단계) 자체의 실험 대조 없음 · 두 단계 압연의 실험 원전 [49] 은 두께 검증에만 씀.
11. **FEM 창 20 × 20 µm** (큰 입자 지름의 1.7 배 · 큰 입자 ≈14 개 [카드 산술]) · 창 선택 · 반복 없음 → 고율 용량의 창 의존 [미확인].
12. **Fig 1(d) 175 µm** = 분리막 25 + 압연 전 150 µm (압연 뒤 106–113 µm 와 다름).
13. **'copper foil as the CC'** — 양극 집전체라면 보통 Al · 어느 쪽 집전체인지 [미확인].
14. **같은 그룹 2025 와 다른 입력** (E_CBD 0.65 → 0.76 · ν 0.25 / 0.2 → 0.3 · 마찰 0.12 / 0.1 → 0.25 · ρ 4.74 → 4.75 · 94 : 6 → 92 : 8) — 설명 없음 · E_CBD 0.76 의 출처 ([56, 62]) 를 정본 카드로 대조 못 함 (§3-1).
15. **NCM 조성 미기재** — FEM 물성은 NMC532 ([70]) · NMC333 / 523 ([71]) 출처 · 검증 셋도 서로 다른 NCM ([37] · [49] · [59]).
16. **오타 · 표기**: 'calendaring' (§2.2 · ref [62] 제목은 원저 그대로) · Fig 6 캡션 'uncalendared' · Fig 2(e) 범례 'Experimentions' · Fig E1(b)–(c) 축 'Pressuer' · Fig 8(i) 5C 균일 곡선 청록 ↔ 범례 초록 · 키워드 'Dem–fem coupling' · ref [64] *"Int J Mech Sci 2025;12:111124"* (권 '12' — 같은 학술지의 다른 2025 인용은 301 · 302 · 307 · 308 · 309).
17. ⚠ **판독 값**은 원 래스터 보정 (눈금 잔차 ≤ 0.03 px 꼴 · 행마다 방법) — 그래도 [판독] 표지로만 인용 · Fig 6 렌더 높이는 원근 3D 라 **낮은 신뢰**.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 49 | Ademmer M, Prifling B, Weller M, Hilger A, Osenberg M, Manke I, Knoblauch V, Schmidt V. Investigating the influence of the calendering process on the 3D microstructure of single-layer and two-layer cathodes in lithium-ion batteries using synchrotron tomography. J Power Sources 2022;548:231960. | 두께 검증 자료 · 두 단계 압연 실험 · 층별 단층촬영 (질문 i · b) | 없음 (papers/ ls · grep · `qin2026_…` L36 도 [46] 으로 인용) |
| 16 | Ge R, Boyce AM, Shui Zhang Y, Shearing PR, Cumming DJ, Smith RM. Discrete element method and electrochemical modelling of lithium ion cathode structures characterised by X-ray computed tomography. Chem Eng J 2023;465:142749. | DEM → 전기화학 넘김의 앞 선례 (질문 h) | 없음 (`song2025_…` 가 인용) |
| 75 | Liao Z, Li H, Wang H, Liu B. Mesoscale mechanical models for active materials in lithium-ion batteries using the multi-particle finite element method. Extreme Mech Lett 2024;69:102154. | 큰 AM 침대 변형률 (p.6) · 입자별 FE (후보 B · 질문 l) | 없음 |
| 69 | Giménez CS, Finke B, Nowak C, Schilde C, Kwade A. Structural and mechanical characterization of lithium-ion battery electrodes via DEM simulations. Adv Powder Technol 2018;29(10):2312–21. | ν 0.3 · 결합 강성 1.35 × 10¹¹ · Hertz–Mindlin 출처 (질문 e) | 없음 |
| 56 | Zhang J, Huang H, Sun J. Investigation on mechanical and microstructural evolution of lithium-ion battery electrode during the calendering process. Powder Technol 2022;409:117828. | E_CBD 0.76 · E_AM · ρ 출처 · 판 속도 방식 · 재배열 근거 (질문 e) | 없음 — wishlist L232 (`du2025_…` · `yano2023_…` 가 인용) |
| 59 | Lu X, Daemi SR, Bertei A, Kok MDR, O'Regan KB, Rasha L, Park J, Hinds G, Kendrick E, Brett DJL. Microstructural evolution of battery electrodes during calendering. Joule 2020;4(12):2746–68. | 전기화학 검증 · 큰 입자 재배열 근거 | `lu2020_insitu_nanoct_calendering_microstructural_evolution` |
| 62 | Giménez CS, Finke B, Schilde C, Froböse L, Kwade A. Numerical simulation of the behavior of lithium-ion battery electrodes during the calendaring process via the discrete element method. Powder Technol 2019;349:1–11. | E_AM 142 · ρ 4.75 출처 · Thornton–Ning (이 논문은 항복을 뺌) | `sangros2019_dem_calendering_lib_electrode` |
| 85 | So M, Inoue G, Hirate R, Nunoshita K, Ishikawa S, Tsuge Y. Effect of mold pressure on compaction and ion conductivity of all-solid-state batteries revealed by the discrete element method. J Power Sources 2021;508:230344. | Hertz–Mindlin 인용 (So 는 경도 캡 접촉 소성) | `so2021_dem_mold_pressure_assb_coldpress` |
| 37 | Wood M, Li J, Du Z, Daniel C, Dunlop AR, Polzin BJ, Jansen AN, Krumdick GK, Wood DL. Impact of secondary particle size and two-layer architectures on the high-rate performance of thick electrodes in lithium-ion battery pouch cells. J Power Sources 2021;515:230429. | 형상 검증 SEM · 이중층 NCM 고율 실험 | 없음 (`pan2026_thesis_…` 가 인용) |
| 78 | Lundkvist A, Larsson P-L, Iyer AHS, Olsson E. Discrete element modelling of the elastic-plastic and viscoelastic properties of a lithium-ion battery electrode layer. Powder Technol 2024;443:119873. | 탄소성 · 점탄성 DEM (되돌아옴 · 질문 b · e) | 없음 — wishlist L106 |
| 60 | Ge R, Cumming DJ, Smith RM. Discrete element method (DEM) analysis of lithium ion battery electrode structures from X-ray tomography-the effect of calendering conditions. Powder Technol 2022;403:117366. | 마찰 0.25 출처 | 없음 |
| 61 | Song Y, Tan L, Gao K, He C, Wu Y, Li N, Yang L, Mao Y, Song W-L, Chen H-S. Insights into cathode densification of calendering process by the combination of in-situ CT and DEM. Powder Technol 2025;453:120667. | 재배열 · 치밀화 (서론) | `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` |
| 13 | Lim J, Song J, Kim KG, Koo JK, Lee H, Kang D, Kim YJ, Park J, Lee YM. Validating the virtual calendering process with 3D-reconstructed composite electrode: an optimization framework for electrode design. Small 2025;21(27):e2410485. | 가상 압연 → 설계 (서론) | `lim2025_virtual_calendering_framework` |
| 54 | Alabdali M, Zanotto FM, Duquesnoy M, Hatz A-K, Ma D, Auvergniot J, Viallet V, Seznec V, Franco AA. Three-dimensional physical modeling of the wet manufacturing process of solid-state battery electrodes. J Power Sources 2023;580:233427. | CGMD (서론) | `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` |
| 82 | Lyu YH, Dong SH, Gao LT, Guo ZS. Three-dimensional discrete element simulation of electrode structural evolution in lithium-ion batteries during drying and calendering. Int J Electr Power Energy Syst 2025;165:110521. | 같은 그룹 DEM 이론 · 입력 차이 (§3-1) | `lyu2025_3d_dem_drying_calendering_lib` |
| 83 | Lyu Y, Dong S, Guo ZS. 2D discrete element simulation of electrode structural evolutions in Li-ion battery during drying and calendering. Energy Technol 2024;12(11):2400583. | 같은 그룹 2D 판 (2D ↔ 3D 대조 후보 · 질문 g) | 없음 |
| 84 | Lyu Y, Dong S, Zhang T, Guo Z-S. Electrode crack evolution and failure mechanism during calendering: insights from discrete element method-based mesoscopic simulation. Eng Fract Mech 2025;321:111120. | Mohr–Coulomb 결합 파단 출처 · 압연 균열 | 없음 |
| 68 | Lyu Y, Dong S, Guo Z-S. Effect of calendering on structure and electrochemical performance of LiNi0.33Mn0.33Co0.33O2 cathodes via 3D reconstruction based on X-ray computed tomography images with different pressures. Energy Storage Mater 2025;82:104643. | Java 기하 재구성 · 전기화학 식 유도 | 없음 |
| 71 | Amin R, Chiang Y-M. Characterization of electronic and ionic transport in Li1-xNi0.33Mn0.33Co0.33O2 (NMC333) and Li1-xNi0.50Mn0.20Co0.30O2 (NMC523) as a function of Li content. J Electrochem Soc 2016;163(8):A1512–7. | σ_p(c) 출처 | `aminchiang2016_nmc_electronic_ionic_transport_vs_li` |
| 76 | Fu Z, Zhang R, Xu Z, Peng L. Elimination of electrode corrugations via a two-step calendering process. Int J Mech Sci 2025;301:110525. | 두 단계 압연 실험 (p.7) | 없음 |

---

## [미확인] 목록
- DEM: PFC3D 판 번호 · 판 속도 · 시간 간격 · 감쇠 계수 · Hertz–Mindlin 강성 식 · 결합 세기 (인장 · 전단 · 마찰각) · 결합 반지름 배수 · 결합이 생기는 거리 · 판 · 집전체 접촉 매개변수 · 처음 충전을 만든 법 · 입자 수 · 반복 (시드) 수 · 계산 시간 · PSD 가 수 / 부피 가중인지.
- 정의: 'calendering pressure' (판 힘 ÷ 면적?) · 두께 (판 위치 ↔ 가장 높은 입자) · 층 기공 (층 경계) · AM 배위수 (AM–AM 만?) · 압력 단계가 연속 압축의 순간인지.
- 상태: Fig 2 · 3 · 4 의 값과 FEM 에 넣은 구조가 누른 채인지 뺀 뒤인지 · Ademmer [49] 실험 두께의 상태 · 원 값.
- FEM: 망 · 요소 수 · 풀이기 · 시간 · i₀ · 처음 c_e · 유효 물성 보정 꼴 · 1C 정의 · 상한 전압 · 20 × 20 µm 창을 고른 법 · 겹침 처리 · 'porosity gradients' 를 망에 사상한 법 · 'copper foil as the CC' 의 자리 · 대조 균일 전극 만든 법 · 균일 0.5C · 1C 곡선 (가림).
- 두 단계: 두 번째 압연을 150 MPa 에서 멈춘 이유 · FEM 에 넣은 압력 · 두 층의 입경 · 첫 압연 뒤 되돌아옴 숫자.
- 재료: NCM 조성 · 전해질 (본문 미인쇄 · [73] 제목 = LiPF₆–EC–EMC) · E_CBD 0.76 의 원 출처 대조.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지: 1저자 메모 (Lyu · Dong · Guo 2026 · IJMS 322, 111716 · 제목) = 원문 첫 쪽과 같음 · 이름 전체 · DOI · 접수 · 수정 · 승인 · 온라인 날짜 · 연구비 번호는 첫 쪽 · p.9 에서 추가 · PDF 메타데이터 (*"International Journal of Mechanical Sciences, 322 (2026) 111716. doi:10.1016/j.ijmecsci.2026.111716"*) 와 같음 · 보충 자료 안내 없음 (부록 A–E 가 본문 안).
- 숫자: 글자 층 + 14 쪽 렌더로 대조 — 48 % · 92 : 8 · 2 µm · 50 × 50 × 150 · 20 × 20 × 175 µm · 25 µm · 0.5 · 1 · 3 · 5C · 2.8 V · 6.2 · 표 1 (142 · 0.76 · 0.3 · 4.75 · 2.2 · 0.25 · 1.35e11) · 표 2 (50061 · 12515 · 375 · 0.5 · 293.15) · 80 → 54 · 183 → 110 µm · 5 % · 300 MPa · 150 µm · 106–113 µm · 25–30 % · 26–30 % · 100 MPa · 0.15 → 2.7 · 250 MPa · 149 · 146 · 98 · 54 · 39.4 % · 64.4 µm · 48 % · 75 µm · ≈148 · ~120 · 97 · >70 % · 6 · 3 µm · σ 0.5 · 75 GPa · 0.8e11 — 전부 위치 확인.
- 낱말 전수 (글자 층): 'springback' 2 (본문 · Fig 6 캡션) · 'pressure removal' 1 · 'unload' 0 · 'stress' 3 (결합 식 + 참고문헌 제목) · 'plastic' 1 (참고문헌 제목) · 'rigid' 0 · 'time step' 0 · 'Bruggeman' 0 · 'mesh' 1 · 'Supplementary' 0 · 'first time' 2.
- 판독 보정: 각 그림의 큰 눈금 직선 맞춤 · 가려진 표식은 그리는 순서로 판정 · Fig 3e ↔ 3f · Fig 4a ↔ E1b · 층 기공 ↔ 두께 (고체 보존) 교차 대조.
- 정본 중복 확인: papers/ 파일 목록 (lyu20* = lyu2025 하나) · DOI · '111716' · 'two-layer' · 'Calendering behavior' grep — 카드 없음 (qin2026 인용만) · 같은 저자 2026 카드 없음.

## 🔗 관련 카드
- 이 논문을 인용한 카드: `qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode` (ref [45] · L36 · L40 · L438 · L506 · L652).
- 같은 그룹: `lyu2025_3d_dem_drying_calendering_lib` (ref [82] · 다른 논문 · 건조 + 압연 DEM).
- DEM → FEM 넘김 · 압연 DEM: `du2025_dem_fem_force_chain_collector_damage_calendering` · `lim2025_virtual_calendering_framework` · `ngandjong2021_dem_calendering_digital_twin` · `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` · `he2026_dem_calendering_inhomogeneity_areal_density` · `zhang2026_xct_dem_cathode_calendering_peel_calibration` · `schreiner2020_dem_calendering_lib` · `sangros2019_dem_calendering_lib_electrode` · `sangros2020_lib_electrode_dem_mech_elec_ionic` · `xu2023_realistic_am_shape_cgmd_calendering`.
- 압연 뒤 되돌아옴 (실측 · 계산): `diener2022_roll_gap_springback_calendering` · `kollenda2024_time_sensitivity_calendered_electrode_springback_storage` · `sangros2019_dem_calendering_lib_electrode` (ER 10–17 %).
- 실측 압연 구조 · 전기화학: `lu2020_insitu_nanoct_calendering_microstructural_evolution` (ref [59]) · `aminchiang2016_nmc_electronic_ionic_transport_vs_li` (ref [71]).
- 접촉 법칙: `so2021_dem_mold_pressure_assb_coldpress` (ref [85]).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

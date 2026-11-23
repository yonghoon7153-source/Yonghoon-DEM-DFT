<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md ·
     같은 그룹 · 같은 1저자의 앞 단계 = sun2026_dem_extrusion_recirculation_dry_electrode.md (트윈스크류 압출 + 재순환 DEM).
     쪽 표기 = 받은 ChemRxiv PDF 의 쪽 (p.1–2 = ChemRxiv 표지 · p.3–43 = 원고 본문 + 참고문헌 · 원고 자체 쪽 번호 없음).  보충 자료 (SI) = 본문이 가리키지만 PDF 에 없다.
     값 표지: [인쇄] = 본문 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv · 원 래스터 화소 · 눈금선 직선 맞춤 ·
     인쇄 범위와 ±0.02 %p · ±0.0001 S/m 안에서 같음) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] = 이 카드의 해석 ·
     [미확인] = 받은 PDF (43 쪽 전수) 에 없음.  원고 41 쪽은 텍스트 층 전수 + 그림 · 식이 있는 쪽은 렌더로 읽었고, 텍스트 층에서 깨진 단위 · 첨자는 렌더로 대조했다. -->
# 압출 DEM 필라멘트를 FFF 3D 프린팅으로 넘긴 입자 단위 사슬 (LAMMPS RHEO: SPH 점성 BC + 고체 구 AM · 가정한 냉각 상태 · BC 결합 연결) — 한 가닥 17 · 한 층 9 · 두 층 18 경우 · 두 층 전극 빈 곳 38.6–40.2 % (BC 나노 공극 10 % 가정 포함 42.8–44.3 %) · τ_Y 1.728–1.823 · 겉보기 σ_e 0.0985–0.1912 S/m (≈1.9 배) — Sun · Fernandez · Vigneaux · Franco (ChemRxiv 2026 · 동료 심사 전)

> slug `sun2026_fff_printing_extruded_filament_sph_dry_electrode_preprint` · DOI `10.26434/chemrxiv.15012329/v1` · type `simulation (DEM 압출 필라멘트 입력 → LAMMPS RHEO: SPH 점성 BC 입자 + 고체 구 AM · 상태 변수 냉각 규칙 · BC–BC / BC–AM 결합 · 복셀 FVM 확산 + 전자 전도) — 실험 없음 · 가압 · 탈압 없음 · ChemRxiv 원고` · PDF `1af7f66c-Microstructure-resolved_modeling_of_fused_filament_fabrication_of_lithium-ion_battery_electrodes.pdf` · digested `2026-11-23` · status ✅
>
> ⚠⚠ **ChemRxiv 원고 — 동료 심사 전 (preprint · not peer reviewed)**.  표지 (p.1–2) 바닥글: *"Posted on 17 November 2026 — CC-BY 4.0 — This is a preprint and has not been peer reviewed. Data may be preliminary."*  인용할 때 "ChemRxiv (2026) preprint" 로 표기하고, 학술지 판이 나오면 이 카드의 숫자를 다시 대조한다.
>
> **저자**: **Pei Sun** (1 LRCS UMR CNRS 7314 · UPJV · 2 LAMFA UMR CNRS 7352 · UPJV · 3 RS2E FR CNRS 3459) · **Francisco Fernandez** (1 · 3) · **Paul Vigneaux\*** (2 · 4 PIMS CNRS IRL 3069 · University of British Columbia) · **Alejandro A. Franco\*** (1 · 3 · 5 ALISTORE-ERI FR CNRS 3104 · 6 Institut Universitaire de France) — \* 교신 (p.3) · ChemRxiv 2026 · DOI 10.26434/chemrxiv.15012329/v1 (표지 날짜 17 November 2026 · PDF 43 쪽 = 표지 2 + 원고 41 (참고문헌 51 편 포함) · **SI 는 PDF 에 없다**) · 연구비 = CNRS MITI STRUDEL3D (80\|PRIME 2022–2023) · EU Horizon Europe DigiCell (101135486) · ANR-22-PEBA-0002 (PEPR BATMAN) · 계산 = UPJV MatriCS HPC (p.37–38) · 기여: Sun = 초고 · 시각화 · 검증 · 소프트웨어 · 방법 · 조사 · 분석 · 자료 · 개념 / Fernandez = 초고 · 방법 · 조사 · 개념 / Vigneaux · Franco = 검토 · 개념 · 방법 · 지도 · 자원 · 과제 관리 · 연구비 (p.38).
> **이웃 카드 (링크만)**: [`sun2026_dem_extrusion_recirculation_dry_electrode`](sun2026_dem_extrusion_recirculation_dry_electrode.md) (이 원고의 ref [37] = 앞 단계 · 같은 1저자) · [`zhang2026_polymer_electrolyte_modeling_perspective`](zhang2026_polymer_electrolyte_modeling_perspective.md) (같은 공동 1저자 Pei Sun · 같은 해) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (ref [35]) · [`nguyen2020_electrode_tortuosity_factor`](nguyen2020_electrode_tortuosity_factor.md) (ref [44]) · [`duquesnoy2023_ml_multiobjective_manufacturing_optimization`](duquesnoy2023_ml_multiobjective_manufacturing_optimization.md) (ref [51]) · [`benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode`](benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode.md) (ref [50]) · [`kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation`](kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md) (같은 부류 복셀 전도 · 형식 본).
> **판독 원자료**: `litdb/figures/sun2026_fff_printing_extruded_filament_sph_dry_electrode_preprint/digitized.csv` (90 행 — Fig 4e · 4f · 5b · 7b · 7c · 8b) · 그림 크롭 74 장 (그림 8 (도구 7 다시 자름 + 손 1) + 페이지에서 잘려 안 보이는 Fig 4g 래스터 1 + 패널 20 · 식 25 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: Franco 그룹이 앞서 DEM (LIGGGHTS) 으로 만든 무용매 압출 필라멘트 (LFP-rich AM 구 + 바인더/도전재 유효상 BC) 를 **잘라 붙여 990 µm 공급 원료**로 쓰고, 그것을 **LAMMPS RHEO 패키지** 위의 입자 모델 — AM = 반지름 5 µm 고체 구 · BC = 점성 SPH 유체 입자 (외피 반지름 2.355 µm) · 접촉하면 줄어드는 **가정한 냉각 상태 변수 θ** 가 점도와 BC 결합 생성을 정함 — 으로 FFF 노즐 흐름 · 기판 위 퇴적 · 고화를 3D 로 모사해, 공정 변수 (공급 · 인쇄 속도 · 노즐 간격 · 냉각률 · 가닥 간격 · 층 경로) 가 가닥 모양 · 층 덮임 · 두 층 전극의 빈 곳 · 확산 τ · 전자 전도를 어떻게 바꾸는지 본 **방법 제안 원고 (실험 대조 없음 · 동료 심사 전)** 다 — 두 층 전극은 빈 곳 (42.8–44.3 %) 과 확산 τ_Y (1.73–1.82) 가 거의 같아도 겉보기 전자 전도도가 0.0985–0.1912 S/m 로 거의 두 배 벌어진다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 무엇을 계산했나 | 압출 DEM 필라멘트 (마지막 6 프레임 × 165 µm = 990 µm · 물질 입자 ≈30,000) → LAMMPS RHEO 3D 입자 모델 (SPH 유체 BC + 고체 AM + 기판 입자 4 층) 로 단계 A (한 가닥 17) · B (한 층 9) · C (두 층 18) = **44 경우** → 0.5 µm 복셀 위 FVM 확산 · 전자 전도 | [인쇄] p.9 · p.15 · p.20 · p.22 |
| ② ★ 앞 논문 (sun2026 압출 DEM) 의 필라멘트 · 설정을 잇는가 | **필라멘트 = 일부** — 방법 절은 출처를 **[36] (Paredes-Goyes 2024)** 로 단다 · 초록은 *"our previously developed twin-screw extrusion model"* (= 서론의 [37] = sun2026 카드) · 조성 (F1–F4) · rpm · 투입 순서 = 본문 없음 (SI S1 [미확인]).  **DEM 설정 = 잇지 않는다** — BC 를 DEM 구에서 **SPH 유체 입자**로 바꿈 (외피 반지름 2.355 µm ↔ sun2026 DEM 2.5 µm) · 코드 LAMMPS RHEO (sun2026 = LIGGGHTS) · 밀도 2.71 / 1.1 pg µm⁻³ 인쇄 · AM 반지름 5 µm 는 같음 · 전도도 BC 1 · AM 10⁻⁴ S/m (sun2026 = 10 · 0.001) · BC 나노 공극 10 % 가정은 이어짐 | [인쇄] p.1 · p.4 · p.8–10 · p.21 · sun2026 카드 §3 |
| ③ 입자 표현 | AM = *"spherical solid inclusions of radius 5 µm"* (원문 서론: *"clusters of spherical, LFP-rich AM particles"* (p.8) — AM 하나 = 고체 구 하나 · 모양 변형 없음) · BC = *"fluid material particles carrying the effective mass and state of the unresolved mixture; individual polymer constituents and carbon additives were not resolved"* · AM–AM · AM–기판 = 짧은 거리 탄성 반발 + 법선 감쇠 (계수 SI 표 S2) · AM–AM 결합 없음 | [인쇄] p.9–11 |
| ④ 지배식 · 수치 | 힘 균형 (식 2: 유체 + 고체 접촉 + 결합 + 노즐 + 공급 + 중력) · 선형 상태식 p = c_s²(ρ − ρ₀) (c_s = 8 µm µs⁻¹) · 5 차 커널 · 차단 거리 11.775 µm · Δt = 0.005 µs · 인공 점성 0.5 · 밀도 확산항 · BC 입자 이동 (shifting) 끔 · 경계 비주기 | [인쇄] p.10–11 · 식 2–3 |
| ⑤ 냉각 · 고화 | θ ∈ [0, 1] = *"an assumed cooling rule rather than a temperature calculated from the energy conservation"* · 기판 (두 층에서는 첫 층) 에 닿으면 θ ← max(0, θ − R_c Δt) · θ 0.8 → 0.2 에서 구조 상태 s 0 → 1 · 점도 η = η₀(1 + 9s) (η₀ = 0.01 Pa s) · s ≥ 임계 ξ ∈ [0.15, 0.85] 이면 BC–BC · BC–AM 결합 (k = 2 pg µs⁻² · γ = 10 pg µs⁻¹ · 성숙 200 µs · 끊김 변형률 0.25) — **결합은 전기 접촉 저항 · 기계 강도에 보정 안 됨** | [인쇄] p.13–15 · 식 8–15 |
| ⑥ 한 가닥 (2⁴ 요인 설계) | 공급 속도 0.04 → 0.06 µm µs⁻¹: 폭 **+22.97 µm (31.05 %)** · 높이 +1.32 · 인쇄 속도 0.08 → 0.12: 폭 **−17.98 (20.15 %)** · 높이 −1.63 · 노즐 간격 25 → 35 µm: 폭 −11.55 · 높이 **+5.23 (21.66 %)** · 냉각률 ×4: 폭 −11.68 · 높이 +2.08 µm — 6 짝 평균 (A14 · A15 수치 중단) | [인쇄] p.25–26 · 그림 3 · [카드 산술] 재현 §3-2 |
| ⑦ 한 층 (A08 · λ = S/W_ref) | λ 0.75 · 0.85 · 1.00: 층 폭 229.01 · 243.45 · 267.33 µm · 높이 29.02 · 27.46 · 25.53 · Sq 3.30 · 3.44 · 4.60 µm · 덮임 100.00 · 99.97 · 97.82 % · 이음매 겹침 ≈18–24 % → ≈8 % → < 0.1 % | [인쇄] 그림 4 · p.28 · [판독] 4e |
| ⑧ 두 층 전극 | 분해된 빈 곳 **38.59–40.15 %** · BC 나노 공극 10 % 가정 포함 **42.83–44.29 %** · 층간 빈 곳 6.85–10.36 % · τ_Y **1.728–1.823** · σ_Y,app **0.0985–0.1912 S/m** · R_Y 최저 4.30 kΩ (U07-85) · R04-75 ↔ X04-75: 빈 곳 43.81 ↔ 43.18 % · τ 1.760 ↔ 1.758 · σ **+92.4 %** | [인쇄] p.32 · p.34 · 그림 7 · 8 |
| ⑨ 수송 계산의 정체 | 0.5 µm 복셀 · 셀 중심 FVM ∇·(k∇u) = 0 · **면 계수 = 조화 평균** · 상 값 = D/D₀ 1 · 0.1^1.5 · 0 · σ 0 · 1 · 10⁻⁴ S/m (공극 · BC · AM, **가정**) · 이상 접촉 = *"excluding additional contact resistance and electrochemical reactions"* → 우리 STEP3 와 같은 CONTACT_FREE 부류 | [인쇄] p.20–22 |
| ⑩ 저자 한계 | *"Experimental validation remains necessary before these predictions can be quantitatively applied"* (p.27) · BC 나노 공극 10 % *"without experimental calibration"* (p.35) · 표면 장력 · 접촉각 · 보정된 유변 법칙 없음 (p.12) · 수치 중단 = *"a numerical limitation, without establishing physical unprintability"* (p.16) | [인쇄] |

⛔ **한정어 (떼지 말 것)**: ① **ChemRxiv 원고 · 동료 심사 전** ② 재료 = **LFP-rich AM 구 + 고분자/탄소 유효상 BC (액체 LIB 양극 · FFF 인쇄)** — 고체전해질 · 압밀 · 압력 없음 ③ **실험 대조 0** (모든 물성 · 냉각률 · 결합 · 상 전도도 = 가정) ④ AM = 고체 구 하나 (입자 안 구조 · 모양 변형 · 파쇄 없음) · BC = 연속체 유체 (개별 고분자 · 탄소 없음) ⑤ 조건당 **한 런** (오차 막대 = 가닥 단면 사이의 공간 SD) ⑥ SI (표 S1 · S2 · S4 · 절 S1 · S4 · S5 · 동영상) 를 받지 못함 → 접촉 계수 · 경우별 설정 [미확인] ⑦ 원고 안 서로 어긋남 (§11) — 식 14 · 16 · 19 · 20 의 인쇄 깨짐 · 노즐 간격 30 ↔ 35 µm · 필라멘트 출처 [36] ↔ 'twin-screw'.
⇒ **절대값 전이**: **없다** — 공정 (용융 인쇄 ↔ 냉간 300 MPa 압밀) · 재료 (LFP + 고분자 ↔ LPSCl + NCM) · 상 역할 (BC 가 전자망 · 기공은 나중에 액체 전해질) 이 다 다르다.  옮길 것은 **방법** — ⓐ DEM 출력을 다음 모델로 넘기는 규약 (입자 수 · 상 · 반지름 · 출처 번호 보존 · 이음매 국소 이완) ⓑ 부피 회계 (기준 부피 합) ↔ 기하 (외피 합집합) 를 나눠 쓰는 연산자 규약 ⓒ 이완 끝 판정 다섯 조건 (결합 집합 변화 포함) ⓓ 겉보기 σ 와 전체 저항이 정규화 기하 (L/A) 때문에 순서가 갈리는 함정.

---

## 0-1. ★ 고른 의도 대조 (후보 표 밖 · 1저자 11-23 업로드 '논문에이전트 부탁' · 지시서 U-1123-1 덧붙임)

의도 원문 (지시서): *"후보 표 밖 · 1저자 11-23 '논문에이전트 부탁' (네 파일 중 하나)"* · *"같은 그룹의 앞 논문 (sun2026 압출 필라멘트 DEM) 다음 단계 = FFF 인쇄. 두 논문이 같은 필라멘트 · 같은 DEM 설정을 잇는지 원문으로 확인해 카드에 적는다 (추측 금지)"* · *"ChemRxiv 원고 (동료 심사 전) 라는 표지를 카드 머리에 둔다"* · 메인 세션 서지 메모 *"43 쪽 (본문 + SI 포함인지 확인)"*.

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "같은 그룹의 앞 논문 (sun2026 압출 DEM) 다음 단계 = FFF 인쇄" | **채움** | p.8: *"By extending our established extrusion modeling to 3D printing and deposition, we provide a foundation for investigating how upstream filament microstructure and downstream printing conditions jointly influence …"* · 그림 1 (Step 1 = 'Solvent-free extrusion · DEM-extruded filament' → Step 2 = FFF) · 같은 1저자 (Pei Sun) · 같은 교신 (Vigneaux · Franco) |
| "같은 필라멘트를 잇는가" | **일부** | p.9: *"The FFF 3D printing model used heterogeneous filaments generated by our upstream DEM extrusion model [36]. These six output filament segments (i.e., the last six frames output by the extrusion model) each provide a continuous segment 165 µm in length, which together form a 990 µm feed filament feedstock"* · ≈30,000 물질 입자 · 이음매 국소 이완 (입자 수 · 상 · 반지름 · 출처 보존) · *"All process conditions in this work used this common filament feedstock"*.  ⚠ [36] = *B. Paredes‐Goyes … A.A. Franco, Mesoscopic Model of Extrusion during Solvent‐Free Lithium‐ion Battery Electrode Manufacturing, Batteries & Supercaps (2024) e202300441* (p.41) — sun2026 카드가 '1 세대 압출 DEM' 이라 부른 논문 · 반면 초록 (p.1 · p.4) 은 *"transfers heterogeneous filaments from our previously developed twin-screw extrusion model"* 이고 서론 (p.8) 의 트윈스크류 + 재순환 모델은 **[37]** = sun2026 카드 논문 · 결론 (p.36) 은 번호 없이 *"our previously developed DEM extrusion model"* ⇒ **어느 모델의 어느 런 (조성 F1–F4 · 회전수 · 투입 순서) 의 출구 프레임인지 원고로 확정할 수 없다 [미확인 · SI S1 대기]** |
| "같은 DEM 설정을 잇는가" | **없음 (잇지 않는다)** | 넘어온 것은 **입자 배치 · 상 · 반지름 · 출처 번호** 뿐 (p.9).  인쇄 모델에서는 — ⓐ BC = DEM 구가 아니라 *"fluid material particles"* (SPH) · *"contact and visualization-envelope radius of 2.355 µm"* (p.9–10) ↔ sun2026 DEM 의 BC 반지름 2.5 µm (그 카드 §3 (나), 그림 2 인쇄) ⓑ 코드 = LAMMPS **RHEO** 패키지 (p.7–8) ↔ sun2026 = LIGGGHTS (그 카드 §4.1) · 이 원고에는 'LIGGGHTS' · 'Hertz' · 'SJKR' 낱말 0 회 ⓒ 밀도 = 2.71 (AM) · 1.1 (BC) pg µm⁻³ **인쇄** (p.10) ↔ sun2026 카드의 ρ_AM ≈3.51 · ρ_BC ≈1.10 은 그 카드의 역산 [DERIVED] (그 논문 미인쇄) — 그 카드 §2 계보는 입자 크기 · 밀도를 '전작 [36] 그대로 계승' 이라 적는데, AM 은 2.71 ↔ 3.51 로 23 % 다르다 [카드 산술: 2.71/3.51 = 0.772] · 어느 쪽이 DEM 의 값인지 이 원고로는 못 가린다 (넘어온 것 = 배치 · 상 · 반지름 · 출처 번호 · 밀도는 RHEO 입력) ⓓ AM–AM 접촉 = *"short-range elastic and normal dissipative interactions"* (계수 SI 표 S2 [미확인]) ↔ sun2026 = Hertz + SJKR 점착 + CDT 구름마찰 · E ×1/1000 ⓔ 같은 것: **AM 반지름 5 µm** (sun2026 AM ⌀10 µm) · BC 안 미분해 공극 **10 %** 가정 (아래 줄) |
| (덧) 수송 물성 설정 | **다름** | 이 원고 σ: 공극 0 · **BC 1 S/m · AM 10⁻⁴ S/m** · D/D₀: 1 · 0.1^1.5 · 0 (p.21) ↔ sun2026: σ_BC 10 S/m · σ_AM 0.001 S/m (그 카드 §3 (아)) · 이 원고 ε_tot = (V_void + 0.1 V_BC)/V_Ω (p.20) ↔ sun2026 식 20 *"1 − (V_AM + q·V_BC)/V_total, q = 10 %"* (그 카드 §6 · §10-5 가 '인쇄 꼴로는 숫자가 재현되지 않고 (1 ∓ q) 꼴이면 자기일관' 이라 적음) — 이 원고의 식은 V_Ω = V_void + V_AM + V_BC 일 때 1 − (V_AM + 0.9 V_BC)/V_Ω 와 같다 [카드 산술] = 그 카드가 든 (1 − q) 꼴.  ⚠ 앞 논문 식 20 이 실제로 그렇게 구현됐다는 증거는 아니다 [카드 추론] |
| "ChemRxiv 원고 (동료 심사 전) 표지" | **채움** | p.1–2 바닥글 *"This is a preprint and has not been peer reviewed. Data may be preliminary."* · DOI 10.26434/chemrxiv.15012329/v1 · 표지 날짜 17 November 2026 (PDF 생성 메타 2026-11-21) — 카드 머리 상자 |
| "43 쪽 (본문 + SI 포함인지 확인)" | **SI 없음** | 43 쪽 = ChemRxiv 표지 2 (p.1 초록 · p.2 초록 끝) + 원고 41 (p.3 머리 → p.36–37 결론 → p.37–38 사사 · 기여 → p.38–43 참고문헌 [1]–[51]) · 본문이 가리키는 *"Section S1 of the Supplementary Information (SI)"* (p.10) · *"SI file Table S2"* (p.11) · *"Section S4 and Table S4"* (p.17) · *"Table S1(a-c)"* (p.17 · p.22) · *"Section S5"* (p.22) · 동영상 (p.31) 이 PDF 에 없다 [미확인] |
| (꼭 뽑을 것) DEM 한계 · 소성 · 2D/3D · 탈압 | **일부** | DEM 한계를 직접 말한 문장 없음 (가까운 = 연속체 · 앞 연구 범위 문장 · §4-5 (i)) · 큰 변형 = BC 를 SPH 유체로 + 상태 점도 + 결합 (§4-5 (ii)) · 전부 3D (§4-5 (iii)) · 가압 · 탈압 없음 — 노즐 후퇴 뒤 균일 냉각 이완만 (§4-5 (iv)) |
| 가리킨 카드의 **2 차 인용 값** | **해당 없음** | 정본에 이 원고를 인용한 카드가 없다 (DOI '15012329' · 제목 낱말 grep 0 건) · sun2026 카드의 서지 (Batteries & Supercaps **2026, 9**, e202500211) ↔ 이 원고 ref [37] *"Batteries & Supercaps (2025) 2500211"* = 조기 공개 연도 ↔ 권호 연도 차이 (카드 문제 아님) |

⇒ **의도 대조 결과: 일부** — FFF 가 그 압출 DEM 의 다음 단계라는 것은 **채움**; 필라멘트를 잇는 것은 **일부** (방법 절 출처 = [36] Paredes-Goyes 2024 ↔ 초록 'twin-screw' = [37] sun2026 · 런 정보는 SI); 같은 DEM 설정은 **없음** (BC 가 SPH 유체로 바뀌고 코드 · 반지름 · 밀도 · 전도도가 달라짐 · AM 반지름 5 µm 와 BC 공극 10 % 가정만 같음).

---

## 1. 한 줄 요약
무용매 압출 → FFF 인쇄로 만드는 LIB 전극에서 *"the filament entering the printer already possesses a heterogeneous microstructure"* (Boudeville 2024 [5] 의 해석 · p.5) 라는 동기로, 그룹의 압출 DEM 이 낸 이질 필라멘트를 그대로 공급 원료로 써서 **노즐 흐름 · 자유 표면 퇴적 · 냉각 고화**를 입자 단위로 잇는 첫 계산 사슬 (*"has never been investigated through computational modeling"* · 초록) 을 세우고, 2⁴ 요인 설계 한 가닥 · 가닥 간격 한 층 · 세 경로 두 층으로 공정 → 형상 → 수송의 관계를 보인다 — 공급 · 인쇄 속도가 폭을, 노즐 간격이 높이를 주로 바꾸고, 같은 빈 곳 · 같은 확산 τ 의 두 층 구조가 전자 전도에서 두 배 가까이 갈린다 (정규화 기하 · 퇴적량 차이 포함 · 인과 분리 안 됨).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| P. Sun · F. Fernandez · P. Vigneaux\* · A. A. Franco\* (UPJV LRCS · LAMFA · RS2E · PIMS-UBC · ALISTORE · IUF) | **ChemRxiv 2026 (원고 · 동료 심사 전)** · 43 쪽 (표지 2 + 원고 41) | 10.26434/chemrxiv.15012329/v1 | **AM = LFP-rich 구형 입자** (*"clusters of spherical, LFP-rich AM particles"* · p.8 · 결론 *"Using LFP-based electrodes as a proof of concept"* · p.36) · **BC = 바인더 + 도전재 유효 유체상** (고분자 · 탄소 미분해) · SE 없음 · 액체 LIB 양극 인쇄 | **계산만** — 입자 기반 (RHEO: SPH + 고체 구 + 결합) 공정 모사 + 복셀 FVM 수송 · 실험 0 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 모델 상수 (p.9–17 · 전부 [인쇄] · 단위 환산 = [카드 산술])
| 항목 | 값 | 비고 |
|---|---|---|
| 공급 원료 | 압출 DEM 출구의 마지막 6 프레임 × 165 µm = **990 µm** · 물질 입자 **≈30,000** · 압출 축 → 공급 축 Y · 기판 = X–Z 면 · 끝나면 처음으로 돌아가 다시 공급 (입자마다 '몇 번째 바퀴' 표지) | p.9 · 필라멘트 지름 [미확인] |
| 입자 종류 | AM (고체 구 · 반지름 **5 µm**) · BC (SPH 유체 · 외피 반지름 **2.355 µm**) · 기판 (고체 입자 4 층 · 정해진 궤적으로 움직여 인쇄 경로를 만듦 · 측정에서 뺌) | p.9–10 |
| 기준 밀도 ρ₀ | AM **2.71** · BC **1.1** pg µm⁻³ (= g cm⁻³) | p.10 |
| 입자 하나의 질량 · 부피 | BC 60.2 pg · 54.7 µm³ · AM 1419 pg · 523.6 µm³ | [카드 산술 · 식 1] |
| 공급 | V_f 로 **5 µs 마다** 입자 공급 · 출처 번호 유지 · 질량 보존 · 입구 운동 · 상태 연속을 계속 확인 · 세부 = SI 절 S1 | p.10 · [미확인] |
| 상태식 · 수치 | p = c_s²(ρ − ρ₀) · c_s = **8 µm µs⁻¹** (수치 음속) · 5 차 (quintic) 커널 · 차단 거리 **11.775 µm** · Δt = **0.005 µs** · 인공 점성 계수 0.5 · 밀도 감쇠 보정 · 밀도 확산항 · BC 입자 이동 (shifting) 미적용 | p.10–11 |
| 위 값의 환산 | 압력 단위 pg µm⁻¹ µs⁻² = **1 kPa** · 힘 단위 pg µm µs⁻² = **1 nN** · c_s = 8 m/s · BC 의 K = ρ₀c_s² = **70.4 kPa** · 차단 거리 = 5.00 r_BC = 2.355 r_AM | [카드 산술] |
| AM 접촉 | AM–AM · AM–기판 = 짧은 거리 탄성 반발 + 법선 감쇠 · AM–AM 결합 없음 · 계수 = SI 표 S2 | p.11 · [미확인] |
| 중력 · 인쇄 | 중력 −Y 9.81 × 10⁻⁶ µm µs⁻² (= 9.81 m/s² [카드 산술]) · 시작 450 µs 뒤 기판이 X–Z 로 움직여 인쇄 (V_p = √(ẋ_b² + ż_b²)) · 기판 반력은 움직임을 강제하기 전에 계산 · 영역 경계 전부 비주기 | p.11 |
| 노즐 | 축 = Y · 끝에 원형 모서리가 있는 유한 원통 옆면 · 힘 = 가장 가까운 면의 법선 방향 (모서리 근처에서는 Y 성분 가능) · 치수 [미확인] | p.11 |
| 공급 힘 | 식 4–6 · 노즐 출구 위 54 µm 부터 8 µm 폭의 부드러운 계단으로 속도를 목표 v_in = ḣ_n − V_f 쪽으로 완화 · *"Material delivery was thus controlled kinematically, without a prescribed extrusion pressure"* · 표면 장력 · 접촉각 · 보정된 전단률 유변 법칙 없음 | p.12 |
| 냉각 상태 | θ 처음 1 · 기판 (두 층에서는 첫 층 지지 입자) 에서 차단 거리 안에 들면 θ ← max(0, θ − R_c Δt) · 접촉 표지 유지 · 재가열 없음 · 잠열 · 기판 온도 없음 · R_c = 2.5 × 10⁻⁴ … 1 × 10⁻³ µs⁻¹ | p.13 · p.15 |
| 냉각 시간 척도 | θ 1 → 0: 4000 µs (R_c 2.5 × 10⁻⁴) · 2000 µs (A00 · 5 × 10⁻⁴) · 1000 µs (1 × 10⁻³) · s 0 → 1 (θ 0.8 → 0.2): 2400 · 1200 · 600 µs | [카드 산술 · 식 8 · 11] |
| 점도 | η = η₀(1 + 9s) · η₀ = 10 pg µm⁻¹ µs⁻¹ (*"also equal to 0.01 Pas"*) → 완전 고화 0.1 Pa s | p.14 · [카드 산술] |
| 결합 | BC–BC · BC–AM · 이웃 찾기 8 · 10 µm · 결합 생성 7 · 9 µm · 쌍마다 임계 ξ_ij ∈ [0.15, 0.85] · min(s_i, s_j) ≥ ξ_ij 이면 생성 · k = 2 pg µs⁻² (= 2 × 10⁻³ N/m) · γ = 10 pg µs⁻¹ (= 1 × 10⁻⁸ kg/s) · 성숙 t_m = 200 µs · 끊김 변형률 ε_c = 0.25 (인장 · 압축) · θ ≥ 0.8 로 돌아가면 다시 생성 가능 | p.14–15 · [카드 산술 환산] |
| 이완 끝 판정 (단계 C) | 연속 3 구간 × 500 µs 동안: max θ ≤ 0.01 · rms 속도 ≤ 10⁻⁴ µm µs⁻¹ · max 속도 ≤ 10⁻³ µm µs⁻¹ · 구간당 max 변위 ≤ 0.1 µm · 결합 집합 상대 변화 f_E ≤ 10⁻³ (식 16 · 0 ≤ f_E ≤ 2) | p.17 |
| 두 층 공정 | 첫 층 λ 0.75 · 0.85 의 여섯 구성 × 경로 셋 (R = *"a reverse parallel path with three straight strands"* · U = *"an inward parallel U-shaped path with two strands"* · X = *"an anchored perpendicular path with three strands"* = 층간 각 90°) · 경로 길이 · 인쇄 시간 · 공급량이 경로마다 다름 (p.17) · 안쪽 변위 δ = −W_ref/2 (δ/S = −1/(2λ)) · 공급 유지한 채 노즐 출구를 1500 µs 동안 **35 → 60 µm** 로 25 µm 올림 (기판 기준) · 다 쌓은 뒤 공급 멈춤 · 노즐 25 µm 후퇴 (1500 µs) · 남은 물질은 기하 선택으로 제거 · 남은 퇴적물은 접촉과 무관하게 같은 R_c 로 균일 냉각 이완 | p.13 · p.17 |
| 계산 비용 | MatriCS · **64 CPU 코어** · 한 가닥 **16–24 h** · 두 층 인쇄 + 냉각 **1–2 일** · 한 가닥 인쇄 구간만 ≈0.92–1.34 × 10⁶ 걸음 (450 µs + 500 µm ÷ V_p, Δt 0.005 µs — 인쇄 뒤 관찰 시간은 빠짐) | p.17 · [카드 산술] |
| 속도 크기 | V_p 0.08–0.12 µm µs⁻¹ = 80–120 mm/s · V_f 0.04–0.06 µm µs⁻¹ = 40–60 mm/s · V_p/c_s = 0.010–0.015 | [카드 산술] |

### 3-2. ★ 단계 A — 한 가닥 2⁴ 요인 설계 (p.15–16 · p.22–27 · 그림 3)
- 설계 [인쇄]: 기준 A00 = V_p 0.10 · V_f 0.05 µm µs⁻¹ · H_g 30 µm · R_c 5 × 10⁻⁴ µs⁻¹ · 요인 수준 (낮음 / 높음) = H_g 25 / 35 µm · V_p 0.08 / 0.12 · V_f 0.04 / 0.06 µm µs⁻¹ · R_c 2.5 × 10⁻⁴ / 1 × 10⁻³ µs⁻¹ · 경로 ≈500 µm · 측정 = d = 100, 110 … 300 µm 의 21 단면 (±5 µm 띠) · 노즐 중심이 지난 뒤 1000 ± 25 µs 의 프레임 · 폭 W · 높이 H = 식 17–18.
- 경우 번호 ↔ 수준: 원문 표 S1(a) 는 SI [미확인].  본문이 수준을 적은 다섯 경우 (A04 · A05 · A07 · A08 · A12) 와 그림 3b 칸 배치가 **A_n − 1 = 8·V_p + 4·V_f + 2·H_g + R_c** (각 0 = 낮음 · 1 = 높음) 와 맞고, 이 배치로 그림 3b · 3c 의 인쇄 값에서 네 주효과를 다시 계산하면 **인쇄 값 (−17.98 · +22.97 · −11.55 · −11.68 / −1.63 · +1.32 · +5.23 · +2.08) 이 0.01 µm 까지 그대로** 나온다 [카드 추론 + 산술] — 아래 표의 수준 칸은 그 배치다.

| 경우 | V_p | V_f | H_g | R_c | 폭 µm (공간 CV) | 높이 µm (CV) |
|---|---|---|---|---|---|---|
| A01 | 0.08 | 0.04 | 25 | 2.5e-4 | 90.47 (2.6 %) | 22.78 (3.1 %) |
| A02 | 0.08 | 0.04 | 25 | 1e-3 | 77.45 (1.9 %) | 25.16 (2.1 %) |
| A03 | 0.08 | 0.04 | 35 | 2.5e-4 | 77.65 (4.7 %) | 28.56 (3.2 %) |
| **A04** | 0.08 | 0.04 | 35 | 1e-3 | **67.06** (2.6 %) | **30.61** (2.3 %) |
| **A05** | 0.08 | 0.06 | 25 | 2.5e-4 | **121.18** (2.1 %) | 24.60 (2.9 %) |
| A06 | 0.08 | 0.06 | 25 | 1e-3 | 101.80 (1.3 %) | 27.58 (3.5 %) |
| **A07** | 0.08 | 0.06 | 35 | 2.5e-4 | **102.75** (1.8 %) | **29.32** (2.7 %) |
| **A08** | 0.08 | 0.06 | 35 | 1e-3 | **88.99** (1.5 %) | **32.43** (2.8 %) |
| A09 | 0.12 | 0.04 | 25 | 2.5e-4 | 70.33 (4.4 %) | 22.46 (6.1 %) |
| A10 | 0.12 | 0.04 | 25 | 1e-3 | 63.42 (3.2 %) | 23.30 (5.4 %) |
| A11 | 0.12 | 0.04 | 35 | 2.5e-4 | 62.65 (8.5 %) | 27.60 (3.7 %) |
| **A12** | 0.12 | 0.04 | 35 | 1e-3 | **56.24** (6.7 %) | 28.71 (4.3 %) |
| A13 | 0.12 | 0.06 | 25 | 2.5e-4 | 91.96 (3.9 %) | 22.62 (3.4 %) |
| A14 | 0.12 | 0.06 | 25 | 1e-3 | **중단** | 중단 |
| A15 | 0.12 | 0.06 | 35 | 2.5e-4 | **중단** | 중단 |
| A16 | 0.12 | 0.06 | 35 | 1e-3 | 70.35 (3.5 %) | 29.66 (3.0 %) |
- 폭 · 높이 · CV = [인쇄 · 그림 3b · 3c 칸 안 글자] · 굵은 다섯 경우의 수준 = [인쇄 p.22–23 · p.25 · p.28] · 나머지 수준 = [카드 추론].  그림 3c 제목은 *"Mean heigh measurementst"* 로 인쇄 (오타).
- 중단 두 경우 [인쇄 p.25]: A14 = *"slightly exceeded the prescribed 5% density-deviation threshold for a single BC particle"* · A15 = *"terminated when a partially structured BC particle penetrated the substrate"* — 원문은 이를 수치 한계로 다루고 *"without establishing physical unprintability"* (p.16).
- 주효과 [인쇄 p.25–26 · 그림 3d · 3e]: 6 짝 (빠진 두 경우가 요인마다 두 짝을 지움 — 2⁴ 의 8 짝 → 6) 의 높음 − 낮음 평균.

| 요인 (낮음 → 높음) | 폭 변화 µm (평균 상대 %) | 높이 변화 µm (%) | 원문 해석 |
|---|---|---|---|
| V_f 0.04 → 0.06 | **+22.97 (31.05 %)** | +1.32 (5.04 %) | 출구 유량 Q_out 이 크게 늘고 늘어난 공급은 주로 옆으로 퍼짐 · 비율의 평균 대신 평균의 비로는 31.38 % (원문) |
| V_p 0.08 → 0.12 | **−17.98 (20.15 %)** | −1.63 (5.84 %) | 유량은 거의 그대로 · 같은 물질이 더 긴 경로에 깔림 → 길이당 공급 Q_v/V_p 가 쓸모 있는 척도 |
| H_g 25 → 35 µm | −11.55 (12.94 %) | **+5.23 (21.66 %)** | 노즐 가둠이 약해져 덜 퍼짐 (Serdeczny [40] · Tu [41] 실험 경향과 같은 방향) |
| R_c ×4 | −11.68 (12.91 %) | +2.08 (8.01 %) | 접촉 뒤 퍼짐이 빨리 묶임 (냉각률 = 실측 온도가 아니라 경험적 상태 규칙 · 원문 한정) |
- 상호작용 [인쇄 p.26]: H_g 25 · 느린 냉각에서 V_f 를 올리면 폭이 낮은 V_p 에서 +30.71 µm (A01 → A05) · 높은 V_p 에서 +21.64 µm (A09 → A13 · 그림 값으로 21.63 [카드 산술]) → *"feeding and printing velocities cannot be treated as independent, additive controls of strand geometry"*.  경향은 6 짝 모두 같고 표본을 위 · 아래 반으로 나눠도 같음.
- 대표 세 경우 (그림 3a · p.23): A05 = 출구 아래 쌓이며 진행 방향으로 휜 C 꼴 · A12 = 크게 늘어나며 처음 퇴적 때 기판 위에서 미끄러지고 출구 아래 국부 분리 (물질 다리는 유지) · 위에서 본 AM–BC 뭉침 · 분리 · A08 = 간격을 채우며 아래로 → 기판을 따라 직각 전이.  저자: Plott 등 [39] 실험의 '늘어남 ↔ 노즐 눌림 · 앞으로 흐름' 구분과 *"qualitatively resemble"*.
- 선택된 세 경우 [인쇄 p.25]: A04 · A07 · A08 (모두 V_p 0.08 · H_g 35) — 폭 67.06 · 102.75 · 88.99 µm · 높이 30.61 · 29.32 · 32.43 µm · 공간 CV < 3 % · A04 → A08 (V_f ↑): 폭 +32.7 % · 높이 +6.0 % · A07 → A08 (R_c ↑): 폭 −13.4 % · 높이 +10.6 %.
- A12 = 평균 폭 최소 ≈56.24 µm 인데 진행 방향으로 점점 좁아짐 · A04 의 중심 평균제곱변위 (평균 변위를 뺀 MSD) 가 출구를 지난 뒤 ≈1500–2000 µs 에 평탄 — *"performed only for A04 and does not establish equivalent behavior for the other cases"* (p.26–27).
- 원문 결론: 정해진 폭 ÷ 높이 비를 처방하지 말고 해당 공정 조건에서 가닥 형상을 정하라 · *"Experimental validation remains necessary before these predictions can be quantitatively applied to printed electrode structures and their transport properties."* (p.27).

### 3-3. ★ 단계 B — 한 층 · 가닥 간격 (p.16 · p.27–30 · 그림 4 · 5 · 6a)
| A08 · λ (S = λ·W_ref) | 0.75 | 0.85 | 1.00 | 표지 |
|---|---|---|---|---|
| 가닥 간격 S (W_ref 88.99 µm) | 66.7 µm | 75.6 µm | 89.0 µm | [카드 산술] |
| 층 외피 폭 | 229.01 µm | 243.45 µm | 267.33 µm | [인쇄 그림 4a] |
| 3 가닥 어림 2S + W_ref | 222.5 µm | 240.3 µm | 267.0 µm | [카드 산술 · 인쇄 값과 −2.8 · −1.3 · −0.1 %] |
| 평균 표면 높이 | 29.02 µm | 27.46 µm | 25.53 µm | [인쇄 그림 4b] |
| Sq (식 21) | 3.30 µm | 3.44 µm (+≈4 %) | 4.60 µm | [인쇄 그림 4c · p.28] |
| 덮인 core 면적 | 100.00 % | 99.97 % | 97.82 % | [인쇄 그림 4d] |
| 이음매 겹침 1–2 / 2–3 (평균 ± 101 단면 공간 SD) | ≈18.2 (≈15.8–20.2) / ≈24.1 (≈20.3–27.9) % | ≈7.8 / ≈8.6 % (막대 ≈5–10.6) | ≈0 / ≈0 % | [판독 그림 4e] · 원문 *"approximately 18-24 %"* · *"approximately 8 % each"* · *"below 0.1 %"* |
| 가닥 사이 골 깊이 1–2 / 2–3 | ≈1.4 / 1.43 µm | ≈3.2 / 2.93 µm | ≈8.4 / 8.60 µm | [판독 그림 4f] |
- 원문 해석 (p.28): λ 를 키우면 층이 넓고 낮아지지만 Sq 와 골이 커진다 — *"layer thickness and surface height uniformity respond differently to strand spacing distance"* · 덮임이 높아도 (97.82 %) 이음매 겹침은 거의 0 일 수 있다 → 덮임과 이음매를 함께 본다 · λ 0.85 = 절충 (높이 27.46 µm · Sq +4 % 만 · 두 이음매 모두 모든 단면에서 양의 겹침 · 둘 다 ≈8 %) · Sq 최소가 목표면 0.75.
- λ = 0.85 세 조건 (그림 5 · p.29–30): core 덮임 모두 > 99.8 % · Sq **4.03 (A04) · 3.61 (A07) · 3.44 (A08) µm** [인쇄] · 겹침 1–2 / 2–3 ≈13.8 / 15.4 (A04) · ≈5.1 / 6.4 (A07) · ≈7.8 / 8.5 % (A08) [판독 그림 5b · 막대 = 공간 변동 (A07 1–2 ≈1.1–9.0)] · A04 겹침 최대 · A07 두 이음매에 겹침 0 인 단면 있음 · A08 = 중간 겹침 + 가장 작은 변동 → 다층 출발점으로 선택.  ⚠ 같은 λ 라도 W_ref 가 달라 절대 간격 S 는 다르다 (A04 57.0 · A07 87.3 · A08 75.6 µm [카드 산술]) — 원문도 *"does not isolate feed-velocity or cooling effects at fixed absolute spacing or deposition age"* (p.30).
- ⚠ 원문 어긋남: p.16 은 단계 B 를 *"at a fixed nozzle-bed gap of 30 µm"* 라 적고, p.25 · p.28 은 A04 · A07 · A08 이 *"an initial nozzle-bed gap of 35 µm"* · p.17 은 두 번째 층에서 노즐을 *"from 35 to 60 µm"* 로 올린다 — 단계 B 의 실제 간격 [미확인 · 35 µm 쪽이 세 곳].
- ⚠ 본문 p.28 *"shown in Fig. 4a, b, and g"* 의 **그림 4g 는 게시된 PDF 에서 보이지 않는다** — 그림 4 래스터 (xref 30) 아래쪽에 패널 'g)' (λ 0.75 · 0.85 · 1.00 위에서 본 모습) 가 있지만 페이지가 그 래스터를 잘라 그리는 상자 (clip · y ≤ 471.4 pt) 밖이다 · 캡션도 (a)–(f) 만 · 크롭 `fig_4g_hidden_raster.png` (기록용) · 같은 장면은 그림 6a.

### 3-4. ★ 단계 C — 두 층 전극의 빈 곳 (p.20 · p.30–33 · 그림 7)
- 정의 [인쇄 p.20]: 0.5 µm 복셀 · 영역 V_Ω = 반지름 5 µm 구 탐침 외피 + 가닥 기반 틈 채움 (같은 층 = 겹치는 이웃 가닥 사이 · 국부 가닥 간격 중앙값의 1.5 배 이하 · 층 사이 = 두 층이 함께 받치고 50 µm 이하) · ε_v = V_void/V_Ω (분해된 기하 빈 곳) · **ε_tot = (V_void + 0.1 V_BC)/V_Ω** (*"an assumed 10 % unresolved BC nanoporosity"*) · f_IL = V_IL/V_Ω (처음 두 층 표면 사이 · 공통 지지 기둥 안 공극 복셀 · ε_v 의 부분 집합) · 매끄럽게 하기 · 구멍 채우기 없음 · 기판 제외.
- 결과 [인쇄 p.32–33]: ε_v **38.59–40.15 %** · ε_tot **42.83–44.29 %** (폭 1.46 %p) · f_IL **6.85 % (U07-85) – 10.36 % (R04-85)** · 같은 공정 · 간격에서 U · X 가 R 보다 층간 빈 곳이 작다 (줄어든 양 U 1.69–2.10 · X 0.78–1.91 %p) · U ↔ X 순서는 일정하지 않음 (X04-75 < U04-75).
- 경우별 [판독 그림 7b · 7c · digitized.csv — 인쇄 범위 · R04-75 / X04-75 의 인쇄 ε_tot 43.81 / 43.18 과 ±0.02 %p 안]:

| 경우 | ε_v % | ε_tot % | f_IL % | φ_BC = 10(ε_tot − ε_v) % [카드 산술] | φ_AM = 100 − ε_v − φ_BC % [카드 산술] |
|---|---|---|---|---|---|
| R04-75 | 39.62 | 43.79 | 10.25 | 41.7 | 18.68 |
| U04-75 | 39.52 | 43.70 | 8.55 | 41.8 | 18.68 |
| X04-75 | 38.97 | 43.16 | 8.34 | 41.9 | 19.13 |
| R04-85 | 40.15 | 44.29 | 10.36 | 41.4 | 18.45 |
| U04-85 | 39.74 | 43.91 | 8.49 | 41.7 | 18.56 |
| X04-85 | 39.35 | 43.53 | 8.57 | 41.8 | 18.85 |
| R07-75 | 39.34 | 43.51 | 8.94 | 41.7 | 18.96 |
| U07-75 | 38.91 | 43.11 | 6.96 | 42.0 | 19.09 |
| X07-75 | 38.97 | 43.15 | 7.74 | 41.8 | 19.23 |
| R07-85 | 39.71 | 43.83 | 8.95 | 41.2 | 19.09 |
| U07-85 | 39.19 | 43.37 | 6.84 | 41.8 | 19.01 |
| X07-85 | 39.25 | 43.42 | 8.01 | 41.7 | 19.05 |
| R08-75 | 38.83 | 43.03 | 9.08 | 42.0 | 19.17 |
| U08-75 | 38.59 | 42.84 | 7.20 | 42.5 | 18.91 |
| X08-75 | 38.67 | 42.90 | 8.23 | 42.3 | 19.03 |
| R08-85 | 39.37 | 43.55 | 9.16 | 41.8 | 18.83 |
| U08-85 | 38.84 | 43.05 | 7.08 | 42.1 | 19.06 |
| X08-85 | 38.78 | 43.00 | 8.36 | 42.2 | 19.02 |
- 판독으로 다시 낸 줄어든 양: U 1.70–2.11 · X 0.80–1.91 %p (인쇄 1.69–2.10 · 0.78–1.91) [카드 산술].
- φ_BC 41.2–42.5 % · φ_AM 18.45–19.23 % · 고체 중 AM 부피 몫 φ_AM/(100 − ε_v) = **0.308–0.317** [카드 산술 · 판독 오차 ±0.4 %p 를 φ_BC 에 전파] — 18 구조가 거의 같은 조성 (공통 공급 원료).  원고는 필라멘트 조성을 적지 않는다; 만약 sun2026 카드 (Boudeville 실험) 의 BC : AM = 0.45 : 0.55 질량비를 이 원고의 ρ₀ (1.1 · 2.71) 로 바꾸면 0.332 [카드 산술 · 가정] — 판독 0.31 과 6 % 차 (원인 [미확인]: 다른 조성 · 외피 합집합 ↔ 기준 부피 · 판독).

### 3-5. ★ 단계 C — 확산 τ_Y 와 전자 전도 (p.21–22 · p.34–35 · 그림 8)
- τ_Y (식 23 = ε_tot · G_hom,Y / G_diff,Y · G_hom = 같은 영역 · 같은 접촉면에 D₀ 균일) — **그림 8a 에 18 값 전부 인쇄**:

| 공정 | R (λ 0.75 / 0.85) | U | X |
|---|---|---|---|
| A04 | 1.760 / 1.763 | 1.776 / **1.747** | 1.758 / **1.728** (최소) |
| A07 | 1.789 / 1.787 | 1.796 / 1.785 | 1.789 / 1.783 |
| A08 | 1.782 / 1.790 | **1.823** (최대) / 1.811 | 1.809 / 1.794 |
- [인쇄 그림 8a · p.34] — λ 0.75 → 0.85 에서 U · X 는 모두 τ 감소 · R 은 부호가 섞임 (A04 · A08 ↑ · A07 ↓) · 원문: *"The factor characterizes the specified diffusion problem; it is neither a direct path-length ratio nor a measure of electrolyte access to all reacting surfaces"* (Nguyen 2020 [44] 인용).
- 겉보기 전도도 · 전체 저항 [판독 그림 8b · digitized.csv — 인쇄 σ 범위 0.0985–0.1912 · U07-85 4.30 kΩ · U/X ↔ R 41.3–57.9 / 45.5–92.4 % · λ ↑ 의 R 감소 4.9–11.6 % · X04 −5.4 / −3.9 % 를 판독이 모두 재현]:

| 경우 | σ_Y,app S/m | R_Y kΩ | L_Y/A_Y = σ·R m⁻¹ [카드 산술] | f = ε_tot/τ_Y [카드 산술] |
|---|---|---|---|---|
| R04-75 | 0.0994 | 13.35 | 1327 | 0.249 |
| R04-85 | 0.0990 | 12.19 | 1207 | 0.251 |
| U04-75 | 0.1491 | 9.22 | 1375 | 0.246 |
| U04-85 | 0.1504 | 8.42 | 1266 | 0.251 |
| X04-75 | **0.1911** (인쇄 0.1912 · p.34) | 8.39 | 1603 | 0.246 |
| X04-85 | 0.1838 | 7.94 | 1459 | 0.252 |
| R07-75 | 0.1100 | 6.50 | 715 | 0.243 |
| R07-85 | 0.1116 | 5.99 | 668 | 0.245 |
| U07-75 | 0.1660 | 4.86 | 807 | 0.240 |
| U07-85 | 0.1763 | **4.30** | 758 | 0.243 |
| X07-75 | 0.1635 | 5.25 | 858 | 0.241 |
| X07-85 | 0.1633 | 4.77 | 779 | 0.244 |
| R08-75 | 0.1001 | 8.30 | 831 | 0.241 |
| R08-85 | **0.0985** | 7.89 | 777 | 0.243 |
| U08-75 | 0.1414 | 6.31 | 892 | 0.235 |
| U08-85 | 0.1489 | 5.58 | 831 | 0.238 |
| X08-75 | 0.1465 | 6.59 | 965 | 0.237 |
| X08-85 | 0.1433 | 6.04 | 866 | 0.240 |
- 원문 [인쇄 p.34–35]: σ 0.0985–0.1912 S/m = *"approaching a twofold range"* (0.1912/0.0985 = 1.94 [카드 산술]) · 같은 공정에서 U · X 가 R 보다 41.3–57.9 · 45.5–92.4 % 높음 · R04-75 ↔ X04-75: 빈 곳 43.81 ↔ 43.18 % · τ 1.760 ↔ 1.758 인데 σ +92.4 % → *"Total void fraction and pore-transport tortuosity therefore did not capture the electronic differences among these structures"* · 그러나 *"the present architecture comparison does not isolate a causal contribution from interlayer connectivity"* · 결론 (p.36): *"this difference cannot be attributed to interlayer orientation alone"* (배치 · 퇴적량이 다름).
- ★ **σ 와 R 의 순서가 갈리는 이유 (원문 + 카드 분해)**: σ_Y,app = G·L_Y/A_Y (L_Y = 영역 상자 높이 · A_Y = X–Z 투영 면적) · R_Y = 1/G (식 24–25) → σ 최고 (X04-75) ≠ R 최저 (U07-85) · λ 0.75 → 0.85 에서 R 은 아홉 짝 모두 4.9–11.6 % 줄지만 σ 는 U 셋 · R07 만 오른다 · X04: R −5.4 · σ −3.9 % (원문).  판독으로 나누면 L/A 가 **668–1603 m⁻¹ (2.4 배)** 로 벌어지고 (A04 구조가 가장 큼 · 좁은 가닥 W_ref 67 µm), X04-75 ÷ R04-75 의 σ 1.92 배 = 컨덕턴스 **1.59 배** × L/A **1.21 배** [카드 산술] — '92.4 %' 의 일부는 정규화 기하에서 온다.
- 상 값 대비 [카드 산술]: σ_app/σ_BC = 0.099–0.191 (σ_BC = 1 S/m) at φ_BC ≈0.41–0.43 · f (확산) = 0.235–0.252 — 확산 f 는 18 구조에서 중앙값 기준 ±3.5 %, 전자 σ 는 ±32 % 흔들린다.

---

## 4. ★ 방법 — 사슬 · 입자 · 냉각 · 측정

### 4-1. 계산 사슬 (그림 1)
DEM 압출 (출구 프레임) → 필라멘트 6 조각 이어 붙임 (이음매 국소 이완) → RHEO 공급 (5 µs 마다 · V_f 운동학 · 순환) → 노즐 흐름 (가둠 힘 · 공급 힘) → 기판 이동으로 인쇄 (450 µs 뒤) → 접촉 냉각 (θ) → 점도 증가 + 결합 생성 (고화) → [두 층: 노즐 35 → 60 µm 올림 · 두 번째 층 · 공급 중단 · 노즐 후퇴 · 잔여 제거 · 균일 냉각 이완 · 다섯 조건 만족까지] → 외피 · 틈 채움 영역 → 0.5 µm 복셀 → FVM 확산 · 전자 전도 → τ_Y · σ_Y,app · R_Y.

### 4-2. 입자 · 힘 (식 1–7 · p.9–12)
| 식 | 내용 | 크롭 |
|---|---|---|
| (1) | V_i,ref = m_i/ρ₀,i = 4πr_i³/3 — 기준 부피 · 외피 반지름 정의 · 합 = 공급 · 유량 회계 | `eq_01_*` |
| (2) | m_i dv_i/dt = F^hyd + F^solid + F^coh + F^noz + F^feed + m_i g | `eq_02_*` |
| (3) | p_i = c_s²(ρ_i − ρ₀,i) — 약압축 선형 상태식 (c_s 8 µm µs⁻¹) | `eq_03_*` |
| (4)–(6) | F^feed = (m_i/τ_f) w_i(t)(v_in − v_i,y) e_y · w = 3u² − 2u³ · u = clip[(y_i − h_n − 54 µm)/8 µm, 0, 1] (목표 속도 아래첨자는 인쇄 깨짐 '¿') | `eq_04_*` – `eq_06_*` |
| (7) | Q_out = (1/Δt) Σ σ_e m_e/ρ₀,e — 출구 면 통과 기준 부피 유량 (방향 ±1) → A_mat ≈ Q_out/V_p · φ_s A_env ≈ Q_out/V_p | `eq_07_*` |
- 유체 상호작용은 쌍의 하나라도 유체일 때만 · 고체 접촉과 결합은 따로 더함 (p.10) · 힘 밀도 → 입자 힘 = 순간 부피 m_i/ρ_i(t) (p.11).

### 4-3. 냉각 · 고화 · 결합 (식 8–16 · p.13–17)
| 식 | 내용 | 크롭 |
|---|---|---|
| (8) | θ_i^{n+1} = max(0, θ_i^n − R_c Δt) — 접촉으로 켜지는 상태 감소 (가정 규칙) | `eq_08_*` |
| (9)–(11) | η_i = η₀(1 + 9s_i) · s_i = 3u_i² − 2u_i³ · u_i = clip((0.8 − θ_i)/0.6, 0, 1) | `eq_09_*` – `eq_11_*` |
| (12) | F_ij^coh = [−k(r − r₀) − γ v_ij,n] a_ij (1 − q_ij⁸) n_ij | `eq_12_*` |
| (13) | a_ij = [min(s_i, s_j)]² S((t − t_b)/t_m) — 덜 고화된 쪽이 진폭을 정함 · 200 µs 성숙 | `eq_13_*` |
| (14) | q_ij = min… — **우변 인쇄 깨짐** (본문: 변형률 크기에 대한 연화 · ε_c = 0.25) [미확인] | `eq_14_*` |
| (15) | ε_ij = (r − r₀)/r₀ | `eq_15_*` |
| (16) | f_E = (결합 집합의 대칭차 크기) / max(…) — **분모 인쇄 깨짐** · 본문 '0 ≤ f_E ≤ 2 · 같은 크기 서로소 두 집합 = 2' 와 맞는 분모 = max(두 집합 크기) [카드 추론] | `eq_16_*` |
- 결합은 BC–BC · BC–AM 만 · AM–AM 결합 없음 · 결합 = *"mechanical connectivity"* (전기 접촉 저항 · 거시 강도 보정 없음 · p.15) · 재결합 규칙은 *"did not explicitly model remelting or interfacial healing"*.

### 4-4. 측정 연산자 (식 17–25 · p.18–22)
| 식 | 내용 | 크롭 |
|---|---|---|
| (17)–(18) | W · H = ±5 µm 띠 안 입자 외피의 가로 · 세로 범위 | `eq_17_*` · `eq_18_*` |
| (19)–(20) | O_ab(d) = 두 가닥 점유 구간의 교집합 길이 · f_ab = O_ab ÷ 작은 쪽 점유 길이 (절댓값 막대 · 분모 인쇄 깨짐 — 정의는 본문) | `eq_19_*` · `eq_20_*` |
| (21) | S_q = √(1/N_cov Σ (h_j − h̄_cov)²) — 덮인 core 격자점만 (덮이지 않은 곳은 0 이 아니라 뺌) | `eq_21_*` |
| (22) | G = (‖F_in‖ + ‖F_out‖)/(2Δu) — 입출구 플럭스 평균 ÷ 걸어 준 차 | `eq_22_*` |
| (23) | τ_Y = ε_tot G_hom,Y/G_diff,Y — 기하 기준 tortuosity factor | `eq_23_*` |
| (24)–(25) | σ_Y,app = G_el,Y L_Y/A_Y · R_Y = 1/G_el,Y | `eq_24_*` · `eq_25_*` |
- 가닥 배정 = 노즐 출구 면을 처음 '믿을 만하게' 아래로 지난 시각 (0.1 µs 기록 선형 보간) · 이후 바뀌지 않음 · 시작 · 회전부 물질은 형상에는 들어가지만 겹침 계산에서 빠짐 (p.18–19).
- 수송 경계: 선택된 방향의 외부 접촉면 집합 사이에 단위 농도차 또는 1 V · 나머지 면 무유속 · 접촉면 후보는 10 µm 기하 제약 (영역은 그대로) · 면 계수 = 조화 평균 · 상 값 D/D₀ = 1 (분해된 공극) · 0.1^1.5 (BC — 공극 10 % 에 지수 1.5 를 건 Bruggeman 꼴로 읽힌다 [카드 추론 · 원문은 값만]) · 0 (AM) · σ = 0 · 1 · 10⁻⁴ S/m (p.20–21).

### 4-5. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 = 직접 진술 없음.**  인쇄 단계는 DEM 이 아니다 (BC = SPH 유체 · AM = 고체 구).  가까운 문장 셋: *"When the deposited composite is represented as an effective continuum medium, however, the redistribution of its individual constituents is not explicitly resolved."* (p.7 — 연속체 모델의 한계) · *"these existing extrusion studies have not yet investigated the processes of particle rearrangement and structural reconstruction resulting from the following 3D printing"* (p.8 — 앞 DEM 연구의 범위 · 인용 번호는 [34,35]) · BC 에 대해 *"individual polymer constituents and carbon additives were not resolved"* (p.9).  ⇒ DEM 구 → SPH 유체로 바꾼 이유를 원문은 말하지 않는다 (용융 흐름 · 고화를 담으려는 선택으로 읽히지만 [카드 추론]).
- **(ii) 소성 · 큰 변형** — 입자 고체의 소성은 없다 (AM 강체 구 · 파쇄 없음).  큰 변형을 받는 것은 **BC 연속체 (SPH)** 이고, 그 '고화' 는 ⓐ 상태 의존 점도 (최대 10 배) ⓑ 결합 그물 (스프링 + 감쇠 · 끊김 · 재생성) ⓒ 가정한 냉각률 로 흉내 낸다.  맞춘 값 = **0 개** (실험에 보정한 값 없음 · 점도 · 결합 · 냉각 · 공극 10 % · 상 전도도 모두 가정) · *"The model omitted explicit surface tension, a prescribed contact angle and a calibrated shear-rate-dependent rheological law."* (p.12) · 비용 64 코어 · 한 가닥 16–24 h · 두 층 1–2 일 (p.17).
- **(iii) 차원** — 인쇄 · 분석 모두 **3D** (그림 6 · 7a · 0.5 µm 복셀).  2D 는 관련 연구 소개에서 Yang 등 [28] 이 *"two-dimensional, isothermal model"* 이었다는 한 줄뿐 · 2D → 3D 전이 진술 없음.
- **(iv) 탈압** — 가압 · 탈압 없음.  가장 가까운 것 = 공급 중단 → 노즐 후퇴 (25 µm · 1500 µs) → 잔여 물질 기하 제거 → **균일 냉각 이완** → 다섯 조건 (θ · rms 속도 · 최대 속도 · 구간 변위 · 결합 집합 변화) 을 연속 3 구간 만족할 때 끝 (p.13 · p.17) — 되돌아옴 (springback) 숫자는 없다.

### 4-6. 기법 미니 용어집
- **FFF (fused filament fabrication)** = 녹인 필라멘트를 노즐로 밀어 기판 위에 가닥을 그리는 3D 프린팅 (= FDM).
- **SPH (smoothed particle hydrodynamics)** = 유체를 입자로 쪼개고 커널 가중합으로 밀도 · 압력 · 점성을 푸는 격자 없는 방법.  **약압축 (weakly compressible)** = 큰 인공 음속 c_s 로 밀도 변화를 작게 묶는 방식 (여기서 5 % 넘으면 런 중단).
- **RHEO (Reproducing Hydrodynamics and Elastic Objects)** = LAMMPS 의 패키지 — 재생 커널 SPH + 결합 입자 모델 · 냉각 · 고화 시연 포함 (ref [31] · p.7).
- **결합 (cohesive link)** = 두 입자 사이 스프링 + 감쇠 (식 12) — 여기서는 고화된 BC 의 기계적 연결을 흉내.
- **λ (spacing factor)** = 가닥 간격 S ÷ 한 가닥 기준 폭 W_ref.
- **Sq** = 덮인 표면의 높이 rms 편차.  **core 덮임** = 바깥 두 가닥 중심선 사이 격자점 중 물질이 있는 몫.
- **tortuosity factor (τ_Y)** = 같은 영역 균질 확산 대비 실제 확산 컨덕턴스의 비 × ε_tot — 우리 이름 **tau2 (수송 tortuosity · √ 아님)** 꼴.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 사슬 개요 — DEM 압출 필라멘트 (파랑 AM · 빨강 BC) → 단계 A · B · C → 구조 · 수송 기술자 | DEM → 다음 모델 넘김의 그림 · ⚠ 'Effective ionic conductivity' 는 계산 안 함 |
| 2 | 공정 변수 정의 (V_f · V_p · H_g · S · W_ref · 층간 경로 R · U · X) | 용어 정의 |
| 3 (a–e) | ★ 한 가닥: 위 · 옆 모습 (A05 · A08 · A12) · 16 경우 폭 · 높이 · CV (인쇄) · 네 주효과 | 요인 설계 + 실패 칸 보고의 본 · §3-2 재현 |
| 4 (a–f) | ★ A08 한 층의 λ 효과 (폭 · 높이 · Sq · 덮임 · 겹침 · 골) | 같은 계에서 측정 지표 여럿이 서로 다른 방향 |
| 4g (숨음) | PDF 래스터에만 있는 패널 g (λ 별 위 모습) | 원고 결함 기록 |
| 5 (a · b) | λ 0.85 세 조건의 Sq · 겹침 | '겹침 크다 ≠ 표면 고르다' |
| 6 (a · b) | 한 층 위 모습 (λ 75 · 85 · 100 %) · R08-75 두 번째 층 쌓기 6 장 | 공정 시각화 |
| 7 (a–c) | ★ R04-75 단면 (층간 빈 곳 노랑) · 18 구조 ε_v · ε_tot · f_IL | 빈 곳 정의 셋 · 분해 / 가정 몫 분리 |
| 8 (a · b) | ★ τ_Y (인쇄 18 값) · σ_Y,app ↔ R_Y | 같은 ε · τ 인데 σ ≈1.9 배 · 정규화 함정 |
| 식 크롭 25 장 | `eq_01_*` … `eq_25_*` (식 14 · 16 · 19 · 20 은 인쇄 깨짐 그대로) | 보고서 공정 · 수송 절 |
| 근거 문단 20 장 | `txt_p7_p8_*` (계보 [36]–[38]) · `txt_p9_*` (공급 원료 · 입자 종류) · `txt_p10_*` (부피 규약 · 출처 번호) · `txt_p11_*` · `txt_p12_*` (운동학 공급 · 표면 장력 없음) · `txt_p13_*` (가정 냉각) · `txt_p14_*` · `txt_p15_*` (결합 미보정) · `txt_p16_*` (실패 = 수치 한계) · `txt_p17_*` (이완 끝 판정 · 비용) · `txt_p20_*` · `txt_p20_p21_*` · `txt_p21_p22_*` (이상 접촉) · `txt_p32_*` · `txt_p34_*` · `txt_p35_*` (한계) | 원문 인용용 |

## 6. Post-processing ★
- **무엇을**: 구 탐침 외피 (5 µm) → 단면 띠 W · H (21 단면 · 1000 ± 25 µs) · 단면 투영 층 폭 · 1 µm 표면 높이 지도 → 평균 높이 · Sq · core 덮임 · 가닥 배정 → 이음매 투영 겹침 · 평면 건너는 BC–BC · BC–AM 결합 수 (기계 연결성) · 골 깊이 · A04 MSD → 0.5 µm 복셀 영역 (외피 + 틈 채움) → ε_v · ε_tot · f_IL → FVM 확산 (τ_Y) · 전자 (σ_Y,app · R_Y).
- **안 한 것**: 해상도 수렴 (복셀 · 커널 · 입자 크기 바꾸기) · 반복 런 · 실험 대조 · 이온 전도 (액체 전해질 상 없음 — 그림 1 목록과 다름) · 전기화학 · 접촉 저항 · 결합 수 숫자 (원문 방법만 · 결과 [미확인]) · 응력 · 강도.
- **이 카드의 후처리**: 그림 4e · 4f · 5b · 7b · 7c · 8b 원 래스터 판독 (90 행 · 눈금선 직선 맞춤 · 색 · 모양 · 채움으로 경우 판별 · 인쇄 범위로 검산) · 요인 설계 배치 추론과 네 주효과 재계산 · φ_BC · φ_AM · f · L/A 산술 · 단위 환산.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 공정 | 용융 필라멘트 FFF 인쇄 (노즐 흐름 · 퇴적 · 냉각 고화) · 압력 없음 | 냉간 압밀 300 MPa (판 서보 · 고정 이완) | **다른 공정** — 수치 전이 금지 |
| 재료 · 상 역할 | LFP-rich AM 구 (거의 절연 10⁻⁴ S/m) + BC (전자망 1 S/m) · 기공 = 나중에 액체 전해질 | NCM (AM · 전자망) + LPSCl (SE · 이온망) · 기공 = 나쁜 것 | 전자망 담지상이 반대 · 기공 의미가 반대 |
| 입자 / 연속체 | AM = 고체 구 하나 (r 5 µm) · BC = SPH 유체 입자 (r_env 2.355 µm) | DEM: AM · SE 둘 다 강체 구 (hooke/hysteresis · E_eff 1.35 GPa · 18 배 연화) · MPM: SE = J2 연속체 (E 1.53 · σ_y 0.30 · ν 0.49) · AM = 고정 골격 (scaffold) | 이 논문 = '무른 상은 연속체 · 단단한 상은 이산 고체' 혼성 — 우리 MPM scaffold 와 같은 나눔 (단 그들은 AM 이 움직이고 우리는 고정) |
| 넘김 | DEM 압출 출구 프레임 → RHEO (입자 수 · 상 · 반지름 · 출처 번호 보존 · 이음매 국소 이완) | DEM 압밀 끝 좌표 → MPM scaffold (AM 고정 · SE 씨앗) | ★ 같은 부류의 'DEM 출력 = 다음 모델 초기 조건' — 그들은 출처 번호를 끝까지 들고 간다 |
| 연산자 (빈 곳) | 기준 부피 합 = 회계 · 외피 합집합 = 기하 · 영역 = 탐침 외피 + 틈 채움 규칙 · 분해 / 가정 (BC 10 %) 몫 분리 | ε_sphere (구 부피 합) ↔ ε_union · 관례 오프셋 1.251 %p 사건 | ★ 같은 두 규약을 목적별로 따로 쓴다 |
| 수송 솔버 | 0.5 µm 복셀 FVM · 조화 평균 면 · 이상 접촉 (접촉 저항 0) · 상 값 가정 | STEP3 복셀 FV (CONTACT_FREE · CL-81) + 접촉망 Kirchhoff/Holm (웹앱) | 같은 부류 — 그들에게는 협착 가지가 없다 |
| τ 이름 | 'tortuosity factor' τ_Y = ε_tot G_hom/G_diff | tau2 = φ/f (수송 tortuosity · √ 아님) | 같은 꼴 · 단 ε 자리에 가정 공극 포함 · 기준 = 같은 영역 균질 확산 |
| σ 정규화 | σ_app = G·L_Y/A_Y (상자 높이 · 투영 면적) · R = 1/G 따로 보고 | σ basis 표지 (판 간격 해 ↔ L_mc 재척도) | ★ 정규화가 순서를 바꾼다는 같은 경고 |
| 속도 · 음속 | V_p/c_s = 0.010–0.015 · 밀도 편차 5 % 중단 | MPM 판 Mach 0.03 (`--platen-mach`) · 기하 규칙 경고 (CL-80/82/83) | 수치 음속 대비 공정 속도를 정해 두는 같은 규율 |
| 이완 끝 | 다섯 조건 × 연속 3 구간 (결합 집합 변화 포함) | 고정 이완 (hold) · settled_over_target · 언로딩 키트 | 그들의 판정이 더 많은 관측량을 묶는다 |
| 검증 | 실험 0 · 반복 0 · 해상도 시험 0 | 각 모델을 실험에 따로 보정 (frame [4]) | 우리 규율이 더 강하다 |

### 7-2. 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 공정 · 상태 | 분모 | 빈 곳 |
|---|---|---|---|---|
| **랩 표준** | LPSCl 순수 SE | 300 MPa | 진밀도 **1.64** g/cm³ (고정) | **10–13 %** |
| 이 논문 (인쇄 범위) | LFP-rich AM 구 + BC 유효상 (액체 LIB 양극) | FFF 두 층 · 압력 없음 · 냉각 이완 뒤 | 외피 + 틈 채움 영역 V_Ω (진밀도 아님) | ε_v 38.59–40.15 % · ε_tot (BC 10 % 가정) 42.83–44.29 % |
- **"랩 표준과 다른 문헌 값"** 자리 — 재료 · 공정 · 분모 · 기공의 역할이 다 달라 **견줄 수 없다** (빈 곳 40 % 대는 인쇄 가닥 사이 · 층 사이 · BC 안의 공간 · 일부는 가정).

### 7-3. 복셀 수송 (STEP3) ↔ 이 논문 — CONTACT_FREE 부류의 두 번째 함정
- 같은 부류 (조화 평균 면 · 계면 저항 0) 이고, 원문이 스스로 *"ideal-contact conditions, excluding additional contact resistance"* 라 적는다 (p.22) — CL-81 의 '복셀 σ = CONTACT_FREE 가지' 와 같은 지위의 외부 사례.  여기에는 실측 대조가 없어 상한 · 하한 판정을 주지 않는다 (kodama2020 은 같은 부류를 EIS 와 견줌).
- 새로 주는 것 = **정규화 기하 함정의 크기**: L/A 2.4 배 · σ 순위 ≠ R 순위 · '같은 ε · τ 인데 σ 1.92 배' 의 1.21 배가 L/A [카드 산술] — 우리 망 σ 를 판 간격 ↔ 질량 보존 두께 (L_mc) 로 다시 잴 때 같은 꼴의 표지가 필요하다는 근거.
- ⚠ 크기를 옮기지 않는다: 액체 LIB 상 값 (가정) · BC 가 전자망 · 복셀 0.5 µm 에서 BC 지름당 ≈9.4 복셀 · AM 지름당 20 복셀 [카드 산술] ↔ 우리 STEP3 복셀 0.15–0.4 µm (정본 `ebner2013_srxtm_nmc_cathode_microstructure_open_dataset_segmentation` 카드의 우리 쪽 칸).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 무른 상 (BC) 의 큰 변형 흐름 · 단단한 입자 (AM) 의 재배열 · 냉각 고화 (가정) — 공정 역학 쪽 (MPM 이 맡는 반쪽과 같은 자리이지만 SPH) + 복셀 수송 (CONTACT_FREE 부류).
- **없는 것**: 압력 · 하중 몫 · 접촉망 (협착 · 접촉 저항) · 입자 고체 소성 · 실험 보정.  ⇒ 우리 계획에는 '연속체 무른 상 + 이산 단단한 입자' 혼성의 한 구현 예 · 넘김 · 판정 규약만 준다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = 지시서 공통 지시 (COMMON.md) 가 준 값: DEM 18 배 연화 · E_eff 1.35 GPa · Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K = E/(3(1 − 2ν)) = 25.5 GPa [카드 산술]) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) 부피 규약 둘을 **목적별로** 나눈다 — 기준 부피 합 (질량 · 유량 회계) ↔ 외피 합집합 (기하 · 겹침 한 번) (p.10) = 우리 ε_sphere ↔ ε_union 을 연산자 등록에 함께 적는 근거 (2) 영역 V_Ω 의 정의 (탐침 반지름 · 틈 채움 한계 1.5 × 간격 · 50 µm) 가 빈 곳 값을 정한다 — 등록 칸에 '영역 규칙' (3) 분해된 몫 (ε_v) 과 가정 몫 (BC 10 %) 을 다른 열로 (ε_tot − ε_v = 0.1 φ_BC) | 압력 · 진밀도 분모 없음 |
| **단계 1** (3D 메모리 · 장 수) | 입자 ≈30,000 (공급 원료) · 64 코어 · 한 가닥 16–24 h · 두 층 1–2 일 · ≈10⁶ 걸음 [카드 산술] — 입자 모델의 비용 감각 | MPM 장 · 메모리 숫자 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 정성: '쌍의 하나라도 유체면 유체 상호작용 · 고체 접촉은 따로 더함' 이라는 혼성 규칙 (p.10) — 한 속도장 (무른 상) + 이산 고체 접촉 (단단한 입자) 꼴 | 2D 없음 · 비교 시험 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나 맞춤) | 없음 | — |
| **단계 5** (3D 복합 압밀) | 정성: 단단한 입자 (AM) 가 무른 유체상 안에서 재배열 · 뭉침 · 분리 (A12 위 모습 · p.23) · MSD 평탄 ≈1500–2000 µs (A04 만) | 압력 · 하중 몫 없음 · AM 은 점 하나 크기의 구 |
| **단계 6** (탈압 · 되돌아옴) | ★ 이완 끝 판정 — 다섯 관측량 (상태 · rms 속도 · 최대 속도 · 구간 최대 변위 0.1 µm · 접촉/결합 집합 대칭차 10⁻³) 을 **연속 3 구간** 만족 (p.17) → 우리 고정 이완 · 언로딩 런의 '언제 끝인가' 판정에 접촉 집합 변화율을 넣는 꼴 | 되돌아옴 숫자 없음 · 하중 제거 없음 |
| **단계 7** (형상 · 피복 · 수송) | ★ 복셀 FVM (조화 평균 · 이상 접촉) 의 정규화 함정 (σ_app ↔ R · L/A 2.4 배) · 같은 ε · τ 에서 σ 1.9 배 = 전자망 연결은 기공 지표로 안 잡힌다 · τ_Y = tau2 꼴 | 실측 대조 없음 · 상 값 가정 |
| **후보 D0** (지금 DEM) | 앞 단계 (sun2026) 의 DEM 출력이 다음 모델로 넘어가는 실제 예 · 넘어가면서 BC 를 DEM 구 → SPH 유체로 바꿈 (이유 진술 없음) | DEM 계산 자체 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 벽 = 고체 입자 4 층 (정해진 궤적 · 반력은 강제 전에 계산) · 노즐 = 가장 가까운 면 법선 가둠 힘 (원형 모서리) · AM–기판 = 탄성 + 법선 감쇠 | 마찰 · 미끄럼 계수 [미확인 SI] |
| **후보 A** (MPM 강체 AM + SE 한 속도장) | ★ 같은 나눔의 meshfree 판 — AM 이 **움직이는** 고체 입자 · BC 가 연속체 (SPH) · 유체–고체 상호작용은 커널로 | AM 이 해상되지 않음 (입자 하나) · 하중 몫 · 압력 없음 |
| **후보 A′** (입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE · NSCD) | 없음 | — |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 | AM 접촉 계수 SI |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | 시험 없음 — 해상도 · 커널 · 복셀 수렴 · 반복 런 0 (막대 = 공간 SD) · 수치 중단 2 건은 '수치 한계' 로 표지 | — |
| **R1–R7** | **R1**: AM 이 움직이고 재배열 (하중 몫 없음) · **R2**: A12 의 기판 위 미끄럼 · 국부 분리 (정성) · **R3**: '입자 경계 기억' 대신 **출처 번호 · 바퀴 표지** 유지 (입자 정체성 기억) · **R5**: 맞춘 값 0 (전부 가정) · **R6**: 무른 상 (BC) 의 모양 변화 = 연속체 흐름 | R4 (탈압) · R7 (AM 파괴) 없음 |
| **결과 전 대조 항목** | 없음 (우리 계와 재료 · 공정 · 상 역할이 다름) — 방법 비교용으로만: 같은 ε · τ 에서 σ 범위 · L/A 분해 · 요인 설계 재현 | 값 전이 금지 |

- **재료 · 차원 · 조건 차이**: LFP + 고분자/탄소 ↔ LPSCl + NCM · 3D = 같음 · 압력 0 ↔ 300 MPa · 용융 냉각 ↔ 상온 · 연속체 BC (SPH) ↔ 우리 SE (DEM 구 / MPM J2) · AM 이동 ↔ 우리 MPM AM 고정.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **DEM 출력 넘김 규약 (Ⓑ DEM → MPM 연계 · 입자 번호 승계)** — 넘길 때 *"particle number, phase, radius, and source identity"* 를 지키고 이음매만 국소 이완하며, 순환 공급이면 '바퀴 번호' 표지를 단다 (p.9–10).  우리 DEM → MPM scaffold 도 입자 번호를 MPM 물질점 묶음까지 들고 가면 입자 형태 · 피복 · SE–SE 계면을 한 번호로 묶을 수 있다 (`docs/reviews/mpm_coverage_interface_design_memo_20261103.md` §4 의 '번호 하나' 와 같은 방향).
2. **부피 규약은 목적별로 둘** — 회계 (기준 부피 합) ↔ 기하 (합집합) 를 원문이 처음부터 나눠 적는다 (p.10).  우리 ε_sphere ↔ ε_union 1.251 %p 사건의 반대 예 — 등록 문서의 연산자 칸에 두 값을 같이 적는다 (단계 0).
3. **이완 끝 판정에 접촉 집합 변화율** — f_E (결합 집합 대칭차 ÷ 큰 쪽) ≤ 10⁻³ 를 속도 · 변위와 함께 연속 3 구간 (p.17).  우리 고정 이완 · 언로딩의 끝 판정 후보 (단계 6 · U3 · U4).
4. **σ 는 L/A 와 함께, 저항은 따로** — 같은 컨덕턴스라도 정규화 기하가 2.4 배 다르면 σ 순서가 뒤집힌다 (X04 −3.9 % σ 인데 R −5.4 %).  LHS · 망 σ 인계에서 σ basis (판 간격 ↔ L_mc) 표지를 값 옆에 두는 이유의 외부 사례 (흐름 밖: LHS 인계 · σ basis).
5. **요인 설계의 빈 칸 보고** — 실패 두 칸을 '수치 한계' 로 표지하고 6 짝 평균임을 밝힌다 · 인쇄 값만으로 주효과가 재현된다 (§3-2).  우리 EXECUTION_FAILED 처분과 같은 꼴 (흐름 밖: 실행 실패 보고 규약).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "A particle-resolved FFF model built on the LAMMPS RHEO package (SPH viscous binder/conductive phase, solid spherical active-material particles, an assumed contact-triggered cooling state and cohesive links) takes DEM-extruded heterogeneous filaments as feedstock, preserving particle number, phase, radius and source identity (Sun et al., ChemRxiv 2026, preprint, not peer reviewed)."
- "In that model, two-layer printed LFP electrodes with total void fractions of 42.8–44.3 % (including an assumed 10 % unresolved binder nanoporosity) and through-thickness tortuosity factors of 1.73–1.82 differ by a factor of ≈1.9 in apparent electronic conductivity (0.0985–0.1912 S m⁻¹, ideal contacts) (Sun et al., ChemRxiv 2026)."
- 국문: *"같은 빈 곳 · 같은 확산 τ 인데 겉보기 전자 전도도가 1.92 배 — 그중 1.21 배는 정규화 기하 (L/A) 몫이다 (Sun 2026 ChemRxiv 원고 그림 8b 판독 · 카드 산술)."*
- 국문: *"이 원고의 FFF 모델은 앞 압출 DEM 의 입자 배치만 잇고 DEM 설정은 잇지 않는다 (BC = SPH 유체 · LAMMPS RHEO)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **동료 심사 전 원고** · 실험 대조 0 · 반복 0 · 해상도 시험 0 — 저자도 *"Experimental validation remains necessary"* (p.27) · 결과 = *"candidates for further evaluation rather than battery-level performance rankings"* (p.35).
2. **필라멘트 출처 어긋남** — 방법 절 [36] (Paredes-Goyes 2024) ↔ 초록 'twin-screw extrusion model' (= 서론 [37] sun2026) · 결론은 번호 없음 · 서론 p.8 의 *"these existing extrusion studies …"* 문장은 압출 연구가 아닌 [34,35] (Lombardo 2021 3D 건조 모델 · Ngandjong 2021 DEM 캘린더링) 를 단다.
3. **식 인쇄 깨짐** — 식 14 (q_ij 우변) · 16 (f_E 분모) · 19 (절댓값 막대) · 20 (분모) 가 '¿' · '∨' 로 깨져 있고, 식 4 의 목표 속도 아래첨자 · 식 22 의 F_in 도 깨짐 — q_ij 의 꼴 [미확인].
4. **그림 4g** — 본문이 인용하지만 PDF 페이지에서 잘려 안 보이고 캡션에도 없다 (§3-3).
5. **노즐 간격** — 단계 B *"fixed nozzle-bed gap of 30 µm"* (p.16) ↔ 35 µm (p.25 · p.28 · p.17).
6. **'four conditions'** — 이완 끝 조건을 다섯 개 나열한 뒤 *"the four conditions are mentioned above"* (p.17).
7. **그림 1 의 'Effective ionic conductivity'** — 계산하지 않음 (확산 τ · 전자만).
8. **오탈자**: 그림 3c 제목 *"Mean heigh measurementst"* · *"the quantity"* 가 겹친 문장 (p.15 *"softening factor the quantity"*) · *"as shown is Fig. 4b"* (p.28) · 'Pas' (Pa s) · 그림 8 캡션 기호 (텍스트 층) — 숫자에는 영향 없음.
9. **결합 · 냉각 · 점도 · 상 값 모두 가정** — 결합은 접촉 저항 · 강도에 보정 안 됨 (p.15) · θ 는 온도가 아님 (p.13) · η₀ 0.01 Pa s 를 실제 용융 점도와 견주지 않음 · BC 공극 10 % 미보정 (p.35).
10. **'≈2 배' 의 해석** — 퇴적량 · 경로 길이 · 정규화 기하가 구조마다 달라 층간 방향만의 효과가 아니다 (원문 p.30 · p.36) · L/A 몫 1.21 배 [카드 산술].
11. **판독 값** — 그림 4e · 4f 의 겹친 표지 (λ 0.85 · 1.00) 는 ±0.3 %p · ±0.2 µm 눈대중 · 나머지는 인쇄 범위로 검산 (digitized.csv 주석).
12. **SI 없음** — 표 S1(a–c) (경우별 설정) · S2 (힘 계수) · S4 (두 층 경로) · 절 S1 (넘김 식) · S5 (추가 결과) · 동영상 [미확인].
13. **서론이 약속한 기술자 중 결과가 없는 것** — 서론은 *"particle distribution, intra-strand porosity, effective conducting phase connectivity, tortuosity, and deposition-induced macroporosity"* 를 정량한다고 적지만 (p.8), 본문 결과에 나온 것은 형상 · 덮임 · 겹침 · 두 층의 빈 곳 · τ_Y · σ_e 뿐 — 입자 분포 변화 · 가닥 안 공극 · 평면 건너는 결합 수 (방법만 p.19) 의 값은 없다 (SI S5 [미확인]).
14. **문장 반복 (편집)** — p.30 *"Fig. 6 illustrates this transition, …"* 가 두 번 · p.34 *"Both quantities were derived from the). Both quantities were derived from the"* — 숫자에는 영향 없음.
15. **정량 순위의 조건 (저자)** — *"The quantitative rankings remain conditional on the reconstructed envelope, voxel resolution, assigned phase properties and ideal surface-following contacts."* (p.35).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 37 | P. Sun, P. Vigneaux, A.A. Franco, Discrete Element Method Modeling of an Extrusion Process with Recirculation for Dry Manufacturing of Lithium‐Ion Battery Electrodes, Batteries & Supercaps (2025) 2500211. | 앞 단계 (트윈스크류 + 재순환 DEM) | `sun2026_dem_extrusion_recirculation_dry_electrode` (권호 2026, 9) |
| 36 | B. Paredes‐Goyes, F.M. Zanotto, V. Boudeville, S. Grugeon, L. Dupont, A.A. Franco, Mesoscopic Model of Extrusion during Solvent‐Free Lithium‐ion Battery Electrode Manufacturing, Batteries & Supercaps (2024) e202300441. | 방법 절이 단 필라멘트 출처 | 없음 (papers/ ls · '202300441' grep = sun2026 카드 인용만) |
| 31 | E.T. Palermo, K.T. Wolf, J.T. Clemmer, T.C. O'Connor, Reproducing hydrodynamics and elastic objects: A hybrid mesh-free model framework for dynamic multi-phase flows, Physics of Fluids 36 (2024) 113337. | RHEO 패키지 원전 (SPH + 결합 입자 · 냉각 · 고화) — 후보 A 류의 meshfree 판 | 없음 |
| 38 | P. Sun, F. Fernandez, D.E. Galvez-Aranda, J.-P. Chehab, P. Vigneaux, A.A. Franco, Machine learning surrogate modeling of materials extrusion for lithium-ion battery electrode dry manufacturing, Energy Storage Materials 91 (2026) 105437. | 압출 DEM 대리 모델 · 역설계 | 없음 |
| 46 | S. Pinilla, F.M. Zanotto, D.Z. Dominguez, T. García, A.A. Franco, Carbon-binder-domain porosity extraction through lithium-ion battery electrode impedance data, Energy Storage Materials 74 (2025) 103818. | BC 내부 공극 (10 % 가정) 을 EIS 로 정하는 방법 | 없음 |
| 5 | V. Boudeville, S. Grugeon, A. Maurel, R. Lesieur, M. Louati, A. Cayla, S. Ursescu, C. Campagne, S. Panier, L. Dupont, Solvent-free extrusion of a LiFePO4-based monofilament for three-dimensional printing of a lithium-ion battery positive electrode, Journal of Power Sources 593 (2024) 233973. | 실험 원본 (필라멘트 · FFF) | 없음 (sun2026 카드 인용만) |
| 44 | T.-T. Nguyen, A. Demortière, B. Fleutot, B. Delobel, C. Delacourt, S.J. Cooper, The electrode tortuosity factor: why the conventional tortuosity factor is not well suited for quantifying transport in porous Li-ion battery electrodes and what to use instead, Npj Comput Mater 6 (2020) 123. | τ 정의 의존 | `nguyen2020_electrode_tortuosity_factor` |
| 50 | S. Ben Hadj Ali, A. Valisammagari, P.T. Bhutia, A.H. Dao, V. Viallet, V. Seznec, A.A. Franco, Fully coupled mechano-electrochemical modeling of 3D-resolved microstructures for solid state batteries manufactured by wet processing, Energy Storage Materials 90 (2026) 105304. | 같은 그룹 ASSB 3D 결합 모델 | `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` |
| 45 | M. Chouchane, A.A. Franco, Deconvoluting the impacts of the active material skeleton and the inactive phase morphology on the performance of lithium ion battery electrodes, Energy Storage Materials 47 (2022) 649–655. | 탄소-바인더 형태 ↔ 수송 분리 | 없음 |
| 51 | M. Duquesnoy, C. Liu, D.Z. Dominguez, V. Kumar, E. Ayerbe, A.A. Franco, Machine learning-assisted multi-objective optimization of battery manufacturing from synthetic data generated by physics-based simulations, Energy Storage Materials 56 (2023) 50–61. | 합성 자료 + ML 최적화 (향후 계획) | `duquesnoy2023_ml_multiobjective_manufacturing_optimization` |

---

## [미확인] 목록
- SI 전체 (절 S1 넘김 식 · 표 S1(a–c) 경우별 설정 · 표 S2 힘 계수 · 절 S4 · 표 S4 두 층 경로 · 절 S5 · 동영상).
- 필라멘트 원천 런 (모델 [36] 인지 [37] 인지 · 조성 · 회전수 · 투입 순서 · 프레임 시각) · 필라멘트 지름 · 노즐 지름 · 기판 입자 크기.
- AM–AM · AM–기판 접촉 계수 (탄성 · 감쇠 · 마찰) · τ_f (공급 완화 시간) · 노즐 가둠 힘의 꼴 · 출력 프레임 간격.
- 식 14 (q_ij) 의 꼴 · 식 16 · 20 의 분모 (본문 문장으로만).
- 단계 B 의 실제 노즐 간격 (30 ↔ 35 µm) · 두 층 구조마다 퇴적 물질량 · 경로 길이 · 시간 · 인쇄된 입자 수.
- 평면 건너는 결합 수의 결과 값 · A00 결과 · 단계 B 아홉 경우 중 그림에 없는 값.
- 확산 · 전도 풀이의 수렴 기준 · 복셀 해상도 시험.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-23)
- 서지: 1저자 메모 (P. Sun, F. Fernandez, P. Vigneaux, A. A. Franco · 제목 · ChemRxiv · 17 November 2026 · DOI 10.26434/chemrxiv.15012329/v1 · 43 쪽) = PDF p.1 · p.3 와 같다 · **43 쪽에 SI 없음** (표지 2 + 원고 41) · PDF 메타 subject 'ChemRxiv 2026.2026' · 생성 2026-11-21 · 표지 소속 1 은 *"UMR CNRS, Université de Picardie Jules Verne"* (원고 p.3 은 LRCS UMR CNRS 7314 로 완전 표기).
- 숫자: 텍스트 층 + 렌더 대조 — 텍스트 층에서 깨진 단위 (p.25 'μm μs' 반복 · p.15 '10⁻ µs ⁴') 는 렌더에서 '0.08 µm µs⁻¹' · '5 × 10⁻⁴ µs⁻¹' 로 확인 · 165 µm · 990 µm · ≈30,000 · 5 µm · 2.355 µm · 2.71 · 1.1 · 5 µs · 0.5 · 8 µm µs⁻¹ · 11.775 µm · 0.005 µs · 9.81 × 10⁻⁶ · 450 µs · 54 µm · 8 µm · 10 pg µm⁻¹ µs⁻¹ · 0.01 Pa s · 8 / 10 · 7 / 9 µm · 0.15–0.85 · 2 pg µs⁻² · 10 pg µs⁻¹ · 200 µs · 0.25 · 0.8 · 17 / 9 / 18 · 44 · 0.10 / 0.05 / 30 / 5 × 10⁻⁴ · 25 / 35 · 0.08 / 0.12 · 0.04 / 0.06 · 2.5 × 10⁻⁴ / 1 × 10⁻³ · 500 µm · 21 · 6 짝 · 5 % · 30 µm (p.16) · 0.75 / 0.85 / 1.00 · 200 µm · 25 µm · 35 → 60 µm · 1500 µs · 500 µs × 3 · 0.01 · 10⁻⁴ · 10⁻³ · 0.1 µm · 10⁻³ · 64 코어 · 16–24 h · 1–2 일 · 5 µm 탐침 · ±5 µm · 100–300 µm · 1000 ± 25 µs · 1 µm · 0.1 µs · 0.5 µm 복셀 · 1.5 배 · 50 µm · 10 % · 1 V · 10 µm · 1 · 0.1^1.5 · 0 · 0 · 1 · 10⁻⁴ S/m — 전부 위치 확인.
- 결과 숫자 (p.25–36) · 그림 3 · 4a–d · 5a · 8a 의 칸 안 글자 = 확대 렌더로 읽음 · 그림 4e · 4f · 5b · 7b · 7c · 8b = 원 래스터 판독 (digitized.csv · 인쇄 범위 · 비율 문장과 검산).
- 그림 래스터 8 장은 모두 content stream 의 clip 상자를 통해 그려진다 — 그림 4 만 clip 밖 (y > 471.4 pt) 에 잉크 (패널 g) 가 있다 (그림 3 래스터 아래 끝의 작은 회색 조각 183 화소는 무시).
- 정본 중복 확인: papers/ 목록 613 · DOI '15012329' · 'filament fabrication' · 'fused filament' · 'Pei Sun' grep — 이 원고 카드 없음 (sun2026_dem_extrusion = 앞 논문 · zhang2026 = 공동 1저자 Pei Sun 의 다른 글 · sun2026_ml_sulfur = 다른 저자 Jinlong Sun).

## 🔗 관련 카드
- 앞 단계 (같은 1저자 · 같은 해): `sun2026_dem_extrusion_recirculation_dry_electrode` — 이 원고 ref [37] · 트윈스크류 압출 + 재순환 DEM (LIGGGHTS) · 이 원고는 그 계열의 출구 필라멘트를 공급 원료로 쓰되 방법 절은 출처를 [36] 으로 단다 (§0-1) · 같은 것 = AM 반지름 5 µm · BC 공극 10 % 가정 / 다른 것 = BC 표현 (DEM 구 2.5 µm ↔ SPH 유체 2.355 µm) · 코드 · 밀도 · 상 전도도.
- 같은 공동 1저자 · 같은 해: `zhang2026_polymer_electrolyte_modeling_perspective` (Y. Zhang · P. Sun 공동 1저자 · Franco · Gerbaldi 교신 · ACS Energy Letters · 고분자계 전해질 모델링 관점 글 · 이 원고와 다른 주제).
- 같은 그룹 제조 사슬 · 수송: `ngandjong2021_dem_calendering_digital_twin` · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` · `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` · `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` · `duquesnoy2023_ml_multiobjective_manufacturing_optimization`.
- 복셀 수송 · τ 정의: `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` (같은 CONTACT_FREE 부류 + 실측 대조) · `nguyen2020_electrode_tortuosity_factor`.
- 건식 · 압출 공정: `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` · `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

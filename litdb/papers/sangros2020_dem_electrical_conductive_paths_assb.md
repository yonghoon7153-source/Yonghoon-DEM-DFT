<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목.  COMPREHENSIVE / paper-level standalone. -->
# ASSB(폴리머 SSB) 복합 양극의 **전자 전도경로**를 DEM으로 — A* 경로탐색 + 실린더-저항 등가회로 + percolation, LFP+CB+PEO — Sangrós Giménez (Chem. Eng. Technol. 2020)

> slug `sangros2020_dem_electrical_conductive_paths_assb` · DOI `10.1002/ceat.201900501` · type `DEM (LIGGGHTS) + A* 경로탐색 + 등가회로 σ + skeleton τ` · PDF `SangrosGimenez_2020_ChemEngTechnol_ElectricalConductivePaths_ASSB.pdf` · digested `2026-06-26` · status ✅
>
> ★ **이것은 사용자가 기대한 "NMC σ_e 자매편"이 아니다 — 메타가 전부 다르다(확인됨).**
> (1) **저자**: Sangrós Giménez, **Laura Helmers, Carsten Schilde, Alexander Diener**, Arno Kwade (2019/2020 자매 논문의 저자목록과 *다름*; 같은 TU-Braunschweig iPAT/BLB).
> (2) **DOI = 10.1002/ceat.**201900501 (task가 적은 .201900180은 *2020 Energy Tech 자매편*의 DOI — 본 논문 아님).
> (3) **소재 = LFP(인산철리튬) 활물질 + carbon black(CB) 도전제 + PEO-LiTFSI 폴리머 전해질** — NMC 아님, 황화물 아님. **ASSB는 맞으나 "폴리머 SSB"**이고, **전해질(PEO-LiTFSI)을 *절연체*로 보고 DEM에서 *공극(pore)으로 처리***(전자전도에 기여 안 함) — LFP+CB 입자만 시뮬.
> (4) **물성 = σ_ELECTRONIC(전자전도) 전용** + tortuosity(이온전도 *추정*만, Bruggeman). σ_ionic을 *풀지는* 않음.
> (5) **방법 = A* 최단경로 탐색(Hart 1968) + 실린더-저항 등가회로(R=ρ·l/A, *구속저항 없음*) + percolation theory**. **Holm 구속저항도, Kirchhoff 전류해도 아님** — Bazzoun/우리와 *방법론이 다르다*.
> ★ **위치**: 이 그룹 calendering-DEM 라인의 **σ_e 적용편(ASSB 버전)**. 2019(역학) → 2020 Energy Tech(LIB 삼중전달) → **본 논문(2020 ChemEngTech, ASSB 전자경로)** → Varkey 2026(halide multi-contact). LIB(2020 Energy Tech)에서는 전자전도가 같은 fabric-균질화였는데, 본 ASSB 편은 **경로탐색+등가회로**라는 *다른* σ_e 알고리즘으로 갈아탔다.

---

## 1. 한 줄 요약
**고체전해질(여기선 PEO-LiTFSI 폴리머, *절연체*)을 공극으로 보고, DEM으로 만든 LFP+CB 양극 구조 안에서 *전자가 흐를 수 있는 경로*를 A\* 최단경로 알고리즘으로 찾아 등가회로로 σ_electronic을 계산하는 후처리 도구를 제시하고, 실제 제조 양극(CB 0–5.2 wt%)의 4-point σ 실측으로 보정·검증한 논문.** 핵심 3성과: ① **DEM 구조 → 입자-접촉 그래프 → A\* 경로탐색 → 직렬-실린더 저항 + 전 경로 병렬 → σ** 의 3-step 파이프라인(Fig 3), ② **CB의 낮은 고유저항(LFP보다 ~10⁵× 작음)을 A\* 비용함수에 반영**(eq 5-6: `g·=‖Δr‖·ρ_ij/A_ij`, 거리만이 아니라 *저항*으로 경로 선택 → 전자가 CB를 경유하도록), ③ **percolation theory(Costamagna/Chen eq 15: P_CB=f(Z_CB,CB))와 비교** — CB 0.5 wt%는 percolation 임계 미만(σ≈0), 2 wt% 초과서 전도망 형성, **~5 wt% CB가 전자·이온의 최적 절충**. **단 σ_ionic은 *안 푼다* — tortuosity τ(skeleton model, eq 13)만 구해 Bruggeman D_eff=ε/τ·D_el(eq 12)로 이온확산을 *추정*.** 형상불변 강체 구(Hertz-Mindlin + van der Waals), σ_thermal 없음. **우리 σ_e(Kirchhoff+Holm 구속저항)와 *같은 목표·다른 방법*** — 그들은 *경로탐색+벌크 실린더저항*, 우리는 *전 노드 Kirchhoff+Holm 구속저항*.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/도전제/전해질) | 연구유형 |
|---|---|---|---|---|
| **Clara Sangrós Giménez, Laura Helmers, Carsten Schilde, Alexander Diener, Arno Kwade** (TU Braunschweig — Institute for Particle Technology iPAT + **Battery LabFactory Braunschweig BLB**) | **Chem. Eng. Technol. 43 (2020) No. 5, 819–829** (접수 2019-09-13, 수정 2020-02-04, 게재 2020) Open Access (CC-BY) | **10.1002/ceat.201900501** | **LFP** LiFePO₄ 활물질 + **carbon black(CB)** 도전제 0–5.2 wt% + **PEO-LiTFSI 폴리머 전해질**(PEO 600 g/mol + 3M LiTFSI, 9.64:2.2:1 wt% LFP/PEO/LiTFSi) — **폴리머 ASSB**. 전해질은 **절연체 → DEM서 공극(pore)으로 처리** | **DEM (LIGGGHTS)** 구조생성 + **A\* 경로탐색**(Python) + **등가회로 σ_e** + **skeleton-model tortuosity τ** + 실측 4-point σ 보정/검증 |

> ★ **계보 정정**: task 설명("NMC σ_e 자매편, ASSB-specific")은 *방향은 맞으나 소재·DOI가 틀림*. 본 논문은 **LFP+폴리머**다. 이 그룹의 σ_e 적용편이되, 2020 *Energy Technology* 자매편(`sangros2020_lib_electrode_dem_mech_elec_ionic`, DOI .201900180, NMC+액체전해질 LIB)과는 **다른 논문**. 두 2020 논문의 σ_e *방법이 서로 다름*: Energy Tech편 = **fabric-tensor 균질화**(eq 1: k_el=C_el·(1−ε)·CN/π·3·F_zz·r_c/r_p·k_p), 본 ChemEngTech편 = **A\* 경로탐색 + 등가회로**. 같은 그룹이 σ_e를 *두 방식*으로 구현했다는 사실 자체가 흥미(균질화 vs 경로탐색). 본 논문 ref [11] = Froböse(porosity 측정 절차), ref [22] = LIGGGHTS, ref [24] = van der Waals(Israelachvili), ref [34] = **Hart 1968 A\* 원전**, ref [37] = Vijayaraghavan(D_eff=ε/τ·D_el), ref [38] = Lee(skeleton model τ), ref [46] = Costamagna(percolation P_CB), ref [42] Chen / [21] Chen(percolation).

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (CB wt%, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **manufactured porosity (=전해질 함량 V_el)** | ε ≈ **0 (실측), 시뮬은 V_el로 대입** | 실제 양극은 calendering으로 **porosity ~0** | stated(본문 3.1) | ★ "측정된 porosity는 *전부 무시할 만큼 0*"(calendering 탓) → **공극=전해질**로 재정의. ε_sim = 전해질 부피분율 |
| **electrolyte content V_el** (=시뮬 porosity) | **60.00 / 48.80 / 48.80 / 47.20 / 46.6 %** | CB **0 / 0.5 / 2 / 3.7 / 5.2 wt%** | stated(Table 4) | CB↑ → 전해질↓(약간). **이게 DEM의 "porosity" 입력**(전해질=빈 공간) |
| **★ σ_electronic (실측, 4-point)** | **1.61×10⁻³ / 1.95×10⁻³ / 6.20×10⁻³ / 1.59×10⁻² / 2.54×10⁻² S/cm** | CB 0 / 0.5 / 2 / 3.7 / 5.2 wt% | stated(Table 4) | ★ **CB↑ → σ_e 지수적 증가**(0→5.2 wt%서 ~16×). 0.5 wt%는 0 wt%와 거의 같음(percolation 미달) |
| **★ σ_electronic (모델, Fig 4)** | **~0.0016 / ~0.0025 / ~0.006 / ~0.013 / ~0.022 S/cm** | CB 0 / 0.5 / 2 / 3.7 / 5.2 wt% | digitized(Fig 4, 파란 ●) | ★ **모델이 실측 추세 재현**, 단 **고-CB(3.7·5.2 wt%)서 실측보다 약간 *과소*** (병렬-경로 합산이 contact loss 미반영) |
| **σ_electronic (percolation theory, Fig 4)** | **~0.001 / ~0.0024 / ~0.007 / ~0.022 / ~0.034 S/cm** | CB 0–5.2 wt% | digitized(Fig 4, 녹색 ▲) | percolation(eq 14·15)은 **고-CB서 실측보다 과대** — 방향성·접촉면적 무시 탓(본문 지적) |
| **★ σ_e (모델, 고-CB 확장 Fig 5)** | **~0.008 → ~0.034 S/cm** (포화) | CB **8 / 10 / 15 / 20 wt%** | digitized(Fig 5) | ★ **6–8 wt% 초과서 σ_e 증가 완만**(percolation 완성 후 = 망 *개수*만 늘어남). knee ~5–8 wt% |
| **specific number of conductive paths n'_paths** | **~10 → ~38 µm⁻¹** | CB 0 → 20 wt% (eq 16 정규화) | digitized(Fig 5, 주황 ■) | 경로 *수*도 CB↑에 증가(σ와 같은 포화) |
| **★ σ_ionic (모델, Fig 7)** | **~7.3×10⁻⁵ → ~4.6×10⁻⁵ S/cm** (감소) | CB 0 → 20 wt% | digitized(Fig 7, 주황 ■) | ★ **CB↑ → σ_ion *감소*** (CB 입자가 τ↑ → 이온확산 방해). σ_e와 **반대 방향** = 전자·이온 trade-off |
| **★ percolation 임계 (CB)** | **0.5 wt%는 미달(σ≈0), 2 wt% 부근서 전도망 형성** | CB wt% | stated(본문 4.2) | ★ "2 wt% 이하 = isolated cluster, percolation 미완"; 2–3.7 wt%서 σ 급증(percolation transition) |
| **★ σ 증가율(percolation 전후)** | 2→3.7 wt%: **+85.89 %** / 8→10 wt%: **+18.65 %** | σ_e 증가율 | stated(본문) | ★ percolation **직후 급증(86 %) → 완성 후 완만(18.65 %)** = knee 정량 |
| **LFP 고유 전도도 k_p (전자)** | LFP **0.023 S/cm**(분말, ε=0.60) → 단일입자 fit **ρ=6177.91 Ω·mm** | LFP 분말 보정 | stated(Table 3 + 본문 4.1) | ★ **LFP는 절연 아님**(전도성 코팅) — 본문 강조 |
| **CB 고유 전도도** | CB **4.390 S/cm**(분말, ε=0.74) → 단일입자 fit **ρ=0.07 Ω·mm** | CB 분말 보정 | stated(Table 3 + 본문 4.2) | **CB가 LFP보다 ρ ~10⁵× 작음**(0.07 vs 6177.91 Ω·mm) → A\*가 CB 경유 선호 |
| **★ E_LFP / E_CB (Young's)** | **123.90 GPa / 5.00 GPa** | LFP / CB (입력) | stated(Table 2, ref [26-28]) | ★ **CB는 무름(5 GPa)** vs LFP stiff(123.9). 우리 E_CAM 140·E_SE real 24와 다른 소재 |
| **Poisson ν (LFP / CB)** | **0.28 / 0.23** | (입력) | stated(Table 2) | |
| **COR (LFP / CB)** | **0.40 / 0.40** | (입력) | stated(Table 2) | |
| **밀도 ρ (LFP / CB)** | **4.28 / 1.96 g/cm³** | (입력, supplier) | stated(Table 2) | |
| **Hamaker 상수 A (LFP / CB)** | **1.21×10⁻¹⁹ / 1.09×10⁻¹⁹ J** | van der Waals (입력) | stated(Table 2) | ★ **인력 vdW 포함**(거리 d 제한) — Hertz-Mindlin + vdW |
| **거리 제한 d (vdW, LFP / CB)** | **7.30×10⁻⁶ / 7.80×10⁻⁶ mm** | vdW 컷오프 | stated(Table 2) | 안정성 위해 vdW를 distance d로 제한 |
| **PSD (LFP)** | **0.28 / 0.30 / 0.32 / 0.34 / 0.36 / 0.40 / 0.60 µm** (7 크기, ΔQ₃ 15/15/15/10/10/15/20 %) | laser diffraction | stated(Table 1) | ★ **LFP ~0.28–0.60 µm**(나노~서브µm, 작음) |
| **CB 일차입자 / 응집체** | 일차 **40–50 nm**, 시뮬 응집체 **65 nm**(전단 분쇄 고려) | SEM | stated(본문 + Fig 1) | CB 응집체 평균 85–500 nm이나 시뮬은 65 nm(전단) |
| **입자 수** | **6000 particles** (모든 케이스 동일) | RVE 가변(l=w=h) | stated(Table 4·5) | 도메인 l=w=h: **6.8 / 4.57 / 3.25 / 2.69 / 2.43 µm** (CB 0–5.2 wt%); 고-CB: 2.19/2.05/1.83/1.69 µm |
| **압축속도 (calendering 모사)** | plate 속도 = **0.75 mm/s** (= 실측 시험기 시료홀더 속도) | DEM 압밀 | stated(본문 3.1) | 일정속도, 목표 V_par 도달 시 정지 |
| **전기측정 하중** | LFP: **380 N**, 복합 양극: **40 N**, 전류 10 mA, 3 s | 실측 4-point | stated(본문 2) | |
| **electrolyte diffusion coeff D_el** | **2×10⁻⁴ S/cm⁻¹** (Pesko et al. [39]) | 이온추정 입력 | stated(본문 3.3) | Bruggeman D_eff=ε/τ·D_el 용 |
| **σ_thermal** | **없음** | — | — | 본 논문 미측정(전자·이온만) |

## 4. 시뮬레이션 방법 ★

### 4.0 전체 구조 — 3-step σ_e 파이프라인 (Fig 3)
**DEM 구조 → (Step 1) 입자-접촉 그래프 생성 → (Step 2) A\* 알고리즘으로 전도경로 탐색 → (Step 3) 등가회로(직렬 실린더 + 병렬 경로) → σ_e.** 별도로 tortuosity(skeleton model)를 구해 Bruggeman으로 σ_ionic을 *추정*. **핵심 = "DEM이 만든 구조에서 전자가 *실제로 흐를 수 있는 경로*를 찾는다"** — 그래서 σ_e가 단순 부피분율(percolation theory)보다 정확.

### 4.1 code / version
- **DEM = LIGGGHTS** [22] (open source). **"LIGGGHTS는 원래 입자 운동·효과 분석용인데, 여기선 *구조 생성*용으로만 씀"**(본문 명시) — 압밀로 전극 구조를 만들고, *접촉면적*을 뽑는 게 목적. 압력은 **위·아래 plate**가 반대로 움직여 압축; plate 속도 0.75 mm/s. 중력 무시, x·y 주기경계.
- **σ_e 후처리 = Python** (별도 스크립트). 입자 정보 파일(ID·반경·위치) + 접촉 파일(접촉쌍·**접촉면적**) 2개를 LIGGGHTS에서 export → 그래프 생성 → A\* → 등가회로.
- **tortuosity = MATLAB** (skeleton model, Lee et al. [38]).

### 4.2 ★ DEM 접촉법칙 — Hertz-Mindlin + van der Waals (소성 *아님*)
**본 논문의 DEM은 탄소성이 *아니다*** — 2019/2020 자매편의 Thornton–Ning 탄소성과 *다르다*. 본문 명시: **"Hertz-Mindlin contact model, with the additional implementation of van der Waals forces"** (eq 미제시, 표준 Hertz-Mindlin).
- **법선/접선 = Hertz-Mindlin**(탄성 spring + damping). **항복캡 없음**(2019의 p_y 캡과 대조).
- **인력 = van der Waals**(eq 미번호; vdW 포텐셜의 1차 미분, Israelachvili [25]). 안정성 위해 거리 d(LFP 7.30e-6, CB 7.80e-6 mm)로 제한, Hamaker A(LFP 1.21e-19, CB 1.09e-19 J).
- ★ **왜 탄성인가**: 목적이 *구조 생성 + 접촉면적 추출*이라 (calendering으로 porosity→0인 *최종* 구조만 필요) — 압밀경로 정밀도가 σ_e 추출에 1차적이지 않음. **단 이는 "접촉면적이 탄성 Hertz 면적"임을 뜻함**(소성 pile-up·Tabor 면적 없음) → 우리 Stage-E와 대조점(§B·C).

### 4.3 ★★ σ_electronic 알고리즘 — A\* 경로탐색 + 등가회로 (eq 2–11, **본 논문 고유 핵심**)
**Step 1 — 그래프 생성:** 입자 = 노드, *접촉한* 입자쌍 = 엣지(엣지 길이 = 두 입자 중심 간 유클리드 거리). 접촉면적은 LIGGGHTS에서 명시 export.

**Step 2 — A\* 최단경로 탐색 (Hart 1968 [34], Dijkstra 확장):**
- 시작노드 = **z 최저 입자들**, 목표노드 = **z 최고 입자들**(전류방향 = z = 집전체 수직).
- 비용함수 (eq 2): `f(n) = g(n) + h(n)` — g=시작→현재 누적비용, h=현재→목표 추정비용(휴리스틱).
- **순수 거리 버전** (eq 3·4): `g(n)=g(n_cur)+‖r_next − r_cur‖`, `h(n)=|z_goal − (z_next + r_next)|` (z-방향 유클리드).
- ★ **저항-가중 버전 (eq 5·6) — 본 논문의 트릭**: 최단*거리* 경로가 최*저저항* 경로와 다르다(CB가 LFP보다 ρ 10⁵× 작음). 그래서 A\*를 **저항으로 재가중**:
  - `g(n) = g(n_cur) + ‖r_next − r_cur‖ · ρ_ij/A_ij` (eq 5) — ρ_ij = 접촉 두 입자의 평균 저항, A_ij = 접촉면적.
  - `h(n) = |z_goal − (z_next + r_next)| · ρ_i/A_i` (eq 6) — ρ_i = *가장 전도성 높은 소재*(CB)의 저항(휴리스틱이 과대평가 안 하도록 admissible 유지), A_i = 최대 접촉면적.
  - ★ **이 재가중으로 A\*가 *CB를 경유하는 경로*를 선호** → "전자는 LFP보다 CB를 따라 흐른다"는 물리 반영. 본문: "the selected pathways corresponded to the electrically most favorable path, taking into consideration the contact resistance between the particles." ⚠ **단 이것은 "구속저항(Holm)"이 아니라 *접촉면적으로 나눈 벌크저항*** — 구속저항 항은 없음(§C 핵심).

**Step 3 — 등가회로 (eq 7–11):**
- **각 경로 = 직렬 실린더들**(Fig 2): 접촉점 좌표 (eq 7) `c⃗_{1,2}=r⃗₁ + (r⃗₂−r⃗₁)/‖r⃗₂−r⃗₁‖·(r₁−δ/2)` (δ=overlap), 실린더 길이 (eq 8) `l_cyl=‖c⃗_{1,2} − c⃗_{1,3}‖`(연속 접촉점 간 거리), 실린더 단면적 (eq 9) `Ā=(A_{1,2}+A_{1,3})/2`(인접 두 접촉면적 평균).
- **실린더 저항 (eq 10): `R_p = ρ·l_cyl / Ā`** — ★ **순수 벌크 저항**(ρ=고유저항, l=길이, A=단면적). **구속/수렴저항 항 *없음*.** "접촉면적의 질이 전자전도에 직접 영향"(본문)이라 A를 명시 쓰지만, *Holm 1/(2σa) 형태가 아니라* l/A 형태.
- **한 경로의 총저항 = 직렬 실린더 합**; **전 경로 = 병렬** → 등가저항 R_eq.
- **σ (eq 11): `σ = h_RVE / (w_RVE·l_RVE·R_eq)`** — 등가저항 + RVE 크기로 비전도도.

### 4.4 ★ σ_ionic — *풀지 않음*, tortuosity로 *추정*만 (eq 12·13)
**본 논문은 σ_ionic을 직접 풀지 않는다.** ASSB라 porosity≈0 → 통상 LIB의 pore-Bruggeman이 *적용 불가*하다고 명시. 대신:
- **tortuosity τ (eq 13, skeleton model, Lee [38]): `τ = L_eff,A→B / h_RVE`** — 모든 입자 위치·크기로 *공극(=전해질)*을 정의 → MATLAB로 skeleton 추출 → 경로 유효길이/높이. ★ **τ는 *공극(전해질) 위상*에서 계산**(전자경로와 별개).
- **이온확산 (eq 12, Vijayaraghavan [37]): `D_eff = ε/τ · D_el`** — ε(porosity) 대신 **전해질 부피분율** 대입(ASSB는 전해질이 공극을 채우므로). D_el=2×10⁻⁴ S/cm(Pesko [39]). → σ_ionic ∝ ε_el/τ로 *추정*(Fig 7).
- ★ **즉 이온은 *여전히 전해질 상*을 통해 흐른다고 봄**(폴리머 전해질이 절연이지만 *이온*은 통과). σ_e는 LFP+CB *고체*망, σ_ion은 *전해질*상 — **두 상이 분리**. **이게 황화물 ASSB(우리 LPSCl)와 다른 점**: 우리는 SE *고체 입자망*이 이온전도체(§B·C·우리 baseline).

### 4.5 ★ 입자 처리 (DEM판 "무질서 처리")
- **구만** (LFP 7 대표크기 0.28–0.60 µm, CB 65 nm 단일크기 = bidisperse). **rigid 입자 + Hertz-Mindlin CONTACT 탄성 + vdW 인력**. **항복캡 없음, 소성 없음**(2019의 Thornton–Ning과 *다름*). **입자 형상 안 변함** — δ-overlap은 접촉면적 계산용 기하량(소성 흐름 아님). **형상소성·void-fill 없음** = frame[5]에서 우리 MPM이 메우는 절반.
- **파쇄 미모델**(입자 안 깨짐; bond도 없음 — 본 논문은 binder bond *없이* vdW만).
- **초기구조**: 6000 입자(LFP+CB) **랜덤 비중첩 배치** → 위·아래 plate 압축으로 목표 V_par 도달까지 → 접촉 발생.
- ★ **CB 응집(aggregation)은 *명시 모델 안 함*** — CB를 65 nm 단일 응집체 구로 근사. 실제 CB 망상구조(fractal)는 단순화.

### 4.6 도메인/RVE / servo / seeds / 압력범위
- **RVE = l×w×h 정육면체**(케이스마다 가변, 입자수 6000 고정 위해). CB 0–5.2 wt%: **6.8/4.57/3.25/2.69/2.43 µm**; 고-CB 8–20 wt%: 2.19/2.05/1.83/1.69 µm. **x·y 주기경계**, z 비주기(전류방향).
- **압밀 = calendering 모사**: 위·아래 plate 반대 이동(0.75 mm/s), **목표 V_par**(=실측 전해질 함량 → porosity) 도달 시 정지. **단일 "압력" 개념 아님** — *부피분율* 목표로 멈춤(실측 양극의 전해질 함량 V_el 재현).
- **seeds/실현**: 명시 반복수 불명(2019는 5 seed). 본 논문은 조성당 1 구조 위주 보고.
- **CB 함량 sweep**: 실측 5수준(0/0.5/2/3.7/5.2 wt%, Table 4) + 시뮬 확장 4수준(8/10/15/20 wt%, Table 5).

### 4.7 후처리 지표
- **σ_electronic (eq 11)**: A\* 경로 → 직렬 실린더 → 병렬 → R_eq → σ.
- **specific number of conductive paths n'_paths (eq 16): `n'_paths = n_paths · h_RVE/(w_RVE·l_RVE)`** — 경로 *개수*를 RVE 크기로 정규화(케이스 간 비교 위해). σ와 함께 percolation 진행 추적.
- **tortuosity τ (eq 13)** → σ_ionic 추정(eq 12).
- **percolation probability P_CB (eq 15, Costamagna [46]/Chen [42]): `P_CB = [1 − ((3.764 − Z_CB,CB)/2)^2.5]^0.4`** — CB-CB 배위수 Z의 함수. **percolation theory σ (eq 14, Bruggeman-type): `σ = σ₀·((1−ε)·V_CB·P_CB)^µ`** (µ=1.5 Bruggeman factor) — 본 논문의 *비교 대상*(자기 A\* 모델이 이걸 이긴다고 주장).

### 4.8 특이사항/튜닝
1. **LFP·CB 고유저항을 분말 측정으로 보정**(Table 3): LFP 분말 σ=0.023 S/cm(ε=0.60), CB 분말 σ=4.390 S/cm(ε=0.74) → 각각 *단일입자* 저항으로 역산(LFP ρ=6177.91, CB ρ=0.07 Ω·mm). ★ 이게 σ_e의 *유일한* fit 입력(나머지는 구조에서).
2. **A\* 저항-재가중(eq 5·6)이 핵심 트릭**: 순수 거리 A\*면 LFP를 많이 지나는 짧은 경로를 고르나, 저항-가중으로 *CB 경유 저저항* 경로를 고름 → 물리적.
3. **percolation theory와 *명시 비교*(Fig 4)**: 자기 A\* 모델 vs Costamagna percolation vs 실측 → A\*가 실측에 *더 가깝다*(percolation은 방향성·접촉면적 무시로 고-CB 과대).
4. **LFP는 절연 아님**(전도성 코팅) 강조: percolation theory는 "CB만 전도"로 가정하나 *실제 LFP도 전도* → A\* 모델은 LFP-LFP 경로도 포함(percolation이 놓치는 것).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | (a) 저배율 + (b) 고배율 **SEM** of CB-LFP granule — 작은 입자=CB, 굵은 입자=LFP. CB 일차입자 40–50 nm, LFP ~350 nm(SEM)/0.28–0.60 µm(laser) | LFP·CB 크기 대비(CB≪LFP). 우리 SE≪CAM과 *위치는 반대*(여기 CB가 작은 도전제) |
| **2** | **등가회로 실린더 근사 모식** — 입자 1-2-3 접촉점 c⃗_{1,2}·c⃗_{1,3}, 접촉면적 A_{1,2}·A_{1,3}, 평균단면 Ā, 실린더 | ★ **eq 7–10의 그림.** 우리 R_bulk=ρ·l/A(=이 실린더)와 *정확히 같은 형태* — 단 우리는 +Holm 구속저항 |
| **3** | ★ **3-step σ_e 파이프라인 2D 모식**: DEM 구조 → Step1(입자-접촉 그래프) → Step2(A\* 경로탐색, 검은 굵은 선=전도경로) → Step3(등가회로 R_eq, 병렬 저항 + σ=h/(w·l·R_eq)) | ★ **우리 DEM→네트워크 σ_e 파이프라인과 *목표 동일, 방법 다름*.** 우리 Step2=Kirchhoff 전노드(경로탐색 아님), Step3=Holm 포함 |
| **4** | ★ **σ_e vs CB wt%(0–5.2)**: 실측(검은 ■-점선) vs **percolation theory(녹색 ▲)** vs **A\* 모델(파란 ●)**. percolation은 고-CB 과대, **A\* 모델이 실측에 더 근접**(단 고-CB서 약간 과소) | ★ **A\* 모델 vs percolation vs 실측 3자 검증.** 우리 σ_e 폼(LOOCV 0.953) 검증 narrative의 LFP판 |
| **5** | **σ_e + 경로수 n'_paths vs CB wt%(0–20, 확장)**: 둘 다 CB↑에 증가하되 **6–8 wt% 초과서 완만**(σ knee). 2–3.7 wt% +85.89 %(급증, percolation) vs 8–10 wt% +18.65 %(완만, 망 개수만) | ★ **percolation knee 정량**(~5–8 wt% CB). 우리 σ_e의 φ_AM⁴ percolation-backbone·dead-AM 임계와 개념 대응 |
| **6** | (a) CB 3.7 wt% + (b) CB 15 wt% **시뮬 구조 + A\* 전도경로 그래프**(우측). 15 wt%가 경로 *조밀*(작은 CB가 서로 가까움 → CB 경유 多); 3.7 wt%는 LFP-LFP 경로 길이 더 김 | ★ **A\* 경로 시각화** — "고-CB서 CB-CB 접촉이 경로를 지배"의 그림. 우리 force-chain/percolation 시각화와 대응 |
| **7** | ★ **σ_e(좌축, 파란 ●) + σ_ion(우축, 주황 ■) vs CB wt%(0–20)**: σ_e ↑(포화), **σ_ion ↓**(7.3e-5→4.6e-5). CB 입자가 τ↑ → 이온확산 방해 | ★ **전자·이온 trade-off 한 그림** — "CB 5 wt% = 절충"의 근거. 단 σ_ion은 τ-Bruggeman *추정*(직접 솔버 아님) |

## 6. Post-processing ★
- **무엇**:
  - **σ_electronic**: **A\* 경로탐색**(eq 2–6, 저항-가중) + **등가회로**(eq 7–11, 직렬 실린더 R=ρl/A + 병렬 경로) → σ. **구속저항 없음.**
  - **n'_paths (eq 16)**: 전도경로 *개수* 정규화 → percolation 진행도.
  - **tortuosity τ (eq 13)**: skeleton model(MATLAB, Lee [38]) on *전해질 공극* 위상.
  - **σ_ionic (eq 12)**: Bruggeman D_eff=ε_el/τ·D_el *추정*(직접 솔버 아님).
  - **percolation P_CB (eq 15)**: CB-CB 배위수 Z → percolation 확률 → percolation-theory σ(eq 14, 비교용).
  - **고유저항 보정**: LFP·CB 분말 σ → 단일입자 ρ 역산(Table 3).
- **도구**: **LIGGGHTS**(DEM 구조·접촉면적) + **Python**(A\* + 등가회로) + **MATLAB**(skeleton τ). 실측: **4-point/two-point σ**(Z020 Zwick 시험기, 380 N[LFP]/40 N[복합], 10 mA, 3 s), **SEM**(Helios G4 CX FEI), **laser diffraction**(LFP PSD), Mitutoyo 두께.
- **수치화·플롯·기록 방식**: CB wt% sweep(실측 5 + 시뮬 4)으로 σ_e·σ_ion·n'_paths를 CB 함량 함수로. **A\* 모델 vs percolation theory vs 실측 3자 parity**(Fig 4). 고유저항 2개(LFP·CB)만 분말로 fit, 나머지는 구조에서.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (2020 ChemEngTech, 폴리머 ASSB) | 우리 (황화물 ASSB) | 차이 / 이유 |
|---|---|---|---|
| **연구 범위** | **σ_electronic 전용** + σ_ion *추정*(τ-Bruggeman). σ_thermal 없음 | 압밀(DEM·MPM) + **전달 삼중항 σ_i/σ_e/σ_thermal** + grade | **우리 삼중항 우위** — 그들 σ_e 단일채널(+이온 추정) |
| **★ σ_e 알고리즘** | **A\* 최단경로 탐색 + 등가회로**(eq 2–11) | **Kirchhoff 전노드 Σ(φi−φj)/R=0** | ★ **방법 근본 다름**: 그들=*대표 경로* 탐색(A\*), 우리=*전 노드 동시* 전위해(Kirchhoff). Kirchhoff가 *모든* 병렬경로를 동시에 푸는 정확해; A\*는 *선택 경로*들의 병렬 근사 |
| **★ 접촉저항 모델** | **벌크 실린더 R=ρ·l/A (eq 10) — 구속저항 *없음***. 접촉면적 A는 *단면적*으로만 | **R_total = R_bulk(=ρl/A) + R_Holm(=1/(2σa))** | ★★ **우리가 그들 R=ρl/A에 *Holm 구속저항을 더한다*.** 그들 실린더 = 우리 R_bulk와 *동일식*; 우리는 +Maxwell/Mikic 수렴저항. 점접촉의 *구속*이 그들엔 빠짐 |
| **★ 접촉면적 종류** | **Hertz-Mindlin 탄성 접촉면적**(소성 없음) | **Stage-E 소성 접촉면적**(Tabor+volume) | ★ **그들=탄성 면적 / 우리=소성 재유도.** 고-밀도서 그들 σ_e 과소(Fig 4)는 탄성 면적 한계와도 연결 |
| **★ 소성 종류** | **없음 — Hertz-Mindlin 탄성 + vdW**(2019의 Thornton–Ning과 *다름*!) | MPM 진짜 J2 SHAPE 소성 + DEM hooke/hysteresis | **그들 본 논문은 *순수 탄성* DEM**(항복캡조차 없음). 형상변화·소성 둘 다 없음 → 우리 MPM·path-A와 대조 |
| **★ 이온 전도체 위상** | **전해질(폴리머)상이 이온전도체**(τ-Bruggeman, ε_el/τ) — *공극=전해질* | **SE 고체 입자망이 이온전도체**(Holm/Kirchhoff) | ★ **위상 다름.** 그들 폴리머 ASSB도 *전해질상*이 이온경로(LIB pore-Bruggeman의 변형); 우리 황화물은 *SE 입자 접촉*. 단 그들 σ_ion은 *추정*(직접 솔버 아님) |
| **percolation 처리** | **percolation theory(Costamagna eq 15)와 *비교*** — 자기 A\* 모델이 더 정확 주장 | √(φ−φc)·CN²·f_p³ percolation-backbone(우리 폼에 내장) | 둘 다 percolation 중시. 그들=외부 percolation 식과 대조; 우리=폼에 backbone 지수 |
| **압밀 모드** | **calendering 모사**(plate 압축, *V_par 목표*서 정지 — 압력 아닌 부피분율) | **cold-press**(단축 정수압 hold, ~300 MPa) | 그들은 압력 sweep 아님(전해질 함량 재현) — P-vs-porosity 곡선 없음 |
| **소재 (AM)** | **LFP**(123.9 GPa, ρ_e 6177.91 Ω·mm = 전도성 코팅, 절연 아님) | **NMC811**(140 GPa, Trevisanello σ_S/σ_P) | 다른 AM. LFP σ_e ≪ NMC; CB 도전제 명시(우리 VGCF/SuperP 대응) |
| **전해질** | **PEO-LiTFSI 폴리머**(절연체→공극; 이온만 통과) | **LPSCl 황화물**(고체 이온전도, σ_grain 3.0) | ★ **폴리머 SSB ≠ 황화물 ASSB.** σ·이온위상·E 전부 다름 → 절대값 전이 금지 |
| **도전제** | **CB**(carbon black, 65 nm, σ 4.39 S/cm, E 5 GPa) | **VGCF/SuperP**(Stage-2 부피점유) | ★ **그들은 CB를 *명시 입자*로 모델**(σ_e 경로에 직접 기여) — 우리 CBD 부피점유보다 *전자경로*에 직접. 흡수 가치 |
| **검증** | **실측 4-point σ_e**(CB 0–5.2 wt%) + percolation 대조 | solver=ground truth(Minnmann·Cronau·Bazzoun 외부 앵커) | ★ **그들 σ_e 실측이 LFP쪽 앵커**(우리 NMC로 직접 전이 불가, 방법만) |

### ★★ 핵심 대비 1 — σ_e *방법*: A\* 경로탐색(그들) vs Kirchhoff 전노드(우리)
- **그들(A\*)**: DEM 구조에서 *대표적인 저저항 경로들*을 A\* 최단경로로 찾아(z 최저→최고), 각 경로를 직렬 실린더 저항으로, 전 경로를 병렬로 묶어 σ. **장점**: 빠르고, "전자가 CB를 따라간다"는 물리를 *경로 선택*으로 명시. **한계**(본문 자인): **"모든 경로를 *마지막에 병렬로만* 묶어 — *경로 간 상호작용(interconnected paths)*을 무시"** → 고-CB(접촉 많을 때) σ_e *과소*(Fig 4). 즉 A\*는 *선택된 경로 부분그래프*만 풀고, 그 사이 교차연결을 놓침.
- **우리(Kirchhoff)**: *모든* 노드에 전위 φ를 부여하고 `Σ(φi−φj)/R=0`을 *동시에* 풀어 — **경로를 고를 필요 없이 전 접촉망의 정확한 전류분배**를 얻는다. 교차연결·병렬·직렬이 자동 포함 → 그들이 놓친 "interconnected paths"가 우리에겐 *내장*. **이게 우리 σ_e가 *방법론적으로 더 정확*한 정확한 이유**(그들 자인한 한계가 우리 솔버엔 없음).
- ★ **깔끔한 대조**: "Sangrós 2020은 *대표 전도경로*를 A\* 최단경로로 탐색해 병렬 등가회로로 σ_e를 근사하며 — 본문 스스로 *경로 간 교차연결을 무시해 고-CB에서 σ_e를 과소평가*한다고 인정한다. 우리 Kirchhoff 전노드 솔버는 *모든* 접촉의 전류분배를 동시에 풀어 그 교차연결을 *내장*하므로 경로선택 근사가 불필요하다." (frame[4]: 같은 DEM 구조에 *더 정확한 전달 솔버*.)

### ★★ 핵심 대비 2 — 접촉저항: 그들 R=ρl/A (구속저항 *없음*) vs 우리 R_bulk + Holm
- ★ **이게 가장 load-bearing한 차이.** 그들 실린더 저항 (eq 10) `R_p = ρ·l_cyl/Ā` = **순수 벌크 저항**(고유저항×길이/단면적). **우리 `network_conductivity.py`의 `R_bulk`와 *수식이 동일*** — 우리도 각 입자를 `R_bulk = (d_ij/2)/(σ·π·r²)` (= ρ·l/A 반-실린더)로 본다(`network_conductivity.py:322-324`). **그러나 우리는 거기에 `R_constriction`(Holm 1/(2σa) 또는 Mikic (1−a/r)^1.5/(2σa))을 *더한다*** (`:342-354`), 그들은 *더하지 않는다*.
- **물리적 의미**: 두 입자가 면적 A로 접촉할 때, 전류는 (i) 입자 *벌크*를 지나고(=그들 실린더 R=ρl/A) (ii) *접촉 좁은목으로 수렴*하며 추가저항을 받는다(=Holm 구속저항, 점접촉일수록 큼). **Sangrós는 (i)만, 우리는 (i)+(ii).** 점접촉(작은 a)에서 구속저항이 *지배적*이므로, **그들 모델은 점접촉의 저항을 *과소평가*** → 같은 구조서 σ_e *과대* 경향(단 A\*의 경로-누락 과소와 부분상쇄 — 그래서 Fig 4가 그럭저럭 맞음).
- ★ **우리 우위 정량화**: 우리 `network_conductivity.py`는 `R_bulk fraction`을 직접 보고한다(`:937`). 우리 솔버에서 **R_bulk(=그들 전부)는 보통 전체의 일부**이고 **R_constriction(=그들이 빠뜨린 것)이 나머지** — 즉 Sangrós 모델은 *우리 R_total에서 구속저항을 뺀 부분집합*이다. **그들 = 우리의 `mode='bulk_only'` 한계**(우리 코드에 *그 모드가 옵션으로 존재*, `:503·662·728` — 그들 모델은 우리 코드의 한 토글).
- ★ **깔끔한 대조**: "Sangrós의 실린더 저항 R=ρ·l/A는 우리 솔버의 *벌크 항*과 동일하다 — 그러나 그들은 점접촉의 *수렴(구속) 저항*(Holm 1967, R=1/(2σa))을 포함하지 않는다. 우리는 R_total = R_bulk + R_constriction으로 둘 다 푼다; Sangrós의 모델은 우리의 `bulk_only` 한계에 해당한다."

### ★★ 핵심 대비 3 — 접촉면적: 그들 탄성 Hertz vs 우리 Stage-E 소성
- 그들 단면적 Ā(eq 9)는 LIGGGHTS의 **Hertz-Mindlin *탄성* 접촉면적**(소성 없음 — 본 논문 DEM은 순수 탄성). 우리는 **Stage-E(Tabor + volume)로 *소성* 접촉면적을 재유도**해 σ의 구속저항 입력으로 쓴다.
- ★ **그들이 자인한 고-CB σ_e *과소*(Fig 4)** 는 (a) A\* 경로-누락 + (b) 탄성 접촉면적(소성 pile-up 미반영) *둘 다*의 결과일 수 있다. 우리 Stage-E는 (b)를 보정하는 방향(고압서 소성으로 접촉면적이 Hertz보다 커짐 → 저항↓ → σ↑). **단 그들은 *압력 sweep이 아니라 CB 함량 sweep*이라** 압력-소성 효과가 1차적이지 않음(차이를 직접 겹치진 못함).

### ★ 핵심 대비 4 — 이온 전도체 위상 (폴리머 ASSB도 전해질상, 우리 황화물은 SE 입자망)
- 그들 폴리머 ASSB는 **PEO-LiTFSI가 절연체지만 *이온*은 통과**하므로, σ_ionic을 *전해질상*의 ε_el/τ Bruggeman으로 *추정*(eq 12·13). 이는 LIB pore-Bruggeman의 변형(공극 대신 전해질 부피분율). **즉 폴리머 SSB는 이온위상이 LIB에 가깝다**(전해질이 *연속상*).
- 우리 황화물 ASSB는 **SE 고체 입자가 서로 *접촉*해야 이온이 흐른다**(연속상 아님, 접촉망) → Holm/Kirchhoff. **그들 τ-Bruggeman 추정과 우리 SE-network 구속해는 *다른 물리*.** ★ 단 *방향*은 양쪽 같음: **CB↑(그들) / AM↑(우리) → 이온경로 방해 → σ_ion↓**(Fig 7 ↔ 우리 Minnmann CAM↑→σ_ion↓). 메커니즘만 다름(그들 τ↑, 우리 SE 접촉↓).

### frame[5] 위치
- **이 논문 = 전달 측의 *σ_e 절반만*** (rigid 탄성 구 → A\* 경로 → σ_e). **σ_ion은 추정(직접 솔버 아님), σ_thermal 없음, 형상소성·void-fill 없음.** 우리 MPM이 메우는 역학 절반 + 우리 σ_ion/σ_thermal 솔버 + Holm 구속저항이 *전부 그들에 빠져* 있다.
- **우리 우위 = (i) 전달 *삼중항* 명시 Kirchhoff+Holm 솔버, (ii) Stage-E 소성면적, (iii) MPM 형상소성** — 셋 다 본 논문에 없음.

## A. 우리 DEM+MPM 대비 (comparison vs ours)
> §7과 중복을 피해, **그들 전자-전도경로 모델 vs 우리 σ_e(Kirchhoff + Holm + Stage-E + Trevisanello NCM)** 를 *접촉저항 처리 중심*으로 압축한다.

**그들 σ_e 파이프라인** = DEM(LIGGGHTS, Hertz-Mindlin 탄성+vdW) → 입자-접촉 그래프 → **A\* 최단경로**(저항-가중 eq 5·6) → **직렬 실린더 저항 R=ρl/A**(eq 10) → 전 경로 **병렬** → σ=h/(w·l·R_eq).
**우리 σ_e 파이프라인** = DEM(LIGGGHTS, hooke/hysteresis+adhesion) → 전 접촉 네트워크 → **Kirchhoff Σ(φi−φj)/R=0** (전 노드 동시) → **R_total = R_bulk(ρl/A) + R_Holm(1/(2σa)) + Stage-E 소성면적 + Trevisanello σ_S/σ_P NCM** → σ_e + 폼압축(LOOCV 0.953).

| 축 | 그들 (A\* + 실린더) | 우리 (Kirchhoff + Holm + Stage-E) | 판정 |
|---|---|---|---|
| **전류해** | A\* *대표 경로* 병렬 (교차연결 *무시*, 본문 자인) | Kirchhoff *전 노드* 동시 (교차연결 *내장*) | **우리 정확** ✓ (그들 자인한 한계가 우리엔 없음) |
| **접촉저항** | **R=ρl/A (벌크만)** — Holm 구속저항 *없음* | **R_bulk + R_Holm** (구속 포함) | **우리 추가** ✓ (그들 = 우리 `bulk_only` 토글) |
| **접촉면적** | Hertz-Mindlin *탄성* | **Stage-E *소성*** (Tabor+volume) | **우리 추가** ✓ |
| **AM σ 처리** | LFP 단일 ρ(분말 fit 6177.91 Ω·mm) | **Trevisanello σ_S/σ_P + NCM(r) GB 보정** | **우리 세분** ✓ (단결정/다결정 분리) |
| **percolation** | 외부 percolation 식과 *비교*(eq 15) | √(φ−φc)·φ_AM⁴·f_p³ *폼 내장* (β=4 Stage-14 lock) | 둘 다 percolation 중시; 우리=검증된 지수 |
| **검증** | **실측 4-point σ_e**(CB 0–5.2 wt%, LFP) | solver=GT (외부 NMC 앵커 일부) | **그들 실측이 LFP 앵커**(방법만 전이) |
| **속도** | A\* 빠름(경로탐색) | Kirchhoff(희소행렬) — 우리도 빠름 | 비등 |
| **삼중항** | σ_e만(+σ_ion 추정) | σ_e + σ_ionic + σ_thermal | **우리 우위** ✓ |

**정직하게 — 그들이 우리보다 앞선/다른 곳:**
- ① **CB를 *명시 입자*로 모델해 전자경로에 직접 넣음** — 우리 CBD(VGCF/SuperP)는 Stage-2 부피점유(전자경로에 *간접*). 그들처럼 도전제 입자를 *경로 노드*로 직접 넣으면 σ_e 정확도↑(흡수 후보, §B·C-①).
- ② **A\* 저항-가중 경로 시각화(Fig 6)** — "전자가 어느 입자를 따라 흐르나"를 *경로 그래프*로 직관적 표현. 우리 Kirchhoff는 전위장은 주나 *대표 경로*는 명시 안 함(시각화 흡수 가치).
- ③ **σ_e 실측(4-point, CB sweep) + percolation theory 대조** — 본 논문은 자기 모델을 *실측 + 독립이론* 둘 다와 검증. 우리는 solver=GT가 주(외부 σ_e 실측 앵커 약함). ⚠ 단 LFP+폴리머라 우리 NMC+황화물로 *절대값* 전이 금지.

## B. 적용가능성 (applicability to our model)
> **그들 전자-전도경로 방법이 우리 `network_conductivity.py`에 *구체적으로* 무엇을 줄 수 있나.** ⚠ **ASSB(폴리머)≠ASSB(황화물) + LFP≠NMC**라 *절대값·소재 전이 금지* — *방법·구조*만.

- ① ★ **CB(도전제)를 *명시 전자경로 노드*로 — 우리 CBD 부피점유의 업그레이드 (backlog A3/A4 연결)**:
  - 그들은 CB를 65 nm 구로 *명시 입자화*하고, A\* 비용함수가 *CB의 낮은 저항*(eq 5·6, ρ_CB/A)을 보고 CB 경유 경로를 고른다. **우리 σ_e는 VGCF/SuperP를 Stage-2 *부피점유*로만 다뤄 — 전자경로에 *직접 노드*로 안 들어간다.**
  - **매핑**: `network_conductivity.py`의 그래프 생성(엣지=접촉)에 **도전제 입자 노드를 추가**하고, 그 σ를 Trevisanello σ_AM이 아닌 *carbon 고유 σ*(그들 CB 4.39 S/cm 류)로 주면, 우리 Kirchhoff가 *자동으로* CB-경유 경로를 가중(A\* 없이도 — Kirchhoff는 저저항 경로에 전류를 더 보냄). ★ **즉 그들 A\* 트릭을 우리는 Kirchhoff로 *공짜로* 얻는다**(전류는 저저항으로 자동 흐름). 필요한 건 *CB 노드를 구조에 넣는 것*뿐.
  - ⚠ 단 우리 황화물 CBD는 PTFE 바인더+VGCF *섬유망*(fractal)이라 65 nm 구 근사가 안 맞음 — Lee2025/cbd_morphology_roadmap의 fibril 모델과 결합 필요.
- ② **A\* 경로 *시각화*를 우리 Kirchhoff 위에 얹기**: 우리는 전위장 φ를 푸니, 사후에 **최대전류 경로(steepest φ-gradient)를 추적**하면 그들 Fig 6 같은 "전도경로 그래프"를 *공짜로* 그릴 수 있다(viz 후보). 우리 force-chain 시각화와 같은 도구 계열.
- ③ ★ **그들 모델 = 우리 `bulk_only` 토글 = Holm 기여 정량화 lever**: 그들 R=ρl/A는 우리 `R_constriction=0`(bulk_only) 모드와 *동일*. → **같은 구조에서 우리 `full`(R_bulk+Holm) vs `bulk_only`(=Sangrós) σ_e를 비교하면, "Holm 구속저항이 σ_e를 얼마나 낮추는가"를 *그들 모델 대비*로 정량화**할 수 있다(우리 코드에 *이미 두 모드 존재* `:503·949-954`). **Bazzoun 비교(RNM은 Holm *있음*)와 짝**: Sangrós(Holm 없음)=상한, Bazzoun/우리(Holm 있음)=정확 → σ_e의 구속저항 기여를 *문헌 두 점*으로 bracket.
- ④ **percolation knee 비교**: 그들 σ_e knee ~5–8 wt% CB(2→3.7 +85.89 %, 8→10 +18.65 %). 우리 σ_e는 dead-AM 임계·f_p³를 폼에 내장 — **그들 "percolation 직후 급증 → 완성 후 완만" 곡선 형태**를 우리 σ_e-vs-φ_AM 추세와 *정성* 대조(절대 wt% 다름). Bielefeld2019 p_c=7.83·ln(d_AM)+36.67과 묶어 percolation-임계 문헌군.
- ⑤ **τ-skeleton(eq 13) — 우리 tortuosity와 대조**: 그들 σ_ion 추정의 τ는 *전해질 공극* skeleton(Lee [38], MATLAB). 우리 τ_Laplace/τ_Dijkstra(σ_thermal Ridge feature)와 *다른 위상*(그들=전해질상, 우리=SE상)이나, **skeleton-model τ 계산법 자체는 흡수 가능**(우리 pore-τ DiffuDict backlog A6과 연결).
- ⚠ **소재 caveat (절대 금지)**: σ_e 절대값(1.61e-3~2.54e-2 S/cm)·CB wt% 임계·고유저항(LFP 6177.91·CB 0.07 Ω·mm)·E(123.9/5 GPa)는 **LFP+CB+폴리머** — 우리 NMC811+VGCF+황화물로 *절대 전이 금지*. **방법(A\*·실린더·percolation 대조·τ-skeleton)과 *구조 추세*(CB↑→σ_e↑·σ_ion↓ trade-off, knee 형태)만** 전이.

## C. ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this DEM model)
> **결론 먼저: 본 논문(Sangrós 2020 ChemEngTech)은 ASSB 전자-전도경로 DEM 모델의 *선구적 적용편*이지만, 접촉저항 물리·전달 삼중항·형상소성·해석압축에서 우리가 명백히 SOTA를 앞선다.** 본 논문은 **σ_e 단일채널**(σ_ion은 τ-추정), 입자는 **형상불변 *탄성* 강체 구**(2019의 항복캡조차 *없음*), σ_e는 **A\* 경로탐색 + *구속저항 없는* 실린더 저항**, 소재는 **LFP+CB+폴리머**다. 우리 7개 차별점을 그들이 *하는 것/없는 것*에 매핑한다 — 모두 *증거 기반*(그들 A\*-경로근사·구속저항-부재·탄성-면적·LFP-범위를 근거로).

**(1) 전달 *삼중항* σ_ionic + σ_e + σ_thermal — 명시 Kirchhoff 전노드 솔버 (★ 가장 강한 우위)**
- **그들**: σ_**e 전용**. σ_ion은 *직접 안 풀고* τ-Bruggeman(eq 12·13)로 *추정*만. σ_thermal 없음. σ_e도 *전 노드 Kirchhoff가 아니라 A\* 대표경로 + 병렬* — 본문 스스로 "*경로 간 교차연결 무시 → 고-CB σ_e 과소*" 인정.
- **우리**: **3채널 모두**(σ_ionic LOOCV 0.975 / σ_e 0.953 / σ_thermal 0.903), **전 노드 Kirchhoff Σ(φi−φj)/R=0** — 교차연결·병렬·직렬이 *자동 정확*. 그들이 자인한 A\* 경로-누락 한계가 우리 솔버엔 *구조적으로 없다*. **삼중항·전노드 정확해 = 명백한 우리 SOTA.**

**(2) Holm 구속저항 + Stage-E 소성 접촉면적 (★ 두 번째 강한 우위, 가장 구체적)**
- **그들**: 접촉저항 = **벌크 실린더 R=ρl/A (eq 10)뿐 — Holm 구속(수렴)저항 *없음***. 접촉면적은 **Hertz-Mindlin *탄성*** 면적.
- **우리**: **R_total = R_bulk(ρl/A, =그들 전부) + R_Holm(1/(2σa), 그들이 빠뜨림) + Stage-E 소성면적**(Tabor+volume로 탄성 면적을 *소성* 재유도). ★ **그들 모델은 *문자 그대로* 우리 `network_conductivity.py`의 `bulk_only` 토글**(`R_constriction=0`) — 우리는 거기에 점접촉 수렴저항 + 소성면적을 더한다. **점접촉이 지배하는 sparse 구조에서 구속저항이 σ를 좌우** → 우리가 *물리적으로 더 완전*. (Bazzoun RNM도 Holm *있음* → Sangrós[없음]은 *우리·Bazzoun 공통 우위*의 반례 = 문헌이 우리 편.)

**(3) DEM↔MPM scaffold 커플링 + 진짜 소성 MORPHOLOGY (J2)**
- **그들**: 입자는 **영원한 *탄성* 강체 구**(Hertz-Mindlin+vdW, 항복캡조차 없음 — 2019 Thornton–Ning *후퇴*). **형상변화·void-fill flow 없음.**
- **우리**: **MPM 진짜 J2 소성 형상변화**(SEM 코어보존+경계평탄화 ✓), **부피보존 void-fill flow**, **DEM AM 골격 + SE만 MPM(scaffold)** 커플링(real_14 porosity 16.7↔15.6 % cross-val). **형상소성 = 우리 고유** (그들은 *탄성*이라 더더욱 없음).

**(4) fracture-aware transport (Auerbach + Lawn)**
- **그들**: 입자 파쇄 **미모델**(bond조차 없음 — vdW만; 입자 안 깨짐). 파괴-전달 연결 0.
- **우리**: **Auerbach 임계 + Lawn 미세균열 → fracture-aware Holm**(f_intact로 σ 부분전도 보정, 깨진 접촉 ~60 % 미세접촉 유지). **파쇄를 *전달*에 연결** = 그들에 전무.

**(5) 문헌-근거 σ_grain / σ_AM (Cronau + Trevisanello)**
- **그들**: LFP σ_e = **분말 측정 단일 ρ**(6177.91 Ω·mm) — 입경·결정성·GB 분리 없음. CB도 단일 ρ.
- **우리**: σ_e는 **Trevisanello σ_S/σ_P + NCM(r) GB 보정**(단결정 AM_S vs 다결정 AM_P 분리), σ_ionic은 **Cronau(r_SE) σ_grain**. **소재 물리를 입경-의존으로 세분** — 그들 단일 ρ보다 미시적.

**(6) 실험-앵커 독립 듀얼모델 frame[4]/[5]**
- **그들**: **단일 DEM 모델**(σ_e 실측 보정). 독립 2모델 교차검증 없음.
- **우리**: **DEM(전달) + MPM(역학)** 을 *각각 독립적으로* 실험에 보정(Minnmann·Cronau·Bazzoun) — *서로 cross-fit 안 함*(frame[4]). 수렴=교차검증, 발산=정량화 모델한계. 본 논문은 단일 모델이라 이 메타-검증 구조 없음.

**(7) 솔버→스케일링 법칙 LOOCV 압축**
- **그들**: σ_e를 *경로탐색 + 등가회로*로 케이스별 계산(고유저항 2개 fit). ML/LOOCV 압축 없음.
- **우리**: 네트워크 솔버 출력 → **스케일링 법칙(LOOCV 0.90–0.98) + grade_engine** 으로 압축, 외부 검증. 설계 knob → 전 metric 예측(Phase-3). 그들 케이스별 계산 ≪ 우리 LOOCV-검증 폼.

**⚖️ 정직하게 — 그들이 우리보다 앞선/다른 곳:**
- **① CB 도전제를 *명시 전자경로 입자*로 모델 (A\* 저항-가중)**: 우리 CBD는 부피점유(전자경로 간접). 그들 CB-노드-직접이 σ_e 정확도에 더 직접적 — **흡수 후보**(우리 Kirchhoff에 CB 노드 추가하면 A\* 없이 자동 가중, §B-①).
- **② percolation theory와의 *명시 대조 검증*(Fig 4)**: 자기 모델을 *실측 + 독립 percolation 이론* 둘 다로 검증 — 검증 narrative가 탄탄. 우리는 solver=GT가 주.
- **③ σ_e *실측*(4-point, CB sweep)**: LFP쪽이지만 *실험 절대 검증점* 보유. 우리 σ_e 외부 실측 앵커는 약함.
- **④ A\* 경로 *시각화*(Fig 6)**: "전자가 어느 입자를 경유하나"를 직관적 그래프로(우리 시각화 흡수 가치).
- ⚠ **단 ①②③④ 모두 LFP+CB+폴리머·σ_e 단일채널·탄성 강체 구 범위** — **삼중항·Holm 구속저항·Stage-E 소성면적·형상소성·해석압축에서 우리가 SOTA**라는 결론은 유지. 그들 우위는 *도전제 명시화·검증 narrative*, 우리 우위는 *전달 완전성(삼중항+구속저항+소성면적)·형상소성·다중모델·압축*. ★ **특히 (2) Holm-부재는 *같은 그룹 후속 Bazzoun 2026이 Holm을 도입*했다는 점에서 — 본 논문은 이 그룹 σ-모델의 *Holm-이전* 세대**임을 보여준다(Sangrós 경로탐색 2020 → Bazzoun RNM/Holm 2026 → 우리 삼중항+Stage-E). **문헌 진화의 *앞*에 우리가 있다.**

## 9. 인용 가능 문장 (deck/paper용)
- "Sangrós Giménez et al. (2020, *Chem. Eng. Technol.*) modeled the **electronic conductive paths** within polymer-electrolyte ASSB cathodes (LFP active material + carbon-black additive + PEO-LiTFSI, the electrolyte treated as an *insulating pore phase*) by an **A\* shortest-path search** over the DEM contact graph followed by an **equivalent circuit** (series fictional cylinders R=ρ·l/A, all paths in parallel), calibrated against four-point conductivity of real electrodes (CB 0–5.2 wt%) and benchmarked against percolation theory."
- "Their resistance model uses only the **bulk cylinder term R = ρ·l_cyl/Ā (eq 10)** and — by their own admission — *neglects the interconnection between conductive paths*, which makes their model **underestimate σ_e at high CB content**. Our solver instead solves **Kirchhoff's law on the full node set** (so path interconnection is built in) and adds the **Holm constriction resistance R = 1/(2σa)** that their cylinder model omits; Sangrós's model is exactly the **bulk-only limit** of our R_total = R_bulk + R_constriction."
- "In an **all-solid-state** cathode the electronic conductor is the active-material/additive particle network — a topology Sangrós and we share — but they resolve it with **representative-path A\* + cylinder bulk resistance** whereas we resolve it with **full-network Kirchhoff + Holm constriction + Stage-E plastic contact area**, across the **full transport triad (σ_ionic/σ_e/σ_thermal)** rather than electronic-only; and we add **true plastic particle morphology via MPM** that their rigid *elastic* spheres lack entirely."
- "Notably this is the **pre-Holm generation** of the Braunschweig group's σ model: their later companion (Bazzoun 2026) adopts the Holm constriction resistance and Kirchhoff balance that our solver already uses — placing our triad+Stage-E formulation ahead of the literature evolution Sangrós(A\* path, 2020) → Bazzoun(RNM/Holm, 2026)."

## 10. 주의/한계 (over-claim 방지)
- ★ **메타 정정(가장 중요)**: 저자 = Sangrós Giménez/**Helmers/Schilde/Diener**/Kwade; DOI = **10.1002/ceat.201900501**; 소재 = **LFP + CB + PEO-LiTFSI 폴리머**(NMC 아님, 황화물 아님). task가 적은 ".201900180 / NMC"는 *2020 Energy Tech 자매편*의 메타 — **본 논문 아님**. 두 2020 논문 혼동 금지.
- **폴리머 SSB (전해질=절연체→공극)** — 전자전도 *전용* 논문. σ_ionic은 *안 풀고* τ-Bruggeman으로 *추정*만(직접 솔버 아님). "그들 σ_ion 솔버"라 하면 안 됨.
- **이온 위상이 우리와 다름**: 폴리머 전해질이 *연속상*(이온은 전해질상 통과, ε_el/τ) ↔ 우리 황화물은 *SE 입자 접촉망*(Holm). 그들 σ_ion 절대값·τ를 우리 ASSB로 전이 *금지*(다른 전도 메커니즘).
- **DEM이 *탄성*(Hertz-Mindlin+vdW), 소성·항복캡 *없음*** — 2019 자매편의 Thornton–Ning 탄소성과 *다름*(본 논문은 구조생성·접촉면적 추출이 목적이라 탄성으로 충분). 그래서 접촉면적=*탄성 Hertz 면적*(우리 Stage-E 소성면적과 대조). **형상소성·void-fill·파쇄 모두 없음** → 우리 MPM·fracture 영역과 별개(frame[5]).
- **접촉저항에 구속저항(Holm) 없음 (eq 10 = ρl/A 벌크만)** — 점접촉 저항 과소평가. 우리 R_bulk+Holm과 비교 시 "그들=우리 bulk_only"로 명시(그들이 *틀린* 게 아니라 *부분*).
- **A\* 모델은 경로 간 교차연결 무시 → 고-CB σ_e 과소(본문 자인, Fig 4)** — 우리 Kirchhoff(전노드)와의 정확도 차이의 *그들 측 근거*. over-claim 말고 *그들 자인*을 인용.
- **σ_e 절대값(1.61e-3~2.54e-2 S/cm)·CB wt% 임계(~2 wt% percolation, ~5–8 knee)·고유저항(LFP 6177.91·CB 0.07 Ω·mm)·E(123.9/5 GPa)** 는 **LFP+CB+폴리머** — 우리 NMC811+VGCF+LPSCl로 *절대 전이 금지*. **방법·구조 추세만**(CB↑→σ_e↑·σ_ion↓ trade-off, percolation knee 형태, A\*·실린더·τ-skeleton 알고리즘).
- **압밀 = calendering 모사 + *V_par(부피분율) 목표 정지*** (압력 sweep 아님) → **P-vs-porosity 곡선 없음** — 우리 Heckel/압밀과 직접 비교 불가. porosity는 *측정상 ~0*(calendering)이라 "porosity=전해질 함량 V_el"로 *재정의*함(우리 ε 정의와 다름).
- **Fig 4/5/6/7의 σ·n'_paths·σ_ion 값은 디지타이즈**(작은 그래프) → **추세만(±)**. **stated**: Table 4(V_el·실측 σ_e·도메인크기), Table 3(LFP/CB 분말 σ·porosity), Table 2(E·ν·COR·ρ·Hamaker·d), Table 1(LFP PSD), 고유저항 fit(LFP 6177.91·CB 0.07 Ω·mm), 입자수 6000, plate 0.75 mm/s, percolation 증가율(85.89 %·18.65 %), D_el 2e-4, eq 5·6·10·11·13·15.
- **CB 응집(fractal) 단순화** — 65 nm 단일 응집체 구로 근사(실제 CB 망상 fractal 무시). 우리 CBD fibril 모델과 결합 시 주의.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

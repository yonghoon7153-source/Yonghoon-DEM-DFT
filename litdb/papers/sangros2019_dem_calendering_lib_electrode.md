<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목.  COMPREHENSIVE / paper-level standalone. -->
# LIB 전극 calendering(압연)을 DEM으로 — 단일 NMC 입자 탄소성 접촉모델(나노압입 보정) + 바인더 bond 모델 + ~17% 점탄성 회복 — Sangrós Giménez (Powder Technology 2019)

> slug `sangros2019_dem_calendering_lib_electrode` · DOI `10.1016/j.powtec.2019.03.020` · type `DEM (in-house, 나노압입 실험 보정 + calendering 실측 검증)` · PDF `SangrosGimenez_2019_PowderTech_DEM_LIBElectrode_Calendering.pdf` · digested `2026-06-26` · status ✅
>
> ★ **이것은 `sangros2020_lib_electrode_dem_mech_elec_ionic.md`의 PREDECESSOR(1부)다.** 2020(2부)이 σ_el·σ_ion·접착을 *그 위에 올린* 논문이라면, **2019(본 논문, 1부)는 그 토대가 되는 *역학 모델 자체*를 만들고 calendering 실측으로 검증**한 논문. 2020이 "식은 1차 논문에 있다(ref [1])"고만 하고 넘긴 **탄소성 접촉식(eq 1–9) + 바인더 bond식(eq 10–13)의 완전한 유도가 바로 여기 있다.** 즉 **우리 contact_models_layer_map 의 "Sangrós bond 모델 = 원전"의 진짜 원전**이고, 2019는 거기에 더해 (a) **나노압입으로 단일 NMC 입자 F-d를 측정해 항복비 YR을 직접 정함**, (b) **~17% 점탄성 회복(springback)** 을 정량화 — 둘 다 2020에 없는 본 논문 고유.

---

## 1. 한 줄 요약
**Li-ion 전극 calendering(압연 압밀)을 "미세(단일 입자) → 거시(전극)" 로 잇는 DEM 모델의 기초 논문.** 핵심 3성과: ①**단일 NMC 입자를 나노압입(TriboIndenter, 40개 입자)으로 측정**해 Hertz가 항복점 이후 F-d를 과대평가함을 보이고 **Thornton–Ning 탄소성 접촉모델**을 채택(항복비 YR=δ_y/x=8.59×10⁻³ 직접 fit); ②**바인더(carbon black+graphite+PVDF, additive-binder matrix)를 입자-입자 bond 로 명시 모델링**(법선·접선 힘+토크 전달, 임계강도 파단); ③실측 calendering 4압력(C1–C4)으로 보정·검증해 **전극 porosity·두께·자유표면적·NMC-NMC 접촉면적·배위수·끊긴 bond 수·접촉 방향성·내부응력**을 모두 재현, 그리고 **실험으로는 측정 불가능한 ~17% 점탄성 탄성회복(spring-back)** 을 시뮬로 정량화. **단, σ_el·σ_ion(전도도)는 아직 안 풂 — 그것은 2부(2020)** . 본 논문은 **순수 역학 모델**(porosity/응력/접촉/방향성). 액체전해질 LIB라 이온 채널 위상이 우리 ASSB와 정반대지만(2020에서 드러남), **본 1부의 메시지는 "calendering 역학을 어떻게 검증된 DEM으로 만드는가" + "단일 입자 측정으로 contact law 를 어떻게 anchor 하는가"** 다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/binder/전해질) | 연구유형 |
|---|---|---|---|---|
| **Clara Sangrós Giménez, Benedikt Finke, Carsten Schilde, Linus Froböse, Arno Kwade** (TU Braunschweig — Institute for Particle Technology + **Battery LabFactory Braunschweig BLB**) | **Powder Technology 349 (2019) 1–11** (접수 2018-10-10, 수정 2019-01-13, 게재 2019-03-16) | 10.1016/j.powtec.2019.03.020 | **NMC111** Li[Ni₁ᐟ₃Mn₁ᐟ₃Co₁ᐟ₃]O₂ AM **90 wt%** + conductive graphite **2 wt%** + carbon black **4 wt%** + **PVDF 4 wt%** binder(= additive-binder matrix); 용매 NMP. **액체전해질 LIB**(전해질은 본 논문 미모델 — 역학만) | **DEM (in-house)** = Thornton–Ning 탄소성 CONTACT + 입자-입자 BOND + **나노압입 실험 보정** + **pilot 압연(GKL 400 two-roll) 실측 검증** |

> ★ **계보**: 이 그룹의 **calendering-DEM 라인의 1번 논문**이다. **2019(본 논문, 역학 모델 + 검증) → 2020(`sangros2020_*`, 그 위에 σ_el·σ_ion·접착·전기화학사이클) → Varkey 2026(`varkey2026_*`, 같은 bond 모델을 halide ASSB로 multi-contact 추가)**. 본 논문이 인용하는 ref [1] = 그들 자신의 또 다른 선행(bond 모델의 더 자세한 설명; 본 논문 = 그 bond를 NMC 탄소성과 결합해 calendering에 적용). Thornton–Ning [16] = 우리 `papers/thorntonning1998_*` (경로 A LAW 원전). 본 논문은 ref [9] Wang(FEM graphite), ref [10] Kespe(spatially-resolved half-cell), ref [11] Lenze(P2D), ref [7] Ott(percolation+resistor-network) 등 calendering 시뮬 선행을 정리 — 그중 **본 논문의 novelty = 단일 입자 측정으로 contact law anchor + bond + 점탄성 회복**.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **noncalendered porosity** | **0.522** (ρ_coating 2.13 g/cm³) | position A, 압연 전, 90:2:4:4 | stated(Table 1) | 실험 앵커. coating mass loading 16.88 ± 0.12 mg cm⁻² |
| **calendered porosity** C1/C2/C3/C4 | **0.416 / 0.372 / 0.295 / 0.217** | 압연응력 19.82/42.71/79.13/159.37 MPa | stated(Table 1) | ρ_coating 2.61/2.80/3.15/3.49 g/cm³. ★ 2020의 C1–C4(0.417/0.368/0.305/0.270)와 **거의 같으나 미세 차**(같은 실측 시리즈의 다른 보정) |
| **calendered thickness h** C1/C2/C3/C4 | **151.2 / 142.2 / 129.2 / 118.6 µm** | (양면 코팅+집전체 포함) | stated(Table 1) | noncalendered h=180 µm. Al 집전체 두께 ~23.5 µm |
| **gap between rolls h_Rolls** | **130 / 108 / 80 / 20 µm** | C1/C2/C3/C4 (롤 갭) | stated(Table 1) | 4 line-load = 롤 갭으로 조절. 롤 직경 430 mm, 폭 465 mm, 속도 2 m min⁻¹ |
| **normal calendering stress P_Cal** | **19.82 / 42.71 / 79.13 / 159.37 MPa** | C1/C2/C3/C4 | stated(Table 1) | 시뮬 압밀 목표응력(position B) |
| **★ 점탄성 탄성회복 ER** | **10.25 % → ~17 %** (C1→C4 증가) | ER=(h_C−h_B)/h_A, posB→posC | stated(본문 Conclusion: "from 10.25% up to almost 17%") | ★ **실험 측정 불가능, 시뮬 고유.** C1만 C2보다 낮음(저압서 재배열 지배) |
| **specific elastic recovery (Fig 8)** | **~0.136 / ~0.171 / ~0.116 / ~0.103** | C1/C2/C3/C4, (h_C−h_B)/h_A | digitized(Fig 8) | C2가 최대(~0.171), 이후 C3·C4 감소(소성 지배) |
| **broken bonds per particle n_BB,p** | **~0.18 / ~0.55 / ~0.78 / ~1.0** | C1/C2/C3/C4 (position C) | digitized(Fig 10) | 압밀 강할수록 bond 더 끊김(임계응력 초과). 초기 bond/입자 = 3.44 (최대) |
| **coordination number CN** (posB) | **CN_C1=1.55 → CN_C4=2.19** | position B (압밀 도달) | stated(본문) + digitized(Fig 10) | posC는 posB보다 약간 증가(관성+탄성). 초기 posA: CN=0 |
| **CN (posB vs posC)** | CN_B < CN_C (전 케이스) | Fig 10 (B 진회색 / C 빗금) | digitized(Fig 10) | 탄성회복으로 약간의 추가 접촉 |
| **NMC-Al 집전체 접촉면적비 A_CC,p** | **~56 % / ~62 % (posC); posB는 더 큼** | C1·C2 ~56%, C3·C4 ~62/65% | stated(본문: "approximately 56% and 61% C1·C2, around 62% and 65% C3·C4") | A_CC,p=ΣA_CC,p/A_CC, A_CC=22500 µm². 압밀↑→NMC가 Al에 더 박힘 |
| **단일 NMC 입자 강성 — Young's modulus E_NMC** | **142 GPa** | pristine NMC (입력) | stated(Table 2, ref [19,20]) | 2020은 142.5→111.6(SOC 가변); 2019는 **고정 142** |
| **Poisson ν** | **0.25** | NMC (입력) | stated(Table 2, ref [21]) | |
| **COR (반발계수)** | **0.25** | NMC (입력) | stated(Table 2, ref [21]) | |
| **밀도 ρ_NMC** | **4.75 g cm⁻³** | NMC (입력) | stated(Table 2, ref [21]) | |
| **★ 항복비 YR (yield ratio)** | **δ_y = 8.59×10⁻³ · x** (x=입자크기, µm) | 나노압입 40 입자 선형회귀 (R²=0.89) | stated(Table 2, Fig 2) | ★ **단일 입자 측정으로 직접 결정한 탄소성 입력.** δ_y=항복 시작 법선변위 |
| **PSD (NMC)** | **x₁₀,₃=4.96 / x₅₀,₃=9.35 / x₉₀,₃=16.59 µm** (laser diffraction) | 실측 NMC | stated(Table 2) | 시뮬 입력 5 대표직경: **5 / 7.5 / 10.5 / 15 / 18 µm** |
| **입자 수** | **2237 particles** | RVE 150×150×h_A µm | stated | 측방 x·y 주기경계 |
| **★ 면적당 bond 강성 S_n=S_t** | **6 × 10¹² N m⁻³** | calendered cathode 보정값 | stated(본문 5.1) | ★ **이 논문에서 직접 보정.** 면적관련 결합강성(법선=접선) |
| **★ bond 파단 임계강도 (ultimate)** | **2 × 10¹³ N m⁻²** | bond breakage 기준 | stated(본문 5.1) | ★ **직접 보정.** 응력이 이 값 도달 시 bond 영구파단 + 힘·토크 제거 |
| **timestep** | **10⁻¹⁰ s** (≈ Rayleigh time의 20 %) | DEM | stated(본문) | LIGGGHTS [24] |
| **σ_el / σ_ion (전도도)** | **없음 — 본 논문 미측정** | — | — | ★ **이것은 2부(2020). 본 1부는 역학만.** |

## 4. 시뮬레이션 방법 ★

### 4.0 전체 구조
**미세(단일 입자 나노압입 → contact law 보정) → 거시(전극 RVE calendering → 구조·역학 지표)**. 본 논문의 핵심은 **두 모델의 결합** = (A) NMC 입자의 **탄소성 CONTACT** (Thornton–Ning, 나노압입 보정) + (B) 바인더의 **입자-입자 BOND**. 전기·이온 전도도는 다루지 않음(2020).

### 4.1 code / version
- **DEM** = **LIGGGHTS** [24] (open source; 본문 4절 "open source DEM simulation software LIGGGHTS"). 압력은 **위 plate(=압연 롤 모사)** 의 하강속도로 제어, NVE(중력 무시 — 입자가 µm 스케일). timestep **10⁻¹⁰ s** (≈ Rayleigh time의 20 %).
- 후처리 = 자체 스크립트(porosity, FSA, CN, bond 수, 접촉면적, fabric tensor, viral 응력 — 4.6·6절).

### 4.2 ★ DEM 접촉법칙 — Thornton–Ning 탄소성 (eq 1–9, **나노압입으로 보정**)
**왜 Hertz가 아니라 탄소성인가** (3절·Fig 1): 나노압입(TriboIndenter TI 900, Hysitron, 일정 하중·제하율 30 nm s⁻¹, 40 입자)으로 단일 NMC F-d를 측정한 결과 — **항복점 이전(겹침 ≲ 반경의 0.1 %)은 Hertz로 잘 맞지만(탄성), 항복점 이후 고압축에서는 측정 F-d가 Hertz 이론곡선에서 점점 벗어남(소성 기여)**. 따라서 Hertz는 **고압축서 실제 거동을 과대평가**(overestimate) → Thornton–Ning [16] 탄소성 채택.

**탄성 영역 (Hertz, contact radius a < 항복 contact radius a_y):**
- 탄성 법선력 (eq 1): `F_el = (4/3)·E*·√(R*·δ³)` — δ=겹침, E*=유효탄성률(E_i, ν_i로부터), R*=유효반경(r_i로부터).
- 접촉반경 (eq 2): `a = (3·F_el·R* / 4E*)^(1/3)`.

**항복 개시 (critical yield pressure p_y):**
- 항복 법선력 (eq 3): `F_y = (1/6)·(R*/E*)²·(π·p_y)³` — p_y=항복 시작의 최대 접촉압.
- 항복 법선변위 (eq 4): `δ_y = (1/4)·(R*/E*²)·(π·p_y)²`. ★ 접촉반경 a가 a_y를 초과하면 접촉이 소성화.

**탄소성 영역 (a > a_y), 압력분포가 elliptical→uniform 으로 바뀜:**
- 탄소성 법선력 (eq 5): `F_el-pl = F_y + π·p_y·R*·(δ − δ_y)` — ★ **선형 관계**(F와 δ가 선형; 항복 이후 plastic branch).

**제하 (unloading, Hertz로 — 잔류 소성변위 도입):**
- 제하력 (eq 6): `F_unloading = (4/3)·E*·√(R_p*·(δ − δ_R)³)` — δ_R=잔류 소성변위, R_p*=유효 소성 접촉반경(제하 시점의 유효 Hertzian 힘과 plastic 힘으로 결정, ref [1]/[18]에 따라). **항복점 미도달 시는 Hertz 그대로 제하**.

**★ 항복비 YR = 단일 입자 측정으로 직접 결정 (3절·Fig 2):** 40개 입자 각각의 **임계 법선변위 δ_y(소성 offset)** 를 나노압입으로 측정 → **δ_y vs 입자크기 x 선형회귀** → **δ_y = 8.59×10⁻³ · x** (R²=0.89). 이 기울기(=YR, yield ratio)를 **시뮬의 탄소성 모델 입력**으로 사용. 즉 p_y를 직접 안 주고 **측정된 YR로 항복점을 정함** — "단일 입자 실험으로 contact law를 anchor" 하는 것이 본 논문의 방법론적 핵심. (laser diffraction PSD x₅₀=9.35 µm 등 다분산이라 입자별 δ_y가 크기 따라 달라야 함 → YR 필요.)

### 4.3 ★★ 바인더 BOND 모델 (eq 10–13) — **= "Sangrós bond 모델"의 식 원전**
2020이 "식은 1차 논문에 있다"고만 한 그 식이 **본 논문 5절에 명시**. 바인더(additive-binder matrix = small additive particles[carbon black+graphite] embedded in PVDF)를 **인접 NMC 입자 사이의 solid bond**로 표현 — **법선·접선 힘 + 법선·접선 토크**를 전달:
- 법선 bond 힘 증분 (eq 10): `dF_b,n = −v_n · S_n · A · dt`
- 접선 bond 힘 증분 (eq 11): `dF_b,t = −v_t · S_t · A · dt`
- 법선 bond 토크 증분 (eq 12): `dM_b,n = −ω_n · S_n · (J/2) · dt`
- 접선 bond 토크 증분 (eq 13): `dM_b,t = −ω_t · S_t · J · dt`

기호: A=bond 단면적, J=극관성모멘트(polar moment of inertia), v_n/v_t=법선/접선 선속도, ω_n/ω_t=법선/접선 각속도, **S_n/S_t = 법선/접선 면적관련 결합강성(area-related bond stiffness) = 고체 bond의 변형 저항**.

**파단 (breakage):** bond에 걸린 응력(법선 또는 접선 인장)이 **임계 인장강도(ultimate tensile strength)** 에 도달하면 **bond가 영구파단**되고 해당 힘·토크가 시뮬에서 **제거**(재형성 없음).

**보정값(본 논문에서 직접 결정):** **면적당 bond 강성 S_n=S_t = 6×10¹² N m⁻³** (법선=접선 동일로 단순화), **임계강도 = 2×10¹³ N m⁻²**. 이 두 값은 **C1·C4를 보정용**으로 쓰고 **C2·C3로 검증**(아래 4.5)해 정함.

> ★ **재형성 여부 = Sangrós(영구파단) vs Ngandjong(재형성) 의 분기점**: 본 논문/2020 = **영구파단(once broken, no reform)**. Ngandjong 2021 SJKR = 끊겼다 재형성. 우리가 CBD bond를 넣을 때 두 철학 중 선택(§B 참조).

### 4.4 ★ 입자 처리 (DEM판 "무질서 처리")
- **구만** (NMC = 강체 구, 실측 PSD 다분산 → 5 대표직경 5/7.5/10.5/15/18 µm). **rigid 입자 + CONTACT 탄소성(Thornton–Ning) + 입자-입자 bond**. **입자 형상은 안 변함** — δ-overlap은 소성의 기하 프록시(진짜 흐름 아님). **형상소성·void-fill 없음** (= frame[5]에서 우리 MPM이 메우는 절반).
- **파쇄(fracture)는 본 1부에서는 입자 깨짐 미모델** — 본문이 고압(C4)서 "균열·입자 파쇄를 고려해야 정확"이라 *한계로만 언급*(2020에서 brittle 임계응력 기준으로 broken% 추가). **단 bond는 끊김**(eq 10–13 파단)이라 "구조의 파단"은 bond 레벨로 표현(입자 자체는 영원한 구).
- **초기구조 생성**: 2237 NMC 구를 **랜덤 비중첩 삽입**(constraint: not in touch) → bond를 인접 입자 사이 계산 생성 → plate 하강으로 접촉 발생.

### 4.5 도메인/RVE / calendering BC / servo / seeds / 압력범위
- **RVE = 150 × 150 × h_A µm** (h_A = noncalendered 전극 두께 = position A). 예비 민감도 연구로 150×150 면적이 valid·representative 확인. **x·y 주기경계**, z는 비주기(plate·집전체).
- **바닥 plate = Al 집전체** (aluminum properties), **위 plate = steel 롤 표면** (steel properties).
- **calendering 모식 (Fig 3, position A/B/C):**
  - **Position A**: 압연 전 (h_A, porosity 0.522). plate가 입자 위에 위치.
  - **Position B**: 위 plate가 **목표 최대응력 P_Cal**(C1–C4)까지 하강 (h_B, 최대 압밀). **여기서 모든 역학 지표를 읽음**(가장 critical).
  - **Position C**: 압력 해제 후 **점탄성 탄성회복(spring-back)** → 최종 구조 (h_C, h_C > h_B). **여기서 최종 porosity·CN·fabric tensor 를 읽음**.
- **속도/기하 (Fig 3a, eq 7–9):** 롤 직경 430 mm ≫ 전극 두께 → **접촉이 거의 법선방향**(접촉각 θ < 1°: C1 0.66°, C4 0.96°). 접촉각 (eq 7): `θ = cos⁻¹((R_Roll − s)/R_Roll)`, s = h_A − h_B. **상대 X-방향 속도 ≈ 0** → plate를 **z방향만** 이동(압연을 단축 압축으로 단순화 정당화). z속도 (eq 8): `v_z,A = (s/k)·v_Roll`, (eq 9): `v_z,B = 0`. 계산된 v_z,A 매우 작음(C1 0.011, C4 0.017 m min⁻¹) → **준정적(quasi-static)**, plate를 v_z,A로 일정 하강. B→C는 같은 속도 반대방향 상승.
- **압력범위**: calendering 응력 4수준 19.82–159.37 MPa (C1–C4). 별도 **초기 porosity sweep**(0.48–0.60)은 응력 42.71 MPa(=C2) 고정.
- **seeds**: 각 시뮬을 **5회**(서로 다른 초기 입자배열) 반복 — **표준편차 2–4.8 %**(porosity), 평균만 플롯.
- **보정/검증 프로토콜 (5.1, 4 조건):** C1·C4를 **보정**, C2·C3를 **검증**. valid 조건: (i) position B가 실측 P_Cal에 도달, (ii) posB porosity ε_B < 실측 최종 ε_C (실측 불가하나 더 낮아야), (iii) posB 두께 h_B > 롤 갭의 절반(h_Rolls/2; 한쪽만 모델링하므로), (iv) 압밀 후 h_C·ε_C가 실측과 **편차 15 % 이하**. → S_n=6×10¹² N m⁻³, 임계강도 2×10¹³ N m⁻²로 4 조건 모두 충족.

### 4.6 전달 솔버
- **없음.** 본 1부는 전기·이온 전도도를 풀지 않는다. (2020에서 eq 1[전자]·eq 2–4[이온]·eq 5[접착] 추가.) 본 논문이 만든 것은 **그 전도도식이 입력으로 쓸 미세구조 지표**(CN, 접촉면적, FSA, fabric tensor)다 — 4.7.

### 4.7 후처리 지표 (본 논문이 정의·계산한 것 — 2020 전도도식의 입력)
- **specific free surface area FSA (eq 15):** `FSA_p = (4πr_p² − Σ A_c,i) / ((4/3)πr_p³)` — 입자 표면적에서 모든 접촉면적을 뺀 자유표면(= Li⁺ 삽입에 전기화학적 활성), 부피로 정규화. 전체 FSA = Σ FSA_p. ΔFSA(eq 16): `(FSA_A − FSA_x)/FSA_A · 100`, x=B or C.
- **coordination number CN (eq 17):** `CN = n_c / n_p` (총 접촉수/입자수).
- **broken bonds per particle (eq 18):** `n_BB,p = n_BB / n_p`. 초기 bonds/입자 = 3.44 (최대, 압밀 전).
- **NMC-집전체 접촉면적비 A_CC,p (eq 19):** `A_CC,p = Σ A_CC,p / A_CC`, A_CC = 22500 µm² (집전체 표면적).
- **★ fabric tensor F_ij (eq 20–21) — 접촉 방향성:** `F_ij = (1/N)·Σ_α n_i^α n_j^α` (Satake [33]·Kanatani [34]), N=단위 접촉법선 수, n^α=α번째 접촉법선. 등방·편차 분해 (eq 21): `F_ij = F̂_ij + F'_ij = (1/3)δ_ij + F'_ij`. **F'_ij(편차부)** 가 0이면 방향성 없음(등방); 한 주값만 다르면 transversely isotropic; 셋 다 다르면 orthotropic. **F'_zz(압밀방향)** 가 핵심 — 음수면 z방향 접촉이 적음(압밀로 z방향 구속).
- **★ 내부응력 (per-particle viral, eq 22):** `σ_ij = (1/2)·Σ_{Nb}(r₁F₁ + r₂F₂)_ij + (1/2)·Σ_{Nbonds}(r₁F₁ + r₂F₂)_ij` — **pairwise 접촉항 + bond항** 합 (단위: 응력×부피). 거시응력 = 전 입자 합을 RVE 부피로 평균: `σ_electrode = (1/3V)·Σ(σxx+σyy+σzz)`. → SOC 함수 아님(본 1부는 압밀응력만; SOC는 2020).

### 4.8 특이사항/튜닝
1. **단일 입자 측정 → contact law anchor**(YR=8.59×10⁻³·x, R²=0.89): 본 논문 방법론의 핵심 — p_y를 임의로 안 주고 **나노압입 40 입자로 직접**.
2. **bond 2 파라미터(S_n, 임계강도)만 보정**, 나머지는 측정/미세구조에서 결정. C1·C4 보정 / C2·C3 검증 → 과적합 회피.
3. **Hertz vs 탄소성 직접 비교(Fig 6·7):** **Hertz+bond 모델은 porosity를 과소평가**(ε_B가 실측 ε_C보다 작아짐 = 물리적으로 불가능) → 탄소성이 **필수**임을 정량 증명. Hertz는 항복 후 F-d를 과대평가 → 같은 응력서 더 압밀 → 너무 낮은 porosity.
4. **점탄성 회복(spring-back) 을 시뮬로 정량화**(ER 10.25→17 %): 실험으로는 롤 사이 입자 위치를 µm 분해능으로 못 봐서 측정 불가 → **시뮬 고유 정보**.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | (a) **단일 NMC 입자 F-d 곡선** — 실측(검은 굵은선) vs Hertz(녹색 점선, **고압서 과대**) vs 탄소성(파란 점선) + **항복점(Yield point)** 표시; (b) **저압축 SEM**(항복점 이하, 매끈), (c) **고압축 SEM**(항복점 초과, 변형) | ★ **"Hertz가 항복 후 과대 → 탄소성 필요"의 1차 증거.** 우리 path-A(항복캡) 정당화의 LIB판. 단일 입자 측정으로 contact law anchor |
| **2** | **항복비 YR 결정** — 임계 법선변위 δ_y vs 입자크기 x (40 입자, ■), 회귀선 **δ_y=8.59×10⁻³·x** (R²=0.89) | ★ **다분산 PSD에서 입자별 항복점을 크기로 스케일.** 우리 Stage-E/Cronau(r_SE) 크기의존과 개념 대응 |
| **3** | (a) calendering 기하(롤 R_Roll, 접촉각 θ, 위치 A·B·C, 속도 v_z·v_x, h_A/h_B/h_C); (b) RVE 모식 150×150×h µm, position A→B(압밀)→C(회복) | **calendering 셋업 + "접촉이 거의 법선(θ<1°)이라 단축압축으로 단순화"의 정당화** |
| **4** | calendering 공정 모식 + **실측 단면 SEM**(Non-cal·C1–C4) vs **시뮬 구조**(색=입자반경, 빨강 굵음→파랑 작음). bond는 미표시 | 실측 SEM ↔ 시뮬 구조 1:1 검증. 우리 morphology 검증의 LIB판(단 그들은 형상불변 구) |
| **5** | ★ **electrode porosity vs mechanical stress P_Cal** (C1–C4, 0–160 MPa) — 0.522서 시작, **저압서 급강하 후 완만**(C2 0.193@42.71 MPa posB → 0.368 posC). ①decrease(압밀) ②increase(탄성회복) 화살표 | ★ **압밀곡선 형태**(elastic→plastic knee + 포화). 우리 P-vs-porosity·Heckel과 대조(LIB 저압 압연). **springback 시각화** |
| **6** | **최종 porosity 비교**: 실측 ε_C,exp(●) vs **탄소성+bond** ε_C,EP(■, 거의 일치) vs **Hertz+bond** ε_C,Hertz(▲, **항상 과대**) — C1→C4 | ★ **탄소성이 Hertz보다 정확**(Hertz는 porosity 과대평가). C4서 탄소성도 약간 편차(ε_C 0.247 vs exp 0.217 — 고압 한계) |
| **7** | **contact model 비교 — porosity vs P_Cal 전 곡선**: 탄소성+bond(컬러 실선) vs Hertz+bond(검은 점선). **Hertz가 더 빨리 낮은 porosity 도달**(ε_B < 실측 ε_C = 물리적 불가) | ★ **Hertz의 porosity 과소(=과대압밀)를 전 압력대에서.** 우리 "연화 없는 강체 구 floor" 논의와 대조(그들은 탄소성으로 해결) |
| **8** | ★ **specific elastic recovery ER vs 케이스**(C1–C4): ~0.136/0.171/0.116/0.103. **C2 최대**, 이후 감소. **C1 < C2**(저압서 재배열/percolation 지배, plastic 적음) | ★ **점탄성 회복 정량 — 실험 불가, 시뮬 고유.** 우리가 spring-back을 못 다루는데(static hold) 이게 추가 경로 |
| **9** | **ΔFSA(자유표면적 감소율) vs 케이스**(C1–C4), position B(채움)·C(회복) — 압밀↑ → FSA 더 감소(접촉↑). **posC > posB**(탄성회복으로 접촉 일부 풀려 자유표면 회복) | 압밀이 활성표면 줄임(전기화학 trade-off). posC>posB = springback이 접촉 일부 해제 |
| **10** | ★ **CN(좌축, posB·posC 막대) + broken bonds/입자 n_BB,p(우축, ★선) vs C1–C4**: CN 1.55→2.19(posB), n_BB,p 0.18→1.0. 압밀↑ → CN↑·끊긴 bond↑ | ★ **배위수 + bond 파단**을 한 그림. 우리 CN/coordination + fracture(f_intact)와 직접 대응 |
| **11** | **NMC-집전체 접촉면적비 A_CC,p vs C1–C4**(posB·posC): C1·C2 ~56%, C3·C4 62/65%. 압밀↑ → NMC가 Al에 더 박힘. **posB > posC**(탄성회복으로 일부 분리) | 집전체 접촉(전자 경로의 출입구). 우리 AM-집전체 접촉 개념 |
| **12** | **편차 fabric tensor 대각성분 F'_xx/F'_yy/F'_zz vs C1–C4** (position C): C1은 **F'_zz가 양(+0.047)**(z방향 접촉 우세), C2 거의 등방, **C3·C4는 F'_zz 음**(압밀로 z방향 접촉 상실, in-plane 우세) → **이방성 발달** | ★ **접촉 방향성이 압밀로 변함**(z→음). transport 이방성에 직결. graded-z/층상(Phase-5) 갈 때 방향성 항 근거 |
| **13** | **내부응력 대각 σ_xx/σ_yy/σ_zz + 총 크기 σ vs C1–C4** (position B): 압밀↑ → 응력↑(C4 ~220 MPa). C1은 **σ_zz가 σ_xx·σ_yy의 2배**(법선 압밀방향), C2 σ_zz/σ_xx≈1.4, C3 1.17, C4 1.08(고압서 등방화) | ★ **압밀도↑ → 내부응력↑**. 우리 MPM 응력장과 대응. bond항 미포함이라 Fig 12 이방성 완전반영 안 됨(저자 인정) |

## 6. Post-processing ★
- **무엇**:
  - **porosity / 밀도**: 압밀 후 ε, ρ_coating (Table 1). 실측은 mass loading + 측정두께 + 성분 평균밀도로(ref [6]). **5 seed 평균**(std 2–4.8 %).
  - **specific elastic recovery ER (eq 14):** `(h_C − h_B)/h_A` — posB→posC 회복. ★ **본 논문 고유 지표.**
  - **FSA (eq 15·16):** 자유표면적 + 감소율 ΔFSA.
  - **CN (eq 17)·broken bonds (eq 18):** 배위수 + 끊긴 bond/입자.
  - **A_CC,p (eq 19):** NMC-집전체 접촉면적비.
  - **fabric tensor (eq 20·21):** 접촉 방향분포 → 편차 F'_ij → 이방성.
  - **viral 내부응력 (eq 22):** per-particle 접촉+bond 응력 → 거시응력.
  - **contact-model 비교**: Hertz+bond vs 탄소성+bond porosity (Fig 6·7) — 탄소성 필요성 증명.
- **도구**: LIGGGHTS(DEM) + 자체 후처리 스크립트. 실험: **나노압입**(TriboIndenter TI 900 Hysitron, 40 입자, 30 nm s⁻¹), **laser diffraction**(Helos Sympatec, PSD), **SEM**(LEO Gemini 1550 Zeiss), **pilot 압연**(GKL 400 Saueressig two-roll, 롤 430 mm, 폭 465 mm, 2 m min⁻¹, 4 갭), 두께(digital gauge ID-C Mitutoyo).
- **수치화·플롯·기록 방식**: C1–C4 4압력 시리즈로 모든 지표를 압밀응력·케이스 함수로. **bond 2 파라미터(S_n, 임계강도)를 C1·C4 보정 / C2·C3 검증**으로 결정 — 나머지는 측정/미세구조 결정. position B(critical, 응력 도달)·C(final, 회복 후)를 구분해 보고.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (2019, LIB 역학) | 우리 (ASSB) | 차이 / 이유 |
|---|---|---|---|
| **연구 범위** | **역학만** (porosity·응력·접촉·방향성·회복). σ 전도도는 2부(2020) | 압밀(DEM·MPM) + **전달 삼중항 σ_i/σ_e/σ_thermal** + grade | **본 1부는 전달 미보유** — 우리가 가진 삼중항이 그들엔 (2019에) 없음 |
| **★ contact law 보정** | **나노압입 40 입자 → YR=8.59×10⁻³·x 직접 측정** | E_eff 1.35(DEM) = real 24의 18× 연화 프록시; MPM J2 σ_y 0.15/0.30 | **그들=단일 입자 실측 anchor / 우리=거시 porosity 앵커(Minnmann)로 연화**. 방법 철학 다름 |
| **★ 소성 종류** | **Thornton–Ning CONTACT 탄소성**(δ 프록시, eq 5 선형 plastic branch) + 항복점 명시 | MPM 진짜 SHAPE 소성(J2) + DEM hooke/hysteresis(**캡 없음**) | **둘 다 입자 형상 안 변함(DEM)**. 그들은 **항복캡 있음**(우리 path-A LAW와 같은 계열); 우리 DEM은 캡 없어 연화. **형상변화 = 우리 MPM 고유** |
| **★ 항복캡 유무** | **있음** (p_y, eq 3·5 — Thornton–Ning) | DEM: **없음**(hooke/hysteresis) → 18× 연화로 보상 | ★ **그들 모델 = 우리 contact_models_layer_map "경로 B(항복캡)"**. 우리가 연화 대신 캡을 넣으려는 그 LAW를 그들은 LIB에 이미 적용 |
| **★ 바인더 bond** | **Sangrós bond**(eq 10–13: 법선·접선 힘+토크, S_n=6e12 N/m³, 파단 2e13 N/m², **영구파단**) | CBD = Stage-2 부피점유; 명시 bond **없음**(backlog A3) | ★ **이게 우리가 binder bond 넣을 때 식의 원전.** eq 10–13 + 파단 = 정확한 템플릿 |
| **압밀 모드** | **calendering**(압연 line-load, plate=롤, B압축→C회복/springback) | **cold-press**(단축 정수압 유지/hold) | LIB 압연 ≠ ASSB 프레싱. **그들은 spring-back 정량(ER 17 %), 우리는 static(회복 미모델)** |
| **압력대** | **~20–160 MPa**(저압 calendering) | **~300–500 MPa**(고압 cold-press) | **압력대 ~2–8× 다름** — Fig 5 P-vs-porosity를 우리 Heckel과 직접 겹치면 안 됨 |
| **porosity floor** | **0.217**(C4 실측) / 시뮬 0.247 @159 MPa | pure-SE ~10 % / real_14 15.6 % @300 MPa | **그들 LIB는 의도적으로 높게 멈춤**(액체전해질이 채움); 압력대도 낮음. 직접 비교 금지 |
| **E_AM** | E_NMC **142 GPa**(고정) | E_CAM **140 GPa**(고정) | **거의 동일**(NMC계). 2020은 SOC 가변 도입 |
| **검증** | **실측 calendering**(porosity·두께 15 % 이내) + **나노압입**(F-d) | solver=ground truth(Minnmann·Cronau·Bazzoun 외부 앵커) | 그들 calendering·나노압입 실측이 LIB 앵커(ASSB 직접 전이 불가) |
| **이온 채널 위상** | (본 1부 미모델 — 2020서 **pore=전도체** Bruggeman) | **SE 입자망=전도체** Kirchhoff/Holm | 2020 대비에서 상술. 본 1부는 역학이라 위상 무관 |
| **소재** | **NMC111 + 액체전해질**(LIB) | **LPSCl SE + NMC811**(ASSB) | **다른 셀 화학** → 절대값 직접 전이 금지 |

### ★★ 핵심 대비 1 — 본 1부(2019)는 **역학 토대 + contact-law anchor**, 우리 우위는 **그 위의 전달 삼중항**
- **2019 = 역학 모델 + 검증만**: porosity·두께·FSA·CN·접촉면적·방향성·응력·회복. **σ 전도도는 안 푼다**(2020). 즉 **본 논문은 우리 frame[5]의 "역학" 절반에 해당하는 부분만**(그것도 형상소성 없는 CONTACT 탄소성). **우리가 가진 전달 삼중항(σ_ionic LOOCV 0.975 / σ_e 0.953 / σ_thermal 0.903, Kirchhoff+Holm+Stage-E)은 본 1부에 전혀 없다.** (2020에서 해석적 균질화로 σ_el·σ_ion 추가하나 명시 Kirchhoff 아님 — 단일 비례상수 fit + fabric tensor.)
- **단 본 논문이 정의한 미세구조 지표(CN·FSA·접촉면적·fabric tensor·viral 응력)는 2020 전도도식의 입력** = 우리 네트워크 솔버 입력(CN, coverage, percolation)과 **같은 종류의 descriptor**. 즉 **본 논문 = "전도도 풀기 전, 미세구조를 정량화하는 법"의 모범**이고, 우리는 거기에 **명시 Kirchhoff/Holm 솔버 + Stage-E 소성면적 + fracture-aware**를 얹어 *더 미시적으로* 푼다.
- **★ contact-law anchor 방법의 대비**: 그들은 **단일 NMC 입자를 나노압입으로 측정**해 항복비 YR을 직접 정한다(Fig 2, R²=0.89). 우리는 **단일 입자 측정 없이 거시 porosity 앵커(Minnmann ~10 %)로 E_eff를 18× 연화**한다. **둘은 상보적** — 그들 방법은 contact stiffness를 *입자 실험*에서, 우리는 *bed 거시거동*에서 잡는다. 만약 우리가 LPSCl SE 단일 입자 나노압입 데이터를 얻는다면 **그들 YR 방법이 우리 σ_y/p_y를 *직접* anchor 하는 템플릿**(현재 우리 σ_y 0.05–0.30은 lit range).

### ★★ 핵심 대비 2 — 항복캡: 그들은 LIB에 이미 적용, 우리는 path-A 백로그
- **그들 Thornton–Ning(eq 3·5)은 항복압 p_y 캡이 있는 LAW** = 우리 `contact_models_layer_map.md` 의 **"경로 B(항복캡)" = path-A LAW** 그 자체. 우리 DEM(Luding hooke/hysteresis)은 **캡이 없어서 E를 18× 연화**한다. **본 논문은 그 캡을 LIB calendering에 이미 실증**했고(Fig 6·7: 탄소성[캡 有]이 Hertz[캡 無]보다 porosity 정확), **Varkey 2026이 같은 LAW를 halide ASSB로** 가져갔다.
- **→ 우리 path-A(real E_SE=24 + 항복캡 → 18× 연화 제거 시험)의 직접 선례**: So 2021(H-cap, LPS 0.98)·Varkey 2026(Thornton–Ning + multi-contact)에 **본 논문(Thornton–Ning + bond, LIB)** 을 추가. **본 논문의 eq 1–6(탄성 Hertz → 항복 p_y → 선형 plastic branch → 잔류겹침 제하)** 이 우리 path-A LAW 구현 스펙의 **완전한 식 출처**(2020은 식 생략, 본 논문에 있음). ⚠ 단 그들 p_y는 NMC(stiff 142 GPa, brittle)용 — LPSCl σ_y(0.05–0.30 GPa)는 훨씬 무름 → p_y 차수 다름.

### ★★ 핵심 대비 3 — spring-back(점탄성 회복) = 우리가 못 다루는 축
- **본 논문 고유 결과 = ER 10.25→17 %** (eq 14, posB→posC). **실험으로는 롤 사이 입자 위치를 µm로 못 봐서 측정 불가** → 시뮬만이 줄 수 있는 정보(저자 강조).
- **우리는 spring-back을 안 다룬다**: DEM·MPM 모두 **압밀 후 정적(hold/displacement-stop)** 으로 멈추고 **압력 해제 후 탄성회복을 모델링하지 않는다**. 우리 Heckel·porosity는 **압밀 시점(position B 대응)** 값이지 **회복 후(position C)** 가 아니다.
- **→ 우리에게**: 만약 실제 ASSB 펠릿의 **제조 후 탄성 spring-back**(특히 stiff LPSCl + 고압)을 정량하려면, **본 논문의 ER 정의(eq 14) + posB→posC 2단계 프로토콜**이 청사진. 우리 MPM은 이미 von Mises J2라 **탄성-소성 분해(F=F_E·F_P)** 가 내장 → **압력 해제 단계(unload)를 추가하면 spring-back을 줄 수 있다**(현재 안 함). ⚠ 단 LIB calendering(저압·압연)의 ER이 ASSB cold-press(고압·단축)에 그대로 안 옴 — 압력대·소재·모드 다름.

### ★ 핵심 대비 4 — fabric tensor 방향성 + 내부응력
- **방향성(Fig 12)**: 압밀이 **F'_zz를 양→음**으로 바꿈(C1 +0.047 → C3·C4 음) = z방향(압밀방향) 접촉이 상실되고 in-plane 접촉이 우세 → **이방성 발달**. 우리 σ 스케일링은 등방 가정이 많은데, **graded-z/층상(Phase-5)** 으로 가면 방향성 항이 필요할 수 있다 — 본 논문이 그 선례(2020도 동일).
- **내부응력(Fig 13)**: 압밀↑ → 내부응력↑(C4 ~220 MPa), 그리고 σ_zz/σ_xx가 C1 ~2.0 → C4 ~1.08(고압서 등방화). 우리 MPM 응력장과 대응. **단 viral 응력에 bond항 포함은 Fig 12 이방성을 완전 반영 못 함**(저자 인정: bond는 z방향에 불리하지 않음 — 전 두께·xy 주기경계라).

### frame[5] 위치
- **이 논문 = 전달/패킹 측의 *역학 부분만*** (rigid 구 + 항복캡 CONTACT 탄소성 + bond → porosity·응력·방향성). **입자 형상소성·void-fill 없음** — 우리 MPM이 메우는 그 절반이 빠져 있다(Varkey·2020·Ngandjong과 동일 한계, 같은/유사 그룹). **게다가 본 1부는 전달 σ도 아직 없음**(2020서 추가) → frame[5]의 "DEM=전달" 중 **σ 솔버 부분도 본 1부엔 미완**.
- **우리 우위 = (i) 전달 삼중항 명시 솔버, (ii) MPM 형상소성** 둘 다 본 논문에 없음.

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **contact-law anchor 방법 — 단일 입자 나노압입(YR=8.59×10⁻³·x)**: 우리 σ_y/p_y(현재 lit range 0.05–0.30)를 **거시 앵커(Minnmann)가 아니라 단일 입자 실측으로 직접** anchor 하는 템플릿. **LPSCl SE 단일 입자 나노압입 F-d**가 있으면 본 논문 방법(Fig 1·2: Hertz fit → 항복점 → YR 선형회귀)으로 우리 contact stiffness를 *입자 레벨*에서 정할 수 있다 — 현재 우리 18× 연화의 *입자-실험 보강*.
- ② **path-A LAW 식 원전 확보(backlog)**: 우리 "real E_SE=24 + 항복캡 → 연화 제거" 시험의 LAW = **본 논문 eq 1–6(Hertz→p_y→선형 plastic→잔류겹침)**. 2020이 생략한 식이 여기 완전히 있음. So 2021·Varkey 2026과 묶어 **Thornton–Ning + bond 를 LPSCl로 이식**.
- ③ **explicit binder bond 템플릿(backlog A3/D5)**: eq 10–13(법선·접선 힘+토크) + 면적당 강성 S_n=6e12 N/m³ + 임계강도 2e13 N/m² + **영구파단**. 우리 CBD(PTFE/VGCF)를 부피점유→명시 bond로 올릴 때 청사진. **재형성 여부**는 Ngandjong(SJKR 재형성) vs **본 논문(영구파단)** 중 선택 — PTFE cold-weld(`--coh`)는 재형성 쪽에 가까울 수도(섬유 재접촉).
- ④ **spring-back 경로(우리 미보유 축)**: ER=(h_C−h_B)/h_A (eq 14) + posB→posC 2단계. 우리 MPM(J2, 탄성-소성 분해 내장)에 **unload 단계 추가**로 spring-back 정량 가능 — 현재 hold/static에서 못 줌.
- ⑤ **방향성(fabric tensor) 근거**: Phase-5 graded-z/층상으로 갈 때 transport에 방향성 항을 넣을 선례(Fig 12: 압밀로 z→음 이방성).
- ⑥ **데이터**: `docs/data/sangros2019_calendering.csv` — Table 1(porosity·두께·밀도·응력, stated) + ER·CN·broken bonds·fabric tensor·내부응력(Fig 8/10/12/13, digitized) + contact·bond 파라미터(stated). **단 LIB·저압·NMC라 절대값 ASSB 전이 금지, 추세·방법·식 대조용**.

## ★ 9. 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this DEM model)
> **결론 먼저: 본 논문(Sangrós 2019)은 calendering-DEM 역학 모델의 *기초이자 검증된 고전*이지만, 전달·형상소성·해석압축 측면에서 우리가 명백히 SOTA를 앞선다.** 본 논문은 **순수 역학 1부**(전도도조차 2020에 미룸)이고, 입자는 **형상불변 강체 구 + CONTACT 탄소성**이며, **LIB(NMC+액체전해질)** 다. 우리 7개 차별점을 그들이 *하는 것/없는 것*에 매핑한다. 모두 **증거 기반**(그들 구-형상·LIB-범위·전달-부재를 근거로).

**(1) 전달 삼중항 σ_ionic + σ_e + σ_thermal — 명시 Kirchhoff/Holm 접촉망 솔버 (★ 가장 강한 우위)**
- **그들(2019)**: 전도도를 **전혀 풀지 않는다.** porosity·응력·접촉·방향성·회복까지만. (2020에서 σ_el[eq1 fabric 균질화]·σ_ion[eq2–4 Bruggeman]·접착[eq5]을 추가하나 — **단일 비례상수 fit + fabric tensor 균질화**이지 *명시 Kirchhoff Σ(φi−φj)/R=0 + Holm 구속저항* 솔버가 아니다.)
- **우리**: **3채널 모두**(σ_ionic LOOCV 0.975 / σ_e 0.953 / σ_thermal 0.903), **명시 접촉 네트워크 Kirchhoff 솔버 + Holm R=1/(2σr_c) 구속저항**. 본 1부는 σ 0채널, 2020도 σ_thermal 없음(σ_el·σ_ion만). **삼중항·명시망·구속저항 = 명백한 우리 SOTA.**

**(2) Stage-E 소성 접촉면적 재유도**
- **그들**: 접촉면적은 **Hertz/탄소성 기하 면적**(eq 2의 a, eq 15의 ΣA_c,i). 소성 pile-up·Tabor 면적 재유도 없음.
- **우리**: **Stage-E(Tabor + volume 소성 접촉면적)** 로 elastic-Hertz 면적을 **소성 면적으로 재유도** → σ의 구속저항 입력 보정. 그들 균질화(2020)는 elastic 면적 기반이라 고-CAM서 과소(2020서 자인) → **우리 Stage-E가 그 보정 방향.**

**(3) DEM↔MPM scaffold 커플링 + 진짜 소성 MORPHOLOGY (J2)**
- **그들**: 입자는 **영원한 강체 구**(δ=기하 프록시). **형상변화·void-fill flow 없음.** 본문조차 고압(C4)서 "균열·파쇄·PVDF reform을 고려해야 정확"이라 *한계로 인정* — 즉 **형상 거동을 못 잡음을 자인**.
- **우리**: **MPM 진짜 J2 소성 형상변화**(SEM 코어보존+경계평탄화 ✓), **부피보존 void-fill flow**, **DEM AM 골격 + SE만 MPM(scaffold)** 커플링. 그들이 자인한 "형상·void 거동 부재"를 우리 MPM이 정확히 메움(frame[5]). **형상소성 = 우리 고유.**

**(4) fracture-aware transport (Auerbach + Lawn)**
- **그들(2019)**: 입자 파쇄 **미모델**(bond 파단만; 입자는 안 깨짐). 본문이 "고압서 입자 파쇄 고려 필요"라 *한계로만*.
- **우리**: **Auerbach 임계 + Lawn 미세균열** → **fracture-aware Holm**(f_intact로 σ 부분전도 보정). 깨진 접촉도 ~60 % 미세접촉 유지를 σ에 반영. **그들 bond 파단(역학)과 달리 우리는 파쇄를 *전달*에 연결.**

**(5) 문헌-근거 σ_grain (Cronau)**
- **그들(2020)**: 이온 σ는 **k_ion^bulk=0.01 S/cm**(액체전해질) 단일값 + Bruggeman. SE 입계·crystallinity 인자 없음(액체라 무관).
- **우리**: **σ_grain=3.0 mS/cm × Cronau(r_SE)** — 단결정 문헌값 + sub-µm amorphization 인자(입계 의존). ASSB SE 고유 — 그들 LIB에 해당 없음(다른 전도체).

**(6) 실험-앵커 독립 듀얼모델 frame[4]/[5]**
- **그들**: **단일 DEM 모델**(나노압입·calendering 실측 보정). 독립 2모델 교차검증 없음.
- **우리**: **DEM(전달) + MPM(역학)** 을 *각각 독립적으로 실험에 보정*(Minnmann·Cronau·Bazzoun) — **서로 cross-fit 안 함**(frame[4]). 수렴=교차검증, 발산=정량화된 모델한계. **본 논문은 단일 모델이라 이 메타-검증 구조가 없음.**

**(7) 솔버→스케일링 법칙 LOOCV 압축**
- **그들**: 미세구조 지표 → 물성을 **단일 비례상수**(C_el/C_ion/C_ad, 2020)로 닫음. ML/LOOCV 압축 없음.
- **우리**: 네트워크 솔버 출력 → **스케일링 법칙(LOOCV 0.90–0.98) + grade_engine** 으로 압축, 외부 검증. **그들 비례상수 fit ≪ 우리 LOOCV-검증 폼.**

**⚖️ 정직하게 — 그들이 우리보다 앞선 곳:**
- **① 단일 입자 나노압입으로 contact law 직접 anchor (YR=8.59×10⁻³·x, R²=0.89)**: 우리는 단일 입자 측정 없이 거시 앵커로 연화한다. **그들의 입자-레벨 실측 보정이 더 직접적**(우리가 LPSCl 나노압입을 얻으면 따라야 할 방법).
- **② 측정된 점탄성 spring-back(ER 10.25→17 %)**: 우리는 spring-back을 *안 다룬다*. **그들이 정량화한 이 축은 우리 미보유**(MPM unload로 추가 가능하나 현재 없음).
- **③ 명시적 binder bond 역학(eq 10–13, 파단)**: 우리 CBD는 부피점유뿐. **그들 bond 역학이 더 완성**(우리 backlog A3가 따라갈 식).
- **④ calendering·나노압입 *역학* 실측 검증의 완성도**: 본 논문은 porosity·두께를 15 % 이내로, F-d를 직접 맞춤. 우리 압밀 검증은 Minnmann porosity 단일 앵커가 주.
- ⚠ **단 ①②③④ 모두 LIB·저압·NMC·역학 범위 / 형상불변 구** — **전달 삼중항·형상소성·해석압축에서 우리가 SOTA**라는 결론은 유지. 그들 우위는 *역학 모델링의 깊이·실측 보정*, 우리 우위는 *전달·형상·다중모델·압축*.

## 10. 인용 가능 문장 (deck/paper용)
- "Sangrós Giménez et al. (2019) established the **mechanical foundation** of calendering DEM for Li-ion cathodes — a **Thornton–Ning elasto-plastic contact** for single NMC particles (its yield ratio YR = 8.59×10⁻³·x **measured directly by nanoindentation of 40 particles**, R²=0.89) combined with an **explicit particle–particle bond** for the additive-binder matrix (normal/tangential forces + torques, eqs 10–13; permanent breakage at 2×10¹³ N m⁻²) — and validated electrode porosity, thickness, free surface area, NMC–NMC contact area, coordination number, broken-bond count, contact directionality (fabric tensor) and internal stress against real pilot-scale calendering. This is the **predecessor (Part I, mechanics)** of their 2020 conductivity paper."
- "Their model uniquely quantified the **viscoelastic spring-back** of the electrode — a relative elastic recovery of **10.25 % up to almost 17 %** that **cannot be measured experimentally** because the particle positions between the calender rolls are inaccessible at micrometre resolution."
- "Crucially, Part I (2019) is **mechanics-only** — it solves **no conductivity**. Our work supplies the missing transport side: a **three-channel (σ_ionic/σ_e/σ_thermal) explicit Kirchhoff/Holm contact-network solver** with **Stage-E plastic contact areas** and **fracture-aware conduction**, plus **true plastic particle-shape morphology via MPM** — none of which the rigid-sphere, contact-plasticity-only LIB model provides."
- "The Thornton–Ning contact (eqs 1–6: elastic Hertz → yield p_y → linear plastic branch → residual-overlap unloading) is the **full equation source** for a **yield-capped DEM law** (their 2020 paper omits it) — the LIB precedent for our path-A test of removing the 18× softening with a real E_SE = 24 GPa plus a yield cap (cf. So 2021, Varkey 2026)."

## 11. 주의/한계 (over-claim 방지)
- **본 1부는 역학만 — 전도도 0채널**: σ_el·σ_ion은 2020(2부). 본 논문에서 "전달"을 끌어오지 말 것(미세구조 지표만 제공). 우리 삼중항 우위 비교는 *그들이 σ를 안 푼다*는 사실에 근거.
- **LIB (액체전해질)** — 2020에서 이온 채널이 **공극(Bruggeman)** 으로 드러남. 본 1부는 역학이라 이온위상 무관하나, σ·이온 절대값을 우리 ASSB(SE-network)로 전이 **금지**(다른 전도체).
- **강체 구 + CONTACT 탄소성** — 입자 형상 안 변함(δ=기하 프록시). **입자 파쇄 미모델**(bond 파단만; 본문이 고압서 파쇄 고려를 *한계로* 언급). **형상소성·void-fill 없음** → 우리 MPM 영역과 별개(frame[5]).
- **calendering(압연, 저압 ~20–160 MPa) ≠ ASSB cold-press(단축 고압 ~300–500 MPa)** — 압력대 ~2–8× + 압밀모드(압연 line-load+springback vs 단축 hold) 달라 **Fig 5/7 P-vs-porosity 곡선을 우리 Heckel과 직접 겹치면 안 됨**(knee·floor 형태만 정성 대응).
- **porosity 절대값(0.217–0.522)은 LIB·NMC111·저압 압연** — 우리 LPSCl(10–15.6 %)과 직접 비교 금지. 그들은 **의도적으로 높게 멈춤**(액체전해질 충전).
- **bond 강성·임계강도(6e12·2e13)는 calendered NMC cathode 보정값** — LPSCl PTFE/VGCF로 직접 전이 불가(소재·바인더 다름). 식(eq 10–13) 형태만 템플릿.
- **YR=8.59×10⁻³·x 는 NMC111 단일 입자** — LPSCl SE 항복(σ_y 0.05–0.30 GPa, 훨씬 무름)에 그대로 안 옴. *방법*(나노압입→YR 선형회귀)만 전이.
- **viral 응력에 bond 방향성 미반영** — Fig 12 이방성이 bond항으로 완전 포착 안 됨(저자 인정). 우리 응력장 비교 시 주의.
- **Fig 5/6/7/8/9/10/11/12/13 의 일부 값은 디지타이즈**(그래프에서 읽음) → **추세만(±)**. **stated**: Table 1(porosity·두께·밀도·응력), Table 2(E·ν·COR·ρ·PSD·YR), bond 파라미터(6e12·2e13), CN_C1=1.55·CN_C4=2.19(posB), ER 10.25→17 %(Conclusion), A_CC,p ~56/61/62/65 %, 초기 bonds/입자 3.44, 입자 수 2237, timestep 1e-10 s.
- **2019 vs 2020 porosity 미세 차**: C1–C4 = 0.416/0.372/0.295/0.217(2019) vs 0.417/0.368/0.305/0.270(2020) — 같은 실측 시리즈의 *다른 보정/재현*. 한 값으로 합치지 말 것(각 논문 stated 별도).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

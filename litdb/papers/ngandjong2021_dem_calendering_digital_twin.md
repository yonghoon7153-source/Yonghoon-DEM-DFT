<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목 -->
# LIB 전극 calendering(압연)을 DEM으로 — AM + carbon-binder domain 명시 + 슬러리→건조→압연→전기화학 "디지털 트윈" 파이프라인 — Ngandjong (J. Power Sources 2021)

> slug `ngandjong2021_dem_calendering_digital_twin` · DOI `10.1016/j.jpowsour.2020.229320` · type `DEM (+ CGMD 슬러리/건조 + FEM 전기화학; exp 검증)` · PDF `Ngandjong_2021_JPowerSources_ElectrodeCalendering_DEM_DigitalTwin.pdf` · digested `2026-06-26` · status ✅

---

## 1. 한 줄 요약
**Franco 그룹(LRCS Amiens / ARTISTIC ERC)의 "Li-ion 제조 디지털 트윈" 플래그십** — **슬러리(CGMD) → 건조(CGMD) → calendering(압연, 본 논문 신규 DEM 모델) → 전기화학(FEM)** 의 순차 멀티스케일 파이프라인 중 **압연 단계를 새 DEM 모델로 채우고 실측(micro-indentation 곡선 + porosity-vs-압력)으로 검증**한 논문. NMC(활물질, AM) + **carbon-binder domain(CBD)을 명시적 별도 입자상**으로 다루며, CBD는 **GH(Granular-Hertz, 탄소성) + SJKR(점착 bond, 끊어졌다 재형성)** 으로 끈끈한 변형상으로 모델링. 압연압력 → porosity → PSD·tortuosity·입자배열(g(r)) → discharge·EIS까지 연결. **우리와 같은 "제조→성능" 철학이되 LIB(액체전해질, porosity = GOOD)** 이라 이온 채널 위상이 우리 ASSB(porosity = BAD)와 정반대.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/binder/전해질) | 연구유형 |
|---|---|---|---|---|
| **Alain C. Ngandjong, Teo Lombardo** (공동 1저자), Emiliano N. Primo, Mehdi Chouchane, Abbos Shodiev, Oier Arcelus, **Alejandro A. Franco**(교신) — LRCS / RS2E / ALISTORE-ERI / IUF, Amiens | **Journal of Power Sources 485, 229320 (2021)** (접수 2020-07-29, 게재 2020-12-22, open access CC BY-NC-ND) | 10.1016/j.jpowsour.2020.229320 | **NMC** LiNi₀.₃₃Mn₀.₃₃Co₀.₃₃O₂ (NMC111, Umicore) 96 wt% + **carbon black(C-NERGY super C65, Imerys) 2 wt% + PVdF(Solef 5130/1000, Solvay) 2 wt%** = CBD; **액체전해질**(공극에 채워짐, FEM 단계). 용매 NMP(NMP→BASF) | **DEM**(LIGGGHTS, 신규 calendering 모델) + **CGMD**(LAMMPS, 슬러리/건조) + **FEM**(COMSOL, 4D-resolved 전기화학) + 실험 검증(micro-indentation, Hg porosimetry, discharge, EIS) |

> ★ **ARTISTIC 프로젝트(EU H2020 ERC #772873)의 핵심 산출물**. 본 논문은 그룹의 **calendering 단계를 처음으로 명시 DEM으로 채운** 것이며(이전엔 슬러리·건조 CGMD + 전기화학 FEM만 있었음), 코드는 ARTISTIC 포털 + GitHub `ARTISTIC-ERC/Manufacturing-Model-Codes`에 공개. 우리 wishlist Tier-5(application context). **같은 그룹 라인업과의 관계**: 본 논문 ref [18]=Lombardo 슬러리 force-field 보정(우리 CGMD 입력의 출처), ref [20–24]=Chouchane/Shodiev/Rucci 4D FEM(전기화학 솔버), ref [39–42]=Sangrós Giménez(`papers/sangros2020_*`, TU-Braunschweig — calendering DEM의 **선행 연구**로 인용), ref [19]=Srivastava DEM(점착·응집 force). 즉 **Sangrós(TU-BS, 2019–2020) ↔ Ngandjong(LRCS, 2021)** 가 calendering-DEM의 두 독립 계보이고, Varkey 2026(`papers/varkey2026_*`)은 Sangrós bond를 halide ASSB로 가져간 후속.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **un-calendered porosity** | **42 ± 2 %** (exp) / **41.6 %** (sim) | 건조 직후(압연 전), 96:2:2 | stated(Table 1) | ρ_dry exp 2.3±0.1, sim 2.4 g/cm³ |
| **calendered porosity vs 압력** | **41.6 → ~31.5 → ~30.7 → ~27.8 → 27.2 %** | 압연압력 ~0→~7→~35→~85→~160 MPa (Fig 2B/5) | digitized(Fig 2B/5) | sim·exp 거의 일치; ~85 MPa 이후 포화(~27 %) |
| **porosity 급강하 knee** | **~5–10 MPa**서 42→~32 %로 급강하, 이후 완만 | Fig 2B | digitized | LIB 전극 압연의 elastic→plastic knee (저압) |
| **porosity 대표 3점(구조분석용)** | **41.6 % (Uncal) / 31.5 % / 27.2 %** | 본문 Fig 3–8의 3 조건 | stated | (S4에는 31.8 / 26.9 % 표기 — PorosityPlus가 2 % 입자팽창 미반영해 약간 다름) |
| **tortuosity τ (z, 압연방향)** | **~1.55 → ~1.95** (CBD inner-porosity 47 % 가정) | Uncal → ~160 MPa, z방향 | digitized(Fig 5) | x·y·z 모두 증가(이방성 작음); EIS-유도 τ는 아래 |
| **τ_EIS (TLM)** | **1.3676 / 1.3808 / 1.7527** | Uncal 41.6 % / 31.5 % / 27.2 % | stated(Table 3) | Landesfeind TLM, R_ion×3 그래프법 |
| **R_ion (전해질 이온저항)** | **0.02595 / 0.02913 / 0.04014 Ω m²** | Uncal / 31.5 % / 27.2 % | stated(Table 3) | calendering↑ → R_ion↑(공극↓→이온경로 악화) |
| **discharge 비용량 @1C** | **116.2 / 121.5 / 130.7 mAh/g** | Uncal 41.6 % / 31.5 % / 27.2 % (sim) | stated | **압연할수록 용량↑** (전자전도 개선이 지배) |
| **un-cal 전위 급락** | discharge 후반 **~70 mAh/g**서 전위 급락(sim) | un-calendered, 1C | stated | 빈약한 전자전도 → 후반 polarization |
| **NMC 단입자 E (DEM 입력)** | **200 GPa** (lit 100–200 중 상한 선택) | NMC 소재 | stated(Table 2) | E_NMC=200, CBD E=2 GPa(아래) |
| **CBD E (DEM 입력)** | **2 GPa** | CBD 입자 | stated(Table 2) | AM의 1/100 → CBD가 "끈끈한 변형상" |
| **CED (점착에너지밀도, SJKR)** | AM **6×10⁵** / CBD **7×10⁴** / Al **5.5×10⁵** / Steel **6×10⁵** pg µm⁻¹ µs⁻² | DEM bond(접착) | stated(Table 2) | 혼합 i-j는 기하평균; CBD가 가장 약함(끈끈하나 부드러움) |
| **마찰 X_u (DEM)** | AM **0.001** / CBD **0.001** / Al **1.2** / Steel **0.76** | DEM | stated(Table 2) | 입자간 거의 마찰無, wall(Al/Steel)은 높음 |
| **ν (DEM)** | 0.3 (AM·CBD·Al·Steel 전부) | DEM | stated(Table 2) | |
| **CBD 밀도/나노porosity** | ρ_CBD,solid **1.81 g/cm³** (CB+PVdF 평균), 압축 CBD 입자 ρ **0.95 g/cm³** | CBD 소재 | stated | → CBD **inner-porosity ≈ 47 %** (FIB-SEM, ref [45]) |
| **CBD 유효 확산계수(FEM)** | **2.46×10⁻¹¹ m²/s** (vs pore 7.5×10⁻¹¹) | FEM 전기화학 | stated | CBD를 부분침투(이온 통과·삽입無)로 처리 |
| **NMC 전자전도도(FEM 입력)** | **5×10⁻³ S/m** (실측 대비 낮춤, 수렴 위해) | FEM | stated | 본문이 "실험보다 낮춰 fast convergence"라 명시 |
| **Li 고체확산 D_Li(FEM)** | **2×10⁻¹⁵ m²/s** | NMC | stated | |
| **PSD (NMC, 6 binned 직경)** | **2.5 / 3.5 / 4.5 / 5.86 / 8.28 / 10.35 µm** (SEM 측정 → 6 bin) | 실측 NMC | stated(Fig S1) | CGMD에 이 6 직경 사용 |
| **CBD 입자 직경** | 슬러리 **3.1 µm**(용매포함) → 건조 **0.65 µm**(용매증발로 수축) | 모델 | stated(Fig 1) | "용매=CBD 부피팽창" 트릭 |
| **입자 수** | AM **396** + CBD **9463** (계산 셀); indentation/calendering용 ~160,000(×4 복제) | 시뮬 | stated | 슬러리 ~5 h, 건조 ~33 h(2 proc×14 core) |

## 4. 시뮬레이션 방법 ★
- **code / version**:
  - **DEM(calendering)** = **LIGGGHTS** (오픈소스), NVE 앙상블, 압력은 **이동 plate(=압연 롤 모사)** 속도로 제어. timestep 1e-5 µs, 압축단계 timestep 수 13e7~20e7(압축도 의존), plate 속도 **2×10⁻³ µm/µs**.
  - **CGMD(슬러리·건조)** = **LAMMPS**, NPT(298 K, 1 atm), 주기경계 x·y·z. 슬러리→건조는 **CBD 입자를 수축**(LJ+GH force-field 파라미터 변경)시켜 용매증발 모사.
  - **FEM(전기화학)** = **COMSOL Multiphysics** (Batteries & Fuel Cells + Transport of Diluted species), 4D-resolved 모델(이전 논문 ref [21] 동일), INNOV 자체 voxelization(0.25 µm voxel)으로 메시 생성.
  - 후처리: **PorosityPlus**(porosity·PSD, CSIRO), **PorosityPlus + Dong/Torayev 알고리즘**(구·실린더 PSD), **GeoDict**(tortuosity, MacMullin), **DiffuDict**(확산 시뮬), **PorosityPlus** g(r).
- **DEM 접촉법칙** ★ (calendering의 핵심 — **두 force-field의 조합**):
  - **GH = Granular-Hertz, eq (1)**: `F_GH = √δ · √(R_iR_j/(R_i+R_j)) · [(k_n·δ·n_ij − m_eff·γ_n·v_n) − (k_t·Δs_t + m_eff·γ_t·v_t)]` — **탄소성/점탄성 접촉**(법선 탄성 k_n + 점성감쇠 γ_n + 접선 k_t·Δs_t). δ=겹침, R=반경. **GH가 0이 아니려면 일정 겹침 필요** → AM 입자 직경을 **2 % 살짝 키워**(slight 2 % expansion) 항상 접촉이 잡히게 함. **k_n↔E(Young), 감쇠↔COR, k_t/k_n·γ_t/γ_n↔ν(Poisson), 마찰비↔X_u**로 매핑(법선·접선 GH 힘의 최대비).
  - **SJKR = 단순화 Johnson-Kendall-Roberts, eq (2)**: `F_SJKR = CED × A` — **점착(adhesive) 힘** = **바인더 "bridge"**의 대리물. CED=점착에너지밀도, A=두 접촉체 사이 접촉면적. **"두 물체가 접촉할 때마다" SJKR 계산; calendering으로 두 물체를 떼어내는 힘이 F_SJKR보다 크면 → 분리(bond 끊김)**. **다시 접촉하면 F_SJKR 재계산(=bond 재형성)**. 즉 **끊어졌다 재형성되는 점착 bond**.
  - **합성**: "역학적 거동은 GH와 SJKR의 복잡한 상호작용에서 나온다"(본문). **CBD CED가 높으면(끈끈) AM의 입자겹침이 지배할 수도 있어 E와 부분 상쇄** → 둘을 함께 보정해야 함(본문이 명시).
- **재료 파라미터(Table 2, DEM)**: E_AM=**200 GPa**(NMC, lit 100–200 상한), E_CBD=**2 GPa**, E_Al=69, E_Steel=200; ν=0.3 전부; X_u(마찰) AM/CBD=0.001, Al=1.2, Steel=0.76; CED AM 6×10⁵ / CBD 7×10⁴ / Al 5.5×10⁵ / Steel 6×10⁵ pg µm⁻¹ µs⁻². **혼합 i-j(예: AM-CBD)는 각 물성의 기하평균**. **AM·CBD 형상(σ)·밀도는 건조전극 CGMD 값 그대로 유지**.
- **CGMD force-field(Table S1/S2)**: LJ(ε, σ, r_c) + GH(k_n, γ_n, ν, X_u). 슬러리: k_n=8, γ_n=30, ν=0.15, X_u=0.015, CBD d=6.2 µm(용매포함), ρ_CBD=0.002. 건조: ε를 **3000×(AM)/3500×(CBD)** 로 키워(=고체화로 강성↑) k_n=500, γ_n=10, ν=0.3, X_u=15, CBD d=1.3 µm, ρ_CBD=0.95. **슬러리는 Lombardo ref [18]이 shear-viscosity η-γ + 슬러리밀도로 검증**(Fig S2: η 3.3→1.0 Pa·s, ρ sim=exp=2.14 g/cm³).
- **bond/binder 모델** ★★ (**CBD = 명시 입자상 + GH+SJKR**):
  - **CBD를 "별도 입자상"으로 명시 모델링**(Sangrós·우리와 같은 철학). CBD 입자 = **carbon black + PVdF 응집체**(단일 입자가 CB+바인더 덩어리 대표), **내부 나노porosity ≈ 47 %**(FIB-SEM). 따라서 ρ_CBD,solid=1.81(CB+PVdF 평균)이 아니라 **압축 CBD 입자는 0.95 g/cm³**로 잡음(나노포어 반영). CBD 입자 수는 이 밀도로부터 계산(9463개).
  - **CBD의 끈끈함 = SJKR 점착**(CED) + **부드러움 = 낮은 E(2 GPa)**. AM-AM·AM-CBD·CBD-CBD 각각 GH+SJKR이 작동, 혼합은 기하평균.
  - **bond 끊김/재형성**: SJKR로 묶인 두 입자를 calendering이 떼면 분리, 재접촉시 재형성 — **Sangrós의 "임계응력 영구파단"과 달리 Ngandjong은 reversible 재형성**(차이점).
- **MPM/continuum**: **없음**. (압밀역학은 DEM이, 전기화학은 FEM continuum이 담당. 입자 **형상소성(SHAPE flow)·void-fill은 없음** — GH는 CONTACT 레벨.)
- **전달 솔버** ★ (이온/전자는 **FEM continuum**, RNM/Kirchhoff 아님):
  - **전기화학 = COMSOL FEM 4D-resolved**(이전 ref [20–24]). 이온은 **전해질(공극)** 통한 확산(Bruggeman inner-porosity 보정), CBD는 **부분침투상**(이온 통과 허용, 삽입無, D_eff=2.46×10⁻¹¹). 전자는 NMC 통해(σ=5×10⁻³ S/m, 수렴위해 낮춤).
  - **tortuosity**: GeoDict로 Fick 1법칙 풀어 MacMullin → τ(x,y,z). Bruggeman 유효확산 D_eff = D_bulk·ε^1.5(CBD inner-porosity 47 % 반영).
  - **EIS = COMSOL**, 7 freq/decade(1–10⁷ Hz, 10 mV). **Landesfeind TLM**으로 R_ion·τ_EIS 추출(고-중주파 기울기×3).
  - **⚠ 우리와 다른 점**: 이온 전도체가 **공극(pore)** 이라 **Bruggeman porosity·tortuosity**가 핵심(SE-network Kirchhoff/Holm 아님). 전자도 NMC-continuum FEM(우리 AM-network Kirchhoff와 대응되나 방법은 continuum).
- **입자 처리** ★ (DEM판 "무질서 처리"): **구만**(AM=6 직경 다분산 강체 구, CBD=단일 0.65 µm 구). **rigid 입자 + GH CONTACT 탄소성/점탄성(δ 프록시) + SJKR 점착 bond** — 입자 **형상은 안 변함**. **2 % 입자팽창**(GH 비영 조건) + **CBD가 부드러운 변형상(E 2 GPa)** 으로 압밀 흡수. **초기구조 = 슬러리 PSD로 랜덤 비중첩 배치**(200×200×1200 µm 박스). **stochastic 생성이 아니라 검증된 슬러리/건조 CGMD 구조에서 출발**(본 논문 novelty 중 하나 — "un-calendered mesostructure from validated slurry+drying").
- **도메인/RVE / servo / seeds / 압력범위**:
  - 슬러리 셀 **200 × 200 × 1200 µm**(중첩방지 큰 박스). calendering/indentation용은 ×4 복제(x·y) → 표면적 **~11,569 µm²**(~160,000 입자)가 size-수렴 최적(S3: 723→2892→11569 µm²서 indentation 곡선 평활화).
  - **calendering 2단계**(Fig 1): 위 plate가 **목표 최대압력**까지 하강(압축) → plate를 **초기위치로 복귀**(완화/springback). 바닥 plate = **집전체(current collector)**. **압력경계는 z만(비주기), x·y는 주기**.
  - **micro-indentation 모사**(검증용): 건조전극을 두께 10 %까지 압입 후 원위치 복귀(Vickers diamond 실측 대응). 실측 접촉면적 ~31,000 µm²/변위 ~18 µm vs sim ~11,600 µm²/~16 µm → 둘 다 F/F_max·d/d_max로 정규화 비교(Fig 2A).
  - **압력범위**: porosity-vs-P는 **~0–160 MPa**(Fig 2B/5). 구조분석은 41.6/31.5/27.2 % 3조건. 압축속도 효과 무시가능(S6: 2e-3→2e-4 µm/µs서 g(r)·PSD 불변).
- **특이사항/튜닝**:
  (1) **CGMD→DEM→FEM 순차 커플링** — 각 단계 출력이 다음 입력. 본 논문의 **핵심 novelty = 압연 단계를 (검증된 슬러리·건조 구조 위에) 명시 DEM으로 채운 것** + **AM·CBD 두 상 명시** + **micro-indentation·porosity 동시 검증**(처음으로 두 descriptor 동시).
  (2) **건조 모델의 한계 명시**: 건조 CGMD가 z방향도 주기경계라 calendering(z 비주기)과 BC 불일치 → "z 비주기 건조모델 개발 중"이라 솔직히 인정. 이게 sim 용량이 실측보다 체계적으로 낮은 일부 원인.
  (3) **NMC 전자전도도를 실측보다 낮춰**(5×10⁻³ S/m) FEM 수렴 확보 — un-calendered의 진짜 전자전도 한계(고-C-rate 무용량)는 COMSOL 수치한계로 직접 재현 못 한다고 명시.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **GA(그래픽 초록)** | 슬러리→건조→압연(롤)→전기화학 + Nyquist·discharge 모식 "Li-ion Battery Manufacturing" | **제조→성능 디지털 트윈 한 컷** — 우리 DEM→Kirchhoff→grade와 같은 철학 그림 |
| **1** | **계산 워크플로**: 슬러리(CGMD) → 용매증발 → 건조전극(CGMD) → calendering(DEM, 이동 plate) → discharged(FEM). 하단에 CBD(슬러리 3.1/건조 0.65 µm) + AM 6직경(1.25–5.2 µm) 색·반경 범례 | **순차 멀티스케일 파이프라인의 1:1 템플릿**. 우리 frame[5] "한 구조 → 여러 물성" 그림으로 인용 |
| **2A** | **micro-indentation 검증**: 실측(흑, 30회 평균 ±산포 회색) vs sim(적) F/F_max–d/d_max. 로딩·언로딩 히스테리시스 형태 일치 | **DEM 역학 검증 방법**(indentation 곡선 fit) — 우리 Heckel/Cronau 앵커의 LIB판 |
| **2B** | ★ **porosity vs 압연압력**(실측 ■ + sim ●, ±산포). 42→~5–10 MPa서 급강하→~85 MPa 이후 ~27 % 포화 | **압연 P-vs-porosity 곡선**(우리 P-vs-porosity·Heckel과 대조; LIB는 저압서 급강하 후 포화 floor ~27 %) |
| **3A** | **Hg porosimetry PSD**(실측, mass 정규화): Uncal 42 %(~0.7 µm 주피크) → 33 %(적) → 26 %(청). 압밀↑ → 피크 작아지고 왼쪽 이동 | 실측 PSD가 압밀에 어떻게 변하나; **Hg는 Washburn 실린더 가정** |
| **3B** | **sim PSD**(PorosityPlus): Uncal 41.6 % → 31.5 % → 27.2 %. ~3–4 µm 분포. **Hg와 절대값 다름**(방법·근사 차이, 본문이 명시) | sim PSD vs 실측 PSD **방법의존 불일치**를 솔직히 비교 — 우리 porosity convention 논쟁의 LIB판 |
| **4A** | **g(r) CBD-CBD**: 1차 shell ~1.25 µm, 2차 ~2 µm. 압밀↑ → 1차 피크 폭 좁아지고(응집 치밀화), 장거리 질서 상실. 인셋 ~1.2 µm 줌 | **CBD가 AM 사이 공간을 채우며 응집**; 압밀로 CBD 더 치밀 |
| **4B** | **g(r) AM-CBD**: 1.69/2.17/2.67/3.35/4.57/5.63 µm 피크. 압밀↑ → CBD가 각 AM을 덮음(피크↑), AM-CBD 거리 감소(한계까지) | CBD가 AM 표면을 덮는 정도(coverage 유사 개념) |
| **4C** | **g(r) AM-AM**: 2.55–9.51 µm 다수 피크(S5 Table S3에 AM쌍 조합 귀속). 압밀↑ → 국소질서↑(피크 약간 우측=AM 반경합보다 큼 → CBD가 끼어있음) | **AM-AM 거리분포로 패킹질서** — 우리 g(r)/CN 분석 대응 |
| **5** | ★ **tortuosity τ(x,y,z) vs 압연압력**(CBD inner-porosity 47 % 가정). Uncal~1.55 → ~160 MPa~1.95. **x·y·z 거의 동일 증가**(이방성 작음). 점선=해당 porosity | **압밀↑ → τ↑**(공극경로 악화). 이방성 작음 = "calendering이 전 방향 transport에 영향" |
| **6A** | **Nyquist(EIS, symmetric cell)**: 고주파 intercept(전자+분리막저항)가 압밀↑에 **좌이동**(전자저항↓), 중주파 기울기 길이↑(이온저항↑) | EIS로 전자↓·이온↑ 동시 읽기 |
| **6B** | **전극 단면 임피던스 2D map**(상=이온 기여 @100 Hz, 하=NMC/CBD/Pore 분포). un-cal은 이온저항 hot-spot 많음 | 공간분해 저항맵 — 우리 4D 솔버 시각화 대응 |
| **7A** | **메시 half-cell 3D**(압연압력 좌→우 증가, 빨강 NMC·노랑 CBD·초록 분리막·보라 Li) | FEM 셀 셋업 |
| **7B** | ★ **discharge 곡선 @1C**(sim): Uncal 116.2 < 31.5 % 121.5 < 27.2 % 130.7 mAh/g. **un-cal은 ~70 mAh/g서 전위 급락**(빈약 전자전도). 압밀할수록 용량↑ | **압밀↑ → 용량↑**(LIB는 전자전도 개선이 지배; 이온저항↑에도 불구) — 우리 grade와 대응 |
| **7C** | **상대값 막대**: Electrolyte Transport(이온, 압밀↑ ↓) / CBD Transport(전자균질도, 압밀↑ ↑) / Active Surface Area(압밀↑ ↓). 세 경쟁 인자 | **압밀이 세 인자를 반대로 움직임** — 최적 porosity는 trade-off |
| **8** | **NMC lithiation state 3D map**(z축 단면, @110 mAh/g): un-cal은 분리막→집전체 농도구배 가파름(전자전도 나쁨), 압밀할수록 균질. 작은 AM이 더 완전 리튬화 | **PSD가 고-C-rate 리튬화 균질도 지배**(작은 입자 유리) |
| **S1** | NMC SEM + PSD 히스토그램 → **6 bin 직경**(2.5/3.5/4.5/5.86/8.28/10.35 µm) | 실측 PSD → DEM 입력 변환 |
| **S2** | **슬러리 검증**: η-γ(3.3→1.0 Pa·s) sim=exp, ρ=2.14 g/cm³ | 슬러리 force-field 검증(Lombardo ref [18]) |
| **S3** | **표면적 size 효과**: 723→2892→11569 µm²서 indentation 곡선 평활화 → 11569 선택 | DEM RVE 크기 수렴 |
| **S4** | **PSD 알고리즘 cross-validation**(구+실린더, Dong/Torayev): 압밀↑ → 구·실린더 포어 모두 감소 | PSD 방법 robustness |
| **S5** | calendering 후 CBD 응집·AM-CBD 거리 한계까지 감소·AM-AM 국소질서↑(Fig S5 pore network 추출: 초록 입자/청 구포어/적 실린더포어) | 압밀 미세구조 변화 종합 |
| **S6** | **plate 속도 효과**: 2e-3→2e-4 µm/µs서 g(r) 불변 → 2e-3 충분히 느림 | DEM 속도 수렴(quasi-static 확인) |
| **S7(=S8 fig)** | **실측 discharge @1C**: 32±1 %(5.92 MPa) vs 26.3±0.8 %(86 MPa). un-cal은 1C서 거의 무용량 | **실측 압밀-용량 추세**(sim과 같은 방향: 압밀↑ 용량↑) |

## 6. Post-processing ★
- **무엇**:
  - **porosity / 밀도**: 압밀 후 ε(Table 1, Fig 2B/5). sim ε = 1−Σ(입자부피)/박스부피. **2 % 입자팽창은 PorosityPlus에서 제외**(과대평가 방지).
  - **PSD**: **Hg porosimetry**(실측, Washburn 실린더 가정) vs **PorosityPlus**(sim, 구 fit, Dong/Torayev) — **두 방법 절대값 다름**(Hg는 실린더·접촉각, PorosityPlus는 구). S4는 **구+실린더 둘 다**(Dong/Torayev) cross-validation.
  - **g(r)**: PorosityPlus로 CBD-CBD/AM-CBD/AM-AM 방사분포(질서 정량). Table S3에 AM-AM 피크를 AM쌍 조합으로 귀속.
  - **tortuosity**: **GeoDict**(Fick 1법칙 → MacMullin) τ(x,y,z), CBD inner-porosity 47 % 반영. **DiffuDict**로 확산 시뮬(pore D=7.5×10⁻¹¹, CBD D=2.46×10⁻¹¹).
  - **EIS τ**: **Landesfeind TLM**(ref [69]) — 고-중주파 sloping을 실축에 투영×3 = R_ion, τ_EIS 그래프법(Table 3).
  - **electrochemistry**: COMSOL 4D-resolved 1C discharge(비용량) + EIS(Nyquist) + lithiation state map. **Electrolyte/CBD transport/Active surface** 3 인자 상대값(Fig 7C).
- **도구**: LIGGGHTS(DEM), LAMMPS(CGMD), COMSOL(FEM/EIS), PorosityPlus(porosity·PSD·g(r)), GeoDict(τ), DiffuDict(확산), INNOV(자체 voxelization 0.25 µm). 실측: micro-indentation(CSM MHT Vickers), Hg porosimetry, comma-gap 코팅·prototype 압연(BPN250, 25 cm 롤, 0.54 m/min, 60 ℃), discharge·EIS.
- **수치화·플롯·기록 방식**: porosity·τ를 압력의 함수로(Fig 2B/5), PSD·g(r)를 3 조건 비교(Fig 3/4), discharge·EIS를 3 조건(Fig 6/7). **검증은 indentation 곡선 형태 + porosity-vs-P 동시**(Fig 2A·2B — 처음으로 두 descriptor).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (LIB calendering) | 우리 (ASSB cold-press) | 차이 / 이유 |
|---|---|---|---|
| **제조→성능 디지털 트윈** | 슬러리(CGMD)→건조(CGMD)→**압연(DEM)**→전기화학(FEM) | DEM 압밀 → 네트워크(Kirchhoff/Holm) σ → grade | **철학 동일 ✓** — Franco가 제조 전 단계를, 우리가 압밀→전달을 |
| **★ 압밀 모드** | **calendering(압연, 이동 plate=롤, 2단계: 압축→복귀/springback)** | **cold-press(단축 정수압, 목표압력 유지/hold)** | **압연 ≠ 단축프레싱** — 압밀경로·springback 다름. 둘 다 입자 densify지만 |
| **★ porosity 목표 방향** | **porosity = GOOD**(액체전해질이 채움; ~27 % floor가 목표, 너무 낮추면 이온저항↑) | **porosity = BAD**(SE가 percolate 해야; 낮을수록 좋음, ~10 % 목표) | **★★ 정반대 목표.** LIB는 적당히 남기고, ASSB는 최대한 없앤다 |
| **★ 이온 채널 위상** | **공극(pore)=전도체**: Li⁺가 액체전해질로 → Bruggeman ε^1.5·τ | **SE 고체 입자망=전도체**: Li⁺가 SE 접촉으로 → Kirchhoff/Holm R=1/(2σr_c) | **★★ 위상 정반대.** 압밀↑ → LIB σ_ion↓(공극↓) vs ASSB σ_ionic↑(SE접촉↑). cf. Sangrós 대조와 동일 |
| **전자 전달** | NMC-continuum **FEM**(COMSOL, σ=5e-3 S/m) | AM-network **Kirchhoff** + Holm + Stage-E | **둘 다 전자전도 미세구조 의존**. 그들=continuum FEM, 우리=명시 접촉망(더 미시) |
| **★ CBD/binder 모델** | **명시 입자상 + GH(E 2 GPa) + SJKR 점착 bond**(끊김·재형성, CED) | CBD = **Stage-2 부피점유**(PTFE/VGCF가 SE 도메인 부피 차지); 명시 bond **없음**(backlog A3) | **이게 우리가 CBD를 끈끈한 bond로 올릴 때 템플릿**(Sangrós 영구파단 vs Ngandjong 재형성 — 둘 중 선택) |
| **접촉 소성** | **GH CONTACT 탄소성/점탄성**(δ 프록시), CBD가 부드러움(E 2 GPa)으로 흡수 | MPM 진짜 SHAPE 소성 + DEM hooke/hysteresis | 둘 다 입자 형상 안 변함(DEM); **형상변화 = 우리 MPM 고유**(frame[5]) |
| **E_AM** | E_NMC **200 GPa**(lit 100–200 상한) | E_CAM **140 GPa**(고정) | 유사 스케일(NMC계). 우리가 약간 낮게 |
| **검증** | **실측 2개 동시**: micro-indentation 곡선 + porosity-vs-P(+ Hg PSD, discharge, EIS) | solver=ground truth(Minnmann·Cronau·Bazzoun 등 외부 앵커) | 그들 indentation·porosity 실측이 LIB 앵커(ASSB 직접 전이 불가) |
| **소재** | **NMC + 액체전해질**(LIB) | **LPSCl SE + NMC811**(ASSB) | **다른 셀 화학** → 절대 porosity·σ·이온위상 직접 전이 금지 |
| **압밀 압력대** | **~5–160 MPa**(저압 calendering, ~85 MPa 포화) | **~300–500 MPa**(고압 cold-press) | **압력대 5–60× 다름** — LIB 압연은 저압, ASSB 프레싱은 고압 |
| **porosity floor** | **~27 %**(96:2:2 NMC, E_NMC 200, low-P 압연) | **~10 %**(pure-SE, soft E_eff + 소성흐름) / 강체 floor ~20 % | LIB는 의도적으로 높게 멈춤; 다만 stiff NMC + 저압이라 자연 floor도 높음 |

### ★★ 핵심 대비 1 — LIB 압연(porosity GOOD) vs ASSB 프레싱(porosity BAD): **같은 DEM 압밀기계, 정반대 목표**
- **같은 기계**: 양쪽 모두 **DEM으로 particulate 전극을 densify**한다. 입자(구) + 접촉 force-field + 이동 boundary(plate/롤)로 porosity를 낮추는 코어 머신은 동일(LIGGGHTS도 같은 코드 — 우리도 LIGGGHTS).
- **정반대 목표**: **LIB(이 논문)** 는 **공극에 액체전해질이 채워져 이온을 나르므로 porosity를 적당히 남겨야** 한다 — 너무 압밀하면(27 % 이하) **이온저항·tortuosity↑**(Fig 5, Table 3: τ 1.37→1.75, R_ion 0.026→0.040)로 손해. 그래서 ~27 % floor서 멈추고, discharge 용량은 **전자전도 개선과 이온저항 악화의 trade-off**(Fig 7C: Electrolyte transport↓ vs CBD transport↑). **우리 ASSB** 는 액체전해질이 없어 **공극은 순수한 방해물**, SE 입자가 서로 닿아야만 Li⁺가 흐르므로 **porosity를 최대한(~10 %) 없애야** 한다.
- **압밀경로도 다름**: calendering은 **압연 line-load + 압축→복귀(springback)** 2단계(Fig 1·Fig 2B). cold-press는 **단축 정수압을 목표값까지 유지(hold)**. 압력대도 LIB **5–160 MPa**(저압, ~85 MPa 포화) vs ASSB **300–500 MPa**(고압) — **5–60× 차이**. 따라서 **Fig 2B의 P-vs-porosity 곡선을 우리 P-vs-porosity·Heckel과 직접 겹치면 안 됨**(압력대·압밀모드·소재 전부 다름). 다만 "압력↑ → porosity↓ → 포화 floor" 형태와 "저압서 elastic→plastic knee"(LIB ~5–10 MPa, 우리 Heckel P_y=138 MPa)는 **물리적으로 대응**.
- **→ 깔끔한 대조**: "Franco의 LIB calendering DEM과 우리 ASSB cold-press DEM은 **동일한 DEM 압밀 머신**(LIGGGHTS, 구+접촉+이동 boundary)을 공유하지만, **LIB는 porosity를 GOOD으로 두고(액체전해질 충전)** ~27 %서 멈춰 trade-off를 최적화하는 반면, **ASSB는 porosity를 BAD로 두고(SE percolation)** ~10 %까지 없앤다 — 같은 기계, **정반대의 porosity 목표함수**." (Sangrós 대조와 짝 — Sangrós도 같은 결론을 LIB-DEM 균질화로, Ngandjong은 LIB-DEM+FEM으로.)

### ★★ 핵심 대비 2 — CBD 모델: Ngandjong(GH+SJKR 명시 입자상, 재형성 bond) vs 우리(Stage-2 부피점유) vs Sangrós(영구파단 bond)
- **Ngandjong CBD** = **명시 별도 입자상**(carbon black+PVdF 응집체, 0.65 µm 구, 내부 나노porosity 47 %) + **GH(E_CBD=2 GPa, AM의 1/100 → 부드러운 변형상) + SJKR 점착**(CED=7×10⁴, AM의 ~1/9 → 약하지만 끈끈). **bond는 끊어졌다 재형성**(SJKR을 매 접촉마다 재계산; 떼는 힘>F_SJKR이면 분리, 재접촉시 복원). → CBD가 **압밀 시 AM 사이를 채우고 AM 표면을 덮으며**(Fig 4B), 부드러워서 압밀을 흡수하고 끈끈해서 구조를 잡음.
- **Sangrós bond**(`papers/sangros2020_*`, 같은 LIB-DEM이나 TU-BS) = **입자-입자 bond(법선·접선, 강성 6e12 N/m³)** + **임계응력서 영구파단**(2e13 N/m², 재형성 없음). CBD를 **bond(연결)** 로, Ngandjong은 **입자(별도상)** 로 — **모델 철학 차이**(bond-as-link vs CBD-as-particle).
- **우리** = CBD를 **Stage-2 부피점유**(PTFE/VGCF가 SE 도메인 부피를 차지)로만, **명시 bond·명시 입자상 둘 다 아직 없음**(backlog A3, `docs/digest_model_application_backlog.md` + `papers/lee2025_*` co-rolled PTFE).
- **→ 우리에게**: CBD를 부피점유에서 **명시 모델**로 올릴 때 **두 청사진**이 있다 — **(a) Ngandjong식 "명시 입자상 + GH(부드러운 E) + SJKR(재형성 점착)"**, **(b) Sangrós식 "입자-입자 bond + 영구파단"**. ASSB의 PTFE/VGCF는 **섬유상 fibrillated PTFE**(`lee2025_*`)라 Ngandjong의 등방 구-CBD와도, Sangrós의 점-bond와도 정확히 같지 않지만, **"부드럽고 끈끈한 변형상(GH+SJKR)" 골격은 PTFE 섬유망의 1차 근사로 적합**. 특히 SJKR의 **CED×접촉면적 + 끊김·재형성**은 PTFE의 점착·cold-weld 거동(우리 `--coh` 백로그 A3)과 직결.

### ★ 핵심 대비 3 — ARTISTIC 디지털 트윈 파이프라인 ↔ 우리 DEM→전달→grade
- **그들 파이프라인**: **슬러리(CGMD, η-γ·밀도 검증) → 건조(CGMD, 용매수축) → 압연(DEM, indentation·porosity 검증) → 전기화학(FEM 4D-resolved, discharge·EIS)**. 각 단계가 **실측으로 독립 검증**되고 출력이 다음 입력(순차 커플링). "디지털 트윈" = 제조 레시피→미세구조→셀 성능을 in-silico로 잇는 것.
- **우리 파이프라인**: **DEM 압밀(Minnmann·Cronau 앵커 검증) → 네트워크 솔버(Kirchhoff/Holm, σ_ionic/e/thermal) → 스케일링 법칙(LOOCV 0.90–0.98) → grade_engine(ASR·Q·η·cycle-stable)** + **MPM(SEM morphology 검증) → scaffold 커플링**. 우리도 **제조(압밀)→전달→성능(grade)** 을 in-silico로 잇는다.
- **공통 철학**: 둘 다 **"한 미세구조에서 여러 물성을 뽑고, 각 단계를 실험에 보정"**. 차이는 **(i) 화학**(LIB 액체 vs ASSB 고체), **(ii) 전달 솔버**(그들 FEM continuum + Bruggeman vs 우리 명시 Kirchhoff/Holm 네트워크), **(iii) 우리는 ML 스케일링 법칙 + grade로 압축**, **(iv) 우리는 MPM으로 형상소성 절반을 추가**(그들은 입자 형상 불변).
- **→ 우리에게**: ARTISTIC은 **"제조 전 단계(슬러리·건조)까지" 모델링한 더 긴 파이프라인** — 우리는 압밀에서 시작하지만, 만약 ASSB 슬러리/건조(또는 dry-process 혼합/fibrillation)를 모델링하려면 **CGMD force-field 보정(Lombardo ref [18]) 방법론이 청사진**. 또한 그들의 **단계별 실측 검증 2개 동시**(indentation 곡선 + porosity-vs-P)는 우리 DEM 압밀 검증을 강화할 LIB판 모범(우리는 Minnmann porosity 단일 앵커가 주).

### ★ 핵심 대비 4 — 압력→porosity, tortuosity, knee
- **압밀곡선**: LIB Fig 2B는 **42 %→(5–10 MPa knee)→~32 %→(85 MPa)~27 % 포화**. 우리 Heckel(pure-SE, 4압력)은 R²=0.965·**P_y=138 MPa**·σ_y_eff≈46 MPa. **둘 다 elastic→plastic knee + 포화 floor 형태**지만 **압력 스케일이 ~20× 다름**(LIB 저압 vs ASSB 고압) — LIB 전극은 **CBD가 부드럽고(E 2 GPa) NMC 사이 공극이 커서** 저압에 쉽게 압밀, ASSB는 stiff SE를 고압으로 밀어야. **floor도 LIB ~27 %(stiff NMC + 저압 + porosity 일부러 남김) vs ASSB ~10 %(soft E_eff + 소성흐름이 강체 floor ~20 % 아래로)**.
- **tortuosity**: 그들 τ는 **압밀↑에 증가**(공극경로 악화, 1.37→1.75) — 이온 전도체가 공극이므로. **우리 τ는 압밀↑에 감소해야 유리**(SE 경로 개선) — **위상 역전의 또 다른 발현**. 그들 τ는 GeoDict Fick + EIS-TLM 두 길로 추출(우리 τ_Laplace/τ_Dijkstra 두 길과 대응).

### frame[5] 위치
- **이 논문 = 전달/패킹 측 + LIB 전기화학**: rigid 구(AM+CBD) + GH+SJKR 접촉/bond → DEM 압밀, 그 위 **FEM continuum 전기화학**(Bruggeman 공극이온 + NMC전자). **입자 형상소성·void-fill은 없음**(GH=CONTACT) — 우리 MPM이 메우는 절반이 빠짐(Sangrós·Varkey와 동일 한계, Franco 그룹도 동일).
- **그들 LIB 이온(pore-Bruggeman + FEM) = 우리 ASSB가 SE-network Kirchhoff/Holm으로 대체하는 바로 그 방법** — 대조축.
- **그들 전자(NMC-continuum FEM) ↔ 우리 AM-network Kirchhoff** — 같은 물리(전자전도 미세구조 의존), 방법만 continuum vs 명시망.

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **paper 대조축 — "같은 DEM 압밀 머신, 정반대 porosity 목표"**: LIB calendering(porosity GOOD, 액체전해질 충전, ~27 % floor, 압밀↑→이온↓·전자↑ trade-off) ↔ ASSB cold-press(porosity BAD, SE percolation, ~10 % 목표, 압밀↑→이온·전자 둘 다↑). **둘 다 LIGGGHTS·구·접촉·이동 plate**라 "머신은 같고 목적함수가 반대"가 가장 선명한 대비. Sangrós(균질화)와 Ngandjong(DEM+FEM)을 **두 LIB 선례**로 묶어 우리 ASSB 정체성 정당화.
- ② **CBD 명시화 청사진(backlog A3)**: 우리가 CBD를 Stage-2 부피점유→명시 모델로 올릴 때 **(a) Ngandjong "명시 입자상 + GH 부드러운 E(2 GPa) + SJKR 재형성 점착(CED×A)"** 또는 **(b) Sangrós "점-bond + 영구파단"** 중 선택. PTFE 섬유(`lee2025_*`)의 **점착·cold-weld(우리 `--coh`)** 는 **SJKR(CED·끊김·재형성)** 와 직결 — Ngandjong식이 우리 fibrillated-PTFE 1차 근사에 더 가까움(부드럽고 끈끈한 변형상).
- ③ **디지털 트윈 파이프라인 확장**: ARTISTIC은 슬러리·건조까지 모델링(CGMD force-field 보정 Lombardo ref [18]). 우리가 ASSB **dry-process 혼합/fibrillation**을 언젠가 모델링하려면 이 CGMD 보정 방법론이 청사진. 또 **단계별 실측 2개 동시 검증**(indentation+porosity)은 우리 압밀 검증 강화 모범.
- ④ **데이터**: `docs/data/ngandjong2021_dem_calendering.csv` — calendering porosity-vs-압력(Fig 2B/5, digitized) + tortuosity(Fig 5, z) + τ_EIS/R_ion(Table 3, stated) + discharge 용량(Fig 7B, stated) + 실측 discharge porosity(Fig S8, stated) + DEM·CBD 파라미터(Table 2, stated). **단 LIB·액체전해질·저압 압연이라 절대 porosity·σ·이온위상 ASSB 전이 금지, 추세·방법·CBD모델 대조용**. (densification_porosity_db.csv에도 calendering 행 추가 — material_SE는 N/A=액체전해질이라 빈칸/표기.)

## 9. 인용 가능 문장 (deck/paper용)
- "Ngandjong, Lombardo et al. (2021, Franco group / ARTISTIC) reported the **first experimentally-validated 3D DEM calendering model** that explicitly resolves both the **active material and the carbon-binder domain** — the CBD modelled as a **soft, sticky deformable phase** via a Granular-Hertz contact (E_CBD = 2 GPa, 1/100 of NMC) plus a **simplified JKR adhesive bond that breaks and re-forms** — embedded in a **slurry(CGMD)→drying(CGMD)→calendering(DEM)→electrochemistry(FEM)** digital-twin pipeline of Li-ion manufacturing."
- "Both the LIB-calendering DEM and our ASSB cold-press DEM use the **same densification machine** (LIGGGHTS spheres + contact force-field + a moving plate), but with **opposite porosity objectives**: in a **liquid-electrolyte** LIB the pores are the **ionic conductor**, so calendering raises tortuosity and ionic resistance (τ 1.37→1.75, R_ion 0.026→0.040 Ω m²) and the electrode is stopped at ~27 % porosity to balance electronic gain against ionic loss; in an **all-solid-state** electrode the **solid-electrolyte particle network** is the ionic conductor, so porosity is purely detrimental and is driven down to ~10 % — the same DEM machine optimised toward an **inverted porosity target**."
- "Across the Franco (Ngandjong/Sangrós) and our groups, every state-of-the-art electrode-densification DEM treats the particles as **rigid spheres with contact-level (visco-)elasto-plasticity** and **no true particle shape change** — independently confirming that the **plastic-morphology / void-fill half** (our MPM) is missing from the DEM side, in LIB and ASSB alike (frame [5])."

## 10. 주의/한계 (over-claim 방지)
- **LIB (액체전해질)** — 이온 채널이 **공극(Bruggeman·τ)** 이라 σ_ion·τ의 **절대값·부호(압밀↑→증가)** 를 우리 ASSB(SE-network, 압밀↑→σ_ionic 증가)로 전이 **금지**. 전자·CBD·압밀역학만 물리 대응; **이온은 위상 자체가 반대**(대조용으로만).
- **저압 calendering(~5–160 MPa) ≠ ASSB cold-press(~300–500 MPa)** — 압력대 5–60× + 압밀모드(압연 line-load+springback vs 단축 hold) 달라 **Fig 2B P-vs-porosity 곡선을 우리 곡선/Heckel과 직접 겹치면 안 됨**(knee·floor 형태만 정성 대응).
- **강체 구(AM+CBD) + GH CONTACT 탄소성/점탄성** — 입자 **형상 안 변함**(δ=기하 프록시, 2 % 팽창은 GH 비영 트릭). **형상소성·void-fill 없음** → 우리 MPM 영역과 별개(frame[5]). CBD의 "변형"도 입자 E가 낮을 뿐 형상흐름 아님.
- **CBD = 등방 구 응집체**(0.65 µm) — 실제 carbon black+PVdF 망의 **섬유·연결 토폴로지를 단일 구로 coarse-grain**. 우리 PTFE는 **섬유상**(`lee2025_*`)이라 토폴로지가 더 다름 — SJKR 골격은 1차 근사이나 섬유 이방성·연결성은 미반영.
- **σ·discharge 절대값은 FEM 입력 보정에 의존**: NMC 전자전도도를 **실측보다 낮춤**(5×10⁻³ S/m, "수렴 위해")이라 본문이 명시 — **un-calendered의 진짜 전자전도 한계(고-C-rate 무용량)는 COMSOL 수치한계로 직접 재현 못 함**. sim 용량이 실측보다 체계적으로 낮은 것도 **건조 z-주기경계 BC 불일치 + AM 전자전도 인위적 상향** 탓이라 저자 인정.
- **PSD 절대값 방법의존**: Hg porosimetry(실린더·Washburn) vs PorosityPlus(구) **절대값 다름**(본문 명시) — 추세(압밀↑→포어↓·작아짐)만 신뢰. S4 구+실린더 cross-validation도 추세 확인용.
- **Fig 2B/3/4/5의 porosity·τ·g(r) 값 일부는 디지타이즈**(그래프에서 읽음) → **추세만(±)**. **stated**: Table 1(porosity 42±2/41.6 %), Table 2(DEM 파라미터 E·ν·CED·X_u), Table 3(R_ion·τ_EIS), discharge 116.2/121.5/130.7 mAh/g, 3 대표 porosity(41.6/31.5/27.2 %), PSD 6 bin, CBD 직경·밀도·47 % 나노porosity, FEM 입력(σ·D), Fig S8 실측 discharge(32±1 %@5.92 MPa, 26.3±0.8 %@86 MPa).
- **NMC111(LiNi₀.₃₃Mn₀.₃₃Co₀.₃₃O₂)** — 우리 NMC811과 다른 활물질(E·전도도·PSD 다름), 게다가 **calendering 자체가 1차입자 cracking·2차입자 거동 미반영**(본 논문이 "primary NMC particles + cracking 후속 연구"라 명시). 절대값 전이 금지.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

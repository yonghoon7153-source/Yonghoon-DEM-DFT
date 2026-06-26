<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목.  COMPREHENSIVE / paper-level standalone. -->
# ASSB 복합양극을 *고강도 믹서(high-intensity mixer)* 로 만드는 공정을 DEM으로 — coarse-graining + **force-scaling**(접촉력 스케일링) + 3단계 보정으로 stressing condition을 추출하고, 그것을 미세구조·풀셀 용량에 연결 — Frankenberg (Powder Technology 2024)

> slug `frankenberg2024_dem_high_intensity_mixer_assb` · DOI `10.1016/j.powtec.2024.119403` · type `DEM (Rocky 2023 R1, coarse-grained + force-scaling, 3-step calibration; exp 풀셀 검증)` · PDF `Frankenberg_2024_PowderTech_DEM_HighIntensityMixer_ASSBCathode.pdf` · digested `2026-06-26` · status ✅ · OPEN ACCESS (CC BY)

> ★ **이것은 calendering(압연) DEM 두 편(`sangros2019_*`, `ngandjong2021_*`)과 *공정 위치가 다르다*.** Sangrós/Ngandjong = **습식 슬러리·건조·압연**(전극을 누르는 densification). 본 논문 = 그보다 **앞 단계인 *건식 혼합(dry high-intensity mixing)*** — LFP+CB+SE 입자를 고속 회전 믹서에서 충돌·전단시켜 **heteroaggregate(이종응집체)** 를 만드는 **mechanofusion/aggregation 공정**을 DEM으로 시뮬한다. 즉 cold-press(우리)·calendering(LIB)이 *압밀*이라면 본 논문은 *그 전의 입자-조립(mixing)*. 그리고 본 논문의 **방법론적 핵심 = "coarse-graining(입자 크기 26.65× 확대로 입자수 격감) + force-scaling(거친 입자의 접촉력을 f²로 스케일해 원래 입자의 응력·충돌당 에너지가 보존되게)"** 인데, 이 **force-scaling이 우리 18× E-연화와 같은 "DEM 접촉력/강성을 인위적으로 조정하는" 부류**라 §A/§B에서 두 철학을 직접 비교한다.

---

## 1. 한 줄 요약
**ASSB 복합양극(LFP + 카본블랙 + 할라이드 SE Li₃InCl₆)을 *고강도 믹서*로 제조할 때 입자에 가해지는 stressing condition(응력강도 SI·응력빈도 SF·응력수 SN·비에너지 E_m)을 DEM으로 *처음* 정량화**하고, 그것을 미세구조(FIB-SEM 응집 상태)·풀셀 방전용량에 연결한 논문. 세 가지 방법론 성과: ① **coarse-graining** — 실제 0.7 µm급 heteroaggregate를 0.5 mm DEM 입자로 **26.65× 확대**(입자수 36,670개로 격감 → 계산시간 단축, 작은 입자는 timestep Δt_sim∝R*가 폭증해서 불가능); ② ★ **force-scaling approach** — 거친 입자는 충돌시 원래 입자보다 큰 힘을 받으므로 **Hertz·Mindlin 접촉력을 f², JKR 점착력을 f²로, 겹침 δ를 f로, 충돌시간 τ를 f로** 스케일해서 **거친 입자의 *응력 σ_CG=σ₀* 와 *충돌당 비에너지 E_m,CG=E_m,0* 가 원래(scale-independent) 입자와 같아지게** 유도·검증(eq 5–8); ③ **3단계 보정**(동적안식각 DAOR → 정적안식각 SAOR → 압축시험)으로 회전드럼·실린더 pull-up·compaction 실험에 맞춰 마찰·점착·E·ν·COR을 결정. **핵심 결과: 풀셀 방전용량은 비에너지 입력 E_m이 클수록 증가(C_discharge ∝ n, 10,000 min⁻¹서 109±5 mAh g⁻¹)하되, 회전속도 n이 정하는 *응력강도 SI 의 한계*에 의해 상한이 걸린다** — 같은 SN에서 SI가 5,000(0.78 J kg⁻¹) vs 10,000 min⁻¹(3.35 J kg⁻¹)이면 SI 큰 쪽이 용량 큼, 그러나 "최대 분산도"에 도달하면 SI·SN 추가 투입은 용량을 더 못 올림(분산 포화 + 재응집/granulation 역효과 가능). **단 이것은 *전달 σ 솔버가 없는* 공정-역학 DEM**(응력·에너지·응집만; porosity·σ_ionic/e/thermal·형상소성 모두 미보유) + **할라이드 SE**(우리 LPSCl 아님) + **rigid 구**(형상불변, mechanofusion의 진짜 표면-융합·코팅은 미모델).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/CB/SE) | 연구유형 |
|---|---|---|---|---|
| **Finn Frankenberg, Maximilian Kissel, Christine Friederike Burmeister, Mark Lippke** (TU Braunschweig — **Institute for Particle Technology**, Volkmaroder Str. 5, 38104 Braunschweig) + **Jürgen Janek** (Justus-Liebig-Universität Gießen — Institute of Physical Chemistry & Center for Materials Research, Heinrich-Buff-Ring 17, 35392 Gießen) + **Arno Kwade** (교신 = Frankenberg, TU-BS) | **Powder Technology 435 (2024) 119403** (접수 2023-10-29, 수정 2024-01-04, 게재 2024-01-11, Available online 2024-01-11) | 10.1016/j.powtec.2024.119403 | **AM = LiFePO₄ (LFP, submicron, Johnson Matthey)** + **CB = carbon black (IMERYS SUPER C65)** + **SE = Li₃InCl₆ (LIC, 할라이드, in-house 수계합성)**; **mass ratio LFP:CB:LIC = 58:4:38**. 음극 = In/InLi. 셀 SE 분리층 = Li₆PS₅Cl (LPSCl, NEI Corp.). | **DEM** (상용 **Rocky 2023 R1**) = **Hertz–Mindlin + JKR 점착 접촉** + **coarse-graining(26.65×)** + ★ **force-scaling(f² 접촉력)** + **3단계 보정**(DAOR/SAOR/compaction 실험) + **풀셀 전기화학 검증**(0.1 C, 1.9–3.4 V) |

> ★ **계보 / TU-Braunschweig Kwade 그룹 라인**: 본 논문은 calendering DEM 두 편과 *같은 그룹(TU-BS IPAT, Kwade)* 이지만 **공정이 다르다** — Sangrós Giménez 2019/2020(`papers/sangros2019_*`, `sangros2020_*`)·우리 wishlist의 calendering은 **전극 압연(densification)**, 본 논문은 **그 전 단계인 *건식 고강도 혼합(heteroaggregate 형성)***. 본 논문은 **CB desagglomeration**(carbon black 풀기)을 DEM+population balance로 다룬 선행(ref [59] Asylbekov, 같은 그룹)을 ASSB 양극 혼합으로 *반대 방향(aggregation)* 확장한 것. **force-scaling 식의 출처** = Bierwisch [68](f² 단면적 스케일), Washino [73](JKR f² 차원해석), Mohajeri [66]/Hoshikawa [78]/Roessler [77]/Thakur [75] — 본 논문은 이들을 **모아 ASSB heteroaggregate에 적용·검증**. **coarse-graining** = Bierwisch [62]·Hilton [63]·Jiang [64]·Hu [65]·Nakamura [66] 계보. Kwade의 **stressing model**(SI·SN·SF·E_m) = ref [86,88]. **Janek 그룹(Gießen)** 이 ASSB 재료·전기화학 측을 댐(LIC 합성 ref [40] Li & Liang, coating ref [35] = LiNbO₃). ⇒ **"제조 공정(IPAT) + ASSB 전기화학(Janek)" 협업**.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (n, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **★ 풀셀 방전용량 vs 회전속도 n** | **109 ± 5 mAh g⁻¹** @ 10,000 min⁻¹ | t_mix=60 min, 0.1 C, In/InLi | stated(본문 §4.4 + Fig 9a) | **C_discharge ∝ n** (선형 증가). LFP 이론용량 140 mAh g⁻¹ — 10,000 min⁻¹서 ~78 % 도달 |
| **방전용량 vs n (저속)** | ~21 / ~46 / ~78 / ~109 mAh g⁻¹ | n ≈ 2,000 / 5,000 / 7,500 / 10,000 min⁻¹ | digitized(Fig 9a) | 1,000 min⁻¹은 거의 0 (응집 불량) |
| **★ 응력강도 SI 한계** | SI = **0.78** (5,000 min⁻¹) vs **3.35 J kg⁻¹** (10,000 min⁻¹) | t_mix 5–60 min | stated(본문 §4.4 + Fig 9b/d/f) | 같은 SN서 **SI 큰 쪽이 용량↑**; SI가 용량 상한 결정 |
| **최적 혼합시간 t_mix** | **~30 min** (그 이후 포화) | 5,000·10,000 min⁻¹ | stated(본문 §4.4 + Fig 9b) | 30 min 이후 용량 정체(분산 포화); >60 min 재응집/granulation 역효과 가능 |
| **★ E_m ∝ n 멱법칙** | **E_m^normal ∝ n^2.79**, E_m^shear ∝ n^2.71, E_m^dissipation ∝ n^2.73 | DEM 전 도메인, 1 s | stated(eq 20–22) | E_m ∝ n^(2.7–2.8). 전체 specific energy E_m ∝ n^2.7–2.8 |
| **★ SI ∝ n 멱법칙** | **SI^normal ∝ n^2.17**, SI^shear ∝ n^2.09, SI^dissipation ∝ n^2.11 | DEM 전 도메인 | stated(eq 17–19) | SI ∝ n²(충돌압축/전단의 운동에너지 ∝ v²∝n²) |
| **★ SN ∝ n 멱법칙** | **SN ∝ n^0.62** | DEM 전 도메인 | stated(본문 §4.3) | 응력빈도/수는 n에 약하게 의존. SI가 SN보다 n에 강하게 의존 |
| **비파워 P_m ∝ n** | **P_m ∝ n^2.82** (sim) ≈ 실측 | DEM vs 실험 | stated(본문 §4.3) | 시뮬-실측 specific power 의존성 일치(검증) |
| **mean SI (Region별, 10,000 min⁻¹)** | gap **SI₁^normal=7.410** / rotor **SI₂^normal=49.430** / outside **SI₃^normal=0.236** J kg⁻¹ | n=10,000 min⁻¹, 0.7–1.0 s | stated(Table 4) | rotor blade서 충돌압축 최대 |
| **mean SI^shear (Region별)** | gap 6.005 / rotor **13.893** / outside 0.327 J kg⁻¹ | 〃 | stated(Table 4) | rotor서 전단 최대 |
| **mean SI^dissipation (Region별)** | gap 14.626 / rotor **51.795** / outside 0.764 J kg⁻¹ | 〃 | stated(Table 4) | rotor서 에너지 소산 최대(응집·sinter 유발) |
| **입자 병진속도 v_part (Region별)** | gap 12.134 / **rotor 35.007** / outside 9.980 m s⁻¹ | 〃 | stated(Table 4) | rotor tip speed v=2πnR_t=39.9 m s⁻¹ (계산) |
| **gap 전단율 γ̇** | **2,604 – 26,042 s⁻¹** | n 1,000–10,000, gap h_min=1.532 mm | stated(eq 15) | γ̇=R_t·2πn/h. 고전단=좋은 분산 |
| **★ coarse-grain factor f** | **f = d_CG/d₀ = 26.65** | DEM 입자 0.5 mm / 실제 응집체 ~18.77 µm | stated(본문 §3.1) | d_CG=0.5 mm ÷ d₀(=x₅₀=18.77 µm) ≈ 26.65 |
| **heteroaggregate 입경 x₅₀** | **18.77 ± 0.26 µm** (laser diffraction) | 10,000 min⁻¹ 제조 | stated(본문 §2.1) | 실제 응집체 중간크기 = coarse-grain의 원래 입자 d₀ |
| **DEM coarse-grain 입자크기** | **0.5 mm** (= 실제 26.65× 확대) | DEM 입력 | stated(본문 §3.2) | <0.5 µm면 timestep 폭증으로 불가; >크면 gap에 jam |
| **DEM 입자수** | **36,670 particles** (3 g 분량) | 축소 도메인(1/5) | stated(본문 §3.2) | 실험 15 g → 도메인 1/5로 3 g만 시뮬 |
| **★ E (coarse-grain, 보정)** | **E = 25 MPa** | compaction 시험 보정값 | stated(Table 3, 본문 §4.1) | ★ **이건 *재료 E가 아니라* heteroaggregate *분체(다공)* 의 압축 거동 E** — 저자 명시 |
| **ν (coarse-grain)** | **0.3** | compaction 보정 | stated(Table 3) | |
| **COR e_pp (입자-입자)** | **0.3** | compaction 보정 | stated(Table 3) | wall e_pw=0.3 |
| **★ rolling friction μ_r** | **0.2** (입자-입자) | DAOR 보정(linear spring rolling) | stated(Table 3, 본문 §4.1) | 비구형 형상을 rolling friction으로 대리 |
| **static friction μ_s,pp** | **0.44** (입자-입자) | DAOR 보정 | stated(Table 3) | wall μ_s,pw=0.5 |
| **dynamic friction μ_d,pp** | **0.44** (입자-입자) | DAOR 보정 | stated(Table 3) | wall μ_d,pw=0.3 (※ 조건: static ≥ dynamic) |
| **★ surface energy Γ_pp (JKR 점착)** | **0.0045 J m⁻²** (입자-입자) | DAOR 보정 | stated(Table 3, 본문 §4.1) | wall Γ_pw=0.001. ★ **강한 점착성 분말 → JKR 필수**(저자 강조) |
| **bulk density ρ_b (coarse-grain)** | **750 kg m⁻³** (sim) / 701.83 ± 16.95 (exp) | DAOR 충진율 보정 | stated(Table 3, 본문 §4.1) | sim ρ_b 살짝 올려 충진율 맞춤(실측 701.83은 드럼압축으로 과대) |
| **입자(응집체) 밀도 ρ_p** | **1,250 kg m⁻³** (coarse-grain) | (포어 0.59 포함) | stated(Table 3) | ε_bulk=0.4 → particle density 1,250 (inner-porosity ε_inner=0.59) |
| **순물질 밀도 ρ₀** | **3,047 kg m⁻³** (coarse-grain) / mixer wall 4,510 | — | stated(Table 3) | |
| **★ DAOR(동적안식각) Φ₁ (sim, 보정 후)** | 30.82 / **30.35** / 29.26 / 15.50° | n = 5/10/15/60 min⁻¹ | stated(Table 2) | 실측 Table 1과 일치(10 min⁻¹ 보정점 Φ₁=30.35 vs exp 30.30) |
| **★ DAOR Φ₂ (sim)** | 53.77 / **57.22** / 61.50 / 65.61° | n = 5/10/15/60 min⁻¹ | stated(Table 2) | 고속 회전서 angle 증가(강점착) |
| **★ SAOR(정적안식각) 검증** | sim **54.21 ± 1.14°** vs exp **55.58 ± 1.44°** | 실린더 pull-up | stated(본문 §4.1 + Fig 5a) | 보정 후 SAOR 재현 = 파라미터 검증 |
| **compaction E 검증** | sim force-displacement = exp (Fig 5b) | 1 g 시료, 상부 stamp 4.17 mm s⁻¹ | stated(Fig 5b) | 초기 편차(coarse-grain) → 고압축서 일치 |
| **셀 압밀압력 (분리층/양극)** | **380 MPa** (LPSCl 분리층 + 양극 uniaxial) | 셀 조립 | stated(본문 §2.2) | cold-press 380 MPa = 우리 300·Doux 370·Minnmann 380 계열 |
| **셀 작동 stack pressure** | **~25 MPa** | cycling(0.1 C, 1.9–3.4 V) | stated(본문 §2.2) | ★ 제조 380 ≫ 작동 25 — 우리 "제조≠작동" 인식과 합류 |
| **DEM timestep Δt_sim** | eq (1): Δt=0.2·πR*√(ρ/G*)/(0.8766+0.1631ν) | coarse-grain 0.5 mm | stated(eq 1) | ★ **Δt ∝ R*** → 작은 입자면 Δt 폭증(=coarse-graining 동기) |
| **σ_ionic / σ_e / σ_thermal** | **없음 — 본 논문 미산출** | — | — | ★ **공정-역학 DEM. 전달 σ 0채널**(우리 삼중항 우위) |
| **porosity (정량)** | **없음 — 본 논문 미산출** | — | — | ★ **압밀 porosity 안 풂**(혼합공정이라 응집·응력만; FIB-SEM은 정성) |

> ★ **LFP를 AM으로 쓴 이유(본문 §1 명시)**: NMC와 달리 **LFP는 *submicron* 으로 구할 수 있어 확산경로가 짧다**(개선된 전기화학 잠재) + **LIC(할라이드)는 LPSCl과 달리 NMC 같은 고전위 CAM에 안정**할 필요가 없음(LFP는 저전위). 즉 이 논문은 **"submicron LFP + 할라이드 SE + CB" 라는 *새 heteroaggregate 재료계*** 를 도입한 것 — 우리 NMC811+LPSCl과 *다른* 소재계라 **절대값 전이 금지**(추세·방법만).

## 4. 시뮬레이션 방법 ★

### 4.0 전체 구조
**고강도 믹서(Picoline + Nobilta, Hosokawa Alpine)의 회전구조-드럼 기하를 CAD로 만들고, 그 안에서 heteroaggregate 분말을 회전(n=1,000–10,000 min⁻¹)시켜 입자에 가해지는 stressing condition(SI·SF·SN·E_m)을 DEM으로 추출**. 핵심 3요소 = **(A) coarse-graining**(실제 18.77 µm 응집체 → DEM 0.5 mm, f=26.65× — 입자수·계산시간 격감) + **(B) force-scaling**(거친 입자 접촉력을 f²로 스케일해 *원래* 입자의 응력·에너지를 보존, eq 3–8) + **(C) 3단계 보정**(DAOR→SAOR→compaction). 추출한 SI를 **Kwade stressing model**(E_m=SN·S̄E/m, SI=Σ충돌에너지/질량)으로 풀셀 용량과 연결. **전기·이온 전도도는 풀지 않음**(실측 풀셀 용량으로만 성능 평가).

### 4.1 code / version
- **DEM = Rocky 2023 R1** (상용; ANSYS Rocky). ★ calendering 두 편(LIGGGHTS)·우리(LIGGGHTS)와 **다른 코드**. Hertz–Mindlin + JKR 접촉모델. 비구형 형상은 **계산비용 때문에 구로 처리**(Rocky의 비구형 입자는 훨씬 느림) + **linear spring rolling friction 모델**로 비구형성 대리.
- 후처리 = **자체 python 스크립트**(Rocky export → 충돌기반 SI·E_m 계산, eq 9–14). 안식각·압축은 실험(GranuDrum, 자체 cylinder pull-up, ZWICK 시험기).

### 4.2 ★ DEM 접촉법칙 — Hertz–Mindlin + JKR (force-scaling 대상)
- **법선 = Hertz**(eq 5): `F_n^Hertz = (4/3)·E*·√(R₀*·f·δ₀·f)·δ₀·f` — E*=유효탄성률, R₀*=원래 입자 유효반경, δ₀=원래 겹침. **접선 = Mindlin**. **점착 = JKR**(F_n^JKR, 표면에너지 Γ).
- **항복캡 없음** — Hertz는 탄성, JKR은 점착. **소성 항복점(p_y) 모델 없음**(= calendering의 Thornton–Ning과 다름; 본 논문은 압밀-소성이 주제가 아니라 *혼합 응력*이라 탄성-점착 접촉으로 충분). compaction 보정 E=25 MPa는 *분체 압축거동*이지 입자 항복 아님.
- ★ **JKR 필수(저자 강조, §4.1)**: heteroaggregate 분말이 **강한 점착성**(submicron LFP+CB) → 안식각이 매우 inhomogeneous(높은 표준편차) → **점착모델(JKR) 없이는 거동 재현 불가**. Hoshikawa et al.도 같은 결론(강점착 입자 = JKR + surface energy·rolling friction 보정).

### 4.3 ★★ force-scaling approach (eq 2–8) — 본 논문의 방법론 심장
**문제**: coarse-graining으로 입자를 f배 키우면, *충돌시* 거친 입자는 원래 입자보다 **더 큰 힘**을 받는다(질량·관성 커짐). 그대로 두면 거친 입자의 응력·에너지가 실제와 달라짐. **해결 = 접촉력을 스케일**해서 *거친 입자가 겪는 응력·충돌당 에너지 = 원래 입자의 것* 이 되게 한다.

**coarse-grain factor (eq 2):** `f = d_CG / d₀` (CG=coarse grain, 0=original). 본 논문 f=26.65.

**스케일 가정(에너지·차원 보존):**
- 겹침 (eq 3): `δ_CG = δ₀ · f` — 거친 입자 겹침은 f배.
- 충돌시간 (eq 4): `τ_CG = τ₀ · f` — 에너지보존에서 충돌시간도 f배(Bierwisch [67]).
- **유효탄성률 E*·전단률 G* 는 상수 유지**(재료 그대로).

**→ 접촉력 스케일 (eq 5·6):** Hertz 법선력에 δ·R가 각각 f씩 → `F_n,CG^Hertz = F_n,0^Hertz · f²`. 일반형 (eq 6): **`F_CG^X = F₀^X · f²`** (X = Hertz/Mindlin/JKR). **JKR 점착력도 f²**(Washino [73] 차원해석; 표면에너지 Γ는 f 스케일이라 JKR이 f²).

**→ 응력·에너지 scale-independence(핵심 결과, eq 7·8):**
- **응력 (eq 7):** `σ_CG = F₀·f² / (A·f²) = σ₀` — 거친 입자 응력 = 원래 입자 응력. (A=단면적 ∝ f²; 분자·분모 f² 상쇄.) ★ **"거친 입자를 시뮬해도 *실제 입자가 겪는 응력*을 그대로 얻는다."**
- **충돌당 비에너지 (eq 8):** `E_m,CG = ∫F₀·f²·dδ₀·f / (m_p,0·f³) = E_m,0` — 충돌당 비에너지도 보존. (충돌에너지 = 힘×거리 ∝ f²·f=f³; 질량 m_p ∝ f³; 상쇄.)
- **스케일 지수 요약(SI 검증, 본문):** 접촉력 ∝ **f²**, 응력 ∝ **f⁰**(독립), 충격량(impulse) ∝ **f³**, 충돌시간 ∝ **f¹**.

**검증(§3.3 끝, SI):** 같은 크기 두 입자를 ρ=1,250 kg m⁻³·v_part=0.1 m s⁻¹·거리 10 mm로 충돌시켜 **force-time 곡선이 입자크기 의존성을 따르는지** 확인 → Hertz·JKR 법선력·Mindlin 접선력 모두 **eq 6의 f² 스케일을 따름을 확인**(마찰영향 제거 위해 friction=0.001).

> ★ **이 force-scaling이 우리 18× E-연화와 *같은 부류*** — 둘 다 **"DEM 접촉력/강성을 *물리적 근거를 갖고* 인위 조정"**. 단 *목적이 다르다*: 그들 force-scaling = **coarse-graining의 부작용(거친 입자 과대힘)을 *상쇄*** 해서 *원래 응력을 보존*(scale-invariant); 우리 18× 연화 = **rigid-sphere가 못 하는 granular 재배열/GB-slide를 *럼핑*** 해서 *거시 porosity를 실험에 맞춤*. **그들 = 보존(invariance), 우리 = 보상(compensation).** 상세 §A.

### 4.4 ★ coarse-graining (왜·어떻게)
- **왜**: 실제 heteroaggregate ~0.5–18.77 µm → 그대로 시뮬하면 입자수 폭발 + **timestep 폭증**. ★ **eq (1) Δt_sim = 0.2·πR*√(ρ/G*)/(0.8766+0.1631ν) ∝ R*** — 입자 반경이 작을수록 Rayleigh timestep이 작아져서 같은 물리시간을 풀려면 step 수가 **지수적으로 증가**(0.5 µm 미만이면 CPU·GPU 모두 비현실적, SI). → 입자를 **26.65× 키워**(d_CG=0.5 mm) Δt를 키우고 입자수를 36,670개로 줄임.
- **크기 선택의 trade-off**: 너무 크면(>0.5 mm) **gap(1.532–1.895 mm)에 jam** → 비현실적 고응력; 너무 작으면 timestep 폭증. **0.5 mm = 정확도-계산시간 절충**(gap의 ~1/3).
- **도메인 축소**: 믹서를 **1/5 크기로 절단** + **y방향 주기경계** → 실험 15 g 대신 **3 g만 시뮬**.

### 4.5 ★ 입자 처리 (DEM판 "무질서 처리")
- **구만** (heteroaggregate = 강체 구, 단분산 0.5 mm coarse-grain). **비구형 형상은 *계산비용 때문에* 구로 단순화** + **rolling friction(linear spring, μ_r=0.2)으로 비구형성 대리**(Rocky 비구형 입자는 훨씬 느림 — 저자 명시). **rigid 입자 + Hertz-Mindlin CONTACT + JKR 점착** — **입자 형상 안 변함**. ★ **mechanofusion의 *진짜* 표면-융합/코팅/입자 합체(sinter-granulation)는 미모델** — 본 논문은 그 "*응력·에너지를 추출*"해서 응집 *경향*을 추론하지, 응집체 *형성 자체*(입자가 붙고 모양이 바뀜)를 시뮬하지 않는다. (= frame[5]에서 우리 MPM이 메우는 형상-변화 절반이 여기도 빠짐; 게다가 본 논문은 단일 응집체를 *입자 하나*로 coarse-grain해서 응집체 *내부* 거동도 안 봄.)
- **PSD**: DEM은 **단분산**(0.5 mm). 실제 heteroaggregate는 x₅₀=18.77 µm 다분산이나 coarse-grain에서 단일크기로. (원료 LFP 0.5 µm–1 µm·CB·LIC 0.1 µm–1 µm는 *응집체 하나로* 합쳐짐.)
- **초기구조**: 입자를 **연속주입(continuous injection, 0.0–0.1 s)** 으로 도입 → 0.1–1.0 s 회전. **steady state**(0.5 s 이후, 특히 0.7–1.0 s)에서 응력·에너지 측정.
- **파쇄(fracture)**: 입자 깨짐 미모델. 단 본문은 **고속서 입자가 깨질 수도(comminution)** 있다고 *정성 언급*(rotor서 고응력·고소산 → LIC 응집체 분쇄 = 더 미세 = 더 좋은 이온망); 이는 SI 분포의 non-monomodality(두 응력 메커니즘)로 *간접* 표현.

### 4.6 ★★ 3단계 보정 (DAOR → SAOR → compaction, Fig 2)
**heteroaggregate 분말의 거동을 세 실험에 순차로 맞춰** 마찰·점착·역학 파라미터를 결정(Fig 2 흐름도: Deviation 있으면 재보정, 셋 다 맞으면 Ready):
1. **DAOR(동적안식각, Dynamic Angle of Repose)** — **회전드럼(GranuDrum)** 으로 Φ₁(낮은각)·Φ₂(높은각)을 n=5/10/15/60 min⁻¹서 측정. **충진율(filling ratio)** 먼저 맞춤(실측 ρ_b 701.83은 드럼압축 과대 → sim ρ_b=750으로 조정해 ε_bulk=0.4·ε_inner=0.59 재현). **민감도(DoE, pyDOE, 16 시뮬)**: DAOR 지배 = **rolling friction μ_r·static/dynamic friction μ_s/μ_d·surface energy Γ_pp**(이 4개를 [μ_r 0.1–0.5, μ_s 0.1–0.9, μ_d 0.1–0.9, Γ 0.0005–0.005] 범위 DoE) → **μ_r=0.2, μ_s=μ_d=0.44, Γ=0.0045 J m⁻²** 가 5–60 min⁻¹ 전 속도 재현. 5 mm 슬라이스(20 mm 드럼의)+y 주기경계로 단축. **10 min⁻¹을 보정점, 나머지를 검증**.
2. **SAOR(정적안식각, Static Angle of Repose)** — **cylinder pull-up test**(실린더에 분말 채우고 일정속도 0.0075 m s⁻¹ 인상 → 무너진 각). **DAOR 보정 파라미터로 SAOR을 *검증*** → sim 54.21° vs exp 55.58°(±1.14/1.44) **일치**(파라미터 correct 확인). 안 맞으면 재보정.
3. **compaction(압축시험)** — **ZWICK 시험기**, 하부 die에 1 g 채우고 상부 stamp를 4.17 mm s⁻¹로 6 mm 도달까지 하강, **force-displacement 곡선** 기록 → **E=25 MPa, ν=0.3, COR e_pp=0.3** 결정. **마지막에 함**(역학파라미터는 안식각에 영향 적음 — ref [81]). ★ 초기 force 편차(coarse-grain 입자망 ε_total=0.75가 초기엔 거의 저항 없다가 점착 극복 후 급증)는 coarse-grain 탓, **고압축서 sim=exp 일치**라 calibrate OK.

### 4.7 전달 솔버
- **없음.** 본 논문은 전기·이온·열 전도도를 풀지 않는다. **성능 = 실측 풀셀 방전용량**(0.1 C, 1.9–3.4 V vs In/InLi)으로만. (= calendering 두 편이 σ를 *풀거나*[Ngandjong FEM] *균질화*[Sangrós 2020]하는 것과도 다름; 본 논문은 *공정 응력*만.)

### 4.8 ★ Kwade stressing model — 응력을 성능에 연결 (eq 9–22)
**DEM에서 뽑은 충돌 데이터를 Kwade의 "stressing model"로 변환**해 미세구조·용량과 잇는다:
- **mean frequency ē_i (eq 10·11):** 입자 i가 Δt_out(=0.005 s) 동안 겪은 충돌수 N_k,i / Δt_out; mean collision duration τ̄.
- **power (eq 9):** `P_i^α = Σ W_k^α / Δt_out` (α = normal/shear/dissipation). 충돌에너지 W_k 합 / 시간.
- **collision-based 비에너지 (eq 13) = stress intensity SI:** `E_m,i^collision = (Σ W_k^α / N_k,i)·(1/m_p) = SI^α` — **입자 질량당 충돌에너지** = 응력강도. normal/shear/dissipation 3종.
- **collision-based 응력 (eq 14):** `σ_x,i^collision = (ΣJ_i/Στ_i)·(N_k,i/ΣJ_i)·(1/A)·...` — 충격량 J·충돌시간 τ·단면적 A로부터. SI를 N_k,i회 저장 → x축 로그분포.
- **stress frequency SF (본문):** SI 분포를 0.3으로 나눠(0.3 s 측정구간) **초당 stress 빈도** = 주어진 SI가 t_mix 동안 몇 번 일어나는가.
- **stress number SN (eq 16, Kwade [86,88]):** `E_m = S̄E·SN / m_total` — 비에너지 = 평균 충돌에너지 S̄E × 응력수 SN / 총질량. (E_m·E_m,collision은 m_p로 이미 나눠서 SI = E_m,i^collision.)
- **멱법칙(allometric fit, eq 17–22):** SI ∝ n^2.1, SN ∝ n^0.62, E_m ∝ n^2.7–2.8, P_m ∝ n^2.82. ★ **SI가 SN보다 n에 훨씬 강하게 의존** → 고속 회전은 *충돌 강도*를 키우는 게 주효과(빈도보다).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **Graphical Abstract** | Process(LIC+LFP+CB → 믹서) → Simulation(coarse-graining·calibration) → Characterization(n·t_mix 영향, FIB-SEM, 용량-vs-에너지). 하단 heteroaggregate 모식+SEM | **"공정→시뮬→특성화" 한 컷** — 우리 DEM→Kirchhoff→grade 철학 그림의 *혼합공정* 판 |
| **1** | (a) heteroaggregate 제조 모식(LFP+LIC+CB → n,t_mix → core-shell 응집체: 큰 LFP 코어 + CB·LIC 쉘); (b) **10,000 min⁻¹ 제조 응집체 SEM**(200 µm scale) | ★ **heteroaggregate = "큰 LFP 입자를 CB·LIC가 둘러싼 core-shell"** 모식 — 우리 AM-SE 접촉 개념의 *혼합공정* 버전. mechanofusion 목표 구조 |
| **2** | ★ **3단계 보정 흐름도**: DAOR(드럼, Φ₁·Φ₂ → μ_r·μ_s·μ_d·Γ_pp) → SAOR(실린더 pull-up, DAOR 검증) → Compaction(E·ν·e_pp). 각 단계 Deviation 시 재보정, Ready까지 | ★ **분체 거동 보정 프로토콜의 모범**(3 독립 실험으로 마찰·점착·역학 분리 결정). 우리 단일 Minnmann 앵커보다 다단계 |
| **3** | (a) **고강도 믹서 CAD 전체**(회전구조+드럼, 20 mm scale); (b) **축소 시뮬 도메인**(1/5, y주기, 입자색=속도) | 믹서 기하·도메인 축소. 우리 RVE와 대응(단 회전기하) |
| **4** | ★ **DAOR 실측 vs 시뮬**(n=5/10/15/60 min⁻¹): 상=실측 드럼사진(Φ₁·Φ₂ 각도 표시), 하=시뮬(입자색=속도, Φ 각). 고속일수록 Φ₂↑(강점착) | **DAOR 보정 검증 1:1**(실측 53.16/56.70/61.88/65.45° vs sim 53.77/57.22/61.50/65.61°). 점착분말 거동 |
| **5** | (a) **SAOR 실측(55.58°) vs 시뮬(54.21°)** 실린더 pull-up; (b) ★ **compaction force-displacement**: sim(파랑) vs exp(빨강 평균). 초기 편차→고압축 일치 | ★ **압축거동 보정·검증**. 초기 "거의 저항없음→점착극복후 급증"이 우리 Heckel 저압 거동과 *형태* 유사(단 분체-E 25 MPa) |
| **6** | ★ **stress intensity 분포 vs 회전속도 n**(1,000–10,000 min⁻¹): (a) **normal SI**, (b) **shear SI** stress frequency(s⁻¹) vs SI(J kg⁻¹) 로그축. **n↑ → SI 분포 우측이동(강해짐)·SF↑·non-monomodal**(두 봉우리=두 응력 메커니즘) | ★ **회전속도가 응력강도 분포를 어떻게 옮기나** — 우리엔 없는 *공정 응력 분포*. non-monomodal = gap압축 + rotor충격 두 메커니즘 |
| **7** | ★ **Region별 응력**(Fig 6 도메인 내 3영역): Region 1=gap(검정), 2=rotor blade(흰), 3=outside gap(파랑). 각 영역 F_n·F_t 방향 모식 | ★ **공간분해 응력맵**: rotor blade서 SI 최대(충격), gap서 압축, outside서 최소. 우리 force-chain 공간분포와 개념 대응 |
| **8** | ★ **FIB-SEM 양극 단면·표면**(다른 n): (a) 1,000 min⁻¹ 단면(CB agglomerate·LIC cluster·**contact loss**), (b) 1,000 표면(LIC cluster·**uneven surface**), (c) 10,000 단면(LIC agglomerate 작음), (d) 10,000 표면(균질·매끈) | ★ **저속=응집체 큼·접촉손실·불균질 / 고속=균질·미세**. 미세구조→용량 인과의 *직접 증거*(단 정성). 우리 morphology 검증의 *혼합공정* 판 |
| **9** | ★★ **방전용량 6패널**: (a) **vs n**(C∝n 선형, 10,000서 109±5); (b) **vs t_mix**(30 min 포화, SI 3.35 vs 0.78); (c) **vs SI**; (d) **vs SN**(SI 3.35가 0.78보다 위); (e) **vs specific energy E_m**; (f) ★ **vs E_m 로그**(겹침 + **SI 한계로 포화/하강** = 분산 최대 후 정체) | ★★ **본 논문 핵심 결과 전부.** 용량 ∝ n·E_m, **SI가 상한 결정**, t_mix 30 min 최적, 분산 포화 후 재응집 역효과 |

## 6. Post-processing ★
- **무엇**:
  - **stress intensity SI (eq 13)·stress frequency SF·stress number SN (eq 16)·specific energy E_m**: Rocky 충돌 데이터(force normal/tangential, 충돌수 N_k, 충돌시간 τ, impulse J)를 **collision-based**로 변환. normal/shear/dissipation 3종. **로그분포**(SI를 N_k회 저장).
  - **mean frequency ē·collision duration τ̄ (eq 10·11)**: 입자별 충돌수/시간.
  - **mean SI·v_part by Region (Table 4)**: gap/rotor/outside 3영역 steady-state(0.7–1.0 s, Δt_out=5 µs로 축소).
  - **allometric fits (eq 17–22)**: SI·SN·E_m·P_m 의 n 의존 멱지수 → 실측 specific power와 대조(검증).
  - **shear rate γ̇ (eq 15)**: gap 전단율 = R_t·2πn/h.
  - **미세구조(FIB-SEM)**: 응집체 크기·접촉손실·표면균질도 *정성* 평가(Fig 8).
  - **전기화학**: 풀셀 방전용량(0.1 C, t_mix·n 함수) — porosity·σ 없이 *성능*만.
- **도구**: **Rocky 2023 R1**(DEM) + **자체 python**(SI·E_m 변환). 실험: **GranuDrum**(DAOR), 자체 cylinder pull-up(SAOR), **ZWICK 시험기**(compaction), **laser diffraction Horiba LA-960**(PSD x₅₀=18.77 µm), **FIB-SEM**(미세구조), **planetary ball mill Pulverisette 7**(LIC 합성), 풀셀 cycler.
- **수치화·플롯·기록 방식**: SI·SF를 n의 함수 로그분포(Fig 6), Region별 mean을 Table 4, 멱법칙 eq 17–22. 용량을 n·t_mix·SI·SN·E_m 5축으로(Fig 9). **검증은 3단계(DAOR 4속도 + SAOR + compaction) + specific power 멱지수 실측 대조**.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (고강도 믹서 DEM) | 우리 (ASSB cold-press) | 차이 / 이유 |
|---|---|---|---|
| **공정 위치** | **건식 고강도 *혼합*(heteroaggregate 형성, mechanofusion)** — 압밀 *전* | **cold-press 압밀**(380 MPa급 단축) | ★ **다른 공정 단계.** 본 논문 = 입자-조립; 우리 = 입자-압밀. 둘이 직렬(혼합→압밀) |
| **연구 범위** | **공정 응력·에너지·응집**(SI·SF·SN·E_m) + 실측 용량 | 압밀(DEM·MPM) + **전달 삼중항 σ_i/σ_e/σ_thermal** + grade | **본 논문 전달 σ 0채널·porosity 미산출** — 우리 삼중항·porosity가 그들엔 없음 |
| **★ DEM 접촉 조정** | **force-scaling**(거친 입자 접촉력 ×f², eq 6) — coarse-graining 부작용 *상쇄*, 응력 *invariant*(eq 7) | **18× E-연화**(24→1.35 GPa) — rigid-sphere 미보유 granular 역학 *럼핑*, porosity 실험에 *맞춤* | ★★ **둘 다 접촉력/강성 인위조정이나 *목적 정반대*: 그들=보존(invariance), 우리=보상(compensation).** 상세 §A |
| **★ coarse-graining** | **26.65×**(0.5 mm 입자, 36,670개) — timestep Δt∝R* 동기 | **coarse-graining 안 함**(실제 12:4:1 크기) — bimodal Furnas dip 위해 실크기 필수 | **그들은 입자수 격감 위해 키움 / 우리는 dip 위해 실크기**. 단 우리 MPM도 grid 한계로 12:4:1 어려움(packing-limited) |
| **★ 소성 종류** | **없음**(Hertz-Mindlin 탄성 + JKR 점착; 항복캡 無) — 혼합응력이라 소성 불필요 | DEM hooke/hysteresis(캡 無)+18×연화; MPM 진짜 J2 SHAPE 소성 | **본 논문은 *압밀-소성 자체가 주제 아님*** → 소성 비교는 calendering 두 편이 더 적합 |
| **★ 점착(JKR)** | **JKR 필수**(Γ_pp=0.0045 J m⁻², 강점착 분말) | SE-SE 점착 = `adhesionStiffness`/`--coh`(DMT 체제) | **둘 다 점착 모델**. 그들 JKR(큰·무른 극한) vs 우리 DMT(작고 단단). cold-weld는 우리 쪽 |
| **압밀 압력대** | **혼합 응력**(SI 0.2–50 J kg⁻¹, *압력 아닌 *비에너지*) + 셀조립 380 MPa | **300–500 MPa** cold-press | ★ **본 논문 주축은 *압력*이 아니라 *비에너지/응력강도*** — 직접 비교 불가(다른 축). 셀조립 380은 우리 300 계열 |
| **porosity** | **미산출**(혼합공정; FIB-SEM 정성) | pure-SE ~10 % / real_14 15.6 % @300 | **그들 porosity 없음** → densification_porosity_db에 *porosity 칸 비움*(공정·E·응력만) |
| **E (입력)** | **E=25 MPa**(★ *분체 압축거동* E, 재료 아님) | E_SE real 24 GPa / E_eff 1.35 | ★ **그들 25 MPa = heteroaggregate *분체(다공)* 압축 모듈러스** — 우리 단일입자 E와 *층위 다름*(직접 동일시 금지). 비교한다면 우리 "압밀-bed E_eff" 쪽 |
| **소재 (SE/AM)** | **할라이드 Li₃InCl₆ + submicron LFP + CB** | **LPSCl + NMC811** | ★ **다른 SE(할라이드)·다른 AM(LFP)** → 절대값·σ·porosity 직접 전이 **금지**(추세·방법만) |
| **검증** | **3단계 분체실험(DAOR/SAOR/compaction) + 풀셀 용량 + specific power 멱지수** | solver=ground truth(Minnmann·Cronau·Bazzoun 외부 앵커) | 그들 분체실험·풀셀이 *공정* 앵커(우리 압밀·전달과 다른 검증축) |
| **형상변화** | **없음**(rigid 구, mechanofusion 표면융합 미모델) | MPM 진짜 J2 형상변화(SEM 일치) | **형상소성 = 우리 MPM 고유**(frame[5]). 게다가 그들은 응집체를 *입자 하나*로 coarse-grain |
| **코드** | **Rocky 2023 R1**(상용) | **LIGGGHTS**(오픈) | 다른 코드(접촉식 유사 Hertz-Mindlin-JKR) |

## A. 우리 DEM+MPM 대비 (comparison vs ours)

### A-1. ★★ 공정 위치: 혼합(그들) → 압밀(우리) = *직렬 공정*, 정면충돌 아님
- **본 논문 = 압밀 *전* 단계.** ASSB 양극 제조는 보통 **① 활물질·SE·도전제를 혼합(mixing) → ② 압밀(cold-press)** 이다. 본 논문은 **①(고강도 건식 혼합으로 heteroaggregate 형성)**, 우리·calendering은 **②(densification)**. 즉 **경쟁이 아니라 *직렬*** — 본 논문의 산출물(혼합된 heteroaggregate 분말)이 우리 DEM의 *입력(초기 패킹)* 이 될 수 있다(§B-3).
- 따라서 **porosity·Heckel·σ 곡선을 직접 겹칠 대상이 아니다.** 본 논문의 주축은 **응력강도 SI·비에너지 E_m**(압력 아님)이고, 산출은 **풀셀 용량**(porosity·σ 아님). calendering 두 편(Sangrós/Ngandjong)이 *압밀*이라 우리와 같은 축(porosity-vs-P)에서 비교됐다면, **본 논문은 *다른 축(혼합 응력-vs-용량)***.

### A-2. ★★ force-scaling(그들) vs 18× E-연화(우리) — *같은 부류, 정반대 목적*
이게 사용자가 짚은 핵심 비교다. **둘 다 "DEM 접촉력/강성을 물리적 근거를 갖고 인위 조정"** 하지만 **목적·방향이 정반대**:

| 축 | 그들 force-scaling (eq 3–8) | 우리 18× E-연화 |
|---|---|---|
| **무엇을** | 거친(coarse-grain) 입자 접촉력을 **×f²**(δ×f, τ×f), E*·G*는 *상수 유지* | SE 영률을 **24→1.35 GPa(÷18)** — *재료 E 자체를 낮춤* |
| **왜** | coarse-graining(26.65×)이 만든 **과대힘을 *상쇄*** | rigid-sphere가 못 하는 **granular 재배열/GB-slide/micro-fracture를 *럼핑*** |
| **목표** | **응력·충돌에너지 *invariance*** — 거친 입자가 *원래 입자와 똑같은* σ₀·E_m,0 (eq 7·8) | **거시 porosity *matching*** — 연화한 bed가 *실험 ~10 %* porosity 재현 |
| **철학** | **보존(conservation/invariance)** — 정보를 *안 바꿈*, 단지 크기효과 상쇄 | **보상(compensation)** — *빠진 물리*(rigid 한계)를 effective param에 *흡수* |
| **검증** | force-time 곡선이 f² 따름(SI), 응력 scale-independent | pure-SE Cronau overlap 11–12 %·MPM 독립 8 %·Heckel 셋이 동일 연화 요구 |
| **근거 출처** | Bierwisch [68](f² 단면적)·Washino [73](JKR 차원해석) — *해석적 유도* | Minnmann 실험 앵커 + MPM 교차검증 — *실험·교차모델* |

- **→ 핵심 통찰**: 우리 18× 연화는 **"보상(빠진 물리 흡수)"** 이라 *어느 정도 임의성*이 늘 비판받았는데(왜 하필 18×?), **force-scaling은 "보존"이라 *해석적으로 유도*(eq 7: σ_CG=σ₀가 *수학적으로 보장*)**. **즉 force-scaling은 우리가 *못 가진* 깔끔한 유도 구조를 보여준다** — 만약 우리가 *coarse-graining*(입자수 줄이려 키우기)을 도입한다면, force-scaling은 **18× 연화와 *별개로*(혹은 위에) 적용해야 할 *추가* 스케일**이다(연화=물리보상, force-scaling=크기보존; 직교).
- **⚠ 단 우리 18× 연화는 *연화가 곧 목적(granular 럼핑)*** 이지 coarse-graining 부작용 상쇄가 아니다 — 우리는 입자를 *안 키운다*(실크기 12:4:1). 그래서 **force-scaling이 우리 연화를 *대체* 하지 않는다.** 둘은 다른 문제를 푼다: force-scaling = "입자를 키웠을 때 응력 보존"(우리는 안 키워서 *불필요*); 18× 연화 = "rigid가 못 하는 흐름 럼핑"(force-scaling은 *제공 안 함*). **상보적이되, 우리 연화의 *임의성 비판*에 대한 답은 force-scaling이 아니라 *경로 A(항복캡)*·MPM 교차검증이다**(So 2021·Varkey + 우리 MPM).
- ★ **그래도 차용 가치**: force-scaling의 **"E*·G* 상수 + δ·τ·force만 스케일 → 응력 invariant" 유도**는 우리가 *만약 큰 RVE를 coarse-grain*(예: 셀-스케일 시뮬)할 때 **18× 연화와 *함께* 써야 할 별도 보정**의 완성된 템플릿이다. 그리고 **"DEM 접촉력 조정이 *임의가 아니라 유도될 수 있다*"는 방법론적 선례** — 우리 연화의 *물리적 정당화* 서술(frame[2])에 "접촉력 스케일링은 DEM에서 확립된 기법(force-scaling 계보 Bierwisch/Washino)"이라 인용 가능(연화도 그 *한 형태*).

### A-3. heteroaggregate(LFP+CB+할라이드) vs 우리 AM-SE 접촉
- **그들 heteroaggregate = "큰 LFP 코어 + CB·LIC 쉘"(Fig 1) core-shell 응집체** — 혼합으로 작은 CB·SE가 큰 AM을 *둘러싸* 좋은 계면접촉을 만드는 게 목표(mechanofusion). 우리 AM-SE는 *압밀 후* SE가 AM을 *덮는* coverage(Stage-E Tabor)와 개념이 닮았으나 **단계가 다름**: 그들 = 혼합 시 *조립*, 우리 = 압밀 시 *접촉면적*.
- **⚠ 소재 차이가 큼**: 그들 SE = **Li₃InCl₆(할라이드)**, AM = **submicron LFP**(우리 NMC811 아님), 게다가 **CB가 제3상**(우리도 CBD 있으나 그들은 혼합 핵심). 할라이드는 LPSCl보다 σ 낮고(Varkey/Kim 2025 cross-check: σ_LIC 류 ~0.5 < LPSCl 1.6) E 다름 → **σ·porosity·E 절대 전이 금지**. 가져올 건 **(i) "혼합이 계면접촉을 만든다"는 *공정 인과*, (ii) force-scaling/coarse-graining *방법*, (iii) 응력강도→용량 *관계 형태***.

## B. 적용가능성 (applicability to our LIGGGHTS DEM model)

### B-1. ★ force-scaling = 우리 *coarse-graining 도입 시* 직접 적용 (현재 우리는 실크기라 미적용)
- **현재**: 우리 DEM은 실크기 12:4:1(coarse-graining 안 함) → **force-scaling 불필요**(입자를 안 키우니 과대힘 없음). 우리 18× 연화는 *별개 문제*(granular 럼핑) — A-2 참조.
- **언제 필요**: 만약 **셀-스케일·대용량 RVE**(입자 수백만 → 계산 불가)로 가면 coarse-graining이 필요해지고, **그때 eq 3–8(δ×f, τ×f, force×f², E*·G* 상수)** 을 그대로 적용해 **응력·에너지를 invariant로 보존**해야 한다. 이건 **18× 연화 *위에* 곱해지는 별도 스케일**(연화는 물리, force-scaling은 크기). LIGGGHTS는 `pair_style`에서 contact stiffness를 직접 주므로 **f² force-scaling 구현 가능**(Hertz `youngsModulus`는 E* 상수 유지, δ·radius만 f 스케일).
- **매핑**: 우리 `network_conductivity.py`/Stage-E의 **접촉면적 A=πR*δ** 가 coarse-grain되면 **A∝f²**(eq 7 분모) → 응력 σ=F/A invariant 자동(eq 7). 즉 **Stage-E 소성면적도 force-scaling과 *호환***(둘 다 면적 ∝f² 가정).

### B-2. ★ 우리 18× 연화 정당화 서술 보강 (frame[2])
- force-scaling 계보(Bierwisch [68]·Washino [73]·Mohajeri [66])는 **"DEM에서 접촉력을 *물리근거로* 조정하는 것은 *확립된 표준 기법*"** 이라는 외부 근거다. 우리 frame[2] "18× 연화는 임의가 아니라 granular 럼핑 프록시"라는 서술에 **"접촉력/강성 스케일링은 coarse-grained DEM의 표준(force-scaling)이며, 우리 연화는 *물리-보상형* 스케일링의 한 형태"** 라 *방법론적 위치*를 줄 수 있다. ⚠ 단 force-scaling은 *보존*(invariance)이고 우리 연화는 *보상*(compensation)이라 **"같은 부류지만 목적이 다르다"** 를 명시해야 over-claim 아님(A-2).
- 적용 위치: `litdb/contact_models_layer_map.md` §0/§2 + CLAUDE.md frame[2] 서술. (현재 contact_models_layer_map은 *항복캡* 계보만 — force-scaling/coarse-graining 축은 *별도*. 추가 후보: "층 F. coarse-graining + force-scaling"으로 Bierwisch/Washino/본 논문.)

### B-3. ★ 혼합-응력 → 초기 패킹 seeding (우리가 *안 하는* PRE-압밀 공정)
- 본 논문의 **혼합 단계(heteroaggregate 형성)는 우리가 모델 안 하는 *압밀 전* 공정**이다. 우리 DEM은 **랜덤 비중첩 삽입**으로 초기구조를 만들고 바로 압밀한다 — 즉 *혼합 이력(mixing history)* 이 없다.
- **차용 가능**: 만약 **혼합이 만든 core-shell heteroaggregate(큰 AM + SE·CB 쉘)** 를 우리 초기 패킹의 *seed* 로 쓰면, 압밀 전부터 **SE가 AM을 둘러싼** 구조에서 출발 → coverage·percolation 초기조건이 달라질 수 있다. 본 논문 Fig 8(저속=응집체 큼·접촉손실 / 고속=균질)은 **"혼합 품질이 미세구조를 정한다"** 는 직접 증거 — 우리 초기 패킹을 *균질 랜덤*이 아니라 *혼합-품질-의존*으로 줄 근거.
- ⚠ 단 **본 논문은 응집체 *형성 자체*를 시뮬 안 함**(응력만 추출, 응집체는 *입자 하나*로 coarse-grain). 그래서 "혼합 구조를 seed로"는 *개념*이지 본 논문에서 *바로 가져올 좌표*는 없다. 실측 FIB-SEM(Fig 8) morphology를 *정성* 참조하거나, 별도 aggregation 시뮬(population balance, ref [59])이 필요.
- 매핑: `scripts/` 초기구조 생성부 + `docs/cbd_morphology_roadmap.md`(CB 분산) — 혼합 품질을 dispersion CV(backlog A5)로 연결 가능.

### B-4. 응력강도→용량 관계 형태 (우리 grade와 대조)
- 본 논문 **C_discharge ∝ n·E_m, SI 한계로 포화**(Fig 9f)는 **"공정 입력 → 셀 성능"** 관계식이다. 우리 grade_engine(ASR·Q·η·cycle-stable)은 *구조 → 성능*이라 **입력축이 다름**(그들 n·SI / 우리 porosity·σ). 직접 합칠 수 없으나, **"성능에 *최적 공정 입력*이 있고 그 이상은 역효과(재응집)"** 라는 *형태*는 우리 Furnas dip("최적 조성 있고 양끝은 손해")과 *철학적으로 대응*.

## C. ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this DEM model)
> **결론 먼저: 본 논문(Frankenberg 2024)은 *고강도 혼합 공정*을 DEM으로 정량화한 우수한 공정-역학 연구이고 force-scaling 유도는 우리가 배울 점이 분명하지만, *전달·압밀-소성·형상*의 4축에서 우리가 명백히 SOTA를 앞선다.** 본 논문은 **전달 σ 0채널·porosity 미산출**(공정 응력·에너지만), 입자는 **형상불변 rigid 구**(게다가 응집체를 *입자 하나*로 coarse-grain), **할라이드+LFP**(우리 LPSCl+NMC811 아님), **압밀-소성 자체가 주제 아님**(혼합 응력). 우리 7개 차별점을 그들이 *하는 것/없는 것*에 매핑한다(모두 증거 기반: 그들 σ-부재·rigid-구·혼합-범위 근거).

**(1) 전달 삼중항 σ_ionic + σ_e + σ_thermal — 명시 Kirchhoff/Holm 접촉망 솔버 (★ 가장 강한 우위)**
- **그들**: 전도도를 **전혀 풀지 않는다.** 성능 = 실측 풀셀 용량으로만. σ_ionic·σ_e·σ_thermal·percolation·constriction 저항 모두 없음.
- **우리**: **3채널 모두**(σ_ionic LOOCV 0.975 / σ_e 0.953 / σ_thermal 0.903), **명시 접촉망 Kirchhoff Σ(φi−φj)/R=0 + Holm R=1/(2σr_c) 구속저항 + Stage-E 소성면적**. **삼중항·명시망·구속저항 = 압도적 우리 SOTA.** (본 논문은 *공정* 측이라 σ가 아예 범위 밖 — 우리 transport 정체성이 그들 빈칸을 통째로 채움.)

**(2) Stage-E 소성 접촉면적 재유도**
- **그들**: 접촉면적은 **Hertz 기하 면적**(eq 7의 A∝f²). 소성 pile-up·Tabor 면적 없음(혼합이라 소성-면적 무관).
- **우리**: **Stage-E(Tabor + volume 소성 접촉면적)** 로 elastic-Hertz 면적을 소성 면적으로 재유도 → σ 구속저항 입력 보정. 본 논문엔 해당 물리 부재.

**(3) DEM↔MPM scaffold 커플링 + 진짜 소성 MORPHOLOGY (J2)**
- **그들**: 입자는 **영원한 강체 구**(δ=기하 프록시), 게다가 **응집체를 *입자 하나*로 coarse-grain**(응집체 *내부*·*형상* 안 봄). mechanofusion의 진짜 표면-융합·코팅을 *응력 추출*로 *추론*만(Fig 8 정성).
- **우리**: **MPM 진짜 J2 소성 형상변화**(SEM 코어보존+경계평탄화 ✓), **부피보존 void-fill flow**, **DEM AM 골격 + SE만 MPM(scaffold)** 커플링, **공간 변형장 Σdg**. 그들이 *추론*만 한 형상-거동을 우리 MPM이 *직접 계산*. **형상소성 = 우리 고유**(frame[5]).

**(4) fracture-aware transport (Auerbach + Lawn)**
- **그들**: 입자 파쇄 **미모델**(고속 comminution을 SI 분포 non-monomodality로 *정성* 언급만).
- **우리**: **Auerbach 임계 + Lawn 미세균열 → fracture-aware Holm**(f_intact로 σ 부분전도). 깨진 접촉도 ~60 % 미세접촉 유지를 *전달*에 반영. 그들 "comminution 정성"과 달리 우리는 파쇄를 *정량 σ*에 연결.

**(5) 문헌-근거 σ_grain (Cronau)**
- **그들**: σ를 안 풀어 σ_grain 개념 없음(할라이드 LIC σ도 미산출).
- **우리**: **σ_grain=3.0 mS/cm × Cronau(r_SE)** — LPSCl 단결정 문헌값 + sub-µm amorphization 인자. ASSB SE 고유.

**(6) 실험-앵커 독립 듀얼모델 frame[4]/[5]**
- **그들**: **단일 DEM 모델**(3단계 분체실험·풀셀 보정). 독립 2모델 교차검증 없음.
- **우리**: **DEM(전달) + MPM(역학)** 을 *각각 독립적으로* 실험에 보정(Minnmann·Cronau·Bazzoun) — 서로 cross-fit 안 함(frame[4]). 수렴=교차검증, 발산=정량화된 모델한계. 본 논문은 단일 모델이라 이 메타-검증 구조 없음.

**(7) 솔버→스케일링 법칙 LOOCV 압축 + grade**
- **그들**: 응력→용량을 **allometric 멱법칙(SI∝n^2.1 등)** 으로 닫음 — 이건 *공정* 멱법칙이지 *구조→물성* 압축 아님. ML/LOOCV·grade 없음.
- **우리**: 네트워크 솔버 출력 → **스케일링 법칙(LOOCV 0.90–0.98) + grade_engine(ASR·Q·η·cycle-stable)** 으로 압축·외부검증. 그들 *공정* 멱법칙 ≠ 우리 *구조→물성→성능* 압축.

**⚖️ 정직하게 — 그들이 우리보다 앞선 곳:**
- ★ **① 명시적 *혼합(mixing) 공정* DEM**: 우리는 *압밀*만 모델한다 — **압밀 *전*의 혼합/heteroaggregate 형성은 우리 미보유.** 그들이 고강도 믹서의 회전기하·응력·에너지를 *처음* 정량화(SI·SF·SN·E_m)한 것은 우리에게 *없는* PRE-압밀 공정 축(§B-3).
- ★ **② 형식적 force-scaling/coarse-graining *유도***: eq 3–8(δ×f·τ×f·force×f²·E*상수 → 응력 invariant, 검증 포함)은 **DEM 접촉력 조정의 *해석적* 유도** — 우리 18× 연화의 *경험적* 보상보다 *유도 구조가 깔끔*. 우리가 coarse-graining 도입 시 직접 따라야 할 완성 템플릿(§B-1), 그리고 우리 연화의 *방법론적 위치*를 줄 외부 근거(§B-2).
- ★ **③ 할라이드 heteroaggregate(LFP+CB+LIC) + 3단계 분체보정**: 새 재료계 + DAOR/SAOR/compaction 3실험 독립 보정은 우리 단일 Minnmann 앵커보다 *분체 거동 보정의 완성도*가 높다(마찰·점착·역학 분리 결정).
- ★ **④ 공정→풀셀 성능 *직접* 연결**: 응력강도→방전용량(Fig 9, SI 한계·t_mix 최적·재응집 역효과)을 *실측 풀셀*로 닫음 — 우리 grade는 *구조→성능 예측*이라 *공정 입력* 축이 없음.
- ⚠ **단 ①②③④ 모두 *혼합공정·할라이드·LFP·rigid-구·전달부재* 범위** — **전달 삼중항·압밀-소성·형상·다중모델·구조-압축에서 우리가 SOTA**라는 결론 유지. 그들 우위 = *공정 모델링의 새 축(혼합) + force-scaling 유도*, 우리 우위 = *전달·압밀·형상·압축*. **상보적**(그들 혼합 → 우리 압밀 → 우리 전달).

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **force-scaling = coarse-graining 도입 시 18× 연화 *위에* 적용할 별도 스케일**(eq 3–8): 우리가 셀-스케일·대RVE로 가면 입자수 격감 위해 coarse-graining 필요 → **δ×f·τ×f·force×f²·E*상수**로 응력 invariant 보존. 우리 Stage-E 면적 A∝f²와 호환. **현재는 실크기라 미적용**(연화는 별개 물리). LIGGGHTS `youngsModulus`(E* 상수)+radius 스케일로 구현.
- ② ★ **우리 18× 연화 정당화 보강**(frame[2]): "접촉력/강성 스케일링은 coarse-grained DEM의 확립된 기법(force-scaling 계보)이며 우리 연화는 그 *물리-보상형*"이라 *방법론적 위치* 부여. ⚠ "보존 vs 보상" 목적 차이 명시(A-2). `contact_models_layer_map.md`에 **"층 F. coarse-graining/force-scaling"**(Bierwisch [68]·Washino [73]·본 논문) 추가 후보.
- ③ ★ **혼합-품질 → 초기 패킹 seeding**(우리 미보유 PRE-압밀): 본 논문 Fig 8(혼합 품질이 미세구조 결정)은 우리 *랜덤 균질* 초기구조를 *혼합-품질-의존*으로 줄 근거. core-shell heteroaggregate(큰 AM+SE쉘) seed → coverage·percolation 초기조건 변화. dispersion CV(backlog A5)와 연결. ⚠ 본 논문은 응집체 *형성*은 안 시뮬(응력만) → *개념*만 차용.
- ④ **공정→성능 관계 형태**(우리 grade와 대조): C∝n·E_m·SI 한계·t_mix 최적(Fig 9)은 *공정 입력→성능*. 우리 grade(구조→성능)와 입력축 다르나 "최적 입력 있고 양끝 역효과" 형태는 Furnas dip과 철학 대응.
- ⑤ ★ **제조≠작동 압력 분리 합류**: 셀조립 **380 MPa** cold-press / 작동 **~25 MPa** stack(본문 §2.2) = 우리 "300 MPa 제조(Heckel P_y 138) ≠ 수~수십 MPa 작동" 인식의 *또 하나 LPSCl-계열 근거*(Doux 370/Minnmann 380/Lee 500 계열). ⚠ 단 분리층은 LPSCl이나 양극 SE는 할라이드 LIC.
- ⑥ **데이터**: `docs/data/frankenberg2024_mixer_stresses.csv` — Table 4(Region별 SI·v_part, stated) + 멱법칙 지수(eq 17–22, stated) + 용량-vs-n·SI·E_m(Fig 9, stated/digitized) + DAOR(Table 1·2, stated) + 보정 파라미터(Table 3, stated) + force-scaling·coarse-graining 파라미터(stated). **단 할라이드·LFP·혼합공정이라 절대값 ASSB 전이 금지, 추세·방법·force-scaling 식 대조용**. densification_porosity_db에는 *porosity 칸 비우고* 공정·E(25 MPa 분체)·압력(380 제조/25 작동)만.

## 9. 인용 가능 문장 (deck/paper용)
- "Frankenberg et al. (2024, TU-Braunschweig IPAT + Janek/Gießen) were the **first to numerically quantify the stressing conditions** (stress intensity SI, stress frequency SF, stress number SN, specific energy E_m) acting on particles inside a **high-intensity mixer** producing ASSB composite-cathode **heteroaggregates** (submicron LiFePO₄ + carbon black + the halide solid electrolyte Li₃InCl₆) — a **dry pre-compaction mixing process** that precedes the cold-press densification we model — and linked these to the full-cell discharge capacity."
- "Their key methodological contribution is a **coarse-graining (26.65×, particle 0.5 mm) plus a force-scaling approach** (Hertz/Mindlin/JKR contact forces scaled by f², overlap by f, collision time by f, while E* and G* are held constant) that makes the **stress and specific collision energy on the coarse grains *scale-independent* (σ_CG = σ₀, E_m,CG = E_m,0; eqs 7–8)** — an *analytically derived* adjustment of DEM contact forces, in contrast to our *empirically compensating* 18× softening (E_SE 24→1.35 GPa). **Both adjust DEM contact stiffness, but force-scaling *preserves* (invariance) while our softening *compensates* (lumps the granular rearrangement a rigid sphere cannot perform).**"
- "The discharge capacity rose almost linearly with rotational speed (C_discharge ∝ n, reaching **109 ± 5 mAh g⁻¹ at 10,000 min⁻¹** with E_m ∝ n^2.7–2.8 and SI ∝ n^2.1) but was **limited by a stress-intensity ceiling**: at equal stress number, the higher SI (3.35 vs 0.78 J kg⁻¹) gave higher capacity, yet beyond a *maximum degree of dispersion* (≈30 min mixing) further SI/SN no longer improved capacity and could even reduce it through re-agglomeration/granulation."
- "Crucially, this is a **process-mechanics DEM with *no transport solver*** — it solves no σ_ionic/σ_e/σ_thermal and reports no compaction porosity, the particles are **rigid spheres** (each heteroaggregate coarse-grained to a *single* particle, so neither its internal structure nor any plastic shape change is resolved), and the materials are a **halide SE + LFP** (not our LPSCl + NMC811). Our work supplies the missing transport triad (explicit Kirchhoff/Holm), Stage-E plastic contact areas, fracture-aware conduction and true plastic morphology (MPM) — the halide pre-mixing process is the complementary upstream half (frame [5])."

## 10. 주의/한계 (over-claim 방지)
- ★ **공정-역학 DEM — 전달 σ 0채널·porosity 미산출**: σ_ionic/e/thermal·압밀 porosity·percolation 모두 *없음*. 본 논문에서 "전달"·"porosity"를 끌어오지 말 것(응력·에너지·용량만). 우리 삼중항·porosity 우위 비교는 *그들이 σ·porosity를 안 푼다*는 사실에 근거.
- ★ **할라이드 SE(Li₃InCl₆) + submicron LFP + CB** — **우리 LPSCl + NMC811 아님.** σ·porosity·E 절대값 **전이 금지**(할라이드 σ ~0.5 < LPSCl 1.6; LFP는 저전위·submicron). *추세·방법·force-scaling 식·공정 인과*만.
- ★ **rigid 구 + 응집체를 *입자 하나*로 coarse-grain** — 입자 형상 안 변함(δ=기하 프록시) + **응집체 *내부*·형상·표면융합 미모델.** mechanofusion의 진짜 코팅·합체는 *응력 추출로 추론*(Fig 8 정성)이지 *시뮬* 아님. **형상소성·void-fill·응집체-내부 = 우리 MPM/별도 aggregation 영역**(frame[5]).
- ★ **압밀-소성 자체가 주제 아님** — Hertz-Mindlin(탄성)+JKR(점착), 항복캡 *없음*. 본 논문은 *혼합 응력*이라 소성 불필요. **소성/항복캡 비교는 calendering 두 편(Sangrós Thornton–Ning)이 적합, 본 논문 아님.**
- ★ **주축이 *압력*이 아니라 *비에너지·응력강도***(SI J kg⁻¹) — porosity-vs-P·Heckel과 *직접 비교 불가*(다른 축). 셀조립 380 MPa·작동 25 MPa만 우리 *압력 분리* 인식과 비교(추세).
- **E=25 MPa는 *heteroaggregate 분체(다공) 압축* 모듈러스**, *재료 E 아님*(저자 명시). 우리 단일입자 E_SE(24)·E_eff(1.35)와 **층위 다름** — 직접 동일시 금지(비교하면 우리 "압밀-bed" 쪽).
- **coarse-grain f=26.65·입자 0.5 mm는 *계산편의*** — 물리 입자크기 아님(실제 x₅₀=18.77 µm). force-scaling이 응력은 보존하나 **국소 충돌 통계·gap jam은 입자크기 의존**(저자: 너무 크면 gap jam, 너무 작으면 timestep 폭증으로 0.5 mm 절충).
- **Fig 6/9의 일부 값은 디지타이즈**(그래프에서 읽음) → **추세만(±)**. **stated**: Table 1·2(DAOR Φ₁·Φ₂ 4속도), Table 3(보정 E·ν·COR·μ·Γ·ρ), Table 4(Region별 SI·v_part), 멱법칙 지수(eq 17–22: SI∝n^2.1·SN∝n^0.62·E_m∝n^2.7–2.8·P_m∝n^2.82), 용량 109±5 mAh g⁻¹@10,000 min⁻¹, x₅₀=18.77 µm, f=26.65, 입자 36,670개, E=25 MPa, 셀 380/25 MPa, γ̇ 2,604–26,042 s⁻¹, gap 1.532–1.895 mm, rotor tip 39.9 m s⁻¹.
- **DAOR 실측 ρ_b 701.83 → sim 750 조정**(드럼압축이 실측 과대) — bulk density 절대값 주의.
- **단분산 coarse-grain** — 실제 heteroaggregate 다분산·원료 다상(LFP+CB+LIC)을 *단일 구*로. PSD·다상 효과 미반영.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

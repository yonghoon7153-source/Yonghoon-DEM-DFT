<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. -->
# LIB 전극 calendering(압연)을 DEM으로 — NMC622 양극 · **EDEM(상용) + EEPA 탄소성 접촉 + Bonding(Potyondy–Cundall)** · 3-모듈 **"USER TOOL"**(공정 파라미터 *예측*) — Schreiner·Klinger·Reinhart (Procedia CIRP 2020, 짧은 학회논문)

> slug `schreiner2020_dem_calendering_lib` · DOI `10.1016/j.procir.2020.05.158` · type `DEM (EDEM 상용, EEPA+Bonding; 나노압입 보정 + 공정 USER TOOL)` · PDF `Schreiner_2020_ProcediaCIRP_DEM_Calendering_LIB.pdf` · digested `2026-06-27` · status ✅ · OPEN ACCESS (CC BY-NC-ND 4.0)
>
> ★ **짧은 학회논문(Procedia CIRP, 7쪽, 53rd CIRP Conference on Manufacturing Systems).** 정량 데이터가 *거의 없다* — 하드 porosity 값은 **압연 전 43 %(ρ 2.53 g/cm³) 단 하나**, porosity-vs-line-load 표/곡선 **없음**. 대부분 **정성적 파라미터 스크리닝**(EEPA plasticity ratio·surface energy, Bonding 임계응력)과 **3-모듈 공정-설계 USER TOOL 콘셉트**. 즉 **이 논문의 무게중심은 *역학 결과*가 아니라 *공정-파라미터를 예측하는 도구의 아키텍처***다.
>
> ★ **계보·자리매김 — LIB-calendering DEM 4번째 peer(우리 litdb 안):**
> - **Sangrós 2019/2020 (TU Braunschweig, Powder Tech / Energy Tech)** = *소재·전도도* 초점. Thornton–Ning 탄소성 + bond + 나노압입 YR + (2020) σ_el·σ_ion 균질화.
> - **Ngandjong 2021 (Franco/LRCS, ARTISTIC)** = 슬러리→건조→압연→전기화학 *멀티스케일 디지털 트윈*. GH+SJKR, FEM.
> - **Lyu 2025 (Shanghai)** = 건조+압연을 *한 DEM*에. PFC3D, fluid-substitution.
> - **본 논문 Schreiner 2020 (TU Munich, Institut für Werkzeugmaschinen und Betriebswissenschaften iwb)** = ★ *기계·생산공학(machine/process)* 초점. **상용 EDEM** + **EEPA** + **Bonding**, 그리고 **공정 파라미터를 *예측*하는 USER TOOL**(압력·온도·압연속도·calender 사양 → 목표 전극물성). 본문이 Sangrós [15]를 "전도도-DEM peer"로, Schreiner et al. [17](2019, *자기 그룹의 NMC622 calendering 선행*)을 직접 인용 — **즉 같은 NMC622 calendering 라인의 *공정-설계 확장*판**.
> ⇒ 4편이 모두 **rigid 구 + CONTACT 탄소성 + bond, 형상소성 없음, 액체전해질 LIB, porosity=GOOD** = frame[5] 분업의 *네 번째 독립 확인*. 본 논문의 *유일한 진짜 lead* = **공정-파라미터 예측 도구(USER TOOL)** — 우리(와 Sangrós/Ngandjong/Lyu)가 *물성*에 집중하는 동안 이들은 *생산공정 설정*을 예측한다.

---

## 1. 한 줄 요약
**Li-ion NMC622 양극의 calendering(압연 압밀)을 *상용 DEM(EDEM/Altair)* 으로 모델링하고, 그 위에 *공정 파라미터를 추천하는 3-모듈 USER TOOL* 을 얹은 짧은 학회논문.** 핵심 3요소: ① **접촉모델 = EEPA(Edinburgh Elasto-Plastic Adhesion, Thakur 2014) + Bonding(Potyondy–Cundall 2004)** — EEPA가 탄소성(접촉 plasticity ratio λ_P로 제하 강성 = 잔류변형 표현) + 하중의존 점착(surface energy Δ_Y → f_min)을 담당하고, Bonding이 바인더(conductive additive-binder matrix CABM)를 입자-입자 가상 접촉(법선·접선 힘, **임계응력 초과 시 영구파단**)으로 표현; **나노압입(flat punch 100 µm, 0.15 µm/s)으로 Young's modulus·접촉모델을 보정**. ② **3-모듈 방법론**: (M1) 전극 모델링(소재·밀도·질량분율 → 입자 충전, control volume 250 µm²·생성높이 120 µm·56 µm로 trim), (M2) 시뮬 파라미터 보정(compaction resistance·initial cohesion·elastic spring-back), (M3) **USER TOOL** = 압력·온도·압연속도·calender 사양 공간에서 *목표 전극물성(두께·밀도·porosity)을 주면 적절한 calendering 파라미터를 역으로 추천*. ③ **calender 기하(roll ~400 mm)를 roll SECTION으로 모델**해 spring-back(탄성회복+갇힌 공기) 정량화 — roll 직경↑·압연속도↓ → de-aeration↑·소성변형비↑ → spring-back↓. **단 정량 결과는 빈약**(porosity 압연전 43 % 단일값, broken bonds ~25k–28k 정성, 나머지는 EEPA/Bonding 파라미터 스크리닝 곡선). **σ_el·σ_ion 전도도는 풀지 않음**(역학·공정만; "energy density = low-density 이온전도 vs high-density 전자전도의 trade-off"라고 *서술만*). **액체전해질 LIB**라 이온 채널 위상(pore=전도체)이 우리 ASSB(SE-network=전도체)와 정반대.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/binder/전해질) | 연구유형 |
|---|---|---|---|---|
| **David Schreiner, André Klinger, Gunther Reinhart** (Technical University of Munich — **Institute for Machine Tools and Industrial Management, iwb**, Boltzmannstr. 15, Garching) | **Procedia CIRP 93 (2020) 149–155** (53rd CIRP Conference on Manufacturing Systems; open access CC BY-NC-ND 4.0; 2023 resupply of corrected template) | 10.1016/j.procir.2020.05.158 | **NMC622** LiNi₀.₆Co₀.₂Mn₀.₂O₂ AM **95.5 wt%** + **PVDF5130 2.25 wt%** + **C65 carbon black 1.50 wt%** + **SFG6L conductive graphite 0.75 wt%** (additives+binder = **CABM, conductive additive-binder matrix**); 용매 NMP(증발). **액체전해질 LIB**(전해질 미모델 — 역학·공정만) | **DEM (상용 EDEM/Altair)** = **EEPA 탄소성 접촉 + Bonding(Potyondy–Cundall) bond** + **나노압입 보정** + **3-모듈 공정-설계 USER TOOL** |

> ★ **그룹·초점의 대비(중요):** Schreiner = **TU Munich iwb(기계공구·생산공학)** — **calendering을 *생산공정*으로** 본다(공정 파라미터 예측, ramp-up 비용 절감이 명시 목표). 반면 Sangrós = **TU Braunschweig(입자공학·BLB)** — *소재·전도도*. Ngandjong = **Franco/LRCS** — *멀티스케일 디지털 트윈*. **같은 NMC-calendering-DEM이지만 *동기*가 다름**: Schreiner는 "operator에게 calendering 파라미터를 추천하는 도구"가 목적. 본 논문이 인용하는 핵심 ref: **[15] Sangrós Giménez**(전도도-DEM peer, `papers/sangros2020_*`), **[17] Schreiner et al. 2019**(*자기 그룹의 선행 NMC622 calendering*, Batt. Prod. 2019 — 본 논문 = 그 *공정-도구 확장*), **[19] Thakur 2014**(= 우리 `papers/thakur2014_eepa_adhesive_elastoplastic_dem.md`, EEPA 원전), **[20] Potyondy–Cundall 2004**(= bonded-particle 모델 원전, Lyu도 사용하는 PFC3D bond의 출처), **[14] Parry–Tabor 1973**(PVDF 전단계수가 온도↑에 선형 감소, 150 ℃까지 — 온도-의존 압밀의 근거), **[11] Günther 2019**(calendering-유발 전극 결함 분류), **[13] Billot 2019**(접착강도 = 바인더함량·코팅두께·압연·roll온도).

## 3. 핵심 물성 (수치) — ⚠ 짧은 학회논문이라 빈약
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **압연 전 porosity** | **43 %** (ρ_coating 2.53 g/cm³) | uncompressed, NMC622 95.5:2.25:1.5:0.75 | **stated(본문)** | ★ **이 논문의 *유일한* 하드 porosity 값.** eq (1)로 계산: ε=1−ΣV_i/(A_sheet·d_coating) |
| **단면 코팅 두께 d_sheet** | **56 µm** | single-sided, 압연 전 | stated | control volume를 이 두께로 trim |
| **압연 후 porosity / 두께** | **표·곡선 없음** | — | — | ⚠ **본 논문은 porosity-vs-line-load를 *보고하지 않음*.** Fig 3/5는 *압력-변위(load-displacement)* 곡선(나노압입·압밀)이지 porosity-vs-P 아님 |
| **NMC622 PSD** | **mean d₅₀ = 7.19 µm** (log-normal, SLS) | 실측 | stated | 시뮬 최소입자 **3.4 µm**(timestep 결정; 무시된 fines <3.4 µm는 <2 vol%, 영향 무시가능), 상한 **20 µm** |
| **control volume(RVE)** | **250 × 250 µm**(edge) × 생성 **120 µm** → **56 µm**로 trim | DEM 도메인 | stated | "dynamic factory"로 일정 flow rate 입자 생성 후 trim(edge effect 회피; 조성 고정이면 재생성 불필요) |
| **나노압입 indenter** | **flat punch ⌀100 µm, 0.15 µm s⁻¹**(로딩·언로딩 동일 속도) | Young's modulus·접촉모델 보정 | stated | 침투깊이 도달 시 같은 속도로 제하 |
| **★ EEPA contact plasticity ratio λ_P** | **λ_P/PVDF-NMC=0.9, λ_P/NMC-NMC=0.8, λ_P/PVDF-PVDF=0.975** → 전부 **0.985로 점증** | EEPA 제하거동 보정 | stated(Fig 4) | ★ λ_P = 초기강성 대비 제하강성의 *고정비*; **0=완전탄성, 1=완전소성**. **NMC-NMC가 영향 최대**(접촉면적 가장 큼) |
| **★ EEPA surface energy Δ_Y** | **Δ_Y/NMC-NMC=5, Δ_Y/PVDF-NMC=20, Δ_Y/PVDF-PVDF=60 J m⁻²** | 하중의존 점착력 f_min | stated | Δ_Y↑ → 필요 압축력 급증(약간만 올리길 권고). 압축판 필요력 ∝ surface energy |
| **broken bonds** | **~25,000 → ~28,000**(압밀경로 ~30 µm) | Fig 5 (압밀 진행) | digitized(Fig 5) | ★ **추세만**. bond가 압밀 초기에 더 깨짐(임계 normal/shear 초과); EEPA가 t=0 생성 단계에 이미 일부 파괴 |
| **bond 재형성** | **없음 — 영구파단** | Bonding 모델 | stated | "once destroyed, bonds cannot reform" — Sangrós와 같은 *영구파단* 철학(Ngandjong SJKR 재형성과 대비) |
| **calender roll 직경** | **~400 mm** | 기계 | stated | 입자 ~10 µm 대비 ~40,000×. **roll SECTION만 모델**(전체 roll 모델 시 계산비 폭증) |
| **σ_el / σ_ion (전도도)** | **없음 — 미모델** | — | — | ★ 본 논문은 역학·공정만. "energy density = ion(low-ρ) vs electron(high-ρ) 전도 trade-off"는 *서술만* |
| **E_NMC (Young's modulus)** | **명시 수치 없음** | NMC622 | — | ⚠ Young's modulus를 "가장 영향 큰 파라미터"로 *먼저 보정*했다 하나 **확정값을 본문에 안 줌**(Fig 3에 "preliminary adjustment of Young's modulus"로만). cf. peer: Sangrós 142 · Lyu 142 · Ngandjong 200 GPa |

## 4. 시뮬레이션 방법 ★

### 4.0 전체 구조 — 3 모듈 (Fig 1)
**이 논문의 골격 = 3-모듈 공정-설계 방법론**(Fig 1):
- **Module 1 (Data measured → Model of the electrode)**: 입력 = 소재·밀도·질량분율(Table 1). PSD 기반으로 control volume 정의·입자 충전 → 전극 모델. 전극밀도·입자분포로 검증.
- **Module 2 (Changing parameters → Simulation parameters)**: 보정 파라미터 = **compaction resistance · initial particle cohesion · elastic spring-back · …**. 이들은 "독립적이지도 물리적으로 측정가능하지도 않은, 순수 수학모델의 조절 파라미터"라 **현미경 분석 또는 예비 시뮬로** 정함. 4 범주: compaction resistance, elastic spring-back, initial cohesion, others.
- **Module 3 (Space of parameters → USER TOOL)**: ★ **공정 파라미터 공간**(pressure·temperature·compaction rate·calender specification·…)에서 **목표 전극물성을 주면 적절한 calendering 파라미터를 추천**. roll section을 모델해 operator recommendation 생성.
⇒ **핵심 novelty = 물성 *예측*이 아니라 *공정-파라미터 역추천 도구*.** (전도도·형상소성은 다루지 않음.)

### 4.1 code / version
- **DEM = EDEM** (상용, Altair — Fig 2b 스크린샷에 "EDEM" 로고). ★ **peer 3편(LIGGGHTS·LIGGGHTS·PFC3D)과 *다른 코드***. 본문이 "applied DEM software (EDEM®)"로 명시. 압력은 **위 압축판(=압연 롤 모사)** 으로 인가, roll 직경을 **roll section**으로 포함.
- 후처리·검증 = 전극밀도 비교 + load-displacement 곡선(나노압입·압밀, Fig 3·5). **전도도/τ 솔버 없음**.

### 4.2 ★ DEM 접촉법칙 — **EEPA(Thakur 2014) + Bonding(Potyondy–Cundall 2004)**, 둘을 *따로 보정 후 결합*
**왜 EEPA인가**(5절): 전극의 **탄소성(elastoplastic) 거동** 때문. 접촉모델 = 입자간 상호작용 파라미터로 전극 거동 기술. **복잡도 절감을 위해 두 모델을 *처음엔 따로* 검토 후 결합·추가보정**:
- **EEPA (Edinburgh Elasto-Plastic Adhesion)** = ★ 입자의 **탄소성 + 하중의존 점착**. 채택 이유 = "탄소성 외에 입자간 *결합력(binding force)* 도 재현"되며, 이 결합력이 **압밀이 진행될수록**(입자가 가까워질수록) 두드러짐. **EEPA가 압연 후 *탄성 spring-back* 의 주역**[20].
  - **★ contact plasticity ratio λ_P (Fig 4):** EEPA에서 **최대압축 도달 후 제하(unloading) 거동**을 정의하는 비 = **초기강성 대비 제하강성의 고정비**. **λ_P=0 → 완전탄성, λ_P=1 → 완전소성.** 값에 따라 load-displacement 곡선의 가로축(abscissa)을 따라 *영향력 있는 이동*(=잔류 소성변형) 가능. **λ_P 증가 = 더 소성적**(제하 시 잔류변위↑). 보정: λ_P/PVDF-NMC=0.9, λ_P/NMC-NMC=0.8, λ_P/PVDF-PVDF=0.975 → 전부 0.985로 점증. **NMC-NMC 상호작용이 EEPA에 영향 최대**(NMC 입자 접촉면적이 가장 크므로, Fig 4).
  - **★ surface energy Δ_Y (하중의존 점착 f_min):** EEPA의 **조절형 점착 surface energy** = 하중의존 점착력 f_min을 정함. 사용값 Δ_Y/NMC-NMC=5, Δ_Y/PVDF-NMC=20, Δ_Y/PVDF-PVDF=60 J m⁻². **압축판 필요력 ∝ surface energy** → 실험에 맞추려면 *약간만* 올릴 것(안 그러면 최대 압축력 급증).
- **Bonding (Potyondy–Cundall 2004 bonded-particle model)** = ★ 바인더(CABM)를 **가상 접촉(virtual contact)** 으로 표현. **bond는 시뮬 첫 timestep(t=0)에 생성** — 입력 = **bond contact radius**(접촉유형별 지정, *입자 직경보다 커야* bond 생성). 두 입자의 접촉반경이 겹치면 첫 timestep 전에 bond 생성.
  - **bond 거동·파단:** 정의된 **법선·전단 임계응력 τ_Cr / σ_Cr** 초과 시 **bond 파단**. ★ **once destroyed, bonds cannot reform**(영구파단; 재형성 없음). bond는 **압밀 초기에** 주로 작용(압밀↑ → bond 더 깨짐 → 영향 감소). 역할 = **압력곡선 초기의 더 뚜렷한 상승**(bond가 힘을 흡수했다가 임계 초과 시 끊겨 *소성적 거동* 유발). EEPA가 t=0 bond 생성 단계에서 일부 bond를 *이미* 파괴.
- **결합:** EEPA(탄소성+점착) + Bonding(바인더 결합) 을 결합하고 추가 파라미터 보정. critical shear/normal stress 값이 최종 튜닝에 결정적; Young's modulus와 약하게(간접) 상관.

> ★ **층위지도 위치(중요한 정정):** EEPA는 우리 `contact_models_layer_map.md` §1에서 **A층(= no-cap 이력 LAW, Luding과 같은 층)** 이다 — **항복압(p_y/H) 캡이 *없다*.** EEPA의 "elasto-plastic"은 **piecewise-linear 이력 + plasticity ratio λ_P(제하강성비)** 이지 *경도 H로 접촉압을 cap하는* Thornton–Ning류(B층, 경로 A LAW)가 **아니다**. 즉 **Schreiner(EEPA) ≠ Sangrós/Varkey(Thornton–Ning 항복캡)** — *같은 "탄소성 접촉"이라 불려도 LAW 계열이 다름.* Schreiner의 EEPA는 우리 hooke/hysteresis와 *같은 no-cap 계열*(둘 다 캡 없는 이력 소성).

### 4.3 ★ 입자 처리 (DEM판 "무질서 처리")
- **구만** (NMC622 = 강체 구). SEM(Fig 2c, 4000× zoom)으로 **NMC 입자가 binder·carbon black matrix에 박혀 있음**을 보여 "구형 가정"을 *정성적으로* 검증. **rigid 입자 + EEPA CONTACT 탄소성(λ_P 제하비) + Bonding bond**. **입자 형상 안 변함** — λ_P/Δ_Y/bond는 *접촉·결합* 레벨이지 *형상흐름* 아님(δ=소성 기하 프록시). **형상소성·void-fill 없음**(= frame[5]에서 우리 MPM이 메우는 절반).
- **CABM(바인더+도전제)은 *개별 입자로 안 그림*:** ★ "conductive additives(C65·SFG6L)와 binder는 *개별적으로 표현하지 않음*. 도전제·바인더가 CABM에 통합되거나 NMC622 입자 *주위에 배치*되므로 그 편차는 무시가능"이라 명시 → **CABM = NMC 표면/사이의 *암묵적* matrix + Bonding bond**(별도 입자상으로 안 잡음). ⇒ **Ngandjong/Lyu(CBD를 *명시 별도 입자상*으로)와 다른 단순화** — Schreiner는 CABM을 *bond로만* 표현.
- **파쇄(fracture)는 미모델** — bond 파단만(입자는 영원한 구). 본문이 "CAM 입자가 anode보다 단단 → 더 큰 힘이 입자-입자 *재배열*(입자마찰 동반)을 일으킨다"[16,17]고 *재배열* 메커니즘만 언급(입자 깨짐 아님).
- **초기구조 생성**: "dynamic factory"가 일정 flow rate로 control volume(250²×120 µm)에 입자 생성 → 56 µm로 trim. **조성 고정이면 입자생성 1회로 재사용**(layer 두께만 바뀌면 trim만 다시) — *공정-도구 효율* 설계.

### 4.4 도메인/RVE / calendering BC / 나노압입 보정 / 압력·온도
- **control volume = 250 × 250 µm(edge) × 생성 120 µm → 56 µm trim.** side는 boundary condition 가정(=주기경계 추정). trim으로 입자생성의 통상적 edge effect 회피.
- **calendering BC:** 위 **압축판**(=압연 롤)이 하강해 압밀. ★ **USER TOOL의 핵심 가정:** roll의 탄성변형 무시 → **이론적 roll gap = 압밀 중 최소 전극두께**. 전극이 roll gap을 통과하면 **탄성 변형 입자 회복 + 갇힌 공기(trapped air)** 로 **spring-back**. spring-back은 **roll 직경·압연속도 의존** → **roll 직경↑·압연속도↓ → de-aeration↑ → 소성변형비↑ → spring-back↓**[21]. roll을 **roll SECTION**으로 모델(전체 roll은 입자 10 µm vs roll 400 mm 차수차로 계산 불가).
- **나노압입 보정(5절, Fig 3):** flat punch ⌀100 µm, 0.15 µm s⁻¹로 단일점 load-displacement 측정 → **Young's modulus를 *먼저* 보정**(가장 영향 큼; 단 ⚠ Young's modulus↑ → Rayleigh wave↑ → timestep↓·계산비↑ → 신중히). 이어 EEPA·Bonding 접촉모델 보정.
- **압력·온도 범위:** USER TOOL의 파라미터 공간 = pressure·temperature·compaction rate·calender specification. ⚠ **구체적 압력 sweep 값은 본문에 표/곡선으로 없음**(Fig 3·5 가로축 = 압밀경로 µm, 세로축 = 압밀압력 MPa이나 *그 곡선이 특정 line-load와 매핑된 표는 없음*). 온도는 *defaults·향후과제*로만(Parry–Tabor [14] PVDF 전단계수 온도의존 인용).
- **seeds:** 명시 없음(단일 RVE 추정).

### 4.5 전달 솔버
- **없음.** 본 논문은 σ_el·σ_ion·σ_thermal·τ 어느 것도 풀지 않는다. "target electrode density = good ion conductivity(low density) ↔ high electrical conductivity(high density)의 conflict"[7]라고 *서술만* 하고, 전도도를 *계산하지 않는다*. (전도도-DEM은 인용 [15] Sangrós의 몫.) ⇒ frame[5]의 "DEM=전달"에서 **σ 솔버 부분이 본 논문엔 *전무*.**

### 4.6 후처리 지표
- **porosity (eq 1):** `ε_coating = 1 − ΣᵢⁿVᵢ / (A_sheet · d_coating)` — V_i = 각 성분 이론부피(측정질량 × 성분함량 ÷ crystal density). 압연 전 43 %만 보고.
- **broken bonds:** 압밀경로 따라 깨진 bond 수(Fig 5, ~25k–28k). compaction resistance·spring-back 진단.
- **load-displacement 곡선:** 나노압입(Fig 3)·압밀(Fig 3·5)의 압력-변위. EEPA λ_P(c)·Young's modulus(b)·critical stress(a)가 곡선의 어느 부분을 지배하는지 분해(Fig 5 캡션).
- ⚠ **CN·fabric tensor·FSA·내부응력·전도도 = 본 논문에 *없음*** (Sangrós 2019가 가진 풍부한 미세구조 지표가 *이 논문엔 빠짐* — 짧은 학회논문 + 공정-도구 초점).

### 4.7 특이사항/튜닝
1. **공정-파라미터 *역추천* USER TOOL** — 본 논문 고유. 물성 *예측*이 아니라 *공정 설정 추천*(목표 두께·밀도 → 압력·온도·속도). ramp-up 비용 절감이 명시 목표.
2. **EEPA + Bonding 을 *따로 보정 후 결합*** — 복잡도 절감. λ_P(제하)·Δ_Y(점착)·τ_Cr/σ_Cr(파단)을 단계적으로.
3. **나노압입으로 Young's modulus·접촉모델 보정** — Sangrós와 같은 *단일점 압입 보정* 철학(단 Sangrós는 40 입자로 YR 선형회귀, Schreiner는 flat-punch 단일 load-displacement).
4. **roll을 roll-section으로 + 관성 스케일링(inertial scaling) 언급** — 압연속도↑를 결과 왜곡 없이 가속하는 향후 방법.
5. **2023 resupply 주의:** PDF 하단에 "This is a resupply of March 2023 as the template used in the publication of the original article contained errors. The content has remained unaffected." → *내용 동일, 템플릿만 정정.*

## 5. Figure set ★ — ⚠ 짧은 논문이라 6개뿐
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | ★ **3-모듈 방법 개요**: M1(Data measured: material·density·mass fraction → Model of electrode), M2(Changing parameters: compaction resistance·initial cohesion·elastic spring-back → Simulation parameters), M3(Space of parameters: pressure·temperature·compaction rate·calender spec → **User tool**) | ★ **공정-설계 도구 아키텍처** — 우리 DEM→전달→grade와 *다른 종류*의 파이프라인(공정 파라미터 역추천). 우리 predictor(설계→물성)와 *방향 반대*(물성→공정) |
| **2** | (a) **SEM NMC622** + (b) **EDEM 모델 스크린샷**(색=입자) + (c) **SEM 4000× zoom**(NMC 입자가 binder·carbon black matrix에 박힘) | 구형 가정의 *정성* 검증(Sangrós Fig 1과 같은 역할). EDEM 로고 = 상용코드 확인 |
| **3** | ★ **NMC622 전극의 load-displacement 곡선**(압밀 전(a)·중(b)·후(c) 모식 + Experiment 곡선) — 세로 압밀압력 MPa(~0–150), 가로 압밀경로 µm(~0–30). **(a)→(b) 압축→(c) spring-back(제하 시 압력 0 아래로, 잔류변위)** | ★ **압밀 load-displacement + spring-back 시각화.** 우리 P-vs-porosity가 아니라 *P-vs-displacement*(다른 축). ⚠ porosity-vs-line-load 아님 |
| **4** | ★ **EEPA plasticity ratio λ_P 영향**: Interaction(all / purely PVDF-PVDF / purely NMC-NMC / purely PVDF-NMC) + previous simulation — 압밀압력 vs 압밀경로. **NMC-NMC 상호작용이 영향 최대**(접촉면적 큼) | ★ **λ_P(제하강성비)가 압밀곡선을 어떻게 바꾸나** — EEPA의 소성 튜닝. 우리 Stage-E/연화와 *다른 방식*의 소성 보정(접촉 제하비) |
| **5** | ★ **시뮬 vs 실험 load-displacement + broken bonds**: 빨강=sim 압밀압력, 주황=exp 압밀압력, 초록=sim broken bonds(우축, ~25k→28k). (a) shift = critical shear/normal stress·surface energy, (b) curve = Young's modulus, (c) elastic recovery = contact plasticity ratio | ★ **어느 파라미터가 곡선의 어느 부분을 지배하나** 분해(a=초기 shift, b=상승 기울기, c=spring-back). broken bonds 진화 |
| **6** | **USER TOOL 입출력 모식**: 입력 = 전극 물성 *before*·*after*(예: thickness_before/after, density_before/after) → **User tool** → 출력 = **Calendering parameters** | ★ **공정-파라미터 역추천의 입출력** — 목표 전극물성(전/후) → calendering 파라미터. 우리에 없는 *공정-도구* 콘셉트 |

## 6. Post-processing ★
- **무엇**:
  - **porosity(eq 1)**: ε = 1 − ΣV_i/(A_sheet·d_coating). 압연 전 43 %만.
  - **load-displacement 곡선**: 나노압입(보정)·압밀(검증). EEPA λ_P·Δ_Y·Young's modulus·critical stress가 곡선의 어느 부분을 지배하는지 *정성* 분해(Fig 5: shift/curve/recovery).
  - **broken bonds(Fig 5)**: 압밀경로 따라 깨진 bond 수(~25k–28k).
  - **전극밀도 비교**(M1 검증): 시뮬 입자 bed 밀도 vs 실측.
- **도구**: **EDEM**(DEM + 내장 후처리). 실험: **나노압입**(flat punch ⌀100 µm, 0.15 µm s⁻¹; Christine Burmeister·Jan-Michael Kröhnke 측정 — Acknowledgements), **SLS**(static laser scattering, PSD; Fabian Linsenmann), **SEM**. **전도도/τ/CN/fabric/FSA 후처리 *없음*.**
- **수치화·플롯·기록 방식:** 거의 *정성*. EEPA λ_P·Δ_Y·Bonding τ_Cr/σ_Cr을 *예시 파라미터 스크리닝*(Fig 4·5)으로 보임. **압력-의존 물성 시리즈(porosity-vs-line-load 표) 없음** — 이 논문은 *방법론·도구 제안*이지 *데이터 논문*이 아님.

## 7. 우리 DEM+MPM 대비 (요약표 — 정식 비교는 아래 "## 우리 DEM+MPM 대비")  →  `our_dem_baseline.md`
| 항목 | 이 논문 (Schreiner 2020, LIB 공정) | 우리 (ASSB) | 차이 / 이유 |
|---|---|---|---|
| **연구 초점** | **공정-파라미터 *예측* 도구**(USER TOOL). 역학·공정만 | 압밀(DEM·MPM) + **전달 삼중항** + grade + **물성 *예측* predictor** | ★ **방향 반대**: 그들=*물성→공정파라미터* 역추천, 우리=*설계→물성* 예측. 전도도는 그들에 *전무* |
| **DEM 코드** | **EDEM(상용, Altair)** | **LIGGGHTS(오픈소스)** | ★ **peer 유일의 상용코드**(Sangrós·Ngandjong LIGGGHTS, Lyu PFC3D). 우리와 *다른 코드* |
| **★ contact LAW** | **EEPA(Thakur 2014, no-cap 이력) + Bonding** | Luding hooke/hysteresis(no-cap) + Stage-E | ★ **둘 다 no-cap 계열**(층위지도 A층). EEPA λ_P(제하비) ↔ 우리 k₁/k₂ 이력. **항복캡 없음**(Sangrós/Varkey의 Thornton–Ning *항복캡*과 *다름*) |
| **★ 소성 종류** | **EEPA CONTACT 탄소성**(λ_P 제하강성비, δ 프록시) | MPM 진짜 SHAPE 소성(J2) + DEM hooke/hysteresis | **입자 형상 안 변함**(DEM). EEPA는 *접촉 제하* 소성이지 *형상흐름* 아님. **형상변화 = 우리 MPM 고유** |
| **★ 바인더 모델** | **CABM = *암묵적* matrix + Bonding bond**(영구파단), 별도 입자상 *아님* | CBD = Stage-2 부피점유; 명시 bond 없음(backlog A3) | ★ **Schreiner = bond-only(입자상 안 그림)** — Ngandjong/Lyu(명시 CBD 입자상)보다 단순. 우리 CBD 명시화의 *또 다른* 청사진(bond만) |
| **압밀 모드** | **calendering**(압연 line-load, 압축→spring-back) | **cold-press**(단축 hold) | LIB 압연 ≠ ASSB 프레싱. **그들 spring-back 정량(roll-section), 우리 static** |
| **압력대** | **저압 calendering**(Fig 3 ~0–150 MPa, 단 line-load 표 없음) | **~300–500 MPa**(고압 cold-press) | 압력대 다름. ⚠ 게다가 *porosity-vs-P 데이터 자체가 없어* 직접 비교 불가 |
| **E_AM** | **명시 수치 *없음***("Young's modulus 보정" 만, 값 미공개) | E_CAM **140 GPa**(고정) | ⚠ peer는 다 줌(142/142/200) — Schreiner만 *미공개* |
| **검증** | **나노압입 load-displacement**(정성 fit) + 전극밀도 | solver=ground truth(Minnmann·Cronau·Bazzoun 외부 앵커) | 그들 = *공정-도구 검증*(곡선 형태). porosity-vs-P 실측 *시리즈 없음* |
| **이온 채널 위상** | (미모델 — LIB라 pore=전도체 전제) | **SE 입자망=전도체** Kirchhoff/Holm | 위상 정반대(전도도 안 풀어 *암묵적* 전제만) |
| **소재** | **NMC622 + 액체전해질**(LIB) | **LPSCl SE + NMC811**(ASSB) | **다른 셀 화학** → 절대값 직접 전이 금지 |

> ★★★ **위 표는 아래 "## 우리 DEM+MPM 대비"에서 모두 풀어 씀**(사용자 mandatory). §7은 요약표.

### frame[5] 위치
- **이 논문 = 전달/패킹 측의 *역학·공정 부분만*, 그것도 *얕게***. rigid 구 + EEPA(no-cap 탄소성) + Bonding bond → 압밀 load-displacement·spring-back. **입자 형상소성·void-fill 없음** — 우리 MPM이 메우는 그 절반이 빠짐(Sangrós·Ngandjong·Lyu·Varkey·Bazzoun과 동일, **LIB-제조 DEM의 네 번째 독립 확인**). **게다가 σ 솔버도 *전무*** (Sangrós 2020/Ngandjong은 적어도 σ를 줬는데 Schreiner는 *0채널* — Lyu와 같은 "σ 안 줌" 그룹, 단 Lyu는 *정성 논증*이라도 했음).
- **우리 우위 = (i) 전달 삼중항 명시 솔버, (ii) MPM 형상소성** 둘 다 본 논문에 *전무*. 본 논문의 *유일 lead* = **공정-파라미터 예측 USER TOOL**(우리 미보유 — 단 우리 predictor는 *반대 방향* 설계→물성).

---

## ★ 우리 DEM+MPM 대비 (comparison vs ours)

> 사용자 mandatory 섹션 A. 그들 LIB calendering DEM(EDEM+EEPA+Bonding, 공정-도구) vs 우리 ASSB cold-press DEM(LIGGGHTS hooke/hysteresis+Stage-E+18× 연화) + MPM; 그들 σ 0채널 vs 우리 Kirchhoff/Holm 삼중항; LIB pore=전도체 위상 vs 우리 SE-network=전도체 위상역전; 그들 contact LAW(EEPA, no-cap) vs 우리(hooke/hysteresis, no-cap).

### A-1. 접촉·압밀 머신: 같은 rigid-sphere DEM, 같은 *no-cap* 계열, 형상 불변 (공통) — 단 코드·LAW 변종 다름
- **그들**: EDEM(상용), 입자 = 강체 구(NMC622, d₅₀ 7.19 µm), 접촉 = **EEPA(Thakur 2014)** = piecewise-linear 이력 탄소성(제하강성비 λ_P) + 하중의존 점착(surface energy Δ_Y) + **Bonding(Potyondy–Cundall)** bond(영구파단).
- **우리**: LIGGGHTS, 입자 = 강체 구(AM_P/AM_S/SE), 접촉 = **Luding hooke/hysteresis**(k₁ 로딩 / k₂ 언로딩 / k_c 점착) + **Stage-E**(Tabor+volume 소성 접촉면적 재유도) + **E_SE 18× 연화**(real 24 → 1.35 GPa).
- **★ 같은 층, 다른 변종(층위지도 정밀):** EEPA와 hooke/hysteresis는 **둘 다 `contact_models_layer_map.md` §1의 A층(= no-cap 이력 LAW)** 이다 — **항복압 캡 없음.** EEPA의 λ_P(제하강성비)는 우리 k₂/k₁(언로딩/로딩 강성비)와 *기능적으로 같은 역할*(이력 잔류변형 표현). Δ_Y(점착)는 우리 k_c/`--coh`와 대응. ⇒ **Schreiner의 EEPA는 우리 모델의 *상용-코드 사촌*** — 둘 다 캡 없는 이력 소성, 형상 불변. ⚠ 단 **Sangrós/Varkey의 Thornton–Ning(항복압 p_y 캡, B층=경로 A LAW)과는 *다른 계열*** — "탄소성 접촉"이라 같은 이름이어도 Schreiner는 *no-cap*(우리 편), Sangrós는 *cap*(경로 A).
- **공통 한계(frame[5])**: 둘 다 **입자 형상 안 변함**(δ=소성 기하 프록시). Schreiner도 Sangrós·Ngandjong·Lyu·Varkey·Bazzoun처럼 *rigid-sphere + CONTACT-레벨*이라 **morphology/void-fill 절반이 빠짐** → **우리 MPM(J2 진짜 SHAPE 소성)이 메우는 칸**. **LIB-제조 DEM 6편 연속 같은 한계** = frame[5] 분업이 분야 공통 구조임을 여섯 번째 독립 확인.
- **차이점(우리 후처리 우위)**: Schreiner는 접촉면적 후보정 없음(EDEM 내장 EEPA 접촉). 우리는 **Stage-E**로 *소성 접촉면적*을 명시 재유도 → 전도도 솔버 입력 정밀화. Schreiner엔 이 층이 *없음*(σ를 안 풀어 불필요했음).

### A-2. ★★ σ(전도도): 그들 **0채널** vs 우리 Kirchhoff/Holm **수치 삼중항** — 우리 *가장 큰* 우위
- **그들**: ★ **σ_el·σ_ion·σ_thermal 어느 것도 풀지 않는다.** "target density = ion 전도(low-ρ) vs electron 전도(high-ρ)의 trade-off"[7]라고 *한 문장 서술*하고 끝. **Bruggeman도, RNM도, FEM도, 정성 논증조차 없음**(Lyu는 *정성 논증*이라도 했는데 Schreiner는 그조차 *전무* — 공정-도구가 목적이라 σ가 scope 밖). 전도도-DEM은 인용 [15] Sangrós의 몫이라 *위임*.
- **우리**: **명시 Kirchhoff 망**(Σ(φi−φj)/R=0) + **Holm 구속저항**(R=1/(2σr_c), 1967) + **Stage-E 소성 접촉면적** → **σ_ionic·σ_electronic·σ_thermal 삼중항을 *수치로*** 산출 + **LOOCV 스케일링 법칙 압축**(σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.903).
- **대비의 의미**: **이게 우리 transport novelty가 *가장* 선명한 peer.** Schreiner는 "압밀↔전도도 trade-off"를 *서술만* 하는데, 우리는 *같은 압밀 구조에서 Holm 구속저항으로 σ를 3채널 풀어* 수치를 준다. **Sangrós(균질화)·Ngandjong(FEM)은 σ 수치를, Lyu는 정성 논증을 줬는데, Schreiner는 *그조차 안 줌*** → **Schreiner 대비 우리 transport 우위는 4 peer 중 *최대***(σ가 완전 부재). ⚠ 정직: Schreiner의 *목적*은 *공정-파라미터 도구*지 transport가 아니었음 — "그들이 못 했다"가 아니라 "그들 scope(공정-설계) 밖, 우리 scope(transport) 안". 이 칸의 정확한 frame[5] 진술 = "Schreiner = 공정-설계 도구 / 우리 = transport+morphology 물성예측 — *상보적이되 겹치지 않는 목적*."

### A-3. ★★ 이온 채널 위상 역전 — LIB pore=전도체(암묵적 Bruggeman) vs ASSB SE-network=전도체(Holm)
- **LIB(이 논문)**: 활물질·CABM은 절연/혼합 매트릭스, Li⁺는 **공극을 채운 액체전해질**로 흐름(본문 미모델이나 [7] "low density = good ion conductivity"로 *명백히 전제* — 공극↑ → 이온↑). → 이온 전도체 = **공극상**, **porosity = GOOD**. 압밀의 trade-off("target density is subject to a conflict between good ion conductivity (low density) and high electrical conductivity (high density)")가 *그대로 LIB 위상의 정의*.
- **우리 ASSB**: 액체전해질 없음. Li⁺는 **SE 입자 접촉망**으로만 → **공극 = 순수 방해물**, σ_ionic = SE-SE 구속저항(Holm). **압밀↑ → SE 접촉↑ → σ_ionic↑**. **porosity = BAD**(~10 % 목표).
- **위상 정반대의 발현**:
  - **목표함수**: Schreiner/LIB는 **porosity를 *남겨야*** 한다(낮추면 이온전도↓; high-ρ면 전자↑·이온↓ trade-off). 우리 ASSB는 **porosity 최대 제거**(~10 %).
  - **압밀 방향성**: 압밀↑ → **LIB σ_ion↓**(공극↓) vs **ASSB σ_ionic↑**(SE접촉↑). **부호 반대.**
- **→ 깔끔한 대조(Sangrós·Ngandjong·Lyu 대비와 동일 축, *네 번째* LIB peer로 보강)**: "액체전해질 LIB calendering에서는 *공극*이 이온 전도체라 밀도가 *good-ion / good-electron* 사이의 conflict[7]를 만드는 반면(Schreiner의 *바로 그* 설계 문제), all-solid-state 전극에서는 *고체전해질 입자망*이 이온 전도체라 porosity가 *순수 방해물*이고 압밀↑→σ_ionic↑이다 — Schreiner가 calendering을 *trade-off 최적화*로 푸는 이유가 우리 ASSB가 *최대 압밀*을 추구하는 이유의 거울상이다." **Schreiner·Sangrós·Ngandjong·Lyu 4편이 같은 위상역전을 LIB쪽에서 독립 확인** → 우리 SE-network 솔버 존재이유의 4중 정당화.

### A-4. ★ 공정-파라미터 *예측* 도구 — 우리 predictor와 *방향 반대*
- **그들 USER TOOL**: 입력 = **목표 전극물성**(두께·밀도 *전/후*), 출력 = **calendering 파라미터**(압력·온도·압연속도·calender 사양). 즉 ***물성 → 공정 설정* 역추천**. 목적 = operator 추천 + ramp-up 비용 절감(생산공학 관점).
- **우리 predictor(Phase 3–4)**: 입력 = **설계 knobs**(조성·PSD·압력·두께), 출력 = **전체 물성 세트**(σ 삼중항·porosity·coverage·grade) → 나아가 *2D 미세구조 합성*. 즉 ***설계 → 물성* 예측**.
- **대비의 의미**: ★ **방향이 정반대.** Schreiner는 "이 물성을 원해 → 압연을 어떻게 설정?", 우리는 "이 설계를 넣으면 → 물성이 뭐?". **둘은 상보적**(서로의 역함수 비슷) — *우리 predictor에 inverse-design(목표 물성 → 설계/공정) 모드를 추가*한다면 Schreiner의 USER TOOL이 *그 컨셉의 LIB 선례*. ⚠ 단 Schreiner는 *공정* 파라미터(압력·온도·속도), 우리 predictor는 *설계* 파라미터(조성·PSD) — 변수 종류가 다름. 또 Schreiner USER TOOL의 *내부*는 여전히 위 EEPA-DEM(σ 없음, 형상 없음)이라 *예측 물성의 깊이*는 우리가 압도(σ 삼중항·morphology). **Schreiner의 lead = *공정-도구 아키텍처(inverse, 생산공학)*, 우리 lead = *예측 물성의 풍부함·정확도*.**

### A-5. 압밀 곡선·spring-back·검증
- **압밀 곡선**: Schreiner Fig 3·5는 **load-displacement**(압밀압력 vs 압밀경로 µm)이지 **porosity-vs-line-load가 *아니다*.** ⚠ **porosity-vs-P 표/곡선이 *전혀 없어* 우리 Heckel(P_y=138)·P-vs-porosity와 *직접 비교 불가*** — Sangrós/Ngandjong/Lyu는 적어도 porosity-vs-P 곡선을 줬는데 Schreiner는 *압밀압력-변위*만. 정성 형태(저압 압축 → spring-back)만 우리 압밀과 대응.
- **spring-back**: Schreiner는 **roll-section 모델 + roll 직경/속도 의존**(roll↑·속도↓ → de-aeration↑ → spring-back↓)으로 spring-back을 *정성 논의*. Sangrós 2019는 ER 10.25→17 %를 *정량*했는데 Schreiner는 *정량값 없이* 기계-파라미터 의존성만. **우리는 spring-back 미보유**(static hold) — Schreiner의 roll-section 의존성은 *공정* 관점의 추가 정보(우리 MPM unload로 정량화 가능하나 현재 없음).
- **검증 깊이**: Schreiner = 나노압입 load-displacement *정성 fit* + 전극밀도. **porosity-vs-P 실측 시리즈·전도도 실측 *없음*.** 우리 = Minnmann porosity·Cronau overlap·Bazzoun σ_ionic·SEM morphology 다중 앵커. ⚠ 둘 다 LIB/ASSB로 절대값 직접 전이 금지.

---

## 적용가능성 (applicability to our LIGGGHTS DEM model)

> 사용자 mandatory 섹션 B. 그들 EEPA/Bonding contact 처리 + 공정-도구가 우리 LIGGGHTS 모델/backlog에 줄 수 있는 것(있다면); LIB-vs-ASSB caveat; 우리 scripts/knobs에 매핑.

### B-1. EEPA contact LAW — 우리 hooke/hysteresis의 *상용-코드 사촌*(직접 흡수 불요, *대조·정당화*)
- **현재 우리**: LIGGGHTS hooke/hysteresis(k₁/k₂/k_c). LIGGGHTS는 EEPA 변종도 지원하나 우리는 hooke/hysteresis 사용.
- **Schreiner가 주는 것**: **EEPA(Thakur 2014)** = piecewise-linear 이력 + **plasticity ratio λ_P(제하강성비)** + **하중의존 점착(Δ_Y → f_min)**. ★ **λ_P ↔ 우리 k₂/k₁, Δ_Y ↔ 우리 k_c** — *기능적으로 같은 노브*. 즉 **Schreiner의 EEPA 파라미터화는 우리 hooke/hysteresis 보정의 *상용-코드 평행 사례***(다른 코드·다른 이름, 같은 no-cap 이력 소성 물리).
- **→ 흡수 판단**: ★ **직접 흡수할 새 물리는 *거의 없음*** (EEPA는 우리와 같은 A층). 가치 = **(i) 정당화** — "no-cap 이력 탄소성 + 제하강성비 + 하중의존 점착"이 *상용 EDEM에서도* LIB calendering 표준임을 보임(우리 hooke/hysteresis 선택이 outlier가 아님); **(ii) λ_P 보정 철학** — Schreiner가 **NMC-NMC 상호작용에 λ_P 영향 최대**(접촉면적 큼)라 *상-쌍별로* λ_P를 다르게 준 것은, 우리가 AM-AM/AM-SE/SE-SE에 *상-쌍별* 이력 파라미터를 줄 때의 선례. ⚠ 단 **EEPA도 *항복캡 없음*** → 경로 A(real E + p_y 캡)에는 *부적합*(Thornton–Ning이라야 함). EEPA는 우리 *현행* 모델 편(no-cap 연화)의 사촌이지 *경로 A* 편이 아님.

### B-2. Bonding(Potyondy–Cundall, 영구파단) — CBD 명시화의 *또 다른* 청사진(bond-only) → backlog A3
- **현재 우리**: CBD = Stage-2 부피점유, 명시 bond 없음(backlog A3).
- **Schreiner가 주는 것**: **Bonding = Potyondy–Cundall bonded-particle**(t=0 생성, bond contact radius > 입자직경, **임계 normal/shear 응력 초과 시 영구파단**). ★ **CABM을 *별도 입자상 없이* bond로만** 표현(NMC 표면/사이의 암묵적 matrix + bond). ⇒ **Ngandjong/Lyu(명시 CBD 입자상)보다 *더 단순한* 청사진** — "바인더를 입자로 그리지 말고 *bond로만*".
- **4개 CBD 청사진 비교(우리 선택지, Lyu 디제스트의 3개에 Schreiner 추가):**
  | 모델 | bond 물리 | 파단 | 입자상 | 우리 적용 |
  |---|---|---|---|---|
  | **Sangrós 2019/2020** | 점-bond(법선·접선 힘, 강성 6e12 N/m³) | **영구파단**(2e13 N/m²) | bond-as-link | 단순·검증됨; 모멘트 無 |
  | **Ngandjong 2021** | SJKR 점착(CED×A) | **끊김·재형성**(reversible) | **명시 CBD 입자** | PTFE cold-weld(`--coh`)에 직결 |
  | **Lyu 2025(PFC3D)** | **parallel bond(힘+모멘트)** vs contact bond(힘) | breakdown stress, open | **명시 CBD 입자** | **모멘트 전달 = 섬유망 휨강성**에 최적 |
  | **Schreiner 2020(EDEM)** | **Potyondy–Cundall bond**(법선·전단 힘) | **영구파단**(τ_Cr/σ_Cr) | ★ **bond-only(입자상 없음)** | ★ **가장 단순** — CABM을 *입자 안 그리고* bond로만 |
- **→ LIGGGHTS 매핑**: ★ **Schreiner의 "bond-only CABM"은 우리 *현행* Stage-2 부피점유에 *가장 가까운 다음 단계***. LIGGGHTS `bond` fix(Potyondy–Cundall류 — Schreiner의 [20]이 바로 그 원전)로 **SE-SE(또는 CBD-걸친) bond를 *입자상 추가 없이* 얹을 수 있음**. ⚠ 단 **영구파단**(Schreiner·Sangrós) vs **재형성**(Ngandjong SJKR) 선택 필요 — PTFE cold-weld(`--coh`)는 *재형성* 쪽이 더 맞음(섬유 재접촉). ⇒ **PTFE에는 Ngandjong/Lyu(재형성·모멘트)가 물리적으로 더 적합**하고, **Schreiner의 bond-only는 *구현 단순성*이 장점**(입자수 안 늘림 → OOM/CFL 부담 없음 = 우리 scaffold AM-freeze 정신과 같은 "물리 추가 없이 효과만" 접근). **Schreiner 청사진의 가치 = *최소 구현*(bond-only, 영구파단) 버전.**

### B-3. 공정-파라미터 USER TOOL — 우리 predictor에 *inverse-design* 모드의 LIB 선례
- **Schreiner USER TOOL**: 목표 전극물성(두께·밀도) → 공정 파라미터(압력·온도·속도) *역추천*. roll-section 모델로 spring-back 보정.
- **→ 우리에게**: ★ **우리 5-phase 로드맵의 Phase 3–4(predictor: 설계→물성→2D synth)는 *forward*** 인데, Schreiner는 *inverse*(목표→설정). **만약 우리가 "원하는 σ_ionic·porosity를 주면 → 필요한 조성·PSD·압력을 역산"하는 inverse-design 모드를 넣는다면, Schreiner USER TOOL이 그 *아키텍처 선례*** (Module 3 = 파라미터 공간 + 목표물성 → 추천). ⚠ 단 변수 종류 다름(Schreiner=*공정* 압력·온도·속도, 우리=*설계* 조성·PSD) + 그들 도구 *내부*는 σ-없는 EEPA-DEM이라 *예측 깊이*는 우리가 압도. ⇒ **흡수할 것 = *inverse 도구 컨셉*(목표→설계 역산)**; *내용*(EEPA·σ-부재)은 안 가져감.

### B-4. 나노압입 보정 — Sangrós와 같은 단일점 압입(우리 σ_y anchor 후보, 약하게)
- **Schreiner**: flat-punch ⌀100 µm로 단일점 load-displacement → Young's modulus·접촉모델 보정. ⚠ 단 **Young's modulus 확정값을 본문에 *안 줌*** + YR 같은 *입자-레벨* 항복비 추출도 안 함(Sangrós 2019의 40-입자 YR 선형회귀가 *더 직접적*).
- **→ 우리에게**: 우리 σ_y(lit range 0.05–0.30)를 *입자 실측*으로 anchor하려면 **Sangrós 2019의 40-입자 YR 방법이 *더 나은* 청사진** — Schreiner의 단일점·값-미공개는 *약한* 선례. ⇒ **Schreiner의 압입은 "상용-코드도 압입 보정을 쓴다"는 정당화 정도**(우리 σ_y anchor 방법은 Sangrós를 따를 것).

### B-5. dry-ASSB vs wet-LIB — 종합 정리
- **우리가 가져갈 것**: ① **bond-only CABM(B-2)** — *최소 구현* CBD bond 청사진(backlog A3; 입자수 안 늘림 = scaffold 정신); ② **inverse-design 도구 컨셉(B-3)** — 목표→설계 역산(우리 predictor 확장 *아이디어*).
- **우리가 안 가져갈 것**: ① EEPA LAW(B-1) — 우리 hooke/hysteresis와 같은 층, 새 물리 없음(대조·정당화만); ② σ(전무) — 우리가 압도; ③ 형상소성(없음) — 우리 MPM; ④ Bruggeman/pore-이온(위상역전) — 우리 SE-network와 반대; ⑤ porosity GOOD 목표 — 우리 BAD; ⑥ EEPA λ_P 절대값·Δ_Y·τ_Cr — NMC622-CABM 보정값이라 LPSCl-PTFE로 직접 전이 불가(*형태/철학*만).
- **결론**: Schreiner는 **4 LIB-peer 중 *우리에게 가장 덜 직접적*** — 그들의 *진짜 산출*(공정-도구)은 우리 물성-예측과 *목적이 달라* 겹치지 않고, contact LAW(EEPA)는 우리와 *같은 층*이라 새 물리가 없으며, σ·형상소성은 *전무*. **흡수 가능한 두 조각 = (i) bond-only CABM 최소구현(A3), (ii) inverse-design 도구 컨셉**. *나머지는 frame[5]/위상역전 대조·정당화용.*

---

## ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this DEM model)

> 사용자 mandatory 섹션 C. 사용자가 firm한 DEM novelty를 원함 — **우리가 SOTA임을 분명히 주장.** 7개 차별점을 Schreiner 2020 대비 매핑. 정직하게 그들이 앞서는 칸(공정-도구)도 명시. evidence-based; LIB-not-ASSB scope 명시.

> **결론 먼저: Schreiner 2020은 LIB calendering의 *공정-설계 도구*로서 가치 있는 학회논문이지만, 물성-시뮬레이션의 거의 모든 축에서 우리가 압도적으로 SOTA를 앞선다.** 본 논문은 **σ 0채널**(전도도 *전무* — Sangrós/Ngandjong은 σ를, Lyu는 정성 논증이라도 줬는데 Schreiner는 그조차 없음), 입자는 **형상불변 강체 구 + EEPA(no-cap CONTACT 탄소성)**, 정량 데이터는 **porosity 43 % 단 하나**(porosity-vs-P 표 없음), **LIB(NMC622 + 액체전해질)** 다. 우리 7개 차별점을 그들이 *하는 것/없는 것*에 매핑한다(증거 기반: 그들 σ-부재·구-형상·LIB-범위·데이터-빈약).

**(1) 전달 삼중항 σ_ionic + σ_e + σ_thermal — 명시 Kirchhoff/Holm 접촉망 솔버 (★ *압도적 최대* 우위 — 이 peer는 σ가 *완전 부재*)**
- **그들**: 전도도를 **전혀, 어떤 형태로도 풀지 않는다.** "density = ion(low-ρ) vs electron(high-ρ) trade-off"[7] *한 문장*이 전부. **Bruggeman도 RNM도 FEM도 정성 논증조차 없음.**
- **우리**: **3채널 모두**(σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.903), **명시 Kirchhoff Σ(φi−φj)/R=0 + Holm R=1/(2σr_c) 구속저항 + Stage-E 소성 접촉면적**. ⇒ **4 LIB-peer 중 σ-우위가 *최대*** (Schreiner는 σ가 *0*; Sangrós 균질화·Ngandjong FEM·Lyu 정성보다도 *더 부재*). **삼중항·명시망·구속저항 = 명백한 우리 SOTA.**

**(2) Stage-E 소성 접촉면적 재유도**
- **그들**: 접촉면적 = EDEM 내장 EEPA 접촉(기하). 소성 pile-up·Tabor 면적 재유도 *없음*(σ를 안 풀어 불필요).
- **우리**: **Stage-E(Tabor F/H + volume V/h 소성 접촉면적)** 로 elastic 접촉면적을 *소성 면적으로* 재유도 → σ 구속저항 입력 정밀화. **그들엔 이 층 자체가 없음.**

**(3) DEM↔MPM scaffold 커플링 + 진짜 소성 MORPHOLOGY (J2)**
- **그들**: 입자 = **영원한 강체 구**(δ=기하 프록시). **형상변화·void-fill 없음.** CABM도 *입자로 안 그림*(암묵적 matrix). 입자 *재배열*[16,17]만 언급(형상 아님).
- **우리**: **MPM 진짜 J2 소성 형상변화**(SEM 코어보존+경계평탄화 ✓), **부피보존 void-fill flow**, **DEM AM 골격 + SE만 MPM(scaffold)** 커플링. 그들이 가진 *것이 없는* 형상 거동을 우리 MPM이 메움(frame[5]). **형상소성 = 우리 고유.**

**(4) fracture-aware transport (Auerbach + Lawn)**
- **그들**: 입자 파쇄 **미모델**(bond 파단만; 입자는 안 깨짐). 고압 파쇄 언급조차 *없음*(Sangrós/Lyu는 한계로 언급했는데 Schreiner는 *재배열*만).
- **우리**: **Auerbach 임계 + Lawn 미세균열 → fracture-aware Holm**(f_intact로 σ 부분전도 보정). 깨진 접촉도 ~60 % 미세접촉 유지를 σ에 반영. **그들 bond 파단(역학)과 달리 우리는 파쇄를 *전달*에 연결.**

**(5) 문헌-근거 σ_grain (Cronau)**
- **그들**: σ_ion = *미계산*. SE 입계·crystallinity 인자 해당 없음(LIB라 SE 없음, 게다가 σ 안 풂).
- **우리**: **σ_grain=3.0 mS/cm × Cronau(r_SE)** — 단결정 문헌값 + sub-µm amorphization 인자(입계 의존). ASSB SE 고유 — 그들 LIB에 해당 없음 + σ 자체 부재.

**(6) 실험-앵커 독립 듀얼모델 frame[4]/[5]**
- **그들**: **단일 DEM 모델**(나노압입·전극밀도 보정). 독립 2모델 교차검증 없음.
- **우리**: **DEM(전달) + MPM(역학)** 을 *각각 독립적으로 실험에 보정*(Minnmann·Cronau·Bazzoun) — **서로 cross-fit 안 함**(frame[4]). 수렴=교차검증, 발산=정량화된 모델한계. **본 논문은 단일 모델이라 이 메타-검증 구조 없음.**

**(7) 솔버→스케일링 법칙 LOOCV 압축 + 물성-예측 predictor**
- **그들**: 미세구조 → 물성을 *닫는 식 없음*(σ를 안 풀어 압축할 대상조차 없음). 그들 도구는 *공정 파라미터*를 추천(물성 예측 아님).
- **우리**: 네트워크 솔버 출력 → **스케일링 법칙(LOOCV 0.90–0.98) + grade_engine** + **물성-예측 predictor**(설계→물성→2D synth). **그들 공정-추천 ≪ 우리 물성-예측 깊이.**

**⚖️ 정직하게 — 그들이 우리보다 앞선 곳:**
- **① 공정-파라미터 *역추천* USER TOOL (생산공학)**: Schreiner의 진짜 lead. 목표 전극물성 → calendering 파라미터(압력·온도·속도) 추천 + ramp-up 비용 절감. **우리 predictor는 *forward*(설계→물성)** 라 *inverse 도구*는 미보유 — Schreiner가 그 *컨셉의 LIB 선례*(우리가 inverse-design 모드를 넣는다면 따를 아키텍처). ⚠ 단 그 도구 *내부*는 σ-없는 형상-없는 EEPA-DEM이라 *예측 깊이*는 우리가 압도.
- **② calender 기계-모델(roll-section, spring-back의 roll 직경/속도 의존)**: Schreiner는 *압연 기계 자체*(roll 직경 400 mm, 압연속도, de-aeration)를 모델 — 우리는 *cold-press static*이라 기계-공정 변수 없음. **기계-공정 모델링은 그들 영역**(생산공학). ⚠ 단 spring-back *정량값*은 Sangrós 2019(ER 17 %)가 줬지 Schreiner는 *정성 의존성*만.
- **③ 상용 EDEM의 검증된 파이프라인 성숙도**: 상용코드라 GUI·후처리·산업 채택이 성숙. 단 *과학적 깊이*(σ·형상·다중앵커)는 우리.
- ⚠ **단 ①②③ 모두 LIB·공정-도구·EEPA(no-cap)·데이터-빈약 범위 / 형상불변 구 / σ 전무** — **전달 삼중항·형상소성·해석압축·물성예측에서 우리가 SOTA**라는 결론은 *4 peer 중 가장 강하게* 유지(Schreiner는 σ가 *완전 부재*해 transport 대비가 가장 극명). 그들 lead = *생산공정 도구·기계 모델*, 우리 lead = *transport·형상·다중모델·물성예측*.

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **paper 대조축 — "같은 calendering DEM, *공정-도구 vs 물성-예측*"**: Schreiner(EDEM+EEPA+Bonding, 목표물성→공정파라미터 *역추천*, σ 0채널) ↔ 우리(LIGGGHTS+Kirchhoff/Holm, 설계→물성 *예측*, σ 삼중항). **4 LIB-peer 중 σ-우위가 가장 극명한 대비**(Schreiner σ 완전 부재). Sangrós·Ngandjong·Lyu·Schreiner를 *네 LIB 선례*로 묶어 우리 ASSB+transport 정체성 정당화.
- ② **bond-only CABM(backlog A3) — *최소 구현* 청사진**: Schreiner의 Potyondy–Cundall bond(입자상 없이, 영구파단)는 우리 Stage-2 부피점유의 *가장 단순한 다음 단계*(입자수 안 늘림 = scaffold AM-freeze 정신). PTFE엔 Ngandjong/Lyu(재형성·모멘트)가 물리적으로 더 맞지만, *구현 비용 최소* 버전으로 Schreiner를 기록. 코드: LIGGGHTS `bond` fix.
- ③ **inverse-design 도구 컨셉**: 우리 predictor에 "목표 σ·porosity → 설계/공정 역산" 모드를 넣을 때 Schreiner USER TOOL이 *아키텍처 선례*(Module 3 = 파라미터 공간 + 목표 → 추천). ⚠ 변수 종류·예측 깊이는 우리가 다름/우위.
- ④ **층위지도 정정 기록**: EEPA = **A층(no-cap)**, *not* B층(경로 A 항복캡). Schreiner(EEPA) ≠ Sangrós/Varkey(Thornton–Ning 캡). 우리 contact_models_layer_map에 "EEPA = 우리 hooke/hysteresis의 상용-코드 사촌(같은 no-cap 층)" 명시(이미 §1에 EEPA/Thakur 있음 — Schreiner를 *그 LAW의 calendering 적용례*로 cross-link).
- ⑤ **데이터**: `docs/data/schreiner2020_calendering.csv` — 조성·밀도(Table 1, stated) + EEPA λ_P/Δ_Y + Bonding 영구파단 + porosity 43 %(압연전) + PSD/RVE/indenter(stated) + broken bonds(Fig 5 digitized). ⚠ **porosity-vs-line-load *없음*(이 논문 미보고)** → densification_porosity_db.csv에 *추가 행 없음*(압연전 43 % 단일점은 압력-시리즈가 아니라 제외; 정성 컨텍스트로만). **LIB·NMC622·공정-도구라 절대값 ASSB 전이 금지, *방법·철학·위상역전 대조*용.**

## 9. 인용 가능 문장 (deck/paper용)
- "Schreiner, Klinger & Reinhart (2020, TU Munich machine-tools institute) presented a **commercial-DEM (EDEM) calendering model** of an NMC622 cathode using an **EEPA elasto-plastic contact** (plasticity ratio λ_P for unloading stiffness; load-dependent adhesion surface energy Δ_Y) plus a **Potyondy–Cundall Bonding model** (permanent bond breakage) for the conductive additive-binder matrix, calibrated by flat-punch nanoindentation — embedded in a **three-module process-design framework whose Module 3 'user tool' inverts target electrode properties into recommended calendering parameters** (pressure, temperature, calendering speed, calender specification)."
- "Unlike its three LIB-calendering DEM peers (Sangrós 2019/2020 homogenised σ, Ngandjong 2021 FEM electrochemistry, Lyu 2025 qualitative σ argument), Schreiner (2020) solves **no conductivity at all** — the electrode-density 'conflict between good ion conductivity (low density) and high electrical conductivity (high density)' is *stated* but never computed. Our work supplies exactly this missing transport half: a **three-channel (σ_ionic/σ_e/σ_thermal) explicit Kirchhoff/Holm contact-network solver** with **Stage-E plastic contact areas** and **fracture-aware conduction**, plus **true plastic particle-shape morphology via MPM** — none of which the rigid-sphere, contact-plasticity-only, σ-free LIB tool provides."
- "Schreiner's EEPA contact is a **no-cap hysteretic elasto-plastic law** (plasticity ratio = unloading-stiffness fraction), i.e. the **commercial-code sibling of our LIGGGHTS hooke/hysteresis** — and is therefore distinct from the *yield-pressure-capped* Thornton–Ning law used by Sangrós and Varkey (our path-A precedent). EEPA shares our model's softening-not-capping plasticity branch."
- "Its genuine lead is a **production-engineering inverse tool** (target property → calendering parameter recommendation, with a roll-section model of spring-back) — the LIB precedent for an inverse-design mode our forward design→property predictor does not yet have; but the tool's interior remains a σ-free, shape-invariant rigid-sphere DEM, so the *depth* of the predicted properties stays decisively ours."

## 10. 주의/한계 (over-claim 방지)
- **★ 짧은 학회논문 — 정량 데이터 빈약**: 하드 porosity = **압연 전 43 % 단 하나**. **porosity-vs-line-load 표/곡선 *없음*** → 우리 P-vs-porosity·Heckel과 **직접 비교 불가**(Sangrós/Ngandjong/Lyu와 달리). Fig 3·5 = *load-displacement*(압밀압력 vs 변위 µm)이지 porosity-vs-P 아님. **densification CSV에 압력-시리즈 행 추가 안 함.**
- **σ 0채널 — 전도도 *전무***: σ_el·σ_ion·σ_thermal 어느 것도 안 풂(정성 논증조차 없음). 본 논문에서 "전달"을 *어떤 형태로도* 끌어오지 말 것. 우리 삼중항 우위 비교는 *그들이 σ를 *전혀* 안 푼다*는 사실에 근거(4 peer 중 가장 극명).
- **E_NMC 값 *미공개***: "Young's modulus를 가장 영향 큰 파라미터로 먼저 보정"이라 하나 *확정값을 본문에 안 줌*. peer(142/142/200 GPa)와 비교 불가. cf. 표 §3 비고.
- **LIB (액체전해질)** — 이온 채널이 **공극(암묵적 Bruggeman)**. σ·이온 절대값을 우리 ASSB(SE-network)로 전이 **금지**(다른 전도체 + 애초에 σ 부재). 본 논문은 역학·공정이라 이온위상은 *전제로만*.
- **강체 구 + EEPA CONTACT 탄소성** — 입자 형상 안 변함(δ=기하 프록시). **입자 파쇄 미모델**(bond 파단만; 파쇄 언급조차 없음 — *재배열*만). **형상소성·void-fill 없음** → 우리 MPM 영역과 별개(frame[5]).
- **★ EEPA = no-cap(A층), NOT 항복캡(경로 A)**: Schreiner의 "elasto-plastic"은 *제하강성비 λ_P*지 *경도 H 접촉압 캡*이 아님. **Sangrós/Varkey의 Thornton–Ning(항복캡)과 *다른 계열*** — 같은 "탄소성 접촉"이라 불려도 LAW 다름. 우리 경로 A(real E + p_y 캡) 선례로 *쓰면 안 됨*(EEPA는 우리 *현행* no-cap 편).
- **calendering(압연, 저압) ≠ ASSB cold-press(고압 ~300–500 MPa)** — 압밀모드·압력대 다름 + *porosity-vs-P 데이터 부재*라 **곡선 비교 자체가 불가**(정성 spring-back 형태만 대응).
- **CABM = 암묵적 matrix + bond-only** — Ngandjong/Lyu(명시 CBD 입자)와 *다른 단순화*. bond 강성·임계응력(τ_Cr/σ_Cr)·λ_P·Δ_Y는 **NMC622-CABM 보정값** → LPSCl-PTFE로 직접 전이 불가(*형태/철학*만 템플릿).
- **나노압입 — Young's modulus·접촉모델 보정용이나 *YR 같은 입자-항복비 추출 안 함*** (Sangrós 2019의 40-입자 YR이 *더 직접적*). Schreiner 압입은 *약한* 선례.
- **공정-도구가 진짜 산출 — 물성 *예측* 아님**: USER TOOL은 *공정 파라미터 역추천*. 우리 predictor(물성 예측)와 *방향·목적이 다름* → "그들이 물성예측을 못 한다"가 아니라 "그들 목적은 *공정설계*"가 정확.
- **2023 resupply**: PDF 하단 "resupply of March 2023 ... content unaffected" = *내용 동일, 템플릿만 정정*. 인용 시 원 2020 게재 유지.
- **Fig 3/4/5 일부 값(broken bonds ~25k–28k, 압밀압력 ~150 MPa)은 디지타이즈** → **추세만(±)**. **stated**: porosity 43 %·ρ 2.53·d_sheet 56 µm·PSD d₅₀ 7.19/최소 3.4/상한 20 µm·RVE 250²×120→56 µm·indenter ⌀100 µm·0.15 µm/s·λ_P(0.9/0.8/0.975→0.985)·Δ_Y(5/20/60 J/m²)·bond 영구파단·roll ~400 mm·Table 1 조성·밀도.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

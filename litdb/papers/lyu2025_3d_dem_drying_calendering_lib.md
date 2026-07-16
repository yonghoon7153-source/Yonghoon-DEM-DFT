<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. -->
# LIB 전극 구조진화를 건조+압연 한 번에 — 3D RVE DEM(AM + carbon-binder domain + 용매 + 입자접촉), 3-stage 건조법 + 압연→σ_e·두께방향 응력 — Lyu (Int. J. Electrical Power & Energy Systems 2025)

> slug `lyu2025_3d_dem_drying_calendering_lib` · DOI `10.1016/j.ijepes.2025.110521` · type `DEM (3D RVE, 건조+압연 연속; exp 검증)` · PDF `Lyu_2025_IJEPES_3D_DEM_ElectrodeEvolution_DryingCalendering.pdf` · digested `2026-06-26` · status ✅ · OPEN ACCESS (CC BY 4.0)

---

## 1. 한 줄 요약
**액체전해질 LIB 양극(NCM811 + carbon-binder domain CBD)의 미세구조 진화를 *건조(solvent evaporation) → 압연(calendering)* 두 공정을 한 3D RVE DEM 안에서 *끊김 없이 연속으로* 시뮬레이션한 논문** — Sangrós(2020)·Ngandjong(2021)이 압연만(또는 슬러리·건조·압연을 *별 코드*로 이어붙임) 다룬 데 비해, **본 논문의 차별점은 (a) 용매를 *fluid-substitution*(부력+점성감쇠, eq 27–29; 명시 CFD 아님)으로 넣어 건조 자체를 DEM으로 굴리고, (b) 그 건조-종료 구조를 그대로 압연 초기조건으로 물려 한 시뮬레이션 사슬로 연결**한 것. 결과: ① 배위수(coordination number) 진화로부터 **3-stage 건조 스킴**(HDR-LDR-HDR = 高-低-高 건조속도)을 도출(실험 [19,20]과 정성 일치), ② 압연이 **기계적 무결성(입자-집전체 접촉 897→2038, +230 %)·배위수(3.6→8.3)·전자전도도**를 향상시키되 **두께방향(z) 응력이 최대**(σ_zz≈−165 vs σ_xx=σ_yy≈−130 MPa)라 **입자 파쇄(실험 200 MPa) 회피를 위해 z-응력 관리 필요**. **⚠ σ_e는 이 논문에서 *정성*(접촉망 완전도 논증)일 뿐 — Bruggeman/RNM 같은 전도도 솔버로 *수치값을 산출하지 않는다*** (peer Sangrós/Ngandjong과의 핵심 차이; over-claim 금지).

**소재·이온위상 주의**: NCM811 + **액체전해질 LIB**라 (i) **이온 전도체가 *공극(pore)*** → 우리 ASSB(SE 고체 입자망=전도체, Holm 구속)와 **위상 정반대**, (ii) **porosity = GOOD**(전해질 충전) → 우리 ASSB(porosity = BAD)와 **목표 정반대**. 우리에겐 **frame[5] 분업의 또 하나 독립 확인(rigid 구 + bond, 형상소성 없음)** + **건조/CBD라는 우리가 안 가진 wet-process 역량의 청사진**(backlog A3/A4/D5)으로서 가치.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/binder/전해질) | 연구유형 |
|---|---|---|---|---|
| **Yuhang Lyu, Shaohai Dong, Li Ting Gao, Zhan-Sheng Guo**(교신, davidzsguo@shu.edu.cn) — Shanghai Institute of Applied Mathematics and Mechanics, School of Mechanics and Engineering Science, **Shanghai University**, Shanghai Key Laboratory of Mechanics in Energy Engineering | **Int. J. Electrical Power & Energy Systems 165, 110521 (2025)** (접수 2024-12-13, 개정 2025-01-17, 게재 2025-02-09, **open access CC BY 4.0**) | 10.1016/j.ijepes.2025.110521 | **NCM811** LiNi₀.₈Co₀.₁Mn₀.₁O₂ AM(ρ 4.74, E 142 GPa) + **carbon-binder domain(CBD)** 입자(carbon black + binder, ρ 2.2, E 0.65 GPa) + **용매(fluid-substitution)** + 액체전해질(공극); AM:CBD = **94:6 wt**, 고체분율 65 wt% | **DEM**(PFC3D 5.00; 건조+압연 연속) + 후처리(coordination·porosity·stress·contact network) + 압연 porosity 실험검증(Giménez [45]) |

> ★ **본 논문의 자리매김**: 같은 "LIB 전극 제조 DEM" 가문의 세 번째 — **Sangrós(2020, TU-BS, 압연역학+삼중 균질화)**, **Ngandjong(2021, Franco/LRCS, 슬러리→건조→압연→전기화학 멀티스케일)**, **Lyu(2025, Shanghai, *건조+압연을 한 DEM에 연속*)**. 본문 Introduction이 이 계보를 직접 인용: Sonzogni [46](압연 DEM)·Sun [47](압연 FEM)·Xu [48](과압연→이온저항↑)·Zhang [49,50](압연 DEM 응력분포)·Ge [51,52](압연 + bonding model)·**Ngandjong [53](압연 DEM, CBD+건조 *함께 다룸*)** 를 선행으로 들고, **"위 DEM 압연 시뮬들은 *건조 구조*를 초기상태로 거의 안 쓰고 랜덤 생성 구조를 쓴다 → 압연 분석에 부적절"**(본문 §1 끝)을 *본 연구의 동기*로 명시. 즉 **"검증된 건조-종료 구조를 압연 초기조건으로 물려준다"가 셀링 포인트**(Ngandjong과 같은 철학이되, *한 DEM 코드(PFC3D)로 건조와 압연을 끊김 없이*). 저자 1저자 본인의 선행 **Lyu [22] = *2D* DEM 건조** → 본 논문이 그 **3D 확장 + 압연 연결**.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **porosity (압연)** | **57 → 22 %** | 건조종료(압연시작) → 압연종료 | stated(Fig 7b) | 두께 80→40 µm(−50 %); ★실험 Hg-intrusion **57→~20 %**[ref32]와 일치 |
| **porosity 곡선 형태** | 0–0.25 평탄(57 %) → 선형 급강하 → 22 % | dimensionless time | digitized(Fig 7b) | **초기 평탄 = 거친 top이라 plate가 高점만 접촉**(RVE 밀도 거의 안 변함); top 평탄화 후 선형 압밀 |
| **두께 (압연)** | **80 → 60 → 40 µm** | t=0 / 0.5 / 1.0 | stated(Fig 7a) | ~40 % 두께감소 = ~75.4 % 밀도증가[ref32,33] |
| **coordination number Z (건조)** | **~0 → 3.6** | 슬러리 → 건조종료 | stated/digitized(Fig 6) | 3-stage: I(느림)·II(급증)·III(느림-안정) |
| **coordination number Z (압연)** | **3.6 → (dip ~2.3) → 8.3** | 압연시작 → 초기 → 종료 | stated/digitized(Fig 7c) | ★초기 dip(건조구조 안정성 파괴, 접촉분리) 후 **최대 8.3**(치밀화) |
| **입자-집전체 접촉수** | **897 → 1087 → 2038** | t=0 / 0.5 / 1.0 (압연) | stated(Fig 8) | **+230 %** — 계면접착↑·계면저항↓[ref38] |
| **평균응력 σ_zz (두께방향)** | **~−165 MPa** | 압연종료 | digitized(Fig 9a) | **★PEAK** — z 우선박막화; 접촉력이 주로 두께방향 |
| **평균응력 σ_xx=σ_yy (면내)** | **~−130 MPa** | 압연종료 | digitized(Fig 9a) | 주기경계 x·y라 등방; σ_zz보다 작음 |
| **입자파쇄 임계응력(실험)** | **200 MPa** | fracture onset | stated(ref [57]) | ★ z-응력을 이 아래로 유지해야 입자 안 깨짐 |
| **압연력(plate / collector)** | **~−4.9 / −5.7 N** | 압연종료 | digitized(Fig 9b) | 0에서 **지수적** 증가; collector가 약간 큼(top 국소 불안정) |
| **σ_electronic** | **수치 없음 — 정성만** | 압연↑ → σ_e↑ | stated | ★ "접촉망 완전도↑ → 전자경로 짧아짐·접촉↑ → e-저항↓"[ref38] *논증*만. **Bruggeman/RNM 솔버로 σ_e 값 산출 안 함** |
| **E_AM (DEM 입력)** | **142 GPa** | NCM811 단입자 | stated(Table 1) | cf 우리 E_CAM 140 / Sangrós 142.5 / Ngandjong 200 |
| **E_CBD (DEM 입력)** | **0.65 GPa** | CBD 입자 | stated(Table 1) | ~AM의 1/220 → **부드러운 변형상**(cf Ngandjong 2 GPa) |
| **ρ_AM / ρ_CBD** | **4.74 / 2.2 g/cm³** | 소재 | stated(Table 1) | NCM811 / CBD |
| **ν_AM / ν_CBD** | **0.25 / 0.2** | 소재 | stated(Table 1) | |
| **마찰(sliding/rolling) AM** | **0.12 / 0.012** | DEM | stated(Table 1) | CBD = 0.1 / 0.01 |
| **AM PSD** | **Gaussian 평균 13 µm, std 0.61** | 실측[ref51] | stated | **거의 단분산**(std 매우 작음) — bimodal 아님 |
| **CBD 직경** | **2.2 µm** | [ref28] | stated | AM·CBD 둘 다 구 가정 |
| **조성** | AM:CBD **94:6 wt**, 고체분율 **65 wt%** | 슬러리[ref26] | stated | |
| **bond gap λ** | **1.67** | bond 형성 기준 | stated[ref51] | ‖Pi−Pj‖ ≤ λ(Ri+Rj)면 bond |
| **압연 plate 속도** | **0.01 m/s** | const z-speed | stated[ref51] | quasi-static 압축 |
| **RVE** | **200×200×200 µm**(슬러리) → 건조후 z≈**80 µm** | 주기 x·y | stated | bottom=집전체, top=자유(건조)/plate(압연) |

## 4. 시뮬레이션 방법 ★
- **code / version**: **PFC3D 5.00**(Particle Flow Code 3D, Itasca — 상용 DEM). 후처리(coordination·porosity·stress·contact-network 진화)는 PFC3D 내장 + 본문 정의식(eq 24–26). **전기화학 솔버 없음**(σ_e는 정성 논증).
- **DEM 지배식(eq 1–2)**: 병진 `m_i du_i/dt = F_c + F_i`, 회전 `I_i dω_i/dt = F_t × R_i`. F_c=접촉력, F_t=접선접촉력, F_i=입자에 가해진 힘(건조 시 유체력).
- **DEM 접촉법칙** ★ (**eq 3–14, Hertz 계열 + 마찰**): 접촉력 `F_c = F^l + F^d` (eq 3) = **탄성+마찰(elastic no-tension + friction) F^l** + **점성감쇠(energy dissipation) F^d**. 법선·접선 분해(eq 4–5):
  - **법선 탄성** `F^l_n = (F^l_n)₀ − k_n·Δδ_n^(3/2)` (eq 6) — **Hertz 비선형(δ^1.5)**, k_n=A·E*/L(eq 14, A=접촉면적, L=중심거리).
  - **접선 탄성** `F^l_s = (F^l_s)₀ − k_s·Δδ_s` (eq 7) — 선형 접선강성 k_s.
  - **법선·접선 감쇠** `F^d_n = (2β_n√(m_c·k_n))·δ_n` (eq 8), `F^d_s = (2β_s√(m_c·k_n))·δ_s` (eq 9) — β_n/β_s=감쇠계수, m_c=감쇠질량(eq 13).
  - **유효물성** E*(eq 10, Hertz)·G*(eq 11)·R*(eq 12)·m_c(eq 13). ⚠ **이는 PFC3D의 *Hertz-Mindlin류 접촉*** — **항복압(p_y/H) 캡 없음**(Thornton–Ning 아님). 즉 **Luding/우리 hooke-hysteresis와 같은 *no-cap* 층**(접촉모델 층위지도 §1-A). 입자는 강체 구, δ=소성의 기하 프록시일 뿐 **형상 안 변함**.
- **재료 파라미터(Table 1)**: E_AM=142 GPa, E_CBD=0.65 GPa(AM의 1/220), ρ_AM=4.74, ρ_CBD=2.2 g/cm³, ν_AM=0.25, ν_CBD=0.2, 마찰 AM(slide 0.12/roll 0.012)·CBD(0.1/0.01).
- **bond/binder 모델** ★★ (**PFC3D 2종 bond — linear contact vs linear parallel; eq 15–23 + Fig 1**):
  - **linear PARALLEL bond(Fig 1b, eq 15–23)** = **CBD에 적용**(CBD-CBD, CBD-AM, CBD-collector). 법선·접선 *힘* `F = −F̄_n·n_c + F̄_s` (eq 15) **+ twisting·bending *모멘트* M̄ = M̄_t·n_c + M̄_b** (eq 16) 까지 전달 — **bond가 굽힘/비틀림 모멘트를 두 입자 사이에 전달**(eq 19–20). 힘-변위 법칙 eq 17–18(법선 F̄_n=(F̄_n)₀+k̄_n·Ā·Δδ_n, 접선 F̄_s). **최대 법선응력 σ̄ = F̄_n/Ā + ‖M̄_b‖R/I (eq 21), 최대 전단응력 τ̄ = ‖F̄_s‖/Ā + ‖M̄_t‖R/J (eq 22)** → bond breakdown stress σ̄_c/τ̄_c 도달 시 파단(Fig 1a). Ā=단면적, Ī=관성모멘트, J̄=극관성모멘트.
  - **linear CONTACT bond(Fig 1c)** = **AM에 적용**(AM-AM, AM-collector). **모멘트 미전달**(parallel bond에서 bending moment M̄를 무시하면 contact bond로 degenerate, 본문 eq 23 주변). 즉 **AM-AM = 힘만, CBD = 힘+모멘트**(CBD 망이 더 "구조적"). ⇒ **소재별 다른 bond 모델 = 본 논문의 명시적 설계**(CBD cohesion + AM-CBD adhesion 물성차 [ref31] 반영).
  - **bond 형성 기준(eq 23)**: 두 입자 중심거리 ‖Pi−Pj‖ ≤ **λ(Ri+Rj), λ=1.67**[ref51]이면 bond 생성. **Fig 1a = bond-to-bond failure 모식**(breakdown stress σ̄_c/τ̄_c에서 끊김; tension/bend/shear/torsion으로 파단, "open" 상태로). ⚠ Sangrós(영구파단)·Ngandjong(SJKR 재형성)과 **또 다른 갈래** — 여기선 **PFC3D linear parallel/contact bond(모멘트 전달 여부로 2종)**.
- **★ 용매/건조 모델 (fluid-substitution; eq 27–29) — 이 논문 차별점**:
  - **명시 CFD/capillary 아님**, **fluid-substitution model**[ref28](=DNS 유체 회피, 계산비 大절감)을 채택. 용매가 입자에 주는 영향을 **3개 힘**으로 대리:
    - **부력 F_b = 4/3·πR³·ρ_liquid·g** (eq 27) — 용매 부력.
    - **중력 F_g = 4/3·πR³·ρ_solid·g** (eq 28) — 입자 중력.
    - **점성감쇠 F_r = α·v** (eq 29) — **점성저항**(α=감쇠계수, v=입자속도; **상수 아님, 속도의존**).
  - **건조 = 용매가 마르며 부력 사라지고 입자가 가라앉아 충돌·압밀**(Fig 4). 슬러리 RVE 200³ µm에서 시작 → top free·bottom collector(입자 못 빠짐) → **안정 구조 형성 시 건조 종료**(두께 ~80 µm). ⚠ **모세관력(capillary bridge)·용매 표면장력은 명시 항으로 없음** — 부력+점성감쇠로 coarse-grain. ("solvent evaporation"을 *유체 부력 소멸*로 모사; 표면장력 유발 바인더 이동은 *결과*로 나타남, Fig 5 CBD top-enrichment).
- **MPM/continuum**: **없음**. 압밀역학·전기 모두 DEM(전기는 *정성*). **입자 형상소성(SHAPE flow)·void-fill 없음** — 접촉은 CONTACT 레벨.
- **전달 솔버** ★ (**없음 — σ_e는 정성 논증**): ⚠⚠ **본 논문은 σ_e/σ_ion을 수치로 산출하는 솔버(Bruggeman·RNM·Kirchhoff·FEM)를 *돌리지 않는다*.** "calendering이 전자전도를 향상"이라는 결론은 **접촉망 완전도(배위수↑·입자-집전체 접촉↑)로부터의 *물리 논증***(본문: tighter network → shorter e-paths → lower e-resistance[ref38]) + **"과압연은 이온저항↑[ref48]"** caveat. 따라서 **σ_e/σ_ion 수치는 우리 비교표에서 *정성 추세*로만** 다뤄야 함(Sangrós eq1 균질화·Ngandjong FEM과 *결정적으로 다른 점*).
- **입자 처리** ★ (DEM판 "무질서 처리"): **구만**(AM=Gaussian 평균 13 µm·std 0.61 = **거의 단분산** 강체 구; CBD=2.2 µm 단일 구). **rigid 입자 + Hertz CONTACT(항복캡 없음, δ 프록시) + bond(AM=contact bond, CBD=parallel bond)** — 입자 **형상 안 변함**. **초기구조 = 슬러리 RVE 균일분포 → *건조 DEM으로 형성*(랜덤 placement 아님)** — 이게 본 논문 novelty(건조-종료 구조를 압연 초기조건으로). PSD가 **bimodal 아님**(std 0.61로 사실상 mono) → **Furnas dip 다루지 않음**.
- **도메인/RVE / servo / seeds / 압력범위**:
  - **RVE 200×200×200 µm**(슬러리), x·y **주기경계**, bottom **집전체(current collector)**(입자 하강 차단), top=자유표면(건조)/**pressure plate**(압연).
  - **건조**: fluid-substitution → 안정 구조 시 종료(두께 ~80 µm). **압연**: 건조-종료 구조를 *그대로* 초기조건으로, **plate가 z축 아래로 const 0.01 m/s** 하강(servo 압력제어 아니라 *변위/속도 제어* — 우리 MPM "hold"와 같은 결).
  - **압력범위**: 명시 절대 압력 sweep 없음(평균응력 −165 MPa까지 발달, Fig 9a). 압연 검증은 Giménez [45] porosity-vs-압력 실험과 대조(Fig 3, ~0–160 MPa 범위에서 sim≈exp).
  - **seeds**: 명시 안 됨(단일 RVE 추정).
- **특이사항/튜닝**:
  (1) **건조+압연 한 DEM 연속** — 건조 출력(구조·접촉·bond)이 압연 입력. **이게 핵심 novelty**(Ngandjong은 CGMD→DEM 코드 전환; Lyu는 PFC3D 한 코드).
  (2) **소재별 bond 차등**(AM=contact bond 모멘트無, CBD=parallel bond 모멘트有) — CBD가 더 "구조 잡는" 상.
  (3) **fluid-substitution**(부력+점성, 명시 모세관 無)으로 용매 coarse-grain — 계산비 절감하되 표면장력 물리는 간접.
  (4) **검증 = Giménez [45] 압연 porosity-vs-압력**(Fig 3) + Hg-intrusion 57→~20 %[ref32] + 입자파쇄 200 MPa[ref57] + EDS CBD top-enrichment[ref18,21]. **σ_e/σ_ion 실측 검증 없음**(정성 결론이라).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **bond 모식**: (a) bond-to-bond failure(법선/모멘트/전단/토크 vs 변위; breakdown stress σ̄_c/τ̄_c에서 파단→open), (b) **linear parallel bond**(힘+모멘트 전달, CBD용), (c) **linear contact bond**(힘만, AM용) | **PFC3D bond 2종(모멘트 전달 여부)의 정의도** — 우리 CBD bond 모델화(backlog A3) 시 *모멘트 전달 CBD vs 힘만 AM* 차등의 청사진 |
| **2** | **초기 RVE**: (a) 건조용(200³ µm, AM 녹색 구 + CBD 적색 점, bottom collector), (b) 압연용(같은 RVE + 상단 **pressure plate**) | 시뮬 셋업; AM:CBD 크기·수 비율 시각화 |
| **3** | ★ **porosity vs 압축응력**(실험■ Giménez[45] + DEM● 적선) — 0→160 MPa서 ~57→~22 %, **sim≈exp 양호**(저압서 급강하 후 완만) | **압연 P-vs-porosity 검증**(우리 P-vs-porosity·Heckel과 대조; LIB 저압 급강하 — 단 압력대 다름) |
| **4** | **건조 3D 구조진화**: (a₁–a₃) 거시구조(슬러리 분산→충돌→치밀 다공), (b₁–b₃) **입자 속도장**(건조 진행에 top 입자가 빠름 = 두께방향 속도구배), (c₁–c₃) **접촉망 진화**(초기 희박→집전체측부터 AM 굵은선 망 형성→안정) | **건조가 집전체측부터 AM 접촉망을 쌓는 것** 시각화; 속도구배=건조 비균질의 직접증거. 우리 압밀 진화 영상의 LIB-건조판 |
| **5** | **CBD 분포 진화(건조)**: (a–c) 3D + 2D 수직단면 — 건조 종료 시 **CBD가 전극 *상단(top)*에 농축**(binder migration). EDS 실험[ref18,21]과 일치 | ★ **건조 시 바인더가 위로 쏠려 *집전체 계면 바인더↓→접착↓*** — 우리가 안 가진 *건조-유발 조성 구배* 현상. backlog A4(coating)·CBD morphology와 개념 연결 |
| **6** | ★ **배위수 vs dimensionless time(건조)** — **3 stage**: I(HDR, 느림 0–0.45)·II(LDR, 급증 0.45–0.9)·III(HDR, 느림-안정 0.9–1.0). Z 0→3.5 | ★ **3-stage 건조 스킴의 근거**(Z 증가율로 stage 구분 → 중간 LDR·양끝 HDR 권장). 우리 압밀 단계론과 개념 대응 |
| **7** | ★ **압연 구조진화**: (a₁–a₃) 3D+front(h 80→60→40 µm), (b) **porosity vs time**(57→22 %, **초기 평탄 후 선형 급강하**), (c) **배위수 vs time**(3.6→**dip ~2.3**→**8.3**) | **압연 압밀 곡선 + 배위수 dip-then-rise**(초기 거친 top·구조파괴 → 재배열 → 치밀). 우리 압밀 Z 진화와 대조 |
| **8** | ★ **입자-집전체 접촉수 vs time(압연)** — **897→1087→2038**(+230 %), 인셋=집전체 접촉키 분포 | **압연이 계면접착·계면저항을 직접 개선**(접촉↑) — 우리 coverage(집전체 계면 아님)와 개념 대응 |
| **9** | ★ **압연 역학**: (a) **평균응력 σ_xx/σ_yy/σ_zz vs time**(전부 압축음수; **σ_zz≈−165 PEAK** > σ_xx=σ_yy≈−130; 인셋=접촉력 벡터도 t=0/0.5/1.0), (b) **plate·collector 힘 vs time**(0에서 **지수증가**, collector −5.7 > plate −4.9 N) | ★ **두께방향(z) 응력 최대 + 지수적 힘 증가** — 우리 MPM 압밀 응력장(z 우선)과 직접 대응; **입자파쇄 200 MPa 회피 = z-응력 관리**가 우리 fracture와 연결 |

## 6. Post-processing ★
- **무엇**:
  - **coordination number(eq 24)**: `C_n = n_c^(b)/N_b` (N_b=입자수, n_c^(b)=총 접촉수). 건조(Fig 6)·압연(Fig 7c) 진화. **stage 구분·치밀화 정량의 1차 지표**.
  - **porosity(eq 25)**: `P = V_void/V_reg = 1 − V_mat/V_reg`(측정영역 내 공극/영역부피). 압연 진화(Fig 7b), 실험(Giménez[45], Hg-intrusion[ref32])과 대조.
  - **average stress(eq 26)**: `σ̄ = −1/V·Σ_{N_c} F^(c)⊗L^(c)` (N_c=측정영역 접촉수, F^(c)=접촉력벡터, L^(c)=두 입자 중심 잇는 branch vector, ⊗=외적, **압축이 음수**). 방향별 σ_xx/σ_yy/σ_zz(Fig 9a) — **두께방향 응력 추출이 핵심**.
  - **contact network 진화**: 접촉망 완전도(굵은선=AM, 가는선=기타; Fig 4c) — **전자전도 *정성* 논증의 근거**(망 완전→e-경로↑).
  - **입자-집전체 접촉수**: 압연 진화(Fig 8) — 계면접착·계면저항 대리.
- **도구**: **PFC3D 5.00**(DEM + 내장 후처리), 본문 정의식(eq 24–26). **외부 전도도/τ 솔버(GeoDict·COMSOL·자체 Kirchhoff) 없음**. 실험 비교: Giménez [45] 압연 porosity, Hg-intrusion[ref32], EDS binder 분포[ref18,21], 입자파쇄[ref57].
- **수치화·플롯·기록 방식**: 모든 진화량을 **dimensionless time의 함수**로(Fig 6·7·8·9). porosity만 압력의 함수로도(Fig 3 검증). **σ_e/σ_ion은 plot 없음**(정성 결론).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (LIB, 건조+압연) | 우리 (ASSB cold-press) | 차이 / 이유 |
|---|---|---|---|
| **공정 모델링 범위** | **건조(fluid-sub) + 압연(plate)을 한 DEM 연속** | DEM 압밀(cold-press) → 네트워크 σ → grade + MPM morphology | ★ **그들은 건조까지** — 우리는 압밀에서 시작(건조=우리 미보유) |
| **★ 이온 채널 위상** | **공극(pore)=전도체**(액체전해질) → porosity GOOD | **SE 고체 입자망=전도체**(Holm 구속) → porosity BAD | **★★ 위상 정반대.** 압밀↑ → LIB 이온↓(공극↓) vs ASSB σ_ionic↑(SE접촉↑) |
| **★ 전달 솔버** | **없음 — σ_e *정성*(접촉망 완전도 논증), Bruggeman/RNM 미사용** | **명시 Kirchhoff + Holm 구속 + Stage-E** σ_ionic/e/thermal **삼중항**(수치) | ★★ **우리가 압도적 우위.** 그들은 σ_e 수치를 *안 줌*; 우리는 3채널 솔버 + LOOCV 스케일링 법칙 |
| **압밀 모드** | **calendering(압연 plate, z-속도 제어)** + 건조 침강 | **cold-press(단축, 변위 hold)** | 압연(저압·z-박막화) ≠ 고압 프레싱. 둘 다 변위/속도 제어(servo 아님) |
| **접촉법칙** | **PFC3D Hertz-Mindlin류(항복캡 없음, δ^1.5)** | Luding hooke/hysteresis(항복캡 없음) + Stage-E 소성면적 | **같은 no-cap 층**(층위지도 §1-A). 우리는 Stage-E로 소성면적 후보정 |
| **★ bond/binder** | **PFC3D linear bond 2종**: CBD=parallel(힘+모멘트), AM=contact(힘만), breakdown stress 파단 | CBD = Stage-2 부피점유(PTFE/VGCF); 명시 bond **없음**(backlog A3) | **세 번째 bond 청사진**(Sangrós 영구파단·Ngandjong SJKR재형성에 더해 *PFC3D 모멘트-전달 parallel bond*) |
| **★ 용매/건조** | **fluid-substitution**(부력+점성, eq 27–29; 모세관 명시無) | **없음**(ASSB는 dry-process/cold-press, 용매 無) | ★ **건조 = 우리가 *근본적으로* 안 다루는 축**(ASSB 건식공정). 단 dry-process 혼합/fibrillation 모델화 시 참고 |
| **접촉 소성** | **CONTACT 레벨(δ 프록시), 형상 불변** | MPM 진짜 SHAPE 소성 + DEM hooke/hysteresis | 입자 형상 안 변함(DEM); **형상변화 = 우리 MPM 고유**(frame[5]) |
| **E_AM** | E_NCM811 **142 GPa** | E_CAM **140 GPa** | **거의 동일**(둘 다 NCM811; Sangrós 142.5·Ngandjong 200와도 정합대) |
| **E_CBD** | **0.65 GPa**(AM의 1/220, 매우 부드러움) | n/a(부피점유만) | Ngandjong 2 GPa보다 더 부드럽게 잡음 |
| **PSD** | **Gaussian 평균 13 µm std 0.61 = 거의 mono** | **bimodal 12:4:1**(AM_P/AM_S/SE) | ★ **그들은 mono-AM → Furnas dip 안 다룸**; 우리는 bimodal + dip 정량 |
| **검증** | **압연 porosity 실측**(Giménez[45], Hg[ref32]) + 입자파쇄 200 MPa | solver=ground truth(Minnmann·Cronau·Bazzoun 등) | 그들 압연 porosity 검증은 LIB 앵커(ASSB 직접 전이 불가) |
| **소재/전해질** | **NCM811 + 액체전해질**(LIB) | **LPSCl SE + NCM811**(ASSB) | CAM은 같으나 **전해질·이온위상 다름** → 절대 porosity·σ 직접 전이 금지 |

> ★★★ **위 표는 §A에서 모두 풀어 씀 — 아래 "## 우리 DEM+MPM 대비"가 정식 비교 섹션**(사용자 mandatory). §7은 요약표.

### frame[5] 위치
- **이 논문 = 전달/패킹 측 + LIB 건조/압연 공정**: rigid 구(AM+CBD) + Hertz 접촉 + PFC3D bond → DEM 압밀(건조+압연). **입자 형상소성·void-fill 없음**(CONTACT 레벨) — 우리 MPM이 메우는 *형상-morphology 절반*이 LIB DEM에도 빠짐 (**Sangrós·Ngandjong·Varkey·Bazzoun과 동일 — frame[5] 5번째 독립 확인**).
- **그들 σ_e는 *솔버 없는 정성 논증***(Bruggeman/RNM 미사용) → 우리 Kirchhoff/Holm/Stage-E 삼중항이 *수치로* 채우는 바로 그 칸 → **우리 transport novelty가 가장 선명하게 드러나는 peer**(§C).
- **그들 건조(fluid-substitution) = 우리가 *아예 안 가진* wet-process 절반** → frame[5]의 우리 쪽이 *압밀부터*임을 확인(건조 전 단계는 ARTISTIC/Lyu 영역).

---

## ★ 우리 DEM+MPM 대비 (comparison vs ours)

> 사용자 mandatory 섹션 A. 그들 DEM(rigid + CBD bond + 용매 + 건조) vs 우리 Luding hooke/hysteresis + Stage-E + 18× 연화; 그들 σ_e(DEM 정성) vs 우리 Kirchhoff+Holm 삼중항; LIB pore=전도체(Bruggeman) vs 우리 ASSB SE-network=전도체(Holm) 위상역전; 그들이 모델하는 *건조*(용매 증발)를 우리는 안 함(ASSB dry-process/cold-press).

### A-1. 접촉·압밀 머신: 같은 rigid-sphere DEM, no-cap 접촉, 형상 불변 (공통)
- **그들**: PFC3D 5.00, 입자 = 강체 구(AM 13 µm·CBD 2.2 µm), 접촉 = **Hertz-Mindlin류**(법선 δ^1.5, 접선 선형, 점성감쇠; eq 6–9) — **항복압 캡 없음**. CBD가 E=0.65 GPa로 부드러워 압밀을 흡수.
- **우리**: LIGGGHTS, 입자 = 강체 구(AM_P/AM_S/SE), 접촉 = **Luding hooke/hysteresis**(k₁ 로딩 / k₂ 언로딩 / k_c 점착) — **항복압 캡 없음**(접촉모델 층위지도 §1-A에 둘 다 같은 *no-cap* 층). **E_SE 18× 연화**(real 24 → effective 1.35 GPa)로 강체 구가 못 잡는 granular 재배열을 럼핑.
- **공통 한계(frame[5])**: 둘 다 **입자 형상 안 변함**(δ=소성 기하 프록시, 진짜 흐름 아님). Lyu도 Sangrós·Ngandjong·Varkey·Bazzoun처럼 *rigid-sphere + CONTACT-레벨*이라 **morphology/void-fill 절반이 빠짐** → **우리 MPM(J2 진짜 SHAPE 소성)이 메우는 칸**. **LIB DEM 5편 연속으로 같은 한계** = frame[5] 분업이 우리만의 변명이 아니라 *분야 공통 구조*임을 다섯 번째 독립 확인.
- **차이점(우리 후처리 우위)**: 그들은 접촉면적 후보정 없음(PFC3D 내장 Hertz 면적). 우리는 **Stage-E**(Tabor F/H + volume V/h 소성 접촉면적 재유도)로 *소성 접촉면적*을 명시 보정 → 전도도 솔버 입력 정밀화. Lyu에는 이 층이 없음(σ_e가 정성이라 불필요했음).

### A-2. ★★ σ_e: 그들 DEM *정성 논증* vs 우리 Kirchhoff+Holm *수치 삼중항* — 우리 결정적 우위
- **그들**: **σ_e/σ_ion을 수치로 산출하는 솔버를 돌리지 않는다.** "calendering이 전자전도를 향상"은 **접촉망 완전도**(배위수 3.6→8.3, 입자-집전체 접촉 897→2038)로부터의 *물리 논증*(tighter network → shorter e-paths → lower e-resistance[ref38]) + **"과압연 → 이온저항↑[ref48]"** caveat. **Bruggeman ε^1.5도, RNM/Kirchhoff도 없음.**
- **우리**: **명시 Kirchhoff 망**(Σ(φi−φj)/R=0) + **Holm 구속저항**(R=1/(2σr_c), 1967) + **Stage-E 소성 접촉면적** → **σ_ionic·σ_electronic·σ_thermal 삼중항을 *수치로*** 산출. 게다가 **솔버 출력을 LOOCV 스케일링 법칙으로 압축**(σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.903).
- **대비의 의미**: **이게 우리 DEM novelty가 가장 선명한 칸.** Lyu는 "압연→전자전도↑"를 *접촉수로 추론*만 하는데, 우리는 *같은 접촉망에서 Holm 구속저항으로 σ를 풀어* 수치를 준다. **peer Sangrós(eq1 fabric 균질화)·Ngandjong(COMSOL FEM)은 적어도 σ 수치를 줬는데, Lyu는 그조차 안 줌** → **Lyu 대비 우리 transport 우위는 Sangrós/Ngandjong 대비보다 *더 큼***(그들은 솔버 자체가 없음). ⚠ 단 정직: Lyu의 *목적*은 구조진화·역학이지 transport 수치가 아니었음(그래서 정성으로 충분했음) — "그들이 못 했다"가 아니라 "그들 scope 밖, 우리 scope 안"이 정확.

### A-3. ★★ 이온 채널 위상 역전 — LIB pore=전도체(Bruggeman) vs ASSB SE-network=전도체(Holm)
- **LIB(이 논문)**: 활물질·CBD는 절연 매트릭스, Li⁺는 **공극을 채운 액체전해질**로 흐름. → 이온 전도체 = **공극상(pore phase)**, σ_ion = f(ε, τ) = **Bruggeman ε^1.5**(Lyu는 이걸 *명시 계산 안 하지만*, 본문이 "과압연→이온저항↑[ref48]"로 *공극 축소→이온 악화* 위상을 분명히 전제). **porosity = GOOD**(전해질 충전 공간).
- **우리 ASSB**: 액체전해질 없음. Li⁺는 **SE 입자가 서로 닿은 접촉망**으로만 흐름 → **공극 = 순수 방해물**, σ_ionic = **SE-SE 구속저항**(Holm) + Kirchhoff. **압밀하면 SE 접촉↑ → σ_ionic↑**. **porosity = BAD**(없앨수록 좋음, ~10 % 목표).
- **위상 정반대의 두 발현**:
  - **목표함수**: Lyu/LIB는 **porosity를 적당히 남김**(과압연 = 이온저항↑ 손해 → moderate calendering이 최적, trade-off). 우리 ASSB는 **porosity 최대 제거**(~10 %).
  - **압밀 방향성**: 압밀↑ → **LIB σ_ion↓**(공극↓·τ↑) vs **ASSB σ_ionic↑**(SE접촉↑). **부호 반대.**
- **→ 깔끔한 대조(Sangrós·Ngandjong 대비와 동일 축, 3번째 LIB peer로 보강)**: "액체전해질 LIB에서는 *공극*이 이온 전도체(porosity GOOD, 과압연은 이온저항↑)인 반면, all-solid-state 전극에서는 *고체전해질 입자망*이 이온 전도체(porosity BAD, 압밀↑→σ_ionic↑)다 — Lyu(2025)가 압연을 *moderate*에서 멈춰야 하는 이유(과압연→이온저항↑[ref48])가 바로 우리 ASSB가 *최대 압밀*을 추구하는 이유의 거울상이다." **Lyu·Sangrós·Ngandjong 3편이 같은 위상역전을 LIB쪽에서 독립 확인** → 우리 SE-network 솔버의 존재 이유를 3중 정당화.

### A-4. ★ 용매/건조 — 우리가 *근본적으로* 안 가진 wet-process 축
- **그들**: **fluid-substitution**(부력 F_b + 중력 F_g + 점성감쇠 F_r, eq 27–29)으로 용매를 coarse-grain → **건조(solvent evaporation) 자체를 DEM으로** 굴림. 건조 결과: 두께방향 속도구배(Fig 4b), **CBD top-enrichment**(binder migration, Fig 5; 집전체 계면 바인더↓→접착↓), 3-stage 건조 스킴(Fig 6).
- **우리**: **건조 없음.** ASSB는 **dry-process / cold-press**(용매 無 또는 최소). 우리 파이프라인은 *이미 형성된 분말 bed의 압밀*에서 시작.
- **대비의 의미**: **건조는 frame[5]의 우리 쪽에 *없는* 축** — 그들이 *앞서는* 정직한 칸. 단 **ASSB는 본질적으로 건식**이라 "우리가 뒤처졌다"가 아니라 **"셀 화학이 달라 건조 단계가 없다"**가 정확. 그래도 **ASSB dry-process 혼합·PTFE fibrillation을 언젠가 모델하려면** Lyu의 fluid-substitution(또는 Ngandjong의 CGMD 용매수축)이 *방법 청사진*. ⚠ 단 **모세관력(capillary)·표면장력은 Lyu도 명시 항으로 없음**(부력+점성만) → 건조 후기 모세관 압밀은 그들도 간접 — 우리가 dry-process 가면 *모세관 없는* 점이 오히려 단순화 이점.

### A-5. 압밀 곡선·응력·검증
- **압밀 P-vs-porosity**: Lyu Fig 3은 ~0–160 MPa서 57→22 %(저압 급강하 후 완만), Giménez[45] 실측과 일치. 우리 Heckel(pure-SE 4압력)은 R²=0.965·**P_y=138 MPa**. **둘 다 elastic→plastic knee + 포화** 형태지만 **압력대 다름**(LIB 압연 저압 vs ASSB 고압 300 MPa) + **소재·이온위상 다름** → **Fig 3 곡선을 우리 P-vs-porosity·Heckel과 직접 겹치면 안 됨**(정성 형태만 대응). LIB floor ~22 %(stiff NMC E=142 + 저압 + porosity 일부러 남김)는 우리 **강체 구 floor ~20 %**와 *우연히 비슷*하나 *물리는 다름*(우리는 소성흐름으로 그 아래 ~10 % 도달).
- **응력장**: Lyu Fig 9a의 **σ_zz≈−165 PEAK > σ_xx=σ_yy≈−130 MPa**(두께방향 우선) = 우리 **MPM 압밀 응력장**(z 우선 박막화)과 **직접 대응**. 그들 "z-응력을 입자파쇄 200 MPa 아래로"는 우리 **fracture-aware transport**(Auerbach/f_intact)와 연결 — 단 그들은 *경고*만(파쇄 모델 없음), 우리는 *fracture 솔버*로 깨진 접촉의 σ 손실을 정량.
- **검증 깊이**: Lyu = 압연 porosity 1개(Giménez) + Hg + 파쇄 + EDS 정성. 우리 = Minnmann porosity·Cronau overlap·Bazzoun σ_ionic·SEM morphology 다중 앵커. ⚠ 둘 다 LIB/ASSB로 *절대값 직접 전이 금지*.

---

## 적용가능성 (applicability to our LIGGGHTS DEM model)

> 사용자 mandatory 섹션 B. 그들 명시 CBD + 용매 + 건조-stage 모델이 우리 backlog A3/A4/D5(CBD 명시 bond)와 co-rolling/dry-process 방향(Lee2025)의 청사진; 압연→두께방향 응력이 우리 압밀 응력에 매핑; LIGGGHTS에 CBD/용매 상을 추가할 수 있나; dry-ASSB vs wet-LIB 차이 명시. 우리 scripts/knobs에 매핑.

### B-1. CBD 명시 bond — *세 번째* 청사진(PFC3D parallel/contact bond) → backlog A3
- **현재 우리**: CBD를 **Stage-2 부피점유**(PTFE/VGCF가 SE 도메인 부피 차지)로만, 명시 입자-입자 bond 없음(`docs/digest_model_application_backlog.md` A3).
- **Lyu가 주는 것**: **PFC3D linear bond 2종** — **CBD = parallel bond(힘+모멘트 전달, eq 15–22)**, **AM = contact bond(힘만)**, breakdown stress σ̄_c/τ̄_c 파단. ★ **소재별 bond 차등이 핵심 시사**: 바인더상(CBD)은 *굽힘/비틀림 모멘트를 전달*(parallel bond)해야 "구조를 잡는" 거동이 나오고, AM-AM은 힘만으로 충분.
- **3개 CBD 청사진 비교(우리 선택지)**:
  | 모델 | bond 물리 | 파단 | 우리 적용 |
  |---|---|---|---|
  | **Sangrós 2020** | 점-bond(법선·접선 힘, 강성 6e12 N/m³) | **영구파단**(2e13 N/m²) | 단순·검증됨; 모멘트 無 |
  | **Ngandjong 2021** | SJKR 점착(CED×A) | **끊김·재형성**(reversible) | PTFE cold-weld(`--coh`)에 직결 |
  | **Lyu 2025(PFC3D)** | **parallel bond(힘+모멘트)** vs contact bond(힘) | breakdown stress, open | **모멘트 전달 = 섬유망 휨강성**에 가장 가까움 |
- **→ LIGGGHTS 매핑**: LIGGGHTS는 PFC3D parallel bond에 해당하는 **`bond` fix(cohesive bond, Potyondy-Cundall류)**가 있음 → **CBD-CBD에 모멘트-전달 bond, AM-AM에 힘-only bond**를 Lyu처럼 차등 적용 가능. ★ **PTFE 섬유는 *휨강성*이 있으므로**(fibrillated 망) **Lyu의 parallel bond(모멘트 전달)가 Sangrós 점-bond보다 PTFE에 더 적합** — Ngandjong SJKR(재형성·등방)과 Lyu parallel-bond(모멘트·구조적)를 *결합*(끊김재형성 + 휨강성)하는 게 우리 fibrillated-PTFE 1차 근사로 이상적. 코드: `--coh`(점착) + bond fix(모멘트) 조합.

### B-2. ★ 용매/건조 상 — LIGGGHTS에 추가 가능하나, dry-ASSB라 *우선순위 낮음*
- **추가 가능성**: Lyu의 **fluid-substitution(eq 27–29)**은 *명시 CFD 없이* 입자별 부력+점성감쇠 힘만 추가 → **LIGGGHTS에 `fix addforce`(부력·중력 차) + `fix viscous`(속도비례 감쇠 F=−αv)로 거의 그대로 구현 가능**(매우 저렴). 건조 = α를 시간에 따라 키우거나(점성↑) 부력 ρ_liquid를 0으로 ramp.
- **⚠ dry-ASSB vs wet-LIB**: 우리 소재계(LPSCl + NCM811 + PTFE/VGCF)는 **건식 co-rolling / cold-press**(`papers/lee2025_*` = 건식 공정 실험 앵커)라 **용매 건조 단계가 *원천적으로 없음***. 따라서 Lyu의 건조 모델은 **우리 production 파이프라인엔 직접 쓸 일 없음**.
- **단 D5(co-rolling/dry-process) 방향엔 유용**: 만약 ASSB **dry-process 혼합·PTFE fibrillation의 동역학**을 모델하려면(Lee2025 co-rolling의 *공정* 재현), Lyu의 fluid-sub *프레임*(입자별 환경력 추가)을 **용매 대신 *전단/혼합력*으로** 변용 가능. fibrillation은 PTFE의 shear-draw(`docs/cbd_morphology_roadmap.md`)라 *유체*가 아니라 *전단*이지만, "입자에 공정-환경력을 per-particle로 더한다"는 *구조*는 동일.

### B-3. 압연→두께방향 응력 → 우리 압밀 응력·fracture에 매핑
- **Lyu Fig 9a(σ_zz PEAK −165 MPa, 두께방향) + 입자파쇄 200 MPa 경고** → 우리 **MPM 압밀 응력장**(이미 z 우선)과 직접 대응. ★ **흡수 포인트**: Lyu는 "z-응력 < 입자 파쇄응력 유지"를 *설계 기준*으로 명시 — 우리 **fracture-aware σ**(Auerbach/f_intact/frac_severe)에 **"압밀 z-응력이 입자강도 초과 시 파쇄→접촉손실→σ 손실"** 인과를 더 명시적으로 넣을 근거(우리는 이미 fracture 솔버 보유 → Lyu의 *경고*를 *정량 솔버*로 이미 채움 = 우리 우위 + 그들 동기 정당화).
- **코드 매핑**: 우리 `scripts/network_conductivity.py`의 fracture 분기(Auerbach 임계) + MPM 응력장(`scripts/mpm3d_compaction.py` wallP/σzz readout)이 Lyu의 σ_zz·파쇄경고를 *이미 정량화*. Lyu는 "압밀응력이 z-편향"을 LIB-DEM으로 확인 → 우리 MPM σzz가 같은 z-편향을 ASSB로 재현하는지 cross-check 거리.

### B-4. 3-stage 건조 + 배위수 진화 → 우리 압밀 단계론과 개념 대응
- Lyu의 **배위수 증가율로 건조를 3-stage 구분**(HDR-LDR-HDR, Fig 6) + **압연 Z dip-then-rise**(Fig 7c, 3.6→2.3→8.3)는 *공정 진화를 Z로 추적*하는 방법론. 우리는 압밀을 *압력의 함수*로 보지만, **Lyu처럼 *시간/변위의 함수로 Z 진화*를 추적**하면 압밀 중 재배열·접촉형성 단계를 더 미시적으로 볼 수 있음 → 우리 DEM dump 시계열에서 Z(t) 추출은 이미 가능(`coordination` 후처리). **압연 초기 Z dip**(구조 안정성 파괴→재배열)은 우리 압밀 초기 거동과 비교 거리.

### B-5. dry-ASSB vs wet-LIB — 종합 정리
- **우리가 가져갈 것**: ① CBD 명시 bond(parallel-bond 모멘트 전달, B-1) — *직접 유용*(backlog A3); ② z-응력/파쇄 인과(B-3) — *이미 보유, 정당화*; ③ Z(t) 진화 추적(B-4) — *방법론*.
- **우리가 안 가져갈 것**: ① 건조/용매(B-2) — ASSB 건식이라 원천 무관(단 D5 dry-process엔 *프레임*만); ② Bruggeman/pore-이온(위상역전) — 우리 SE-network와 정반대; ③ porosity GOOD 목표 — 우리 BAD.
- **결론**: Lyu는 **CBD bond 모델화(A3)의 세 번째·가장 구조적(모멘트) 청사진**이자 **압밀 z-응력·파쇄의 LIB 확인**으로 우리에게 *부분적으로* 유용. 건조·이온위상·porosity-목표는 LIB 특유라 전이 불가. **핵심: "CBD parallel-bond(모멘트) 차등 적용 + z-응력 파쇄 인과"가 우리 LIGGGHTS에 실제 흡수 가능한 두 조각.**

---

## ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this DEM model)

> 사용자 mandatory 섹션 C. 사용자가 firm한 DEM novelty를 원함 — **우리가 SOTA임을 분명히 주장.** 7개 차별점을 Lyu 2025 대비 매핑. 정직하게 그들이 앞서는 칸(건조·CBD·용매)도 명시. evidence-based; LIB-not-ASSB scope 명시.

**총평: Lyu 2025는 "LIB 전극 구조진화(건조+압연)를 한 DEM으로 연속 시뮬"한 견고한 *공정-역학* 논문이지만, *transport(전도도)는 정성 논증에 그치고, 입자는 rigid 구(형상소성 없음)이며, 단분산 AM(dip 없음)이다.* 우리는 그 *비어 있는 칸 셋*(수치 transport 삼중항 / 진짜 소성 morphology / bimodal dip)을 정면으로 채우면서, 추가로 fracture·literature-grounded σ·dual-model 독립검증·LOOCV 예측기까지 갖춘다. 따라서 *transport·morphology·예측* 축에서 우리가 명백히 SOTA이고, Lyu는 *건조/CBD/용매*라는 wet-process 공정 축에서 우리보다 앞선다.** (단, 우리 = ASSB, Lyu = LIB — *셀 화학이 다른 보완 관계*임을 항상 병기.)**

| # | 우리 차별점 | Lyu 2025는? | 증거 / 우위 정도 |
|---|---|---|---|
| **1** | ★ **전달 TRIAD via Kirchhoff + Holm 구속** (σ_ionic/e/thermal *수치*) | **σ_e *정성*만**(접촉망 완전도 논증), σ_ion 미산출, Holm 구속 물리 無, Bruggeman/RNM 無 | ★★★ **압도적 우위.** Lyu는 transport *수치 자체가 없음* — Sangrós(균질화)·Ngandjong(FEM)보다도 transport는 *덜* 함. 우리 Holm R=1/(2σr_c)+Kirchhoff 3채널 = *완전히 비어 있는 칸* |
| **2** | ★ **Stage-E 소성 접촉 AREA**(Tabor F/H + volume V/h 재유도) | **없음**(PFC3D 내장 Hertz 면적; σ_e 정성이라 면적 정밀화 불요) | ★★ 우위. 우리는 *소성 접촉면적*을 별도 보정 → 전도도 솔버 입력 정밀(Lyu엔 해당 층 자체가 없음) |
| **3** | ★ **DEM↔MPM scaffold + J2 진짜 소성 MORPHOLOGY**(SEM 코어보존+경계평탄화 ✓, void-fill flow, Σdg 변형장) | **rigid 구 + bond, 형상 불변**(CONTACT 레벨, δ 프록시) | ★★★ 우위. Lyu는 *형상소성 절반이 빠짐*(frame[5]) — Sangrós·Ngandjong·Varkey·Bazzoun과 **5번째 동일 한계**. 우리 MPM이 *유일하게* 그 칸 보유 |
| **4** | ★ **fracture-aware transport**(Auerbach/Lawn, 깨진 접촉의 σ 손실 정량) | **입자파쇄 *경고*만**(실험 200 MPa 인용; 파쇄 솔버 無) | ★★ 우위. Lyu는 "z-응력<파쇄응력 유지"를 *설계 기준*으로 말만 함 — 우리는 *fracture 솔버*로 파쇄→접촉손실→σ 손실을 *정량*(그들 동기를 우리가 이미 채움) |
| **5** | ★ **literature-grounded σ_grain**(Cronau 단결정 3.0 + Cronau(r_SE) sub-µm 인자) | **n/a**(LIB·σ 정성이라 σ_grain 입력 자체 없음) | ★ 우위(축이 다름). 우리 σ는 *재료물성에 anchor*; Lyu σ_e는 *접촉수 추론* |
| **6** | ★ **실험-anchored INDEPENDENT dual-model**(DEM·MPM 각각 실험에 보정, 서로 cross-fit 금지 — frame[4]/[5]) | **단일 DEM**(MPM·이중모델 無; 검증=압연 porosity 1점 + 정성) | ★★ 우위. 우리는 *두 독립 모델의 수렴=교차검증*(frame[4]) — Lyu는 단일 모델·단일 porosity 앵커 |
| **7** | ★ **solver→scaling-law LOOCV 예측기**(σ_ionic 0.975/σ_e 0.953/σ_thermal 0.903; design knobs→metrics) | **없음**(공정진화 시뮬, 예측 법칙 無) | ★★ 우위. 우리는 솔버를 *예측 가능한 법칙으로 압축* — Lyu는 case-by-case 시뮬 |

### ★ 정직하게, Lyu가 *앞서는* 칸 (over-claim 방지)
- **(가) 건조(solvent evaporation)를 DEM으로 연속 시뮬** — **우리 *근본적으로* 미보유**. fluid-substitution(부력+점성)으로 건조 침강·CBD top-enrichment·3-stage 스킴을 잡음. ⚠ 단 **ASSB는 건식**이라 "우리가 뒤처졌다"가 아니라 *셀 화학상 건조 단계가 없다* — 보완 관계.
- **(나) CBD를 *명시 입자상 + bond*로 모델** — 우리는 Stage-2 부피점유만(명시 bond는 backlog A3, *미구현*). Lyu(+Sangrós/Ngandjong)가 CBD bond를 *이미 구현*. ★ **이건 우리가 *따라가야 할* 칸**(그들 청사진 = §B-1).
- **(다) 건조+압연 *한 코드 연속*** — Ngandjong은 CGMD→DEM 코드전환, Lyu는 PFC3D 한 코드로 끊김 없이. *공정 사슬 연속성*은 그들이 앞섬(우리는 압밀 단일 공정).
- **(라) 압연 porosity 실측 직접검증**(Giménez[45]) — LIB 압연 앵커. 단 ASSB로 전이 불가.

### ★ 종합 positioning (한 문단, deck용)
"Lyu(2025)·Sangrós(2020)·Ngandjong(2021) — LIB 전극 제조 DEM의 세 SOTA — 는 모두 **rigid 구 + CONTACT 접촉 + CBD bond**로 압밀을 굴리고 **이온 전도체를 *공극*(Bruggeman, porosity GOOD)**으로 둔다. 우리 ASSB DEM+MPM은 이 셋과 **이온위상이 정반대**(SE 입자망=전도체, Holm 구속, porosity BAD)이고, 세 가지를 *추가*한다: ① **수치 transport 삼중항**(Kirchhoff/Holm/Stage-E — Lyu는 σ_e조차 정성), ② **진짜 소성 morphology**(MPM J2 — LIB DEM 5편 전부 형상 불변), ③ **bimodal Furnas dip**(Lyu는 단분산 AM). 거기에 fracture 솔버·literature σ_grain·independent dual-model·LOOCV 예측기까지 더해 **transport·morphology·예측 축에서 SOTA**다. 정직히 **건조/CBD-bond/용매는 그들이 앞서지만**(wet-process 공정 — ASSB 건식엔 원천 무관하거나 우리 backlog A3), 이는 *셀 화학이 다른 보완 관계*이지 우리 핵심 novelty(고체 transport + 소성 morphology)를 잠식하지 않는다."

---

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **paper 대조축 — "LIB 제조 DEM 3종(Sangrós·Ngandjong·Lyu) 모두 이온=공극(porosity GOOD), transport는 균질화/FEM/*정성* — 우리만 SE-network 수치 솔버 + porosity BAD"**: Lyu는 *transport 수치가 아예 없는* 가장 극단 케이스라 우리 Kirchhoff/Holm 삼중항의 우위가 *가장 선명*. 세 LIB peer를 묶어 우리 ASSB transport novelty를 3중 정당화.
- ② **CBD 명시 bond 3번째 청사진(backlog A3)**: Lyu의 **PFC3D parallel bond(힘+모멘트, CBD) vs contact bond(힘, AM)** 차등 = **PTFE 섬유 *휨강성*에 가장 적합**(Sangrós 점-bond·Ngandjong SJKR보다). LIGGGHTS bond fix(모멘트) + `--coh`(점착) 조합 → Ngandjong 재형성 + Lyu 모멘트 = fibrillated-PTFE 1차 근사.
- ③ **z-응력/파쇄 인과 = 우리 fracture 솔버 *정당화***: Lyu의 "압밀 σ_zz PEAK > 면내 + 입자파쇄 200 MPa 회피" = 우리가 *이미 fracture 솔버로 정량화한* 인과의 LIB 확인. 우리 MPM σzz(z 우선)이 같은 편향을 ASSB로 재현하는지 cross-check.
- ④ **건조 = 우리 미보유 축(정직)**: ASSB 건식이라 직접 무관하나, **D5 dry-process/Lee2025 co-rolling** 모델 시 fluid-sub *프레임*(per-particle 환경력)을 *전단력*으로 변용 가능(방법론).
- ⑤ **데이터**: `docs/data/lyu2025_drying_calendering.csv` — 압연 porosity(57→22 %, stated/digitized)·두께(80→40 µm)·배위수(건조 0→3.6, 압연 3.6→2.3→8.3)·입자-집전체 접촉(897→2038)·응력(σ_zz −165 PEAK, σ_xx=σ_yy −130)·압연력(plate/collector −4.9/−5.7 N)·DEM 파라미터(E_AM 142/E_CBD 0.65 등)·bond·fluid-sub. **⚠ σ_e는 정성(수치 행 없음); LIB·액체전해질·저압 압연이라 절대 porosity·이온위상 ASSB 전이 금지, 추세·방법·CBD-bond 대조용.**

## 9. 인용 가능 문장 (deck/paper용)
- "Lyu et al. (2025, Shanghai University) simulated Li-ion cathode (NCM811 + carbon-binder domain) microstructure evolution through **both drying and calendering in a single continuous 3D DEM** (PFC3D), representing the solvent by a **fluid-substitution model** (buoyancy + velocity-dependent viscous damping, no explicit CFD/capillary) and using **two PFC3D bonds — a moment-transmitting linear parallel bond for the CBD and a force-only linear contact bond for the active material**; they derived a **three-stage drying scheme** (high-low-high drying rate) from the coordination-number evolution and showed calendering raises mechanical integrity (particle–collector contacts 897→2038, +230 %; coordination 3.6→8.3) with the **peak compressive stress in the thickness direction** (σ_zz ≈ −165 vs σ_xx=σ_yy ≈ −130 MPa)."
- "Unlike Sangrós (analytic homogenization) or Ngandjong (COMSOL FEM), Lyu (2025) reports **no numerical conductivity** — the calendering→electronic-conductivity claim rests on a **qualitative contact-network-completeness argument**, with no Bruggeman or resistor-network solver. Our ASSB DEM+MPM fills exactly this gap with a **numerical Kirchhoff/Holm constriction-resistance triad** (σ_ionic/electronic/thermal), making the transport-side novelty against Lyu even larger than against the homogenization/FEM LIB peers."
- "Across the three state-of-the-art Li-ion manufacturing DEMs (Sangrós 2020, Ngandjong 2021, Lyu 2025) the ionic conductor is always the **pore phase** (Bruggeman, porosity beneficial, over-calendering raises ionic resistance), whereas in our all-solid-state electrode the **solid-electrolyte particle network** is the ionic conductor (Holm constriction, porosity detrimental, densification raises σ_ionic) — Lyu's need to stop at *moderate* calendering is the mirror image of our drive toward *maximum* densification."

## 10. 주의/한계 (over-claim 방지)
- **LIB (액체전해질)** — 이온 채널이 **공극(Bruggeman·porosity GOOD)**이라 이온 위상·porosity 목표·압밀방향(압밀↑→이온↓)을 우리 ASSB(SE-network, 압밀↑→σ_ionic↑, porosity BAD)로 전이 **금지**. 전자·압밀역학·bond·z-응력만 물리 대응; **이온은 위상 자체가 반대**(대조용).
- **★ σ_e/σ_ion 수치 없음 — *정성* 결론** — Lyu는 Bruggeman/RNM/Kirchhoff/FEM **전도도 솔버를 안 돌린다.** "압연→전자전도↑"는 **접촉망 완전도 논증**(배위수·집전체 접촉수↑)일 뿐 *수치 σ 산출 아님*. → 우리 비교에서 **σ_e는 *정성 추세*로만**(Sangrós eq1·Ngandjong FEM과 *결정적으로 다름* — 그들조차 수치를 줬는데 Lyu는 안 줌). CSV의 σ_e 행은 *qualitative*로 표기.
- **강체 구 + Hertz CONTACT(항복캡 없음)** — 입자 **형상 안 변함**(δ=기하 프록시). **형상소성·void-fill 없음** → 우리 MPM 영역과 별개(frame[5], LIB DEM 5번째 동일 한계). CBD의 "변형"도 입자 E가 낮을 뿐(0.65 GPa) 형상흐름 아님.
- **fluid-substitution(부력+점성)만 — 모세관·표면장력 명시 항 없음** — 건조 후기 capillary 압밀·표면장력 유발 바인더 이동은 *간접*(부력 소멸의 결과로 CBD top-enrichment가 *나타남*). 명시 capillary-bridge 모델(Lippke[28] 등) 대비 coarse. **건조 절대 동역학(시간 스케일)은 fluid-sub α 보정에 의존.**
- **압연 = calendering(저압, plate z-속도)** ≠ ASSB cold-press(고압 ~300 MPa, 변위 hold) — 압력대 다름 + 압밀모드(압연 z-박막화 vs 단축 hold) 달라 **Fig 3 P-vs-porosity 곡선을 우리 곡선/Heckel과 직접 겹치면 안 됨**(knee·floor 형태만 정성). LIB floor ~22 %가 우리 강체 floor ~20 %와 비슷한 건 *우연*(물리 다름 — 우리는 소성으로 그 아래 도달).
- **NCM811 + 액체전해질** — CAM은 우리와 같으나(E 142≈우리 140) **전해질·이온위상이 다름**. AM PSD = **Gaussian std 0.61 = 거의 단분산** → **bimodal/Furnas dip 안 다룸**(우리 12:4:1과 다름). 절대 porosity·σ 전이 금지.
- **응력·porosity·힘 값 일부 digitized**(Fig 7b/9a/9b 그래프에서 읽음) → **추세만(±)**. **stated**: porosity 57→22 %, 두께 80/60/40 µm, 배위수(3.6 start·8.3 max), 입자-집전체 접촉(897/1087/2038), 입자파쇄 200 MPa, Table 1(E·ρ·ν·마찰), AM PSD(13 µm·std 0.61), CBD 2.2 µm, 조성 94:6·65 wt%, bond λ=1.67, plate 0.01 m/s. **σ_zz/σ_xx/압연력 절대값은 digitized**(Fig 9 그래프).
- **검증 = 압연 porosity 1개 + Hg + 파쇄 + EDS 정성** — Sangrós(σ_el 4-point·접착 pull-off·porosity)·Ngandjong(indentation+porosity 2개 동시 + discharge + EIS)보다 *검증 descriptor 적음*. σ_e/σ_ion 실측 검증 없음(정성이라).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

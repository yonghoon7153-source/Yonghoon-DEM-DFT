# DEM 파라미터 민감도 분석 + 캘리브레이션 — 냉간가압 ASSB 양극 미세구조 (Bazzoun & Piruzjam, Electrochim. Acta 2025)

> slug `bazzoun2025_dem_parameter_sensitivity_assb_cathode` · DOI `10.1016/j.electacta.2025.146536` · type `DEM` · PDF `Bazzoun_2025_ElectrochimActa_DEM_ParameterSensitivity_ASSBCathode.pdf` · digested `2026-06-26` · status ✅

## 1. 한 줄 요약 (TL;DR)
**우리와 정확히 같은 공정(단축 냉간가압 LPSCl+NCM811 양극)·같은 코드(LIGGGHTS)·같은 연구(DEM 압밀)** 의
**파라미터 민감도 분석 + 실험 캘리브레이션** 논문 — 8개 입력(입경분포·마찰 3종·E 2종·ν 2종·COR)이
CAM 이용률 θ_CAM / SE 이용률 θ_SE / porosity ε 에 미치는 영향을 OAT(One-At-a-Time)로 정량화하고,
**CAM–SE 마찰계수 μ_CAM-SE 가 percolation·연결성·porosity 의 단일 최강 민감 파라미터**(특히 고-CAM 로딩
f_CAM 에서)임을 밝힘.  ★ 결정적으로 저자 스스로 **"DEM 은 저-f_CAM 에서 정확하나 고-f_CAM 에서 현저한
불일치 + 민감도 급증"** 이라 명시 — **이것이 강체-구(rigid-sphere) DEM 의 천장이며, 바로 우리 Stage-E
소성 접촉면적 + MPM J2 소성 morphology 가 메우는 칸**.  이 논문은 이미 digest 된 **Bazzoun 2026 (J. Power
Sources, σ_ionic FEM·RNM)** 의 **DEM-캘리브레이션 자매편**(같은 그룹·같은 소재·같은 LIGGGHTS) —
2026 이 *전달(σ)* 를 풀었다면 2025 는 *구조·캘리브레이션·민감도* 를 푼다.  **우리 work 의 가장 가까운 peer.**

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **A.M. Bazzoun, J. Piruzjam (공동제1저자)**, S. Hink, L. Rubacek, A. Fill, T. Carraro, K.P. Birke (**Mercedes-Benz AG** + Univ. Stuttgart IPV + **Helmut Schmidt Univ./연방군 Hamburg** 응용수학) | **Electrochimica Acta 535 (2025) 146536** | 10.1016/j.electacta.2025.146536 | **Li₆PS₅Cl (CIS Korea) + LiNi₀.₅Mn₀.₃Co₀.₂O₂ (NMC532, Nippon Chemical)** + CB Super C45 + CNF + PTFE (dry-film) | **DEM 압밀** (LIGGGHTS, 파라미터 민감도 + 실험 캘리브레이션), 실험 검증 |
| 접수 2025-03-08 / 개정 2025-04-29 / 수락 2025-05-23 / 온라인 2025-06-10. **Open Access (CC BY 4.0).** |

> ⚠ **소재 미묘한 차이 주의**: SE 는 LPSCl(우리와 같음)이지만 CAM 은 **NMC532 (Ni₀.₅Mn₀.₃Co₀.₂)** — 우리/Bazzoun 2026 의 **NMC811 (Ni₀.₈)** 과 *조성이 다름*.  E_CAM=161.5 GPa 는 둘 다 같게 가정하나(NMC 일반), 절대 σ·균열 전이 시 주의.  단 *압밀 역학·패킹·민감도* 는 NMC 조성과 거의 무관(E·ρ 만 관여) → 추세·방법론은 직접 적용 가능.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| porosity ε (SE45, sim) | **~0.22(60wt%)→~0.25(85wt%)** | 300 MPa nominal, box-conv | digitized Fig5/6 | 고-CAM↑→ε↑ (불완전 충전) |
| porosity ε (SE19, sim) | **~0.16→~0.18** | 300 MPa | digitized Fig5/6 | 작은 SE19 가 *더 치밀*(~0.06 낮음) |
| ε 실측 (SE19) | 0.19/0.13/0.105/0.137 감소율 | 200→400 MPa, f_CAM 60/70/80/85 | stated §4.4 | 압력↑→ε **−19.0/−12.6/−11.8/−13.7 %** |
| ε 실측 (SE45) | 감소율 −22.0/−10.9/−7.5/−6.1 % | 200→400 MPa, f_CAM 60–85 | stated §4.4 | |
| **SE19 vs SE45 ε 차** | SE19 가 **23.6/20.5/12.7/13.8 % 낮음**(@200), **37.4/32.8/30.6/24.9 %**(@400) | f_CAM 60/70/80/85 | stated §4.4 | 작은 SE → 패킹↑ → ε↓ (Furnas/size 효과) |
| **θ_CAM (CAM 이용률)** | f_CAM 60–70wt%서 **≈1.0(완전)**, 80서 ~0.7–0.85, **85서 ~0.35–0.5 급락** | 400 MPa, μ=0.4 nominal | digitized Fig12/18 | percolation 임계 근처 급락 |
| **θ_SE (SE 이용률)** | f_CAM 60–70서 **≈1.0**, 80서 ~0.75–0.9, **85서 ~0.4 급락** | 400 MPa | digitized Fig20 | θ_SE 가 θ_CAM 보다 *먼저* 떨어짐(조기 경고) |
| θ_CAM 실측(SE19/SE45) | SE45: 60–80서 ~0.9–1.0, 85서 **~0.35** 급락; SE19: 85서도 ~0.5(>SE45) | 200·400 MPa | stated Fig18 | 작은 SE19 가 고-CAM서 θ_CAM 우월 |
| 비방전용량 (SE45) | 136.5/137.5/104/50.5(@200)→140.2/139/114/52.5 mAh/g(@400) | f_CAM 60/70/80/85 | stated §4.4 | C_max,disch=150 (θ_CAM=1 기준점, 60wt% SE19@400) |
| 비방전용량 (SE19) | 142.5/144.5/139.5/122.5(@200)→148.5/146.5/148.5/130(@400) | f_CAM 60–85 | stated §4.4 | SE19 가 고-CAM서 142.6/147.6 %↑ vs SE45 |
| **E_SE** | **20.5 GPa** (범위 15–200 sweep) | LPSCl | stated Table 3 | ≈ 우리 real 22–24 / Bazzoun 2026 의 22.1 |
| **E_CAM** | **161.5 GPa** (범위 123–200) | NMC | stated Table 3 | = Bazzoun 2026 |
| ν_SE / ν_CAM | **0.33 (0.29–0.37) / 0.27 (0.24–0.3)** | | stated Table 3 | (Bazzoun 2026 은 ν_SE=0.37) |
| **마찰 μ (SE-SE/CAM-CAM/CAM-SE)** | **모두 0.4 (범위 0.2–0.6)**, 통합 μ_eff | This work | stated Table 3/5 | **최강 민감 파라미터** |
| COR (RC) | **0.4 (0.2–0.6)** | This work | stated Table 3 | 최저 민감(거의 무영향) |
| 압력 p | **300 MPa nominal (200–400 sweep)** | | stated Table 3 | 우리 300 과 동일 |
| ρ_CAM / ρ_SE / ρ_CB / ρ_CNF / ρ_PTFE | **4.77 / 1.64 / 2.00 / 1.90 / 2.15 g/cm³** | | stated Table 2 | |
| **PSD D̄ (mean diameter)** | **CAM 5.8 µm · SE45(pristine) 4.5 µm · SE19(ball-milled) 1.9 µm** | 레이저회절 | stated §4.1 | 입경비 λ=D̄_CAM/D̄_SE: SE45 **1.3** / SE19 **~3** |
| bulk σ_ionic (EIS) | **SE45 = 2.9 mS/cm · SE19 = 1.0 mS/cm** | 350 MPa 펠릿 | stated Fig4b | 볼밀↑→입계↑→σ↓ (cf. Bazzoun 2026 펠릿 1.02) |
| Heckel P_y / knee | **n/a** (Heckel 안 함) | | n/a | ε-vs-P 곡선만; 압력민감도 "유의 추세 없음" 명시 |

## 4. 시뮬레이션 방법 ★
- **code / version**: **LIGGGHTS** (오픈소스 DEM, Kloss et al. [40,42]) + MATLAB 자동화 스크립트(입력 생성→대량 데이터→모델기반 최적화).  서버 = Lenovo ThinkSystem SR650 / SUSE Linux, 다중 태스크 병렬.  Lagrangian 방법(입자별 Newton 운동방정식 eq4/5, 유한차분 적분).
- **DEM 접촉법칙** ★: **법선 = Hertzian spring + 점성감쇠 / 접선 = damping spring + Coulomb 절단**.  (= 우리 hooke/hysteresis 와 같은 *no-cap 탄성 이력* 계열, `contact_models_layer_map.md` 층 A).
  - 법선력 `F_ij,n = k_ij,n·δ_ij,n·n − γ_ij,n·u_ij,n` (eq6), 접선력 `F_ij,t = k_ij,t·δ_ij,t − γ_ij,t·u_ij,t` (eq7).
  - **탄성항 = Hertz**: `k_ij,n = (4/3)·E*·√(R*·δ_ij,n)`, `k_ij,t = 8G*·√(R*·δ_ij,t)` (eq26, Appendix).
  - **감쇠항 = COR(RC) 의존 점탄성**: γ_n = −√5·[ln(RC)/√(ln²(RC)+π²)]·√(m*·k_n), γ_t = −√(10/3)·[...]·√(m*·k_t) (eq27).
  - **접선력 Coulomb 절단** (eq32): |F_ij,t| > μ_ij·|F_ij,n| 이면 F_t = μ·|F_n|·(F_t/|F_t|) 로 클램프.  Rolling friction = "rolling friction method" [40] 로 비구형성 근사(추가 토크 T_i, eq5).
  - **★ 항복캡 없음**: Thornton–Ning 의 p_y 도, So 의 H-cap 도 *없음* → 순수 탄성 Hertz + 감쇠.  소성변형 미모델(아래 §10 한계).
- **재료 파라미터** (Table 3): E_SE 20.5(15–200), E_CAM 161.5(123–200) GPa, ν_SE 0.33(0.29–0.37), ν_CAM 0.27(0.24–0.3), μ(3종) 0.4(0.2–0.6), COR 0.4(0.2–0.6), p 300(200–400) MPa.  밀도 Table 2.
- **bond/binder 모델**: **명시적 binder 없음** — CB/CNF/PTFE(각 1 wt%, 총 ~3 wt%)는 DEM 도메인에서 *제외*하고 **질량 prefactor 로만 보정**: `m_tot=(m_CAM+m_SE)/(1−(f_CB+f_CNF+f_PTFE))=(m_CAM+m_SE)/(1−f_add)` (eq8).  근거 = 부피·연결성 영향 작음(저자 인정: 이 가정이 θ 과대평가 가능, §3.7).
- **MPM/continuum**: **없음** (순수 DEM 구조 생성).  2025 논문은 *전달 솔버도 없음* — θ_CAM/θ_SE 는 percolation *존재* + cluster *부피*(이용률)까지만, σ 절대값은 *안 풂* (그건 자매편 Bazzoun 2026 의 FEM/RNM 이 함).
- **전달 솔버** ★: **없음 (핵심)**.  대신 **percolation 기반 이용률(utilization)** 만:
  - **θ_CAM** (eq9): 각 입자=노드, 중심거리 < 반경합 이면 이웃.  **CAM 입자가 SE separator 층까지 *연속 percolation 경로* 로 연결되면 "active"**.  `θ_CAM = V_CAM^active / V_CAM^total`.  (Li⁺ 가 SE 망 통과는 CAM 통과보다 훨씬 빠르다는 가정 [44,45] — SE 경로만 평가.)
  - **θ_SE** (eq10): SE 망만 분리, separator 까지 연속 경로 있는 SE 부피 / 전체 SE 부피.  `θ_SE = V_SE^connected / V_SE^total`.
  - ⚠ **이것은 σ 가 아니라 percolation 연결성·이용률** — 전류해(Kirchhoff)·접촉저항(Holm)·field 는 *전혀 없음*.  순수 *기하 connectivity*.
- **porosity 계산 ★ (Monte Carlo)**: soft-sphere 겹침 때문에 해석적 부피가 어려움 → **MC 점 무작위 삽입**(eq11–13): `v_CAM=N_CAM/N_total`, `v_SE`, `v_void`.  SE-CAM 겹침 영역의 점은 *CAM 으로* 귀속(E_CAM≫E_SE 라 CAM 이 SE 를 압입).  체적 V_X=v_X·V_box (eq14–16), 질량 m_X=V_X·ρ_X (eq17–18).  **additive 부피(CB/CNF/PTFE)를 void 에서 빼서 보정** (eq19–22): `ε=(V_void−(V_CB+V_CNF+V_PTFE))/V_box` (eq22).  **MC 점 30,000 개면 수렴**(100→200,000 스윕, Fig10), porosity 정밀엔 50,000 권장.
- **입자 처리** ★★ (DEM 판 "무질서 처리"):
  - **구(sphere)만** — CAM·SE 모두 완벽 구.  **형상은 절대 변하지 않음**.  저자 명시(§3.1): "복잡 형상은 응집체(여러 구 결합)로 가능하나 *계산비용 최소화 위해 구로 한정*."
  - **rigid 입자 + CONTACT 탄성(Hertz)만** — **CONTACT 소성조차 없음**(δ 는 탄성 겹침; So 의 h_eq·H 항복도, Thornton–Ning p_y 도 없음).  → **진짜 SHAPE 소성도, CONTACT 소성도 아닌 순수 탄성 강체구**.  저자 §3.7 명시: "이상화 spring-dashpot, *소성변형·점착 미고려* → 접촉면적 과소·연결성 과대 가능."
  - PSD: **mono-modal 분리**(CAM 1종 + SE 1종), Gaussian-like 단봉(레이저회절).  CAM PSD 고정, **SE 만 2종(SE45 D̄ 4.5 / SE19 D̄ 1.9 µm)** 비교 = 입경비 λ 효과(1.3 vs 3).
- **도메인/RVE / servo / seeds / 압력범위**:
  - 직육면체 box, **측방 주기경계 + 바닥 고정벽 + 상단 하강 servo wall**(= 단축 냉간가압).  초기 무작위 삽입(겹침 0), 중력 + 상단벽 최대속도 **0.2 µm/µs**, **PID 제어**로 목표 단축압 유지 → 총 운동에너지 0 수렴까지 hold.  Rayleigh·Hertz time-step 기준 만족.
  - **box size factor(RVE) 수렴 연구**: side length ratio ω(virtual box / 전체) 도입 — 벽 2–4 입경 이내는 bulk 아님 → 제외.  **ω=0.7 선택**(top/bottom 벽효과 제거).  box factor 8 이상서 ε 수렴, **box factor 10 + ω=0.7** 채택.
  - **조성당 독립 실현 3개**(seed) → 평균 + 표준편차(에러바).
  - **압력**: nominal 300, sweep **200/300/400 MPa**.  f_CAM **60/70/80/85 wt%** (Table 1).
  - **민감도 스윕 규모**: 8 파라미터 × 10 값(이산균일) × SE 2종 × f_CAM 4종 × 압력 3종 = **총 1920 케이스**, 각 ≥3 seed.
- **특이사항/튜닝**:
  - **OAT(One-At-a-Time) 민감도** (Saltelli [56]): 파라미터 q 의 10 값 `q_i=q_l+(i−1)(q_u−q_l)/(N_s−1)` (eq23), nominal `q̄=(q_l+q_u)/2` (eq24).  **민감도 지수 SI = 분석 state x_i 의 표준편차** `SI=√(1/N_s·Σ(x_ij−x̄_i)²)` (eq25).  SI 클수록 영향 큼.
  - **마찰 3종 통합**: μ_SE-SE/μ_CAM-CAM/μ_CAM-SE 를 개별 측정 어려움 + 민감도 분석이 셋 다 강함 → **통합 effective μ** 5 레벨(0.2/0.3/0.4/0.5/0.6, Table 5)로 단순화해 모델-실험 대조.
  - **dry-film(DF) 양극 제조** (실험): 볼밀(CAM+SE→CB+CNF→PTFE 순차) → 100 ℃ mortar grinder dough → 롤링 ~105 µm 시트.  torque cell(PEEK, 10 mm), separator 100 MPa + 양극 200/400 MPa, Li-In 음극, CCCV 0.05 mA/cm² (kinetic 한계 최소화 → θ_CAM 순수 측정).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | spring-dashpot 접촉모델 모식 (k_ij,n/t, γ_ij,n/t, R_i/R_j) | 우리 hooke/hysteresis 와 같은 법선/접선 spring+damper 구조도 |
| 2 | DEM 양극 생성 과정 스냅샷 (초기 무작위 → 단축가압 → 침강 → SE separator(빨강) 접촉 CAM 표시) | 우리 DEM→네트워크 파이프라인의 *구조 생성* 단계와 1:1 |
| 3 | SEM: (a)CAM (b)SE45(pristine) (c)SE19(ball-milled), 스케일 10 µm | CAM 매끈·SE45 큰입자·SE19 미분쇄 morphology — 우리 PSD 입력 시각 근거 |
| 4 | (a)PSD CAM/SE45/SE19 (D̄ 5.8/4.5/1.9) (b)EIS 펠릿 σ(SE45 2.9·SE19 1.0 mS/cm) (c)XRD | **bulk σ 앵커**(볼밀→σ↓), PSD 입력값, 결정성 유지 |
| 5 | θ_CAM·θ_SE vs box size factor (SE19 a,b / SE45 c,d), f_CAM 60–85 | RVE 수렴: box≥10서 θ 안정; 우리 RVE 수렴(box factor 35)과 대조 |
| 6 | porosity ε vs box size factor (SE19 a / SE45 b), f_CAM 60–85 | **SE19 가 SE45 보다 ~0.06 낮은 ε** (작은 SE→치밀) = 우리 size=packing |
| 7 | (a)벽효과 illustration (b)side length ratio ω 정의 | ω=0.7 = 우리 periodic-RVE 경계처리와 같은 문제의식 |
| 8 | porosity ε vs ω (SE19 a / SE45 b), plateau 영역 빨강 | ω 0.4–0.9 plateau → ω=0.7 선택; bulk porosity 추출법 |
| 9 | porosity ε vs box factor at ω=0.7 (SE19 a / SE45 b) | ω-보정 후 box factor 8+ 수렴 확인 |
| 10 | porosity ε vs MC 점수 (SE19 a / SE45 b), 100–200,000 | **30,000 점 수렴** → 우리 ε_sphere/union MC 방법론 대조 |
| 11 | 시뮬레이션 시간 vs box factor (SE19/SE45) | SE19(작은 입자→입자수↑)가 훨씬 느림 → 우리 계산비용 논거 |
| 12 | **θ_CAM·θ_SE·ε vs μ_CAM-SE (a,c,e) 및 vs E_SE (b,d,f)**, f_CAM 60–85, 400 MPa, SE45 | **μ_CAM-SE↑→θ↓·ε↑**(고-f_CAM서 급); E_SE 는 약함 — 핵심 민감도 그림 |
| 13 | 민감도 행렬 (θ_CAM/θ_SE/ε × 8파라미터 × f_CAM × 압력), 구 크기=SI (SE45 a-c / SE19 d-f) | 8파라미터 전 영향 한눈 — μ_CAM-SE 구가 가장 큼 |
| 14 | **정규화 SI 랭킹 막대** (θ_CAM/θ_SE/ε, SE45 a / SE19 b) | **★ μ_CAM-SE 1위 / 마찰 3종 상위 / E moderate / ν·RC 최저** = 캘리브레이션 우선순위 |
| 15 | 충방전 1주기 곡선 (SE45 a-d / SE19 e-h), f_CAM 60–85, 200·400 MPa | θ_CAM 추출용 비방전용량; 우리 grade_engine Q_grav 와 대조 |
| 16 | 비방전용량 vs f_CAM (SE45 a / SE19 b), 200·400 MPa | **85wt%서 SE45 급락 vs SE19 유지**(142.6/147.6 %↑) = 작은 SE 고-CAM 이득 |
| 17 | (a)밀도 ρ vs f_CAM (b)porosity ε vs f_CAM, SE19/SE45, 200·400 MPa, theoretical(빨강) | **ρ_sim < ρ_theoretical**(빨강선) = porosity 잔존; 우리 porosity@P 앵커 직접대조 |
| 18 | **모델 vs 실험**: θ_CAM(SE19 a/SE45 b) + ε(SE19 c/SE45 d) vs f_CAM, 200·400 MPa, Sim vs Exp | **★ 저-f_CAM 일치 / 고-f_CAM(80–85) 불일치** = rigid-sphere 천장의 직접 증거 |
| 19 | **상대오차 vs μ_eff** (θ_CAM a-d / ε e-h, SE19/SE45, 200·400 MPa), red=over/blue=under | μ=0.4 가 오차 최소; 고-f_CAM서 ε 일관 과소(under) = 소성 흐름 부재 |
| 20 | θ_SE vs f_CAM (SE19 a / SE45 b), 200·400, sim only | θ_SE 가 θ_CAM 보다 *먼저* 하락(조기 열화 지표) — 실험 측정 못 함(nano-CT 필요) |

## 6. Post-processing ★
- **무엇**:
  ① **porosity ε** — Monte Carlo 점 카운팅(eq11–22), additive 부피 보정, ω=0.7 가상박스 + box factor 10 + MC 30,000~50,000 점.  ε convention = bulk void(폴리결정 내부 공극 제외 명시 §2.10).
  ② **θ_CAM / θ_SE 이용률** — percolation cluster 분석(노드=입자, 이웃=중심거리<반경합).  separator 까지 연속경로 있는 *active/connected* 부피 분율.  (= 우리 f_AM^cc/dead-AM·dead-SE 와 같은 *이용률* 지표지만 σ 가중 없는 순수 기하.)
  ③ **민감도 지수 SI** — OAT, state 표준편차(eq25), f_CAM·압력별 정규화 행렬(Fig13) + 막대 랭킹(Fig14).
  ④ **RVE 수렴** — box size factor + side length ratio ω + MC 점수 3중 수렴 연구(Fig5–10).
  ⑤ **실험 θ_CAM** — 비방전용량/C_max,disch(=150 mAh/g) 정규화(eq1).
  ⑥ **실험 ε** — DF coin(9 mm) 무게·두께 → ρ_measured=m/(π(d/2)²h) (eq2) → ε=1−ρ_measured/ρ_theoretical (eq3).
- **도구**: LIGGGHTS(DEM) + MATLAB(자동화·MC porosity·percolation·SI·플롯).  실험 = 레이저회절 PSD(Horiba LA-960V2), EIS(Biologic VMP-300/VMP3), XRD(Rigaku), SEM(Phenom Pure).
- **수치화·플롯·기록 방식**: 8 파라미터 OAT 각 10 값, SE 2종 × f_CAM 4종 × 압력 3종.  모델 vs 실험 직접 오버레이(Fig18/19) + theoretical density(Fig17 빨강선)로 porosity 검증.  **민감도는 정규화(0–1) SI** 로 파라미터 간 비교.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (Bazzoun 2025) | 우리 | 차이 / 이유 (rigid·plastic / NMC532·811 / mono·bimodal / 민감도·솔버) |
|---|---|---|---|
| code | **LIGGGHTS** (Hertz spring+damping) | **LIGGGHTS** hooke/hysteresis | **같음(거의)** — 둘 다 LIGGGHTS no-cap 탄성 이력. 우리는 점착(adhesion) 추가, 그들은 순수 Hertz |
| **소성** | **없음** (순수 탄성 Hertz, CONTACT 소성조차 X) | DEM hooke/hysteresis(소성 無) + **Stage-E**(Tabor 소성면적 사후) + **MPM J2**(진짜 SHAPE) | **★ 우리가 두 단계 더 감**: 그들 = rigid 탄성구 only / 우리 = +Stage-E 접촉면적 +MPM 형상소성 |
| 입자 형상 | 구만, 형상 불변 | DEM 구·rigid / **MPM 진짜 형상변화** | **같음(DEM)** + MPM 고유. 그들 §3.1 "구=계산비용 타협" 명시 = frame[5] 확증 |
| E_SE | **20.5 GPa (real)** | E_eff 1.35(연화) / real 22–24 | 우리 1.35는 *압밀용 연화 프록시*(그들엔 없음); 전달 σ_grain 은 별도. 그들 real-E 압밀은 항복캡 없어 *고-f_CAM 불일치*로 귀결 |
| PSD | **mono-modal** (CAM 1 + SE 1, SE 2종 비교) | **bimodal/multimodal** (AM_P+AM_S+SE, 12:4:1) | **★ 우리가 더 현실적**: 그들은 SE 단봉 2종 *비교*뿐, 우리는 AM 자체가 bimodal → Furnas dip 표현 |
| 출력 | **θ_CAM·θ_SE·ε** (percolation *존재*·이용률·porosity) | porosity + **σ_ionic·σ_e·σ_thermal 삼중항** + coverage + Z + dip + fracture | **★ 그들은 전달 σ 없음**(2025); θ_CAM/θ_SE 는 percolation 연결성, σ 절대값 아님 |
| 전달 솔버 | **없음** (자매편 2026 이 FEM/RNM 추가) | **Kirchhoff + Holm + Stage-E** | **★ 우리 핵심 우위** — 2025 는 구조·캘리브레이션, 우리는 그 위에 σ |
| **민감도 분석** | **★ 정식 OAT, 8파라미터 × SI 랭킹** (μ_CAM-SE 1위) | 우리 σ-폼 ablation(항별 LOOCV)·E_SE 캘리브레이션은 있으나 *DEM 입력 8파라미터 정식 SI 미발표* | **★ 그들이 앞섬**: 체계적 파라미터 민감도 = 우리가 정식으로 안 한 것 |
| 캘리브레이션 검증 | **실험 θ_CAM·ε** (Mercedes-scale, 2 cell/조건) | solver=ground truth + Minnmann/Bazzoun2026 앵커 | **그들 실험 = frame[4] 외부 앵커**(우리 σ 검증과 보완) |
| **고-f_CAM 정확도** | **★ 저-f_CAM 정확 / 고-f_CAM(80–85) 현저 불일치 + 민감도 급증** (저자 명시) | Stage-E 소성면적 + MPM 소성흐름이 고-f_CAM rigid 천장 보정 | **★ 핵심 갭**: 그들 *명시 한계* = 우리 work 가 메우는 정확한 칸 |
| 압력 민감도 | "유의 추세 없음"(200–400서 ε·θ 압력영향 작다) | DEM Heckel P_y=138, 압력↑→ε↓ 명확 | 우리 Heckel 이 압력의존을 정량(그들은 압밀역학이 마찰에 묻혀 압력영향 약하게 봄) |
| Furnas dip | **미관측**(mono SE, 조성 4점만) | DEM·de Larrard dip @AM 70–85 wt% | **★ 우리 고유**: 그들 mono-PSD 4조성으론 dip 못 봄 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **★ 그들 민감도 랭킹(μ_CAM-SE 1위 > 마찰 3종 > E moderate > ν·COR 최저) = 우리 DEM 캘리브레이션 우선순위표**.  우리가 E_SE 만 집중 캘리브레이션(1.35 결정)했으나, 그들 SI 는 **마찰계수가 percolation·porosity·연결성의 단일 최강 레버**(특히 고-CAM)임을 정량 증명 → 우리 input 스크립트의 `*Friction*`/`*Roughness*` 설정이 *E 만큼 중요* 하다는 근거.  COR 은 거의 무영향(우리도 COR 튜닝 불필요 확인).  `docs/data/bazzoun2025_dem_sensitivity.csv` 에 SI 데이터.
- ② **그들 마찰값(μ=0.4 nominal, 0.2–0.6 범위) = 우리 LIGGGHTS 마찰 설정 sanity-check**.  우리 input(`input_real_*.liggghts`)의 SE-SE/CAM-CAM/CAM-SE 마찰이 0.2–0.6 밴드 안인지 점검.  μ=0.4 가 모델-실험 오차 최소(Fig19) → 우리 default 후보.
- ③ **★ 그들 "저-f_CAM 정확 / 고-f_CAM 불일치 + ε 과소" = 우리 Stage-E + MPM 의 존재 이유의 *외부 인용*.**  저자 §4.5/5.3 명시: 고-f_CAM서 모델이 *ε 를 과소*(under-predict) + *θ_CAM 혼합*(저-μ 과대/고-μ 과소) — 원인을 스스로 **"입자 형상·소성변형·혼합 거동 미반영"**(§5.5 future work)으로 진단.  → **우리 MPM 형상소성(void-fill)·Stage-E 소성 접촉면적이 정확히 이 갭을 메움** = "우리 work 가 SOTA DEM 의 *자인된* 한계를 해결" 이라는 가장 강한 positioning.
- ④ **실험 θ_CAM·ε 데이터 = frame[4] 외부 앵커**.  ε_sim<ε_exp(고-f_CAM)·θ_CAM 85wt% 급락(SE45 ~0.35) = 우리 dead-AM·dead-SE 경고와 같은 물리 → 우리 f_AM^cc<80% 경고를 그들 실험 θ_CAM 급락으로 검증.  단 CAM=NMC532(우리 811 과 조성차) → σ·균열 절대전이 주의, *압밀·이용률 추세* 만.
- ⑤ **작은 SE 의 고-f_CAM 이득**(SE19 가 SE45 보다 ε 낮고 θ_CAM·비용량 높음, 85wt%서 142.6/147.6 %↑) = 우리 "작은 SE→packing↑→percolation↑→σ↑"(size=packing)·bimodal 설계의 독립 실험 확증.  우리 12:4:1 의 작은 SE(D 1)가 큰 CAM 공극 채우는 것과 같은 이득.
- ⑥ **RVE/MC 방법론 대조**: 그들 box factor 10 + ω=0.7 + MC 30,000 점.  우리 RVE 수렴(box factor 35)·ε_sphere/union convention 과 *방법은 다르나 같은 문제*(벽효과·겹침 부피) → 우리 porosity convention 정당화에 비교 근거.

## 9. 인용 가능 문장 (deck/paper용)
- "A systematic OAT sensitivity analysis of a LIGGGHTS DEM cold-pressing model on the identical Li₆PS₅Cl/NMC system (Bazzoun et al. 2025) — varying 8 inputs across 1920 cases — identifies the CAM–SE interparticle friction coefficient as the single most influential parameter governing percolation, connectivity and porosity, especially at high CAM loading; Young's moduli rank moderate and Poisson ratios / coefficient-of-restitution lowest."
- "Crucially, the authors report that their rigid-sphere DEM achieves high accuracy at low f_CAM but exhibits notable discrepancies and increased parameter sensitivity at higher loadings, explicitly attributing the gap to unmodeled particle morphology, plastic deformation and mixing behavior — precisely the resolved-grain plastic regime our Stage-E plastic contact-area correction and J2-MPM shape plasticity fill (frame [5])."
- "This DEM-calibration study and its sister transport paper (Bazzoun 2026, FEM·RNM σ_ionic) together represent the closest peer to our pipeline — same group, same material, same LIGGGHTS code — yet neither resolves transport σ_electronic/σ_thermal nor true plastic morphology, the differentiators of our DEM↔MPM framework."

## 10. 주의/한계 (over-claim 방지)
- **★ 순수 탄성 강체구** — CONTACT 소성조차 *없음*(So 의 h_eq·H-cap, Thornton–Ning p_y, Varkey multi-contact 모두 없음).  순수 Hertz spring + 감쇠.  δ 는 *탄성* 겹침이지 소성 잔류 아님 → **압밀이 재배열 + 탄성 겹침으로만**, 형상흐름·void-fill *전무*.  이 점에서 So 2021·Varkey 2026 보다 *덜* 정교(소성 LAW 없음) — 단 *민감도·캘리브레이션* 은 가장 체계적.
- **★ 고-f_CAM 불일치는 *명시된* 한계** — 저자 스스로 80–85 wt% CAM 서 (i) ε 과소(under-predict), (ii) θ_CAM 저-μ 과대/고-μ 과소, (iii) 민감도 급증 보고.  원인 = 형상·소성·혼합 미반영.  ⇒ 그들 *고-f_CAM 절대값 전이 금지*(우리 production core AM 70–85 wt% 상단과 겹치므로 특히 주의) — **우리 MPM/Stage-E 가 메우는 칸임을 인용할 때만 사용**.
- **소재 = NMC532** (Ni₀.₅), 우리/Bazzoun 2026 의 **NMC811 (Ni₀.₈) 과 다름** → CAM 조성차.  E_CAM=161.5 는 공유하나 σ_e·균열·표면화학 절대 전이 금지.  *압밀·패킹·민감도* 는 NMC 조성 거의 무관(E·ρ 만) → 추세·방법은 적용 가능.  SE 는 LPSCl 동일(추세 직접 비교 OK).
- **mono-modal PSD** (SE 2종 *비교*, AM 단봉) → **Furnas dip 미관측**(조성 4점·단봉 SE).  우리 bimodal 12:4:1 dip 과 직접 비교 데이터 없음.
- **θ_CAM/θ_SE 는 percolation 연결성·이용률이지 σ 아님** — Kirchhoff/Holm·field·접촉저항 *전혀 없음*(2025).  σ 절대값은 자매편 Bazzoun 2026 소유.  "θ_CAM=1" 은 *완전 percolation* 이지 *최대 σ* 아님.
- **binder(CB/CNF/PTFE) = 질량 prefactor 만** (eq8) — 부피·연결성·이온저항 미모델.  저자 인정: θ 과대평가 가능.  우리 voxel σ-블로킹·CBD morphology 가 이 칸 보강.
- **압력 민감도 "유의 추세 없음"** 은 *그들 모델 한계*일 수 있음 — 마찰이 압밀을 지배해 200–400 MPa 압력영향이 묻힘.  우리 DEM Heckel(P_y=138, 압력↑→ε↓ 명확)·So 2021 다중압력 곡선과 대조 → 압력의존은 *항복캡 있는* 모델에서 더 뚜렷.
- **digitized 값은 추세만(±)** — θ_CAM/θ_SE/ε 의 Fig5–6/12/17/18 수치는 그림 읽은 근삿값.  stated(Table 1–3·5 파라미터, §4.4 감소율 %, 비방전용량, bulk σ 2.9/1.0, PSD D̄ 5.8/4.5/1.9)와 구분.
- **단일 그룹 NMC532·dry-film·Mercedes 공정** — 그들 실험 절대 θ_CAM·ε 는 *그들 공정* 산물(롤링 ~105 µm DF 시트, torque cell).  우리 공정·우리 소재(811)와 절대 동일시 금지, frame[4] 외부 *추세* 앵커로.

## ★ 우리 novelty — 왜 우리가 state-of-the-art 인가 (our novelty vs this DEM model)

> 이것은 **우리와 가장 가까운 peer**(같은 그룹·소재·코드)다.  따라서 차별점을 *정밀하게* 못 박는다.
> Bazzoun 2025(구조·캘리브레이션·민감도) + Bazzoun 2026(σ_ionic FEM/RNM)을 **합쳐도** 아래 7개 중
> 1·2·3·4·6·7 은 *그들에게 없다*.  5(민감도·실험)는 *그들이 앞서며*, 정직히 인정한다.

| # | 우리 차별점 (SOTA) | Bazzoun 2025 | Bazzoun 2026 (자매편) | 우리 |
|---|---|---|---|---|
| **1** | **전달 삼중항 σ_ionic+σ_e+σ_thermal** (Kirchhoff+Holm) | **없음** (θ_CAM/θ_SE = percolation *존재*·이용률만, σ 절대값 X) | σ_ionic 만(RNM, e/thermal 없음) | **σ_ionic(LOOCV 0.975) + σ_e(0.953) + σ_thermal(0.903) 전부** |
| **2** | **Stage-E 소성 접촉면적** (강체구 위에 Tabor+volume 으로 소성면적 재유도) | **없음** (순수 탄성 Hertz, 접촉면적=탄성 πR*δ만) | RNM 구속저항만(field spreading X)→고-CAM 과소 | **Stage-E 가 고-f_CAM rigid 천장의 접촉면적 과소를 직접 보정** |
| **3** | **DEM↔MPM scaffold + J2 소성 morphology** (진짜 형상흐름·void-fill) | **없음** (형상 불변 구; 고-f_CAM 불일치를 형상·소성 미반영으로 자인) | 없음(구만) | **MPM 가 그들 *자인된* 고-f_CAM 갭(소성흐름)을 메움** |
| **4** | **fracture-aware transport** (Auerbach 임계 + Lawn 미세asperity + f_intact) | 없음(파괴 미모델) | 없음 | **AM_P 균열(92:8 8mAh서 37–40%)→f_intact→partial-Holm σ** |
| **5** | **(그들이 앞섬, 정직)** 정식 OAT 8파라미터 민감도 + Mercedes-scale 실험 캘리브레이션 | **★ 보유** (μ_CAM-SE 1위 SI 랭킹, 1920 케이스, 실험 θ_CAM·ε) | (실험 EIS σ) | 우리는 *DEM 입력 8파라미터 정식 SI 미발표* (σ-폼 ablation·E_SE 캘리브레이션만) → **흡수·인용 대상** |
| **6** | **literature-grounded σ_grain** (Cronau 단결정 3.0 ×Cronau(r_SE) sub-µm + Trevisanello NCM + Wang) | n/a(σ 안 풂; bulk EIS 2.9/1.0 측정만) | bulk pellet 1.02(정규화 σ=1 S/cm 상대) | **σ_grain 물리 앵커 명시** |
| **7** | **solver→scaling-law LOOCV predictor** (설계값→전 metric 예측, frame[4]/[5] 독립 이중모델) | n/a(예측식 없음) | n/a | **σ_ionic 0.975 등 예측식 + DEM(전달)·MPM(역학) 독립 보정** |

**정밀 매핑 (이 peer 한정):**
- **그들 θ_CAM/θ_SE = percolation EXISTENCE + utilization** 이지 **transport σ 가 아니다**.  "CAM 이 separator 까지 연속경로로 연결됨" = 우리 f_perc/percolation *조건*에 해당.  우리는 *그 위에* Holm 구속저항·Kirchhoff 전류해·Stage-E 소성면적을 얹어 **σ 절대값**을 낸다.  ⇒ Bielefeld(2019, percolation·utilization, σ 안 풂) → **Bazzoun(2025, 같은 그룹, θ_CAM/θ_SE percolation+utilization)** → Bazzoun(2026, RNM σ_ionic 추가) → **우리(σ 삼중항 + Stage-E + MPM)** 라는 *그룹-내부 진화의 자연스러운 끝* 에 우리가 놓인다 (positioning 최강 근거; comparison_vs_ours.md §E 와 일관).
- **그들 *자인된* 고-f_CAM 한계 = 우리 #2·#3 의 존재 이유**.  §4.5/5.3/5.5 명시: 고-f_CAM 서 (i) ε 과소, (ii) θ_CAM 혼합오차, (iii) 민감도 급증, 원인 = *형상·소성·혼합 미반영*.  → **우리 Stage-E(소성 접촉면적) + MPM(소성 형상흐름·void-fill)** 가 정확히 이 세 결손을 해결.  "SOTA DEM 이 *스스로 인정한* 갭을 우리가 메운다" = 가장 방어 가능한 novelty 주장.
- **정직한 한계 인정 (#5)**: 그들은 **정식 파라미터 민감도(OAT/SI)** + **Mercedes-scale 실험 캘리브레이션**(1920 케이스, 2 cell/조건, dry-film 공정)에서 *우리보다 앞선다*.  우리는 σ-폼 ablation(항별 LOOCV)·E_SE 3-seed 캘리브레이션은 했으나 *DEM 8개 물리입력의 체계적 SI 랭킹은 미발표*.  → 이건 *경쟁* 아니라 **흡수**: 그들 μ_CAM-SE 1위 랭킹을 우리 캘리브레이션 우선순위로 채택(§8①).

## 적용가능성 (applicability to our LIGGGHTS DEM model)

> 같은 LIGGGHTS·같은 소재(SE)·같은 공정이므로 **직접 적용 가능성이 가장 높은 peer**.

1. **민감도 랭킹 → 캘리브레이션 우선순위 (직접 적용)**:
   - 그들 정규화 SI(Fig14): **μ_CAM-SE > μ_SE-SE ≈ μ_CAM-CAM > E_SE > E_CAM > ν_SE ≈ ν_CAM ≈ COR**.
   - 우리 input 스크립트(`input_real_*.liggghts` 등)의 **마찰 3종이 E 만큼 중요** → 우리가 E_SE(1.35) 만 집중한 것을 보완해 **마찰 캘리브레이션 우선순위 상향**.
   - COR(RC) 거의 무영향 → 우리도 COR 튜닝 deprioritize (그들 확증).
   - ⚠ 단 우리는 *전달 σ* 가 출력 → 민감도 순위가 *porosity/percolation* 기준(그들)과 *σ* 기준(우리)에서 다를 수 있음 → 우리 σ-출력에 대한 자체 SI 는 별도 검증 필요(흡수 후보).

2. **마찰값 sanity-check (직접)**:
   - 우리 LIGGGHTS 마찰계수가 그들 **0.2–0.6 밴드·nominal 0.4** 안인지 점검.  μ=0.4 가 모델-실험 오차 최소(Fig19) → 우리 default 후보값.
   - 우리 `*Friction*`/접촉 설정을 그들 (μ_SE-SE/CAM-CAM/CAM-SE)=0.4 와 대조.

3. **실험 θ_CAM·ε = frame[4] 외부 앵커 (간접, 추세)**:
   - ε_sim/θ_CAM-vs-f_CAM(Fig18) + 비방전용량(Fig16) = 우리 dead-AM(f_AM^cc<80% 경고)·porosity@P 의 *추세* 검증점.
   - ⚠ NMC532·dry-film·Mercedes 공정 → 절대 동일시 금지, *추세* 만(85wt%서 θ_CAM 급락 = 우리 dead-AM 물리).

4. **RVE/MC porosity 방법론 (방법 대조)**:
   - box factor 10 + ω=0.7 + MC 30,000~50,000 점 = 우리 RVE 수렴·ε_sphere/union convention 정당화 비교 근거.
   - 그들 MC porosity(겹침 영역 CAM 귀속) vs 우리 ε_sphere(소성 보존)/ε_union(기하 상한) — convention 차이 명시.

5. **우리가 *흡수* 할 것 (정직)**:
   - **정식 OAT 8파라미터 SI** → 우리 DEM σ-출력에 대한 같은 OAT 민감도 분석(우리 미발표).
   - **마찰 통합(effective μ)** 단순화 = 우리 마찰 설정 단순화 청사진.
   - **theoretical density 대비 검증**(Fig17 빨강선) = 우리 porosity 절대검증 방법.

## Appendix — 수식 (재현용)
- 운동방정식: m_i·ẍ_i = Σ F_ij + F_i^ext (eq4); I_i·ω̇_i = Σ r_i×F_ij + T_i (eq5, T_i=rolling friction 토크).
- 접촉력: F_ij,n = k_ij,n·δ_ij,n − γ_ij,n·u_ij,n (eq6); F_ij,t = k_ij,t·δ_ij,t − γ_ij,t·u_ij,t (eq7).
- 강성: k_n=(4/3)E*√(R*δ_n), k_t=8G*√(R*δ_t) (eq26).  감쇠 γ_n/γ_t = f(RC) (eq27).
- 등가량: 1/R*=1/R_i+1/R_j (eq28); 1/m*=1/m_i+1/m_j (eq29); 1/E*=(1−ν_i²)/E_i+(1−ν_j²)/E_j (eq30); 1/G*=2(2−ν_i)(1+ν_i)/E_i+2(2−ν_j)(1+ν_j)/E_j (eq31).  벽: R/m/E→∞ 라 해당항 0.
- Coulomb 절단: F_ij,t^final = F_ij,t (|F_t|≤μ|F_n|) / μ|F_n|·(F_t/|F_t|) (|F_t|>μ|F_n|) (eq32).
- 질량보정: m_tot=(m_CAM+m_SE)/(1−f_add) (eq8).  θ_CAM=V_CAM^active/V_CAM^total (eq9); θ_SE=V_SE^connected/V_SE^total (eq10).
- porosity(MC): v_X=N_X/N_total (eq11–13); V_X=v_X·V_box (eq14–16); m_X=V_X·ρ_X (eq17–18); V_add=f_add·m_tot/ρ_add (eq19–21); ε=(V_void−ΣV_add)/V_box (eq22).
- 실험: θ_CAM=C_spec.disch/C_max.disch (eq1, C_max=150 mAh/g); ρ_meas=m/(π(d/2)²h) (eq2); ε=1−ρ_meas/ρ_theo (eq3).
- 민감도: q_i=q_l+(i−1)(q_u−q_l)/(N_s−1) (eq23), q̄=(q_l+q_u)/2 (eq24); SI=√(1/N_s·Σ(x_ij−x̄_i)²) (eq25).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

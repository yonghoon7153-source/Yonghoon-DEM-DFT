# DEM-기반 미세구조 생성 + FEM·RNM으로 복합 양극 이온전도도 평가 — Bazzoun (J. Power Sources 2026)

> slug `bazzoun2026_dem_fem_rnm_ionic` · DOI `10.1016/j.jpowsour.2025.238682` · type `DEM+FEM+RNM` · PDF `Bazzoun_2026_JPowerSources_DEM_FEM_RNM_IonicConductivity_ASSB.pdf` · digested `2026-06-23` · status ✅

## 1. 한 줄 요약
**우리와 정확히 같은 소재(LPSCl+NMC811)·같은 코드(LIGGGHTS)·같은 전달물리(Holm 접촉저항+Kirchhoff)**로
복합 양극의 유효 이온전도도 σ_eff,ion을 DEM→FEM·RNM으로 뽑고 **실험 EIS로 검증** — 우리 σ_ionic
파이프라인의 독립 평행 구현(frame [4] 교차검증)이자, 우리가 부족했던 **실험 절대 앵커**를 제공.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| A.M. Bazzoun, J. Piruzjam, S. Hink, L. Rubacek, A. Fill, K.P. Birke (Mercedes-Benz + Univ. Stuttgart + Helmut Schmidt) | J. Power Sources 661 (2026) 238682 | 10.1016/j.jpowsour.2025.238682 | **Li₆PS₅Cl + NMC811** (POSCO) + CNF + PTFE | DEM+FEM+RNM, 실험 EIS 검증 |

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| σ_eff,ion (exp) | **0.137 / 0.101 / 0.065 mS/cm** | f_CAM 70/75/80 wt%, 400 MPa | stated | full-blocking EIS |
| bulk LPSCl σ | **1.02 mS/cm** | pellet 400 MPa | stated | GB-incl < Cronau 단결정 3.0 |
| σ vs 압력 (RNM) | 70%: 0.068→0.135 / 75%: 0.035→0.079 / 80%: 0.008→0.031 | 100→400 MPa | endpoint text-derived | +98/+126/+291 %, ~400 포화 |
| E_SE | **22.1 GPa** | LPSCl | stated | ≈ 우리 real 24 |
| ν_SE / E_CAM / ν_CAM | 0.37 / 161.5 GPa / 0.30 | | stated | |
| PSD (D10/D50/D̄/D90) | SE 0.71/1.49/2.00/3.80 · CAM 3.90/5.50/6.00/7.62 µm | | stated | SE≪CAM |
| 조성 (wt%→vol% CAM:SE) | 70:27.7→45:53 · 75:22.7→52:46 · 80:17.7→60:38 | CNF:PTFE 2:0.3 고정 | stated | |

## 4. 시뮬레이션 방법 ★
- **code**: **LIGGGHTS** (DEM) + COMSOL Multiphysics (FEM) + in-house MATLAB (RNM).
- **DEM 접촉법칙**: 법선 **Hertzian spring + damping** (= 우리 hooke/hysteresis 계열), 접선 damping spring.
  구형 CAM+SE. 마찰 μ(SE-SE/CAM-CAM/CAM-SE)=0.4, COR=0.4. PID 제어로 **일정 단축 압축압력** 유지.
- **재료 파라미터**: E_SE 22.1, ν_SE 0.37, E_CAM 161.5, ν_CAM 0.30, ρ_SE 1.64 / ρ_CAM 4.77 g/cm³.
- **bond/binder 모델**: CNF/PTFE(~3.4 wt%)는 DEM 도메인에서 **제외** (eq 2 질량보정 `m_tot=(m_CAM+m_SE)/(1−(f_CNF+f_PTFE))`); 부피·침투 영향 작다는 근거.
- **MPM/continuum**: 없음 (DEM→연속체는 FEM이 담당).
- **전달 솔버** ★ (= 우리 솔버):
  - FEM: SE 상 추출·메싱 → 정상상태 확산 `∇·J=0, J=−σ∇φ` (eq 3), Dirichlet φ₁=1V/φ₀=0V,
    절연 Neumann. `σ_eff,ion = qL/(A_dom·Δφ)` (eq 6). GMRES.
  - RNM: SE 입자=노드, 접촉=저항. **`R^IJ=1/(2σ·r_c)` (eq 8) = Holm 1967 그대로**; 입자-전극 `1/(4σr_c)` (eq 9).
    접촉반경 구-구 교차(eq 10)/변형깊이 `r_c=√(r²−(r−δ)²)` (eq 11). Kirchhoff `Σ(φi−φj)/R=0` (eq 12).
    고유 σ=1 S/cm 정규화 → **상대추세**(절대는 bulk로 스케일). Birkholz 방법.
- **입자 처리** ★: **구만** (형상변화 없음). mono-PSD 분리(SE D50 1.49, CAM 5.50). rigid 입자 +
  CONTACT 탄성(Hertz) — **진짜 SHAPE 소성 아님**. 침투 SE만 전달평가.
- **도메인/RVE**: 직육면체 10D̄×10D̄(측방)×15D̄(수직), 측방 주기경계. 초기 패킹 ~75 %. 최대속도 0.2 µm/µs.
  조성당 **독립 실현 10개**. box factor(RVE) 수렴 35.
- **네트워크 지표**: θ_SE=V_connected/V_total(SE-이용률, eq 16), R̄_SE-SE(평균 접촉저항, eq 18),
  Z_SE-SE(배위수, eq 19).

## 5. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | DEM 압밀 과정 + FEM/RNM 워크플로 | 우리 DEM→네트워크 파이프라인과 1:1 대응 |
| 2 | RNM 저항망 모식 (R^IJ, R^I,0) | = 우리 Holm/Kirchhoff 그림 |
| 3 | SEM·XRD·PSD·bulk EIS (σ_SE=1.02) | bulk LPSCl 앵커(pellet, GB-incl) |
| 4 | Z-type TLM EIS 피팅 (R_ion/R_elec/CPE) | σ_eff,ion 실험 추출법 |
| 6c | σ_eff,ion exp vs FEM vs RNM (f_CAM 70/75/80) | **실험 절대 검증점**; RNM 고-CAM 과소 |
| 7 | SE 크기 효과 (D̄_SE 1–8µm) | 작은 SE→σ↑ (우리 size=packing 일치) |
| 8 | σ vs 압력 (100–400 MPa) | 다중압력 σ_ionic(우리 Heckel knee 비교) |

## 6. Post-processing ★
- **무엇**: FEM 확산 풀이(σ_eff,ion), RNM Kirchhoff(σ_eff,ion), 네트워크 지표 θ_SE/Z_SE-SE/R̄_SE-SE,
  실험 EIS **Z-type TLM**(transmission line) 피팅으로 R_ion 추출 → `σ=l/(R·a)` (eq 1).
- **도구**: COMSOL(FEM), in-house MATLAB(RNM, Birkholz), RELAXIS-3(EIS 피팅).
- **수치화**: RNM이 **FEM 대비 32–98× 빠름**(Table 5: FEM 2551–3352 s vs RNM 26–105 s).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 접촉저항 | R=1/(2σr_c) (Holm) | 동일 Holm | **같음** ✓ |
| 전류해 | Kirchhoff Σ(φi−φj)/R=0 | 동일 | **같음** ✓ |
| E_SE | 22.1 GPa (real) | E_eff 1.35(연화) / real 24 | 우리 1.35는 압밀용 프록시; 전달은 σ_grain 별도 |
| σ_grain 앵커 | pellet 1.02 mS/cm (GB-incl) | Cronau 단결정 3.0 ×Cronau(r_SE) | pellet<단결정(GB) — 일관; 이중계상 점검 필요 |
| 전달 채널 | σ_ionic만 | σ_ionic + σ_e + σ_thermal | 우리 삼중항 우위 |
| 접촉면적 보정 | RNM 구속저항만 (field spreading X) → 고-CAM 과소 | Stage-E 소성 접촉면적(Tabor+volume) | 우리 Stage-E가 그들 과소를 보정 방향 |
| 검증 | **실험 EIS**(조성+압력) | solver=ground truth (외부 실측 부족) | **그들 실험이 우리 외부 앵커** |
| FEM continuum | 보유(COMSOL) | 없음 | 흡수 가치 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **실험 절대 앵커 도입**: σ_eff,ion 0.137/0.101/0.065 @f_CAM 70/75/80 (400 MPa) + bulk 1.02 mS/cm
  → 우리 σ_ionic 폼/솔버의 외부 검증점 (그들 vol% CAM:SE 45/53→60/38 을 우리 φ_SE로 매핑 후). `docs/data/bazzoun2026_sigma_ionic.csv`.
- ② **다중압력 σ-vs-P**(100–400, ~400 포화) ↔ 우리 Heckel P_y 138 / σ-vs-ε. "missing direct validation" 보강.
- ③ **RNM(구속) vs 우리 Stage-E(소성면적)** 같은 구조 대조 → Stage-E 기여 정량(고-CAM 과소 보정폭).

## 9. 인용 가능 문장 (deck/paper용)
- "An independently-calibrated DEM→resistor-network model on the identical Li₆PS₅Cl/NMC811 system
  (Bazzoun 2026), using the same Holm constriction resistance and Kirchhoff balance as our solver,
  reproduces the composition and pressure trends of σ_eff,ion and validates them against EIS —
  providing an external experimental anchor (0.137/0.101/0.065 mS/cm at f_CAM = 70/75/80 wt%)."

## 10. 주의/한계 (over-claim 방지)
- **구만** (형상변화 없음) → 우리 MPM morphology는 안 다룸 (frame[5] 전달 절반).
- **RNM 구속저항만**: FEM/실험 대비 과소, 고-CAM서 심함(80 % RNM 0.031 ≪ exp 0.065) — field spreading 부재.
- σ 정규화 σ=1 S/cm(상대) → 절대는 bulk 스케일링 가정 (우리 Cronau σ_grain과 다름, 직접 절대비교 주의).
- LPSCl 동일소재라 **추세·물리 직접 비교 가능** (Varkey halide와 달리) — 단 그들 φ 정의(vol% CAM:SE) 매핑 선행.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

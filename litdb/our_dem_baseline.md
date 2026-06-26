# 🎯 우리 DEM+MPM 기준값 — 모든 문헌 비교의 기준점

> 출처: CLAUDE.md(상보 프레임 [1]–[5] + 세션 결과). 문헌 digest의 §7은 항상 이 표와 대조.
> 소재: LPSCl Li₆PS₅Cl SE + NMC811 CAM. 핵심 인식 = **DEM = 전달 / MPM = 역학** (두 모델을
> 서로가 아니라 각각 실험에 보정 — frame [4]).

## 0. 소재 파라미터
| 물성 | 값 | 비고 |
|---|---|---|
| E_SE (real bulk) | **22–24 GPa** | LPSCl 단결정/벌크 (Bazzoun 22.1, lit 24) |
| E_SE (DEM effective) | **1.35 GPa** | 18× 연화 — granular 재배열/GB-slide/micro-fracture 럼핑 프록시 |
| E_SE (MPM champion) | **1.53 GPa**, σ_y 0.15 (2D) / 0.30 (3D) | softened-J2; SEM morphology + pure-SE 앵커 일치 |
| ν_SE | 0.49 (MPM, stiff-bulk) / 0.37 (real) | bulk만 real, shear만 soft = 부피보존 granular flow |
| E_CAM (NMC811) | 140 GPa | (Bazzoun 161.5, lit 140) |
| σ_grain (이온) | 3.0 mS/cm | Cronau 2022 단결정 · ×Cronau(r_SE) sub-µm 인자 |

## 1. 압밀 / porosity (frame [1]–[3])
| 항목 | 우리 값 | 방법 |
|---|---|---|
| pure-SE porosity @300 MPa | **~10 %** | Minnmann 실험 앵커; MPM 3D σ_y=0.30 → 10.0 % 재현 |
| real_14 composite @300 MPa | **15.6 %** (DEM) / 16.7 % (MPM scaffold) | DEM 측정 / MPM se-dump (1.2%p = 수렴된 모델차) |
| pure-SE Cronau overlap | **11–12 %** | SE 하중지지 시 (lens exact) — Cronau 소성 floor 재현 |
| Heckel | **R²=0.965, P_y=138 MPa, σ_y_eff≈46 MPa** | DEM pure-SE 4압력 |
| 강체 구 porosity floor | **~20 %** | 소성 흐름 없으면 못 넘음 |
| Furnas dip | AM ~70–85 wt% | DEM·de Larrard 기하 — **소성 연속체 MPM은 재현 못 함** (frame [4] 증명) |

## 2. 전달 삼중항 (Phase 1 — 스케일링 법칙)
| 채널 | LOOCV | 형태 |
|---|---|---|
| **σ_ionic** | **0.975** (n=88, 5 OLS) | σ_grain·Cronau·√φ_eff·CN²·√cov_Hertz·f_p³·C(τ) |
| **σ_electronic** | **0.953** (n=76, 8 LIVE+2 LOCK) | Trevisanello endpoints·φ_AM⁴·√A·... Stage 22.5 |
| **σ_thermal** | **0.903** (n=82, 14 Ridge) | 멀티패스 — 단일 backbone 안 됨, Ridge irreducible |
- Ground truth = 네트워크 솔버 (Kirchhoff, Holm 1967 접촉저항 R=1/(2σr_c)). Stage-E = 소성 접촉면적(Tabor+volume).
- fracture-aware Holm (f_intact), Auerbach 균열, percolation/coordination/coverage(Hertz·Tabor).

## 3. MPM 고유 (frame [5] — 역학/morphology)
- 진짜 소성 입자 형상변화 (SEM 코어보존+경계평탄화 ✓), 부피보존 void-fill flow,
  공간 누적소성변형장 Σdg(열화 개시), 응력장, SE bridge 채널폭.
- scaffold 커플링: 실제 DEM AM 위치 고정 + SE만 MPM → porosity 15.93 %·두께 29.95µm EMERGE.
- coverage plastic(deformed) vs rigid(geometric): Hertz 16 % / Tabor 52 % (real_14).

## 4. 핵심 발산 / 한계 (비교 시 주의 — frame [1] LIMITS)
- **rigid-sphere DEM**: 입자 형상 안 변함 — δ overlap은 소성 프록시, 진짜 흐름 아님. 18× 연화로 보상.
- **MPM continuum**: 명시적 접촉 네트워크 없음 → transport σ 못 줌(DEM 영역). Furnas dip 못 재현(기하 부재).
- **2D ≠ 3D**: 절대 스케일 다름 (3D가 흐름 방향 많아 더 치밀; σ_y 2D 0.15 → 3D 0.30 필요).
- **연화는 IRREDUCIBLE** (resolved-grain): cap/shear-jam/bulk-jam 전부 Heckel 재현 실패 →
  압밀 Heckel은 접촉-네트워크 현상(DEM·homogenized-REV DPC 소유), MPM은 morphology 소유.

## 5. 비교 시 체크리스트 (method 의존성)
- **소재**: halide(E~10.6 GPa) ≠ LPSCl(E_eff 1.35 / real 24) → 절대 porosity·σ 직접 비교 금지, 추세만.
  더 뻣뻣한 SE → 더 높은 floor (우리 MPM E-sweep: E24→33-38 %, E1.35→8 %와 정합).
- **소성 종류**: CONTACT 탄소성(δ 프록시) vs 진짜 SHAPE 소성(MPM) — 논문이 어느 쪽인지 먼저 명시.
- **전달**: 그들 RNM(구속저항만)은 FEM/실험 대비 과소(고-CAM서 심함) → 우리 Stage-E 소성면적이 보정 방향.
- **digitized**: 그림에서 읽은 값은 추세만(±), stated 텍스트 값과 구분.
- **frame [4]**: DEM↔MPM 강제 일치(cross-fit) 금지. 수렴=교차검증, 발산=정량화된 모델한계.

# DEM으로 생성한 3D 복합 양극 미세구조에 3D Lattice Boltzmann 열전도 모델로 ETC를 푼 연구 — Huang (J. Energy Storage 2025)

> slug `huang2025_dem_lbm_heat_conduction_composite_cathode` · DOI `10.1016/j.est.2025.115692` · type `DEM+LBM (mixed)` · PDF `Huang_2025_JEnergyStorage_DEM_LBM_HeatConduction_CompositeCathode.pdf` · digested `2026-06-26` · status ✅
>
> ★ Paper #26 — **DEM + thermal**: 우리 σ_thermal 채널의 가장 직접적인 문헌 카운터파트. 우리와 *같은 워크플로의 절반*(DEM으로 미세구조 생성)을 공유하되, 열전도는 **접촉망 저항(Kirchhoff/Holm)이 아니라 voxel화된 3D Lattice Boltzmann 연속체 PDE**로 푼다. 소재는 **산화물 LCO/LLZO**(우리 황화물 LPSCl/NCM 아님 → 절대값 전이 금지, 추세만).

---

## 1. 한 줄 요약
DEM(in-house)으로 LCO(=AM)+LLZO(=SE) 복합 양극 미세구조를 압밀 생성한 뒤, **3D D3Q19 Lattice Boltzmann 열전도 모델**로 유효 열전도도(ETC, k_eff)를 계산하고, **porosity·체적비(vol-fraction)·입자크기·tortuosity** 네 인자를 스윕하여 ETC에 미치는 영향을 정량화. 결론: **porosity·체적비·입자크기 셋 다 결정적(decisive), tortuosity는 무시 못 할(non-negligible) 인자**. = 우리 σ_thermal Ridge 폼(porosity·se_se_cn·tortuosity_median/std·접촉면적에 의존)의 **다중경로(multi-pathway) 주장과 같은 물리적 메시지**를 *독립 방법(LBM)·다른 소재(oxide)*로 재현.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| Juan Huang, Jiawei Hu, Duo Zhang, Yuheng Du, Chuan-Yu Wu, **Qiong Cai**(교신) — Univ. of Surrey, UK | J. Energy Storage **114** (2025) 115692 | 10.1016/j.est.2025.115692 | **SE = LLZO** (Li₇La₃Zr₂O₁₂, 산화물 garnet) · **CAM = LCO** (LiCoO₂) | **DEM**(미세구조 생성) + **3D LBM**(열전도 ETC). 실험은 *packed steel-particle* 검증 1건 (양극 직접 아님). |

- 접수 2024-10-16, 개정 2025-01-31, 게재 2025-02-10. EPSRC/UKCOMES + Horizon Europe OPERA 지원, J. Huang CSC 장학.
- ⚠ **소재가 우리와 다름**: 산화물 LLZO(k=0.46 W/m·K, σ_ion 별도)·LCO. 우리는 황화물 LPSCl(냉간가압 치밀화)+NCM811. → ETC 절대값·k 값 전이 금지. **방법론·구조→열 추세만** 우리에 매핑.
- ⚠ **DEM 코드 = in-house** ("LIGGGHTS" 아님; 본문은 LIGGGHTS를 *언급만* 하고, 실제 사용은 자체 thermomechanical-adapted in-house code [36–38]). 우리 LIGGGHTS와 코드 다름.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **k_LCO** (AM 고유 열전도) | **5.40 W m⁻¹ K⁻¹** | — | stated (Table 1) | ρ=5.06 g/cm³, Cp=715.42 J/kg·K, α_T=1.49×10⁻⁶ m²/s |
| **k_LLZO** (SE 고유) | **0.46 (0.47±0.01) W m⁻¹ K⁻¹** | — | stated (Table 1) | ρ=5.11, Cp=927.19, α_T=1.00×10⁻⁷ m²/s. **k_LCO/k_LLZO ≈ 11.7×** |
| k_pore (기공) | ≈ 0 (near-vacuum) | ASSB 기공 = 진공/글러브박스 | stated (§2.3.2) | 액체 없음 → **단열 진공 기공**이 열을 막음 (대류·복사 무시) |
| **ETC k_eff (LBM)** | **0.41 – 4.02 W m⁻¹ K⁻¹** | 스윕 전체 범위 | stated (Table 5/6/7/8/9) | 최저 I-c5(1:4, 31.2% poro)·최고 I-b1(4:1, 4.4% poro) |
| porosity 스윕 | **4.4 / 8.1 / 15.1 / 21.1 / 31.2 %** | DEM 압밀로 조절 | stated (Table 5) | 압밀 깊이로 5수준 |
| CAM:SE 체적비 | **1:1 / 4:1 / 1:4** (LCO:LLZO) | §4.1 | stated (Table 4) | + §4.3 CAM vol% 30–70 % 스윕 |
| 입자크기 | LCO/LLZO = 3·5·6·10 µm 조합 | §4.3 (3:3/6:3/3:6/6:6/5:5), §4.2 (5/10) | stated (Table 4/9) | 단봉(mono) per phase, 위상별 단일 크기 |
| tortuosity τ (TauFactor) | pore 5.3–15.2 · LCO 1.35–32 · LLZO 1.57–14.8 | 위상별·방향별(X/Y/Z) | stated (Table 5/7/8/9) | percolation 안 되면 "inf" |
| E_LCO / ν_LCO | n/a (명시 안 함) | — | n/a | Hertz-Mindlin-Deresiewicz 쓰나 E·ν 값 본문 미기재 |
| E_SE / σ_y / Heckel P_y | **n/a** | — | n/a | **압밀 역학 정량 없음** — DEM은 *구조 생성기*로만, 항복/Heckel/coverage 미산출 |
| σ_ionic / σ_e / coverage / Z | **n/a** | — | n/a | **열전도 단일 채널** — 이온·전자·배위수·coverage 전부 안 다룸 |

→ **이 논문이 주는 숫자 = ETC(k_eff) vs (porosity·vol-frac·size·tortuosity) 의 정량 맵**. 전부 `docs/data/huang2025_etc_vs_microstructure.csv`.
→ **안 주는 것** = 우리 핵심 절대 앵커(porosity@P 정량, σ_ion/e, coverage, Z, E_SE, Heckel) — 이 논문은 *열*에만 집중.

## 4. 시뮬레이션 방법 ★
### (A) 미세구조 생성 — DEM
- **code / version**: **in-house thermomechanical DEM** ([36–38]; LIGGGHTS는 비교 문헌으로만 언급, 실사용 아님). MATLAB로 grid 통계(체적비·porosity), **TauFactor**로 tortuosity.
- **DEM 접촉법칙**: 고전 **Hertz–Mindlin–Deresiewicz** (마찰 탄성 입자, **adhesion·정전기력 없음**).
  - 법선력 (eq 4): F_n = (4/3)·E*·R*^½·α^{3/2} (Hertz; α=overlap, E*·R* = 등가 모듈러스·반경, eq 5/6).
  - 접선력 (eq 7–13): 증분 Mindlin–Deresiewicz, no-slip(θ_k=1 if |ΔF_s|<μF_n) / partial-slip(θ_k 식 11/12), 하중·제하·재하 경로(k=0,1,2), 접촉반경 r_c=√(αR*) (eq 8).
  - 벽 접촉 시 벽 반경 = 무한대.
- **재료 파라미터**: E_i, ν_i, R_i (eq 6에 등장하나 **수치 본문 미기재** → n/a). 마찰 μ·COR 값도 본문 미기재. ρ_LCO 5.06 / ρ_LLZO 5.11 g/cm³ (Table 1).
- **bond/binder 모델**: **없음** (바인더/CBD 미포함; pristine 양극만).
- **압밀 절차** (Fig 2): ① red(LCO)+blue(LLZO) 입자를 3D 컨테이너(80×80×**430** µm)에 랜덤 생성 → ② 중력 침적·정지 → ③ **top plate를 v=0.003 m/s 등속 하강**으로 압축 → 최종 **80×80×100 µm** bed로 압밀. porosity는 압밀 깊이로 조절. **PBC(주기경계)**로 인공 가장자리 효과 제거, 3D 배위수(이웃 수) 랜덤화로 국소 군집 회피(자연 granular 균일성).
- **MPM/continuum**: **없음** (DEM→열은 LBM이 담당).
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - **구만(spherical grains)**. LCO 실제는 hexagonal layered지만 **구로 근사**(저자 명시 근거: ① 다공질 미세구조 모델링에 구가 표준, ② 실제 LCO는 ball-milling 등 가공으로 구형에 가까움 + spherical LCO 합성·성능 우위 문헌[33,34], ③ 효율적 패킹·빠른 수렴). 비구형은 **future work**로 명시 보류.
  - **mono-PSD per phase** (위상별 단일 크기; 진짜 PSD 분포 아님). §4.3에서 LCO/LLZO 크기를 *케이스별 고정값*으로 바꿔 크기효과 스윕.
  - ★ **rigid sphere + CONTACT 탄성(Hertz)** — **진짜 SHAPE 소성 전혀 없음**. 입자는 압밀 후에도 완벽 구. δ-overlap이 압밀의 유일한 변형. → **우리 MPM이 메우는 형상-소성 간극을 이 논문도 똑같이 안 가짐**(Varkey/Bazzoun과 동일 frame[1]/[2] 한계). 게다가 **항복캡조차 없음**(adhesion-free 순수 Hertz) → 우리 DEM hooke/hysteresis보다도 단순한 탄성 접촉.

### (B) 열전도 — 3D Lattice Boltzmann (LBM)
- **격자**: **D3Q19** (3차원 19속도) LBM, advection-diffusion 기반. 점성가열·Dufour·Soret 무시. **속도 u=0**(고체상 전도만; ASSB 기공은 진공이라 유체대류 없음 → LBM의 convection 항 제거가 핵심 단순화).
  - 지배식 (eq 14): ∂T/∂t + ∇·(uT) = ∇·(α_T∇T) + S. u=0 → 순수 확산.
  - 평형분포 (eq 16→17): f_α^eq = w_α·T (u=0이므로 단순화).
  - 이산진화 (eq 18): f_α(r+e_α·Δt, t+Δt) − f_α(r,t) = −(1/τ_T)[f_α(r,t)−f_α^eq(r,t)] + Δt·w_α·S.
  - 온도 T = Σf_α (eq 19). 열확산도 α_T = c_s²[τ_T − ½]Δt (eq 20).
- **상별 다중-시간척도(multi-time-scale)** ★: LCO·LLZO의 α_T가 **>10× 차이**(1.49×10⁻⁶ vs 1.00×10⁻⁷ m²/s). 같은 격자·시간척도에서 완화계수 ω=1/τ_T는 0.4<ω<0.95 안에 둬야 안정(ω<0.4 or >0.95 발산). 단일 격자로는 둘 다 만족 불가 → **상마다 시간척도(time-step 내 iteration 수)를 다르게**: LCO ω=0.6177, LLZO ω=0.7984; **한 time-step = LCO 10 iteration + LLZO 1 iteration**. Δt=2.5×10⁻⁶ s. (Servan-Camas LTRT 대안은 복잡 기하에 부적합 → multi-time-scale 채택.)
- **경계조건** (Fig 4, Table 2):
  - **상단(top)**: Neumann **일정 열유속 q=200,000 W/m²** (heat flux in).
  - **하단(bottom)**: Dirichlet **T_substrate=343 K**.
  - **측면(vertical)**: 단열(adiabatic).
  - **LCO/LLZO 계면**: 두 상의 Cp가 달라 계면 경계 처리 필요 → **국소열평형(LTE) 가정**: 계면 grid를 **Dirichlet T_e**로 (eq 21–23): ΔQ_i=Cp_i·m_i(T_i−T_e), T_e=(Cp₁ρ₁T₁+Cp₂ρ₂T₂)/(Cp₁ρ₁+Cp₂ρ₂) (질량가중 평형온도). 계면 검출 = voxel을 LCO=1/LLZO=2/pore=0로 디지털화 → 3종 계면(1/2, 2/pore, 1/pore) 식별 후 BC 적용 (Fig 5).
  - ⚠ **계면 열저항(thermal boundary resistance/Kapitza) 미포함**: LCO/LLZO 나노계면 열저항 실험값이 문헌에 없어 명시적으로 안 넣음(future work). → ETC는 *계면 저항 없는 상한* 경향.
- **ETC 추출** (eq 24): **k_eff,xi = q_loss / (∂T/∂x_i)** = 열유속 ÷ 전도방향 온도구배. 수치적으로 k_eff = q_loss·Δx_i/ΔT. (packed-particle 검증은 Robin BC + Nu/Ra 자연대류 보정 eq 25–29.)
- **수렴**: L²-norm of 온도장 (eq 30), 기준 ε=1×10⁻⁷ K. ~6×10⁵ iteration, 물리시간 3000 s.
- **도메인/RVE / seeds / 압력범위**:
  - 양극 샘플 **80×80×100 µm** (최대입자 10 µm의 ≥7.5× → REV 충족; 총 grid **80×80×100 = 640,000**). **mesh(grid) = 1 µm**.
  - **mesh 독립성 검증**: 5 해상도(1·2·1.333·0.667·0.5 µm)에서 ETC 불변 확인 → coarse 1 µm로 충분 (21.1% poro, LCO 5/LLZO 10 µm, 1:1).
  - seeds: 명시 없음(랜덤 packing, 케이스당 1개로 보임). 압력: **압밀압 명시 안 됨**(plate 등속 하강 변위제어 = 우리 hold 프로토콜과 같은 계열, target 압력 아님).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | ASSB 셀 모식 (Al 집전체 / LCO+LLZO 양극 / Li 음극 / Cu) | 복합 양극 = AM+SE 입자 혼합 (우리와 같은 구도) |
| 2 | **DEM 압밀 4단계** (생성→침적→plate 압축→80×80×100 bed); porosity 8.1%·LCO:LLZO 1:1 예시 | = 우리 DEM 압밀 워크플로의 절반. plate 변위제어 = 우리 hold 프로토콜 |
| 3 | LBM 열전도 흐름도 (mesh→초기화→상별 collision/streaming→계면 BC→수렴) | **상별 multi-time-scale** 구현 (α_T 10× 차이 처리) |
| 4 | **경계조건 모식**: 상단 q=200,000 W/m², 하단 343 K, 측면 단열 | ETC 추출 BC = 1방향 열유속/온도구배 |
| 5 | **계면 검출**: voxel을 0/1/2로 디지털화 → 3종 계면(1/2·2/pore·1/pore) 식별 | voxel화 미세구조에서 상-계면 BC 거는 법 |
| 6 | 계면평형온도 T_e (질량가중, eq 23) 모식 | LTE 가정 (계면 열저항 무시) |
| 7 | **packed steel-particle 열전달 실험 장치** (D=41 mm 튜브, 6.35 mm 강구, TC1–6 열전대) | **유일한 실험 검증**(양극 아님 — packed bed 대리검증) |
| 8 | 실험 vs LBM 온도-높이 곡선 (TC1–6, 343→300 K) | LBM 모델 검증 OK (good consistency) |
| 9 | **3D 온도분포** (Case I-a1/b1/a5/b5; 전체상·LCO·LLZO 분리) (a) + 전도방향 온도구배 (b) | 저-poro(4.4%)는 균일, **고-poro(31.2%)는 큰 구배**(진공기공이 국소 열장벽). LLZO상에 작은 구배도 hotspot 가능 |
| 10 | **ETC vs porosity** (Case I-a 1:1·I-b 4:1·I-c 1:4) ★ | **porosity↑ → ETC↓ 단조**; **체적비: 4:1(LCO多)>1:1>1:4**. LCO가 LLZO의 ~11.7× 전도 → CAM多가 ETC↑ |
| 11 | **유사-tortuosity 그룹**(Case II-a) tortuosity·ETC(X/Y/Z) | 비슷한 τ → ETC 좁게(0.895–0.967) = 등방·균일 |
| 12 | **다른-tortuosity 그룹**(Case II-b) tortuosity·ETC(X/Y/Z) | 다른 τ → ETC 넓게(0.758–1.306) = 이방성. **τ_pore↑ → ETC↑**(기공 우회가 길수록 열이 고체로 감) |
| 13 | **MPR(3차 다항회귀) 예측 ETC vs LBM 시뮬 ETC** (R²=0.9852, p=2.8×10⁻¹³) | tortuosity 3종(pore·LCO·LLZO)으로 ETC 회귀 — **다중인자 비선형 결합** |
| 14 | **ETC vs CAM vol%(30–70%)** 5 입자크기 케이스 (poro 7% 고정) ★ | **CAM%↑ → ETC↑** 단조; **작은 입자(3:3µm)>큰 입자(6:6µm)** (작은 입자 = 접촉多·고체상 τ↓) |

## 6. Post-processing ★
- **무엇**:
  - **ETC(k_eff)** = LBM 정상상태 온도장에서 q_loss/(∂T/∂x) (eq 24).
  - **tortuosity** = **TauFactor**(MATLAB) [35]로 위상별(pore/LCO/LLZO)·방향별(X/Y/Z) 산출. **percolation 안 되면 "inf"**(전도방향 미연결 시 τ 측정 불가).
  - **porosity / 체적비** = grid(voxel) 통계 (MATLAB).
  - **EMT(effective medium theory)** 비교 (eq 31): 완전랜덤·균질 가정 다성분 EMT k_eff = Σk_i·v_i·d/[(d_i−1)k̄+k_i] / Σv_i·d/[…], d=3. 해석 벤치마크.
  - **MPR(multivariate polynomial regression, 3차)** (eq 32–33): ETC를 τ_pore·τ_LCO·τ_LLZO 의 3차 다항(교호항 포함)으로 회귀. MATLAB `MultiPolyRegress`(A. Cecen) 사용. **R²=0.9852, p=2.8×10⁻¹³** → ETC↔3-tortuosity 강한 비선형 관계 확인.
  - **interconnected solid/pore 분율** (Table 6): 연결된 고체상은 전 케이스 >99% (강건), 연결 기공상은 porosity와 함께 0.213%(I-a1)→74.265%(I-a5) 급증(고립공극→연결공극망 전이).
- **도구**: in-house DEM([36–38]), in-house 3D LBM(Surrey), MATLAB(voxel 통계 + MPR), **TauFactor**(tortuosity).
- **수치화·플롯·기록 방식**: Table 5(porosity·τ·ETC·EMT), Table 6(LBM vs EMT + interconnected%), Table 7/8(τ X/Y/Z·표준편차), Table 9(입자크기×CAM% ETC), Fig 10/14(ETC 곡선), Fig 13(MPR parity).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **미세구조 생성** | **DEM 압밀** (Hertz, 구만, plate 변위제어) | DEM 압밀 (LIGGGHTS hooke/hysteresis, 구만) + MPM 소성 morphology | **워크플로 절반 같음** ✓ (둘 다 DEM 강체 구) — 단 우리는 MPM으로 소성 SHAPE 추가 |
| **열전도 솔버** | **3D LBM** (voxel 연속체 PDE, ∇·(α∇T)=0) | **접촉망 저항(Kirchhoff)** + 각 접촉 Holm 구속저항 1/(2σr_c) + Stage-E 소성 접촉면적 | **방법 근본적 다름**: 그들=필드 PDE on voxel / 우리=lumped resistor on contact graph |
| **열 채널** | 열전도(ETC) **단일** | σ_ionic + σ_e + **σ_thermal**(삼중항, 동일 접촉망) | **우리 삼중항 우위**; 그들은 별도 LBM solve가 *열만* |
| **계면/접촉 모델** | voxel 계면 LTE(eq 23) + **계면 열저항 무시** | Stage-E **소성 접촉면적**(Tabor+volume) + Holm 구속 | 그들=기하 voxel 접촉만 / 우리=소성-면적 인지 constriction |
| **소재** | **산화물 LCO/LLZO** (k_LCO 5.40 / k_LLZO 0.46) | 황화물 LPSCl/NCM811 | **절대값 전이 금지** (oxide≠sulfide; k·σ·압밀거동 다름) |
| **입자 소성** | rigid 구 + Hertz(항복캡도 없음) | DEM 강체 구 + MPM **진짜 J2 소성**(SEM 일치 morphology) | 우리 MPM이 *형상* 메움 (frame[5]) |
| **파괴** | 없음 (pristine만; degradation은 future) | Auerbach/fracture-Holm (AM_P 92:8 8mAh 37–40% cracked) + f_intact | **우리 균열-인지 열화 우위** |
| **검증** | packed steel-bed 실험 1건 (양극 아님) | solver=ground truth + 외부 실험 앵커(Minnmann/Bazzoun/Lee) | 둘 다 양극 직접 열 검증은 부재 |
| **설계 예측속도** | 케이스마다 **LBM 재계산**(6×10⁵ iter) | σ_thermal **스케일링 폼**(Ridge 14-feat, LOOCV 0.90) = 즉시 예측 | 우리 폼 = 디자인 인스턴트, 그들은 매번 재solve |
| **연속체 필드** | **공간 온도장 보유**(Fig 9 3D T분포, hotspot) | lumped resistor → 공간 T장 없음 | **그들 우위**: spatial gradient/hotspot 해상 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **σ_thermal 다중경로 주장의 *독립* 교차검증 (frame[4]).** 그들도 **porosity·vol-frac·size·tortuosity 넷이 다 결정적, 단일 인자로 안 줄어든다**고 결론 → MPR을 *3-tortuosity 3차 다항*(R²=0.985)으로 푼 것 자체가 "열전도 ≠ 단일 power-law"의 증거. ⇒ 우리 "σ_thermal은 14-feature Ridge, 순수 power-law는 LOOCV 0.59에서 막힘, 2상 Bruggeman EMT는 R²<0(neg)" 결론과 **방법·소재 다른데 같은 메시지**. ★ **인용 무기**: "An independent DEM+LBM study on an oxide composite (Huang 2025) likewise finds thermal transport governed jointly by porosity, volume fraction, particle size AND tortuosity — requiring a 3rd-order multivariate regression rather than a single scaling — corroborating our multi-pathway σ_thermal form."
- ② **EMT 불신의 외부 근거.** 그들 EMT(eq 31)는 고-poro·LCO-dominated에서 LBM 대비 크게 빗나감(I-a5 EMT 0.874 vs LBM 0.542 = +61% 과대; I-c1 −28% 과소). = 우리 σ_thermal에서 **Bruggeman EMT가 음의 R²**로 실패한 것과 같은 결론(이상화·등방·연속 경로 가정이 이질·이방 양극을 못 잡음). Bielefeld 2020 "Bruggeman 4× 과소"와 합류 → **EMT는 벤치마크일 뿐 예측 불가**.
- ③ **tortuosity 항을 우리 폼에 *방향성*으로.** 그들 핵심: **τ_pore↑ → ETC↑**(기공 우회 길수록 열이 고체로 우회), **τ_LCO(고체상)↑ → ETC↓**(전도상 경로 꼬임 = 저항↑), τ_LLZO는 영향 작음(저-전도상이라). 우리 Ridge는 `tortuosity_median`·`tortuosity_std`를 쓰되 **위상 미분리** → ★ 흡수 후보: 우리 열 폼에 *pore-tortuosity*(우회=양)와 *solid-phase tortuosity*(전도상=음) **부호 반대 두 항**으로 분리. (backlog A6 pore-τ DiffuDict와 연결.)
- ④ **LBM을 우리 DEM dump의 *열 cross-check 솔버*로 도입 검토.** §B 적용가능성 참조 — 우리 DEM dump를 voxel화 → 우리 자체 LBM(또는 TauFactor τ만)으로 ETC를 독립 산출 → 우리 Kirchhoff σ_thermal과 frame[4] 교차검증. 단 소재 k는 LPSCl/NCM 값으로 교체.

## 9. 인용 가능 문장 (deck/paper용)
- "A DEM-generated microstructure coupled to a 3D Lattice Boltzmann heat-conduction solve (Huang 2025, Surrey) on an oxide LCO/LLZO composite cathode finds porosity, volume fraction and particle size all decisive for the effective thermal conductivity, with tortuosity a non-negligible factor — and requires a 3rd-order multivariate (3-tortuosity) regression to fit the ETC (R²=0.985), an independent corroboration of our multi-pathway σ_thermal claim that composite thermal transport does not reduce to a single scaling law."
- "Their LBM is a continuum field PDE on a voxelised DEM microstructure resolving spatial temperature gradients and hotspots; our Kirchhoff/Holm contact-network resistor solve instead delivers all three transport channels (ionic, electronic, thermal) from one explicit contact graph with plastic-area-aware constriction — complementary methods on the same DEM packing."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **소재 = 산화물 LCO/LLZO**(k_LCO 5.40 / k_LLZO 0.46 W/m·K). 우리 황화물 LPSCl/NCM811과 k·σ·압밀거동 전부 다름 → **ETC·k 절대값 전이 절대 금지, 구조→열 추세만**.
- ⚠ **rigid 구만 + Hertz(항복캡·adhesion 없음)** → 진짜 SHAPE 소성 전무. 우리 MPM morphology 간극은 이 논문도 못 메움(frame[1]/[2]). 게다가 우리 DEM hooke/hysteresis보다 단순(adhesion-free).
- ⚠ **계면 열저항(Kapitza) 미포함** → ETC는 *계면 저항 없는 상한* 경향(실제 LCO/LLZO 나노계면은 추가 저항 → 실 ETC는 더 낮을 것). 저자 명시 future work.
- ⚠ **압밀 정량 없음**: DEM은 *구조 생성기*로만 — porosity는 plate 변위로 *조절*하되 **압력·Heckel·coverage·배위수 미산출**. → 우리 porosity@P / Heckel 앵커와 직접 비교 불가.
- ⚠ **실험 검증 = packed *steel* bed**(양극 아님) — LBM 솔버의 일반 타당성만 검증, *복합 양극 ETC 실측 검증은 아님*. ASSB 양극 열실험은 "challenging/unreliable"이라 대리 검증.
- ⚠ **DEM code = in-house**(LIGGGHTS 아님). 우리 LIGGGHTS와 코드 다름 — "같은 코드"라 말하면 안 됨.
- ⚠ **단봉 입자(위상별 단일 크기)** — 진짜 PSD 분포·bimodal 12:4:1·Furnas dip 미탐구. 크기효과는 *케이스별 단일 크기 비교*지 *분포* 효과 아님. → 우리 dip은 그들이 비운 칸.
- ⚠ ETC 일부(Fig 10/14 곡선의 보간점)는 표값 사이 추세 — Table 5/7/8/9의 *표 stated 값*만 정밀, 곡선 보간은 TREND.

---

## 우리 DEM+MPM 대비 (comparison vs ours)

> 핵심 질문: 그들 **DEM+LBM ETC**(voxel 연속체 열-PDE)와 우리 **σ_thermal 채널**(Kirchhoff 접촉망 resistor + Stage-E Tabor/volume 접촉면적 + Wang phonon-GB σ_grain)은 *같은 구조→열* 문제를 *다른 방법*으로 푼다. 같은 결론에 도달하는가?

### (1) 워크플로 — 절반은 같다, 절반은 근본적으로 다르다
- **같은 절반 (DEM 미세구조 생성)**: 둘 다 *강체 구 DEM 압밀*로 AM+SE 복합 양극 미세구조를 만든다. 그들 plate 변위제어(v=0.003 m/s 하강) = 우리 **hold 프로토콜**(LIGGGHTS 변위정지)과 같은 계열. 둘 다 **구만**(no shape plasticity), 둘 다 PBC, 둘 다 3D 배위수 랜덤화.
- **다른 절반 (열전도)** ★ 핵심 대비:
  - **그들 = LBM 연속체 필드 PDE on voxel**: 미세구조를 1 µm voxel로 디지털화 → 각 voxel에 상별 α_T 부여 → D3Q19 LBM으로 ∇·(α∇T)=0 풀어 *공간 온도장* 전체를 얻고, 상단/하단 BC의 열유속/구배에서 ETC 추출. **공간 분해능 있음**(Fig 9 hotspot).
  - **우리 = lumped resistor on contact graph**: 입자=노드, *접촉*=저항. 각 SE-SE/AM-AM/AM-SE 접촉에 **Holm 구속저항 1/(2σ·r_c)**(우리 σ_thermal은 열-아날로그), Kirchhoff Σ(φi−φj)/R=0 풀어 유효 σ_thermal. **공간 온도장 없음**(접촉망 등가저항만) — 대신 **접촉별 소성면적(Stage-E Tabor+volume)·percolation·배위수·fracture를 명시 보유**.
  - ⇒ **상보적(complementary)**: 그들 LBM은 *어디가 뜨거운지*(spatial gradient/hotspot)를 주고, 우리 망솔버는 *접촉망이 얼마나 열을 흘리는지 + 그 망이 이온·전자도 동시에 흘리는지(삼중항)*를 준다. 둘 다 같은 DEM 패킹 위.

### (2) 결론 일치 — 다중경로(multi-pathway)를 *독립 재현*
- **그들 결론**: porosity·vol-fraction·particle-size **셋 다 decisive**, tortuosity **non-negligible**. 그리고 결정적으로, **ETC를 단일 인자/단일 power-law로 못 줄여** **3차 다항 MPR(τ_pore·τ_LCO·τ_LLZO 교호항)** R²=0.985로 회귀.
- **우리 σ_thermal 결론**(CLAUDE.md "Stage T1 FINALIZED"): κ는 **MULTI-PATHWAY**(AM-AM/AM-SE/SE-SE 병렬, 조성의존 k_weights) → 단일 backbone 스케일링 불가. A/B/C 스크린: 순수 power-law LOOCV 천장 0.59, 2상 Bruggeman EMT baseline R²<0, **14-feature Ridge만 0.90**. 핵심 features = porosity·log(se_se_cn)·**tortuosity_std·tortuosity_median**·gb_density·접촉면적(area_SE_SE/area_AM_SE)·n_components·fracture flags…
- ⇒ ★ **방법(LBM vs Kirchhoff)·소재(oxide vs sulfide)·구현 다른데 *같은 메시지*: 복합 양극 열전도는 porosity+조성+크기+tortuosity의 비선형 결합이며 단일 스케일링으로 안 줄어든다.** 그들 MPR 3차(R² 0.985, p 2.8e-13) ≈ 우리 Ridge 14-feat(LOOCV 0.90)이 둘 다 *다인자 회귀를 강제* → **우리 multi-pathway 주장의 독립 외부 확증(frame[4])**.
- **세부 정합**:
  - **porosity 중심성**: 그들 ETC vs porosity 단조 감소(Fig 10) = 우리 thermal 폼 1번 feature가 porosity(forward-selection LOOCV 0.50, 단일 최강). ✓
  - **tortuosity 비무시**: 그들 τ를 *핵심 회귀변수*로 = 우리 tortuosity_median(15번째 feature, "0.9 돌파")·tortuosity_std(3번째). ✓ 단 ★ 그들은 **위상별 τ 분리**(pore↑→ETC↑, solid↑→ETC↓ 부호 반대), 우리는 위상 미분리 → 흡수 후보(§8-③).
  - **접촉/연결성**: 그들 interconnected solid >99%·pore 0.2→74% = 우리 se_se_cn(2번째 feature)·n_large_components(연결성). ✓
  - **EMT 실패 공통**: 그들 EMT ±28~61% 빗나감 = 우리 Bruggeman EMT R²<0. ✓

### (3) 우리가 못 주는 것 (그들 우위, 정직)
- **공간 온도장/hotspot**: 그들 LBM은 양극 내부 3D 온도구배·국소 hotspot(Fig 9: 고-poro 31.2%서 inlet 340→outlet 295 K 큰 구배; 저-전도상에 작은 구배도 hotspot)을 *해상*. 우리 lumped resistor는 등가 유효 σ_thermal만 → **공간 hotspot 못 봄**. (단 우리 MPM은 *응력/소성변형* 공간장은 보유 — 열장은 아님.)
- **산화물 k 데이터**: k_LCO 5.40 / k_LLZO 0.46 (산화물 garnet). 우리 황화물 계엔 없음.

## 적용가능성 (applicability to our LIGGGHTS DEM model)

> 구체적으로: 그들 LBM ETC를 우리 σ_thermal Stage-T1의 *독립 열 기준*으로 쓸 수 있는가? 어떻게?

- **(A) LBM을 우리 DEM dump의 열 cross-check 솔버로 도입 (frame[4] 교차검증).**
  - 경로: 우리 LIGGGHTS dump(예: `input_real_14`, atom 좌표+반경) → **voxel화**(우리 `scripts/extract_2d_microstructure.py`/`viz_mpm_continuum.py`가 이미 voxel/mesh 파이프라인 보유 → 3D voxel union으로 확장) → 각 voxel에 **우리 소재 k**(k_LPSCl·k_NCM·k_pore≈0) 부여 → 3D LBM(또는 더 가볍게 **TauFactor τ만** 산출 후 우리 식에 투입) → ETC 독립 산출.
  - 의미: 우리 **Kirchhoff σ_thermal**(접촉망)과 **LBM ETC**(voxel 필드)를 같은 DEM 구조 위에서 비교 = **두 독립 열-방법의 교차검증**. 일치 → 우리 σ_thermal 신뢰 보강; 불일치 → 정량 모델한계(constriction 유무·계면저항). **DEM·MPM·실험을 서로 교차검증하던 frame[4]에 *열-방법* 축을 추가.**
  - ⚠ **소재 swap 필수**: 그들 k는 oxide. 우리는 k_LPSCl(황화물, 문헌값)·k_NCM811·k_pore≈0(우리도 진공기공 — *같은 조건*, ASSB 공통). k 값만 교체하면 *방법은 그대로 적용 가능* (LBM은 소재-무관 솔버).
- **(B) tortuosity↔ETC 매핑을 우리 `tortuosity_median` feature로.**
  - 그들 TauFactor τ(위상별·방향별) = 우리 σ_thermal Ridge의 `tortuosity_median`·`tortuosity_std`와 **같은 양**(우리도 TauFactor 계열 정의). ★ 그들 **위상-부호 분리**(pore-τ 양 / solid-τ 음)를 우리 폼에 흡수 시도 = 직접 적용 가능한 정량 lever(§8-③, backlog A6 pore-τ DiffuDict).
- **(C) ETC 곡선을 우리 σ_thermal *형태* 검증.**
  - 그들 Fig 10(ETC vs porosity 단조↓)·Fig 14(ETC vs CAM% 단조↑, 작은입자>큰입자) = 우리 σ_thermal이 porosity↑→κ↓·AM↑→κ↑(고전도 AM多)·작은입자→접촉多→κ↑를 *재현하는지* 정성 체크. (단 절대값은 oxide → 형태만.)
  - ⚠ **방향 주의**: 그들 "CAM(LCO)↑→ETC↑"는 **LCO가 LLZO의 11.7× 전도**라서(고전도상이 AM). 우리는 **NCM(AM)이 LPSCl(SE)보다 열전도 높음** 여부를 우리 k로 확인해야 부호 같음(NCM ~수 W/m·K vs LPSCl 황화물 ~0.5–1 → 같은 방향 가능성↑, 단 우리 k 값으로 확정 필요).
- **(D) 한계**: 그들 LBM은 *계면 열저항 없음* → 우리가 도입 시 LPSCl/NCM 계면 Kapitza 저항(문헌 부족, 우리 Stage-E 접촉면적이 부분 대용)도 같이 고려. 그리고 LBM은 *구조당 재solve*(6×10⁵ iter, 무겁다) → 우리 스케일링 폼(즉시)의 *검증용*으로만, 생산 예측은 우리 폼 유지.

## ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this DEM model)

> 이 논문은 2025년 J. Energy Storage의 **열전도-특화 DEM+LBM** 연구다. 그러나 우리 DEM+MPM 파이프라인은 *열을 포함한 전 영역*에서 더 앞선다. 증거 기반으로 못박는다:

1. **삼중항 from ONE 접촉망 vs 그들 별도 LBM solve (열만).** ★ 최강 차별점.
   우리는 **하나의 명시적 접촉 그래프**에서 σ_ionic(LOOCV 0.975) + σ_electronic(0.953) + **σ_thermal**(0.90)을 *동시에* 푼다 — 같은 노드·같은 접촉·같은 Holm 구속물리(채널별 σ만 교체). Huang은 **열전도 단일 채널**이고, 그조차 *별도 LBM 재계산*(6×10⁵ iteration)이 필요하다. 이온·전자 전달은 *전혀 다루지 않음*. ⇒ 우리는 *복합 양극 설계의 3대 수송을 일관 프레임에서*, 그들은 *열 하나를 무거운 PDE로*. **SOTA = 통합 삼중항.**

2. **Stage-E 소성 접촉면적이 열 constriction에 들어간다 (plastic-area aware) vs LBM 기하 voxel 접촉.**
   우리 σ_thermal의 각 접촉저항은 **Stage-E(Tabor 소성 + volume 접촉면적)** 로 보정된 *실제 소성 변형 면적*을 쓴다 — 압밀로 입자가 눌리며 넓어진 접촉을 열이 더 잘 흐르는 물리. Huang LBM은 **voxel 기하 접촉**(눌린 구의 겹침 voxel)만 — *소성 면적 확대 미반영*(애초에 항복캡 없는 순수 Hertz). ⇒ 우리 열 솔버가 *압밀-소성 물리를 면적에 반영*, 그들은 기하만.

3. **DEM↔MPM scaffold = 진짜 소성 morphology vs 그들 rigid-구 패킹(형상변화 0).**
   우리는 DEM AM 골격(real_14 scaffold)에 **MPM J2 소성 SE**를 채워 *진짜 입자 형상변화*(SEM 일치: 코어보존+경계평탄화)·void-fill flow·공간 변형장 Σdg를 얻는다(`scripts/mpm3d_compaction.py --se-dump`). Huang은 **완벽 구 rigid**(저자 명시: 비구형=future work) — 형상 전혀 안 바뀜. ⇒ 우리 morphology 채널은 그들에 *존재하지 않음* (frame[5] 분업: 그들=transport 절반의 *열만*, 우리=transport 삼중항 + mechanics morphology 둘 다).

4. **균열-인지(fracture-aware) 열화 vs 그들 균열 전무.**
   우리는 Auerbach/Lawn 균열(AM_P 92:8 8mAh서 37–40% cracked) + f_intact·frac_severe로 **균열이 수송(이온·전자·열 다)을 깎는** 효과를 모델 — σ_thermal 폼에도 `am_vulnerable_pct`·fracture flags가 들어감. Huang은 **pristine만**(degradation = 명시적 future work). ⇒ 우리는 *열화된 양극*의 열까지, 그들은 *무손상*만.

5. **문헌-grounded Wang phonon-GB σ_grain (열) + Cronau GB (이온).**
   우리 σ_thermal은 Wang phonon-GB 산란을 σ_grain prefactor에 반영(입계 phonon 산란). 입계 물리를 *재료-수준*으로 반영. Huang은 단일 상-내 균질 α_T만(입계 phonon 산란 미반영, LTE 계면 평형온도뿐).

6. **실험-앵커 독립 보정 (frame[4]).** 우리 DEM·MPM은 각각 *실험*에 독립 보정(Minnmann porosity·σ_ion / Bazzoun σ_eff,ion / Lee σ / Doux porosity), 서로 cross-fit 안 함. Huang의 양극 열 검증은 **packed steel-bed 대리실험 1건**(양극 직접 ETC 실측 없음). ⇒ 우리 보정 앵커가 *재료-특이 실측*에 더 직접.

7. **σ_thermal 스케일링 폼(LOOCV 0.90) = 즉시 설계 예측 vs 그들 per-microstructure LBM 재solve.**
   우리는 14-feature Ridge 폼으로 *디자인 입력→κ 즉시 예측*(ML 예측기에 탑재, Phase 3). Huang은 새 미세구조마다 **LBM을 6×10⁵ iteration 재계산**(무겁다). ⇒ 우리 = 설계 루프 인스턴트, 그들 = 검증용 1샷.

### 그들이 *앞서는* 점 (정직 — over-claim 금지)
- ★ **진짜 연속체 필드 PDE(LBM)** → 양극 내부 *공간 온도장·열구배·국소 hotspot*을 해상(Fig 9: 고-poro서 inlet-outlet 45 K 구배, 저-전도상 hotspot). 우리 lumped resistor 망은 **등가 유효 κ만** → 공간 온도분포 *못 봄*. 이건 우리가 갖지 않은 능력(우리 MPM은 *응력/소성* 공간장은 있어도 *열* 공간장은 없음). 만약 우리가 "어디가 열폭주 위험"을 보려면 그들 LBM-류 필드 솔버를 *추가*해야 함(§적용가능성-A).
- **산화물 LCO/LLZO k 데이터**(5.40 / 0.46 W/m·K) — 우리 황화물 계엔 없는 외부 소재점.
- **mesh 독립성·수렴(L²<1e-7)·MPR(R² 0.985) 깔끔한 수치 위생** — 방법론 성숙도.

⇒ **결론**: 열전도 *공간 해상*은 그들(LBM)이 앞서지만, **복합 양극 설계에 필요한 수송 삼중항·소성 면적·morphology·균열·즉시-예측**은 모두 우리가 SOTA. Huang은 *열 단일 채널의 무거운 필드 솔버*이고, 우리는 *통합 multi-physics 설계 엔진*. 그들의 multi-pathway 결론(porosity+조성+크기+τ 비선형 결합, EMT 실패)은 오히려 **우리 σ_thermal Ridge-폼의 독립 외부 확증**으로 우리 편이다.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

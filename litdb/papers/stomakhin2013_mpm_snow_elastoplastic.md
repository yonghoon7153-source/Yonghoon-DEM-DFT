# 눈(snow) 시뮬레이션을 위한 Material Point Method — Stomakhin (ACM TOG 2013, SIGGRAPH)

> slug `stomakhin2013_mpm_snow_elastoplastic` · DOI `10.1145/2461912.2461948` · type `MPM` · PDF `Stomakhin_2013_ACMTOG_MaterialPointMethod_SnowSimulation.pdf` · digested `2026-06-26` · status ✅

> ⚠ WISHLIST Tier-4 #22 (MPM 탄소성). **컴퓨터그래픽스(UCLA+Disney) 논문 — 배터리·LPSCl·NMC 와 무관**.
> 우리에게 중요한 이유는 단 하나: **우리 MPM 가족(`mpm3d_compaction.py`, `mpm2d_*`)이 직접 계승하는
> 탄소성 MPM(EP-MPM)의 원전·대중화 논문.** 핵심 수확 = ① 변형구배 곱분해 **F = F_E·F_P** + ② **return
> mapping**(특이값 클램프) 알고리즘 = 우리 SE 소성압밀 엔진의 *알고리즘 토대*; ③ 그들의 snow 소성(점착·
> 압축경화·압축성 cap-유사) vs 우리 **von Mises J2**(등적) 구성식 대조; ④ F_P ↔ 우리 누적소성변형 Σdg.
> Frame[5]: MPM = 우리의 **역학/morphology 절반**(연속체 소성 엔진).

---

## 1. 한 줄 요약
"눈"을 **사용자 제어형 탄소성 연속체**로 보고, 입자(Lagrangian point)↔배경 격자(Eulerian grid) 하이브리드인
**Material Point Method(MPM)**로 푼 SIGGRAPH 논문. 핵심 알고리즘 = 변형구배를 **탄성·소성으로 곱분해
`F = F_E·F_P`**(multiplicative elasto-plasticity)하고, 매 스텝 탄성 trial 변형구배의 **특이값을 임계 압축/
신장 구간 `[1−θ_c, 1+θ_s]`로 클램프(return mapping)** 하여 초과분을 소성으로 넘기며, **압축될수록 단단해지는
hardening**을 Lamé 계수에 지수적으로 넣어 눈의 흐름·뭉침·균열·파쇄를 한 구성식으로 재현. 이 **F_E·F_P 분해 +
특이값-클램프 return mapping** 이 오늘날 그래픽스 EP-MPM의 표준이 되었고, **우리 MPM SE 압밀의 알고리즘적 뼈대**다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| A. Stomakhin, C. Schroeder, L. Chai, J. Teran (UCLA), A. Selle (Walt Disney Animation Studios) | ACM Trans. Graph. **32(4)** Article 102 (July 2013), SIGGRAPH | 10.1145/2461912.2461948 | **해당 없음 — 눈(snow), 물+얼음 혼합 연속체.** 우리 소재(LPSCl/NMC)와 무관; *알고리즘*만 전이 | 그래픽스 시뮬레이션: 하이브리드 Eulerian/Lagrangian **MPM** + 탄소성 구성식 (in-house, semi-implicit) |

> ⚠ 이 논문은 σ_ionic·porosity·Heckel·EIS 같은 **배터리 물성을 전혀 다루지 않는다.** §3 핵심물성 표는
> "snow 구성식 파라미터"로 채우며, 우리 비교(§7)는 *물성 절대값*이 아니라 *알고리즘·구성식 구조* 차원이다.

## 3. 핵심 물성 (수치) — snow 구성식 파라미터 (Table 2)
| 물성 | 값 | 조건 (의미) | stated/digitized | 비고 |
|---|---|---|---|---|
| 초기 영률 E₀ | **1.4×10⁵ Pa = 0.14 MPa** | 눈 | stated (Table 2) | ★ 우리 MPM SE champion 1.53 GPa보다 **~1.1만 배 연함**(눈이므로 당연) |
| Poisson ν | **0.2** | 눈 | stated | ★ **압축성** 재료. 우리 MPM SE는 ν=0.49(stiff-bulk, 등적 granular flow) — 정반대 선택 |
| 임계 압축 θ_c | **2.5×10⁻²** | F_E 특이값 하한 `1−θ_c=0.975` | stated | 소성 압축 개시. 작을수록 powdery(가루눈) |
| 임계 신장 θ_s | **7.5×10⁻³** | F_E 특이값 상한 `1+θ_s=1.0075` | stated | 소성 신장/파쇄(fracture) 개시. 작을수록 chunky(덩어리) |
| 경화계수 ξ (hardening) | **10** | μ,λ ∝ exp(ξ(1−J_P)) | stated | ★ **압축될수록 단단**. 클수록 brittle, 작을수록 ductile |
| 초기밀도 ρ₀ | **4.0×10² kg/m³** | 눈 | stated | (참고: LPSCl SE bulk ≈ 1640–2000 kg/m³로 훨씬 무겁다) |
| Lamé μ₀ (전단) | **5.83×10⁴ Pa** | E₀,ν에서 유도 | derived | μ₀=E₀/(2(1+ν))=58.3 kPa |
| Lamé λ₀ | **3.89×10⁴ Pa** | E₀,ν에서 유도 | derived | λ₀=E₀ν/((1+ν)(1−2ν))=38.9 kPa |
| FLIP/PIC 블렌드 α | **0.95** | v=(1−α)v_PIC+α v_FLIP | stated (§4.1) | FLIP 지배. **우리는 APIC/MLS-MPM(후속) 사용** |
| 격자당 입자수 | **4–10 ppc** | 초기 패킹 눈 | stated (§11) | 우리도 유사(resolved-grain n_grid 256–768) |
| dt (explicit) | **~1×10⁻⁵ s** | CFL 안정한계 | stated (§11) | 명시적 한계 |
| dt (semi-implicit) | **~5×10⁻⁴ s** | backward/trapezoidal Euler | stated (§11) | ★ **~50배 큰 스텝**; CG 10–30회, preconditioner 불필요 |

> 배터리 물성(porosity@P / σ_ionic / σ_e / σ_thermal / coverage / Z / Heckel P_y / PSD)은 **전부 n/a**
> (눈 시뮬레이션 논문이라 존재하지 않음).

## 4. 시뮬레이션 방법 ★ — 이 논문의 본체
> 여기가 우리에게 중요한 전부. 알고리즘을 *논문 수준*으로 옮긴다(수식 exact).

- **code / version**: in-house **MPM**(Material Point Method). 격자 = 정규 Cartesian Eulerian grid를
  "scratch-pad"로, 입자 = 지배적 표현(Lagrangian material point). **세계 최초로 MPM을 그래픽스에 도입**
  (그들 주장; MPM 자체는 Sulsky et al. 1995). semi-implicit 시간적분(아래).

### 4.0 큰 그림 — MPM 이란
물체 변형 = 미변형 좌표 X → 변형 좌표 x 의 사상 `x=φ(X)`. **변형구배 `F=∂φ/∂X`**. 입자 p 는 위치 x_p,
속도 v_p, 질량 m_p, 변형구배 **F_p** 를 보유. MPM은:
1. 입자량(질량·운동량)을 격자에 **rasterize**(전사) → 격자에서 ∇·σ 같은 미분을 표준 FEM weak form 으로 계산
   (입자만으로는 연결성이 없어 미분이 어려움 — 격자가 이를 해결).
2. 격자에서 힘·속도를 풀고 → 입자로 **되돌려**(FLIP/PIC) 입자 위치·F 업데이트.
- **보간함수**: 1D cubic B-spline 의 dyadic product (Steffen et al. 2008):
  `N_i^h(x_p) = N((1/h)(x_p−ih))·N((1/h)(y_p−jh))·N((1/h)(z_p−kh))`,
  `N(x)= ½|x|³−x²+⅔ (0≤|x|<1); −⅙|x|³+x²−2|x|+4/3 (1≤|x|<2); 0 (else)`.
  표기 `w_ip=N_i^h(x_p)`, `∇w_ip=∇N_i^h(x_p)`.

### 4.1 전체 업데이트 절차 (Fig 7, 10단계 — 우리 timestep 과 1:1)
1. **입자→격자 rasterize**: 질량 `m_i^n=Σ_p m_p w_ip^n`. 속도는 운동량 보존 위해
   `v_i^n = Σ_p v_p^n m_p w_ip^n / m_i^n` (정규화 가중 — 비압축 FLIP과 다름).
2. **입자 부피·밀도 계산 (첫 스텝만)**: cell 밀도 `ρ_i^0=m_i^0/h³`, 입자 밀도 `ρ_p^0=Σ_i m_i^0 w_ip^0/h³`,
   입자 부피 `V_p^0=m_p/ρ_p^0`.
3. **격자 힘 계산**: eq(6)으로 `f_i=−Σ_p V_p^n σ_p ∇w_ip^n`.
4. **격자 속도 업데이트** (explicit): `v_i^* = v_i^n + Δt m_i^{−1} f_i^n` (eq 10).
5. **격자 기반 body collision** on `v_i^*` (§8, level-set).
6. **선형계 풀이 (semi-implicit)**: eq(9). explicit이면 `v_i^{n+1}=v_i^*`.
7. **변형구배 업데이트** (§7, return mapping — 핵심): `F_p^{n+1}=(I+Δt∇v_p^{n+1})F_p^n` 의 탄성·소성 분리.
8. **입자 속도 업데이트** (FLIP/PIC 블렌드):
   `v_p^{n+1}=(1−α)v_PIC,p^{n+1}+α v_FLIP,p^{n+1}`,
   `v_PIC,p^{n+1}=Σ_i v_i^{n+1} w_ip`, `v_FLIP,p^{n+1}=v_p^n+Σ_i(v_i^{n+1}−v_i^n)w_ip`, α=0.95.
9. **입자 기반 body collision** on v_p^{n+1} (§8).
10. **입자 위치 업데이트**: `x_p^{n+1}=x_p^n+Δt v_p^{n+1}`.

### 4.2 ★★ 구성식 — multiplicative elasto-plasticity F = F_E·F_P (§5)
이 논문의 심장. **변형구배를 탄성부·소성부로 곱분해**:

  **F = F_E · F_P**   (multiplicative elasto-plasticity)

탄소성 에너지밀도(constitutive model):

  **Ψ(F_E, F_P) = μ(F_P)·‖F_E − R_E‖²_F  +  (λ(F_P)/2)·(J_E − 1)²**   ……(eq 1)

- 탄성부 = **fixed corotated** 모델(Stomakhin et al. 2012). R_E = F_E 의 극분해 회전부
  (**F_E = R_E·S_E**, polar decomposition). J_E = det F_E. ‖·‖_F = Frobenius norm.
- Lamé 계수가 **소성변형의 함수**(=hardening):
  **μ(F_P) = μ₀·e^{ξ(1−J_P)}**,  **λ(F_P) = λ₀·e^{ξ(1−J_P)}**   ……(eq 2),  J_P=det F_P.
  → **소성 압축(J_P<1)이 진행될수록 μ,λ ↑ = 단단해짐**(눈 다질 때 굳는 효과). ξ가 hardening 세기.
- **임계 압축/신장 임계값**: 소성 개시를 결정. **F_E 의 특이값을 구간 `[1−θ_c, 1+θ_s]`로 제한**.
  특이값이 이 구간을 벗어나면(압축 θ_c 초과, 또는 신장 θ_s 초과) 그 초과분이 소성으로 흘러감(§7).

> 설계 의도(논문 §5): 주응력(principal stress)이 아니라 **주신장(principal stretch=특이값)** 기준으로
> yield criteria 를 정의 → 사용자가 "언제 부서지나(θ_c,θ_s)"·"얼마나 빨리 굳나(ξ)"를 직관적으로 제어.
> 정확도보다 **제어성·시각적 사실성** 우선(눈에 충분).

### 4.3 응력·힘 (§6)
- 총 탄성 위치에너지 `∫Ψ(F_E,F_P)dX` (eq 3). MPM 이산화에서 격자노드 위치 `x̂_i=x_i+Δt v_i`로 표현:
  `Φ(x̂)=Σ_p V_p^0 Ψ(F̂_Ep(x̂),F_Pp^n)`.
- 탄성 trial 변형구배(격자 속도가 만든):
  `F̂_Ep(x̂) = (I + Σ_i(x̂_i−x_i)(∇w_ip^n)^T) F_Ep^n`   ……(eq 4).
- 격자 힘 = 에너지의 격자위치 미분:
  `−f_i(x̂)=∂Φ/∂x̂_i=Σ_p V_p^0 (∂Ψ/∂F_E)(F̂_Ep,F_Pp^n)(F_Ep^n)^T ∇w_ip^n`   ……(eq 5),
  Cauchy 응력으로 `f_i(x̂)=−Σ_p V_p^n σ_p ∇w_ip^n`   ……(eq 6),  `σ_p=(1/J_p^n)(∂Ψ/∂F_E)(F_Ep^n)^T`.
- **semi-implicit**(§6.1): 에너지의 Hessian(∂²Ψ/∂F_E²) 작용으로 `v_i` 를 음함수적으로 진행. eq(7)(8)이
  Hessian-vector product. 최종 (mass-symmetric) 선형계:
  `Σ_j (I δ_ij + βΔt² m_i^{−1} ∂²Φ^n/∂x̂_i∂x̂_j) v_j^{n+1} = v_i^*`   ……(eq 9),
  `v_i^* = v_i^n + Δt m_i^{−1} f_i^n` (eq 10). β: 0=explicit, ½=trapezoidal, 1=backward Euler.
  CG로 풀이, 10–30회, **격자해상도·입자수와 무관**(논문이 강조하는 장점).

### 4.4 ★★ 변형구배 업데이트 = return mapping (§7) — 우리 MPM의 알고리즘 핵심
매 스텝, **모든 변화를 일단 탄성부에 임시 배정**한 뒤 임계초과분만 소성으로 넘긴다:

1. 임시(trial): `F̂_Ep^{n+1}=(I+Δt∇v_p^{n+1})F_Ep^n`, `F̂_Pp^{n+1}=F_Pp^n`. 그러면 전체:
   **F_p^{n+1}=(I+Δt∇v_p^{n+1})F_Ep^n F_Pp^n = F̂_Ep^{n+1} F̂_Pp^{n+1}**   ……(eq 11).
2. **SVD(특이값분해)**: `F̂_Ep^{n+1}=U_p Σ̂_p V_p^T`.
3. **특이값 클램프(return to yield surface)**:
   **Σ_p = clamp(Σ̂_p, [1−θ_c, 1+θ_s])**   ← 임계 압축/신장 구간으로 사영.
4. 최종 분해:
   **F_Ep^{n+1} = U_p Σ_p V_p^T**,  **F_Pp^{n+1} = V_p Σ_p^{−1} U_p^T F_p^{n+1}**   ……(eq 12).
   항등식 `F_p^{n+1}=F_Ep^{n+1} F_Pp^{n+1}` 가 보존됨(쉽게 검증 가능, 논문 명시).

> 즉 **return mapping = "탄성 trial → SVD → 특이값을 yield 구간으로 클램프 → 초과분을 F_P 에 흡수"**.
> 이게 우리 `mpm3d_compaction.py`/`mpm2d_*` 의 **von Mises J2 return mapping** 과 *완전히 같은 골격*
> (우리는 클램프 대상이 특이값 구간이 아니라 J2 항복면=편차응력 노름 ≤ √(2/3)σ_y 라는 점만 다름; §7 대비).

- **재료 처리** ★ (DEM판 "무질서 처리"에 대응하는 MPM판): **진짜 연속체 SHAPE 소성**.
  입자=물질점이며 그 사이 형상이 격자 위에서 실제로 흐른다 → δ-overlap 프록시가 아니라 **참 소성 흐름**.
  (이게 rigid-sphere DEM 이 못 하는 절반. frame[5].) PSD 개념 없음(연속체).
- **도메인/seeds**: 입자를 부피에 무작위 시드, 4–10 ppc. reseeding 불필요(보간반경 겹침 노드에만
  격자연산 → 계산량이 점유 cell 수에 비례). Table 3: 예제별 30만–270만 입자, 격자 ~200³–800³,
  5–36 s/frame (8-core Xeon).
- **특이사항/튜닝**: ① **공간가변 파라미터** — 눈덩이 바깥을 더 단단/무겁게(노이즈) 해서 chunky 파쇄 유도
  (실제 눈덩이 모사); ② **sticky collision**(§8) — 수직/오버행 면에 눈이 붙도록 상대속도 0 강제(packing
  snow 효과, Fig 1); ③ body collision 은 level-set(φ≤0), inelastic, Coulomb 마찰.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | Rolling snowball — 굴러가며 눈이 달라붙음(sticky packing) | packing 효과 = 압축 hardening(eq 2)의 가시화 |
| 2 | Snowball smash — 벽 충돌, sticky(아래)/non-sticky(위) | collision BC가 morphology 결정(우리 servo/hold BC 대응) |
| 3 | Double smash — 눈덩이 충돌·파쇄 | **fracture가 별도 모델 없이 소성에서 창발**(MPM 장점) |
| 4 | Snowball drop — 바닥 충돌 | 기본 압밀/충격 |
| 5 | "SIGGRAPH" 글자 파쇄 | θ_c/θ_s 가 파쇄 형상 제어 |
| 6 | Castle destruction — 구조물 붕괴 | 큰 변형·위상변화 자동 처리(remesh 불필요) |
| 7 | **MPM Overview — 10단계 입자↔격자 흐름도** | ★ **우리 MPM timestep 과 1:1**(§4.1 대조표) |
| **8** | **눈 블록이 쐐기 위에서 부서짐 — 파라미터 변주(E₀·θ_c·θ_s·ξ 각각 낮춤 vs reference)** | ★★ **각 파라미터가 형상·동역학에 미치는 영향의 직접 시각화** — 우리 (E,σ_y,경화) 스윕의 그래픽스판 |
| 9 | Walking character — 발자국 | 국소 압밀+잔류(소성) |
| 10 | Snowplow — 제설, 원통형 분출 | 소성 흐름의 방향성 |
| 11 | Character digging — 곡괭이 자국 corrugation | 잔류 소성변형(F_P)의 흔적 |
| 12 | "THE END" — 다른 글자도 가능 | (데모) |

> Fig 8 이 우리에게 가장 유용: **E₀ 낮춤 = 더 잘 흐름, θ_c 낮춤 = 더 일찍 압축소성(powdery), θ_s 낮춤 =
> 더 잘 찢어짐(chunky), ξ 낮춤 = 덜 단단(ductile)**. 우리 MPM E_eff/σ_y/hardening 스윕 해석과 같은 논리.

## 6. Post-processing ★
- **무엇**: (배터리 후처리 없음 — 그래픽스 논문) 렌더 시점에 입자를 격자에 rasterize 후 **volumetric
  path tracer**로 Mie 산란 근사(Henyey–Greenstein, g=0.5, σ_t=724 m⁻¹) — 시각화용. 정량지표는
  Table 3(입자수·격자·계산시간)뿐.
- **도구**: in-house MPM + 자체 렌더러. (우리 OVITO/네트워크솔버 같은 정량 후처리 대응물 없음.)
- **수치화·플롯**: 정량 그래프 없음. 모든 결과가 시각(렌더 프레임)으로 제시. **이 논문에서 우리가 "데이터"로
  쓸 것은 Table 2 의 구성식 파라미터뿐** → `docs/data/stomakhin2013_mpm_snow_params.csv`.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
> ⚠ **물성 절대값 비교는 불가·무의미**(눈 vs LPSCl). 비교 축은 **알고리즘·구성식 구조**다.

| 항목 | 이 논문 (snow MPM) | 우리 (LPSCl SE MPM) | 차이 / 이유 |
|---|---|---|---|
| **변형구배 분해** | **F = F_E·F_P** (곱분해) | **동일 F=F_E·F_P** | ★★ **같음 — 우리 MPM의 알고리즘 토대** |
| **return mapping** | 탄성 trial → SVD → **특이값 클램프 `[1−θ_c,1+θ_s]`** | 탄성 trial → **편차응력을 J2 항복면 √(2/3)σ_y 로 사영** | **골격 동일, 항복면 형태만 다름**(주신장-box vs J2-구) |
| **탄성 모델** | fixed corotated (Stomakhin 2012), ν=0.2 | (MLS-)MPM, fixed corotated 계열, ν=0.49 | 같은 corotated 계열; **우리 ν=0.49(stiff-bulk)로 등적화** |
| **소성 종류** | **압축성**(눈은 부피 변함), cap-유사 압축경화 | **등적 J2**(부피보존), champion E=1.53/σ_y=0.15(2D)·0.30(3D) | ★ **구성식 차이**: 눈=압축 가능+경화, 우리=등적. 우리 DPC cap(`docs/mpm_dpc_cap_crosscheck.md`)이 snow류 **부피경화**를 시도했다가 resolved-grain서 실패 |
| **hardening** | μ,λ ∝ e^{ξ(1−J_P)}, **압축할수록 단단**(ξ=10) | von Mises 선형 work-hardening(HARD_SE≈10, 2D champion) | 둘 다 hardening 보유; 눈은 **부피 J_P 기반**, 우리는 **누적 소성변형 기반** |
| **plastic gradient F_P** | det F_P = 압축이력, hardening 구동 | **누적 소성변형 Σdg = 열화 개시장** | ★ **F_P ↔ 우리 Σdg**: 둘 다 "소성이 얼마나 쌓였나" — 우리는 이를 degradation-onset 공간장으로 사용 |
| **입자 처리** | 연속체 SHAPE 소성(진짜 흐름) | 동일 — 진짜 SHAPE 소성 | **같음** ✓ (둘 다 rigid-sphere DEM 이 못 하는 절반) |
| **transport σ** | **없음**(그래픽스, 전달 무관) | **없음**(MPM 영역 아님 — DEM이 담당) | frame[5]: 둘 다 MPM=역학, 전달은 DEM |
| **격자/적분** | semi-implicit(β-Euler), FLIP/PIC α=0.95 | MLS-MPM(APIC 후속), explicit GPU(Taichi) | 우리는 **APIC/MLS-MPM**(이 논문 이후 표준) + GPU |
| **BC/protocol** | level-set collision, sticky | servo(정압)/hold(변위정지+relax) | 우리 BC가 실험(정압 프레스) 모사에 특화 |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **계보 확립(인용)**: 우리 `mpm3d_compaction.py`/`mpm2d_PS_pressure.py` 의 **F=F_E·F_P + return
  mapping** 은 *이 논문이 그래픽스에 대중화한 EP-MPM* 의 직계다. 논문/덱에서 "MPM 토대"를 인용할 때 **원전 =
  Stomakhin 2013**(+ MPM 자체는 Sulsky 1995). 우리 von Mises J2 는 그들의 **특이값-클램프 return mapping
  자리에 J2 항복면을 끼운 변형**으로 정확히 서술 가능.
- ② **구성식 차이의 정확한 언어**: 우리 DPC cap dead-end(`docs/mpm_dpc_cap_crosscheck.md`)는 사실상
  **"snow류 압축성 cap-경화를 resolved-grain LPSCl 에 이식하려다 실패"** 였다. 이유가 이 논문으로 명확해짐 —
  **눈은 진짜로 부피가 줄지만(ρ₀ 400, 압축성 ν=0.2), LPSCl 입자는 bulk 24 GPa ≫ 300 MPa 라 부피 불변**
  → 눈의 `(J_E−1)²`·`e^{ξ(1−J_P)}` 부피경화는 LPSCl 입자에 비물리. **우리가 등적 J2 + ν=0.49(stiff-bulk)로
  간 것이 정당**함을, "snow는 cap이 맞고 우리는 안 맞다"로 frame[5] 안에서 깔끔히 설명.
- ③ **θ_c/θ_s ↔ 우리 θ(yield) 직관 차용**: 그들의 "θ_c=압축 개시, θ_s=신장/파쇄 개시, ξ=경화속도" 3-노브
  직관(Fig 8)은 우리 (σ_y, hardening) 스윕을 *사용자 언어*로 설명하는 데 그대로 쓸 수 있다(예: 우리 σ_y↓ =
  그들 θ_c↓ = 더 powdery/더 잘 흐름). **단 우리는 파쇄(θ_s)를 DEM Auerbach로 따로 다룸**(MPM 등적이라 신장-
  파쇄 미보유) — 이 갈림이 frame[5] 분업.
- ④ **Klár 2016(WISHLIST #21) 연결**: 이 논문의 직계 후속이 **모래(sand) Drucker-Prager MPM(Klár 2016)**.
  눈(cap-경화)→모래(DP, 비점착 마찰)→우리 LPSCl(J2 등적)의 **구성식 계보**가 선다. 우리 DPC 실험은 이미
  "DP/cap을 resolved-grain에 시도"한 것이므로 Klár 와 직접 대조 대상.

## 9. 인용 가능 문장 (deck/paper용)
- "Our solid-electrolyte plastic-compaction MPM inherits the elasto-plastic material-point framework
  popularised by Stomakhin et al. (2013): the multiplicative split **F = F_E·F_P** and the
  **return-mapping** update (elastic trial → SVD → project the singular values onto the yield
  surface) are the algorithmic basis of our SE compaction, with their snow singular-value box
  `[1−θ_c, 1+θ_s]` replaced by a **von Mises J2** deviatoric-norm projection."
- "Where Stomakhin's snow is **compressible** with volumetric cap-like hardening
  (μ,λ ∝ e^{ξ(1−J_P)}), our LPSCl solid electrolyte is treated as **volume-preserving J2**
  (ν≈0.49 stiff-bulk): the bulk modulus of crystalline Li₆PS₅Cl (~24 GPa) far exceeds the 300 MPa
  press, so the snow-type volumetric hardening is unphysical for the resolved SE grain — which is
  precisely why our Drucker-Prager-cap experiment failed on the resolved grain."

## 10. 주의/한계 (over-claim 방지)
- **분야가 다르다 — 그래픽스(눈), 배터리 아님.** porosity·σ·Heckel·coverage·PSD 등 **모든 배터리 물성 n/a**.
  이 digest 의 가치는 **알고리즘·구성식 계보**에 한정. 절대 물성 전이 **금지**.
- **시각적 사실성 우선, 정량 검증 없음.** 논문에 실험 anchor·수렴·정량 그래프 없음(렌더 프레임만). 파라미터
  (Table 2)는 "useful starting point"라고 저자가 명시 — *측정값이 아님*. CSV는 그 시작점 표일 뿐.
- **구성식이 우리와 다르다**: 눈 = **압축성 + cap-유사 부피경화**(`(J_E−1)²`, `e^{ξ(1−J_P)}`, ν=0.2);
  우리 = **등적 J2**(ν=0.49). 따라서 *수치·구성식 절대 전이 불가*, **알고리즘 골격(F_E·F_P + return
  mapping)만** 공유. 우리 DPC가 이 snow류 cap을 시도→실패한 기록이 그 비전이성의 증거.
- **FLIP/PIC(α=0.95) ≠ 우리 APIC/MLS-MPM.** 전달 방식 세부가 다름(우리가 더 최신). 알고리즘 *원리*는 같다.
- **2D/3D·해상도**: 이 논문은 3D 그래픽스. 우리 2D/3D 절대 스케일 차이 논의(σ_y 2D 0.15→3D 0.30)는
  이 논문과 무관(눈은 정량 스케일 검증을 안 함).
- **frame[5] 재확인**: 이 논문은 **MPM=역학/연속체-소성 엔진**의 원전. 전달(σ)·packing-dip·접촉망은
  여전히 DEM 영역 — 이 논문도 transport를 전혀 다루지 않아 분업을 *반증이 아니라 재확인*한다.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

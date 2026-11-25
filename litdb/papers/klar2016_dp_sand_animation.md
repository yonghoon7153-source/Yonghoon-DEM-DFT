# 모래(sand) 애니메이션을 위한 Drucker-Prager 탄소성 — Klár (ACM TOG 2016, SIGGRAPH)

> slug `klar2016_dp_sand_animation` · DOI `10.1145/2897824.2925906` · type `MPM` · PDF `Klar_2016_ACMTOG_DruckerPrager_SandAnimation.txt` · digested `2026-06-26` · status ✅

> ⚠ WISHLIST Tier-4 #21 (MPM 탄소성 — Drucker-Prager). **컴퓨터그래픽스(UCLA) 논문 — 배터리·LPSCl·NMC 와 무관.**
> 우리에게 중요한 이유는 **딱 두 가지**: ① 이 논문이 우리 **DPC dead-end**(`docs/mpm_dpc_cap_crosscheck.md`)의
> *직계 원전*이다 — 우리가 resolved-grain LPSCl 에 이식했다가 실패한 **Drucker-Prager 구성식**의 정전(canonical
> sand-DP). ② **구성식 계보의 가운데 고리**: 눈(Stomakhin 2013, cap-경화) → **모래(Klár 2016, DP 비점착 마찰)**
> → 우리 LPSCl(von Mises J2 등적)의 3-재료 3-구성식 계보를 닫는다. 핵심 수확 = ★ **DP 원뿔 yield surface +
> 로그-특이값(Hencky strain) 공간의 return mapping 3-케이스**(원뿔 안/원뿔 옆면/원뿔 꼭짓점) + ★ **non-associative
> 부피보존 소성 흐름** = 우리가 J2 cylinder 로 대체한 바로 그 자리. Frame[5]: MPM = 우리의 **역학/morphology 절반**.

---

## 1. 한 줄 요약
"모래"를 **점착 없는(cohesionless) 탄소성 연속체**로 보고, **Drucker-Prager(DP) 항복면**(전단응력 ≤ 마찰계수×수직응력,
= Coulomb 마찰의 연속체판)을 **Hencky 변형률(=변형구배 특이값의 로그) 공간의 return mapping**으로 강제하여 모래의
흐름·쌓임·붕괴·충돌·위상변화를 MPM 으로 재현한 SIGGRAPH 논문. 핵심 알고리즘 = Stomakhin 2013 의 `F=F_E·F_P` +
특이값-SVD 골격을 그대로 쓰되, **클램프 대상이 snow 의 "특이값 box `[1−θ_c,1+θ_s]`"가 아니라 "DP 원뿔"**이고, 사영
방향이 **부피를 보존하는 non-associative 방향**(꼭짓점에서 trace 불변)이라는 점만 다르다. 사영은 정확히 **3 케이스** —
(I) 원뿔 안=탄성(정지마찰, 무변형) / (II) 인장·팽창=원뿔 **꼭짓점**으로(응력 0, 자유 분리) / (III) 그 외=원뿔
**옆면**으로(동마찰, 부피보존 사영). ★ **이 DP 구성식이 정확히 우리가 LPSCl resolved-grain 에 시도했다가 실패한
DPC 의 원형**이며, 모래에선 맞고 LPSCl 입자에선 안 맞는 이유가 이 논문으로 깔끔히 설명된다(아래 §7-(1)).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| G. Klár, T. Gast, A. Pradhana, C. Fu, C. Schroeder, C. Jiang, J. Teran (University of California, Los Angeles) | ACM Trans. Graph. **35(4)** Article 103 (July 2016), SIGGRAPH '16 | 10.1145/2897824.2925906 | **해당 없음 — 마른 모래(dry granular).** 우리 소재(LPSCl/NMC)와 무관; *구성식·알고리즘*만 전이 | 그래픽스 시뮬레이션: **MPM + Drucker-Prager 탄소성** + APIC 전사 (in-house, explicit/implicit) |

> ⚠ 이 논문은 σ_ionic·porosity·Heckel·EIS 같은 **배터리 물성을 전혀 다루지 않는다.** §3 핵심물성 표는 "모래 DP
> 구성식 파라미터"로 채우며, 우리 비교(§7)는 *물성 절대값*이 아니라 **구성식·알고리즘 구조** 차원이다.
> 학술 계보: 저자들이 명시하길 본 논문은 토목공학의 **Mast et al.(2013, 2014)** DP-MPM(landslide/column-collapse,
> Acta Geotech.)의 **implicit·APIC 판**이며, Drucker-Prager 자체는 **Drucker & Prager 1952**(Soil mechanics)다.
> 즉 "공학 DP-MPM → 그래픽스 DP-MPM" 의 다리이기도 하다 — 우리 DPC 실험의 직접 조상.

## 3. 핵심 물성 (수치) — 모래 DP 구성식 파라미터 (Table 3, §10)
| 물성 | 값 | 조건 (의미) | stated/digitized | 비고 |
|---|---|---|---|---|
| 마찰각 φ_F | **30°** (스윕 20/25/30/35/40°) | DP 원뿔 반각을 결정 (Fig 13) | stated (Table 3) | ★ **DP 의 1차 노브**. 클수록 더 높고 가파른 모래더미(steeper repose angle). splash=22°, spout=30° |
| α (마찰계수→원뿔) | **α = √(2/3)·(2 sinφ_F)/(3−sinφ_F)** | φ_F→DP 원뿔 half-angle | stated (eq 31) | φ_F=0 → α=0 → 유체처럼 거동 |
| 영률 E (씬 사용값) | **3.537×10⁵ Pa = 0.354 MPa** | 대부분 3D 씬 | stated (Table 3) | **실제 모래값이 아님**(↓) |
| 영률 E (실제 모래) | **3.537×10⁷ Pa = 35.4 MPa** | 실제 마른모래 | stated (§10) | ★ 저자가 **의도적으로 100× 연화**(solver 효율·implicit 안정). "물리적으로 정확한 E 가 항상 최선이나 더 작은 값도 시각엔 무방" |
| Poisson ν | **0.3** | 모래 | stated (Table 3) | **압축성** 재료(눈 0.2, 우리 LPSCl MPM 0.49 와 대조) |
| 점착 c (cohesion) | **0** (=cohesionless) | 마른 모래 | stated (§7) | ★ **원뿔 꼭짓점이 원점(응력 0)** — 점착=미래과제(젖은모래/흙) |
| 경화 h₀/h₁/h₂/h₃ | **35/9/0.2~0.3/10** (°) | φ_F = h₀+(h₁q−h₃)e^{−h₂q} (eq 30) | stated (Table 3) | h₁=0 인 씬(friction-angle/spout/splash)은 **경화 없음**. 가능범위 h₀>h₃≥0, h₁,h₂≥0 |
| 밀도 ρ | **2200 kg/m³** (splash 1582) | 모래 | stated (Table 3) | (참고: LPSCl SE bulk ≈ 1640–2000) |
| dt (explicit/implicit) | **1×10⁻⁴~5×10⁻⁵ / ≤1.5×10⁻³ s** | CFL=1 | stated (Table 2) | implicit 가 castle/spout 에 사용 |
| 격자/입자 | dx 0.00083–0.016 m · 입자 4.6×10⁵–6.6×10⁶ · ppc 2–9 | 씬별 | stated (Table 2) | 5–33 s/frame(Narain 대비 8.7× 느리나 staircasing 없음) |
| 전사 | **APIC**(Jiang 2015) | particle↔grid | stated (§1) | ★ Mast 의 FLIP 대체 → 고-ppc 안정, ringing 없음 |

> 배터리 물성(porosity@P / σ_ionic / σ_e / σ_thermal / coverage / Z / Heckel P_y / PSD)은 **전부 n/a**
> (모래 애니메이션 논문이라 존재하지 않음). 데이터 → `docs/data/klar2016_dp_sand_params.csv`.

## 4. 시뮬레이션 방법 ★ — 이 논문의 본체
> 여기가 우리에게 중요한 전부. **DP 구성식·return mapping 을 *논문 수준* 으로 옮긴다(수식 exact).** 알고리즘 골격은
> Stomakhin 2013 과 공유하므로(§4.1·§4.3 transfer/force) **새로운 부분 = DP 항복면 + 3-케이스 사영(§4.4)**에 집중.

### 4.0 큰 그림 — 지배방정식과 탄소성 분해
- 모래를 탄소성 연속체로 보고 질량보존 `Dρ/Dt + ρ∇·v = 0` (eq 1), 운동량보존 `ρ Dv/Dt = ∇·σ + ρg` (eq 2),
  변형구배 진화 `DF/Dt = (∇v)F` (eq 3). (D/Dt = material derivative.)
- **변형구배 곱분해 `F = F_E·F_P`** (eq, §3): 소성부 F_P 는 "잊혀진 변형 이력"(코일스프링 비유 — 굽힌 이력은
  F_P 에, 그 위 추가 압축은 F_E 에). **응력은 F_E 만으로 계산**.
- **응력**(1st PK 경유 Cauchy) `σ = (1/det F)·(∂ψ/∂F_E)·F_E^T` (eq 4), ψ = 탄성에너지밀도.
- **이산화 = MPM**(Sulsky 1994): 입자(Lagrangian)에 질량·운동량·F 저장, 격자(Eulerian)에서 힘 계산.
  접촉·위상변화·이력의존을 자연 처리. **Stomakhin 2013 snow MPM 과 같은 절차**(아래는 그 위 DP 만 얹음).

### 4.1 전체 업데이트 절차 (Fig 7 — 우리 timestep 과 1:1, snow 와 동일 골격)
1. **입자→격자 전사**: 질량 `m_i^n=Σ_p w_ip^n m_p` (eq 7), 속도는 **APIC**로
   `v_i^n = (1/m_i^n)Σ_p w_ip^n m_p(v_p^n + B_p^n(D_p^n)^{−1}(x_i^n−x_p^n))` (eq 9).
   B_p^n = APIC affine momentum, D_p^n = inertia tensor(cubic/quadratic spline 이면 I 의 상수배).
2. **격자 힘·속도 업데이트**: 힘 `f_i = −Σ_p V_p^0 (∂ψ/∂F_E)(F_E)(F_E^n)^T ∇w_ip` (eq 23) + 중력(eq 24).
   explicit: `v_i^s = v_i^n + (Δt/m_i^n) f_i(⟨F_p^E⟩)` (eq 10). implicit(§5.6): eq 19, **GMRES**(비대칭계,
   plastic 때문) — 보통 ≤3 iter, 15 cap.
3. **격자 충돌**(§8, level-set φ, sticky/slipping/separating) → 마찰(§8.1, Coulomb μ_b).
4. **격자→입자 전사**(APIC): v_p^{n+1}, B_p^{n+1}=Σ w(v)(x−x)^T (eq 11,12).
5. **입자 위치·F 업데이트**: `x_p^{n+1}=Σ w_ip x_i^{n+1}` (eq 13), `F_p^{n+1}=(I+Δt(∇v)_p)F_p^n` (eq 14),
   (∇v)_p = Σ v_i^{n+1}(∇w_ip)^T (eq 15).
6. **★ 소성·경화**(§5.5·§7 — 이 논문 핵심): trial 탄성 `F̂_E^{n+1}=F_E^n+Δt(∇v)_p F_E^n` (eq 16) 를
   **DP 항복면으로 사영** `F_E^{n+1}=Z(F̂_E^{n+1},α_p^n)` (eq 17), 소성부 갱신
   `F_P^{n+1}=(F_E^{n+1})^{−1} F̂_E^{n+1} F̂_P^{n+1}` (eq 18). **이 Z 가 §4.4**.

### 4.2 ★ 구성식 — Hencky 변형률 St.Venant-Kirchhoff 에너지 (§6.3)
- Mast et al. 2013 의 에너지밀도 채택: St.Venant-Kirchhoff 와 같은 형이되 **left Cauchy-Green 대신 Hencky 변형률
  `½ln(FF^T)`** 사용 → DP 사영이 매우 단순해짐(아래). SVD `F=UΣV^T` 로 쓰면:

  **ψ(F) = μ·tr((ln Σ)²) + ½·λ·(tr(ln Σ))²**   ……(eq 25)

  (Σ 대각 → ln Σ = 대각원소 로그.) 응력 미분:

  **∂ψ/∂F = U(2μ Σ^{−1}lnΣ + λ tr(lnΣ)Σ^{−1})V^T**   ……(eq 26)

- μ, λ = Lamé(E=0.354 MPa, ν=0.3 에서). **핵심**: 에너지·소성 둘 다 **로그-특이값 공간 `ε = lnΣ`(Hencky)**에서
  표현 → DP 항복함수가 ε 의 *선형* 식이 되어 사영이 닫힌형(closed-form)이 된다(snow 의 특이값-box clamp 와 같은
  편의, 단 box 대신 cone).

### 4.3 ★★★ Drucker-Prager 항복면 + return mapping 3-케이스 (§7 — 우리 DPC 의 원형)
> **이 절이 WISHLIST #21 의 본체이자 우리 DPC dead-end 의 직접 대상.** 수식 전부.

DP 모델 = 입자 간 **Coulomb 마찰**의 연속체화: **전단응력 ≤ (마찰계수)×(수직응력)**. 주응력 공간에서 yield surface 는
**원뿔(cone)**, 꼭짓점이 원점(=무응력, cohesion=0). 사영 함수 `Z(F_E, α_p)`를 다음으로 정의(SVD `F_E=U_p Σ_p V_p^T`,
**ε := s_p = ln Σ_p**, d = 공간차원):

1. **편차 변형률 + 소성량**:

   **ŝ = s_p − (tr(s_p)/d)·I**  (편차 로그-변형률, trace-free)

   **δγ = ‖ŝ‖_F + (dλ+2μ)/(2μ)·tr(s_p)·α**   ……(eq 27)

   여기서 α = DP 마찰계수(eq 31, φ_F 에서), ‖·‖_F = Frobenius norm. δγ = "원뿔 밖으로 얼마나 나갔나" 의 척도.

2. **3 케이스 분기**(Fig 14·15 의 색):
   - **Case I — 원뿔 안(녹색)**: **δγ ≤ 0** → F_E 가 이미 항복면 안. **수정 없이 반환**(`return Σ_p`).
     정지마찰, 소성 없음. det(F_E) 불변 → 부피 불변.
   - **Case II — 꼭짓점(적색, 인장/팽창)**: **‖ŝ‖_F = 0 또는 tr(s_p) > 0** → 모래가 팽창/인장 중 → 저항 없음 →
     **원뿔 꼭짓점으로 사영, `return U_p V_p^T`** (=Σ=I, 즉 무변형·무응력). 입자가 **자유롭게 분리**(no stress).
   - **Case III — 옆면(청색, 압축+초과전단=동마찰)**: 그 외 → **원뿔 옆면으로 사영, `return U_p e^{H_p} V_p^T`**, 단

     **H_p = s_p − δγ·ŝ/‖ŝ‖_F**   ……(eq 28)

   (e^{H_p}, ln Σ_p 모두 대각행렬 연산 = 원소별 exp/log.) **U_p, V_p 는 사영 후 불변** → 사영 결과의 SVD 가 공짜로
   주어짐(힘 계산에 필요). 그래서 full result 대신 대각부(Σ_p, I, e^{H_p})만 반환.

3. **★ 부피보존(non-associative flow) — 우리에게 결정적인 부분**(§7.2):
   - associative flow(법선방향 사영)를 쓰면 모래가 **과도하게 부피를 얻는다**(Bonet&Wood). 대신 DP 는
     **non-associative** 흐름으로 부피를 보존: **`tr(ŝ)=0` 이므로 Case III 의 H_p 가 `tr(H_p)=tr(s_p)`를 유지** →
     `det(U_p e^{H_p} V_p^T)=e^{tr(H_p)}=e^{tr(s_p)}=det Σ_p=det(F_E)` → **사영이 det(F_E)를 바꾸지 않음 = 부피보존**.
   - 즉 "원뿔 위 최근접점"이 아니라 **"trace 를 보존하는 원뿔 위 점"**으로 사영하는 것이 핵심. (snow 는 box-clamp 가
     자동으로 압축을 허용 = 압축성; DP 는 일부러 등적으로 만든다.)
   - 또한 사영이 **엔트로피 증가**(2법칙)와 부피보존을 동시에 만족하도록 설계됨(논문·supplementary 명시).

### 4.4 경화(hardening, §7.3) — Mast 2014 채택
- 소성변형이 **마찰을 증가**(다질수록 더 잘 버팀). 경화량 = 소성 보정량에 비례:
  Case I → δq=0; Case II(응력 전부 제거) → δq=‖s_E^{n+1}‖_F; 각 케이스 δq≥0.
- 경화상태 `q^{n+1}=q^n+δq` (eq 29), 마찰각:

  **φ_F = h₀ + (h₁ q − h₃)·e^{−h₂ q}**   ……(eq 30),   **α = √(2/3)·(2 sinφ_F)/(3−sinφ_F)**   ……(eq 31)

- (30)은 최대값+점근선을 갖는 곡선. **입자마다 자기 항복면**(Fig 16: 다지면 원뿔이 넓어짐). h₁=0 이면 경화 없음.

### 4.5 입자 처리 ★ + 도메인/seeds
- **재료 처리** ★ (DEM판 "무질서 처리"에 대응하는 MPM판): **진짜 연속체 SHAPE 소성**. 입자=물질점, 그 사이 형상이
  격자 위에서 실제로 흐른다 → δ-overlap 프록시가 아니라 **참 소성 흐름**(rigid-sphere DEM 이 못 하는 절반, frame[5]).
  PSD 개념 없음(연속체). **단, 모래는 비점착·마찰지배**(우리 LPSCl 은 점착·등적) — 같은 "참 소성"이라도 구성식 클래스
  다름(§7-(1)).
- **초기화**: Poisson disk sampling, V_p^0 = seeding 밀도. q^0=0 → α^0 (eq 30,31). 초기 무변형 F_E=I.
- **도메인/seeds**: Table 2 — 입자 4.6×10⁵~6.6×10⁶, 격자 ~160³~432³, dx 0.00083~0.016, 4-core~12-thread Xeon,
  5–33 s/frame. 검증=Narain 2010 column-collapse 비교(Fig 18; Narain 8.7× 빠르나 본 방법은 staircasing 없고 덜 점성).
- **특이사항/튜닝**: ① **explicit 가 자주 implicit 보다 빠름**(implicit nonlinear solve 비용 > 더 많은 explicit 스텝);
  ② **APIC > FLIP**(Fig 17: FLIP 은 spurious velocity·ringing instability; APIC 안정·저소산); ③ E 100× 연화(시각
  무방·implicit 안정); ④ 2-way coupling 자동(Fig 3 탄성공+모래성 — 입자별 구성식만 다르게 주면 됨).

### 4.6 ★ 한계(저자 명시, §11) — 우리 비교에 직접 인용
- "framework 는 넓은 yield surface·탄성포텐셜에 일반화되나 **DP 만 조사**."
- **★ DP 원뿔은 2D 에서만 Coulomb 마찰과 정확히 등가**; 3D 에선 진짜 탄성영역이 더 복잡한 **Mohr-Coulomb** 이고 DP 는
  *근사*(Mast 2013). → 우리 J2 cylinder 도 마찬가지로 "근사적 구성식 선택"임을 상대화하는 근거.
- **미래과제 = 점착(cohesion) 도입(흙·젖은모래)** + 더 넓은 yield surface + 경화의 시각적 중요도. (우리 관점:
  "점착 도입 = LPSCl 방향으로 한 걸음" — LPSCl 은 점착성 고체. 단 LPSCl 은 등적이라 DP 원뿔 자체가 부적합, §7-(1).)

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | 모래시계(hourglass) — 좁은 목 통과·바닥 누적 | 흐름+쌓임의 대표; 위상변화 자동(MPM) |
| 2 | 강체공 모래상자 낙하 — crown splash | 충격 동역학 안정(APIC), 우리 servo/hold 충격 대응 |
| 3 | **변형구 공 ↔ 모래성 2-way coupling** | 입자별 구성식만 다르게 = 우리 AM(rigid)+SE(plastic) scaffold 와 같은 발상 |
| 5 | 바위 주위 갈퀴질(Zen garden) | 잔류 소성변형(F_P) 흔적 = 우리 누적 Σdg 가시화 |
| **10** | **영률 E 변주(1/10/100/1000 kPa)** — 낮으면 통통 튐 | ★ E 가 거동에 미치는 영향 = 우리 MPM E_eff 스윕 그래픽스판(E↓→흐름↑) |
| **13** | **마찰각 φ_F 변주(20–40°) 기둥붕괴** — 클수록 높고 가파른 더미 | ★★ **DP 의 1차 노브가 repose angle·packing 결정** — 우리 σ_y 노브 대응 |
| **14** | **모래기둥 붕괴, 입자를 현재 소성거동으로 색칠 + 주응력공간 위치** | ★★★ **3-케이스(녹=원뿔안/청=옆면(부피보존)/적=꼭짓점(자유분리))의 직접 가시화** — 우리 DPC/J2 항복판정의 그림 |
| **15** | **주신장 공간 DP 원뿔 모식** — 꼭짓점=무응력 | ★★★ **DP yield surface 의 정전 그림** = 우리 DPC 원형. J2 는 이 원뿔 대신 원기둥 |
| **16** | 붕괴 더미 3입자 경화 — 다질수록 원뿔 넓어짐(입자별 항복면) | hardening=마찰각 증가; 우리 work-hardening(HARD_SE) 대응 |
| 17 | APIC(좌) vs FLIP(우) — FLIP ringing | 전사 안정성; 우리 APIC/MLS-MPM 선택 정당화 |
| 18 | notched block fall: ours vs Narain 2010 | DP-MPM vs 기존 연속체; staircasing 없음 |

> Fig 14·15 가 우리에게 가장 중요: **DP 원뿔 + 3-케이스 사영의 정전 시각화**. 우리 DPC 실험이 코드로 구현한 바로
> 그 항복면이며, 우리가 J2 로 바꾼 자리(원뿔→원기둥)를 그림으로 대조할 수 있다. Fig 13(마찰각→더미각)은 "DP 의
> 1차 물성이 packing/repose 를 정한다"는 점에서 우리 Furnas-packing 논의와 결이 닿되, **모래는 마찰각으로 packing
> 을 만들고 우리 LPSCl 은 그게 아님**(우리 packing-dip 은 rigid-AM 기하 — DEM 영역)을 구분하는 근거.

## 6. Post-processing ★
- **무엇**: (배터리 후처리 없음 — 그래픽스 논문) Mantra(SideFX) 렌더, 입자를 matte sphere 로(색 랜덤 yellow/brown/
  white) 렌더; 빠른 흐름엔 motion blur. 정량지표 = Table 2(입자수·격자·s/frame), Table 4(Narain 대비 성능)뿐.
  **정량 검증 그래프·실험 anchor·수렴 연구 없음**(Fig 12 의 "실험실 부어내기 vs 우리" 정성 비교가 유일한 실측 대조).
- **도구**: in-house MPM(C++ 추정) + GMRES(implicit) + Mantra 렌더러. (우리 OVITO/네트워크솔버 같은 정량 후처리
  대응물 없음.)
- **수치화·플롯·기록**: 정량 그래프 없음. 모든 결과가 시각(렌더 프레임)으로 제시. **이 논문에서 우리가 "데이터"로
  쓸 것은 Table 3 의 DP 구성식 파라미터 + §7 의 3-케이스 사영식뿐** → `docs/data/klar2016_dp_sand_params.csv`.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
> ⚠ **물성 절대값 비교는 불가·무의미**(모래 vs LPSCl). 비교 축은 **구성식 클래스·알고리즘 구조**다.

| 항목 | 이 논문 (sand DP-MPM) | 우리 (LPSCl SE MPM) | 차이 / 이유 |
|---|---|---|---|
| **변형구배 분해** | **F = F_E·F_P** (곱분해) | **동일 F=F_E·F_P** | ★ **같음 — 우리 MPM 토대(Stomakhin 2013 계승)** |
| **return mapping 골격** | 탄성 trial → SVD → **로그-특이값(Hencky)을 항복면으로 사영** | 동일: 탄성 trial → 편차응력을 항복면으로 사영 | **골격 동일, 항복면 형태만 다름** |
| **항복면(yield surface)** | **Drucker-Prager 원뿔**(꼭짓점=원점, cohesion=0) | **von Mises J2 원기둥**(편차응력 노름 ≤ √(2/3)σ_y) | ★★ **구성식 클래스 차이**: 원뿔(압력의존·마찰) vs 원기둥(압력무관·고정 σ_y) |
| **소성 흐름** | **non-associative, 부피보존**(tr 보존; 단 케이스II 팽창 가능) | **등적(isochoric) J2**(완전 부피보존) | DP 도 Case III 는 등적이나, **Case II(꼭짓점)에서 팽창·자유분리** 허용 = 모래 특유; 우리는 그 자유분리 없음 |
| **점착(cohesion)** | **0 (cohesionless)** = 마른 모래 | **점착성 고체**(LPSCl 결정·소결성) | ★ **핵심 물성 차이**: 모래=비점착 → 인장 시 자유분리; LPSCl=점착 → 인장 저항 있음 |
| **압축성** | **압축성**(ν=0.3, cap/box 없이 마찰 원뿔) | **비압축**(ν=0.49 stiff-bulk; bulk 24 GPa≫300 MPa) | ★★ **우리 DPC 실패의 핵심**(↓ (1)) |
| **1차 노브** | **마찰각 φ_F**(repose angle·packing 결정, Fig 13) | **σ_y**(항복응력; champion 0.15(2D)/0.30(3D)) | 둘 다 1-파라미터로 거동 지배; DP=마찰, 우리=항복 |
| **경화** | φ_F = h₀+(h₁q−h₃)e^{−h₂q} (마찰각 증가, eq 30) | von Mises 선형 work-hardening(HARD_SE≈10) | 둘 다 hardening; DP=**마찰각 기반**, 우리=**누적 소성변형 기반** |
| **plastic gradient F_P** | det F_P=압축이력, 경화상태 q 구동 | **누적 소성변형 Σdg = 열화 개시장** | ★ F_P ↔ 우리 Σdg(소성 누적 — 우리는 degradation-onset 공간장) |
| **입자 처리** | 연속체 SHAPE 소성(진짜 흐름), 구·PSD 없음 | 동일 — 진짜 SHAPE 소성 | **같음** ✓ (둘 다 rigid-sphere DEM 이 못 하는 절반) |
| **transport σ** | **없음**(그래픽스) | **없음**(MPM 영역 아님 — DEM 담당) | frame[5]: 둘 다 MPM=역학, 전달=DEM |
| **전사/적분** | **APIC**(Jiang 2015) + explicit/implicit(GMRES) | **MLS-MPM**(APIC 후속) + explicit GPU(Taichi) | 우리가 더 최신(MLS-MPM); APIC 계열 공유 |
| **2D/3D 한계** | DP 원뿔 = **2D 에서만 Coulomb 정확**; 3D 는 Mohr-Coulomb 근사(§11) | J2 도 근사 구성식; 2D σ_y 0.15→3D 0.30 | 둘 다 "근사 항복면" — 절대화 주의 |

### ★★ (1) 우리 DPC dead-end 의 직접 원전 — 모래선 맞고 LPSCl 입자선 안 맞는 이유
이 논문이 우리 **DPC 실패(`docs/mpm_dpc_cap_crosscheck.md`, CLAUDE.md "DPC volumetric cap × resolved-grain")**의
*정전(canonical sand-DP)*이다. 우리는 resolved-grain LPSCl SE 에 **Drucker-Prager + (발산 경화)cap** 을 이식했고
**실패**했다 — 그 이유가 이 논문으로 정확히 설명된다:

- **모래에서 DP 가 맞는 이유**: 모래는 **(a) 비점착(cohesionless)** + **(b) 압축/팽창 가능**(grain 재배열로 부피
  변함, ν=0.3). DP 원뿔의 **압력의존 마찰**(전단 ≤ μ×수직)과 **꼭짓점 자유분리**(인장 시 grain 이 흩어짐)는 마른
  모래의 *진짜 물리*다. cap(=p_c 에서 발산하는 압축경화)을 붙이면 "느슨한 모래가 압축되며 다져진다"가 물리적으로 맞다
  (de Larrard/Mast 의 column-collapse 가 이를 검증). → DP/cap = **올바른 구성식 클래스 for 모래**.
- **우리 resolved-grain LPSCl 에서 DP/cap 이 틀리는 이유**: LPSCl SE 입자는 **(a) 점착성 결정 고체** + **(b) 거의
  비압축**(bulk modulus ≈ 24 GPa ≫ 300 MPa 프레스 → 입자 *내부* 부피변화 ~1 %). 그런데 **cap = 입자 부피 수축**을
  허용한다 → resolved-grain 에선 **비물리적 입자 압착**을 도입 → 등적 저항이 제거되어 **과압축/붕괴**.
  데이터(`docs/data/mpm_dpc_heckel_sweep.csv`): champion(no cap, E=1.53) pure-SE 300 MPa → **11 %**인데, **cap 추가
  시 300 MPa → 0.8 %**(더 나빠짐). E=24+cap 은 저압서 과소압밀(100 MPa→26–35 % vs Heckel ~14 %, 너무 뻣뻣). 즉
  **두 E 모두 cap 으로는 Heckel 재현 실패** → cap 은 resolved-grain 의 틀린 도구.
- **결론**: 모래의 부피변화는 **grain 재배열(=거시 부피변화)**이지 grain *내부* 압착이 아니다 — DP/cap 은 이 재배열을
  연속체 부피변형으로 모형화한다(homogenized 관점에서 맞음). resolved-grain LPSCl 에선 그 "재배열"이 **개별 입자
  형상흐름(등적)**으로 일어나야 하므로 **DP 원뿔/cap 이 아니라 von Mises J2(등적) + ν=0.49(stiff-bulk)** 가 옳다.
  우리 DPC 실험은 **DP/sand 가지를 resolved LPSCl 에 시도→불일치**를 정량화한 것이며(frame[4] **정량화된 모델한계**,
  버그 아님), 이 논문이 그 "시도한 가지"의 원형이다.
- **★ 단, DP/cap 이 우리에게서도 맞는 곳이 있다**: **homogenized REV**(`scripts/cap_compaction_heckel.py`, "나").
  여기선 물질점=**voids 가진 분말 덩어리**(powder-with-voids)이고 **부피 압밀=void 감소**라서 cap 이 물리적으로 정확 →
  clean Heckel **100/300/600 → 13.9/10.0/8.3 %**(Minnmann 300→10 앵커, φ0=0.5/φ_min=0.03/b=2.5). 즉
  **DP/cap 의 정당한 자리 = homogenized-REV(분말=연속체), 틀린 자리 = resolved-grain(입자=결정고체).** Klár 의 모래는
  애초에 grain-단위가 아니라 "모래=연속체"로 두므로 우리 REV 쪽에 대응하는 것이고, 우리가 grain 을 resolve 하면
  J2 로 가야 한다.

### ★ (2) 구성식 계보 — 눈(cap) → 모래(DP) → 우리(J2): 3-재료 3-구성식
| 재료 | 논문/우리 | 항복면(yield surface) | 점착 | 부피 | 왜 그 선택인가 |
|---|---|---|---|---|---|
| **눈(snow)** | Stomakhin 2013 (`papers/stomakhin2013_*`) | **특이값 box** `[1−θ_c,1+θ_s]` + 압축경화 e^{ξ(1−J_P)} | (점착-유사 hardening) | **압축성**(ρ₀ 400, ν=0.2) | 눈은 진짜 부피 줄며 다져짐 → cap-유사 부피경화 맞음 |
| **모래(sand)** | **Klár 2016 (THIS)** | **Drucker-Prager 원뿔**(꼭짓점=원점) | **0 (cohesionless)** | 압축/팽창 가능(ν=0.3), Case III 등적 | 마른 모래=비점착 마찰 grain → 마찰 원뿔+꼭짓점 자유분리 |
| **LPSCl SE(우리)** | our MPM (`mpm3d_compaction.py`/`mpm2d_PS_pressure.py`) | **von Mises J2 원기둥**(편차 ≤ √(2/3)σ_y) | **점착성 고체** | **비압축**(ν=0.49, bulk 24 GPa) | 점착·거의 비압축 결정 → 등적 형상흐름(원뿔/cap 부적합) |

→ **세 재료가 같은 MPM 프레임(F=F_E·F_P + 특이값-공간 return mapping)을 공유하되, 항복면만 box→cone→cylinder 로
바뀐다.** 우리 DPC 실험은 이 계보의 **모래(DP) 가지를 이미 테스트**하여 resolved-LPSCl 에 부적합함을 확인했고
(frame[4] 정량 모델한계), Klár 가 그 가지의 정전이다. snow→sand→J2 계보의 *닫힘 고리*가 바로 이 digest.

### (3) return-mapping-in-singular-value-space = 우리 MPM 과 같은 프레임
Klár 의 사영 `Z(F_E,α)`(SVD → 로그-특이값 ε=lnΣ → DP 원뿔로 사영 → exp 복원)는 **우리 `mpm3d_compaction.py`/
`mpm2d_*` 의 von Mises return mapping 과 골격이 완전히 동일**하다. 차이는 **사영 대상 항복면뿐** — Klár 는 **DP 원뿔**
(eq 27·28, 압력의존·꼭짓점 자유분리), 우리는 **J2 원기둥**(편차응력 노름 클램프, 압력무관·등적), snow 는 **box**. 즉
우리 코드의 "편차응력을 √(2/3)σ_y 로 사영" 한 줄을 "로그-특이값을 DP 원뿔로 사영(eq 28)"으로 바꾸면 Klár 가 되고,
실제로 우리 DPC 코드(`scripts/mpm_dem_match.py --model dpc`)가 정확히 그 교체를 구현했었다.

### (4) frame[5]/[4] 위치
- **frame[5]**(분업): 이 논문은 **MPM=역학/연속체-소성 엔진** 쪽 100 %. 전달(σ)·packing-dip·접촉망은 전혀 안 다룸 →
  우리 MPM=morphology/역학, DEM=transport 분업을 *반증이 아니라 재확인*. 우리 MPM 의 절반(morphology·플라스틱 흐름)
  이 정확히 Klár 가 사는 자리.
- **frame[4]**(cross-fit 금지·정량 모델한계): 우리 DPC 실패는 "DEM↔MPM 불일치"가 아니라 **"resolved-grain 에 틀린
  구성식 클래스(DP/cap)를 쓰면 어떻게 깨지는지"의 정량화** — 정보(모델한계)이지 버그가 아니다. Klár 는 그 틀린(=모래엔
  맞는) 클래스가 *모래에선 왜 맞는지*를 보여줌으로써, 우리 LPSCl 에서 왜 안 맞는지를 대조로 확정한다.

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **DPC dead-end 의 "원전" 확보(인용·서술)**: 우리 `docs/mpm_dpc_cap_crosscheck.md` 의 실패를 논문/덱에서 설명할 때,
  "우리가 시도한 DP 구성식 = **Klár et al. 2016 의 sand DP-MPM**(+ 공학 원전 Mast 2013/2014, DP 자체 Drucker-Prager
  1952)"으로 정전을 댈 수 있다. 그리고 **"모래(비점착·압축성)에선 DP 가 맞고, LPSCl(점착·비압축 결정)에선 J2 가
  맞다"**를 frame[5] 안에서 한 문장으로 정당화 → 우리 von Mises J2 + ν=0.49 선택이 *임의*가 아니라 **재료 클래스에서
  유도된 필연**임을 보인다.
- ② **계보 3-단(snow→sand→J2) 한 슬라이드**: Stomakhin 2013(box/cap)·Klár 2016(DP cone)·우리(J2 cylinder)를
  **같은 return-mapping 프레임의 항복면 3종**으로 나란히 → "우리는 표준 EP-MPM 위에서 재료에 맞는 항복면을 골랐고,
  대안(snow-cap, sand-DP)을 둘 다 *실제로 테스트*(DPC 실험)했다"는 강한 방법론 서사. (우리 DPC 가 **sand 가지**,
  homogenized-REV cap 이 **snow-유사 부피경화 가지**를 각각 검증한 셈.)
- ③ **"DP/cap 의 올바른 자리 = homogenized REV" 못박기**: Klár 의 모래는 grain-단위가 아니라 *연속체 모래*다 →
  우리 `cap_compaction_heckel.py`(REV, cap 정당, Heckel 13.9/10/8.3) 와 같은 추상화 수준. 따라서 **"resolved-grain →
  J2 / homogenized-REV → DP·cap"** 의 분업을 Klár 로 정당화 → DEM(transport·dip) + resolved-MPM(morphology) +
  REV-DPC(절대 Heckel) 의 3-도구 역할분담을 깔끔히 정리(frame[5] 구체화).

## 9. 인용 가능 문장 (deck/paper용)
- "The Drucker-Prager constitutive model we tested on the resolved LPSCl grain (our DPC cross-check)
  is the canonical sand model of Klár et al. (2016): a cohesionless friction cone projected in
  log-singular-value (Hencky) space with a non-associative, volume-preserving return mapping. It is
  the correct constitutive class for *dry sand* — cohesionless, grain-rearranging, compressible — but
  not for our solid electrolyte: crystalline Li₆PS₅Cl is cohesive and nearly incompressible (bulk
  ≈ 24 GPa ≫ 300 MPa), so its densification is isochoric shape-flow of the grains, not the
  particle-volume reduction a Drucker-Prager cap admits. We therefore use a von Mises J2 cylinder
  (E_eff = 1.53 GPa, σ_y = 0.15/0.30 GPa, ν = 0.49) — the same return-mapping framework with the DP
  cone replaced by an isochoric yield surface."
- "Snow (Stomakhin 2013, singular-value box with volumetric cap-hardening) → sand (Klár 2016,
  Drucker-Prager cohesionless cone) → our LPSCl SE (von Mises J2 isochoric cylinder) are three
  constitutive choices for three materials within one elasto-plastic MPM framework (F = F_E·F_P,
  return mapping in singular-value space); our DPC experiment already tested the sand/DP branch and
  quantified that it does not fit the resolved-grain solid electrolyte (frame[4] model-limit, not a
  bug), while the cap remains correct in the homogenized REV (powder-with-voids)."

## 10. 주의/한계 (over-claim 방지)
- **분야가 다르다 — 그래픽스(모래), 배터리 아님.** porosity·σ·Heckel·coverage·PSD 등 **모든 배터리 물성 n/a**.
  이 digest 의 가치는 **구성식 클래스·알고리즘 계보 + 우리 DPC dead-end 의 설명**에 한정. 절대 물성 전이 **금지**.
- **시각적 사실성 우선, 정량 검증 거의 없음.** 실험 anchor·수렴·정량 그래프 없음(렌더 프레임 + Fig 12 정성 비교만).
  E 를 실제 모래값(35.4 MPa)에서 **100× 연화**해 씀(시각 무방·solver 효율) — *측정 재현이 아니라 애니메이션*임을 명시.
- **구성식 클래스가 우리와 다르다**: 모래 = **비점착 DP 원뿔 + 압축성**(ν=0.3, 꼭짓점 자유분리); 우리 = **점착 J2
  원기둥 + 비압축**(ν=0.49). 따라서 *수치·구성식 절대 전이 불가*, **return-mapping 골격(F_E·F_P + 특이값-공간 사영)
  만** 공유. 우리 DPC 가 이 DP 를 resolved-LPSCl 에 시도→불일치한 기록이 그 비전이성의 *정량 증거*.
- **DP 원뿔의 2D 한계(저자 명시)**: DP=Coulomb 마찰과 **2D 에서만 정확**, 3D 는 Mohr-Coulomb 근사 → DP 가 *모래에서도*
  근사임. 우리 J2 도 근사 구성식이므로 "어느 항복면이 절대적으로 옳다"는 주장 금지 — **재료 클래스에 맞는 선택**일 뿐.
- **APIC/explicit ≠ 우리 MLS-MPM/GPU 세부.** 전사·적분 구현이 다름(우리가 더 최신). 알고리즘 *원리*는 같다.
- **homogenized vs resolved 혼동 주의**: Klár 의 "모래=연속체 DP"는 우리 **homogenized-REV(cap 정당)** 추상화 수준에
  대응하지, resolved-grain 에 대응하지 **않는다**. "Klár 가 DP 를 썼으니 우리도 resolved 에 DP 쓰면 된다"는 **틀린
  추론**(바로 그게 우리 DPC 실패) — resolved-grain 은 J2, REV 는 cap.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

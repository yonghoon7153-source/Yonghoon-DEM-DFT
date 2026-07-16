# 점착·마찰 분말의 접촉모델 (인장 가능 LAW) — Luding (Granular Matter 2008)

> slug `luding2008_cohesive_frictional_contact_models` · DOI `10.1007/s10035-008-0099-x` · type `DEM (contact-LAW theory)` · PDF `Luding_2008_GranularMatter_CohesiveFrictionalPowders_ContactModels.pdf` · digested `2026-06-26` · status ✅
> ★ **OPEN ACCESS** (© The Author(s) 2008, Creative Commons Attribution-Noncommercial) — **자유 인용 가능**. Walton–Braun 1986(유료·구버전)을 대체하는 공개·완전판.
> ★★ **이 논문 = 우리 LIGGGHTS `hooke/hysteresis` + adhesion + plasticity-depth 접촉법칙의 이론 정의서.** §2.3.2 (eq 6)가 우리 모델의 핵심. 우리 input `m6`(maxElasticStiffness)·`m7`(adhesionStiffness)·`m8`(plasticityDepth)이 여기 k̂₂·k_c·φ_f와 1:1 대응. WISHLIST Tier-1 #13 = 1순위.

---

## 0. 왜 이 논문이 우리에게 *foundational*인가 (먼저 읽을 것)

우리 DEM 전체(압밀·porosity·전달 네트워크·Stage-E·f_AM)는 **LIGGGHTS `hooke/hysteresis` 접촉법칙** 위에서
돈다. 그 법칙의 **정확한 수식·파라미터 정의**가 그동안 코드 주석/매뉴얼 수준으로만 있었고, 원전
Walton–Braun 1986은 유료·축약판이었다. **이 Luding 2008이 바로 그 법칙(점착 탄소성 이력 선형 스프링,
adhesive elasto-plastic hysteretic)의 공개·완전 정의서**다. 따라서 이 digest는 "literature 비교"가 아니라
**우리 모델 자체의 사양서(spec sheet)**다.

이 digest가 *직접 해소*하는 세 가지 (2026-06-26 발견, `docs/mpm_wallP_conditional_troubleshooting.md §12`):
1. **f_AM(실제 LAW ≠ Hertz)**: real_14 dump에서 Hertz 재구성(AM-AM 0.843@E=1.35)이 실제 hooke/hysteresis
   접촉력(0.670)을 못 맞춘다. 원인은 모듈러스가 아니라 **접촉 LAW 형태**. → eq 6이 그 "형태"의 정의.
2. **ε_sphere "displaced material" 규약**: Luding의 **δ₀ = (1−k₁/k₂)·δ_max = 영구 소성 잔류겹침**이 우리
   ε_sphere porosity가 가정하는 바로 그 영구 overlap이다.
3. **18× 연화**: 우리 hooke/hysteresis는 ~선형이라 **경도/항복압 캡이 없어** 진짜 소성보다 덜 변형 → E를
   18× 낮춰 보상. Luding 모델이 **소성 분기(k₁→k₂, δ₀)는 가지지만 경도(H)/항복압 캡은 없는** 바로 그
   한계를 명확히 보여줌(§1.2 "model is limited … in the regime of large deformations").

---

## 1. 한 줄 요약

**미세 점착·마찰 분말(0.1–10 µm)을 위한 최소(minimal) 접촉모델**을 제시: 법선 방향은 **점착 탄소성 이력
선형 스프링**(5-파라미터 k₁·k̂₂·k_c·φ_f·γ₀), 접선 방향은 마찰(Cundall–Strack 스프링)+구름저항+비틀림저항.
이 단일 모델 하나로 **압밀(pressure-sintering)·응력완화·그리고 형성된 고체의 인장/압축 강도시험**까지 모두
재현 — 특히 **k_c(점착 강성) 덕에 접촉이 인장(tension)을 버틴다**(논문 제목의 핵심). **= 우리 LIGGGHTS
접촉법칙의 원형 정의.**

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Stefan Luding** (Multi-Scale Mechanics, U. Twente / Particle Technology, TU Delft) | **Granular Matter 10(4) 235–246 (2008)**, Received 2006-12-22, Published 2008-03-27 | **10.1007/s10035-008-0099-x** | 소재 무관 — 일반 점착·마찰 분말(반경 ~µm, ρ=2000 kg/m³ 예시). **우리 LPSCl/NMC811에 직접 소재 데이터는 없음** | **DEM 접촉 LAW 이론** (+ 압밀·인장 데모 시뮬), N=1728/1728 입자 |

> ★ **OPEN ACCESS 기록**: 본문 우상단 "OpenAccess" 마크 + 말미 "Open Access This article is distributed under
> the terms of the Creative Commons Attribution Noncommercial License …". → deck/paper에 **자유 인용**.
> 이것이 WISHLIST에서 유료·구버전 Walton–Braun 1986(#12, 10.1122/1.549893)을 대체하는 PRIMARY인 이유.

## 3. 핵심 물성 (수치)

> ⚠ **이 논문은 소재 측정값 논문이 아니라 LAW 논문**이다. 아래 "수치"는 (a) 모델 파라미터(무차원/비율),
> (b) Table 2의 예시 단위계, (c) 인장/압축 시험 결과. **LPSCl·NMC811 물성 전이는 불가**(rigid-floor·σ·
> porosity 절대값 없음). 우리에게 가치 있는 건 **수식·파라미터 정의·정성 거동**이다.

| 물성/파라미터 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| porosity / 상대밀도 | n/a (절대 porosity 안 줌) | — | — | 압밀은 ν(부피분율)·C(배위수)로만 보고 |
| 부피분율 ν (압밀 후) | **0.6754** (k_c/k̂₂=0.5) / **0.630** (k_c=0) | p_s·2a/k̂₂≈0.02 isotropic, sinter | stated | 배위수 C≈7.16 → 완화 후 6.19/6.23 |
| σ_ionic / σ_e / σ_thermal | n/a | — | — | **전달 전혀 안 다룸** (역학 전용) — frame[5] 역학 절반 |
| coverage / 접촉면적% | n/a | — | — | 접촉면적 명시 출력 없음(Hertz도 권장 안 함) |
| coordination Z (C) | **7.16** (sinter) → **6.19** (relax) | N=1728, a=5µm Gaussian | stated | 준비절차(k_c=0 vs 0.5)에 둔감(6.19 vs 6.23) |
| E_SE / σ_y / ν | **소재값 없음** (k는 모듈러스로 직접 환산 불가) | — | — | §3.1 "magnitude of k cannot be compared directly with bulk modulus C" — k는 접촉 property, k∼C·a (micro-macro) |
| Heckel P_y / knee | n/a | — | — | Heckel 분석 안 함(압밀은 isotropic 한 점) |
| PSD | **Gaussian**, a=5 µm 중심 (좁은 분포) | a_i ~ N(a=0.005 mm) | stated | mono에 가까운 좁은 Gaussian; bi/poly-PSD 아님 |
| 인장강도 vs 압축강도 | **압축이 인장의 6–7×** | uni-axial, k_c/k=1/2 | stated (Fig 2) | k_c↑ → 인장강도↑·파괴 전 변형↑ |
| 파괴 변형 (k_c/k=1/2) | 인장 ε_xx≈**−0.006**, 압축 ε_xx≈**+0.045** | 약점착 시료 | stated | k_c/k=20이면 파괴가 **벽에서**(bulk 아님) |
| 선형탄성 영역 기울기 C₁ | Fig2: **3×10¹¹ N/m²**, Fig4: **~10⁹ N/m²** (단위계 차) | C₁ε 피팅 | stated | 인장·압축 동일 초기기울기(= 탄성 가역) |

## 4. 시뮬레이션 방법 ★  — **이것이 우리 접촉 LAW의 정의**

- **code / version**: 일반 **soft-particle MD = DEM**(논문은 코드명 비특정; 방법론 자체가 우리 LIGGGHTS
  `pair_style gran model hooke/hysteresis`의 모델 정의). 시간적분 Newton (eq 1), linked-cell 이웃탐색.
- **DEM 접촉법칙 (법선)** — ★★ **§2.3 전체가 우리 모델의 LAW**:
  - **두 입자 overlap (eq 2)**: `δ = (aᵢ+aⱼ) − (rᵢ−rⱼ)·n`, δ>0일 때만 접촉. 법선 n=(rᵢ−rⱼ)/|rᵢ−rⱼ|,
    j→i 방향. 힘 분해 fᶜ = fⁿn + fᵗt.
  - **§2.3.1 선형 스프링-대시포트 (LSD, eq 3)** — *비점착 기준*: `fⁿ = k·δ + γ₀·vₙ` (k=스프링강성,
    γ₀=점성댐핑, vₙ=법선상대속도). 접촉지속 t_c=π/ω (eq 4), ω=√(k/m₁₂−η₀²), m₁₂=mᵢmⱼ/(mᵢ+mⱼ)=환산질량,
    η₀=γ₀/(2m₁₂). 반발계수 **r = v′ₙ/vₙ = exp(−η₀π/ω) = exp(−η₀t_c)** (eq 5). **권장 r=0.4–0.8**("strong"
    dissipation); r<0.4면 인위적 과댐핑, r=1이면 탄성극한. ⚠ t_c는 적분 timestep Δt 상한을 정함
    (Δt ≪ t_c). 과댐핑 스프링은 t_c가 비현실적으로 커진다(주의).
  - **§2.3.2 ★★★ 점착 탄소성 이력 모델 (eq 6) — 우리 모델 본체:**
    ```
              ┌ k₁·δ                 if  k₂(δ−δ₀) ≥ k₁δ        (초기 재하 loading, 기울기 k₁)
    f^hys =   ┤ k₂(δ−δ₀)             if  k₁δ > k₂(δ−δ₀) > −k_c·δ (제하/재하 un/reloading, 기울기 k₂)
              └ −k_c·δ               if  −k_c·δ ≥ k₂(δ−δ₀)      (점착 분기 adhesive, 기울기 −k_c)
    ```
    조건 **k₁ ≤ k₂ ≤ k̂₂**. 최종 법선력 **fⁿ = f^hys + γ₀·vₙ** (점성 추가).
    - **k₁ (initial loading stiffness)**: 초기 재하(처녀 압축) 기울기. **소성을 머금는 가장 부드러운 가지.**
      δ_max(이력변수, 지금까지의 최대 overlap)까지 이 선을 따라 힘이 선형 증가.
    - **k₂ (un/reloading stiffness)**: 제하·재하 기울기. **k₁→k̂₂ 사이를 δ_max에 따라 보간**(eq 8). 처짐 후
      이 가파른 선을 따라 내려옴 → δ=δ_max에서 0이 되는 overlap = 영구겹침 δ₀.
    - **k̂₂ (maximal / limit stiffness)**: k₂의 상한(상수). 큰 변형에서 강성이 무한히 안 커지게 cap →
      timestep 안정성 유지(§2.3.2 "limit stiffness k̂₂ ≥ k₂ is desirable for practical reasons").
    - **k_c (adhesion / cohesion stiffness)**: 점착 가지 기울기. 제하가 δ₀ 아래로 가면 **인장력**(음수) 발생,
      −k_c·δ 선을 따라 최소력(최대 인력)까지. **이 항이 접촉을 인장에서 버티게 함 = 논문 제목.**
    - **φ_f (dimensionless plasticity depth)**: 소성 흐름 한계를 정하는 무차원 깊이(환산반경 대비 분율).
      입자 반경의 φ_f 분율을 넘으면 (최대)상수 강성 k̂₂ 사용.
    - **γ₀ (viscous damping)**: 작은 진폭 변형 소산(eq 3과 동일 점성). 큰 속도/큰 변형 충돌 시 이력에 더해 소산.
  - **영구 소성 잔류겹침 (★ 우리 ε_sphere의 물리):** 제하 시 δ=δ_max에서 출발해 k₂ 선이 0을 만나는 곳
    **δ₀ = (1 − k₁/k₂)·δ_max** = *plastic contact deformation*. δ_max는 history 변수(메모리). **이 δ₀가 곧
    영구히 남는 겹침** = "변형이 풀려도 입자가 떨어지지 않고 남는 압흔".
  - **최대 인력 (점착):** δ₀ 아래 제하 → 최소력 **f_min = −(k₂−k₁)δ_max/(k₂+k_c)** at
    **δ_min = (k₂−k₁)δ_max/(k₂+k_c)**. k_c→∞ 극한에서 **f_min ≥ −(k₂−k₁)δ_max** (k_c 무관 상한 인력).
  - **소성흐름 한계 overlap (eq 7):** `δ*_max = (k̂₂/(k̂₂−k₁))·φ_f·(2a₁a₂/(a₁+a₂))`. 환산반경
    2a₁a₂/(a₁+a₂)에 φ_f를 곱한 것. overlap이 (최대)반경의 φ_f 분율보다 크면 상수 k̂₂. 입자-벽 접촉(벽반경=∞)
    극한에서는 환산반경이 작은 입자 지름으로 감 — David et al.[43,44] 정식과 등가.
  - **k₂(δ_max) 보간 (eq 8):** `k₂ = k̂₂` if δ_max ≥ δ*_max ; else `k₁ + (k̂₂−k₁)·δ_max/δ*_max`. → **약한 접촉
    = 작은 소성, 강한 접촉 = 큰 소성**(증가하는 강성 = 비선형 이력의 선형근사).
  - **★ 특수극한 — 순수 선형 접촉:** **k₁/k̂₂ = 1 → 단순 선형 스프링**(k_c, φ_f 무의미). 즉 이력모델은
    선형모델을 특수경우로 포함. (우리 SE/AM은 k̂₂>k₁로 *완전 이력*을 씀 → 선형 특수극한 아님.)
  - **참고**: 이 piece-wise 선형 모델은 **비선형(Walton 94,96) 모델의 단순화판**(§1.2). 큰 변형에선 물리가
    바뀌므로 모델은 "단순 선형 최대강성 변위 분기"로 제한됨 — **이것이 timestep을 고정해 주는 장점이자,
    큰 변형 영역에서 questionable해지는 한계**. ⚠ **경도(H)/항복압(p_y) 캡 없음** → 큰 변형서 비물리.
- **접선 접촉법칙 (§2.4–2.5)** — 토크까지:
  - **마찰 (sliding, §2.4.1, 2.5.1):** Cundall–Strack 가상 접선 스프링 ξ. 접선 시험력 fᵗ₀=−kₜξ−γₜvₜ (eq 18),
    Coulomb 한계 fᶜₛ=μˢ(fⁿ+k_c·δ) — **점착 접촉에선 fⁿ을 (fⁿ+k_cδ)로 대체**(인력 레벨 −k_cδ가 기준). 정지마찰
    |fᵗ₀|≤fᶜₛ 이면 스프링 증가(eq 19), 미끄럼이면 Coulomb 길이로 스프링 재조정(eq 20). 동/정 마찰 μᵈ≤μˢ.
  - **objectivity (§2.4.2):** 공통회전 프레임에서 접선 관계가 객관적(eq 11). 회전 가산 시 sliding 0 검증.
  - **구름저항 (rolling, §2.4.3, 2.5.2):** 객관적 rolling 속도 vᵣ (eq 15, 환산반경 사용), quasi-force fᵣ →
    토크 q^rolling. 파라미터 kᵣ, μᵣ, γᵣ (φᵣ=φᵈ 차용). 표면거칠기/비구형 효과를 어느정도 흉내.
  - **비틀림저항 (torsion, §2.4.4, 2.5.3):** 법선축 상대스핀 v_o (eq 16), quasi-force f_o → 토크 q^torsion.
    파라미터 k_o, μ_o, γ_o.
  - **§2.6 background friction:** 매질 소산 γ_b·vᵢ (eq 22) + γ_br 배경 점성토크 (eq 23) — 장파장 협동모드
    소산용(과댐핑 주의).
- **재료 파라미터 (Table 1·2, 예시):** (모두 비율/무차원 except 몇 개 단위)
  - **k=k̂₂=5** (mg/µs² 단위), **k₁/k=0.5**, **k_c/k=0.5**, **kₜ/k=0.2**, **kᵣ/k=k_o/k=0.1**, **φ_f=0.05**,
    μ=μᵈ=μˢ=1, φᵈ=μᵈ/μˢ=1, μᵣ=μ_o=0.1, γ=γₙ=5×10⁻⁵, γₜ/γ=0.2, γᵣ/γ=γ_o/γ=0.05, γ_b/γ=4.0, γ_br/γ=1.0.
  - 입자: a₀=0.005 mm=5 µm, ρ=2000 kg/m³, 입자-벽은 k_c^wall/k̂₂=20, μ^wall=10(인장시험 시만).
- **bond/binder 모델**: **없음**(바인더 미모델 — 점착은 k_c로 통합 표현). "고체 granule"은 sinter로 형성.
- **MPM / continuum**: **없음**(순수 이산 DEM).
- **전달 솔버**: **없음**(σ_ionic/e/thermal 전혀 안 다룸). → frame[5]에서 **역학 절반만** 소유.
- **입자 처리** ★ (DEM판 "무질서 처리"):
  - **구(sphere)만** (반경 a_i, 비구형은 §1.1에서 "advanced algorithms required, not discussed").
  - **좁은 Gaussian PSD** (a=5µm 중심) — mono에 가까움; **bi/poly-PSD 아님**.
  - **rigid sphere + CONTACT 탄소성** (eq 6의 k₁→k₂ 소성분기 + δ₀ 영구겹침) — **진짜 SHAPE 소성 아님**.
    입자 자체 형상은 절대 안 변하고, "소성"은 **접촉점 힘-변위 LAW의 분기 + 잔류 overlap**일 뿐.
    ⇒ `elasto_plastic_feasibility.md §0` 층위(1) CONTACT-LAW에 해당(층위(3) SHAPE는 우리 MPM이 가짐).
- **도메인/RVE / seeds / 압력범위**: §3 데모는 N=1728 입자 cuboid. (i)압밀(isotropic p_s·2a/k̂₂≈0.02 →
  ν=0.6754) → (ii)응력완화(pᵣ≪1) → (iii)인장/압축 시험(uni-axial, 끈끈한 벽 2개를 cos 함수로 천천히 이동).
  벽: 2개는 점착(k_c^wall/k̂₂=20)으로 시료를 잡고, 나머지는 점착없음(쉽게 분리). 단일 압력영역(시험은
  변형률 제어).
- **특이사항/튜닝**: §1 철학 = **"최소(minimal) 접촉모델 — 과한 디테일은 구현·해석을 어렵게 함. 미시
  디테일이 거시거동에 중요치 않아 보이는 경우 단순모델이 더 낫다."** = 우리가 hooke/hysteresis를 쓰는
  바로 그 정당화. §4 결론도 "k₁/k와 kₜ/k 비율의 상세영향은 아직 미연구; real 데이터에 대한 정량 튜닝이
  향후과제" — **우리 18× 연화/보정이 바로 그 '정량 튜닝'에 해당**.

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1 (★ 핵심)** | **左**: 두 입자 접촉 overlap δ 모식. **右**: eq 6 piece-wise 선형 점착 이력 힘-변위 그래프 — k₁δ(초기재하), k₂(δ−δ₀)(제하/재하), −k_cδ(점착), δ₀(영구겹침), δ_min/f_min(최대인력), δ_max(최대겹침) 모두 표시 | **우리 `hooke/hysteresis` 접촉 LAW의 정의 그림.** δ₀=영구 소성겹침=우리 ε_sphere "displaced material". −k_cδ=우리 SE-SE adhesion. 슬라이드/논문 method에 이 그림을 인용(공개 라이선스) |
| **2** | 上: 인장 응력-변형 (k_c/k=1/2, 1, 20). 下: 압축 응력-변형. C₁ε 선형피팅(C₁ Fig2=3×10¹¹) | **점착 강성 k_c가 인장강도를 결정** — 강한 k_c → 인장강도↑·파괴 전 변형↑. **압축강도가 인장의 6–7×.** 초기기울기는 인장=압축(탄성 가역). 우리 SE-SE adhesion이 압밀 후 시료 결합력을 줌 |
| **3** | 인장시험 스냅샷(k_c/k=1/2, ε_xx≈0.8), 색=viewer 거리 | 약점착이면 **bulk에서 파단**; 강점착(k_c=20)이면 **벽에서 파단**. 균열 위치가 점착세기에 의존 — 우리 Auerbach/fracture 논의와 정성 연결 |
| **4** | 인장 응력-변형, 마찰·구름·비틀림 계수 변화 (μ=μᵣ=μ_o up to 100; μˢ=1·μᵈ=0.5) | **마찰·구름·비틀림은 인장강도에 거의 영향 없음**(점착이 지배). μ를 100까지 키워도 큰 변화 없음. → 인장강도는 **k_c가 주도, 마찰은 부차**. 우리 μ=0.5 선택이 인장강도엔 둔감하다는 근거 |

## 6. Post-processing ★

- **무엇**:
  - **압밀 모니터**: 부피분율 ν=ΣV(aᵢ)/V, 배위수 C(coordination). Heckel/percolation/coverage/tortuosity는
    **안 함**(이 논문은 LAW+강도시험 전용).
  - **응력 텐서**: 인장/압축 시험에서 거시 σ_xx 산출(균질 응력). C₁ε 선형피팅으로 탄성영역 추출.
  - **micro-macro 관계**: k는 모듈러스로 직접 비교 불가, **k ∼ C·a²/V** 관계(ref [42]) — 접촉강성↔벌크모듈러스
    스케일링.
- **도구**: 자체 DEM(논문 비특정). 시각화는 viewer(거리색).
- **수치화·플롯·기록 방식**: 모델 파라미터 Table 1(기호)·Table 2(값/rescaled/SI 3열). 인장·압축 σ_xx-ε_xx 곡선.
  단위계: t_u=1µs, x_u=1mm, m_u=1mg (rescaled), SI 환산인자(에너지 10³·가속도 10⁹·응력 10⁹) Table 2 주석.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ★★ **이 절이 핵심.** Luding 2008 = 우리 접촉 LAW의 *정의서*이므로 "대비"는 "literature 차이"가 아니라
> **우리 input 파라미터 ↔ Luding 기호의 1:1 매핑 + 우리 핵심 물리(f_AM·ε_sphere·18× 연화)의 LAW 근거**다.

### 7.1 ★★ 파라미터 1:1 매핑 — 우리 LIGGGHTS `hooke/hysteresis` input ↔ Luding eq 6

> 우리 input(예: `dem_scripts/thin9_seed.liggghts`, type 1=AM_P / 2=AM_S / 3=SE)에서 실측한 값. LIGGGHTS의
> `hooke/hysteresis` 모델은 **Luding eq 6의 직접 구현**이다(Walton–Braun 계열 = Luding이 일반화).

| LIGGGHTS input (우리) | Luding 기호 (eq 6) | 물리 의미 | 우리 real_14/thin9 값 (1=AM_P,2=AM_S,3=SE) |
|---|---|---|---|
| `fix m1 youngsModulus peratomtype` | **k₁** (initial loading) 의 출처 | 초기 재하 강성. LIGGGHTS가 E·반경에서 k₁ 산출(접촉강성∼E·a) | AM **1.4e8**(140 GPa) · SE **0.135e7**(=1.35 GPa, **18× 연화**) |
| `fix m6 coefficientMaxElasticStiffness` | **k̂₂ / k₂** (max/limit stiffness) | 제하·재하 가파른 가지의 상한. **소성겹침 δ₀=(1−k₁/k₂)δ_max를 만드는 핵심**. k̂₂>k₁ → 완전 이력 | **AM-AM 1.5** · AM-SE 3.0 · **SE-SE 5.0** (SE가 더 큰 cap) |
| `fix m7 coefficientAdhesionStiffness` | **k_c** (adhesion/cohesion) | 점착 가지 −k_c·δ 의 기울기. **접촉이 인장 버팀**(논문 제목) | **AM-AM 1.0e5** · AM-SE 2.0e5 · **SE-SE 1.0e6** (SE가 10× 점착) |
| `fix m8 coefficientPlasticityDepth` | **φ_f** (dimensionless plasticity depth) | 소성흐름 한계 δ*_max=(k̂₂/(k̂₂−k₁))·φ_f·(2a₁a₂/(a₁+a₂)) 결정. **클수록 늦게 항복** | **AM-AM 0.05** · AM-SE 0.01 · **SE-SE 0.005** (SE가 가장 일찍 항복) |
| `fix m3 coefficientRestitution` | **γ₀** (viscous) ↔ r (eq 5) | 반발계수 r=exp(−η₀t_c). γ₀를 r에서 역산 | 전부 **0.3** (r=0.3 < Luding 권장 0.4–0.8 하한 — 우리는 강한 소산) |
| `fix m4 coefficientFriction` | μˢ=μᵈ (Coulomb) | 접선 마찰. 점착 시 한계 μˢ(fⁿ+k_cδ) | 전부 **0.5** |
| `fix m5 coefficientRollingFriction` | μᵣ (rolling) | 구름저항(표면거칠기/비구형 흉내) | AM 0.2 / 0.1 혼합, SE-SE **0.1** |
| `fix m9 characteristicVelocity` | (LIGGGHTS hysteresis 내부 v_char) | 강성 보간 기준속도 | scalar **2.0** |
| `pair_style gran model hooke/hysteresis` | **eq 6 그 자체** | 점착 탄소성 이력 = Luding LAW | (모델 선택) |

★ **읽는 법**: 우리 input의 `m6/m7/m8` 세 줄이 곧 **Luding의 k̂₂·k_c·φ_f**다. **SE 쌍이 AM 쌍보다 (a) max
강성 cap이 크고(5.0>1.5) (b) 점착이 10× 크고(1e6>1e5) (c) 더 일찍 항복(φ_f 0.005<0.05)** — 즉 SE 접촉을
**더 무르게·끈끈하게·소성적으로** 설정. 이 *SE-우대 비대칭*이 §7.3의 f_AM 결과를 만든다.

⚠ **단, k₁의 정확한 LIGGGHTS 산출식은 코드 의존**(youngsModulus·반경·characteristicVelocity에서 내부 계산)
→ 위 "youngsModulus↔k₁"은 *물리적 대응*이며 정확한 수식 등호는 아니다. k̂₂/k_c/φ_f는 **직접 계수**라 등호.

### 7.2 ★★ δ₀ (영구 소성겹침) = 우리 ε_sphere "displaced material" 규약

CLAUDE.md / `esse_calibration` 의 ε_sphere 규약: *"소성 압밀에서 변위된 접촉 물질은 bulge로 재출현 → solid =
Σ 원래 구 부피"* (material-conserving). **Luding의 δ₀ = (1−k₁/k₂)·δ_max 가 바로 그 영구 overlap이다:**
- 제하해도 δ가 0으로 안 돌아가고 δ₀만큼 **영구히 겹친 채** 남음 = "압흔이 남는다".
- 우리 ε_sphere가 "겹침을 void에서 빼지 않고 원래 부피로 센다"는 것은 **그 δ₀ 만큼의 물질이 사라진 게
  아니라 bulge로 옮겨갔다**는 가정. Luding LAW는 이 영구겹침이 **소성 분기에서 자연 발생**함을 보장한다.
- ⚠ 단 Luding δ₀는 **접촉점 overlap**(국소)이고 우리 ε_sphere는 **입자부피 합산**(전역) — 두 단계가
  연결되려면 "δ₀ 만큼의 겹침 부피가 bulge로 보존"이라는 비압축 가정이 필요(우리 규약이 명시하는 바).
  ⇒ **ε_sphere가 ε_union보다 물리적으로 옳은 이유의 LAW 근거 = δ₀ 영구겹침이 실재**(Luding eq 6).

### 7.3 ★★ f_AM(실제 LAW ≠ Hertz)의 근거 — eq 6 = 그 "실제 LAW"

`docs/mpm_wallP_conditional_troubleshooting.md §12` 발견(real_14 dump):
- **실제 hooke 접촉력 Love-Weber σzz 분해**: AM-AM **0.670** · AM-SE 0.276 · SE-SE 0.053. (per-atom virial
  AM-phase 0.809.)
- **Hertz 재구성**(δ^1.5 순수탄성): E_SE=1.35 → AM-AM **0.843**(과대); E_SE=24 → AM-AM **0.258**(과소).
  → **어떤 단일 Hertz 모듈러스도 실제 0.670을 못 맞춤** (위로·아래로 갈라짐).
- **이 간극의 정체 = Luding eq 6 vs Hertz의 LAW 형태 차이**:
  | 메커니즘 (eq 6) | Hertz엔 없음 | f_AM에 미치는 효과 |
  |---|---|---|
  | **선형 k₁δ** (vs Hertz δ^1.5) | δ^1.5 → 깊을수록 더 가파름 | Hertz가 깊은(=큰 AM-AM) 접촉을 과대평가 |
  | **plasticityDepth φ_f** (SE 0.005 일찍·AM 0.05 늦게 항복) | 항복 없음 | SE가 일찍 항복(무름) → SE쪽이 하중 더 받음 → AM-AM 감소 |
  | **maxElasticStiffness k̂₂** (SE-SE 5.0 > AM-AM 1.5) | cap 없음 | SE 접촉 강성 cap이 높아 SE가 더 버팀 → AM-AM 감소 |
  | **adhesion −k_cδ** (SE-SE 1e6 ≫ AM-AM 1e5) | 점착 없음(압축 순수반발) | SE-SE 인력이 SE망 결속 → 하중경로 SE로 | 
  - ⇒ **이 SE-우대 항(φ_f·k̂₂·k_c)들이 AM-AM에서 하중을 떼어 SE로 보낸다** → 실제 0.670 < Hertz 0.843.
    Hertz는 이 항들이 전무하므로 구조적으로 AM-AM을 과대평가.
- **결론(LAW 측면):** 믿을 f_AM = **eq 6(hooke/hysteresis) 접촉력 직접측정**(0.670/0.809), **Hertz 재구성 아님.**
  Luding 2008이 그 eq 6의 정의서 → `scripts/dem_am_load_fraction.py`의 hooke f_AM 측정이 **물리적으로 정당**함을
  이 논문이 뒷받침. (Hertz scaffold 0.847은 per-atom AM-phase 0.809에 *우연히* 근접 → bounded-safe, §12.)

### 7.4 ★★ 18× 연화의 LAW 근거 — eq 6은 소성 분기는 있으나 **경도/항복압 캡이 없다**

- 우리 18× 연화(E_SE 24→1.35): hooke/hysteresis는 **~선형**(k₁δ)이라 같은 300 MPa에서 진짜 소성보다 overlap이
  부족 → E를 18× 낮춰 overlap을 강제(displaced-material 보상).
- **Luding LAW가 정확히 이 한계를 보여줌**: eq 6은 **소성 분기(k₁→k₂)와 영구겹침(δ₀)은 가지지만, 접촉면이
  항복압 p_y(또는 경도 H)에 도달하면 평균압을 cap하는 메커니즘이 없다.** §1.2/§2.3.2가 "큰 변형서 물리가
  바뀌고 모델은 단순 선형 최대강성 분기로 *제한*된다(questionable in large deformation)"고 명시.
- ⇒ **eq 6 = '소성을 흉내내되 경도 캡이 없는' LAW** = 우리 18× 연화가 보상하는 바로 그 결함. `elasto_plastic_
  feasibility.md` **경로 A**(So 2021 H-cap)가 "eq 6에 항복압/경도 캡을 더해 real E로 연화 없이 압밀"하자는
  제안이며, Luding 모델은 그 **출발 LAW**(캡 추가 전 상태)다.
  - 즉 So 2021의 H-cap ≈ **eq 6 + (접촉 평균압 ≤ H 제약)**. Thornton–Ning(WISHLIST #14)은 같은걸 Hertz 기반
    항복으로 함. Luding eq 6은 **선형 기반**이라 LIGGGHTS에서 H-cap을 얹기 더 단순(경로 A 1순위 근거).
- ⚠ **MPM cap/jam dead-end과 모순 아님**: 그건 *연속체 볼륨 cap*, 여기 18× 연화/경로 A는 *이산 접촉 LAW*의
  경도 캡(다른 메커니즘). frame[5] 분업 유지: eq 6 + H-cap을 넣어도 **입자 SHAPE 흐름·morphology·변형장은
  여전히 못 줌**(overlap은 기하 proxy) → 그건 MPM 영역.

### 7.5 ★ 점착(k_c) = 우리 SE-SE cold-weld/vdW + MPM `--coh`

- Luding의 **−k_c·δ 인장 분기**가 "접촉이 인장을 버틴다"의 정의. 우리 SE-SE adhesionStiffness 1e6(AM의 10×)
  = SE 입자간 **cold-weld/vdW 결합**의 DEM 표현. 압밀 후 시료가 한 덩어리로 결합(Fig 2의 인장강도)되는 물리.
- **MPM `--coh` knob (backlog A3)** = 같은 점착을 연속체 SE에 준 것(압축 시 attractive σ). Luding이 **그 점착의
  이산 정의·정성거동**(k_c↑→인장강도↑, 압축이 인장의 6–7×, k_c↑→bulk 대신 벽에서 파단)을 제공. → `--coh`
  도입 시 **k_c↔coh 매핑·검증의 정성 기준**.
- ★ **k₁/k̂₂=1 선형 특수극한**: Luding은 점착이력모델이 **선형 스프링을 특수경우로 포함**함을 보임(k_c·φ_f
  무의미). 우리 SE/AM은 **k̂₂>k₁**(완전 이력)을 쓰므로 선형 극한이 아님 — 즉 우리는 Luding 모델의 *완전판*을 씀.

### 7.6 비교 요약표

| 항목 | 이 논문 (Luding 2008) | 우리 | 차이 / 관계 |
|---|---|---|---|
| 접촉 LAW | **eq 6 점착 탄소성 이력**(k₁·k̂₂·k_c·φ_f·γ₀) | LIGGGHTS `hooke/hysteresis` (= eq 6 구현) | **동일 LAW** ✓ — 이게 우리 모델의 *정의* |
| max 강성 cap | k̂₂ | `coefficientMaxElasticStiffness`(SE5/AM1.5) | **1:1 매핑** ✓ |
| 점착 강성 | k_c | `coefficientAdhesionStiffness`(SE1e6/AM1e5) | **1:1 매핑** ✓ |
| 소성 깊이 | φ_f | `coefficientPlasticityDepth`(SE0.005/AM0.05) | **1:1 매핑** ✓ |
| 영구 소성겹침 | **δ₀=(1−k₁/k₂)δ_max** | ε_sphere "displaced material" 규약 | **같은 물리** ✓ — δ₀가 ε_sphere의 근거 |
| 소성 종류 | **CONTACT-LAW**(층위1) — rigid 구 | DEM도 CONTACT(층위1); SHAPE는 MPM | **같은 한계**(SHAPE 없음) — frame[5] |
| 경도/항복압 캡 | **없음**(LAW 한계, 큰변형서 questionable) | 없음 → **18× 연화로 보상** | 우리 연화의 *원인*이 이 LAW 결함 |
| 전달 σ | **전혀 없음**(역학 전용) | σ_ionic+σ_e+σ_thermal 삼중항 | 우리가 전달 절반 추가(frame[5]) |
| morphology/변형장 | 없음(rigid 구) | MPM 진짜 형상변화·Σdg | 우리 MPM이 보강 |
| 소재 | **소재 무관**(일반 µm 분말) | LPSCl/NMC811 | **절대값 전이 불가**(ν·강도 무차원/예시) — 정성·LAW만 |
| 차원 | 3D(N=1728) + 2D 표기 통용 | 3D DEM | (인장데모는 cuboid 3D) |

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **method 섹션의 접촉 LAW 정의서로 직접 인용** (OPEN ACCESS): "우리 DEM은 Luding(2008)의 점착 탄소성
  이력 접촉모델(eq 6)을 LIGGGHTS `hooke/hysteresis`로 구현 — k̂₂=`maxElasticStiffness`, k_c=
  `adhesionStiffness`, φ_f=`plasticityDepth`." 유료 Walton–Braun 1986 대신 이걸 citation으로. §7.1 표를
  논문 SI/method 표로 그대로 사용.
- ② **f_AM 측정의 정당화** (`dem_am_load_fraction.py`): "AM 하중분담은 **eq 6 접촉력**으로 측정해야지 Hertz
  근사로 재구성하면 안 된다(φ_f·k̂₂·k_c의 SE-우대가 AM-AM 하중을 떼어 SE로 보내므로)." → §7.3. wallP 조건부
  doc §12를 이 LAW 근거로 보강.
- ③ **ε_sphere 규약의 LAW 근거**: "displaced-material 가정은 Luding δ₀=(1−k₁/k₂)δ_max(영구 소성겹침)에
  대응 — ε_sphere가 ε_union보다 물리적인 이유." → CLAUDE.md 규약설명에 인용.
- ④ **경로 A(항복캡 DEM)의 출발 LAW**: "Luding eq 6은 소성 분기는 있으나 경도/항복압 캡이 없다 → 18× 연화로
  보상. 경로 A = eq 6 + (접촉 평균압 ≤ H) 제약(So 2021 H-cap / Thornton–Ning p_y)으로 real E 압밀." →
  `elasto_plastic_feasibility.md §1·§5` 보강. LIGGGHTS에 H-cap 얹기가 선형 기반이라 단순함이 1순위 근거.
- ⑤ **`--coh`(MPM 점착, backlog A3) 매핑 기준**: k_c↔coh 정성거동(인장강도·압축 6–7×·파단위치)을 Luding
  Fig 2–3에서 가져와 검증 기준 삼기.

## 9. 인용 가능 문장 (deck/paper용)

- "우리 DEM의 법선 접촉은 Luding(2008, Granular Matter, open access)의 점착 탄소성 이력 모델 — 초기재하 k₁,
  제하·재하 k₂(한계 k̂₂), 점착 −k_c, 소성깊이 φ_f — 을 LIGGGHTS `hooke/hysteresis`로 구현하며, 우리 input의
  `maxElasticStiffness`/`adhesionStiffness`/`plasticityDepth`가 각각 k̂₂/k_c/φ_f에 1:1 대응한다."
- "이 모델의 영구 소성겹침 δ₀=(1−k₁/k₂)δ_max 는 우리 ε_sphere(material-conserving) porosity 규약이 가정하는
  바로 그 영구 overlap이며, 따라서 displaced-material 가정에 물리적 근거를 준다."
- "Hertz(δ^1.5, 순수탄성)는 우리 실제 접촉 LAW가 아니다 — Luding 모델의 소성깊이·최대강성·점착 항이 하중을
  AM-AM에서 SE로 재분배하므로, AM 하중분담은 실측 hooke 접촉력으로 계산해야지 Hertz로 재구성하면 안 된다
  (Hertz는 어떤 단일 모듈러스로도 실측 0.670을 재현 못 함; E=1.35→0.843, E=24→0.258)."
- "Luding 모델은 소성 분기(k₁→k₂, δ₀)는 갖지만 경도/항복압 캡이 없어 큰 변형서 한계가 있다(저자 명시) —
  이것이 우리가 E_SE를 18× 연화(24→1.35 GPa)하여 보상하는 결함이며, 경도 캡을 더하는 것이 향후 경로다."

## 10. 주의/한계 (over-claim 방지)

- **소재 데이터 없음 = 절대값 전이 불가.** 이 논문은 LAW 정의서 — LPSCl·NMC811 σ·porosity·강도 절대값을 주지
  않는다. ν=0.6754·C=7.16 등은 무차원 예시이며 **우리 압밀 절대값과 직접 비교 금지**. 가치는 **수식·파라미터
  정의·정성거동·우리 모델의 LAW 근거**에 있다.
- **rigid 구 + CONTACT 소성만**(층위1). 입자 SHAPE 흐름·morphology·변형장 전무 — 우리 MPM 영역. "soft
  particle MD"의 'soft'는 *접촉 overlap이 허용된다*는 뜻이지 입자가 변형된다는 뜻이 아님(혼동 주의).
- **전달 σ 전혀 없음**(역학 전용) → frame[5]의 역학 절반만. σ_ionic/e/thermal 비교점 0.
- **piece-wise 선형 단순화** — 비선형 Walton(94,96)의 근사판. 큰 변형서 questionable(저자 명시). **경도/항복압
  캡 없음** = 우리 18× 연화가 보상하는 결함(장점이 아니라 한계).
- **좁은 Gaussian PSD**(mono에 가까움) — bi/poly-PSD 아님. Furnas-dip/패킹 효과는 이 논문 범위 밖.
- **k₁↔youngsModulus는 물리적 대응**(정확한 LIGGGHTS 내부식 등호 아님). k̂₂/k_c/φ_f만 직접계수 등호.
- **반발계수 r=0.3**(우리) < Luding 권장 0.4–0.8 하한 → 우리는 의도적으로 강한 점성소산(준정적 압밀 안정화).
  Luding은 r<0.4를 "artificially strong viscous"라 부름 — 우리 압밀은 동역학이 아니라 준정적이라 무방하나,
  **충돌 동역학을 본다면 r 재고 필요**(우리는 압밀이라 해당없음).

## Supplementary Information

**없음** (사용자 지시: SI 없음). 본문 12쪽 자체가 완결.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

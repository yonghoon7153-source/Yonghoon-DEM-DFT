# DEM 지배방정식 보고서 — 발표용 문헌 기본형 ↔ 우리 코드 구현식 (LIGGGHTS-PUBLIC 3.8.0 · 3d5c00f) — 2026-10-09

- **왜 둘로 나누나 (1저자 10-09)**: 발표 슬라이드에는 문헌의 대표 지배방정식을 **감쇠 · 점착 등을 뺀 기본형**으로 싣는다.  우리 코드가 실제로 푸는 식 (구현식) 은 이 보고서에 따로 둔다.
- **코드**: LIGGGHTS-PUBLIC 3.8.0 · git `3d5c00f` (2024-06-07 "Remove logos") — ibb 빌드 배너 · `lmp_mpi` sha256 `ee2d7726…` 와 같은 커밋 (`docs/reviews/dem_unloading_ps45_precheck1_20261009/README.md` §2).
  덱 = `pair_style gran model hooke/hysteresis tangential history rolling_friction cdt` (ps45 원 덱 · 다섯 조성 덱의 재료 · 접촉 · 적분 줄은 서로 같다 — 10-09 diff 0 줄).
- **근거 파일**: 소스 사본 5 개 `docs/data/liggghts_3d5c00f_dem_eq_source_20261009/` (공개 저장소 github.com/CFDEMproject/LIGGGHTS-PUBLIC 의 그 커밋 그대로 · SHA256SUMS · 줄 번호는 이 사본 기준) ·
  같은 커밋의 설명서 쪽 (gran_model_hooke · gran_tangential_history · gran_rolling_friction_cdt · fix_nve_sphere · fix_gravity · fix_viscous) · 문헌 = litdb 정본 카드 luding2008_cohesive_frictional_contact_models
  (S. Luding, Granular Matter 2008, DOI 10.1007/s10035-008-0099-x · 오픈 액세스 — 카드 표현으로 "우리 hooke/hysteresis + adhesion + plasticity-depth 접촉법칙의 이론 정의서").
- **한정**: 식 판독 = 내 소스 · 덱 판독 (10-09) — 실행으로 재현한 것이 아니다.  이 보고서는 **수식 근거 자료**이고, 조건표 수치가 실제 런과 일치하는지 · SE 유효 영률 1.35 GPa 보정이 타당한지를 검증한 자료가 아니다 (발표 리뷰 의견 그대로).

## 1. 한눈에 — 슬라이드 기본형 ↔ 구현식

기호: k₁ ≡ 코드 kn (하중 강성) · k₂ = 제하 · 재하 강성 · k₂,max = kn × coefficientMaxElasticStiffness · k_c = kn × coefficientAdhesionStiffness · φ_F = coefficientPlasticityDepth · R* · m* · E* = 환산 반경 · 질량 · 영률 · V = characteristicVelocity.

| 식 | 슬라이드 (문헌 기본형) | 구현식 (코드가 푸는 것) | 소스 (사본 줄) | 기본형에서 뺀 것 |
|---|---|---|---|---|
| ① 병진 | m_i dv_i/dt = Σ_j (F_n,ij + F_t,ij) + m_i g | 같은 식 + 전역 감쇠 −γ v_i (`fix viscous`) — 적분 v += Δt/(2m)·F | fix_nve_sphere.cpp 167–170 · 설명서 fix_gravity · fix_viscous ("F = − gamma * velocity") | −γ v_i (덱에서 단계마다 1e-5 → 0.5 → 1e-5) |
| ② 회전 | I_i dω_i/dt = Σ_j (R_i n_ij × F_t,ij + M_r,ij) · I_i = (2/5) m_i R_i² | 접선력 토크의 지렛대 = **접촉 반지름 c_ri = R_i − δ/2** (설명서 gran_model_hooke "contactradius") · I = 0.4 m R² | tangential_model_history.h 229–231 · 254–256 · fix_nve_sphere.cpp 68 · 158 · 179 | c_ri → R_i (구 근사) |
| ③ 법선 | F_n = k₁δ (loading) · k₂(δ − δ₀) (unloading) · δ₀ = (1 − k₁/k₂) δ_max | 비포화 (δ_max < δ_lim): F_n = max{min[k₁δ, k₂(δ − δ₀)], −k_c δ} − γ_n v_n · k₂ = k₂(δ_max) ·<br>포화 (δ_max ≥ δ_lim = k₂,max/(k₂,max − k₁)·φ_F·2R*): F = k₂,max(δ − δ_lim) + k₁ δ_lim · δ_max 는 접촉마다 기록 (분리하면 0) | normal_model_hooke_hysteresis.h 139–141 · 150–151 · 156–159 · 163 · 166–176 · 180–193 · 197–198 | 점착 가지 −k_c δ (F_n < 0 쪽) · 접촉 감쇠 −γ_n v_n · 포화 가지 · k₂(δ_max) 보간 |
| ④ 접선 | F_t = −k_t δ_t · ‖F_t‖ ≤ μ F_n | 비미끄럼: −k_t δ_t − γ_t v_t · 미끄럼 (‖k_t δ_t‖ > μ\|F_n\|): 크기를 μ\|F_n\| 로 자르고 기록 재설정 · 감쇠 없음 · **k_t = k_n** · μ = coefficientFriction (설명서 기호 cof · 소스 변수 xmu) | tangential_model_history.h 149–158 · 163 · 166–168 · 175 · 178–210 · 212–217 | 비미끄럼 접선 감쇠 −γ_t v_t |
| ⑤ 구름 저항 | 기호 M_r 만 | M_r = −μ_r k_n δ R* · ω_r/‖ω_r‖ · ω_r = ω_i − ω_j · torsionTorque off 이면 법선 성분 제거 · i 에 −, j 에 + | rolling_model_cdt.h 135 · 145 · 147–155 · 160–166 (벽 가지 104–131) | (슬라이드는 정의를 싣지 않음) |
| ⑥ 강성 · 감쇠 계수 | (슬라이드 없음) | k_n = (16/15)·√R*·E*·[15 m* V²/(16 √R* E*)]^(1/5) · k_t = k_n · 1/E* = (1−ν_i²)/E_i + (1−ν_j²)/E_j · γ_n = √(4 m* k_n / (1 + (π/c)²)) · c = 코드 변수 coeffRestLogChosen (반발계수 e 의 로그로 보임 — 미확인) | normal_model_hooke_hysteresis.h 139–141 · global_properties.cpp 432 | — |

- ⚠ 구름 저항: 설명서 문장은 `w_r_shear/mag(w_r_shear)` (비틀림을 뺀 성분 크기로 나눔) 인데 소스는 전체 ‖ω_r‖ 로 나눈 뒤 법선 성분을 뺀다 — 이 보고서 · 10-09 식 슬라이드는 **소스**를 따른다.
- 입자–입자 · 입자–벽 (판 메시 · 바닥) 접촉은 같은 모델이다 (덱의 `fix ... wall/gran` · `mesh/surface/stress` 가 같은 `model hooke/hysteresis tangential history rolling_friction cdt`).

## 2. 핵심 소스 줄 (사본에서 그대로)

```
normal_model_hooke_hysteresis.h:139  double kn = 16./15.*sqrtval*(Yeff[itype][jtype])*pow(15.*meff*charVel*charVel/(16.*sqrtval*Yeff[itype][jtype]),0.2);
normal_model_hooke_hysteresis.h:140  double kt = kn;
normal_model_hooke_hysteresis.h:141  const double gamman = sqrt(4.*meff*kn/(1.+(M_PI/coeffRestLogChosen)*(M_PI/coeffRestLogChosen)));
normal_model_hooke_hysteresis.h:150  const double k2Max = kn * kn2k2Max[itype][jtype];
normal_model_hooke_hysteresis.h:151  const double kc = kn * kn2kc[itype][jtype];
normal_model_hooke_hysteresis.h:163  const double deltaMaxLim =(k2Max/(k2Max-kn))*phiF[itype][jtype]*2*reff;
normal_model_hooke_hysteresis.h:169  const double fTmp = k2*(deltan-deltaMaxLim)+kn*deltaMaxLim;//k2*(deltan-delta0);
normal_model_hooke_hysteresis.h:182  if (fTmp >= kn*deltan) { // loading part (kn)
normal_model_hooke_hysteresis.h:183      fHys = kn*deltan;
normal_model_hooke_hysteresis.h:184  } else { // un-/reloading part (k2)
normal_model_hooke_hysteresis.h:185      if (fTmp > -kc*deltan) {
normal_model_hooke_hysteresis.h:186          fHys = fTmp;
normal_model_hooke_hysteresis.h:187      } else { // cohesion part
normal_model_hooke_hysteresis.h:188          fHys = -kc*deltan;
normal_model_hooke_hysteresis.h:197  const double Fn_damping = -gamman*sidata.vn;
normal_model_hooke_hysteresis.h:198  const double Fn = fHys + Fn_damping;
tangential_model_history.h:163       const double xmu = coeffFrict[sidata.itype][sidata.jtype];
tangential_model_history.h:166       double Ft_ela1 = -(kt * shear[0]);
tangential_model_history.h:175       const double Ft_friction = xmu * fabs(sidata.Fn);
tangential_model_history.h:230       const double tor1 = eny * Ft3 - enz * Ft2;
rolling_model_cdt.h:135              vectorSubtract3D(atom->omega[sidata.i],atom->omega[sidata.j],wr_roll);
rolling_model_cdt.h:145              vectorScalarMult3D(wr_roll,rmu*sidata.kn*sidata.deltan*reff/wr_rollmag,r_torque);
global_properties.cpp:432            matrix->data[i][j] = 1./((1.-pow(vi,2.))/Yi+(1.-pow(vj,2.))/Yj);
fix_nve_sphere.cpp:68                #define INERTIA 0.4          // moment of inertia prefactor for sphere
fix_nve_sphere.cpp:168               v[i][0] += dtfm * f[i][0];
```
(줄 앞 공백은 줄였다 · 내용은 사본 그대로.  비포화 가지의 fTmp = k2·(δ − δ₀) 는 180–181 행.)

## 3. 덱 값 (ps45 원 덱 · `docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` · sha256 `69f4359c0f436ebe…` · 다섯 조성 같은 줄)

```
  44  timestep        ${dt}
   ⋮
  57  fix m1 all property/global youngsModulus peratomtype 1.4e8 1.4e8 0.135e7
  58  fix m2 all property/global poissonsRatio peratomtype 0.25 0.25 0.30
  59  
  60  fix m3 all property/global coefficientRestitution peratomtypepair 3 &
  61      0.3 0.3 0.3 &
  62      0.3 0.3 0.3 &
  63      0.3 0.3 0.3
  64  
  65  fix m4 all property/global coefficientFriction peratomtypepair 3 &
  66      0.5 0.5 0.5 &
  67      0.5 0.5 0.5 &
  68      0.5 0.5 0.5
  69  
  70  fix m5 all property/global coefficientRollingFriction peratomtypepair 3 &
  71      0.2 0.2 0.1 &
  72      0.2 0.2 0.1 &
  73      0.1 0.1 0.1
  74  
  75  fix m6 all property/global coefficientMaxElasticStiffness peratomtypepair 3 &
  76      1.5 1.5 3.0 &
  77      1.5 1.5 3.0 &
  78      3.0 3.0 5.0
  79  
  80  fix m7 all property/global coefficientAdhesionStiffness peratomtypepair 3 &
  81      1.0e5 1.0e5 2.0e5 &
  82      1.0e5 1.0e5 2.0e5 &
  83      2.0e5 2.0e5 1.0e6
  84  
  85  fix m8 all property/global coefficientPlasticityDepth peratomtypepair 3 &
  86      0.05 0.05 0.01 &
  87      0.05 0.05 0.01 &
  88      0.01 0.01 0.005
  89  
  90  fix m9 all property/global characteristicVelocity scalar 2.0
  91  
  92  # --- 4. Contact Model ---
  93  pair_style      gran model hooke/hysteresis tangential history rolling_friction cdt
   ⋮
 137  thermo_style    custom step atoms ke cpu
 138  thermo          1000
 139  
 140  # --- 9. Phase 1: Settling ---
 141  print "====== PHASE 1: SETTLING ======"
 142  fix integr all nve/sphere
 143  fix gravi all gravity 98.1 vector 0.0 0.0 -1.0
 144  fix damp all viscous 1.0e-5
 145  
   ⋮
 189  fix gravi all gravity 9.81 vector 0.0 0.0 -1.0
 190  unfix damp
 191  fix damp all viscous 0.5
   ⋮
 217  fix damp all viscous 1.0e-5
   ⋮
```

- 단위 · 축척: `units si` · 길이 × 1000 (µm → 덱 mm) — 영률 덱 값 × 1000 = 실제 값 (AM 1.4e8 → 140 GPa · SE 0.135e7 → **1.35 GPa = SE 접촉 강성에 쓰는 유효 모델 입력값**, 재료의 실측 영률과 구분) ·
  판 압력 기준 0.30 (덱) = 300 MPa · 중력 9.81 (덱) 그대로라 자중 응력이 실제의 10⁶ 배 (`docs/reviews/dem_unloading_ps45_prereg_20261009.md` §9-8).
- 감쇠 단계: 정착 `viscous 1.0e-5` → 압축 `viscous 0.5` → 이완 `viscous 1.0e-5` (덱 142–144 · 189–191 · 217 행 꼴 — 압축 중 판 힘의 큰 몫이 이 감쇠 저항이었다 · 원장 `DEMP-01`).

## 4. 슬라이드 기본형의 문헌 근거 (litdb 정본 카드 luding2008 에서)

| 슬라이드 식 | Luding 2008 (카드가 적은 대로) | 뺀 항 |
|---|---|---|
| ① · ② 운동방정식 | Eq. 1 (Newton 시간적분) | 전역 감쇠 · 배경 마찰 (§2.6) |
| ③ 이력 스프링 | Eq. 6: k₁δ (loading) · k₂(δ − δ₀) (un/reloading) · −k_c δ (adhesive) · 최종 fⁿ = f^hys + γ₀ vₙ · k₁ ≤ k₂ ≤ k̂₂ · δ₀ = (1 − k₁/k₂) δ_max | 점착 가지 · γ₀ vₙ |
| ④ 접선 마찰 | Eq. 18–20: Cundall–Strack 접선 스프링 · 시험력 −k_t ξ − γ_t v_t · Coulomb 한계 μˢ(fⁿ + k_c δ) · 정지 / 미끄럼 갱신 | γ_t v_t · 점착 (k_c δ) |
| 구름 저항 | §2.4.3 (k_r · μ_r · γ_r 스프링형) — LIGGGHTS CDT 와 꼴이 다르다 | 슬라이드는 기호 M_r 만 |

- 카드에 없는 서지 (Cundall & Strack 1979 · Walton & Braun 1986 · Ai 2011 · Kloss 2012 · Di Renzo 2004) 는 이 보고서 · 슬라이드에 넣지 않았다 (규율 ⑥ — 원문 카드 없음).

## 5. 산출물 (리포 밖)

- 발표 슬라이드 초안 (1저자 덱 위 · 가운데 = 1저자 그림 그대로 · 둘레 = 기본형 식 넷) — 1저자에게 전달 (10-09 · 덱은 리포에 넣지 않는다).
- LIGGGHTS 3.8.0 (3d5c00f) 고정 버전 설명서 · 소스 발췌본 PDF (34 쪽) — 1저자에게 전달 (10-09).

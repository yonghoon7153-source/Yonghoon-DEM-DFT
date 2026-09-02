# Methods — 시뮬레이션 절 개정안 v7 (2026-08-29)

> # ⛔⛔ `PROVISIONAL — NOT FOR SUBMISSION`
> **Codex R10 판정: 투고 준비 NO-GO · 완성된 Methods 교체안으로 전달 NO-GO.**
> 공저자에게는 **쟁점을 결정하기 위한 provisional review package** 로만 보낸다.
> 해제조건 8개: `docs/reviews/codex_r10_verdict_20260829.md`.
>
> ⚠ **정본 원장이 이미 HOLD 다** — `table_s3_data_20260827.md` 헤더가
> `RAW_W4_VERIFIED_UNTRACKED · 원고 승격 HOLD` 라고 적는다 (W4 16팔 JSON·receipt 가
> 리포에 없어 제3자가 σ_e 를 재검증할 수 없다).  **그런데 이 초안은 그 값을 reported 로
> 승격했다** — 내가 쓴 헤더를 내가 어겼다.  원자료 커밋 전까지 이 표는 투고용이 아니다.

> 대상: `Manuscript v6` 의 *"DEM simulations:"* 문단 (Methods) + SI Table S2 · S3.
> 감사 근거: `ms_si_v6_audit_20260829.md` · 수치 정본 `table_s3_data_20260827.md`.
> **두 판을 낸다** — ⓐ **설명형**(독자가 이해하게) · ⓑ **압축형**(지면 제약용).
> 두 판은 **같은 사실**을 담는다.  압축은 문장을 줄이는 것이지 한정어를 빼는 것이 아니다.

## ★ v6 대비 무엇이 바뀌나 (넷)

| # | v6 | v7 | 왜 |
|---|---|---|---|
| 1 | 전 과정을 "DEM" 으로 부름 | **DEM · MPM · voxel FV 를 이름으로 분리** | 세 도구다.  표 제목·그림 설명이 전부 DEM 이라 협업자도 MPM 을 못 봤다 |
| 2 | *"E 를 24 → 1.35 로 연화"* 가 앞 | **porosity 표적이 앞, E 는 노브로 뒤** | 실제로 한 일이 그것이다.  ⚠ 두 값은 표에 **그대로 남긴다** |
| 3 | *"paired mean with its **standard error**"* | **origin-phase spread + range**, SE·CI 명시 부정 | 8 origin 은 한 침대의 완전 factorial — 복제 오차 자유도 0 (R8 Q1) |
| 4 | PTFE 규약·σ_VGCF 규약 암묵 | **둘 다 명시**.  본문은 공칭 규약 값 하나, 규약 민감도는 **Table S3c** | 이득이 규약에 의존한다 (1.124 ↔ 1.308) — 관행대로 **민감도 절**에 둔다 |

★★ ~~**주 규약 = PTFE 를 차단상으로 그린다**~~ — **R10 Q1 [P1] 로 기각**.

⚠⚠ **두 번 틀렸다.**
① 처음엔 "안 그림" 을 주 규약으로 썼고 이유는 **편집 편의**였다.
② 지적받고 "차단" 으로 뒤집었는데, **두 값을 본 뒤에 큰 쪽으로 옮긴 것**이라 결과 독립이
   아니다.  물리적 우려 자체는 결과 전에도 있었으나, **생산 승격은 명시적으로 보류돼**
   있었고 그것을 값을 본 뒤 바꿨다.

★ 더 근본적으로 — **centerline 은 PTFE 를 "resolved" 한 규약이 아니다.**
구현은 **한 셀 폭 centerline** 을 찍고 그 셀을 **정확히 0-DOF 로 제거**한다.  직경 인식
`capsule` 은 **미구현 예약값**이다.  ⇒ 얇은 코팅의 **공간 범위는 과소**표현하면서 찍힌
셀에서는 **차단을 과대**한다.  따라서:
- `off` 가 **보수적이라는 판정도 성립하지 않는다** — 더 작은 이득을 냈을 뿐 물리적 하한임이
  입증된 바 없다.
- *"PTFE 를 빼면 치환의 절반이 사라진다"* 도 **과장**이다.  PTFE 의 함량과 역학 효과는
  **DEM–MPM 침대에 남는다** (W2 실측: PTFE 만 E 가 바뀌어 변위가 달라졌다).  사라지는 것은
  **전자격자의 직접 절연배제 채널** 하나다.

⇒ `resolved` 라는 말을 **쓰지 않는다** — 어느 쪽도 PTFE 를 해상하지 않았다.  본문은 **공칭
규약 값 하나**를 쓰고, 규약을 바꿨을 때의 변화는 **Table S3c (민감도)** 로 내린다:

| 규약 라벨 | σ_ele SBE | DBE | 비 | PTFE 부피 표현 |
|---|---|---|---|---|
| **`PTFE centerline voxels excluded`** — **본문 공칭 규약** | 54.0 | 70.6 mS cm⁻¹ | **1.308** | **0.43** |
| `PTFE omitted from the electronic grid` — Table S3c 민감도 | 72.3 | 81.3 | 1.124 | **0.00** |

★★ **보고 규약 = centerline** (사용자 결정 2026-08-29).  본문은 **값 하나**를 쓰고,
규약 민감도는 **Table S3c** 에 둔다.

⚠ **형식 근거 (2026-08-29 확인)**: 같은 재료계·같은 코드의 **Bazzoun 2025** 는 파라미터
민감도를 **별도 절**에 싣고 본문은 공칭값 하나를 쓴다.  우리 litdb **65장 어디에도**
*"두 규약을 동등하게 병기하고 어느 쪽도 primary 로 지정하지 않는다"* 는 형태가 **없다**.
⇒ 초안이 그 형태였던 것은 **출판 관행이 아니라 내가 지어낸 형식**이었다.

⚠ **내부적으로 유지되는 것** (원고에 쓰지 않는다): A1 사전등록 판정은
*"centerline 을 **교정된 표현**으로 채택하지 않는다"* 였고 **그대로다** (부피비 0.428 / 0.422,
등록 밴드 [0.5, 2.0] 밖).  본문이 centerline 을 쓰는 것은 *"교정됐다"* 가 아니라
**공칭 규약**으로 쓰는 것이고, 그 선택의 정량 근거(표현 부피 0.43 vs 0.00)는 Table S3c
각주에 있다.  ⛔ *"centerline 이 참값에 가깝다"* · *"부피를 더 그리니 전도가 더 맞다"* ·
*"실험에 더 가까워서 골랐다"* 는 **셋 다 쓰지 않는다** (근거는 `ptfe_convention_prereg`).

**코드 기본값은 옮기지 않는다** (R10 Q2 — 사후 primary 를 정당화하지 못하고 옛 영수증만
흔든다).  대신: ① 재현 러너에서 `PTFE_STAMP` **필수 명시** ② `software default` ·
`analysis role` · `publication profile` 을 **별도 필드**로 ③ 로그 라벨을
`explicit exact-zero sensitivity protocol` 로 중립화 ④ 규약 변화는 **Table S3c 민감도**로.

---

# ⓐ 설명형 (Full — 독자가 이해하는 판)

**Microstructure reconstruction and transport simulation.**

Three-dimensional SBE and DBE microstructures were built in two stages and then used as the
geometry for a separate transport calculation, so that three distinct tools are involved: a
discrete element method (DEM) for the rigid-particle packing, a material point method (MPM)
for the plastic deformation of the electrolyte, and a finite-volume solver on a voxel grid for
the effective conductivities.

*Stage 1 — DEM packing.* Rigid-sphere packing was computed in LIGGGHTS using 1,271 NCM811
spheres (radius 2.5 μm) and 146,420 LPSCl spheres (radius 0.5 μm), sized after the experimental
powders and mixed at 70:27 by weight in a 50 × 50 μm² domain, compacted under displacement
control. Rigid-sphere contacts do reproduce particle rearrangement, but not the plastic
flattening, fracture and grain-boundary deformation that also densify sulfide powders, so the
contact stiffness of LPSCl was selected against a densification target for sulfide cold pressing
rather than taken from the dense material. **The 1.35 GPa value is an empirical contact-law
input, not an intrinsic LPSCl modulus and not an independent validation of the present SBE/DBE
beds**; the dense-material value (24 GPa) is listed beside it in Table S2. The ~10 % target is
derived from composite and glass literature rather than measured directly on pure LPSCl at
300 MPa, and the 11–12 % contact overlap is a pure-SE simulation consistency result rather than
a measured calibration target.

*Stage 2 — MPM compaction.* Plastic deformation was then resolved on the fixed DEM skeleton with
a GPU-accelerated MPM. VGCF fibres, PTFE fibrils and SDCP particles were **present in the
material-point cloud during this stage** at the experimental weight fractions, so their stiffness
enters the compaction rather than being added afterwards. The deviatoric plasticity follows a
J2 (von Mises) model with a yield strength of 0.30 GPa; the elastic pair E = 1.53 GPa and
ν = 0.49 is a **model choice** that sets K = 25.5 GPa and G = 0.51 GPa, confining the softening
to shear while leaving the bulk response at a dense-solid value. ⚠ The resulting beds are
**more compacted than the experimental porosity anchor**, so this parameterisation is not a
validation of the present SBE/DBE geometry.

*Stage 3 — voxel transport.* Each microstructure was rasterized onto a cubic grid with a voxel
edge of 0.15 μm. Adjacent conducting voxels were coupled through harmonic-mean conductances and
the potential field obtained from ∇·(σ∇φ) = 0, with 1 V applied between the separator (φ = 0)
and current-collector (φ = 1 V) faces and the remaining boundaries insulating; the effective
conductivity was taken from the total current. NCM811, VGCF and SDCP carried the electronic
network and LPSCl and SDCP the ionic network. The insulating binder was represented by
excluding its centerline voxels from conduction. Sensitivity of the reported conductivities to
this representation is given in Table S3c.

*Conductivity of the carbon network.* The coefficient assigned to the VGCF phase
(100 S cm⁻¹) is a **frozen, uncalibrated legacy voxel-network coefficient**, not a fibre
material constant and not a value derived from any measurement reported here. It was introduced
as an explicit order-of-magnitude placeholder, taken from the low end of a range cited at the
time as the literature band for graphitic fibre (10²–10³ S cm⁻¹); that band was subsequently
found to describe compacted powder rather than single filaments, VGCF-H having a single-filament
resistivity of 1 × 10⁻⁴ Ω cm (10⁴ S cm⁻¹). The coefficient therefore coincides with the powder
regime rather than having been selected against it, and it has not been recalibrated since. It
is retained so that the results presented in this work remain reproducible. Voxelisation fuses
touching fibres
into shared cells and therefore does not resolve fibre–fibre contact resistance, which is one of
several contributions separating single-filament (≈ 10⁴ S cm⁻¹) from compressed-powder
(≈ 83 S cm⁻¹) measurements of VGCF-H; packing fraction, orientation, network tortuosity,
contact number, compaction pressure and the measurement configuration also enter the powder
value. The coefficient is rescaled with voxel size so that the one-voxel-thick tube carries the
axial conductance of a 0.15 μm fibre, σ_eff = σ·πd²/(4h²), giving 78.5 S cm⁻¹ at h = 0.15 μm.
Because this coefficient was not independently calibrated, the conductivities and ratios below
are protocol responses under a stated closure rather than material-level estimates.

*Grid-origin ensemble and reported statistics.* Because the voxel grid samples the same
microstructure differently depending on where its origin falls, each electrode was solved at all
eight half-voxel origin shifts of a 2 × 2 × 2 factorial, the SBE and DBE sharing the same
origins so that ratios are formed pair by pair. **The eight phases are a complete factorial of a
single bed rather than independent replicates**, so ratios are reported as the mean over the
eight prescribed phases together with the spread across them and the observed range; no standard
error or confidence interval is implied. All arms reached the solver convergence criterion.

*Values.* Under the centerline convention **selected for reporting, but not calibrated**, the
effective electronic conductivity is 54.0 mS cm⁻¹ (SBE) and 70.6 mS cm⁻¹ (DBE), a paired ratio
of 1.308 (spread 0.003 across the eight origin phases; observed range 1.302–1.310). Omitting the
binder from the conduction grid instead gives 72.3 and 81.3 mS cm⁻¹, a ratio of **1.124**; the
two conventions differ only in whether the binder occupies conduction cells, and **neither is a
calibrated representation of it**, so the magnitude of the increase is convention-dependent while
its direction is not. Ohmic loss per phase was evaluated as Σ gₖ Δφₖ², summed over the
voxel-to-voxel connections belonging to that phase. Table S3c gives the two settings.

*Limitations.* The absolute conductivities have not been calibrated against a
composition-matched measurement and should be read as the output of an idealised bulk model:
the solver places no contact resistance at any interface — between active particles, between
active material and carbon, or at the current collector — so it does not reproduce the quantity
a two-terminal DC-polarisation measurement returns. The ratio is not grid-converged: refining
the voxel edge increases it monotonically without following a power law, so the reported gain is
larger at finer voxels **over the refinement interval examined**; neither a continuum
extrapolation nor a global bound is established. Explicitly restoring the additive contacts that
voxelisation drops recovers only about a fifth of that grid dependence — **measured under the
binder-omitted convention only**, and not transferable to the exact-zero convention. The
magnitude is also conditional on the carbon conductivity being treated as an effective network
constant: at the single-filament value, a hundredfold higher, the ordering reverses. That upper
arm is **not better physics** but a doubly idealised sensitivity at one origin phase, assuming
perfect fibre–fibre contact on top of equipotential fibres; a single scalar can absorb part of
the missing resistance numerically but is **not identified** as a fibre–fibre contact parameter.
Three further limits apply to the beds themselves. They are more compacted than the experimental
porosity anchor. **The compaction was not quasi-static**: the platen advanced at 0.27 of the
dilatational wave speed against an internal limit of 0.01, so the bed state carries a rate
contribution. Both electrodes were compacted at the same platen speed, which makes the inputs like-for-like
but **does not imply that the rate contribution cancels in the ratio** — equal driving speed is
not equal dynamic response for two different compositions. The reported ratio is therefore
**conditional on this high-rate compaction protocol**, and the absolute geometric quantities are
a terminal wall separation and a high-rate simulation-geometry diagnostic rather than
quasi-static converged values. Finally,
the specimen provenance of the SDCP conductivity (250 S cm⁻¹) is not established.

---

# ⓑ 압축형 (Compact — 지면 제약용)

**Microstructure reconstruction and transport simulation.** Three-dimensional SBE and DBE
microstructures were built with a discrete element method (DEM) for the rigid-particle packing
and a material point method (MPM) for the plastic deformation of the electrolyte, and the
effective conductivities were then obtained with a finite-volume solver on a voxel grid.
Rigid-sphere packing was computed in LIGGGHTS from 1,271 NCM811 spheres (r = 2.5 μm) and
146,420 LPSCl spheres (r = 0.5 μm), mixed 70:27 by weight in a 50 × 50 μm² domain and compacted
under displacement control. Rigid spheres do rearrange but cannot flatten, fracture or deform
grain boundaries, so the LPSCl contact stiffness was selected against a densification target for
sulfide cold pressing rather than taken from the dense material: **1.35 GPa is an empirical
contact-law input, not an intrinsic modulus and not a validation of these beds**, and 24 GPa is
listed alongside it in Table S2. The ~10 % target is derived from composite and glass literature
rather than measured on pure LPSCl, and the 11–12 % overlap is a pure-SE simulation result, not
a measured target. Plastic deformation was then resolved on the fixed DEM skeleton by MPM with
J2 plasticity (σ_y = 0.30 GPa); the elastic pair E = 1.53 GPa, ν = 0.49 is a model choice giving
K = 25.5 GPa and G = 0.51 GPa, confining the softening to shear. VGCF, PTFE and SDCP were
**present in the material-point cloud during compaction** at the experimental weight fractions.
The resulting beds are more compacted than the experimental porosity anchor.

Each microstructure was rasterized at a voxel edge of 0.15 μm; adjacent conducting voxels were
coupled through harmonic-mean conductances and ∇·(σ∇φ) = 0 solved with 1 V between the
separator and current-collector faces, the remaining boundaries insulating. NCM811, VGCF and
SDCP carried the electronic network and LPSCl and SDCP the ionic network. The insulating binder was
represented by excluding its centerline voxels from conduction; sensitivity to this
representation is given in Table S3c. The coefficient assigned to the VGCF phase
(100 S cm⁻¹) is a frozen, uncalibrated legacy value rather than a fibre constant. Voxelisation
fuses touching fibres and so carries no fibre–fibre contact resistance, one of several
contributions — along with packing fraction, orientation, network tortuosity, contact number
and compaction pressure — separating single-filament (≈ 10⁴ S cm⁻¹) from compressed-powder
(≈ 83 S cm⁻¹) measurements. The coefficient is rescaled with voxel size to preserve the axial
conductance of a 0.15 μm fibre (78.5 S cm⁻¹ at the 0.15 μm grid used here). Because it was not
independently calibrated, the conductivities and ratios reported are protocol responses under a
stated closure rather than material-level estimates.

Each electrode was solved at all eight half-voxel grid-origin shifts of a 2 × 2 × 2 factorial,
SBE and DBE sharing the same origins so that ratios are paired. These eight phases are a
complete factorial of a single bed rather than independent replicates, so ratios are given as
the mean over the prescribed phases with the spread and observed range; **no standard error and
no confidence interval** are implied. Ohmic loss per phase was evaluated as Σ g_k Δφ_k². Under the centerline convention selected for reporting but **not calibrated**, the effective
electronic conductivity is 54.0/70.6 mS cm⁻¹, a paired ratio of 1.308 (spread 0.003; range
1.302–1.310); omitting the binder instead gives 72.3/81.3 and a ratio of **1.124**. Neither
convention is a calibrated representation of the binder, so the magnitude is
convention-dependent while the direction is not. Absolute conductivities are those of
an idealised bulk model with no interfacial contact resistance anywhere and are not
composition-matched to a measurement. The ratio is not grid-converged and grew at finer voxels
**over the refinement interval examined**; no continuum extrapolation or global bound is
established. Restoring the additive contacts that voxelisation drops recovers about a fifth of
that dependence, **measured under the binder-omitted convention only**. The magnitude is also
conditional on the carbon conductivity being an effective network constant: at the
single-filament value the ordering reverses, but that arm is **not better physics** — it is a
doubly idealised sensitivity at one origin phase. Three further limits: the beds are more
compacted than the experimental porosity anchor; the compaction was **not quasi-static** (platen at 0.27 of the
dilatational wave speed against an internal limit of 0.01), and although both electrodes moved at
the same speed this makes the inputs like-for-like rather than making the rate contribution
cancel, so the ratio is **conditional on this protocol** and the thickness and ε_union are a
terminal wall separation and a high-rate diagnostic; and the specimen provenance of the SDCP conductivity
(250 S cm⁻¹) is not established.

---

# 부록 — SI Table S2 · S3 수정안

## Table S2 — 제목과 블록 분리

제목: ~~*Material parameters used for the DEM simulations*~~ →
***Material and numerical parameters used for the DEM–MPM–voxel transport workflow*.**

`Category` 열을 세 블록으로:

| 블록 | 들어가는 행 |
|---|---|
| **DEM (packing)** | 도메인 50 × 50 µm² · NCM811 r 2.5 / E 140 GPa · LPSCl r 0.5 / E(dense) 24 / **E(DEM contact) 1.35 `Calibrated`** |
| **MPM (plastic compaction)** | E 1.53 · ν 0.49 → **`Model choice`** (K 25.5 · G 0.51 을 만든다) · σ_y 0.30 → **`Selected against densification target`** |
| **Voxel transport** | Voxel edge 0.15 µm · σ_e(NCM) 1.0 × 10⁻² · σ_ion(LPSCl) 3.0 × 10⁻³ · **σ_e(VGCF) 1.0 × 10² → `Frozen, uncalibrated`** · **σ_e(SDCP) 250 → `Frozen, uncalibrated`** · PTFE 0 |

⚠ `E(dense) 24` 와 `E(DEM contact) 1.35` 는 **둘 다 남긴다** (전자가 물성, 후자가 규약).
⚠⚠ **VGCF 는 그 형식이 아니다** (2026-09-02 정정).  `78.5` 는 물성이 아니라 `100` 을 이
격자에 환산한 **격자 산물**이라 재료 파라미터 표에 값으로 있을 자리가 없다 — 세 격자에서
78.5 / 113.1 / 133.6 을 썼으므로 하나만 실으면 나머지 계산이 다른 물질처럼 보이고, 다른
해상도로 재현하려는 독자가 그 값을 그대로 넣으면 틀린다.  ⇒ 표에는 `100` 한 줄, 환산은
Methods 의 **식**으로 (`σ_eff = σ·πd²/(4h²)`).
⚠⚠ **`powder` 라벨을 쓰지 않는다** — 그것은 `100` 이 83 에서 유도됐다는 뜻으로 읽히는데
**거짓**이다 (도입 커밋이 83 감사보다 앞서고 스스로 order-of-magnitude hook 이라 적었다).
⚠⚠ **SDCP 250 도 같은 등급이다** — 출처가 리포에 없다 (SELF-13).  옛 서술이 *"SDCP 는
재료 앵커, VGCF 는 유효 망 상수"* 라는 **범주 비대칭**을 말했는데, 그것은 SDCP 를 실제보다
잘 근거된 것처럼 보이게 한다.  둘 다 미보정으로 같이 라벨한다.
⚠⚠ **`Calibrated` 한 라벨로 뭉치지 않는다** (R10 재판정): `E(DEM contact) 1.35` 는
**`Empirical contact-law input`**, MPM 의 `E, ν` 는 **`Model choice`**, `σ_y` 는
**`Selected against densification target`**.  세 역할이 다르다.

## Table S3 — σ_ele 만 갱신, 나머지는 미완 (⚠ 투고용 아님)

★ **수치 정본은 `docs/reviews/table_s3_data_20260827.md`** 다 — σ_e 두 규약은 §2·§3,
**구조 지표·접촉 수·면적 하중은 §10** (2026-08-29 등재).  아래 표는 그 인용이고,
값이 갈리면 **원장이 이긴다**.

| Parameter | SBE | DBE | Unit |
|---|---|---|---|
| Thickness | 72.53 | 72.53 | µm |
| ε_union (simulation-geometry diagnostic) | 7.86 | 7.37 | % |
| σ_ele,eff | **54.0** | **70.6** | mS cm⁻¹ |
| σ_ele ratio, DBE/SBE (paired over 8 grid-origin phases) | SPAN **1.308** (spread 0.003; range 1.302–1.310) | | — |
| σ_ion,eff | *not evaluated in this cohort* | *not evaluated in this cohort* | mS cm⁻¹ |
| SE coverage of AM (Tabor band) | **86.6** | **86.6** | % |
| VGCF coverage of AM | **13.1** | **15.5** | % |
| Electronic connectivity | **100** | **100** | % |
| Areal capacity | **[비용량 확인 필요 — §아래]** | **동일** | mAh cm⁻² |
| Median conductive-additive contacts per AM (VGCF + SDCP) | **74** | **86** | ea |
| ⌐ including the binder (VGCF + SDCP + PTFE) | 80 | 88 | ea |

**⚠ Areal capacity — SI v6 의 `3.11 / 3.07` 은 이 침대에서 성립하지 않는다.**
두 전극은 **같은 AM scaffold** 를 쓰고(`n_AM = 1271`, `seed_AM_frac_pct = 45.68` 동일) 정지
두께도 같다(`72.534 µm`).  ⇒ 면적 용량이 **서로 다를 수 없다.**
우리 기하가 주는 면적 하중은 두 전극 모두

  `0.4568 × 72.534 µm × 4.8 g cm⁻³ = 0.015904 g cm⁻²`

이고, 여기에 곱할 **비용량이 원고에 적혀 있지 않다.**  SI 의 3.11 을 재현하는 값은
**195.5 mAh g⁻¹**, 3.07 은 193.0 이다 — 즉 v6 의 두 값은 **같은 침대에 서로 다른 비용량을
곱한 것처럼** 보인다.  ⇒ 협업자에게 *"어느 비용량을 썼는가"* 를 확인한 뒤 채운다.
**추정해서 적지 않는다** (§F1).

**⚠ 접촉 수는 규약 의존이고, 그 규약이 이득까지 바꾼다.**
정의: AM 구 **표면 바깥** 0.15 µm(= σ_e 격자 한 복셀) 껍질 안에 있는 첨가제 물질점이 속한
**서로 다른 개체의 수** — 점 수가 아니다 (굵은 섬유 하나는 접촉 1).  경계는 침대 규약대로
`periodic_xy + z_open`.  접촉이 0 인 AM 은 **양 침대 모두 0/1271** 이다.
- 전도성만(VGCF+SDCP): 74 → 86 = **+16.2 %**
- 절연 바인더 포함: 80 → 88 = **+10.0 %**
⇒ PTFE 를 *"conductive binder domain"* 에 넣느냐가 **이득을 16.2 % ↔ 10.0 % 로 바꾼다.**
본문이 이 수를 기전 근거로 쓰므로 **규약을 함께 적지 않으면 인용할 수 없다.**
⚠ **SI v6 의 `433 → 517` 은 재현되지 않는다** (절대값 5.8배 차).  v6 이 무엇을 셌는지
(점 수 / 개체 수 · band 폭 · 격자 세대) 기록이 없다.  **방향과 상대 크기는 정합적**이다
(+16.2 % vs +19.4 %) — 즉 *"SDCP 가 AM 당 접촉을 늘린다"* 는 본문 주장은 유지되고,
**절대 수치만** 규약과 함께 갱신된다.
★ 좌표 프레임 검증(접촉과 무관): AM 구 깊은 안쪽(d < 0.8 r) 첨가제 밀도 **0.0006–0.0017**
(bulk = 1), 표면 바로 밖 **1.41** ⇒ 배제가 실재하고 사상이 맞다.

**⚠ coverage 세 행의 규약**: `SE coverage of AM` 은 **Tabor 밴드**(0.26 µm) 값이다 —
v6 의 86.7 이 이 규약이며 새 침대가 86.6 으로 재현했다.  같은 침대의 다른 규약 값도 함께
산출된다 (Hertz 밴드 65.7 · 복셀 인접 40.4) — **셋은 서로 다른 양이므로 섞어 인용하지 않는다.**
`VGCF coverage of AM` 은 첨가제 인접 복셀 규약(`coverage_AM_S_add_pct`)이다.
⚠ `AM_P` 계열은 전부 0 이다 — 이 침대의 NCM811 이 **단일 크기**라 큰 AM 개체군이 없다.

⚠ **두 규약을 같은 서식으로 적는다** — 굵은 글씨·`reported`·`resolved` 금지 (R10 재판정 1).
⚠ **`σ_ion` 은 이 cohort(§2·§3) 에서 평가하지 않았다** (`LEAN=2` 가 이온을 안 푼다).  옛 값을
재사용하지 않는다.  나머지 다섯 행은 **각각** 상태를 적는다 (한 행에 합치지 않는다).
⚠⚠ **별도로 돌린 이온 cohort 도 이 표에 못 넣는다** (원장 §6-1, 2026-08-29).  돌긴 돌았고
비가 **1 보다 작게** 나왔는데, 그것이 물리가 아니라 **입력 규약의 비대칭**이다: SBE 의
바인더 1 wt% 가 전도 격자에 **한 셀도 없고**(`ptfe_cells_observed = 0`) DBE 에서만 SDCP 가
실재하면서 자기 자리의 전해질을 σ 가 1/3 인 상으로 바꾼다.  ⇒ 채우면
*"SDCP 가 이온 전도를 떨어뜨린다"* 를 싣는 셈인데 그것은 **모델이 바인더를 안 그린 결과**다.
~~해제는 런 완주가 아니라 **D13 펠릿 보정**이 `σ_ion(SDCP)` 와 `ptfe_block_um` 을 앵커한
뒤다.~~  그때까지 이 행은 비워 둔다 (§F1).

⚠⚠ **정정 2026-08-30 (Codex R13 C-7) — D13 만으로는 안 열린다.**  위 문장은 D13 펠릿
보정을 **충분조건**처럼 적었는데 세 겹으로 성립하지 않는다:
1. 펠릿이 낸 `σ_ion(SDCP)* = 0.62e-3` 은 **그 RVE 규약 안에서만** 유효하다 — 동결 문서
   자신이 *"상수로 이식 금지"* 라고 못 박았다 (`pellet_calib_freeze_20260825.md` §3,
   그 RVE 가 Bruggeman 대비 −9.95 % 초과희석이라 σ_i 가 되메꾼다).
2. **D13 의 전극 holdout 이 PTFE-only** 다 (`d13_pellet_calibration_prereg_20260829.md`).
   그래서 `ptfe_block_um` 의 전이는 시험할 수 있어도 **SDCP 를 포함한 전극에서
   `σ_ion(SDCP)` 를 재식별하거나 이식을 검증하지 못한다.**
3. 상대비도 그대로 안 옮겨간다 — 동결값은 `0.62/3.57 = 0.1737` 인데, 생산 SE 를 `0.003`
   에 두고 SDCP 만 `0.00062` 로 바꾸면 `0.2067` 이다.  같은 상대비를 지키려면 먼저
   `0.000521` 이어야 한다.  (물론 그 전에 1번의 이식 금지가 걸린다.)
⚠ 배선도 아직 없다 — 8팔 러너의 `P2_EXTRA` 허용목록이 수치 전용이라
`--sigma-ion-sdcp` 는 **exit 2** 다.  두 이온 σ 를 정식 축으로 올려야 한다.

⇒ **해제 조건 (갱신)**: ⓐ **SDCP 포함 전극 표적**을 D13 에 추가하거나 전극 규약 안에서
재캘리브, ⓑ `σ_ion(SE)` 와 `σ_ion(SDCP)` **두 입력을 함께 봉인**, ⓒ 그 축을 러너 노브로
승격.  셋이 서기 전까지 이 행은 계속 공백이다.

**`ε_union` · thickness 연산 정의** (R10 재판정 6):
- `ε_union = 1 − V_solid / (A · (z_plate − z_floor))` — 분자는 **겹침을 한 번만 세는 합집합
  부피**, 분모는 바닥판과 플래튼 사이의 상자 부피.  통상적인 전극 porosity 가 **아니다**.
- `Thickness` = **terminal wall separation under the kinematic stopping rule** — 플래튼이
  멈춘 위치로 정해지는 값이지 응력 평형에서 창발한 두께가 아니다.
- ⚠ 두 침대의 thickness 가 **같다는 것이 과압축이 비에서 상쇄된다는 뜻이 아니다.**
  같은 속도·같은 정지 위치는 **like-for-like 입력**을 보장할 뿐이다.
- 실험 앵커(~15.6 %) 대비 **과압축**이다.

## Table S3c (신설) — 모델-형식 민감도

⚠ **형식 근거**: 같은 재료계·같은 코드(LIGGGHTS)의 Bazzoun 2025 (Electrochim. Acta,
`litdb: bazzoun2025_dem_parameter_sensitivity_assb_cathode`) 가 파라미터 8개 × 1920 케이스
OAT 민감도를 **별도 절**에 싣고 본문은 공칭값 하나를 쓴다.  우리 litdb 65장에 *"두 규약을
동등하게 병기"* 하는 선례는 **없다**.  ⇒ 본문은 공칭 규약 값 하나, 민감도는 이 표.

| Varied | Setting | σ_ele SBE | σ_ele DBE | ratio |
|---|---|---|---|---|
| Binder representation | centerline voxels excluded (**as reported**) | 54.0 | 70.6 | **1.308** |
| | omitted from the electronic grid | 72.3 | 81.3 | 1.124 |

각주: *Both settings were evaluated on the same beds with the same code and grid, differing only
in whether the insulating binder occupies conduction cells; a machine-checked contract confirms
that no other parameter differs. The reported setting stamps a one-voxel centerline through each
binder fibril and removes those cells from conduction, which accounts for 43 % of the binder
volume present in the bed; omitting the binder accounts for none of it. The increase from SBE to
DBE is obtained under both settings. The binder's mass and stiffness are present in the DEM–MPM
bed under either, since the setting affects only the conduction grid.*

---

# ⚠ 본문에서 함께 고쳐야 할 곳

| 자리 | 현재 | 고침 |
|---|---|---|
| §전송 문단 | *"σ_ele increases from 1.98 to 3.00 S cm⁻¹"* | *"the simulated effective σ_ele increases from **54.0 to 70.6 mS cm⁻¹** (a ratio of 1.308)"*.  민감도는 **Table S3c** 로 (본문에 규약 논쟁을 넣지 않는다) |
| 같은 문단 | *"σ_ion … 0.203 and 0.215 mS cm⁻¹"* | ⚠ **재측정 전까지 보류** |
| 같은 문단 | *"reconstructed using a discrete element method (DEM)"* | *"**generated** by DEM packing and MPM compaction"* — ⚠ `reconstructed` 는 tomography 재구성을 암시한다 |
| **Figure 4a 캡션** | *"**DEM**-reconstructed SBE and DBE geometries"* | *"SBE and DBE composite-cathode geometries **generated by DEM particle packing and compacted by MPM**"*.  두 군데다 — ⓐ `reconstructed` 는 실물 **토모그래피 재구성**을 암시하는데 우리는 생성했다 ⓑ `DEM` 은 세 도구 중 하나만 부른다 |
| **Figure 4a 그림** | 출처 미상 | ⚠ **재렌더 권장** — 침대가 2026-08-27 에 재압밀됐다 (첨가제 탄성계수 세대 교체).  벌크 지표는 거의 안 움직였으나(두께 72.48 → 72.53 µm) **입자 위치는 바뀌었다** ⇒ 지금 그림이 옛 침대면 Table S3 이 보고하는 것과 **다른 미세구조**다.  ⛔ 다만 **v6 Fig 4a 의 생성 경로를 우리가 모른다** — 스타일을 맞출 수 없으므로 **후보를 내고 협업자가 판단**한다 |
| Figure 4b | 옛 σ 값 그림 | **재작도 필요** (두 규약 병기) |
| Table S3 제목 | *"…from the DEM simulations"* | *"Structural metrics from the DEM–MPM geometry and transport metrics from the voxel finite-volume solver"* |
| Figure S16 설명 | *"**Reconstructed** SBE and DBE geometries used for the **DEM** simulations"* | *"SBE and DBE geometries **generated by DEM packing and MPM compaction**"* — 두 군데다 (`Reconstructed` + 전 과정을 DEM 으로 부름) |
| Figure S17·S18 설명 | *"Simulated ionic / electronic current-density distributions in the SBE and DBE"* | ✅ **DEM 오귀속 없음.**  다만 솔버가 무명이라 *"…computed with the voxel finite-volume solver"* 를 붙이는 것이 낫다 (선택) |
| §전송 문단 첫 문장 | 옛 세대 값 | 위 행으로 교체.  ⚠ **자릿수가 바뀐다** (S cm⁻¹ → mS cm⁻¹) |

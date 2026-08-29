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
| 4 | PTFE 규약·σ_VGCF 규약 암묵 | **둘 다 명시**, PTFE 는 두 규약 병기 | 이득이 규약에 크게 의존한다 (12.4 ↔ 30.8 %) |

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

⇒ **두 규약은 동등한 model-form sensitivity 두 점**이다 (R8 Q2 와 동일).  굵은 글씨 ·
`reported` · `resolved` 를 **전부 제거**한다.  라벨은 이렇게 쓴다:

| 규약 라벨 | σ_ele SBE | DBE | 비 |
|---|---|---|---|
| `PTFE omitted from the electronic grid (legacy/default convention)` | 72.3 | 81.3 mS cm⁻¹ | 1.124 |
| `PTFE centerline voxels excluded (exact-zero sensitivity convention)` | 54.0 | 70.6 | 1.308 |

**코드 기본값은 옮기지 않는다** (R10 Q2 — 사후 primary 를 정당화하지 못하고 옛 영수증만
흔든다).  대신: ① 재현 러너에서 `PTFE_STAMP` **필수 명시** ② `software default` ·
`analysis role` · `publication profile` 을 **별도 필드**로 ③ 로그 라벨을
`explicit exact-zero sensitivity protocol` 로 중립화 ④ 두 규약 **동등 보고**.

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
network and LPSCl and SDCP the ionic network. The insulating binder was treated under **two
conventions, reported as equivalent sensitivity points rather than one primary result**: omitted
from the electronic grid, and with its centerline voxels excluded from conduction. Neither is
established as closer to a real thin coating — the one-cell centerline under-represents the
coating's spatial extent while over-blocking where it is stamped, and the diameter-aware variant
is not implemented. Note that omitting the binder from the conduction grid does not remove it
from the model: its mass and stiffness are present in the DEM–MPM bed, and only its direct
insulating exclusion on the electronic grid is absent.

*Conductivity of the carbon network.* The conductivity assigned to VGCF is an **effective
network value, not a fibre material constant**. Voxelisation fuses touching fibres into shared
cells and therefore removes the fibre–fibre contact resistance that dominates a real carbon
network — the two orders of magnitude between the compressed-powder (≈ 83 S cm⁻¹) and
single-filament (≈ 10⁴ S cm⁻¹) values of VGCF-H is essentially that contact resistance. The
powder-scale value (100 S cm⁻¹) was therefore adopted and rescaled to the voxel grid so that the
axial conductance of a fibre is preserved (78.5 S cm⁻¹ at 0.15 μm).

*Grid-origin ensemble and reported statistics.* Because the voxel grid samples the same
microstructure differently depending on where its origin falls, each electrode was solved at all
eight half-voxel origin shifts of a 2 × 2 × 2 factorial, the SBE and DBE sharing the same
origins so that ratios are formed pair by pair. **The eight phases are a complete factorial of a
single bed rather than independent replicates**, so ratios are reported as the mean over the
eight prescribed phases together with the spread across them and the observed range; no standard
error or confidence interval is implied. All arms reached the solver convergence criterion.

*Values under the two binder conventions.* With PTFE centerline voxels excluded (exact-zero
sensitivity convention) the effective electronic conductivity is 54.0 mS cm⁻¹
(SBE) and 70.6 mS cm⁻¹ (DBE), a paired ratio of 1.308 (spread 0.003 across the eight origin
phases; observed range 1.302–1.310). Leaving PTFE unresolved gives 72.3 and 81.3 mS cm⁻¹, a
ratio of 1.124 (spread 0.003; range 1.120–1.127). The two differ only in whether the binder's
centerline voxels are excluded from conduction — a machine-checked contract confirms that no
other parameter differs — and **neither is established as closer to a real thin coating**: the
one-cell centerline under-represents the coating's spatial extent while over-blocking where it
is stamped. Measured against the binder volume actually present in the bed, the two conventions
represent **0 %** and **43 %** of it respectively (327,093 and 161,407 stamped voxels for the SBE
and DBE against true binder volumes of 2,581 and 1,290 μm³ — a consistent 2.4-fold
under-representation, the two electrodes agreeing to within 1.3 %); neither reproduces the real
volume, and which of the two errs less for conduction is not determined by volume alone, since
blocking follows connected topology rather than volume. They are therefore reported as **two
equivalent model-form sensitivity points**; the direction of the change is common to both, its
magnitude is not. Ohmic loss per phase was evaluated as Σ g_k Δφ_k², summed over the
voxel-to-voxel connections belonging to that phase.

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
contribution. Both electrodes were compacted at the same platen speed, so that contribution is
common to them and the ratio is unaffected, but the **absolute** geometric quantities (thickness,
ε_union) would require a slower re-compaction before being quoted as converged values. Finally,
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
SDCP carried the electronic network and LPSCl and SDCP the ionic network. The insulating binder
was treated under two conventions reported as equivalent sensitivity points — omitted from the
electronic grid, and with its centerline voxels excluded — since neither is established as closer
to a real thin coating: the one-cell centerline under-represents the coating's extent while
over-blocking where stamped, and omitting it removes only the electronic exclusion, the binder's
mass and stiffness remaining in the bed. The VGCF conductivity is an effective network
value rather than a fibre constant, since voxelisation removes the fibre–fibre contact
resistance that separates the powder (≈ 83 S cm⁻¹) and single-filament (≈ 10⁴ S cm⁻¹) values;
the powder-scale value was adopted and rescaled to preserve axial fibre conductance
(78.5 S cm⁻¹).

Each electrode was solved at all eight half-voxel grid-origin shifts of a 2 × 2 × 2 factorial,
SBE and DBE sharing the same origins so that ratios are paired. These eight phases are a
complete factorial of a single bed rather than independent replicates, so ratios are given as
the mean over the prescribed phases with the spread and observed range; **no standard error and
no confidence interval** are implied. Ohmic loss per phase was evaluated as Σ g_k Δφ_k². The two
binder conventions give 72.3/81.3 mS cm⁻¹ (ratio 1.124) and 54.0/70.6 mS cm⁻¹ (ratio 1.308):
**the direction is common to both, the magnitude is not.** Absolute conductivities are those of
an idealised bulk model with no interfacial contact resistance anywhere and are not
composition-matched to a measurement. The ratio is not grid-converged and grew at finer voxels
**over the refinement interval examined**; no continuum extrapolation or global bound is
established. Restoring the additive contacts that voxelisation drops recovers about a fifth of
that dependence, **measured under the binder-omitted convention only**. The magnitude is also
conditional on the carbon conductivity being an effective network constant: at the
single-filament value the ordering reverses, but that arm is **not better physics** — it is a
doubly idealised sensitivity at one origin phase. Three further limits: the beds are more
compacted than the experimental porosity anchor; the compaction was **not quasi-static** (platen
at 0.27 of the dilatational wave speed against an internal limit of 0.01), which is common to
both electrodes and so cancels in the ratio but leaves the **absolute** thickness and ε_union
requiring a slower re-compaction; and the specimen provenance of the SDCP conductivity
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
| **Voxel transport** | Voxel edge 0.15 µm · σ_e(NCM) 1.0 × 10⁻² · σ_ion(LPSCl) 3.0 × 10⁻³ · **σ_e(VGCF, powder) 1.0 × 10²** · **σ_e(VGCF, voxel diameter-preserving) 78.5** · σ_e(SDCP) 250 · PTFE 0 |

⚠ `E(dense) 24` 와 `E(DEM contact) 1.35` 를 **둘 다 남긴다.**  VGCF 두 행(powder / voxel)도
그대로 — 규약이 표에서 보여야 한다.
⚠⚠ **`Calibrated` 한 라벨로 뭉치지 않는다** (R10 재판정): `E(DEM contact) 1.35` 는
**`Empirical contact-law input`**, MPM 의 `E, ν` 는 **`Model choice`**, `σ_y` 는
**`Selected against densification target`**.  세 역할이 다르다.

## Table S3 — σ_ele 만 갱신, 나머지는 미완 (⚠ 투고용 아님)

| Parameter | SBE | DBE | Unit |
|---|---|---|---|
| Thickness | 72.53 | 72.53 | µm |
| ε_union (simulation-geometry diagnostic) | 7.86 | 7.37 | % |
| σ_ele,eff — `PTFE omitted from the electronic grid (legacy/default convention)` | 72.3 | 81.3 | mS cm⁻¹ |
| σ_ele,eff — `PTFE centerline voxels excluded (exact-zero sensitivity convention)` | 54.0 | 70.6 | mS cm⁻¹ |
| σ_ele ratio (paired, 8 origin phases) — omitted / centerline-excluded | 1.124 | 1.308 | — |
| ⌐ spread / range | 0.003 / 1.120–1.127 | 0.003 / 1.302–1.310 | — |
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
⚠ **`σ_ion` 은 이번 cohort 에서 평가하지 않았다** (`LEAN=2` 가 이온을 안 푼다).  옛 값을
재사용하지 않는다.  나머지 다섯 행은 **각각** 상태를 적는다 (한 행에 합치지 않는다).

**`ε_union` · thickness 연산 정의** (R10 재판정 6):
- `ε_union = 1 − V_solid / (A · (z_plate − z_floor))` — 분자는 **겹침을 한 번만 세는 합집합
  부피**, 분모는 바닥판과 플래튼 사이의 상자 부피.  통상적인 전극 porosity 가 **아니다**.
- `Thickness` = **terminal wall separation under the kinematic stopping rule** — 플래튼이
  멈춘 위치로 정해지는 값이지 응력 평형에서 창발한 두께가 아니다.
- ⚠ 두 침대의 thickness 가 **같다는 것이 과압축이 비에서 상쇄된다는 뜻이 아니다.**
  같은 속도·같은 정지 위치는 **like-for-like 입력**을 보장할 뿐이다.
- 실험 앵커(~15.6 %) 대비 **과압축**이다.

## Table S3b (신설) — PTFE 표현 민감도

| PTFE convention | σ_ele SBE | σ_ele DBE | ratio | spread | range |
|---|---|---|---|---|---|
| PTFE omitted from the electronic grid (legacy/default convention) | 72.3 | 81.3 | 1.124 | 0.003 | 1.120–1.127 |
| PTFE centerline voxels excluded (exact-zero sensitivity convention) | 54.0 | 70.6 | 1.308 | 0.003 | 1.302–1.310 |

각주: *Both conventions were evaluated on the same beds with the same code and grid, differing
only in whether the insulating binder occupies conduction cells; a machine-checked contract
confirms that no other parameter differs. Neither convention is designated primary: the
one-cell centerline under-represents the spatial extent of a thin coating while over-blocking
the cells it occupies, and the diameter-aware variant is not implemented, so neither is
established as closer to the real film. Omitting the binder from the conduction grid removes
only its electronic exclusion; its mass and stiffness remain in the DEM–MPM bed. The direction
of the change is common to both conventions, its magnitude is not.*

---

# ⚠ 본문에서 함께 고쳐야 할 곳

| 자리 | 현재 | 고침 |
|---|---|---|
| §전송 문단 | *"σ_ele increases from 1.98 to 3.00 S cm⁻¹"* | **두 규약을 동등하게** — *"72.3 → 81.3 mS cm⁻¹ (ratio 1.124) with the binder omitted from the electronic grid, and 54.0 → 70.6 (1.308) with its centerline voxels excluded"*.  ⚠ **어느 쪽도 먼저 headline 으로 주지 않는다** |
| 같은 문단 | *"σ_ion … 0.203 and 0.215 mS cm⁻¹"* | ⚠ **재측정 전까지 보류** |
| 같은 문단 | *"reconstructed using a discrete element method (DEM)"* | *"**generated** by DEM packing and MPM compaction"* — ⚠ `reconstructed` 는 tomography 재구성을 암시한다 |
| Figure 4a 설명 | *"DEM-reconstructed …"* | *"DEM-packed and MPM-compacted …"* |
| Figure 4b | 옛 σ 값 그림 | **재작도 필요** (두 규약 병기) |
| Table S3 제목 | *"…from the DEM simulations"* | *"Structural metrics from the DEM–MPM geometry and transport metrics from the voxel finite-volume solver"* |
| Figure S16 설명 | *"**Reconstructed** SBE and DBE geometries used for the **DEM** simulations"* | *"SBE and DBE geometries **generated by DEM packing and MPM compaction**"* — 두 군데다 (`Reconstructed` + 전 과정을 DEM 으로 부름) |
| Figure S17·S18 설명 | *"Simulated ionic / electronic current-density distributions in the SBE and DBE"* | ✅ **DEM 오귀속 없음.**  다만 솔버가 무명이라 *"…computed with the voxel finite-volume solver"* 를 붙이는 것이 낫다 (선택) |
| §전송 문단 첫 문장 | 한쪽 규약만 | **두 값을 한 문장 또는 병렬 표로 동등하게** |

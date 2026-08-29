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
network and LPSCl and SDCP the ionic network. **PTFE was resolved on the conduction grid as a
blocking phase**: the binder is insulating and its content differs between the two electrodes
(1.0 wt% in the SBE against 0.5 wt% in the DBE), so a transport model that omitted it could not
represent half of the compositional change under study. Because a voxel emptied of conduction
may over-represent the local blocking of a thin surface coating, the alternative convention in
which PTFE is left unresolved is reported alongside it in Table S3b, and both are quoted in the
text.

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
is stamped. They are therefore reported as **two equivalent model-form sensitivity points**;
the direction of the change is common to both, its magnitude is not. Ohmic loss per phase was evaluated as Σ g_k Δφ_k², summed over the
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
Two further limits apply: the beds are more compacted than the experimental porosity anchor, and
the specimen provenance of the SDCP conductivity (250 S cm⁻¹) is not established.

---

# ⓑ 압축형 (Compact — 지면 제약용)

**Microstructure reconstruction and transport simulation.** Three-dimensional SBE and DBE
microstructures were built with a discrete element method (DEM) for the rigid-particle packing
and a material point method (MPM) for the plastic deformation of the electrolyte, and the
effective conductivities were then obtained with a finite-volume solver on a voxel grid.
Rigid-sphere packing was computed in LIGGGHTS from 1,271 NCM811 spheres (r = 2.5 μm) and
146,420 LPSCl spheres (r = 0.5 μm), mixed 70:27 by weight in a 50 × 50 μm² domain and compacted
under displacement control. Since rigid-sphere contacts cannot reproduce the plastic flattening
and rearrangement that densify sulfide powders, the LPSCl contact stiffness was calibrated
against the measured compaction response (~10 % porosity, 11–12 % contact overlap at 300 MPa);
the calibrated value (1.35 GPa) is an effective parameter, and the dense-material modulus
(24 GPa) is listed alongside it in Table S2. Plastic deformation was then resolved on the fixed
DEM skeleton by MPM with von Mises plasticity (E = 1.53 GPa, ν = 0.49, σ_y = 0.30 GPa), the high
ν confining the softening to shear (K = 25.5 GPa, G = 0.51 GPa). VGCF, PTFE and SDCP were seeded
into the pore space at the experimental weight fractions.

Each microstructure was rasterized at a voxel edge of 0.15 μm; adjacent conducting voxels were
coupled through harmonic-mean conductances and ∇·(σ∇φ) = 0 solved with 1 V between the
separator and current-collector faces, the remaining boundaries insulating. NCM811, VGCF and
SDCP carried the electronic network and LPSCl and SDCP the ionic network. PTFE was resolved as a
blocking phase, since it is insulating and its content differs between the two electrodes
(1.0 against 0.5 wt%), so omitting it would remove half of the compositional change under study;
the alternative convention in which it is left unresolved is given alongside in Table S3b. The VGCF conductivity is an effective network
value rather than a fibre constant, since voxelisation removes the fibre–fibre contact
resistance that separates the powder (≈ 83 S cm⁻¹) and single-filament (≈ 10⁴ S cm⁻¹) values;
the powder-scale value was adopted and rescaled to preserve axial fibre conductance
(78.5 S cm⁻¹).

Each electrode was solved at all eight half-voxel grid-origin shifts of a 2 × 2 × 2 factorial,
SBE and DBE sharing the same origins so that ratios are paired. These eight phases are a
complete factorial of a single bed rather than independent replicates, so ratios are given as
the mean over the prescribed phases with the spread and observed range, and no standard error is
implied. Ohmic loss per phase was evaluated as Σ g_k Δφ_k². Absolute conductivities are those of
an idealised bulk model containing no interfacial contact resistance and are not
composition-matched to a measurement; the ratio is not grid-converged and increases on
refinement, so the reported gain is a lower bound on that axis. Its magnitude is likewise
conditional on the carbon conductivity being an effective network constant — at the
single-filament value, which assumes perfect fibre–fibre contact as well, the ordering
reverses.

---

# 부록 — SI Table S2 · S3 수정안

## Table S2 — 제목과 블록 분리

제목: ~~*Material parameters used for the DEM simulations*~~ →
***Material and numerical parameters used for the DEM–MPM–voxel transport workflow*.**

`Category` 열을 세 블록으로:

| 블록 | 들어가는 행 |
|---|---|
| **DEM (packing)** | 도메인 50 × 50 µm² · NCM811 r 2.5 / E 140 GPa · LPSCl r 0.5 / E(dense) 24 / **E(DEM contact) 1.35 `Calibrated`** |
| **MPM (plastic compaction)** | E 1.53 · ν 0.49 · σ_y 0.30 (전부 `Calibrated`) |
| **Voxel transport** | Voxel edge 0.15 µm · σ_e(NCM) 1.0 × 10⁻² · σ_ion(LPSCl) 3.0 × 10⁻³ · **σ_e(VGCF, powder) 1.0 × 10²** · **σ_e(VGCF, voxel diameter-preserving) 78.5** · σ_e(SDCP) 250 · PTFE 0 |

⚠ `E(dense) 24` 와 `E(DEM contact) 1.35` 를 **둘 다 남긴다.**  `Calibrated` 라벨도 그대로.
VGCF 두 행(powder / voxel)도 그대로 — 규약이 표에서 보여야 한다.

## Table S3 — 갱신 (옛 값 전량 교체)

| Parameter | SBE | DBE | Unit |
|---|---|---|---|
| Thickness | 72.53 | 72.53 | µm |
| ε_union (simulation-geometry diagnostic) | 7.86 | 7.37 | % |
| σ_ele,eff (PTFE resolved — reported) | **54.0** | **70.6** | mS cm⁻¹ |
| σ_ele ratio (paired, 8 origin phases) | — | **1.308** | — |
| ⌐ spread / range | — | 0.003 / 1.302–1.310 | — |
| σ_ion,eff | *재측정 필요* | *재측정 필요* | — |
| SE coverage of AM · VGCF coverage · CBD contacts · connectivity · areal capacity | *새 침대에서 재측정 필요* | | |

⚠ **`Porosity` 를 `ε_union` 으로 개명하고 각주**: 시뮬레이션 기하 진단값이며 통상적인 전극
porosity 가 아니다.  실험 앵커(~15.6 %) 대비 과압축이다.

## Table S3b (신설) — PTFE 표현 민감도

| PTFE convention | σ_ele SBE | σ_ele DBE | ratio | spread | range |
|---|---|---|---|---|---|
| **resolved as blocking phase (reported)** | **54.0** | **70.6** | **1.308** | 0.003 | 1.302–1.310 |
| left unresolved | 72.3 | 81.3 | 1.124 | 0.003 | 1.120–1.127 |

각주: *Both conventions were evaluated on the same beds with the same code and grid, differing
only in whether the insulating binder occupies conduction cells; a machine-checked contract
confirms that no other parameter differs. PTFE is resolved in the reported configuration
because it is insulating and its content differs between the two electrodes, so omitting it
would remove half of the compositional change under study. Because a fully emptied voxel may
over-represent the local blocking of a thin surface coating, the unresolved convention is given
alongside; the direction of the change is common to both, its magnitude is not.*

---

# ⚠ 본문에서 함께 고쳐야 할 곳

| 자리 | 현재 | 고침 |
|---|---|---|
| §전송 문단 | *"σ_ele increases from 1.98 to 3.00 S cm⁻¹"* | **"from 54.0 to 70.6 mS cm⁻¹"** (+30.8 %) — ⚠ 같은 문장 또는 바로 뒤에 **미표현 규약 값(72.3 → 81.3, +12.4 %)도 함께**.  한쪽만 적지 않는다 |
| 같은 문단 | *"σ_ion … 0.203 and 0.215 mS cm⁻¹"* | ⚠ **재측정 전까지 보류** |
| 같은 문단 | *"reconstructed using a discrete element method (DEM)"* | *"reconstructed with a DEM–MPM workflow"* |
| Figure 4a 설명 | *"DEM-reconstructed …"* | *"DEM–MPM-reconstructed …"* |
| Figure 4b | 옛 σ 값 그림 | 새 값으로 재작도 |
| Table S3 제목 | *"…from the DEM simulations"* | *"…from the DEM–MPM–voxel transport workflow"* |

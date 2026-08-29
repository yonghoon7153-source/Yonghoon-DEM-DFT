# Methods — 시뮬레이션 절 개정안 v7 (2026-08-29)

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

⚠ **주 규약 = PTFE 미표현** (v6 Methods 가 이미 *"PTFE was not resolved"* 라고 적는다).
차단 규약은 **SI 민감도**로 싣는다.

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
control. Because rigid-sphere contacts cannot reproduce the plastic flattening, particle
rearrangement and grain-boundary sliding that densify sulfide powders, **the contact stiffness
of LPSCl was calibrated against the measured compaction response** — the ~10 % porosity and
11–12 % contact overlap reported for cold-pressed LPSCl at 300 MPa. The calibrated contact
modulus (1.35 GPa) is therefore an effective parameter that stands in for those unresolved
mechanisms; the dense-material modulus (24 GPa) is retained in Table S2 for reference.

*Stage 2 — MPM compaction.* The plastic deformation of the electrolyte was then resolved on the
fixed DEM skeleton with a GPU-accelerated MPM using von Mises plasticity (E = 1.53 GPa,
ν = 0.49, yield strength 0.30 GPa). The high Poisson ratio confines the softening to shear:
the bulk modulus stays at a dense-solid value (K = 25.5 GPa) while the shear modulus is reduced
(G = 0.51 GPa). VGCF fibres, PTFE fibrils and SDCP particles were then seeded into the pore
space at the experimental weight fractions.

*Stage 3 — voxel transport.* Each microstructure was rasterized onto a cubic grid with a voxel
edge of 0.15 μm. Adjacent conducting voxels were coupled through harmonic-mean conductances and
the potential field obtained from ∇·(σ∇φ) = 0, with 1 V applied between the separator (φ = 0)
and current-collector (φ = 1 V) faces and the remaining boundaries insulating; the effective
conductivity was taken from the total current. NCM811, VGCF and SDCP carried the electronic
network, LPSCl and SDCP the ionic network. **In the reported configuration PTFE is not resolved
on the conduction grid**; because the binder is insulating and its two electrodes differ in
PTFE content, this choice affects the result, and the alternative convention in which PTFE is
stamped as a blocking phase is reported as a sensitivity in Table S3b.

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

*Reported values.* Under this configuration the effective electronic conductivity is
72.3 mS cm⁻¹ (SBE) and 81.3 mS cm⁻¹ (DBE), a paired ratio of 1.124 (spread 0.003 across the
eight origin phases; observed range 1.120–1.127). Ohmic loss per phase was evaluated as
Σ g_k Δφ_k², summed over the voxel-to-voxel connections belonging to that phase.

*Limitations.* The absolute conductivities have not been calibrated against a
composition-matched measurement and should be read as the output of an idealised bulk model:
the solver places no contact resistance at any interface — between active particles, between
active material and carbon, or at the current collector — so it does not reproduce the quantity
a two-terminal DC-polarisation measurement returns. The ratio is not grid-converged: refining
the voxel edge increases it monotonically without following a power law, so the reported gain is
a **lower bound on that axis**. Explicitly restoring the fibre–fibre and additive contacts that
voxelisation drops recovers only about a fifth of that grid dependence, indicating that the
remainder originates elsewhere, most plausibly in how the additive volume is represented.

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
SDCP carried the electronic network and LPSCl and SDCP the ionic network; PTFE was not resolved
on the conduction grid, and the alternative convention in which it is stamped as a blocking
phase is given as a sensitivity in Table S3b. The VGCF conductivity is an effective network
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
refinement, so the reported gain is a lower bound on that axis.

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
| σ_ele,eff | **72.3** | **81.3** | mS cm⁻¹ |
| σ_ele ratio (paired, 8 origin phases) | — | **1.124** | — |
| ⌐ spread / range | — | 0.003 / 1.120–1.127 | — |
| σ_ion,eff | *재측정 필요* | *재측정 필요* | — |
| SE coverage of AM · VGCF coverage · CBD contacts · connectivity · areal capacity | *새 침대에서 재측정 필요* | | |

⚠ **`Porosity` 를 `ε_union` 으로 개명하고 각주**: 시뮬레이션 기하 진단값이며 통상적인 전극
porosity 가 아니다.  실험 앵커(~15.6 %) 대비 과압축이다.

## Table S3b (신설) — PTFE 표현 민감도

| PTFE convention | σ_ele SBE | σ_ele DBE | ratio | spread | range |
|---|---|---|---|---|---|
| not resolved (reported) | 72.3 | 81.3 | 1.124 | 0.003 | 1.120–1.127 |
| stamped as blocking phase | 54.0 | 70.6 | 1.308 | 0.003 | 1.302–1.310 |

각주: *Both conventions were evaluated on the same beds with the same code and grid, differing
only in whether the insulating binder occupies conduction cells; the machine-checked contract
confirms that no other parameter differs. Which convention is closer to a real thin surface
coating is not established, so both are reported.*

---

# ⚠ 본문에서 함께 고쳐야 할 곳

| 자리 | 현재 | 고침 |
|---|---|---|
| §전송 문단 | *"σ_ele increases from 1.98 to 3.00 S cm⁻¹"* | **"from 72.3 to 81.3 mS cm⁻¹"** (+12.4 %) |
| 같은 문단 | *"σ_ion … 0.203 and 0.215 mS cm⁻¹"* | ⚠ **재측정 전까지 보류** |
| 같은 문단 | *"reconstructed using a discrete element method (DEM)"* | *"reconstructed with a DEM–MPM workflow"* |
| Figure 4a 설명 | *"DEM-reconstructed …"* | *"DEM–MPM-reconstructed …"* |
| Figure 4b | 옛 σ 값 그림 | 새 값으로 재작도 |
| Table S3 제목 | *"…from the DEM simulations"* | *"…from the DEM–MPM–voxel transport workflow"* |

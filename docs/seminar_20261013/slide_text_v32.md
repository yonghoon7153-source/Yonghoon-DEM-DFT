# 연구세미나 덱 v3.2 (18 장 · 1저자 10-14 결정) — 장별 글 전문 (생성기 출력에서 추출 · 표 · 출처 줄 · 무리 안 라벨 · 식 이름 · 다리 줄 · notes 포함)

## p01
- [직사각형 10] Yonghoon An
- [직사각형 10] Division of Materials Science & Engineering, Hanyang University
- [직사각형 10] (E-mail : yonghoon71@hanyang.ac.kr)
- [직사각형 12] [date — to be set]
- [Rectangle 4] Research Seminar
- [Rectangle 4] Particle-resolved multiscale simulation of sulfide all-solid-state composite cathodes:from powder packing to transport
- [picture] 그림 2
- [picture] 그림 3
- notes: Title. Date to be set by the presenter.

## p02
- [Rectangle 4] A coupled DEM–MPM–transport workflow
- [Rectangle 4] Each stage has specific calibration targets and unresolved validation tasks.
- [Rectangle 4] Agreement between models sharing inputs is a consistency check, not independent validation.
- [TextBox 20] Introduction
- [Flow box 1] DEM packing
- [Flow box 1] soft-sphere DEM
- [Flow box 1] (contact law)
- [Flow box 2] Plastic compaction
- [Flow box 2] MPM: J2 plasticity
- [Flow box 2] DEM scaffold
- [Flow box 3] Voxel transport
- [Flow box 3] finite-volume solver
- [Flow box 3] ionic · electronic · thermal
- [Flow box 4] Electrode response
- [Flow box 4] reaction distribution
- [Flow box 4] (in development)
- [Flow target 1] calibration target:
- [Flow target 1] compaction data
- [Flow target 2] calibration target:
- [Flow target 2] pure-SE compaction
- [Flow target 3] comparison target:
- [Flow target 3] conductivity data
- [Caption] DEM packing → plastic compaction → voxel transport → electrode response; targets are what each stage is calibrated or compared against
- [Bridge] Question: how do packing and compaction shape transport paths?
- notes: No numbers. Calibration targets per stage: DEM — compaction experiments; MPM (material point method) — pure-electrolyte compaction (lab reference sample, unpublished); voxel transport — comparison with conductivity measurements (not yet matched). Agreement between stages that share inputs is a consistency check (SEM-01).

## p03
- [Rectangle 4] DEM governing equations: particle motion and contact forces
- [TextBox 20] Model
- [TextBox 69] This work — implemented equations of LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1]
- [picture] Equation panel/Panel frame/Panel frame picture
- [Equation panel/Panel tab] DEM model
- [Equation panel/Panel title] Governing equations · calculation steps
- [Equation panel/Step every dt] every Δt
- [Equation panel/Rounded Rectangle 4] Contact detection
- [Equation panel/Rounded Rectangle 6] Contact forces ③–⑤
- [Equation panel/Rounded Rectangle 8] Time integration ①–②
- [Equation panel/Rounded Rectangle 10] Update x · v · ω
- [Equation panel/eq_label_1] ① Translation
- [Equation panel/eq_label_1] Newton's 2nd law
- [Equation panel/eq_label_1] contact + gravity + global damping
- [Equation panel/eq_label_2] ② Rotation
- [Equation panel/eq_label_2] contact torque
- [Equation panel/eq_label_2] + rolling resistance Mr (④)
- [Equation panel/eq_label_3] ③ Normal contact force
- [Equation panel/eq_label_3] linear hysteresis + adhesion
- [Equation panel/eq_label_3] (non-saturated branch)
- [Equation panel/eq_label_4] ④ Tangential friction · rolling resistance
- [Equation panel/eq_hint_eq4_1] tangential spring (Coulomb limit)
- [Equation panel/eq_hint_eq4_2] rolling resistance (CDT)
- [Equation panel/eq_hint_eq4_2] ωr = ωi − ωj
- [Equation panel/eq_label_5] ⑤ Contact stiffness
- [Equation panel/eq_label_5] material (E, ν) → contact stiffness k1
- [Equation panel/eq_label_5] V: characteristic impact velocity
- [picture] Force diagram/Force diagram picture
- [Force diagram/Force label load] Load
- [Force diagram/Force label i] i
- [Force diagram/Force label j] j
- [Force diagram/Force label Fn] Fn
- [Force diagram/Force label Ft] Ft
- [Force diagram/Force label Mr] Mr
- [Force diagram/Force label mg] mig
- [Force diagram/Force caption] Forces on particle i(same model for particle–particleand particle–wall contacts)
- [Callout] Per particle: translational and rotational equations of motion; per contact pair: contact force and rolling-resistance torque.
- [Callout damping] Global damping −γv_i in ①: γ = 0.5 during stabilization and compression, 1e-5 during settling and relaxation (input-deck units) — see Problem 4.
- [Bridge] Next: what a fixed-sphere contact law cannot capture
- [equation] eq1 (OMML copied from the 10-09 slide · fallback image kept)
- [equation] eq2 (OMML copied from the 10-09 slide · fallback image kept)
- [equation] eq3_1 (OMML copied from the 10-09 slide · fallback image kept)
- [equation] eq3_2 (OMML copied from the 10-09 slide · fallback image kept)
- [equation] eq4_1 (OMML copied from the 10-09 slide · fallback image kept)
- [equation] eq4_2 (OMML copied from the 10-09 slide · fallback image kept)
- [equation] eq5_1 (OMML copied from the 10-09 slide · fallback image kept)
- [equation] eq5_2 (OMML copied from the 10-09 slide · fallback image kept)
- notes: Sources: docs/dem_governing_equations_report_20261009.md §1 (literature form ↔ implemented form ↔ source lines of LIGGGHTS-PUBLIC 3.8.0, commit 3d5c00f) and §3 (deck values); docs/dem_governing_equations_background_20261011.md §2.3 (order of one time step: contact detection → contact forces → integration → update), §3.1 (translational and rotational equations, eqs 1–2), §5.2 (k1 from E*, R*, m* and V), §5.3 (hooke/hysteresis), §6 (tangential spring with Coulomb limit), §7 (rolling resistance, CDT), §8.2 (global viscous damping), §9 (compression procedure), §11 (limits). Equations ①–⑤, the force diagram and the process strip are copied from the author's 10-09 slide: equation objects and pictures unchanged, Korean labels translated, project header removed. Qualifiers: these are the implemented equations of the LIGGGHTS-PUBLIC 3.8.0 hooke/hysteresis model [2], read from the source code, not re-derived by a run; the linear hysteretic law (loading stiffness k1, unloading/reloading stiffness k2, adhesion branch −k_c δ) follows Luding 2008 [1]; ③ shows the non-saturated branch only (the saturated branch and the k2(δmax) interpolation are in the report); ④ shows the spring part (tangential damping in non-slip steps is omitted); k_t = k_n in this model; the rolling torque uses k_n δ, not the hysteretic normal force; k1 depends on mass and the characteristic velocity V (k1 ∝ m*^(1/5) V^(2/5)), so V acts as a stiffness input in quasi-static compaction; the SE modulus 1.35 GPa entering E* is a calibrated input. The global damping term −γv_i in ① takes a large share of the plate reaction during compression (ledger DEMP-01, open) — see the Problem 4 slide. Particle–particle and particle–wall contacts use the same model.

## p04
- [Rectangle 4] Fixed-shape DEM limits and the material point method (MPM)
- [Rectangle 4] Our fixed-shape implementation has no shape change and no yield cap: overlap is the only plasticity proxy; the softened SE modulus (1.35 vs ≈ 22 GPa) is an effective parameter, not a property [1, 2].
- [Rectangle 4] J2 plasticity on a background grid: shape change and void filling that a fixed-shape sphere cannot represent; active material is kept rigid (DEM skeleton), only the electrolyte flows.
- [TextBox 20] DEM → MPM
- [TextBox 69] Luding 2008, Fig. 1 [1] (left) · figure: presenter — MPM 3D view of the DEM-scaffold bed (right)
- [Lit tag] Literature: hysteretic contact law [1]
- [picture] Lit Luding
- [Credit] Reproduced from Luding, Granul. Matter 10, 235 (2008), Fig. 1
- [Caption] δ = overlap; piece-wise linear loading / unloading branches;
- [Caption] the implementation used here is the LIGGGHTS hysteretic law [2]
- [Bridge] Next: which inputs are properties and which are effective
- notes: Sources: docs/dem_governing_equations_background_20261011.md (§5.3; §10.3 literature counts; §11 limits); CLAUDE.md MPM sections (2026-06-07 … 06-17). In one 7:3 bed, global viscous damping carries 58 % of the plate reaction during compression — an open issue (damping share 57.9 % measured on one 7:3 bed during compression; ledger DEMP-01, open). Selected literature survey (22 studies; author classification, not a systematic review): softened SE modulus 0/22; yield or hardness cap 7/22; linear hysteretic law 1/22; global damping in dry compaction none. Young's modulus reference: our DFT E_VRH = 22.06 GPa (literature DEM input 22.1 GPa, Bazzoun 2026 [8]); the bulk modulus K / B0 = 26.23 GPa is a separate quantity; the glass-electrolyte value 24 GPa (Sakuda 2013 [3]) is a different material system. The DEM statement is about this implementation (fixed spherical shapes, hooke/hysteresis), not about DEM in general. MPM parameters: 2D E = 1.53 GPa, σy = 0.15 GPa; 3D E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa (next slide). Presenter figure (right, blank): MPM 3D render of the DEM-scaffold bed (AM fixed, SE material points), e.g. python3 scripts/viz_mpm_morphology.py --se <SE material points .npy> --scaffold <AM scaffold .csv> --y 0.5 --out morphology.png (actual files required; MPM renders are not tracked in the repository). Do not present the MPM image as an independent validation of the DEM bed.

## p05
- [Rectangle 4] Effective material inputs and their status
- [Rectangle 4] Bulk modulus from DFT; shear softening and yield stress from a pure-electrolyte calibration sweep.
- [Rectangle 4] Historical and current scaffold calculations use different electrolyte initializations and run configurations; they are not one validation series.
- [TextBox 20] MPM
- [TextBox 69] This work (left) · So et al., J. Electrochem. Soc. 168, 030538 (2021), Fig. 4a (right) [9]
- [Table inputs] Input | Value and status
- [Table inputs] LPSCl reference | E ≈ 22 GPa (our DFT E_VRH; literature DEM input 22.1 GPa [8])
- [Table inputs] DEM effective | E = 1.35 GPa — reproduces compaction, not a property
- [Table inputs] MPM | E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa; K = 25.5 ≈ DFT 26.2 GPa
- [Table inputs] Calibration target | pure-SE porosity 10 % at 300 MPa (lab reference sample, unpublished)
- [Table inputs] Lab anchor (planned) | EIS + DC polarization, no results yet: NCM pellets 0.1 / 0.2 / 0.3 g, polycrystalline and single-crystal; LPSCl pellets, small and large particles
- [Caption] Tested alternatives (volumetric cap, real E) did not remove the need for effective parameters.
- [Lit tag] Literature: DEM vs SE density–pressure data [9]
- [picture] Lit So
- [Credit] Reproduced from So et al., J. Electrochem. Soc. 168, 030538 (2021), Fig. 4a
- [Bridge] Next: from the compacted structure to a transport mesh
- notes: Sources: CLAUDE.md "3D MPM compaction — 3-fix calibration" (K = E/(3(1−2ν)) = 25.5 GPa vs DFT B0 26.23); our DFT E_VRH 22.06 GPa; Bazzoun 2026 [8] uses E_SE = 22.1 GPa for Li6PS5Cl; the sulfide-glass value 24 GPa (75Li2S·25P2S5, Sakuda 2013 [3]) is a different material system and is not used on the slide. σy = 0.30 GPa was selected in the pure-SE calibration sweep (0.15 → 5.6 %, 0.20 → 6.7 %, 0.25 → 9.0 %, 0.30 → 10.0 %). Claims ledger CL-94: the pure-SE 10 % value is a calibration target (lab standard sample, unpublished); it is not a literature anchor — our earlier literature attribution was withdrawn. Shear-only softening (ν = 0.49) keeps K = 25.5 GPa close to the DFT reference B0 = 26.23 GPa; softening the bulk modulus over-crushed the bed. "Tested alternatives" = DPC volumetric cap and real-E runs (docs/mpm_dpc_cap_crosscheck.md); the statement is limited to the tested models. Scaffold calculations (AM skeleton from the DEM bed) — status: Earlier: cell-filled SE, bidirectional servo — historical, not a DEM-seeded validation. Current registered runs: DEM-seeded SE, stress-controlled servo — f = 0 completed; f(a) execution failed. AM-load-sharing hypothesis: verdict pending. The current statuses refer to the registered servo runs (--protocol servo; primary endpoint = final thickness after servo convergence). AM load sharing remains a candidate explanation for over-compaction; the final hypothesis verdict is pending. The earlier thickness agreement is not shown: it comes from a different initialization and loading protocol and cannot serve as the validation value of the DEM-seeded runs (SEM-02). Literature crop: So et al., J. Electrochem. Soc. 168, 030538 (2021) [9], Fig. 4a — relative density vs pressure of a sulfide SE with their contact-plasticity parameter (experimental points from Sakuda et al.): a literature example of calibrating an effective contact parameter on pure-SE compaction data. Planned lab anchor (replaces the earlier "validation pending" row; no results yet): docs/session_20260923_progress.md 10-14 entries — EIS plan: LPSCl pellet 0.1 g (10 mm diameter, 300 MPa) as the σ₀ reference; NCM polycrystalline and single-crystal pellets of 0.1 / 0.2 / 0.3 g (six pellets, EIS + DC polarization); composite and Li-In electron-blocking cells after the NCM pellets; the small-particle SE pellet also gives a geometric porosity (true density unverified) as the pure-SE compaction check; a large-particle LPSCl pellet tests the particle-size factor (listed by the author on 10-14 for this deck; the progress log of 10-14 evening still records it as a recommendation awaiting an answer).

## p06
- [Rectangle 4] Voxelizing the compacted microstructure into a transport mesh
- [Rectangle 4] Faces are joined by a harmonic mean with no interface-resistance term: an ideal-interface voxel model — an upper bound only within the same geometry, properties and boundaries.
- [Rectangle 4] VGCF as diameter-preserving segments, PTFE as a centre-line insulator, polymer as spheres; a registered 104-arm study keeps the σ(e⁻) order across 1–4 wt% VGCF on all tested grids (72/72).
- [TextBox 20] Transport
- [TextBox 69] figure: presenter — 3D current-flow views, contact network and voxel (left) · this work, 104-arm study (right)
- [picture] Fig VGCF
- [Caption] Original Phase A campaign (VGCF E = 10 GPa): means of 96 primary arms,
- [Caption] three voxel sizes; no contact resistance
- [Bridge] Model chain set — next: results from the simulated beds
- notes: Sources: CLAUDE.md "σ 를 내는 솔버는 둘이다" table and CL-81. Finite-volume conservation on the phase grid gives electrical (σ, φ) and thermal (κ, T) transport on the same structure. The voxel solver has no interface-resistance term by default (the film mechanism exists but is off): this makes it an ideal-interface model and an upper bound only for the same geometry, phase properties and boundary conditions — not a physical upper bound; geometric necks still cost resistance inside the voxel grid. The 4.04× (contact-free / full network, n = 157) is a ratio inside the contact-network model. Additives: carbon fibres (VGCF) as diameter-preserving segments, PTFE as a centre-line insulator, a conductive polymer as true-diameter spheres. Pre-registered 104-arm study: the electronic-conductivity order across 1–4 wt% VGCF holds across the tested voxel sizes and grid-origin offsets (72/72) — docs/data/phase_a_rep100_20260930/README.md (104 arms, 72/72 adjacent-composition comparisons with no threshold violation; order only is the registered estimand; increments are technical report only; replay difference 0.00000 %); docs/report_20261021 G6 (voxel σe means; contact resistance not included; figure F_vgcf redrawn from G6). The plotted means are the original campaign (VGCF E = 10 GPa, docs/data/phase_a_104arms_20260921); the 100 GPa replication (docs/data/phase_a_rep100_20260930) also keeps the order 72/72 with slightly different means, so the plotted values are not the 100 GPa means. Stamp conventions: CLAUDE.md SR-01 (sphere stamp, centerline PTFE = CL-60). Presenter figures (left, blank): (i) contact-network current pathways of the 7:3 bed — scripts/network_current.py dump <7:3 result folder> → webapp DEM 3D viewer "current flow" (same bed, same H0/FULL ionic solution, 1 V, colour = j = |I|/A; "top 50 % of current" = edges carrying the top half of the current share, not the top half by count); (ii) STEP3 phase grid and the 1 V current-density field of the same voxel solution (A cm⁻²; state origin, voxel size, phase mapping, electrode rule, run hash).

## p07
- [Rectangle 4] Composition-dependent porosity in five simulated beds
- [Rectangle 4] Soft-sphere DEM with a linear hysteretic contact law, pressed to 300 MPa; one bed per composition, no seed replicates.
- [Rectangle 4] One 7:3 bed: porosity 31.8 → 25.1 → 16.7 → 16.5 % (final state relaxed at fixed platen); 7:3 (large : small NCM) is the lowest of the five beds.
- [TextBox 20] DEM
- [TextBox 69] This work — DEM, five NCM–SE beds (one bed per composition)
- [picture] Fig 3D stages
- [picture] Fig porosity
- [Caption] Left: four stages of one 7:3 bed, 0 · 47 · 296 · 165 MPa (last = relaxed at fixed platen); porosity = exact union of spheres.
- [Caption] Right: final porosity of the five beds (one bed each; the red bar is the minimum).
- [Lit tag] Literature: pure LPSCl in the die at 0.3 GPa, porosity ≈ 13 % (D50 40 µm) to ≈ 26 % (4 µm) [13] — not composite beds
- [Bridge] Next: the same five beds as a Li⁺ contact network
- notes: Sources: docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md §6; docs/report_20261021/summary.json G1 (figure F_poro redrawn from the same values). Qualifiers: one bed per composition, no seed replicates; porosity = exact union of spheres; "lowest of five" is a statement about these five single beds, not an optimum ratio; the 165 MPa panel is the relaxed state at fixed platen, not an unloaded state. Literature context (pure SE, not composite beds; different convention and state): Faka 2026 [13] — in-die (at pressure) relative density of pure Li6PS5Cl at 0.3 GPa read from their Fig. S2: porosity ≈ 12.9 % (D50 40 µm), 16.0 % (20 µm), 22.5 % (11 µm), 26.3 % (4 µm); relative density uses the Rietveld crystal density; no compliance or elastic-compression correction is described. Thompson 2026 [12] — in situ CT (1.277 µm pixel) of pure LPSCl under quasi-isostatic pressure: intergranular pores mostly closed at 479 MPa; no pores resolved at 1155 MPa. Neither is a validation of the five DEM beds. Cards: litdb faka2026_particle_size_consolidation_strain_lpscl · thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography (docs/seminar_20261013/slide_sources_v32.json).

## p08
- [Rectangle 4] From the contact network to Li⁺ transport
- [Rectangle 4] Contact-network approach [8]: bulk resistance + Holm/Maxwell constriction using Hertz contact radii; chosen σ₀ = 1.5 mS cm⁻¹ (pellet-literature range).
- [Rectangle 4] Transport tortuosity T = φ_SE σ₀ / σ_eff: 7.2 → 5.0 (0:10 → 7:3). Contact constriction accounts for 73–75 % of Joule dissipation in this network model.
- [TextBox 20] DEM
- [TextBox 69] This work (left) · Bazzoun et al., J. Power Sources 661, 238682 (2026), Fig. 2 (right) [8]
- [picture] Fig transport
- [Lit tag] Literature: SE resistor network [8]
- [picture] Lit Bazzoun
- [Credit] Reproduced from Bazzoun et al., J. Power Sources 661, 238682 (2026), Fig. 2
- [Caption] (a) transport tortuosity (Hertz), (b) σ(Li⁺) at σ₀ = 1.5 mS cm⁻¹; one bed per composition;
- [Caption] T is the literature "tortuosity factor" (not its square root); red = extreme of the five
- [Bridge] Next: what does not work — grid and absolute σ(e⁻)
- notes: Sources: docs/data/ps45_r45_network_g2_20261007/README.md (values, σ0 = 1.5 section, decomposition section); figure F_trans redrawn from those values (y-axes start at 0). Qualifiers: transport tortuosity T = φ_SE σ0 / σ_eff (the literature "tortuosity factor"; not its square root); Hertz H0 = primary; the 73–75 % share = ΣI²R(constriction) / ΣI²R(total) of the same FULL network solution — a model-internal ratio, not evidence that contact necks explain 75 % of a real electrode. No seed replicates for these five beds; the 7:3 vs 10:0 difference is not resolved. [8] = Bazzoun 2026 (same network approach; the crop shows their resistor-network scheme). A 3D current-pathway view of the 7:3 bed is on the transport slide (presenter figure).

## p09
- [Rectangle 4] Problems 1 and 2: grid dependence and absolute σ(e⁻)
- [Rectangle 4] The electronic ratio decreases across the three tested voxel spacings (0.4, 0.3, 0.25 µm); the ionic ratio crosses 1. Grid convergence has not been established.
- [Rectangle 4] Voxel predictions exceed the available DC-polarization estimates; measurement conditions remain unverified. A registered re-run calibrates carbon on SBE alone (σ_VGCF* = 3.41 S cm⁻¹, an effective value); the DBE prediction (order only) is pending.
- [TextBox 20] Limits
- [TextBox 69] This work — voxel transport solver (a, b) · contact network, five NCM–SE beds (c)
- [picture] Fig limits
- [Caption] (a) Grid dependence: same bed pair and convention; no converged conductivity ratio is reported.
- [Caption] (b) Voxel model vs DC polarization, log scale; conditions not yet matched.
- [Caption] (c) NCM–SE beds: no carbon/binder; Hertz H0; common NCM reference 4.1 mS cm⁻¹ [11]; size factor off; one bed per composition.
- [Table absolute] Lee 2025 [10] | R = 2.07, model / literature: order-of-magnitude agreement, not within the registered band
- [Table absolute] PTFE 1 vs 0.5 wt% | Q = 0.84, retained after PTFE: registered model-sensitivity prediction met, not an experimental hit
- [Bridge] Next: how load is shared between NCM and SE contacts
- notes: Sources: claims ledger CL-24 (public values at vox 0.4/0.3/0.25); CL-41 (vox ≤ 0.15 values on hold — not shown); CL-72 ("lower bound" retracted). The three public points admit an exact power-law fit (three points, three parameters), so no statement about power laws or extrapolation is made from them (SEM-03); the earlier manuscript headline at 0.4 µm is superseded. Finer grids reach the memory limit of one GPU (peak RSS 35.6 GB at vox 0.115; 0.10 µm ≈ 54 GB). Panel (b): docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md (DC-polarization values 4.47 and 12.4 mS/cm, measurement conditions unverified; model 54.0 and 70.6; re-run registered: S1–S2 done on 10-14, σ_VGCF* = 3.41 S/cm interpolated in ln σ_e – ln σ_VGCF between 2.618 and 3.927 S/cm (local slope 0.545); S3 (8 origins × SBE and DBE) running — acceptance (J1) and order (J2) verdicts pending; docs/session_20260923_progress.md 10-14). Panel (c): docs/data/ps45_sigmae_factor_off_20261013/README.md (0.391 · 0.406 · 0.402 · 0.375 · 0.467 mS/cm; raw minimum 0.3747). Footnote (Codex §6-1): computed effective electronic conductivity of the DEM particle arrangement; Hertz H0 / Holm–Maxwell constriction; common reference conductivity 4.1 mS/cm for polycrystalline and single-crystal NCM (Wang 2018 [11], SPS pellet NMC811 at 20 °C, designated reference); no empirical size factor; absolute values conditional on this reference and contact model; single bed per composition, scatter not evaluated; carbon- and binder-free AM–SE composite. Qualifiers for σ_VGCF* (registration §4): a lumped effective value at vox 0.15 — fibre contact resistance and unresolved geometry in one carbon conductivity (grid not converged; not a fibre property); calibrated on one SBE point, DBE predicted (only the order is judged); experimental conditions unverified, so "the model reproduces the experiment" is not claimed (one calibration point plus one order check). Absolute-conductivity comparison (moved from the removed progress slide): docs/reviews/lee_abs_sigma_e_prereg_20260923.md §5 (R = 2.074 ± 0.004, Tier 1 "order-of-magnitude", not "within band"; Q = 0.840 = registered model-sensitivity prediction met, not an experimental hit; comparison with Lee 2025 [10]). Historical eight-origin study (moved from the removed progress slide): docs/reviews/sdcp_gain_prereg_v2_20260816.md — the eight-origin (voxel 0.15 µm) study: numerical ratios and the h1 inference are on hold in the claims ledger (CL-33/34/41), so no result is reported. "Origin" = voxel-grid origin offsets of the same bed, not independent replicate beds. Moved from the slide body to these notes (the (c) note line carries it): The NCM–SE comparison uses a common reference conductivity and a specified contact model.

## p10
- [Rectangle 4] Problem 3: Load sharing during compaction
- [Rectangle 4] NCM–NCM contacts contribute 48–60 % of vertical stress after relaxation at fixed platen position; 7:3 is the minimum.
- [Rectangle 4] The NCM–NCM stress-share ranking matches the experimental porosity summaries for the selected five compositions (exploratory, n = 5).
- [TextBox 20] Limits
- [TextBox 69] This work — DEM, five beds (left) · one 7:3 bed, four stages (right)
- [picture] Fig load share
- [picture] Fig SE von Mises
- [Caption] Left: contribution to σ_zz by contact type, 21 planes, load-weighted; relaxed at fixed platen.
- [Caption] Right: SE von Mises stress in one 7:3 bed, four stages (0 · 47 · 296 · 165 MPa), 0–150 MPa; wall SE excluded.
- [Bridge] Next: what the nominal plate pressure contains
- notes: Sources: docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json (21-plane load-weighted shares; figure F_load redrawn from contribution_sigma_zz_pct: NCM–NCM 59.56 · 54.63 · 52.37 · 48.46 · 56.91 % for 0:10 → 10:0; all NCM–NCM contacts, not large–large — the 0:10 bed has no large particles); state = relaxed at fixed platen (mean plane load 158–175 MPa, not the 300 MPa peak). Codex 2026-10-09 verdict: correlation observed; "springback" interpretation and stiffness inversion on hold (RB-01/RB-02); experimental thickness = selected 3-of-n average. SE stress figure: ps73 stages README §6 (wall SE excluded, linear 0–150 MPa). A 3D view of NCM particle stress / force chains of the same bed can be added by the presenter from the webapp. Literature on unloading (pure LPSCl; context for the springback question above, not a validation): Thompson 2026 [12] — on decompression the lattice shift is reversible while peak broadening and the conductivity gain remain (quasi-isostatic cell; decompression only to ≈1.1–1.8 GPa, not to zero load; conductivity from a separate cell under similar pressure conditions). Faka 2026 [13] — distinguishes in-die (at pressure) from out-of-die Heckel analysis, the latter including elastic recovery; their own data are in-die only.

## p11
- [Rectangle 4] Problem 4: what the 300 MPa plate reaction contains
- [Rectangle 4] The 300 MPa stop criterion reads the plate reaction during compression, which includes global viscous damping: in one 7:3 bed the drag is 57.9 % of the target force (750 N, deck units).
- [Rectangle 4] At fixed platen the same bed relaxes to 165 MPa; a servo branch holding the target force (damping 1e-5) instead compacts it further (111.05 → 105.84 µm) — model-internal until the open checks pass.
- [TextBox 20] Limits
- [TextBox 69] This work — DEM, one 7:3 bed: stop, relaxation and servo-hold branch
- [picture] Fig plate reaction
- [Table checks] Before citing the hold state | Status
- [Table checks] Convergence flag vs. static equilibrium | open
- [Table checks] Plate re-created at servo start: contact history reset | open
- [Table checks] Atom-count guard vs. conservation (13 SE particles lost) | open
- [Caption] (a) one 7:3 bed: stop step (damping 0.5), relaxed at fixed platen (original run), servo hold at the target force (damping 1e-5)
- [Caption] (b) ε_sphere = sphere-volume porosity, not the exact union; shaded = band registered before the run; hatched = checks still open
- [Bridge] Next: in progress — dry mixing before pressing
- notes: Sources: docs/reviews/findings.json DEMP-01 (open: global viscous damping 0.5 during stabilization and compression, 1e-5 during relaxation; the stop criterion |F_plate|/A ≥ 0.30 deck MPa includes the damping drag; one 7:3 bed: drag −γΣv_z = 434.3 N = 57.9 % of the 750 N target (deck units: 0.30 deck MPa × plate area 0.0025 in deck units; docs/dem_governing_equations_background_20261011.md §9); after the plate stops the network pressure relaxes to 165 MPa), MV-01, MV-02 and MV-08 (open); docs/data/ps73_damping_branch_20261007/README.md §1 (original run, relaxation end at fixed platen 165.34 MPa), §4 (predictions B1 and B2 registered before the run), §12-4 (branch B on ibb, job 271368: stop step 3,125,000, 111.052 µm, ε_sphere 14.953 %, 300.906 MPa, drag 434.18 N = 57.89 %; servo hold at 750 N with damping 1e-5 to step 3,735,000, 122 chunks, CONVERGED flag, 105.842 µm, ε_sphere 10.769 %, 299.274 MPa; atoms 160,420 → 160,407, 13 SE lost, AM unchanged; plane-load NCM–NCM share 52.1 → 58.1 %, judgement on hold). B1 equals the registered stop state; B2 (104.9 µm, band 103–107 µm; ε_sphere 10.0 %, band 8.3–11.7 %) contains the result. Figure F_p4 is redrawn from these recorded values only (docs/seminar_20261013/figs_v3/make_seminar_figs_v32.py). Qualifiers: one bed, one composition, one checkpoint; model-internal diagnostic values. (i) The CONVERGED flag does not certify static equilibrium (MV-01). (ii) The servo deck re-creates the plate and wall fixes, which also resets the normal plastic contact history, so B is a combined protocol (history reset + damping drop + force hold); the registered follow-up protocol includes a reset of the plate contact history (MV-02). (iii) The atom-count guard does not certify conservation; the 13 lost particles are SE (MV-08). Wording (docs/reviews/codex_review_model_validation_20261008.md Q11): relative to the existing dynamic stop state, the registered follow-up protocol changed thickness and sphere-volume porosity by −5.210 µm and −4.184 %p; only after separate equilibrium and conservation checks pass may the end point be read as the nominal static 300 MPa state; the comparison is limited to this bed and loading history. ε_sphere is the sphere-volume porosity (overlap counted twice), a different convention from the exact-union porosity shown earlier. The porosity and load-sharing slides use the original protocol (generation 1).

## p12
- [Rectangle 4] Layered-bed mixing: unresolved mixing-index contrast
- [Rectangle 4] Rotating-drum DEM, cohesive soft contacts: ten runs from a layered start, eight revolutions; Lacey index M on 16×16×4 bins vs a random reference.
- [Rectangle 4] Low NCM–NCM cohesion versus the reference setting gives an unresolved paired contrast at 16×16×4 bins (ΔM = 0.0012, seed SE = 0.0073). Subsequent diagnostic classification; the original 1% overlap condition was not met.
- [TextBox 20] Mixing
- [TextBox 69] This work (left) · figure: presenter — bed view, layered start and after eight revolutions (right)
- [picture] Fig mixing index
- [Caption] M = 1: random-reference variance; error bars = within-run SD; all ten runs reach M ≈ 0.96–1.00,
- [Caption] so this bin grid cannot separate the settings
- [Bridge] Next: exploratory cohesion settings
- notes: Sources: docs/reviews/mixer_layered_prereg_20260921.md §2 (verdict line), §5 (report wording), §6 (readout 2026-09-30); docs/data/mixer_final10_20260930/ (ten runs; figure F_mix1 redrawn from the registered final values, report_20261021 G7). Registered estimand: paired contrast of the final Lacey index between the low NCM–NCM cohesion setting (small but nonzero: CED 108,795 and 142,562 J m⁻³ for the large and small NCM self-pairs; model Bond number 0.00109 and 0.00553) and the reference setting (model Bond number 3.0), three seeds, 16×16×4 bins: Δ = +0.0012, seed-to-seed SE 0.0073 ⇒ |Δ| ≤ SE. The numerical rule maps this contrast to the registered "no segregation" category. This does not establish compliance with the original registration, equivalence, or a physical absence of segregation (this model, this drum, the tested inputs and this bin convention). Coarser grids (report only): 12×12×3 Δ −0.0156, SE 0.0058 (ambiguous); 8×8×2 Δ +0.0081, SE 0.0144. Negative control (no cohesion): M ≥ 0.8 in all three grids; floor check 10/10; flatness 30/30; QC 30/30. The two cohesion matrices differ in NCM–NCM and NCM–wall adhesion together; the comparison is not a reproduction of real coating or of powder flowability. Contract qualifier (Codex wording, 2026-09-28): the result is a comparison of mixing indices after eight revolutions in the specified soft-contact model; in the reference state the maximum stored-frame overlap was 4.7–5.8 % particle–particle and 4.5–5.7 % at the wall, so the registered 1 % condition was not met; the effect of the overlap error on the mixing index has not been verified. Conditions: three phases, 100,000 particles, drum radius 13.1 mm, 75 rpm. Presenter figure (right, blank): bed view of one run, layered start and after eight revolutions (webapp bed view; display only). Literature on the index (context): Lacey's M is normalized to a random-mixture variance; Hersey 1975 [4] noted that homogeneity measures referenced to a random mixture are not satisfactory for ordered mixtures. Mixing in which small particles adhere to carrier-particle surfaces was called ordered mixing by Hersey 1975 [4]; Egermann & Orr 1983 [5] proposed calling this type interactive mixing and reserved "ordered" for homogeneity beyond random (σ < σ_R) (wording of docs/hetero_thesis.md §2-5). The M values here use the random reference.

## p13
- [Rectangle 4] Exploratory cohesion settings produce different mixing indices
- [Rectangle 4] One seed, two revolutions: large-NCM self-pair model Bond number 38.4, 384, 1152, or all nonzero cohesion-energy densities ×10 and ×14.42 (vs the low-cohesion comparator).
- [Rectangle 4] Within each series ΔM rises with the imposed level; levels were chosen post hoc, and wall adhesion and start states also differ — no verdict.
- [TextBox 20] Mixing
- [TextBox 69] This work (left) · figure: presenter — low versus higher NCM cohesion, two revolutions (right)
- [picture] Fig cohesion exploration
- [Caption] ΔM = M(low-cohesion comparator) − M(setting); hatched: bin grid failed the volume-coverage check;
- [Caption] ΔM includes start-state differences; M < 0 lies outside the Lacey range
- [Bridge] Next: why SE–SE adhesion is the open term
- notes: Sources: docs/data/mixer_highbo_devrot_prelim_20261002/, mixer_highbo_devbo_prelim_20261003/, mixer_highbo_devu_prelim_20261006/ (README and readout JSONs; development data; one seed per arm; two revolutions; no pass/fail line; not used for any verdict; not mixed with the confirmatory seeds). Two series, defined separately: (i) the model Bond number of the large-NCM self-pair (code convention: equilibrium cohesive force / particle weight) 38.4 → 384 → 1152 — the large-NCM cohesion energy density rises only 3.56348e6 → 7.67728e6 → 1.10725e7 J m⁻³ (×2.154, ×3.107); (ii) all nine nonzero cohesion-energy-density entries of the low-cohesion comparator multiplied by 10 and 14.42. ΔM = M(low-cohesion comparator) − M(setting), bins 16×16×4 / 12×12×3 / 8×8×2: NCM-pair Bo 38.4 +0.010 / −0.006 / +0.008 · Bo 384 +0.827 / +0.927 / +0.988 · Bo 1152 +1.876 / +2.432 / +3.164 · all-pair CED ×10 +0.239 / +0.165 / +0.103 · CED ×14.42 +0.865 / +0.484 / +0.267. The 16×16×4 cells of NCM-pair Bo 384 and 1152 and of all-pair CED ×14.42 failed the volume-coverage check. M of the NCM-pair Bo 1152 setting is −0.968 / −1.407 / −2.283 (outside the Lacey range [0, 1]); start-state variances differ between settings, so ΔM mixes a start-state difference with the post-rotation difference. Cohesion levels were selected after earlier runs (post hoc); every setting uses the same development seed. NCM–NCM and NCM–wall adhesion change together. All exploratory decks share the stiffened SE modulus (2e8 Pa); compare with the original soft campaign only with that generation noted. The low-cohesion comparator is small but nonzero (CED 108,795 and 142,562 J m⁻³ for the large and small NCM self-pairs). No sentence about real coating effects or real powders is made. Presenter figure (right, blank): bed snapshots of the low-cohesion comparator vs a higher-cohesion setting after two revolutions (webapp bed view). Literature on mixer stress (context, different system and mixer): Kissel 2026 [6] — coarse-grained DEM of a high-intensity mixer (one particle species, no cohesion term; simulated net specific power agreed with the experiment at high rotor speed only) for a halide-SE coating on single-crystal NCM: coating coverage followed the stress intensity rather than the number of stress events. This is context for mixer-side process variables, not a comparison with the drum runs.

## p14
- [Rectangle 4] Surface energy and coating: SE–SE adhesion is the open term
- [Rectangle 4] With equal contact areas and an assumed geometric-mean adhesion rule, ΔW = 2(√γ_A − √γ_S)² ≥ 0 is an adhesive-work difference per unit area; SE–SE cluster survival also depends on relative surface energies and contact dynamics.
- [Rectangle 4] Exploratory all-pair CED scaling retains a larger SE–SE cluster fraction than the low-cohesion comparator; the confirmatory 18-run block remains on hold.
- [TextBox 20] Mixing
- [TextBox 69] This work: exploratory contact statistics (left), conditional adhesion model (right)
- [picture] Fig SE clusters
- [picture] Fig adhesion scheme
- [Caption] Left: one seed, mean over the second revolution; whiskers = dump-resolution range, not a confidence interval.
- [Caption] Right: γ = surface energy, W = work of adhesion; the uncoated NCM / SE surface-energy ratio is not known.
- [Lit tag] Literature: fines adhering to carriers — ordered mixing [4], interactive mixture [5]; clean-slab DFT γ: LiNiO₂ < LiCoO₂ [7]
- [Bridge] Next: the plan for these open items
- notes: Sources: docs/hetero_thesis.md (ratified 2026-10-05) §2-1 · §2-2 · §2-8. With W_AA = 2γ_A, W_SS = 2γ_S and an assumed geometric-mean rule W_AS = 2√(γ_A γ_S), ΔW = W_AA + W_SS − 2 W_AS = 2(√γ_A − √γ_S)² ≥ 0 (J m⁻²) is a per-area comparison at equal contact areas (ΔU = −A·ΔW for a common area A); real exchanges also change contact areas, deformation energy and dynamics, so contact counts alone do not fix the sign of the released energy. Pull-off force (JKR) scales with W·R*: at equal W the weight-normalized SE–SE adhesion is about 194× that of the large-NCM self-pair (arithmetic estimate), but for one SE particle the SE–NCM pull-off exceeds SE–SE by 2r_NCM/(r_NCM + r_SE) = 1.8 (large NCM) and 1.6 (small NCM). Under the geometric-mean rule the SE–SE pull-off exceeds the SE–large-NCM pull-off only if γ_NCM/γ_SE < 0.309 (small NCM: 0.391) — a two-contact force comparison, not a necessary or sufficient condition for cluster survival; that ratio is not known (open decision). Predictions P1–P3 of the thesis: uncoated beds keep SE–SE clustering above random; coating removes it; the mixing difference carries into the compacted SE pathway. The all-pair CED runs also scale SE–SE cohesion; the model is not calibrated to measured surface energies or coating selectivity, so the CED-scaling runs do not validate a surface-energy-based coating mechanism. Left figure: docs/data/mixer_highbo_devu_prelim_20261006/devu_contact.json — fraction of SE in SE–SE clusters (second revolution, 100 frames): 0.400 [0.143, 0.542] low NCM–NCM cohesion; 0.954 [0.875, 0.957] all-pair CED ×10; 0.988 [0.981, 0.988] all-pair CED ×14.42 (ranges = dump-resolution [certain, possible], not confidence intervals; one seed; development data; the lower bounds of the two higher settings exceed the comparator upper bound). Confirmatory 18-run block: registered, on hold after the Codex rounds (docs/reviews/mixer_highbo_prereg_20260927.md). Literature (canonical cards): Mixing in which small particles adhere to carrier-particle surfaces was called ordered mixing by Hersey 1975 [4]; Egermann & Orr 1983 [5] proposed calling this type interactive mixing and reserved "ordered" for homogeneity beyond random (σ < σ_R) (wording of docs/hetero_thesis.md §2-5). NCM side of the surface-energy ratio: Kim 2012 [7] — clean-slab DFT (GGA+U, 0 K) surface energies of the end members LiNiO₂ and LiCoO₂ (not NCM) are lower for LiNiO₂ on all computed facets; these are bond-breaking energies of clean slabs, not the dispersion adhesion W of particle contacts, so the uncoated NCM / SE ratio stays open (docs/hetero_thesis.md §2-8).

## p15
- [TextBox 20] Plan
- [Rectangle 4] Tests for unresolved model limits
- [Rectangle 4] Grid sensitivity remains unresolved. Diagnostic results exist, while final hypothesis verdicts remain pending.
- [Audit findings] Electronic transport
- [Audit findings items] Interface resistance: film model implemented, production on hold
- [Audit findings items] Carbon conductivity: comparison with DC polarization
- [Audit findings items] NCM conductivity: literature-based input review
- [Decisions recorded on Sep 12] Compaction and mixing
- [Decisions recorded on Sep 12 items] AM load sharing: final hypothesis verdict pending
- [Decisions recorded on Sep 12 items] Unloading (springback vs. measured thickness): history test passed; kit re-review HOLD, fixes ratified
- [Decisions recorded on Sep 12 items] Mixing: an adhesion parameter for SE–SE contacts
- [Gen2 head] DEM protocol generation 2 — plan, no runs yet
- [Gen2 box 1] insertion
- [Gen2 box 2] stabilization
- [Gen2 box 3] compression
- [Gen2 box 4] servo
- [Gen2 box 5] relaxation
- [Gen2 box 6] platen removal
- [Gen2 box 7] unloading
- [Gen2 note] SE true density 1.64 g cm⁻³ (lab standard, unverified) · E_SE set so that pure-SE beds reach ε_union = 10–13 % after 300 MPa and relaxation (ε_sphere kept internally) · Heckel analysis redone
- [Bridge] Next: summary of findings and limitations
- notes: Sources: docs/reviews/contact_resistance_pipeline_draft_v3_1_20261007.md; docs/reviews/fam_platen_prereg_20260812.md §12; docs/reviews/dem_unloading_ps45_prereg_20261009.md §12–13; docs/hetero_thesis.md §4. Grid sensitivity: no new grid campaign is promised here. Unloading: the contact-history test on ibb passed (H0–H5 all PASS; docs/reviews/dem_unloading_history_test_20261014/README.md); the Codex re-review of the unloading kit returned HOLD (12 findings ULKR-01 … ULKR-12; docs/reviews/codex_review_dem_unloading_kit_20261014.md); the fix plan docs/reviews/dem_unloading_kit_fix_plan_20261014.md was ratified on 10-14 (Q1–Q9 as recommended; docs/session_20260923_progress.md, 10-14 afternoon 2 entry); the main unloading run waits for the Codex re-check. DEM protocol generation 2 — plan only, no runs and no results (docs/session_20260923_progress.md, 10-14 evening entries): stages insertion → stabilization → compression → servo (holding the target force) → relaxation → platen removal → unloading, so the unloading logic is a prerequisite; SE true density 1.64 g/cm³ to match the lab value (true density unverified; canonical cards give 1.64 or 1.86–1.87); E_SE re-calibrated so that a pure-SE bed after 300 MPa and relaxation has a union porosity of 10–13 % (lab standard; the small-particle SE pellet geometric porosity is the check), with ε_sphere still recorded internally — choosing ε_union alone cannot resolve a mismatch with a mass-based porosity (docs/reviews/codex_review_model_validation_20261008.md MV-03); Heckel analysis redone, because a slope against the nominal stop pressure is an apparent coefficient of the old protocol (same review, Q2). Design points: compression damping, a static stop rule, no plate re-creation at the servo switch, conservation checks; generation-1 beds stay as labelled results. Next: plan document with canonical literature cards → author ratification → Codex.

## p16
- [TextBox 20] Summary
- [Rectangle 4] Current findings and limitations
- [Rectangle 4] DEM and contact networks: composition trends from one bed per composition
- [Rectangle 4] DEM loading: the nominal 300 MPa plate reaction includes damping; a revised protocol is planned
- [Rectangle 4] MPM: plastic deformation, with compaction agreement dependent on initialization and loading protocol
- [Rectangle 4] Voxel transport: ideal-interface calculations with grid dependence and unresolved absolute conductivity
- [Rectangle 4] Mixing: unresolved diagnostic mixing-index contrast under an unmet overlap condition; exploratory cohesion results without a verdict
- [Rectangle 4] Final model-validation verdicts remain pending
- [Bridge] Questions and discussion
- notes: Summary; no new numbers. No universal guarantee about registration or verification is claimed (SEM-06). The "DEM loading" line summarizes the Problem 4 slide (docs/reviews/findings.json DEMP-01, open; docs/data/ps73_damping_branch_20261007/README.md §12-4) and the generation-2 plan (docs/session_20260923_progress.md 10-14).

## p17
- [TextBox 20] References
- [Refs left] Contact mechanics and DEM
- [Refs left] [1] S. Luding, Granul. Matter 10, 235–246 (2008)
- [Refs left] [2] LIGGGHTS-PUBLIC 3.8.0 (commit 3d5c00f, 2024), github.com/CFDEMproject/LIGGGHTS-PUBLIC
- [Refs left] [3] A. Sakuda, A. Hayashi, M. Tatsumisago, Sci. Rep. 3, 2261 (2013)
- [Refs left] Powder mixing and surface energy
- [Refs left] [4] J.A. Hersey, Powder Technol. 11, 41–44 (1975)
- [Refs left] [5] H. Egermann, N.A. Orr, Powder Technol. 36, 117–118 (1983)
- [Refs left] [6] M. Kissel et al., Nat. Commun. 17, 3215 (2026)
- [Refs left] [7] Y. Kim, H. Lee, S. Kang, J. Mater. Chem. 22, 12874–12881 (2012)
- [Refs right] Solid-state battery electrodes and electrolytes
- [Refs right] [8] A.M. Bazzoun et al., J. Power Sources 661, 238682 (2026)
- [Refs right] [9] M. So et al., J. Electrochem. Soc. 168, 030538 (2021)
- [Refs right] [10] D.J. Lee et al., Nat. Commun. 16, 4200 (2025)
- [Refs right] [11] S. Wang, M. Yan, Y. Li, C. Vinado, J. Yang, J. Power Sources 393, 75–82 (2018)
- [Refs right] [12] O. Thompson et al., Adv. Funct. Mater. 36, e75195 (2026)
- [Refs right] [13] V. Faka et al., Adv. Energy Mater. 16, e05186 (2026)
- notes: All literature entries ([1], [3]–[13]) are taken from the canonical literature cards (original PDFs, litdb canonical branch); no bibliographic field was filled from memory; [2] is the software repository at the pinned commit (docs/data/liggghts_add_pair_pin.json; version and commit date 2024-06-07 from docs/data/liggghts_3d5c00f_dem_eq_source_20261009/README.md and docs/dem_governing_equations_report_20261009.md). Card slugs: docs/seminar_20261013/slide_sources_v32.json. Entries not cited anywhere in v3.2 were removed and the list was renumbered (v3.1 → v3.2: [7] → [2], [15] → [3], [12] → [10], [16] → [11]; [1], [8], [9] unchanged). The constriction law (Holm/Maxwell) and the MLS-MPM numerical method have no canonical card yet and are cited as the models used, without a bibliographic entry. Literature crops on the DEM-limits, MPM-inputs and contact-network slides are reproduced from the papers of [1], [9] and [8] (canonical figure crops).

## p18
- [picture] Picture 2
- [TextBox 1] Thank you
- [직사각형 2] For more information or any questions, please e-mail at yonghoon71@hanyang.ac.kr

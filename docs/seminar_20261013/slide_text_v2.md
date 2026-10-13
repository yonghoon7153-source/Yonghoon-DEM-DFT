# 연구세미나 덱 v2 — 장별 글 전문 (Codex 10-13 판정 반영 · 생성기 build_seminar.py 출력에서 추출)

## p01
- [직사각형 10] Yonghoon An
- [직사각형 10] Division of Materials Science & Engineering, Hanyang University
- [직사각형 10] (E-mail : yonghoon71@hanyang.ac.kr)
- [직사각형 12] [date — to be set]
- [Rectangle 4] Research Seminar
- [Rectangle 4] Particle-resolved multiscale simulation of sulfide all-solid-state composite cathodes:from powder packing to transport
- notes: Title. Date to be set by the presenter.

## p02
- [Rectangle 4] A coupled DEM–MPM–transport workflow
- [Rectangle 4] Each stage has specific calibration targets and unresolved validation tasks.
- [Rectangle 4] Agreement between models sharing inputs is a consistency check, not independent validation.
- [TextBox 20] Introduction
- [Caption] < DEM packing → plastic compaction → voxel transport → electrode response >
- notes: No numbers. Calibration targets per stage: DEM — compaction experiments; MPM — pure-electrolyte compaction (lab reference sample, unpublished); voxel transport — comparison with conductivity measurements (not yet matched). Agreement between stages that share inputs is a consistency check (SEM-01).

## p03
- [Rectangle 4] Composition-dependent porosity in five simulated beds
- [Rectangle 4] Soft-sphere DEM with a linear hysteretic contact law, pressed to 300 MPa; one bed per composition, no seed replicates.
- [Rectangle 4] One 7:3 bed: porosity 31.8 → 25.1 → 16.7 → 16.5 % (final state relaxed at fixed platen); 7:3 (large : small NCM) is the lowest of the five beds.
- [TextBox 20] DEM
- [Caption] < Four stages of one 7:3 bed: 0 · 47 · 296 · 165 MPa (last = relaxed) >
- [Caption] < Porosity vs large : small NCM (one bed each) >
- notes: Sources: docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md §6; docs/report_20261021/summary.json G1. Qualifiers: one bed per composition, no seed replicates; porosity = exact union of spheres; "lowest of five" is a statement about these five single beds, not an optimum ratio; the 165 MPa panel is the relaxed state at fixed platen, not an unloaded state.

## p04
- [Rectangle 4] From the contact network to Li⁺ transport
- [Rectangle 4] Kirchhoff network: each SE–SE contact = bulk resistance + Holm/Maxwell constriction using Hertz contact radii; σ₀ = 1.5 mS cm⁻¹ [8].
- [Rectangle 4] Transport tortuosity T = φ_SE σ₀ / σ_eff: 7.2 → 5.0 (0:10 → 7:3). Contact constriction accounts for 73–75 % of Joule dissipation in this network model.
- [TextBox 20] DEM
- [Placeholder] Figure pending: current pathways in the 7:3 bed (ionic, Hertz; top 50 % of current)
- [Caption] < Transport tortuosity (Hertz) >
- [Caption] < truncated y-axis — compare values >
- [Caption] < σ(Li⁺), σ₀ = 1.5 mS cm⁻¹ >
- [Caption] < truncated y-axis — compare values >
- [Caption] < Current pathways (figure pending) >
- notes: Sources: docs/data/ps45_r45_network_g2_20261007/README.md (values, σ0 = 1.5 section, decomposition section). Qualifiers: transport tortuosity T = φ_SE σ0 / σ_eff (the literature "tortuosity factor"; not its square root); Hertz H0 = primary; the 73–75 % share = ΣI²R(constriction) / ΣI²R(total) of the same FULL network solution — a model-internal ratio, not evidence that contact necks explain 75 % of a real electrode. No seed replicates for these five beds; the 7:3 vs 10:0 difference is not resolved. Pending figure: scripts/network_current.py dump <7:3 result folder> → webapp DEM 3D viewer "current flow" (same bed, same H0/FULL ionic solution, 1 V, colour = j = |I|/A; "top 50 % of current" = edges carrying the top half of the current share, not the top half by count). [8] = Bazzoun 2026 (same network approach).

## p05
- [Rectangle 4] What a fixed-shape soft-sphere DEM cannot do
- [Rectangle 4] No shape change and no yield cap: overlap is the only plasticity proxy; the softened SE modulus (1.35 vs ≈ 22 GPa) is an effective parameter, not a property [1, 7].
- [Rectangle 4] In one 7:3 bed, global viscous damping carries 58 % of the plate reaction during compression — an open issue.
- [TextBox 20] DEM
- [Lit box] Selected literature survey
- [Lit box] (22 studies; author classification)
- [Lit box] · softened SE modulus: 0/22
- [Lit box] · yield or hardness cap: 7/22
- [Lit box] · linear hysteretic law: 1/22
- [Lit box] · global damping, dry compaction: none
- [Caption] < Contact-law illustration from the implementation [1, 7] >
- notes: Sources: docs/dem_governing_equations_background_20261011.md (§5.3 figure 2; §10.3 literature counts; §11 limits). Damping share 57.9 % = measured on one 7:3 bed during compression (ledger DEMP-01, open). Literature count = selected canonical cards, our classification; not a systematic review. Bulk modulus reference ≈ 22 GPa = our DFT E_VRH 22.06 GPa (literature DEM input 22.1 GPa, Bazzoun 2026 [8]); the glass-electrolyte value 24 GPa (Sakuda 2013 [15]) is a different material system. The statement is about this implementation (fixed spherical shapes, hooke/hysteresis), not about DEM in general.

## p06
- [Rectangle 4] The material point method supplies the plastic half
- [Rectangle 4] J2 plasticity on a background grid: shape change and void filling that a fixed-shape sphere cannot represent.
- [Rectangle 4] Active material is kept rigid (DEM skeleton); only the electrolyte flows. 2D: E = 1.53 GPa, σy = 0.15 GPa; 3D: E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa.
- [TextBox 20] MPM
- [Placeholder] Figure pending: plastic SE morphology after compaction (2D)
- [Placeholder] Figure pending: 3D DEM-scaffold MPM, x–z slice (AM fixed, SE material points)
- [Caption] < 2D: SE flows into voids (figure pending) >
- [Caption] < 3D: fixed AM skeleton, plastic SE (figure pending) >
- notes: Figures to be added by the presenter (MPM renders are not tracked in the repository). Left: 2D morphology image (file outside the repository; state the 2D conditions and add a length scale). Right: python3 scripts/viz_mpm_morphology.py --se <SE material points .npy> --scaffold <AM scaffold .csv> --y 0.5 --out morphology.png (actual files required; the earlier "--slice xz" form does not match the parser). Do not present either image as an independent validation of the other. Sources: CLAUDE.md MPM sections (2026-06-07 … 06-17).

## p07
- [TextBox 20] MPM
- [Rectangle 4] Effective material inputs and their status
- [Rectangle 4] Bulk modulus from DFT; shear softening and yield stress from a pure-electrolyte calibration sweep.
- [Audit findings] Effective material inputs
- [Audit findings items] Bulk LPSCl: E ≈ 22 GPa (DFT; DEM input 22.1 GPa [8]); σy 0.05–0.30 GPa
- [Audit findings items] DEM effective: E = 1.35 GPa — reproduces compaction, not a property
- [Audit findings items] MPM: E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa; K = 25.5 ≈ DFT 26.2 GPa
- [Decisions recorded on Sep 12] Calibration target and limits
- [Decisions recorded on Sep 12 items] Calibration target: pure-SE porosity 10 % at 300 MPa (lab reference sample, unpublished)
- [Decisions recorded on Sep 12 items] Not a literature anchor; the earlier attribution was withdrawn
- [Decisions recorded on Sep 12 items] Shear-only softening keeps the real bulk modulus (ν = 0.49)
- [Conclusion] Tested alternatives (volumetric cap, real E) did not remove the need for effective parameters.
- notes: Sources: CLAUDE.md "3D MPM compaction — 3-fix calibration" (K = E/(3(1−2ν)) = 25.5 GPa vs DFT B0 26.23); our DFT E_VRH 22.06 GPa; Bazzoun 2026 [8] uses E_SE = 22.1 GPa for Li6PS5Cl; the sulfide-glass value 24 GPa (75Li2S·25P2S5, Sakuda 2013 [15]) is a different material system and is not used on the slide. σy = 0.30 GPa was selected in the pure-SE calibration sweep (0.15 → 5.6 %, 0.20 → 6.7 %, 0.25 → 9.0 %, 0.30 → 10.0 %), inside the literature range. Claims ledger CL-94: the pure-SE 10 % value is a calibration target (lab standard sample, unpublished); our earlier literature attribution was withdrawn. "Tested alternatives" = DPC volumetric cap and real-E runs (docs/mpm_dpc_cap_crosscheck.md); the statement is limited to the tested models.

## p08
- [Rectangle 4] Compaction agreement depends on initialization and loading protocol
- [Rectangle 4] Historical and current scaffold calculations differ in electrolyte initialization and loading protocol; they are not one validation series.
- [Rectangle 4] AM load sharing remains a candidate explanation for over-compaction; the final hypothesis verdict is pending.
- [TextBox 20] MPM
- [Status box] Scaffold calculations (AM skeleton from the DEM bed)
- [Status box] · Earlier: cell-filled SE, bidirectional servo — historical, not a DEM-seeded validation
- [Status box] · Current registered runs: DEM-seeded SE, fixed-platen hold — f = 0 completed; f(a) execution failed
- [Status box] · AM-load-sharing hypothesis: verdict pending
- notes: Sources: CLAUDE.md "DEM→MPM SCAFFOLD" and the 2026-09-09 correction (porosity agreement = same geometry, not independent); docs/mpm3d_calibration.md (earlier cell-filled SE, servo); docs/reviews/fam_platen_prereg_20260812.md §11 (R1 over-compaction) and §12-6-2 (f = 0 completed with I0 false; f(a) EXECUTION_FAILED; four-cell verdict unassigned). The earlier thickness agreement (30.7 vs 30.28 µm) is not shown: it comes from a different initialization and loading protocol and cannot serve as the validation value of the DEM-seeded runs (SEM-02). No figure: a side-by-side comparison requires the same initialization, loading history and state.

## p09
- [Rectangle 4] Voxelizing the compacted microstructure into a transport mesh
- [Rectangle 4] Finite-volume conservation on the phase grid gives electrical (σ, φ) and thermal (κ, T) transport on the same structure.
- [Rectangle 4] Faces are joined by a harmonic mean with no interface-resistance term: an ideal-interface voxel model — an upper bound only within the same geometry, properties and boundaries.
- [TextBox 20] Transport
- [Placeholder] Figure pending: voxelized phase grid of a compacted bed (mid-plane slice; AM · SE · pore · additives)
- [Placeholder] Figure pending: electronic current-density field at 1 V
- [Caption] < Phase grid (figure pending) >
- [Caption] < Current density at 1 V (figure pending) >
- notes: Sources: CLAUDE.md "σ 를 내는 솔버는 둘이다" table and CL-81. The voxel solver has no interface-resistance term by default (the film mechanism exists but is off): this makes it an ideal-interface model and an upper bound only for the same geometry, phase properties and boundary conditions — not a physical upper bound; geometric necks still cost resistance inside the voxel grid. The 4.04× (contact-free / full network, n = 157) is a ratio inside the contact-network model. Pending figures: STEP3 phase grid (full sid grid, origin, voxel size, phase mapping, electrode rule, run hash) and the 1 V current-density field of the same solution (A cm⁻²).

## p10
- [Rectangle 4] Additive geometry used in transport rasterization
- [Rectangle 4] Carbon fibres (VGCF) as diameter-preserving segments, PTFE as a centre-line insulator, a conductive polymer as true-diameter spheres.
- [Rectangle 4] Pre-registered 104-arm study: the electronic-conductivity order across 1–4 wt% VGCF holds across the tested voxel sizes and grid-origin offsets (72/72).
- [TextBox 20] Transport
- [Caption] < Additive seeding illustration >
- [Caption] < not a production stamp >
- [Caption] < Synthetic morphology example >
- [Caption] < not a production stamp >
- [Caption] < σ(e⁻) vs VGCF wt% at three voxel sizes >
- [Caption] < campaign values; contact resistance not included >
- notes: Sources: docs/data/phase_a_rep100_20260930/README.md (104 arms, 72/72 adjacent-composition comparisons with no threshold violation; order only is the registered estimand; increments are technical report only; replay difference 0.00000 %); docs/report_20261021 G6 (voxel σe means; contact resistance not included). Left and centre panels are illustrations (seeding schematic; synthetic preview that includes additive types not used in Phase A) — they do not demonstrate the fidelity of the production VGCF/PTFE stamps. Stamp conventions: CLAUDE.md SR-01 (sphere stamp, centerline PTFE = CL-60).

## p11
- [Rectangle 4] Problem 1: Grid dependence
- [Rectangle 4] The electronic ratio decreases across the three tested voxel spacings (0.4, 0.3, 0.25 µm); the ionic ratio crosses 1.
- [Rectangle 4] Grid convergence has not been established.
- [TextBox 20] Limits
- [Side box] No converged conductivity ratio is reported.
- [Caption] < Conductivity ratio, with / without conductive polymer, vs voxel size >
- [Caption] < same bed pair and convention >
- notes: Sources: claims ledger CL-24 (public values at vox 0.4/0.3/0.25); CL-41 (vox ≤ 0.15 values on hold — not shown); CL-72 ("lower bound" retracted). The three public points admit an exact power-law fit (three points, three parameters), so no statement about power laws or extrapolation is made from them (SEM-03); the earlier manuscript headline at 0.4 µm is superseded. Finer grids reach the memory limit of one GPU (peak RSS 35.6 GB at vox 0.115; 0.10 µm ≈ 54 GB).

## p12
- [Rectangle 4] Problem 2: Absolute electronic conductivity
- [Rectangle 4] Voxel predictions exceed the available DC-polarization estimates; measurement conditions remain unverified.
- [Rectangle 4] The NCM–SE comparison uses a common reference conductivity and a specified contact model.
- [TextBox 20] Limits
- [Caption] < Model and DC-polarization estimates — log scale >
- [Caption] < conditions not yet matched >
- [Caption] < Carbon- and binder-free NCM–SE beds; Hertz H0 contacts >
- [Caption] < common NCM reference 4.1 mS cm⁻¹ [16]; empirical size factor off; one bed per composition >
- notes: Sources: docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md (DC-polarization values 4.47 and 12.4 mS/cm, measurement conditions unverified; model 54.0 and 70.6; re-run registered, no results yet); docs/data/ps45_sigmae_factor_off_20261013/README.md (0.391 · 0.406 · 0.402 · 0.375 · 0.467 mS/cm; raw minimum 0.3747). Footnote for the right panel (Codex §6-1): computed effective electronic conductivity of the DEM particle arrangement; Hertz H0 / Holm–Maxwell constriction; common reference conductivity 4.1 mS/cm for polycrystalline and single-crystal NCM (Wang 2018 [16], SPS pellet NMC811 at 20 °C, designated reference); no empirical size factor; absolute values conditional on this reference and contact model; single bed per composition, scatter not evaluated; carbon- and binder-free AM–SE composite.

## p13
- [Rectangle 4] Problem 3: Load sharing during compaction
- [Rectangle 4] NCM–NCM contacts contribute 48–60 % of vertical stress after relaxation at fixed platen position; 7:3 is the minimum.
- [Rectangle 4] The porosity ranking agrees for the selected five compositions (exploratory comparison, n = 5).
- [TextBox 20] Limits
- [Caption] < Contribution to σ_zz by contact type >
- [Caption] < 21 planes, load-weighted; relaxed at fixed platen >
- [Caption] < SE von Mises stress, four stages >
- [Caption] < 0–150 MPa; wall SE excluded >
- notes: Sources: docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json (21-plane load-weighted AM–AM share: 59.56 · 54.63 · 52.37 · 48.46 · 56.91 % for 0:10 → 10:0; all NCM–NCM contacts, not large–large — the 0:10 bed has no large particles); state = relaxed at fixed platen (mean plane load 158–175 MPa, not the 300 MPa peak). Codex 2026-10-09 verdict: correlation observed; "springback" interpretation and stiffness inversion on hold (RB-01/RB-02); experimental thickness = selected 3-of-n average. SE stress figure: ps73 stages README §6 (wall SE excluded, linear 0–150 MPa).

## p14
- [TextBox 20] Progress
- [Rectangle 4] Registered studies and current status
- [Rectangle 4] Registered before launch, reviewed externally; the table shows the ledger state, not result claims.
- [Frame title] Study status
- [Item 1] 1.	Historical eight-origin study
- [Note 1] Conductivity estimates and inference remain on hold
- [Item 2] 2.	VGCF ordering study (104 arms)
- [Note 2] Ordering holds across tested grids and offsets (72/72)
- [Item 3] 3.	Absolute-conductivity comparison [12]
- [Note 3] R = 2.07 (Tier 1); Q = 0.84
- [Item 4] 4.	194-bed dataset v1.2
- [Note 4] Released for conditional use as model descriptors
- [Conclusion] R: model / literature conductivity. Q: conductivity retained after PTFE treatment (registered model-sensitivity prediction).
- [Item 5] 5.	Updated transport software
- [Note 5] Seven reviews completed; production remains pending
- notes: Sources: docs/reviews/sdcp_gain_prereg_v2_20260816.md — the eight-origin (voxel 0.15 µm) study: numerical ratios and the h1 inference are on hold in the claims ledger (CL-33/34/41), so no result is reported; docs/data/phase_a_rep100_20260930/README.md (104 arms; 72/72; replay 0.00000 %); docs/reviews/lee_abs_sigma_e_prereg_20260923.md §5 (R = 2.074 ± 0.004, Tier 1 "order-of-magnitude", not "within band"; Q = 0.840 = registered model-sensitivity prediction met, not an experimental hit; comparison with Lee 2025 [12]); docs/data/lhs_release_20261006_v12/README.md (v1.2 released for conditional use as model descriptors); docs/reviews/codex_review_gen2_network_reverify7_20261012.md (seven software re-verification rounds completed; the updated 194-bed production run, v1.3 and the 20-bed extension are not yet launched or approved). "Origin" = voxel-grid origin offsets of the same bed, not independent replicate beds.

## p15
- [Rectangle 4] A 194-bed design-of-experiments dataset for machine learning
- [Rectangle 4] 130 + 64 Latin-hypercube beds (composition, particle sizes) → structure and transport descriptors, released as v1.2 (conditional use as model descriptors).
- [Rectangle 4] SE percolation 106/130; geometric shortest-path tortuosity 1.3–4.2 (percolating beds; not transport tortuosity).
- [TextBox 20] Progress
- [Caption] < Geometric tortuosity vs SE fraction (130 beds) >
- [Caption] < × = no percolating SE path (24 beds) >
- [Caption] < Porosity vs SE fraction >
- [Caption] < 130 + 64 beds >
- notes: Sources: docs/data/lhs_release_20261006_v12/README.md (130 × 132 and 64 × 131; physical-target HOLD 59/130 and 62/64 — released as model descriptors, not validated physical targets); docs/report_20261021/summary.json (G5: span 106/130; finite geometric tortuosity 1.29–4.15 over the 130-bed set; G5b = ionically isolated AM, not shown). Loading is not a free design axis (derived from thickness and composition). The collaborator porosity model (OOF R² 0.99) and our five-knob fit (0.98) use unverified and different CV protocols; no comparison is claimed.

## p16
- [TextBox 20] Plan
- [Rectangle 4] Tests for unresolved model limits
- [Rectangle 4] Grid sensitivity remains unresolved. Diagnostic results exist, while final hypothesis verdicts remain pending.
- [Audit findings] Electronic transport
- [Audit findings items] Interface resistance: film model implemented, production on hold
- [Audit findings items] Carbon conductivity: comparison with DC polarization
- [Audit findings items] NCM conductivity: literature-based input review
- [Decisions recorded on Sep 12] Compaction and mixing
- [Decisions recorded on Sep 12 items] AM load sharing: final hypothesis verdict pending
- [Decisions recorded on Sep 12 items] Unloading: springback and measured thickness
- [Decisions recorded on Sep 12 items] Mixing: an adhesion parameter for SE–SE contacts
- [Conclusion] Pending: separate launch approvals for the updated 194-bed run and the 20-bed extension.
- notes: Sources: docs/reviews/contact_resistance_pipeline_draft_v3_1_20261007.md; docs/reviews/fam_platen_prereg_20260812.md §12; docs/reviews/dem_unloading_ps45_prereg_20261009.md §12–13; docs/hetero_thesis.md §4. Grid sensitivity: no new grid campaign is promised here. The updated 194-bed production run and the 20-bed extension have separate launch approvals pending (software review complete).

## p17
- [TextBox 20] Summary
- [Rectangle 4] Current findings and limitations
- [Rectangle 4] DEM and contact networks: composition trends from one bed per composition
- [Rectangle 4] MPM: plastic deformation, with compaction agreement dependent on initialization and loading protocol
- [Rectangle 4] Voxel transport: ideal-interface calculations with grid dependence and unresolved absolute conductivity
- [Rectangle 4] Final model-validation verdicts remain pending
- notes: Summary; no new numbers. No universal guarantee about registration or verification is claimed (SEM-06).

## p18
- [TextBox 20] References
- [Refs left] Contact mechanics and DEM
- [Refs left] [1] S. Luding, Granul. Matter 10, 235–246 (2008)
- [Refs left] [2] C. Thornton, Z. Ning, Powder Technol. 99, 154–162 (1998)
- [Refs left] [3] M. Paulick, M. Morgeneyer, A. Kwade, Powder Technol. 283, 66–76 (2015)
- [Refs left] [4] C.J. Coetzee, Powder Technol. 310, 104–142 (2017)
- [Refs left] [5] K. Giannis et al., Granul. Matter 23, 17 (2021)
- [Refs left] [6] W. Zunker, K. Kamrin, J. Mech. Phys. Solids 183, 105492 (2024)
- [Refs left] [7] LIGGGHTS-PUBLIC 3.8.0 (commit 3d5c00f, 2024), github.com/CFDEMproject/LIGGGHTS-PUBLIC
- [Refs left] [15] A. Sakuda, A. Hayashi, M. Tatsumisago, Sci. Rep. 3, 2261 (2013)
- [Refs right] Solid-state battery electrodes
- [Refs right] [8] A.M. Bazzoun et al., J. Power Sources 661, 238682 (2026)
- [Refs right] [9] M. So et al., J. Power Sources 508, 230344 (2021)
- [Refs right] [10] C.A. Varkey et al., Adv. Powder Technol. 37, 105338 (2026)
- [Refs right] [11] T. Shi et al., Adv. Energy Mater. 10, 1902881 (2020)
- [Refs right] [12] D.J. Lee et al., Nat. Commun. 16, 4200 (2025)
- [Refs right] [13] P. Minnmann et al., J. Electrochem. Soc. 168, 040537 (2021)
- [Refs right] [14] V. Miß, F. Lange, S. Staubitz, B. Roling, ACS Appl. Mater. Interfaces 18, 32830–32836 (2026)
- [Refs right] [16] S. Wang, M. Yan, Y. Li, C. Vinado, J. Yang, J. Power Sources 393, 75–82 (2018)
- notes: All entries are taken from the canonical literature cards (original PDFs); no bibliographic field was filled from memory. The constriction law (Holm/Maxwell) and the MLS-MPM numerical method have no canonical card yet and are cited as the models used, without a bibliographic entry.

## p19
- [TextBox 1] Thank you
- [직사각형 2] For more information or any questions, please e-mail at yonghoon71@hanyang.ac.kr

# 연구세미나 덱 v3.1 "보는 판" (Codex v3 재확인 반영) — 장별 글 전문 (생성기 출력에서 추출 · 표 · 출처 줄 · notes 포함)

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
- notes: No numbers. Calibration targets per stage: DEM — compaction experiments; MPM (material point method) — pure-electrolyte compaction (lab reference sample, unpublished); voxel transport — comparison with conductivity measurements (not yet matched). Agreement between stages that share inputs is a consistency check (SEM-01).

## p03
- [Rectangle 4] Composition-dependent porosity in five simulated beds
- [Rectangle 4] Soft-sphere DEM with a linear hysteretic contact law, pressed to 300 MPa; one bed per composition, no seed replicates.
- [Rectangle 4] One 7:3 bed: porosity 31.8 → 25.1 → 16.7 → 16.5 % (final state relaxed at fixed platen); 7:3 (large : small NCM) is the lowest of the five beds.
- [TextBox 20] DEM
- [TextBox 69] This work — DEM, five NCM–SE beds (one bed per composition)
- [picture] Fig 3D stages
- [picture] Fig porosity
- [Caption] Left: four stages of one 7:3 bed, 0 · 47 · 296 · 165 MPa (last = relaxed at fixed platen); porosity = exact union of spheres.
- [Caption] Right: final porosity of the five beds (one bed each; the red bar is the minimum).
- notes: Sources: docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md §6; docs/report_20261021/summary.json G1 (figure F_poro redrawn from the same values). Qualifiers: one bed per composition, no seed replicates; porosity = exact union of spheres; "lowest of five" is a statement about these five single beds, not an optimum ratio; the 165 MPa panel is the relaxed state at fixed platen, not an unloaded state.

## p04
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
- notes: Sources: docs/data/ps45_r45_network_g2_20261007/README.md (values, σ0 = 1.5 section, decomposition section); figure F_trans redrawn from those values (y-axes start at 0). Qualifiers: transport tortuosity T = φ_SE σ0 / σ_eff (the literature "tortuosity factor"; not its square root); Hertz H0 = primary; the 73–75 % share = ΣI²R(constriction) / ΣI²R(total) of the same FULL network solution — a model-internal ratio, not evidence that contact necks explain 75 % of a real electrode. No seed replicates for these five beds; the 7:3 vs 10:0 difference is not resolved. [8] = Bazzoun 2026 (same network approach; the crop shows their resistor-network scheme). A 3D current-pathway view of the 7:3 bed is on the transport slide (presenter figure).

## p05
- [Rectangle 4] Fixed-shape DEM limits and the material point method (MPM)
- [Rectangle 4] Our fixed-shape implementation has no shape change and no yield cap: overlap is the only plasticity proxy; the softened SE modulus (1.35 vs ≈ 22 GPa) is an effective parameter, not a property [1, 7].
- [Rectangle 4] J2 plasticity on a background grid: shape change and void filling that a fixed-shape sphere cannot represent; active material is kept rigid (DEM skeleton), only the electrolyte flows.
- [TextBox 20] DEM → MPM
- [TextBox 69] Luding 2008, Fig. 1 [1] (left) · figure: presenter — MPM 3D view of the DEM-scaffold bed (right)
- [Lit tag] Literature: hysteretic contact law [1]
- [picture] Lit Luding
- [Credit] Reproduced from Luding, Granul. Matter 10, 235 (2008), Fig. 1
- [Caption] δ = overlap; piece-wise linear loading / unloading branches;
- [Caption] the implementation used here is the LIGGGHTS hysteretic law [7]
- notes: Sources: docs/dem_governing_equations_background_20261011.md (§5.3; §10.3 literature counts; §11 limits); CLAUDE.md MPM sections (2026-06-07 … 06-17). In one 7:3 bed, global viscous damping carries 58 % of the plate reaction during compression — an open issue (damping share 57.9 % measured on one 7:3 bed during compression; ledger DEMP-01, open). Selected literature survey (22 studies; author classification, not a systematic review): softened SE modulus 0/22; yield or hardness cap 7/22; linear hysteretic law 1/22; global damping in dry compaction none. Young's modulus reference: our DFT E_VRH = 22.06 GPa (literature DEM input 22.1 GPa, Bazzoun 2026 [8]); the bulk modulus K / B0 = 26.23 GPa is a separate quantity; the glass-electrolyte value 24 GPa (Sakuda 2013 [15]) is a different material system. The DEM statement is about this implementation (fixed spherical shapes, hooke/hysteresis), not about DEM in general. MPM parameters: 2D E = 1.53 GPa, σy = 0.15 GPa; 3D E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa (next slide). Presenter figure (right, blank): MPM 3D render of the DEM-scaffold bed (AM fixed, SE material points), e.g. python3 scripts/viz_mpm_morphology.py --se <SE material points .npy> --scaffold <AM scaffold .csv> --y 0.5 --out morphology.png (actual files required; MPM renders are not tracked in the repository). Do not present the MPM image as an independent validation of the DEM bed.

## p06
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
- [Table inputs] Validation | against independent experiments: pending
- [Caption] Tested alternatives (volumetric cap, real E) did not remove the need for effective parameters.
- [Lit tag] Literature: DEM vs SE density–pressure data [9]
- [picture] Lit So
- [Credit] Reproduced from So et al., J. Electrochem. Soc. 168, 030538 (2021), Fig. 4a
- notes: Sources: CLAUDE.md "3D MPM compaction — 3-fix calibration" (K = E/(3(1−2ν)) = 25.5 GPa vs DFT B0 26.23); our DFT E_VRH 22.06 GPa; Bazzoun 2026 [8] uses E_SE = 22.1 GPa for Li6PS5Cl; the sulfide-glass value 24 GPa (75Li2S·25P2S5, Sakuda 2013 [15]) is a different material system and is not used on the slide. σy = 0.30 GPa was selected in the pure-SE calibration sweep (0.15 → 5.6 %, 0.20 → 6.7 %, 0.25 → 9.0 %, 0.30 → 10.0 %). Claims ledger CL-94: the pure-SE 10 % value is a calibration target (lab standard sample, unpublished); it is not a literature anchor — our earlier literature attribution was withdrawn. Shear-only softening (ν = 0.49) keeps K = 25.5 GPa close to the DFT reference B0 = 26.23 GPa; softening the bulk modulus over-crushed the bed. "Tested alternatives" = DPC volumetric cap and real-E runs (docs/mpm_dpc_cap_crosscheck.md); the statement is limited to the tested models. Scaffold calculations (AM skeleton from the DEM bed) — status: Earlier: cell-filled SE, bidirectional servo — historical, not a DEM-seeded validation. Current registered runs: DEM-seeded SE, stress-controlled servo — f = 0 completed; f(a) execution failed. AM-load-sharing hypothesis: verdict pending. The current statuses refer to the registered servo runs (--protocol servo; primary endpoint = final thickness after servo convergence). AM load sharing remains a candidate explanation for over-compaction; the final hypothesis verdict is pending. The earlier thickness agreement is not shown: it comes from a different initialization and loading protocol and cannot serve as the validation value of the DEM-seeded runs (SEM-02). Literature crop: So et al., J. Electrochem. Soc. 168, 030538 (2021) [9], Fig. 4a — relative density vs pressure of a sulfide SE with their contact-plasticity parameter (experimental points from Sakuda et al.): a literature example of calibrating an effective contact parameter on pure-SE compaction data.

## p07
- [Rectangle 4] Voxelizing the compacted microstructure into a transport mesh
- [Rectangle 4] Faces are joined by a harmonic mean with no interface-resistance term: an ideal-interface voxel model — an upper bound only within the same geometry, properties and boundaries.
- [Rectangle 4] VGCF as diameter-preserving segments, PTFE as a centre-line insulator, polymer as spheres; a registered 104-arm study keeps the σ(e⁻) order across 1–4 wt% VGCF on all tested grids (72/72).
- [TextBox 20] Transport
- [TextBox 69] figure: presenter — 3D current-flow views, contact network and voxel (left) · this work, 104-arm study (right)
- [picture] Fig VGCF
- [Caption] Original Phase A campaign (VGCF E = 10 GPa): means of 96 primary arms,
- [Caption] three voxel sizes; no contact resistance
- notes: Sources: CLAUDE.md "σ 를 내는 솔버는 둘이다" table and CL-81. Finite-volume conservation on the phase grid gives electrical (σ, φ) and thermal (κ, T) transport on the same structure. The voxel solver has no interface-resistance term by default (the film mechanism exists but is off): this makes it an ideal-interface model and an upper bound only for the same geometry, phase properties and boundary conditions — not a physical upper bound; geometric necks still cost resistance inside the voxel grid. The 4.04× (contact-free / full network, n = 157) is a ratio inside the contact-network model. Additives: carbon fibres (VGCF) as diameter-preserving segments, PTFE as a centre-line insulator, a conductive polymer as true-diameter spheres. Pre-registered 104-arm study: the electronic-conductivity order across 1–4 wt% VGCF holds across the tested voxel sizes and grid-origin offsets (72/72) — docs/data/phase_a_rep100_20260930/README.md (104 arms, 72/72 adjacent-composition comparisons with no threshold violation; order only is the registered estimand; increments are technical report only; replay difference 0.00000 %); docs/report_20261021 G6 (voxel σe means; contact resistance not included; figure F_vgcf redrawn from G6). The plotted means are the original campaign (VGCF E = 10 GPa, docs/data/phase_a_104arms_20260921); the 100 GPa replication (docs/data/phase_a_rep100_20260930) also keeps the order 72/72 with slightly different means, so the plotted values are not the 100 GPa means. Stamp conventions: CLAUDE.md SR-01 (sphere stamp, centerline PTFE = CL-60). Presenter figures (left, blank): (i) contact-network current pathways of the 7:3 bed — scripts/network_current.py dump <7:3 result folder> → webapp DEM 3D viewer "current flow" (same bed, same H0/FULL ionic solution, 1 V, colour = j = |I|/A; "top 50 % of current" = edges carrying the top half of the current share, not the top half by count); (ii) STEP3 phase grid and the 1 V current-density field of the same voxel solution (A cm⁻²; state origin, voxel size, phase mapping, electrode rule, run hash).

## p08
- [Rectangle 4] Problems 1 and 2: grid dependence and absolute σ(e⁻)
- [Rectangle 4] The electronic ratio decreases across the three tested voxel spacings (0.4, 0.3, 0.25 µm); the ionic ratio crosses 1. Grid convergence has not been established.
- [Rectangle 4] Voxel predictions exceed the available DC-polarization estimates; measurement conditions remain unverified. The NCM–SE comparison uses a common reference conductivity and a specified contact model.
- [TextBox 20] Limits
- [TextBox 69] This work — voxel transport solver (a, b) · contact network, five NCM–SE beds (c)
- [picture] Fig limits
- [Caption] (a) Grid dependence: same bed pair and convention; no converged conductivity ratio is reported.
- [Caption] (b) Voxel model vs DC polarization, log scale; conditions not yet matched.
- [Caption] (c) NCM–SE beds: no carbon/binder; Hertz H0; common NCM reference 4.1 mS cm⁻¹ [16]; size factor off; one bed per composition.
- notes: Sources: claims ledger CL-24 (public values at vox 0.4/0.3/0.25); CL-41 (vox ≤ 0.15 values on hold — not shown); CL-72 ("lower bound" retracted). The three public points admit an exact power-law fit (three points, three parameters), so no statement about power laws or extrapolation is made from them (SEM-03); the earlier manuscript headline at 0.4 µm is superseded. Finer grids reach the memory limit of one GPU (peak RSS 35.6 GB at vox 0.115; 0.10 µm ≈ 54 GB). Panel (b): docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md (DC-polarization values 4.47 and 12.4 mS/cm, measurement conditions unverified; model 54.0 and 70.6; re-run registered, no results yet). Panel (c): docs/data/ps45_sigmae_factor_off_20261013/README.md (0.391 · 0.406 · 0.402 · 0.375 · 0.467 mS/cm; raw minimum 0.3747). Footnote (Codex §6-1): computed effective electronic conductivity of the DEM particle arrangement; Hertz H0 / Holm–Maxwell constriction; common reference conductivity 4.1 mS/cm for polycrystalline and single-crystal NCM (Wang 2018 [16], SPS pellet NMC811 at 20 °C, designated reference); no empirical size factor; absolute values conditional on this reference and contact model; single bed per composition, scatter not evaluated; carbon- and binder-free AM–SE composite.

## p09
- [Rectangle 4] Problem 3: Load sharing during compaction
- [Rectangle 4] NCM–NCM contacts contribute 48–60 % of vertical stress after relaxation at fixed platen position; 7:3 is the minimum.
- [Rectangle 4] The NCM–NCM stress-share ranking matches the experimental porosity summaries for the selected five compositions (exploratory, n = 5).
- [TextBox 20] Limits
- [TextBox 69] This work — DEM, five beds (left) · one 7:3 bed, four stages (right)
- [picture] Fig load share
- [picture] Fig SE von Mises
- [Caption] Left: contribution to σ_zz by contact type, 21 planes, load-weighted; relaxed at fixed platen.
- [Caption] Right: SE von Mises stress in one 7:3 bed, four stages (0 · 47 · 296 · 165 MPa), 0–150 MPa; wall SE excluded.
- notes: Sources: docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json (21-plane load-weighted shares; figure F_load redrawn from contribution_sigma_zz_pct: NCM–NCM 59.56 · 54.63 · 52.37 · 48.46 · 56.91 % for 0:10 → 10:0; all NCM–NCM contacts, not large–large — the 0:10 bed has no large particles); state = relaxed at fixed platen (mean plane load 158–175 MPa, not the 300 MPa peak). Codex 2026-10-09 verdict: correlation observed; "springback" interpretation and stiffness inversion on hold (RB-01/RB-02); experimental thickness = selected 3-of-n average. SE stress figure: ps73 stages README §6 (wall SE excluded, linear 0–150 MPa). A 3D view of NCM particle stress / force chains of the same bed can be added by the presenter from the webapp.

## p10
- [Rectangle 4] Registered studies and a 194-bed dataset for machine learning
- [Rectangle 4] The table summarizes the current status of each registered study.
- [Rectangle 4] 130 + 64 Latin-hypercube beds (composition, particle sizes) → structure and transport descriptors, released as v1.2 (conditional use as model descriptors).
- [TextBox 20] Progress
- [TextBox 69] This work — registered studies (left) · dataset v1.2 (right)
- [Table studies] Registered study | Status
- [Table studies] Historical eight-origin study | Conductivity estimates and inference remain on hold
- [Table studies] VGCF ordering study (104 arms) | Ordering holds across tested grids and offsets (72/72)
- [Table studies] Absolute-conductivity comparison [12] | R = 2.07 (order-of-magnitude agreement); Q = 0.84
- [Table studies] 194-bed dataset v1.2 | Released for conditional use as model descriptors
- [Table studies] Updated transport software | Seven reviews completed; production remains pending
- [Caption] R: model / literature conductivity. Q: conductivity retained after PTFE treatment
- [Caption] (registered model-sensitivity prediction).
- [picture] Fig dataset
- [Caption] (a) geometric tortuosity, 130 + 64 beds; ×: 24 non-percolating beds in the
- [Caption] 130-bed set (display position only); not transport tortuosity · (b) porosity, 130-bed set
- notes: Sources: docs/reviews/sdcp_gain_prereg_v2_20260816.md — the eight-origin (voxel 0.15 µm) study: numerical ratios and the h1 inference are on hold in the claims ledger (CL-33/34/41), so no result is reported; docs/data/phase_a_rep100_20260930/README.md (104 arms; 72/72; replay 0.00000 %); docs/reviews/lee_abs_sigma_e_prereg_20260923.md §5 (R = 2.074 ± 0.004, Tier 1 "order-of-magnitude", not "within band"; Q = 0.840 = registered model-sensitivity prediction met, not an experimental hit; comparison with Lee 2025 [12]); docs/data/lhs_release_20261006_v12/README.md (130 × 132 and 64 × 131; physical-target HOLD 59/130 and 62/64 — released as model descriptors, not validated physical targets; figure F_dataset drawn from the released CSV columns se_of_solid_vol, tortuosity_SE_wall, porosity_union_exact_pct); docs/reviews/codex_review_gen2_network_reverify7_20261012.md (seven software re-verification rounds completed; the updated 194-bed production run, v1.3 and the 20-bed extension are not yet launched or approved). "Origin" = voxel-grid origin offsets of the same bed, not independent replicate beds. In the 130-bed set: SE percolation 106/130; geometric shortest-path tortuosity 1.3–4.2 (percolating beds; not transport tortuosity); 64-bed set 1.3–1.6. Loading is not a free design axis (derived from thickness and composition). The collaborator porosity model (OOF R² 0.99) and our five-knob fit (0.98) use unverified and different CV protocols; no comparison is claimed.

## p11
- [Rectangle 4] Layered-bed mixing: unresolved mixing-index contrast
- [Rectangle 4] Rotating-drum DEM, cohesive soft contacts: ten runs from a layered start, eight revolutions; Lacey index M on 16×16×4 bins vs a random reference.
- [Rectangle 4] Low NCM–NCM cohesion versus the reference setting gives an unresolved paired contrast at 16×16×4 bins (ΔM = 0.0012, seed SE = 0.0073). Subsequent diagnostic classification; the original 1% overlap condition was not met.
- [TextBox 20] Mixing
- [TextBox 69] This work (left) · figure: presenter — bed view, layered start and after eight revolutions (right)
- [picture] Fig mixing index
- [Caption] M = 1: random-reference variance; error bars = within-run SD; all ten runs reach M ≈ 0.96–1.00,
- [Caption] so this bin grid cannot separate the settings
- notes: Sources: docs/reviews/mixer_layered_prereg_20260921.md §2 (verdict line), §5 (report wording), §6 (readout 2026-09-30); docs/data/mixer_final10_20260930/ (ten runs; figure F_mix1 redrawn from the registered final values, report_20261021 G7). Registered estimand: paired contrast of the final Lacey index between the low NCM–NCM cohesion setting (small but nonzero: CED 108,795 and 142,562 J m⁻³ for the large and small NCM self-pairs; model Bond number 0.00109 and 0.00553) and the reference setting (model Bond number 3.0), three seeds, 16×16×4 bins: Δ = +0.0012, seed-to-seed SE 0.0073 ⇒ |Δ| ≤ SE. The numerical rule maps this contrast to the registered "no segregation" category. This does not establish compliance with the original registration, equivalence, or a physical absence of segregation (this model, this drum, the tested inputs and this bin convention). Coarser grids (report only): 12×12×3 Δ −0.0156, SE 0.0058 (ambiguous); 8×8×2 Δ +0.0081, SE 0.0144. Negative control (no cohesion): M ≥ 0.8 in all three grids; floor check 10/10; flatness 30/30; QC 30/30. The two cohesion matrices differ in NCM–NCM and NCM–wall adhesion together; the comparison is not a reproduction of real coating or of powder flowability. Contract qualifier (Codex wording, 2026-09-28): the result is a comparison of mixing indices after eight revolutions in the specified soft-contact model; in the reference state the maximum stored-frame overlap was 4.7–5.8 % particle–particle and 4.5–5.7 % at the wall, so the registered 1 % condition was not met; the effect of the overlap error on the mixing index has not been verified. Conditions: three phases, 100,000 particles, drum radius 13.1 mm, 75 rpm. Presenter figure (right, blank): bed view of one run, layered start and after eight revolutions (webapp bed view; display only).

## p12
- [Rectangle 4] Exploratory cohesion settings produce different mixing indices
- [Rectangle 4] One seed, two revolutions: large-NCM self-pair model Bond number 38.4, 384, 1152, or all nonzero cohesion-energy densities ×10 and ×14.42 (vs the low-cohesion comparator).
- [Rectangle 4] Within each series ΔM rises with the imposed level; levels were chosen post hoc, and wall adhesion and start states also differ — no verdict.
- [TextBox 20] Mixing
- [TextBox 69] This work (left) · figure: presenter — low versus higher NCM cohesion, two revolutions (right)
- [picture] Fig cohesion exploration
- [Caption] ΔM = M(low-cohesion comparator) − M(setting); hatched: bin grid failed the volume-coverage check;
- [Caption] ΔM includes start-state differences; M < 0 lies outside the Lacey range
- notes: Sources: docs/data/mixer_highbo_devrot_prelim_20261002/, mixer_highbo_devbo_prelim_20261003/, mixer_highbo_devu_prelim_20261006/ (README and readout JSONs; development data; one seed per arm; two revolutions; no pass/fail line; not used for any verdict; not mixed with the confirmatory seeds). Two series, defined separately: (i) the model Bond number of the large-NCM self-pair (code convention: equilibrium cohesive force / particle weight) 38.4 → 384 → 1152 — the large-NCM cohesion energy density rises only 3.56348e6 → 7.67728e6 → 1.10725e7 J m⁻³ (×2.154, ×3.107); (ii) all nine nonzero cohesion-energy-density entries of the low-cohesion comparator multiplied by 10 and 14.42. ΔM = M(low-cohesion comparator) − M(setting), bins 16×16×4 / 12×12×3 / 8×8×2: NCM-pair Bo 38.4 +0.010 / −0.006 / +0.008 · Bo 384 +0.827 / +0.927 / +0.988 · Bo 1152 +1.876 / +2.432 / +3.164 · all-pair CED ×10 +0.239 / +0.165 / +0.103 · CED ×14.42 +0.865 / +0.484 / +0.267. The 16×16×4 cells of NCM-pair Bo 384 and 1152 and of all-pair CED ×14.42 failed the volume-coverage check. M of the NCM-pair Bo 1152 setting is −0.968 / −1.407 / −2.283 (outside the Lacey range [0, 1]); start-state variances differ between settings, so ΔM mixes a start-state difference with the post-rotation difference. Cohesion levels were selected after earlier runs (post hoc); every setting uses the same development seed. NCM–NCM and NCM–wall adhesion change together. All exploratory decks share the stiffened SE modulus (2e8 Pa); compare with the original soft campaign only with that generation noted. The low-cohesion comparator is small but nonzero (CED 108,795 and 142,562 J m⁻³ for the large and small NCM self-pairs). No sentence about real coating effects or real powders is made. Presenter figure (right, blank): bed snapshots of the low-cohesion comparator vs a higher-cohesion setting after two revolutions (webapp bed view).

## p13
- [Rectangle 4] Surface energy and coating: SE–SE adhesion is the open term
- [Rectangle 4] With equal contact areas and an assumed geometric-mean adhesion rule, ΔW = 2(√γ_A − √γ_S)² ≥ 0 is an adhesive-work difference per unit area; SE–SE cluster survival also depends on relative surface energies and contact dynamics.
- [Rectangle 4] Exploratory all-pair CED scaling retains a larger SE–SE cluster fraction than the low-cohesion comparator; the confirmatory 18-run block remains on hold.
- [TextBox 20] Mixing
- [TextBox 69] This work: exploratory contact statistics (left), conditional adhesion model (right)
- [picture] Fig SE clusters
- [picture] Fig adhesion scheme
- [Caption] Left: one seed, mean over the second revolution; whiskers = dump-resolution range, not a confidence interval.
- [Caption] Right: γ = surface energy, W = work of adhesion; the uncoated NCM / SE surface-energy ratio is not known.
- notes: Sources: docs/hetero_thesis.md (ratified 2026-10-05) §2-1 · §2-2 · §2-8. With W_AA = 2γ_A, W_SS = 2γ_S and an assumed geometric-mean rule W_AS = 2√(γ_A γ_S), ΔW = W_AA + W_SS − 2 W_AS = 2(√γ_A − √γ_S)² ≥ 0 (J m⁻²) is a per-area comparison at equal contact areas (ΔU = −A·ΔW for a common area A); real exchanges also change contact areas, deformation energy and dynamics, so contact counts alone do not fix the sign of the released energy. Pull-off force (JKR) scales with W·R*: at equal W the weight-normalized SE–SE adhesion is about 194× that of the large-NCM self-pair (arithmetic estimate), but for one SE particle the SE–NCM pull-off exceeds SE–SE by 2r_NCM/(r_NCM + r_SE) = 1.8 (large NCM) and 1.6 (small NCM). Under the geometric-mean rule the SE–SE pull-off exceeds the SE–large-NCM pull-off only if γ_NCM/γ_SE < 0.309 (small NCM: 0.391) — a two-contact force comparison, not a necessary or sufficient condition for cluster survival; that ratio is not known (open decision). Predictions P1–P3 of the thesis: uncoated beds keep SE–SE clustering above random; coating removes it; the mixing difference carries into the compacted SE pathway. The all-pair CED runs also scale SE–SE cohesion; the model is not calibrated to measured surface energies or coating selectivity, so the CED-scaling runs do not validate a surface-energy-based coating mechanism. Left figure: docs/data/mixer_highbo_devu_prelim_20261006/devu_contact.json — fraction of SE in SE–SE clusters (second revolution, 100 frames): 0.400 [0.143, 0.542] low NCM–NCM cohesion; 0.954 [0.875, 0.957] all-pair CED ×10; 0.988 [0.981, 0.988] all-pair CED ×14.42 (ranges = dump-resolution [certain, possible], not confidence intervals; one seed; development data; the lower bounds of the two higher settings exceed the comparator upper bound). Confirmatory 18-run block: registered, on hold after the Codex rounds (docs/reviews/mixer_highbo_prereg_20260927.md).

## p14
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

## p15
- [TextBox 20] Summary
- [Rectangle 4] Current findings and limitations
- [Rectangle 4] DEM and contact networks: composition trends from one bed per composition
- [Rectangle 4] MPM: plastic deformation, with compaction agreement dependent on initialization and loading protocol
- [Rectangle 4] Voxel transport: ideal-interface calculations with grid dependence and unresolved absolute conductivity
- [Rectangle 4] Mixing: unresolved diagnostic mixing-index contrast under an unmet overlap condition; exploratory cohesion results without a verdict
- [Rectangle 4] Final model-validation verdicts remain pending
- notes: Summary; no new numbers. No universal guarantee about registration or verification is claimed (SEM-06).

## p16
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
- [Refs right] [9] M. So et al., J. Electrochem. Soc. 168, 030538 (2021)
- [Refs right] [10] C.A. Varkey et al., Adv. Powder Technol. 37, 105338 (2026)
- [Refs right] [11] T. Shi et al., Adv. Energy Mater. 10, 1902881 (2020)
- [Refs right] [12] D.J. Lee et al., Nat. Commun. 16, 4200 (2025)
- [Refs right] [13] P. Minnmann et al., J. Electrochem. Soc. 168, 040537 (2021)
- [Refs right] [14] V. Miß, F. Lange, S. Staubitz, B. Roling, ACS Appl. Mater. Interfaces 18, 32830–32836 (2026)
- [Refs right] [16] S. Wang, M. Yan, Y. Li, C. Vinado, J. Yang, J. Power Sources 393, 75–82 (2018)
- notes: All entries are taken from the canonical literature cards (original PDFs); no bibliographic field was filled from memory. The constriction law (Holm/Maxwell) and the MLS-MPM numerical method have no canonical card yet and are cited as the models used, without a bibliographic entry. Literature crops on slides 4–6 are reproduced from the papers of [8], [1] and [9] (canonical figure crops).

## p17
- [picture] Picture 2
- [TextBox 1] Thank you
- [직사각형 2] For more information or any questions, please e-mail at yonghoon71@hanyang.ac.kr

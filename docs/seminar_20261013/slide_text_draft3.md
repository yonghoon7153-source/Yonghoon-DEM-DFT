# 연구세미나 덱 — 장별 글 전문 (생성기 출력 · draft 3 · 2026-10-13)

> 덱 pptx 는 리포 밖 (사용자 덱 미반입 규약) — 이 파일이 글의 정본 사본이다.  `[Figure to add]` = 리포에 없는 그림 자리 (채울 내용 · 출처 · 명령).

## Slide 1
- **직사각형 10**: Yonghoon An /  / Division of Materials Science & Engineering, Hanyang University / (E-mail : yonghoon71@hanyang.ac.kr)
- **직사각형 12**: [date — to be set]
- **Rectangle 4**: Research Seminar / Particle-resolved multiscale simulation of sulfide all-solid-state composite cathodes: / from powder packing to transport
- picture: 그림 2
- picture: 그림 3
- notes: Title. Date to be set by the presenter.

## Slide 2
- **Rectangle 4**: Heterogeneous-technology pipeline for a sulfide composite cathode / Three particle-level stages, each calibrated to its own experiment — never to one another. / Agreement between stages is treated as cross-validation; disagreement as a quantified model limit.
- **TextBox 20**: Introduction
- picture: Picture 21
- **Caption**: < DEM → MPM → voxel transport → electrode response >
- notes: No numbers. Source: project framing document (DEM/MPM complementary frame, finalized 2026-06-07).

## Slide 3
- **Rectangle 4**: Soft-sphere DEM reproduces the composition dependence of porosity / Rigid spheres with a linear hysteretic contact law, pressed to 300 MPa; one bed per composition. / Porosity 31.8 → 25.1 → 16.7 → 16.5 % through one run; 7:3 (large : small NCM) is the densest of five.
- **TextBox 20**: DEM
- picture: Picture 21
- picture: Picture 22
- **Caption**: < four stages of one 7:3 bed (0 · 47 · 296 · 165 MPa) >
- **Caption**: < porosity vs large : small NCM >
- notes: Sources: docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md §6; docs/report_20261021/summary.json G1. Qualifier: one bed per composition, no seed replicates; porosity = exact union of spheres.

## Slide 4
- **Rectangle 4**: From the contact network to Li⁺ transport: a Kirchhoff network with contact constriction / Each SE–SE contact = bulk resistance + Hertz constriction; σ₀ = 1.5 mS cm⁻¹ (pellet literature range). / Transport tortuosity 7.2 → 5.0 (0:10 → 7:3): 73–75 % of the resistance sits in the contact necks, not in path length.
- **TextBox 20**: DEM
- picture: Picture 21
- picture: Picture 22
- **figure placeholder**: Figure to add / Current pathways in the 7:3 bed (3D, ionic, Hertz, top 50 % of current) / webapp DEM 3D viewer "current flow" after scripts/network_current.py dump <ps45 7:3 result folder> / command to be run by the presenter (WSL); capture at the same camera as the geometry panels
- **Caption**: < transport tortuosity (Hertz) >
- **Caption**: < σ(Li⁺), σ₀ = 1.5 mS cm⁻¹ >
- **Caption**: < actual current pathways >
- notes: Sources: docs/data/ps45_r45_network_g2_20261007/README.md (values, σ0 = 1.5 section, decomposition section). Qualifiers: transport tortuosity = φ_SE σ0 / σ_eff (not its square root); Hertz = primary; the 73–75 % share and the path-only tortuosity 1.25–1.79 are model-internal ratios, not a measured decomposition; 7:3 vs 10:0 difference is within seed scatter.

## Slide 5
- **Rectangle 4**: What a rigid-sphere DEM cannot do / No shape change and no yield cap: overlap is the only proxy for plasticity, so the 18× softened SE modulus (24 → 1.35 GPa) is a surrogate, not a property. / During compression, global viscous damping carries 58 % of the plate reaction in one 7:3 bed — an open issue.
- **TextBox 20**: DEM
- picture: Picture 21
- **Lit box**: Battery-electrode DEM literature (22 studies) / · softened SE modulus: 0 of 22 / · yield / hardness cap: 7 of 22 / · linear hysteretic law: 1 of 22 / · global damping during dry compaction: none reported
- **Caption**: < hysteretic normal force (code reproduction) >
- notes: Sources: docs/dem_governing_equations_background_20261011.md (§5.3 figure 2; §10.3 literature counts; §11 limits). Damping share 57.9 % = measured on the ps45 7:3 bed during compression (ledger DEMP-01, open). Literature count = canonical cards, our classification.

## Slide 6
- **Rectangle 4**: The material point method supplies the plastic half / J2 plasticity on a background grid: true shape change and void filling that a rigid sphere cannot represent. / Active material is kept rigid (DEM skeleton); only the electrolyte flows.
- **TextBox 20**: MPM
- **figure placeholder**: Figure to add / Plastic SE morphology after compaction (2D champion, E = 1.53 GPa, σy = 0.15 GPa) / uma: ~/work/mpm/vis_/viszoom_E1.53_sy0.15.png (not in repo) / copy the PNG into the deck folder; same scale bar as the right panel
- **figure placeholder**: Figure to add / 3D DEM-scaffold MPM, x–z slice (AM fixed, SE material points) / scripts/viz_mpm_morphology.py on the real_14 scaffold run (payload not in repo) / python3 scripts/viz_mpm_morphology.py <mpm run dir> --slice xz
- **Caption**: < 2D: SE flows into voids >
- **Caption**: < 3D: fixed AM skeleton, plastic SE >
- notes: Figures to be added by the presenter (MPM renders are not tracked in the repository). Sources: CLAUDE.md MPM sections (2026-06-07 … 06-17).

## Slide 7
- **TextBox 20**: MPM
- **Rectangle 4**: How the electrolyte parameters were fixed / Bulk modulus from DFT; shear softening calibrated to pure-electrolyte compaction; yield stress from the LPSCl literature range.
- **Audit findings**: Three layers of the SE model
- **Audit findings items**: Real bulk: E ≈ 24 GPa, σy 0.05–0.30 GPa (single-crystal LPSCl range) / DEM effective: E = 1.35 GPa (18× softened) — reproduces compaction, not a property / MPM: E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa; K = 25.5 GPa ≈ DFT bulk modulus 26.2 GPa
- **Decisions recorded on Sep 12**: What is — and is not — an external anchor
- **Decisions recorded on Sep 12 items**: Pure-SE porosity 10 % at 300 MPa is the calibration target: a lab reference sample, unpublished / It is not a literature anchor; the earlier citation was retracted / Shear-only softening keeps the real bulk modulus (ν = 0.49); softening the bulk over-crushed the bed
- **Conclusion**: The softening is irreducible for a resolved-grain continuum — a volumetric cap and real E both failed the Heckel test.
- notes: Sources: CLAUDE.md "3D MPM compaction — 3-fix calibration" (K = E/(3(1−2ν)) = 25.5 GPa vs DFT B0 26.23); claims ledger CL-94 (pure-SE 10 % is a calibration target; the Minnmann citation was retracted); 2026-10-08 note: the 10 % value is a lab standard sample, unpublished. "Heckel test" = DPC/jamming cross-check (docs/mpm_dpc_cap_crosscheck.md).

## Slide 8
- **Rectangle 4**: DEM-scaffold MPM: what agrees, and what does not count as evidence / Stress-stop thickness agrees (30.7 vs 30.3 µm); porosity agreement is not independent — the AM skeleton and the SE seeds both come from the DEM bed. / Pressed honestly to 300 MPa the MPM over-compacts (sphere porosity 1.1 % vs 15.6 % measured): AM load sharing is the missing piece.
- **TextBox 20**: MPM
- **figure placeholder**: Figure to add / DEM-scaffold MPM at the stress stop: x–z slice with the DEM bed side by side (same scale) / scripts/viz_mpm_morphology.py (scaffold run real_14, n_grid 384) + DEM dump atom_2060000 (docs/data/real14_reference_20260928) / render both at the same camera; label thickness 30.7 vs 30.28 µm
- notes: Sources: CLAUDE.md "DEM→MPM SCAFFOLD" (thickness 30.7 vs 30.28 µm) and the 2026-09-09 correction (porosity agreement = same geometry, not independent); docs/reviews/fam_platen_prereg_20260812.md §11 (R1: ε_sphere 1.125 %, experiment 15.6 %, 14.5 %p over-compaction). Figure to be added.

## Slide 9
- **Rectangle 4**: Voxelizing the compacted microstructure turns morphology into a transport mesh / Finite-volume ∇·(σ∇φ) = 0 on the phase grid gives ionic, electronic and thermal conductivity on the same structure. / Faces are joined by a harmonic mean, so there is no interface-resistance term: the voxel solver sits on the contact-free branch.
- **TextBox 20**: Transport
- **figure placeholder**: Figure to add / Voxelized phase grid of a compacted bed (AM · SE · pore · additives) / STEP3 phase grid from the MPM payload (scripts/step3_sigma.py); manuscript Fig. S16/S17 style / export a mid-plane slice of the sid grid (phase colours) at vox 0.15 µm
- **figure placeholder**: Figure to add / Electronic current-density field at 1 V (manuscript S16/S17) / manuscript SI figures (rendered by the presenter, outside the repository) / reuse the S16/S17 panels; colourbar in A cm⁻²
- **Caption**: < phase grid >
- **Caption**: < current density at 1 V >
- notes: Sources: CLAUDE.md "σ 를 내는 솔버는 둘이다" table and CL-81 note (voxel FV = CONTACT_FREE branch; the 4.04× median is a model-internal ratio over 157 cases). Figures to be added.

## Slide 10
- **Rectangle 4**: Additives enter at the voxel stage / Carbon fibres (VGCF) as diameter-preserving segments, PTFE as a centre-line insulator, a conductive polymer as true-diameter spheres. / A 104-arm pre-registered run: the electronic-conductivity order across 1–4 wt% VGCF is robust to voxel size and origin shift (72/72).
- **TextBox 20**: Transport
- picture: Picture 21
- picture: Picture 22
- picture: Picture 23
- **Caption**: < fibre + binder seeds >
- **Caption**: < additive stamps >
- **Caption**: < σ(e⁻) vs VGCF wt%, three voxel sizes >
- notes: Sources: docs/data/phase_a_rep100_20260930/README.md (104 arms, 72/72, order only is the registered estimand; increments are technical report only); docs/report_20261021 G6 (voxel σe means; contact resistance not included). Stamp conventions: CLAUDE.md SR-01 (sphere stamp, centerline PTFE = CL-60).

## Slide 11
- **Rectangle 4**: Problem 1 — the voxel electronic gain is grid-dependent and does not extrapolate / Same bed pair, same convention, voxel 0.4 → 0.3 → 0.25 µm: the electronic ratio keeps falling and the ionic ratio changes sign. / The increments follow no power law — no Richardson extrapolation, and no lower-bound claim either.
- **TextBox 20**: Limits
- picture: Picture 21
- **Side box**: What survives / · the headline of the earlier manuscript draft is a grid artefact / · the shape (monotonic, decelerating) is real; no converged value yet / · finer grids reach the memory limit of one GPU
- **Caption**: < conductivity ratio vs voxel size >
- notes: Sources: claims ledger CL-24 (public values at vox 0.4/0.3/0.25); CL-41 (vox ≤ 0.15 values on hold — not shown); CL-72 ("lower bound" retracted). Memory: peak RSS 35.6 GB at vox 0.115; 0.10 µm needs ≈ 54 GB.

## Slide 12
- **Rectangle 4**: Problem 2 — absolute electronic conductivity sits far above DC-polarization measurements / Voxel model 54 and 71 vs 4.5 and 12 mS cm⁻¹ measured (×12, ×5.7): no interface resistance, unanchored carbon conductivity. / Carbon- and binder-free NCM–SE beds, common NCM reference 4.1 mS cm⁻¹: 0.38–0.47 mS cm⁻¹ across the five compositions.
- **TextBox 20**: Limits
- picture: Picture 21
- picture: Picture 22
- **Caption**: < voxel model vs experiment (log scale) >
- **Caption**: < NCM–SE beds, common-conductivity network >
- notes: Sources: docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md (experimental values from DC polarization, conditions unverified; re-run registered, no results yet); docs/data/ps45_sigmae_factor_off_20261013/README.md. Footnote for the right panel (Codex §6-1): computed effective electronic conductivity of the DEM particle arrangement; Hertz H0 / Maxwell constriction; common reference conductivity 4.1 mS/cm for polycrystalline and single-crystal NCM (sintered-pellet literature ≈ 4 mS/cm at 20 °C, designated reference); no empirical size factor; absolute values conditional on this reference and contact model; single bed per composition, scatter not evaluated; carbon- and binder-free AM–SE composite.

## Slide 13
- **Rectangle 4**: Problem 3 — compaction mechanics: over-compaction and load sharing / Large–large NCM contacts carry 48–60 % of the vertical stress; 7:3 is the minimum. / Its five-composition order matches the measured porosity order (n = 5, exploratory; the experimental set is a selected subset).
- **TextBox 20**: Limits
- picture: Picture 21
- picture: Picture 22
- **Caption**: < contribution to σzz by contact type >
- **Caption**: < SE von Mises stress, four stages (0–150 MPa) >
- notes: Sources: docs/data/ps45_plane_load_20261007/README.md (21-plane load-weighted average); Codex 2026-10-09 verdict (correlation observed, "springback" interpretation and stiffness inversion on hold, RB-01/RB-02); experimental thickness = selected 3-of-n average (2026-10-09 note). SE stress figure: ps73 stages README §6.

## Slide 14
- **TextBox 20**: Progress
- **Rectangle 4**: Pre-registered, origin-replicated runs — what each one settled / Every production run is registered before launch (hypotheses, decision lines, sealed code) and judged by an independent reviewer.
- **Frame title**: Registered campaigns
- **Item 1**: 1.	8-arm origin factorial, voxel 0.15 µm
- **Note 1**: gain follows the represented additive volume (procedure and verdict only)
- **Item 2**: 2.	Phase A: 104 arms, VGCF 1–4 wt%
- **Note 2**: order robust, 72/72; replay 0.00000 %
- **Item 3**: 3.	Lee-2025 absolute comparison, 16 arms
- **Note 3**: R = 2.07 → order-of-magnitude agreement; Q = 0.84 → prediction met
- **Item 4**: 4.	194 LHS beds → descriptor dataset v1.2
- **Note 4**: sealed pipeline; 7 external re-verification rounds before launch
- **Conclusion**: Ratios and gains of the 8-arm series are on hold — only the procedure and the verdict are reported.
- notes: Sources: docs/reviews/sdcp_gain_prereg_v2_20260816.md (verdict h1 = gain follows represented SDCP volume; numeric ratios on hold); docs/data/phase_a_rep100_20260930/README.md; docs/reviews/lee_abs_sigma_e_prereg_20260923.md §5 (R = 2.074 ± 0.004, Tier 1 "order-of-magnitude", not "within band"; Q = 0.840); docs/data/lhs_release_20261006_v12/README.md.

## Slide 15
- **Rectangle 4**: A 194-bed design-of-experiments dataset for machine learning / 130 + 64 Latin-hypercube beds (composition, particle sizes, loading) → structure and transport descriptors, released as v1.2. / SE percolation 106/130; geometric tortuosity 1.3–4.2 (shortest path, not transport); porosity OOF R² 0.99 (collaborator) vs 0.98 from the five design knobs.
- **TextBox 20**: Progress
- picture: Picture 21
- picture: Picture 22
- picture: Picture 23
- **Caption**: < geometric tortuosity >
- **Caption**: < ionically isolated AM >
- **Caption**: < porosity vs SE fraction >
- notes: Sources: docs/data/lhs_release_20261006_v12/README.md; docs/report_20261021/summary.json (G5: span 106/130, tau 1.29–4.15); docs/data/lhs_ml_crosscheck_20261005/README.md. Qualifier: wall-based tortuosity is geometric (Dijkstra), not transport tortuosity.

## Slide 16
- **TextBox 20**: Plan
- **Rectangle 4**: Next steps — closing the three problems / Each item is registered before it is run; nothing below has a result yet.
- **Audit findings**: Transport
- **Audit findings items**: Interface resistance in the voxel solver: AM–AM film implemented (default off), production on hold / Anchor the carbon conductivity with the SBE/DBE DC-polarization values (re-run registered) / Polycrystalline vs single-crystal NCM conductivity: literature first, then the model
- **Decisions recorded on Sep 12**: Mechanics and mixing
- **Decisions recorded on Sep 12 items**: AM load sharing in the MPM platen (registered contract) / Stepwise unloading of the five beds: springback vs measured thickness (registration revised twice) / Coating-aware mixing: surface-energy anchor for SE–SE adhesion before the confirmatory runs
- **Conclusion**: Decisions pending: launch of the 194 + 20 network batch after the final external check.
- notes: Sources: docs/reviews/contact_resistance_pipeline_draft_v3_1_20261007.md; docs/reviews/fam_platen_prereg_20260812.md §12; docs/reviews/dem_unloading_ps45_prereg_20261009.md §12–13; docs/hetero_thesis.md §4. No numbers claimed.

## Slide 17
- **TextBox 20**: Summary
- **Rectangle 4**: What the pipeline can and cannot say today / DEM + contact network: composition trends in porosity, Li⁺ transport and load sharing — one bed per composition, model-internal ratios. / MPM: plastic morphology and the stress-stop thickness; porosity agreement is not independent evidence. / Voxel transport: a contact-free upper branch; electronic gains are grid-dependent and absolute values exceed measurements. / Every production number is pre-registered, sealed and externally re-verified before it is reported.
- notes: Summary; no new numbers.

## Slide 18
- **TextBox 20**: References
- **Refs left**: Contact mechanics and DEM / [1] S. Luding, Granul. Matter 10, 235–246 (2008) / [2] C. Thornton, Z. Ning, Powder Technol. 99, 154–162 (1998) / [3] M. Paulick, M. Morgeneyer, A. Kwade, Powder Technol. 283, 66–76 (2015) / [4] C.J. Coetzee, Powder Technol. 310, 104–142 (2017) / [5] K. Giannis et al., Granul. Matter 23, 17 (2021) / [6] W. Zunker, K. Kamrin, J. Mech. Phys. Solids 183, 105492 (2024) / [7] LIGGGHTS-PUBLIC 3.8.0 (commit 3d5c00f, 2024), github.com/CFDEMproject/LIGGGHTS-PUBLIC
- **Refs right**: Solid-state battery electrodes / [8] A.M. Bazzoun et al., J. Power Sources 661, 238682 (2026) / [9] M. So et al., J. Power Sources 508, 230344 (2021) / [10] C.A. Varkey et al., Adv. Powder Technol. 37, 105338 (2026) / [11] T. Shi et al., Adv. Energy Mater. 10, 1902881 (2020) / [12] D.J. Lee et al., Nat. Commun. 16, 4200 (2025) / [13] P. Minnmann et al., J. Electrochem. Soc. 168, 040537 (2021) / [14] V. Miß, F. Lange, S. Staubitz, B. Roling, ACS Appl. Mater. Interfaces 18, 32830–32836 (2026)
- notes: All entries are taken from the canonical literature cards (original PDFs); no bibliographic field was filled from memory.

## Slide 19
- picture: Picture 2
- **TextBox 1**: Thank you
- **직사각형 2**: For more information or any questions, please e-mail at yonghoon71@hanyang.ac.kr

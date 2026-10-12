# Wang anchor, PC size factor, and Asano contrast

Research date: 2026-10-13. Read-only scientific/reporting audit. No production changes or simulations. The PDF skill was read; Trevisanello's complete relevant page 5 was rendered and visually checked, and the original article figure/table crops listed below were visually inspected.

## Judgment for Q2/Q3

Use **dense-polycrystalline-pellet electronic conductivity reference** for Wang's approximately 4.1 mS/cm NMC811 value. Do not relabel it an independently isolated grain-interior conductivity or a measured SC/PC pair. The authors' intended intrinsic-material interpretation is relevant, but the measurement geometry does not itself establish an intragrain-only scalar.

Applying the corpus-fit PC factor `F(r) = 1 / (1 + (r / 2 um)^1.5)` to this reference presents an **unverified transfer and overlap risk**, not an established double discount. A pellet being polycrystalline is insufficient to prove that its measured resistance already contains precisely the same penalty represented by `F`. Conversely, declaring the reference intrinsic does not prove that adding `F` is valid. The missing link is the mapping between the measured specimen's grain/contact structure and the model factor's physical meaning and reference state.

Recommended reporting language: "The NMC811 electronic reference is based on a dense SPS polycrystalline pellet measurement. Its use for both SC and PC phases is a common-reference assumption. The additional PC size modifier is an empirical model factor; its transfer to this reference has not been experimentally established, and overlap with microstructural resistance already present in the reference cannot be excluded."

## Wang 2018: what was checked, and what remains card-based

Primary article: Shanyu Wang et al., *Separating electronic and ionic conductivity in mix-conducting layered lithium transition-metal oxides*, J. Power Sources 393 (2018), 75-82. [DOI](https://doi.org/10.1016/j.jpowsour.2018.05.005); [publisher](https://www.sciencedirect.com/science/article/pii/S037877531830466X).

- Publisher introduction directly confirms measurements on SPS **polycrystalline pellets**, about 800 C for 5 min, and the authors' rationale of cleaning grain boundaries to approach intrinsic transport.
- Original Fig. 1 shows ion-blocking/electron-conducting contacts and steady electronic DC current; resistance is the V-I slope. It separates carriers, not grains from boundaries.
- Original Fig. 4e/f (printed p. 79) independently confirms **NMC811**, **20 C**, and about **4 x 10^-3 S/cm = 4 mS/cm**. NMC811 sample dimensions: 2.81 mm thick, 44.3 mm2 area. Fig. S8 shows corresponding EIS/DC agreement; Fig. S2 shows the polycrystalline microstructure.
- Exact **4.1**, composition **LiNi0.8Mn0.1Co0.1O2**, **>98% density**, **40 MPa**, Ag paste, as-received/nominally stoichiometric state, and hundreds-of-nanometers grains/1-20 um precursor secondary particles are recorded in the pinned card at p. 76 sections 2.1/2.3, p. 77 section 3.1, p. 78 section 3.3, and SI S1/S2. These exact textual conditions were **not independently re-read from the complete Wang PDF in this subaudit**; flag this boundary instead of silently promoting the card to fresh full-text verification.

The direct publisher full text was inaccessible in the web tool (403); ResearchGate gives no Wang full text. No primary correction/retraction notice was found in exact-title/DOI searches, but this is not a conclusive status check. An unrelated aggregator label must not be repeated as a retraction finding.

### Measurement-to-model reasoning (our inference)

`sigma_measured = L / (A * R_e)` is the sample-spanning scalar electronic response. High density removes most pore volume but does not prove that grain-boundary, orientation, grain-neck, surface-chemistry, or electrode-contact contributions have been deconvolved. The Fig. 1 EIS circuit splits ionic and electronic branches; it does not contain an independently resolved electronic grain-interior and electronic grain-boundary decomposition.

The term "intrinsic" in this paper describes the experimental aim of reducing extrinsic complications. For a report comparing different modeling layers, the specimen-qualified label is safer than interpreting that word as proof of grain-only transport. At the same time, it would overstate the evidence to claim that the pellet necessarily contains a large electron-blocking grain-boundary penalty: neither its magnitude nor sign has been isolated here.

The original powder's secondary-particle diameter is not interchangeable with sintered grain size or with the model's `r_AM_P`. SPS modifies contacts and the relation between original secondary particles and the contiguous pellet. Thus no source-verified `r_ref` is available with which to identify the absolute normalization of `F`.

### When double counting would actually be established

A double-discount claim would need evidence that (1) the anchor includes a specific PC resistance effect, (2) `F` represents that same effect at the same structural level, and (3) the implementation applies the full absolute effect again instead of a change relative to the anchor's reference structure. A fit might already compensate through its endpoint, or the factor could represent an additional unresolved limitation absent from a clean dense pellet. Neither possibility can be inferred just from the PC label.

For illustration only, using 4.1 mS/cm as the unmodified input produces 2.05 mS/cm at `r=2 um`, because `F=0.5`. This is an algebraic implication of the model, not a new experimental result. If a measured reference really corresponded to a known `r_ref`, a transfer law would ordinarily need an explicitly justified reference normalization such as `F(r)/F(r_ref)`. The present evidence does **not** justify introducing that correction or choosing `r_ref`; it only identifies what is missing.

Giving SC and PC the same reference can be a transparent convention for isolating the modeled structure, but it does not show equal intrinsic SC and PC conductivity. Giving them different factors similarly does not turn the resulting ratio into a measured materials fact.

## Trevisanello 2021: electronic attribution boundary

Primary full text: *Polycrystalline and Single Crystalline NCM Cathode Materials - Quantifying Particle Cracking, Active Surface Area, and Lithium Diffusion*, Adv. Energy Mater. 11, 2003400 (2021). [DOI](https://doi.org/10.1002/aenm.202003400); [full PDF](https://d-nb.info/1372186662/34).

The investigated quantities are lithium chemical diffusion, surface area, and charge-transfer behavior in **liquid-electrolyte** NCM811 cells. Pages 4-5 and Fig. 4 distinguish apparent diffusion increases from intrinsic diffusion: PC cracking permits liquid infiltration, increasing active area. Page 7 connects diffusion overpotential to particle length/area. Pages 10-11 describe 90:5:5 NCM:PVDF:carbon electrodes and measurements at 25 C.

The paper discusses electronic contact contributions in EIS (page 6) and possible long-term contact loss (page 9), but supplies **no measured electronic-conductivity-versus-radius law**, no electronic SC/PC endpoint pair, and no basis for `r0=2 um` or exponent `1.5`. Its morphology/kinetics discussion can motivate a hypothesis; it cannot validate an electronic PC penalty or its magnitude. The mechanism also depends on liquid infiltration, so transferring its kinetic direction to a solid-state electronic network needs separate support.

## Asano 2017: composite versus pure-phase denominator

Primary article: *Electronic and Ionic Conductivities of LiNi1/3Mn1/3Co1/3O2-Li3PS4 Positive Composite Electrodes for All-Solid-State Lithium Batteries*, JES 164 (14), A3960-A3963 (2017). [DOI](https://doi.org/10.1149/2.1501714jes); [publisher-provided first-page preview](https://www.researchgate.net/publication/322154854_Electronic_and_Ionic_Conductivities_of_LiNi_13_Mn_13_Co_13_O_2_-Li_3_PS_4_Positive_Composite_Electrodes_for_All-Solid-State_Lithium_Batteries).

The preview verifies LiNbO3-coated NMC111 (about 5 um), Li3PS4 glass, and 48/55/62 vol% NMC composites. Original Table I (A3962) directly gives SOC-0 DC electronic conductivities **0.0020/0.0027/0.0067 mS/cm**; AC values are **0.0019/0.0028/0.0064**. Original Fig. 4a gives a **graphical approximately 0.07 mS/cm** at 100% NMC. It is not a tabulated exact value. Original Table II gives SOC-50 electronic values **0.052/0.093/0.30 mS/cm** and identifies Li2/3 composition.

The exact pure-reference preparation, coating status, and porosity/volume-fraction convention were not independently established from the available excerpts. Do not present the approximate pure point as verified grain-interior conductivity. The complete Asano text was unavailable in this subaudit; the table/figure values were verified directly from the source image crops.

Our derived comparison, using only the approximate Fig. 4a endpoint:

| NMC volume % | sigma_e,eff (mS/cm) | f_e = sigma_e,eff / 0.07 | sigma_e,eff / (x_NMC * 0.07) |
|---:|---:|---:|---:|
| 48 | 0.0020 | 0.0286 | 0.0595 |
| 55 | 0.0027 | 0.0386 | 0.0701 |
| 62 | 0.0067 | 0.0957 | 0.1544 |

The final column is conditional on using the stated NMC fraction directly as the specimen volume fraction. If the reported fraction is a solids-only fraction and specimen porosity is `epsilon`, the correct total-volume fraction is `(1-epsilon)*x_NMC`; the final column increases by `1/(1-epsilon)`. `f_e` itself needs no volume fraction, but still inherits uncertainty in the pure-point reference and measurement comparability. It should be described as a reference-normalized conductivity ratio, not automatically as a geometry-only factor.

Asano's NMC111/Li3PS4 composite conductivity cannot replace Wang's NMC811 pellet input: the composition and structural levels differ. Its value for this audit is demonstrating that composite sigma and the phase reference must be named separately, and that SOC affects the comparison. The SOC-50 table lacks a matching pure-NMC endpoint; carrying the SOC-0 denominator over would be an additional assumption.

## Source audit trail

Pinned literature figures were acquired by the parent agent from commit `e739c9730f8758d2d61b2db22d940ee9a2440897`; see `evidence/literature_figures_manifest.json` for their URLs, Git blob hashes, and SHA-256 digests. Original figure images inspected here:

- `literature_figures/litdb/figures/wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni/{fig_1,fig_4,fig_S2,fig_S8}.png`.
- `literature_figures/litdb/figures/asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity/{tab_1,tab_2,fig_4}.png`.
- `literature/trevisanello2021.pdf`, especially rendered full page 5 in `tmp/pdfs/trevisanello_p5.png`.

These source reproductions establish the displayed results; their storage in the repository does not independently authenticate every omitted part of the complete source PDF. Report fresh verification and card-transcribed conditions separately.

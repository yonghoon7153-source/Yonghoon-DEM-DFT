# ps45 electronic conductivity: primary-literature evidence notes

검토일 2026-10-13. 범위: Ketter 2025 및 Minnmann 2021의 `sigma_e,eff` 비교 조건. 생산 코드 수정/계산은 하지 않음. 문헌 카드 pin: `e739c9730f8758d2d61b2db22d940ee9a2440897`. 카드는 탐색용이며 아래 verified 항목은 원문/저자 SI로 다시 확인함.

## Sources and evidence status

- Ketter et al., *Nature Communications* **16**, 1411 (2025), DOI [10.1038/s41467-025-56514-5](https://doi.org/10.1038/s41467-025-56514-5). Publisher HTML saved as `literature/ketter2025.html`; [institutional full-paper mirror](https://juser.fz-juelich.de/record/1040442/files/s41467-025-56514-5.pdf?version=1) read through web PDF text. [Publisher SI](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-025-56514-5/MediaObjects/41467_2025_56514_MOESM1_ESM.pdf) saved as `literature/ketter2025_si.pdf`, 34 pages; text inspected, Table S3/S4 rendered and visually checked.
- Ketter [Source Data ZIP](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-025-56514-5/MediaObjects/41467_2025_56514_MOESM3_ESM.zip); dataset DOI [10.17879/54928371863](https://doi.org/10.17879/54928371863). Downloaded ZIP `literature/ketter2025_source_data.zip` extracted and exact `SourceData_Manuscript/Fig3d.csv` directly checked. CSV SHA256 `663a0f6a9b3f39fcece16bac3fc4b347085a1cb95bebc517711b92799c359ef5`.
- Minnmann et al., *Journal of The Electrochemical Society* **168**, 040537 (2021), DOI [10.1149/1945-7111/abf8d7](https://doi.org/10.1149/1945-7111/abf8d7). [Publisher-provided full text on ResearchGate](https://www.researchgate.net/publication/350927031_Editors%27_Choice-Quantifying_the_Impact_of_Charge_Transport_Bottlenecks_in_Composite_Cathodes_of_All-Solid-State_Batteries) read first. Independently confirmed against author's institutional thesis reprint and SI: [Giessen thesis PDF](https://jlupub.ub.uni-giessen.de/server/api/core/bitstreams/62b7b618-5ae3-423e-98cd-28d39c4b0749/content), saved as `literature/minnmann_thesis.pdf` (123 pages). PDF p.44/printed p.28 identifies the reprint and DOI. Relevant main-paper PDF pp.46-49 and SI PDF pp.102-105,109 were rendered and visually inspected.
- Page convention below: Ketter = printed main-paper/SI page; Minnmann = thesis PDF page plus printed thesis page, because article itself has no ordinary page numbers. This is distinct from the card's IOP-cover-inclusive PDF numbering.

## Verified findings

### Ketter 2025

| Item | Primary evidence | Interpretation for Q3 |
|---|---|---|
| Material | NCM83 = LiNi0.83Co0.11Mn0.06O2 + Li6PS5Cl; main p.6 Methods | NCM chemistry differs from NCM622 and any nominal NCM811 input. |
| Fraction denominator | SI Table S4 p.S32: NCM:SE 60:40 vol maps to 79:21 wt (rounded). Main p.6 uses densities 4.78/1.86 g/cm3 and two-phase volume ratios. | The 60 vol% is nominal **solid phase ratio**, not measured total-pellet NCM fraction including pores. |
| Pressure | Main p.7 Cell assembly: 100 mg, 370 MPa for 3 min; then constant 50 MPa for transport measurements. | 370 MPa forming and 50 MPa measuring are different. Neither equals DEM 300 MPa measurement state. |
| Method | Main pp.3-4 Fig.3; p.7 Methods; SI pp.S13-S19. Electronic EIS uses steel ion-blocking contacts, T-type TLM; DC steady-state voltage/current slope. EIS 7 MHz-100 mHz, 10 mV, 2 h OCV equilibration. DC -40 to +50 mV, 3.5 h each; 25 C. | Effective total electronic transport includes the electronic bulk and interface terms. Neither result is a single-crystal measurement. |
| Pure NCM baseline | SI Table S3 p.S29: 5.22 mS/cm input; SI S4.3 p.S18 and Fig.S14 p.S19 explicitly include pure NCM83 in DC measurements. | Measured powder-pellet DC baseline, used in RN as phase input. Grain-intrinsic conductivity is not established. |
| Particle/domain sizes | Main p.3: NCM particles about 2 um, LPSCl domains about 20 um; SEM Fig.2. | These are not two laser PSD medians. Compare to DEM PSD only with the same size definition. |
| Carbon/binder | Baseline binary series; separate VGCF series at 40 vol% NCM, SI S2 pp.S8-S9. Preparation lists no binder. | Carbon-free baseline is usable; do not mix in VGCF data or LFA carbon coating. |
| SoC | As-received NCM83 dried and soft-milled; no cycling/pre-delithiation step stated in transport methods. | Pristine/lithiated interpretation is reasonable **inference**; an explicit quantitative 0% SoC certification was not found. |
| Porosity | SI S7 p.S24: inputs measured on porous samples; modeled porosity partly implicit. The reported densities are from 500 MPa/60 min isostatic **thermal** specimens. | Do not assign those thermal-pellet porosities (e.g. pure NCM about29%) to electronic 370/50 MPa specimens. Electronic-specimen porosity remains unverified. |
| Uncertainty | SI Fig.S22 p.S31: electrical points individual measurements; error bars relative deviation50%. | Not replicate SD or a measured 95% interval. |

**Exact electronic values, independently verified:** publisher Source Data `SourceData_Manuscript/Fig3d.csv`, units explicitly mS/cm. The repeated composition columns refer to different series; do not pair the first RN composition column with the DC/EIS values on the same row.

| phi_NCM solid % | sigma_e DC mS/cm | sigma_e EIS mS/cm | RN prediction mS/cm |
|---:|---:|---:|---:|
|20|0.01466|0.01373|0.00918|
|40|0.20859|0.22570|0.51259|
|60|**1.03488**|**1.12144**|1.62022|
|80|1.98451|1.71756|3.23011|
|100|**5.22147**|not listed|5.22 input|

The user's rounded60vol% DC1.035/EIS1.121 and pure5.22 claims are supported. CSV `yerr` entries are exactly about50% of values, corroborating SI Fig.S22's plotting convention; e.g.60vol% DC yerr0.51744 and EIS yerr0.56072. They must not be relabeled measured uncertainty. At60vol%, EIS/DC=1.08364 (our calculation), an8.36% difference.

### Minnmann 2021

| Item | Primary evidence | Interpretation for Q3 |
|---|---|---|
| Material/size | Thesis PDF p.46/printed30, Experimental: BASF NCM622 typical3 um; NEI LPSCl. SI Table S5 PDF p.109/printed93: coarse D50=3.45, D90=20.05 um; fine D50=2.45, D90=8.57 um. | Fine/coarse differs mainly in the upper SE tail; do not substitute D50 for all domains. |
| Preparation/pressure | Main reprint PDF p.46: hand mortar15 min, 100 mg, 10 mm diameter PEEK cell,380 MPa/3 min at RT; steel rods for electronic measurement; EIS at approximately40 MPa. | 380 MPa is forming;40 MPa is measurement. Ionic measurement follows electronic measurement and involves adding SE layers and repressing. |
| Method/SoC | Same page: EIS7 MHz-50 mHz,10 mV,RT. PDF p.47/printed31 states fully lithiated NCM622 (0% SoC); SI PDF p.102/printed86 confirms. SI S6: R_el=L(r_el,bulk+r_el,int), with NCM-NCM contact term. | Composite sigma_e is EIS-derived total DC-limit partial conductivity, including particle contacts; comparable in observable type to a full electronic network effective conductivity. |
| Fraction definition | SI Eq.S9/TableS1 PDF p.104/printed88: phi_i=(1-phi_porosity)phi_i,nom; average porosity14% applied to all formulations. 53vol%=80:20wt;61vol%=86:14wt. | **61vol% is total electrode volume including pores**, unlike Ketter60vol% solid ratio. |
| Pure reference | Main PDF p.48/printed32 says pure samples measured by EIS. SI §3 PDF p.103/printed87 explicitly states pores in pure CAM/SE reduce measured conductivity; tau set1 for simplicity. TableS2 pure NCM10mS/cm. | A porous pure-sample reference, not demonstrated dense-grain intrinsic sigma0. Pure NCM specimen porosity/thickness and separate detailed pressure history not established. |
| Additives | Main preparation and SI§3 use pure powder mixtures; VGCF addressed as separate experiment. | Baseline table is carbon/binder-free. |

**Exact electronic table, independently verified:** SI Table S2, thesis PDF p.105/printed89. Units below converted from printed S/cm to mS/cm (x1000).

| phi_NCM total % | phi_SE total % | NCM:SE wt ratio (TableS1) | sigma_e,eff mS/cm | tau_e^2 |
|---:|---:|---:|---:|---:|
|25|61|50:50|0.0206|120|
|33|53|60:40|0.236|13.7|
|42|44|70:30|0.556|7.44|
|53|33|80:20|1.11|4.77|
|61|25|86:14|1.43|4.29|
|61|25 (fine SE)|86:14|0.697|8.79|
|100 (nominal)|0|pure NCM|10.0|1 by convention|

SI TableS1 sample porosities are7.6,13,17,17,15%, averaging13.9% rounded14%; the composition correction uses the common14% rather than each sample's porosity. Fine-SE sample porosity is not separately tabulated. Main reported13-17% range omits the7.6% sample. No uncertainty bars/repeat count for these sigma values established by the inspected table; two-cell replication mentioned in main paper concerns cycling.

## Derived comparisons (our arithmetic, not new paper measurements)

Final cross-check: the actual archived DEM beds use 4800/2000 kg/m3 and reconstruct to 64.71–64.92% AM in solid sphere volume, not the request's60%. See `composition_basis.md` and the main verdict. The60% calculation below is a conditional explanation of the original request's assumption, not the final bed composition.

1. At assumed14% porosity, DEM60vol% of solids maps to51.6vol% of the total electrode. Minnmann53vol% is closer than61vol%. Conversely53/86=61.63% solids;61/86=70.93% solids (rounded printed fractions).
2. DEM81.6:18.4wt cannot be simultaneously matched to both papers'60vol% using their densities. Ketter densities give63.31% solid NCM for81.6wt%; Ketter60vol% corresponds79.40wt% (SI rounded79%). Minnmann densities give64.07% solid/55.10% total at14% pores for81.6wt%. Treat fixed weight fraction and fixed solid-volume fraction as separate comparison choices; density conventions matter.
3. Minnmann normalized electronic ratios sigma_eff/sigma_pure:53vol%0.111;61coarse0.143;61fine0.0697. These are **pellet-referenced ratios**. Applying the same normalization to DEM grain-edge sigma0 does not remove the reference-material mismatch automatically.
   Ketter60vol% likewise gives0.19820 (DC/DC-pure) or0.21477 (EIS/DC-pure), using the exact5.22147mS/cm measured pure baseline. The EIS ratio uses a DC-measured denominator; pure EIS is not listed in Fig3d.csv.
4. A result near1mS/cm is consistent in order with the closest measured compositions, but the papers do not establish agreement at300MPa, the DEM PSD, or DEM grain/constriction convention. They cannot identify whether a model gap is caused by an intrinsic sigma0 choice, contact law, geometry, or pressure without those conditions being matched.

## Reuse cautions

- Cite Minnmann53vol%/1.11mS/cm as the closer **composition benchmark**, and61vol% coarse/fine as a particle-size sensitivity case at higher CAM loading.
- Keep bulk/pellet sigma0 versus grain sigma0 explicit. Both pure references have interparticle/porosity contributions, so introducing them as dense particle conductivities in a DEM with explicit pores/contacts risks additional attenuation. The precise amount of double counting is not quantified by these papers.
- A measured effective sigma includes unresolved constriction/contact physics. A paper saying its tortuosity formula neglects explicit constriction terms does not mean the measured conductivity excludes constriction.
- No final report verdict or parameter recommendation made in these notes.

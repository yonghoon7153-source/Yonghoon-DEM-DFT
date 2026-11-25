# B. Computational quantification of sulfide-SE decomposition volume change (argyrodites, Li3PS4, Li7P3S11, LGPS-type), incl. dopant dependence: literature gap check (to Nov 2026)

*Reading conventions for the report writer.* Tags: **[COMP]** computational, **[EXP]** experimental, **[COMP+EXP]** both. **[litdb]** = already in the project literature DB (`litdb/papers/<slug>.md`, summarized from the digest text only; litdb figure PNGs were not opened in this pass). **[NEW]** = found in this search, with no digest of its own in litdb. An rg search of `litdb/` for their DOIs and titles gave 0 hits, except Koerver 2018, which is only cited inside other digests (barai2021, jung2019). **Verification level**: "full text (digest)" = a litdb digest made from the full text + SI. "abstract/snippet" = only abstracts, metadata or search-engine summaries were seen, because WebFetch failed with DNS errors in this session for pmc.ncbi.nlm.nih.gov, www.ebi.ac.uk, pubs.rsc.org, scholar.harvard.edu, www.nature.com, par.nsf.gov, www.ornl.gov, arxiv.org and advanced.onlinelibrary.wiley.com. All numbers are as reported (literature values). None were computed here.

## Q1. Has any paper computed decomposition-reaction volume changes for argyrodites or other sulfide SEs (any potential)? Which compositions, potentials, methods, numbers?

### Takeaway
Yes. "First to compute the decomposition volume change of a sulfide SE" is **not** an available novelty claim. Two independent computational lines already exist:
- Wang/Zeier/Janek/Mollenhauer (*Angew.* 2026). DFT-volume-based ΔV/V maps for interfacial reactions of 7 sulfide SEs, including Li6PS5Cl, Li3PS4, Li7P3S11 and LGPS, at 2.0–4.5 V.
- The Xin Li group (Harvard), since 2018. They compute a "reaction strain" (the volume change of decomposition) of LSPS-, LGPS- and Li6PS5Cl-type sulfides and feed it into a mechanically constrained thermodynamics.

Further DFT or MLIP work exists on (de)lithiated argyrodite intermediates and on Li|Li6PS5Cl interphase products. In all of it the volume is a side output, not a screening metric.

### Cited Findings
**(a) Wang–Zeier–Janek–Mollenhauer 2026: the closest direct precedent [COMP] [litdb] [full text (digest)]**
- Citation: Wang, K.; Zeier, W. G.; Janek, J.; Mollenhauer, D. "Interface Stability and Kinetics of Sulfide Electrolytes in all-Solid-State Batteries", *Angew. Chem. Int. Ed.* **65**, e19663 (2026), DOI 10.1002/anie.202519663. It is computational only: VASP/PBE(+U), pymatgen, Materials Project hull data and AIMD. Digest: `litdb/papers/wang2026_interface_stability_kinetics_sulfide_assb.md`. — [Source](https://doi.org/10.1002/anie.202519663)
- Definition (their Eq. 3): ΔV/V = [V_eq,interface − x·V(c_A) − (1−x)·V(c_B)] / [x·V(c_A) + (1−x)·V(c_B)] × 100 %.
  - x is the pseudo-binary mixing ratio of the two contacting materials.
  - Volumes are DFT-relaxed.
  - The volumes of gaseous products (SO2, O2) are set to zero, on the assumption that they leave the reaction zone. The digest notes this can exaggerate negative ΔV/V.
  - Source: [Source](https://doi.org/10.1002/anie.202519663)
- Scope:
  - 7 SEs: Li3PS4, Li7P3S11, Li6PS5Cl, Li4GeS4, Li4SnS4, Li10SnP2S12 and Li10GeP2S12.
  - Partners: 20 cathodes, about 70 interlayer/coating materials and 6 amorphous a-LixSi anodes.
  - Each pair is computed chemically (pseudo-binary) and electrochemically (grand potential with μ_Li = μ⁰_Li − eφ). The cathode and coating side runs over 2.0–4.5 V; the a-LixSi side runs over 0–2.5 V (SI Figs. S16–S22).
  - Source: [Source](https://doi.org/10.1002/anie.202519663)
- Reported trends and numbers:
  - Heatmap color scales: about ±25 % for the chemical cathode×SE ΔV/V, and ±30 % for the Li6PS5Cl electrochemical case (2.0–4.5 V × 20 cathodes).
  - High voltage gives expansion, because product phases with large molar volume form. Example: NiO2 + Li6PS5Cl gives NiP4O11 (131 cm³/mol), SOCl2 (72 cm³/mol) and Ni(PO3)2 (65 cm³/mol).
  - Low voltage gives contraction. Example: LiNiO2 + Li6PS5Cl gives Ni3S2 (40 cm³/mol), Li2SO4 (52 cm³/mol), Li3PO4 (48 cm³/mol) and LiCl (21 cm³/mol).
  - For a-LixSi, expansion appears at x = 0.00 and is attributed to SiS2 formation.
  - Source: [Source](https://doi.org/10.1002/anie.202519663)
- Limits:
  - No numeric table of ΔV/V exists, not even in the SI. Results are heatmap colors only, and Table S2 gives product names only.
  - Mechanics is qualitative only. The paper says *"positive ΔV/V … could lead to stress accumulation and potential cracking"* and has no elastic constants, EOS or stress conversion.
  - The SE host is fixed: no dopant or substituent variation of Li6PS5Cl.
  - The digest also flags an internal inconsistency. The SiS2-based volume explanation conflicts with the paper's own AIMD, which shows Si–S coordination ≈ 0 (Fig. 8). In other words, the thermodynamic product set and the kinetically formed interphase disagree.
  - Source: [Source](https://doi.org/10.1002/anie.202519663)

**(b) Xin Li group (Harvard): "reaction strain" plus mechanical constriction (constrained-ensemble thermodynamics) [NEW unless marked litdb]**
- Wu, F.; Fitzhugh, W.; Ye, L.; Ning, J.; Li, X. "Advanced sulfide solid electrolyte by core-shell structural design", *Nat. Commun.* **9**, 4037 (2018), DOI 10.1038/s41467-018-06123-2. [COMP+EXP] [abstract/snippet]
  - System: Li–Si–P–S (LSPS) core–shell. The window is reported as 0.7–3.1 V, with a quasi-stability window up to 5 V for a high-Si shell.
  - This is attributed to volume constriction resisting the decomposition that accompanies electrolyte expansion. A constant-volume constraint opens the window further.
  - [Source](https://doaj.org/article/cae607d9b42546a0ad6d18336848d877); [Source](https://ideas.repec.org/a/nat/natcom/v9y2018i1d10.1038_s41467-018-06123-2.html)
- Fitzhugh, W.; Wu, F.; Ye, L.; Su, H.; Li, X. "Strain-Stabilized Ceramic-Sulfide Electrolytes", *Small* **15** (33), e1901470 (2019), DOI 10.1002/smll.201901470. [COMP/theory per abstract; any experimental content not verified] [abstract/snippet]
  - Li10GeP2S12 is argued to be stabilized by a thin amorphous shell that earlier models considered too thin.
  - The choice of "decay-morphology" model strongly changes the predicted voltage widening.
  - [Source](https://zendy.io/title/10.1002/smll.201901470); [Source](https://pesquisa.bvsalud.org/ses/resource/pt/mdl-31268620)
- Fitzhugh, W.; Wu, F.; Ye, L.; …; Li, X. "A High-Throughput Search for Functionally Stable Interfaces in Sulfide Solid-State Lithium Ion Conductors", *Adv. Energy Mater.* **9**, 1900807 (2019), DOI 10.1002/aenm.201900807. [COMP] [abstract only; full author list not verified]
  - DFT phase data analyzed in high throughput: >2,000 candidate materials for the cathode voltage range and >1,000 for the anode range.
  - LiCoO2 is the test cathode; the screen looks for coatings stable against both Li10SiP2S12 and LCO. The paper adds a binary-search algorithm for pseudo-phases.
  - The abstract does **not** confirm whether reaction strain or constriction enters this particular screen.
  - [Source](https://onlinelibrary.wiley.com/doi/abs/10.1002/aenm.201900807)
- Fitzhugh, W.; Ye, L.; Li, X. "The effects of mechanical constriction on the operation of sulfide based solid-state batteries", *J. Mater. Chem. A* **7** (issue 41) (2019), DOI 10.1039/C9TA05248H. [review/perspective of the constriction framework] [title/metadata only; first page not verified] — [Source](https://www.researchgate.net/publication/335801494_The_effects_of_mechanical_constriction_on_the_operation_of_sulfide_based_solid-state_batteries)
- Gil-González, E.; Ye, L.; Wang, Y.; Shadike, Z.; Xu, Z.; Hu, E.; Li, X. "Synergistic effects of chlorine substitution in sulfide electrolyte solid state batteries", *Energy Storage Mater.* **45**, 484–493 (2022), DOI 10.1016/j.ensm.2021.12.008. [COMP (AIMD + constrained-ensemble ESW) + EXP] [litdb, full text (digest)]
  - Reaction strain is defined as ε_RXN = (V_products − V_SE)/V_SE.
  - Compositions: Li7−xPS6−xClx with x = 0.5, 1.0, 1.5 and 2.0, plus Li7P3S11 and LGPS.
  - Cl-rich decomposition products (PCl3, SCl, P2S7) have large molar volume, hence large reaction strain. Under constriction this widens the window.
  - For x = 1.5 the window is 1.70–2.40 V at K_eff = 0 and 0.80–4.30 V at K_eff = 20 GPa.
  - Digest: `litdb/papers/gilgonzalez2022_synergistic_cl_constricted_esw.md`. [Source](https://doi.org/10.1016/j.ensm.2021.12.008)
- Su, Y.; Ye, L.; Fitzhugh, W.; Wang, Y.; Gil-González, E.; Kim, I.; Li, X. "A more stable lithium anode by mechanical constriction for solid state batteries", *Energy Environ. Sci.* **13**, 908–916 (2020), DOI 10.1039/C9EE04007B. [EXP cells per abstract; computational part not verified] [abstract/snippet]
  - LGPS with a Li/graphite composite anode.
  - Constriction "modifies the decomposition pathway of LGPS at the anode interface" and suppresses dendrites. No short circuit was seen up to 10 mA cm⁻².
  - [Source](https://pubs.rsc.org/en/content/articlelanding/2020/ee/c9ee04007b)
- Ye, L.; Li, X. "A dynamic stability design strategy for lithium metal solid state batteries", *Nature* **593**, 218–222 (2021), DOI 10.1038/s41586-021-03486-3. [EXP cells; computational content not verified] [abstract/snippet]
  - Multilayer electrolyte: a less stable electrolyte sandwiched between more stable layers.
  - Cycled for 1,800 h at 0.25 mA cm⁻².
  - [Source](https://ideas.repec.org/a/nat/nature/v593y2021i7858d10.1038_s41586-021-03486-3.html); [Source](https://www.peeref.com/works/22154989)
- Wang, Y.; Ye, L.; Chen, X.; Li, X. "A Two-Parameter Space to Tune Solid Electrolytes for Lithium Dendrite Constriction", *JACS Au* **2**, 886–897 (2022), DOI 10.1021/jacsau.2c00009. [COMP (high-throughput + ML) + EXP] [abstract/snippet]
  - Electrolytes are classified by decomposition energy against Li metal (E_hull) and by an interface "critical modulus" K*. The recommended design target is K* to Li metal "well below 20 GPa".
  - "Positions of electrolytes in such a space can be controlled by the chemical composition of the electrolyte". Core–shell microstructures realize those compositions experimentally.
  - Reported cycling: 10,000–20,000 cycles at 8.6–30 mA/cm².
  - ⚠ One search summary said the high-throughput part covers ">120,000 material interfaces to lithium metal". A second search could not confirm this. Treat it as unverified.
  - [Source](https://api-pubmed-ncbi.laibokeji.com/35557758); [Source](https://www.omicsdi.org/dataset/biostudies-literature/S-EPMC9088294)

**(c) DFT volumes of (de)lithiated argyrodite intermediates. These are not decomposition products. [COMP+EXP] [litdb]**
- Schwietert, T. K.; Arszelewska, V. A.; Wang, C.; Yu, C.; Vasileiadis, A.; …; Wagemaker, M. "Clarifying the relationship between redox activity and electrochemical stability in solid electrolytes", *Nat. Mater.* **19**, 428–435 (2020), DOI 10.1038/s41563-019-0576-0.
  - DFT lattice parameter vs Li content in LixPS5Cl (SI Fig. S3, figure-read in our digest): x = 6 ≈ 9.88 Å, x = 4 ≈ 9.78 Å, x = 11 ≈ 10.54 Å.
  - XRD on delithiation: 9.8693 → 9.7620 Å, consistent with DFT.
  - On lithiation, no XRD peak shift was seen even though DFT predicts expansion.
  - Digest: `litdb/papers/schwietert2020_redox_activity_vs_electrochemical_stability.md`. [Source](https://doi.org/10.1038/s41563-019-0576-0)
- Schwietert, T. K.; Vasileiadis, A.; Wagemaker, M. "First-Principles Prediction of the Electrochemical Stability and Reaction Mechanisms of Solid-State Electrolytes", *JACS Au* **1**, 1488–1496 (2021), DOI 10.1021/jacsau.1c00228. [COMP] [litdb]
  - SI Tables S2–S13 tabulate volumes, band gaps and σ of metastable (de)lithiated phases for 12 SEs.
  - The digest notes that the paper's generalization *"Most metastable phases show a significant volume increase during lithiation"* is contradicted by its own table. LATP goes 1404.34 → 1351.52 Å³ on lithiation.
  - [Source](https://doi.org/10.1021/jacsau.1c00228)

**(d) Li|Li6PS5Cl interphase works that touch volume [NEW]**
- Hao, H.; Liu, Y.; Greene, S. M.; Yang, G.; Naik, K. G.; Vishnugopi, B. S.; Wang, Y.; Celio, H.; Dolocan, A.; Tsai, W.-Y.; Fang, R.; Watt, J.; Mukherjee, P. P.; Siegel, D. J.; Mitlin, D. "Tuned Reactivity at the Lithium Metal–Argyrodite Solid State Electrolyte Interphase", *Adv. Energy Mater.* **13** (46), 2301338 (2023), DOI 10.1002/aenm.202301338. [COMP (DFT + mesoscale chemo-mechanical model) + EXP (cryo-FIB, Raman)] [abstract/snippet]
  - Abstract quote: *"Decomposition drives voiding in Li metal due to its high flux to the reaction front, as well as voiding in the SSE due to the associated volume changes."*
  - "Tuned" refers to a 0.75 µm Li2Te–LiTe3 interlayer, not to SE doping.
  - No ΔV numbers were retrieved.
  - [Source](https://oa.mg/work/10.1002/aenm.202301338); [Source](https://impact.ornl.gov/en/publications/tuned-reactivity-at-the-lithium-metalargyrodite-solid-state-elect/)
- Yang et al. "Enhanced Ionic Conductivity at the Solid Electrolyte Interphase of Oxygen-Doped Li6PS5Cl", *Adv. Sci.* (2026), DOI 10.1002/advs.76563, PMID 42439417. [COMP] [snippet only; full author list and volume not retrieved]
  - Method: SevenNet (NequIP-type) MLIP-MD plus ML phase identification at the Li6PS5−xClOx | Li interface.
  - Equations of state for candidate products (Li6PS5Cl, Li2S, Li3P, LiCl, Li2O) were computed with DFT and with the MLIP, apparently as validation. Reaction energies of Li with Li6PS5Cl and with Li6PS4ClO1 were computed by both.
  - The interfacial reaction is "almost" independent of the anti-site ratio. The SEI is dominated by Li2S-based anion-substituted phases.
  - After about 1050 ps the O-doped SEI shows a steeper Li MSD slope. The retrieved text does not report a volume change.
  - [Source](https://pubmed.ncbi.nlm.nih.gov/42439417/); [Source](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.76563)
- Ding, J.; Zichi, L.; Carli, M.; Wang, M.; Musaelian, A.; Xie, Y.; Kozinsky, B. "Coupled reaction and diffusion governing interface evolution in solid-state batteries", arXiv:2506.10944 (2025). [COMP (active-learned equivariant MLIP reactive MD)] [abstract]
  - Reports a previously unreported crystalline disordered SEI phase, Li2S0.72P0.14Cl0.14, that *"evaded previous predictions based purely on thermodynamics"*.
  - [Source](https://arxiv.org/abs/2506.10944)
- "Two-step growth mechanism of the solid electrolyte interphase in argyrodyte/Li-metal contacts", arXiv:2402.04095, and the related APS March Meeting 2024 abstract. [COMP (moment-tensor potentials)] [title/abstract; authors not retrieved]
  - Rapid Li influx first reduces the SE to an amorphous phase, which then slowly crystallizes into a Li2(SxPyCl1−x−y) solid solution.
  - [Source](https://arxiv.org/pdf/2402.04095); [Source](https://meetings-archive.aps.org/mar/2024/g64/1/)

**(e) Secondary mentions with unresolved primary source**
- A 2026 open-access *J. Mater. Chem. A* paper (d6ta01253a) states that *"a related DFT study found that lithiation of Li3PS4 and LGPS gives rise to volume expansion and band gap narrowing"*. The underlying DFT study was not identified. — [Source](https://pubs.rsc.org/en/content/articlehtml/2026/ta/d6ta01253a)
- A search summary of 2026 reviews claims that *"the oxidative decomposition of sulfide SEs further reduces their molar volume"*, contributing to pressure drop and contact loss under constant-volume conditions. Attribution between two reviews (Song et al., *Adv. Sci.* 2026, DOI 10.1002/advs.202524187, and "Rational design of sulfide solid electrolytes for solid-state batteries", Springer 2026) was **not resolved**. — [Source](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202524187); [Source](https://link.springer.com/article/10.1007/s44503-026-00022-0)

### Inferences
- **The novelty space is narrower than "computing ΔV of decomposition".** The quantity has been computed:
  - as an interface pseudo-binary or grand-potential ΔV/V against partner materials (Wang 2026);
  - as an SE-normalized reaction strain inside a constrained-ensemble ESW (Li group, 2018–2022).
  A new study must differentiate itself on axes those works lack: dopant resolution, both electrodes for the same host, explicit reference-state conventions, numeric tables and a mechanics conversion.
- **The sign depends on conventions.** The literature uses different reference states:
  - Wang normalizes to the reactant mixture and sets gas volume to 0.
  - Li normalizes to V_SE.
  - The treatment of the Li reservoir is not stated in either digest.
  Whether consumed Li (anode) or removed Li and released gases (cathode) are counted can plausibly flip the sign of ΔV/V. This would also explain the apparent conflict between "high-voltage expansion" (Wang 2026, with oxide cathodes) and a review claim that SE oxidation lowers molar volume. A screening study must fix and state this convention.
- **Thermodynamic and observed products diverge for Li|Li6PS5Cl.** Examples: indirect (de)lithiated intermediates (Schwietert); a crystalline disordered Li2(S,P,Cl) phase (Ding/Kozinsky); amorphous-then-solid-solution growth (arXiv 2402.04095); and Wang 2026's SiS2 explanation vs its own AIMD. Hull-based ΔV/V is therefore a thermodynamic-limit descriptor, not an interphase volume.

### Gaps
- Full texts of the following could not be opened (DNS-blocked hosts listed above): Wang 2022 *JACS Au*; Fitzhugh 2019 *AEM*, *Small* and *JMCA*; Ye & Li 2021 *Nature*; Hao 2023; Yang 2026; Ding 2025.
  - So the exact reaction-strain and K* formulas, the treatment of the Li reservoir, and any numeric ε_RXN values for specific sulfides (LGPS, LSPS, Li6PS5Cl) are **not verified here**.
  - Highest priority: the *JACS Au* 2022 main text and SI ([PMC9088294](https://pmc.ncbi.nlm.nih.gov/articles/PMC9088294); [SI](https://scholar.harvard.edu/files/lixin/files/au2c00009_si_001.pdf)).
- Wang 2026: whether exchanged Li is counted in the *electrochemical* ΔV/V is not stated in our digest (Eqs. 4–5 define only energies). The SI needs checking.
- No numeric table of decomposition ΔV/V for Li6PS5Cl self-decomposition at fixed anode and cathode potentials (SE alone, no partner) was found in any source.
- Negative-search log for Q1:
  - "sulfide solid electrolyte decomposition products volume change ΔV/V dopant DFT argyrodite chemo-mechanical" (extended) → no paper combining these.
  - "arXiv solid electrolyte interphase "volume change" decomposition reaction thermodynamic products lithium metal sulfide 2025" → no matching 2025 arXiv preprint.
  - "sulfide electrolyte oxidative decomposition molar volume decrease stack pressure drop contact loss composite cathode Li6PS5Cl" → no quantitative primary source.

## Q2. Has anyone done this per dopant/substituent (O, Br, I, Sb, Ge, Si, Sn, Al, Zn, Cu, B, Nd, Bi) or as a screening axis? Any HT/ML study using "decomposition volume change" or "interphase volume mismatch" as a descriptor?

### Takeaway
Only partial precedents exist:
- a **Cl-content series** (Li7−xPS6−xClx, x = 0.5–2.0) with reaction strain inside a constrained-ensemble ESW (Gil-González 2022);
- a **composition-tunable two-parameter space** (decomposition energy, critical modulus K*) built with high-throughput + ML against Li metal (Wang 2022 *JACS Au*), whose compositional scope could not be verified;
- compound-level Ge/Sn/Si comparisons (Wang 2026; LSPS vs LGPS).

No study was found that screens a broad set of dopants in Li6PS5Cl-type argyrodites by decomposition ΔV/V at both cathode and anode potentials. The recent HT/ML interface screens either omit volume or explicitly list it as not captured.

### Cited Findings
- **Cl substituent axis.** Gil-González 2022 computes reaction strain for Li7−xPS6−xClx (x = 0.5, 1.0, 1.5, 2.0). Cl-rich products (PCl3, SCl, P2S7) give higher molar volume and larger reaction strain, which widens the window under K_eff = 10–20 GPa. This is the only found substituent-resolved reaction-strain series for argyrodites. [COMP+EXP] [litdb] — [Source](https://doi.org/10.1016/j.ensm.2021.12.008)
- **Composition-controlled position in (E_hull, K*) space.** Wang, Ye, Chen, Li (2022): *"computational work with high-throughput calculations and machine learning indicates that the positions of electrolytes in such a space can be controlled by the chemical composition of the electrolyte"*, with design target K* "well below 20 GPa". The scope is Li-metal (anode) side only. Which dopants and hosts are covered was not retrievable. [COMP+EXP] [abstract] — [Source](https://api-pubmed-ncbi.laibokeji.com/35557758)
- **Compound-level cation variation.** Wang 2026 *Angew.* includes Li4GeS4, Li4SnS4, Li10SnP2S12 and Li10GeP2S12 alongside Li6PS5Cl, Li3PS4 and Li7P3S11. These are different compounds, not dopant series in one host. ΔV/V is given as heatmaps only. [COMP] [litdb] — [Source](https://doi.org/10.1002/anie.202519663)
- **O-doped Li6PS5Cl at Li metal.** Yang et al. *Adv. Sci.* 2026 is dopant-resolved: Li6PS5−xClOx, with Li6PS4ClO1 reaction energies from DFT and MLIP. Its metric is SEI Li transport (MSD), not volume, although EOS of products were computed. [COMP] [snippet] — [Source](https://pubmed.ncbi.nlm.nih.gov/42439417/)
- **HT/ML interface screens without a volume descriptor.**
  - Park, S.; Jang, M.; Jung, H.-G.; Chung, K. Y.; Yu, S. "Machine-Learning Framework for Designing Stable Interfaces in All-Solid-State Lithium-Ion Batteries", *Adv. Sci.* (2026) e76305, DOI 10.1002/advs.76305. [COMP: MP energies + pymatgen + ML; no own DFT] [litdb]
    - The paper lists *"strain and volume-change effects"* among phenomena its reaction-energy screening does not capture (future work).
    - Its only volume-like input is an elemental descriptor, "GS Volume per Atom (max−min)". It ranks 6th in permutation importance (ΔMAE ≈ 4 meV/atom, figure-read) and is not a reaction volume.
    - [Source](https://doi.org/10.1002/advs.76305)
  - Jang, M.; Kwon, E.; Jeon, C.; Kim, S.; Yu, S. "Interfacial Stability and Design Strategies for Halide Solid Electrolytes in High-Voltage All-Solid-State Sodium-Ion Batteries", *Small Methods* **10** (3), e02179 (2026), DOI 10.1002/smtd.202502179. [COMP: MP data + pymatgen grand-potential/pseudo-binary + PCA/K-means; no own DFT] [litdb: `litdb/papers/jang2026_halide_se_interfacial_stability_highv_na.md`]
    - High-throughput screen of 12,800 Na-containing compounds as coatings that suppress interfacial reaction driving forces. Same KIST group as Park 2026.
    - Neither the abstract nor our digest has any volume or ΔV content (grep for "volume/부피/ΔV" in the digest: 0 hits).
    - [Source](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/smtd.202502179)
  - Shen et al. "Harnessing database-supported high-throughput screening for the design of stable interlayers in halide-based all-solid-state batteries", *Nat. Commun.* **16** (2025), DOI 10.1038/s41467-025-58522-x. [COMP+EXP] [abstract]
    - Li3OCl is the top interlayer for Li3InCl6 | Li. Li6PS5Cl + Li3InCl6 degrades in two steps to LiCl, LiInS2 and Li3PS4.
    - Volume change is not mentioned in the retrieved metadata.
    - [Source](https://www.nature.com/articles/s41467-025-58522-x); [Source](https://doaj.org/article/67f2d77ff11f46a29b4abd177ad7ca2a)
  - "Data-driven design strategies for chemically stabilizing cathode–coating interfaces employing interpretable machine learning", *J. Mater. Chem. A* (2026), DOI 10.1039/D6TA02648F. SHAP descriptors for interfacial reactivity; volume change or voids are not mentioned in the abstract. [COMP] [abstract] — [Source](https://pubs.rsc.org/en/content/articlelanding/2026/ta/d6ta02648f)
- **Hull caveat for doped argyrodite screens.** "The devil in the details: lessons from Li6PS5X for robust high-throughput workflows", *J. Mater. Chem. A* **13**, 526 (2025): *"none of these Li6PS5X crystals lies on the convex hull of the Li–P–S–X phase diagram at 0 K, according to the Materials Project."* [COMP] [snippet] — [Source](https://pubs.rsc.org/ta/article/13/1/526/874967/The-devil-in-the-details-lessons-from-Li6PS5X-for)

### Inferences
- **The gap that survives:** a **dopant-resolved** map of decomposition ΔV/V for one argyrodite host (aliovalent cation dopants such as Sb, Ge, Si, Sn, Al, Zn, Cu, B, Nd, Bi, plus anion dopants O, Br, I), computed at **both** a reducing (Li-metal) and an oxidizing (cathode-potential) condition, with an explicit Li/gas reference-state convention and numeric tables. No such study was found.
- The closest competitor to differentiate against is the **Xin Li constriction line**: Gil-González for the Cl axis and the *JACS Au* 2022 two-parameter space for the composition axis at Li metal. Their full texts must be read before claiming the gap, because the *JACS Au* HT+ML set might already include doped argyrodites.
- **The two lines value the same quantity in opposite ways.**
  - Li group: positive reaction strain is *beneficial*, because under constriction it stabilizes the SE and widens the ESW.
  - Wang 2026: positive ΔV/V means *stress or cracking (bad)* and negative ΔV/V means *voids (bad)*.
  A dopant screen must state its objective up front, for example minimizing |ΔV/V| for contact retention, or maximizing ε_RXN for constriction stabilization.
- For doped argyrodites with E_hull > 0, the decomposition product set, and hence ΔV/V, depends on how metastability is handled. A robust screen would report sensitivity to that choice, since MP places no Li6PS5X on the hull.

### Gaps
- Not verified: whether Wang 2022 *JACS Au* or Fitzhugh 2019 *AEM* includes doped Li6PS5Cl, Li3PS4 or Li7P3S11 compositions in the high-throughput set (full text blocked).
- Not searched individually per dopant (e.g., "Li6PS5Cl Sb doping decomposition volume"). The broad dopant queries returned nothing relevant, but single-dopant papers that compute volume as a side result could have been missed.
- Negative-search log for Q2:
  - "sulfide solid electrolyte decomposition products volume change ΔV/V dopant DFT argyrodite chemo-mechanical" (extended) → none.
  - "reaction strain decomposition doped Li6PS5Cl substitution mechanical constriction high-throughput constrained ensemble screening" (extended) → none combining these. It returned the O-doped SEI paper, the halide interlayer screen and the Li6PS5X HT caveat.
  - "high-throughput interfacial reaction volume change descriptor solid electrolyte cathode coating screening 2025 void cracking" (extended) → none. The search engine's own summary concluded: *"the likely gap is a screen that adds a mechanical or volume-mismatch term to the reaction-energy descriptor"*.

## Q3. Analogous computational work for other SEs (oxides LLZO/LATP/LAGP, halides Li3YCl6/Li3InCl6, LiPON) on decomposition or interphase volume expansion: transplantable methods

### Takeaway
For oxides, the canonical chemo-mechanical case is **Li|LAGP**: interphase formation with volume expansion leads to fracture and impedance rise. It is established mainly by experiment (tomography) and backed by FEM stress modeling. Li|LATP shows large expansion (experimental). Computed volumes of metastable (de)lithiated phases exist for 12 SEs (Schwietert 2021).

For halides, the searches found experimental interphase growth (Li3InCl6 → In metal) and HT interlayer or coating screens, but **no computed decomposition volume change**. LiPON was not searched specifically.

Transplantable methods:
- Wang 2026's Eq. 3 ΔV/V on pseudo-binary or grand-potential products;
- the Li group's constrained ensemble (ε_RXN, K_eff, K*);
- Pilling–Bedworth-type molar-volume ratios (from metal oxidation and liquid-electrolyte SEI literature).

### Cited Findings
- Tippens, J.; Miers, J. C.; Afshar, A.; Lewis, J. A.; Cortes, F. J. Q.; Qiao, H.; Marchese, T. S.; Di Leo, C. V.; Saldana, C.; McDowell, M. T. "Visualizing Chemomechanical Degradation of a Solid-State Battery Electrolyte", *ACS Energy Lett.* **4**, 1475–1483 (2019), DOI 10.1021/acsenergylett.9b00816. [EXP (in situ µ-XCT) + COMP (FEM)] [abstract/snippet; author list partly from memory]
  - Interphase growth at Li/LAGP is tied to fracture. The severity of fracture, more than the interphase's own resistance, drives the impedance rise.
  - Cracks start near the edge of the Li/LAGP interface, where FEM predicts stress concentrations.
  - [Source](https://perfilesycapacidades.javeriana.edu.co/en/publications/visualizing-chemomechanical-degradation-of-a-solid-state-battery-/)
- Lewis, J. A.; Cortes, F. J. Q.; …; McDowell, M. T. "Interphase Morphology between a Solid-State Electrolyte and Lithium Controls Cell Failure", *ACS Energy Lett.* **4**, 591–599 (2019) (DOI 10.1021/acsenergylett.8b02496, from memory). [EXP] [abstract/snippet]
  - Li reacting with LAGP gives an amorphous phase that "takes up more space". The resulting stress fractures the electrolyte.
  - The interphase becomes nonuniform at high current, which accelerates failure. Failure comes through impedance rise, not shorting.
  - [Source](https://impact.ornl.gov/en/publications/interphase-morphology-between-a-solid-state-electrolyte-and-lithi/)
- Xiao, Y.; Wang, Y.; Bo, S.-H.; Kim, J. C.; Miara, L. J.; Ceder, G. "Understanding interface stability in solid-state batteries", *Nat. Rev. Mater.* **5**, 105–126 (2020), DOI 10.1038/s41578-019-0157-5. [review] [litdb]
  - LATP|Li: Li insertion gives **130 %** expansion and cracking (the review cites experimental refs 200–202). The impedance rise is attributed to cascading chemo-mechanical degradation rather than to the interphase alone.
  - [Source](https://doi.org/10.1038/s41578-019-0157-5)
- Schwietert, Vasileiadis, Wagemaker, *JACS Au* **1**, 1488 (2021). DFT volumes of metastable (de)lithiated phases of 12 SEs, oxides included. LATP volume decreases on lithiation (1404.34 → 1351.52 Å³), so "lithiation = expansion" is not universal. [COMP] [litdb] — [Source](https://doi.org/10.1021/jacsau.1c00228)
- Riegger, L. M.; Schlem, R.; Sann, J.; Zeier, W. G.; Janek, J. "Lithium-Metal Anode Instability of the Superionic Halide Solid Electrolytes and the Implications for Solid-State Batteries", *Angew. Chem. Int. Ed.* **60**, 6718 (2021), DOI 10.1002/anie.202015238. [EXP] [abstract/snippet]
  - Li|Li3InCl6 is thermodynamically unstable, with continuously growing interphase resistance. In-situ XPS shows In³⁺ reduced to metallic In.
  - No computed volume change was found.
  - [Source](https://zendy.io/title/10.1002/anie.202015238)
- Halide ESW context (theory, as quoted in a halide paper retrieved by the search): Li3InCl6 2.38–4.26 V and Li3YCl6 0.62–4.02 V vs Li. Attribution to the specific Springer paper was not verified. — [Source](https://link.springer.com/content/pdf/10.1007/s40843-020-1580-3.pdf)
- **Molar-volume-ratio descriptor (PBR) from neighboring fields.**
  - An ACS AMI SI ("Porosity of solid electrolyte interphases on …") defines PBR for Li SEI compounds as the molar volume of the Li compound divided by (number of reacted Li × molar volume of Li metal). [Source](https://pubs.acs.org/aamick/article-supplement/578541/pdf/am1c15607_si_001)
  - Wikipedia lists PBR = 0.567 for Li2O. [Source](https://en.wikipedia.org/wiki/Pilling%E2%80%93Bedworth_ratio)
  - A Springer review notes the SEI use of PBR is an empirical adaptation of a concept built for oxides in dry air. [Source](https://link.springer.com/article/10.1007/s11661-024-07658-4)
  - These sources concern liquid-electrolyte SEI or metal oxidation, not SE decomposition.
- **Si anode | sulfide SE.** Wang 2026 computes ΔV/V for a-LixSi (x = 4.40 → 0.00) × 7 sulfide SEs (chemical, and electrochemical over 0–2.5 V), with expansion at x = 0 attributed to SiS2. [COMP] [litdb] — [Source](https://doi.org/10.1002/anie.202519663)

### Inferences
- The oxide precedents (LAGP and LATP) show that SE-side interphase volume expansion can dominate failure. That is the physical motivation for a sulfide-dopant ΔV/V screen. However, in those oxide cases the expansion was **measured or modeled per system**, not screened.
- PBR-type ratios computed from thermodynamic products are a cheap, transplantable "molar-volume ratio" metric. A sulfide-SE version would need the same explicit statement of which Li volume is counted, the same issue as in Q1.

### Gaps
- LiPON and LLZO were **not** specifically searched for computed interphase volumes in this pass. No negative claim can be made for them.
- No computed decomposition ΔV/V was found for halides (Li3YCl6, Li3InCl6) or for LATP/LAGP at the hull level. The oxide numbers above are experimental, or from DFT on metastable intermediates.
- Negative-search log for Q3:
  - "halide solid electrolyte Li3InCl6 Li3YCl6 lithium metal reduction interphase volume expansion computed molar volume chemo-mechanical" → experimental halide-Li reactivity only. The search engine's summary: *"nothing on computed molar volumes or chemo-mechanical modeling"*.
  - "Pilling-Bedworth ratio solid electrolyte interphase lithium metal computed molar volume decomposition" → liquid-SEI PBR only, with no SE-decomposition PBR table.

## Q4. Has anyone combined computed decomposition volume change with mechanics (stress from volume misfit, elastic moduli, fracture criteria) at SE/electrode interfaces?

### Takeaway
Yes, but only in two forms:
1. the Xin Li group's **constrained-ensemble thermodynamics**, which turns reaction strain into a strain-energy penalty through an effective modulus K_eff or a critical modulus K* (design K* "well below 20 GPa"), used for ESW widening and dendrite "dynamic stability";
2. **continuum or mesoscale models** of interphase-growth stress or voiding for specific interfaces (FEM for Li|LAGP; mesoscale for Li|Li6PS5Cl).

No study was found that systematically converts hull-based argyrodite decomposition ΔV/V into interphase stress with SE elastic constants and a fracture criterion (e.g., K_IC), let alone per dopant. Recent MLMD addresses the reverse coupling (pressure → reaction), and operando stack-pressure measurements give experimental signatures of interphase formation.

### Cited Findings
- **Constrained ensemble.**
  - Gil-González 2022: windows at K_eff = 0 / 10 / 20 GPa, e.g. Li5.5PS4.5Cl1.5 (x = 1.5) at 1.70–2.40 V (K_eff = 0) vs 0.80–4.30 V (K_eff = 20 GPa). [litdb] — [Source](https://doi.org/10.1016/j.ensm.2021.12.008)
  - Wang 2022 *JACS Au*: two-parameter space of E_hull and K*, with K* to Li metal "well below 20 GPa". [Source](https://api-pubmed-ncbi.laibokeji.com/35557758)
  - Fitzhugh 2019 *Small*: the choice of decay-morphology model strongly affects the predicted voltage widening. [Source](https://zendy.io/title/10.1002/smll.201901470)
  - Wu 2018: a constant-volume constraint further opens the window. [Source](https://doaj.org/article/cae607d9b42546a0ad6d18336848d877)
- **FEM for interphase-growth stress.** Tippens 2019 (Li|LAGP): FEM-predicted stress concentrations at the interface edge match where cracks start in µ-XCT. [EXP+COMP] — [Source](https://perfilesycapacidades.javeriana.edu.co/en/publications/visualizing-chemomechanical-degradation-of-a-solid-state-battery-/)
- **Mesoscale chemo-mechanics at Li|Li6PS5Cl.** Hao 2023 *AEM* (Mukherjee and Siegel co-authors): decomposition drives voiding in Li (from flux to the reaction front) and in the SE (from the associated volume changes). [COMP+EXP] [abstract] — [Source](https://oa.mg/work/10.1002/aenm.202301338)
- **Reverse coupling, pressure → interfacial reaction.** Jang, K.; Choi, J.; Choi, J. W.; Jung, Y. "Pressure-regulated mechanochemistry at lithium metal–sulfide electrolyte interfaces", arXiv:2609.01088 (2026). [COMP (pressure-aware, charge-resolved ML-MD)] [abstract]
  - About 1 kbar accelerates PS4 decomposition and Li2S-like ordering. 10–100 kbar slows structural rearrangement and long-range crystallization, so the response is nonmonotonic.
  - Uniaxial loading accelerates the reaction relative to isostatic loading at the same nominal pressure.
  - [Source](https://arxiv.org/abs/2609.01088)
- **Operando stack pressure as an interphase signature.** Lee, C.; Han, S. Y.; Lewis, J. A.; Shetty, P. P.; Yeh, D.; Liu, Y.; Klein, E.; Lee, H.-W.; McDowell, M. T. "Stack Pressure Measurements to Probe the Evolution of the Lithium–Solid-State Electrolyte Interface", *ACS Energy Lett.* **6**, 3261–3269 (2021), DOI 10.1021/acsenergylett.1c01395. [EXP]
  - Li symmetric cells with Li10SnP2S12 and Li6PS5Cl. Stack-pressure evolution "sensitively depends on interphase formation", and interphase formation decreases stack pressure during operation.
  - Li-filament growth gives distinct signatures that depend on SE density.
  - [Source](https://figshare.com/articles/journal_contribution/Stack_Pressure_Measurements_to_Probe_the_Evolution_of_the_Lithium_Solid-State_Electrolyte_Interface/16431080); [Source](https://www.peeref.com/works/22939757)
- **Absence of a mechanics conversion in the largest ΔV/V map.** Wang 2026 has no elastic constants, EOS or moduli; ΔV/V is not converted to stress (only the qualitative sentence quoted in Q1). [litdb] — [Source](https://doi.org/10.1002/anie.202519663)
- **Reviews located but not read** (they may compile relevant numbers):
  - "Chemomechanical Degradation at Inorganic Solid Electrolyte–Lithium Metal Interfaces", *Exp. Mech.* (2026), DOI 10.1007/s11340-026-01342-x. [Source](https://link.springer.com/article/10.1007/s11340-026-01342-x)
  - "Pressure-Related Challenges and Strategic Approaches in Lithium Metal Sulfide all-Solid-State Batteries" (PMID 42394421). [Source](https://pubmed.ncbi.nlm.nih.gov/42394421/)
  - "Mechanically Programmed Interfaces in Solid-State Lithium Batteries: Pressure-Driven Strategies for High-Rate Stability", *ChemEngineering* (2026), DOI 10.3390/chemengineering10060076. It states pressure-enhanced decomposition and densification of interphases may raise impedance over time. [Source](https://doi.org/10.3390/chemengineering10060076)

### Inferences
- An **explicit stress estimate** has not been found in the sulfide literature. One example form is a misfit stress from ΔV/V with a composite modulus, compared against SE fracture toughness or yield. The constrained-ensemble approach uses moduli **thermodynamically** (as a free-energy penalty that shifts phase equilibria), not to predict fracture or void nucleation.
- So a screening study that pairs ΔV/V with per-dopant SE elastic constants and a failure criterion would be methodologically distinct from both lines. It must still cite the K_eff/K* formalism as the nearest mechanics coupling.
- Experiments show interphase formation changes stack pressure (Lee 2021) and MLMD shows pressure changes reaction kinetics (Jang 2026). The coupling therefore runs both ways, which a static hull-plus-volume screen cannot capture. This limitation should be stated.

### Gaps
- The formulas for K* and for the constrained decomposition energy, and the numeric K* values for named sulfides, were not verified (full texts blocked).
- Negative-search log for Q4:
  - The query "Chemomechanical Degradation at Inorganic Solid Electrolyte-Lithium Metal Interfaces" interphase volume expansion → only LAGP works (Lewis 2019, Tippens 2019).
  - No source was found that computes interphase stress from hull-derived ΔV/V for any argyrodite.

## Q5. Which works compute electrode volume changes instead? (To separate "electrode ΔV", which is well studied, from "SE-decomposition ΔV", the target.)

### Takeaway
Electrode volume change is mature and quantitative: crystallographic compilations, pressure-dependent OCV "reaction volumes", HT DFT workflows for intercalation volume change, and constriction screens of alloy anodes. It should be cited as background and kept clearly separate from SE-decomposition ΔV/V, for which only the sparse literature in Q1–Q4 exists.

### Cited Findings
- Koerver, R.; Zhang, W.; de Biasi, L.; Schweidler, S.; Kondrakov, A. O.; Kolling, S.; Brezesinski, T.; Hartmann, P.; Zeier, W. G.; Janek, J. "Chemo-mechanical expansion of lithium electrode materials – on the route to mechanically optimized all-solid-state batteries", *Energy Environ. Sci.* **11**, 2142–2158 (2018), DOI 10.1039/C8EE00907D. [EXP + analysis of crystallographic data] [abstract; author list from memory]
  - Summarizes electrode volume changes from crystallographic studies and evaluates the partial molar volume of Li.
  - Measures full-cell "charge/discharge volumes" from pressure-dependent OCV, with changes "in the order of 1 mV/100 MPa". Proposes "mechanical" blending toward zero-strain electrodes.
  - A search summary of the SI mentions LCO expanding about 1.4 % and NCM-811 contracting about 6 % on delithiation. This is unverified, SI-level.
  - [Source](https://pubs.rsc.org/en/content/articlelanding/2018/ee/c8ee00907d); [SI](https://www.rsc.org/suppdata/c8/ee/c8ee00907d/c8ee00907d1.pdf)
- Ye, L.; Lu, Y.; Wang, Y.; Li, J.; Li, X. "Fast cycling of lithium metal in solid-state batteries by constriction-susceptible anode materials", *Nat. Mater.* **23**, 244–251 (2024), DOI 10.1038/s41563-023-01722-x. [COMP+EXP]
  - Micron-Si lithiation is constricted at the surface, so the particles act as a 3D scaffold for Li plating. The constrained ensemble predicts a family of such anodes (Si, Ag, Mg alloys).
  - High-throughput calculation over 59,524 materials. This is electrode-side (anode lithiation) constriction, not SE decomposition.
  - A commentary reports Li–NMC83 pouch cells at about 125 mAh/g initial capacity and about 80 % retention after 6000 cycles.
  - [Source](https://www.nature.com/articles/s41563-023-01722-x.pdf); [Source](https://html.rhhz.net/zghxkb/20250204.htm)
- "High-Throughput-Screening Workflow for Predicting Volume Changes by Ion Intercalation in Battery Materials", *ACS Appl. Energy Mater.*, DOI 10.1021/acsaem.5c03917 (arXiv:2603.10631). [COMP] [abstract] Bulk-host intercalation volume screening; not interfaces, not SE decomposition. — [Source](https://pubs.acs.org/doi/10.1021/acsaem.5c03917); [Source](https://arxiv.org/html/2603.10631v2)
- Kang et al. (our group's review), *Chem. Commun.* **62**, 10277 (2026), DOI 10.1039/d5cc06309d. [review] [litdb, given as known] It discusses electrode volume changes (Ni-rich NCM 6–8 %, Li about 100 %, Li–In 105.6 %), not SE-decomposition volume per dopant. — [Source](https://doi.org/10.1039/d5cc06309d)
- Classic operando pressure work on electrode-driven expansion: Zhang, W.; Schröder, D.; Arlt, T.; Manke, I.; Koerver, R.; Pinedo, R.; Weber, D. A.; Sann, J.; Zeier, W. G.; Janek, J., *J. Mater. Chem. A* **5**, 9929 (2017), DOI 10.1039/C7TA02730C. [EXP] [⚠ title and authors from memory; only the DOI-bearing URL appeared in the search, content not verified] — [Source](https://pubs.rsc.org/en/content/articlehtml/2021/xx/c7ta02730c)
- Li group's anode-side constriction (Su 2020, Ye & Li 2021) mixes both categories. The constriction acts on the **SE decomposition at the anode interface** (target category), but the cell design concerns the Li anode. Cite carefully. — [Source](https://pubs.rsc.org/en/content/articlelanding/2020/ee/c9ee04007b); [Source](https://ideas.repec.org/a/nat/nature/v593y2021i7858d10.1038_s41586-021-03486-3.html)

### Inferences
- The electrode-ΔV literature (Koerver 2018; Kang 2026 review; HT intercalation workflow; Ye 2024) is broad and quantitative. The SE-decomposition-ΔV literature amounts to one heatmap paper (Wang 2026), one constriction line (Xin Li group) and scattered MLIP and mesoscale studies of Li|Li6PS5Cl. This asymmetry supports framing the planned dopant screen as filling the SE-side gap.
- Pressure-OCV "reaction volumes" (Koerver 2018) and stack-pressure signatures of interphases (Lee 2021) are existing experimental routes that could validate a computed SE-decomposition ΔV/V. No paper was found that has done this validation for sulfide SE decomposition.

### Gaps
- Not verified in full text: Koerver 2018's SI numbers; Zhang 2017's content.
- Not searched: Doux et al. (stack pressure, Meng group) and other operando dilatometry or pressure work specific to SE decomposition at the cathode.
- Whether any operando study isolates the SE-decomposition contribution to cell volume or pressure, as opposed to the electrode contribution, was not established. The query "sulfide electrolyte oxidative decomposition molar volume decrease stack pressure drop contact loss composite cathode Li6PS5Cl" returned no direct quantitative source.

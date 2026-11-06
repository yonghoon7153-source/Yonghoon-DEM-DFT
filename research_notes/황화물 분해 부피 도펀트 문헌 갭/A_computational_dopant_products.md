# A — Computational design/screening of dopants in sulfide SEs by the decomposition products they produce ("beneficial decomposition" vs "less decomposition"): literature gap check (to Nov 2026)

*How this was compiled (2026-11-06):* the project's litdb digests were used as already-known sources (text of the digests only; the litdb figure crops were **not** viewed in this session, so any "figure-read" number below is the digest author's reading, not mine). New items come from web search (US index). Two publisher hosts could not be fetched from this session (`advanced.onlinelibrary.wiley.com`, `www.ncbi.nlm.nih.gov`); items that only exist there are reported at abstract/search-summary level and flagged. Labels: **[comp]** computational only, **[exp]** experimental only, **[both]**. "Product properties as design objective" means the computed properties of the decomposition products (gap, Li transport, stability) were used to *choose or rank* the material, not merely discussed afterwards. All numbers are quoted as reported by the source, with its conditions; none are our values.

---

## Q1. Which computational papers compute decomposition products of doped/substituted argyrodites or thiophosphates vs potential (grand potential, interface reaction energy, pseudo-binary mixing)? Which dopants and electrodes? Did they evaluate product properties or only the window?

### Takeaway
Only a small set of computational papers resolve decomposition products for *substituted* thiophosphates, and none uses the properties of those products to rank dopants. They rank by window width, reaction energy or bulk properties of the doped SE, and the product sets appear only as outputs. On the cathode side the computational result is a **negative** for the "wider window" route: substitution does not move the S-limited oxidation onset (Banik 2022 for argyrodites; Ong 2013 for isovalent cations in LGPS). That leaves product quality as the remaining lever, but no one has screened on it. On the anode side, the dopant-specific work is MLIP/AIMD/DFT interface simulation of one to three dopants each (Se/F/O, Zr/F, BH₄⁻, O). None of it is grand-potential screening across many dopants.

### Cited Findings

#### Cathode side (oxidative)
- **Banik, A.; Liu, Y.; Ohno, S.; Rudel, Y.; Jiménez-Solano, A.; Gloskovskii, A.; Vargas-Barbosa, N. M.; Mo, Y.; Zeier, W. G.** "Can Substitutions Affect the Oxidative Stability of Lithium Argyrodite Solid Electrolytes?" *ACS Appl. Energy Mater.* **5**, 2045 (2022), DOI 10.1021/acsaem.1c03599. **[both]**
  - What it computed: grand-potential (phase-stability) windows and "lithium evolution vs potential" profiles (Fig. S5), with the decomposition products in Table S2 and the phase equilibria at the reduction and oxidation potentials in Table S3. It also computed pDOS and COHP for Li₆PS₅Cl, Li₆PS₅I and Si/Ge-substituted Li₆PS₅I. The DFT models were Li₆.₂₅P₀.₇₅Si₀.₂₅S₅I and Li₆.₇₅P₀.₂₅Ge₀.₇₅S₅I; the experiments used Li₆.₆P₀.₄M₀.₆S₅I with M = Si or Ge. The windows read from Fig. 3c on the Li⁺/Li axis are about 1.7–2.3 V for LPSCl and about 1.7–2.4 V for the I, Si and Ge compositions (figure-read in the litdb digest). The products are polysulfides, S and (P–S)ₓ, plus LiX. The paper cites Hakari's result that LiX raises the oxidative stability of thiophosphates. The text does not state the functional, k-mesh, U or disorder treatment. — [Source](https://doi.org/10.1021/acsaem.1c03599) (litdb digest `litdb/papers/banik2022_substitutions_oxidative_stability_argyrodite.md`; bibliographic check via [NSF PAR](https://par.nsf.gov/biblio/10394080))
  - Conclusion: on going from Li₆PS₅Cl to Li₆₊ₓP₁₋ₓMₓS₅I (M = Si⁴⁺, Ge⁴⁺) the oxidative stability does not change. Nonbonding PS₄³⁻ states and free S²⁻ populate the valence-band edge, and "as long as sulfur is part of the solid electrolyte, the oxidative stability will always be limited". The authors therefore point to coatings or other material classes. Product properties were **not** a design objective; the paper is a window study. — [Source](https://aminer.org/pub/61c8514d5244ab9dcb1b7b13/can-substitutions-affect-the-oxidative-stability-of-lithium-argyrodite-solid-electrolytes)
- **Ong, S. P.; Mo, Y.; Richards, W. D.; Miara, L.; Lee, H. S.; Ceder, G.** "Phase stability, electrochemical stability and ionic conductivity of the Li₁₀±₁MP₂X₁₂ (M = Ge, Si, Sn, Al or P, and X = O, S or Se) family of superionic conductors." *Energy Environ. Sci.* (2013), DOI 10.1039/c2ee23355j. The volume and page (6, 148) were not re-verified in this session. **[comp]**
  - It used a two-point Li grand potential (μ⁰ and μ⁰ − 5 eV) with no onset voltages. At 5 V the products are GeS₂ + P₂S₅ + S for Ge/S, but for oxides they are MₓPᵧO_z plus **O₂ release**, which the authors call serious for long-term stability. P₂S₅-type sulfide products "could be good glassy ionic conductors and passivate". Isovalent cation substitution barely changes stability or σ, whereas anion substitution dominates: O makes the phase unstable (E_decomp > 90 meV/atom) and drops σ to 0.03 mS/cm (AIMD). This is the earliest substituted-thiophosphate paper to comment on product quality, but only qualitatively. — [Source](https://doi.org/10.1039/c2ee23355j) (litdb `litdb/papers/ong2013_lgps_family_substitution.md`)
- **Jiang, M.; Chen, Z.-W.; Rao, A.; Chen, L.-X.; Zu, X.-T.; Singh, C. V.** "Se-doped Li₆PS₅Cl and Li₅.₅PS₄.₅Cl₁.₅ with improved ionic conductivity and interfacial compatibility: a high-throughput DFT study." *J. Mater. Chem. C* (2022), DOI 10.1039/d2tc03696g; volume and page not captured. **[comp]**
  - Se on the S(16e) site of PS₄: σ(298 K) 2.592 → 15.397 mS/cm and Ea 0.282 → 0.203 eV (Li₆PS₅₋ₓSeₓCl), and 8.916 → 19.286 mS/cm and Ea 0.244 → 0.144 eV (Li₅.₅PS₄.₅₋ₓSeₓCl₁.₅), all from AIMD.
  - The paper's own interface table shows Se **worsening** cathode compatibility (ΔE_D −302 → −328 meV/atom vs LiCoO₂). The "improved interfacial compatibility" in the title is a comparison with LGPS and Li₃PS₄, not a doping effect (litdb reading).
  - It ranks by σ, bulk gap and reaction energy, not by product properties. — [Source](https://doi.org/10.1039/d2tc03696g) (litdb `litdb/papers/jiang2022_se_doped_lpscl_high_throughput_dft.md`)
- **Wu, X.; Liang, L.; Du, B.; Liu, Y.; Zhang, Z.; Shi, Y.; Tang, S.; Hou, G.; Zhou, H.; He, P.** "High-Conductivity Argyrodite Electrolyte with Self-Passivating Stability for Single-Electrolyte All-Solid-State Lithium Batteries." *Angew. Chem. Int. Ed.* **65** (2026), DOI 10.1002/anie.202523225; litdb records the article number as e23225. **[both]**
  - Computation: a DFT dopant screen of 15 elements (Mo, W, Ce, La, Fe, Y, Cr, As, Bi, Sb, Si, Ge, Sn, Nb, Ta) in Li_yP₀.₉M₀.₁S₄.₅Cl₀.₇₅Br₀.₇₅, ranked by the **bulk PBE band gap of the doped SE**. Undoped is 2.12 eV, Ta 2.66 eV and Nb 2.29 eV; the other 13 elements sit below 2.12 eV.
  - litdb audit: no +U or spin for the Mo, W, Ce, Fe and Cr models, *y* is unspecified, and the AIMD is 300 K for 20 ps.
  - Experiment: Ta⁵⁺ at 6 mol% on the P site gives σ = 12 mS/cm. Ta is reported to form **insulating LiTaO₃ in the CEI** and **metallic Ta⁰ in the SEI**. The "practical ESW 0.1–4.3 V" is a 3rd-cycle CV extrapolation, not a thermodynamic window.
  - Assessment: this is the closest *conceptual* precedent ("self-passivating" through a dopant), but the dopant ranking descriptor is the bulk gap. The products were identified afterwards by XPS rather than predicted and ranked. — [Source](https://doi.org/10.1002/anie.202523225) (litdb `litdb/papers/wu2026_ta_argyrodite_selfpassivating.md`)
- **Wang, K.; Zeier, W. G.; Janek, J.; Mollenhauer, D.** "Interface Stability and Kinetics of Sulfide Electrolytes in all-Solid-State Batteries." *Angew. Chem. Int. Ed.* (2026), DOI 10.1002/anie.202519663. **[comp]**
  - Pseudo-binary plus grand-potential DFT for 7 sulfide SEs across 6 interface types (cathode/SE, SE/interlayer, SE/coating, cathode/interlayer, cathode/coating, LiₓSi/SE).
  - Per the litdb audit, it **never judges the electronic conductivity of the products**. It predicts that the Al dopant of NCA segregates as a separate phase at the interface; that dopant belongs to the cathode, not the SE. — [Source](https://doi.org/10.1002/anie.202519663) (litdb `litdb/papers/wang2026_interface_stability_kinetics_sulfide_assb.md`)
- **Qi, X.; Wu, G.; Wu, M.; Li, D.; Wang, C.; Gao, L.; Zhang, S.; Fan, L.-Z.** "Deciphering and overcoming the high-voltage limitations of halide and sulfide-based all-solid-state lithium batteries." *J. Energy Chem.* **103**, 926 (2025), DOI 10.1016/j.jechem.2024.11.034. **[both]**
  - Cells: NCM85/SE at 4.5 V. DFT: closed-system pseudo-binary reaction energies (Materials Project) plus PBE DOS of the products.
  - Conclusion: LPSC degradation is "self-limited, resulting from high interface reactivity and **partially favorable reaction products**", while Li₂ZrCl₆ degradation is "unlimited", from moderate reactivity and "unfavorable reaction products" (a narrow-gap ZrO₂ product).
  - litdb caveats: XPS did not confirm ZrO₂/Li₂ZrO₃, and products were checked against the cathode only, not against the LPSC side.
  - This compares SE classes and selects a coating (LiZr₂(PO₄)₃); it does not rank dopants. — [Source](https://doi.org/10.1016/j.jechem.2024.11.034) (litdb `litdb/papers/qi2025_high_voltage_limits_halide_sulfide_assb.md`)
- Undoped LPSCl baseline, intrinsic vs decomposition window: **Schwietert, T. K.; Arszelewska, V. A.; Wang, C.; Yu, C.; Vasileiadis, A.; de Klerk, N. J. J.; Hageman, J.; Hupfer, T.; Kerkamm, I.; Xu, Y.; van der Maas, E.; Kelder, E. M.; Ganapathy, S.; Wagemaker, M.** "Clarifying the relationship between redox activity and electrochemical stability in solid electrolytes." *Nat. Mater.* **19**, 428 (2020), DOI 10.1038/s41563-019-0576-0. **[both]**
  - Li₆PS₅Cl first oxidizes at 2.24 V to Li₄PS₅Cl, keeping its framework (S²⁻ → S⁰), and reduces at 1.08 V to Li₁₁PS₅Cl (P⁵⁺ → P⁰).
  - These intermediates then decompose to Li₃PS₄ + S + LiCl on the oxidation side and P + Li₂S + LiCl on the reduction side.
  - The observed window is set by intermediate formation (1.16 V), not by the predicted direct decomposition (≈0.3 V), and agrees with the measured 1.25 V. — [Source](https://doi.org/10.1038/s41563-019-0576-0) (litdb `litdb/papers/schwietert2020_redox_activity_vs_electrochemical_stability.md`)
- Experimental, the closest *cathode-side* analogue to the planned idea: **Hartel, J.; Banik, A.; … Zeier, W. G.** "Investigating the Influence of Transition Metal Substitution in Lithium Argyrodites on Structure, Transport, and Solid-State Battery Performance." *Chem. Mater.* **36**, 10731 (2024), DOI 10.1021/acs.chemmater.4c02281; full author list not retrieved. **[exp]**
  - Stated aim: **tune the CEI composition** through Zn²⁺ substitution, in Li₅.₅₋₂ₓZnₓPS₄.₅Cl₁.₅ and Li₆₋₂ₓZnₓPS₅Br (0 ≤ x ≤ 0.15).
  - Zn sits on Li sites (neutron and X-ray refinement). In NCM-83 half-cells Zn speeds up decomposition kinetics and changes the CEI composition. No computed product screening (abstract level). — [Source](https://impact.ornl.gov/en/publications/investigating-the-influence-of-transition-metal-substitution-in-l/); [X-MOL abstract](https://x-mol.com/paper/1852782697355485184)

#### Anode side (reductive)
- Ong 2013, 0 V side: every composition reduces to **Li₂X + Li₃P + LiₓM_y alloy**; for Ge/S this is Li₁₅Ge₄ + Li₂S + Li₃P. The text says these products are "relatively good Li⁺ conductors" (so a conductive SEI is possible) but that "the presence of metallic products is a concern". — [Source](https://doi.org/10.1039/c2ee23355j) (litdb `ong2013` digest)
- **Zhu, Y.; He, X.; Mo, Y.** "Strategies Based on Nitride Materials Chemistry to Stabilize Li Metal Anode." *Adv. Sci.* **4**, 1600517 (2017), DOI 10.1002/advs.201600517. **[comp]**
  - Database-wide first-principles analysis: nitride anion chemistry is uniquely more stable against Li than oxides, sulfides and halides.
  - The authors **propose nitride materials and high nitrogen doping to form a stable SEI**. Of everything found, this is the clearest *computational* proposal of the "N → Li₃N-type interphase by design" idea, though without SE-dopant screening (abstract level). — [Source](https://doi.org/10.1002/advs.201600517); [UMD DRUM](https://drum.lib.umd.edu/handle/1903/19716)
- **Lai et al.** "Machine-learning-accelerated mechanistic exploration of interface modification in lithium metal anode." *npj Comput. Mater.* **11**, 245 (2025), DOI 10.1038/s41524-025-01747-7; full author list not captured. **[comp]**
  - Method: hybrid AIMD ↔ MTP ("HAML") for Li(100)|Li₆PS₅Cl(100) at 300 K, 528 ps–1 ns, 23–46× cheaper than pure AIMD.
  - Doped models: Li₆PS₄.₇₅Se₀.₂₅Cl, Li₆PS₅Cl₀.₅F₀.₅ and Li₆PS₄.₇₅O₀.₂₅Cl, at the minimum concentrations the supercell allows.
  - The paper claims doping makes the protective layer form faster. litdb notes that in SI Fig. S14 the reaction ends at about 20 ps in all four systems with little difference between them. No product-property ranking. — [Source](https://doi.org/10.1038/s41524-025-01747-7) (litdb `litdb/papers/lai2025_haml_li_metal_lpscl_interface_doping_seFO.md`)
- "First-Principles Calculation Study on the Interfacial Stability Between Zr and F Co-Doped Li₆PS₅Cl and Lithium Metal Anode." *Batteries* (MDPI) **11**(12), 456; year shown as 2025 in the search index; authors not retrieved. **[comp]**
  - Model: VASP/PBE, Li₆P₀.₉Zr₀.₁S₄.₉F₀.₁Cl against Li. The maximum interfacial strain rises from 6% to 12%, and the interfacial Li⁺ migration barrier falls by 36%.
  - The authors argue that F binds Li⁺ to form LiF. This is one dopant pair, not a screen. — [Source](https://www.mdpi.com/2313-0105/11/12/456)
- **Wang et al. (incl. H. Fang, P. Jena, D. Mitlin)** "Understanding the Role of Borohydride Doping in Electrochemical Stability of Argyrodite Li₆PS₅Cl Solid-State Electrolyte." *Adv. Mater.* (2025), DOI 10.1002/adma.202506095. **[both]** (abstract level; the Wiley and PMC hosts were blocked)
  - Performance: 5 wt% BH₄⁻ is optimal; the CCD is 7.3 vs 2.6 mA cm⁻² for the baseline.
  - SEI: a tri-layer of Li₃P, LiBH₄ and Li₂S that blocks electrons while conducting ions.
  - Theory: substitution has a limited effect on the thermodynamic stability of PS₄³⁻, which still decomposes on contact with Li, and higher substitution levels (25–62.5%) further destabilize PS₄. The benefit is framed as "site-specific kinetic", i.e. an interphase effect rather than bulk thermodynamics. — [ORNL record](https://impact.ornl.gov/en/publications/understanding-the-role-of-borohydride-doping-in-electrochemical-s/); [OSTI](https://www.osti.gov/biblio/3015583)
- **Yang et al.** "Enhanced Ionic Conductivity at the Solid Electrolyte Interphase of Oxygen-Doped Li₆PS₅Cl." *Adv. Sci.*, DOI listed as 10.1002/advs.76563; year and authors not verified, search-summary level only. **[comp, MLIP-MD; experimental content unknown]**
  - Reported: moderate O doping is preferable because excess O hurts both bulk conductivity and interphase stability, and the interfacial reactions are largely insensitive to the anti-site ratio. This is the only item found that evaluates a **product (SEI) transport property as a function of dopant content**, but for a single dopant. — [Source (search listing)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13360120/); [publisher listing](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.76563)
- "Insights on the Properties of the O-Doped Argyrodite Sulfide Solid Electrolytes (Li₆PS₅₋ₓClOₓ, x = 0–1)." *ACS Appl. Mater. Interfaces* **13**, 54924 (2021), DOI 10.1021/acsami.1c14573; authors not retrieved. **[both]**
  - Li₆PS₄.₇₅ClO₀.₂₅ reaches 4.7 mS cm⁻¹ (cold-pressed), against 4.2 for undoped.
  - O doping improves stability against Li metal (CV and XRD), and a LiCoO₂ cell retains 86% after 250 cycles. The snippets show no product-resolved interface model. — [Source](https://www.pubmed.gov/34779200/)
- Undoped product transport at Li metal: **Wang, Panchal, Sai Gautam & Canepa** "The resistive nature of decomposing interfaces of solid electrolytes with alkali metal electrodes." *J. Mater. Chem. A* **10**, 19732 (2022), DOI 10.1039/d2ta02202h. Given names not captured. **[comp]**
  - Method: static DFT adhesion for 20 metal|binary-product interfaces, plus interface-specific MTP MD (8320 atoms, 10–20 ns) for Li|Li₂S, Li|Li₃P and Li|LiCl.
  - Result: **Li₃P conducts while Li₂S and LiCl block**. Because the decomposition stoichiometry gives Li₂S in about 5× excess, the argyrodite|Li interface is overall resistive.
  - It evaluates product properties, but for the undoped SE only. — [Source](https://doi.org/10.1039/d2ta02202h) (litdb `litdb/papers/wang2022_resistive_decomposing_interfaces_se_alkali_metal.md`)
- **Li, B. Y.; Karan, V.; Kaplan, A. D.; Wen, M.; Persson, K. A.** "An Atomistic Study of Reactivity in Solid-State Electrolyte Interphase Formation for Li/Li₇P₃S₁₁." *J. Phys. Chem. C* **129**, 16043 (2025), DOI 10.1021/acs.jpcc.5c03589. **[comp]**
  - An active-learning MLIP framework for interfacial reactivity. It finds a layered amorphous interphase in the order Li/Li₃P → LiₓP → Li₂S → mixed Li₂S–LiₓP → Li₇P₃S₁₁.
  - "Passivation of the interface is shown as the ionic fluxes all approach zero." No dopants. — [Source](https://www.osti.gov/biblio/2998199)
- Kim, J. S. et al. "Deciphering Li₂S-like SEI Formation Mechanism at Li/Argyrodite Anodic Interfaces via Large-Scale Machine-Learned Reactive Dynamics." SSRN preprint, abstract 6020397. **[comp]**
  - Method: MTP (optB88-vdW labels) with active learning; Li(100)|Li₆PS₅Cl(100), about 7,000 atoms, 20 ns at 350 K.
  - PS₄ decomposition starts immediately and builds an S-rich amorphous layer of about 6 nm; Li₂S-like crystals nucleate at about 11 ns. No dopants. — [Source](https://ssrn.com/abstract=6020397) (litdb `litdb/papers/kim2026_li_argyrodite_sei_reactive_md.md`)
- Generic undoped thiophosphate|Li DFT: Marana et al. (2023) propose Li₂S as a passivating layer between β-Li₃PS₄ and Li — [Source](https://iris.unito.it/retrieve/handle/2318/1952790/1230919/marana-et-al-2023-stability-and-formation-of-the-li3ps4-li-li3ps4-li2s-and-li2s-li-interfaces-a-theoretical-study.pdf). Zhou, Luo & An (*J. Mater. Chem. A*, 2026) state that thiophosphates decompose to Li₂S/Li₃P and that the initial products passivate — [Source](https://pubs.rsc.org/en/content/articlehtml/2026/ta/d6ta01253a). Both are search-summary level; titles and authors were not fully retrieved.

### Inferences
- Across all of these, the decomposition **products of doped argyrodites as a function of potential, on both electrode sides, are not tabulated anywhere for more than about three dopants at a time**. Banik covers Si/Ge/I (cathode side), Jiang covers Se (cathode reaction energy), Ong covers M/X in LGPS at only two μLi points, and the anode-side MLIP/DFT papers cover one to three dopants each.
- The Banik/Ong "substitution doesn't move the onset" result is itself the argument for product-based ranking. If the S-limited onset is pinned for essentially all dopants, ranking by window width cannot separate dopants on the cathode side. This matches the project's internal record that most dopants in the internal cascade leave the oxidation onset unchanged (location: banik2022 digest §7; check the internal registry before quoting any number).
- On the anode side the literature is split on whether dopant-derived metals or alloys are good or bad. Ong 2013 calls them "a concern"; Wu 2026 reports metallic Ta⁰ in a well-performing SEI; Sundar 2025 (Q2) finds Li-alloy-forming coatings good. A product-quality descriptor therefore has to state its stance on minority metallic phases explicitly.
- Wang/Mitlin (2025) and Lai (2025) both suggest that the measurable benefit of doping at Li metal may be kinetic or site-specific rather than visible in the thermodynamic product set. That is a direct risk to a purely grand-potential product ranking and should be pre-registered as a limitation.

### Gaps
- No computational paper was found that tabulates grand-potential product sets vs potential for a **series** of dopants in Li₆PS₅Cl on both the cathode and the Li side.
- Abstract-level only (full text not read): Zhu, He & Mo 2016 (*J. Mater. Chem. A* 4, 3253, DOI 10.1039/C5TA08574H — the abstract says interphase formation is thermodynamically favorable at many SE/electrode interfaces and that interphase properties strongly influence performance; [Source](https://pubs.rsc.org/af/content/articlelanding/2016/ta/c5ta08574h)), the BH₄⁻ paper, the Yang O-doped SEI paper, the MDPI Zr/F paper, and the 2021 O-doped ACS AMI paper. Author lists for Hartel 2024, Lai 2025, the MDPI paper, Yang and the ACS AMI 2021 paper are incomplete.
- The first two author names of Schwietert 2020 were not visible in the litdb text I read (14 authors; the rest were checked against the digest).
- The two blocked hosts (`advanced.onlinelibrary.wiley.com`, `www.ncbi.nlm.nih.gov`) have to be allowed in the session's network settings before the BH₄⁻ and O-doped SEI papers can be read in full.

---

## Q2. Has anyone explicitly proposed or screened a "self-forming / in situ passivating interphase by design" via dopant choice, computationally? Is there any HT or ML screening with interphase product quality as the target?

### Takeaway
- **Stated computationally:** the design principle has been stated, mostly qualitatively, by Ong 2013, Zhu 2015, Richards 2016 and Zhu 2017 (which proposes nitrogen doping), with Nolan 2021 adding that "a limited amount of minor reaction may be beneficial".
- **Operationalized for coatings and surface layers:** Tian 2019 (reactivity-guided), Sundar 2025 (screening on the products' Li barrier and gap) and Qian 2025 (engineered stable decomposition products).
- **Whole-material classification:** Lomeli 2024 classifies whole SEs as passivating vs reactive against Li metal (HT ML).
- **Dopants inside the SE:** the idea is common in experimental work from 2021 to 2026 (≥ 12 papers: F → LiF, N → Li₃N, O → Li₂O or Li₃PO₄, Br → LiBr, Ta → LiTaO₃, Zn → CEI tuning, BH₄⁻, Y/O, La/O, Sn/Sb/I, In/F, Ga/F, Nd/O). However, **no computational study was found that screens or ranks SE dopants by the computed properties of their decomposition products.**
- **HT/ML dopant screens that do exist** target the bulk gap, E_hull, window or σ: Jung 2026 (LGPS, 2,550 compositions), Wu 2026 (15 elements), Jiang 2022, Muy 2025 (24 dopants in Li₇PS₆), Kong 2026 (E2I ML) and a Na-argyrodite Pareto screen.
- **Nearest dopant-selection proposal:** Kim 2026 (*Nat. Commun.*) proposes choosing dopants by a product property (atomic volume) for moisture protection, but computes no dopants.

### Cited Findings

#### Computational statements of the principle (no dopant ranking)
- **Zhu, Y.; He, X.; Mo, Y.** "Origin of Outstanding Stability in the Lithium Solid Electrolyte Materials: Insights from Thermodynamic Analyses Based on First-Principles Calculations." *ACS Appl. Mater. Interfaces* **7**, 23685 (2015), DOI 10.1021/acsami.5b07517. **[comp]**
  - Grand-potential windows for 14 Li SEs: the intrinsic sulfide windows are about 1.6–2.3 V.
  - The observed "0–5 V stability" comes from kinetic overpotential plus **passivation by electronically insulating decomposition interphases**. If a product is electronically conductive (Li–Ge alloy, Ti³⁺), passivation fails and decomposition continues. Coatings are framed as artificial SEIs that extend the sulfide anodic limit from about 2–2.3 V to about 4 V. — [Source](https://doi.org/10.1021/acsami.5b07517) (litdb `litdb/papers/zhu2015_esw_grand_potential_origin.md`)
- **Richards, W. D.; Miara, L. J.; Wang, Y.; Kim, J. C.; Ceder, G.** "Interface Stability in Solid-State Batteries." *Chem. Mater.* **28**, 266 (2016), DOI 10.1021/acs.chemmater.5b04082. **[comp]**
  - Defines closed (eq. 2) and Li-open (eq. 4) pseudo-binary reaction energies and tabulates products and driving forces for about 30 electrolytes × 7 cathodes.
  - Thiophosphates react strongly with oxide cathodes (forming PO₄ and transition-metal sulfides), so coatings are needed. Several SEs (Li₃PS₄, LiPON, …) are unstable against Li but **self-passivate** because their products (Li₂S or Li₂O + Li₃P) are electronically insulating and Li-conducting. — [Source](https://doi.org/10.1021/acs.chemmater.5b04082) (litdb `litdb/papers/richards2016_interface_stability_pseudobinary.md`)
- Zhu, He & Mo 2017 (*Adv. Sci.* 4, 1600517) proposes "high nitrogen doping to form stable solid-electrolyte-interphase". This is the only explicit computational *doping-for-interphase* proposal found, and it is at the level of anion chemistry, not a dopant screen. — [Source](https://doi.org/10.1002/advs.201600517)
- **Nolan, A. M.; Wachsman, E. D.; Mo, Y.** "Computation-guided discovery of coating materials to stabilize the interface between lithium garnet solid electrolyte and high-energy cathodes for all-solid-state lithium batteries." *Energy Storage Mater.* **41**, 571 (2021), DOI 10.1016/j.ensm.2021.06.027. **[comp]**
  - The selection rule is relaxed from E_d = 0 to |E_d| < 0.05 eV/atom, with the statement "a limited amount of minor reaction may be beneficial … strong chemical bonding" (for adhesion). This applies to garnet-cathode coatings, not sulfides. — [Source](https://doi.org/10.1016/j.ensm.2021.06.027) (litdb `litdb/papers/nolan2021_garnet_cathode_coating.md`)

#### Operational precedents on coatings and surface layers (closest methodological analogues)
- **Sundar, A.; Kim, T.; Lagunas, F.; Mane, A. U.; Eze, U. D.; Ginter, C.; Pathak, R.; Tepavcevic, S.; Elam, J. W.; Hood, Z. D.; Zapol, P.; Connell, J. G.** "Computationally-Guided Development of Sulfide Solid Electrolyte Powder Coatings." *Adv. Sci.* **12**, e13191 (2025), DOI 10.1002/advs.202513191. **[both]**
  - A two-stage DFT screen of binary-oxide coatings on LPSCl powder:
    1. interface decomposition energy (pymatgen InterfaceReactions, at the electrolyte, Li and cathode interfaces) and bulk/slab gaps (HSE06);
    2. the **decomposition products' Li migration barriers and band gaps**.
  - Validation: ALD MgO, ZrO₂ and ZnO.
  - Conclusion: the most predictive metric is **the ionic/electronic conductivity of the interfacial decomposition products formed with LPSCl and Li metal**, not the coating's own thermodynamic stability. Li-conductive oxides plus Li-alloy formation are good at the anode; MgO is best overall; ZnO raised σ_e, contrary to expectation.
  - This is the closest published instance of "rank by product properties", but for coatings, not dopants. — [Source](https://doi.org/10.1002/advs.202513191) (litdb `litdb/papers/sundar2025_oxide_coating_screening_lpscl.md`)
- **Qian, L.; Huang, Y.; Dean, C.; Kochetkov, I.; Singh, B.; Nazar, L. F.** "Engineering Stable Decomposition Products on Cathode Surfaces to Enable High Voltage All-Solid-State Batteries." *Angew. Chem. Int. Ed.* (2025), e202413591, DOI 10.1002/anie.202413591. **[both]**
  - Coating: LiPO₂F₂ at 1 wt% (25–35 nm, amorphous) on NCM85. The DFT convex hull predicts a **LiF + LiPₓOᵧF_z + LiPO₃ CEI** that suppresses Li₆PS₅Cl oxidation.
  - Cycling: 81.4% vs 56.0% (bare) after 200 cycles (2.8–4.3 V, 0.2 C); R_cathode 90 vs 200 Ω cm².
  - This is *cathode-side* "design the decomposition products", through a coating rather than an SE dopant. — [Source](https://doi.org/10.1002/anie.202413591) (litdb `litdb/papers/qian2025_lipo2f2_coating_stable_cei.md`)
- **Tian, Y.; Sun, Y.; Hannah, D. C.; Xiao, Y.; Liu, H.; Chapman, K. W.; Bo, S.-H.; Ceder, G.** "Reactivity-Guided Interface Design in Na Metal Solid-State Batteries." *Joule* **3**, 1037 (2019), DOI 10.1016/j.joule.2018.12.019. **[both]**
  - A hydrate surface layer on Na₃SbS₄, formed by air exposure, reacts with Na metal to give an **ionically conductive passivating interphase** that can re-form when damaged.
  - This is the canonical "choose the surface chemistry by its reaction products" paper, but for Na, an anode-side surface layer and no dopant. — [eScholarship](https://escholarship.org/uc/item/6b24r92b); [Ceder group PDF](https://ceder.berkeley.edu/publications/2018_Yaosen_Na_hydrate_coating.pdf)

#### HT/ML classification with "passivation" as the target (whole materials, not dopants)
- **Lomeli, Ransom, Ramdas, Jost, Moritz, Sendek, Reed & Devereaux.** "Predicting Reactivity and Passivation of Solid-State Battery Interfaces." *ACS Appl. Mater. Interfaces* **16**, 51584 (2024), DOI 10.1021/acsami.4c06095. Given names not captured. **[comp]**
  - Data: AIMD of 67 SE candidates against Li metal (550 K, 40–60 ps, ≤ 150 atoms), each labeled stable, passivating or reactive.
  - Models: two logistic regressions, applied to 3,535 Materials Project structures.
  - Result: stable 533 + passivating 788 = 1,321 materials, against 229 under the |ΔE_rxn| < 100 meV/atom rule. LiB₁₃C₂ and LiB₁₂PC were confirmed.
  - This is the only HT/ML work found with "passivating" as an explicit target class. Passivation is judged from interface-normal MSD, not from product properties, and there are no dopants or cathode side. — [Source](https://doi.org/10.1021/acsami.4c06095) (litdb `litdb/papers/lomeli2024_predicting_reactivity_passivation_ssb_interfaces.md`)

#### HT/ML dopant screens that exist (all target bulk or window quantities)
- **Jung et al.** "Scalable AI-accelerated design of dual-doped LGPS electrolytes for next-generation solid-state batteries." *eTransportation* (2026), 100570, DOI 10.1016/j.etran.2026.100570; full author list not captured. **[comp]**
  - Search space: 40 dopants × 4 sites × 9 site-pair templates, giving 2,550 compositions.
  - Funnel: ML E_form < 0 and E_hull < 0.025 (2,065 left) → ML E_gap > 2.0 eV (987) → ML G_VRH > 8.4 GPa and G/K < 0.7 (873) → **DFT ECW ≥ 0.58 V** (21) → AIMD σ for 4 compositions.
  - It has **no interface axis**. Its headline is Li₉P₃OS₁₁ at 17.28 mS/cm (extrapolated to 300 K, Ea 209 meV). — [Source](https://doi.org/10.1016/j.etran.2026.100570) (litdb `litdb/papers/jung2026_scalable_ai_dual_doped_lgps.md`)
- Wu 2026: a 15-element dopant screen on the bulk PBE gap (see Q1). — [Source](https://doi.org/10.1002/anie.202523225)
- **Muy et al.** "Optimizing Ionic Conductivity of Lithium in Li₇PS₆ Argyrodite via Dopant Engineering." *Chem. Mater.* (2025), DOI 10.1021/acs.chemmater.4c01049. **[both]** Automated defect thermodynamics (AiiDA-defects) for 24 substitutional dopants plus DeePMD; the target is conductivity. — [Source](https://doi.org/10.1021/acs.chemmater.4c01049) (litdb `litdb/papers/muy2025_li7ps6_dopant_engineering_conductivity.md`)
- **Kong et al.** "From Composition to Ionic Conductivity: Machine Learning-Guided Discovery and Experimental Validation of Argyrodite-Type Lithium-Ion Electrolytes." *Small* (2026), DOI 10.1002/smll.202509918. **[both]** A composition-only "E2I" model predicts conductivity; the best co-substituted compound reaches 7.2 × 10⁻³ S cm⁻¹ (Ea 0.20 eV). There is no window or interphase target. — [Source](https://pubmed.ncbi.nlm.nih.gov/41255030/)
- A virtual Na-argyrodite screen (Sejong University) uses E_hull, E_f, E_g and the window in a 4-D Pareto sort to reach 15 compounds; the window is the stability target. Journal details not retrieved. — [Source](https://sejong.elsevierpure.com/en/publications/discovering-virtual-na-based-argyrodites-as-solid-state-electroly-2/)
- Earlier HT workflow precedent: Deng et al. (Materials Virtual Lab), "Data-Driven First-Principles Methods for the Study and Design of Alkali Superionic Conductors," *Chem. Mater.* (2017), DOI 10.1021/acs.chemmater.6b02648. It uses Li₆PS₅Cl as a test case for phase stability, electrochemical stability and σ, and notes that DFT can suggest doping strategies; there is no product-property target. — [Source](https://materialsvirtuallab.org/pubs/10.1021_acs.chemmater.6b02648.pdf)
- Kim et al., "Moisture-induced surface degradation mechanism of argyrodite Li₆PS₅Cl under dry-room conditions." *Nat. Commun.* (2026), DOI 10.1038/s41467-026-75537-0. **[both]**
  - All moisture-decomposition products (LiCl, Li₃PO₄, Li₂SO₄, LiOH, Li₂CO₃) have smaller atomic volumes than pristine LPSC (Materials Project volumes), so the surface layer contracts and becomes porous rather than protective.
  - The authors suggest **selecting dopants that promote decomposition products with sufficient atomic volumes** so that they form stable protective layers. **No dopant was calculated** (litdb).
  - This is a product-based dopant-selection *proposal*, for moisture rather than electrochemistry. — [Source](https://www.nature.com/articles/s41467-026-75537-0) (litdb `litdb/papers/kim2026_moisture_surface_degradation_lpscl_dryroom.md`)

#### Experimental "dopant → in situ beneficial interphase" claims (no computed product ranking)
*Cathode side*
- Wu 2026: Ta → insulating LiTaO₃ in the CEI (XPS). — [Source](https://doi.org/10.1002/anie.202523225)
- Hartel 2024: Zn²⁺ substitution with the stated aim of tuning the CEI composition. — [Source](https://impact.ornl.gov/en/publications/investigating-the-influence-of-transition-metal-substitution-in-l/)
- **Kang, J.; Lee, Y.; Lee, T. Y.; Oh, G.; Nam, S.-C.; Kwon, O.; Lee, J.-W.** "Dendrite-tolerant fast-kinetics design for all-solid-state lithium-metal batteries via site-specific customized sulfide electrolytes." *Energy Storage Mater.* **90**, 105335 (2026), DOI 10.1016/j.ensm.2026.105335. **[exp; zero calculations]**
  - Design: an O-substituted LPSOC catholyte (about 1 µm), with R_int 74.0 → 47.3 Ω cm² after 100 cycles; Cl-rich LPSC₁.₆ as the separator; an M-SE layer at the Li interface (CCD 3.5 vs 1.7 mA cm⁻² at 45 °C).
  - The authors attribute part of the benefit to a **Li₃PO₄-type interphase that is electronically insulating**. The Li₃PO₄ gap of 7.4 eV is a cited value, and the Li₃PO₄ XPS component after 5 cycles is small (figure-read in litdb). — [Source](https://doi.org/10.1016/j.ensm.2026.105335) (litdb `litdb/papers/kang2026_site_specific_customized_se_dendrite_tolerant_li_metal.md`)

*Anode side*
- Mg/F co-doping → in situ insulating LiF layer. CCD 0.6 → 1.4 mA cm⁻², symmetric cell 90 → 1800 h, σ_e 8× lower. **Liu, C.; Chen, B.; Zhang, T.; Zhang, J.; Wang, R.; Zheng, J.; Mao, Q.; Liu, X.**, *Angew. Chem. Int. Ed.* **62**, e202302655 (2023). **[both]** — [Source](https://doi.org/10.1002/anie.202302655)
- N doping → in situ Li₃N-rich interface. Li₆.₂₅PS₄.₇₅N₀.₂₅Cl; CCD 1.52 mA cm⁻² (RT); > 1000 h. Liu et al., *J. Mater. Chem. A* (2021), DOI 10.1039/D1TA03343C. **[exp, per search summary]** — [Source](https://doi.org/10.1039/D1TA03343C)
- F doping, Li₆PS₅F₀.₅Cl₀.₅ (about 3.5 × 10⁻⁴ S/cm RT) → SEI containing Li₃P + LiCl + LiF. *ACS AMI* (2022). **[exp]** — [Source](https://www.osti.gov/pages/biblio/1867866-synthesis-fluorine-doped-lithium-argyrodite-solid-electrolytes-solid-state-lithium-metal-batteries)
- Y/O co-doping (Li₆.₁P₀.₉₅Y₀.₀₅S₄.₉₂₅O₀.₀₇₅Cl).
  - Effects: Li₂S/Li₃P formation at Li cut by more than half, plus an in situ Li₂O protective layer; σ_e 6.33 → 1.55 × 10⁻⁷ S/cm; CCD 1.5 mA cm⁻².
  - Citation: Wang, D.; Liu, C.; … Liu, X., "Electronic Localization Enables Long-Cycling Sulfides-Based All-Solid-State Lithium Batteries," *Angew. Chem. Int. Ed.* **64**, e202501411 (2025). **[exp + DFT/BVSE auxiliary]** — [Source](https://doi.org/10.1002/anie.202501411)
- CuBr₂ → LiCl/LiBr insulating SEI (product PDOS gaps; see Q4).
  - Effects: CCD 0.6 → 1.9 mA cm⁻²; σ_e 1.02 × 10⁻⁸ → 3.35 × 10⁻⁹ S/cm (measured).
  - Citation: **Li, Y.; Wu, G.; Fan, X.; Li, D.; Liu, H.; Zhao, X.; Ren, W.; Lei, P.; Zhao, X.; Wang, X.; Wang, G.; Gao, L.; Nan, C.-W.; Fan, L.-Z.**, *Energy Storage Mater.* **77**, 104221 (2025). **[both]** — [Source](https://doi.org/10.1016/j.ensm.2025.104221)
- La₂O₃ → La⁰ + LiCl SEI (the paper also claims LaCl₃); CCD 0.9 → 3.1 mA cm⁻². *Electrochim. Acta* (2025), DOI 10.1016/j.electacta.2025.146619. **[exp]** — [Source](https://doi.org/10.1016/j.electacta.2025.146619)
- Sn⁴⁺/Sb⁵⁺/I⁻ → in situ LiI + Li–Sn/Sb alloy interface. *J. Mater. Chem. A* (2024), DOI 10.1039/d4ta03873h. **[exp + NEB]** — [Source](https://doi.org/10.1039/d4ta03873h)
- In/F and Ga/F co-doping (Fan group): Li–Ga alloy for plating homogenization plus F for electronic insulation. The digests did not capture DOIs. — [litdb](litdb/papers/li2024_inf3_argyrodite_ultrathin_film.md); [litdb](litdb/papers/liyaru_gaf3_codoping_argyrodite.md)
- BH₄⁻ → Li₃P/LiBH₄/Li₂S tri-layer SEI. **[both]** — [Source](https://impact.ornl.gov/en/publications/understanding-the-role-of-borohydride-doping-in-electrochemical-s/)
- Nd–O co-doping (Li₅.₃₊₂ₓP₁₋ₓNdₓS₄.₃₋₁.₅ₓO₁.₅ₓCl₁.₇, x = 0.025).
  - Effects: CCD 2.29 → 6.62 mA cm⁻²; the "Li–Nd alloy SEI" mechanism is presumed, with zero calculations.
  - Citation: Xu, C. et al., *Nano Energy* (2026), DOI 10.1016/j.nanoen.2026.112246. **[exp]** — [Source](https://doi.org/10.1016/j.nanoen.2026.112246)
- Related, but a multilayer "beneficial decomposition" design rather than a dopant: **Ye, L.; Li, X.** "A dynamic stability design strategy for lithium metal solid state batteries." *Nature* **593**, 218 (2021), DOI 10.1038/s41586-021-03486-3. A less-stable middle electrolyte decomposes locally and "fills cracks" ("expansion screw"); NMC811 retains 82% after 10,000 cycles at 20C (abstract). This overlaps with topic B (decomposition volume). — [Source](https://ideas.repec.org/a/nat/nature/v593y2021i7858d10.1038_s41586-021-03486-3.html)

### Inferences
- The "beneficial decomposition by dopant" idea is mainstream in the **experimental** literature. It has been argued since 2013–2017 in **computational** thermodynamics papers (passivation needs electronically insulating, Li-conducting products). It has been turned into a **computational screen only for coatings** (Sundar 2025; Qian 2025 as a single-candidate design) and for **whole-material passivation classification** (Lomeli 2024). The specific combination targeted by the planned study did not turn up in any search: SE dopant → grand-potential product set vs potential on both sides → ranking by product properties, contrasted with ranking by window.
- The planned study has three closest prior works, one per axis: Sundar 2025 for the method (product-property screening, but for coatings); Wu 2026 for the concept (one dopant, self-passivating, but ranked by bulk gap with products found by XPS); and Lomeli 2024 or Jung 2026 for the HT/ML framing (passivation class for whole materials, and window-based dopant funnel, respectively). A novelty statement should be positioned against these three.
- Because experimental papers already *claim* dopant-specific interphases (LiF, Li₃N, Li₂O, LiBr, LiTaO₃, Li₃PO₄, Ta⁰/La⁰/Li–M alloys), a computed product atlas could serve as a **consistency check** of those claims. That is a value proposition the literature has not met, and a first test of it would be Wu 2026's XPS-observed Ta⁰ against the product predicted for a Ta-bearing product at Li potential (see Q4).

### Gaps
- No computational SE-dopant screen ranked by product properties was found, whether published or preprinted (arXiv/ChemRxiv were reached only through the general web index). The search engine is a US index and may under-cover Chinese- or Korean-language venues and very recent (2026 Q3–Q4) items.
- "Wang et al. reactivity-guided interface design" from the task brief could not be uniquely identified. The candidates are Tian 2019 (Ceder) and Wang/Canepa 2022, which is about resistive decomposing interfaces rather than reactivity-guided design. The name may refer to a different paper.
- **Negative-search log** (queries that returned no paper ranking SE dopants by computed decomposition-product properties):
  1. "dopant screening argyrodite Li6PS5Cl decomposition products interphase high-throughput DFT" (extended) → none. It surfaced the BH₄⁻ paper, F-doping experiments and Kim 2026 *Nat. Commun.* (moisture proposal).
  2. "fluorine-doped argyrodite in situ LiF interphase grand potential DFT decomposition Li metal" → no grand-potential F-doped study; MDPI Zr/F DFT only.
  3. "nitrogen doped Li6PS5Cl Li3N interphase lithium metal first-principles" → experimental only (Liu 2021); SEI-component DFT (Chen 2026).
  4. "machine learning screening substituted argyrodite electrochemical stability window dopants 2025" (extended) → no argyrodite window ML; LGPS (Jung 2026), Na-argyrodite Pareto, E2I conductivity.
  5. "design principles self-forming interphase solid electrolyte decomposition products passivating computational screening lithium metal" (extended) → only liquid-electrolyte analogues (arXiv 1903.09593; *Nat. Commun.* 2023 multiscale SEI) and Li/Li₇P₃S₁₁ MLIP.
  6. "high-throughput first-principles doping Li6PS5Cl dopants site preference electrochemical stability window interface 2024" (extended) → none.
  7. "doped sulfide electrolyte in situ cathode electrolyte interphase electronically insulating oxidation products DFT designed dopant LiTaO3 LiNbO3 Li3PO4" (extended) → none.
  8. "oxygen-substituted argyrodite Li6PS5-xOxCl first-principles interface Li metal Li2O Li3PO4 decomposition products" → no product-resolved study.
  9. "first-principles anion doping sulfide electrolyte form passivating interphase Li metal fluorine nitrogen grand potential decomposition products design Li3PS4" → none.

---

## Q3. Characterization of the key computational references: what exactly was computed, and were product properties used as a design objective?

### Takeaway
Of the canonical references in the brief, **none uses product properties as a design objective for an SE dopant**.
- Zhu 2015/2016, Richards 2016 and Ong 2013 argue *qualitatively* that passivation requires electronically insulating, Li-conducting products.
- Xiao 2019 and Nolan 2019 screen coatings on the coating's **own** gap and reaction energy, and the product sets appear only in SI tables.
- Schwietert 2020/2021 redefine the window through kinetic intermediates.
- Banik 2022 shows that substitution does not move the window.
- Only post-2024 papers move to product properties: Sundar 2025 (coatings), Qian 2025 (coating), and Qi 2025 (SE class plus coating, with product gaps).

### Cited Findings

| Work (type) | What was computed | Systems / dopants / electrodes | Products (examples) | Product properties as design objective? | Source |
|---|---|---|---|---|---|
| Ong 2013 [comp] | Two-point μLi grand potential, HSE DOS, AIMD σ | LGPS family, M = Ge/Si/Sn/Al/P, X = O/S/Se; 0 V and 5 V | 0 V: Li₂X + Li₃P + LiₓM_y; 5 V: GeS₂/P₂S₅/S, or oxides + O₂ | **No** — qualitative only ("conductive SEI possible", "metallic products a concern", "glassy P₂S₅ may passivate") | [DOI](https://doi.org/10.1039/c2ee23355j) |
| Zhu, He & Mo 2015 [comp] | Grand-potential windows and lithium evolution for 14 SEs and Li-binaries | Undoped SEs; Li metal and high voltage | LPSCl family products; Li-binary windows | **No** — passivation criterion stated (insulating products); used to explain, not to rank | [DOI](https://doi.org/10.1021/acsami.5b07517) |
| Zhu, He & Mo 2016 [comp] | SE–electrode interface chemical and electrochemical stability | Undoped SEs vs electrodes (abstract) | Interphase layers "thermodynamically favorable" | Abstract: interphase properties "strongly influence" performance; ranking use unknown | [RSC](https://pubs.rsc.org/af/content/articlelanding/2016/ta/c5ta08574h); [OSTI](https://www.osti.gov/pages/biblio/1433677) |
| Richards 2016 [comp] | Closed and Li-open pseudo-binary reaction energies | About 30 SEs × 7 cathodes, plus Li | PO₄ + TM sulfides vs oxide cathodes; Li₂S/Li₂O + Li₃P vs Li | **No** — self-passivation discussed qualitatively | [DOI](https://doi.org/10.1021/acs.chemmater.5b04082) |
| Xiao 2019 [comp] | HT gates on the coating's own Eg > 0.5 eV, E_hull < 5 meV/atom, ESW, \|ΔE_rxt\| < 100 meV/atom vs Li₃PS₄ and charged NCM | 104,082 Li compounds → 62,437 → 1,600 → 302 → 184 | SI Table S5, e.g. LPSCl/LiNbO₃ → Li₂S, LiCl, Li₅(NbS₂)₇, S, Li₃PO₄; LPSCl/LiTaO₃ → TaS₃, Li₂(TaS₂)₃, Li₃TaS₄, Li₃PO₄, LiCl | **No** — products listed, not scored | [DOI](https://doi.org/10.1016/j.joule.2019.02.006); products per [litdb comparison](litdb/comparison_vs_ours.md) |
| Schwietert 2020 [both] | Intrinsic redox of the SE before decomposition (DFT, AIMD) plus experiment | Li₆PS₅Cl, LLZO, NASICON | Li₄PS₅Cl (2.24 V), Li₁₁PS₅Cl (1.08 V) → Li₃PS₄ + S + LiCl or P + Li₂S + LiCl | **No** — the window is redefined through intermediates | [DOI](https://doi.org/10.1038/s41563-019-0576-0) |
| Schwietert 2021 [comp] | Intrinsic vs decomposition windows, 12 SEs | 12 SEs | Intrinsic window wider in 10/12 (narrower for LLTO and LATP); V-shaped hull = phase separation | **No** | [DOI](https://doi.org/10.1021/jacsau.1c00228) |
| Nolan 2019 [comp] | Boolean E_d = 0 against 8 cathode states | 236 materials × 8 = 1,888 pairs | Li phosphates and ternary fluorides survive; only Li₂SO₄ and BeO stable in all 8 (litdb Sup2 analysis) | **No** (coating chemistry) | [DOI](https://doi.org/10.1021/acsenergylett.9b01703) |
| Banik 2022 [both] | Grand potential, lithium evolution, pDOS/COHP, HAXPES, CV | Si/Ge/I-substituted argyrodites; oxidative side | S/polysulfides/(P–S)ₓ + LiX | **No** — conclusion: substitution cannot improve oxidative stability | [DOI](https://doi.org/10.1021/acsaem.1c03599) |
| Tian 2019 [both] | Reactivity-guided layer design (Na) | Na₃SbS₄ hydrate surface vs Na | Ionically conductive passivating interphase | **Yes (concept)**, for a surface layer, Na, anode side | [eScholarship](https://escholarship.org/uc/item/6b24r92b) |
| Wang/Canepa 2022 [comp] | DFT adhesion; MTP MD Li transport through Li\|product | Argyrodite and Li₃PS₄ products at Li/Na | Li₃P conducts; Li₂S and LiCl block → resistive | Product properties **evaluated** for undoped SEs; not used to design | [DOI](https://doi.org/10.1039/d2ta02202h) |
| Lomeli 2024 [comp] | AIMD labels plus logistic regression → MP | 67 → 3,535 materials vs Li | Stable / passivating / reactive classes | Passivation is the **target**, but judged from MSD; no dopants or products | [DOI](https://doi.org/10.1021/acsami.4c06095) |
| Sundar 2025 [both] | Interface ΔE + gaps → products' Li barriers + gaps | Binary-oxide coatings on LPSCl; electrolyte, Li and cathode interfaces | e.g. MgO-derived products best | **Yes** — product σ_ion and σ_e are the most predictive metric (coatings) | [DOI](https://doi.org/10.1002/advs.202513191) |
| Qian 2025 [both] | Convex hull for coating + LPSCl at the cathode | LiPO₂F₂ on NCM85 | LiF + LiPₓOᵧF_z + LiPO₃ | **Yes** (single coating, cathode) | [DOI](https://doi.org/10.1002/anie.202413591) |
| Qi 2025 [both] | Pseudo-binary ΔE + PBE DOS of products | LPSC vs Li₂ZrCl₆ at 4.5 V; LZPO coating | "Partially favorable" vs "unfavorable" products | **Partly** — product gaps used to explain and select a coating | [DOI](https://doi.org/10.1016/j.jechem.2024.11.034) |
| Jiang 2022 [comp] | AIMD σ, bulk gap, ΔE_D vs electrodes | Se on S(16e) | — | **No** | [DOI](https://doi.org/10.1039/d2tc03696g) |
| Wu 2026 [both] | Bulk-gap dopant screen (15 elements), NEB, AIMD | Ta/Nb/… on the P site | LiTaO₃ CEI, Ta⁰ SEI (XPS) | **No** — ranked by bulk gap; products found afterwards | [DOI](https://doi.org/10.1002/anie.202523225) |
| Jung 2026 [comp] | ML + DFT ECW funnel | LGPS dual dopants (2,550) | — | **No** (window) | [DOI](https://doi.org/10.1016/j.etran.2026.100570) |

- Review-level synthesis of the same lineage: **Nolan, A. M.; Zhu, Y.; He, X.; Bai, Q.; Mo, Y.** "Computation-Accelerated Design of Materials and Interfaces for All-Solid-State Lithium-Ion Batteries." *Joule* **2**, 2016 (2018), DOI 10.1016/j.joule.2018.08.017. **[comp review]** It defines the cathodic and anodic limits as the potentials at which reduction or oxidation becomes thermodynamically favorable, and states that the window differs from the band or HOMO–LUMO gap, which is only an upper bound. It quotes sulfide windows of 1.7–2.4 V (Li₃PS₄, Li₇P₃S₁₁, Li₆PS₅Cl; secondary). — [Source](https://doi.org/10.1016/j.joule.2018.08.017) (litdb `litdb/papers/nolan2018_computation_accelerated_design_review.md`)
- **Xiao, Y.; Wang, Y.; Bo, S.-H.; Kim, J. C.; Miara, L. J.; Ceder, G.** "Understanding interface stability in solid-state batteries." *Nat. Rev. Mater.* (2020), DOI 10.1038/s41578-019-0157-5. **[comp review]** For Li₃PO₄ against Li, the products are Li₃P + Li₂O, and the review states: *"These reaction products are passivating and can enable the stable cycling…"*. The review treats product passivation qualitatively. — [Source](https://doi.org/10.1038/s41578-019-0157-5) (litdb `litdb/papers/xiao2020_interface_stability_ssb_review.md`)
- **Honrao, S. J.; Yang, X.; Radhakrishnan, B.; Kuwata, S.; Komatsu, H.; Ohma, A.; Sierhuis, M.; Lawson, J. W.** "Discovery of novel Li SSE and anode coatings using interpretable machine learning and high-throughput multi-property screening." *Sci. Rep.* **11**, 16484 (2021), DOI 10.1038/s41598-021-94275-5. **[comp]**
  - Data: 15,446 MP Li compounds with softBV barriers, grand-potential windows, E_hull and E_g.
  - Output: 250+ SE candidates and 26 Li-anode coatings. GB regressions reach R² 0.86 (barrier), 0.95 (reduction potential) and 0.92 (oxidation potential).
  - There is no cathode, no interface reaction energy and no product property. — [Source](https://doi.org/10.1038/s41598-021-94275-5) (litdb `litdb/papers/honrao2021_interpretable_ml_sse_anode_coatings.md`)

### Inferences
- The field's computational toolchain (grand potential, Li-open pseudo-binary, MP hull) has always **returned** the product sets. The step nobody took for SE dopants is to *score* those sets: by electronic gap, Li transport, the product's own stability window and phase fraction. Methodologically, the planned study is therefore an additional scoring layer on a standard pipeline, which Sundar 2025 has already demonstrated for coatings.
- Xiao 2019's SI products for niobate and tantalate coatings on LPSCl (Nb/Ta sulfides plus Li₃PO₄ and LiCl) are directly relevant **reference product sets** for Nb- or Ta-doped argyrodites at the cathode. They show that Ta-bearing reaction products against a sulfide are sulfides (TaS₃, Li₂(TaS₂)₃, Li₃TaS₄), not only LiTaO₃. This is a point to test against Wu 2026's LiTaO₃ claim (inference from the tabulated products; no paper makes this comparison).

### Gaps
- Zhu, He & Mo 2016 (*J. Mater. Chem. A*) was read at abstract level only, so whether it scored product properties (beyond the 2015 qualitative argument) is unverified. The full text is on [OSTI](https://www.osti.gov/pages/biblio/1433677) and the [author site](https://terpconnect.umd.edu/~yfmo/Mo-Interface%20stability%20solid-state%20battery_JMCA16.pdf); it was not fetched, to respect the session's fetch restrictions after two hosts failed.
- No 2023–2026 high-throughput **argyrodite** dopant screen with an interface or interphase axis was found. The HT dopant screens found are for LGPS (Jung 2026), Li₇PS₆ (Muy 2025, σ), a 15-element bulk-gap screen (Wu 2026) and a σ-ML screen (Kong 2026).

---

## Q4. Has anyone computed whether decomposition products are electronically insulating (band gaps of the product set) as a function of dopant, i.e. a "passivation quality" descriptor?

### Takeaway
Only piecemeal. Product gaps or Li transport have been computed for coating-derived products (Sundar 2025; Qian 2025), for SE-class comparisons (Qi 2025), for single doped systems (Li 2025 CuBr₂: LiCl/LiBr/Li₂S PDOS gaps), and for generic SEI components (Chen 2026; Wang/Canepa 2022). Zhu 2015 supplies stability windows for Li-binary products and reduction products of coating oxides (Nb, Ta, Si → metal or alloy). **No paper was found that defines a passivation-quality descriptor for the whole product set (gap plus phase fraction plus transport) and evaluates it across dopants and potentials.**

### Cited Findings

#### Cathode side (oxidative)
- Qian 2025, SI Table S1: product gaps for the LiPO₂F₂-derived CEI as listed (eV): LiF 8.7, LiCl 6.3, Li₃PO₄ 5.8, Li₄P₂O₇ 5.6, Li₂NiF₄ 4.7, P₂O₃F₄ 5.8, SOCl₂ 3.6, Ni₃(PO₄)₂ 3.4, P₂S₅ 2.6, LiPO₃ 2.5, P₂S₇ 2.1, … (the gap method is as the paper states it; litdb notes that the paper's own table only half supports the claim that the products are electronically insulating). — [Source](https://doi.org/10.1002/anie.202413591); values transcribed in [litdb comparison](litdb/comparison_vs_ours.md)
- Qi 2025: PBE DOS of the cathode-side products used to classify reaction products as "partially favorable" (LPSC) or "unfavorable" (Li₂ZrCl₆, a narrow-gap ZrO₂ product). litdb flags this as a leap from thermodynamics to a growth law. — [Source](https://doi.org/10.1016/j.jechem.2024.11.034)
- Zhu 2015, Fig. 2a: anodic limits of Li-binaries (figure-read by litdb, ±0.02 V; all are stable down to 0 V): LiF 6.38 > LiCl 4.21 > Li₂O 2.90 > LiI 2.46 > Li₂S 2.00 > Li₃P 0.85 > Li₃N 0.45 V vs Li. These define which dopant-derived Li-binaries can survive as **cathode-side** passivants (LiF, LiCl) and which oxidize at low potential (Li₃N, Li₃P, Li₂S). — [Source](https://doi.org/10.1021/acsami.5b07517); readings in [litdb comparison](litdb/comparison_vs_ours.md)
- Wu 2026 reports the LiTaO₃ CEI as insulating (qualitative; no computed gap of the product set). — [Source](https://doi.org/10.1002/anie.202523225)

#### Anode side (reductive)
- Sundar 2025: the **products'** band gaps and Li migration barriers were computed and used in screening; litdb records the product-gap ordering Li₂S < LiCl, with LiAlS₂ and MgS large. The LPSCl HSE06 gap was 3.92 eV (mixing 0.32). — [Source](https://doi.org/10.1002/advs.202513191)
- Li 2025 (CuBr₂-doped): DFT PDOS gaps of the SEI products LiCl 6.13, LiBr 5.07 and Li₂S 3.04 eV. This is the one dopant-specific product (LiBr) whose gap was computed alongside the native products. — [Source](https://doi.org/10.1016/j.ensm.2025.104221); [litdb comparison](litdb/comparison_vs_ours.md)
- **Chen, S. et al.** "Interfacial Stability and Li⁺ Transport Trade-Off in Halide-Based SEI Components for LPSC: A First-Principles Study." *Carbon Neutralization* **5**, e70141 (2026), DOI 10.1002/cnl2.70141. **[comp]** (abstract level)
  - Systems: LiF, LiCl, LiBr, LiI, Li₂S and Li₃P against Li metal.
  - Result: LiBr and LiI give the fastest Li⁺ surface migration and better adhesion but weaker mechanical resistance and electronic insulation. LiF gives the highest interfacial energy and the strongest electronic blocking, a trade-off governed by halogen identity.
  - This is a *component-level* passivation-quality comparison relevant to halide or F doping, but not a dopant → product-set calculation. — [Source](https://journal.hep.com.cn/cnl/EN/10.1002/cnl2.70141)
- Wang/Canepa 2022: Li transport through Li|product interfaces (Li₃P passes, Li₂S and LiCl block), weighted by the decomposition stoichiometry (Li₂S about 5× Li₃P), giving an overall resistive verdict for argyrodite|Li. This is the only work found that **weights products by phase fraction** when judging the interphase. — [Source](https://doi.org/10.1039/d2ta02202h)
- Zhu 2015, SI Table S3 (litdb reading): reduction steps of coating oxides — Li₃PO₄ at 0.69 V, a single step to Li₃P + Li₂O (both electronically insulating Li-binaries); LiNbO₃ at 0.55 V to **Nb metal**; LiTaO₃ at 0.35 V to **Ta metal**; Li₂SiO₃ at 0.10 V to **Li₂₁Si₅ alloy**. These are reference outcomes for what Nb-, Ta- or Si-bearing products become at Li potential. — [Source](https://doi.org/10.1021/acsami.5b07517); [litdb comparison](litdb/comparison_vs_ours.md)
- Wu 2026: metallic Ta⁰ found in the SEI by XPS (Ta 4f 24.4/22.4 eV) together with Li₂S, Li₃P, LiCl and LiBr. CCD 0.8 → 2.4 mA cm⁻²; the symmetric cell shorted at 278 h without Ta but ran > 1600 h (< 60 mV) with it. A metallic minority product coexists with improved performance. — [Source](https://doi.org/10.1002/anie.202523225)
- Li, X. et al. (2026), "functionally differentiated interphase" on Li metal (LPSCl). **[exp + thin DFT: VASP/PBE interface supercells, DOS, CI-NEB]** The design assigns roles to products: LiF for electron blocking, LiCl/LiBr for homogeneous coverage, Li₃N for fast Li⁺. CCD 0.398 → 3.581 mA cm⁻². This is an *artificial* multi-component SEI, not dopant-derived. *J. Energy Storage* (2026), DOI 10.1016/j.est.2026.124529. — [Source](https://doi.org/10.1016/j.est.2026.124529) (litdb `litdb/papers/li2026_functionally_differentiated_interphase.md`)

### Inferences
- A defensible "passivation quality" descriptor would need, at minimum, four things the literature treats separately:
  1. the electronic gap of each product (Qian, Sundar, Li 2025, Qi);
  2. the **phase fraction** and connectivity of any narrow-gap or metallic minority phase (Wang/Canepa's stoichiometric weighting; the Li₃P leak problem; Ta⁰/Nb/La⁰/Li–M alloys predicted at 0 V by Zhu 2015 SI and Ong 2013, and observed by Wu 2026 and others);
  3. Li transport through the product layer (Sundar barriers; Wang/Canepa MD; Chen 2026);
  4. the product's own stability window on the side where it forms (Zhu 2015 Li-binary windows: Li₃N and Li₃P cannot passivate a cathode).

  No paper combines these four, and none does so across dopants.
- Anion dopants (F, Cl/Br/I, O) map onto wide-gap Li-binaries (LiF, LiX, Li₂O) that are stable from 0 V up to their anodic limits. **Cation** dopants generally map onto metals or alloys at Li potential and onto oxides, sulfides or thiometallates at the cathode. Under a product-quality ranking, the expected first-order picture is therefore that anion dopants help the anode side, while cation dopants are ambiguous at the anode (MCI risk vs "Li-alloy is good") and dopant-specific at the cathode. This is an inference to be tested, not a published result.
- The magnitudes reported in these papers vary with method (PBE vs HSE06 vs measured; for example litdb lists Li₃PO₄ at 5.8 eV in Qian Table S1 and 7.4 eV as cited by Kang 2026). Product gaps should be used as **orderings with one method**, not as absolute values mixed across sources.

### Gaps
- No product-set descriptor evaluated across dopants was found, under any name: "passivation index", "interphase electronic leakage" or "insulating fraction".
- No computational work was found that tests whether a minority metallic or narrow-gap product percolates in a dopant-derived interphase (the dopant at a few at% means its products are a small volume fraction). The relevant phase fractions follow from the grand-potential stoichiometry, but nobody has reported them per dopant.
- Chen 2026 and the MDPI Zr/F paper were read at abstract level only.

---

## Q5. What computational support exists for the "Li⁺ release / chemical re-lithiation of the cathode" benefit of SE oxidation (Kang et al., *Chem. Commun.* 61, 16850 (2025))?

### Takeaway
None that targets the benefit directly. No computational paper was found that models Li released by sulfide-SE oxidation re-entering delithiated NCM, or that uses this re-entry as a design metric. The ingredients exist:
- grand-potential "lithium evolution" profiles count the Li released per formula unit as the potential rises (Zhu 2015; Banik 2022 Fig. S5);
- Schwietert 2020 computes the first oxidation step Li₆PS₅Cl → Li₄PS₅Cl at 2.24 V, which releases 2 Li;
- Haruyama 2014 (DFT+U) shows Li moving from β-Li₃PS₄ onto LiCoO₂(110) at contact;
- the Li-open pseudo-binary formalism (Richards 2016) treats Li exchange with an electrode reservoir.

The experimental support is Kang 2025, supplemented by Kaeli 2025 on NMC relithiation kinetics.

### Cited Findings

#### Cathode side (this question is entirely oxidative)
- **Kang, J.; Lee, Y.; Bae, Y.; Lee, J.-W.** "High-voltage stability of sulfide-based all-solid-state batteries: benefit of the parasitic reaction." *Chem. Commun.* **61**, 16850 (2025), DOI 10.1039/d5cc04349b. **[exp; no calculations]**
  - Setup: LPSCl dry-coated onto NCM811, stored at 100% SOC after a 4.25 V charge.
  - Observation: XRD peaks shift to lower angle, read as higher Li content (lower SOC), and the shift is larger for SE-coated NCM.
  - Interpretation: LPSCl oxidation releases Li⁺, which chemically re-lithiates the delithiated NCM. A conformal coating makes this uniform, confines the layered → rock-salt transition to the surface, and gives a 15.0% capacity-retention advantage at 200 cycles. The digest lists its theory/DFT content as "none". — [Source](https://doi.org/10.1039/d5cc04349b) (litdb `litdb/papers/kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb.md`)
- Schwietert 2020: the computed intrinsic oxidation of Li₆PS₅Cl at 2.24 V to Li₄PS₅Cl releases Li while keeping the framework; the intermediate then decomposes to Li₃PS₄ + S + LiCl. — [Source](https://doi.org/10.1038/s41563-019-0576-0)
- Banik 2022: "lithium-evolution number vs potential" (Fig. S5) for LPSCl and the substituted argyrodites, i.e. the computed Li released per formula unit as the potential rises. — [Source](https://doi.org/10.1021/acsaem.1c03599) (litdb digest §9)
- Zhu 2015 introduced the same grand-potential lithium-evolution analysis for 14 SEs. — [Source](https://doi.org/10.1021/acsami.5b07517)
- **Haruyama, J.; Sodeyama, K.; Han, L.; Takada, K.; Tateyama, Y.** "Space–Charge Layer Effect at Interface between Oxide Cathode and Sulfide Electrolyte in All-Solid-State Lithium-Ion Battery." *Chem. Mater.* **26**, 4248 (2014), DOI 10.1021/cm5016959. **[comp, static DFT+U slabs]**
  - Model: the LiCoO₂(110)|β-Li₃PS₄(010) interface.
  - Li from the LPS surface and subsurface adsorbs onto exposed O ridges of LCO. The LPS slab disorders, and the Li-vacancy formation energy at LP2 drops to 1.44 eV, against 3.2 eV in bulk LPS (a difference of −1.76 eV by litdb arithmetic).
  - The authors relate 1.44 eV to the voltage at which charging begins, and read the slope of the early voltage profile as space-charge-layer growth.
  - This is computational evidence that **Li transfers from sulfide SE to the oxide cathode at contact**, but it concerns a pristine interface and space charge, not oxidative decomposition or bulk re-lithiation. — [Source](https://doi.org/10.1021/cm5016959) (litdb `litdb/papers/haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md`)
- Richards 2016: the Li-open pseudo-binary reaction energy (eq. 4) lets the interfacial reaction exchange Li with a reservoir at fixed μ_Li, so Li released by the SE is formally accounted for. It is not translated into a cathode SOC change. — [Source](https://doi.org/10.1021/acs.chemmater.5b04082)
- **Kaeli, E.; Jiang, Z.; Yang, X.; Choy, E. P. K. L.; Liang, N. B.; Barks, E.; Wang, S.; Kang, S. D.; Chueh, W. C.** "Decoupling First-Cycle Capacity Loss Mechanisms in Sulfide Solid-State Batteries." *Energy Environ. Sci.* **18**, 1452 (2025), DOI 10.1039/D4EE04908J. **[exp, operando XRD]**
  - Much of the apparent first-cycle loss in Li₆PS₅Cl|NMC cells is **sluggish NMC relithiation** rather than irreversible SE oxidation; the first-cycle CE is 96.2%.
  - Reduction of the sulfide oxidation products is kinetically limited, and sulfide oxidation persists beyond the first cycle.
  - This gives adjacent experimental context on Li inventory and relithiation, not on SE-derived Li. — [Source](https://pubs.rsc.org/en/Content/ArticleLanding/2025/EE/D4EE04908J); [ChemRxiv](https://chemrxiv.org/engage/chemrxiv/article-details/6718440912ff75c3a13d759e)
- A web search for computational support found none. The engine summary of the closest hits: "no single paper that combines first-principles calculations of sulfide oxidation with NCM relithiation". — [Search context: review](https://www.oaepublish.com/articles/energymater.2022.01); [NCM811–sulfide review](https://pmc.ncbi.nlm.nih.gov/articles/PMC12665888/)

### Inferences
- The computational quantity that matches the Kang 2025 benefit already exists in every grand-potential calculation: the **Li evolved per formula unit** between OCV and the cathode potential (lithium-evolution profile), multiplied by the amount of SE that reacts. For undoped LPSCl, the final products reported by Schwietert 2020 (Li₃PS₄ + S + LiCl) imply, by stoichiometry, Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2 Li⁺ + 2 e⁻. This is my balancing of the reported products, not a quoted equation.
- Dopants could change the **Li-release capacity** only by changing the oxidation product set. Products that **retain Li** (Li₃PO₄, LiCl, LiF, Li₂SO₄) release less Li than fully delithiated products (S, P₂S₅/P₂S₇). That suggests a possible trade-off for the planned ranking: a dopant that forms a Li-rich, insulating, passivating CEI would *reduce* the re-lithiation benefit per unit SE oxidized, while also reducing how much SE oxidizes. No paper discusses this trade-off; it is an inference to be pre-registered, not a literature finding.
- Kaeli 2025 shows that NMC relithiation is kinetically limited even electrochemically. A purely thermodynamic "Li supplied" metric would therefore overstate the benefit unless paired with a kinetic caveat. The uniformity argument of Kang 2025 is also not captured by any bulk thermodynamic number.

### Gaps
- No computational paper was found on the following, so the Kang 2025 mechanism has no first-principles counterpart:
  - the thermodynamics or kinetics of Li transfer from SE oxidation products into Li₁₋ₓNiₓ…O₂;
  - SOC homogenization by SE oxidation;
  - the dopant dependence of Li release.
- The Kang 2025 digest records no calculations, and the litdb comparison notes that its mechanism (SOC lowering) is different physics from the insulating-CEI passivation story. The two should not be cited as evidence for each other ([litdb comparison](litdb/comparison_vs_ours.md), Kang25 row).

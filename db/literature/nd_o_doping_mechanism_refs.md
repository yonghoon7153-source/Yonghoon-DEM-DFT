# Reference map — Nd₂O₃-doped LPSCl band-gap / electronic-structure mechanism

Built 2026-06-17. Maps each mechanistic CLAIM in our Nd₂O₃-doped LPSCl band-gap
analysis to supporting literature. "DB#" = row in `argyrodite_computational_littable.csv`.
WebFetch blocked (403) → entries from WebSearch snippets; verify DOIs before citing.

---

## CLAIM 1 — Argyrodite host gap: VBM = S 3p, CBM = PS₄ antibonding (+ Li); orbital hybridization governs redox
- **Ke et al. 2025**, *Energy Storage Mater.* 104125 — `10.1016/j.ensm.2025.104125` (DB#17). S-p / p-p
  hybridization reconfigures PS₄ electron-acceptance; ELF+PDOS template. ★ (our Mg+O analog)
- **Braga group 2026**, *Batteries* 12(2) 060 — `10.3390/batteries12020060` (DB#11). LPSCl gap PBE 2.45 / HSE06 3.30 eV.
- **Physica B 2023** — `10.1016/j.physb.2023.414932` (DB#14, mBJ gap 3.11). **RSC Adv. 2022** — `10.1039/D2RA05900B` (DB#15, direct gap @Γ).
- **"Devil in the details" 2025** — `10.1039/D4TA06603K` (DB#16). PBE gap 2.15 eV (closest to our eigenvalue 2.07/2.10).

## CLAIM 2 — O-for-S (PS₃O / oxysulfide) widens the gap / extends the oxidative-stability window in thiophosphates
- **O-doped argyrodite Li₆PS₅₋ₓClOₓ (x=0–1), ACS AMI 2022** — `10.1021/acsami.1c14573` (DB#18). ★★ direct O-doping precedent.
- **"Can substitutions affect the oxidative stability of Li argyrodite?" (ChemRxiv 2021)** — `10.26434/chemrxiv-2021-3j2sz`.
  Theory: replacing S with O **extends the electrochemical window** of Li₆PS₅Cl. ★ (direct "O widens stability" support)
- **Oxysulfide Li₆.₂₅PS₄O₁.₂₅Cl₀.₇₅** — arXiv:2010.08805. O substitution extends ESW, keeps σ.
- **"Enhanced electrochemistry stability of O-doped Li₆PS₅Cl (liquid-phase)", Solid State Ionics 2023** — PII S0167273823002023 (exp).
- **Li₃PO₄–Li₃PS₄ oxysulfide, Solid State Ionics 2005** — PII S0167273805002894 (oxysulfide precedent).
- **"Effect of selected dopants on conductivity & moisture stability of Li₃PS₄" 2022** — PII S2468519422000660 (anion/cation doping DFT).
- **Oxidative degradation PS₄→S–S→PS₃, Cell Rep. Phys. Sci. 2024** — `10.1016/j.xcrp.2024.101909` (DB#19). P–S(O) distortion / oxidation.
- NOTE: "ESW/oxidative-stability widening" is robust & O-driven; the **fundamental band gap** widening from dilute PS₃O in
  *crystalline argyrodite* is weaker (VBM = free/non-bonding S, not the PS₄ bonding S that O replaces) — see CLAIM 5.

## CLAIM 3 — PBE/PBE+U mis-place rare-earth 4f → gap fails; 4f UHB; HSE/GW/DMFT needed (our U=8 keeps it insulating)
- **"The nature of the electronic band gap in lanthanide oxides"** — arXiv:1208.0503. ★ Minimum gap varies as filled/empty
  **Ln 4f states move into the O 2p → 5d gap**; HSE06 needed; sX-LDA puts empty 4f higher (better vs exp).
- **"Semi-local exchange + DMFT: rare-earth sesquioxides"** — arXiv:2110.00400. ★★ Nd₂O₃/La₂O₃ **directly**:
  "In Nd₂O₃ the optical transition is **O 2p → 4f upper Hubbard band**, gap ≈ La₂O₃." (= our dopant source)
- **Dudarev et al. 1998**, *Phys. Rev. B* 57, 1505 — `10.1103/PhysRevB.57.1505`. The +U (Dudarev) formulation used by QE/VASP. (methods)

## CLAIM 4 — Lanthanide 4f is contracted/shielded by 5s5p (spectator); 5d/6s do the bonding (→ and the band-edge hybridization)
- **Lanthanide contraction / 4f shielding** — textbook (e.g. Cotton & Wilkinson; LibreTexts "Lanthanide Contraction"). 4f
  shielded by 5s²5p⁶ → transitions insensitive to environment; bonding via 5d/6s.
- **"Localized 4f orbital electrons of lanthanide dopants in MoP for HER" (2024)** — PMC12199375. 4f localized; weak 5d/6s
  shielding allows 4f–d hybridization (supports "5d/6s extended → hybridize" vs "4f localized → spectator").
- **"Cerium dimer anion & 4f contribution to Ln–Ln bonds", JACS 2025** — `10.1021/jacs.5c07348`. 4f covalency only in extreme
  cases (light Ln) — i.e., normally spectator.

## CLAIM 5 — Aliovalent M³⁺ on Li site → Li vacancies (σ) + band-edge shift (our narrowing driver)
- **"Influence of Aliovalent Cation Substitution … Argyrodite", Chem. Mater. 2021** — `10.1021/acs.chemmater.0c03090`. ★ aliovalent in argyrodite.
- **"AC conductivity of Li₆₋ₐMₐ/ₙPS₅Cl (M=Ca,Mg,Ba,Zn,Al,Y)" 2024** — PMC11106650. **Y³⁺** = closest RE³⁺-like sulfide analog.
- **"Cl- and Al-Doped Li₆PS₅Cl", Nanomaterials 2022** — `10.3390/nano12244355`. Al³⁺ aliovalent.
- **Zr & F co-doped LPSCl, Batteries 2025** (DB#20). Co-doping interface DFT.
- **LLZO rare-earth/aliovalent doping review, Rare Metals 2024** — `10.1007/s12598-024-03146-1`. RE in OXIDE SE context (La structural; Al/Ga/Ta dope).
- **"Bandgap engineering via anion-lattice doping in high-entropy oxides" 2025** — PMC12442597 (dopant-induced gap narrowing precedent).

---

## HONEST GAP
**Direct La/Nd doping of a SULFIDE argyrodite was NOT found in the literature** — closest = Y³⁺-in-LPSCl (PMC11106650) and
rare-earths in OXIDE SEs (LLZO). → our **Nd₂O₃-doped LPSCl is largely novel** (a selling point); mechanisms are supported by
the trivalent-aliovalent + RE-oxide-4f analogs above. User also holds experimental **La₂O₃+O ("La+O")** data (σ ↓) as the
closest experimental precedent.

## CLAIM 6 — Nd / O dopant ROLE (why Nd2O3?) : O = stability at sigma cost; Nd = oxophilic carrier/getter (2026-06-17 search)
- **"Site-selective oxygen introduction in sulfide argyrodite" 2025** — PII S2405829725000790. O -> structural stabilization + moisture stability.
- **"Oxysulfide SE: impact of oxygen in sulfides" 2025** — PII S2405829725006671. + **air-stability review** PII S1385894725086310.
  KEY quote (review): "O improves moisture stability but **significantly degrades ionic conductivity & cell performance**" == our sigma 0.52x.
- **Metal-oxide H2S getters** (ZnO/Fe2O3/Bi2O3) suppress H2S in sulfides "**at the expense of ionic conductivity**" -> Nd2O3 (basic oxide) fits this archetype.
- **HSAB**: O2- hard base binds Nd3+ hard acid -> Nd oxophilically ANCHORS O (our P-O-Nd bridges). (soft acids As/Sb/Sn instead protect S.)
- **Nd3+-LiNiPO4 cathode** — PII S0167577X18318676. Nd in phosphate -> high-voltage structural stability (resonates with NdPO4 motif).
- **Nd3+ in ceramics** (CeO2:Nd S1567173912003021 etc.): lattice distortion + grain-boundary/sintering/densification = microstructural lever (may touch GB/total conductivity).
- READING (lit <-> our DFT AGREE): O does the function (oxidation/moisture stability) with a documented sigma penalty; Nd is the
  oxophilic hard-acid carrier/anchor for O + basic-oxide air-stability getter + microstructure modifier. Nd's standalone gap/sigma
  effects are neutral-to-negative (our DFT) -> consistent with "RE/oxide doping = stability-for-conductivity trade".

## DECISIVE FOLLOW-UP CALC (to nail attribution)
O-only PS₃O+PS₂O₂ cell (remove Nd, Li charge-compensate) → predicted gap widen/unchanged ⇒ proves narrowing is 100% Nd.

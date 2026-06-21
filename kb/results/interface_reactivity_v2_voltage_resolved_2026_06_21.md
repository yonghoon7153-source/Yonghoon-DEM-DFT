# Voltage-resolved SE/cathode interface reactivity (v2) — 2026-06-21

**Method:** `GrandPotentialInterfacialReactivity` (Richards/Ong 2016), open to Li
reservoir, μ_Li = μ_Li(metal) − V, MP GGA_GGA+U hull (4886 entries, Cl-Co-Li-Mn-Ni-O-P-S).
Tool: `tools/oxidation/interface_reactivity_v2.py` (gabia, 2026-06-21).
More negative ΔE_rxn (eV/atom) = more reactive interface at that voltage.
**Upgrade vs v1:** v1 was OCV-only (modelc marginally more reactive, Δ0.008 = noise);
v2 evaluates the *charged-state* (operating-voltage) condition where degradation happens.

## Results (min ΔE_rxn, eV/atom)
| cathode | V | LPSCl | LPSCl1.6 | gap (LPSCl1.6−LPSCl) |
|---|---|---|---|---|
| LiCoO2 | 2.5 | −0.666 | −0.624 | +0.042 |
| LiCoO2 | 4.0 | −1.315 | −1.166 | +0.150 |
| LiCoO2 | 4.3 | −1.544 | −1.346 | **+0.198** |
| LiNiO2 | 4.3 | −1.607 | −1.449 | +0.158 |
| NMC811 | 2.5 | −0.751 | −0.710 | +0.041 |
| NMC811 | 4.3 | −1.579 | −1.415 | +0.164 |
(full grid in `interface_reactivity_v2.json`)

## Findings
1. **Both SEs react strongly with all cathodes** (−0.6 → −1.6 eV/atom) and reactivity
   **grows with voltage** (more oxidizing) → cathode coating essential, worse at high V.
2. **LPSCl is MORE reactive than LPSCl1.6 at every voltage & cathode**; the gap GROWS
   with V (+0.04 @2.5 V → +0.20 @4.3 V).
3. **Why:** Cl⁻ is electrochemically inert; LPSCl1.6 has more Cl (1.6 vs 1.0) and less
   reactive S/Li → Cl "dilutes" the reactive content → less reaction with cathode O per atom.
4. **Implication:** thermodynamic cathode reactivity *favors* Cl-rich (less reactive). So
   the experimental "Cl-rich worse at cathode" (↑decomposition current; AdvFM'22, Angew'22)
   is **NOT thermodynamic** — it is kinetic/interfacial/electronic (consistent with the
   electronic-conductivity / self-discharge mechanism, not cathode thermodynamics).
5. **Accuracy payoff:** the OCV point (v1) was misleading (noise, wrong sign); the
   operating-voltage analysis (v2) is the physically relevant condition and gives a clear,
   monotonic trend.

## Caveats
- `use_hull_energy=True` → both SEs placed at their MP hull energy (modelc has no own MP
  entry); consistent footing but doesn't capture modelc's metastability.
- Cathodes are ideal MP phases; real NMC is a disordered solid solution.
- Thermodynamic driving force only (no kinetic passivation / CEI).

## CHARGED (delithiated) cathodes — confirms & strengthens (2026-06-21)
Ran with delithiated cathodes (CoO2, Li0.5CoO2, NiO2, Li0.5-NMC811) at V=3.5–4.5
(`interface_reactivity_charged.json`):
- **Same trend, robust:** LPSCl MORE reactive than LPSCl1.6 at every charged cathode &
  voltage; gap grows to **+0.29 eV/atom @4.5 V (CoO2)**.
- **High-V cathode-independence:** at 4.3 & 4.5 V the LPSCl value is IDENTICAL across all
  cathodes (−1.5438, −1.7153) = the reaction is the SE's own oxidation (cathode = O sink).
- **CoO2@4.3 = LiCoO2(v2)@4.3 = −1.5438 exactly** → the grand-potential framework already
  delithiates the cathode at high V, so lithiated and charged contacts converge there
  (charged run mainly matters at intermediate V).
→ Conclusion is robust across cathode chemistry AND lithiation state: **Cl-rich is
thermodynamically LESS reactive at the cathode interface**; the experimental "Cl-rich worse"
is kinetic/electronic, not thermodynamic. (Closes the interface-accuracy question.)
Figure: `docs/figures/oxidation/interface_reactivity_charged.png`.

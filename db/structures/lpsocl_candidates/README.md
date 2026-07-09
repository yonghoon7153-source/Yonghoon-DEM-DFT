# LPSOCl candidates — O-substituted LPSCl1.6, minimum-representable stoichiometry (2026-07-09)

**Concept**: LPSCl1.6 synthesized with Li2O precursor -> O incorporates on S sites.
Minimal charge-neutral model = isovalent S -> O substitution in the 62-atom modelc cell.

**Stoichiometry convention** (mirrors the b2o3 champion bookkeeping, where nominal x~0.02
is represented by the cell-minimum substitution):
- 62-atom cell = Li27 P5 S22 Cl8 = 5 f.u. of Li5.4PS4.4Cl1.6
- 1 O on an S site -> **Li5.4 P S4.2 O0.2 Cl1.6  (x_O = 0.2)** = smallest representable unit

**Site classes found** (modelc_V0_k663.xyz): 22 S = 2 free-S (Li6 cage, no P within 4.2 A)
+ 20 PS4-corner (P 2.04-2.08 A; Li 2-3). Candidates cover both classes:

| file | site | class |
|---|---|---|
| lpsocl62_x02_OonS53_freeS_Li6.xyz | S53 | free-S (Li6 cage) |
| lpsocl62_x02_OonS33_corner_P2.04_Li2.xyz | S33 | PS4-corner |
| lpsocl62_x02_OonS49_corner_P2.05_Li2.xyz | S49 | PS4-corner |
| lpsocl62_x02_OonS38_corner_P2.06_Li3.xyz | S38 | PS4-corner |

**Prior**: in the b2o3 champion, O sat on phosphate corners (P-O bonds), not free-S
-> corner expected to win, but free-S must be tested (site-preference step of the pipeline).

**Next (KISTI)**: QE vc-relax the 4 candidates -> lowest E = site preference ->
Layer-1 property cascade (EOS / elastic / ESW / BVSE / MD 3-seed) same track as b2o3.
Alternative model (recorded, not default): Li2O interstitial addition (+2 Li + 1 O).

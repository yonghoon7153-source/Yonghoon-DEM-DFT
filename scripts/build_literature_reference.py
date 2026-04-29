"""Hard-coded literature reference table for NCM brittle fracture validation.

This table is the side-by-side companion to b2_b4_diagnostic.csv. It
lists experimental NCM cracking observations from the literature so the
master DB can carry a single 'fraction observed in real cathodes'
range next to our DEM-derived counts.

Sources (all open-access or institutional access):
  Lim 2018          Nano Lett. 18, 2087    — secondary particle pulverization
                                              under 200 MPa stack pressure
  Quinn 2020        Joule 4, 2466          — cycled NCM SEM, 2-5% pulv
  de Vasconcelos    Acta Mater. 178, 35    — fracture-toughness; 15-25% microcrack
   2019                                       observable post-compaction
  Liu 2020          Nat. Energy 5, 304     — single-crystal robustness ratio (~10×)
  Xu 2017           PRX 7, 041038          — NCM811 nanoindentation (E, H)
  Wang 2020         JPS 470, 228413        — NCM hardness measurement
  Bielefeld 2020    J. Electrochem. Soc.   — relaxation-included DEM, max overlap 5%
  Wang 2023         J. Power Sources 555   — DEM, max overlap 0.05-0.15
  Minnmann 2021     Adv. Energy Mater. 11  — DEM with relaxation, max overlap 0.08

Output:
  docs/figures/physics_regime/literature_brittle_reference.csv

This file is regenerated each time the script is run. It is plain
hard-coded data — no analysis needed — but lives in the supplementary
folder so build_metrics_db auto-merges it as a constant lookup table
keyed on a synthetic 'lit_reference' column (so it doesn't dilute the
per-case rows).
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parent.parent / 'docs' / 'figures' / 'physics_regime'
OUT.mkdir(parents=True, exist_ok=True)


REFERENCE = [
    # Damage stage occurrence ranges (post-compaction polycryst NCM)
    {'category': 'fracture_stage', 'metric': 'severe_pct',
     'lit_low': 1.0,  'lit_high': 5.0,
     'unit': '%', 'source': 'Lim 2018; Quinn 2020',
     'note': 'Severe = fragmentation + pulverization, post-200 MPa stack'},
    {'category': 'fracture_stage', 'metric': 'multicrack_pct',
     'lit_low': 5.0,  'lit_high': 10.0,
     'unit': '%', 'source': 'Quinn 2020',
     'note': 'SEM observation post-cycling'},
    {'category': 'fracture_stage', 'metric': 'microcrack_pct',
     'lit_low': 15.0, 'lit_high': 25.0,
     'unit': '%', 'source': 'de Vasconcelos 2019',
     'note': 'Post-compaction'},
    {'category': 'fracture_stage', 'metric': 'intact_pct',
     'lit_low': 60.0, 'lit_high': 75.0,
     'unit': '%', 'source': 'Lim 2018; ensemble inference',
     'note': 'Implied by severe + multi + micro = ~25-40%'},

    # Material constants
    {'category': 'material', 'metric': 'K_IC_AM_S_MPa_m05',
     'lit_low': 0.8, 'lit_high': 1.4,
     'unit': 'MPa·m^0.5', 'source': 'Liu 2020',
     'note': 'Single crystal NCM811'},
    {'category': 'material', 'metric': 'K_IC_AM_P_MPa_m05',
     'lit_low': 0.2, 'lit_high': 0.5,
     'unit': 'MPa·m^0.5', 'source': 'Quinn 2020; de Vasconcelos 2019',
     'note': 'Polycrystalline secondary'},
    {'category': 'material', 'metric': 'K_IC_ratio_S_over_P',
     'lit_low': 2.5, 'lit_high': 5.0,
     'unit': 'dimensionless', 'source': 'Liu 2020',
     'note': 'Single/poly fracture-toughness ratio (we used 1.0/0.3 = 3.3)'},
    {'category': 'material', 'metric': 'E_NCM811_GPa',
     'lit_low': 130.0, 'lit_high': 165.0,
     'unit': 'GPa', 'source': 'Xu 2017',
     'note': 'Nanoindentation; project-wide use 140 GPa'},
    {'category': 'material', 'metric': 'H_NCM_GPa',
     'lit_low': 5.0, 'lit_high': 8.0,
     'unit': 'GPa', 'source': 'Wang 2020',
     'note': 'Vickers hardness, NCM811'},

    # DEM literature comparison
    {'category': 'dem_overlap', 'metric': 'max_dr_R_typical',
     'lit_low': 0.05, 'lit_high': 0.15,
     'unit': 'dimensionless', 'source': 'Wang 2023',
     'note': 'Max δ/R in DEM, with relaxation steps'},
    {'category': 'dem_overlap', 'metric': 'max_dr_R_with_cap',
     'lit_low': 0.04, 'lit_high': 0.05,
     'unit': 'dimensionless', 'source': 'Bielefeld 2020',
     'note': 'Explicit overlap cap at 5%'},
    {'category': 'dem_overlap', 'metric': 'max_dr_R_with_relax',
     'lit_low': 0.06, 'lit_high': 0.10,
     'unit': 'dimensionless', 'source': 'Minnmann 2021',
     'note': 'Relaxation step included'},
    {'category': 'dem_overlap', 'metric': 'max_dr_R_our_DEM',
     'lit_low': 0.20, 'lit_high': 0.55,
     'unit': 'dimensionless', 'source': 'this work',
     'note': 'Our 156 cases — no relaxation, aggressive porosity target'},

    # SE Tabor reference (already used in our model)
    {'category': 'tabor_se', 'metric': 'sigma_grain_single_cryst',
     'lit_low': 2.5, 'lit_high': 3.5,
     'unit': 'mS/cm', 'source': 'Sakuda 2013',
     'note': 'Li6PS5Cl single-crystal ultrasonic, project default 3.0'},
    {'category': 'tabor_se', 'metric': 'sigma_grain_pellet',
     'lit_low': 0.25, 'lit_high': 0.40,
     'unit': 'mS/cm', 'source': 'Sakuda 2013',
     'note': 'Cold-pressed Li6PS5Cl pellet, GB-dominated'},
    {'category': 'tabor_se', 'metric': 'H_SE_GPa',
     'lit_low': 0.7, 'lit_high': 1.0,
     'unit': 'GPa', 'source': 'Sakuda 2013',
     'note': 'Li6PS5Cl hardness, project default 0.85'},
]


def main() -> None:
    df = pd.DataFrame(REFERENCE)
    out_path = OUT / 'literature_brittle_reference.csv'
    df.to_csv(out_path, index=False)
    print(f'→ {out_path}  ({len(df)} reference values)')
    # Quick console summary
    for cat, sub in df.groupby('category', sort=False):
        print(f'\n[{cat}]')
        for _, r in sub.iterrows():
            print(f'  {r["metric"]:30s}  {r["lit_low"]:>6.2f} - {r["lit_high"]:<6.2f}  '
                  f'{r["unit"]:<15s}  ({r["source"]})')


if __name__ == '__main__':
    main()

# Independent composition-basis audit

**The five stored ps45 beds reconstruct to approximately 65% AM by AM+SE solid volume, not 60%.** This is an arithmetic audit of the decks, archived records, and AM scaffolds. No new DEM or network run was performed.

Source pin: `46cd0bdb872e7d6c85ca50ec4172e98377253130`. Reproducer: `../probes/composition_basis.py`; complete values and source hashes: `../evidence/composition_basis.json`.

## Deck composition versus the proposed density conversion

All five decks (`source/dem_scripts/ps_sweep_6mah_20260914/in.ps_*_r45.liggghts`) declare the same radii and densities in executable lines:

- Radii at lines 39–41: AM_P 4.5 µm, AM_S 2.0 µm, SE 0.5 µm, using the declared simulation-to-physical scale of 1000.
- Particle-template densities at lines 107–109: AM_P=AM_S=4800 kg/m³ and SE=2000 kg/m³.
- Distribution at line 113: total AM mass weight 0.816 and SE mass weight 0.184; the AM share is split into P:S variants.

For the AM fraction among the two solid components,

`x_AM,solid = (w_AM/rho_AM) / [(w_AM/rho_AM) + (w_SE/rho_SE)]`.

| Mass basis | Density basis, AM / SE (kg/m³) | Nominal AM solid-volume fraction |
|---|---:|---:|
| Deck 0.816 : 0.184 | 4800 / 2000 | 64.885496% |
| Same rounded mass weights | 4850 / 1640 | 59.993544% |
| Exact 80 : 18 | 4800 / 2000 | 64.935065% |
| Exact 80 : 18 | 4850 / 1640 | 60.045767% |

Thus the user's approximately 60% conversion is consistent with the stated 4850/1640 density assumption, but that assumption does not describe the executable density basis that generated these decks. The small difference between exact 80:18 and rounded 81.6:18.4 is secondary to the density mismatch.

One deck comment still says AM_P r=6 µm at the template section; the executable radius variable and every stored AM scaffold radius are 4.5 µm. The operative quantities, not that stale comment, were used here.

## Reconstruction from stored counts and AM scaffold radii

For each case, AM volume was summed directly from the compressed `am_scaffold.csv.gz` rows as `sum(4*pi*r_i^3/3)`. SE volume was calculated from the archived SE count and the matched deck's fixed 0.5 µm radius. The shared `4*pi/3` cancels in the solid fraction:

`x_AM,solid = (N_P*4.5^3 + N_S*2^3) / (N_P*4.5^3 + N_S*2^3 + N_SE*0.5^3)`.

| P:S label | AM_P count | AM_S count | SE count | Actual PC share within AM volume | Reconstructed AM solid-volume fraction |
|---|---:|---:|---:|---:|---:|
| 10:0 | 403 | 0 | 158749 | 100% | 64.920139% |
| 7:3 | 280 | 1376 | 158761 | 69.860088% | 64.793711% |
| 5:5 | 198 | 2293 | 158766 | 49.586044% | 64.707687% |
| 3:7 | 121 | 3209 | 158763 | 30.045472% | 64.902464% |
| 0:10 | 0 | 4588 | 158760 | 0% | 64.906541% |

The ~0.2 percentage-point spread is consistent with discrete particle counts around the deck target. The P:S labels represent approximate AM mass/volume shares (same AM density), not number fractions.

All five AM scaffold header case IDs match the archived network case IDs. Every AM count matches the raw archive's `dump_type_counts`; all stored AM radii are exactly the deck radii at the scaffold's precision. The external TSV and archived JSON agree on all type counts, and the ionic and electronic network node counts equal the corresponding total particle counts. Those are consistency checks across stored products, not five independent measurements of the same bed.

Additional independent arithmetic using the solver certificate's actual box area and plate gap reproduces the TSV's `phi_se` within 4.7e-13 and its reported porosity within 3.3e-12. Using the separately recorded mass-conserving thickness reproduces `phi_se_mass_conserving` to the same scale. This materially strengthens the linkage of the count/radius reconstruction to the network rows.

## Keep solid composition distinct from whole-electrode volume fraction

The approximately 65% value is AM/(AM+SE), excluding void. On the stored plate-gap volume basis, reconstructed AM fractions are 54.646754%, 55.104702%, 54.223367%, 53.766842%, and 52.469236% in the table order. The corresponding reported porosities are 15.824651%, 14.953625%, 16.202588%, 17.157472%, and 19.161867%.

Using the mass-conserving height gives AM whole-bed fractions of 53.950405%, 54.123952%, 53.273758%, 52.792914%, and 51.514569%. Those alternate height conventions do not change AM/(AM+SE), because both phase volumes have the same denominator. Do not equate either whole-bed AM fraction with a literature fraction defined only over the solids.

Assigning densities 4850/1640 after the simulation would not change the existing radii/counts or turn the same geometry into a 60% AM bed. It would instead make its inferred AM mass fraction about 84.43–84.55%, rather than the original ~81.6%. To compare this stored geometry to a 60%-AM solid-composition experiment, explicitly acknowledge the ~5 percentage-point composition mismatch; a conductivity rescaling alone does not remove it or yield a universal correction.

## Provenance limits

This subset does not include the complete original atom dump or an SE scaffold, so individual SE radii and input bytes were not independently rehashed here. The SE radius is supported by the matched executable decks and the near-exact reconstruction of the stored SE volume fractions. AM radii were actually read from every scaffold row. `build_ps45_kits.py:1–19` describes conversion from webapp case inputs and count checks, and explicitly cautions that it cannot verify that the selected atom dump was the completed DEM trajectory; `:82–85` compares counts to nominal targets within tolerance. Matching IDs/counts is strong internal linkage, not a substitute for original-input provenance.

The volume calculation sums nominal sphere volumes, the same basis consistent with these stored fractions. It is not an exact union-volume calculation for overlapping/deformed particles, nor an experimental measurement of phase volume. Claims about laboratory densities and experimental volume definitions require their separate source evidence.

Finally, the separately retrieved actual-run `network_conductivity.py` at `0801d4ceb540f5a5813761b20a5e0f304ed80a03` is **byte-for-byte identical** to the latest pinned solver tested in `code_scaling.py`: both SHA-256 `da9ecfefd8dc4b84e222140e347e4a718381169f27c88bf56c71ec4a7c2749be`. This closes that solver-file temporal linkage; it does not assert every imported module or input file is identical across the two repository commits.

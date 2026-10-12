# Design adapter and ML contract audit

Reviewed pin `b429c3c1df0956d2721861d89cc29a2d56f2b581` read-only. Executable evidence: `probes/design_probe.py`; output: `evidence/design_probe.json`; invocation log: `evidence/design_probe.log` and `evidence/run_design_probe.json`. No DEM, network calculation, source changes, or supplied-selftest duplication. Temporary regeneration output is confined to the review's `tmp` directory.

## Result

No blocking numerical defect found in the actual committed 20 × 40 adapter output. All 800 cells independently reconstructed from the raw design, elementary sphere volume, phase mass/volume conversion, and stated mapping match (numeric tolerance 1e-9 relative; strings and blanks exact). Production regeneration also matches every output byte.

| Evidence | Result |
|---|---|
| Raw design | 28 rows × 30 columns = supp 20 + thick 8 |
| Raw SHA-256 | `73d9a47f76f49989ddbd2c1237007c8499601d63bd5baf0e1ad11c527f21beb0` = hardcoded sealed input |
| Adapted SHA-256 | `df505b79a756ee3fe2759c740bfb43282dd69035c5a9fb9354a657300117dc0c` |
| Adapted dimensions / uniqueness | 20 × 40 / 20 unique `lhss_001…lhss_020` |
| Families | bimodal 14 / mono_AM_S 4 / mono_AM_P 2 |
| Main loading | exactly ten `2.0`, ten empty cells |
| Maximum integer particle-count residual | 0.4699027304183119 (under 0.5 rounding bound) |
| Maximum reported loading rounding residual | 4.923621065755501e-5 mAh/cm² |
| r2 archive SHA-256 | `baa03b6b65d57b7850df151a011d8102b605fc15d81aa9f58969629ac9d00aff` |
| r2 union | exact 20 selected cases; all lx_um = 50; production union check passes |

Independent physical calculation uses AM density 4800 / SE 2000, insertion volume 3.34e-13 m³, and radii in meters. This avoids calling the adapter/generator count or mass-conversion routines. Source convention `lhs_ext_design.py:133–138` represents the same geometry in scaled deck units; adapting mono_AM_S correctly moves the raw P slot into the S phase.

## Q2: normalize the design source suffix

Acceptable for this generator/schema. `lhs_design_dataset.py:2296–2307` creates meanings as a stable body followed by ` · 원천 = ...`. `lhs_release_build.py:1634–1643` removes that suffix only when source equals `design`, then compares source, verdict, normalized meaning, and caveat. The 22 design columns shared by all three actual schemas agree. A path-only mutation passes; separate body, caveat, and source mutations each fail with the expected shared-column error.

This is equivalence of definition, not authentication of the cited source path. The implementation splits on the first delimiter rather than validating that only a terminal path was removed; no actual generated shared definition embeds that delimiter in its semantic body. I did not promote this hypothetical case to a finding. Source validity belongs to the separately pinned input/manifest checks.

## Q3: loading role and blank code

For the pinned cohort, `X_DERIVED` plus `NA_NOT_DESIGN_INPUT` correctly describes the representation. The main column is a fixed-rule marker: 2.0 where the design uses 2 mAh/cm², empty where volume fraction was independently chosen. The raw inverse-calculated loading stays in the handover provenance column. The blank must not be interpreted as zero, an uncomputed measurement, or a value to impute. No new independent ML factor is needed or authorized.

`lhss_design_adapter.py:148–157` cross-checks rule ↔ pdd_SE ↔ am_pct and insists on the source generator's 2.0 default before emitting the main column. `lhs_release_build.py:824–840` uses that generator's SE_SPLIT for blankness, while `:675` and `:690–691` assign/describe X_DERIVED. Actual data yield zero blank-contract errors. The closest actual supplemental am_pct is 7.5 percentage points from 70, so differing floating tolerances at the boundary cannot affect these 20 rows.

Narrow guard limitation, demonstrated but NOT an end-to-end release bypass claim: for actual fixed row `lhss_005`, `v13_blank_problems` accepts loading values `'99'`, `'-1'`, `'NaN'`, and `'junk'`; it validates only blankness. Empty fixed loading is rejected, and nonempty free loading is rejected. Source: `lhs_release_build.py:833–840, 881–891`. Ordinary use of the SHA-bound adapter prevents these incorrect values; a caller-supplied handover is a broader trust boundary. The old release code already had no numerical loading check, so this should not be presented as new corruption of the normal path. If the author intends the new Q3 gate to enforce the full closed-value contract for arbitrary handovers, add a finite numeric equality-to-2.0 check and a mutation case.

## Q4: 214 fit plus 194 reference

Yes. `lhs_release_build.py:1777–1859` keeps the same locked/free equations and eligibility: only OK/MODEL_BELOW_CONTINUUM_BOUND with finite positive f, phi, CN; NOT_PERCOLATING/NOT_COMPUTED/BAND_FALLBACK are retained as excluded rows with reasons. `:1876–1886` fits all datasets and separately refits datasets whose batch is not supp20 for the reference. It does not append the 194 reference as extra observations or overweight those rows. Raw original 194 measurements remain unchanged, while fitted predictions/residuals for those rows can change when fitting 214; the wording "only summary changes" should be read as preserving the measured input rows, not preserving the derived refit-row predictions.

On the real committed v1.2 / g1 194 rows, the new wrapper equals a direct call to the unchanged fitting routine exactly: 170 included (lhs 106 + lhsx 64), 24 NOT_PERCOLATING excluded. This is an algorithm/path diagnostic, not validation of future g2 coefficients. No real supp20 g2 data exist at the pin, so no 214 numerical fit was manufactured or claimed. Parent runs the provided synthetic 214 path tests.

## Nonblocking documentation finding (new lhss wording copied from older lhsx wording)

Suggested P3: `lhs_design_dataset.py:2275–2276` describes `lhss_w_AM_P` as literal AM_P mass fraction and says `ps_frac = w_AM_P/(w_AM_P+w_AM_S)` without a mono-slot qualification. Actual `lhss_001`, `002`, `003`, `020` are mono_AM_S, with respectively raw P-slot weights 0.3, 0.3, 0.3, 0.375 and raw S-slot weight 0; that formula yields 1, while the correctly adapted `ps_frac` is 0. The raw P column is the generic AM slot in two-type decks, as already documented and implemented by `lhsx_design_adapter.py:15, 82–88` and the new adapter's module header.

This is a handover column-dictionary error, not a numerical adapter defect or a blocker for the 194 launch. Qualify both new lhss raw-weight definitions with the two-type convention and restrict the P/(P+S) formula to bimodal rows; preserve mono_AM_P=1 / mono_AM_S=0. The analogous older lhsx wording already had the same issue; explicitly distinguish that inheritance if reported. Unique lhss provenance columns are not shared across datasets and therefore cannot be protected by the shared-definition comparison.

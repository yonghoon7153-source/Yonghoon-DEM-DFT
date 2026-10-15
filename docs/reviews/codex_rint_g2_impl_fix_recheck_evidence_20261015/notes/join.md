# Join closure notes (RIMP-02 / RIMP-03; questions 3 / 4 / 5)

Pin supplied by parent: `dcb97f1ed942f622d9189eee1a1e9432dc05a655`. All source locations below refer to `source/` in this immutable bundle. Only own probes, notes, evidence and temporary fixtures were written. No production source, Git state, or campaigns changed.

## Closure recommendation

- RIMP-02: **partial**. Every named old adversarial case is now rejected, including its actual plan/quantitative consumer, but two independently demonstrated entrance/schema gaps remain below.
- RIMP-03: **closed within the declared canonical g6 input contract**. Uniform 16-digit originals and single-token trailing-zero changes reject before gate calculations. The scoped contract does not claim to infer the historical producer precision from byte strings: e.g. a low-precision producer can emit the same bytes as g6 for special values. The guarantee is membership in the supported canonical token language and applying the matching six-digit enclosure assumption to each parsed field. Schema completeness is a separate remaining issue.
- Normal real14, case15, synthetic baseline and declared D19 positive remain PASS. Quantitative production HOLD remains unchanged.

## Questions 3 / 4 / 5

Q3: Yes to the **record design**. Entrance REJECT with skipped `g_geo/g_frame` plus explicit reasons separates uncomputed/uncertified data from PASS. Negative/uncertified AM-AM rows reject at `rint_iface_join.py:645-651`. Actual consumer `_iface_join_record` at `step3_sigma.py:1436-1439` turns a REJECT or nonempty rejections list into `join_gate_failed`; `iface_require_quantitative` rejects at `1611-1613`. Census checks `status` and exits at `rint_t41_census.py:195-197` before using `delta_bound_um` at 202. The prior probe's KeyError is its old assumption that a rejected record has a computed delta bound, not an acceptance bypass. However, implementation closure remains partial because the entrance can still misclassify the two cases below.

Q4: Yes **for AM-AM area certification only**, which is what the current source and record now explicitly claim (`rint_iface_join.py:652-653`, `691-695`). This is not certification of all contact areas. Independently parsed case15 negative rows are zero-based 7589 (ids 31,29241; AM_P,SE; -1.86036e-7 sim²) and 9374 (ids 38,29241; AM_P,SE; -1.86264e-7 sim²). Both are outside AM-AM; the 119 AM-AM rows are all certified. Nonfinite fields and frame consistency still apply to the consumed rows of other kinds; the negative-area exception is not a blanket input-validation exemption.

Q5: Yes within the canonical six-digit contract. `rint_iface_join.py:176` checks token equality to `%g` of the parsed finite value; entrance uses format diagnostics at `438-443`; the helper call remains at 640 and helper's `AREA_CHECK_SIGFIG = 6` remains at `lhs_descriptor_harvest.py:164`. Helper SHA256 matches the prior snapshot exactly: `96fa643e309aab46b2a5cbd59e2276ee16b99107a9a7514e5d9fdcaf5c2d8d9e`. No tolerance loosening or helper mutation was used.

## Proposed RIMPR-01 P2: parser discards invalid frame content before validating it

Primary location: `scripts/rint_iface_join.py:245-253` (especially 250-251: append only rows whose width equals header width). Count validation at 522-523 compares the header to **parsed retained rows**, so a malformed numeric row disappears before the declared-vs-physical count check. Duplicate required column names also resolve silently to the first occurrence at 280 and 306. Scalar timestep/count readers take only the first token at 224 and 234.

All probes use genuine `am_iface_join` output; no record editing, rehashing, monkeypatching or solver execution is involved. Baseline geometry is two radius .001 sim spheres at (.002,.002,.002) and (.0035,.002,.002), delta .0005, true area 1.3744467859455347e-6 sim², encoded canonical area 1.37445e-6. Both atoms are AM_P. A genuine ledger is built from that baseline and each join is passed to `am_iface_plan` and `iface_require_quantitative(sid=sid, vox=.25)`.

| Mutation | Declared / physical / retained | Actual outcome |
|---|---|---|
| Insert a 24-column numeric contact row immediately after ENTRIES, **before** the valid 23-column row | 1 / 2 / 1 | join PASS, rejections [], plan PASS/rejections [], quantitative guard ACCEPT |
| Insert a 7-column numeric atom row immediately after ATOMS, **before** two valid 6-column rows | 2 / 3 / 2 | same PASS/ACCEPT |
| Add second `radius` header and `nan` in the second radius column in both atom rows | 2 / 2 / 2, widths 7 | entrance nonfinite=0, join PASS, quantitative ACCEPT |
| Contact TIMESTEP line `100 0.9` | first token read as 100 | join PASS, quantitative ACCEPT |
| Contact count line `1 garbage` | first token read as 1 | join PASS, quantitative ACCEPT |

The first two are **numeric data inside a current frame block**, not a trailer or legal comment. They reproduce the original row's valid tokens then append one numeric zero. Removing that extra zero makes them ordinary duplicate rows, and the positive rejection controls correctly return `count_mismatch` + `dem_duplicate_pair` (contact) and `count_mismatch` + `atom_id_duplicate` plus ambiguous mapping (atom). Thus rejection is lost specifically because width-invalid rows vanish before validation.

Evidence: `evidence/join_independent.json`, keys `malformed_numeric_contact_row_inside_block`, `malformed_numeric_atom_row_inside_block`, `duplicate_radius_column`, `step_extra_token`, `count_extra_token` and `wellshaped_duplicate_*_control`. Exact fixture bytes are under `evidence/join_fixtures/` with matching prefixes, plus `evidence/join_fixture_manifest.json`.

Impact boundary: this defeats the claimed complete-frame/count/required-field certification and passes the existing plan guard. It does **not** demonstrate changed physical conductivity or any real-data corruption. The current area/geometry consumer still operates on retained valid rows.

Minimum fix/regressions: count/reject every nonempty malformed data line in the current frame instead of silently skipping; reject duplicate required column names (ideally duplicate headers generally); require each scalar step/count line to have exactly one token. Preserve these exact numeric-in-block fixtures and duplicate controls, and assert rejected joins propagate to `join_gate_failed`. Keep baseline and D19 positives.

## Proposed RIMPR-02 P3: Decimal-finite scaffold token becomes float64 infinity

Primary location: `scripts/rint_iface_join.py:340-357`, especially 347 and 353-357. Finiteness is counted using `Decimal.is_finite()`, then actual numeric arrays are independently parsed as float64. A finite decimal of magnitude 10^309 becomes infinity in float64, but `n_nonfinite` stays zero; the radius-positive count also excludes nonfinite values (`np.isfinite(rr) & ~(rr > 0)`). Subsequent radius comparison at 613-615 divides infinity by infinity, obtains NaN and does not reject (`NaN > 1` is false). Scaffold delta comparison at 633-635 similarly does not reject.

Replacing only the **second scaffold radius** with either `1e309`, or the unambiguously fixed-decimal token `'1' + '0'*309 + '.000000000000'`, returns entrance PASS, n_nonfinite=0, n_nonpositive_radius=0, join PASS/rejections [], matched=2, max_radius_ratio=0.0, area_all_certified=true, and particle radii `[1.0, inf]` µm. The fixed-decimal **negative** equivalent also returns PASS with `[1.0, -inf]`. Thus this is not an objection about unsupported scientific scaffold notation.

Evidence keys: `scaffold_float64_radius_overflow`, `scaffold_fixed_decimal_radius_overflow`, `scaffold_fixed_decimal_negative_radius_overflow`; exact CSV bytes in the corresponding fixture files. `max_delta_scaffold_ratio` is NaN and runtime warnings expose invalid division.

Boundary that limits severity: `step3_sigma._iface_input_check` at 1054-1055 independently rejects nonfinite radius. Actual `am_iface_ledger` called on the returned infinite particles raises ValueError (`overflow_matching_ledger`). Pairing the join with the prior finite baseline ledger raises `join_particles_mismatch` instead. No numerical or quantitative execution bypass is claimed for this case. P3 is proportionate to a remaining malformed-input certification hole with this downstream defense; RIMP-02's broad e1/e2 claim remains incomplete.

Minimum fix/regressions: check finiteness on the **float64 arrays actually used**, not just Decimal metadata; reject overflow before comparisons/fingerprints. Retain Decimal only for decimal precision accounting. Add both positive and negative fixed-decimal overflow tokens, and assert `nonfinite_value`/REJECT, skipped geometry, finite normal controls unchanged. The separate exact integer token `9223372036854775808` raises OverflowError during int64 assignment at 156; this is fail-closed parser hardening rather than an additional false-PASS finding.

## Original probe executions and adaptation

The wrapper `probes/join_original_runner.py` reads original probe text from the old review unchanged and compiles it with virtual `__file__` rooted in this new bundle so imports and outputs use the new source. It stores original SHA256, rc and traceback in `evidence/join_original_*_run.json` and logs.

| Original | rc | Result |
|---|---:|---|
| join_adversarial.py | 0 | real14 baseline PASS; negative area area_negative; NaN area/pos/delta nonfinite_value; tilt box_tilted; fractional timestep int_token, observed contact step None |
| join_synthetic.py | 1 | baseline REJECT numeric_format, n=16 (atom 8 + contact 8), g_geo/g_frame skipped; original KeyError `delta_bound_um` preserved |
| join_global_precision.py | 0 | both equal-value trailing-zero edits REJECT numeric_format at entrance |

Adapted `probes/join_synthetic_adapted.py` changes the normal fixture formatter to `%g`, handles empty area arrays in early rejects, and redirects artifacts. The **uniformly 16-digit +1ppm attack is explicitly kept uniformly 16-digit**; converting it to g6 would erase its mutation because both area values round to the same token. All changes are in `evidence/join_synthetic_adaptation.diff`. Six original main mutations now reject and their plan guards raise ValueError `join_gate_failed`: negative area; NaN area; NaN position; NaN delta; 16-digit +1ppm; different tilt.

Near-concentric caveat: merely converting the old centers .002 and .002000001 to `%g` merges them, so the preserved old geometry rejects by scaffold ambiguity before area checking. Independently translate both centers in x by -.002, preserving exact distance 1e-9, radii .001 and supplied area **100 sim²**, so the g6 tokens remain distinct. This returns area_uncertified, tested=0, uncertified=1, area_all_certified=false. Supplying the true area instead also rejects for the same certification reason. Evidence keys `uncertified_100_translated` and `uncertified_true_translated`. No attack was reduced to obtain an expected result.

## Quantitative positive and boundary controls

| Control | Outcome |
|---|---|
| real14 | PASS, matched 457/457, AM-AM 660, tested 660, uncertified 0, negative 0, seam 70, certain pairs 563, missing 0 |
| case15 | PASS, matched 104/104, AM-AM 119, tested 119, uncertified 0, negative 0, seam 10, certain pairs 106, missing 0; out-of-scope negative rows 2 |
| both real beds delta bound | 0.002915255888325765 µm |
| synthetic normal | PASS, tested 1/1; plan no rejections; quantitative guard ACCEPT |
| D19 synthetic atom step 100/contact 101, declaration matches | PASS, declaration and observed steps retained; plan no rejections; quantitative guard ACCEPT |
| D19 undeclared / wrong declaration / unnecessary declaration | respectively timestep_mismatch / geom_reuse_mismatch / geom_reuse_not_needed; guards reject |
| contact pos .002 → .00200001 | canonical g6, PASS, max_pos_ratio 0.999999999638789 (touching rounding enclosures) |
| contact pos .002 → .00200002 | canonical g6, REJECT pos_mismatch, max_pos_ratio 1.99999999927758 |
| area tokens 1.37442e-6, 1.37443e-6 | area_enclosure REJECT |
| area tokens 1.37444e-6, 1.37445e-6, 1.37446e-6 | PASS under input uncertainty enclosure |
| area tokens 1.37447e-6, 1.37448e-6 | area_enclosure REJECT |

Additional straightforward negative cases cover NaN/inf scaffold values, zero/negative radii, fractional id/type/scaffold type/count, reversed/extra-token box bounds, trailing zeros, noncanonical plus signs/exponent spellings. Correctly rejected. Finite malformed integer overflow remains an exception, not a PASS.

## Exact command family

Working directory: `C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20`.

Environment for all executions:

```powershell
$env:PYTHONPATH = 'C:\Users\Administrator\Documents\Codex\2026-08-24\claude-stoic-knuth-nobvq-x20\lhs_coverage_review_20260930\deps;C:\Users\Administrator\Documents\Codex\2026-08-24\claude-stoic-knuth-nobvq-x20\gen2_network_reverify3_20261007\deps'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B 'rint_g2_impl_reverify_20261015/probes/join_original_runner.py' join_adversarial.py
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B 'rint_g2_impl_reverify_20261015/probes/join_original_runner.py' join_synthetic.py
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B 'rint_g2_impl_reverify_20261015/probes/join_original_runner.py' join_global_precision.py
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B 'rint_g2_impl_reverify_20261015/probes/join_synthetic_adapted.py'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B 'rint_g2_impl_reverify_20261015/probes/join_independent.py'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B 'rint_g2_impl_reverify_20261015/probes/join_pack_evidence.py'
```

Adapted and independent probes returned rc=0. Those scripts are evidence generators, not all-green assertions: their JSON deliberately records the remaining false PASS cases. Parent runs the author regression suite separately; no duplicate full suite run here.

# Join workstream — pinned 1087a9b2f4a93aa6a3b0debc698a14fffa13488d

Scope: `scripts/rint_iface_join.py`, `step3_sigma.py` join integration, `test_rint_g2_join.py`, request Q3–Q5. Read-only snapshot; all mutations below are generated temporary copies. No solver campaigns or source edits. Existing supplied real14 join returns PASS; these findings do not say the supplied real14/case15 inputs contain the mutations. Production runs/data remain outside this review, and quantitative adoption/production HOLD remains.

## Finding J-A: strict provenance gate fails open on invalid or discarded input

Suggested priority P1 for the gate-correctness claim (not a demonstrated production sigma defect).

1. Nonfinite contact geometry is accepted. In real14 contact file line 22, the first AM–AM row (ids 1,201), independently changing `pos1.x` from `0.0250327` to `nan`, delta from `0.000199496` to `nan`, or area from `1.8247e-06` to `nan` each gives `status=PASS`, `rejections=[]`. Comparison predicates `abs(res)>tol`, `dd>wd`, and `delta<=0` do not reject NaN. Source: `rint_iface_join.py:337–338`, `:350–358`, `:432–440`; readers `:176–180` and `:200–206` have no finite-value gate. The area helper is not itself a finite-input validator. For NaN position the maximum-ratio reporting can also conceal the problem because max comparisons involving NaN do not raise a failure.

2. A diagnostic exclusion is treated as certification. Changing the same real14 AM–AM area from `+1.8247e-06` to `-1.8247e-06` gives PASS with zero rejections; `n_area_tested` drops from 660 to 659 while the join contains no negative-area rejection/count. `rint_iface_join.py:437–441` only rejects `beyond`. Imported `_contact_area_rows` explicitly masks negative and uncertified rows out of `beyond` (`lhs_descriptor_harvest.py:637–657`, particularly `:648–651`), because its original caller is reporting diagnostics rather than enforcing a gate. A separate two-sphere case with radii .001 sim, center separation 1e-9 sim, delta .001999999 sim and supplied area **100 sim²** (true intersection area `3.141592653589008e-06 sim²`) returns PASS with `n_area_tested=0`, `n_area_uncertified=1`. Thus `n_area_beyond=0` is not equivalent to all rows certified.

3. Box identity loses tilt information. With `ITEM: BOX BOUNDS xy xz yz ...`, setting atom xy tilt to `.001` and contact xy tilt to `.002` while retaining identical first-two bound columns returns PASS and `box_equal=true`. The parser keeps only the last three header fields and first two numeric fields at `rint_iface_join.py:142–143`; equality at `:316–318` then compares already-truncated metadata. Orthorhombic-only scope should explicitly reject tilted boxes; otherwise all tilt components need comparison and a correct triclinic minimum-image calculation. This is an input-domain failure, not evidence that the current real14 orthorhombic box is wrong.

4. Lower-priority parse hardening: contact step text `2060000.9` becomes integer `2060000` and passes against the genuine atom step (`:129`). IDs/types use the same lossy `int(float(...))` pattern (`:176–177`, `:200–201`). Require exact integral tokens and supported domain instead of silently normalizing malformed identity metadata. This is malformed-input hardening, not the principal valid-format counterexample.

Actual consumer reach: `probes/join_synthetic.py` builds a two-particle .25 µm raster, calls the actual join, `am_iface_ledger`, `am_iface_plan(join=...)`, then `iface_require_quantitative(plan,sid=sid)`. Independent negative area, NaN area/position/delta, and different box tilts all produce plan `iface_join.status=PASS`, no plan rejections, and `iface_require_quantitative=True`. This checks the current implementation boundary without claiming production authorization or running a conduction solve. Existing finite tamper tests only exercise finite +1nm / +1% cases and so do not cover this.

Fix direction: validate schema, finite numeric fields, positive radii/box lengths, exact integer metadata, supported box form, and the complete certification mask before any PASS. Explicitly reject or return an unverified state for negative/nonfinite/uncertified area rows. Add each mutation as a negative test. Keep the already-frozen diagnostic helper semantics intact if necessary by enforcing strict checks in this consumer.

## Finding J-B: inferred precision is not used by the area gate

Suggested priority P2 (claims outside verified uniform six-significant-digit producer domain).

`rint_iface_join.py:106` infers file S=max(6, observed), stores atom/contact S and `h_area` (`:206`), and uses inferred token half-widths for positions/delta. But `:437` calls `_contact_area_rows` without those precisions or half-widths. That helper uses fixed `AREA_CHECK_SIGFIG=6` (`lhs_descriptor_harvest.py:164`, defaults at `:450`, `:545`, and use at `:637–651`). The consumer's apparent measured-precision rule does not hold for area.

Actual uniform 16-significant-digit counterexample:

- two AM spheres, radii `.001` sim, center distance `.0015`, delta `.0005`;
- shared `lens_geometry` area `1.3744467859455347e-06 sim²`;
- supplied area after +1 ppm mutation `1.374448160392321e-06 sim²`;
- 16-digit enclosure: `[1.3744467859455032e-06, 1.3744467859455659e-06]`;
- even retaining the wider six-digit producer-error bound `E=1.67859784936371e-20`, the mutated token interval is disjoint by about `1.3744e-12`;
- actual join records atom S=contact S=16, `n_area_tested=1`, `n_area_beyond=0`, status PASS; actual plan and quantitative guard also PASS.

Remedy: propagate supported per-file/per-field precision into the common enclosure implementation, or explicitly constrain/reject input outside the certified six-digit producer format. This is separate from the known lack of DEM-area adoption: the current certificate already claims area agreement.

## Conditional `_half_ulp` limitation — do not overstate as a supplied-data defect

`probes/join_global_precision.py` appends ten redundant trailing zeros to one first x token (`0.0250327` → `0.02503270000000000`) without changing its numeric value. Atom-only modification rejects seven `pos_mismatch` rows. Contact-only modification rejects 21 position rows and 99,113 delta-consistency rows out of 106,563. The global maximum precision shrinks uncertainty for all unrelated tokens.

The requested rule explicitly assumes one file-wide `%g` precision, and supplied datasets demonstrably use S=6. Under that producer guarantee the rule is coherent; the probe shows that observed max digits alone is not proof of a uniform producer format. Treat this as a declared-domain/documentation requirement or conservative mixed-format refusal. Do not silently change to token-local digits: `%g` stripping of trailing zeros makes that unsafe in the opposite direction. Uniform16 positive area mismatch above is the concrete current-API issue even when format is uniform.

## Q4/Q5 and non-findings

- D19 logic matches the written contract: undeclared different steps reject; declared atom/contact steps must exactly match observed parsed steps; same-step declaration rejects; geometry/box/id checks still execute. Empty reason is permitted by implementation, but contract only mandates declaration plus two steps, so not promoted to a defect.
- `join=None` leaves row construction and area source unchanged; changing only descriptive join-status text is consistent with the scoped numerical OFF-bit claim, not byte identity of serialized report text. Root is independently running the supplied baseline tests.
- DEM class/area adoption, payload wiring, full production inputs, periodic quantitative solves remain disclosed HOLD/unsupported scope. The gate intentionally checks only scaffold-certain contact subset completeness; it does not prove completeness of ambiguous contacts or all SE contacts. Do not infer full-contact-set certification from PASS.
- Plan-record summary omits full particle/contact arrays, type_map/scale, and some source join fields, but preserves input hashes and `fp_join`. This is an auditability limitation if only the summary is retained; not a demonstrated contract breach by itself.
- `fp_join` is an accidental-mutation consistency hash, not authentication. A caller that edits a join and deliberately recomputes the public hash can forge it. In an explicit boundary probe, shifting all certificate particle coordinates +100 µm, leaving declared `fp_particles` stale, and recomputing `fp_join` yields plan PASS (`step3_sigma.py:1441` compares stored particle hashes only). Consider recomputing the inner fingerprint for consistency, but do not claim a cryptographic security defect without an untrusted-certificate threat model. Fresh join results are internally consistent; stale edits without rehash are detected.

## Reproduction and files

Run from workspace root with bundled Python and the two local dependency directories. Set `PYTHONDONTWRITEBYTECODE=1`, `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=1`, and TEMP/TMP to `rint_g2_impl_review_20261014/tmp`. No network needed.

- `probes/join_adversarial.py` → `evidence/join_adversarial.json`: real14 baseline and independent invalid fields, mismatched tilts, fractional step.
- `probes/join_synthetic.py` → `evidence/join_synthetic.json`: tiny actual join/plan/quantitative-guard reach, uniform16 area enclosure, uncertified area, explicit rehash trust-boundary probe.
- `probes/join_global_precision.py` → `evidence/join_global_precision.json`: numeric-equivalent formatting variants.

All three scripts finished successfully. Generated raw copies are confined to `tmp/join_*`; supplied snapshot files remain unchanged.

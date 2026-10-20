# Independent numeric input review

Scope: RIMPR-02 and the already-open RIMPR-03 / RIMPR-04 limitations. Current source is the immutable `2b9efa253edbf455c2e1abfef1d60e51818e01f8` snapshot; comparison source is immutable `dcb97f1ed942f622d9189eee1a1e9432dc05a655`. Read current AGENTS, submitted 10-20 request, and the prior 10-15 report in full. No source, Git, old artifact, WSL, or campaign changes.

## Judgment

RIMPR-02 closes at its requested input boundary: actual float64 scaffold values and exported scaffold units are checked, and consumed integer tokens outside int64 now produce structured rejection. The named prior false-PASS examples are fixed. Both normal beds remain PASS with the same certification counts.

RIMPR-03 remains an accepted non-ASCII integer spelling with the same numerical identity, and may remain P3 deferred.

RIMPR-04 remains preexisting and may remain P3 deferred at the stated production-scale/HOLD boundary, but its impact must not be described as always fail-closed or as only an unusable `delta_bound_um=inf` diagnostic. A preserved, separately replayable example now demonstrates false G-frame PASS plus `iface_require_quantitative` ACCEPT with normal AM particles and a finite AM bound. No incorrect AM sigma or production effect is demonstrated. The error is an unfulfilled frame-consistency certificate for an extreme, non-AM contact row; the normal AM plan is unchanged.

## Reproduction

From this review root, with the bundled interpreter:

```text
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B probes/numeric_review.py
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B probes/numeric_review.py --baseline
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B probes/numeric_overflow_replay.py
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B probes/numeric_overflow_replay.py --baseline
```

The scripts set all BLAS thread counts to 1 and disable bytecode. Dependencies: sibling `lhs_coverage_review_20260930/deps` and `gen2_network_reverify3_20261007/deps`. Environment: Windows Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3. The unavailable Windows `resource` import is shimmed only for memory diagnostics, with `ru_maxrss=NaN`; numerical functions are not replaced.

Results:

| Run | Cases | PASS | REJECT | Exception |
|---|---:|---:|---:|---:|
| Current | 113 | 15 | 98 | 0 |
| Baseline | 113 | 19 | 56 | 38 |

These counts include deliberately invalid fixtures and retained P3 controls, not a test pass/fail tally. Current ordinary invalid-input cases have structured rejection and a blocked consumer. The `one_far_1e306` case records join rejection directly; the other unit-overflow probes additionally exercise plan/quantitative rejection. The two real-bed controls are additional to 113 cases.

Primary evidence: `evidence/numeric_current.json`, `evidence/numeric_baseline.json`. All synthetic input bytes: `tmp/numeric_current/` and `tmp/numeric_baseline/`.

## RIMPR-02 details

Current `rint_iface_join.py:412` requires both finite Decimal and finite `_safe_float` for scaffold precision/input accounting. `:486` checks the actual coordinate/radius products with `sim_to_um`. `:167–174` checks normalized decimal integer digits and exact inclusive int64 bounds before int64 array assignment.

Probes cover:

- Every scaffold real column x/y/z/r with `±1e309` and signed fixed-decimal `1` followed by 309 zeroes plus `.000000000000` (16 fixtures).
- Every scaffold real column with `±1e306`, which is float64-finite but overflows `×1000` (8 fixtures). The positive `one_far_1e306` additionally uses a single particle with a fixed-decimal coordinate, matching atom coordinate, and zero contact rows.
- Every consumed atom real column x/y/z/radius, every consumed contact real column pos1/pos2/pflag/area/delta, and all six box tokens in both dumps with out-of-float64 values (38 fixtures).
- All nine integer positions (two steps, two counts, atom id/type, contact id1/id2, scaffold type) with `2^63`, `-2^63-1`, and 5000-digit integers (27 fixtures).
- Exact int64 min/max identifiers and steps; 5000 ASCII leading zeros followed by 1; all preserve exact identity and normal PASS / quantitative ACCEPT.
- Noncanonical float spellings `+0.002`, `0.0020`, `2e-03`, fullwidth `０.００２`, underscore `0.0_02`, hexadecimal `0x1p-9`, and underflow token `1e-9999`. All are structured REJECT rather than a silently changed accepted numeric value.

Named old-to-new cases:

| Evidence key | Baseline | Current |
|---|---|---|
| `scaffold_radius_exp_pos` | PASS, infinite returned radius; consumer particle mismatch | REJECT, `nonfinite_value`, geometry skipped, consumer `join_gate_failed` |
| `scaffold_radius_fixed_pos` | Same false PASS | Same structured rejection |
| `scaffold_radius_fixed_neg` | Same false PASS with negative infinity | Same structured rejection |
| `one_far_1e306` | PASS, infinite exported coordinate | REJECT, `nonfinite_value`, `scaffold_um` count positive |
| `int_atom_id_over` | OverflowError | REJECT, `int_token`, consumer blocked |

The rejected records may retain infinite original particle values for diagnosis. This is not a PASS or a geometry computation; the guard receives `join_gate_failed`.

Normal controls:

- `real14`: PASS; scaffold/dump matched 457/457; AM–AM tested 660/660; zero negative or uncertified AM–AM areas; bound `0.00291525588832576 µm`.
- `case15`: PASS; matched 104/104; AM–AM tested 119/119; zero negative or uncertified AM–AM areas; same bound. The two negative AM–SE areas remain explicitly outside AM–AM certification.
- Two-sphere normal synthetic: PASS, bound `2.732324012649634e-05 µm`, plan has no rejections, quantitative guard ACCEPT.

## RIMPR-03

Current `rint_iface_join.py:79` still uses `[+-]?\d+`. Fullwidth digits and Arabic-Indic digits are accepted by this grammar and Python's integer conversion. The all-fullwidth consumed integer fixture is PASS on both pins and reaches quantitative ACCEPT. Its particle fingerprint and atom-id mapping equal the ASCII fixture. Real float columns using fullwidth digits are rejected by canonical `%g`.

This is a lexical contract limitation, not demonstrated loss of numerical identity or integer range enforcement. Keep existing P3 ID and defer without describing the parser as ASCII-only. The new leading-zero normalization strips ASCII `0`; long Unicode zero padding can therefore be rejected despite numerical equivalence, another consequence of the same unresolved lexical contract.

## RIMPR-04: known derived-bound example

`one_far_1e160`: one AM particle at x=`1e160 sim`, radius `.001 sim`, no contacts. Input and exported coordinate `1e163 µm` are finite. Both pins return join PASS with `g_geo.delta_bound_um=inf` and an overflow warning at current `rint_iface_join.py:767` (baseline `:678`).

Calling the actual ledger with this derived bound raises `ValueError: ①′ delta_bound_um 은 유한한 0 이상: inf` at `step3_sigma.py:1202`. The same behavior occurs for exponents 200 and 305. Exponents 150 and 159 have finite calculated bounds; their tiny empty-grid diagnostic ledger calls return successfully.

The `finite_bound_override` field in the 1e160 evidence passes an independently supplied `.001` bound into the ledger and uses an empty grid. It is an explicitly out-of-contract consumer misuse/control, not equivalent to the normal workflow that consumes the derived bound, and not evidence of a valid astronomical-scale scientific calculation.

## RIMPR-04: stronger false-PASS example, preexisting

Minimal replay reads `tmp/numeric_current/huge_nonam_inside_box_{sc.csv,atom.dump,contact.dump}` and calls the actual join, planner, and quantitative guard on both source snapshots. Evidence: `numeric_overflow_replay_current.json` / `numeric_overflow_replay_baseline.json`, key `huge_nonam_inside_box`.

The scaffold and two AM particles stay ordinary: centers `(0.002,0.002,0.002)` and `(0.0035,0.002,0.002) sim`, radii `.001 sim`, normal positive contact. Add two SE atoms at `(1e160,.002,.002)` and `(2e160,.002,.002) sim`, both radii `.001`, with a contact row claiming positive delta `.0005 sim`. Both matching dump boxes are x `[0,3e160]`, y/z `[0,.01]`, with `ff ff ff`; all four atoms are inside their box. Headers, counts, integer grammar, all input values, and canonical `%g` spelling are valid. No duplicate/omitted/malformed row is involved.

Current `rint_iface_join.py:641–645` (baseline `:552–556`) squares the displacement and rounding half-widths:

| Quantity | Squaring computation | Stable diagnostic |
|---|---:|---:|
| SE center distance | inf | `1e160` via `math.hypot` |
| tolerance norm | inf | final propagated tolerance `1.0000000001776357e155` |
| absolute delta mismatch | inf | `1e160` |
| mismatch > tolerance | False (`inf > inf`) | True |

Actual output on both pins:

- Entrance PASS; join PASS; no join rejections.
- `g_frame.n_delta_pos_mismatch=0`; `max_delta_pos_ratio=NaN`.
- Normal AM fingerprint unchanged, normal finite AM bound `2.732324012649634e-05`.
- `am_iface_plan(normal_ledger, ..., join=...)`: no rejections; `iface_require_quantitative(..., sid=normal_sid, vox=.25)`: ACCEPT.
- Current `_iface_join_record` at `step3_sigma.py:1420–1451` trusts the PASS/fingerprint/particle agreement and carries this invalid G-frame certificate forward.

The `huge_nonam_1e150_control` uses exactly the same form at coordinates `1e150` / `2e150`. Both pins correctly reject `delta_pos_mismatch`; mismatch ratio is `99999.99998223643`, and the plan is blocked by `join_gate_failed`. Thus the 1e160 PASS is caused by intermediate arithmetic overflow, not a deliberate exemption of non-AM rows from G-frame consistency.

This strengthens existing RIMPR-04's known impact, not a new defect ID or a regression from these fixes. Only AM–AM area certification is restricted in scope; G-frame f6 explicitly checks all contact rows. No new SE area science or requirement is introduced. This reproduction does not demonstrate changed AM rows or sigma, and it is far outside either actual production bed. P3 deferral is defensible with this limit stated; a global “all overflow ultimately fails closed” claim is not.

## Other bounded arithmetic observation

The public API accepts any finite positive `sim_to_um`. With the normal two-sphere fixture and `sim_to_um=1e160`, both versions PASS and the returned `dem_am_am.area_um2` overflows to infinity at current `rint_iface_join.py:799`. The scaffold particles and bound remain finite. Evidence key `finite_custom_scale_contact_area_overflow`.

This is another post-entrance/derived-value limitation of the existing finite arithmetic range, using a nonproduction unit factor. It is not the requested default `×1000` scaffold fix, not a new regression, and not a demonstrated downstream quantitative calculation. Retain as RIMPR-04 scope evidence, not a new ID or a reopening of the named RIMPR-02 minimum fix.

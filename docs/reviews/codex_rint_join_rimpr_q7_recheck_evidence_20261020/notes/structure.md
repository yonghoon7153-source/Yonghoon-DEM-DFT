# Q1 RIMPR-01 and Q2 structural-parser independent review

Review pin: `2b9efa253edbf455c2e1abfef1d60e51818e01f8`.
Prior pin: `dcb97f1ed942f622d9189eee1a1e9432dc05a655`.
Scope: parser structure, original RIMPR-01 counterexamples, final-frame consumption,
normal `%g`/D19/blank-line/gzip controls. RIMPR-02 and Q7 numerical validation are
owned by other reviewers. No production/source, prior artifacts, Git state,
registrations, WSL, DEM or campaigns were modified.

## Conclusion

**RIMPR-01's prior minimum remedy is closed in the tested scope.** All seven
retained original malformed-input examples now produce entrance `REJECT`, skip
G-geo/G-frame calculations, propagate `join_gate_failed` into the plan, and raise
`ValueError` at `iface_require_quantitative`. Their exact original fixture bytes
were read from the prior review's `tmp/join_independent`; they were not recreated
from the submitted selftest. The two original well-shaped duplicate-row controls
still reject under their original count/duplicate diagnostics.

**Normal inputs remain accepted.** The new independent synthetic baseline,
zero-contact baseline, trailing/section-end/row-interior blank lines, gzip, CRLF,
valid signed/zero-padded scalar integers, and correctly declared D19 reuse all
produce `PASS` and quantitative `ACCEPT`. Raw compressed real14 and case15 both
pass and retain their stated matching/AM–AM area-certification counts.

**The broadened "no discarded tokens / exact known sections" claim has a small
residual gap.** Prefix matching plus unrestricted `str.replace()` accepts malformed
ATOMS/ENTRIES/BOX BOUNDS headers. This is present on the prior pin as well; it is
newly exposed, not an introduced regression. Suggested severity **P3**:
certificate/format completeness. The reproduced malformed header cases have
identical consumed physical fields and no demonstrated change to sigma; they are
not the earlier P2 silent omission of bad-width data rows. This does not reopen
the prior narrowly specified RIMPR-01 minimum remedy.

## Method and artifacts

Read in full: current `source/AGENTS.md`, the submitted 2026-10-20 request,
the prior 2026-10-15 final review, and prior independent/replay probe sources.

- `probes/structure_probe.py`: independent serializer with analytic equal-sphere
  disk area `pi*(r*r-(d/2)**2)`, original-byte replay, current/prior module
  comparisons, actual join → plan → quantitative guard, production raw controls.
  No submitted selftest is imported.
- `evidence/structure_results.json`: 144 cases: **112 structured REJECT**,
  **8 ValueError exceptions**, **24 PASS**. Of those PASS results, 14 are
  expected positives (including two raw production controls) and 10 are
  malformed-header false-PASS examples. No expected positive was rejected.
- `evidence/structure_fixture_manifest.json`: SHA256 and paths for new fixture
  bytes; the original-byte replay records the original SHA256 in the results.
- `probes/structure_minimal_replay.py`: two standalone header counterexamples,
  each changing one header in the retained prior independent baseline.
- `evidence/structure_minimal_replay.json`: both counterexamples PASS/ACCEPT,
  explicit field-by-field equality with the normal parser result.
- `tmp/structure_fixtures/`, `tmp/structure_minimal/`: retained fixtures.

No old probe source was rewritten. Prior independent fixtures were read directly.
The new harness adapts the consumer sequence from the prior review but supplies
its own serializer and explicit mutations. The old `rint_iface_join` module is
loaded under a separate name for selected comparisons; its imported numerical
dependencies are the unchanged current modules. This is disclosed and is enough
to localize these parser outcomes, not a claim of whole-stack prior-version
equivalence.

Execution: bundled Python 3.12, `-X utf8 -B`, NumPy/SciPy supplied by existing
sibling review dependencies; BLAS/OpenMP/NumExpr thread counts = 1; temporary
directories remain under the new review root. The Windows `resource` adapter
provides only `ru_maxrss=NaN` for memory reporting; no numerical function is
replaced. Both scripts exited 0.

## Prior counterexample closure

| Exact retained prior fixture | Prior pin | Current join | Current plan/guard |
|---|---|---|---|
| `malformed_numeric_contact_row_inside_block` (24/23-column rows) | PASS | `row_width`; physical rows contact=2, bad width=1; gates skipped | `join_gate_failed` / ValueError |
| `malformed_numeric_atom_row_inside_block` (7/6/6-column rows) | PASS | `row_width`; physical rows atom=3, bad width=1; gates skipped | `join_gate_failed` / ValueError |
| `malformed_extra_contact_row` (short trailing row) | PASS | `row_width`; gates skipped | `join_gate_failed` / ValueError |
| `malformed_extra_atom_row` (short trailing row) | PASS | `row_width`; gates skipped | `join_gate_failed` / ValueError |
| `duplicate_radius_column` (second radius NaN) | PASS | `header_duplicate`; gates skipped | `join_gate_failed` / ValueError |
| `step_extra_token` (`100 0.9`) | PASS | `int_token`; gates skipped | `join_gate_failed` / ValueError |
| `count_extra_token` (`1 garbage`) | PASS | `int_token`; gates skipped | `join_gate_failed` / ValueError |
| `wellshaped_duplicate_contact_control` | REJECT | `count_mismatch`, `dem_duplicate_pair` | `join_gate_failed` / ValueError |
| `wellshaped_duplicate_atom_control` | REJECT | `count_mismatch`, `atom_id_duplicate`, `scaffold_row_ambiguous`, `dump_am_unmatched` | `join_gate_failed` / ValueError |

Current implementation references in `source/scripts/rint_iface_join.py`:

- 244–257: removes only trailing blank lines and joins the complete scalar
  section body, so a second nonblank line is not silently discarded.
- 303–312: visits every nonempty data-section line; saves bad width diagnostics
  and increments `n_rows_physical` even when the malformed row is not used as
  numeric data.
- 341 and 368: duplicate checks for every consumed required atom/contact column.
- 495–502 and 513–527: emits scalar, row-width, required-header-duplicate and
  frame-layout entrance rejections.
- 588–591: returns `_early_reject` before the G-frame code starts at 592.
- 541–561: early-reject record preserves the consumer fields with gates skipped.

## Independent extension coverage

For both atom and contact dumps:

- Every consumed required column duplicated with an extra `nan` value:
  six atom columns, eleven contact columns → `header_duplicate`.
- Count/box/data sections duplicated as separate `ITEM:` sections → `frame_layout`.
- Unknown sections before the first frame, between each section, and after data
  → `frame_layout`.
- Incorrect counts 0/−1/3 and missing count → `count_mismatch`.
  Empty/decimal/exponent/underscore/extra-token/int64-overflow/5,000-digit counts
  → `int_token`.
- Scalar body second line, vertical tab, form feed, leading/interior blank line,
  inline comment, decimal/exponent/underscore, int64 overflow → `int_token`.
- Nonblank preamble, trailing junk row, fourth box line, interior box blank line
  all fail with their relevant entrance diagnostics.
- Missing box or rows, empty trailing TIMESTEP, incomplete trailing frame each
  raises `ValueError`; no join certificate exists and no plan is built.
- A second complete frame and an earlier malformed frame followed by a complete
  valid final frame both give `multi_frame` and are blocked by the plan/guard.
- TIMESTEP/count header suffixes and trailing header tokens → `frame_layout`.

The reader's declared task is to inspect the final frame; it does not promise to
validate every earlier frame's body. The malformed-earlier-frame case was *not*
counted as a parser bypass: the outer one-frame contract already rejects it
(`rint_iface_join.py:593–594`). Similarly, malformed trailing frames that raise
ValueError are fail-closed, although they are not structured entrance REJECT.
The declared minimum did not require converting every absent-section exception
into a certificate.

Optional extra atom/contact diagnostic columns with a nonnumeric unused value
are accepted on both pins. This is recorded as a scope control, not a new defect:
the declared numeric contract covers *consumed* real columns, and required-header
uniqueness applies only to consumed fields. Acceptance does not certify arbitrary
unused columns.

## Normal-data compatibility

| Control | Result |
|---|---|
| Independent two-sphere `%g` baseline | PASS, empty plan rejections, quantitative ACCEPT |
| Independent separated spheres, declared zero contact rows | PASS, empty plan rejections, quantitative ACCEPT |
| Prior original baseline bytes | PASS on both pins, quantitative ACCEPT |
| Section-end/row-interior/file-end blank lines and blank preamble | PASS on both pins, quantitative ACCEPT |
| Scalar-leading blank and interior box blank | REJECT, consistent with declared prior behavior |
| Gzip and CRLF serialization | PASS on both pins, quantitative ACCEPT |
| Steps `+100`, `000100`, `-0` consistently in both dumps | PASS on both pins |
| D19 atom=100/contact=101 with matching declaration | PASS on both pins, quantitative ACCEPT |
| D19 absent/wrong declaration | `timestep_mismatch` / `geom_reuse_mismatch`, guard ValueError |
| Raw real14 compressed data | PASS; scaffold/dump/matched 457/457/457; AM–AM tested 660/660, all certified; physical rows 33,289/106,563 |
| Raw case15 compressed data | PASS; scaffold/dump/matched 104/104/104; AM–AM tested 119/119, all certified; out-of-scope AM–SE negative areas remain 2 |

The raw production results claim join compatibility only; this probe does not
recompute production sigma or claim final quantitative adoption.

## Residual candidate: P3 exact header grammar still normalizes malformed input

Suggested title: **Validate section-name token boundaries and remove only the
leading marker.**

Exact current source:

- `rint_iface_join.py:278–279` classifies `BOX BOUNDS` and row sections using
  `startswith`, without requiring a token boundary.
- `rint_iface_join.py:298` applies
  `secs['box'][0].replace('ITEM: BOX BOUNDS', '').split()`: **every** occurrence
  is removed before the exact three-flag check.
- `rint_iface_join.py:302` does the same for ATOMS/ENTRIES before required-column
  and width validation.
- The explicit header-token check at 286–288 applies only to step/count.

Minimal examples (only one header line is changed; all rows, counts, geometry
and the other dump remain normal):

```text
ITEM: ATOMS id type x y z radius
  ->
ITEM: ATOMSid type x y z radius
```

and:

```text
ITEM: BOX BOUNDS ff ff ff
  ->
ITEM: BOX BOUNDS ff ff ff ITEM: BOX BOUNDS
```

Actual output of `structure_minimal_replay.py`, for **each**:

```text
join_status = PASS
join_codes = []
entrance_status = PASS
frame_layout = all eight counters 0
box_format = {'atom': 'orthogonal', 'contact': 'orthogonal'}
plan_codes = []
quantitative_guard = ACCEPT
all_consumed_atom_fields_unchanged = true
```

The larger probe additionally reproduces atom/contact no-boundary, repeated
marker, and trailing row-marker cases (10 cases total). Each is PASS on both
the prior and current join modules. Examples include
`ITEM: ENTRIESc_cpl[1] ...`,
`ITEM: BOX BOUNDSff ff ff`,
`ITEM: ATOMSITEM: ATOMS id ...`,
`ITEM: ENTRIES ... ITEM: ENTRIES`.

Impact is specifically that the newly documented e6/e4 contract claims exact
known sections and no discarded header tokens, but these headers are repaired
and certified silently. No consumed numeric value or geometry changes in the
minimal reproducer, and no actual production-format false rejection was found.
Therefore P3 is proportionate; there is no demonstrated P2 numerical corruption
from this family.

Minimal remedy: tokenize/validate the leading section-name words exactly, remove
one prefix using slicing or `removeprefix`, and pass the remaining tokens
unchanged to the existing header/box checks. Preserve arbitrary explicitly
unused data columns, normal spaces/tabs, and the current one-frame contract.
Add both examples above and atom/contact equivalents to regression coverage.
Do not widen this into an unnecessary whole-history validation requirement.

Reproduce from the workspace:

```text
python -X utf8 -B rint_join_q7_recheck_20261020/probes/structure_probe.py
python -X utf8 -B rint_join_q7_recheck_20261020/probes/structure_minimal_replay.py
```

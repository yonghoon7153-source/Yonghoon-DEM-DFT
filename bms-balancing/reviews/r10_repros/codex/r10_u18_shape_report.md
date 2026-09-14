# R10 U18 / `ne_shape` adversarial review

Target: `bd6ba4749a92f8d441b4d9176eb876bfc6cc287c`

Focused baseline: `python -m pytest tests/test_r9_codex.py -q` → **12 passed in 19.87s**.  The checkout remained clean.  The probes below create only temporary fixtures and reviewer files under `outputs/`.

## Verdict for this slice

**NO-GO: P1 5.**  R9's named regression tests are green, but the U18 promotion predicate and the canonical `ne_shape` publication predicate are still bypassable.

One command reproduces every case:

```bash
python outputs/r10_u18_shape_repros.py \
  --target work/harness-r10-target-wsl/bms-balancing \
  --output outputs/r10_u18_shape_results.json
```

Expected terminal marker: `R10_U18_SHAPE_REPROS_PASSED`.  Each bad case nevertheless records the production return code `0`.

## P1-1 — an explicitly narrowed state roster replaces the complete canonical unit

- Code: `scripts/ne_shape.py:264-275`, `scripts/ne_shape.py:384-401`.
- Reproduction: the script first publishes a complete canonical unit for declared states `100,200`, then invokes the same production `main()` with `--states 100`.
- Observed: the second call returns `0`, records `status: complete`, and replaces `ne_shape_GITT_Li.csv` with a one-row file.  `--states 100,100` likewise returns `0`, records requested/paired `2/2`, and publishes two duplicate state rows.
- Why: user input replaces the authority roster.  Completeness is calculated only relative to that input, and every such `complete` result shares the same canonical filename.
- Invalidates: R9-04 requested-population closure and R9-06 “only complete reaches canonical.”  `complete` is structurally weaker than the canonical population.
- Minimum condition: validate `--states` as a unique, canonical roster; a canonical publication must equal a code/version-controlled source roster (or an explicit versioned allowlist).  Any strict subset must remain noncanonical/typed partial, or carry a roster digest in a separate artifact identity.

## P1-2 — an extra `error` column disables the entire success-row schema

- Code: `bms_balancing/schema.py:114-136`, especially `:120-121`; `scripts/check_u14.py:190-194`, `:239-241`, `:447-448`.
- Reproduction: candidate rows retain the old scientific values, add `error=pretend...`, and blank `inputs_sha`, `ref_inputs_sha`, `consumed_inputs`, and `ref_consumed_inputs`; bytes/meta are signed normally.
- Observed: full `check_u14 --new NEW --old OLD` returns `0` and prints both “새 스키마: 전부 갖췄다” and “전부 같다.”
- Why: any truthy `error` cell executes `continue`, skipping every required-cell, numeric, and receipt check.  Extra columns are treated only as harmless additions; provenance columns are excluded from numeric comparison.
- Invalidates: R9-03 content/provenance closure and the U18 promotion predicate.
- Minimum condition: use an exact tagged union.  A success row must have exactly `MATRIX_ROW` and no `error`; an error row must have an exact error schema and make the matrix/U18 unit typed partial/nonpromotable.  Never let a free extra column select the validation branch.

## P1-3 — a decoy is accepted in place of the producer's input-role roster

- Code: `bms_balancing/schema.py:80-110`.
- Reproduction: replace both receipts with only `{"decoy":{"path":"not-a-model-input.bin","sha256":"aa…"}}` and recompute the 12-hex aggregate.
- Observed: the full gate returns `0`, calls the schema complete, and calls all numbers equal although `half_cell`, `full_cell`, `literature.gr`, and `literature.si` are all absent.
- Why: `validate_receipt()` validates the shape of whatever roles happen to be supplied, but has no artifact/side-specific required role set and rejects neither missing nor extra roles.
- Invalidates: R9-03 “receipt roles” and U18 provenance completeness.
- Minimum condition: pass a closed receipt schema for `(artifact kind, target/ref)` and require its exact nested role set before recomputing the aggregate.  Reject unknown, missing, scalar, and deeper unvalidated members.

## P1-4 — environment changes and disappearing controls are accepted as the same execution

- Code: `scripts/check_u14.py:37-40`, `:195-212`.
- Reproduction A: old/new rows are numerically identical but candidate meta changes `env` from the fixture environment to Python/NumPy/SciPy `9.9/999/999`.
- Reproduction B: candidate meta deletes `state` and `starts`.
- Observed: both full comparisons return `0`, print “전부 같다,” and report no execution-condition mismatch.
- Why: `env` is required only for presence, never compared.  Every `META_CONTROLS` comparison is guarded by `k in meta and k in ometa`, while those controls are absent from `META_KEYS`, so deleting one disables its equality check.
- Invalidates: R9-03 condition closure and R10's stated U18 condition/environment gate.
- Minimum condition: require every applicable control in candidate and baseline; compare a canonical environment signature and all controls before numeric comparison.  If environment drift is intentionally allowed, make it an explicit nonpromotion/sensitivity mode rather than an omitted check.

## P1-5 — candidate and baseline may be the same directory

- Code: `scripts/check_u14.py:325-362`; there is no distinct-identity check before `check()`.
- Reproduction: provide one valid signed directory as both `--new` and `--old`.
- Observed: return `0`, roster `1/1`, “정본(...candidate)과 전부 같다.”
- Why: the promotion gate permits a self-comparison, so equality can be proven after the independent baseline has already been overwritten or never existed.
- Invalidates: R9-02 exact-baseline comparison as a promotion gate (its basename roster logic works only after two independent roots exist).
- Minimum condition: reject roots that resolve/samefile to the same directory, and bind the report to distinct candidate/baseline manifest identities.  A revision baseline may instead be read from immutable `--old-rev` bytes.

## R9-01..06 assessment

| Prior item | Status | Evidence |
|---|---|---|
| R9-01 duplicate root labels | closed within its declared syntactic boundary | both duplicate explicit labels and multiple implicit `out` labels are rejected by the green focused test; physical-root typed identity was already declared open and is not recounted |
| R9-02 exact artifact roster | partial | distinct-root missing/extra basenames are caught, but a self-root makes the comparison vacuous (P1-5) |
| R9-03 schema/receipt/controls | not closed | P1-2, P1-3, P1-4 |
| R9-04 requested state population | not closed | caller-controlled `--states` can shrink the authority roster (P1-1) |
| R9-05 duplicate matrix keys | closed for its named matrix-row axis | focused regression passes; duplicate *requested states* is a newly opened roster axis in P1-1 |
| R9-06 partial publication | not closed as a canonical invariant | narrowing first converts a partial population into `complete`, then publishes it canonically (P1-1) |

## Reviewer artifact hashes

- `r10_u18_shape_repros.py`: `40385898878974cb9e9f51b22f77c33933117a44ae5ad30de1c8bf8932165cea`
- `r10_u18_shape_results.json`: `13e05054777573d3c18e2dfc73502006fba085c13a0138566f1dc498f9bcdece`


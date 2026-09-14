# R9 provenance / receipt audit

Target verified: `29ef5058e68c0c64dba840ecc5a7495644cb092e`; target worktree remained clean. Reproduction: `outputs/r9_provenance_repro.py`; machine-readable results: `outputs/r9_provenance_repro_results.json`.

## Findings

### R9-PROV-01 — P1 — U18 comparison accepts an incomplete artifact roster

`scripts/check_u14.py:129-130` enumerates only files present under `--new`; `:152-155` pairs only those files to the baseline. It never enumerates baseline-only/expected files. The sole completeness floor is `seen != 0` at `:305-306`, and `:348` therefore returns 0 for any nonempty valid subset.

Reproduction: copy the signed production `out/degeneracy_100_Li.json{,.meta.json}` alone to a new directory and run:

`python3 scripts/check_u14.py --new <one-file-dir> --old out`

Observed rc 0: `산출 1 개 ... 새 스키마: 전부 갖췄다 ... 숫자 ... 전부 같다`. U18 expects 12 artifacts, but 11 absent artifacts are invisible. See result `u18_gate.one_of_twelve`.

Minimal fix: form an exact expected-name set from the current baseline (or a signed run manifest containing command × state × Si) and require equality: no missing, no extras, every expected unit verified. `--schema-only` also needs an explicit expected manifest/states rather than `seen > 0`.

### R9-PROV-02 — P1 — U18 checks provenance column names, not receipts or run controls

For CSV, `check_u14.py:143-145` checks only header membership and never checks any row value. For JSON, `:20` omits the reference receipt and `:141` treats `{}` as present. The comparison projection at `:30-35,159-180` ignores JSON run controls such as `n_starts`, `seed`, `n_grid`, `n_samples`, and `tol_percent_of_best`, and does not cross-check artifact controls with sidecar controls.

Reproduction uses the production CSV publisher and production `read_unit`. All 12 files are present and signed; every matrix/profile row has blank `ref_inputs_sha`, `consumed_inputs`, and `ref_consumed_inputs`. `read_unit(matrix_100)` returns `(True, "일치")`; `check_u14 --new <12-file-dir> --old out` returns rc 0 and says the new schema is complete and all numbers equal. A separately signed degeneracy artifact changed controls from `{starts:24, seed:0, grid:21, samples:400, tol:1%}` to `{1,731,999,1,50%}` and was also reported equal. See `u18_gate.blank_receipts` and `u18_gate.config_mismatch`.

Minimal fix: validate every row: nonempty 12-hex aggregate ids, JSON-decodable target/ref receipt objects, required roles (`half_cell`, `full_cell`, `literature.gr`, `literature.si`), nonempty paths, 64-hex SHA-256, and recomputed `inputs_digest` equality. Require `ref_consumed_inputs` in degeneracy JSON. Compare an exact typed control projection and cross-check data versus sidecar; fail on missing/extra fields.

### R9-PROV-03 — P1 — `eval --compare` validates different bytes from those it consumes

`_compare_dd_eval` parses the MATLAB CSV at `bms_balancing/verify.py:1116`, then `resolve_precision` rereads the path at `:1117` (via `:983`), and `dd_eval_csv_audit` rereads it again at `:1148-1150` (reader at `:682`). No snapshot bytes or input digest are carried through.

Reproduction: snapshot A has a duplicate header (the same production audit returns `invalid`). Immediately after the first read, a normal replacement publishes valid snapshot B. The actual production comparator reads three SHA values `A,B,B`, compares all 32 cells, and returns `complete`; the control with A throughout is `invalid`. See `dd_eval_reread`.

Minimal fix: read once into an `InputBytes`-like object; make parsing, precision resolution and audit accept the same immutable text/bytes. Record full SHA-256 and path in any persisted comparison result. Do not re-open by path after validation.

### R9-PROV-04 — P2 — matrix sidecar scope contradicts the verified CSV

The generic sidecar records singular `half_cell_source=src` and `si_source=$SI` at `scripts/run_states.sh:45-70`. But the matrix invocation at `:211-215` passes neither `--only-source` nor `--only-wdqdv`; `cmd_matrix` enumerates all half-cell sources, all Si sources and both weights at `bms_balancing/verify.py:1361-1368`.

The committed signed `out/matrix_100.csv.meta.json` says `GITT` / `Li`, while its 32 rows contain `{GITT, step_005C}` × 8 Si sources × `{0,1}`. Row receipts remain useful, but the bundle contains contradictory provenance and U18 does not check it.

Minimal fix: producer or locked sidecar writer must emit a typed roster (`half_cell_sources`, `si_sources`, `w_dqdv_values`, exact argv) derived from the verified CSV; do not reuse the degeneracy/profile singular fields for matrix.

## Positive closures

- R8-04 is positively closed for profile CSV: the real `cmd_profile` writer plus optimizer produced three rows, every row carried full target/ref receipt JSON, receipt SHA values matched the consumed half-cell files, and emptying the `.csv.log` did not remove either receipt (`production_paths`). Relevant writer: `verify.py:1563-1568`, atomic publication `:1605-1609`.
- Input parsers bind hashes to consumed bytes: `data.py:63-83` keeps one `InputBytes` snapshot, and `verify.build` parses and records that snapshot at `verify.py:170-190`.
- Canonical bundle byte binding is sound: `provenance.read_unit` returns the exact verified data/meta snapshot (`scripts/provenance.py:194-214`), and current `out/` fails schema-only as intended with 24 missing provenance columns across the eight matrix/profile files.
- The open export contract is genuinely visible rather than hidden: a real matrix optimizer run re-exported the shared full-cell workbook between reference and target builds; the row recorded distinct reference/target SHA-256 values and still published. Thus receipts diagnose the mismatch, but no policy rejects it.

## R9 Q2-Q5

**Q2.** The five observations may enter a draft only as explicitly provisional, provenance-incomplete evidence. They cannot support GO, promotion, causal/source claims, or a normative design requirement until U18 supplies complete receipts and the promotion gate above is fixed. “Numerically unchanged” does not restore the missing source linkage.

**Q3.** Enforce a common immutable snapshot inside the command/build layer, not solely in `run_states`. At command start, resolve and read shared workbook/Gr/chosen-Si bytes once, pass a typed snapshot object to both reference and target `build` calls and all rows, and assert same role SHA for default comparisons. `run_states` should add a campaign manifest, but pre-hashing paths cannot enforce later consumption. Different exports require explicit `sensitivity` mode with A/B snapshot IDs and must not enter the default comparison aggregate.

**Q4.** Yes. Today `run()` converts every nonzero child status to 1 at `run_states.sh:153-168`, and the final wrapper collapses all failures to 1 at `:239`. `ne_shape` publishes its signed CSV/meta before returning 3 (`scripts/ne_shape.py:340-343,413-415`). Default/GO workflows should treat rc 3 as non-success but preserve it as typed `PARTIAL`, validate and retain its receipt/pairing, and return 3 when there are partials but no hard failures. Only an explicit exploratory `--allow-partial` may normalize it; never U18/GO.

**Q5.** Promotion needs an exact 12-artifact manifest, verified bundles/receipts, same inputs and controls, then equality of a defined numerical projection. Whole-file bytes cannot match because run IDs/timestamps/provenance change. Prefer exact parsed IEEE values for deterministic fields; where legacy evidence defines printed decimal tokens, require exact token equality and state that contract. Any moved profile row is not a provenance-only backfill: keep the old canonical, retain the candidate as a new evidence version, reproduce under the pinned old environment, and adjudicate environment/input/optimizer differences. Do not tolerance-promote it or fold it silently into U16.

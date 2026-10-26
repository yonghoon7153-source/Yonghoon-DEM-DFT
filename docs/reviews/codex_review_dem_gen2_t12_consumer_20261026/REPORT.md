# External T12 review — intake index (not the external report)

The [verbatim external report](codex_review_dem_gen2_t12_consumer_20261026.original.txt)
retains every original byte, including line endings. It was named
`codex_review_dem_gen2_t12_consumer_20261026.md` inside the received archive.
Its SHA256 is `ee8ce50a6c7ab5ae3fa92c81ca28b2d89e2cefe581dc87e6b7bb02b1af19b531`.
This index is authored intake metadata, not a rewritten external verdict.
[The path mapping](report-path-mapping.json) records the original and repository names.
The original review_scope.json still names the archive report and its original hash.

The report accepts the P1 contract/observation interpretation and retains the narrow
ULPRI-01/02 closure. T12R-01 remains OPEN until external recheck; physical T12 is NOT_RUN.
Its §6 A–D describes future P2 facts, implementation tests, physical qualification,
and integrated-tree/CI acceptance criteria; no missing measurements are supplied here.

Archive shorthand references resolve to these preserved receipts:

- [Loader and contract checks](evidence/loader/report.json)
- [Thirteen mutants](evidence/mutants/report.json)
- [Independent scope probes](evidence/scope_probes/result.json)
- [Restoration truth table](evidence/scope_probes/restore_truth_table.json)
- [Promisor control result](evidence/promisor_probe/result.json)

The 40-character object ID discussed in T12R-01 identifies a Git **blob** for
ul_gates.py, not a commit. See the structured mapping for its exact ID.
Original source metadata, raw traces and finite inputs remain byte-preserved.
See [INTAKE.md](INTAKE.md) for the selected subset and full-archive replay limits.

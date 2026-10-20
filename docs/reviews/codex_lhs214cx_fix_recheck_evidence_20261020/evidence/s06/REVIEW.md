# S06 independent read-only review — 2026-10-20

Review pin: `34713ac9650ece7c8d59b7c4d9a2aefccee693ea`.
Baseline: `685c2bbdbbfee82898a9ec062bb9c2bc94612fc8`.

**Decision: L214R-S06 / L214S-CX01 is closed. R03 can be marked closed within the explicitly agreed grammar: fenced code blocks and column-zero ATX headings, including empty headings. No new supported-scope counterexample was found. This is not full CommonMark conformance or launch approval.**

## Code inspected

- `scripts/supp20_input_receipt.py:113,142–154`: recognize one to six `#` markers followed by space, tab, or end of line; allow empty content; trim closing hash runs only when preceded by space/tab.
- `:170–191`: fences retain state, all recognized ATX headings become boundary candidates, and h1/h2 close the active h2 section. Empty h3–h6 do not close it.
- `:186`: active §3 identification remains the old level-two plus `3.(whitespace|end)` rule.
- `:202,205,211,215–222`: actual registration path reads with universal newline handling, uses the code-stripped active section, and refuses an absent or ambiguous value.
- `:1364,1373,1382,1400`: resident S12k–S12k4 tests cover the 12 prior fail-open shapes, two false rejections, five controls, and 24 guards.
- `:165–166`: unsupported block grammar remains explicitly documented.

## Independent evidence

Oracle: locally available markdown-it-py 3.0.0, `commonmark` preset. We used block-token heading maps and fenced-code spans, rather than the submitted parser's heading/fence helpers, to determine active sections and value placement. Scope-generating cases avoid lists, quotes, HTML, setext, indented code, and indented headings. Markdown-it's Unicode trimming of heading content is not being certified as the document's §3-identification contract.

| Check | Result |
|---|---|
| Prior 19 heading documents, baseline and new actual `receipt()` | Baseline 14 mismatches; new 0. All 12 false acceptances now fail with R0/D1; both false rejections now accept the valid active value. Five controls preserved. |
| Prior 114 fence documents, baseline and new actual `receipt()` | 0 mismatches in both versions; rc0 count remains 57, rc1 count remains 57. |
| New 8,736 boundary/fence/history combinations | Baseline 608 mismatches; new 0. Includes levels 1–8, empty/ASCII/Unicode tails, closing-hash forms, malformed closers, and values before/after boundaries. |
| Independent deterministic transition documents | 30,000 documents, seed 20261020; baseline 2,212 mismatches, new 0. Includes duplicate §3 candidates and repeated fence transitions. |
| Representative new cases through complete `receipt()` | 12/12 expected values and outcomes. |
| Actual file ingestion with LF, CRLF, and CR | 18/18 expected values, failure IDs, and rc values. |
| Actual registration, old/new tools | Identical values and checks; both rc1 with only D1 failing. |
| Adapted source selftest | 122/122, rc0; metadata and isolated dependency-path adapters explicitly recorded. |
| Receipt source after checks | SHA-256 matches intake manifest: `2c7e0b81dbe81d0518e27c8e1781959b9cc983509a1ce66001028faa3768a2f9`. |

Combination counts are generated test cases, not claims of that many independent defects. The submitted 275,148-line and 234,256-document fuzz counts were inspected but not rerun or included as our independent results.

The actual registration remains:

- Active §3: `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`.
- Recomputed sealed fingerprint: `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`.
- The pending declaration is not used to pass D1. No registration content was changed.

## Original selftest environment failure — do not obscure it

The root agent's unmodified-source executions recorded **baseline 105/118, rc1** and **current 109/122, rc1** in `../original_baseline_receipt_selftest.log` and `../original_current_receipt_selftest.log`. We compared all 13 `FAIL` lines: they are byte-for-byte equal as text. The 13 failing checks propagate an incomplete S7 preflight and missing expected generation (P3/P8). The four new S12k–S12k4 checks all pass in the original current log.

We independently captured the actual isolated child failure. `run_network_194_parallel.py:939` runs `python -I -B -c GEN_PROBE`; the `-I` child cannot see the separately supplied dependency roots. Its traceback reaches `network_conductivity.py:41`, `from scipy import sparse`, then fails:

```text
ModuleNotFoundError: No module named 'scipy'
```

`derive_generation()` consequently returns generation=None and an error (`:943–945`); preflight cannot complete, causing P3, and generation validation causes P8 (`:2053–2057`). The receipt selftest caches this probe at `supp20_input_receipt.py:785`.

The same generation call with **only the dependency directories prepended to the isolated child's `sys.path`** returns rc0, generation=g2, problems=[], error='', and imports `network_conductivity.py` and `tau_flux.py` from the pinned new snapshot. No Git metadata lookup occurs in either generation call. This evidence does not attribute the raw failure to Git or to S06.

The full adapted selftest uses:

1. A metadata-only `git_info` stub because the snapshot is not a Git checkout. It records the declared review pin and dirty=None; it is not clean-tree or author-approval evidence.
2. A dependency-path shim on the exact isolated GEN_PROBE child only. Probe computations, receipt comparisons, thresholds, assertions, and source files are unchanged.

Thus write **“original 109/122 due to isolated-child missing SciPy; explicitly adapted 122/122”**, not “unmodified Windows 122/122.”

## Supported-scope limit

Six explicit out-of-scope controls are retained in `unsupported_scope_controls.json`. In particular, indented headings, setext boundaries, and indented code still diverge from a complete Markdown parser. The submitted request explicitly acknowledges that an empty column-zero `##` inside an HTML block is now treated as a boundary; a control reproduces this behavior. It belongs to the already excluded HTML grammar and is not silently promoted into a supported-scope defect or a full-Markdown guarantee.

No supported-scope counterexample is outstanding. No production source, registration, sealed data, Git state, or launch state was modified; no production batch was run.

## Reproduction and files

From the workspace, use the bundled Python with `-X utf8 -B`:

```text
lhs214cx_recheck_20261020/probes/s06/parser_audit.py all
lhs214cx_recheck_20261020/probes/s06/parser_audit.py selftest
lhs214cx_recheck_20261020/probes/s06/supplementary.py
lhs214cx_recheck_20261020/probes/s06/generation_environment.py
```

Key artifacts in this directory:

- `prior_133_replay.json`: full prior-case oracle, baseline/new helper and complete-receipt results.
- `new_boundary_matrix.json`, `random_transitions.json`: independent generated cases and zero-mismatch totals.
- `new_boundary_receipts.json`, `new_cases/`, `new_receipt_*.json`: representative full-path follow-ups.
- `newline_receipts.json`, `newline_cases/`: actual file newline ingestion.
- `actual_noimpact.json`, `actual_receipt_old.json`, `actual_receipt_new.json`: actual registered document.
- `selftest.log`, `selftest_result.json`: adapted complete selftest and adapter calls.
- `generation_environment.json`: raw and dependency-only child stdout/stderr and return values.
- `metadata.json`, `receipt_source_integrity.json`: tool versions, dependency paths, source identity.

# Probe package dependencies and write audit

Read-only audit of all ten current `probes/*.py` files, 2026-10-19. No package was built and no probe/source was changed.

## Baseline files to include

Preserve sibling directory names relative to `lhs214s_recheck_20261019/`:

```text
lhs214s_recheck_20261019/                 current review, source, evidence, probes, notes
lhs214rr_recheck_20261019/
  source_manifest.json                  exact baseline pin and file inventory
  source/<every path in manifest.files>  exactly the 2,030 manifest-listed files
  evidence/receipt_fence_matrix.json     old 114-case matrix, read by S01
  evidence/receipt_fence_cases/*.md      all 114 named inputs (1,859,718 bytes total)
```

The manifest-listed baseline source set is the recommended exact selection, rather than a hand-pruned import closure. The baseline Flask app loads templates and supporting modules dynamically; old R01 tests and receipt checks read data archives, harvest/design inputs and sealed code beyond their top-level scripts. Keeping this bounded source inventory avoids claiming a smaller untested selection is standalone. All baseline files are read-only inputs. Do **not** copy the baseline source folder indiscriminately: it also contains three unmanifested runtime files, `docs/db/.mtime_cache.json`, `docs/db/metrics_master.csv`, `docs/db/metrics_master.sqlite`; exclude them. Old probes, old HTML outputs, other old evidence and old temporary directories are not required by the ten new probes.

Direct baseline use by probe:

| Probe | Baseline dependency |
|---|---|
| `root_checks.py` | baseline manifest; sealed/handover files; changed old code for diffs; full source if `which=old` |
| `s01_parser_audit.py` | old `scripts/supp20_input_receipt.py`, receipt source/data context, matrix JSON and 114 Markdown inputs |
| `s02_run.py` | old `scripts/test_l214r_r01_restored_full.py` and its source/data dependency chain for label `old` |
| `s02_boundary.py` | old `scripts/network_conductivity.py`, `scripts/tau_flux.py` for byte comparison; numerical diagnostic fixture constants are embedded, no old numerical JSON is read |
| `s04_matrix.py`, `s04_types.py`, `s04_submitted_baseline.py` | old Flask app, scripts, templates and source context; submitted-baseline compiles the **current** new test in memory with old import paths, so no baseline `test_single_null_metrics.py` file must be invented |
| `s04_compare.py` | old `webapp/app.py`, `scripts/analyze_contacts.py`, `webapp/test_tau_labels.py`, `webapp/templates/single.html`, `scripts/check_all.sh`; current S04 evidence/HTML produced by earlier probes |
| `s04_run.py`, `s04_tau_adapter.py` | no direct old files; tau adapter requires the current source manifest and its four TSV entries |

`s04_matrix.py` also reads the archived original probe at **current** `source/docs/reviews/codex_lhs214rr_fix_recheck_evidence_20261019/probes/rr_display_extended.py`; preserve that current source file. `root_checks.py metadata` reads current `evidence/tree_diff.json`, both manifests, and the submitted send request. Replaying comparison scripts requires the earlier current probe outputs; these are not dependencies on old evidence outside the entries above.

## External runtime dependencies

The probes add these sibling paths to Python import search (in this order where applicable):

1. `lhs_coverage_review_20260930/deps/` — Flask 3.1.3, Jinja2 3.1.6, SciPy 1.16.3, NetworkX 3.7, Requests 2.34.2 and their dependencies.
2. `gen2_network_reverify3_20261007/deps/` — NumPy 2.5.3, Matplotlib 3.11.2, Pillow 12.3.0 and plotting dependencies.
3. `lhs214rr_recheck_20261019/deps/` — markdown-it-py 3.0.0 and mdurl 0.1.2, required by S01; root checks also add this path.

These libraries are external to the recommended evidence/source ZIP. The recipient must provision them under the same sibling paths or in the interpreter's normal environment. Existing compiled packages are Windows CPython 3.12 builds and should not be described as portable to Linux. The review interpreter is `C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe` (Python 3.12.14); runner subprocesses use `sys.executable`, so the absolute interpreter location need not be reproduced. Use `-X utf8 -B` and the recorded one-thread environment. Numerical edge results can differ with platform/library versions—the S02 portability result is precisely about this, not a promise of identical failure counts everywhere.

## Write audit and replay isolation

All **direct writes in the ten probes** target the current review's `evidence/` or `tmp/`. Baseline paths and manifests are read, not written. In-memory negative controls in `s02_boundary.py` do not edit source. S01 temporary mutations use `tempfile` redirected into current `tmp`; S04 explicitly redirects application result/upload/archive/MPM folders and temporary directories. Run S04 scripts through `s04_run.py` as documented; that wrapper also supplies dependencies and isolation.

There is one material qualification: `root_checks.py regression` and `s02_run.py` do not themselves set the four `WEBAPP_*` variables. Their child tests import `app` (`test_pipeline_provenance.py:1393`, `test_l214r_r01_restored_full.py:432`); `app.py:317–328` defaults these directories under the selected `source/webapp/` and calls `os.makedirs`. Therefore a bare replay can create source-side directories even though the probes contain no direct source write. The current source has four such empty directories (`uploads`, `results`, `archive`, `mpm_lab`), no files within them. This is an isolation qualification, not proof of production-file mutation. Before replaying any probes, explicitly set `WEBAPP_UPLOAD_FOLDER`, `WEBAPP_RESULTS_FOLDER`, `WEBAPP_ARCHIVE_FOLDER`, `WEBAPP_MPM_LAB_FOLDER`, and `MPLCONFIGDIR` to dedicated children of the **current** review's `tmp/`, set `SUPABASE_URL` and `SUPABASE_KEY` empty, and retain `-B`. Do not claim that the scripts alone guarantee zero directory creation in source. No file changes were made to fix this during this audit.

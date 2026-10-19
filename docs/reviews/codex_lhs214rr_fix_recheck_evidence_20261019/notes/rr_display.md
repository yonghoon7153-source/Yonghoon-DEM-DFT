# Display review working notes (not the final review report)

Scope: fixed source `77d8fd44545c33cd10ab18fc250c7ad3023833ea`; R02/WEB09 accepted ionic refresh, actual `_load_case_tables` and full Flask GET `/single/<id>`, compared with immutable earlier `60ba39e224aff48a030dccfe750342f3bf9db61f` source. No production edits, Git operation, simulations, registration approval, or old-evidence write.

## Results

- Submitted `test_web09_accepted_refresh.py`: 18/18 PASS, rc0. Includes actual small producer-chain cases and loader/full-page comparisons. Evidence `evidence/rr_display_web09.log` and corresponding `_run.json`.
- Submitted `test_pipeline_provenance.py`: 284/284 PASS, rc0. Evidence `evidence/rr_display_pipeline.log`. Reviewed its full diff: numeric sentinels 999→4.2, 5→3.6 and matching expectations, plus explanation; retain distinction from old 1.0 and preserve/force/Stage-E/failure-publication assertions. `evidence/rr_display_pipeline_fixture.diff` records this.
- Old `display_fresh.py` unchanged bytes: 21 cases, 13 checks, errors=0, failed=0. All original seven stale-Δ rows close. `probes/rr_display_old.py` compiles original bytes with relocated `__file__`, redirects only output names to `rr_display_old_replay*`, and supplies a read-only old `display_source.json` for the unrelated K2 fixture. Display inputs all use new fixed source. Adapter and original SHA recorded in `evidence/rr_display_old_adapter.json`; authoritative output `evidence/rr_display_old_replay_source.json`. The K2 reused producer folder is not fresh producer evidence.
- New independent comparison: **128 cases per tree**, 2,288 checks per tree. Fixed source 2,272 pass / 16 fail; baseline 2,216 pass / 72 fail. The 16 failures in both trees are the same null-template issue below; **56 stale-Δ row checks** fail only before the fix. 24 cases change, all 56 changed rows only replace old Δ with `—`; their H/P cells do not change. **112/128 pages HTTP200 and 16/128 HTTP500 in both trees**. Every CSV and full_metrics input byte remains unchanged.

Authoritative current comparison: `evidence/rr_display_extended_source.json`, baseline `evidence/rr_display_extended_old.json`, full comparison `evidence/rr_display_summary.json`. The earlier `rr_display_extended.json` was an initial 120-case probe draft, with 10 false expectations about an optional new-table CF row corrected after checking app.py:3377; it is not the final count. New table's optional CF row is absent when Hertz R_brug is unavailable, as before.

New controls: missing/explicit-null R_brug in H/P/both independently; missing/explicit-null sigma_ratio and both derived sources; accepted current H/P (.24/.72, Δ +200%); legacy missing state keys; model-limit not_computed both with null and stale numeric σ; valid_zero with null and numeric zero, H/P/both; failed/unknown states; new/two-column/split/four-column layouts. Exact input labels are original producer labels; output matching uses their official paper-label mapping. Duplicate rows are not silently collapsed (list of rows per label). Unknown diagnostic sentinel, constriction diagnostic and electronic/thermal rows are checked unchanged, and model-limit missing labels stay intact. Numeric zero never replaces missing ionic values. No derivative helpers or route/template functions are patched.

## R02 / WEB09 conclusion

Original R02 closes at app.py:807–813: every recognized accepted ionic row assigns Δ on every pass, including ref=None and fresh=[]; both current cells retain new-table Δ, otherwise `—`. Following `_mask_unaccepted_ion_modes` app.py:816–834 retains valid_zero/model-limit behavior. Final loader calls refresh/mask at app.py:2592–2593, before paper renaming at :7537. Original and broader asymmetric/missing controls show no new overblocking or stale-cell resurrection.

This supports closure of the original accepted refresh/freshness defect; do not expand into a promise that every malformed/nullable historical full_metrics file can render.

## Additional observation: optional sigma_ratio=null makes the full page HTTP500

Potential P3, pre-existing UI robustness issue, not a change regression or numerical handover gate failure. Minimal change from the normal fixture: keep accepted ionic σ H=.24/P=.72 and set **only `sigma_ratio` to JSON null**. Loader succeeds, ionic row remains `.24/.72/+200%`, missing-current SBI row correctly retains old values with Δ `—`, but Flask GET `/single` returns **500**. Four layouts all reproduce.

Cause: `webapp/templates/single.html:2111–2114` checks `is defined` then formats None with `%.4f`; null counts as defined. When phi_se is omitted to bypass that tooltip branch, the independent tooltip at **:2187–2189** still multiplies null by grain conductivity and the page returns 500. A third same-pattern site exists at **:2272–2275** (source inspection; not separately isolated). Actual stack traces in `evidence/rr_display_extended_source.log`, case evidence `brug_null_*`, `all_derived_null_*`, and corresponding `_no_phi_*`. Captured 500 HTML is under `evidence/rr_display_extended_source_work/all_derived_null_fourcol.html`.

Controls: same input with numeric sigma_ratio=.24 is HTTP200; removing the key is HTTP200; R_brug null alone is HTTP200. Both current and old pinned source reproduce; template bytes exactly equal, SHA256 `78be881634be85f6391b79a4a7bcebf11b7968537fe9d67bd5afb8cbb63df71c`. This is 4 null-input variants × 4 layouts = 16 cases, not 16 different defects.

Reachability limit: `scripts/analyze_contacts.py:649–650` currently only inserts sigma_ratio when its value is not None. I did **not** establish a normal current producer that emits this null; this is a directly persisted/legacy nullable-input robustness case. Missing-key inputs from current producer work. Treat it separately from R02's original missing-key failure and do not use it as an independent numerical HOLD. If accepting legacy nullable derived metrics is the intended contract, normalize null in these tooltips and add full-page controls rather than loader-only tests.

## Reproduction

All commands use bundled Python `C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B` and `probes/rr_display_run.py`, which isolates env/temp/output to this review, uses both requested dependency roots, and fixes OMP/OpenBLAS/MKL/NumExpr threads to 1.

Runner arguments:

```
web09 source/webapp/test_web09_accepted_refresh.py
pipeline source/webapp/test_pipeline_provenance.py
old probes/rr_display_old.py
extended_source probes/rr_display_extended.py source
extended_old probes/rr_display_extended.py old
```

Then run `probes/rr_display_summarize.py` (standard library only). Extended probes deliberately return rc1 when the HTTP500 issue is reproduced. No browser screenshot is claimed: final-screen evidence is full rendered template HTML and parsed visible table cells from actual Flask GET.

## Follow-up: ionic channel metadata mutation versus actual final page

Numeric agent's fresh normal producer fixture (`rr_numeric_scope.json`) was copied read-only into four display cases: baseline and H0 `ionic_status` changed to valid_zero / valid_null / no_result, each with reason no_through_path. This does not change FULL status, numeric value, or certificate. `probes/rr_display_channel.py` invokes **actual `app._network_projection`**, then ordinary loader and full Flask GET. The only adapter is `ps.code_sha` returning the pinned identity while stamping the isolated fixture, avoiding a Git operation; no validation or rendering function is patched.

All four return HTTP200; **entire network-summary loader rows are identical**. Final ionic σ `.8263 / 2.8151 / +240.7%`; network state `계산됨 / 계산됨`; tau handover `OK / OK`; g2 generation contract. Original numeric-agent fixtures remain byte-identical.

Thus the accepted inconsistent channel fields do **not** hide positive σ or corrupt these visible state labels. Display acceptance reads sigma_full_status at app.py:718; visible state reads sigma_full_status/reason at :1055–1062. Actual projection does preserve `ionic_channel_verdict=ok`, `ionic_channel_reason=no_through_path` (:3642–3645), so it remains contradictory channel metadata and can be printed by the pipeline-stage diagnostic formatter `_network_channel_stage` (:3664 onward). These tests establish no numerical HOLD or final summary-table mislabel. Evidence: `evidence/rr_display_channel.json`, `rr_display_channel.log`, and four full HTML files in `rr_display_channel_work/`.

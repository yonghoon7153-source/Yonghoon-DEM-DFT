# RRM reviewer working notes — RIMP-04 / RIMP-06, Q6 / Q7 / Q9

Pin: `dcb97f1ed942f622d9189eee1a1e9432dc05a655`. Immutable snapshot `source/`; no source modifications, Git mutation, network calls, DEM runs, production campaigns, or changed HOLD decision. This is sub-review evidence, not the final review report.

Read `source/AGENTS.md`, the 2026-10-15 recheck request, prior 2026-10-14 RIMP-04/06 findings, current `rint_rrm_reference.py`, relevant `step3_sigma.py` interfaces and `test_rint_g2_rrm.py`. The cwd is an offline snapshot and has no Git repository; read-only `git status -sb`, `git worktree list`, `git rev-parse HEAD` returned that fact. Manifest pin was used instead. SHA256 of the inspected modules matches the pinned manifest:

- `scripts/rint_rrm_reference.py`: `6cb16e030c0a25ce737b6c7a35b2ebc59e451b88521dfac47b4304c8b27c30a0`
- `scripts/step3_sigma.py`: `22839a15c0faf3849180d50c200eaceff0b14c8876e483ce36f4009bebbf9803`

## Reproduction

Probe: `probes/rrm_recheck.py`; generated evidence: `evidence/rrm_recheck.json`. Source imports are asserted to resolve inside the new snapshot. The old `rrm_probe.py` is imported after new `step3_sigma`/RRM/FIX modules, so its old path insertion cannot silently switch the inspected modules. Only its `rrm()`, `geometry()`, and independent `areas()` functions are run; old `boundary_control()` is deliberately not run on the patched harness.

Command from workspace root, exit status 0 (about 3 seconds):

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; $env:OPENBLAS_NUM_THREADS='1'; $env:OMP_NUM_THREADS='1'; $env:MKL_NUM_THREADS='1'; & 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B rint_g2_impl_reverify_20261015/probes/rrm_recheck.py > rint_g2_impl_reverify_20261015/evidence/rrm_recheck.json
```

## RIMP-04 closure and Q6

Recommend **closed within the stated wrapper / trusted-ledger scope**. No new demonstrated RRM numerical failure in these tests.

Relevant exact source lines:

- `rint_rrm_reference.py:333–354`: required recipe fields, finite positive nonboolean k, normalized r table, exact exception-law key set and allowed values.
- `:390–411`: all rows finite/nonnegative, cut tombstones (rface=0 and ck=0), film cid bounds, film rface=0 only if the contact's registered r is zero.
- `:412–431`: candidates come from ledger classification, surviving support and positive geometric area **without filtering by the r table**. Missing r, tilt, and insufficient resolution count exclusions.
- `:433–462`: owner-face traversal, rface equality, missing rows, and explicit required rejection counts. This independently detects the old metadata empty-set failure.
- `:463–479`: planner replay is an additional internal-consistency check. It is not independent model/geometry verification and should not be called that.
- `:483–494`: `rrm_solve` unconditionally calls `rrm_require`, then the generic solver; `step3_sigma.py:1611–1613` rejects an intact plan with registered eligibility rejections.

The old cut-removed+k=5, cut-removed+empty-rtable, and NaN film cases all produce nonempty violations and `ValueError` through `rrm_solve`. Cut-only deletion has 85 `film_off_outside` violations. NaN reports 67 `rface_nonfinite` plus 67 `rface_mismatch` violations; negative film rows report corresponding negative/mismatch violations. The generic gate continues to accept the old mutations, as explicitly disclosed in the request and prior report.

Expanded probe: **25/25 mutations fail both full checks and independent checks 1–3**. To isolate independence, replay was replaced in memory with a stub returning the candidate unchanged, so replay could never reject it. Cases: cut deletion+k/empty table; all rows removed+k/empty table while also setting `n_reference=0`, contacts=[], realized=False; NaN/+Inf/-Inf/negative/unregistered-zero film values; six invalid k values; three missing recipe fields; NaN/negative/Inf r tables; unknown law; nonzero cut rface/ck; out-of-range film cid. Each also fails the genuine wrapper. This is a stronger independence control than rerunning author tests.

Explicit eligibility boundary: disc radius `a=0.40003468599610187`, h=0.1, threshold `a/h=4.000346859961018`. k below and at threshold retain film67/cut85 and pass. k above by relative 1e-12 has zero rows and `rrm_unresolved_subgrid(n=1)`; generic guard rejects it. Clearing this rejection yields `excluded_without_rejection`, including with replay disabled. Equivalent controls cover missing r and tilted contacts (removing the tilted rejection is independently rejected).

Important semantic detail: `rrm_check=[]` for a faithfully generated **rejected** k=5 or empty-table plan is correct as a consistency result; it is not eligibility approval. `rrm_solve` still rejects at the generic rejection guard. Do not present the raw empty violation list as a solve PASS.

Valid positive controls: baseline `rrm_check=[]`, registered r=0 `rrm_check=[]` and wrapper solve accepted; three axis rotations of unequal-radius/mixed-type fixture all pass. Independent quadrature comparison for 1000 disc/rectangle intersections: max absolute error/a² `1.73102875081053e-13` (geometric integration comparison only, not T2/T3 validation).

Baseline σ=`0.003334457143882423 S/cm`, residual `6.6107095948726855e-15`, unconverged=False. No baseline change from old reported result.

Limits: replay is the same planner, and the supplied canonical ledger remains the trusted geometry source; these checks are not cryptographic authenticity of arbitrary replaced ledger/summary dictionaries or independent RRM physical accuracy. The requested fix does not require such expansion. Search of the complete downloaded `scripts/*.py` set finds RRM use only in `test_rint_g2_rrm.py` and its own module; the production scripts do not import it. A follow-up scan also covered all 57 verified `webapp` Python/JavaScript files and found no RRM calls/imports or affected summary-key references. These scopes do not prove absence in unknown external consumers. Direct generic calls in tests are explicit negative-bypass measurements/eligibility controls. Any future actual RRM run must use `rrm_solve`.

## Q7 — generic finite/nonnegative guard

Recommend **yes**, add model-independent `isfinite(rface) & (rface >= 0)` at the common quantitative ingress before assembly, preserving valid r=0. This needs no RRM import and is a common physical row invariant. It is a remaining hardening recommendation explicitly outside the approved RIMP-04 wrapper change; do **not** count the already-disclosed direct bypass as a new regression or reopen RIMP-04 merely because it exists.

The limit is reproducible for ordinary CNC plans as well as RRM plans. After deliberately editing film rows and recomputing row fingerprints (same mutation convention as prior N9 tests), the generic guard accepts both NaN and negative rows even when vox is supplied. `step3_sigma.py:1597–1649` has no finite/nonnegative row check; `:354–356` treats values not satisfying r>0 as unchanged bulk conductance. This is not evidence that the valid planner normally emits NaN.

| family | normal σ S/cm | NaN or negative film σ S/cm | unconverged | residual of bypass |
|---|---:|---:|---|---:|
| RRM via direct generic solver | 0.003334457143882423 | 0.0037299595666211234 | False | 6.2089744354216986e-15 |
| ordinary CNC via direct generic solver | 0.0038116099134384756 | 0.004141925781633665 | False | 6.2335439758997235e-15 |

RRM wrapper rejects those same NaN/negative plans before solver assembly. The generic helper's accepted result and small solver residual do not certify valid film semantics.

## RIMP-06 closure and Q9

Recommend **closed for inspected core consumers**. Exact source lines: RRM plan separation `rint_rrm_reference.py:243–274`; `_GEOM_SUMMARY_KEYS` and row-derived summary `:279–307`. Standard scalar G/rface namespaces are now `rrm`, CNC comparisons are explicitly separate, uniform `rface_c=None`, carbon law=None with an explanatory status. This is intentionally a schema distinction, not backward compatibility for external consumers that blindly assume `remove_area` exists for all references.

| fixture | actual film/cut | standard film/cut | actual and standard G (S) | separately labeled CNC G (S) |
|---|---:|---:|---:|---|
| baseline A | 67 / 85 | 67 / 85 | 5.027420037705035e-6 | remove_area=renormalize=5.027420037705035e-6 |
| carbon half | 37 / 42 | 37 / 42 | 2.7535056597827278e-6 | remove_area=2.612935414333538e-6; renormalize=5.027420037705035e-6 |

Baseline `A_film_sum_um2=0.5027420037705037`; carbon half `0.2753505659782727`. `realized=[True]`, summary_source explicitly says rrm_rows. Returned solve record has exactly 67/85 and 37/42 `n_*_rows_used`. Old probe's key `CNC_summary_film_G_S_total` is merely its legacy variable label; its new value is correctly `{rrm: ...}`. Full new summary extraction separately verifies the CNC comparison namespace.

Generic consumer audit: `step3_sigma.py:2140–2172` consumes rows/realized and adds used row counts/current shares without indexing CNC-only summary keys. `iface_plan_film_G_S` at `:1660–1669` is row-derived. Runtime `phase_current_share` and `per_particle_current` work for baseline and carbon half; phase share sums `1.0000000000000002`, returned records serialize directly as JSON. In the inspected complete `scripts/*.py` set, no production consumer outside this module depends on `film_G_S_total.remove_area`, `rface_ohm_cm2.remove_area`, or treating `iface_carbon_cover` as always a string. Follow-up scan of all 57 verified `source/webapp` Python/JavaScript files found zero matches for `iface_contact_ledger|film_G_S_total|rface_ohm_cm2|iface_carbon_cover|rint_rrm_reference|rrm_plan|rrm_solve|iface_reference|cnc_comparison|summary_source`. This supports compatibility of the inspected core and webapp consumers, not unknown external software. Future external consumers should branch on `iface_reference`/`summary_source` or iterate the available named law entries; do not silently map `rrm` back to a CNC law.

Existing quantitative adoption/production HOLD is unchanged. No new must-fix finding was demonstrated in the assigned RIMP-04/06 closure scope; Q7 is a concretely reproduced known residual common-guard limitation.

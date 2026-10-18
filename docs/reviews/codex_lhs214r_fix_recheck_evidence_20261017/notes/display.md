# L214R display lane — independent recheck, 2026-10-17

Code pin `60ba39e224aff48a030dccfe750342f3bf9db61f`; base `6cb2569569ec74b7f5a96e0ef19494e872da5272`. Source and base are the parent's obtained snapshots. Read submitted request, `source/AGENTS.md`, and relevant `CLAUDE.md` work discipline and code→webapp contract (especially line 100 and lines 416 onward). No Git, production-code edits, new 214 execution, WSL, registration change, or resealing. All scripts and fixture outputs below this review's `probes/display*` and `evidence/display*`.

## Verdict

- **L214R-03 closes in the final UI scope.** Actual imports, final loader, and complete template show the rejected mode's ionic σ and FULL-derived values masked after split merge / four-column input. The ordinary current values are refreshed independently of rejected-mode masking.
- **WEB-09 principal stale-accepted-value counterexamples close, with one P3 residual:** if neither current derived metric exists, retained historical values can retain their old Δ. This is a missed edge of the explicitly stated Δ invariant, not a new numerical-release defect. Recommend numerical release nonblocking, but do not claim the whole WEB-09 Δ contract closed.
- **valid_zero → dash is acceptable in this presentation contract.** The adjacent status row explicitly says proven nonpercolation and the τ row says NOT_PERCOLATING. Dash does not silently turn nonpercolation into numerical failure, and FULL ratios are undefined rather than zero. No new reason code or numerical target is introduced.
- **K1–K4 reproduce as disclosed, without a new accepting publication path in this lane.** K1 wording should include actual grade score/composite participation, not merely a displayed infinity. These are preexisting on base too. They need separate bounded follow-up, not another reopening of L214R-01–11's numerical closure solely on the present evidence.

## Evidence and reproducibility

`probes/display_rerun.py` compiles the bytes of the prior independent `../lhs214_fix_reverify_20261015/probes/l214_display.py` unchanged, with only `__file__` relocated so its existing HERE/source/evidence convention points at this review. Exact original bytes are stored self-contained in `probes/display_original.py.b64` (preserves CRLF); original SHA256 is asserted as `a8815414b3ebf282ad05a987048df9c88255ab03fd541be632b8c4b019020db2`. Provenance is in `evidence/display_adapter.json`. No function is mocked or extracted. Full import location appears in each JSON. The producer harness is reused, not the submitted display assertions.

Use the pinned executable `C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B` and `probes/display_run_command.py`, which records exact command, exit code, runtime, stdout/stderr under `evidence/display_<tag>*`. It sets both supplied dependency folders in PYTHONPATH, all numerical thread variables to 1, TMP/TEMP/TMPDIR to review/tmp, and bytecode off.

From the outer workspace, after that executable prefix:

```text
lhs214r_fix_recheck_20261017/probes/display_run_command.py independent probes/display_rerun.py --tree source --producers
lhs214r_fix_recheck_20261017/probes/display_run_command.py independent_base probes/display_rerun.py --tree base --producers
lhs214r_fix_recheck_20261017/probes/display_run_command.py l214r03 source/webapp/test_l214r03_display.py
lhs214r_fix_recheck_20261017/probes/display_run_command.py web09 source/webapp/test_web09_accepted_refresh.py
lhs214r_fix_recheck_20261017/probes/display_run_command.py provenance source/webapp/test_pipeline_provenance.py
lhs214r_fix_recheck_20261017/probes/display_run_command.py tau_grade source/webapp/test_tau_grade_unify.py
lhs214r_fix_recheck_20261017/probes/display_run_command.py fresh probes/display_fresh.py source
lhs214r_fix_recheck_20261017/probes/display_run_command.py fresh_base probes/display_fresh.py base
lhs214r_fix_recheck_20261017/probes/display_run_command.py summary probes/display_summarize.py
```

| Execution | Independently observed result |
|---|---|
| Unchanged old probe, source | 68 cases, zero exceptions; four producer states done |
| Unchanged old probe, base | 68 cases, zero exceptions; four producer states done |
| Submitted L214R-03 test | 14/14 PASS |
| Submitted WEB-09 test | 16/16 PASS |
| Existing provenance regression | 284/284 PASS |
| Existing τ/grade regression | 20 PASS, 0 FAIL |
| Fresh independent probe, each tree | 21 actual loader + Flask GET cases, zero exceptions |

The 68 original cases are 52 synthetic metrics cases using Flask GET `/single/<id>`, plus 16 small producer cases using actual loader then full `single.html` render; the latter are not described as GET. The fresh 21 all use actual loader and Flask GET. All fixture CSV files remain byte-identical across reading/rendering; all four independent producer fixtures preserve the preexisting contact CSV across publication.

`evidence/display_summary.json` records 55 changed and 13 unchanged rendered outputs, independently matching the request's change accounting. A separate output-derived oracle checks 233 ionic/derived displayed rows across 68 cases: no unaccepted-mode mask leak, no Δ when either mode unaccepted, and all displayed accepted ionic σ cells equal current metrics rounded to four decimals. The 68 count alone is not asserted as 68 independent property passes.

The fresh probe uses different current values (H=.2, P=.8, R=3/.75) and stale CSV values (H=17, P=19, R=31/37) to prevent accidental equality. All four layouts produce ionic .2/.8/+300.0% on source; base retains 17 in two-column, 17/19 in split and four-column. This independently distinguishes the WEB-09 fix from mere masking.

## Main counterexample closure

Source code final chain is `webapp/app.py:7530` onward: transform → injections → normalize → paper labels → final electronic/thermal suppression. Within normalize, Pass G invokes refresh then mask at `app.py:2588–2592`, after merging and sorting. State acceptance is `app.py:712–718`; refresh is `:783–812`; masking is `:815–833`.

Actual small producer + adversarial preexisting CSV outputs (`evidence/display_source.json`, JSON path cases.<name>.rendered_rows):

| Case | Exact ionic row H / P / Δ | Other relevant result |
|---|---|---|
| producer_ml_physics_split | `2.3861 / — (모형 한계 · full_over_conduction — FULL q > 1.5 출력 상한 · 수치 인증 통과 · 값 미제공) / —` | R=4.9×/same reason/—; Plastic amplification=—/—/— |
| producer_ml_hertz_csv | both cells same model-limit reason / Δ — | no old 0.6 or 2.0× resurrected |
| producer_ml_el_fourcol | `1.2016 / 2.0783 / +73.0%` | R=9.8×/5.7×/−42.2%; Plastic amplification=1.73×/1.73×/0% |
| producer_nonthrough_csv | `— / — / —` | state `비관통 (관통 경로 없음)` both; τ `NOT_PERCOLATING — 비관통 (관통 경로 없음) · 과학적 HOLD` both |

These are contract fixtures, not evidence that a historical production case actually carried the injected stale CSV numbers. Model-limit fixtures deliberately use synthetic chains, not validation of a physical bed. Full model-limit reason text remains separate from nonpercolation (`app.py:985`, `:1009–1020`, `:1098–1100`). New tables can omit the ionic numeric section when Hertz is absent; existing state/τ reasons remain visible. That was disclosed and unchanged for these cases, not elevated into a fresh P2.

## L214RR-02 · P3 residual — WEB-09 retains Δ when neither cell is fresh

Location: `source/webapp/app.py:806–812`. A None reference row exits at 806–807. A present reference row with both cells blank creates `fresh=[]` at 808 and bypasses Δ assignment at 811. The subsequent mask only clears Δ if a **displayed** cell is blank (`:832–833`); retained historical numeric cells are not blank.

Explicit invariant, not reviewer invention: `source/webapp/test_web09_accepted_refresh.py:14–16` says Δ is present only when both cells are current and says retained old cells require dash. The test at `:250–256` covers **one** old/one fresh R_brug and expects dash; neither-old-cell-replaced is missing. `app.py:784–787` documents the same refresh ownership and legacy retention policy.

Fresh minimal category: legacy metrics have accepted finite σ H=.2/P=.8, no producer state keys, **no R_brug_over_full, no R_brug_over_full_physics, no sigma_ratio**. Keeping old derived values is the explicitly accepted fallback. Four-column input contains:

```text
R_brug (과대추정 배수)       31.0×  37.0×  +19.4%
Contact-free / Full        31.0×  37.0×  +19.4%
σ_brug / σ_ionic           41.0×  43.0×  +4.9%
```

Actual GET `/single/missing_both_derived_fourcol`, HTTP 200, full HTML (`evidence/display_fresh_source_missing_both_derived_fourcol.html`) still contains these exact paper-labeled rows:

```text
Bruggeman overestimation, R_brug = σ_Bruggeman / σ_ionic | 31.0× | 37.0× | +19.4%
σ_contact-free / σ_full — constriction overestimation | 31.0× | 37.0× | +19.4%
σ_Bruggeman / σ_ionic — EMT vs Network solver          | 41.0× | 43.0× | +4.9%
```

Expected under the stated rule: retained first two numbers, Δ `—` on all three. Two-column/split variants likewise leave CF/FULL `31.0×/31.0×/0%` and σ_Bruggeman/σ_ionic `41.0×/41.0×/0%`. Seven failed checks in `display_fresh_source.json` concern only this neither-fresh Δ invariant. The source fixes the main current σ row to .2/.8/+300.0%, so this is not absence of refresh generally.

Base and source produce identical affected derived rows (`display_summary.json.fresh_old_and_new_same_derived_rows` all true): **preexisting edge missed by the fix**, not a regression newly introduced by the patch. Priority P3 because this is a historical UI comparison; it does not bypass a publication/numeric gate or restore unaccepted σ. Small follow-up: determine Δ from freshness on every recognized row, including ref=None/fresh=[]; keep explicitly approved legacy value preservation. No production fix made.

## K1–K4 adjudication

**K1, existing finite-output gap:** `tau_flux.py:522–527` checks three inputs but not their product/quotient. Fresh direct calls reproduce `(inf,3.0)` for phi=.5/σ=1e−310 and inf for `tau2_value(1e308,3.0,1e−3)`. `grade_engine._tau_axis` returns inf (`grade_engine.py:810–811`); derived-value lookup bypasses the ordinary finite gate (`:1336–1337`); grading only excludes None (`:1481`) and scores the value (`:1494`). Actual `build_overall_grade` produces Hertz τ value inf, score **0, grade D**, and includes it among scored axes in the composite (`:1631–1635`). Full Flask rendering succeeds and contains the result. Both base and source agree. Therefore revise “웹앱 등급 표시값” to “τ display and grade score/composite/ranking consumers”; do not claim this is confined to typography. No counterexample here establishes corrupt f/tau publication after L214R-09. Recommended P3 known limitation for this numerical-release decision; fix before relying on grades of extreme/malformed historical metrics.

**K2, disclosed exception and fail-closed:** `se_material.py:245–250` calls float on 10**400. Direct tau2 getter raises OverflowError. Calling actual `network_stop_verdict` on an independently produced ml_el directory with only the candidate metrics temperature-provenance argument changed returns False, with `⑦ τ 인계 도우미 실패 (OverflowError: int too large to convert to float)` (plus projection mismatch). This verifies actual reader rejection, not accepted publication. Catch is `pipeline_service.py:1091–1093`. Same underlying failure exists on base. Nonblocking P3 diagnostic quality.

**K3, disclosed metadata inf:** Take archived `cases/lhs00_001/work/results/lhs00_001/network_conductivity_dual.json` directly from the immutable v1.2 tar, change both legacy records' sigma_grain_S_cm to 1e306 in memory. `ion_columns` emits ion_sigma0_mScm=inf and both NOT_PERCOLATING. Conversion is `tau_flux.py:1253`. With matching full_metrics σ₀/temperature copies, `network_sigma0_problem` still rejects because 1e306 differs from temperature convention .003. This avoids relying solely on a projection mismatch. The helper used by stop check ⑧ is `pipeline_service.py:1066–1069`; full stop publication was not separately replayed for this legacy mutation. Same result on base. Disclosed P3 metadata validation gap, no demonstrated publication acceptance.

**K4, disclosed validator exception:** `stage_e_missing_keys({'sigma_full_mScm_stage_e':10**400})` raises OverflowError, both base/source. The app's real verification wrapper returns False on any exception at `app.py:3967–3978`, without a reason line. This last wrapper conclusion is source inspection, not a separately injected Stage-E subprocess trial; provenance regression 284/284 remains green. Nonblocking P3 diagnostics, no evidence of false successful Stage E.

## Limits of the no-impact claim

The independent 55/13 final-screen accounting corroborates the submitted rerun and closes the prior gap in an A4 transform-only check. It is stronger than A4 W for final UI, and still fixture-specific. Ordinary unchanged cases include normal_new/normal_csv/normal_split; normal_fourcol changes because stale Physics .6 now becomes current .9. The tests do not prove every historical layout or every numeric input unaffected. The new P3 counterexample shows why “all Δ semantics closed” would be too strong. No code in this lane changed solver results or registration scope.

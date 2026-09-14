# R11 publication/schema adversarial subreview

## Verdict

**NO-GO.** Core count: **P1 6, P2 3**, plus one promotion gap adjacent to (but narrower than) the R11-declared open export contract.

Target: `work/harness-r11-target-wsl/bms-balancing` at `2add074cf0c3ebfaa02b22d2311dd4330f0879b0`; executable code is unchanged from `665c87e`. Final WSL `git status --short -- bms-balancing` was empty. This reviewer never wrote target bytes; all fixtures were temporary and all persistent reviewer files are under `outputs/`.

Named closure rerun:

```text
PYTHONPATH=/tmp/r11-pydeps-publish PYTHONDONTWRITEBYTECODE=1 \
python3 -m pytest tests/test_r10_codex.py \
  -k 'd10_02 or d10_03 or d10_04 or d10_05 or d10_06 or d10_07 or d10_08 or d10_09 or d10_10 or d10_11' \
  -q -p no:cacheprovider

..........  10 passed, 6 deselected in 4.59s
```

The named regressions are green, but the following new executable paths bypass them.

## New findings

### P1-1 — Matrix/profile completeness is still relative to caller-selected work, so reduced runs publish canonical

Locations: `bms_balancing/verify.py:1445`, `:1449`, `:1507-1508`, `:1581-1586`; profile equivalents `:1612`, `:1685-1689`, `:1725-1730`.

State/command: the repro invokes the real `cmd_matrix` with `only_source=True`, `only_wdqdv=True` and all selected fits succeeding, then the real `cmd_profile` with `grid=1`. Scientific functions are deterministic stubs; publication and status logic are production code.

Observed:

```json
{
  "matrix": {"rc": 0, "canonical_exists": true, "rows": 8, "authority_rows": 32},
  "profile": {"rc": 0, "canonical_exists": true, "rows": 1,
              "gamma_roster": {"requested": 1, "succeeded": 1, "missing": []}}
}
```

`--only-source`/`--only-wdqdv` first shrink `sources`/`weights`; `complete` then means only “all filtered work succeeded.” Likewise `--grid` defines the profile authority itself. Both replace the same canonical filename. R10 P1-3/P1-4 only distinguish failures inside the caller-selected roster.

Minimal fix: define canonical matrix and profile authority rosters independently of diagnostic flags (including exact gamma values/count and profile-scale policy). Any invocation that differs from authority must be typed `subset`, return 3, and publish only under `partial/`. Persist the authority/requested/succeeded/missing roster in the verified unit and validate its semantics, not merely non-emptiness.

### P1-2 — `--schema-only` emits a promotion certificate with no baseline or comparison

Locations: `scripts/check_u14.py:211-212`, `:368`, `:479-490`.

State/command: one valid signed candidate, then `python3 scripts/check_u14.py --new <candidate> --schema-only`.

Observed: rc 0 and `PROMOTION {"promotion_eligible": true, "old": null, "roster":{"old":0,"new":1,"compared":0}, ...}`.

The mode sets `old=None`; `check()` skips pairing, environment, controls and numbers, then `main()` defines eligibility solely as `rc == 0`. A second case removed `state`, `half_cell_source`, `si_source`, `starts`, `seed`, `argv`, and `roster` and used `env={}`; it still returned the same promotion certificate.

Minimal fix: schema-only must unconditionally set `promotion_eligible:false` (a distinct non-promotion rc is preferable), include `baseline_absent`/`schema_only` in `blocked_by`, and still run standalone exact meta-schema checks for required controls, canonical env shape, argv and roster.

### P1-3 — Distinct directory names can still be the same candidate/baseline evidence via per-file aliases

Locations: `scripts/check_u14.py:88-95`, `:213-217`, `:381-384`.

State/command: create distinct `old/` and `new/` directories, hardlink candidate data to baseline data and candidate meta to baseline meta, then run a normal full comparison.

Observed: `directories_samefile=false`, `artifacts_samefile=true`, `metas_samefile=true`, but rc 0 and `promotion_eligible:true`.

The R10 P1-8 guard tests only the directory objects. An overwrite through either hardlink would overwrite both “independent” sides before comparison.

Minimal fix: after resolving every pair, reject if either data files or sidecars are `samefile`; reject symlink/hardlink aliases or materialize one side from an immutable revision into owned regular files before reading. Recheck identity at the snapshot boundary.

### P1-4 — Non-finite scientific values are valid schema and can be promoted as equal

Locations: `bms_balancing/schema.py:193-197`, `:211-219`; `scripts/check_u14.py:156-162`.

State/command: two independently signed matrix units with `obj=inf`, and two independently signed degeneracy units with JSON `best_obj=Infinity`, followed by normal full comparisons.

Observed: both runs report zero content problems, zero numeric differences, rc 0, and `promotion_eligible:true`.

CSV validation calls only `float()`, which accepts `nan`/`inf`. Degeneracy has no typed numeric validation at all. The comparator treats positive infinity as equal to positive infinity. Python's permissive JSON parser also accepts the non-standard `Infinity` token.

Minimal fix: require `math.isfinite()` for every scalar/array scientific number, validate shapes and types recursively for degeneracy, and parse/emit strict JSON with `NaN`/`Infinity` rejected. Apply the same finite predicate in producers before publication and in the comparison path.

### P1-5 — The production `ne_shape` wrapper prints typed status but does not enforce it

Locations: `scripts/run_states.sh:215-236`; outer status conversion `:297-305`, `:307-317`.

State/command: a directory contains only `partial/ne_shape_GITT_Li.csv` with meta `{"status":"partial"}`; a producer shim returns 0 without publishing canonical; invoke the real sourced `shape_step`.

Observed:

```text
ne_shape: **complete** (meta status partial) →
SHAPE_STEP_RC=0
```

`shape_step` branches only on process rc and merely interpolates meta status into text. It neither requires `rc↔status` consistency nor binds the selected artifact to this invocation. It also searches arbitrary first/stale artifacts. Separately, the outer wrapper explicitly consumes a genuine rc 3 without incrementing `fail`, so it can finish with “전부 통과” and exit 0 when `ne_shape` is partial.

Minimal fix: select the exact expected artifact, bind it to this invocation/run id, require the exact mapping `(0,complete/canonical)`, `(1,none/partial namespace)`, `(3,partial|subset/partial namespace)`, and fail closed on any mismatch. Preserve rc 3 (or another non-success overall status) through `run_states.sh`; never print all-pass for partial.

### P1-6 — Promotion ignores adverse provenance/control values and contradictory artifact environment

Locations: `scripts/check_u14.py:39-40`, `:200-212`, `:223-229`, `:479-489`.

Normal full-comparison counterexamples all returned rc 0 and `promotion_eligible:true`:

- candidate meta has `git_state_changed_during_run=true` and `git_commit_at_start="attacker-commit"`;
- candidate degeneracy body says every environment axis is `alien`, while candidate sidecar env matches baseline;
- candidate sidecar omits `argv` and `roster` entirely.

`META_KEYS` checks only presence for a small subset; it never requires the changed-during-run flag to be false or start commit to match policy. Environment comparison consults only the independently editable sidecar and never requires body/meta consistency. `argv` and `roster` are not meta requirements or controls.

Minimal fix: define one exact sidecar schema per artifact kind; reject unknown/missing fields; require stable-run flags to have safe values and code commit to match the expected commit; require body/meta environment equality before baseline comparison; validate argv as an exact vector consistent with kind, output, controls and roster.

### P2-1 — Profile stdout mode turns a typed partial result back into rc 0

Locations: `bms_balancing/verify.py:1689`, `:1725-1742`.

State/command: `grid=2`, one gamma succeeds and one fails, `out=None`.

Observed: summary says `status:"partial"`, roster is requested 2 / succeeded 1 / missing `[0.5]`, but `cmd_profile()` returns 0. The typed exit is returned only inside `if args.out and rows`; stdout mode falls through to unconditional `return 0`.

Minimal fix: determine semantic rc solely from status and return it after optional sink handling; sink selection must not change validity.

### P2-2 — Exact receipt roles are implemented as a set, so duplicate semantic roles pass

Locations: `bms_balancing/schema.py:58-69`, `:83-86`, `:144-163`.

State: one receipt contains both a top-level dotted `literature.gr` leaf and nested `literature: {gr: ...}`. Flattening yields `literature.gr` twice with different hashes.

Observed: flattened roles are `full_cell, half_cell, literature.gr, literature.gr, literature.si`; `validate_receipt()` returns no problems. The digest binds both entries but does not resolve which leaf is authoritative.

Minimal fix: reject duplicate flattened role names before set conversion and require one canonical receipt tree/leaf schema with no unknown nested members.

### P2-3 — Profile completeness seal is only a non-empty string

Locations: `bms_balancing/schema.py:18-24`, `:167-208`.

State: a fully valid profile row has `gamma_roster="not-json"`.

Observed: `check_rows("profile", ...)` returns no problems.

Minimal fix: parse and exact-validate the roster; require identical roster in every row, unique finite gamma values, `requested == succeeded + len(missing)`, row count/key set equal to succeeded values, and the canonical authority for promotion.

## R11-declared open issues versus new findings

Not counted as new: path omission from the receipt digest, the code-side `HALF_CELL_ABSENT` policy question, unsigned subset manifests, string `(root,state,si)` identity, U16/U17/U18 measurements, and the build-wide shared export contract listed in R11 §5.

One adjacent result is preserved in the JSON for adjudication: old and new can contain different, individually valid role-keyed input hashes and still promote, because `ROW_SKIP`/`JSON_NUM` omit input identity comparison (`schema.py:51-52`, `check_u14.py:44-48`, `:230-258`). This is not the declared **path** question. It is also narrower than the build-wide shared snapshot contract: the candidate/baseline gate itself does not establish that the compared computation consumed the same bytes. If R11 intends that omission to be covered by the open export-contract item, treat it as declared-open rather than incrementing the new P1 count; otherwise it is an additional P1.

## Artifacts

- `outputs/r11_publish_schema_repros.py`
- `outputs/r11_publish_schema_results.json`

Repro command:

```text
cd <workspace>
PYTHONPATH=/tmp/r11-pydeps-publish PYTHONDONTWRITEBYTECODE=1 \
python3 outputs/r11_publish_schema_repros.py
```

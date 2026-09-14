# R13 scientific roster and schema review

Target: `work/harness-r13-target-wsl/bms-balancing`, requested HEAD `94add7b5d48ad5d19448d562a0909b15ce4dc056`, code baseline `c7217c04f939889e88b915575fce6997005072aa`.

Scope: C04, C05, C06, C14; ordinary scientific CSV/JSON contracts and producer-to-consumer compatibility. Read `reviews/R13_REQUEST.md` completely. No target files were edited. No numerical solver, original workbook, evidence replay, import-escape, injection, or security-boundary test was run. The shape writer itself was invoked with synthetic finite measurements and all three declared GITT states; the scientific calculations were not executed.

Evidence: `outputs/r13_roster_schema_checks.py`; generated inputs, stdout/stderr and machine-readable results in `outputs/r13_roster_schema_results/`, particularly `results.json`. Execution used WSL Ubuntu `/home/yonghoon71/ddvenv/bin/python -B`, external preinstalled dependencies, and disabled bytecode writes. The script completed successfully. Three complete controls passed; eleven invalid-data cases also passed; the fresh shape writer's output was rejected.

Control validity: `control_profile_complete` uses the actual 21 points over [0, 0.5]; `control_matrix_complete` uses all 32 state-100 combinations of the two declared half-cell sources, eight declared Si sources and weights 0/1; `control_degeneracy` uses finite numeric values, five-element parameter vectors and nonempty mode-statistics records. All three receive rc 0/promotion true and **zero** unit, schema, content, input, environment and control blockers. Every sidecar has the real data SHA-256 and `S.body_roster` result, and each compared side has a different run ID. The receipt payloads are structurally valid and digest-consistent synthetic role identities. They are uniform across rows by design here and do not test C01's row-dependent receipt behavior.

For the repeated-invalid-data comparisons below, both synthetic runs deliberately contain the same scientific defect and have distinct run IDs, valid receipts and matching file checksums. These establish that U14 cannot validate a repeated incomplete or malformed result; they do **not** establish that changing a correct full baseline into a smaller candidate avoids U14's row/number comparison. The boolean-objective case additionally starts from a numeric baseline and changes only the candidate type.

## R13-S01 — P1 — C04 still accepts the wrong scientific gamma grid

Location: `bms_balancing/schema.py:376-384`, especially the post-count check at line 378. Producer contract: `bms_balancing/verify.py:1651` generates 21 points from `LB5[4]` to `UB5[4]`; `bms_balancing/model.py:286-287` fixes these endpoints to 0 and 0.5.

`check_gamma_roster` verifies count arithmetic, body length, requested versus authority, and disjointness between body and missing entries. It does not require a complete canonical result to have an empty missing list, make that list unique, or match the actual canonical point set.

Executed cases all return `S.check_rows(...) == []`, U14 rc 0, `promotion_eligible: true`, and zero blockers:

| Case | Body and declared roster |
|---|---|
| `profile_wrong_grid` | 21 unique points from 0 to 0.4, step 0.02; authority/requested/succeeded 21, missing empty |
| `profile_one_gamma_missing` | Correct grid except gamma 0.5: 20 rows; authority/requested 21, succeeded 20, missing `[0.5]` |
| `profile_twenty_duplicate_missing` | Only gamma 0: one row; authority/requested 21, succeeded 1, missing `[0.5]` repeated 20 times |

The first case is a different scientific experiment despite the correct row count and a claim of no missing points; it is the strongest membership counterexample. The second is an honest partial-result declaration of exactly the kind `cmd_profile` places in `partial/`. Repeating either can certify an incomplete or narrower sensitivity analysis as canonical. The partial examples support the consumer-contract mismatch and overlap R13 §5's explicitly open partial-lifetime axis; they are **not separately counted new findings**.

Fixture gap: `tests/test_r12_selfreview.py:317-319` calls points `i/(n-1)` its good full-grid control, covering 0 to **1.0**, whereas the actual legal gamma box ends at **0.5**. The regression therefore labels the missing invariant's counterexample as valid.

Repair: define the full canonical gamma values in a shared contract, validate body membership against them, and require complete coverage with no missing values for canonical promotion. A separate diagnostic contract can describe partial coverage; duplicate or unknown missing values should never count as distinct failed points.

## R13-S02 — P1 — C05 trusts its own matrix authority and scientific membership

Location: `bms_balancing/schema.py:332-339`. The independent authority is computed only in `bms_balancing/verify.py:1457-1464`: every declared half-cell source, every `D.SI_SOURCES` member, and weights exactly `(0.0, 1.0)`, excluding only the state-specific declared absence. `bms_balancing/data.py:25-38` declares the two sources GITT/step_005C, eight Si sources, and the sole known absence GITT/300_0147. Therefore state 100 has exactly 32 canonical combinations and 300_0147 has 16.

`check_combo_roster` accepts any matching nonboolean integer authority/requested and never derives the expected combinations from state and the declared source/Si/weight roster. It also accepts nonempty `missing_input` or `failed` lists when their lengths balance the arithmetic. It does not compare missing/failed/absent identities to body keys or canonical keys.

Executed cases all return an empty schema problem list, U14 rc 0, promotion true, and zero blockers:

| Case | Body and declared roster |
|---|---|
| `matrix_self_declared_one_row_authority` | State 100, only GITT/Li/weight 0; authority=requested=succeeded=1; all lists empty. State 100's real authority is 32. |
| `matrix_one_input_missing` | 31 legitimate body combinations; authority/requested 32, succeeded 31, one missing-input key |
| `matrix_wrong_member` | 32 unique body combinations but one Si name is `Li2`, outside the eight declared sources; authority/requested/succeeded 32 |

The first case reproduces the small-population certification that C05 says it closes. The third shows that fixing the authority count alone would still leave the wrong scientific roster accepted. These are the novel exact-authority/membership defects. The second also contradicts producer status: `verify.py:1534` requires **no** missing inputs or failures for complete output; it is supporting evidence overlapping the acknowledged partial-lifetime axis, not an additional finding.

Fixture gap: the C05 regression explicitly accepts a two-row population with `authority: 2` as its good canonical example (`tests/test_r12_selfreview.py:349-351`), and other new helpers seal authority to whatever row count they receive. They cannot detect incorrect authority or membership.

Repair: share the state-dependent authority with consumers; pass state/context into matrix validation; validate the exact combination set and known absences, and require zero failed/missing combinations for canonical promotion. Do not infer authority from produced rows or a caller's count.

## R13-S03 — P2 — C06 checks finiteness but still has no scientific JSON type/shape contract

Location: `bms_balancing/schema.py:388-415` (`bool` accepted at line 390, failed numeric-string conversion accepted at line 405, required values checked only against `None`/empty string at line 412); numeric comparison in `scripts/check_u14.py:282-287`.

The new recursive check catches parseable nonfinite strings, but it intentionally accepts every nonnumeric string as a possible label without knowing the field. It also accepts booleans and empty containers. Consequently a required scalar objective, parameter vector, or statistics object can contain no usable scientific result while the schema says it is complete.

Executed cases with `best_obj: "not-computed"`, `best_p: []`, `LLI_percent: {}`, or `best_obj: true` each receive empty schema problems and promotion true when repeated. More directly, changing a correct baseline's `best_obj: 1.0` to candidate `best_obj: true` also yields rc 0/promotion true: the schema allows the boolean and the numeric comparator coerces it to 1.

C06's `"1e999"`/`"Infinity"` fix is real, but the original “scientific values must be finite numeric data” requirement remains only partially implemented. The C06 regression's text mentions `"not-a-number"`, yet its rejection loop does not test that value.

Repair: validate by field, keeping labels separate from numeric scalars; reject booleans and nonnumeric text in scientific numeric slots; require five-element parameter vectors and the required nested statistics fields. Apply finiteness after successful type and shape validation.

## R13-S04 — P1 workflow blocker — C14 includes shape output but has no matching current producer schema

This extends an **acknowledged open** issue in R13 §4/Q6 rather than claiming it was previously closed.

Location: `scripts/check_u14.py:110-111` maps every CSV other than `matrix_*` to `profile`. The real shape writer is `scripts/ne_shape.py:166`, its 20-column header at line 188, and its sidecar at lines 211-234. `schema.body_roster` uses the same fallback classification.

Invoked current `ne_shape._write_csv` with finite synthetic measurements for every declared GITT state (100, 200, 300_0009), complete pairing, and status complete. U14 `--schema-only` returns rc 2 with:

`{schema: 27, provenance_cols: 3, content: 1, provenance: 1, baseline_absent: 1}`

It reports the writer's 19 shape-specific columns as unknown profile columns, requires nonexistent profile fields, and also rejects missing current sidecar fields (`env`, start provenance, etc.). The artifact unit itself passes (`unit: 0`). The production `shape_step` checks its unit/status but does not convert or complete this metadata schema.

Answer to Q6: **regeneration alone cannot fix the shape defect**; current producer output still fails. Introduce a dedicated shape schema, state row key, receipt/pairing/coverage contract, and appropriate sidecar requirements, then adapt the writer and perform an actual regeneration. Simply adding 19 permitted columns to `PROFILE_ROW` would mix unrelated artifact contracts and retain the wrong row key and provenance expectations.

## Q1 interpretation across the assigned axes

C04's count-to-body improvement is real, but it stops before tying the **identities** of the scientific points to the producer's canonical grid. C05 has the same pattern for combinations: the consumer compares counts while its authority remains supplied by the artifact. C14 does fix the earlier omission of `ne_shape_*.csv` from the filename roster, but stops before a compatible kind/schema/row-key/metadata contract. These are the requested “half-closed” pattern at different layers.

C01 was assigned to another reviewer. The present checks do not assess row-dependent input identity and should not be cited as evidence that C01 is closed or reopened. The positive controls establish the unit/receipt/checker path needed for these scientific-schema cases; uniform receipts would be an unsuitable C01 control, as R13 §6 itself explains.

## C14/Q4 scope note

`ARTIFACT_SUFFIXES = {".csv", ".json"}` at `scripts/check_u14.py:54,133` remains a suffix allowlist, despite comments describing the implementation as a denylist. New `.tsv`/other artifact formats would still be ignored. No current producer for such a format was established in this review, so this is a design answer, not an additional demonstrated current regression. An explicit artifact-kind registry or dataset manifest is clearer; any unknown scientific artifact declared by that manifest should be reported rather than silently omitted. Recognition must choose a genuine artifact schema, not the current “all other CSV is profile” fallback.

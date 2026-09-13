# R13 evidence contract — static review

Review target supplied by parent: `94add7b5d48ad5d19448d562a0909b15ce4dc056`, under `work/harness-r13-target-wsl/bms-balancing`. Read `reviews/R13_REQUEST.md` completely. This review inspected source, parsed existing JSON, and independently hashed archived package files. It did **not** execute replay runners, archived evidence scripts, injected inputs, or security reproduction workflows. Findings marked static are code-path conclusions, not reproduced attacks. Windows Git could not read this checkout's metadata (`not a git repository: (NULL)`); fresh commit identity must come from the parent's WSL verification.

## Findings

### P1 — C08 still places the isolation boundary after ordinary imports

**Static evidence:** R7 imports its dependencies at `reviews/r7_repros/replay_codex_r7.py:23`, then conditionally replaces the process at lines 37–45. The identical ordering exists at R9 lines 20/34–42, R10 lines 19/33–41, and R11 lines 16/24–32. Therefore the code cannot support its claim that the new process boundary precedes **all** repository-influenced imports. The restart predicate also checks only `safe_path`, not the complete intended isolation state. Importing the module and subsequently calling `main()` does not enforce this restart predicate because of its `__main__` condition.

The regression named `test_f13_runners_isolate_sys_path_before_any_import` only searches the text before `import evidence_gate` for two tokens (`tests/test_r12_selfreview.py:412–415`). It does not establish import ordering or the runtime state required by evidence production. This is the same “half-closed” pattern the request asks about.

**Q3:** Process replacement is a reasonable implementation component, but it is not a sufficient trust boundary at this location. Start the attesting process in its required isolated configuration before importing application dependencies; keep testable helper functions separate from the executable bootstrap; require the full bootstrap invariants at the evidence-producing entry point independently of the module name. A trusted launcher and independently checked source identity should own this boundary. No claim of a newly demonstrated false certificate is made here.

### P1 — Aggregate `closed` and rc still certify unresolved observations as closed

**Observed stored evidence:** R7, R10, and R11 JSON each has `closed: true`, `evidence_eligible: true`, and an adjacent rc file containing `0`, despite retaining premise-changed or environment-limited records. R10 and R11 additionally state `rc_reason: "모든 case 가 닫혔다"` (“all cases closed”). This contradicts R13 §1 and §5, and the evidence README, which say those categories were not counted as closed.

**Static cause:** R7 allows `전제 변경` in its aggregate closure set (`replay_codex_r7.py:263–268`). R10 excludes `전제 변경` and `우리 코드 밖` from unresolved (`replay_codex_r10.py:301–307`). R11 excludes `환경상 불가` and `전제 변경` (`replay_codex_r11.py:420–423`). The C19 return-code change correctly checks evidence eligibility, but does not correct these closure semantics.

Retain separate fields for execution validity, coverage completeness, closure, and waived/inapplicable status. Compute closure from the expected individual case roster and successful case-specific evidence. An environment limitation or changed premise needs explicit incomplete/replacement status and cannot, by itself, establish closure. If rc 0 means only that the reporting job completed, remove the contradictory “all cases closed” claim and expose a distinct decision status to consumers.

### P2 — The promised exception fingerprints are incomplete

**Static evidence:** `replay_codex_r10.py:301–303` changes any `오류` for `u18:shape_duplicates` into `전제 변경`, with no check of exception type, location, or cause. This contradicts the statement that each of the four premise changes is fingerprint-sealed. The stored instance is a `TypeError`, but its observed type is not enforced by this classifier.

`replay_codex_r11.py:339–341` identifies `data:shape_wrapper` as environment-limited from any error starting with `FileNotFoundError`; it does not bind the classification to the specifically unavailable dependency documented by the request. The stored record does identify that dependency, but unrelated missing fixture/output errors are not distinguished by the branch. The explanatory text is also indexed as a tuple although its source value is a string, leaving the observed `세부` value as just `"원"`. `_record` marks both environment-limited and grouped premise failures as reached (`도달: true`), even when their individual case assertions did not run.

Require structured, case-specific causes and explicit reachability, preserve the complete explanation, and leave unexpected failures as errors. Keep this separate from whether an adapted replacement test closes the intended invariant.

### P2 — R11's 35 slots are not 35 individual cases

**Observed stored evidence:** R11 contains 35 records: root 6, data 7, checker 12, publication 2, evidence 8. Of these, 32 have status `반례 소멸`.

**Static roster:** `publication_repros()` returns three separate cases (`reviews/r11_repros/codex/r11_publish_schema_repros.py:308–328`); the runner also invokes `publish:shape_step`. On the stored path, a group exception collapses all three publication cases into one `publish:*` record (`replay_codex_r11.py:366–381`). The full individual roster is therefore **37**: root 6 + data 7 + checker 12 + publication 4 + evidence 8. The stored run establishes 32 successful closure records, one changed-premise root case, three individually unresolved publication cases after a group interruption, and one environment-limited case. Two later publication cases were not run.

The request does call these “slots,” so 35 is a correct JSON record count. It must not be used as a denominator for independent case closure. More precisely, the three publication leaf cases are individually unresolved after the group stops at its first matrix case; the two later profile cases were not executed and must not be assigned individually established premise-change verdicts. The R11 runner has no final expected-versus-observed case-set equality check. Preserve all expected leaf cases when a group stops early and report the group cause on each uncompleted case, together with any separately verified replacement coverage.

### P2 — C28's regression still does not verify typed `none` classification

**Static evidence:** `tests/test_r10_codex.py:583` says the `none` producer has no artifact, but lines 591–593 call the same helper that writes an artifact and sidecar at lines 568–579. Production `ne_shape.py:443–447` does write an artifact for `none` when `--write` is supplied, so the comment is wrong and the artifact-bearing fixture is consistent with that production path. The `none` assertion nevertheless checks only `STEP_RC=1`.

The changed test cannot distinguish a normal typed `none` outcome from a parsing/contract failure that also returns 1. The intended label remains unchecked, and the fixture contradicts its own comment. Correct the documented representation and assert the classified outcome, absence of a contradiction diagnostic, and rc. This is a static regression coverage issue, not a claim that the normal production `none` path currently fails. No helper was executed for this review.

### P3 — C31 removed the unused helper, but ordinary temporary ownership remains incomplete

**Static evidence:** Every runner still creates module-level `_PYC` with `mkdtemp` and has no corresponding cleanup. R7/R9/R10 additionally call `gate.isolate_bytecode()`, which creates another temporary root without registering cleanup (`evidence_gate.py:120–130`). `materialize()` creates a parent temporary directory at line 93 but its cleanup removes only the nested worktree at lines 98–100. R11's new `_child_pyc` at line 393 is likewise never removed.

This does not demonstrate the historical leak counts quoted by C31, but the ordinary completion path still lacks ownership for newly created roots. Scope temporary roots to the run and clean them in a reliable finalizer, honoring explicit retention. C35's relocation of the publication workspace outside the source tree is a useful fix for the specific tree-contamination issue.

## Passive evidence audit

These are new observations from files, not rerun scientific or security outcomes:

Reproducible subset: `outputs/r13_passive_evidence_audit.py --target <bms-balancing>` parses the five current stored replay reports and adjacent rc files and hashes the four package manifests using only standard-library file reads. Its completed stdout is saved in `outputs/r13_passive_evidence_results.json` (audit rc 0). That rc means the passive reads/parsing/hashing succeeded; it does not certify closure of the recorded replay cases. The wider 29-file archive parse check below was a separate passive PowerShell observation.

| Stored report | Requested/expected individual cases | JSON records | Extinct/closed status | Other statuses | Stored rc |
|---|---:|---:|---:|---|---:|
| R6 adapted | 6 | 6 | 6 `닫힘` | None; `mode: full` | 0 |
| R7 | 6 requested, exactly matching observed keys | 6 | 5 | 1 premise changed | 0 |
| R9 | 12 requested, exactly matching observed keys | 12 | 12 | None | 0 |
| R10 | 22 source-enumerated cases | 22 | 20 | 1 outside implementation, 1 premise changed | 0 |
| R11 | 37 source-enumerated individual cases | 35 | 32 | 2 grouped/individual premise records, 1 unavailable | 0 |

- All five JSON files under `reviews/r12_repros/replay_ours_after_selfreview` parsed successfully. All 29 JSON files directly inside `replay_ours_*` directories found under `reviews/` parsed successfully; no rc suffix remains in that sampled archive scope (C24).
- All manifest entries matched independently calculated SHA-256: R7 10/10, R9 11/11, R10 10/10, R11 13/13. Including each manifest itself, their directories have 11, 12, 11, and 14 files. The C27 distinction is now accurately documented.
- Stored R7/R9/R10/R11 evidence names head `c7217c04f939889e88b915575fce6997005072aa` and tree `ae9e484798051fa67e99aab76cbfd8450e68d139`; all four report instrument and package checks true. This is recorded identity, not my independent verification of the target checkout's commit.
- Stored R7/R9/R11 evidence includes a dirty source state caused by the untracked evidence directory. That is compatible with running a separately materialized snapshot; it does not establish source execution contamination. R10 records the dirty boolean but not its paths.
- Stored R11 `data:shape_reader` has `child_rc: 1` and extinct status. Its explicit expected reader-rejection predicate explains that path; it should not be portrayed as proof of an arbitrary child-failure false positive. It does limit any prose claim that all child reports require rc 0.
- C25's two before-evidence files without a full commit ID remain the root and publication reports. The evidence report contains full IDs in nested `head_after` fields. Preserving archive bytes while acknowledging incomplete identity is appropriate; archival status does not strengthen the evidence.

## Other requested closure checks

| Item | Static disposition |
|---|---|
| C07 | Both instrument and snapshot hashes use `--no-filters` (`evidence_gate.py:148,196`). This specific asymmetry is fixed. No filter reproduction performed. |
| C09 | The metadata/shape heredocs begin in isolated mode before their Python imports (`scripts/run_states.sh:58,226`). This addresses the specified interpreter startup path; it is not a certificate for every production import. |
| C10 | Catch-all LF policy precedes archived-package `-text` exception in `.gitattributes`. Actual archived bytes match their manifests. No fresh clone was performed here. |
| C19 | All four runners return 3 for `evidence_eligible: false` on their final decision path. Aggregate closure semantics remain the separate finding above. |
| C20/C26/C27 | Documented extinct namespace split is root 5/data 6/check 12/publish 1/evidence 8; R7 is 5+1; R11 archive is 13 signed files plus manifest. These counts match inspected stored files. |
| C21/C22/C23 | Checker docstring explains schema-only rc 0 vs no promotion. `blocked_by` splits ordinary schema and provenance columns. List truncation is centralized in `_show`; its normal positive-limit path announces omitted counts. A stale comment at `check_u14.py:704–705` still says incomparable inputs do not change rc, contrary the implementation. |
| C28 | Still incomplete; see finding. |
| C29 | Shape result takes the producer run ID from process-owned state (`scripts/ne_shape.py:453–457`), and wrapper's final unit check receives its own generated ID (`run_states.sh:269`). The earlier direct reread tautology is removed. |
| C30 | R11 isolates ordinary child caches and retains the explicit legacy exception (`replay_codex_r11.py:392–401`). R10 still removes the cache prefix for its entire evidence group (`replay_codex_r10.py:273–277`); the claimed general snapshot lifetime guarantee should remain limited. No cache/injection workflow executed. |
| C31 | Dead bootstrap helper removed; lifecycle cleanup remains incomplete as above. |
| C35 | Publication workspace is now a separate temporary directory (`replay_codex_r11.py:356–384`), removing the described self-reference from the target tree. No signal test performed. |

Evidence-sector verdict: **do not treat these stored aggregate closure flags as a complete closure certificate**. Package integrity and JSON validity improved, but bootstrap ordering, exception classification, case accounting, and conclusion semantics still require correction or explicit limitation.

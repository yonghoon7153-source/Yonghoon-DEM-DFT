# GATE70 E3 / E5 / E6 and proposed execution flow

Review target: `C:/Users/Administrator/Documents/Codex/g70_20260924`, HEAD `8568f782db3acbf00d872ce5527147258c00bec7`; requested code `f0dfaff3bea1e1caedcd7a34275e908284cc2d4f`, source digest `5e660a8c73d5663a`. All source references below are under `degradation-degeneracy/`. Read root CLAUDE.md and the complete GATE70 request. This subtask does not assess F50b or rerun the science.

## Conclusions for the parent review

1. E3 is an existing incomplete contract, not a new defect count. The old CAS transaction receipt checker exists, but the actual lifecycle consumer still derives `full_bundle` from a directory/count/index-hash declaration. It does not consume a typed CAS/archive/restore/validation/retention receipt. It can skip index member coverage when the index cannot be interpreted; the parser probe returned `None`. Finalization correctly retains `unvalidated` / `diagnostic`, so this is not proof that current code automatically grants scientifically validated status. A result label alone does not implement the requested canonical preservation contract; provisional raw calculation can remain explicitly pending.
2. E5 is **partially implemented**, not wholly unstarted as GATE70 table line 38 says. Content addressing, temporal seals, class capabilities, publication readback/durability, conflict rejection, and content-based lookup already exist. The remaining typed reader is demonstrably permissive: it accepted both a two-key canonical record and wrong-typed `sealed/evidence/recorded_at` plus a surplus key. This is evidence that exact typed consumption is open; it is not a demonstrated remote/adversarial authority bypass. Legacy compatibility must be specified rather than retroactively rewriting existing records.
3. E6 cannot be described solely as third-party verifiability for the proposed workflow. Tests can create production canonical authority, and session cleanup can remove unrelated canonical authority produced after its initial snapshot. The latter was reproduced using the exact cleanup function body against an owned fixture root. However, finishing all historical registry migration is not automatically necessary before a new isolated run: verifiable isolation or exclusive use of the operational registry can remove this concrete concurrency hazard while historical restoration/class changes remain separately scoped.
4. The E1–E8 list omits concrete execution-plan prerequisites. Literal `./run.sh` exits 1 with `--mode 필수`; default output is timestamped; `--mode all` performs no archive step and finalizes `preservation_pending`. The checked-in planned roster contains only eight retrospective/executed records and no `grid_fit_v4` prospective authorization. Closing E3/E5/E7 alone would not make the requested command execute or produce the claimed complete bundle.

## E3 evidence and minimum closure

| Code / request coordinate | Observation and consequence |
|---|---|
| `docs/22p_gap/GATE49_REQUEST.md:18` | Original scope explicitly says typed CAS/archive/restore/validation/retention receipt **consumption** is unstarted, with only intermediate state/tuple support present. |
| `tools/preserve.py:2979`, `:3050`, `:3096`, `:3245`, `:3262` | Existing CAS transaction machinery validates a closed `execution-receipt/v1`, planned envelope, backend/store, validation names, outputs, and manifest binding. Do not claim no receipt validation exists anywhere. |
| `tools/preserve.py:7311`, `:7380`, `:7396` | Lifecycle bundle evidence is five caller fields: `bundle_uri`, `bundle_files`, `payload_bytes`, `payload_index`, `payload_index_sha256`. |
| `tools/preserve.py:7464`, `:7469`, `:7474` | Consumer checks directory file count/bytes and index bytes hash. These are useful byte checks but not typed preservation/restore/retention proof. |
| `tools/preserve.py:7492`, `:7493`, `:7505`, `:7512` | Member set comparison occurs only if `_declared_index_members` returns a set. Invalid JSON, unknown shapes, and unreadable content return `None`; coverage is silently skipped. Isolated parser probe against plain non-JSON text returned `None`. The full Linux mount-dependent bundle verifier was not run here. |
| `tools/preserve.py:7774`, `:7780`, `:7955` | Finalize uses `_verify_declared_bundle`, then presence of all five fields selects `full_bundle`. It does not select state from the older typed receipt consumer. |
| `tools/preserve.py:7957`–`:7960` | Validation/inference remain `unvalidated` / `diagnostic`. Preserve this truthful behavior; do not overstate the observed failure as automatic current-validated/canonical inference. |
| `tools/preserve.py:7537` | Code itself acknowledges the mutable-directory verify→seal window and need for immutable content-addressed publication; this dependency also needs a defined claim boundary (coordinate with E1). |

Minimum closure: choose a versioned receipt contract with explicit performed/failed/unperformed states for archive, CAS/storage, restoration, validation, and retention; consume it in the lifecycle finalization/promotion path; bind leg/run/producer and content identities to the actual validated bundle. A missing or unsupported index format must not be treated as verified coverage. Test supported complete receipts, missing/extra/wrong-type nested fields, unsupported indexes, stale or foreign receipts, and partial work remaining pending. Do not require a new test-only cryptographic trust scheme without a threat-model reason, and do not let `check_receipt`'s existence stand in for integration.

## E5 evidence and minimum closure

| Code coordinate | Implemented or remaining behavior |
|---|---|
| `tools/preserve.py:4335`–`:4350` | Registry authority is alongside canonical ledger; lookup key is content identity, not current run path. |
| `tools/preserve.py:4638`–`:4655` | A seal supplies the manifest descriptor; legacy fallback hashes present manifests. |
| `tools/preserve.py:4763`, `:4788`, `:4793`, `:4811` | Publication computes content id, records seal presence, and uses a per-content lock. |
| `tools/preserve.py:4818`, `:4834`, `:4847` | Existing readback plus directory fsync; retain these guarantees. |
| `tools/preserve.py:4880`–`:4887` | Writer emits content id, class, evidence, recorded_at, sealed. |
| `tools/preserve.py:4950`–`:4974` | Reader checks single-link record, JSON dict, enum class, and matching content id only. No exact key set, typed evidence/time/sealed, or schema variant validation. |
| `tools/preserve.py:4995`–`:5010` | Both shared and local registries are consulted; opposite class is fail-closed. Moving to `local/` alone does not isolate authority from this reader. |
| `tools/preserve.py:5076`–`:5112` | Promotion looks up content id. Seal deletion protection depends on truthiness of `rec.get("sealed")`; absent/falsey malformed fields can be interpreted like legacy records if admitted to authority. |
| `tools/preserve.py:5238`, `:5267`, `:5283`, `:5386`–`:5391` | Initial class is determined by namespace once; issued capability binds publication, which seals then registers. This already addresses much of historical P0-8. |

Actual isolated read probe (exit 0):

```json
{"content_id":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","execution_class":"canonical"}
```

was returned as a valid record; so was:

```json
{"content_id":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","execution_class":"canonical","sealed":[],"evidence":17,"recorded_at":false,"surplus":{"accepted":true}}
```

The probe called the original `_read_exec_class_at` only on owned files, not on a forged operational registry. Downstream promotion was not invoked. Therefore report this as the remaining typed-consumer gap, with a concrete weak-field consequence in `resolve_execution_class`, not as a proven same-principal exploit or proof of incorrect scientific numbers.

Minimum closure: explicitly define closed typed record variants for production completion and authorized legacy classification; preserve existing content/seal/capability/durability guarantees; reject unknown or ill-typed shapes before class use; bind sealed completion to the corresponding seal identity; exercise copied/moved runs and full writer→reader→promotion paths. A pure relocation test is already insufficient and should not be the sole E5 acceptance test. Existing legacy records need a deliberate compatibility/migration contract; this review does not approve rewriting their class or restoring deleted records.

## E6 read-only dependency map

The promised `docs/22p_gap/registry_impact.md` does not exist at this HEAD (request line 39 promises it this round). This report provides observations, not an operational migration.

| Component | Dependency / mutation |
|---|---|
| `tools/preserve.py:4350`, `:4692`, `:4695` | Shared canonical records are `<ledger-parent>/_exec_class/*.json`; smoke records are `local/*.json`. Both locations remain reader inputs. |
| `src/grid.py:388`–`:389`, `src/fitting.py:1058`–`:1059` | Normal completed phases call `commit_run_outputs`. |
| `tools/preserve.py:5386`–`:5391` | Completion seals outputs and registers class under the capability's ledger, normally default production ledger. |
| `tools/preserve.py:5594` | Promotion consumes registry class via `resolve_execution_class(..., for_promotion=True)`; missing authority rejects output promotion. |
| `tools/make_results.py:1702`–`:1703` | Report path uses `assert_not_smoke_provenance`, which includes the content/class check. |
| `tools/archive_bundle.py:596`–`:599` | Archive producer entrypoint uses `assert_promotable`, also consuming that authority. |
| `tests/test_compare.py:940`–`:950` | `_complete_artifact` directly seals and registers a synthetic canonical artifact with no alternate ledger supplied; it reaches the production registry. |
| `tests/conftest.py:154`–`:188` | Autouse session fixture snapshots root `*.json` names in `_exec_class` and `_frozen_coords`, then unlinks every new name. It does not prove ownership, take registry content locks, or restore prior bytes. It is cleanup, not isolation. |

Read-only observed shared root records: **367**. Evidence-string groups: **174** `_complete_artifact` synthetic descriptions; **177** `leg=L phase=grid class=canonical` completion descriptions; **16** legacy/re-key descriptions. These labels are not a proof that the 177 came from real science, nor that every record is synthetic. Do not inherit the GATE70 claim of "real canonical" from label text alone.

Concrete interference schedule:

1. Pytest session A snapshots names in production `_exec_class`.
2. Independently executing legitimate run B publishes a previously absent canonical record.
3. Session A's teardown deletes B's record because its filename is not in A's initial snapshot.
4. Report/archive promotion reads the same registry and rejects B's otherwise complete output as unregistered.

The exact fixture body was compiled from `tests/conftest.py` with only its decorator removed and `ROOT` redirected to the owned scratch directory. Inserting a new canonical record after the snapshot yielded `before_teardown=true`, `after_teardown=false`, while an existing sentinel survived. No production registry record was written or deleted by that probe. This is an operational evidence-loss hazard, not merely independent-review incompleteness. Abrupt session termination also bypasses cleanup, leaving synthetic authority, as already documented in GATE65 Q5.

Minimum route for a new run: either inject isolated test authority through every in-process/subprocess entrypoint and prove the production registry unchanged, or use a dedicated controlled checkout/operational authority with no overlapping tests, cleanup, writers, or synchronization for the full critical window. Capture the initial and final registry bytes, validate all new records as belonging to that run, and preserve new authority before promotion. The requested "no commits during the run" rule alone does not prevent test cleanup. Smoke and later verification must have a defined authority destination, not implicit shared-root writes. Existing record restoration/class migration can remain separately authorized; a deferred migration label is acceptable only after this concrete run's authority integrity is independently satisfied.

## Missing execution-plan prerequisites

| Coordinate | Finding |
|---|---|
| `docs/22p_gap/GATE70_REQUEST.md:57` | Claims literal `./run.sh` will generate receipt, class registration, and archive bundle in one execution. |
| `run.sh:17`, `:213` | `MODE=""`; no mode rejects with exit 1. Re-executed through Git Bash with `/usr/bin:/bin` in PATH: `--mode 필수`, **exit 1**. No science launched. |
| `run.sh:60` | Default output is `results/run_<timestamp>`, not `results/grid_fit_v4`. |
| `run.sh:313`–`:321` | Finalize supplies digest/cohort/out only, explicitly prints `preservation_pending` and that bundle creation/verification is a separate step. |
| `run.sh:558`–`:565` | `all` calls grid, fit, finalize, score, report; it never invokes archive creation. |
| `docs/22p_gap/LEG_PRESERVATION.yaml:662`–`:734` | Eight planned-index entries are retrospective/executed. No requested new canonical leg exists. |
| `tools/preserve.py:5791`–`:5798`, `:5807`–`:5818`, `:7281` | Actual precheck requires a registered planned leg, active cohort, and current source identity. New prospective run spec and its own digest must match actual arguments. |

Minimum closure: publish the exact reviewed command(s), explicit config/axes/output/leg/cohort, prospective plan and run-spec identity on the final reviewed code, and explicit archive/receipt/verification/state-transition steps. This can initially be a runbook using existing interfaces; it need not be a new monolithic implementation. Validate parser/preflight without science, then test the complete integrated flow in an isolated small fixture. No provisional E1–E8 checkbox can substitute for this plan. Code changes for E3/E5 would also require a new final source identity and review of the actual replacement commit; they cannot retroactively make `f0dfaff3` implement those changes.

## Probe files, execution limits, and side effects

- `probe.py` and `fixtures/*` are owned scratch artifacts under this report directory. Source import used bundled Python with `-B` (no import cache writes). The original source and operational class/ledger files were not edited. The isolated cleanup probe deleted only its newly copied scratch sentinel, recoverable from `fixtures/minimal.json`; it preserved the existing sentinel.
- Native Windows lacks Linux mount information; the attempted original `precheck_leg_run` raised `BoundaryUnknown` for `/proc/self/mountinfo`. A subsequent direct `assert_planned_leg` attempt stopped at missing PyYAML; it did not demonstrate the missing-leg runtime rejection. Missing planned authorization is a complete ledger/code inspection finding, not a claimed Linux preflight execution.
- **Original-checkout directory side effect:** contrary to the precheck docstring, `claims_root_for_ledger` calls `_lifecycle_root`, whose lines 6392–6394 create the directory before checking mounts at line 6404. The attempted precheck left an empty `C:/Users/Administrator/Documents/Codex/g70_20260924/degradation-degeneracy/docs/22p_gap/_claims/`, observed CreationTime/LastWriteTime **2026-09-24 14:53:57 local**. No claim file, token, class record, or ledger mutation occurred. The directory was left in place and disclosed to the parent; no cleanup/restoration was attempted. Thus clean Git status is not a claim of zero filesystem writes.
- `wsl --list --quiet` was denied (`E_ACCESSDENIED`); no permission bypass attempted. No Linux kernel validation, full regression, science execution, COMSOL, registry restoration, class migration, commits, pushes, or external messages were performed.
- Initial Git Bash invocation lacked `dirname` in PATH and failed before argument dispatch; the corrected PATH invocation above is the evidence used for the exit-1 command finding.

See `probe_results.json` for the successful probe's result summary (the platform error message is abbreviated there; full error was returned in the tool transcript). The retained `probe.py` includes the attempted precheck and is explicitly marked not to rerun blindly. Native Windows limitations do not negate the exact parser/cleanup results, but they do limit all Linux operational conclusions to source inspection.

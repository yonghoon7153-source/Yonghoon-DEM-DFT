# Mixer first8 launch preparation: feasibility and inventory, 2026-11-06

Status: PREPARATION ONLY / full HOLD / research results 0. No actual host inspection, simulation, submission, active registration, external send, or repository edit was performed for this analysis. Rint② has priority. User's 11-06 statement that ibb is empty is a relayed observation, not live scheduler evidence; it does not authorize execution. Existing 18 runs and D3 SOP stay frozen; P1/T12 and four shared records are out of scope.

## Source and scope

Read-only checkout: `/workspace/nonrint-1104/mixer`, branch `codex/mixer-1104`, observed clean HEAD `7e40b7f2398a82cd5ae04b84017c0a9e1a89d521`. Root is aligning the requested `main` baseline `18bb6a2e41ad58129657a68450f4c88157f3d5a6`; this analysis does not assert alignment has completed. Re-read/pin final source before package generation. AGENTS.md was read. Managed cloud runtime skill was read and environment status inspected; no host connection attempted.

Primary sources:
- `scripts/mixer_precal_prepare.py`: exact fixed recipe, static in-memory API and stdout-only CLI; never a launcher.
- `scripts/mixer_precal_observe.py`: read-only fresh-result API/CLI, private source bindings, frame/log/identity contracts; never execution qualification.
- `docs/reviews/mixer_precal_first8_preparation_20261104/{README.md,author_decisions.json}`.
- `docs/reviews/mixer_precal_pre8_acceptance_20261105/{README.md,ledger_proposal.json}` and `docs/collab/codex_to_claude/20261105-0038_pre8-scoped-acceptance.md`.
- `docs/reviews/mixer_precal_exploration_registration_draft_20261104.md` §6 and `docs/reviews/mixer_precal_map_draft_evidence_20261104/planning_arithmetic.json`.

PRE8-01/02 acceptance is code/small synthetic scope. External real symlink behavior was unexecuted on Windows (27 OK, 1 ERROR/rc1); author Linux 28-pass records are separate. Actual 100000-particle positive pipeline, real log compatibility, binary/MPI/physics qualification remain unproven. MXD2R independent recheck remains separately pending. Do not turn any static preparation PASS into any of these qualifications or a GO.

## Exact available recipe and identifiers

Eight case IDs in API order: `PRECAL_R1_B1_U`, `PRECAL_R1_B1_C`, `PRECAL_R1_B2_U`, `PRECAL_R1_B2_C`, `PRECAL_R1_B3_U`, `PRECAL_R1_B3_C`, `PRECAL_N0`, `PRECAL_E0`.

B1/B2/B3 are 0.21244/21.244/212.44. Positive six use r=0.10, gamma(SE)=1, gamma(AM)=0.1 for U and 1 for C, wall from r=0.1. N0 is zero-CED layered/two revolutions; E0 is zero-CED uniform/zero revolutions. Fixed: seed 32452843, density generation lab20261014, planned N=100000, CGF151.4, SE stiffness×20, pairwise force preservation, dt_factor1, Fr0.0827, no baffles, full precision dumps. N0/E0 use separate unregistered zero contract. NP20 is proposed metadata only. Remaining12 are rejected by fixed API.

`prepare_case(case_id)` returns physical UTF-8/LF deck bytes and metadata; `validate_case(case_id, deck, meta)` requires exact generator recipe and metadata binding; positive six also use D2 readback and three U/C pair diffs are available through `prepare_first8()`. No CLI currently writes an export. A small standalone preparation writer is feasible, with fresh destination, exact eight allowlist, byte/meta SHA inventory, source pin, and non-executable templates; it must not change core generation/observation code or claim registration.

Actual deck hashes should be generated from the final pinned code, not copied from old static receipts. Metadata includes deck SHA/bytes. Hash and inventory every source dependency, each physical deck/meta, all three physical STL files, draft policy and command-template bytes; disallow symlinks and overwriting existing run outputs. Repository STL candidates exist at `dem_scripts/mixer_20260919/{Drum,Front,Back}.stl`. Their mere presence is not geometry qualification: reader currently derives geometry from scale only. Exact destination paths and actual host STL identity remain unset.

## Existing execution machinery is not first8 machinery

`dem_scripts/mixer_20260921/launch_highbo.sh` and `scripts/mixer_stage_gate.py` support historical registered cohorts. `launch_policy.json` is schema `mixer_highbo_launch_policy/4`, ID `STIFF-DEV-U-2026-10-05`, allowed stages first/rest/dev-e0/dev-rot/dev-bo/dev-u; none is first8. Reusing this policy or relabelling PRECAL cases as historical cohorts is invalid. Do not invoke its submit path or modify its active policy.

Historical SLURM defaults in launch_highbo.sh: `NP=20`, partition `cpu`, QoS `cpu-60`, conda env `myenv`, `mpirun --oversubscribe --bind-to none`; matched `#SBATCH -n` and `mpirun -np`. Stage time limits are policy-specific and cannot be inherited as first8 approval. `scripts/mixer_exact_frames.py` historical executable default is `/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi`. This is a candidate path, NOT verified current identity, access or compatibility. Historical upstream source tag 3d5c00f belongs to CFDEM/LIGGGHTS-PUBLIC; it is not a measured binary digest. Actual MPI library/launcher identity and module/environment setup remain unset.

`run_all.sh` defaults to serial and guards historical cohorts; do not use it for first8. `make_mixer_resume.py` and resume scripts are not first8 interfaces. First8 is fresh-only; periodic restart files do not authorize a resume or imply bit identity.

## Preparation package design (fail closed)

Recommended contents: README/runbook; manifest with source Git pin and hashes, eight cases, fixed recipe and explicit unknowns; `preflight-checklist.md`; an inert launch-command template (`.txt`, not runnable); read-only monitor and retrieval recipes (`.txt`); stop rules; author-choice form; draft policy with `execution_authorized:false`, `allowed_to_submit:[]`, full HOLD, no active registration; validation report.

Do not implement a launcher that accepts a free-form GO environment variable. Package provides no submission function; release requires a separately reviewed execution change and a specific first-author GO bound to final source, decks/STLs/binary/policy/NP/order/concurrency plus current host receipts and prerequisite decisions. In particular choices alone, an old GO, or user-reported empty ibb cannot unblock launch.

Preflight fields, to be collected later only within explicit authorization:
1. Date/hostname/operator, scheduler/QoS association and policy bytes/ID/SHA; exact first8 case allowlist and fresh output root; final author GO reference and unresolved gates resolved explicitly, including separate MXD2R disposition.
2. Absolute resolved executable, SHA256, version/build receipt and dependencies; MPI launcher resolved path/SHA/version, library compatibility and tested dump format/log behavior. Capture again inside allocated job before execution. No fictional identity and no assumption that `-help` is risk-free verification of physics.
3. SHA/size of deck, metadata, sources, STLs, runner and draft-to-approved policy; compare at preparation, staging, and job start. Abort before simulation on drift.
4. Author-approved NP, equal SLURM tasks/MPI ranks, CPU-per-task and thread counts; aggregate reserved running tasks across relevant user's jobs plus new wave ≤60 under cpu-60 and approved concurrency. Historical oversubscribe flag is not permission to exceed allocated tasks. Live resource/queue snapshot and D0.7 status must be recorded later; cloud `nproc` is irrelevant.
5. Disk/quota/inodes on actual destination plus retrieval space, estimated dumps/restarts/logs and reserve. No sourced numerical disk floor exists; mark UNKNOWN/BLOCKED until measured frame sizes or conservatively justified budget is approved. Rotation dump interval derives from steps_run//200; E0 uses minimum interval1000 and therefore must not be assumed to produce only one raw file.
6. Walltime request independently approved, labelled separately from estimated runtime. No current time limit selected.

Conceptual launch recipe only (all placeholders unresolved; no shell execution in this task): approved submit wrapper for one exact case → checked job start → matched allocated NP and `mpirun --oversubscribe --bind-to none -np <APPROVED_NP> <PINNED_ABSOLUTE_BINARY> -in in.mixer`, preserving stdout/stderr separately from `log.liggghts`, exit status and scheduler accounting. Do not offer `launch_highbo.sh first8`: it does not exist. Source `myenv` setup only if verified and approved, not because the old script did it.

## Monitoring, retrieval and stops

Monitor recipe should use exact returned job IDs and read-only scheduler status/accounting, task count, elapsed/time limit, logs for ERROR/NaN/lost particles, dump progress and disk/quota/inodes. Missing telemetry is UNKNOWN, not healthy. Record source SHA and timestamps. Check observed throughput before any later-wave release; no automated dependent submission.

Stop before start for any missing/mismatched pin, approval, rank/resource cap, policy scope, asset, disk budget or unresolved prerequisite. During a separately authorized execution, failure/interruption, unexpected rank, nonfinite/error log, storage threshold breach, stale/missing expected progress or identity drift means TECH/HOLD and no subsequent wave. Exact numeric disk/stall thresholds remain to be fixed before GO. Cancellation must target only this package's exact recorded job IDs; no broad user/partition cancellation. Preserve partial data and logs, record cause, no resume/retry/resubmit until a new author decision. UNDEFINED metric/denominator is reported as such, never coerced to zero or silently tuned.

Retrieval recipe must copy to a new local snapshot without delete/sync-overwrite, retain manifests and preflight/job-start receipts, scheduler stdout/stderr/accounting and exit status, in.mixer, deck_meta.json, physical STLs, log.liggghts, all dumps and restart files (restart forensic only). Hash source and destination; incomplete/changed/in-flight copies are unqualified. `n_expected`, if present, must equal planned count; its absence is permitted by observer, not permission to invent an observed count.

Post-copy CLI: `python3 scripts/mixer_precal_observe.py --case PRECAL_E0 --run <E0_SNAPSHOT>`; rotating cases require `--case <EXACT_CASE_ID> --run <CASE_SNAPSHOT> --reference <E0_SNAPSHOT>`. Observer expects in.mixer, deck_meta.json, log.liggghts and post/dump_<step>.liggghts. Four fresh run endpoints/thermo table are checked, but process exit/rank/binary identity need separate receipts. E0 is analyzed without reference. All structural failures preserve TECH and omit metrics. This procedure is prospective only; no actual data analysed here.

## Historical time estimate, not allocation or deadline

Source assumes 63–70 step/s from historical evidence, rounded lab geometry/timing and NP20. Rotation plus settling ≈7.72M steps →30.6–34.0h; E0 settling≈1.12M steps →4.4–4.9h. First8 seven rotating+one E0 total≈219–243 slot-hours, 4376–4862 core-hours. Old two-slot baseline-then-three-pair arithmetic≈122–136h (5–6 days) excludes queue, startup, changed precision I/O, current performance, holds, postprocess and retries; it is not an upper bound. An E0-first sequential qualification pause changes schedule, so do not present old wave elapsed time as the recommended schedule's completion date. Re-estimate from first approved fresh case before later release; no numerical speed guarantee.

## Three author questions, one recommendation each

1. NP: keep proposed NP20 per case? Recommendation: NP20, with identical rank/allocation receipts and no speed-driven NP change; proposal does not establish rank or insertion qualification.
2. Concurrency: what is the allowed maximum after qualification? Recommendation: one initial E0 only, then at most two concurrent NP20 jobs (40 cores), subject to current aggregate cpu-60 cap and explicit wave release. Do not use three slots just because ibb was reported empty.
3. Order: which cases first? Recommendation: E0 alone for reference/log/I/O qualification; pause for real-output review, then N0 alone to verify fresh rotating baseline; pause, then B1 U/C, B2 U/C, B3 U/C pairs in increasing B with review between waves. This supports early detection without declaring E0 validates cohesive dynamics. All8 remain proposed; no follow-on automatic submission.

These are planning questions, not requests to execute. New package creation can proceed without answers by encoding them as proposed/unapproved and preserving every execution blocker.

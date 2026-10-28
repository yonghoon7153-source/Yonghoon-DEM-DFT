# KG50 scheduler / G0–G3 independent review

Pin: `f118c1fd1e3eb1a558299663dcee6a0bf83b9942`.
Source: `repo/scripts/resume_ckpt.sh` (pinned bytes unchanged).

**Execution boundary:** exact embedded Python functions were extracted unchanged and executed with isolated Python. Git Bash cannot start in this environment (`NtCreateDirectoryObject ... 0xC0000022`, process rc 3221225794). Consequently neither fake-SLURM end-to-end probe nor GNU-awk functions ran. No real scheduler / WSL / DEM was invoked. Shell findings below are source-proved control-flow counterexamples, not reported as successfully executed Bash tests.

## SCHED-01 — P1: queue skip can still resubmit main from an old trial marker

Locations: `resume_ckpt.sh:661–662` (failure/busy continue), `:709–716` (write successful trial marker without invocation identity), `:718–719` (second loop reads any existing marker), `:777–780` (main submission). Test gap: `test_resume_ckpt.py:354–364` gives every scenario a fresh directory; queue tests `:516–523` never retain old job/mode/log artifacts.

Counterexample preparation: W already contains `job_r56t.txt = 7001`, `mode_r56.txt = settling 20001 ... 22001`, successful previous trial log and source log. Current `squeue -u` either returns this case's active main job OR fails. The first loop prints '건너뜀' and continues. The second loop still reads 7001, whose historical sacct remains `COMPLETED|0:0`, and consumes its old completed log. All four gates then permit main submission again.

Deterministic gate trace for the preserved fixture (author's own ORIG_LOG / T_OK):

- G0: old `7001` COMPLETED / 0:0; final row 22001 = old EXP; following Loop; ERROR 0.
- G1: first step 20001; Atoms 312506; KinEng 0.1000 = source 0.1000.
- G2: settling, no source S0 dumps; existing KE substitute sets PASS.
- G3: required 21000 and 22000 both present; only first row compared, 0.0955 vs 0.0950 = 0.526315789% < 5%.
- No second-loop condition requires trial 7001 to have been submitted by this invocation, nor rechecks case queue status before main.

`probe_stale_trial.py` builds both fake scheduler scenarios. Actual Bash execution is **NOT_EXECUTED_BASH_RUNTIME_BLOCKED**, accurately recorded in `stale_trial_results.json`; Linux replay command with the same sibling `repo/` layout: `python3 independent/scheduler/probe_stale_trial.py`.

Minimum fix: maintain an invocation-local approved/submitted case→job map and iterate only that map in phase 2. Never reconstruct eligibility solely from persistent files. Capture sbatch rc and validate job identity; bind mode/checkpoint/deck/log to invocation/job. Requery queue with status checked just before main (and use an atomic lock if concurrent invocations are in scope). Add two-invocation tests retaining W for busy queue, failed queue query, failed generator/static gate, and failed trial submission; require new main calls = 0 in every blocked case. Merely deleting files after the initial queue check does not fix queue-skip paths.

KG50-02 / KG50-14: **partial**. Fresh-directory queue and G0 protections can be supported, but 'skip means no main submission' is not a cross-invocation invariant.

## SCHED-02 — P2: continued first long run is not necessarily a TIMEOUT closed failure

Locations: `resume_ckpt.sh:693` (raw-line slicer), `:406–445` (logical-command sum), `:703–711` (uses sum as expectation), `:732` (G0 compares that enlarged expectation).

**Executed unchanged embedded Python results:**

| resumed first long run | static check | generated trial logical runs | trial_steps | G0 expected final step |
|---|---:|---|---:|---:|
| `run 180000` | rc 0 | `run 2000` | 2000 | 22001 |
| `run &` newline `180000` | rc 0 | `run 180000`; `run 1`; `run 2000` | 182001 | 202002 |

Trial files were built by a narrow explicitly labeled static transcription of the raw awk slicer; actual GNU awk did not execute. `probe_trial_steps.py` executes the unchanged production `check()` and `trial_steps()` via the extracted source; `trial_steps_results.json` and trial deck files preserve the outputs. Reproduce: `python3 independent/scheduler/probe_trial_steps.py`.

The 1-hour walltime is a cost cap, not proof this fails. A faster case may complete all 182001 steps; then G0 considers step202002 correct. Request Q3's 'G0 TIMEOUT이 막는 닫힌 실패' is false as a general guarantee. The known slicer limitation must be rejected **before submission**, or slicing must use the same logical-command parser. Assert trial schedule = the registered setup runs plus at most TS steps from the first logical long run. Do not simply bless the accidentally enlarged sum.

KG50-18: correct fix for legitimate `run1 + run2000`, but **partial** as a short-trial contract; Q3 needs correction. This does not assert the actual KG50 case would finish 182001 steps within 1h.

## G0 parsing hardening (source finding, not counted as executed proof)

`:648 lastrun()` labels any digit-first line while a thermo block is open as its final thermo row; it does not check header width. The prepared `probe_log_functions_NOT_EXECUTED.sh` presents last true row22000 then one-token `22001`, followed by `Loop time ... 1999 steps`. `lastrun` selects22001, while strict `tl` cannot produce that row. G0 never checks the loop's step count or finite terminal fields. Require a complete final thermo row with expected header and finite values, not merely a digit-first token. Do not label this dynamic reproduction completed here.

## Q6 / G3 wording

`:754–760` checks existence of *all* required regular-row steps but compares numeric values only at F2 (the first such step). Request wording that G3 'looks at 21000 and 22000' must not imply both are within5%. The prepared non-executed awk probe changes22000 to Atoms10 / KE1000000 while leaving21000 normal. This is an explicit existing design limitation, not a newly undisclosed implementation bug. State hashes and hidden restart history have separate scope.

## Q7 tool identity

Reporting the exact resume tool and external `dem_restart.py` SHA256 and checking approved expected identities before any submission is warranted given observed version drift. It authenticates the approved implementation, not physical validity. Bind those identities to the current invocation/trial evidence; hashing alone cannot repair SCHED-01.

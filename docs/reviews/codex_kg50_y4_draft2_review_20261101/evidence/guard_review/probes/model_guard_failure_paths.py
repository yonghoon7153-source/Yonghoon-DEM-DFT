"""Finite traces for the pinned guard. NOT a Bash/SLURM execution test.

Only pathlib/JSON and source extraction are used. Every job is an in-memory
synthetic identifier. No external commands, network, or simulation are run.
"""
from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[2]
REPO = BASE / "source/repo"
OUT = BASE / "guard_review/evidence"
guard = (REPO / "docs/50kg/d07_guard/d07_guard_v2_1031.sh").read_text(encoding="utf-8")
resume = (REPO / "scripts/resume_ckpt.sh").read_text(encoding="utf-8")
lines = guard.splitlines()
branch = "\n".join(lines[55:59])
assert 'scancel $J' in branch and 'exit 1' in branch
assert 'main_job' not in branch and 'squeue' not in branch and 'sacct' not in branch
assert 'while :; do grep -q \'^LMP_IDENTITY \' $O 2>/dev/null && break; sleep 15; done' in guard
assert 'while :; do grep -q \'^결정\' $W/$A/result.txt 2>/dev/null && break; sleep 10; done' in guard

traces = []
for scenario in ("cancellation_failure", "late_cancellation"):
    events = ["new receipt differs from approved OKR", "guard enters lines 56-59"]
    trial_state = "RUNNING" if scenario == "cancellation_failure" else "COMPLETED"
    main_state = "NOT_SUBMITTED" if scenario == "cancellation_failure" else "RUNNING"
    events += [f"synthetic trial=444444 state={trial_state}", f"synthetic main=555555 state={main_state}"]
    events.append("mock scancel(444444) returns nonzero; no scheduler was called")
    events.append("guard ignores return value and exits 1; no main-job inspection")
    if scenario == "cancellation_failure":
        trial_state = "COMPLETED"
        main_state = "RUNNING"
        events += ["trial later completes G0-G3", "resume tool checks its own new receipt MIS (not approved OKR)", "resume branch may submit synthetic main 555555"]
    traces.append({"scenario":scenario,"trace":events,"guard_exit":1,"main_final_state":main_state,"approval_block_guaranteed":False,"evidence_level":"independent control-flow model, not actual Bash"})

events = []
for tick in range(20):
    events.append({"poll":tick+1,"grep_identity":False,"job_state_in_world":"FAILED","guard_queries_job_state":False,"guard_action":"sleep 15; repeat"})
traces.append({"scenario":"main_terminal_before_identity","trace":events,"after_20_polls_seconds":300,"guard_still_waiting":True,"invariant":"while no identity line appears, condition never exits regardless of terminal job state","evidence_level":"independent control-flow model, not actual Bash"})

# Exercise the actual embedded pure-Python producer to establish the real
# runner ordering. It only creates text and does not run the resulting script.
start = resume.index("def render(C, SFX, NP, WR, info, trial):")
end = resume.index("\ndef main():", start)
namespace = {}
exec(compile(resume[start:end], "pinned_resume_runner_render", "exec"), namespace)
info={"sb":{"--time=":"5-00:00:00"},"ab":{"재개 덱":"/synthetic/unavailable/work/input.liggghts"},"sha":{"재개 덱":"a"*64,"체크포인트":"b"*64},"ckp":"/synthetic/unavailable/work/restart.bin","env":[]}
runner=namespace["render"]("synthetic_case","r56","56","/synthetic/unavailable/work",info,False)
assert runner.index('cd "/synthetic/unavailable/work" || exit 1') < runner.index('echo "LMP_IDENTITY ')
(OUT/"rendered_runner.synthetic.sh").write_text(runner,encoding="utf-8")
(OUT/"failure_path_models.json").write_text(json.dumps({"disclaimer":"No Bash, SLURM, remote process, cancellation, or DEM execution. Models describe pinned code branches and do not substitute for end-to-end reproduction.","guard_mismatch_branch":branch,"traces":traces,"producer_render_executed":True,"producer_output":"rendered_runner.synthetic.sh","producer_property":"cd failure exits before LMP_IDENTITY"},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("3 source-bound failure traces saved; actual pure-Python render() ordering verified. No shell or scheduler invoked.")

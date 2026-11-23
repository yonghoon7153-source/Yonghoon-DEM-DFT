"""B2-C preflight for the first author's single overlapping development arm."""
import os
from pathlib import Path
import re
import runpy
import shutil
import time


rotation = runpy.run_path(str(Path(__file__).with_name("mixer_rotation_n0_ibb.py")))
base = rotation["base"]
need = base["need"]
U_JOB = "368758"
U_CASE = "PRECAL_R1_B2_U"


def queue_budget(queue, expected_workdir):
    """Count all user CPUs. Only the bound B2-U may occupy another mixer slot."""
    used, first8 = base["queue_counts"](queue)
    seen = set()
    peer_count = 0
    for line in queue.splitlines():
        if not line.strip():
            continue
        job, name, state, cpus, qos, partition, workdir = line.split("|")
        need(re.fullmatch(r"[0-9]+(?:_[0-9]+)?(?:\+[0-9]+)?", job) and job not in seen
             and int(cpus) > 0, "unresolved queue job or CPU allocation")
        seen.add(job)
        if job == U_JOB:
            need(name == "runner.sbatch" and cpus == "20" and qos == "cpu-60"
                 and partition == "cpu" and workdir == str(expected_workdir),
                 "active B2-U differs from the approved peer")
            peer_count += 1
        elif name == "runner.sbatch":
            need(workdir not in ("", "(null)", "N/A", "Unknown"), "unresolved runner workdir")
    need(first8 == peer_count, "another active first8 job occupies a mixer slot")
    need(used + 20 <= 60, "B2-C exceeds the aggregate CPU budget")
    return used, first8


def preflight(root, ctx, binary, mpi, prefix, prior_root):
    """Apply the existing 48 h rotation and E0 site checks with the B2-C queue rule."""
    shutil.copyfile(root / "control/runtime_reference.json", ctx / "control/runtime_reference.json")
    capture = base["capture"]
    user = os.environ["USER"]
    assoc_args = ["sacctmgr", "-n", "-P", "show", "assoc", "user=" + user, "format=User,QOS,MaxWall"]
    part_args = ["scontrol", "show", "partition", "cpu", "-o"]

    wall = ctx / "evidence/wall"
    max_wall, _ = capture(wall, "qos", ["sacctmgr", "-n", "-P", "show", "qos", "cpu-60", "format=Name,MaxWall"])
    assoc, _ = capture(wall, "assoc", assoc_args)
    partition, _ = capture(wall, "partition", part_args)
    rotation["wall_limits"](max_wall, assoc, partition, user)

    identity = base["runtime"](ctx, binary, mpi, prefix, "runtime_pre")
    need(identity["matches"], "runtime identity mismatch")
    scheduler = ctx / "evidence/scheduler_pre"
    qos, _ = capture(scheduler, "qos", ["sacctmgr", "-n", "-P", "show", "qos", "cpu-60", "format=Name,MaxTRESPU"])
    assoc, _ = capture(scheduler, "assoc", assoc_args)
    partition, _ = capture(scheduler, "partition", part_args)
    base["scheduler_ok"](qos, assoc, partition, user)

    folder = ctx / "evidence/live_preflight_0"
    calls = {
        "queue": ["squeue", "--array", "-h", "-u", user, "-o", "%i|%j|%T|%C|%q|%P|%Z"],
        "df": ["df", "-PB1", str(ctx)],
        "inode": ["df", "-Pi", str(ctx)],
        "ost": ["lfs", "df", str(ctx)],
        "quota": ["lfs", "quota", "-u", user, str(ctx)],
    }
    observed = time.time()
    raw, receipts = {}, {}
    for label, args in calls.items():
        raw[label], receipts[label] = capture(folder, label, args, 10)
    need(0 <= time.time() - observed <= 10, "preflight ten-second window exceeded; no automatic retry")

    peer_case = (prior_root / "B" / base["F8"] / "cases" / U_CASE).resolve(strict=True)
    used, first8 = queue_budget(raw["queue"], peer_case)
    storage = base["storage_ok"](raw["df"], raw["inode"], raw["ost"])
    need(not re.search(r"\d+\*", raw["quota"]), "quota exceeded marker")
    live = dict(observed_unix=observed, qos="cpu-60", partition="cpu", qos_verified=True,
                d07_finished=True, d07_basis="historical completion: job 338349; baseline_table section 0-A",
                paths_verified=True, reserved_cpus=used, running_first8=first8,
                allowed_mixer_peer=dict(job=U_JOB, case=U_CASE, observed_in_queue=bool(first8)),
                cpu_count_rule="all listed active user jobs including pending and completing",
                raw_outputs=receipts, **storage)
    base["put"](ctx / "evidence/live_preflight.json", live)
    live.update(qualification_accepted=True, qualification_scope="E0_DEVELOPMENT_ONLY",
                E0_job="366423", N0_job="367547", e0_W9_at_T9=False)
    approved = ctx / "evidence/b2_c_live.json"
    base["put"](approved, live)
    return approved

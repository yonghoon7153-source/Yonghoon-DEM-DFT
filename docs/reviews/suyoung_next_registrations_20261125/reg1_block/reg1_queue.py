"""reg1 contact mini (Suyoung 2D registration 1) execution block: environment gate, two-core queue, return unpack.

DEVELOPMENT_ONLY.  This module never steps the MPM itself.  `go` launches the pinned thin driver
(`driver.py RUN`) once per registered arm on two CPUs of distinct physical cores (taskset, one
thread per arm), longest arm first, with the registered per-arm limit plus a 30 s grace, no
automatic retry, and keeps going when an arm fails.  `env`, `cores` and `plan` compute nothing.

    python3 -I -X utf8 -B reg1_queue.py env
    python3 -I -X utf8 -B reg1_queue.py cores ROOT
    python3 -I -X utf8 -B reg1_queue.py plan ROOT
    python3 -I -X utf8 -B reg1_queue.py go ROOT RUN
    python3 -I -X utf8 -B reg1_queue.py unpack ROOT RETURN_DIRECTORY TEMP

ROOT is the unpacked block package (or a repository checkout): pinned files sit at their
repository paths and are read only after their sha256 matches PINS below (the seven physics
sources are checked by the driver's own SOURCES pins).
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import signal
import subprocess
import sys
import tarfile
import time
from types import ModuleType


LABEL = "DEVELOPMENT_ONLY"
DRIVER = "docs/reviews/suyoung_next_registrations_20261125/driver/driver.py"
REGISTRATION = "docs/reviews/suyoung_next_registrations_20261125/reg1_contact_mini_20261125.md"
FORCE_RULE = "docs/reviews/suyoung_u6c_force_rule_20261122/force_rule.py"
RULE_JSON = "docs/reviews/suyoung_u6c_force_rule_20261122/rule.json"
DOUBLING = "docs/reviews/suyoung_u6c_doubling_readback_20261122/doubling.py"
COORDINATE = "docs/reviews/suyoung_q13_setting2_20261125/coordinate.py"
PINS = {
    "docs/reviews/suyoung_next_registrations_20261125/driver/driver.py":
        "d45c53f5d8dd43e629fa97eb322cb97446ba894d96c900c4e8976514217d3179",
    "docs/reviews/suyoung_next_registrations_20261125/reg1_contact_mini_20261125.md":
        "11c19c422d27f5ee17c64016fea91e230dc1f580198486f489851e083455fd2b",
    "docs/reviews/suyoung_u6c_force_rule_20261122/force_rule.py":
        "145b5fe6f456e8b66c2a8cc422ff88648c82d07c4420482f06bc6da7a5b1b6db",
    "docs/reviews/suyoung_u6c_force_rule_20261122/rule.json":
        "1736322b4b2f4cef384becd97099998668137c19272e504edd951b698502a8f4",
    "docs/reviews/suyoung_u6c_doubling_readback_20261122/doubling.py":
        "9d664ed38a70295b9bd04ecbf5dae4ffda663c5efbc348c30a77bf6b99fa1bda",
    "docs/reviews/suyoung_q13_setting2_20261125/coordinate.py":
        "fc71075de94c49e33b85a0a8b791a3c8abb4da81a2378a20bcfb98d0857370b9",
}
WORKER = DRIVER
TARGET_ENVIRONMENT = ('3.12.3', '2.5.2')
GRACE_S = 30
RESULT_TAR = "suyoung_contact_mini_result.tar.gz"
THREAD_VARIABLES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS",
                    "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def say(text):
    """Screen line, best effort: a closed screen (terminal gone) must not stop the queue or its record."""
    try:
        print(text, flush=True)
    except OSError:
        pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_pinned(root, relative, name=None):
    """Execute the pinned bytes of `relative` under ROOT as a fresh module (refuses a changed file)."""
    path = Path(root).resolve() / relative
    raw = path.read_bytes()
    require(sha(raw) == PINS[relative], "pinned file changed: " + relative)
    module = ModuleType(name or "reg1_pinned_" + Path(relative).stem)
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def check_pin(root, relative):
    require(sha((Path(root).resolve() / relative).read_bytes()) == PINS[relative], "pinned file changed: " + relative)


def environment_gate(target=None):
    """Python and NumPy of this interpreter equal the registered WSL target; thread variables are 1."""
    target = tuple(TARGET_ENVIRONMENT if target is None else target)
    import numpy
    here = (platform.python_version(), numpy.__version__)
    threads = {k: os.environ.get(k) for k in THREAD_VARIABLES}
    line = f"python={here[0]} numpy={here[1]} target={target[0]}/{target[1]}"
    if here != target:
        return False, "ENVIRONMENT_MISMATCH " + line
    if any(v != "1" for v in threads.values()):
        return False, "THREAD_VARIABLES_NOT_ONE " + json.dumps(threads, sort_keys=True)
    return True, "ENVIRONMENT_OK " + line + " threads=1"


def engine_for(root):
    driver = load_pinned(root, DRIVER, "reg1_queue_driver")
    return driver, driver.Engine(Path(root).resolve())


def queue_plan(driver, engine):
    """The 50 registered arms, longest first (registered upper estimate), ties by name."""
    jobs = []
    for arm in driver.reg1_arms():
        p = engine.plan(arm)
        jobs.append(dict(arm=arm.name, cells=arm.cells, steps=p["steps"], limit_s=p["limit_s"],
                         est_high_s=p["est_high_s"], v_over_cP=p["v_over_cP"]))
    jobs.sort(key=lambda j: (-j["est_high_s"], j["arm"]))
    return jobs


def two_cores(root):
    """Q13's pinned core choice: two CPUs of distinct (package, core_id) from this process's affinity."""
    coord = load_pinned(root, COORDINATE, "reg1_queue_coordinate")
    chosen = coord.eligible()
    cpus = (chosen["S"], chosen["F"])
    return cpus, {c: list(coord.topology(c)) for c in cpus}


def run_queue(jobs, cpus, cores, command_for, run, grace_s=GRACE_S, poll_s=.5, env=None):
    """Run every job once on the two CPUs; write RUN/execution.json (also on interruption).

    jobs: [{"arm", "limit_s"}, ...] in queue order.  A job still running limit_s + grace_s after its
    start is killed (rc 124).  A failed job never stops the queue and is never started again.
    """
    run = Path(run)
    cpus = tuple(cpus)
    require(len(cpus) == 2 and cpus[0] != cpus[1] and list(cores[cpus[0]]) != list(cores[cpus[1]]),
            "two CPUs on distinct physical cores required")
    names = [j["arm"] for j in jobs]
    require(len(set(names)) == len(names), "duplicate arm in the queue")
    (run / "arms").mkdir()
    (run / "logs").mkdir()
    child_env = dict(os.environ if env is None else env)
    child_env.update({k: "1" for k in THREAD_VARIABLES})
    pending, running, records = list(jobs), {}, {}
    complete = False

    def stop(signum, _frame):
        raise InterruptedError(f"received signal {signum}")
    previous = {s: signal.signal(s, stop) for s in (signal.SIGHUP, signal.SIGTERM)}

    def finished(cpu, rc, killed):
        job, proc, started, _ = running.pop(cpu)
        ended = time.time_ns()
        records[job["arm"]] = dict(arm=job["arm"], cpu=cpu, physical_core=list(cores[cpu]), threads=1, rc=rc,
                                   killed=killed, limit_s=job["limit_s"], started_ns=started, ended_ns=ended,
                                   elapsed_including_wrapper_s=(ended - started) / 1e9, attempts=1,
                                   log=f"logs/{job['arm']}.log")
        say(f"END arm={job['arm']} cpu={cpu} rc={rc} killed={str(killed).lower()} "
            f"elapsed_s={(ended - started) / 1e9:.1f} done={len(records)}/{len(jobs)}")

    try:
        while pending or running:
            for cpu in cpus:
                if cpu in running or not pending:
                    continue
                job = pending.pop(0)
                with (run / "logs" / (job["arm"] + ".log")).open("xb") as log:
                    started, mono = time.time_ns(), time.monotonic()
                    proc = subprocess.Popen(command_for(job["arm"], cpu), stdout=log, stderr=subprocess.STDOUT,
                                            start_new_session=True, env=child_env)
                running[cpu] = (job, proc, started, mono)
                say(f"BEGIN order={names.index(job['arm']) + 1:02d} arm={job['arm']} cpu={cpu} "
                    f"core={cores[cpu]} limit_s={job['limit_s']}")
            for cpu, (job, proc, _, mono) in list(running.items()):
                rc = proc.poll()
                if rc is None and time.monotonic() - mono > job["limit_s"] + grace_s:
                    proc.kill()
                    proc.wait()
                    finished(cpu, 124, True)
                elif rc is not None:
                    finished(cpu, rc, False)
            if running:
                time.sleep(poll_s)
        complete = True
    finally:
        for cpu, (job, proc, _, _) in list(running.items()):
            if proc.poll() is None:
                proc.kill()
            proc.wait()
            finished(cpu, proc.returncode, True)
        for s, handler in previous.items():
            signal.signal(s, handler)
        execution = dict(label=LABEL, complete=complete, cpus=list(cpus),
                         physical_cores={str(c): list(cores[c]) for c in cpus}, grace_s=grace_s,
                         queue_order=names, retries=0, arms=records)
        with (run / "execution.json").open("x", encoding="ascii", newline="\n") as stream:
            json.dump(execution, stream, indent=2, sort_keys=True)
            stream.write("\n")
    return execution


def go(root, run):
    root, run = Path(root).resolve(), Path(run).resolve()
    driver, engine = engine_for(root)
    jobs = queue_plan(driver, engine)
    cpus, cores = two_cores(root)
    worker = root / WORKER

    def command(arm, cpu):
        return ["taskset", "-c", str(cpu), sys.executable, "-I", "-X", "utf8", "-B", str(worker), "RUN",
                "--arm", arm, "--out", str(run / "arms" / arm), "--cpu", str(cpu), "--root", str(root)]
    say(f"QUEUE_START arms={len(jobs)} cpus={cpus[0]},{cpus[1]} cores={cores[cpus[0]]},{cores[cpus[1]]} "
        f"grace_s={GRACE_S} retries=0")
    execution = run_queue(jobs, cpus, cores, command, run)
    failed = sorted(a for a, r in execution["arms"].items() if r["rc"] != 0)
    say(f"QUEUE_DONE arms={len(execution['arms'])} nonzero_rc={len(failed)} "
        f"killed={sum(r['killed'] for r in execution['arms'].values())}"
        + ("" if not failed else " nonzero=" + ",".join(failed)))
    return execution


def plan_lines(root):
    driver, engine = engine_for(root)
    problems = [p for p in driver.registration_problems(engine) if p.startswith(("R1-", "reg1"))]
    require(not problems, "reg1 plan differs from the registration: " + "; ".join(problems))
    jobs = queue_plan(driver, engine)
    lines = [f"QUEUE order={i:02d} arm={j['arm']} cells={j['cells']} V/cP={j['v_over_cP']:.5f} steps={j['steps']} "
             f"limit_s={j['limit_s']} est_high_s={j['est_high_s']:.0f}" for i, j in enumerate(jobs, 1)]
    totals = driver.plan_totals(engine, driver.reg1_arms())
    lines.append(f"QUEUE_TOTAL arms={len(jobs)} cpu_h={totals['cpu_low_h']:.2f}-{totals['cpu_high_h']:.2f} "
                 f"two_core_wall_h={totals['wall2_low_h']:.2f}-{totals['wall2_high_h']:.2f} "
                 f"longest_limit_s={totals['longest_limit_s']} grace_s={GRACE_S} retries=0")
    return lines


def unpack_return(root, directory, temp):
    """Verify the return folder (outer sums, members, inner sums, screen) and unpack it under TEMP."""
    coord = load_pinned(root, COORDINATE, "reg1_unpack_coordinate")
    directory, temp = Path(directory), Path(temp)
    coord.checks(directory, [RESULT_TAR, "screen.txt"])
    seen = set()
    with tarfile.open(directory / RESULT_TAR, "r:gz") as archive:
        for item in archive:
            p = PurePosixPath(item.name)
            require(p.parts and p.parts[0] == "run" and ".." not in p.parts and str(p) == item.name
                    and p not in seen and (item.isdir() or item.isfile()), "unexpected return member " + item.name)
            seen.add(p)
            dest = temp.joinpath(*p.parts)
            if item.isdir():
                dest.mkdir(parents=True, exist_ok=True)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(item) as src, dest.open("xb") as out:
                shutil.copyfileobj(src, out)
    run = temp / "run"
    coord.checks(run, [p.relative_to(run).as_posix() for p in run.rglob("*") if p.is_file() and p != run / "SHA256SUMS"])
    screen = (run / "screen.txt").read_bytes()
    require(screen == (directory / "screen.txt").read_bytes(), "returned screen differs from the archived screen")
    last = screen.splitlines()[-1] if screen.splitlines() else b""
    require(last == b"COMMAND_RC=0", "incomplete return: " + last.decode("ascii", "replace"))
    return run, sha((directory / RESULT_TAR).read_bytes()), sha(screen)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    mode = args.pop(0) if args else ""
    try:
        if mode == "env" and not args:
            ok, line = environment_gate()
            print(line)
            return 0 if ok else 1
        if mode == "cores" and len(args) == 1:
            cpus, cores = two_cores(args[0])
            print(f"CORES cpu={cpus[0]} core={cores[cpus[0]]} cpu={cpus[1]} core={cores[cpus[1]]}")
            return 0
        if mode == "plan" and len(args) == 1:
            print("\n".join(plan_lines(args[0])))
            return 0
        if mode == "go" and len(args) == 2:
            go(*args)
            return 0
        if mode == "unpack" and len(args) == 3:
            run, tar_sha, screen_sha = unpack_return(*args)
            print(f"RETURN_VERIFIED tar_sha256={tar_sha} screen_sha256={screen_sha}")
            return 0
    except (OSError, ValueError, KeyError, tarfile.TarError) as exc:
        print("REG1_QUEUE_REFUSED", type(exc).__name__, exc)
        return 1
    print("usage: env | cores ROOT | plan ROOT | go ROOT RUN | unpack ROOT RETURN TEMP")
    return 2


if __name__ == "__main__":
    sys.exit(main())

"""Exercise the shipped B2-U tar in a temporary Linux directory using a fake scheduler.

Supply the source tar and the two original B1 return directories. This writes only
in a temporary local directory. The five B2 inputs and the submitter come from the
shipped tar. No simulator, MPI process or scheduler command is started.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from types import SimpleNamespace
from unittest.mock import patch


def deny_external(event, args):
    if event in {"subprocess.Popen", "os.system", "socket.connect"}:
        raise RuntimeError(f"External operation in offline fixture: {event}")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage_prior(folder, role, supplied):
    receipt = json.loads((supplied / "return.json").read_bytes())
    ctx = folder / "arms" / role
    out = ctx / receipt["directory"]
    out.mkdir(parents=True)
    shutil.copyfile(supplied / "return.json", ctx / "return.json")
    shutil.copyfile(supplied / "SHA256SUMS", out / "SHA256SUMS")


def exercise(tar, u_dir, c_dir):
    if not sys.platform.startswith("linux"):
        raise SystemExit("Use Linux for the canonical submitter fixture")
    if digest(tar) != "332148bd05db2718da30487352cc54523cb69b9abb92db43a5af44a8fa51df64":
        raise ValueError("Unexpected B2-U source tar")
    sys.addaudithook(deny_external)
    with tempfile.TemporaryDirectory(prefix="b2-contract-") as tmp:
        work = Path(tmp)
        with tarfile.open(tar) as archive:
            for member in archive:
                dest = work / member.name
                if not member.isfile() or not dest.resolve().is_relative_to(work):
                    raise ValueError("Unexpected packet member")
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open("xb") as out, archive.extractfile(member) as stream:
                    shutil.copyfileobj(stream, out)
        root = work / "packet"
        sys.path.insert(0, str(root / "controller"))
        import mixer_b2_u_ibb as driver

        prior = work / "previous" / "packet"
        stage_prior(prior, "U", u_dir)
        stage_prior(prior, "C", c_dir)
        before = {p: digest(p) for p in prior.rglob("*") if p.is_file()}
        runtime = (work / "engine", work / "mpi", work / "prefix")
        for file in runtime[:2]:
            file.write_bytes(b"simulated executable")
        runtime[2].mkdir()
        pin_file = next((root / "control").glob("*pin.json"))
        pin = json.loads(pin_file.read_bytes())["commit"]
        calls = []

        def live(root, ctx, *args):
            output = ctx / "evidence" / "mock_live.json"
            driver.put(output, dict(observed_unix=time.time(), running_first8=0, reserved_cpus=6,
                                    qos="cpu-60", partition="cpu", qos_verified=True, disk_budget_verified=True,
                                    inode_budget_verified=True, d07_finished=True, paths_verified=True,
                                    qualification_accepted=True))
            return output

        def fake_submit(argv, **kwargs):
            assert argv[:3] == ["sbatch", "--parsable", "--no-requeue"]
            assert {"--ntasks=20", "--cpus-per-task=1", "--nodes=1", "--qos=cpu-60",
                    "--partition=cpu", "--time=2-00:00:00"} <= set(argv)
            assert not any("--array" in arg for arg in argv)
            calls.append(argv)
            return SimpleNamespace(stdout="5103\n", stderr="", returncode=0)

        case_id = "PRECAL_R1_B2_U"
        with patch.dict(os.environ, {"PATH": os.environ["PATH"], "USER": "tester", "HOME": tmp}, clear=True), \
                patch.object(driver, "runtime_preflight", live):
            submit, ap = driver.prepare(root, prior, "U", "GO_B2_U_ONCE", pin, runtime)
            approval = driver.read(ap)
            assert approval["wave_release"] == [case_id] and approval["approved_concurrency"] == 1
            campaign = driver.read(Path(approval["campaign_policy"]["path"]))
            assert campaign["max_concurrency"] == 1
            submit_main = runpy.run_path(str(submit))["main"]
            with patch.object(subprocess, "run", fake_submit):
                submit_main(str(ap))
                try:
                    submit_main(str(ap))
                except (RuntimeError, ValueError, SystemExit):
                    pass
                else:
                    raise AssertionError("Repeated submission was accepted")
            assert len(calls) == 1
            case = Path(approval["case_dir"])
            assert driver.read(case / "submission.receipt.json")["job_id"] == "5103"
            assert sorted(p.name for p in (submit.parent / "admission").iterdir()) == [
                case_id + ".reservation.json", case_id + ".submission.json"]
            assert not (case.parent / "PRECAL_R1_B2_C").exists()
            driver.put(case / "job_end.json", dict(job_id="5103", returncode=0, end_unix=time.time()))
            post = case / "post"
            post.mkdir()
            for index in range(1, 235):
                (post / f"mix_{index * 32976}.liggghts").write_bytes(b"fixture")
            with patch.dict(driver.base, runtime=lambda *args: {"matches": True}):
                assert driver.collect(root, "U", "5103", "5103|COMPLETED|0:0|\n", runtime, True, pin) == 0
            pointer = driver.read(root / "arms/U/return.json")
            assert pointer["case"] == case_id and pointer["role"] == "U" and pointer["return_ready"]
            assert pointer["frame_count"] == 234 and pointer["w9"] == "LIVE_TERMINAL_MATCH"
            result = root / "arms/U" / pointer["directory"]
            assert all(digest(result / name) == sha for name, sha in pointer["archive_hashes"].items())
            assert len(pointer["archive_hashes"]) == 2
        after = {p: digest(p) for p in prior.rglob("*") if p.is_file()}
        assert before == after
    print("B2_U_OFFLINE_OK submit_calls=1 repeat_refused=1 B2_C_calls=0 frames=234 W9=LIVE_TERMINAL_MATCH archive_hashes=2/2 B1_unchanged=1")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source_tar", "b1_u_dir", "b1_c_dir"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    exercise(args.source_tar, args.b1_u_dir, args.b1_c_dir)

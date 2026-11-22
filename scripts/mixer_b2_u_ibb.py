"""Run a single author-approved B2-U development rotation from an isolated installation."""
import argparse
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tarfile
import time


HERE = Path(__file__).resolve().parent
b1 = runpy.run_path(str(HERE / "mixer_b1_pair_ibb.py"))
rotation, base = b1["rotation"], b1["base"]
need, sha, put, read, ref = (base[k] for k in ("need", "sha", "put", "read", "ref"))
F8 = base["F8"]
B1_PIN = "8c5c90086a3ada71d88e34adbc790ba629cbd1a7"
PAIR_SHA = "6fb926e4a0fbe2b536acccb90cf10e440da2d064611cf0b0bc913a341d8f0f1a"
CASE = "PRECAL_R1_B2_U"
TOKEN = "GO_B2_U_ONCE"
DECK = "b37974e5c0674947912e932c55517e9e84243293f29257183f8f70cc032f2fd7"
META = "7e7b3f13354aaf312d780f8b96094a432cc64fadd20c335b815ab871ff2602ec"
ARCHIVES = ("b2_report.tar.gz", "b2_full_result.tar.gz")
CONTROLLERS = ("mixer_b2_u_ibb.py", "mixer_b1_pair_ibb.py",
               "mixer_rotation_n0_ibb.py", "mixer_e0_pilot_ibb.py")
runtime_preflight = b1["runtime_preflight"]


def case_name(role):
    need(role == "U", "only B2-U is authorized")
    return CASE


def author_token(role, token):
    case_name(role)
    need(token == TOKEN, "explicit B2-U author GO required")


def authority(pin, previous):
    return dict(label="DEVELOPMENT_DATA_ONLY", release_pin=pin, author_action=TOKEN,
                allowed_to_submit=[CASE], execution_authorized=True, runtime_concurrency=1,
                asset_manifest=b1["B_MANIFEST"], previous=previous,
                automatic_retry=False, paper_qualified=False)


def prior_completion(record, role, jid):
    sched = record.get("scheduler", {})
    need(record.get("case") == "PRECAL_R1_B1_" + role and record.get("role") == role
         and record.get("release_pin") == B1_PIN and record.get("job_id") == jid
         and record.get("job_end_id") == jid and type(record.get("runner_rc")) is int
         and record["runner_rc"] == 0 and record.get("return_ready") is True
         and record.get("exact_frame_names") is True and record.get("frame_count") == 234
         and record.get("post_runtime_matches") is True and record.get("w9") == "LIVE_TERMINAL_MATCH"
         and sched.get("job_id") == jid and sched.get("state") == "COMPLETED"
         and sched.get("exit_code") == "0:0", "B1 completion or live W9 changed")


def previous_pair(prior_root, original_pair):
    """Match original pointers and small digest lists to the B1 U/C local readback."""
    need(not original_pair.is_symlink() and sha(original_pair) == PAIR_SHA, "B1 pair readback identity")
    pair = read(original_pair)
    need(pair["status"] == "DEVELOPMENT_READBACK_OK" and pair["formal_review"] is False
         and pair["next_wave_author_go"] is False, "B1 pair scope")
    previous = b1["N0_POINTER"]
    for role, jid in (("U", "368139"), ("C", "368316")):
        ctx = prior_root / "arms" / role
        path = ctx / "return.json"
        need(not path.is_symlink() and path.is_file(), "B1 pointer missing or linked")
        pointer = ref(path)
        tech = pair[role]["technical"]
        need(pointer["sha256"] == tech["return_pointer_sha256"] and previous == tech["previous_return_sha256"],
             "B1 return history differs")
        rec = read(path)
        prior_completion(rec, role, jid)
        need(re.fullmatch(r"collection_[0-9]+", rec["directory"]), "B1 collection directory")
        manifest = ctx / rec["directory"] / "SHA256SUMS"
        need(not manifest.is_symlink() and manifest.is_file(), "B1 archive digest list")
        expected = rec["archive_hashes"]
        need(set(expected) == set(b1["ARCHIVES"]) and expected == tech["archive_sha256"], "B1 archive binding")
        rows = manifest.read_text(encoding="ascii").splitlines()
        need(sorted(rows) == sorted(h + "  " + name for name, h in expected.items()), "B1 archive digest mismatch")
        previous = pointer["sha256"]
    return pointer


def prepare(root, prior_root, role, token, pin, runtime):
    author_token(role, token)
    here_root, prior_root = root.resolve(), prior_root.resolve()
    need(here_root != prior_root and here_root not in prior_root.parents and prior_root not in here_root.parents,
         "B2 requires its own installation")
    original_pair = root / "control/b1_pair_readback.json"
    peer = previous_pair(prior_root, original_pair)
    manifest_path = root / "B_manifest.json"
    need(sha(manifest_path) == b1["B_MANIFEST"], "B manifest identity")
    manifest = base["verify_deployment"](root)
    need(manifest["source_pin"] == rotation["PIN_B"] and len(manifest["files"]) == 283
         and manifest["approved_return_sha256"] == rotation["A_B_RETURN"], "B provenance")
    here = root / "B" / F8
    assets = here / "planned_assets" / CASE
    need(sha(assets / "in.mixer") == DECK and sha(assets / "deck_meta.json") == META, "B2-U assets")
    need(sha(root / "control/n0_return.json") == b1["N0_POINTER"], "N0 receipt identity")
    ctx = root / "arms/U"
    ctx.mkdir(parents=True, exist_ok=False)
    (ctx / "control").mkdir()
    (ctx / "evidence").mkdir()
    auth = root / "control/pair_authority.json"
    put(auth, authority(pin, peer))
    policy = here / "campaign_policy.json"
    put(policy, base["policy"](str(here), sha(auth)))
    case, folder = here / "cases" / CASE, here / "approvals" / CASE
    case.mkdir(parents=True)
    folder.mkdir(parents=True)
    parts = ("in.mixer", "deck_meta.json", "Drum.stl", "Front.stl", "Back.stl")
    for name in parts:
        shutil.copyfile(assets / name, case / name)
    put(ctx / "evidence/author_arm.json", dict(token=token, case=CASE, pin=pin, previous=peer,
                                              label="DEVELOPMENT_DATA_ONLY", automatic_retry=False))
    put(folder / "qualification.json", dict(E0_development_accepted=True, paper_qualified=False,
                                           E0_W9_at_T9=False, B1_pair_readback=ref(original_pair), previous=peer))
    put(folder / "policy.json", dict(policy_id="B2_U_DEVELOPMENT_ONLY", execution_authorized=True,
                                     allowed_to_submit=[CASE]))
    put(folder / "mxd2r_disposition.json", dict(scope="one B2-U development arm", E0_known_limit="MXE0-02",
                                               paper_release=False))
    python = Path(sys.executable).resolve(strict=True)
    binary, mpi, prefix = runtime
    paths = [root / "B" / base["safe_rel"](row["path"]) for row in manifest["files"]]
    paths.extend(case / n for n in parts)
    paths.extend(HERE / n for n in CONTROLLERS)
    paths.extend([python, auth, original_pair, Path(peer["path"]), manifest_path,
                  root / "control/n0_return.json", root / "control/pair_pin.json",
                  root / "control/AB_RECEIPT.json", root / "control/runtime_reference.json",
                  ctx / "evidence/author_arm.json"])
    put(folder / "source_manifest.json", {"files": [ref(p) for p in paths]})
    live = runtime_preflight(root, ctx, binary, mpi, prefix)
    approval = dict(schema="mixer_first8_execution_approval/1", gate="MAP_CASE_GO", execution_authorized=True,
                    case=CASE, case_dir=str(case), np=20, author_choices_confirmed=True, approved_concurrency=1,
                    wave_release=[CASE], runner_reviewed=True, walltime_approved=True, source_root=str(root/"B"),
                    source_pin=rotation["PIN_B"], minimum_free_bytes=base["FREE_BYTES"],
                    minimum_free_inodes=base["FREE_INODES"], campaign_policy=ref(policy), author_go=ref(auth),
                    qualification=ref(folder/"qualification.json"), policy=ref(folder/"policy.json"),
                    mxd2r_disposition=ref(folder/"mxd2r_disposition.json"), live_preflight=ref(live),
                    source_manifest=ref(folder/"source_manifest.json"), binary=ref(binary), mpi_launcher=ref(mpi),
                    runner_bindings=dict(python=str(python), job_start=str(here/"job_start.py.txt"),
                                         stdout=str(case/"slurm.stdout"), stderr=str(case/"slurm.stderr"),
                                         walltime=rotation["WALL"]))
    submit, ap, runner = here / "submit_one.py.txt", folder / "approval.json", folder / "runner.sbatch"
    with runner.open("x", encoding="utf-8", newline="\n") as out:
        out.write(runpy.run_path(str(submit))["canonical_runner"](approval, str(ap)))
    approval["runner"] = ref(runner)
    put(ap, approval)
    return submit, ap


def collect(root, role, jid, acct, runtime, live, pin):
    case_name(role)
    terminal = base["terminal"](acct, jid)
    need(terminal is not None, "job is not accounted terminal")
    ctx = root / "arms/U"
    with b1["collection_lease"](ctx):
        need(not (ctx / "return.json").exists(), "return already exists")
        return collect_terminal(root, ctx, jid, acct, terminal, runtime, live, pin)


def collect_terminal(root, ctx, jid, acct, terminal, runtime, live, pin):
    here = root / "B" / F8
    case = here / "cases" / CASE
    name = "collection_" + str(time.time_ns())
    start = time.time()
    error = None
    try:
        match = base["runtime"](ctx, *runtime, name + "_post")["matches"]
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        match, error = False, str(exc)
    finish = time.time()
    end = read(case / "job_end.json") if (case / "job_end.json").is_file() else {}
    frames = [p.name for p in (case / "post").glob("mix_*.liggghts")]
    exact = rotation["frames_ok"](frames)
    ready = bool(exact and match and rotation["completed"](acct, jid, end))
    w9 = b1["w9_status"](match, live, end.get("end_unix"), start)
    record = dict(label="DEVELOPMENT_DATA_ONLY", case=CASE, role="U", release_pin=pin, job_id=jid,
                  scheduler=terminal, runner_rc=end.get("returncode"), job_end_id=end.get("job_id"),
                  frame_count=len(frames), exact_frame_names=exact, return_ready=ready, post_runtime_matches=match,
                  w9=w9, post_runtime_error=error, post_start_unix=start, post_finished_unix=finish,
                  job_end_unix=end.get("end_unix"))
    put(ctx / "evidence" / (name + ".json"), record)
    out = ctx / name
    out.mkdir()
    with tarfile.open(out / ARCHIVES[1], "x:gz", compresslevel=1) as tar:
        for path in sorted(case.rglob("*")):
            need(not path.is_symlink() and (path.is_file() or path.is_dir()), "nonregular result")
            if path.is_file():
                tar.add(path, CASE + "/" + path.relative_to(case).as_posix(), recursive=False)
    with tarfile.open(out / ARCHIVES[0], "x:gz", compresslevel=1) as tar:
        for rel in ("control/pair_pin.json", "control/pair_authority.json", "B_manifest.json"):
            tar.add(root / rel, rel)
        tar.add(ctx / "evidence", "evidence")
        for rel in ("campaign_policy.json", "approvals/" + CASE, "admission"):
            tar.add(here / rel, rel)
    hashes = {n: sha(out / n) for n in ARCHIVES}
    with (out / "SHA256SUMS").open("x", encoding="ascii") as f:
        for n, digest in hashes.items():
            f.write(digest + "  " + n + "\n")
    b1["publish_return"](ctx, dict(record, directory=name, archive_hashes=hashes))
    print("JOB_ID=%s RUNNER_RC=%s F=%d W9=%s RETURN_READY=%s" %
          (jid, record["runner_rc"], len(frames), w9, str(ready).upper()), flush=True)
    return 0 if ready else 1


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("role", choices=("U",))
    p.add_argument("action", choices=(TOKEN, "collect"))
    for key in ("root", "prior-root", "binary", "mpi", "prefix"):
        p.add_argument("--" + key, type=Path, required=True)
    args = p.parse_args()
    root = args.root.resolve(strict=True)
    runtime = tuple(path.resolve(strict=True) for path in (args.binary, args.mpi, args.prefix))
    need(sys.platform.startswith("linux"), "Linux required")
    need(not any(k.startswith(("SBATCH_", "SLURM_", "SALLOC_", "SRUN_")) for k in os.environ),
         "inherited scheduler options or allocation")
    keep = {k: os.environ[k] for k in ("PATH", "HOME", "USER", "LOGNAME", "LANG", "LC_ALL", "TMPDIR")
            if k in os.environ}
    os.environ.clear()
    os.environ.update(keep)
    pin = read(root / "control/pair_pin.json")
    need(re.fullmatch("[0-9a-f]{40}", pin["commit"]) and set(pin["controllers"]) == set(CONTROLLERS)
         and all(sha(HERE / n) == pin["controllers"][n] for n in CONTROLLERS), "controller identity")
    live = args.action != "collect"
    if live:
        submit, ap = prepare(root, args.prior_root, args.role, args.action, pin["commit"], runtime)
        reply = base["command"]([sys.executable, "-I", "-B", str(submit), str(ap)], 90)
        put(root / "arms/U/evidence/submit.json", dict(rc=reply.returncode, stdout=reply.stdout, stderr=reply.stderr))
        print("SUBMIT_RC=" + str(reply.returncode), flush=True)
        need(reply.returncode == 0, "submission failed or uncertain; no automatic retry")
    case = root / "B" / F8 / "cases" / CASE
    receipt = read(case / "submission.receipt.json")
    jid = str(receipt["job_id"])
    need(receipt["case"] == CASE and receipt["state"] == "SUBMITTED"
         and re.fullmatch("[1-9][0-9]*", jid), "no confirmed B2-U job")
    print("JOB_ID=" + jid, flush=True)
    acct = rotation["monitor"](case, jid) if live else rotation["account"](jid)
    return collect(root, args.role, jid, acct, runtime, live, pin["commit"])


if __name__ == "__main__":
    raise SystemExit(main())

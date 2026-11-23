"""Run a single author-approved B2-C development rotation from an isolated installation."""
import argparse
import hashlib
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
u_completion = runpy.run_path(str(HERE / "mixer_b2_u_completion.py"))
PAIR_SHA = "6fb926e4a0fbe2b536acccb90cf10e440da2d064611cf0b0bc913a341d8f0f1a"
CASE = "PRECAL_R1_B2_C"
TOKEN = "GO_B2_C_ONCE"
PARALLEL_TOKEN = "GO_B2_C_PARALLEL_ONCE"
PARALLEL_DISPOSITION = "B2_U_TERMINAL_AND_W9_WAIVED_20261123"
DECK = "d36d199388243ccd630cbd346cbcdb6f37bf8bb92ae9c8f4e73e2e98597a6a3e"
META = "18f2e3cb3d83e6402a128acd2d0172813505fd34f1b8d17aa4067569728535eb"
ARCHIVES = ("b2_report.tar.gz", "b2_full_result.tar.gz")
CONTROLLERS = ("mixer_b2_c_ibb.py", "mixer_b2_u_completion.py", "mixer_b2_u_ibb.py", "mixer_b1_pair_ibb.py",
               "mixer_rotation_n0_ibb.py", "mixer_e0_pilot_ibb.py")
PARALLEL_CONTROLLERS = CONTROLLERS + ("mixer_b2_c_parallel_ibb.py", "mixer_b2_c_parallel_capacity.py")
runtime_preflight = b1["runtime_preflight"]


def case_name(role):
    need(role == "C", "only B2-C is authorized")
    return CASE


def author_token(role, token, parallel=False):
    case_name(role)
    need(token == (PARALLEL_TOKEN if parallel else TOKEN), "explicit B2-C author GO required")


def authority(pin, previous, parallel=False):
    grant = dict(label="DEVELOPMENT_DATA_ONLY", release_pin=pin, author_action=TOKEN,
                 allowed_to_submit=[CASE], execution_authorized=True, runtime_concurrency=1,
                 asset_manifest=b1["B_MANIFEST"], previous=previous,
                 automatic_retry=False, paper_qualified=False)
    if parallel:
        grant.update(author_action=PARALLEL_TOKEN, runtime_concurrency=2, peer_admission=PARALLEL_DISPOSITION)
    return grant


def acknowledged_peer(prior_root):
    """Bind the original acknowledged U job to its immutable approval and author release."""
    u_case, u_job, u_pin = (u_completion[key] for key in ("U_CASE", "U_JOB", "U_PIN"))
    site = prior_root / "B" / F8
    paths = dict(submission=site/"cases"/u_case/"submission.receipt.json",
                 approval=site/"approvals"/u_case/"approval.json",
                 release=prior_root/"control/pair_pin.json", authority=prior_root/"control/pair_authority.json")
    refs = {}
    records = {}
    for key, path in paths.items():
        need(path.resolve(strict=True) == path.absolute() and path.is_file(), "linked B2-U " + key)
        raw = path.read_bytes()
        refs[key] = {"path":str(path.resolve()), "sha256":hashlib.sha256(raw).hexdigest()}
        records[key] = json.loads(raw)
    submitted, approval, go = (records[key] for key in ("submission", "approval", "authority"))
    need(records["release"].get("commit") == u_pin and go.get("release_pin") == u_pin
         and go.get("author_action") == "GO_B2_U_ONCE" and go.get("allowed_to_submit") == [u_case]
         and go.get("execution_authorized") is True, "B2-U original release or authority differs")
    need(approval.get("case") == u_case and approval.get("np") == 20
         and approval.get("wave_release") == [u_case] and approval.get("execution_authorized") is True
         and approval.get("author_go") == refs["authority"], "B2-U original approval differs")
    need(submitted.get("case") == u_case and str(submitted.get("job_id")) == u_job
         and submitted.get("state") == "SUBMITTED" and type(submitted.get("returncode")) is int
         and submitted["returncode"] == 0 and submitted.get("approval_sha256") == refs["approval"]["sha256"],
         "B2-U original submission differs")
    return dict(evidence_type="SUBMISSION_ACKNOWLEDGEMENT", release_pin=u_pin, job_id=u_job,
                case=u_case, files=refs)


def prepare(root, prior_root, role, token, pin, runtime, parallel=False):
    author_token(role, token, parallel)
    here_root, prior_root = root.resolve(), prior_root.resolve()
    need(here_root != prior_root and here_root not in prior_root.parents and prior_root not in here_root.parents,
         "B2 requires its own installation")
    original_pair = root / "control/b1_pair_readback.json"
    need(sha(original_pair) == PAIR_SHA, "B1 pair readback identity")
    if parallel:
        proof = root / "control/b2_u_submission.json"
        acknowledgement = acknowledged_peer(prior_root)
        put(proof, acknowledgement)
        peer = dict(ref(proof), evidence_type=acknowledgement["evidence_type"],
                    case=acknowledgement["case"], job_id=acknowledgement["job_id"])
        prior_refs = list(acknowledgement["files"].values())
    else:
        proof = root / "control/b2_u_return.json"
        peer = ref(u_completion["verify_original"](prior_root, proof))
        prior_refs = [peer]
    manifest_path = root / "B_manifest.json"
    need(sha(manifest_path) == b1["B_MANIFEST"], "B manifest identity")
    manifest = base["verify_deployment"](root)
    need(manifest["source_pin"] == rotation["PIN_B"] and len(manifest["files"]) == 283
         and manifest["approved_return_sha256"] == rotation["A_B_RETURN"], "B provenance")
    here = root / "B" / F8
    assets = here / "planned_assets" / CASE
    need(sha(assets / "in.mixer") == DECK and sha(assets / "deck_meta.json") == META, "B2-C assets")
    need(sha(root / "control/n0_return.json") == b1["N0_POINTER"], "N0 receipt identity")
    ctx = root / "arms/C"
    ctx.mkdir(parents=True, exist_ok=False)
    (ctx / "control").mkdir()
    (ctx / "evidence").mkdir()
    auth = root / "control/pair_authority.json"
    grant = authority(pin, peer, parallel)
    put(auth, grant)
    policy = here / "campaign_policy.json"
    campaign = base["policy"](str(here), sha(auth))
    campaign["max_concurrency"] = grant["runtime_concurrency"]
    put(policy, campaign)
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
    put(folder / "policy.json", dict(policy_id="B2_C_DEVELOPMENT_ONLY", execution_authorized=True,
                                     allowed_to_submit=[CASE]))
    put(folder / "mxd2r_disposition.json", dict(scope="one B2-C development arm", E0_known_limit="MXE0-02",
                                               paper_release=False))
    python = Path(sys.executable).resolve(strict=True)
    binary, mpi, prefix = runtime
    paths = [root / "B" / base["safe_rel"](row["path"]) for row in manifest["files"]]
    paths.extend(case / n for n in parts)
    paths.extend(HERE / n for n in (PARALLEL_CONTROLLERS if parallel else CONTROLLERS))
    paths.extend([python, auth, original_pair, proof, manifest_path,
                  root / "control/n0_return.json", root / "control/pair_pin.json",
                  root / "control/AB_RECEIPT.json", root / "control/runtime_reference.json",
                  ctx / "evidence/author_arm.json"])
    put(folder / "source_manifest.json", {"files": [ref(p) for p in paths] + prior_refs})
    if parallel:
        capacity = runpy.run_path(str(HERE / "mixer_b2_c_parallel_capacity.py"))
        live = capacity["preflight"](root, ctx, binary, mpi, prefix, prior_root)
    else:
        live = runtime_preflight(root, ctx, binary, mpi, prefix)
    approval = dict(schema="mixer_first8_execution_approval/1", gate="MAP_CASE_GO", execution_authorized=True,
                    case=CASE, case_dir=str(case), np=20, author_choices_confirmed=True,
                    approved_concurrency=grant["runtime_concurrency"],
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


def collect(root, role, jid, acct, runtime, live, pin, parallel=False):
    case_name(role)
    terminal = base["terminal"](acct, jid)
    need(terminal is not None, "job is not accounted terminal")
    ctx = root / "arms/C"
    with b1["collection_lease"](ctx):
        need(not (ctx / "return.json").exists(), "return already exists")
        return collect_terminal(root, ctx, jid, acct, terminal, runtime, live, pin, parallel)


def collect_terminal(root, ctx, jid, acct, terminal, runtime, live, pin, parallel=False):
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
    record = dict(label="DEVELOPMENT_DATA_ONLY", case=CASE, role="C", release_pin=pin, job_id=jid,
                  scheduler=terminal, runner_rc=end.get("returncode"), job_end_id=end.get("job_id"),
                  frame_count=len(frames), exact_frame_names=exact, return_ready=ready, post_runtime_matches=match,
                  w9=w9, post_runtime_error=error, post_start_unix=start, post_finished_unix=finish,
                  job_end_unix=end.get("end_unix"))
    if parallel:
        record["peer_admission"] = PARALLEL_DISPOSITION
    put(ctx / "evidence" / (name + ".json"), record)
    out = ctx / name
    out.mkdir()
    with tarfile.open(out / ARCHIVES[1], "x:gz", compresslevel=1) as tar:
        for path in sorted(case.rglob("*")):
            need(not path.is_symlink() and (path.is_file() or path.is_dir()), "nonregular result")
            if path.is_file():
                tar.add(path, CASE + "/" + path.relative_to(case).as_posix(), recursive=False)
    with tarfile.open(out / ARCHIVES[0], "x:gz", compresslevel=1) as tar:
        peer_file = "control/b2_u_submission.json" if parallel else "control/b2_u_return.json"
        for rel in ("control/pair_pin.json", "control/pair_authority.json", peer_file, "B_manifest.json"):
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


def main(parallel=False):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("role", choices=("C",))
    p.add_argument("action", choices=(PARALLEL_TOKEN if parallel else TOKEN, "collect"))
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
    controllers = PARALLEL_CONTROLLERS if parallel else CONTROLLERS
    need(re.fullmatch("[0-9a-f]{40}", pin["commit"]) and set(pin["controllers"]) == set(controllers)
         and all(sha(HERE / n) == pin["controllers"][n] for n in controllers), "controller identity")
    live = args.action != "collect"
    if live:
        submit, ap = prepare(root, args.prior_root, args.role, args.action, pin["commit"], runtime, parallel)
        reply = base["command"]([sys.executable, "-I", "-B", str(submit), str(ap)], 90)
        put(root / "arms/C/evidence/submit.json", dict(rc=reply.returncode, stdout=reply.stdout, stderr=reply.stderr))
        print("SUBMIT_RC=" + str(reply.returncode), flush=True)
        need(reply.returncode == 0, "submission failed or uncertain; no automatic retry")
    case = root / "B" / F8 / "cases" / CASE
    receipt = read(case / "submission.receipt.json")
    jid = str(receipt["job_id"])
    need(receipt["case"] == CASE and receipt["state"] == "SUBMITTED"
         and re.fullmatch("[1-9][0-9]*", jid), "no confirmed B2-C job")
    print("JOB_ID=" + jid, flush=True)
    acct = rotation["monitor"](case, jid) if live else rotation["account"](jid)
    return collect(root, args.role, jid, acct, runtime, live, pin["commit"], parallel)


if __name__ == "__main__":
    raise SystemExit(main())


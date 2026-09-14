"""R5 numerical-workflow fixtures; no target sources or user data are changed.

Exit 0 means the documented counterexamples/controls were reproduced, not GO.
The concurrency schedule only pauses the unmodified metadata writer between its
run-ID check and its Python write. The two profile commands use synthetic fits.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
from unittest.mock import patch


def wait_file(path):
    deadline = time.monotonic() + 30
    while not path.exists():
        if time.monotonic() > deadline:
            raise TimeoutError(str(path))
        time.sleep(.01)


def profile(target, output, role):
    import numpy as np
    sys.path.insert(0, str(target))
    from bms_balancing import verify as v
    center = (v.LB5 + v.UB5) / 2
    selected = v.LB5[:4] + (.25 if role == "A" else .75) * (v.UB5[:4] - v.LB5[:4])

    class Obj:
        c_cell = 1.0
        scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}

        def __call__(self, p):
            return float(1 + 1e-4 * np.square(np.asarray(p) - center).sum())

        def rmse_pocv(self, p):
            return self(p)

    def successful(fun, start, **kwargs):
        return SimpleNamespace(x=selected.copy(), fun=fun(selected), success=True)

    with patch.object(v.D, "data_root", return_value=output.parent), \
         patch.object(v, "build", return_value=Obj()), \
         patch.object(v, "multistart", return_value=(center.copy(), 1., [])), \
         patch.object(v, "minimize", side_effect=successful):
        return v.main(["profile", "--data-root", str(output.parent), "--starts", "1",
                       "--grid", "2", "--out", str(output)])


def helpers(target):
    text = (target / "scripts/run_states.sh").read_text(encoding="utf-8")
    return (text[text.index("write_meta ()"):text.index('\nmkdir -p "$OUT"')]
            + "\n" + text[text.index("say ()"):text.index("\nfail=0")])


def fixture_repo(target, root):
    (root / "scripts").mkdir()
    (root / "out").mkdir()
    shutil.copyfile(target / "scripts/provenance.py", root / "scripts/provenance.py")
    (root / "code.py").write_text("value = 1\n", encoding="utf-8")
    git = ["git", "-C", str(root)]
    subprocess.run(git + ["init", "-q"], check=True, capture_output=True)
    subprocess.run(git + ["add", "."], check=True, capture_output=True)
    subprocess.run(git + ["-c", "user.name=R5 Fixture", "-c", "user.email=r5@example.invalid",
                          "commit", "-qm", "synthetic fixture"], check=True, capture_output=True)


def env_for(root):
    return dict(os.environ, STARTS="1", SI="Li", BMS_DATA_ROOT="synthetic", OUT=str(root / "out"),
                REAL_PY=sys.executable, REPRO=str(Path(__file__).resolve()), FIXTURE=str(root))


def metadata_race(target, root):
    fixture_repo(target, root)
    output = root / "out/profile.csv"
    # A is paused AFTER the shell's grep succeeded, before the metadata Python
    # process starts. No target check, payload, or writer is replaced.
    schedule = '''
python3 () {
  if [ "$1" = "-" ] && [ "$ROLE" = "A" ]; then
    "$REAL_PY" "$REPRO" --pause "$FIXTURE/A.meta.ready" --until "$FIXTURE/B.done"
  fi
  "$REAL_PY" "$@"
}
'''
    body = '''
run "profile $ROLE" "$1" - "$2" "$REAL_PY" "$REPRO" --target "$3" --worker "$ROLE" --out "$1" \
  && write_meta "$1" 100 GITT && printf 'WRITER %s %s\n' "$ROLE" "$LAST_RUN_ID"
'''
    commands = ["bash", "-c", schedule + helpers(target) + body, "r5", str(output)]
    a = subprocess.Popen(commands + [str(root / "A.log"), str(target)], cwd=root,
                         env=dict(env_for(root), ROLE="A"), stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True)
    b = None
    try:
        wait_file(root / "A.meta.ready")
        a_rows = list(csv.DictReader(output.open(encoding="utf-8")))
        b = subprocess.Popen(commands + [str(root / "B.log"), str(target)], cwd=root,
                             env=dict(env_for(root), ROLE="B"), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
        bo, be = b.communicate(timeout=30)
        b_meta = json.loads(Path(str(output) + ".meta.json").read_text(encoding="utf-8"))
        (root / "B.done").write_text("done", encoding="utf-8")
        ao, ae = a.communicate(timeout=30)
    finally:
        for process in (a, b):
            if process is not None and process.poll() is None:
                process.terminate()
                process.wait(timeout=5)
    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    meta = json.loads(Path(str(output) + ".meta.json").read_text(encoding="utf-8"))
    aid, bid = a_rows[0]["run_id"], rows[0]["run_id"]
    assert a.returncode == b.returncode == 0, (ao, ae, bo, be)
    assert aid != bid and meta["run_id"] == aid and b_meta["run_id"] == bid
    assert {r["run_id"] for r in rows} == {bid}
    assert float(a_rows[0]["a_NE"]) != float(rows[0]["a_NE"])
    return {"A_rc": a.returncode, "B_rc": b.returncode,
            "A_run_id": aid, "B_run_id": bid, "final_artifact_run_id": bid,
            "final_meta_run_id": meta["run_id"], "A_a_NE": a_rows[0]["a_NE"],
            "final_B_a_NE": rows[0]["a_NE"], "before_A_resumes_pair_is_consistent": True,
            "A_stdout": ao, "A_stderr": ae, "B_stdout": bo, "B_stderr": be,
            "schedule": "A publishes/validates A, pauses after write_meta grep; B publishes/validates/writes B metadata; A writes A metadata."}


def default_ids(target, root):
    output = root / "profile.csv"
    captured = io.StringIO()
    with patch.dict(os.environ):
        os.environ.pop("BMS_RUN_ID", None)
        with contextlib.redirect_stdout(captured):
            rc = profile(target, output, "A")
    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    ids = [r["run_id"] for r in rows]
    printed_id = captured.getvalue().strip().splitlines()[-1].split("run_id ")[1].rstrip(")")
    assert rc == 0 and len(ids) == 2 and len(set(ids + [printed_id])) == 3
    with patch.dict(os.environ, BMS_RUN_ID="explicit-attempt"), contextlib.redirect_stdout(io.StringIO()):
        control = profile(target, output, "A")
    explicit = list(csv.DictReader(output.open(encoding="utf-8")))
    assert control == 0 and {r["run_id"] for r in explicit} == {"explicit-attempt"}
    return {"default_rc": rc, "row_run_ids": ids, "printed_run_id": printed_id,
            "distinct_ids_in_one_attempt": 3, "explicit_env_control_consistent": True,
            "scope": "Actual profile CLI dispatcher; synthetic successful fits; default UUID not cached per command."}


def membership_not_schema(target, root):
    fixture_repo(target, root)
    output = root / "out/profile.csv"
    producer = ("import csv,os,sys; f=open(sys.argv[1],'w',newline=''); "
                "w=csv.writer(f); w.writerow(['gamma_Si','obj','run_id','note']); "
                "w.writerow([0,1,'previous-attempt',os.environ['BMS_RUN_ID']]); f.close()")
    body = '\nrun "schema probe" "$1" - "$2" "$REAL_PY" -c "$3" "$1" && write_meta "$1" 100 GITT\n'
    r = subprocess.run(["bash", "-c", helpers(target) + body, "r5", str(output), str(root / "run.log"), producer],
                       cwd=root, env=env_for(root), capture_output=True, text=True)
    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    meta = json.loads(Path(str(output) + ".meta.json").read_text(encoding="utf-8"))
    assert r.returncode == 0 and rows[0]["run_id"] != meta["run_id"] == rows[0]["note"]
    return {"rc": r.returncode, "artifact_run_id": rows[0]["run_id"], "meta_run_id": meta["run_id"],
            "matched_unrelated_note": rows[0]["note"], "stderr": r.stderr,
            "scope": "Helper contract probe with synthetic CSV; not a claim current optimizer emits such a note."}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", type=Path)
    p.add_argument("--worker", choices=["A", "B"])
    p.add_argument("--out", type=Path)
    p.add_argument("--pause", type=Path)
    p.add_argument("--until", type=Path)
    args = p.parse_args()
    if args.pause:
        args.pause.write_text("ready", encoding="utf-8")
        wait_file(args.until)
        return 0
    target = args.target.resolve()
    if args.worker:
        return profile(target, args.out, args.worker)
    os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")
    results = {}
    with tempfile.TemporaryDirectory(prefix="harness-r5-execution-") as d:
        for name, fn in (("metadata_race", metadata_race), ("default_attempt_ids", default_ids),
                         ("membership_not_schema", membership_not_schema)):
            root = Path(d) / name
            root.mkdir()
            results[name] = fn(target, root)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""R4 scientific workflow review: isolated output/provenance fixtures only.

No reviewed sources, user datasets, or remote services are modified.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import importlib.util
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


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def wait_file(path):
    deadline = time.monotonic() + 15
    while not path.exists():
        if time.monotonic() > deadline:
            raise TimeoutError(str(path))
        time.sleep(.01)


def profile_worker(target, output, role):
    import numpy as np
    sys.path.insert(0, str(target))
    from bms_balancing import verify as v
    center = (v.LB5 + v.UB5) / 2
    fraction = .25 if role == "A" else .75
    selected = v.LB5[:4] + fraction * (v.UB5[:4] - v.LB5[:4])

    class Obj:
        c_cell = 1.0
        scales = {"pocv": 1.0, "dvdq": 1.0, "dqdv": 1.0}
        def __call__(self, p):
            return float(1 + 1e-4 * np.square(np.asarray(p)-center).sum())
        def rmse_pocv(self, p):
            return self(p)

    def successful(fun, start, **kwargs):
        return SimpleNamespace(x=selected.copy(), fun=fun(selected), success=True)

    original_replace = os.replace
    root = output.parent

    def scheduled_replace(source, destination):
        # The profile has already CLOSED its .part output when it gets here.
        (root / (role + ".ready")).write_text("ready", encoding="utf-8")
        if role == "A":
            wait_file(root / "B.ready")
            original_replace(source, destination)
            (root / "A.published").write_text("published", encoding="utf-8")
        else:
            wait_file(root / "A.published")
            original_replace(source, destination)

    print(json.dumps({"role": role, "own_computed_a_NE": float(selected[2])}), flush=True)
    with patch.object(v.D, "data_root", return_value=root), \
         patch.object(v, "build", return_value=Obj()), \
         patch.object(v, "multistart", return_value=(center.copy(), 1.0, [])), \
         patch.object(v, "minimize", side_effect=successful), \
         patch.object(v.os, "replace", side_effect=scheduled_replace):
        return v.main(["profile", "--data-root", str(root), "--starts", "1", "--grid", "2",
                       "--out", str(output)])


def shared_part_race(target, root):
    output = root / "profile.csv"
    command = [sys.executable, str(Path(__file__).resolve()), "--target", str(target), "--out", str(output)]
    a = subprocess.Popen(command + ["--worker", "A"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    b = None
    try:
        wait_file(root / "A.ready")
        b = subprocess.Popen(command + ["--worker", "B"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ao, ae = a.communicate(timeout=20)
        bo, be = b.communicate(timeout=20)
    finally:
        for process in (a, b):
            if process is not None and process.poll() is None:
                process.terminate()
                process.wait(timeout=5)
    rows = list(csv.DictReader(output.open(encoding="utf-8")))
    aa = json.loads(ao.splitlines()[0])["own_computed_a_NE"]
    ba = json.loads(bo.splitlines()[0])["own_computed_a_NE"]
    observed = [float(row["a_NE"]) for row in rows]
    assert aa != ba and observed and all(x == ba for x in observed)
    assert a.returncode == 0 and b.returncode != 0 and "FileNotFoundError" in be
    return {"A_exit_code": a.returncode, "B_exit_code": b.returncode,
            "A_computed_a_NE": aa, "B_computed_a_NE": ba, "published_a_NE": observed,
            "A_published_B_rows": True, "A_stdout": ao, "B_stdout": bo,
            "A_stderr": ae, "B_stderr": be,
            "scope": "Actual profile writer; synthetic successful fits; deterministic pause only at os.replace boundary."}


def helpers(target):
    text = (target / "scripts/run_states.sh").read_text(encoding="utf-8")
    return text[text.index("say ()"):text.index("\nfail=0")]


def freshness_touch(target, root):
    output = root / "old_profile.csv"
    output.write_text("gamma_Si,obj\n0,1\n", encoding="utf-8")
    before = hashlib.sha256(output.read_bytes()).hexdigest()
    old = time.time()-60
    os.utime(output, (old, old))
    script = helpers(target) + '\nrun "freshness probe" "$1" - "$2" "$3" -c "$4" "$1"\n'
    noop = subprocess.run(["bash", "-c", script, "r4", str(output), str(root/"noop.log"),
                           sys.executable, "pass"], capture_output=True, text=True)
    touched = subprocess.run(["bash", "-c", script, "r4", str(output), str(root/"touch.log"),
                              sys.executable, "import pathlib,sys; pathlib.Path(sys.argv[1]).touch()"],
                             capture_output=True, text=True)
    assert noop.returncode != 0 and touched.returncode == 0 and "OK" in touched.stderr
    assert before == hashlib.sha256(output.read_bytes()).hexdigest()
    return {"noop_control_rc": noop.returncode, "touch_only_rc": touched.returncode,
            "old_bytes_sha256": before, "bytes_unchanged": True,
            "noop_stderr": noop.stderr, "touch_stderr": touched.stderr,
            "scope": "Question 4 helper boundary; no claim that current production optimizer calls touch."}


def provenance_sequence(target, root):
    (root / "scripts").mkdir()
    (root / "out").mkdir()
    shutil.copyfile(target / "scripts/provenance.py", root / "scripts/provenance.py")
    (root / "code.py").write_text("value = 1\n", encoding="utf-8")
    for state in ("100", "200"):
        (root / "out" / (state + ".csv")).write_text("a,b\n1,2\n", encoding="utf-8")
    git = ["git", "-C", str(root)]
    subprocess.run(git + ["init", "-q"], check=True, capture_output=True)
    subprocess.run(git + ["add", "."], check=True, capture_output=True)
    subprocess.run(git + ["-c", "user.name=R4 Fixture", "-c", "user.email=r4@example.invalid",
                          "commit", "-qm", "synthetic clean fixture"], check=True, capture_output=True)
    text = (target / "scripts/run_states.sh").read_text(encoding="utf-8")
    writer = text[text.index("write_meta ()"):text.index('\nmkdir -p "$OUT"')]
    script = 'STARTS=1\nSI=Li\nBMS_DATA_ROOT=synthetic\n' + writer + '\nwrite_meta "$1" "$2" GITT\n'
    result = []
    for state in ("100", "200"):
        output = root / "out" / (state + ".csv")
        output.write_text("a,b\n3,4\n", encoding="utf-8")
        call = subprocess.run(["bash", "-c", script, "r4", "out/"+state+".csv", state],
                              cwd=root, capture_output=True, text=True)
        assert call.returncode == 0, call.stderr
        meta = json.loads(output.with_name(output.name+".meta.json").read_text(encoding="utf-8"))
        result.append({"state":state, "git_dirty":meta["git_dirty"], "git_commit":meta["git_commit"]})
    assert result[0]["git_dirty"] is False and result[1]["git_dirty"] is True
    code_diff = subprocess.check_output(git + ["diff", "--", "code.py", "scripts/provenance.py"], text=True)
    assert code_diff == ""
    return {"sequential_artifact_metadata": result, "tracked_code_diff": code_diff,
            "changed_tracked_files": subprocess.check_output(git+["diff","--name-only"],text=True).splitlines(),
            "scope": "Actual write_meta helper in an isolated Git fixture; only two outputs rewritten."}


def c21_closure(target, root):
    sys.path.insert(0, str(target))
    test = module("r4_c21_tests", target/"tests/test_review_findings.py")
    shutil.copytree(target/"out/recompare", root/"out/recompare")
    shutil.copyfile(target/"FINDINGS.md", root/"FINDINGS.md")
    check = test.test_section_1_8_192_values_are_backed_by_committed_recompare_artifacts
    with patch.object(test,"ROOT",root):
        check()
        file=root/"out/recompare/dd_eval_pristine_Li_r2.csv"
        lines=file.read_text(encoding="utf-8").splitlines()
        header=next(i for i,line in enumerate(lines) if line.startswith("a_PE,"))
        fields=lines[header+1].split(",")
        fields[5]="9.0"
        lines[header+1]=",".join(fields)
        file.write_text("\n".join(lines)+"\n",encoding="utf-8")
        try:
            check()
        except AssertionError as exc:
            return {"original_passes":True,"R3_csv_9_regression_now_rejected":True,"assertion":str(exc)}
        raise AssertionError("R3 CSV-only mutation unexpectedly passed")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--target",type=Path,required=True)
    parser.add_argument("--worker",choices=["A","B"])
    parser.add_argument("--out",type=Path)
    args=parser.parse_args()
    target=args.target.resolve()
    if args.worker:
        return profile_worker(target,args.out,args.worker)
    env_path=str(Path(sys.executable).parent)
    os.environ["PATH"]=env_path+os.pathsep+os.environ.get("PATH","")
    result={}
    with tempfile.TemporaryDirectory(prefix="harness-r4-execution-") as directory:
        root=Path(directory)
        for key,function in (("shared_profile_part",shared_part_race),
                             ("touch_only_freshness",freshness_touch),
                             ("sequential_provenance",provenance_sequence),
                             ("C21_closure",c21_closure)):
            fixture=root/key
            fixture.mkdir()
            result[key]=function(target,fixture)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__=="__main__":
    sys.exit(main())

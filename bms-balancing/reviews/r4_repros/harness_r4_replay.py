"""Replay the R4 scientific review against its exact isolated Git revision.

Exit 0 confirms expected controls/counterexamples, NOT a model GO decision.
Requires Linux/WSL, target requirements, pytest, and the four sibling probes.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

COMMIT="39a5fe06215710b16e9b42bf3dc3c04c63cb8663"


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--target",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    target=args.target.resolve()
    here=Path(__file__).resolve().parent
    git=["git","-c","safe.directory="+str(target.parent),"-C",str(target.parent)]
    sha=subprocess.check_output(git+["rev-parse","HEAD"],text=True).strip()
    if sha!=COMMIT:
        raise SystemExit(f"Expected {COMMIT}; found {sha}")
    before=subprocess.check_output(git+["status","--porcelain","--","bms-balancing"],text=True)
    env=dict(os.environ)
    env["PATH"]=str(Path(sys.executable).parent)+os.pathsep+env.get("PATH","")
    env["PYTHONDONTWRITEBYTECODE"]="1"
    scripts=["harness_r4_port_repros.py","harness_r4_shape_repros.py",
             "harness_r4_inference_repros.py","harness_r4_execution_repros.py"]
    old="reviews/r3_repros/"
    commands=[
        ("baseline_pytest",[sys.executable,"-m","pytest","tests/","-q","-p","no:cacheprovider"],0),
        ("matlab_tests_available_stages",["bash","matlab/tests/run_all.sh"],0),
        ("compare_states",[sys.executable,"scripts/compare_states.py","pouch=out",
                           "fixedhc=out/cells_pouch_fixedhc","c168=out/cells_c168","c171=out/cells_c171"],0),
        ("old_R3_port",[sys.executable,old+"harness_r3_port_repros.py","--target",str(target)],1),
        ("old_R3_shape",[sys.executable,old+"harness_r3_shape_repros.py","--target",str(target)],1),
        ("old_R3_artifact",[sys.executable,old+"harness_r3_artifact_repros.py","--target",str(target)],1),
        ("old_R3_denominator",[sys.executable,old+"harness_r3_inference_repros.py","--root",str(target),"--case","denominator"],1),
        ("old_R3_noise",[sys.executable,old+"harness_r3_inference_repros.py","--root",str(target),"--case","noise"],0),
    ]
    commands += [(name,[sys.executable,str(here/script),"--target",str(target)],0)
                 for name,script in zip(("R4_port","R4_shape","R4_inference","R4_execution"),scripts)]
    runs=[]
    for name,command,expected in commands:
        start=time.monotonic()
        run=subprocess.run(command,cwd=target,env=env,capture_output=True,text=True,
                           encoding="utf-8",errors="replace",timeout=180)
        elapsed=round(time.monotonic()-start,3)
        runs.append({"case":name,"command":command,"exit_code":run.returncode,
                     "expected_exit_code":expected,"elapsed_seconds":elapsed,
                     "stdout":run.stdout,"stderr":run.stderr})
        print(f"{name}: rc={run.returncode}, expected={expected}, {elapsed}s",flush=True)
        # Preserve an actual Windows-checkout shell failure, then test an
        # isolated copy with only shell line endings normalized. Never edit
        # the review target or turn the original failure into a claimed pass.
        if (name=="matlab_tests_available_stages" and run.returncode==2
                and b"\r\n" in (target/"matlab/tests/run_all.sh").read_bytes()):
            with tempfile.TemporaryDirectory(prefix="harness-r4-lf-") as temporary:
                copy=Path(temporary)/"bms-balancing"
                subprocess.run(["cp","-a",str(target),str(copy)],check=True)
                shell_files=[str(p) for p in copy.rglob("*.sh")]
                subprocess.run(["sed","-i","s/\r$//",*shell_files],check=True)
                retry_cmd=["bash","matlab/tests/run_all.sh"]
                start_lf=time.monotonic()
                retry=subprocess.run(retry_cmd,cwd=copy,env=env,capture_output=True,
                                     text=True,encoding="utf-8",errors="replace",timeout=180)
                if retry.returncode==0:
                    runs[-1]["environment_failure_resolved_by"]="matlab_tests_LF_copy"
                runs.append({"case":"matlab_tests_LF_copy","command":retry_cmd,
                             "exit_code":retry.returncode,"expected_exit_code":0,
                             "elapsed_seconds":round(time.monotonic()-start_lf,3),
                             "stdout":retry.stdout,"stderr":retry.stderr,
                             "scope":"Temporary copy of target; only .sh CRLF->LF conversion; original direct rc2 retained."})
                print(f"matlab_tests_LF_copy: rc={retry.returncode}, expected=0",flush=True)
    after=subprocess.check_output(git+["status","--porcelain","--","bms-balancing"],text=True)
    result={"meaning":"Expected codes include reproduced defects and old assertions that now fail; this is not GO.",
            "reviewed_commit":sha,"target":str(target),
            "recorded_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "python":sys.version,
            "packages":{p:importlib.metadata.version(p) for p in ("numpy","scipy","pandas","openpyxl","pytest")},
            "review_script_sha256":{p:hashlib.sha256((here/p).read_bytes()).hexdigest() for p in scripts},
            "tracked_target_before":before,"tracked_target_after":after,"runs":runs}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return int(before!=after or any(r["exit_code"]!=r["expected_exit_code"]
               and not r.get("environment_failure_resolved_by") for r in runs))


if __name__=="__main__":
    sys.exit(main())

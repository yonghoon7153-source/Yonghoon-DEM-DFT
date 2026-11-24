"""Build the proposed WSL30 roster solely from the sealed cohort and value-blind receipts."""
import argparse
import ast
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

HERE = Path(__file__).resolve().parent
BASE = "132f250ef2f56d1b7f88fe46b85600f2c9f926c4"
REPORTS = {"result_20261124_1933.txt":"8dede0754d3bafad68be8fe542890fc0d8856b4dc6bd03fa6443792ef4d92fd2",
           "result_b_20261124_1936.txt":"5be01e8a048ad34d9fffd42c6200fc6e27c9bd5c8a06562e0b397ecb09a88840"}
COHORT = "docs/data/area_s2_cohort.tsv"
PLAN = "docs/reviews/lhs_v13_preparation_20261118/wsl30_access_plan.tsv"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_tsv(data):
    return list(csv.DictReader((s for s in io.StringIO(data.decode("utf8")) if not s.startswith("#")), delimiter="\t"))


def build(repo):
    def blob(path):
        return subprocess.check_output(["git","-c","safe.directory="+repo.as_posix(),"-C",str(repo),
                                        "show",BASE+":"+path])
    cohort_raw = blob(COHORT)
    cohort = {r["case"]:r for r in read_tsv(cohort_raw)}
    plan = {r["case_alias"]:r for r in read_tsv(blob(PLAN))}
    raw = {k:(HERE/"evidence"/k).read_bytes() for k in REPORTS}
    assert {k:sha(v) for k,v in raw.items()} == REPORTS
    primary, followup = [b.decode("utf8") for b in raw.values()]
    lines = primary.splitlines()
    assert len(lines)==31 and "OK 0 / 30 · CHECK 30" in lines[-1]
    assert "전체 19/30 · 덱 줄 자리만 30/30" in followup
    cases = [f"lhs00_{n}" for n in range(100,130)]
    assert set(plan)==set(cases)
    roster = []
    for case,line in zip(cases,lines[:-1],strict=True):
        c = cohort[case]
        prev = plan[case]
        assert line.startswith(case+"  banner 1/1 · Finished 1 · ") and line.endswith(" · CHECK")
        hits = re.search(r"압력줄 (\d+)/(\d+) 같음=Y \(([0-9a-f]{12})\)",line)
        endpoint = re.search(r"하베스트 step (\d+) \(lig 범위 Y · txt 범위 Y · 정확히 Y\)",line)
        assert hits and hits[1]==hits[2]==prev["candidate_b7_count"]==prev["comparison_b7_count"]
        assert endpoint and endpoint[1]==c["step_atom"]==c["step_contact"] and c["step_gap"]=="0"
        assert c["status"]=="RAW_OK" and c["deck_sha256"]==prev["current_deck_sha256"]
        assert "덱 100/128 (include 0 · 없는 include 0) · 덱 지문=코호트 Y" in line and "atom 지문=코호트 Y" in line
        deck = PurePosixPath(c["deck"]).name
        atom = PurePosixPath(c["atom_file"]).name
        assert deck == f"input_{case}.liggghts" and atom == f"atom_{endpoint[1]}.liggghts"
        roster.append(dict(case=case,run_segment=case+"/run1",canonical_log="log.liggghts",
            comparison_log="log.txt",deck=deck,deck_sha256=c["deck_sha256"],harvest_step=int(endpoint[1]),
            atom=atom,atom_sha256=c["atom_sha256"],b7_line_count=int(hits[1]),b7_lines_sha256_prefix12=hits[3]))
    return dict(schema="wsl30_pressure_freeze_draft/1",date="2026-11-24",cohort_source=COHORT,
                cohort_sha256=sha(cohort_raw),reports_sha256=REPORTS,historical_b7_refusal="PRESERVED",
                canonical_route="A",value_access="AWAITING_AUTHOR_GO",result_rows=0,roster=roster)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo",type=Path)
    p.add_argument("--check",action="store_true")
    p.add_argument("--author-script-dir",type=Path,help="optional location of the two provenance scripts; never executed")
    a=p.parse_args()
    proposal=build(a.repo.resolve())
    if a.author_script_dir:
        first=(a.author_script_dir/"check_wsl30.py").read_bytes()
        second=(a.author_script_dir/"check_wsl30_b.py").read_bytes()
        assert sha(first)=="04f1c4bdd49396b3e8c1d24837443d3d7afe26155888eb53bb024b769828e782"
        assert sha(second)=="0ff5b548a645e2811ede1b06b25e15fa4a50b88d2b77d43eefe2db0820a8f60b"
        entries=[ast.literal_eval(node.value) for node in ast.parse(first).body if isinstance(node,ast.Assign)
                 and any(isinstance(t,ast.Name) and t.id=="COHORT" for t in node.targets)]
        expected={r["case"]:(r["harvest_step"],r["deck_sha256"],r["atom_sha256"]) for r in proposal["roster"]}
        assert entries==[expected]
        print("AUTHOR_STATIC_COHORT_30_OF_30")
    data=(json.dumps(proposal,indent=2,ensure_ascii=False)+"\n").encode("utf8")
    path=HERE/"roster.json"
    if a.check:
        if path.read_bytes()!=data:
            raise SystemExit("roster mismatch")
    else:
        with path.open("xb") as f:
            f.write(data)
    print("ROSTER_BOUND=30 PRESSURE_RESULTS=0")

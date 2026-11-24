"""Author-only read of the single canonical WSL30 log using the original B7 pressure reader."""
import argparse
import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROSTER_SHA = "407d03aa2a2cd1ea2ff6c5e95de336af77de61d00cf19d35302c5c6bf3e01e81"
GO = "GO_LHS_WSL30_SECTION5_PRESSURE_ONCE"
BANNER = re.compile(r"^\s*LIGGGHTS \(Version")
STEP = re.compile(r"^\s*(\d+)\s+\S")
sys.path.insert(0, str(HERE/"b7"))
import lhs_pressure_record as b7


class SourceMismatch(ValueError):
    pass


def require(condition, reason):
    if not condition:
        raise SourceMismatch(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def canonical_check(raw, row):
    lines = [s.rstrip() for s in raw.decode("utf8", "surrogateescape").splitlines()]
    banners = [i for i,s in enumerate(lines) if BANNER.match(s)]
    require(len(banners) == 1, "RUN_SEGMENT")
    finishes = [i for i,s in enumerate(lines) if "Finished!" in s
                and not s.lstrip().startswith(("print ", "print\t", "#"))]
    require(len(finishes) == 1 and finishes[0] > banners[0], "RUN_FINISH")
    rows = []
    harvest_found = False
    for i,s in enumerate(lines):
        if s.lstrip().startswith("Current Pressure:"):
            require(banners[0] < i < finishes[0] and b7.PRESS_LINE.match(s), "B7_LINE_SHAPE_OR_SEGMENT")
            rows.append(s)
        if banners[0] < i < finishes[0]:
            step = STEP.match(s)
            if step and int(step[1]) == row["harvest_step"]:
                harvest_found = True
    fingerprint = digest("\n".join(rows).encode("utf8","surrogateescape"))
    require(len(rows) == row["b7_line_count"] and len(rows)>0 and
            fingerprint[:12] == row["b7_lines_sha256_prefix12"], "REPORTED_B7_SEQUENCE")
    require(harvest_found, "HARVEST_STEP_MARKER")
    return fingerprint


def assess(root, row):
    case = row["case"]
    provenance = {"case":case, "run_segment":row["run_segment"], "harvest_step":row["harvest_step"]}
    try:
        folder = root/case
        deck, log = folder/row["deck"], folder/row["canonical_log"]
        require(root.is_dir() and not root.is_symlink() and folder.is_dir() and not folder.is_symlink()
                and all(p.is_file() and not p.is_symlink() for p in (deck,log)), "SOURCE_MISSING_OR_LINK")
        require(b7.sha256_of(deck) == row["deck_sha256"], "DECK_IDENTITY")
        raw = log.read_bytes()
        log_hash = digest(raw)
        line_hash = canonical_check(raw,row)
        # Same B7 record function. The selected source is one explicit path; no log glob.
        record = b7.record(case,str(deck),[str(log)],row["deck_sha256"])
        require(b7.sha256_of(deck)==row["deck_sha256"] and b7.sha256_of(log)==log_hash,
                "SOURCE_CHANGED_DURING_READ")
        if record["log_sha256"]:
            require(record["log_sha256"]==log_hash and int(record["n_press_lines"])==row["b7_line_count"],
                    "B7_READBACK_IDENTITY")
        require(record["status"] in b7.STATUSES, "B7_STATUS")
        qualified = record["status"]=="OK" and record["reached"]=="True"
        if qualified:
            target,last = float(record["target_mpa"]),float(record["last_press_mpa"])
            qualified = (math.isfinite(target) and math.isfinite(last) and abs(target-300.0)<=1e-6
                         and last>=target-1e-6)
        reason = None if qualified else (record["status"] if record["status"] != "OK" else "DESIGN_TARGET_OR_REACHED")
        return dict(provenance,pressure_check="OK" if qualified else "HOLD",reason=reason,
                    b7=record,canonical_sha256=log_hash,normalized_pressure_sequence_sha256=line_hash)
    except (SourceMismatch,OSError,UnicodeError) as exc:
        reason=str(exc) if isinstance(exc,SourceMismatch) else type(exc).__name__
        return dict(provenance,pressure_check="HOLD",b7=None,reason=reason)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=[GO])
    p.add_argument("out",type=Path)
    a=p.parse_args()
    roster_bytes=(HERE/"roster.json").read_bytes()
    require(digest(roster_bytes)==ROSTER_SHA, "ROSTER_IDENTITY")
    rows=json.loads(roster_bytes)["roster"]
    require([r["case"] for r in rows]==[f"lhs00_{n}" for n in range(100,130)],"ROSTER_CASES")
    start=utc()
    values=[assess(Path.home()/"lhs_local",r) for r in rows]
    count=sum(r["pressure_check"]=="OK" for r in values)
    report={"scope":"WSL30_ONLY_SECTION5_PRESSURE","operator":"first_author","approval_mode":a.mode,
            "read_started_utc":start,"read_ended_utc":utc(),"roster_sha256":ROSTER_SHA,
            "release":(HERE/"RELEASE").read_text().strip(),"planned":30,"ok":count,
            "rows":values,"tau_read":False,"release_authorized":False}
    data=(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode()
    path=a.out/"lhs_wsl30_section5_return.zip"
    with zipfile.ZipFile(path,"x",compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("readback.json",data)
        z.writestr("SHA256SUMS",digest(data)+"  readback.json\n")
    with zipfile.ZipFile(path) as z:
        require(z.testzip() is None and z.read("readback.json")==data, "ARCHIVE")
    print(f"RETURN_ZIP={path}\nSHA256={digest(path.read_bytes())}\nRECORDED=30")
    return 0 if count==30 else 1


if __name__=="__main__":
    raise SystemExit(main())

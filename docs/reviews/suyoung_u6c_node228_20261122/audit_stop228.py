"""Offline byte comparison, fixed source membership, and independent contact-face search."""
import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tarfile

PIN = "d0c33bc19c2dd1291f3cf3ae0788fd193065e72b"
CURRENT = "a100f018bd5e9c3621395ac436550029759fe17a02a55641db121d52dba1fdbe"
OLD = "c39bbd65d1c0caa5825abc8095611a8d20a8168e5464db3cd2a05743e3abbbeb"
CAPTURE145 = "90b070d33e84735008035eb399d648acb6065edfb677653f8db9f3c9c61eca18"
STOP = "fca406d296c8a6f2b5bb260784711afdc87a34cda48f71ce93c8abcaf7f1059f"
ANALYZER = "321806f1031af00022c171420c40b197b9b75ab51ccd9b3405bd20aabefee44e"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(test, msg):
    if not test:
        raise ValueError(msg)


def module(path):
    spec = importlib.util.spec_from_file_location("readback_witness", path)
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    return source


def member(t, key):
    m = t.getmember(key)
    require(m.isfile(), "expected data file")
    return t.extractfile(m).read()


def run(a):
    for path, expected in ((a.result,CURRENT),(a.previous,OLD),(a.capture145,CAPTURE145)):
        require(digest(path.read_bytes()) == expected, "input archive identity")
    with tarfile.open(a.result) as new, tarfile.open(a.previous) as old, tarfile.open(a.capture145) as capture:
        nt = member(new,"run/ORIGINAL/trace.csv")
        ot = member(old,"run/ORIGINAL/trace.csv")
        ct = member(capture,"run/capture/replay/trace.csv")
        lines = list(csv.DictReader(nt.decode("ascii").splitlines()))
        require([int(row["step"]) for row in lines] == list(range(228)), "trace step order")
        require(ot == ct and len(ot.splitlines()) == 146, "history/reference disagreement")
        require(nt.splitlines(keepends=True)[:146] == ot.splitlines(keepends=True), "partial prefix drift")
        stop_bytes = member(new,"run/ORIGINAL/contact_stop.json")
        require(digest(stop_bytes) == STOP and stop_bytes == a.node.read_bytes(), "contact stop binding")
        stop = json.loads(member(new,"run/ORIGINAL/stop.json"))
        require(stop["attempted_step"] == 228 and stop["returned_nodes"] == 1 and
                stop["trace"]["sha256"] == digest(nt) and stop["contact_stop_sha256"] == STOP and
                not stop["stage3_go"] and not stop["u6_qualified"],"terminal cross-references")
        source = member(new,"run/SOURCE_SHA256SUMS")
        origin = dict(line.split("=",1) for line in member(new,"run/origin.txt").decode("ascii").splitlines())
        require(origin["release"] == PIN and origin["source_sums"] == digest(source) and
                origin["prior_capture"] == CAPTURE145, "source manifest binding")
        entries = dict(line.split(maxsplit=1)[::-1] for line in source.decode("ascii").splitlines())
        require(len(entries) == 10 and entries["scripts/suyoung_multicontact_dev.py"] == stop["kernel_sha256"],
                "kernel/manifest mismatch")
        repo = a.repo.resolve().as_posix()
        for path, expected in entries.items():
            if path == "RELEASE":
                data = ("\n".join((PIN,"6bdfac91520c868b5036071e6d60464972727f49",
                        "c36516a26d4a66f3db71c70de31b75802cb4bdb7",
                        "c3c9ae92655ad39508ea6dd52efac8b71e5001b8",
                        "001e5e5e5f3bedde8106b608910e95f5dd1f78cb",
                        "f24cce28be28aece96d18cf77173d8fe05a2bfb0"))+"\n").encode("ascii")
            else:
                data = subprocess.check_output(["git","-c","safe.directory="+repo,"-C",repo,"show",PIN+":"+path])
            require(digest(data) == expected,"pinned content differs: "+path)
        require(not any("/RELABEL/" in name for name in new.getnames()), "unexpected relabel output")
    analyzer = a.repo/"docs/reviews/suyoung_u6c_step145_20261122/analyze_stop_node.py"
    require(digest(analyzer.read_bytes()) == ANALYZER,"analyzer SHA")
    record = json.loads(stop_bytes)
    require(record["attempted_step"] == 228 and len(record["nodes"]) == 1 and
            record["nodes"][0]["node_id"] == 2304,"node scope")
    analyzed = module(analyzer).analyze(record["nodes"][0])
    witness = analyzed["witness"]
    require(witness["status"] == "WITNESS_AT_ORIGINAL_TOLERANCE","no verified face witness")
    witness.pop("scaled_impulses_nt")  # External field values stay local.
    return {"release":PIN,"archive_sha256":CURRENT,"node_sha256":STOP,"prefix_sha256":digest(ot),
            "header_and_steps_0_through_144_byte_equal_across_three_returns":True,
            "last_complete_step":int(lines[-1]["step"]),"trace_data_rows":len(lines),
            "relabel_present":False,"source_manifest_entries":len(entries),
            "frozen_node":analyzed}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for flag in ("repo","result","previous","capture145","node","out"):
        p.add_argument("--"+flag,required=True,type=Path)
    args = p.parse_args()
    report = run(args)
    print(json.dumps(report,sort_keys=True))
    with args.out.open("x",encoding="utf-8") as out:
        json.dump(report,out,sort_keys=True,indent=2)
        out.write("\n")

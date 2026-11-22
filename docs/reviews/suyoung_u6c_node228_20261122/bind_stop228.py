"""Bind the returned native F8 stop and its producer to a distinct candidate kernel."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import tarfile


RELEASE = "d0c33bc19c2dd1291f3cf3ae0788fd193065e72b"
ARCHIVE = "a100f018bd5e9c3621395ac436550029759fe17a02a55641db121d52dba1fdbe"
SUMS = "d459b724a45ea207706d313b53125fa7cf34d6f6e19c5064e4385d1c692dd289"
KERNEL = "742bd8b04ed41192ba888825f713605327042d4bd8fdb215a068495a323e7f2d"
NODE = "fca406d296c8a6f2b5bb260784711afdc87a34cda48f71ce93c8abcaf7f1059f"
PREFIX = "d4584cad3dd412aa58478ea04cd39da5af2b2152b9bb37634cbd0cbdb23efc30"
PRIOR = dict(prior_capture="90b070d33e84735008035eb399d648acb6065edfb677653f8db9f3c9c61eca18",
             prior_wall="0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90",
             prior_order="8e76ec686e8f384c28c42b5c5304d25256096f0568fe999d602bdec307991e17")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, label):
    if not ok:
        raise ValueError(label)


def read_return(path):
    raw = path.read_bytes()
    require(sha(raw) == ARCHIVE, "STOP228_ARCHIVE")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        def member(name):
            return tar.extractfile("run/"+name).read()

        require("run/REVERSED" not in tar.getnames() and "run/comparison.json" not in tar.getnames(),
                "STOP228_SCOPE")
        origin = dict(line.split("=", 1) for line in member("origin.txt").decode("ascii").splitlines())
        sums = member("SOURCE_SHA256SUMS")
        data = {name:member("ORIGINAL/"+name) for name in ("trace.csv","contact_stop.json","stop.json")}
        screen = member("screen.txt").decode("ascii").splitlines()
    require(origin["release"] == RELEASE and origin["source_sums"] == sha(sums) == SUMS and
            all(origin[k] == v for k,v in PRIOR.items()), "STOP228_ORIGIN")
    require("F8_ORIGINAL_RC=4" in screen and "COMMAND_RC=4" in screen, "STOP228_SCREEN")
    state = json.loads(data["stop.json"])
    contact = json.loads(data["contact_stop.json"])
    trace = data["trace.csv"]
    require(state["mapping"] == "ORIGINAL" and state["status"] == "CONTACT_STOP"
            and not state["u6_qualified"] and not state["stage3_go"] and state["kernel_sha256"] == KERNEL
            and state["prior_capture_sha256"] == PRIOR["prior_capture"], "STOP228_RECEIPT")
    require(state["contact_stop_sha256"] == sha(data["contact_stop.json"]) == NODE and
            state["scope"] == contact["scope"] == "NATIVE_UNRESOLVED_ROWS" and
            state["attempted_step"] == contact["attempted_step"] == 228 and
            state["returned_nodes"] == len(contact["nodes"]) == 1
            and contact["nodes"][0]["node_id"] == 2304, "STOP228_NODE")
    require(state["trace"]["sha256"] == sha(trace) == PREFIX and state["trace"]["sequence_valid"]
            and state["trace"]["last_complete_step"] == 227 and len(trace) == state["trace"]["bytes"]
            and [int(row["step"]) for row in csv.DictReader(io.StringIO(trace.decode("ascii")))] == list(range(228)),
            "STOP228_PREFIX")
    return dict(line.split("  ",1)[::-1] for line in sums.decode("ascii").splitlines())


def verify_sources(sources, root):
    expected = sources.copy()
    del expected["RELEASE"]
    kernel = "scripts/suyoung_multicontact_dev.py"
    require(expected.pop(kernel) == KERNEL and sha((root/kernel).read_bytes()) != KERNEL,
            "STOP228_KERNEL_UNCHANGED")
    require(all(sha((root/name).read_bytes()) == digest for name,digest in expected.items()),
            "STOP228_DRIVER_CHANGED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stop", required=True, type=Path)
    parser.add_argument("--package-root", required=True, type=Path)
    args = parser.parse_args()
    verify_sources(read_return(args.stop), args.package_root)
    print("PRIOR_STEP_228_BOUND")

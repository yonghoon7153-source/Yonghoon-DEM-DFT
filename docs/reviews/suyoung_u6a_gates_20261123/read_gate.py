"""Read setting 1 U6(a) with the pre-existing first-pressure-crossing reader."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import tarfile


PHYSICS = "99938d3bd4cb1cbba0e1377be2ff9dac9b228d2f"
FLOOR = "4b64bcfe6d0975e3bb18d450cfab77c8c3db750dc06f17965c21c5057f3dd72b"
RULE = "512fa5cbad8319cf0cff0ef2f800ad5cb00f91cdf8ce806ee6768fd3742dac7c"
TARGET_E = 0.12
RETURNS = {
    "full": ((8, 16), "aa0f2ad7126a65654975de6a741a58b49c57a5cc84c42983b226ddca15212b65",
             "37aa078fb8079c655d88e24ff779048a78d1c8f131dc77c954ae4b41c1836595",
             "c0e077ad5961d7be8dd801ea2f527b76089b362a"),
    "fine": ((12, 24), "c1506ea6fb6f16181fe36e85e76043101380b75c9cf435b2811a5b53b761d673",
             "4013a5e5d39bb06675d1427e5f4a67ca2cffeffd237f2a4c0cc06df23787b007",
             "e8e2f2535aa12b9fb089d714e1325d862cb1161b"),
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def registered_reader(path):
    require(sha(path.read_bytes()) == RULE, "registered endpoint reader identity")
    spec = importlib.util.spec_from_file_location("registered_u6_repeat", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_pair(kind, path, rule):
    cells, expected_tar, expected_screen, release = RETURNS[kind]
    raw = path.read_bytes()
    require(sha(raw) == expected_tar, "return SHA256")
    manifest = dict(line.split("  ", 1)[::-1] for line in (path.parent/"SHA256SUMS").read_text().splitlines())
    require(manifest == {path.name: expected_tar, "screen.txt": expected_screen}, "external manifest")
    results = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        def read(name):
            return tar.extractfile("run/" + name).read()

        screen = read("screen.txt")
        require(sha(screen) == expected_screen and screen == (path.parent/"screen.txt").read_bytes(),
                "screen identity")
        lines = screen.splitlines()
        require(lines[-1] == b"COMMAND_RC=0" and b"RETRIES=0" in lines, "operator status")
        summary = json.loads(read("summary.json"))
        source_hash = sha(read("SOURCE_SHA256SUMS"))
        physics_key = "physics_pin" if kind == "full" else "base_physics_pin"
        source_key = "source_manifest_sha256" if kind == "full" else "package_manifest_sha256"
        require(summary["release"] == read("RELEASE").decode().strip() == release
                and summary[physics_key] == PHYSICS and summary["floor_sha256"] == FLOOR
                and summary[source_key] == source_hash and summary["both_reached_target"]
                and not summary["stage3_go"] and not summary["u6_qualified"], "return provenance")
        if kind == "fine":
            require(summary["previous_return_sha256"] == RETURNS["full"][1]
                    and summary["previous_pin"] == RETURNS["full"][3], "full/fine cross-binding")

        for n in cells:
            prefix = f"F{n}/"
            require(f"F{n}_RC=0".encode() in lines, "arm rc")
            receipt = json.loads(read(prefix + kind + "_receipt.json"))
            result_raw = read(prefix + "result.json")
            result = json.loads(result_raw)
            data = read(prefix + "trace.csv")
            require(receipt == summary["arms"][f"F{n}"] and receipt["release"] == release
                    and receipt[physics_key] == PHYSICS and receipt["floor_sha256"] == FLOOR
                    and receipt["reached_target"] and result["status"] == "TARGET_BRACKETED"
                    and result["protocol"] == "U6b-setting1-bottom-loading-v1" and result["setting"] == 1
                    and result["arm"] == "F" and result["cells"] == n == receipt["cells"]
                    and sha(result_raw) == receipt["result_sha256"]
                    and sha(data) == receipt["trace_sha256"] == result["trace_sha256"], "arm provenance")
            steps = result["steps"]
            endpoint = rule.bracket_value(data, TARGET_E, steps)
            records = list(csv.DictReader(io.StringIO(data.decode("ascii"))))
            a, b = records[-2:]
            p0, p1 = (float(r["bottom_pressure_E"]) for r in (a,b))
            h0, h1 = (float(r["height"]) for r in (a,b))
            h_target = h0 + (h1-h0)*(TARGET_E-p0)/(p1-p0)
            width = float(records[0]["height"])
            reference_area = float(records[0]["phi_m"])*width*width
            require(math.isclose(reference_area,49*math.pi*0.05**2, rel_tol=1e-12)
                    and math.isclose(endpoint, reference_area/(width*h_target), rel_tol=1e-14)
                    and p0 < TARGET_E <= p1 and int(b["step"]) == steps, "area or crossing")
            results[n] = dict(phi_m_at_target=endpoint, height_at_target=h_target, step_bracket=[steps-1,steps],
                              pressure_bracket_MPa=[10*p0,10*p1], first_at_or_above_phi_m=float(b["phi_m"]),
                              elapsed_seconds=result["elapsed_s"], budget_seconds=result["budget_s"],
                              reference_area=reference_area, box_area_at_target=width*h_target,
                              max_floor_penetration_code=receipt["floor_audit"]["max_penetration"],
                              trace_sha256=sha(data), receipt_sha256=sha(read(prefix+kind+"_receipt.json")))
    return results


def evaluate(full, fine, path):
    rule = registered_reader(path)
    arms = dict(sorted((read_pair("full",full,rule) | read_pair("fine",fine,rule)).items()))
    diff = abs(arms[12]["phi_m_at_target"] - arms[16]["phi_m_at_target"])
    require(rule.BAND == 0.005, "registered selection line")
    within = rule.grid_status(diff) == "WITHIN_DEVELOPMENT_BAND"
    return dict(label="DEVELOPMENT_ONLY", setting=1, grid_cells=[12,16], arms=arms,
                threshold=rule.BAND, absolute_delta=diff, status="PASS" if within else "FAIL",
                seconds_total=sum(a["elapsed_seconds"] for a in arms.values()),
                historical_timeouts_these_four_runs=0, new_model_runs=0, timeouts_this_readback=0,
                registered_reader_sha256=RULE, full_return_sha256=RETURNS["full"][1],
                fine_return_sha256=RETURNS["fine"][1], physics_pin=PHYSICS, floor_sha256=FLOOR)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("full",type=Path)
    parser.add_argument("fine",type=Path)
    parser.add_argument("--reader",type=Path,default=Path(__file__).resolve().parents[1]/
                        "suyoung_u6_repeat_20261120"/"repeat_readback.py")
    args=parser.parse_args()
    print(json.dumps(evaluate(args.full,args.fine,args.reader),indent=2,allow_nan=False))

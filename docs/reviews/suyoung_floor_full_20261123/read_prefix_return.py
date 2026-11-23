"""Read the author's frozen wall-prefix return and export its two weekly artifacts."""
import argparse
import bisect
import csv
import hashlib
import io
import json
import math
import tarfile
import zipfile
from pathlib import Path


PIN = "b16bef3f7791b86d31f0197d86b58d9d93d84750"
ZIP_SHA = "99ab81990d0524a47ba844cdd69941e5fbb4b47ea2dfe5b591ed598d27362a12"
TAR_SHA = "57d0a6fe178b2faf0545013ef43b9ff6d175c1fdb18e93522ec8dcb8eb1b7e34"
SCREEN_SHA = "eab22d6188bb6d524afb9f68f5deba42276c8b3ea2cdd49ba3f3a9f2524cf8fb"
DENOMINATOR = 0.6636991102836952


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def require(test, what):
    if not test:
        raise ValueError(what)


def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("ascii"))))


def lerp(trace, xs, x):
    i = bisect.bisect_left(xs, x)
    if xs[i] == x:
        return trace[i][1]
    ratio = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
    return trace[i - 1][1] + ratio * (trace[i][1] - trace[i - 1][1])


def read(zpath, tpath, screen, out):
    require(digest(zpath.read_bytes()) == ZIP_SHA and digest(tpath.read_bytes()) == TAR_SHA
            and digest(screen.read_bytes()) == SCREEN_SHA, "outer checksum")
    with zipfile.ZipFile(zpath) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) and z.testzip() is None, "zip integrity")
        sums = {n: h for h, n in (r.split("  ", 1) for r in z.read("SHA256SUMS").decode().splitlines())}
        require(set(sums) == set(names) - {"SHA256SUMS"}
                and all(digest(z.read(n)) == h for n, h in sums.items()), "inner checksums")
        weekly = {name: z.read("weekly/" + name) for name in
                  ("weekly_pressure_displacement.png", "pressure_displacement.csv", "summary.json")}
    with tarfile.open(tpath, "r:gz") as tar:
        require(len(tar.getnames()) == len(set(tar.getnames())), "tar duplicates")
        def get(name):
            member = tar.getmember("run/" + name)
            require(member.isfile(), name)
            return tar.extractfile(member).read()
        require(all(v == get(k) for k,v in weekly.items()), "weekly files differ from author return")
        summary = json.loads(weekly["summary.json"])
        require(get("RELEASE").decode().strip() == summary["release"] == PIN, "pin")
        table = rows(weekly["pressure_displacement.csv"])
        require(len(table) == 1624 and summary["registered_fine_peak_MPa"] == DENOMINATOR, "scope")
        report = {"release": PIN, "zip_payload_hashes": len(sums), "native_rows":len(table),
                  "registered_peak_MPa": DENOMINATOR, "models": {}}
        for model in ("original", "candidate"):
            arms = {}
            trace = {}
            for cells, count in ((8, 271), (16, 541)):
                name = f"{model}/F{cells}/trace.csv"
                raw = get(name)
                require(digest(raw) == summary["trace_sha256"][name], name)
                arm = rows(raw)
                mapped = [r for r in table if r["wall_model"] == model and int(r["cells"]) == cells]
                require(len(arm) == len(mapped) == count, "trace count")
                width = float(arm[0]["height"])
                events = []
                for i, (a, r) in enumerate(zip(arm, mapped)):
                    x, p = width-float(a["height"]), 10.*float(a["bottom_pressure_E"])
                    require(int(a["step"]) == int(r["step"]) == i and float(r["pressure_MPa"]) == p
                            and float(r["displacement_code"]) == x and float(r["time_code"]) == float(a["time_code"]),
                            "raw samples")
                    events.append((x, p))
                trace[cells] = events
                positive = [i for i, (_,p) in enumerate(events) if p > 0.]
                arms[str(cells)] = dict(first_positive_step=positive[0] if positive else None,
                                        positive_samples=len(positive), last_pressure_MPa=events[-1][1])
            x8, x16 = ([x for x,p in trace[c]] for c in (8,16))
            knots = sorted(set(x8)|set(x16))
            require(x8[0] == x16[0] and x8[-1] == x16[-1] and len(knots) == 541, "common support")
            delta = [abs(lerp(trace[8], x8, x) - lerp(trace[16], x16, x)) for x in knots]
            i_max = max(range(len(delta)), key=delta.__getitem__)
            k_first = next((i for i,d in enumerate(delta) if d > .05*DENOMINATOR), None)
            require(math.isclose(delta[i_max], summary["gap_summary"][model]["native_union"]["peak"]["signed_gap_MPa"],
                                 rel_tol=1e-13), "peak")
            report["models"][model] = dict(arms=arms, peak_gap_MPa=delta[i_max],
                                            peak_pct=100*delta[i_max]/DENOMINATOR, fine_step_at_peak=i_max,
                                            first_above_5pc=k_first, last_displacement=knots[-1])
    out.mkdir(parents=True, exist_ok=True)
    for name in ("weekly_pressure_displacement.png", "pressure_displacement.csv"):
        path = out / name
        if path.exists():
            require(path.read_bytes() == weekly[name], "existing file differs")
        else:
            with path.open("xb") as f:
                f.write(weekly[name])
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("zip", "tar", "screen", "out"):
        p.add_argument(name, type=Path)
    a = p.parse_args()
    read(a.zip, a.tar, a.screen, a.out)

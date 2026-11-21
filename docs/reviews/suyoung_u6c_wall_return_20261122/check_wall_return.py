"""Independently read the fingerprinted F8/F16 wall return; no solver imports."""

import argparse
from bisect import bisect_left
import csv
import hashlib
import io
import json
from pathlib import Path
import tarfile


ARCHIVE_SHA256 = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"
TRACE_SHA256 = {
    8: "03f3bc2c106aa466f1ccc2b774e0b768f2a902792006609680faa53038434cdf",
    16: "5475cc87df297533002afb621cbdac06c0319ca40eb65ddf40322ae6c018b0de",
}
FORCES = ("total", "pre", "post", "top_pre", "top_post")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def member(tar, name):
    info = tar.getmember(name)
    require(info.isreg(), "Expected a regular archive member")
    with tar.extractfile(info) as stream:
        return stream.read()


def csv_rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode("ascii"), newline="")))


def read_arm(tar, cells):
    folder = f"run/arms/F{cells}/"
    obs = json.loads(member(tar, folder + "observer.json"))
    trace = member(tar, folder + "trace.csv")
    wall = member(tar, folder + "wall.csv")
    require(hashlib.sha256(trace).hexdigest() == obs["trace_sha256"] == TRACE_SHA256[cells], "Native trace mismatch")
    require(hashlib.sha256(wall).hexdigest() == obs["wall_sha256"], "Wall table mismatch")
    native, side = csv_rows(trace), csv_rows(wall)
    require(len(native) == len(side) + 1 == obs["steps"] + 1, "Step count mismatch")
    dt, width, scale = obs["dt"], obs["width"], obs["E_MPa"]
    samples = [{key: 0.0 for key in ("u", *FORCES)}]
    for step, (t, w) in enumerate(zip(native[1:], side), start=1):
        require(step == int(w["step"]) == int(t["step"]), "Step mismatch")
        displacement = width - float(t["height"])
        require(displacement == float(w["plate_displacement_code"]) and displacement > samples[-1]["u"], "Displacement mismatch")
        pre, post = float(w["bottom_J_pre"]), float(w["bottom_J_post"])
        pressure = (pre + post) / (dt * width)
        require(pressure == float(t["bottom_pressure_E"]) == float(w["bottom_pressure_E"]), "Native reaction mismatch")
        samples.append({
            "u": displacement, "total": scale * pressure,
            "pre": scale * (pre / (dt * width)), "post": scale * (post / (dt * width)),
            "top_pre": scale * (float(w["top_J_down_pre"]) / (dt * width)),
            "top_post": scale * (float(w["top_J_down_post"]) / (dt * width)),
            "row": int(w["first_top_row"]), "lid": float(w["lid_code"]),
        })
    return samples


def interpolate(samples, axis, x):
    right = bisect_left(axis, x)
    if right < len(axis) and axis[right] == x:
        return samples[right]
    require(0 < right < len(axis), "Outside measured support")
    lo, hi = samples[right - 1], samples[right]
    fraction = (x - lo["u"]) / (hi["u"] - lo["u"])
    return {key: lo[key] + fraction * (hi[key] - lo[key]) for key in FORCES}


def examine(path):
    with path.open("rb") as stream:
        require(hashlib.file_digest(stream, "sha256").hexdigest() == ARCHIVE_SHA256, "Unexpected return archive")
    with tarfile.open(path, "r:gz") as tar:
        arms = {c: read_arm(tar, c) for c in (8, 16)}
    axes = {c: [s["u"] for s in arm] for c, arm in arms.items()}
    end = min(axes[c][-1] for c in arms)
    union = sorted({x for xs in axes.values() for x in xs if x <= end})
    gaps = []
    max_fine = 0.0
    for x in union:
        a, b = (interpolate(arms[c], axes[c], x) for c in (8, 16))
        gaps.append({key: a[key] - b[key] for key in FORCES})
        max_fine = max(max_fine, abs(b["total"]))
    worst = max(range(len(gaps)), key=lambda i: abs(gaps[i]["total"]))
    max_post = max(range(len(gaps)), key=lambda i: abs(gaps[i]["post"]))
    exceeds = [i for i, g in enumerate(gaps) if abs(g["total"]) > 0.05 * max_fine]

    # Never interpolate a row index. Compare the first eligible node heights at
    # exactly coincident, positive native displacements on both physical grids.
    shared = sorted(set(axes[8][1:]) & set(axes[16][1:]))
    groups = {"same_height": [], "different_height": []}
    by_u = {c: {s["u"]: s for s in a[1:]} for c, a in arms.items()}
    for x in shared:
        a, b = (by_u[c][x] for c in (8, 16))
        require(a["lid"] == b["lid"], "Lid positions disagree")
        key = "same_height" if 2 * a["row"] == b["row"] else "different_height"
        groups[key].append(abs(a["total"] - b["total"]))
    xworst = union[worst]
    detail = {}
    for c in (8, 16):
        s = by_u[c][xworst]
        row_height = s["row"] / (10 * c)
        detail[f"F{c}"] = {
            "native_step": bisect_left(axes[c], xworst), "bottom_total_MPa": s["total"],
            "lid_code": s["lid"], "row": s["row"], "row_height_code": row_height,
            "top_row_minus_lid_code": row_height - s["lid"],
            "top_down_impulse_pressure_equivalent_MPa": s["top_pre"] + s["top_post"],
        }
    return {
        "archive_sha256": ARCHIVE_SHA256, "native_steps": {f"F{c}": len(a) - 1 for c, a in arms.items()},
        "common_positive_and_origin_knots": len(union), "common_end_displacement": end,
        "fine_peak_MPa": max_fine, "above_5_percent_knots": len(exceeds),
        "first_above_5_percent_u": union[exceeds[0]],
        "worst_total_u": xworst, "signed_F8_minus_F16_at_worst_MPa": gaps[worst],
        "native_at_worst": detail, "max_abs_bottom_post_gap_MPa": abs(gaps[max_post]["post"]),
        "max_abs_bottom_post_gap_u": union[max_post],
        "aligned_native_row_height_comparison": {
            k: {"count": len(v), "above_5_percent": sum(d > .05 * max_fine for d in v), "max_abs_gap_MPa": max(v)}
            for k, v in groups.items()
        },
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("archive", type=Path)
    p.add_argument("--out", type=Path, help="Write a new JSON file (default: stdout)")
    args = p.parse_args()
    result = json.dumps(examine(args.archive), indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        with args.out.open("x", encoding="ascii", newline="\n") as f:
            f.write(result)
    else:
        print(result, end="")


if __name__ == "__main__":
    main()

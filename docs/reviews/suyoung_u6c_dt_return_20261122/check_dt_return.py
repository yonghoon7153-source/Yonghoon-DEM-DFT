"""Recompute the F8 half-step comparison from three native CSVs. No model imports."""
import argparse
import csv
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


WALL = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"
HALF = "e574396d010514b3cd77f57d2e06d0c25227c88a7b6e985577f2981aa8c154e4"


def check(condition, reason):
    if not condition:
        raise ValueError(reason)


def unpack(path, digest, names):
    with path.open("rb") as stream:
        check(hashlib.file_digest(stream, "sha256").hexdigest() == digest, "Unexpected archive")
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode="r:gz") as tar:
            return [tar.extractfile(name).read() for name in names]


def curve(raw):
    rows = csv.DictReader(io.StringIO(raw.decode("ascii"), newline=""))
    initial = next(rows)
    width = float(initial["height"])
    check(initial["step"] == "0" and float(initial["bottom_pressure_E"]) == 0, "Invalid starting point")
    samples = [(0., 0.)]
    for step, row in enumerate(rows, start=1):
        u, p = width - float(row["height"]), 10 * float(row["bottom_pressure_E"])
        check(step == int(row["step"]) and u > samples[-1][0] and math.isfinite(p), "Invalid trace")
        samples.append((u, p))
    return samples


def interpolate(samples, support):
    j = 0
    for u in support:
        while samples[j][0] < u:
            j += 1
        x1, y1 = samples[j]
        if u == x1:
            yield y1
        else:
            x0, y0 = samples[j-1]
            yield y0 + (u-x0)/(x1-x0)*(y1-y0)


def readback(wall, dt):
    c, f = unpack(wall, WALL, ["run/arms/F8/trace.csv", "run/arms/F16/trace.csv"])
    h, report_raw = unpack(dt, HALF, ["run/F8_HALF/trace.csv", "run/dt_summary.json"])
    curves = [curve(data) for data in (c, h, f)]
    report = json.loads(report_raw)["comparison"]
    end = min(curve[-1][0] for curve in curves)
    support = sorted({u for curve in curves for u, _ in curve if u <= end})
    c, h, f = (list(interpolate(s, support)) for s in curves)
    old = [x-y for x,y in zip(c, f)]
    time = [x-y for x,y in zip(c, h)]
    remaining = [x-y for x,y in zip(h, f)]
    anchor = max(range(len(support)), key=lambda i: abs(old[i]))
    denominator = max(map(abs, f))
    check(len(support) == report["common_knots"] and end == report["common_end_u"], "Support mismatch")
    check(support[anchor] == report["prior_peak_gap_u"] and report["prior_peak_coverage"] == "REACHED",
          "Anchor mismatch")
    for name, series in (("original_F8_minus_F16", old), ("F8_minus_F8_half_dt", time),
                         ("F8_half_dt_minus_F16", remaining)):
        check(abs(series[anchor] - report["at_prior_peak"]["signed_gaps_MPa"][name]) < 1e-14,
              "Anchor contrast mismatch")
        check(abs(max(map(abs, series)) - report["common_max_abs_gap_MPa"][name]) < 1e-14,
              "Maximum contrast mismatch")
    check(max(abs(x-y-z) for x,y,z in zip(old,time,remaining)) < 1e-14, "Residual mismatch")
    def exceed(series):
        return sum(20 * Fraction(abs(x)) > Fraction(denominator) for x in series)

    return {
        "u_anchor": support[anchor], "knots_including_origin": len(support),
        "F16_peak_on_common_support_MPa": denominator,
        "MPa_at_anchor": dict(zip(("F8", "F8_half_dt", "F16"), (c[anchor],h[anchor],f[anchor]))),
        "signed_contrasts_MPa_at_anchor": dict(zip(("original", "time", "remaining"),
                                               (old[anchor],time[anchor],remaining[anchor]))),
        "time_contrast_percent_of_original_at_anchor": time[anchor]/old[anchor]*100.,
        "remaining_percent_of_original_at_anchor": remaining[anchor]/old[anchor]*100.,
        "largest_abs_time_contrast_MPa": max(map(abs,time)),
        "largest_abs_remaining_contrast_MPa": max(map(abs,remaining)),
        "original_over_5_percent_of_fine_peak_knots": exceed(old),
        "remaining_over_5_percent_of_fine_peak_knots": exceed(remaining),
        "time_over_5_percent_of_fine_peak_knots": exceed(time),
        "remaining_max_percent_of_fine_peak": max(map(abs,remaining))/denominator*100.,
        "signed_identity_max_abs_roundoff_MPa": max(abs(x-y-z) for x,y,z in zip(old,time,remaining)),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wall", type=Path)
    p.add_argument("dt", type=Path)
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    text = json.dumps(readback(args.wall, args.dt), indent=2, sort_keys=True, allow_nan=False)+"\n"
    if args.out:
        with args.out.open("x", encoding="ascii", newline="\n") as stream:
            stream.write(text)
    else:
        print(text, end="")

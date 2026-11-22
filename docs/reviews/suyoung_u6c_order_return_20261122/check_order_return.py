"""Independent two-trace F8 ID-order readback, using only Python's standard library."""
import argparse
from bisect import bisect_left
import csv
from hashlib import sha256
import io
import json
import math
from pathlib import Path
import tarfile


WALL = "0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90"
ORDER = "8e76ec686e8f384c28c42b5c5304d25256096f0568fe999d602bdec307991e17"
ANCHOR = 0.11562281664031926
CAP_MPA = 1.2


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unpack(path, identity, names):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == identity, "Wrong archive")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        return {name:tar.extractfile(name).read() for name in names}


def parse(data, receipt):
    require(sha256(data).hexdigest() == receipt["trace_sha256"], "Wrong trace")
    reader = csv.DictReader(io.StringIO(data.decode("ascii"), newline=""))
    require(reader.fieldnames == ["step","time_code","height","bottom_pressure_E","phi_m"], "Columns changed")
    u, pressure, t, fraction = [], [], [], []
    for step, row in enumerate(reader):
        h = float(row["height"])
        p = 10 * float(row["bottom_pressure_E"])
        if step == 0:
            initial = h
        require(step == int(row["step"]) and math.isfinite(p) and p >= 0, "Bad pressure or step")
        u.append(initial-h)
        pressure.append(p)
        t.append(float(row["time_code"]))
        fraction.append(float(row["phi_m"]))
    require(len(u) == receipt["steps"]+1 and t[0] == u[0] == pressure[0] == 0, "Step count or initial state")
    require(all(a < b for a,b in zip(u,u[1:])) and all(a < b for a,b in zip(t,t[1:])), "Invalid time/displacement schedule")
    require(receipt["status"] == "TARGET_BRACKETED" and max(pressure[:-1]) < CAP_MPA <= pressure[-1], "Not a first pressure crossing")
    return u, pressure, t, fraction


def at_displacement(axis, values, u):
    if u < axis[0] or u > axis[-1]:
        return None
    j = bisect_left(axis,u)
    if axis[j] == u:
        return values[j]
    return values[j-1]+(values[j]-values[j-1])*(u-axis[j-1])/(axis[j]-axis[j-1])


def cap_bracket(u, p):
    alpha = (CAP_MPA-p[-2])/(p[-1]-p[-2])
    return {"first_step_at_or_above":len(u)-1, "last_two_displacements":u[-2:],
            "last_two_pressures_MPa":p[-2:],
            "linear_crossing_u":u[-2]+alpha*(u[-1]-u[-2])}


def readback(wall_path, order_path):
    folder_a, folder_b = "run/arms/F8/", "run/F8_RELABEL/"
    old = unpack(wall_path, WALL, [folder_a+"trace.csv",folder_a+"result.json"])
    new = unpack(order_path, ORDER, [folder_b+"trace.csv",folder_b+"result.json","run/order_summary.json"])
    oa = json.loads(old[folder_a+"result.json"])
    ob = json.loads(new[folder_b+"result.json"])
    x,a,ta,fa = parse(old[folder_a+"trace.csv"],oa)
    y,b,tb,fb = parse(new[folder_b+"trace.csv"],ob)
    n = min(len(x),len(y))
    require(x[:n] == y[:n] and ta[:n] == tb[:n] and fa[:n] == fb[:n], "Original and reversed native schedules differ")
    diff = [left-right for left,right in zip(a[:n],b[:n],strict=True)]
    def point(i):
        return {"step":i,"u":x[i],"original_MPa":a[i],"relabelled_MPa":b[i],
                "original_minus_relabelled_MPa":diff[i]}
    j = max(range(n),key=lambda i:abs(diff[i]))
    anchor = at_displacement(y,b,ANCHOR)
    s = json.loads(new["run/order_summary.json"])
    q = s["comparison"]
    verify = point(j).copy()
    del verify["step"]
    require(q["first_worst"] == verify and q["common_end_u"] == x[n-1] and q["common_knots"] == n
            and q["max_abs_difference_MPa"] == abs(diff[j]) and q["fixed_u"] == ANCHOR,
            "Returned comparison differs from native CSV")
    require(anchor is None and q["at_fixed_anchor"] is None and q["anchor_status"] == "NOT_REACHED", "Unexpected anchor")
    cap_a, cap_b = cap_bracket(x,a), cap_bracket(y,b)
    examples = []
    for u in (.025,.05,.075,.1):
        ao = at_displacement(x,a,u)
        bo = at_displacement(y,b,u)
        if ao is not None and bo is not None:
            examples.append({"u":u, "original_MPa":ao, "relabelled_MPa":bo, "original_minus_relabelled_MPa":ao-bo})
    return {
        "status":"DEVELOPMENT_ONLY", "fixed_u":ANCHOR, "anchor_observed_by_both":False,
        "shared_native_knots":n, "common_end_u":x[n-1], "first_abs_max":point(j),
        "max_signed":point(max(range(n),key=diff.__getitem__)),
        "min_signed":point(min(range(n),key=diff.__getitem__)),
        "max_gap_percent_of_1p2_MPa_cap_descriptive":100*abs(diff[j])/CAP_MPA,
        "illustrative_inside_common_support":examples,
        "original_cap":cap_a,"relabelled_cap":cap_b,
        "linear_cap_u_original_minus_relabelled":cap_a["linear_crossing_u"]-cap_b["linear_crossing_u"],
        "relabelled_points":ob["points_count"],"relabelled_elapsed_s":ob["elapsed_s"],
        "order_qualification_threshold":None,"stage3_go":False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wall",type=Path)
    parser.add_argument("order",type=Path)
    parser.add_argument("--out",type=Path)
    args = parser.parse_args()
    result = json.dumps(readback(args.wall,args.order),indent=2,sort_keys=True,allow_nan=False)+"\n"
    if args.out:
        with args.out.open("x",encoding="ascii",newline="\n") as f:
            f.write(result)
    else:
        print(result,end="")

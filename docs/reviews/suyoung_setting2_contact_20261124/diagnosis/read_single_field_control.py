"""Retrospective S control on native F clock, for localization, with no formal S qualification."""
import argparse
from bisect import bisect_left
import csv
import hashlib
import io
import json
from pathlib import Path
import tarfile


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def curve(archive, label, grid):
    path = f"run/{label}{grid}/"
    name = "receipt.json" if label == "S" else "target_receipt.json"
    proof = json.load(archive.extractfile(path + name))
    trace, observation = (archive.extractfile(path + x).read() for x in ("trace.csv", "observation.json"))
    require(proof["trace_sha256"] == hashlib.sha256(trace).hexdigest()
            and proof["observation_sha256"] == hashlib.sha256(observation).hexdigest(), "bound native files")
    obs = json.loads(observation)
    if label == "S":
        require(obs["field_count"] == 1 and obs["interbody_impulses"] == 0 and obs["physical_disks"] == 49,
                "single-field control")
    rows = list(csv.DictReader(io.StringIO(trace.decode("ascii"))))
    top = float(rows[0]["height"])
    u = [top-float(r["height"]) for r in rows]
    p = [10*float(r["bottom_pressure_E"]) for r in rows]
    dt = float(rows[1]["time_code"])
    require(all(int(r["step"]) == i and float(r["time_code"]) == i*dt for i,r in enumerate(rows))
            and all(a < b for a,b in zip(u,u[1:])) and max(p[:-1]) < 1.2 <= p[-1], "native schedule")
    return u, p, dt, obs


def interpolate(curve, x):
    u, p = curve[:2]
    i = bisect_left(u,x)
    require(0 <= x <= u[-1] and i < len(u), "extrapolation")
    if u[i] == x:
        return p[i]
    return p[i-1] + (x-u[i-1]) / (u[i]-u[i-1]) * (p[i]-p[i-1])


def summarize(inputs, n, f):
    coarse, fine = inputs[n], inputs[f]
    end = min(coarse[0][-1],fine[0][-1])
    knots = sorted({x for arm in (coarse,fine) for x in arm[0] if x <= end})
    rows = [(x,interpolate(coarse,x),interpolate(fine,x)) for x in knots]
    peak = max(abs(b) for _,_,b in rows)
    m,a,b = max(rows, key=lambda q: abs(q[1]-q[2]))
    x,first_a,first_b = next(q for q in rows if 20*abs(q[1]-q[2]) > peak)
    return dict(knots=len(knots), reference_MPa=peak, max_abs_MPa=abs(a-b), ratio=abs(a-b)/peak,
                worst_u_code=m, first_exceedance_u_code=x,
                first_exceedance_coarse_MPa=first_a, first_exceedance_fine_MPa=first_b)


def evaluate(files):
    shas = [hashlib.sha256(x.read_bytes()).hexdigest() for x in files]
    require(shas == ["882c078ba22efab1699773b1c657996933aa2b87b34c8058c62a6a5860f8a0af",
                     "120b5afb767007c3c99d2e51ae95742d665d366a173c492189f800373f068307"], "input identity")
    curves={}
    for path,label in zip(files,("F","S")):
        with tarfile.open(path,"r:gz") as archive:
            curves[label]={k:curve(archive,label,k) for k in (8,12,16,24)}
    for k in (8,12,16,24):
        f,s=curves["F"][k],curves["S"][k]
        size=min(len(f[0]),len(s[0]))
        require(f[0][:size] == s[0][:size] and f[2] == s[2]
                and f[3]["geometry_sha256"] == s[3]["geometry_sha256"]
                and f[3]["identity"]["floor_sha256"] == s[3]["identity"]["floor_sha256"], "common input")
    return dict(label="DEVELOPMENT_ONLY", S_control_only=True, new_model_runs=0, input_sha256=shas,
                by_arm={label:{f"{label}{n}_{label}{f}":summarize(inputs,n,f) for n,f in ((8,16),(12,24))}
                        for label,inputs in curves.items()})


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("F",type=Path)
    p.add_argument("S",type=Path)
    args=p.parse_args()
    print(json.dumps(evaluate((args.F,args.S)), indent=2, allow_nan=False))

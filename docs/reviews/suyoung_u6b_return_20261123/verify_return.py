"""Read the two immutable author returns and independently replay setting 2 U6(b)."""
import argparse
import csv
from decimal import Decimal, localcontext
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


GRIDS = (8, 12, 16, 24)
TARGETS = ("0.84", "0.90", "0.95")
S_RETURN = ("suyoung_u6b_setting2_result.tar.gz",
            "120b5afb767007c3c99d2e51ae95742d665d366a173c492189f800373f068307",
            "a69e28af79a485197133cadb99e68457f23c8b83689e68c83b40ffd37a91f116",
            "c858862722bf6e5eb587ccbd54e1eef7dd59aa27",
            "7647ce296cffe72d4776ce33b8201fd97ca2266bb549e6c479a100802e25eb4b")
F_RETURN = ("suyoung_u6a_setting2_result.tar.gz",
            "882c078ba22efab1699773b1c657996933aa2b87b34c8058c62a6a5860f8a0af",
            "711488b61bf077172335d60de019ca06f7004de4a118f8c15d70268c84b6758c",
            "eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112",
            "7d698c085e250be40fd7d2bfdad7ae84233ddaa847bed4939d69d0ac343834b3")


def require(condition, why):
    if not condition:
        raise ValueError(why)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def load_return(directory, spec):
    name, checksum, screen_hash, pin, source_hash = spec
    raw = (directory/name).read_bytes()
    screen = (directory/"screen.txt").read_bytes()
    require(sha(raw) == checksum and sha(screen) == screen_hash, "TAR or screen hash")
    require(sorted((directory/"SHA256SUMS").read_text("ascii").splitlines()) ==
            sorted([f"{checksum}  {name}", f"{screen_hash}  screen.txt"]), "external manifest")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as t:
        files = {m.name: t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
    require(files["run/RELEASE"].decode("ascii").strip() == pin and
            sha(files["run/SOURCE_SHA256SUMS"]) == source_hash and files["run/screen.txt"] == screen and
            screen.splitlines()[-1] == b"COMMAND_RC=0" and b"AUTOMATIC_RETRIES=0" in screen.splitlines(),
            "source, status or run identity")
    return files


def points(raw, steps, dt, speed):
    """Use Decimal linear interpolation in physical box height, independent of the recorded code."""
    reader = csv.DictReader(io.StringIO(raw.decode("ascii")))
    require(reader.fieldnames == ["step", "time_code", "height", "bottom_pressure_E", "phi_m"], "trace columns")
    with localcontext() as context:
        context.prec = 48
        samples = [(int(r["step"]), float(r["time_code"]), Decimal(r["height"]),
                    Decimal(r["bottom_pressure_E"])*10, Decimal(r["phi_m"])) for r in reader]
        require(len(samples) == steps + 1, "trace count")
        width, reference = samples[0][2], samples[0][2]*samples[0][4]
        for i, (step, time, height, pressure, phi) in enumerate(samples):
            require(step == i and time == dt*i and float(height) == float(width)-speed*time and
                    height > 0 and abs(height*phi-reference) < Decimal("1e-13") and pressure >= 0,
                    "clock, reference area, height or pressure")
        require(samples[0][3] == 0 and max(row[3] for row in samples[:-1]) < Decimal("1.2")
                <= samples[-1][3], "first pressure cap or samples after cap")
        out = {}
        for key in TARGETS:
            ht = reference/Decimal(key)
            value, bracket = None, None
            for (_, _, h0, p0, _), (n, _, h1, p1, _) in zip(samples, samples[1:]):
                if h0 >= ht >= h1:
                    pressure = p0 + (p1-p0)*(ht-h0)/(h1-h0)
                    if pressure <= Decimal("1.2"):
                        value, bracket = float(pressure), [n-1,n]
                    break
            state = "NOT_REACHED" if value is None else ("VALUE" if value > .008 else "NOISE")
            out[key] = dict(pressure_MPa=value, state=state, sample_steps=bracket)
        return out


def same(value, recorded, name):
    if isinstance(value, list) and isinstance(recorded, list):
        require(len(value) == len(recorded), name)
        for a,b in zip(value,recorded):
            same(a,b,name)
    elif isinstance(value, float) and isinstance(recorded,(float,int)):
        require(math.isclose(value,recorded,rel_tol=2e-10,abs_tol=1.5e-11), name)
    else:
        require(value == recorded, name)


def resolution(pressures):
    """Appendix D-1 for the above-noise, fully reached arms in the fixed campaign."""
    logs = [math.log(p) for p in pressures]
    d0, d1, d2 = [b-a for a,b in zip(logs,logs[1:])]
    lo, hi = sorted((1.46*d1,4.23*d1))
    bias = abs(d0) > .02 and (d0 < lo-.02 or d0 > hi+.02)
    a = d1*d2 > 0 and .5*abs(d1) <= abs(d2) <= 1.1*abs(d1)
    pool = [d1,d2] + ([d0] if abs(d0) <= .02 else [])
    rule, interval = "UNCONVERGED", None
    if a:
        rule = "A"
        ends = sorted((logs[-1], logs[-1] + 3*d2))
        interval = [ends[0]-.02, ends[1]+.02]
    elif max(abs(d1),abs(d2)) <= .02 and min(pool) <= 0 <= max(pool):
        rule = "B"
        half = .02 + 3*max(map(abs, pool))
        interval = [logs[-1]-half, logs[-1]+half]
    return dict(rule=rule, interval=interval, d0_d1_d2=[d0,d1,d2], bias_signal=bias,
                noise_signal=(not a and d1*d2 < 0 and max(abs(d1),abs(d2)) > .01),
                suspect_asymptotic=(a and d0*d1 < 0))


def readback(s_directory, f_directory):
    s_files, f_files = load_return(s_directory,S_RETURN), load_return(f_directory,F_RETURN)
    summary = json.loads(s_files["run/summary.json"])
    selected = json.loads(f_files["run/summary.json"])
    require(selected["gate"] == "U6(a)" and selected["assessment"] == "PASS" and
            selected["selected_setting"] == selected["setting"] == summary["setting"] == 2 and
            selected["gap_correction"] and not selected["distance_filter"] and
            summary["release"] == S_RETURN[3] and summary["gate_pin"] == F_RETURN[3] and
            summary["gate_return_sha256"] == F_RETURN[1] and summary["gate"] == "U6(b)" and
            summary["floor_sha256"] == selected["floor_sha256"] and summary["status"] == "DEVELOPMENT_READBACK"
            and not any(summary[k] for k in ("stage3_go","three_dimensional_go","u6_qualified")), "gate binding")
    require(summary["reused_f_arms"] == summary["fresh_s_arms"] == 4 and
            summary["automatic_retries"] == summary["timeouts_this_complete_return"] == 0 and
            list(GRIDS) == summary["original_grids"] == summary["resolutions"], "arm set")
    timing = list(csv.DictReader(io.StringIO(s_files["run/arm_status.tsv"].decode()), delimiter="\t"))
    require(tuple(int(r["grid"]) for r in timing) == GRIDS and
            all(r["process_rc"]=="0" and r["watchdog_status"]=="none" for r in timing), "operator clock")
    results, durations, trace_hash = {}, {}, {}
    for arm, files in (("S", s_files), ("F", f_files)):
        for n in GRIDS:
            name = arm + str(n)
            pre = "run/" + name + "/"
            info = summary["inputs"][name]
            observed = json.loads(files[pre+"observation.json"])
            curve = files[pre+"trace.csv"]
            raw_result = files[pre+"result.json"]
            raw_obs = files[pre+"observation.json"]
            native = json.loads(raw_result)
            rec = json.loads(files[pre+("receipt.json" if arm=="S" else "target_receipt.json")])
            f_ref = selected["arms"][str(n)]
            require(rec["trace_sha256"] == info["trace_sha256"] == native["trace_sha256"] == sha(curve)
                    and rec["result_sha256"] == sha(raw_result) and rec["observation_sha256"] == sha(raw_obs)
                    and native["setting"] == 2 and native["arm"] == arm and
                    native["cells"] == info["cells"] == observed["cells"] == n and
                    native["steps"] == info["steps"] == observed["floor"]["steps"] and
                    native["status"] == info["terminal"] == "TARGET_BRACKETED" and
                    observed["geometry_sha256"] == f_ref["geometry_sha256"] and
                    native["points_count"] == f_ref["points"] and native["elapsed_s"] == info["elapsed_seconds"]
                    and 0 < native["elapsed_s"] <= native["budget_s"], "curve receipt "+name)
            if arm == "F":
                require(rec == f_ref and observed["gap"]["cell_size_gap_correction"] and
                        not observed["gap"]["distance_based_contact_detection"] and
                        observed["interbody_calls"] == native["steps"], "original F identity")
            else:
                require(rec == info and native["field_count"] == observed["field_count"] == 1 and
                        observed["interbody_impulses"] == 0 and observed["material_vertices"] == 49*256 and
                        observed["physical_disks"] == 49 and observed["dt"] == f_ref["dt"] and
                        observed["identity"]["release"] == S_RETURN[3] and
                        observed["checked_single_field_calls"] == native["steps"], "S identity")
            values = points(curve,native["steps"],f_ref["dt"],f_ref["wall_speed"])
            for key, row in values.items():
                recorded = info["points"][key]
                require(recorded["state"] == row["state"], "native target state")
                same(row["pressure_MPa"], recorded["pressure_MPa"], "native target pressure")
            results[name] = values
            durations[name] = native["elapsed_s"]
            trace_hash[name] = sha(curve)
    targets = {}
    for key in TARGETS:
        original = summary["targets"][key]
        common = all(results[a+str(n)][key]["state"] != "NOT_REACHED" for a in ("S","F") for n in GRIDS)
        same(common, original["common"], "common target")
        arms = {}
        for arm in ("S","F"):
            values = [results[arm+str(n)][key]["pressure_MPa"] for n in GRIDS]
            ref = original["arms"][arm]
            rule = None
            if common:
                require(all(p > .008 for p in values), "outside this return's above-noise comparison")
                rule = resolution(values)
                for k,v in rule.items():
                    same(v, ref["resolution"][k], "resolution "+k)
            else:
                require(ref["resolution"] is None, "noncommon arm resolution")
            same(None if rule is None else rule["interval"], ref["ln_pressure_interval"], "arm interval")
            arms[arm] = dict(pressures_MPa=values, resolution=rule)
        require(original["ln_S_over_F_interval_report_only"] is None and
                all(arms[a]["resolution"] is None or arms[a]["resolution"]["interval"] is None for a in arms),
                "ratio requires two pressure intervals")
        targets[key] = dict(common=common, arms=arms, ln_S_over_F_interval=None)
    return dict(label="DEVELOPMENT_ONLY", gate="U6(b)", setting=2, release=S_RETURN[3],
                return_sha256=S_RETURN[1], screen_sha256=S_RETURN[2], reused_f_return_sha256=F_RETURN[1],
                grid_order=list(GRIDS), targets=targets, elapsed_seconds_by_arm=durations,
                new_s_total_seconds=sum(durations["S"+str(n)] for n in GRIDS),
                operator_seconds=sum(int(r["elapsed_s"]) for r in timing), timeout_count=0,
                automatic_retries=0, trace_sha256=trace_hash,
                requested_target_cells_by_arm={"S":12,"F":12},
                reached_target_cells_by_arm={a:sum(results[a+str(n)][k]["state"] != "NOT_REACHED"
                             for n in GRIDS for k in TARGETS) for a in ("S","F")},
                target_steps={name:{k:v["sample_steps"] for k,v in points_.items()}
                              for name,points_ in results.items()},
                new_compression_runs_during_readback=0, u6_qualified=False, stage3_go=False, three_dimensional_go=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("s_return_directory",type=Path)
    parser.add_argument("f_return_directory",type=Path)
    parser.add_argument("--out",type=Path)
    args = parser.parse_args()
    data = json.dumps(readback(args.s_return_directory, args.f_return_directory), indent=2, allow_nan=False)+"\n"
    if args.out is None:
        print(data,end="")
    else:
        with args.out.open("x",encoding="ascii",newline="\n") as stream:
            stream.write(data)

"""Reconstruct the completed F8/F16 decision from the three named author archives."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import tarfile


HERE = Path(__file__).resolve().parent
RELEASE = "c0e077ad5961d7be8dd801ea2f527b76089b362a"
PARSER_SHA = "f3eb1aa342e97e5accd9619230b695e523d9113035937daf676b29c88b498d3a"
ARCHIVES = {
    "full": "aa0f2ad7126a65654975de6a741a58b49c57a5cc84c42983b226ddca15212b65",
    "prefix": "57d0a6fe178b2faf0545013ef43b9ff6d175c1fdb18e93522ec8dcb8eb1b7e34",
    "old": "fc685932f4a1710fe944c5d2dafbcb56bf239f473184f009983a3ff4805dabea",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def contents(path, key):
    with path.open("rb") as src:
        require(hashlib.file_digest(src, "sha256").hexdigest() == ARCHIVES[key], key + " archive")
        src.seek(0)
        with tarfile.open(fileobj=src, mode="r:gz") as tar:
            result = {}
            seen = set()
            for entry in tar:
                p = PurePosixPath(entry.name)
                require(p.parts and p.parts[0] == "run" and ".." not in p.parts and p not in seen
                        and (entry.isfile() or entry.isdir()), "unexpected tar member")
                seen.add(p)
                if entry.isfile():
                    result[p.relative_to("run").as_posix()] = tar.extractfile(entry).read()
    return result


def native_parser():
    file = HERE.parent / "suyoung_floor_full_20261123/full_compare.py"
    require(sha(file.read_bytes()) == PARSER_SHA, "native reader identity")
    spec = importlib.util.spec_from_file_location("floor_native_reader", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reduced(pair):
    return {key: pair[key] for key in (
        "samples", "max_abs_difference_MPa", "fixed_reference_ratio", "fixed_reference_comparison",
        "fixed_reference_first_exceedance", "first_worst")}


def read(args):
    full, prefix, old = (contents(getattr(args, k), k) for k in ("full", "prefix", "old"))
    meta = json.loads(full["summary.json"])
    screen = full["screen.txt"].decode("ascii").splitlines()
    require(meta["release"] == full["RELEASE"].decode().strip() == RELEASE and
            sha(full["SOURCE_SHA256SUMS"]) == meta["source_manifest_sha256"] and
            meta["prior_return_sha256"] == ARCHIVES["prefix"] and
            meta["both_native_terminated"] and meta["both_reached_target"] and
            meta["u6_qualified"] is False and meta["stage3_go"] is False and
            all(screen.count(flag) == 1 for flag in ("F8_RC=0", "F16_RC=0", "COMMAND_RC=0")), "release or status")
    require(args.screen.read_bytes() == full["screen.txt"] and
            sha(full["screen.txt"]) == "37aa078fb8079c655d88e24ff779048a78d1c8f131dc77c954ae4b41c1836595",
            "screen")
    parser = native_parser()
    schedules = {}
    curves = {}
    per_arm = {}
    for arm in ("F8", "F16"):
        path = arm + "/trace.csv"
        rec = json.loads(full[arm+"/full_receipt.json"])
        result = json.loads(full[arm+"/result.json"])
        before = prefix["candidate/"+path]
        raw = full[path]
        require(rec == meta["arms"][arm] and sha(raw) == rec["trace_sha256"] == result["trace_sha256"]
                and sha(full[arm+"/result.json"]) == rec["result_sha256"]
                and rec["prior_trace_sha256"] == sha(before) and raw.startswith(before)
                and result["status"] == rec["terminal_reason"] == "TARGET_BRACKETED", arm + " receipt")
        schedules[arm] = rec["dt"]
        for name, archive in (("previous", old), ("candidate", full)):
            run = json.loads(archive[arm+"/result.json"])
            data = archive[path]
            require(run["status"] == "TARGET_BRACKETED" and run["trace_sha256"] == sha(data), name + arm)
            curves[name,arm] = parser.read_native(data, rec["width"], rec["wall_speed"], rec["dt"], run["status"])
        u, pressure = curves["candidate",arm]
        onset = next(i for i,p in enumerate(pressure) if p>0.)
        require(onset == rec["first_nonzero_step"] and len(u)-1 == rec["terminal_step"], arm + " onset")
        per_arm[arm] = dict(first_positive_step=onset, first_positive_displacement_diameters=u[onset]/.1,
                            first_positive_MPa=pressure[onset], terminal_step=len(u)-1,
                            terminal_displacement_diameters=u[-1]/.1, terminal_MPa=pressure[-1],
                            elapsed_seconds=result["elapsed_s"], stable_prefix_rows=len(before.splitlines())-1)
    pairs = {}
    for model, archive in (("previous",old),("candidate",full)):
        pair = parser.compare_pair(archive["F8/trace.csv"],archive["F16/trace.csv"],width=rec["width"],
                                   speed=rec["wall_speed"],dt8=schedules["F8"],dt16=schedules["F16"],
                                   terminal8="TARGET_BRACKETED",terminal16="TARGET_BRACKETED")
        if model == "candidate":
            require(pair == meta["comparison"], "reported pair vs native samples")
        pairs[model] = {kind:reduced(pair[kind]) for kind in ("common","both_positive_knots")}
    # Compare the wall changes again on *identical* support for all four traces.
    common_end = min(u[-1] for u,p in curves.values())
    knots = sorted({x for u,p in curves.values() for x in u if x <= common_end})
    trace_at = {}
    for name, (u,p) in curves.items():
        trace_at[name] = [parser.interpolate(x,u,p)[0] for x in knots]
    four = {}
    for model in ("previous","candidate"):
        gaps = [a-b for a,b in zip(trace_at[model,"F8"],trace_at[model,"F16"])]
        i = max(range(len(gaps)),key=lambda j:abs(gaps[j]))
        four[model] = dict(peak_MPa=abs(gaps[i]), peak_pct=100*abs(gaps[i])/parser.FIXED_REFERENCE_MPA,
                          at_displacement_diameters=knots[i]/.1)
    return dict(label="DEVELOPMENT_ONLY", release=RELEASE, archives=ARCHIVES, arms=per_arm,
                reference_MPa=parser.FIXED_REFERENCE_MPA, pairs=pairs,
                four_curve_common=dict(knots=len(knots), end_diameters=common_end/.1, peaks=four),
                coarse_result=pairs["candidate"]["common"]["fixed_reference_comparison"],
                finer_pair_status="UNMEASURED", u6_qualified=False, stage3_go=False)


if __name__ == "__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    for k in ("full","prefix","old","screen"):
        cli.add_argument("--"+k, type=Path, required=True)
    print(json.dumps(read(cli.parse_args()),indent=2,allow_nan=False))

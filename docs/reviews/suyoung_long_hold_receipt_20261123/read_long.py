"""Read a completed fixed-height return as historical development evidence, without running its code."""
import argparse
import csv
from datetime import datetime
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import re
import tarfile


PIN = "206dd6dd00547237fba2ef577098a448263b7736"
SOURCE = "695a5a5586cbb3f3d33a3507b52dddb9ccf072e97f87b7c3397bd8c9feebce66"
OLD = "218f4b4b784a63ededdefefba92a8160e41c86bc56f0e2c121febc7cd4ff4cf2"
OLD_PIN = "cf81ed8a70fd4c6b7b65874f45920c31c0871ee9"
OLD_SOURCE = "d0f0783801d4b826cf9dd8b7fd5b86d4e7c8bdfa77371f080c6cdce8be1061c4"
INPUTS = {
    "PRIOR_DEPTH_SHA256": "cd9b0e6b9ce31719716b3ae4b9f97734a7a4ba3614c7de7bd3d93d44f3be83e6",
    "PRIOR_HALF_SPEED_SHA256": "ddcf2fd738430c40246d177d1e1dea73de24883c07218e4f07c0dcf6de90f863",
    "PRIOR_MATERIAL_LID_SHA256": "cdd3ff1dcdbe02dcb6493a4112a0136076883f2179c33f322e2287c0ffdfb14e",
    "PRIOR_BALANCE_SHA256": "1f680f4f255910bb2c93ce7e2edea004c89b4177fb3a4b8af93bd59edeab209e",
    "PRIOR_QUARTER_SHA256": "5bee9a0cc9f92ba88fd7039444c7efb71bb8946c84912159d6a23838f8399d04",
    "PRIOR_SHORT_HOLD_SHA256": OLD,
}
OBS = ("trace.csv", "wall_steps.csv", "layer_steps.csv", "particle_momentum.csv", "energy.csv")
LOCKS = ("u6_qualified", "stage3_go", "three_dimensional_go")


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def archive(path):
    """Validate the two-file outer manifest, exact screen copy and archive paths."""
    raw = path.read_bytes()
    screen = (path.parent / "screen.txt").read_bytes()
    expected = {path.name: sha(raw), "screen.txt": sha(screen)}
    lines = (path.parent / "SHA256SUMS").read_text(encoding="ascii").splitlines()
    listed = [line.split("  ", 1) for line in lines]
    require(len(listed) == 2 and {n: h for h, n in listed} == expected, "return manifest")
    files, times, seen = {}, {}, set()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        for member in tar:
            key = PurePosixPath(member.name)
            require(key.parts and key.parts[0] == "run" and ".." not in key.parts and str(key) == member.name
                    and not re.search(r"[:\\\x00\r\n]", member.name) and member.name.casefold() not in seen
                    and (member.isdir() or member.isfile()), "unexpected or duplicate return member")
            seen.add(member.name.casefold())
            if member.isfile():
                name = key.relative_to("run").as_posix()
                files[name] = tar.extractfile(member).read()
                times[name] = member.mtime
    require(files["screen.txt"] == screen, "inner screen")
    return files, times, expected


def close(actual, trusted):
    require(math.isclose(actual, trusted, rel_tol=2e-11, abs_tol=2e-14), "stored observation disagrees with raw samples")


def parse_table(raw):
    return list(csv.DictReader(io.StringIO(raw.decode("ascii"))))


def stats_for_arm(n, new, old, times, meta, summary, previous):
    multiple = n // 12
    ramp, short, held = 1638*multiple, 1200*multiple, 4800*multiple
    prefix = f"F{n}/"
    arm = summary["arms"][str(n)]
    prior = previous["arms"][str(n)]
    rec = json.loads(new[prefix+"hold_receipt.json"])
    prior_rec = json.loads(old[prefix+"hold_receipt.json"])
    boundary = json.loads(new[prefix+"old_hold_boundary.json"])
    result = json.loads(new[prefix+"long_hold_receipt.json"])
    require(rec == arm["receipt"] and prior_rec == prior["receipt"] and arm["windows"] == prior["windows"]
            and rec["grid"] == n and rec["fork"] == prior_rec["fork"] == boundary["fork"], "prior fork/observations")
    require(boundary["step"] == result["short_hold_replayed"] == ramp+short
            and boundary["previous_return_sha256"] == OLD and boundary["status"] == "SHORT_HOLD_PREFIX_REPLAYED"
            and result["status"] == "LONG_HOLD_ARM_COMPLETE" and result["hold_steps"] == held
            and result["ramp_steps"] == ramp and rec["status"] == "HOLD_ARM_COMPLETE"
            and result["arm_receipt_sha256"] == sha(new[prefix+"hold_receipt.json"])
            and result["boundary_receipt_sha256"] == sha(new[prefix+"old_hold_boundary.json"]), "arm or boundary receipt")
    for receipt in (rec, result, boundary):
        require(receipt["grid"] == n and receipt["release"] == PIN and receipt["source_sha256"] == SOURCE
                and receipt["fixed_return_sha256"] == OLD and all(receipt[k] is False for k in LOCKS), "receipt source/scope")
    names = set((*OBS,"layer_spec.json"))
    require(set(rec["hashes"]) == set(prior_rec["hashes"]) == names and set(boundary["prefix_sha256"]) == set(OBS), "arm hash coverage")
    for name in names:
        buf, original = new[prefix+name], old[prefix+name]
        require(sha(buf) == rec["hashes"][name] and sha(original) == prior_rec["hashes"][name], "arm observation hash")
        if name in OBS:
            require(buf.startswith(original) and sha(original) == boundary["prefix_sha256"][name], "short history mismatch")
        else:
            require(buf == original, "layer definition changed")
    trace = parse_table(new[prefix+"trace.csv"])
    energy = parse_table(new[prefix+"energy.csv"])
    walls = parse_table(new[prefix+"wall_steps.csv"])
    require(len(trace) == len(energy) == len(walls)+1 == ramp+held+1, "unexpected native steps")
    dt = float(trace[1]["time_code"])
    width = float(trace[0]["height"])
    height = float(trace[ramp]["height"])
    require(all(int(trace[i]["step"]) == int(energy[i]["step"]) == int(walls[i-1]["step"]) == i
                and float(trace[i]["height"]) == height and float(trace[i]["time_code"]) == i*dt
                and energy[i]["phase"] == "hold" and float(energy[i]["plate_speed"]) == 0
                for i in range(ramp+1, ramp+held+1)), "stationary clock")
    close(arm["locked_height"], height)
    close(arm["hold_time"], held*dt)
    limit = {12:2400, 24:7200}[n]
    require(result["budget_seconds"] == rec["budget_seconds"] == int(meta[f"F{n}_BUDGET_SECONDS"]) == limit, "time budget")
    started = datetime.fromisoformat(meta[f"F{n}_BEGIN"]).timestamp()
    receipt_time = times[prefix+"long_hold_receipt.json"]
    late = []
    span = 300*multiple
    for i in range(12,16):
        start, stop = ramp+i*span, ramp+(i+1)*span
        pressures = [float(row["bottom_pressure_E"])*10 for row in trace[start+1:stop+1]]
        floor = math.fsum(pressures)/span
        contact = math.fsum(float(row["floor_impulse"]) for row in walls[start:stop])*10/(dt*width*span)
        energy_mean = math.fsum(float(row["particle_ke"]) for row in energy[start+1:stop+1])/span
        native = summary["windows"][i][f"F{n}"]
        close(floor,contact)
        close(floor,native["floor_mean_MPa"])
        close(energy_mean,native["particle_ke"]["mean"])
        close(floor,summary["last_four_windows"][f"F{n}_floor_mean_MPa"]["values"][i-12])
        close(energy_mean,summary["last_four_windows"][f"F{n}_particle_ke"]["values"][i-12])
        late.append({"floor_MPa": floor, "particle_kinetic_energy_model_units": energy_mean})
    return dict(ramp_steps=ramp, hold_steps=held, windows_verified=4, previous_csv_prefixes_verified=5,
                begin_utc=meta[f"F{n}_BEGIN"], budget_s=limit,
                begin_to_long_receipt_approx_seconds=round(receipt_time-started), late=late)


def read(path, old_path):
    new, times, sums = archive(path)
    old, _, old_sums = archive(old_path)
    require(old_sums[old_path.name] == OLD and old["RELEASE"].decode().strip() == OLD_PIN
            and sha(old["SOURCE_SHA256SUMS"]) == OLD_SOURCE, "previous return identity")
    require(new["RELEASE"].decode("ascii").strip() == PIN and sha(new["SOURCE_SHA256SUMS"]) == SOURCE, "new release/manifest")
    lines = new["screen.txt"].decode("ascii").splitlines()
    metadata = dict(x.split("=",1) for x in lines if "=" in x)
    require(metadata["RELEASE"] == PIN and all(metadata[k] == v for k,v in INPUTS.items())
            and metadata["RETRIES"] == "0" and metadata["HOLD_SPEED"] == "0"
            and float(metadata["RAMP_SPEED_RATIO"]) == .25, "operator identity")
    if metadata.get("COMMAND_RC") != "0":
        require("incomplete.json" in new and lines[-1] == "COMMAND_RC="+metadata["COMMAND_RC"], "incomplete receipt")
        return dict(label="DEVELOPMENT_ONLY", status="INCOMPLETE", phase=json.loads(new["incomplete.json"])["phase"],
                    operator_rc=int(metadata["COMMAND_RC"]), author_tar_sha256=sums[path.name], screen_sha256=sums["screen.txt"])
    require(lines[-1] == "COMMAND_RC=0" and "LONG_HOLD_READBACK_COMPLETE" in lines
            and metadata["F12_RC"] == metadata["F24_RC"] == "0" and "incomplete.json" not in new, "completion status")
    s, prior = (json.loads(a["summary.json"]) for a in (new,old))
    require(s["status"] == "LONG_HOLD_PAIR_COMPLETE" and s["qualification_basis"] == "fixed_height_transient_development_only"
            and s["release"] == PIN and s["source_sha256"] == SOURCE and s["fixed_return_sha256"] == OLD
            and s["short_hold_pin"] == prior["release"] == OLD_PIN and s["quarter_return_sha256"] == prior["quarter_return_sha256"]
            and all(s[k] is False for k in LOCKS), "result identity/scope")
    require(len(s["windows"]) == 16 and s["previous_windows"] == 4 and s["extension_windows"] == 12
            and [w["index"] for w in s["windows"]] == list(range(1,17))
            and [w["source"] for w in s["windows"]] == ["previous"]*4+["extension"]*12, "window indices")
    arms = {n:stats_for_arm(n,new,old,times,metadata,s,prior) for n in (12,24)}
    gaps = []
    for idx,window in enumerate(s["windows"][12:]):
        gap = arms[12]["late"][idx]["floor_MPa"]-arms[24]["late"][idx]["floor_MPa"]
        close(gap,window["F12_minus_F24"]["floor_MPa"]["mean"])
        close(gap,s["last_four_windows"]["F12_minus_F24_floor_MPa"]["values"][idx])
        gaps.append(gap)
    return dict(label="DEVELOPMENT_ONLY", purpose="historical_fixed_height_return", u6a_used=False,
                status="COMPLETE", release=PIN, author_tar_sha256=sums[path.name], screen_sha256=sums["screen.txt"],
                source_manifest_sha256=SOURCE, previous_fixed_tar_sha256=OLD, previous_csv_prefixes_verified=10,
                timeouts_observed=0, retries=0, total_windows=16, last_four_windows=[13,14,15,16],
                arms=arms, late_signed_floor_gap_MPa=gaps, new_research_runs_for_readback=0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("long_tar",type=Path)
    parser.add_argument("short_tar",type=Path)
    args = parser.parse_args()
    print(json.dumps(read(args.long_tar,args.short_tar), indent=2, allow_nan=False))

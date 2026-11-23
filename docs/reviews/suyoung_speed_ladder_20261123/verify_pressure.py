"""Read fixed original-, half-, and quarter-speed author returns; no simulation."""
import argparse
import csv
from dataclasses import dataclass
from hashlib import sha256
import io
import json
import math
from pathlib import Path
import tarfile


REF = 0.6636991102836952
DIAMETER = .1
HISTORIES = {
    "original": (1, "cdd3ff1dcdbe02dcb6493a4112a0136076883f2179c33f322e2287c0ffdfb14e",
                 "35099db02148c1a5dc2581f880e0adbf28c0368d", "candidate_receipt"),
    "half": (2, "ddcf2fd738430c40246d177d1e1dea73de24883c07218e4f07c0dcf6de90f863",
             "ba0e2bb980a4f098aee6ee526d069ed2d2446151", "half_speed_receipt"),
    "quarter": (4, "5bee9a0cc9f92ba88fd7039444c7efb71bb8946c84912159d6a23838f8399d04",
                "4a56e468c931e024d08f5476df9ccb0237694741", "quarter_speed_receipt"),
}


def require(ok, description):
    if not ok:
        raise ValueError(description)


def agree(a, b, name):
    require(math.isclose(a, b, rel_tol=2e-12, abs_tol=2e-12), name)


def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("ascii"), newline="")))


@dataclass
class Arm:
    height: list
    pressure: list
    time: list
    wall: list
    motion: list


def read_case(path, speed):
    scale, digest, pin, receipt_name = HISTORIES[speed]
    data = path.read_bytes()
    require(sha256(data).hexdigest() == digest, "return SHA256 " + speed)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        members = tar.getmembers()
        require(len({m.name for m in members}) == len(members), "duplicate archive path")
        def raw(name):
            member = tar.getmember("run/" + name)
            require(member.isfile(), "regular member")
            return tar.extractfile(member).read()
        receipt = json.loads(raw("summary.json"))
        require(receipt["release"] == pin == raw("RELEASE").decode().strip(), "release")
        require(receipt["source_sha256"] == sha256(raw("SOURCE_SHA256SUMS")).hexdigest(), "source binding")
        require(receipt["label"] == "DEVELOPMENT_ONLY" and receipt["reference_MPa"] == REF and
                all(receipt[k] is False for k in ("stage3_go","u6_qualified","three_dimensional_go")), "scope")
        screen = raw("screen.txt").decode().splitlines()
        require(screen[-1] == "COMMAND_RC=0" and {"F12_RC=0", "F24_RC=0"} <= set(screen), "completed screen")
        arms = {}
        for n in (12, 24):
            key = f"F{n}/"
            rec = json.loads(raw(key + receipt_name + ".json"))
            steps = 569 * (n // 12) * scale
            require(rec == receipt["arms"][str(n)] and rec["steps"] == steps and rec["release"] == pin, "arm receipt")
            def bound(name, hash_key, data_rows, first):
                blob = raw(key + name)
                require(sha256(blob).hexdigest() == rec[hash_key], "CSV binding " + name)
                items = rows(blob)
                require(len(items) == data_rows and all(int(r["step"]) == i for i,r in enumerate(items,first)), "row identity " + name)
                return items
            trace = bound("trace.csv","trace_sha256",steps+1,0)
            wall = bound("wall_steps.csv","wall_csv_sha256",steps,1)
            motion = [] if scale == 1 else bound("particle_momentum.csv","particle_momentum_sha256",steps,1)
            height = [float(r["height"]) for r in trace]
            p = [10*float(r["bottom_pressure_E"]) for r in trace]
            t = [float(r["time_code"]) for r in trace]
            require(t[0] == 0 and p[0] == 0 and all(a>b for a,b in zip(height,height[1:])), "time zero or decreasing height")
            a = arms[n] = Arm(height,p,t,wall,motion)
            for i,w in enumerate(wall,1):
                agree(t[i], i*t[1], "solver clock")
                f,l = float(w["floor_impulse"]),float(w["lid_signed_impulse"])
                require(f >= 0 and l <= 0, "wall impulse sign")
                agree(f*10/(height[0]*t[1]), p[i], "trace pressure vs native impulse")
                if motion:
                    m = a.motion[i-1]
                    before, after = float(m["particle_Py_before"]),float(m["particle_Py_after"])
                    agree(after-before,f+l,"signed momentum balance")
                    agree(after-before,float(m["particle_delta_Py"]), "stored vs direct difference")
    return arms, receipt


def native_union(arms):
    """Use F24 native knots; interpolate only F12 at the intervening actual heights."""
    a,b = arms[12],arms[24]
    require(len(b.height) == 2*len(a.height)-1, "nested clock")
    out = []
    for i,h in enumerate(b.height):
        j = i//2
        if i%2:
            h0,h1 = a.height[j:j+2]
            require(h0 > h > h1, "non-overlapping heights")
            weight = (h0-h)/(h0-h1)
            coarse = a.pressure[j]*(1-weight)+a.pressure[j+1]*weight
        else:
            require(h == a.height[j], "mismatched native heights")
            coarse = a.pressure[j]
        fine = b.pressure[i]
        out.append(dict(step_F24=i, displacement_D=(b.height[0]-h)/DIAMETER,
                        F12_MPa=coarse,F24_MPa=fine,gap_MPa=coarse-fine))
    return out


def statistics(samples):
    peak = max(samples, key=lambda r: abs(r["gap_MPa"]))
    first = next((r for r in samples if abs(r["gap_MPa"]) > .05*REF), None)
    return dict(count=len(samples),max_abs_MPa=abs(peak["gap_MPa"]),
                max_percent=100*abs(peak["gap_MPa"])/REF,peak=peak,first_above=first)


def impulse_window(arm, end, count):
    """End index is a 1-based native step; assess an actual window without temporal interpolation."""
    require(0 < count <= end <= len(arm.wall), "window bounds")
    wall = arm.wall[end-count:end]
    norm = 10/(arm.height[0]*arm.time[1]*count)
    floor = math.fsum(float(r["floor_impulse"]) for r in wall)*norm
    lid = math.fsum(-float(r["lid_signed_impulse"]) for r in wall)*norm
    py = ((float(arm.motion[end-1]["particle_Py_after"])-float(arm.motion[end-count]["particle_Py_before"]))*norm
          if arm.motion else None)
    return dict(floor_MPa=floor,lid_down_MPa=lid,floor_over_lid=(floor/lid if lid else None),
                inferred_momentum_MPa=floor-lid,direct_momentum_MPa=py)


def pair_window(arms, step):
    if step%2 or step==0:
        return None
    coarse = impulse_window(arms[12],step//2,1)
    fine = impulse_window(arms[24],step,1)
    same = impulse_window(arms[24],step,2)
    def diff(target):
        return {k:(None if coarse[k] is None else coarse[k]-target[k]) for k in
                ("floor_MPa","lid_down_MPa","inferred_momentum_MPa","direct_momentum_MPa")}
    return dict(F12=coarse,F24=fine,F12_minus_F24=diff(fine),
                F24_two_steps=same,F12_minus_F24_same_duration=diff(same))


def arrival(arm):
    i = next(i for i,w in enumerate(arm.wall,1) if float(w["floor_impulse"])>0)
    j = next(i for i,w in enumerate(arm.wall,1) if float(w["floor_gap_after"])<=0.)
    require(i == j, "floor impulse and closed transported minimum gap at different steps")
    return dict(step=i, time_code=arm.time[i], displacement_D=(arm.height[0]-arm.height[i])/DIAMETER)


def delay_diagnostic(coarse, fine, delay_steps, native_peak_step, common_peak_step, first_crossing=None):
    """Hold the independently measured floor-onset delay; compare only overlapping native F12 steps."""
    require(len(fine.time)==2*len(coarse.time)-1, "delay grid lengths")
    agree(coarse.time[1],2*fine.time[1],"delay grid spacing")
    # Intersect common-time and shifted-time domains; negative delays are admissible too.
    first=max(0,-(delay_steps//2))
    last=min(len(coarse.time)-1, (len(fine.time)-1-delay_steps)//2)
    require(first<=last,"no common native F12 support for shift")
    def pair_at(step):
        lo,intervening=divmod(step,2)
        if not intervening:
            p=coarse.pressure[lo]
            height=coarse.height[lo]
        else:
            height=fine.height[step]
            h0,h1=coarse.height[lo:lo+2]
            require(h0>height>h1,"delay marker interpolation support")
            w=(h0-height)/(h0-h1)
            p=coarse.pressure[lo]*(1-w)+coarse.pressure[lo+1]*w
        j=step+delay_steps
        return dict(F12_bracketing_steps=[lo,lo+intervening],F12_interpolated=bool(intervening),
                    original_F24_step=step,aligned_F24_step=j,original_displacement_D=(coarse.height[0]-height)/DIAMETER,
                    aligned_F24_displacement_D=(fine.height[0]-fine.height[j])/DIAMETER,
                    same_time_gap_MPa=p-fine.pressure[step],aligned_gap_MPa=p-fine.pressure[j])
    samples=[pair_at(2*i) for i in range(first,last+1)]
    def marker(step):
        return pair_at(step) if 2*first<=step<=2*last else None
    return dict(label="DEVELOPMENT_DIAGNOSTIC_DIFFERENT_PLATE_DISPLACEMENTS_ONLY",use_for_qualification=False,
                delay_F24_steps=delay_steps,delay_time_code=delay_steps*fine.time[1],comparison_samples=len(samples),
                F12_first_step=first,F12_last_step=last,same_time_peak=max(samples,key=lambda r:abs(r["same_time_gap_MPa"])),
                aligned_peak=max(samples,key=lambda r:abs(r["aligned_gap_MPa"])),
                at_original_native_peak=marker(native_peak_step),at_original_common_peak=marker(common_peak_step),
                at_first_common_crossing=marker(first_crossing) if first_crossing is not None else None)


def check_summary(observed, registered):
    require(observed["count"] == registered["samples"], "declared sample count")
    agree(observed["max_percent"],registered["fixed_reference_percent"],"declared fixed percent")
    for key in ("peak","first_above"):
        record, expected = observed[key], registered[key]
        for our,their in (("displacement_D","displacement_diameters"),("gap_MPa","signed_gap_MPa"),
                          ("F12_MPa","F12_MPa"),("F24_MPa","F24_MPa")):
            agree(record[our],expected[their], "declared "+key+" "+our)


def evaluate(paths):
    report = dict(label="DEVELOPMENT_ONLY",fixed_reference_MPa=REF,qualification="HOLD",speeds={})
    wide = []
    arms_ref = None
    for name in HISTORIES:
        scale = HISTORIES[name][0]
        arms, receipt = read_case(paths[name],name)
        all_rows = native_union(arms)
        shared = all_rows[::scale]
        native, common = statistics(all_rows), statistics(shared)
        require(len(shared)==1139 and len(all_rows)==1138*scale+1, "sample sizes")
        if name=="original":
            check_summary(native,receipt["new_material_lid"])
            arms_ref = arms
            wide = [dict(step_F24_original=r["step_F24"],displacement_D=r["displacement_D"]) for r in shared]
        else:
            historic = receipt["pressure_union"]
            check_summary(native,historic[f"{name}_native_{len(all_rows)}"])
            check_summary(common,historic["half_on_original_1139" if name=="half" else "quarter_on_common_1139"])
        for i,(target,r) in enumerate(zip(wide,shared,strict=True)):
            require(arms[24].height[i*scale] == arms_ref[24].height[i], "speed-varying comparison knot")
            for k in ("F12_MPa","F24_MPa","gap_MPa"):
                target[name+"_"+k] = r[k]
        markers = {"anchor_0p139D":shared[930], "anchor_0p170D":shared[1138],
                   "common_peak":common["peak"], "native_peak":native["peak"],
                   "common_first_above":common["first_above"], "native_first_above":native["first_above"]}
        onsets={n:arrival(a) for n,a in arms.items()}
        delay=onsets[24]["step"]-2*onsets[12]["step"]
        first = common["first_above"]
        phase=delay_diagnostic(arms[12],arms[24],delay,native["peak"]["step_F24"],common["peak"]["step_F24"],
                               first["step_F24"] if first else None)
        report["speeds"][name] = dict(common=common,native=native,floor_arrival=onsets, onset_delay_diagnostic=phase,
                                  at={k:dict(pressure=r,impulse=pair_window(arms,r["step_F24"])) if r is not None else None
                                      for k,r in markers.items()})
    return report,wide


if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    for k in (*HISTORIES,"json","csv"):
        cli.add_argument(k,type=Path)
    args=cli.parse_args()
    report,wide=evaluate({k:getattr(args,k) for k in HISTORIES})
    args.json.write_bytes((json.dumps(report,indent=2,allow_nan=False)+"\n").encode("ascii"))
    with args.csv.open("w",newline="",encoding="ascii") as out:
        writer=csv.DictWriter(out,fieldnames=tuple(wide[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(wide)

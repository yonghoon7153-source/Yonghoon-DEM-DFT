"""Offline pressure and particle-motion readback from two pinned author returns."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import tarfile


FIXED = ("218f4b4b784a63ededdefefba92a8160e41c86bc56f0e2c121febc7cd4ff4cf2",
         "cf81ed8a70fd4c6b7b65874f45920c31c0871ee9",
         "d0f0783801d4b826cf9dd8b7fd5b86d4e7c8bdfa77371f080c6cdce8be1061c4",
         "1939d24401626de69eedb765ca9643dfd932b72d4066cc5ebbdce68be48008e6")
QUARTER = ("5bee9a0cc9f92ba88fd7039444c7efb71bb8946c84912159d6a23838f8399d04",
           "4a56e468c931e024d08f5476df9ccb0237694741",
           "8d8f1cd80492f264857a459ce8775da93cd7adb2330d224dc83699e2c88391de",
           "d6d2527e39cd7a41c52dc2c8a366f45d23cd1b5fbc55ddf7aa0cf7c524a5f119")
REFERENCE = .6636991102836952
RAMP = {12:1638, 24:3276}
HOLD = {12:1200, 24:2400}
OLD_KEYS = {"trace.csv":"trace_sha256","wall_steps.csv":"wall_csv_sha256",
            "layer_steps.csv":"layer_sha256","particle_momentum.csv":"particle_momentum_sha256"}
LAYERS = ("lower","middle","upper")
NAMES = ("first_300","overlap_last_300","late_1","late_2")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def near(a,b,what):
    require(math.isclose(a,b,abs_tol=2e-11,rel_tol=2e-11),what)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_sidecars(path, identity):
    manifest = (path.parent / "SHA256SUMS").read_text(encoding="ascii").splitlines()
    expected = {path.name: identity[0], "screen.txt": identity[3]}
    listed = [line.split("  ", 1) for line in manifest]
    require(len(listed) == len(expected)
            and all(len(pair) == 2 for pair in listed)
            and {name: digest for digest, name in listed} == expected, "sidecar manifest")
    require(sha((path.parent / "screen.txt").read_bytes()) == identity[3], "external screen hash")


def archive(path, identity):
    data = path.read_bytes()
    require(sha(data)==identity[0],"outer hash")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data),mode="r:gz") as tar:
        for item in tar:
            if item.isdir():
                continue
            key = PurePosixPath(item.name)
            require(item.isfile() and key.parts[0]=="run" and ".." not in key.parts
                    and not key.is_absolute() and item.name not in files,"tar members")
            files[item.name] = tar.extractfile(item).read()
    summary = json.loads(files["run/summary.json"])
    require(identity[1] == summary["release"] == files["run/RELEASE"].decode("ascii").strip()
            and sha(files["run/SOURCE_SHA256SUMS"]) == summary["source_sha256"] == identity[2]
            and sha(files["run/screen.txt"])==identity[3],"release/source/screen binding")
    screen = files["run/screen.txt"].decode("ascii").splitlines()
    require("F12_RC=0" in screen and "F24_RC=0" in screen and screen[-1]=="COMMAND_RC=0","arm completion")
    require(summary["label"]=="DEVELOPMENT_ONLY" and all(summary[k] is False for k in
            ("stage3_go","three_dimensional_go","u6_qualified")),"scope")
    near(summary["reference_MPa"],REFERENCE,"reference pressure")
    return files,summary


def csv_rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode("ascii"), newline="")))


def bound_prefix(new,old,rows):
    a,b = (raw.splitlines(keepends=True) for raw in (new,old))
    require(rows>=1 and len(a)>rows and len(b)>rows and a[:rows+1]==b[:rows+1],"fork prefix")
    return sha(b"".join(a[:rows+1]))


def mean(xs):
    return math.fsum(xs)/len(xs)


def range_stats(xs):
    require(xs and all(map(math.isfinite,xs)),"non-finite or empty series")
    return dict(mean=mean(xs),min=min(xs),max=max(xs),rms=math.sqrt(mean([x*x for x in xs])))


def wall_terms(floor_gap, lid_gap):
    return dict(mean_of_grid_differences=(floor_gap + lid_gap) / 2,
                half_signed_imbalance=(floor_gap - lid_gap) / 2)


def paired_series(coarse, fine, fine_dt):
    """At odd fine times, use only the two surrounding coarse observation times."""
    require(len(fine)==2*len(coarse)-1 and len(coarse)>=2,"paired clocks")
    out = []
    for i,b in enumerate(fine):
        j,odd = divmod(i,2)
        a = coarse[j]
        if odd:
            a = {k:(a[k]+coarse[j+1][k])/2 for k in a}
        row = dict(hold_F24_step=i,time_since_stop=i*fine_dt,F12_interpolated=int(bool(odd)))
        for k in ("floor_MPa","lid_MPa","KE"):
            row["F12_"+k],row["F24_"+k] = a[k],b[k]
        row["floor_gap_MPa"] = a["floor_MPa"]-b["floor_MPa"]
        out.append(row)
    return out


def read_arm(n, new, old, summary, before):
    key = f"run/F{n}/"
    rec = json.loads(new[key+"hold_receipt.json"])
    oldrec = json.loads(old[key+"quarter_speed_receipt.json"])
    exported = summary["arms"][str(n)]
    require(rec==exported["receipt"] and oldrec==before["arms"][str(n)] and rec["grid"]==n
            and rec["status"]=="HOLD_ARM_COMPLETE" and rec["release"]==FIXED[1],"arm receipt")
    require(set(rec["hashes"])=={*OLD_KEYS,"energy.csv","layer_spec.json"} and
            all(sha(new[key+f])==digest for f,digest in rec["hashes"].items()),"output CSV hashes")
    require(json.loads(new[key+"layer_spec.json"])==oldrec["layer_spec"],"seed layer identity")
    prefixes = {}
    ramp, total = RAMP[n],RAMP[n]+HOLD[n]
    for f,kind in OLD_KEYS.items():
        require(sha(old[key+f])==oldrec[kind],"baseline "+kind)
        prefixes[f] = bound_prefix(new[key+f],old[key+f],ramp+int(f=="trace.csv"))
    require(prefixes==rec["fork"]["prefix_sha256"],"stored fork hashes")
    trace,wall,layer,motion,energy = (csv_rows(new[key+f]) for f in (*OLD_KEYS,"energy.csv"))
    require(len(trace)==len(energy)==len(wall)+1==len(layer)+1==len(motion)+1==total+1,"complete native records")
    width, dt = float(trace[0]["height"]),float(trace[1]["time_code"])
    height = float(trace[ramp]["height"])
    require(height==exported["locked_height"]==rec["fork"]["height"] and ramp==rec["fork"]["step"],"hold configuration")
    speed = before["quarter_wall_speed"]
    require(trace[0]["step"]=="0" and float(trace[0]["time_code"])==0 and energy[0]["phase"]=="initial","initial sample")
    old_py = 0.
    py_layers = dict.fromkeys(LAYERS,0.)
    series = []
    scale = 10/(width*dt)
    for i,(r,w,l,m,e) in enumerate(zip(trace[1:],wall,layer,motion,energy[1:],strict=True),1):
        require(all(v["step"]==str(i) for v in (r,w,l,m,e)),"synchronized native steps")
        moving = i<=ramp
        require(float(r["time_code"])==dt*i and float(r["height"])==(width-(dt*i)*speed if moving else height)
                and e["phase"]==("compression" if moving else "hold") and float(e["plate_speed"])==(speed if moving else 0.),"height or clock")
        floor_j,lid_j = float(w["floor_impulse"]),float(w["lid_downward_impulse"])
        floor,lid = floor_j*scale,lid_j*scale
        require(floor>=0 and lid>=0 and min(float(w["top_gap_after"]),float(w["floor_gap_after"]))>=-2e-12 and
                float(w["lid_signed_impulse"])==-lid_j and float(l["floor_J"])==floor_j and float(l["lid_signed_J"])==-lid_j,"plate impulses/gaps")
        near(floor,10*float(r["bottom_pressure_E"]),"measured floor pressure")
        py = float(m["particle_Py_after"])
        require(old_py==float(m["particle_Py_before"])==float(l["whole_before"]) and py==float(l["whole_after"]),"particle continuity")
        near(py-old_py,float(m["particle_delta_Py"]),"particle delta")
        near(py-old_py,floor_j-lid_j,"instantaneous wall/particle balance")
        near(py-old_py,float(l["whole_delta"]),"whole/layer delta")
        changes = {}
        for name in LAYERS:
            require(float(l[name+"_before"])==py_layers[name],"fixed layer continuity")
            val = float(l[name+"_after"])
            near(val-py_layers[name],float(l[name+"_delta"]),"layer change")
            changes[name] = (val-py_layers[name])*scale
            py_layers[name] = val
        near(math.fsum(changes.values()),(py-old_py)*scale,"sum of layers")
        ke,vke = float(e["particle_ke"]),float(e["vertical_ke"])
        require(math.isfinite(ke) and 0<=vke<=ke+1e-15,"particle kinetic energy")
        if i>=ramp:
            series.append(dict(floor_MPa=floor,lid_MPa=lid,KE=ke,vertical_KE=vke,whole_MPa=(py-old_py)*scale,
                               **{k+"_MPa":x for k,x in changes.items()}))
        old_py = py
    continued = {}
    old_wall = csv_rows(old[key+"wall_steps.csv"])
    for k, name in enumerate(NAMES[:2]):
        count = 300 * n // 12
        begin = ramp + k * count
        rows = old_wall[begin:begin+count]
        require(len(rows) == count and [int(row["step"]) for row in rows] == list(range(begin+1,begin+count+1)),
                "continued ramp comparison window")
        means = dict(floor_MPa=mean([float(r["floor_impulse"])*scale for r in rows]),
                     lid_MPa=mean([float(r["lid_downward_impulse"])*scale for r in rows]))
        expected = exported["windows"][name]["continued_compression_equal_time_different_height"]
        near(means["floor_MPa"], expected["floor_mean_MPa"], "continued loading mean floor")
        near(means["lid_MPa"], expected["lid_mean_MPa"], "continued loading mean lid")
        continued[name] = means
    return dict(dt=dt,height=height,width=width,prefixes=prefixes,series=series,expected=exported["windows"],
                continued_loading=continued)


def evaluate(fixed_path,quarter_path):
    new,summary = archive(fixed_path,FIXED)
    old,before = archive(quarter_path,QUARTER)
    require(summary["quarter_return_sha256"]==QUARTER[0] and summary["quarter_release"]==QUARTER[1]
            and summary["status"]=="HOLD_PAIR_COMPLETE" and before["status"]=="QUARTER_SPEED_PREFIX_COMPLETE","input lineage")
    arms = {n:read_arm(n,new,old,summary,before) for n in (12,24)}
    a,b = arms[12],arms[24]
    require(a["height"]==b["height"] and a["dt"]==2*b["dt"],"shared fixed height/time")
    series = paired_series(a["series"],b["series"],b["dt"])
    report = dict(label="DEVELOPMENT_ONLY", result_sha256=FIXED[0],baseline_sha256=QUARTER[0],
                  hold_release=FIXED[1],quarter_release=QUARTER[1],qualification="HOLD",
                  reference_MPa=REFERENCE,displacement_D=(a["width"]-a["height"])/.1,
                  duration=series[-1]["time_since_stop"],common_native_times_including_fork=len(a["series"]),
                  union_times_including_fork=len(series),fork_gap_MPa=series[0]["floor_gap_MPa"],
                  loading_prefixes_sha256={n:arm["prefixes"] for n,arm in arms.items()},windows={})
    near(report["fork_gap_MPa"],before["pressure_union"]["quarter_on_common_1139"]["peak"]["signed_gap_MPa"],"registered moving peak")
    for k,name in enumerate(NAMES):
        window={}
        for n,arm in arms.items():
            count=300*n//12
            native=arm["series"][k*count+1:(k+1)*count+1]
            stats={key:range_stats([r[key] for r in native]) for key in native[0]}
            expect=arm["expected"][name]
            for metric in ("floor","lid"):
                near(stats[metric+"_MPa"]["mean"],expect[metric+"_mean_MPa"],"reported mean wall pressure")
                near(stats[metric+"_MPa"]["min"],expect[metric+"_range_MPa"][0],"minimum pressure")
                near(stats[metric+"_MPa"]["max"],expect[metric+"_range_MPa"][1],"maximum pressure")
            for key2 in ("mean","min","max"):
                near(stats["KE"][key2],expect["particle_ke"][key2],"mean/range of kinetic energy")
            near(stats["whole_MPa"]["mean"],expect["whole_delta_Py_MPa"],"window material momentum")
            for layer in LAYERS:
                near(stats[layer+"_MPa"]["mean"],expect[layer+"_delta_Py_MPa"],"window layer: "+layer)
            window[str(n)]=stats
        delta={key:window["12"][key]["mean"]-window["24"][key]["mean"] for key in window["12"]}
        near(delta["floor_MPa"],summary["F12_minus_F24_equal_time"][name]["floor_mean_MPa"],"window grid gap")
        near(delta["floor_MPa"],delta["lid_MPa"]+delta["whole_MPa"],"net balance")
        u=series[600*k+1:600*(k+1)+1]
        gaps=[r["floor_gap_MPa"] for r in u]
        terms = wall_terms(delta["floor_MPa"],delta["lid_MPa"])
        near(terms["half_signed_imbalance"],delta["whole_MPa"]/2,"two-wall asymmetry")
        window.update(wall_identity_MPa=terms,time_since_stop=[k*600*b["dt"],u[-1]["time_since_stop"]],
                      native_mean_difference=delta,union_gap=range_stats(gaps),
                      union_abs_gap_max_MPa=max(map(abs,gaps)),
                      union_steps_above_loading_reference=sum(abs(p)>.05*REFERENCE for p in gaps))
        report["windows"][name]=window
        if name in a["continued_loading"]:
            c12,c24 = (arm["continued_loading"][name] for arm in (a,b))
            window["continued_compression_equal_time_different_height_MPa"] = {
                "F12": c12, "F24": c24,
                "floor_gap": c12["floor_MPa"]-c24["floor_MPa"],
                "lid_gap": c12["lid_MPa"]-c24["lid_MPa"]}
    late=[report["windows"][key]["wall_identity_MPa"] for key in ("late_1","late_2")]
    report["late2_minus_late1_wall_identity_MPa"]={k:late[1][k]-late[0][k] for k in late[0]}
    # Time zero is the last moving sample and is excluded from all stationary statistics.
    held=series[1:]
    peak=max(held,key=lambda r:abs(r["floor_gap_MPa"]))
    gaps=[r["floor_gap_MPa"] for r in held]
    momentum = {}
    for n,arm in arms.items():
        momentum[n] = dict(KE_at_fork=arm["series"][0]["KE"],KE_at_end=arm["series"][-1]["KE"],
                           vertical_KE_at_fork=arm["series"][0]["vertical_KE"],
                           vertical_KE_at_end=arm["series"][-1]["vertical_KE"])
    report.update(instantaneous_union=dict(held_samples=len(held),peak=peak,
                  peak_abs_reference_percent=100*abs(peak["floor_gap_MPa"])/REFERENCE,
                  held_steps_above_loading_reference=sum(abs(p)>.05*REFERENCE for p in gaps),stats=range_stats(gaps)),
                  endpoint_energies=momentum,final_pair=series[-1])
    return report,series


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ("fixed_tar","quarter_tar","out_json","out_csv"):
        parser.add_argument(arg,type=Path)
    parser.add_argument("--check-sidecars",action="store_true",
                        help="Also verify SHA256SUMS and screen.txt beside each author archive.")
    args=parser.parse_args()
    if args.check_sidecars:
        check_sidecars(args.fixed_tar,FIXED)
        check_sidecars(args.quarter_tar,QUARTER)
    report,series=evaluate(args.fixed_tar,args.quarter_tar)
    args.out_json.write_bytes((json.dumps(report,indent=2,allow_nan=False)+"\n").encode("ascii"))
    with args.out_csv.open("w",encoding="ascii",newline="") as f:
        csv_out=csv.DictWriter(f,fieldnames=list(series[0]),lineterminator="\n")
        csv_out.writeheader()
        csv_out.writerows(series)

"""Read four native traces and pinned source blobs; standard library, no integration."""
import argparse
from bisect import bisect_left
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import tarfile
from contextlib import ExitStack


PIN = "2cf17b1df57396ef01505a72641e01b19629bed5"
PRIOR = "d0c33bc19c2dd1291f3cf3ae0788fd193065e72b"
HASHES = {
    "result":"9dbf1dda91de65ecdf83c37497b8be34e9a77c6868512d97b2b4a2a438c0a69b",
    "wall":"0df5971d360ed20463d67ab36bd97b677b3e55bee9aaf01dbd559daf79a9ed90",
    "order":"8e76ec686e8f384c28c42b5c5304d25256096f0568fe999d602bdec307991e17",
    "stop228":"a100f018bd5e9c3621395ac436550029759fe17a02a55641db121d52dba1fdbe",
    "capture145":"90b070d33e84735008035eb399d648acb6065edfb677653f8db9f3c9c61eca18"}
SCREEN = "d7cc44e1476b151e34e92c541e6cee8f9ee7e6d9dcb3ce6c6ceb5eb3fc3dd70b"
ARM_NAMES = ("old_original","old_reversed","candidate_original","candidate_reversed")
PRIOR_TRACES = ("03f3bc2c106aa466f1ccc2b774e0b768f2a902792006609680faa53038434cdf",
                "faafadfcb01671f5816e1cc2e2eb04bbef235835616fa0a2d6580c3fe46e97c5")
ANCHOR = .11562281664031926


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def member(archive, name):
    info = archive.getmember(name)
    require(info.isfile(), "unexpected member type")
    return archive.extractfile(info).read()


def no_go(data):
    require(data["u6_qualified"] is False and data["stage3_go"] is False and
            data["label"] == "DEVELOPMENT_ONLY","qualification flags")


def parse_native(data, result, width, dt, modulus):
    require(result["trace_sha256"] == sha(data),"native trace identity")
    require((result["status"],result["arm"],result["label"],result["setting"],result["cells"]) ==
            ("TARGET_BRACKETED","F","DEVELOPMENT_ONLY",1,8),"native identity")
    rows = csv.reader(io.StringIO(data.decode("ascii")))
    require(next(rows) == ["step","time_code","height","bottom_pressure_E","phi_m"],"trace columns")
    curve = []
    speed = .034*math.sqrt(1/(2*(1+.45)))
    for index, row in enumerate(rows):
        i, time, h, p, phi = row
        time, h, p, phi = map(float,(time,h,p,phi))
        require(i == str(index) and time == dt*index and h == width-time*speed and h>=.75*width,
                "native time and height schedule")
        require(math.isfinite(p) and p >= 0 and (index>0 or p==0),"reaction invalid")
        require(p < .12 if index<result["steps"] else p >= .12,"first bracket")
        require(math.isclose(phi,49*math.pi*.05**2/(width*h),rel_tol=1e-12),"seed area")
        curve.append((width-h,modulus*p))
    require(len(curve) == result["steps"]+1 and len(curve)>1,"trace count")
    return curve


def at(curve,u):
    if u<curve[0][0] or u>curve[-1][0]:
        return None
    j=bisect_left(curve,(u,-math.inf))
    x,y=curve[j]
    if x == u:
        return y
    a,b=curve[j-1]
    return b+(u-a)/(x-a)*(y-b)


def shared(curves):
    rows = list(zip(*curves))
    require(bool(rows),"empty native support")
    require(all(len({pt[0] for pt in row})==1 for row in rows),"displacement grid differs")
    return rows


def delta(a,b):
    rows=shared((a,b))
    ds=[pa-pb for (_,pa),(_,pb) in rows]
    peak=max(range(len(rows)), key=lambda i: abs(ds[i]))
    return ds,peak


def check_pair(a,b,reported):
    ds,i=delta(a,b)
    n=len(ds)
    u,pa=a[i]
    _,pb=b[i]
    expect={"samples":n,"start_u":a[0][0],"end_u":a[n-1][0],"max_abs_MPa":abs(ds[i]),
            "first_worst":{"step":i,"u":u,"original_MPa":pa,"reversed_MPa":pb,"original_minus_reversed_MPa":ds[i]},
            "at_fixed_anchor":None}
    if ANCHOR<=a[n-1][0]:
        oa,ob=at(a,ANCHOR),at(b,ANCHOR)
        expect["at_fixed_anchor"]={"original_MPa":oa,"reversed_MPa":ob,"u":ANCHOR,"original_minus_reversed_MPa":oa-ob}
    require(expect==reported,"pair metadata or maximum")
    return ds,i


def check_curves(curves,reported):
    a,b,c,d=curves
    n=len(shared(curves))
    require(reported["fixed_u"] == ANCHOR and reported["first_cap_steps"] ==
            {name:len(curve)-1 for name,curve in zip(ARM_NAMES,curves)},"stopping steps or anchor")
    check_pair(a,b,reported["historical_pair"])
    nd,_=check_pair(c,d,reported["candidate_pair"])
    joint=reported["all_four_common"]
    jold,io=check_pair(a[:n],b[:n],joint["old"])
    jnew,inew=check_pair(c[:n],d[:n],joint["candidate"])
    require(joint["samples"]==n and joint["end_u"]==a[n-1][0] and
            joint["decrease_in_max_abs_MPa"]==abs(jold[io])-abs(jnew[inew]),"four-way maximum")
    for key,i in (("at_old_worst",io),("at_candidate_worst",inew)):
        require(joint[key]=={"step":i,"u":a[i][0],"old_original_minus_reversed_MPa":jold[i],
                             "candidate_original_minus_reversed_MPa":jnew[i]},"extremum location")
    shifts=[]
    for key,old,new in (("original_kernel_change",a,c),("reversed_kernel_change",b,d)):
        dis,i=delta(new[:n],old[:n])
        shifts.append(abs(dis[i]))
        require(joint[key]=={"candidate_minus_historical_MPa":dis[i],"max_abs_MPa":abs(dis[i]),
                             "step":i,"u":old[i][0]},"kernel shift metadata")
    require(len(joint["fixed_points"])==3,"fixed point count")
    for u,stored in zip((.1,.11100328595220721,ANCHOR),joint["fixed_points"]):
        values=[at(curve,u) for curve in curves]
        if None in values:
            expected={"u":u,"status":"NOT_REACHED_BY_ALL_FOUR","pressures_MPa":None}
        else:
            oa,ob,na,nb=values
            expected={"u":u,"status":"REACHED","pressures_MPa":dict(zip(ARM_NAMES,values)),
                      "old_original_minus_reversed_MPa":oa-ob,"candidate_original_minus_reversed_MPa":na-nb,
                      "candidate_minus_historical_original_MPa":na-oa,"candidate_minus_historical_reversed_MPa":nb-ob}
        require(stored==expected,"fixed displacement comparison")
    diag=reported["candidate_numerical_comparison"]
    matches=(len(c)==len(d) and all(abs(v)<=1e-12*(1+max(abs(x[1]),abs(y[1]))) for v,x,y in zip(nd,c,d)))
    require(diag=={"absolute_tolerance_MPa":1e-12,"relative_tolerance":1e-12,
                   "qualification_threshold":None,"exact_samples_and_same_stop":(c==d),
                   "within_diagnostic_tolerance_and_same_stop":matches,"max_abs_on_pair_common_MPa":max(map(abs,nd))},
            "diagnostic status")
    return {"sample_counts":dict(zip(ARM_NAMES,map(len,curves))),"all_four_samples":n,
            "all_four_end_u":a[n-1][0],"old_common_max_gap_MPa":abs(jold[io]),
            "candidate_four_common_max_gap_MPa":abs(jnew[inew]),"candidate_pair_max_gap_MPa":max(map(abs,nd)),
            "candidate_pair_nonidentical_MPa_samples":sum(x!=0 for x in nd),
            "kernel_shift_max_MPa":dict(zip(("original","reversed"),shifts)),
            "candidate_anchor_MPa":{"original":at(c,ANCHOR),"reversed":at(d,ANCHOR)},
            "all_four_reached_anchor":all(at(curve,ANCHOR) is not None for curve in curves)}


def audit(args):
    repo=args.repo.resolve().as_posix() if args.repo else None
    directory=args.result.parent
    screen=(directory/"screen.txt").read_bytes()
    require(sha(screen)==SCREEN,"outer screen SHA")
    sums=(directory/"SHA256SUMS").read_text("ascii").splitlines()
    require(sorted(sums)==sorted([HASHES["result"]+"  "+args.result.name,SCREEN+"  screen.txt"]),"outer checksum list")
    with ExitStack() as ctx:
        ar={}
        for name,expected in HASHES.items():
            p=getattr(args,name)
            require(sha(p.read_bytes())==expected,"archive SHA "+name)
            ar[name]=ctx.enter_context(tarfile.open(p,mode="r:gz"))
            require(len(set(ar[name].getnames()))==len(ar[name].getnames()),"duplicate member")
        new=ar["result"]
        text=lambda t,k: member(t,k).decode("ascii")
        val=lambda t,k: json.loads(member(t,k))
        screen_data=member(new,"run/screen.txt")
        require(screen_data==screen and all(screen.splitlines().count(item)==1 for item in
                (b"F8_ORIGINAL_RC=0",b"F8_REVERSED_RC=0",b"SUMMARY_RC=0",b"COMMAND_RC=0")),"screen status")
        provenance=dict(line.split("=",1) for line in text(new,"run/origin.txt").splitlines())
        sources=member(new,"run/SOURCE_SHA256SUMS")
        manifest=dict(line.split(maxsplit=1)[::-1] for line in sources.decode("ascii").splitlines())
        require(provenance["release"]==PIN and provenance["source_sums"]==sha(sources) and len(manifest)==11,"manifest identity")
        require(all(provenance["prior_"+k] == HASHES[v] for k,v in
                    (("wall","wall"),("order","order"),("capture","capture145"),("stop228","stop228"))),"prior identity")
        for name,expected in manifest.items():
            if name=="RELEASE":
                data=(PIN+"\n"+PRIOR+"\n").encode("ascii")
            elif repo:
                data=subprocess.check_output(["git","-c","safe.directory="+repo,"-C",repo,"show",PIN+":"+name])
            else:
                data=(args.source_snapshot / name).read_bytes()
            require(sha(data)==expected,"fixed source blob "+name)
        summary=val(new,"run/comparison.json")
        no_go(summary)
        require(summary["status"]=="DEVELOPMENT_READ_BACK" and summary["historical_archive_sha256"]==
                {"wall":HASHES["wall"],"order":HASHES["order"]},"readback scope")
        observer=val(ar["wall"],"run/arms/F8/observer.json")
        width,dt,mod=(observer[key] for key in ("width","dt","E_MPa"))
        geometry=val(ar["order"],"run/F8_RELABEL/order_control.json")
        curves=[]; trace_ids=[]; geometry_current=[]
        for i,(archive,stem) in enumerate(((ar["wall"],"run/arms/F8"),(ar["order"],"run/F8_RELABEL"),
                                           (new,"run/ORIGINAL"),(new,"run/REVERSED"))):
            trace=member(archive,stem+"/trace.csv")
            native_bytes=member(archive,stem+"/result.json")
            native=json.loads(native_bytes)
            require(native["points_count"]==9653,"native physical count")
            trace_ids.append(sha(trace))
            curves.append(parse_native(trace,native,width,dt,mod))
            if i<2:
                control=(observer,geometry)[i]
                native_sha=control[("result_sha256","native_result_sha256")[i]]
                require(trace_ids[-1]==PRIOR_TRACES[i]==control["trace_sha256"] and native_sha==sha(native_bytes),"historical bytes")
                continue
            m=("ORIGINAL","REVERSED")[i-2]
            candidate=val(archive,stem+"/candidate.json")
            no_go(candidate)
            require(summary["receipts"][m.lower()]==candidate and candidate["mapping"]==m and
                    candidate["trace_sha256"]==trace_ids[-1] and candidate["native_result_sha256"]==sha(native_bytes) and
                    candidate["candidate_calls"]==native["steps"] and candidate["status"]==native["status"],"candidate receipts")
            require(candidate["candidate_sha256"]==manifest["scripts/suyoung_multicontact_dev.py"] and
                    candidate["adapter_sha256"]==manifest["docs/reviews/suyoung_u6c_friction_candidate_20261122/friction_pair.py"] and
                    candidate["base_source_sha256"]==observer["original_source_sha256"]==geometry["source_sha256"] and
                    candidate["base_source_sha256"]=={k:manifest["scripts/"+k] for k in candidate["base_source_sha256"]} and
                    native["source_sha256"]=={k:candidate["base_source_sha256"][k] for k in native["source_sha256"]},
                    "projector or base provenance")
            expected_geometry=dict(geometry["geometry_sha256"])
            if i==2:
                expected_geometry["field_ids"]=expected_geometry["physical_ids"]
                for hist,member_name in ((ar["capture145"],"run/capture/replay/trace.csv"),(ar["stop228"],"run/ORIGINAL/trace.csv")):
                    require(trace.startswith(member(hist,member_name)),"captured trace prefix")
            require(candidate["geometry_sha256"]==expected_geometry,"physical mapping")
            geometry_current.append(candidate["geometry_sha256"])
        require(geometry_current[0]["field_ids"]!=geometry_current[1]["field_ids"],"relabel did not change field IDs")
    metrics=check_curves(curves,summary["comparison"])
    return {"status":"OFFLINE_READBACK_MATCH","release":PIN,"archive_sha256":HASHES,
            "source_entries":len(manifest),"source_mode":"GIT_PINNED_BLOBS" if repo else "PINNED_MANIFEST_SNAPSHOT",
            "bound_trace_sha256":dict(zip(ARM_NAMES,trace_ids)),
            "prefix_through_steps":[144,227],"diagnostic":metrics,"u6_qualified":False,"stage3_go":False}


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    source=parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--repo",type=Path)
    source.add_argument("--source-snapshot",type=Path,help="Root containing all ten original manifest sources")
    for name in ("result","wall","order","stop228","capture145","out"):
        parser.add_argument("--"+name,type=Path,required=True)
    args=parser.parse_args()
    report=audit(args)
    with args.out.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")
    print(json.dumps(report["diagnostic"],sort_keys=True))

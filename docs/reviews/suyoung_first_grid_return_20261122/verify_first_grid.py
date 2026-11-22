"""Independent, standard-library readback of the completed F8/F16 development pair."""
import argparse
from bisect import bisect_left
import csv
from contextlib import ExitStack
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import subprocess
import tarfile


PIN="99938d3bd4cb1cbba0e1377be2ff9dac9b228d2f"
SOURCE="3cb189bc2f5180e929043ec4c1737aade3588362b1c5e5a16f1650eee567c4e7"
PREVIOUS8="9dbf1dda91de65ecdf83c37497b8be34e9a77c6868512d97b2b4a2a438c0a69b"
PREVIOUS16="bdd10395a7acc1aa7e64f7aaa6d8509a343ea448b47ee39e0770f520e310ec6d"
KERNEL="acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645"
RULE="1736322b4b2f4cef384becd97099998668137c19272e504edd951b698502a8f4"
RESULT="fc685932f4a1710fe944c5d2dafbcb56bf239f473184f009983a3ff4805dabea"
SCREEN="c4ceac7ae1bc304012811f9e281ef4447b2a71846e9892616d36176892cd88ba"
MANIFEST="040c9f1b68ed04bfc62bc5e1528c8bd6fb2ced2830135d82f41c8294290bc0e8"
WIDTH=.7024180763115129
SPEED=.034*math.sqrt(1/(2*(1+.45)))
DT={8:.0022463670164795577,16:.0011231835082397789}


def require(ok,msg):
    if not ok:
        raise ValueError(msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def entry(t,name):
    m=t.getmember(name)
    require(m.isfile(),"invalid member type")
    return t.extractfile(m).read()


def sums(data):
    lines=[line.split("  ",1) for line in data.decode("ascii").splitlines()]
    mapping={p:h for h,p in lines}
    require(len(mapping)==len(lines),"duplicate manifest input")
    return mapping


def scope(data):
    require(data["label"]=="DEVELOPMENT_ONLY" and data["u6_qualified"] is False and
            data["stage3_go"] is False,"scope changed")


def samples(data,native,cells):
    require(native["trace_sha256"]==sha(data) and native["status"]=="TARGET_BRACKETED" and
            (native["arm"],native["cells"],native["setting"],native["points_count"])==
            ("F",cells,1,{8:9653,16:39053}[cells]),"native identity")
    c=csv.reader(io.StringIO(data.decode("ascii")))
    require(next(c,None)==["step","time_code","height","bottom_pressure_E","phi_m"],"schema")
    out=[]
    for i,row in enumerate(c):
        require(len(row)==5 and row[0]==str(i),"step sequence")
        t,h,p,phi=map(float,row[1:])
        require(t==i*DT[cells] and h==WIDTH-t*SPEED and h>=.75*WIDTH and
                math.isclose(phi,49*math.pi*.05**2/(WIDTH*h),rel_tol=1e-12),"loading or seed area")
        require(math.isfinite(p) and p>=0 and (i>0 or p==0) and
                (p<.12 if i<native["steps"] else p>=.12),"first pressure bracket")
        out.append((WIDTH-h,10.*p))
    require(len(out)==native["steps"]+1 and len(out)>1,"complete length")
    return out


def evaluate(curves):
    for c in curves:
        require(len(c)>=2 and c[0][0]==0 and all(math.isfinite(x) and math.isfinite(y) and y>=0 for x,y in c)
                and all(p[0]<q[0] for p,q in zip(c,c[1:])),"invalid curve")
    coarse,fine=curves
    end=min(coarse[-1][0],fine[-1][0])
    knots=sorted({x for c in curves for x,y in c if x<=end})

    def values(curve):
        axis=[x for x,y in curve]
        for u in knots:
            i=bisect_left(axis,u)
            if i<len(axis) and axis[i]==u:
                yield curve[i][1]
            else:
                require(0<i<len(axis),"extrapolation")
                x,y=curve[i-1]
                z,v=curve[i]
                yield y+(v-y)*((u-x)/(z-x))

    coarse_p,fine_p=(list(values(c)) for c in curves)
    signed=[a-b for a,b in zip(coarse_p,fine_p)]
    di=max(range(len(knots)),key=lambda i: abs(fine_p[i]))
    ni=max(range(len(knots)),key=lambda i: abs(signed[i]))
    d,n=abs(fine_p[di]),abs(signed[ni])
    info={"common_start_u":0.,"common_end_u":end,"coarse_end_u":coarse[-1][0],"fine_end_u":fine[-1][0],
          "coarse_samples":len(coarse),"fine_samples":len(fine),
          "coarse_samples_in_common":sum(u<=end for u,_ in coarse),"fine_samples_in_common":sum(u<=end for u,_ in fine),
          "union_knots":len(knots),"fine_peak_MPa":d,"u_at_first_fine_peak":knots[di],
          "max_abs_difference_MPa":n,"coarse_minus_fine_at_first_max_MPa":signed[ni],"u_at_first_max_abs":knots[ni]}
    if d==0:
        info.update(comparison="HOLD",reason="ZERO_REFERENCE",ratio=None,exceeding_knots=None)
    else:
        limit=Fraction(d)/20
        above=[u for u,s in zip(knots,signed) if Fraction(abs(s))>limit]
        info.update(comparison="EXCEEDS" if above else "WITHIN",ratio=n/d,exceeding_knots=len(above),
                    first_exceedance_u=above[0] if above else None)
    return info


def verify_arms(past8,past16,result,submitted,manifest):
    old8=entry(past8,"run/ORIGINAL/trace.csv")
    old16=entry(past16,"run/F16/trace.csv")
    require(sha(old8)==json.loads(entry(past8,"run/ORIGINAL/result.json"))["trace_sha256"] and
            sha(old16)==json.loads(entry(past16,"run/F16/incomplete.json"))["trace"]["sha256"],"prior trace binding")
    runner="docs/reviews/suyoung_u6c_f16_stop_20261122/run_pair.py"
    curves=[]
    for cells,prior in ((8,old8),(16,old16)):
        prefix=f"run/F{cells}/"
        trace=entry(result,prefix+"trace.csv")
        raw=entry(result,prefix+"result.json")
        native=json.loads(raw)
        receipt=submitted["receipts"][f"F{cells}"]
        scope(receipt)
        require(json.loads(entry(result,prefix+"candidate.json"))==receipt,"summary-arm receipt mismatch")
        require(receipt["status"]=="TARGET_BRACKETED" and receipt["cells"]==cells and
                receipt["mapping"]=="ORIGINAL" and receipt["candidate_calls"]==native["steps"] and
                receipt["kernel_sha256"]==KERNEL and receipt["runner_sha256"]==manifest[runner] and
                receipt["trace_sha256"]==sha(trace) and receipt["native_result_sha256"]==sha(raw),"arm receipt")
        if cells==8:
            geometry=json.loads(entry(past8,"run/ORIGINAL/candidate.json"))["geometry_sha256"]
        else:
            geometry={"positions":"ce12e262721141b2c4fc36cc72733686055a9e22ce62a8cc733a1e2ad591858a",
                      "field_ids":"da5560998c5a66797d7928279d5b43f6e26cb8432aac52a37f99d7cef5a3d7b2",
                      "volume":"06f4c3ce49ffece1d401bdcae453605728c4ba0e7731b4c2c6027e337cdc88b4"}
            geometry["physical_ids"]=geometry["field_ids"]
        require(receipt["geometry"]==geometry,"seed or ORIGINAL field mapping")
        require(all(v==manifest["scripts/"+k] for k,v in native["source_sha256"].items()) and
                native["budget_s"]=={8:1140,16:1740}[cells] and native["label"]=="DEVELOPMENT_ONLY","native binding")
        if cells==8:
            require(trace==prior,"F8 original trace differs")
        else:
            require(trace.startswith(prior) and len(trace)>len(prior) and len(prior.splitlines())==4804,
                    "F16 prefix or extension")
        curves.append(samples(trace,native,cells))
    return curves


def verify_pair_report(report,curve_pair):
    scope(report)
    expected=evaluate(curve_pair)
    missing={"comparison":"HOLD","reason":"UPDATED_KERNEL_F12_F24_PAIR_MISSING","ratio":None,"exceeding_knots":None}
    require(report["pairs"]=={"F8_F16":expected,"F12_F24":missing},"registered pair result mismatch")
    require(report["development_grid_comparison"]==("EXCEEDS" if expected["comparison"]=="EXCEEDS" else "HOLD"),
            "missing pair aggregation")
    return expected


def run(args):
    folder=args.result.parent
    screen=(folder/"screen.txt").read_bytes()
    require(sha(screen)==SCREEN and sums((folder/"SHA256SUMS").read_bytes())==
            {"suyoung_contact_pair_result.tar.gz":RESULT,"screen.txt":SCREEN},"outer manifests")
    with ExitStack() as stack:
        archives={}
        for name,pinned in (("result",RESULT),("source",SOURCE),("old_f8",PREVIOUS8),("old_f16_stop",PREVIOUS16)):
            path=getattr(args,name)
            stream=stack.enter_context(path.open("rb"))
            require(hashlib.file_digest(stream,"sha256").hexdigest()==pinned,"archive digest "+name)
            stream.seek(0)
            ar=archives[name]=stack.enter_context(tarfile.open(fileobj=stream,mode="r:gz"))
            require(len(set(ar.getnames()))==len(ar.getnames()),"duplicate tar member")
        result,source=archives["result"],archives["source"]
        returned_sums=entry(result,"run/SOURCE_SHA256SUMS")
        require(sha(returned_sums)==MANIFEST and returned_sums==entry(source,"SOURCE_SHA256SUMS"),"source manifest")
        outer=sums(entry(source,"SHA256SUMS"))
        require(set(outer)==set(source.getnames())-{"SHA256SUMS"},"source inventory")
        for name,expect in outer.items():
            require(sha(entry(source,name))==expect,"source payload")
        manifest=sums(returned_sums)
        require(len(manifest)==14 and manifest["scripts/suyoung_multicontact_dev.py"]==KERNEL and
                manifest["docs/reviews/suyoung_u6c_force_rule_20261122/rule.json"]==RULE and
                all(outer[k]==expect for k,expect in manifest.items()),"analysis source")
        release=(PIN+"\n2cf17b1df57396ef01505a72641e01b19629bed5\ne5c3ac7bba373efc4a7a0367c6f6ecee41018f29\n").encode("ascii")
        require(entry(source,"RELEASE")==release,"source release")
        if args.repo:
            repo=args.repo.resolve().as_posix()
            for path,h in manifest.items():
                if path!="RELEASE":
                    blob=subprocess.check_output(["git","-c","safe.directory="+repo,"-C",repo,"show",PIN+":"+path])
                    require(sha(blob)==h,"Git source membership")
        origin=dict(line.split("=",1) for line in entry(result,"run/origin.txt").decode("ascii").splitlines())
        expected_origin={"release":PIN,"historical_contact_pin":"2cf17b1df57396ef01505a72641e01b19629bed5",
                         "source_sums":MANIFEST,"prior_f8":PREVIOUS8,"prior_f16_stop":PREVIOUS16,
                         "kernel_sha256":KERNEL,"CPU":"0","F8_soft_hard_s":"1140,1200","F16_soft_hard_s":"1740,1800"}
        require(all(origin[k]==v for k,v in expected_origin.items()),"origin identity")
        require(entry(result,"run/screen.txt")==screen and all(screen.splitlines().count(v)==1 for v in
                (b"F8_RC=0",b"F8_CHECK_RC=0",b"F16_RC=0",b"SUMMARY_RC=0",b"COMMAND_RC=0")),"return codes")
        report_bytes=entry(result,"run/grid_comparison.json")
        report=json.loads(report_bytes)
        require(report["rule_sha256"]==RULE and report["registration_id"]=="U6c-06-force-displacement-v1" and
                report["status"]=="DEVELOPMENT_PAIR_READ_BACK" and report["kernel_sha256"]==KERNEL and
                report["previous_f8_sha256"]==PREVIOUS8 and report["previous_f16_sha256"]==PREVIOUS16 and
                report["F8_native_trace"]=="ALL_BYTES_EQUAL" and
                report["F16_native_prefix"]=="ALL_BYTES_EQUAL_THROUGH_STEP_4802","grid report provenance")
        curves=verify_arms(archives["old_f8"],archives["old_f16_stop"],result,report,manifest)
        metrics=verify_pair_report(report,curves)
    return {"status":"VERIFIED_DEVELOPMENT_PAIR_READBACK","release":PIN,"kernel_sha256":KERNEL,
            "return_sha256":RESULT,"previous_f8_sha256":PREVIOUS8,"previous_f16_stop_sha256":PREVIOUS16,
            "source_tar_sha256":SOURCE,"original_report_sha256":sha(report_bytes),
            "source_members":len(manifest),"source_git_verified":bool(args.repo),"rule_sha256":RULE,
            "F8_native_history":"ALL_BYTES_EQUAL","F16_prior_steps_0_to_4802":"ALL_BYTES_EQUAL",
            "F8_F16":metrics,"F12_F24":report["pairs"]["F12_F24"],"u6_qualified":False,"stage3_go":False,
            "new_field_executions_by_readback":0}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ("result","source","old-f8","old-f16-stop","out"):
        p.add_argument("--"+flag,required=True,type=Path)
    p.add_argument("--repo",type=Path,help="Optional Git clone for an extra fixed-blob comparison")
    args=p.parse_args()
    receipt=run(args)
    with args.out.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(receipt,out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")
    print(receipt["status"],receipt["F8_F16"]["comparison"],receipt["F8_F16"]["ratio"])

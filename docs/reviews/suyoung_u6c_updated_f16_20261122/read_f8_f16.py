"""Apply the registered 5% rule to updated F8/F16 ORIGINAL development curves."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import tarfile


F8_ARCHIVE = "9dbf1dda91de65ecdf83c37497b8be34e9a77c6868512d97b2b4a2a438c0a69b"
F8_PIN = "2cf17b1df57396ef01505a72641e01b19629bed5"
F8_TRACE = "56f0f5f836e00cc5c7a94afaaef7885e684f17c7983abf631f06e7e39a1c8132"
F8_NATIVE = "bda999234026c35f1e71f673d951e72df87951e75359292d051e4095e7e8a405"
KERNEL = "8af03f07e8149219a13baa1d1ca79c2fc87940bb991c6055769ac0beeb3a8880"
BASE = {
    "dem_suyoung_sf2d_dev.py": "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
    "suyoung_u6_first_dev.py": "5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "suyoung_u6b_dev.py": "50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762",
}
FORCE_DIR = "docs/reviews/suyoung_u6c_force_rule_20261122"
ADAPTER = "docs/reviews/suyoung_u6c_updated_f16_20261122/f16_candidate.py"
ADAPTER_SHA = "de76a1068a938875745165ce649a0390418d9a34993dad9fd82ae3b4e95c0e54"
RULE_SHA = "1736322b4b2f4cef384becd97099998668137c19272e504edd951b698502a8f4"
FORCE_SHA = "145b5fe6f456e8b66c2a8cc422ff88648c82d07c4420482f06bc6da7a5b1b6db"
DOUBLING = "docs/reviews/suyoung_u6c_doubling_readback_20261122/doubling.py"
DOUBLING_SHA = "9d664ed38a70295b9bd04ecbf5dae4ffda663c5efbc348c30a77bf6b99fa1bda"
DT = {8: .0022463670164795577, 16: .0011231835082397789}
WIDTH = .7024180763115129
SPEED = .034*math.sqrt(1/(2*(1+.45)))
POINTS = {8: 9653, 16: 39053}
EXPECTED_IDS = {
    8: "a91d7701d1e24908a53f6807d6bc9042402e70fba67bc82393889895a06868e4",
    16: "da5560998c5a66797d7928279d5b43f6e26cb8432aac52a37f99d7cef5a3d7b2",
}


def require(test, code):
    if not test:
        raise ValueError(code)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def get_rule(repo):
    folder = repo / FORCE_DIR
    checks = ((folder/"rule.json",RULE_SHA), (folder/"force_rule.py",FORCE_SHA), (repo/DOUBLING,DOUBLING_SHA))
    for path, expected in checks:
        require(digest(path.read_bytes()) == expected, "REGISTERED_RULE_BYTES")
    return module(folder/"force_rule.py","registered_u6c_force_rule")


def verify_source(repo):
    for name, expected in dict(BASE, **{"suyoung_multicontact_dev.py":KERNEL}).items():
        require(digest((repo/"scripts"/name).read_bytes()) == expected, "MODEL_OR_KERNEL_SOURCE")


def native_curve(trace, native, cells):
    require(digest(trace) == native["trace_sha256"], "NATIVE_TRACE_BINDING")
    require(native["protocol"]=="U6b-setting1-bottom-loading-v1" and native["label"]=="DEVELOPMENT_ONLY" and
            native["arm"]=="F" and type(native["setting"]) is int and native["setting"]==1 and
            native["cells"]==cells and native["points_count"]==POINTS[cells] and
            native["status"]=="TARGET_BRACKETED" and native["origin"]=="new", "NATIVE_IDENTITY")
    require(native["source_sha256"] == {k:BASE[k] for k in ("dem_suyoung_sf2d_dev.py","suyoung_u6_first_dev.py")},
            "MATERIAL_SOURCE")
    steps = native["steps"]
    require(type(steps) is int and steps > 0, "NATIVE_STEP_COUNT")
    reader = csv.reader(io.StringIO(trace.decode("ascii")))
    require(next(reader, None)==["step","time_code","height","bottom_pressure_E","phi_m"], "TRACE_COLUMNS")
    curve=[]
    for i,row in enumerate(reader):
        require(len(row)==5 and row[0]==str(i), "NATIVE_STEP_SEQUENCE")
        t,h,p,phi = map(float,row[1:])
        require(t==DT[cells]*i and h==WIDTH-t*SPEED and h>=.75*WIDTH, "NATIVE_WALL_SCHEDULE")
        require(math.isfinite(phi) and math.isclose(phi,49*math.pi*.05**2/(WIDTH*h),rel_tol=1e-12), "NATIVE_AREA")
        require(math.isfinite(p) and p>=0 and (i>0 or p==0), "NONNEGATIVE_WALL_REACTION")
        require(p<.12 if i<steps else p>=.12, "FIRST_TARGET_BRACKET")
        curve.append((WIDTH-h,10.*p))
    require(len(curve)==steps+1, "NATIVE_STEP_COUNT")
    return curve


def bind_arm(trace, result_data, receipt, cells):
    native=json.loads(result_data)
    require(receipt["stage3_go"] is False and receipt["u6_qualified"] is False and
            receipt["label"]=="DEVELOPMENT_ONLY" and receipt["status"]=="TARGET_BRACKETED" and
            receipt["mapping"]=="ORIGINAL", "ARM_SCOPE")
    require(receipt["candidate_sha256"]==KERNEL and type(receipt["candidate_calls"]) is int and
            receipt["candidate_calls"]==native["steps"] and receipt["native_result_sha256"]==digest(result_data) and
            receipt["trace_sha256"]==digest(trace), "ARM_BINDING")
    geometry=receipt["geometry_sha256"]
    require(geometry["physical_ids"] == geometry["field_ids"] == EXPECTED_IDS[cells], "FIELD_MAPPING")
    curve=native_curve(trace,native,cells)
    proof={"cells":cells,"points":native["points_count"],"steps":native["steps"],"trace_sha256":digest(trace),
           "native_sha256":digest(result_data),"geometry_sha256":geometry,"kernel_sha256":KERNEL}
    return curve,proof


def read_f8(path):
    with path.open("rb") as src:
        require(hashlib.file_digest(src,"sha256").hexdigest()==F8_ARCHIVE,"FINAL_F8_ARCHIVE_IDENTITY")
        src.seek(0)
        with tarfile.open(fileobj=src,mode="r:gz") as ar:
            def member(name):
                item=ar.getmember(name)
                require(item.isfile(),"F8_MEMBER_TYPE")
                return ar.extractfile(item).read()
            trace=member("run/ORIGINAL/trace.csv")
            result=member("run/ORIGINAL/result.json")
            rec_data=member("run/ORIGINAL/candidate.json")
            rec=json.loads(rec_data)
            comparison=json.loads(member("run/comparison.json"))
            require(comparison["receipts"]["original"]==rec and comparison["stage3_go"] is False and
                    comparison["u6_qualified"] is False and comparison["status"]=="DEVELOPMENT_READ_BACK", "F8_RECEIPT")
            require(rec["base_source_sha256"]==BASE and digest(trace)==F8_TRACE and digest(result)==F8_NATIVE,
                    "F8_ORIGINAL_TRACE")
            origin=dict(line.split("=",1) for line in member("run/origin.txt").decode("ascii").splitlines())
            sums=member("run/SOURCE_SHA256SUMS")
            require(origin["release"]==F8_PIN and origin["source_sums"]==digest(sums),"F8_PROVENANCE")
    curve,proof=bind_arm(trace,result,rec,8)
    proof.update(archive_sha256=F8_ARCHIVE,release=F8_PIN,receipt_sha256=digest(rec_data))
    return curve,proof


def read_f16(repo, folder):
    adapter_path=repo/ADAPTER
    require(digest(adapter_path.read_bytes())==ADAPTER_SHA,"F16_ADAPTER_SOURCE")
    adapter=module(adapter_path,"fixed_f16_receipt")
    receipt=adapter.check_arm(repo,folder)
    receipt_bytes=(folder/"candidate.json").read_bytes()
    require(json.loads(receipt_bytes)==receipt,"F16_RECEIPT_CHANGED")
    require(receipt["adapter_sha256"]==ADAPTER_SHA and receipt["source_sha256"]==BASE and
            receipt["f8_release"]==F8_PIN and receipt["f8_archive_sha256"]==F8_ARCHIVE and
            receipt["f8_original_trace_sha256"]==F8_TRACE,
            "F8_F16_CAMPAIGN_IDENTITY")
    require(receipt["dt"]==DT[16] and receipt["width"]==WIDTH and receipt["wall_speed"]==SPEED,
            "F16_RUNTIME_SETTINGS")
    curve,proof=bind_arm((folder/"trace.csv").read_bytes(),(folder/"result.json").read_bytes(),receipt,16)
    proof.update(receipt_sha256=digest(receipt_bytes),adapter_sha256=digest(adapter_path.read_bytes()))
    return curve,proof


def blank_report():
    return {"label":"DEVELOPMENT_ONLY","status":"INCOMPLETE","stage3_go":False,"u6_qualified":False,
            "rule_sha256":RULE_SHA,"registration_id":"U6c-06-force-displacement-v1",
            "development_grid_comparison":"HOLD","pairs":{"F12_F24":{"comparison":"HOLD",
            "reason":"UPDATED_KERNEL_F12_F24_PAIR_MISSING","ratio":None,"exceeding_knots":None}}}


def apply(rule,report,coarse,fine):
    pair=rule.compare(coarse,fine)
    report["pairs"]["F8_F16"]=pair
    report["development_grid_comparison"]=rule.aggregate(report["pairs"])
    if pair["comparison"]=="HOLD":
        report["reason"]=pair["reason"]
        return 2
    report["status"]="DEVELOPMENT_PAIR_READ_BACK"
    return 0


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",required=True,type=Path)
    p.add_argument("--f8",required=True,type=Path)
    p.add_argument("--check-f8",action="store_true")
    p.add_argument("--f16",type=Path)
    p.add_argument("--out",type=Path)
    args=p.parse_args()
    if args.check_f8:
        if args.f16 or args.out:
            p.error("--check-f8 is read-only and accepts only --repo/--f8")
    elif args.f16 is None or args.out is None:
        p.error("comparison requires --f16 and --out")
    report=blank_report()
    rc=2
    try:
        verify_source(args.repo)
        rule=get_rule(args.repo)
        coarse,proof=read_f8(args.f8)
        if args.check_f8:
            print("FINAL_F8_ORIGINAL_AND_RULE_OK")
            return 0
        fine,proof16=read_f16(args.repo,args.f16)
        report["receipts"]={"F8":proof,"F16":proof16}
        rc=apply(rule,report,coarse,fine)
    except (ArithmeticError, OSError, ValueError, TypeError, AttributeError, ImportError, KeyError, tarfile.TarError,
            RuntimeError, csv.Error, IndexError) as e:
        reason=str(e) if isinstance(e,ValueError) and str(e).isascii() and str(e).isupper() else type(e).__name__
        report["reason"]=reason
        report["pairs"]["F8_F16"]={"comparison":"HOLD","reason":reason,"ratio":None,"exceeding_knots":None}
        if args.check_f8:
            print("F8_CHECK_FAILED",reason)
            return 2
    with args.out.open("x",encoding="ascii",newline="\n") as out:
        json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")
    print(report["status"],report["pairs"]["F8_F16"]["comparison"])
    return rc


if __name__=="__main__":
    sys.exit(main())

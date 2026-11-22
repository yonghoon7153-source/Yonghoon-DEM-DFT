"""One F8 field-label reversal in physical row order, using the fixed native time step."""
import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tarfile


PREVIOUS = Path(__file__).resolve().parent.parent/"suyoung_u6c_wall_return_20261122"/"dt_control.py"
if hashlib.sha256(PREVIOUS.read_bytes()).hexdigest() != "1811424d5e02767f70f210cfe292c9a4d49091ecf63c5ced7bcb6229095a3e17":
    raise ValueError("PREVIOUS_TOOL_IDENTITY")
spec = importlib.util.spec_from_file_location("order_dt_reference", PREVIOUS)
dt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = dt
spec.loader.exec_module(dt)

PROTOCOL = "U6c-F8-native-dt-reverse49-v1"
ANCHOR = 0.11562281664031926
GEOMETRY = {
    "positions": "474424dea2a36388e28e02b9a5d47f9dad183bb1672dbf4e33ea84bdf7a6efc9",
    "volume": "78fe7907be63b6b084b71ec3262bf2d3f936b2b4eca65c255fc99cdd666a69f0",
    "physical_ids": "a91d7701d1e24908a53f6807d6bc9042402e70fba67bc82393889895a06868e4",
    "field_ids": "f2ce21c5ad339ea079bbcd52c49ba1b6fef0f97eb3b2ca88d31e0a2cff4ccffd",
}


def array_digest(array, dtype, shape):
    dt.require(array.dtype.kind == dtype[1] and array.dtype.itemsize == 8 and array.shape == shape,
               "INITIAL_ARRAY_TYPE_OR_SHAPE")
    return dt.sha(array.astype(dtype, copy=False).tobytes(order="C"))


def reverse_ids(ids):
    dt.require(array_digest(ids, "<i8", (9653,)) == GEOMETRY["physical_ids"], "PHYSICAL_ROW_ORDER")
    mapped = 48 - ids
    dt.require(array_digest(mapped,"<i8",(9653,)) == GEOMETRY["field_ids"], "MAPPING_IDENTITY")
    return mapped


def integrate(driver,budget,out):
    factory = driver.fixed_solver
    solver = factory()
    original_seed = solver.seed
    captured = {}
    def seed(cells):
        dt.require(cells == 8 and not captured, "UNEXPECTED_SEED_REQUEST")
        x,ids,volume = original_seed(cells)
        mapped = reverse_ids(ids)
        captured.update(positions=array_digest(x,"<f8",(9653,2)),volume=array_digest(volume,"<f8",(9653,)),
                        physical_ids=array_digest(ids,"<i8",(9653,)),field_ids=array_digest(mapped,"<i8",(9653,)))
        dt.require(captured == GEOMETRY, "INITIAL_GEOMETRY")
        return x,mapped,volume
    solver.seed = seed
    driver.fixed_solver = lambda: solver
    try:
        native = driver.run_arm("F",8,budget,out)
        dt.require(captured == GEOMETRY, "MISSING_SEED")
        return native,captured
    finally:
        driver.fixed_solver = factory
        solver.seed = original_seed


def make_receipt(folder,native,geometry):
    trace = dt.sha((folder/"trace.csv").read_bytes())
    dt.require(native["trace_sha256"] == trace and native["points_count"] == 9653, "NATIVE_TRACE")
    return {"protocol":PROTOCOL,"label":"DEVELOPMENT_ONLY","u6_qualified":False,"stage3_go":False,
            "geometry_sha256":geometry,"mapping":"physical_id_to_48_minus_id","source_sha256":dt.SOURCE,
            "tool_sha256":dt.sha(Path(__file__).read_bytes()),"trace_sha256":trace,
            "native_result_sha256":dt.sha((folder/"result.json").read_bytes()),"status":native["status"]}


def run_command(directory,budget,out):
    for name, digest in dt.SOURCE.items():
        dt.require(dt.sha((directory/name).read_bytes()) == digest, "SOURCE_BINDING")
    spec = importlib.util.spec_from_file_location("fixed_order_driver",directory/"suyoung_u6b_dev.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    native,geometry = integrate(driver,budget,out)
    dt.write_json(out/"order_control.json",make_receipt(out,native,geometry))
    print(native["status"])
    return 0 if native["status"] == "TARGET_BRACKETED" else 4


def load_arm(folder,ref):
    native = json.loads((folder/"result.json").read_bytes())
    dt.require(native["status"] == "TARGET_BRACKETED", "INCOMPLETE_ARM")
    fields = ("arm","cells","setting","origin","points_count","protocol","label")
    dt.require(tuple(native[k] for k in fields) == ("F",8,1,"new",9653,dt.NATIVE,"DEVELOPMENT_ONLY")
               and ref["points_count"] == 9653, "NATIVE_CONFIGURATION")
    dt.require(native["source_sha256"] == {k:v for k,v in dt.SOURCE.items() if k!="suyoung_u6b_dev.py"},
               "SOURCE_BINDING")
    receipt = json.loads((folder/"order_control.json").read_bytes())
    dt.require(receipt == make_receipt(folder,native,GEOMETRY) and
               receipt["u6_qualified"] is False and receipt["stage3_go"] is False, "CONTROL_BINDING")
    curve = dt.parse_curve((folder/"trace.csv").read_bytes(),native["steps"],ref["dt"],ref["width"],dt.SPEED)
    return curve,receipt["trace_sha256"]


def compare(original,relabelled,anchor):
    common = min(original.u[-1],relabelled.u[-1])
    knots = sorted({u for curve in (original,relabelled) for u in curve.u if u <= common})
    def at(u):
        a,b = original.at(u),relabelled.at(u)
        return {"u":u,"original_MPa":a,"relabelled_MPa":b,"original_minus_relabelled_MPa":a-b}
    worst_u = max(knots,key=lambda u:abs(original.at(u)-relabelled.at(u)))
    worst = at(worst_u)
    reached = knots[0] <= anchor <= common
    return {"fixed_u":anchor,"anchor_status":"REACHED" if reached else "NOT_REACHED",
            "at_fixed_anchor":at(anchor) if reached else None,"first_worst":worst,
            "max_abs_difference_MPa":abs(worst["original_minus_relabelled_MPa"]),
            "common_start_u":knots[0],"common_end_u":common,"common_knots":len(knots)}


def read_command(wall,arm,out):
    result = {"status":"INCOMPLETE","protocol":PROTOCOL,"label":"DEVELOPMENT_ONLY",
              "u6_qualified":False,"stage3_go":False}
    try:
        curves,refs,peak = dt.load_prior(wall)
        dt.require(peak["at_first_worst_total_gap"]["u"] == ANCHOR, "FIXED_ANCHOR")
        curve,trace = load_arm(arm,refs[8])
        result.update(status="DEVELOPMENT_ORDER_CONTRAST",comparison=compare(curves[8],curve,ANCHOR),
                      prior_wall_sha256=dt.PRIOR_SHA,relabelled_trace_sha256=trace)
    except (ArithmeticError,KeyError,ValueError,TypeError,OSError,tarfile.TarError,csv.Error) as exc:
        result["issue"] = str(exc) if isinstance(exc,ValueError) and str(exc).isupper() else type(exc).__name__
    dt.write_json(out,result)
    print(result["status"])
    return 0 if "comparison" in result else 4


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode",required=True)
    run = sub.add_parser("run")
    run.add_argument("--source-dir",type=Path,required=True)
    run.add_argument("--out",type=Path,required=True)
    run.add_argument("--budget",type=float,required=True)
    read = sub.add_parser("read")
    for key in ("wall","arm","out"):
        read.add_argument("--"+key,type=Path,required=True)
    args = parser.parse_args()
    if args.mode == "run":
        raise SystemExit(run_command(args.source_dir,args.budget,args.out))
    raise SystemExit(read_command(args.wall,args.arm,args.out))

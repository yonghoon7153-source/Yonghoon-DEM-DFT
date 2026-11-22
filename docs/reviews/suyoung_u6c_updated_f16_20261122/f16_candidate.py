"""One F16 ORIGINAL development arm with the returned F8 multi-contact kernel."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np


F8_PIN = "2cf17b1df57396ef01505a72641e01b19629bed5"
F8_ARCHIVE = "9dbf1dda91de65ecdf83c37497b8be34e9a77c6868512d97b2b4a2a438c0a69b"
F8_ORIGINAL = "56f0f5f836e00cc5c7a94afaaef7885e684f17c7983abf631f06e7e39a1c8132"
KERNEL = "8af03f07e8149219a13baa1d1ca79c2fc87940bb991c6055769ac0beeb3a8880"
HERE = Path(__file__).resolve()
SOURCE = {
    "suyoung_u6b_dev.py":"50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762",
    "suyoung_u6_first_dev.py":"5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py":"6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}
PROTOCOL = "U6c-updated-F16-original-native-v1"
F16_DT, WIDTH, SPEED = 0.0011231835082397789, 0.7024180763115129, 0.01996548746349992
POINTS, BUDGET = 39053, 1740.
GEOMETRY = {
    "positions":"ce12e262721141b2c4fc36cc72733686055a9e22ce62a8cc733a1e2ad591858a",
    "physical_ids":"da5560998c5a66797d7928279d5b43f6e26cb8432aac52a37f99d7cef5a3d7b2",
    "field_ids":"da5560998c5a66797d7928279d5b43f6e26cb8432aac52a37f99d7cef5a3d7b2",
    "volume":"06f4c3ce49ffece1d401bdcae453605728c4ba0e7731b4c2c6027e337cdc88b4",
}
HELPERS = {
    "observer":("suyoung_u6c_node145_20261122/node145_pair.py",
                "db913bd40bd860bd015cf8c88c0b860b3fec7699113d7f9b76e81404ea841655"),
    "capture":("suyoung_u6c_step145_20261122/capture_stop.py",
               "7d981e2f77b117bc5929ac91bf7b93a219a5ed3b90b5c29130405cee6ec9d4f6"),
    "dt":("suyoung_u6c_wall_return_20261122/dt_control.py",
          "1811424d5e02767f70f210cfe292c9a4d49091ecf63c5ced7bcb6229095a3e17"),
}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def modules(repo):
    scripts = repo/"scripts"
    files = {"driver":scripts/"suyoung_u6b_dev.py", "kernel":scripts/"suyoung_multicontact_dev.py"}
    pins = {scripts/name:sha for name,sha in SOURCE.items()}
    pins[files["kernel"]] = KERNEL
    for name,(path,sha) in HELPERS.items():
        files[name] = repo/"docs/reviews"/path
        pins[files[name]] = sha
    for path,sha in pins.items():
        require(digest(path.read_bytes()) == sha, "SOURCE_BINDING")
    loaded = {}
    for name, path in files.items():
        spec = importlib.util.spec_from_file_location("updated_f16_"+name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        loaded[name] = mod
    return loaded


def array_sha(array, dtype, shape):
    require(array.shape == shape and array.dtype.kind == dtype[1] and array.dtype.itemsize == 8,
            "SEED_SHAPE_OR_TYPE")
    return digest(array.astype(dtype,copy=False).tobytes(order="C"))


def seed_identity(x, ids, volume):
    result = dict(positions=array_sha(x,"<f8",(POINTS,2)), physical_ids=array_sha(ids,"<i8",(POINTS,)),
                  volume=array_sha(volume,"<f8",(POINTS,)))
    require(all(value == GEOMETRY[name] for name,value in result.items()), "F16_SEED_BINDING")
    return result


def check_clock(driver, solver):
    require((driver.step_size(solver,16),solver.WIDTH,solver.WALL_SPEED) == (F16_DT,WIDTH,SPEED),
            "F16_SCHEDULE")


def bind_fields(observed, selector, mode, ids):
    require(mode == "F" and observed and "field_ids" not in observed, "FIELD_REQUEST")
    fields = selector(mode,ids)
    require(fields is ids, "ORIGINAL_FIELD_IDENTITY")
    observed["field_ids"] = array_sha(fields,"<i8",(POINTS,))
    require(observed == GEOMETRY, "F16_FIELD_BINDING")
    return fields


def check_setup(repo):
    """Check the local F16 bytes, actual native seed, field selector and clock."""
    driver = modules(repo)["driver"]
    solver = driver.fixed_solver()
    check_clock(driver,solver)
    x, ids, volume = solver.seed(16)
    observed = seed_identity(x,ids,volume)
    bind_fields(observed,driver.field_ids,"F",ids)
    return dict(status="F16_SETUP_OK",candidate_sha256=KERNEL,geometry_sha256=observed,
                points_count=len(x),dt=F16_DT,width=WIDTH,wall_speed=SPEED)


def receipt(mods, arm, native, calls, geometry):
    trace = (arm/"trace.csv").read_bytes()
    require(tuple(native[k] for k in ("protocol","status","label","setting","arm","cells","points_count","origin")) ==
            (mods["dt"].NATIVE,"TARGET_BRACKETED","DEVELOPMENT_ONLY",1,"F",16,POINTS,"new"), "NATIVE_BINDING")
    require(type(calls) is int and type(native["steps"]) is int and calls == native["steps"] and calls > 0,
            "PROJECTOR_CALL_COUNT")
    require(geometry == GEOMETRY and native["budget_s"] == BUDGET and math.isfinite(native["elapsed_s"])
            and native["elapsed_s"] >= 0 and native["source_sha256"] == mods["driver"].SOURCE,
            "NATIVE_CONFIGURATION")
    require(native["trace_sha256"] == digest(trace), "TRACE_BINDING")
    mods["dt"].parse_curve(trace, calls, F16_DT, WIDTH, SPEED)
    return dict(protocol=PROTOCOL,label="DEVELOPMENT_ONLY",stage3_go=False,u6_qualified=False,
                cells=16,mapping="ORIGINAL",status=native["status"],points_count=POINTS,
                dt=F16_DT,width=WIDTH,wall_speed=SPEED,source_sha256=SOURCE,
                candidate_sha256=KERNEL,candidate_calls=calls,geometry_sha256=geometry,
                adapter_sha256=digest(HERE.read_bytes()),f8_release=F8_PIN,
                f8_archive_sha256=F8_ARCHIVE,f8_original_trace_sha256=F8_ORIGINAL,
                trace_sha256=digest(trace),native_result_sha256=digest((arm/"result.json").read_bytes()))


def run(repo, arm, budget):
    require(budget == BUDGET, "BUDGET")
    if arm.exists() or arm.is_symlink():
        raise FileExistsError(arm)
    mods = modules(repo)
    driver = mods["driver"]
    factory, selector = driver.fixed_solver, driver.field_ids
    solver = factory()
    check_clock(driver,solver)
    native_seed, native_project = solver.seed, solver.project_contacts
    observed = {}
    observer = mods["observer"].ObservedProjector(mods["kernel"],mods["capture"])

    def seed(cells):
        require(cells == 16 and not observed, "SEED_REQUEST")
        x, ids, volume = native_seed(cells)
        observed.update(seed_identity(x,ids,volume))
        return x, ids, volume

    def field_ids(mode, ids):
        return bind_fields(observed,selector,mode,ids)

    def project(ids, nodes, mass, grad, velocity, centers, friction):
        require(friction == .5 and observed == GEOMETRY, "CONTACT_CONFIGURATION")
        return observer.project_contacts(ids,nodes,mass,grad,velocity,centers,friction)

    solver.seed, solver.project_contacts = seed, project
    driver.fixed_solver, driver.field_ids = lambda: solver, field_ids
    try:
        native = driver.run_arm("F",16,budget,arm)
        if native["status"] == "TARGET_BRACKETED":
            require(native == json.loads((arm/"result.json").read_bytes()), "NATIVE_RESULT_BYTES")
            record = receipt(mods,arm,native,observer.calls,observed)
            driver.write_json(arm/"candidate.json",record)
            return 0
        incomplete = dict(status="NATIVE_STOP",native_status=native["status"])
    except FileExistsError:
        raise
    except Exception as error:
        incomplete = dict(status="CONTACT_STOP" if observer.stop else "OTHER_EXCEPTION",
                          exception=type(error).__name__, message=str(error))
    finally:
        solver.seed, solver.project_contacts = native_seed, native_project
        driver.fixed_solver, driver.field_ids = factory,selector
    if arm.is_dir():
        if observer.stop is not None:
            incomplete["contact_stop_sha256"] = mods["capture"].write_json(arm/"contact_stop.json",observer.stop)
            incomplete["attempted_step"] = observer.stop["attempted_step"]
        incomplete.update(trace=mods["observer"].trace_info(arm/"trace.csv"), candidate_sha256=KERNEL,
                          label="DEVELOPMENT_ONLY",stage3_go=False,u6_qualified=False)
        driver.write_json(arm/"incomplete.json",incomplete)
    print(incomplete["status"])
    return 4


def check_arm(repo, arm):
    mods = modules(repo)
    require(not any((arm/n).exists() for n in ("incomplete.json","contact_stop.json")), "ARM_INCOMPLETE")
    native = json.loads((arm/"result.json").read_bytes())
    actual = json.loads((arm/"candidate.json").read_bytes())
    expected = receipt(mods,arm,native,native["steps"],GEOMETRY)
    require(json.dumps(actual,sort_keys=True) == json.dumps(expected,sort_keys=True), "CANDIDATE_RECEIPT")
    return actual


if __name__=="__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    run_args = sub.add_parser("run")
    check_args = sub.add_parser("check")
    setup_args = sub.add_parser("check-setup")
    setup_args.add_argument("--repo",type=Path,required=True)
    for parser in (run_args,check_args):
        parser.add_argument("--repo",type=Path,required=True)
        parser.add_argument("--out",type=Path,required=True)
    run_args.add_argument("--budget",type=float,choices=(BUDGET,),required=True)
    args = ap.parse_args()
    if args.command == "check-setup":
        print(json.dumps(check_setup(args.repo),sort_keys=True))
    elif args.command == "check":
        check_arm(args.repo,args.out)
        print("F16_ORIGINAL_VALIDATED")
    else:
        rc = run(args.repo,args.out,args.budget)
        if rc == 0:
            print("TARGET_BRACKETED")
        raise SystemExit(rc)

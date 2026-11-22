"""One development grid pair for the three-body fallback. Both arms use one kernel."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import tarfile

HERE = Path(__file__).resolve()
PREVIOUS = "docs/reviews/suyoung_u6c_updated_f16_20261122"
READER_SHA = "5b4f391b7fe23503192405aff94dad836b7ab76a54b4a7fa4b8d20a0836638e0"
ADAPTER_SHA = "de76a1068a938875745165ce649a0390418d9a34993dad9fd82ae3b4e95c0e54"
KERNEL = "acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645"
STOP_SHA = "bdd10395a7acc1aa7e64f7aaa6d8509a343ea448b47ee39e0770f520e310ec6d"
STOP_TRACE = "aba3b5e93bbdda6400777e2bc73ebf75a5eb7792aed2da9661be048836999def"
BUDGET = {8: 1140, 16: 1740}
F8_GEOMETRY = {
    "positions": "474424dea2a36388e28e02b9a5d47f9dad183bb1672dbf4e33ea84bdf7a6efc9",
    "volume": "78fe7907be63b6b084b71ec3262bf2d3f936b2b4eca65c255fc99cdd666a69f0",
    "physical_ids": "a91d7701d1e24908a53f6807d6bc9042402e70fba67bc82393889895a06868e4",
}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path, expected):
    require(sha(path.read_bytes()) == expected, "SOURCE_BINDING_" + path.stem.upper())
    spec = importlib.util.spec_from_file_location("three_body_" + path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def load_sources(repo):
    reader = load(repo / PREVIOUS / "read_f8_f16.py", READER_SHA)
    adapter = load(repo / PREVIOUS / "f16_candidate.py", ADAPTER_SHA)
    for name, expected in adapter.SOURCE.items():
        require(sha((repo / "scripts" / name).read_bytes()) == expected, "NATIVE_SOURCE")
    mods = {"driver": load(repo / "scripts/suyoung_u6b_dev.py", adapter.SOURCE["suyoung_u6b_dev.py"]),
            "kernel": load(repo / "scripts/suyoung_multicontact_dev.py", KERNEL),
            "reader": reader, "adapter": adapter}
    for name in ("observer", "capture"):
        rel, digest = adapter.HELPERS[name]
        mods[name] = load(repo / "docs/reviews" / rel, digest)
    return mods


def expected_geometry(cells):
    if cells == 8:
        return dict(F8_GEOMETRY, field_ids=F8_GEOMETRY["physical_ids"])
    return load(HERE.parents[1] / "suyoung_u6c_updated_f16_20261122/f16_candidate.py", ADAPTER_SHA).GEOMETRY


def seed_hashes(x, ids, volume, cells):
    points = 9653 if cells == 8 else 39053
    result = {}
    for name, arr, dtype, shape in (("positions", x, "<f8", (points, 2)),
                                    ("physical_ids", ids, "<i8", (points,)),
                                    ("volume", volume, "<f8", (points,))):
        require(arr.shape == shape and arr.dtype.kind == dtype[1] and arr.dtype.itemsize == 8, "SEED_LAYOUT")
        result[name] = sha(arr.astype(dtype, copy=False).tobytes(order="C"))
    expected = expected_geometry(cells)
    require(all(expected[name] == digest for name, digest in result.items()), "SEED_GEOMETRY")
    return result


def select_fields(selector, cells, arm, ids, observed):
    require(arm == "F" and observed and "field_ids" not in observed, "FIELD_REQUEST")
    fields = selector(arm, ids)
    require(fields is ids, "ORIGINAL_FIELD_SELECTOR")
    observed["field_ids"] = sha(fields.astype("<i8", copy=False).tobytes(order="C"))
    require(observed == expected_geometry(cells), "ORIGINAL_IDS")
    return fields


def setup_geometry(driver, solver, cells):
    dt = .0022463670164795577 if cells == 8 else .0011231835082397789
    require((driver.step_size(solver, cells), solver.WIDTH, solver.WALL_SPEED) ==
            (dt, .7024180763115129, .01996548746349992), "ARM_SCHEDULE")
    x, ids, volume = solver.seed(cells)
    observed = seed_hashes(x, ids, volume, cells)
    select_fields(driver.field_ids, cells, "F", ids, observed)
    return observed


def make_receipt(mods, cells, folder, native, calls, geometry):
    require(type(calls) is int and type(native["steps"]) is int and calls == native["steps"] and calls > 0,
            "PROJECTOR_COUNT")
    require(geometry == expected_geometry(cells) and native["budget_s"] == BUDGET[cells] and
            math.isfinite(native["elapsed_s"]) and native["elapsed_s"] >= 0., "ARM_CONFIGURATION")
    data = (folder / "trace.csv").read_bytes()
    curve = mods["reader"].native_curve(data, native, cells)
    raw = (folder / "result.json").read_bytes()
    require(json.loads(raw) == native, "NATIVE_RESULT")
    receipt = dict(protocol="U6c-step4803-pair-v1", label="DEVELOPMENT_ONLY", cells=cells, mapping="ORIGINAL",
                   status="TARGET_BRACKETED", candidate_calls=calls, kernel_sha256=KERNEL, geometry=geometry,
                   trace_sha256=sha(data), native_result_sha256=sha(raw), runner_sha256=sha(HERE.read_bytes()),
                   stage3_go=False, u6_qualified=False)
    return data, curve, receipt


def run_arm(repo, cells, folder):
    if folder.exists() or folder.is_symlink():
        raise FileExistsError(folder)
    mods = load_sources(repo)
    driver = mods["driver"]
    factory, selector = driver.fixed_solver, driver.field_ids
    solver = factory()
    setup_geometry(driver, solver, cells)
    native_seed, native_project = solver.seed, solver.project_contacts
    observed = {}
    observer = mods["observer"].ObservedProjector(mods["kernel"], mods["capture"])

    def seed(count):
        require(count == cells and not observed, "SEED_REQUEST")
        x, ids, volume = native_seed(count)
        observed.update(seed_hashes(x, ids, volume, count))
        return x, ids, volume

    def project(*args):
        require(args[-1] == .5 and observed == expected_geometry_cached, "CONTACT_CONFIGURATION")
        return observer.project_contacts(*args)

    expected_geometry_cached = expected_geometry(cells)
    driver.fixed_solver = lambda: solver
    driver.field_ids = lambda arm, ids: select_fields(selector, cells, arm, ids, observed)
    solver.seed, solver.project_contacts = seed, project
    try:
        value = driver.run_arm("F", cells, BUDGET[cells], folder)
        if value["status"] == "TARGET_BRACKETED":
            _, _, receipt = make_receipt(mods, cells, folder, value, observer.calls, observed)
            driver.write_json(folder / "candidate.json", receipt)
            return 0
        incomplete = dict(status="NATIVE_STOP", native_status=value["status"])
    except FileExistsError:
        raise
    except Exception as error:
        incomplete = dict(status="CONTACT_STOP" if observer.stop else "OTHER_EXCEPTION",
                          exception=type(error).__name__, message=str(error))
    finally:
        driver.fixed_solver, driver.field_ids = factory, selector
        solver.seed, solver.project_contacts = native_seed, native_project
    if folder.is_dir():
        if observer.stop is not None:
            incomplete["attempted_step"] = observer.stop["attempted_step"]
            incomplete["contact_stop_sha256"] = mods["capture"].write_json(folder / "contact_stop.json", observer.stop)
        incomplete.update(trace=mods["observer"].trace_info(folder / "trace.csv"), kernel_sha256=KERNEL,
                          cells=cells, label="DEVELOPMENT_ONLY", u6_qualified=False, stage3_go=False)
        driver.write_json(folder / "incomplete.json", incomplete)
    print(incomplete["status"])
    return 4


def read_arm(mods, cells, folder):
    require(not any((folder / n).exists() for n in ("contact_stop.json", "incomplete.json")), "INCOMPLETE_ARM")
    value = json.loads((folder / "result.json").read_bytes())
    data, curve, expected = make_receipt(mods, cells, folder, value, value["steps"], expected_geometry(cells))
    require(json.dumps(json.loads((folder / "candidate.json").read_bytes()), sort_keys=True) ==
            json.dumps(expected, sort_keys=True), "ARM_RECEIPT")
    return data, curve, expected


def bound_trace(archive, expected_archive, member, expected_trace):
    with archive.open("rb") as f:
        require(hashlib.file_digest(f, "sha256").hexdigest() == expected_archive, "HISTORY_ARCHIVE")
        f.seek(0)
        with tarfile.open(fileobj=f, mode="r:gz") as t:
            info = t.getmember(member)
            require(info.isfile(), "TRACE_MEMBER")
            raw = t.extractfile(info).read()
    require(sha(raw) == expected_trace, "HISTORY_TRACE")
    return raw


def prefix_matches(previous, current):
    return current.startswith(previous) and len(current) > len(previous)


def check_history(cells, previous, current):
    if cells == 8:
        require(previous == current, "F8_TRACE_CHANGED")
    else:
        require(prefix_matches(previous, current), "F16_PREFIX_CHANGED_OR_NOT_EXTENDED")


def old_f16(path):
    return bound_trace(path, STOP_SHA, "run/F16/trace.csv", STOP_TRACE)


def old_f8(mods, path):
    reader = mods["reader"]
    reader.read_f8(path)
    return bound_trace(path, reader.F8_ARCHIVE, "run/ORIGINAL/trace.csv", reader.F8_TRACE)


def write_json(path, value):
    with path.open("x", encoding="ascii", newline="\n") as f:
        json.dump(value, f, ensure_ascii=True, sort_keys=True, indent=2, allow_nan=False)
        f.write("\n")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    sub = cli.add_subparsers(dest="action", required=True)
    for name, fields in (("check", ("repo", "f8", "stop")), ("arm", ("repo", "out")),
                         ("check8", ("repo", "f8", "run")), ("read", ("repo", "f8", "stop", "run", "out")),
                         ("partial", ("stop", "run", "out"))):
        cmd = sub.add_parser(name)
        for field in fields:
            cmd.add_argument("--" + field, type=Path, required=True)
        if name == "arm":
            cmd.add_argument("--cells", type=int, choices=(8, 16), required=True)
    a = cli.parse_args()
    if a.action == "partial":
        prior = old_f16(a.stop).splitlines(keepends=True)
        current = (a.run / "F16/trace.csv").read_bytes().splitlines(keepends=True)
        count = next((i for i, (x, y) in enumerate(zip(prior, current)) if x != y), min(len(prior), len(current)))
        write_json(a.out, dict(identical_leading_lines_including_header=count, prior_lines=len(prior),
                               current_lines=len(current), u6_qualified=False, stage3_go=False))
        return 0
    if a.action == "arm":
        return run_arm(a.repo, a.cells, a.out)
    mods = load_sources(a.repo)
    reader = mods["reader"]
    rule = reader.get_rule(a.repo)
    previous8 = old_f8(mods, a.f8)
    if a.action == "check":
        old_f16(a.stop)
        for cells in (8, 16):
            setup_geometry(mods["driver"], mods["driver"].fixed_solver(), cells)
        print("BOTH_HISTORIES_AND_NATIVE_SEEDS_OK")
        return 0
    raw8, coarse, receipt8 = read_arm(mods, 8, a.run / "F8")
    check_history(8, previous8, raw8)
    if a.action == "check8":
        print("NEW_F8_RECEIPT_AND_FULL_HISTORY_MATCH")
        return 0
    previous16 = old_f16(a.stop)
    raw16, fine, receipt16 = read_arm(mods, 16, a.run / "F16")
    check_history(16, previous16, raw16)
    report = reader.blank_report()
    report.update(receipts={"F8": receipt8, "F16": receipt16}, kernel_sha256=KERNEL,
                  F8_native_trace="ALL_BYTES_EQUAL", F16_native_prefix="ALL_BYTES_EQUAL_THROUGH_STEP_4802",
                  previous_f8_sha256=reader.F8_ARCHIVE, previous_f16_sha256=STOP_SHA)
    rc = reader.apply(rule, report, coarse, fine)
    write_json(a.out, report)
    print(report["status"], report["pairs"]["F8_F16"]["comparison"])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())

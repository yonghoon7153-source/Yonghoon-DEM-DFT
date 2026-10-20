"""Independent S02 review, Windows. Production and submitted sources stay immutable.

Modes: core, axis, mutants, failclosed, sweep. All mutations are in-process and
explicitly named. Generated results are confined to evidence/s02.
"""
from pathlib import Path
import contextlib
import copy
import hashlib
import inspect
import io
import json
import math
import os
import platform
import struct
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT.parent
OUTDIR = ROOT / "evidence/s02"
OUTDIR.mkdir(parents=True, exist_ok=True)
TEMP = OUTDIR / "tmp"
TEMP.mkdir(exist_ok=True)
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"
os.environ["TEMP"] = os.environ["TMP"] = str(TEMP)
sys.path[:0] = [
    str(ROOT / "source/scripts"), str(ROOT / "source/webapp"),
    str(WORK / "lhs_coverage_review_20260930/deps"),
    str(WORK / "gen2_network_reverify3_20261007/deps"),
]
import numpy as np
import scipy
import network_conductivity as nc
import tau_flux as tf
import test_l214r_r01_restored_full as submitted
from test_lhs214_model_limit import chain_bed

MODE = sys.argv[1]
START = time.perf_counter()
RESULT = {
    "mode": MODE,
    "source_pin": "34713ac9650ece7c8d59b7c4d9a2aefccee693ea",
    "environment": dict(python=sys.version, platform=platform.platform(), numpy=np.__version__, scipy=scipy.__version__),
    "checks": [], "logs": {},
}


def mark(name, ok, detail=None):
    result = dict(name=name, ok=bool(ok), detail=detail)
    RESULT["checks"].append(result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


def shift(value, count):
    for _ in range(abs(count)):
        value = math.nextafter(value, math.inf if count > 0 else 0.0)
    return value


def bits(value):
    return struct.unpack(">Q", struct.pack(">d", value))[0]


def produce(area, bx, by):
    A, C, plate, _ = chain_bed(1.0, area=area)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return nc._run_all_networks(A, C, [1], [], {1: "SE"}, 1, plate, bx, by, None, contact_mode="hertzian")


def raw(rec):
    cert = rec["solve_certificate_full"]
    geometry = cert["geometry"]
    # Explicit independent transcription of producer arithmetic, no submitted
    # geometry/search/raw helper and no q_withheld as the numerical oracle.
    thickness = geometry["plate_z"] * geometry["scale"]
    cross_section = geometry["box_x"] * geometry["box_y"] * geometry["scale"] ** 2
    return (cert["I_bottom"] / cert["delta_V"]) * thickness / cross_section


def describe_search(search):
    return {key: value for key, value in search.items() if key not in ("A", "C", "plate")}


def capture(name, fn):
    submitted._ok, submitted._fail = 0, []
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
        fn()
    RESULT["logs"][name] = stream.getvalue()
    return dict(passed=submitted._ok, failed=len(submitted._fail), failures=list(submitted._fail))


def replace_function(module, name, before, after):
    original = getattr(module, name)
    source = inspect.getsource(original)
    assert source.count(before) == 1, (name, before, source.count(before))
    scope = dict(module.__dict__)
    exec(compile(source.replace(before, after), f"<S02 in-memory mutant: {MODE}:{name}>", "exec"), scope)
    setattr(module, name, scope[name])
    return original


if MODE == "core":
    RESULT["identities"] = {}
    for rel in ("scripts/network_conductivity.py", "scripts/tau_flux.py"):
        now = (ROOT / "source" / rel).read_bytes()
        old = (WORK / "lhs214s_recheck_20261019/source" / rel).read_bytes()
        RESULT["identities"][rel] = dict(same=now == old, sha256=hashlib.sha256(now).hexdigest())
    mark("producer and consumer byte-identical to prior pin", all(v["same"] for v in RESULT["identities"].values()), RESULT["identities"])
    RESULT["starts"] = {}
    for label, area in dict(registered=submitted.E_AREA, **submitted.E2_START).items():
        A, C, plate, _ = chain_bed(1.0, area=area)
        old_found, old_steps, old_problems = submitted.find_boundary_inputs(nc, A, C, plate, submitted.E_BX, submitted.E_BY)
        search = submitted.e0_search(nc, area, submitted.E_BX, submitted.E_BY)
        repeated = submitted.e0_search(nc, area, submitted.E_BX, submitted.E_BY)
        records = {key: produce(search["area"], submitted.E_BX, by) for key, by in search["bys"].items()}
        facts = {
            key: dict(by=search["bys"][key], raw=raw(rec), raw_hex=raw(rec).hex(),
                      I_bottom=rec["solve_certificate_full"]["I_bottom"],
                      status=rec["sigma_full_status"], stored_q=rec["sigma_full"],
                      withheld=rec["solve_certificate_full"].get("q_withheld"))
            for key, rec in records.items()
        }
        assertions = submitted._e_checks(nc, tf, search["A"], search["C"], search["plate"], submitted.E_BX, search["bys"])
        RESULT["starts"][label] = dict(start_area=area, one_axis=dict(found=old_found, steps=old_steps, problems=old_problems),
                                      search=describe_search(search), records=facts, assertions=assertions)
        mark(f"{label}: deterministic exact three-boundary fixture at one area",
             not search["probs"] and describe_search(search) == describe_search(repeated)
             and {key: value["raw"] for key, value in facts.items()} == submitted.E_Q
             and len({value["I_bottom"] for value in facts.values()}) == 1,
             RESULT["starts"][label])
        mark(f"{label}: original E1-E4 policy assertions pass", len(assertions) == 4 and all(v[1] for v in assertions))
    mark("Windows original registered one-axis skip remains reproducible",
         "prev" in RESULT["starts"]["registered"]["one_axis"]["problems"],
         RESULT["starts"]["registered"]["one_axis"])
    result = capture("E Eprime Esecond E5", lambda: (
        submitted.sec_E({}), submitted.sec_E_shift({}), submitted.sec_E2({}), submitted.sec_E5({})))
    mark("submitted E/Eprime/Esecond/E5 sections pass unmodified", result["passed"] == 18 and result["failed"] == 0, result)

elif MODE == "axis":
    base = produce(submitted.E_AREA, submitted.E_BX, submitted.E_BY["eq"])
    cert = base["solve_certificate_full"]
    numerator = (cert["I_bottom"] / cert["delta_V"]) * 20.0
    RESULT["I_bottom"] = cert["I_bottom"]
    RESULT["I_lattice_2p53"] = cert["I_bottom"] * 2 ** 53
    combinations = [(submitted.E_BX, submitted.E_BY["eq"]), (0.6, 0.9), (0.9, 0.6), (0.51, 1.04), (1.2, 0.45), (2.0, 0.265)]
    box_records = []
    for bx, by in combinations:
        rec = produce(submitted.E_AREA, bx, by)
        c = rec["solve_certificate_full"]
        box_records.append(dict(bx=bx, by=by, I=c["I_bottom"], raw=raw(rec), arithmetic=numerator / (bx * by)))
    RESULT["box_records"] = box_records
    mark("six actual box geometries preserve current; explicit q formula is bit-exact",
         all(v["I"] == cert["I_bottom"] and v["raw"] == v["arithmetic"] for v in box_records), box_records)
    # The following 129 real solves are independent of the submitted search.
    scan = []
    for offset in range(-64, 65):
        by = shift(submitted.E_BY["eq"], offset)
        rec = produce(submitted.E_AREA, submitted.E_BX, by)
        scan.append(dict(offset=offset, by=by, product=submitted.E_BX * by, raw=raw(rec),
                         I=rec["solve_certificate_full"]["I_bottom"]))
    RESULT["registered_scan"] = scan
    increments = [bits(b["product"]) - bits(a["product"]) for a, b in zip(scan, scan[1:])]
    mark("registered box_y neighbourhood covers each product double without gaps",
         set(increments) <= {0, 1} and 0 in increments and 1 in increments, dict(increments=sorted(set(increments)), span=bits(scan[-1]["product"]) - bits(scan[0]["product"])))
    mark("129 real records: original prev remains absent, exact eq/next present",
         not any(v["raw"] == submitted.E_Q["prev"] for v in scan)
         and all(any(v["raw"] == submitted.E_Q[key] for v in scan) for key in ("eq", "next"))
         and all(v["I"] == cert["I_bottom"] for v in scan))
    # Enumerate representable denominator products themselves. This is stronger
    # than varying box_x: every bx*by is one of these floats near the boundary.
    p0 = numerator / 1.5
    denominator_scan = [dict(offset=i, product=shift(p0, i), q=numerator / shift(p0, i)) for i in range(-8, 9)]
    RESULT["denominator_scan"] = denominator_scan
    mark("product-level enumeration proves missing prev locally for this current",
         denominator_scan[0]["q"] > submitted.E_Q["next"]
         and denominator_scan[-1]["q"] < submitted.E_Q["prev"]
         and not any(v["q"] == submitted.E_Q["prev"] for v in denominator_scan), denominator_scan)
    bx_sweep = []
    for index in range(-200, 201):
        bx = shift(submitted.E_BX, index)
        by0 = numerator / (bx * 1.5)
        values = [numerator / (bx * shift(by0, j)) for j in range(-8, 9)]
        bx_sweep.append(dict(offset=index, bx=bx, hits={k: tgt in values for k, tgt in submitted.E_Q.items()}))
    RESULT["box_x_sweep"] = bx_sweep
    mark("401 box_x arithmetic probes cannot supply missing prev", all(not v["hits"]["prev"] for v in bx_sweep),
         dict(count=len(bx_sweep), prev_hits=sum(v["hits"]["prev"] for v in bx_sweep)))

elif MODE == "mutants":
    base = submitted.e0_search(nc, submitted.E_AREA, submitted.E_BX, submitted.E_BY)
    RESULT["unmutated_fixture"] = describe_search(base)
    producer_before = "reject = sigma_ratio > FULL_Q_GUARD_MAX"
    consumer_before = "if branch == 'full' and q_rec > nc.FULL_Q_GUARD_MAX:"
    mutations = [
        ("producer_ge", nc, "solve_network", producer_before, "reject = sigma_ratio >= FULL_Q_GUARD_MAX", (1,)),
        ("producer_rounded", nc, "solve_network", producer_before, "reject = round(sigma_ratio, 8) > FULL_Q_GUARD_MAX", (0, 2, 3)),
        ("producer_disabled", nc, "solve_network", producer_before, "reject = False", (0, 2, 3)),
        ("consumer_ge", tf, "_cert_published_problem", consumer_before, "if branch == 'full' and q_rec >= nc.FULL_Q_GUARD_MAX:", (1,)),
        ("consumer_rounded", tf, "_cert_published_problem", consumer_before, "if branch == 'full' and round(q_rec, 8) > nc.FULL_Q_GUARD_MAX:", (3,)),
        ("consumer_disabled", tf, "_cert_published_problem", consumer_before, "if False:", (3,)),
    ]
    RESULT["mutations"] = []
    for label, module, name, before, after, must_fail in mutations:
        original = replace_function(module, name, before, after)
        try:
            search = submitted.e0_search(nc, submitted.E_AREA, submitted.E_BX, submitted.E_BY)
            assertions = submitted._e_checks(nc, tf, search["A"], search["C"], search["plate"], submitted.E_BX, search["bys"])
            e5 = capture(label + " E5", lambda: submitted.sec_E5({}))
            row = dict(label=label, search=describe_search(search), assertions=assertions, e5=e5,
                       failed=[i + 1 for i, v in enumerate(assertions) if not v[1]])
            RESULT["mutations"].append(row)
            mark(label + ": search still finds exact input and assertions detect wrong policy",
                 not search["probs"] and all(not assertions[i][1] for i in must_fail), row)
            if label.startswith("consumer_"):
                mark(label + ": independent E5 also detects policy error", e5["failed"] == 1, e5)
        finally:
            setattr(module, name, original)
    original = produce(base["area"], submitted.E_BX, base["bys"]["next"])
    restored = copy.deepcopy(original)
    submitted.restore(restored, "hertz", drop_guard=True)
    problems = tf.certificate_binding_problems("hertz", restored)
    mark("consumer rejects restored next despite removal of all four guard diagnostic keys",
         nc.MODEL_LIMIT_POLICY in repr(problems) and all(k not in restored["solve_certificate_full"] for k in submitted.GUARD_KEYS), problems)
    computed = produce(base["area"], submitted.E_BX, base["bys"]["eq"])
    snapshot = copy.deepcopy(computed)
    try:
        submitted.restore(computed, "hertz")
        error = None
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    mark("restore on published eq is explanatory ValueError with no mutation",
         error and error.startswith("ValueError:") and "q_withheld" in error and computed == snapshot, error)

elif MODE == "failclosed":
    real_restore = submitted.restore
    restore_calls = []
    def forbid_restore(*args, **kwargs):
        restore_calls.append(True)
        raise AssertionError("restore must not run after unavailable boundary")
    old_bound = submitted.E_AREA_ULP
    submitted.E_AREA_ULP = 0
    submitted.restore = forbid_restore
    try:
        limited = submitted.e0_search(nc, submitted.E_AREA, submitted.E_BX, submitted.E_BY)
        result = capture("limited registered E then E5", lambda: (
            submitted._guard("E", lambda: submitted.sec_E({})),
            submitted._guard("E5", lambda: submitted.sec_E5({}))))
        mark("kmax zero exhausts explicitly; E1-E4 fail without restore; independent E5 passes",
             bool(limited["probs"]) and len(limited["tried"]) == 1 and limited["bys"] == {}
             and result["failed"] == 5 and result["passed"] == 1 and not restore_calls,
             dict(search=describe_search(limited), result=result, restore_calls=len(restore_calls)))
    finally:
        submitted.E_AREA_ULP = old_bound
        submitted.restore = real_restore
    # Four adjacent q values are impossible for this denominator spacing;
    # forcing them tests the complete declared area bound (129 attempts).
    old_targets = submitted.E_Q
    targets = dict(old_targets, second_next=math.nextafter(old_targets["next"], math.inf))
    starts = dict(submitted.E_BY, second_next=submitted.E_BY["next"])
    submitted.E_Q = targets
    try:
        exhausted = submitted.e0_search(nc, submitted.E_AREA, submitted.E_BX, starts)
    finally:
        submitted.E_Q = old_targets
    mark("full declared bound exhaustion returns no partial fixture and explicit failure",
         bool(exhausted["probs"]) and len(exhausted["tried"]) == 129
         and exhausted["bys"] == {} and exhausted["area"] is None, describe_search(exhausted))
    real_raw = submitted._e_raw_q
    def raising_raw(*args, **kwargs):
        raise RuntimeError("independent injected search exception")
    submitted._e_raw_q = raising_raw
    try:
        result = capture("injected E exception then E5", lambda: (
            submitted._guard("E", lambda: submitted.sec_E({})),
            submitted._guard("E5", lambda: submitted.sec_E5({}))))
    finally:
        submitted._e_raw_q = real_raw
    mark("exception remains failed section and independent E5 still passes",
         result["failed"] == 1 and result["passed"] == 1 and "RuntimeError" in result["failures"][0], result)

elif MODE == "sweep":
    rows = []
    for offset in range(-200, 201):
        area = shift(submitted.E_AREA, offset)
        search = submitted.e0_search(nc, area, submitted.E_BX, submitted.E_BY)
        # Re-read production records; retain full search transcript for failures.
        found = {} if search["probs"] else {
            key: raw(produce(search["area"], submitted.E_BX, by))
            for key, by in search["bys"].items()
        }
        rows.append(dict(offset=offset, start_area=area, search=describe_search(search), raw=found,
                         ok=not search["probs"] and found == submitted.E_Q))
        if (offset + 200) % 25 == 0:
            print(json.dumps(dict(progress=len(rows), total=401, seconds=time.perf_counter()-START)), flush=True)
    RESULT["sweep"] = rows
    RESULT["sweep_summary"] = dict(total=len(rows), failures=sum(not v["ok"] for v in rows),
                                    second_axis_needed=sum(v["search"]["k"] != 0 for v in rows),
                                    max_abs_k=max(abs(v["search"]["k"] or 0) for v in rows),
                                    max_attempts=max(len(v["search"]["tried"]) for v in rows))
    mark("401 starting areas all produce independently re-read exact boundaries", all(v["ok"] for v in rows), RESULT["sweep_summary"])
else:
    raise ValueError(MODE)

RESULT["seconds"] = time.perf_counter() - START
RESULT["summary"] = dict(passed=sum(c["ok"] for c in RESULT["checks"]), total=len(RESULT["checks"]))
(OUTDIR / f"{MODE}.json").write_text(json.dumps(RESULT, ensure_ascii=False, indent=2), encoding="utf8")
(OUTDIR / f"{MODE}.log").write_text("\n\n".join(f"=== {key} ===\n{value}" for key, value in RESULT["logs"].items()), encoding="utf8")
print(json.dumps(dict(summary=RESULT["summary"], seconds=RESULT["seconds"])), flush=True)
sys.exit(0 if all(c["ok"] for c in RESULT["checks"]) else 1)

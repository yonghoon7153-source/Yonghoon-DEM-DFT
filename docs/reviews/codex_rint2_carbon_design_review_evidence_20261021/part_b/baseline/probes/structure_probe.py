"""Independent RIMPR-01/final-frame probes; no submitted selftest imports.

Original 10-15 counterexamples are replayed from their retained bytes without
rewriting them. New fixtures use an analytic equal-sphere disk area and an
independent serializer. Only review evidence and review temporary files change.
"""
from pathlib import Path
import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
import math
import os
import sys
import types
import warnings

ROOT = Path(__file__).resolve().parents[1]
PRIOR = ROOT.parent / "rint_g2_impl_reverify_20261015"
TMP = ROOT / "tmp/structure_fixtures"
TMP.mkdir(parents=True, exist_ok=True)
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
            "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
for key in ("TEMP", "TMP", "TMPDIR"):
    os.environ[key] = str(TMP)
sys.path[:0] = [
    str(ROOT / "source/scripts"),
    str(ROOT.parent / "lhs_coverage_review_20260930/deps"),
    str(ROOT.parent / "gen2_network_reverify3_20261007/deps"),
]
try:
    import resource
except ImportError:
    # Only a Windows memory-report diagnostic adapter; no numerical replacement.
    resource = types.ModuleType("resource")
    resource.RUSAGE_SELF = 0
    resource.getrusage = lambda _: types.SimpleNamespace(ru_maxrss=float("nan"))
    sys.modules["resource"] = resource
import numpy as np
import rint_iface_join as J
import step3_sigma as S

spec = importlib.util.spec_from_file_location(
    "structure_prior_join", PRIOR / "source/scripts/rint_iface_join.py")
OLD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(OLD)
TM = {1: "AM_P", 2: "SE"}
SUFFIX = ("sc.csv", "atom.dump", "contact.dump")
results = []
fixture_manifest = {}
contexts = {}


def independent_lines(contact=True):
    centers = ((.002, .002, .002), (.0035 if contact else .005, .002, .002))
    radius = .001
    distance = centers[1][0] - centers[0][0]
    area = math.pi * (radius * radius - (distance / 2) ** 2)
    box = ["ITEM: BOX BOUNDS ff ff ff"] + ["0 0.01"] * 3
    atom = ["ITEM: TIMESTEP", "100", "ITEM: NUMBER OF ATOMS", "2"] + box
    atom += ["ITEM: ATOMS id type x y z radius"]
    atom += [f"{k+1} 1 " + " ".join("%g" % x for x in (*c, radius))
             for k, c in enumerate(centers)]
    cont = ["ITEM: TIMESTEP", "100", "ITEM: NUMBER OF ENTRIES",
            "1" if contact else "0"] + box
    cont += ["ITEM: ENTRIES " + " ".join(f"c_cpl[{k}]" for k in range(1, 24))]
    if contact:
        values = [*centers[0], *centers[1], 1, 2, 0] + [0] * 12
        values += [area, 2 * radius - distance]
        cont += [" ".join("%g" % x for x in values)]
    sc = [",".join(["1", *(f"{x:.12f}" for x in (*c, radius))])
          for c in centers]
    return [sc, atom, cont]


def save(tag, lines, gz=False, newline="\n"):
    paths = []
    for suffix, body in zip(SUFFIX, lines):
        path = TMP / (tag + "_" + suffix + (".gz" if gz else ""))
        data = (newline.join(body) + newline).encode("utf8")
        path.write_bytes(gzip.compress(data, mtime=0) if gz else data)
        paths.append(path)
    fixture_manifest[tag] = [
        {"path": str(p.relative_to(ROOT)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in paths]
    return paths


def make_context(join):
    c, r, t = (join["particles"][k] for k in ("c_um", "r_um", "t"))
    with contextlib.redirect_stdout(io.StringIO()):
        sid, _ = S.rasterize(c, r, t, None, None, (0, 0, 0), (7, 4, 4),
                            .25, bridge_um=.24)
    ledger = S.am_iface_ledger(
        c, r, t, sid, sid, (0, 0, 0), .25,
        delta_bound_um=join["g_geo"]["delta_bound_um"], bridge_um=.24)
    return sid, ledger


def consume(join, context):
    sid, ledger = context
    plan = S.am_iface_plan(
        ledger, {"AM_P|AM_P": .001}, join=join, gap_law="cut",
        unreg_law="cut", ambiguous_arm="cut")
    out = {"plan_codes": [r["code"] for r in plan["rejections"]]}
    try:
        S.iface_require_quantitative(plan, sid=sid, vox=.25)
        out["quantitative_guard"] = "ACCEPT"
    except Exception as exc:
        out["quantitative_guard"] = type(exc).__name__
        out["quantitative_message"] = str(exc)
    return out


def compact(join):
    return {
        "status": join["status"],
        "codes": [r["code"] for r in join["rejections"]],
        "rejections": join["rejections"],
        "entrance": join.get("entrance"),
        "g_geo": join["g_geo"],
        "g_frame": join["g_frame"],
        "geom_reuse": join.get("geom_reuse"),
    }


def evaluate(tag, paths, expected, *, context="base", compare_prior=False,
             kwargs=None, prior_bytes=False):
    out = {"case": tag, "expected": expected, "paths": [str(p) for p in paths]}
    if prior_bytes:
        out["original_fixture_sha256"] = [hashlib.sha256(p.read_bytes()).hexdigest()
                                          for p in paths]
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            join = J.am_iface_join(*paths, type_map=TM, **(kwargs or {}))
        out.update(compact(join))
        out["warnings"] = [str(w.message) for w in caught]
        if context:
            out.update(consume(join, contexts[context]))
    except Exception as exc:
        out.update(status="EXCEPTION", exception=type(exc).__name__, message=str(exc))
    if compare_prior:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                old = OLD.am_iface_join(*paths, type_map=TM, **(kwargs or {}))
            out["prior"] = {"status": old["status"],
                            "codes": [r["code"] for r in old["rejections"]]}
        except Exception as exc:
            out["prior"] = {"status": "EXCEPTION", "exception": type(exc).__name__,
                            "message": str(exc)}
    out["unexpected_pass"] = expected == "reject" and out["status"] == "PASS"
    out["unexpected_reject"] = expected == "pass" and out["status"] != "PASS"
    results.append(out)
    print(tag, out["status"], out.get("codes"), out.get("quantitative_guard"),
          "UNEXPECTED" if out["unexpected_pass"] or out["unexpected_reject"] else "",
          flush=True)
    return out


basepaths = save("baseline", independent_lines())
base = J.am_iface_join(*basepaths, type_map=TM)
contexts["base"] = make_context(base)
zeropaths = save("zero_contacts", independent_lines(contact=False))
contexts["zero"] = make_context(J.am_iface_join(*zeropaths, type_map=TM))
evaluate("independent_baseline", basepaths, "pass", compare_prior=True)
evaluate("independent_zero_contacts", zeropaths, "pass", context="zero", compare_prior=True)

# Exact retained counterexamples: no path substitution inside old probe or data.
for tag in (
    "baseline", "malformed_numeric_contact_row_inside_block",
    "malformed_numeric_atom_row_inside_block", "malformed_extra_contact_row",
    "malformed_extra_atom_row", "duplicate_radius_column", "step_extra_token",
    "count_extra_token", "wellshaped_duplicate_contact_control",
    "wellshaped_duplicate_atom_control",
):
    paths = [PRIOR / "tmp/join_independent" / (tag + "_" + s) for s in SUFFIX]
    evaluate("original_" + tag, paths, "pass" if tag == "baseline" else "reject",
             compare_prior=True, prior_bytes=True)


def probe(tag, edit, expected="reject", **kw):
    lines = independent_lines()
    edit(lines)
    return evaluate(tag, save(tag, lines), expected, **kw)


def setline(fi, row, value):
    return lambda lines: lines[fi].__setitem__(row, value)


def append_col(fi, name, value="nan"):
    def edit(lines):
        lines[fi][8] += " " + name
        for k in range(9, len(lines[fi])):
            lines[fi][k] += " " + value
    return edit


for fi, name in ((1, "atom"), (2, "contact")):
    required = ("id", "type", "x", "y", "z", "radius") if fi == 1 else (
        *(f"c_cpl[{k}]" for k in range(1, 10)), "c_cpl[22]", "c_cpl[23]")
    for col in required:
        probe(name + "_duplicate_" + col.replace("[", "_").replace("]", ""),
              append_col(fi, col))
    for rowname, a, b in (("count", 2, 4), ("box", 4, 8), ("rows", 8, None)):
        def duplicate(lines, fi=fi, a=a, b=b):
            lines[fi].extend(lines[fi][a:b])
        probe(name + "_duplicate_section_" + rowname, duplicate)
    for row in (0, 2, 4, 8, len(independent_lines()[fi])):
        def unknown(lines, fi=fi, row=row):
            lines[fi][row:row] = ["ITEM: UNKNOWN", "unconsumed junk"]
        probe(name + "_unknown_at_" + str(row), unknown)
    for count in ("0", "-1", "3", "", "1.0", "1e0", "1_0", "1 garbage",
                  "9223372036854775808", "9" * 5000):
        probe(name + "_count_" + (count[:24] or "empty"), setline(fi, 3, count))
    for step in ("100 0.9", "100\n0.9", "100\v0.9", "100\f0.9",
                 "", "\n100", "100\n\n0.9", "100#comment", "100.0",
                 "1e2", "1_00", "9223372036854775808"):
        tag = name + "_step_case_" + str(len(results))
        probe(tag, setline(fi, 1, step))
    for a, b, label in ((2, 4, "count"), (4, 8, "box"), (8, None, "rows")):
        probe(name + "_missing_" + label,
              lambda lines, fi=fi, a=a, b=b: lines[fi].__delitem__(slice(a, b)))
    probe(name + "_preamble", lambda lines, fi=fi: lines[fi].insert(0, "junk"))
    probe(name + "_trailing_junk", lambda lines, fi=fi: lines[fi].append("junk"))
    probe(name + "_fourth_box_line", lambda lines, fi=fi: lines[fi].insert(8, "0 0.01"))
    probe(name + "_leading_scalar_blank", lambda lines, fi=fi: lines[fi].insert(1, ""))
    probe(name + "_interior_box_blank", lambda lines, fi=fi: lines[fi].insert(6, ""))
    probe(name + "_last_frame_empty",
          lambda lines, fi=fi: lines[fi].append("ITEM: TIMESTEP"))
    probe(name + "_last_frame_partial",
          lambda lines, fi=fi: lines[fi].extend(["ITEM: TIMESTEP", "101", "ITEM: NUMBER OF " + ("ATOMS" if fi == 1 else "ENTRIES")]))
    probe(name + "_last_frame_valid",
          lambda lines, fi=fi: lines[fi].extend(lines[fi].copy()))
    probe(name + "_earlier_frame_malformed",
          lambda lines, fi=fi: lines[fi].__setitem__(slice(0, 0),
              ["ITEM: TIMESTEP", "bad", "ITEM: UNKNOWN", "bad"]))
    for extra in ("suffix", " 0.9"):
        probe(name + "_step_header_" + extra.replace(" ", "_"),
              setline(fi, 0, "ITEM: TIMESTEP" + extra))
        probe(name + "_count_header_" + extra.replace(" ", "_"),
              setline(fi, 2, independent_lines()[fi][2] + extra))

# New attack: no separating token or repeated section marker inside a header.
# Each should be a malformed/unknown ITEM header under the declared e6 scope.
for fi, name in ((1, "atom"), (2, "contact")):
    for label, row, old, new in (
        ("rows_no_boundary", 8, "ITEM: ATOMS " if fi == 1 else "ITEM: ENTRIES ",
         "ITEM: ATOMS" if fi == 1 else "ITEM: ENTRIES"),
        ("box_no_boundary", 4, "BOUNDS ", "BOUNDS"),
        ("rows_repeated_marker", 8, "ITEM: ATOMS" if fi == 1 else "ITEM: ENTRIES",
         "ITEM: ATOMSITEM: ATOMS" if fi == 1 else "ITEM: ENTRIESITEM: ENTRIES"),
        ("box_repeated_marker", 4, "ITEM: BOX BOUNDS", "ITEM: BOX BOUNDSITEM: BOX BOUNDS"),
        ("rows_marker_at_end", 8, None, " ITEM: ATOMS" if fi == 1 else " ITEM: ENTRIES"),
    ):
        def edit(lines, fi=fi, row=row, old=old, new=new):
            lines[fi][row] = (lines[fi][row].replace(old, new, 1) if old
                              else lines[fi][row] + new)
        probe(name + "_" + label, edit, compare_prior=True)

# Whitespace and storage positives, plus the declared D19 reuse contract.
def blank_ok(lines):
    for fi in (1, 2):
        for row in (len(lines[fi]), 9, 8, 4, 2, 0):
            lines[fi].insert(row, " \t")
probe("blank_whitespace_only", blank_ok, "pass", compare_prior=True)
evaluate("gzip_baseline", save("gzip_baseline", independent_lines(), gz=True),
         "pass", compare_prior=True)
evaluate("crlf_baseline", save("crlf_baseline", independent_lines(), newline="\r\n"),
         "pass", compare_prior=True)
for scalar in ("+100", "000100", "-0"):
    def same_steps(lines, scalar=scalar):
        lines[1][1] = lines[2][1] = scalar
    probe("integer_valid_" + scalar, same_steps, "pass", compare_prior=True)
for declared, expected in ((None, "reject"),
                           ({"atom_step": 100, "contact_step": 101,
                             "reason": "independent same-geometry control"}, "pass"),
                           ({"atom_step": 100, "contact_step": 102}, "reject")):
    probe("d19_" + expected + "_" + str(len(results)), setline(2, 1, "101"), expected,
          kwargs={"geom_reuse": declared}, compare_prior=True)

# Additional columns have explicitly limited certification: only consumed fields
# are numeric-validated; duplicate/garbage optional values are documented controls.
probe("unconsumed_optional_atom_column", append_col(1, "diagnostic", "garbage"),
      "pass", compare_prior=True)
probe("unconsumed_optional_contact_column", append_col(2, "diagnostic", "garbage"),
      "pass", compare_prior=True)

# Original compressed production bytes: no reserialization and no test helpers.
for name, scaffold, atom, contact, tmap in (
    ("real14", "real14_am_scaffold.csv",
     "real14_reference_20260928/atom_2060000.liggghts.gz",
     "real14_reference_20260928/contact_2060000.liggghts.gz",
     {1: "AM_P", 2: "AM_S", 3: "SE"}),
    ("case15", "case15_corner_20261001/case15_am_scaffold.csv",
     "case15_corner_20261001/atom_v4_1710000.liggghts.gz",
     "case15_corner_20261001/contact_v4_1710000.liggghts.gz",
     {1: "AM_P", 2: "SE"}),
):
    data = ROOT / "source/docs/data"
    paths = [data / p for p in (scaffold, atom, contact)]
    with warnings.catch_warnings(record=True) as caught:
        join = J.am_iface_join(*paths, type_map=tmap)
    out = {"case": name, **compact(join),
           "sha256": [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
           "warnings": [str(w.message) for w in caught]}
    results.append(out)
    print(name, join["status"], join["g_geo"], flush=True)

report = {
    "source_pin": "2b9efa253edbf455c2e1abfef1d60e51818e01f8",
    "prior_pin": "dcb97f1ed942f622d9189eee1a1e9432dc05a655",
    "notes": [
        "Original fixtures replayed byte-for-byte, not regenerated.",
        "Current/prior join modules share unchanged imported numerical dependencies.",
        "New fixtures generated independently; no submitted selftest imported.",
        "Windows resource shim affects only memory diagnostics.",
        "Last-frame validation is distinguished from whole-history validation; multiple frames always reject.",
    ],
    "summary": {
        "n_cases": len(results),
        "unexpected_pass": [r["case"] for r in results if r.get("unexpected_pass")],
        "unexpected_reject": [r["case"] for r in results if r.get("unexpected_reject")],
    },
    "results": results,
}
(ROOT / "evidence/structure_results.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf8")
(ROOT / "evidence/structure_fixture_manifest.json").write_text(
    json.dumps(fixture_manifest, ensure_ascii=False, indent=2), encoding="utf8")
print(json.dumps(report["summary"], ensure_ascii=False), flush=True)

"""Independent R7 pure-function mutations; no solver or network execution.

Run from anywhere; stdout is the evidence JSON. The caller saves stdout using
apply_patch. Source and imported evidence are read only, and -B avoids bytecode.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
sys.dont_write_bytecode = True
sys.path[:0] = [str(SOURCE / "scripts"), str(SOURCE / "webapp")]
import g2_network_reread as rr
import wsl_network_smoke as smoke

POS = SOURCE / "docs/reviews/codex_gen2_network_reverify6_evidence_20261011/evidence/r6_s0b_positive.input.json"
BASE = json.loads(POS.read_text(encoding="utf-8"))
CID = "case15_network"
REG = rr.CASE15_NEGCTL
RESULTS = []


def report(doc):
    return doc["reports"][CID]


def probe(name, mutation, expected, category, contract):
    doc = copy.deepcopy(BASE)
    mutation(doc)
    r = report(doc)
    try:
        verdicts = rr.case15_negctl_verdicts(r, doc["timings"][CID], CID)
        failed = {i: v for i, _name, v, _detail in verdicts if v != "PASS"}
        why = rr.case15_negctl_s0b_problems(CID, r, doc["checks"], doc["timings"][CID])
        produced = smoke.evaluate({CID: r}, {CID: doc["timings"][CID]})
        producer_fail = {c["id"]: c["verdict"] for c in produced if c.get("id", "").startswith("case15.") and c["verdict"] != "PASS"}
        observed = "pass" if not failed and not why else "reject"
        RESULTS.append(dict(name=name, category=category, expected=expected,
                            observed=observed, contract=contract,
                            failed_checks=failed, s0b_problem_count=len(why),
                            producer_matches_shared=(producer_fail == failed),
                            matches_expected=(observed == expected),
                            failing_details={i: str(d)[:450] for i, _n, v, d in verdicts if v != "PASS"}))
    except Exception as exc:
        RESULTS.append(dict(name=name, category=category, expected=expected,
                            observed="exception", exception=f"{type(exc).__name__}: {exc}",
                            contract=contract, matches_expected=False))


def set_r(key, value):
    return lambda d: report(d).__setitem__(key, value)


def set_tau(key, value):
    return lambda d: report(d)["tau"].__setitem__(key, value)


def set_cell(row, col, value):
    return lambda d: report(d)["negctl"]["negative_area"][row].__setitem__(col, value)


def raw_pair(key, value):
    return lambda d: report(d)["raw_sha"].__setitem__(key, value)


probe("positive_actual_20261009", lambda d: None, "pass", "positive", "Imported real report.")
probe("positive_raw_key_order", lambda d: report(d).__setitem__("raw_sha", dict(reversed(list(report(d)["raw_sha"].items())))), "pass", "positive", "Mapping order is immaterial.")
probe("positive_tau_key_order", lambda d: report(d).__setitem__("tau", dict(reversed(list(report(d)["tau"].items())))), "pass", "positive", "Mapping order is immaterial.")
probe("positive_negative_row_order", lambda d: report(d)["negctl"]["negative_area"].reverse(), "pass", "positive", "Rows are compared after sorting.")
probe("positive_check_order", lambda d: d["checks"].reverse(), "pass", "positive", "Stable ID collection is unordered.")
probe("positive_tuple_sha_pair", lambda d: report(d).__setitem__("raw_sha", {k: tuple(v) for k, v in report(d)["raw_sha"].items()}), "pass", "positive", "stage_refbed emits tuples before JSON serialization.")
probe("positive_tuple_inner_rows", lambda d: report(d)["negctl"].__setitem__("negative_area", [tuple(v) for v in report(d)["negctl"]["negative_area"]]), "pass", "positive", "Helper explicitly supports tuple rows; JSON converts to lists.")
probe("positive_lexical_precision", lambda d: report(d)["negctl"].__setitem__("negative_area", json.loads('[[31,29241,-1.860360e-1,1.0511400],[38,29241,-0.1862640,1.051200e0]]')), "pass", "positive", "Equivalent JSON number spellings parse to identical floats.")
probe("positive_all_blank_tau_fields_removed", lambda d: report(d).__setitem__("tau", {k:v for k,v in report(d)["tau"].items() if v is not None}), "pass", "positive", "No numeric exposure; missing optional numeric fields remain blank.")
probe("positive_blank_tau_empty_strings", lambda d: report(d).__setitem__("tau", {k:('' if v is None else v) for k,v in report(d)["tau"].items()}), "pass", "positive", "Empty strings retain blank-cell semantics.")
probe("positive_check_id_name_swap", lambda d: (d["checks"][0].__setitem__("id", "case15.raw_sha"), d["checks"][1].__setitem__("id", "case15.proc")), "pass", "positive", "Verdicts are recomputed from report by stable ID; names/details are nonauthoritative display text.")

# SHA: independently exercise every registered file and both sides of each pair.
for key, pair in report(BASE)["raw_sha"].items():
    for side in (0, 1):
        for label, val in (("wrong", "0" * 12), ("uppercase", pair[side].upper()), ("full64", REG["raw_sha256"][key]), ("short", pair[side][:-1]), ("nonhex", "g" * 12), ("integer", 123456789012), ("bool", True), ("null", None)):
            new_pair = list(pair)
            new_pair[side] = val
            probe(f"sha_{key}_{side}_{label}", raw_pair(key, new_pair), "reject", "negative_sha", "Both sides must be lowercase hexadecimal strings of exactly 12 characters matching the registered prefix.")
    probe(f"sha_{key}_both_wrong", raw_pair(key, ["0" * 12, "0" * 12]), "reject", "negative_sha", "Mutually equal hashes must still match the registration.")
    probe(f"sha_{key}_absent", lambda d,k=key: report(d)["raw_sha"].pop(k), "reject", "negative_sha", "Closed four-file map.")
    probe(f"sha_{key}_three_values", raw_pair(key, pair + [pair[0]]), "reject", "negative_sha", "Pair has exactly two elements.")
for label, val in (("absent", None), ("empty", {}), ("list", []), ("string", "hashes"), ("bool", True)):
    probe("sha_shape_" + label, set_r("raw_sha", val), "reject", "negative_sha", "Raw detail must be a mapping with all four registered keys.")
probe("sha_extra_key", lambda d: report(d)["raw_sha"].__setitem__("extra", ["a"*12]*2), "reject", "negative_sha", "Closed four-file map.")
probe("sha_mixed_key_types", lambda d: report(d)["raw_sha"].__setitem__(1, ["a"*12]*2), "reject", "negative_sha", "Malformed non-JSON-map input must fail closed without propagating an exception.")
for val in (False, 0, 1, "True", None):
    probe("sha_flag_" + repr(val), set_r("raw_sha_ok", val), "reject", "negative_sha", "The summary flag must be the Boolean True.")

# Negative area rows: both rows and all four positions, without relying on the shipped tests.
for row in (0, 1):
    for col in (0, 1):
        original = report(BASE)["negctl"]["negative_area"][row][col]
        for label, val in (("bool", True), ("float_integer", float(original)), ("string", str(original)), ("null", None), ("wrong", original+1)):
            probe(f"row{row}_id{col}_{label}", set_cell(row,col,val), "reject", "negative_rows", "IDs must be actual integers at the registered positions.")
    for col in (2, 3):
        original = report(BASE)["negctl"]["negative_area"][row][col]
        values = (("bool", True), ("string", str(original)), ("null", None), ("zero", 0), ("nan", math.nan), ("inf", math.inf), ("negative_inf", -math.inf), ("wrong_sign", -original), ("one_ulp", math.nextafter(original, math.inf)), ("subprecision", original+1e-8), ("one_micro", original+1e-6), ("huge_integer", 10**400))
        for label,val in values:
            probe(f"row{row}_value{col}_{label}", set_cell(row,col,val), "reject", "negative_rows", "Fixed producer emits round(raw_unit_conversion, 6); values must be finite, signed correctly, and equal to that display value.")
probe("rows_duplicate", lambda d: report(d)["negctl"].__setitem__("negative_area", [report(d)["negctl"]["negative_area"][0]]*2), "reject", "negative_rows", "Registered pairs are distinct.")
probe("rows_extra", lambda d: report(d)["negctl"]["negative_area"].append([1,2,-1.,1.]), "reject", "negative_rows", "Exactly two rows.")
probe("rows_missing", lambda d: report(d)["negctl"]["negative_area"].pop(), "reject", "negative_rows", "Exactly two rows.")
probe("rows_tuple_container", lambda d: report(d)["negctl"].__setitem__("negative_area", tuple(report(d)["negctl"]["negative_area"])), "reject", "nonproducer_schema", "Producer list comprehension and JSON array both produce a list, not tuple container.")
for row in (0,1):
    for size in (0,1,2,3,5):
        probe(f"row{row}_length{size}", lambda d,row=row,size=size: report(d)["negctl"]["negative_area"].__setitem__(row, (report(d)["negctl"]["negative_area"][row] + [99])[:size]), "reject", "negative_rows", "Exactly four columns per row.")
probe("rows_endpoints_swapped", lambda d: [r.__setitem__(slice(0,2), list(reversed(r[:2]))) for r in report(d)["negctl"]["negative_area"]], "reject", "nonproducer_schema", "IDs preserve ordered c_cpl[7]/c_cpl[8] fields from registered bytes; no undirected-pair normalization exists in producer.")
probe("rows_values_swapped_across_pairs", lambda d: (report(d)["negctl"]["negative_area"][0].__setitem__(slice(2,4), [ -0.186264, 1.0512]), report(d)["negctl"]["negative_area"][1].__setitem__(slice(2,4), [-0.186036, 1.05114])), "reject", "negative_rows", "Each pair binds its own area and delta.")

solver = REG["solver_step"]
for label, val in (("empty", []), ("other", ["Parse"]), ("extra", [solver, "Parse"]), ("duplicate", [solver, solver]), ("string", solver), ("null", None), ("tuple", (solver,))):
    probe("failed_stages_"+label, set_r("failed_stages", val), "reject", "negative_stage", "The producer emits exactly the required solver failure as a list.")
for field,val in (("status", "done"), ("stage_e_ran", True), ("stage_e_ran", 0), ("returned_network_run_id", "RUN-x")):
    probe(f"blocked_{field}_{val}", set_r(field,val), "reject", "negative_stage", "Existing publication-blocking contract is preserved.")

for key in ("tau_ion_hertz", "tau2_flux_ion_net_full", "unregistered_numeric", "ion_net_status_reason_hertz", "case"):
    for label,val in (("integer", 1), ("float", 0.5), ("zero", 0), ("nan", math.nan), ("inf", math.inf)):
        probe(f"tau_{key}_{label}", set_tau(key,val), "reject", "negative_tau", "Every top-level int/float other than bool is rejected, regardless of key.")
for label,val in (("bool", True), ("string_numeric", "1.5"), ("nested_dict", {"value":1.5}), ("nested_list", [1.5])):
    probe("tau_registered_"+label, set_tau("tau_ion_hertz",val), "reject", "negative_tau", "Registered numeric-column prefixes reject every nonblank value, including nested containers and bool.")
for label,val in (("bool", True), ("string_numeric", "1.5"), ("nested_dict", {"tau_ion_hertz":1.5}), ("nested_list", [1.5]), ("deep_nested", {"a":[{"value":1.5}]})):
    probe("tau_unknown_"+label, set_tau("extra",val), "pass", "nonproducer_boundary", "Current producer selects flat scalar case_row fields and cannot emit this new nested tau extension; shallow scanning is not recursive JSON validation.")
probe("tau_missing_mode", lambda d: report(d)["tau"].pop("ion_net_status_hertz_h12"), "reject", "negative_tau", "All three statuses remain required.")
probe("tau_bad_mode", set_tau("ion_net_status_physics", "OK"), "reject", "negative_tau", "All three statuses must be NOT_COMPUTED.")

# Read only fixed raw contact bytes: reproduce display conversion, not the network.
contact_path = SOURCE / "docs/data/case15_corner_20261001/contact_v4_1710000.liggghts.gz"
raw_neg = []
with gzip.open(contact_path, "rt", encoding="utf-8") as fh:
    fields = None
    for line in fh:
        if line.startswith("ITEM: ENTRIES"):
            fields = line[len("ITEM: ENTRIES"):].split()
            break
    for line in fh:
        if not line.strip() or line.startswith("ITEM"):
            continue
        r = dict(zip(fields, line.split()))
        area, delta = float(r["c_cpl[22]"]), float(r["c_cpl[23]"])
        if area < 0:
            raw_neg.append(dict(id1=int(float(r["c_cpl[7]"])), id2=int(float(r["c_cpl[8]"])),
                                raw_area=r["c_cpl[22]"], raw_delta=r["c_cpl[23]"],
                                area_um2=area*1e6, delta_um=delta*1000,
                                displayed=[int(float(r["c_cpl[7]"])), int(float(r["c_cpl[8]"])), round(area*1e6,6), round(delta*1000,6)]))
displayed = [r["displayed"] for r in raw_neg]
probe("positive_raw_bytes_display_conversion", lambda d: report(d)["negctl"].__setitem__("negative_area", displayed), "pass", "positive", "Direct gzip read + producer's documented six-decimal conversion; no solver execution.")
probe("unrounded_raw_values", lambda d: report(d)["negctl"].__setitem__("negative_area", [[r["id1"],r["id2"],r["area_um2"],r["delta_um"]] for r in raw_neg]), "reject", "nonproducer_schema", "Unrounded input is not the current report format; producer explicitly rounds to six decimals.")

readme = (SOURCE / "docs/data/case15_corner_20261001/README.md").read_text(encoding="utf-8")
table = dict((m.group(2),m.group(1)) for m in re.finditer(r"^([0-9a-f]{64})\s+[\d,]+ B\s+(\S+)", readme, re.M))
artifact = dict(schema="r7_predicate_probes/v1", review_pin="3cedd40a5911d0606bf33ed2085d5cb93c4db2e0",
                scope="Pure predicates and producer evaluate only; raw gzip display conversion read only; no DEM, WSL or network simulation.",
                source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (Path(rr.__file__),Path(smoke.__file__),POS)},
                raw_negative_rows=raw_neg,
                registered_rows_equal_producer_display=(sorted(map(tuple,displayed)) == sorted(REG["negative_rows_ref"])),
                registered_sha_table_matches_readme=all(table.get(k)==v for k,v in REG["raw_sha256"].items()),
                result_counts=dict(Counter(r["category"] for r in RESULTS)), total=len(RESULTS),
                mismatches=[r["name"] for r in RESULTS if not r["matches_expected"]],
                producer_shared_mismatches=[r["name"] for r in RESULTS if r.get("producer_matches_shared") is False],
                results=RESULTS)
print(json.dumps(artifact, ensure_ascii=False, indent=2, allow_nan=False))
sys.exit(1 if artifact["mismatches"] or artifact["producer_shared_mismatches"] else 0)

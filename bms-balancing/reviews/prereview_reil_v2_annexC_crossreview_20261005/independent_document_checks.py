"""Independent document algebra/partition checks. NOT a REIL/P0 execution.

Standard library only. No submitted code imports, workbooks, fitting or network.
Run: python independent_document_checks.py --out evidence/independent_checks.json
Optional --prior-snapshot PATH checks the prior review's three protocol documents.
The required --out is the sole file this program writes; inputs stay unchanged.
"""
import argparse
import hashlib
import itertools
import json
import re
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOC = "bms-balancing/docs/"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--prior-snapshot", type=Path)
    args = parser.parse_args()
    snap_path = ROOT / "input_bundle/RECEIVED_SNAPSHOT.json"
    remote_path = ROOT / "evidence/remote_identity.json"
    inputs = [snap_path, remote_path]
    if args.prior_snapshot:
        inputs.append(args.prior_snapshot)
    if args.out.resolve() in {p.resolve() for p in inputs}:
        raise ValueError("Output must not replace an input")
    snap = json.loads(snap_path.read_text(encoding="utf8"))
    remote = json.loads(remote_path.read_text(encoding="utf8"))
    rmap = {r["path"]: r for r in remote["files"]}
    checks = []

    def check(name, passed, **evidence):
        checks.append(dict(name=name, passed=bool(passed), **evidence))

    def text(name):
        return snap["files"][DOC + name]["content"]

    check("fixed_commit", snap["fixed_commit"] == remote["fixed_commit"] ==
          "4ad68af441cf00981c1b7e27bd71f5a1858ff70e")
    check("remote_inventory", set(rmap) == set(snap["files"]))
    for path, rec in snap["files"].items():
        raw = rec["content"].encode("utf8")
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        check("blob_and_saved_remote_identity:" + path,
              blob == rec["sha"] == rmap[path]["sha"] and not rmap[path]["error"],
              blob=blob, sha256=hashlib.sha256(raw).hexdigest())

    prior_status = "NOT_RECHECKED_WITHOUT_OPTIONAL_PRIOR_SNAPSHOT"
    if args.prior_snapshot:
        prior = json.loads(args.prior_snapshot.read_text(encoding="utf8"))
        prior_status = {"fixed_commit": prior["fixed_commit"], "path": str(args.prior_snapshot),
                        "sha256": hashlib.sha256(args.prior_snapshot.read_bytes()).hexdigest()}
        for name in ["REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md",
                     "REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md",
                     "REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md"]:
            path = DOC + name
            check("prior_bytes_unchanged:" + name,
                  snap["files"][path]["content"].encode("utf8") ==
                  prior["files"][path]["content"].encode("utf8"))

    core = text("REIL_C1_CORE_SPEC_20261005.md")
    rows = {}
    for line in core.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|", line)
        if m:
            check("sheet_row_unique:" + m[1], int(m[1]) not in rows)
            rows[int(m[1])] = m[2]
    check("19_document_rows_not_workbook_observation", set(rows) == set(range(1, 20)))
    analysis, references = set(range(1, 12)), {15, 16}
    outside = set(rows) - analysis - references
    check("sheet_partition", outside == {12, 13, 14, 17, 18, 19} and
          not analysis.intersection(references),
          outside=[dict(index=i, name=rows[i]) for i in sorted(outside)])
    bad_sentence = next(s for s in core.splitlines() if "나머지 6 시트" in s)
    listed = {int(x) for x in re.findall(r"#(\d+)", bad_sentence)}
    check("N3_counterexample_prose_differs_from_table", listed == {12, 13, 15, 17, 18, 19}
          and listed != outside, erroneous_inclusion=sorted(listed-outside), omission=sorted(outside-listed))

    # Independently transcribed from source PDF p9 Table 1 (not fitted bars).
    # Columns: LAM_PE %, LAM_NE %, LLI %.
    paper_table = [(0,0,0),(0,0,10),(0,0,20),(36,0,0),(0,44,0),
                   (36,0,36),(36,0,42),(0,44,10),(0,44,20),(36,44,42),(36,44,49)]
    nominal = {}
    for line in text("REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md").splitlines():
        parts = [s.strip() for s in line.split("|")]
        if len(parts) > 5 and parts[1].isdigit() and re.fullmatch(r"\([\d., ]+\)", parts[4]):
            nominal[int(parts[1])] = tuple(F(v.strip()) for v in parts[4][1:-1].split(","))
    check("11_nominal_rows", set(nominal) == set(range(11)))
    for i, percentages in enumerate(paper_table):
        expected = tuple(1-F(p,100) for p in percentages)
        check("nominal_vs_paper_Table1:"+str(i), nominal.get(i) == expected,
              expected=[str(v) for v in expected])
    check("case3_G_exclusion_even_tau_005", nominal[3][0]+F(".05") < nominal[3][2]-F(".05"),
          max_mP="0.69", min_z="0.95", meaning="Frozen nominal vs G only, not empirical inventory")

    q, delta = F(3), F(".15")
    fresh1 = F("1.05")-delta/q
    check("N1_unit_fresh_not_requires_unit_mP_zero_delta", fresh1 == 1,
          mP=1.05, delta_mAh=.15, q_mAh=3, z_fresh=float(fresh1))
    fresh2, z = F(1)-delta/q, F(".8")
    relative = z/fresh2
    check("N1_nonunit_fresh_changes_coordinate", fresh2 == F(".95") and relative != z,
          z=float(z), z_fresh=float(fresh2), relative_remaining=float(relative),
          difference=float(relative-z), kind="Synthetic algebra; not a measured cell")
    check("N1_zero_degeneracy", F(0)/fresh2 == F(0),
          note="An individual zero does not prove global equality of coordinate systems")

    ce = F(".9")
    stock = F(100)  # mAh-equivalent inventory, entirely synthetic.
    product = ce**4
    constant_throughput = []
    for charge in [F(10), F(20)]:
        loss = sum((1-ce)*charge for _ in range(4))
        remaining = 1-loss/stock
        constant_throughput.append(dict(charge_each_mAh=float(charge),
                                       lost_mAh_equivalent=float(loss), remaining=float(remaining)))
        check("N2_CE_product_not_inventory:"+str(charge), remaining != product,
              product=float(product), remaining=float(remaining))
    # Sufficient telescoping construction, NOT asserted for the paper's experiment.
    stocks = [stock]
    for _ in range(4):
        stocks.append(ce*stocks[-1])
    check("N2_product_can_hold_under_extra_coupling", stocks[-1]/stock == product,
          required_extra_model="Each cycle charges the entire current inventory and loses fraction 1-CE")

    state_table = []
    for cycle, direction in itertools.product(["match", "mismatch", "unknown"], repeat=2):
        result = ("mismatch" if "mismatch" in (cycle,direction) else
                  "match" if cycle == direction == "match" else "unknown")
        expected = {("match","match"): "match", ("match","unknown"): "unknown",
                    ("unknown","match"): "unknown", ("unknown","unknown"): "unknown"}.get(
                        (cycle,direction), "mismatch")
        check("N3_proposed_combiner:"+cycle+"/"+direction, result == expected)
        state_table.append(dict(cycle=cycle, direction=direction, result=result))

    result = dict(scope="Document identities, paper-table transcription, synthetic algebra and proposed state table only",
                  fixed_commit=snap["fixed_commit"], prior_comparison=prior_status,
                  checks=checks, check_count=len(checks), all_pass=all(c["passed"] for c in checks),
                  ce_example=dict(CE_each=.9, cycles=4, initial_inventory_mAh_equivalent=100,
                                  product=float(product), scenarios=constant_throughput),
                  proposed_P0_summary_truth_table=state_table,
                  scientific_claims_automatically_proved=False,
                  workbooks_opened=False, provided_programs_executed=False, execution_authorized=False)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf8")
    print(json.dumps(dict(check_count=len(checks), all_pass=result["all_pass"], output=str(args.out)), ensure_ascii=False))
    raise SystemExit(0 if result["all_pass"] else 1)


if __name__ == "__main__":
    main()

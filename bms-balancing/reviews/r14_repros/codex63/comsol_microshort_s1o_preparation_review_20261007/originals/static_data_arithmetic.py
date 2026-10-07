"""Reviewer-owned data and arithmetic checks. No candidate import or execution."""
from pathlib import Path
from decimal import Decimal as D, localcontext
import json,hashlib
ROOT=Path(__file__).resolve().parent
R=ROOT/"received"
def sha(data): return hashlib.sha256(data).hexdigest()
code_manifest=json.loads((R/"CODE_MANIFEST.json").read_text())
code_checks=[]
for item in code_manifest["files"]:
    b=(R/item["path"]).read_bytes()
    code_checks.append({"path":item["path"],"match":len(b)==item["bytes"] and sha(b)==item["sha256"]})
plan=json.loads((R/"VALIDATION_PLAN.json").read_text())
ids=[x["id"] for x in plan["cases"]]
counts={}
for case in plan["cases"]: counts[case["engine"]]=counts.get(case["engine"],0)+1
s0manifest=json.loads((R/"reference/s0/MANIFEST.json").read_text())
s0entries=s0manifest["files"]
s0matches=[]
for item in s0entries:
    b=(R/"reference/s0"/item["path"]).read_bytes()
    s0matches.append(len(b)==item["bytes"] and sha(b)==item["sha256"])
with localcontext() as ctx:
    ctx.prec=50
    time=[D("0"),D("100"),D("100.001")]
    q=[D("0"),D("25.001"),D("25.00025")]
    qI=[D("0"),D("25"),D("25.00025")]
    points=[]
    for t,qn,qi in zip(time,q,qI):
        limit=D("0.0002")+D("0.0001")*max(qn,qi)
        points.append({"time":str(t),"qN_qP_C_m2":str(qn),"qI_qRN_qRP_C_m2":str(qi),
            "cumulative_residual":str(abs(qn-qi)),"existing_limit":str(limit),"residual_with_zero_bound_within":abs(qn-qi)<=limit})
    reversed_increment=q[2]-q[1]
    threshold=D(".001")
    fine=D("0.00100000000000000001")
    precision={"value":str(fine),"decimal_exceeds_0_001":fine>threshold,
        "binary64_value":repr(float(fine)),"binary64_threshold":repr(float(threshold)),
        "binary64_exceeds_0_001":float(fine)>float(threshold),
        "scope":"Independent scalar conversion arithmetic, not execution of the PowerShell or Python candidate."}
result={"scope":"Data/byte inspection and hand-trace scalar arithmetic only, not functional reproduction",
 "code_manifest_entries":len(code_checks),"code_manifest_all_match":all(x["match"] for x in code_checks),
 "s0_payload_entries":len(s0entries),"s0_payload_all_match":all(s0matches),
 "validation_unique_ids":len(set(ids)),"validation_cases":len(ids),"engine_counts":counts,
 "interval_reversal_arithmetic":{"assumptions":"I=j=RN=0.25 A/m2 for A=1; RP=-0.25; qN=qP; LiE constant; exact bound=0",
    "points":points,"last_inventory_transfer_increment_C_m2":str(reversed_increment),
    "negative_deadband_C_m2":"-0.0002","violates_interval_deadband":reversed_increment<D("-0.0002")},
 "precision_projection":precision}
with (ROOT/"STATIC_DATA_AND_ARITHMETIC.json").open("x",encoding="utf8") as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False))


"""Reviewer-owned fixed-text identity and scalar arithmetic, not REIL execution."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
root=Path(__file__).parent
s=json.loads((root/"RECEIVED_SNAPSHOT.json").read_text(encoding="utf-8"))
files=[]
for path,d in s["files"].items():
    b=d["content"].encode("utf-8")
    blob=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    files.append({"path":path,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"git_blob":blob,"blob_match":blob==d["sha"]})
assert all(x["blob_match"] for x in files)
p="bms-balancing/docs/"
assert s["files"][p+"REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md"]["sha"]=="872ca88b3b5c57aebf295bd0109e95a830b3ae13"
assert s["files"][p+"REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md"]["sha"]=="9f49d6061cf3c9e69ed35e3b00e5e0addafd8fd3"
prior="bms-balancing/reviews/prereview_reil_v2_annexA_20261004/"
m=json.loads(s["files"][prior+"PACKAGE_MANIFEST.json"]["content"])
manifest_checks=[]
for n in ("REVIEW_KO.md","DECISION.json"):
    b=s["files"][prior+n]["content"].encode("utf-8")
    e=next(e for e in m["files"] if e["path"]==n)
    local=(root/("PRIOR_"+n)).read_bytes()
    check={"name":n,"manifest_size_sha_match":len(b)==e["bytes"] and hashlib.sha256(b).hexdigest()==e["sha256"],"local_prior_byte_identical":b==local}
    assert all((check["manifest_size_sha_match"],check["local_prior_byte_identical"]))
    manifest_checks.append(check)
for n in ("REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md","REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md"):
    b=s["files"][p+n]["content"].encode("utf-8")
    e=next(e for e in m["files"] if e["path"]=="reference/"+n)
    assert len(b)==e["bytes"] and hashlib.sha256(b).hexdigest()==e["sha256"]
tol=F("1e-10")
g=F("0.0001")-(F(0.1)-F(0.09990000005))
tau=F(1.02000000005)-F("1.02")
assert 0<g<tol and 0<tau<tol
# Claim-specific residual illustration only, no real objective or model coordinates.
actual=F(1.00000000005); target=F(1); lo,hi=F("0.3"),F("1.5")
domain_violation=max(lo-actual,actual-hi)
claim_violation=actual-(F("0.98")+F("0.02"))
assert domain_violation<0 and 0<claim_violation<tol and 0<abs(actual-target)<tol
# Same-grid-node arithmetic from prior review, and the replacement counting rule.
q=[0.0,0.1/999,2*(0.1/999)]; v=[1.1,2.0,2.5]; c=2.0
left=q[0]+(c-v[0])*(q[1]-q[0])/(v[1]-v[0])
right=q[1]+(c-v[1])*(q[2]-q[1])/(v[2]-v[1])
assert left!=right and right==q[1]
def scalar_crossings(q,v,c):
    if any(a==c and b==c for a,b in zip(v,v[1:])):
        return {"flat":True,"nodes":[],"intervals":[],"count":None}
    nodes=[j for j,x in enumerate(v) if x==c]
    intervals=[j for j,(a,b) in enumerate(zip(v,v[1:])) if a!=c and b!=c and ((a<c<b) or (b<c<a))]
    return {"flat":False,"nodes":nodes,"intervals":intervals,"count":len(nodes)+len(intervals)}
cases={
    "same_grid_node":scalar_crossings(q,v,2.0),
    "tangent_contact":scalar_crossings([0,1,2],[1,2,1],2),
    "flat_rejected":scalar_crossings([0,1,2],[1,2,2],2),
    "strict_interior":scalar_crossings([0,1],[1,3],2),
    "two_crossings":scalar_crossings([0,1,2],[1,3,1],2),
    "endpoint_contact":scalar_crossings([0,1],[2,3],2)}
assert cases["same_grid_node"]["nodes"]==[1] and cases["same_grid_node"]["intervals"]==[]
assert cases["tangent_contact"]["count"]==1
assert cases["flat_rejected"]["flat"]
assert cases["strict_interior"]["count"]==1
assert cases["two_crossings"]["count"]==2
assert cases["endpoint_contact"]["count"]==1
counts=[{"n_valid":n,"nominal_before_dedup":min(4,n)+12,"within_16":min(4,n)+12<=16} for n in range(1,129)]
assert all(x["within_16"] for x in counts)
locals_cap=(128+3*46*4+2*16+1)*77
objectives_cap=locals_cap*2000+77*201
assert locals_cap==54901 and objectives_cap==109817477
# Check monotonicity on a fixed, entirely synthetic set; not objective evaluation.
pairs=[(F(1),F("1.2")),(F("1.2"),F(1))]
old_den=(F(1),F(1)); new_den=(F("0.5"),F("0.8"))
old_rho=[max(x/old_den[0],y/old_den[1]) for x,y in pairs]
new_rho=[max(x/new_den[0],y/new_den[1]) for x,y in pairs]
assert all(b>=a for a,b in zip(old_rho,new_rho))
report={"scope":"Fixed documentation bytes and reviewer-owned scalar arithmetic only. No REIL input, objective, P0, fit, cost measurement, provided program, implementation validation or COMSOL executed.",
    "fixed_commit":s["fixed_commit"],"files":files,"prior_review_checks":manifest_checks,"v2_and_annex_a_unchanged":True,
    "constant_residuals":{"G_exact":str(g),"G_approx":float(g),"tau_exact":str(tau),"tau_approx":float(tau),"both_numerically_accepted_not_exact":True},
    "claim_specific_grade_illustration":{"actual":str(actual),"profile_equality_residual":str(actual-target),"domain_violation":str(domain_violation),"nominal_interval_violation":str(claim_violation),"profile_domain_exact":True,"compatibility_numerical_only":True,"real_objective_evaluated":False},
    "grid_node_arithmetic":{"left_old":left,"right_old":right,"old_float_equal":left==right,"new_node_index":1,"new_position":q[1],"synthetic_rule_cases":cases},
    "start_count_examples":counts[:5],"start_count_all_1_to_128_within_16":True,
    "unchanged_nominal_caps":{"local_executions":locals_cap,"objective_calls_excluding_separate_items":objectives_cap},
    "fixed_set_rho_illustration":{"old":[str(x) for x in old_rho],"new":[str(x) for x in new_rho],"all_nondecreasing":True},
    "data_files_opened":False,"P0_executed":False,"provided_code_executed":False,"fit_executed":False,"installation_performed":False}
print(json.dumps(report,ensure_ascii=False))

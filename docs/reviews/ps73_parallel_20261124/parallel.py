"""Pure operating rules for the 7:3 isolated NP6 comparison."""
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from decimal import Decimal

BED="ps_7_3_r45"
ARMS=("UT","UC","UB","UVa")
GO="GO_PS73_PARALLEL_ONCE"
S0=3200000
UB_JOB="368469"
ORIG="ps45_a5_rj_9fd6aa9d3bee_1120_once"
OPS="ps73_isolated_1124"
OLD="ps73_dev_ops_20261121"
ACTIVE={"PENDING","RUNNING","COMPLETING","CONFIGURING","SUSPENDED","RESIZING","SIGNALING","STAGE_OUT","REQUEUED","REQUEUE_FED"}
HARD={"FAILED","CANCELLED","NODE_FAIL","OUT_OF_MEMORY","BOOT_FAIL","DEADLINE","PREEMPTED","REVOKED","SPECIAL_EXIT"}

def need(v,msg):
    if not v:
        raise ValueError(msg)

def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1048576),b""):
            h.update(b)
    return h.hexdigest()

def read(p):
    return json.loads(p.read_bytes())

def publish(p,v):
    fd,t=tempfile.mkstemp(dir=p.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf8") as f:
            json.dump(v,f,sort_keys=True,allow_nan=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.link(t,str(p))
    finally:
        os.unlink(t)

def claim_submit(p,record,send):
    publish(p/"claim.json",record)
    jid=send()
    need(isinstance(jid,str) and re.fullmatch("[1-9][0-9]*",jid),"AMBIGUOUS_SUBMISSION")
    publish(p/"ack.json",{"job":jid,**record})
    return jid

def arm_dir(ops,origin,arm):
    need(arm in ARMS,"unsupported arm")
    ops,origin=Path(ops),Path(origin).resolve()
    dest=ops/"runs"/arm/BED/arm
    need(ops.is_absolute() and dest.resolve()==dest and ops!=origin and
         ops not in origin.parents and origin not in dest.parents,"work paths overlap or redirect")
    return dest

def projected(text,new,unseen):
    rows={}
    for line in text.splitlines():
        if not line.strip():
            continue
        cols=line.strip().split("|")
        need(len(cols)==3,"bad queue row")
        jid,state,n=cols
        need(re.fullmatch(r"[0-9]+(?:_[0-9]+)?(?:\+[0-9]+)?",jid) and jid not in rows
             and state in ACTIVE and n.isdigit() and int(n)>0,"unknown allocation")
        rows[jid]=int(n)
    need(all(j not in rows or rows[j]==n for j,n in unseen.items()),"allocation changed")
    total=sum(rows.values())+sum(n for j,n in unseen.items() if j not in rows)+new
    need(total<=60,"CAPACITY_STOP projected="+str(total))
    return total

def ub_ready(state,r):
    return bool(state=="COMPLETED" and r and type(r.get("runner_rc")) is int
                and r["runner_rc"]==0 and r.get("technical_ok") is True)

def resume_ok(arm,state,step,prior):
    return arm in ("UB","UT","UVa") and state=="TIMEOUT" and step>prior

FIELDS=("ul_rstep","ul_k","ul_phase","ul_modeB","ul_pz","ul_lift","ul_ncross","ul_xk","ul_lk0","ul_Pbar","ul_kind")

def checkpoint(d):
    folder=d/"restart"
    found=[]
    for p in folder.glob("restart_unload_*.bin"):
        m=re.fullmatch(r"restart_unload_([0-9]+)\.bin",p.name)
        need(m is not None,"unknown restart name")
        found.append((int(m[1]),p))
    need(found,"NO_CHECKPOINT")
    step,binary=max(found)
    state=folder/("state_unload_%d.in"%step)
    need(binary.is_file() and binary.resolve()==binary and binary.stat().st_size>0 and
         state.is_file() and state.resolve()==state,"incomplete latest restart pair")
    vals={}
    for line in state.read_text("ascii").splitlines():
        parts=line.split()
        need(len(parts)==4 and parts[0]=="variable" and parts[1] not in vals,"invalid state record")
        key,kind,value=parts[1:]
        if key=="ul_kind":
            need(kind=="string" and value in ("0","A","B"),"restart motion kind")
        else:
            need(kind=="equal" and re.fullmatch(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?",value),"state number")
            value=Decimal(value)
            need(value.is_finite(),"nonfinite state")
        vals[key]=value
    need(set(vals)==set(FIELDS) and vals["ul_rstep"]==step and vals["ul_k"]==int(vals["ul_k"])
         and vals["ul_k"]>=0,"state/step mismatch")
    return dict(step=step,k=int(vals["ul_k"]),binary=digest(binary),state=digest(state))

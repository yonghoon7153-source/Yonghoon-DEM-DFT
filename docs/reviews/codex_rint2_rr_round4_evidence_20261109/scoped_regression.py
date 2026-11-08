"""Portable scoped rerun; no fixtures(), shell, host or research input.
Run: python -I -X utf8 -B scoped_regression.py [--repo PATH] [--out PATH]
This is implementation-authored regression rerun, not independent attack.
"""
import argparse, sys, os, json, tempfile, importlib.util, traceback, hashlib
from pathlib import Path
P=argparse.ArgumentParser()
P.add_argument("--repo",type=Path,default=Path(__file__).parent/"package"/"repo")
P.add_argument("--out",type=Path,default=Path(__file__).parent/"scoped_regression.json")
A=P.parse_args()
repo=A.repo.resolve()
sys.path.insert(0,str(repo/"scripts"))
blocked=[]
def audit(event,args):
    if event in ("subprocess.Popen","os.system","os.posix_spawn","socket.connect","socket.bind"):
        blocked.append(event)
        raise RuntimeError("Review forbids external process/network: "+event)
sys.addaudithook(audit)
# Windows has no O_NONBLOCK; all input handles here are regular synthetic files.
adaptation=[]
if not hasattr(os,"O_NONBLOCK"):
    os.O_NONBLOCK=0
    adaptation.append("os.O_NONBLOCK=0 on Windows regular-file synthetic fixtures only")
import rint_r_chain as R
import test_rint_r_chain as T
T.RR=R
result={"python":sys.version,"repo":str(repo),"source_sha256":{
p:hashlib.sha256((repo/"scripts"/p).read_bytes()).hexdigest()
for p in ("rint_r_chain.py","test_rint_r_chain.py")},
"platform_adapter":adaptation,"checks":{},"blocked_events":blocked,
"not_run":["fixtures()","full 495 chain","bash/Linux process groups/flock","actual 12-unit e2e","research inputs"]}
with tempfile.TemporaryDirectory(prefix="r4_scoped_",dir=A.out.parent) as td:
    T.TD=Path(td)
    for name in ("t_RR3A","t_RR3B","t_RR3C","t_PA14A"):
        try:
            ok,detail=getattr(T,name)()
            result["checks"][name]={"ok":bool(ok),"detail":detail}
        except Exception as exc:
            result["checks"][name]={"ok":False,"exception":repr(exc),"traceback":traceback.format_exc()}
    try:
        tau=T.pa14_tau()
        rows,bad=T.pa14_arm_eval(T.pa14_form_rows(tau),"independent_rerun_form")
        result["checks"]["PA14C_value_subpart_only"]={"ok":not bad,"rows":rows,"bad":bad,"tau":tau,
            "not_full_method":"s_main(P0/P1)/s_main_predict omitted: Linux fixture"}
    except Exception as exc:
        result["checks"]["PA14C_value_subpart_only"]={"ok":False,"exception":repr(exc),"traceback":traceback.format_exc()}
result["pass"]=all(x["ok"] for x in result["checks"].values()) and not blocked
A.out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"pass":result["pass"],"checks":{k:{"ok":v["ok"],"n":v.get("detail",{}).get("n"),"error":v.get("exception")} for k,v in result["checks"].items()},"blocked":blocked},ensure_ascii=False))
sys.exit(0 if result["pass"] else 1)


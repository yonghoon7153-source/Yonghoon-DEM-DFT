"""R8 numerical input provenance checks; synthetic workbooks, actual optimizers.

Uses the unchanged R7 fixture utilities committed inside the R8 target. No target
source or original input files are modified. All exported workbooks are temporary.
"""
from __future__ import annotations
import argparse
import contextlib
import csv
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sign_with_actual_helper(target, base, root, art, rid, state):
    shell=(target/"scripts/run_states.sh").read_text(encoding="utf-8")
    code=shell[shell.index("write_meta ()"):shell.index('\nmkdir -p "$OUT"')]
    code+='\n'+shell[shell.index("\nsay ()")+1:shell.index("\nfail=0")]
    code+='\nLAST_RUN_ID="$2"; write_meta "$1" "$3" GITT\n'
    env=dict(os.environ,STARTS="2",SI="Li",BMS_DATA_ROOT=str(root),OUT=str(base/"out"),
             PATH=str(Path(sys.executable).parent)+os.pathsep+os.environ.get("PATH",""))
    p=subprocess.run(["bash","-c",code,"r8",str(art),rid,state],cwd=base,
                     env=env,capture_output=True,text=True,timeout=30)
    assert p.returncode==0,(p.stdout,p.stderr)


def noise_closed(target, fx):
    from bms_balancing import verify as v
    with tempfile.TemporaryDirectory(prefix="bms-r8-noise-") as td:
        root=Path(td); fx.generate(target,root)
        wb=v.D.full_cell_workbook(root)
        def run():
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):
                v.cmd_noise(fx.args_for(root))
            return json.loads(buf.getvalue())
        A=run(); real_build=v.build; count=0
        def build_then_export(*a,**kw):
            nonlocal count
            obj=real_build(*a,**kw); count+=1
            fx.rewrite_xlsx(wb,"full",noise=.020)
            return obj
        with patch.object(v,"build",side_effect=build_then_export):
            raced=run()
        B=run()
        assert count==1 and raced==A
        assert A["inputs_sha"]!=B["inputs_sha"]
        assert A["sigma_at_k1_V"]!=B["sigma_at_k1_V"]
        fields=["misfit_rmse_pocv_V","sigma_at_k1_V","misfit_over_sigma_if_raw_data","inputs_sha"]
        return {"real_optimizer":True,"raced_full_JSON_equals_A":True,
                "A":{k:A[k] for k in fields},"raced":{k:raced[k] for k in fields},"B":{k:B[k] for k in fields}}


def reference_closed(target, fx):
    from bms_balancing import verify as v
    with tempfile.TemporaryDirectory(prefix="bms-r8-ref-") as td:
        base=Path(td); root=base/"inputs"; fx.generate(target,root)
        real_build=v.build; wb=v.D.full_cell_workbook(root)
        def run(name, export=False):
            observed=[]
            def build_then_export(*a,**kw):
                obj=real_build(*a,**kw); observed.append(obj.consumed_inputs)
                if a[2]=="pristine" and export:
                    fx.rewrite_xlsx(wb,"full",state="pristine")
                return obj
            art=base/f"{name}.csv"
            with patch.object(v.D,"SI_SOURCES",["Li"]),patch.object(v,"build",side_effect=build_then_export),contextlib.redirect_stdout(io.StringIO()):
                v.cmd_matrix(fx.args_for(root,art))
            rows=list(csv.DictReader(art.open(encoding="utf-8"))); assert len(rows)==1
            row=rows[0]
            assert json.loads(row["ref_consumed_inputs"])==observed[0]
            assert json.loads(row["consumed_inputs"])==observed[1]
            return row
        A=run("A"); mixed=run("mixed",True); B=run("B")
        assert A["inputs_sha"]!=mixed["inputs_sha"]==B["inputs_sha"]
        assert A["ref_inputs_sha"]==mixed["ref_inputs_sha"]!=B["ref_inputs_sha"]
        assert mixed["LAM_NE_pct"]!=B["LAM_NE_pct"]
        fields=["inputs_sha","ref_inputs_sha","LAM_NE_pct"]
        return {"real_optimizer":True,"target_ref_identity_matches_actual_builds":True,
                "A":{k:A[k] for k in fields},"mixed_exports_explicit":{k:mixed[k] for k in fields},
                "B":{k:B[k] for k in fields}}


def profile_identity_log_loss(target, fx, ex):
    from bms_balancing import verify as v
    with tempfile.TemporaryDirectory(prefix="bms-r8-profile-") as td:
        base=Path(td); ex.fixture(target,base)
        root=base/"inputs"; fx.generate(target,root)
        art=base/"out/profile_gamma_200_Li.csv"; log=Path(str(art)+".log")
        args=fx.args_for(root,art); args.run_id="r8-profile-complete"
        with log.open("w",encoding="utf-8") as out,contextlib.redirect_stdout(out):
            assert v.cmd_profile(args)==0
        sign_with_actual_helper(target,base,root,art,args.run_id,"200")
        pv=load("r8_profile_pv",target/"scripts/provenance.py")
        assert pv.verify_unit(art,args.run_id)[0] is True
        log_before=log.read_text(encoding="utf-8")
        summary=json.loads(next(s[8:] for s in log_before.splitlines() if s.startswith("SUMMARY ")))
        rows=list(csv.DictReader(art.open(encoding="utf-8")))
        assert rows and all(r["ref_inputs_sha"]==summary["ref_inputs_sha"] for r in rows)
        assert summary["consumed_inputs"] and summary["ref_consumed_inputs"]
        original_csv=art.read_bytes(); meta=Path(str(art)+".meta.json"); original_meta=meta.read_bytes()
        assert "consumed_inputs" not in rows[0] and "consumed_inputs" not in json.loads(original_meta)
        # Invoke the current production run() helper; normal profile failure from
        # unavailable input directory occurs after shell truncates this same log.
        shell=(target/"scripts/run_states.sh").read_text(encoding="utf-8")
        code=shell[shell.index("\nsay ()")+1:shell.index("\nfail=0")]
        code+='\nrun "profile 200" "$1" - "$2" "$3" -m bms_balancing.verify profile --data-root "$4" --source GITT --state 200 --si-source Li --starts 2 --grid 3 --out "$1"\n'
        env=dict(os.environ,PATH=str(Path(sys.executable).parent)+os.pathsep+os.environ.get("PATH",""),
                 PYTHONPATH=str(target)+os.pathsep+os.environ.get("PYTHONPATH",""))
        p=subprocess.run(["bash","-c",code,"r8",str(art),str(log),sys.executable,str(base/"input-export-not-mounted")],
                         cwd=base,env=env,capture_output=True,text=True,timeout=45)
        assert p.returncode!=0 and art.read_bytes()==original_csv and meta.read_bytes()==original_meta
        assert "SUMMARY " not in log.read_text(encoding="utf-8")
        ok,why=pv.verify_unit(art,args.run_id)
        assert ok is True
        return {"real_optimizer":True,"profile_rows":len(rows),"summary_had_both_input_identities":True,
                "profile_rows_contain_only_aggregate_target_ref_hashes":True,"retry_rc":p.returncode,
                "old_csv_and_meta_unchanged":True,"old_unit_after_retry":[ok,why],
                "old_identity_summary_remaining":False,"retry_log":log.read_text(encoding="utf-8"),
                "retry_stderr":p.stderr}


def shape_old_fit_new_literature(target, fx, ex):
    import numpy as np
    import pandas as pd
    from bms_balancing import verify as v
    ns=load("r8_shape",target/"scripts/ne_shape.py")
    with tempfile.TemporaryDirectory(prefix="bms-r8-shape-") as td:
        base=Path(td); ex.fixture(target,base); root=base/"inputs"; fx.generate(target,root)
        for state in ["100","200","300_0009","300_0147"]:
            art=base/f"out/matrix_{state}.csv"; a=fx.args_for(root,art); a.state=state; a.run_id=f"r8-fit-{state}"
            with patch.object(v.D,"SI_SOURCES",["Li"]),contextlib.redirect_stdout(io.StringIO()):
                v.cmd_matrix(a)
            sign_with_actual_helper(target,base,root,art,a.run_id,state)
        selected=list(csv.DictReader((base/"out/matrix_200.csv").open(encoding="utf-8")))[0]
        matrix_consumed=json.loads(selected["consumed_inputs"])
        def run():
            buf=io.StringIO()
            with patch.object(sys,"argv",["ne_shape.py","--data-root",str(root),"--out-dir",str(base/"out"),"--write",str(base/"out")]),contextlib.redirect_stdout(buf):
                rc=ns.main()
            art=base/"out/ne_shape_GITT_Li.csv"
            rows={r["state"]:r for r in csv.DictReader(art.open(encoding="utf-8"))}
            meta=json.loads(Path(str(art)+".meta.json").read_text(encoding="utf-8"))
            return rc,rows,meta,buf.getvalue()
        rc_A,A,meta_A,_=run()
        gr_path=root/"data/literature/Si_Gr_literature_OCP.xlsx"
        f=pd.read_excel(gr_path)
        q=f["Gr_capacity"].to_numpy(float); q=q/np.nanmax(q)
        f["Gr_voltage"]=f["Gr_voltage"]+.040*q*q
        nextpath=gr_path.with_name("export.next.xlsx"); f.to_excel(nextpath,index=False); os.replace(nextpath,gr_path)
        rc_B,B,meta_B,text_B=run()
        assert rc_A==rc_B==0
        assert meta_A["consumed_inputs"]["200"]["matrix"]==meta_B["consumed_inputs"]["200"]["matrix"]
        assert meta_B["consumed_inputs"]["literature"]["gr"]["sha256"]!=matrix_consumed["literature"]["gr"]["sha256"]
        changed={k:[A["200"][k],B["200"][k]] for k in A["200"] if A["200"][k]!=B["200"][k] and k!="run_id"}
        assert changed
        return {"real_matrix_optimizer":True,"ne_shape_refits":False,"rc_A":rc_A,"rc_B":rc_B,
                "same_matrix_gamma_pair":[selected["gamma_Si"],selected["ref_gamma_Si"]],
                "matrix_input_literature_gr_sha":matrix_consumed["literature"]["gr"]["sha256"],
                "current_shape_gr_sha":meta_B["consumed_inputs"]["literature"]["gr"]["sha256"],
                "both_direct_inputs_recorded_but_no_fit_export_consistency_check":True,
                "state200_changes":changed,"stdout_after_reexport":text_B}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--target",type=Path,default=Path(__file__).resolve().parents[1]/"work/harness-r8-target-wsl/bms-balancing")
    p.add_argument("--case",choices=["noise","matrix","profile","shape","closures","all"],default="all")
    a=p.parse_args(); a.target=a.target.resolve(); sys.path.insert(0,str(a.target))
    pkg=a.target/"reviews/r7_repros/codex"
    fx=load("r8_r7_fixture",pkg/"harness_r7_claims_repros.py")
    ex=load("r8_r7_execution_fixture",pkg/"harness_r7_execution_repros.py")
    results={}
    if a.case in ("noise","all"): results["noise_closure"]=noise_closed(a.target,fx)
    if a.case in ("matrix","all"): results["reference_closure"]=reference_closed(a.target,fx)
    if a.case in ("profile","all"): results["profile_identity_log_loss"]=profile_identity_log_loss(a.target,fx,ex)
    if a.case in ("shape","all"): results["shape_fit_export_policy"]=shape_old_fit_new_literature(a.target,fx,ex)
    if a.case in ("closures","all"):
        results["build_closures"]=fx.build_snapshot_closures(a.target)
        results["shape_same_bytes_closure"]=fx.shape_multiple_consumers(a.target)
    print(json.dumps(results,ensure_ascii=False,indent=2))


if __name__=="__main__": main()

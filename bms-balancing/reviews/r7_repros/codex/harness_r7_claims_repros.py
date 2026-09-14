"""R7 scientific input-snapshot and reference-provenance checks.

Actual loaders/Objectives and, for command-level cases, real local optimizers.
Only generated synthetic workbooks under TemporaryDirectory are changed.
"""
from __future__ import annotations
import argparse
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(target,root):
    subprocess.run([sys.executable,str(target/"matlab/tests/gen_synth_xlsx.py"),str(root)],
                   check=True,capture_output=True,text=True)


def rewrite_xlsx(path,kind,state="200",noise=0.):
    import numpy as np
    import pandas as pd
    if kind=="full":
        frame=pd.read_excel(path,header=None)
        col=2*["pristine","100","200","300_0009","300_0147"].index(state)+1
        val=pd.to_numeric(frame.iloc[2:,col],errors="coerce").to_numpy(float)
        if noise:
            val=val+noise*np.random.default_rng(731).normal(size=val.size)
        else:
            val=val+.020
        frame.iloc[2:,col]=val
        options={"header":False,"index":False}
    else:
        frame=pd.read_excel(path)
        frame["PE_voltage"]+=.020
        if kind=="half_and_capacity":
            frame["NE_capacity"]*=.8
        options={"index":False}
    temp=path.with_name(path.stem+".next.xlsx")
    frame.to_excel(temp,**options)
    os.replace(temp,path)


@contextlib.contextmanager
def cwd(path):
    old=Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def args_for(root,out=None):
    return SimpleNamespace(data_root=str(root),source="GITT",state="200",si_source="Li",w_dqdv=0.,
                           starts=2,seed=0,only_source=True,only_wdqdv=True,out=str(out) if out else None,
                           run_id="r7-synthetic-own-attempt",grid=3,tol=.01,profile_scale="global")


def build_snapshot_closures(target):
    import numpy as np
    import pandas as pd
    from bms_balancing import verify as v
    results=[]
    for kind in ["full","half","si","gr"]:
        with tempfile.TemporaryDirectory(prefix="bms-r7-snapshot-") as temp:
            root=Path(temp)
            generate(target,root)
            paths={"full":v.D.full_cell_workbook(root),"half":root/"data/half_cell/GITT/200.xlsx",
                   "si":root/"data/literature/Si_OCP_sources/Li.csv","gr":root/"data/literature/Si_Gr_literature_OCP.xlsx"}
            path=paths[kind]
            before=digest(path)
            original=v.build(root,"GITT","200","Li",scale_seed=0)
            real_read=v.D.read_input
            count=0
            def snapshot_then_export(p):
                nonlocal count
                snap=real_read(p)
                if Path(p)==path:
                    count+=1
                    if count==1:
                        if kind in ("full","half"):
                            rewrite_xlsx(path,kind)
                        elif kind=="si":
                            f=pd.read_csv(path); f["voltage"]+=.01
                            new=path.with_name(path.name+".next"); f.to_csv(new,index=False); os.replace(new,path)
                        else:
                            f=pd.read_excel(path); f["Gr_voltage"]+=.01
                            new=path.with_name(path.stem+".next.xlsx"); f.to_excel(new,index=False); os.replace(new,path)
                return snap
            with patch.object(v.D,"read_input",side_effect=snapshot_then_export):
                raced=v.build(root,"GITT","200","Li",scale_seed=0)
            normal_B=v.build(root,"GITT","200","Li",scale_seed=0)
            assert count==1
            assert raced.inputs_sha==original.inputs_sha!=normal_B.inputs_sha
            assert raced.consumed_inputs==original.consumed_inputs
            p=np.asarray(v.DD_EVAL_P)
            rm_A=np.array([original.rmse_pocv(q) for q in p])
            rm_r=np.array([raced.rmse_pocv(q) for q in p])
            rm_B=np.array([normal_B.rmse_pocv(q) for q in p])
            assert np.array_equal(rm_A,rm_r)
            results.append({"input":kind,"pathname_read_count":count,"raced_hash_is_A":True,
                            "raced_arrays_match_A":True,"B_hash_changed":before!=digest(path),
                            "B_max_rmse_difference_V":float(np.max(abs(rm_A-rm_B)))})
    return results


def shape_multiple_consumers(target):
    ns=load("r7_shape",target/"scripts/ne_shape.py")
    with tempfile.TemporaryDirectory(prefix="bms-r7-shape-") as temp:
        base=Path(temp); root=base/"inputs"
        generate(target,root)
        (base/"out").mkdir()
        for state in ["100","200","300_0009","300_0147"]:
            # Explicit legacy diagnostic input fixture, not a modern unsigned unit.
            (base/f"out/matrix_{state}.csv").write_text(
                "half_cell,si,w_dqdv,gamma_Si,ref_gamma_Si\nGITT,Li,0,0.16,0.15\n",encoding="utf-8")
        def run():
            with cwd(base),patch.object(sys,"argv",["ne_shape.py","--data-root",str(root)]),contextlib.redirect_stdout(io.StringIO()):
                assert ns.main()==0
            art=base/"out/ne_shape_GITT_Li.csv"
            rows={r["state"]:r for r in csv.DictReader(art.open(encoding="utf-8"))}
            meta=json.loads(art.with_name(art.name+".meta.json").read_text(encoding="utf-8"))
            return rows,meta
        original,meta_A=run()
        path=root/"data/half_cell/GITT/200.xlsx"
        real_read=ns.D.read_input
        count=0
        def snapshot_then_export(p):
            nonlocal count
            snap=real_read(p)
            if Path(p)==path:
                count+=1
                if count==1:
                    rewrite_xlsx(path,"half_and_capacity")
            return snap
        with patch.object(ns.D,"read_input",side_effect=snapshot_then_export):
            raced,meta_r=run()
        normal_B,meta_B=run()
        assert count==1
        fields=["cap_delta_pct","pe_shape_max_mV","measured_shape_mV"]
        assert all(original["200"][f]==raced["200"][f] for f in fields)
        assert meta_A["consumed_inputs"]["200"]["half_cell"]==meta_r["consumed_inputs"]["200"]["half_cell"]
        assert meta_r["consumed_inputs"]["200"]["half_cell"]!=meta_B["consumed_inputs"]["200"]["half_cell"]
        return {"read_count":count,"same_bytes_for_half_capacity_identity":True,
                "A":{k:original["200"][k] for k in fields},"raced":{k:raced["200"][k] for k in fields},
                "normal_B":{k:normal_B["200"][k] for k in fields}}


def matrix_reference_omission(target):
    from bms_balancing import verify as v
    with tempfile.TemporaryDirectory(prefix="bms-r7-ref-") as temp:
        base=Path(temp); root=base/"inputs"
        generate(target,root)
        observed=[]
        real_build=v.build
        def capture_build(*args,**kwargs):
            obj=real_build(*args,**kwargs)
            observed.append({"state":args[2],"inputs_sha":obj.inputs_sha,"consumed":obj.consumed_inputs})
            return obj
        def run(name):
            out=base/f"{name}.csv"
            with patch.object(v.D,"SI_SOURCES",["Li"]),patch.object(v,"build",side_effect=capture_build),contextlib.redirect_stdout(io.StringIO()):
                v.cmd_matrix(args_for(root,out))
            rows=list(csv.DictReader(out.open(encoding="utf-8")))
            assert len(rows)==1 and not rows[0].get("error"),rows
            return rows[0]
        A=run("A")
        pristine=root/"data/half_cell/GITT/pristine.xlsx"
        rewrite_xlsx(pristine,"half",state="pristine")
        B=run("B")
        assert A["inputs_sha"]==B["inputs_sha"]
        refs=[r for r in observed if r["state"]=="pristine"]
        assert refs[0]["inputs_sha"]!=refs[1]["inputs_sha"]
        assert not any("ref" in k and ("inputs" in k or "sha" in k or "consumed" in k) for k in A)
        keys=["inputs_sha","ref_a_PE","ref_b_PE","ref_a_NE","ref_b_NE","ref_gamma_Si","ref_rmse_pocv","LAM_PE_pct","LAM_NE_pct","LLI_pct"]
        assert any(A[k]!=B[k] for k in keys if k!="inputs_sha")
        return {"real_optimizer":True,"restricted_fixture":"one GITT/Li/w=0 combination; starts=2",
                "A":{k:A[k] for k in keys},"B":{k:B[k] for k in keys},
                "observed_reference_inputs_sha_A":refs[0]["inputs_sha"],"observed_reference_inputs_sha_B":refs[1]["inputs_sha"],
                "reference_input_signature_in_csv":False}


def noise_reopen(target):
    from bms_balancing import verify as v
    with tempfile.TemporaryDirectory(prefix="bms-r7-noise-") as temp:
        root=Path(temp)
        generate(target,root)
        real_build=v.build
        wb=v.D.full_cell_workbook(root)
        def run():
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                v.cmd_noise(args_for(root))
            return json.loads(out.getvalue())
        A=run()
        selected=[]
        def build_then_export(*args,**kwargs):
            obj=real_build(*args,**kwargs)
            selected.append(obj.consumed_inputs["full_cell"])
            rewrite_xlsx(wb,"full",noise=.020)
            return obj
        with patch.object(v,"build",side_effect=build_then_export):
            mixed=run()
        normal_B=run()
        assert A["misfit_rmse_pocv_V"]==mixed["misfit_rmse_pocv_V"]
        assert A["sigma_at_k1_V"]!=mixed["sigma_at_k1_V"]
        assert normal_B["sigma_at_k1_V"]==mixed["sigma_at_k1_V"]
        assert normal_B["misfit_rmse_pocv_V"]!=mixed["misfit_rmse_pocv_V"]
        assert selected[0]["sha256"]!=digest(wb)
        keys=["misfit_rmse_pocv_V","sigma_meas_from_raw_V","sigma_at_k1_V","misfit_over_sigma_if_raw_data","verdict"]
        return {"real_optimizer":True,"inputs_at_build":selected[0],"raw_reopened_hash_B":digest(wb),
                "A":{k:A[k] for k in keys},"mixed_A_misfit_B_noise":{k:mixed[k] for k in keys},
                "normal_B":{k:normal_B[k] for k in keys}}


def matrix_shared_workbook_schedule(target):
    """An ordinary workbook export between pristine and target builds."""
    from bms_balancing import verify as v
    with tempfile.TemporaryDirectory(prefix="bms-r7-shared-") as temp:
        base=Path(temp); root=base/"inputs"
        generate(target,root)
        wb=v.D.full_cell_workbook(root)
        real_build=v.build
        def run(name,export_after_reference=False):
            observed=[]
            def actual_build(*args,**kwargs):
                obj=real_build(*args,**kwargs)
                observed.append({"state":args[2],"inputs_sha":obj.inputs_sha})
                if args[2]=="pristine" and export_after_reference:
                    rewrite_xlsx(wb,"full",state="pristine")
                return obj
            out=base/f"{name}.csv"
            with patch.object(v.D,"SI_SOURCES",["Li"]),patch.object(v,"build",side_effect=actual_build),contextlib.redirect_stdout(io.StringIO()):
                v.cmd_matrix(args_for(root,out))
            rows=list(csv.DictReader(out.open(encoding="utf-8")))
            assert len(rows)==1 and not rows[0].get("error"),rows
            return rows[0],observed
        A,obs_A=run("A")
        mixed,obs_m=run("mixed",True)
        B,obs_B=run("B")
        assert A["inputs_sha"]!=mixed["inputs_sha"]==B["inputs_sha"]
        assert obs_A[0]["inputs_sha"]==obs_m[0]["inputs_sha"]!=obs_B[0]["inputs_sha"]
        assert A["ref_a_NE"]==mixed["ref_a_NE"]!=B["ref_a_NE"]
        assert mixed["a_NE"]==B["a_NE"]
        assert A["LAM_NE_pct"]==mixed["LAM_NE_pct"]!=B["LAM_NE_pct"]
        fields=["inputs_sha","a_NE","ref_a_NE","ref_rmse_pocv","LAM_NE_pct"]
        return {"real_optimizer":True,"normal_reexport":"pristine voltage +20mV in shared fullcell workbook",
                "A_A":{k:A[k] for k in fields},"reference_A_target_B":{k:mixed[k] for k in fields},
                "B_B":{k:B[k] for k in fields},"captured_actual_build_inputs":{"A":obs_A,"mixed":obs_m,"B":obs_B},
                "same_published_target_signature_different_reference_bytes_and_LAM":True}


def path_and_premise(target):
    pv=load("r7_pv",target/"scripts/provenance.py")
    with tempfile.TemporaryDirectory(prefix="bms-r7-path-") as temp:
        root=Path(temp); (root/"out").mkdir()
        def git(*a):
            subprocess.run(["git",*a],cwd=root,check=True,capture_output=True,text=True)
        git("init","-q"); git("config","user.name","fixture"); git("config","user.email","fixture@example.invalid")
        names=["out/측정.csv","out/a -> b.csv"]
        for n in names:
            (root/n).write_text("x\n1\n",encoding="utf-8")
        git("add",*names); git("commit","-qm","outputs")
        for n in names:
            (root/n).write_text("x\n2\n",encoding="utf-8")
        result=pv.git_provenance(cwd=root)
        assert result["git_dirty"] is False and result["git_modified_code"]==[]
        assert result["git_modified_outputs"]==sorted(names)
    shell=(target/"scripts/run_states.sh").read_text(encoding="utf-8")
    assert "inputs_sha" not in shell and "LAST_PRE_PV" in shell
    return {"R6_05_closed":True,"correct_modified_outputs":result["git_modified_outputs"],
            "run_states_inputs_sha_occurrences":0,"preflight_is_git_provenance_not_input_hash":True}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--target",type=Path,default=Path(__file__).resolve().parents[1]/"work/harness-r7-target/bms-balancing")
    p.add_argument("--case",choices=["closures","matrix","noise","all"],default="all")
    args=p.parse_args()
    sys.path.insert(0,str(args.target))
    result={}
    if args.case in ("closures","all"):
        result["build_snapshots"]=build_snapshot_closures(args.target)
        result["shape_consumers"]=shape_multiple_consumers(args.target)
        result["paths_and_Q2"]=path_and_premise(args.target)
    if args.case in ("matrix","all"):
        result["matrix_reference"]=matrix_reference_omission(args.target)
        result["matrix_shared_workbook"]=matrix_shared_workbook_schedule(args.target)
    if args.case in ("noise","all"):
        result["noise_reopen"]=noise_reopen(args.target)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()

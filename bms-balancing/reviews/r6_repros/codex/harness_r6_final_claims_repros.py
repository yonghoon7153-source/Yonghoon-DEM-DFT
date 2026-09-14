"""d431404-only review fixtures: actual consumed arrays versus input signature.

All files written are synthetic and live in TemporaryDirectory. Real model and
loaders run; no optimizer, target code edits, or private battery data are used.
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
from unittest.mock import patch


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@contextlib.contextmanager
def cwd(path):
    old=Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def git(root,*args):
    return subprocess.run(["git",*args],cwd=root,capture_output=True,text=True,check=True).stdout.strip()


def matrix(path,gamma):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+".new")
    with temporary.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f,lineterminator="\n")
        w.writerow(["half_cell","si","w_dqdv","gamma_Si","ref_gamma_Si","run_id"])
        w.writerow(["GITT","Li",0,gamma,.15,"synthetic-matrix"])
    os.replace(temporary,path)


def write_half(path,blend,gamma,pe_offset=0.):
    import numpy as np
    import pandas as pd
    u=np.linspace(0,1,301)
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.stem+".new.xlsx")
    pd.DataFrame({"PE_capacity":u,"PE_voltage":4.2-.7*u+pe_offset,
                  "NE_capacity":u,"NE_voltage":blend.E(u,gamma)}).to_excel(temporary,index=False)
    os.replace(temporary,path)


def shape_inputs(base):
    import numpy as np
    import pandas as pd
    from bms_balancing.model import Blend
    u=np.linspace(0,1,301)
    arrays=((1-u)**2,.1+.7*u,1-u,.1+.7*u)
    b=Blend(*arrays,window=11,poly_order=3)
    data=base/"data-root"
    lit=data/"data/literature"
    (lit/"Si_OCP_sources").mkdir(parents=True)
    pd.DataFrame({"normalizedCapacity":arrays[0],"voltage":arrays[1]}).to_csv(lit/"Si_OCP_sources/Li.csv",index=False)
    pd.DataFrame({"Gr_capacity":arrays[2],"Gr_voltage":arrays[3]}).to_excel(lit/"Si_Gr_literature_OCP.xlsx",index=False)
    for state,gamma in [("pristine",.15),("100",.45)]:
        write_half(data/f"data/half_cell/GITT/{state}.xlsx",b,gamma)
    matrix(base/"out/matrix_100.csv",.16)
    return data,b


def run_shape(ns,base,data):
    buf=io.StringIO()
    with cwd(base),patch.object(sys,"argv",["ne_shape.py","--data-root",str(data),"--write","out"]),contextlib.redirect_stdout(buf):
        assert ns.main()==0
    path=base/"out/ne_shape_GITT_Li.csv"
    with path.open(encoding="utf-8") as f:
        row=next(csv.DictReader(f))
    meta=json.loads(path.with_name(path.name+".meta.json").read_text(encoding="utf-8"))
    return row,meta


def shape_and_matrix(target):
    ns=load("r6_final_ne_shape",target/"scripts/ne_shape.py")
    with tempfile.TemporaryDirectory(prefix="bms-r6-final-shape-") as temp:
        base=Path(temp)
        data,blend=shape_inputs(base)
        selected=base/"out/matrix_100.csv"
        first,first_meta=run_shape(ns,base,data)
        matrix(base/"out/matrix_100_v2.csv",.45)
        second,second_meta=run_shape(ns,base,data)
        a=first_meta["consumed_inputs"]["100"]["matrix"]
        b=second_meta["consumed_inputs"]["100"]["matrix"]
        assert a["file"]!=b["file"] and a["sha256"]!=b["sha256"]
        (base/"out/matrix_100_v2.csv").unlink()

        # Internal F03 closure: after A's bytes have reached DictReader, a new
        # export B can replace the path, but hash and gamma must BOTH stay A.
        before=sha(selected)
        reader=ns.csv.DictReader
        replaced=[]
        def replace_after_snapshot(fh,*args,**kwargs):
            result=reader(fh,*args,**kwargs)
            if isinstance(fh,io.StringIO) and not replaced:
                matrix(selected,.45)
                replaced.append(True)
            return result
        with patch.object(ns.csv,"DictReader",side_effect=replace_after_snapshot):
            pair=ns.fitted_pair_info(base/"out","100","GITT","Li")
        assert replaced and pair["gamma_target"]==.16 and pair["sha256"]==before
        assert sha(selected)!=before

        # Fresh final-commit retest: actual workbook arrays are loaded first,
        # but workbook identity is still acquired later from the pathname.
        half=data/"data/half_cell/GITT/100.xlsx"
        half_A=sha(half)
        real_load=ns.D.load_literature
        def finish_new_half_export(root,source):
            arrays=real_load(root,source)
            write_half(half,blend,.45,pe_offset=.02)
            return arrays
        with patch.object(ns.D,"load_literature",side_effect=finish_new_half_export):
            raced,raced_meta=run_shape(ns,base,data)
        normal_B,meta_B=run_shape(ns,base,data)
        recorded=raced_meta["consumed_inputs"]["100"]["half_cell"]
        assert recorded["sha256"]==sha(half)!=half_A
        assert recorded==meta_B["consumed_inputs"]["100"]["half_cell"]
        assert float(raced["pe_shape_max_mV"])==0. and float(normal_B["pe_shape_max_mV"])==20.
        return {"R5_static_v2_recording_closed":{"gamma_before":first["gamma_target"],"gamma_after":second["gamma_target"],
                    "before_input":a,"after_input":b},
                "internal_F03_matrix_read_hash_closed":{"consumed_gamma":pair["gamma_target"],"hash_matches_consumed_A":True,"path_now_B":True},
                "half_cell_late_identity":{"output_A_PE_change_mV":raced["pe_shape_max_mV"],
                    "output_for_recorded_B_PE_change_mV":normal_B["pe_shape_max_mV"],"same_recorded_half_identity":True,
                    "A_hash":half_A,"recorded_B":recorded},
                "full_cell_directory_not_needed_by_shape":not (data/"data/full_cell").exists()}


def fullcell_build_signature(target):
    import numpy as np
    import pandas as pd
    from bms_balancing import verify
    with tempfile.TemporaryDirectory(prefix="bms-r6-final-build-") as temp:
        data=Path(temp)
        subprocess.run([sys.executable,str(target/"matlab/tests/gen_synth_xlsx.py"),str(data)],check=True,capture_output=True,text=True)
        original=verify.build(data,"GITT","200","Li",w_dqdv=1.,scale_seed=0)
        workbook=verify.D.full_cell_workbook(data)
        A_hash=sha(workbook)
        real_load=verify.D.load_full_cell
        def finish_new_fullcell_export(root,state,workbook=None):
            arrays=real_load(root,state,workbook=workbook)
            frame=pd.read_excel(workbook,header=None)
            col=2*verify.D.FULL_COL[state]+1
            frame.iloc[2:,col]=pd.to_numeric(frame.iloc[2:,col],errors="coerce")+.020
            temporary=workbook.with_name(workbook.stem+".new.xlsx")
            frame.to_excel(temporary,header=False,index=False)
            os.replace(temporary,workbook)
            return arrays
        with patch.object(verify.D,"load_full_cell",side_effect=finish_new_fullcell_export):
            raced=verify.build(data,"GITT","200","Li",w_dqdv=1.,scale_seed=0)
        normal_B=verify.build(data,"GITT","200","Li",w_dqdv=1.,scale_seed=0)
        assert np.array_equal(raced.voltage,original.voltage)
        assert raced.inputs_sha==normal_B.inputs_sha!=original.inputs_sha
        assert raced.consumed_inputs==normal_B.consumed_inputs
        assert raced.consumed_inputs["full_cell"]["sha256"]==sha(workbook)!=A_hash
        voltage_delta=float(np.max(abs(raced.voltage-normal_B.voltage)))
        assert abs(voltage_delta-.02)<1e-12
        p=np.asarray(verify.DD_EVAL_P)
        a=np.array([raced.rmse_pocv(q) for q in p])
        b=np.array([normal_B.rmse_pocv(q) for q in p])
        delta=float(np.max(abs(a-b)))
        assert delta>1e-6
        return {"actual_build_and_Objective":True,"optimizer_not_run":True,
                "same_inputs_sha_for_different_consumed_arrays":raced.inputs_sha,
                "same_consumed_input_records":True,"recorded_full_cell":raced.consumed_inputs["full_cell"],
                "full_cell_consumed_voltage_difference_V":voltage_delta,
                "max_rmse_pocv_difference_over_8_points_V":delta,
                "raced_arrays_match_original_A_exactly":True}


def role_checks(target):
    pv=load("r6_final_roles",target/"scripts/provenance.py")
    with tempfile.TemporaryDirectory(prefix="bms-r6-final-paths-") as temp:
        root=Path(temp)
        (root/"out").mkdir()
        git(root,"init","-q")
        git(root,"config","user.name","R6 fixture")
        git(root,"config","user.email","fixture@example.invalid")
        git(root,"config","core.quotePath","true")
        names=["out/측정.csv","out/a -> b.csv"]
        for name in names:
            (root/name).write_text("value\n1\n",encoding="utf-8")
        git(root,"add",*names)
        git(root,"commit","-qm","named outputs")
        (root/names[0]).write_text("value\n2\n",encoding="utf-8")
        fixed=pv.git_provenance(cwd=root)
        assert fixed["git_dirty"] is False and fixed["git_modified_outputs"]==[names[0]]
        (root/names[1]).write_text("value\n2\n",encoding="utf-8")
        bad=pv.git_provenance(cwd=root)
        assert bad["git_dirty"] is True and bad["git_modified_code"]==["b.csv"]
        return {"R5_unicode_path_closed":True,"actual_additional_changed_output":names[1],"reported":bad}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--target",type=Path,default=Path(__file__).resolve().parents[1]/"work/harness-r6-d431404/bms-balancing")
    a=ap.parse_args()
    sys.path.insert(0,str(a.target))
    result={"target":git(a.target,"rev-parse","HEAD"),"shape":shape_and_matrix(a.target),
            "build_input_signature":fullcell_build_signature(a.target),"path_roles":role_checks(a.target)}
    assert result["target"]=="d4314048c63605fb4613f8b0a91859271fddda98"
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()

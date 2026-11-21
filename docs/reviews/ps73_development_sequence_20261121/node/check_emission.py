"""Exercise the sealed ordinary shell on its own *synthetic* runner fixture."""
import hashlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(payload):
    node=load("node",Path(__file__).with_name("ps73_node.py"))
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        kit=root/"source"
        with zipfile.ZipFile(payload) as z:
            raw=z.read("fixed_kit_9fd6aa9d3bee.zip")
        assert hashlib.sha256(raw).hexdigest()=="d8074dfd86d227d80bc3188fa8817a7af7b22b333caa3c22292ce62b10650920"
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            z.extractall(kit)
        mock=load("historical_mock",kit/"ul_runner_test.py")
        # Its setup normally takes an R8 text fixture from the full repository.
        # In these ordinary jobs only the presence of the synthetic last deck
        # is checked. Stand in for that fixture without reading research files.
        mock.ul_lib.r8_text=lambda params: "fake writer deck, ordinary-arm shell fixture only\n"
        synthetic_kit,work,unused=mock._setup(str(root/"synthetic"),beds=[node.BED])
        work=Path(work)
        assert (Path(synthetic_kit)/"run_unload.sh").read_bytes()==(kit/"run_unload.sh").read_bytes()
        bed=work/node.BED
        (bed/"RJ").mkdir()
        # Synthetic predecessor for the ordinary shell. The independent check in
        # verify_source.py exercises the genuine 368315 receipt. No fake job can pass the field worker.
        (bed/"RJ"/"restore_verdict.json").write_text('{"status":"RESTORED"}')
        (bed/"RJ"/"run_manifest.txt").write_text("grammar_prereq=PASS\nend=X fails=0 reader_rc=0\n")
        (bed/"ul_base.in").write_text("variable ul_S2max equal 1\n")
        for i,arm in enumerate(("UB","UT","UC")):
            job=str(810000+i)
            extra=dict(SLURM_JOB_ID=job,SLURM_NTASKS="6",SLURM_JOB_NODELIST="mocknode")
            rc,log=mock._run(str(root/"synthetic"),synthetic_kit,node.BED,arm,extra)
            if rc:
                raise ValueError("sealed fixture runner refused "+arm+": "+log[-1500:])
            r=node.outcome(work,arm,job)
            assert r["technical_ok"] and r["runner_rc"]==0
            print(arm+" EXACT_ORDINARY_SHELL_RECEIPT_PASS")
    print("ENGINE_CALLS=0 REAL_SUBMISSIONS=0")


if __name__=="__main__":
    main(sys.argv[1])

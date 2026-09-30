# 트리 밖 탐침 — 패치 전 코드에서 "새 API 없음" 이 아니라 **실제 결함** 을 잰다 (커밋하지 않음)
import sys, tempfile, shutil
from pathlib import Path
sys.path.insert(0,'.'); sys.path.insert(0,'tests')
import test_gate81_stage3_wire as G81
from test_fitting import _tiny_curves, _obj_cfg_min, _BOUNDS_MIN
from src import fitting as F
from tools import preserve as PV
tmp = Path(tempfile.mkdtemp(prefix="g84probe-", dir=str(Path("results/_smoke/_unit").resolve())))
def plan(ctx, **over):
    p = ctx["planned"]; return {**ctx, "planned": PV.PlannedLegV4(**{**p.__dict__, **over})}
def run(name, ctx, in_dir):
    out = tmp / name
    try:
        F.run_fit(in_dir, out, _obj_cfg_min(), G81._OBJ_W, _BOUNDS_MIN, "expanded", 2, nproc=1, adaptive=False, warm_start=False, stage3=ctx)
        return f"STARTED_AND_FINISHED fits={ (out/'fits.parquet').exists() }"
    except Exception as e:
        return f"{type(e).__name__}: {str(e)[:90]}"
in_dir = _tiny_curves(tmp / "in")
base = G81._v6_context(in_dir)
inp = base["planned"].inputs
print("[n1_02 padded hex64]   ", run("a", plan(base, inputs={**inp, "base_config_digest": F._config_closure_digest("configs/base.yaml") + "0"*48}), in_dir))
print("[n1_03 foreign hex64]  ", run("b", plan(base, inputs={**inp, "base_config_digest": "f"*64}), in_dir))
print("[n3_00 other source]   ", run("c", plan(base, source_digest="deadbeefcafe0001"), in_dir))
print("[n3_02 plan ref=halfcell]", run("d", plan(base, inputs={**inp, "reference": "halfcell"}), in_dir))
print("[n1_01 null digest]    ", run("e", base, in_dir))
shutil.rmtree(tmp, ignore_errors=True)

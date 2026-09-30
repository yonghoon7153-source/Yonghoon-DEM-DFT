# 85차 증거 — 라운드 2a 계획 결속 탐침의 **재현판** (패치 전 · 패치 뒤 두 커밋에서 같은 본문으로 돈다).
#
# `probe_g84_real_reasons.as_run.py` (10:54:35Z, 원 실행 그대로) 와 차이:
#   · null 경우를 fixture 기본값에 기대지 않고 **명시**한다 (패치 뒤 `_v6_context` 는 hex64 를 넣는다).
#   · 진짜 closure hex64 는 패치 뒤 `config_closure_sha256` 로만 얻는다. 패치 전에는 그 함수도 결속도
#     없으므로 n3_00 · n3_02 의 closure 칸은 None (원 실행과 같은 조건) — 결속이 없으면 값과 무관하다.
#   · 양성 대조 [control] (패치 뒤만) — 진짜 closure hex64 로는 끝까지 돈다.
#   · 결과 줄에 예외 이유를 90 자까지 적는다 (원 실행과 같은 형식).
# 실행: degradation-degeneracy/ 루트에서 `python probe_g84_before_after.py` (tests/ 의 fixture 를 import).
#   `git archive` 사본에서 돌릴 때는 PROBE_COMMIT=<sha> 로 커밋을 적는다.
import subprocess, sys, tempfile, shutil
from pathlib import Path
sys.path.insert(0, '.'); sys.path.insert(0, 'tests')
import test_gate81_stage3_wire as G81
from test_fitting import _tiny_curves, _obj_cfg_min, _BOUNDS_MIN
from src import fitting as F
from src.io import source_digest
from tools import preserve as PV

import os
head = os.environ.get("PROBE_COMMIT") or subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print(f"# commit={head} source_digest={source_digest()} has_config_closure_sha256={hasattr(F, 'config_closure_sha256')}")
Path("results/_smoke/_unit").mkdir(parents=True, exist_ok=True)
tmp = Path(tempfile.mkdtemp(prefix="g84probe-", dir=str(Path("results/_smoke/_unit").resolve())))

def plan(ctx, **over):
    p = ctx["planned"]; return {**ctx, "planned": PV.PlannedLegV4(**{**p.__dict__, **over})}

def run(name, ctx, in_dir):
    out = tmp / name
    try:
        F.run_fit(in_dir, out, _obj_cfg_min(), G81._OBJ_W, _BOUNDS_MIN, "expanded", 2, nproc=1,
                  adaptive=False, warm_start=False, stage3=ctx)
        return f"STARTED_AND_FINISHED fits={(out / 'fits.parquet').exists()}"
    except Exception as e:
        return f"REFUSED {type(e).__name__}: {str(e)[:90]}"

in_dir = _tiny_curves(tmp / "in")
base = G81._v6_context(in_dir)
inp = base["planned"].inputs
hex16 = F._config_closure_digest("configs/base.yaml")
real64 = F.config_closure_sha256("configs/base.yaml") if hasattr(F, "config_closure_sha256") else None
print("[n1_01 null digest]       ", run("e", plan(base, inputs={**inp, "base_config_digest": None}), in_dir))
print("[n1_02 padded hex64]      ", run("a", plan(base, inputs={**inp, "base_config_digest": hex16 + "0" * 48}), in_dir))
print("[n1_03 foreign hex64]     ", run("b", plan(base, inputs={**inp, "base_config_digest": "f" * 64}), in_dir))
print("[n3_00 other source]      ", run("c", plan(base, source_digest="deadbeefcafe0001",
                                               inputs={**inp, "base_config_digest": real64}), in_dir))
print("[n3_02 plan ref=halfcell] ", run("d", plan(base, inputs={**inp, "reference": "halfcell",
                                                              "base_config_digest": real64}), in_dir))
if real64 is not None:
    print("[control real hex64]      ", run("f", plan(base, inputs={**inp, "base_config_digest": real64}), in_dir))
else:
    print("[control real hex64]       (패치 전 — config_closure_sha256 없음 · 결속 자체가 없으므로 위 다섯 경우가 곧 대조)")
shutil.rmtree(tmp, ignore_errors=True)

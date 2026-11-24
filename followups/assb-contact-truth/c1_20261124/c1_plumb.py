"""C1 2 차 배관 점검 (P3 선례 — 코드 경로 충돌만 잡는다 · 결과 버림 · 수치를 보지 않는다).

c1_grid · c1_analyze 의 모든 단계를 아주 작은 묶음으로 (펄스 2 · k {4, 8} · 율 하나 · C1b 8 실행) 스크래치에 돌리고,
각 단계의 예외 여부만 출력한다. 단계 함수의 stdout 은 버린다 (수치 미열람). 사용: python -I c1_plumb.py --spk <spike dir> --tmp <scratch dir>
"""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(os.environ["C1_COPY"]).resolve()))
sys.path.insert(0, str(HERE))

import c1_analyze as an  # noqa: E402
import c1_grid as cg  # noqa: E402


def shrink():
    cg.PULSES = cg.PULSES[:2]
    cg.K_RUN = (4, 8)
    cg.WAS = (10.0,)
    cg.RATES = (("C/3", 1 / 3),)
    cg.P_K = [1.0, 2.0 ** (-9 / 4)]
    cg.FA_LV = (1.0, 0.4)
    cg.FK_LV = (1.0, 0.25)
    an.PULSES = an.PULSES[:2]
    an.SHAPES = ("G05",)
    an.WAS = (10.0,)
    an.K_ALL = (0, 4, 8)
    an.REP_K = (4, 8)
    an.M = 2
    an.FA_LV = (1.0, 0.4)
    an.FK_LV = (1.0, 0.25)


def call(name, fn, *a):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = fn(*a)
        print(f"PLUMB {name}: no exception (rc {rc if not isinstance(rc, tuple) else 'tuple'})", flush=True)
        return True
    except Exception:
        print(f"PLUMB {name}: EXCEPTION\n{traceback.format_exc()}", flush=True)
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spk", required=True)
    ap.add_argument("--tmp", required=True)
    a = ap.parse_args()
    shrink()
    out = Path(a.tmp) / "grid"
    csvd = Path(a.tmp) / "csv"
    out.mkdir(parents=True, exist_ok=True)
    G = argparse.Namespace(out=str(out), spk=a.spk, shape="G05", Wa=10.0)
    A = argparse.Namespace(out=str(out), spk=a.spk, csv=str(csvd))
    ok = []
    ok.append(call("conv", cg.conv, G))
    ok.append(call("c1a", cg.c1a, G))
    ok.append(call("failcheck", an.failcheck, A))
    ok.append(call("dc", cg.dc, G))
    ok.append(call("c1b", cg.c1b, G, "off"))
    ok.append(call("ad_c1a", lambda g: cg.c1a(g, arms=("AD",), tag="ad_c1a"), G))
    ok.append(call("ad_dc", lambda g: cg.dc_runs(g, arms=("AD",), tag="ad_dc", include_fresh=False), G))
    ok.append(call("ad_c1b", cg.c1b, G, "on"))
    ok.append(call("analyze_c1a", an.analyze_c1a, A))
    ok.append(call("expectation", an.expectation, A))
    ok.append(call("dc_features", an.dc_features, A))
    ok.append(call("analyze_c1b", an.analyze_c1b, A))
    ok.append(call("analyze_ad", lambda x: an.analyze_c1a(x, arms=("AD", "K"), tag="ad_c1a", do_mc=False), A))
    ok.append(call("analyze_ad_c1b", lambda x: an.analyze_c1b(x, tag="ad_c1b", mode="on"), A))
    import json as _j
    I1 = _j.loads((Path(a.spk) / "s6_registered.json").read_text())["I_1C_A"]
    ok.append(call("ad_dc_z", lambda: cg.dc_z(out, I1, arm_a="AD", tag_a="ad_dc")))
    print("PLUMB ALL OK" if all(ok) else "PLUMB FAILURES")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())

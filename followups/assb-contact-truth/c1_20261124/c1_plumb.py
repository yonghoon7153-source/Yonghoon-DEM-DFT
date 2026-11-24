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


_T0 = __import__("time").time()


def call(name, fn, *a):
    import time as _t
    buf = io.StringIO()
    ts = _t.time() - _T0
    try:
        with contextlib.redirect_stdout(buf):
            rc = fn(*a)
        shown = rc if isinstance(rc, (int, type(None))) else type(rc).__name__     # 6 차: 반환값의 수는 찍지 않는다 (8-12 사후 발견 4)
        print(f"PLUMB {name}: no exception (rc {shown}) · t {ts:.1f}–{_t.time() - _T0:.1f} s", flush=True)
        return True
    except Exception:
        print(f"PLUMB {name}: EXCEPTION · t {ts:.1f}–{_t.time() - _T0:.1f} s\n{traceback.format_exc()}", flush=True)
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
    ok.append(call("heavy_fine_nu160_x80_taf_soc08", heavy160, a.spk))
    print("PLUMB ALL OK" if all(ok) else "PLUMB FAILURES")
    import c1_memguard as mg
    rc_mem = mg.rusage_exit_hook()                       # §8-11 ③ 교차 확인
    if rc_mem is not None:
        return rc_mem
    return 0 if all(ok) else 1


def heavy160(spk):
    """§8-13 ⑤ (8-11 ④ 의 꼴): 판정 짝 정밀판 NU(160) · x 80 · 1e-10 의 Tafel 진폭 펄스 (SOC 0.8 taf± — 5 차 최악 행) × 수렴 묶음 셋
    (Wa 0.1 · G½) — 가벼운 길 · 결과 버림 (최대 RSS 는 감시자가 기록)."""
    import json as _j
    import time as _t
    import c1_truth as tr
    R = _j.loads((Path(spk) / "s6_registered.json").read_text())
    base = tr.base_inputs(shape="G05", Wa=0.1, x_mid=R["x_mid"])
    runs = {"fresh": base, "A_k8": tr.knob_inputs("A", 0.25, base=base), "K_k8": tr.knob_inputs("K", 0.25, base=base)}
    import c1_grid as gr
    m, so, sim = tr.build_model("G05", var_pts=gr.VAR_FINE, rtol=gr.TOL_FINE, atol=gr.TOL_FINE)
    t0 = _t.time()
    for name, d in runs.items():
        for sgn in ("+", "-"):
            r = tr.run_pulse_lean(m, so, sim, d, x_start=R["soc_x"]["0.8"], I_A=R["pulse_I_A"]["taf" + sgn])
            del r
    return {"elapsed_s": _t.time() - t0}


if __name__ == "__main__":
    sys.exit(main())

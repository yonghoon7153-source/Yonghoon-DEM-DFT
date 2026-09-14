"""Python 쪽 `verify eval` 배관 스모크 — 합성 xlsx 로 **돌긴 도는지** 본다.

원자료가 없는 기계에서 확인할 수 있는 것만 확인한다: 적재 경로가 8개 Si
소스 · 2개 반쪽전지 소스 · 5개 상태를 다 통과하는가, 앵커가 유한한가,
CSV 왕복이 값을 보존하는가. **수치의 물리적 의미는 없다.**

fixture 감사 (이 저장소에서 네 번 이상 겪은 패턴):
  합성 문헌곡선 Si·Gr 이 둘 다 전압에 선형이면 Blend 의 min-max 정규화 뒤
  겹쳐서 γ_Si 가 목적함수에 **전혀 닿지 않는다**. 그러면 이 스모크는 블렌드
  경로를 통과한 척만 한다. 그래서 아래 `γ 가 목적함수를 움직이는가` 를
  단언으로 박아 둔다 — 이게 깨지면 코드가 아니라 fixture 를 의심할 것.
"""
from __future__ import annotations
import io, contextlib, pathlib, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
import numpy as np                                                    # noqa: E402
from bms_balancing import data as D                                   # noqa: E402
from bms_balancing.verify import (DD_EVAL_P, build, cmd_eval,         # noqa: E402
                                  dd_eval_anchors, read_dd_eval_csv)


class A:                                        # argparse 대역
    def __init__(self, **kw):
        self.__dict__.update(dict(
            data_root=None, source="GITT", state="pristine", si_source="Li",
            w_dqdv=0.0, seed=0, out=None, compare=None), **kw)


def main():
    root = pathlib.Path(tempfile.mkdtemp(prefix="bmssmoke_"))
    subprocess.run([sys.executable, str(HERE / "gen_synth_xlsx.py"), str(root)],
                   check=True, capture_output=True)
    fails = []

    def chk(name, cond, extra=""):
        print(f"  {'OK  ' if cond else 'FAIL'} {name}{'' if cond else '  ' + extra}")
        if not cond:
            fails.append(name)

    # 1. 5 상태 × 2 반쪽전지 소스 × 8 Si 소스 적재
    for src in D.HALF_FILE:
        for st in D.STATES:
            obj = build(root, src, st, "Li")
            an = dict(dd_eval_anchors(obj))
            ok = all(np.isfinite(v) for v in an.values()) and an["dv_n"] > 50
            chk(f"적재 {src}/{st}", ok, str(an))
    for si in D.SI_SOURCES:
        obj = build(root, "GITT", "pristine", si)
        chk(f"Si 소스 {si}", np.isfinite(obj.rmse_pocv(np.array(DD_EVAL_P[0]))))

    # 2. fixture 감사 — γ_Si 가 목적함수를 실제로 움직이는가
    obj = build(root, "GITT", "pristine", "Li")
    base = np.array([1.10, -0.05, 1.10, -0.01, 0.10])
    vals = []
    for g in (0.05, 0.15, 0.25, 0.35, 0.45):
        p = base.copy(); p[4] = g
        vals.append((obj.rmse_pocv(p), obj.rmse_dvdq(p),
                     obj.rmse_dqdv(p, False), obj.rmse_dqdv(p, True)))
    spread = [max(v[j] for v in vals) - min(v[j] for v in vals) for j in range(4)]
    chk(f"γ 가 rmse_pocv 를 움직인다 (폭 {spread[0]:.3e})", spread[0] > 1e-4)
    chk(f"γ 가 rmse_dvdq 를 움직인다 (폭 {spread[1]:.3e})", spread[1] > 1e-4)
    # dQ/dV 항도 같은 감사를 받는다. 이 항은 보간 범위에 5 점을 못 넣으면
    # 원본 규약대로 **모든 p 에서 1e6** 을 내는데, 그러면 대조는 통과하고
    # 경로는 안 탄다 — 그 상태를 여기서 잡는다 (check_e2e.py 와 같은 취지).
    chk(f"γ 가 rmse_dqdv 를 움직인다 (폭 {spread[2]:.3e})", spread[2] > 1e-4)
    chk("rmse_dqdv 가 1e6 으로 죽지 않는다",
        all(v[2] < 1e6 and v[3] < 1e6 for v in vals), str([v[2] for v in vals]))
    chk("피크 가중이 무가중과 다르다",
        any(abs(v[2] - v[3]) > 1e-12 for v in vals),
        f"n_peaks={len(obj.peak_locs)}")

    # 3. 앵커 이름·순서가 dd_eval.m 과 같은가
    from bms_balancing.verify import ANCHOR_STAGE
    chk("앵커 이름·순서가 ANCHOR_STAGE 와 일치",
        [k for k, _ in dd_eval_anchors(obj)] == [k for k, _ in ANCHOR_STAGE])

    # 4. CSV 왕복 — 쓰고 다시 읽어 값이 보존되는가
    out = root / "rt.csv"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cmd_eval(A(data_root=str(root), out=str(out)))
    an2, rows2, hdr2 = read_dd_eval_csv(out)
    want = dict(dd_eval_anchors(build(root, "GITT", "pristine", "Li")))
    chk(f"CSV 왕복: 앵커 {len(want)}개 보존",
        len(an2) == len(want) and all(abs(an2[k] - want[k]) <= 1e-12 * max(abs(want[k]), 1)
                               for k in want))
    chk("CSV 왕복: 파라미터 8행 보존",
        len(rows2) == len(DD_EVAL_P) and
        all(abs(rows2[i][j] - DD_EVAL_P[i][j]) < 1e-6
            for i in range(len(DD_EVAL_P)) for j in range(5)))

    # 5. 풀셀 워크북 후보가 여럿일 때 이름순 첫 것을 고르는가 (MATLAB dir() 과 맞추기)
    d = root / "data/full_cell/large_cell_033C"
    (d / "aaa_decoy.xlsx").write_bytes((d / "fullcell_states.xlsx").read_bytes())
    chk("워크북 후보 여럿 → 이름순 첫 것", D.full_cell_workbook(root).name == "aaa_decoy.xlsx",
        f"골른 것: {D.full_cell_workbook(root).name}")
    (d / "aaa_decoy.xlsx").unlink()

    print(f"\n{'PASS' if not fails else 'FAIL'} — 실패 {len(fails)}: {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

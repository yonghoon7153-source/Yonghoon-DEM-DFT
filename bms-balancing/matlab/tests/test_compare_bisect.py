"""`verify.py --compare` 의 **이분 판정**이 실제로 갈린 단계를 짚는지 본다.

이 테스트가 필요한 이유: 대조기가 언제나 "일치" 라고만 말하면 없는 것만
못하다. 그래서 **일부러 어긋뜨린 CSV** 를 먹여서 (a) 갈렸음을 알아채는지,
(b) 갈린 단계 이름을 맞게 부르는지를 확인한다.
"""
from __future__ import annotations
import io, pathlib, sys, contextlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from bms_balancing.verify import (ANCHOR_STAGE, DD_EVAL_P, _compare_dd_eval,   # noqa: E402
                                  read_dd_eval_csv)

BASE = {"c_cell": 74.671, "dv_lo": 0.1492985972, "dv_hi": 0.8507014028,
        "dv_n": 350.0, "dq_lo": 3.1064629259, "dq_hi": 4.1435370741,
        "dq_n": 450.0, "n_peaks": 2.0, "w_peak_sum": 855.1713943113,
        "w_peak_max": 7.0, "dq_nuniq_p1": 500.0, "dq_nin_p1": 254.0,
        "E_PE_0p5": 3.5584147098, "E_NE_0p5_0p25": 0.381225,
        "dv_PE_0p5": -0.6573737739, "dv_NE_0p5_0p25": 0.0695302306}
COLS = ["rmse_pocv", "rmse_dvdq", "rmse_dqdv", "rmse_dqdv_w"]
ROWS = [list(q) + [0.78 + 0.001 * i, 0.20 + 0.0001 * i,
                   0.38 + 0.002 * i, 0.29 + 0.0015 * i]
        for i, q in enumerate(DD_EVAL_P)]
PY_P = [r[:5] for r in ROWS]
PY_VALS = {c: [r[5 + j] for r in ROWS] for j, c in enumerate(COLS)}


def write_csv(path, anchors, rows, cols=COLS):
    out = ["# dd_eval  state=pristine  halfcell=data/half_cell/GITT/  Si=Li  w_dqdv=0",
           "# printed_format,%.10f"]                  # 아래 rmse 토큰과 같은 선언 (R4-02: 추정은 complete 가 아니다)
    out += [f"# {k},{v:.17g}" for k, v in anchors.items()]
    out.append("a_PE,b_PE,a_NE,b_NE,gamma_Si," + ",".join(cols))
    out += [",".join([f"{x:.6f}" for x in r[:5]]
                     + [f"{r[5 + j]:.10f}" for j in range(len(cols))])
            for r in rows]
    pathlib.Path(path).write_text("\n".join(out) + "\n")


def run(tmp, anchors_m, rows_m, cols=COLS):
    write_csv(tmp, anchors_m, rows_m, cols)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _compare_dd_eval(dict(BASE), PY_P, PY_VALS, tmp)
    return buf.getvalue()


def main():
    tmp = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/ddc.csv")
    fails = []

    def expect(name, text, must_have, must_not=()):
        bad = [m for m in must_have if m not in text] + [m for m in must_not if m in text]
        print(f"  {'OK  ' if not bad else 'FAIL'} {name}")
        if bad:
            fails.append((name, bad, text))

    # 0) 같은 값 → 일치 판정
    expect("동일 입력 → 일치", run(tmp, BASE, ROWS),
           ["전부 일치"], ["처음 갈린다"])

    # 1) 각 앵커를 하나씩 어긋뜨리면 그 앵커의 단계를 불러야 한다
    for k, stage in ANCHOR_STAGE:
        a = dict(BASE)
        a[k] = a[k] + (1.0 if k == "dv_n" else max(abs(a[k]), 1.0) * 1e-3)
        txt = run(tmp, a, ROWS)
        expect(f"{k} 어긋남 → 「{stage[:24]}…」", txt,
               [f"**{k}** 에서 처음 갈린다" if k != "dv_n" else "dv_n", stage],
               ["전부 일치"])

    # 2) 앵커는 맞고 rmse 만 갈리면 '목적함수 산술' 로 판정해야 한다
    #    — **네 열 각각**에서. 새로 붙인 dQ/dV 두 열이 사실은 안 읽히는데
    #    통과하는 일이 없게 열마다 따로 어긋뜨려 본다.
    for j, c in enumerate(COLS):
        r2 = [list(r) for r in ROWS]
        r2[3][5 + j] *= 1.02
        expect(f"{c} 만 어긋남 → 목적함수 산술", run(tmp, BASE, r2),
               ["앵커는 전부 맞는데 rmse 가 갈린다", "목적함수 산술"], ["전부 일치"])

    # 3) 파라미터 격자가 어긋나면 알아채야 한다
    r3 = [list(r) for r in ROWS]
    r3[2][0] += 0.05
    expect("p 격자 어긋남 감지 → 성공 아님", run(tmp, BASE, r3),
           ["격자가 어긋났다", "성공 아님"], ["전부 일치"])          # Codex R2-01
    expect("행 누락 → 성공 아님", run(tmp, BASE, [list(r) for r in ROWS[:-1]]),
           ["행 수가 다르다", "성공 아님"], ["전부 일치"])          # Codex R2-01

    # 4) 앞머리 없는 옛 산출도 죽지 않아야 한다
    old = pathlib.Path(str(tmp) + ".old")
    old.write_text("a_PE,b_PE,a_NE,b_NE,gamma_Si,rmse_pocv,rmse_dvdq\n" +
                   "\n".join(",".join([f"{x:.6f}" for x in r[:5]] +
                                      [f"{r[5]:.10f}", f"{r[6]:.10f}"]) for r in ROWS) + "\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _compare_dd_eval(dict(BASE), PY_P, PY_VALS, old)
    expect("앵커 없는 옛 CSV 도 처리", buf.getvalue(), ["(없음)"])

    # 4b) **rmse 두 열뿐인 옛 산출**(2026-09-10 이전)도 그대로 대조돼야 한다.
    #     사용자가 이미 만든 4개 CSV(104 값 일치)가 열 추가로 무효가 되면 안 된다.
    txt = run(tmp, BASE, ROWS, cols=["rmse_pocv", "rmse_dvdq"])
    expect("옛 2열 산출 → 있는 열만 대조하고 일치", txt,
           ["전부 일치", "rmse_dqdv", "옛 dd_eval.m 산출이다"], ["처음 갈린다"])

    # 4c) 그때도 **있는 열의 불일치는 놓치지 않아야** 한다
    r4 = [list(r) for r in ROWS]
    r4[1][5] *= 1.02
    expect("옛 2열 산출에서도 불일치는 잡는다",
           run(tmp, BASE, r4, cols=["rmse_pocv", "rmse_dvdq"]),
           ["앵커는 전부 맞는데 rmse 가 갈린다"], ["전부 일치"])

    # 5) BOM 붙은 CSV (MATLAB 이 UTF-8 BOM 을 붙이는 경우)
    bom = pathlib.Path(str(tmp) + ".bom")
    write_csv(bom, BASE, ROWS)
    bom.write_bytes(b"\xef\xbb\xbf" + bom.read_bytes())
    an, rw, hd = read_dd_eval_csv(bom)
    ok = len(an) == len(BASE) and len(rw) == 8 and hd[5:] == COLS
    print(f"  {'OK  ' if ok else 'FAIL'} BOM 붙은 CSV 파싱 "
          f"(앵커 {len(an)}, 행 {len(rw)}, 열 {hd[5:]})")
    if not ok:
        fails.append(("BOM", [f"앵커 {len(BASE)} / 행 8 / 열 {COLS} 이어야 한다"], ""))

    print(f"\n{'PASS' if not fails else 'FAIL'} — {len(fails)} 개 실패")
    for n, b, t in fails:
        print(f"\n--- {n}: 빠졌거나 잘못 나온 것 {b}\n{t}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

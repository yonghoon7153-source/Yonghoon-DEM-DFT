"""원통형 셀(#168 · #171) 자료를 `data.py` 가 기대하는 트리로 옮긴다.

## 왜 변환기인가 — `data.py` 를 고치지 않는다

`bms_balancing/` 은 **검증 대상 코드**다. 새 셀을 붙이려고 그 적재 경로에
분기를 넣으면, 그 뒤로 나오는 모든 숫자가 "우리가 손댄 적재기" 를 지난 값이
된다. 그래서 코드가 아니라 **자료 쪽을 옮긴다.** 변환은 이 파일 하나에
모여 있고, 원본과 산출을 나란히 놓고 감사할 수 있다.

## 사용법

    python3 scripts/prepare_cell.py --src '/mnt/d/…/degradation mode' \\
        --cell '#168' --out ~/dd/cells/c168
    BMS_DATA_ROOT=~/dd/cells/c168 python3 -m bms_balancing.verify eval

## 파우치 셀과 다른 점 — **읽을 때 반드시 알아야 한다**

1. **상태가 4 개다** (pristine · 100 · 200 · 300cyc). `300_0147` 이 없으므로
   그 상태를 부르면 깨진다. 부르지 마라.
2. **반쪽전지 측정이 하나뿐이다.** 파우치 파이프라인은 상태마다 반쪽전지를
   따로 쟀는데(`data/half_cell/GITT/{상태}.xlsx`) 이 셀은 한 번만 쟀다.
   그래서 같은 파일을 네 상태 이름으로 복사한다.
   ⚠ 이것은 **모델 가정이 달라지는 자리**다. 파우치 쪽은 `E_PE` 가 상태마다
   갱신되는데 여기서는 고정이다. 그러면 양극 OCP 의 실제 변화가 전부
   `a_PE`·`b_PE` 로 흡수되어 **LAM_PE 가 다른 것을 재게 된다.**
   두 셀의 LAM_PE 를 나란히 비교하지 마라.

   ⚠⚠ **LLI 도 안전하지 않다** (2026-09-11 정정). 이 머리말은 오래
   "LAM_NE·LLI 는 영향이 적다" 고 적어 왔고 사용자에게도 그렇게 말했는데
   **틀렸다.** 정의가 `c_lit = (a_PE + b_PE − b_NE)·c` 이므로 LLI 는
   `a_PE`·`b_PE` 를 **직접** 쓴다. 즉 위 대체는 LAM_PE 와 **LLI 양쪽**에
   들어간다. 절연된 것은 **LAM_NE 하나뿐**이다 —
   `LAM_NE = 1 − (a_NE·c)/(a_NE_ref·c_ref)` 에 PE 항이 없다.
   이것이 원통형 셀의 넓은 LLI 띠를 "셀 차이" 로 읽으면 안 되는 이유다.
   산술은 `tests/test_review_findings.py::
   test_half_cell_substitution_reaches_lli_not_just_lam_pe` 가 고정한다.
   (덧붙여: `main_blend_final.m` 머리말은 "PE=pristine 고정" 이라고 적어
   두었으므로, 이 셀 쪽이 오히려 **그들이 문서에 쓴 의도**와 같다 — §4-3.)
3. **`step_005C` 소스가 없다.** `matrix` 는 반쪽전지 축이 하나뿐이라
   조합이 절반(w_dqdv 당 8 개)이 된다. `cmd_matrix` 가 없는 파일을 건너뛴다.
4. 문헌 곡선은 원 루트에서 **그대로 복사**한다 (셀과 무관한 자료).
"""
from __future__ import annotations
import argparse, shutil, sys
from pathlib import Path

import numpy as np
import pandas as pd

#: 컬럼쌍 인덱스 → 우리 상태 이름. 용량이 단조 감소하는 것으로 순서를 확인했다
#: (#168: 0.3790→0.3777→0.3637→0.3457, #171: 0.3783→0.3716→0.3520→0.3311).
STATE_OF_COL = {0: "pristine", 1: "100", 2: "200", 3: "300_0009"}

CELL_FILE = {"#168": "experiment/cylindrical/pOCV_#168.xlsx",
             "#171": "experiment/cylindrical/pOCV_#171.xlsx"}
HALF_FILE = "half cell ocv/320mAh_cylindrical_cell_half_cell_ocv.xlsx"


def read_cell(path: Path) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """`{k}_capacity` / `{k}_voltage` 컬럼쌍 4 개를 상태별로 꺼낸다."""
    df = pd.read_excel(path)
    out = {}
    for k, state in STATE_OF_COL.items():
        cc, vc = f"{k}_capacity", f"{k}_voltage"
        if cc not in df.columns or vc not in df.columns:
            raise SystemExit(f"{path.name} 에 {cc}/{vc} 가 없다 — 컬럼: "
                             f"{list(df.columns)}")
        c = pd.to_numeric(df[cc], errors="coerce")
        v = pd.to_numeric(df[vc], errors="coerce")
        ok = c.notna() & v.notna()
        out[state] = (c[ok].to_numpy(float), v[ok].to_numpy(float))
    return out


def write_full_cell(states: dict, dest: Path) -> Path:
    """2 행 헤더 + 컬럼쌍 — `load_full_cell` 이 읽는 그 형식.

    파일 이름에 `pristine`·`300cycle` 이 들어가면 `full_cell_workbook` 이
    후보에서 뺀다. 그래서 중립적인 이름을 쓴다.
    """
    dest.mkdir(parents=True, exist_ok=True)
    names = [STATE_OF_COL[k] for k in sorted(STATE_OF_COL)]
    cols, n = [], max(len(states[s][0]) for s in names)
    for s in names:
        c, v = states[s]
        pad = np.full(n - len(c), np.nan)
        cols += [np.concatenate([c, pad]), np.concatenate([v, pad])]
    hdr = pd.DataFrame([sum(([s, s] for s in names), []),
                        ["Ah", "V"] * len(names)])
    body = pd.DataFrame(np.column_stack(cols))
    path = dest / "cell_states.xlsx"
    with pd.ExcelWriter(path) as w:
        hdr.to_excel(w, index=False, header=False, startrow=0)
        body.to_excel(w, index=False, header=False, startrow=2)
    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="규진팀 프로젝트 루트")
    ap.add_argument("--cell", required=True, choices=sorted(CELL_FILE))
    ap.add_argument("--out", required=True, help="만들 BMS_DATA_ROOT")
    ap.add_argument("--half-cell", default=HALF_FILE)
    a = ap.parse_args()

    src, out = Path(a.src), Path(a.out)
    cell_path, half_path = src / CELL_FILE[a.cell], src / a.half_cell
    for p in (cell_path, half_path):
        if not p.is_file():
            raise SystemExit(f"없다: {p}")

    states = read_cell(cell_path)
    print(f"풀셀 {cell_path.name}")
    prev = None
    for s in (STATE_OF_COL[k] for k in sorted(STATE_OF_COL)):
        c, v = states[s]
        drop = "" if prev is None else f"  (직전 대비 {100*(c[-1]/prev-1):+.2f} %)"
        print(f"  {s:10} n={len(c):6d}  c_max={c[-1]:.6g}  "
              f"V {v[0]:.4f} → {v[-1]:.4f}{drop}")
        prev = c[-1]
    # ⚠ **이름 순서**로 검사한다. 컬럼 위치로 검사하면 STATE_OF_COL 을 통째로
    #   뒤집어도 통과한다 — 쓰기도 읽기도 위치 기반이라 뒤집힘이 상쇄되기
    #   때문이다 (2026-09-10 변이 시험에서 실제로 안 잡혔다). 이름을 붙드는
    #   물리 제약은 하나뿐이다: **열화하면 용량이 준다.**
    ORDER = ["pristine", "100", "200", "300_0009"]
    caps = [states[s][0][-1] for s in ORDER if s in states]
    if not all(x > y for x, y in zip(caps, caps[1:])):
        raise SystemExit(
            "상태 이름과 용량이 안 맞는다 — " +
            " > ".join(f"{s}={states[s][0][-1]:.6g}" for s in ORDER if s in states) +
            "\n  열화하면 용량이 줄어야 한다. STATE_OF_COL 매핑을 확인하라.")

    wb = write_full_cell(states, out / "data" / "full_cell" / "large_cell_033C")
    print(f"\n→ {wb}")

    hc_dir = out / "data" / "half_cell" / "GITT"
    hc_dir.mkdir(parents=True, exist_ok=True)
    for s in STATE_OF_COL.values():
        shutil.copyfile(half_path, hc_dir / f"{s}.xlsx")
    print(f"→ {hc_dir}/{{{','.join(STATE_OF_COL.values())}}}.xlsx"
          f"   (같은 측정 하나를 네 번 — 머리말 2번)")

    lit_src, lit_dst = src / "data" / "literature", out / "data" / "literature"
    if not lit_src.is_dir():
        raise SystemExit(f"문헌 곡선이 없다: {lit_src}")
    if lit_dst.exists():
        shutil.rmtree(lit_dst)
    shutil.copytree(lit_src, lit_dst)
    print(f"→ {lit_dst}  (원 루트에서 복사)")

    # ── 만든 것을 **실제로 적재해 본다** — 산출을 안 열어보고 끝내지 않는다 ──
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from bms_balancing import data as D                       # noqa: E402
    from bms_balancing.verify import build, dd_eval_anchors    # noqa: E402
    print("\n적재 확인 (data.py 로 되읽기)")
    for s in STATE_OF_COL.values():
        obj = build(out, "GITT", s, "Li")
        an = dict(dd_eval_anchors(obj))
        print(f"  {s:10} c_cell={an['c_cell']:.6g}  dv_n={an['dv_n']:.0f}  "
              f"E_PE(0.5)={an['E_PE_0p5']:.4f}  "
              f"E_NE(0.5,0.25)={an['E_NE_0p5_0p25']:.4f}  "
              f"n_peaks={an['n_peaks']:.0f}")
    print(f"\n됐다.  BMS_DATA_ROOT={out}")
    print("⚠ 이 트리에는 `300_0147` 과 `step_005C` 가 없다 (머리말 1·3번).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

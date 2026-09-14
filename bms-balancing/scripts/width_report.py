#!/usr/bin/env python3
"""폭을 읽는다 — `cycles_*.csv` 하나면 표로, 둘이면 **한 축만 다른 두 실행**을 견준다.

    python3 scripts/width_report.py <cycles.csv>                     # 표
    python3 scripts/width_report.py <A.csv> <B.csv> --axis w_dqdv    # 비교 (축 하나만 달라야 한다)

왜 스크립트인가 (`compare_states.py` 와 같은 이유): 이 비교를 손으로 하면 그 숫자가 **문서에만 있는 주장**이
된다. 그리고 두 실행의 설정이 축 하나 말고 또 다르면 그 비교는 아무것도 뜻하지 않는데, 눈으로는 안 보인다 —
sidecar 를 읽어 **기계가 막는다**.

종료 코드: 0 정상 · 2 입력 문제 (파일 없음 · 폭이 안 실림 · 축 말고 다른 설정이 다름).

⚠ 폭은 **하한**이다 (`width_is_lower_bound`). 국소 해법 + 격자로 미는 값이라 참 폭보다 좁을 수 있다.
⚠ 이 폭은 **모델 고정 축**이다 — 문헌 곡선 선택이 만드는 폭(`matrix_*`)은 여기 안 들어간다. 두 축을 합치지 않는다.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys

MODES = ("LAM_PE", "LAM_NE", "LLI")

#: 두 실행이 **같아야** 하는 설정 — 여기가 다르면 그 비교는 축 하나의 것이 아니다.
#: (`--axis` 로 지정한 것 하나만 예외다. `run_states.sh` 의 "같은 설정이어야 비교가 성립한다" 와 같은 규율.)
COMPARED_SETTINGS = ("lb", "ub", "initial", "gamma_prefit", "gamma_lb", "n_multistart", "seed",
                     "scale_seed", "w_pocv", "w_dvdq", "w_dqdv", "optimizer",
                     "widths", "width_tol", "width_starts", "width_method",
                     "cell", "si_source", "starts", "cycles")


def load(path: pathlib.Path):
    """(rows, meta) — 폭이 실려 있지 않으면 여기서 멈춘다."""
    if not path.is_file():
        print(f"! 파일이 없다: {path}", file=sys.stderr); raise SystemExit(2)
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if not rows:
        print(f"! 행이 없다: {path}", file=sys.stderr); raise SystemExit(2)
    if "width_status" not in rows[0]:
        print(f"! 폭 열이 없다 ({path.name}) — `--widths` 없이 만든 산출이다", file=sys.stderr); raise SystemExit(2)
    st = {r["width_status"] for r in rows}
    if st != {"measured"}:
        print(f"! 폭이 전부 measured 가 아니다 ({path.name}): {sorted(st)} — "
              f"안 잰 행이 섞이면 이 표는 모집단을 말할 수 없다", file=sys.stderr)
        raise SystemExit(2)
    mp = path.with_name(path.name + ".meta.json")
    meta = json.loads(mp.read_text(encoding="utf-8")) if mp.is_file() else {}
    return rows, meta


def span(r, mode) -> float:
    """폭 (%p) — 행의 단위는 분수라 100 을 곱한다."""
    return (float(r[f"{mode}_hi"]) - float(r[f"{mode}_lo"])) * 100.0


def table(rows, meta, path):
    tol = rows[0].get("width_tol", "?")
    print(f"\n══ {path.name}  (허용 {tol} · w_dqdv {meta.get('w_dqdv', '?')} · "
          f"seed {meta.get('seed', '?')} · starts {meta.get('n_multistart', meta.get('starts', '?'))}) ══")
    print(f"{'cyc':>4}  " + "".join(f"{m:^30}" for m in MODES))
    print(f"{'':>4}  " + "".join(f"{'점추정   [ 하한 ,  상한 ]':^30}" for _ in MODES))
    for r in rows:
        line = f"{r['cycle']:>4}  "
        for m in MODES:
            pt = float(r[m]) * 100.0
            lo = float(r[f"{m}_lo"]) * 100.0
            hi = float(r[f"{m}_hi"]) * 100.0
            line += f"{pt:7.2f} [{lo:7.2f},{hi:7.2f}] "
        print(line)
    print(f"{'폭':>4}  " + "".join(
        f"{'':7} 최대 {max(span(r, m) for r in rows):7.2f} %p " for m in MODES))
    if not all(str(r.get("width_is_lower_bound")) == "True" for r in rows):
        print("  ⚠ 어떤 행의 width_is_lower_bound 가 True 가 아니다 — 확인할 것")
    else:
        print("  ⚠ 이 폭은 **하한**이다 (국소 해법 + 격자). 참 폭은 이보다 넓을 수 있다.")
    print("  ⚠ **모델 고정 축**의 폭이다 — 문헌 곡선 선택이 만드는 폭은 여기 안 들어간다.")


def guard_same_except(axis, ma, mb, pa, pb):
    """축 하나 말고 다른 설정이 다르면 **비교를 거부한다.**"""
    diff = [k for k in COMPARED_SETTINGS
            if k != axis and json.dumps(ma.get(k), sort_keys=True) != json.dumps(mb.get(k), sort_keys=True)]
    if axis not in COMPARED_SETTINGS:
        print(f"! `--axis {axis}` 는 견주는 설정 목록에 없다: {COMPARED_SETTINGS}", file=sys.stderr); raise SystemExit(2)
    if json.dumps(ma.get(axis)) == json.dumps(mb.get(axis)):
        print(f"! 두 실행의 {axis} 가 같다 ({ma.get(axis)!r}) — 이 비교는 그 축의 것이 아니다",
              file=sys.stderr); raise SystemExit(2)
    if diff:
        print(f"! 축({axis}) 말고 다른 설정이 다르다 — 비교하지 않는다:", file=sys.stderr)
        for k in diff:
            print(f"    {k}: {pa.name} {ma.get(k)!r}  ↔  {pb.name} {mb.get(k)!r}", file=sys.stderr)
        raise SystemExit(2)


def compare(axis, ra, ma, pa, rb, mb, pb):
    guard_same_except(axis, ma, mb, pa, pb)
    ca, cb = {r["cycle"]: r for r in ra}, {r["cycle"]: r for r in rb}
    common = [c for c in ca if c in cb]
    if not common:
        print("! 공통 cycle 이 없다", file=sys.stderr); raise SystemExit(2)
    print(f"\n══ 폭 비교 — 축 `{axis}`: {ma.get(axis)!r} → {mb.get(axis)!r}  (공통 cycle {len(common)}) ══")
    print(f"{'축':>8}  {'A 최대 폭':>12}  {'B 최대 폭':>12}  {'B/A':>8}   판정")
    for m in MODES:
        a = max(span(ca[c], m) for c in common)
        b = max(span(cb[c], m) for c in common)
        ratio = (b / a) if a > 0 else float("nan")
        verdict = ("좁아졌다" if b < a * 0.9 else "넓어졌다" if b > a * 1.1 else "거의 그대로")
        print(f"{m:>8}  {a:9.3f} %p  {b:9.3f} %p  {ratio:8.3f}   {verdict}")
    print("\n  ⚠ 이것은 **이 셀·이 사이클 집합·이 허용**에서의 비교다. 다른 셀로 일반화하지 않는다.")
    print("  ⚠ 폭이 좁아졌다고 그 설정이 '옳다' 는 뜻은 아니다 — 좁은 답이 참에 가깝다는 근거가 따로 필요하다.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="+", type=pathlib.Path, help="cycles_*.csv (하나 또는 둘)")
    ap.add_argument("--axis", default="w_dqdv", help="두 실행에서 **유일하게** 달라야 하는 설정 이름 (기본 w_dqdv)")
    a = ap.parse_args(argv)
    if len(a.csv) > 2:
        print("! 파일은 하나 또는 둘이다", file=sys.stderr); return 2
    loaded = [(p, *load(p)) for p in a.csv]
    for p, rows, meta in loaded:
        table(rows, meta, p)
    if len(loaded) == 2:
        (pa, ra, ma), (pb, rb, mb) = loaded
        compare(a.axis, ra, ma, pa, rb, mb, pb)
    return 0


if __name__ == "__main__":
    sys.exit(main())

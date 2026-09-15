#!/usr/bin/env python3
"""§20 — Desktop 부분 후처리 묶음의 수치를 **원시 CSV 에서** 다시 센다.

묶음의 분석 산출(`analysis/`)을 입력으로 쓰지 않는다. 읽는 것은 보존된
`reviews/r14_repros/codex63/desktop_postproc/raw_csv/` 의 다섯 CSV 와 좌표 입력뿐이다.
산술은 전부 `Decimal`. COMSOL 을 부르지 않고 묶음 안의 Java/Python 도 실행하지 않는다.

출력은 JSON 하나 (stdout). 판정을 내리지 않는다 — 숫자를 다시 낼 뿐이고, 판정과 그 범위는
`docs/COMSOL_REBUILD_SPEC.md` §20 이 적는다.

    python3 scripts/recheck_desktop_postproc.py > reviews/r14_repros/codex63/desktop_postproc/RECHECK_YYYY-MM-DD.json

⚠ COMSOL 표는 머리에 `%` 주석 줄이 있고, 열 이름이 단위·Point 를 달고 온다. 헤더를 손으로
  옮겨 적지 않고 `% Time (s),` 로 시작하는 줄을 그대로 열 이름으로 쓴다.
"""
from __future__ import annotations

import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
BUNDLE = HERE / "reviews" / "r14_repros" / "codex63" / "desktop_postproc"
RAW = BUNDLE / "raw_csv"


def table(path: Path) -> tuple[list[str], list[list[str]], dict]:
    """COMSOL 표 CSV → (열 이름, 행, 머리말). 머리 주석은 버리지 않고 돌려준다."""
    import csv

    head, cols, body = {}, None, []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if not row:
                continue
            if row[0].startswith("%"):
                key = row[0].lstrip("% ").strip()
                if cols is None and key.startswith("Time (s)"):
                    cols = [key] + row[1:]          # 마지막 주석 줄이 열 이름이다
                else:
                    head[key] = row[1] if len(row) > 1 else ""
                continue
            body.append(row)
    if cols is None:
        raise SystemExit(f"! {path.name}: 열 이름 줄(`% Time (s),…`)을 못 찾았다")
    return cols, body, head


def dec(s: str) -> Decimal:
    try:
        return Decimal(s.strip())
    except InvalidOperation:
        raise SystemExit(f"! 숫자로 못 읽는 값: {s!r}")


def times_ok(body: list[list[str]]) -> dict:
    ts = [dec(r[0]) for r in body]
    return {"rows": len(ts), "unique": len(set(ts)), "strictly_increasing": all(
        a < b for a, b in zip(ts, ts[1:])), "first_s": str(ts[0]), "last_s": str(ts[-1]),
        "duplicate_time_column": all(dec(r[0]) == dec(r[1]) for r in body)}


def electrolyte() -> dict:
    cols_a, body_a, head_a = table(RAW / "electrolyte_auto_units.csv")
    cols_e, body_e, head_e = table(RAW / "electrolyte_explicit_units.csv")

    # 자동 단위판과 명시 단위판이 **값까지** 같은가 (바이트가 같다는 주장은 하지 않는다)
    same_cols = cols_a == cols_e
    same_vals = (len(body_a) == len(body_e)
                 and all(len(x) == len(y) and all(dec(p) == dec(q) for p, q in zip(x, y))
                         for x, y in zip(body_a, body_e)))

    i_min = next(i for i, c in enumerate(cols_a) if c.startswith("Minimum (") )
    i_d = [i for i, c in enumerate(cols_a) if c.startswith("Minimum ")][1:]      # 1·2·3
    i_thr = next(i for i, c in enumerate(cols_a) if c.startswith("ce_stop_threshold"))
    i_cond = next(i for i, c in enumerate(cols_a) if c.startswith("comp1.minguardall"))

    overall_matches = all(dec(r[i_min]) == min(dec(r[j]) for j in i_d) for r in body_a)
    thr_nonzero = sum(1 for r in body_a if dec(r[i_thr]) != 0)
    cond_nonzero = sum(1 for r in body_a if dec(r[i_cond]) != 0)
    finite = all(dec(r[j]).is_finite() for r in body_a for j in (i_min, *i_d))

    best = min(body_a, key=lambda r: dec(r[i_min]))
    which = [k for k, j in enumerate(i_d, 1) if dec(best[j]) == dec(best[i_min])]

    return {
        "times": times_ok(body_a),
        "auto_vs_explicit": {"same_column_names": same_cols, "same_decimal_values": same_vals,
                             "note": "값이 같다는 확인이다 — 원본 바이트가 같다는 주장이 아니다 "
                                     "(머리말의 날짜·표 이름이 다르다)",
                             "auto_table": head_a.get("Table"), "explicit_table": head_e.get("Table")},
        "overall_min_equals_min_of_three_domains_every_row": overall_matches,
        "all_finite": finite,
        "overall_min_mol_m3": str(dec(best[i_min])),
        "overall_min_time_s": str(dec(best[0])),
        "overall_min_domain": which,
        "threshold_nonzero_rows": thr_nonzero,
        "guard_condition_nonzero_rows": cond_nonzero,
        "columns": cols_a,
    }


def guards() -> dict:
    cols, body, _ = table(RAW / "ocp_surface_guards.csv")
    conds = list(range(2, len(cols)))
    return {"times": times_ok(body), "condition_columns": len(conds),
            "nonzero_rows_per_condition": {cols[j][:60]: sum(1 for r in body if dec(r[j]) != 0)
                                           for j in conds}}


def boundary(name: str, point: str) -> dict:
    cols, body, _ = table(RAW / name)

    def col(prefix: str) -> int:
        hit = [i for i, c in enumerate(cols) if c.startswith(prefix)]
        if len(hit) != 1:
            raise SystemExit(f"! {name}: `{prefix}` 열이 {len(hit)} 개다")
        return hit[0]

    i_phis, i_phil = col('"phis (V)'.strip('"')), col("phil (V)")
    i_eeq, i_etamid = col("liion.Eeq_per1 (V)"), col("liion.etamid_per1 (V)")
    res = max(abs(dec(r[i_phis]) - dec(r[i_phil]) - dec(r[i_eeq]) - dec(r[i_etamid])) for r in body)
    return {"times": times_ok(body), "point": point, "columns": len(cols),
            "identity_max_abs_residual_V": str(res),
            "phis_by_time": {str(dec(r[0])): str(dec(r[i_phis])) for r in body}}


def voltage_windows(b1: dict, b4: dict) -> dict:
    """경계 4(양극) − 경계 1(음극) 의 `phis` 차 = 단자전압. 여기서는 **한 해**뿐이라 창별 범위만 낸다."""
    t1, t4 = b1["phis_by_time"], b4["phis_by_time"]
    common = sorted((Decimal(t) for t in t1 if t in t4))
    out = {}
    for ko, lo, hi in (("0.1–1 s", Decimal("0.1"), Decimal(1)), ("1–5 s", Decimal(1), Decimal(5)),
                       ("0–1 s", Decimal(0), Decimal(1)), ("0–5 s", Decimal(0), Decimal(5))):
        ts = [t for t in common if lo <= t <= hi]
        v = [Decimal(t4[str(t)]) - Decimal(t1[str(t)]) for t in ts]
        out[ko] = {"n_times": len(ts), "min_V": str(min(v)), "max_V": str(max(v))} if ts else {"n_times": 0}
    return {"exact_common_times": len(common), "windows": out}


def coordinates() -> dict:
    d = BUNDLE / "coordinate_inputs"
    out = {}
    for p in sorted(d.glob("*")) if d.is_dir() else []:
        if not p.is_file():
            continue
        vals = [x for x in p.read_text(encoding="utf-8").replace(",", " ").split() if x]
        try:
            nums = [Decimal(x) for x in vals]
        except InvalidOperation:
            out[p.name] = {"lines": len(vals), "note": "숫자로 못 읽는 항목이 있다"}
            continue
        out[p.name] = {"count": len(nums), "unique": len(set(nums)),
                       "min": str(min(nums)), "max": str(max(nums)),
                       "strictly_increasing": all(a < b for a, b in zip(nums, nums[1:]))}
    return out


def main() -> int:
    if not RAW.is_dir():
        print(f"보존 묶음이 없다: {RAW}", file=sys.stderr)
        return 2
    b1 = boundary("boundary1.csv", "1 (음극)")
    b4 = boundary("boundary4.csv", "4 (양극)")
    vw = voltage_windows(b1, b4)
    for b in (b1, b4):
        b.pop("phis_by_time")
    json.dump({
        "bundle": str(BUNDLE.relative_to(HERE)),
        "what_this_is": "보존된 원시 CSV 다섯 개에서 다시 센 것. 묶음의 분석 산출은 입력이 아니다. "
                        "판정은 이 파일이 내리지 않는다.",
        "electrolyte": electrolyte(),
        "ocp_surface_guards": guards(),
        "boundary_1": b1, "boundary_4": b4,
        "terminal_voltage_from_phis": vw,
        "coordinate_inputs": coordinates(),
    }, sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

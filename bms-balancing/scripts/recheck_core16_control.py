#!/usr/bin/env python3
"""§18 — 16 코어 통제 해 묶음의 16 개 비교를 **원시 CSV 에서** 다시 센다.

묶음의 분석 구현을 import 하지 않는다. 읽는 것은 보존된
`reviews/r14_repros/codex63/core16_control/outputs/core16_control/` 의
비교 CSV(`*_{requested_grid,all_exact_common_stored}_{창}.csv`), 그 옆의
`_profile_at_*` CSV, 세 해의 `*_scalar_all_rows.csv`, `*_accepted_steps.csv`,
`three_way_surface_identity_by_time.csv` 뿐이다. 산술은 전부 `Decimal`.

출력은 JSON 하나 (stdout). 판정을 내리지 않는다 — 숫자를 다시 낼 뿐이고,
판정과 그 범위는 `docs/COMSOL_REBUILD_SPEC.md` §18 이 적는다.

    python3 scripts/recheck_core16_control.py > reviews/r14_repros/codex63/core16_control/RECHECK_YYYY-MM-DD.json
"""
from __future__ import annotations

import csv
import glob
import json
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
BUNDLE = HERE / "reviews" / "r14_repros" / "codex63" / "core16_control" / "outputs" / "core16_control"
RES = BUNDLE / "results"

FAMILIES = {"core_control_2_to_16": "control16 − old2 (코어 축 단독)",
            "late_cap_at_16_cores": "A16 − control16 (cap 축 단독, 16 코어 고정)"}
SETS = {"requested_grid": "지정 요청", "all_exact_common_stored": "정확 공통 저장"}
WINDOWS = ["0p1_to_1s", "1_to_5s", "0_to_1s", "0_to_5s"]
RUNS = {"old2": "Caps300R320H0125_18a00b03e38d4694b9ba30d88e7008f4",
        "control16": "Caps300R320H0125C16_5d1a87652ed54e6a945d4f2af4aeda70",
        "A16": "Caps300R320LateCapA5s_c40c05d3cfb643a4b706345637b00f57"}
STEPS = {"old2": "Caps300R320H0125", "control16": "Caps300R320H0125C16",
         "A16": "Caps300R320LateCapA5s"}


def rows(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def comparisons() -> dict:
    out = {}
    for fam, fam_ko in FAMILIES.items():
        for st, st_ko in SETS.items():
            for w in WINDOWS:
                base = f"{fam}_{st}_{w}"
                main = rows(RES / f"{base}.csv")
                best = max(main, key=lambda r: abs(Decimal(r["difference_V_second_minus_first_V"])))
                dv = Decimal(best["difference_V_second_minus_first_V"])
                comp = (Decimal(best["difference_delta_Eeq_V"]) + Decimal(best["difference_delta_etaMid_V"])
                        + Decimal(best["difference_delta_phiL_V"]))
                xb = None
                for pf in sorted(glob.glob(str(RES / f"{base}_profile_at_*.csv"))):
                    for r in rows(Path(pf)):
                        v = abs(Decimal(r["x_surface_difference_second_minus_first"]))
                        if xb is None or v > xb[0]:
                            xb = (v, r)
                out[base] = {
                    "family": fam_ko, "sample_set": st_ko, "window": w, "n_times": len(main),
                    "max_abs_dV_mV": str(abs(dv) * 1000), "dV_signed_V": str(dv), "at_time_s": best["time_s_exact"],
                    "decomp_residual_V_recomputed": str(dv - comp),
                    "decomp_residual_V_column": best["difference_decomposition_residual_V"],
                    "max_abs_dx_surface": str(xb[0]), "dx_signed": xb[1]["x_surface_difference_second_minus_first"],
                    "dx_time_s": xb[1]["time_s_exact"], "dx_electrode": xb[1]["electrode"],
                    "dx_coordinate_m": xb[1]["coordinate_first_m"],
                }
    return out


def three_way() -> dict:
    scal = {k: {Decimal(r["time_s"]): Decimal(r["V_V"]) for r in rows(RES / f"{v}_scalar_all_rows.csv")}
            for k, v in RUNS.items()}
    o, c, a = scal["old2"], scal["control16"], scal["A16"]
    common = set(o) & set(c) & set(a)
    req = json.loads((BUNDLE / "comparison_contract.json").read_text(encoding="utf-8"))["requested_times_s"]
    vres = max(abs((a[t] - o[t]) - ((c[t] - o[t]) + (a[t] - c[t]))) for t in common)
    surf = rows(RES / "three_way_surface_identity_by_time.csv")
    return {
        "stored_rows": {k: len(v) for k, v in scal.items()},
        "exact_common_all_three": len(common),
        "pairwise_common": {"old2∩control16": len(set(o) & set(c)), "control16∩A16": len(set(c) & set(a)),
                            "old2∩A16": len(set(o) & set(a))},
        "requested_times_in_common": sum(1 for r in req if Decimal(r) in common),
        "requested_times_total": len(req),
        "voltage_identity_max_residual_V": str(vres),
        "surface_identity_file": {
            "rows": len(surf), "times": len({r["time_s_exact"] for r in surf}),
            "coordinate_sum": sum(int(r["checked_coordinates"]) for r in surf),
            "coordinates_per_row": sorted({int(r["checked_coordinates"]) for r in surf}),
            "max_abs_residual": str(max(Decimal(r["max_abs_signed_identity_residual_x"]) for r in surf)),
            "note": "전달 파일의 검산 — 전 시각 profile 원문은 미보존(8 MiB 초과)이라 원시 재계산 아님",
        },
    }


def intervals() -> dict:
    out = {}
    tbl = {}
    for k, v in STEPS.items():
        st = rows(BUNDLE / f"{v}_accepted_steps.csv")
        tbl[k] = st
        reg: dict[str, list[Decimal]] = {}
        for r in st:
            reg.setdefault(r["region"], []).append(Decimal(r["actual_step_s_exact"]))
        out[k] = {
            "accepted": len(st),
            "cap_violations": sum(1 for r in st if r["within_cap_with_1e-12s_roundoff"].strip().lower()
                                  not in ("true", "1", "yes")),
            "by_region": {name: {"count": len(h), "max_h_s": str(max(h))} for name, h in reg.items()},
        }
    o, c = tbl["old2"], tbl["control16"]
    out["old2_vs_control16_identical_intervals"] = sum(
        1 for x, y in zip(o, c) if x["start_time_s_exact"] == y["start_time_s_exact"]
        and x["end_time_s_exact"] == y["end_time_s_exact"])
    return out


def main() -> int:
    if not RES.is_dir():
        print(f"보존 묶음이 없다: {RES}", file=sys.stderr)
        return 2
    json.dump({"bundle": str(BUNDLE.relative_to(HERE)), "comparisons": comparisons(),
               "three_way": three_way(), "intervals": intervals()},
              sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

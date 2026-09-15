#!/usr/bin/env python3
"""§19 — 물리축 B (300 → 600) 묶음의 여덟 비교를 **원시 CSV 에서** 다시 센다.

묶음의 분석 구현(`analysis.json` · `physical_axis_*.csv`)을 **입력으로 쓰지 않는다.**
전압은 두 해의 `*_scalar_all_rows.csv` 에서 **경계의 `phis` 차**로 다시 만들고, 시각은
두 해에 **정확히 같은 저장 시각**만 잇는다 (보간·최근접 대체 없음). 표면 조성은 보존된
`_profile_at_*` CSV 에서 센다. 산술은 전부 `Decimal`.

`analysis.json` 과 `physical_axis_*.csv` 는 **대조 대상**으로만 읽는다 — 우리가 낸 값과
묶음이 적은 값이 같은지 보기 위해서다. 다르면 그것이 발견이다.

출력은 JSON 하나 (stdout). 판정을 내리지 않는다 — 숫자를 다시 낼 뿐이고, 판정과 그 범위는
`docs/COMSOL_REBUILD_SPEC.md` §19 가 적는다.

    python3 scripts/recheck_physical600_b.py > reviews/r14_repros/codex63/physical600_b/RECHECK_YYYY-MM-DD.json

⚠ 이 스크립트는 COMSOL 을 부르지 않고 묶음 안의 Java·Python 도 실행하지 않는다.
  하는 일은 읽기·산술·대조뿐이다.
"""
from __future__ import annotations

import csv
import glob
import json
import sys
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
BUNDLE = HERE / "reviews" / "r14_repros" / "codex63" / "physical600_b" / "outputs" / "physical600_b"
RES = BUNDLE / "results"

#: 기준(300) 과 B(600). 이름 안의 job id 는 묶음이 적은 것이고 파일명으로 확인한다.
FIRST = "Caps300R320H0125C16_5d1a87652ed54e6a945d4f2af4aeda70"
SECOND = "Caps600R320H0125C16_56975e4d24054b23bcec87553875f729"
SETS = {"requested_grid": "지정 요청", "all_exact_common_stored": "정확 공통 저장"}
#: (파일 이름 조각, 사람용, 구간) — 끝점 **포함**이다. 그래서 개수를 단순 합산하지 않는다.
WINDOWS = [("0p1_to_1", "0.1–1 s", Decimal("0.1"), Decimal("1")),
           ("1_to_5", "1–5 s", Decimal("1"), Decimal("5")),
           ("0_to_1", "0–1 s", Decimal("0"), Decimal("1")),
           ("0_to_5", "0–5 s", Decimal("0"), Decimal("5"))]


def rows(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def scalar(tag: str) -> list[dict]:
    hit = sorted(glob.glob(str(RES / f"{tag}_scalar_all_rows.csv")))
    if len(hit) != 1:
        raise SystemExit(f"! {tag} 의 scalar CSV 가 {len(hit)} 개다")
    return rows(Path(hit[0]))


def terminal_voltage(rs: list[dict]) -> dict:
    """저장 시각 → 단자전압. **경계의 `phis` 차로 다시 만든다** (묶음의 `V_V` 를 안 쓴다)."""
    out = {}
    for r in rs:
        t = Decimal(r["time_s"])
        if t in out:
            raise SystemExit(f"! 저장 시각이 중복이다: {t}")
        out[t] = Decimal(r["boundary_P_phis_V"]) - Decimal(r["boundary_N_phis_V"])
    return out


def against_bundle_v(rs: list[dict]) -> str:
    """우리가 만든 전압과 묶음이 적은 `V_V` 열의 최대 차 — 묶음 내부 정합성 대조."""
    m = Decimal(0)
    for r in rs:
        d = abs((Decimal(r["boundary_P_phis_V"]) - Decimal(r["boundary_N_phis_V"])) - Decimal(r["V_V"]))
        m = max(m, d)
    return str(m)


def surface(tag: str) -> dict:
    """저장 시각 → (음극 표면 조성, 양극 표면 조성). scalar CSV 의 경계 값이다."""
    return {Decimal(r["time_s"]): (Decimal(r["boundary_N_x_surface"]),
                                   Decimal(r["boundary_P_x_surface"]))
            for r in scalar(tag)}


def windows(v1: dict, v2: dict, requested: list[Decimal]) -> dict:
    """여덟 창의 최대 |δV| — **정확히 같은 저장 시각**만 잇는다."""
    common = sorted(set(v1) & set(v2))
    req_common = [t for t in requested if t in v1 and t in v2]
    out = {}
    for key, ko, lo, hi in WINDOWS:
        for st, st_ko in SETS.items():
            pool = req_common if st == "requested_grid" else common
            ts = [t for t in pool if lo <= t <= hi]
            if not ts:
                out[f"{st}_{key}"] = {"sample_set": st_ko, "window": ko, "n_times": 0}
                continue
            best = max(ts, key=lambda t: abs(v2[t] - v1[t]))
            d = v2[best] - v1[best]
            out[f"{st}_{key}"] = {
                "sample_set": st_ko, "window": ko, "n_times": len(ts),
                "max_abs_dV_mV": str(abs(d) * 1000), "dV_signed_V": str(d),
                "at_time_s": str(best),
            }
    return out


def bundle_windows() -> dict:
    """묶음이 적은 비교 CSV 에서 같은 값을 뽑는다 — **대조 대상**이지 우리 계산이 아니다."""
    out = {}
    for key, ko, _lo, _hi in WINDOWS:
        for st, st_ko in SETS.items():
            p = RES / f"physical_axis_{st}_{key}.csv"
            if not p.is_file():
                continue
            rs = rows(p)
            best = max(rs, key=lambda r: abs(Decimal(r["difference_V_second_minus_first_V"])))
            d = Decimal(best["difference_V_second_minus_first_V"])
            comp = (Decimal(best["difference_delta_Eeq_V"]) + Decimal(best["difference_delta_etaMid_V"])
                    + Decimal(best["difference_delta_phiL_V"]))
            out[f"{st}_{key}"] = {
                "n_times": len(rs), "max_abs_dV_mV": str(abs(d) * 1000),
                "at_time_s": best["time_s_exact"],
                "decomp_residual_V_recomputed": str(d - comp),
                "decomp_residual_V_column": best["difference_decomposition_residual_V"],
            }
    return out


def profiles() -> dict:
    """보존된 `_profile_at_*` CSV 에서 최대 |δx| 와 그 자리."""
    out = {}
    for key, ko, _lo, _hi in WINDOWS:
        for st, st_ko in SETS.items():
            best = None
            n = 0
            for pf in sorted(glob.glob(str(RES / f"physical_axis_{st}_{key}_profile_at_*.csv"))):
                for r in rows(Path(pf)):
                    n += 1
                    v = abs(Decimal(r["x_surface_difference_second_minus_first"]))
                    if best is None or v > best[0]:
                        best = (v, r)
            if best is None:
                continue
            out[f"{st}_{key}"] = {
                "sample_set": st_ko, "window": ko, "profile_rows": n,
                "max_abs_dx_surface": str(best[0]),
                "dx_signed": best[1]["x_surface_difference_second_minus_first"],
                "dx_time_s": best[1]["time_s_exact"], "dx_electrode": best[1]["electrode"],
                "dx_coordinate_m": best[1]["coordinate_first_m"],
            }
    return out


def identity(tag: str) -> dict:
    """`phis − phil − Eeq − etamid` 의 최대 절대 잔차 — 두 경계 각각."""
    out = {}
    for side in ("N", "P"):
        m = Decimal(0)
        for r in scalar(tag):
            d = (Decimal(r[f"boundary_{side}_phis_V"]) - Decimal(r[f"boundary_{side}_phil_V"])
                 - Decimal(r[f"boundary_{side}_Eeq_V"]) - Decimal(r[f"boundary_{side}_etamid_V"]))
            m = max(m, abs(d))
        out[side] = str(m)
    return out


def intervals() -> dict:
    """§19-3 의 시간 이력을 accepted_steps CSV 에서 다시 센다 (보존돼 있다)."""
    out = {}
    for label, stem in (("first_300", "Caps300R320H0125C16"), ("second_600", "Caps600R320H0125C16")):
        st = rows(BUNDLE / f"{stem}_accepted_steps.csv")
        reg: dict[str, list[Decimal]] = {}
        for r in st:
            reg.setdefault(r["region"], []).append(Decimal(r["actual_step_s_exact"]))
        crossing = sum(1 for r in st
                       if any(Decimal(r["start_time_s_exact"]) < b < Decimal(r["end_time_s_exact"])
                              for b in (Decimal("0.1"), Decimal("1"))))
        out[label] = {
            "accepted": len(st),
            "cap_violations_1e-12s": sum(
                1 for r in st
                if r["within_cap_with_1e-12s_roundoff"].strip().lower() not in ("true", "1", "yes")),
            "crossing_0p1_or_1s": crossing,
            "by_region": {name: {"count": len(h), "max_h_s": str(max(h))} for name, h in sorted(reg.items())},
        }
    a, b = rows(BUNDLE / "Caps300R320H0125C16_accepted_steps.csv"), rows(BUNDLE / "Caps600R320H0125C16_accepted_steps.csv")
    out["identical_intervals"] = sum(
        1 for x, y in zip(a, b)
        if x["start_time_s_exact"] == y["start_time_s_exact"]
        and x["end_time_s_exact"] == y["end_time_s_exact"])
    out["same_length"] = len(a) == len(b)
    return out


def main() -> int:
    if not RES.is_dir():
        print(f"보존 묶음이 없다: {RES}", file=sys.stderr)
        return 2
    r1, r2 = scalar(FIRST), scalar(SECOND)
    v1, v2 = terminal_voltage(r1), terminal_voltage(r2)
    contract = json.loads((BUNDLE / "comparison_contract.json").read_text(encoding="utf-8"))
    requested = [Decimal(x) for x in contract["requested_times_s"]]
    s1, s2 = surface(FIRST), surface(SECOND)
    common = sorted(set(v1) & set(v2))

    ours = windows(v1, v2, requested)
    theirs = bundle_windows()
    agree = {k: {"n_times": ours[k]["n_times"] == theirs[k]["n_times"],
                 "max_abs_dV_mV": ours[k].get("max_abs_dV_mV") == theirs[k]["max_abs_dV_mV"],
                 "at_time_s": Decimal(ours[k]["at_time_s"]) == Decimal(theirs[k]["at_time_s"])}
             for k in sorted(set(ours) & set(theirs))}

    json.dump({
        "bundle": str(BUNDLE.relative_to(HERE)),
        "what_this_is": "원시 scalar CSV 에서 phis 차로 전압을 다시 만들어 여덟 창을 다시 센 것. "
                        "묶음의 분석 산출은 대조 대상으로만 읽었다. 판정은 이 파일이 내리지 않는다.",
        "runs": {"first_300": FIRST, "second_600": SECOND},
        "stored_rows": {"first": len(r1), "second": len(r2)},
        "stored_times": {"first": len(v1), "second": len(v2), "exact_common": len(common),
                         "first_min_s": str(min(v1)), "first_max_s": str(max(v1)),
                         "monotonic_unique_first": len(v1) == len(r1),
                         "monotonic_unique_second": len(v2) == len(r2)},
        "requested_times": {"total": len(requested),
                            "in_exact_common": sum(1 for t in requested if t in v1 and t in v2)},
        "our_voltage_vs_bundle_V_column_max_abs_V": {"first": against_bundle_v(r1),
                                                     "second": against_bundle_v(r2)},
        "identity_residual_max_abs_V": {"first": identity(FIRST), "second": identity(SECOND)},
        "windows_ours": ours,
        "windows_bundle": theirs,
        "agreement_ours_vs_bundle": agree,
        "surface_profiles": profiles(),
        "intervals": intervals(),
        "surface_at_boundary_only": {
            "note": "scalar CSV 의 경계 표면 조성 — 241 좌표 공간 비교가 아니다 (그것은 profile CSV 다)",
            "max_abs_dx_N": str(max(abs(s2[t][0] - s1[t][0]) for t in common)),
            "max_abs_dx_P": str(max(abs(s2[t][1] - s1[t][1]) for t in common)),
        },
    }, sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

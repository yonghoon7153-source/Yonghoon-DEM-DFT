#!/usr/bin/env python3
"""α·β 적합 결과표에 난간을 건다 — 규진팀 MATLAB 결과 xlsx 든 우리 `fit_cycles` 산출이든 **같은 검사**.

    python3 scripts/check_rails.py <result.xlsx|.csv> [...] [--settings settings.json] [--json out.json]

층별 뜻은 `bms_balancing/rails.py` 머리말. 설정 파일(`--settings`)은 optimizer 의 **기록된** 설정
(`{"lb": [...5], "ub": [...5], "free": [...], "n_multistart": N}`) — 없으면 경계 접촉을 확정하지 않는다.
파일 옆에 `<파일>.settings.json` 이 있으면 그것을 쓴다 (MATLAB 드라이버 `matlab/fit_cycles_driver.m` 가 쓴다).

종료 코드: 0 = 계약 위반 없음 (경고는 있을 수 있다) · 2 = 1/3 층 위반 · 3 = 파일을 읽지 못했거나 필수 열이 없다.
마지막 줄 `RAILS {…}` 가 machine-readable 판정이다.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bms_balancing import rails as R          # noqa: E402


def _read(path: pathlib.Path) -> list:
    import pandas as pd
    df = pd.read_excel(path) if path.suffix.lower() in (".xlsx", ".xls") else pd.read_csv(path)
    rows = []
    for rec in df.to_dict(orient="records"):
        rows.append({str(k): (None if (isinstance(v, float) and math.isnan(v)) else v) for k, v in rec.items()})
    return rows


def _settings_for(path: pathlib.Path, explicit: pathlib.Path | None):
    """optimizer 설정: `--settings` → `<파일>.settings.json` (MATLAB 드라이버) → `<파일>.meta.json` (우리 `fit_cycles`
    sidecar — lb/ub 를 담는다). 어느 것도 없으면 None (3 층은 접촉을 확정하지 않는다)."""
    cands = [explicit] if explicit else [path.with_name(path.name + ".settings.json"), path.with_name(path.name + ".meta.json")]
    for cand in cands:
        if cand and cand.is_file():
            try:
                d = json.loads(cand.read_text(encoding="utf-8-sig"))
            except ValueError as e:
                return None, f"{cand}: JSON 이 아니다 ({e})"
            if isinstance(d, dict) and "lb" in d and "ub" in d:
                return d, str(cand)
    return None, None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--settings", type=pathlib.Path, default=None, help="optimizer 설정 JSON (모든 파일에 적용)")
    ap.add_argument("--json", type=pathlib.Path, default=None, help="판정 전체를 이 파일에 JSON 으로")
    ap.add_argument("--atol", type=float, default=1e-9, help="후처리 항등식 허용 오차 (기본 1e-9)")
    a = ap.parse_args(argv)
    out = {"ok": True, "files": [], "rc": 0}
    unreadable = False
    for f in a.files:
        entry = {"file": str(f), "n_rows": 0, "ok": False, "settings": None, "findings": [], "counts": {}}
        print(f"■ {f}")
        try:
            rows = _read(f)
        except Exception as e:                        # noqa: BLE001 — 읽기 실패는 판정이 아니라 입력 문제다
            print(f"  ! 읽지 못했다: {type(e).__name__}: {e}")
            entry["error"] = f"{type(e).__name__}: {e}"; unreadable = True
            out["files"].append(entry); continue
        settings, src = _settings_for(f, a.settings)
        entry["settings"] = src
        rep = R.run_all(rows, settings=settings, atol=a.atol)
        entry.update({"n_rows": rep["n_rows"], "ok": rep["ok"], "findings": rep["findings"], "counts": rep["counts"]})
        if any(x["check"] == "columns" for x in rep["findings"]):
            unreadable = True
        print(f"  행 {rep['n_rows']} · 열 {len(rep['columns'])} · 설정 {src or '없음'} · "
              f"error {rep['counts']['error']} · warning {rep['counts']['warning']} · info {rep['counts']['info']}")
        for lv in R.LEVELS:
            for x in rep["findings"]:
                if x["level"] == lv:
                    print(f"  [{lv:7s}] L{x['layer']} {x['check']}: {x['msg']}")
        out["files"].append(entry)
        out["ok"] = out["ok"] and rep["ok"]
    out["rc"] = 3 if unreadable else (0 if out["ok"] else 2)
    if a.json:
        a.json.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=float) + "\n", encoding="utf-8")
    print("RAILS " + json.dumps({"ok": out["ok"], "rc": out["rc"],
                                 "files": [{k: v for k, v in e.items() if k != "findings"} for e in out["files"]]},
                                ensure_ascii=False, default=float))
    return out["rc"]


if __name__ == "__main__":
    sys.exit(main())

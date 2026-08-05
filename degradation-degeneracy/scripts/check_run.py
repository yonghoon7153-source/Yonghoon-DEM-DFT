#!/usr/bin/env python3
"""check_run.py — grid 실행 결과 정합성 검사.

중단·재개·(사고로) 동시 실행이 있었던 run은 반드시 이걸로 확인한다.
"완료 표시는 남았는데 곡선이 없는" 조건이 있으면 resume이 그 조건을 건너뛰어
조용히 빠진 채로 Phase 4로 넘어가게 된다.

사용:
    python scripts/check_run.py results/grid_fine_v1
    python scripts/check_run.py results/grid_fine_v1 --repair

--repair: 곡선이 없는 조건의 완료 표시를 지운다.
          이후 `./run.sh --mode grid ... --resume` 하면 그 조건만 다시 계산한다.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd  # noqa: E402

from src.io import completed_path, load_completed, load_failed  # noqa: E402


def check(run_dir: Path) -> dict:
    curves_path = run_dir / "curves.parquet"
    if not curves_path.exists():
        raise SystemExit(f"curves.parquet 없음: {curves_path} (실행이 끝나지 않았을 수 있음)")

    df = pd.read_parquet(curves_path)
    curves = set(df["cond_id"].unique())
    done = load_completed(run_dir)
    failed = load_failed(run_dir)

    missing = done - failed - curves          # 완료 표시됐는데 곡선 없음 ★
    orphan = curves & failed                  # 곡선도 있고 실패로도 기록됨
    untracked = curves - done                 # 곡선은 있는데 완료 표시 없음

    rows_per_cond = df.groupby("cond_id").size()
    bad_len = rows_per_cond[rows_per_cond != rows_per_cond.mode()[0]]

    return {
        "curves": len(curves), "done": len(done), "failed": len(failed),
        "rows": len(df), "points_per_cond": int(rows_per_cond.mode()[0]),
        "missing": sorted(missing), "orphan": sorted(orphan),
        "untracked": sorted(untracked), "bad_len": bad_len.to_dict(),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="grid 결과 정합성 검사")
    ap.add_argument("run_dir")
    ap.add_argument("--repair", action="store_true",
                    help="곡선 없는 완료 표시를 제거 (이후 --resume으로 재계산)")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    r = check(run_dir)

    print(f"곡선 조건      : {r['curves']}")
    print(f"완료표시(고유) : {r['done']}")
    print(f"failed(고유)   : {r['failed']}")
    print(f"행 수          : {r['rows']} (= {r['curves']} × {r['points_per_cond']})")
    print(f"기대 조건 수   : {r['done'] - r['failed']} (완료 − 실패)")

    ok = True
    if r["missing"]:
        ok = False
        print(f"\n★ 완료표시됐는데 곡선 없음: {len(r['missing'])}건 — 데이터 손실")
        print(f"  예: {r['missing'][:5]}")
    if r["orphan"]:
        ok = False
        print(f"\n! 곡선과 failed에 중복 기록: {len(r['orphan'])}건")
    if r["untracked"]:
        print(f"\n! 곡선은 있으나 완료표시 없음: {len(r['untracked'])}건 "
              f"(재실행 시 중복 계산됨, 데이터 손실은 아님)")
    if r["bad_len"]:
        ok = False
        print(f"\n! 포인트 수가 다른 조건: {len(r['bad_len'])}건 {list(r['bad_len'])[:5]}")

    if ok and not r["untracked"]:
        print("\n정상 — 손실·중복 없음")
        return 0

    if args.repair and r["missing"]:
        path = completed_path(run_dir)
        drop = set(r["missing"])
        kept = [ln for ln in path.read_text(encoding="utf-8").splitlines()
                if ln.strip() and json.loads(ln)["cond_id"] not in drop]
        backup = path.with_suffix(".jsonl.bak")
        path.rename(backup)
        path.write_text("\n".join(kept) + "\n", encoding="utf-8")
        print(f"\n복구: 완료표시 {len(drop)}건 제거 (백업 {backup.name})")
        print("  이제 같은 명령에 --resume 을 붙여 재실행하면 그 조건만 다시 계산됩니다.")
    elif r["missing"]:
        print("\n복구하려면 --repair 를 붙여 다시 실행하세요.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

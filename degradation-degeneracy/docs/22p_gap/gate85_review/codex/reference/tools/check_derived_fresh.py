"""check_derived_fresh.py — 보관 전 **파생 산출물 의미 동치** 게이트.

★ 18차 발견 6 — `payload_sha256.yaml` 은 stale bytes 도 충실히 해시한다.
바이트 보존은 파생 파일이 **봉인 fits 에서 재계산한 최신 의미**를 담는지
증명하지 못한다. 실제로 v4 묶음의 `objective_comparison.yaml` 은 경계 규약
수정(17차 발견 1) 이전 값(`36/98`, `90.0`)을 그대로 갖고 있었고, 모든 무결성
검사를 통과했다.

이 게이트는 봉인 fits 에서 파생을 다시 계산해 숫자를 대조하고, 다르면
**보관을 실패시킨다**. `scripts/archive_results.sh` 가 승격 직전에 호출한다.

    python -m tools.check_derived_fresh results/grid_fit_v4

exit 0 = 파생이 최신 의미다. nonzero = stale (승격 금지).
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="파생 산출물 의미 동치 게이트")
    ap.add_argument("run_dir")
    ap.add_argument("--tol", type=float, default=0.02)
    args = ap.parse_args()

    run = Path(args.run_dir)
    if not (run / "objective_comparison.yaml").is_file():
        # 파생이 아예 없는 artifact(곡선 producer 등)는 이 게이트 대상이 아니다
        print(f"  파생 없음 — 건너뜀: {run}")
        return 0

    from tools.compare_objectives import verify_derived_freshness
    res = verify_derived_freshness(run, tol=args.tol)
    if res["ok"]:
        print(f"  파생 semantic freshness: 통과 ({run})")
        return 0
    print(f"  파생 semantic freshness: 실패 ({run})")
    for w in res["fail"]:
        print(f"    - {w}")
    print("  → 봉인 fits 에서 score → compare 를 다시 돌린 뒤 보관하세요.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

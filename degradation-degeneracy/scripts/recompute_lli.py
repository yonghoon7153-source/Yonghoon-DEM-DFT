#!/usr/bin/env python3
"""recompute_lli.py — 이미 만들어진 fits.parquet의 LLI 열만 다시 계산한다.

fitting은 α·β를 저장하므로 LLI 환산식이 바뀌어도 **재fitting이 필요 없다.**
(3,069조건 재fitting 50분 → 후처리 수 초)

사용:
    python scripts/recompute_lli.py results/grid_fine_v1
    python scripts/recompute_lli.py results/grid_fine_v1 --in-dir results/grid_fine_v1
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from src.config import load_config  # noqa: E402
from src.inventory import reference_inventory  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="fits.parquet의 LLI 열 재계산")
    ap.add_argument("run_dir", help="fits.parquet 이 있는 디렉터리")
    ap.add_argument("--curves-dir", default=None,
                    help="reference 용량을 읽을 grid 결과 (기본: run_dir)")
    ap.add_argument("--base-config", default="configs/base.yaml")
    args = ap.parse_args()

    run_dir = Path(args.run_dir)
    fits_path = run_dir / "fits.parquet"
    if not fits_path.exists():
        raise SystemExit(f"fits.parquet 없음: {fits_path}")
    f = pd.read_parquet(fits_path)

    # reference 용량 [Ah] — r = Q/Q_ref 이므로 q_mah/r 로 복원 가능
    q_ref_ah = float((f["q_mah"] / f["r"]).median()) / 1000.0

    inv = reference_inventory(load_config(args.base_config), q_ref_ah)
    print(f"reference 용량 {q_ref_ah*1000:.1f} mAh")
    print(f"환산 상수: w_PE={inv.w_pe:.4f}  w_NE={inv.w_ne:.4f}  κ={inv.kappa:.4f}")

    r = f["r"].to_numpy()
    a_pe, b_pe = f["a_pe"].to_numpy(), f["b_pe"].to_numpy()
    a_ne, b_ne = f["a_ne"].to_numpy(), f["b_ne"].to_numpy()

    old = f["lli_hat"].to_numpy().copy()
    f["lli_hat"] = 1.0 - r * (inv.w_pe * a_pe + inv.w_ne * a_ne
                              + inv.kappa * (b_ne - b_pe))
    f["lli_hat_21p"] = 1.0 - (a_pe + b_pe - b_ne) * r
    f["lli_hat_code"] = (1.0 - a_pe) + (b_pe - b_ne)
    f["lam_pe_hat"] = 1.0 - a_pe * r
    f["lam_ne_hat"] = 1.0 - a_ne * r

    backup = fits_path.with_suffix(".parquet.bak")
    if not backup.exists():
        fits_path.rename(backup)
        print(f"원본 백업: {backup.name}")
    f.to_parquet(fits_path, index=False)

    print(f"\nLLI 열 갱신 완료 ({len(f)}행). 이전 값과 평균 차이 "
          f"{np.abs(f['lli_hat'].to_numpy() - old).mean():.4f}")
    if "lli" in f.columns:      # 합성 데이터면 정답과 대조까지
        for col, name in (("lli_hat", "유도식"), ("lli_hat_21p", "21p 식"),
                          ("lli_hat_code", "원본 코드")):
            err = (f[col] - f["lli"]).abs()
            print(f"  {name:8s} |오차| 평균 {err.mean():.4f}  최대 {err.max():.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

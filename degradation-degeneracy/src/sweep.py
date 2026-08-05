"""sweep.py — 1D sweep (32p 재현).

원본의 5개 모드 + reference를 모드별 원본 프로토콜 매핑 그대로 실행한다.
출력: curves.parquet (long format) + figures/32p_reproduction.png
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from src.baseline import get_discharged_state
from src.config import config_hash, load_config, validate_config
from src.curves import extract_curves
from src.io import base_manifest, write_manifest
from src.modes import Baseline, single_mode_overrides
from src.protocol import protocol_name_for_mode
from src.runner import make_solver, run_one, solver_name

log = logging.getLogger(__name__)


def run_sweep1d(cfg: dict, out_dir: str | Path) -> pd.DataFrame:
    """모드별 1D sweep 실행 → long format DataFrame + parquet 저장."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    values = list(cfg["sweep1d"]["values"])
    modes = list(cfg["sweep1d"]["modes"])
    n_trim = int(cfg["postprocess"]["n_trim"])
    n_interp = int(cfg["postprocess"]["n_interp"])

    b = Baseline.from_config(cfg)
    d = get_discharged_state(cfg)
    solver = make_solver(cfg)

    # ── reference 먼저 (Q_ref 산출 — 원본과 동일하게 전 모드 정규화 기준) ──
    ref_protocol = protocol_name_for_mode(cfg, "reference")
    ref = run_one(cfg, None, ref_protocol, solver=solver)
    if not ref.ok:
        raise RuntimeError(f"reference solve 실패: {ref.error}")
    ref_curves = extract_curves(ref.solution, n_trim, n_interp)
    q_ref = ref_curves["q_mah"]
    log.info("Reference Q_ref = %.1f mAh (%.1f s)", q_ref, ref.elapsed_s)

    records: list[pd.DataFrame] = []
    failed: list[tuple] = []

    def _append(mode: str, value: float, curves: dict) -> None:
        n = len(curves["x_norm"])
        records.append(pd.DataFrame({
            "mode": [mode] * n,
            "value": [value] * n,
            "protocol": [protocol_name_for_mode(cfg, mode)] * n,
            "q_mah": [curves["q_mah"]] * n,
            "x_norm": curves["x_norm"],
            "v_pe": curves["v_pe"],
            "v_ne": curves["v_ne"],
            "v_full": curves["v_full"],
        }))

    _append("reference", 0.0, ref_curves)

    for mode in modes:
        if mode == "reference":
            continue
        protocol = protocol_name_for_mode(cfg, mode)
        for v in values:
            ov = single_mode_overrides(mode, float(v), b, d)
            res = run_one(cfg, ov, protocol, solver=solver)
            if not res.ok:
                log.warning("실패: %s=%s → %s", mode, v, res.error)
                failed.append((mode, v, res.error))
                continue
            curves = extract_curves(res.solution, n_trim, n_interp, q_ref_mah=q_ref)
            _append(mode, float(v), curves)
            log.info("%s=%s: Q=%.1f mAh (%.1f s)", mode, v, curves["q_mah"], res.elapsed_s)

    df = pd.concat(records, ignore_index=True)
    df.to_parquet(out_dir / "curves.parquet", index=False)

    write_manifest(out_dir, base_manifest(config_hash(cfg), extra={
        "run_type": "sweep1d",
        "values": values,
        "modes": modes,
        "q_ref_mah": float(q_ref),
        "solver": solver_name(solver),
        "discharged_state": {
            "ne_primary": d.ne_primary, "ne_secondary": d.ne_secondary, "pe": d.pe,
        },
        "n_failed": len(failed),
        "failed": [f"{m}={v}: {e}" for m, v, e in failed],
    }))
    return df


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="1D sweep — 32p 재현")
    ap.add_argument("--config", default="configs/sweep1d.yaml")
    ap.add_argument("--out", required=True)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = load_config(args.config)
    validate_config(cfg)
    df = run_sweep1d(cfg, args.out)

    from tools.plot_sweep1d import plot_sweep1d
    fig_path = Path(args.out) / "figures" / "32p_reproduction.png"
    plot_sweep1d(df, fig_path)
    print(f"저장: {args.out}/curves.parquet, {fig_path}")


if __name__ == "__main__":
    main()

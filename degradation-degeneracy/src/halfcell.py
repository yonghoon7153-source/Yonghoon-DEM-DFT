"""halfcell.py — full-range half-cell OCV 기준 곡선 추출.

────────────────────────────────────────────────────────────────────────
왜 필요한가 ★

지금까지 fitting의 reference는 **기준 셀이 실제로 지나간 구간**(4.2/2.5 V,
0.05C)만 담고 있었다. 그러면 두 가지 문제가 생긴다.

  1) α<1인 조건은 재구성 창이 reference 범위를 넘어서 원리적으로 복원 불가
     (33p의 lb=1.00을 풀어줘도 같은 하한이 사실상 존재)
  2) α·β → 리튬량 환산에 셀별 상수(w_PE, w_NE, κ)가 필요해지고,
     22p가 쓴 "provided half-cell OCV" 기준과 달라진다

22p는 별도 측정한 half-cell OCV를 기준으로 fitting했다. 같은 성격의 기준을
쓰려면 **전극 자체 화학량론에 대한 OCP 곡선**이 필요하다.

이 모듈은 넓은 전압창(기본 2.0~4.4 V)·저율(0.02C) 시뮬레이션 1회로 그것을 뽑는다.
전극 전위를 그 전극의 화학량론에 짝지어 저장하므로, 결과는 셀 용량 정규화와
무관한 **half-cell OCV 테이블**이다.

실측 확보 범위 (Chen2020_composite baseline):
    PE  y = 0.251 ~ 0.928   (U 3.545 ~ 4.338 V)
    NE  z = 0.001 ~ 0.998   (U -0.053 ~ 1.275 V)   ← 사실상 전 범위

NE가 전 범위인 이유는 이 셀이 음극 제한이라 흑연이 먼저 바닥·천장에 닿기 때문이고,
PE가 0.25 아래로 못 가는 것도 같은 이유다 (진짜 반쪽셀이라야 그 아래가 나온다).
그래도 기존 기준보다 훨씬 넓어 α<1 영역을 덮는다.
────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.config import baseline_hash

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class HalfCellReference:
    """전극 화학량론 대비 OCP 테이블 (오름차순 정렬)."""

    y_pe: np.ndarray        # 양극 화학량론 (리튬 분율)
    u_pe: np.ndarray        # 양극 OCP [V]
    z_ne: np.ndarray        # 음극 화학량론 (Gr+Si 가중 평균)
    u_ne: np.ndarray        # 음극 bulk OCP [V]

    def as_dict(self) -> dict:
        return {"y_pe": self.y_pe.tolist(), "u_pe": self.u_pe.tolist(),
                "z_ne": self.z_ne.tolist(), "u_ne": self.u_ne.tolist()}

    @classmethod
    def from_dict(cls, d: dict) -> "HalfCellReference":
        return cls(*(np.asarray(d[k], float) for k in ("y_pe", "u_pe", "z_ne", "u_ne")))

    def coverage(self) -> dict:
        return {"pe_min": float(self.y_pe.min()), "pe_max": float(self.y_pe.max()),
                "ne_min": float(self.z_ne.min()), "ne_max": float(self.z_ne.max())}


def _dedupe_sorted(x: np.ndarray, y: np.ndarray) -> tuple:
    """화학량론 오름차순 + 중복 제거 (보간자를 만들 수 있게)."""
    order = np.argsort(x)
    x, y = x[order], y[order]
    keep = np.concatenate([[True], np.diff(x) > 1e-9])
    return x[keep], y[keep]


def compute_halfcell_reference(cfg: dict, v_lo: float = 2.0, v_hi: float = 4.4,
                               c_rate: float = 0.02) -> HalfCellReference:
    """넓은 전압창 저율 사이클 1회로 half-cell OCV 테이블을 만든다."""
    import pybamm

    from src.model import build_model
    from src.runner import build_param, make_solver

    b = cfg["baseline"]
    model = build_model(cfg)
    param = build_param(cfg, {"Upper voltage cut-off [V]": v_hi,
                              "Lower voltage cut-off [V]": v_lo})
    # ★ 충전 먼저 → 마지막 **방전 스텝만** 쓴다.
    #   NE가 composite(current sigmoid 히스테리시스)라 충전·방전 가지의 OCP가 다르다.
    #   두 가지를 한 테이블에 섞으면 같은 화학량론에 값이 두 개가 되어
    #   기준 곡선이 망가진다 (실측: β_NE가 bound까지 달아나고 LAM 오차 0.10).
    #   grid 곡선도 최종 방전 스텝에서 추출하므로 가지를 맞춘다.
    exp = pybamm.Experiment([
        f"Charge at {c_rate}C until {v_hi}V",
        "Rest for 30 minutes",
        f"Discharge at {c_rate}C until {v_lo}V",
    ])
    sol = pybamm.Simulation(model, parameter_values=param, experiment=exp,
                            solver=make_solver(cfg)).solve()

    ys, us_pe, zs, us_ne = [], [], [], []
    for step in sol.cycles[-1].steps[-1:]:      # 최종 방전 스텝만
        c_pe = step["Average positive particle concentration [mol.m-3]"].entries
        c_gr = step["Average negative primary particle concentration [mol.m-3]"].entries
        c_si = step["Average negative secondary particle concentration [mol.m-3]"].entries
        ys.append(c_pe / b["pe_max_conc"])
        us_pe.append(step["X-averaged positive electrode open-circuit potential [V]"].entries)
        # NE는 2상 복합 — 용량 가중 평균 화학량론
        num = c_gr * b["ne_primary_vf"] + c_si * b["ne_secondary_vf"]
        den = (b["ne_primary_max_conc"] * b["ne_primary_vf"]
               + b["ne_secondary_max_conc"] * b["ne_secondary_vf"])
        zs.append(num / den)
        us_ne.append(step["Battery negative electrode bulk open-circuit potential [V]"].entries)

    y, u_p = _dedupe_sorted(np.concatenate(ys), np.concatenate(us_pe))
    z, u_n = _dedupe_sorted(np.concatenate(zs), np.concatenate(us_ne))
    ref = HalfCellReference(y_pe=y, u_pe=u_p, z_ne=z, u_ne=u_n)
    log.info("half-cell 기준 확보: PE y %.3f~%.3f (%d점), NE z %.3f~%.3f (%d점)",
             y.min(), y.max(), len(y), z.min(), z.max(), len(z))
    return ref


def get_halfcell_reference(cfg: dict, cache_dir: str | Path | None = None,
                           force: bool = False, **kw) -> HalfCellReference:
    """baseline 해시 키 캐시 → 미스 시 계산 (완방상태와 같은 정책)."""
    root = Path(cfg.get("_config_path", ".")).resolve().parent.parent
    d = Path(cache_dir) if cache_dir else root / ".cache" / "halfcell"
    path = d / f"{baseline_hash(cfg)}.json"

    if not force and path.exists():
        log.info("half-cell 기준 캐시 적중: %s", path)
        return HalfCellReference.from_dict(json.loads(path.read_text(encoding="utf-8")))

    ref = compute_halfcell_reference(cfg, **kw)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ref.as_dict()), encoding="utf-8")
    log.info("half-cell 기준 캐시 저장: %s", path)
    return ref


def main() -> None:
    import argparse

    from src.config import load_config, validate_config

    ap = argparse.ArgumentParser(description="full-range half-cell OCV 기준 추출")
    ap.add_argument("--config", default="configs/base.yaml")
    ap.add_argument("--v-lo", type=float, default=2.0)
    ap.add_argument("--v-hi", type=float, default=4.4)
    ap.add_argument("--c-rate", type=float, default=0.02)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--plot", default=None, help="곡선 그림 저장 경로")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = load_config(args.config)
    validate_config(cfg)
    ref = get_halfcell_reference(cfg, force=args.force, v_lo=args.v_lo,
                                 v_hi=args.v_hi, c_rate=args.c_rate)
    print(json.dumps(ref.coverage(), indent=2))

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
        ax[0].plot(ref.y_pe, ref.u_pe, "b-"); ax[0].set_title("PE half-cell OCV")
        ax[0].set_xlabel("PE stoichiometry y"); ax[0].set_ylabel("U [V]")
        ax[1].plot(ref.z_ne, ref.u_ne, "r-"); ax[1].set_title("NE half-cell OCV")
        ax[1].set_xlabel("NE stoichiometry z"); ax[1].set_ylabel("U [V]")
        for a in ax:
            a.grid(alpha=0.3)
        out = Path(args.plot); out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out, dpi=150)
        print(f"그림 저장: {out}")


if __name__ == "__main__":
    main()

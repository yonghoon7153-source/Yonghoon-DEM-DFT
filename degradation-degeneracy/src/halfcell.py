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

두 가지 방법을 제공한다.

  method="ocp" (기본, 권장) — 파라미터셋의 OCP 함수를 직접 평가.
      **화학량론 0~1 전 범위**를 얻는다. 복합 음극은 평형 조건으로 Gr·Si를 분배.
  method="sim"              — 넓은 전압창 시뮬레이션에서 추출.
      셀이 실제 지나간 구간만 (PE y 0.251~0.928) → 전 범위가 아니다.

검증: 두 방법을 겹치는 구간에서 비교하면
    PE 평균차 1.7 mV (최대 4.7)
    NE 평균차 3.8 mV (z 0.02~0.98 구간; 끝단은 흑연 OCP 발산으로 큼)
→ OCP 함수 평가가 시뮬레이션 결과를 정확히 재현한다.

★ 이 기준으로 fitting하면 α·β가 논문 규약의 의미를 정확히 갖는다.
  기준 조건 자체를 fitting한 결과가 그 증거다:
      α_PE,ini = 1.465  →  셀이 PE 전 범위의 1/1.465 = 68.3% 사용
                           (시뮬레이션 관측 0.251~0.928 = 67.7%와 일치)
      β_PE,ini = -0.395 →  x=0에서 y = 0.395/1.465 = 0.270
                           (baseline 17038/63104 = 0.270과 일치)
      α_NE,ini = 1.029  →  NE는 전 범위의 97% 사용 (관측과 일치)
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


def _eval_ocp(fn, xs: np.ndarray) -> np.ndarray:
    """pybamm OCP 함수를 점별 평가. (흑연 OCP는 심볼 연산이라 배열 입력 불가)"""
    import pybamm

    out = []
    for xi in xs:
        r = fn(pybamm.Scalar(float(xi)))
        r = r.evaluate() if hasattr(r, "evaluate") else r
        out.append(float(np.asarray(r).ravel()[0]))
    return np.asarray(out)


def compute_halfcell_from_ocp(cfg: dict, n_points: int = 400,
                              branch: str = "delithiation") -> HalfCellReference:
    """★ 진짜 full-range half-cell OCV — 파라미터셋의 OCP 함수를 직접 평가한다.

    시뮬레이션 추출본은 셀이 실제로 지나간 구간(PE y 0.251~0.928)만 담지만,
    OCP 함수는 화학량론 0~1 전 범위를 준다. 22p가 쓴 "provided half-cell OCV"와
    같은 성격이며, 이래야 α·β가 논문 규약의 의미를 정확히 갖는다.

    복합 음극(Gr+Si)은 **평형 조건**으로 푼다:
      같은 전위 U에서 U_gr(x_gr) = U_si(x_si) = U 이므로 각 OCP를 역보간해
      x_gr(U), x_si(U)를 얻고, 용량 가중 평균으로 z(U)를 만든다.
        z = (Q_gr·x_gr + Q_si·x_si)/(Q_gr + Q_si),  Q = c_max·vf
      (이 baseline에서 Gr 83.5%, Si 16.5%)

    branch: Si는 히스테리시스가 있어 가지를 골라야 한다. grid 곡선이 최종 방전
            스텝에서 추출되므로 기본값은 "delithiation"(방전 중 음극은 탈리튬화).
    """
    import pybamm

    b = cfg["baseline"]
    p = pybamm.ParameterValues(cfg["parameter_set"])
    x = np.linspace(1e-4, 1 - 1e-4, n_points)

    # ── 양극: 화학량론 그대로 ──
    u_pe = _eval_ocp(p["Positive electrode OCP [V]"], x)

    # ── 음극: Gr·Si 평형 분배 ──
    si_key = {"delithiation": "Secondary: Negative electrode delithiation OCP [V]",
              "lithiation": "Secondary: Negative electrode lithiation OCP [V]",
              "mean": "Secondary: Negative electrode OCP [V]"}[branch]
    u_gr = _eval_ocp(p["Primary: Negative electrode OCP [V]"], x)
    u_si = _eval_ocp(p[si_key], x)

    q_gr = b["ne_primary_max_conc"] * b["ne_primary_vf"]
    q_si = b["ne_secondary_max_conc"] * b["ne_secondary_vf"]

    u_grid = np.linspace(min(u_gr.min(), u_si.min()), max(u_gr.max(), u_si.max()),
                         n_points * 2)
    # OCP는 단조감소 → 역보간 위해 뒤집는다. 범위 밖은 포화(0 또는 1).
    x_gr = np.interp(u_grid, u_gr[::-1], x[::-1], left=1.0, right=0.0)
    x_si = np.interp(u_grid, u_si[::-1], x[::-1], left=1.0, right=0.0)
    z = (q_gr * x_gr + q_si * x_si) / (q_gr + q_si)

    y_s, u_p = _dedupe_sorted(x, u_pe)
    z_s, u_n = _dedupe_sorted(z, u_grid)
    ref = HalfCellReference(y_pe=y_s, u_pe=u_p, z_ne=z_s, u_ne=u_n)
    log.info("half-cell(OCP 함수) 기준: PE y %.4f~%.4f, NE z %.4f~%.4f (Si 가지=%s)",
             y_s.min(), y_s.max(), z_s.min(), z_s.max(), branch)
    return ref


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


#: ★ F64 — **결과를 바꾸는** 생성 인자. 캐시 키와 meta 에 모두 들어가야 한다.
#:   기본값은 `compute_halfcell_from_ocp` / `compute_halfcell_reference` 시그니처와
#:   일치해야 하며, 여기 없는 인자를 추가하면 그 인자는 서명에서 빠진다.
RECIPE_DEFAULTS = {
    "ocp": {"n_points": 400, "branch": "delithiation"},
    "sim": {"v_lo": 2.0, "v_hi": 4.4, "c_rate": 0.02},
}


def recipe_of(method: str = "ocp", **kw) -> dict:
    """생성 인자를 기본값과 합쳐 **완전한** recipe 로 만든다."""
    if method not in RECIPE_DEFAULTS:
        raise ValueError(f"알 수 없는 method: {method} (가능: {list(RECIPE_DEFAULTS)})")
    r = dict(RECIPE_DEFAULTS[method])
    unknown = set(kw) - set(r)
    if unknown:
        # 조용히 무시하면 "서명에 없는데 결과는 바뀌는" 인자가 생긴다
        raise ValueError(f"method={method}가 모르는 인자: {sorted(unknown)}")
    r.update({k: v for k, v in kw.items() if v is not None})
    return {"method": method, **r}


def recipe_hash(cfg: dict, method: str = "ocp", **kw) -> str:
    """baseline + recipe 를 함께 해시한다 (★ F64)."""
    import hashlib

    payload = {"baseline": baseline_hash(cfg), "recipe": recipe_of(method, **kw)}
    return hashlib.sha1(
        json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:12]


def halfcell_cache_path(cfg: dict, cache_dir: str | Path | None = None,
                        method: str = "ocp", **kw) -> Path:
    """★ F45 — 실제로 쓰이는 캐시 경로. 서명·manifest가 이걸 그대로 써야 한다.

    한때 fitting이 현재 작업 디렉터리의 `.cache/halfcell/*_ocp.json` 을 glob 했다.
    실제 경로는 base config의 `_config_path` 에서 저장소 root 를 계산해 고른
    **하나**이므로, 다른 작업 디렉터리나 외부 --base-config 를 쓰면 실제 사용
    캐시가 서명에서 빠지고, 반대로 무관한 캐시까지 서명에 들어가 resume 을
    불필요하게 막았다.

    ★ F64 — 키에 **recipe 해시**를 넣는다. 예전 키는 `baseline_hash + method`
    뿐이라 `branch`(Si 히스테리시스 가지)나 `n_points` 가 달라도 같은 경로였다.
    그래서 다른 recipe 로 만든 곡선을 같은 경로에 미리 넣어두면 fitting 이 그걸
    쓰고도 검증을 통과했다 — 실측으로 `p_ini[pocv]` 가
    `[1.343, -0.325, 2.429, -0.100]` → `[1.628, -0.404, 1.500, -0.410]` 로 움직였다.
    좌표 원점이 바뀌므로 Case 1 의 모든 수치가 따라 바뀐다.
    """
    root = Path(cfg.get("_config_path", ".")).resolve().parent.parent
    d = Path(cache_dir) if cache_dir else root / ".cache" / "halfcell"
    return d / f"{baseline_hash(cfg)}_{method}_{recipe_hash(cfg, method, **kw)}.json"


def halfcell_meta_path(path: str | Path) -> Path:
    """캐시 JSON 옆의 recipe 기록 파일. 캐시와 함께 봉인된다."""
    p = Path(path)
    return p.with_name(p.stem + ".meta.yaml")


def get_halfcell_reference(cfg: dict, cache_dir: str | Path | None = None,
                           force: bool = False, method: str = "ocp",
                           **kw) -> HalfCellReference:
    """baseline+recipe 해시 키 캐시 → 미스 시 계산 (완방상태와 같은 정책).

    method: "ocp" (기본) — 파라미터셋 OCP 함수 직접 평가, 화학량론 전 범위
            "sim"        — 넓은 전압창 시뮬레이션 추출 (셀이 지나간 구간만)

    ★ F64 — 생성 시 `*.meta.yaml` 에 recipe·생성 코드·환경을 같이 남긴다.
      배열 네 개만 저장하면 "이 숫자가 어떤 recipe 에서 나왔는가"를 파일만
      보고 알 수 없고, 그러면 캐시를 바꿔치기해도 아무도 모른다.
    """
    import yaml

    from src.io import env_fingerprint, source_digest

    path = halfcell_cache_path(cfg, cache_dir, method, **kw)
    recipe = recipe_of(method, **kw)

    if not force and path.exists():
        log.info("half-cell 기준 캐시 적중: %s", path)
        return HalfCellReference.from_dict(json.loads(path.read_text(encoding="utf-8")))

    ref = (compute_halfcell_from_ocp(cfg, **kw) if method == "ocp"
           else compute_halfcell_reference(cfg, **kw))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ref.as_dict()), encoding="utf-8")
    halfcell_meta_path(path).write_text(yaml.safe_dump({
        "recipe": recipe,
        "baseline_hash": baseline_hash(cfg),
        "recipe_hash": recipe_hash(cfg, method, **kw),
        "parameter_set": cfg.get("parameter_set"),
        "source_digest": source_digest(),
        "env": env_fingerprint(),
        "coverage": ref.coverage(),
        "cache_file": path.name,
    }, allow_unicode=True, sort_keys=False), encoding="utf-8")
    log.info("half-cell 기준 캐시 저장: %s (recipe %s)", path, recipe)
    return ref


def main() -> None:
    import argparse

    from src.config import load_config, validate_config

    ap = argparse.ArgumentParser(description="full-range half-cell OCV 기준 추출")
    ap.add_argument("--config", default="configs/base.yaml")
    ap.add_argument("--v-lo", type=float, default=2.0)
    ap.add_argument("--v-hi", type=float, default=4.4)
    ap.add_argument("--c-rate", type=float, default=0.02)
    ap.add_argument("--method", default="ocp", choices=["ocp", "sim"],
                    help="ocp=OCP 함수 직접 평가(전 범위) | sim=시뮬레이션 추출")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--plot", default=None, help="곡선 그림 저장 경로")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = load_config(args.config)
    validate_config(cfg)
    kw = ({} if args.method == "ocp"
          else {"v_lo": args.v_lo, "v_hi": args.v_hi, "c_rate": args.c_rate})
    ref = get_halfcell_reference(cfg, force=args.force, method=args.method, **kw)
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

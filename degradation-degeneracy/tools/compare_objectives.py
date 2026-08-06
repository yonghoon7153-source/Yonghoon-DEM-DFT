"""compare_objectives.py — 목적함수 4종 비교 (Phase 6). ★ 최종 산출물

같은 격자·같은 정답에 대해 pocv / pocv_dvdq / pocv_dvdq_dqdv / dqdv_only 를
적용했을 때 degeneracy가 얼마나 줄어드는지를 표 하나로 만든다.
"dQ/dV를 넣으면 X% → Y%로 준다"의 X와 Y가 여기서 나온다.

리뷰 규칙이 표의 형태를 결정한다
──────────────────────────────
F1  복원가능군(α_true≥1)에서만 센다. 복원불가군을 섞으면 모든 목적함수가
    똑같이 나빠 보여 정작 비교하려는 차이가 묻힌다. 제외 비율은 따로 명시.
F5  방법 바이어스를 뺀 보정 판정을 **같은 표에** 나란히 둔다. 둘 중
    유리한 쪽만 고르는 일이 없도록.
F10 노이즈 수준별로 쪼갠 표를 함께 낸다. dQ/dV의 이점은 노이즈에서
    희석되므로 노이즈 0 결과만 보면 과대평가된다.
F4  restart 기반 지표(불일치율)는 여기 넣지 않는다. 조건마다 restart 수가
    달라 목적함수 간 비교가 성립하지 않는다.
F14 저LLI·고LAM_PE 코너 공백을 각주로 붙인다.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# run.sh 없이 직접 실행해도 src/tools를 찾도록 (PYTHONPATH 미설정 대비)
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

log = logging.getLogger(__name__)

# 34p 순서 — 항이 하나씩 쌓이는 순서로 보여야 개선 효과가 읽힌다
OBJ_ORDER = ["pocv", "pocv_dvdq", "pocv_dvdq_dqdv", "dqdv_only"]
OBJ_LABEL = {
    "pocv": "pOCV only",
    "pocv_dvdq": "pOCV + dV/dQ  (33p 기존)",
    "pocv_dvdq_dqdv": "pOCV + dV/dQ + dQ/dV  (34p 개선)",
    "dqdv_only": "dQ/dV only",
}
EXP_22P = {"lam_pe": 0.13, "lam_ne": 0.13, "lli": 0.17}


def _order(objs) -> list:
    known = [o for o in OBJ_ORDER if o in set(objs)]
    return known + sorted(set(objs) - set(known))


# ---------------------------------------------------------------- 표

def comparison_table(df: pd.DataFrame, by_noise: bool = False) -> pd.DataFrame:
    """목적함수별 핵심 지표. F1에 따라 복원가능군만."""
    rec = df[df["recoverable"]] if "recoverable" in df.columns else df
    keys = ["objective"] + (["noise"] if by_noise and "noise" in rec.columns else [])
    rows = []
    for key, g in rec.groupby(keys):
        o = key[0] if isinstance(key, tuple) else key
        row = {"objective": o}
        if isinstance(key, tuple) and len(key) > 1:
            row["noise"] = key[1]
        row.update({
            "n": int(len(g)),
            "degenerate_frac": float(g["degenerate"].mean()),
            "degenerate_frac_corrected": float(g["degenerate_corrected"].mean())
            if "degenerate_corrected" in g.columns else np.nan,
            "mean_abs_err": float(g["abs_err_max"].mean()),
            "mean_abs_err_lam_pe": float(g["err_lam_pe"].abs().mean()),
            "mean_abs_err_lam_ne": float(g["err_lam_ne"].abs().mean()),
            "mean_abs_err_lli": float(g["err_lli"].abs().mean()),
            "pe_ne_antisym_frac": float(g["pe_ne_antisym"].mean()),
            "alpha_wall_frac": float(g["alpha_wall_any"].mean())
            if "alpha_wall_any" in g.columns else np.nan,
        })
        rows.append(row)
    out = pd.DataFrame(rows)
    out["_ord"] = out["objective"].map({o: i for i, o in enumerate(_order(out["objective"]))})
    sort_by = ["_ord"] + (["noise"] if "noise" in out.columns else [])
    return out.sort_values(sort_by).drop(columns="_ord").reset_index(drop=True)


def to_markdown(tbl: pd.DataFrame) -> str:
    """04_PROMPTS.md Phase 6이 요구한 형태의 마크다운 표."""
    has_noise = "noise" in tbl.columns
    head = ("| objective |" + (" noise |" if has_noise else "")
            + " n | degeneracy | (바이어스 보정) | 평균 \\|err\\| | PE-NE 상쇄 |")
    sep = "|---|" + ("---|" if has_noise else "") + "---|---|---|---|---|"
    lines = [head, sep]
    for _, r in tbl.iterrows():
        label = OBJ_LABEL.get(r["objective"], r["objective"])
        cells = [label]
        if has_noise:
            cells.append(f"{r['noise']:g}")
        corr = ("—" if pd.isna(r["degenerate_frac_corrected"])
                else f"{100 * r['degenerate_frac_corrected']:.0f}%")
        cells += [f"{r['n']:d}", f"{100 * r['degenerate_frac']:.0f}%", corr,
                  f"{100 * r['mean_abs_err']:.1f}%p",
                  f"{100 * r['pe_ne_antisym_frac']:.0f}%"]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------- 22p 판정

def verdict_22p(df: pd.DataFrame, objective: str = "pocv_dvdq",
                noise: float = 0.0, radius: float = 0.021) -> dict:
    """22p 실험 조건(LAM_PE≈LAM_NE≈13%, LLI≈17%) 근방의 복원 성적.

    ★ 이 프로젝트의 질문에 직접 답하는 함수다.
    격자 간격이 0.02이므로 반경 0.021이면 인접 격자점까지 포함한다.
    """
    sub = df[df["objective"] == objective]
    if "noise" in sub.columns:
        sub = sub[sub["noise"] == noise]
    if sub.empty:
        return {"error": f"조건 없음 (objective={objective}, noise={noise})"}

    d = np.sqrt(sum((sub[k] - v) ** 2 for k, v in EXP_22P.items()))
    near = sub[d <= radius]
    if near.empty:                       # 격자에 정확히 없으면 최근접 1점
        near = sub.loc[[d.idxmin()]]

    rec = bool(near["recoverable"].all()) if "recoverable" in near.columns else True
    out = {
        "objective": objective, "noise": noise,
        "n_near": int(len(near)),
        "nearest_distance": float(d.min()),
        "recoverable": rec,
        "degenerate_frac": float(near["degenerate"].mean()),
        "mean_abs_err": float(near["abs_err_max"].mean()),
        "mean_err_lam_pe": float(near["err_lam_pe"].mean()),
        "mean_err_lam_ne": float(near["err_lam_ne"].mean()),
        "mean_err_lli": float(near["err_lli"].mean()),
        "pe_ne_antisym_frac": float(near["pe_ne_antisym"].mean()),
        "recovered_pe_ne_gap": float(near["pe_ne_gap_recovered"].mean()),
        "true_pe_ne_gap": float(near["pe_ne_gap_true"].mean()),
    }
    if "degenerate_corrected" in near.columns:
        out["degenerate_frac_corrected"] = float(near["degenerate_corrected"].mean())
    return out


# ---------------------------------------------------------------- 격차 붕괴

def gap_analysis(df: pd.DataFrame, objective: str, noise: float | None = 0.0,
                 gap_thresh: float = 0.06, tol: float = 0.02) -> dict:
    """★ 22p 질문에 가장 직접적으로 답하는 지표.

    22p 근방 격자점은 참값이 애초에 LAM_PE = LAM_NE라서, 거기서 복원값이
    비슷하게 나오는 건 아무 증거가 못 된다. 물어야 할 것은 **반대 방향**이다.

      격차 붕괴(gap collapse)
        참값이 뚜렷이 다른데(|ΔLAM|_true ≥ gap_thresh)
        복원값은 같다고(|ΔLAM|_hat < tol) 말하는 비율.
        이 비율이 높으면 → 실측에서 LAM_PE ≈ LAM_NE가 나와도 **정보가 없다**.
        22p 결과를 물리로 읽을 근거가 사라진다.

      거짓 분리(false split)
        참값은 같은데(|ΔLAM|_true < tol) 복원값은 다르다고 말하는 비율.
        반대 방향 실패로, 격차 지표 자체의 신뢰도를 깎는다.

      shrinkage = mean(|ΔLAM|_hat / |ΔLAM|_true)
        1이면 격차를 그대로 복원, 0에 가까우면 전부 뭉갠다.

    gap_thresh 기본 0.06 = fine 격자 3칸. 참값 격차가 판정 기준(2%p)의
    3배는 돼야 "뚜렷이 다르다"고 말할 수 있다.
    """
    sub = df[df["objective"] == objective]
    if noise is not None and "noise" in sub.columns:
        sub = sub[sub["noise"] == noise]
    if "recoverable" in sub.columns:
        sub = sub[sub["recoverable"]]
    if sub.empty:
        return {"error": f"조건 없음 (objective={objective}, noise={noise})"}

    gt, gr = sub["pe_ne_gap_true"], sub["pe_ne_gap_recovered"]
    wide, same = sub[gt >= gap_thresh], sub[gt < tol]

    out = {
        "objective": objective, "noise": noise,
        "gap_thresh": gap_thresh, "tol": tol,
        "n_wide_gap_true": int(len(wide)),
        "n_zero_gap_true": int(len(same)),
    }
    if len(wide):
        w_gr = wide["pe_ne_gap_recovered"]
        out.update({
            # ★ 참값이 다른데 같다고 말하는 비율
            "gap_collapse_frac": float((w_gr < tol).mean()),
            "mean_true_gap_wide": float(wide["pe_ne_gap_true"].mean()),
            "mean_recovered_gap_wide": float(w_gr.mean()),
            "shrinkage": float((w_gr / wide["pe_ne_gap_true"]).mean()),
        })
    if len(same):
        out["false_split_frac"] = float(
            (same["pe_ne_gap_recovered"] >= tol).mean())
    return out


def plot_gap(df: pd.DataFrame, out_path, objective: str, noise: float = 0.0,
             tol: float = 0.02):
    """참 격차 vs 복원 격차 산점도. 대각선에서 아래로 눌리면 격차 붕괴."""
    sub = df[df["objective"] == objective]
    if "noise" in sub.columns:
        sub = sub[sub["noise"] == noise]
    rec = sub[sub["recoverable"]] if "recoverable" in sub.columns else sub
    unrec = sub[~sub["recoverable"]] if "recoverable" in sub.columns else sub.iloc[:0]

    fig, ax = plt.subplots(figsize=(4.4, 4.2), constrained_layout=True)
    if len(unrec):
        ax.scatter(unrec["pe_ne_gap_true"], unrec["pe_ne_gap_recovered"],
                   s=10, c="0.8", marker="x", label="unrecoverable")
    ax.scatter(rec["pe_ne_gap_true"], rec["pe_ne_gap_recovered"],
               s=12, c="tab:blue", alpha=0.55, label="recoverable")
    lim = float(max(sub["pe_ne_gap_true"].max(), sub["pe_ne_gap_recovered"].max())) * 1.05
    ax.plot([0, lim], [0, lim], "k--", lw=1, label="perfect recovery")
    ax.axhspan(0, tol, color="tab:red", alpha=0.12)
    ax.text(lim * 0.98, tol * 0.5, "reported as equal", ha="right", va="center",
            fontsize=8, color="tab:red")
    ax.set_xlabel(r"true  $|LAM_{PE}-LAM_{NE}|$")
    ax.set_ylabel(r"recovered  $|LAM_{PE}-LAM_{NE}|$")
    ax.set_title(f"Electrode gap recovery — {objective}, noise={noise:g}", fontsize=10)
    ax.set_xlim(0, lim); ax.set_ylim(0, lim)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------- 그림

def plot_panel(df: pd.DataFrame, out_path, noise: float = 0.0,
               value: str = "abs_err_max", tol: float = 0.02):
    """같은 지도를 목적함수 4종에 대해 나란히. 색 스케일 공유가 핵심."""
    from tools.plot_map import EXP_22P as MARK

    sub = df[df["noise"] == noise] if "noise" in df.columns else df
    objs = _order(sub["objective"].unique())
    lli_vals = sorted(sub["lli"].unique())
    # LLI는 22p에 가장 가까운 한 면만 (4×11 패널은 못 읽는다)
    lli = min(lli_vals, key=lambda v: abs(v - MARK["lli"]))
    g0 = sub[sub["lli"] == lli]
    pe_vals, ne_vals = sorted(g0["lam_pe"].unique()), sorted(g0["lam_ne"].unique())
    vmax = float(np.nanpercentile(sub[value], 98))

    fig, axes = plt.subplots(1, len(objs), figsize=(3.0 * len(objs) + 1.6, 3.5),
                             sharey=True, constrained_layout=True)
    axes = np.atleast_1d(axes)
    im = None
    for ax, o in zip(axes, objs):
        g = g0[g0["objective"] == o]
        grid = np.full((len(ne_vals), len(pe_vals)), np.nan)
        unrec = np.zeros_like(grid, dtype=bool)
        for _, r in g.iterrows():
            i, j = ne_vals.index(r["lam_ne"]), pe_vals.index(r["lam_pe"])
            grid[i, j] = r[value]
            if "recoverable" in r and not r["recoverable"]:
                unrec[i, j] = True
        cmap = plt.get_cmap("RdYlGn_r").with_extremes(bad="0.85")
        im = ax.pcolormesh(pe_vals, ne_vals, np.ma.masked_invalid(grid),
                           cmap=cmap, vmin=0, vmax=vmax, shading="nearest")
        if unrec.any():
            ax.contourf(pe_vals, ne_vals, unrec.astype(float), levels=[0.5, 1.5],
                        colors="none", hatches=["///"], alpha=0)
        frac = g["degenerate"].mean() if len(g) else np.nan
        ax.set_title(f"{o}\ndegenerate {100 * frac:.0f}%", fontsize=9)
        ax.set_xlabel(r"LAM$_{PE}$")
        ax.plot(MARK["lam_pe"], MARK["lam_ne"], "*", ms=16, mfc="cyan",
                mec="k", mew=1.1, zorder=5)
    axes[0].set_ylabel(r"LAM$_{NE}$")
    cb = fig.colorbar(im, ax=axes, shrink=0.85)
    cb.set_label(value)
    fig.suptitle(f"Objective comparison — LLI = {lli:g}, noise = {noise:g}"
                 "    [star = 22p experiment · hatched = unrecoverable]",
                 y=1.06, fontsize=10)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_weight_curve(summary: pd.DataFrame, out_path,
                      metric: str = "degenerate_frac_corrected"):
    """w_dqdv sweep 곡선 — "튜닝 아니냐"에 대한 시각적 근거."""
    col = metric if metric in summary.columns else "degenerate_frac"
    fig, ax = plt.subplots(figsize=(5.2, 3.4), constrained_layout=True)
    for n, g in summary.groupby("noise"):
        g = g.sort_values("w_dqdv")
        ax.plot(g["w_dqdv"], 100 * g[col], "o-", ms=4, label=f"noise = {n:g} V")
    ax.axvline(1.0, color="0.6", ls=":", lw=1)
    ax.text(1.02, ax.get_ylim()[1], " default w=1", va="top", fontsize=8, color="0.4")
    ax.set_xlabel(r"$w_{dQ/dV}$")
    ax.set_ylabel(f"{col}  [%]")
    ax.set_title("dQ/dV weight sweep", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------- 실행

def run_compare(in_dir, out_dir=None, tol: float = 0.02) -> dict:
    import yaml

    in_dir = Path(in_dir)
    out_dir = Path(out_dir) if out_dir else in_dir
    map_path = in_dir / "degeneracy_map.parquet"
    if not map_path.exists():
        raise SystemExit(f"{map_path} 없음 — 먼저 ./run.sh --mode score --in {in_dir}")
    df = pd.read_parquet(map_path)

    tbl = comparison_table(df)
    tbl_noise = comparison_table(df, by_noise=True)
    tbl.to_csv(out_dir / "objective_comparison.csv", index=False)
    tbl_noise.to_csv(out_dir / "objective_comparison_by_noise.csv", index=False)

    objs = _order(df["objective"].unique())
    verdicts = {o: verdict_22p(df, o) for o in objs}
    gaps = {o: gap_analysis(df, o, tol=tol) for o in objs}

    figs = {}
    for o in objs:
        try:
            figs[f"gap_{o}"] = str(plot_gap(
                df, out_dir / "figures" / f"gap_recovery_{o}.png", o, tol=tol))
        except Exception as e:  # noqa: BLE001
            log.warning("격차 그림 실패 (%s): %s", o, e)
    for noise in (sorted(df["noise"].unique()) if "noise" in df.columns else [None]):
        try:
            figs[f"noise_{noise:g}"] = str(plot_panel(
                df, out_dir / "figures" / f"objective_panel_noise{noise:g}.png",
                noise, tol=tol))
        except Exception as e:  # noqa: BLE001
            log.warning("패널 그림 실패 (noise=%s): %s", noise, e)

    ws = in_dir / "wsweep" / "weight_sweep_summary.csv"
    if ws.exists():
        try:
            figs["weight_curve"] = str(plot_weight_curve(
                pd.read_csv(ws), out_dir / "figures" / "weight_sweep.png"))
        except Exception as e:  # noqa: BLE001
            log.warning("가중치 곡선 실패: %s", e)

    result = {"table": tbl.to_dict("records"),
              "table_by_noise": tbl_noise.to_dict("records"),
              "verdict_22p": verdicts, "gap_analysis": gaps, "figures": figs,
              "unrecoverable_frac": float(1 - df["recoverable"].mean())
              if "recoverable" in df.columns else 0.0}
    (out_dir / "objective_comparison.yaml").write_text(
        yaml.safe_dump(result, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8")

    print(to_markdown(tbl))
    return result


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="목적함수 4종 비교 (Phase 6)")
    ap.add_argument("--in", dest="in_dir", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--tol", type=float, default=0.02)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    run_compare(args.in_dir, args.out, args.tol)


if __name__ == "__main__":
    main()

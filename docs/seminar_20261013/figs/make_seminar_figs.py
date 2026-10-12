"""연구세미나 덱 (2026-10 · 1저자 비준 개요 v1) — 새로 그리는 그림 넷.

값은 전부 리포 정본에서 가져온다 (아래 SRC 주석).  철회값 (claims.json quotation_ban) 은 쓰지 않는다.
  F1 pipeline       파이프라인 흐름도 (DEM → MPM → voxel transport → electrochemistry) · 수치 없음
  F2 grid           복셀 전자 · 이온 전도도 비 vs 복셀 크기 — CL-24 공개값 (1.4215 · 1.1621 · 1.0849 / 1.0742 · 0.9926 · 0.9908)
  F3 sigma_e_exp    복셀 모델 σ_e ↔ DC 분극 실험 (SBE 54.0 ↔ 4.47 · DBE 70.6 ↔ 12.4 mS/cm) — sdcp_sigma_e_dcp_anchor_registration_20261012.md
  F4 ps45_sigma_e   ps45 다섯 조성 σ_e (Hertz H0 · 공통 4.1 mS/cm · PC 크기 인자 끔) — ps45_sigmae_factor_off_20261013/README.md
실행: python3 make_seminar_figs.py <out_dir>   · selftest: --selftest
"""
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch  # noqa: E402

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.linewidth": 0.9, "svg.fonttype": "none",
                     "mathtext.fontset": "dejavusans"})
RED, NAVY, GRAY, SKY, ORANGE = "#C0392B", "#1F3A68", "#6B7280", "#4A90C8", "#D95D12"

# ── 정본 값 (SRC) ────────────────────────────────────────────────────────────
GRID = dict(vox_um=[0.4, 0.3, 0.25],                      # SRC CLAUDE.md SR-01 (CL-24 · live · 공개값)
            sigma_e_ratio=[1.4215, 1.1621, 1.0849],
            sigma_ion_ratio=[1.0742, 0.9926, 0.9908])
SIGMA_E_EXP = dict(labels=["SBE", "DBE"],                 # SRC docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md §0 · §1
                   model=[54.0, 70.6], exp=[4.47, 12.4])
PS45 = dict(ps=["0:10", "3:7", "5:5", "7:3", "10:0"],     # SRC docs/data/ps45_sigmae_factor_off_20261013/README.md (주 값 · 소수 3 자리)
            sigma_e=[0.391, 0.406, 0.402, 0.375, 0.467])


def _fmt(ax, nx=4, ny=4):
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(nx))
    ax.yaxis.set_major_locator(MaxNLocator(ny))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace("-", "−")))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def fig_pipeline(out):
    fig, ax = plt.subplots(figsize=(22 / 2.54, 8.2 / 2.54))
    boxes = [("Powder packing\nand die compaction", "Discrete element method\n(soft spheres, contact law)", NAVY),
             ("Plastic compaction\nof the electrolyte", "Material point method\n(J2 plasticity, DEM scaffold)", NAVY),
             ("Voxelized\nmicrostructure", "Finite-volume transport\n(ionic, electronic, thermal)", NAVY),
             ("Electrode\nresponse", "Reaction distribution,\nrate capability", GRAY)]
    n = len(boxes); w, h, gap = 4.6, 3.6, 1.1; x0 = 0.6
    for i, (head, sub, col) in enumerate(boxes):
        x = x0 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 1.6), w, h, boxstyle="round,pad=0.02,rounding_size=0.25", fc="white", ec=col, lw=1.4))
        ax.text(x + w / 2, 1.6 + h * 0.68, head, ha="center", va="center", fontsize=11.5, color=col, fontweight="bold")
        ax.text(x + w / 2, 1.6 + h * 0.27, sub, ha="center", va="center", fontsize=9.2, color="#333333")
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((x + w + 0.08, 1.6 + h / 2), (x + w + gap - 0.08, 1.6 + h / 2),
                                         arrowstyle="-|>", mutation_scale=14, lw=1.3, color=GRAY))
    # 독립 보정 표시 (아래 띠)
    for i in range(3):
        x = x0 + i * (w + gap)
        ax.annotate("", xy=(x + w / 2, 1.45), xytext=(x + w / 2, 0.75), arrowprops=dict(arrowstyle="-", lw=0.8, color=GRAY, ls=(0, (3, 2))))
        ax.text(x + w / 2, 0.45, ["calibrated to\ncompaction experiments", "calibrated to\npure-electrolyte compaction", "anchored to\nconductivity measurements"][i],
                ha="center", va="center", fontsize=8.4, color=GRAY)
    ax.set_xlim(0, x0 + n * (w + gap)); ax.set_ylim(-0.2, 5.6); ax.axis("off")
    fig.tight_layout(pad=0.2)
    for ext in ("png", "svg"):
        fig.savefig(f"{out}/F1_pipeline.{ext}", dpi=300, transparent=True)
    plt.close(fig)


def fig_grid(out):
    fig, ax = plt.subplots(figsize=(11 / 2.54, 8.2 / 2.54))
    v = GRID["vox_um"]
    ax.plot(v, GRID["sigma_e_ratio"], "-o", color=RED, lw=1.6, ms=6, label="electronic")
    ax.plot(v, GRID["sigma_ion_ratio"], "-s", color=SKY, lw=1.6, ms=6, label="ionic")
    ax.axhline(1.0, color=GRAY, lw=0.8, ls=":")
    ax.invert_xaxis()
    ax.set_xlabel("Voxel size (µm)")
    ax.set_ylabel("Conductivity ratio, with / without SDCP")
    ax.set_ylim(0.95, 1.5)
    _fmt(ax, nx=3, ny=5)
    ax.set_xticks(v); ax.set_xticklabels([f"{x:g}" for x in v])
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout(pad=0.4)
    for ext in ("png", "svg"):
        fig.savefig(f"{out}/F2_grid_dependence.{ext}", dpi=300, transparent=True)
    plt.close(fig)
    with open(f"{out}/F2_grid_dependence.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n"); w.writerow(["Voxel size (um)", "sigma_e ratio", "sigma_ion ratio"])
        for row in zip(v, GRID["sigma_e_ratio"], GRID["sigma_ion_ratio"]):
            w.writerow(row)


def fig_sigma_e_exp(out):
    fig, ax = plt.subplots(figsize=(11 / 2.54, 8.2 / 2.54))
    x = [0, 1]; wdt = 0.34
    ax.bar([i - wdt / 2 for i in x], SIGMA_E_EXP["model"], wdt, color=NAVY, label="voxel model")
    ax.bar([i + wdt / 2 for i in x], SIGMA_E_EXP["exp"], wdt, color=ORANGE, label="DC polarization")
    ax.set_xticks(x); ax.set_xticklabels(SIGMA_E_EXP["labels"])
    ax.set_ylabel("Electronic conductivity (mS cm$^{-1}$)")
    ax.set_yscale("log"); ax.set_ylim(1, 200)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout(pad=0.4)
    for ext in ("png", "svg"):
        fig.savefig(f"{out}/F3_sigma_e_model_vs_exp.{ext}", dpi=300, transparent=True)
    plt.close(fig)
    with open(f"{out}/F3_sigma_e_model_vs_exp.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n"); w.writerow(["Electrode", "Voxel model (mS/cm)", "DC polarization (mS/cm)"])
        for row in zip(SIGMA_E_EXP["labels"], SIGMA_E_EXP["model"], SIGMA_E_EXP["exp"]):
            w.writerow(row)


def fig_ps45_sigma_e(out):
    fig, ax = plt.subplots(figsize=(11 / 2.54, 8.2 / 2.54))
    x = list(range(5))
    ax.bar(x, PS45["sigma_e"], 0.55, color=NAVY)
    ax.set_xticks(x); ax.set_xticklabels(PS45["ps"])
    ax.set_xlabel("Large : small NCM (mass)")
    ax.set_ylabel("Electronic conductivity (mS cm$^{-1}$)")
    ax.set_ylim(0, 0.6)
    _fmt(ax, nx=5, ny=4)
    fig.tight_layout(pad=0.4)
    for ext in ("png", "svg"):
        fig.savefig(f"{out}/F4_ps45_sigma_e.{ext}", dpi=300, transparent=True)
    plt.close(fig)
    with open(f"{out}/F4_ps45_sigma_e.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n"); w.writerow(["PC:SC", "sigma_e (mS/cm) Hertz H0 · common 4.1 mS/cm · PC size factor off"])
        for row in zip(PS45["ps"], PS45["sigma_e"]):
            w.writerow(row)


def selftest():
    root = Path(__file__).resolve()
    repo = next(p for p in root.parents if (p / "CLAUDE.md").exists()) if any((p / "CLAUDE.md").exists() for p in root.parents) else Path("/home/user/Yonghoon-DEM-DFT")
    t = (repo / "docs/data/ps45_sigmae_factor_off_20261013/README.md").read_text(encoding="utf-8")
    for s in ("0.390802", "0.405815", "0.402466", "0.374697", "0.467175"):
        assert s in t, s
    for a, b in zip(PS45["sigma_e"], (0.390802, 0.405815, 0.402466, 0.374697, 0.467175)):
        assert abs(a - round(b, 3)) < 1e-9
    c = (repo / "CLAUDE.md").read_text(encoding="utf-8")
    assert "1.4215 → 1.1621 → 1.0849" in c and "1.0742 → 0.9926 → 0.9908" in c
    r = (repo / "docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md").read_text(encoding="utf-8")
    assert "54.0" in r and "70.6" in r and "4.47" in r and "12.4" in r
    ban = json.loads((repo / "docs/reviews/claims.json").read_text(encoding="utf-8")).get("quotation_ban", [])
    pats = [q.get("pattern") if isinstance(q, dict) else q for q in ban]
    src = root.read_text(encoding="utf-8")
    hits = [p for p in pats if p and p in src]
    assert not hits, hits
    print("selftest ok — values match canonical sources · no banned strings")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        out = sys.argv[1] if len(sys.argv) > 1 else "."
        Path(out).mkdir(parents=True, exist_ok=True)
        fig_pipeline(out); fig_grid(out); fig_sigma_e_exp(out); fig_ps45_sigma_e(out)
        print("written", out)

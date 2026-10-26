#!/usr/bin/env python3
"""fig_weekly_2026_10_25.py — 주간보고 (2026-10-19 ~ 10-25) 그림 1 장 + Origin CSV 1 벌.

그림: Nd 자리 두 모델 (MLi_04 · MP_07) 의 EOS 점 (점마다 이온 이완) 위에, **기준 셀 (x = 1.00) 의 압력 하나로** 그린
조화 어림 곡선 E(V) ≈ E₁ − P₁ (V − V₁) + B (V − V₁)² / (2 V₁) 을 겹친다. 이번 주 CLAUDE.md 에 들어간
'EOS 는 조건부 — 압력 어림이 먼저' (사용자 2026-10-23) 의 근거 그림이다.

    python3 tools/figures/fig_weekly_2026_10_25.py
    python3 tools/figures/fig_weekly_2026_10_25.py --selftest   # 교차검산 양성 · 음성 (압력 · 모델 짝)

읽는 것 (전부 기록 · 새 계산 없음)
  · db/properties/ndo_site_eos_fit_2026_10_23.json       — EOS 점 (x · V · E) · BM3 V₀
  · db/properties/ndo_site_dft_v0_readout_2026_10_23.json — V₀ 이온 이완 에너지 (모델 최저)
  · db/raw/ndo_site_eos_2026_10_16/<모델>_x100/scf.out     — x = 1.00 점의 마지막 압력 P

⛔ 이 그림이 못 하는 것
  · ΔG_site 를 그리지 않는다 (그 값은 판독 기록과 카드 §5 문장에서만 쓴다).
  · B 를 재지 않는다 — 어림 곡선의 B 는 **가정** (중심 30 GPa · 띠 21.7–32.5 GPa = 우리 DFT B₀ 범위) 이다.
  · 비등방 응력 (모양) 을 안 본다 — P (평균) 만 쓴다.
  · MLi_04 의 x = 1.02 점은 Li 하나가 다른 자리에 있는 묶음이라 V₀ 이완보다 낮게 찍힌다 (그대로 그린다 · 고치지 않는다).
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import sys

import numpy as np

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/figures"))
import house_style as H  # noqa: E402

DB = R / "db/properties"
FIT = DB / "ndo_site_eos_fit_2026_10_23.json"
V0R = DB / "ndo_site_dft_v0_readout_2026_10_23.json"
RAW = R / "db/raw/ndo_site_eos_2026_10_16"
OUT = R / "docs/figures/weekly_2026_10_25"
CSV = DB / "weekly_nd_eos_pressure_origin_2026_10_25.csv"

GPA_TO_EV_A3 = 1.0 / 160.21766208          # 1 GPa = 0.00624151 eV/Å³
B_MID, B_LO, B_HI = 30.0, 21.7, 32.5       # GPa — 가정 (카드 · CLAUDE.md 와 같은 값)
MODELS = (("MLi_04", "MLi", "Nd on Li site (MLi_04)"), ("MP_07", "MP", "Nd on P site (MP_07)"))
COL = {"MLi_04": "#0d9488", "MP_07": "#7c3aed"}


class Refuse(RuntimeError):
    """교차검산이 틀렸다 — 그리지 않는다."""


def last_pressure_kbar(out: pathlib.Path) -> float:
    hits = re.findall(r"total\s+stress\s+\(Ry/bohr\*\*3\)\s+\(kbar\)\s+P=\s*(-?\d+\.?\d*)",
                      out.read_text(errors="ignore"))
    if not hits:
        raise Refuse(f"{out}: 압력 줄이 없다")
    return float(hits[-1])


def harmonic(x, x1, e1, p_gpa, v1, b_gpa):
    """기준점 (x1 · e1 · P) 하나와 B 로 만든 조화 곡선 — x = V/V_ref."""
    dv = (x - x1) * v1 / x1 * x1          # V − V₁ (V = x · V_ref · V₁ = x1 · V_ref) → V_ref = v1 / x1
    p = p_gpa * GPA_TO_EV_A3
    b = b_gpa * GPA_TO_EV_A3
    return e1 - p * dv + b * dv * dv / (2.0 * v1)


def compute(pressure=last_pressure_kbar, models=MODELS):
    """기록 → (panel, rows, est, eos). 교차검산이 틀리면 Refuse (그리지 않는다)."""
    fit = json.loads(FIT.read_text())["cells"]
    rd = json.loads(V0R.read_text())["dopants"]["Nd"]["models"]
    rows, panel = [], {}
    for name, key, label in models:
        c = fit[name]
        pts = sorted(c["points"], key=lambda p: p["x"])
        e_v0 = rd[key]["ranked"][0]["E_eV"]
        if rd[key]["ranked"][0]["name"] != name:
            raise Refuse(f"{key}: 판독 기록의 최저 모델이 {name} 가 아니다")
        p1 = next(p for p in pts if abs(p["x"] - 1.0) < 1e-9)
        pk = pressure(RAW / f"{name}_x100" / "scf.out")
        panel[name] = dict(label=label, pts=pts, e_v0=e_v0, x0=c["x0"], p1=p1, p_gpa=pk / 10.0)
        for p in pts:
            rows.append([name, "eos_point_ion_relaxed", f"{p['x']:.4f}", f"{p['V_A3']:.4f}",
                         f"{p['E_eV'] - e_v0:.6f}", "", ""])
        rows.append([name, "v0_ion_relaxed", f"{c['x0']:.6f}", f"{c['fit_all']['V0_A3']:.4f}",
                     "0.000000", "", ""])
    # ── 교차검산: 압력 어림 보정 (B 30) 이 카드 · CLAUDE.md 의 −0.098 eV/Nd 를 다시 내는가 · EOS 는 −0.100 ──
    v1 = panel["MP_07"]["p1"]["V_A3"]
    if abs(v1 - panel["MLi_04"]["p1"]["V_A3"]) > 1e-6:
        raise Refuse("두 모델의 x = 1.00 부피가 다르다")
    corr = {n: -(d["p_gpa"] * GPA_TO_EV_A3) ** 2 * v1 / (2 * B_MID * GPA_TO_EV_A3) for n, d in panel.items()}
    est = (corr["MP_07"] - corr["MLi_04"]) / 2.0                      # eV/Nd (Nd 2)
    eos = -((panel["MP_07"]["p1"]["E_eV"] - panel["MP_07"]["e_v0"])
            - (panel["MLi_04"]["p1"]["E_eV"] - panel["MLi_04"]["e_v0"])) / 2.0
    if abs(est + 0.098) > 0.0015 or abs(eos + 0.1005) > 0.0015:
        raise Refuse(f"기록 재현 실패 — 압력 어림 {est:+.4f} (기록 −0.098) · EOS {eos:+.4f} (기록 −0.100)")
    return panel, rows, est, eos, v1


def _selftest() -> int:
    ok = bad = 0

    def chk(c, m):
        nonlocal ok, bad
        print(("  ✓ " if c else "  ✗ ") + m)
        ok, bad = ok + bool(c), bad + (not c)

    _, _, est, eos, _ = compute()
    chk(abs(est + 0.0980) < 5e-4 and abs(eos + 0.1005) < 5e-4,
        f"[양성] 기록 재현 — 압력 어림 {est:+.4f} · EOS {eos:+.4f} eV/Nd")
    v1, pg, bg = 1175.66, 1.31, 30.0
    xs = np.linspace(0.95, 1.10, 3001)
    e = harmonic(xs, 1.0, 0.0, pg, v1, bg)
    depth = (pg * GPA_TO_EV_A3) ** 2 * v1 / (2 * bg * GPA_TO_EV_A3)
    chk(abs(e.min() + depth) < 1e-6 and abs(xs[e.argmin()] - (1 + pg / bg)) < 1e-4,
        "[양성] 조화 곡선의 바닥 = −P²V/(2B) · 위치 x = 1 + P/B (해석해)")
    # 음성은 **어느 가드가** 거부했는지까지 본다 — 짝을 바꾸면 e_v0 도 바뀌어 교차검산이 먼저 잡을 수 있다
    #   (2026-10-26 깨기: 짝 검사를 꺼도 초록이었다 — 교차검산이 대신 거부했다)
    def refused_by(fn, needle):
        try:
            fn()
        except Refuse as e:
            return needle in str(e)
        return False

    chk(refused_by(lambda: compute(pressure=lambda f: last_pressure_kbar(f) * (1.5 if "MP_07" in str(f) else 1.0)),
                   "기록 재현 실패"),
        "[음성] MP_07 압력을 1.5 배로 넣으면 교차검산이 거부 (그리지 않는다)")
    chk(refused_by(lambda: compute(models=(("MLi_04", "MP", "x"), ("MP_07", "MLi", "y"))),
                   "최저 모델이"),
        "[음성] 모델 ↔ 판독 기록 짝이 바뀌면 짝 검사가 거부")
    print(f"fig selftest: ✓ {ok} · ✗ {bad}")
    return 0 if bad == 0 else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    panel, rows, est, eos, v1 = compute()
    print(f"교차검산 ✓ 압력 어림 {est:+.4f} · EOS {eos:+.4f} eV/Nd (B {B_MID:g} GPa 가정)")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    OUT.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.3), sharey=False)
    xs = np.linspace(0.975, 1.085, 221)
    for ax, (name, _, _) in zip(axes, MODELS):
        d = panel[name]
        col = COL[name]
        e1 = d["p1"]["E_eV"] - d["e_v0"]
        lo = harmonic(xs, 1.0, e1, d["p_gpa"], v1, B_LO)
        hi = harmonic(xs, 1.0, e1, d["p_gpa"], v1, B_HI)
        mid = harmonic(xs, 1.0, e1, d["p_gpa"], v1, B_MID)
        ax.fill_between(xs, np.minimum(lo, hi), np.maximum(lo, hi), color=col, alpha=0.12, lw=0,
                        label=f"estimate band (B {B_LO:g}–{B_HI:g} GPa)")
        ax.plot(xs, mid, ls="--", color=col, lw=1.6,
                label=f"estimate from P(x = 1.00) = {d['p_gpa'] * 10:.1f} kbar, B {B_MID:g} GPa")
        ax.plot([p["x"] for p in d["pts"]], [p["E_eV"] - d["e_v0"] for p in d["pts"]], "o",
                color=H.INK, ms=6, label="EOS points (ion relax at fixed cell)")
        ax.plot([d["x0"]], [0.0], marker="*", ms=14, color=col, mec=H.INK, ls="none",
                label=f"V0 ion relax (x = {d['x0']:.3f})")
        ax.plot([1.0], [e1], marker="s", ms=8, mfc="white", mec=col, mew=1.8, ls="none",
                label="reference cell (x = 1.00)")
        H.apply_axes(ax, xlabel="V / V(reference cell)", ylabel="E − E(V0 ion relax) (eV per cell)",
                     title=d["label"], fontsize=11)
        ax.set_xlim(0.975, 1.085)
        ax.set_ylim(-0.05, max(0.5, e1 + 0.12))
        ax.legend(fontsize=7.6, frameon=False, loc="upper center")
        for x_ in xs[::20]:
            rows.append([name, "pressure_estimate_B30", f"{x_:.4f}", f"{x_ * v1:.4f}",
                         f"{harmonic(x_, 1.0, e1, d['p_gpa'], v1, B_MID):.6f}", f"{d['p_gpa'] * 10:.2f}", B_MID])
    sgn = lambda v: f"{v:+.3f}".replace("-", "\u2212")          # 진짜 마이너스 (하이픈 아님)
    fig.suptitle("Site energy check: EOS (12 points, one week) vs one-cell pressure estimate "
                 f"({sgn(est)} vs {sgn(eos)} eV/Nd correction)", fontsize=11.5, color=H.INK)
    fig.tight_layout()
    png = OUT / "nd_eos_vs_pressure.png"
    fig.savefig(png, dpi=300)
    with CSV.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "kind", "x_V_over_Vref", "V_A3", "dE_eV_per_cell_vs_V0_ion_relax",
                    "P_reference_kbar", "B_assumed_GPa"])
        w.writerows(rows)
    print(f"→ {png.relative_to(R)} · {CSV.relative_to(R)} ({len(rows)} 줄)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

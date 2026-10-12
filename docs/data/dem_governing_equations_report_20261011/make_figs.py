"""DEM 지배방정식 배경 보고서 (2026-10-11) 그림 두 장.

fig1 — 접촉 기하 모식도 (그림만 · 수치 없음).
fig2 — LIGGGHTS-PUBLIC 3d5c00f `normal_model_hooke_hysteresis.h` 156–195 행의 이력 법선력을
       그대로 옮긴 함수로 한 번의 적재–제하–재적재 경로를 그린다 (접촉 감쇠 −γ_n v_n 은 뺐다).
       축은 δ/δ_lim · F/(k₁ δ_lim) 로 무차원화 — 덱 (ps45) 의 상 쌍별 k̂₂/k₁ · k_c/k₁ 값을 쓴다.
실행: python3 make_figs.py <출력 폴더>   (selftest: python3 make_figs.py --selftest)
"""
import math
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Arc  # noqa: E402

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "mathtext.fontset": "dejavusans",
                     "axes.linewidth": 1.0, "svg.fonttype": "none"})


def f_hys(dn, hist, kn, k2max, kc, phif, reff, update=True):
    """normal_model_hooke_hysteresis.h 156–195 행 (감쇠 제외) — 반환 (F_hys, 새 δ_max)."""
    if dn > hist:
        hist = dn
    dmax = hist
    dlim = (k2max / (k2max - kn)) * phif * 2 * reff
    if dmax >= dlim:                                   # 포화 가지 (166–178)
        k2 = k2max
        ftmp = k2 * (dn - dlim) + kn * dlim
        if ftmp >= -kc * dn:
            f = ftmp
        else:
            f = -kc * dn
            nd = 0.5 * (dn + math.sqrt(dn * dn + 4 * ((kn + kc) * dn * dlim / (k2max - kn))))
            if update:
                hist = nd
    else:                                              # 비포화 가지 (179–195)
        k2 = kn + (k2max - kn) * dmax / dlim
        ftmp = k2 * (dn - dmax) + kn * dmax
        if ftmp >= kn * dn:
            f = kn * dn
        elif ftmp > -kc * dn:
            f = ftmp
        else:
            f = -kc * dn
            nd = 0.5 * (dn + math.sqrt(dn * dn + 4 * ((kn + kc) * dn * dlim / (k2max - kn))))
            if update:
                hist = nd
    return f, hist


def path(points, n=4000):
    out = []
    for a, b in zip(points[:-1], points[1:]):
        out += [a + (b - a) * i / n for i in range(n)]
    return out + [points[-1]]


PAIRS = [("AM–AM", 1.5, 1.0e5, 0.05), ("AM–SE", 3.0, 2.0e5, 0.01), ("SE–SE", 5.0, 1.0e6, 0.005)]
PROTOCOL = [0.0, 0.6, 1e-4, 1.4, 1e-4]   # δ/δ_lim: 비포화 적재 → 제하 → 포화 넘어 재적재 → 제하


def cycle(k2r, kcr, phif):
    kn = 1.0
    reff = 1.0 / ((k2r / (k2r - 1.0)) * phif * 2)      # δ_lim = 1 이 되게
    hist, xs, ys = 0.0, [], []
    for d in path(PROTOCOL):
        f, hist = f_hys(d, hist, kn, k2r * kn, kcr * kn, phif, reff)
        xs.append(d)
        ys.append(f)
    return xs, ys


def _fmt(ax):
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    for axis in (ax.xaxis, ax.yaxis):
        axis.set_major_locator(MaxNLocator(5))
        axis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace("-", "\u2212")))


def _arrow_on(ax, xs, ys, i, color="k"):
    ax.annotate("", xy=(xs[i + 40], ys[i + 40]), xytext=(xs[i], ys[i]),
                arrowprops=dict(arrowstyle="-|>", lw=0, color=color, mutation_scale=9))


def fig2(out):
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(16 / 2.54, 7.2 / 2.54))
    # (a) 한 쌍 (AM–SE 계수) 의 경로 — O→A 적재 · A→B 제하 · B→A→C 재적재 · C→D 제하
    name, k2r, kcr, phif = PAIRS[1]
    xs, ys = cycle(k2r, kcr, phif)
    ax.plot(xs, ys, color="k", lw=1.4)
    n = len(xs) // 4
    for i in (n // 2, n + n // 3, 2 * n + n // 5, 2 * n + int(0.82 * n), 3 * n + n // 2):
        _arrow_on(ax, xs, ys, i)
    ax.axhline(0, color="0.65", lw=0.7)
    ax.axvline(1.0, color="0.65", lw=0.7, ls=":")
    k2a = 1 + (k2r - 1) * 0.6
    d0a = (1 - 1 / k2a) * 0.6
    ax.plot([d0a], [0], "o", ms=3.5, color="k")
    ax.annotate(r"$\delta_0$", xy=(d0a, 0), xytext=(d0a - 0.05, 0.55), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.text(0.10, 0.38, r"$k_1$", fontsize=9)
    ax.text(0.20, -0.78, r"$k_2(\delta_{\max})$", fontsize=9)
    ax.text(1.22, 1.18, r"$\hat k_2$", fontsize=9)
    ax.text(1.03, -1.75, r"$\delta_{\max}\geq\delta_{\rm lim}$", fontsize=8, color="0.3")
    ax.text(0.02, -1.55, "tension\n" + r"($F<0$)", fontsize=8, color="0.3")
    ax.set_xlabel(r"$\delta/\delta_{\rm lim}$")
    ax.set_ylabel(r"$F/(k_1\delta_{\rm lim})$")
    ax.set_title(r"(a) one cycle, $\hat k_2/k_1=3$", fontsize=9, loc="left")
    ax.set_xlim(0, 1.5)
    _fmt(ax)
    # (b) 세 상 쌍 계수 — 포화 뒤 (δ_max = 1.4 δ_lim) 제하 직선
    for (nm, k2r, kcr, phif), ls in zip(PAIRS, ["-", "--", ":"]):
        xs = [i / 1000 for i in range(1, 1401)]
        hist, ys = 1.4, []
        reff = 1.0 / ((k2r / (k2r - 1.0)) * phif * 2)
        for d in xs:
            f, _ = f_hys(d, 1.4, 1.0, k2r, kcr, phif, reff, update=False)
            ys.append(f)
        bx.plot(xs, ys, ls, color="k", lw=1.4, label=rf"{nm}  $\hat k_2/k_1$ = {k2r:g}")
    bx.plot([0, 1], [0, 1], color="0.55", lw=1.0)
    bx.text(0.06, 0.55, r"loading $k_1$", fontsize=8, color="0.35")
    bx.axhline(0, color="0.65", lw=0.7)
    bx.set_xlabel(r"$\delta/\delta_{\rm lim}$")
    bx.set_title(r"(b) unloading from $\delta_{\max}=1.4\,\delta_{\rm lim}$", fontsize=9, loc="left")
    bx.set_xlim(0, 1.5)
    bx.legend(frameon=False, fontsize=7.5, loc="lower right")
    _fmt(bx)
    fig.tight_layout()
    for ext in ("svg", "png"):
        fig.savefig(f"{out}/fig2_hysteresis_cycle.{ext}", dpi=300)
    plt.close(fig)


def fig1(out):
    fig, ax = plt.subplots(figsize=(12 / 2.54, 7.5 / 2.54))
    Ri, Rj, d = 1.0, 0.75, 1.55          # 중심 거리 d < R_i + R_j → 겹침 δ = 0.2
    xi, xj = 0.0, d
    delta = Ri + Rj - d
    ax.add_patch(Circle((xi, 0), Ri, fill=False, lw=1.4))
    ax.add_patch(Circle((xj, 0), Rj, fill=False, lw=1.4))
    ax.plot([xi, xj], [0, 0], color="0.6", lw=0.7, ls=(0, (3, 3)))
    ax.plot([xi, xj], [0, 0], "ko", ms=3)
    ax.text(xi - 0.05, 0.10, r"$i$", fontsize=10)
    ax.text(xj - 0.02, 0.10, r"$j$", fontsize=10)
    xc = Ri - delta / 2                   # 접촉면 (중심 i 에서 c_ri = R_i − δ/2)
    hh = math.sqrt(Ri ** 2 - xc ** 2)
    ax.plot([xc, xc], [-hh, hh], color="0.35", lw=1.0, ls="--")
    # δ (겹침) — 위쪽에 따로
    ax.annotate("", xy=(d - Rj, 0.93), xytext=(Ri, 0.93), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax.plot([d - Rj, d - Rj], [0.62, 0.98], color="0.6", lw=0.5)
    ax.plot([Ri, Ri], [0.62, 0.98], color="0.6", lw=0.5)
    ax.text(xc - 0.05, 1.02, r"$\delta$", fontsize=10)
    # c_r,i (아래 치수선)
    ax.plot([xi, xi], [0, -1.18], color="0.6", lw=0.5)
    ax.plot([xc, xc], [-hh, -1.18], color="0.6", lw=0.5)
    ax.annotate("", xy=(xc, -1.13), xytext=(xi, -1.13), arrowprops=dict(arrowstyle="<->", lw=0.8))
    ax.text(0.05, -1.36, r"$c_{r,i}=R_i-\delta/2$", fontsize=8)
    # R_i, R_j
    ax.annotate("", xy=(xi - 0.62, 0.78), xytext=(xi, 0), arrowprops=dict(arrowstyle="->", lw=0.8, color="0.35"))
    ax.text(-0.55, 0.30, r"$R_i$", fontsize=9, color="0.35")
    ax.annotate("", xy=(xj + 0.53, -0.53), xytext=(xj, 0), arrowprops=dict(arrowstyle="->", lw=0.8, color="0.35"))
    ax.text(xj + 0.33, -0.22, r"$R_j$", fontsize=9, color="0.35")
    # n_ij (j → i) · F_t (접촉점에서 접선 방향)
    ax.add_patch(FancyArrowPatch((xc, 0), (xc - 0.5, 0), arrowstyle="-|>", mutation_scale=10, lw=1.3))
    ax.text(xc - 0.52, -0.20, r"$\mathbf{n}_{ij}$", fontsize=10)
    ax.add_patch(FancyArrowPatch((xc, 0), (xc, 0.55), arrowstyle="-|>", mutation_scale=10, lw=1.3))
    ax.text(xc - 0.30, 0.40, r"$\mathbf{F}_{t}$", fontsize=10)
    # ω_i
    ax.add_patch(Arc((xi - 0.35, -0.35), 0.42, 0.42, theta1=200, theta2=340, lw=1.0))
    ax.add_patch(FancyArrowPatch((xi - 0.35 + 0.195, -0.35 - 0.075), (xi - 0.35 + 0.21, -0.35 + 0.01),
                                 arrowstyle="-|>", mutation_scale=7, lw=1.0))
    ax.text(xi - 0.42, -0.72, r"$\boldsymbol{\omega}_i$", fontsize=9)
    ax.set_xlim(-1.15, 2.45)
    ax.set_ylim(-1.45, 1.15)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    for ext in ("svg", "png"):
        fig.savefig(f"{out}/fig1_contact_geometry.{ext}", dpi=300)
    plt.close(fig)


def selftest():
    ok = 0
    # ① 적재 = k1 δ
    f, h = f_hys(0.3, 0.0, 1.0, 1.5, 1e5, 0.05, 1 / (3 * 0.05 * 2))
    assert abs(f - 0.3) < 1e-12 and h == 0.3
    ok += 1
    # ② 비포화 제하: k2 = k1 + (k̂2 − k1) δmax/δlim · F = k2 (δ − δmax) + k1 δmax
    f, h = f_hys(0.2, 0.6, 1.0, 1.5, 1e5, 0.05, 1 / (3 * 0.05 * 2))
    k2 = 1 + 0.5 * 0.6
    assert abs(f - (k2 * (0.2 - 0.6) + 0.6)) < 1e-12
    ok += 1
    # ③ 포화: F = k̂2 (δ − δlim) + k1 δlim (δ_lim = 1)
    f, h = f_hys(1.2, 1.4, 1.0, 5.0, 1e6, 0.005, 1 / (1.25 * 0.005 * 2))
    assert abs(f - (5.0 * (1.2 - 1.0) + 1.0)) < 1e-9
    ok += 1
    # ④ 큰 k_c: 제하 직선이 인장까지 이어진다 — δ > k2 δ0/(k2 + k_c) 이면 F = k2 (δ − δ0) < 0
    k2 = 1 + 0.5 * 0.6
    f, h = f_hys(1e-5, 0.6, 1.0, 1.5, 1e5, 0.05, 1 / (3 * 0.05 * 2))
    assert abs(f - (k2 * (1e-5 - 0.6) + 0.6)) < 1e-9 and f < 0 and h == 0.6
    ok += 1
    # ⑤ 그 문턱 아래 (δ = 1e-6 < k2 δ0/(k2 + k_c) ≈ 1.8e-6) = 점착 가지 −k_c δ · δ_max 를 줄여 다시 쓴다
    f, h = f_hys(1e-6, 0.6, 1.0, 1.5, 1e5, 0.05, 1 / (3 * 0.05 * 2))
    assert abs(f - (-1e5 * 1e-6)) < 1e-12 and h < 0.6
    ok += 1
    print(f"selftest {ok}/5 PASS")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        out = sys.argv[1] if len(sys.argv) > 1 else "."
        fig1(out)
        fig2(out)
        print("written", out)

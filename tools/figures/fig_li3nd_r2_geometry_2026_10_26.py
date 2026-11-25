#!/usr/bin/env python3
"""fig_li3nd_r2_geometry_2026_10_26.py — Li₃Nd 3×3×3 대조군 r2 의 기하가 시작 대비 어떻게 바뀌었나 (진단용).

사용자 10-26 *'지금 원자 상태 cif 로 뽑아서 초반에 비해 어떻게 됐는지 볼 수 있나'* — 이완이 **진행 중**이라
이 기하는 진단용이다 (kb/questions/li3nd_pristine_reconstruction_2026_09_02.md '아직 말하면 안 되는 것').

    python3 tools/figures/fig_li3nd_r2_geometry_2026_10_26.py
    python3 tools/figures/fig_li3nd_r2_geometry_2026_10_26.py --selftest   # σ 복원 · 중심 보존 · 음성 둘

읽는 것 (전부 기록 · 새 계산 없음)
  · db/structures/sei_li3nd_mp-976264.vasp — MP 원시셀 (build_dft_inputs.make_control_structures 와 같은 × (3,3,3))
  · db/raw/li3nd_p333_r2_geometry_2026_10_26/00_control_relax.in — 지금 이력의 출발 기하 (9 월 첫 실행 50 스텝 뒤를
    이어받은 것 · 파일 첫 줄 'carried-from-unconverged … step 50')
  · 같은 폴더 positions_by_step.txt — gabia 출력 파일마다 BFGS 스텝의 ATOMIC_POSITIONS (e479d738f)

원래 r2 시작 구조 (이상 자리 + rattle · 시드 2) 는 기록에 크기가 없다 → **되푼다**: QE 이완은 힘의 합을 0 으로 두므로
좌표 중심 (가중 없음) 이 보존된다. carry 기하의 중심 − 이상 자리 중심 = σ · (시드 2 난수의 중심) 을 세 축이 같은 σ 로
만족해야 한다 — 축마다 다르면 거부 (시드 · 순서 · 셀 중 하나가 틀렸다).

쓰는 것
  · db/raw/li3nd_p333_r2_geometry_2026_10_26/structures/ — 이상 · r2 시작 · 9 월 carry · 지금 (cif · vasp · xyz)
  · docs/figures/li3nd_r2_geometry_2026_10_26/li3nd_r2_geometry.png
  · db/properties/li3nd_r2_geometry_trend_origin_2026_10_26.csv · li3nd_r2_ndnd_hist_origin_2026_10_26.csv

⛔ 이 도구가 못 하는 것
  · 에너지를 읽지 않는다 — 기하만 본다 (진행 중 이완의 에너지 · 기하는 정량 인용 금지).
  · 첫 실행 (r2 시작 → 50 스텝) 의 중간 기하는 없다 (.out.step50 은 추출하지 않았다) — 그림에서 그 구간은 점선이다.
  · '상분리' 를 판정하지 않는다 — Nd–Nd 거리 · Nd 이웃 수 · 덩어리 크기 · 이웃 중 Nd 비율만 센다 (문턱은 아래 상수).
  · 셀은 고정 (relax) 이다 — 셀 모양 · 부피 변화는 이 계산에 없다.
"""
from __future__ import annotations

import csv
import pathlib
import re
import sys

import numpy as np

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/figures"))
import house_style as H  # noqa: E402

O = R / "db/raw/li3nd_p333_r2_geometry_2026_10_26"
PRIM = R / "db/structures/sei_li3nd_mp-976264.vasp"
FIG = R / "docs/figures/li3nd_r2_geometry_2026_10_26"
CSV_T = R / "db/properties/li3nd_r2_geometry_trend_origin_2026_10_26.csv"
CSV_H = R / "db/properties/li3nd_r2_ndnd_hist_origin_2026_10_26.csv"

SEED = 2                 # r2 = rattle 시드 2 (build_dft_inputs: default_rng(seed).normal(0, σ, shape))
CURRENT = ("00_control_relax.out.004", "00_control_relax.out.005", "00_control_relax.out.006",
           "00_control_relax.out.007", "00_control_relax.out.008", "00_control_relax.out")   # 지금 이력 (09-06 from_scratch 부터)
CARRY_STEP = 50          # 첫 실행이 50 스텝에서 멈춰 이어받았다 (입력 첫 줄)
R_NDND = 4.2             # Å — Nd 끼리 '닿음' (이상 최단 5.186 · 이 값 아래는 이상 구조에 없다)
R_MIX = 3.8              # Å — 이웃 중 Nd 비율을 셀 반경
CLS = np.array(["Li_tet", "Li_tet", "Li_oct", "Nd"] * 27)   # MP 원시셀 순서 Li(¼) Li(¾) Li(½) Nd(0) × 27


class Refuse(RuntimeError):
    pass


def ideal():
    from ase.io import read
    return read(str(PRIM)) * (3, 3, 3)


def qe_in(path):
    t = pathlib.Path(path).read_text().splitlines()
    i = next(k for k, ln in enumerate(t) if ln.startswith("CELL_PARAMETERS"))
    cell = np.array([[float(x) for x in t[i + j].split()] for j in (1, 2, 3)])
    i = next(k for k, ln in enumerate(t) if ln.startswith("ATOMIC_POSITIONS"))
    if "angstrom" not in t[i]:
        raise Refuse(f"{path}: ATOMIC_POSITIONS 단위가 angstrom 이 아니다")
    sy, xyz = [], []
    for ln in t[i + 1:]:
        p = ln.split()
        if len(p) < 4 or not re.match(r"^[A-Z][a-z]?$", p[0]):
            break
        sy.append(p[0])
        xyz.append([float(v) for v in p[1:4]])
    return cell, sy, np.array(xyz)


def blocks(path, n=108):
    out, lines, k = [], pathlib.Path(path).read_text().splitlines(), 0
    while k < len(lines):
        if lines[k].startswith("## "):
            p = lines[k].split()
            if "angstrom" not in lines[k]:
                raise Refuse(f"블록 단위가 angstrom 이 아니다: {lines[k]}")
            rows = [lines[k + 1 + j].split() for j in range(n)]
            out.append({"file": p[1], "bfgs": int(p[3]), "sy": [r[0] for r in rows],
                        "xyz": np.array([[float(v) for v in r[1:4]] for r in rows])})
            k += n + 1
        else:
            k += 1
    return out


def recover_sigma(I, x_start, seed=SEED):
    """중심 보존으로 rattle σ 를 푼다 → (σ, 축별 σ). 세 축이 1e-6 (상대) 안에서 같지 않으면 Refuse."""
    from ase.geometry import find_mic
    d, _ = find_mic(x_start - I.positions, I.cell, pbc=True)
    z = np.random.default_rng(seed).standard_normal((len(I), 3))
    s = d.mean(0) / z.mean(0)
    if np.ptp(s) > 1e-6 * abs(s.mean()):
        raise Refuse(f"축마다 σ 가 다르다 {np.round(s, 6)} — 시드 · 원자 순서 · 셀 중 하나가 틀렸다")
    return float(s.mean()), s


def centroid_check(x_ref, bl, tol=1e-6):
    """지금 이력의 블록마다 좌표 중심이 출발 기하와 같은가 (QE 이완은 힘의 합이 0). 아니면 Refuse."""
    c0 = x_ref.mean(0)
    worst = max(float(np.abs(b["xyz"].mean(0) - c0).max()) for b in bl)
    if worst > tol:
        raise Refuse(f"좌표 중심이 {worst:.2e} Å 움직였다 — 블록이 같은 이력이 아니거나 잘렸다")
    return worst


def metrics(I, x):
    from ase.geometry import find_mic, get_distances
    from scipy.sparse.csgraph import connected_components
    _, L = find_mic(x - I.positions, I.cell, pbc=True)
    D = get_distances(x, cell=I.cell, pbc=True)[1]
    np.fill_diagonal(D, 99.0)
    nd = np.where(CLS == "Nd")[0]
    li = np.where(CLS != "Nd")[0]
    touch = D[np.ix_(nd, nd)] < R_NDND
    _, lab = connected_components(touch.astype(int), directed=False)
    nb = D < R_MIX
    m = {f"mean_disp_{c}_A": float(L[CLS == c].mean()) for c in ("Nd", "Li_tet", "Li_oct")}
    m.update({f"max_disp_{c}_A": float(L[CLS == c].max()) for c in ("Nd", "Li_tet", "Li_oct")})
    m.update({"NdNd_CN_lt4p2A_mean": float(touch.sum(1).mean()),
              "NdNd_min_A": float(D[np.ix_(nd, nd)].min()),
              "largest_Nd_cluster": int(np.bincount(lab).max()),
              "Nd_fraction_around_Nd_lt3p8A": float(np.mean([nb[i, nd].sum() / max(1, nb[i].sum()) for i in nd])),
              "Nd_fraction_around_Li_lt3p8A": float(np.mean([nb[i, nd].sum() / max(1, nb[i].sum()) for i in li])),
              "n_atoms_disp_gt1A": int((L > 1.0).sum())})
    return m, D[np.ix_(nd, nd)]


def build():
    I = ideal()
    cell, sy, x_carry = qe_in(O / "00_control_relax.in")
    if not np.allclose(I.cell[:], cell, atol=1e-6) or I.get_chemical_symbols() != sy:
        raise Refuse("이상 초격자와 입력의 셀 · 원자 순서가 다르다")
    bl = [b for b in blocks(O / "positions_by_step.txt") if b["file"] in CURRENT]
    if any(b["sy"] != sy for b in bl):
        raise Refuse("블록의 원자 순서가 입력과 다르다")
    centroid_check(x_carry, bl)
    sigma, _ = recover_sigma(I, x_carry)
    x_r2 = I.positions + sigma * np.random.default_rng(SEED).standard_normal((len(I), 3))
    series = [("r2_start", 0, "-", x_r2), ("sept_carry", CARRY_STEP, "00_control_relax.in", x_carry)]
    series += [(f"bfgs_{b['bfgs']}", CARRY_STEP + 1 + b["bfgs"], b["file"], b["xyz"]) for b in bl]
    return I, sigma, series


def write_structs(I, series):
    from ase.io import write
    sd = O / "structures"
    sd.mkdir(exist_ok=True)
    pick = {"ideal": I.positions, "r2_start_rattle": series[0][3], "sept_carry_step50": series[1][3],
            f"now_{series[-1][0]}_inprogress": series[-1][3]}
    names = []
    for tag, x in pick.items():
        at = I.copy()
        at.positions = x
        at.wrap()
        for ext, fmt in (("cif", "cif"), ("vasp", "vasp"), ("xyz", "extxyz")):
            f = sd / f"li3nd_p333_{tag}.{ext}"
            write(str(f), at, format=fmt, **({"direct": True} if fmt == "vasp" else {}))
            names.append(f.name)
    return sd, names


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()
    I, sigma, series = build()
    rows, hist = [], {}
    bins = np.arange(2.5, 7.01, 0.1)
    keep = {"ideal": None, "sept_carry": None, "bfgs_150": None, series[-1][0]: None}
    m0, d0 = metrics(I, I.positions)
    hist["ideal"] = d0
    for tag, g, f, x in series:
        m, dnn = metrics(I, x)
        rows.append({"tag": tag, "global_step": g, "source_file": f, **m})
        if tag in keep:
            hist[tag] = dnn
    sd, names = write_structs(I, series)
    now = rows[-1]
    print(f"σ (rattle) {sigma:.6f} Å · 지금 {series[-1][0]} · Nd 평균 변위 {now['mean_disp_Nd_A']:.2f} Å · "
          f"Nd 둘레 Nd (<{R_NDND} Å) {now['NdNd_CN_lt4p2A_mean']:.2f} · 가장 큰 Nd 덩어리 {now['largest_Nd_cluster']}/27")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    FIG.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(1, 3, figsize=(14.2, 4.3))
    g = np.array([r["global_step"] for r in rows])
    sty = {"Nd": (H.ELEM["Nd"], "-"), "Li_tet": (H.ELEM["Li"], "-"), "Li_oct": (H.ELEM["Li"], "--")}
    lab = {"Nd": "Nd", "Li_tet": "Li (tetrahedral site)", "Li_oct": "Li (octahedral site)"}
    for c, (col, ls) in sty.items():
        y = np.array([r[f"mean_disp_{c}_A"] for r in rows])
        ax[0].plot(g[1:], y[1:], ls=ls, color=col, lw=1.8, label=lab[c])
        ax[0].plot(g[:2], y[:2], ls=":", color=col, lw=1.2)
        ax[0].plot(g[:2], y[:2], "o", color=col, ms=4)
    ax[0].axvline(CARRY_STEP, color=H.MUT, lw=0.8, ls=":")
    ax[0].text(CARRY_STEP + 4, 0.30, "Sept restart\n(step 50 carried)", fontsize=7.5, color=H.MUT, va="bottom")
    H.apply_axes(ax[0], xlabel="BFGS step from r2 start", ylabel="mean displacement from ideal site (Å)",
                 title="(a) displacement", fontsize=10.5)
    ax[0].legend(fontsize=8, frameon=False, loc="upper left")
    cn = np.array([r["NdNd_CN_lt4p2A_mean"] for r in rows])
    ax[1].plot(g[1:], cn[1:], color=H.ELEM["Nd"], lw=1.8, label=f"Nd neighbours of Nd (< {R_NDND} Å)")
    ax[1].plot(g[:2], cn[:2], ":o", color=H.ELEM["Nd"], ms=4, lw=1.2)
    fr = np.array([r["Nd_fraction_around_Nd_lt3p8A"] for r in rows])
    a2 = ax[1].twinx()
    a2.plot(g, fr, color=H.INK, lw=1.2, ls="--", label=f"Nd share among neighbours of Nd (< {R_MIX} Å)")
    a2.set_ylabel("Nd share", fontsize=9.5, color=H.INK)
    a2.spines["top"].set_visible(False)
    H.apply_axes(ax[1], xlabel="BFGS step from r2 start", ylabel="mean count per Nd",
                 title="(b) Nd–Nd contacts", fontsize=10.5)
    h1, l1 = ax[1].get_legend_handles_labels()
    h2, l2 = a2.get_legend_handles_labels()
    ax[1].legend(h1 + h2, l1 + l2, fontsize=7.5, frameon=False, loc="lower right")
    cols = {"ideal": H.MUT, "sept_carry": "#9ca3af", "bfgs_150": "#f472b6", series[-1][0]: H.ELEM["Nd"]}
    names_h = {"ideal": "ideal sites", "sept_carry": "Sept restart (step 50)", "bfgs_150": "BFGS 150",
               series[-1][0]: f"now (BFGS {series[-1][0].split('_')[1]})"}
    hist_rows = {}
    for tag, dnn in hist.items():
        iu = np.triu_indices(27, 1)
        v = dnn[iu]
        h, _ = np.histogram(v[v < bins[-1]], bins=bins)
        hist_rows[tag] = h / 27.0
        if tag == "ideal":          # 이상 자리는 한 칸에 6 쌍/Nd 라 다른 선을 납작하게 만든다 → 세로선으로
            ax[2].axvline(float(v.min()), color=cols[tag], lw=1.2, ls="--",
                          label=f"ideal sites (6 pairs per Nd at {v.min():.2f} Å)")
            continue
        ax[2].step(bins[:-1], h / 27.0, where="post", color=cols[tag], lw=1.6, label=names_h[tag])
    ax[2].axvspan(2.5, R_NDND, color=H.ELEM["Nd"], alpha=0.06, lw=0)
    H.apply_axes(ax[2], xlabel="Nd–Nd distance (Å)", ylabel="pairs per Nd (0.1 Å bins)",
                 title="(c) Nd–Nd distances", fontsize=10.5)
    ax[2].legend(fontsize=8, frameon=False, loc="upper left")
    fig.suptitle("Li3Nd 3×3×3 control r2 (rattle seed 2, σ = 0.08 Å, fixed cell): relaxation in progress, "
                 "not converged, diagnostic only", fontsize=11, color=H.INK)
    fig.tight_layout()
    png = FIG / "li3nd_r2_geometry.png"
    fig.savefig(png, dpi=300)
    with CSV_T.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with CSV_H.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["NdNd_bin_low_A"] + [f"pairs_per_Nd_{t}" for t in hist_rows])
        for k, b0 in enumerate(bins[:-1]):
            w.writerow([f"{b0:.2f}"] + [f"{hist_rows[t][k]:.4f}" for t in hist_rows])
    print(f"→ {png.relative_to(R)} · {CSV_T.relative_to(R)} ({len(rows)} 줄) · {CSV_H.relative_to(R)} · "
          f"구조 {len(names)} 파일 → {sd.relative_to(R)}")
    return 0


def _selftest() -> int:
    ok = bad = 0

    def chk(c, msg):
        nonlocal ok, bad
        print(("  ✓ " if c else "  ✗ ") + msg)
        ok, bad = ok + bool(c), bad + (not c)

    I = ideal()
    _, _, x_carry = qe_in(O / "00_control_relax.in")
    s, s3 = recover_sigma(I, x_carry)
    chk(abs(s - 0.08) < 1e-6, f"[양성] 중심 보존으로 σ 복원 = {s:.6f} Å (세 축 {np.round(s3, 6)})")
    try:
        recover_sigma(I, x_carry, seed=3)
        chk(False, "[음성] 다른 시드 (3) 면 축마다 σ 가 달라 거부")
    except Refuse:
        chk(True, "[음성] 다른 시드 (3) 면 축마다 σ 가 달라 거부")
    bl = [b for b in blocks(O / "positions_by_step.txt") if b["file"] in CURRENT]
    chk(centroid_check(x_carry, bl) < 1e-9, f"[양성] 지금 이력 {len(bl)} 블록 좌표 중심 보존")
    bad_bl = [dict(bl[-1], xyz=bl[-1]["xyz"] + np.array([[0.05, 0, 0]] + [[0, 0, 0]] * 107))]
    try:
        centroid_check(x_carry, bad_bl)
        chk(False, "[음성] 원자 하나를 0.05 Å 옮긴 블록은 중심 검사가 거부")
    except Refuse:
        chk(True, "[음성] 원자 하나를 0.05 Å 옮긴 블록은 중심 검사가 거부")
    m, _ = metrics(I, I.positions)
    chk(m["NdNd_CN_lt4p2A_mean"] == 0 and abs(m["NdNd_min_A"] - 5.18587) < 1e-4 and m["largest_Nd_cluster"] == 1,
        f"[양성] 이상 구조: Nd–Nd 최단 {m['NdNd_min_A']:.4f} Å · 4.2 Å 안 Nd 이웃 0 · 덩어리 1")
    print(f"fig selftest: ✓ {ok} · ✗ {bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

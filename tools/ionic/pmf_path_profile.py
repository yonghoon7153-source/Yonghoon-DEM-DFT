#!/usr/bin/env python3
"""pmf_path_profile.py — **MD Li-밀도 PMF** 로 BV 판과 같은 그림을 만든다.

1저자 요청(2026-08-05): BV 프록시 말고 **MD 로 구한 자유에너지 지형**으로
경로 프로파일·구간 장벽·3D 등가면을 그리자. LPSCl1.6(게이트 통과 계)이 대상.

    F(r) = -k_B T ln( rho(r) / rho_max )      [eV]   (밀도 최대점 = 0)

BV 판과 **완전히 같은 관례**로 분석한다 (fig_bv_path_profile 의 원시함수 재사용):
  · 26-연결 + {0,1}³ 감김 판정, 축별 이분탐색으로 침투 문턱 F*(1D/2D/3D)
  · F* 천장 아래에서 에너지 선적분 최소 경로 (dijkstra_valley)
  · 반응좌표는 랩 해제 + bvlain mesh metric (cell/(N-1), 경계 스텝 0 Å)
→ 그래서 BV 그림과 **나란히 놓고 읽을 수 있다** (축·정의가 동일).

⚠⚠ **표집이 곧 신뢰도다.** rho=0 인 voxel 은 F=∞ 이고, 하필 장벽 꼭대기가 가장 덜
  방문된 곳이라 **궤적이 짧으면 F* 가 과대**해진다. 그래서 이 도구는 **β 게이트를 통과한
  계·온도**에만 쓴다 (comp1 600 K 는 6/6 케이지 → open_items #9 참조).
  통과 계라도 시드를 합쳐 밀도를 쌓는 게 좋다 (밀도는 앙상블 평균이 정당 — MSD 와 다름).

⚠ F* 는 **그 온도의 자유에너지**다. 온도를 반드시 병기하고, Ea 와 같은 양이라 부르지 않는다
  (실측 오프셋: comp1/modelc 에서 F* − Ea ≈ −53/−54 meV, 계통적).

  # 밀도 cube 는 li_density_cube.py 산출 (프레임워크 원자 + Li 밀도)
  python3 tools/ionic/pmf_path_profile.py --cube modelc_s1_T600_Li.cube \
      --cube modelc_s2_T600_Li.cube --cube modelc_s3_T600_Li.cube \
      --T 600 --tag modelc --label "LPSCl1.6" --out_dir pmf_out

자체 검증: --selftest_bv <cif> 를 주면 rho = exp(-E_BV/kT) 로 만든 가짜 밀도를 넣어
  F ≈ E_BV 가 되는지, 문턱이 BV 판과 일치하는지 확인한다 (파이프라인 단위검사).
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import label as nd_label, generate_binary_structure

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
from house_style import INK, MUT                                        # noqa: E402
import fig_bv_path_profile as bvp                                       # noqa: E402
from fig_bv_path_annotated import (label_valley, label_saddle, ANION,   # noqa: E402
                                   cage_centers, cage_of, mic_fn)
from plot_elf_clean import read_cube                                    # noqa: E402

KB = 8.617333262e-5
F_CAP = 5.0            # rho=0 voxel 의 F [eV] — 문턱 탐색 상한보다 충분히 크게


def label_valley_pmf(r, atoms, mic, has_li):
    """PMF 골짜기 라벨.

    ⚠ li_density_cube.py 의 cube 에는 **Li 가 원자로 없다** (프레임워크만; Li 는 밀도).
      그때 BV 판의 'on Li / vacant' 판정은 의미가 없다 — PMF 에서는 **밀도 극대 = Li 자리**가
      정의상 참이라, 음이온 배위만 적는다. Li 가 들어있는 cube 면 BV 판 라벨을 그대로 쓴다.
    """
    if has_li:
        return label_valley(r, atoms, mic)
    shell = sorted((float(np.linalg.norm(mic(p - r))), s) for s, p in atoms if s in ANION)
    coord = {}
    for dist, s in shell:
        if dist <= 3.2:
            coord[s] = coord.get(s, 0) + 1
    cstr = "+".join(f"{n}{s}" for s, n in sorted(coord.items())) or "—"
    return f"Li site\n{cstr}", float("nan")


def load_density(paths):
    """여러 cube 의 Li 밀도를 **합산**한다 (시드 앙상블). 격자·셀 일치 검사 포함."""
    tot, ref = None, None
    for p in paths:
        data, origin, cell, gn, atoms = read_cube(p)
        if ref is None:
            ref = (origin, cell, gn, atoms)
            tot = np.array(data, float)
        else:
            if data.shape != tot.shape or not np.allclose(cell, ref[1], atol=1e-6):
                raise SystemExit(f"⛔ {p}: 격자/셀이 첫 cube 와 다르다 — 합산 불가")
            tot += data
        print(f"   + {Path(p).name}  격자 {data.shape}  적분 {data.sum():.3e}")
    return tot, ref[0], ref[1], ref[2], ref[3]


def pmf_from_density(rho, T):
    rho = np.clip(rho, 0.0, None)
    rmax = float(rho.max())
    if rmax <= 0:
        raise SystemExit("⛔ 밀도가 전부 0")
    with np.errstate(divide="ignore"):
        F = -KB * T * np.log(np.where(rho > 0, rho / rmax, 1e-300))
    return np.minimum(F, F_CAP)


def cluster_curve(F, levels):
    """F 를 올리며 **최대 연결 성분 부피비**(%)를 잰다 (26-연결 + PBC 면 병합).

    ⚠⚠ 왜 필요한가 — **첫-관통과 전이점은 다른 값이다.**
      첫-관통(perc_threshold) = 처음으로 셀을 감는 순간. 그런데 그게 **1.4% 짜리 가는
      실가닥**(유한크기 우연 연결)일 수 있다 (modelc 실측: 0.08 eV 가 그 경우).
      전이점 = 최대 성분이 **급상승**하는 F — 대표 통로가 열리는 지점.
      MASTER(2026-06-21)가 채택한 F* 0.20/0.17 은 **전이점** 정의다.
    """
    tot = F.size
    out = []
    for lv in levels:
        lab = bvp._labels_周期(F <= lv)
        cnt = np.bincount(lab.ravel())
        cnt[0] = 0
        out.append(100.0 * (cnt.max() if cnt.size > 1 else 0) / tot)
    return np.array(out)


def transition_level(levels, pct):
    """최대 성분 곡선의 **최대 상승률** 지점 = 전이점 F*."""
    dp = np.diff(pct) / np.diff(levels)
    k = int(np.argmax(dp))
    return float(0.5 * (levels[k] + levels[k + 1])), float(dp[k])


def analyse(F, cell, T, gate_axes=(2, 4, 8), cap=None):
    """BV 판과 같은 관례로 문턱·경로. fig_bv_path_profile 의 원시함수를 그대로 쓴다."""
    N = np.array(F.shape)
    perc = {}
    for name, need in zip(("F_1D", "F_2D", "F_3D"), gate_axes):
        t = bvp.perc_threshold(F, need)
        perc[name] = t
        print(f"   {name} = {t:.4f} eV" if t is not None else f"   {name} = 없음")
    t = cap if cap is not None else perc["F_1D"]
    if t is None:
        raise SystemExit("⛔ 1D 침투조차 없다 — 표집 부족(궤적이 짧다) 의심")
    T7wind, v = bvp.wrap_witness(F, t)
    if T7wind is None:
        raise SystemExit("⛔ 문턱에서 감김 증인이 없다 (모순)")
    open_axes = {d for d in range(3) if T7wind[d]}
    F2 = F
    for d in sorted(open_axes):
        F2 = np.concatenate([F2, F2], axis=d)
    start = tuple(v)
    tgt = tuple(v[d] + (N[d] if T7wind[d] else 0) for d in range(3))
    path = bvp.dijkstra_valley(F2, start, tgt, open_axes, t, cell, N)
    if path is None:
        raise SystemExit("⛔ 문턱에서 경로가 안 이어진다 (모순)")

    idx = np.array(path, int)                       # BV 판과 동일한 좌표 규약
    phys = np.empty_like(idx)
    for d in range(3):
        n_ax = N[d]
        if d in open_axes:
            phys[:, d] = (idx[:, d] // n_ax) * (n_ax - 1) + idx[:, d] % n_ax
        else:
            phys[:, d] = idx[:, d] % (n_ax - 1)
    dif = np.diff(phys, axis=0)
    for d in range(3):
        if d not in open_axes:
            m = N[d] - 1
            dif[:, d] = (dif[:, d] + m // 2) % m - m // 2
    if np.abs(dif).max() > 1:
        raise SystemExit("⛔ 랩 해제 후에도 |Δindex|>1")
    step = (dif / (N - 1.0)) @ cell
    d_arr = np.concatenate([[0.0], np.cumsum(np.linalg.norm(step, axis=1))])
    e = np.array([F2[tuple(p)] for p in path])
    cart = np.vstack([np.zeros(3), np.cumsum(step, axis=0)]) + \
        (np.array(start, float) / (N - 1.0)) @ cell
    wind = "[" + "".join(str(x) for x in T7wind) + "]"
    print(f"   경로: winding {wind} · {len(path)}점 · 길이 {d_arr[-1]:.1f} Å · "
          f"max {e.max():.4f} eV")
    return {"axis": wind, "d": d_arr, "e": e, "cart": cart, "F_perc": float(t),
            "ref": perc}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", action="append", default=[],
                    help="Li 밀도 cube (여러 번 주면 합산 = 시드 앙상블)")
    ap.add_argument("--T", type=float, required=True, help="MD 온도 (K) — F 스케일에 직결")
    ap.add_argument("--tag", default="sys")
    ap.add_argument("--label", default="")
    ap.add_argument("--out_dir", default=".")
    ap.add_argument("--min_prom", type=float, default=0.02)
    ap.add_argument("--use_transition", action="store_true", default=True,
                    help="경로를 **전이점** 문턱에서 뽑는다 (MASTER 채택 정의; 기본)")
    ap.add_argument("--first_spanning", dest="use_transition", action="store_false",
                    help="대신 첫-관통 문턱을 쓴다 (가는 실가닥일 수 있음)")
    ap.add_argument("--selftest_bv", default=None,
                    help="검증용: cif 로 BV 지도를 만들어 rho=exp(-E/kT) 가짜 밀도로 자체검사")
    a = ap.parse_args()

    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    kT = KB * a.T

    if a.selftest_bv:
        from bvlain import Lain
        calc = Lain(verbose=False)
        calc.read_file(a.selftest_bv)
        E = calc.bvse_distribution(mobile_ion="Li1+", r_cut=bvp.RCUT,
                                   resolution=bvp.RES, k=bvp.K)
        E = E - E.min()
        cell = calc.atoms.cell.array
        atoms = [(s, np.asarray(p)) for s, p in
                 zip(calc.atoms_copy.get_chemical_symbols(), calc.atoms_copy.positions)]
        rho = np.exp(-E / kT)                       # 가짜 볼츠만 밀도
        print(f"[selftest] rho = exp(-E_BV/kT), kT({a.T:.0f} K) = {kT:.4f} eV")
    else:
        if not a.cube:
            raise SystemExit("--cube 또는 --selftest_bv 필요")
        print(f"밀도 cube {len(a.cube)}개 합산:")
        rho, _origin, cell, _gn, atoms = load_density(a.cube)

    F = pmf_from_density(rho, a.T)
    frac0 = float((rho == 0).mean()) if not a.selftest_bv else 0.0
    print(f"PMF: kT = {kT:.4f} eV · F 범위 0–{F[F < F_CAP].max():.3f} eV · "
          f"미방문 voxel {100*frac0:.2f}%")
    if frac0 > 0.60:
        print("⚠ 미방문 voxel 이 60% 를 넘는다 — 궤적이 짧을 가능성. F* 는 상한으로 읽을 것")

    # 첫-관통 vs 전이점 (MASTER 채택 정의 = 전이점)
    lv = np.linspace(0.005, min(0.60, float(F[F < F_CAP].max())), 120)
    pct = cluster_curve(F, lv)
    F_trans, slope = transition_level(lv, pct)
    print(f"클러스터 곡선: 전이점 F* = {F_trans:.4f} eV (최대 상승률 {slope:.0f} %/eV)")

    r = analyse(F, cell, a.T, cap=F_trans if a.use_transition else None)
    r["F_trans"] = F_trans
    r["curve"] = (lv, pct)
    mic = mic_fn(cell)
    cages = cage_centers(atoms, mic)
    d, e, cart = r["d"], r["e"], r["cart"]

    if a.selftest_bv:                               # ★ 단위검사: F 가 E_BV 를 복원하나
        err = float(np.abs(F[F < F_CAP] - E[F < F_CAP]).max())
        print(f"[selftest] max|F − E_BV| = {err:.6f} eV  → "
              f"{'PASS' if err < 1e-6 else 'FAIL'}")
        ref = bvp.perc_threshold(E, 2)
        print(f"[selftest] 문턱 PMF {r['F_perc']:.4f} vs BV {ref:.4f} eV  → "
              f"{'PASS' if abs(r['F_perc']-ref) < 3e-3 else 'FAIL'}")

    # ── 구간 분해 (BV 판과 같은 정의) ──────────────────────────────────
    pk = [i for i in range(1, len(e) - 1) if e[i] > e[i - 1] and e[i] >= e[i + 1]]
    pk = [i for i in pk if e[i] - min(e[:i].min(), e[i:].min()) >= a.min_prom]
    seg, prev = [], 0
    for i in pk:
        j = int(np.argmin(e[prev:i + 1])) + prev
        seg.append((j, i, float(e[i] - e[j]))); prev = i
    vcage = [cage_of(cart[j], cages, mic) for j, _i, _b in seg] + \
            [cage_of(cart[seg[-1][1]], cages, mic)]
    htype = ["inter" if (vcage[k + 1][0] if k + 1 < len(vcage) else vcage[k][0])
             != vcage[k][0] else "intra" for k in range(len(seg))]

    has_li = any(s == "Li" for s, _p in atoms)
    if not has_li:
        print("   (cube 에 Li 원자 없음 = 밀도로만 표현 — 골짜기는 정의상 Li 자리)")
    rows = []
    print(f"\n{a.label or a.tag} · {r['axis']} · {len(seg)} 구간 · "
          f"inter {htype.count('inter')} / intra {htype.count('intra')}")
    for k, (j, i, db) in enumerate(seg, 1):
        vl, dli = label_valley_pmf(cart[j], atoms, mic, has_li)
        sd, wr = label_saddle(cart[i], atoms, mic)
        print(f"  {k}: {d[j]:5.2f}→{d[i]:5.2f} Å  ΔF {db:.3f} eV  [{htype[k-1]}]"
              f" | {vl.replace(chr(10),' ')} | {sd.replace(chr(10),' ')}")
        rows.append({"segment": k, "hop_type": htype[k - 1],
                     "s_valley_A": f"{d[j]:.3f}", "s_saddle_A": f"{d[i]:.3f}",
                     "F_valley_eV": f"{e[j]:.4f}", "F_saddle_eV": f"{e[i]:.4f}",
                     "barrier_eV": f"{db:.4f}", "valley_site": vl.replace("\n", " "),
                     "nearest_Li_A": f"{dli:.2f}", "saddle_window": sd.replace("\n", " "),
                     "window_r_A": f"{wr:.3f}"})

    # ── 산출: 프로파일 CSV · 구간 CSV · 그림 ───────────────────────────
    with open(out / f"{a.tag}_pmf_profile.csv", "w", newline="", encoding="utf-8-sig") as f:
        f.write(f"# MD Li-density PMF percolation-path profile - {a.label or a.tag}, "
                f"T = {a.T:.0f} K, F_perc = {r['F_perc']:.4f} eV, axis {r['axis']}.\n")
        f.write("# F(r) = -kB*T*ln(rho/rho_max) from the time-averaged Li density "
                f"({len(a.cube) or 1} trajectory/ies summed).\n")
        f.write("# Same conventions as the BV figures (26-connectivity percolation, "
                "min-energy-line-integral path, PBC-unwrapped mesh metric).\n")
        f.write("# WARNING: F* is a FREE ENERGY AT THIS TEMPERATURE, not Ea. Sampling-limited "
                "if the trajectory is short - use only for beta-gate-passing systems.\n")
        w = csv.writer(f); w.writerow(["d_A", "F_eV"])
        for x, y in zip(d, e):
            w.writerow([f"{x:.3f}", f"{y:.4f}"])
    with open(out / f"{a.tag}_pmf_segments.csv", "w", newline="", encoding="utf-8-sig") as f:
        f.write(f"# PMF segment barriers - {a.label or a.tag}, T = {a.T:.0f} K, "
                f"F_perc {r['F_perc']:.4f} eV. barrier_eV = F(saddle) - F(preceding valley).\n")
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(out / f"{a.tag}_pmf_cluster.csv", "w", newline="", encoding="utf-8-sig") as f:
        f.write(f"# Largest connected Li cluster vs PMF level - {a.label or a.tag}, "
                f"T = {a.T:.0f} K.\n")
        f.write(f"# First-spanning F* = {r['ref']['F_1D']:.4f} eV ; "
                f"TRANSITION (steepest rise, ADOPTED) F* = {r['F_trans']:.4f} eV.\n")
        w = csv.writer(f); w.writerow(["F_eV", "largest_cluster_pct"])
        for x, y in zip(r["curve"][0], r["curve"][1]):
            w.writerow([f"{x:.4f}", f"{y:.4f}"])
    np.savez_compressed(out / f"{a.tag}_pmf_path.npz", d=d, e=e, cart=cart,
                        cell=cell, F_perc=r["F_perc"], T=a.T, axis=r["axis"],
                        sym=np.array([s for s, _p in atoms]),
                        pos=np.array([p for _s, p in atoms]))

    fig, ax = plt.subplots(figsize=(11.4, 5.6))
    ax.axhspan(0, r["F_perc"], color="#eef6ff", zorder=0)
    ax.plot(d, e, color="#0284c7", lw=2.0, zorder=3)
    ax.axhline(r["F_perc"], ls="--", lw=1.2, color=INK, zorder=2)
    ax.text(d[-1], r["F_perc"] + 0.004, f"$F^*$ = {r['F_perc']:.3f} eV",
            ha="right", fontsize=10, color=INK, fontweight="bold")
    for k, (j, i, db) in enumerate(seg, 1):
        ax.annotate("", xy=(d[i], e[i]), xytext=(d[i], e[j]),
                    arrowprops=dict(arrowstyle="<->", color=MUT, lw=0.9))
        ax.text(d[i] + 0.12, (e[i] + e[j]) / 2, f"{db:.3f}", fontsize=8.5,
                color=INK, va="center", fontweight="bold")
        ax.plot(d[i], e[i], "o", ms=5, mfc="white", mec="#0284c7", mew=1.4, zorder=4)
    ax.set_xlabel("Reaction coordinate (Å)", fontsize=11.5)
    ax.set_ylabel(f"Li free energy, PMF at {a.T:.0f} K (eV)", fontsize=11.5)
    ax.set_title(f"MD Li-density PMF percolation path — {a.label or a.tag}, "
                 f"axis {r['axis']}, T = {a.T:.0f} K", fontsize=12.5,
                 color=INK, fontweight="bold")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.text(0.5, -0.02,
             "F = -kBT ln(rho/rho_max) from the time-averaged Li density of the MD trajectory: "
             "unlike the bond-valence map this includes every Li,\nvacancies, correlated motion "
             "and lattice vibration. F* is a free energy at this temperature — not an "
             "activation energy.", ha="center", fontsize=8.8, color=MUT)
    fig.tight_layout()
    fig.savefig(out / f"{a.tag}_pmf_profile.png", dpi=300, bbox_inches="tight",
                facecolor="white")
    print(f"\n→ {out}/{a.tag}_pmf_profile.png · _pmf_profile.csv · _pmf_segments.csv · _pmf_path.npz")


if __name__ == "__main__":
    main()

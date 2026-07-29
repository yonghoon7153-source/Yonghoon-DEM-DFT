#!/usr/bin/env python3
"""elf_planes_lpsocl.py — 결합별 ELF **2D 평면 slice** (b2o3/LPSCl16 계열과 같은 양식).

왜 별도 드라이버인가
  plot_elf_clean.py 는 **P 중심 모티프(PS4/PS2O2/PS3O)만** 고른다. LPSOCl 에서 정작
  하고 싶은 얘기는 Li–O / Li–Cl / Li–S 라서 P 중심으로는 그 평면을 못 만든다.
  여기선 중심 원자를 자유롭게 잡고(음이온 중심 포함) 평면을 세 원자로 정의한다.
  cube 읽기·컬러맵은 plot_elf_clean.py 에서 그대로 가져와 중복을 안 만든다.

⚠ 축 방향 slice(xy/xz/yz)를 쓰면 안 된다 — 비직교 셀에서 사다리꼴로 찌그러진다.
  세 원자로 평면을 정의해야 셀 모양과 무관하게 같은 축척으로 비교된다.

⚠ 이 스크립트는 **cube 가 있는 기계에서 돌린다**(gabia). cube 는 수십 MB라 repo 로
  못 옮긴다. PNG 도 base64 회수 한도를 넘으므로 **gabia 에서 직접 내려받는다**:
      scp root@121.78.116.27:/data/work/runs/lpsocl_elf/postproc/planes/'*.png' .
  대신 각 평면의 **판정 수치**(결합 위 최소 ELF 등)는 작은 CSV 로 같이 내보내
  repo 에 등록한다.

  python3 tools/figures/elf_planes_lpsocl.py \\
      --cube /data/work/runs/lpsocl_elf/lpsocl_elf.cube \\
      --out  /data/work/runs/lpsocl_elf/postproc/planes \\
      --label "LPSOCl (Li27P5S21OCl8)" --tag lpsocl
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import map_coordinates

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plot_elf_clean import read_cube, elf_cmap                       # noqa: E402

# 원자 마커 색 — plot_elf_plane.py 의 VESTA 풍 팔레트와 맞춘다(하우스 팔레트가 아니라
# 여기선 진한 ELF 배경 위 가독성이 우선).
ELEM_COLOR = {"Li": "#111111", "P": "#FF9933", "S": "#FFDC52", "Cl": "#3E8E41",
              "O": "#E8482B", "B": "#2ea3f2", "N": "#3050F8"}
# 결합 판정 컷오프 (Å) — sample_elf_bonds.py 의 CUT 표와 같은 계열
CUT = {("P", "S"): 2.4, ("P", "O"): 1.9, ("Li", "S"): 3.0,
       ("Li", "Cl"): 3.1, ("Li", "O"): 2.5}


def cut(a, b):
    return CUT.get((a, b), CUT.get((b, a), 2.8))


def neighbors(sym, pos, mic, i, elem, rmax):
    """i 원자 주변 elem 이웃을 거리순으로 [(d, j), …]."""
    out = [(float(np.linalg.norm(mic(pos[j] - pos[i]))), j)
           for j in range(len(sym)) if sym[j] == elem and j != i]
    return sorted(d for d in out if d[0] <= rmax)


MIN_SIN = 0.34          # ~20° — 이보다 일직선에 가까우면 평면으로 못 쓴다


def pick_B(p0, iA, cands, pos, mic, min_sin=MIN_SIN):
    """A 와 (거의) 일직선이 아닌 가장 가까운 두 번째 이웃.

    ⚠⚠ **일직선이면 cross(e1, B−p0) = 0 이라 법선이 NaN 이 되고 평면이 통째로
      깨진다.** trans 배위(Li–Cl–Li 180°, Li–S–Li)는 실제 구조에서 흔해서
      "가장 가까운 둘"을 그냥 집으면 조용히 빈 그림이 나온다.
    """
    eA = mic(pos[iA] - p0); eA = eA / np.linalg.norm(eA)
    for _, j in cands:
        if j == iA:
            continue
        v = mic(pos[j] - p0)
        n = np.linalg.norm(v)
        if n < 1e-6:
            continue
        if np.linalg.norm(np.cross(eA, v / n)) >= min_sin:
            return j
    return None


def pick_planes(sym, pos, mic, want):
    """모티프 이름 → (center, A, B) 인덱스. 못 찾으면 그 항목만 건너뛴다.

    ⚠ 평면은 **결합 두 개를 한 화면에** 담도록 고른다 — 결합 하나만 있는 평면은
      '주변보다 진한가'를 눈으로 못 재서 그림으로서 쓸모가 적다.
    """
    P = [i for i, s in enumerate(sym) if s == "P"]
    Li = [i for i, s in enumerate(sym) if s == "Li"]
    O = [i for i, s in enumerate(sym) if s == "O"]
    Cl = [i for i, s in enumerate(sym) if s == "Cl"]
    S = [i for i, s in enumerate(sym) if s == "S"]
    got = {}

    for i in P:                                   # PS4 = O 이웃이 없는 P
        nO = neighbors(sym, pos, mic, i, "O", cut("P", "O"))
        nS = neighbors(sym, pos, mic, i, "S", cut("P", "S"))
        if "PS4" not in got and not nO and len(nS) >= 2:
            jB = pick_B(pos[i], nS[0][1], nS, pos, mic)
            if jB is not None:
                got["PS4"] = (i, nS[0][1], jB)
        if "PS3O" not in got and len(nO) == 1 and nS:   # O 치환된 P — P–O 와 P–S 한 평면
            jB = pick_B(pos[i], nO[0][1], nS, pos, mic)
            if jB is not None:
                got["PS3O"] = (i, nO[0][1], jB)

    for i in O:                                   # O 중심: P–O 와 Li–O 를 한 평면에
        nP = neighbors(sym, pos, mic, i, "P", cut("P", "O"))
        nLi = neighbors(sym, pos, mic, i, "Li", cut("Li", "O"))
        if nP and nLi:
            jB = pick_B(pos[i], nP[0][1], nLi, pos, mic)
            if jB is not None:
                got["O_PLi"] = (i, nP[0][1], jB)
                break

    for i in Cl:                                  # Cl 중심: Li 두 개 (Li–Cl 두 결합)
        nLi = neighbors(sym, pos, mic, i, "Li", cut("Li", "Cl"))
        jB = pick_B(pos[i], nLi[0][1], nLi, pos, mic) if nLi else None
        if jB is not None:
            got["ClLi2"] = (i, nLi[0][1], jB)
            break

    for i in S:                                   # free S²⁻ (P 이웃 없음) 중심 + Li 두 개
        nP = neighbors(sym, pos, mic, i, "P", cut("P", "S"))
        nLi = neighbors(sym, pos, mic, i, "Li", cut("Li", "S"))
        jB = pick_B(pos[i], nLi[0][1], nLi, pos, mic) if nLi else None
        if not nP and jB is not None:
            got["SfreeLi2"] = (i, nLi[0][1], jB)
            break
    if "SfreeLi2" not in got:                     # free S 가 없으면 PS4-S 로 대체
        for i in S:
            nLi = neighbors(sym, pos, mic, i, "Li", cut("Li", "S"))
            jB = pick_B(pos[i], nLi[0][1], nLi, pos, mic) if nLi else None
            if jB is not None:
                got["SLi2"] = (i, nLi[0][1], jB)
                break
    return {k: v for k, v in got.items() if not want or k in want}


TITLE = {"PS4": "PS$_4$ — host P–S", "PS3O": "PS$_3$O — P–O vs P–S in one plane",
         "O_PLi": "O site — P–O (covalent) vs Li–O (ionic)",
         "ClLi2": "Cl site — Li–Cl", "SfreeLi2": "free S$^{2-}$ — Li–S",
         "SLi2": "S site — Li–S"}


def sample_plane(data, origin, cell, gn, p0, A, B, half, n):
    """세 원자로 정의한 평면 위 ELF.

    ⚠ 화면 중심은 중심원자가 아니라 **세 원자의 무게중심**이다. 중심원자에 맞추면
      결합이 전부 한쪽 사분면으로 몰려 프레임 절반이 빈다(실측). 기저(e1,e2)는
      그대로 p0→A 로 잡아 방향 규약은 유지한다.
    """
    cinv = np.linalg.inv(cell)
    e1 = (A - p0); e1 /= np.linalg.norm(e1)
    nrm = np.cross(e1, B - p0); nrm /= np.linalg.norm(nrm)
    e2 = np.cross(nrm, e1)
    c0 = (p0 + A + B) / 3.0
    us = np.linspace(-half, half, n)
    U, V = np.meshgrid(us, us)
    R = c0[None, :] + U.ravel()[:, None] * e1 + V.ravel()[:, None] * e2
    F = ((R - origin) @ cinv) % 1.0
    img = map_coordinates(data, (F * gn).T, order=1, mode="grid-wrap").reshape(n, n)
    return img, us, e1, e2, nrm, c0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", required=True)
    ap.add_argument("--out", required=True, help="출력 디렉터리")
    ap.add_argument("--label", default="")
    ap.add_argument("--tag", default="sys")
    ap.add_argument("--motifs", nargs="*", default=None,
                    help="기본은 찾은 것 전부. 예: PS4 PS3O O_PLi ClLi2 SfreeLi2")
    ap.add_argument("--half", type=float, default=4.0, help="반폭 (Å)")
    ap.add_argument("--n", type=int, default=480)
    ap.add_argument("--thickness", type=float, default=1.3,
                    help="평면에서 이 거리(Å) 안의 원자만 표시")
    ap.add_argument("--dpi", type=int, default=300)
    a = ap.parse_args()

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    data, origin, cell, gn, atoms = read_cube(a.cube)
    sym = [x[0] for x in atoms]; pos = np.array([x[1] for x in atoms])
    cell_invT = np.linalg.inv(cell.T)

    def mic(d):
        f = cell_invT @ d; f -= np.round(f); return cell.T @ f

    planes = pick_planes(sym, pos, mic, a.motifs)
    if not planes:
        raise SystemExit("모티프를 하나도 못 찾았다 — --motifs 지정하거나 CUT 표 확인")
    print(f"{len(planes)} 개 평면: {', '.join(planes)}")

    rows, imgs = [], {}
    for name, (i0, iA, iB) in planes.items():
        p0 = pos[i0]
        A = p0 + mic(pos[iA] - p0); B = p0 + mic(pos[iB] - p0)
        img, us, e1, e2, nrm, c0 = sample_plane(data, origin, cell, gn, p0, A, B, a.half, a.n)
        imgs[name] = (img, us)
        dA, dB = np.linalg.norm(A - p0), np.linalg.norm(B - p0)
        print(f"  {name:10s} center atom{i0+1}({sym[i0]}) "
              f"A atom{iA+1}({sym[iA]},{dA:.2f}Å) B atom{iB+1}({sym[iB]},{dB:.2f}Å)")

        # ── clean (논문용, 크롬 없음) ─────────────────────────────────────
        fig = plt.figure(figsize=(6, 6)); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
        ax.imshow(img, origin="lower", extent=[-a.half, a.half, -a.half, a.half],
                  cmap=elf_cmap(), vmin=0, vmax=1, aspect="equal", interpolation="bilinear")
        f_clean = out / f"elf_plane_{a.tag}_{name}.png"
        fig.savefig(f_clean, dpi=a.dpi); plt.close(fig)

        # ── labeled (원자·등고선·컬러바) ─────────────────────────────────
        fig, ax = plt.subplots(figsize=(7.4, 6.6))
        im = ax.imshow(img, origin="lower", extent=[-a.half, a.half, -a.half, a.half],
                       cmap=elf_cmap(), vmin=0, vmax=1, aspect="equal",
                       interpolation="bilinear")
        cb = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02); cb.set_label("ELF", fontsize=12)
        ax.contour(us, us, img, levels=[0.30, 0.70], colors=["white", "black"],
                   linewidths=[1.0, 1.2], linestyles=["--", "-"])
        for k in range(len(sym)):
            d = c0 + mic(pos[k] - c0) - c0        # 무게중심 기준 (MIC 로 최근접 상)
            u, v, w = float(d @ e1), float(d @ e2), float(d @ nrm)
            if abs(w) > a.thickness or abs(u) > a.half or abs(v) > a.half:
                continue
            ax.plot(u, v, "o", mfc=ELEM_COLOR.get(sym[k], "#888"), mec="white",
                    mew=0.9, ms=9, zorder=5)
            ax.text(u + 0.18, v + 0.18, sym[k], fontsize=8, color="white", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.12", fc="black", alpha=0.55, ec="none"))
        ax.set_xlabel("in-plane x (Å)"); ax.set_ylabel("in-plane y (Å)")
        ax.set_title(f"{TITLE.get(name, name)} — {a.label}", fontsize=11.5)
        ax.text(0.99, 0.015, "solid 0.70 (covalent) · dashed 0.30 (ionic)",
                transform=ax.transAxes, ha="right", fontsize=8, color="white")
        fig.tight_layout()
        f_lab = out / f"{a.tag}_elf_plane_{name}.png"
        fig.savefig(f_lab, dpi=220, facecolor="white", bbox_inches="tight"); plt.close(fig)

        # ── 판정 수치: 두 결합선 위 ELF 최솟값 ([0.40,0.60] 규약과 동일) ────
        for lab, tgt in (("A", A), ("B", B)):
            j = iA if lab == "A" else iB
            ts = np.linspace(0.40, 0.60, 9)
            vals = []
            for t in ts:
                r = p0 + (tgt - p0) * t
                f = ((r - origin) @ np.linalg.inv(cell)) % 1.0
                vals.append(float(map_coordinates(data, (f * gn)[:, None], order=1,
                                                  mode="grid-wrap")[0]))
            rows.append([a.tag, name, f"{sym[i0]}-{sym[j]}",
                         f"{np.linalg.norm(tgt - p0):.3f}", f"{min(vals):.4f}"])
        print(f"    → {f_clean.name} · {f_lab.name}")

    # ── 몽타주 (한 장에 전부) ────────────────────────────────────────────
    ks = list(imgs)
    ncol = min(3, len(ks)); nrow = int(np.ceil(len(ks) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.5 * ncol, 4.8 * nrow), squeeze=False)
    for ax in axes.ravel():
        ax.axis("off")
    for ax, name in zip(axes.ravel(), ks):
        img, us = imgs[name]
        ax.imshow(img, origin="lower", extent=[-a.half, a.half, -a.half, a.half],
                  cmap=elf_cmap(), vmin=0, vmax=1, aspect="equal", interpolation="bilinear")
        ax.set_title(TITLE.get(name, name), fontsize=10)
        ax.axis("off")
    fig.suptitle(f"ELF planes — {a.label}", fontsize=12)
    fig.tight_layout()
    f_m = out / f"{a.tag}_elf_planes.png"
    fig.savefig(f_m, dpi=200, facecolor="white", bbox_inches="tight"); plt.close(fig)
    print(f"→ 몽타주 {f_m.name}")

    f_csv = out / f"{a.tag}_elf_planes.csv"
    with open(f_csv, "w", newline="", encoding="utf-8-sig") as f:
        f.write("# ELF plane slices — 평면 위 결합의 central min ([0.40,0.60] 규약)\n")
        f.write("# 그림 자체는 gabia 에 있다(PNG 는 base64 회수 한도 초과). scp 로 받는다.\n")
        w = csv.writer(f)
        w.writerow(["system", "motif", "bond", "dist_A", "central_min"])
        w.writerows(rows)
    print(f"→ {f_csv}  (이건 작아서 회수 가능)")
    print("\n회수: base64 -w 200 " + str(f_csv))
    print("그림:  scp root@121.78.116.27:'" + str(out) + "/*.png' .")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""ELF line profiles along bonds — the quantitative covalent-vs-ionic discriminator.

Samples ELF on the straight line between two atoms (periodic MIC) and plots ELF
vs fractional bond coordinate (0 = atom A, 1 = atom B). Signature:
  * COVALENT (P-S): a bond ATTRACTOR = local ELF maximum BETWEEN the two cores
    (off-nucleus, value ~0.8+).
  * IONIC (Li-Cl, Li-S): NO between-bond attractor; ELF is the superposition of
    the two atomic shells with a MINIMUM (saddle) between them — high only on the
    anion's closed shell, ~0 on Li+.

Auto-picks one representative P-S, Li-Cl, Li-S(free) bond unless --pairs given.
Pure numpy. Reads a QE plot_num=8 ELF cube.

Usage:
  python3 plot_elf_profile.py --cube V0_ELF.cube --out comp1_ELF_profiles.png --label "LPSCl"
  python3 plot_elf_profile.py --cube X.cube --pairs 47 42 1 5 --out y.png   # A B A B (1-based)
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BOHR = 0.5291772108
PT = {3: "Li", 7: "N", 8: "O", 9: "F", 11: "Na", 15: "P", 16: "S", 17: "Cl", 35: "Br", 60: "Nd"}
PS_BOND = 2.35  # P-S cutoff to find free S


def read_cube(path):
    L = open(path).read().splitlines()
    nat = int(L[2].split()[0])
    origin = np.array([float(x) for x in L[2].split()[1:4]]) * BOHR
    gn, vox = [], []
    for i in range(3):
        p = L[3 + i].split()
        gn.append(int(p[0])); vox.append([float(x) for x in p[1:4]])
    gn = np.array(gn); cell = np.array(vox) * BOHR * gn[:, None]
    atoms = []
    for i in range(nat):
        p = L[6 + i].split()
        atoms.append((PT.get(int(p[0]), str(p[0])),
                      np.array([float(x) for x in p[2:5]]) * BOHR))
    data = np.array(" ".join(L[6 + nat:]).split(), float).reshape(*gn)
    return data, origin, cell, gn, atoms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--pairs", type=int, nargs="+", default=None,
                    help="flat list of 1-based atom index pairs A B A B ...")
    ap.add_argument("--n", type=int, default=200)
    # ⚠ 그림만 내면 원고에서 다시 못 쓴다 — 곡선 자체를 Origin-ready CSV 로 같이 낸다.
    ap.add_argument("--csv", default=None, help="결합별 ELF 프로파일 CSV")
    args = ap.parse_args()

    data, origin, cell, gn, atoms = read_cube(args.cube)
    cinvT = np.linalg.inv(cell.T)
    syms = [a[0] for a in atoms]; pos = np.array([a[1] for a in atoms])

    def mic(d):
        f = cinvT @ d; f -= np.round(f); return cell.T @ f

    def elf_at(r):
        f = (cinvT @ (r - origin)) % 1.0
        g = f * gn; i0 = np.floor(g).astype(int); d = g - i0
        val = 0.0
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    w = ((d[0] if dx else 1 - d[0]) * (d[1] if dy else 1 - d[1])
                         * (d[2] if dz else 1 - d[2]))
                    val += w * data[(i0[0]+dx) % gn[0], (i0[1]+dy) % gn[1], (i0[2]+dz) % gn[2]]
        return val

    def nearest(i, elem):
        cand = [(np.linalg.norm(mic(pos[k] - pos[i])), k)
                for k in range(len(atoms)) if syms[k] == elem and k != i]
        return min(cand)[1] if cand else None

    # build bond list
    bonds = []  # (labelA, iA, labelB, iB, color)
    if args.pairs:
        idx = [k - 1 for k in args.pairs]
        for a, b in zip(idx[0::2], idx[1::2]):
            bonds.append((syms[a], a, syms[b], b))
    else:
        P = [k for k in range(len(atoms)) if syms[k] == "P"]
        Cl = [k for k in range(len(atoms)) if syms[k] == "Cl"]
        # free S = S not within PS_BOND of any P
        freeS = [k for k in range(len(atoms)) if syms[k] == "S" and
                 min((np.linalg.norm(mic(pos[k] - pos[p])) for p in P), default=9) > PS_BOND]
        if P:
            iP = P[len(P)//2]; iS = nearest(iP, "S"); bonds.append(("P", iP, "S", iS))
        if Cl:
            iCl = Cl[len(Cl)//2]; iLi = nearest(iCl, "Li"); bonds.append(("Cl", iCl, "Li", iLi))
        if freeS:
            iFS = freeS[len(freeS)//2]; iLi2 = nearest(iFS, "Li"); bonds.append(("S(free)", iFS, "Li", iLi2))
        # ⚠ O 결합이 기본 탐색에 없었다 — LPSOCl/b2o3 에서 **정작 보고 싶은 결합**이 빠졌다.
        #   P-O 는 격자 최강(ICOHP -8.41), Li-O 는 최이온(ELF cmin 0.163)이라 둘 다 필요하다.
        O = [k for k in range(len(atoms)) if syms[k] == "O"]
        if O and P:
            # P 에 결합한 O (POS3 단위) 를 고른다 — 없으면 그냥 첫 O
            iO = next((k for k in O if min(np.linalg.norm(mic(pos[k] - pos[q]))
                                           for q in P) < 1.9), O[0])
            iPo = min(P, key=lambda q: np.linalg.norm(mic(pos[iO] - pos[q])))
            bonds.append(("P", iPo, "O", iO))
            iLiO = nearest(iO, "Li")
            if iLiO is not None:
                bonds.append(("O", iO, "Li", iLiO))
        B = [k for k in range(len(atoms)) if syms[k] == "B"]
        if B:                       # b2o3 계 — BS3 단위
            iB = B[0]; iSb = nearest(iB, "S")
            if iSb is not None:
                bonds.append(("B", iB, "S", iSb))

    # house_style 원소 팔레트와 맞춘다 (P 보라 · S 시에나 · Cl 라임 · O 크림슨 · B 스카이)
    COL = {"P-S": "#7c3aed", "Cl-Li": "#65a30d", "S(free)-Li": "#c05621",
           "Li-Cl": "#65a30d", "Li-S(free)": "#c05621",
           "P-O": "#be123c", "O-Li": "#be123c", "Li-O": "#be123c", "B-S": "#0284c7"}
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    t = np.linspace(0, 1, args.n)
    curves = {}          # {bond: (length_A, profile)} — CSV 용
    print(f"[{args.label}] ELF bond profiles:")
    for la, ia, lb, ib in bonds:
        A = pos[ia]; B = A + mic(pos[ib] - A)
        L = np.linalg.norm(B - A)
        prof = np.array([elf_at(A + tt * (B - A)) for tt in t])
        # interior max (exclude ~18% near each nucleus core spike)
        interior = (t > 0.18) & (t < 0.82)
        imax = np.argmax(prof[interior]); tmax = t[interior][imax]; vmax = prof[interior][imax]
        imin = np.argmin(prof[interior]); vmin = prof[interior][imin]
        key = f"{la}-{lb}"
        curves[key] = (L, prof)
        c = COL.get(key, COL.get(f"{lb}-{la}", "#666"))
        ionic = vmin < 0.18
        kind = "ionic (deep moat)" if ionic else "covalent (bond maintained)"
        ax.plot(t, prof, lw=2.4, color=c,
                label=f"{la}–{lb} ({L:.2f} Å): bond-min ELF {vmin:.2f} → {kind.split()[0]}")
        # mark the moat/attractor minimum
        tmin = t[interior][imin]
        ax.plot(tmin, vmin, "v" if ionic else "o", color=c, ms=8, mec="k", mew=0.6, zorder=5)
        print(f"  {la}{ia+1}-{lb}{ib+1}  L={L:.2f} A  interior ELF min={vmin:.3f}@t={tmin:.2f} "
              f"max={vmax:.3f}  -> {kind}")

    ax.axhline(0.5, color="grey", ls=":", lw=0.8)
    ax.text(0.015, 0.51, "0.5 (homogeneous e-gas)", fontsize=8, color="grey")
    ax.set_xlabel("fractional bond coordinate  (0 = first atom → 1 = second atom)", fontsize=11)
    ax.set_ylabel("ELF", fontsize=12)
    ax.set_ylim(0, 1.02)
    ax.set_title(f"ELF bond profiles — covalent P–S (hump between) vs ionic Li–Cl/Li–S\n{args.label}",
                 fontsize=11.5)
    ax.legend(fontsize=9, loc="lower center"); ax.grid(alpha=0.25)
    if args.csv:
        import csv as _csv
        with open(args.csv, "w", newline="", encoding="utf-8-sig") as _f:
            _f.write("# ELF profile along each bond path — Origin-ready\n")
            _f.write("# frac = 0 at first atom, 1 at second. 결합 길이는 열 이름에 (Å).\n")
            _f.write("# ⚠ 판정은 **내부 최솟값**(frac 0.18~0.82)으로 — 핵 근처 스파이크 제외.\n")
            _w = _csv.writer(_f)
            _ks = list(curves)
            _w.writerow(["frac"] + [f"ELF_{k}_{curves[k][0]:.2f}A" for k in _ks])
            for _i, _tt in enumerate(t):
                _w.writerow([f"{_tt:.4f}"] + [f"{curves[k][1][_i]:.5f}" for k in _ks])
        print(f"  -> CSV {args.csv}")
    plt.tight_layout(); plt.savefig(args.out, dpi=200, facecolor="white")
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Nd2O3-doped modelc DOS/PDOS -> Origin CSV + matplotlib preview (nspin=2, site-resolved Nd 4f).

Run in the KISTI v0_champion dir (uma env: numpy+matplotlib) where V0_dos.dat and
the 300 V0_pdos.pdos_atm#*(X)_wfc#*(l) files live. Handles:
  - nspin=2 total DOS (dos.dat cols: E, dosup, dosdw, intdos) -> total = up+dn
  - species labels with digits (Nd1/Nd2) -> grouped as element "Nd" for totals,
    kept SEPARATE for the 4f (the two inequivalent sites: oxy-bound vs sulfide)
  - PDOS files have their own energy grid (projwfc) distinct from dos.dat (dos.x)

Outputs (scp these off KISTI):
  nd_dos_origin.csv   E-EF, total, up, -dn         (dos.dat grid; -dn for mirror plot)
  nd_pdos_origin.csv  E-EF, Li,P,S,Cl,O,Nd, Nd1_4f, Nd2_4f   (pdos grid)
  nd_dos_pdos.png     quick preview

Provenance note: current data is from the k441 SCF (dos.in prefix nd_pair01_v0_k441);
the k661 nscf crashed on nbnd mismatch (466 requested vs 359 saved). Qualitative
features (clean gap, Nd 4f out of gap, O 2p deep in VB, no defect band) are k-robust;
re-run with k661 (nbnd=359) only if a smooth publication curve / matched-k gap is needed.
"""
import glob
import re
import numpy as np

DOS = "V0_dos.dat"
PDOS_GLOB = "V0_pdos.pdos_atm*"
WFC_RE = re.compile(r"\(([A-Za-z]+\d*)\)_wfc#\d+\(([a-z])\)")


def ef_from_header(path):
    return float(re.search(r"EFermi\s*=\s*([\-\d.]+)", open(path).readline()).group(1))


def main():
    EF = ef_from_header(DOS)
    d = np.loadtxt(DOS)
    E = d[:, 0] - EF
    up, dn = d[:, 1], d[:, 2]
    tot = up + dn

    files = glob.glob(PDOS_GLOB)
    Ep = np.loadtxt(files[0])[:, 0] - EF

    def summ(species_pat, orb=None):
        s = np.zeros_like(Ep)
        for f in files:
            m = WFC_RE.search(f)
            if not m:
                continue
            sp, o = m.group(1), m.group(2)
            if not re.fullmatch(species_pat, sp):
                continue
            if orb and o != orb:
                continue
            a = np.loadtxt(f)
            s += a[:, 1] + a[:, 2]      # nspin=2: ldos up + dn
        return s

    elems = {"Li": "Li", "P": "P", "S": "S", "Cl": "Cl", "O": "O", "Nd": r"Nd\d?"}
    pe = {k: summ(p) for k, p in elems.items()}
    nd1_4f = summ("Nd1", "f")
    nd2_4f = summ("Nd2", "f")

    with open("nd_dos_origin.csv", "w") as fo:
        fo.write("E-EF,DOS_total,DOS_up,DOS_dn\neV,states/eV,up,dn(mirrored)\n")
        for i in range(len(E)):
            fo.write(f"{E[i]:.4f},{tot[i]:.5g},{up[i]:.5g},{-dn[i]:.5g}\n")

    with open("nd_pdos_origin.csv", "w") as fo:
        cols = ["E-EF"] + list(pe) + ["Nd1_4f", "Nd2_4f"]
        fo.write(",".join(cols) + "\n")
        for i in range(len(Ep)):
            fo.write(",".join([f"{Ep[i]:.4f}"]
                              + [f"{pe[k][i]:.5g}" for k in pe]
                              + [f"{nd1_4f[i]:.5g}", f"{nd2_4f[i]:.5g}"]) + "\n")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        col = {"Li": "tab:blue", "P": "tab:orange", "S": "tab:green",
               "Cl": "tab:purple", "O": "tab:red", "Nd": "tab:cyan"}
        fig, ax = plt.subplots(figsize=(9, 5.5))
        ax.plot(E, tot, color="black", lw=1.5, label="Total", zorder=5)
        for k in ["S", "P", "Cl", "O", "Li", "Nd"]:
            ax.fill_between(Ep, 0, pe[k], color=col[k], alpha=0.4, label=k)
        ax.plot(Ep, nd1_4f, color="magenta", lw=1.4, ls="--", label="Nd1 4f (oxy)")
        ax.plot(Ep, nd2_4f, color="saddlebrown", lw=1.4, ls=":", label="Nd2 4f (sulfide)")
        ax.axvline(0, color="gray", ls="--", lw=1.0, label=r"$E_F$")
        ax.set_xlim(-7, 4)
        ax.set_ylim(bottom=0)
        ax.set_xlabel(r"$E - E_F$ (eV)", fontsize=13)
        ax.set_ylabel("DOS (states/eV)", fontsize=13)
        ax.legend(loc="upper right", fontsize=9, ncol=2, framealpha=0.95)
        ax.grid(alpha=0.3)
        ax.set_title(r"Nd$_2$O$_3$-doped modelc — DOS/PDOS (k441)", fontsize=13)
        plt.tight_layout()
        plt.savefig("nd_dos_pdos.png", dpi=200, facecolor="white", bbox_inches="tight")
        print("-> nd_dos_pdos.png")
    except Exception as e:
        print(f"(plot skipped: {e})")

    print("-> nd_dos_origin.csv, nd_pdos_origin.csv")
    print(f"EF={EF:.3f} eV  (E axis already shifted to E-EF)")


if __name__ == "__main__":
    main()

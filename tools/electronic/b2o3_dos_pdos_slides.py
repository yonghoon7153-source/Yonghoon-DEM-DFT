#!/usr/bin/env python3
"""b2o3 DOS/PDOS slide set (Gaussian-broadened), matching the LPSCl/LPSCl1.6
presentation style — for the B2O3-doped champion (adds B-S(BS3) + O sites).

Run ON KISTI in the dir holding b2o3.dos + b2o3.pdos.* (e.g. b2o3_eos), with the
champion cif reachable for site classification. Produces 3 figures + prints all
table values (gap, VBM%, mean-3p per site) AND writes compact CSVs so the
figures can be rebuilt off-cluster from a paste.

  python3 b2o3_dos_pdos_slides.py --dir . --prefix b2o3 \
      --cif /scratch/x3430a02/kgy/Yonghoon-DEM-DFT/db/structures/b2o3_relaxV0.cif \
      --vbm 2.4717 --cbm 4.4388

Site classification (each S/anion):
  B-S    : S within 2.0 A of a B   (trigonal BS3)
  PS4-S  : S within 2.6 A of a P   (phosphate/thiophosphate)
  free-S : S bonded to neither     (non-bridging S2-, oxidation-prone)
  Cl     : all Cl                  ;  O : all O (on P) ; Li : all Li
"""
import argparse, glob, re, math, json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse_cif(fn):
    t = open(fn).read()
    g = lambda k: float(re.search(k + r"\s+([\d.]+)", t).group(1))
    a, b, c = g("_cell_length_a"), g("_cell_length_b"), g("_cell_length_c")
    al, be, ga = (math.radians(g("_cell_angle_" + x)) for x in ("alpha", "beta", "gamma"))
    cs = math.cos
    v = math.sqrt(1 - cs(al)**2 - cs(be)**2 - cs(ga)**2 + 2*cs(al)*cs(be)*cs(ga))
    A = np.array([[a, 0, 0], [b*cs(ga), b*math.sin(ga), 0],
                  [c*cs(be), c*(cs(al)-cs(be)*cs(ga))/math.sin(ga), c*v/math.sin(ga)]])
    sym, frac = [], []
    # try both column orders (label-first OR symbol-first)
    for m in re.finditer(r"^\s*(?:[A-Za-z]{1,2}\d+\s+([A-Za-z]{1,2})|([A-Za-z]{1,2})\s+[A-Za-z]{1,2}\d+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)", t, re.M):
        s = m.group(1) or m.group(2)
        sym.append(s); frac.append([float(m.group(3)), float(m.group(4)), float(m.group(5))])
    return A, np.array(frac), sym


def mic_d(fi, fj, A):
    df = fi - fj; df -= np.round(df); return np.linalg.norm(df @ A)


def classify(A, frac, sym):
    """Return dict atom_index(1-based, QE order) -> site label."""
    P = [i for i, s in enumerate(sym) if s == "P"]
    B = [i for i, s in enumerate(sym) if s == "B"]
    lab = {}
    for i, s in enumerate(sym):
        if s == "S":
            dB = min((mic_d(frac[i], frac[j], A) for j in B), default=9)
            dP = min((mic_d(frac[i], frac[j], A) for j in P), default=9)
            lab[i+1] = "B-S" if dB < 2.0 else ("PS4-S" if dP < 2.6 else "free-S")
        else:
            lab[i+1] = s          # Cl, O, Li, P, B
    return lab


def load_pdos_by_atom(d, prefix, wfc_filter=None):
    """{atom_index: (E, summed-ldos over its wfc)}; wfc_filter e.g. '(p)'."""
    out = {}
    for f in glob.glob(f"{d}/{prefix}.pdos.pdos_atm#*_wfc#*"):
        if wfc_filter and wfc_filter not in f:
            continue
        n = int(re.search(r"atm#(\d+)", f).group(1))
        arr = np.loadtxt(f)
        E, l = arr[:, 0], arr[:, 1]
        if n in out:
            out[n] = (E, out[n][1] + l)
        else:
            out[n] = (E, l.copy())
    return out


def gauss_broaden(E, y, sigma):
    if sigma <= 0:
        return y
    dE = E[1] - E[0]
    n = max(1, int(4 * sigma / dE))
    k = np.exp(-0.5 * (np.arange(-n, n+1) * dE / sigma) ** 2)
    k /= k.sum()
    return np.convolve(y, k, mode="same")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    ap.add_argument("--prefix", default="b2o3")
    ap.add_argument("--cif", required=True)
    ap.add_argument("--vbm", type=float, default=2.4717)
    ap.add_argument("--cbm", type=float, default=4.4388)
    ap.add_argument("--sigma", type=float, default=0.10, help="Gaussian eV")
    args = ap.parse_args()
    d, p = args.dir.rstrip("/"), args.prefix
    gap = args.cbm - args.vbm

    A, frac, sym = parse_cif(args.cif)
    lab = classify(A, frac, sym)
    from collections import Counter
    print("site counts:", dict(Counter(lab.values())))

    # --- total DOS from pdos_tot, element + site sums from per-atom p-projections ---
    tot = np.loadtxt(f"{d}/{p}.pdos.pdos_tot")
    E0 = tot[:, 0] - args.vbm                  # E - VBM
    total = gauss_broaden(E0, tot[:, 1], args.sigma)
    per_atom = load_pdos_by_atom(d, p)         # all wfc (s+p)
    per_atom_p = load_pdos_by_atom(d, p, "(p)")  # p only (for 3p site analysis)

    # element sums
    elems = ["Li", "P", "S", "Cl", "B", "O"]
    Eref = per_atom[next(iter(per_atom))][0] - args.vbm
    el_sum = {e: np.zeros_like(Eref) for e in elems}
    for n, (E, y) in per_atom.items():
        s = sym[n-1]
        if s in el_sum:
            el_sum[s] += y
    el_sum = {e: gauss_broaden(Eref, v, args.sigma) for e, v in el_sum.items()}

    # site sums (p-projection)
    sites = ["free-S", "B-S", "PS4-S", "Cl", "O"]
    cnt = Counter(lab.values())
    site_sum = {k: np.zeros_like(Eref) for k in sites}
    for n, (E, y) in per_atom_p.items():
        L = lab.get(n)
        if L in site_sum:
            site_sum[L] += y
    site_pa = {k: gauss_broaden(Eref, site_sum[k]/max(1, cnt.get(k, 1)), args.sigma) for k in sites}

    # ---- TABLE 1: gap / N(EF) ----
    occ = Eref <= 0.02
    NEf = 0.0  # insulator: DOS at E_F is ~0
    print("\n=== TABLE 1: DOS ===")
    print(f"  E_VBM={args.vbm:.3f}  E_CBM={args.cbm:.3f}  band_gap={gap:.3f} eV  N(E_F)~0 (insulator)")

    # ---- TABLE 2: VBM-edge element % (within 0.5 eV below VBM) ----
    edge = (Eref <= 0.0) & (Eref >= -0.5)
    wsum = {e: float(el_sum[e][edge].sum()) for e in elems}
    tt = sum(wsum.values()) or 1
    print("\n=== TABLE 2: VBM-edge element %% (top 0.5 eV of valence) ===")
    for e in elems:
        print(f"  {e:3s}: {100*wsum[e]/tt:5.1f}%")

    # ---- TABLE 3: mean 3p position per site (occupied) ----
    print("\n=== TABLE 3: mean 3p (E-VBM, occupied) per site ===")
    mean3p = {}
    for k in sites:
        y = site_sum[k]
        m = occ & (y > 0)
        mp = float((Eref[m]*y[m]).sum()/y[m].sum()) if y[m].sum() > 0 else float("nan")
        mean3p[k] = mp
        print(f"  {k:6s} (n={cnt.get(k,0):2d}): mean 3p = {mp:+.2f} eV")

    # ---- FIGURES ----
    # Fig1: total DOS
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.plot(E0, total, "k", lw=1.5)
    ax.axvspan(0, gap, color="0.92"); ax.axvline(0, color="b", ls="--", lw=1); ax.axvline(gap, color="b", ls="--", lw=1)
    ax.set_xlim(-8, 8); ax.set_xlabel("E − E$_{VBM}$ (eV)"); ax.set_ylabel("DOS (states/eV)")
    ax.set_title(f"b2o3 DOS (gap {gap:.2f} eV, N(E_F)=0)")
    fig.tight_layout(); fig.savefig(f"{d}/{p}_dos_slide.png", dpi=180)

    # Fig2: element PDOS
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    colmap = {"S": "#d69e2e", "P": "#dd6b20", "Cl": "#38a169", "Li": "#888", "B": "#c53030", "O": "#3182ce"}
    ax.plot(E0, total, color="0.6", lw=1, label="total")
    for e in elems:
        ax.plot(Eref, el_sum[e], color=colmap[e], lw=1.6, label=e)
    ax.axvspan(0, gap, color="0.93"); ax.axvline(0, color="k", lw=1)
    ax.set_xlim(-8, 8); ax.set_xlabel("E − E$_{VBM}$ (eV)"); ax.set_ylabel("PDOS (states/eV)")
    ax.legend(ncol=2, fontsize=8); ax.set_title("b2o3 element PDOS (VBM = S 3p)")
    fig.tight_layout(); fig.savefig(f"{d}/{p}_pdos_element_slide.png", dpi=180)

    # Fig3: site-projected per-atom (free-S / B-S / PS4-S / Cl / O)
    fig, ax = plt.subplots(figsize=(8, 5))
    sc = {"free-S": "#d62728", "B-S": "#9467bd", "PS4-S": "#1f77b4", "Cl": "#2ca02c", "O": "#3182ce"}
    ls = {"free-S": "-", "B-S": "-", "PS4-S": "-", "Cl": "--", "O": ":"}
    ax.fill_between(Eref, site_pa["free-S"], color="#d62728", alpha=0.6, label=f"free S²⁻/atom (×{cnt.get('free-S',0)})")
    for k in ["B-S", "PS4-S", "Cl", "O"]:
        ax.plot(Eref, site_pa[k], color=sc[k], ls=ls[k], lw=1.8, label=f"{k}/atom (×{cnt.get(k,0)})")
    for k in sites:
        if not math.isnan(mean3p[k]):
            ax.axvline(mean3p[k], color=sc[k], lw=1.0, ls=":")
    ax.axvspan(0, gap, color="0.93"); ax.axvline(0, color="k", lw=1.2)
    ax.set_xlim(-7, 4); ax.set_xlabel("E − E$_{VBM}$ (eV)"); ax.set_ylabel("per-atom PDOS (states/eV)")
    ax.legend(fontsize=8.5, loc="upper left")
    ax.set_title("b2o3 site-projected 3p: free-S²⁻ shallowest → oxidation-prone\n"
                 f"mean 3p: free-S {mean3p['free-S']:+.2f}, B-S {mean3p['B-S']:+.2f}, "
                 f"PS₄-S {mean3p['PS4-S']:+.2f}, Cl {mean3p['Cl']:+.2f} eV")
    fig.tight_layout(); fig.savefig(f"{d}/{p}_pdos_site_slide.png", dpi=180)

    # ---- compact CSV export (downsampled) for off-cluster figure rebuild ----
    sel = (E0 >= -8) & (E0 <= 8)
    idx = np.where(sel)[0][::4]
    with open(f"{d}/{p}_dos_pdos_slides.csv", "w") as f:
        cols = ["E_minus_VBM", "total"] + elems + ["site_free-S", "site_B-S", "site_PS4-S", "site_Cl", "site_O"]
        f.write(",".join(cols) + "\n")
        for i in idx:
            row = [E0[i], total[i]] + [el_sum[e][i] for e in elems] + [site_pa[k][i] for k in sites]
            f.write(",".join(f"{x:.4f}" for x in row) + "\n")
    print(f"\n-> figures: {p}_dos_slide.png / {p}_pdos_element_slide.png / {p}_pdos_site_slide.png")
    print(f"-> compact csv (paste this): {d}/{p}_dos_pdos_slides.csv")
    json.dump({"gap": gap, "VBM": args.vbm, "CBM": args.cbm,
               "VBM_edge_pct": {e: round(100*wsum[e]/tt, 1) for e in elems},
               "mean_3p_per_site": {k: round(mean3p[k], 3) for k in sites},
               "site_counts": dict(cnt)},
              open(f"{d}/{p}_dos_pdos_values.json", "w"), indent=2)


if __name__ == "__main__":
    main()

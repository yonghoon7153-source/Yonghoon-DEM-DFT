#!/usr/bin/env python3
"""MSD / Arrhenius -> Origin-ready CSVs for a multi-T AIMD run (comp1 / modelc).

Reproduces the 3-panel figure as CSVs (no matplotlib needed for the data):
  (a) Li MSD vs t for each T          -> <label>_LiMSD_vs_t.csv
  (b) Arrhenius log10(D) vs 1000/T    -> <label>_arrhenius.csv (+ _fitline.csv)
  (c) per-element MSD at the top T     -> <label>_MSD_byelem_<T>K.csv

D from MSD = 6 D t (default window 2-50 ps, auto-shrinks for short runs).
Arrhenius: ln D = ln D0 - Ea/(kB T). numpy-only; reads aimd_mlip T*/traj.xyz.

Usage:
  python3 msd_origin.py --out_root <dir with T600/T800/T1000> --label modelc \
      --temperatures 600 800 1000 --out_dir msd_origin/modelc --fit_window 2 50
  (--save_fs auto-read from each T*/aimd_results.json; override with --save_fs)
"""
import argparse, json, re
from pathlib import Path
import numpy as np

KB = 8.617333262e-5  # eV/K
A2ps_to_cm2s = 1e-4  # 1 Å²/ps = 1e-4 cm²/s


def read_traj(path):
    txt = open(path).read().splitlines()
    pos, cells, sym, i, L = [], [], None, 0, len(txt)
    while i < L:
        if not txt[i].strip():
            i += 1; continue
        n = int(txt[i].split()[0])
        m = re.search(r'Lattice="([^"]+)"', txt[i + 1])
        cell = np.array([float(x) for x in m.group(1).split()]).reshape(3, 3)
        s, p = [], []
        for ln in txt[i + 2:i + 2 + n]:
            t = ln.split()
            s.append(t[0]); p.append([float(t[1]), float(t[2]), float(t[3])])
        if sym is None:
            sym = np.array(s)
        pos.append(p); cells.append(cell); i += 2 + n
    return sym, np.array(pos, float), np.array(cells, float)


def msd_per_element(sym, pos, cell, save_fs):
    cinv = np.linalg.inv(cell)
    frac = pos @ cinv
    df = np.diff(frac, axis=0); df -= np.round(df)
    fuw = np.empty_like(frac); fuw[0] = frac[0]; fuw[1:] = frac[0] + np.cumsum(df, axis=0)
    cart = fuw @ cell
    T = len(pos); t = np.arange(T) * save_fs / 1000.0
    out = {}
    for e in sorted(set(sym)):
        idx = np.where(sym == e)[0]
        d2 = ((cart[:, idx] - cart[0, idx]) ** 2).sum(-1)   # (T, nE)
        out[e] = d2.mean(1)
    return t, out


def fit_D(t, msd_Li, win):
    lo, hi = win
    m = (t >= lo) & (t <= hi)
    if m.sum() < 3:
        m = (t > 0.2 * t[-1]) & (t < 0.9 * t[-1])
    if m.sum() < 3:
        return None
    slope = np.polyfit(t[m], msd_Li[m], 1)[0]   # Å²/ps
    return slope / 6.0 * A2ps_to_cm2s           # cm²/s


def save_csv(path, header, cols):
    n = max(len(c) for c in cols)
    rows = []
    for i in range(n):
        rows.append(",".join("" if i >= len(c) else f"{c[i]:.6g}" for c in cols))
    Path(path).write_text(header + "\n" + "\n".join(rows) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_root", required=True, help="dir containing T600/, T800/, ...")
    ap.add_argument("--label", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--temperatures", type=float, nargs="+", default=[600, 800, 1000])
    ap.add_argument("--save_fs", type=float, default=None)
    ap.add_argument("--fit_window", type=float, nargs=2, default=[2.0, 50.0])
    args = ap.parse_args()

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    root = Path(args.out_root)

    li_curves, byelem_top, Ds, Ts = {}, None, [], []
    for T in args.temperatures:
        tdir = root / f"T{int(T)}"
        traj = tdir / "traj.xyz"
        if not traj.exists():
            print(f"  [skip] {traj} missing"); continue
        sfs = args.save_fs
        if sfs is None:
            aj = tdir / "aimd_results.json"
            if aj.exists():
                try: sfs = float(json.load(open(aj)).get("save_fs"))
                except Exception: pass
        if sfs is None:
            sfs = 100.0; print(f"  [warn] save_fs unknown for {T} K -> assume 100 fs")
        sym, pos, cells = read_traj(traj)
        t, msd = msd_per_element(sym, pos, cells[0], sfs)
        D = fit_D(t, msd["Li"], args.fit_window)
        print(f"  T={int(T)}K  frames={len(pos)} dt={sfs/1000:.3f}ps  "
              f"D_Li={D:.3e} cm2/s" if D else f"  T={int(T)}K  D fit failed")
        li_curves[int(T)] = (t, msd["Li"])
        if D: Ds.append(D); Ts.append(T)
        if int(T) == int(max(args.temperatures)):
            byelem_top = (int(T), t, msd)

    # (a) Li MSD vs t (aligned to shortest)
    if li_curves:
        Tk = sorted(li_curves)
        nmin = min(len(li_curves[k][0]) for k in Tk)
        cols = [li_curves[Tk[0]][0][:nmin]] + [li_curves[k][1][:nmin] for k in Tk]
        save_csv(out / f"{args.label}_LiMSD_vs_t.csv",
                 "t_ps," + ",".join(f"MSD_{k}K_A2" for k in Tk), cols)

    # (c) per-element MSD at top T
    if byelem_top:
        Ttop, t, msd = byelem_top
        order = [e for e in ["Li", "Cl", "P", "S", "O", "Br", "I", "N"] if e in msd]
        order += [e for e in msd if e not in order]
        save_csv(out / f"{args.label}_MSD_byelem_{Ttop}K.csv",
                 "t_ps," + ",".join(order), [t] + [msd[e] for e in order])

    # (b) Arrhenius
    arr = {}
    if len(Ds) >= 2:
        Ts_a, Ds_a = np.array(Ts), np.array(Ds)
        invT = 1.0 / Ts_a
        slope, intc = np.polyfit(invT, np.log(Ds_a), 1)
        Ea = -slope * KB; D0 = float(np.exp(intc))
        D300 = D0 * np.exp(-Ea / (KB * 300.0))
        arr = {"Ea_eV": round(Ea, 4), "D0_cm2_s": D0, "D300_cm2_s": D300}
        save_csv(out / f"{args.label}_arrhenius.csv",
                 f"# Ea={Ea:.4f} eV  D0={D0:.3e}  D300={D300:.3e} cm2/s\n"
                 "1000_over_T,log10_D,T_K,D_cm2_s",
                 [1000.0 / Ts_a, np.log10(Ds_a), Ts_a, Ds_a])
        xf = np.linspace(0.9, 3.5, 60)             # 1000/T grid incl. 300 K (=3.33)
        log10D_fit = (intc + slope * (xf / 1000.0)) / np.log(10)
        save_csv(out / f"{args.label}_arrhenius_fitline.csv",
                 "1000_over_T,log10_D_fit", [xf, log10D_fit])

    summary = {"label": args.label, "D_per_T": dict(zip([int(x) for x in Ts], Ds)), **arr}
    (out / f"{args.label}_msd_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n" + json.dumps(summary, indent=2))
    print(f"-> {out}/  (LiMSD_vs_t = panel a, arrhenius = panel b, MSD_byelem = panel c)")


if __name__ == "__main__":
    main()

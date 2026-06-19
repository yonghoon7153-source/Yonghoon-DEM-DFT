#!/usr/bin/env python3
"""AIMD Li+ jump statistics — clean intra/inter-cage distance picture (Fig-2d style).

Static-structure Li-Li distances are noisy (ordered approximant, all sites filled).
This instead samples the REAL mobile-Li distribution from an AIMD trajectory and
gives the quantities argyrodite papers actually plot:

  1. Van Hove self-correlation  Gs(r, dt)  -> P(a Li moved r in time dt).
       short dt = vibration peak (~0.5 A); longer dt grows secondary peaks at the
       characteristic JUMP distances (doublet / intra-cage / inter-cage).
  2. Cage-resolved hops: free anions (S-not-bonded-to-P + Cl) = ~immobile cage
       centres; a Li changing its nearest centre (persisting >= --hop_persist
       frames) = an INTER-cage hop. -> inter-cage hop RATE + hop-distance hist.
  3. MSD -> D (sanity / quantitative anchor).

numpy-only; reads multi-frame extended-xyz (traj.xyz from aimd_mlip.py). Run on the
server where the trajectories live (one trajectory per call; overlay systems in Origin).

Usage:
  python3 aimd_jump_stats.py --traj aimd/T600/traj.xyz --label comp1_T600 \
      --save_fs 20 --out_dir aimd_jump/comp1_T600 \
      --lags_ps 0.5 2 10 --hop_persist 5
  (save_fs auto-read from sibling aimd_results.json if present)
"""
import argparse, json, re, sys
from pathlib import Path
import numpy as np

PS_BOND = 2.30


def read_traj(path):
    txt = open(path).read().splitlines()
    pos, cells, sym = [], [], None
    i, L = 0, len(txt)
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
        pos.append(p); cells.append(cell)
        i += 2 + n
    return sym, np.array(pos, float), np.array(cells, float)


def mic(pi, pj, cell):
    cinv = np.linalg.inv(cell)
    d = (pi @ cinv)[:, None, :] - (pj @ cinv)[None, :, :]
    d -= np.round(d)
    return np.linalg.norm(d @ cell, axis=2)


def unwrap(pos, cell):
    cinv = np.linalg.inv(cell)
    frac = pos @ cinv
    df = np.diff(frac, axis=0); df -= np.round(df)
    fuw = np.empty_like(frac)
    fuw[0] = frac[0]; fuw[1:] = frac[0] + np.cumsum(df, axis=0)
    return fuw @ cell


def free_anions(sym, pos0, cell):
    idx = {e: np.where(sym == e)[0] for e in set(sym)}
    P, S, Cl = (idx.get(e, np.array([], int)) for e in ("P", "S", "Cl"))
    bonded = set()
    if len(P) and len(S):
        d = mic(pos0[P], pos0[S], cell)
        for i in range(len(P)):
            for j in np.where(d[i] < PS_BOND)[0]:
                bonded.add(int(S[j]))
    freeS = np.array([s for s in S if s not in bonded], int)
    return np.concatenate([freeS, Cl]) if (len(freeS) or len(Cl)) else np.array([], int), \
        np.array(["S"] * len(freeS) + ["Cl"] * len(Cl))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--traj", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--save_fs", type=float, default=None,
                    help="fs between saved frames (auto from aimd_results.json if omitted)")
    ap.add_argument("--lags_ps", type=float, nargs="+", default=[0.5, 2.0, 10.0])
    ap.add_argument("--jump_lag_ps", type=float, default=2.0)
    ap.add_argument("--hop_smooth_ps", type=float, default=2.0,
                    help="rolling-mode window (ps) that removes boundary-vibration flicker "
                         "from the per-frame cage label before counting hops")
    ap.add_argument("--hop_min_dist", type=float, default=2.5,
                    help="min unwrapped displacement (A) across a cage transition to count it "
                         "as a real inter-cage hop (excludes ~1 A rattle)")
    ap.add_argument("--rmax", type=float, default=8.0)
    ap.add_argument("--nbins", type=int, default=160)
    args = ap.parse_args()

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    save_fs = args.save_fs
    if save_fs is None:
        sib = Path(args.traj).parent / "aimd_results.json"
        if sib.exists():
            try:
                save_fs = float(json.load(open(sib)).get("save_fs"))
            except Exception:
                pass
    if save_fs is None:
        sys.exit("ERROR: --save_fs required (could not auto-read aimd_results.json)")
    dt_ps = save_fs / 1000.0

    sym, pos, cells = read_traj(args.traj)
    T = len(pos)
    cell0 = cells[0]
    Li = np.where(sym == "Li")[0]
    cen, ctype = free_anions(sym, pos[0], cell0)
    print(f"[{args.label}] frames={T}  dt={dt_ps:.4f} ps  total={T*dt_ps:.1f} ps  "
          f"Li={len(Li)}  cages={len(cen)} ({int((ctype=='S').sum())}S+{int((ctype=='Cl').sum())}Cl)")

    # unwrapped Li (for displacements/MSD/van Hove)
    cart_uw = unwrap(pos, cell0)
    Li_uw = cart_uw[:, Li, :]

    # ---- MSD -> D ----
    msd = ((Li_uw - Li_uw[0]) ** 2).sum(-1).mean(-1)        # (T,)
    t = np.arange(T) * dt_ps
    w = (t > 0.2 * t[-1]) & (t < 0.9 * t[-1])
    D = None
    if w.sum() > 5:
        slope = np.polyfit(t[w], msd[w], 1)[0]              # A^2/ps
        D = slope / 6.0 * 1e-16 / 1e-12                     # cm^2/s
    np.savetxt(out / f"{args.label}_msd.csv",
               np.c_[t, msd], delimiter=",", header="t_ps,MSD_A2", comments="")

    # ---- Van Hove self Gs(r, dt) ----
    edges = np.linspace(0, args.rmax, args.nbins + 1)
    rc = 0.5 * (edges[:-1] + edges[1:])
    vh_cols = [rc]; vh_hdr = ["r_A"]
    for lag_ps in args.lags_ps:
        lag = max(1, int(round(lag_ps / dt_ps)))
        if lag >= T:
            continue
        d = np.linalg.norm(Li_uw[lag:] - Li_uw[:-lag], axis=2).ravel()
        h, _ = np.histogram(d, bins=edges, density=True)
        vh_cols.append(h); vh_hdr.append(f"Gs_dt{lag_ps:g}ps")
    np.savetxt(out / f"{args.label}_vanhove.csv", np.c_[vh_cols].T,
               delimiter=",", header=",".join(vh_hdr), comments="")

    # ---- cage-resolved hops (inter-cage), flicker-robust ----
    # naive "nearest-centre changed" counts boundary vibration as hops. Instead:
    #   (1) smooth each Li's per-frame cage label by a rolling MODE (kills flicker)
    #   (2) count transitions in the smoothed label ONLY if the Li's unwrapped
    #       displacement across the transition window exceeds --hop_min_dist (a
    #       real cage-to-cage move, not a ~1 A rattle).
    cart = pos[:, :, :]
    assign = np.empty((T, len(Li)), int)
    for ti in range(T):
        assign[ti] = np.argmin(mic(cart[ti, Li], cart[ti, cen], cells[ti]), axis=1)

    sw = max(3, int(round(args.hop_smooth_ps / dt_ps)))      # rolling-mode window
    h = sw // 2

    def rolling_mode(a):
        o = np.empty(len(a), int)
        for t in range(len(a)):
            seg = a[max(0, t - h):min(len(a), t + h + 1)]
            o[t] = np.bincount(seg).argmax()
        return o

    inter_hops, flick = 0, 0
    hop_dists = []
    for k in range(len(Li)):
        a = assign[:, k]
        flick += int((np.diff(a) != 0).sum())
        sm = rolling_mode(a)
        for ti in np.where(np.diff(sm) != 0)[0]:
            lo, hi = max(0, ti - h), min(T - 1, ti + h)
            d = np.linalg.norm(Li_uw[hi, k] - Li_uw[lo, k])
            if d >= args.hop_min_dist:
                inter_hops += 1
                hop_dists.append(d)
    intra_changes = flick
    total_ps = T * dt_ps
    rate = inter_hops / len(Li) / (total_ps / 1000.0)       # hops / Li / ns
    hop_dists = np.array(hop_dists)
    if len(hop_dists):
        hh, _ = np.histogram(hop_dists, bins=edges, density=True)
        np.savetxt(out / f"{args.label}_intercage_hopdist.csv", np.c_[rc, hh],
                   delimiter=",", header="r_A,P_intercage_hop", comments="")

    summary = {
        "label": args.label, "frames": T, "dt_ps": dt_ps, "total_ps": total_ps,
        "n_Li": len(Li), "n_cages": int(len(cen)),
        "cage_Cl_fraction": round(float((ctype == "Cl").mean()), 3) if len(ctype) else None,
        "D_cm2_s": D,
        "inter_cage_hops": inter_hops,
        "inter_cage_hop_rate_per_Li_per_ns": round(rate, 4),
        "inter_cage_hop_dist_mean_A": round(float(hop_dists.mean()), 3) if len(hop_dists) else None,
        "transient_cage_flickers": flick,
        "hop_smooth_frames": sw,
        "hop_min_dist_A": args.hop_min_dist,
        "files": [f"{args.label}_{s}.csv" for s in ("vanhove", "msd", "intercage_hopdist")],
    }
    (out / f"{args.label}_jumpstats.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print(f"\n-> {out}/  (vanhove.csv = Fig-2d-style distance distribution; "
          f"inter-cage hop rate = long-range/σ proxy)")


if __name__ == "__main__":
    main()

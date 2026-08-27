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


def van_hove(uw, dt_ps, lags_ps, rmax=8.0, nbins=160):
    """자기 van Hove — P(|Δr| = r, 시간간격 dt). uw = **unwrap 된** (T, N, 3).

    읽는 법: 짧은 dt 는 진동 봉우리 하나(~0.5 Å)뿐이다. dt 를 늘렸을 때
      **자리 간격(~3 Å)에 두 번째 봉우리가 자라면 진짜 홉**, 첫 봉우리만 넓어지면
      cage 안에서 흔들리는 것이다.

    ★ 왜 MSD 와 다른가: 이건 **창을 안 고른다.** MSD 기울기는 어느 구간을 잡느냐에
      달렸지만(β·D_inc 논쟁 전부), 여기서는 분포 모양이 직접 답한다.

    ⛔ 못 하는 것
      · 절대 D 를 안 준다 — "확산 중인가" 만 본다.
      · 반드시 **unwrap 된 좌표**를 넣어야 한다. wrap 된 걸 넣으면 경계를 넘은 원자가
        셀 크기만 한 변위로 잡혀 없는 봉우리가 생긴다.
      · 시간원점을 전부 쓰므로 이웃 원점끼리 상관돼 있다 — 오차막대의 근거가 아니다.
    """
    edges = np.linspace(0, rmax, nbins + 1)
    rc = 0.5 * (edges[:-1] + edges[1:])
    T = len(uw)
    cols, hdr, skipped = [], [], []
    for lag_ps in lags_ps:
        lag = max(1, int(round(lag_ps / dt_ps)))
        if lag >= T:
            skipped.append(lag_ps)
            continue
        d = np.linalg.norm(uw[lag:] - uw[:-lag], axis=2).ravel()
        h, _ = np.histogram(d, bins=edges, density=True)
        cols.append(h); hdr.append(f"Gs_dt{lag_ps:g}ps")
    return rc, cols, hdr, skipped


def second_peak(rc, g, rmin=2.0):
    """`rmin` 밖에서 가장 큰 국소 봉우리 → (r, 높이). 없으면 (None, 0).

    "홉이 보이는가" 를 사람 눈 대신 숫자로 읽는다. 국소 최대만 센다 —
    단조 꼬리는 봉우리가 아니다.
    """
    m = rc > rmin
    if m.sum() < 3:
        return None, 0.0
    idx = np.where(m)[0]
    best, br = 0.0, None
    for i in idx[1:-1]:
        if g[i] >= g[i - 1] and g[i] >= g[i + 1] and g[i] > best:
            best, br = float(g[i]), float(rc[i])
    return br, best


def _selftest():
    """합성 궤적으로 판별력을 확인한다 — **음성 경로가 핵심**이다.

    양성(홉)만 보면 "무엇을 넣어도 봉우리가 보인다" 는 도구여도 통과한다.
    """
    ok = True

    def chk(c, m):
        nonlocal ok
        ok = ok and bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    rng = np.random.default_rng(0)
    T, N, dt = 2000, 60, 0.1                      # 200 ps · 100 fs 저장
    site = rng.normal(0, 20, (N, 3))

    def rattle(amp=0.35):
        return site[None, :, :] + rng.normal(0, amp, (T, N, 3))

    # ① cage 안 흔들림만 — 긴 lag 에서도 두 번째 봉우리가 **생기면 안 된다**
    uw = rattle()
    rc, cols, hdr, _sk = van_hove(uw, dt, [0.5, 20.0, 100.0])
    r2, h2 = second_peak(rc, cols[-1])
    chk(h2 < 0.02, f"[vanHove·음성] 흔들림만이면 3 Å 대 봉우리가 없다 (h={h2:.4f})")
    r1 = rc[int(np.argmax(cols[0]))]
    chk(0.2 < r1 < 1.2, f"[vanHove] 짧은 lag 은 진동 봉우리 하나 (r={r1:.2f} Å)")

    # ② 같은 흔들림 + 3.0 Å 홉 — 긴 lag 에서 두 번째 봉우리가 **자라야 한다**
    uw2 = rattle()
    for i in range(N):                            # 원자마다 한 번씩 3 Å 점프
        t0 = int(rng.integers(T // 4, 3 * T // 4))
        uw2[t0:, i, 0] += 3.0
    rc, cols2, hdr2, _sk = van_hove(uw2, dt, [0.5, 20.0, 100.0])
    r2b, h2b = second_peak(rc, cols2[-1])
    chk(r2b is not None and 2.4 < r2b < 3.6,
        f"[vanHove·양성] 홉이 있으면 자리 간격에 봉우리가 선다 (r={r2b} Å)")
    chk(h2b > 5 * max(h2, 1e-6),
        f"[vanHove·판별력] 홉 쪽 봉우리가 흔들림 쪽보다 훨씬 크다 ({h2b:.4f} vs {h2:.4f})")

    # ③ 짧은 lag 에서는 홉이 있어도 아직 안 보인다 (시간 의존성이 옳은가)
    r2c, h2c = second_peak(rc, cols2[0])
    chk(h2c < h2b / 5, f"[vanHove] 짧은 lag 에서는 그 봉우리가 아직 없다 ({h2c:.4f})")

    # ④ 가드: 궤적보다 긴 lag 은 조용히 버리지 않고 **보고**한다
    _rc, _c, _h, sk = van_hove(uw, dt, [1.0, 9999.0])
    chk(sk == [9999.0], f"[vanHove·가드] 궤적보다 긴 lag 을 보고한다 ({sk})")

    # ⑤ 가드: **wrap 된 좌표**를 넣으면 셀 크기의 가짜 변위가 생긴다 —
    #    unwrap 이 실제로 그걸 없애는지 확인한다 (오늘 min-image 에서 데인 유형)
    L = 12.0
    cell = np.eye(3) * L
    drift = np.zeros((T, N, 3))
    drift[:, :, 0] = np.linspace(0, 3 * L, T)[:, None]      # 셀을 3번 가로지른다
    wrapped = (site[None] + drift) % L
    uwr = unwrap(wrapped, cell)
    step = np.abs(np.diff(uwr, axis=0)).max()
    chk(step < L / 2, f"[vanHove·가드] unwrap 뒤 한 스텝 이동이 셀 절반 미만 ({step:.2f} < {L/2})")
    _rc, cw, _h, _s = van_hove(wrapped, dt, [50.0])
    _r, hw = second_peak(_rc, cw[0])
    chk(hw > 0.01, "[vanHove·음성] wrap 된 좌표를 그대로 넣으면 **가짜 봉우리**가 생긴다 "
                   "— 그래서 unwrap 이 필수다")
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
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
    rc, cols, hdr, skipped = van_hove(Li_uw, dt_ps, args.lags_ps, args.rmax, args.nbins)
    if skipped:
        print(f"  ! lag {skipped} ps 는 궤적({T*dt_ps:.1f} ps)보다 길어 건너뛴다")
    np.savetxt(out / f"{args.label}_vanhove.csv", np.c_[[rc] + cols].T,
               delimiter=",", header=",".join(["r_A"] + hdr), comments="")
    # ★ 25개를 쓸어 담을 때 CSV 25장을 눈으로 볼 수는 없다 — **판정을 한 줄로** 찍는다.
    #   보는 것: 긴 lag 에서 자리 간격(≳2 Å)에 두 번째 봉우리가 자랐는가.
    vh_verdict = []
    for lp, g in zip([x for x in args.lags_ps if x not in skipped], cols):
        r2, h2 = second_peak(rc, g)
        r1 = float(rc[int(np.argmax(g))])
        vh_verdict.append({"lag_ps": lp, "first_peak_A": round(r1, 2),
                           "second_peak_A": None if r2 is None else round(r2, 2),
                           "second_peak_h": round(h2, 5)})
    if vh_verdict:
        a, b = vh_verdict[0], vh_verdict[-1]
        grew = b["second_peak_h"] > 5 * max(a["second_peak_h"], 1e-6) and b["second_peak_A"]
        print(f"  vanHove: dt {a['lag_ps']:g}→{b['lag_ps']:g} ps · 1st {a['first_peak_A']}→"
              f"{b['first_peak_A']} Å · 2nd {a['second_peak_A']}→{b['second_peak_A']} Å "
              f"(h {a['second_peak_h']:.4f}→{b['second_peak_h']:.4f})")
        print("  ⇒ " + ("**홉이 보인다** — 자리 간격에 두 번째 봉우리가 자란다"
                        if grew else
                        "⚠ **두 번째 봉우리가 안 자란다** — 이 창에서는 cage 안 흔들림이 지배적이다"))

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
        "van_hove": vh_verdict,
        "files": [f"{args.label}_{s}.csv" for s in ("vanhove", "msd", "intercage_hopdist")],
    }
    (out / f"{args.label}_jumpstats.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print(f"\n-> {out}/  (vanhove.csv = Fig-2d-style distance distribution; "
          f"inter-cage hop rate = long-range/σ proxy)")


if __name__ == "__main__":
    main()

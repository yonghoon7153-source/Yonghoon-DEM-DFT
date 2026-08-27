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


def van_hove(uw, dt_ps, lags_ps, rmax=None, nbins=160):
    """자기 van Hove의 **radial displacement density** P_s(r,t) = 4πr²·G_s(r,t).

    ⛔ 2026-08-28 (리뷰 L · P0-4) — 열 이름을 `Gs_*` 로 썼는데 이건 G_s 가 아니다.
      |Δr| 의 히스토그램이라 **r² 야코비안이 이미 들어간** radial density 다. `Ps_*` 로 고쳤다.

    uw = **unwrap 된** (T, N, 3).

    읽는 법: 짧은 dt 는 진동 봉우리 하나(~0.5 Å)뿐이다. dt 를 늘렸을 때
      **자리 간격(~3 Å)에 두 번째 봉우리가 자라면 진짜 홉**, 첫 봉우리만 넓어지면
      cage 안에서 흔들리는 것이다.

    ★ 왜 MSD 와 다른가: 이건 **창을 안 고른다.** MSD 기울기는 어느 구간을 잡느냐에
      달렸지만(β·D_inc 논쟁 전부), 여기서는 분포 모양이 직접 답한다.

    ⛔⛔ 2026-08-28 실측 수정 — **판정 기준이 틀렸었다.**
      첫 판은 *"자리 간격에 두 번째 봉우리가 자라는가"* 로 봤다. 그건 합성 궤적(모든
      원자가 정확히 한 번, 정확히 3 Å 점프)에서는 보이지만 **진짜 확산에서는 안 보인다** —
      긴 lag 에서 분포는 이산 봉우리가 아니라 **넓은 분포로 퍼지고 봉우리가 밖으로 이동**한다.
      실측 대조(합성):
          cage      1st peak 0.68 → 0.62 → 0.68 → 0.73 Å  (안 움직인다)
          diffusive 1st peak 0.68 → 0.93 → 1.58 → 3.03 Å  (밖으로 이동한다)
      ⇒ **주 지표는 봉우리 위치의 이동**이다. 두 번째 봉우리는 부차 정보로만 남긴다.
      내 selftest 가 이걸 못 잡은 이유: 합성 fixture 가 *한 번씩 딱 3 Å 점프* 라
      실제 확산이 아니라 **이산 홉만** 시험하고 있었다. 진짜 데이터가 잡아줬다.

    ⛔⛔ rmax 를 8 Å 로 고정했던 것도 틀렸다 — 빠른 계는 50 ps 에 RMS 가 그걸 넘어
      **분포가 잘린 채** 봉우리가 범위 밖으로 나간다. rmax=None 이면 자동으로 잡고,
      잘린 비율을 같이 보고한다.

    ⛔ 못 하는 것
      · 절대 D 를 안 준다 — "확산 중인가" 만 본다.
      · 반드시 **unwrap 된 좌표**를 넣어야 한다. wrap 된 걸 넣으면 경계를 넘은 원자가
        셀 크기만 한 변위로 잡혀 없는 봉우리가 생긴다.
      · 시간원점을 전부 쓰므로 이웃 원점끼리 상관돼 있다 — 오차막대의 근거가 아니다.
    """
    T = len(uw)
    use = [l for l in lags_ps if max(1, int(round(l / dt_ps))) < T]
    skipped = [l for l in lags_ps if l not in use]
    if rmax is None and use:
        lag = max(1, int(round(max(use) / dt_ps)))
        dmax = float(np.linalg.norm(uw[lag:] - uw[:-lag], axis=2).max())
        rmax = max(8.0, 1.15 * dmax)      # 잘리면 봉우리가 범위 밖으로 나간다
    rmax = rmax or 8.0
    edges = np.linspace(0, rmax, nbins + 1)
    rc = 0.5 * (edges[:-1] + edges[1:])
    cols, hdr, trunc = [], [], []
    for lag_ps in use:
        lag = max(1, int(round(lag_ps / dt_ps)))
        d = np.linalg.norm(uw[lag:] - uw[:-lag], axis=2).ravel()
        h, _ = np.histogram(d, bins=edges, density=True)
        cols.append(h); hdr.append(f"Ps_dt{lag_ps:g}ps")
        trunc.append(float((d > rmax).mean()))
    return rc, cols, hdr, skipped, {"rmax_A": round(rmax, 2), "trunc_frac": trunc}


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
    import os
    import shutil
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
    rc, cols, hdr, _sk, _i = van_hove(uw, dt, [0.5, 20.0, 100.0])
    r2, h2 = second_peak(rc, cols[-1])
    chk(h2 < 0.02, f"[vanHove·음성] 흔들림만이면 3 Å 대 봉우리가 없다 (h={h2:.4f})")
    r1 = rc[int(np.argmax(cols[0]))]
    chk(0.2 < r1 < 1.2, f"[vanHove] 짧은 lag 은 진동 봉우리 하나 (r={r1:.2f} Å)")

    # ★★ 2026-08-28 실측 수정 — 첫 판 fixture 는 *한 번씩 딱 3 Å 점프* 라
    #   **이산 홉만** 시험했다. 진짜 확산은 그런 봉우리를 안 만든다(분포가 퍼진다).
    #   그래서 실제 궤적에서 modelc T1000(확실히 확산하는 계)이 "cage 지배" 로 찍혔다.
    #   ⇒ **브라운 운동을 fixture 에 넣고, 판정은 봉우리 이동으로** 바꾼다.
    def peaks(uw_, lags=(0.5, 2.0, 10.0, 50.0)):
        rc_, cs, _h, _sk, info = van_hove(uw_, dt, list(lags))
        return [float(rc_[int(np.argmax(g))]) for g in cs], info

    pk_cage, _i = peaks(uw)
    chk(max(pk_cage) - min(pk_cage) < 0.3,
        f"[vanHove·음성] cage 는 봉우리가 **제자리**다 ({pk_cage[0]:.2f}→{pk_cage[-1]:.2f} Å)")

    step = rng.normal(0, 0.10, (T, N, 3))
    walk = site[None] + np.cumsum(step, axis=0) + rng.normal(0, 0.3, (T, N, 3))
    pk_diff, info_d = peaks(walk)
    chk(pk_diff[-1] - pk_diff[0] >= 0.5,
        f"[vanHove·양성·실측회귀] **확산은 봉우리가 밖으로 이동**한다 "
        f"({pk_diff[0]:.2f}→{pk_diff[-1]:.2f} Å) — 옛 판정(두 번째 봉우리)은 이걸 놓쳤다")
    chk(all(a <= b + 1e-9 for a, b in zip(pk_diff, pk_diff[1:])),
        "[vanHove] 확산이면 봉우리가 lag 과 함께 **단조로** 밀려난다")

    # ③ rmax 자동: 빠른 계가 잘리지 않아야 한다 (8 Å 고정이 실제로 잘랐다)
    fast = site[None] + np.cumsum(rng.normal(0, 0.5, (T, N, 3)), axis=0)
    _rc, _c, _h, _sk, inf = van_hove(fast, dt, [50.0])
    chk(inf["rmax_A"] > 8.0 and inf["trunc_frac"][0] < 0.02,
        f"[vanHove·실측회귀] 빠른 계는 rmax 를 키운다 ({inf['rmax_A']} Å · "
        f"잘림 {100*inf['trunc_frac'][0]:.2f} %)")
    _rc, _c, _h, _sk, inf8 = van_hove(fast, dt, [50.0], rmax=8.0)
    chk(inf8["trunc_frac"][0] > 0.02,
        f"[vanHove·음성] rmax 8 Å 로 고정하면 실제로 잘린다 "
        f"({100*inf8['trunc_frac'][0]:.1f} %) — 그래서 잘림 비율을 보고한다")

    # ④ 가드: 궤적보다 긴 lag 은 조용히 버리지 않고 **보고**한다
    _rc, _c, _h, sk, _i = van_hove(uw, dt, [1.0, 9999.0])
    chk(sk == [9999.0], f"[vanHove·가드] 궤적보다 긴 lag 을 보고한다 ({sk})")

    # ⑤ 가드: wrap 된 좌표는 unwrap 이 없으면 가짜 변위를 만든다
    L = 12.0
    cell = np.eye(3) * L
    drift = np.zeros((T, N, 3))
    drift[:, :, 0] = np.linspace(0, 3 * L, T)[:, None]
    wrapped = (site[None] + drift) % L
    uwr = unwrap(wrapped, cell)
    step_max = np.abs(np.diff(uwr, axis=0)).max()
    chk(step_max < L / 2, f"[vanHove·가드] unwrap 뒤 한 스텝이 셀 절반 미만 ({step_max:.2f})")
    pk_w, _i = peaks(wrapped, lags=(0.5, 50.0))
    chk(abs(pk_w[-1] - pk_w[0]) > 0.5,
        "[vanHove·음성] wrap 된 좌표를 그대로 넣으면 **가짜 이동**이 보인다 — unwrap 이 필수다")

    # ★★★ 배선 회귀 (2026-08-28) — 오늘 van Hove 버그 셋 중 **둘이 배선**이었다.
    #   함수 기본값을 None 으로 고쳐놓고 CLI 기본값 8.0 을 안 고쳐서, 실제 실행에서는
    #   적응형 rmax 가 한 번도 안 먹었다(33/33 궤적이 전부 잘림). selftest 는 함수를
    #   직접 불러서 **CLI 를 안 탔고** 그래서 통과했다.
    #   ⇒ 이제 파서 자체를 시험한다. 함수만 보는 테스트는 배선 버그를 못 잡는다.
    _ap = _build_parser()
    _d = {a.dest: a.default for a in _ap._actions}
    chk(_d.get("rmax") is None,
        f"[배선·실측회귀] `--rmax` **CLI 기본값이 None** 이어야 적응형이 산다 ({_d.get('rmax')})")
    chk(_d.get("save_fs") is None,
        "[배선] `--save_fs` 는 기본값을 두지 않는다 (추측하면 시간축이 통째로 틀린다)")
    _ns = _ap.parse_args(["--traj", "x", "--label", "y", "--out_dir", "z"])
    chk(_ns.rmax is None and _ns.lags_ps,
        "[배선] 기본 인자로 파싱했을 때도 rmax 가 None 이다")

    # ★★★ E2E (2026-08-28, 리뷰 L P0-1) — **실제 CLI 를 태운다.**
    #   `edges` NameError 는 홉이 잡힐 때만 나는데, 함수 단위 테스트는 main() 을 안 타서
    #   못 잡았다. 러너도 traceback 을 숨기고 성공으로 세어 33건이 "완료" 로 보고됐다.
    #   ⇒ 홉이 **실제로 잡히는** 합성 궤적을 만들어 CLI 를 돌리고 종료코드와 산출물을 본다.
    import subprocess
    import tempfile
    td = tempfile.mkdtemp(prefix="ajs_e2e_")
    # ⚠ **홉이 실제로 잡혀야 한다.** 첫 fixture 는 cage 중심이 하나뿐이라 홉이 0 이었고,
    #   그러면 `edges` 를 쓰는 줄이 아예 안 돌아 **회귀 테스트가 판별력이 없었다**
    #   (제거해도 통과했다 — 오늘 세 번째 '합성이 실제보다 쉽다').
    #   ⇒ cage 중심(자유 음이온) **둘**을 두고 Li 하나를 그 사이로 확실히 넘긴다.
    NF = 400
    cell = [[18., 0, 0], [0, 18., 0], [0, 0, 18.]]
    rows0 = [("P", [9., 9., 0.]),                       # PS4 (S 는 결합 → 자유 아님)
             ("S", [10.9, 9., 0.]), ("S", [7.1, 9., 0.]),
             ("S", [9., 10.9, 0.]), ("S", [9., 7.1, 0.]),
             ("Cl", [0., 0., 0.]), ("Cl", [6., 0., 0.]),  # ← cage 중심 2개
             ("Li", [0.6, 0., 0.]),                       # 이 Li 가 Cl1 → Cl2 로 넘어간다
             ("Li", [0., 3.0, 0.]), ("Li", [6., 3.0, 0.])]
    HOP_I = 7
    with open(os.path.join(td, "traj.xyz"), "w") as f:
        for t_ in range(NF):
            f.write(f"{len(rows0)}\nLattice=\"" +
                    " ".join(f"{v:.6f}" for r in cell for v in r) + "\"\n")
            for i, (sym, q) in enumerate(rows0):
                x = list(q)
                if i == HOP_I and t_ > NF // 2:
                    x[0] = 5.4            # 0.6 → 5.4 Å : 4.8 Å 이동 (문턱 2.5 초과)
                f.write(f"{sym} {x[0]:.6f} {x[1]:.6f} {x[2]:.6f}\n")
    json.dump({"save_fs": 100.0}, open(os.path.join(td, "aimd_results.json"), "w"))
    r = subprocess.run([sys.executable, os.path.abspath(__file__),
                        "--traj", os.path.join(td, "traj.xyz"), "--label", "e2e",
                        "--out_dir", os.path.join(td, "out"), "--lags_ps", "0.5", "5", "20"],
                       capture_output=True, text=True, timeout=180)
    chk(r.returncode == 0,
        f"[E2E·실측회귀] **실제 CLI 가 종료코드 0 으로 끝난다** "
        f"(rc={r.returncode}) — `edges` NameError 가 여기서 났다"
        + ("\n      " + (r.stderr or "").strip().splitlines()[-1] if r.returncode else ""))
    chk("NameError" not in (r.stderr or ""), "[E2E·실측회귀] traceback 이 없다")
    chk(os.path.isfile(os.path.join(td, "out", "e2e_vanhove.csv")),
        "[E2E] vanhove.csv 가 생긴다")
    hdr0 = open(os.path.join(td, "out", "e2e_vanhove.csv")).readline()
    chk("Ps_dt" in hdr0 and "Gs_dt" not in hdr0,
        f"[E2E·리뷰L] 열 이름이 **P_s**(=4πr²G_s) 다 — G_s 가 아니다 ({hdr0.split(',')[1].strip()})")
    js = os.path.join(td, "out", "e2e_summary.json")
    if os.path.isfile(js):
        d_ = json.load(open(js))
        chk("D_cm2_s" not in d_ and "D_single_origin_diagnostic_cm2_s" in d_,
            "[E2E·리뷰L] 비정본 D 를 일반 이름으로 저장하지 않는다")
    shutil.rmtree(td, ignore_errors=True)

    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def _build_parser():
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
    # ⛔ 2026-08-28 — 여기가 **8.0 으로 남아 있어서** 함수 쪽 적응형 rmax 가
    #   한 번도 안 먹었다. 실측 33/33 궤적이 전부 잘려서 못 읽는 상태로 나왔다.
    #   함수 기본값만 고치고 **배선을 안 고친 것**이다 — selftest 는 함수를 직접
    #   불러서 CLI 를 한 번도 안 탔고, 그래서 통과했다.
    ap.add_argument("--rmax", type=float, default=None,
                    help="기본 None = 가장 긴 lag 의 최대 변위에서 자동으로 잡는다. "
                         "고정하면 빠른 계에서 분포가 잘린다")
    ap.add_argument("--nbins", type=int, default=160)
    return ap


def main():
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    ap = _build_parser()
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
    rc, cols, hdr, skipped, vhinfo = van_hove(Li_uw, dt_ps, args.lags_ps,
                                             args.rmax, args.nbins)
    # ⛔ 2026-08-28 (리뷰 L · P0-1) — 아래 inter-cage 히스토그램이 `edges` 를 쓰는데
    #   그건 van_hove() 의 **지역변수**다. van_hove 를 함수로 뽑을 때 이 참조를 안 고쳤고,
    #   **홉이 하나라도 잡히면 NameError** 로 죽었다. 같은 격자를 여기서 다시 만든다.
    edges = np.linspace(0, vhinfo["rmax_A"], args.nbins + 1)
    if skipped:
        print(f"  ! lag {skipped} ps 는 궤적({T*dt_ps:.1f} ps)보다 길어 건너뛴다")
    np.savetxt(out / f"{args.label}_vanhove.csv", np.c_[[rc] + cols].T,
               delimiter=",", header=",".join(["r_A"] + hdr), comments="")
    # ★ 25개를 쓸어 담을 때 CSV 25장을 눈으로 볼 수는 없다 — **판정을 한 줄로** 찍는다.
    #   보는 것: 긴 lag 에서 자리 간격(≳2 Å)에 두 번째 봉우리가 자랐는가.
    vh_verdict = []
    for lp, g, tf in zip([x for x in args.lags_ps if x not in skipped], cols,
                         vhinfo["trunc_frac"]):
        r2, h2 = second_peak(rc, g)
        r1 = float(rc[int(np.argmax(g))])
        vh_verdict.append({"lag_ps": lp, "first_peak_A": round(r1, 2),
                           "second_peak_A": None if r2 is None else round(r2, 2),
                           "second_peak_h": round(h2, 5), "trunc_frac": round(tf, 4)})
    if vh_verdict:
        a, b = vh_verdict[0], vh_verdict[-1]
        shift = b["first_peak_A"] - a["first_peak_A"]
        print(f"  vanHove: dt {a['lag_ps']:g}→{b['lag_ps']:g} ps · **1st peak "
              f"{a['first_peak_A']} → {b['first_peak_A']} Å (Δ{shift:+.2f})** · "
              f"rmax {vhinfo['rmax_A']} Å · 잘림 {100*b['trunc_frac']:.1f} %")
        # ★ 주 지표는 **봉우리 이동**이다 (2026-08-28 실측 수정 — van_hove docstring 참조)
        if b["trunc_frac"] > 0.02:
            print(f"  ⇒ ⛔ 분포의 {100*b['trunc_frac']:.1f} % 가 rmax 밖이다 — **잘려서 못 읽는다.** "
                  f"--rmax 를 키울 것")
        elif shift >= 0.5:
            # ⚠ 판정 문구에 다른 판정의 어휘를 안 쓴다 (watch 분류기가 겹쳐 센 적 있다).
            # ⛔ 2026-08-28 (리뷰 L · P0-2) — 카드에는 "갇힘/고원/확산" 세 체제라고 써 놓고
            #   **코드는 shift ≥ 0.5 를 전부 '확산' 이라고 찍고 있었다.** 문서와 코드가 갈렸다.
            #   (그 전에 넣었다고 생각한 편집이 실제로는 안 붙었는데, selftest 가 판정 **문구**를
            #    안 보기 때문에 통과했다 — 오늘 세 번째 같은 유형이다.)
            SITE_LO, SITE_HI = 3.2, 4.8
            if SITE_LO <= b["first_peak_A"] <= SITE_HI:
                print(f"  ⇒ **움직인다 — 자리 간격 고원**이다 (봉우리 {b['first_peak_A']} Å, "
                      f"Δ{shift:+.2f}). 홉이 대략 한 번 수준이라 **이 구간에서는 D 에 둔감**하다 "
                      f"— 빠르기 비교에 쓰지 말 것")
            else:
                print(f"  ⇒ **확산한다** — 봉우리가 {shift:+.2f} Å 밖으로 이동했다 "
                      f"(고원 밖: {b['first_peak_A']} Å)")
        elif shift <= 0.2:
            print(f"  ⇒ ⚠ **봉우리가 제자리다** ({shift:+.2f} Å) — 이 창에서는 "
                  f"cage 안 흔들림이 지배적이다")
            if vhinfo["rmax_A"] > 12:
                print(f"     ⚠ 다만 rmax 가 {vhinfo['rmax_A']} Å 로 잡혔다 — "
                      f"**소수는 멀리 갔다.** 봉우리는 최빈값이라 그 꼬리를 안 센다")
        else:
            print(f"  ⇒ ⚠ 중간 ({shift:+.2f} Å) — 어느 쪽도 주장하지 않는다. "
                  f"더 긴 lag 이 필요하다")

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
        # ⛔ 2026-08-28 (리뷰 L · P0-4) — 이 D 는 **정본 창(2–50 ps)이 아니다.**
        #   single-origin 20–90 % 적합이다. 일반 이름으로 두면 정본 D 와 섞인다.
        "D_single_origin_diagnostic_cm2_s": D,
        "⛔_D_규약": ("정본은 MSD 창 2–50 ps · 자유절편이다(CLAUDE.md). 이 값은 "
                     "single-origin 20–90 % 적합이라 **정본 D 로 인용 금지** — 진단용이다."),
        "inter_cage_hops": inter_hops,
        "inter_cage_hop_rate_per_Li_per_ns": round(rate, 4),
        "inter_cage_hop_dist_mean_A": round(float(hop_dists.mean()), 3) if len(hop_dists) else None,
        "transient_cage_flickers": flick,
        "hop_smooth_frames": sw,
        "hop_min_dist_A": args.hop_min_dist,
        "van_hove": vh_verdict, "van_hove_info": vhinfo,
        "files": [f"{args.label}_{s}.csv" for s in ("vanhove", "msd", "intercage_hopdist")],
    }
    (out / f"{args.label}_jumpstats.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    print(f"\n-> {out}/  (vanhove.csv = Fig-2d-style distance distribution; "
          f"inter-cage hop rate = long-range/σ proxy)")


if __name__ == "__main__":
    main()

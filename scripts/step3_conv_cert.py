#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""STEP3 수렴 증서 (설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §6 · 등록 R 초안 §3-5 · N15 = 1저자 10-20
권고대로) — 다음 세대 판정 해의 게시 조건.

왜: 지금 생산 술어 (`step3_sigma.solve_sigma_z` — CG `info` 0 · 잔차 유한 · 잔차 ≤ 1e-6 · rtol 1e-8 고정) 는 다음 세대 꼴
(섬유 σ 7,853.98 ↔ σ_NCM 0.0041 = 대비 1.9 × 10⁶ · 아래 판에 매달린 섬유) 에서 **틀린 σ 를 수렴으로 인증**한다 (사전 리뷰 ② 탐침 ·
이 모듈의 `probe_table` 이 리포 시험으로 다시 만든다).  잔차의 상대 기준 ‖b‖ 이 섬유의 판 결합 g (2σ_f·h) 에 지배돼 NCM 영역이
덜 풀린 채 rtol 에 닿는다.

증서 셋 (σ 를 게시하려면 셋 다 · 하나라도 실패 = 미수렴 = 미게시):
  ⓐ 정지 규칙  CG rtol ≤ `CERT_RTOL_MAX` (봉인) · info 0 · 잔차 유한
  ⓑ 판 전류 불균형  |I_bot − I_top| / I_bot ≤ `CERT_EPS_I` (봉인) — 정확한 해에서는 KCL 로 0 (두 판 전류가 같다)
  ⓒ 조임 재풀이  앞 해를 초기값으로 max(rtol × `CERT_RESOLVE_FACTOR`, 1e-14) 까지 이어 풀어 |Δσ|/σ ≤ `CERT_RESOLVE_TOL`
                 (재풀이 자체도 info 0 · 바닥 1e-14 = 설계 권고값 — 봉인 체제 1e-12 에서는 걸리지 않는다)

봉인 (설계 §6 절차 3 · 결과 전 · 합성 직접해 대조 — 실침대 σ 를 보지 않는다):
  `probe_table()` = 24 × 24 × 72 · vox 0.15 · AM (σ 0.0041) 바탕에 아래 판에서 자라 위 판에 안 닿는 섬유 기둥 (σ 7,853.98 · 셀 10 %) ·
  시드 0 · 1 · 2 · 꼴 둘 (`plain` · 기둥 가운데 축방향 면 하나를 접합 간선 g = 1e4/R_j (R_j 1e6 Ω) 로 바꾼 `junction`) ·
  rtol {1e-8, 1e-10, 1e-12, 1e-14} × CPU Jacobi CG (생산 `_solve_cg`) ↔ 같은 행렬 직접해.
  `derive_seal(table)` = 정지 rtol = 모든 행에서 σ 오차 ≤ 1e-4 인 가장 느슨한 rtol · ε_I 구간 = [σ 오차 ≤ 1e-4 인 해의 불균형 최댓값,
  σ 오차 > 1e-4 인 해의 최솟값) · 1e-4 가 구간 안이면 1e-4 · 아니면 기하 중점 · 구간이 비면 ⓑ = 진단 칸 (증서 = ⓐ + ⓒ).
  ⇒ 아래 상수는 그 규칙의 결과다 — `scripts/test_step3_conv_cert.py` K8 이 다시 계산해 대조한다 (상수만 바꾸면 실패).
⚠ 합성 격자 · 실침대 아님 · 수치 인용 불가 ([탐침]).  실침대 반복 수 · 시간은 숫자 탐침 (값 봉인) 에서 따로 잰다.

  python3 scripts/step3_conv_cert.py --table      # 봉인 표 (CPU · 수 분)
"""
import argparse
import math
import os
import sys

import numpy as np

CERT_VERSION = 'conv-cert-v1'
#: ⓐ 정지 rtol 상한 — `derive_seal(probe_table())` 의 결과 (2026-10-20 · 봉인 · 바꾸려면 새 봉인 = 표를 다시 · R 개정)
CERT_RTOL_MAX = 1.0e-12
#: ⓑ 판 전류 불균형 문턱 — 같은 표의 기계 규칙 결과 (권고 출발 1e-4 가 구간 안)
CERT_EPS_I = 1.0e-4
#: ⓒ 이어 풀기 rtol = 정지 rtol × 이 값 (설계: 1/100) · 허용 |Δσ|/σ
CERT_RESOLVE_FACTOR = 1.0e-2
CERT_RESOLVE_TOL = 1.0e-4
#: ⓒ 이어 풀기 rtol 의 바닥 — 설계 권고값 1e-14 (= 봉인 정지 rtol 1e-12 × 1/100).  정지 rtol 을 그보다 조이면 1/100 은 1e-16 근처
#:   (float64 CG 가 늘 닿지 못하는 곳) 이 되어 maxiter 까지 돈다 → 바닥에서 멈춘다 (봉인 체제 1e-12 에서는 바닥이 걸리지 않는다).
CERT_RESOLVE_RTOL_FLOOR = 1.0e-14
#: 생산 술어의 잔차 상한 (비교용 — `step3_sigma.solve_sigma_z` 의 `resid > 1e-6`)
PROD_RESID_MAX = 1.0e-6

PROBE_SHAPE = (24, 24, 72)
PROBE_VOX = 0.15
PROBE_FRAC = 0.10
PROBE_SIGMA_FIBRE = 7853.98
PROBE_SIGMA_AM = 0.0041
PROBE_SEEDS = (0, 1, 2)
PROBE_RTOLS = (1e-8, 1e-10, 1e-12, 1e-14)
PROBE_RJ_OHM = 1.0e6
PROBE_MAXITER = 400000
SEAL_ERR_TOL = 1.0e-4
SEAL_EPS_START = 1.0e-4


def plate_currents(phi, Ab, gb, At, gt):
    """해 → (아래 판 전류 I_bot = Σ g_b (1 − φ) · 위 판 전류 I_top = Σ g_t φ) — 코드 단위 · ΔV = 1."""
    phi = np.asarray(phi, np.float64)
    Ib = float(np.sum(np.asarray(gb, np.float64) * (1.0 - phi[np.asarray(Ab)]))) if Ab is not None and len(Ab) else 0.0
    It = float(np.sum(np.asarray(gt, np.float64) * phi[np.asarray(At)])) if At is not None and len(At) else 0.0
    return Ib, It


def certify(L, b, phi, info, resid, rtol_used, Ab, gb, At, gt, scale, resolve):
    """증서 ⓐ ⓑ ⓒ → dict (모든 칸 · ok).  resolve(L, b, x0, rtol) → (φ, info) = 생산 솔버로 이어 풀기.
    scale = σ_eff / I_bot (L_gap / A) — ⓒ 는 상대 변화라 scale 과 무관하지만 기록용 σ 를 같이 남긴다."""
    Ib, It = plate_currents(phi, Ab, gb, At, gt)
    imb = abs(Ib - It) / abs(Ib) if (Ib != 0.0 and math.isfinite(Ib) and math.isfinite(It)) else math.inf
    try:
        rt = float(rtol_used)
    except (TypeError, ValueError):
        rt = math.nan
    a_ok = (type(info) is int or isinstance(info, (np.integer,))) and int(info) == 0 \
        and resid is not None and math.isfinite(float(resid)) and math.isfinite(rt) and rt <= CERT_RTOL_MAX
    b_ok = bool(math.isfinite(imb) and imb <= CERT_EPS_I)
    rr = max(rt * CERT_RESOLVE_FACTOR, CERT_RESOLVE_RTOL_FLOOR) if math.isfinite(rt) else math.nan
    s1 = Ib * float(scale)
    try:
        phi2, info2 = resolve(L, b, np.asarray(phi, np.float64), rr)
        Ib2, It2 = plate_currents(phi2, Ab, gb, At, gt)
        s2 = Ib2 * float(scale)
        d = abs(s2 - s1) / abs(s1) if (s1 != 0.0 and math.isfinite(s1) and math.isfinite(s2)) else math.inf
        info2 = int(info2)
    except Exception as e:                                 # noqa: BLE001 — 재풀이 실패 = ⓒ 실패 (fail-closed)
        s2, d, info2, Ib2, It2 = math.nan, math.inf, -1, math.nan, math.nan
        _err = f'{type(e).__name__}: {e}'
    else:
        _err = None
    c_ok = bool(info2 == 0 and math.isfinite(d) and d <= CERT_RESOLVE_TOL)
    out = {'version': CERT_VERSION, 'rtol_used': rt, 'rtol_max': CERT_RTOL_MAX, 'eps_I': CERT_EPS_I,
           'resolve_rtol': rr, 'resolve_rtol_floor': CERT_RESOLVE_RTOL_FLOOR, 'resolve_tol': CERT_RESOLVE_TOL,
           'info': int(info) if info is not None else None,
           'resid': (float(resid) if resid is not None else None), 'I_bot': Ib, 'I_top': It, 'imbalance': imb,
           'sigma': s1, 'sigma_resolve': s2, 'dsigma_rel': d, 'resolve_info': info2,
           'resolve_I_bot': Ib2, 'resolve_I_top': It2,
           'pass_a': bool(a_ok), 'pass_b': b_ok, 'pass_c': c_ok, 'ok': bool(a_ok and b_ok and c_ok)}
    if _err:
        out['resolve_error'] = _err
    return out


# ═════════════════════════ 봉인 탐침 (합성 · 리포 시험) ═════════════════════════
def probe_bed(seed, shape=PROBE_SHAPE, frac=PROBE_FRAC):
    """AM 바탕 (sid 1) + 아래 판에서 자라 위 판에 안 닿는 섬유 기둥 (sid 3 · 셀 몫 ≈ frac) — 결정적 (시드)."""
    rng = np.random.default_rng(int(seed))
    nx, ny, nz = shape
    sid = np.ones(shape, np.int8)
    target = int(round(frac * nx * ny * nz))
    used = np.zeros((nx, ny), bool)
    count = 0
    cols = rng.permutation(nx * ny)
    for c in cols:
        if count >= target:
            break
        i, j = divmod(int(c), ny)
        if used[i, j]:
            continue
        L = int(rng.integers(nz // 4, nz - 3))             # 위 판에 안 닿는다 (위 셋 이상 비움)
        L = min(L, target - count) if target - count >= 4 else L
        sid[i, j, :L] = 3
        used[i, j] = True
        count += L
    return sid


def probe_sigma_table():
    t = np.zeros(10)
    t[1] = t[2] = PROBE_SIGMA_AM
    t[3] = PROBE_SIGMA_FIBRE
    return t


def probe_system(sid, sig, vox=PROBE_VOX, s3=None):
    """생산 조립 (`solve_sigma_z`) 이 만든 행렬 L · b · 판 간선을 붙잡는다 (직접해로 푼다 — 그 해가 기준).
    → dict(L, b, Ab, gb, At, gt, phi_direct, idx)."""
    from scipy.sparse.linalg import spsolve
    if s3 is None:
        import step3_sigma as s3
    cap = {}
    old = s3._solve_cg

    def _rec(L, b, *a, **k):
        cap['L'] = L.tocsr(); cap['b'] = np.asarray(b, np.float64).copy()
        x = spsolve(cap['L'].tocsc(), cap['b'])
        cap['phi'] = x
        return x, 0
    s3._solve_cg = _rec
    try:
        res = s3.solve_sigma_z(sid, sig, vox, return_field=True, z_top_um=float(sid.shape[2]) * vox, z_bot_um=0.0)
    finally:
        s3._solve_cg = old
    cond = res['cond']
    idx = -np.ones(sid.shape, np.int64)
    idx[cond] = np.arange(int(cond.sum()))
    (cb, gb, _), (ct, gt, _) = res['plate_edges']['bot'], res['plate_edges']['top']
    Ab = idx[cb[0], cb[1], cb[2]]; At = idx[ct[0], ct[1], ct[2]]
    return {'L': cap['L'], 'b': cap['b'], 'Ab': Ab, 'gb': np.asarray(gb, np.float64), 'At': At,
            'gt': np.asarray(gt, np.float64), 'phi_direct': cap['phi'], 'idx': idx}


def junction_variant(sysd, sid, rj_ohm=PROBE_RJ_OHM):
    """`plain` 계에서 섬유 기둥마다 가운데 축방향 (z) 면 하나를 접합 간선 g_j = 1e4/R_j 로 바꾼다 (직렬 접합 꼴)."""
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    L = sysd['L'].tocsr().astype(np.float64)
    idx = sysd['idx']
    gj = 1.0e4 / float(rj_ohm)
    ui, vi, dg = [], [], []
    nx, ny, nz = sid.shape
    for i in range(nx):
        for j in range(ny):
            col = np.flatnonzero(sid[i, j, :] == 3)
            if len(col) < 4:
                continue
            km = int(col[len(col) // 2 - 1])
            u, v = int(idx[i, j, km]), int(idx[i, j, km + 1])
            if u < 0 or v < 0:
                continue
            gax = -float(L[u, v])
            ui.append(u); vi.append(v); dg.append(gj - gax)
    ui = np.asarray(ui); vi = np.asarray(vi); dg = np.asarray(dg)
    n = L.shape[0]
    D = sparse.coo_matrix((np.r_[-dg, -dg, dg, dg], (np.r_[ui, vi, ui, vi], np.r_[vi, ui, ui, vi])), shape=(n, n)).tocsr()
    L2 = (L + D).tocsr()
    out = dict(sysd)
    out['L'] = L2
    out['phi_direct'] = spsolve(L2.tocsc(), sysd['b'])
    out['n_junction'] = int(len(ui))
    return out


def probe_table(seeds=PROBE_SEEDS, rtols=PROBE_RTOLS, maxiter=PROBE_MAXITER, s3=None):
    """봉인 표 — 행마다 seed · 꼴 · rtol · info · 잔차 · 생산 술어 · σ 오차 (직접해 대비) · 판 전류 불균형 · 증서."""
    if s3 is None:
        import step3_sigma as s3
    rows = []
    old_mi = s3.CG_MAXITER
    s3.CG_MAXITER = int(maxiter)
    try:
        for seed in seeds:
            sid = probe_bed(seed)
            base = probe_system(sid, probe_sigma_table(), s3=s3)
            for variant, sysd in (('plain', base), ('junction', junction_variant(base, sid))):
                L, b = sysd['L'], sysd['b']
                Ib0, _ = plate_currents(sysd['phi_direct'], sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'])

                def _resolve(L_, b_, x0, rtol):
                    return s3._solve_cg(L_, b_, x0=x0, rtol=rtol)
                for rt in rtols:
                    it = [0]

                    def _cb(xk):
                        it[0] += 1
                    phi, info = _cg_count(s3, L, b, rt, it)
                    resid = float(np.linalg.norm(L @ phi - b) / max(np.linalg.norm(b), 1e-30))
                    prod_ok = bool(int(info) == 0 and math.isfinite(resid) and resid <= PROD_RESID_MAX)
                    Ib, It = plate_currents(phi, sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'])
                    err = abs(Ib - Ib0) / abs(Ib0)
                    c = certify(L, b, phi, int(info), resid, rt, sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'], 1.0, _resolve)
                    rows.append({'seed': int(seed), 'variant': variant, 'rtol': float(rt), 'info': int(info),
                                 'resid': resid, 'prod_ok': prod_ok, 'sigma_err': float(err), 'imbalance': c['imbalance'],
                                 'cert_ok': c['ok'], 'pass_a': c['pass_a'], 'pass_b': c['pass_b'], 'pass_c': c['pass_c'],
                                 'dsigma_resolve': c['dsigma_rel'], 'iters': it[0],
                                 'n_dof': int(L.shape[0]), 'n_junction': int(sysd.get('n_junction', 0))})
    finally:
        s3.CG_MAXITER = old_mi
    return rows


def _cg_count(s3, L, b, rt, it):
    """생산 `_solve_cg` 를 그대로 부르되 반복 수만 센다 (scipy cg 의 callback · 해는 같다)."""
    real = s3.cg

    def _wrap(A, bb, *a, **k):
        k = dict(k)
        k['callback'] = lambda xk: it.__setitem__(0, it[0] + 1)
        return real(A, bb, *a, **k)
    s3.cg = _wrap
    try:
        return s3._solve_cg(L, b, rtol=rt)
    finally:
        s3.cg = real


def derive_seal(rows, err_tol=SEAL_ERR_TOL, eps_start=SEAL_EPS_START):
    """설계 §6 절차 3 — 기계 규칙 (고르지 않는다)."""
    rts = sorted({r['rtol'] for r in rows}, reverse=True)          # 느슨한 것부터
    rtol_stop = None
    for rt in rts:
        sub = [r for r in rows if r['rtol'] == rt]
        if sub and all(r['sigma_err'] <= err_tol for r in sub):
            rtol_stop = rt
            break
    good = [r['imbalance'] for r in rows if r['sigma_err'] <= err_tol]
    bad = [r['imbalance'] for r in rows if r['sigma_err'] > err_tol]
    lo = max(good) if good else 0.0
    hi = min(bad) if bad else math.inf
    if lo < hi:
        if lo <= eps_start < hi:
            eps = eps_start
        elif math.isfinite(hi) and lo > 0.0:
            eps = math.sqrt(lo * hi)
        else:
            eps = max(lo, eps_start)
        diag_only = False
    else:
        eps, diag_only = None, True
    return {'rtol_stop': rtol_stop, 'eps_I': eps, 'interval': (lo, hi), 'b_diagnostic_only': diag_only,
            'n_rows': len(rows), 'n_good': len(good), 'n_bad': len(bad), 'err_tol': err_tol, 'eps_start': eps_start}


def main(argv=None):
    ap = argparse.ArgumentParser(description='STEP3 수렴 증서 봉인 표 (합성 직접해 대조 · 실침대 아님)')
    ap.add_argument('--table', action='store_true', help='봉인 표를 찍는다')
    a = ap.parse_args(argv)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    if a.table:
        tab = probe_table()
        for r in tab:
            print(f"{r['variant']:9s} seed {r['seed']} rtol {r['rtol']:.0e} info {r['info']} resid {r['resid']:.2e} "
                  f"prod_ok {r['prod_ok']!s:5s} σerr {r['sigma_err']:.3e} imb {r['imbalance']:.3e} cert {r['cert_ok']} "
                  f"(a {r['pass_a']} b {r['pass_b']} c {r['pass_c']}) it {r['iters']}")
        print(derive_seal(tab))
    return 0


if __name__ == '__main__':
    sys.exit(main())

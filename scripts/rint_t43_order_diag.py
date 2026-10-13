#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""①′ T4-3 `raster_order_size` (원장 `RINTG-11`) — legacy raster 의 입자 행 순서 의존 크기 (보고 전용 · 2026-10-13).

등록 (실행 전 커밋) = docs/reviews/rint_t43_order_dependence_registration_20261013.md — K 7 (역순 + default_rng seed 20261013 … 20261018) ·
침대 셋 (real_14 · case15 · kit_ps_5_5 · 리포 안 AM-only scaffold) · 격자 둘 (T4-1 과 같음) · 보고 항목 · σ_OFF = real_14 × vox 0.4 만.
근거 = v3 §1 T4-3 · v3.1 §2 · Codex v3 판정 §3.  판정 없음 — 결과는 legacy OFF 계약 (선택 (1)) 을 바꾸지 않는다 (크기가 의미 있으면
D21 = 1저자).  ①′ 정량 채택 · 생산 HOLD · 웹앱 화면 없음 (기구 · 시험 전용).

보고 (π_k ↔ π₀ · 셀 단위): sid 가 다른 셀 (라벨 AM_S ↔ AM_P · 마스크 AM ↔ 비어 있음) · pid 가 다른 셀 (pid 는 원래 행 번호로 되돌려 비교) ·
자리 (lens = 셀 중심을 품는 구 ≥ 2 · bridge = 구 ≤ 1 이고 브리지 공 (두 계산 순서 합집합) 안 · other = 그 밖) · 렌즈 종류 (mixed · AM_S · AM_P).

  python3 scripts/rint_t43_order_diag.py --out docs/data/rint_t43_order_20261013
"""
import argparse
import datetime
import json
import os
import platform
import resource
import subprocess
import sys
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import step3_sigma as S3          # noqa: E402

K = 7
SEEDS = (20261013, 20261014, 20261015, 20261016, 20261017, 20261018)
TOL_AM_UM = 0.10
SIGMA_BED, SIGMA_CFG = 'real_14', 'vox0.4_bridge1.2h'
SIGMA_Z_TOP_UM = 30.2845          # real_14 판 메시 z (docs/data/real14_reference_20260928/README.md)
SIGMA_BUDGET_S = 1200.0           # 솔브 하나 벽시계 상한 (등록 §2)
SIGMA_RTOL = 1e-12


def registered_perms(N):
    """등록된 순서 — π₀ 파일 순서 · π₁ 역순 · π₂ … π₇ = default_rng(seed).permutation(N)."""
    return [np.arange(N), np.arange(N)[::-1]] + [np.random.default_rng(s).permutation(N) for s in SEEDS]


def _geom_grids(c, r, t, lo, shape, vox, bridge, tol):
    """셀마다 품는 AM_S · AM_P 구 수 (int16) · 브리지 공 (두 계산 순서 합집합) 안 여부 — `rasterize` · 원장과 같은 판정식 (`_ball_cells`)."""
    n = np.array(shape, dtype=int)
    nS = np.zeros(shape, np.int16); nP = np.zeros(shape, np.int16); br = np.zeros(shape, bool)
    lo = np.asarray(lo, np.float64)
    for k in range(len(c)):
        hit = S3._ball_cells(c[k], r[k], lo, vox, n)
        if hit is None:
            continue
        i0, i1, m = hit
        g = nP if int(t[k]) == 1 else nS
        g[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1][m] += 1
    rb = S3._am_bridge_radius(vox, bridge)
    for i, j, d in S3.am_bridge_pairs(c, r, tol):
        for mid in S3._am_bridge_claim_mids(c, r, i, j, d):
            hit = S3._ball_cells(mid, rb, lo, vox, n)
            if hit is None:
                continue
            i0, i1, m = hit
            br[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1][m] = True
    return nS, nP, br


def _raster(c, r, t, lo, hi, vox, bridge, p, tol):
    sid, pid = S3.rasterize(c[p], r[p], t[p], None, None, lo, hi, vox, bridge_um=bridge, tol_am_um=tol)
    pid_orig = np.where(pid >= 0, p[np.maximum(pid, 0)], -1).astype(np.int64)     # 원래 행 번호로
    return sid, pid_orig


def order_diag_raster(c, r, t, lo, hi, vox, bridge, perms, tol=TOL_AM_UM):
    """perms[0] (기준) 과 나머지 순서의 raster 를 셀 단위로 비교 → {'ref': …, 'perms': [π_k 마다 dict]}."""
    c = np.asarray(c, np.float64); r = np.asarray(r, np.float64); t = np.asarray(t)
    sid0, pid0 = _raster(c, r, t, lo, hi, vox, bridge, np.asarray(perms[0]), tol)
    nS, nP, br = _geom_grids(c, r, t, lo, sid0.shape, vox, bridge, tol)
    nsph = nS.astype(np.int32) + nP
    lens = nsph >= 2
    brg = ~lens & br
    other = ~lens & ~brg
    am0 = np.isin(sid0, (1, 2))
    out = {'ref': {'grid': list(sid0.shape), 'n_cells': int(sid0.size), 'n_M': int(am0.sum()),
                   'n_lens_cells': int((lens & am0).sum()), 'n_bridge_only_cells': int((brg & am0).sum())}, 'perms': []}
    for p in perms[1:]:
        sid, pid = _raster(c, r, t, lo, hi, vox, bridge, np.asarray(p), tol)
        am = np.isin(sid, (1, 2))
        d = sid != sid0
        label = d & am0 & am
        mask = am0 != am
        dp = pid != pid0

        def loc(x):
            return {'lens': int((x & lens).sum()), 'bridge': int((x & brg).sum()), 'other': int((x & other).sum())}
        out['perms'].append({
            'n_sid_diff': int(d.sum()), 'n_label': int(label.sum()), 'n_mask': int(mask.sum()),
            'n_other_transition': int((d & ~label & ~mask).sum()),
            'loc': loc(d),
            'lens_kind': {'mixed': int((d & lens & (nS > 0) & (nP > 0)).sum()), 'AM_S': int((d & lens & (nS > 0) & (nP == 0)).sum()),
                          'AM_P': int((d & lens & (nS == 0) & (nP > 0)).sum())},
            'n_pid_diff': int(dp.sum()), 'pid_loc': loc(dp), 'n_M': int(am.sum()),
            'sample_cells': [[int(v) for v in x] for x in np.argwhere(d)[:8]]})
    return out


def _agg(perms, key, sub=None):
    v = np.array([(p[key] if sub is None else p[key][sub]) for p in perms], np.float64)
    return {'min': float(v.min()), 'median': float(np.median(v)), 'max': float(v.max())} if v.size else None


def _cg_tight(L, b):
    from scipy import sparse
    from scipy.sparse.linalg import cg
    M = sparse.diags(1.0 / L.diagonal())
    return cg(L, b, rtol=SIGMA_RTOL, maxiter=200000, M=M)


def sigma_off(c, r, t, lo, hi, vox, bridge, perms, z_top_um, tol=TOL_AM_UM, budget_s=SIGMA_BUDGET_S):
    """등록 §2 σ_OFF — 생산 solve_sigma_z (AM-only 전자 σ 표) · 이 진단 안에서만 _solve_cg = Jacobi CG rtol 1e−12."""
    sig = S3.electronic_sigma_table(0.010, 0.005, 100.0, 10.0, 250.0)
    old = S3._solve_cg
    S3._solve_cg = _cg_tight
    rows = []
    try:
        for k, p in enumerate(perms):
            sid, _pid = _raster(c, r, t, lo, hi, vox, bridge, np.asarray(p), tol)
            t0 = time.time()
            res = S3.solve_sigma_z(sid, sig, vox, z_bot_um=0.0, z_top_um=z_top_um)
            el = time.time() - t0
            rows.append({'perm': k, 'sigma_eff_S_cm': res['sigma_eff'], 'n_dof': res['n_dof'], 'cg_info': res['cg_info'],
                         'resid': res['resid'], 'unconverged': res['unconverged'], 'wall_s': round(el, 1)})
            if el > budget_s:
                rows.append({'status': 'not_computed (cost)', 'why': f'솔브 하나 {el:.0f} s > 상한 {budget_s:.0f} s — 나머지 순서 σ 를 멈춘다'})
                break
    finally:
        S3._solve_cg = old
    s0 = rows[0]['sigma_eff_S_cm'] if rows and 'sigma_eff_S_cm' in rows[0] else None
    rel = [x['sigma_eff_S_cm'] / s0 - 1.0 for x in rows[1:] if 'sigma_eff_S_cm' in x] if s0 else []
    return {'rows': rows, 'rel_change_vs_pi0': rel,
            'rel_abs_max': (float(np.max(np.abs(rel))) if rel else None),
            'solver': f'생산 solve_sigma_z · 이 진단 안에서만 _solve_cg = Jacobi CG rtol {SIGMA_RTOL:g} maxiter 200000',
            'sigma_table': 'electronic_sigma_table(0.010, 0.005, …) — AM_S 0.010 · AM_P 0.005 S/cm · 첨가제 없음',
            'plates_um': [0.0, z_top_um]}


def _git(*args):
    try:
        return subprocess.run(['git', '-C', ROOT, *args], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:                                  # noqa: BLE001
        return None


def run_all(out_dir):
    import rint_t41_census as T41
    #  출처는 **실행 시작** 시점에 잰다 (10-13 첫 실행은 끝에 재서 그 사이 커밋의 HEAD 가 찍혔다 — blob 은 같았다 · README 표지)
    head0 = _git('rev-parse', 'HEAD')
    blobs0 = {f: _git('hash-object', f) for f in ('scripts/step3_sigma.py', 'scripts/rint_t43_order_diag.py',
                                                  'scripts/rint_t41_census.py', 'scripts/rint_iface_join.py')}
    os.makedirs(out_dir, exist_ok=True)
    jobs, sig = [], None
    for bed in T41.BEDS:
        scaf, L, jn, _db, _src = T41.bed_setup(bed)
        if jn is not None:
            c, r, t = jn['particles']['c_um'], jn['particles']['r_um'], jn['particles']['t']
        else:
            import rint_iface_join as J
            sc = J.read_scaffold_csv(scaf)
            c, r, t = sc['xyz'] * 1000.0, sc['r'] * 1000.0, sc['t']
        lo, hi = (0.0, 0.0, 0.0), (L, L, float((c[:, 2] + r).max()))
        perms = registered_perms(len(c))
        for cfg, C in T41.CONFIGS.items():
            t0 = time.time()
            R = order_diag_raster(c, r, t, lo, hi, C['vox'], C['bridge_um'], perms)
            el = time.time() - t0
            P = R['perms']
            nM = R['ref']['n_M']
            summ = {k: _agg(P, k) for k in ('n_sid_diff', 'n_label', 'n_mask', 'n_other_transition', 'n_pid_diff')}
            summ['loc'] = {k: _agg(P, 'loc', k) for k in ('lens', 'bridge', 'other')}
            summ['lens_kind'] = {k: _agg(P, 'lens_kind', k) for k in ('mixed', 'AM_S', 'AM_P')}
            summ['frac_sid_diff_of_n_M'] = {k: (v / nM if nM else None) for k, v in summ['n_sid_diff'].items()}
            jobs.append({'bed': bed, 'config': cfg, 'vox_um': C['vox'], 'bridge_um': C['bridge_um'], 'box_um': [list(lo), list(hi)],
                         'n_particles': int(len(c)), 'ref': R['ref'], 'per_perm': P, 'summary': summ, 'wall_s': round(el, 1),
                         'peak_rss_mb': round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0, 1)})
            print(f"  {bed} × {cfg}: {el:.0f} s · n_M {nM} · sid 차 {summ['n_sid_diff']} · 라벨 {summ['n_label']} · 마스크 {summ['n_mask']} · "
                  f"pid 차 {summ['n_pid_diff']}", flush=True)
            if bed == SIGMA_BED and cfg == SIGMA_CFG:
                sig = sigma_off(c, r, t, lo, hi, C['vox'], C['bridge_um'], perms, SIGMA_Z_TOP_UM)
                print(f"  σ_OFF ({bed} × {cfg}): rel max {sig['rel_abs_max']} · rows {len(sig['rows'])}", flush=True)
    import scipy as _sp
    doc = {'kind': 'rint_t43_order_diag', 'version': 'v1',
           'date_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
           'registration': 'docs/reviews/rint_t43_order_dependence_registration_20261013.md',
           'status': ('보고 전용 (RINTG-11) — 판정 없음 · legacy OFF 계약 (선택 (1)) 무변경 · 크기가 의미 있으면 D21 = 1저자 · '
                      '①′ 정량 채택 · 생산 HOLD · 웹앱 화면 없음'),
           'K': K, 'seeds': list(SEEDS), 'git_head_at_start': head0, 'git_head': _git('rev-parse', 'HEAD'),
           'code_blobs': blobs0,
           'environment': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': _sp.__version__},
           'jobs': jobs, 'sigma_off': {'bed': SIGMA_BED, 'config': SIGMA_CFG, **(sig or {'status': 'not_run'})},
           'sigma_not_done': 'case15 · kit_ps_5_5 · vox 0.15 의 σ_OFF = 이 컨테이너에서 하지 않음 (등록 §2 · 생산 기계 몫)'}
    with open(os.path.join(out_dir, 'order_diag.json'), 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
        fh.write('\n')
    return doc


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    run_all(a.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())

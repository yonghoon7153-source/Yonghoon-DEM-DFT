#!/usr/bin/env python3
"""실침대 계단 인자 k 를 **여러 격자에서** 재고, 옛/새 estimator 를 나란히 놓는다.

★ 왜 (Codex CDX-02 / CL-29): 리뷰가 옛 estimator 로 실침대 k 를 세 격자에서 재
  1.4855@0.4 · 1.4917@0.3 · 1.4461@0.25 (폭 0.046) 를 얻고 "k 는 격자 무관이 아니다" 라고
  결론했다.  그런데 그 estimator 는 `np.unique` 로 경로 순서를 버려 저항 경로 길이가 아니고,
  참값을 아는 통제 합성 실험에서 **그 산포가 구간 길이에 좌우된다**는 것이 확인됐다
  (구간 1.08 µm 에서 폭 0.0417 = 실침대 0.0456 과 같은 크기).
  ⇒ 실침대에서 **같은 점 구름**에 두 estimator 를 다 걸어 갈라낸다.

★ 규율: 씨는 **한 번만** 뿌리고 모든 격자·모든 estimator 가 그 점 구름을 공유한다
  (CLAUDE.md 사다리 ② — 따로 뿌리면 차이가 격자 때문인지 시드 때문인지 못 가른다).

사용:
  python3 scripts/sr01_k_grid_sweep.py --kit kit_ps_7_3 --vox 0.4 0.3 0.25
  python3 scripts/sr01_k_grid_sweep.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fibre_segment_raster import segment_cells                  # noqa: E402
from sr01_staircase_factor import staircase_factor              # noqa: E402


def k_legacy(pts, fid, vox, gap_tol=2.0):
    """f21990f8 시점의 estimator — `np.unique` 로 **경로 순서와 재방문을 버린다**.

    ⚠ 비교 기준으로만 둔다.  이것으로 얻은 k 를 물리 보정계수로 쓰지 말 것.
    """
    P, F = np.asarray(pts, np.float64), np.asarray(fid)
    tot_path = tot_true = 0.0
    for f in np.unique(F):
        Q = P[F == f]
        if len(Q) < 2:
            continue
        d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
        med = float(np.median(d)) if len(d) else 0.0
        brk = (np.nonzero(d > gap_tol * med)[0] + 1) if med > 0 else np.array([], int)
        for R in (np.split(Q, brk) if len(brk) else [Q]):
            if len(R) < 2:
                continue
            cells = np.vstack([segment_cells(R[i], R[i + 1], vox) for i in range(len(R) - 1)])
            cells = np.unique(cells, axis=0)
            L_arc = float(np.linalg.norm(np.diff(R, axis=0), axis=1).sum())
            if L_arc <= 0:
                continue
            tot_path += max(len(cells) - 1, 0) * vox
            tot_true += L_arc
    return float(tot_path / tot_true) if tot_true > 0 else float('nan')


def runs_of(pts, fid, gap_tol=2.0):
    """폴리라인을 **격자와 무관하게** 미리 끊어 둔다 — 세 격자가 같은 구간 목록을 본다.

    ⚠ 왜 필요한가: `staircase_factor` 는 셀이 2개 미만인 구간을 건너뛴다.  그 판정이
      vox 에 달려 있어서 격자마다 **모집단이 달라진다** (실측 581 / 581 / 565).  그러면
      "k 가 격자에 따라 다르다" 가 구간 집합이 달라서인지 경로가 달라서인지 못 가른다 —
      이 리뷰 전체가 지적한 바로 그 오류다.  ⇒ 구간을 먼저 고정하고 그 위에서만 잰다.
    """
    P, F = np.asarray(pts, np.float64), np.asarray(fid)
    out = []
    for f in np.unique(F):
        Q = P[F == f]
        if len(Q) < 2:
            continue
        d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
        med = float(np.median(d)) if len(d) else 0.0
        brk = (np.nonzero(d > gap_tol * med)[0] + 1) if med > 0 else np.array([], int)
        for R in (np.split(Q, brk) if len(brk) else [Q]):
            if len(R) >= 2 and float(np.linalg.norm(np.diff(R, axis=0), axis=1).sum()) > 0:
                out.append(R)
    return out


def _run_k(R, vox):
    """한 구간의 (경로길이, 참길이) — 없으면 None.  staircase_factor 와 **같은 규약**."""
    cells = np.vstack([segment_cells(R[i], R[i + 1], vox) for i in range(len(R) - 1)])
    keep = np.ones(len(cells), bool)
    keep[1:] = (cells[1:] != cells[:-1]).any(1)
    cells = cells[keep]
    if len(cells) < 2:
        return None
    n_hops = int(np.abs(np.diff(cells.astype(np.int64), axis=0)).sum())
    L_arc = float(np.linalg.norm(np.diff(R, axis=0), axis=1).sum())
    L_chord = float(np.linalg.norm(R[-1] - R[0]))
    span = float(np.linalg.norm((cells[-1] + 0.5) * vox - (cells[0] + 0.5) * vox))
    if L_chord <= 0 or span <= 0:
        return None
    return n_hops * vox, L_arc * (span / L_chord)


def sweep_common(pts, fid, voxes):
    """★ 모든 격자에서 유효한 구간만 써서 k 를 잰다 (공통 모집단)."""
    runs = runs_of(pts, fid)
    per = {v: [_run_k(R, v) for R in runs] for v in voxes}
    ok = [i for i in range(len(runs)) if all(per[v][i] is not None for v in voxes)]
    rows = []
    for v in voxes:
        num = sum(per[v][i][0] for i in ok)
        den = sum(per[v][i][1] for i in ok)
        rows.append({'vox': float(v), 'k_common': float(f'{num / den:.6f}')})
    lens = [float(np.linalg.norm(np.diff(runs[i], axis=0), axis=1).sum()) for i in ok]
    return rows, {'n_runs_total': len(runs), 'n_runs_common': len(ok),
                  'dropped': len(runs) - len(ok),
                  'run_len_um_med': float(f'{np.median(lens):.4g}') if lens else None,
                  'short_run_frac': float(f'{np.mean(np.array(lens) < 1.0):.4f}') if lens else None}


def sweep(pts, fid, voxes):
    rows = []
    for v in voxes:
        kn, st = staircase_factor(pts, fid, v)
        rows.append({'vox': float(v), 'k_new': float(f'{kn:.6f}'),
                     'k_legacy': float(f'{k_legacy(pts, fid, v):.6f}'),
                     'n_segments': st['n_segments'],
                     'run_len_um_med': st['run_len_um_med'],
                     'short_run_frac': st['short_run_frac'],
                     'short_run_warning': st['short_run_warning']})
    data = list(rows)                          # ← 요약을 넣기 **전** 스냅샷 (안 그러면 자기를 읽는다)
    for tag in ('k_new', 'k_legacy'):
        vals = [r[tag] for r in data]
        rows.append({'summary': tag, 'min': min(vals), 'max': max(vals),
                     'range': float(f'{max(vals) - min(vals):.6f}')})
    return rows


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    # 축정렬 긴 섬유: 새 estimator = 1 정확, 옛 estimator 는 끝셀 편향으로 < 1
    t = np.arange(0, 40) * 0.12
    P = np.stack([t, np.full_like(t, 1.1), np.full_like(t, 2.1)], 1)
    F = np.zeros(len(P), int)
    kn, _ = staircase_factor(P, F, 0.4)
    kl = k_legacy(P, F, 0.4)
    chk(f'축정렬: 새 = 1.000000 (측정 {kn:.6f})', abs(kn - 1.0) < 1e-9)
    chk(f'축정렬: 옛 estimator 는 1 미만 = 비물리 (측정 {kl:.4f})', kl < 0.99)

    # 통제 합성: 짧은 구간일수록 **옛** estimator 의 격자 산포가 커진다 (CL-29 재현)
    rng = np.random.default_rng(0)
    out = {}
    for npts in (60, 6):
        pts, fids = [], []
        for i in range(400):
            u = rng.normal(size=3); u /= np.linalg.norm(u)
            s = np.arange(0, npts) * 0.12
            pts.append(np.array([10., 10., 10.]) + np.outer(s, u))
            fids.append(np.full(npts, i))
        Pp, Ff = np.vstack(pts), np.concatenate(fids)
        kk = [k_legacy(Pp, Ff, v) for v in (0.4, 0.3, 0.25)]
        out[npts] = max(kk) - min(kk)
    chk(f'CL-29: 짧은 구간이 옛 estimator 의 격자 산포를 키운다 '
        f'(긴 {out[60]:.4f} → 짧은 {out[6]:.4f})', out[6] > 5 * out[60])
    print(f'\nsr01_k_grid_sweep selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--kit', default='kit_ps_7_3')
    ap.add_argument('--n-grid', type=int, default=288)
    ap.add_argument('--vgcf-wt', type=float, default=1.0)
    ap.add_argument('--max-fibres', type=int, default=0, help='0 = 전부')
    ap.add_argument('--vox', type=float, nargs='+', default=[0.4, 0.3, 0.25])
    ap.add_argument('--out', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())

    from sr01_realbed_ab import seed_carbon_on_kit               # noqa: E402
    print(f'씨 뿌리는 중 — {a.kit}, n_grid={a.n_grid}, VGCF {a.vgcf_wt} wt% '
          f'(모든 격자가 이 **한** 점 구름을 공유한다)', flush=True)
    S = seed_carbon_on_kit(a.kit, a.n_grid, a.vgcf_wt, 0, max_fibres=a.max_fibres)
    print(f'  점 {len(S["pts"]):,} · 섬유 {len(np.unique(S["fid"])):,}', flush=True)

    rows = sweep(S['pts'], S['fid'], a.vox)
    crows, cinfo = sweep_common(S['pts'], S['fid'], a.vox)
    kc = {r['vox']: r['k_common'] for r in crows}
    print()
    print(f'{"vox":>6} {"k_legacy":>10} {"k_new":>10} {"k_공통모집단":>13} '
          f'{"구간중앙":>9} {"1µm미만":>8} {"구간수":>8}')
    for r in rows:
        if 'summary' in r:
            continue
        print(f'{r["vox"]:>6} {r["k_legacy"]:>10.4f} {r["k_new"]:>10.4f} '
              f'{kc[r["vox"]]:>13.4f} {r["run_len_um_med"]:>9.3f} '
              f'{r["short_run_frac"]:>8.1%} {r["n_segments"]:>8,}')
    print()
    for r in rows:
        if 'summary' in r:
            print(f'  {r["summary"]:>12} 폭 = {r["range"]:.4f}  ({r["min"]} ~ {r["max"]})')
    cv = list(kc.values())
    print(f'  {"k_공통모집단":>12} 폭 = {max(cv) - min(cv):.4f}  ({min(cv)} ~ {max(cv)})')
    print(f'\n  공통 구간 {cinfo["n_runs_common"]:,} / 전체 {cinfo["n_runs_total"]:,} '
          f'(격자마다 유효성이 달라 {cinfo["dropped"]:,} 개 제외) · '
          f'구간중앙 {cinfo["run_len_um_med"]} µm · 1 µm 미만 {cinfo["short_run_frac"]:.1%}')
    rows.append({'summary': 'k_common', 'min': min(cv), 'max': max(cv),
                 'range': float(f'{max(cv) - min(cv):.6f}'), **cinfo})
    w = next((r.get('short_run_warning') for r in rows if r.get('short_run_warning')), None)
    if w:
        print(f'\n  ⚠ {w}')
    if a.out:
        json.dump(rows, open(a.out, 'w'), ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')

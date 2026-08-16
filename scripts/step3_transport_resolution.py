#!/usr/bin/env python3
"""STEP3 **수송**의 해상도 규칙을 잰다 — 역학의 `d_h/dx ≳ 3.5` 에 대응하는 것.

★ 왜 이것이 목적지의 병목인가 (2026-08-16):
  MPM 을 확실히 쓰려면 세 가지가 서야 한다 — ① 역학 ② 수송 ③ **"어디까지 믿나" 규칙**.
  역학에는 ③ 이 있다 (`d_h/dx ≳ 3.5`, 잔여 ~4 %; CLAUDE.md se_curve 절).  **수송에는 없었다.**
  그래서 σ_ion/σ_e 가 격자와 함께 움직일 때 그것이 결함인지 미해상인지 판정할 근거가 없었고,
  SR-01 의 결론들이 무너진 뿌리가 거기다.

★ 왜 GPU 가 필요 없나:
  `step3_sigma.solve_sigma_z` 는 **sid 배열을 직접 받는다**.  그래서 MPM 압밀을 거치지 않고
  킷 스캐폴드(리포 안 `docs/data/kit_ps_scaffolds/`)의 **해석적 구**를 원하는 vox 로 직접
  래스터해 풀 수 있다.  기하가 해석적이라 참값이 **격자 무관**이고, 남는 변화는 전부
  이산화 것이다 — 규칙을 세우기에 오히려 실침대보다 낫다.

★ origin 앙상블이 필수인 이유:
  단일 origin 의 σ 는 격자 **위상**에 2.4~5.8 % 흔들린다 (아래 실측).  한 origin 만 보고
  격자 추세를 읽으면 그 잡음을 물리로 오독한다.  ⇒ half-cell shift ×4 를 평균한다.

사용:
  python3 scripts/step3_transport_resolution.py --kit kit_ps_7_3 --vox 0.4 0.3 0.25 0.2
  python3 scripts/step3_transport_resolution.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from step3_sigma import solve_sigma_z                            # noqa: E402

SID_AM, SID_SE, SID_SDCP = 1, 6, 5
SIGMA_ION_SE = 3.0e-3                                            # S/cm (Cronau, se_material)
SIGMA_E_AM = 0.010                                               # S/cm (AM_S, SIGMA_DEFAULT)
SIGMA_E_SDCP = 250.0                                             # S/cm (USER anchor 2026-07-16)
SDCP_D_UM = 0.30


def sdcp_point_cells(centres, vox, origin, length_um, n):
    """**생산 규약 재현** — SDCP 는 입자당 점 하나이고 그 점이 든 셀 **하나**만 찍힌다.

    `seed_sdcp` singles 모드가 입자당 점 1개를 내고, `step3_sigma` 첨가제 경로는 `add_fid` 가
    없으면 `np.floor((pts-lo)/vox)` 로 셀 하나를 찍는다 (섬유만 선분 스탬프를 받는다).
    ⇒ 한 입자가 차지하는 부피가 **vox³** 이 되어 참부피 π/6·d³ 의 4.53× (vox 0.4) 가 된다.
    이 함수는 그 규약을 RVE 에서 **그대로** 재현해 σ 영향을 재기 위한 것이다 (CL-25).
    """
    rel = np.asarray(centres, float) - np.asarray(origin, float)
    m = ((rel >= 0) & (rel < length_um)).all(1)
    ijk = np.floor(rel[m] / vox).astype(int)
    ijk = ijk[((ijk >= 0) & (ijk < n)).all(1)]
    return ijk


def rasterize_spheres(vox, origin, length_um, spheres):
    """해석적 구 목록 → sid 격자.  `spheres` = [(centres, radii, sid_code), ...] 순서대로 덮는다.

    ⚠ 순서가 규약이다: SE 를 먼저 찍고 AM 이 덮는다 (production `step3_sigma` 와 같게 —
      AM 이 SE 를 밀어낸 자리는 AM 이다).  뒤집으면 φ 가 달라진다.
    """
    n = int(round(length_um / vox))
    sid = np.zeros((n, n, n), np.int8)
    g = (np.arange(n) + 0.5) * vox
    X, Y, Z = np.meshgrid(g, g, g, indexing='ij')
    o = np.asarray(origin, float)
    for cen, rad, code in spheres:
        rel = np.asarray(cen, float) - o
        r = np.asarray(rad, float)
        m = ((rel + r[:, None] > 0) & (rel - r[:, None] < length_um)).all(1)
        for p, rr in zip(rel[m], r[m]):
            i0 = np.maximum(((p - rr) / vox).astype(int), 0)
            i1 = np.minimum(((p + rr) / vox).astype(int) + 2, n)
            if (i0 >= i1).any():
                continue
            sx, sy, sz = (slice(i0[k], i1[k]) for k in range(3))
            d2 = ((X[sx, sy, sz] - p[0]) ** 2 + (Y[sx, sy, sz] - p[1]) ** 2
                  + (Z[sx, sy, sz] - p[2]) ** 2)
            sid[sx, sy, sz][d2 <= rr * rr] = code
    return sid


def resolution_sweep(spheres, base_origin, length_um, voxes, feature_d_um=1.0, n_origin=4):
    """격자 × origin 앙상블 → σ_ion 표.  반환 rows + 판정."""
    sig = np.zeros(9)
    sig[SID_SE] = SIGMA_ION_SE
    rows = []
    for vox in voxes:
        shifts = [np.zeros(3)] + [np.eye(3)[k] * (vox / 2.0) for k in range(3)][:n_origin - 1]
        vals, phi = [], []
        for sh in shifts:
            sid = rasterize_spheres(vox, np.asarray(base_origin, float) + sh, length_um, spheres)
            vals.append(float(solve_sigma_z(sid, sig, vox)['sigma_eff']))
            phi.append(float((sid == SID_SE).mean()))
        vals = np.array(vals)
        rows.append({'vox': float(vox), 'feature_per_dx': float(f'{feature_d_um / vox:.3f}'),
                     'sigma_ion_origins': [float(f'{v:.6g}') for v in vals],
                     'sigma_ion_mean': float(f'{vals.mean():.6g}'),
                     'origin_spread_pct': float(f'{(vals.max() / vals.min() - 1) * 100:.3g}'),
                     'phi_se_mean': float(f'{np.mean(phi):.4f}'),
                     'n_cells': int(round(length_um / vox) ** 3)})
    for a, b in zip(rows, rows[1:]):
        b['inc_pct'] = float(f'{(b["sigma_ion_mean"] / a["sigma_ion_mean"] - 1) * 100:.3g}')
    return rows


def verdict(rows, tol_pct=3.0):
    """어느 `feature/dx` 부터 origin-평균이 `tol_pct` 안에서 안정되나."""
    ok = [r for r in rows[1:] if abs(r.get('inc_pct', 1e9)) <= tol_pct]
    return {
        'tol_pct': tol_pct,
        'converged_from_feature_per_dx': (min(r['feature_per_dx'] for r in ok) if ok else None),
        'max_origin_spread_pct': max(r['origin_spread_pct'] for r in rows),
        'note': ('origin-평균의 증분이 tol 안에 드는 최소 feature/dx.  ⚠ **단일 origin 은 '
                 '이 tol 을 만족하지 않는다** — origin 폭이 그보다 크다.  단일 origin σ 를 '
                 '이 tol 로 인용하지 말 것.'),
    }


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    # ① 균질 블록 = 해석해 σ_eff = σ_SE (기하가 없으면 격자도 무관해야 한다)
    sig = np.zeros(9)
    sig[SID_SE] = SIGMA_ION_SE
    for vox in (0.5, 0.25):
        sid = np.full((int(8 / vox),) * 3, SID_SE, np.int8)
        se = float(solve_sigma_z(sid, sig, vox)['sigma_eff'])
        chk(f'① 균질 블록 vox {vox} = σ_SE ({se:.6g} vs {SIGMA_ION_SE:.6g})',
            abs(se / SIGMA_ION_SE - 1) < 1e-6)
    # ② 래스터 순서 규약 — AM 이 SE 를 덮는다
    c = np.array([[2.0, 2.0, 2.0]])
    r = np.array([1.0])
    s = rasterize_spheres(0.25, (0, 0, 0), 4.0, [(c, r, SID_SE), (c, r, SID_AM)])
    chk('② 겹치면 뒤에 찍은 상(AM)이 이긴다', (s == SID_AM).any() and not (s == SID_SE).any())
    # ③ 구 부피가 격자를 조이면 해석값으로 수렴 (래스터가 옳게 도는지)
    v = []
    for vox in (0.4, 0.2, 0.1):
        s = rasterize_spheres(vox, (0, 0, 0), 4.0, [(c, r, SID_SE)])
        v.append((s == SID_SE).sum() * vox ** 3)
    exact = 4.0 / 3.0 * np.pi
    chk(f'③ 구 부피 → 4πr³/3 = {exact:.4f} (측정 {v[0]:.4f} → {v[2]:.4f})',
        abs(v[2] / exact - 1) < abs(v[0] / exact - 1) and abs(v[2] / exact - 1) < 0.03)
    # ④ verdict 가 **단일 origin 을 tol 로 인용하지 말라**고 말한다
    rows = [{'vox': 0.4, 'feature_per_dx': 2.5, 'sigma_ion_mean': 1.0, 'origin_spread_pct': 3.5},
            {'vox': 0.3, 'feature_per_dx': 3.3, 'sigma_ion_mean': 1.04, 'origin_spread_pct': 5.8,
             'inc_pct': 4.0},
            {'vox': 0.25, 'feature_per_dx': 4.0, 'sigma_ion_mean': 1.06,
             'origin_spread_pct': 3.2, 'inc_pct': 1.7}]
    vd = verdict(rows, tol_pct=3.0)
    chk(f'④ 수렴 시작 feature/dx = 4.0 (측정 {vd["converged_from_feature_per_dx"]})',
        vd['converged_from_feature_per_dx'] == 4.0)
    chk('④b origin 폭이 tol 보다 크다는 것을 보고한다',
        vd['max_origin_spread_pct'] > vd['tol_pct'])
    print(f'\nstep3_transport_resolution selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--kit', default='kit_ps_7_3')
    ap.add_argument('--len-um', type=float, default=20.0, help='RVE 한 변')
    ap.add_argument('--vox', type=float, nargs='+', default=[0.4, 0.3, 0.25, 0.2])
    ap.add_argument('--tol-pct', type=float, default=3.0)
    ap.add_argument('--out', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())

    from sr01_realbed_ab import load_kit                          # noqa: E402
    am_c, am_r, se_c, se_r, lat, thick = load_kit(a.kit)
    base = np.array([lat / 2 - a.len_um / 2, lat / 2 - a.len_um / 2, thick / 2 - a.len_um / 2])
    d_se = float(2 * np.median(se_r))
    print(f'{a.kit}: SE Ø {d_se:.2f} µm · RVE {a.len_um} µm³ · 중앙 크롭')
    rows = resolution_sweep([(se_c, se_r, SID_SE), (am_c, am_r, SID_AM)], base, a.len_um,
                            a.vox, feature_d_um=d_se)
    print(f'\n{"vox":>6} {"SEØ/dx":>7} {"φ_SE":>7} {"σ_ion 평균":>12} {"증분%":>8} {"origin폭%":>10}')
    for r in rows:
        print(f'{r["vox"]:>6} {r["feature_per_dx"]:>7.1f} {r["phi_se_mean"]:>7.4f} '
              f'{r["sigma_ion_mean"]:>12.6g} {r.get("inc_pct", float("nan")):>8.2f} '
              f'{r["origin_spread_pct"]:>10.2f}')
    vd = verdict(rows, a.tol_pct)
    print(f'\n  ★ origin-평균이 ±{vd["tol_pct"]} % 안에 드는 최소 SE Ø/dx = '
          f'**{vd["converged_from_feature_per_dx"]}**')
    print(f'  ⚠ 단일 origin 은 이 tol 을 못 지킨다 — origin 폭 최대 '
          f'{vd["max_origin_spread_pct"]:.2f} %.  단일 origin σ 인용 금지 한계도 그만큼이다.')
    if a.out:
        json.dump({'kit': a.kit, 'len_um': a.len_um, 'se_d_um': d_se,
                   'rows': rows, 'verdict': vd}, open(a.out, 'w'), ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')

#!/usr/bin/env python3
"""SDCP **점-스탬프 교란**을 GPU 없이 잰다 — 목표 B 의 조건 ③(기전 분리)를 선점한다.

★ 무엇을 묻나 (CL-25):
  생산 STEP3 는 SDCP 를 **입자당 셀 하나**로 찍는다 (`seed_sdcp` singles = 입자당 점 1개,
  `step3_sigma` 첨가제 경로 = `np.floor` 셀 하나).  그러면 한 입자가 **vox³** 을 차지해
  참부피 π/6·(0.3)³ = 0.014137 µm³ 의 **4.53× (vox 0.4) · 1.91 (0.3) · 1.11 (0.25)** 가 된다.
  ⇒ "격자를 조이면 DBE 이득이 준다" 가 **SDCP 가 홀쭉해져서**일 수 있다 — 그러면 이득의
  기전이 물리(혼합전도 SDCP)가 아니라 **스탬프 인공물**이다.  원고의 헤드라인이 걸린 지점.

★ 어떻게 GPU 없이 되나:
  `step3_sigma.solve_sigma_z` 가 sid 배열을 직접 받는다.  같은 SDCP 중심 좌표를
  **① 참 구(Ø0.30 µm)로 래스터** vs **② 생산 점-스탬프** 두 규약으로 각각 굽고, 나머지
  (AM·SE·격자·origin)를 **완전히 고정**한 채 σ_e 만 비교한다.  차이는 정의상 스탬프 것뿐이다.

★ 이 시험이 실침대와 다른 점 (넘겨짚지 말 것):
  · 침대가 다르다 — 킷 스캐폴드의 AM/SE + **합성 SDCP 배치**다 (실제 seed_sdcp 배치 아님).
  · 그래서 나오는 것은 **기전의 크기와 부호**이지 실침대 보정계수가 아니다.
  · 실침대 값은 여전히 GPU 원장(상별 `count(sid)·vox³` vs 레시피)이 필요하다.

사용:
  python3 scripts/sdcp_stamp_confound.py --vox 0.4 0.3 0.25 0.2 0.15
  python3 scripts/sdcp_stamp_confound.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from step3_sigma import solve_sigma_z                            # noqa: E402
from step3_transport_resolution import (SDCP_D_UM, SID_AM, SID_SDCP, SID_SE,  # noqa: E402
                                        SIGMA_E_AM, SIGMA_E_SDCP,
                                        rasterize_spheres, sdcp_point_cells)


def build(vox, origin, length_um, am, se, sdcp_c, mode, lattice_shift=None):
    """sid 격자.  `mode` = 'sphere'(참 구) | 'point'(생산 점-스탬프) | 'none'.

    ⚠ origin 앙상블은 `origin`(물리 crop 창)이 아니라 `lattice_shift`(격자 위상)로 한다
      — Codex CDX-R2-01.  crop 을 움직이면 팔마다 SDCP/SE 표본이 달라져 위상 효과와
      표본 효과가 섞인다.
    """
    sh = np.zeros(3) if lattice_shift is None else np.asarray(lattice_shift, float)
    sid = rasterize_spheres(vox, origin, length_um, [(se[0], se[1], SID_SE),
                                                     (am[0], am[1], SID_AM)],
                            lattice_shift=sh)
    n = sid.shape[0]
    if mode == 'sphere':
        r = np.full(len(sdcp_c), SDCP_D_UM / 2.0)
        add = rasterize_spheres(vox, origin, length_um, [(sdcp_c, r, SID_SDCP)],
                                lattice_shift=sh)
        sid[add == SID_SDCP] = SID_SDCP
    elif mode == 'point':
        #  격자 위상 이동 = 셀 경계가 −s 만큼 밀린 것과 같다 → floor((p−origin+s)/vox)
        rel = np.asarray(sdcp_c, float) - np.asarray(origin, float) + sh
        m = ((rel >= 0) & (rel < length_um + sh)).all(1)
        ijk = np.floor(rel[m] / vox).astype(int)
        ijk = ijk[((ijk >= 0) & (ijk < n)).all(1)]
        if len(ijk):
            sid[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = SID_SDCP
    return sid


def run(am, se, sdcp_c, base_origin, length_um, voxes, n_origin=8):
    sig = np.zeros(9)
    sig[SID_AM] = SIGMA_E_AM
    sig[SID_SDCP] = SIGMA_E_SDCP                                 # SE·기공 = 전자 절연
    V_true = np.pi / 6.0 * SDCP_D_UM ** 3
    rows = []
    for vox in voxes:
        import itertools as _it
        shifts = [np.array(t) for t in _it.product((0.0, vox / 2.0), repeat=3)][:n_origin]
        res = {}
        for mode in ('none', 'sphere', 'point'):
            vals, vol = [], []
            for sh in shifts:
                sid = build(vox, base_origin, length_um, am, se, sdcp_c, mode,
                            lattice_shift=sh)
                vals.append(float(solve_sigma_z(sid, sig, vox)['sigma_eff']))
                vol.append(float((sid == SID_SDCP).sum()) * vox ** 3)
            res[mode] = (np.array(vals), float(np.mean(vol)))
        rows.append({
            'vox': float(vox),
            'sdcp_d_per_dx': float(f'{SDCP_D_UM / vox:.3f}'),
            'sigma_e_none': float(f'{res["none"][0].mean():.6g}'),
            'sigma_e_sphere': float(f'{res["sphere"][0].mean():.6g}'),
            'sigma_e_point': float(f'{res["point"][0].mean():.6g}'),
            'origin_spread_point_pct': float(
                f'{(res["point"][0].max() / max(res["point"][0].min(), 1e-30) - 1) * 100:.3g}'),
            'vol_sphere_um3': float(f'{res["sphere"][1]:.4g}'),
            'vol_point_um3': float(f'{res["point"][1]:.4g}'),
            'vol_point_over_true': float(f'{res["point"][1] / (len(sdcp_c) * V_true):.3f}'),
            'vol_sphere_over_true': float(f'{res["sphere"][1] / (len(sdcp_c) * V_true):.3f}'),
        })
    for r in rows:
        base = r['sigma_e_none']
        r['gain_sphere_pct'] = float(f'{(r["sigma_e_sphere"] / base - 1) * 100:.4g}') if base > 0 \
            else None
        r['gain_point_pct'] = float(f'{(r["sigma_e_point"] / base - 1) * 100:.4g}') if base > 0 \
            else None
        r['point_over_sphere'] = float(f'{r["sigma_e_point"] / max(r["sigma_e_sphere"], 1e-30):.4g}')
    return rows


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    # ① 점-스탬프 부피 = 입자수 × vox³ (정의) — 그리고 참부피 대비 배수가 산술과 맞다
    c = np.array([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0], [3.0, 3.0, 3.0]])
    V_true = np.pi / 6.0 * SDCP_D_UM ** 3
    for vox, want in ((0.4, 4.53), (0.3, 1.91), (0.25, 1.11)):
        n = int(round(4.0 / vox))
        ijk = sdcp_point_cells(c, vox, (0, 0, 0), 4.0, n)
        got = len(ijk) * vox ** 3 / (len(c) * V_true)
        chk(f'① 점-스탬프 vox {vox}: 참부피의 {got:.2f}배 (산술 {want})', abs(got - want) < 0.02)
    # ② ★ 점-스탬프 부피는 vox 0.24 근처에서 **우연히 정확**해지고 그 아래로는 과소가 된다
    #    (vox³ = π/6·d³ 인 지점).  ⇒ 0.4 → 0.25 스윕은 "수렴" 과 "부피가 정답을 통과하는 것"
    #    이 섞여 있고, 그 아래에서는 **부호가 뒤집힌다** = 판별 검사가 된다.
    xover = SDCP_D_UM * (np.pi / 6.0) ** (1.0 / 3.0)
    chk(f'② 점-스탬프 부피가 정확해지는 vox = {xover:.4f} µm (생산 0.25 바로 옆)',
        abs(xover - 0.2418) < 1e-3)
    for vox, want in ((0.4, 4.53), (0.15, 0.239)):
        got = vox ** 3 / V_true
        chk(f'②b vox {vox} 에서 점/참 = {got:.3f} ({"과대" if got > 1 else "**과소**"})',
            abs(got - want) < 0.01)
    # ③ ★ 서브복셀 구는 래스터에서 **통째로 사라진다** — 그래서 점-스탬프가 쓰인 것이고,
    #    두 규약 다 vox 0.4 에서는 틀린다 (하나는 87 % 소실, 하나는 4.53× 과대).
    gap = 1.0
    g0 = np.arange(0.5, 4.0, gap)
    C = np.stack(np.meshgrid(g0, g0, g0, indexing='ij'), -1).reshape(-1, 3) + 0.137
    R = np.full(len(C), SDCP_D_UM / 2.0)
    lost = {}
    for vox in (0.4, 0.15):
        n = int(round(4.5 / vox)); gg = (np.arange(n) + 0.5) * vox
        lost[vox] = sum(1 for p in C if ((np.array([gg[np.abs(gg - p[k]).argmin()]
                                                    for k in range(3)]) - p) ** 2).sum()
                        > (SDCP_D_UM / 2) ** 2) / len(C)
    chk(f'③ vox 0.4 에서 구 래스터는 입자의 {lost[0.4]:.0%} 를 잃는다 (서브복셀)',
        lost[0.4] > 0.7)
    chk(f'③b vox 0.15 (Ø/dx = 2) 에서는 아무도 안 잃는다 ({lost[0.15]:.0%})', lost[0.15] == 0.0)
    _ = R
    print(f'\nsdcp_stamp_confound selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--kit', default='kit_ps_7_3')
    ap.add_argument('--len-um', type=float, default=12.0)
    ap.add_argument('--vox', type=float, nargs='+', default=[0.4, 0.3, 0.25, 0.2, 0.15])
    ap.add_argument('--sdcp-vol-pct', type=float, default=0.5,
                    help='RVE 부피 대비 SDCP 부피 %% (레시피가 아니라 **통제 변수**)')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--out', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())

    from sr01_realbed_ab import load_kit                          # noqa: E402
    am_c, am_r, se_c, se_r, lat, thick = load_kit(a.kit)
    base = np.array([lat / 2 - a.len_um / 2, lat / 2 - a.len_um / 2, thick / 2 - a.len_um / 2])
    V_true = np.pi / 6.0 * SDCP_D_UM ** 3
    n_sdcp = int(round(a.sdcp_vol_pct / 100.0 * a.len_um ** 3 / V_true))
    rng = np.random.default_rng(a.seed)
    sdcp_c = base + rng.uniform(0, a.len_um, size=(n_sdcp, 3))
    print(f'{a.kit} · RVE {a.len_um} µm³ · SDCP Ø{SDCP_D_UM} µm × {n_sdcp:,} '
          f'({a.sdcp_vol_pct} vol%, 균일 랜덤 배치 = **통제 변수**)')
    print('σ_e: AM 0.010 · SDCP 250 S/cm · SE/기공 전자절연\n')
    rows = run((am_c, am_r), (se_c, se_r), sdcp_c, base, a.len_um, a.vox)
    print(f'{"vox":>6} {"Ø/dx":>6} {"부피 점/참":>10} {"σ_e AM만":>11} {"σ_e +구":>11} '
          f'{"σ_e +점":>11} {"이득 구%":>9} {"이득 점%":>9} {"점/구":>7}')
    for r in rows:
        print(f'{r["vox"]:>6} {r["sdcp_d_per_dx"]:>6.2f} {r["vol_point_over_true"]:>10.2f} '
              f'{r["sigma_e_none"]:>11.5g} {r["sigma_e_sphere"]:>11.5g} '
              f'{r["sigma_e_point"]:>11.5g} {r["gain_sphere_pct"]:>9.2f} '
              f'{r["gain_point_pct"]:>9.2f} {r["point_over_sphere"]:>7.3f}')
    if a.out:
        json.dump({'kit': a.kit, 'len_um': a.len_um, 'n_sdcp': n_sdcp,
                   'sdcp_vol_pct': a.sdcp_vol_pct, 'rows': rows},
                  open(a.out, 'w'), ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')

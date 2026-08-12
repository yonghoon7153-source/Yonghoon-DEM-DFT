#!/usr/bin/env python3
"""SR-01 조치 #7·#8 — 탄소상을 **하나의 망**으로 재고, econn 이 그것에 눈먼 것을 실증한다.

판정 문서 `docs/reviews/sr01_raster_review_verdict_20260812.md` §13 의 #7("가장 값싼 결정타")
과 #8.  GPU 불요, CPU 수 분.

무엇이 기존 A/B 와 다른가 (`sr01_realbed_ab.py` 는 **섬유 하나씩** 잰다):
  · 저기 = "섬유 한 가닥이 몇 조각으로 깨지나" (point_mean_components 3.4 등)
  · 여기 = "탄소 **전체**가 몇 개의 전도체로 갈라지고, 그 중 최대 성분이 질량의 몇 %인가,
            그리고 그것이 **AM 에 꽂혀 있나**"
  ⇒ 앞의 것은 **정도**를 재고, 뒤의 것은 **문턱을 넘었나**를 잰다.  ×35.79 가
    "협착 보정"(정도)인지 "퍼콜 붕괴"(문턱)인지는 **뒤의 것만** 가른다.

왜 이것이 결정타인가:
  점 스탬프에서 탄소가 1–2 셀 섬으로 흩어지고 그 섬들이 AM 에 **닿아 있으면** 죽지 않는다
  (6-face 솔버는 인접 AM 으로 전류를 흘린다).  반대로 닿지 않으면 그 탄소는 **전기적으로
  존재하지 않는다**.  분담 4 %→95 % 는 후자를 시사하지만 시사는 측정이 아니다.

★ 표본 주의: per-fibre 통계는 수백 가닥이면 수렴하지만 **퍼콜레이션은 수렴하지 않는다**.
  네트워크 측정은 `--max-fibres 0`(레시피 전량, 기본)로 해야 한다.

#8 (econn 맹목):  `mpm_webapp_payload.electronic_connectivity` 는 **재료 점**을 받아
  `vox_um`(기본 0.30 µm) 격자에 **26-conn** 으로 라벨한다 — STEP3 래스터를 아예 보지 않는다.
  그 함수 주석 자신이 "vox ≥2× the 0.7·dx point spacing → one continuous fibre labels as
  one cluster" 라고 적고 있다.  ⇒ point/segment 는 **같은 점 구름**이므로 econn 은
  경험적으로가 아니라 **구조적으로** 두 팔에 같은 값을 낸다.  입력에 변수가 없다.

사용:
    python3 scripts/sr01_carbon_network.py --selftest
    python3 scripts/sr01_carbon_network.py --kit kit_ps_7_3           # 전량 (수 분)
    python3 scripts/sr01_carbon_network.py --all-kits --csv docs/data/sr01_carbon_network.csv
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fibre_segment_raster import polyline_cells                     # noqa: E402
from sr01_realbed_ab import seed_carbon_on_kit, point_cells_from    # noqa: E402

KITS = ('kit_ps_0_10', 'kit_ps_3_7', 'kit_ps_5_5', 'kit_ps_7_3', 'kit_ps_10_0')


def _label6(mask, periodic_xy=False):
    """6-face 연결성분 라벨 (솔버와 **같은 인접 규약**).

    ⚠ D4(두-그래프 합의 불변식): 진단 지표는 솔버와 같은 인접 규약·같은 격자에서 재야 한다.
    econn 의 26-conn/0.30 µm 이 6-face/0.4 µm 결함에 눈먼 것이 정확히 이 규율의 위반이었다.
    """
    from scipy import ndimage
    lab, n = ndimage.label(mask, structure=ndimage.generate_binary_structure(3, 1))
    if not periodic_xy:
        return lab, n
    # x/y seam 을 가로질러 이어진 성분을 병합 (z 는 병합하지 않는다)
    par = np.arange(n + 1)
    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]; i = int(par[i])
        return i
    for ax in (0, 1):
        A = np.take(lab, 0, axis=ax); B = np.take(lab, -1, axis=ax)
        m = (A > 0) & (B > 0)
        for u, v in set(zip(A[m].tolist(), B[m].tolist())):
            ru, rv = find(u), find(v)
            if ru != rv:
                par[ru] = rv
    roots = np.array([find(i) for i in range(n + 1)])
    uniq = {r: k + 1 for k, r in enumerate(sorted(set(roots[1:].tolist())))}
    remap = np.zeros(n + 1, np.int64)
    for i in range(1, n + 1):
        remap[i] = uniq[roots[i]]
    return remap[lab], len(uniq)


def _shift(mask, axis, sh, periodic):
    """축별 이웃 이동.  주기축은 wrap, **비주기축은 zero-padding**.

    ★ 왜 (2026-08-12, Codex intentional error #5 — 내 코드다):
      첫 판은 `np.roll` 하나로 xyz 를 **전부 toroidal 로** 감았다.  그런데 성분 라벨은
      `ndimage.label` = **비주기 6-face** 였다 ⇒ **같은 그림 위에서 두 규약을 섞었다**.
      z 는 어떤 경우에도 감으면 안 된다 (솔버가 위·아래 플레이트로 막는 축).
    """
    out = np.roll(mask, sh, axis=axis)
    if not periodic:                       # zero-padding: 넘어온 면을 지운다
        sl = [slice(None)] * mask.ndim
        sl[axis] = slice(0, sh) if sh > 0 else slice(mask.shape[axis] + sh, None)
        out = out.copy()
        out[tuple(sl)] = False
    return out


def carbon_network_stats(cells, shape, am_mask=None, periodic_xy=False,
                         plate_bot=None, plate_top=None):
    """탄소 셀 집합 → 전역 망 통계.

    cells    : (N,3) int 복셀 좌표 (중복 허용 — 내부에서 unique)
    shape    : 격자 크기 (nx,ny,nz)
    am_mask  : 같은 격자의 AM 점유 (bool) 또는 None

    반환 키 중 **판정용 두 개**:
      largest_mass_frac  — 최대 성분이 탄소 질량의 몇 분율 (망이 있나)
      plugged_frac       — AM 에 면-인접한 성분에 속한 탄소 분율 (전기적으로 살아 있나)
    ⚠ am_mask=None 이면 plugged_* 는 **None** — 0 으로 눕히지 않는다 (§F1).
    """
    g = np.zeros(shape, bool)
    if len(cells):
        c = np.asarray(cells, np.int64)
        keep = np.all((c >= 0) & (c < np.asarray(shape)), axis=1)
        c = c[keep]
        g[c[:, 0], c[:, 1], c[:, 2]] = True
    n_cells = int(g.sum())
    out = {'n_cells': n_cells, 'n_components': 0, 'largest_cells': 0,
           'largest_mass_frac': None, 'singleton_frac': None, 'spans_z': None,
           'span_mass_frac': None, 'plugged_frac': None, 'plugged_components_frac': None}
    if n_cells == 0:
        return out
    lab, ncomp = _label6(g, periodic_xy=periodic_xy)   # AM-touch 판정과 **같은** periodicity
    sizes = np.bincount(lab.ravel())[1:]                    # 성분별 셀 수 (0 = 배경)
    out['n_components'] = int(ncomp)
    out['largest_cells'] = int(sizes.max())
    out['largest_mass_frac'] = float(sizes.max() / n_cells)
    out['singleton_frac'] = float((sizes == 1).sum() * 1.0 / n_cells)   # 고립 1셀 섬의 질량몫
    # z 를 관통하는 성분 (STEP3 는 두께 방향으로 전위차를 건다).
    # ★ z 범위는 **격자에 실제로 남은** 탄소에서 뽑는다 — 입력 좌표에서 뽑으면 격자 밖으로
    #   버려진 셀이 인덱스를 넘겨 터진다 (selftest '격자 밖 셀은 무시' 가 잡았다).
    # ★ 솔버의 실제 plate 를 쓴다.  첫 판은 **탄소 점유 범위**의 양 끝을 썼는데, 그러면
    #   탄소가 어디에 있든 "관통" 이 되기 쉬워 판별력이 거의 없다 (Codex #5).
    if plate_bot is None or plate_top is None:
        zc = np.nonzero(g.any(axis=(0, 1)))[0]
        z0, z1 = int(zc.min()), int(zc.max())
        out['spans_z_basis'] = 'carbon_envelope (LEGACY — 판별력 낮음)'
    else:
        z0, z1 = int(plate_bot), int(plate_top)
        out['spans_z_basis'] = f'solver_plates z={z0}..{z1}'
    z0 = max(0, min(z0, g.shape[2] - 1)); z1 = max(0, min(z1, g.shape[2] - 1))
    top = set(np.unique(lab[:, :, z1][lab[:, :, z1] > 0]).tolist())
    bot = set(np.unique(lab[:, :, z0][lab[:, :, z0] > 0]).tolist())
    spanning = sorted(top & bot)
    out['spans_z'] = bool(spanning)
    out['span_mass_frac'] = float(sum(sizes[i - 1] for i in spanning) / n_cells)
    if am_mask is not None:
        # 성분이 AM 에 **면-인접**하면 그 성분 전체가 전류를 흘릴 수 있다 (6-face 솔버)
        touch = np.zeros(ncomp + 1, bool)
        for ax in range(3):
            per = bool(periodic_xy) and ax in (0, 1)     # z 는 절대 wrap 하지 않는다
            for sh in (1, -1):
                nb = _shift(am_mask, ax, sh, per)
                touch[np.unique(lab[g & nb])] = True
        touch[0] = False
        out['plugged_frac'] = float(sizes[touch[1:]].sum() / n_cells)
        out['plugged_components_frac'] = float(touch[1:].sum() / max(ncomp, 1))
    return out


def _am_voxel_mask(am_c, am_r, lo, vox, shape):
    """AM 구를 같은 복셀 격자에 굽는다 (STEP3 rasterize 와 같은 floor 규약)."""
    m = np.zeros(shape, bool)
    sh = np.asarray(shape)
    for c0, r0 in zip(np.asarray(am_c, float), np.asarray(am_r, float)):
        i0 = np.maximum(np.floor((c0 - r0 - lo) / vox).astype(np.int64), 0)
        i1 = np.minimum(np.floor((c0 + r0 - lo) / vox).astype(np.int64) + 1, sh - 1)
        if np.any(i1 < i0):
            continue
        gx = (np.arange(i0[0], i1[0] + 1) + 0.5) * vox + lo[0] - c0[0]
        gy = (np.arange(i0[1], i1[1] + 1) + 0.5) * vox + lo[1] - c0[1]
        gz = (np.arange(i0[2], i1[2] + 1) + 0.5) * vox + lo[2] - c0[2]
        d2 = gx[:, None, None] ** 2 + gy[None, :, None] ** 2 + gz[None, None, :] ** 2
        m[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1] |= (d2 < r0 * r0)
    return m


def run(kit='kit_ps_7_3', n_grid=288, vox=0.4, vgcf_wt=1.0, seed=0, max_fibres=0,
        gap_tol=2.0, with_am=True, verbose=True, periodic_xy=False, legacy=False):
    S = seed_carbon_on_kit(kit, n_grid, vgcf_wt, seed, max_fibres=max_fibres)
    pts, fid, step = S['pts'], S['fid'], S['step']
    lat, thick = S['lat'], S['thick']
    if verbose:
        print(f"  [{kit}] {S['nobj']}/{S['nobj_full']} fibres, {len(pts):,} pts, "
              f"vox={vox} µm, step={step:.4f} µm")

    lo = np.array([0.0, 0.0, 0.0])
    shape = (int(np.ceil(lat / vox)) + 2, int(np.ceil(lat / vox)) + 2,
             int(np.ceil(thick / vox)) + 2)
    pt_all, sg_all = [], []
    for f in np.unique(fid):
        P = pts[fid == f]
        if len(P) < 2:
            continue
        d = np.linalg.norm(np.diff(P, axis=0), axis=1)
        brk = np.nonzero(d > gap_tol * step)[0] + 1          # AM 이 끊은 자리 = 물리적 단절
        runs = np.split(P, brk) if len(brk) else [P]
        pt_all.append(point_cells_from(P, vox))
        sg_all.append(np.vstack([polyline_cells(R, vox) for R in runs if len(R) >= 1]))
    pt_c = np.unique(np.vstack(pt_all), axis=0) if pt_all else np.zeros((0, 3), np.int64)
    sg_c = np.unique(np.vstack(sg_all), axis=0) if sg_all else np.zeros((0, 3), np.int64)

    am_mask = None
    if with_am:
        if verbose:
            print(f"  [{kit}] AM {len(S['am_r']):,} 구를 복셀로 …")
        am_mask = _am_voxel_mask(S['am_c'], S['am_r'], lo, vox, shape)

    # ★ 경계 규약을 **타깃 STEP3 실행과 통일**한다 (2026-08-12, Codex #5).
    #   생산 STEP3 기본은 비주기(`MPM_PERIODIC_SIGMA` 미설정) → periodic_xy=False.
    #   z 는 어떤 경우에도 wrap 하지 않는다 — 솔버가 위·아래 플레이트로 막는 축이다.
    #   plate 는 솔버 규약(z_bot=0, z_top=thickness, band=vox)의 셀 인덱스.
    pb, pt_ = (None, None) if legacy else (0, int(round(thick / vox)) - 1)
    kw = {} if legacy else dict(periodic_xy=periodic_xy, plate_bot=pb, plate_top=pt_)
    A = carbon_network_stats(pt_c, shape, am_mask, **kw)     # arm A = 점 스탬프 (현 기본값)
    B = carbon_network_stats(sg_c, shape, am_mask, **kw)     # arm B = 선분 스탬프
    r = {'kit': kit, 'n_grid': n_grid, 'vox_um': vox, 'vgcf_wt_pct': vgcf_wt,
         'boundary': 'LEGACY_xyz_toroidal' if legacy else
                     f'corrected(periodic_xy={periodic_xy}, z=zero-pad, plates={pb}..{pt_})',
         'n_fibres': S['nobj'], 'n_fibres_recipe': S['nobj_full'], 'n_points': int(len(pts)),
         'am_voxels': int(am_mask.sum()) if am_mask is not None else None}
    for tag, d in (('point', A), ('segment', B)):
        for k, v in d.items():
            r[f'{tag}_{k}'] = round(v, 6) if isinstance(v, float) else v
    return r


def econn_blindness():
    """#8 — econn 이 스탬프 규약에 **구조적으로** 눈멀었음을 코드에서 증명한다.

    경험적 "두 팔에 같은 값" 보다 강하다: econn 의 입력에 스탬프 변수가 **없다**.
    """
    import inspect
    from mpm_webapp_payload import electronic_connectivity as ec
    sig = inspect.signature(ec)
    params = set(sig.parameters)
    src = inspect.getsource(ec)

    def _names(code, seen=()):
        """실제로 **참조하는 이름**만 모은다 (중첩 함수 포함).
        ⚠ 소스 문자열 검색은 안 된다 — econn docstring 이 'STEP3 Kirchhoff' 를 **설명으로**
          언급해서 첫 판(문자열 매칭)이 오탐했다.  코드 객체가 정본이다."""
        out = set(code.co_names)
        for k in code.co_consts:
            if hasattr(k, 'co_names') and k not in seen:
                out |= _names(k, seen + (k,))
        return out
    used = _names(ec.__code__)
    return {
        'params': sorted(params),
        'takes_stamp_arg': bool({'fibre_stamp', 'stamp', 'add_kind', 'segment'} & params),
        'uses_step3_raster': bool({'rasterize', 'step3_sigma', '_s3'} & used),
        'connectivity': '26-conn' if 'np.ones((3, 3, 3)' in src else 'unknown',
        'input': 'material points (se/phase), NOT the STEP3 voxel raster',
        'verdict': 'STRUCTURALLY BLIND — the stamp convention is not in econn\'s input, so '
                   'arm A and arm B are bit-identical to it by construction, not by measurement.',
    }


def _fmt(r):
    L = [f"── {r['kit']}  (vox {r['vox_um']} µm, {r['n_fibres']:,}/{r['n_fibres_recipe']:,} fibres, "
         f"{r['n_points']:,} pts)"]
    L.append(f"{'':22s} {'point(A)':>14s} {'segment(B)':>14s}")
    rows = [('탄소 셀 수', 'n_cells', '{:,}'), ('연결성분 수', 'n_components', '{:,}'),
            ('최대 성분 (셀)', 'largest_cells', '{:,}'),
            ('★ 최대 성분 질량몫', 'largest_mass_frac', '{:.4f}'),
            ('1셀 고립 섬 질량몫', 'singleton_frac', '{:.4f}'),
            ('z 관통 성분 질량몫', 'span_mass_frac', '{:.4f}'),
            ('★ AM 에 꽂힌 질량몫', 'plugged_frac', '{:.4f}'),
            ('  꽂힌 성분 비율', 'plugged_components_frac', '{:.4f}')]
    for name, key, fm in rows:
        a, b = r.get(f'point_{key}'), r.get(f'segment_{key}')
        fa = fm.format(a) if a is not None else '—'
        fb = fm.format(b) if b is not None else '—'
        L.append(f"{name:22s} {fa:>14s} {fb:>14s}")
    return '\n'.join(L)


def _selftest():
    ok = 0
    fail = []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
            print(f'  PASS  {name}')
        else:
            fail.append(name)
            print(f'  FAIL  {name}')

    sh = (10, 10, 10)
    # 1) 축정렬이 아닌 **대각선** 점열 — 점 스탬프가 실제로 깨지는 유일한 배치 (D2)
    diag = np.array([[i, i, i] for i in range(8)], np.int64)
    s = carbon_network_stats(diag, sh)
    chk('대각선 8점 = 8 성분 (6-face 로는 모서리 접촉이 안 이어진다)', s['n_components'] == 8)
    chk('대각선: 최대 성분 질량몫 = 1/8', abs(s['largest_mass_frac'] - 0.125) < 1e-9)
    chk('대각선: 전부 1셀 섬', abs(s['singleton_frac'] - 1.0) < 1e-9)
    # 2) 같은 대각선을 **이으면** 한 성분 = 이 측정이 스탬프 차이를 실제로 본다 (판별력 > 0)
    fill = np.array([[i, i, k] for i in range(8) for k in (i,)] +
                    [[i + 1, i, i] for i in range(7)] + [[i + 1, i + 1, i] for i in range(7)],
                    np.int64)
    s2 = carbon_network_stats(fill, sh)
    chk('★ 이으면 1 성분 — 지표가 스탬프 차이를 본다 (가능도비 ≫ 1)', s2['n_components'] == 1)
    # 3) z 관통 판정
    col = np.array([[5, 5, k] for k in range(10)], np.int64)
    chk('z 기둥은 관통', carbon_network_stats(col, sh)['spans_z'] is True)
    half = np.array([[5, 5, k] for k in range(5)], np.int64)
    s3 = carbon_network_stats(half, sh)
    chk('반쪽 기둥도 자기 z-범위 안에서는 관통 (범위는 탄소 범위로 잡는다)',
        s3['spans_z'] is True and abs(s3['span_mass_frac'] - 1.0) < 1e-9)
    # 4) AM 인접 — 꽂힌 것과 뜬 것을 가른다
    am = np.zeros(sh, bool); am[5, 5, 5] = True
    cc = np.array([[5, 5, 4], [1, 1, 1]], np.int64)          # 하나는 AM 에 면-인접, 하나는 멀리
    s4 = carbon_network_stats(cc, sh, am)
    chk('AM 에 면-인접한 셀만 plugged (0.5)', abs(s4['plugged_frac'] - 0.5) < 1e-9)
    am2 = np.zeros(sh, bool); am2[5, 6, 5] = True            # 모서리도 면도 아닌 대각 이웃
    s5 = carbon_network_stats(np.array([[5, 5, 4]], np.int64), sh, am2)
    chk('대각 이웃은 plugged 아님 (6-face 규약 준수)', abs(s5['plugged_frac'] - 0.0) < 1e-12)
    # 5) §F1 — AM 이 없으면 plugged 는 0 이 아니라 None
    chk('am_mask 없으면 plugged_frac = None (0 으로 눕히지 않는다)',
        carbon_network_stats(col, sh)['plugged_frac'] is None)
    chk('탄소 0 개면 전부 기본값 + n_cells 0', carbon_network_stats(
        np.zeros((0, 3), np.int64), sh)['n_cells'] == 0)
    # 6) 격자 밖 좌표는 조용히 버린다 (경계에서 IndexError 로 죽지 않게)
    chk('격자 밖 셀은 무시', carbon_network_stats(
        np.array([[99, 99, 99], [1, 1, 1]], np.int64), sh)['n_cells'] == 1)
    # 7) ★ 경계 규약 (Codex #5) — 같은 그림에서 두 규약을 섞지 않는다
    sh2 = (6, 6, 6)
    am_e = np.zeros(sh2, bool); am_e[0, 2, 2] = True          # x=0 벽
    c_e = np.array([[5, 2, 2]], np.int64)                     # x=nx-1 — seam 건너 인접
    chk('#5: 비주기면 seam 건너 AM 은 plugged 아님 (zero-pad)',
        carbon_network_stats(c_e, sh2, am_e, periodic_xy=False)['plugged_frac'] == 0.0)
    chk('#5: periodic_xy 면 seam 건너 AM 이 plugged',
        carbon_network_stats(c_e, sh2, am_e, periodic_xy=True)['plugged_frac'] == 1.0)
    am_z = np.zeros(sh2, bool); am_z[2, 2, 0] = True
    c_z = np.array([[2, 2, 5]], np.int64)
    chk('#5: ★z 는 periodic_xy 라도 절대 wrap 하지 않는다',
        carbon_network_stats(c_z, sh2, am_z, periodic_xy=True)['plugged_frac'] == 0.0)
    two = np.array([[0, 2, 2], [5, 2, 2]], np.int64)
    chk('#5: 라벨도 같은 periodicity — 비주기 2성분 / 주기 1성분',
        carbon_network_stats(two, sh2)['n_components'] == 2
        and carbon_network_stats(two, sh2, periodic_xy=True)['n_components'] == 1)
    col = np.array([[2, 2, k] for k in range(1, 5)], np.int64)
    chk('#5: spans_z 가 solver plate 기준이면 짧은 기둥은 관통 아님',
        carbon_network_stats(col, sh2, plate_bot=0, plate_top=5)['spans_z'] is False)
    chk('#5: legacy(carbon envelope) 는 같은 기둥을 관통으로 본다 = 판별력 낮음',
        carbon_network_stats(col, sh2)['spans_z'] is True)

    # 8) #8 econn 구조적 맹목
    try:
        eb = econn_blindness()
        chk('econn 은 스탬프 인자를 받지 않는다 (구조적 맹목)', not eb['takes_stamp_arg'])
        chk('econn 은 STEP3 래스터를 부르지 않는다', not eb['uses_step3_raster'])
        chk('econn 은 26-conn (솔버의 6-face 와 다른 규약 = D4 위반)',
            eb['connectivity'] == '26-conn')
    except Exception as e:                                   # scipy/의존성 없는 환경
        print(f'  SKIP  econn 내성검사 ({e})')

    print(f'\nsr01_carbon_network selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--kit', default='kit_ps_7_3')
    ap.add_argument('--all-kits', action='store_true')
    ap.add_argument('--n-grid', type=int, default=288)
    ap.add_argument('--vox', type=float, default=0.4)
    ap.add_argument('--vgcf-wt', type=float, default=1.0)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--max-fibres', type=int, default=0,
                    help='0 = 레시피 전량 (기본).  ⚠ 표본을 줄이면 per-fibre 통계는 살아도 '
                         '**퍼콜레이션은 무의미**해진다 — 네트워크 측정은 전량으로.')
    ap.add_argument('--periodic-xy', action='store_true',
                    help='타깃 STEP3 가 --periodic 일 때만.  z 는 어떤 경우에도 wrap 안 함')
    ap.add_argument('--legacy', action='store_true',
                    help='⚠ 옛 혼합 규약 재현 전용 (xyz toroidal + carbon-envelope spans_z). '
                         '기전 증거로 쓰지 말 것 — 보존용.')
    ap.add_argument('--no-am', action='store_true', help='AM 복셀화 생략 (plugged_* 는 null)')
    ap.add_argument('--csv', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())

    print(econn_blindness()['verdict'] + '\n')
    rows = []
    for kit in (KITS if a.all_kits else [a.kit]):
        r = run(kit, a.n_grid, a.vox, a.vgcf_wt, a.seed, a.max_fibres, with_am=not a.no_am,
                periodic_xy=a.periodic_xy, legacy=a.legacy)
        rows.append(r)
        print(_fmt(r) + '\n')
    if a.csv and rows:
        import csv as _csv
        os.makedirs(os.path.dirname(a.csv) or '.', exist_ok=True)
        with open(a.csv, 'w', newline='') as fh:
            w = _csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f'  → {a.csv}  ({len(rows)} rows)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

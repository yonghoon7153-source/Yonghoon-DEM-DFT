#!/usr/bin/env python3
"""2D SE-voxel 초미세확대 뷰 — payload/grid의 SE가 '복셀로 어떻게 존재하는지'를 2D 슬라이스로.

사용자 질문("payload로 먹여준 걸 초미세확대해서 SE가 어떻게 voxel로 존재하는지 2D로"): STEP3가 SE를
0.4µm 복셀로 래스터화한 **실제 sid 격자**(step4_grid.npz의 sid, 또는 스캐폴드에서 즉석 rasterize)를 받아
지정한 얇은 슬라이스를 **초확대**해 상별 색으로 보여준다.  개별 복셀이 사각형으로 보이게 격자선(--gridlines) —
SE 복셀 채움·계단화(staircase, 매끈한 구가 축-정렬 복셀로 계단이 되는 것)를 눈으로 확인하는 진단 뷰.

색: pore=흰 · AM=회 · carbon(VGCF/SuperP/SDCP/SWCNT)=검 · SE=파랑 · PTFE=주황.

sid 규약(step3_sigma): 0=pore,1=AM_S,2=AM_P,3=VGCF,4=SuperP,5=SDCP,6=SE,7=PTFE,8=SWCNT.

사용:
  python3 scripts/viz_se_voxel_2d.py --grid step4_grid.npz --slice z --at 36 --center 10,10 --win 12 --out se_vox
  python3 scripts/viz_se_voxel_2d.py --am-scaffold am_scaffold.csv --se-dump se_scaffold.csv --vox 0.4 --slice y --at 25 --out se_vox
  python3 scripts/viz_se_voxel_2d.py --selftest
"""
import argparse
import sys

import numpy as np

# 상별 색 (categorical) — sid → RGB
_PHASE_COLOR = {
    0: (1.00, 1.00, 1.00),   # pore  흰
    1: (0.62, 0.65, 0.70),   # AM_S  회
    2: (0.52, 0.55, 0.62),   # AM_P  진회
    3: (0.10, 0.10, 0.10),   # VGCF  검
    4: (0.20, 0.20, 0.20),   # SuperP
    5: (0.30, 0.30, 0.30),   # SDCP
    6: (0.15, 0.39, 0.92),   # SE    파랑 ★
    7: (0.90, 0.49, 0.13),   # PTFE  주황
    8: (0.05, 0.05, 0.05),   # SWCNT
}
_PHASE_NAME = {0: 'pore', 1: 'AM_S', 2: 'AM_P', 3: 'VGCF', 4: 'SuperP', 5: 'SDCP', 6: 'SE', 7: 'PTFE', 8: 'SWCNT'}


def load_sid_from_grid(path):
    """step4_grid.npz (payload STEP4 export) → sid 격자 + vox(µm).  vox 없으면 0.4 가정(라벨)."""
    d = np.load(path, allow_pickle=True)
    sid = np.asarray(d['sid']).astype(int)
    vox = float(d['vox_um']) if 'vox_um' in d else (float(d['vox']) if 'vox' in d else 0.4)
    return sid, vox


def rasterize_from_scaffold(am_csv, se_csv, vox, tol_am_um=0.10):
    """스캐폴드(AM+SE centre/r) → sid 격자 (step3_sigma.rasterize 규약, SE=6·AM=1/2).  즉석 확인용."""
    import step3_sigma as s3

    def _load(path):
        rows = []
        with open(path) as f:
            for ln in f:
                ln = ln.strip()
                if not ln or ln.startswith('#'):
                    continue
                p = ln.split(',')
                rows.append([float(x) for x in p[:5]])
        a = np.array(rows)
        return a  # [type,x,y,z,r] (스캐폴드는 mm — ×1000 µm 변환)

    am = _load(am_csv)
    se = _load(se_csv)
    _sc = 1000.0 if np.median(am[:, 4]) < 0.05 else 1.0     # mm→µm 자동
    am_c = am[:, 1:4] * _sc
    am_r = am[:, 4] * _sc
    se_c = se[:, 1:4] * _sc
    lo = np.minimum(am_c.min(0), se_c.min(0))
    hi = np.maximum(am_c.max(0), se_c.max(0))
    am_c -= lo
    se_c -= lo
    box_hi = tuple((hi - lo))
    # AM type: r 기준 poly/SC (2µm=SC/AM_S, 6µm=poly/AM_P — step3 SID 1=AM_S,2=AM_P)
    am_t = np.where(am_r >= 3.5, 2, 1)
    sid, _pid = s3.rasterize(am_c, am_r, am_t, None, None, (0.0, 0.0, 0.0), box_hi, vox, se_pts=se_c)
    return sid, vox


def slice2d(sid, axis, at_um, vox):
    """3D sid → 2D 슬라이스.  axis 'z'=x-y평면(z고정), 'y'=x-z평면(y고정), 'x'=y-z평면.  at_um=슬라이스 위치."""
    k = int(round(at_um / vox))
    if axis == 'z':
        k = min(max(k, 0), sid.shape[2] - 1)
        return sid[:, :, k], ('x', 'y')
    if axis == 'y':
        k = min(max(k, 0), sid.shape[1] - 1)
        return sid[:, k, :], ('x', 'z')
    k = min(max(k, 0), sid.shape[0] - 1)
    return sid[k, :, :], ('y', 'z')


def crop(sl, vox, center=None, win=None):
    """중심(µm)·창(µm) 크롭.  center None이면 전체.  반환 (crop, extent_um)."""
    ny, nx = sl.shape        # sl[i,j] — i=첫축, j=둘째축
    if center is None or win is None:
        return sl, (0, nx * vox, 0, ny * vox)
    cx, cy = center
    h = win / 2.0
    i0 = max(0, int((cx - h) / vox)); i1 = min(ny, int((cx + h) / vox) + 1)
    j0 = max(0, int((cy - h) / vox)); j1 = min(nx, int((cy + h) / vox) + 1)
    if i1 <= i0 or j1 <= j0:
        return sl, (0, nx * vox, 0, ny * vox)
    return sl[i0:i1, j0:j1], (j0 * vox, j1 * vox, i0 * vox, i1 * vox)


def render(sl, extent, axnames, vox, out_png, gridlines=True, title=''):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.colors import ListedColormap
        from matplotlib.patches import Patch
    except ImportError:
        print('  matplotlib 없음 — 상별 복셀 카운트만:')
        u, c = np.unique(sl, return_counts=True)
        for s, n in zip(u, c):
            print(f'    {_PHASE_NAME.get(int(s), s)}: {n} vox ({100.0*n/sl.size:.1f}%)')
        return
    smax = max(_PHASE_COLOR)
    cmap = ListedColormap([_PHASE_COLOR[i] for i in range(smax + 1)])
    fig, ax = plt.subplots(figsize=(7.5, 7.0))
    ax.imshow(sl, cmap=cmap, vmin=0, vmax=smax, origin='lower', extent=extent, interpolation='nearest')
    npix = sl.size
    if gridlines and npix <= 6000:                         # 초확대일 때만 복셀 격자선 (개별 복셀 사각형)
        for x in np.arange(extent[0], extent[1] + 1e-9, vox):
            ax.axvline(x, color='#00000018', lw=0.4)
        for y in np.arange(extent[2], extent[3] + 1e-9, vox):
            ax.axhline(y, color='#00000018', lw=0.4)
    ax.set_xlabel(f'{axnames[0]} (µm)')
    ax.set_ylabel(f'{axnames[1]} (µm)')
    present = sorted(set(int(s) for s in np.unique(sl)))
    ax.legend(handles=[Patch(facecolor=_PHASE_COLOR[s], edgecolor='#888', label=_PHASE_NAME.get(s, str(s)))
                       for s in present], loc='upper right', fontsize=8, framealpha=0.9)
    ax.set_title(title or f'SE voxel 2D (vox={vox}µm, {sl.shape[1]}×{sl.shape[0]} vox)', fontsize=11, fontweight='bold')
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches='tight')
    print(f'  saved -> {out_png}  ({sl.shape[1]}×{sl.shape[0]} vox, SE {100.0*(sl==6).sum()/sl.size:.1f}%)')


def _selftest():
    ok = tot = 0

    def chk(n, c):
        nonlocal ok, tot
        tot += 1
        ok += 1 if c else 0
        print(f"  {'✓' if c else '✗ FAIL'} {n}")

    # 합성 sid: AM 구 + SE 채움
    n = 40
    sid = np.zeros((n, n, n), int)
    zz, yy, xx = np.mgrid[0:n, 0:n, 0:n]
    sid[(xx - 20) ** 2 + (yy - 20) ** 2 + (zz - 20) ** 2 < 64] = 1   # AM 구 (r=8)
    sid[sid == 0] = 6                                                # 나머지 SE
    sl, axn = slice2d(sid, 'z', 8.0, 0.4)                            # z=20 근처 (0.4µm vox → k=20)
    chk('slice2d z → 2D', sl.ndim == 2 and sl.shape == (n, n))
    chk('슬라이스에 AM(1)·SE(6) 둘 다', (sl == 1).any() and (sl == 6).any())
    cr, ext = crop(sl, 0.4, center=(8.0, 8.0), win=6.0)
    chk('crop 축소', cr.size < sl.size and cr.ndim == 2)
    chk('extent 4-tuple µm', len(ext) == 4 and ext[1] > ext[0])
    slx, axnx = slice2d(sid, 'y', 8.0, 0.4)
    chk("slice 'y' = x-z 평면", axnx == ('x', 'z'))
    # 경계 clamp (at 범위 밖)
    slc, _ = slice2d(sid, 'z', 999.0, 0.4)
    chk('at 범위밖 clamp (죽지 않음)', slc.shape == (n, n))
    import os
    import tempfile
    tf = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    tf.close()
    render(cr, ext, axn, 0.4, tf.name, gridlines=True, title='selftest')
    chk('render PNG 생성', os.path.getsize(tf.name) > 0)
    os.unlink(tf.name)
    print(f'  viz_se_voxel_2d selftest: {ok}/{tot} PASS')
    return ok == tot


def main(argv):
    ap = argparse.ArgumentParser(description='2D SE-voxel 초미세확대 뷰')
    ap.add_argument('--grid', help='step4_grid.npz (sid 격자)')
    ap.add_argument('--am-scaffold', help='AM 스캐폴드 csv (--se-dump와 함께, 즉석 rasterize)')
    ap.add_argument('--se-dump', help='SE 스캐폴드 csv')
    ap.add_argument('--vox', type=float, default=0.4, help='복셀 크기 µm (스캐폴드 rasterize용)')
    ap.add_argument('--slice', default='z', choices=['x', 'y', 'z'], help="슬라이스 축 (z=x-y평면, y=x-z, x=y-z)")
    ap.add_argument('--at', type=float, default=None, help='슬라이스 위치 µm (기본 중앙)')
    ap.add_argument('--center', help='크롭 중심 "a,b" µm (초확대)')
    ap.add_argument('--win', type=float, default=None, help='크롭 창 크기 µm (예 12 = 12µm×12µm)')
    ap.add_argument('--no-gridlines', action='store_true', help='복셀 격자선 끄기')
    ap.add_argument('--out', default='se_voxel_2d', help='PNG prefix')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.grid:
        sid, vox = load_sid_from_grid(a.grid)
    elif a.am_scaffold and a.se_dump:
        sys.path.insert(0, __file__.rsplit('/', 1)[0])
        sid, vox = rasterize_from_scaffold(a.am_scaffold, a.se_dump, a.vox)
    else:
        ap.error('--grid 또는 (--am-scaffold + --se-dump) 필요 (또는 --selftest)')
    at = a.at if a.at is not None else (sid.shape[{'x': 0, 'y': 1, 'z': 2}[a.slice]] * vox / 2.0)
    sl, axn = slice2d(sid, a.slice, at, vox)
    center = tuple(float(x) for x in a.center.split(',')) if a.center else None
    cr, ext = crop(sl, vox, center=center, win=a.win)
    render(cr, ext, axn, vox, a.out + '.png', gridlines=not a.no_gridlines,
           title=f'SE voxel 2D — {a.slice}-slice @{at:.1f}µm (vox {vox}µm)')


if __name__ == '__main__':
    main(sys.argv[1:])

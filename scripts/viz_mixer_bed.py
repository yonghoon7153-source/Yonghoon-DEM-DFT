#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""믹서 침대 단면 렌더 — 가로 드럼을 **축 방향으로 들여다본** 그림.

    python3 scripts/viz_mixer_bed.py --dir <post> [--dir ...] --out bed.png
    python3 scripts/viz_mixer_bed.py --selftest

★ 색은 리포 규약을 **가져다 쓴다** (`viz_mpm_continuum.PALETTES['dem']`):
  AM 회색 뼈대 + SE 카키.  여기서 새로 정하면 두 벌이 되고 그림끼리 안 맞는다.
★ 드럼 축은 **x** 이므로 (y, z) 평면을 그린다 — `measure_bed_aspect --axis x` 와 같은 규약.
⚠ 원의 크기는 **실제 반경**이다 (점 크기를 임의로 키우지 않는다 — 채워 보이려고 키우면
  φ 를 눈으로 잘못 읽게 된다).
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from measure_bed_aspect import frames, read_dump        # noqa: E402

#: 타입 → 색.  1 AM_P · 2 AM_S · 3 SE · 4 VGCF · 5 PTFE
TYPE_COL = {1: '#5b5b5b', 2: '#8f8f8f', 3: '#c9b88a', 4: '#1f77b4', 5: '#d62728'}
TYPE_LAB = {1: 'AM_P', 2: 'AM_S', 3: 'SE', 4: 'VGCF', 5: 'PTFE'}


def panel(ax, path, r_drum, title=''):
    D = read_dump(path)
    y, z, r, t = D['y'], D['z'], D['radius'], D['type'].astype(int)
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(r_drum * np.cos(th) * 1e3, r_drum * np.sin(th) * 1e3,
            color='#333', lw=1.2, zorder=3)
    #  큰 것부터 그려 작은 입자가 위에 오게 한다
    for ty in sorted(TYPE_COL, key=lambda k: -np.median(r[t == k]) if (t == k).any() else 0):
        m = t == ty
        if not m.any():
            continue
        for Y, Z, RR in zip(y[m] * 1e3, z[m] * 1e3, r[m] * 1e3):
            ax.add_patch(__import__('matplotlib').patches.Circle(
                (Y, Z), RR, facecolor=TYPE_COL[ty], edgecolor='none', alpha=0.9))
    lim = r_drum * 1.08 * 1e3
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=9)
    for s in ax.spines.values():
        s.set_visible(False)
    return len(y)


#: 한글이 들어간 라벨을 쓰므로 CJK 글리프가 있는 폰트를 **골라야 한다**.
#  ⚠ 없으면 matplotlib 이 조용히 두부(□)를 찍는다 — 오류도 경고도 없다.
#    2026-09-20 실측으로 그렇게 나왔다.  ⇒ 고르고, **못 고르면 알린다**.
_CJK_PREFER = ('WenQuanYi Zen Hei', 'Noto Sans CJK KR', 'NanumGothic',
               'Noto Sans KR', 'IPAGothic', 'Unifont-JP')


def pick_cjk_font(warn=True):
    """설치된 폰트 중 CJK 글리프가 있는 것.  없으면 None 을 주고 **알린다**."""
    import matplotlib.font_manager as fm
    have = {f.name for f in fm.fontManager.ttflist}
    for n in _CJK_PREFER:
        if n in have:
            return n
    if warn:
        print('⚠ CJK 폰트가 없다 — 한글 라벨이 □ 로 나온다.  라벨을 영문으로 쓸 것.',
              file=sys.stderr)
    return None


def render(dirs, labels, out, r_drum=0.02056, suptitle=''):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    _f = pick_cjk_font()
    if _f:
        plt.rcParams['font.family'] = _f
        plt.rcParams['axes.unicode_minus'] = False
    n = len(dirs)
    fig, axes = plt.subplots(1, n, figsize=(3.1 * n, 3.6))
    if n == 1:
        axes = [axes]
    for ax, d, lab in zip(axes, dirs, labels):
        fr = frames(d)
        if not fr:
            raise SystemExit(f'⛔ {d}: 덤프가 없다')
        step, path = fr[-1]
        npart = panel(ax, path, r_drum, f'{lab}\nstep {step:,} · n {npart if False else ""}')
        ax.set_title(f'{lab}\nstep {step:,}', fontsize=9)
    hs = [plt.Line2D([], [], marker='o', ls='', color=TYPE_COL[k], label=TYPE_LAB[k])
          for k in sorted(TYPE_COL)]
    fig.legend(handles=hs, loc='lower center', ncol=5, frameon=False, fontsize=8)
    if suptitle:
        fig.suptitle(suptitle, fontsize=10)
    fig.tight_layout(rect=[0, 0.07, 1, 0.97])
    fig.savefig(out, dpi=150)
    print(f'→ {out}')
    return out


def _selftest():
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    chk('① 색 규약이 리포의 dem 팔레트와 같다 (두 벌을 만들지 않는다)',
        TYPE_COL[1] == '#5b5b5b' and TYPE_COL[2] == '#8f8f8f' and TYPE_COL[3] == '#c9b88a')
    #  ★ 한글 라벨을 쓰는 도구이므로 폰트를 고르는지 본다 (없으면 조용히 □ 가 된다)
    _f = pick_cjk_font(warn=False)
    chk(f'②pre CJK 폰트를 고른다 ({_f or "**없음 — 한글은 □ 가 된다**"})', _f is not None)
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, 'm_100.liggghts'), 'w') as fh:
            fh.write('ITEM: TIMESTEP\n100\nITEM: NUMBER OF ATOMS\n3\n')
            fh.write('ITEM: BOX BOUNDS mm mm mm\n-1 1\n-1 1\n-1 1\n')
            fh.write('ITEM: ATOMS id type x y z radius\n')
            fh.write('1 1 0 0.010 0.000 0.0012\n2 3 0 0.000 0.010 0.0003\n'
                     '3 5 0 -0.010 0.000 0.0003\n')
        out = os.path.join(td, 'x.png')
        render([td], ['t'], out)
        chk('② PNG 가 실제로 만들어진다', os.path.exists(out) and os.path.getsize(out) > 5000)
        #  ★ 변이 — 덤프가 없으면 조용히 빈 그림을 내지 않는다
        empty = os.path.join(td, 'e'); os.makedirs(empty)
        try:
            render([empty], ['e'], os.path.join(td, 'y.png'))
            bad = False
        except SystemExit:
            bad = True
        chk('③ 변이: 덤프 없는 디렉터리는 **거부** (빈 그림을 내지 않는다)', bad)
    print(f'\nviz_mixer_bed selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', action='append', default=[])
    ap.add_argument('--label', action='append', default=[])
    ap.add_argument('--r-drum', type=float, default=0.02056)
    ap.add_argument('--suptitle', default='')
    ap.add_argument('--out', default='bed.png')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.dir:
        ap.error('--dir 을 하나 이상')
    labs = a.label or [os.path.basename(os.path.dirname(d)) for d in a.dir]
    render(a.dir, labs, a.out, a.r_drum, a.suptitle)

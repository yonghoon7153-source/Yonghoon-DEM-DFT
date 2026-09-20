#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lacey 혼합지수 `M(t)` — §24 층상 시작 런의 **믹싱** 지표 (2026-09-20).

    python3 scripts/measure_mixing_index.py <런 디렉터리> --ref <균일 삽입 런 디렉터리>
    python3 scripts/measure_mixing_index.py --selftest

━━ 정의 (사전등록 §24-3 — 결과 보고 바꾸지 않는다) ━━━━━━━━━━━━━━━━━━━━━━━━━━━
  셀      (y, z) `cells`×`cells` × x `x_cells`  (드럼 축 x, 통 반경 R 기준).  입자 ≥ n_min 인 칸만.
  p_i     칸 i 의 AM **부피분율** (type 1·2 부피 / 칸 안 고체 부피)
          ⚠ 개수분율이면 SE(개수 73 %)가 지배해 AM 의 분포를 못 본다.
  S²(t)   p_i 의 칸 간 분산
  S₀²     같은 런의 t=0 (정착 끝) 프레임         ← 층상 = 완전 분리 기준
  S_R²    균일 삽입 런(--ref, 같은 시드·같은 칸)의 정착 끝 프레임   ← 무작위 기준 (실측)
  M(t)  = (S₀² − S²(t)) / (S₀² − S_R²)

  ⚠ S_R² 를 이항식으로 두지 않는 이유: 다분산·부피가중 분율에 이항 공식이 안 맞는다.
    균일 삽입 침대가 이미 있으니(§13 E0) **같은 코드로 재서** 기준을 삼는다.

━━ t=0 · 바퀴 경계는 덱(`in.mixer`)에서 읽는다 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  `run N` 두 번 = 정착 (`2·steps_fill`) · `timestep` · `fix mvD … period P` ⇒ 바퀴 = P/dt 스텝.
  덱이 실행 기록이므로 별도 메타파일을 두지 않는다 (두 벌이면 갈린다).
  ⚠ 프레임은 **숫자순** (`ls | tail` 함정 — measure_bed_aspect.frames 를 재사용).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

import numpy as np

_SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCR)
from measure_bed_aspect import frames, read_dump                  # noqa: E402

AM_TYPES = (1, 2)


def deck_plan(deck_path):
    """`in.mixer` → dict(steps_fill, dump_every, dt, steps_per_rev, steps_run).  없으면 ValueError."""
    t = open(deck_path, encoding='utf-8', errors='replace').read()
    runs = [int(x) for x in re.findall(r'^run\s+(\d+)\s*$', t, re.M)]
    #  실제 덱은 `run 1`(삽입) · `run F` · `run F`(정착 두 번) · `run N`(회전) = 넷이다.
    #  ⇒ **회전 직전의 같은 값 두 줄**을 정착으로 잡는다 (앞에 뭐가 있든).
    if len(runs) < 3:
        raise ValueError(f'run 줄이 {len(runs)}개 — 정착 2 + 회전 1 이어야 한다')
    if runs[-3] != runs[-2]:
        raise ValueError(f'회전 직전의 두 run 이 다르다: {runs[-3]} vs {runs[-2]} (정착이 아니다)')
    dt = float(re.search(r'^timestep\s+([0-9.eE+-]+)', t, re.M).group(1))
    per = float(re.search(r'fix\s+mvD\s+.*?period\s+([0-9.eE+-]+)', t).group(1))
    de = int(re.search(r'^dump\s+dmp\s+all\s+custom\s+(\d+)', t, re.M).group(1))
    return dict(steps_fill=runs[-2], dump_every=de, dt=dt,
                steps_per_rev=per / dt, steps_run=runs[-1], n_run_lines=len(runs))


def cell_variance(D, r_container, cells=8, x_cells=2, n_min=20, axis='x'):
    """한 프레임 → (S², 쓴 칸 수, 버린 칸 수, 칸별 p_i)."""
    x, y, z = D['x'], D['y'], D['z']
    r = D['radius']; t = D['type'].astype(int)
    vol = (4.0 / 3.0) * np.pi * r ** 3
    am = np.isin(t, AM_TYPES).astype(float)
    if axis == 'x':                                    # 자유 단면 (y, z), 축 x
        a, b, c = y, z, x
    elif axis == 'y':
        a, b, c = x, z, y
    else:
        a, b, c = x, y, z
    R = float(r_container)
    ia = np.clip(((a + R) / (2 * R) * cells).astype(int), 0, cells - 1)
    ib = np.clip(((b + R) / (2 * R) * cells).astype(int), 0, cells - 1)
    lo, hi = c.min(), c.max()
    ic = np.clip(((c - lo) / max(hi - lo, 1e-12) * x_cells).astype(int), 0, x_cells - 1)
    key = (ia * cells + ib) * x_cells + ic
    ncell = cells * cells * x_cells
    cnt = np.bincount(key, minlength=ncell)
    vtot = np.bincount(key, weights=vol, minlength=ncell)
    vam = np.bincount(key, weights=vol * am, minlength=ncell)
    use = cnt >= n_min
    p = vam[use] / np.maximum(vtot[use], 1e-30)
    s2 = float(p.var(ddof=0)) if p.size > 1 else float('nan')
    return s2, int(use.sum()), int((cnt > 0).sum() - use.sum()), p


def _t0_frame(fr, steps_fill):
    """정착 끝 = 스텝 ≤ 2·steps_fill 인 마지막 프레임."""
    cand = [(st, p) for st, p in fr if st <= 2 * steps_fill]
    if not cand:
        raise SystemExit('⛔ 정착 구간 프레임이 없다 — 덤프 간격이 정착보다 길다')
    return cand[-1]


def analyse(run_dir, ref_dir, r_container, cells=8, x_cells=2, n_min=20, axis='x'):
    deck = os.path.join(run_dir, 'in.mixer')
    plan = deck_plan(deck)
    fr = frames(os.path.join(run_dir, 'post'))
    if not fr:
        raise SystemExit(f'⛔ {run_dir}: 덤프가 없다')
    kw = dict(cells=cells, x_cells=x_cells, n_min=n_min, axis=axis)
    st0, p0 = _t0_frame(fr, plan['steps_fill'])
    s0, n0, _, _ = cell_variance(read_dump(p0), r_container, **kw)
    #  무작위 기준 — 균일 삽입 런의 **같은 위치**(정착 끝) 프레임
    rplan = deck_plan(os.path.join(ref_dir, 'in.mixer'))
    rfr = frames(os.path.join(ref_dir, 'post'))
    _, rp = _t0_frame(rfr, rplan['steps_fill'])
    sR, nR, _, _ = cell_variance(read_dump(rp), r_container, **kw)
    if not (s0 > sR):
        raise SystemExit(f'⛔ S₀² ({s0:.4g}) ≤ S_R² ({sR:.4g}) — 층상 시작이 아니거나 기준이 틀렸다.  '
                         f'M 을 정의할 수 없다 (§24-4 바닥 검사 실패)')
    rows = []
    for st, pth in fr:
        if st < st0:
            continue
        s2, nu, nd, _ = cell_variance(read_dump(pth), r_container, **kw)
        rev = (st - st0) / plan['steps_per_rev']
        rows.append(dict(step=st, rev=rev, s2=s2, M=(s0 - s2) / (s0 - sR), cells_used=nu, cells_dropped=nd))
    #  바퀴별 요약
    by_rev = {}
    for r_ in rows:
        k = int(np.floor(r_['rev'] + 1e-9))
        by_rev.setdefault(k, []).append(r_['M'])
    revs = {k: dict(M_mean=float(np.mean(v)), M_sd=float(np.std(v, ddof=1)) if len(v) > 1 else 0.0,
                    n=len(v)) for k, v in sorted(by_rev.items())}
    last_k = max(revs)
    return dict(run=run_dir, ref=ref_dir, plan=plan, t0_step=st0, S0=s0, SR=sR,
                cells_t0=n0, cells_ref=nR, rows=rows, by_rev=revs,
                M_final=revs[last_k]['M_mean'], M_final_sd=revs[last_k]['M_sd'], final_rev=last_k,
                M_t0=rows[0]['M'])


def report(res):
    print(f"{res['run']}")
    print(f"   t0 step {res['t0_step']} · S₀² {res['S0']:.5f} ({res['cells_t0']} 칸) · S_R² {res['SR']:.5f} "
          f"({res['cells_ref']} 칸, ref {os.path.basename(res['ref'].rstrip('/'))}) · M(t0) {res['M_t0']:+.3f}")
    for k, v in res['by_rev'].items():
        print(f"   바퀴 {k:2d}  M {v['M_mean']:6.3f} ± {v['M_sd']:.3f}  (프레임 {v['n']})")
    print(f"   ★ M_final (바퀴 {res['final_rev']}) = {res['M_final']:.3f} ± {res['M_final_sd']:.3f}")


# ───────────────────────────── selftest ─────────────────────────────
def _selftest():                                              # noqa: C901
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    rng = np.random.default_rng(7)
    R = 0.02

    def cloud(n, layered, seg_frac=1.0, r_am=0.0012, r_se=0.0003):
        """반지름 R 안에 n 개 — layered=True 면 AM 은 z<0, SE 는 z>0 (seg_frac 만큼)."""
        th = rng.uniform(0, 2 * np.pi, n); rr = R * 0.9 * np.sqrt(rng.uniform(0, 1, n))
        y, z = rr * np.cos(th), rr * np.sin(th)
        x = rng.uniform(-0.007, 0.007, n)
        t = np.where(rng.uniform(0, 1, n) < 0.3, 1, 3)
        if layered:
            flip = rng.uniform(0, 1, n) < seg_frac
            z = np.where(flip, -np.abs(z) * (t == 1) + np.abs(z) * (t == 3), z)
        r = np.where(t == 1, r_am, r_se)
        return dict(id=np.arange(n) + 1., type=t.astype(float), mol=-np.ones(n),
                    x=x, y=y, z=z, radius=r)

    def write_dump(path, D):
        n = len(D['x'])
        with open(path, 'w') as f:
            f.write(f'ITEM: TIMESTEP\n0\nITEM: NUMBER OF ATOMS\n{n}\nITEM: BOX BOUNDS pp pp pp\n'
                    '-1 1\n-1 1\n-1 1\nITEM: ATOMS id type mol x y z radius\n')
            for i in range(n):
                f.write(f"{int(D['id'][i])} {int(D['type'][i])} {int(D['mol'][i])} "
                        f"{D['x'][i]:.6g} {D['y'][i]:.6g} {D['z'][i]:.6g} {D['radius'][i]:.6g}\n")

    DECK = ('timestep 1e-6\nrun 1\nrun 1000\nrun 1000\n'
            'dump dmp all custom 500 post/mix_*.liggghts id type mol x y z radius\n'
            'fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1. 0. 0. period 1.0\n'
            'run 4000\n')

    seg = cloud(6000, True); mix = cloud(6000, False)
    s_seg, nu_seg, _, _ = cell_variance(seg, R)
    s_mix, nu_mix, _, _ = cell_variance(mix, R)
    chk('① 완전 분리 침대의 S² 가 무작위 침대보다 훨씬 크다', s_seg > 5 * s_mix and nu_seg > 20)
    half = cloud(6000, True, seg_frac=0.5)
    s_half, _, _, _ = cell_variance(half, R)
    chk('② 반만 분리하면 S² 가 그 사이에 온다', s_mix < s_half < s_seg)

    #  부피가중 vs 개수가중이 실제로 다른 경우 (AM 이 크고 적다)
    p_num = None
    D = seg
    t = D['type'].astype(int); am = np.isin(t, AM_TYPES)
    chk('③ AM 개수분율 ≪ 부피분율 (개수로 재면 SE 가 지배한다)',
        am.mean() < 0.35 and ((4/3*np.pi*D['radius']**3)[am].sum() /
                              (4/3*np.pi*D['radius']**3).sum()) > 0.8)

    with tempfile.TemporaryDirectory() as td:
        run = os.path.join(td, 'run'); ref = os.path.join(td, 'ref')
        for d in (run, ref):
            os.makedirs(os.path.join(d, 'post'))
            open(os.path.join(d, 'in.mixer'), 'w').write(DECK)
        #  run: t0(step 2000) 층상 → 점점 섞임 (프레임 9600 이 249600 뒤에 오게 이름을 둔다: 숫자순 검사)
        seq = [(2000, 1.0), (2500, 0.75), (3000, 0.5), (4000, 0.25), (9600, 0.1)]
        for st, f in seq:
            write_dump(os.path.join(run, 'post', f'mix_{st}.liggghts'), cloud(6000, True, seg_frac=f))
        #  마지막 프레임 = 기준 구름과 **동일** ⇒ 공식상 M_final 이 정확히 1 이어야 한다
        _refc = cloud(6000, False)
        write_dump(os.path.join(run, 'post', 'mix_249600.liggghts'), _refc)
        write_dump(os.path.join(ref, 'post', 'mix_2000.liggghts'), _refc)
        res = analyse(run, ref, R)
        chk('④ t0 = 정착 끝(step 2000) 프레임이고 M(t0) ≈ 0', res['t0_step'] == 2000 and abs(res['M_t0']) < 1e-9)
        Ms = [r_['M'] for r_ in res['rows']]
        #  단조성은 프레임마다 새 추첨이라 잡음 허용(−0.05); 마지막은 기준과 같은 구름이라 정확히 1
        chk('⑤ M 이 시간에 따라 (잡음 안에서) 증가하고, 기준과 같은 구름이면 정확히 1',
            all(np.diff(Ms) > -0.05) and Ms[-1] > Ms[0] + 0.5 and abs(Ms[-1] - 1.0) < 1e-9)
        chk('⑥ 프레임을 숫자순으로 읽는다 (249600 이 9600 뒤)', res['rows'][-1]['step'] == 249600)
        chk('⑦ 바퀴 경계 = period/dt (1e6 스텝) 로 계산돼 전부 0 바퀴째다', res['final_rev'] == 0
            and res['plan']['steps_per_rev'] == 1e6)
        #  빈 칸 보고
        _, nu, nd, _ = cell_variance(cloud(300, False), R, n_min=20)
        chk('⑧ 입자가 적으면 칸을 버리고 **개수를 보고**한다 (조용히 안 넘긴다)', nd > 0 and nu < 128)
        #  바닥 검사: 층상이 아닌 런을 주면 거부
        run2 = os.path.join(td, 'run2'); os.makedirs(os.path.join(run2, 'post'))
        open(os.path.join(run2, 'in.mixer'), 'w').write(DECK)
        write_dump(os.path.join(run2, 'post', 'mix_2000.liggghts'), cloud(6000, False))
        try:
            analyse(run2, ref, R); bad = False
        except SystemExit as e:
            bad = '바닥 검사' in str(e)
        chk('⑨ S₀² ≤ S_R² 면 M 을 정의하지 않고 거부한다 (§24-4 바닥 검사)', bad)
        #  덱 파싱 거부
        open(os.path.join(run2, 'in.mixer'), 'w').write('timestep 1e-6\nrun 5\n')
        try:
            deck_plan(os.path.join(run2, 'in.mixer')); bad2 = False
        except ValueError:
            bad2 = True
        chk('⑩ 덱에 run 줄이 셋 미만이면 거부한다', bad2)

    #  실제 덱으로 파서 검증 (스크래치패드에 있을 때만 — 없으면 이름으로 보고)
    _real = os.environ.get('MIX_REAL_DECK', '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/'
                           'd26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/arms3/E1/in.mixer')
    if os.path.exists(_real):
        pl = deck_plan(_real)
        chk('⑪ 실제 덱: run 줄 4 개 중 정착 36308 ×2 · 회전 427062 · 바퀴 ≈ 213,538 스텝',
            pl['n_run_lines'] == 4 and pl['steps_fill'] == 36308 and pl['steps_run'] == 427062
            and abs(pl['steps_per_rev'] - 213538) < 2)
    else:
        print('  SKIP  ⑪ 실제 덱이 없어 건너뜀 (MIX_REAL_DECK 로 지정 가능)')

    print(f'\nmeasure_mixing_index selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='Lacey 혼합지수 (§24)')
    ap.add_argument('runs', nargs='*', help='런 디렉터리 (in.mixer + post/)')
    ap.add_argument('--ref', help='균일 삽입 런 디렉터리 (S_R² 기준)')
    ap.add_argument('--r-container', type=float, default=0.02056)
    ap.add_argument('--cells', type=int, default=8)
    ap.add_argument('--x-cells', type=int, default=2)
    ap.add_argument('--n-min', type=int, default=20)
    ap.add_argument('--axis', default='x', choices=('x', 'y', 'z'))
    ap.add_argument('--json', help='결과 JSON 을 쓸 경로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not (a.runs and a.ref):
        ap.error('런 디렉터리와 --ref 가 필요하다')
    out = []
    for d in a.runs:
        res = analyse(d, a.ref, a.r_container, a.cells, a.x_cells, a.n_min, a.axis)
        report(res)
        out.append(res)
    if a.json:
        json.dump(out, open(a.json, 'w'), ensure_ascii=False, indent=1, default=float)
        print(f'→ {a.json}')


if __name__ == '__main__':
    main()

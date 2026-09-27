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

━━ 2026-09-27 보조 진단 (Codex HB-05) — M 의 정의는 그대로, 판정에 안 쓰는 값만 더 적는다 ━━━━━━━━━━━━━
  ① `planned` = 덱의 계획 바퀴 수의 **마지막 완전 bin** (8 바퀴면 bin 7, 25 프레임) 과 평탄 조건.
     ⚠ 옛 `M_final` 은 **마지막 bin** 이라 중간 판독에서는 부분 bin (2–12 프레임) 이다 — 최종값으로 쓰지 말 것.
  ② 칸 선택 진단 — `n_min` 미만 칸을 버리면 한 상이 버린 칸에 몰렸을 때 분리가 숨는다 (셀프테스트 ⑫).
     프레임마다 상별 유지 부피·입자 비 (`am_vol_kept` · `se_vol_kept` …) · 버린 칸 · 칸당 입자 중앙값 ·
     빈 칸만 뺀 **전 칸 M (`M_all`, 민감도)**.
  ③ `tech` — 미완주 · 최종 bin 비유한값 · 최종·직전 bin 덤프 결손.  있으면 등록 최종값을 쓰지 않는다.

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
    """한 프레임 → (S², 쓴 칸 수, 버린 칸 수, 칸별 p_i).  (계산은 cell_stats — 이 함수는 옛 반환형 그대로)"""
    st = cell_stats(D, r_container, cells, x_cells, n_min, axis)
    return st['s2'], st['used'], st['dropped'], st['p']


def cell_stats(D, r_container, cells=8, x_cells=2, n_min=20, axis='x'):
    """한 프레임 → dict: s2 · used · dropped · p (= cell_variance) + **보조 진단** (2026-09-27, Codex HB-05).

    ⚠ 왜 — `n_min` 미만 칸을 버리므로 **한 상이 통째로 버린 칸에 몰리면 분리가 '분산 0' 으로 숨는다**
      (셀프테스트 ⑫: AM 칸 둘 + SE 19 알 칸 하나 → S² = 0).  M 의 정의는 바꾸지 않고, 버린 몫을 **보이게** 한다:
      am_vol_kept · se_vol_kept = 쓴 칸 안의 상별 부피 / 그 상 전체 · am_n_kept · se_n_kept (입자 수) ·
      nonempty (빈 칸 아닌 칸) · cell_n_median (쓴 칸의 입자 수 중앙값 — prereg §2 가 보고를 요구) ·
      s2_all = **빈 칸만 뺀 모든 칸**의 분산 (민감도 — 판정에 쓰지 않는다).
      'se' = AM 이 아닌 상 전부 (3 상 캠페인에서는 SE).
    """
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
    cam = np.bincount(key, weights=am, minlength=ncell)
    vtot = np.bincount(key, weights=vol, minlength=ncell)
    vam = np.bincount(key, weights=vol * am, minlength=ncell)
    use = cnt >= n_min
    ne = cnt > 0
    p = vam[use] / np.maximum(vtot[use], 1e-30)
    s2 = float(p.var(ddof=0)) if p.size > 1 else float('nan')
    p_all = vam[ne] / np.maximum(vtot[ne], 1e-30)
    vse, cse = vtot - vam, cnt - cam

    def _frac(a_, tot):
        return float(a_[use].sum() / tot) if tot > 0 else float('nan')
    return dict(s2=s2, used=int(use.sum()), dropped=int(ne.sum() - use.sum()), p=p,
                nonempty=int(ne.sum()), s2_all=float(p_all.var(ddof=0)) if p_all.size > 1 else float('nan'),
                am_vol_kept=_frac(vam, vam.sum()), se_vol_kept=_frac(vse, vse.sum()),
                am_n_kept=_frac(cam, cam.sum()), se_n_kept=_frac(cse, cse.sum()),
                cell_n_median=float(np.median(cnt[use])) if use.any() else float('nan'))


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
    c0 = cell_stats(read_dump(p0), r_container, **kw)
    s0, n0 = c0['s2'], c0['used']
    #  무작위 기준 — 균일 삽입 런의 **같은 위치**(정착 끝) 프레임
    rplan = deck_plan(os.path.join(ref_dir, 'in.mixer'))
    rfr = frames(os.path.join(ref_dir, 'post'))
    _, rp = _t0_frame(rfr, rplan['steps_fill'])
    cR = cell_stats(read_dump(rp), r_container, **kw)
    sR, nR = cR['s2'], cR['used']
    if not (s0 > sR):
        raise SystemExit(f'⛔ S₀² ({s0:.4g}) ≤ S_R² ({sR:.4g}) — 층상 시작이 아니거나 기준이 틀렸다.  '
                         f'M 을 정의할 수 없다 (§24-4 바닥 검사 실패)')
    #  민감도 (판정에 안 씀): 빈 칸만 뺀 모든 칸의 M — 버린 칸이 분리를 숨기는지 보이게
    s0a, sRa = c0['s2_all'], cR['s2_all']
    DIAG = ('am_vol_kept', 'se_vol_kept', 'am_n_kept', 'se_n_kept', 'nonempty', 'cell_n_median', 's2_all')
    rows = []
    for st, pth in fr:
        if st < st0:
            continue
        cs = c0 if st == st0 else cell_stats(read_dump(pth), r_container, **kw)
        s2 = cs['s2']
        rev = (st - st0) / plan['steps_per_rev']
        row = dict(step=st, rev=rev, s2=s2, M=(s0 - s2) / (s0 - sR), cells_used=cs['used'], cells_dropped=cs['dropped'])
        row.update({k: cs[k] for k in DIAG})
        row['M_all'] = (s0a - cs['s2_all']) / (s0a - sRa) if s0a > sRa else float('nan')
        rows.append(row)
    #  바퀴별 요약
    by_rev = {}
    for r_ in rows:
        k = int(np.floor(r_['rev'] + 1e-9))
        by_rev.setdefault(k, []).append(r_)
    revs = {}
    for k, rr in sorted(by_rev.items()):
        v = [r_['M'] for r_ in rr]
        fin = [x for x in v if np.isfinite(x)]
        revs[k] = dict(M_mean=float(np.mean(v)), M_sd=float(np.std(v, ddof=1)) if len(v) > 1 else 0.0, n=len(v),
                       n_nonfinite=len(v) - len(fin),
                       M_all_mean=float(np.mean([r_['M_all'] for r_ in rr])),
                       s2_mean=float(np.mean([r_['s2'] for r_ in rr])),
                       am_vol_kept_mean=float(np.mean([r_['am_vol_kept'] for r_ in rr])),
                       se_vol_kept_mean=float(np.mean([r_['se_vol_kept'] for r_ in rr])),
                       vol_kept_min=float(min(min(r_['am_vol_kept'], r_['se_vol_kept']) for r_ in rr)),
                       cells_dropped_frac=float(np.mean([r_['cells_dropped'] / max(r_['nonempty'], 1) for r_ in rr])))
    last_k = max(revs)
    #  ★ 등록 최종값 (2026-09-27, Codex HB-05) — 덱의 계획 바퀴 수의 **마지막 완전 바퀴**.  옛 `M_final` 은 마지막
    #    bin 이라 **부분 bin** (2–12 프레임, 중간 판독) 일 수 있어 최종값으로 쓰면 안 된다 (셀프테스트 ⑬b).
    #    완전 = 그 뒤 bin 에 프레임이 있거나, 마지막 프레임이 바퀴 끝에서 덤프 한 간격 안.
    fpr = plan['steps_per_rev'] / plan['dump_every']
    last_rev = rows[-1]['rev']
    n_revs = int(round(plan['steps_run'] / plan['steps_per_rev']))

    def _complete(k):
        return k in revs and (k < last_k or last_rev >= k + 1 - 1.0 / fpr - 1e-9)
    steps = [r_['step'] for r_ in rows]
    gaps = [(a_, b_) for a_, b_ in zip(steps, steps[1:]) if b_ - a_ != plan['dump_every']]
    tech = []
    planned = None
    if n_revs >= 1:
        fb = n_revs - 1
        ok_ = _complete(fb)
        planned = dict(n_revs=n_revs, final_bin=fb, frames_per_rev=fpr, complete=ok_,
                       n=revs[fb]['n'] if fb in revs else 0,
                       M_final=revs[fb]['M_mean'] if ok_ else None, M_final_sd=revs[fb]['M_sd'] if ok_ else None,
                       prev_bin=fb - 1, flat=None)
        if ok_ and _complete(fb - 1):
            planned['flat'] = bool(abs(revs[fb]['M_mean'] - revs[fb - 1]['M_mean']) <= revs[fb]['M_sd'])
        if not ok_:
            tech.append(f'미완주 — 계획 {n_revs} 바퀴의 마지막 bin {fb} 이 완전하지 않다 (마지막 프레임 rev {last_rev:.3f})')
        elif revs[fb]['n_nonfinite']:
            tech.append(f'최종 bin {fb} 에 비유한 M {revs[fb]["n_nonfinite"]} 프레임')
        if any(a_ >= st0 + (fb - 1) * plan['steps_per_rev'] - plan['dump_every'] for a_, _ in gaps):
            tech.append(f'최종·직전 bin (평탄 조건) 의 덤프 간격 결손: {gaps}')
    return dict(run=run_dir, ref=ref_dir, plan=plan, t0_step=st0, S0=s0, SR=sR,
                cells_t0=n0, cells_ref=nR, rows=rows, by_rev=revs,
                M_final=revs[last_k]['M_mean'], M_final_sd=revs[last_k]['M_sd'], final_rev=last_k,
                M_t0=rows[0]['M'], planned=planned, tech=tech, dump_gaps=gaps,
                S0_all=s0a, SR_all=sRa,
                diag_t0={k: c0[k] for k in DIAG + ('used', 'dropped')},
                diag_ref={k: cR[k] for k in DIAG + ('used', 'dropped')})


def report(res):
    print(f"{res['run']}")
    print(f"   t0 step {res['t0_step']} · S₀² {res['S0']:.5f} ({res['cells_t0']} 칸) · S_R² {res['SR']:.5f} "
          f"({res['cells_ref']} 칸, ref {os.path.basename(res['ref'].rstrip('/'))}) · M(t0) {res['M_t0']:+.3f}")
    d0 = res['diag_t0']
    print(f"   t0 보조: 유지 부피 AM {d0['am_vol_kept']:.3f} · SE {d0['se_vol_kept']:.3f} · 버린 칸 {d0['dropped']}/{d0['nonempty']} "
          f"· 칸당 입자 중앙 {d0['cell_n_median']:.0f} · 전 칸 S₀² {res['S0_all']:.5f} / S_R² {res['SR_all']:.5f}")
    for k, v in res['by_rev'].items():
        print(f"   바퀴 {k:2d}  M {v['M_mean']:6.3f} ± {v['M_sd']:.3f}  (프레임 {v['n']})"
              f"   [유지 부피 AM {v['am_vol_kept_mean']:.3f} · SE {v['se_vol_kept_mean']:.3f} · 버린 칸 "
              f"{v['cells_dropped_frac']*100:.1f} % · 전 칸 M {v['M_all_mean']:.3f}]")
    print(f"   (옛 키) M_final = 마지막 bin {res['final_rev']} ({res['by_rev'][res['final_rev']]['n']} 프레임 — 부분일 수 있다) "
          f"= {res['M_final']:.3f} ± {res['M_final_sd']:.3f}")
    pl = res.get('planned')
    if pl:
        if pl['complete']:
            print(f"   ★ 등록 최종값 (계획 {pl['n_revs']} 바퀴 · bin {pl['final_bin']} · {pl['n']} 프레임) = "
                  f"{pl['M_final']:.3f} ± {pl['M_final_sd']:.3f}   평탄 {pl['flat']}")
        else:
            print(f"   ★ 등록 최종값 — 없음 (bin {pl['final_bin']} 미완 · {pl['n']} 프레임)")
    for t in res.get('tech', []):
        print(f"   ⚠ {t}")


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

    # ══ ⑫~⑮ 2026-09-27 Codex HB-05 — 버린 칸이 분리를 숨기는가 · 부분 바퀴를 최종값으로 쓰는가 ══════════════
    #  ⑫ Codex 반례 그대로: AM 만 25 알 든 칸 둘 + SE 만 19 알 든 칸 하나 (n_min 20) → S² = 0 · 쓴 칸 2 · 버린 칸 1.
    #     두 상은 완전히 갈라져 있는데 SE 칸이 통째로 빠져 '분산 0' 이 된다.
    def _blob(cy, cz, n, typ, rad):
        return dict(y=np.full(n, cy) + rng.uniform(-1e-4, 1e-4, n), z=np.full(n, cz) + rng.uniform(-1e-4, 1e-4, n),
                    x=rng.uniform(-0.006, -0.004, n), type=np.full(n, float(typ)), radius=np.full(n, rad))
    parts = [_blob(-0.015, -0.015, 25, 1, 5e-4), _blob(0.015, -0.015, 25, 1, 5e-4), _blob(0.005, 0.015, 19, 3, 2e-4)]
    Dsep = {k: np.concatenate([p_[k] for p_ in parts]) for k in parts[0]}
    s2_, nu_, nd_, _ = cell_variance(Dsep, R, cells=4, x_cells=1, n_min=20)
    chk(f'⑫ 재현: 버린 칸이 분리를 숨긴다 — S² {s2_:.3g} · 쓴 칸 {nu_} · 버린 칸 {nd_} (Codex 반례)',
        s2_ == 0.0 and nu_ == 2 and nd_ == 1)
    cs = cell_stats(Dsep, R, cells=4, x_cells=1, n_min=20)
    chk(f'⑫b ★ 보조 진단이 그것을 드러낸다 — SE 유지 부피 {cs["se_vol_kept"]:.2f} · AM {cs["am_vol_kept"]:.2f} · '
        f'전 칸 S² {cs["s2_all"]:.3f}',
        cs['se_vol_kept'] == 0.0 and cs['am_vol_kept'] == 1.0 and cs['s2_all'] > 0.2 and cs['nonempty'] == 3)
    #  ⑬ 등록 최종값 = 덱의 계획 바퀴 수의 **마지막 완전 바퀴**.  옛 `M_final` 은 마지막 bin (부분일 수 있다).
    DECK2 = ('timestep 1e-3\nrun 1\nrun 10\nrun 10\n'
             'dump dmp all custom 250 post/mix_*.liggghts id type mol x y z radius\n'
             'fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1. 0. 0. period 1.001\n'
             'run 2000\n')
    with tempfile.TemporaryDirectory() as td:
        run = os.path.join(td, 'run'); ref = os.path.join(td, 'ref')
        for d in (run, ref):
            os.makedirs(os.path.join(d, 'post'))
            open(os.path.join(d, 'in.mixer'), 'w').write(DECK2)
        write_dump(os.path.join(ref, 'post', 'mix_20.liggghts'), cloud(6000, False))
        write_dump(os.path.join(run, 'post', 'mix_20.liggghts'), cloud(6000, True))
        #  t0 = 20 · 바퀴 = 1001 스텝 · 덤프 250 ⇒ 실제 캠페인 (바퀴 = 덤프 25.0004 개) 처럼 마지막 덤프가 계획 끝
        #  **바로 앞** (rev 1.998) 이고 덤프 간격에 결손이 없다
        for k_ in range(1, 9):
            write_dump(os.path.join(run, 'post', f'mix_{20 + 250 * k_}.liggghts'), cloud(6000, True, seg_frac=0.3))
        res = analyse(run, ref, R)
        pl_ = res['planned']
        chk(f'⑬ 계획 바퀴 수 {pl_["n_revs"]} · 최종 bin {pl_["final_bin"]} 완전 ({pl_["n"]} 프레임) · 값 = 그 bin 평균',
            pl_['n_revs'] == 2 and pl_['final_bin'] == 1 and pl_['complete'] and pl_['n'] == 4
            and abs(pl_['M_final'] - res['by_rev'][1]['M_mean']) < 1e-12 and not res['tech'])
        #  덤프가 계획 끝을 한 프레임 넘으면 옛 `M_final` 은 **1 프레임짜리 부분 bin** 을 낸다 — 등록 값은 안 움직인다
        write_dump(os.path.join(run, 'post', f'mix_{20 + 250 * 9}.liggghts'), cloud(6000, False))
        res2 = analyse(run, ref, R)
        chk(f'⑬b 옛 M_final (bin {res2["final_rev"]}, 프레임 {res2["by_rev"][res2["final_rev"]]["n"]}) ≠ 등록 최종값 '
            f'(bin {res2["planned"]["final_bin"]}) — 부분 bin 을 최종값으로 쓰지 않는다',
            res2['final_rev'] == 2 and res2['by_rev'][2]['n'] == 1
            and abs(res2['planned']['M_final'] - res['planned']['M_final']) < 1e-12)
        #  미완주 — 마지막 두 프레임을 치우면 최종 bin 이 불완전 ⇒ 값 없음 + 기술 표지
        for k_ in (7, 8, 9):
            os.remove(os.path.join(run, 'post', f'mix_{20 + 250 * k_}.liggghts'))
        res3 = analyse(run, ref, R)
        chk(f'⑭ 미완주면 등록 최종값 = 없음 · 기술 표지 ({"; ".join(res3["tech"])[:60]})',
            res3['planned']['M_final'] is None and not res3['planned']['complete'] and res3['tech'])
        #  ⑮ 평탄 조건 (prereg §2: |M̄₈ − M̄₇| ≤ M_sd(8)) 을 등록 bin 으로 계산해 둔다
        pf_ = res['planned']
        chk('⑮ 평탄 조건 = |M̄(최종) − M̄(직전)| ≤ sd(최종) 를 등록 bin 으로 계산한다',
            pf_['flat'] == (abs(res['by_rev'][1]['M_mean'] - res['by_rev'][0]['M_mean']) <= res['by_rev'][1]['M_sd']))

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

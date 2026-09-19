#!/usr/bin/env python3
"""침대 종횡비 지표 — `docs/reviews/mixing_model_design_20260919.md` §6 주지표.

왜 이 지표인가 (실측 근거)
  1저자가 준 `Tutorials_public/cohesion` 대조쌍을 직접 돌려 확인했다 (2026-09-19):
      noCohesion  R99 48.50 mm · H  2.60 mm · H/R 0.054 · phi 0.737
      cohesion    R99 43.46 mm · H 13.01 mm · H/R 0.299 · phi 0.183
      ⇒ H/R 이 **5.59배**.  문턱 조정이 필요 없다.

⚠⚠ 두 가지를 이 도구가 강제한다 — 둘 다 실제로 틀렸던 자리다.
  ① **프레임은 숫자순으로 고른다.**  `ls | tail` 은 사전순이라 `_9600` 이 `_249600`
     뒤에 온다 (CLAUDE.md 가 경고한 그 함정).
  ② **정착을 확인한다.**  튜토리얼 기본 `run 50000 upto` 는 0.5 초인데 낙하 60 mm ·
     반발계수 0.9 의 정착 시간은 약 2.1 초다 = **정착의 24 %**.  그 시점에 재면
     침대가 아니라 튀는 구름이고 지표가 **부호까지 반대로** 나온다.
     ⇒ `phi(포락)` 이 0.10 미만이면 **경고**한다.

usage
  python3 scripts/measure_bed_aspect.py <디렉터리> [<디렉터리> ...]
  python3 scripts/measure_bed_aspect.py nocoh/post coh/post
  python3 scripts/measure_bed_aspect.py --r-container 0.05 nocoh/post coh/post
  python3 scripts/measure_bed_aspect.py --axis x E0/post E4/post   # 가로 드럼
  python3 scripts/measure_bed_aspect.py --selftest
"""
import argparse
import glob
import os
import re
import sys

import numpy as np

PHI_LOOSE_WARN = 0.10      # 이 아래면 "정착 안 됨" 경고
STEP_RE = re.compile(r'_(\d+)\.[A-Za-z]+$')


def frames(d):
    """디렉터리의 덤프를 **숫자순**으로 (step, path) 리스트로."""
    out = []
    for f in glob.glob(os.path.join(d, '*')):
        m = STEP_RE.search(os.path.basename(f))
        if m:
            out.append((int(m.group(1)), f))
    return sorted(out)


def read_dump(path):
    """LIGGGHTS 평문 덤프 또는 legacy VTK POLYDATA → {열이름: 배열}."""
    txt = open(path, encoding='utf-8', errors='replace').read()
    L = txt.split('\n')
    hdr = [k for k, l in enumerate(L) if l.startswith('ITEM: ATOMS')]
    if hdr:                                             # 평문
        i = hdr[0]
        cols = L[i].split()[2:]
        A = np.array([[float(v) for v in l.split()] for l in L[i + 1:] if l.strip()])
        return {n: A[:, j] for j, n in enumerate(cols)}
    if 'DATASET POLYDATA' in txt:                       # VTK
        k = next(j for j, l in enumerate(L) if l.startswith('POINTS'))
        n = int(L[k].split()[1])
        vals = []
        j = k + 1
        while len(vals) < n * 3:
            t = L[j].split()
            if not t or not re.match(r'^-?[\d.eE+-]+$', t[0]):
                break
            vals += [float(x) for x in t]
            j += 1
        P = np.array(vals[:n * 3]).reshape(n, 3)
        out = {'x': P[:, 0], 'y': P[:, 1], 'z': P[:, 2]}
        m = re.search(r'^radius\s+1\s+(\d+)\s+\w+$', txt, re.M)
        if m:                                           # FIELD 안의 radius
            k2 = next(j for j, l in enumerate(L) if l.startswith('radius '))
            rv = []
            j = k2 + 1
            while len(rv) < n:
                t = L[j].split()
                if not t or not re.match(r'^-?[\d.eE+-]+$', t[0]):
                    break
                rv += [float(x) for x in t]
                j += 1
            out['radius'] = np.array(rv[:n])
        return out
    raise SystemExit(f'⛔ 읽을 수 없는 형식: {path}')


def measure_many(d, r_container=0.05, label=None, axis='z', last=1):
    """마지막 `last` 프레임의 평균 ± 표준편차.

    ⚠⚠ **회전 중인 침대는 한 프레임으로 재면 안 된다** — 텀블링 침대는 매 순간
      모양이 흔들린다 (cataracting 에서 사태가 주기적으로 무너진다).  한 장만
      보면 그 요동이 팔 사이 차이로 읽힌다.
      ⇒ 마지막 한 바퀴 분량을 평균하고 **산포를 같이 보고한다**.
      ★ 이 산포는 **런 내부** 변동이다.  판정선(§7)이 요구하는 **시드 간** SE 와
        다른 양이다 — 둘을 섞지 말 것.
    """
    fr = frames(d)
    if not fr:
        raise SystemExit(f'⛔ {d}: 번호 붙은 덤프가 없다')
    use = fr[-last:] if last > 1 else fr[-1:]
    ms = [measure(d, r_container, label, axis, _path=p) for _, p in use]
    out = dict(ms[-1])
    out['n_used'] = len(ms)
    for k in ('HR', 'R', 'H', 'phi'):
        v = np.array([m[k] for m in ms], dtype=float)
        out[k] = float(v.mean())
        out[k + '_sd'] = float(v.std(ddof=1)) if len(v) > 1 else 0.0
    out['step_lo'] = use[0][0]
    return out


def measure(d, r_container=0.05, label=None, axis='z', _path=None):
    """axis = **통의 대칭축** (중력은 언제나 −z).

    ⚠⚠ 축을 인자로 뺀 이유 — 초판은 `hypot(x, y)` 를 **박아** 뒀고, 그것은
       세로 실린더(튜토리얼 `cohesion`)에서만 맞는다.  우리 드럼은 STL 실측
       x 15.14 mm · y 75.62 · z 75.56 = **축이 x 인 가로 드럼**이라
       `hypot(x, y)` 가 드럼 길이(x)와 자유 퍼짐(y)을 섞어 버렸다.
         axis='z' → 측방 퍼짐은 (x, y) 평면      R = pct99(√(x²+y²))
         axis='x' → 축이 x 이므로 자유 퍼짐은 y  R = pct99(|y|)
         axis='y' → 자유 퍼짐은 x                R = pct99(|x|)
    """
    fr = frames(d)
    if not fr:
        raise SystemExit(f'⛔ {d}: 번호 붙은 덤프가 없다')
    step, path = fr[-1]                                 # ★ 숫자순 마지막
    if _path is not None:                               # 특정 프레임을 지정할 때
        step = next(st for st, pp in fr if pp == _path)
        path = _path
    D = read_dump(path)
    if 'radius' not in D:
        raise SystemExit(f'⛔ {path}: radius 열이 없다 — 덤프에 radius 를 넣을 것')
    x, y, z, r = D['x'], D['y'], D['z'], D['radius']
    n = len(x)
    if axis == 'z':                                     # 세로 실린더 — 중력축 = 통축
        rad = np.hypot(x, y)
        env_of = lambda R, H: np.pi * R ** 2 * H        # 원기둥 포락
    elif axis == 'x':                                   # 가로 드럼, 축 = x
        rad = np.abs(y)
        env_of = lambda R, H: 2 * R * float(x.max() - x.min()) * H
    elif axis == 'y':
        rad = np.abs(x)
        env_of = lambda R, H: 2 * R * float(y.max() - y.min()) * H
    else:
        raise SystemExit(f'⛔ axis 는 x·y·z 중 하나여야 한다 (받은 값 {axis!r})')
    R99 = float(np.percentile(rad, 99))                 # 튄 입자가 최댓값을 지배하지 않도록
    H = float(z.max() - z.min())
    #  ⚠ 다분산 침대에서 `n·(4/3)π r̄³` 은 **틀린다** (AM 1.2 mm 와 SE 0.3 mm 를
    #    평균내면 부피가 엉망이 된다).  입자마다 더한다.
    Vp = float(((4 / 3) * np.pi * r ** 3).sum())
    env = env_of(R99, H)
    phi = Vp / env if (R99 > 0 and H > 0 and env > 0) else float('nan')
    return dict(label=label or d, step=step, n=n, R=R99, H=H, axis=axis,
                HR=(H / R99 if R99 > 0 else float('nan')),
                R_over_Rc=(R99 / r_container if r_container else float('nan')),
                phi=phi, n_frames=len(fr), path=path)


def report(rs):
    for m in rs:
        print(f'{m["label"]:14s} step {m["step"]:7d} · n {m["n"]:5d} · 프레임 {m["n_frames"]}'
              f' · 통축 {m.get("axis", "z")}')
        sd = (f' ± {m["HR_sd"]:.3f}' if m.get('HR_sd') else '')
        nu = (f' · {m["n_used"]} 프레임 평균 (step {m.get("step_lo")}~)'
              if m.get('n_used', 1) > 1 else '')
        print(f'   R(99%) {m["R"]*1e3:7.2f} mm · H {m["H"]*1e3:7.2f} mm · ★ H/R {m["HR"]:6.3f}{sd}'
              f' · R/R_통 {m["R_over_Rc"]:5.3f} · φ(포락) {m["phi"]:5.3f}{nu}')
        if m['phi'] < PHI_LOOSE_WARN:
            print(f'   ⚠⚠ φ(포락) < {PHI_LOOSE_WARN} — **정착 안 된 것으로 보인다**'
                  f' (침대가 아니라 튀는 구름).  런을 늘리고 다시 잴 것.')
    if len(rs) == 2:
        a, b = rs
        print(f'\n★★ 대조  H/R {a["HR"]:.3f} → {b["HR"]:.3f} = ×{b["HR"]/a["HR"]:.2f}'
              f'   ·  R ×{b["R"]/a["R"]:.2f}  ·  H ×{b["H"]/a["H"]:.2f}  ·  φ ×{b["phi"]/a["phi"]:.2f}')


def _selftest():
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        (globals().__setitem__('_', 0), ok := ok + 1) if cond else fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    with tempfile.TemporaryDirectory() as td:
        def write(step, pts, r=0.0015):
            p = os.path.join(td, f'b_{step}.liggghts')
            with open(p, 'w') as fh:
                fh.write('ITEM: TIMESTEP\n%d\nITEM: NUMBER OF ATOMS\n%d\n' % (step, len(pts)))
                fh.write('ITEM: BOX BOUNDS mm mm mm\n-1 1\n-1 1\n0 1\n')
                fh.write('ITEM: ATOMS id type x y z radius\n')
                for i, (X, Y, Z) in enumerate(pts):
                    fh.write(f'{i+1} 1 {X} {Y} {Z} {r}\n')
            return p
        write(9600, [(0, 0, 0)])
        write(249600, [(0.01, 0, 0.001), (-0.01, 0, 0.002), (0, 0.02, 0.003)])
        fr = frames(td)
        chk('① 프레임을 숫자순으로 고른다 (_9600 이 _249600 뒤가 아니다)',
            fr[-1][0] == 249600)
        m = measure(td)
        chk('② 마지막 프레임의 n 을 읽는다 (3)', m['n'] == 3)
        chk('③ R 은 실린더 축(0,0) 기준이다',
            abs(m['R'] - 0.02) < 2e-3)
        #  ★ 변이 대조 — 사전순으로 고르면 n 이 1 이 된다 (시험이 장식이 아님을 보인다)
        lex = sorted(glob.glob(os.path.join(td, '*')))[-1]
        chk('④ 변이: 사전순으로 고르면 틀린 프레임이 잡힌다',
            STEP_RE.search(os.path.basename(lex)).group(1) == '9600')
        #  ⑤ 느슨한 침대는 경고 대상
        chk('⑤ 느슨한 침대(φ 낮음)를 경고 문턱 아래로 잡는다', m['phi'] < PHI_LOOSE_WARN)
        #  ★ 다분산 — 큰 입자 하나가 부피를 지배해야 한다 (평균반경 쓰면 못 잡는다)
        #  ⚠ **제 디렉터리에 둔다** — 같은 td 에 두면 measure() 가 숫자순 마지막인
        #     249600 을 골라 이 고정구를 아예 안 읽는다 (초판이 그래서 통과 못 했다).
        with tempfile.TemporaryDirectory() as tp:
            with open(os.path.join(tp, 'poly_100.liggghts'), 'w') as fh:
                fh.write('ITEM: TIMESTEP\n100\nITEM: NUMBER OF ATOMS\n3\n')
                fh.write('ITEM: BOX BOUNDS mm mm mm\n-1 1\n-1 1\n0 1\n')
                fh.write('ITEM: ATOMS id type x y z radius\n')
                fh.write('1 1 0.01 0 0.001 0.005\n2 2 -0.01 0 0.002 0.0005\n'
                         '3 2 0 0.01 0.003 0.0005\n')
            mp = measure(tp)
            env = np.pi * mp['R'] ** 2 * mp['H']        # 포락 부피 (공유 분모)
            v_got = mp['phi'] * env                     # 도구가 실제로 쓴 고체 부피
            v_true = (4/3)*np.pi*(0.005**3 + 2*0.0005**3)
            v_mean = 3*(4/3)*np.pi*((0.005+0.0005+0.0005)/3)**3
            chk('⑥ 다분산 부피를 입자별로 더한다 (참값과 일치)',
                abs(v_got - v_true) < v_true*1e-9)
            #  ★ 변이 대조 — 평균반경 판이면 여기서 걸린다 (시험이 장식이 아님을 보인다)
            chk(f'⑥b 변이: 평균반경 판(n·(4/3)π r̄³)과 {v_true/v_mean:.1f}배 다르다',
                abs(v_got - v_mean) > v_mean*0.5)

        #  ⑧ 다중 프레임 평균 — 회전 침대는 한 장으로 재면 안 된다
        with tempfile.TemporaryDirectory() as tm:
            for k, st in enumerate((100, 200, 300)):
                with open(os.path.join(tm, f'r_{st}.liggghts'), 'w') as fh:
                    fh.write(f'ITEM: TIMESTEP\n{st}\nITEM: NUMBER OF ATOMS\n2\n')
                    fh.write('ITEM: BOX BOUNDS mm mm mm\n-1 1\n-1 1\n0 1\n')
                    fh.write('ITEM: ATOMS id type x y z radius\n')
                    #  H 를 프레임마다 바꾼다 (1·2·3 mm) → 평균 2 mm
                    fh.write(f'1 1 0.01 0 0 0.0005\n2 1 0.01 0 {0.001*(k+1)} 0.0005\n')
            mm = measure_many(tm, last=3)
            m1 = measure_many(tm, last=1)
            chk(f'⑧ 마지막 3 프레임을 평균한다 (H {mm["H"]*1e3:.2f} mm = 1·2·3 의 평균)',
                abs(mm['H'] - 0.002) < 1e-9 and mm['n_used'] == 3)
            chk(f'⑧b 산포를 같이 낸다 (sd {mm["H_sd"]*1e3:.2f} mm)', mm['H_sd'] > 0)
            chk('⑧c 변이: last=1 이면 마지막 프레임만 (3 mm)',
                abs(m1['H'] - 0.003) < 1e-9 and m1['H_sd'] == 0.0)

        #  ⑦ 통축 — 가로 드럼에서 두 규약이 **실제로 갈린다**
        #     고정구: 축(x) 으로 길고 측방(y) 으로 좁은 침대 = 드럼 바닥의 풀
        #     axis='z' → R = pct99(√(x²+y²)) 가 드럼 **길이**를 먹어 크게 나온다
        #     axis='x' → R = pct99(|y|)       = 진짜 측방 퍼짐
        with tempfile.TemporaryDirectory() as tx:
            with open(os.path.join(tx, 'drum_10.liggghts'), 'w') as fh:
                pts = [(X*0.001, Y*0.001, 0.001) for X in range(-30, 31, 2)
                       for Y in (-2, 0, 2)]
                fh.write(f'ITEM: TIMESTEP\n10\nITEM: NUMBER OF ATOMS\n{len(pts)}\n')
                fh.write('ITEM: BOX BOUNDS mm mm mm\n-1 1\n-1 1\n0 1\n')
                fh.write('ITEM: ATOMS id type x y z radius\n')
                for i, (X, Y, Z) in enumerate(pts):
                    fh.write(f'{i+1} 1 {X} {Y} {Z+i*1e-6} 0.0005\n')
            mz = measure(tx, axis='z')
            mx = measure(tx, axis='x')
            chk('⑦ axis=x 는 측방 퍼짐 |y| 만 본다 (2 mm)',
                abs(mx['R'] - 0.002) < 1e-4)
            chk('⑦b 변이: axis=z 는 드럼 길이(x)를 먹어 10배 넘게 크다',
                mz['R'] > mx['R'] * 10)
    print(f'\nmeasure_bed_aspect selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dirs', nargs='*', help='덤프 디렉터리 (여러 개면 나란히 비교)')
    ap.add_argument('--r-container', type=float, default=0.05, help='통 반경 (m). 기본 0.05')
    ap.add_argument('--label', action='append', default=None, help='디렉터리별 표시 이름')
    ap.add_argument('--last', type=int, default=1,
                    help='마지막 N 프레임 평균 ± sd.  ★ 회전 중이면 한 바퀴 분량을 줄 것')
    ap.add_argument('--axis', default='z', choices=['x', 'y', 'z'],
                    help='통의 대칭축 (중력은 언제나 −z).  가로 드럼이면 x.  기본 z')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.dirs:
        ap.error('디렉터리를 하나 이상 주세요 (예: nocoh/post coh/post)')
    labs = a.label or [None] * len(a.dirs)
    report([measure_many(d, a.r_container, labs[i] if i < len(labs) else None,
                         axis=a.axis, last=a.last)
            for i, d in enumerate(a.dirs)])

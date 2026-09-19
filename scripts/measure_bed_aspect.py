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


def measure(d, r_container=0.05, label=None):
    fr = frames(d)
    if not fr:
        raise SystemExit(f'⛔ {d}: 번호 붙은 덤프가 없다')
    step, path = fr[-1]                                 # ★ 숫자순 마지막
    D = read_dump(path)
    if 'radius' not in D:
        raise SystemExit(f'⛔ {path}: radius 열이 없다 — 덤프에 radius 를 넣을 것')
    x, y, z, r = D['x'], D['y'], D['z'], D['radius']
    n = len(x)
    rad = np.hypot(x, y)                                # ★ 실린더 축(0,0) 기준
    R99 = float(np.percentile(rad, 99))                 # 튄 입자가 최댓값을 지배하지 않도록
    H = float(z.max() - z.min())
    Vp = n * (4 / 3) * np.pi * float(r.mean()) ** 3
    phi = Vp / (np.pi * R99 ** 2 * H) if (R99 > 0 and H > 0) else float('nan')
    return dict(label=label or d, step=step, n=n, R=R99, H=H,
                HR=(H / R99 if R99 > 0 else float('nan')),
                R_over_Rc=(R99 / r_container if r_container else float('nan')),
                phi=phi, n_frames=len(fr), path=path)


def report(rs):
    for m in rs:
        print(f'{m["label"]:14s} step {m["step"]:7d} · n {m["n"]:5d} · 프레임 {m["n_frames"]}')
        print(f'   R(99%) {m["R"]*1e3:7.2f} mm · H {m["H"]*1e3:7.2f} mm · ★ H/R {m["HR"]:6.3f}'
              f' · R/R_통 {m["R_over_Rc"]:5.3f} · φ(포락) {m["phi"]:5.3f}')
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
    print(f'\nmeasure_bed_aspect selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dirs', nargs='*', help='덤프 디렉터리 (여러 개면 나란히 비교)')
    ap.add_argument('--r-container', type=float, default=0.05, help='통 반경 (m). 기본 0.05')
    ap.add_argument('--label', action='append', default=None, help='디렉터리별 표시 이름')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.dirs:
        ap.error('디렉터리를 하나 이상 주세요 (예: nocoh/post coh/post)')
    labs = a.label or [None] * len(a.dirs)
    report([measure(d, a.r_container, labs[i] if i < len(labs) else None)
            for i, d in enumerate(a.dirs)])

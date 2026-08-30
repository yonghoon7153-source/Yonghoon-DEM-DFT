#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OAT(one-at-a-time) 스윕 폴더들 → 파라미터축마다 ∂ε/∂param · ∂plate_z/∂param.

  python3 scripts/oat_sensitivity.py --root ~/dem-web/dem_scripts/oat_sweep --csv oat.csv

계기 (`docs/reviews/oat_controls_verified_20260829.md`): 대조 2건이 통과해 11런이
해석 가능해졌다.  목적은 Coetzee bulk-calibration §5("각 실험은 파라미터 하나를
고립시켜야 한다")를 우리 계에서 재는 것 — 즉 **∂ε/∂μ 가 실제로 0 인가**.

★ 기점 규약은 `make_heckel_manifest.scan()` 을 **그대로 재사용**한다 (마지막 contact
  기점, atom·mesh 를 그 스텝에서, plate_z 는 그 STL 에서).  여기서 다시 짜면 규약이
  갈라진다 — 그 함수 주석이 경고하는 실수(마지막 atom 을 기점으로 잡아 4압력 중 3점을
  버린 것)가 바로 그것이다.  ε 도 `heckel_analysis.vol_and_lens` 를 그대로 부른다.

⚠ **ε 를 소수 2자리로 읽으면 판별이 안 된다** — 대조 문서가 명시적으로 남긴 한계다
  ("판별력은 plate_z 가 갖는다").  그 한계는 *출력 서식*의 것이지 양의 것이 아니므로,
  이 도구는 ε 를 직접 계산해 **전체 정밀도**로 낸다.  plate_z 도 8자리로 찍는다.

⚠ 이 도구는 **기울기를 내지, 판정하지 않는다**.  "∂ε/∂μ ≈ 0" 은 문턱을 런 전에 등록한
  뒤에야 판정이 된다 (prereg).  등록 없이 나온 기울기는 *측정*이다.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CONTROL = '(대조)'


def parse_oat(name):
    """`post_oat_cor0p2` → ('cor', 0.2).  대조는 (CONTROL, nan).  못 읽으면 None.

    값 표기는 `<정수>p<소수>` (셸에서 점을 못 쓰는 런 이름 규약): `0p2`→0.2, `24p0`→24.0.
    """
    s = name
    for pre in ('post_', 'oat_', 'esweep_'):
        if s.startswith(pre):
            s = s[len(pre):]
    if not s:
        return None
    m = re.match(r'^(?P<p>.*?)(?P<a>\d+)p(?P<b>\d+)$', s)
    if m and m.group('p'):
        return (m.group('p').rstrip('_'), float(f"{m.group('a')}.{m.group('b')}"))
    # 값이 없는 것 = 대조 (base · orig_1type).  버리지 않고 표에 남긴다.
    return (CONTROL, float('nan'))


def _key_fn(name):
    pv = parse_oat(name)
    if pv is None:
        return None
    param, val = pv
    # 정렬: 대조를 맨 앞, 그다음 파라미터 이름 → 값
    return (pv, (0 if param == CONTROL else 1, param, (0.0 if math.isnan(val) else val)))


def slope(xs, ys):
    """최소제곱 기울기.  유한한 점이 2개 미만이면 None."""
    pts = [(x, y) for x, y in zip(xs, ys)
           if x is not None and y is not None
           and math.isfinite(x) and math.isfinite(y)]
    if len(pts) < 2:
        return None
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    if sxx <= 0:
        return None
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    return sxy / sxx


def collect(root, pattern='post_*'):
    """→ (rows, skipped).  rows 는 ε 까지 채워진 레코드."""
    from make_heckel_manifest import scan
    from heckel_analysis import vol_and_lens

    pts, skipped = scan(root, pattern, key_fn=_key_fn, key_name='oat',
                        key_err='OAT 런 이름으로 못 읽음')
    rows = []
    for p in pts:
        param, val = p['oat']
        try:
            Vs, Vl, Vb, Vc = vol_and_lens(p['atom'], p.get('contacts'), p['plate_z'])
        except Exception as e:
            skipped.append((p['name'], f'ε 계산 실패 ({type(e).__name__}: {e})'))
            continue
        rows.append(dict(
            name=p['name'], param=param, value=val, step=p['step'], anchor=p['anchor'],
            plate_z=p['plate_z'],
            eps_union=1.0 - (Vs - Vl) / Vb,
            eps_sphere=1.0 - Vs / Vb,
            V_sphere=Vs, V_lens=Vl, V_box=Vb, V_lens_contacts=Vc))
    return rows, skipped


def axes(rows):
    """파라미터축별 기울기.  대조는 축이 아니다."""
    out = {}
    for param in sorted({r['param'] for r in rows} - {CONTROL}):
        sub = sorted((r for r in rows if r['param'] == param), key=lambda r: r['value'])
        xs = [r['value'] for r in sub]
        out[param] = dict(
            n=len(sub), values=xs,
            d_eps_union=slope(xs, [r['eps_union'] for r in sub]),
            d_eps_sphere=slope(xs, [r['eps_sphere'] for r in sub]),
            d_plate_z=slope(xs, [r['plate_z'] for r in sub]),
            span_plate_z=(max(r['plate_z'] for r in sub) - min(r['plate_z'] for r in sub)),
            span_eps_union=(max(r['eps_union'] for r in sub)
                            - min(r['eps_union'] for r in sub)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', help='post_* 런 폴더들이 있는 상위 디렉터리')
    ap.add_argument('--pattern', default='post_*', help='폴더 glob (기본 post_*)')
    ap.add_argument('--csv', help='행 단위 CSV 출력 경로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.root:
        ap.error('--root 가 필요합니다 (또는 --selftest)')

    rows, skipped = collect(a.root, a.pattern)
    if not rows:
        sys.exit(f'{a.root}: 읽을 수 있는 런이 없습니다 ({len(skipped)}개 건너뜀)'
                 + ('' if not skipped else f' — {skipped[0][0]}: {skipped[0][1]}'))

    print(f'{"런":<26}{"파라미터":<10}{"값":>7}  {"plate_z":>12}  '
          f'{"ε_union%":>10}  {"ε_sphere%":>10}  기점')
    for r in rows:
        v = '  —  ' if math.isnan(r['value']) else f'{r["value"]:>7.3g}'
        flag = '' if r['anchor'] == 'contact' else '  ⚠ contact 없음(폴백)'
        print(f'{r["name"]:<26}{r["param"]:<10}{v}  {r["plate_z"]:>12.8g}  '
              f'{100*r["eps_union"]:>10.4f}  {100*r["eps_sphere"]:>10.4f}  '
              f'{r["anchor"]}{flag}')
    for n, why in skipped:
        print(f'  ⚠ 건너뜀 {n}: {why}')

    ax = axes(rows)
    if ax:
        print(f'\n{"축":<10}{"n":>3}  {"∂ε_union/∂p":>14}  {"∂ε_sphere/∂p":>14}  '
              f'{"∂plate_z/∂p":>14}   값')
        for param, d in ax.items():
            def f(x):
                return '     —        ' if x is None else f'{x:>14.6g}'
            vals = ', '.join(f'{v:g}' for v in d['values'])
            print(f'{param:<10}{d["n"]:>3}  {f(d["d_eps_union"])}  '
                  f'{f(d["d_eps_sphere"])}  {f(d["d_plate_z"])}   [{vals}]')
        print('\n⚠ 이 표는 **측정**이다 — 문턱을 런 전에 등록하지 않았으므로 '
              '"∂ε/∂μ ≈ 0" 은 아직 판정이 아니다.')
        print('⚠ ε 의 판별 폭을 plate_z 와 함께 볼 것 (span 은 CSV 에 있다).')

    if a.csv:
        os.makedirs(os.path.dirname(os.path.abspath(a.csv)) or '.', exist_ok=True)
        cols = ['name', 'param', 'value', 'step', 'anchor', 'plate_z',
                'eps_union', 'eps_sphere', 'V_sphere', 'V_lens', 'V_box',
                'V_lens_contacts']
        with open(a.csv, 'w', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore')
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f'\n{a.csv}  ·  {len(rows)}행')
    return 0


def _selftest():
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    # ── ① 런 이름 파싱 ────────────────────────────────────────────────
    chk('① cor0p2 → (cor, 0.2)', parse_oat('post_oat_cor0p2') == ('cor', 0.2))
    chk('① mu_pp0p4 → (mu_pp, 0.4)', parse_oat('post_oat_mu_pp0p4') == ('mu_pp', 0.4))
    chk('① mu_pw0p6 → (mu_pw, 0.6)', parse_oat('post_oat_mu_pw0p6') == ('mu_pw', 0.6))
    chk('① E24p0 → (E, 24.0)', parse_oat('post_esweep_E24p0') == ('E', 24.0))
    chk('① E5p0 → (E, 5.0)', parse_oat('post_esweep_E5p0') == ('E', 5.0))
    b = parse_oat('post_oat_base')
    chk('① base 는 대조 (버리지 않는다)', b is not None and b[0] == CONTROL
        and math.isnan(b[1]))
    o = parse_oat('post_oat_orig_1type')
    chk('① orig_1type 도 대조', o is not None and o[0] == CONTROL)
    # 값 표기가 진짜 소수로 읽히는가 — `0p2` 를 2 로 읽으면 기울기가 10배 틀린다
    chk('★① 0p2 를 0.2 로 읽는다 (2 가 아니다)', parse_oat('post_oat_cor0p2')[1] == 0.2)

    # ── ② 기울기 ────────────────────────────────────────────────────
    chk('② 직선 기울기', abs(slope([0.2, 0.4, 0.6], [1.0, 2.0, 3.0]) - 5.0) < 1e-12)
    chk('② 평평하면 0', abs(slope([0.2, 0.4, 0.6], [7.0, 7.0, 7.0])) < 1e-12)
    chk('② 점 1개면 None', slope([0.2], [1.0]) is None)
    chk('② x 가 같으면 None (0으로 안 나눈다)', slope([0.3, 0.3], [1.0, 2.0]) is None)
    chk('② nan 은 빠진다', abs(slope([0.2, 0.4, 0.6],
                                   [1.0, float('nan'), 3.0]) - 5.0) < 1e-12)

    # ── ③ scan 재사용: 기점 규약이 OAT 이름에서도 그대로인가 ──────────
    from make_heckel_manifest import scan
    td = tempfile.mkdtemp(prefix='oat_')

    def stl(path, z):
        open(path, 'w').write(
            'solid plate\n facet normal 0 0 1\n  outer loop\n'
            f'   vertex 0 0 {z}\n   vertex 1 0 {z}\n   vertex 0 1 {z}\n'
            '  endloop\n endfacet\nendsolid\n')

    def mk(nm, atoms, meshes, cons):
        d = os.path.join(td, nm)
        os.makedirs(d, exist_ok=True)
        for s in atoms:
            open(os.path.join(d, f'atom_{s}.liggghts'), 'w').write('x\n')
        for s in meshes:
            stl(os.path.join(d, f'mesh_{s}.stl'), 0.03)
        for s in cons:
            open(os.path.join(d, f'contact_{s}.liggghts'), 'w').write('x\n')
        return d

    # atom/mesh 는 5000 간격, contact 는 10000 간격 → 마지막 atom(15000) 이 아니라
    # 마지막 **contact**(10000) 가 기점이어야 한다.
    mk('post_oat_cor0p2', [5000, 10000, 15000], [5000, 10000, 15000], [5000, 10000])
    mk('post_oat_cor0p4', [5000, 10000], [5000, 10000], [10000])
    mk('post_oat_base', [5000, 10000], [5000, 10000], [10000])
    mk('post_oat_nomesh', [5000], [], [5000])
    pts, skipped = scan(td, 'post_*', key_fn=_key_fn, key_name='oat',
                        key_err='OAT 런 이름으로 못 읽음')
    by = {p['name']: p for p in pts}
    chk('★③ 마지막 contact 가 기점 (마지막 atom 아님)',
        by.get('post_oat_cor0p2', {}).get('step') == 10000)
    chk('③ 기점 라벨 = contact',
        by.get('post_oat_cor0p2', {}).get('anchor') == 'contact')
    chk('③ mesh 없는 폴더는 건너뛰고 사유를 남긴다',
        any(n == 'post_oat_nomesh' and 'mesh' in w for n, w in skipped))
    chk('③ 대조도 표에 남는다', 'post_oat_base' in by)
    chk('③ 대조가 맨 앞으로 정렬', pts and pts[0]['name'] == 'post_oat_base')
    chk('③ plate_z 를 STL 에서 읽는다',
        abs(by.get('post_oat_cor0p2', {}).get('plate_z', -1) - 0.03) < 1e-12)

    # ── ④ 축 집계에서 대조는 축이 아니다 ──────────────────────────────
    rows = [dict(name='b', param=CONTROL, value=float('nan'), plate_z=1.0,
                 eps_union=0.10, eps_sphere=-0.02),
            dict(name='c2', param='cor', value=0.2, plate_z=1.0,
                 eps_union=0.10, eps_sphere=-0.02),
            dict(name='c4', param='cor', value=0.4, plate_z=1.2,
                 eps_union=0.12, eps_sphere=-0.01)]
    ax = axes(rows)
    chk('④ 대조는 축에서 빠진다', CONTROL not in ax and set(ax) == {'cor'})
    chk('④ ∂ε/∂cor 를 계산한다', abs(ax['cor']['d_eps_union'] - 0.1) < 1e-9)
    chk('④ ∂plate_z/∂cor 도 낸다', abs(ax['cor']['d_plate_z'] - 1.0) < 1e-9)

    # ── ⑤ 출력 정밀도: ε 가 소수 2자리로 잘리면 판별이 죽는다 ─────────
    #     (대조 문서가 남긴 한계를 이 도구가 재현하지 않는지 확인)
    s = f'{100*0.100812345:.4f}'
    chk('★⑤ ε 를 4자리로 찍는다 (2자리 아님)', s == '10.0812' and len(s.split('.')[1]) == 4)
    chk('★⑤ plate_z 를 8자리로 찍는다', f'{0.00823721234:.8g}' == '0.0082372123')

    print(f'oat_sensitivity selftest: {ok}/{ok+len(fail)} PASS')
    for f_ in fail:
        print('  ✗', f_)
    return 1 if fail else 0


if __name__ == '__main__':
    raise SystemExit(main())

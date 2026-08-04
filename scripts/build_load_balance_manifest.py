#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MPM 킷 폴더들 → `am_load_balance_jam.py --cases` 매니페스트.

킷 하나(`mpm_input_from_case.py --out <dir>` 산출물)에는 판정에 필요한 게 이미 다 있다:
  am_scaffold.csv · se_scaffold.csv · mpm_input.json(press_gpa, dem_thickness_um)
그걸 그대로 긁어 매니페스트 한 장으로 만든다.  손으로 옮겨 적다 두께/압력을 어긋나게
붙이는 사고를 막는 것이 이 스크립트의 존재 이유다.

  # 케이스별 킷 만들기 (케이스마다 한 번)
  python3 scripts/mpm_input_from_case.py --results webapp/results/<cid> --out kits/<cid>
  # 킷들 → 매니페스트 → 판정
  python3 scripts/build_load_balance_manifest.py --kits kits --out kits/cases.csv
  python3 scripts/am_load_balance_jam.py --cases kits/cases.csv

★ 압력이 모두 같으면 이것은 **조성 축** 검증이다 (같은 300 MPa 에서 조성만 다른 베드들이
  하나의 H_AM 으로 설명되는가).  압력 축은 `make_pressure_sweep_decks.py` 로 만든
  다압력 DEM 런이 있어야 열린다 — 판정기가 그 단서를 함께 찍는다.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import sys


def scan_kit(d):
    """킷 폴더 하나 → 매니페스트 행 (부족하면 사유와 함께 None)."""
    am = os.path.join(d, 'am_scaffold.csv')
    se = os.path.join(d, 'se_scaffold.csv')
    pj = os.path.join(d, 'mpm_input.json')
    for p in (am, se, pj):
        if not os.path.exists(p):
            return None, f'{os.path.basename(p)} 없음'
    try:
        j = json.load(open(pj))
    except Exception as e:
        return None, f'mpm_input.json 파싱 실패 ({type(e).__name__})'
    h = j.get('dem_thickness_um')
    p = j.get('press_gpa')
    if not h or float(h) <= 0:
        return None, 'dem_thickness_um 없음/0 — DEM 두께 없이는 역산 불가'
    if not p or float(p) <= 0:
        return None, 'press_gpa 없음/0'
    # 경로는 절대경로로 담고, 매니페스트를 쓸 때 그 파일 위치 기준 상대경로로 바꾼다
    # (킷 위치와 매니페스트 위치가 다를 수 있으므로 여기서 상대화하면 어긋난다)
    return dict(label=(j.get('case') or os.path.basename(d.rstrip('/')))[:24],
                p_gpa=float(p), am_csv=os.path.abspath(am), se_csv=os.path.abspath(se),
                h_dem_um=round(float(h), 4)), ''


def build(kits_dir, out_path):
    rows, skipped = [], []
    for d in sorted(glob.glob(os.path.join(kits_dir, '*'))):
        if not os.path.isdir(d):
            continue
        r, why = scan_kit(d)
        (rows.append(r) if r else skipped.append((os.path.basename(d), why)))
    if not rows:
        sys.exit(f'{kits_dir}: 쓸 수 있는 킷이 없습니다 '
                 f'(건너뜀 {len(skipped)}개){"" if not skipped else " — " + skipped[0][1]}')
    # 매니페스트의 상대경로는 **매니페스트 위치** 기준으로 해석되므로 거기에 맞춰 상대화한다
    base = os.path.dirname(os.path.abspath(out_path))
    for r in rows:
        for k in ('am_csv', 'se_csv'):
            r[k] = os.path.relpath(r[k], base)
    with open(out_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['label', 'p_gpa', 'am_csv', 'se_csv', 'h_dem_um'])
        w.writeheader()
        w.writerows(rows)
    return rows, skipped


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--kits', help='킷 폴더들이 들어있는 상위 디렉터리')
    ap.add_argument('--out', default='cases.csv', help='매니페스트 출력 경로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.kits:
        ap.error('--kits 가 필요합니다 (또는 --selftest)')

    rows, skipped = build(a.kits, a.out)
    ps = sorted({r['p_gpa'] for r in rows})
    print(f'매니페스트 {a.out}  ·  케이스 {len(rows)}개  ·  압력 {len(ps)}종 '
          f'({", ".join(f"{p:g}" for p in ps)} GPa)')
    for r in rows[:10]:
        print(f'  {r["label"]:>24}  P={r["p_gpa"]:.3f} GPa  h_DEM={r["h_dem_um"]:.2f} µm')
    if len(rows) > 10:
        print(f'  … 외 {len(rows) - 10}개')
    for n, why in skipped:
        print(f'  ⚠ 건너뜀 {n}: {why}')
    if len(ps) == 1:
        print(f'\n  ⚠ 압력이 {ps[0]:g} GPa 한 종류 → **조성 축 검증만** 됩니다.  '
              f'Heckel(압력 축)을\n     주장하려면 같은 베드의 다압력 DEM 런이 필요합니다 '
              f'(make_pressure_sweep_decks.py).')
    print(f'\n다음: python3 scripts/am_load_balance_jam.py --cases {a.out}')
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

    td = tempfile.mkdtemp(prefix='blm_')
    kits = os.path.join(td, 'kits')

    def kit(name, **j):
        d = os.path.join(kits, name)
        os.makedirs(d, exist_ok=True)
        for f in ('am_scaffold.csv', 'se_scaffold.csv'):
            if j.pop(f, True):
                open(os.path.join(d, f), 'w').write('1,0,0,0.03,0.006\n')
        if j.pop('_nojson', False):
            return d
        json.dump(j, open(os.path.join(d, 'mpm_input.json'), 'w'))
        return d

    kit('caseA', case='input_A', press_gpa=0.30, dem_thickness_um=30.28)
    kit('caseB', case='input_B', press_gpa=0.30, dem_thickness_um=27.5)
    kit('bad_nojson', _nojson=True)
    kit('bad_noh', case='input_C', press_gpa=0.30)                     # 두께 없음
    kit('bad_zeroh', case='input_D', press_gpa=0.30, dem_thickness_um=0)

    out = os.path.join(td, 'cases.csv')
    rows, skipped = build(kits, out)
    chk('멀쩡한 킷만 실린다', len(rows) == 2)
    chk('두께 없는 킷은 사유와 함께 건너뛴다',
        any(n == 'bad_noh' and '두께' in w for n, w in skipped))
    chk('두께 0 도 거른다 (0 이면 역산이 발산)', any(n == 'bad_zeroh' for n, _ in skipped))
    chk('json 없는 폴더도 거른다', any(n == 'bad_nojson' for n, _ in skipped))
    chk('label 은 case id 를 쓴다', {r['label'] for r in rows} == {'input_A', 'input_B'})

    # ★ 판정기가 실제로 읽히는지 — 경로 해석이 어긋나면 여기서 죽는다
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import am_load_balance_jam as albj
    cases = albj.read_cases(out)
    chk('판정기가 매니페스트를 읽는다', len(cases) == 2)
    chk('상대경로가 실제 파일로 풀린다', all(os.path.exists(c['am']) for c in cases))
    chk('압력·두께가 킷에서 그대로 전달', abs(cases[0]['p'] - 0.30) < 1e-12
        and abs(cases[0]['h_dem'] - 30.28) < 1e-9)

    # 매니페스트를 다른 위치에 써도 경로가 살아있어야 한다 (킷 폴더 이동 내성)
    sub = os.path.join(td, 'deeper')
    os.makedirs(sub, exist_ok=True)
    out2 = os.path.join(sub, 'cases.csv')
    build(kits, out2)
    chk('다른 위치에 쓴 매니페스트의 상대경로도 유효',
        all(os.path.exists(c['am']) for c in albj.read_cases(out2)))

    print(f'selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 0 if not fail else 1


if __name__ == '__main__':
    sys.exit(main())

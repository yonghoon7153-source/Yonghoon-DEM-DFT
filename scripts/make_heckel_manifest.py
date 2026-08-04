#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`post_SE_heckel_<P>/` 덤프 폴더들 → `heckel_analysis.py` 가 먹는 manifest.json.

heckel_analysis.py 는 압력마다 (atom 덤프 · contact 덤프 · plate_z) 를 요구하는데,
그 셋을 손으로 골라 JSON 에 옮겨 적는 일이 사고 지점이다 — **마지막 타임스텝**을 골라야
하고(중간 스냅샷을 집으면 압밀 도중 상태), plate_z 는 같은 타임스텝의 mesh STL 에서
읽어야 한다(다른 프레임 걸 쓰면 두께가 어긋난다).  그걸 자동화한다.

  python3 scripts/make_heckel_manifest.py --root "/mnt/f/.../post_SE" --out heckel/manifest.json
  python3 scripts/heckel_analysis.py heckel/manifest.json

폴더 이름에서 압력을 읽는다 (`post_SE_heckel_300` → 300 MPa).  atom/mesh 는 **같은
타임스텝**을 짝지어 고르고, 못 맞추면 그 압력을 넣지 않고 사유를 찍는다 (조용히 빼면
Heckel 이 3점 fit 이 된 걸 모른다).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import struct
import sys


def _step(path):
    m = re.search(r'_(\d+)\.(?:liggghts|stl)$', os.path.basename(path))
    return int(m.group(1)) if m else -1


def plate_z_from_stl(path):
    """평판 메시 STL 의 z (ASCII/바이너리 모두).  평판이므로 정점 z 의 최솟값 = 접촉면."""
    with open(path, 'rb') as f:
        head = f.read(512)
    if head.lstrip()[:5].lower() == b'solid' and b'facet' in head:
        zs = [float(l.split()[3]) for l in open(path, errors='ignore')
              if l.strip().startswith('vertex')]
    else:                                            # 바이너리 STL
        with open(path, 'rb') as f:
            f.read(80)
            n = struct.unpack('<I', f.read(4))[0]
            zs = []
            for _ in range(n):
                d = f.read(50)
                if len(d) < 50:
                    break
                v = struct.unpack('<12fH', d)
                zs += [v[3 + 3 * k + 2] for k in range(3)]
    if not zs:
        raise ValueError(f'{path}: 정점을 못 읽음')
    return min(zs)


def scan(root, pattern='post_SE_heckel_*'):
    pts, skipped = [], []
    for d in sorted(glob.glob(os.path.join(root, pattern))):
        if not os.path.isdir(d):
            continue
        m = re.search(r'_(\d+)\s*$', os.path.basename(d))
        if not m:
            skipped.append((os.path.basename(d), '폴더 이름에서 압력을 못 읽음'))
            continue
        p_mpa = int(m.group(1))
        atoms = sorted(glob.glob(os.path.join(d, 'atom_*.liggghts')), key=_step)
        meshes = sorted(glob.glob(os.path.join(d, 'mesh_*.stl')), key=_step)
        cons = sorted(glob.glob(os.path.join(d, 'contact_*.liggghts')), key=_step)
        if not atoms:
            skipped.append((os.path.basename(d), 'atom 덤프 없음'))
            continue
        if not meshes:
            skipped.append((os.path.basename(d), 'mesh STL 없음 → plate_z 불명'))
            continue
        # ★ atom 과 mesh 는 **같은 타임스텝** 이어야 한다.  공통 스텝 중 최대를 쓴다.
        common = sorted(set(map(_step, atoms)) & set(map(_step, meshes)))
        if not common:
            skipped.append((os.path.basename(d),
                            f'atom/mesh 타임스텝이 하나도 안 겹침 '
                            f'(atom max {_step(atoms[-1])}, mesh max {_step(meshes[-1])})'))
            continue
        st = common[-1]
        atom = next(a for a in atoms if _step(a) == st)
        mesh = next(x for x in meshes if _step(x) == st)
        try:
            pz = plate_z_from_stl(mesh)
        except Exception as e:
            skipped.append((os.path.basename(d), f'STL 파싱 실패 ({type(e).__name__})'))
            continue
        # contact 는 선택 (있으면 ε_union 이 계산된다) — 같은 스텝 것만 쓴다
        cc = [c for c in cons if _step(c) == st]
        pts.append(dict(P_MPa=p_mpa, plate_z=pz, atom=os.path.abspath(atom),
                        contacts=[os.path.abspath(c) for c in cc], step=st,
                        mesh=os.path.abspath(mesh)))
    return sorted(pts, key=lambda r: r['P_MPa']), skipped


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', help='post_SE_heckel_* 폴더들이 있는 상위 디렉터리')
    ap.add_argument('--pattern', default='post_SE_heckel_*', help='폴더 glob')
    ap.add_argument('--out', default='heckel/manifest.json')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.root:
        ap.error('--root 가 필요합니다 (또는 --selftest)')

    pts, skipped = scan(a.root, a.pattern)
    if not pts:
        sys.exit(f'{a.root}: 쓸 수 있는 압력점이 없습니다 ({len(skipped)}개 건너뜀)'
                 + ('' if not skipped else f' — {skipped[0][1]}'))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump([{k: v for k, v in p.items() if k in ('P_MPa', 'plate_z', 'atom', 'contacts')}
               for p in pts], open(a.out, 'w'), indent=2)
    print(f'{a.out}  ·  압력점 {len(pts)}개')
    for p in pts:
        print(f'  {p["P_MPa"]:>4} MPa  step={p["step"]:<9} plate_z={p["plate_z"]:.6g}  '
              f'contact {len(p["contacts"])}개'
              + ('' if p['contacts'] else '  ⚠ ε_union 계산 불가(ε_sphere 만)'))
    for n, why in skipped:
        print(f'  ⚠ 건너뜀 {n}: {why}')
    if len(pts) < 3:
        print(f'\n  ⚠ 압력점이 {len(pts)}개 — Heckel 직선성을 주장하기엔 부족합니다')
    print(f'\n다음: python3 scripts/heckel_analysis.py {a.out}')
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

    td = tempfile.mkdtemp(prefix='hm_')

    def stl(path, z):
        open(path, 'w').write(
            'solid plate\n facet normal 0 0 1\n  outer loop\n'
            f'   vertex 0 0 {z}\n   vertex 1 0 {z}\n   vertex 0 1 {z}\n'
            '  endloop\n endfacet\nendsolid\n')

    def mkdir_case(p, steps_atom, steps_mesh, steps_con=(), zmap=None):
        d = os.path.join(td, f'post_SE_heckel_{p}')
        os.makedirs(d, exist_ok=True)
        for s in steps_atom:
            open(os.path.join(d, f'atom_{s}.liggghts'), 'w').write('x\n')
        for s in steps_mesh:
            stl(os.path.join(d, f'mesh_{s}.stl'), (zmap or {}).get(s, 0.03))
        for s in steps_con:
            open(os.path.join(d, f'contact_{s}.liggghts'), 'w').write('x\n')
        return d

    mkdir_case(100, (500, 1000), (500, 1000), (1000,), {500: 0.05, 1000: 0.041})
    mkdir_case(300, (500, 2000), (500, 2000), (2000,), {500: 0.05, 2000: 0.033})
    mkdir_case(200, (700,), (900,))                       # 스텝 안 겹침 → 거부
    mkdir_case(400, (100,), ())                           # mesh 없음 → 거부

    pts, skipped = scan(td)
    chk('압력 오름차순 정렬', [p['P_MPa'] for p in pts] == [100, 300])
    chk('★ 마지막 타임스텝을 고른다 (중간 스냅샷 금지)',
        all(p['step'] in (1000, 2000) for p in pts))
    chk('plate_z 를 같은 스텝 STL 에서 읽는다',
        abs(pts[0]['plate_z'] - 0.041) < 1e-9 and abs(pts[1]['plate_z'] - 0.033) < 1e-9)
    chk('contact 도 같은 스텝만 붙인다', all(len(p['contacts']) == 1 for p in pts))
    chk('atom/mesh 스텝이 안 겹치면 거부 (두께 어긋남 차단)',
        any(n.endswith('_200') and '안 겹침' in w for n, w in skipped))
    chk('mesh 없으면 거부 (plate_z 불명)',
        any(n.endswith('_400') and 'mesh' in w for n, w in skipped))

    # 바이너리 STL 도 읽혀야 한다 (LIGGGHTS 빌드에 따라 갈린다)
    b = os.path.join(td, 'bin.stl')
    with open(b, 'wb') as f:
        f.write(b'\0' * 80 + struct.pack('<I', 1))
        f.write(struct.pack('<12fH', 0, 0, 1, 0, 0, 0.07, 1, 0, 0.07, 0, 1, 0.07, 0))
    chk('바이너리 STL 도 파싱', abs(plate_z_from_stl(b) - 0.07) < 1e-6)

    # 실제 heckel_analysis 가 읽는 스키마인지 (키 이름 오타 회귀 방지)
    need = {'P_MPa', 'plate_z', 'atom', 'contacts'}
    chk('manifest 스키마가 heckel_analysis 요구와 일치', need <= set(pts[0]))

    print(f'selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 0 if not fail else 1


if __name__ == '__main__':
    sys.exit(main())

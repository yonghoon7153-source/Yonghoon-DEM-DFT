#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`post_SE_heckel_<P>/` 덤프 폴더들 → `heckel_analysis.py` 가 먹는 manifest.json.

heckel_analysis.py 는 압력마다 (atom 덤프 · contact 덤프 · plate_z) 를 요구하는데,
그 셋을 손으로 골라 JSON 에 옮겨 적는 일이 사고 지점이다 — **마지막 타임스텝**을 골라야
하고(중간 스냅샷을 집으면 압밀 도중 상태), plate_z 는 같은 타임스텝의 mesh STL 에서
읽어야 한다(다른 프레임 걸 쓰면 두께가 어긋난다).  그걸 자동화한다.

  python3 scripts/make_heckel_manifest.py --root "/mnt/f/.../post_SE" --out heckel/manifest.json
  python3 scripts/heckel_analysis.py heckel/manifest.json

폴더 이름에서 압력을 읽는다 (`post_SE_heckel_300` → 300 MPa).

★★ 기점 규약 (2026-08-05 사용자 확인 — webapp 에 먹인 모든 케이스가 이 규약):
    **마지막 contact 파일**을 기점으로 삼고 atom·mesh 를 **그 스텝에서** 가져온다.
    덤프 간격이 다르다 (atom/mesh 5000 vs contact 10000) → "마지막 atom" 을 기점으로 잡으면
    contact 가 없는 스텝에 걸려 교차검증을 통째로 버린다 (실제로 4압력 중 3점을 그렇게 버렸다).
    contact 기점이면 세 파일이 **정확히 같은 순간**이고 기존 코퍼스와 같은 상태를 본다.
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


def pressure_key(name):
    """기본 색인: 폴더 이름 끝의 정수 = 압력(MPa).  → (색인값, 정렬키) 또는 None(건너뜀)."""
    m = re.search(r'_(\d+)\s*$', name)
    return None if not m else (int(m.group(1)), float(m.group(1)))


def scan(root, pattern='post_SE_heckel_*', key_fn=None, key_name='P_MPa',
         key_err='폴더 이름에서 압력을 못 읽음'):
    """덤프 폴더들 → 기점이 잡힌 레코드 목록.

    `key_fn`: 폴더 이름 → (색인값, 정렬키) 또는 None(=그 폴더는 건너뛴다).  기본 = 압력.
    ★ **색인만** 갈아끼우게 한 이유: 기점 선택·plate_z·건너뜀 사유는 축과 무관하게
      공유돼야 한다.  압력이 아닌 축(OAT 파라미터 등)을 재는 도구가 이 함수를 다시 짜면
      아래 contact-기점 규약이 조용히 갈라진다 — 이 파일이 이미 한 번 당한 실수다.
    """
    key_fn = key_fn or pressure_key
    pts, skipped = [], []
    for d in sorted(glob.glob(os.path.join(root, pattern))):
        if not os.path.isdir(d):
            continue
        kv = key_fn(os.path.basename(d))
        if kv is None:
            skipped.append((os.path.basename(d), key_err))
            continue
        keyval, sortkey = kv
        atoms = sorted(glob.glob(os.path.join(d, 'atom_*.liggghts')), key=_step)
        meshes = sorted(glob.glob(os.path.join(d, 'mesh_*.stl')), key=_step)
        cons = sorted(glob.glob(os.path.join(d, 'contact_*.liggghts')), key=_step)
        if not atoms:
            skipped.append((os.path.basename(d), 'atom 덤프 없음'))
            continue
        if not meshes:
            skipped.append((os.path.basename(d), 'mesh STL 없음 → plate_z 불명'))
            continue
        # ★★ 규약 (2026-08-05 사용자 확인, webapp 에 먹인 모든 케이스가 이 규약):
        #    **마지막 contact 파일을 기점**으로 삼고 atom·mesh 를 **그 스텝에서** 가져온다.
        #    덤프 간격이 다르므로(atom/mesh 5000 vs contact 10000) "마지막 atom" 을 기점으로
        #    잡으면 contact 가 없는 스텝에 걸린다 — 내가 처음 그렇게 짜서 4압력 중 3점의
        #    교차검증을 버렸다.  contact 기점이면 세 파일이 **정확히 같은 순간**이라 스텝차가
        #    아예 없고, 기존 코퍼스와도 같은 상태를 본다.
        a_steps, m_steps = set(map(_step, atoms)), set(map(_step, meshes))
        triple = sorted(set(map(_step, cons)) & a_steps & m_steps)
        if triple:
            st, anchor = triple[-1], 'contact'
        else:
            common = sorted(a_steps & m_steps)
            if not common:
                skipped.append((os.path.basename(d),
                                f'atom/mesh 타임스텝이 하나도 안 겹침 '
                                f'(atom max {_step(atoms[-1])}, mesh max {_step(meshes[-1])})'))
                continue
            st, anchor = common[-1], 'atom'      # contact 가 없는 폴더 → 폴백(플래그)
        atom = next(a for a in atoms if _step(a) == st)
        mesh = next(x for x in meshes if _step(x) == st)
        try:
            pz = plate_z_from_stl(mesh)
        except Exception as e:
            skipped.append((os.path.basename(d), f'STL 파싱 실패 ({type(e).__name__})'))
            continue
        cc = [c for c in cons if _step(c) == st]
        rec = dict(plate_z=pz, atom=os.path.abspath(atom),
                   contacts=[os.path.abspath(c) for c in cc], step=st, anchor=anchor,
                   name=os.path.basename(d),
                   last_atom_step=(max(a_steps) if a_steps else None),
                   n_contact_files=len(cons), mesh=os.path.abspath(mesh))
        rec[key_name] = keyval
        pts.append((sortkey, rec))
    return [r for _, r in sorted(pts, key=lambda t: t[0])], skipped


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
        la = p.get('last_atom_step')
        tag = f'기점={p["anchor"]}  contact {len(p["contacts"])}개'
        if p['anchor'] == 'contact' and la and la != p['step']:
            tag += f'  (마지막 atom 은 {la} — contact 기점 규약대로 {p["step"]} 사용)'
        if p['anchor'] != 'contact':
            tag += f'  ⚠ contact 파일 {p["n_contact_files"]}개 — 규약 밖 폴백, 교차검증 없음'
        print(f'  {p["P_MPa"]:>4} MPa  step={p["step"]:<9} plate_z={p["plate_z"]:.6g}  ' + tag)
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

    # ★★ 규약: **마지막 contact 기점** — atom/mesh 는 그 스텝에서.  덤프 간격이 다르므로
    #    (atom 5000 / contact 10000) 마지막 atom 을 기점으로 잡으면 contact 없는 스텝에 걸린다.
    d5 = os.path.join(td, 'post_SE_heckel_500')
    os.makedirs(d5, exist_ok=True)
    for s_ in (1450000, 1455000):
        open(os.path.join(d5, f'atom_{s_}.liggghts'), 'w').write('x\n')
        stl(os.path.join(d5, f'mesh_{s_}.stl'), 0.02 if s_ == 1450000 else 0.019)
    open(os.path.join(d5, 'contact_1450000.liggghts'), 'w').write('x\n')
    p5 = [r for r in scan(td)[0] if r['P_MPa'] == 500][0]
    chk('★ 마지막 contact 를 기점으로 삼는다 (마지막 atom 이 아니라)', p5['step'] == 1450000)
    chk('세 파일이 같은 스텝 → 교차검증 가능', len(p5['contacts']) == 1)
    chk('plate_z 도 기점 스텝의 mesh 에서 (다른 프레임 섞지 않는다)',
        abs(p5['plate_z'] - 0.02) < 1e-12)
    chk('마지막 atom 스텝을 기록해 규약 이탈을 눈에 보이게', p5['last_atom_step'] == 1455000)
    chk('기점 종류를 남긴다', p5['anchor'] == 'contact')

    # contact 가 아예 없는 폴더는 atom 기점 폴백 + 플래그
    d6 = os.path.join(td, 'post_SE_heckel_600')
    os.makedirs(d6, exist_ok=True)
    open(os.path.join(d6, 'atom_900.liggghts'), 'w').write('x\n')
    stl(os.path.join(d6, 'mesh_900.stl'), 0.015)
    p6 = [r for r in scan(td)[0] if r['P_MPa'] == 600][0]
    chk('contact 없으면 atom 기점 폴백 + 플래그', p6['anchor'] == 'atom' and not p6['contacts'])

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

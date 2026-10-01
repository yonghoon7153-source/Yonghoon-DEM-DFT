#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""atom 파일만 있는 케이스의 결과 페이지 회귀 — 2026-10-02 1저자 보고
(*"예전에는 파일 하나만 넣어도 다른건 안떠도 3d는 나오게 했었는데 그게 안되네"*).

atoms-only 모드 (`run_pipeline` 이 atom_*.liggghts 만 보고 3D 용 atoms.csv 만 만든다 · 04-24 부터) 의 결과 페이지
`/single/<id>` 가 **500** 이었다.  `single.html` 의 `_DEM_POR` (06-28 `afb9112e0` · MPM↔DEM 영역 표시) 가
`metrics.porosity` 를 읽는데 atoms-only 의 full_metrics 에는 그 키가 없어 Jinja `Undefined` 가 `tojson` 에서 죽고
페이지 전체가 내려간다 ⇒ 3D 뷰어가 붙을 자리가 없다.  3D 데이터 (`/3d-data`) 자체는 멀쩡했다.

  ① run_pipeline 이 atom 파일 하나로 atoms-only 성공을 낸다 (atoms.csv · full_metrics.has_contacts=False)
  ② 그 케이스의 결과 페이지가 200 이다
  ③ 페이지에 3D 데이터 경로가 붙고 `_DEM_POR` 은 null 이다 (값이 없으면 없다고 — 0 으로 채우지 않는다)
  ④ /3d-data 가 200 · 입자 수 = 덤프 원자 수 · atoms_only 표지
  ⑥ atom + 판 메시 STL 을 같이 올리면 /3d-data 에 판 삼각형이 실리고 3D 뷰어가 그린다
  ⑤ 공극률이 있는 케이스는 `_DEM_POR` 이 그대로다 — sphere-sum 우선, 없으면 porosity (영역 표시 동작 불변)
  ⑦ 3D 뷰어 — atom 만 올린 케이스도 상 이름이 전부 알려졌으면 상별 색 · 모르는 이름은 회색으로 그린다 (버리지 않는다)

  python3 webapp/test_atoms_only_viewer.py
"""
import json
import os
import random
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


COLS = 'id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke'


def write_dump(path, n2=6, n3=30, step=1, seed=7):
    """0:10 투입 덤프와 같은 모양 — 타입 2 (r 2 µm → sim 0.002) · 3 (r 0.5 µm → sim 0.0005) 만, 타입 1 없음."""
    rnd = random.Random(seed)
    rows = []
    for i in range(n2 + n3):
        t, r = (2, 0.002) if i < n2 else (3, 0.0005)
        rows.append(f'{i + 1} {t} {rnd.uniform(0.005, 0.045):.6g} {rnd.uniform(0.005, 0.045):.6g} '
                    f'{rnd.uniform(0.005, 0.3):.6g} {r} 0 0 -0.5 0 0 0 0')
    with open(path, 'w') as f:
        f.write(f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(rows)}\n'
                'ITEM: BOX BOUNDS pp pp ff\n0 0.05\n0 0.05\n-0.01 1\n'
                f'ITEM: ATOMS {COLS}\n' + '\n'.join(rows) + '\n')
    return len(rows)


def make_case(up, cid, **meta):
    d = os.path.join(up, cid)
    os.makedirs(d)
    m = {'name': cid, 'created': '2026-10-02T00:40:49', 'mode': 'standard', 'type_map': '2:AM_S,3:SE',
         'scale': 1000, 'status': 'uploaded', 'files': ['atom_1.liggghts']}
    m.update(meta)
    with open(os.path.join(d, 'meta.json'), 'w') as f:
        json.dump(m, f)
    return d


def dem_por(body):
    m = re.search(r'const _DEM_POR = (.*?);', body)
    return m.group(1).strip() if m else None


def main():
    td = tempfile.mkdtemp()
    up, rs = os.path.join(td, 'uploads'), os.path.join(td, 'results')
    os.makedirs(up)
    os.makedirs(rs)
    os.environ['WEBAPP_UPLOAD_FOLDER'], os.environ['WEBAPP_RESULTS_FOLDER'] = up, rs
    import app as webapp
    webapp.app.config['UPLOAD_FOLDER'], webapp.app.config['RESULTS_FOLDER'] = up, rs
    c = webapp.app.test_client()

    # ── atoms-only 케이스 (진짜 run_pipeline 경로) ──
    cid = '261002_000001_atomsonly'
    n = write_dump(os.path.join(make_case(up, cid), 'atom_1.liggghts'))
    try:
        res, err = webapp.run_pipeline(cid, 'standard', '2:AM_S,3:SE', figures=False, auto_db=False), None
    except Exception as e:                                         # noqa: BLE001
        res, err = {}, e
    fm_path = os.path.join(webapp.get_results_dir(cid), 'full_metrics.json')
    fm = json.load(open(fm_path)) if os.path.exists(fm_path) else {}
    chk(f'① run_pipeline atoms-only 성공{"" if err is None else " — " + type(err).__name__ + ": " + str(err)[:120]}',
        err is None and res.get('success') is True and res.get('atoms_only') is True)
    chk('①b atoms.csv 가 생기고 full_metrics.has_contacts 는 False',
        os.path.exists(os.path.join(webapp.get_results_dir(cid), 'atoms.csv')) and fm.get('has_contacts') is False)
    mp = os.path.join(up, cid, 'meta.json')
    m = json.load(open(mp))
    m['status'] = 'done'
    with open(mp, 'w') as f:
        json.dump(m, f)

    r = c.get(f'/single/{cid}')
    body = r.get_data(as_text=True)
    chk(f'② 결과 페이지 200 (받은 값 {r.status_code})', r.status_code == 200)
    chk("③ 3D 데이터 경로가 페이지에 붙는다 ('dem': base + '/3d-data')", "'dem': base + '/3d-data'" in body)
    chk(f'③b _DEM_POR = null (받은 값 {dem_por(body)!r})', dem_por(body) == 'null')

    r = c.get(f'/results/{cid}/3d-data')
    j = r.get_json(silent=True) or {}
    parts = j.get('particles') or []
    chk(f'④ /3d-data 200 · 입자 {len(parts)} = 덤프 {n} · atoms_only',
        r.status_code == 200 and len(parts) == n and j.get('atoms_only') is True)
    chk('④b 상 이름 = meta type_map (2 → AM_S · 3 → SE)',
        {p['type'] for p in parts} == {'AM_S', 'SE'})

    # ── atom + 판 메시 (mesh_<step>.stl) 를 같이 올린 atoms-only 케이스 — 판이 3D 에 같이 그려진다 ──
    #    (1저자 10-02 *"atom, mesh 같이 넣으면 3D 랜더 같이"* · 메시 = real_14 기준 상태의 판 STL, 평평 z 0.0302845)
    stl_src = os.path.join(HERE, '..', 'docs', 'data', 'real14_reference_20260928', 'mesh_2060000.stl')
    cid3 = '261002_000002_atomsmesh'
    d3 = make_case(up, cid3, files=['atom_405000.liggghts', 'mesh_405000.stl'])
    n3 = write_dump(os.path.join(d3, 'atom_405000.liggghts'), step=405000)
    with open(stl_src) as f_in, open(os.path.join(d3, 'mesh_405000.stl'), 'w') as f_out:
        f_out.write(f_in.read())
    try:
        res3, err3 = webapp.run_pipeline(cid3, 'standard', '2:AM_S,3:SE', figures=False, auto_db=False), None
    except Exception as e:                                         # noqa: BLE001
        res3, err3 = {}, e
    mi = os.path.join(webapp.get_results_dir(cid3), 'mesh_info.json')
    chk('⑥ atom + mesh → atoms-only 성공 · mesh_info.json 생성',
        err3 is None and res3.get('atoms_only') is True and os.path.exists(mi))
    m3 = json.load(open(os.path.join(up, cid3, 'meta.json')))
    m3['status'] = 'done'
    with open(os.path.join(up, cid3, 'meta.json'), 'w') as f:
        json.dump(m3, f)
    r = c.get(f'/single/{cid3}')
    chk(f'⑥b 결과 페이지 200 (받은 값 {r.status_code})', r.status_code == 200)
    j3 = c.get(f'/results/{cid3}/3d-data').get_json(silent=True) or {}
    tris = j3.get('mesh_triangles') or []
    zs = [v[2] for t in tris for v in t]
    chk(f'⑥c /3d-data 에 판 삼각형 {len(tris)} 개 · z = 30.2845 µm (STL 0.0302845 × scale 1000) · 입자 {len(j3.get("particles") or [])} = {n3}',
        len(tris) == 2 and zs and all(abs(z - 30.2845) < 1e-3 for z in zs) and len(j3.get('particles') or []) == n3)
    with open(os.path.join(HERE, 'static', 'js', 'viewer3d.js')) as f:
        vsrc = f.read()
    chk('⑥d 3D 뷰어가 mesh_triangles 를 판 메시로 그린다 (viewer3d.js · buildPlateMesh)',
        re.search(r'data\.mesh_triangles[^\n]*\n[^\n]*buildPlateMesh\(data\.mesh_triangles', vsrc) is not None)

    # ── 공극률이 있는 케이스 — 영역 표시 값이 바뀌지 않는다 ──
    for k, (fmx, want) in enumerate([({'porosity_spheresum': 15.63, 'porosity': 17.1}, '15.63'),
                                     ({'porosity': 17.1}, '17.1'),
                                     ({'porosity_spheresum': None, 'porosity': 17.1}, '17.1')]):
        cid2 = f'261002_00001{k}_withpor'
        d2 = make_case(up, cid2, status='done')
        write_dump(os.path.join(d2, 'atom_1.liggghts'))
        rd = webapp.get_results_dir(cid2)
        os.makedirs(rd, exist_ok=True)
        with open(os.path.join(rd, 'full_metrics.json'), 'w') as f:
            json.dump(fmx, f)
        r = c.get(f'/single/{cid2}')
        got = dem_por(r.get_data(as_text=True))
        chk(f'⑤{"abc"[k]} {sorted(fmx)} → _DEM_POR {want} (받은 값 {r.status_code} · {got!r})',
            r.status_code == 200 and got == want)

    # ── ⑦ 3D 뷰어 색 — atom 만 올린 케이스도 상 이름이 전부 알려졌으면 상별 색 (1저자 10-02 *"입자간의 구분이 없잖아"*) ──
    #    옛 판: atoms-only = "공정 보기" 로 전부 연회색 (COL.ATOMS_ONLY) · 맵에 없는 타입 이름 (T3 등) 은 **아예 안 그림**.
    #    새 판: 이름이 전부 AM_P · AM_S · SE 면 전체 모드와 같은 상별 색 · 조명 / 하나라도 모르는 이름이 있으면 옛 회색
    #    (덱 없이 반지름 되돌림 규칙 → 이름이 틀렸을 수 있다) · 모르는 이름의 입자도 회색으로 그린다 (버리지 않는다).
    vsrc_nc = re.sub(r'//[^\n]*', '', vsrc)
    chk('⑦ 맵에 없는 타입 이름의 입자를 버리지 않는다 (OTHER 묶음으로)',
        re.search(r'\(groups\[p\.type\]\s*\|\|\s*groups\.OTHER\)\.push\(p\)', vsrc_nc) is not None)
    chk('⑦b atoms-only 회색은 모르는 이름이 있을 때만 (phaseKnown = OTHER 비었음)',
        re.search(r'const phaseKnown\s*=\s*groups\.OTHER\.length\s*===\s*0', vsrc_nc) is not None
        and re.search(r'const grayView\s*=\s*atomsOnly\s*&&\s*!phaseKnown', vsrc_nc) is not None
        and re.search(r'if\s*\(\s*grayView\s*\)\s*\{\s*\n\s*state\.meshes\.AM_P\s*=\s*createInstancedSpheres\(groups\.AM_P,\s*16,\s*COL\.ATOMS_ONLY',
                      vsrc_nc) is not None)
    chk('⑦c 모르는 이름의 입자는 회색으로 그린다 (createInstancedSpheres(groups.OTHER … COL.ATOMS_ONLY))',
        re.search(r'createInstancedSpheres\(groups\.OTHER,\s*\d+,\s*COL\.ATOMS_ONLY', vsrc_nc) is not None)

    print(f'\n{_ok}/{_ok + len(_fail)} PASS')
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

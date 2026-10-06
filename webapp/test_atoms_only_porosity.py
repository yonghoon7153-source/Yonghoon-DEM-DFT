#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""atom 덤프 + 판 메시만 올린 케이스 (접촉 덤프 없음) 의 공극률 · 두께 (2026-10-07).

1저자 요청 — atoms-only 모드 (`run_pipeline` 의 "atoms_only — 3D viewer enabled, contact-based metrics skipped") 는 3D 만 띄우고
**공극률 · 두께도 안 냈다**.  둘 다 접촉이 필요 없는 정의다 → 접촉 분석과 **같은 함수**로 낸다 (새 식 없음):
  ε_sphere  = dem_analysis_core.calc_porosity            (구 부피 합 · 생산 규약 · 상자 x·y × 판 간격)
  ε_union   = dem_analysis_core.calc_porosity_union_exact (몬테카를로 정확 union · 벽 밖 제외 · x·y 주기)
  두께      = dem_analysis_core.get_plate_z × scale     (판 메시 = 판 간격 · 판이 없으면 계산하지 않는다)
접촉이 있어야 하는 값 (쌍 렌즈 union · 겹침 비율 · 질량 보존 두께 · 퍼콜레이션 …) 은 내지 않는다.
판이 입자 윗면보다 위에 떠 있으면 (덜 다져진 프레임 — 판 간격에 빈 머리 공간) 입자 윗면 (max z + r) 기준 값도 같은 함수로 따로 낸다.

  python3 webapp/test_atoms_only_porosity.py      # 종료코드 0 = PASS

[P] run_pipeline (진짜 경로 · parse 와 공극률 단계를 실제로 돈다)
    R  real_14 기준 덤프 (atom + 판 STL · input deck 없음) — 접촉 분석이 같은 원자 · 판 · 상자로 낼 값과 **비트까지 같다** ·
       case_master 의 ε_sphere 15.639 % · 판 간격 30.2845 µm · 상자 = 덤프 BOX BOUNDS · 판이 침대에 닿아 있어 입자 윗면 기준 값 없음
    L  덜 다져진 합성 침대 (판이 입자 윗면보다 ~9 µm 위) — 입자 윗면 기준 ε_sphere · ε_union 도 같은 함수로 · 판 간격 값보다 작다
    N  atom 만 (판 메시 없음) — 계산하지 않고 사유를 적는다 (공극률 키 없음 · _DEM_POR null 그대로)
    C  atoms.csv + mesh_info.json 만 (CSV 모드) — 같은 계산
    B  덤프 상자 100 µm · input deck 없음 — 덤프 BOX BOUNDS 상자로 (기본 50 µm 로 틀리게 재지 않는다)
    M  input deck 상자 ≠ 덤프 상자 — 계산하지 않는다 (어느 쪽이 맞는지 모른다)
    D  input deck 상자 = 덤프 상자 — 상자 출처 = input_params.json
[W] 결과 페이지 머리 배지 (ε_sphere · ε_union 정확 · 두께 판 간격 · atom+mesh 표지 · 입자 윗면 기준 · 계산 안 함 사유) · _DEM_POR
[V] 3D 뷰어 기공 보기 (dem_pore) — atom+mesh 케이스의 /3d-data 로 격자 빈 칸 비율 = 표의 ε_union 정확 (± 격자) · 영역 윗면 고르기
    (판 · 입자 윗면) · 머리 공간 안내 (node · 뷰어 함수 그대로)
[REG] check_all 등재
"""
import gzip
import json
import os
import random
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
REAL14 = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
CHECK_ALL = os.path.join(ROOT, 'scripts', 'check_all.sh')
MC_N = 400000                     # 시험 속도 — 생산 기본 4×10⁶ (DEM_UNION_MC_N) · 기대값도 같은 N 으로 잰다

sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)
from test_closed_param_labels import js_fn, js_const, run_node   # noqa: E402

_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {extra}' if extra else ''))
    return bool(cond)


COLS = 'id type x y z radius vx vy vz'


def write_dump(path, atoms, box=(0.0, 0.05, 0.0, 0.05), step=1000, flags='pp pp ff'):
    """LIGGGHTS atom 덤프 (sim 단위) — atoms = [(id, type, x, y, z, r)]"""
    with open(path, 'w') as f:
        f.write(f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(atoms)}\nITEM: BOX BOUNDS {flags}\n'
                f'{box[0]} {box[1]}\n{box[2]} {box[3]}\n-0.001 1\nITEM: ATOMS {COLS}\n')
        for a in atoms:
            f.write(f'{a[0]} {a[1]} {a[2]:.9g} {a[3]:.9g} {a[4]:.9g} {a[5]:.9g} 0 0 0\n')


def write_stl(path, z, lx=0.05, ly=0.05):
    with open(path, 'w') as f:
        f.write('solid plate\n')
        for tri in (((0, 0), (lx, ly), (lx, 0)), ((0, 0), (0, ly), (lx, ly))):
            f.write('  facet normal 0 0 1\n    outer loop\n')
            for x, y in tri:
                f.write(f'      vertex {x} {y} {z}\n')
            f.write('    endloop\n  endfacet\n')
        f.write('endsolid plate\n')


def write_deck(path, lx, ly, lz=0.2):
    with open(path, 'w') as f:
        f.write(f'# test deck\nregion reg block 0 {lx} 0 {ly} -0.001 {lz} units box\ncreate_box 3 reg\n')


def loose_atoms(lx=0.02, n=150, seed=11):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        t, r = (1, 0.002) if i < 10 else (2, 0.001)
        out.append((i + 1, t, rnd.uniform(0, lx), rnd.uniform(0, lx), rnd.uniform(r, 0.010), r))
    return out


def make_case(up, cid, type_map, files):
    d = os.path.join(up, cid)
    os.makedirs(d)
    with open(os.path.join(d, 'meta.json'), 'w') as f:
        json.dump({'name': cid, 'created': '2026-10-07T09:00:00', 'mode': 'standard', 'type_map': type_map,
                   'scale': 1000, 'status': 'uploaded', 'files': files}, f)
    return d


def mark_done(up, cid):
    p = os.path.join(up, cid, 'meta.json')
    m = json.load(open(p))
    m['status'] = 'done'
    with open(p, 'w') as f:
        json.dump(m, f)


def expected(results_dir, plate_z, box_x, box_y):
    """접촉 분석 (run_full_analysis) 이 같은 원자 · 판 · 상자로 부르는 바로 그 함수들 — plate_z None = 접촉 분석과 같은 판
    (get_plate_z = mesh_info.json 의 꼭짓점 z 평균 · real_14 0.030284499999999994 — 문자 0.0302845 와 마지막 자리가 다르다)"""
    import analyze_contacts as AC
    import dem_analysis_core as C
    atoms, _ = AC.load_atoms_raw(os.path.join(results_dir, 'atoms.csv'))
    if plate_z is None:
        plate_z, _src = C.get_plate_z(results_dir, atoms, 1000)
    eps = C.calc_porosity(atoms, plate_z, box_x, box_y)
    dual = C.calc_porosity_dual(atoms, [], plate_z, box_x, box_y)        # run_full_analysis 의 ε_sphere 는 이 함수의 sphere-sum
    ue = C.calc_porosity_union_exact(atoms, plate_z, box_x, box_y)
    top = max(a['z'] + a['radius'] for a in atoms.values())
    return atoms, eps, dual['porosity_spheresum'], ue, top


def section_pipeline(tmp):
    print('[P] run_pipeline — atom + 판 메시만 (접촉 덤프 없음)')
    up, rs = os.path.join(tmp, 'uploads'), os.path.join(tmp, 'results')
    import app as webapp
    webapp.app.config['UPLOAD_FOLDER'], webapp.app.config['RESULTS_FOLDER'] = up, rs
    out = {}

    def run(cid):
        try:
            r = webapp.run_pipeline(cid, 'standard', json.load(open(os.path.join(up, cid, 'meta.json')))['type_map'],
                                    figures=False, auto_db=False)
        except Exception as e:                                    # noqa: BLE001
            r = {'error': f'{type(e).__name__}: {e}'}
        rd = webapp.get_results_dir(cid)
        fm_p = os.path.join(rd, 'full_metrics.json')
        fm = json.load(open(fm_p)) if os.path.exists(fm_p) else {}
        mark_done(up, cid)
        return r, fm, rd

    # ── R  real_14 (atom + 판 STL · input deck 없음) ──
    cid = '261007_000001_real14_atoms_mesh'
    d = make_case(up, cid, '1:AM_P,2:AM_S,3:SE', ['atom_2060000.liggghts', 'mesh_2060000.stl'])
    with gzip.open(os.path.join(REAL14, 'atom_2060000.liggghts.gz'), 'rb') as fi, open(os.path.join(d, 'atom_2060000.liggghts'), 'wb') as fo:
        shutil.copyfileobj(fi, fo)
    shutil.copy2(os.path.join(REAL14, 'mesh_2060000.stl'), os.path.join(d, 'mesh_2060000.stl'))
    r, fm, rd = run(cid)
    out['R'] = (cid, fm, rd)
    chk('R1 run_pipeline atoms-only 성공 (success · atoms_only) · has_contacts False 그대로 · mode_note 그대로',
        r.get('success') is True and r.get('atoms_only') is True and fm.get('has_contacts') is False
        and str(fm.get('mode_note', '')).startswith('atoms_only'), repr(r)[:300])
    chk(f"R2 공극률 계산됨 (porosity_status OK · 출처 atoms_only) — 받은 상태 {fm.get('porosity_status')!r}",
        fm.get('porosity_status') == 'OK' and fm.get('porosity_source') == 'atoms_only', repr({k: fm.get(k) for k in ('porosity_status', 'porosity_source')}))
    if fm.get('porosity_status') == 'OK':
        atoms, eps, eps_dual, ue, top = expected(rd, None, 0.05, 0.05)
        chk(f"R3 ε_sphere = 접촉 분석이 같은 원자 · 판 · 상자로 내는 값 (calc_porosity · calc_porosity_dual sphere-sum) — 비트까지 같다 "
            f"({fm.get('porosity')!r} · {eps!r})",
            fm.get('porosity') == eps == eps_dual and fm.get('porosity_spheresum') == eps)
        chk(f"R3b ε_sphere = case_master real_14 보고값 15.639 % ({fm.get('porosity'):.4f})", abs(fm['porosity'] - 15.639) < 6e-4)
        chk(f"R4 ε_union 정확 (MC {MC_N:,}) = calc_porosity_union_exact 같은 N · 같은 씨앗 — 비트까지 같다 ({fm.get('porosity_union_exact_pct')!r})",
            fm.get('porosity_union_exact_pct') == ue['porosity_union_exact_pct'] and fm.get('union_exact_mc_seed') == ue['union_exact_mc_seed']
            and fm.get('union_exact_mc_n') == MC_N and fm.get('union_exact_status') == 'OK'
            and fm.get('porosity_union_exact_se_pct') == ue['porosity_union_exact_se_pct']
            and fm.get('wall_overhang_over_Vbox_pct') == ue['wall_overhang_over_Vbox_pct'])
        chk(f"R4b ε_union 정확 ≈ 웹앱 정확 union real_14 17.86 % (격자 시험 D15 의 10⁶ 점 · ±0.3 %p) ({fm.get('porosity_union_exact_pct'):.3f})",
            abs(fm['porosity_union_exact_pct'] - 17.86) < 0.3)
    chk(f"R5 두께 = 판 간격 = 판 메시 z × scale = 30.2845 µm · 출처 mesh ({fm.get('thickness_um')!r} · {fm.get('plate_z_source')!r})",
        fm.get('thickness_um') is not None and abs(fm['thickness_um'] - 30.2845) < 1e-9 and fm.get('plate_z_source') == 'mesh')
    chk(f"R6 상자 = 덤프 BOX BOUNDS (input deck 없음) 50 × 50 µm ({fm.get('porosity_box_source')!r} · {fm.get('porosity_box_x_um')} × {fm.get('porosity_box_y_um')})",
        fm.get('porosity_box_source') == 'atom dump BOX BOUNDS' and fm.get('porosity_box_x_um') == 50.0 and fm.get('porosity_box_y_um') == 50.0)
    chk('R7 판이 침대에 닿아 있다 (입자 윗면 31.336 > 판 30.2845) → 입자 윗면 기준 값은 내지 않고 사유만',
        fm.get('porosity_bedtop_spheresum') is None and str(fm.get('porosity_bedtop_status', '')).startswith('not_applicable')
        and fm.get('bed_top_um') is not None and abs(fm['bed_top_um'] - 31.336) < 1e-3 and fm.get('headspace_um') is not None
        and fm['headspace_um'] < 0, repr({k: fm.get(k) for k in ('porosity_bedtop_status', 'bed_top_um', 'headspace_um')}))
    chk('R8 접촉이 있어야 하는 값은 없다 (쌍 렌즈 union · 겹침 비율 · 질량 보존 두께 · 퍼콜레이션 · CN)',
        all(k not in fm for k in ('porosity_union', 'overlap_fraction_pct', 'thickness_mass_conserving_um', 'percolation_pct', 'se_se_cn')))

    # ── L  덜 다져진 합성 침대 — 판이 입자 윗면보다 위 ──
    cid = '261007_000002_loose'
    d = make_case(up, cid, '1:AM_P,2:SE', ['atom_200000.liggghts', 'mesh_200000.stl'])
    atoms_l = loose_atoms()
    write_dump(os.path.join(d, 'atom_200000.liggghts'), atoms_l, box=(0, 0.02, 0, 0.02), step=200000)
    write_stl(os.path.join(d, 'mesh_200000.stl'), 0.020, 0.02, 0.02)
    r, fm, rd = run(cid)
    out['L'] = (cid, fm, rd)
    chk(f"L1 덜 다져진 프레임도 계산 · 두께 = 판 간격 20 µm ({fm.get('porosity_status')!r} · {fm.get('thickness_um')!r})",
        fm.get('porosity_status') == 'OK' and fm.get('thickness_um') is not None and abs(fm['thickness_um'] - 20.0) < 1e-9)
    if fm.get('porosity_status') == 'OK':
        atoms, eps, _, ue, top = expected(rd, None, 0.02, 0.02)
        _, eps_t, _, ue_t, _ = expected(rd, top, 0.02, 0.02)
        chk(f"L2 판 간격 값 = 같은 함수 (ε_sphere {fm.get('porosity'):.3f} · ε_union 정확 {fm.get('porosity_union_exact_pct'):.3f})",
            fm.get('porosity') == eps and fm.get('porosity_union_exact_pct') == ue['porosity_union_exact_pct'])
        chk(f"L3 입자 윗면 = max z + r ({fm.get('bed_top_um')!r} µm) · 빈 머리 공간 = 판 − 윗면 ({fm.get('headspace_um')!r} µm > 0)",
            fm.get('bed_top_um') is not None and abs(fm['bed_top_um'] - top * 1000) < 1e-9
            and abs(fm['headspace_um'] - (20.0 - top * 1000)) < 1e-9 and fm['headspace_um'] > 5)
        chk(f"L4 입자 윗면 기준 ε_sphere · ε_union 정확 = 같은 함수를 판 대신 윗면으로 ({fm.get('porosity_bedtop_spheresum')!r} · "
            f"{fm.get('porosity_bedtop_union_exact_pct')!r})",
            fm.get('porosity_bedtop_spheresum') == eps_t and fm.get('porosity_bedtop_union_exact_pct') == ue_t['porosity_union_exact_pct']
            and fm.get('porosity_bedtop_union_exact_se_pct') == ue_t['porosity_union_exact_se_pct'] and fm.get('porosity_bedtop_status') == 'OK')
        chk('L5 판 간격 값 > 입자 윗면 기준 값 (판 간격은 빈 머리 공간을 포함한다)',
            fm['porosity'] > fm['porosity_bedtop_spheresum'] and fm['porosity_union_exact_pct'] > fm['porosity_bedtop_union_exact_pct'])

    # ── N  atom 만 (판 메시 없음) ──
    cid = '261007_000003_atoms_only'
    d = make_case(up, cid, '1:AM_P,2:SE', ['atom_1.liggghts'])
    write_dump(os.path.join(d, 'atom_1.liggghts'), loose_atoms(), box=(0, 0.02, 0, 0.02))
    r, fm, rd = run(cid)
    out['N'] = (cid, fm, rd)
    chk(f"N1 판 메시 없음 → 계산하지 않고 사유를 적는다 ({fm.get('porosity_status')!r}) · 공극률 · 두께 키 없음",
        r.get('success') is True and str(fm.get('porosity_status', '')).startswith('not_computed') and '판 메시' in fm.get('porosity_status', '')
        and 'porosity' not in fm and 'thickness_um' not in fm and 'porosity_union_exact_pct' not in fm, repr(fm)[:300])

    # ── C  atoms.csv + mesh_info.json (CSV 모드) ──
    cid = '261007_000004_csv'
    d = make_case(up, cid, '1:AM_P,2:SE', ['atoms.csv', 'mesh_info.json'])
    with open(os.path.join(d, 'atoms.csv'), 'w') as f:
        f.write('id,type,x,y,z,radius\n')
        for a in loose_atoms(lx=0.05):
            f.write(f'{a[0]},{a[1]},{a[2]:.9g},{a[3]:.9g},{a[4]:.9g},{a[5]:.9g}\n')
    with open(os.path.join(d, 'mesh_info.json'), 'w') as f:
        json.dump({'plate_z': 0.012, 'source': 'mesh_x.stl', 'triangles': [[[0, 0, 0.012], [0.05, 0.05, 0.012], [0.05, 0, 0.012]]],
                   'n_triangles': 1}, f)
    r, fm, rd = run(cid)
    out['C'] = (cid, fm, rd)
    ok_c = fm.get('porosity_status') == 'OK'
    if ok_c:
        _, eps, _, ue, _ = expected(rd, None, 0.05, 0.05)
        ok_c = fm.get('porosity') == eps and fm.get('porosity_union_exact_pct') == ue['porosity_union_exact_pct']
    chk(f"C1 CSV 모드 (atoms.csv + mesh_info.json) 도 같은 계산 · 상자 = 기본 50 µm (덱 · 덤프 없음) ({fm.get('porosity_status')!r} · {fm.get('porosity_box_source')!r})",
        ok_c and str(fm.get('porosity_box_source', '')).startswith('default') and abs(fm.get('thickness_um', 0) - 12.0) < 1e-9)

    # ── B  덤프 상자 100 µm · input deck 없음 ──
    cid = '261007_000005_box100'
    d = make_case(up, cid, '1:AM_P,2:SE', ['atom_1.liggghts', 'mesh_1.stl'])
    write_dump(os.path.join(d, 'atom_1.liggghts'), loose_atoms(lx=0.1, n=300), box=(0, 0.1, 0, 0.1))
    write_stl(os.path.join(d, 'mesh_1.stl'), 0.012, 0.1, 0.1)
    r, fm, rd = run(cid)
    out['B'] = (cid, fm, rd)
    ok_b = fm.get('porosity_status') == 'OK'
    if ok_b:
        _, eps, _, ue, _ = expected(rd, None, 0.1, 0.1)
        ok_b = fm.get('porosity') == eps and fm.get('porosity_union_exact_pct') == ue['porosity_union_exact_pct']
    chk(f"B1 덤프 상자 100 µm · deck 없음 → 덤프 BOX BOUNDS 상자로 (기본 50 µm 로 틀리게 재지 않는다) ({fm.get('porosity_box_x_um')} µm)",
        ok_b and fm.get('porosity_box_source') == 'atom dump BOX BOUNDS' and fm.get('porosity_box_x_um') == 100.0)

    # ── M  deck 상자 ≠ 덤프 상자 ──
    cid = '261007_000006_mismatch'
    d = make_case(up, cid, '1:AM_P,2:SE', ['atom_1.liggghts', 'mesh_1.stl', 'input_x.liggghts'])
    write_dump(os.path.join(d, 'atom_1.liggghts'), loose_atoms(lx=0.1, n=300), box=(0, 0.1, 0, 0.1))
    write_stl(os.path.join(d, 'mesh_1.stl'), 0.012, 0.1, 0.1)
    write_deck(os.path.join(d, 'input_x.liggghts'), 0.05, 0.05)
    r, fm, rd = run(cid)
    chk(f"M1 input deck 상자 (50 µm) ≠ 덤프 상자 (100 µm) → 계산하지 않는다 · 사유 ({fm.get('porosity_status')!r})",
        str(fm.get('porosity_status', '')).startswith('not_computed') and 'box_mismatch' in fm.get('porosity_status', '')
        and 'porosity' not in fm, repr(fm)[:300])

    # ── D  deck 상자 = 덤프 상자 ──
    cid = '261007_000007_deck'
    d = make_case(up, cid, '1:AM_P,2:SE', ['atom_1.liggghts', 'mesh_1.stl', 'input_x.liggghts'])
    write_dump(os.path.join(d, 'atom_1.liggghts'), loose_atoms(lx=0.05, n=200), box=(0, 0.05, 0, 0.05))
    write_stl(os.path.join(d, 'mesh_1.stl'), 0.012, 0.05, 0.05)
    write_deck(os.path.join(d, 'input_x.liggghts'), 0.05, 0.05)
    r, fm, rd = run(cid)
    chk(f"D1 input deck 상자 = 덤프 상자 → 계산 · 상자 출처 input_params.json ({fm.get('porosity_box_source')!r})",
        fm.get('porosity_status') == 'OK' and fm.get('porosity_box_source') == 'input_params.json')
    return out


def section_page(tmp, cases):
    print('[W] 결과 페이지 머리 배지')
    import app as webapp
    c = webapp.app.test_client()

    def page(cid):
        r = c.get(f'/single/{cid}')
        body = r.get_data(as_text=True)
        head = body[:body.find('</p>', body.find('page-header'))] if 'page-header' in body else body[:5000]
        plain = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', head))
        m = re.search(r'const _DEM_POR = (.*?);', body)
        return r.status_code, plain, head, (m.group(1).strip() if m else None)

    cid, fm, _ = cases['R']
    st, plain, head, dp = page(cid)
    want = '%.1f' % fm['porosity'] if fm.get('porosity') is not None else '?'
    chk(f'W1 atom+mesh 결과 페이지 200 · "Porosity ε_sphere: {want}%" · "ε_union 정확 (MC)" · "두께 (판 간격): 30.3μm"',
        st == 200 and f'Porosity ε_sphere: {want}%' in plain and 'ε_union 정확 (MC):' in plain and '두께 (판 간격): 30.3μm' in plain, plain[:600])
    chk('W2 atom+mesh 표지 배지 — 접촉 덤프 없음 · 공극률 · 두께만 (접촉 지표 · 쌍 렌즈 union · 질량 보존 두께 없음)',
        'atom + 판 메시만' in plain and re.search(r'title="[^"]*접촉 덤프[^"]*"', head) is not None, plain[:600])
    chk(f'W3 _DEM_POR = ε_sphere ({dp}) — MPM↔DEM 영역 표시가 이 값을 쓴다', dp is not None and dp != 'null' and abs(float(dp) - fm['porosity']) < 1e-9)
    cid, fm, _ = cases['L']
    st, plain, head, dp = page(cid)
    chk(f"W4 덜 다져진 프레임 — '입자 윗면 기준' 배지 (ε_sphere · ε_union 정확 · 빈 머리 공간 µm) · 판 간격 값과 나란히",
        st == 200 and '입자 윗면 기준' in plain and ('%.1f' % fm.get('porosity_bedtop_spheresum', -1)) in plain
        and '머리 공간' in plain and ('%.1f' % fm.get('headspace_um', -1)) in plain, plain[:700])
    cid, fm, _ = cases['N']
    st, plain, head, dp = page(cid)
    chk(f'W5 판 메시 없음 — "Porosity — 계산 안 함" 배지 (사유 = 판 메시 없음) · _DEM_POR null ({dp})',
        st == 200 and 'Porosity — 계산 안 함' in plain and '판 메시' in head and dp == 'null', plain[:500])


V_RUN = r"""
const OUT = {};
const data = PAY;
const box = data.box;
const domP = demPoreDomainTop(data);
const domB = demPoreDomainTop(data, 'bed_top');
OUT.domP = domP; OUT.domB = domB;
for (const [k, dom] of [['plate', domP], ['bed', domB]]) {
  const nx = demPoreGridNx(box, dom.zTop, 'fine');
  const r = computeVoidVoxels(data.particles, box, dom.zTop, nx, {});
  OUT[k] = { vf: r.voidFraction, dims: [r.nx, r.ny, r.nz] };
}
const res = { nx: 100, ny: 100, nz: 61, hx: 0.5, hy: 0.5, hz: 0.5, nTotal: 610000, nVoid: 104432, voidFraction: 0.171, periodicXY: true };
OUT.legP = demPoreLegendHTML(res, domP, { preset: 'normal', top: 'plate' });
OUT.legB = demPoreLegendHTML(res, domB, { preset: 'normal', top: 'bed_top' });
console.log(JSON.stringify(OUT));
"""


def section_viewer(tmp, cases):
    print('[V] 3D 뷰어 기공 보기 (dem_pore) — atom+mesh 케이스')
    import app as webapp
    c = webapp.app.test_client()
    if not shutil.which('node'):
        chk('V0 node 필요', False, 'node 미설치')
        return
    js = open(VIEWER_JS, encoding='utf-8').read()
    names = ('computeVoidVoxels', 'demPoreDomainTop', 'demPoreGridNx', 'demPoreLegendHTML', 'demPoreStatusHTML')
    parts, miss = [], []
    for n in names:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    try:
        parts.append(js_const(js, 'DEM_PORE_PRESETS'))
    except (ValueError, AssertionError):
        miss.append('DEM_PORE_PRESETS')
    parts += re.findall(r'^const DEM_PORE_(?:COL|MAX_INSTANCES) = [^;]+;', js, re.M)
    if not chk('V0 기공 함수를 잘라 냈다', not miss, repr(miss)):
        return
    for key, tag in (('R', 'real_14'), ('L', '덜 다져진 합성')):
        cid, fm, _ = cases[key]
        j = c.get(f'/results/{cid}/3d-data').get_json(silent=True) or {}
        chk(f'V1 {tag} /3d-data — atoms_only · 판 삼각형 · 입자 전부', j.get('atoms_only') is True and len(j.get('mesh_triangles') or []) > 0
            and len(j.get('particles') or []) > 0)
        res = run_node('"use strict";\n' + '\n'.join(parts) + '\nconst PAY = ' + json.dumps(j) + ';\n' + V_RUN)
        if not chk(f'V1b {tag} node 실행', res is not None):
            continue
        ue = fm.get('porosity_union_exact_pct')
        chk(f"V2 {tag} — 기공 보기 (판 영역 · 고운 격자) 빈 칸 비율 {100 * res['plate']['vf']:.2f} % = 표의 ε_union 정확 {ue} % (± 0.5 %p)",
            ue is not None and abs(100 * res['plate']['vf'] - ue) <= 0.5, repr(res['plate']))
        chk(f"V3 {tag} — 영역 윗면 고르기: 판 (mesh · {res['domP'].get('zTop')}) · 입자 윗면 (bed_top · {res['domB'].get('zTop')} = max z + r)",
            res['domP'].get('source') == 'mesh' and res['domB'].get('source') == 'bed_top'
            and abs(res['domB']['zTop'] - max(p['z'] + p['r'] for p in j['particles'])) < 1e-9, repr({'P': res['domP'], 'B': res['domB']}))
        legp = re.sub(r'<[^>]+>', '', res['legP'])
        chk(f'V4 {tag} — 범례에 영역 윗면 고르기 (id dem-pore-top · 판 메시 · 입자 윗면)',
            'id="dem-pore-top"' in res['legP'] and '입자 윗면' in res['legP'], legp[:300])
        if key == 'L':
            bt = fm.get('porosity_bedtop_union_exact_pct')
            mh = re.search(r'보다 ([0-9.]+) µm 위', legp)
            chk(f"V5 덜 다져진 프레임 — 범례가 빈 머리 공간을 말한다 (판이 입자 윗면보다 {fm.get('headspace_um', 0):.2f} µm 위 · "
                f"payload 좌표 소수 둘째 자리 반올림 ± 0.02)",
                '머리 공간' in legp and mh is not None and abs(float(mh.group(1)) - fm.get('headspace_um', -99)) <= 0.02, legp[:500])
            chk(f"V6 입자 윗면 영역 빈 칸 비율 {100 * res['bed']['vf']:.2f} % = 표의 입자 윗면 기준 ε_union 정확 {bt} % (± 1 %p)",
                bt is not None and abs(100 * res['bed']['vf'] - bt) <= 1.0)
        else:
            chk('V5 real_14 (판이 침대에 닿음) — 범례에 머리 공간 경고 없음', '머리 공간' not in legp, legp[:400])
            legb = re.sub(r'<[^>]+>', '', res['legB'])
            chk('V5b real_14 에서 영역 윗면 = 입자 윗면을 고르면 — 판이 입자 윗면보다 아래라 판 위로 나온 입자 끝 사이까지 넣는다는 경고 · 표의 값은 판 영역',
                '판이 침대에 닿음' in legb and '표의 값은 판 영역' in legb, legb[:500])


def section_registration():
    print('[REG] check_all 배선')
    chk('REG scripts/check_all.sh 가 이 시험을 돈다', 'webapp/test_atoms_only_porosity.py' in open(CHECK_ALL, encoding='utf-8').read())


def main():
    tmp = tempfile.mkdtemp(prefix='atomspor_')
    try:
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
            os.environ[k] = os.path.join(tmp, v)
            os.makedirs(os.environ[k], exist_ok=True)
        os.environ['DEM_UNION_MC_N'] = str(MC_N)
        cases = section_pipeline(tmp)
        try:
            section_page(tmp, cases)
        except Exception as e:                                   # noqa: BLE001
            chk('W 절 실행', False, f'{type(e).__name__}: {e}')
        try:
            section_viewer(tmp, cases)
        except Exception as e:                                   # noqa: BLE001
            chk('V 절 실행', False, f'{type(e).__name__}: {e}')
        section_registration()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print()
    print(f'{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        print('FAIL — ' + ' | '.join(_fail))
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())

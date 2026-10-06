#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D 뷰어 "AM 접촉 확대" — 2026-10-06 1저자 요청 (보고 슬라이드 패널 "Coverage 확대" · "활물질 주위 SE").

  python3 webapp/test_viewer_am_contacts.py      # 종료코드 0 = PASS

AM 하나를 골라 그 AM 에 닿은 입자 (SE · AM) 와 AM 표면의 접촉 cap 을 그린다.  자료는 새 경로 하나가 준다:
  GET /results/<case>/am-contacts?am_id=<id>   ·   GET /archive/results/<folder>/am-contacts?am_id=<id>
  (contacts.csv 에서 그 AM 의 행만 — 상대 id · 상 · 반경 · 위치 (x · y 주기 최소영상 = AM 옆 자리) · 접촉 면적 (c_cpl[22]) ·
   세대 2 표면 면적 · 접촉점 · δ — µm · µm²)

  [R] 경로 — 합성 침대 (손 계산) · live · archive 같은 답 · 오류 (am_id 없음 · 없는 id · SE id · 접촉 덤프 없음) ·
      주기 경계 너머 상대는 AM 옆 영상 자리 (|d| = r1 + r2 − δ) · 상자 (input_params.json) 없으면 그리기는 0.05 기본 · 보고 규칙
      합집합은 빈칸 (생산과 같은 계약) · 합집합 값 = 생산 함수 (`union_coverage_bed` · `union_cap_coverage`) · cap 합 = ΣA/(4πR²)
  [Q] real_14 기준 상태 (커밋 덤프 → parse_liggghts) — SE 수 = 그 AM 의 AM–SE CN (독립 행 셈) · 방향 검사 0 실패 · 경계 AM 의 영상 ·
      세대 2 합집합 = 침대 전체 `union_coverage_bed` 의 입자 값 (정확히) · 그린 cap (경로의 방향 · 면적) 으로 다시 재도 같다
  [V] viewer3d.js — cap 각 함수 (node: A 0 → 0 · A 2πR² → 90° · 단조 · 반구로 자름) · DEM 조작판 버튼 · 모달 (경로 · 4× 투명 PNG ·
      상대 보기 토글 · cap 규칙 · PC/SC 고르기) · 범례 (SE 수 · 그림 합집합 · cap 합 = 겹침 두 번 셈 · 보고값) · 후보 순서
"""
import gzip
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
REF = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)
from test_closed_param_labels import js_fn, run_node   # noqa: E402

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


def _try(fn, default=None):
    """응답에 키가 없을 때 (옛 코드 · 오류 응답) 시험이 죽지 않고 FAIL 로 적히게."""
    try:
        return fn()
    except (KeyError, TypeError, ValueError, IndexError):
        return default


TM_STR = '1:AM_P,2:AM_S,3:SE'
TM = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
L = 0.05                       # 주기 상자 (sim)
R_P, R_S, R_SE = 0.006, 0.002, 0.0015   # SE 를 크게 (cap 이 Fibonacci 점 수십 개를 덮게 — 합집합 대조가 0 = 0 이 되지 않게)
AM1 = (0.003, 0.025, 0.012)    # x − r < 0 → x = 0 경계를 걸친다
D10 = R_P + R_SE - 3.0e-4      # SE 10 (x 경계 너머) 의 중심 거리 = r1 + r2 − δ = 7.2 µm


def disc_area(r1, r2, d):
    x = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    return math.pi * max(r1 * r1 - x * x, 0.0), x


def synth_bed():
    """atoms {id: (type, r, x, y, z)} · rows [(id1, id2, δ, area, cp)] — AM_P 1 에 SE 6 (하나는 x 경계 너머 · 둘은 cap 이 겹친다)
    + AM_S 1 (AM–AM).  다른 AM 의 접촉 · SE–SE 접촉도 하나씩 (AM 1 의 목록에 나오면 안 된다)."""
    atoms = {1: (1, R_P) + AM1, 2: (1, R_P, 0.030, 0.030, 0.030)}
    rows = []
    t = math.radians(10.0)
    dirs = {10: (-1, 0, 0), 11: (1, 0, 0), 12: (math.cos(t), math.sin(t), 0), 13: (0, 1, 0), 14: (0, -1, 0),
            15: (0, 0, 1)}
    deltas = {10: 3.0e-4, 11: 2.5e-4, 12: 3.5e-4, 13: 3.0e-4, 14: 2.0e-4, 15: 4.0e-4}
    for sid, u in dirs.items():
        d = R_P + R_SE - deltas[sid]
        p = [AM1[k] + d * u[k] for k in range(3)]
        p[0] %= L                                            # 원자 표 = 상자 안 (덤프가 감싼 좌표)
        atoms[sid] = (3, R_SE, *p)
        A, x = disc_area(R_P, R_SE, d)
        cp = [AM1[k] + x * u[k] for k in range(3)]
        cp[0] %= L                                           # 접촉점도 감싼 좌표로 — 경로가 AM 옆으로 되돌려야 한다
        rows.append((1, sid, deltas[sid], A, cp) if sid % 2 == 0 else (sid, 1, deltas[sid], A, cp))
    # AM_S 3 — (1, 1, 0)/√2 방향 AM–AM 접촉
    u = (2 ** -0.5, 2 ** -0.5, 0.0)
    d = R_P + R_S - 1.0e-4
    atoms[3] = (2, R_S) + tuple(AM1[k] + d * u[k] for k in range(3))
    A, x = disc_area(R_P, R_S, d)
    rows.append((3, 1, 1.0e-4, A, [AM1[k] + x * u[k] for k in range(3)]))
    # 다른 AM 의 접촉 · SE–SE 접촉 (AM 1 에서 멀리)
    z20 = 0.030 + R_P + R_SE - 3e-4
    atoms[20] = (3, R_SE, 0.030, 0.030, z20)
    A20, _ = disc_area(R_P, R_SE, R_P + R_SE - 3e-4)
    rows.append((2, 20, 3e-4, A20, [0.030, 0.030, 0.0359]))
    atoms[21] = (3, R_SE, 0.030, 0.030, z20 + 2 * R_SE - 1e-5)
    A21, _ = disc_area(R_SE, R_SE, 2 * R_SE - 1e-5)
    rows.append((20, 21, 1e-5, A21, [0.030, 0.030, z20 + R_SE]))
    return atoms, rows


def write_case(folder, atoms, rows, meta=True, contacts=True, input_params=True, full_metrics=None):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, 'atoms.csv'), 'w') as f:
        f.write('id,type,x,y,z,radius\n')
        for i, (t, r, x, y, z) in atoms.items():
            f.write(f'{i},{t},{x!r},{y!r},{z!r},{r!r}\n')
    if contacts:
        with open(os.path.join(folder, 'contacts.csv'), 'w') as f:
            f.write('id1,id2,fn_x,fn_y,fn_z,contact_area,delta,cp_x,cp_y,cp_z\n')
            for a, b, dl, A, cp in rows:
                f.write(f'{a},{b},0,0,0.0001,{A!r},{dl!r},{cp[0]!r},{cp[1]!r},{cp[2]!r}\n')
    if input_params:
        with open(os.path.join(folder, 'input_params.json'), 'w') as f:
            json.dump({'box_x': L, 'box_y': L}, f)
    if full_metrics is not None:
        with open(os.path.join(folder, 'full_metrics.json'), 'w') as f:
            json.dump(full_metrics, f)
    if meta:
        with open(os.path.join(folder, 'meta.json'), 'w') as f:
            json.dump({'name': os.path.basename(folder), 'type_map': TM_STR, 'scale': 1000, 'status': 'done'}, f)


def setup_app(tmp):
    up, rs, ar = (os.path.join(tmp, k) for k in ('uploads', 'results', 'archive'))
    for p in (up, rs, ar):
        os.makedirs(p, exist_ok=True)
    os.environ['WEBAPP_UPLOAD_FOLDER'], os.environ['WEBAPP_RESULTS_FOLDER'] = up, rs
    os.environ['WEBAPP_ARCHIVE_FOLDER'] = ar
    import app as webapp
    webapp.app.config['UPLOAD_FOLDER'], webapp.app.config['RESULTS_FOLDER'] = up, rs
    webapp.app.config['ARCHIVE_FOLDER'] = ar
    return webapp, webapp.app.test_client(), up, rs, ar


def live_case(up, rs, cid, atoms, rows, **kw):
    write_case(os.path.join(up, cid), atoms, rows, meta=True, contacts=False, input_params=False)
    kw.setdefault('meta', False)
    write_case(os.path.join(rs, cid), atoms, rows, **kw)


def section_r(c, up, rs, ar):
    print('[R] /am-contacts — 합성 침대')
    import pandas as pd
    from coverage_physics_vs_hertzian import union_coverage_bed
    from plastic_coverage import union_cap_coverage, fibonacci_sphere
    atoms, rows = synth_bed()
    fm = {'coverage_AM_P_mean_physics_union': 41.5, 'coverage_status_physics_union': 'ok', 'coverage_AM_P_mean': 17.0,
          'coverage_AM_S_mean_physics_union': 44.0}
    cid = '261006_000002_amcsynth'
    live_case(up, rs, cid, atoms, rows, full_metrics=fm)
    r = c.get(f'/results/{cid}/am-contacts?am_id=1')
    j = r.get_json(silent=True) or {}
    chk(f'R1 live 200 (받은 값 {r.status_code})', r.status_code == 200, (r.get_data(as_text=True) or '')[:120])
    cs = j.get('contacts') or []
    by = {int(x.get('partner_id', -1)): x for x in cs}
    chk('R1b 그 AM 의 행만 — SE 6 (10–15) + AM 1 (3) · 다른 AM 의 접촉 · SE–SE 행은 없다',
        sorted(by) == [3, 10, 11, 12, 13, 14, 15] and j.get('n_se') == 6 and j.get('n_am') == 1, repr(sorted(by)))
    am = j.get('am') or {}
    chk('R1c AM = id 1 · AM_P · R 6 µm · 위치 µm (덤프 × scale)',
        am.get('id') == 1 and am.get('type') == 'AM_P' and abs(am.get('r', 0) - 6.0) < 1e-9
        and abs(am.get('x', 0) - 3.0) < 1e-9 and abs(am.get('z', 0) - 12.0) < 1e-9, repr(am))
    ok_fields = bool(cs) and all(all(k in x for k in ('partner_id', 'partner_type', 'pair', 'partner_r', 'x', 'y', 'z',
                                                       'wrapped', 'area_um2', 'area_g2_um2', 'delta_um', 'cp', 'geom_ok'))
                                 for x in cs)
    chk('R2 행마다 상대 id · 상 · 반경 · 위치 · 영상 표지 · 면적 (c_cpl[22] · 세대 2) · δ · 접촉점 · 방향 검사', ok_fields,
        repr(cs[0] if cs else None)[:300])
    rowmap = {(b if a == 1 else a): (a, b, dl, A, cp) for a, b, dl, A, cp in rows if 1 in (a, b)}
    areas_ok = _try(lambda: bool(by) and all(
        abs(by[p]['area_um2'] - rowmap[p][3] * 1e6) <= 1e-12 * max(1, rowmap[p][3] * 1e6)
        and abs(by[p]['delta_um'] - rowmap[p][2] * 1e3) <= 1e-12 for p in by))
    chk('R2b 면적 µm² = c_cpl[22] × scale² · δ µm = δ × scale', areas_ok)
    chk('R2c 상 · 쌍 — SE 는 AM_SE · AM_S 3 은 AM_AM · 반경 µm (SE 1.5 · AM_S 2)',
        _try(lambda: all(by[s]['partner_type'] == 'SE' and by[s]['pair'] == 'AM_SE'
                         and abs(by[s]['partner_r'] - 1.5) < 1e-12 for s in (10, 11, 12, 13, 14, 15))
             and by[3]['partner_type'] == 'AM_S' and by[3]['pair'] == 'AM_AM' and abs(by[3]['partner_r'] - 2.0) < 1e-12))
    p10 = by.get(10, {})
    d10 = _try(lambda: math.dist((p10['x'], p10['y'], p10['z']), (am['x'], am['y'], am['z'])), float('nan'))
    want_d = D10 * 1e3
    chk(f'R3 x 경계 너머 SE 10 = AM 옆 영상 자리 (x {p10.get("x")} µm · |d| {d10:.6f} = {want_d:.3f} µm) · wrapped',
        p10.get('wrapped') is True and abs(p10.get('x', 0) - (3.0 - want_d)) < 1e-6 and abs(d10 - want_d) < 1e-6)
    chk('R3b 나머지 상대는 감싸지 않았다 · 영상 수 1 · 방향 검사 실패 0',
        _try(lambda: all(by[p]['wrapped'] is False for p in (3, 11, 12, 13, 14, 15))) and j.get('n_wrapped') == 1
        and j.get('n_dir_inconsistent') == 0 and bool(cs) and all(x.get('geom_ok') for x in cs), repr(j.get('n_wrapped')))
    cp10 = p10.get('cp') or [None] * 3
    chk('R3c 접촉점도 AM 옆으로 되돌린다 (감싼 47 µm → −3 µm 근처)', cp10[0] is not None and -3.1 < cp10[0] < -2.9, repr(cp10))
    # 합집합 · cap 합 — 생산 함수와 같다
    adf = pd.read_csv(os.path.join(rs, cid, 'atoms.csv'))
    cdf = pd.read_csv(os.path.join(rs, cid, 'contacts.csv'))
    keys, per = union_coverage_bed(adf, cdf, TM, scale=1000.0, box_xy=(L, L))
    u = j.get('union_pct') or {}
    g2 = u.get('g2') or {}
    chk(f'R4 보고 규칙 합집합 (세대 2 · 이 AM) = 생산 union_coverage_bed 의 입자 값 ({g2.get("value")} = {per.get(1)})',
        keys.get('coverage_status_physics_union') == 'ok' and g2.get('status') == 'ok' and g2.get('value') is not None
        and abs(g2['value'] - per[1]) < 1e-12, repr(g2))
    se_c = [x for x in cs if x.get('pair') == 'AM_SE']
    am_c = [x for x in cs if x.get('pair') == 'AM_AM']
    vec = lambda x: [x['x'] - am['x'], x['y'] - am['y'], x['z'] - am['z']]   # noqa: E731
    U = fibonacci_sphere()
    want_h = _try(lambda: union_cap_coverage(6.0, [vec(x) for x in se_c], [x['area_um2'] for x in se_c],
                                             [vec(x) for x in am_c], [x['area_um2'] for x in am_c], points=U)[0])
    hz = u.get('hertz') or {}
    chk(f'R4b 그림 합집합 (c_cpl[22] cap) = union_cap_coverage 로 다시 잰 값 ({hz.get("value")} = {want_h})',
        bool(se_c) and want_h is not None and hz.get('status') == 'ok' and hz.get('value') is not None
        and abs(hz['value'] - want_h) < 1e-9, repr(hz))
    want_g = _try(lambda: union_cap_coverage(6.0, [vec(x) for x in se_c], [x['area_g2_um2'] for x in se_c],
                                             [vec(x) for x in am_c], [x['area_g2_um2'] for x in am_c], points=U)[0])
    chk('R4c 경로가 준 세대 2 면적 · 방향으로 다시 재면 = 보고 규칙 합집합 (그린 cap = 보고 cap)',
        bool(se_c) and want_g is not None and g2.get('value') is not None and abs(want_g - g2['value']) < 1e-9,
        repr((want_g, g2.get('value'))))
    cs_sum = sum(x.get('area_um2', 0) for x in se_c) / (4 * math.pi * 36.0) * 100
    cap = j.get('cap_sum_pct') or {}
    chk(f'R4d cap 단순 합 = ΣA_SE / (4πR²) × 100 ({cap.get("hertz")} = {cs_sum:.6f})',
        bool(se_c) and cap.get('hertz') is not None and abs(cap['hertz'] - cs_sum) < 1e-9
        and cap.get('g2') is not None and cap['g2'] >= cap['hertz'] - 1e-12, repr(cap))
    chk(f'R4f 겹친 cap (SE 11 · 12 — 10° 떨어짐) — 그림 합집합 {hz.get("value")} < cap 단순 합 {cap.get("hertz")} '
        '(합은 겹침을 두 번 센다)',
        hz.get('value') is not None and cap.get('hertz') is not None and 0 < hz['value'] < cap['hertz'] - 0.05)
    rep = j.get('reported') or {}
    chk('R4e 보고값 (침대 평균 · 케이스 표) — full_metrics 의 AM_P 합집합 41.5 · 상태 ok · Hertz 계열 합-클립 17.0',
        rep.get('label') == 'AM_P' and rep.get('union_mean_pct') == 41.5 and rep.get('union_status') == 'ok'
        and rep.get('hertz_mean_pct') == 17.0, repr(rep))
    # archive — 같은 파일 · 같은 답
    write_case(os.path.join(ar, 'amc_synth'), atoms, rows, full_metrics=fm)
    ra = c.get('/archive/results/amc_synth/am-contacts?am_id=1')
    ja = ra.get_json(silent=True) or {}
    chk(f'R5 archive 경로 200 · live 와 같은 답 (받은 값 {ra.status_code})',
        ra.status_code == 200 and ja.get('contacts') == j.get('contacts') and ja.get('union_pct') == j.get('union_pct')
        and ja.get('am') == j.get('am'))
    # 오류
    codes = [c.get(f'/results/{cid}/am-contacts').status_code,
             c.get(f'/results/{cid}/am-contacts?am_id=abc').status_code,
             c.get(f'/results/{cid}/am-contacts?am_id=99999').status_code,
             c.get(f'/results/{cid}/am-contacts?am_id=10').status_code,
             c.get('/archive/results/no_such_folder/am-contacts?am_id=1').status_code]
    chk(f'R6 오류 — am_id 없음 400 · 숫자 아님 400 · 없는 id 404 · SE id 400 · 없는 archive 폴더 404 (받은 값 {codes})',
        codes == [400, 400, 404, 400, 404])
    cid2 = '261006_000003_amcatoms'
    live_case(up, rs, cid2, atoms, rows, contacts=False)
    r2 = c.get(f'/results/{cid2}/am-contacts?am_id=1')
    chk(f'R6b 접촉 덤프 없는 케이스 (atoms-only) = 404 · contacts.csv 가 없다고 말한다 (받은 값 {r2.status_code})',
        r2.status_code == 404 and 'contacts.csv' in (r2.get_data(as_text=True) or ''))
    cid3 = '261006_000004_amcnobox'
    live_case(up, rs, cid3, atoms, rows, input_params=False)
    j3 = c.get(f'/results/{cid3}/am-contacts?am_id=1').get_json(silent=True) or {}
    g3 = (j3.get('union_pct') or {}).get('g2') or {}
    p3 = {int(x['partner_id']): x for x in (j3.get('contacts') or [])}
    chk('R7 상자 (input_params.json) 없음 — 그리기는 뷰어와 같은 0.05 기본 (영상 자리 그대로) · box_source 표지 · '
        '보고 규칙 합집합은 빈칸 + 사유 (생산과 같은 계약 · 0.05 로 떨어지지 않는다)',
        j3.get('box_source') == 'default_0.05' and p3.get(10, {}).get('wrapped') is True
        and g3.get('value') is None and 'blank' in str(g3.get('status', '')), repr((j3.get('box_source'), g3)))
    return j


def build_real14_case(dst):
    raw = os.path.join(dst, '_raw')
    os.makedirs(raw, exist_ok=True)
    for gz, name in (('atom_2060000.liggghts.gz', 'atom_2060000.liggghts'),
                     ('contact_2060000.liggghts.gz', 'contact_2060000.liggghts')):
        with gzip.open(os.path.join(REF, gz), 'rb') as fi, open(os.path.join(raw, name), 'wb') as fo:
            shutil.copyfileobj(fi, fo)
    for name in ('mesh_2060000.stl', 'input_real_14.liggghts'):
        shutil.copy(os.path.join(REF, name), os.path.join(raw, name))
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'parse_liggghts.py'),
                        os.path.join(raw, 'atom_2060000.liggghts'), os.path.join(raw, 'contact_2060000.liggghts'),
                        os.path.join(raw, 'mesh_2060000.stl'), os.path.join(raw, 'input_real_14.liggghts'), '-o', dst],
                       capture_output=True, text=True, timeout=300)
    shutil.rmtree(raw, ignore_errors=True)
    return r.returncode == 0


def section_q(c, up, rs):
    print('[Q] real_14 기준 상태 — /am-contacts')
    import pandas as pd
    from coverage_physics_vs_hertzian import union_coverage_bed
    from plastic_coverage import union_cap_coverage, fibonacci_sphere
    cid = '261006_000005_real14'
    d = os.path.join(rs, cid)
    if not chk('Q0 real_14 덤프 → parse_liggghts (웹앱 파서) → 케이스 폴더', build_real14_case(d)):
        return
    os.makedirs(os.path.join(up, cid), exist_ok=True)
    with open(os.path.join(up, cid, 'meta.json'), 'w') as f:
        json.dump({'name': 'input_2mAh_real_14', 'type_map': TM_STR, 'scale': 1000, 'status': 'done'}, f)
    adf = pd.read_csv(os.path.join(d, 'atoms.csv'))
    cdf = pd.read_csv(os.path.join(d, 'contacts.csv'), low_memory=False)
    ty = dict(zip(adf['id'].astype(int), adf['type'].astype(int)))
    n_se = Counter()
    for a, b in zip(cdf['id1'].astype(int), cdf['id2'].astype(int)):
        if ty.get(a) in (1, 2) and ty.get(b) == 3:
            n_se[a] += 1
        elif ty.get(b) in (1, 2) and ty.get(a) == 3:
            n_se[b] += 1
    keys, per = union_coverage_bed(adf, cdf, TM, scale=1000.0, box_xy=(L, L))
    edge = adf[(adf.type == 1) & ((adf.x - adf.radius < 0) | (adf.x + adf.radius > L)
                                  | (adf.y - adf.radius < 0) | (adf.y + adf.radius > L))]
    picks = [('AM_P (경계)', int(edge.id.iloc[0])), ('AM_S', int(adf[adf.type == 2].id.iloc[0]))]
    U = fibonacci_sphere()
    for lab, aid in picks:
        j = c.get(f'/results/{cid}/am-contacts?am_id={aid}').get_json(silent=True) or {}
        cs = j.get('contacts') or []
        am = j.get('am') or {}
        g2 = (j.get('union_pct') or {}).get('g2') or {}
        print(f'      {lab} id {aid}: SE {j.get("n_se")} · AM {j.get("n_am")} · 영상 {j.get("n_wrapped")} · '
              f'그림 합집합 {((j.get("union_pct") or {}).get("hertz") or {}).get("value")} · 보고 규칙 {g2.get("value")} · '
              f'cap 합 {j.get("cap_sum_pct")}')
        chk(f'Q1 {lab} — SE 수 = 그 AM 의 AM–SE CN (독립 행 셈 {n_se[aid]})', j.get('n_se') == n_se[aid] and n_se[aid] > 0)
        chk(f'Q1b {lab} — 방향 검사 실패 0 (|d 최소영상| = r1 + r2 − δ)', j.get('n_dir_inconsistent') == 0
            and cs and all(x['geom_ok'] for x in cs))
        chk(f'Q2 {lab} — 보고 규칙 합집합 = 침대 전체 union_coverage_bed 의 입자 값 ({g2.get("value")} = {per.get(aid)})',
            keys.get('coverage_status_physics_union') == 'ok' and g2.get('value') is not None
            and abs(g2['value'] - per[aid]) < 1e-12)
        se_c = [x for x in cs if x.get('pair') == 'AM_SE']
        am_c = [x for x in cs if x.get('pair') == 'AM_AM']
        vec = lambda x: [x['x'] - am['x'], x['y'] - am['y'], x['z'] - am['z']]   # noqa: E731
        re_g = _try(lambda: union_cap_coverage(am['r'], [vec(x) for x in se_c], [x['area_g2_um2'] for x in se_c],
                                               [vec(x) for x in am_c], [x['area_g2_um2'] for x in am_c], points=U)[0])
        chk(f'Q2b {lab} — 경로의 방향 · 세대 2 면적으로 다시 재도 같다 (그린 cap = 보고 cap · {re_g})',
            bool(se_c) and re_g is not None and g2.get('value') is not None and abs(re_g - g2['value']) < 1e-9)
        if lab.startswith('AM_P'):
            chk(f'Q3 {lab} — 경계 걸친 AM 의 상대 일부는 영상 자리 (n_wrapped {j.get("n_wrapped")} > 0)',
                (j.get('n_wrapped') or 0) > 0)


def section_v():
    print('[V] viewer3d.js — AM 접촉 확대')
    js = open(VIEWER_JS, encoding='utf-8').read()
    try:
        bc = js_fn(js, 'buildControls')
    except (ValueError, AssertionError):
        bc = ''
    i_dem = bc.find('data-layer="SE"')
    btns = [m.start() for m in re.finditer(r'<button data-action="amContactCloseup"', bc)]
    chk('V1 DEM 조작판에만 버튼 (data-action="amContactCloseup") — MPM 조작판에는 없다 (접촉 덤프 없음)',
        len(btns) == 1 and i_dem >= 0 and btns[0] > i_dem, repr(btns))
    try:
        wc = js_fn(js, 'wireControls')
    except (ValueError, AssertionError):
        wc = ''
    chk("V1b 조작판 단추 → showAMContactCloseup(state)",
        re.search(r"action === 'amContactCloseup'\)\s*\{\s*showAMContactCloseup\(state\)", wc) is not None)
    try:
        sm = js_fn(js, 'showAMContactCloseup')
    except (ValueError, AssertionError):
        sm = ''
    chk('V2 모달 — 경로 = 3D 데이터 경로의 /3d-data → /am-contacts · am_id 질의',
        ".replace('/3d-data', '/am-contacts')" in sm and 'am_id=' in sm)
    chk('V2b 모달 — PNG = 4× · 투명 배경 (지우기 알파 0 · scene.background 없음) — 옛 AM Close-up 과 같은 내보내기',
        re.search(r'captureHighRes\(r3, s3, c3, 4\)', sm) is not None and 'setClearColor(0x000000, 0)' in sm
        and 's3.background = null' in sm)
    chk('V2c 모달 — 상대 입자 보기 토글 (#amcc-partners) · cap 규칙 (#amcc-rule: hertz · g2) · PC/SC 고르기 (#amcc-phase)',
        'id="amcc-partners"' in sm and re.search(r'id="amcc-rule"[\s\S]*value="hertz"[\s\S]*value="g2"', sm) is not None
        and re.search(r'id="amcc-phase"[\s\S]*AM_P \(PC\)[\s\S]*AM_S \(SC\)', sm) is not None)
    #  ★ 10-07 1저자 결정 — Coverage 그림의 노랑 = Physics 세대 2 (케이스 표의 보고 coverage 와 같은 cap) 가 **기본**
    chk('V2f ★ 기본 cap 넓이 = Physics 세대 2 (#amcc-rule 의 g2 option 이 selected · hertz 는 선택지로 남음 · 1저자 10-07)',
        re.search(r'<option value="g2" selected>', sm) is not None and '<option value="hertz" selected>' not in sm
        and 'value="hertz"' in sm)
    chk("V2d 모달 — SE 접촉 = 노란 cap · AM–AM 접촉 = 회색 cap (쌍 이름으로 가른다) · cap 각 = capHalfAngle",
        "pair === 'AM_SE'" in sm and "pair === 'AM_AM'" in sm and 'capHalfAngle(' in sm)
    chk('V2e 모달 — 이전 · 다음 · id 로 가기', 'id="amcc-prev"' in sm and 'id="amcc-next"' in sm and 'id="amcc-goto"' in sm)
    if not shutil.which('node'):
        chk('V3 node 필요', False, 'node 미설치')
        return
    names = ('capHalfAngle', 'cnPhaseLabel', 'cnFmt', 'amContactLegendHtml', 'amCloseupOrder')
    parts, miss = [], []
    for n in names:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    if not chk('V3 viewer3d.js 에서 함수 다섯 (cap 각 · 이름표 · 숫자 · 범례 · 후보 순서) 을 잘라 냈다', not miss, f'없음 {miss}'):
        return
    resp = {'am': {'id': 12, 'type': 'AM_P', 'r': 6.0, 'x': 25.0, 'y': 25.0, 'z': 12.0},
            'n_se': 351, 'n_am': 4, 'n_other': 0, 'n_wrapped': 3, 'n_dir_inconsistent': 0,
            'cap_sum_pct': {'hertz': 15.53, 'g2': 41.94},
            'union_pct': {'hertz': {'value': 14.21, 'status': 'ok'}, 'g2': {'value': 40.13, 'status': 'ok'}},
            'reported': {'label': 'AM_P', 'union_mean_pct': 39.718, 'union_status': 'ok', 'hertz_mean_pct': 18.399},
            'box_source': 'input_params'}
    blank = json.loads(json.dumps(resp))
    blank['union_pct']['g2'] = {'value': None, 'status': 'blank: 주기 상자 box 를 모른다'}
    blank['reported'] = {'label': 'AM_P', 'union_mean_pct': None, 'union_status': None, 'hertz_mean_pct': None}
    script = '\n'.join(parts) + '\nconst R = ' + json.dumps(resp) + ';\nconst B = ' + json.dumps(blank) + ''';
const R2 = 2 * Math.PI * 36;
const grid = Array.from({length: 101}, (_, i) => capHalfAngle(R2 * i / 100, 6));
const parts = [{id: 1, x: 0, y: 0, z: 0}, {id: 2, x: 25, y: 25, z: 15}, {id: 3, x: 30, y: 25, z: 15}];
console.log(JSON.stringify({
  a0: capHalfAngle(0, 6), a90: capHalfAngle(R2, 6), aOver: capHalfAngle(3 * Math.PI * 36, 6),
  aNeg: capHalfAngle(-1, 6), aNaN: capHalfAngle(NaN, 6), aR0: capHalfAngle(1, 0),
  aQ: capHalfAngle(R2 / 2, 6), grid,
  hH: amContactLegendHtml(R, 'hertz'), hG: amContactLegendHtml(R, 'g2'), hB: amContactLegendHtml(B, 'g2'),
  oC: amCloseupOrder(parts, {x_min: 0, x_max: 50, y_min: 0, y_max: 50, z_min: 0, z_max: 30}, {}, 'center').map(p => p.id),
  oT: amCloseupOrder(parts, {x_min: 0, x_max: 50, y_min: 0, y_max: 50, z_min: 0, z_max: 30}, {1: 10, 2: 30, 3: 21}, 'typical').map(p => p.id)}));
'''
    res = run_node(script)
    if not chk('V3b node 실행', res is not None):
        return
    mono = all(b >= a for a, b in zip(res['grid'], res['grid'][1:])) and res['grid'][0] == 0
    chk(f'V4 cap 각 — A 0 → 0 · A = 2πR² → 90° ({math.degrees(res["a90"]):.9f}°) · 단조 (101 점)',
        res['a0'] == 0 and abs(res['a90'] - math.pi / 2) < 1e-12 and mono)
    chk('V4b cap 각 — A = πR² (반구의 반) → cos θ = ½ → 60° · cos θ = 1 − A/(2πR²)',
        abs(res['aQ'] - math.pi / 3) < 1e-12, repr(res['aQ']))
    chk('V4c cap 각 — A > 2πR² 는 반구로 자른다 (생산 union_cap_coverage 와 같다) · 음수 · NaN · R 0 = cap 없음 (0)',
        abs(res['aOver'] - math.pi / 2) < 1e-12 and res['aNeg'] == 0 and res['aNaN'] == 0 and res['aR0'] == 0)
    h = res['hH']
    chk('V5 범례 — AM_P (PC) · SE 접촉 351 개 = 이 AM 의 AM–SE CN · AM–AM 4 개', 'AM_P (PC)' in h and '351' in h
        and 'AM–SE CN' in h and 'AM–AM' in h, h[:300])
    chk('V5b 범례 — 그림 노란 면적 = cap 합집합 14.2 % (겹침 한 번) · cap 단순 합 15.5 % 는 겹친 cap 을 두 번 셀 수 있다 (그림 설명용)',
        '14.2' in h and '합집합' in h and '15.5' in h and '두 번' in h and '그림 설명용' in h, h)
    chk('V5c 범례 — cap 넓이 출처 = c_cpl[22] (Hertz 계열 기하면적) · cap 각 식', 'c_cpl[22]' in h and '1 − A/(2πR²)' in h, h)
    chk('V5d 범례 — 보고 coverage = 케이스 표 합집합 · 이 AM (세대 2) 40.1 % · 침대 평균 AM_P 39.7 %',
        '40.1' in h and '39.7' in h and '케이스 표' in h, h)
    chk('V5e 범례 — 주기 영상 자리에 그린 상대 3 개', '3' in h and '영상' in h, h)
    g = res['hG']
    chk('V5f g2 규칙 — 그림 합집합 = 보고 규칙 (같은 cap) 이라 적는다 · 40.1 · cap 합 41.9',
        '40.1' in g and '41.9' in g and '보고 규칙과 같은 cap' in g, g)
    b = res['hB']
    chk('V5g 값이 없으면 — 0 으로 채우지 않고 — 와 사유 (blank)', '—' in b and 'blank' in b and '0.0 %' not in b, b)
    chk('V6 후보 순서 — center = 상자 중심에 가까운 순 · typical = AM–SE CN 이 평균 (20.33) 에 가까운 순',
        res['oC'] == [2, 3, 1] and res['oT'][0] == 3, repr((res['oC'], res['oT'])))


def main():
    tmp = tempfile.mkdtemp(prefix='viewer_amc_')
    try:
        webapp, c, up, rs, ar = setup_app(tmp)
        section_r(c, up, rs, ar)
        section_q(c, up, rs)
        section_v()
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

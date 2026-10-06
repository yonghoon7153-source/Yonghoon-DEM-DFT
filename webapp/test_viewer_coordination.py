#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D 뷰어 배위수 (CN) 보기 — 2026-10-06 1저자 요청 (보고 슬라이드 패널 "활물질 주위 SE 배위수" · PC = AM_P · SC = AM_S).

  python3 webapp/test_viewer_coordination.py      # 종료코드 0 = PASS

  [A] `viewer3d_data.aggregate_particle_metrics` 가 **입자별** CN 을 낸다 — SE–SE (SE 마다) · AM–SE (AM 마다) · AM–AM (AM 마다).
      접촉 정의 = `dem_analysis_core` 의 CN 함수 (`calc_se_se_cn` · `calc_am_isolation_risk` · `calc_am_am_cn`) 와 **같은 집합**:
      contacts.csv 행 하나 = 접촉 하나 · δ · 면적으로 거르지 않는다 (δ = 0 행도 센다) · 두 id 가 원자 표에 있어야 한다 · 같은 행이
      두 번이면 두 번.  상별 평균 = 그 함수들의 보고값 (full_metrics: se_se_cn · AM_P_se_cn_mean · AM_S_se_cn_mean · am_se_cn_mean ·
      am_am_cn — 접촉 0 인 입자 포함).
      A1 손으로 셀 수 있는 합성 접촉 · A2 같은 접촉에서 core 함수와 같은 평균 · A3 real_14 기준 상태 (커밋 덤프 → parse_liggghts →
      contacts.csv) = core = case_master 보고값.
  [C] 3D 데이터 캐시 스키마 11 → 12 (두 경로) — 옛 캐시는 다시 계산 · 새 캐시 HIT 에서도 CN 키가 살아 있다 (live · archive).
  [V] viewer3d.js — DEM 드롭다운 'cn' (MPM 조작판에는 없음) · applyViewMode 'cn' 분기 · 범례 (AM_P (PC) · AM_S (SC) · SE–SE 평균 · n)
      · 이산 색 구간 (node 로 함수를 잘라 그대로 돌린다).
"""
import csv
import gzip
import json
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
from test_closed_param_labels import js_fn, run_node   # noqa: E402  (렌더된 JS 를 잘라 node 로 — 같은 도구)

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


def close(a, b, tol=1e-12):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b)))


TM = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}

# ── 합성 침대 (손으로 센다) ─────────────────────────────────────────────────────────────────────────────────
#   AM_P 1 · 2 (2 는 접촉 0) · AM_S 3 · 4 · SE 10–16 (14 는 AM 접촉만 · 15 · 16 은 접촉 0)
ATOMS = {1: (1, 0.006), 2: (1, 0.006), 3: (2, 0.002), 4: (2, 0.002),
         10: (3, 0.0005), 11: (3, 0.0005), 12: (3, 0.0005), 13: (3, 0.0005), 14: (3, 0.0005), 15: (3, 0.0005),
         16: (3, 0.0005)}
#   (id1, id2, δ, 면적) — δ = 0 행 · 뒤집힌 순서 · 중복 행 · 원자 표에 없는 id 를 일부러 넣었다
ROWS = [(1, 10, 1e-5, 2e-7), (11, 1, 1e-5, 2e-7), (1, 12, 0.0, 0.0),
        (3, 13, 1e-5, 1e-7), (3, 14, 1e-5, 1e-7), (4, 14, 1e-5, 1e-7),
        (1, 3, 2e-5, 3e-7), (3, 4, 2e-5, 3e-7),
        (10, 11, 1e-5, 5e-8), (11, 12, 1e-5, 5e-8), (12, 13, 1e-5, 5e-8), (10, 11, 1e-5, 5e-8),
        (13, 999, 1e-5, 5e-8)]
WANT_AM_SE = {1: 3, 3: 2, 4: 1}                   # 2 = 0 (항목 없음)
WANT_AM_AM = {1: 1, 3: 2, 4: 1}
WANT_SE_SE = {10: 2, 11: 3, 12: 2, 13: 1}         # 14 · 15 · 16 = 0


def synth_inputs():
    atoms_by_id = {i: {'type': t, 'radius': r, 'x': 0.01 * (k % 4), 'y': 0.01 * (k // 4), 'z': 0.01}
                   for k, (i, (t, r)) in enumerate(ATOMS.items())}
    recs = [{'id1': a, 'id2': b, 'delta': d, 'contact_area': ar, 'fn_x': 0.0, 'fn_y': 0.0, 'fn_z': 1e-4}
            for a, b, d, ar in ROWS]
    return atoms_by_id, recs


def core_values(atoms, contacts):
    import dem_analysis_core as dac
    se = dac.calc_se_se_cn(atoms, contacts, [t for t, v in TM.items() if v == 'SE'])
    risk = dac.calc_am_isolation_risk(atoms, contacts, TM)
    amam = dac.calc_am_am_cn(atoms, contacts, [t for t, v in TM.items() if 'AM' in v])
    return se, risk, amam


def section_a_synth():
    print('[A] 입자별 CN — 손으로 센 합성 침대')
    import viewer3d_data as V
    atoms, recs = synth_inputs()
    agg = V.aggregate_particle_metrics(iter(recs), atoms, TM, scale=1000.0)
    got_se, got_am_se, got_am_am = (agg.get('cn_se_se'), agg.get('cn_am_se'), agg.get('cn_am_am'))

    def norm(d):
        return {int(k): int(v) for k, v in (d or {}).items() if v}
    chk('A1 SE–SE CN (SE 마다) = 손 계산 (중복 행 두 번 · 접촉 0 인 SE 는 항목 없음 = 0)',
        isinstance(got_se, dict) and norm(got_se) == WANT_SE_SE, repr(got_se))
    chk('A1b AM–SE CN (AM 마다) = 손 계산 (δ = 0 행도 센다 · 뒤집힌 순서 · 원자 표에 없는 id 는 안 센다)',
        isinstance(got_am_se, dict) and norm(got_am_se) == WANT_AM_SE, repr(got_am_se))
    chk('A1c AM–AM CN (AM 마다) = 손 계산', isinstance(got_am_am, dict) and norm(got_am_am) == WANT_AM_AM, repr(got_am_am))
    sm = agg.get('cn_summary') or {}
    ph = sm.get('phases') or {}
    se, risk, amam = core_values(atoms, recs)
    chk('A2 상별 평균 = core 함수 — SE–SE (calc_se_se_cn mean · 접촉 0 포함) 8/7',
        close((ph.get('SE') or {}).get('se_se_mean'), se['mean']) and close(se['mean'], 8 / 7), repr(ph.get('SE')))
    chk('A2b AM_P · AM_S AM–SE 평균 = calc_am_isolation_risk {상}_se_cn_mean (1.5 · 1.5)',
        close((ph.get('AM_P') or {}).get('am_se_mean'), risk['AM_P_se_cn_mean'])
        and close((ph.get('AM_S') or {}).get('am_se_mean'), risk['AM_S_se_cn_mean']), repr(ph))
    chk('A2c AM 전체 AM–SE 평균 = am_se_cn_mean · AM–AM 평균 = calc_am_am_cn mean (1.0)',
        close(sm.get('am_se_mean_all'), risk['am_se_cn_mean']) and close(sm.get('am_am_mean_all'), amam['mean']),
        repr({k: sm.get(k) for k in ('am_se_mean_all', 'am_am_mean_all')}))
    chk('A2d n = 상의 입자 수 (AM_P 2 · AM_S 2 · SE 7) · 접촉 0 인 입자 수 (AM_P 1 · SE 3)',
        [(ph.get(k) or {}).get('n') for k in ('AM_P', 'AM_S', 'SE')] == [2, 2, 7]
        and (ph.get('AM_P') or {}).get('am_se_n_zero') == 1 and (ph.get('SE') or {}).get('se_se_n_zero') == 3, repr(ph))
    chk('A2e 접촉 정의 문구가 요약에 실린다 (δ · 면적으로 거르지 않는다 · core 함수 이름)',
        'calc_se_se_cn' in str(sm.get('rule', '')) and 'calc_am_isolation_risk' in str(sm.get('rule', '')),
        str(sm.get('rule', ''))[:160])
    chk('A2f 행 수 (SE–SE 4 · AM–SE 6 · AM–AM 2 · 원자 표에 없는 id 1)',
        (sm.get('n_rows') or {}) == {'se_se': 4, 'am_se': 6, 'am_am': 2, 'other': 0, 'unknown_id': 1}, repr(sm.get('n_rows')))
    # 기존 키 불변 — 이 묶음은 키를 더할 뿐이다
    chk('A2g 기존 출력 키는 그대로 (stress_max · se_engagement · tabor_stats · brittle_pairs …)',
        all(k in agg for k in ('stress_max', 'dr_max', 'brittle_pairs', 'se_stress_pairs', 'am_se_stress_pairs',
                               'particle_max_fpc', 'stress_chain_segments', 'tabor_stats', 'se_engagement')))


def build_real14_case(dst):
    """커밋 덤프 → parse_liggghts (웹앱 파이프라인과 같은 파서) → atoms.csv · contacts.csv · input_params.json."""
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


def section_a_real14(tmp):
    print('[A3] real_14 기준 상태 — 뷰어 평균 = core 함수 = 보고값 (case_master)')
    import pandas as pd
    import viewer3d_data as V
    import analyze_contacts as AC
    d = os.path.join(tmp, 'real14')
    os.makedirs(d)
    if not chk('A3 real_14 덤프 → parse_liggghts → contacts.csv (웹앱 파서)', build_real14_case(d)):
        return
    # 뷰어 경로 = /3d-data 와 같은 읽기 (pandas · itertuples 행 스트림)
    df = pd.read_csv(os.path.join(d, 'atoms.csv'))
    atoms_by_id = {int(r.id): {'type': int(r.type), 'radius': float(r.radius), 'x': float(r.x), 'y': float(r.y),
                               'z': float(r.z)} for r in df.itertuples(index=False)}
    cdf = pd.read_csv(os.path.join(d, 'contacts.csv'), low_memory=False)
    cols = list(cdf.columns)
    agg = V.aggregate_particle_metrics((dict(zip(cols, t)) for t in cdf.itertuples(index=False, name=None)),
                                       atoms_by_id, TM, scale=1000.0)
    sm = agg.get('cn_summary') or {}
    ph = sm.get('phases') or {}
    # core = 생산 분석기 (analyze_contacts) 와 같은 읽기
    atoms_raw, _ = AC.load_atoms_raw(os.path.join(d, 'atoms.csv'))
    contacts_raw, _ = AC.load_contacts_raw(os.path.join(d, 'contacts.csv'))
    se, risk, amam = core_values(atoms_raw, contacts_raw)
    vals = {'AM_P': (ph.get('AM_P') or {}).get('am_se_mean'), 'AM_S': (ph.get('AM_S') or {}).get('am_se_mean'),
            'SE': (ph.get('SE') or {}).get('se_se_mean'), 'AM': sm.get('am_se_mean_all'), 'AMAM': sm.get('am_am_mean_all')}
    print(f'      뷰어 AM_P (PC) {vals["AM_P"]} · AM_S (SC) {vals["AM_S"]} · SE–SE {vals["SE"]} · AM 전체 {vals["AM"]} · '
          f'AM–AM {vals["AMAM"]}')
    chk('A3b 뷰어 상별 평균 = core 함수 (같은 contacts.csv · 생산 분석기 읽기) — 정확히 같다',
        vals['AM_P'] == risk['AM_P_se_cn_mean'] and vals['AM_S'] == risk['AM_S_se_cn_mean'] and vals['SE'] == se['mean']
        and vals['AM'] == risk['am_se_cn_mean'] and vals['AMAM'] == amam['mean'],
        repr((vals, risk['AM_P_se_cn_mean'], risk['AM_S_se_cn_mean'], se['mean'])))
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'docs', 'data', 'case_master.csv'), encoding='utf-8')))
    cm = next((r for r in rows if r.get('name') == 'input_2mAh_real_14'), {})
    chk('A3c 뷰어 평균 = 보고값 (case_master real_14: AM_P_se_cn_mean 348.111 · AM_S_se_cn_mean 44.577 · se_se_cn 4.5446 · '
        'am_se_cn_mean 68.488 · am_am_cn 2.8884)',
        cm and close(vals['AM_P'], cm['AM_P_se_cn_mean'], 1e-12) and close(vals['AM_S'], cm['AM_S_se_cn_mean'], 1e-12)
        and close(vals['SE'], cm['se_se_cn'], 1e-12) and close(vals['AM'], cm['am_se_cn_mean'], 1e-12)
        and close(vals['AMAM'], cm['am_am_cn'], 1e-12),
        repr({k: cm.get(k) for k in ('AM_P_se_cn_mean', 'AM_S_se_cn_mean', 'se_se_cn', 'am_se_cn_mean', 'am_am_cn')}))
    chk('A3d n — AM_P 36 · AM_S 421 · SE 32832 (덤프 원자 수)',
        [(ph.get(k) or {}).get('n') for k in ('AM_P', 'AM_S', 'SE')] == [36, 421, 32832], repr(ph))
    # 입자별 값 = 독립 셈 (행 단위 Counter)
    ty = {int(r.id): TM[int(r.type)] for r in df.itertuples(index=False)}
    c_se, c_am_se, c_am_am = Counter(), Counter(), Counter()
    for a, b in zip(cdf['id1'].astype(int), cdf['id2'].astype(int)):
        ta, tb = ty.get(a), ty.get(b)
        if ta is None or tb is None:
            continue
        if ta == 'SE' and tb == 'SE':
            c_se[a] += 1
            c_se[b] += 1
        elif 'AM' in ta and 'AM' in tb:
            c_am_am[a] += 1
            c_am_am[b] += 1
        elif 'AM' in ta and tb == 'SE':
            c_am_se[a] += 1
        elif 'AM' in tb and ta == 'SE':
            c_am_se[b] += 1
    n = lambda dd: {int(k): int(v) for k, v in (dd or {}).items() if v}   # noqa: E731
    chk('A3e 입자별 맵 = 독립 행 셈 (SE–SE 32832 개 · AM–SE · AM–AM 457 개)',
        n(agg.get('cn_se_se')) == dict(c_se) and n(agg.get('cn_am_se')) == dict(c_am_se)
        and n(agg.get('cn_am_am')) == dict(c_am_am))
    return d


# ── [C] 캐시 스키마 ────────────────────────────────────────────────────────────────────────────────────────
def write_synth_case(folder, meta=True):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, 'atoms.csv'), 'w') as f:
        f.write('id,type,x,y,z,radius\n')
        for k, (i, (t, r)) in enumerate(ATOMS.items()):
            f.write(f'{i},{t},{0.004 + 0.004 * (k % 4)},{0.004 + 0.004 * (k // 4)},0.01,{r}\n')
    with open(os.path.join(folder, 'contacts.csv'), 'w') as f:
        f.write('id1,id2,fn_x,fn_y,fn_z,contact_area,delta\n')
        for a, b, d, ar in ROWS:
            f.write(f'{a},{b},0,0,0.0001,{ar},{d}\n')
    with open(os.path.join(folder, 'input_params.json'), 'w') as f:
        json.dump({'box_x': 0.05, 'box_y': 0.05}, f)
    if meta:
        with open(os.path.join(folder, 'meta.json'), 'w') as f:
            json.dump({'name': 'cn_synth', 'type_map': '1:AM_P,2:AM_S,3:SE', 'scale': 1000, 'status': 'done'}, f)


def section_c_cache(tmp):
    print('[C] 3D 데이터 캐시 — 스키마 12 · 옛 캐시 다시 계산 · HIT 에서도 CN 키 (live · archive)')
    src = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
    n12 = len(re.findall(r"_schema'\)\s*==\s*12\b", src))
    w12 = len(re.findall(r"\['_schema'\]\s*=\s*12\b", src))
    n11 = len(re.findall(r"_schema'\)\s*==\s*11\b", src)) + len(re.findall(r"\['_schema'\]\s*=\s*11\b", src))
    chk(f'C0 두 경로 (live · archive) 모두 스키마 12 를 읽고 쓴다 · 11 은 남지 않는다 (읽기 {n12} · 쓰기 {w12} · 옛 {n11})',
        n12 == 2 and w12 == 2 and n11 == 0)
    up, rs, ar = (os.path.join(tmp, k) for k in ('uploads', 'results', 'archive'))
    for p in (up, rs, ar):
        os.makedirs(p, exist_ok=True)
    os.environ['WEBAPP_UPLOAD_FOLDER'], os.environ['WEBAPP_RESULTS_FOLDER'] = up, rs
    os.environ['WEBAPP_ARCHIVE_FOLDER'] = ar
    import app as webapp
    webapp.app.config['UPLOAD_FOLDER'], webapp.app.config['RESULTS_FOLDER'] = up, rs
    webapp.app.config['ARCHIVE_FOLDER'] = ar
    c = webapp.app.test_client()
    cid = '261006_000001_cnsynth'
    write_synth_case(os.path.join(up, cid))                    # meta.json → uploads (case_dir)
    write_synth_case(os.path.join(rs, cid), meta=False)        # atoms · contacts → results
    cache = os.path.join(rs, cid, 'viewer_aux.json')
    #   옛 스키마 캐시 — 같은 contacts.csv mtime · CN 키 없음 → 다시 계산해야 한다
    with open(cache, 'w') as f:
        json.dump({'_schema': 11, '_contacts_mtime': os.path.getmtime(os.path.join(rs, cid, 'contacts.csv')),
                   'stress_max': {}, 'se_engagement': {}}, f)
    j = c.get(f'/results/{cid}/3d-data').get_json(silent=True) or {}
    aux = j.get('aux') or {}
    cn1 = {k: aux.get(k) for k in ('cn_se_se', 'cn_am_se', 'cn_am_am', 'cn_summary')}
    chk('C1 옛 캐시 (스키마 11) → 다시 계산 · aux 에 CN 키 넷 (cn_se_se · cn_am_se · cn_am_am · cn_summary)',
        all(isinstance(v, dict) and v for v in cn1.values()), repr({k: type(v).__name__ for k, v in cn1.items()}))
    chk('C1b JSON 의 입자별 값 = 손 계산 (키는 문자열 id)',
        {int(k): v for k, v in (cn1['cn_am_se'] or {}).items()} == WANT_AM_SE
        and {int(k): v for k, v in (cn1['cn_se_se'] or {}).items()} == WANT_SE_SE)
    blob = json.load(open(cache)) if os.path.exists(cache) else {}
    chk('C1c 새 캐시는 스키마 12 로 쓰고 CN 키를 담는다', blob.get('_schema') == 12 and 'cn_summary' in blob, repr(blob.get('_schema')))
    j2 = c.get(f'/results/{cid}/3d-data').get_json(silent=True) or {}
    aux2 = j2.get('aux') or {}
    chk('C2 두 번째 요청 (캐시 HIT) 도 같은 CN 값 (live)',
        all(cn1[k] and aux2.get(k) == cn1[k] for k in cn1), repr({k: aux2.get(k) == cn1[k] for k in cn1}))
    # archive — 같은 파일을 한 폴더에
    af = os.path.join(ar, 'cn_synth_case')
    write_synth_case(af)
    ja = c.get('/archive/results/cn_synth_case/3d-data').get_json(silent=True) or {}
    auxa = ja.get('aux') or {}
    chk('C3 archive 경로도 CN 키 넷 (첫 요청 = 계산)', all(isinstance(auxa.get(k), dict) and auxa.get(k) for k in cn1),
        repr(sorted(auxa)[:12]))
    ja2 = c.get('/archive/results/cn_synth_case/3d-data').get_json(silent=True) or {}
    auxa2 = ja2.get('aux') or {}
    chk('C3b archive 캐시 HIT 에서도 CN 키 · 값이 산다 (archive 의 키 목록 복원에 CN 넷을 더했다)',
        all(auxa2.get(k) == auxa.get(k) and auxa2.get(k) for k in cn1),
        repr({k: bool(auxa2.get(k)) for k in cn1}))


# ── [V] viewer3d.js ─────────────────────────────────────────────────────────────────────────────────────────
def section_v():
    print('[V] viewer3d.js — 배위수 보기')
    js = open(VIEWER_JS, encoding='utf-8').read()
    try:
        bc = js_fn(js, 'buildControls')
    except (ValueError, AssertionError):
        bc = ''
    sels = re.findall(r'<select id="view-mode".*?</select>', bc, re.S)
    opts = [re.findall(r'<option value="([^"]+)"', s) for s in sels]
    chk('V1 DEM 조작판 드롭다운에 cn (배위수) — MPM 조작판에는 없다 (접촉망 없음)',
        len(opts) == 2 and 'cn' not in opts[0] and 'cn' in opts[1], repr([len(o) for o in opts]))
    m = re.search(r'<option value="cn">([^<]*)</option>', bc)
    chk('V1b 이름표 = 배위수 · 활물질 주위 SE · SE–SE', m is not None and '배위수' in m.group(1) and 'SE–SE' in m.group(1)
        and '활물질 주위 SE' in m.group(1), m.group(1) if m else '')
    try:
        avm = js_fn(js, 'applyViewMode')
    except (ValueError, AssertionError):
        avm = ''
    try:
        br = js_fn(js, 'applyCnView')
    except (ValueError, AssertionError):
        br = ''
    chk("V2 applyViewMode 에 'cn' 분기 → applyCnView(state) — 앞쪽 공통 정리 (다른 모드의 오버레이 · AM 색 되돌림) 뒤에 탄다",
        re.search(r"if \(mode === 'cn'\)\s*\{[^}]*applyCnView\(state\);\s*return;", avm) is not None
        and avm.find("mode === 'cn'") > avm.find('state.brittleGlowGroup = null'))
    chk('V2a applyCnView — AM 은 cn_am_se · SE 는 cn_se_se 로 칠하고 범례는 cn_summary',
        'aux.cn_am_se' in br and 'aux.cn_se_se' in br and 'aux.cn_summary' in br, br[:200])
    chk('V2b 옛 캐시 · atoms-only (cn_summary 없음) = 칠하지 않고 이유를 적는다 (0 으로 채우지 않는다)',
        re.search(r'if \(!sm \|\| !sm\.phases\)', br) is not None and '배위수 자료' in br)
    if not shutil.which('node'):
        chk('V3 node 필요 (범례 · 구간 함수를 실제로 돌린다)', False, 'node 미설치')
        return
    names = ('cnPhaseLabel', 'cnFmt', 'cnNiceBins', 'cnBinIndex', 'cnClassColor', 'cnLegendHtml')
    parts, miss = [], []
    for n in names:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    if not chk('V3 viewer3d.js 에서 배위수 함수 여섯을 잘라 냈다', not miss, f'없음 {miss}'):
        return
    summary = {'rule': 'r', 'phases': {
        'AM_P': {'kind': 'AM', 'n': 36, 'am_se_mean': 348.1111111111111, 'am_se_std': 44.57314698446549,
                 'am_se_median': 351.0, 'am_se_max': 439, 'am_se_min': 249, 'am_se_n_zero': 0, 'am_am_mean': 4.2},
        'AM_S': {'kind': 'AM', 'n': 421, 'am_se_mean': 44.57719714964371, 'am_se_std': 8.803845668645694,
                 'am_se_median': 45.0, 'am_se_max': 69, 'am_se_min': 0, 'am_se_n_zero': 2, 'am_am_mean': 2.7},
        'SE': {'kind': 'SE', 'n': 32832, 'se_se_mean': 4.544590643274854, 'se_se_std': 2.00199948250334,
               'se_se_median': 5.0, 'se_se_max': 16, 'se_se_min': 0, 'se_se_n_zero': 598}},
        'am_se_mean_all': 68.48796498905908, 'am_am_mean_all': 2.888402625820569, 'n_am_all': 457}
    script = '\n'.join(parts) + '\nconst S = ' + json.dumps(summary) + ''';
const vP = [249, 300, 351, 439, 260, 410], vS = [0, 0, 21, 45, 69, 33];
const bP = cnNiceBins(vP, 6), bS = cnNiceBins(vS.filter(v => v > 0), 6);
const idxP = vP.map(v => cnBinIndex(v, bP)), idxS = vS.filter(v => v > 0).map(v => cnBinIndex(v, bS));
const html = cnLegendHtml(S, {AM_P: bP, AM_S: bS, SE: {start: 1, step: 1, n: 8, openTop: true}});
const cols = [0, 1, 2, 3, 4, 5].map(i => cnClassColor(i, 6, 'AM'));
console.log(JSON.stringify({bP, bS, idxP, idxS, html, labP: cnPhaseLabel('AM_P'), labS: cnPhaseLabel('AM_S'),
  labSE: cnPhaseLabel('SE'), f1: cnFmt(348.1111), f2: cnFmt(4.5446), cols, se8: cnBinIndex(16, {start: 1, step: 1, n: 8, openTop: true})}));
'''
    res = run_node(script)
    if not chk('V3b node 실행', res is not None):
        return
    print(f"      AM_P 구간 {res['bP']} · AM_S 구간 {res['bS']}")
    chk('V4 이름표 — AM_P (PC) · AM_S (SC) · SE 그대로', res['labP'] == 'AM_P (PC)' and res['labS'] == 'AM_S (SC)'
        and res['labSE'] == 'SE', repr((res['labP'], res['labS'], res['labSE'])))
    bp, bs = res['bP'], res['bS']
    okP = bp['step'] in (1, 2, 5, 10, 20, 50, 100) and bp['start'] <= 249 and bp['start'] + bp['n'] * bp['step'] > 439
    okS = bs['step'] in (1, 2, 5, 10, 20, 50) and bs['start'] <= 21 and bs['start'] + bs['n'] * bs['step'] > 69
    chk('V5 이산 구간 — 깔끔한 정수 폭 (1 · 2 · 5 × 10ⁿ) · 최솟값 · 최댓값을 덮는다 · 구간 수 ≤ 6',
        okP and okS and bp['n'] <= 6 and bs['n'] <= 6, repr((bp, bs)))
    chk('V5b 구간 번호는 값 순서를 따른다 (단조) · 범위 안', all(0 <= k < bp['n'] for k in res['idxP'])
        and [res['idxP'][i] for i in (0, 1, 2, 3)] == sorted(res['idxP'][i] for i in (0, 1, 2, 3)), repr(res['idxP']))
    chk('V5c SE 열린 윗구간 — 16 은 마지막 구간 (≥ 8)', res['se8'] == 7, repr(res['se8']))
    chk('V5d 구간 색이 서로 다르다 (6 개)', len(set(res['cols'])) == 6, repr(res['cols']))
    h = res['html']
    chk('V6 범례 — AM_P (PC) AM–SE 평균 348.1 ± 44.6 · n = 36', 'AM_P (PC)' in h and '348.1' in h and '44.6' in h
        and 'n = 36' in h, h[:300])
    chk('V6b 범례 — AM_S (SC) AM–SE 평균 44.6 · n = 421 · 접촉 0 인 AM 2 개', 'AM_S (SC)' in h and 'n = 421' in h
        and '44.6' in h, h[:300])
    chk('V6c 범례 — SE–SE 평균 4.54 · n = 32832 (천 단위 쉼표 없음)', 'SE–SE' in h and '4.54' in h and 'n = 32832' in h
        and '32,832' not in h, h[:300])
    chk('V6d 범례 — 케이스 표 배위수와 같은 접촉 집합이라 적는다 · AM–AM 평균 2.89', '같은 접촉 집합' in h and '2.89' in h, h[-400:])
    chk('V6e 범례 — 한 상만 남기는 법 (체크박스) 을 적는다', '체크박스' in h)


def main():
    tmp = tempfile.mkdtemp(prefix='viewer_cn_')
    try:
        section_a_synth()
        section_a_real14(tmp)
        section_c_cache(tmp)
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

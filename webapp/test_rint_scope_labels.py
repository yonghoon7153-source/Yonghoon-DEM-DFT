#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""① 계면 저항 G1-3 화면 표지 — Codex r_int 1단계 `RINT-04` · `05` · `17` · `18` (10-03 · 1저자 비준 G1 · J20-l).

  A  Joule 범위 표지 `jouleScopeNote` (node 로 그대로) — bulk-only · 지도 밖 계면 몫 % · 옛 payload = 범위 표지 없음 ·
     총 발열 hotspot 으로 읽지 말라는 문구 · payload 문자열 이스케이프
  B  반응전류 범위 표지 `rxnScopeNote` — r-ON 에서 끈 반응 솔브의 사유를 말한다 (데이터가 없는 이유) · 정상 rxn = 빈 문자열
  C  배선 — Joule 필드 범례 · 반응전류 단일 범례 (데이터 없음 가지 포함) · 비교 캡션이 표지를 부른다
  D  RINT-18 — 손실 분담 막대 · 범례 = "상/계면" (계면은 상이 아니다)
  E  RINT-17 — STEP4 R_int 화면 표지 = 셀 단자 ASR (내부 상 경계 r_int 와 다른 양)
  F  RGL-01 (Codex 10-05) — 집전체 기하 (component `collector_geom`) 표지: 보조 솔브 (wetted · bare) 둘 다 수렴해야 R_geom ·
     jb 게시.  `collectorGeomNote` · `rGeomText` (node) — 미수렴 · 실패 · 옛 payload (수렴 3필드 없음) 를 말하고 null R_geom 을
     "0.00e+0" 으로 그리지 않는다 · 수렴 키 = producer · 공용 계약 (`run_contract.COMPONENT_RESULT`) 과 같은 글자 ·
     배선 (je · je_delta 범례 · jb 없음 가지 · 요약 칩 · CSV 상태 행 · 비교 캡션) · 템플릿 둘 (mpm_lab 요약 · 케이스 카드)

  python3 webapp/test_rint_scope_labels.py
"""
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_closed_param_labels import js_fn, run_node   # noqa: E402

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return cond


with open(os.path.join(HERE, 'static', 'js', 'viewer3d.js'), encoding='utf-8') as f:
    JS = f.read()


def block(src, start, end):
    i = src.find(start)
    if i < 0:
        return ''
    j = src.find(end, i + len(start))
    return src[i:j] if j > 0 else ''


print('A · B  표지 함수 (node)')
have = all(f'function {n}(' in JS for n in ('jouleScopeNote', 'rxnScopeNote', 'jeEscH'))
if not shutil.which('node'):
    chk('A0 node 필요', False, 'node 미설치')
elif not have:
    chk('A0 jouleScopeNote · rxnScopeNote · jeEscH 가 뷰어에 있다', False, '정의 없음')
else:
    cases = {
        'none': None,
        'nojoule': {'sigma_e_eff_S_cm': 0.05},
        'old': {'joule': {'hot_frac_50': 0.4, 'conc_ratio': 3.0}},
        'bulk_r': {'joule': {'scope': 'bulk_only', 'excluded': ['interface_I2R', 'plate_coupling'],
                             'interface_share_outside_map': 0.9524}},
        'bulk_off': {'joule': {'scope': 'bulk_only', 'excluded': ['interface_I2R', 'plate_coupling'],
                               'interface_share_outside_map': 0.0}},
        'weird': {'joule': {'scope': '<b>x</b>'}},
        'rxn_ok': {'rxn': {'n_bv_faces': 120, 'active_am_pct': 88.0}},
        'rxn_off': {'rxn': {'status': 'disabled', 'reason': 'r_int ON <script> — 막 없는 반응수송 (RINT-05)'}},
    }
    script = (js_fn(JS, 'jeEscH') + '\n' + js_fn(JS, 'jouleScopeNote') + '\n' + js_fn(JS, 'rxnScopeNote') + '\n'
              + 'const C = ' + json.dumps(cases) + ';\nconst out = {};\n'
              + 'for (const k of Object.keys(C)) { out["j_" + k] = jouleScopeNote(C[k]); out["r_" + k] = rxnScopeNote(C[k]); }\n'
              + 'console.log(JSON.stringify(out));\n')
    r = run_node(script)
    if chk('A0 node 실행', r is not None):
        chk('A1 Joule 없음 · step3 없음 = 빈 문자열', r['j_none'] == '' and r['j_nojoule'] == '')
        chk('A2 옛 payload (scope 없음) = 범위 표지 없음 경고', '범위 표지 없음' in r['j_old'], r['j_old'])
        chk('A3 bulk-only · 지도 밖 계면 몫 95 % · 총 발열로 읽지 말 것',
            'bulk' in r['j_bulk_r'] and '95' in r['j_bulk_r'] and '지도 밖' in r['j_bulk_r']
            and '총 발열' in r['j_bulk_r'], r['j_bulk_r'])
        chk('A4 r 없음 (계면 몫 0) 도 bulk-only 표지 · 판 결합 제외를 말한다',
            'bulk' in r['j_bulk_off'] and '판' in r['j_bulk_off'], r['j_bulk_off'])
        chk('A5 payload 문자열 이스케이프', '<b>x' not in r['j_weird'], r['j_weird'])
        chk('B1 정상 rxn · 없음 = 빈 문자열', r['r_rxn_ok'] == '' and r['r_none'] == '' and r['r_nojoule'] == '')
        chk('B2 r-ON 으로 끈 반응 솔브 = 사유 · RINT-05 · 이스케이프',
            'RINT-05' in r['r_rxn_off'] and '<script>' not in r['r_rxn_off'] and '막 없는' in r['r_rxn_off'],
            r['r_rxn_off'])

print('C  배선')
jfield = block(JS, "const joule = mode === 'jt_field';", "\n  if (mode === ")
chk('C1 Joule 필드 범례가 jouleScopeNote(s3)', 'jouleScopeNote(s3)' in jfield)
jr = block(JS, "if (mode === 'jrxn') {", "\n  if (mode === ")
nodata = block(jr, 'if (!vals.length) {', 'return;')
chk('C2 반응전류 단일 범례 — 데이터 없음 가지에서도 rxnScopeNote(s3) (끈 이유를 말한다)', 'rxnScopeNote(s3)' in nodata)
cmp_rx = block(JS, "} else if (mode === 'jrxn') {", "} else if (mode === 'je_delta') {")
chk('C3 비교 반응전류 캡션이 rxnScopeNote', 'rxnScopeNote(' in cmp_rx)

print('D  RINT-18 상/계면')
chk('D1 "각 상의 전력손실 %" 문구가 없다', '각 상의 전력손실 %' not in JS)
chk('D2 손실 분담 막대 = "각 상/계면의 전력손실 %" (전자 · 이온)', JS.count('각 상/계면의 전력손실 %') >= 2)
chk('D3 je 범례 손실 분담 = 상/계면', '손실(발열) 분담 (상/계면)' in JS)

print('E  RINT-17 단자 R_int')
rint_lbls = re.findall(r"R_int[^`'\"]{0,12}\$\{st\.r_int_ohm_cm2\}", JS)
chk('E1 STEP4 화면의 R_int 표지 (그림 제목 · 범례) 가 셀 단자 ASR 라고 말한다',
    len(rint_lbls) >= 2 and all('단자' in x for x in rint_lbls), repr(rint_lbls))

print('F  RGL-01 집전체 기하 (collector_geom) — 보조 솔브 수렴 표지')
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
try:
    import run_contract as _RC
    _convs = [k for t in _RC.COMPONENT_RESULT['collector_geom'].get('convs', ()) for k in t]
except Exception as e:   # noqa: BLE001
    _convs = []
    print('    run_contract import 실패:', e)
_mk = re.search(r'const COLLECTOR_CONV_KEYS = \[([^\]]*)\];', JS)
_jk = re.findall(r"'([^']+)'", _mk.group(1)) if _mk else []
chk('F0 뷰어 수렴 키 = 공용 계약 (run_contract.COMPONENT_RESULT collector_geom convs) 과 같은 글자 · 여섯',
    len(_convs) == 6 and _jk == _convs, f'js={_jk} rc={_convs}')
have_f = all(f'function {n}(' in JS for n in ('collectorGeomNote', 'rGeomText', 'jeEscH')) and _mk
if not shutil.which('node'):
    chk('F1 node 필요', False, 'node 미설치')
elif not have_f:
    chk('F1 collectorGeomNote · rGeomText · COLLECTOR_CONV_KEYS 가 뷰어에 있다', False, '정의 없음')
else:
    _ok_cg = {'wetted_sigma_S_cm': 0.08, 'bare_sigma_S_cm': 0.05, 'R_geom_ohm_cm2': 1.2e-4,
              'wetted_cg_info': 0, 'wetted_unconverged': False, 'wetted_cg_resid': 1e-9,
              'bare_cg_info': 0, 'bare_unconverged': False, 'bare_cg_resid': 1e-9}
    _old_cg = {k: v for k, v in _ok_cg.items() if 'cg_' not in k and 'unconverged' not in k}

    def _s3(cg, st=None, reason=None):
        o = {'sigma_e_eff_S_cm': 0.05}
        if cg is not None:
            o['collector_geometric'] = cg
        if st is not None:
            o['manifest'] = {'components': {'collector_geom': dict({'status': st}, **({'reason': reason} if reason else {}))}}
        return o
    fcases = {
        'none': None,
        'nocg': _s3(None),
        'disabled': _s3(None, 'disabled'),
        'ok': _s3(_ok_cg, 'complete'),
        'unconv': _s3(dict(_ok_cg, R_geom_ohm_cm2=None, bare_cg_info=1, bare_unconverged=True, bare_cg_resid=0.35),
                      'unconverged', '보조 솔브 미수렴 — bare(unconv) <script>'),
        'failed': _s3(dict(_ok_cg, R_geom_ohm_cm2=None, bare_reason='no_plate_contact'), 'failed',
                      'solve degenerate (bare/wetted 중 하나가 비퍼콜)'),
        'old': _s3(_old_cg, 'complete'),
        'nullr': _s3(dict(_ok_cg, R_geom_ohm_cm2=None), 'complete'),
    }
    fscript = (_mk.group(0) + '\n' + js_fn(JS, 'jeEscH') + '\n' + js_fn(JS, 'rGeomText') + '\n'
               + js_fn(JS, 'collectorGeomNote') + '\n'
               + 'const C = ' + json.dumps(fcases) + ';\nconst out = {};\n'
               + 'for (const k of Object.keys(C)) { out["n_" + k] = collectorGeomNote(C[k]); '
               + 'out["p_" + k] = collectorGeomNote(C[k], true); out["r_" + k] = C[k] ? rGeomText(C[k]) : null; }\n'
               + 'console.log(JSON.stringify(out));\n')
    f = run_node(fscript)
    if chk('F1 node 실행', f is not None):
        chk('F2 집전체 기하 없음 · --no-collector · 정상 (수렴 3필드 + R_geom) = 빈 문자열',
            f['n_none'] == '' and f['n_nocg'] == '' and f['n_disabled'] == '' and f['n_ok'] == '', repr(f['n_ok']))
        chk('F3 unconverged = collector_geom 미수렴 · R_geom · jb 미게시 · RGL-01 · 사유 이스케이프',
            all(s in f['n_unconv'] for s in ('collector_geom', '미수렴', 'jb', 'RGL-01'))
            and '<script>' not in f['n_unconv'] and '&lt;script&gt;' in f['n_unconv'], f['n_unconv'])
        chk('F4 failed = 실패 · 사유', '실패' in f['n_failed'] and '비퍼콜' in f['n_failed'], f['n_failed'])
        chk('F5 옛 payload (수렴 3필드 없음) = 수렴 확인 없이 게시된 R_geom 경고 · RGL-01',
            '옛 payload' in f['n_old'] and 'RGL-01' in f['n_old'], f['n_old'])
        chk('F6 상태 complete 인데 R_geom null = R_geom 없음 경고', 'R_geom 없음' in f['n_nullr'], f['n_nullr'])
        chk('F7 rGeomText — 수 = 지수 표기 · null = "—" (옛 범례의 Number(null) → "0.00e+0" 아님)',
            f['r_ok'] == '1.20e-4' and f['r_unconv'] == '—' and f['r_failed'] == '—' and f['r_nullr'] == '—',
            repr((f['r_ok'], f['r_unconv'])))
        chk('F8 평문 판 (캔버스) 에 태그 없음 · 같은 판정',
            all('<div' not in f['p_' + k] for k in ('unconv', 'failed', 'old')) and '미수렴' in f['p_unconv'])
single_dl = block(JS, "if (mode === 'je_delta') {", "if (mode === 'je') {")
single_je = block(JS, "if (mode === 'je') {", "if (mode === 'additives'")
nojb = block(single_dl, 'if (!have) {', 'return;')
chips = block(JS, 'const chips = [', "['porosity (공극률)'")
csvsum = block(JS, 'function summaryCsv()', "row('scalar', 'porosity_pct'")
cmp_dl = block(JS, "} else if (mode === 'je_delta') {", "} else if (mode === 'pore') {")
chk('F9 옛 R_geom 서식 (Number(cg.R_geom_ohm_cm2).toExponential) 이 뷰어 어디에도 없다',
    'Number(cg.R_geom_ohm_cm2)' not in JS)
chk('F10 je_delta 범례 = rGeomText · collectorGeomNote · jb 없음 가지가 collectorGeomNote 로 이유를 말한다',
    'rGeomText(s3)' in single_dl and 'collectorGeomNote(s3)' in single_dl and 'collectorGeomNote(' in nojb)
chk('F11 je 범례 = rGeomText · collectorGeomNote · 상세에 "둘 다 수렴" 문구',
    'rGeomText(s3)' in single_je and 'collectorGeomNote(s3)' in single_je and '둘 다</b> 수렴' in single_je)
chk('F12 요약 칩 R_geom = rGeomText · 값 없으면 collector_geom 상태', 'rGeomText(s3)' in chips and 'collector_geom' in chips)
chk('F13 CSV 요약에 collector_geom_status 행', "'collector_geom_status'" in csvsum)
chk('F14 비교 je_delta 캡션이 collectorGeomNote', 'collectorGeomNote(' in cmp_dl)
with open(os.path.join(HERE, 'templates', 'mpm_lab.html'), encoding='utf-8') as _f:
    _lab = _f.read()
with open(os.path.join(HERE, 'templates', 'single.html'), encoding='utf-8') as _f:
    _sgl = _f.read()
_lab_cg = block(_lab, 'const cg = s3s.collector_geometric', "L.push('');")
_sgl_cg = block(_sgl, 'const cg = s3m.collector_geometric', 'const selC')
chk('F15 mpm_lab 요약 · 케이스 카드 — R_geom 이 없으면 collector_geom 상태 (unconverged = 보조 솔브 미수렴 · RGL-01) 를 적는다',
    all('collector_geom' in t and 'unconverged' in t and 'RGL-01' in t for t in (_lab_cg, _sgl_cg)),
    repr((len(_lab_cg), len(_sgl_cg))))

print(f'\n{_ok} PASS · {len(_fail)} FAIL')
if _fail:
    for n in _fail:
        print('  -', n)
    sys.exit(1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""① 계면 저항 G1-3 화면 표지 — Codex r_int 1단계 `RINT-04` · `05` · `17` · `18` (10-03 · 1저자 비준 G1 · J20-l).

  A  Joule 범위 표지 `jouleScopeNote` (node 로 그대로) — bulk-only · 지도 밖 계면 몫 % · 옛 payload = 범위 표지 없음 ·
     총 발열 hotspot 으로 읽지 말라는 문구 · payload 문자열 이스케이프
  B  반응전류 범위 표지 `rxnScopeNote` — r-ON 에서 끈 반응 솔브의 사유를 말한다 (데이터가 없는 이유) · 정상 rxn = 빈 문자열
  C  배선 — Joule 필드 범례 · 반응전류 단일 범례 (데이터 없음 가지 포함) · 비교 캡션이 표지를 부른다
  D  RINT-18 — 손실 분담 막대 · 범례 = "상/계면" (계면은 상이 아니다)
  E  RINT-17 — STEP4 R_int 화면 표지 = 셀 단자 ASR (내부 상 경계 r_int 와 다른 양)

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

print(f'\n{_ok} PASS · {len(_fail)} FAIL')
if _fail:
    for n in _fail:
        print('  -', n)
    sys.exit(1)

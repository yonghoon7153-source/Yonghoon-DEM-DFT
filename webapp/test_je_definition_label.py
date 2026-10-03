#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""입자별 전류 je · jb 의 **정의 표지** — Codex r_int 1단계 `RINT-03` (10-03 · 1저자 비준 G1 묶음).

`step3_sigma.per_particle_current` 는 입자 번호 pid 가 같은 셀의 |J_z| 를 평균한다.  옛 정의는 AM 자리를 덮은
탄소 · 첨가제 셀 (스탬프가 pid 를 남긴다) 의 전류까지 AM 몫에 넣었다 (r 를 끈 실침대에서도 — 계면 항 무관).
G1 수정은 **최종 상이 AM (sid 1 · 2) 인 셀만** 평균하도록 바꿨다 (`PER_PARTICLE_CURRENT_DEF = 'am-final-sid-v2'`).
같은 이름 `je` 가 정의 둘을 갖게 됐으므로 화면이 그것을 말해야 한다 — 옛 payload 를 새 것처럼 읽지 않게.

  A  payload 가 step3 성공 가지에 `je_definition = _s3.PER_PARTICLE_CURRENT_DEF` 를 싣는다 (AST)
     · 뷰어의 v2 상수가 솔버 상수와 같은 글자다 (사본이 갈라지면 전부 '알 수 없는 정의' 가 된다)
  B  `jeDefNote` 를 잘라 node 로 돌린다 — 없음 = 옛 정의 경고 (RINT-03) · v2 = 'AM 셀만' · 모르는 값 = 해석 보류
     (payload 문자열은 HTML 이스케이프) · 평문 판 (캔버스 약어표) 에 태그 없음 · step3 없음 = 빈 문자열
  C  `jeDefMismatch` — A/B 정의가 다르면 경고 (옛 ↔ v2 포함) · 같으면 빈 문자열
  D  배선 — 단일 모드 je · je_delta 범례 · 비교 모드 je · je_delta 캡션 · 대시보드 약어표가 표지를 부른다

  python3 webapp/test_je_definition_label.py
"""
import ast
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from test_closed_param_labels import js_fn, run_node   # noqa: E402  (같은 도구 — 렌더된 JS 를 잘라 node 로)

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


VIEWER = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
PAYLOAD = os.path.join(ROOT, 'scripts', 'mpm_webapp_payload.py')
with open(VIEWER, encoding='utf-8') as f:
    JS = f.read()
with open(PAYLOAD, encoding='utf-8') as f:
    PY = f.read()


def block(src, start, end):
    """src 에서 start 부터 그 뒤 처음 나오는 end 앞까지 (없으면 '')."""
    i = src.find(start)
    if i < 0:
        return ''
    j = src.find(end, i + len(start))
    return src[i:j] if j > 0 else ''


# ── A  payload · 상수 단일 출처 ─────────────────────────────────────────────
print('A  payload 가 정의를 싣는다 · 상수가 한 글자')
try:
    import step3_sigma as _s3
    DEF = getattr(_s3, 'PER_PARTICLE_CURRENT_DEF', None)
except Exception as e:   # noqa: BLE001
    DEF = None
    print('    import 실패:', e)
chk('A1 솔버 상수 PER_PARTICLE_CURRENT_DEF = am-final-sid-v2', DEF == 'am-final-sid-v2', repr(DEF))

found = []
for node in ast.walk(ast.parse(PY)):
    if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict)):
        continue
    if not any(isinstance(t, ast.Name) and t.id == 'step3' for t in node.targets):
        continue
    keys = {k.value: v for k, v in zip(node.value.keys, node.value.values)
            if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    if 'n_dof' in keys:                                    # 성공 가지 (σ_e 를 푼 쪽)
        v = keys.get('je_definition')
        found.append(isinstance(v, ast.Attribute) and v.attr == 'PER_PARTICLE_CURRENT_DEF'
                     and isinstance(v.value, ast.Name) and v.value.id == '_s3')
chk('A2 step3 성공 가지 dict 가 하나', len(found) == 1, f'{len(found)} 개')
chk('A3 그 dict 에 je_definition = _s3.PER_PARTICLE_CURRENT_DEF (사본 글자 아님)', found == [True], repr(found))

m = re.search(r"const JE_DEF_V2 = '([^']*)';", JS)
chk('A4 뷰어 v2 상수 = 솔버 상수 (갈라지면 새 payload 도 "알 수 없는 정의")',
    bool(m) and m.group(1) == DEF, m.group(1) if m else '상수 없음')

# ── B · C  node 로 그대로 돌린다 ─────────────────────────────────────────────
print('B  jeDefNote · C  jeDefMismatch (node)')
if not shutil.which('node'):
    chk('B0 node 필요 (표지 함수를 실제로 돌린다)', False, 'node 미설치')
elif not ('function jeDefNote(' in JS and 'function jeDefMismatch(' in JS and 'function jeEscH(' in JS and m):
    chk('B0 jeDefNote · jeDefMismatch · jeEscH · JE_DEF_V2 가 뷰어에 있다', False, '정의 없음')
else:
    cases = {
        'none': None,
        'empty': {},                                        # 비교 모드의 `mm.step3 || {}` = STEP3 없음
        'old': {'sigma_e_eff_S_cm': 0.05},                 # 옛 payload — STEP3 는 있는데 정의 키가 없다
        'old_null': {'sigma_e_eff_S_cm': 0.05, 'je_definition': None},
        'v2': {'sigma_e_eff_S_cm': 0.05, 'je_definition': 'am-final-sid-v2'},
        'weird': {'sigma_e_eff_S_cm': 0.05, 'je_definition': '<img src=x onerror=alert(1)>'},
    }
    script = (m.group(0) + '\n' + js_fn(JS, 'jeEscH') + '\n' + js_fn(JS, 'jeDefNote') + '\n'
              + js_fn(JS, 'jeDefMismatch') + '\n'
              + 'const C = ' + json.dumps(cases) + ';\n'
              + 'const out = {};\n'
              + 'for (const k of Object.keys(C)) { out[k] = jeDefNote(C[k]); out[k + "_plain"] = jeDefNote(C[k], true); }\n'
              + 'out.mm_v2_old = jeDefMismatch(C.v2, C.old);\n'
              + 'out.mm_old_v2 = jeDefMismatch(C.old, C.v2);\n'
              + 'out.mm_v2_v2 = jeDefMismatch(C.v2, C.v2);\n'
              + 'out.mm_old_old = jeDefMismatch(C.old, C.old_null);\n'
              + 'out.mm_none_none = jeDefMismatch(null, null);\n'
              + 'out.mm_v2_empty = jeDefMismatch(C.v2, C.empty);\n'
              + 'out.mm_weird_v2 = jeDefMismatch(C.weird, C.v2);\n'
              + 'console.log(JSON.stringify(out));\n')
    r = run_node(script)
    if chk('B0 node 실행', r is not None):
        chk('B1 step3 없음 (null · 빈 dict) = 빈 문자열 — je 자체가 없다',
            r['none'] == '' and r['none_plain'] == '' and r['empty'] == '', repr((r['none'], r['empty'])))
        chk('B2 정의 없음 = 옛 정의 경고 (RINT-03)', '옛 정의' in r['old'] and 'RINT-03' in r['old'], r['old'])
        chk('B3 정의 null 도 옛 정의 (값 없음 ≠ 새 정의)', '옛 정의' in r['old_null'], r['old_null'])
        chk('B4 v2 = "AM 셀만" · 경고 표시 없음', 'AM 셀만' in r['v2'] and '⚠' not in r['v2'], r['v2'])
        chk('B5 모르는 정의 = 해석 보류', '알 수 없는' in r['weird'], r['weird'])
        chk('B6 payload 문자열은 이스케이프 (태그 주입 없음)',
            '<img' not in r['weird'] and '&lt;img' in r['weird'], r['weird'])
        chk('B7 평문 판에 HTML 태그 없음 (캔버스 약어표용)',
            all('<div' not in r[k + '_plain'] for k in ('old', 'v2', 'weird')))
        chk('B8 평문 판도 같은 판정 (옛 · v2)',
            '옛 정의' in r['old_plain'] and 'AM 셀만' in r['v2_plain'])
        chk('C1 옛 ↔ v2 = 경고 (양방향)',
            'RINT-03' in r['mm_v2_old'] and 'RINT-03' in r['mm_old_v2'], r['mm_v2_old'])
        chk('C2 같은 정의 = 빈 문자열 (v2·v2 · 옛·옛(null) · 둘 다 step3 없음)',
            r['mm_v2_v2'] == '' and r['mm_old_old'] == '' and r['mm_none_none'] == '',
            repr((r['mm_v2_v2'], r['mm_old_old'], r['mm_none_none'])))
        chk('C3 불일치 경고에도 payload 문자열 이스케이프', '<img' not in r['mm_weird_v2'], r['mm_weird_v2'])
        chk('C4 한쪽에 STEP3 가 없으면 불일치 경고 없음 (비교할 je 가 없다)', r['mm_v2_empty'] == '',
            r['mm_v2_empty'])

# ── D  배선 ──────────────────────────────────────────────────────────────
print('D  배선 — 표지를 부르는 자리')
single_je = block(JS, "if (mode === 'je') {", "if (mode === 'additives'")
single_dl = block(JS, "if (mode === 'je_delta') {", "if (mode === 'je') {")
cmp_je = block(JS, "} else if (mode === 'je') {", "} else if (mode === 'jrxn') {")
cmp_dl = block(JS, "} else if (mode === 'je_delta') {", "} else if (mode === 'pore') {")
gloss = block(JS, 'const gloss = [', '];')
chk('D1 단일 je 범례가 jeDefNote(s3)', 'jeDefNote(s3)' in single_je)
chk('D2 단일 je_delta 범례가 jeDefNote(s3) (jb/je 둘 다 같은 함수)', 'jeDefNote(s3)' in single_dl)
chk('D3 비교 je 캡션이 jeDefNote · jeDefMismatch', 'jeDefNote(' in cmp_je and 'jeDefMismatch(sA, sB)' in cmp_je)
chk('D4 비교 je_delta 캡션이 jeDefNote · jeDefMismatch',
    'jeDefNote(' in cmp_dl and 'jeDefMismatch(sA, sB)' in cmp_dl)
chk('D5 대시보드 약어표 je 줄이 평문 표지 (jeDefNote(s3, true))', 'jeDefNote(s3, true)' in gloss)

print(f'\n{_ok} PASS · {len(_fail)} FAIL')
if _fail:
    for n in _fail:
        print('  -', n)
    sys.exit(1)

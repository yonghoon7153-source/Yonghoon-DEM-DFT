#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""siteq_probe.py 의 C02b (PATH 의 python3 환경 단위 대조) 회귀 — Codex Rint ② 회차 ⑥ RR6-01 (P3 · 11-10).

RR6-01: C02b 가 자식 python3 의 종료 코드를 보지 않아, 환경 JSON 을 찍고 rc 1 로 끝난 자식도 PASS 였다
(`docs/reviews/codex_review_rint2_rr_round6_20261110.md` §4).  고친 뒤 계약:

  ① 같은 단위 + rc 0 → PASS · 결과 data 에 자식 rc (`path_python3_rc` = 0) 가 남는다
  ② 같은 단위 + rc 1 → FAIL (고치기 전 = PASS · 이것이 반례)
  ③ 다른 단위 + rc 0 → FAIL
  ④ JSON 깨짐 + rc 0 → FAIL
  ⑤ PATH 에 python3 없음 → FAIL (자식 안 띄움)
  ⑥ rc 가 정수가 아닌 값 (None) → FAIL

방법 = Codex 탐침과 같다: siteq_probe.py 를 import 하지 않고 c02b 함수 정의만 AST 로 떼어 컴파일하고,
shutil · subprocess · RR 을 메모리 가짜로 바꾼다 (실제 자식 프로세스 · 호스트 탐침 0 회).

  python3 -I -B docs/reviews/rint2_siteq_prep_20261109/tools/test_siteq_c02b.py
"""
import ast
import json
import posixpath
import sys
from pathlib import Path
from types import SimpleNamespace

SRC = Path(__file__).resolve().parent / 'siteq_probe.py'
UNIT = {'python_minor': '3.8', 'numpy': '1.24.4', 'scipy': '1.10.1'}

_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print('  PASS', name)
    else:
        _fail.append(name)
        print('  FAIL', name)


def load_c02b(run_result, which='/synthetic/python3'):
    """c02b 정의만 컴파일 · 바깥 입출력은 가짜.  run_result = 가짜 subprocess.run 이 돌려줄 값."""
    tree = ast.parse(SRC.read_bytes(), filename=str(SRC))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'c02b']
    assert len(nodes) == 1, 'c02b 정의가 정확히 하나여야 한다'
    calls = []

    def fake_run(argv, **kw):
        calls.append(argv)
        return run_result

    ns = {
        'shutil': SimpleNamespace(which=lambda _name: which),
        'sys': SimpleNamespace(executable='/synthetic/python3'),
        'subprocess': SimpleNamespace(run=fake_run, DEVNULL=-3, PIPE=-1),
        'json': json,
        'RR': SimpleNamespace(env_record=lambda: {'unit': dict(UNIT)}),
        'os': SimpleNamespace(path=SimpleNamespace(abspath=posixpath.abspath)),
        'UNIT_SNIPPET': 'NOT EXECUTED',
    }
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SRC), 'exec'), ns)
    return ns['c02b'], calls


def child(rc, unit=None, raw=None):
    out = raw if raw is not None else json.dumps(unit if unit is not None else UNIT).encode()
    return SimpleNamespace(returncode=rc, stdout=out, stderr=b'')


def main():
    print('── C02b 자식 종료 코드 (RR6-01)')
    f, calls = load_c02b(child(0))
    st, detail, data = f()
    chk('① 같은 단위 + rc 0 → PASS', st == 'PASS')
    chk('① data 에 자식 rc 0 이 남는다 (path_python3_rc)', data.get('path_python3_rc') == 0)
    chk('① detail 에 rc 가 보인다', 'rc 0' in detail)
    chk('① 자식은 한 번 · python3 -I', len(calls) == 1 and calls[0][:2] == ['/synthetic/python3', '-I'])

    f, _ = load_c02b(child(1))
    st, detail, data = f()
    chk('② 같은 단위 + rc 1 → FAIL (고치기 전 = PASS)', st == 'FAIL')
    chk('② data 에 자식 rc 1 이 남는다', data.get('path_python3_rc') == 1)

    f, _ = load_c02b(child(0, unit=dict(UNIT, numpy='2.0.0')))
    st, _, _ = f()
    chk('③ 다른 단위 + rc 0 → FAIL', st == 'FAIL')

    f, _ = load_c02b(child(0, raw=b'{not json'))
    st, _, data = f()
    chk('④ JSON 깨짐 + rc 0 → FAIL', st == 'FAIL' and data.get('path_python3_unit') is None)

    f, calls = load_c02b(child(0), which=None)
    st, _, data = f()
    chk('⑤ PATH 에 python3 없음 → FAIL · 자식 안 띄움', st == 'FAIL' and calls == [])

    f, _ = load_c02b(SimpleNamespace(returncode=None, stdout=json.dumps(UNIT).encode(), stderr=b''))
    st, _, _ = f()
    chk('⑥ rc 가 정수 아님 (None) → FAIL', st == 'FAIL')

    print(f'\n== test_siteq_c02b: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('   실패: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 10 회차 (독립) RC01 스캐너 탐침 — ① 시험의 `rc_scan` 이 못 잡는 rc 읽기 꼴 (작은 반례) ② 실제 원천 (scripts/rint_r_chain.py) 의
'rc' 낱말 전수 (상수 · 속성 · 이름 · match 열쇠) 를 독립 AST 로 찾아 문맥을 적는다 (스캐너가 0 을 낸 것이 원천에 그 꼴이 없어서인지 본다).

쓰는 법: python3 -I probe_rcscan.py <scripts 폴더> <출력 json>
"""
import ast
import json
import sys
from pathlib import Path

SCRIPTS, OUT = sys.argv[1], sys.argv[2]
sys.path.insert(0, SCRIPTS)
import test_rint_r_chain as T  # noqa: E402

EVADE = {
    'dict_value_launder': "def f(er):\n    d = {'v': er.get('rc')}\n    return d['v'] == 0\n",
    'dict_kw_launder': "def f(er):\n    d = dict(v=er.get('rc'))\n    return d['v'] == 0\n",
    'subscript_target_launder': "def f(er, rec):\n    rec['ok'] = er.get('rc')\n    return rec['ok'] == 0\n",
    'attribute_rc': "def f(r):\n    return r.rc == 0\n",
    'dict_get_unbound': "def f(er):\n    return dict.get(er, 'rc') == 0\n",
    'pop': "def f(er):\n    return er.pop('rc') == 0\n",
    'setdefault': "def f(er):\n    return er.setdefault('rc', 1) == 0\n",
    'itemgetter': "import operator\ndef f(er):\n    return operator.itemgetter('rc')(er) == 0\n",
    'match_mapping': "def f(er):\n    match er:\n        case {'rc': 0}:\n            return True\n    return False\n",
    'variable_key': "K = 'rc'\ndef f(er):\n    return er.get(K) == 0\n",
    'closure_alias': "def f(er):\n    x = er.get('rc')\n    def g():\n        return x == 0\n    return g()\n",
    'starred_arg': "def f(er):\n    return er.get(*['rc']) == 0\n",
    'getattr_get': "def f(er):\n    return getattr(er, 'get')('rc') == 0\n",
    'items_loop': "def f(er):\n    for k, v in er.items():\n        if k == 'rc' and v == 0:\n            return 1\n",
    'fstring_compare': "def f(er):\n    return f\"{er.get('rc')}\" == '0'\n",
    'json_text': "def f(raw):\n    return '\"rc\":0' in raw\n",
    'ifexp_launder': "def f(er, c):\n    x = er.get('rc') if c else None\n    return x == 0\n",
}
CTRL = {   # 잡혀야 하는 대조 (스캐너가 이것들은 잡는다)
    'alias_eq': "def f(er):\n    x = er.get('rc')\n    return x == 0\n",
    'truthy': "def f(er):\n    return not er.get('rc')\n",
    'int_wrap': "def f(rc):\n    return int(rc) == 0\n",
    'walrus': "def f(er):\n    return (x := er.get('rc')) == 0\n",
    'return_alias': "def f(er):\n    x = er.get('rc')\n    return x\n",
}
res = {'evade': {k: bool(T.rc_scan(s)) for k, s in EVADE.items()}, 'ctrl': {k: bool(T.rc_scan(s)) for k, s in CTRL.items()}}

src_path = Path(SCRIPTS) / 'rint_r_chain.py'
src = src_path.read_text(encoding='utf-8')
tree = ast.parse(src)
par = {}
for n in ast.walk(tree):
    for ch in ast.iter_child_nodes(n):
        par[ch] = n


def fn_of(n):
    p = par.get(n)
    while p is not None and not isinstance(p, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        p = par.get(p)
    return p.name if p is not None else '<모듈>'


hits = []
for n in ast.walk(tree):
    kind = None
    if isinstance(n, ast.Constant) and n.value == 'rc':
        kind = 'const'
    elif isinstance(n, ast.Attribute) and n.attr == 'rc':
        kind = 'attr'
    elif isinstance(n, ast.keyword) and n.arg == 'rc':
        kind = 'kwarg'
    elif isinstance(n, ast.Name) and n.id == 'rc' and isinstance(n.ctx, ast.Load):
        kind = 'name'
    elif hasattr(ast, 'MatchMapping') and isinstance(n, ast.MatchMapping):
        kind = 'match'
    if kind:
        p = par.get(n)
        seg = ast.get_source_segment(src, p if p is not None else n) or ''
        hits.append({'line': getattr(n, 'lineno', getattr(p, 'lineno', 0)), 'kind': kind, 'fn': fn_of(n), 'parent': type(p).__name__,
                     'seg': ' '.join(seg.split())[:110]})
hits.sort(key=lambda h: h['line'])
res['source'] = {'path': str(src_path), 'rc_scan_raw': T.rc_scan(src), 'n_hits': len(hits), 'hits': hits,
                 'n_attr': sum(h['kind'] == 'attr' for h in hits), 'n_match': sum(h['kind'] == 'match' for h in hits)}
Path(OUT).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('evade (True = 잡힘):', res['evade'])
print('ctrl  (True = 잡힘):', res['ctrl'])
print('source rc_scan raw:', len(res['source']['rc_scan_raw']), '· rc 낱말 자리', res['source']['n_hits'], '· 속성 .rc', res['source']['n_attr'],
      '· match', res['source']['n_match'])
for h in hits:
    print(f"  {h['line']:5d} {h['kind']:6s} {h['fn'][:24]:24s} {h['parent']:12s} {h['seg']}")

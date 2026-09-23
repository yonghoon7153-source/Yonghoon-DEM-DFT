#!/usr/bin/env python3
"""미정의 이름 정적 검사 — **긴 런이 끝난 뒤** NameError 로 죽는 것을 막는다.

★ 왜 (실사고 2026-08-16): 사전등록 판별 런이 SE 점 6,792 만 개를 읽고 메쉬까지 만든 **뒤**
  `NameError: _zt3` 로 죽었다.  내가 정의를 옮긴다면서 주석만 넣고 대입을 빠뜨린 것이다.
  GPU 시간을 그만큼 버렸고, 더 나쁘게는 STEP3 를 `try` 가 삼켜 "skipped" 로만 찍혀서
  **조용히 σ 없는 payload 가 나올 뻔했다**.
  ⇒ 런 **전에** 정적으로 잡는다.  pyflakes 가 있으면 그것을, 없으면 AST 로 최소 검사.

★ 한계 (넘겨짚지 말 것): 정적 검사는 **동적 이름**(globals()/setattr/exec)을 못 본다.
  "미정의 없음" 이 "런이 성공한다" 는 뜻이 아니다 — NameError **한 부류**만 막는다.

사용:
  python3 scripts/check_undefined_names.py                 # scripts/**/*.py 전부
  python3 scripts/check_undefined_names.py --selftest
"""
from __future__ import annotations

import argparse
import ast
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def with_pyflakes(paths):
    """(errors, available) — pyflakes 가 있으면 그 결과를 쓴다 (훨씬 정확하다)."""
    try:
        r = subprocess.run([sys.executable, '-m', 'pyflakes'] + paths,
                           capture_output=True, text=True, timeout=300)
    except Exception:
        return [], False
    if 'No module named' in (r.stderr or ''):
        return [], False
    #  ⚠ **NameError 를 내는 부류만** 남긴다.  "assigned to but never used" 는 미사용이지
    #    미정의가 아니다 — 그걸로 게이트를 막으면 281 건이 잡혀 검사기를 끄게 된다
    #    (오탐이 많으면 규칙이 없는 것보다 나쁘다 — 규칙 F 에서 이미 배운 것).
    keep = [ln for ln in (r.stdout or '').splitlines()
            if 'undefined name' in ln or 'referenced before assignment' in ln]
    return keep, True


def with_ast(path):
    """pyflakes 가 없을 때의 최소 검사 — 함수 안에서 **어디서도 대입되지 않은** 이름 사용."""
    try:
        tree = ast.parse(open(path, encoding='utf-8').read())
    except SyntaxError as ex:
        return [f'{path}: SyntaxError {ex}']
    #  ★ 2026-09-23 — `dir(__builtins__)` 는 이 파일이 **import 될 때** dict 라 `float`·`list` 가 빠진다
    #    (스크립트로 돌 때만 모듈).  `builtins` 모듈을 직접 읽는다.
    import builtins as _bi
    mod_names = set(dir(_bi)) | {'__file__', '__name__', '__doc__'}
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for al in n.names:
                mod_names.add((al.asname or al.name).split('.')[0])
        elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            mod_names.add(n.id)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            mod_names.add(n.name)
    def _scope_bound(f):
        """함수 노드 f 안에서 묶이는 이름 — 자기 인자 · 대입 · import · 정의 · except · 하위 스코프 인자 · match."""
        b = set()
        for a in list(f.args.args) + list(f.args.kwonlyargs) + list(f.args.posonlyargs):
            b.add(a.arg)
        if f.args.vararg:
            b.add(f.args.vararg.arg)
        if f.args.kwarg:
            b.add(f.args.kwarg.arg)
        for n in ast.walk(f):
            if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                b.add(n.id)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                for al in n.names:
                    b.add((al.asname or al.name).split('.')[0])
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                b.add(n.name)
            elif isinstance(n, ast.ExceptHandler) and n.name:
                b.add(n.name)
            #  ★ 2026-09-23 (Lee 러너 실사고, 오탐 129 건) — `ast.walk(f)` 는 **중첩 함수·lambda 속까지**
            #    내려가는데 그 **자기 인자**는 바인딩에 안 넣었다 → `def chk(c, m): … c …` 의 `c` 가 바깥
            #    함수 기준으로 "미정의" 가 됐다.  스코프를 근사한다: 하위 스코프 인자는 바인딩으로 본다
            #    (바깥 함수에서 같은 이름을 미정의로 쓰는 드문 경우는 놓친다 — 최소 검사의 한계로 적는다).
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)) and n is not f:
                _aa = n.args
                for a in list(_aa.args) + list(_aa.kwonlyargs) + list(_aa.posonlyargs):
                    b.add(a.arg)
                for a in (_aa.vararg, _aa.kwarg):
                    if a is not None:
                        b.add(a.arg)
            #  match 문 캡처 (3.10+) 도 Name Store 가 아니다.
            elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name:
                b.add(n.name)
            elif isinstance(n, ast.MatchMapping) and n.rest:
                b.add(n.rest)
        return b

    #  ★ 2026-09-23 — **클로저**: 안쪽 함수는 바깥 함수의 지역을 읽는다 (`_filt` 가 바깥의 `in_am` 을 읽는
    #    additives.py:600 모양).  함수마다 **둘러싼 함수들의 바인딩**을 같이 본다.
    parent = {}
    for n in ast.walk(tree):
        for ch in ast.iter_child_nodes(n):
            parent[ch] = n
    out = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        bound = set(mod_names) | _scope_bound(fn)
        up = parent.get(fn)
        while up is not None:
            if isinstance(up, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                bound |= _scope_bound(up) if not isinstance(up, ast.Lambda) else set()
            up = parent.get(up)
        for n in ast.walk(fn):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id not in bound:
                out.append(f'{path}:{n.lineno}: undefined name {n.id!r} in {fn.name}')
    return out


def scan(paths):
    errs, have = with_pyflakes(paths)
    if have:
        return errs, 'pyflakes'
    out = []
    for p in paths:
        out += with_ast(p)
    return out, 'ast(최소)'


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    import tempfile
    d = tempfile.mkdtemp()
    bad_p = os.path.join(d, 'bad.py')
    open(bad_p, 'w').write('def f():\n    return _never_defined + 1\n')
    good_p = os.path.join(d, 'good.py')
    open(good_p, 'w').write('import os\n\n\ndef f():\n    x = 1\n    return os.sep, x\n')
    # ★ 실사고 재현 — 정의를 빠뜨린 그 모양
    real_p = os.path.join(d, 'real.py')
    open(real_p, 'w').write('def f(z):\n    #  _zt3 정의를 빠뜨렸다\n    return solve(z_top=_zt3)\n')

    e_bad, how = scan([bad_p])
    chk(f'① 미정의 이름을 잡는다 ({how}): {len(e_bad)} 건', len(e_bad) >= 1)
    e_good, _ = scan([good_p])
    chk(f'② 정상 파일은 오탐 없음: {len(e_good)} 건', len(e_good) == 0)
    e_real, _ = scan([real_p])
    chk(f'③ ★ 실사고 모양(_zt3 대입 누락)을 잡는다: {len(e_real)} 건', len(e_real) >= 1)
    # ── ★ 2026-09-23 (Lee STEP3 러너 실사고) — **AST 대체 경로를 직접** 시험한다.  위 ①~③ 은
    #    `scan()` 이라 pyflakes 가 있으면 대체 경로를 **한 번도 안 탄다**.  v100 conda env 에 pyflakes 가
    #    없어 대체 경로로 떨어졌고, 중첩 함수·lambda 의 **자기 인자**를 바깥 함수 기준으로 봐서
    #    runner 5 파일에 오탐 **129 건** → 러너가 GPU 를 잡기 전에 ABORT 했다 (pyflakes 로는 0 건).
    nest_p = os.path.join(d, 'nest.py')
    open(nest_p, 'w').write('def outer(xs):\n'
                            '    def chk(c, m):\n'
                            '        return c and m\n'
                            '    ys = sorted(xs, key=lambda r: r[0])\n'
                            '    return chk(float(len(ys)), list(ys))\n')
    e_nest = with_ast(nest_p)
    chk(f'④ AST 대체: 중첩 함수·lambda 의 **자기 인자**는 미정의가 아니다 (sr01:476 `chk(c, m)` 모양): '
        f'{len(e_nest)} 건', len(e_nest) == 0)
    nest_bad_p = os.path.join(d, 'nest_bad.py')
    open(nest_bad_p, 'w').write('def outer():\n    def inner(a):\n        return a + _zt3\n    return inner(1)\n')
    e_nb = with_ast(nest_bad_p)
    chk(f'⑤ AST 대체: 중첩 함수 안의 **진짜** 미정의(_zt3)는 여전히 잡는다: {len(e_nb)} 건',
        any("'_zt3'" in e for e in e_nb))
    clo_p = os.path.join(d, 'clo.py')
    open(clo_p, 'w').write('def outer():\n    k = 3\n    def inner(x):\n        return x + k\n    return inner(1)\n')
    e_clo = with_ast(clo_p)
    chk(f'⑤b AST 대체: 클로저 — 안쪽 함수가 바깥 지역(k)을 읽는 것은 미정의가 아니다: {len(e_clo)} 건',
        len(e_clo) == 0)
    e_real_ast = with_ast(real_p)
    chk(f'⑥ AST 대체: 실사고 모양도 대체 경로에서 잡는다: {len(e_real_ast)} 건', len(e_real_ast) >= 1)
    _runner = [os.path.join(ROOT, 'scripts', f) for f in
               ('mpm_webapp_payload.py', 'step3_sigma.py', 'viz_mpm_continuum.py', 'additives.py',
                'sr01_stamp_compare.py')]
    if all(os.path.exists(p) for p in _runner):
        e_run = [e for p in _runner for e in with_ast(p)]
        chk(f'⑦ ★ AST 대체: 러너가 거는 실제 5 파일에서 오탐 0 (실사고 129 건): {len(e_run)} 건'
            + (f' — 예: {e_run[:3]}' if e_run else ''), len(e_run) == 0)
    print(f'\ncheck_undefined_names selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    paths = a.paths or sorted(glob.glob(os.path.join(ROOT, 'scripts', '**', '*.py'),
                                        recursive=True))
    errs, how = scan(paths)
    print(f'미정의 이름 검사 ({how}) — 파일 {len(paths)}')
    for e in errs:
        print(f'  ✗ {e}')
    print(f'\n{"✗ " + str(len(errs)) + " 건" if errs else "✓ 없음"}'
          f'   ⚠ 동적 이름(globals/exec)은 정적으로 못 본다 — 이 통과가 런 성공을 뜻하지 않는다')
    raise SystemExit(1 if errs else 0)

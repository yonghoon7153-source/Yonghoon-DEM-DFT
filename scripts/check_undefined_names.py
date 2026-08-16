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
    mod_names = set(dir(__builtins__)) | {'__file__', '__name__', '__doc__'}
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for al in n.names:
                mod_names.add((al.asname or al.name).split('.')[0])
        elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            mod_names.add(n.id)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            mod_names.add(n.name)
    out = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        bound = set(mod_names)
        for a in list(fn.args.args) + list(fn.args.kwonlyargs) + list(fn.args.posonlyargs):
            bound.add(a.arg)
        if fn.args.vararg:
            bound.add(fn.args.vararg.arg)
        if fn.args.kwarg:
            bound.add(fn.args.kwarg.arg)
        for n in ast.walk(fn):
            if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                bound.add(n.id)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                for al in n.names:
                    bound.add((al.asname or al.name).split('.')[0])
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                bound.add(n.name)
            elif isinstance(n, ast.ExceptHandler) and n.name:
                bound.add(n.name)
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

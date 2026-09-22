#!/usr/bin/env python3
"""웹앱/킷 파이썬 환경 감사 — **리포를 실제로 훑어** 필요한 3rd-party 를 정한다.

왜 목록을 손으로 안 적나 (규율 ⑤, SELF-02~05):
  "후보를 고르는 코드" 가 곧 사각지대다.  import 목록을 상수로 박아두면
  새 모듈이 들어와도 검사기는 **초록**을 낸다.  그래서 여기서는 매번
  `webapp/*.py` · `scripts/*.py` 를 **AST 로 전수 파싱**해 최상위 import 를
  뽑고, 그 중 하나라도 아래 표에 분류돼 있지 않으면 selftest 가 **거부**한다.

`try/except ImportError` 안이거나 함수 안에 있는 import 는 **없어도 import
시점에 안 죽으므로** HARD 가 아니다 — 그 구분을 안 하면 taichi·cupy·mph 까지
설치 대상이 돼 설치가 통째로 실패한다 (실제로 그럴 뻔했다).

쓰임:
  --selftest       검사기 자신이 맞는지 (음성 대조 포함)
  --check          지정 인터프리터에 REQUIRED 가 다 있나 (없으면 rc=1)
  --list-missing   없는 것의 **pip 이름**만 한 줄에 하나씩 (설치기가 먹는다)
"""
from __future__ import annotations

import argparse
import ast
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = ('webapp', 'scripts')

# ── import 이름 → pip 이름 (다른 것만 적는다; 같으면 생략 가능) ────────────
PIP_NAME = {
    'sklearn': 'scikit-learn',
    'skimage': 'scikit-image',
    'skopt': 'scikit-optimize',
    'PIL': 'pillow',
    'pptx': 'python-pptx',
    'docx': 'python-docx',
    'cupyx': 'cupy',
    'mpl_toolkits': 'matplotlib',
    'BioLogic': 'galvani',
    'mph': 'MPh',
    'jinja2': 'Jinja2',
    'markupsafe': 'MarkupSafe',
    'werkzeug': 'Werkzeug',
    'markdown': 'Markdown',
}

# ── 반드시 (없으면 웹앱 분석 경로가 import 시점에 죽는다) ──────────────────
REQUIRED = ('flask', 'numpy', 'scipy', 'pandas', 'matplotlib',
            'networkx', 'sklearn', 'requests')

# ── 권장 (guarded 라 안 죽지만 없으면 기능이 조용히 빠진다) ───────────────
RECOMMENDED = ('adjustText', 'markdown', 'tabulate', 'joblib')

# ── 선택 (--full) ─────────────────────────────────────────────────────────
EXTRA = ('shapely', 'trimesh', 'skimage', 'h5py', 'weasyprint', 'pyamg',
         'plotly', 'anthropic', 'gunicorn', 'pptx', 'docx', 'PIL',
         'skopt', 'gplearn', 'impedance', 'galvani', 'pybamm', 'pysr')

# ── GPU/전용 — 이 기계에 안 깐다 (uma·V100 소관) ──────────────────────────
EXEMPT = ('taichi', 'cupy', 'cupyx', 'mph', 'pysisso', 'msvcrt')

# flask 가 끌고 오므로 따로 안 적는다
BUNDLED = ('jinja2', 'markupsafe', 'werkzeug', 'mpl_toolkits', 'security')


def _classified() -> set:
    return set(REQUIRED) | set(RECOMMENDED) | set(EXTRA) | set(EXEMPT) | set(BUNDLED)


def pip_name(mod: str) -> str:
    return PIP_NAME.get(mod, mod)


# ────────────────────────────── AST 전수 스캔 ──────────────────────────────
def _local_module_names(root: str) -> set:
    out = set()
    for d in SCAN_DIRS:
        p = os.path.join(root, d)
        if not os.path.isdir(p):
            continue
        for f in os.listdir(p):
            if f.endswith('.py'):
                out.add(f[:-3])
    return out


def _top_imports(path: str):
    """(hard, guarded) — 최상위에서 무조건 실행되는 import vs 아닌 것."""
    try:
        with open(path, encoding='utf-8', errors='replace') as fh:
            tree = ast.parse(fh.read())
    except SyntaxError:
        return set(), set()
    hard, guarded = set(), set()

    def add(node, bucket):
        if isinstance(node, ast.Import):
            for a in node.names:
                bucket.add(a.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                bucket.add(node.module.split('.')[0])

    def catches_import(try_node) -> bool:
        for h in try_node.handlers:
            t = h.type
            names = []
            if isinstance(t, ast.Name):
                names = [t.id]
            elif isinstance(t, ast.Tuple):
                names = [e.id for e in t.elts if isinstance(e, ast.Name)]
            elif t is None:
                names = ['BaseException']
            if any(n in ('ImportError', 'ModuleNotFoundError',
                         'Exception', 'BaseException') for n in names):
                return True
        return False

    def walk(node, soft):
        for ch in ast.iter_child_nodes(node):
            stmt(ch, soft)

    def stmt(node, soft):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            add(node, guarded if soft else hard)
        elif isinstance(node, ast.Try):
            soft2 = soft or catches_import(node)
            for b in node.body:
                stmt(b, soft2)
            for h in node.handlers:
                for b in h.body:
                    stmt(b, True)
            for b in list(node.orelse) + list(node.finalbody):
                stmt(b, soft)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # 함수 안 import = 지연 로드.  import 시점에 안 죽는다.
            for sub in ast.walk(node):
                add(sub, guarded)
        else:
            walk(node, soft)

    walk(tree, False)
    return hard, guarded


def scan(root: str = ROOT):
    """리포 전수 → {'hard': {mod: [files]}, 'guarded': {mod: [files]}}"""
    std = set(getattr(sys, 'stdlib_module_names', ()))
    local = _local_module_names(root)
    hard, guarded = {}, {}
    for d in SCAN_DIRS:
        p = os.path.join(root, d)
        if not os.path.isdir(p):
            continue
        for f in sorted(os.listdir(p)):
            if not f.endswith('.py'):
                continue
            h, g = _top_imports(os.path.join(p, f))
            for m in h:
                if m in std or m in local:
                    continue
                hard.setdefault(m, []).append(f'{d}/{f}')
            for m in g:
                if m in std or m in local:
                    continue
                guarded.setdefault(m, []).append(f'{d}/{f}')
    return {'hard': hard, 'guarded': guarded}


# ────────────────────────────── 실물 확인 ──────────────────────────────────
def probe(python: str, mods) -> dict:
    """그 인터프리터로 **실제로 import 해 본다** (경로 추측 금지)."""
    mods = list(mods)
    if not mods:
        return {}
    src = (
        'import importlib,json,sys\n'
        'out={}\n'
        'for m in %r:\n'
        '    try:\n'
        '        mod=importlib.import_module(m)\n'
        '        out[m]=getattr(mod,"__version__","?")\n'
        '    except BaseException as e:\n'
        '        out[m]=None\n'
        'json.dump(out,sys.stdout)\n' % (mods,)
    )
    try:
        r = subprocess.run([python, '-c', src], capture_output=True,
                           text=True, timeout=300)
    except (OSError, subprocess.SubprocessError) as e:
        raise SystemExit(f'⛔ 인터프리터를 못 돌렸다: {python} — {e}')
    if r.returncode != 0:
        raise SystemExit(f'⛔ 프로브 실패 rc={r.returncode}\n{r.stderr[-2000:]}')
    import json
    return json.loads(r.stdout)


def _sets(full: bool, mpm: bool):
    want = list(REQUIRED) + list(RECOMMENDED)
    if full:
        want += list(EXTRA)
    if mpm:
        want += ['taichi']
    seen, out = set(), []
    for m in want:
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


# ────────────────────────────── selftest ───────────────────────────────────
def selftest() -> int:
    fails = []

    def chk(name, cond):
        print(('  ok  ' if cond else '  FAIL') + '  ' + name)
        if not cond:
            fails.append(name)

    print('webapp_env_audit selftest')
    res = scan()
    hard = res['hard']

    chk('① 스캔이 실제로 파일을 읽었다 (numpy 가 HARD 에 있다)', 'numpy' in hard)
    chk('② networkx 가 HARD 다 (웹앱을 세운 바로 그 모듈)', 'networkx' in hard)
    chk('③ REQUIRED 는 전부 HARD 다',
        all(m in hard for m in REQUIRED if m != 'mpl_toolkits'))

    # ★ 이 리포에 있는 HARD 가 하나도 빠짐없이 분류돼 있나 — 목록이 낡는 것을 막는다
    unclassified = sorted(m for m in hard if m not in _classified())
    chk('④ ★ 분류 안 된 HARD import 가 없다  ' +
        (f'(남은 것: {unclassified})' if unclassified else ''), not unclassified)

    chk('⑤ guarded-only 는 REQUIRED 에 없다 (없어도 사는 걸 필수로 올리지 않는다)',
        all(m not in REQUIRED for m in res['guarded'] if m not in hard))

    chk('⑥ taichi 는 HARD 지만 EXEMPT 다 (MPM 전용, 웹앱 분석 경로 아님)',
        'taichi' in hard and 'taichi' in EXEMPT and 'taichi' not in REQUIRED)

    chk('⑦ pip 이름 매핑이 실재한다', pip_name('sklearn') == 'scikit-learn'
        and pip_name('numpy') == 'numpy')

    # ★★ 음성 대조 — 가짜 HARD 를 심으면 ④ 가 **반드시** 걸려야 한다.
    #    안 걸리면 ④ 는 false-green 이고 이 검사기는 쓸모가 없다.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, 'webapp'))
        os.makedirs(os.path.join(td, 'scripts'))
        with open(os.path.join(td, 'webapp', 'zz_probe.py'), 'w') as fh:
            fh.write('import zzz_not_a_real_package\n')
        res2 = scan(td)
        caught = 'zzz_not_a_real_package' in res2['hard'] \
            and 'zzz_not_a_real_package' not in _classified()
    chk('⑧ ★★ 음성 대조: 가짜 HARD import 를 심으면 ④ 가 잡는다', caught)

    # 함수 안 import 는 HARD 가 아니어야 한다 (지연 로드)
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, 'scripts'))
        with open(os.path.join(td, 'scripts', 'zz_lazy.py'), 'w') as fh:
            fh.write('def f():\n    import zzz_lazy_only\n')
        res3 = scan(td)
    chk('⑨ 함수 안 import 는 HARD 가 아니다',
        'zzz_lazy_only' not in res3['hard']
        and 'zzz_lazy_only' in res3['guarded'])

    # try/except ImportError 안은 HARD 가 아니어야 한다
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, 'scripts'))
        with open(os.path.join(td, 'scripts', 'zz_try.py'), 'w') as fh:
            fh.write('try:\n    import zzz_guarded\nexcept ImportError:\n'
                     '    zzz_guarded = None\n')
        res4 = scan(td)
    chk('⑩ try/except ImportError 안의 import 는 HARD 가 아니다',
        'zzz_guarded' not in res4['hard'])

    # 이 인터프리터로 실제 프로브가 도는가 (stdlib 로 확인 — 설치 무관)
    got = probe(sys.executable, ['json', 'zzz_definitely_absent'])
    chk('⑪ 프로브가 실물 import 를 한다 (있는 것/없는 것 구분)',
        got.get('json') is not None and got.get('zzz_definitely_absent') is None)

    print()
    if fails:
        print(f'⛔ {len(fails)} FAIL: ' + ' · '.join(fails))
        return 1
    print('✅ selftest 11/11')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description='웹앱 파이썬 환경 감사 (리포를 AST 로 전수 스캔해 필요 패키지를 정한다)')
    ap.add_argument('--python', default=sys.executable,
                    help='검사할 인터프리터 (기본: 지금 돌고 있는 것)')
    ap.add_argument('--check', action='store_true',
                    help='REQUIRED 가 다 있나 본다.  하나라도 없으면 rc=1')
    ap.add_argument('--list-missing', action='store_true',
                    help='없는 것의 pip 이름만 한 줄에 하나씩 (설치기가 먹는다)')
    ap.add_argument('--scan', action='store_true',
                    help='리포의 HARD/guarded import 를 전수로 보여준다')
    ap.add_argument('--full', action='store_true', help='선택 패키지까지 포함')
    ap.add_argument('--mpm', action='store_true', help='taichi 까지 포함')
    ap.add_argument('--selftest', action='store_true', help='검사기 자신을 검사')
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    if a.scan:
        res = scan()
        print('=== HARD ===')
        for m, fs in sorted(res['hard'].items(), key=lambda kv: -len(kv[1])):
            mark = '' if m in _classified() else '   ⛔ 분류 안 됨'
            print(f'  {m:<16} {len(fs):>3} 파일   예: {fs[0]}{mark}')
        print('\n=== guarded / lazy 만 ===')
        print('  ' + ', '.join(sorted(set(res['guarded']) - set(res['hard']))))
        return 0

    want = _sets(a.full, a.mpm)
    got = probe(a.python, want)
    missing_req = [m for m in REQUIRED if got.get(m) is None]
    missing_all = [m for m in want if got.get(m) is None]

    if a.list_missing:
        seen = set()
        for m in missing_all:
            p = pip_name(m)
            if p not in seen:
                seen.add(p)
                print(p)
        return 0

    print(f'인터프리터: {a.python}')
    for m in want:
        v = got.get(m)
        tier = ('필수' if m in REQUIRED else
                '권장' if m in RECOMMENDED else '선택')
        print(f'  {"✅" if v else "⛔"}  {m:<14} {tier}   ' +
              (f'{v}' if v else '없음'))
    print()
    if missing_req:
        print('⛔ 필수 누락: ' + ' '.join(pip_name(m) for m in missing_req))
        return 1
    if missing_all:
        print('⚠ 선택/권장 누락 (웹앱은 뜬다): '
              + ' '.join(pip_name(m) for m in missing_all))
    print('✅ 필수 전부 있음')
    return 0


if __name__ == '__main__':
    sys.exit(main())

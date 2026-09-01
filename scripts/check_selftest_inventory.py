#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""리포의 `--selftest` 진입점이 **분류돼 있고 실제로 불리는가** — 그리고 CI 가 그것을
돌릴 **의존을 실제로 깔고 있는가**.

    python3 scripts/check_selftest_inventory.py            # 리포 실물
    python3 scripts/check_selftest_inventory.py --selftest
    python3 scripts/check_selftest_inventory.py --draft    # 등재 초안 생성 (사람이 검토)

═══ 계기 (2026-09-01, Codex R19 Q6) ═══

규칙 K 는 `check_all.sh` ↔ `discipline.yml` 을 **손으로 적은 10개 목록**으로 대조한다.
그래서 *둘 다에 없는* 검사기는 원리적으로 못 잡는다.  실측: 진입점 103개 중 **77개가
어느 쪽에도 없었다** — `check_undefined_names.py` · `network_conductivity.py` ·
`step4_dyn.py` · `predictor_engine.py` 처럼 이 리포의 결론을 떠받치는 것들이 포함된다.
돌지 않는 검사는 **없는 것과 같고**, 더 나쁘게는 "있다" 는 인상을 준다.

★ 그렇다고 77개를 전부 CI 에 넣는 것이 답은 아니다 — GPU·외부 데이터·수 분짜리가 섞여
  있다.  답은 **분류를 강제하는 것**이다: 어느 레인에 있는지, 아니면 왜 없는지를 적게 하고,
  적지 않은 것이 있으면 검사가 실패한다.  등재가 낡으면(파일이 사라지면) 그것도 실패다.

═══ 등재의 뜻 ═══

`docs/reviews/selftest_inventory.tsv` — `경로<TAB>플래그<TAB>등급<TAB>레인<TAB>담당<TAB>이유`

  등급 fast     — 초 단위, 표준 의존만.  **레인에 있어야 한다** (없으면 실패)
       gpu      — cupy/taichi/GPU 가 있어야 뜻이 있다
       external — 리포 밖 데이터·네트워크·무거운 의존(sklearn, node, LIGGGHTS dump)
       slow     — 초록이지만 분 단위 — CI 예산 밖
       broken   — 지금 빨간불.  **이유에 무엇이 깨졌는지 적는다** (숨기지 않는다)
       legacy   — 일회성/역사.  남겨 두되 돌리지 않는다

  레인 both · check_all · ci · none

⚠ 등급은 **실측**으로 정한다 (`--draft` 가 실제로 돌려 rc·소요시간을 재고 초안을 만든다).
  추정으로 적으면 등재 자체가 거짓말이 된다 — 이 리포는 그 실패를 이미 겪었다
  (`doc_refs_allowlist` 의 이유 6건이 사실과 달랐다, R19 Q5).
"""
from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
import time

INVENTORY = 'docs/reviews/selftest_inventory.tsv'
CHECK_ALL = 'scripts/check_all.sh'
WORKFLOW = '.github/workflows/discipline.yml'

CLASSES = ('fast', 'gpu', 'external', 'slow', 'broken', 'legacy')
LANES = ('both', 'check_all', 'ci', 'none')

#: ★ `fast` 는 **드라이버**가 한꺼번에 돌린다.  72개를 손으로 두 파일에 적으면 그 목록이
#:  또 낡는다 — 규칙 K 의 10개짜리 손목록이 정확히 그렇게 낡았다.  드라이버 한 줄이
#:  등재를 읽어 도니까, 새 검사기를 만들면 **등재만 하면 자동으로 돈다**.
#:  실측: `fast` 98개 합계 292 s, 그중 레인 밖 72개가 130 s — 충분히 싸다.
DRIVER = 'check_selftest_inventory.py --run-fast'

#: 그 파일이 **실제로 받는** 플래그만 찾는다.  단순히 `--selftest` 라는 글자가 있는 것과
#: 그 플래그를 받는 것은 다르다 — 실측: `mpm_webapp_payload.py` 는 `--selftest-temperature`
#: 만 받고, `mutation_sweep_20260825.py` 는 **남을** 그렇게 부를 뿐이며,
#: `additives.py` 는 `--selftest-dispersion`·`--selftest-sheath` 라 **바 `--selftest` 는
#: argparse 가 ambiguous 로 거절**한다.  그래서 플래그를 등재의 한 칸으로 둔다.
_RE_ACCEPTS = (
    re.compile(r"""add_argument\(\s*['"](--self-?test[a-z0-9-]*)['"]"""),   # argparse
    re.compile(r"""['"](--self-?test[a-z0-9-]*)['"]\s+in\s+sys\.argv"""),   # 직접 검사
    re.compile(r"""^\s*(--self-?test[a-z0-9-]*)\)""", re.M),               # sh case
    re.compile(r"""\$1['"]?\s*==?\s*['"](--self-?test[a-z0-9-]*)['"]"""),   # sh test
)

#: import 이름 → pip 배포 이름 (다른 것만).
_PIP_NAME = {'PIL': 'pillow', 'sklearn': 'scikit-learn', 'yaml': 'pyyaml',
             'cv2': 'opencv-python', 'skimage': 'scikit-image', 'pptx': 'python-pptx',
             'docx': 'python-docx', 'bs4': 'beautifulsoup4', 'OpenGL': 'pyopengl'}
#: 다른 배포가 **딸려 설치**하는 것 — 따로 적을 필요가 없다.
_PROVIDED_BY = {'jinja2': 'flask', 'werkzeug': 'flask', 'click': 'flask',
                'itsdangerous': 'flask', 'blinker': 'flask',
                'urllib3': 'requests', 'certifi': 'requests',
                'charset_normalizer': 'requests', 'idna': 'requests',
                'pyparsing': 'matplotlib', 'cycler': 'matplotlib',
                'kiwisolver': 'matplotlib', 'dateutil': 'matplotlib'}


def _repo_root(start: str | None = None) -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(start or __file__)))


# ══════════════════════════════════════════════════════════════════════
#  ① 진입점 발견
# ══════════════════════════════════════════════════════════════════════

_RE_FLAG = re.compile(r'--self-?test[a-z0-9-]*$')


def _accepted_flags_py(src: str):
    """파이썬 소스가 **실제로 받는** selftest 플래그 (AST).

    문자열 리터럴 안에 적힌 플래그는 세지 않는다 — 남의 플래그를 문서나 픽스처에
    적어 둔 것을 자기 진입점으로 오분류하지 않으려는 것이다.
    """
    got = set()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return got
    for n in ast.walk(tree):
        #  ① `ap.add_argument('--selftest', …)`
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == 'add_argument'):
            for a in n.args:
                if isinstance(a, ast.Constant) and isinstance(a.value, str) \
                        and _RE_FLAG.match(a.value):
                    got.add(a.value)
        #  ② `'--selftest' in sys.argv`
        if isinstance(n, ast.Compare) and len(n.ops) == 1 and isinstance(n.ops[0], ast.In):
            tgt = n.comparators[0]
            is_argv = (isinstance(tgt, ast.Attribute) and tgt.attr == 'argv') or (
                isinstance(tgt, ast.Subscript)
                and isinstance(tgt.value, ast.Attribute) and tgt.value.attr == 'argv')
            if is_argv and isinstance(n.left, ast.Constant) \
                    and isinstance(n.left.value, str) and _RE_FLAG.match(n.left.value):
                got.add(n.left.value)
    return got


def entry_points(root: str):
    """→ 정렬된 `(경로, 플래그)` 목록.  한 파일이 여러 플래그를 받으면 각각 한 줄이다.

    ⚠ 러너(`check_all.sh`)는 제외한다 — 그것은 **레인 자신**이지 그 안의 항목이 아니다
      (`--selftest` 문자열이 잔뜩 있는 것은 남을 그렇게 부르기 때문이다).
    """
    out = set()
    for base in ('scripts', 'webapp'):
        d0 = os.path.join(root, base)
        if not os.path.isdir(d0):
            continue
        for r, ds, fs in os.walk(d0):
            ds[:] = [x for x in ds if x not in ('.git', 'node_modules', '__pycache__')]
            for f in fs:
                if not f.endswith(('.py', '.sh', '.mjs')):
                    continue
                p = os.path.relpath(os.path.join(r, f), root).replace(os.sep, '/')
                if p == CHECK_ALL:
                    continue
                try:
                    s = open(os.path.join(r, f), encoding='utf-8', errors='replace').read()
                except OSError:
                    continue
                #  ⚠ 파이썬은 **AST** 로 본다.  정규식은 *문자열 리터럴 안*의 플래그까지
                #    집는다 — 실측: 이 검사기 자신의 selftest 픽스처
                #    `w('scripts/c.py', "ap.add_argument('--selftest-temp')")` 가 이 파일을
                #    `--selftest-temp` 진입점으로 오분류했다.  59) 검사가 문자열 → AST 로
                #    올라간 것과 **같은 이유**다.
                flags = (_accepted_flags_py(s) if f.endswith('.py')
                         else {m for rx in _RE_ACCEPTS for m in rx.findall(s)})
                for fl in flags:
                    out.add((p, fl))
    return sorted(out)


def lanes(root: str):
    """→ (check_all 이 부르는 basename 집합, CI 가 부르는 basename 집합)."""
    def _names(path):
        try:
            s = open(os.path.join(root, path), encoding='utf-8', errors='replace').read()
        except OSError:
            return set()
        #  `scripts/x.py` · `webapp/x.py` · `node webapp/x.mjs` 를 그대로 집는다
        return set(re.findall(r'(?:scripts|webapp)/[A-Za-z0-9_./-]+\.(?:py|sh|mjs)', s))
    return _names(CHECK_ALL), _names(WORKFLOW)


def driver_lane(root: str) -> str:
    """드라이버(`--run-fast`)가 어느 레인에 배선돼 있나."""
    def _has(path):
        try:
            s = open(os.path.join(root, path), encoding='utf-8', errors='replace').read()
        except OSError:
            return False
        return DRIVER in ' '.join(s.split())
    a, b = _has(CHECK_ALL), _has(WORKFLOW)
    return 'both' if a and b else 'check_all' if a else 'ci' if b else 'none'


def observed_lane(p: str, in_ca: set, in_ci: set) -> str:
    a, b = p in in_ca, p in in_ci
    return 'both' if a and b else 'check_all' if a else 'ci' if b else 'none'


# ══════════════════════════════════════════════════════════════════════
#  ② 등재
# ══════════════════════════════════════════════════════════════════════

def load_inventory(root: str):
    """→ {(경로, 플래그): {klass, lane, owner, why}}."""
    fp = os.path.join(root, INVENTORY)
    out = {}
    if not os.path.exists(fp):
        return out
    for i, ln in enumerate(open(fp, encoding='utf-8'), 1):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        parts = [x.strip() for x in ln.split('\t')]
        if len(parts) < 6 or not all(parts[:6]):
            raise SystemExit(f'⛔ {INVENTORY}:{i} (경로,플래그,등급,레인,담당,이유) '
                             f'6칸이 필요하다 — {ln!r}')
        path, flag, klass, lane, owner, why = parts[:6]
        if not flag.startswith('--'):
            raise SystemExit(f'⛔ {INVENTORY}:{i} 플래그가 아니다 — {flag!r}')
        if klass not in CLASSES:
            raise SystemExit(f'⛔ {INVENTORY}:{i} 알 수 없는 등급 {klass!r} — {CLASSES}')
        if lane not in LANES:
            raise SystemExit(f'⛔ {INVENTORY}:{i} 알 수 없는 레인 {lane!r} — {LANES}')
        if (path, flag) in out:
            raise SystemExit(f'⛔ {INVENTORY}:{i} 중복 등재 — {path} {flag}')
        out[(path, flag)] = dict(klass=klass, lane=lane, owner=owner, why=why)
    return out


# ══════════════════════════════════════════════════════════════════════
#  ③ CI 가 돌리는 것의 **의존 폐포**
# ══════════════════════════════════════════════════════════════════════

def _toplevel_imports(src: str):
    """모듈 **최상위**(try 블록 포함) import 만.  함수 안 지연 import 는 세지 않는다."""
    got = set()

    def _add(node):
        if isinstance(node, ast.Import):
            for a in node.names:
                got.add(a.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            got.add(node.module.split('.')[0])
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return got
    for n in tree.body:
        _add(n)
        if isinstance(n, (ast.Try, ast.If, ast.With)):
            for s in ast.walk(n):
                _add(s)
    return got


def _all_imports(src: str):
    """AST 전체의 import (깊이 무관).  **진입점 파일**에 쓴다 — 그 파일은 통째로 도니까
    `main()` 안의 `import app` 도 실제로 실행된다.

    ⚠ 이것이 없으면 웹앱 테스트의 의존을 통째로 놓친다: 다섯 테스트가 전부
      `def main(): import app` 꼴이라 최상위만 보면 flask 가 안 보이고, 그래서 CI 가
      flask 를 안 깔아도 검사가 초록이었다 (R19 Q6 P2 의 바로 그 상태).
    """
    got = set()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return got
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                got.add(a.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
            got.add(n.module.split('.')[0])
    return got


def import_closure(root: str, starts):
    """리포 안 모듈을 따라가며 모은 **외부** 의존.

    진입점은 전체 AST 를, 거기서 도달한 모듈은 **최상위**만 본다 (모듈을 import 하면
    최상위는 반드시 돌지만 함수 안까지 돈다는 보장은 없다).
    """
    local = {}
    for base in ('scripts', 'webapp'):
        d0 = os.path.join(root, base)
        if os.path.isdir(d0):
            for f in os.listdir(d0):
                if f.endswith('.py'):
                    local[f[:-3]] = os.path.join(base, f)
    std = set(getattr(sys, 'stdlib_module_names', ()))
    starts = list(starts)
    seen, third, queue = set(), set(), [(r, True) for r in starts]
    while queue:
        rel, is_start = queue.pop()
        if rel in seen or not rel.endswith('.py'):
            continue
        seen.add(rel)
        fp = os.path.join(root, rel)
        if not os.path.exists(fp):
            continue
        _src = open(fp, encoding='utf-8', errors='replace').read()
        for m in (_all_imports(_src) if is_start else _toplevel_imports(_src)):
            if m in std or m.startswith('_'):
                continue
            if m in local:
                queue.append((local[m], False))
            else:
                third.add(m)
    return third


def ci_installed(root: str):
    """워크플로가 `pip install` 하는 배포 이름들."""
    try:
        s = open(os.path.join(root, WORKFLOW), encoding='utf-8', errors='replace').read()
    except OSError:
        return set()
    got = set()
    for m in re.finditer(r'pip install([^\n]*)', s):
        for tok in m.group(1).split():
            if tok.startswith('-'):
                continue
            got.add(re.split(r'[=<>\[]', tok)[0].lower())
    return got


def ci_python_targets(root: str):
    """CI 가 `python …` 으로 부르는 리포 안 스크립트."""
    try:
        s = open(os.path.join(root, WORKFLOW), encoding='utf-8', errors='replace').read()
    except OSError:
        return []
    return sorted(set(re.findall(r'python3?\s+((?:scripts|webapp)/[A-Za-z0-9_./-]+\.py)', s)))


# ══════════════════════════════════════════════════════════════════════
#  ④ 검사
# ══════════════════════════════════════════════════════════════════════

def run(root: str, verbose: bool = True):
    eps = entry_points(root)
    inv = load_inventory(root)
    in_ca, in_ci = lanes(root)
    drv = driver_lane(root)
    errs = []

    for p, fl in eps:
        if (p, fl) not in inv:
            errs.append(f'등재 없음 (분류되지 않은 진입점): {p} {fl}')
    for p, fl in inv:
        if (p, fl) in eps:
            continue
        why = ('파일이 없다' if not os.path.exists(os.path.join(root, p))
               else f'{fl} 를 더는 받지 않는다')
        errs.append(f'낡은 등재 ({why}): {p} {fl}')

    lane_bad = []
    for (p, fl), row in inv.items():
        if (p, fl) not in eps:
            continue
        obs = observed_lane(p, in_ca, in_ci)
        if obs != row['lane']:
            lane_bad.append(f'레인 불일치: {p}  등재={row["lane"]}  실제={obs}')
        #  ★ fast 인데 아무 데서도 안 불리면 그것이 바로 Q6 가 지적한 상태다.
        #    단 **드라이버가 양쪽에 배선돼 있으면** 그것이 돌려 준다.
        if row['klass'] == 'fast' and obs == 'none' and drv != 'both':
            lane_bad.append(f'fast 인데 어디서도 안 불린다: {p} {fl}  '
                            f'(드라이버 `{DRIVER}` 도 {drv})')
    errs += lane_bad

    #  ── CI 의존 폐포 ──────────────────────────────────────────────────
    targets = ci_python_targets(root)
    need = import_closure(root, targets)
    have = ci_installed(root)
    missing = sorted(m for m in need
                     if _PIP_NAME.get(m, m).lower() not in have
                     and _PROVIDED_BY.get(m, '') not in have)
    for m in missing:
        errs.append(f'CI 가 {m} 를 깔지 않는다 (pip: {_PIP_NAME.get(m, m)}) — '
                    f'깨끗한 러너에서 import 부터 죽는다')

    if verbose:
        print(f'진입점 {len(eps)}개 · 등재 {len(inv)}개')
        by = {}
        for k in eps:
            kl = inv.get(k, {}).get('klass', '(미등재)')
            by[kl] = by.get(kl, 0) + 1
        print('  등급별: ' + ' · '.join(f'{k} {v}' for k, v in sorted(by.items())))
        _ln = [observed_lane(p, in_ca, in_ci) for p, _ in eps]
        print(f'  레인:   both {_ln.count("both")} · 한쪽 '
              f'{_ln.count("check_all") + _ln.count("ci")} · 없음 {_ln.count("none")}')
        print(f'  드라이버 `{DRIVER}` → {drv}'
              + ('' if drv == 'both' else '   ⛔ 양쪽에 있어야 fast 가 실제로 돈다'))
        print(f'  CI 대상 {len(targets)}개 → 외부 의존 {len(need)}종 '
              f'({", ".join(sorted(need)) or "없음"})')
        if errs:
            print(f'\n⛔ {len(errs)}건')
            for e in errs[:40]:
                print(f'  {e}')
            if len(errs) > 40:
                print(f'  … 외 {len(errs) - 40}건')
    return (1 if errs else 0), errs


# ══════════════════════════════════════════════════════════════════════
#  ⑤ 초안 — **실제로 돌려서** 등급을 정한다
# ══════════════════════════════════════════════════════════════════════

def run_fast(root: str, timeout: int = 180, workers: int = 6):
    """등재된 `fast` 를 전부 돌린다 — 이것이 레인이다.

    ★ 손목록 대신 **등재를 읽어** 돈다.  새 검사기를 만들면 등재만 하면 자동으로 돌고,
      목록이 낡을 자리가 없다 (규칙 K 의 10개짜리 손목록이 낡은 것이 계기다).
    """
    import concurrent.futures as cf
    inv = load_inventory(root)
    eps = set(entry_points(root))
    todo = sorted(k for k, v in inv.items() if v['klass'] == 'fast' and k in eps)
    if not todo:
        print('⛔ 등재에 fast 가 하나도 없다 — 등재가 비었거나 경로가 어긋났다')
        return 1

    def one(key):
        p, fl = key
        cmd = (['bash', p] if p.endswith('.sh')
               else ['node', p] if p.endswith('.mjs') else [sys.executable, p])
        t = time.time()
        try:
            r = subprocess.run(cmd + [fl], cwd=root, capture_output=True,
                               text=True, timeout=timeout)
            rc, out = r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            rc, out = 124, f'{timeout}s TIMEOUT'
        except OSError as e:
            rc, out = 127, str(e)
        return key, rc, time.time() - t, out

    bad, t0 = [], time.time()
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for (p, fl), rc, sec, out in ex.map(one, todo):
            if rc:
                bad.append((p, fl, rc, out))
                print(f'  ✗ {p} {fl}  rc={rc}')
            elif sec > 20:
                print(f'  · {p} {fl}  {sec:.0f}s (느려졌다 — 등재를 slow 로 옮길 것)')
    print(f'fast 자기검사 {len(todo) - len(bad)}/{len(todo)} 통과  '
          f'({time.time() - t0:.0f}s)')
    for p, fl, rc, out in bad:
        print(f'\n── {p} {fl}  rc={rc} ' + '─' * 30)
        for ln in [x for x in out.splitlines() if x.strip()][-12:]:
            print('   ' + ln[:160])
    return 1 if bad else 0


def draft(root: str, timeout: int = 90, workers: int = 6):
    import concurrent.futures as cf
    eps = entry_points(root)
    in_ca, in_ci = lanes(root)

    def probe(key):
        p, fl = key
        cmd = (['bash', p] if p.endswith('.sh')
               else ['node', p] if p.endswith('.mjs') else [sys.executable, p])
        t = time.time()
        try:
            r = subprocess.run(cmd + [fl], cwd=root, capture_output=True,
                               text=True, timeout=timeout)
            rc, out = r.returncode, r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            rc, out = 124, 'TIMEOUT'
        except OSError as e:
            rc, out = 127, str(e)
        return key, rc, time.time() - t, out

    rows = []
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for (p, fl), rc, sec, out in ex.map(probe, eps):
            if rc == 124:
                klass, why = 'slow', f'{timeout}s 안에 안 끝난다 (실측)'
            elif rc != 0:
                first = next((ln.strip() for ln in out.splitlines()
                              if 'Error' in ln or 'error' in ln), '')[:110]
                klass = 'external' if ('ModuleNotFoundError' in out
                                       or 'FileNotFoundError' in out) else 'broken'
                why = f'rc={rc} · {first}' if first else f'rc={rc}'
            elif sec > 20:
                klass, why = 'slow', f'초록이나 {sec:.0f}s (실측)'
            else:
                klass, why = 'fast', f'초록 {sec:.1f}s (실측)'
            rows.append((p, fl, klass, observed_lane(p, in_ca, in_ci), 'claude', why))
    for r in sorted(rows):
        print('\t'.join(r))


def _selftest():
    import tempfile
    ok, bad = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(f'{name} {extra}')

    root = tempfile.mkdtemp(prefix='inv_')
    for d in ('scripts', 'webapp', 'docs/reviews', '.github/workflows'):
        os.makedirs(os.path.join(root, d), exist_ok=True)

    def w(rel, s):
        open(os.path.join(root, rel), 'w', encoding='utf-8').write(s)

    w('scripts/a.py', "import argparse\nap.add_argument('--selftest')\n")
    w('scripts/b.py', "if '--selftest' in sys.argv: pass\n")
    w('scripts/c.py', "ap.add_argument('--selftest-temp')\n")
    w('scripts/plain.py', 'x = 1\n')
    #  ⚠ 남을 `--selftest` 로 **부르기만** 하는 파일 — 진입점이 아니다 (실측:
    #    `mutation_sweep_20260825.py` 가 이 모양이라 초판이 오분류했다)
    w('scripts/caller.py', "run(['python3', 'scripts/a.py', '--selftest'])\n")
    w(CHECK_ALL, 'python3 scripts/a.py --selftest\n')
    w(WORKFLOW, '  - run: python scripts/a.py --selftest\n'
                '  - run: python -m pip install --quiet numpy\n')

    eps = entry_points(root)
    chk('① 진입점을 찾는다 (argparse·sys.argv 두 형태)',
        eps == [('scripts/a.py', '--selftest'), ('scripts/b.py', '--selftest'),
                ('scripts/c.py', '--selftest-temp')], str(eps))
    chk('★① 플래그가 다르면 그 플래그를 적는다 (바 --selftest 가 아니다)',
        ('scripts/c.py', '--selftest-temp') in eps, str(eps))
    chk('① `--selftest` 없는 파일은 안 센다',
        not any(p == 'scripts/plain.py' for p, _ in eps))
    chk('★① 남을 그렇게 **부르기만** 하는 파일은 진입점이 아니다',
        not any(p == 'scripts/caller.py' for p, _ in eps), str(eps))
    chk('★① 러너 자신은 진입점이 아니다 (남을 그렇게 부를 뿐)',
        not any(p == CHECK_ALL for p, _ in eps))
    ca, ci = lanes(root)
    chk('② 레인을 읽는다', 'scripts/a.py' in ca and 'scripts/a.py' in ci, f'{ca} {ci}')
    chk('② 실제 레인 판정', observed_lane('scripts/a.py', ca, ci) == 'both'
        and observed_lane('scripts/b.py', ca, ci) == 'none')

    w(INVENTORY, 'scripts/a.py\t--selftest\tfast\tboth\tclaude\t초록\n')
    rc, errs = run(root, verbose=False)
    chk('★③ 미등재 진입점을 잡는다', rc == 1 and any('scripts/b.py' in e for e in errs), str(errs))

    w(INVENTORY, 'scripts/a.py\t--selftest\tfast\tboth\tclaude\t초록\n'
                 'scripts/b.py\t--selftest\tlegacy\tnone\tclaude\t역사 기록용\n'
                 'scripts/c.py\t--selftest-temp\tlegacy\tnone\tclaude\t다른 플래그\n')
    rc, errs = run(root, verbose=False)
    chk('③ 전부 등재되면 통과', rc == 0, str(errs))

    w(INVENTORY, 'scripts/a.py\t--selftest\tfast\tboth\tclaude\t초록\n'
                 'scripts/b.py\t--selftest\tfast\tnone\tclaude\t초록\n'
                 'scripts/c.py\t--selftest-temp\tlegacy\tnone\tclaude\t다른 플래그\n')
    rc, errs = run(root, verbose=False)
    chk('★③ fast 인데 아무 레인에도 없으면 잡는다',
        rc == 1 and any('fast 인데' in e for e in errs), str(errs))

    w(INVENTORY, 'scripts/a.py\t--selftest\tfast\tci\tclaude\t초록\n'
                 'scripts/b.py\t--selftest\tlegacy\tnone\tclaude\t역사\n'
                 'scripts/c.py\t--selftest-temp\tlegacy\tnone\tclaude\t다른 플래그\n')
    rc, errs = run(root, verbose=False)
    chk('★③ 레인 불일치를 잡는다 (등재 ci · 실제 both)',
        rc == 1 and any('레인 불일치' in e for e in errs), str(errs))

    w(INVENTORY, 'scripts/a.py\t--selftest\tfast\tboth\tclaude\t초록\n'
                 'scripts/b.py\t--selftest\tlegacy\tnone\tclaude\t역사\n'
                 'scripts/c.py\t--selftest-temp\tlegacy\tnone\tclaude\t다른 플래그\n'
                 'scripts/gone.py\t--selftest\tfast\tnone\tclaude\t없어진 것\n')
    rc, errs = run(root, verbose=False)
    chk('★③ 사라진 파일의 등재를 잡는다',
        rc == 1 and any('낡은 등재' in e and 'gone' in e for e in errs), str(errs))

    for bad_row, label in (('scripts/a.py\t--selftest\tfast\tboth\tclaude\n', '칸이 모자란 등재'),
                           ('scripts/a.py\t--selftest\tquick\tboth\tclaude\t초록\n', '알 수 없는 등급'),
                           ('scripts/a.py\t--selftest\tfast\teverywhere\tclaude\t초록\n', '알 수 없는 레인'),
                           ('scripts/a.py\t--selftest\tfast\tboth\tclaude\t초록\n'
                            'scripts/a.py\tfast\tboth\tclaude\t또\n', '중복 등재')):
        w(INVENTORY, bad_row)
        try:
            load_inventory(root)
            chk(f'★③ {label} 를 거부', False, '통과해 버렸다')
        except SystemExit:
            chk(f'★③ {label} 를 거부', True)

    #  ── ④ CI 의존 폐포 ────────────────────────────────────────────────
    w('scripts/a.py', "import argparse\nimport helper\nap.add_argument('--selftest')\n")
    w('scripts/helper.py', 'import numpy\nimport flask\n')
    w(INVENTORY, 'scripts/a.py\t--selftest\tfast\tboth\tclaude\t초록\n'
                 'scripts/b.py\t--selftest\tlegacy\tnone\tclaude\t역사\n'
                 'scripts/c.py\t--selftest-temp\tlegacy\tnone\tclaude\t다른 플래그\n')
    need = import_closure(root, ['scripts/a.py'])
    chk('★④ 리포 안 모듈을 **따라가** 외부 의존을 모은다 (a → helper → flask)',
        need == {'numpy', 'flask'}, str(need))
    rc, errs = run(root, verbose=False)
    chk('★★④ CI 가 안 까는 의존을 잡는다 (깨끗한 러너에서 import 부터 죽는다)',
        rc == 1 and any('flask' in e for e in errs), str(errs))
    w(WORKFLOW, '  - run: python scripts/a.py --selftest\n'
                '  - run: python -m pip install --quiet numpy flask\n')
    rc, errs = run(root, verbose=False)
    chk('④ 깔면 통과', rc == 0, str(errs))
    w('scripts/helper.py', 'import numpy\nfrom PIL import Image\n')
    rc, errs = run(root, verbose=False)
    chk('★④ import 이름과 pip 이름이 다른 것도 안다 (PIL → pillow)',
        rc == 1 and any('pillow' in e for e in errs), str(errs))
    w('scripts/helper.py', 'def f():\n    import flask\n    return flask\n')
    need = import_closure(root, ['scripts/a.py'])
    chk('④ 함수 안 지연 import 는 세지 않는다 (CI 가 그 경로를 안 탄다)',
        'flask' not in need, str(need))

    print(f'check_selftest_inventory selftest: {ok}/{ok + len(bad)} PASS')
    for b in bad:
        print('  ✗', b)
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', default=None)
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--draft', action='store_true',
                    help='진입점을 실제로 돌려 등재 초안을 찍는다 (사람이 검토해 커밋)')
    ap.add_argument('--run-fast', action='store_true',
                    help='등재된 fast 를 전부 돌린다 (check_all·CI 가 이것을 부른다)')
    ap.add_argument('--timeout', type=int, default=90)
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    root = a.root or _repo_root()
    if a.run_fast:
        return run_fast(root)
    if a.draft:
        draft(root, a.timeout)
        return 0
    rc, _ = run(root, verbose=not a.quiet)
    print('\n' + ('✗ 분류되지 않았거나 낡은 항목이 있다' if rc else '✓ 전부 분류돼 있다'))
    return rc


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""진입점의 **전이 외부 의존**을 정적으로 뽑는다 — 환경 셋업이 드립이 되지 않게.

왜 (2026-08-11 V100 실측):
  `network_conductivity.py --selftest` 를 돌리려는데 결손 모듈이 **한 번에 하나씩** 나왔다 —
  pandas 죽음 → 설치 → networkx 죽음 → …  원인은 셋업 스크립트의 pip 목록이 **손으로 적은
  것**이고, 그 목록이 어느 진입점을 위한 것인지 아무도 적어두지 않았다는 것.
  게다가 setup_v100 의 진입점 스모크는 **MPM/킷 경로만** 봤다 (cKDTree·planner·transfer) —
  웹앱 DEM 접촉망 σ 경로는 검증 대상이 아니었다.  CLAUDE.md frame[5] 가 경고한
  "두 파이프라인은 따로다" 가 **환경 셋업에도 그대로** 나타난 것이다.

  ⇒ 목록을 **코드에서 유도**한다.  손으로 적은 목록과 코드가 갈라지면 여기서 잡힌다.

한계 (정직):
  · 정적 AST 스캔이라 **함수 안 지연 import 도 잡지만**, `importlib.import_module(name)` 처럼
    이름이 런타임에 정해지는 것은 못 잡는다.
  · optional 의존(cupy 처럼 없으면 CPU fallback)을 **구분하지 못한다** — `--optional` 목록으로
    사람이 표시해 준다.
  · 그러므로 이것은 **실제 import 스모크의 대체가 아니라 보완**이다.  셋업은 둘 다 해야 한다.

사용:
    python3 scripts/trace_deps.py                      # 주요 진입점 표
    python3 scripts/trace_deps.py --entry network_conductivity --pip
    python3 scripts/trace_deps.py --check numpy,scipy,pandas,networkx   # 목록이 충분한가
    python3 scripts/trace_deps.py --selftest
"""
from __future__ import annotations

import argparse
import ast
import os
import sys
from collections import deque

SCRIPTS = os.path.dirname(os.path.abspath(__file__))

#: 없어도 CPU/대체 경로로 도는 것 — 셋업이 필수로 강제하면 안 된다.
OPTIONAL = frozenset({'cupy', 'cupyx', 'taichi', 'sklearn', 'skopt', 'pysisso', 'pybamm'})

#: import 이름 → pip 패키지 이름 (다른 것만).
PIP_NAME = {'skimage': 'scikit-image', 'sklearn': 'scikit-learn', 'PIL': 'pillow',
            'cv2': 'opencv-python', 'fitz': 'pymupdf', 'yaml': 'pyyaml'}

#: 셋업이 검증해야 하는 진입점 — **두 파이프라인을 다** 담는다 (frame[5]).
ENTRYPOINTS = (
    'network_conductivity',            # 웹앱 DEM 접촉망 σ (Kirchhoff/Holm)
    'analyze_contacts',
    'analyze_contacts_bimodal',
    'run_network_full_corrections',    # Stage E
    'mpm3d_compaction',                # 킷 MPM
    'mpm_webapp_payload',              # 킷 payload + STEP3/4
    'step3_sigma',
    'step4_dyn',
)


def _local_modules(scripts_dir=SCRIPTS):
    """리포 안의 모듈 = 로컬.  ★ scripts/ 뿐 아니라 **webapp/ 도 우리 코드**다 —
    scripts 가 `sys.path` 에 webapp 를 끼워 `pipeline_service` 를 import 하는 자리가 있고
    (network_conductivity 의 상태-어휘 대조), 그걸 외부 패키지로 세면 셋업이
    `pip install pipeline_service` 를 시도하게 된다 (실측 오탐)."""
    mods = {f[:-3] for f in os.listdir(scripts_dir) if f.endswith('.py')}
    sib = os.path.join(os.path.dirname(scripts_dir), 'webapp')
    if os.path.isdir(sib):
        mods |= {f[:-3] for f in os.listdir(sib) if f.endswith('.py')}
    return mods


def _imports_of(path):
    """파일 하나의 최상위 import 이름들 (함수 안 지연 import 포함)."""
    try:
        tree = ast.parse(open(path, encoding='utf-8').read())
    except (OSError, SyntaxError):
        return set()
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                out.add(a.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:          # 상대 import 는 로컬
                out.add(node.module.split('.')[0])
    return out


def trace(entry, scripts_dir=SCRIPTS):
    """진입점 → (방문한 로컬 모듈, 외부 의존 set).  로컬을 따라 전이적으로 내려간다."""
    local = _local_modules(scripts_dir)
    std = set(sys.stdlib_module_names)
    seen, ext = set(), set()
    q = deque([entry])
    while q:
        m = q.popleft()
        if m in seen:
            continue
        seen.add(m)
        p = os.path.join(scripts_dir, m + '.py')
        if not os.path.exists(p):
            continue
        for name in _imports_of(p):
            if name in local:
                q.append(name)
            elif name not in std:
                ext.add(name)
    return seen, ext


def required(entries=ENTRYPOINTS, scripts_dir=SCRIPTS):
    """필수(=optional 아님) 외부 의존 합집합 → sorted list."""
    out = set()
    for e in entries:
        if os.path.exists(os.path.join(scripts_dir, e + '.py')):
            out |= trace(e, scripts_dir)[1]
    return sorted(out - OPTIONAL)


def pip_names(mods):
    return [PIP_NAME.get(m, m) for m in mods]


def _selftest():
    import shutil
    import tempfile
    ok = fail = 0

    def chk(msg, cond):
        nonlocal ok, fail
        print(('  PASS  ' if cond else '  FAIL  ') + msg)
        ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)

    tmp = tempfile.mkdtemp()
    try:
        w = lambda n, s: open(os.path.join(tmp, n), 'w', encoding='utf-8').write(s)
        w('a.py', 'import os, json\nimport numpy\nfrom b import thing\n')
        w('b.py', 'import pandas\nfrom c import x\n')
        w('c.py', 'import networkx\n\ndef f():\n    import cupy   # 지연 import\n')
        seen, ext = trace('a', tmp)
        chk('1) 로컬을 전이적으로 따라간다 (a→b→c)', seen == {'a', 'b', 'c'})
        chk('2) 외부 의존을 모은다', ext == {'numpy', 'pandas', 'networkx', 'cupy'})
        chk('3) ★ 표준 라이브러리는 안 센다 (os·json)', 'os' not in ext and 'json' not in ext)
        chk('4) ★ 함수 안 지연 import 도 잡는다 (c.f 의 cupy)', 'cupy' in ext)
        chk('5) optional 은 required 에서 빠진다',
            'cupy' not in required(['a'], tmp) and 'numpy' in required(['a'], tmp))
        chk('6) pip 이름 매핑 (skimage→scikit-image)',
            pip_names(['skimage', 'numpy']) == ['scikit-image', 'numpy'])
        chk('7) 없는 진입점은 조용히 건너뛴다', required(['nope'], tmp) == [])
        # 순환 import 에서 안 멈춘다
        w('d.py', 'from e import q\n')
        w('e.py', 'from d import r\nimport scipy\n')
        chk('8) 순환 import 에서 무한루프에 안 빠진다', trace('d', tmp)[1] == {'scipy'})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 실제 리포에 대해 — 이 두 줄이 2026-08-11 V100 결손의 회귀다
    _, ext_nc = trace('network_conductivity')
    chk('9) ★ network_conductivity 가 pandas 를 요구한다 (V100 1차 결손)',
        'pandas' in ext_nc)
    chk('10) ★ network_conductivity 가 networkx 를 요구한다 (V100 2차 결손)',
        'networkx' in ext_nc)
    chk('10b) ★ webapp 모듈은 외부 패키지가 아니다 (pipeline_service 오탐 방지)',
        'pipeline_service' not in ext_nc and 'pipeline_service' not in required())
    chk('11) 두 파이프라인이 ENTRYPOINTS 에 다 있다 (frame[5])',
        'network_conductivity' in ENTRYPOINTS and 'step3_sigma' in ENTRYPOINTS)
    req = required()
    chk(f'12) 필수 목록이 비어 있지 않다: {req}', len(req) >= 3 and 'numpy' in req)
    chk('13) ★ GPU 전용(cupy)·taichi 는 필수에 안 들어간다 (CPU 머신 셋업을 막지 않게)',
        'cupy' not in req and 'taichi' not in req)

    # setup_v100.sh 의 손-목록이 코드와 갈라지지 않았는가 (drift 가드)
    sv = os.path.join(os.path.dirname(SCRIPTS), 'scripts', 'setup_v100.sh')
    if os.path.exists(sv):
        txt = open(sv, encoding='utf-8').read()
        missing = [m for m in req if m not in txt]
        chk(f'14) ★ setup_v100.sh 가 필수 모듈을 전부 담고 있다 (누락: {missing})', not missing)

    print(f'\ntrace_deps selftest: {ok}/{ok + fail} PASS')
    return fail == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--entry', help='이 진입점만 추적')
    ap.add_argument('--pip', action='store_true', help='pip install 한 줄로 출력')
    ap.add_argument('--check', help='쉼표 목록이 충분한지 검사 (부족하면 exit 1)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    entries = [a.entry] if a.entry else list(ENTRYPOINTS)
    if a.check:
        have = {x.strip() for x in a.check.split(',') if x.strip()}
        miss = [m for m in required(entries) if m not in have]
        if miss:
            print('✗ 부족: ' + ', '.join(pip_names(miss)))
            sys.exit(1)
        print('✓ 목록 충분')
        return
    if a.pip:
        print('pip install -q ' + ' '.join(pip_names(required(entries))))
        return
    print('진입점별 전이 외부 의존 (★=optional, 없어도 대체 경로)')
    for e in entries:
        if not os.path.exists(os.path.join(SCRIPTS, e + '.py')):
            print(f'  {e:30s} (파일 없음)')
            continue
        seen, ext = trace(e)
        req = sorted(ext - OPTIONAL)
        opt = sorted(ext & OPTIONAL)
        print(f'  {e:30s} local {len(seen):3d}  필수 {req}'
              + (f'  ★{opt}' if opt else ''))
    print('\n필수 합집합:', ', '.join(pip_names(required(entries))))
    print('pip install -q ' + ' '.join(pip_names(required(entries))))


if __name__ == '__main__':
    main()

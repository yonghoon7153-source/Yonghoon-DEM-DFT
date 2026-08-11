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

★ 2026-08-11 실측으로 드러난 구멍 (이 도구가 만들어진 바로 그날 밤):
  킷 압밀이 끝나고 payload 가 `ModuleNotFoundError: No module named 'skimage'` 로 죽었다.
  그런데 이 도구는 `mpm_webapp_payload` 의 필수 의존을 matplotlib/numpy/pyamg/scipy 로만
  보고했다 — **skimage 가 목록에 없었다**.  원인: payload 가 `viz_mpm_continuum` 을 평범한
  `import` 가 아니라 **경로 문자열 + importlib** 로 로드한다
  (`p = os.path.join(os.path.dirname(__file__), 'viz_mpm_continuum.py')`).
  AST 는 import 문만 보니 그 간선을 못 따라가고, 그 아래 skimage·plotly 를 통째로 놓쳤다.
  ⇒ **`'<모듈>.py'` 꼴 문자열 상수도 로컬 간선으로 센다** (`_dyn_locals_of`).  정적 스캔이
    문자열 경로 로딩까지는 따라갈 수 있다 — 못 따라가는 것은 이름이 **런타임 계산**될 때뿐.

한계 (정직):
  · 정적 AST 스캔이라 **함수 안 지연 import 도, `'x.py'` 문자열 경로 로딩도** 잡지만,
    `importlib.import_module(f'{prefix}_{n}')` 처럼 이름이 런타임에 조립되는 것은 못 잡는다.
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

#: pip 로 **따로 설치하지 않는** import 이름 → 딸려 오는 모 패키지.
#   ⚠ 이걸 안 빼면 셋업이 `pip install mpl_toolkits` 를 시도하고 실패한다 (그런 배포판은 없다).
#   모 패키지를 대신 넣어 주므로 의존이 사라지지는 않는다.
BUNDLED = {'mpl_toolkits': 'matplotlib'}

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


def _dyn_locals_of(path):
    """`'viz_mpm_continuum.py'` 같은 **문자열 상수**가 가리키는 모듈 이름들.

    ★ importlib 로 경로 로딩하는 간선을 잇는다.  import 문이 없어도 그 파일의 의존은
    런타임에 진짜로 필요하다 (2026-08-11 skimage 사고).

    ⚠ 조건을 **두 개** 건다.  이 리포는 docstring·help·오류안내에서 다른 모듈의 파일명을
    끊임없이 언급하므로, `'x.py'` 문자열을 전부 세면 그래프가 산문으로 뒤엉켜
    "필수 의존" 이 부풀고 도구가 거짓말을 하게 된다 (실측: step3_sigma 가 payload 의
    전 의존을 상속했다).
      ① 파일이 실제로 **동적 로딩을 한다** (importlib / spec_from_file_location / SourceFileLoader)
      ② 그 문자열이 **호출 인자**다 (`os.path.join(…, 'viz_mpm_continuum.py')`)
    산문 언급은 ②에서 걸러지고, 동적 로딩을 안 하는 파일은 ①에서 통째로 걸러진다."""
    try:
        src = open(path, encoding='utf-8').read()
        tree = ast.parse(src)
    except (OSError, SyntaxError):
        return set()
    if not any(t in src for t in ('importlib', 'spec_from_file_location', 'SourceFileLoader')):
        return set()
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                v = arg.value
                if v.endswith('.py') and '/' not in v and '\\' not in v:
                    out.add(v[:-3])
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
        # 문자열 경로로 로딩되는 로컬 모듈도 **같은 간선**으로 따라간다.
        for name in _dyn_locals_of(p):
            if name in local and name != m:
                q.append(name)
    return seen, ext


def required(entries=ENTRYPOINTS, scripts_dir=SCRIPTS):
    """필수(=optional 아님) 외부 의존 합집합 → sorted list."""
    out = set()
    for e in entries:
        if os.path.exists(os.path.join(scripts_dir, e + '.py')):
            out |= trace(e, scripts_dir)[1]
    return sorted(out - OPTIONAL)


def pip_names(mods):
    """import 이름 목록 → **설치 가능한** pip 이름 목록 (중복 제거, 순서 보존).

    BUNDLED 는 모 패키지로 접고(mpl_toolkits→matplotlib), PIP_NAME 은 배포판 이름으로
    바꾼다(skimage→scikit-image).  이 두 단계를 안 거치면 셋업 한 줄이 통째로 실패한다."""
    out = []
    for m in mods:
        n = PIP_NAME.get(BUNDLED.get(m, m), BUNDLED.get(m, m))
        if n not in out:
            out.append(n)
    return out


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
        # ★ 2026-08-11 skimage 사고의 회귀 — importlib 경로 로딩 간선
        w('g.py', "import importlib.util\n"
                  "def load():\n"
                  "    p = os.path.join(os.path.dirname(__file__), 'h.py')\n"
                  "    return importlib.util.spec_from_file_location('h', p)\n")
        w('h.py', 'import skimage\n')
        chk('8b) ★ importlib 경로 로딩 간선을 따라간다 (g→h→skimage)',
            'skimage' in trace('g', tmp)[1])
        # ⚠ 반대편: 산문에서 파일명을 언급만 하는 것은 간선이 아니다
        w('i.py', '"""자세한 것은 h.py 를 보라."""\nprint("h.py 참조")\n')
        chk('8c) ★ 산문·출력의 파일명 언급은 간선이 아니다 (그래프 부풀기 방지)',
            'skimage' not in trace('i', tmp)[1])
        # 동적 로딩을 안 하는 파일 안의 호출 인자 문자열도 간선이 아니다
        w('j.py', "import os\nprint(os.path.join('x', 'h.py'))\n")
        chk('8d) ★ importlib 을 안 쓰는 파일은 문자열을 안 따라간다',
            'skimage' not in trace('j', tmp)[1])
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
    # ★ 2026-08-11 밤 실측 회귀: 킷 payload 가 skimage 결손으로 죽었는데 이 도구는
    #   그것을 목록에 넣지 않았다 (viz_mpm_continuum 을 importlib 경로로 로드하기 때문).
    _, ext_pl = trace('mpm_webapp_payload')
    chk('10c) ★ payload 가 skimage 를 요구한다 (V100 3차 결손 = importlib 간선)',
        'skimage' in ext_pl)
    chk('10d) ★ mpl_toolkits 는 pip 목록에 안 들어간다 (그런 배포판이 없다)',
        'mpl_toolkits' not in pip_names(sorted(ext_pl)) and 'matplotlib' in pip_names(sorted(ext_pl)))
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
        # ★ **pip 이름**으로 대조한다.  모듈 이름으로 대조하면 skimage↔scikit-image 가
        #   영원히 어긋나고(설치는 맞는데 검사만 실패), mpl_toolkits 는 아예 설치 불가라
        #   가드가 항상 빨간불이 되어 **아무도 안 보게 된다** (경보 피로).
        missing = [m for m in pip_names(req) if m not in txt]
        chk(f'14) ★ setup_v100.sh 가 필수 패키지를 전부 담고 있다 (누락: {missing})', not missing)
    # ★ --check 자체의 회귀 (잠복 버그였다): 정확한 목록이 통과해야 하고,
    #   모듈 이름으로 적어도 통과해야 하며, 진짜 빠졌을 때만 실패해야 한다.
    import subprocess
    _td = os.path.join(SCRIPTS, 'trace_deps.py')
    _pip = ','.join(pip_names(required()))
    _mod = ','.join(required())
    for lab, lst, want in ((f'15) --check 가 pip 이름 목록을 통과시킨다', _pip, 0),
                           (f'16) --check 가 모듈 이름 목록도 통과시킨다', _mod, 0),
                           (f'17) ★ 진짜 빠지면 실패한다 (numpy 제거)',
                            ','.join(n for n in pip_names(required()) if n != 'numpy'), 1)):
        r = subprocess.run([sys.executable, _td, '--check', lst], capture_output=True, text=True)
        chk(f'{lab} → rc={r.returncode} {r.stdout.strip()[:60]}', r.returncode == want)

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
        # ★ 대조는 **pip 이름 공간**에서 한다 (2026-08-11 잠복 버그).  옛 코드는 모듈 이름
        #   (skimage, mpl_toolkits) 을 셋업의 pip 목록(scikit-image, matplotlib) 과 직접
        #   비교해서, 정확히 맞게 적어 둔 목록을 "부족" 이라 하고 그 이유로 **matplotlib 를
        #   지목**했다 (mpl_toolkits 가 없다는 뜻이었는데 그렇게 안 보인다).  둘 다 pip
        #   이름으로 접으면 모듈 이름으로 적든 pip 이름으로 적든 통과한다.
        have = pip_names([x.strip() for x in a.check.split(',') if x.strip()])
        miss = [n for n in pip_names(required(entries)) if n not in have]
        if miss:
            print('✗ 부족: ' + ', '.join(miss))
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

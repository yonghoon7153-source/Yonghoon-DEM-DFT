#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""방법론 규율 검사 v2 — D1~D5 를 **산문에서 검사로** 승격한다.

★ 왜 (CLAUDE.md 자기 진단):
    "리포는 같은 실수를 이미 3번 잡고(K 25.5 vs 영률 24 · SDCP pellet ×5.1 ·
     koo2026 0.20) **규칙으로 승격하지 않았다.**"

★★ v1 은 적대 감사(S0, 2026-08-12)에서 **연극으로 판정**됐다.  그 감사가 실증한 것:
  · 규칙 D 는 rejected 교정표본 3건 **밖에서 한 번도 발동한 적이 없다**
    (`COUNT_METRICS` 가 리포의 세는-양 이름 440종 중 18종 = 4 %만 덮었다)
  · CL-01 과 **물리적으로 동일한** 주장을 새 id·live 로 넣으면 오류 0
    (h1_predicts 를 "분담 ≈ 4 %" → "분담이 4 % 수준" 으로 말만 바꾸면 통과)
  · 등록부를 **비우면 통과** — 규칙을 지워도 초록불
  · 그러고도 화면은 `✓ 0 오류` + `거부됨 CL-01/02/03` 을 인쇄한다
    ⇒ **규칙이 작동한다는 증거처럼 보인다.  그것이 규칙이 없는 것보다 나쁘다.**
  · 규칙 B 의 판정 함수(`n_varying_axes`)는 인증하려는 성질과 **무관**했다 —
    45° 반셀 스태거는 k=2 인데 점 스탬프가 안 깨진다(오프셋 스윕 21점 중 13점 맹목).
    진짜 축은 obliqueness 가 아니라 **축간 경계교차의 위상 일치**다.
  · 4규칙이 **자기 동기를 못 덮었다** — K vs 영률은 **량(quantity) 범주 오류**인데
    량/단위 패리티 축이 없었다.

v2 의 설계 원칙 (감사에 대한 응답):
  ① 판정은 **거동**으로 — 이름·문자열이 아니라 실제로 돌려서 성질을 확인
  ② 거부 패턴을 **모든 live 주장**에 적용 (사후 라벨에만 적용하면 재발을 못 잡는다)
  ③ 등록부를 **비우면 오류** (규칙의 존재 자체를 검사)
  ④ 과잉차단 해소 — `kind` / `relation` / `parity_certified` 로 정당한 예외를 **기계 판독
     가능한 필드**로 (산문 탈출구 금지)
  ⑤ 못 막는 것은 **못 막는다고 적는다** — h0/h1 을 사람이 채우는 구멍은 정적 텍스트로
     닫히지 않는다.  유일한 실효 장치는 `prereg`(순서)다.

사용:
    python3 scripts/check_method_discipline.py
    python3 scripts/check_method_discipline.py --selftest
"""
from __future__ import annotations

import argparse
import ast                      # ⚠ 모듈 수준 — `_src_of` 가 모듈 함수라 지역 import 로는
                                #   안 보인다 (규칙 F 가 잡는 바로 그 패턴을 내가 냈다)
import glob
import inspect
import json
import os
import re
import sys
import unicodedata

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
LEDGER = os.path.join(ROOT, 'docs', 'reviews', 'claims.json')

#  ③ 등록부의 **존재**를 검사한다 — 비우면 규칙이 조용히 사라지던 것 (S0 X-2)
_RUNGS_MIN = 3
_DIAG_MIN = 2
_REQUIRED_REJECTED = frozenset({'CL-01', 'CL-02', 'CL-03'})   # 교정 표본. 사라지면 오류.


# ═══════════════════════════════════════════════════════════════════════════
# 규칙 A — 규약 패리티 (D4)
# ═══════════════════════════════════════════════════════════════════════════
#  relation 어휘 (S0 A-6 과잉차단 해소):
#    diagnoses               구현 충실도 진단 → 패리티 **필수**
#    independent_measurement frame[4] 다른 이산화의 독립 측정 → 패리티 **금지**,
#                            대신 `shared_input` 을 요구해 S4 순환성을 강제 점검
#    bounds                  a-fortiori 상/하한 → `direction` 을 적으면 불일치가 오류 아님
_RELATIONS = ('diagnoses', 'independent_measurement', 'bounds')

SOLVERS = {
    'step3_sigma.solve_sigma_z': {
        'adjacency': '6-face',
        'vox_um': 0.4,
        'periodic': True,                      # periodic_xy 인자를 받는다
        'why': '유한체적 ∇·(σ∇φ)=0 은 면을 공유하는 셀 사이에서만 플럭스를 정의한다',
        # ★ 선언을 **코드에 대조**한다 (아래 `verify_declared_adjacency`).
        'label_site': ('step3_sigma', 'solve_sigma_z'),
    },
}

DIAGNOSTICS = {
    'mpm_webapp_payload.electronic_connectivity': {
        'relation': 'diagnoses', 'target': 'step3_sigma.solve_sigma_z',
        'adjacency': '26-conn', 'vox_um': 0.30, 'periodic': False,
        'grid_source': 're-voxelized',
        'waiver': ('econn 의 목적은 STEP3 진단이 아니라 **이진 퍼콜레이션**(집전체까지 전자 '
                   '경로가 있는가 = dead-AM)이다.  26-conn 과 큰 복셀은 "이어진 한 가닥 = '
                   '한 도체" 를 만들기 위한 **의도된 선택**이며 함수 주석이 그렇게 적는다.'),
        'must_not_certify': ['fibre_stamp', 'raster fidelity', 'STEP3 connectivity',
                             'point vs segment', 'n_carbon_clusters 절대값',
                             'connected_pct 침대 간 비교', 'DEM 접촉 기준과 동일',
                             'seam 근방 AM 의 dead-AM 판정'],
        # S1b P1-①: cKDTree 에 boxsize 가 없어 seam 접촉을 놓친다.  실측 seam 전용 AM-AM
        #   접촉 = real14 10.2 % · kit 3.6~16.1 % (조성 의존 4.5배) → 공통모드 상쇄 안 됨.
        'periodic_waiver': '주기 seam 을 보지 않는다 — 경계 근방 입자의 연결 판정은 증언 불가',
        'label_site': ('mpm_webapp_payload', 'electronic_connectivity'),
    },
    'sr01_carbon_network.carbon_network_stats': {
        'relation': 'diagnoses', 'target': 'step3_sigma.solve_sigma_z',
        'adjacency': '6-face', 'vox_um': 0.4, 'periodic': False,
        'grid_source': 'solver-raster',
        'waiver': None,
        # ⚠ S1a: AM 마스크가 솔버 AM 상의 **진부분집합**(접촉 브릿지 볼 미포함) → plugged 는 하한
        'must_not_certify': ['plugged_frac 의 절대값 (하한만)', 'periodic 런의 성분 수'],
        'periodic_waiver': '기본(비주기) 런 전용 — 주기 런의 성분 수는 증언하지 않는다',
        # 이쪽은 이름 있는 라벨러가 있어 **거동 프로브**까지 간다 (정적 대조보다 강하다)
        'label_fn': 'sr01_carbon_network._label6',
        'label_site': ('sr01_carbon_network', 'carbon_network_stats'),
    },
}


def _resolve(dotted):
    """`a.b.c` → 객체.  중첩 모듈·클래스 메서드 지원 (S0 A-7)."""
    import importlib
    parts = dotted.split('.')
    for k in range(len(parts) - 1, 0, -1):
        try:
            obj = importlib.import_module('.'.join(parts[:k]))
        except ImportError:
            continue
        for p in parts[k:]:
            obj = getattr(obj, p)
        return obj
    raise ImportError(f'cannot resolve {dotted}')


#  ① 인접 규약은 **돌려서** 읽는다.  문자열 시그니처는 S0 A-2 에서 코딩 스타일 19종 중
#     16종을 오탐/미탐했다 (리포 label 호출의 64 %가 미탐, 솔버 자신 포함).
#     프로브 정확도 18/18.  독스트링 경고에도 영향받지 않는다 (S0 A-5 오탐 해소).
def probe_adjacency(fn_label):
    """라벨 함수(3D bool → (lab, n))를 **대각 두 셀**로 돌려 규약을 확정한다.

    대각 이웃은 6-face 에서 2성분, 26-conn 에서 1성분이다 — 이보다 짧은 판별 픽스처는 없다.
    """
    g = np.zeros((4, 4, 4), bool)
    g[1, 1, 1] = g[2, 2, 2] = True
    try:
        n = fn_label(g)
    except Exception:
        return None
    n = int(n[1] if isinstance(n, tuple) else n)
    return {2: '6-face', 1: '26-conn'}.get(n)


#  ② 선언된 `adjacency` 를 **코드에 대조**한다.
#     계기: v2 까지 `probe_adjacency` 는 selftest 에서만 돌고 등록부 검사에는 한 번도 쓰이지
#     않았다 — 즉 SOLVERS/DIAGNOSTICS 의 `adjacency` 는 전부 **검증되지 않은 문자열**이었고,
#     이 파일 자신이 솔버 **이름**에 대해서는 "검증되지 않는 선언" 이라며 오류로 막고 있었다.
#     등록부가 틀리면 규칙 A 전체가 조용히 무의미해진다 (D4 의 뿌리).
#  두 경로:
#     (a) `label_fn` — 이름 있는 라벨러 → **거동 프로브** (가장 강함)
#     (b) `label_site` — 함수 안의 `ndimage.label(...)` 호출을 **AST 로** 읽는다.
#         정규식이 아니다 (S0 A-2 에서 문자열 시그니처는 19종 중 16종을 오탐/미탐했다).
#         `structure` 없음 = scipy 기본 = 6-face · `np.ones((3,3,3))` = 26-conn.
_CONN_OF_STRUCT = {None: '6-face', '3x3x3': '26-conn'}


def _ast_label_conns(module_name, func_name):
    """`module.func` 안의 ndimage.label 호출들이 쓰는 인접 규약 집합을 돌려준다."""
    import ast
    import importlib
    mod = importlib.import_module(module_name)
    src = open(mod.__file__, encoding='utf-8').read()
    tree = ast.parse(src)
    target = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
            target = node
            break
    if target is None:
        raise LookupError(f'{module_name}.{func_name} 를 AST 에서 못 찾았다')
    conns = set()
    for node in ast.walk(target):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if not (isinstance(f, ast.Attribute) and f.attr == 'label'):
            continue
        st = next((k.value for k in node.keywords if k.arg == 'structure'), None)
        if st is None and len(node.args) >= 2:
            st = node.args[1]
        if st is None:
            conns.add('6-face')
            continue
        src = _src_of(st)
        if '3, 3, 3' in src or '3,3,3' in src:
            conns.add('26-conn')
        else:
            conns.add(f'UNKNOWN({src})')
    return conns


def _src_of(node):
    """AST 노드 → 소스 문자열.  ⚠ `ast.unparse` 는 **Python 3.9+** 다.

    실사고 2026-08-16: 원격 GPU 호스트가 py3.8 이라 `AttributeError: module 'ast' has no
    attribute 'unparse'` 로 규율 검사가 **fail-closed** 되어 런 게이트를 못 넘었다.
    (fail-closed 자체는 옳은 동작 — 조용히 통과시키지 않았다.)
    ⇒ 3.9+ 면 `unparse`, 아니면 우리가 쓰는 노드 모양만 직접 복원한다.  둘 다 안 되면
      `UNKNOWN(...)` 로 남겨 **여전히 fail-closed** 다 (추측으로 통과시키지 않는다).
    """
    up = getattr(ast, 'unparse', None)
    if up is not None:
        return up(node)
    # py3.8 대체 — `np.ones((3,3,3), bool)` · `generate_binary_structure(3, 1)` 류만 복원
    if isinstance(node, ast.Tuple):
        return '(' + ', '.join(_src_of(e) for e in node.elts) + ')'
    if isinstance(node, ast.List):
        return '[' + ', '.join(_src_of(e) for e in node.elts) + ']'
    if isinstance(node, ast.Num):                       # py3.8: 상수는 Num/Str/NameConstant
        return repr(node.n)
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f'{_src_of(node.value)}.{node.attr}'
    if isinstance(node, ast.Call):
        parts = [_src_of(a) for a in node.args]
        parts += [f'{k.arg}={_src_of(k.value)}' for k in node.keywords if k.arg]
        return f'{_src_of(node.func)}({", ".join(parts)})'
    return f'<{type(node).__name__}>'


def verify_declared_adjacency(name, spec):
    """선언 ≠ 코드 이면 오류 문자열, 확인되면 근거 문자열, 확인 불가면 오류 문자열."""
    decl = spec.get('adjacency')
    if 'label_fn' not in spec and 'label_site' not in spec:
        return False, (f'{name}: `adjacency` 가 **검증되지 않는 선언**이다 — `label_fn`(거동 '
                       f'프로브) 또는 `label_site`(AST 대조) 중 하나는 필수.  등록부가 틀리면 '
                       f'규칙 A 전체가 조용히 무의미해진다')
    if 'label_fn' in spec:
        try:
            fn = _resolve(spec['label_fn'])
        except Exception as e:
            return False, (f'{name}: label_fn `{spec["label_fn"]}` 를 불러올 수 없다 '
                           f'({type(e).__name__}) — fail-closed 로 오류 처리한다')
        got = probe_adjacency(fn)
        if got is None:
            return False, (f'{name}: label_fn 프로브가 규약을 판정하지 못했다 (unknown) '
                           f'— fail-closed.  모르면 통과가 아니라 오류다')
        if got != decl:
            return False, (f'{name}: 선언 {decl} 인데 **거동은 {got}** (대각 두 셀 프로브)')
        return True, f'{name}: {decl} — 거동 프로브로 확인'
    try:
        conns = _ast_label_conns(*spec['label_site'])
    except Exception as e:
        return False, (f'{name}: label_site AST 대조 실패 ({type(e).__name__}: {e}) '
                       f'— fail-closed')
    if not conns:
        return False, (f'{name}: {spec["label_site"][1]} 안에서 라벨 호출을 찾지 못했다 '
                       f'— 규약을 코드로 확인할 수 없으므로 fail-closed')
    bad = [c for c in conns if c.startswith('UNKNOWN')]
    if bad:
        return False, f'{name}: 라벨 structure 를 해석하지 못했다 {sorted(bad)} — fail-closed'
    if conns != {decl}:
        return False, (f'{name}: 선언 {decl} 인데 **코드는 {sorted(conns)}** '
                       f'({".".join(spec["label_site"])})')
    return True, f'{name}: {decl} — AST 대조로 확인 ({len(conns)} 규약 일치)'


#  ③ 지역 import 그림자 — `UnboundLocalError` 를 정적으로 잡는다.
#     계기 (2026-08-12 실사고): `mpm_webapp_payload.py` 는 모듈 수준에서 `import os as _os`
#     인데 어떤 함수 안에 `import os` 가 있었다.  그러면 그 함수에서 `os` 는 **지역명**이 되고,
#     그 대입보다 앞줄의 `os.path.exists(...)` 는 UnboundLocalError 다.  그 예외를 근처의
#     `except Exception` 이 삼켜 **선분 스탬프가 조용히 꺼졌다** — 런은 성공한 것처럼 끝나고
#     요청과 다른 규약을 쟀다.  한 건을 고치는 대신 **패턴을 검사로 승격**한다.
def find_local_import_shadows(path):
    """(errors, collisions) — 지역 import 로 생기는 UnboundLocalError 위험과 이름 충돌.

    errors     : 그 이름이 **오직 import 로만** 묶이는데 그 줄보다 앞에서 쓰인다 = 확실한 위험
    collisions : 같은 함수에서 한 이름이 **일반 대입과 import 양쪽**에 묶인다 = 재바인딩 위험
                 (예: dict `_tb` 를 쓰다가 except 안에서 `import traceback as _tb`)
    ⚠ 정밀화 이유: 첫 판은 일반 대입을 안 봐서 `_tb` 를 12건 오탐했다.  오탐이 많으면
      검사기를 끄게 되고, 그러면 규칙이 없는 것보다 나쁘다 (S0 의 교훈).
    ⚠ 2026-08-13 (Codex CDX-10): `ast.walk` 가 **중첩 함수 안으로 내려가** 그쪽 지역 import 를
      바깥 함수 것으로 오인했다 — 중첩 함수는 자기 스코프라 바깥은 멀쩡한데 오류를 냈다
      (재현: 바깥이 `os.path` 를 쓰고 안쪽 함수가 `import os` 하면 런타임 정상인데 오탐).
      ⇒ 스코프 경계(중첩 def/lambda/class)에서 멈추는 순회로 교체.  중첩 함수 자신은
      바깥 루프가 따로 잡으므로 검사에서 빠지지 않는다.
    """
    import ast

    def own_scope(fn):
        """fn 의 **자기 스코프** 노드만 (중첩 def/lambda/class 는 경계에서 자른다)."""
        out, stack = [], list(ast.iter_child_nodes(fn))
        while stack:
            n = stack.pop()
            out.append(n)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef,
                              ast.Lambda, ast.ClassDef)):
                continue                              # 다른 스코프 — 내려가지 않는다
            stack.extend(ast.iter_child_nodes(n))
        return out

    tree = ast.parse(open(path, encoding='utf-8').read())
    errs, coll = [], []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        imp = {}                                      # import 로 묶이는 이름 → 첫 줄
        asg = {}                                      # 그 외 대입으로 묶이는 이름 → 첫 줄
        for a in list(fn.args.args) + list(fn.args.kwonlyargs) + list(fn.args.posonlyargs):
            asg[a.arg] = 0
        body = own_scope(fn)
        for n in body:
            if isinstance(n, (ast.Global, ast.Nonlocal)):
                for nm in n.names:                    # global/nonlocal 선언 = 지역 아님
                    asg[nm] = 0
        for n in body:
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                for al in n.names:
                    nm = (al.asname or al.name).split('.')[0]
                    imp[nm] = min(imp.get(nm, 10 ** 9), n.lineno)
            elif isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                asg[n.id] = min(asg.get(n.id, 10 ** 9), n.lineno)
        for n in body:
            if not (isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)):
                continue
            if n.id not in imp or n.lineno >= imp[n.id]:
                continue
            if n.id in asg and asg[n.id] <= n.lineno:
                continue                              # 앞에서 일반 대입됨 → unbound 아님
            errs.append((fn.name, n.id, n.lineno, imp[n.id]))
        for nm in sorted(set(imp) & set(asg)):
            coll.append((fn.name, nm, asg[nm], imp[nm]))
    return sorted(set(errs)), sorted(set(coll))


# ⚠ 2026-08-13 (Codex CDX-10): 손으로 적은 6-파일 목록은 tracked 415 개의 **1.4 %** 였다 —
#   그 목록에 없던 신규 `fibre_1d_network.py` 는 검사 밖이었다.  이제 `scripts/**/*.py` 를
#   **자동 열거**한다 (스코프 정정 후 전 리포 0 오류를 확인하고 올렸다).  목록이 낡을 일이 없다.
_SHADOW_ALWAYS = ('mpm_webapp_payload.py', 'step3_sigma.py', 'mpm3d_compaction.py',
                  'network_conductivity.py', 'sr01_carbon_network.py',
                  'fibre_segment_raster.py')


def _shadow_scan_files():
    """스캔 대상 = scripts/**/*.py 전부.  `_SHADOW_ALWAYS` 는 **반드시 있어야 하는** 최소집합
    (사라지면 fail-closed — 실사고가 났던 파일들이라 조용히 빠지면 안 된다)."""
    root = os.path.join(ROOT, 'scripts')
    found = sorted(os.path.relpath(p, root)
                   for p in glob.glob(os.path.join(root, '**', '*.py'), recursive=True))
    return found


def check_local_import_shadows(verbose=True):
    errs, warns = [], []
    root = os.path.join(ROOT, 'scripts')
    scan = _shadow_scan_files()
    for must in _SHADOW_ALWAYS:                       # fail-closed — 실사고 파일이 빠지면 거부
        if must not in scan:
            errs.append(f'{must}: 반드시 스캔해야 하는 파일인데 없다 (fail-closed)')
    for fname in scan:
        fp = os.path.join(root, fname)
        try:
            hits, coll = find_local_import_shadows(fp)
        except SyntaxError as ex:
            warns.append(f'{fname}: 파싱 불가 ({ex.__class__.__name__}) — 스캔에서 건너뜀')
            continue
        for func, nm, use, imp in hits:
            errs.append(f'{fname}:{use} `{nm}` 가 함수 `{func}` 의 지역 import(:{imp})보다 '
                        f'**앞에서** 쓰인다 — UnboundLocalError.  근처 except 가 삼키면 '
                        f'기능이 조용히 꺼진다')
        for func, nm, aline, iline in coll:
            warns.append(f'{fname}: `{nm}` 이 함수 `{func}` 에서 대입(:{aline})과 '
                         f'import(:{iline}) 양쪽에 묶인다 — 그 import 가 실행되면 앞의 값이 '
                         f'덮인다 (오류는 아니지만 이름을 갈라 놓을 것)')
        if verbose and not hits:
            print(f'  OK      {fname}: 지역 import 그림자 없음'
                  + (f'  (⚠ 이름 충돌 {len(coll)}건)' if coll else ''))
    return errs, warns


def check_convention_parity(verbose=True):
    errs, warns = [], []
    # ★ 등록부의 adjacency 를 먼저 **검증**한다 — 이 검사가 없으면 아래 패리티는
    #   틀린 선언끼리 맞춰보는 것이 된다.
    for _reg, _kind in ((SOLVERS, 'SOLVER'), (DIAGNOSTICS, 'DIAG')):
        for _n, _s in _reg.items():
            ok, msg = verify_declared_adjacency(_n, _s)
            if not ok:
                errs.append(msg)
            elif verbose:
                print(f'  verify  {msg}')
    # ★ 진단도 **불러올 수 있어야** 한다 (v2 는 SOLVERS 만 확인했다 — Codex #9 fail-closed)
    for dname in DIAGNOSTICS:
        try:
            _resolve(dname)
        except Exception as e:
            errs.append(f'DIAGNOSTICS 키 `{dname}` 를 불러올 수 없다 ({type(e).__name__}) '
                        f'— 진단 규약이 **검증되지 않는 선언**이 된다 (fail-closed)')
    if len(DIAGNOSTICS) < _DIAG_MIN:                      # ③ 비우면 오류
        errs.append(f'DIAGNOSTICS 가 {len(DIAGNOSTICS)}개 — 최소 {_DIAG_MIN}.  '
                    f'등록부를 비우면 규칙 A 가 조용히 사라진다')
    for sname in SOLVERS:                                 # 솔버 이름도 코드에서 확인 (S0 A-1)
        try:
            _resolve(sname)
        except Exception as e:
            errs.append(f'SOLVERS 키 `{sname}` 를 불러올 수 없다 ({type(e).__name__}) '
                        f'— 솔버 규약이 **검증되지 않는 선언**이 된다')
    for dname, d in DIAGNOSTICS.items():
        rel = d.get('relation')
        if rel not in _RELATIONS:
            errs.append(f'{dname}: relation 은 {_RELATIONS} 중 하나여야 한다')
            continue
        if rel == 'independent_measurement':              # ④ frame[4] — 패리티 금지
            if not d.get('shared_input', 'MISSING') != 'MISSING':
                errs.append(f'{dname}: independent_measurement 는 `shared_input` 필수 '
                            f'(없으면 null) — 일치가 강제되는 경로를 명시해야 한다')
            elif verbose:
                print(f'  frame[4] {dname}: 독립 측정 — 패리티 미적용, shared_input='
                      f'{d.get("shared_input")!r}')
            continue
        if rel == 'bounds':
            if d.get('direction') not in ('upper', 'lower'):
                errs.append(f'{dname}: bounds 는 direction ∈ {{upper,lower}} 필수')
            elif verbose:
                print(f'  bounds  {dname}: {d["direction"]}-bound — 불일치가 오류 아님')
            continue
        solver = SOLVERS.get(d.get('target'))
        if solver is None:
            errs.append(f'{dname}: target {d.get("target")} 가 SOLVERS 에 없다')
            continue
        if d['adjacency'] != solver['adjacency'] and not d.get('waiver'):
            errs.append(f'{dname}: 솔버 {solver["adjacency"]} ≠ 진단 {d["adjacency"]} '
                        f'이고 waiver 가 없다 (D4)')
        # ★ grid 도 채점한다 — v1 은 `grid` 를 한 번도 읽지 않았다 (S0 A-3).
        #   econn 결함은 26-conn **과** 0.30 µm 둘 다였다.
        if abs(float(d['vox_um']) - float(solver['vox_um'])) > 1e-9 and not d.get('waiver'):
            errs.append(f'{dname}: 격자 {d["vox_um"]} µm ≠ 솔버 {solver["vox_um"]} µm '
                        f'이고 waiver 가 없다 (D4 — 규약만 맞추고 격자를 흘리면 안 된다)')
        if d.get('grid_source') == 're-voxelized' and not d.get('waiver'):
            errs.append(f'{dname}: 재복셀화(grid_source) 는 waiver 필수 — 솔버가 실제로 푼 '
                        f'격자를 보지 않는다')
        # ★ 주기 축 (S0 A-4): 같은 인접 규약이어도 솔버가 감고 진단이 안 감으면 다른 그래프
        if solver.get('periodic') and not d.get('periodic') and not d.get('periodic_waiver'):
            errs.append(f'{dname}: 솔버는 주기 wrap 을 다루는데 진단은 그 face 를 안 본다 '
                        f'— periodic_waiver 로 포기를 명시할 것')
        if d['adjacency'] != solver['adjacency'] and d.get('waiver') \
                and not d.get('must_not_certify'):
            errs.append(f'{dname}: waiver 는 있는데 must_not_certify 가 비었다')
        elif verbose:
            print(f'  {"waiver " if d.get("waiver") else "OK     "} {dname}: '
                  f'{d["adjacency"]} @{d["vox_um"]} µm')
    return errs, warns


# ═══════════════════════════════════════════════════════════════════════════
# 규칙 B — 판별력 있는 rung (D2)
# ═══════════════════════════════════════════════════════════════════════════
#  ★ v1 의 `is_axis_aligned` 는 **틀린 성질**이었다 (S0 B-1/B-2 실증):
#    · 충분조건 아님 — 45° 반셀 스태거·(1,1,1) 3중 스태거·L자·미세노이즈 전부 k≥2 인데
#      점 스탬프가 안 깨진다.  45° 오프셋 스윕 21점 중 **13점(62 %)이 맹목**.
#    · 필요조건 아님 — 축정렬이라도 step/vox ≥ 1.25 면 깨진다 (리포 서브샘플 경로에 실재:
#      mpm_webapp_payload.py:132 "0.14→~4 µm ... would falsely fragment conductors").
#    진짜 축은 obliqueness 가 아니라 **축간 경계교차의 위상 일치**이고, 리포의 canonical
#    rung 이 작동하는 것은 세 축 위상이 완전 동상이라는 **우연**이었다.
#  ⇒ 이름 대신 **거동**으로 판정한다.
def n_varying_axes(pts, tol=1e-9):
    P = np.asarray(pts, float)
    if P.ndim != 2 or len(P) < 2:
        return 0
    return int(((P.max(0) - P.min(0)) > tol).sum())


def assert_stamp_discriminating(pts, vox, name):
    """이 픽스처가 점↔선분 스탬프를 **실제로 가르는가**를 돌려서 확인한다.

    `n_varying_axes` 로는 알 수 없다 (S0 B-1).  가능도비가 1 인 픽스처는 시험이 아니다.
    """
    from fibre_segment_raster import n_components_6face, point_cells, polyline_cells
    P = np.asarray(pts, float)
    npt = n_components_6face(np.unique(point_cells(P, vox), axis=0))
    nsg = n_components_6face(np.unique(polyline_cells(P, vox), axis=0))
    if not (npt > 1 and nsg == 1):
        raise AssertionError(
            f'픽스처 "{name}" 은 점↔선분 규약을 **가르지 못한다** (점 {npt} · 선분 {nsg}). '
            f'가능도비 1 = 이 시험은 결함을 영원히 통과시킨다.  격자 경계교차의 위상을 '
            f'어긋나게 하거나(오프셋), step/vox 를 바꿀 것.')
    return True


def _staggered_blind_fixture():
    """★ 비축정렬(k=3)인데 점 스탬프가 **안 깨지는** 픽스처.

    ⚠ 이 좌표는 우연이 아니다.  생산 점 간격 `0.7·dx`(=0.0987 µm @dx 0.141) 에서 축 오프셋
    (0, 0.20, 0.10) 이면 세 축의 경계교차 위상이 어긋나 L1 점프가 1 로 유지된다 → 1 성분.
    같은 방향·같은 오프셋이라도 **간격을 0.1 로 바꾸면 16 성분으로 깨진다** — 즉
    "대각으로 짜라" 는 조언은 간격까지 같이 정하지 않으면 무의미하다.
    (v2 를 짜면서 내가 간격 0.1 을 써서 이 시험을 통과시켰다가 실측 스캔에서 잡혔다.)
    """
    st = 0.7 * 0.141                                      # 생산 규약 (additives.py:643)
    t = np.arange(0, 60) * st + 0.3
    return np.stack([t, t + 0.20, t + 0.10], axis=1)


def _rung_oblique_segment():
    """비스듬한 1D 도체 — 점은 깨지고 선분은 안 깨진다 (알려진 정답)."""

    P = np.stack([np.linspace(0.3, 6.3, 60)] * 3, axis=1)
    assert_stamp_discriminating(P, 0.4, 'oblique 1D conductor')
    return True, '대각 도체: 점↔선분을 가른다 (거동으로 확인)'


def _rung_staggered_is_blind():
    """★ 대조군: **비축정렬인데도** 위상을 어긋내면 결함이 안 보인다 (v1 이 놓친 것)."""
    from fibre_segment_raster import n_components_6face, point_cells
    P = _staggered_blind_fixture()
    npt = n_components_6face(np.unique(point_cells(P, 0.4), axis=0))
    return (npt == 1 and n_varying_axes(P) >= 2,
            f'스태거 대각: k={n_varying_axes(P)} 인데 점 스탬프도 {npt} 성분 '
            f'→ **비축정렬은 판별력의 보증이 아니다**')


def _rung_substep_sampling_is_blind():
    """축정렬이어도 step/vox ≥ 1.25 면 깨진다 = obliqueness 는 필요조건도 아니다."""
    from fibre_segment_raster import n_components_6face, point_cells
    P = np.stack([np.arange(0, 20) * 0.5, np.full(20, 1.1), np.full(20, 2.1)], axis=1)
    npt = n_components_6face(np.unique(point_cells(P, 0.4), axis=0))
    return (npt > 1 and n_varying_axes(P) == 1,
            f'축정렬 step/vox=1.25: 점 {npt} 성분 → 축정렬도 깨질 수 있다')


RUNGS = {
    'raster (oblique, discriminating)': _rung_oblique_segment,
    'raster (staggered oblique = BLIND control)': _rung_staggered_is_blind,
    'raster (axis-aligned but step/vox≥1.25 = breaks)': _rung_substep_sampling_is_blind,
}


def check_oblique_rungs(verbose=True):
    errs, warns = [], []
    if len(RUNGS) < _RUNGS_MIN:                            # ③ 비우면 오류 (S0 X-2)
        errs.append(f'RUNGS 가 {len(RUNGS)}개 — 최소 {_RUNGS_MIN}')
    for name, fn in RUNGS.items():
        try:
            ok, msg = fn()
        except Exception as e:
            #  ★ 실행 실패를 **오류**로 (v1 은 warns 로 빠져 규칙이 조용히 사라졌다, S0 B-5)
            errs.append(f'{name}: 실행 불가 ({type(e).__name__}: {e}) — rung 이 안 돌면 '
                        f'규칙 B 는 없는 것이다')
            continue
        if ok and verbose:
            print(f'  OK      {name}: {msg}')
        elif not ok:
            errs.append(f'{name}: {msg}')
    return errs, warns


# ═══════════════════════════════════════════════════════════════════════════
# 규칙 C·D·E — 판별력 / 개수≠귀결 / 량 패리티
# ═══════════════════════════════════════════════════════════════════════════
_KINDS = ('hypothesis', 'convention', 'measurement_record')
_STATUS = ('live', 'retired', 'rejected', 'retrospective', 'hold')
#  ★ evidence_state (2026-08-12, Codex 재검증 P1 §4): v2 는 `evidence_state` 를 **읽지 않아**
#    문서상 hold 가 실제 인용차단이 아니었다.  active 가 아닌 live 주장은 **오류**로 만든다.
_EVIDENCE_OK = ('active', None)

#  ① 이름 화이트리스트 → **패턴**.  v1 의 10개 어휘는 리포의 세는-양 440종 중 18종(4 %)만
#    덮었다 — `se_se_cn`(118회)·`f_perc`(101)·`percolation_pct`(109), 심지어 현행 live
#    주장 자신의 `plugged_frac`/`largest_mass_frac` 도 미등재였다 (S0 D-1).
_COUNT_RE = re.compile(
    r'(^|_)(n|num|count)($|_)'
    r'|_(count|cn|components?|contacts?|pieces|fragments|clusters|edges|dof)$'
    r'|_(frac|fraction|pct|share|ratio)$'
    r'|^(share|ratio|percolation_pct|f_perc|f_intact|f_broken)')

#  ② 귀결 어휘 3갈래.  v1 은 '검증'(1118회)·'일치'(405)·'교차검증'(157)·'증명'(101)·
#    '차단'(204)·'병목'·'율속'·'끊' 을 전부 놓쳤다 — S4 가 찾는 어휘가 하나도 없었다.
_CONSEQ_TRANSPORT = ('단절', '끊', '차단', '병목', '율속', '절연', '고립', '퍼콜', 'percolat',
                     'severed', 'disconnected', 'isolated', 'bottleneck', 'rate-limit',
                     'dead', '전기적으로 죽', '활성', 'active')
_CONSEQ_CAUSAL = ('지배', '기여', '원인', '때문', '유발', '하중분담', 'load share',
                  'load-bearing', 'dominates', 'contributes', 'causes', 'responsible',
                  'determines', 'explains', 'implies', '따라서', 'therefore')
#  ★ 신설 — 이 갈래는 count 가 아니어도 `shared_input` 을 요구한다 (S4 를 규칙 안으로 흡수)
_CONSEQ_VERIF = ('검증', '일치', '교차검증', '증명', '정당', '보장', '수렴', 'validat',
                 'confirm', 'agree', 'cross-valid', 'proves', 'justif', 'converg')
CONSEQUENCE_WORDS = _CONSEQ_TRANSPORT + _CONSEQ_CAUSAL + _CONSEQ_VERIF

#  ★ 규칙 E — 량 패리티.  CLAUDE.md 가 자책한 3건(K vs 영률 · pellet ×5.1 · koo2026)은
#    전부 **량/단위/스케일** 계열인데 v1 4규칙에 그 축이 없었다 (S0 X-1).
#    C-6 의 원리적 한계와 달리 이것은 정적으로 **완전히 검사 가능**하다.
_QUANTITY_ALIASES = {
    'bulk_modulus': 'K', 'youngs_modulus': 'E', 'shear_modulus': 'mu',
    'conductivity_material': 'sigma_mat', 'conductivity_line': 'sigma_line',
    'conductivity_effective': 'sigma_eff', 'toughness_KIC': 'K_IC',
    'energy_release_Gc': 'G_c', 'porosity_eps_sphere': 'eps_sphere',
    'porosity_union': 'eps_union',
}


def _norm(s):
    """표기 정규화 — 공백 1개·마침표·전각 %·`0` vs `0.0` 로 무력화되던 것 (S0 C-1)."""
    if s is None:
        return ''
    t = unicodedata.normalize('NFKC', str(s)).casefold()
    t = re.sub(r'(\d+\.?\d*)', lambda m: repr(float(m.group(1))), t)
    return re.sub(r'[\s.,;:!?~≈%()\[\]{}<>/\-_]+', '', t)


def _nums(s):
    return [float(x) for x in re.findall(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?', str(s or ''))]


def _reject_reasons(c):
    """★ **모든** live 주장에 적용되는 거부 패턴.

    v1 은 이 판정을 `status == 'rejected'` 라벨이 붙은 것에만 실질 적용했고, 물리적으로
    동일한 주장을 새 id·live 로 넣으면 오류 0 이었다 (S0 C-5, 가장 위험한 구멍).
    """
    out = []
    if c.get('kind', 'hypothesis') != 'hypothesis':
        return out                                        # 규약·기록은 가설검정이 아니다
    h0p, h1p = c.get('h0_predicts'), c.get('h1_predicts')
    # C-1 표기 정규화 동등
    if _norm(h0p) == _norm(h1p):
        out.append(f'C_EQUAL_PREDICTION| **가능도비 1** — h0 와 h1 이 똑같이 "{h0p}" 를 예측한다 (D1)')
    else:
        # C-2 분해능: 차이가 측정 산포보다 작으면 증거량은 CL-01 과 같다
        n0, n1 = _nums(h0p), _nums(h1p)
        # ★ 상보 부등호는 **완벽히 판별적**이다 (`< X` vs `>= X`) — 같은 수를 쓴다고 가능도비 1
        #   이 아니다.  2026-08-12 CL-10 등록 때 이 과잉차단이 실제로 발생했다 (S0 가 경고한 류).
        _LO = ('<', '≤', '미만', '이하', '작다', '보다 작')
        _HI = ('>', '≥', '이상', '초과', '크다', '보다 크')
        _a, _b = str(h0p), str(h1p)
        if (any(t in _a for t in _LO) and any(t in _b for t in _HI)) or \
           (any(t in _a for t in _HI) and any(t in _b for t in _LO)):
            return out                                    # 문턱 양쪽 = 판별적
        res = c.get('resolution')
        if res is not None and len(n0) == 1 and len(n1) == 1:
            if abs(n0[0] - n1[0]) < float(res):
                out.append(f'C_SUB_RESOLUTION| 두 예측의 차이 {abs(n0[0]-n1[0]):.4g} 가 분해능 {res} 미만 '
                           f'— 분해능 아래의 판별력은 가능도비 1 과 같다')
        # C-3 구간 겹침
        if len(n0) == 2 and len(n1) == 2:
            if min(n0[1], n1[1]) >= max(n0[0], n1[0]):
                out.append(f'C_INTERVAL_OVERLAP| 두 예측 구간이 겹친다 {n0} ∩ {n1} — 관측이 양쪽에 든다')
    # C-4 measured ↔ verdict 정합
    mv = _nums((c.get('measured') or {}).get('value'))
    vd = _norm(c.get('verdict'))
    if len(mv) == 1 and vd:
        for tag, pred in (('h0채택', h0p), ('h1채택', h1p)):
            other = h1p if tag == 'h0채택' else h0p
            if tag in vd and _nums(other) and _nums(pred):
                if abs(mv[0] - _nums(other)[0]) < abs(mv[0] - _nums(pred)[0]):
                    out.append(f'C_VERDICT_INCONSISTENT| 측정 {mv[0]} 이 채택하지 않은 가설에 더 가까운데 '
                               f'verdict 가 "{c.get("verdict")}" 다')
    # 규칙 D — 개수 ≠ 귀결.  scan 대상을 claim+asserted+verdict 로 (S0 D-3)
    metric = str((c.get('measured') or {}).get('metric', ''))
    text = ' '.join(str(c.get(k, '')) for k in ('claim', 'asserted', 'verdict'))
    hit_t = [w for w in _CONSEQ_TRANSPORT + _CONSEQ_CAUSAL if w in text]
    hit_v = [w for w in _CONSEQ_VERIF if w in text]
    br = c.get('bridge')
    br_ok = isinstance(br, dict) or (isinstance(br, str) and len(_norm(br)) >= 12) \
        or c.get('parity_certified')                      # D-6 과잉차단 해소
    if _COUNT_RE.search(metric) and hit_t and not br_ok:
        out.append(f'D_COUNT_NOT_CONSEQUENCE| `{metric}` 은 **세는 양**인데 귀결({hit_t[:2]})을 주장하면서 쓸 만한 '
                   f'bridge 가 없다 (규칙 D)')
    # ★ 검증-귀결 갈래는 count 가 아니어도 shared_input 을 요구 (S4 흡수)
    if hit_v and 'shared_input' not in c:
        out.append(f'D_VERIF_NO_SHARED_INPUT| 검증-귀결 어휘({hit_v[:2]})를 쓰면서 `shared_input` 이 없다 — '
                   f'A 와 B 가 입력을 공유해 일치가 강제되는 경로를 적어야 한다 (없으면 null)')
    # 규칙 E — 량 패리티 (S0 X-1)
    q = c.get('quantity')
    qa = c.get('compared_to_quantity')
    if q and qa and _QUANTITY_ALIASES.get(q, q) != _QUANTITY_ALIASES.get(qa, qa):
        out.append(f'E_QUANTITY_MISMATCH| **량 범주 오류** — {q} 를 {qa} 와 비교한다 (규칙 E). '
                   f'K 25.5 vs 영률 24 가 이 형태였다')
    return out


def _codes(reasons):
    """거부 사유 문자열들에서 기계 코드 집합을 뽑는다."""
    return {r.split('|', 1)[0].strip() for r in reasons if '|' in r.split(' ', 1)[0] or '| ' in r[:32]}


def _msg(reason):
    """인쇄용 — 코드 접두를 뗀다."""
    return reason.split('| ', 1)[1] if '| ' in reason[:32] else reason


_REQUIRED = ('id', 'claim', 'measured', 'asserted', 'status')
_REQ_HYP = ('h0', 'h1', 'h0_predicts', 'h1_predicts')


def check_claim(c):
    e = []
    for k in _REQUIRED:
        if k not in c or c[k] in (None, '', {}):
            e.append(f'{c.get("id", "?")}: 필수 필드 `{k}` 누락')
    if e:
        return e
    if c['status'] not in _STATUS:
        e.append(f'{c["id"]}: status 는 {_STATUS} 중 하나')
    if c.get('kind', 'hypothesis') not in _KINDS:
        e.append(f'{c["id"]}: kind 는 {_KINDS} 중 하나')
    m = c['measured']
    if not isinstance(m, dict) or not str(m.get('metric', '')).strip():
        e.append(f'{c["id"]}: measured 는 {{metric,value,unit}} — metric 이 비었다')
    if c.get('kind', 'hypothesis') == 'hypothesis':
        for k in _REQ_HYP:
            if k not in c or c[k] in (None, ''):
                e.append(f'{c["id"]}: 가설 주장은 `{k}` 필수 (규약/기록이면 kind 를 바꿀 것)')
    else:                                                  # C-8 과잉차단 해소
        if not c.get('provenance'):
            e.append(f'{c["id"]}: kind={c["kind"]} 는 `provenance` 필수 '
                     f'(코드 위치·기본값·누가 언제 정했나)')
    # ── 규칙 G (2026-08-13, Codex CDX-11) — 대체된 주장이 live 로 남으면 안 된다 ────────
    #   실사고: CL-20 은 `superseded_by: CL-21` 을 달고 verdict 안에서 자기 결론을 무효화하면서도
    #   `status: live` 로 검사기를 통과했다.  그 상태의 원장을 읽은 사람은 철회된 하한 논증을
    #   현재형으로 인용하게 된다 (실제로 `diameter_preserving_sigma` 의 provenance 가 그것을
    #   새 payload 마다 다시 찍어내고 있었다 — 같은 날 CDX-14 로 적발).
    if c.get('superseded_by') and c['status'] == 'live':
        e.append(f'{c["id"]}: `superseded_by`({c["superseded_by"]}) 가 있는데 status=live — '
                 f'대체된 주장은 retired/hold 여야 한다 (규칙 G)')
    return e + _reject_reasons(c)


def check_claims_ledger(path=LEDGER, verbose=True):
    errs, warns = [], []
    if not os.path.exists(path):
        return [f'claims 원장이 없다: {path}'], warns
    claims = json.load(open(path, encoding='utf-8')).get('claims', [])
    if not claims:
        return ['claims 원장이 비었다 — 규칙 C·D 가 사라진다'], warns
    ids = [c.get('id') for c in claims]
    for dup in {i for i in ids if ids.count(i) > 1}:
        errs.append(f'중복 id: {dup}')
    rej_ids = {c['id'] for c in claims if c.get('status') == 'rejected'}
    if not _REQUIRED_REJECTED <= rej_ids:                  # ③ 교정 표본이 사라지면 오류
        errs.append(f'교정 표본 {sorted(_REQUIRED_REJECTED - rej_ids)} 이 원장에서 사라졌다 '
                    f'— 규칙이 이빨 빠졌는지 검사할 수단이 없어진다')
    n_live = 0
    for c in claims:
        bad = check_claim(c)
        st = c.get('status')
        if st == 'hold':                                   # ★ 실제 인용차단 (Codex P1 §4)
            if verbose:
                print(f'  HOLD    {c["id"]}: {str(c.get("hold_reason", ""))[:66]}')
            continue
        if st in ('rejected', 'retired'):                  # C-7 과잉차단 해소: retired 도 면제
            if st == 'rejected' and not bad:
                errs.append(f'{c.get("id")}: rejected 인데 검사를 **통과했다** — 규칙이 이 '
                            f'역사적 실패를 못 잡는다 (연극이 됐다)')
            # ★ 2026-08-12 — **규칙 귀속**까지 검사한다.  "잡히긴 했다" 로는 부족하다:
            #   다른 이유로 잡히면 기대한 규칙은 여전히 이빨이 없는데 초록불이 뜬다
            #   (= 커버리지 구멍이 우연에 가려진다).  `expected_violations` 가 있으면
            #   실제로 발동한 코드가 그것을 **포함**해야 한다.
            exp = c.get('expected_violations')
            if st == 'rejected' and exp and bad:
                got = _codes(bad)
                miss = set(exp) - got
                if miss:
                    errs.append(f'{c["id"]}: 거부되긴 했으나 **기대한 규칙이 아니다** — '
                                f'기대 {sorted(exp)} · 실제 {sorted(got)}.  '
                                f'{sorted(miss)} 는 여전히 검증되지 않았다')
            if verbose and st == 'rejected' and bad:
                print(f'  거부됨  {c["id"]}: {_msg(bad[0]).split(": ", 1)[-1][:70]}')
            continue
        if c.get('evidence_state') not in _EVIDENCE_OK:
            errs.append(f'{c["id"]}: evidence_state={c.get("evidence_state")!r} 인데 status='
                        f'{st!r} 다 — 인용차단이 안 된다.  status 를 "hold" 로 내릴 것')
        n_live += 1
        errs.extend(_msg(x) for x in bad)
        if not bad and verbose:
            print(f'  OK      {c["id"]}: {str(c["claim"])[:68]}')
    if verbose:
        print(f'  ── claims {len(claims)}건 (채점 {n_live} · 면제 {len(claims) - n_live})')
    return errs, warns


# ═══════════════════════════════════════════════════════════════════════════
#: ★★★ 규칙 K (2026-08-25, Codex 흡수 리뷰 ⑩) — **규율 selftest 가 실제로 돌아야 한다.**
#
#   Codex: *"테스트 파일이 존재하고 수동 실행이 녹색인 것만으로는 자동 규율이 아니다."*
#   실사고: S1 봉인의 핵심 셋(`sr01_stamp_compare` = 팔 검사기 · `mpm_webapp_payload`
#   = PTFE 규약 · `step3_sigma` = 솔버 규약)이 `check_all.sh` 에도 CI yml 에도 **없었다**.
#   셋 다 1초 미만이라 비용 이유도 없었다 — 그냥 배선을 잊은 것이고, 잊었다는 사실을
#   알려 줄 것이 아무것도 없었다.  규칙 D 가 말하는 "발동한 적 없는 검사" 의 상위 판이다.
#
#   ⇒ 여기 적힌 것은 **두 곳 다** 에서 돌아야 한다.  한쪽에만 있으면 오류다 (드리프트 금지).
#   ⚠ 목록에 더할 때는 실제로 두 파일에 배선하고 나서 더할 것 — 이 목록만 늘리면
#     규칙 K 자신이 "선언만 있고 실행이 없는" 그것이 된다.
K_REQUIRED_SELFTESTS = (
    ('scripts/run_contract.py', '--selftest'),
    ('scripts/check_review_findings.py', '--selftest'),
    ('scripts/check_method_discipline.py', '--selftest'),
    ('scripts/sdcp_gain_verdict.py', '--selftest'),
    ('scripts/sdcp_phase_ledger_match.py', '--selftest'),
    ('scripts/sr01_stamp_compare.py', '--selftest'),
    ('scripts/mpm_webapp_payload.py', '--selftest-temperature'),
    ('scripts/step3_sigma.py', '--selftest'),
)
K_CHECK_ALL = 'scripts/check_all.sh'
K_CI_YML = '.github/workflows/discipline.yml'


def _live_after(toks):
    """토큰열에서 **rc 가 보존되는** python 호출이 있는가 (R4-CX-06).

    거부하는 뒤꼬리: `|| true` · `|| :` · `|| echo …` · `; true` · `| tee …` · `&`.
    ⚠ 파이프는 마지막 명령의 rc 만 남기므로(`pipefail` 없이는) 규율 증거가 못 된다.
    """
    _SWALLOW_NEXT = ('true', ':', 'echo', 'printf', 'cat')
    for _j, _t in enumerate(toks):
        if _t == '||' and _j + 1 < len(toks) \
                and toks[_j + 1].rsplit('/', 1)[-1] in _SWALLOW_NEXT:
            return False
        if _t == ';' and _j + 1 < len(toks) and toks[_j + 1] in ('true', ':'):
            return False
        if _t == '|':
            return False                       # rc 가 파이프 끝 명령의 것이 된다
        if _t == '&':
            return False                       # 백그라운드 = 기다리지 않는다
    return True


def k_live_invocation(line, base, flag):
    """이 줄이 `base` 를 `flag` 로 **실제 실행**하는가 (주석·echo·인용문 배제).

    ★ 왜 (2026-08-25, Codex 재리뷰 조건 7): 규칙 K 의 초판은 한 줄에 스크립트 이름과
      플래그가 같이 있기만 하면 배선으로 셌다.  그래서 아래가 전부 통과했다 —
        `# python3 scripts/foo.py --selftest`      (주석 처리된 죽은 줄)
        `echo "python3 scripts/foo.py --selftest"` (안내문일 뿐 실행이 아니다)
        `run 'foo.py --selftest' python3 scripts/bar.py` (라벨만 맞고 대상이 다르다)
      = 규칙 K 자신이 false-green.  ⇒ **인터프리터 호출 형태**를 요구한다.

    받아들이는 형태: `python`/`python3` 토큰 **바로 뒤**에 `…/base` 가 오고, 그 뒤
    어딘가에 `flag` 가 있다.  그 앞에 `echo`/`printf` 가 있으면 실행이 아니다.
    ⚠ 정적 검사의 한계는 남는다 (`if false; then … fi` 안은 못 본다) — 그래서
      `check_all.sh` 자신이 **실행**으로 다시 본다.  두 층은 서로를 대신하지 않는다.
    """
    st = line.strip()
    if not st or st.startswith('#'):
        return False
    #  주석 꼬리 제거 (YAML/셸 공통) — 따옴표 안의 `#` 은 흔치 않아 단순 규칙으로 충분하다
    if ' #' in st and st.count('"') % 2 == 0 and st.count("'") % 2 == 0:
        st = st.split(' #', 1)[0]
    toks = st.replace('"', ' ').replace("'", ' ').split()
    #  ★★★ 2026-08-25 (R3-CX-08, Codex 3차) — **죽은 가지와 실패 삼킴도 배선이 아니다.**
    #    Codex 실측: `false && python … --selftest` 와 `python … --selftest || true` 가
    #    live 로 세어졌다.  앞은 **절대 안 돌고**, 뒤는 **실패해도 초록**이라 둘 다
    #    "규율이 돈다" 의 증거가 못 된다 (규칙 K 의 존재 이유가 정확히 그것이다).
    #  ★★★ 2026-08-25 (R4-CX-06, Codex 4차) — 앞판이 여섯 형태를 더 통과시켰다:
    #    `true || python …` (안 돈다) · `python … || echo x` (실패 삼킴) ·
    #    `python … ; true` (종료코드 덮기) · `python … | tee f` (파이프가 rc 를 가린다) ·
    #    `exit 0; python …` (도달 불가) · `python … &` (기다리지 않는다).
    #    ⇒ **제어흐름을 본다** — 앞에 죽은 가드가 있는가 · 뒤에 rc 를 덮는 것이 오는가.
    _DEADG = ('false', ':', 'true', 'exit')
    for _j, _t in enumerate(toks[:-1]):
        if _t in _DEADG and toks[_j + 1] in ('&&', '||', ';'):
            #  `false &&` / `true ||` / `: ;` / `exit 0;` = 뒤가 안 돌거나 조건부다
            if not (_t == 'true' and toks[_j + 1] == '&&') \
                    and not (_t == 'false' and toks[_j + 1] == '||'):
                return False
        #  `exit …` 이 python 호출보다 **앞에** 있으면 그 뒤는 도달 불가.
        #  ⚠ 토큰 분해에서 `exit 0;` 은 `['exit','0;']` 이 될 수 있어 `;` 를 따로 안 센다.
        if _t == 'exit':
            return False
    if not _live_after(toks):
        return False
    for _i, _t in enumerate(toks[:-1]):
        if _t.rsplit('/', 1)[-1] not in ('python', 'python3'):
            continue
        if any(_p.rsplit('/', 1)[-1] in ('echo', 'printf') for _p in toks[:_i]):
            continue                       # 안내문 안의 명령어 — 실행이 아니다
        _tgt = toks[_i + 1]
        if _tgt.rsplit('/', 1)[-1] != base:
            continue
        if flag in toks[_i + 2:]:
            return True
    return False


import ast as _ast                          # 규칙 K 가 소스를 훑는다
import collections as _collections          # 규칙 M 회계 집계
import subprocess as _sp                    # 규칙 J·L 이 실물을 **실행**한다
import tempfile as _tf

#: 규칙 L — 러너 통합.  ★ 이름은 파일 안에서만 쓰인다 (프로덕션 러너 경로).
L_RUNNER = 'scripts/sdcp_gain_vox015_8arm.sh'
#: `RUNNER_CONFIG_END` 위쪽 = 순수 변수 조립.  아래는 mkdir·venv·게이트 (실행 금지).
L_MARKER = 'RUNNER_CONFIG_END'


def runner_config(env, runner=None):
    """러너의 **설정 조립부를 실제로 실행**해 조립된 변수를 돌려준다.

    ★★★ 왜 (2026-08-25, Codex 재리뷰 조건 7): 러너의 배선(`LEAN_FLAGS` · `EP_FLAG` ·
      `--require-arms` 상수 8)이 **한 번도 실행으로 확인된 적이 없었다** — grep 뿐이었다.
      grep 은 주석·죽은 줄을 배선으로 세고(규칙 K 가 방금 그 부류였다), 셸의 조건 전개
      (`[ "${LEAN:-0}" = "2" ] && …`)는 정적으로 못 읽는다.
      ⇒ `RUNNER_CONFIG_END` 위쪽만 잘라 서브셸에서 **돌리고** 결과를 읽는다.
    ⚠ 아래쪽(mkdir·venv·GPU 솔브)은 자르므로 부작용이 없다.  표지가 사라지면 **거부**한다
      (fail-closed — 잘못 자르면 진짜 러너를 돌려 버린다).
    """
    _p = os.path.join(ROOT, runner or L_RUNNER)
    with open(_p, encoding='utf-8') as f:
        src = f.read()
    if L_MARKER not in src:
        raise RuntimeError(f'{L_MARKER} 표지가 러너에 없다 — 어디까지가 설정인지 알 수 없다')
    head = src[:src.index(L_MARKER)].rsplit('\n', 1)[0]
    _keys = ('LEAN_FLAGS', 'PREREG_ARMS', 'ARMS', 'OUTDIR', 'FIBRE_STAMP')
    #  ⚠ `${V-…}` 는 **콜론 없이** — `${V:-…}` 는 빈 문자열도 미설정으로 읽어
    #    "기본에서 LEAN_FLAGS 가 비었는가" 를 물을 수 없게 만든다 (초판이 그랬다).
    probe = head + '\n' + '\n'.join(
        'printf "%s=%s\\n" ' + k + ' "${' + k + '-<UNSET>}"' for k in _keys)
    _env = dict(os.environ, **{k: str(v) for k, v in env.items()})
    _env.setdefault('MPM_NO_VENV', '1')
    r = _sp.run(['bash', '-s'], input=probe, capture_output=True, text=True,
                timeout=60, env=_env, cwd=_tf.gettempdir())
    if r.returncode != 0:
        #  ★ 2026-08-25 (R4-CX-08) — 설정부가 **의도적으로 abort** 할 수 있다 (실경로 충돌·
        #    ARMS 범위·P2_EXTRA 금지).  그것은 검사 대상의 **정상 거동**이므로 예외가
        #    아니라 결과로 돌려준다.  호출부가 "abort 도 격리의 증거" 로 읽는다.
        return {'_aborted': str(r.returncode),
                '_msg': ((r.stdout or '') + (r.stderr or ''))[-400:]}
    out = {}
    for ln in (r.stdout or '').splitlines():
        if '=' in ln:
            k, v = ln.split('=', 1)
            if k in _keys:
                out[k] = v
    return out


def runner_extra_flags(env, runner=None):
    """러너의 `--extra-flags "…"` 문자열을 **셸에 실제로 전개**시켜 돌려준다.

    ★ 왜 (조건 7): 이 한 문자열이 payload 에 가는 물리 인자 전부다.  `$EP_FLAG` 를
      조립해 놓고 **문자열에 넣는 것을 잊는** 부류는 grep 으로 안 잡힌다 (변수는 있고
      쓰이지 않았을 뿐이다).  ⇒ 러너에서 그 리터럴과 `EP_FLAG` 조립 줄을 떼어
      같은 셸에서 전개한다.  전개 결과 = payload 가 실제로 받을 인자열.
    ⚠ 다른 변수는 표지값으로 채운다 (이 검사의 대상이 아니다).  `local` 은 함수 밖에서
      문법 오류라 떼어낸다.
    """
    _p = os.path.join(ROOT, runner or L_RUNNER)
    with open(_p, encoding='utf-8') as f:
        lines = f.read().splitlines()
    _ep = [ln.strip().replace('local ', '', 1) for ln in lines
           if 'EP_FLAG=' in ln and not ln.strip().startswith('#')]
    if not _ep:
        raise RuntimeError('EP_FLAG 조립 줄을 러너에서 못 찾았다')
    _xf = [ln for ln in lines if '--extra-flags "' in ln and not ln.strip().startswith('#')]
    if len(_xf) != 1:
        raise RuntimeError(f'`--extra-flags` 리터럴이 {len(_xf)}개다 (1개를 기대)')
    _lit = _xf[0].split('--extra-flags "', 1)[1].rsplit('"', 1)[0]
    #  `--expect-physics` 조립 줄도 같이 떼어 온다 (조건 4 — 러너 자기 설정 선언)
    _xp = [ln.strip().replace('local ', '', 1) for ln in lines
           if ('XP=' in ln or 'XP_FLAG=' in ln) and not ln.strip().startswith('#')]
    _seed = ['SIGMA=SIG', 'VOX=0.15', 'BRIDGE_UM=0.48', 'SH=SHIFT', 'FIBRE_STAMP=segment',
             'SD_FLAG=', 'YV_FLAG=', 'PT_FLAG=', 'PS_FLAG=', 'FS_FLAG=',
             'LEAN_FLAGS=', 'P2_EXTRA=', 'XP_FLAG=']
    probe = '\n'.join(['set -u', *_seed, *_ep, *_xp,
                        'printf "%s\\n" "' + _lit + '"'])
    _env = dict(os.environ, **{k: str(v) for k, v in env.items()})
    _env.pop('EXPECT_PROTOCOL', None)
    _env.update({k: str(v) for k, v in env.items()})
    r = _sp.run(['bash', '-s'], input=probe, capture_output=True, text=True,
                timeout=60, env=_env, cwd=_tf.gettempdir())
    if r.returncode != 0:
        raise RuntimeError(f'전개가 exit {r.returncode} — {(r.stderr or "")[-300:]}')
    return (r.stdout or '').strip()


def check_runner_integration(verbose=True, runner=None):
    """→ (문제 목록, 경고).  규칙 L — 러너의 배선이 **실행으로** 확인되는가."""
    problems, warns = [], []
    _p = os.path.join(ROOT, runner or L_RUNNER)
    if not os.path.exists(_p):
        return [f'L_MISSING| 러너가 없다 ({_p})'], warns
    _bn = _sp.run(['bash', '-n', _p], capture_output=True, text=True, timeout=60)
    if _bn.returncode != 0:
        return [f'L_SYNTAX| 러너가 문법 오류다 — {(_bn.stderr or "").strip()[-200:]}'], warns
    try:
        _std = runner_config({}, runner)
        _l2 = runner_config({'LEAN': '2'}, runner)
        _ep = runner_config({'EXPECT_PROTOCOL': 'p1-deadbeefdeadbeef'}, runner)
    except Exception as e:                                  # noqa: BLE001
        return [f'L_PROBE| 러너 설정 조립부를 실행할 수 없다 ({type(e).__name__}: {e}) — '
                f'확인 못 한 것을 통과시키지 않는다'], warns
    #  ⓐ LEAN=2 = σ_e 전용.  이 일곱이 러너 문서(§LEAN)가 선언한 집합이다.
    _need = ('--no-step4', '--no-thermal', '--no-trackb', '--no-field',
             '--no-ion', '--no-pore', '--no-collector')
    _miss = [f for f in _need if f not in _l2.get('LEAN_FLAGS', '')]
    if _miss:
        problems.append(f'L_LEAN2| LEAN=2 가 {_miss} 를 켜지 않는다 (조립 결과 '
                        f'`{_l2.get("LEAN_FLAGS")}`) — σ_e 전용 규약이 선언과 다르다')
    if _std.get('LEAN_FLAGS', '<UNSET>').strip():
        problems.append(f'L_LEANDEFAULT| LEAN 미지정인데 LEAN_FLAGS 가 비어 있지 않다 '
                        f'(`{_std.get("LEAN_FLAGS")}`) — 기본이 조용히 LEAN 이 된다')
    #  ⓑ EXPECT_PROTOCOL 통과 — 요청↔적용 봉인의 **유일한** 배선점이다 (CDXR3-3).
    #    `EP_FLAG` 은 함수 안 `local` 이라 설정 프리픽스에 없다 ⇒ 러너에서 그 조립 줄과
    #    `--extra-flags` 문자열을 **그대로 떼어 셸에 전개**시킨다 (진짜 확장이라
    #    "$EP_FLAG 를 문자열에 넣는 것을 잊었다" 도 잡힌다 — grep 으로는 못 잡는다).
    try:
        _on = runner_extra_flags({'EXPECT_PROTOCOL': 'p1-deadbeefdeadbeef'}, runner)
        _off = runner_extra_flags({}, runner)
    except Exception as e:                                  # noqa: BLE001
        problems.append(f'L_EXTRA| `--extra-flags` 전개를 실행할 수 없다 '
                        f'({type(e).__name__}: {e}) — 확인 못 한 것을 통과시키지 않는다')
        _on = _off = ''
    if '--expect-protocol p1-deadbeefdeadbeef' not in _on:
        problems.append(f'L_EXPECT| EXPECT_PROTOCOL 이 payload 인자로 안 들어간다 '
                        f'(전개 결과 `{_on[:200]}`) — 규약 봉인이 끊긴다')
    if '--expect-protocol' in _off:
        problems.append(f'L_EXPECTDEFAULT| EXPECT_PROTOCOL 없이도 `--expect-protocol` 이 '
                        f'붙는다 (`{_off[:200]}`)')
    #  ⓑ′ ★★ **러너 자기 설정 선언** (조건 4).  첫 팔의 id 를 베끼는 것과 다르다 —
    #     그것은 첫 팔이 진리가 되므로, 첫 팔이 조용히 틀리면 나머지가 그것에 일치해
    #     전부 통과한다.  러너가 자기가 넘긴 축을 선언하고 payload 가 적용값과 맞춘다.
    _xp_need = ('vox_um=0.15', 'bridge_um=0.48', 'sigma_vgcf_S_cm=SIG',
                'fibre_stamp=segment', 'sdcp_stamp=point', 'sdcp_yield_to_vgcf=False')
    if '--expect-physics' not in _off:
        problems.append(f'L_EXPECTPHYS| 러너가 `--expect-physics` 를 넘기지 않는다 '
                        f'(`{_off[:200]}`) — 기대값을 자기 설정에서 만들지 않으면 '
                        f'첫 팔이 진리가 된다 (조건 4)')
    else:
        _decl = _off.split('--expect-physics ', 1)[1].split(' ')[0]
        _xmiss = [f for f in _xp_need if f not in _decl]
        if _xmiss:
            problems.append(f'L_EXPECTPHYS_AXIS| 러너 선언에 {_xmiss} 가 없다 '
                            f'(선언 `{_decl}`) — 러너가 넘긴 축인데 대조되지 않는다')
    #  ⓒ 사전등록 팔 수는 **상수**여야 한다.  ARMS 로 자기가 자기한테 요구하면 봉인이 아니다.
    if _std.get('PREREG_ARMS') != '8':
        problems.append(f'L_PREREG_ARMS| PREREG_ARMS = {_std.get("PREREG_ARMS")!r} (기대 8) — '
                        f'사전등록 팔 수가 상수가 아니면 최종 봉인이 뜻을 잃는다')
    _a2 = runner_config({'ARMS': '2'}, runner)
    if _a2.get('_aborted'):
        #  ★ R4-CX-08 — 진단 런을 **아예 거부**한 것은 더 강한 격리다 (통과).
        _a2 = dict(_a2, OUTDIR='<aborted>')
    if _a2.get('PREREG_ARMS') != '8':
        problems.append(f'L_PREREG_DRIFT| ARMS=2 에서 PREREG_ARMS 가 '
                        f'{_a2.get("PREREG_ARMS")!r} 로 따라 움직인다 — 자기가 자기한테 '
                        f'요구하는 봉인은 봉인이 아니다')
    #  ⓓ 진단 런은 **다른 디렉터리**로 가야 한다 (사전등록 팔과 섞이면 안 된다).
    if _a2.get('OUTDIR') == _std.get('OUTDIR'):
        problems.append(f'L_ARMTAG| ARMS=2 진단 런이 사전등록과 **같은 OUTDIR** 로 간다 '
                        f'({_std.get("OUTDIR")}) — 2팔과 8팔 산출물이 섞인다')
    #  ⓔ ★★ **봉인이 원값보다 먼저 나와야 한다** (Codex 재리뷰 조건 1).
    #    옛 러너는 `--collect-only` 로 16 팔 σ_e 표를 찍은 **뒤** 봉인을 걸었다 —
    #    운영자가 결과를 다 보고 봉인 통과 여부를 고를 수 있으면 눈먼 봉인이 아니다.
    #    ⚠ 여기서는 **순서**만 본다 (실행은 GPU 팔이 있어야 한다).  주석 줄은 뺀다 —
    #      규칙 K 가 방금 그 부류로 false-green 이었다.
    with open(_p, encoding='utf-8') as f:
        _rl = [ln for ln in f.read().splitlines() if not ln.strip().startswith('#')]
    #  ★★★ 2026-08-25 (R3-CX-08, Codex 3차) — **live 호출만 센다.**  옛 판은 주석만
    #    걸러 `echo "… --seal-only"` 안내문도 순서 증거가 됐다.  `k_live_invocation` 을
    #    재사용해 인터프리터 호출 형태만 인정한다 (규칙 K 와 **같은 판정기**).
    def _live(ln, flag):
        return k_live_invocation(ln, 'sdcp_gain_verdict.py', flag)
    _seal_i = next((i for i, ln in enumerate(_rl) if _live(ln, '--seal-only')), None)
    _coll = [i for i, ln in enumerate(_rl) if _live(ln, '--collect-only')]
    if _seal_i is None:
        problems.append('L_NOSEAL| 러너가 `--seal-only` 를 부르지 않는다 — 계약 봉인이 없다')
    else:
        _early = [i for i in _coll if i < _seal_i]
        if _early:
            problems.append(
                f'L_SEALORDER| `--collect-only` 가 봉인보다 **먼저** 나온다 '
                f'(줄 {[i + 1 for i in _early]} vs 봉인 {_seal_i + 1}) — 원값 표를 보고 '
                f'봉인을 통과시킬지 고를 수 있으면 눈먼 봉인이 아니다 (조건 1)')
    #  ⓕ ★★ 2026-08-25 (R3-CX-04) — 생산 봉인이 **digest 를 요구**하는가, 그리고
    #     `P2_EXTRA` 가 규약 인자를 **거부**하는가 (주의 문구는 게이트가 아니다).
    if '--require-digest' not in '\n'.join(_rl):
        problems.append('L_NODIGEST| 최종 봉인이 `--require-digest` 를 넘기지 않는다 — '
                        '같은 침대·재현 가능한 코드라는 증거 없이 통과한다 (R3-CX-04)')
    _pb = _sp.run(['bash', '-c',
                   #  ⚠ 범위는 **표지까지**다 — 고정 줄수로 자르면 러너가 길어질 때
                   #    검사가 조용히 대상 밖으로 나간다 (실제로 그렇게 무력해졌다).
                   f'set -e; sed -n "1,/{L_MARKER}/p" {_p!r} > "$0"; '
                   f'P2_EXTRA="--periodic" bash "$0"',
                   os.path.join(_tf.gettempdir(), 'l_p2extra_probe.sh')],
                  capture_output=True, text=True, timeout=120)
    if 'P2_EXTRA' not in (_pb.stdout or '') + (_pb.stderr or ''):
        problems.append('L_P2EXTRA| `P2_EXTRA="--periodic"` 가 **거부되지 않는다** — '
                        'P2_EXTRA 는 조립 문자열 맨 뒤라 러너의 `--expect-physics` 선언을 '
                        '덮는다.  주의 주석은 게이트가 아니다 (R3-CX-04)')
    #  ⓖ ★★ 2026-08-25 (R3-CX-02/09) — 봉인 실패 시 **원값을 자동으로 안 찍는가**,
    #     진단 런이 **생산 이름공간을 못 쓰는가**.
    _seal_i2 = next((i for i, ln in enumerate(_rl) if '--seal-only' in ln), None)
    #  ⚠ **실패 블록만** 본다.  진단 런(ARMS≠8) 분기의 `--collect-only` 는 정당하다
    #    (그 분기는 "판정하지 말 것" 이라고 스스로 선언한다) — 거기까지 잡으면 과잉차단이다.
    if _seal_i2 is not None:
        _end = next((i for i in range(_seal_i2, min(_seal_i2 + 30, len(_rl)))
                     if _rl[i].strip() == 'exit 1'), _seal_i2)
        _after = _rl[_seal_i2:_end + 1]
        _auto = [ln for ln in _after if _live(ln, '--collect-only')]
        if _auto:
            problems.append(f'L_FAILDUMP| 봉인 실패 경로가 `--collect-only` 를 **자동 실행**한다 '
                            f'({_auto[0].strip()[:70]}) — metadata 를 일부러 깨뜨려 봉인을 '
                            f'실패시키고 raw table 을 보는 경로가 열린다 (R3-CX-02)')
    _a9 = runner_config({'ARMS': '2', 'OUTDIR': '/tmp/prod_dir'}, runner)
    if _a9.get('_aborted'):
        _a9 = dict(_a9, OUTDIR='/tmp/prod_dir_arm2')   # abort = 격리 성립
    if not str(_a9.get('OUTDIR', '')).endswith('_arm2'):
        problems.append(f'L_ARMNS| `ARMS=2 OUTDIR=<생산경로>` 가 그대로 쓰인다 '
                        f'({_a9.get("OUTDIR")}) — 진단 산출물이 생산 이름공간에 섞인다 '
                        f'(R3-CX-09)')
    if verbose and not problems:
        print(f'  ✓ 규칙 L — 러너 배선을 실행으로 확인 (LEAN=2 {len(_need)}플래그 · '
              f'EXPECT_PROTOCOL 통과 · PREREG_ARMS 상수 8 · 진단 런 분리 · '
              f'봉인이 원값보다 먼저)')
    return problems, warns


#: 규칙 M 이 **실제 파서**를 잡을 때 쓰는 조각.  `parse_args` 를 가로채 그 시점의
#  파서를 통째로 들고 나온다 — 그때는 helper 모듈이 등록한 옵션까지 전부 붙어 있다.
_M_PROBE = r'''
import argparse, importlib, json, sys
class _Got(Exception):
    def __init__(self, ap): self.ap = ap
def _hook(self, *a, **k): raise _Got(self)
argparse.ArgumentParser.parse_args = _hook
argparse.ArgumentParser.parse_known_args = _hook
sys.argv = [sys.argv[0]]
m = importlib.import_module(%r)
try:
    m.main()
except _Got as g:
    print(json.dumps(sorted({s for act in g.ap._actions
                             for s in act.option_strings if s.startswith('--')})))
    raise SystemExit(0)
raise SystemExit('NO_PARSE_ARGS')
'''


def _payload_options(payload):
    """→ (옵션 목록, 오류|None).  **파서를 실행해서** 잡는다.

    ★★ 2026-08-25 (A1 2차) — 초판은 payload 파일을 AST 로 훑었다.  그런데
      `--temp-c`·`--ea-ion-ev` 는 `se_material.temperature_argparse(ap)` 가 **다른
      모듈**에서 등록해 AST 에 안 보였고, 초판은 그것을 "회계에 있으나 파서에 없다"
      (M_STALE) 로 **거꾸로** 보고했다.  ⇒ 정적 훑기를 버리고 실물을 잡는다."""
    _mod = os.path.splitext(os.path.basename(payload))[0]
    _out = _sp.run([sys.executable, '-c', _M_PROBE % _mod],
                          cwd=os.path.dirname(payload), capture_output=True,
                          text=True, timeout=180)
    if _out.returncode != 0:
        return [], (f'M_INTROSPECT| 파서를 못 잡았다 (rc={_out.returncode}) '
                    f'{(_out.stderr or "").strip().splitlines()[-1:] or ""}')
    try:
        return json.loads(_out.stdout.strip().splitlines()[-1]), None
    except Exception as e:                                  # noqa: BLE001
        return [], f'M_INTROSPECT| 파서 목록을 못 읽었다 ({e})'


def check_cli_accounting(verbose=True, payload=None):
    """→ (문제 목록, 경고).  규칙 M — **CLI 가 전부 회계에 있는가**.

    ★★★ 2026-08-25 (A1, Codex R4-CX-03 잔여): 허용/금지 목록을 손으로 유지하면 새 옵션이
      조용히 밖에 남는다.  실제로 `--sigma-superp` 가 전자 σ 표에 들어가는데
      `PROTOCOL_FIELDS` 에 없었고, 전수 대조로 `--sigma-swcnt`·`--swcnt-ion-block` 이
      같이 나왔다.  ⇒ **파서를 훑어** 미등재를 오류로 낸다.
    ⚠ 등재는 "회계 범주를 밝힌다" 는 뜻이지 "규약 축이다" 가 아니다 —
      `mode`/`numeric` 도 유효한 답이고, 다만 **답을 적어야** 한다.
    ★★ 2026-08-25 (A1 2차) — 초판의 초록은 **가짜 보증**이었다.  ⓐ payload 파일만 AST 로
      훑어 helper 모듈이 등록한 `--temp-c`·`--ea-ion-ev` 를 못 봤고, ⓑ 이름 조각으로
      "물리 후보" 를 걸러 `--dilate-z`(침대 z 늘림)·`--k-carbon`·`--i0-a-m2` 를 후보에서
      제외했다.  ⇒ **부분집합 필터를 전부 버린다** — 실물 파서의 전 옵션이 등재를 요구한다.
      그 결과 `--dilate-z`·`--se-proxy`(+`--se-frac`/`--n-vox`) 가 규약 축 없이 σ 침대를
      바꾸고 있었다는 것이 드러나 `dilate_z`·`se_source` 를 신설했다.
    """
    problems, warns = [], []
    _p = payload or os.path.join(ROOT, 'scripts', 'mpm_webapp_payload.py')
    if not os.path.exists(_p):
        return [f'M_MISSING| payload 가 없다 ({_p})'], warns
    try:
        if os.path.join(ROOT, 'scripts') not in sys.path:
            sys.path.insert(0, os.path.join(ROOT, 'scripts'))
        import run_contract as _rc_m
    except Exception as e:                              # noqa: BLE001
        return [f'M_IMPORT| run_contract 를 못 읽는다 ({e})'], warns
    _opts, _err = _payload_options(_p)
    if _err:
        return [_err], warns
    problems += cli_accounting_problems(_opts, _rc_m.CLI_ACCOUNTING,
                                        _rc_m.PROTOCOL_FIELDS, _rc_m.PROTOCOL_CODE_CONST,
                                        _rc_m.CLI_CATEGORIES)
    if verbose and not problems:
        _n = _collections.Counter(c for c, _f in _rc_m.CLI_ACCOUNTING.values())
        print(f'  ✓ 규칙 M — 실물 파서 CLI {len(_opts) - 1}개가 전부 회계에 있다 ('
              + ' · '.join(f'{k} {_n[k]}' for k in _rc_m.CLI_CATEGORIES if _n[k])
              + f' · 규약 축 {len(_rc_m.PROTOCOL_FIELDS)} 전수 도달)')
    return problems, warns


def cli_accounting_problems(_opts, _acct, _protocol_fields, _code_const, _categories):
    """→ 문제 목록.  규칙 M 의 **순수 부분** — 잡은 옵션 목록과 회계를 대조한다.

    ★ 분리한 이유: 음성 대조를 돌리려면 "새 옵션이 하나 생겼다" 를 모방해야 하는데,
      그것을 위해 리포의 payload 를 건드릴 수는 없다.  준비 단계(파서 포획)와
      판정 단계를 나누면 판정을 합성 입력으로 직접 물을 수 있다."""
    problems = []
    #  ① 파서에 있는데 회계에 없다 = 규약 밖에서 물리가 바뀔 수 있다
    _un = sorted(o for o in _opts if o != '--help' and o not in _acct)
    if _un:
        problems.append(
            f'M_UNACCOUNTED| CLI {len(_un)}개가 `CLI_ACCOUNTING` 에 없다 {_un[:8]} — '
            f'각각 {"/".join(_categories)} 중 무엇인지 적을 것.  '
            f'적지 않으면 규약 밖에서 물리가 바뀐다 (R4-CX-03: `--sigma-superp`)')
    #  ② 회계에 있는데 파서에 없다 = 낡은 등재 (이름이 바뀌었거나 옵션이 사라졌다)
    _stale = sorted(set(_acct) - set(_opts))
    if _stale:
        problems.append(f'M_STALE| 회계에 있으나 파서에 없는 옵션 {_stale[:8]} — '
                        f'이름이 바뀌었거나 옵션이 사라졌다')
    #  ③ 범주 어휘 오타
    _badcat = sorted(o for o, (c, _f) in _acct.items() if c not in _categories)
    if _badcat:
        problems.append(f'M_BADCAT| 모르는 회계 범주 {_badcat[:8]} — 허용: {_categories}')
    #  ④ `protocol`/`derived` 로 적은 것은 **정말** 규약 축을 가리켜야 한다
    #     ⚠ heuristic 을 쓰지 않는다 — 회계가 **필드명을 직접** 적는다 (이름 규칙 추측 금지).
    _PF = set(_protocol_fields)
    _bad_p = sorted(o for o, (c, flds) in _acct.items()
                    if c in ('protocol', 'derived')
                    and (not flds or any(f not in _PF for f in flds)))
    if _bad_p:
        problems.append(f'M_NOTINPROTOCOL| `protocol`/`derived` 로 적었는데 그 필드가 '
                        f'`PROTOCOL_FIELDS` 에 없다(또는 비었다) {_bad_p} — 선언과 거동이 갈렸다')
    #  ⑤ 반대 방향 — 규약 축인데 **어떤 CLI 도** 그것을 못 가리키면 죽은 축이거나 회계 누락
    _covered = {f for c, flds in _acct.values()
                if c in ('protocol', 'derived') and flds for f in flds}
    _orphan = sorted(f for f in _PF if f not in _covered
                     and f not in _code_const)
    if _orphan:
        problems.append(f'M_ORPHAN_FIELD| CLI 로 못 바꾸는 규약 축 {_orphan} — '
                        f'코드 상수면 `PROTOCOL_CODE_CONST` 에, 아니면 회계에 적을 것')
    return problems


def check_selftest_wiring(verbose=True, check_all=None, ci_yml=None):
    """→ (문제 목록, 경고).  규칙 K — 규율 selftest 가 두 곳 다에 배선됐는가.

    ★ 문자열 포함으로 본다 (실행하지 않는다) — 실행은 `check_all.sh` 자신이 한다.
      여기서 보는 것은 **호출이 존재하는가** 이고, 그것이 이 규칙의 전부다."""
    problems, warns = [], []
    _ca_p = check_all or os.path.join(ROOT, K_CHECK_ALL)
    _ci_p = ci_yml or os.path.join(ROOT, K_CI_YML)
    for _lbl, _p in (('check_all', _ca_p), ('CI yml', _ci_p)):
        if not os.path.exists(_p):
            problems.append(f'K_MISSING_FILE| {_lbl} 이 없다 ({_p}) — 규율이 어디서 도는지 '
                            f'확인할 수 없다')
    if problems:
        return problems, warns
    with open(_ca_p, encoding='utf-8') as f:
        ca = f.read()
    with open(_ci_p, encoding='utf-8') as f:
        ci = f.read()
    for _script, _flag in K_REQUIRED_SELFTESTS:
        _base = os.path.basename(_script)
        for _lbl, _txt in (('check_all.sh', ca), (K_CI_YML, ci)):
            #  ★★★ 2026-08-25 (Codex 재리뷰 조건 7) — **살아 있는 호출만** 센다.
            #    초판은 `_base in ln and _flag in ln` 이라 주석 처리된 줄과
            #    `echo "… --selftest"` 안내문이 배선으로 통과했다 = 규칙 K 자신이
            #    false-green 이었다 (규칙 J 가 `--help` 만 보다 놓친 것과 같은 부류).
            _hit = any(k_live_invocation(ln, _base, _flag) for ln in _txt.splitlines())
            if not _hit:
                problems.append(
                    f'K_UNWIRED| `{_base} {_flag}` 가 **{_lbl} 에서 안 돈다** — '
                    f'수동으로 녹색인 것은 자동 규율이 아니다 (Codex ⑩).  배선하거나 '
                    f'K_REQUIRED_SELFTESTS 에서 빼고 이유를 적을 것')
    if verbose and not problems:
        print(f'  ✓ 규칙 K — 규율 selftest {len(K_REQUIRED_SELFTESTS)}개가 '
              f'check_all·CI 양쪽에 배선돼 있다')
    return problems, warns


def check_argparse_help(verbose=True):
    """규칙 H — `--help` 가 살아 있어야 한다.

    ★ 실사고 2026-08-18: `mpm_webapp_payload.py --help` 가 **완전히 죽어 있었다**
    (`ValueError: unsupported format character ')'`).  argparse 는 help 문자열에
    `% params` 를 적용하므로 홑 `%` 하나가 **모든** 옵션 문서를 못 쓰게 만든다.
    우리 help 는 "왜 이 플래그가 있나" 를 담는 1차 문서라 이것이 죽으면 규약이 사라진다.
    조용한 실패라 아무도 몰랐다 — 그래서 검사로 만든다.

    검사는 **정적**이다 (모듈을 import 하지 않는다): AST 로 add_argument 의 help 를 꺼내
    `% params` 를 흉내 낸다.  `%%` · `%(default)s` 는 정상이다.
    """
    errs, warns = [], []
    root = os.path.join(ROOT, 'scripts')
    probe = {'default': 0, 'prog': 'x', 'type': 'x', 'choices': 'x',
             'const': 'x', 'metavar': 'x', 'dest': 'x'}
    n = 0
    for fname in _shadow_scan_files():
        try:
            tree = ast.parse(open(os.path.join(root, fname), encoding='utf-8').read())
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and node.func.attr == 'add_argument'):
                continue
            opt = next((a.value for a in node.args
                        if isinstance(a, ast.Constant) and isinstance(a.value, str)
                        and a.value.startswith('-')), '?')
            for kw in node.keywords:
                if kw.arg != 'help':
                    continue
                try:
                    h = ast.literal_eval(kw.value)
                except Exception:                      # noqa: BLE001 — f-string 등은 검사 밖
                    continue
                n += 1
                try:
                    h % probe
                except Exception as ex:                # noqa: BLE001
                    errs.append(f'{fname}:{node.lineno} `{opt}` help 가 argparse 를 깨뜨린다 '
                                f'({ex}) — 홑 `%` 를 `%%` 로.  **이 파일의 --help 가 통째로 죽는다**')
    if verbose:
        print(f'  {"OK" if not errs else "✗"}      argparse help {n}건 — `% params` 통과 '
              f'({len(errs)} 오류)')
    return errs, warns


#: 규칙 I — 본체 ↔ 폴백 사본이 어긋나면 안 된다.
#:   (모듈경로, 심볼)  ↔  (사본파일, 그 안의 리터럴 이름)
#:   ⚠ 등록부가 좁으면 규칙이 조용히 반만 산다 — 2026-08-20 감사에서 `_KNOWN` 한 쌍만
#:   등록돼 있고 같은 폴백 블록의 `_NONADD` 는 빠져 있었다 (fable F5 · 코드 감사 δ).
#:   `_DENS` 는 **의도적으로 제외**한다: 폴백 사본은 `additives.DENS` 의 3키 부분집합이라
#:   리터럴 동일성으로 볼 대상이 아니다 (`mpm_input_from_case.py` 주석이 그렇게 명시).
_COPY_PARITY = (
    ('scripts/additives.py', 'KNOWN_ADDITIVES',
     'scripts/mpm_input_from_case.py', '_KNOWN'),
    ('scripts/additives.py', '_RECIPE_NON_ADDITIVE',
     'scripts/mpm_input_from_case.py', '_NONADD'),
)


def check_copy_parity(verbose=True):
    """규칙 I — "verbatim 사본" 은 실제로 verbatim 이어야 한다.

    ★ 실사고 2026-08-19: `mpm_input_from_case.py` 의 ImportError 폴백에 있는
    `_awt` 가 스스로 *"= additives.additive_wt verbatim"* 이라 적어 놓고 **SWCNT 를
    빠뜨리고 있었다** (A14 로 SWCNT 를 추가할 때 본체만 고쳤다).  그 경로로 도는 런은
    SWCNT 를 조용히 드랍했다 — 규칙 F 가 잡는 "조용한 강등" 과 같은 부류인데,
    F 는 import 그림자만 보므로 이 형태는 통과했다.

    ⚠ 이 검사는 **이름 목록의 일치**만 본다.  로직이 갈라지는 것은 못 잡는다 —
    사본을 두는 것 자체가 부채라는 사실은 변하지 않는다.
    """
    import ast as _ast
    errs, warns = [], []
    for src_f, src_name, cp_f, cp_name in _COPY_PARITY:
        vals = {}
        for f, n in ((src_f, src_name), (cp_f, cp_name)):
            p = os.path.join(ROOT, f)
            try:
                tree = _ast.parse(open(p, encoding='utf-8').read())
            except (OSError, SyntaxError) as exc:
                errs.append(f'I_COPY_UNREADABLE| {f} 를 못 읽는다 ({exc})')
                vals[n] = None
                continue
            got = None
            for node in _ast.walk(tree):
                if isinstance(node, _ast.Assign) and any(
                        isinstance(t, _ast.Name) and t.id == n for t in node.targets):
                    try:
                        got = tuple(_ast.literal_eval(node.value))
                    except (ValueError, SyntaxError):
                        got = None
            vals[n] = got
            if got is None:
                errs.append(f'I_COPY_MISSING| {f} 에서 `{n}` 리터럴을 못 찾았다 — '
                            f'이름이 바뀌었으면 _COPY_PARITY 를 갱신할 것')
        a, b = vals.get(src_name), vals.get(cp_name)
        if a is not None and b is not None:
            if a != b:
                errs.append(f'I_COPY_DRIFT| **사본 표류** — {src_f}:{src_name} = {list(a)} 인데 '
                            f'{cp_f}:{cp_name} = {list(b)}.  폴백 경로로 돈 런은 '
                            f'{sorted(set(a) ^ set(b))} 를 조용히 다르게 처리한다')
            elif verbose:
                print(f'  ✓ {src_name} ↔ {cp_name} 일치 ({len(a)}개)')
    return errs, warns


# ─────────────────────────────────────────────────────────────────────────────────
# 규칙 J — 생산 엔트리포인트 **최소-픽스처 스모크** (2026-08-20)
#
# 왜: 규칙 H 는 `--help` 가 사는지(파서)만 본다.  이 부류의 사고 3건은 전부 **기본 경로**
#   에서 났다 —
#     ① `_kind_all` 조건부 바인딩 → `--fibre` 없는 모든 킷에서 STEP3 통째로 사망 (08-12~20)
#     ② `float(a.temp_c)` → `--temp-c` 기본 None 에서 2,474 s GPU 솔브 뒤 TypeError
#     ③ `60bd849e` → `--fibre` 로드 실패를 except 가 삼켜 선분 스탬프가 **조용히** 점으로
#   셋 다 "옵션 입력이 붙은/빠진 조합"이고, 셋 다 **정적 검사로는 안 보인다**
#   (`check_undefined_names.py`(pyflakes) 가 ① 을 통과시킴을 실측 확인).
#   ⇒ 유일하게 증명 가능한 방법은 **실제로 돌려 보는 것**이다.
#
# 비용: 픽스처가 63구 × n_vox 48 × step3_vox 1.5 라 팔당 ~4 s (실측).  두 팔 ~8 s.
# 단언: exit 0 **이 아니라** — 그것이 바로 ① 이 통과한 이유다 —
#   `mpm_metrics.step3.manifest.components` 의 모든 항목이 `complete`/`disabled` 이고
#   `_step3` 가 `failed` 가 아닐 것.  로그의 `STEP3 skipped` 도 실패로 본다.
_SMOKE_VOX, _SMOKE_NVOX = '1.0', '64'


def _smoke_fixture(d):
    """→ (am_csv, se_npy, phase_npy, fid_npy, dia_npy).  numpy 없으면 (am_csv, None…)."""
    import itertools
    am = os.path.join(d, 'am.csv')
    rows = ['# type,x,y,z,r  (규칙 J 스모크 픽스처 — 관통하는 AM 기둥)']
    for ix, iy in itertools.product(range(3), range(3)):
        for k in range(7):
            rows.append('2,%.6f,%.6f,%.6f,%.6f'
                        % (0.018 + 0.007 * ix, 0.018 + 0.007 * iy, 0.004 + 0.0055 * k, 0.0040))
    with open(am, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rows) + '\n')
    try:
        import numpy as _np
    except Exception:                                          # noqa: BLE001
        return am, None, None, None, None
    #  SE 점구름 + 상 + 섬유 id — `--fibre` 팔용.  길이가 서로 **정확히** 같아야 한다
    #  (그 길이 검사 자체가 ① 의 쌍둥이 결함이 있던 자리다).
    g = _np.linspace(0.012, 0.046, 9)
    z = _np.linspace(0.0045, 0.040, 9)
    pts = _np.array([[x, y, zz] for x in g for y in g for zz in z], _np.float64)
    ph = _np.ones(len(pts), _np.int32)                          # 1 = SE
    ph[::7] = 2                                                 # 2 = VGCF (전도 첨가제)
    fid = _np.full(len(pts), -1, _np.int32)
    fid[ph == 2] = _np.arange(int((ph == 2).sum())) // 4         # 4점씩 한 섬유
    dia = _np.ones(len(pts), _np.float64)
    se_p, ph_p = os.path.join(d, 'se.npy'), os.path.join(d, 'phase.npy')
    fid_p, dia_p = os.path.join(d, 'fibre.npy'), os.path.join(d, 'fibre_dia.npy')
    _np.save(se_p, pts); _np.save(ph_p, ph); _np.save(fid_p, fid); _np.save(dia_p, dia)
    return am, se_p, ph_p, fid_p, dia_p


def smoke_assert_payload(out, label, errs, warns, expect=None):
    """규칙 J 의 **사후 단언**만 떼어낸 것 — 가짜 payload 로 음성 대조를 걸 수 있게.

    ★ 2026-08-20 (Codex CDX-IJ-05): 이 단언들이 실제로 무는지 증명하려면 계산 없이
      status 만 적은 producer 를 먹여 봐야 한다.  `check_entrypoint_smoke` 안에 인라인으로
      두면 그 실험을 할 수 없어 밖으로 뺐다.  `errs`/`warns` 에 append 하고 bad 여부를 돌려준다.
    """
    import json as _json
    try:
        with open(out, encoding='utf-8') as f:
            s3 = ((_json.load(f).get('mpm_metrics') or {}).get('step3') or {})
    except Exception as e:                              # noqa: BLE001
        errs.append(f'J_PAYLOAD| {label}: payload 를 읽을 수 없다 ({e})')
        return None
    comps = ((s3.get('manifest') or {}).get('components') or {})
    if not comps:
        errs.append(f'J_NO_MANIFEST| {label}: STEP3 manifest components 가 비었다 — '
                    f'"돌았다" 를 증명할 수 없다')
        return None
    #  ★★ 2026-08-20 (Codex CDX-IJ-05) — status 문자열만 보면 **계산 없는 자가보고**가
    #    통과한다 (독립 fake producer 가 `electronic=complete` 한 줄만 적고 통과했고,
    #    전부 `disabled` 로 적어도 통과했다).  ⇒ ⓐ 팔별 **기대 상태 맵**을 고정하고
    #    ⓑ 실제 **수치**(σ_e 유한·양수, dof>0)를 본다.
    #  ★ 2026-08-25 (M-R3-03) — 기대 상태는 **팔마다 다르다**.  러너의 LEAN=2 는
    #    thermal 도 끄므로 그 팔에서 `thermal: complete` 를 요구하면 정상 생산 경로를
    #    거짓 실패시킨다.  ⇒ 호출부가 팔의 플래그에 맞는 기대를 넘긴다 (기본은 옛 값).
    _EXPECT = expect or {'electronic': 'complete', 'thermal': 'complete',
                         'ionic': 'disabled', 'pore': 'disabled', 'pnm': 'disabled'}
    bad = {k: (v or {}).get('status') for k, v in comps.items()
           if (v or {}).get('status') not in ('complete', 'disabled')}
    _wrong = {k: (comps.get(k) or {}).get('status')
              for k, want in _EXPECT.items()
              if (comps.get(k) or {}).get('status') != want}
    if bad or _wrong:
        errs.append(f'J_COMPONENT| {label}: 기대 상태와 다르다 — 미완료 {bad} · '
                    f'기대 불일치 {_wrong} (기대 {_EXPECT})')
    #  ★★ 2026-08-20 (Codex 재검증 IJ-05) — 값의 **존재**만 보면 여전히 통과한다:
    #    Codex 가 `sigma_e=1 · n_dof=1 · 기대 상태 전부` 로 통과시켰다.
    #    ⇒ **계산이 실제로 일어났다는 증거**를 요구한다 — CG 수렴 기록과, complete 로 선언한
    #      component 의 **산출물**(thermal 이면 k_eff).  픽스처는 결정론적이라 문턱이 안 흔들린다.
    _se = s3.get('sigma_e_eff_S_cm')
    _nd = s3.get('n_dof')
    _ci, _cr = s3.get('cg_info'), s3.get('cg_resid')
    _num = []
    if not (isinstance(_se, (int, float)) and _se == _se and 0 < float(_se) < 1e9):
        _num.append(f'sigma_e_eff_S_cm={_se!r}')
    if not (isinstance(_nd, int) and _nd > 1000):
        _num.append(f'n_dof={_nd!r} (픽스처 dof 는 1000 을 넘는다)')
    if _ci != 0 or not (isinstance(_cr, (int, float)) and 0 < float(_cr) < 1e-6):
        _num.append(f'CG 증거 없음/미수렴 cg_info={_ci!r} cg_resid={_cr!r}')
    if (comps.get('thermal') or {}).get('status') == 'complete':
        _k = (s3.get('thermal') or {}).get('k_eff_W_mK')
        if not (isinstance(_k, (int, float)) and _k == _k and float(_k) > 0):
            _num.append(f'thermal=complete 인데 k_eff_W_mK={_k!r}')
    if _num:
        errs.append(f'J_NUMBERS| {label}: **status 는 complete 인데 수치가 없다** '
                    f'{_num} — 자가보고만으로 통과하면 안 된다 (CDX-IJ-05)')
    #  ★ 2026-08-20 — 판정기의 **고정-인자 기록**이 기본 경로에서 실제로 채워지는가.
    #    두 사고가 여기서 났다: `backend` 를 없는 키로 읽어 항상 None(→ 게이트 무발화,
    #    오늘 고친 뒤엔 거짓 HOLD) · `bridge_um` 이 기본 실행에서 None(→ 거짓 HOLD).
    #    둘 다 **매니페스트를 눈으로 안 봤기 때문**에 생겼다 — 스모크가 대신 본다.
    #    ★ 키 위치를 여기서 **다시 적지 않는다** — 그것이 두 사고의 원인이었다.
    #      판정기 자신의 리더(`sdcp_gain_verdict._read`)를 불러 **그것이 보는 값**을 본다.
    try:
        if os.path.join(ROOT, 'scripts') not in sys.path:
            sys.path.insert(0, os.path.join(ROOT, 'scripts'))
        import sdcp_gain_verdict as _sgv
        _rec = _sgv._read(out)
        _blank = [k for k in ('vox', 'bridge_um', 'fibre_stamp', 'sdcp_stamp',
                              'sigma_vgcf_S_cm', 'sigma_sdcp_S_cm', 'backend',
                              'sdcp_sphere_d_um', 'sdcp_yield_to_vgcf',
                              'sigma_ptfe_S_cm')
                  if _rec.get(k) is None]
        if _blank:
            errs.append(f'J_MANIFEST| {label}: **판정기의 리더가** 고정 인자를 '
                        f'기본 경로에서 못 읽는다 {_blank} — 그 게이트는 무발화이거나 '
                        f'거짓 HOLD 를 낸다 (2026-08-20 실사고 2건이 정확히 이것)')
    except Exception as _e:                            # noqa: BLE001
        #  ⚠ 2026-08-20 (Codex 재검증 IJ-05) — 옛 판은 warning 이라 **exit 0** 이었다.
        #    판정기 리더가 터지는 것은 "확인 못 했다" 이고 그것을 성공으로 세면 fail-open 이다.
        errs.append(f'J_READER| {label}: 판정기 리더가 payload 를 읽다 죽었다 '
                    f'({type(_e).__name__}: {_e}) — 확인 못 한 것을 통과시키지 않는다')
    #  ★★★ 2026-08-25 (자체발견) — **물리 규약 id 가 실제로 확정되는가.**
    #    `PROTOCOL_FIELDS` 에 이름은 있는데 producer 가 그 키를 **안 쓰면**
    #    `physics_protocol_id` 는 조용히 `unknown:<빠진 필드>` 로 내려앉는다.  그 값은
    #    모든 팔에서 **같은 상수**라 팔간 일치 게이트가 초록이고, 규약이 실제로 갈려도
    #    못 잡는다 = 가짜 보증.  실제로 `vox_um` 이 그 상태였다 (오늘 발견·수정).
    #    ⇒ 여기서 **접두사**를 본다.  `unknown:` 뒤에 빠진 필드 이름이 그대로 실려 있으므로
    #      이 한 줄이 "규약 필드를 새로 넣고 producer 에 안 쓴" 부류를 전부 잡는다.
    #    ⚠ 필드 목록을 여기 **다시 적지 않는다** — 그것이 backend/bridge_um 두 사고의 원인이다.
    #  ⚠ 접두사를 **여기 적지 않는다** — 스키마를 올릴 때마다 이 줄이 낡는다 (실제로
    #    `p1-` 하드코딩이 `p2` 승격에서 규칙 J 를 빨갛게 만들었다).
    #  ★ 그리고 접두사만 보지 않는다 — `run_contract.protocol_ok` 로 **재계산 대조**까지
    #    한다 (저장값이 raw manifest 와 다른 stale/손으로 쓴 값을 producer 단계에서 잡는다).
    try:
        if os.path.join(ROOT, 'scripts') not in sys.path:
            sys.path.insert(0, os.path.join(ROOT, 'scripts'))
        import run_contract as _rc_j
        _ok_j, _why_j = _rc_j.protocol_ok(s3.get('manifest') or {})
        if not _ok_j:
            errs.append(f'J_PROTOCOL| {label}: 규약 기록이 계약을 만족하지 않는다 — '
                        f'{_why_j}.  producer 가 축을 다 싣지 않았거나 저장값이 raw '
                        f'manifest 와 다르다 (R3-CX-03; 2026-08-25 vox_um 실사고)')
    except Exception as _e_j:                          # noqa: BLE001
        errs.append(f'J_PROTOCOL_ERR| {label}: 규약 대조가 죽었다 '
                    f'({type(_e_j).__name__}: {_e_j}) — 확인 못 한 것을 통과시키지 않는다')
    return (bad, comps)


def check_entrypoint_smoke(verbose=True, timeout=900, payload=None):
    errs, warns = [], []
    import json as _json
    import subprocess as _sp
    import tempfile as _tf
    pay = payload or os.path.join(ROOT, 'scripts', 'mpm_webapp_payload.py')
    if not os.path.exists(pay):
        return ['J_NO_ENTRYPOINT| mpm_webapp_payload.py 가 없다'], warns
    with _tf.TemporaryDirectory() as d:
        am, se_p, ph_p, fid_p, dia_p = _smoke_fixture(d)
        #  ⚠⚠ 2026-08-20 (kgy 실사고) — 두 팔 모두 **`--se` 실 점구름**을 쓴다.
        #    옛 판은 plain 팔에 `--se-proxy` 를 썼는데 그 경로가 `viz_mpm_morphology_3d` 를
        #    import 하고 그것이 **matplotlib** 을 끌어온다.  kgy 의 dem-venv 에 matplotlib 이
        #    없어 규칙 J 가 실패했고, 러너의 규율 게이트가 그것을 보고 **GPU 런을 전부 막았다**.
        #    ⇒ 그 실패는 **생산 경로의 결함이 아니다** — 생산은 `--se se_dump.npy` 라 그 import
        #      를 타지 않는다.  픽스처가 생산이 안 가는 길로 갔던 것이 문제다 (오늘의 주제).
        #    ⇒ 두 팔의 차이를 **`--fibre` 축 하나로** 좁힌다 (그것이 FA-01 이 난 축이다).
        if not se_p:
            return (['J_NO_NUMPY| numpy 가 없어 스모크 픽스처를 만들 수 없다 — '
                     '확인 못 한 것을 통과시키지 않는다 (fail-closed)'], warns)
        #  ★ 2026-08-25 (R3-CX-04) — `collector_geom` 도 **명시**한다.  성공 경로가
        #    도장을 안 찍고 있었는데 기대 맵에 없어서 안 보였다 (계획은 True 인데
        #    component 는 아예 없는 상태 = "껐다" 와 "죽었다" 를 구분 못 함).
        _EXP_STD = {'electronic': 'complete', 'thermal': 'complete',
                    'collector_geom': 'complete',
                    'ionic': 'disabled', 'pore': 'disabled', 'pnm': 'disabled'}
        _EXP_LEAN = {'electronic': 'complete', 'thermal': 'disabled',
                     'collector_geom': 'disabled',
                     'ionic': 'disabled', 'pore': 'disabled', 'pnm': 'disabled'}
        arms = [('plain  (--fibre 없음 = 첨가제 없는 킷)',
                 ['--scaffold', am, '--se', se_p], _EXP_STD),
                ('fibre  (--phase/--fibre 있음 = 첨가제 킷)',
                 ['--scaffold', am, '--se', se_p, '--phase', ph_p,
                  '--fibre', fid_p, '--fibre-dia', dia_p], _EXP_STD),
                #  ★★★ 2026-08-25 (M-R3-03, Codex 재리뷰) — **LEAN 생산 경로**를 태운다.
                #    옛 스모크는 `--no-ion --no-pore` 만 써서 러너가 실제로 쓰는
                #    `--no-thermal --no-trackb --no-field --no-collector` 를 **한 번도
                #    안 태웠다**.  그래서 내가 넣은 required 게이트가 thermal 을 missing 으로
                #    세어 **LEAN=1/2 스윕 팔 전부를 exit 3** 으로 죽이는데도 J-1 이 초록이었다.
                #    ⇒ 러너의 LEAN=2 플래그 집합을 그대로 넣는다.  이 팔이 이 부류의 유일한
                #      실물 증인이다 (손수 만든 manifest 픽스처는 producer 를 증명하지 못한다).
                ('lean2  (러너 LEAN=2 = σ_e 전용 생산 경로)',
                 ['--scaffold', am, '--se', se_p, '--phase', ph_p,
                  '--fibre', fid_p, '--fibre-dia', dia_p,
                  '--no-thermal', '--no-trackb', '--no-field', '--no-collector',
                  '--no-step4'], _EXP_LEAN)]
        for label, extra, _exp in arms:
            out = os.path.join(d, 'p_%d.json' % len(errs))
            cmd = [sys.executable, pay, *extra, '--n-vox', _SMOKE_NVOX,
                   '--step3-vox', _SMOKE_VOX, '--no-ion', '--no-pore', '--out', out]
            try:
                r = _sp.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=d)
            except Exception as e:                              # noqa: BLE001
                errs.append(f'J_RUN| {label}: 실행 자체가 실패 ({type(e).__name__}: {e})')
                continue
            log = (r.stdout or '') + (r.stderr or '')
            if r.returncode != 0:
                errs.append(f'J_EXIT| {label}: exit {r.returncode} — {log.strip()[-200:]}')
                continue
            if 'STEP3 skipped' in log:
                _ln = [x for x in log.split('\n') if 'STEP3 skipped' in x]
                errs.append(f'J_SKIPPED| {label}: **STEP3 가 조용히 죽었다** (exit 0 인데) — '
                            f'{_ln[0].strip()}')
                continue
            _res = smoke_assert_payload(out, label, errs, warns, expect=_exp)
            if _res is None:
                continue
            bad, comps = _res
            if verbose and not bad:
                _st = ', '.join('%s=%s' % (k, (v or {}).get('status'))
                                for k, v in comps.items())
                print(f'  ✓ {label} — {_st}')
        #  ★★★ 2026-08-25 (R3-CX-01, Codex 3차) — **producer → check_arm → move 통합.**
        #    `check_arm` 의 `_STEP3_PATHS` 가 `metrics` 오타라 **모든 실제 팔을 거부**했다
        #    (러너의 cache·fresh 두 경로가 이것을 부른다 = 생산 전면 차단).  selftest 는
        #    75/75 초록이었다 — 내 fixture 가 실제 producer 가 아니라 **틀린 자리**에
        #    쓰고 있었기 때문이다.  픽스처가 버그를 인코딩하면 selftest 는 그 버그를 지킨다.
        #    ⇒ 이 부류의 유일한 증인은 **실제 producer 산출물을 CLI 에 그대로 먹이는 것**.
        #      손으로 만든 payload 는 producer 를 증명하지 못한다.
        _arm = os.path.join(d, 'p_0.json')          # 위 plain 팔이 실제로 만든 것
        if os.path.exists(_arm):
            _chk = os.path.join(ROOT, 'scripts', 'sr01_stamp_compare.py')
            _cr = _sp.run([sys.executable, _chk, '--check-arm', _arm, '--stamp', 'point'],
                          capture_output=True, text=True, timeout=300, cwd=d)
            if _cr.returncode != 0:
                errs.append(f'J_ARMCHK| **실제 producer 산출물을 `check_arm` 이 거부한다** '
                            f'(exit {_cr.returncode}: '
                            f'{((_cr.stdout or "") + (_cr.stderr or "")).strip()[-160:]}) — '
                            f'러너의 cache·fresh 두 경로가 이것을 부르므로 생산이 전면 차단된다 '
                            f'(R3-CX-01)')
            elif verbose:
                print('  ✓ producer → check_arm — 실제 산출물을 그대로 받아들인다')
            #  ★ 판별력 자기증명 — 스탬프를 **틀리게** 주면 거부해야 한다 (관대해서 통과가
            #    아니라 정말 읽고 있다는 증거).
            _cw = _sp.run([sys.executable, _chk, '--check-arm', _arm, '--stamp', 'segment'],
                          capture_output=True, text=True, timeout=300, cwd=d)
            if _cw.returncode == 0:
                errs.append('J_ARMCHK_BLIND| `check_arm` 이 **틀린 스탬프**(segment vs 실제 '
                            'point)도 통과시킨다 — 자리를 못 찾아 조용히 넘어가는 것과 '
                            '구분되지 않는다')
        else:
            errs.append('J_ARMCHK_NOFILE| plain 팔 산출물이 없어 통합 회귀를 돌리지 못했다 — '
                        '확인 못 한 것을 통과시키지 않는다')

        #  ★★★ 2026-08-25 (R3-CX-02, Codex 3차) — **producer 가 기본에서 값을 가리는가.**
        #    러너는 팔마다 producer stdout 을 그대로 보여 준다.  최종 봉인을 앞으로 옮긴
        #    것만으로는 부족했다 — 운영자는 **팔이 끝날 때마다** σ_e·σ_ion 을 이미 봤다.
        #    ⇒ 기본 실행의 stdout 에 σ 값이 **없어야** 하고, `--show-results` 로는 나와야
        #      한다 (가리기만 하고 못 여는 것도 결함이다 — 디버깅이 막힌다).
        _blind_out = os.path.join(d, 'blind.json')
        _bc = [sys.executable, pay, '--scaffold', am, '--se', se_p,
               '--n-vox', _SMOKE_NVOX, '--step3-vox', _SMOKE_VOX,
               '--no-ion', '--no-pore', '--out', _blind_out]
        try:
            _rb = _sp.run(_bc, capture_output=True, text=True, timeout=timeout, cwd=d)
            _rs = _sp.run(_bc[:-2] + ['--show-results', '--out', _blind_out + '.s'],
                          capture_output=True, text=True, timeout=timeout, cwd=d)
        except Exception as e:                              # noqa: BLE001
            errs.append(f'J_BLINDRUN| 봉인 팔 실행 실패 ({type(e).__name__}: {e})')
        else:
            #  ★★★ 2026-08-25 (R4-CX-01, Codex 4차) — **값을 payload 에서 뽑아 stdout 을
            #    훑는다.**  옛 판은 `σ_e_eff` 한 줄만 봤다.  그래서 `ideal_R0`(= σ_e 와
            #    **대수적으로 같은 수**)가 `bulk 0.00105` 로 그대로 새고 있었다 —
            #    **이름을 바꾼 것은 가린 것이 아니다** (Codex 실측).
            #    ⇒ payload 의 결과-보유 값들을 유효숫자 3자리로 만들어 stdout 에서 찾는다.
            #      새 출력이 생겨도 자동으로 걸린다 (손으로 목록을 유지하지 않는다).
            def _leaks(_log, _path):
                import json as _jl
                try:
                    _pp = _jl.load(open(_path, encoding='utf-8'))
                except Exception:                           # noqa: BLE001
                    return ['(payload 를 못 읽었다)']
                _s3 = ((_pp.get('mpm_metrics') or {}).get('step3') or {})
                _vals = {}

                def _walk(o, path=''):
                    if isinstance(o, dict):
                        for _k, _v in o.items():
                            _walk(_v, f'{path}.{_k}' if path else _k)
                    elif isinstance(o, (int, float)) and not isinstance(o, bool):
                        #  σ·κ·저항·면적 = 결과.  개수·좌표·크기는 진단이라 뺀다.
                        if any(_t in path for _t in
                               ('sigma', 'k_eff', 'R_geom', 'tau', 'area', 'eps_')) \
                                and abs(o) > 0:
                            _vals[path] = float(o)
                for _k in ('sigma_e_eff_S_cm', 'sigma_ion_eff_S_cm', 'collector',
                           'collector_geometric', 'thermal', 'pore', 'track_b',
                           'carbon_se_area_um2'):
                    if _k in _s3:
                        _walk(_s3[_k], _k)
                _hit = []
                for _k, _v in _vals.items():
                    _f = f'{_v:.3g}'
                    if len(_f) >= 4 and _f in _log:          # 짧은 수는 우연 일치가 많다
                        _hit.append(f'{_k}={_f}')
                return _hit
            _blind_log = (_rb.stdout or '') + (_rb.stderr or '')
            _leaked = _leaks(_blind_log, _blind_out)
            if _leaked:
                errs.append(f'J_LEAK| 봉인 실행의 stdout 에 **결과값이 드러난다** '
                            f'({len(_leaked)}건: {_leaked[:4]}) — 이름이 달라도 같은 수면 '
                            f'가린 것이 아니다 (R4-CX-01: `ideal_R0` = σ_e)')
            _lb = [x for x in _blind_log.split('\n') if 'σ_e_eff' in x]
            _ls = [x for x in ((_rs.stdout or '') + (_rs.stderr or '')).split('\n')
                   if 'σ_e_eff' in x]
            if not _lb or '봉인' not in _lb[0]:
                errs.append(f'J_NOTBLIND| 기본 실행이 σ_e 값을 stdout 에 **찍는다** '
                            f'({(_lb or ["(줄 없음)"])[0].strip()[:90]}) — 러너가 팔마다 '
                            f'이것을 보여 주므로 운영자가 봉인 전에 결과를 본다 (R3-CX-02)')
            if not _ls or '봉인' in _ls[0]:
                errs.append(f'J_NOTOPENABLE| `--show-results` 로도 값이 안 나온다 '
                            f'({(_ls or ["(줄 없음)"])[0].strip()[:90]}) — 가리기만 하고 '
                            f'못 여는 것도 결함이다 (디버깅이 막힌다)')
            elif verbose:
                print('  ✓ producer 봉인 — 기본은 값을 가리고 `--show-results` 로 열린다')

        #  ★★★ 2026-08-25 (Codex 재리뷰 조건 7) — **실패 경로도 실물로 태운다.**
        #    여태 규칙 J 는 성공 팔만 돌렸다.  그래서 `_payload_reject_reason` 이
        #    ⓐ 정확히 어떤 코드로 끝나는지 ⓑ 최종 파일명을 정말 안 쓰는지 ⓒ 진단본을
        #    남기는지가 **한 번도 실행으로 확인되지 않았다** (R3-F2 는 손으로만 봤다).
        #    ⚠ exit 코드는 **정확히** 본다 — nonzero 만 보면 3↔4 가 뒤바뀌어도 통과한다.
        _fail_arms = [
            ('exit3  (required electronic 미완 — 도체 σ=0)', 3, 'STEP3_REQUIRED_INCOMPLETE',
             ['--sigma-am-s', '0', '--sigma-am-p', '0']),
            ('exit4  (물리 규약 불일치)', 4, 'PROTOCOL_MISMATCH',
             ['--expect-protocol', 'DELIBERATELY_WRONG']),
        ]
        for label, want_rc, want_code, extra in _fail_arms:
            out = os.path.join(d, 'f_%d.json' % want_rc)
            cmd = [sys.executable, pay, '--scaffold', am, '--se', se_p,
                   '--n-vox', _SMOKE_NVOX, '--step3-vox', _SMOKE_VOX,
                   '--no-ion', '--no-pore', *extra, '--out', out]
            try:
                r = _sp.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=d)
            except Exception as e:                          # noqa: BLE001
                errs.append(f'J_FAILRUN| {label}: 실행 자체가 실패 ({type(e).__name__}: {e})')
                continue
            log = (r.stdout or '') + (r.stderr or '')
            if r.returncode != want_rc:
                errs.append(f'J_EXITCODE| {label}: exit {r.returncode} — **정확히 '
                            f'{want_rc}** 여야 한다 (러너가 코드로 갈라 처리한다).  '
                            f'{log.strip()[-160:]}')
            if want_code not in log:
                errs.append(f'J_FAILCODE| {label}: 인과 코드 `{want_code}` 가 로그에 없다 — '
                            f'사유가 문자열 매칭에 의존하면 러너가 원인을 못 가른다')
            if os.path.exists(out):
                errs.append(f'J_PUBLISHED| {label}: **최종 파일명이 만들어졌다** ({out}) — '
                            f'실패 payload 가 러너의 `[ -s "$OUT" ]` 캐시를 오염시킨다 (R3-F2)')
            if not os.path.exists(out + '.failed'):
                errs.append(f'J_NODIAG| {label}: 진단본 `<out>.failed` 가 없다 — '
                            f'실패를 조사할 산출물이 사라졌다')
            if os.path.exists(out + '.part'):
                errs.append(f'J_STRAYPART| {label}: `.part` 임시 파일이 남았다')
            if verbose:
                print(f'  ✓ {label} — exit {r.returncode} · out 없음 · .failed 있음')
    return errs, warns


#: 규칙 J 의 **음성 대조** — 이 한 줄(2026-08-20 hoist)을 지우면 ① 이 그대로 재현된다.
#: 사본에서만 지우고 원본은 건드리지 않는다.  needle 이 안 맞으면 그것 자체가 실패다
#: (검사가 무엇을 지웠는지 모르는 채 통과하면 규칙 D 의 "발동한 적 없는 검사" 가 된다).
#  ★ 2026-08-24 (CDXR2-2) — hoist 가 **둘**이 됐다.  `_dia_all` 을 읽는 게이트
#    (`PTFE_STAMP_NEEDS_DIA`)도 `if a.fibre` 블록 밖에 있어 같은 부류의 결함이다.
#    ⇒ 니들을 두 줄로 넓혀 **어느 쪽을 지워도** 음성 대조가 발화하게 한다.
_J_NEEDLE = ("    _dia_all = None\n"
             "    _kind_all = None\n"
             "    if getattr(a, 'fibre', '') and phase is not None:")
_J_MUTANT = "    if getattr(a, 'fibre', '') and phase is not None:"


def smoke_negative_control(verbose=True):
    """→ (문제 목록, 경고).  규칙 J 가 **정말** ① 부류를 잡는지 돌연변이로 확인."""
    import shutil as _sh
    import tempfile as _tf
    src_dir = os.path.join(ROOT, 'scripts')
    pay = os.path.join(src_dir, 'mpm_webapp_payload.py')
    with open(pay, encoding='utf-8') as f:
        src = f.read()
    if _J_NEEDLE not in src:
        return (['J_NEG_STALE| 음성 대조의 needle(`_kind_all = None` hoist)이 소스에 없다 — '
                 '고침이 사라졌거나 코드가 바뀌었다.  둘 다 사람이 봐야 한다'], [])
    with _tf.TemporaryDirectory() as d:
        dst = os.path.join(d, 'scripts')
        _sh.copytree(src_dir, dst)
        with open(os.path.join(dst, 'mpm_webapp_payload.py'), 'w', encoding='utf-8') as f:
            f.write(src.replace(_J_NEEDLE, _J_MUTANT, 1))
        e, _ = check_entrypoint_smoke(verbose=False,
                                      payload=os.path.join(dst, 'mpm_webapp_payload.py'))
    #  ★★ 2026-08-25 (CDXR3-2) — **잡히는 코드가 둘이다.**  producer 가 required
    #    component 실패를 nonzero 로 전파하게 된 뒤로(fail-closed), 이 돌연변이는
    #    `J_SKIPPED`(조용히 건너뜀)가 아니라 `J_EXIT`(요란하게 죽음)로 잡힌다 —
    #    **더 강한 포착**이다.  둘 다 "돌연변이를 잡았다" 이므로 둘 다 인정하되,
    #    `plain` 팔이라는 것과 **둘 중 하나여야 한다**는 것은 그대로 고정한다
    #    (무엇이든 오류가 나면 통과, 로 느슨해지면 CDX-IJ-05 가 막으려던 그것이 된다).
    #  ★★★ 2026-08-25 (R3-CX-08, Codex 3차) — **"무엇이든 nonzero" 를 적발로 세지 않는다.**
    #    옛 판은 `J_EXIT` 이면 통과였다 ⇒ 무관한 SyntaxError exit 99 도 "잡았다" 가 된다
    #    (Codex 실측).  ⇒ 이 돌연변이가 재현하는 **그 실패**인지 확인한다:
    #      · `NameError`/`UnboundLocalError` 로 STEP3 가 죽는다 (①번 사고의 형태)
    #      · 또는 STEP3 가 조용히 건너뛰어진다 (`J_SKIPPED`)
    #    문법·import 오류는 **배터리 사고**이지 포착이 아니다.
    _NEEDLE = ('NameError', 'UnboundLocalError', 'not defined', 'STEP3')
    _HARNESS = ('SyntaxError', 'IndentationError', 'ModuleNotFoundError', 'ImportError')
    caught, harness = [], []
    for x in e:
        if 'plain' not in x:
            continue
        if any(h in x for h in _HARNESS):
            harness.append(x)
        elif x.startswith('J_SKIPPED') or (x.startswith('J_EXIT')
                                           and any(n in x for n in _NEEDLE)):
            caught.append(x)
    if harness:
        return ([f'J_NEG_HARNESS| ★ 음성 대조가 **배터리 사고**로 죽었다 '
                 f'({harness[0][:120]}) — 돌연변이가 재현한 실패가 아니다.  '
                 f'사본 만들기가 깨진 것이므로 "잡았다" 로 세지 않는다'], [])
    if not caught:
        return (['J_NEG_BLIND| ★ 규칙 J 가 돌연변이를 **못 잡았다** — hoist 를 '
                 f'지웠는데 plain 팔이 그 실패 형태로 죽지 않았다 (얻은 오류: '
                 f'{e or "없음"}).  검사가 무의미하거나 다른 이유로 죽은 것이다'], [])
    if verbose:
        print(f'  ✓ 음성 대조 — 돌연변이(plain 팔)를 잡았다: {caught[0][:110]}')
    return [], []


def run_all(verbose=True):
    errs, warns = [], []
    for title, fn in (('규칙 I — 본체 ↔ 폴백 사본 패리티', check_copy_parity),
                      ('규칙 A — 규약·격자·주기 패리티 (D4)', check_convention_parity),
                      ('규칙 B — 판별력 있는 rung (D2)', check_oblique_rungs),
                      ('규칙 C·D·E — 판별력 / 개수≠귀결 / 량 패리티 (D1)', check_claims_ledger),
                      ('규칙 H — argparse help 가 살아 있는가', check_argparse_help),
                      ('규칙 K — 규율 selftest 가 check_all·CI 에서 실제로 도는가',
                       check_selftest_wiring),
                      ('규칙 L — 러너 배선을 **실행으로** 확인 (LEAN·규약·팔 수)',
                       check_runner_integration),
                      ('규칙 M — CLI 회계 (실물 파서 전 옵션이 등재됐는가)',
                       check_cli_accounting),
                      ('규칙 J — 생산 엔트리포인트 스모크 (기본 경로가 정말 도는가)',
                       check_entrypoint_smoke),
                      ('규칙 F — 지역 import 그림자 (조용한 기능 꺼짐)', check_local_import_shadows)):
        if verbose:
            print(f'\n{title}')
        e, w = fn(verbose=verbose)
        errs += e
        warns += w
    return errs, warns


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
            print(f'  PASS  {name}')
        else:
            fail.append(name)
            print(f'  FAIL  {name}')

    from scipy import ndimage
    chk('A: 프로브가 6-face 를 거동으로 읽는다',
        probe_adjacency(lambda g: ndimage.label(g)) == '6-face')
    chk('A: 프로브가 26-conn 을 거동으로 읽는다',
        probe_adjacency(lambda g: ndimage.label(g, structure=np.ones((3, 3, 3), bool)))
        == '26-conn')
    chk('A: 프로브는 독스트링 경고에 흔들리지 않는다 (v1 오탐 해소)',
        probe_adjacency(lambda g: ndimage.label(g)) == '6-face')
    # ★★ 규칙 F — 지역 import 그림자.  실사고(2026-08-12): `mpm_webapp_payload` 가 모듈에서
    #    `import os as _os` 인데 main 안에 `import os` 가 있어 그 앞의 `os.path.exists` 가
    #    UnboundLocalError → 근처 `except Exception` 이 삼켜 **선분 스탬프가 조용히 꺼졌다**.
    #    아래 4건은 "검사가 **진짜 버그를 잡고 오탐은 안 내는가**" 를 묻는다.
    import tempfile as _tf
    _fx = os.path.join(_tf.mkdtemp(), 'fx.py')
    open(_fx, 'w').write(
        'import os as _os\n'
        'def main():\n'
        '    if _os.path.exists("x"):\n'
        '        print(os.path.exists("y"))     # ← import 보다 앞 = UnboundLocalError\n'
        '    import os\n'
        '    return os\n')
    _e, _c = find_local_import_shadows(_fx)
    chk('F: import 보다 앞에서 쓴 이름을 잡는다 (실사고 재현)',
        len(_e) == 1 and _e[0][1] == 'os')
    open(_fx, 'w').write(
        'def main():\n'
        '    _tb = {}\n'
        '    _tb["a"] = 1\n'
        '    try:\n'
        '        pass\n'
        '    except Exception:\n'
        '        import traceback as _tb\n'
        '    return _tb\n')
    _e, _c = find_local_import_shadows(_fx)
    chk('F: 앞에서 일반 대입된 이름은 **오탐하지 않는다** (첫 판이 12건 오탐했다)', len(_e) == 0)
    chk('F: 그래도 대입↔import 충돌은 경고로 남긴다', len(_c) == 1 and _c[0][1] == '_tb')
    open(_fx, 'w').write('def main():\n    import os\n    return os.getcwd()\n')
    chk('F: 정상 순서는 통과 (과잉차단 아님)', find_local_import_shadows(_fx) == ([], []))
    _ep, _ = find_local_import_shadows(os.path.join(ROOT, 'scripts', 'mpm_webapp_payload.py'))
    chk('F: 생산 파일이 현재 깨끗하다 (회귀 방지)', _ep == [])

    _save_d = dict(DIAGNOSTICS); DIAGNOSTICS.clear()
    e_a, _ = check_convention_parity(verbose=False)
    DIAGNOSTICS.update(_save_d)
    chk('A: 등록부를 비우면 오류 (v1 은 통과했다)', any('비우면' in x for x in e_a))

    # ★★ v3 — 선언된 adjacency 를 **검증**하는가.  v2 까지 probe_adjacency 는 selftest 에서만
    #    돌고 등록부에는 안 쓰였다 = 모든 `adjacency` 가 검증되지 않는 문자열이었다.
    #    아래 5개는 전부 "검증기가 **틀린 선언을 실제로 잡는가**" 를 묻는다 (가능도비 ≠ 1).
    chk('A3: 선언 6-face ↔ 거동 26-conn 이면 오류',
        verify_declared_adjacency('X', {'adjacency': '6-face',
                                        'label_fn': 'numpy.ndarray'})[0] is False)

    import types as _ty
    _m = _ty.ModuleType('_probe_mod')
    _m.__file__ = __file__
    sys.modules['_probe_mod'] = _m
    _m.good6 = lambda g: ndimage.label(g)
    _m.bad26 = lambda g: ndimage.label(g, structure=np.ones((3, 3, 3), bool))
    chk('A3: label_fn 이 26-conn 인데 6-face 로 선언 → 오류',
        verify_declared_adjacency('X', {'adjacency': '6-face',
                                        'label_fn': '_probe_mod.bad26'})[0] is False)
    chk('A3: label_fn 이 6-face 이고 선언도 6-face → 통과',
        verify_declared_adjacency('X', {'adjacency': '6-face',
                                        'label_fn': '_probe_mod.good6'})[0] is True)
    chk('A3: label_fn/label_site 가 아예 없으면 오류 (검증되지 않는 선언)',
        verify_declared_adjacency('X', {'adjacency': '6-face'})[0] is False)
    chk('A3: label_fn 이 안 불러와지면 fail-closed (warn 아님)',
        verify_declared_adjacency('X', {'adjacency': '6-face',
                                        'label_fn': 'no_such_mod.nope'})[0] is False)
    chk('A3: 프로브가 unknown 이면 fail-closed',
        verify_declared_adjacency('X', {'adjacency': '6-face',
                                        'label_fn': '_probe_mod.__class__'})[0] is False)
    # AST 경로 — 실제 리포 코드로 대조 (픽스처가 아니라 생산 함수)
    chk('A3: AST 가 econn 의 26-conn 을 읽는다',
        _ast_label_conns('mpm_webapp_payload', 'electronic_connectivity') == {'26-conn'})
    chk('A3: AST 가 STEP3 솔버의 6-face 를 읽는다',
        _ast_label_conns('step3_sigma', 'solve_sigma_z') == {'6-face'})
    chk('A3: AST 대조가 틀린 선언을 잡는다 (econn 을 6-face 로 선언)',
        verify_declared_adjacency('X', {
            'adjacency': '6-face',
            'label_site': ('mpm_webapp_payload', 'electronic_connectivity')})[0] is False)
    chk('A3: 없는 함수를 가리키면 fail-closed',
        verify_declared_adjacency('X', {'adjacency': '6-face',
                                        'label_site': ('step3_sigma', 'no_such_fn')})[0] is False)
    # 진단 자체가 안 불러와져도 fail-closed 여야 한다 (Codex #9)
    DIAGNOSTICS['zz_missing.nope'] = {'relation': 'diagnoses',
                                      'target': 'step3_sigma.solve_sigma_z',
                                      'adjacency': '6-face', 'vox_um': 0.4,
                                      'label_fn': '_probe_mod.good6'}
    e_a2, _ = check_convention_parity(verbose=False)
    DIAGNOSTICS.pop('zz_missing.nope')
    chk('A3: 진단이 import 안 되면 오류 (v2 는 SOLVERS 만 봤다)',
        any('불러올 수 없다' in x for x in e_a2))

    P = np.stack([np.linspace(0.3, 6.3, 60)] * 3, axis=1)
    chk('B: 동상 대각은 판별력 있다', assert_stamp_discriminating(P, 0.4, 'd'))
    S = _staggered_blind_fixture()
    try:
        assert_stamp_discriminating(S, 0.4, 's')
        chk('B: ★스태거 대각(k=2)을 거부 — v1 의 핵심 구멍', False)
    except AssertionError:
        chk('B: ★스태거 대각(k=2)을 거부 — v1 의 핵심 구멍', True)
    _save_r = dict(RUNGS); RUNGS.clear()
    e_b, _ = check_oblique_rungs(verbose=False)
    RUNGS.update(_save_r)
    chk('B: rung 을 비우면 오류 (v1 은 통과했다)', bool(e_b))
    def _boom():
        raise ImportError('x')
    RUNGS['tmp'] = _boom
    e_b2, _ = check_oblique_rungs(verbose=False)
    del RUNGS['tmp']
    chk('B: rung 실행 실패가 오류 (v1 은 warns 였다)', any('실행 불가' in x for x in e_b2))

    base = {'id': 'T', 'claim': 'c', 'asserted': 'VGCF 가 σ_e 에 기여한다', 'status': 'live',
            'measured': {'metric': 'dissipation_share', 'value': 0.04, 'unit': 'frac'},
            'h0': '스탬프가 끊었다', 'h1': '원래 작다',
            'h0_predicts': '분담 ≈ 4 %', 'h1_predicts': '분담 ≈ 4 %'}
    chk('C: 원본 CL-01 형태를 거부', any('가능도비 1' in x for x in check_claim(base)))
    for tag, v in (('공백', '분담 ≈ 4%'), ('마침표', '분담 ≈ 4 %.'), ('전각', '분담 ≈ 4 ％')):
        chk(f'C: ★표기만 바꾼 우회({tag})도 거부',
            any('가능도비 1' in x for x in check_claim(dict(base, h1_predicts=v))))
    chk('C: 0 vs 0.0 도 같은 예측으로 본다',
        any('가능도비 1' in x for x in check_claim(
            dict(base, h0_predicts='0', h1_predicts='0.0'))))
    chk('C: ★분해능 아래 차이를 거부 (E_SE 1.35≡1.5 형태)',
        any('분해능' in x for x in check_claim(dict(
            base, h0_predicts='overlap 1.75', h1_predicts='overlap 1.74', resolution=0.31))))
    chk('C: ★상보 부등호(< X vs >= X)는 판별적 — 과잉차단 안 함 (CL-10 때 발생)',
        check_claim(dict(base, h0_predicts='|Δ| < 4.0 %p', h1_predicts='|Δ| >= 4.0 %p',
                         resolution=1.0)) == [])
    chk('C: ★구간 겹침을 거부', any('구간이 겹친다' in x for x in check_claim(dict(
        base, h0_predicts='8.0 ~ 16.0', h1_predicts='9.0 ~ 15.6'))))
    # ★★ S0 C-5 — 같은 실패를 새 id·live 로 넣어도 물어야 한다
    reborn = dict(base, id='X-99', h1_predicts='분담이 4 % 수준', bridge='별도 측정함')
    chk('C·D: ★★같은 실패를 새 id·live 로 재발시켜도 거부 (v1 의 가장 위험한 구멍)',
        bool(check_claim(reborn)))
    chk('D: 세는 양 패턴이 se_se_cn·f_perc·plugged_frac 을 잡는다',
        all(_COUNT_RE.search(m) for m in ('se_se_cn', 'f_perc', 'plugged_frac',
                                          'n_components', 'percolation_pct')))
    chk('D: 귀결을 verdict 로 옮겨도 스캔된다',
        any('세는 양' in x for x in check_claim(dict(
            base, measured={'metric': 'n_components', 'value': 23914, 'unit': 'c'},
            asserted='성분 수가 크다', verdict='따라서 탄소가 단절됐다',
            h1_predicts='성분 수가 매우 크다'))))
    chk('D: bridge="." 같은 빈 다리는 인정 안 한다',
        any('bridge' in x for x in check_claim(dict(
            base, measured={'metric': 'n_components', 'value': 1, 'unit': 'c'},
            asserted='탄소가 단절됐다', bridge='.', h1_predicts='성분 수가 매우 크다'))))
    chk('D: ★검증-귀결 어휘는 shared_input 을 요구한다 (S4 흡수)',
        any('shared_input' in x for x in check_claim(dict(
            base, asserted='DEM 과 일치하므로 교차검증됐다', h1_predicts='다르다'))))
    chk('E: ★량 범주 오류를 거부 (K vs 영률)',
        any('량 범주' in x for x in check_claim(dict(
            base, h1_predicts='다르다', quantity='bulk_modulus',
            compared_to_quantity='youngs_modulus'))))
    chk('C-8: 규약 기록은 h0/h1 없이 provenance 로 통과 (과잉차단 해소)',
        check_claim({'id': 'V', 'claim': '생산 vox 는 0.4 µm', 'kind': 'convention',
                     'status': 'live', 'asserted': '기본값', 'provenance': 'step3_sigma.py:68',
                     'measured': {'metric': 'vox_um', 'value': 0.4, 'unit': 'µm'}}) == [])
    chk('D-6: parity_certified 는 합법적 bridge 다 (동어반복 요구 해소)',
        check_claim(dict(base, measured={'metric': 'n_components', 'value': 1, 'unit': 'c'},
                         asserted='탄소가 고립되지 않는다', h1_predicts='성분 수 = 1',
                         parity_certified='sr01_carbon_network.carbon_network_stats')) == [])
    # ── py3.8 호환 (2026-08-16 실사고: 원격 GPU 호스트가 3.8 이라 게이트가 막혔다) ──
    #   `ast.unparse` 는 3.9+ 다.  `_src_of` 의 대체 경로가 **같은 답**을 내야 한다.
    _n38 = ast.parse('f(np.ones((3, 3, 3), bool))').body[0].value.args[0]
    _s39 = _src_of(_n38)
    _u = ast.unparse if hasattr(ast, 'unparse') else None
    if _u is not None:
        del ast.unparse
    try:
        _s38 = _src_of(_n38)
    finally:
        if _u is not None:
            ast.unparse = _u
    chk(f'py38: unparse 없이도 같은 소스 복원 ({_s38!r})', _s38 == _s39 and '3, 3, 3' in _s38)
    chk('py38: 모르는 노드는 추측하지 않고 <Type> 로 남긴다 (fail-closed 유지)',
        _src_of(ast.parse('x[1:2]').body[0].value.slice).startswith('<')
        or hasattr(ast, 'unparse'))

    # ── 규칙 G (Codex CDX-11) ─────────────────────────────────────────────────────
    #   실사고: CL-20 이 `superseded_by: CL-21` 을 달고 verdict 안에서 자기 결론을 무효화
    #   하면서도 status=live 로 통과했다 → 철회된 하한 논증이 계속 인용 가능했다.
    good = dict(base, measured={'metric': 'n_components', 'value': 1, 'unit': 'c'},
                asserted='탄소가 고립되지 않는다', h1_predicts='성분 수 = 1',
                parity_certified='sr01_carbon_network.carbon_network_stats')
    chk('G-0: 기준 픽스처는 통과한다 (G 시험의 전제)', check_claim(good) == [])
    chk('G-1: superseded_by + live 는 거부 (CL-20 이 이 상태로 통과했었다)',
        any('규칙 G' in x for x in check_claim(dict(good, status='live',
                                                   superseded_by='CL-21'))))
    chk('G-2: superseded_by + retired 는 통과 (과잉차단 없음)',
        check_claim(dict(good, status='retired', superseded_by='CL-21')) == [])
    chk('G-3: superseded_by 없는 live 는 그대로 통과',
        check_claim(dict(good, status='live')) == [])

    # ── 규칙 H (2026-08-18) — 검사기 자신이 깨진 help 를 **정말** 잡는가 ────────────────
    #   실사고: `mpm_webapp_payload --help` 가 홑 `%` 하나로 완전히 죽어 있었고 아무도 몰랐다.
    #   이 두 줄은 검사가 이빨 빠지는 것을 막는다 (탐지 + 과잉차단 없음).
    _probe = {'default': 0, 'prog': 'x', 'type': 'x', 'choices': 'x',
              'const': 'x', 'metavar': 'x', 'dest': 'x'}

    def _help_ok(h):
        try:
            h % _probe
            return True
        except Exception:                              # noqa: BLE001
            return False
    chk('H-1: 홑 `%` 가 든 help 는 거부 (argparse 가 실제로 죽는 형태)',
        not _help_ok('격자 수렴 ≤0.014 %).  다음 문장'))
    chk('H-2: `%%` 와 `%(default)s` 는 통과 (과잉차단 없음)',
        _help_ok('오차 ≤0.014 %% (기본 %(default)s)'))
    chk('H-3: 리포 전체가 지금 통과한다 (0 오류)',
        check_argparse_help(verbose=False)[0] == [])

    # ── 규칙 K (2026-08-25, Codex ⑩) — 규율 selftest 배선 ──────────────────────────────
    chk('K-1: 리포가 지금 통과한다 (7개 전부 두 곳에 배선)',
        check_selftest_wiring(verbose=False)[0] == [])
    #  ★ 음성 대조 — 한쪽에서 빼면 **잡는가**.  "지금 통과한다" 만으로는 검사가 인증되지
    #    않는다 (규칙 D 의 교훈).  사본에서만 지운다.
    import tempfile as _tk, shutil as _sk
    with _tk.TemporaryDirectory() as _dk:
        _ca = os.path.join(_dk, 'check_all.sh')
        _sk.copy(os.path.join(ROOT, K_CHECK_ALL), _ca)
        with open(_ca, encoding='utf-8') as _f:
            _t = _f.read()
        _t = '\n'.join(ln for ln in _t.splitlines()
                        if not ('sr01_stamp_compare.py' in ln and '--selftest' in ln))
        with open(_ca, 'w', encoding='utf-8') as _f:
            _f.write(_t)
        _ek, _ = check_selftest_wiring(verbose=False, check_all=_ca)
        chk(f'K-2: ★ 음성 대조 — check_all 에서 한 줄 빼면 **잡는다** '
            f'({len(_ek)}건)',
            any(x.startswith('K_UNWIRED') and 'sr01_stamp_compare' in x
                and 'check_all.sh' in x for x in _ek))
        _ci = os.path.join(_dk, 'ci.yml')
        _sk.copy(os.path.join(ROOT, K_CI_YML), _ci)
        with open(_ci, encoding='utf-8') as _f:
            _t2 = _f.read()
        _t2 = '\n'.join(ln for ln in _t2.splitlines()
                         if not ('step3_sigma.py' in ln and '--selftest' in ln))
        with open(_ci, 'w', encoding='utf-8') as _f:
            _f.write(_t2)
        _ek2, _ = check_selftest_wiring(verbose=False, ci_yml=_ci)
        chk('K-3: ★ 음성 대조 — CI yml 에서 빼도 **잡는다** (드리프트 금지)',
            any(x.startswith('K_UNWIRED') and 'step3_sigma' in x for x in _ek2))
    chk('K-4: ★ 목록에 있는 selftest 가 **실재하는 파일**이다 (선언만 있고 파일이 없으면 '
        '규칙 K 자신이 가짜 보증이 된다)',
        all(os.path.exists(os.path.join(ROOT, _sc)) for _sc, _ in K_REQUIRED_SELFTESTS))
    #  ── K-5 (2026-08-25, Codex 재리뷰 조건 7) — **죽은 줄을 배선으로 세지 않는가** ────
    #    초판은 `이름 in ln and 플래그 in ln` 이라 아래가 전부 통과했다 = 규칙 K 자신이
    #    false-green (규칙 J 가 `--help` 만 보다 놓친 것과 같은 부류).
    #    ⚠ 이 문자열들은 **검사 대상 파일이 아니라 이 시험 안**에 있다 — 규칙 K 는
    #      `check_all.sh`/CI yml 만 읽으므로 여기 적어도 리포가 빨개지지 않는다.
    _DEAD = (
        ('주석 처리된 줄', '# python3 scripts/step3_sigma.py --selftest'),
        ('들여쓴 주석', '    #python3 scripts/step3_sigma.py --selftest'),
        ('echo 안내문', 'echo "python3 scripts/step3_sigma.py --selftest"'),
        ('printf 안내문', "printf '%s\\n' \"python scripts/step3_sigma.py --selftest\""),
        ('꼬리 주석', 'true   # python3 scripts/step3_sigma.py --selftest'),
        ('라벨만 일치 (대상이 다르다)',
         "run 'step3_sigma.py --selftest' python3 scripts/other.py --selftest"),
        ('플래그 없음', 'python3 scripts/step3_sigma.py'),
        ('인터프리터 없음', 'scripts/step3_sigma.py --selftest'),
        #  ★ R3-CX-08 — 죽은 가지 · 실패 삼킴 (Codex 실측 2종)
        ('죽은 가지 (false &&)', 'false && python3 scripts/step3_sigma.py --selftest'),
        ('죽은 가지 (: &&)', ': && python3 scripts/step3_sigma.py --selftest'),
        ('실패 삼킴 (|| true)', 'python3 scripts/step3_sigma.py --selftest || true'),
        ('실패 삼킴 (|| :)', 'python3 scripts/step3_sigma.py --selftest || :'),
        #  ★ R4-CX-06 (Codex 4차) — 여섯 형태를 더 통과시켰다
        ('죽은 가드 (true ||)', 'true || python scripts/step3_sigma.py --selftest'),
        ('실패 삼킴 (|| echo)', 'python scripts/step3_sigma.py --selftest || echo ignored'),
        ('종료코드 덮기 (; true)', 'python scripts/step3_sigma.py --selftest ; true'),
        ('파이프 (rc 가 가려진다)', 'python scripts/step3_sigma.py --selftest | tee r.txt'),
        ('도달 불가 (exit 0;)', 'exit 0; python scripts/step3_sigma.py --selftest'),
        ('백그라운드 (&)', 'python scripts/step3_sigma.py --selftest &'),
    )
    _dead_pass = [_lb for _lb, _ln in _DEAD
                  if k_live_invocation(_ln, 'step3_sigma.py', '--selftest')]
    chk(f'K-5: ★★ 죽은 줄 {len(_DEAD)}종을 배선으로 세지 않는다 (통과한 것: {_dead_pass})',
        not _dead_pass)
    #  ★ 판별력 자기증명 — 진짜 호출 형태는 **받아들여야** 한다 (거부만 하면 규칙이 죽는다)
    _LIVE = (
        ("run 'step3_sigma            --selftest' python3 scripts/step3_sigma.py --selftest",
         'check_all.sh 실물 형태'),
        ('        run: python scripts/step3_sigma.py --selftest', 'CI yml 실물 형태'),
        ('  /usr/bin/python3 scripts/step3_sigma.py --selftest', '절대경로 인터프리터'),
    )
    _live_fail = [_lb for _ln, _lb in _LIVE
                  if not k_live_invocation(_ln, 'step3_sigma.py', '--selftest')]
    chk(f'K-6: ★ 진짜 호출 3종은 받아들인다 (거부된 것: {_live_fail})', not _live_fail)
    #  ★★★ K-7 (2026-08-25) — **검사기가 그 판별을 실제로 쓰는가.**
    #    K-5/K-6 은 `k_live_invocation()` 을 **직접** 부르므로, 호출부가 옛 부분문자열
    #    검사로 되돌아가도 둘 다 초록이다 — 실제로 조건 8 돌연변이 스윕에서 그 되돌림을
    #    **놓쳤다**.  ⇒ 죽은 줄만 남은 `check_all.sh` 사본을 만들어 **검사기를 통째로**
    #    돌린다 (helper 가 아니라 `check_selftest_wiring` 의 거동을 본다).
    with _tk.TemporaryDirectory() as _dk7:
        _ca7 = os.path.join(_dk7, 'check_all.sh')
        with open(os.path.join(ROOT, K_CHECK_ALL), encoding='utf-8') as _f:
            _t7 = _f.read()
        _live7 = [ln for ln in _t7.splitlines()
                  if k_live_invocation(ln, 'step3_sigma.py', '--selftest')]
        _t7 = '\n'.join(('# ' + ln + '   ← 주석 처리 (K-7 음성 대조)')
                         if ln in _live7 else ln for ln in _t7.splitlines())
        #  안내문만 남긴다 — 옛 부분문자열 검사는 이것을 배선으로 센다
        _t7 += '\necho "run:  python3 scripts/step3_sigma.py --selftest"\n'
        with open(_ca7, 'w', encoding='utf-8') as _f:
            _f.write(_t7)
        _ek7, _ = check_selftest_wiring(verbose=False, check_all=_ca7)
        chk(f'K-7: ★★ **검사기가** 주석+echo 만 남은 check_all 을 거부한다 '
            f'(helper 직접 호출이 아니라 `check_selftest_wiring` 자신) — '
            f'호출부를 옛 부분문자열로 되돌리면 여기서 빨간불 ({len(_ek7)}건)',
            any(x.startswith('K_UNWIRED') and 'step3_sigma' in x for x in _ek7))

    # ── 규칙 L (2026-08-25, Codex 재리뷰 조건 7) — 러너 통합 ───────────────────────────
    chk('L-1: 리포의 러너가 지금 통과한다 (LEAN·EXPECT_PROTOCOL·PREREG_ARMS·진단분리)',
        check_runner_integration(verbose=False)[0] == [])
    #  ★ 음성 대조 4종 — 사본에서만 고친다.  "지금 통과한다" 는 검사를 인증하지 않는다.
    import tempfile as _tl, shutil as _sl
    _RSRC = open(os.path.join(ROOT, L_RUNNER), encoding='utf-8').read()

    def _rmut_src(src_):
        """완성된 러너 소스 문자열로 규칙 L 을 돌린다 (여러 겹을 동시에 지울 때)."""
        _rel = os.path.join('scripts', 'mutant_runner.sh')
        _abs = os.path.join(ROOT, _rel)
        with open(_abs, 'w', encoding='utf-8') as _f:
            _f.write(src_)
        try:
            return check_runner_integration(verbose=False, runner=_rel)[0]
        finally:
            os.remove(_abs)

    def _rmut(old_, new_):
        assert _RSRC.count(old_) == 1, (old_[:40], _RSRC.count(old_))
        _d = _tl.mkdtemp()
        _rel = os.path.join('scripts', 'mutant_runner.sh')
        _abs = os.path.join(ROOT, _rel)
        with open(_abs, 'w', encoding='utf-8') as _f:
            _f.write(_RSRC.replace(old_, new_))
        try:
            return check_runner_integration(verbose=False, runner=_rel)[0]
        finally:
            os.remove(_abs)
            _sl.rmtree(_d, ignore_errors=True)
    _m1 = _rmut('LEAN_FLAGS=" --no-step4 --no-thermal --no-trackb --no-field --no-ion --no-pore --no-collector"',
                'LEAN_FLAGS=" --no-step4 --no-thermal --no-trackb --no-field --no-ion --no-pore"')
    chk(f'L-2: ★ LEAN=2 에서 `--no-collector` 를 빼면 **잡는다** ({len(_m1)}건)',
        any(x.startswith('L_LEAN2') and 'no-collector' in x for x in _m1))
    _m2 = _rmut('$PS_FLAG$EP_FLAG$XP_FLAG$FS_FLAG', '$PS_FLAG$XP_FLAG$FS_FLAG')
    chk(f'L-3: ★★ `$EP_FLAG` 를 인자열에서 빼면 **잡는다** — 변수는 그대로 있고 '
        f'**쓰이지 않을 뿐**이라 grep 으로는 안 보인다 ({len(_m2)}건)',
        any(x.startswith('L_EXPECT') for x in _m2))
    _m3 = _rmut('PREREG_ARMS=8', 'PREREG_ARMS="$ARMS"')
    chk(f'L-4: ★★ 사전등록 팔 수가 `$ARMS` 를 따라가면 **잡는다** (자기가 자기한테 '
        f'요구하는 봉인) ({len(_m3)}건)',
        any(x.startswith('L_PREREG') for x in _m3))
    #  ⚠ 2026-08-25: 진단 분리는 이제 **두 겹**이다 — 조립 태그(`AR_TAG`) 와 R3-CX-09 의
    #    강제 접미사.  한 겹만 지우면 다른 겹이 막으므로(정상), 돌연변이는 **둘 다** 지운다.
    #    그래야 "분리가 실제로 사라진 상태" 를 시험한다.
    _m4 = _rmut('${FS_TAG}${AR_TAG}${LEAN_TAG}', '${FS_TAG}${LEAN_TAG}')
    _m4b = [x for x in _m4 if x.startswith(('L_ARMTAG', 'L_ARMNS'))]
    chk(f'L-5a ★ 조립 태그만 지우면 **강제 접미사가 막는다** (과잉차단 아님, {len(_m4)}건)',
        not _m4b)
    _both = _RSRC.replace('${FS_TAG}${AR_TAG}${LEAN_TAG}', '${FS_TAG}${LEAN_TAG}')
    _m4c = _rmut_src(_both.replace(
        'if [ "$ARMS" -ne 8 ] && [ "${OUTDIR%_arm$ARMS}" = "$OUTDIR" ]; then', 'if false; then'))
    chk(f'L-5: ★★ 두 겹을 **다** 지우면 잡는다 — 진단 런이 생산 OUTDIR 에 쓴다 '
        f'({len(_m4c)}건)',
        any(x.startswith(('L_ARMTAG', 'L_ARMNS')) for x in _m4c))
    #  ★ 표지가 사라지면 **거부**한다 (잘못 자르면 진짜 러너를 돌려 버린다)
    _m5 = _rmut(L_MARKER, 'RUNNER_CONFIG_' + 'RENAMED')
    chk(f'L-6: ★★ `{L_MARKER}` 표지가 없으면 **거부**한다 (fail-closed — 어디까지가 '
        f'설정인지 모르면 실행하지 않는다) ({len(_m5)}건)',
        any(x.startswith('L_PROBE') for x in _m5))
    _m6 = _rmut('  echo "[p2] 계약 봉인 — 데이터가 쓸 만한가 (판정 아님, 원값은 아직 안 본다)"',
                '  python3 "$SCR/sdcp_gain_verdict.py" --dir "$OUTDIR" --collect-only')
    #  ★ R3-CX-08 — `echo` 안내문이 순서 증거가 되면 안 된다 (옛 판은 됐다).
    #  실제 봉인 호출을 **안내문으로 바꾼다** — 옛 판은 그 echo 를 순서 증거로 셌다.
    _m14 = _rmut('''  if ! python3 "$SCR/sdcp_gain_verdict.py" --dir "$OUTDIR" --seal-only \\
       --require-arms "$PREREG_ARMS" --require-digest; then''',
                 '''  echo "먼저 돌릴 것: python3 $SCR/sdcp_gain_verdict.py --seal-only"
  if false; then''')
    chk(f'L-14: ★★ `echo "… --seal-only"` 안내문은 순서 증거가 아니다 (live 호출만 센다) '
        f'({len(_m14)}건)',
        any(x.startswith(('L_NOSEAL', 'L_SEALORDER')) for x in _m14))
    #  ⚠ `|| true` 는 이제 live 가 아니다 (실패 삼킴) — 순수 호출로 되돌려야 재현된다.
    _m12 = _rmut('''    echo "     원값이 필요하면 **명시로** 칠 것 — 자동으로 찍지 않는다:"''',
                 '''    python3 "$SCR/sdcp_gain_verdict.py" --dir "$OUTDIR" --collect-only''')
    chk(f'L-12: ★★ 봉인 **실패** 경로가 원값을 자동으로 찍으면 잡는다 — metadata 를 '
        f'일부러 깨뜨려 raw table 을 보는 경로 (R3-CX-02) ({len(_m12)}건)',
        any(x.startswith('L_FAILDUMP') for x in _m12))
    _m13 = _rmut('''if [ "$ARMS" -ne 8 ] && [ "${OUTDIR%_arm$ARMS}" = "$OUTDIR" ]; then''',
                 'if false; then')
    chk(f'L-13: ★★ 진단 런이 **사용자 OUTDIR** 을 그대로 쓰면 잡는다 — 2팔이 8팔 '
        f'디렉터리에 섞인다 (R3-CX-09) ({len(_m13)}건)',
        any(x.startswith('L_ARMNS') for x in _m13))
    _m10 = _rmut('--require-arms "$PREREG_ARMS" --require-digest',
                 '--require-arms "$PREREG_ARMS"')
    chk(f'L-10: ★ 최종 봉인에서 `--require-digest` 를 빼면 **잡는다** ({len(_m10)}건)',
        any(x.startswith('L_NODIGEST') for x in _m10))
    _m11 = _rmut('  for _tok in $P2_EXTRA; do', '  for _tok in ; do')
    chk(f'L-11: ★★ `P2_EXTRA` 금지 검사를 무력화하면 **잡는다** — 주의 주석은 게이트가 '
        f'아니다 ({len(_m11)}건)',
        any(x.startswith('L_P2EXTRA') for x in _m11))
    _m7 = _rmut('$PS_FLAG$EP_FLAG$XP_FLAG$FS_FLAG', '$PS_FLAG$EP_FLAG$FS_FLAG')
    chk(f'L-8: ★★ 러너 자기설정 선언(`$XP_FLAG`)이 인자열에서 빠지면 **잡는다** — '
        f'첫 팔의 id 를 베끼면 첫 팔이 진리가 된다 (조건 4) ({len(_m7)}건)',
        any(x.startswith('L_EXPECTPHYS') for x in _m7))
    _m8 = _rmut('local XP="vox_um=$VOX,bridge_um=$BRIDGE_UM,sigma_vgcf_S_cm=$SIGMA"',
                'local XP="bridge_um=$BRIDGE_UM,sigma_vgcf_S_cm=$SIGMA"')
    chk(f'L-9: ★ 선언에서 축 하나(vox_um)를 빼면 **잡는다** ({len(_m8)}건)',
        any(x.startswith('L_EXPECTPHYS_AXIS') for x in _m8))
    chk(f'L-7: ★★ 원값 덤프(`--collect-only`)가 봉인보다 앞서면 **잡는다** — '
        f'결과를 보고 봉인을 통과시킬지 고를 수 있으면 눈먼 봉인이 아니다 ({len(_m6)}건)',
        any(x.startswith('L_SEALORDER') for x in _m6))

    # ── 규칙 M (2026-08-25, A1 / R4-CX-03 잔여) — CLI 회계 ────────────────────────────
    import run_contract as _rcM
    _MOPT, _MERR = _payload_options(os.path.join(ROOT, 'scripts', 'mpm_webapp_payload.py'))
    chk('M-1: 실물 파서를 잡는다 (parse_args 가로채기)', _MERR is None and len(_MOPT) > 40)
    #  ★★ 이것이 초판의 구멍이다 — `--temp-c`·`--ea-ion-ev` 는 `se_material.temperature_argparse`
    #    가 **다른 모듈**에서 등록한다.  payload 파일만 AST 로 훑던 판은 이 둘을 못 봤고,
    #    오히려 "회계에 있는데 파서에 없다" 고 **거꾸로** 보고했다.  정적 훑기로 되돌리면
    #    여기서 빨간불이 난다.
    chk('M-2: helper 모듈이 등록한 옵션도 잡힌다 (--temp-c·--ea-ion-ev — 초판 AST 가 놓쳤다)',
        '--temp-c' in _MOPT and '--ea-ion-ev' in _MOPT)
    chk('M-3: 리포 실물이 지금 통과한다 (79 옵션 · 규약 축 전수 도달)',
        check_cli_accounting(verbose=False)[0] == [])

    def _mprob(opts=None, acct=None, pf=None, cc=None, cats=None):
        """합성 입력으로 규칙 M 의 **판정부**를 직접 문다 (리포를 안 건드린다)."""
        return cli_accounting_problems(
            list(opts if opts is not None else _MOPT),
            dict(acct if acct is not None else _rcM.CLI_ACCOUNTING),
            tuple(pf if pf is not None else _rcM.PROTOCOL_FIELDS),
            tuple(cc if cc is not None else _rcM.PROTOCOL_CODE_CONST),
            tuple(cats if cats is not None else _rcM.CLI_CATEGORIES))

    chk('M-4: 새 옵션이 회계 없이 생기면 → M_UNACCOUNTED',
        any(x.startswith('M_UNACCOUNTED') and '--brand-new-sigma' in x
            for x in _mprob(opts=_MOPT + ['--brand-new-sigma'])))
    _acct_stale = dict(_rcM.CLI_ACCOUNTING); _acct_stale['--gone-knob'] = ('mode', None)
    chk('M-5: 파서에서 사라진 옵션이 회계에 남으면 → M_STALE',
        any(x.startswith('M_STALE') and '--gone-knob' in x for x in _mprob(acct=_acct_stale)))
    _acct_bad = dict(_rcM.CLI_ACCOUNTING); _acct_bad['--sigma-vgcf'] = ('protocol', ('no_such_axis',))
    chk('M-6: `protocol` 인데 규약 축에 없는 필드를 대면 → M_NOTINPROTOCOL',
        any(x.startswith('M_NOTINPROTOCOL') and '--sigma-vgcf' in x for x in _mprob(acct=_acct_bad)))
    #  ★ `derived` 도 같은 잣대다 — "다른 축이 흡수한다" 는 주장은 그 축이 실재해야 성립한다
    _acct_bd = dict(_rcM.CLI_ACCOUNTING); _acct_bd['--ea-ion-ev'] = ('derived', ('no_such_axis',))
    chk('M-7: `derived` 가 없는 축을 가리켜도 → M_NOTINPROTOCOL',
        any(x.startswith('M_NOTINPROTOCOL') and '--ea-ion-ev' in x for x in _mprob(acct=_acct_bd)))
    chk('M-8: 규약 축을 아무 CLI 도 못 가리키면 → M_ORPHAN_FIELD',
        any(x.startswith('M_ORPHAN_FIELD') and 'lonely_axis' in x
            for x in _mprob(pf=tuple(_rcM.PROTOCOL_FIELDS) + ('lonely_axis',))))
    #  ⚠ **그 축에 대해서만** 묻는다.  옛 판은 `M_ORPHAN_FIELD` 가 하나도 없을 것을
    #    요구해, 리포의 **다른** 축이 고아가 되는 변형(`--dilate-z` 강등)에도 같이
    #    빨간불이 났다 = 시험 얽힘 (배터리가 '과잉' 으로 잡았다).
    chk('M-9: 코드 상수로 선언하면 고아가 아니다 (plate_rule 규약)',
        not any(x.startswith('M_ORPHAN_FIELD') and 'lonely_axis' in x for x in
                _mprob(pf=tuple(_rcM.PROTOCOL_FIELDS) + ('lonely_axis',),
                       cc=tuple(_rcM.PROTOCOL_CODE_CONST) + ('lonely_axis',))))
    _acct_cat = dict(_rcM.CLI_ACCOUNTING); _acct_cat['--cam'] = ('protokol', ('cam',))
    chk('M-10: 범주 어휘 오타 → M_BADCAT',
        any(x.startswith('M_BADCAT') and '--cam' in x for x in _mprob(acct=_acct_cat)))
    #  ★★ A1 이 실제로 적발한 것 — 이 둘이 규약 축이 아니면 침대가 조용히 달라진다
    chk('M-11: `--dilate-z`·`--se-proxy` 가 규약 축을 가리킨다 (A1 2차 적발)',
        _rcM.CLI_ACCOUNTING['--dilate-z'] == ('protocol', ('dilate_z',))
        and _rcM.CLI_ACCOUNTING['--se-proxy'][1] == ('se_source',)
        and {'dilate_z', 'se_source'} <= set(_rcM.PROTOCOL_FIELDS))

    # ── 규칙 J (2026-08-20) — 생산 엔트리포인트 스모크 ────────────────────────────────
    #   J-2 가 이 규칙의 존재 이유다: "지금 리포가 통과한다" 만으로는 검사기가 **정말**
    #   잡는지 증명되지 않는다 (규칙 D 의 교훈).  고쳐 둔 hoist 한 줄을 사본에서 지우고
    #   실제로 돌려, 08-12~20 의 그 사고가 재현되고 **검사가 그것을 잡는지** 본다.
    chk('J-1: 두 팔(±--fibre)이 지금 통과한다 (STEP3 manifest 가 complete)',
        check_entrypoint_smoke(verbose=False)[0] == [])
    chk('J-2: ★ 음성 대조 — `_dia_all`/`_kind_all` hoist 를 지우면 **잡는다**',
        smoke_negative_control(verbose=False)[0] == [])
    #  ── J-3 (2026-08-20, Codex CDX-IJ-05) — **계산 없는 자가보고**를 잡는가 ──────────────
    #     Codex 가 독립 fake producer 로 통과시킨 두 변형을 그대로 상주 음성 대조로 만든다.
    import json as _j3
    import tempfile as _t3

    def _fake(comps, s3extra=None):
        _d = _t3.mkdtemp()
        _p = os.path.join(_d, 'fake.json')
        with open(_p, 'w', encoding='utf-8') as _f:
            _j3.dump({'mpm_metrics': {'step3': dict(
                {'manifest': {'components': comps}}, **(s3extra or {}))}}, _f)
        _e, _w = [], []
        smoke_assert_payload(_p, 'fake', _e, _w)
        return _e
    #  ⚠ 2026-08-20 (Codex 재검증 IJ-05) — 옛 판은 "오류 목록이 비었는지" 만 봤다.  그러면
    #    J_COMPONENT 검사를 **지워도** 다른 오류가 대신 남아 통과한다 = 그 검사가 인증되지 않는다.
    #    ⇒ **예상 diagnostic code 를 고정**한다 (Codex 최소 계약 ④).
    def _codes(e_):
        return {x.split('|', 1)[0] for x in e_}
    chk('J-3a: ★ electronic=complete 한 줄만 적은 가짜 producer 를 J_COMPONENT 로 잡는다',
        'J_COMPONENT' in _codes(_fake({'electronic': {'status': 'complete'}})))
    chk('J-3b: ★ 전부 disabled 로 적은 변형을 J_COMPONENT 로 잡는다',
        'J_COMPONENT' in _codes(_fake({k: {'status': 'disabled'} for k in
                                       ('electronic', 'ionic', 'thermal', 'pore', 'pnm')})))
    #  J-3d: Codex 가 **통과시킨** 변형 — 기대 상태 전부 + sigma_e=1 + n_dof=1, 계산 증거 없음
    chk('J-3d: ★★ 상태·수치가 다 있어도 **CG 증거가 없으면** 잡는다 (Codex 통과 변형)',
        'J_NUMBERS' in _codes(_fake(
            {'electronic': {'status': 'complete'}, 'thermal': {'status': 'complete'},
             'ionic': {'status': 'disabled'}, 'pore': {'status': 'disabled'},
             'pnm': {'status': 'disabled'}},
            {'sigma_e_eff_S_cm': 1.0, 'n_dof': 1})))
    chk('J-3c: ★ 상태는 맞는데 **수치가 없는** 변형을 잡는다 (자가보고)',
        any('J_NUMBERS' in x for x in _fake(
            {'electronic': {'status': 'complete'}, 'thermal': {'status': 'complete'},
             'ionic': {'status': 'disabled'}, 'pore': {'status': 'disabled'},
             'pnm': {'status': 'disabled'}})))

    print(f'\ncheck_method_discipline v3 selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    errs, warns = run_all(verbose=not a.quiet)
    print()
    for w in warns:
        print(f'  ⚠ {w}')
    if errs:
        print(f'\n✗ 방법론 규율: {len(errs)} 오류')
        for x in errs:
            print(f'  · {x}')
        return 1
    print('✓ 방법론 규율: 0 오류' + (f' ({len(warns)} 경고)' if warns else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

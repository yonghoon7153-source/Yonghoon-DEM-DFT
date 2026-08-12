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
        elif '3, 3, 3' in ast.unparse(st) or '3,3,3' in ast.unparse(st):
            conns.add('26-conn')
        else:
            conns.add(f'UNKNOWN({ast.unparse(st)})')
    return conns


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
        out.append(f'**가능도비 1** — h0 와 h1 이 똑같이 "{h0p}" 를 예측한다 (D1)')
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
                out.append(f'두 예측의 차이 {abs(n0[0]-n1[0]):.4g} 가 분해능 {res} 미만 '
                           f'— 분해능 아래의 판별력은 가능도비 1 과 같다')
        # C-3 구간 겹침
        if len(n0) == 2 and len(n1) == 2:
            if min(n0[1], n1[1]) >= max(n0[0], n1[0]):
                out.append(f'두 예측 구간이 겹친다 {n0} ∩ {n1} — 관측이 양쪽에 든다')
    # C-4 measured ↔ verdict 정합
    mv = _nums((c.get('measured') or {}).get('value'))
    vd = _norm(c.get('verdict'))
    if len(mv) == 1 and vd:
        for tag, pred in (('h0채택', h0p), ('h1채택', h1p)):
            other = h1p if tag == 'h0채택' else h0p
            if tag in vd and _nums(other) and _nums(pred):
                if abs(mv[0] - _nums(other)[0]) < abs(mv[0] - _nums(pred)[0]):
                    out.append(f'측정 {mv[0]} 이 채택하지 않은 가설에 더 가까운데 '
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
        out.append(f'`{metric}` 은 **세는 양**인데 귀결({hit_t[:2]})을 주장하면서 쓸 만한 '
                   f'bridge 가 없다 (규칙 D)')
    # ★ 검증-귀결 갈래는 count 가 아니어도 shared_input 을 요구 (S4 흡수)
    if hit_v and 'shared_input' not in c:
        out.append(f'검증-귀결 어휘({hit_v[:2]})를 쓰면서 `shared_input` 이 없다 — '
                   f'A 와 B 가 입력을 공유해 일치가 강제되는 경로를 적어야 한다 (없으면 null)')
    # 규칙 E — 량 패리티 (S0 X-1)
    q = c.get('quantity')
    qa = c.get('compared_to_quantity')
    if q and qa and _QUANTITY_ALIASES.get(q, q) != _QUANTITY_ALIASES.get(qa, qa):
        out.append(f'**량 범주 오류** — {q} 를 {qa} 와 비교한다 (규칙 E). '
                   f'K 25.5 vs 영률 24 가 이 형태였다')
    return out


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
            elif verbose and st == 'rejected':
                print(f'  거부됨  {c["id"]}: {bad[0].split(": ", 1)[-1][:76]}')
            continue
        if c.get('evidence_state') not in _EVIDENCE_OK:
            errs.append(f'{c["id"]}: evidence_state={c.get("evidence_state")!r} 인데 status='
                        f'{st!r} 다 — 인용차단이 안 된다.  status 를 "hold" 로 내릴 것')
        n_live += 1
        errs.extend(bad)
        if not bad and verbose:
            print(f'  OK      {c["id"]}: {str(c["claim"])[:68]}')
    if verbose:
        print(f'  ── claims {len(claims)}건 (채점 {n_live} · 면제 {len(claims) - n_live})')
    return errs, warns


# ═══════════════════════════════════════════════════════════════════════════
def run_all(verbose=True):
    errs, warns = [], []
    for title, fn in (('규칙 A — 규약·격자·주기 패리티 (D4)', check_convention_parity),
                      ('규칙 B — 판별력 있는 rung (D2)', check_oblique_rungs),
                      ('규칙 C·D·E — 판별력 / 개수≠귀결 / 량 패리티 (D1)', check_claims_ledger)):
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

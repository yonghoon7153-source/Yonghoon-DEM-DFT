#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""방법론 규율 검사 — D1~D5 를 **산문에서 검사로** 승격한다.

★ 왜 필요한가 (CLAUDE.md 가 자기 입으로 진단한 것):

    "리포는 같은 실수를 이미 3번 잡고(K 25.5 vs 영률 24 · SDCP pellet ×5.1 ·
     koo2026 0.20) **규칙으로 승격하지 않았다.**"

D1~D5 도 판정 문서 안의 **글**이지 검사가 아니었다.  그래서 다음 세션이 같은 함정을
다시 밟는다.  이 파일은 그 글을 기계가 읽는 규칙으로 만든다.

★★ **이 검사 자체에 거는 규율**: 규칙은 그것을 낳은 **실제 결함을 잡아야 한다**.
   잡지 못하는 규칙은 연극이다 (D1 을 규칙 자신에게 적용).  그래서 selftest 는
   각 규칙이 **역사적 실패 사례를 실제로 거부하는지** 시험한다.

──────────────────────────────────────────────────────────────────────────────
규칙 A — 규약 패리티 (D4).  진단 지표는 솔버와 **같은 인접 규약·같은 격자**에서.
  낳은 결함: econn 이 26-conn @0.30 µm 로 재료 점을 재복셀화해 6-face @0.4 µm
  솔버의 SR-01 결함에 **원리적으로** 눈멀었다.  4개월.

규칙 B — 비축정렬 rung (D2).  래스터/솔버는 **비스듬한** 알려진-정답 시험을 가진다.
  낳은 결함: STEP3 selftest 가 전부 축정렬이라 점 스탬프가 안 깨졌다.  그 rung 하나가
  SR-01 을 작년에 잡았을 것.  (2026-08-12 에 **내가 게이트 ② 픽스처를 또 축정렬로**
  짜서 통과시켰다 — 사람도 같은 함정에 빠진다는 실증.)

규칙 C — 판별력 (D1).  수를 증거로 인용하려면 **경쟁 가설이 예측하는 값**을 같은 줄에.
  h0 와 h1 이 같은 값을 예측하면 가능도비 1 = **증거량 0** 이다.
  낳은 결함: "VGCF 소산분담 4 %"(안심 신호로 오독) · "f_am_mpm ≈ 0.50"(보존 항등식)
  — 둘 다 두 가설이 **같은 값**을 예측하는 수였다.

규칙 D — 개수 ≠ 귀결.  세어놓고 귀결을 추론하지 않는다.  다리(bridge)를 명시하거나
  귀결 자체를 측정한다.
  낳은 결함: "탄소가 23,914 조각" → "전기적으로 단절" 로 비약.  실제로는 94 %가
  AM 에 면-인접해 **회로에 꽂혀 있었다** (2026-08-12 측정).

사용:
    python3 scripts/check_method_discipline.py            # 전체 검사
    python3 scripts/check_method_discipline.py --selftest # 규칙이 실제로 무는지
"""
from __future__ import annotations

import argparse
import inspect
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
LEDGER = os.path.join(ROOT, 'docs', 'reviews', 'claims.json')

# ═══════════════════════════════════════════════════════════════════════════
# 규칙 A — 규약 패리티
# ═══════════════════════════════════════════════════════════════════════════
#  솔버가 쓰는 인접 규약이 정본이다.  진단은 거기 맞추거나, 못 맞추면 **무엇을 증언할 수
#  없는지** 명시적으로 포기해야 한다 (waiver).  포기 없이 어긋나면 오류.
SOLVERS = {
    'step3_sigma.solve': {
        'adjacency': '6-face',
        'grid': 'STEP3 복셀 (--vox, 생산 기본 0.4 µm)',
        'why': '유한체적 ∇·(σ∇φ)=0 은 면을 공유하는 셀 사이에서만 플럭스를 정의한다',
    },
}

DIAGNOSTICS = {
    'mpm_webapp_payload.electronic_connectivity': {
        'diagnoses': 'step3_sigma.solve',
        'adjacency': '26-conn',
        'grid': 'vox_um 기본 0.30 µm — **재료 점을 재복셀화** (STEP3 래스터를 보지 않는다)',
        'waiver': (
            'econn 의 목적은 STEP3 진단이 아니라 **이진 퍼콜레이션**(집전체까지 전자 경로가 '
            '있는가 = dead-AM)이다.  26-conn 과 큰 복셀은 "이어진 한 가닥 = 한 도체" 를 '
            '만들기 위한 **의도된 선택**이며 함수 주석이 그렇게 적고 있다.'),
        'must_not_certify': ['fibre_stamp', 'raster fidelity', 'STEP3 connectivity',
                             'point vs segment'],
        'evidence': ('두 팔은 같은 재료 점을 쓰므로 econn 은 경험적으로가 아니라 **정의에 '
                     '의해** 동일하다 — 입력에 변수가 없다 (sr01_carbon_network.econn_blindness).'),
    },
    'sr01_carbon_network.carbon_network_stats': {
        'diagnoses': 'step3_sigma.solve',
        'adjacency': '6-face',
        'grid': '같은 vox (기본 0.4 µm)',
        'waiver': None,
        'must_not_certify': [],
        'evidence': 'D4 준수 — 솔버와 같은 규약이라 스탬프 차이를 본다.',
    },
}

# 소스에서 인접 규약을 **읽어낸다** (선언을 믿지 않는다 — 코드가 정본)
_ADJ_SIG = {
    '26-conn': ('np.ones((3, 3, 3)', 'generate_binary_structure(3, 3)'),
    '6-face': ('generate_binary_structure(3, 1)', '_label6', 'n_components_6face'),
}


def _detect_adjacency(fn):
    """함수 소스에서 인접 규약을 추정한다.  ⚠ 선언과 다르면 **선언이 틀린 것**이다."""
    try:
        src = inspect.getsource(fn)
    except (OSError, TypeError):
        return None
    hits = [k for k, sigs in _ADJ_SIG.items() if any(s in src for s in sigs)]
    return hits[0] if len(hits) == 1 else (None if not hits else '/'.join(sorted(hits)))


def _resolve(dotted):
    mod, _, name = dotted.rpartition('.')
    return getattr(__import__(mod), name)


def check_convention_parity(verbose=True):
    errs, warns = [], []
    for dname, d in DIAGNOSTICS.items():
        solver = SOLVERS.get(d['diagnoses'])
        if solver is None:
            errs.append(f'{dname}: 진단 대상 솔버 {d["diagnoses"]} 가 등록부에 없다')
            continue
        try:
            fn = _resolve(dname)
        except Exception as e:                                     # 의존성 없는 환경
            warns.append(f'{dname}: 불러올 수 없음 ({type(e).__name__}) — 규약 대조 생략')
            continue
        seen = _detect_adjacency(fn)
        if seen and seen != d['adjacency']:
            errs.append(f'{dname}: 등록부는 {d["adjacency"]} 라는데 소스는 {seen} '
                        f'— **등록부가 낡았다** (코드가 정본)')
        if d['adjacency'] != solver['adjacency']:
            if not d.get('waiver'):
                errs.append(f'{dname}: 솔버는 {solver["adjacency"]} 인데 진단은 '
                            f'{d["adjacency"]} 이고 waiver 가 없다 (D4 위반)')
            elif not d.get('must_not_certify'):
                errs.append(f'{dname}: waiver 는 있는데 **무엇을 증언할 수 없는지**'
                            f'(must_not_certify)가 비었다 — 포기가 명시되지 않았다')
            elif verbose:
                print(f'  waiver  {dname}: {solver["adjacency"]} ≠ {d["adjacency"]} '
                      f'→ 증언 금지 {d["must_not_certify"]}')
        elif verbose:
            print(f'  OK      {dname}: {d["adjacency"]} = 솔버와 일치')
    return errs, warns


# ═══════════════════════════════════════════════════════════════════════════
# 규칙 B — 비축정렬 rung
# ═══════════════════════════════════════════════════════════════════════════
def n_varying_axes(pts, tol=1e-9):
    P = np.asarray(pts, float)
    if P.ndim != 2 or len(P) < 2:
        return 0
    return int(((P.max(0) - P.min(0)) > tol).sum())


def is_axis_aligned(pts, tol=1e-9):
    """축정렬(= 한 축으로만 변하는) 선인가.

    ★ 점 스탬프 결함은 **연속된 두 점이 모서리/꼭짓점만 닿는 셀에 떨어질 때** 나타난다.
      방향 벡터의 유효 성분이 1개면 그런 일이 **절대** 안 생긴다 → 그 픽스처는 결함을
      영원히 통과시킨다.  2개 이상이어야 시험이 시험이다.
    """
    return n_varying_axes(pts, tol) < 2


def assert_oblique(pts, name, tol=1e-9):
    """픽스처가 비축정렬임을 강제한다.  selftest 안에서 부른다."""
    k = n_varying_axes(pts, tol)
    if k < 2:
        raise AssertionError(
            f'축정렬 픽스처 "{name}" ({k}개 축으로만 변함) — 점 스탬프 결함은 이 배치에서 '
            f'원리적으로 나타나지 않는다.  대각 방향으로 바꾸거나, 의도된 것이면 '
            f'is_axis_aligned() 를 직접 부르고 이유를 주석에 남길 것.')
    return True


#  래스터/연결성 도구는 **비스듬한 알려진-정답 rung** 을 최소 1개 가져야 한다.
#  등록만 하는 게 아니라 이 검사가 **실제로 실행**한다.
def _rung_oblique_segment():
    """비스듬한 1D 도체: 점 스탬프는 깨지고 선분 스탬프는 안 깨진다 (알려진 정답)."""
    from fibre_segment_raster import n_components_6face, point_cells, polyline_cells
    P = np.stack([np.linspace(0.3, 6.3, 60)] * 3, axis=1)      # (1,1,1) 대각
    assert_oblique(P, 'oblique 1D conductor')
    pt = np.unique(point_cells(P, 0.4), axis=0)
    sg = np.unique(polyline_cells(P, 0.4), axis=0)
    npt, nsg = n_components_6face(pt), n_components_6face(sg)
    return (npt > 1 and nsg == 1,
            f'대각 도체: 점 {npt} 성분 / 선분 {nsg} 성분 (기대: 점>1, 선분=1)')


def _rung_axis_aligned_is_blind():
    """★ 대조군: 축정렬이면 **점 스탬프도 안 깨진다** = 그 픽스처는 증거를 못 준다."""
    from fibre_segment_raster import n_components_6face, point_cells
    P = np.stack([np.linspace(0.3, 6.3, 60), np.full(60, 1.1), np.full(60, 2.1)], axis=1)
    npt = n_components_6face(np.unique(point_cells(P, 0.4), axis=0))
    return (npt == 1 and is_axis_aligned(P),
            f'축정렬 도체: 점 스탬프도 {npt} 성분 → 이 픽스처는 SR-01 을 영원히 통과시킨다')


RUNGS = {
    'fibre_segment_raster (oblique)': _rung_oblique_segment,
    'fibre_segment_raster (axis-aligned control)': _rung_axis_aligned_is_blind,
}


def check_oblique_rungs(verbose=True):
    errs, warns = [], []
    for name, fn in RUNGS.items():
        try:
            ok, msg = fn()
        except Exception as e:
            warns.append(f'{name}: 실행 불가 ({type(e).__name__}: {e})')
            continue
        if ok and verbose:
            print(f'  OK      {name}: {msg}')
        elif not ok:
            errs.append(f'{name}: {msg}')
    return errs, warns


# ═══════════════════════════════════════════════════════════════════════════
# 규칙 C·D — 판별력 + 개수 ≠ 귀결  (원장 docs/reviews/claims.json)
# ═══════════════════════════════════════════════════════════════════════════
_REQUIRED = ('id', 'claim', 'measured', 'asserted', 'h0', 'h1',
             'h0_predicts', 'h1_predicts', 'status')
_STATUS = ('live', 'retired', 'rejected')

#  "세는 양" — 이것만으로 귀결을 주장하면 다리(bridge)가 필요하다
COUNT_METRICS = ('n_components', 'n_fragments', 'component_count', 'broken_pct',
                 'mean_components', 'n_pieces', 'dissipation_share', 'share',
                 'f_am_volume_sum', 'ratio_sum')
#  "귀결" 어휘 — 세어놓고 이걸 주장하면 비약이다
CONSEQUENCE_WORDS = ('단절', 'severed', '전기적으로 죽', 'dead', '하중분담', 'load share',
                     'load-bearing', '기여', 'contributes', '지배', 'dominates',
                     'disconnected', '고립', 'isolated')


def check_claim(c):
    """claim 한 건을 검사한다 → 오류 문자열 리스트."""
    e = []
    for k in _REQUIRED:
        if k not in c or c[k] in (None, ''):
            e.append(f'{c.get("id", "?")}: 필수 필드 `{k}` 누락')
    if e:
        return e
    if c['status'] not in _STATUS:
        e.append(f'{c["id"]}: status 는 {_STATUS} 중 하나여야 한다')
    # 규칙 C — 판별력.  두 가설이 같은 값을 예측하면 그 수는 증거가 아니다.
    if str(c['h0_predicts']).strip() == str(c['h1_predicts']).strip():
        e.append(f'{c["id"]}: **가능도비 1** — h0 와 h1 이 똑같이 '
                 f'"{c["h0_predicts"]}" 를 예측한다.  이 수는 증거가 아니라 기록이다 (D1)')
    # 규칙 D — 개수 ≠ 귀결.  세는 양으로 귀결을 주장하려면 다리를 명시한다.
    metric = str((c['measured'] or {}).get('metric', ''))
    if any(m in metric for m in COUNT_METRICS):
        if any(w in str(c['asserted']) for w in CONSEQUENCE_WORDS) and not c.get('bridge'):
            e.append(f'{c["id"]}: `{metric}` 은 **세는 양**인데 귀결("{c["asserted"]}")을 '
                     f'주장하면서 bridge 가 없다 — 개수→귀결 비약 (규칙 D)')
    return e


def check_claims_ledger(path=LEDGER, verbose=True):
    errs, warns = [], []
    if not os.path.exists(path):
        return [f'claims 원장이 없다: {path}'], warns
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    claims = data.get('claims', [])
    ids = [c.get('id') for c in claims]
    for dup in {i for i in ids if ids.count(i) > 1}:
        errs.append(f'중복 id: {dup}')
    n_live = 0
    for c in claims:
        bad = check_claim(c)
        if c.get('status') == 'rejected':
            #  거부 표본은 **반드시 걸려야** 한다 — 안 걸리면 규칙이 이빨 빠진 것
            if not bad:
                errs.append(f'{c.get("id")}: status=rejected 인데 검사를 **통과했다** '
                            f'— 규칙이 이 역사적 실패를 못 잡는다 (규칙이 연극이 됐다)')
            elif verbose:
                print(f'  거부됨  {c["id"]}: {bad[0].split(": ", 1)[-1][:78]}')
            continue
        n_live += 1
        errs.extend(bad)
        if not bad and verbose:
            print(f'  OK      {c["id"]}: {str(c["claim"])[:70]}')
    if verbose:
        print(f'  ── claims: {len(claims)}건 (live/retired {n_live}, '
              f'rejected 표본 {len(claims) - n_live})')
    return errs, warns


# ═══════════════════════════════════════════════════════════════════════════
def run_all(verbose=True):
    errs, warns = [], []
    for title, fn in (('규칙 A — 규약 패리티 (D4)', check_convention_parity),
                      ('규칙 B — 비축정렬 rung (D2)', check_oblique_rungs),
                      ('규칙 C·D — 판별력 / 개수≠귀결 (D1)', check_claims_ledger)):
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

    # 규칙 B — 탐지기 자체
    diag = np.stack([np.linspace(0, 5, 20)] * 3, axis=1)
    axis = np.stack([np.linspace(0, 5, 20), np.zeros(20), np.zeros(20)], axis=1)
    plane = np.stack([np.linspace(0, 5, 20), np.linspace(0, 3, 20), np.zeros(20)], axis=1)
    chk('B: 대각선은 비축정렬', not is_axis_aligned(diag))
    chk('B: 한 축 선은 축정렬', is_axis_aligned(axis))
    chk('B: 평면 안 대각선도 비축정렬 (점 스탬프가 실제로 깨지는 배치)',
        not is_axis_aligned(plane))
    try:
        assert_oblique(axis, 'x')
        chk('B: assert_oblique 가 축정렬을 거부', False)
    except AssertionError:
        chk('B: assert_oblique 가 축정렬을 거부', True)
    chk('B: assert_oblique 가 대각선은 통과', assert_oblique(diag, 'd'))

    # ★ 역사적 실패 3건을 규칙이 실제로 무는가 (규칙 자신에게 D1 적용)
    hist_vgcf = {'id': 'T1', 'claim': 'VGCF 가 잘 배선돼 있다', 'status': 'live',
                 'measured': {'metric': 'dissipation_share', 'value': 0.04},
                 'asserted': 'VGCF 가 σ_e 에 기여한다',
                 'h0': '점 스탬프가 VGCF 를 끊었다', 'h1': 'VGCF 는 원래 기여가 작다',
                 'h0_predicts': '분담 ≈ 4 %', 'h1_predicts': '분담 ≈ 4 %'}
    chk('C: "VGCF 4 %" 를 가능도비 1 로 거부', any('가능도비 1' in x
                                                for x in check_claim(hist_vgcf)))
    hist_fam = {'id': 'T2', 'claim': 'MPM 이 f_AM 을 스스로 쟀다', 'status': 'live',
                'measured': {'metric': 'f_am_volume_sum', 'value': 0.50},
                'asserted': 'AM 이 하중분담의 절반을 진다',
                'h0': '진짜 절반을 진다', 'h1': '전부피 합이 보존 항등식이다',
                'h0_predicts': '0.50', 'h1_predicts': '0.50'}
    e2 = check_claim(hist_fam)
    chk('C: "f_am 0.50" 을 가능도비 1 로 거부', any('가능도비 1' in x for x in e2))
    chk('D: "f_am 0.50" 은 세는 양→하중분담 비약으로도 거부',
        any('개수→귀결' in x for x in e2))
    hist_frag = {'id': 'T3', 'claim': '점 스탬프가 탄소를 전기적으로 끊는다', 'status': 'live',
                 'measured': {'metric': 'n_components', 'value': 23914},
                 'asserted': '탄소가 전기적으로 단절됐다',
                 'h0': '조각이 회로에서 고립됐다', 'h1': '조각이 AM 에 꽂혀 있다',
                 'h0_predicts': '성분 수가 크다', 'h1_predicts': '성분 수가 크다'}
    e3 = check_claim(hist_frag)
    chk('D: "23,914 조각 → 단절" 을 개수→귀결 비약으로 거부',
        any('개수→귀결' in x for x in e3))
    chk('C: 같은 건이 가능도비 1 로도 거부', any('가능도비 1' in x for x in e3))
    #  다리를 달면 통과해야 한다 (규칙이 정당한 주장까지 막으면 안 된다)
    fixed = dict(hist_frag, bridge='plugged_frac 0.944 를 별도 측정 — 조각이 AM 에 꽂혀 있다',
                 h1_predicts='성분 수가 크지만 plugged_frac ≈ 1')
    chk('D: bridge + 갈리는 예측을 달면 통과 (규칙이 과잉차단하지 않는다)',
        check_claim(fixed) == [])
    #  필수 필드
    chk('C: 필수 필드 누락을 잡는다', any('필수 필드' in x for x in check_claim({'id': 'T4'})))

    # 규칙 A — 소스에서 규약을 읽는다 (선언을 믿지 않는다)
    try:
        from mpm_webapp_payload import electronic_connectivity as _ec
        chk('A: econn 의 26-conn 을 **소스에서** 읽어낸다',
            _detect_adjacency(_ec) == '26-conn')
    except Exception as e:
        print(f'  SKIP  A: econn 불러오기 불가 ({e})')
    try:
        from sr01_carbon_network import carbon_network_stats as _cn
        chk('A: 6-face 진단도 소스에서 읽어낸다', _detect_adjacency(_cn) == '6-face')
    except Exception as e:
        print(f'  SKIP  A: carbon_network 불러오기 불가 ({e})')
    #  ★ 실제로 **불러올 수 있는** 대상이어야 한다 — 가짜 이름을 쓰면 import 실패가
    #    warns 로 빠져 규칙이 무는지 시험이 안 된다 (첫 판이 그렇게 통과했다).
    bad_reg = {'mpm_webapp_payload.electronic_connectivity': {
        'diagnoses': 'step3_sigma.solve', 'adjacency': '26-conn',
        'grid': '?', 'waiver': None, 'must_not_certify': []}}
    _save = DIAGNOSTICS.copy()
    DIAGNOSTICS.clear(); DIAGNOSTICS.update(bad_reg)
    e_a, _ = check_convention_parity(verbose=False)
    DIAGNOSTICS.clear(); DIAGNOSTICS.update(_save)
    chk('A: waiver 없는 규약 불일치를 거부', any('waiver 가 없다' in x for x in e_a))

    print(f'\ncheck_method_discipline selftest: {ok}/{ok + len(fail)} PASS'
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
    print(f'✓ 방법론 규율: 0 오류' + (f' ({len(warns)} 경고)' if warns else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

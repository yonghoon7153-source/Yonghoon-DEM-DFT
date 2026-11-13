#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② Q12 두 기계 조립 비교 설계 (`scripts/cjunc_asm_compare.py`) · 시험 먼저 (11-13 Codex 반박 1/2 RCPX-03 · 실제 실행 없음 · CPU · 수 초).

  K1a 판정문 반례 그대로 (비교 모듈 없이 · 고치기 전 트리에서도 돈다) — 실제 `CjuncAssembler._assemble` · 두 노드 · 병렬 간선 셋 (전도도
      [1, 2^-53, 2^-53] ↔ [2^-53, 2^-53, 1]): 가중 그래프 지문 같음 · CSR 비대각 1 ulp 다름 (-0x1.0000000000000p+0 ↔ -0x1.0000000000001p+0) ·
      b · indices · indptr 같음 (= 지문 같음에서 CSR 비트 같음이 나오지 않는다)
  K1  같은 반례를 비교 함수로 → graph_equal True · csr_equal False · bytes_equal False · 받치는 주장 = 가중 그래프 같음 하나 (조립 바이트 같음 아님)
  K2  완전히 같은 입력 둘 → 둘 다 같음 · 주장 둘
  K3  조립 미완료 (조기 반환 사유) · main 지문 null · 빈 그래프 지문 → 못 견줌 (주장 없음 · 칸 None · 사유)
  K4  DOF 원 번호 목록이 다름 (나머지 같음) → dof_equal False · bytes_equal False · 한쪽만 실음 = 한정 사유 글
  K5  조립만 기록 (`run_contract.cjunc_graph_only_record`) — 조기 반환 (null) · 사유 있음 · main null · 빈 그래프 = 양성 근거 아님 · 정상 둘 = 가중 그래프
      같음까지만 (조립 바이트 같음은 말할 수 없다는 사유 글)
⚠ PASS = 비교 함수가 두 주장을 가른다는 증거 · 두 기계 실측 · 풀이 · σ 와 무관.

  python3 scripts/test_cjunc_asm_compare.py
"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import run_contract as _RCG                                # noqa: E402
_RCG.drop_git_env()                                        # 이 시험 프로세스와 그 자식은 부르는 쪽 GIT_* 를 물려받지 않는다 (test_git_env_isolation G6 꼴)

import carbon_junction as CJ                               # noqa: E402

try:
    import cjunc_asm_compare as AC                         # noqa: E402
    AC_ERR = None
except ImportError as _e:                                  # 고치기 전 판 = 모듈 없음
    AC, AC_ERR = None, _e

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:600]})' if why != '' else ''))
    return bool(cond)


def assemble(gs):
    """판정문 반례의 조립 — 실제 `CjuncAssembler._assemble` (생성자를 건너뛰고 칸만 채운다 · 두 노드 · 판 결합 아래 0 · 위 1 · 병렬 간선 = gs)."""
    a = CJ.CjuncAssembler.__new__(CJ.CjuncAssembler)
    z = np.zeros(0, np.int64)
    a.plan = {'mode': z, 'g_code': np.zeros(0)}
    a.reg = {'subedges': {'port_i': z, 'port_j': z}, 'positions': {}, 'cell_lin': z}
    a.pos_dof = z
    a.cells_lin = np.arange(2)
    a.n_total = 2
    a.n_cells = 2
    a.tomb = {}
    a.n_unreg_fused = 0
    a.n_self_fused = 0
    k = len(gs)
    a.E = [(np.zeros(k, np.int64), np.ones(k, np.int64), np.asarray(gs, np.float64), np.zeros(k, np.int64), np.ones(k), np.ones(k),
            np.ones(k, np.int64), np.ones(k, np.int64), np.full(k, -1, np.int64), np.zeros(k, bool))]
    out, st = a._assemble(np.array([0]), np.array([1.0]), np.array([1]), np.array([1.0]), graph_fp=True)
    return out, st.get('graph_fp')


def main():
    t = 2.0 ** -53
    o1, f1 = assemble([1.0, t, t])
    o2, f2 = assemble([t, t, 1.0])
    off1 = [float(x).hex() for x in o1['L'].data[[1, 2]]]
    off2 = [float(x).hex() for x in o2['L'].data[[1, 2]]]
    chk('K1a 판정문 반례 재현 (실제 _assemble · 비교 모듈 없이) — 병렬 간선 차례만 다른 두 계: 가중 그래프 지문 같음 (64 hex) · CSR 비대각 '
        '-0x1.0000000000000p+0 ↔ -0x1.0000000000001p+0 (1 ulp) · b · indices · indptr 바이트 같음',
        isinstance(f1, str) and len(f1) == 64 and f1 == f2 and off1 == ['-0x1.0000000000000p+0'] * 2 and off2 == ['-0x1.0000000000001p+0'] * 2
        and o1['b'].tobytes() == o2['b'].tobytes() and o1['L'].indices.tobytes() == o2['L'].indices.tobytes()
        and o1['L'].indptr.tobytes() == o2['L'].indptr.tobytes(), (f1, f2, off1, off2))
    if AC is None:
        chk('K0 cjunc_asm_compare 모듈이 있다', False, f'고치기 전 판 — {AC_ERR}')
        print(f'\n== test_cjunc_asm_compare: {_ok}/{_ok + len(_fail)} PASS')
        return 1
    r1, r2 = AC.assembly_record(o1, f1, dof_ids=[0, 1]), AC.assembly_record(o2, f2, dof_ids=[0, 1])
    c = AC.compare_assembly(r1, r2)
    chk('K1 같은 반례를 비교 함수로 → graph_equal True · csr_equal False · rhs · dof 같음 · bytes_equal False · 주장 = 가중 그래프 같음 하나 (RCPX-03)',
        c['comparable'] is True
        and c['graph_equal'] is True and c['csr_equal'] is False and c['rhs_equal'] is True and c['dof_equal'] is True
        and c['bytes_equal'] is False and c['claims'] == [AC.CLAIM_GRAPH] and r1['csr']['indices'] == r2['csr']['indices']
        and r1['csr']['indptr'] == r2['csr']['indptr'], (f1 == f2, off1, off2, c))
    o3, f3 = assemble([1.0, t, t])
    c2 = AC.compare_assembly(r1, AC.assembly_record(o3, f3, dof_ids=[0, 1]))
    chk('K2 완전히 같은 입력 둘 → graph · csr · rhs · dof 같음 · bytes_equal True · 주장 둘 (가중 그래프 같음 · 조립 바이트 같음)',
        c2['comparable'] and c2['bytes_equal'] is True and c2['claims'] == [AC.CLAIM_GRAPH, AC.CLAIM_BYTES], c2)
    ef = AC.empty_graph_fp()
    bad = {'조립 미완료 (조기 반환)': AC.assembly_record({'reason': 'no_through_component'}, f1),
           'main 지문 null': AC.assembly_record(o1, None, dof_ids=[0, 1]),
           '빈 그래프 지문': AC.assembly_record(o1, ef, dof_ids=[0, 1])}
    res3 = {k: AC.compare_assembly(r1, v) for k, v in bad.items()}
    chk('K3 조립 미완료 · main 지문 null · 빈 그래프 지문 → 못 견줌 (comparable False · 칸 None · 주장 없음 · 사유 = 양성 근거 아님)',
        all(r['comparable'] is False and r['graph_equal'] is None and r['bytes_equal'] is None and r['claims'] == []
            and any('양성 근거 아님' in w for w in r['why']) for r in res3.values()) and bad['조립 미완료 (조기 반환)']['complete'] is False
        and isinstance(ef, str) and len(ef) == 64, res3)
    c4 = AC.compare_assembly(r1, AC.assembly_record(o3, f3, dof_ids=[1, 0]))
    c5 = AC.compare_assembly(r1, AC.assembly_record(o3, f3))
    chk('K4 DOF 원 번호 목록 다름 (나머지 같음) → dof_equal False · bytes_equal False · 주장 = 가중 그래프 같음만 · 한쪽만 실음 = 같음으로 두되 한정 사유 글',
        c4['dof_equal'] is False and c4['bytes_equal'] is False and c4['claims'] == [AC.CLAIM_GRAPH]
        and c5['bytes_equal'] is True and any('DOF 원 번호' in w for w in c5['why']), (c4, c5))
    env_u = _RCG.env_unit_now()
    cost = {'seconds_step3': 1.0, 'seconds_assemble': 0.5, 'peak_rss_kb': None}

    def go(graphs, reason=None):
        import ca_ext_svcf as SV
        bind = dict.fromkeys(SV.BIND_FIELDS)
        bind['bind_version'] = 'v'
        return _RCG.cjunc_graph_only_record({'cjunc_graphs': graphs, 'reason': reason, 'bind': bind}, env_unit=env_u, cost=cost)
    import ca_ext_svcf as SV
    rule = SV.GRAPH_FP_RULE
    good = go({'rule': rule, 'main': f1, 'lower': None, 'upper': None})
    probs = {'조기 반환 (null)': AC.graph_only_positive_problem(go(None, reason='no_through_component')),
             '사유 있음': AC.graph_only_positive_problem(go({'rule': rule, 'main': f1, 'lower': None, 'upper': None}, reason='x')),
             'main null': AC.graph_only_positive_problem(go({'rule': rule, 'main': None, 'lower': None, 'upper': None})),
             '빈 그래프': AC.graph_only_positive_problem(go({'rule': rule, 'main': ef, 'lower': None, 'upper': None}))}
    cg = AC.compare_graph_only(good, go({'rule': rule, 'main': f2, 'lower': None, 'upper': None}))
    chk('K5 조립만 기록 — 조기 반환 (null) · 사유 있음 · main null · 빈 그래프 = 양성 근거 아님 (사유 글) · 정상 = 문제 없음 · 정상 둘 비교 = 가중 그래프 같음만 '
        '(조립 바이트 같음은 이 기록으로 말할 수 없다는 사유 글 · RCPX-03)',
        all(isinstance(v, str) and v for v in probs.values()) and AC.graph_only_positive_problem(good) is None and cg['comparable']
        and cg['graph_equal'] is True and cg['claims'] == [AC.CLAIM_GRAPH] and any('조립 바이트' in w for w in cg['why']), (probs, cg))
    print(f'\n== test_cjunc_asm_compare: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('FAIL: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

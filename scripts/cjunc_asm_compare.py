#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② Q12 두 기계 조립 비교 설계 (1저자 11-12 Q10 · 11-13 Codex 반박 1/2 RCPX-03) — '가중 그래프 같음' 과 '조립 바이트 같음' 을 가른다.

왜: 정규 가중 그래프 지문 (`carbon_junction.solved_graph_fp`) 은 쌍마다 병렬 간선 전도도를 **정확 합** (차례 무관 · 반올림 없음) 으로 싣는다.  실제 조립
(`CjuncAssembler._assemble` 의 COO → CSR) 은 같은 쌍의 항을 부동소수로 차례대로 더한다 → 차례가 다르면 지문은 같아도 CSR 바이트가 다를 수 있다.
판정문 반례 (실제 `_assemble` · 두 노드 · 병렬 간선 셋): 전도도 차례 [1, 2^-53, 2^-53] ↔ [2^-53, 2^-53, 1] = 지문 같음 · CSR 비대각 원소
-0x1.0000000000000p+0 ↔ -0x1.0000000000001p+0 (1 ulp) · b · DOF · indices · indptr 같음.  ⇒ 지문 같음에서 CSR 비트 같음을 끌어내지 않는다.

이 모듈 = **개발 설계 도구** — 생산 · 봉인 원천 (`RunnerGraphSource`) · payload 가 부르지 않는다 · 실제 실행 없음 (Q12 두 기계 런 = 1저자 결정 · 결과 전에
개발 탐침 원장 줄 (코드 · 입력 · 모드 · 읽지 않을 값 · 기대 · 실패 보고) 을 먼저 커밋 — 판정문 Q12 권고).  두 주장:
  · 가중 그래프 같음 = 두 기록의 main 지문 (64 hex · 빈 그래프 아님) 이 같다 — 조립만 기록 (`run_contract.cjunc_graph_only_record`) 으로 말할 수 있는 것은
    여기까지 (`graph_only_positive_problem` · `compare_graph_only`) · 조기 반환 (cjunc_graphs null) · 빈 main = 양성 근거 아님
  · 조립 바이트 같음 = 위 + 최종 CSR (형식 · 모양 · dtype · data · indices · indptr 바이트) + RHS b + DOF 차례 (dof 수 · 판 결합 Ab · gb · At · gt 바이트 ·
    원 dof 번호 목록 — 둘 다 실었을 때만 대조) 가 같다 — `assembly_record` (조립 출력 → 기록) · `compare_assembly`
⚠ 한정: DOF 원 번호 목록을 싣지 않은 기록끼리는 'DOF 차례 = 지문의 dof 집합 + 같은 코드의 정렬 번호 매김' 에 기댄다 (같은 코드 신원 = 따로 대조할 것) ·
   기록은 그 런의 자기 기록이다 (위조 방지 아님) · 이 비교는 풀이 · σ · 수렴과 무관하다 (조립까지).

  python3 scripts/cjunc_asm_compare.py --compare A.json B.json     # 기록 둘 (assembly_record 꼴 또는 조립만 기록) 을 견줘 JSON 으로 찍는다
"""
import argparse
import hashlib
import json
import re
import sys

import numpy as np

SCHEMA = 'cjunc-asm-record-v1'
CLAIM_GRAPH = 'weighted_graph_equal'
CLAIM_BYTES = 'assembly_bytes_equal'
_HEX64 = re.compile(r'[0-9a-f]{64}')
_EMPTY = []


def empty_graph_fp():
    """빈 그래프 (dof · 간선 · 판 결합 없음) 의 정규 지문 — 같은 함수 (`carbon_junction.solved_graph_fp`) 로 센다 (사본 없음 · 한 번만)."""
    if not _EMPTY:
        import carbon_junction as CJ
        z = np.zeros(0, np.int64)
        f = np.zeros(0, np.float64)
        _EMPTY.append(CJ.solved_graph_fp(z, z, z, f, z, f, z, f))
    return _EMPTY[0]


def _hex64(x):
    return isinstance(x, str) and _HEX64.fullmatch(x) is not None


def _arr(a):
    """배열 → {dtype · shape · sha256 (dtype · 모양 · C 차례 바이트)} (값 비교 아님 · 바이트 비교)."""
    a = np.asarray(a)
    h = hashlib.sha256()
    h.update(a.dtype.str.encode('ascii'))
    h.update(repr(tuple(int(x) for x in a.shape)).encode('ascii'))
    h.update(np.ascontiguousarray(a).tobytes())
    return {'dtype': a.dtype.str, 'shape': [int(x) for x in a.shape], 'sha256': h.hexdigest()}


def _count(value, positive=False):
    return type(value) is int and (1 if positive else 0) <= value <= 2**63 - 1


def _descriptor_problem(value, kinds, length=None):
    if not isinstance(value, dict) or not _hex64(value.get('sha256')):
        return 'array descriptor/hash'
    shape = value.get('shape')
    if type(shape) is not list or len(shape) != 1 or not _count(shape[0]):
        return 'array shape'
    if length is not None and shape != [length]:
        return 'array length'
    try:
        dtype = np.dtype(value.get('dtype')) if type(value.get('dtype')) is str else None
    except (TypeError, ValueError):
        dtype = None
    if dtype is None or dtype.hasobject or dtype.kind not in kinds:
        return 'array dtype'
    return None


def _source_array(value, kinds, length=None):
    if value is None:
        raise ValueError('missing array')
    arr = np.asarray(value)
    if arr.dtype.hasobject or arr.dtype.kind not in kinds or arr.ndim != 1:
        raise ValueError('array dtype/shape')
    if length is not None and len(arr) != length:
        raise ValueError('array length')
    if not np.all(np.isfinite(arr)):
        raise ValueError('nonfinite array')
    return arr


def assembly_record(asm_out, graph_fp=None, dof_ids=None):
    """조립 출력 (`CjuncAssembler.build` · `_assemble` 의 첫 반환 = {'L', 'b', 'Ab', 'gb', 'At', 'gt', 'n_dof', …} 또는 {'reason'}) → 조립 기록.
    graph_fp = 그 계의 main 정규 가중 그래프 지문 (`build(..., graph_fp=True)` 뒤 `self.graph_fp`) · dof_ids = 조립 번호 차례의 원 dof 번호 (없으면 None ·
    한정).  조기 반환 · L 없음 = complete False (양성 근거 아님)."""
    o = asm_out if isinstance(asm_out, dict) else {}
    L = o.get('L')
    rec = {'schema': SCHEMA, 'complete': False, 'reason': None, 'graph_fp': graph_fp, 'csr': None, 'rhs': None, 'dof': None}
    if 'reason' in o or L is None:
        rec['reason'] = str(o.get('reason') or '조립 출력 없음')
        return rec
    fmt = getattr(L, 'format', None)
    if fmt != 'csr':
        rec['reason'] = f'조립 행렬 꼴 {fmt!r} (csr 이어야)'
        return rec
    # Check original types/shapes before any integer conversion or hashing.
    try:
        n = o.get('n_dof')
        if isinstance(n, np.integer) and not isinstance(n, np.bool_):
            n = int(n)
        if not _count(n, positive=True) or tuple(L.shape) != (n, n):
            raise ValueError('dof count/shape')
        data = _source_array(L.data, 'f', int(L.nnz))
        indices = _source_array(L.indices, 'iu', len(data))
        indptr = _source_array(L.indptr, 'iu', n + 1)
        if len(data) == 0 or indptr[0] != 0 or indptr[-1] != len(data) or np.any(indptr[1:] < indptr[:-1]):
            raise ValueError('CSR pointer/empty')
        if np.any(indices < 0) or np.any(indices >= n):
            raise ValueError('CSR index')
        _source_array(o.get('b'), 'f', n)
        for idx, weight in (('Ab', 'gb'), ('At', 'gt')):
            aa = _source_array(o.get(idx), 'iu')
            _source_array(o.get(weight), 'f', len(aa))
            if np.any(aa < 0) or np.any(aa >= n):
                raise ValueError('boundary index')
        ids = None
        if dof_ids is not None:
            if isinstance(dof_ids, (list, tuple)) and any(
                    not isinstance(x, (int, np.integer)) or isinstance(x, (bool, np.bool_)) for x in dof_ids):
                raise ValueError('DOF id type')
            ids = _source_array(dof_ids, 'iu', n)
            if np.any(ids < 0) or any(int(x) > 2**63 - 1 for x in ids) or len(np.unique(ids)) != n:
                raise ValueError('DOF ids range/duplicate')
    except (ValueError, TypeError, OverflowError, AttributeError) as exc:
        rec['reason'] = 'invalid assembly input: ' + str(exc)
        return rec
    rec['complete'] = True
    rec['csr'] = {'format': 'csr', 'shape': [int(x) for x in L.shape], 'nnz': int(L.nnz), 'sorted_indices': bool(L.has_sorted_indices),
                  'data': _arr(L.data), 'indices': _arr(L.indices), 'indptr': _arr(L.indptr)}
    rec['rhs'] = _arr(o.get('b'))
    rec['dof'] = {'n': int(o.get('n_dof')), 'Ab': _arr(o.get('Ab')), 'gb': _arr(o.get('gb')), 'At': _arr(o.get('At')), 'gt': _arr(o.get('gt')),
                  'ids': (None if ids is None else _arr(ids.astype(np.int64)))}
    return rec


def _record_problem(r):
    if not isinstance(r, dict) or r.get('schema') != SCHEMA:
        return '조립 기록 꼴 (schema) 이 아니다'
    if r.get('complete') is not True or r.get('reason') is not None:
        return f'조립 미완료 ({r.get("reason")}) — 양성 근거 아님'
    if not _hex64(r.get('graph_fp')):
        return 'main 그래프 지문이 없다 (null · 꼴 아님) — 양성 근거 아님'
    if r['graph_fp'] == empty_graph_fp():
        return 'main 그래프 = 빈 그래프 — 양성 근거 아님'
    dof, csr = r.get('dof'), r.get('csr')
    if not isinstance(dof, dict) or not isinstance(csr, dict):
        return 'missing dof/CSR — 양성 근거 아님'
    n, nnz = dof.get('n'), csr.get('nnz')
    if not _count(n, True) or not _count(nnz, True):
        return 'invalid dof/nnz — 양성 근거 아님'
    shape = csr.get('shape')
    if (type(shape) is not list or len(shape) != 2 or not all(_count(x, True) for x in shape)
            or shape != [n, n] or csr.get('format') != 'csr' or type(csr.get('sorted_indices')) is not bool):
        return 'invalid CSR shape/format — 양성 근거 아님'
    checks = [(csr.get('data'), 'f', nnz), (csr.get('indices'), 'iu', nnz),
              (csr.get('indptr'), 'iu', n + 1), (r.get('rhs'), 'f', n)]
    for idx, weight in (('Ab', 'gb'), ('At', 'gt')):
        if _descriptor_problem(dof.get(idx), 'iu'):
            return 'invalid boundary descriptor — 양성 근거 아님'
        checks.append((dof.get(weight), 'f', dof[idx]['shape'][0]))
    if 'ids' not in dof:
        return 'missing DOF ids field — 양성 근거 아님'
    if dof['ids'] is not None:
        checks.append((dof['ids'], 'iu', n))
    if any(_descriptor_problem(value, kinds, length) for value, kinds, length in checks):
        return 'invalid array descriptor — 양성 근거 아님'
    return None


def compare_assembly(a, b):
    """조립 기록 둘 → {'comparable' · 'graph_equal' · 'csr_equal' · 'rhs_equal' · 'dof_equal' · 'bytes_equal' · 'claims' · 'why'}.
    claims = 이 비교가 받치는 주장 (가중 그래프 같음 · 조립 바이트 같음 — 따로) · 못 견줌 (미완료 · 빈 main · 꼴) = 칸 None · claims 빈 목록."""
    why = []
    for nm, r in (('a', a), ('b', b)):
        p = _record_problem(r)
        if p:
            why.append(f'{nm}: {p}')
    out = {'comparable': not why, 'graph_equal': None, 'csr_equal': None, 'rhs_equal': None, 'dof_equal': None, 'bytes_equal': None,
           'claims': [], 'why': why}
    if why:
        return out
    out['graph_equal'] = a['graph_fp'] == b['graph_fp']
    out['csr_equal'] = a['csr'] == b['csr']
    out['rhs_equal'] = a['rhs'] == b['rhs']
    da, db = dict(a['dof']), dict(b['dof'])
    ia, ib = da.pop('ids', None), db.pop('ids', None)
    out['dof_equal'] = da == db and (ia == ib if (ia is not None and ib is not None) else True)
    if ia is None or ib is None:
        why.append('DOF 원 번호 목록을 한쪽 이상이 싣지 않았다 — DOF 차례 = 지문의 dof 집합 + 같은 코드의 정렬 번호 매김에 기댄다 (한정 · 코드 신원 따로 대조)')
    if not out['graph_equal']:
        why.append('main 그래프 지문이 다르다')
    if out['graph_equal'] and not out['csr_equal']:
        why.append('가중 그래프는 같은데 CSR 바이트가 다르다 (병렬 항 합산 차례 등 · 지문으로 CSR 비트를 말하지 않는다 · RCPX-03)')
    out['bytes_equal'] = bool(out['graph_equal'] and out['csr_equal'] and out['rhs_equal'] and out['dof_equal'])
    if out['graph_equal']:
        out['claims'].append(CLAIM_GRAPH)
    if out['bytes_equal']:
        out['claims'].append(CLAIM_BYTES)
    return out


def graph_only_positive_problem(rec):
    """조립만 기록 (`run_contract.cjunc_graph_only_record`) → '가중 그래프 같음' 의 양성 근거가 될 수 없는 사유 | None.  꼴 (`cjunc_graph_only_problem`) ·
    조기 반환 (cjunc_graphs null) · 사유 있음 · main null · main = 빈 그래프 = 아님.  이 기록은 CSR 을 싣지 않는다 → '조립 바이트 같음' 근거가 될 수 없다."""
    import run_contract as RC
    p = RC.cjunc_graph_only_problem(rec)
    if p:
        return p
    g = rec.get('cjunc_graphs')
    if g is None:
        return f'조립 전 조기 반환 (cjunc_graphs null · 사유 {rec.get("reason")!r}) — 양성 근거 아님'
    if rec.get('reason') is not None:
        return f'조립 사유 {rec.get("reason")!r} — 양성 근거 아님'
    if not _hex64(g.get('main')):
        return 'main 그래프 지문 null — 양성 근거 아님'
    if g['main'] == empty_graph_fp():
        return 'main 그래프 = 빈 그래프 — 양성 근거 아님'
    return None


def compare_graph_only(a, b):
    """조립만 기록 둘 → {'comparable' · 'graph_equal' · 'claims' · 'why'} — 받치는 주장 = 가중 그래프 같음 뿐 (조립 바이트 같음 아님)."""
    why = []
    for nm, r in (('a', a), ('b', b)):
        p = graph_only_positive_problem(r)
        if p:
            why.append(f'{nm}: {p}')
    out = {'comparable': not why, 'graph_equal': None, 'claims': [], 'why': why}
    if not why:
        out['graph_equal'] = a['cjunc_graphs']['main'] == b['cjunc_graphs']['main']
        if out['graph_equal']:
            out['claims'].append(CLAIM_GRAPH)
        why.append('조립만 기록은 CSR · RHS · DOF 차례를 싣지 않는다 — 조립 바이트 같음은 이 비교로 말할 수 없다 (RCPX-03)')
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description='Rint ② Q12 두 기계 조립 비교 (개발 설계 도구 · 실제 실행 없음 · 기록 둘을 견준다)')
    ap.add_argument('--compare', nargs=2, metavar=('A', 'B'), required=True, help='기록 JSON 둘 (assembly_record 꼴 또는 조립만 기록)')
    a = ap.parse_args(argv)
    recs = [json.load(open(p, encoding='utf-8')) for p in a.compare]
    if all(isinstance(r, dict) and r.get('schema') == SCHEMA for r in recs):
        res = compare_assembly(*recs)
    else:
        res = compare_graph_only(*recs)
    print(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True))
    return 0 if res['comparable'] else 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RIMP 수정 — iface 끔 (`solve_sigma_z(iface=None)`) 비트 같음 재확인 (수치 OFF 16 사례 · 증거 생성 전용 · 시험 레인 밖).

같은 16 사례 (Codex 10-14 판정문 §1-2 의 OFF 비교와 같은 격자 — h 0.1 · 0.2 × 입자 순서 둘 × 브리지 0.24 · 기본 × r1 끔 · 켬) 를
두 step3_sigma 모듈로 풀어 rasterize (sid · pid) · 전체 반환 dict (키 · 값 · 배열 dtype · 모양 · 바이트) 를 비교한다.
두 쪽 다 같은 직접 풀이 (`_solve_cg` → scipy spsolve) — CG 허용오차가 끼지 않게 (작은 픽스처 대조 · 생산 경로 아님).
⚠ 16 사례 통과는 전 입력 공간의 동등성 증명이 아니다 (판정문 §1-2 한정 그대로).

  python3 docs/reviews/rint_g2_impl_fix_evidence_20261015/off_compat_16.py --old OLD.py --new scripts/step3_sigma.py [--json OUT]

OLD = 비교할 옛 판 파일 (git show <커밋>:scripts/step3_sigma.py 로 꺼낸 사본).
"""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import numpy as np                                            # noqa: E402
from scipy.sparse.linalg import spsolve                       # noqa: E402


def _module(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    m._solve_cg = lambda L, b: (spsolve(L.tocsc(), b), 0)
    return m


def _quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def _eq(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, np.ndarray):
        return a.dtype == b.dtype and a.shape == b.shape and a.tobytes() == b.tobytes()
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(_eq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(_eq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a.hex() == b.hex()
    return a == b


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--old', required=True)
    ap.add_argument('--new', required=True)
    ap.add_argument('--json', default='')
    a = ap.parse_args(argv)
    old, new = _module('s3_old', a.old), _module('s3_new', a.new)
    c = np.array([[1., 1., 1.], [1., 1., 2.9]]); r = np.ones(2); t = np.array([2, 1])
    cases = []
    for h in (0.1, 0.2):
        for perm in ([0, 1], [1, 0]):
            for bridge in (0.24, None):
                for rint in (None, {(1, 2): 1e-3}):
                    got = []
                    for m in (old, new):
                        sid, pid = _quiet(m.rasterize, c[perm], r[perm], t[perm], None, None, (0, 0, 0), (2, 2, 3.9), h, bridge_um=bridge)
                        sig = m.electronic_sigma_table(.01, .005, 100., 10., 250.)
                        res = _quiet(m.solve_sigma_z, sid, sig, h, return_field=True, z_bot_um=0, z_top_um=3.9, rint=rint, pid=pid)
                        got.append((sid, pid, res))
                    cases.append({'h': h, 'order': perm, 'bridge': bridge, 'r1_on': bool(rint),
                                  'all_keys_values_array_bytes_equal': _eq(got[0], got[1]), 'sigma': got[1][2]['sigma_eff']})
    sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()                # noqa: E731
    out = {'old_source_sha256': sha(a.old), 'new_source_sha256': sha(a.new), 'solver': 'same spsolve small-fixture control (both sides)',
           'n_cases': len(cases), 'n_equal': int(sum(x['all_keys_values_array_bytes_equal'] for x in cases)), 'cases': cases}
    txt = json.dumps(out, indent=1)
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            fh.write(txt + '\n')
    print(txt)
    return 0 if out['n_equal'] == out['n_cases'] else 1


if __name__ == '__main__':
    sys.exit(main())

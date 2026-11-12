#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② Q11 (1저자 11-12) — STEP3 GPU 길 Jacobi 전처리의 **표현** (dia_matrix → 벡터 곱 연산자) · 시험 먼저 (규율 ② · GPU 없음).

무엇을 보나 (가짜 cupy = numpy · scipy 로 흉내 · 이 시험 안에서만 · sys.modules 에 끼웠다가 되돌린다):
  G1  `_solve_cg` GPU 길이 cg 에 넘기는 M = 벡터 곱 연산자 (LinearOperator) — 고치기 전 = dia_matrix (`cxs.diags`) 라 실패
  G1r 같은 것을 `rtol=` 호출 길 (새 cupy 서명 · `tol=` TypeError 뒤 다시 부름) 에서
  G2  연산자 matvec = (1/diag) * r 와 바이트 같음 · 늘 새 배열 (입력 · 앞 호출과 메모리 공유 없음 — cupyx cg 첫 반복 `p = z` 별칭) · 입력 그대로 ·
      dtype float64 를 넘겨 dtype 탐침 호출 없음
  G3  옛 판 (`11a794674` 의 `_solve_cg` = A 꼴) ↔ 지금 판 (C 꼴): 해 바이트 · info · 반복 수 (LAST_CG) · LAST_BACKEND 같음 —
      침대 셋 · `tol=` / `rtol=` 두 호출 길 · x0 없음 / 있음 (이어 풀기 ⓒ = rtol 1e-14) · 증서 켬 (callback) / 끔 · 수렴까지 (rtol 1e-12) · maxiter 도달
  G4  부호 있는 0 (b 에 −0.0) — 반복 · info · 값 같음 · 바이트가 다르면 값 0 자리에서만 (dia→CSR 경로의 +0 합 시작 ↔ 원소 곱 −0 · 생산 b 는 ≥ +0)
  G5  CPU 길 (GPU_SOLVE 끔) — 옛 판과 바이트 같음 · 가짜 cg 를 부르지 않는다
  G6  GPU 길 불러오기 실패 → CPU 폴백 — 옛 판과 같음 (해 · LAST_BACKEND 사유 글) · REQUIRE_GPU 면 둘 다 SystemExit
  G7  `solve_sigma_z` 끝-끝 (가짜 GPU · 증서 켬 · rtol 1e-12) — 옛 판과 결과 dict (σ 비트 · 증서 · 반복 수 · 키 집합) · LAST_BACKEND 같음 = 매니페스트 키 변화 0
가짜 cg = cupy 12.3.0 `cupyx/scipy/sparse/linalg/_iterative.py` `cg` (14–91 줄) · `_make_system` (301–349 줄) 의 동작 그대로 옮긴 것:
  A = csr → spMV · M = csr → spMV · 그 밖 희소 행렬 → MatrixLinearOperator → matvec = (M.tocsc().tocsr() @ x.reshape(-1, 1)).reshape(-1)
  (cupy dia 의 `__mul__` = `tocsr()` = `tocsc().tocsr()` · `_dia.py` 140–190) · LinearOperator → 그 matvec · 정지 = resid ≤ max(atol, tol·‖b‖) ·
  첫 반복 `p = z` (별칭).  ⚠ 가짜는 GPU 의 반올림을 흉내 내지 않는다 — A ↔ C 를 **같은 산술**에서 견줄 뿐이다 (GPU 의 비트 같음 = 확인 블록).

  python3 scripts/test_step3_gpu_precond.py
"""
import contextlib
import importlib.util
import inspect
import io
import os
import subprocess
import sys
import tempfile
import types

import numpy as np
from scipy import sparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
#: 고치기 전 판 (Q11 · Q2 묶음의 바탕 · 이 판의 GPU 길 = dia_matrix 전처리)
BASE_COMMIT = '11a794674'

import step3_sigma as S3                                   # noqa: E402

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return bool(cond)


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def load_base():
    src = subprocess.run(['git', '-C', ROOT, 'show', f'{BASE_COMMIT}:scripts/step3_sigma.py'], capture_output=True, check=True).stdout
    d = tempfile.mkdtemp(prefix='s3base_gp_')
    p = os.path.join(d, 'step3_sigma_base_gp.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('step3_sigma_base_gp', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    #  scipy < 1.12 (kgy 판) 이면 지금 판의 CPU `cg` = `_cg_v112` — 기반 모듈에도 같은 cg (CPU 길 비교가 코드 경로만 보게 · SELF-133 꼴)
    if getattr(S3, 'cg', None) is getattr(S3, '_cg_v112', 0) and hasattr(m, '_solve_cg'):
        m.cg = S3.cg
    return m


# ═════════════════════════ 가짜 cupy (cupy 12.3.0 동작) ═════════════════════════
REC = {}


class FakeLinearOperator:
    """cupyx `LinearOperator` (= `_CustomLinearOperator`) 의 동작 — dtype 이 없으면 0 벡터로 matvec 를 한 번 불러 정한다 (`_init_dtype`) ·
    matvec = 모양 검사 → 사용자 함수 → (N,) / (N,1) 로 모양 맞춤."""

    def __init__(self, shape, matvec, rmatvec=None, matmat=None, dtype=None, rmatmat=None):
        self.shape = tuple(int(x) for x in shape)
        self._impl = matvec
        REC.setdefault('linop_made', []).append({'dtype_given': dtype is not None})
        self.dtype = None if dtype is None else np.dtype(dtype)
        if self.dtype is None:
            REC['dtype_probe_calls'] = REC.get('dtype_probe_calls', 0) + 1
            self.dtype = self.matvec(np.zeros(self.shape[-1])).dtype

    def matvec(self, x):
        M, N = self.shape
        if x.shape != (N,) and x.shape != (N, 1):
            raise ValueError('dimension mismatch')
        y = self._impl(x)
        if x.ndim == 1:
            y = y.reshape(M)
        elif x.ndim == 2:
            y = y.reshape(M, 1)
        return y


def _psolve_of(M):
    if M is None:
        return lambda r: r
    if sparse.issparse(M) and M.format == 'csr':
        return lambda r: M @ r                                   # cupy 빠른 spMV
    if sparse.issparse(M):                                       # cupy MatrixLinearOperator → dot → tocsr() = tocsc().tocsr() 매번
        return lambda r: (M.tocsc().tocsr() @ r.reshape(-1, 1)).reshape(-1)
    if isinstance(M, FakeLinearOperator):
        return M.matvec
    raise TypeError(f'가짜 cg: 모르는 M 형 {type(M).__name__}')


def _cg_core(A, b, x0, tol, atol, maxiter, M, callback):
    REC.setdefault('M_seen', []).append(M)
    A = sparse.csr_matrix(A)
    n = A.shape[0]
    matvec = (lambda v: A @ v)
    psolve = _psolve_of(M)
    if not (b.shape == (n,) or b.shape == (n, 1)):
        raise ValueError('b has incompatible dimensions')
    b = b.astype(np.float64).ravel()
    x = np.zeros((n,), np.float64) if x0 is None else x0.astype(np.float64).ravel()
    if maxiter is None:
        maxiter = n * 10
    if n == 0:
        return np.empty_like(b), 0
    b_norm = np.linalg.norm(b)
    if b_norm == 0:
        return b, 0
    atol = tol * float(b_norm) if atol is None else max(float(atol), tol * float(b_norm))
    r = b - matvec(x)
    iters = 0
    rho = 0
    resid = None
    while iters < maxiter:
        z = psolve(r)
        rho1 = rho
        rho = np.dot(r, z)
        if iters == 0:
            p = z                                                # ★ 별칭 (cupyx 72 줄)
        else:
            beta = rho / rho1
            p = z + beta * p
        q = matvec(p)
        alpha = rho / np.dot(p, q)
        x = x + alpha * p
        r = r - alpha * q
        iters += 1
        if callback is not None:
            callback(x)
        resid = np.linalg.norm(r)
        if resid <= atol:
            break
    info = 0
    if iters == maxiter and not (resid <= atol):
        info = iters
    return x, info


def fake_cg_tol(A, b, x0=None, tol=1e-5, maxiter=None, M=None, callback=None, atol=None):
    """cupy 12.3.0 서명 (`tol=` · `rtol=` 없음)."""
    REC['calls'] = REC.get('calls', 0) + 1
    return _cg_core(A, b, x0, tol, atol, maxiter, M, callback)


def fake_cg_rtol(A, b, x0=None, **kw):
    """새 cupy 꼴 서명 (`rtol=` · `atol=` · `tol=` 없음 → 생산 코드는 TypeError 뒤 다시 부른다).  서명 불일치를 흉내 내되 시도 수를 센다
    (실제 함수라면 서명 불일치 TypeError 는 본문에 들어오기 전에 난다 — 그래서 `calls` = 본문 부름 · `attempts` = 부른 횟수)."""
    REC['attempts'] = REC.get('attempts', 0) + 1
    unk = sorted(k for k in kw if k not in ('rtol', 'atol', 'maxiter', 'M', 'callback'))
    if unk:
        raise TypeError(f"cg() got an unexpected keyword argument {unk[0]!r}")
    REC['calls'] = REC.get('calls', 0) + 1
    return _cg_core(A, b, x0, kw.get('rtol', 1e-5), kw.get('atol', 0.0), kw.get('maxiter'), kw.get('M'), kw.get('callback'))


@contextlib.contextmanager
def fake_cupy(variant='tol', fail_linalg=False):
    """sys.modules 에 가짜 cupy · cupyx 를 끼운다 (나올 때 되돌린다).  fail_linalg = cupyx.scipy.sparse.linalg 불러오기 실패 (폴백 길)."""
    REC.clear()
    names = ('cupy', 'cupyx', 'cupyx.scipy', 'cupyx.scipy.sparse', 'cupyx.scipy.sparse.linalg')
    old = {k: sys.modules.get(k) for k in names}
    cp = types.ModuleType('cupy')
    cp.asarray = lambda a, dtype=None: np.array(a, dtype=dtype, copy=True)   # 기기 사본 (늘 새 배열)
    cp.asnumpy = lambda a: np.array(a, copy=True)
    cx = types.ModuleType('cupyx')
    cxsc = types.ModuleType('cupyx.scipy')
    cxs = types.ModuleType('cupyx.scipy.sparse')
    cxs.csr_matrix = lambda a: sparse.csr_matrix(a, copy=True)
    cxs.diags = lambda d, offsets=0, shape=None, format=None, dtype=None: sparse.diags(d, offsets, shape=shape, format=format, dtype=dtype)
    cx.scipy, cxsc.sparse = cxsc, cxs
    mods = {'cupy': cp, 'cupyx': cx, 'cupyx.scipy': cxsc, 'cupyx.scipy.sparse': cxs}
    if not fail_linalg:
        cxl = types.ModuleType('cupyx.scipy.sparse.linalg')
        cxl.cg = fake_cg_tol if variant == 'tol' else fake_cg_rtol
        cxl.LinearOperator = FakeLinearOperator
        cxs.linalg = cxl
        mods['cupyx.scipy.sparse.linalg'] = cxl
    try:
        for k in names:
            sys.modules.pop(k, None)
        sys.modules.update(mods)
        yield REC
    finally:
        for k in names:
            sys.modules.pop(k, None)
            if old[k] is not None:
                sys.modules[k] = old[k]


@contextlib.contextmanager
def knobs(mods, gpu=True, cert=True, rtol=1e-12, maxiter=None, require=False):
    saved = [(m, m.GPU_SOLVE, m.CONV_CERT, m.CG_RTOL, m.CG_MAXITER, m.REQUIRE_GPU) for m in mods]
    try:
        for m in mods:
            m.GPU_SOLVE, m.CONV_CERT, m.CG_RTOL, m.REQUIRE_GPU = gpu, cert, rtol, require
            if maxiter is not None:
                m.CG_MAXITER = maxiter
        yield
    finally:
        for m, g, c, r, mi, rq in saved:
            m.GPU_SOLVE, m.CONV_CERT, m.CG_RTOL, m.CG_MAXITER, m.REQUIRE_GPU = g, c, r, mi, rq


# ═════════════════════════ 침대 (STEP3 꼴 SPD 계 · b ≥ +0) ═════════════════════════
def system(seed, n=(10, 10, 18), lo=-3.0, hi=4.0, neg_zero=False):
    """격자 셀 = 미지수 · 이웃 6 · 면 g = 조화 평균 (σ 대비 10^(hi−lo)) · 아래 판 φ 1 · 위 판 φ 0 (판 결합 = 대각 · b = g_bot ≥ 0) —
    `solve_sigma_z` 조립과 같은 꼴 (b = np.zeros + 양수).  neg_zero = b 의 0 칸 일부를 −0.0 으로 (부호 있는 0 진단)."""
    rng = np.random.default_rng(seed)
    nx, ny, nz = n
    N = nx * ny * nz
    sig = 10.0 ** rng.uniform(lo, hi, N)
    idx = np.arange(N).reshape(nx, ny, nz)
    rows, cols, vals = [], [], []
    diag = np.zeros(N)
    for ax in range(3):
        a = np.moveaxis(idx, ax, 0)[:-1].ravel()
        c = np.moveaxis(idx, ax, 0)[1:].ravel()
        g = 2.0 * sig[a] * sig[c] / (sig[a] + sig[c])
        rows += [a, c]; cols += [c, a]; vals += [-g, -g]
        np.add.at(diag, a, g); np.add.at(diag, c, g)
    bot, top = idx[:, :, 0].ravel(), idx[:, :, -1].ravel()
    gb, gt = 2.0 * sig[bot], 2.0 * sig[top]
    np.add.at(diag, bot, gb); np.add.at(diag, top, gt)
    b = np.zeros(N)
    np.add.at(b, bot, gb * 1.0)
    if neg_zero:
        z = np.flatnonzero(b == 0.0)
        b[z[::3]] = -0.0
    L = sparse.coo_matrix((np.concatenate(vals + [diag]), (np.concatenate(rows + [np.arange(N)]), np.concatenate(cols + [np.arange(N)]))),
                          shape=(N, N)).tocsr()
    return L, b


def run_solve(mod, L, b, **kw):
    mod.LAST_CG['iters'] = None
    x, info = quiet(mod._solve_cg, L, b, **kw)
    return np.asarray(x), int(info), mod.LAST_CG.get('iters'), dict(mod.LAST_BACKEND)


# ═════════════════════════ 시험 ═════════════════════════
def t_form(variant):
    L, b = system(1)
    with fake_cupy(variant) as rec, knobs([S3]):
        run_solve(S3, L, b)
        seen = list(rec.get('M_seen') or [])
        calls, attempts = rec.get('calls'), rec.get('attempts')
    m = seen[-1] if seen else None
    tag = 'G1' if variant == 'tol' else 'G1r'
    chk(f'{tag} GPU 길 ({variant}= 호출) 이 cg 에 넘기는 M = 벡터 곱 연산자 (LinearOperator · 희소 행렬 아님) — 고치기 전 = dia_matrix',
        isinstance(m, FakeLinearOperator) and not sparse.issparse(m),
        f'M 형 {type(m).__name__} · 부름 {calls} · 본 M {[type(x).__name__ for x in seen]}')
    if variant == 'rtol':
        chk('G1r rtol= 길 — 첫 tol= 부름이 서명 TypeError 로 떨어진 뒤 rtol= 로 다시 부름 (시도 2 · 본문 1 · 본 M 1)',
            attempts == 2 and calls == 1 and len(seen) == 1, f'시도 {attempts} · 본문 {calls} · 본 M {len(seen)}')
    return m


def t_matvec():
    L, b = system(2)
    with fake_cupy('tol') as rec, knobs([S3]):
        run_solve(S3, L, b)
        m = (rec.get('M_seen') or [None])[-1]
        made = list(rec.get('linop_made') or [])
        probes = rec.get('dtype_probe_calls', 0)
    if not isinstance(m, FakeLinearOperator):
        chk('G2 연산자 matvec (고치기 전 = 연산자 아님)', False, f'M 형 {type(m).__name__}')
        return
    dinv = 1.0 / L.diagonal()
    rng = np.random.default_rng(3)
    v = rng.normal(size=L.shape[0])
    v[::7] = 0.0
    v0 = v.copy()
    y1, y2 = m.matvec(v), m.matvec(v)
    want = dinv * v
    chk('G2 matvec = (1/diag)·r 바이트 같음 (같은 수 · 같은 반올림 한 번)', y1.dtype == np.float64 and y1.tobytes() == want.tobytes())
    chk('G2 늘 새 배열 — 입력 · 앞 호출과 메모리 공유 없음 (cupyx cg 첫 반복 p = z 별칭) · 입력 그대로',
        y1 is not v and y2 is not y1 and not np.shares_memory(y1, v) and not np.shares_memory(y1, y2) and v.tobytes() == v0.tobytes())
    chk('G2 dtype float64 를 넘긴다 — dtype 탐침 matvec 호출 없음 · 연산자 하나',
        len(made) == 1 and made[0]['dtype_given'] is True and probes == 0 and m.dtype == np.float64, f'{made} 탐침 {probes}')


def t_equal(base):
    rows = []
    for seed, n, lo, hi in ((11, (8, 8, 14), -3.0, 4.0), (12, (12, 9, 20), -2.0, 2.0), (13, (6, 14, 16), -4.0, 4.0)):
        L, b = system(seed, n, lo, hi)
        for variant in ('tol', 'rtol'):
            for cert in (True, False):
                with fake_cupy(variant), knobs([base, S3], cert=cert, rtol=1e-12):
                    ra = run_solve(base, L, b)
                    rc = run_solve(S3, L, b)
                    rows.append((seed, variant, cert, 'main', ra, rc))
                    xs = ra[0]
                    ra2 = run_solve(base, L, b, x0=xs, rtol=1e-14)            # ⓒ 이어 풀기 (x0 · 조임 rtol)
                    rc2 = run_solve(S3, L, b, x0=xs, rtol=1e-14)
                    rows.append((seed, variant, cert, 'x0', ra2, rc2))
    bad = [(s, v, c, k) for s, v, c, k, ra, rc in rows if not (ra[0].tobytes() == rc[0].tobytes() and ra[1:] == rc[1:])]
    iters = [ra[2] for _s, _v, c, k, ra, _rc in rows if c and k == 'main']
    conv = all(ra[1] == 0 for *_x, ra, _rc in rows)
    chk('G3 옛 판 (A 꼴) ↔ 지금 판 — 해 바이트 · info · 반복 수 · LAST_BACKEND 같음 (침대 셋 · tol= / rtol= · x0 없음 / 있음 (rtol 1e-14) · 증서 켬 / 끔 · 24 짝)',
        not bad and len(rows) == 24, f'다름 {bad[:6]}')
    chk('G3 수렴까지 (rtol 1e-12 · info 0) · 주 풀이 반복 수가 의미 있게 크다 (> 30 · 증서 켬)', conv and all(isinstance(i, int) and i > 30 for i in iters),
        f'반복 {iters}')
    lb = [rc[3] for *_x, _ra, rc in rows if _x[2] is True]
    want_bk = {'requested': 'gpu', 'used': 'gpu', 'fallback_reason': None, 'precond': 'jacobi', 'rtol': 1e-12}
    chk('G3 LAST_BACKEND = {requested gpu · used gpu · 폴백 없음 · precond jacobi · rtol} (글자 그대로 · 새 키 없음)',
        all(x == want_bk for x in lb), f'{lb[:2]}')
    L, b = system(14, (10, 10, 30), -4.0, 4.0)
    with fake_cupy('tol'), knobs([base, S3], cert=True, rtol=1e-14, maxiter=40):
        ra = run_solve(base, L, b)
        rc = run_solve(S3, L, b)
    chk('G3 maxiter 도달 (미수렴) — info = maxiter · 해 바이트 · 반복 수 같음', ra[1] == 40 and rc[1] == 40 and ra[2] == rc[2] == 40
        and ra[0].tobytes() == rc[0].tobytes(), f'{ra[1:3]} {rc[1:3]}')


def t_negzero(base):
    L, b = system(21, (8, 8, 12), -3.0, 3.0, neg_zero=True)
    with fake_cupy('tol'), knobs([base, S3], cert=True, rtol=1e-12):
        ra = run_solve(base, L, b)
        rc = run_solve(S3, L, b)
    xa, xc = ra[0], rc[0]
    diffb = np.flatnonzero(xa.view(np.uint64) != xc.view(np.uint64))
    chk('G4 부호 있는 0 (b 에 −0.0) — info · 반복 수 같음 · 값 같음 (−0 = +0) · 바이트 차이는 값 0 자리에서만',
        ra[1:3] == rc[1:3] and np.array_equal(xa, xc) and bool(np.all(xa[diffb] == 0.0)),
        f'{ra[1:3]} {rc[1:3]} 바이트 다른 칸 {len(diffb)}')
    print(f'    (G4 관찰: 바이트 다른 칸 {len(diffb)} — 생산 b 는 np.zeros + 양수라 −0 이 없다)')


def t_cpu(base):
    rows = []
    for seed in (31, 32):
        L, b = system(seed, (8, 8, 12))
        with fake_cupy('tol') as rec, knobs([base, S3], gpu=False, cert=True, rtol=1e-12):
            ra = run_solve(base, L, b)
            rc = run_solve(S3, L, b)
            calls = rec.get('calls', 0)
        rows.append((ra, rc, calls))
    chk('G5 CPU 길 (GPU_SOLVE 끔) — 옛 판과 해 바이트 · info · 반복 수 · LAST_BACKEND 같음 · 가짜 cg 부름 0',
        all(ra[0].tobytes() == rc[0].tobytes() and ra[1:] == rc[1:] and c == 0 and rc[3].get('used') == 'cpu' for ra, rc, c in rows),
        f'{[(ra[1:], rc[1:], c) for ra, rc, c in rows][:1]}')


def t_fallback(base):
    L, b = system(41, (6, 6, 10))
    with fake_cupy('tol', fail_linalg=True), knobs([base, S3], cert=True, rtol=1e-12):
        ra = run_solve(base, L, b)
        rc = run_solve(S3, L, b)
    chk('G6 GPU 길 불러오기 실패 → CPU 폴백 — 옛 판과 해 바이트 · info · 반복 수 · LAST_BACKEND (사유 글) 같음',
        ra[0].tobytes() == rc[0].tobytes() and ra[1:] == rc[1:] and rc[3].get('used') == 'cpu' and bool(rc[3].get('fallback_reason')),
        f'{ra[3]} | {rc[3]}')
    outs = []
    for mod in (base, S3):
        with fake_cupy('tol', fail_linalg=True), knobs([mod], cert=True, rtol=1e-12, require=True):
            try:
                quiet(mod._solve_cg, L, b)
                outs.append(None)
            except SystemExit as e:
                outs.append(str(e).splitlines()[0])
    chk('G6 REQUIRE_GPU — 둘 다 SystemExit (같은 첫 줄)', outs[0] is not None and outs[0] == outs[1], f'{outs}')


def _sid_fixture(seed, n=(9, 9, 14)):
    rng = np.random.default_rng(seed)
    sid = rng.choice(np.array([0, 1, 2, 3, 6], np.int8), size=n, p=[0.25, 0.25, 0.15, 0.10, 0.25]).astype(np.int8)
    sid[n[0] // 2, n[1] // 2, :] = 3                        # 판–판 VGCF 기둥 하나 (관통 보장)
    return sid


def _deep_same(a, b):
    """dict · list · 배열 · 실수 비트까지 같음."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(_deep_same(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(_deep_same(x, y) for x, y in zip(a, b))
    if isinstance(a, np.ndarray):
        return a.dtype == b.dtype and a.shape == b.shape and a.tobytes() == b.tobytes()
    if isinstance(a, float):
        return np.float64(a).tobytes() == np.float64(b).tobytes()
    return a == b


def t_solve_sigma(base):
    sig_new = S3.electronic_sigma_table(0.0041, 0.0041, 7853.98, 10.0, 256.6)
    sig_old = base.electronic_sigma_table(0.0041, 0.0041, 7853.98, 10.0, 256.6)
    same, keys, bks = [], [], []
    for seed in (51, 52):
        sid = _sid_fixture(seed)
        for variant in ('tol', 'rtol'):
            with fake_cupy(variant), knobs([base, S3], cert=True, rtol=1e-12):
                base.LAST_CG['iters'] = S3.LAST_CG['iters'] = None
                ra = quiet(base.solve_sigma_z, sid, sig_old, 0.15, z_top_um=14 * 0.15, z_bot_um=0.0, return_field=False)
                ba = dict(base.LAST_BACKEND)
                rc = quiet(S3.solve_sigma_z, sid, sig_new, 0.15, z_top_um=14 * 0.15, z_bot_um=0.0, return_field=False)
                bc = dict(S3.LAST_BACKEND)
            same.append(_deep_same(ra, rc))
            keys.append(sorted(ra) == sorted(rc))
            bks.append(ba == bc and bc.get('used') == 'gpu')
            cc = rc.get('conv_cert') or {}
    chk('G7 solve_sigma_z 끝-끝 (가짜 GPU · 증서 켬 · rtol 1e-12 · 이어 풀기 ⓒ 포함) — 옛 판과 결과 dict 비트 같음 (σ · 증서 · 반복 수) · 키 집합 같음 · '
        'LAST_BACKEND 같음 (= 매니페스트 backend 기록 변화 0)', all(same) and all(keys) and all(bks) and cc.get('ok') is True,
        f'같음 {same} 키 {keys} backend {bks} 증서 {cc.get("status")}')


def main():
    print('── G1 · G1r 전처리 꼴 (고치기 전 = dia_matrix)')
    t_form('tol')
    t_form('rtol')
    print('── G2 연산자 matvec')
    t_matvec()
    try:
        base = load_base()
    except Exception as e:                                 # noqa: BLE001 — 기반 판을 못 읽으면 대조 묶음 실패
        chk('기반 판 (git show 11a794674) 을 읽는다', False, f'{type(e).__name__}: {e}')
        base = None
    if base is not None:
        print('── G3 옛 판 ↔ 지금 판')
        t_equal(base)
        print('── G4 부호 있는 0')
        t_negzero(base)
        print('── G5 CPU 길')
        t_cpu(base)
        print('── G6 폴백')
        t_fallback(base)
        print('── G7 solve_sigma_z 끝-끝')
        t_solve_sigma(base)
    src = inspect.getsource(S3._solve_cg)
    print(f'\n== test_step3_gpu_precond: {_ok}/{_ok + len(_fail)} PASS (판 = {"고침 뒤" if "LinearOperator" in src else "고치기 전"})')
    if _fail:
        print('FAIL: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

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
  G4  부호 있는 0 (★ 11-12 내부 반박 리뷰 RCP-09 — 옛 G4 "바이트 차이는 값 0 자리에서만" 은 해 x 가 +0 에서 시작해 −0 을 갖지 않아 늘 참이었다 = 공허):
      G4a 전처리 적용 자체 — A 꼴 (dia → CSR · 합이 +0 에서 시작) ↔ C 꼴 (원소 곱) 이 값은 같고 바이트는 **C 가 −0 을 내는 칸에서만** 갈린다 (갈림을 실제로 가른다)
      G4b 생산 꼴 b (np.zeros + 양수) — CG 가 전처리에 넘기는 r 어디에도 −0 이 없고 반복마다 A ↔ C 적용 바이트가 같다 (설계 논증을 이 산술에서 잰다)
      G4c (관찰) b 에 −0 을 넣은 꼴 — info · 반복 수 · 해 값 같음 · 해 바이트 차이 수는 찍기만 (판별은 G4a)
      ★ 11-13 Codex 반박 1/2 RCPX-06 — '입력 r 에 −0 이 없으면 A ↔ C 비트 같음' 은 충분조건이 아니다 (철회 · 음의 비정규 곱이 underflow 하면 C = −0 ·
      A = +0).  비트 같음은 잰 입력 · 환경 범위에서만 말한다 (G4b = 이 가짜 산술 · 이 침대 둘에서 반복마다 잰 값).
      G4d (기록 · 보장 아님) 실제 `_solve_cg` 가 만든 M 에 diag [4, 4] · r [−5e-324, 1] (r 에 −0 없음) → A [+0, 0.25] · C [−0, 0.25]
      G4e (기록) 유한 SPD [[4, −1], [−1, 4]] · b [0, 1] · x0 [5e-324, 15e-324] 의 첫 잔차 = 같은 꼴 · 그 반복에서 A ↔ C 적용 바이트 다름 ·
          끝 해 · info · 반복 수는 찍기만 (Codex 관찰 = 같았다)
  G5  CPU 길 (GPU_SOLVE 끔) — 옛 판과 바이트 같음 · 가짜 cg 를 부르지 않는다
  G6  GPU 길 불러오기 실패 → CPU 폴백 — 옛 판과 같음 (해 · LAST_BACKEND 사유 글) · REQUIRE_GPU 면 둘 다 SystemExit (글 전체 같음)
  G6b (★ 11-12 RCP-08) cg 만 있고 LinearOperator 가 없는 옛 cupyx — GPU 길을 쓰지 않는다 (옛 A 꼴로 되돌리지 않는다) · CPU 폴백 = CPU 길 해 ·
      REQUIRE_GPU 면 조치 글이 사유별 (cupy 판 · LinearOperator — "GPU 를 비우고 … 재개" 아님)
  G7  `solve_sigma_z` 끝-끝 (가짜 GPU · 증서 켬 · rtol 1e-12) — 옛 판과 결과 dict (σ 비트 · 증서 · 반복 수 · 키 집합) · LAST_BACKEND 같음 = 매니페스트 키 변화 0
  G8  ★ 11-13 Codex 반박 1/2 Q11 · `SELF-181` — GPU 확인 블록 v8 (`docs/reviews/rint2_codepkg_20261113/q11_gpu_check_block_v8.txt`):
      a 글자 (ASCII · '!' · 탭 · CR 없음 · bash -n) b 하네스 md5 관문 = 추출 바이트 · v7 과 다름 c git 읽기 앞 GIT_DROP_SH · GIT_NO_REPLACE_OBJECTS=1
      d se_material = 핀에서 git show 로 새 폴더에 · --scripts = 그 폴더 · live 저장소 경로 없음 (`SELF-181`) · sha 셋 = 이 리포 e 핀 blob 대조
      f 머리 소비 규칙 g–i 하네스 (numpy · 작은 계): maxiter 1 = all_identical 참인데 adopt 거짓 (판정문 재현) · 수렴 = adopt 거짓 (numpy) ·
      v7 꼴 live import = rc 2 j 가짜 cupy (이 프로세스): adopt 참 · maxiter 1 거짓 · 다른 전처리 거짓 k consume 칸 하나씩 l 블록 셸 끝-끝
      (cupy 없는 이 기계 · 저장소 = 이 리포 · HOME 임시 · rc 1 = cupy 없음 · 리포 그대로)
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
import run_contract as _RCG                                # noqa: E402 — ★ 11-12 2 회차 (재리뷰 RCP2-06) 이 시험 프로세스와 그 자식 (git · payload ·
_RCG.drop_git_env()                                        #   러너) 은 부르는 쪽 환경의 GIT_* 를 물려받지 않는다 (scripts/test_git_env_isolation.py G6)
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
    src = subprocess.run(['git', '-C', ROOT, 'show', f'{BASE_COMMIT}:scripts/step3_sigma.py'], capture_output=True, check=True,
                         env=_RCG.git_env()).stdout                # ★ 11-13 §3 — 봉인용 읽기 env (대체 객체 끔)
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
    watch = REC.get('watch_r')                                   # ★ G4b — 전처리에 넘기는 r 을 반복마다 본다 (시험 고리 · 산술 그대로)
    while iters < maxiter:
        if watch is not None:
            watch(r)
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
def fake_cupy(variant='tol', fail_linalg=False, no_linop=False):
    """sys.modules 에 가짜 cupy · cupyx 를 끼운다 (나올 때 되돌린다).  fail_linalg = cupyx.scipy.sparse.linalg 불러오기 실패 (폴백 길) ·
    no_linop = linalg 에 cg 는 있고 LinearOperator 가 없다 (옛 cupyx 꼴 · RCP-08)."""
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
        if not no_linop:
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


def _apply_A(diag, r):
    """옛 A 꼴 전처리 적용 — 가짜 cupy 산술 그대로 (dia → `tocsc().tocsr()` → (N,1) 곱 · scipy CSR 곱은 합을 +0 에서 시작한다)."""
    return _psolve_of(sparse.diags(1.0 / diag))(r)


def _apply_C(diag, r):
    """C 꼴 전처리 적용 — 생산 GPU 길의 연산자 matvec 산술 (`(1/diag) * r` · 원소 곱 한 번)."""
    return (1.0 / diag) * r


def _negz(v):
    return np.signbit(v) & (v == 0.0)


def t_negzero(base):
    """★ 11-12 (내부 반박 리뷰 RCP-09) — 옛 G4 는 공허했다 (해 x 가 +0 에서 시작해 −0 을 갖지 않으므로 "바이트 차이는 값 0 자리에서만" 이 늘 참).
    갈림이 생길 수 있는 자리 = 전처리 적용 (A: +0 + d·r · C: d·r) 이고 그 입력 = CG 의 r 이다 → G4a 가 그 자리를 직접 가르고 · G4b 가 생산 꼴 b 에서
    그 자리에 갈림의 재료 (−0) 가 오지 않음을 반복마다 잰다 · G4c = 옛 시나리오 (b 에 −0) 의 비공허한 부분 + 관찰."""
    L, _b = system(21, (8, 8, 12), -3.0, 3.0)
    diag = L.diagonal()
    rng = np.random.default_rng(4)
    r = rng.normal(size=L.shape[0])
    r[::5] = 0.0
    r[2::5] = -0.0
    r[3::11] = 5e-324                                            # 양의 비정규 (곱이 +0 으로 떨어질 수 있다)
    r[4::13] = -5e-324                                           # 음의 비정규 (곱이 −0 으로 떨어질 수 있다 — C 만 −0)
    za, zc = _apply_A(diag, r), _apply_C(diag, r)
    diffb = za.view(np.uint64) != zc.view(np.uint64)
    want = _negz(zc) & (za == 0.0) & ~np.signbit(za)              # C = −0 · A = +0 인 칸
    chk('G4a 전처리 적용 — A 꼴 ↔ C 꼴 값 같음 · 바이트 다른 칸 = 정확히 "C 가 −0 · A 가 +0" 인 칸 (−0 입력 전부 포함 · 비어 있지 않음) · 그 밖 바이트 같음 '
        '— 부호 있는 0 갈림을 이 시험이 실제로 가른다 (RCP-09)',
        np.array_equal(za, zc) and np.array_equal(diffb, want) and int(_negz(r).sum()) > 0 and bool(np.all(want[_negz(r)])),
        f'−0 입력 {int(_negz(r).sum())} · 바이트 다른 칸 {int(diffb.sum())} · 기대 칸 {int(want.sum())}')
    stats = []
    for seed, n in ((22, (8, 8, 12)), (23, (10, 6, 14))):
        L2, b2 = system(seed, n, -3.0, 3.0)
        d2 = L2.diagonal()
        for variant in ('tol', 'rtol'):
            for resume in (False, True):
                w = {'seed': seed, 'variant': variant, 'resume': resume, 'n_r': 0, 'negz': 0, 'ab_bytes_diff': 0}

                def watch(rv, d2=d2, w=w):
                    w['n_r'] += 1
                    w['negz'] += int(np.count_nonzero(_negz(rv)))
                    if _apply_A(d2, rv).tobytes() != _apply_C(d2, rv).tobytes():
                        w['ab_bytes_diff'] += 1
                with fake_cupy(variant) as rec, knobs([S3], cert=True, rtol=1e-12):
                    if resume:
                        xs = run_solve(S3, L2, b2)[0]
                        rec['watch_r'] = watch
                        run_solve(S3, L2, b2, x0=xs, rtol=1e-14)
                    else:
                        rec['watch_r'] = watch
                        run_solve(S3, L2, b2)
                stats.append(w)
    chk('G4b 생산 꼴 b (np.zeros + 양수 · STEP3 조립 꼴) — CG 가 전처리에 넘긴 r 어디에도 −0 없음 · 반복마다 A ↔ C 적용 바이트 같음 (침대 둘 · tol= / rtol= · '
        '처음 풀이 / 이어 풀기 ⓒ) — 이 산술 · 이 침대에서 반복마다 잰 값 (RCP-09 · ★ 11-13 RCPX-06: r 에 −0 없음만으로는 충분조건이 아니다 — G4d)',
        len(stats) == 8 and all(w['n_r'] > 0 and w['negz'] == 0 and w['ab_bytes_diff'] == 0 for w in stats), stats)
    L, b = system(21, (8, 8, 12), -3.0, 3.0, neg_zero=True)
    with fake_cupy('tol'), knobs([base, S3], cert=True, rtol=1e-12):
        ra = run_solve(base, L, b)
        rc = run_solve(S3, L, b)
    xa, xc = ra[0], rc[0]
    diffx = np.flatnonzero(xa.view(np.uint64) != xc.view(np.uint64))
    chk('G4c (b 에 −0 을 넣은 꼴 · 생산에 없음) — info · 반복 수 같음 · 해 값 같음 (−0 = +0)', ra[1:3] == rc[1:3] and np.array_equal(xa, xc),
        f'{ra[1:3]} {rc[1:3]}')
    print(f'    (G4c 관찰: 해 바이트 다른 칸 {len(diffx)} — 해 x 는 +0 에서 시작해 −0 을 갖지 않는다 · 갈림의 판별은 G4a · 생산 꼴의 재료 없음은 G4b)')


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
                outs.append(str(e))
    chk('G6 REQUIRE_GPU — 둘 다 SystemExit (글 전체 같음 · 사유별 조치 글을 더한 뒤에도 이 사유의 글은 옛 판 그대로)', outs[0] is not None and outs[0] == outs[1],
        f'{outs}')


def t_fallback_nolinop():
    """★ 11-12 (내부 반박 리뷰 RCP-08) — cg 만 있고 LinearOperator 가 없는 옛 cupyx: 바탕 판은 dia 전처리로 GPU 를 썼고 지금 판은 C 꼴만 안다.
    옛 A 꼴로 조용히 되돌리지 않는다 (GPU 길 전처리 꼴 = 하나 · 기록 키 없이 코드 신원이 C 꼴을 증명한다) → GPU 길을 쓰지 않고 폴백 ·
    REQUIRE_GPU 면 멈추되 조치 글이 그 사유에 맞아야 한다 (GPU 를 비우고 같은 명령으로 재개해도 같은 실패 — cupy 판을 봐야 한다)."""
    L, b = system(42, (6, 6, 10))
    with fake_cupy('tol', no_linop=True) as rec, knobs([S3], cert=True, rtol=1e-12):
        rc = run_solve(S3, L, b)
        calls = rec.get('calls', 0)
    with knobs([S3], gpu=False, cert=True, rtol=1e-12):
        rcpu = run_solve(S3, L, b)
    chk('G6b LinearOperator 없는 옛 cupyx (RCP-08) — 지금 판은 GPU 길을 쓰지 않는다 (가짜 cg 부름 0 · 옛 A 꼴로 되돌리지 않는다) · used cpu · 폴백 사유 글에 '
        'LinearOperator · 해 · info · 반복 수 = CPU 길과 같음',
        calls == 0 and rc[3].get('used') == 'cpu' and 'LinearOperator' in str(rc[3].get('fallback_reason'))
        and rc[0].tobytes() == rcpu[0].tobytes() and rc[1:3] == rcpu[1:3], f'cg 부름 {calls} · {rc[3]}')
    with fake_cupy('tol', no_linop=True), knobs([S3], cert=True, rtol=1e-12, require=True):
        try:
            quiet(S3._solve_cg, L, b)
            msg = None
        except SystemExit as e:
            msg = str(e)
    head, _, rest = (msg or '').partition('\n')
    chk('G6b REQUIRE_GPU + LinearOperator 없음 — SystemExit · 첫 줄 꼴 그대로 (STEP3 ABORT — GPU 솔브 실패인데 …) · 조치 글 = 사유별 (cupy 판 · '
        'LinearOperator 를 이름 댄다 · "GPU 를 비우고 … 재개" 가 아니다 — 비워도 같은 실패) · 자원 낱말 없음 (사슬 자동 재시도로 새지 않게)',
        msg is not None and head.startswith('STEP3 ABORT — GPU 솔브 실패인데') and 'LinearOperator' in rest and 'cupy' in rest
        and 'GPU 를 비우고' not in msg and not any(w in msg for w in ('MemoryError', 'OutOfMemory', 'No space left')), msg)


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


def t_negzero_product(base):
    """★ 11-13 Codex 반박 1/2 RCPX-06 — '입력 r 에 −0 이 없으면 A ↔ C 비트 같음' 은 충분조건이 아니다 (철회).  음의 유한 비정규 곱이 underflow 하면
    C 꼴 (원소 곱 · 생산 GPU 길 연산자) 은 −0 · A 꼴 (CSR 합 · +0 에서 시작) 은 +0.  기록 시험 (보장 아님) = 판정문 반례 그대로."""
    L = sparse.csr_matrix(np.array([[4.0, -1.0], [-1.0, 4.0]]))
    b = np.array([0.0, 1.0])
    Ms = {}
    for tag, mod in (('A', base), ('C', S3)):
        with fake_cupy('tol') as rec, knobs([mod], cert=True, rtol=1e-12):
            run_solve(mod, L, b)
            Ms[tag] = (rec.get('M_seen') or [None])[-1]
    r = np.array([-5e-324, 1.0])
    za = _psolve_of(Ms['A'])(r) if sparse.issparse(Ms['A']) else None
    zc = Ms['C'].matvec(r) if isinstance(Ms['C'], FakeLinearOperator) else None
    ok = (za is not None and zc is not None and not _negz(r).any() and np.array_equal(za, zc)
          and za.view(np.uint64)[0] != zc.view(np.uint64)[0] and bool(_negz(zc)[0]) and za[0] == 0.0 and not np.signbit(za[0])
          and za.view(np.uint64)[1] == zc.view(np.uint64)[1] and float(za[1]) == 0.25)
    chk('G4d ★ 11-13 Codex 반박 1/2 RCPX-06 기록 (보장 아님) — 실제 `_solve_cg` 가 만든 M (A = 옛 판 dia · C = 지금 판 연산자) 에 diag [4, 4] · '
        'r = [−5e-324, 1] (r 에 −0 없음) → A = [+0, 0.25] · C = [−0, 0.25] · 값 같음 · 첫 칸 바이트 다름 ⇒ "r 에 −0 이 없으면 비트 같음" 은 충분조건이 '
        '아니다 (음의 비정규 곱 underflow)', ok, f'A {None if za is None else [float(v).hex() for v in za]} · '
        f'C {None if zc is None else [float(v).hex() for v in zc]}')
    x0 = np.array([5e-324, 15e-324])
    d2 = np.array([4.0, 4.0])
    obs = {}
    for tag, mod in (('A', base), ('C', S3)):
        w = {'first_r': None, 'diff_iters': 0, 'n_r': 0}

        def watch(rv, w=w):
            w['n_r'] += 1
            if w['first_r'] is None:
                w['first_r'] = np.array(rv, copy=True)
            if _apply_A(d2, rv).tobytes() != _apply_C(d2, rv).tobytes():
                w['diff_iters'] += 1
        with fake_cupy('tol') as rec, knobs([mod], cert=True, rtol=1e-12):
            rec['watch_r'] = watch
            obs[tag] = run_solve(mod, L, b, x0=x0) + (w,)
    want_r = np.array([-5e-324, 1.0])
    fr = [obs[t][4]['first_r'] for t in ('A', 'C')]
    chk('G4e ★ 11-13 RCPX-06 기록 — 유한 SPD [[4, −1], [−1, 4]] · b [0, 1] · 비음수 x0 [5e-324, 15e-324]: 첫 잔차 = [−5e-324, 1] (−0 없음 · A · C 같음) · '
        '그 잔차에서 A ↔ C 전처리 적용 바이트 다름 (두 풀이 모두 ≥ 1 반복)',
        all(v is not None and v.tobytes() == want_r.tobytes() for v in fr) and all(obs[t][4]['diff_iters'] >= 1 for t in ('A', 'C')),
        f'첫 잔차 {[None if v is None else [float(x).hex() for x in v] for v in fr]} · 다른 반복 {[obs[t][4]["diff_iters"] for t in ("A", "C")]}')
    xa, xc = obs['A'][0], obs['C'][0]
    print(f'    (G4e 관찰 · 보장 아님: 끝 해 바이트 같음 {xa.tobytes() == xc.tobytes()} · info {obs["A"][1]} / {obs["C"][1]} · '
          f'반복 {obs["A"][2]} / {obs["C"][2]} — Codex 관찰 = 같음 · info 0 · 반복 2)')


# ═════════════════════════ G8 (★ 11-13 Codex 반박 1/2 Q11 · SELF-181) — GPU 확인 블록 v8 ═════════════════════════
#  환경 변수 Q11_BLOCK_UNDER_TEST = 다른 블록 파일로 G8 을 돌린다 (옛 v7 블록 대조 · 증거용 · 게이트는 쓰지 않는다)
BLOCK_V8 = os.environ.get('Q11_BLOCK_UNDER_TEST') or os.path.join(ROOT, 'docs', 'reviews', 'rint2_codepkg_20261113', 'q11_gpu_check_block_v8.txt')
V7_HARNESS_MD5 = 'acfeb4b4e1515d6aa7d46ddaf67e6e68'
#: 소비 규칙의 사유 머리 (하네스 `consume` 의 why 글 첫 낱말 — 시험 쪽 기준 글자)
WHY_HEAD = {'identical': 'identical false', 'converged': 'converged false', 'backend_ok': 'backend_ok false',
            'short_iters_ok': 'short_iters_ok false', 'source_ok': 'source_ok false', 'numpy': 'backend numpy'}


def _sha256_bytes(bts):
    import hashlib
    return hashlib.sha256(bts).hexdigest()


def _git_show(rev_path):
    r = subprocess.run(['git', '-C', ROOT, 'show', rev_path], capture_output=True, env=_RCG.git_env())
    return r.stdout if r.returncode == 0 else None


def block_parts(text):
    lines = text.split('\n')
    i = [k for k, ln in enumerate(lines) if ln.endswith("<<'Q11_CHECK_EOF'")]
    j = [k for k, ln in enumerate(lines) if ln == 'Q11_CHECK_EOF']
    if len(i) != 1 or len(j) != 1 or not i[0] < j[0]:
        return None
    return '\n'.join(lines[i[0] + 1:j[0]]) + '\n', lines[:i[0] + 1], lines[j[0] + 1:]


def _load_harness(src, name='q11_harness_t'):
    d = tempfile.mkdtemp(prefix='q11h_')
    p = os.path.join(d, 'q11_gpu_check.py')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, p


def _stage(folder, new_bytes=None):
    """하네스가 쓸 폴더 — s3_old.py (기반 판) · s3_new.py (지금 판 또는 넘긴 바이트) · se_material.py (이 리포 · 핀과 같은 바이트)."""
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, 's3_old.py'), 'wb') as fh:
        fh.write(_git_show(f'{BASE_COMMIT}:scripts/step3_sigma.py') or b'')
    with open(os.path.join(folder, 's3_new.py'), 'wb') as fh:
        fh.write(new_bytes if new_bytes is not None else open(os.path.join(SCRIPTS, 'step3_sigma.py'), 'rb').read())
    with open(os.path.join(folder, 'se_material.py'), 'wb') as fh:
        fh.write(open(os.path.join(SCRIPTS, 'se_material.py'), 'rb').read())
    return folder


def _harness_sub(hp, folder, out, extra):
    import json
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    cmd = [sys.executable, hp, '--backend', 'numpy', '--n-side', '6', '--out', out, '--old', os.path.join(folder, 's3_old.py'),
           '--new', os.path.join(folder, 's3_new.py'), '--label', 't'] + extra
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=tempfile.gettempdir(), timeout=600)
    try:
        res = json.load(open(os.path.join(out, 'result.json'), encoding='utf-8'))
    except Exception:                                       # noqa: BLE001
        res = None
    return r.returncode, res, (r.stdout + r.stderr)[-600:]


def _consume_fixture():
    bk = {'requested': 'gpu', 'used': 'gpu', 'fallback_reason': None, 'precond': 'jacobi'}
    pair = {'bytes_identical': True, 'value_differ_count': 0, 'max_abs_diff': 0.0, 'info_same': True, 'iters_same': True, 'backend_same': True}
    short = [{'info': 200, 'iters': 200, 'finite': True, 'backend': dict(bk)} for _ in range(6)]
    solve = [{'info': 0, 'iters': 57, 'finite': True, 'backend': dict(bk)} for _ in range(4)]
    return [dict(pair) for _ in range(5)], short, solve


def t_block_v8():
    import hashlib
    import json
    import re
    if not os.path.isfile(BLOCK_V8):
        chk('G8 GPU 확인 블록 v8 파일이 있다', False, f'없음 — {os.path.relpath(BLOCK_V8, ROOT)} (고치기 전 판)')
        return
    raw = open(BLOCK_V8, 'rb').read()
    text = raw.decode('utf-8', 'replace')
    bn = subprocess.run(['bash', '-n', BLOCK_V8], capture_output=True, text=True)
    chk('G8a 블록 글자 — ASCII 만 · "!" 없음 (대화형 bash 역사 확장) · 탭 · CR 없음 · 끝 줄 바꿈 · bash -n rc 0',
        all(c < 128 for c in raw) and b'!' not in raw and b'\t' not in raw and b'\r' not in raw and raw.endswith(b'\n') and bn.returncode == 0,
        f'bash -n rc {bn.returncode} {bn.stderr[:200]}')
    parts = block_parts(text)
    if parts is None:
        chk('G8b 하네스 heredoc (Q11_CHECK_EOF) 하나', False, '찾지 못함')
        return
    harness, pre, post = parts
    m5 = re.search(r'md5sum < "\$Q11D/q11_gpu_check\.py" \| cut -c1-32\)" = ([0-9a-f]{32}) \]', '\n'.join(post))
    hmd5 = hashlib.md5(harness.encode('utf-8')).hexdigest()
    try:
        compile(harness, 'q11_gpu_check.py', 'exec')
        comp = True
    except SyntaxError:
        comp = False
    chk('G8b 하네스 md5 관문 = 추출한 하네스 바이트의 md5 (cat heredoc 이 쓰는 바이트) · v7 하네스 (acfeb4b4…) 와 다름 · 컴파일 됨',
        m5 is not None and m5.group(1) == hmd5 and hmd5 != V7_HARNESS_MD5 and comp, f'관문 {m5.group(1) if m5 else None} · 추출 {hmd5}')
    gi = [k for k, ln in enumerate(post) if 'git -C' in ln]
    di = [k for k, ln in enumerate(post) if ln.strip() == _RCG.GIT_DROP_SH]
    ei = [k for k, ln in enumerate(post) if ln.strip() == 'export GIT_NO_REPLACE_OBJECTS=1']
    chk('G8c 셸 git 읽기 앞 — run_contract.GIT_DROP_SH 글자 그대로 한 줄 · export GIT_NO_REPLACE_OBJECTS=1 한 줄 · 둘 다 첫 git -C 앞 (봉인용 읽기 · §3)',
        gi and len(di) == 1 and len(ei) == 1 and di[0] < gi[0] and ei[0] < gi[0] and text.count(_RCG.GIT_DROP_SH) == 1,
        f'git {gi[:1]} drop {di} export {ei}')
    old_b = _git_show(f'{BASE_COMMIT}:scripts/step3_sigma.py')
    sha_old = _sha256_bytes(old_b or b'')
    sha_new = _sha256_bytes(open(os.path.join(SCRIPTS, 'step3_sigma.py'), 'rb').read())
    sha_se = _sha256_bytes(open(os.path.join(SCRIPTS, 'se_material.py'), 'rb').read())
    call = [ln for ln in post if 'q11_gpu_check.py" --label' in ln]
    c0 = call[0] if len(call) == 1 else ''
    chk('G8d 모듈 출처 (`SELF-181`) — se_material = 핀에서 git show 로 새 폴더 ($Q11D/se_material.py) · 하네스 --scripts "$Q11D" · --forbid-dir "$Q11REPO" · '
        'PYTHONDONTWRITEBYTECODE=1 · live 저장소 scripts 경로 ($Q11REPO/scripts) 없음 · --old-sha · --new-sha · --se-sha = 이 리포의 기반 판 · 지금 판 · '
        'se_material sha256',
        'show "${Q11PIN}:scripts/se_material.py" > "$Q11D/se_material.py"' in text and '--scripts "$Q11D"' in c0
        and '--forbid-dir "$Q11REPO"' in c0 and 'PYTHONDONTWRITEBYTECODE=1' in c0 and '$Q11REPO/scripts' not in text
        and f'--old-sha {sha_old}' in c0 and f'--new-sha {sha_new}' in c0 and f'--se-sha {sha_se}' in c0 and old_b is not None,
        c0[-400:])
    mp = re.search(r'^Q11PIN=([0-9a-f]{40})$', text, re.M)
    pin = mp.group(1) if mp else None
    pin_new = _git_show(f'{pin}:scripts/step3_sigma.py') if pin else None
    pin_se = _git_show(f'{pin}:scripts/se_material.py') if pin else None
    base_se = _git_show(f'{BASE_COMMIT}:scripts/se_material.py')
    chk('G8e Q11PIN (40 hex) 의 blob = 블록 sha — 핀 step3_sigma.py = --new-sha · 핀 se_material.py = --se-sha · 기반 판 se_material.py = 같은 sha '
        '(옛 · 새 모듈이 같은 se_material 을 쓴다)',
        pin is not None and pin_new is not None and _sha256_bytes(pin_new) == sha_new and pin_se is not None
        and _sha256_bytes(pin_se) == sha_se and base_se is not None and _sha256_bytes(base_se) == sha_se, f'핀 {pin}')
    head = '\n'.join(pre)
    chk('G8f 머리 소비 규칙 (결과 전 · Q11) — consume.adopt · Equality is not convergence · rc 줄 = 판정 아님 · kgy ↔ gabia 이식 안 함 · '
        '하네스 CONSUME_RULE 같은 뜻',
        all(w in head for w in ('consume.adopt', 'Equality is not convergence', 'The rc line only says', 'says nothing about gabia'))
        and 'CONSUME_RULE' in harness and 'Equality is not convergence' in harness)
    try:
        H, hp = _load_harness(harness)
    except Exception as e:                                   # noqa: BLE001
        chk('G8g 하네스 불러오기', False, f'{type(e).__name__}: {e}')
        return
    td = tempfile.mkdtemp(prefix='q11v8_')
    fold = _stage(os.path.join(td, 'f'))
    se_args = ['--scripts', fold, '--forbid-dir', ROOT, '--old-sha', sha_old, '--new-sha', sha_new, '--se-sha', sha_se]
    rc1, r1, t1 = _harness_sub(hp, fold, os.path.join(td, 'o1'), se_args + ['--maxiter', '1'])
    c1 = (r1 or {}).get('consume') or {}
    chk('G8g 하네스 (numpy · 6^3 · maxiter 1 = 판정문 Q11 재현) — rc 0 · all_identical 참 · 주 · 이어 풀이 info 1 · consume.adopt 거짓 · identical 참 · '
        'converged 거짓 · short_iters_ok 참 · 사유에 converged · numpy',
        rc1 == 0 and r1 is not None and r1.get('all_identical') is True and (r1.get('main_old') or {}).get('info') == 1
        and c1.get('adopt') is False and c1.get('identical') is True and c1.get('converged') is False and c1.get('short_iters_ok') is True
        and any(w.startswith(WHY_HEAD['converged']) for w in c1.get('why', [])) and any(w.startswith(WHY_HEAD['numpy']) for w in c1.get('why', [])),
        f'rc {rc1} · {c1} · {t1[-200:]}')
    rc2, r2, t2 = _harness_sub(hp, fold, os.path.join(td, 'o2'), se_args)
    c2 = (r2 or {}).get('consume') or {}
    f2 = (r2 or {}).get('files') or {}
    chk('G8h 하네스 (numpy · 수렴) — rc 0 · identical · converged · backend_ok · short_iters_ok · source_ok 참 · adopt 거짓 (사유 = numpy 하나 · GPU 확인 아님) · '
        'se_material = --scripts 에서 · live 저장소 모듈 0 · 폴더에 .pyc 없음',
        rc2 == 0 and all(c2.get(k) is True for k in ('identical', 'converged', 'backend_ok', 'short_iters_ok', 'source_ok'))
        and c2.get('adopt') is False and len(c2.get('why', [])) == 1 and c2['why'][0].startswith(WHY_HEAD['numpy'])
        and f2.get('se_material_from_scripts') is True and f2.get('loaded_from_forbid_dir_end') == []
        and not any(n.endswith('.pyc') or n == '__pycache__' for n in os.listdir(fold)), f'rc {rc2} · {c2} · {f2} · {t2[-200:]}')
    fold7 = _stage(os.path.join(td, 'f7'))                  # v7 꼴 = 모듈 사본 폴더에 se_material 없음 (step3_sigma 는 제 폴더를 sys.path 맨 앞에 둔다)
    os.remove(os.path.join(fold7, 'se_material.py'))
    rc3, r3, t3 = _harness_sub(hp, fold7, os.path.join(td, 'o3'), ['--scripts', SCRIPTS, '--forbid-dir', ROOT])
    rc4, r4, t4 = _harness_sub(hp, fold, os.path.join(td, 'o4'), se_args[:-1] + ['0' * 64])
    other = _stage(os.path.join(td, 'f_other'))             # --scripts = 다른 폴더 (se_material 사본 있음) · 모듈은 제 폴더 (fold) 의 것을 먼저 본다
    rc5, r5, t5 = _harness_sub(hp, fold, os.path.join(td, 'o5'), ['--scripts', other])
    chk('G8i v7 꼴 live import (모듈 사본 폴더에 se_material 없음 · --scripts = 이 리포 scripts) → rc 2 · 사유 = live 저장소 모듈 (se_material) · 풀이 0 · '
        'se_material sha 틀림 → rc 2 · 풀이 0 · 불러온 se_material ≠ --scripts 의 것 (모듈 폴더 사본이 먼저) → rc 2 · 풀이 0',
        rc3 == 2 and 'live repository' in str((r3 or {}).get('error')) and 'main_old' not in (r3 or {'main_old': 1})
        and 'short_runs' not in (r3 or {'short_runs': 1}) and rc4 == 2 and 'se_material.py' in str((r4 or {}).get('error'))
        and 'short_runs' not in (r4 or {'short_runs': 1}) and rc5 == 2 and 'not imported from --scripts' in str((r5 or {}).get('error'))
        and 'short_runs' not in (r5 or {'short_runs': 1}),
        f'{rc3} {(r3 or {}).get("error")} · {rc4} {(r4 or {}).get("error")} · {rc5} {(r5 or {}).get("error")}')
    #  ── j 가짜 cupy (이 프로세스) — 하네스 main 을 직접 부른다 · se_material 은 이 프로세스에 이미 (live scripts) 있으므로 잠시 뺀다
    fake_mods = {}

    def call_fake(out, extra, new_bytes=None, late=False):
        f = _stage(os.path.join(td, out + '_f'), new_bytes)
        forbid = tempfile.mkdtemp(prefix='q11forbid_')
        saved_se = sys.modules.pop('se_material', None)
        saved_path = list(sys.path)
        sync = (lambda: None)
        if late:                                             # 풀이 도중 (첫 검사 뒤) live 저장소 (forbid) 의 모듈을 불러오는 꼴
            with open(os.path.join(forbid, 'q11_late_mod.py'), 'w') as fh:
                fh.write('X = 1\n')

            def sync():
                if forbid not in sys.path:
                    sys.path.insert(0, forbid)
                importlib.import_module('q11_late_mod')
        try:
            with fake_cupy('tol'):
                cpm = sys.modules['cupy']
                cpm.__version__ = 'fake-12.3.0'
                cpm.cuda = types.SimpleNamespace(Device=lambda i: types.SimpleNamespace(synchronize=sync),
                                                 runtime=types.SimpleNamespace(getDeviceProperties=lambda i: {'name': b'fake'}))
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    try:
                        rc = H.main(['--backend', 'cupy', '--n-side', '6', '--out', os.path.join(td, out), '--old', os.path.join(f, 's3_old.py'),
                                     '--new', os.path.join(f, 's3_new.py'), '--scripts', f, '--forbid-dir', forbid, '--label', out] + extra)
                    except SystemExit as e:                   # 옛 하네스 (인자 모름) = argparse 멈춤
                        rc = e.code
        finally:
            sys.path[:] = saved_path
            sys.modules.pop('se_material', None)
            sys.modules.pop('q11_late_mod', None)
            if saved_se is not None:
                sys.modules['se_material'] = saved_se
        try:
            res = json.load(open(os.path.join(td, out, 'result.json'), encoding='utf-8'))
        except Exception:                                    # noqa: BLE001
            res = {}
        return rc, res
    fake_mods['pos'] = call_fake('j1', [])
    fake_mods['it1'] = call_fake('j2', ['--maxiter', '1'])
    new_src = open(os.path.join(SCRIPTS, 'step3_sigma.py'), 'rb').read()
    tweak = new_src.replace(b'_dinv = 1.0 / cp.asarray(diag)', b'_dinv = 1.0000000001 / cp.asarray(diag)', 1)
    fake_mods['diff'] = call_fake('j3', [], new_bytes=tweak)
    fake_mods['late'] = call_fake('j4', [], late=True)
    cp_, ci_, cd_, cl_ = (fake_mods[k][1].get('consume') or {} for k in ('pos', 'it1', 'diff', 'late'))
    chk('G8j 가짜 cupy (cupy 12.3.0 cg 산술 · 이 프로세스) — 같은 전처리: rc 0 · adopt 참 (identical · converged · backend gpu · 200 반복 · source) · '
        'maxiter 1: all_identical 참인데 adopt 거짓 (converged 거짓) · 다른 전처리 (1/diag 를 아주 조금 바꾼 새 판): identical 거짓 → adopt 거짓 · '
        '풀이 도중 live 저장소 모듈 import (첫 검사 뒤) → source_ok 거짓 → adopt 거짓',
        fake_mods['pos'][0] == 0 and cp_.get('adopt') is True and fake_mods['it1'][0] == 0 and fake_mods['it1'][1].get('all_identical') is True
        and ci_.get('adopt') is False and ci_.get('converged') is False and ci_.get('identical') is True and tweak != new_src
        and fake_mods['diff'][0] == 0 and cd_.get('identical') is False and cd_.get('adopt') is False
        and fake_mods['late'][0] == 0 and cl_.get('source_ok') is False and cl_.get('identical') is True and cl_.get('adopt') is False
        and (fake_mods['late'][1].get('files') or {}).get('loaded_from_forbid_dir_end') == ['q11_late_mod'],
        f'{fake_mods["pos"][0]} {cp_} | {ci_} | {cd_} | {cl_}')
    if not hasattr(H, 'consume'):
        chk('G8k consume 칸 하나씩 (합성 기록)', False, '하네스에 consume 없음 (옛 판)')
        return
    pairs, short, solve = _consume_fixture()
    base_c = H.consume('cupy', 200, pairs, short, solve)
    flips = []

    def flip(name, key, fn, backend='cupy', source_ok=True):
        p_, s_, v_ = _consume_fixture()
        fn(p_, s_, v_)
        c = H.consume(backend, 200, p_, s_, v_, source_ok=source_ok)
        others = [k for k in ('identical', 'converged', 'backend_ok', 'short_iters_ok', 'source_ok') if k != key and key != 'numpy']
        ok = (c['adopt'] is False and any(w.startswith(WHY_HEAD[key]) for w in c['why'])
              and (key == 'numpy' or (c[key] is False and all(c[k] is True for k in others))))
        flips.append((name, ok, c['why']))
    flip('pair bytes', 'identical', lambda p, s, v: p[3].update(bytes_identical=False))
    flip('pair iters', 'identical', lambda p, s, v: p[4].update(iters_same=False))
    flip('main info 1', 'converged', lambda p, s, v: v[0].update(info=1))
    flip('resolve not finite', 'converged', lambda p, s, v: v[3].update(finite=False))
    flip('short used cpu', 'backend_ok', lambda p, s, v: s[2]['backend'].update(used='cpu'))
    flip('solve precond amg', 'backend_ok', lambda p, s, v: v[1]['backend'].update(precond='amg'))
    flip('fallback reason', 'backend_ok', lambda p, s, v: v[2]['backend'].update(fallback_reason='x'))
    flip('short iters 199', 'short_iters_ok', lambda p, s, v: s[5].update(iters=199))
    flip('short info 0', 'short_iters_ok', lambda p, s, v: s[0].update(info=0))
    flip('source', 'source_ok', lambda p, s, v: None, source_ok=False)

    def to_cpu(p, s, v):
        for r in s + v:
            r['backend'].update(used='cpu', requested='cpu')
    flip('backend numpy', 'numpy', to_cpu, backend='numpy')
    chk('G8k consume 칸 하나씩 (합성 기록) — 기준 = adopt 참 · 쌍 바이트 · 반복 수 · 주 info 1 · 이어 풀이 비유한 · 짧은 런 cpu · amg · 폴백 사유 · '
        '199 반복 · info 0 · live 모듈 · numpy 백엔드 = 하나씩 adopt 거짓 · 그 칸만 거짓 · 그 사유 글',
        base_c['adopt'] is True and base_c['why'] == [] and all(ok for _n, ok, _w in flips) and len(flips) == 11,
        [(n, w) for n, ok, w in flips if not ok] or base_c)
    import importlib.util as _iu
    if _iu.find_spec('cupy') is not None:
        print('    (G8l 건너뜀 — 이 기계에 cupy 가 있다 (실제 GPU 확인을 돌리지 않는다))')
        return
    home = tempfile.mkdtemp(prefix='q11home_')
    os.makedirs(os.path.join(home, 'dem-venv', 'bin'))
    open(os.path.join(home, 'dem-venv', 'bin', 'activate'), 'w').close()
    blk = text.replace('Q11REPO="$HOME/dem-mt"', 'Q11REPO="' + ROOT + '"', 1)
    bp = os.path.join(home, 'block.sh')
    with open(bp, 'w', encoding='utf-8') as fh:
        fh.write(blk)
    st0 = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True, env=_RCG.git_env()).stdout
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['HOME'] = home
    rb = subprocess.run(['bash', bp], capture_output=True, text=True, env=env, cwd=home, timeout=900)
    st1 = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True, env=_RCG.git_env()).stdout
    outs = [d for d in os.listdir(home) if d.startswith('q11check_kgy_')]
    res_b, files_b, names = None, {}, []
    if len(outs) == 1:
        names = sorted(os.listdir(os.path.join(home, outs[0])))
        try:
            res_b = json.load(open(os.path.join(home, outs[0], 'result.json'), encoding='utf-8'))
            files_b = res_b.get('files') or {}
        except Exception:                                    # noqa: BLE001
            res_b = None
    chk('G8l 블록 셸 끝-끝 (cupy 없는 이 기계 · Q11REPO = 이 리포 · HOME 임시) — md5 관문 통과 · git show 셋 · 하네스 rc 1 (cupy 없음 = 기록된 오류) · '
        'sha 셋 맞음 · se_material = 새 폴더에서 · 폴더 = 블록 · 하네스 · 모듈 셋 · 결과 · 로그뿐 (.pyc 없음) · 이 리포 git status 그대로',
        '[q11] rc 1 ' in rb.stdout and res_b is not None and 'cupy' in str(res_b.get('error')) and files_b.get('se_material_from_scripts') is True
        and files_b.get('new_sha256') == sha_new and files_b.get('old_sha256') == sha_old and files_b.get('se_material_sha256') == sha_se
        and names == sorted(['check.log', 'q11_gpu_check.py', 'result.json', 's3_new.py', 's3_old.py', 'se_material.py']) and st0 == st1,
        f'{rb.stdout[-300:]} {rb.stderr[-300:]} {names} {None if res_b is None else res_b.get("error")}')


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
        print('── G6b 옛 cupyx (LinearOperator 없음)')
        t_fallback_nolinop()
        print('── G7 solve_sigma_z 끝-끝')
        t_solve_sigma(base)
        print('── G4d · G4e 부호 있는 0 — 충분조건 철회 기록 (11-13 RCPX-06)')
        t_negzero_product(base)
    print('── G8 GPU 확인 블록 v8 (11-13 Q11 소비 규칙 · SELF-181)')
    t_block_v8()
    src = inspect.getsource(S3._solve_cg)
    print(f'\n== test_step3_gpu_precond: {_ok}/{_ok + len(_fail)} PASS (판 = {"고침 뒤" if "LinearOperator" in src else "고치기 전"})')
    if _fail:
        print('FAIL: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

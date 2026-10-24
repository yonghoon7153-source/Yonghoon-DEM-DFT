"""Step B (SELF-133 · 1저자 10-24 Q2 (가)) — 사본/리포에 적용.  Usage: python3 apply_stepB.py ROOT [--tests-only|--code-only]"""
import sys, pathlib
R = pathlib.Path(sys.argv[1])
mode = sys.argv[2] if len(sys.argv) > 2 else 'all'


def rep(rel, old, new, count=1):
    p = R / rel
    s = p.read_text(encoding='utf-8')
    n = s.count(old)
    if n != count:
        raise SystemExit(f'{rel}: 기대 {count} 곳 · 실제 {n} 곳 — {old[:70]!r}')
    p.write_text(s.replace(old, new), encoding='utf-8')
    print(f'  ✓ {rel}')


if mode in ('all', '--code-only'):
    rep('scripts/step3_sigma.py', 'from scipy.sparse.linalg import cg\n', '''from scipy.sparse.linalg import cg as _cg_scipy
import inspect as _inspect
''')
    rep('scripts/step3_sigma.py', 'import se_material  # single source of truth', '''

def _cg_v112(A, b, x0=None, *, rtol=1e-5, atol=0., maxiter=None, M=None, callback=None):
    """scipy ≥ 1.12 의 `cg` 와 같은 반복 (`scipy/sparse/linalg/_isolve/iterative.py` · 1.17.1 에서 옮김 · 실수 계).
    scipy < 1.12 (kgy dem-venv = scipy 1.10.1 · 1저자 10-24) 의 `cg` 는 `tol=` (legacy atol) 이라 정지 의미가 다르고, 정확한 해에서
    rtol 1e-14 로 이어 풀면 30,000 회 동안 수렴하지 못하고 잔차가 나빠진다 (`SELF-133` · 시험 K4) → 옛 판에서는 이것이 `cg` 다 (아래).
    1.12+ 에서는 쓰지 않는다 (scipy 의 `cg` 그대로 · 같은 판에서 비트 같음 = 시험 K4b)."""
    from scipy.sparse.linalg import aslinearoperator
    A = aslinearoperator(A)
    N = A.shape[0]
    b = np.asarray(b, dtype=np.float64).ravel()
    x = np.zeros(N, dtype=np.float64) if x0 is None else np.array(x0, dtype=np.float64).ravel()
    psolve = (lambda v: v) if M is None else aslinearoperator(M).matvec
    bnrm2 = np.linalg.norm(b)
    atol = max(float(atol), float(rtol) * float(bnrm2))
    if bnrm2 == 0:
        return b, 0
    if maxiter is None:
        maxiter = N * 10
    matvec = A.matvec
    r = b - matvec(x) if x.any() else b.copy()
    rho_prev, p = None, None
    for iteration in range(maxiter):
        if np.linalg.norm(r) < atol:
            return x, 0
        z = psolve(r)
        rho_cur = np.dot(r, z)
        if iteration > 0:
            beta = rho_cur / rho_prev
            p *= beta
            p += z
        else:
            p = np.empty_like(r)
            p[:] = z[:]
        q = matvec(p)
        alpha = rho_cur / np.dot(p, q)
        x += alpha * p
        r -= alpha * q
        rho_prev = rho_cur
        if callback:
            callback(x)
    return x, maxiter


#: CPU CG — scipy ≥ 1.12 = scipy `cg` (`rtol=`) · 옛 판 = `_cg_v112` (같은 반복 · 같은 정지 의미 · `SELF-133`).  감싸기 (`step3_conv_cert._cg_count`) 가
#  이 이름을 바꿔 끼우므로 두 판 모두 이 이름 하나로 부른다.
cg = _cg_scipy if 'rtol' in _inspect.signature(_cg_scipy).parameters else _cg_v112

import se_material  # single source of truth''')
    rep('scripts/step3_sigma.py', '''    try:
        _r = cg(L, b, rtol=_rt, maxiter=CG_MAXITER, M=Minv, **_x0k, **_cbk)
    except TypeError:                                      # scipy < 1.12 has no rtol kwarg
        _cnt[0] = 0
        _r = cg(L, b, tol=_rt, maxiter=CG_MAXITER, M=Minv, **_x0k, **_cbk)
''', '''    #  ★ 10-24 (SELF-133) — 옛 `except TypeError → cg(tol=…)` (scipy < 1.12 의 legacy 정지) 를 뺐다 · 옛 판의 `cg` = `_cg_v112` (위)
    _r = cg(L, b, rtol=_rt, maxiter=CG_MAXITER, M=Minv, **_x0k, **_cbk)
''')

if mode in ('all', '--tests-only'):
    rep('scripts/test_step3_conv_cert.py', '''def t_k5_certify_unit():''', '''def t_k4b_v112():
    """★ 10-24 (`SELF-133` · kgy scipy 1.10.1) — 옛 scipy 의 `cg` 자리에 쓰는 `_cg_v112` 가 scipy ≥ 1.12 의 cg 와 같은 판에서 비트 같다
    (해 · info · callback 수 · 네 계) · 그 길 (`S3.cg` = `_cg_v112`) 로 K4 (정확한 해에서 rtol 1e-14 이어 풀기) 가 수렴한다 · 판에 맞는 `cg` 가 묶였다."""
    import inspect
    import scipy
    import scipy.sparse.linalg as SL
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    real = SL.cg
    has = 'rtol' in inspect.signature(real).parameters
    rng = np.random.default_rng(24)
    rows = []
    for n, x0kind, rt, mi in ((200, None, 1e-8, 5000), (500, 'exact', 1e-14, 30000), (300, 'rand', 1e-10, 5000), (400, None, 1e-12, 7)):
        L, b = _lap(n, rng)
        M = sparse.diags(1.0 / L.diagonal())
        x0 = None if x0kind is None else (spsolve(L.tocsc(), b) if x0kind == 'exact' else rng.normal(size=n))
        cv, cr = [0], [0]
        xv, iv = S3._cg_v112(L, b, x0=x0, rtol=rt, maxiter=mi, M=M, callback=lambda xk: cv.__setitem__(0, cv[0] + 1))
        if has:
            xr, ir = real(L, b, x0=x0, rtol=rt, maxiter=mi, M=M, callback=lambda xk: cr.__setitem__(0, cr[0] + 1))
            rows.append((n, x0kind, rt, mi, iv == ir and cv[0] == cr[0] and xv.tobytes() == xr.tobytes(), (iv, ir, cv[0], cr[0])))
    if has:
        chk('K4b `_cg_v112` = scipy ≥ 1.12 cg (같은 판 · 해 비트 · info · callback 수 · 초기값 없음 · 정확한 해 · 무작위 · maxiter 소진)',
            len(rows) == 4 and all(r[4] for r in rows), rows)
    else:
        print(f'  --  K4b 대조 건너뜀 (scipy {scipy.__version__} < 1.12 · 비교 대상 cg(rtol=) 없음 · 3.11 게이트가 본다 · 세지 않음)')
    rng = np.random.default_rng(9)
    L, b = _lap(500, rng)
    xs = spsolve(L.tocsc(), b)
    saved = S3.cg
    S3.cg = S3._cg_v112
    try:
        x, info = quiet(S3._solve_cg, L, b, x0=xs, rtol=1e-14)
    finally:
        S3.cg = saved
    chk('K4c 옛 scipy 길 (`cg` = `_cg_v112`) 로 K4 — 정확한 해에서 rtol 1e-14 이어 풀기 수렴 (info 0 · 최대 차 ≤ 1e-10 · 옛 scipy cg = 30,000 회 미수렴)',
        info == 0 and np.max(np.abs(x - xs)) <= 1e-10 * np.max(np.abs(xs)), f'{info}')
    chk('K4d 판에 맞는 `cg` (scipy ≥ 1.12 = scipy cg · < 1.12 = `_cg_v112`)',
        (S3.cg is real) == has and (S3.cg is S3._cg_v112) == (not has), f'has_rtol={has} cg={getattr(S3.cg, "__name__", S3.cg)}')


def t_k5_certify_unit():''')
    rep('scripts/test_step3_conv_cert.py', 'for fn in (t_k1_default_bitid, t_k2_defaults, t_k3_knob, t_k4_x0, t_k5_certify_unit,',
        'for fn in (t_k1_default_bitid, t_k2_defaults, t_k3_knob, t_k4_x0, t_k4b_v112, t_k5_certify_unit,')
print('done')

# ── 시험 기반 모듈 — 오래된 scipy 에서는 같은 cg 를 넣어 "끈 경로 비트 같음" 이 코드 경로만 비교하게 (3.11 = 아무것도 안 바꿈) ──
SAME_CG = ('    #  ★ 10-24 (`SELF-133`) — scipy < 1.12 이면 지금 판의 CPU `cg` = `_cg_v112` (옛 legacy `cg(tol=…)` 폴백 대신) → 기반 모듈에도\n'
           '    #    같은 cg 를 넣어 끈 경로 비트 대조가 코드 경로만 본다 (scipy ≥ 1.12 = 둘 다 scipy cg · 이 줄은 아무것도 바꾸지 않는다)\n'
           "    if S3 is not None and getattr(S3, 'cg', None) is getattr(S3, '_cg_v112', 0) and hasattr(m, '_solve_cg'):\n"
           '        m.cg = S3.cg\n')
if mode in ('all', '--harness-only'):
    rep('scripts/test_carbon_junction.py', "    spec = importlib.util.spec_from_file_location('step3_sigma_base_d1768', p)\n"
        "    m = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(m)\n    return m, ''\n",
        "    spec = importlib.util.spec_from_file_location('step3_sigma_base_d1768', p)\n"
        "    m = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(m)\n" + SAME_CG + "    return m, ''\n")
    rep('scripts/test_step3_conv_cert.py', "    spec = importlib.util.spec_from_file_location('step3_sigma_base_cc', p)\n"
        "    m = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(m)\n    return m\n",
        "    spec = importlib.util.spec_from_file_location('step3_sigma_base_cc', p)\n"
        "    m = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(m)\n" + SAME_CG + "    return m\n")
    rep('scripts/test_step3_target_cert.py', "    spec = importlib.util.spec_from_file_location(name, p)\n"
        "    m = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(m)\n    return m\n",
        "    spec = importlib.util.spec_from_file_location(name, p)\n"
        "    m = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(m)\n" + SAME_CG + "    return m\n")
print('harness done')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""STEP3 수렴 증서 (설계 v1 §6 · R §3-5 · N15 = 권고대로) — 시험 먼저 (규율 ② · 2026-10-20).

증서 셋 (σ 를 게시하려면 셋 다): ⓐ 정지 규칙 = CG rtol ≤ 봉인값 · info 0 · 잔차 유한 ⓑ 판 전류 불균형 |I_bot − I_top|/I_bot ≤ ε_I
ⓒ 조임 재풀이 = 앞 해를 초기값으로 rtol/100 까지 이어 풀어 |Δσ|/σ ≤ 1e-4.  하나라도 실패 = 미수렴 (미게시).
ε_I · 정지 rtol = 합성 직접해 대조 (24 × 24 × 72 · vox 0.15 · 아래 판에 매달려 위 판에 안 닿는 섬유 · σ_fibre 7,853.98 ·
σ_NCM 0.0041 · 시드 셋 · 접합 간선이 있는 꼴 하나 더) 의 표에서 **기계적으로** 정한다 (설계 §6 봉인 절차 3) — 코드 상수가 그 규칙의
결과와 같은지 이 시험이 대조한다 (상수만 바꾸면 실패).  ⚠ 합성 격자 · 실침대 아님 · 인용 불가.

  python3 scripts/test_step3_conv_cert.py
  python3 scripts/test_step3_conv_cert.py --table     # 봉인 표만 찍는다 (R 개정 근거 · 결과 0 건)
"""
import argparse
import contextlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
BASE_COMMIT = 'd1768cf0c'

S3 = None
CC = None
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


@contextlib.contextmanager
def knobs(rtol=None, cert=None):
    o_r, o_c = S3.CG_RTOL, S3.CONV_CERT
    try:
        if rtol is not None:
            S3.CG_RTOL = rtol
        if cert is not None:
            S3.CONV_CERT = cert
        yield
    finally:
        S3.CG_RTOL, S3.CONV_CERT = o_r, o_c


def _load_base():
    src = subprocess.run(['git', '-C', ROOT, 'show', f'{BASE_COMMIT}:scripts/step3_sigma.py'],
                         capture_output=True, check=True).stdout
    d = tempfile.mkdtemp(prefix='s3base_cc_')
    p = os.path.join(d, 'step3_sigma_base_cc.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('step3_sigma_base_cc', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    #  ★ 10-24 (`SELF-133`) — scipy < 1.12 이면 지금 판의 CPU `cg` = `_cg_v112` (옛 legacy `cg(tol=…)` 폴백 대신) → 기반 모듈에도
    #    같은 cg 를 넣어 끈 경로 비트 대조가 코드 경로만 본다 (scipy ≥ 1.12 = 둘 다 scipy cg · 이 줄은 아무것도 바꾸지 않는다)
    if S3 is not None and getattr(S3, 'cg', None) is getattr(S3, '_cg_v112', 0) and hasattr(m, '_solve_cg'):
        m.cg = S3.cg
    return m


def _lap(n, rng):
    """무작위 SPD 라플라시안 + 접지 (판 결합 꼴)."""
    from scipy import sparse
    g = rng.uniform(0.01, 100.0, n - 1)
    rows = np.r_[np.arange(n - 1), np.arange(1, n)]; cols = np.r_[np.arange(1, n), np.arange(n - 1)]
    A = sparse.coo_matrix((np.r_[-g, -g], (rows, cols)), shape=(n, n)).tocsr()
    d = -np.asarray(A.sum(1)).ravel()
    d[0] += 5.0; d[-1] += 3.0
    L = (A + sparse.diags(d)).tocsr()
    b = np.zeros(n); b[0] = 5.0
    return L, b


def t_k1_default_bitid():
    base = _load_base()
    rng = np.random.default_rng(11)
    same = True
    for n in (50, 400, 3000):
        L, b = _lap(n, rng)
        xb, ib = base._solve_cg(L, b)
        xc, ic = S3._solve_cg(L, b)
        same &= (xb.tobytes() == xc.tobytes() and int(ib) == int(ic))
    chk('K1 `_solve_cg` 기본 호출 = 옛 경로 비트 동일 (해 · info)', same)
    chk('K1 LAST_BACKEND 기본 = 옛 키 그대로 (rtol 키 없음)', sorted(S3.LAST_BACKEND) == sorted(base.LAST_BACKEND)
        and 'rtol' not in S3.LAST_BACKEND, f'{sorted(S3.LAST_BACKEND)}')


def t_k2_defaults():
    chk('K2 기본값 — CG_RTOL 1e-8 · CONV_CERT 끔', S3.CG_RTOL == 1e-8 and S3.CONV_CERT is False,
        f'{getattr(S3, "CG_RTOL", None)} {getattr(S3, "CONV_CERT", None)}')
    sid = np.zeros((3, 3, 6), np.int8); sid[1, 1, :] = 3
    r = quiet(S3.solve_sigma_z, sid, S3.electronic_sigma_table(0.01, 0.005, 100.0, 10.0, 250.0), 1.0, z_top_um=6.0,
              z_bot_um=0.0)
    chk('K2 증서 끔 → 결과에 conv_cert 키 없음 · 판 전류 기록 키 없음', 'conv_cert' not in r and 'I_top' not in r, f'{sorted(r)}')


def t_k3_knob():
    seen = {}
    real = S3.cg

    def spy(L, b, *a, **k):
        seen.update(k)
        return real(L, b, *a, **k)
    S3.cg = spy
    try:
        rng = np.random.default_rng(5)
        L, b = _lap(200, rng)
        with knobs(rtol=1e-11):
            quiet(S3._solve_cg, L, b)
            bk = dict(S3.LAST_BACKEND)
        r1 = seen.get('rtol', seen.get('tol'))
        quiet(S3._solve_cg, L, b)
        bk2 = dict(S3.LAST_BACKEND)
    finally:
        S3.cg = real
    chk('K3 CG_RTOL 노브 → CG 에 그 rtol 이 간다 (numeric 노브)', r1 == 1e-11, f'{seen}')
    chk('K3 노브를 켜면 LAST_BACKEND 에 rtol 기록 · 끄면 키가 사라진다 (매니페스트 바이트 동일)',
        bk.get('rtol') == 1e-11 and 'rtol' not in bk2, f'{bk} {bk2}')


def t_k4_x0():
    from scipy.sparse.linalg import spsolve
    rng = np.random.default_rng(9)
    L, b = _lap(500, rng)
    xs = spsolve(L.tocsc(), b)
    x, info = quiet(S3._solve_cg, L, b, x0=xs, rtol=1e-14)
    chk('K4 `_solve_cg(x0=…, rtol=…)` — 초기값 · 조임 rtol 을 받는다 (이어 풀기 ⓒ 의 바탕)',
        info == 0 and np.max(np.abs(x - xs)) <= 1e-10 * np.max(np.abs(xs)), f'{info}')


def _exact_system():
    from scipy import sparse
    from scipy.sparse.linalg import spsolve
    #  두 셀 직렬: 아래 판 g 2 · 면 g 1 · 위 판 g 2 → I = 1/(0.5 + 1 + 0.5) = 0.5
    L = sparse.csr_matrix(np.array([[3.0, -1.0], [-1.0, 3.0]]))
    b = np.array([2.0, 0.0])
    phi = spsolve(L.tocsc(), b)
    return L, b, phi, (np.array([0]), np.array([2.0])), (np.array([1]), np.array([2.0]))


def t_k4b_v112():
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


def t_k5_certify_unit():
    from scipy.sparse.linalg import spsolve
    L, b, phi, (Ab, gb), (At, gt) = _exact_system()
    exact = lambda L_, b_, x0, rtol: (spsolve(L_.tocsc(), b_), 0)          # noqa: E731
    c = CC.certify(L, b, phi, 0, 0.0, 1e-12, Ab, gb, At, gt, 1.0, exact)
    chk('K5 정확한 해 · rtol 1e-12 → ⓐ ⓑ ⓒ 통과 · ok', c['ok'] and c['pass_a'] and c['pass_b'] and c['pass_c'], f'{c}')
    chk('K5 판 전류 I_bot = I_top = 0.5 (KCL)', abs(c['I_bot'] - 0.5) < 1e-15 and abs(c['I_top'] - 0.5) < 1e-15)
    c2 = CC.certify(L, b, phi, 0, 0.0, 1e-8, Ab, gb, At, gt, 1.0, exact)
    chk('K5 ⓐ rtol 1e-8 > 봉인 상한 → 실패 (지금 생산 술어를 다음 세대에 그대로 쓰지 않는다)', not c2['pass_a'] and not c2['ok'])
    c3 = CC.certify(L, b, phi, 7, 0.0, 1e-12, Ab, gb, At, gt, 1.0, exact)
    c4 = CC.certify(L, b, phi, 0, float('nan'), 1e-12, Ab, gb, At, gt, 1.0, exact)
    chk('K5 ⓐ info ≠ 0 · 잔차 NaN → 실패', not c3['ok'] and not c4['ok'])
    bad = phi + np.array([0.0, 0.05])
    c5 = CC.certify(L, b, bad, 0, 0.0, 1e-12, Ab, gb, At, gt, 1.0, exact)
    chk('K5 ⓑ 판 전류 불균형 > ε_I → 실패', not c5['pass_b'] and not c5['ok'], f"{c5['imbalance']}")
    drift = lambda L_, b_, x0, rtol: (x0 * 1.01, 0)                     # noqa: E731 — 재풀이가 σ 를 1 % 옮긴다
    c6 = CC.certify(L, b, phi, 0, 0.0, 1e-12, Ab, gb, At, gt, 1.0, drift)
    chk('K5 ⓒ 이어 풀기 |Δσ|/σ > 1e-4 → 실패', not c6['pass_c'] and not c6['ok'], f"{c6.get('dsigma_rel')}")
    stuck = lambda L_, b_, x0, rtol: (x0, 5)                            # noqa: E731 — 재풀이 미수렴
    c7 = CC.certify(L, b, phi, 0, 0.0, 1e-12, Ab, gb, At, gt, 1.0, stuck)
    chk('K5 ⓒ 재풀이 자체가 미수렴 (info ≠ 0) → 실패', not c7['pass_c'])
    chk('K5 증서 판 이름 · 봉인값 기록', c['version'] == CC.CERT_VERSION and c['rtol_max'] == CC.CERT_RTOL_MAX
        and c['eps_I'] == CC.CERT_EPS_I and c['resolve_rtol'] == 1e-12 * CC.CERT_RESOLVE_FACTOR)
    c8 = CC.certify(L, b, phi, 0, 0.0, 1e-14, Ab, gb, At, gt, 1.0, exact)
    chk('K5 ⓒ 이어 풀기 rtol 바닥 1e-14 (정지 rtol 1e-14 → 1e-16 으로 내려가 maxiter 까지 돌지 않는다)',
        c8['resolve_rtol'] == CC.CERT_RESOLVE_RTOL_FLOOR == 1e-14 and c8['ok'], f"{c8['resolve_rtol']}")


def t_k6_solve_cert():
    from scipy.sparse.linalg import spsolve
    sid = np.zeros((3, 3, 6), np.int8); sid[1, 1, :] = 3
    tab = S3.electronic_sigma_table(0.01, 0.005, 100.0, 10.0, 250.0)
    old = S3._solve_cg
    S3._solve_cg = lambda L, b, *a, **k: (spsolve(L.tocsc(), b), 0)
    try:
        with knobs(rtol=1e-12, cert=True):
            r = quiet(S3.solve_sigma_z, sid, tab, 1.0, z_top_um=6.0, z_bot_um=0.0)
        with knobs(rtol=1e-8, cert=True):
            r2 = quiet(S3.solve_sigma_z, sid, tab, 1.0, z_top_um=6.0, z_bot_um=0.0)
    finally:
        S3._solve_cg = old
    chk('K6 증서 켬 · rtol 1e-12 · 정확한 해 → conv_cert.ok · unconverged False',
        r.get('conv_cert', {}).get('ok') is True and r['unconverged'] is False, f"{r.get('conv_cert')}")
    chk('K6 증서 켬 · rtol 1e-8 → ⓐ 실패 → unconverged True (미게시)',
        r2.get('conv_cert', {}).get('ok') is False and r2['unconverged'] is True)


_TABLE = None


def _table():
    global _TABLE
    if _TABLE is None:
        _TABLE = quiet(CC.probe_table)
    return _TABLE


def t_k7_probe():
    tab = _table()
    prod_false = [r for r in tab if r['rtol'] == 1e-8 and r['prod_ok'] and r['sigma_err'] > 1e-4]
    chk('K7 합성 탐침 — rtol 1e-8 에서 생산 술어 (info 0 · 잔차 ≤ 1e-6) 는 통과인데 σ 오차 > 1e-4 인 해가 있다 (거짓 수렴 재현)',
        len(prod_false) >= 1, f'{[(r["variant"], r["seed"], r["sigma_err"]) for r in tab if r["rtol"] == 1e-8]}')
    bad = [r for r in tab if r['sigma_err'] > 1e-4]
    caught = all(not r['cert_ok'] for r in bad)
    chk('K7 증서가 σ 오차 > 1e-4 인 해를 전부 거부한다 (거짓 수렴을 시험이 잡는다)', caught and len(bad) >= 1,
        f'{[(r["variant"], r["seed"], r["rtol"], r["cert_ok"]) for r in bad]}')
    good_at_stop = [r for r in tab if r['rtol'] == CC.CERT_RTOL_MAX]
    chk('K7 봉인 정지 rtol 의 해는 전부 σ 오차 ≤ 1e-4 · 증서 통과', all(r['sigma_err'] <= 1e-4 and r['cert_ok'] for r in good_at_stop)
        and len(good_at_stop) >= 6, f'{[(r["variant"], r["seed"], r["sigma_err"], r["cert_ok"]) for r in good_at_stop]}')
    chk('K7 탐침 = 시드 셋 이상 × 꼴 둘 (접합 간선 꼴 포함)', len({r['seed'] for r in tab}) >= 3
        and {r['variant'] for r in tab} >= {'plain', 'junction'})


def t_k8_seal():
    tab = _table()
    s = CC.derive_seal(tab)
    lo, hi = s['interval']
    chk('K8a 봉인값이 이 환경에서도 유효 — 봉인 rtol 의 해 전부 σ 오차 ≤ 1e-4 · 봉인 ε_I ∈ [좋은 해 불균형 최대, 나쁜 해 최소)',
        all(r['sigma_err'] <= 1e-4 for r in tab if r['rtol'] == CC.CERT_RTOL_MAX) and lo <= CC.CERT_EPS_I < hi,
        f'interval [{lo:.3e}, {hi:.3e}) ε_I {CC.CERT_EPS_I}')
    chk('K8b 봉인 규칙 (설계 §6 절차 3) 의 결과 = 코드 상수 (정지 rtol) — 다르면 봉인이 환경에 걸린다는 정보 (R 개정으로 다시 봉인)',
        s['rtol_stop'] == CC.CERT_RTOL_MAX, f"{s['rtol_stop']} ↔ {CC.CERT_RTOL_MAX}")
    chk('K8b 봉인 규칙의 결과 = 코드 상수 (ε_I · 구간 비지 않음)', (not s['b_diagnostic_only']) and s['eps_I'] == CC.CERT_EPS_I,
        f"{s} ↔ {CC.CERT_EPS_I}")


def t_k9_cli():
    import run_contract as RC
    chk('K9 `--step3-rtol` = numeric (규약 · 물리 해시 밖 · CLI 회계)', RC.CLI_ACCOUNTING.get('--step3-rtol') == ('numeric', None))
    src = open(os.path.join(SCRIPTS, 'mpm_webapp_payload.py'), encoding='utf-8').read()
    chk('K9 payload 에 `--step3-rtol` 인자 · CG_RTOL · CONV_CERT 배선',
        "'--step3-rtol'" in src and re.search(r'_s3\.CG_RTOL\s*=', src) is not None
        and re.search(r'_s3\.CONV_CERT\s*=\s*True', src) is not None)


def main():
    global S3, CC
    ap = argparse.ArgumentParser(description='STEP3 수렴 증서 시험 (시험 먼저)')
    ap.add_argument('--table', action='store_true', help='봉인 표만 찍는다')
    a = ap.parse_args()
    import step3_sigma as _s3
    S3 = _s3
    try:
        import step3_conv_cert as _cc
        CC = _cc
    except Exception as e:                                 # noqa: BLE001
        print(f'  ⚠ step3_conv_cert import 실패: {type(e).__name__}: {e}')
    if a.table:
        tab = _table()
        for r in tab:
            print(f"  {r['variant']:9s} seed {r['seed']}  rtol {r['rtol']:.0e}  info {r['info']}  resid {r['resid']:.2e}  "
                  f"prod_ok {r['prod_ok']!s:5s}  σerr {r['sigma_err']:.3e}  imb {r['imbalance']:.3e}  cert {r['cert_ok']}  "
                  f"it {r.get('iters', '-')}")
        print(CC.derive_seal(tab))
        return 0
    for fn in (t_k1_default_bitid, t_k2_defaults, t_k3_knob, t_k4_x0, t_k4b_v112, t_k5_certify_unit, t_k6_solve_cert, t_k7_probe,
               t_k8_seal, t_k9_cli):
        print(f'── {fn.__name__}')
        try:
            fn()
        except Exception as e:                             # noqa: BLE001
            import traceback
            traceback.print_exc(limit=2)
            chk(f'{fn.__name__} 예외 없이 끝남', False, f'{type(e).__name__}: {e}')
    print(f'\n== test_step3_conv_cert: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('FAIL: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

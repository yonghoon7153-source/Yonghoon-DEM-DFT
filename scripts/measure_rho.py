#!/usr/bin/env python3
"""ρ 측정 — S3 사전등록 v3 ① 의 **수치 민감도 진단** (오차 상한이 아니다).

계약 `docs/area_contract_20260913.md` §5-v3 ①.  Codex 2라운드 (`R2-01`):
*"`network_conductivity.py:669` 는 tol/atol 분기와 fallback 을 갖고 있어 'tol 10배' 만으로 실행
규약이 확정되지 않는다.  solver 경로·라이브러리·실제 rtol/atol·수렴 상태·비교 분모·채널별 ρ 를
먼저 명시해야 한다."*

무엇을 하나 — 케이스 × 채널마다 **생산 솔버**(`solve_network`)를 두 번 돈다:
  A. 생산 그대로.
  B. `cg` 의 허용오차(`tol` 또는 `atol` — 어느 kwarg 가 받아들여졌는지 **기록**)를 **×0.1** 로 조여서.
  ρ_channel = max_i |σ_B − σ_A| / σ_A (%).  기록: 실제 탄 경로(`spsolve` / `cg` / `cg+ilu` /
  `spsolve_fallback` / `cg_after_spsolve`), n_nodes, scipy 버전, 수렴 info.
⚠ **직접해(`spsolve`) 경로에는 허용오차가 없다** — 그 케이스의 Δ=0 은 "잰 0" 이 아니라 **"경로에
  허용오차가 없다"** 는 뜻이다 (`rho_kind = direct`).  한 채널 안에 두 경로가 섞이면 (n_nodes 30,000
  문턱) 그 사실을 그대로 보고한다.
⚠ 솔버 소스를 **바꾸지 않는다** — 격리 로드한 모듈의 `cg`/`spsolve` 이름만 기록·조임 래퍼로 감싼다.

사용:
  python3 scripts/measure_rho.py --webapp ~/lhs_local --deck-dir ~/lhs_local \\
      --out-csv docs/data/rho_lhs_20260913.csv --out-json docs/data/rho_lhs_20260913.json
  python3 scripts/measure_rho.py --selftest
"""
from __future__ import annotations
import argparse
import csv
import datetime as _dt
import importlib.util
import io
import json
import math
import subprocess
import sys
import types
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'


def _load(name, path, subs=()):
    src = Path(path).read_text(encoding='utf-8')
    for a, b in subs:
        assert src.count(a) == 1, (a, src.count(a))
        src = src.replace(a, b, 1)
    mod = types.ModuleType(name); mod.__file__ = str(path)
    sys.path.insert(0, str(SCRIPTS))
    exec(compile(src, str(path), 'exec'), mod.__dict__)
    return mod


_S0 = _load('_s0_for_rho', SCRIPTS / 'audit_constriction_deleted.py')   # 로더·채널·덱 지도 재사용
TIGHTEN = 0.1
RTOL_DEFAULT = 1e-5      # scipy ≥ 1.12 `cg` 기본 rtol — 생산이 안 넘기므로 이것이 실제 판정 기준


def set_tighten(factor):
    """조임 배수를 정한다 (`--tighten`).  0 < factor < 1 만 — 1 이상은 느슨하게 하는 것이라 ρ 가 아니다.
    사다리(SELF-31 크기 실측) = 0.1 → 0.01 → 0.001 (rtol 1e-6 → 1e-7 → 1e-8 = 옛 `tol=1e-8` 의 의도값)."""
    global TIGHTEN
    f = float(factor)
    if not (0.0 < f < 1.0):
        raise ValueError(f'--tighten 은 (0, 1) 사이여야 한다: {factor!r}')
    TIGHTEN = f
    return f
import numpy as np


class _Recorder:
    """`cg`/`spsolve` 호출을 기록하고, 원하면 cg 허용오차를 조인다."""

    def __init__(self, nc, factor=None):
        self.nc, self.factor, self.calls = nc, factor, []
        self._cg, self._sp = nc.cg, nc.spsolve

    def __enter__(self):
        rec = self

        def cg(A, b, **kw):
            kwarg = 'tol' if 'tol' in kw else ('atol' if 'atol' in kw else 'rtol' if 'rtol' in kw else '')
            used = dict(kw)
            #  ★ SELF-31: scipy ≥ 1.12 의 정지 조건은 max(rtol·‖b‖, atol) 이고 생산은 rtol 을 안 넘긴다
            #    → 기본 rtol=1e-5 가 지배, atol=1e-8 은 **안 걸린다** (‖b‖~1).  그래서 조임은 **rtol** 에 건다.
            #    (atol 만 조인 첫 판은 σ 가 비트 동일 = 거짓 0 이었다.)
            #  ⚠⚠ R3-03 (Codex 3라운드) — 옛 판은 키 우선순위 tol→atol→rtol 로 **하나만** 골라
            #    조였다.  그래서 생산이 SELF-31 처방대로 `rtol=1e-8, atol=0` 을 **함께** 넘기면
            #    `kwarg='atol'` 이 뽑히고 `atol *= factor` = 0 → **상대 허용오차가 안 바뀐다**
            #    → A/B 해가 bitwise 동일 = false-zero 재발.  ⇒ 키를 고르지 말고 **정지 기준**
            #    `max(rtol·‖b‖, atol)` 이 factor 배로 줄도록 **관련된 것을 전부** 조인다.
            if rec.factor is not None:
                if kwarg == 'tol':                       # 옛 scipy: tol 이 상대 허용오차다
                    used['tol'] = kw['tol'] * rec.factor
                else:
                    used['rtol'] = kw.get('rtol', RTOL_DEFAULT) * rec.factor
                    if 'atol' in kw:
                        used['atol'] = kw['atol'] * rec.factor
            rec.bnorm = float(np.linalg.norm(b))
            try:
                V, info = rec._cg(A, b, **used)
            except TypeError:
                #  생산 코드는 tol → TypeError → atol 로 재시도한다.  래퍼도 같은 TypeError 를 올려
                #  생산의 분기가 그대로 타게 둔다 (기록만 남긴다).
                rec.calls.append({'fn': 'cg', 'kwarg': kwarg, 'value': used.get(kwarg), 'result': 'TypeError'})
                raise
            _rt = used.get('tol', used.get('rtol', RTOL_DEFAULT))
            _at = used.get('atol', 0.0)
            rec.calls.append({'fn': 'cg', 'kwarg': kwarg, 'value': used.get(kwarg), 'info': int(info),
                              'M': 'M' in kw, 'maxiter': kw.get('maxiter'),
                              'rtol_used': _rt, 'atol_used': _at,
                              #  실제 정지 기준 — 이것이 A/B 에서 안 줄면 조임이 **판별력 0** 이다
                              'crit': max(_rt * rec.bnorm, _at),
                              'binding': ('rtol' if _rt * rec.bnorm >= _at else 'atol')})
            return V, info

        def spsolve(A, b, *a, **kw):
            rec.calls.append({'fn': 'spsolve'})
            return rec._sp(A, b, *a, **kw)

        self.nc.cg, self.nc.spsolve = cg, spsolve
        return self

    def __exit__(self, *exc):
        self.nc.cg, self.nc.spsolve = self._cg, self._sp

    def path(self):
        seq = []
        for c in self.calls:
            if c['fn'] == 'spsolve':
                seq.append('spsolve')
            elif c.get('result') == 'TypeError':
                continue
            else:
                seq.append('cg+ilu' if c.get('M') else 'cg')
        return '>'.join(seq) or 'none'

    def _eff(self):
        return [c for c in self.calls if c['fn'] == 'cg' and c.get('result') != 'TypeError']

    def kwarg(self):
        e = self._eff()
        return (e[0]['kwarg'], e[0]['value'], e[0].get('info')) if e else ('', None, None)

    def adopted(self):
        """**채택된** 해의 상태 — ⚠ R3-04: 옛 판은 첫 cg 의 info 를 적었다.  fallback 이
        일어나면(cg info=1 → ILU-cg info=0) 채택되지 않은 해의 상태를 보고한 셈이다.

        → (info, n_cg, fell_back).  마지막 유효 cg 가 채택된 해다 (그 뒤 spsolve 로
        넘어갔으면 반복해가 아니므로 info 는 의미가 없고 None 을 준다).
        """
        e = self._eff()
        if not e:
            return None, 0, False
        last_is_cg = self.calls and self.calls[-1]['fn'] == 'cg'
        return (e[-1].get('info') if last_is_cg else None), len(e), len(e) > 1

    def crit(self):
        """채택된 해의 실제 정지 기준 (없으면 None)."""
        e = self._eff()
        return e[-1]['crit'] if e else None

    def criterion(self):
        """실제 정지 기준 → (rtol_used, atol_used, binding) — 첫 유효 cg 호출 기준."""
        for c in self.calls:
            if c['fn'] == 'cg' and c.get('result') != 'TypeError':
                return c['rtol_used'], c['atol_used'], c['binding']
        return None, None, ''


def solve_pair(nc, net):
    """→ (σ_A, σ_B, pathA, pathB, kwargA, valueA, infoA, kwargB, valueB, n_nodes)."""
    n_nodes = len(net['nodes']) if isinstance(net, dict) else None
    buf = io.StringIO()
    with redirect_stdout(buf):
        with _Recorder(nc) as ra:
            gA, sA = nc.solve_network(net, mode='full')
        with _Recorder(nc, factor=TIGHTEN) as rb:
            gB, sB = nc.solve_network(net, mode='full')
    ka, va, ia = ra.kwarg(); kb, vb, _ib = rb.kwarg()
    rA, aA, bindA = ra.criterion(); rB, aB, _bB = rb.criterion()
    #  R3-04: **채택된** 해의 상태 (fallback 뒤에도 첫 해를 적던 것을 고친다)
    fa, na, fba = ra.adopted(); fb, nb, fbb = rb.adopted()
    cA, cB = ra.crit(), rb.crit()
    return dict(sigma_A=sA, sigma_B=sB, path_A=ra.path(), path_B=rb.path(),
                kwarg=ka, tol_A=va, tol_B=vb, info_A=ia, n_nodes=n_nodes,
                rtol_A=rA, rtol_B=rB, atol_A=aA, binding_A=bindA,
                info_final_A=fa, info_final_B=fb, n_cg_A=na, n_cg_B=nb,
                fallback_A=fba, fallback_B=fbb, crit_A=cA, crit_B=cB)


def measure_case(case_dir: Path, deck_dir, channels):
    atoms, type_map, scale, _m, contacts, source = _S0.load_case_any(case_dir)
    if deck_dir:
        cands = [Path(deck_dir) / case_dir.name / f'input_{case_dir.name}.liggghts',
                 Path(deck_dir) / f'input_{case_dir.name}.liggghts']
        dk = next((p for p in cands if p.is_file()), None)
        if dk is None:
            raise ValueError('덱을 못 찾았다')
        type_map, _src = _S0.type_map_from_deck(dk)
    plate_z = _S0._SED.estimate_plate_z(atoms)
    span = max((max(a['x'] for a in atoms.values()) - min(a['x'] for a in atoms.values()),
                max(a['y'] for a in atoms.values()) - min(a['y'] for a in atoms.values()), 1e-9))
    box = span * 1000.0
    rows = []
    for ch in channels:
        mode, pick = _S0.CHANNELS[ch]
        tt = pick(type_map)
        if not tt:
            raise ValueError(f'채널 {ch}: target_types 비었다')
        net = _S0._NC.build_network(atoms, contacts, tt, scale, plate_z, box_x=box, box_y=box,
                                    mode=mode, type_map=type_map, contact_mode='physics')
        if net is None:
            rows.append({'case': case_dir.name, 'channel': ch, 'status': 'NO_NETWORK'}); continue
        r = solve_pair(_S0._NC, net)
        sA, sB = r['sigma_A'], r['sigma_B']
        kind = 'direct' if r['path_A'] == 'spsolve' and r['path_B'] == 'spsolve' else 'iterative'
        if sA is None or sB is None:
            status, delta, kind = 'SOLVE_NONE', '', 'none'
        #  ⚠ R3-04: 옛 판은 None 만 걸렀다 — NaN/inf 가 **OK 로 발행**되고 집계를 오염시켰다
        elif not (np.isfinite(sA) and np.isfinite(sB)):
            status, delta = 'NONFINITE', ''
        elif not sA:
            status, delta = 'OLD_ZERO', ''
        #  ⚠ R3-03: 조여도 **정지 기준이 안 줄면** 판별력 0 이다 (거짓 0 의 자리).
        #    직접해는 반복 허용오차 자체가 없으므로 이 검사를 적용하지 않는다.
        elif kind == 'iterative' and not (r['crit_A'] and r['crit_B']
                                          and r['crit_B'] < r['crit_A'] * (1 + 1e-12)):
            status, delta = 'TIGHTEN_NOOP', ''
        else:
            delta = 100.0 * abs(sB - sA) / abs(sA)
            status = 'OK'
        rows.append({'case': case_dir.name, 'channel': ch, 'status': status, 'rho_kind': kind,
                     'n_nodes': r['n_nodes'], 'path_A': r['path_A'], 'path_B': r['path_B'],
                     'kwarg': r['kwarg'], 'tol_A': r['tol_A'], 'tol_B': r['tol_B'], 'cg_info_A': r['info_A'],
                     'cg_info_final_A': r['info_final_A'], 'cg_info_final_B': r['info_final_B'],
                     'n_cg_A': r['n_cg_A'], 'fallback_A': r['fallback_A'], 'fallback_B': r['fallback_B'],
                     'crit_A': r['crit_A'], 'crit_B': r['crit_B'],
                     #  §8-B: 직접해는 **반복 허용오차에 한해** 비적용 (finite·성공 검사는 유지)
                     'tol_gate': 'TOL_NOT_APPLICABLE' if kind == 'direct' else 'applicable',
                     'rtol_A': r['rtol_A'], 'rtol_B': r['rtol_B'], 'atol_A': r['atol_A'], 'binding_A': r['binding_A'],
                     'sigma_ratio_A': sA, 'sigma_ratio_B': sB, 'delta_pct': delta})
    return rows


def summarize(rows, channels):
    import scipy
    out = {'scipy': scipy.__version__, 'python': sys.version.split()[0], 'tighten': TIGHTEN,
           'git_head': subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--short=9', 'HEAD'],
                                      capture_output=True, text=True).stdout.strip(),
           'date': _dt.date.today().isoformat(), 'channels': {}}
    for ch in channels:
        sub = [r for r in rows if r['channel'] == ch]
        #  ⚠ R3-04: 비유한 값이 섞이면 max 가 **행 순서에 따라** 0.0 이 되기도 NaN 이 되기도
        #    했다.  OK 만 세고, 그래도 한 번 더 유한성을 확인한다 (fail-closed).
        ok = [r for r in sub if r['status'] == 'OK' and r['delta_pct'] != ''
              and np.isfinite(r['delta_pct'])]
        it = [r for r in ok if r['rho_kind'] == 'iterative']
        dr = [r for r in ok if r['rho_kind'] == 'direct']
        out['channels'][ch] = {
            'n_cases': len(sub), 'n_ok': len(ok), 'n_iterative': len(it), 'n_direct': len(dr),
            'n_no_network': sum(1 for r in sub if r['status'] == 'NO_NETWORK'),
            'n_solve_none': sum(1 for r in sub if r['status'] == 'SOLVE_NONE'),
            'n_nonfinite': sum(1 for r in sub if r['status'] == 'NONFINITE'),
            'n_old_zero': sum(1 for r in sub if r['status'] == 'OLD_ZERO'),
            'n_tighten_noop': sum(1 for r in sub if r['status'] == 'TIGHTEN_NOOP'),
            'n_fallback': sum(1 for r in sub if r.get('fallback_A') or r.get('fallback_B')),
            'rho_pct_max_iterative': (max(r['delta_pct'] for r in it) if it else None),
            'rho_pct_max_all': (max(r['delta_pct'] for r in ok) if ok else None),
            'paths': sorted({r['path_A'] for r in ok}),
            'kwargs': sorted({r['kwarg'] for r in ok if r['kwarg']}),
            'binding': sorted({r.get('binding_A', '') for r in it if r.get('binding_A')}),
            'rtol_A': sorted({r.get('rtol_A') for r in it if r.get('rtol_A') is not None}),
            'rtol_B': sorted({r.get('rtol_B') for r in it if r.get('rtol_B') is not None}),
        }
    return out


def _print_summary(sm):
    print(f"\n═══ ρ (수치 민감도, cg **rtol** ×{sm['tighten']} — atol 은 안 걸린다) — scipy {sm['scipy']} · HEAD {sm['git_head']} ═══")
    for ch, c in sm['channels'].items():
        rho_it = c['rho_pct_max_iterative']; rho_all = c['rho_pct_max_all']
        print(f"  {ch:11s} 케이스 {c['n_cases']:>3} · OK {c['n_ok']:>3} (반복해 {c['n_iterative']} · 직접해 {c['n_direct']}) "
              f"· 망없음 {c['n_no_network']} · 해없음 {c['n_solve_none']}")
        print(f"      ρ(반복해 max) = {('%.6f %%' % rho_it) if rho_it is not None else '—'}   "
              f"ρ(전체 max) = {('%.6f %%' % rho_all) if rho_all is not None else '—'}   "
              f"경로 {c['paths']} · kwarg {c['kwargs']} · 실제 기준 {c.get('binding')} rtol {c.get('rtol_A')}→{c.get('rtol_B')}")
    print('  ⚠ ρ 는 수치 민감도 진단이지 오차 상한이 아니다.  직접해 케이스의 0 은 "경로에 허용오차가 없다" 는 뜻.')
    print('  ⚠ §5-v3 ①: ρ > 3 % 인 채널은 h0 를 발행하지 않는다 (UNRESOLVED_NUMERIC).')


def _selftest() -> int:
    ok = True
    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)
    print('ρ 측정 (수치 민감도)')
    nc = _S0._NC
    R = 0.5e-6; sc = 1e6
    #  작은 격자 망: 4×4×4 SE 구, 6-이웃 접촉 (직접해 경로, n_nodes ≤ 30000).
    #  ⚠ 첫 판의 5구 사슬은 생산 sanity 검사(G_eff > 1.1·Σg → cg 재시도 → None)에 걸렸다 —
    #    한 줄 사슬은 그 검사의 전제(전극 사이 병렬 경로)에 안 맞는다.  격자는 통과한다.
    pitch = 1.9 * R
    atoms, rows, idx = {}, [], {}
    n = 0
    for ix in range(4):
        for iy in range(4):
            for iz in range(4):
                n += 1; idx[(ix, iy, iz)] = n
                atoms[n] = {'type': 3, 'radius': R, 'x': ix * pitch, 'y': iy * pitch, 'z': R + iz * pitch}
    for (ix, iy, iz), i in idx.items():
        for nb in ((ix + 1, iy, iz), (ix, iy + 1, iz), (ix, iy, iz + 1)):
            if nb in idx:
                rows.append({'id1': i, 'id2': idx[nb], 'contact_area': 0.0, 'delta': 0.1 * R})
    tm = {3: 'SE'}
    pz = _S0._SED.estimate_plate_z(atoms)
    net = nc.build_network(atoms, rows, {3}, sc, pz, box_x=4 * pitch, box_y=4 * pitch, mode='ionic', type_map=tm,
                           contact_mode='physics')
    r = solve_pair(nc, net)
    chk('① 작은 망은 직접해 경로 — path=spsolve, Δ=0 (허용오차 없음)',
        r['path_A'] == 'spsolve' and r['path_B'] == 'spsolve' and r['sigma_A'] == r['sigma_B'] and r['kwarg'] == '',
        f"{r['path_A']}/{r['path_B']} σ={r['sigma_A']}")
    #  ② CG 경로를 **강제** (격리 메모리에서 문턱 30000 → 0): 래퍼가 kwarg·info 를 기록하고 조임이 실제로 들어간다
    nc2 = _load('_nc_cg', SCRIPTS / 'network_conductivity.py', [('if n_nodes > 30000:', 'if n_nodes > 0:')])
    net2 = nc2.build_network(atoms, rows, {3}, sc, pz, box_x=4 * pitch, box_y=4 * pitch, mode='ionic', type_map=tm,
                             contact_mode='physics')
    r2 = solve_pair(nc2, net2)
    chk('② CG 강제 경로: path 가 cg 계열, kwarg 기록 (scipy 1.17 은 tol→TypeError→atol)',
        r2['path_A'].startswith('cg') and r2['kwarg'] in ('tol', 'atol'),
        f"path={r2['path_A']} kwarg={r2['kwarg']} tol_A={r2['tol_A']} info={r2['info_A']}")
    chk('②b 조임이 **rtol** 에 들어갔다 (rtol_B = 1e-5 × 0.1) · 실제 기준 = rtol (atol 1e-8 은 안 걸린다)',
        r2['rtol_A'] == RTOL_DEFAULT and abs(r2['rtol_B'] / RTOL_DEFAULT - TIGHTEN) < 1e-12 and r2['binding_A'] == 'rtol',
        f"rtol {r2['rtol_A']} → {r2['rtol_B']} · atol {r2['atol_A']} · binding {r2['binding_A']}")
    # ②d ★ 판별력 (SELF-31): atol 만 조이면 σ 가 **비트 동일**(거짓 0), rtol 을 조이면 움직인다
    from scipy.sparse.linalg import cg as _cg
    import numpy as _np
    from scipy import sparse as _sp
    n_ = 3000; rng = _np.random.default_rng(1)
    A_ = _sp.diags([_np.full(n_-1, -1.0), _np.full(n_, 2.0) + rng.uniform(0, .5, n_), _np.full(n_-1, -1.0)], [-1, 0, 1]).tocsr()
    b_ = _np.zeros(n_); b_[0] = 1.0; b_[-1] = -1.0
    xa, _ = _cg(A_, b_, atol=1e-8, maxiter=10000); xb, _ = _cg(A_, b_, atol=1e-9, maxiter=10000)
    xr, _ = _cg(A_, b_, rtol=1e-6, maxiter=10000)
    chk('②d 판별력: atol 1e-8→1e-9 는 해가 비트 동일(안 걸림), rtol 1e-5→1e-6 은 해가 움직인다',
        _np.array_equal(xa, xb) and not _np.array_equal(xa, xr),
        f"atol 동일={_np.array_equal(xa, xb)} · rtol 차 max={float(_np.max(_np.abs(xa - xr))):.3e}")
    chk('②c 두 경로(직접·반복)의 σ 가 같은 망에서 서로 근접 (상대차 < 1e-4) — 래퍼가 해를 망치지 않는다',
        r['sigma_A'] and r2['sigma_A'] and abs(r2['sigma_A'] - r['sigma_A']) / r['sigma_A'] < 1e-4,
        f"direct {r['sigma_A']!r} vs cg {r2['sigma_A']!r}")
    #  ③ 요약이 직접해/반복해를 갈라 센다
    fake = [{'case': 'a', 'channel': 'ionic', 'status': 'OK', 'rho_kind': 'direct', 'delta_pct': 0.0, 'path_A': 'spsolve', 'kwarg': ''},
            {'case': 'b', 'channel': 'ionic', 'status': 'OK', 'rho_kind': 'iterative', 'delta_pct': 0.42, 'path_A': 'cg', 'kwarg': 'atol'},
            {'case': 'c', 'channel': 'ionic', 'status': 'NO_NETWORK'}]
    sm = summarize(fake, ('ionic',))
    c = sm['channels']['ionic']
    chk('③ 요약: 직접해 1 · 반복해 1 · 망없음 1 · ρ(반복해)=0.42', c['n_direct'] == 1 and c['n_iterative'] == 1
        and c['n_no_network'] == 1 and c['rho_pct_max_iterative'] == 0.42)
    #  ⑤ --tighten 사다리: setter 가 실제 solve 의 rtol_B 를 옮긴다 (0.001 → rtol 1e-8) · 범위 밖 거부 · 원상복구
    _saved = TIGHTEN
    try:
        set_tighten('0.001')
        r5 = solve_pair(nc2, net2)
        sm5 = summarize([], ('ionic',))
        chk('⑤ --tighten 0.001: rtol_B = 1e-8 (의도값) · rtol_A 불변 · 요약에 tighten 기록  (64-노드 픽스처는 1e-6 에서 이미 기계정밀이라 σ_B 동일이 정상)',
            abs(r5['rtol_B'] - 1e-8) < 1e-20 and sm5['tighten'] == 0.001 and r5['rtol_A'] == RTOL_DEFAULT
            and r5['sigma_B'] is not None,
            f"rtol_B={r5['rtol_B']} tighten={sm5['tighten']} σ_B(×0.1)={r2['sigma_B']!r} σ_B(×0.001)={r5['sigma_B']!r}")
        # ⑤d 사다리 판별력 — 같은 래퍼(atol 만 넘기는 생산 호출 형태)로 ②d 의 3000-노드 toy 를 ×0.1 / ×0.001 로 풀면
        #    기록된 rtol 이 1e-6 / 1e-8 이고 해가 **다르다** (조임이 실제로 더 깊이 들어간다)
        with _Recorder(nc2, factor=0.1) as w1:
            x1, i1 = nc2.cg(A_, b_, atol=1e-8, maxiter=10000)
        with _Recorder(nc2, factor=0.001) as w3:
            x3, i3 = nc2.cg(A_, b_, atol=1e-8, maxiter=10000)
        rt1, rt3 = w1.criterion()[0], w3.criterion()[0]
        chk('⑤d 사다리 판별력 (3000-노드 toy, 생산 호출 형태 atol=1e-8): 기록 rtol 1e-6 / 1e-8 · 둘 다 수렴 · 해가 다르다',
            abs(rt1 - 1e-6) < 1e-18 and abs(rt3 - 1e-8) < 1e-20 and i1 == 0 and i3 == 0 and not _np.array_equal(x1, x3),
            f"rtol {rt1} / {rt3} · info {i1}/{i3} · max|Δx| = {float(_np.max(_np.abs(x1 - x3))):.3e}")
        bad = []
        for v in ('1', '0', '-0.1', '10', 'abc'):
            try:
                set_tighten(v); bad.append(v)
            except ValueError:
                pass
        chk('⑤b 범위 밖 거부: 1 · 0 · 음수 · 10 · 문자 전부 ValueError', not bad, f'통과해 버린 값={bad}')
    finally:
        set_tighten(_saved)
    chk('⑤c 원상복구: TIGHTEN 이 기본값으로 돌아왔다', TIGHTEN == _saved == 0.1)
    #  ④ 래퍼가 빠져나가면 모듈의 cg/spsolve 가 원상복구된다
    chk('④ 래퍼 원상복구', nc.cg is _S0._NC.cg and callable(nc.spsolve))

    # ══ Codex 3라운드 회귀 (R3-03 · R3-04) — 전부 옛 판에서 빨간불이어야 한다 ══
    class _Fake:                     # 생산 solve 를 흉내내는 최소 모듈 대역
        def __init__(self, infos): self._infos, self.spsolve = list(infos), (lambda A, b, *a, **k: b)
        def cg(self, A, b, **kw): return b, self._infos.pop(0)

    _A = np.eye(2); _b = np.array([1.0, 0.0])

    #  ⑥ R3-03 — 생산이 rtol 과 atol 을 **함께** 넘겨도 조임이 rtol 에 들어간다.
    #     옛 판은 키 우선순위(tol→atol→rtol)로 atol 만 골라 `atol*factor` 를 했고,
    #     처방값 atol=0 이면 **아무것도 안 조여졌다** (기준 불변 = false-zero).
    f6 = _Fake([0])
    with _Recorder(f6, factor=0.01) as r6:
        f6.cg(_A, _b, rtol=1e-8, atol=0.0)
    c6 = r6.calls[-1]
    chk('⑥ ★ rtol+atol 을 함께 넘겨도 rtol 이 조여진다 (R3-03)',
        abs(c6['rtol_used'] - 1e-10) < 1e-22, f"rtol_used={c6['rtol_used']:.3g}")
    chk('⑥b 정지 기준이 실제로 factor 배로 줄었다',
        abs(c6['crit'] - 1e-10) < 1e-22, f"crit={c6['crit']:.3g}")

    #  ⑦ R3-04 — fallback 이 일어나면 **채택된**(마지막) 해의 상태를 보고한다.
    #     옛 판의 kwarg() 는 첫 호출(info=1, 채택 안 됨)을 적었다.
    f7 = _Fake([1, 0])
    with _Recorder(f7) as r7:
        f7.cg(_A, _b, atol=1e-8)                 # 실패
        f7.cg(_A, _b, atol=1e-8, M='ilu')        # fallback 성공 ← 채택
    chk('⑦ 첫 해의 info 는 1 (기록은 남긴다)', r7.kwarg()[2] == 1)
    chk('⑦b ★ 채택된 해의 info 는 0 이고 fallback 이 표시된다 (R3-04)',
        r7.adopted() == (0, 2, True), str(r7.adopted()))

    #  ⑧⑨ R3-04 — NaN 이 OK 로 새지 않고, 집계가 **행 순서에 무관**하다.
    def _row(st, d):
        return {'channel': 'ion', 'status': st, 'rho_kind': 'iterative', 'delta_pct': d,
                'path_A': 'cg', 'path_B': 'cg', 'kwarg': 'atol', 'binding_A': 'rtol',
                'rtol_A': 1e-5, 'rtol_B': 1e-6, 'atol_A': 1e-8, 'n_nodes': 40000,
                'fallback_A': False, 'fallback_B': False, 'crit_A': 1e-5, 'crit_B': 1e-6}
    _rows = [_row('OK', 0.0), _row('NONFINITE', ''), _row('OK', 2.0)]
    s1 = summarize(_rows, ['ion'])['channels']['ion']
    s2 = summarize(list(reversed(_rows)), ['ion'])['channels']['ion']
    chk('⑧ ★ NONFINITE 는 OK 로 세지 않는다 (R3-04)',
        s1['n_ok'] == 2 and s1['n_nonfinite'] == 1, f"n_ok={s1['n_ok']} n_nonfinite={s1['n_nonfinite']}")
    chk('⑨ ★ 집계가 행 순서에 무관하다 (옛 판은 0.0 ↔ NaN 로 갈렸다)',
        s1['rho_pct_max_all'] == s2['rho_pct_max_all'] == 2.0,
        f"{s1['rho_pct_max_all']} vs {s2['rho_pct_max_all']}")
    chk('⑩ 새 상태가 요약에 세어진다 (OLD_ZERO · TIGHTEN_NOOP · fallback)',
        all(k in s1 for k in ('n_old_zero', 'n_tighten_noop', 'n_fallback')))

    print('ρ 측정 SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description='ρ 측정 — 생산 솔버 허용오차 민감도 (S3 prereg v3 ①)')
    ap.add_argument('--webapp', default='')
    ap.add_argument('--deck-dir', default='')
    ap.add_argument('--channels', default='ionic,electronic,thermal')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--out-csv', default='')
    ap.add_argument('--out-json', default='')
    ap.add_argument('--tighten', default=None,
                    help='cg rtol 조임 배수 (기본 0.1 = rtol 1e-5→1e-6).  사다리: 0.01 · 0.001 (→1e-7 · 1e-8)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.tighten is not None:
        try:
            set_tighten(a.tighten)
        except ValueError as e:
            print(f'⛔ {e}'); return 2
    if not a.webapp:
        print('⛔ --webapp 이 필요하다'); return 2
    root = Path(a.webapp).expanduser().resolve()
    cases = _S0.discover_raw_cases(root)
    if not cases:
        _S0._SED.WEBAPP = root
        cases = _S0._SED.discover_cases(flat=True)
    if a.limit:
        cases = cases[:a.limit]
    if not cases:
        print(f'⛔ {root} 에서 케이스를 못 찾았다'); return 2
    chans = tuple(c.strip() for c in a.channels.split(',') if c.strip())
    print(f'케이스 {len(cases)} · 채널 {chans} · cg 허용오차 ×{TIGHTEN}')
    rows, errs = [], []
    for i, d in enumerate(cases):
        try:
            rs = measure_case(d, a.deck_dir or None, chans)
        except Exception as e:
            errs.append((d.name, f'{type(e).__name__}: {e}'))
            print(f'  [{i+1:>3}/{len(cases)}] {d.name[:30]:30s} ⛔ {type(e).__name__}: {e}'); continue
        rows.extend(rs)
        line = ' · '.join(f"{r['channel'][:4]} {r.get('path_A','—')} Δ={r['delta_pct'] if r.get('delta_pct','')!='' else '—'}"
                          + ('' if r.get('delta_pct', '') == '' else '%') for r in rs)
        print(f'  [{i+1:>3}/{len(cases)}] {d.name[:30]:30s} {line}')
    if errs:
        print(f'\n⛔ 실패 {len(errs)}건 — 집계를 발행하지 않는다 (부분 census 금지)')
        for n_, m_ in errs[:10]:
            print(f'    {n_}: {m_}')
        return 3
    sm = summarize(rows, chans)
    _print_summary(sm)
    if a.out_csv:
        p = Path(a.out_csv); p.parent.mkdir(parents=True, exist_ok=True)
        keys = ['case', 'channel', 'status', 'rho_kind', 'n_nodes', 'path_A', 'path_B', 'kwarg', 'tol_A', 'tol_B',
                'cg_info_A', 'rtol_A', 'rtol_B', 'atol_A', 'binding_A', 'sigma_ratio_A', 'sigma_ratio_B', 'delta_pct']
        with p.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
        print(f'→ {p}')
    if a.out_json:
        p = Path(a.out_json); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(sm, ensure_ascii=False, indent=1), encoding='utf-8'); print(f'→ {p}')
    return 0


if __name__ == '__main__':
    sys.exit(main())

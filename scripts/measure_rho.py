#!/usr/bin/env python3
"""ρ 측정 — S3 사전등록 v3 ① 의 **수치 민감도 진단** (오차 상한이 아니다).

계약 `docs/area_contract_20260913.md` §5-v3 ①.  Codex 2라운드 (`R2-01`):
*"`network_conductivity.py:669` 는 tol/atol 분기와 fallback 을 갖고 있어 'tol 10배' 만으로 실행
규약이 확정되지 않는다.  solver 경로·라이브러리·실제 rtol/atol·수렴 상태·비교 분모·채널별 ρ 를
먼저 명시해야 한다."*

무엇을 하나 — 케이스 × 채널마다 **생산 솔버**(`solve_network`)를 돌린다:
  A. 생산 그대로.
  B. `cg` 의 허용오차(`tol` 또는 `atol` — 어느 kwarg 가 받아들여졌는지 **기록**)를 **×0.1** 로 조여서.
  C. **노드 라벨을 치환**해서 (고정 씨앗) — 행렬이 `P A Pᵀ` 가 되어 LU 소거 순서가 바뀐다.
  ρ_case = |σ_B − σ_A|/σ_A (반복해) 또는 |σ_C − σ_A|/σ_A (직접해).  채널 ρ = 그 최대.
  기록: 실제 탄 경로(`spsolve` / `cg` / `cg+ilu` / …), n_nodes, scipy 버전, 수렴 info.

⛔⛔ **직접해(`spsolve`) 경로에는 반복 허용오차가 없다** — 조일 것이 없으므로 B 방식의 ρ 가
  **정의되지 않는다**.  옛 판은 그 자리에 `0.0` 을 찍었는데 그것은 *"잰 0"* 이 아니라 *"경로에
  허용오차가 없다"* 였고, 증서에 옮기면 **결측을 0 으로 채워 양의 주장으로 렌더하는 것**
  = 원장 `GAP2-05` 와 같은 부류다.
⇒ **C (라벨 치환)** 를 그 자리의 등록된 ρ 로 쓴다 (계약 §5-v3 ①-b, 런 전 등록 2026-09-15).
  실측으로 **0 이 아니다** — 64-노드 픽스처에서 Δ = 7.222412821174157e-12 %.
⚠ 솔버 소스를 **바꾸지 않는다** — 격리 로드한 모듈의 `cg`/`spsolve` 이름만 기록·조임 래퍼로 감싼다.

사용:
  python3 scripts/measure_rho.py --webapp ~/lhs_local --deck-dir ~/lhs_local \\
      --out-csv docs/data/rho_s3.csv --out-json docs/data/rho_s3.json \\
      --emit-certificate docs/data/s3_rho_cert.json
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


#: 치환 프로브의 씨앗 — 고정한다 (재현 가능해야 한다).  ⛔ 결과를 보고 바꾸지 말 것.
PERM_SEED = 20260917


def permute_net(net, seed=PERM_SEED):
    """망의 **노드 라벨만** 무작위 재배정 → `(새 net, 옮겨진 라벨 수)`.

    ★★ **왜 이것이 직접해판 ρ 인가** (저자 승인 2026-09-15, 선택지 (ii)).
      직접해(`spsolve`) 경로에는 **반복 허용오차가 없어** 조일 것이 없다 ⇒ `tighten` 방식의
      ρ 가 **정의되지 않는다**.  옛 요약이 그 자리에 `0.0` 을 찍었지만 그것은 *"잰 0"* 이
      아니라 *"경로에 허용오차가 없다"* 였고, 증서에 그대로 옮기면 **결측을 0 으로 채워 양의
      주장으로 렌더하는 것** = 원장 `GAP2-05` 와 같은 부류가 된다.
    ★ 그런데 잴 수 있는 자유도가 실재한다 — `network_conductivity.solve_network` 가
      `all_ids = list(perc_nodes)` 로 **집합의 우연한 순서**를 써서 행렬 순서를 정한다.
      아무도 고른 적 없는 순서다.  라벨을 바꾸면 그 자리에 다른 노드가 앉아 행렬이
      `P A Pᵀ` 가 되고, **LU 소거 순서가 달라져 반올림 누적이 달라진다.**
    ⇒ σ 는 **수학적으로 불변**이어야 한다 (동형 그래프 · 같은 저항 · 같은 경계).
      달라지는 만큼이 그 경로의 **재현성 바닥**이고, 그것이 직접해판 ρ 다.
    ⚠ **같은 값 집합 위로** 재배정한다 — 그래야 `list(set)` 이 같은 자리 순서를 유지하면서
      그 자리에 다른 노드가 앉는다 (순수한 대칭 치환).  값 범위가 바뀌면 순서 변화와
      라벨 변화가 뒤섞여 무엇을 쟀는지 흐려진다.
    ⚠ 씨앗은 고정이다 — 이 프로브는 **재현 가능한 한 점**이지 분포 추정이 아니다.
    """
    import random
    ids = sorted({e['id1'] for e in net['edges']} | {e['id2'] for e in net['edges']}
                 | set(net['nodes']) | set(net['bottom']) | set(net['top']))
    shuffled = ids[:]
    random.Random(seed).shuffle(shuffled)
    m = dict(zip(ids, shuffled))
    out = dict(net)
    out['nodes'] = [m[i] for i in net['nodes']]
    out['bottom'] = {m[i] for i in net['bottom']}
    out['top'] = {m[i] for i in net['top']}
    out['edges'] = [dict(e, id1=m[e['id1']], id2=m[e['id2']]) for e in net['edges']]
    return out, sum(1 for i in ids if m[i] != i)


def solve_permuted(nc, net, seed=PERM_SEED):
    """치환 프로브 → `(σ_perm, 옮겨진 라벨 수, 경로)`.  실패하면 `(None, n, 경로)`."""
    pnet, n_moved = permute_net(net, seed)
    buf = io.StringIO()
    with redirect_stdout(buf):
        with _Recorder(nc) as rp:
            _g, sP = nc.solve_network(pnet, mode='full')
    return sP, n_moved, rp.path()


def measure_case(case_dir: Path, deck_dir, channels, permute=True):
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
        #  ── 치환 프로브 (직접해판 ρ).  ⚠ 반복해에서도 **같이 잰다** — 두 수를 나란히 두면
        #     "조임" 과 "순서" 중 어느 자유도가 큰지 보이고, 둘 다 없으면 잰 것이 없다.
        d_perm, n_moved, path_P = '', '', ''
        perm_status = 'skipped'
        if permute and sA is not None and np.isfinite(sA) and sA:
            try:
                sP, n_moved, path_P = solve_permuted(_S0._NC, net)
            except Exception as e:                                # noqa: BLE001
                perm_status, sP = f'EXC:{type(e).__name__}', None
            if sP is None:
                perm_status = perm_status if perm_status.startswith('EXC') else 'SOLVE_NONE'
            elif not np.isfinite(sP):
                perm_status = 'NONFINITE'
            elif not n_moved:
                #  ⛔ 아무 라벨도 안 옮겼으면 **잰 것이 없다** — 0 을 값으로 내지 않는다.
                perm_status = 'PERM_NOOP'
            else:
                d_perm = 100.0 * abs(sP - sA) / abs(sA)
                perm_status = 'OK'
        #  ★ 이 케이스의 **등록된** ρ — 경로가 정한다 (반복해=조임 · 직접해=치환).
        #    ⛔ 둘 중 해당하는 쪽이 실패하면 값을 만들지 않는다 (빈 칸으로 둔다).
        if kind == 'iterative':
            rho_reg, rho_src = (delta, 'tighten') if status == 'OK' else ('', '')
        elif kind == 'direct':
            rho_reg, rho_src = ((d_perm, 'permutation') if perm_status == 'OK' else ('', ''))
        else:
            rho_reg, rho_src = '', ''
        rows.append({'case': case_dir.name, 'channel': ch, 'status': status, 'rho_kind': kind,
                     'delta_perm_pct': d_perm, 'perm_status': perm_status,
                     'perm_n_moved': n_moved, 'perm_path': path_P,
                     'rho_registered_pct': rho_reg, 'rho_source': rho_src,
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
        #  치환 프로브가 실제로 잰 행 · 그리고 **등록된** ρ 가 확정된 행
        _pm = [r for r in sub if r.get('perm_status') == 'OK' and r.get('delta_perm_pct') != ''
               and np.isfinite(r['delta_perm_pct'])]
        _rg = [r['rho_registered_pct'] for r in sub
               if r.get('rho_registered_pct') not in ('', None)
               and np.isfinite(r['rho_registered_pct'])]
        out['channels'][ch] = {
            'n_cases': len(sub), 'n_ok': len(ok), 'n_iterative': len(it), 'n_direct': len(dr),
            'n_no_network': sum(1 for r in sub if r['status'] == 'NO_NETWORK'),
            'n_solve_none': sum(1 for r in sub if r['status'] == 'SOLVE_NONE'),
            'n_nonfinite': sum(1 for r in sub if r['status'] == 'NONFINITE'),
            'n_old_zero': sum(1 for r in sub if r['status'] == 'OLD_ZERO'),
            'n_tighten_noop': sum(1 for r in sub if r['status'] == 'TIGHTEN_NOOP'),
            'n_fallback': sum(1 for r in sub if r.get('fallback_A') or r.get('fallback_B')),
            'rho_pct_max_iterative': (max(r['delta_pct'] for r in it) if it else None),
            #  ⛔ **허용오차 축이 없으면 `None` 이다 — 0.0 이 아니다** (원장 `GAP3-30`, 2026-09-18).
            #    `ok` 는 반복해(`it`) + 직접해(`dr`) 를 합친 것인데, 직접해는 조일 허용오차가
            #    **아예 없어** `delta_pct` 가 **구조적으로 0** 이다 (같은 해를 자기와 비교한다).
            #    옛 판은 그 0 들 위에서 `max` 를 잡아, 반복해가 **한 건도 없는** 채널
            #    (실측: electronic 30/30 이 `spsolve`) 에서도 `rho_pct_max_all = 0.0` 을 냈다.
            #    ⇒ 그것은 *"허용오차 민감도가 0 이다"* 가 아니라 **측정이 없다**는 뜻인데,
            #      숫자로 적히면 계약 §5-v3 ① 의 `ρ > 3 %` 차단을 **구조적으로 통과**시킨다.
            #  ★ `it` 가 비지 않으면 값은 안 바뀐다 — delta 는 음수가 아니고 직접해는 0 이라
            #    `max(over ok) == max(over it)` 다 (실측: rtol 판 세 개에서 두 값이 동일).
            #    ⇒ 이 수정은 **반복해가 0 건인 채널에서만** 결과를 바꾼다.
            'rho_pct_max_all': (max(r['delta_pct'] for r in ok) if (ok and it) else None),
            #  ── 치환 프로브 (직접해판 ρ) ──
            'n_perm_ok': len(_pm), 'n_perm_noop': sum(1 for r in sub if r.get('perm_status') == 'PERM_NOOP'),
            'n_perm_bad': sum(1 for r in sub if r.get('perm_status', 'skipped')
                              not in ('OK', 'skipped', 'PERM_NOOP')),
            'rho_pct_max_permutation': (max(r['delta_perm_pct'] for r in _pm) if _pm else None),
            #  ★★ **증서에 들어가는 값** — 케이스마다 그 경로의 등록된 ρ 를 쓰고 최대를 잡는다.
            #    ⛔ `n_registered < n_ok` 면 잰 것이 정의역을 못 덮는다 ⇒ 증서를 낼 수 없다.
            'n_registered': len(_rg),
            'rho_pct_channel': (max(_rg) if _rg else None),
            'rho_sources': sorted({r['rho_source'] for r in sub if r.get('rho_source')}),
            'paths': sorted({r['path_A'] for r in ok}),
            'kwargs': sorted({r['kwarg'] for r in ok if r['kwarg']}),
            'binding': sorted({r.get('binding_A', '') for r in it if r.get('binding_A')}),
            'rtol_A': sorted({r.get('rtol_A') for r in it if r.get('rtol_A') is not None}),
            'rtol_B': sorted({r.get('rtol_B') for r in it if r.get('rtol_B') is not None}),
        }
    return out


#: 증서가 반드시 들고 있어야 하는 키 — 러너(`run_s3_psi.load_rho_certificate`)의 계약.
CERT_KEYS = ('cohort_ids', 'channels', 'generation', 'stop_criterion', 'aggregation', 'rho')

STOP_CRITERION = (
    '반복해(cg): 생산 rtol 을 ×{t} 로 조여 |σ_B−σ_A|/σ_A.  실제 binding 기준과 채택 해의 info 를 '
    '행마다 기록한다.  '
    '직접해(spsolve): 반복 허용오차가 없으므로 **노드 라벨 치환**(고정 씨앗 {s})으로 행렬을 '
    'P A Pᵀ 로 바꿔 LU 소거 순서를 흔들고 |σ_P−σ_A|/σ_A.  두 경우 모두 σ 는 수학적으로 불변이어야 '
    '하며, 달라지는 만큼이 그 경로의 재현성 바닥이다.')

AGGREGATION = (
    '케이스마다 **그 경로의 등록된 ρ** 를 취하고(반복해=조임 · 직접해=치환) 채널 안에서 **최대**를 '
    '잡는다.  ⛔ 등록된 ρ 가 확정되지 않은 행이 하나라도 있으면 그 채널의 증서를 발행하지 않는다 '
    '(결측을 0 으로 채우지 않는다).  판정에는 **그 채널 자신의 ρ** 를 쓴다.')


def build_certificate(sm, rows, channels, cohort_ids):
    """측정 요약 → 러너가 받는 **ρ 증서** → `(doc, 거부 사유)`.

    ⛔ 값을 만들지 않는다 — 못 잰 채널이 있으면 증서를 **안 낸다**.  러너가 증서를 요구하는
      이유가 *"ρ 가 무엇에서 나왔는지 복원할 수 있어야 한다"* 이므로, 복원 불가한 칸을
      0 으로 채우면 요구 자체가 무의미해진다 (`AREA5-04` · `GAP2-05`).
    """
    bad, by_ch = [], {}
    for ch in channels:
        c = sm['channels'][ch]
        n_need = c['n_ok']
        if not n_need:
            bad.append(f'{ch}: OK 인 케이스가 0건 — 잰 것이 없다')
            continue
        if c['n_registered'] < n_need:
            bad.append(f"{ch}: 등록된 ρ 가 {c['n_registered']}/{n_need} 행에서만 확정됐다 "
                       f"(치환 noop {c['n_perm_noop']} · 치환 실패 {c['n_perm_bad']})")
            continue
        if c['rho_pct_channel'] is None:
            bad.append(f'{ch}: ρ 를 못 냈다')
            continue
        #  ★★ **그 채널에서 실제로 ρ 를 잰 케이스 ID** — 러너가 `B_ch` 를 채널별로 덮는지
        #     확인하는 데 쓴다.  ⚠ 케이스 단위 `cohort_ids` 만으로는 부족하다:
        #     같은 케이스라도 채널마다 `SOLVE_NONE` 이 갈린다 (실측: lhs00_001 은 이온만 해없음).
        _mid = sorted(r['case'] for r in rows
                      if r['channel'] == ch and r.get('rho_registered_pct') not in ('', None))
        by_ch[ch] = {'rho': c['rho_pct_channel'], 'measured_ids': _mid,
                     'n_cases': c['n_cases'], 'n_ok': n_need,
                     'n_iterative': c['n_iterative'], 'n_direct': c['n_direct'],
                     'sources': c['rho_sources'],
                     'rho_max_tighten': c['rho_pct_max_iterative'],
                     'rho_max_permutation': c['rho_pct_max_permutation'],
                     'paths': c['paths'], 'binding': c.get('binding'),
                     'rtol_A': c.get('rtol_A'), 'rtol_B': c.get('rtol_B')}
    if bad:
        return None, '; '.join(bad)
    doc = {
        'what': 'ρ 수치-QC 증서 (계약 §5-v3 ① · 러너 AREA5-04 의 유일한 ρ 입력)',
        'cohort_ids': sorted(cohort_ids),
        'channels': sorted(by_ch),
        'generation': sm.get('git_head', ''),
        'stop_criterion': STOP_CRITERION.format(t=sm.get('tighten'), s=PERM_SEED),
        'aggregation': AGGREGATION,
        #  ★ 스칼라 `rho` = 채널 최대 (러너의 옛 경로 호환).  ⚠ **보수적**이다 — ρ 가 클수록
        #    h1 이 어려워진다.  판정기는 `rho_by_channel` 이 있으면 그쪽을 쓴다.
        'rho': max(v['rho'] for v in by_ch.values()),
        'rho_by_channel': {ch: v['rho'] for ch, v in by_ch.items()},
        #  ⛔ 러너가 **채널별로** `B_ch ⊆ measured` 를 확인한다 (fail-closed).
        'measured_by_channel': {ch: v['measured_ids'] for ch, v in by_ch.items()},
        'per_channel': by_ch,
        'scipy': sm.get('scipy'), 'python': sm.get('python'),
        'tighten': sm.get('tighten'), 'permutation_seed': PERM_SEED,
        'measured_date': sm.get('date'),
        'n_rows': len(rows),
    }
    return doc, ''


def _print_summary(sm):
    print(f"\n═══ ρ (수치 민감도, cg **rtol** ×{sm['tighten']} — atol 은 안 걸린다) — scipy {sm['scipy']} · HEAD {sm['git_head']} ═══")
    for ch, c in sm['channels'].items():
        rho_it = c['rho_pct_max_iterative']; rho_all = c['rho_pct_max_all']
        print(f"  {ch:11s} 케이스 {c['n_cases']:>3} · OK {c['n_ok']:>3} (반복해 {c['n_iterative']} · 직접해 {c['n_direct']}) "
              f"· 망없음 {c['n_no_network']} · 해없음 {c['n_solve_none']}")
        rho_pm, rho_ch = c.get('rho_pct_max_permutation'), c.get('rho_pct_channel')
        print(f"      ρ(조임 max) = {('%.6g %%' % rho_it) if rho_it is not None else '—'}   "
              f"ρ(치환 max) = {('%.6g %%' % rho_pm) if rho_pm is not None else '—'}   "
              f"→ **ρ(채널) = {('%.6g %%' % rho_ch) if rho_ch is not None else '—'}**  "
              f"({c.get('rho_sources')} · 확정 {c.get('n_registered')}/{c['n_ok']})")
        print(f"      경로 {c['paths']} · kwarg {c['kwargs']} · 실제 기준 {c.get('binding')} "
              f"rtol {c.get('rtol_A')}→{c.get('rtol_B')} · 치환 noop {c.get('n_perm_noop')} "
              f"· 치환 실패 {c.get('n_perm_bad')}")
    print('  ⚠ ρ 는 수치 민감도 진단이지 오차 상한이 아니다.')
    print('  ★ 직접해(spsolve)는 반복 허용오차가 없어 **조임 ρ 가 정의되지 않는다** — 그 자리는')
    print('    **노드 라벨 치환**(P A Pᵀ 로 LU 소거 순서를 흔든다)으로 잰다.  ⛔ 0 으로 채우지 않는다.')
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
    # ══ ⑪ 치환 프로브 = **직접해판 ρ** (저자 결정 (ii), 2026-09-15) ═══════════════════
    #    ⛔ 옛 판은 직접해 채널의 ρ 자리에 `0.0` 을 찍었는데 그것은 "잰 0" 이 아니라
    #      "경로에 허용오차가 없다" 였다.  증서에 그대로 옮기면 `GAP2-05`(결측을 0으로)다.
    pnet, n_moved = permute_net(net)
    chk('⑪ 치환은 **라벨만** 바꾼다 — 간선 수·경계 크기·저항 다중집합이 그대로다',
        n_moved > 0 and len(pnet['edges']) == len(net['edges'])
        and len(pnet['bottom']) == len(net['bottom']) and len(pnet['top']) == len(net['top'])
        and sorted(e['R_total'] for e in pnet['edges']) == sorted(e['R_total'] for e in net['edges'])
        and {e['id1'] for e in pnet['edges']} | {e['id2'] for e in pnet['edges']}
        == {e['id1'] for e in net['edges']} | {e['id2'] for e in net['edges']},
        f'옮긴 라벨 {n_moved}/{len(net["nodes"])}')
    chk('⑪b ★ 그리고 실제로 **다른 라벨**이 붙었다 (항등이면 잰 것이 없다)',
        any((a['id1'], a['id2']) != (b['id1'], b['id2'])
            for a, b in zip(net['edges'], pnet['edges'])))
    _sP, _nm, _pp = solve_permuted(nc, net)
    _dp = 100.0 * abs(_sP - r['sigma_A']) / abs(r['sigma_A'])
    chk('⑪c ★★ σ 는 **수학적으로 불변**이어야 한다 — 동형 그래프·같은 저항·같은 경계.  '
        '달라지는 만큼이 그 경로의 재현성 바닥(= 직접해판 ρ)',
        _sP is not None and np.isfinite(_sP) and _dp < 1e-6,
        f"σ {r['sigma_A']!r} → {_sP!r}  Δ = {_dp:.3g} %  (경로 {_pp})")
    _tiny, _nm0 = permute_net({'edges': [{'id1': 1, 'id2': 1}], 'nodes': [1],
                               'bottom': {1}, 'top': {1}})
    chk('⑪d ⛔ 옮길 라벨이 없으면 **PERM_NOOP** — 그 자리에 0 을 쓰지 않는다',
        _nm0 == 0)
    chk('⑪e ★ 그리고 이 값은 **0 이 아니다** — 직접해 경로에도 잴 것이 실재한다 '
        '(옛 판이 0 을 찍던 자리)', _dp > 0.0, f'Δ = {_dp!r} %')

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

    # ══ ⑫ ρ 증서 (`AREA5-04` 의 유일한 ρ 입력) ═══════════════════════════════════
    def _row(case, ch, kind, d_tol, d_perm, pst='OK'):
        return {'case': case, 'channel': ch, 'status': 'OK', 'rho_kind': kind,
                'delta_pct': d_tol, 'delta_perm_pct': d_perm, 'perm_status': pst,
                'perm_n_moved': 5, 'perm_path': 'spsolve', 'path_A': 'spsolve', 'kwarg': '',
                'rho_registered_pct': (d_tol if kind == 'iterative' else
                                       (d_perm if pst == 'OK' else '')),
                'rho_source': ('tighten' if kind == 'iterative' else
                               ('permutation' if pst == 'OK' else ''))}

    _fr = [_row('a', 'ionic', 'iterative', 0.004, 1e-9),
           _row('b', 'ionic', 'direct', 0.0, 2e-9),
           _row('c', 'electronic', 'direct', 0.0, 7e-9),
           _row('d', 'electronic', 'direct', 0.0, 3e-9)]
    _sm = summarize(_fr, ('ionic', 'electronic'))
    chk('⑫ 채널 ρ 는 **경로별 등록값의 최대** — 이온은 조임 0.004 · 전자는 치환 7e-09',
        _sm['channels']['ionic']['rho_pct_channel'] == 0.004
        and _sm['channels']['electronic']['rho_pct_channel'] == 7e-9,
        f"ionic {_sm['channels']['ionic']['rho_pct_channel']} · "
        f"electronic {_sm['channels']['electronic']['rho_pct_channel']}")
    chk('⑫b ★★ 전자 채널이 **전부 직접해**여도 ρ 가 0 이 아니다 — 옛 판이 0 을 찍던 자리다',
        _sm['channels']['electronic']['n_direct'] == 2
        and _sm['channels']['electronic']['rho_sources'] == ['permutation']
        and _sm['channels']['electronic']['rho_pct_channel'] > 0)
    _doc, _why = build_certificate(_sm, _fr, ('ionic', 'electronic'), ['a', 'b', 'c', 'd'])
    chk('⑫c 증서가 러너의 필수 키를 전부 들고 나간다',
        _doc is not None and all(k in _doc and (k == 'rho' or _doc[k]) for k in CERT_KEYS), _why)
    chk('⑫d 채널별 ρ 와 보수적 스칼라(채널 최대)를 같이 싣는다',
        _doc and _doc['rho_by_channel'] == {'ionic': 0.004, 'electronic': 7e-9}
        and _doc['rho'] == 0.004, str(_doc and _doc['rho_by_channel']))
    #  ★★ 판별력 — 한 행이라도 등록된 ρ 가 비면 **증서를 안 낸다** (0 으로 안 채운다).
    _fr2 = list(_fr)
    _fr2[2] = _row('c', 'electronic', 'direct', 0.0, '', pst='PERM_NOOP')
    _sm2 = summarize(_fr2, ('ionic', 'electronic'))
    _doc2, _why2 = build_certificate(_sm2, _fr2, ('ionic', 'electronic'), ['a', 'b', 'c', 'd'])
    chk('⑫e ★★ 판별력: 치환이 noop 인 행이 하나라도 있으면 **증서를 발행하지 않는다** '
        '(결측을 0 으로 채우면 러너가 증서를 요구하는 이유가 사라진다)',
        _doc2 is None and 'electronic' in _why2, _why2[:100])
    #  러너가 실제로 이 증서를 받는가 — 계약을 **직접** 확인한다 (사본이 갈라지지 않게).
    _rs = _load('_runner_for_cert', SCRIPTS / 'run_s3_psi.py')
    chk('⑫f 러너의 필수 키 목록과 여기 CERT_KEYS 가 같다 (사본이 갈라지면 증서가 거부된다)',
        set(_rs.CERT_REQUIRED) == set(CERT_KEYS),
        f'러너 {sorted(_rs.CERT_REQUIRED)} vs 여기 {sorted(CERT_KEYS)}')

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

    #  ══ ⑪ GAP3-30 — 허용오차 축이 없으면 `rho_pct_max_all` 은 **None** 이다 (0.0 이 아니다) ══
    #     실사고: 전자 채널 30/30 이 `spsolve` 인데 `rho_pct_max_all = 0.0` 이 나왔다.
    #     직접해는 조일 허용오차가 없어 delta 가 **구조적으로 0** 이라, 그 위의 max 는
    #     *"민감도가 0"* 이 아니라 **측정이 없다**는 뜻이다.  그런데 숫자로 적히면 계약
    #     §5-v3 ① 의 `ρ > 3 %` 차단을 구조적으로 통과시킨다.
    def _drow(d, kind='direct'):
        return {'channel': 'el', 'status': 'OK', 'rho_kind': kind, 'delta_pct': d,
                'path_A': 'spsolve' if kind == 'direct' else 'cg', 'path_B': 'spsolve',
                'kwarg': '', 'n_nodes': 100, 'fallback_A': False, 'fallback_B': False}
    _d_only = summarize([_drow(0.0), _drow(0.0)], ['el'])['channels']['el']
    chk('⑬ ★★ 직접해뿐인 채널: `rho_pct_max_all` 이 **None** — 항등식 0 을 측정으로 적지 않는다',
        _d_only['rho_pct_max_all'] is None and _d_only['n_iterative'] == 0
        and _d_only['n_direct'] == 2,
        f"max_all={_d_only['rho_pct_max_all']} n_it={_d_only['n_iterative']}")
    chk('⑬b `rho_pct_max_iterative` 는 원래도 None 이었다 (그쪽은 옳았다)',
        _d_only['rho_pct_max_iterative'] is None)
    #  ★ 판별력 — 반복해가 **하나라도** 있으면 값이 살아 있어야 한다 (과잉 억제 방지).
    _mixed = summarize([_drow(0.0), _drow(1.5, 'iterative')], ['el'])['channels']['el']
    chk('⑬c ★ 반복해가 하나라도 있으면 값이 산다 (직접해 0 이 최대를 끌어내리지 않는다)',
        _mixed['rho_pct_max_all'] == 1.5 and _mixed['rho_pct_max_iterative'] == 1.5,
        f"all={_mixed['rho_pct_max_all']} it={_mixed['rho_pct_max_iterative']}")
    chk('⑬d ★ 그때 두 값이 같다 — 직접해는 0 이고 delta 는 음수가 아니므로 max 가 같다',
        _mixed['rho_pct_max_all'] == _mixed['rho_pct_max_iterative'])

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
    ap.add_argument('--emit-certificate', default='',
                    help='러너가 받는 **ρ 증서** JSON 을 낸다 (AREA5-04).  ⛔ 못 잰 채널이 '
                         '있으면 발행하지 않는다')
    ap.add_argument('--no-permutation', action='store_true',
                    help='치환 프로브를 끈다 (진단 전용 — 직접해 채널의 증서를 낼 수 없게 된다)')
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
            rs = measure_case(d, a.deck_dir or None, chans, permute=not a.no_permutation)
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
                'cg_info_A', 'rtol_A', 'rtol_B', 'atol_A', 'binding_A', 'sigma_ratio_A', 'sigma_ratio_B', 'delta_pct',
                'delta_perm_pct', 'perm_status', 'perm_n_moved', 'perm_path',
                'rho_registered_pct', 'rho_source']
        with p.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
        print(f'→ {p}')
    if a.out_json:
        p = Path(a.out_json); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(sm, ensure_ascii=False, indent=1), encoding='utf-8'); print(f'→ {p}')
    if a.emit_certificate:
        doc, why = build_certificate(sm, rows, chans, [d.name for d in cases])
        if doc is None:
            print(f'\n⛔ ρ 증서를 발행하지 않는다 — {why}')
            print('   ⇒ 못 잰 칸을 0 으로 채우면 러너가 증서를 요구하는 이유가 사라진다.')
            return 3
        p = Path(a.emit_certificate); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f"\n→ ρ 증서 {p}")
        print(f"   코호트 {len(doc['cohort_ids'])} · 채널별 ρ {doc['rho_by_channel']} · 스칼라 {doc['rho']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

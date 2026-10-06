#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""망 솔버 수치 증서 (`G2R-03`) · 협착-only 0 저항 (`GEN2-01`) — Codex 세대 2 판정 §4 · §7 Q3 · §8 (1저자 비준 10-06 밤).

  python3 scripts/test_network_solve_certificate.py

★ 시험 먼저 — 고치기 전 모듈 (a0a24c538 의 network_conductivity · HEAD 83ca185c2 와 같은 파일) 에서 빨갛다:
  S  G2R-03 반례 (Codex probes/adversarial.py `cg_dead_end`) — B–중간–T 의 1 Ω 두 개짜리 경로 30,001 개 병렬 + B 에만 붙은 막다른 노드 하나
     (10^14 S) · 자유 노드 30,002 → CG 가지.  참 G = 30,001/2 = 15,000.5 S.  옛 판: computed · cg · G 30,001 (+100 %) · I_top ≈ −3e-10 · Σg 상한 통과.
     새 판: 풀이마다 증서 (I_bottom · I_top · 보존 잔차 · 내부 잔차 · 방법) — 보존 잔차가 1e-6 을 넘으면 그 해를 내지 않고 사다리로 다시 푼다
     (직접해 → Jacobi CG → ILU GMRES · Krylov 단은 잔차 보정) → 참값 (상대 1e-9) 또는 NOT_COMPUTED (current_conservation_failed).
     계산됐는데 틀린 값은 없다.  대조 10^6 · 10^8 · 10^10 · 10^12 = 참값 그대로 (첫 단 cg 가 증서를 통과).
  K  사다리 단마다 — 직접해가 막히면 Jacobi CG (SPD 전처리) · 그것도 막히면 ILU + GMRES (ILU 를 CG 에 넣지 않는다) · 큰 간선이 자유 노드끼리
     이어진 변형은 잔차 보정이 있어야 풀린다 (끄면 두 Krylov 단 다 증서 실패 → 거부) · 모든 단이 증서 실패면 NOT_COMPUTED +
     current_conservation_failed (run_decomposition 상태 · 이온 채널 failed — 게시 차단).
  Z  GEN2-01 — 협착-only 가지가 R_c = 0 간선 (ψ floor · clamp) 을 지우면 단락을 개방으로 바꾼 다른 회로를 푼다:
     B–중간–T (R_c 0 · 1 Ω 직렬) ∥ B–T 10 Ω → 옛 판 0.1 S computed (단락 수축 참값 1.1 S · −90.9 %).  새 판: 관통 간선에 R_c = 0 이 있으면
     그 가지만 NOT_COMPUTED + zero_resistance_requires_contraction · FULL · CF 는 그대로.
  R  증서가 생산 레코드에 실린다 — run_decomposition 결과 `solve_certificate_{full,bulk_net,constr_net}` · 전자 · 열 (`electronic_` · `thermal_`) ·
     H12 레코드 · CLI 가 쓰는 네 JSON (모드 둘 · dual · legacy) · real_14 기준 덤프 (커밋) 의 실침대 증서 · 순수 도우미 `certificate_problem`.
  B  정상 망 = 오늘과 같은 값 — 첫 단이 증서를 통과하면 해를 건드리지 않는다: 큰 망 (자유 노드 32,368 · CG) · 작은 망 · 21 구 사슬 세 가지 ·
     H12 · real_14 를 고치기 전 모듈 (git a0a24c538) 과 float.hex 로 대조 (git 객체가 없으면 SKIP).
⚠ 범위 — 수치 증서 (해가 그 선형계의 해인가 · 전극 전류가 보존되는가) 의 시험이다.  모델의 물리 정확도 · 띠 규칙 · 194 배포값으로 확대하지 않는다.
"""
import contextlib
import gzip
import importlib.util
import io
import json
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
OLD_REF = 'a0a24c538'          # 고치기 전 network_conductivity (세대 2 망 · 증서 없음) — 정상 망 비트 동일 대조의 기준
CONS_MAX = RES_MAX = 1e-6      # 동결 oracle — 등록 허용치 (모듈 상수를 import 하지 않고 같은 값인지 대조한다)
CONS_FAILED = 'current_conservation_failed'
ZERO_R = 'zero_resistance_requires_contraction'
_ok, _fail, _skip = 0, [], []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}' + (f'   {extra}' if extra else ''))
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {extra}' if extra else ''))


def skip(name, why):
    _skip.append(name)
    print(f'  SKIP  {name}   {why}')


def _guard(label, fn):
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001
        chk(f'{label} — 예외 {type(e).__name__}: {e}', False)


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def rel(a, b):
    return abs(a - b) / abs(b) if b else float('inf')


def hexf(v):
    return float(v).hex() if isinstance(v, (int, float)) and not isinstance(v, bool) else repr(v)


def cons_of(ib, it):
    """보존 잔차의 독립 계산 — |I_b + I_t| / max(|I_b|, |I_t|, tiny)."""
    return abs(ib + it) / max(abs(ib), abs(it), sys.float_info.min)


def Eg(i, j, g):
    """간선 하나 (전도도 g · 협착 0 — 솔버가 읽는 키만)."""
    return {'id1': i, 'id2': j, 'R_total': 1.0 / g, 'R_bulk': 1.0 / g, 'R_constriction': 0.0}


def Er(i, j, rb, rc):
    return {'id1': i, 'id2': j, 'R_total': rb + rc, 'R_bulk': rb, 'R_constriction': rc}


def net_of(edges, bottom, top, plate=1.0, box=1000.0):
    nodes = sorted({e['id1'] for e in edges} | {e['id2'] for e in edges})
    return {'nodes': nodes, 'edges': edges, 'bottom': set(bottom), 'top': set(top), 'scale': 1.0,
            'plate_z': plate, 'box_x': box, 'box_y': box}


def dead_end(high, n_paths=30001, connect_dead=False):
    """Codex `cg_dead_end` — 바닥 0 · 위 1 · 경로 i (B–i–T · 1 S 둘) × n_paths + 막다른 노드 2 (B 에만 high S).
    connect_dead: 막다른 노드 대신 B–2 (high S) – 3 (1 S) – T (1 S) — 큰 간선이 자유 노드끼리 이어진다 (Jacobi 한 걸음으로는 안 풀린다).
    참 G = n_paths/2 (+ connect_dead 면 1/(2 + 1/high))."""
    edges = [Eg(0, 2, high)]
    if connect_dead:
        edges += [Eg(2, 3, 1.0), Eg(3, 1, 1.0)]
    base = 4 if connect_dead else 3
    for i in range(base, base + n_paths):
        edges += [Eg(0, i, 1.0), Eg(i, 1, 1.0)]
    exact = n_paths / 2.0 + ((1.0 / (2.0 + 1.0 / high)) if connect_dead else 0.0)
    return net_of(edges, {0}, {1}), exact


_MISSING = object()


@contextlib.contextmanager
def patched(mod, **fns):
    """모듈 전역 (cg · spsolve · gmres) 을 잠시 바꾼다 — measure_rho 가 하는 것과 같은 자리 (모듈 이름 조회)."""
    old = {k: getattr(mod, k, _MISSING) for k in fns}
    try:
        for k, v in fns.items():
            setattr(mod, k, v)
        yield
    finally:
        for k, v in old.items():
            if v is _MISSING:
                delattr(mod, k)
            else:
                setattr(mod, k, v)


def _load_old_module():
    """git 의 고치기 전 모듈을 별도 이름으로 싣는다 — 없으면 None (SKIP)."""
    try:
        src = subprocess.run(['git', '-C', ROOT, 'show', f'{OLD_REF}:scripts/network_conductivity.py'],
                             capture_output=True, check=True, timeout=60).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    d = tempfile.mkdtemp(prefix='nc_cert_old_')
    path = os.path.join(d, f'network_conductivity_{OLD_REF}.py')
    with open(path, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location(f'network_conductivity_{OLD_REF}', path)
    mod = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def chain(n=21, r=1.0, area=0.1, delta=0.05, clamp_at=None):
    """21 구 사슬 z 0..20 (판 20 · 상자 10 · 띠 L0).  clamp_at = 그 접촉의 c_cpl[22] 를 π(1.02 r)² 로 (원판 > π r_min² → physics g2 · H12 협착 0)."""
    A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': r} for i, z in enumerate(range(n), 1)}
    C = [{'id1': i, 'id2': i + 1, 'contact_area': (math.pi * (1.02 * r) ** 2 if i == clamp_at else area), 'delta': delta}
         for i in range(1, n)]
    return A, C


def se_am_bed():
    """SE 사슬 (type 1 · x 0) + AM 사슬 (type 2 · x 5) 둘 다 관통 — 이온 · 전자 · 열 세 채널이 다 돈다 (test_pipeline_provenance se_am 과 같은 모양)."""
    A = {i: dict(type=1, x=0., y=0., z=float(z), radius=1.) for i, z in enumerate(range(21), 1)}
    A.update({100 + k: dict(type=2, x=5., y=0., z=float(z), radius=1.) for k, z in enumerate(range(21))})
    C = [dict(id1=i, id2=i + 1, contact_area=0.1, delta=0.05) for i in range(1, 21)]
    C += [dict(id1=100 + k, id2=101 + k, contact_area=0.1, delta=0.05) for k in range(20)]
    return A, C


def lattice(nx_, ny_, nz_, seed, lo, hi):
    """정상 격자 망 (test_network_dirichlet D6 · D7 와 같은 만듦새) — 저항 균등 [lo, hi]."""
    import numpy as np
    rng = np.random.default_rng(seed)
    idx = {}
    for k in range(nz_):
        for j in range(ny_):
            for i in range(nx_):
                idx[(i, j, k)] = len(idx)
    edges = []
    for (i, j, k), u in idx.items():
        for di, dj, dk in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            v = idx.get((i + di, j + dj, k + dk))
            if v is not None:
                edges.append(Er(u, v, float(rng.uniform(lo, hi)), 0.0))
    bot = {u for (i, j, k), u in idx.items() if k == 0}
    top = {u for (i, j, k), u in idx.items() if k == nz_ - 1}
    return net_of(edges, bot, top, plate=float(nz_), box=float(nx_))


def _gz_items(path, tag):
    with gzip.open(path, 'rt') as fh:
        lines = fh.read().splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith(tag):
            head = ln.replace(tag, '').split()
            return head, [ln_.split() for ln_ in lines[i + 1:] if ln_ and not ln_.startswith('ITEM')]
    raise ValueError(path)


def load_real14():
    """커밋된 real_14 기준 덤프 (docs/data/real14_reference_20260928 · test_physics_area_g2 와 같은 읽기) → (atoms, contacts, type_map, plate_z, box)."""
    d = os.path.join(ROOT, 'docs', 'data', 'real14_reference_20260928')
    ha, ra = _gz_items(os.path.join(d, 'atom_2060000.liggghts.gz'), 'ITEM: ATOMS')
    ia = {k: ha.index(k) for k in ('id', 'type', 'x', 'y', 'z', 'radius')}
    A = {int(r[ia['id']]): {'type': int(r[ia['type']]), 'x': float(r[ia['x']]), 'y': float(r[ia['y']]),
                            'z': float(r[ia['z']]), 'radius': float(r[ia['radius']])} for r in ra}
    hc, rc = _gz_items(os.path.join(d, 'contact_2060000.liggghts.gz'), 'ITEM: ENTRIES')
    j1, j2, jA, jD = (hc.index('c_cpl[7]'), hc.index('c_cpl[8]'), hc.index('c_cpl[22]'), hc.index('c_cpl[23]'))
    C = [{'id1': int(float(r[j1])), 'id2': int(float(r[j2])), 'contact_area': float(r[jA]), 'delta': float(r[jD])} for r in rc]
    return A, C, {1: 'AM_P', 2: 'AM_S', 3: 'SE'}, 0.0302845, 0.05


def cert_ok(nc, c):
    """증서가 있고 도우미가 통과시키며 기록값이 독립 재계산과 맞는가 → (bool, 설명)."""
    cp = getattr(nc, 'certificate_problem', None)
    if not isinstance(c, dict):
        return False, f'증서 없음 ({type(c).__name__})'
    if cp is None:
        return False, 'certificate_problem 도우미 없음'
    prob = cp(c)
    ib, it, cr, rr = c.get('I_bottom'), c.get('I_top'), c.get('conservation_rel'), c.get('residual_rel')
    nums = all(isinstance(v, float) and math.isfinite(v) for v in (ib, it, cr, rr))
    good = (prob is None and nums and cr == cons_of(ib, it) and cr <= CONS_MAX and 0.0 <= rr <= RES_MAX
            and c.get('conservation_rel_max') == CONS_MAX and c.get('residual_rel_max') == RES_MAX and isinstance(c.get('method'), str))
    return good, f"prob {prob!r} · method {c.get('method')!r} · cons {cr!r} · res {rr!r}"


def json_clean(obj):
    """JSON 직렬화 가능 (NaN · inf 없이) 하고 왕복이 같다."""
    try:
        s = json.dumps(obj, allow_nan=False)
    except (TypeError, ValueError):
        return False
    return json.loads(s) == obj


def main():
    import network_conductivity as nc
    old = _load_old_module()
    if old is None:
        print(f'  (고치기 전 모듈 {OLD_REF} 를 git 에서 못 읽었다 — 비트 동일 대조는 SKIP)')

    # ══ S. G2R-03 반례 + 대조 ═══════════════════════════════════════════════════════════════════════
    def sS():
        res = {}
        for high in (1e6, 1e8, 1e10, 1e12, 1e14):
            n, exact = dead_end(high)
            G, q = quiet(nc.solve_network, n)
            res[high] = (G, q, dict(n['solve_info']['full']), exact)
        G14, q14, i14, ex = res[1e14]
        ok_true = G14 is not None and rel(G14, ex) <= 1e-9 and i14.get('status') == 'computed'
        ok_refused = G14 is None and i14.get('status') == 'not_computed' and i14.get('reason') == CONS_FAILED
        chk('S1 ★ G2R-03 반례 (10^14 막다른 간선 · 자유 노드 30,002 · CG 가지) — 참 G 15,000.5 (상대 1e-9) 또는 NOT_COMPUTED '
            '(current_conservation_failed) · 계산됐는데 틀린 값 없음 (옛: computed · cg · 30,001 = +100 %)',
            ok_true or ok_refused, f'G {G14!r} · q {q14!r} · {i14.get("status")} · {i14.get("reason")} · {i14.get("method")}')
        bad = [h for h in (1e6, 1e8, 1e10, 1e12)
               if not (res[h][0] is not None and rel(res[h][0], res[h][3]) <= 1e-9 and res[h][2].get('status') == 'computed'
                       and res[h][2].get('method') == 'cg')]
        chk('S2 대조 10^6 · 10^8 · 10^10 · 10^12 — 참값 그대로 (상대 1e-9) · computed · 첫 단 cg 가 채택', not bad,
            repr({h: (res[h][0], res[h][2].get('method')) for h in bad}))
        cb = []
        for h in (1e6, 1e8, 1e10, 1e12):
            G, _q, info, _ex = res[h]
            good, why = cert_ok(nc, info)
            if not (good and info.get('I_bottom') == G and rel(-info['I_top'], G) <= 1e-6):
                cb.append((h, why))
        chk('S3 ★ 대조 넷의 증서 — I_bottom = G · I_top ≈ −G · 보존 잔차 = 독립 재계산 ≤ 1e-6 · 내부 잔차 ≤ 1e-6 · 방법 · 허용치 기록 · '
            'certificate_problem 통과 (옛: 증서 없음)', not cb, repr(cb[:2]))
        att = i14.get('attempts') or []
        a0 = att[0] if att else {}
        good14, why14 = cert_ok(nc, i14)
        chk('S4 ★ 반례의 사다리 기록 — 첫 단 cg 가 보존 잔차로 떨어지고 (잔차 > 0.5 · I_top ≈ −3e-10) 직접해 단이 참값을 증서와 함께 낸다 '
            '(method ≠ cg · certificate_problem 통과)',
            ok_true and a0.get('method') == 'cg' and a0.get('outcome') == 'certificate_failed'
            and isinstance(a0.get('conservation_rel'), float) and a0['conservation_rel'] > 0.5
            and isinstance(a0.get('I_top'), float) and abs(a0['I_top']) < 1e-6
            and i14.get('method') == 'spsolve_fallback' and good14,
            f'attempts {[(a.get("method"), a.get("outcome"), a.get("conservation_rel")) for a in att]} · {why14}')
        chk('S5 허용치 상수 = 등록값 (보존 잔차 · 내부 잔차 1e-6) · 사유 이름',
            getattr(nc, 'DIRICHLET_CONSERVATION_REL_MAX', None) == CONS_MAX and getattr(nc, 'DIRICHLET_RESIDUAL_REL_MAX', None) == RES_MAX
            and getattr(nc, 'CURRENT_CONSERVATION_FAILED_REASON', None) == CONS_FAILED
            and getattr(nc, 'ZERO_RESISTANCE_REASON', None) == ZERO_R)
    _guard('S', sS)

    # ══ K. 사다리 단마다 · 모든 단 실패 ═══════════════════════════════════════════════════════════════
    def sK():
        import numpy as np
        orig_cg = nc.cg

        def boom(*_a, **_k):
            raise RuntimeError('주입: 직접해 실패 (사다리 시험)')
        n, ex = dead_end(1e14)
        with patched(nc, spsolve=boom):
            G, _q = quiet(nc.solve_network, n)
        info = n['solve_info']['full']
        good, why = cert_ok(nc, info)
        chk('K1 ★ 직접해가 막히면 Jacobi CG (SPD 대각 전처리 · 잔차 보정) — 10^14 반례 참값 (상대 1e-9) · 증서 통과 (옛: cg 30,001)',
            G is not None and rel(G, ex) <= 1e-9 and info.get('method') == 'cg+jacobi' and good, f'G {G!r} · {why}')
        n2, ex2 = dead_end(1e14, connect_dead=True)
        with patched(nc, spsolve=boom):
            G2, _q2 = quiet(nc.solve_network, n2)
        info2 = n2['solve_info']['full']
        good2, why2 = cert_ok(nc, info2)
        a2 = {a.get('method'): a for a in (info2.get('attempts') or [])}
        chk('K2 ★ 큰 간선이 자유 노드끼리 이어진 변형 (B–2 10^14 · 2–3 · 3–T) — Jacobi CG + 잔차 보정 (2 회 이상) 이 참값 15,001.0 (상대 1e-9) · '
            '증서 통과 · 첫 단 cg 는 보존 잔차로 떨어진다 (내부 잔차는 1e-6 밑 — 판별력 없음)',
            G2 is not None and rel(G2, ex2) <= 1e-9 and info2.get('method') == 'cg+jacobi' and good2
            and ((a2.get('cg+jacobi') or {}).get('refine_passes') or 0) >= 2
            and (a2.get('cg') or {}).get('outcome') == 'certificate_failed' and ((a2.get('cg') or {}).get('residual_rel') or 1.0) < RES_MAX,
            f'G {G2!r} vs {ex2!r} · {why2} · 단 {[(m, a.get("outcome"), a.get("refine_passes")) for m, a in a2.items()]}')
        n2b, _ex2b = dead_end(1e14, connect_dead=True)
        with patched(nc, spsolve=boom, DIRICHLET_REFINE_PASSES=1):
            r2b = quiet(nc.solve_network, n2b)
        i2b = n2b['solve_info']['full']
        chk('K2b ★ 잔차 보정을 끄면 (1 회) 두 Krylov 단이 다 ‖b‖ 상대 종료로 일찍 멈춰 증서 실패 → 틀린 값 대신 NOT_COMPUTED (current_conservation_failed)',
            r2b == (None, None) and i2b.get('status') == 'not_computed' and i2b.get('reason') == CONS_FAILED,
            repr((r2b, [(a.get('method'), a.get('outcome'), a.get('conservation_rel')) for a in i2b.get('attempts') or []])))

        def cg_no_prec(A, b, **kw):
            if kw.get('M') is not None:
                raise RuntimeError('주입: 전처리 CG 실패 (사다리 시험)')
            return orig_cg(A, b, **kw)
        n3, ex3 = dead_end(1e14)
        with patched(nc, spsolve=boom, cg=cg_no_prec):
            G3, _q3 = quiet(nc.solve_network, n3)
        info3 = n3['solve_info']['full']
        good3, why3 = cert_ok(nc, info3)
        chk('K3 ★ 직접해 · Jacobi CG 가 다 막히면 ILU + GMRES (ILU 를 CG 에 넣지 않는다) — 참값 (상대 1e-9) · 증서 통과',
            G3 is not None and rel(G3, ex3) <= 1e-9 and info3.get('method') == 'gmres+ilu' and good3, f'G {G3!r} · {why3}')

        def z_direct(A, b, *a, **k):
            return np.zeros(np.shape(b)[0])

        def z_krylov(A, b, *a, **k):
            return np.zeros(np.shape(b)[0]), 0                     # 수렴했다고 거짓 신고하는 0 해

        A21, C21 = chain()
        n4 = quiet(nc.build_network, A21, C21, [1], 1.0, 20.0, 10.0, 10.0, mode='ionic', type_map={1: 'SE'})
        with patched(nc, spsolve=z_direct, cg=z_krylov, gmres=z_krylov):
            r4 = quiet(nc.solve_network, n4, mode='full')
        i4 = n4['solve_info']['full']
        chk('K4 ★ 모든 단이 거짓 해 (0 · 수렴 신고) → (None, None) · NOT_COMPUTED · current_conservation_failed · 단마다 기록 (옛: 바닥 간선 전류를 G 로 게시)',
            r4 == (None, None) and i4.get('status') == 'not_computed' and i4.get('reason') == CONS_FAILED
            and len(i4.get('attempts') or []) >= 3 and all(a.get('outcome') != 'pass' for a in i4['attempts'])
            and getattr(nc, 'certificate_problem', lambda _i: None)(i4) is not None,
            repr((r4, i4.get('status'), i4.get('reason'), [(a.get('method'), a.get('outcome')) for a in i4.get('attempts') or []])))
        with patched(nc, spsolve=z_direct, cg=z_krylov, gmres=z_krylov):
            rd = quiet(nc.run_decomposition, A21, C21, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='hertzian', mode='ionic')
            ra = quiet(nc._run_all_networks, A21, C21, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode='hertzian')
        chk('K5 ★ run_decomposition — sigma_full None · 상태 not_computed · 사유 current_conservation_failed (CF · constr 도) · '
            '_run_all_networks 이온 채널 failed (사유에 current_conservation_failed — 게시 차단)',
            rd is not None and rd.get('sigma_full') is None and rd.get('sigma_full_status') == 'not_computed'
            and rd.get('sigma_full_reason') == CONS_FAILED and rd.get('sigma_bulk_net_reason') == CONS_FAILED
            and rd.get('sigma_constr_net_reason') == CONS_FAILED
            and ra is not None and ra.get('ionic_status') == 'failed' and CONS_FAILED in str(ra.get('ionic_status_reason')),
            repr({k: (rd or {}).get(k) for k in ('sigma_full', 'sigma_full_status', 'sigma_full_reason')})
            + f" · ionic {(ra or {}).get('ionic_status')!r}")
    _guard('K', sK)

    # ══ Z. GEN2-01 — 협착-only 의 R_c = 0 ══════════════════════════════════════════════════════════════
    def sZ():
        def zr_net():
            return net_of([Er(0, 2, 2.0, 0.0), Er(2, 1, 2.0, 1.0), Er(0, 1, 2.0, 10.0)], {0}, {1})
        n = zr_net()
        r = quiet(nc.solve_network, n, mode='constriction_only')
        i = n['solve_info']['constriction_only']
        chk('Z1 ★ GEN2-01 반례 (B–중간–T: R_c 0 · 1 Ω 직렬 ∥ B–T 10 Ω) — 협착-only = (None, None) · NOT_COMPUTED · '
            'zero_resistance_requires_contraction · 0 저항 간선 1 (옛: 0.1 S computed · 단락 수축 참값 1.1 S)',
            r == (None, None) and i.get('status') == 'not_computed' and i.get('reason') == ZERO_R and i.get('n_zero_resistance') == 1,
            repr((r, i.get('status'), i.get('reason'), i.get('n_zero_resistance'))))
        gF, _qF = quiet(nc.solve_network, n, mode='full')
        gB, _qB = quiet(nc.solve_network, n, mode='bulk_only')
        same = True
        if old is not None:
            no = zr_net()
            same = (hexf(gF) == hexf(quiet(old.solve_network, no, mode='full')[0])
                    and hexf(gB) == hexf(quiet(old.solve_network, no, mode='bulk_only')[0]))
        chk('Z2 같은 망의 FULL = 1/5 + 1/12 · CF = 1/4 + 1/2 (상대 1e-12) · computed · 고치기 전 모듈과 비트 동일 (FULL · CF 는 영향 없음)',
            gF is not None and gB is not None and rel(gF, 1 / 5 + 1 / 12) < 1e-12 and rel(gB, 0.75) < 1e-12
            and n['solve_info']['full'].get('status') == n['solve_info']['bulk_only'].get('status') == 'computed' and same,
            f'{gF!r} · {gB!r} · old 비트 동일 {same if old is not None else "SKIP"}')
        A, C = chain(clamp_at=10)
        rp = quiet(nc.run_decomposition, A, C, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='physics', mode='ionic')
        rh = quiet(nc._run_all_networks, A, C, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode='hertzian')
        h12 = (rh or {}).get('hertz_h12') or {}
        chk('Z3 ★ run_decomposition (physics g2 · 21 구 사슬 · 가운데 접촉 clamp) — sigma_constr_net None · 상태 not_computed · 사유 '
            'zero_resistance_requires_contraction (옛: 단락을 개방으로 바꿔 G 1.1e-16 = 반올림 잡음 · I_top 0 을 computed 0.0 으로 게시) · '
            'FULL · CF computed · H0 (Maxwell) 협착-only computed · H12 협착-only 같은 사유',
            rp is not None and rp.get('n_clamp_zero') == 1 and rp.get('sigma_constr_net') is None
            and rp.get('sigma_constr_net_status') == 'not_computed' and rp.get('sigma_constr_net_reason') == ZERO_R
            and rp.get('sigma_full_status') == 'computed' and rp.get('sigma_bulk_net_status') == 'computed'
            and (rh or {}).get('sigma_constr_net_status') == 'computed'
            and h12.get('sigma_constr_net_status') == 'not_computed' and h12.get('sigma_constr_net_reason') == ZERO_R,
            repr({k: (rp or {}).get(k) for k in ('n_clamp_zero', 'sigma_constr_net', 'sigma_constr_net_status', 'sigma_constr_net_reason')})
            + f" · H0 constr {(rh or {}).get('sigma_constr_net_status')!r} · H12 constr {h12.get('sigma_constr_net_status')!r}")
        if old is not None:
            op = quiet(old.run_decomposition, A, C, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='physics', mode='ionic')
            oh = quiet(old._run_all_networks, A, C, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode='hertzian')
            keys = ('sigma_full', 'sigma_bulk_net', 'sigma_full_mScm', 'sigma_bulk_net_mScm', 'sigma_full_status', 'sigma_bulk_net_status',
                    'R_brug_over_full')
            diff = [k for k in keys if hexf(rp.get(k)) != hexf(op.get(k))]
            diff += ['H0 ' + k for k in keys + ('sigma_constr_net', 'sigma_constr_net_status') if hexf(rh.get(k)) != hexf(oh.get(k))]
            diff += ['H12 ' + k for k in keys if hexf(h12.get(k)) != hexf((oh.get('hertz_h12') or {}).get(k))]
            chk('Z3b 같은 사슬의 FULL · CF (physics) · H0 세 가지 · H12 FULL · CF = 고치기 전 모듈과 비트 동일 (0 저항 정책은 협착-only 만)', not diff,
                repr(diff))
        else:
            skip('Z3b', 'git 객체 없음')
    _guard('Z', sZ)

    # ══ R. 생산 레코드 ════════════════════════════════════════════════════════════════════════════════
    BR = ('full', 'bulk_net', 'constr_net')

    def sR():
        cp = getattr(nc, 'certificate_problem', None)
        A, C = chain()
        bad = []
        for cm in ('hertzian', 'physics'):
            rd = quiet(nc.run_decomposition, A, C, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode=cm, mode='ionic')
            for b in BR:
                c = (rd or {}).get(f'solve_certificate_{b}')
                good, why = cert_ok(nc, c)
                if not (good and json_clean(c)):
                    bad.append((cm, b, why))
            if (rd or {}).get('solve_method_full') != ((rd or {}).get('solve_certificate_full') or {}).get('method'):
                bad.append((cm, 'solve_method_full ≠ 증서 method'))
        chk('R1 ★ run_decomposition 결과 — 가지마다 solve_certificate_{full,bulk_net,constr_net} (I_bottom · I_top · 보존 · 내부 잔차 · 방법 · 허용치 · '
            '단 기록) · 도우미 통과 · JSON 왕복 (NaN 없음) · solve_method_full = 증서 방법 (21 구 사슬 · Hertz · physics)', not bad, repr(bad[:3]))
        A2, C2 = se_am_bed()
        ra = quiet(nc._run_all_networks, A2, C2, [1], [2], {1: 'SE', 2: 'AM_P'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode='hertzian')
        bad2 = []
        for pre in ('', 'electronic_', 'thermal_'):
            for b in BR:
                good, why = cert_ok(nc, (ra or {}).get(f'{pre}solve_certificate_{b}'))
                if not good:
                    bad2.append((pre or 'ionic_', b, why))
        h12 = (ra or {}).get('hertz_h12') or {}
        for b in BR:
            good, why = cert_ok(nc, h12.get(f'solve_certificate_{b}'))
            if not good:
                bad2.append(('hertz_h12', b, why))
        chk('R2 ★ _run_all_networks (SE + AM 두 사슬) — 이온 · 전자 (electronic_) · 열 (thermal_) · H12 레코드 모두 세 가지의 증서 · 도우미 통과',
            not bad2 and json_clean({k: v for k, v in ra.items() if 'solve_certificate' in k}), repr(bad2[:3]))
        #  CLI = 웹앱 망 단계가 부르는 그 명령 (모드 파일 둘 · dual · legacy 를 쓴다)
        d = tempfile.mkdtemp(prefix='nc_cert_cli_')
        out = os.path.join(d, 'out')
        os.makedirs(out)
        with open(os.path.join(d, 'atoms.csv'), 'w') as f:
            f.write('id,type,x,y,z,radius\n' + ''.join(f'{i},{a["type"]},{a["x"]!r},{a["y"]!r},{a["z"]!r},{a["radius"]!r}\n' for i, a in A2.items()))
        with open(os.path.join(d, 'contacts.csv'), 'w') as f:
            f.write('id1,id2,fn_x,fn_y,fn_z,ft_x,ft_y,ft_z,contact_area,delta\n' + ''.join(
                f'{c["id1"]},{c["id2"]},0,0,0,0,0,0,{c["contact_area"]!r},{c["delta"]!r}\n' for c in C2))
        with open(os.path.join(out, 'mesh_info.json'), 'w') as f:
            json.dump({'plate_z': 20.0}, f)
        with open(os.path.join(out, 'input_params.json'), 'w') as f:
            json.dump({'box_x': 10.0, 'box_y': 10.0}, f)
        p = subprocess.run([sys.executable, os.path.join(HERE, 'network_conductivity.py'), os.path.join(d, 'atoms.csv'),
                            os.path.join(d, 'contacts.csv'), '-o', out, '-t', '1:SE,2:AM_P', '-s', '1'],
                           capture_output=True, text=True, timeout=600)
        bad3, seen = [], []
        if p.returncode == 0:
            def _strict(path):
                with open(path) as fh:
                    return json.load(fh, parse_constant=lambda c: (_ for _ in ()).throw(ValueError(f'비표준 상수 {c}')))
            recs = {}
            for fn in ('network_conductivity_hertzian.json', 'network_conductivity_physics.json', 'network_conductivity.json'):
                recs[fn] = _strict(os.path.join(out, fn))
            dual = _strict(os.path.join(out, 'network_conductivity_dual.json'))
            recs['dual.hertzian'], recs['dual.physics'] = dual.get('hertzian'), dual.get('physics')
            for name, rec in recs.items():
                seen.append(name)
                for pre in ('', 'electronic_', 'thermal_'):
                    good, why = cert_ok(nc, (rec or {}).get(f'{pre}solve_certificate_full'))
                    if not good:
                        bad3.append((name, pre or 'ionic_', why))
                if 'hertzian' in name or name == 'network_conductivity.json':
                    good, why = cert_ok(nc, ((rec or {}).get('hertz_h12') or {}).get('solve_certificate_full'))
                    if not good:
                        bad3.append((name, 'hertz_h12', why))
        chk('R3 ★ 실 망 단계 (CLI network_conductivity.py) 가 쓴 네 JSON (모드 둘 · dual · legacy) — 이온 · 전자 · 열 FULL 증서 + Hertz 쪽 H12 증서 · '
            '표준 JSON (NaN · Infinity 없음) · 도우미 통과',
            p.returncode == 0 and len(seen) == 5 and not bad3, f'rc {p.returncode} · {bad3[:2]} · {p.stderr[-300:]!r}')
        #  순수 도우미 — 기록만 본다 (반례마다 사유 · 정상은 None)
        if cp is not None:
            base = (ra or {}).get('solve_certificate_full') or {}
            cases = {
                '반례 첫 단 (I_b 30,001 · I_t −3e-10)': dict(base, I_bottom=30001.0, I_top=-3.0000999999995355e-10,
                                                         conservation_rel=cons_of(30001.0, -3.0000999999995355e-10)),
                '보존 잔차 기록 ≠ 전류 (과소 기록)': dict(base, conservation_rel=0.0, I_top=base.get('I_top', 0.0) * (1 + 1e-3)),
                '내부 잔차 1e-3': dict(base, residual_rel=1e-3),
                '내부 잔차 NaN': dict(base, residual_rel=float('nan')),
                'I_bottom 없음': {k: v for k, v in base.items() if k != 'I_bottom'},
                'I_bottom ≤ 0': dict(base, I_bottom=-base.get('I_bottom', 1.0), I_top=-base.get('I_top', -1.0)),
                '상태 not_computed': dict(base, status='not_computed', reason=CONS_FAILED),
                '모르는 방법 (cg+ilu)': dict(base, method='cg+ilu'),
                '증서 없음 (None)': None,
            }
            missed = [k for k, v in cases.items() if cp(v) is None]
            chk('R4 ★ certificate_problem (순수) — 정상 증서 None · 반례 첫 단 · 과소 기록 · 내부 잔차 · NaN · 결손 · G ≤ 0 · 상태 · 모르는 방법 · 없음 → 사유',
                cp(base) is None and not missed and all(isinstance(cp(v), str) and cp(v) for v in cases.values()), repr(missed))
        else:
            chk('R4 ★ certificate_problem (순수) — 도우미가 없다', False)
    _guard('R', sR)

    # ══ R5 · B. real_14 실침대 + 정상 망 비트 동일 ═══════════════════════════════════════════════════════
    def sReal():
        A, C, tm, pz, box = load_real14()
        rr = {cm: quiet(nc.run_decomposition, A, C, [3], 1000.0, pz, box, box, type_map=tm, contact_mode=cm, mode='ionic')
              for cm in ('hertzian', 'physics')}
        bad, meas = [], {}
        for cm, r in rr.items():
            for b in (('full', 'bulk_net', 'constr_net') if cm == 'hertzian' else ('full', 'bulk_net')):
                c = (r or {}).get(f'solve_certificate_{b}')
                good, why = cert_ok(nc, c)
                meas[f'{cm}/{b}'] = (c or {}).get('method'), (c or {}).get('conservation_rel'), (c or {}).get('residual_rel')
                if not good:
                    bad.append((cm, b, why))
        rp = rr['physics'] or {}
        chk('R5 ★ real_14 기준 덤프 (커밋 · 이온 망) — Hertz FULL · CF · 협착-only 와 physics FULL · CF 의 증서 통과 (실측 보존 · 내부 잔차는 아래) · '
            'physics 협착-only (clamp 접촉 있음) = NOT_COMPUTED zero_resistance_requires_contraction',
            not bad and rp.get('n_clamp_zero', 0) > 0 and rp.get('sigma_constr_net') is None
            and rp.get('sigma_constr_net_status') == 'not_computed' and rp.get('sigma_constr_net_reason') == ZERO_R
            and ((rp.get('solve_certificate_constr_net') or {}).get('n_zero_resistance') or 0) > 0,
            f'{bad[:2]} · clamp {rp.get("n_clamp_zero")} · ' + ' · '.join(f'{k} {m} cons {c!r} res {s!r}' for k, (m, c, s) in meas.items()))
        if old is not None:
            ro = {cm: quiet(old.run_decomposition, A, C, [3], 1000.0, pz, box, box, type_map=tm, contact_mode=cm, mode='ionic')
                  for cm in ('hertzian', 'physics')}
            keys = ('sigma_full', 'sigma_bulk_net', 'sigma_full_mScm', 'sigma_bulk_net_mScm', 'R_brug_over_full', 'sigma_full_status',
                    'sigma_bulk_net_status', 'solve_method_full')
            diff = [(cm, k) for cm in rr for k in keys if hexf(rr[cm].get(k)) != hexf(ro[cm].get(k))]
            diff += [('hertzian', k) for k in ('sigma_constr_net', 'sigma_constr_net_mScm', 'sigma_constr_net_status')
                     if hexf(rr['hertzian'].get(k)) != hexf(ro['hertzian'].get(k))]
            chk('B1 ★ real_14 이온 망 — Hertz 세 가지 · physics FULL · CF 의 σ · 상태 · 방법 = 고치기 전 모듈과 비트 동일 (첫 단 spsolve 가 증서 통과)',
                not diff, repr(diff))
        else:
            skip('B1', 'git 객체 없음')
    _guard('R5·B1', sReal)

    def sB():
        big = lattice(34, 34, 30, 7, 0.5, 2.0)
        g_new, _ = quiet(nc.solve_network, big)
        info = big['solve_info']['full']
        good, why = cert_ok(nc, info)
        chk(f'B2 ★ 큰 망 (34×34×30 · 자유 노드 {info.get("n_free")} > 30,000) — 첫 단 cg 채택 · 증서 통과 (실측 {why})',
            g_new is not None and info.get('method') == 'cg' and good and info.get('n_free') == 32368, f'G {g_new!r}')
        if old is not None:
            big_o = lattice(34, 34, 30, 7, 0.5, 2.0)
            g_old, _ = quiet(old.solve_network, big_o)
            small = lattice(3, 3, 6, 20261006, 0.2, 5.0)
            small_o = lattice(3, 3, 6, 20261006, 0.2, 5.0)
            gs_new, _ = quiet(nc.solve_network, small)
            gs_old, _ = quiet(old.solve_network, small_o)
            A, C = chain()
            rn = {cm: quiet(nc._run_all_networks, A, C, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm)
                  for cm in ('hertzian', 'physics')}
            ro = {cm: quiet(old._run_all_networks, A, C, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm)
                  for cm in ('hertzian', 'physics')}
            keys = ('sigma_full', 'sigma_bulk_net', 'sigma_constr_net', 'sigma_full_mScm', 'sigma_bulk_net_mScm', 'sigma_constr_net_mScm',
                    'R_brug_over_full', 'sigma_full_status', 'sigma_bulk_net_status', 'sigma_constr_net_status', 'solve_method_full',
                    'thermal_sigma_full_mScm', 'ionic_status', 'thermal_status')
            diff = [(cm, k) for cm in rn for k in keys if hexf(rn[cm].get(k)) != hexf(ro[cm].get(k))]
            diff += [('hertz_h12', k) for k in keys[:11] if hexf((rn['hertzian'].get('hertz_h12') or {}).get(k))
                     != hexf((ro['hertzian'].get('hertz_h12') or {}).get(k))]
            chk(f'B3 ★ 정상 망 = 고치기 전 모듈과 비트 동일 — 큰 망 cg G ({g_new!r}) · 작은 격자 spsolve G · 21 구 사슬 Hertz · physics 세 가지 · 열 · H12',
                hexf(g_new) == hexf(g_old) and hexf(gs_new) == hexf(gs_old) and not diff,
                f'{hexf(g_new)} vs {hexf(g_old)} · {hexf(gs_new)} vs {hexf(gs_old)} · {diff[:3]}')
        else:
            skip('B3', 'git 객체 없음')
    _guard('B', sB)

    print(f'\ntest_network_solve_certificate: {_ok}/{_ok + len(_fail)} PASS' + (f' · SKIP {len(_skip)}' if _skip else '')
          + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

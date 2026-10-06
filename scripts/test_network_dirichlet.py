#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""망 솔버 전극 = 정확 Dirichlet (`L2-05` · C1-1 · 1저자 비준 10-06 *"권고대로"*).

  python3 scripts/test_network_dirichlet.py

★ 시험 먼저 — 옛 코드 (HEAD 50de4e806) 는 가상 전원 · 싱크를 전극 띠에 g_b = max(100·Σg/n_el, 10·g_max, 1e-6) 로 잇는다 (`L2-05`).
  g_b 가 **모든 간선**의 합 · 최대에서 나오므로 전류가 0 인 막다른 가지 하나가 σ 를 바꾼다 (Codex 반례: 단일 경로 R = 1 →
  G 0.96153846 · 바닥 노드에 막다른 가지 하나 → 0.99996004 · +3.996 %).  D1 · D2 · D3 · D5 · D6 · D7 이 옛 코드에서 빨갛다.
★ 새 전극: 바닥 띠 B 의 V = 1 · 위 띠 T 의 V = 0 고정 → L_ff·x = −L_fB·1 · G = Σ_{b∈B} (L·V)_b · B ∩ T ≠ ∅ → (None, None) + 사유
  `boundary_overlap` · 자유 노드 ≤ 30,000 이면 spsolve · 그 위면 CG (rtol 1e-10 · atol 0 · 실패하면 ILU · SciPy < 1.12 는 tol) ·
  기록 `electrode_model = 'dirichlet_exact'` (망 solve_info · run_decomposition 결과).
  D1 Codex 반례 (바닥 노드의 막다른 가지) · D2 내부 노드의 막다른 가지 · D3 해석해 (직렬 · 병렬 · 휘트스톤 브리지 · L2-08 몫 · 양 끝이 다른 두 경로
  9/110) · D4 단위 척도 · D5 경계 겹침 · D6 전류 보존 · KCL · 장 출력 호환 (V_source 1.0) · 기록 · D7 큰 망 CG 경로 (독립 직접해 대조 · SciPy 키워드)
⚠ 범위 — 전극 처리의 식 시험이다.  띠 규칙 (L0 · L1 · L2) · 간선 저항 모델 · 194 배포값으로 확대하지 않는다 (배포값 변화 = 5–6 째 자리 · 설계 측정).
"""
import contextlib
import io
import math
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}' + (f'   {extra}' if extra else ''))
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {extra}' if extra else ''))


def _guard(label, fn):
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001
        chk(f'{label} — 예외 {type(e).__name__}: {e}', False)


def E(i, j, R, rc=0.0):
    """간선 하나 (R_total = R · R_bulk = R − rc · R_constriction = rc) — 솔버가 읽는 키만."""
    return {'id1': i, 'id2': j, 'R_total': R, 'R_bulk': R - rc, 'R_constriction': rc, 'R_Maxwell': 1e12, 'type1': 1, 'type2': 1,
            'delta': 0.0, 'delta_over_R': 0.0, 'regime': 'toy', 'r1': 1.0, 'r2': 1.0, 'd_ij': 1.0,
            'A_hertzian': 0.0, 'A_physics': 0.0, 'A_contact': 0.0}


def net_of(edges, bottom, top, plate=1.0, box=1.0):
    nodes = sorted({e['id1'] for e in edges} | {e['id2'] for e in edges})
    return {'nodes': nodes, 'edges': edges, 'bottom': set(bottom), 'top': set(top), 'scale': 1.0,
            'plate_z': plate, 'box_x': box, 'box_y': box}


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def G(nc, net, mode='full'):
    return quiet(nc.solve_network, net, mode=mode)[0]


def rel(a, b):
    return abs(a - b) / abs(b) if b else float('inf')


def main():
    import network_conductivity as nc

    # ── D1 · D2 Codex 반례 — 막다른 가지가 G 를 바꾸지 않는다 ──
    def s12():
        base = net_of([E(1, 2, 1.0)], {1}, {2})
        dead = net_of([E(1, 2, 1.0), E(1, 3, 1e-3)], {1}, {2})
        g0, g1 = G(nc, base), G(nc, dead)
        chk('D1 ★ 바닥 노드에 막다른 가지 (R 1e-3) — G 불변 · 단일 경로 R = 1 → G = 1 (상대 1e-12) (옛: 0.96153846 → 0.99996004 · +4.0 %)',
            g0 is not None and g1 is not None and rel(g0, 1.0) < 1e-12 and rel(g1, g0) < 1e-12, f'{g0!r} → {g1!r}')
        base_m = net_of([E(1, 4, 0.5), E(4, 2, 0.5)], {1}, {2})
        dead_m = net_of([E(1, 4, 0.5), E(4, 2, 0.5), E(4, 5, 1e-3)], {1}, {2})
        h0, h1 = G(nc, base_m), G(nc, dead_m)
        chk('D2 ★ 내부 노드에 막다른 가지 — G 불변 = 1 (상대 1e-12) (옛: 0.990099 → 0.999960 · +1.0 %)',
            h0 is not None and h1 is not None and rel(h0, 1.0) < 1e-12 and rel(h1, h0) < 1e-12, f'{h0!r} → {h1!r}')
    _guard('D1·D2', s12)

    # ── D3 해석해 ──
    def s3():
        Rs = [1.0, 2.0, 3.0, 4.0, 5.0]
        chain = net_of([E(k, k + 1, Rs[k]) for k in range(5)], {0}, {5})
        g_chain = G(nc, chain)
        par = net_of([E('b', 'a', 10.0, 9.0), E('a', 't', 10.0, 9.0), E('b', 'c', 1.0), E('c', 't', 1.0)], {'b'}, {'t'})
        g_par = G(nc, par)
        #  휘트스톤 브리지 — Fraction 으로 V_x · V_y 를 푼다 (독립 정확 해)
        R_bx, R_by, R_xt, R_yt, R_xy = map(Fraction, (1, 2, 2, 1, 3))
        g = {k: 1 / v for k, v in dict(bx=R_bx, by=R_by, xt=R_xt, yt=R_yt, xy=R_xy).items()}
        #  KCL (V_b = 1 · V_t = 0):  (g_bx+g_xt+g_xy) Vx − g_xy Vy = g_bx · −g_xy Vx + (g_by+g_yt+g_xy) Vy = g_by
        a11, a12, a22 = g['bx'] + g['xt'] + g['xy'], -g['xy'], g['by'] + g['yt'] + g['xy']
        det = a11 * a22 - a12 * a12
        Vx, Vy = (g['bx'] * a22 - a12 * g['by']) / det, (a11 * g['by'] - a12 * g['bx']) / det
        G_w = g['bx'] * (1 - Vx) + g['by'] * (1 - Vy)
        wh = net_of([E('b', 'x', 1.0), E('b', 'y', 2.0), E('x', 't', 2.0), E('y', 't', 1.0), E('x', 'y', 3.0)], {'b'}, {'t'})
        g_wh = G(nc, wh)
        chk('D3 ★ 해석해 — 직렬 1/ΣR = 1/15 · 공유 끝 병렬 1/20 + 1/2 = 0.55 · 휘트스톤 브리지 (Fraction 정확 해) — 상대 1e-12',
            None not in (g_chain, g_par, g_wh) and rel(g_chain, 1 / 15) < 1e-12 and rel(g_par, 0.55) < 1e-12
            and rel(g_wh, float(G_w)) < 1e-12, f'{g_chain!r} · {g_par!r} · {g_wh!r} vs {float(G_w)!r}')
        _G, _s, fd = quiet(nc.solve_network, net_of([E(0, 2, 10.0, 9.0), E(1, 3, 1.0)], {0, 1}, {2, 3}), mode='full', return_field=True)
        share, st = nc.constriction_power_share(fd)
        chk('D3b ★ 양 끝이 다른 두 경로 (C1d) — 협착 전력 몫 = 이상 전극 극한 9/110 정확 (옛 유한 전극 0.0916787 · +12.05 %)',
            st == 'computed' and share is not None and rel(share, 9.0 / 110.0) < 1e-12, f'{share!r}')
        _G2, _s2, fp = quiet(nc.solve_network, par, mode='full', return_field=True)
        share2, _st2 = nc.constriction_power_share(fp)
        chk('D3c L2-08 반례 (공유 끝) 몫 = 18/220 그대로 (전극이 공유 끝이면 옛 판도 같았다)', share2 is not None and rel(share2, 18 / 220) < 1e-12)
    _guard('D3', s3)

    # ── D4 단위 척도 ──
    def s4():
        e1 = [E(1, 4, 0.5), E(4, 2, 0.5), E(4, 5, 1e-3), E(1, 6, 2.0), E(6, 2, 0.7)]
        e7 = [E(e['id1'], e['id2'], 7.0 * e['R_total']) for e in e1]
        g1, g7 = G(nc, net_of(e1, {1}, {2})), G(nc, net_of(e7, {1}, {2}))
        chk('D4 단위 척도 — 모든 R ×7 → G ÷7 (상대 1e-12)', g1 is not None and g7 is not None and rel(7.0 * g7, g1) < 1e-12, f'{g1!r} · {g7!r}')
    _guard('D4', s4)

    # ── D5 경계 겹침 B ∩ T ≠ ∅ ──
    def s5():
        net = net_of([E(1, 2, 1.0), E(2, 3, 1.0)], {1, 2}, {2, 3})
        r = quiet(nc.solve_network, net, mode='full')
        info = (net.get('solve_info') or {}).get('full') or {}
        chk("D5 ★ B ∩ T ≠ ∅ (노드 2) → (None, None) · solve_info 사유 'boundary_overlap' (옛: 값이 나왔다)",
            r == (None, None) and info.get('reason') == 'boundary_overlap', repr((r, info)))
        A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': z, 'radius': 1.5} for i, z in enumerate((0.0, 0.8, 1.6, 2.4, 3.2, 4.0), 1)}
        C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.2, 'delta': 0.1} for i in range(1, 6)]
        rd = quiet(nc.run_decomposition, A, C, [1], 1.0, 4.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='hertzian', mode='ionic')
        chk("D5b run_decomposition — 얇은 침대 (띠 겹침 2 노드) → sigma_full None · 상태 not_computed · 사유 boundary_overlap · n_boundary_overlap 2",
            rd is not None and rd.get('sigma_full') is None and rd.get('sigma_full_status') == 'not_computed'
            and rd.get('sigma_full_reason') == 'boundary_overlap' and rd.get('n_boundary_overlap') == 2,
            repr({k: (rd or {}).get(k) for k in ('sigma_full', 'sigma_full_status', 'sigma_full_reason', 'n_boundary_overlap')}))
    _guard('D5', s5)

    # ── D6 전류 보존 · KCL · 장 출력 · 기록 ──
    def s6():
        import random
        rng = random.Random(20261006)
        nx_, ny_, nz_ = 3, 3, 6
        idx = {(i, j, k): 1 + i + nx_ * (j + ny_ * k) for i in range(nx_) for j in range(ny_) for k in range(nz_)}
        edges = []
        for (i, j, k), u in idx.items():
            for di, dj, dk in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
                v = idx.get((i + di, j + dj, k + dk))
                if v:
                    edges.append(E(u, v, rng.uniform(0.2, 5.0), 0.0))
        bot = {u for (i, j, k), u in idx.items() if k == 0}
        top = {u for (i, j, k), u in idx.items() if k == nz_ - 1}
        net = net_of(edges, bot, top, plate=6.0, box=3.0)
        Gx, sr, fld = quiet(nc.solve_network, net, mode='full', return_field=True)
        V = fld['node_V']
        cur = {u: 0.0 for u in V}
        for e in fld['edge_records']:
            cur[e['id1']] += e['I']
            cur[e['id2']] -= e['I']
        I_bot = sum(cur[u] for u in bot)
        I_top = sum(cur[u] for u in top)
        kcl = max(abs(cur[u]) for u in V if u not in bot and u not in top)
        chk('D6 ★ 전류 보존 — 바닥 띠에서 나간 전류 = G (ΔV 1) = 위 띠로 들어간 전류 · 자유 노드 KCL (|ΣI| ≤ 1e-10·G) · V ∈ [0, 1] · 띠 = 1 · 0',
            Gx is not None and rel(I_bot, Gx) < 1e-10 and rel(-I_top, Gx) < 1e-10 and kcl <= 1e-10 * Gx
            and all(-1e-12 <= v <= 1 + 1e-12 for v in V.values()) and all(V[u] == 1.0 for u in bot) and all(V[u] == 0.0 for u in top),
            f'G {Gx!r} · I_bot {I_bot!r} · I_top {I_top!r} · KCL {kcl:.3g}')
        info = (net.get('solve_info') or {}).get('full') or {}
        chk("D6b 장 출력 호환 — V_source = 1.0 · G_eff = G · σ_ratio = G·L/A · electrode_model = 'dirichlet_exact' (장 · solve_info) · 방법 spsolve",
            fld.get('V_source') == 1.0 and fld.get('G_eff') == Gx and rel(sr, Gx * 6.0 / 9.0) < 1e-12
            and fld.get('electrode_model') == info.get('electrode_model') == 'dirichlet_exact' and info.get('method') == 'spsolve',
            repr((fld.get('V_source'), info)))
        A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
        C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
        rd = quiet(nc.run_decomposition, A, C, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='hertzian', mode='ionic')
        chk("D6c run_decomposition 결과 electrode_model = 'dirichlet_exact' (세 풀이 같은 전극)", (rd or {}).get('electrode_model') == 'dirichlet_exact',
            repr((rd or {}).get('electrode_model')))
    _guard('D6', s6)

    # ── D7 큰 망 (자유 노드 > 30,000) → CG (rtol 1e-10) · 독립 직접해 대조 · SciPy 키워드 ──
    def s7():
        import numpy as np
        from scipy import sparse
        from scipy.sparse.linalg import spsolve
        nx_, ny_, nz_ = 34, 34, 30
        rng = np.random.default_rng(7)
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
                    edges.append(E(u, v, float(rng.uniform(0.5, 2.0))))
        bot = {u for (i, j, k), u in idx.items() if k == 0}
        top = {u for (i, j, k), u in idx.items() if k == nz_ - 1}
        net = net_of(edges, bot, top, plate=float(nz_), box=float(nx_))
        g_cg = G(nc, net)
        info = (net.get('solve_info') or {}).get('full') or {}
        #  독립 직접해 — 같은 라플라시안을 이 시험이 따로 짓고 Dirichlet 소거로 푼다
        n = len(idx)
        I = np.array([e['id1'] for e in edges]); J = np.array([e['id2'] for e in edges])
        gg = 1.0 / np.array([e['R_total'] for e in edges])
        L = sparse.coo_matrix((np.r_[gg, gg, -gg, -gg], (np.r_[I, J, I, J], np.r_[I, J, J, I])), shape=(n, n)).tocsr()
        fixed = np.zeros(n, bool); Vf = np.zeros(n)
        for u in bot:
            fixed[u], Vf[u] = True, 1.0
        for u in top:
            fixed[u] = True
        fr = np.flatnonzero(~fixed)
        x = spsolve(L[fr][:, fr].tocsc(), -(L[fr][:, np.flatnonzero(fixed)] @ Vf[fixed]))
        Vv = Vf.copy(); Vv[fr] = x
        g_ref = float(sum((L @ Vv)[u] for u in bot))
        chk(f'D7 ★ 자유 노드 {len(fr)} > 30,000 → CG 경로 (방법 {info.get("method")!r}) · 독립 직접해와 상대 ≤ 1e-8 · n_free 기록',
            g_cg is not None and info.get('method') in ('cg', 'cg+ilu') and rel(g_cg, g_ref) <= 1e-8 and info.get('n_free') == len(fr),
            f'{g_cg!r} vs {g_ref!r} · {info}')
        orig = nc.cg

        def _old_scipy_cg(A, b, **kw):
            if 'rtol' in kw:
                raise TypeError("cg() got an unexpected keyword argument 'rtol'")    # SciPy < 1.12 모양
            kw2 = dict(kw)
            kw2['rtol'] = kw2.pop('tol')
            return orig(A, b, **kw2)
        nc.cg = _old_scipy_cg
        try:
            net2 = net_of(edges, bot, top, plate=float(nz_), box=float(nx_))
            g_old = G(nc, net2)
        finally:
            nc.cg = orig
        chk('D7b SciPy < 1.12 (rtol 키워드 없음) → tol 키워드로 같은 해 (상대 1e-8)', g_old is not None and rel(g_old, g_ref) <= 1e-8, f'{g_old!r}')
        #  문턱 줄은 감사 (measure_rho — 소스 치환 앵커 `if n_nodes > 30000:`) 가 글자로 찾는다 → 상수와 같은 수 · 한 곳뿐이어야 한다
        src = open(nc.__file__, encoding='utf-8').read()
        anchor = f'if n_nodes > {nc.DIRICHLET_DIRECT_MAX_FREE}:'
        chk(f'D7c 직접해 ↔ CG 문턱 줄 = 상수 DIRICHLET_DIRECT_MAX_FREE ({nc.DIRICHLET_DIRECT_MAX_FREE}) · 소스에 한 번 (measure_rho 치환 앵커)',
            nc.DIRICHLET_DIRECT_MAX_FREE == 30000 and src.count(anchor) == 1, f'count={src.count(anchor)}')
    _guard('D7', s7)

    print(f'\ntest_network_dirichlet: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

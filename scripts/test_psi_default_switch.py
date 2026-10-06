#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ψ 배치 기본값 전환 — `L2-01` 세대 2 (1저자 개정 2026-10-06 · 계약 `docs/area_contract_20260913.md` 개정 노트).

  python3 scripts/test_psi_default_switch.py

★ 시험 먼저 — 옛 코드 (기본 = legacy_divide) 에서 ① ②(기본 팔) ③(기본 팔) ⑤(곱셈 라벨) ⑥ 이 빨갛다.
★ 무엇을 지키나:
  ① 기본값 = `PSI_MULTIPLY` (세대 2) — 모듈 상수 · build_network · run_decomposition · _run_all_networks 서명 · 망 기록
  ② 2 구 Physics 접촉 (s = a_eff/r_min ≈ 0.2 · 0.5 · 0.9) × 세 채널 — 기본 R_c = ψ/(σ_rel·k·2·a_eff) ·
     명시 `PSI_DIVIDE` R_c = 1/(σ_rel·k·2·a_eff·ψ) (상대 1e-12).  ψ · σ_rel · k 는 **동결 상수로 따로** 계산한다
     (솔버에서 빌리면 상수 변이가 기대값과 같이 움직인다 — audit_transport_cap_equivalence ⑦i · ⑦k 와 같은 규약)
  ③ 단조 — 기본 R_c 는 a_eff 에 단조 감소 · legacy 는 s > 0.4 에서 오른다 (L2-01 비단조 재현 · 최소 = s 0.4)
  ④ Hertz 가지 — 두 배치의 간선 · σ 가 비트 동일 (ψ 를 안 쓴다 · 계약 §3) · ④c (10-06) H12 민감도 팔은 늘 곱셈 (배치 인자와 무관)
  ⑤ tau_flux 협착 라벨 = 결과의 ψ 배치 (physics multiply → mikic_psi_multiply · legacy_divide → mikic_psi_divide ·
     hertz → maxwell_halfspace) — 손 레코드 · 실 생산자 둘 다.  ★ 10-06 밤 세대 계약 (G2R-02) — 명시 ψ 분모 실 생산자 팔은 세대 1 도 2 도 아닌 연구
     팔이라 τ 상태는 NOT_COMPUTED (invalid_input · 라벨은 그대로) · 방향은 생산자 σ_ratio 로 · ⑤c 옛 픽스처 (Hertz ψ multiply + physics ψ 없음 혼종) 는
     두 모드 다 ψ 기록 없는 진짜 옛 모양으로 고쳤다
  ⑥ `_run_all_networks` 의 세 채널 결과가 ψ 배치를 싣는다 (이온 psi_placement · electronic_psi_placement ·
     thermal_psi_placement) — 기본 · 명시 legacy 둘 다 (값 = 실제로 쓴 배치)
⚠ 범위 — 합성 2 구 · 사슬 픽스처의 식 · 표기 시험이다.  실침대 σ · 코퍼스 · 물리 정확도로 확대하지 않는다
  (배치 선택의 근거는 독립 기준해 `scripts/constriction_reference.py` · AREA-09 STEP 4).
"""
import contextlib
import inspect
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ok, _fail = 0, []

#  동결 oracle 상수 — 솔버에서 import 하지 않는다 (계약 §C 동결값 · network_conductivity 재료 상수)
PSI_EXP, PSI_FLOOR = 1.5, 1e-4
NCM_R0, NCM_BETA = 2.0, 1.5                      # σ_AM(r) = 1/(1+(r/r0)^β) — AM_P 만
K_AM, K_SE = 4.0e-2, 0.7e-2                      # 열 k_weight (AM–SE 조화평균)
#  2 구 픽스처의 겹침 → s (실측: 0.03 → 0.2028 · 0.1 → 0.5003 · 0.22 → 0.9037 · r = 1 · 척도 1)
S_TARGETS = ((0.03, 0.15, 0.25), (0.1, 0.45, 0.55), (0.22, 0.85, 0.95))


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}' + (f'   {extra}' if extra else ''))
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'   {extra}' if extra else ''))


def _k_thermal_am_se():
    kr = K_AM / K_SE
    return 2.0 * kr / (1.0 + kr)


#  채널 → (두 입자 type, type_map, σ_rel, k) — r = 1 µm (척도 1) 의 AM_P σ_rel = 1/(1+(1/2)^1.5)
CHANNELS = {
    'ionic': ((1, 1), {1: 'SE'}, 1.0, 1.0),
    'electronic': ((2, 2), {2: 'AM_P'}, 1.0 / (1.0 + (1.0 / NCM_R0) ** NCM_BETA), 1.0),
    'thermal': ((2, 1), {1: 'SE', 2: 'AM_P'}, 1.0, _k_thermal_am_se()),
}


def edge(nc, delta, mode='ionic', cm='physics', place=None, r=1.0):
    """2 구 접촉 한 간선 (audit_constriction_deleted selftest `net()` 꼴 — 반경 r · 척도 1 · 판 10 · 상자 1e4).
    place=None 이면 인자를 넘기지 않는다 (= 기본값 경로).
    ★ 10-06 세대 2 면적 (C2 · `film_area_g2`) 이 기본이 됐다 — 이 픽스처의 겹침 → s 목표 (0.2 · 0.5 · 0.9) 는 세대 1 면적으로 잡은 것이라
      physics 간선은 **명시 area_rule='physics_g1'** 로 짓는다 (ψ 식 · 배치 시험은 면적 규칙과 무관 — 세대 2 면적은 test_physics_area_g2).
      ψ 배치 인자는 그대로 기본 / 명시 두 길을 본다."""
    t, tm, _sr, _k = CHANNELS[mode]
    atoms = {1: {'type': t[0], 'radius': r, 'x': 0.0, 'y': 0.0, 'z': 0.0},
             2: {'type': t[1], 'radius': r, 'x': 2.0 * r - delta, 'y': 0.0, 'z': 0.0}}
    rows = [{'id1': 1, 'id2': 2, 'contact_area': 0.0, 'delta': delta}]
    kw = {} if place is None else {'psi_placement': place}
    if cm == 'physics':
        kw['area_rule'] = 'physics_g1'                          # ★ 10-06 — 픽스처의 s 목표를 잡은 면적 (위 docstring)
    with contextlib.redirect_stdout(io.StringIO()):
        n = nc.build_network(atoms, rows, set(t), 1.0, 10.0, box_x=1e4, box_y=1e4, mode=mode, type_map=dict(tm),
                             contact_mode=cm, **kw)
    return n['edges'][0], n


def oracle(e, mode):
    """간선의 면적 (솔버가 낸 A_contact — 면적은 재구현하지 않는다) 에서 s · ψ · 두 배치의 기대 R_c."""
    _t, _tm, sr, k = CHANNELS[mode]
    a = math.sqrt(e['A_contact'] / math.pi) if e['A_contact'] > 0 else 0.0
    r_min = min(e['r1'], e['r2'])
    a_eff = min(a, r_min)
    s = a_eff / r_min
    psi = max(1.0 - s, 0.0) ** PSI_EXP
    return dict(s=s, psi=psi, a_eff=a_eff, mul=psi / (sr * k * 2.0 * a_eff), div=1.0 / (sr * k * 2.0 * a_eff * psi))


def _rel(x, y):
    return abs(x - y) / abs(y) if y else float('inf')


def _bits(v):
    """비트 서명 — 실수는 float.hex · dict · list 는 재귀 (== 로는 −0.0/0.0 · NaN 을 못 가른다)."""
    if isinstance(v, dict):
        return {k: _bits(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_bits(x) for x in v]
    if isinstance(v, float) or type(v).__name__ in ('float64', 'float32'):
        return float(v).hex()
    return v


def _guard(label, fn):
    """한 절이 예외로 죽어도 나머지를 센다 (옛 코드 = 없는 인자 TypeError 도 FAIL 로)."""
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001
        chk(f'{label} — 예외 {type(e).__name__}: {e}', False)


def main():
    import network_conductivity as nc
    import tau_flux as tf

    # ── ① 기본값 = 곱셈 (세대 2) ──
    def s1():
        sig = {f.__name__: inspect.signature(f).parameters.get('psi_placement')
               for f in (nc.build_network, nc.run_decomposition, nc._run_all_networks)}
        chk('① PSI_PLACEMENT_DEFAULT == PSI_MULTIPLY (세대 2 · 10-06 개정) · legacy 는 PSI_DIVIDE 상수로 남는다',
            nc.PSI_PLACEMENT_DEFAULT == nc.PSI_MULTIPLY == 'multiply' and nc.PSI_DIVIDE == 'legacy_divide'
            and set(nc.PSI_PLACEMENTS) == {'multiply', 'legacy_divide'}, repr(nc.PSI_PLACEMENT_DEFAULT))
        chk('①b build_network · run_decomposition · _run_all_networks 의 psi_placement 기본 = multiply (서명)',
            all(p is not None and p.default == nc.PSI_MULTIPLY for p in sig.values()),
            repr({k: (None if p is None else p.default) for k, p in sig.items()}))
        _e, net = edge(nc, 0.1)
        chk('①c 인자 없이 지은 망의 기록 psi_placement = multiply (망이 세대를 들고 다닌다)', net.get('psi_placement') == 'multiply',
            repr(net.get('psi_placement')))
    _guard('①', s1)

    # ── ② 식 — 세 채널 × s ≈ 0.2 · 0.5 · 0.9 ──
    def s2():
        bad_mul, bad_div, bad_same, s_seen, n = [], [], [], [], 0
        for mode in CHANNELS:
            for d, lo, hi in S_TARGETS:
                e_def, _ = edge(nc, d, mode=mode)
                e_div, _ = edge(nc, d, mode=mode, place=nc.PSI_DIVIDE)
                e_mul, _ = edge(nc, d, mode=mode, place=nc.PSI_MULTIPLY)
                o = oracle(e_div, mode)
                n += 1
                s_seen.append((mode, d, round(o['s'], 4), lo < o['s'] < hi and o['psi'] > PSI_FLOOR))
                if not (_rel(e_def['R_constriction'], o['mul']) <= 1e-12):
                    bad_mul.append((mode, d, e_def['R_constriction'], o['mul']))
                if not (_rel(e_div['R_constriction'], o['div']) <= 1e-12):
                    bad_div.append((mode, d, e_div['R_constriction'], o['div']))
                if float(e_def['R_constriction']).hex() != float(e_mul['R_constriction']).hex():
                    bad_same.append((mode, d))
        chk('②a 픽스처가 목표 영역에 든다 — s ∈ (0.15, 0.25) · (0.45, 0.55) · (0.85, 0.95) · ψ > floor (세 채널)',
            n == 9 and all(x[3] for x in s_seen), str(s_seen[:3]))
        chk('②b ★ 기본 간선 R_c = ψ/(σ_rel·k·2·a_eff) (상대 1e-12 · 세 채널 × 세 s)', n == 9 and not bad_mul, str(bad_mul[:3]))
        chk('②c 명시 PSI_DIVIDE 간선 R_c = 1/(σ_rel·k·2·a_eff·ψ) (세대 1 재현 · 상대 1e-12)', n == 9 and not bad_div, str(bad_div[:3]))
        chk('②d 기본 = 명시 PSI_MULTIPLY (R_c float.hex 동일)', n == 9 and not bad_same, str(bad_same[:3]))
    _guard('②', s2)

    # ── ③ 단조 — 기본은 a_eff 에 단조 감소 · legacy 는 s > 0.4 에서 오른다 ──
    def s3():
        rows = []
        for i in range(2, 25):
            d = 0.01 * i                                            # 0.02 … 0.24 (s ≈ 0.15 … 0.97)
            e_def, _ = edge(nc, d)
            e_div, _ = edge(nc, d, place=nc.PSI_DIVIDE)
            o = oracle(e_div, 'ionic')
            rows.append((o['a_eff'], o['s'], e_def['R_constriction'], e_div['R_constriction']))
        a_mono = all(rows[i + 1][0] > rows[i][0] for i in range(len(rows) - 1))
        dec = all(rows[i + 1][2] < rows[i][2] for i in range(len(rows) - 1))
        hi_pairs = [(rows[i], rows[i + 1]) for i in range(len(rows) - 1) if rows[i][1] >= 0.4]
        rise = bool(hi_pairs) and all(b[3] > a[3] for a, b in hi_pairs)
        lo_fall = any(rows[i + 1][3] < rows[i][3] for i in range(len(rows) - 1) if rows[i + 1][1] < 0.4)
        chk('③a 전제: 겹침을 키우면 a_eff 가 단조 증가 (2 구 · 이온)', a_mono)
        chk('③b ★ 기본 (곱셈) R_c 는 a_eff 에 단조 감소 — 접촉을 키우면 저항이 준다', dec,
            f'R_c {rows[0][2]:.6g} → {rows[-1][2]:.6g}')
        chk(f'③c 명시 legacy 는 s ≥ 0.4 에서 a_eff 를 키우면 R_c 가 **오른다** ({len(hi_pairs)} 쌍 · L2-01 비단조) · s < 0.4 에서는 내려간다',
            rise and len(hi_pairs) >= 3 and lo_fall,
            f'legacy s≥0.4 첫·끝 R_c {hi_pairs[0][0][3]:.6g} → {hi_pairs[-1][1][3]:.6g}' if hi_pairs else '')
    _guard('③', s3)

    # ── ④ Hertz 가지는 배치와 무관 (비트 동일) ──
    def s4():
        bad = []
        for mode in CHANNELS:
            for d, _lo, _hi in S_TARGETS:
                e_a, _ = edge(nc, d, mode=mode, cm='hertzian', place=nc.PSI_DIVIDE)
                e_b, _ = edge(nc, d, mode=mode, cm='hertzian', place=nc.PSI_MULTIPLY)
                e_c, _ = edge(nc, d, mode=mode, cm='hertzian')
                if not (_bits(e_a) == _bits(e_b) == _bits(e_c)):
                    bad.append((mode, d))
        chk('④a Hertz 간선 (전 필드) — PSI_DIVIDE · PSI_MULTIPLY · 기본이 비트 동일 (세 채널 × 세 겹침)', not bad, str(bad))
        A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
        C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
        keys = ('sigma_full', 'sigma_bulk_net', 'sigma_constr_net', 'sigma_full_mScm', 'percolating_fraction', 'phi_se')
        got = {}
        for p in (nc.PSI_DIVIDE, nc.PSI_MULTIPLY, None):
            kw = {} if p is None else {'psi_placement': p}
            with contextlib.redirect_stdout(io.StringIO()):
                r = nc.run_decomposition(A, C, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='hertzian',
                                         mode='ionic', **kw)
            got[p] = _bits({k: r.get(k) for k in keys})
        chk('④b Hertz 21 구 사슬 run_decomposition σ (FULL · CF · CONSTR) — 두 배치 · 기본이 비트 동일',
            got[nc.PSI_DIVIDE] == got[nc.PSI_MULTIPLY] == got[None], str(got[None]))
        #  ★ 10-06 H12 (C1-3) — Hertz 민감도 팔은 ψ 를 **늘 곱한다** (psi_placement 는 physics 가지의 배치) → 두 배치 · 기본이 비트 동일 · R_c = ψ·R_Maxwell
        bad12 = []
        for mode in CHANNELS:
            for d, _lo, _hi in S_TARGETS:
                t, tm, _sr, _k = CHANNELS[mode]
                atoms = {1: {'type': t[0], 'radius': 1.0, 'x': 0.0, 'y': 0.0, 'z': 0.0},
                         2: {'type': t[1], 'radius': 1.0, 'x': 2.0 - d, 'y': 0.0, 'z': 0.0}}
                a2 = d * (4.0 - d) / 4.0 * math.pi                    # 같은 반경 교차 원판 (c_cpl[22] 기하)
                rows = [{'id1': 1, 'id2': 2, 'contact_area': a2, 'delta': d}]
                es = []
                for p in (nc.PSI_DIVIDE, nc.PSI_MULTIPLY, None):
                    kw = {} if p is None else {'psi_placement': p}
                    with contextlib.redirect_stdout(io.StringIO()):
                        es.append(nc.build_network(atoms, rows, set(t), 1.0, 10.0, box_x=1e4, box_y=1e4, mode=mode, type_map=dict(tm),
                                                   contact_mode='hertzian', hertz_constriction='mikic_psi_multiply',
                                                   bulk_model='sphere_segment', **kw)['edges'][0])
                o = oracle(es[0], mode)
                if not (_bits(es[0]) == _bits(es[1]) == _bits(es[2])
                        and (o['psi'] <= PSI_FLOOR or _rel(es[0]['R_constriction'], o['mul']) <= 1e-12)):
                    bad12.append((mode, d))
        chk('④c ★ H12 (Hertz ψ 곱 + 구 조각 bulk · 10-06) — ψ 배치 인자와 무관 (두 배치 · 기본 비트 동일) · R_c = ψ/(σ·k·2·a_eff) (세 채널 × 세 겹침)',
            not bad12, str(bad12))
    _guard('④', s4)

    # ── ⑤ tau_flux 협착 라벨 = 결과의 ψ 배치 ──
    def s5():
        led = {'thickness_um': 30.0, 'thickness_mass_conserving_um': 28.5, 'phi_se_mass_conserving': 0.21}

        def rec(mode, **kw):
            q, s0 = (0.05 if mode == 'hertzian' else 0.08), 0.003
            b = {'sigma_full': q, 'sigma_full_mScm': round(q * s0 * 1000, 6), 'percolating_fraction': 0.9,
                 'boundary_rule': 'L0', 'boundary_band_frac': 0.06, 'phi_se': round(0.21 * 28.5 / 30.0, 4),
                 'resistance_model': 'maxwell' if mode == 'hertzian' else 'mikic', 'contact_mode': mode,
                 'sigma_full_status': 'computed', 'sigma_grain_S_cm': s0,
                 'temperature_provenance': {'T_C': None, 'T_ref_C': 25.0, 'sigma_ion_T_factor': 1.0, 'T_dependence': 'NOT_MODELLED'}}
            b.update(kw)
            return b

        def lab(**kw):
            o = tf.ion_columns({'hertzian': rec('hertzian', psi_placement=kw.get('h_psi', 'multiply')),
                                'physics': rec('physics', **({'psi_placement': kw['p_psi']} if 'p_psi' in kw else {}))}, led, 92.0)
            return o['ion_net_constriction_hertz'], o['ion_net_constriction_physics'], o['ion_net_psi_physics'], o['ion_net_psi_hertz']
        #  ★ 10-06 밤 (G2R-02) — ⑤c 의 "ψ 기록 없는 옛 산출물" 은 두 모드 다 ψ 기록이 없다 (09-15 깃발 전 생산자는 어느 결과에도 psi_placement 를 안 썼다).
        #    옛 픽스처는 Hertz 에 multiply (세대 2 표지) 를 둔 혼종이었다 — 새 세대 계약은 세대 2 표지가 남은 레코드의 빈 ψ 를 세대 1 로 추론하지 않는다
        #    (unknown:mikic/None · 세대 계약 위반 — test_gen2_role_contract R3).  라벨 규칙 (기록 없음 = 세대 1) 자체는 그대로 시험한다.
        m, d_, miss, unk = lab(p_psi='multiply'), lab(p_psi='legacy_divide'), lab(h_psi=None), lab(p_psi='foo')
        chk('⑤a 손 레코드 — physics + multiply → mikic_psi_multiply · ψ 칸 multiply · hertz → maxwell_halfspace · hertz ψ 칸 빈칸',
            m == ('maxwell_halfspace', 'mikic_psi_multiply', 'multiply', ''), repr(m))
        chk('⑤b 손 레코드 — physics + legacy_divide → mikic_psi_divide (세대 1 라벨 그대로)',
            d_ == ('maxwell_halfspace', 'mikic_psi_divide', 'legacy_divide', ''), repr(d_))
        chk('⑤c ψ 기록 없는 mikic (09-15 깃발 도입 전 산출물 = 세대 1 · 두 모드 다 ψ 기록 없음) → mikic_psi_divide · ψ 칸 빈칸 · 모르는 ψ → unknown 표지',
            miss == ('maxwell_halfspace', 'mikic_psi_divide', '', '') and unk[1] == 'unknown:mikic/foo', repr((miss, unk)))
        A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
        C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
        v_se = 21 * 4.0 / 3.0 * math.pi
        eps_s, eps_u = 1.0 - v_se / (10.0 * 10.0 * 20.0), 0.97
        led2 = {'thickness_um': 20.0, 'thickness_mass_conserving_um': 20.0 * (1 - eps_s) / (1 - eps_u),
                'phi_se_mass_conserving': 1 - eps_u}
        out, sig = {}, {}
        for tag, kw in (('default', {}), ('legacy', {'psi_placement': nc.PSI_DIVIDE})):
            with contextlib.redirect_stdout(io.StringIO()):
                dk = {cm: nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm, **kw)
                      for cm in ('hertzian', 'physics')}
            dk = json.loads(json.dumps(dk))                         # 디스크 모양
            o = tf.ion_columns(dk, led2, 100.0)
            out[tag] = (o['ion_net_constriction_physics'], o['ion_net_psi_physics'], o['ion_net_constriction_hertz'],
                        o['ion_net_status_physics'], o['tau2_ion_physics'], tf.reason_code(o['ion_net_status_reason_physics']))
            sig[tag] = dk['physics']['sigma_full']
        #  ★ 10-06 밤 (G2R-02 · 1저자 비준 세대 계약) — 명시 ψ 분모 (세대 2 생산자 + PSI_DIVIDE) 는 세대 1 도 2 도 아닌 **연구 팔**이다 (전극 dirichlet_exact ·
        #    physics_g2 면적 위의 ψ 분모 · 세대 1 전극은 더 만들 수 없다) → τ 인계 소비자는 세대 계약 위반 (NOT_COMPUTED invalid_input) 으로 막는다
        #    (인계 · 학습 표에 들어가지 않는다).  라벨 (mikic_psi_divide · legacy_divide) 은 결과의 실제 배치 그대로 보인다.
        chk('⑤d 실 생산자 21 구 사슬 — 기본 = mikic_psi_multiply · multiply · OK · 명시 legacy (연구 팔) = 라벨 mikic_psi_divide · legacy_divide 그대로 · '
            '상태 NOT_COMPUTED (invalid_input · 세대 계약 — 인계에 안 실린다)',
            out['default'][:4] == ('mikic_psi_multiply', 'multiply', 'maxwell_halfspace', 'OK')
            and out['legacy'][:4] == ('mikic_psi_divide', 'legacy_divide', 'maxwell_halfspace', 'NOT_COMPUTED')
            and out['legacy'][5] == 'invalid_input' and out['legacy'][4] is None, repr(out))
        #  방향 (세대 2 곱셈 → σ 상향 = tau2 하향) 은 생산자 σ_ratio 로 직접 본다 (τ 소비자는 연구 팔을 받지 않는다)
        chk('⑤e 같은 사슬의 physics σ_ratio — 세대 2 (곱셈) > 명시 ψ 분모 (곱셈 = 활성 간선 R_c 가 ψ² 배 → σ 상향 = tau2 하향 · 계약 §C 방향)',
            isinstance(sig['default'], float) and isinstance(sig['legacy'], float) and sig['default'] > sig['legacy'],
            f"physics sigma_full ψ 분모 {sig['legacy']!r} → 곱셈 {sig['default']!r}")
    _guard('⑤', s5)

    # ── ⑥ 세 채널 결과가 ψ 배치를 싣는다 ──
    def s6():
        mA, mC = {}, []
        for i, z in enumerate(range(21), 1):
            mA[i] = {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0}            # SE 사슬
            mA[100 + i] = {'type': 2, 'x': 3.0, 'y': 0.0, 'z': float(z), 'radius': 1.0}      # AM 사슬 (떨어져 있음)
        mC = ([{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
              + [{'id1': 100 + i, 'id2': 101 + i, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)])
        got = {}
        for cm in ('physics', 'hertzian'):
            for tag, kw in (('default', {}), ('legacy', {'psi_placement': nc.PSI_DIVIDE})):
                with contextlib.redirect_stdout(io.StringIO()):
                    ra = nc._run_all_networks(mA, mC, [1], [2], {1: 'SE', 2: 'AM_P'}, 1.0, 20.0, 10.0, 10.0, None,
                                              contact_mode=cm, **kw)
                got[(cm, tag)] = (ra.get('psi_placement'), ra.get('electronic_psi_placement'), ra.get('thermal_psi_placement'),
                                  ra.get('electronic_status'), ra.get('thermal_status'))
        chk('⑥a ★ 기본 — 이온 · 전자 · 열 결과가 모두 psi_placement = multiply 를 싣는다 (전자 · 열 채널이 실제로 풀렸다)',
            got[('physics', 'default')] == ('multiply', 'multiply', 'multiply', 'computed', 'computed'), repr(got[('physics', 'default')]))
        chk('⑥b 명시 PSI_DIVIDE — 세 채널 모두 legacy_divide (값 = 실제로 쓴 배치 · 상수 표기가 아니다)',
            got[('physics', 'legacy')] == ('legacy_divide',) * 3 + ('computed', 'computed'), repr(got[('physics', 'legacy')]))
        chk('⑥c Hertz 결과도 같은 표기를 싣는다 (Hertz 는 ψ 를 안 쓴다 — 값 무관 · 표기만)',
            got[('hertzian', 'default')][:3] == ('multiply',) * 3 and got[('hertzian', 'legacy')][:3] == ('legacy_divide',) * 3,
            repr((got[('hertzian', 'default')], got[('hertzian', 'legacy')])))
    _guard('⑥', s6)

    print(f'\ntest_psi_default_switch: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

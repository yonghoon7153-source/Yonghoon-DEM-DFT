#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""망 세대 2 — CF 가드 (C1-5) · Hertz H12 민감도 팔 (C1-3) · 세대 표기 · 세대 섞임 거부 (1저자 비준 10-06 *"권고대로"*).

  python3 scripts/test_network_generation2.py

★ 시험 먼저 — 옛 코드 (HEAD 50de4e806) 에서 빨갛다:
  C  CF q > 1.5 가드 — 옛 판은 CONTACT_FREE · CONSTRICTION_ONLY 가지에도 σ_ratio > 1.5 → None 을 걸어 "모형 과전도" 를 풀이 실패처럼 지웠다
     (LHSx CF 29 행 solve_failed · q = −0.222 + 0.233·φ·CN · R² 0.985 · 설계 측정).  새 판: 가드는 FULL 에만 · CF · 협착-only 는 값 유지 +
     상태 'model_over_conduction' (진단 열만 · 학습 열 아님).
  H  H12 — Hertz 협착 ψ 곱셈 + 구 조각 bulk 를 **짝으로만** (H1 단독 = ψ 만 · H2 단독 = bulk 만은 거부).  h_i = clip((d² + r_i² − r_j²)/(2d), 0, r_i) ·
     V_i = π(r_i² h_i − h_i³/3) · R_bulk,i = h_i²/(σ_i·k·V_i) · R_c = ψ/(σ·k·2·a_eff) (ψ ≤ 1e-4 → 0).  Hertz 기본 = H0 (Maxwell + 원기둥 반 d) 그대로
     (세대 1 과 같은 협착 · bulk).  H12 는 이온 민감도 레코드 (`hertz_h12` — Hertz 결과 안에 · `_run_all_networks` 의 hertzian 실행이 함께 낸다) 로만.
  E  세대 표기 — 결과 · τ 인계 열에 전극 (`ion_net_electrode_<m>` = dirichlet_exact) · bulk (`ion_net_bulk_<m>`) · 면적 규칙 (`ion_net_area_rule_<m>`) ·
     표기 없는 옛 산출물 = 이력 사실 (전극 virtual_source_legacy · 면적 physics_g1 · bulk cylinder_half_d) · 한 행 안 · 여러 행 사이 세대 섞임 거부.
★ 10-06 밤 세대 계약 (Codex G2R-01 · 02 · 1저자 비준) 으로 뜻을 고친 넷 — E2 옛 산출물 픽스처는 세대 2 표지를 **전부** 뺀다 (옛 픽스처는 진단 키 ·
  채널 표기를 남겨 세대 2 숫자에 세대 1 표기를 붙인 혼종이었다 — 새 계약은 그런 부분 결손을 옛 세대로 추론하지 않는다 · 194 역사 레코드에는 표지가 하나도
  없다) · E4 세대 축 = 세대 칸 + 모드별 협착 · bulk 까지 · E7 열 50 (공통 세대 칸 ion_net_generation) · H5b H12 없는 세대 2 결과 = 세대 계약 위반
  (부분 결손 — 주 두 모드도 NOT_COMPUTED · 생산자는 hertzian 실행에 늘 H12 를 함께 낸다).  역할 · 닫힌 열거 · 코호트 반례 = test_gen2_role_contract.
⚠ 범위 — 합성 망 · 2 구 · 21 구 사슬의 식 · 표기 시험이다.  σ 의 물리 정확도 · 194 배포값으로 확대하지 않는다 (H12 = 민감도 · 기본 학습 열 제외).
"""
import contextlib
import copy
import io
import json
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ok, _fail = 0, []

#  동결 oracle 상수 (network_conductivity 의 재료 상수 — import 하지 않는다)
PSI_EXP, PSI_FLOOR = 1.5, 1e-4
NCM_R0, NCM_BETA = 2.0, 1.5
K_AM, K_SE = 4.0e-2, 0.7e-2


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


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def rel(a, b):
    return abs(a - b) / abs(b) if b else float('inf')


def E(i, j, rb, rc):
    return {'id1': i, 'id2': j, 'R_total': rb + rc, 'R_bulk': rb, 'R_constriction': rc, 'R_Maxwell': 1e12, 'type1': 1, 'type2': 1,
            'delta': 0.0, 'delta_over_R': 0.0, 'regime': 'toy', 'r1': 1.0, 'r2': 1.0, 'd_ij': 1.0,
            'A_hertzian': 0.0, 'A_physics': 0.0, 'A_contact': 0.0}


def chain(n=21, r=1.0, area=0.1, delta=0.05):
    A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': r} for i, z in enumerate(range(n), 1)}
    C = [{'id1': i, 'id2': i + 1, 'contact_area': area, 'delta': delta} for i in range(1, n)]
    return A, C


def sphere_seg_R(ri, rj, d, sk):
    """구 조각 bulk 반쪽 (독립 구현) — h_i²/(σk·V_i)."""
    h = min(max((d * d + ri * ri - rj * rj) / (2.0 * d), 0.0), ri)
    if h <= 0:
        return 0.0
    V = math.pi * (ri * ri * h - h ** 3 / 3.0)
    return h * h / (sk * V)


def main():
    import network_conductivity as nc
    import tau_flux as tf

    # ══ C. CF 가드 = FULL 만 ═════════════════════════════════════════════════════════════════════
    def sC():
        net = {'nodes': [1, 2], 'edges': [E(1, 2, 0.1, 0.9)], 'bottom': {1}, 'top': {2}, 'scale': 1.0, 'plate_z': 1.0,
               'box_x': 1.0, 'box_y': 1.0}
        gF, qF = quiet(nc.solve_network, net, mode='full')
        gB, qB = quiet(nc.solve_network, net, mode='bulk_only')
        infoB = (net.get('solve_info') or {}).get('bulk_only') or {}
        chk("C1 ★ 한 간선 (R_bulk 0.1 · R_c 0.9) — FULL q = 1.0 (가드 밑) 값 · CF q = 10 > 1.5 → 값 유지 + solve_info 상태 'model_over_conduction' "
            "(옛: CF None)", qF is not None and rel(qF, 1.0) < 1e-12 and qB is not None and rel(qB, 10.0) < 1e-12
            and infoB.get('status') == 'model_over_conduction', repr((qF, qB, infoB)))
        net2 = {'nodes': [1, 2], 'edges': [E(1, 2, 0.1, 0.4)], 'bottom': {1}, 'top': {2}, 'scale': 1.0, 'plate_z': 1.0,
                'box_x': 1.0, 'box_y': 1.0}
        r2 = quiet(nc.solve_network, net2, mode='full')
        chk('C1b FULL q = 2 > 1.5 → (None, None) 그대로 (단상 가드는 FULL 에 남는다)', r2 == (None, None), repr(r2))
        A, Cc = chain()
        rd = quiet(nc.run_decomposition, A, Cc, [1], 1.0, 20.0, 1.0, 1.0, type_map={1: 'SE'}, contact_mode='hertzian', mode='ionic')
        chk("C2 ★ run_decomposition (21 구 사슬 · 상자 1 × 1) — FULL computed · CF σ_ratio ≈ π > 1.5 값 유지 · sigma_bulk_net_status "
            "'model_over_conduction' · R_brug_over_full 계산 (옛: CF None)",
            rd is not None and rd.get('sigma_full_status') == 'computed' and isinstance(rd.get('sigma_bulk_net'), float)
            and rd['sigma_bulk_net'] > 1.5 and rd.get('sigma_bulk_net_status') == 'model_over_conduction'
            and isinstance(rd.get('R_brug_over_full'), float),
            repr({k: (rd or {}).get(k) for k in ('sigma_full', 'sigma_full_status', 'sigma_bulk_net', 'sigma_bulk_net_status',
                                                 'sigma_bulk_net_reason', 'R_brug_over_full')}))
        rok = quiet(nc.run_decomposition, A, Cc, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='hertzian', mode='ionic')
        chk("C2b 양성 대조 — 상자 10 × 10 (CF q 0.03) 은 상태 computed 그대로", (rok or {}).get('sigma_bulk_net_status') == 'computed')
    _guard('C', sC)

    # ══ H. H12 짝 팔 ═════════════════════════════════════════════════════════════════════════════
    def _edge(mode, delta, r1=0.5, r2=6.0, t=(1, 1), tm=None, **kw):
        tm = tm or {1: 'SE'}
        d = r1 + r2 - delta
        atoms = {1: {'type': t[0], 'radius': r1, 'x': 0.0, 'y': 0.0, 'z': 0.0},
                 2: {'type': t[1], 'radius': r2, 'x': d, 'y': 0.0, 'z': 0.0}}
        a2 = (4 * d * d * r1 * r1 - (d * d - r2 * r2 + r1 * r1) ** 2) / (4 * d * d)
        rows = [{'id1': 1, 'id2': 2, 'contact_area': math.pi * max(a2, 0.0), 'delta': delta}]
        n = quiet(nc.build_network, atoms, rows, set(t), 1.0, 10.0, box_x=1e4, box_y=1e4, mode=mode, type_map=tm, **kw)
        return n['edges'][0], n

    def sH():
        H12 = dict(hertz_constriction='mikic_psi_multiply', bulk_model='sphere_segment')
        bad = []
        for lbl, kw in (('H1 단독 (ψ 만)', dict(hertz_constriction='mikic_psi_multiply')),
                        ('H2 단독 (bulk 만)', dict(bulk_model='sphere_segment')),
                        ('physics + H12', dict(contact_mode='physics', **H12)),
                        ('모르는 협착', dict(hertz_constriction='holm')), ('모르는 bulk', dict(bulk_model='cone'))):
            try:
                _edge('ionic', 0.05, **kw)
                bad.append(lbl)
            except ValueError:
                pass
        chk('H1 ★ 짝 강제 — H1 단독 · H2 단독 · physics 모드의 H12 · 모르는 값 → ValueError', not bad, repr(bad))
        #  식 oracle — 세 채널 (σ_rel · k) · 반지름 순서 둘 · s 두 점
        CH = {'ionic': ((1, 1), {1: 'SE'}), 'electronic': ((2, 2), {2: 'AM_P'}), 'thermal': ((2, 1), {1: 'SE', 2: 'AM_P'})}
        badf, n = [], 0
        for mode, (t, tm) in CH.items():
            for r1, r2 in ((0.5, 6.0), (6.0, 0.5), (1.0, 1.0)):
                for delta in (0.02, 0.2):
                    e, _n = _edge(mode, delta, r1=r1, r2=r2, t=t, tm=tm, **H12)
                    lab1, lab2 = tm[t[0]], tm[t[1]]
                    srel = [1.0 / (1.0 + (max(r, 0.1) / NCM_R0) ** NCM_BETA) if (mode == 'electronic' and lb == 'AM_P') else 1.0
                            for r, lb in ((e['r1'], lab1), (e['r2'], lab2))]
                    kr = K_AM / K_SE
                    k = (kr if (lab1 != 'SE' and lab2 != 'SE') else 1.0 if (lab1 == 'SE' and lab2 == 'SE') else 2 * kr / (1 + kr)) \
                        if mode == 'thermal' else 1.0
                    want_b = sphere_seg_R(e['r1'], e['r2'], e['d_ij'], srel[0] * k) + sphere_seg_R(e['r2'], e['r1'], e['d_ij'], srel[1] * k)
                    a = math.sqrt(e['A_contact'] / math.pi)
                    rmin = min(e['r1'], e['r2'])
                    ae = min(a, rmin)
                    psi = max(1 - ae / rmin, 0.0) ** PSI_EXP
                    want_c = (psi / (min(srel) * k * 2 * ae)) if psi > PSI_FLOOR else 0.0
                    n += 1
                    if rel(e['R_bulk'], want_b) > 1e-12 or (want_c and rel(e['R_constriction'], want_c) > 1e-12) or (not want_c and e['R_constriction']):
                        badf.append((mode, r1, r2, delta, e['R_bulk'], want_b, e['R_constriction'], want_c))
        chk(f'H2 ★ H12 식 (독립 oracle) — R_bulk = Σ h_i²/(σ_i·k·V_i) (구 조각) · R_c = ψ/(σ·k·2·a_eff) — 세 채널 × 반지름 순서 · 같은 반지름 × s 두 점 ({n})',
            n == 18 and not badf, repr(badf[:2]))
        same = []
        for mode, (t, tm) in CH.items():
            e0, _ = _edge(mode, 0.05, t=t, tm=tm)
            e1, _ = _edge(mode, 0.05, t=t, tm=tm, hertz_constriction='maxwell', bulk_model='cylinder_half_d')
            same.append({k: float(v).hex() if isinstance(v, float) else v for k, v in e0.items() if k != 'A_components'}
                        == {k: float(v).hex() if isinstance(v, float) else v for k, v in e1.items() if k != 'A_components'})
            lab1, lab2 = tm[t[0]], tm[t[1]]
            s1, s2 = [1.0 / (1.0 + (max(r, 0.1) / NCM_R0) ** NCM_BETA) if (mode == 'electronic' and lb == 'AM_P') else 1.0
                      for r, lb in ((e0['r1'], lab1), (e0['r2'], lab2))]
            kr = K_AM / K_SE
            k = (kr if (lab1 != 'SE' and lab2 != 'SE') else 1.0 if (lab1 == 'SE' and lab2 == 'SE') else 2 * kr / (1 + kr)) \
                if mode == 'thermal' else 1.0
            cyl = (e0['d_ij'] / 2) / (s1 * k * math.pi * e0['r1'] ** 2) + (e0['d_ij'] / 2) / (s2 * k * math.pi * e0['r2'] ** 2)
            same.append(e0['R_constriction'] == e0['R_Maxwell'] and rel(e0['R_bulk'], cyl) < 1e-12)
        chk('H3 Hertz 기본 = H0 (Maxwell + 원기둥 반 d) — 인자 없음 ↔ 명시 H0 간선 비트 동일 · R_c = R_Maxwell · R_bulk = 원기둥 (세 채널)',
            len(same) == 6 and all(same))
        A, Cc = chain()
        rr = {cm: json.loads(json.dumps(quiet(nc._run_all_networks, A, Cc, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None,
                                              contact_mode=cm))) for cm in ('hertzian', 'physics')}
        h12 = rr['hertzian'].get('hertz_h12')
        meta_ok = isinstance(h12, dict) and all(h12.get(k) == v for k, v in (
            ('hertz_constriction', 'mikic_psi_multiply'), ('bulk_model', 'sphere_segment'), ('electrode_model', 'dirichlet_exact'),
            ('resistance_model', 'mikic'), ('psi_placement', 'multiply'), ('sensitivity_mode', 'hertz_h12'),
            ('sigma_full_status', 'computed'), ('ionic_status', 'computed')))
        chk("H4 ★ _run_all_networks (hertzian) 결과 안 이온 민감도 레코드 hertz_h12 — 짝 메타 · 전극 · mikic + multiply · 상태 · σ₀ · 온도 = 주 결과 · "
            "physics 결과에는 없다 · H12 σ ≠ H0 σ",
            meta_ok and 'hertz_h12' not in rr['physics']
            and h12.get('sigma_grain_S_cm') == rr['hertzian'].get('sigma_grain_S_cm')
            and h12.get('temperature_provenance') == rr['hertzian'].get('temperature_provenance')
            and h12.get('boundary_rule') == rr['hertzian'].get('boundary_rule')
            and h12.get('percolating_fraction') == rr['hertzian'].get('percolating_fraction')
            and h12.get('sigma_full') != rr['hertzian'].get('sigma_full'),
            repr({k: (h12 or {}).get(k) for k in ('hertz_constriction', 'bulk_model', 'electrode_model', 'resistance_model', 'psi_placement',
                                                  'sigma_full', 'sigma_full_status')}))
        chk('H4b 주 Hertz 결과 (H0) 의 메타 — bulk cylinder_half_d · 협착 maxwell · 전극 dirichlet_exact · 면적 hertz_ccpl22',
            rr['hertzian'].get('bulk_model') == 'cylinder_half_d' and rr['hertzian'].get('hertz_constriction') == 'maxwell'
            and rr['hertzian'].get('electrode_model') == 'dirichlet_exact' and rr['hertzian'].get('area_rule') == 'hertz_ccpl22')
        v_se = 21 * 4.0 / 3.0 * math.pi
        eps_s = 1.0 - v_se / (10.0 * 10.0 * 20.0)
        led = {'thickness_um': 20.0, 'thickness_mass_conserving_um': 20.0 * (1 - eps_s) / (1 - 0.97), 'phi_se_mass_conserving': 0.03}
        o = tf.ion_columns(rr, led, 100.0)
        chk("H5 ★ τ 인계 열 — hertz_h12 모드 f · tau2 · tau · 상태 (OK 또는 MODEL_BELOW_CONTINUUM_BOUND) · 협착 mikic_psi_multiply · ψ multiply · "
            "bulk sphere_segment · 면적 hertz_ccpl22 · 전극 dirichlet_exact · 주 hertz 열은 H0 (maxwell_halfspace · cylinder_half_d)",
            o.get('ion_net_status_hertz_h12') in ('OK', 'MODEL_BELOW_CONTINUUM_BOUND') and isinstance(o.get('tau2_ion_hertz_h12'), float)
            and abs(o['tau_ion_hertz_h12'] - math.sqrt(o['tau2_ion_hertz_h12'])) < 1e-12
            and o.get('ion_net_constriction_hertz_h12') == 'mikic_psi_multiply' and o.get('ion_net_psi_hertz_h12') == 'multiply'
            and o.get('ion_net_bulk_hertz_h12') == 'sphere_segment' and o.get('ion_net_area_rule_hertz_h12') == 'hertz_ccpl22'
            and o.get('ion_net_electrode_hertz_h12') == 'dirichlet_exact'
            and o.get('ion_net_constriction_hertz') == 'maxwell_halfspace' and o.get('ion_net_bulk_hertz') == 'cylinder_half_d'
            and o.get('tau2_ion_hertz_h12') != o.get('tau2_ion_hertz'),
            repr({k: o.get(k) for k in o if k.endswith('_h12')}))
        rr2 = copy.deepcopy(rr)
        rr2['hertzian'].pop('hertz_h12')
        o2 = tf.ion_columns(rr2, led, 100.0)
        #  ★ 10-06 밤 (G2R-02) — 세대 2 표지가 있는 결과에서 H12 만 빠졌다 = 부분 결손 (생산자는 hertzian 실행에 늘 함께 낸다) → 세대 계약 위반 ·
        #    레코드 있는 주 두 모드도 NOT_COMPUTED (invalid_input) · H12 는 레코드 없음 (missing_input).  옛 판은 주 두 모드를 그대로 OK 로 실었다.
        chk('H5b ★ H12 레코드 없는 세대 2 결과 (부분 결손) → 세대 invalid · hertz_h12 NOT_COMPUTED (missing_input) · 주 두 모드 NOT_COMPUTED '
            '(invalid_input: 세대 계약) · 값 빈칸',
            o2.get('ion_net_status_hertz_h12') == 'NOT_COMPUTED' and o2.get('ion_net_status_reason_hertz_h12') == 'missing_input'
            and o2.get('ion_net_generation') == 'invalid'
            and all(o2.get(f'ion_net_status_{m}') == 'NOT_COMPUTED' and '세대 계약' in str(o2.get(f'ion_net_status_reason_{m}'))
                    and tf.reason_code(o2.get(f'ion_net_status_reason_{m}')) == 'invalid_input' for m in ('hertz', 'physics'))
            and o2.get('tau2_ion_physics') is None, repr({k: o2.get(k) for k in ('ion_net_generation', 'ion_net_status_reason_hertz')}))
    _guard('H', sH)

    # ══ E. 세대 표기 · 섞임 거부 ═════════════════════════════════════════════════════════════════════
    def sE():
        A, Cc = chain()
        rr = {cm: json.loads(json.dumps(quiet(nc._run_all_networks, A, Cc, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None,
                                              contact_mode=cm))) for cm in ('hertzian', 'physics')}
        led = {'thickness_um': 20.0, 'thickness_mass_conserving_um': 20.0, 'phi_se_mass_conserving': 21 * 4.0 / 3.0 * math.pi / 2000.0}
        o = tf.ion_columns(rr, led, 100.0)
        chk("E1 ★ 세대 2 표기 — ion_net_electrode_<m> = dirichlet_exact (세 모드) · ion_net_area_rule_physics = physics_g2 · "
            "ion_net_area_rule_hertz = hertz_ccpl22 · ion_net_bulk_hertz · _physics = cylinder_half_d",
            all(o.get(f'ion_net_electrode_{m}') == 'dirichlet_exact' for m in ('hertz', 'physics', 'hertz_h12'))
            and o.get('ion_net_area_rule_physics') == 'physics_g2' and o.get('ion_net_area_rule_hertz') == 'hertz_ccpl22'
            and o.get('ion_net_bulk_hertz') == o.get('ion_net_bulk_physics') == 'cylinder_half_d',
            repr({k: o.get(k) for k in o if 'electrode' in k or 'area_rule' in k or 'bulk' in k}))
        old = copy.deepcopy(rr)
        #  ★ 10-06 밤 (G2R-02) — 옛 산출물 모양 = 세대 2 표지가 **하나도** 없다 (194 v1.2 배치 원천 실측: resistance_model · contact_mode · ψ legacy_divide 만).
        #    옛 픽스처는 모델 표기 다섯만 빼고 진단 키 (h_film_nm · n_clamp_zero …) · 채널 표기 (thermal_electrode_model …) 를 남겼다 — 새 계약은 그 혼종을
        #    세대 2 부분 결손으로 거부한다 (test_gen2_role_contract R7).  표지 목록 = 실 생산자 ↔ 역사 레코드 키 차 (test_gen2_role_contract K1 오라클과 같다).
        gone = ('electrode_model', 'area_rule', 'area_rule_physics', 'bulk_model', 'hertz_constriction', 'sensitivity_mode', 'hertz_h12',
                'area_binding_counts_physics', 'n_area_physics_unavailable', 'n_clamp_zero', 'n_floor_only', 'h_film_nm', 'h_film_status',
                'solve_method_full')
        gone_ch = ('electrode_model', 'bulk_model', 'area_rule', 'area_rule_physics', 'area_binding_counts_physics', 'n_clamp_zero', 'n_floor_only',
                   'psi_placement')
        for m in ('hertzian', 'physics'):
            for k in list(old[m]):
                if k in gone or any(k == f'{ch}_{g}' for ch in ('electronic', 'thermal') for g in gone_ch):
                    old[m].pop(k, None)
            old[m]['psi_placement'] = 'legacy_divide'
        og = tf.ion_columns(old, led, 100.0)
        chk('E2 표기 없는 옛 산출물 = 이력 사실 — 전극 virtual_source_legacy · physics 면적 physics_g1 · bulk cylinder_half_d (짐작이 아니라 10-06 전 코드가 그것뿐) · '
            '세대 칸 inferred_legacy (추론임을 말한다)',
            og.get('ion_net_electrode_hertz') == og.get('ion_net_electrode_physics') == 'virtual_source_legacy'
            and og.get('ion_net_area_rule_physics') == 'physics_g1' and og.get('ion_net_bulk_hertz') == 'cylinder_half_d'
            and og.get('ion_net_electrode_hertz_h12') == '' and og.get('ion_net_generation') == 'inferred_legacy',
            repr({k: og.get(k) for k in og if 'electrode' in k or 'area_rule' in k or k == 'ion_net_generation'}))
        mix = copy.deepcopy(rr)
        mix['physics'].pop('electrode_model')
        om = tf.ion_columns(mix, led, 100.0)
        chk('E3 ★ 한 행 안 전극 세대 섞임 (hertz = dirichlet_exact · physics = 표기 없음) → 레코드 있는 모드 전부 NOT_COMPUTED (invalid_input: 세대 섞임)',
            all(om.get(f'ion_net_status_{m}') == 'NOT_COMPUTED' and tf.reason_code(om.get(f'ion_net_status_reason_{m}')) == 'invalid_input'
                for m in ('hertz', 'physics', 'hertz_h12')), repr({m: om.get(f'ion_net_status_reason_{m}', '')[:60] for m in ('hertz', 'physics')}))
        g2, g1 = tf.generation_axes(o), tf.generation_axes(og)
        #  ★ 10-06 밤 (G2R-01) — 세대 축에 세대 칸 · 모드별 협착 · bulk 가 더해졌다 (옛 축에는 주 Hertz 의 bulk · 협착이 없어 H12 를 주 자리에 둔 행이 같았다)
        chk("E4 세대 축 — 세대 2 (g2 · psi multiply · physics_g2 · dirichlet_exact · H0 maxwell + 원기둥 · physics ψ 곱 + 원기둥 · H12 ψ 곱 + 구 조각) ↔ "
            "옛 (inferred_legacy · legacy_divide · physics_g1 · virtual_source_legacy · H0 · physics ψ 분모 · H12 없음)",
            g2 == {'generation': 'g2', 'psi': 'multiply', 'area_rule_physics': 'physics_g2', 'electrode': 'dirichlet_exact',
                   'constriction_hertz': 'maxwell_halfspace', 'bulk_hertz': 'cylinder_half_d', 'constriction_physics': 'mikic_psi_multiply',
                   'bulk_physics': 'cylinder_half_d', 'constriction_hertz_h12': 'mikic_psi_multiply', 'bulk_hertz_h12': 'sphere_segment'}
            and g1 == {'generation': 'inferred_legacy', 'psi': 'legacy_divide', 'area_rule_physics': 'physics_g1', 'electrode': 'virtual_source_legacy',
                       'constriction_hertz': 'maxwell_halfspace', 'bulk_hertz': 'cylinder_half_d', 'constriction_physics': 'mikic_psi_divide',
                       'bulk_physics': 'cylinder_half_d', 'constriction_hertz_h12': '', 'bulk_hertz_h12': ''}, repr((g2, g1)))
        chk('E5 ★ 여러 행 섞임 판정 — 같은 세대 행끼리 = 문제 없음 · 세대 2 + 옛 행 = 거부 사유 (축 · 값) · 레코드 없는 행 (모든 축 빈칸) 은 판정 밖',
            tf.generation_mixing_problem([dict(o, case='a'), dict(o, case='b')]) == ''
            and 'electrode' in tf.generation_mixing_problem([dict(o, case='a'), dict(og, case='b')])
            and tf.generation_mixing_problem([dict(o, case='a'), {'case': 'c'}]) == '')
        tmp = tempfile.mkdtemp(prefix='gen2_')
        for name, d in (('a_g2', rr), ('b_g1', old)):
            c = os.path.join(tmp, name)
            os.makedirs(c)
            json.dump(d, open(os.path.join(c, 'network_conductivity_dual.json'), 'w'))
            json.dump(dict(led, percolation_pct=100.0), open(os.path.join(c, 'full_metrics.json'), 'w'))
        out_tsv = os.path.join(tmp, 'out.tsv')
        r = subprocess.run([sys.executable, os.path.join(HERE, 'tau_flux.py'), os.path.join(tmp, 'a_g2'), os.path.join(tmp, 'b_g1'),
                            '--tsv', out_tsv], capture_output=True, text=True, timeout=120)
        r1 = subprocess.run([sys.executable, os.path.join(HERE, 'tau_flux.py'), os.path.join(tmp, 'a_g2'), '--tsv', out_tsv + '1'],
                            capture_output=True, text=True, timeout=120)
        chk('E6 ★ tau_flux CLI — 세대가 다른 케이스 폴더를 한 표로 묶으면 거부 (rc 2 · TSV 를 쓰지 않는다 · 사유에 세대) · 한 세대만이면 rc 0',
            r.returncode == 2 and not os.path.exists(out_tsv) and '세대' in r.stderr and r1.returncode == 0 and os.path.exists(out_tsv + '1'),
            f'rc {r.returncode} · {r.stderr[-200:]!r} · 한 세대 rc {r1.returncode}')
        cols = tf.column_names()
        #  ★ 10-06 밤 (G2R-02) — 공통 세대 칸 ion_net_generation 이 더해졌다 (g2 · inferred_legacy · invalid — 옛 세대 추론이 행에서 보인다) → 공통 5
        chk('E7 열 — 모드 셋 (hertz · physics · hertz_h12) × (12 + 전극 · bulk · 면적 규칙 3) + 공통 5 (σ₀ · T · φ · L 기준 · 세대 칸) = 50 · 모드 꼬리 · '
            '꼬리 없는 상태 키 없음',
            tuple(tf.MODES) == ('hertz', 'physics', 'hertz_h12') and len(cols) == 3 * 15 + 5 and len(set(cols)) == len(cols)
            and cols[-1] == 'ion_net_generation'
            and all(f'ion_net_{b}_{m}' in cols for b in ('electrode', 'bulk', 'area_rule') for m in tf.MODES) and 'ion_net_status' not in cols)
    _guard('E', sE)

    print(f'\ntest_network_generation2: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

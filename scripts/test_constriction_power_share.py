#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""④a 협착 저항의 전력 (I²R) 몫 — 새 열 (J20-s · 1저자 비준 10-04 *"권고대로"* · 원장 LHS-30 · L2-08).

옛 `bulk_resistance_fraction` = 간선마다 R_bulk/(R_bulk+R_c) 를 내고 **비가중 평균** (전류 없는 간선 · 비관통 덩어리 포함) — 이름표만
고쳤다 (L2-08).  새 열 = **같은 FULL 해**의 Σ I²R_c / Σ I²R_total (관통 간선 · 가상 전극 연결 제외) — 키는 채널 · 모드 꼬리를 명시
(τ 명명 규약): `constriction_power_share_{ion,el,th}_{hertz,physics}` + `_status`.  σ 값은 비트 동일 (해에 출력만 더한다 —
`test_network_boundary_rule.py` 의 GOLD 가 같이 지킨다).  network_conductivity.py = S3 수치 모듈 → S3 전 재봉인 (결정 16).

  python3 scripts/test_constriction_power_share.py
"""
import contextlib
import io
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))


def edge(i, j, rb, rc):
    return {'id1': i, 'id2': j, 'R_bulk': rb, 'R_constriction': rc, 'R_total': rb + rc, 'type1': 'SE', 'type2': 'SE',
            'delta': 0.0, 'delta_over_R': 0.0, 'regime': 'toy', 'r1': 1.0, 'r2': 1.0, 'd_ij': 2.0,
            'A_hertzian': 0.1, 'A_physics': 0.1, 'A_contact': 0.1}


def toy_l208():
    """L2-08 반례 — 바닥 b → 위 t 두 병렬 경로 × 직렬 간선 둘 · R_bulk 1 · 경로 A R_c 9 · 경로 B R_c 0."""
    edges = [edge('b', 'a', 1.0, 9.0), edge('a', 't', 1.0, 9.0), edge('b', 'c', 1.0, 0.0), edge('c', 't', 1.0, 0.0)]
    return {'nodes': {'b': {}, 'a': {}, 'c': {}, 't': {}}, 'edges': edges, 'bottom': {'b'}, 'top': {'t'},
            'scale': 1.0, 'plate_z': 1.0, 'box_x': 10.0, 'box_y': 10.0}


def chain(zs, r, t=1):
    A = {i: {'type': t, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': float(r)} for i, z in enumerate(zs, 1)}
    C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1 * r * r, 'delta': 0.05 * r} for i in range(1, len(zs))]
    return A, C


def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)


def main():
    import network_conductivity as nc
    have = hasattr(nc, 'constriction_power_share')
    chk('C0 network_conductivity.constriction_power_share 가 있다 (④a)', have)
    if not have:
        print(f'\n{_ok}/{_ok + len(_fail)} PASS')
        return 1

    # ── C1 L2-08 반례 — 손풀이: I_A = 1/11 · I_B = 10/11 → Σ I²R_c / Σ I²R_total = 18/220 = 8.1818 % ──────────────
    net = toy_l208()
    G, sr, field = quiet(nc.solve_network, net, mode='full', return_field=True)
    share, st = nc.constriction_power_share(field)
    chk('C1 반례 전력 몫 = 18/220 = 0.0818182 (손풀이) · 상태 computed',
        st == 'computed' and share is not None and abs(share - 18.0 / 220.0) < 1e-9, f'{share} · {st}')
    uw = 1.0 - sum(e['R_bulk'] / e['R_total'] for e in net['edges']) / len(net['edges'])
    chk('C1b 같은 망의 옛 통계 (1 − 비가중 평균 bulk 비) = 0.45 → 5.5 배 차 (L2-08 그대로)', abs(uw - 0.45) < 1e-12 and abs(uw / share - 5.5) < 1e-6)
    chk('C1c 가상 전극 연결은 세지 않는다 — 몫은 경계 전도도 크기와 무관 (경로 비만)',
        len(field['edge_records']) == 4)

    # ── C2 · C3 run_decomposition 결과 키 (채널 · 모드 꼬리) ─────────────────────────────────────────────
    A, C = chain(range(21), 1.0)
    for cm, tail in (('hertzian', 'hertz'), ('physics', 'physics')):
        res = quiet(nc.run_decomposition, A, C, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode=cm, mode='ionic')
        key = f'constriction_power_share_ion_{tail}'
        _G, _sr, fld = quiet(nc.solve_network, quiet(nc.build_network, A, C, [1], 1.0, 20.0, 10.0, 10.0, 2.0, mode='ionic',
                                                     type_map={1: 'SE'}, contact_mode=cm), mode='full', return_field=True)
        want, _ = nc.constriction_power_share(fld)
        chk(f'C2 [{cm}] run_decomposition 결과에 {key} (같은 FULL 해의 값) · _status computed · 0 < 몫 < 1',
            res is not None and res.get(f'{key}_status') == 'computed' and isinstance(res.get(key), float)
            and abs(res[key] - round(want, 6)) < 1e-12 and 0 < res[key] < 1,   # 저장 = 6 자리 반올림
            f'{res and {k: v for k, v in res.items() if "power" in k}}')
        chk(f'C2b [{cm}] 옛 bulk_resistance_fraction 키 · 값 그대로 있다 (이름표만 정정)', res is not None and 'bulk_resistance_fraction' in res)
        other = [k for k in (res or {}) if k.startswith('constriction_power_share') and k not in (key, f'{key}_status')]
        chk(f'C2c [{cm}] 꼬리 없는 이름 · 다른 채널 이름을 쓰지 않는다 (한 양 = 한 이름)', not other, repr(other))
    resE = quiet(nc.run_decomposition, A, C, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'AM'}, contact_mode='hertzian', mode='electronic')
    resT = quiet(nc.run_decomposition, A, C, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='hertzian', mode='thermal',
                 is_thermal=True)
    chk('C3 전자 · 열 채널 꼬리 — _el_hertz · _th_hertz', isinstance((resE or {}).get('constriction_power_share_el_hertz'), float)
        and isinstance((resT or {}).get('constriction_power_share_th_hertz'), float),
        repr([(resE or {}).get('constriction_power_share_el_hertz'), (resT or {}).get('constriction_power_share_th_hertz')]))

    # ── C4 관통 없음 → 값 None · 상태 not_computed (0 으로 안 채움) ──────────────────────────────────────
    A2, C2 = chain(range(21), 1.0)
    C2 = [c for c in C2 if c['id1'] != 10]                 # 가운데 끊김
    res = quiet(nc.run_decomposition, A2, C2, [1], 1.0, 20.0, 10.0, 10.0, type_map={1: 'SE'}, contact_mode='hertzian', mode='ionic')
    chk('C4 관통 없음 → constriction_power_share_ion_hertz None · 상태 not_computed',
        res is not None and res.get('constriction_power_share_ion_hertz') is None
        and str(res.get('constriction_power_share_ion_hertz_status', '')).startswith('not_computed'),
        repr(res and {k: v for k, v in res.items() if 'power' in k}))
    s0, st0 = nc.constriction_power_share(None)
    chk('C4b 해 없음 (None) → (None, not_computed …)', s0 is None and st0.startswith('not_computed'))

    # ── C5 _run_all_networks — 이온 중심 결과에 전자 · 열 키가 실린다 (network_conductivity.json 에 셋 다) ──────────────
    A3 = {}
    for i, z in enumerate(range(21), 1):
        A3[i] = {'type': 1, 'x': 2.0, 'y': 2.0, 'z': float(z), 'radius': 1.0}
        A3[100 + i] = {'type': 2, 'x': 6.0, 'y': 6.0, 'z': float(z), 'radius': 1.0}
    C3 = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
    C3 += [{'id1': 100 + i, 'id2': 101 + i, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
    tmp = tempfile.mkdtemp(prefix='cps_')
    res = quiet(nc._run_all_networks, A3, C3, [1], [2], {1: 'SE', 2: 'AM'}, 1.0, 20.0, 10.0, 10.0, tmp, contact_mode='hertzian')
    keys = ('constriction_power_share_ion_hertz', 'constriction_power_share_el_hertz', 'constriction_power_share_th_hertz')
    chk('C5 _run_all_networks (hertzian) — ion · el · th 세 키 + 상태', res is not None and all(isinstance(res.get(k), float) for k in keys)
        and all(res.get(k + '_status') == 'computed' for k in keys), repr(res and {k: res.get(k) for k in keys}))

    # ── C6 웹앱 머지 목록 — hertz 세 키는 network_conductivity.json → full_metrics · physics 꼬리 키는 dual 에서 그대로 ──
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'webapp'))
    import pipeline_service as ps
    chk('C6 pipeline_service.NET_MERGE_KEYS 에 hertz 세 키 + 상태', all(k in ps.NET_MERGE_KEYS and k + '_status' in ps.NET_MERGE_KEYS for k in keys))
    pk = tuple(k.replace('_hertz', '_physics') for k in keys)
    chk('C6b physics 꼬리 키는 이름 그대로 복사 (옛 _physics 덧붙이기 미러가 아니다 — 두 번 붙지 않게)',
        all(k in getattr(ps, 'NET_PHYSICS_TAILED_KEYS', ()) for k in pk) and not any(k in ps.NET_PHYSICS_MIRROR_KEYS for k in keys + pk))

    print(f'\n{_ok}/{_ok + len(_fail)} PASS' + ('' if not _fail else '  — FAIL: ' + ' · '.join(_fail)))
    return 1 if _fail else 0


if __name__ == '__main__':
    sys.exit(main())

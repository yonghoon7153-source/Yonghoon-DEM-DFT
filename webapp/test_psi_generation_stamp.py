#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ψ 세대 표기 — 웹앱 망 산출물이 세대를 싣는가 (`L2-01` 세대 2 · 1저자 개정 2026-10-06 · 계약 개정 노트).

  python3 webapp/test_psi_generation_stamp.py

★ 시험 먼저 — 옛 코드 (기본 = legacy_divide · 표기 없음) 에서 ①b · ①d · ①e · ② · ③ · ④ 가 빨갛다.
  ① 실 생산자 (network_conductivity CLI 그대로 · test_pipeline_provenance._CLIRunner) → `app._network_and_stage_e(stop_before_stage_e=True)`:
     done (망 정지 계약 ⑥b — 새 표기 키도 이번 세대의 투영과 같다) · full_metrics `psi_placement_physics` = multiply = 생산자 기본 =
     dual physics 기록 · `physics_resistance_model` = mikic (옛 도장 그대로) · 활성 도장 (network_provenance.json) 도 같은 표기 ·
     도장의 값은 **솔버 출력**에서 읽는다 (세대 1 dual 을 둔 폴더에 도장을 찍으면 legacy_divide)
  ② 표기는 망 소유 키 — `NET_MERGE_KEYS` 에 있고 (세대마다 걷어내고 다시 채운다 · RC5-03) · physics 미러 (`NET_PHYSICS_MIRROR_KEYS`) 로 채운다
  ③ 세대 1 산출물 (dual physics psi_placement = legacy_divide) 을 다시 투영하면 legacy_divide · 기록 없는 옛 산출물 (09-15 깃발 전) 이면
     표기 키가 없다 (지금 full_metrics 의 multiply 가 옛 세대 밑에 남지 않는다)
  ④ τ 인계 메타 (`tau_flux.case_row` — 같은 폴더) — 협착 mikic_psi_multiply · ψ multiply · 상태 OK
  ⑤ ★ 10-06 저녁 세대 2 (1저자 비준 C1 · C2) — 전극 · bulk · physics 면적 규칙 표기 (full_metrics · 활성 도장) · H12 민감도 레코드
     (Hertz 레코드 안 · 모든 사본 · τ 상태 OK) · 망 정지 계약 ⑨ 가 H12 없음 · H12 σ ×4 · H12 짝 메타 어긋남 · 모드끼리 전극 섞임을 거부
     (복사본 폴더 · 다른 것은 그대로 — 거부 사유가 ⑨ 하나뿐) · 옛 세대 (표기 없는 legacy) 투영엔 새 표기 키가 없다
⚠ 범위 — 합성 21 구 사슬 침대의 표기 · 소유 시험이다 (값 · 물리 정확도 아님).
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
for _p in (HERE, SCRIPTS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pipeline_service as ps            # noqa: E402
import test_pipeline_provenance as TP    # noqa: E402  (침대 · 실 CLI 대역 — 같은 도구를 쓴다)

PASS = FAIL = 0
STAMP = 'psi_placement_physics'


def chk(label, ok, detail=''):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f'  PASS {label}')
    else:
        FAIL += 1
        print(f'  FAIL {label}' + (f' — {detail}' if detail else ''))


def _load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def _dump(p, obj):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f)


_NET_FILES = (('network_conductivity_dual.json', None), ('network_conductivity.json', 'hertzian'),
              ('network_conductivity_hertzian.json', 'hertzian'), ('network_conductivity_physics.json', 'physics'))


def _variant(src, dst, fn):
    """복사본 폴더 — 망 JSON 넷 (dual · legacy · 모드 파일 둘) 모두에 같은 변이 fn({'hertzian': …, 'physics': …}) (사본끼리 일관)."""
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)
    for n, key in _NET_FILES:
        p = os.path.join(dst, n)
        if not os.path.exists(p):
            continue
        obj = _load(p)
        fn(obj if key is None else {key: obj})
        _dump(p, obj)
    return dst


def main():
    import app
    import network_conductivity as nc
    import tau_flux as tf

    d = tempfile.mkdtemp(prefix='psi_gen_')
    d2 = tempfile.mkdtemp(prefix='psi_gen_g1_')
    try:
        a, c = TP._write_bed(d, 'through')
        _dump(os.path.join(d, 'full_metrics.json'), TP._bed_ledger('through'))
        stages, rid = app._network_and_stage_e(d, SCRIPTS, a, c, '1:SE', 1, [], runner=TP._CLIRunner(), stop_before_stage_e=True)
        st, failed = ps.summarize(stages)
        fm = _load(os.path.join(d, 'full_metrics.json'))
        dual = _load(os.path.join(d, 'network_conductivity_dual.json'))
        prov = ps.read_network_provenance(d)

        print('① 실 생산자 → 망 정지 계약 → 게시')
        chk(f'①a done — 망 정지 계약 통과 (⑥b 망 소유 키 = 이번 세대 투영 · 새 표기 키 포함) ({st})', st == 'done',
            str([s.get('step') for s in failed]))
        chk(f"①b ★ full_metrics {STAMP} = multiply = 생산자 기본 = dual physics 기록 ({fm.get(STAMP)!r})",
            fm.get(STAMP) == 'multiply' == nc.PSI_PLACEMENT_DEFAULT == dual['physics'].get('psi_placement'),
            repr((fm.get(STAMP), nc.PSI_PLACEMENT_DEFAULT, dual['physics'].get('psi_placement'))))
        chk(f"①c physics_resistance_model = mikic (옛 도장 그대로 · 세대 표기는 그 옆 키) ({fm.get('physics_resistance_model')!r})",
            fm.get('physics_resistance_model') == 'mikic')
        chk(f"①d ★ 활성 도장 (network_provenance.json) {STAMP} = multiply · run id = 이번 실행 ({prov.get(STAMP)!r})",
            prov.get(STAMP) == 'multiply' and prov.get('network_run_id') == rid and prov.get('solver_status') == 'success',
            repr({k: prov.get(k) for k in (STAMP, 'network_run_id', 'solver_status')}))
        #  도장의 값 = 솔버 출력 (dual) — 모듈 기본값을 베끼지 않는다: 세대 1 dual 을 둔 폴더에 도장을 찍으면 legacy_divide
        g1 = json.loads(json.dumps(dual))
        g1['physics']['psi_placement'] = nc.PSI_DIVIDE
        _dump(os.path.join(d2, 'network_conductivity_dual.json'), g1)
        p2 = ps.stamp_network_provenance(d2, 'RUN-G1', {}, 'success', argv={'contact_mode': 'both'})
        shutil.rmtree(d2, ignore_errors=True)
        os.makedirs(d2)
        p3 = ps.stamp_network_provenance(d2, 'RUN-NODUAL', {}, 'success')
        chk(f"①e 도장은 솔버 출력에서 읽는다 — 세대 1 dual → legacy_divide · dual 없음 → None ({p2.get(STAMP)!r} · {p3.get(STAMP)!r})",
            p2.get(STAMP) == 'legacy_divide' and STAMP in p3 and p3.get(STAMP) is None, repr((p2.get(STAMP), p3.get(STAMP, '키 없음'))))

        print('② 망 소유 키')
        chk(f'② {STAMP} ∈ NET_MERGE_KEYS (세대마다 걷어내고 다시 채운다) · 원천 = physics 미러 psi_placement',
            STAMP in ps.NET_MERGE_KEYS and 'psi_placement' in ps.NET_PHYSICS_MIRROR_KEYS
            and STAMP not in getattr(ps, 'NET_PHYSICS_TAILED_KEYS', ()))

        print('④ τ 인계 메타 (같은 폴더)')
        row = tf.case_row(d)
        chk(f"④ case_row — 협착 {row.get('ion_net_constriction_physics')!r} · ψ {row.get('ion_net_psi_physics')!r} · 상태 "
            f"{row.get('ion_net_status_physics')!r} (세대 2 = mikic_psi_multiply · multiply · OK)",
            row.get('ion_net_constriction_physics') == 'mikic_psi_multiply' and row.get('ion_net_psi_physics') == 'multiply'
            and row.get('ion_net_status_physics') == 'OK' and row.get('ion_net_constriction_hertz') == 'maxwell_halfspace')

        print('③ 옛 세대 산출물을 다시 투영 (메모리 · 쓰지 않는다)')
        dp = os.path.join(d, 'network_conductivity_dual.json')
        _dump(dp, g1)
        pj1 = app._network_projection(d, rid)
        old = json.loads(json.dumps(dual))
        old['physics'].pop('psi_placement', None)
        _dump(dp, old)
        pj2 = app._network_projection(d, rid)
        f1, f2 = (pj1.get('fm') or {}), (pj2.get('fm') or {})
        chk(f"③a 세대 1 dual (legacy_divide) → 투영 {STAMP} = legacy_divide ({f1.get(STAMP)!r})",
            not pj1.get('error') and f1.get(STAMP) == 'legacy_divide', pj1.get('error') or '')
        chk(f"③b ψ 기록 없는 옛 dual (09-15 전) → 투영에 {STAMP} 키 없음 (지금 full_metrics 의 multiply 가 남지 않는다 · "
            f"디스크 full_metrics = {fm.get(STAMP)!r})",
            not pj2.get('error') and STAMP not in f2 and fm.get(STAMP) == 'multiply', repr(f2.get(STAMP, '키 없음')))

        print('⑤ ★ 세대 2 표기 · H12 민감도 레코드 (10-06 저녁)')
        _dump(dp, dual)                                           # ③ 이 덮은 dual 을 이번 세대로 되돌린다 (디스크 = 게시 세대)
        G2 = {'electrode_model': 'dirichlet_exact', 'bulk_model': 'cylinder_half_d', 'area_rule_physics': 'physics_g2'}
        chk(f"⑤a full_metrics 표기 = dual Hertz 기록 (전극 · bulk · physics 면적 규칙) · 망 소유 키 ({ {k: fm.get(k) for k in G2} })",
            all(fm.get(k) == v == dual['hertzian'].get(k) for k, v in G2.items()) and all(k in ps.NET_MERGE_KEYS for k in G2)
            and dual['physics'].get('area_rule') == 'physics_g2' and dual['physics'].get('electrode_model') == 'dirichlet_exact',
            repr({k: (fm.get(k), dual['hertzian'].get(k)) for k in G2}))
        chk(f"⑤b 활성 도장 — electrode_model · area_rule_physics · hertz_h12 ({ {k: prov.get(k) for k in ('electrode_model', 'area_rule_physics', 'hertz_h12')} })",
            prov.get('electrode_model') == 'dirichlet_exact' and prov.get('area_rule_physics') == 'physics_g2' and prov.get('hertz_h12') is True)
        r12 = ps.network_h12_record(dual)
        leg = _load(os.path.join(d, 'network_conductivity.json'))
        hz = _load(os.path.join(d, 'network_conductivity_hertzian.json'))
        row5 = tf.case_row(d)
        chk(f"⑤c H12 레코드 = Hertz 레코드 안 (dual · legacy · hertzian 모드 파일 같은 사본) · 짝 메타 · τ 상태 "
            f"{row5.get('ion_net_status_hertz_h12')!r} · σ ≠ H0",
            isinstance(r12, dict) and leg.get('hertz_h12') == hz.get('hertz_h12') == r12
            and all(r12.get(k) == v for k, v in ps.NETWORK_H12_META)
            and row5.get('ion_net_status_hertz_h12') == 'OK' and row5.get('ion_net_bulk_hertz_h12') == 'sphere_segment'
            and r12.get('sigma_full_mScm') != dual['hertzian'].get('sigma_full_mScm'),
            repr({k: r12.get(k) for k, _ in ps.NETWORK_H12_META}) if isinstance(r12, dict) else 'H12 없음')
        d5 = tempfile.mkdtemp(prefix='psi_gen_v_')
        try:
            ok0, why0 = ps.network_stop_verdict(_variant(d, os.path.join(d5, 'same'), lambda dd: None), rid)
            chk(f'⑤d 양성 대조 — 바꾸지 않은 복사본은 망 정지 계약 통과 ({why0[:80]})', ok0, why0)

            def _drop(dd):
                if isinstance(dd.get('hertzian'), dict):
                    dd['hertzian'].pop('hertz_h12', None)

            def _x4(dd):
                if isinstance(dd.get('hertzian'), dict) and isinstance(dd['hertzian'].get('hertz_h12'), dict):
                    dd['hertzian']['hertz_h12']['sigma_full_mScm'] *= 4.0

            def _bulk(dd):
                if isinstance(dd.get('hertzian'), dict) and isinstance(dd['hertzian'].get('hertz_h12'), dict):
                    dd['hertzian']['hertz_h12']['bulk_model'] = 'cylinder_half_d'

            def _mix(dd):
                if isinstance(dd.get('physics'), dict):
                    dd['physics']['electrode_model'] = 'virtual_source_legacy'
            #  (라벨 · 변이 · 꼭 있어야 할 사유 · 허용 사유 머리) — 전극 섞임은 τ 소비자 (⑦ — 한 행 안 전극 세대 섞임 = NOT_COMPUTED) 도 함께 거부한다
            for lab, fn, tag, allow in (('⑤e H12 없음 (세대 2 Hertz 레코드)', _drop, '⑨ H12', ('⑨',)),
                                        ('⑤f H12 σ_full_mScm ×4 (σ_ratio 그대로 — 두 표현 항등식 깨짐)', _x4, '⑨ H12: 기술적 입력 무효', ('⑨',)),
                                        ('⑤g H12 bulk = 원기둥 (짝 메타 어긋남 — ψ 단독 H1 은 기각)', _bulk, '⑨ H12: 짝 메타', ('⑨',)),
                                        ('⑤h 모드끼리 전극 섞임 (physics = virtual_source_legacy)', _mix, '⑨ 세대 섞임', ('⑨', '⑦ τ 인계'))):
                okv, whyv = ps.network_stop_verdict(_variant(d, os.path.join(d5, lab[:2]), fn), rid)
                bad_other = [w for w in str(whyv).split('; ') if not w.startswith(allow)]
                chk(f'{lab} → 망 정지 계약 거부 · 사유 = {"/".join(allow)} 뿐 ({str(whyv)[:90]})', (not okv) and tag in str(whyv) and not bad_other,
                    str(whyv)[:300])
        finally:
            shutil.rmtree(d5, ignore_errors=True)
        #  옛 세대 (표기 없는 legacy) 를 다시 투영하면 새 표기 키가 없다 — 지금 full_metrics 의 dirichlet_exact 가 옛 세대 밑에 남지 않는다 (RC5-03)
        lp = os.path.join(d, 'network_conductivity.json')
        old_leg = json.loads(json.dumps(leg))
        for k in ('electrode_model', 'bulk_model', 'area_rule_physics', 'area_rule', 'hertz_h12'):
            old_leg.pop(k, None)
        _dump(lp, old_leg)
        pj3 = app._network_projection(d, rid)
        f3 = pj3.get('fm') or {}
        chk(f"⑤i 표기 없는 옛 legacy → 투영에 electrode_model · bulk_model · area_rule_physics 키 없음 ({ {k: f3.get(k, '키 없음') for k in G2} })",
            not pj3.get('error') and not any(k in f3 for k in G2) and fm.get('electrode_model') == 'dirichlet_exact', pj3.get('error') or '')
        _dump(lp, leg)
    finally:
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(d2, ignore_errors=True)

    print(f'\ntest_psi_generation_stamp: {PASS}/{PASS + FAIL} PASS')
    return 0 if FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

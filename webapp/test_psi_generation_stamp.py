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
    finally:
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(d2, ignore_errors=True)

    print(f'\ntest_psi_generation_stamp: {PASS}/{PASS + FAIL} PASS')
    return 0 if FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

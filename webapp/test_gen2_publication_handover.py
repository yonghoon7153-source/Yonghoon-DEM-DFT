#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""망 세대 계약 — 게시 전 거부 · 인계 거부 (Codex 세대 2 적대 리뷰 G2R-01 · G2R-02 · 1저자 비준 10-06 밤).

  python3 webapp/test_gen2_publication_handover.py

Codex `probes/publication.py` · `probes/handover.py` 를 **실 생산자 사슬**로 상주시킨다 (우리 트리 재현: 다섯 다 done · 일곱 다 인계 통과 —
`docs/reviews/codex_gen2_network_review_evidence_20261006/_reproduction_ours_7a5976602/`):
  ① 게시 — `network_conductivity.py` CLI 그대로 (test_pipeline_provenance._CLIRunner) 가 쓴 네 망 JSON 을 Codex `change` 로 바꾼 후보
     (h12_as_primary · bad_psi · bad_electrode · partial_missing_g2 · 표지를 전부 뺀 옛 모양) → `app._network_and_stage_e`:
     정지 경로 (stop_after=network) · 일반 경로 (Stage E 앞) 둘 다 failed · 활성 세대 없음 · 망 JSON 안 남음 · 최근 시도 candidate_rejected.
     baseline (실 생산자 그대로) = done (양성).  옛 코드: 다섯 다 done (h12_as_primary 주 σ +28.2 %).
  ② 인계 — 같은 변이를 **디스크에 강제로 남긴** 폴더 (게시된 baseline 폴더 복사 → 네 망 JSON 변이 → 웹앱 투영 (`app._network_projection`) 으로
     full_metrics → 도장 다시 찍기 = 옛 게시가 남겼을 모양) 를 배치 기록과 함께 `lhs_design_dataset.load_tau_results` 로:
     단독 넷 · [baseline, h12_as_primary] · [baseline, bad_psi] · [bad_psi, bad_psi] (같은 결함 코호트) 전부 거부 (τ P4 세대 계약) ·
     같은 절차로 만든 변이 없는 폴더 = 통과 (강제 절차가 P0–P3 를 깨지 않는다는 대조).  옛 코드: 일곱 다 통과.
  ③ 옛 세대 추론 자격 — 표지를 전부 뺀 레코드 + 세대 2 를 말하는 도장 (게시 뒤 표기만 지운 폴더) = 거부 · 같은 레코드 + 확인된 역사 도장 스키마
     (세대 키 없는 8 키 = 194 v1.2 모양) = inferred_legacy 로 통과 (H12 = missing_input) · 거울: 세대 2 표기 레코드 + 세대 키 없는 옛 도장 (역사 폴더에
     표기만 덧붙인 모양) = 거부.  ★ 10-06 밤 G2RR-01 — 도장 값 대조 (unknown · null · legacy · 부분 결손 · 역사 스키마 밖) 반례는 test_gen2_stamp_record.
  ④ 표 만들 때 — 원천이 다른 길로 들어와 두 행이 **같은 결함** (주 Hertz 칸 = H12 표기) 이면 `build_handover` 거부 (행마다 먼저 · 옛: 동질이라 통과).
  ⑤ ★ G2RR-02 (Codex 세대 2 재검증 §3 · §7-2 · probes/acceptance.py · 10-06 밤) — 증서 ↔ 가지 · 역할 · 발행값 결합: 실 생산자 CLI 의 네 망 JSON 에
     CF → FULL · H12 → H0 · 기하 인자 ×2 · 위장 CF (가지 · 기하를 맞춘 것) · 숫자만 · CF 보존 실패 · CF · 협착-only 증서 삭제 · 결합 키 없음 → 정지 경로 ·
     일반 경로 failed (⑨ · 공용 기록 검사) · 강제 폴더 → τ 소비자 NOT_COMPUTED · 인계 τ P4 거부.  양성 = 진짜 비관통 · GEN2-01 협착-only 미계산 (done ·
     τ 상태 그대로 · 인계 통과).  옛 코드: CF → FULL · H12 → H0 · 기하 · 숫자만 · CF 진단 넷이 done · τ OK.
⚠ 범위 — 표기 계약 + 증서 결합 (⑤).  모든 사본 · 도장 · 증서 · 기하를 함께 일관되게 바꾼 전면 위조는 못 잡는다 (TAU_SAME_GEN_BASIS 한계).
"""
import copy
import csv
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCRIPTS = ROOT / 'scripts'
for _p in (str(HERE), str(SCRIPTS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pipeline_service as ps            # noqa: E402
import test_pipeline_provenance as TP    # noqa: E402  (침대 · 실 CLI 대역 — 같은 도구)

PASS = FAIL = 0
LABELS = ('h12_as_primary', 'bad_psi', 'bad_electrode', 'partial_missing_g2')
NET_FILES = (('network_conductivity_dual.json', None), ('network_conductivity.json', 'hertzian'),
             ('network_conductivity_hertzian.json', 'hertzian'), ('network_conductivity_physics.json', 'physics'))
G2_ONLY = ('electrode_model', 'bulk_model', 'area_rule', 'area_rule_physics', 'hertz_constriction', 'sensitivity_mode', 'hertz_h12',
           'area_binding_counts_physics', 'n_area_physics_unavailable', 'n_clamp_zero', 'n_floor_only', 'h_film_nm', 'h_film_status',
           'solve_method_full', 'solve_certificate_full', 'solve_certificate_bulk_net', 'solve_certificate_constr_net')
G2_CHANNEL = ('electrode_model', 'bulk_model', 'area_rule', 'area_rule_physics', 'area_binding_counts_physics', 'n_clamp_zero', 'n_floor_only',
              'psi_placement')
STAMP_G2_KEYS = ('psi_placement_physics', 'electrode_model', 'area_rule_physics', 'hertz_h12')


def chk(label, ok, detail=''):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f'  PASS {label}')
    else:
        FAIL += 1
        print(f'  FAIL {label}' + (f' — {str(detail)[:400]}' if detail else ''))


def change(du, label):
    """Codex probes/publication.py `change` 그대로."""
    for k, r in du.items():
        if not isinstance(r, dict):
            continue
        if label == 'h12_as_primary' and k == 'hertzian':
            r.update(copy.deepcopy(r['hertz_h12']))
        elif label == 'bad_psi' and k == 'physics':
            r['psi_placement'] = 'multiply_TYPO'
        elif label == 'bad_electrode':
            r['electrode_model'] = 'DIRICHLET_TYPO'
            if 'hertz_h12' in r:
                r['hertz_h12']['electrode_model'] = 'DIRICHLET_TYPO'
        elif label == 'partial_missing_g2' and k == 'physics':
            for key in ('area_rule', 'psi_placement'):
                r.pop(key, None)


def strip_g2(du):
    """세대 2 표지를 전부 뺀다 (값 그대로 · 역사 레코드 모양 — resistance_model · contact_mode · ψ legacy_divide 만)."""
    for m in ('hertzian', 'physics'):
        r = du.get(m)
        if not isinstance(r, dict):
            continue
        for k in list(r):
            if k in G2_ONLY or any(k == f'{ch}_{g}' for ch in ('electronic', 'thermal') for g in G2_CHANNEL):
                r.pop(k, None)
        r['psi_placement'] = 'legacy_divide'


#: ★ 10-06 밤 G2RR-02 (Codex 세대 2 재검증 §3 · probes/acceptance.py) — 증서 ↔ 가지 · 역할 · 발행값 결합 변이 (네 사본에 같이 · σ · 모델 표기는 그대로)
CERT_LABELS = ('full_cert_from_cf', 'full_cert_from_h12', 'full_cert_g2q_x2', 'full_cert_cf_disguised', 'numbers_only',
               'cf_bad_conservation', 'missing_cf_cert', 'missing_constr_cert', 'certs_unbound')
CERT_KEYS = ('solve_certificate_full', 'solve_certificate_bulk_net', 'solve_certificate_constr_net')
CERT_BIND = ('branch', 'channel', 'role', 'contact_mode', 'delta_V', 'geometry', 'g_to_q', 'sigma_bulk_S_cm')    # 독립 오라클


def _geo(c):
    """증서의 기하 — 없으면 (고치기 전 생산자) 이 침대 (판 20 · 상자 10 · 척도 1) 의 기하를 넣는다 (옛 코드에서도 변이가 적용돼 실패로 보이게)."""
    return c.setdefault('geometry', {'plate_z': 20.0, 'box_x': 10.0, 'box_y': 10.0, 'scale': 1})


def cchange(du, label):
    """G2RR-02 변이 — du = {'hertzian': …, 'physics': …} (둘 중 하나만 있어도 된다 · 사본마다 같은 결과)."""
    rh, rp = du.get('hertzian'), du.get('physics')
    if label == 'full_cert_from_cf' and rh:
        rh['solve_certificate_full'] = copy.deepcopy(rh['solve_certificate_bulk_net'])
    elif label == 'full_cert_from_h12' and rh:
        rh['solve_certificate_full'] = copy.deepcopy(rh['hertz_h12']['solve_certificate_full'])
    elif label == 'full_cert_g2q_x2' and rh:
        c = rh['solve_certificate_full']
        c['g_to_q'] = (c.get('g_to_q') or 0.2) * 2
    elif label == 'full_cert_cf_disguised' and rh:          # CF 증서 · 가지 'full' · 판 높이를 발행 q 에 맞춰 재척도 (증서 하나 안은 자기일관 · 재구성도 맞다)
        c = copy.deepcopy(rh['solve_certificate_bulk_net'])
        g = _geo(c)
        a_ = g['box_x'] * g['box_y'] * g['scale'] ** 2
        g['plate_z'] = rh['sigma_full'] / c['I_bottom'] * a_ / g['scale']
        c['g_to_q'] = (g['plate_z'] * g['scale']) / a_
        c['branch'] = 'full'
        rh['solve_certificate_full'] = c
    elif label == 'numbers_only':                           # 숫자만 ×1.25 — σ_ratio · σ_dim 두 표현 항등식은 맞춘다 (공용 기술 검사 통과)
        for r in (rh, rp):
            if r:
                r['sigma_full'] = round(r['sigma_full'] * 1.25, 8)
                r['sigma_full_mScm'] = round(r['sigma_full'] * r['sigma_grain_S_cm'] * 1000, 6)
    elif label == 'cf_bad_conservation' and rh:
        rh['solve_certificate_bulk_net'].update(I_top=0.0, conservation_rel=1.0)
    elif label == 'missing_cf_cert' and rh:
        rh.pop('solve_certificate_bulk_net', None)
    elif label == 'missing_constr_cert' and rh:
        rh.pop('solve_certificate_constr_net', None)
    elif label == 'certs_unbound':                          # G2RR-02 이전 세대 2 증서 모양 (결합 키 없음) — 옛 기록 정책
        for r in (rh, (rh or {}).get('hertz_h12'), rp):
            for k, v in (r or {}).items():
                if k.endswith(CERT_KEYS) and isinstance(v, dict):
                    for b in CERT_BIND:
                        v.pop(b, None)


def mut(d, label):
    """Codex `mut` 그대로 — 네 망 JSON (dual · legacy · 모드 파일 둘) 에 같은 변이 (사본끼리 일관)."""
    for name, key in NET_FILES:
        p = Path(d) / name
        obj = json.loads(p.read_text(encoding='utf-8'))
        wrapped = obj if key is None else {key: obj}
        if label == 'legacy_shape':
            strip_g2(wrapped)
        elif label in CERT_LABELS:
            cchange(wrapped, label)
        else:
            change(wrapped, label)
        p.write_text(json.dumps(obj), encoding='utf-8')


def _why(stages):
    return ' | '.join(str(s.get('stderr') or '') for s in stages if not s.get('ok'))


def _write_clamp_bed(d):
    """GEN2-01 침대 — through 사슬 (21 구 · 판 20 · 상자 10) 에서 가운데 접촉 (10–11) 의 c_cpl[22] 만 π(1.02 r)² (원판 > π r_min²) → physics g2 · H12 의
    협착-only 관통 간선 R_c = 0 = NOT_COMPUTED zero_resistance_requires_contraction (FULL · CF 는 그대로).  장부는 through 와 같다 (원자 · 접촉 쌍이 같다)."""
    import math
    a, c = TP._write_bed(d, 'through')
    _A, C, _plate, _box = TP._bed('through')
    with open(c, 'w') as f:
        f.write('id1,id2,fn_x,fn_y,fn_z,ft_x,ft_y,ft_z,contact_area,delta\n' + ''.join(
            f'{r["id1"]},{r["id2"]},0,0,0,0,0,0,{(math.pi * 1.02 ** 2 if r["id1"] == 10 else r["contact_area"])!r},{r["delta"]!r}\n'
            for r in C))
    return a, c


def _publish(app, label, stop=True, bed='through'):
    d = tempfile.mkdtemp(prefix=f'g2ph_{label}_')
    a, c = _write_clamp_bed(d) if bed == 'clamp' else TP._write_bed(d, bed)
    with open(os.path.join(d, 'full_metrics.json'), 'w') as f:
        json.dump(TP._bed_ledger('through' if bed == 'clamp' else bed), f)
    runner = TP._CLIRunner(mutate=(None if label == 'baseline' else (lambda p, _l=label: mut(p, _l))), delegate=TP._fake_stage_e)
    stages, rid = app._network_and_stage_e(d, str(SCRIPTS), a, c, '1:SE', 1, [], runner=runner, stop_before_stage_e=stop)
    st, failed = ps.summarize(stages)
    return d, st, failed, rid


def _force(app, base_dir, rid, label, dst, stamp='restamp'):
    """게시된 baseline 폴더를 복사해 네 망 JSON 을 변이 → 웹앱 투영으로 full_metrics → 도장 (restamp = 옛 게시가 남겼을 도장 · keep = baseline 도장 그대로
    · historical = 세대 2 키 없는 옛 도장 모양)."""
    shutil.copytree(base_dir, dst)
    if label != 'baseline':
        mut(dst, label)
    proj = app._network_projection(str(dst), rid)
    if proj.get('error') or proj.get('fm') is None:
        raise RuntimeError(f'투영 실패: {proj.get("error")}')
    (Path(dst) / 'full_metrics.json').write_text(json.dumps(proj['fm']), encoding='utf-8')
    prov0 = ps.read_network_provenance(str(base_dir))
    if stamp in ('restamp', 'historical'):
        p = ps.stamp_network_provenance(str(dst), rid, prov0.get('input_digests') or {}, 'success', argv=prov0.get('argv') or {})
        if stamp == 'historical':
            for k in STAMP_G2_KEYS:
                p.pop(k, None)
            (Path(dst) / ps.PROVENANCE_FILE).write_text(json.dumps(p), encoding='utf-8')
    return Path(dst)


def main():
    import app
    import tau_flux as tf
    import lhs_webapp_batch as LWB
    import lhs_design_dataset as LDD
    GEN_COL = getattr(tf, 'ROW_GENERATION_COL', 'ion_net_generation')
    tmp = Path(tempfile.mkdtemp(prefix='g2ph_root_'))
    made = []
    try:
        print('① 게시 — 실 생산자 + Codex 변이 → 망 정지 계약 (정지 경로) · 공용 기록 검사 (일반 경로)')
        b_d, b_st, b_f, b_rid = _publish(app, 'baseline')
        made.append(b_d)
        chk(f'①a 양성 — baseline (실 생산자 세 모드 그대로) = done · 활성 세대 = 이번 실행 ({b_st})',
            b_st == 'done' and ps.read_network_provenance(b_d).get('network_run_id') == b_rid, _why(b_f))
        pub = {}
        for lab in LABELS + ('legacy_shape',):
            d, st, f, rid = _publish(app, lab)
            made.append(d)
            prov = ps.read_network_provenance(d)
            left = sorted(n for n in os.listdir(d) if n.startswith('network_conductivity'))
            att = json.load(open(os.path.join(d, ps.ATTEMPT_FILE))) if os.path.exists(os.path.join(d, ps.ATTEMPT_FILE)) else {}
            pub[lab] = (st, prov.get('provenance_state'), bool(left), att.get('failure_kind'), _why(f))
        bad = {k: v[:4] for k, v in pub.items() if v[:4] != ('failed', 'missing', False, 'candidate_rejected')}
        chk(f'①b ★ 정지 경로 — h12_as_primary · bad_psi · bad_electrode · partial_missing_g2 · 표지 없는 옛 모양 → failed · 활성 세대 없음 · 망 JSON 안 남음 · '
            f'최근 시도 candidate_rejected (옛: 다섯 다 done) {bad or ""}', not bad and len(pub) == 5)
        why = {k: v[4] for k, v in pub.items()}
        chk('①c 거부 사유 = 세대 계약 (⑨ · 주 Hertz 자리 · 모르는 값 · 부분 결손 · 옛 세대 추론 불가) — 사유가 보인다',
            all('세대' in w and '⑨' in w for w in why.values()) and 'hertz' in why['h12_as_primary'].lower()
            and 'inferred_legacy' in why['legacy_shape'], {k: v[:160] for k, v in why.items()})
        gen = {}
        for lab in ('baseline', 'h12_as_primary', 'bad_psi', 'legacy_shape'):
            d, st, f, rid = _publish(app, lab, stop=False)
            made.append(d)
            gen[lab] = (st, any(ps.NETWORK_RECORD_CHECK_STEP in str(s.get('step')) for s in f), _why(f)[:160])
        chk(f'①d ★ 일반 경로 (Stage E 앞 승격) — baseline done · h12_as_primary · bad_psi · 표지 없는 옛 모양 = failed (승격 전 공용 기록 검사 · '
            f'RGLR2-01 과 같은 자리) {gen}',
            gen['baseline'][0] == 'done' and all(gen[k][:2] == ('failed', True) for k in ('h12_as_primary', 'bad_psi', 'legacy_shape')))

        print('② 인계 — 디스크에 강제로 남긴 폴더 → load_tau_results (출처 관문 P0–P4)')
        src = ROOT / 'docs/data/lhs_webapp_contact_d1ec42fba'
        st0 = json.loads((src / 'status.json').read_text(encoding='utf-8'))

        def _tau_batch(tag, cases):
            root = tmp / f'tau_{tag}'
            res_ = root / 'results'
            res_.mkdir(parents=True)
            stx = json.loads(json.dumps(st0))
            stx.update(stop_after='network', cases={})
            rowsx = {}
            for c, d_ in cases.items():
                shutil.copytree(d_, res_ / c)
                fm_ = json.loads((res_ / c / 'full_metrics.json').read_text(encoding='utf-8'))
                stx['cases'][c] = dict(case=c, stop_after='network', status='done', failed_stages=[], network_run_id=fm_['network_run_id'])
                rowsx[c] = dict({k: v for k, v in fm_.items() if not isinstance(v, (dict, list))}, case=c)
            LWB.write_outputs(root / 'batch', stx, rowsx)
            return res_, LDD.load_webapp(root / 'batch')

        def _load(tag, cases):
            res_, lw_ = _tau_batch(tag, cases)
            try:
                return LDD.load_tau_results(res_, lw_), ''
            except Exception as e:                                       # noqa: BLE001
                return None, f'{type(e).__name__}: {e}'

        forced = {lab: _force(app, b_d, b_rid, lab, tmp / f'forced_{lab}') for lab in ('baseline',) + LABELS}
        forced['bad_psi_b'] = _force(app, b_d, b_rid, 'bad_psi', tmp / 'forced_bad_psi_b')
        tv0, e0 = _load('ctrl', {'lhs00_000': forced['baseline']})
        cells0 = ((tv0 or {}).get('cases') or {}).get('lhs00_000', {}).get('cells') or {}
        chk('②a 대조 — 같은 강제 절차 (복사 · 투영 · 도장) 로 만든 변이 없는 폴더는 통과 (P0–P4) · 세 모드 OK',
            not e0 and all(cells0.get(f'ion_net_status_{m}') == 'OK' for m in ('hertz', 'physics', 'hertz_h12')), e0[:300])
        chk("②a2 ★ 통과한 행의 세대 칸 = 'g2' (인계표 소비자가 세대를 본다)", cells0.get(GEN_COL) == 'g2', cells0.get(GEN_COL))
        hv = {}
        for tag, cases in ([(lab, {'lhs00_000': forced[lab]}) for lab in LABELS]
                           + [('mix_h12', {'lhs00_000': forced['baseline'], 'lhs00_001': forced['h12_as_primary']}),
                              ('mix_psi', {'lhs00_000': forced['baseline'], 'lhs00_001': forced['bad_psi']}),
                              ('same_defect', {'lhs00_000': forced['bad_psi'], 'lhs00_001': forced['bad_psi_b']})]):
            tv_, e_ = _load(tag, cases)
            hv[tag] = e_
        bad_h = {k: (v[:120] or '통과') for k, v in hv.items() if not (v.startswith('FillRefusal') and 'τ P4' in v and '세대' in v)}
        chk(f'②b ★ 강제 폴더 — 단독 넷 · [baseline, h12_as_primary] · [baseline, bad_psi] · [bad_psi, bad_psi] (같은 결함 코호트) → 전부 거부 '
            f'(τ P4 세대 계약 · 옛: 일곱 다 통과) {bad_h or ""}', not bad_h and len(hv) == 7)

        print('③ 옛 세대 추론 자격 — 표지 없는 레코드 ↔ 도장')
        f_keep = _force(app, b_d, b_rid, 'legacy_shape', tmp / 'forced_legacy_keep', stamp='keep')
        f_hist = _force(app, b_d, b_rid, 'legacy_shape', tmp / 'forced_legacy_hist', stamp='historical')
        tvk, ek = _load('legacy_keep', {'lhs00_000': f_keep})
        tvh, eh = _load('legacy_hist', {'lhs00_000': f_hist})
        ch = ((tvh or {}).get('cases') or {}).get('lhs00_000', {}).get('cells') or {}
        chk('③a ★ 표지 없는 레코드 + 세대 2 를 말하는 도장 (게시 뒤 표기만 지운 폴더) → 거부 (옛 세대 추론 자격 없음 · 옛: 통과)',
            ek.startswith('FillRefusal') and 'τ P4' in ek and '세대' in ek, ek[:300] or '통과')
        chk("③b 양성 — 같은 레코드 + 세대 2 키 없는 옛 도장 모양 → 통과 · 세대 칸 'inferred_legacy' · 주 두 모드 OK · H12 = NOT_COMPUTED (missing_input)",
            not eh and ch.get(GEN_COL) == 'inferred_legacy' and ch.get('ion_net_status_hertz') == ch.get('ion_net_status_physics') == 'OK'
            and ch.get('ion_net_status_hertz_h12') == 'NOT_COMPUTED' and ch.get('ion_net_status_reason_hertz_h12') == 'missing_input',
            eh[:300] or {k: ch.get(k) for k in (GEN_COL, 'ion_net_status_hertz', 'ion_net_status_reason_hertz_h12')})
        #  ③c 거울 — 세대 2 표기 레코드 + 세대 2 이전 코드의 도장 (세대 키가 하나도 없음 = 194 v1.2 도장 모양) = 옛 폴더에 표기를 덧붙인 모양 (표기만 보는
        #     계약은 g2 로 받는다) → 거부.  세대 2 레코드는 세대 2 코드만 낼 수 있고 그 코드의 게시는 늘 세대 키를 찍는다 (pipeline_service.stamp_network_provenance).
        f_g2h = _force(app, b_d, b_rid, 'baseline', tmp / 'forced_g2_histstamp', stamp='historical')
        _tvg, eg = _load('g2_histstamp', {'lhs00_000': f_g2h})
        chk('③c ★ 세대 2 표기 레코드 + 세대 키 없는 옛 도장 (역사 폴더에 표기만 덧붙인 모양) → 거부 (세대 2 로 싣지 않는다 · 옛: 통과)',
            eg.startswith('FillRefusal') and 'τ P4' in eg and '세대' in eg, eg[:300] or '통과')

        print('④ 표 만들 때 (build_handover) — 같은 결함만 모인 원천도 거부 (행마다 먼저)')
        with open(src / 'metrics_flat.csv', encoding='utf-8', newline='') as fh:
            flat = {r['case']: {k: v for k, v in r.items() if v != ''} for r in csv.DictReader(fh)}
        done = sorted(c for c, r in st0['cases'].items() if r.get('status') == 'done' and c in flat
                      and float(flat[c].get('percolation_pct', 'nan')) > 0.0)
        pick = done[:2]
        tie = tuple(ps.NETWORK_STOP_LEDGER_KEYS) + tuple(getattr(LDD, 'TAU_TIE_EXTRA', ()))
        root4 = tmp / 'bh'
        res4 = root4 / 'results'
        res4.mkdir(parents=True)
        st4 = json.loads(json.dumps(st0))
        st4.update(stop_after='network', cases={})
        rows4 = {}
        for c in pick:
            shutil.copytree(forced['baseline'], res4 / c)
            fm_ = json.loads((res4 / c / 'full_metrics.json').read_text(encoding='utf-8'))
            st4['cases'][c] = dict(st0['cases'][c], stop_after='network', status='done', failed_stages=[], network_run_id=fm_['network_run_id'])
            rows4[c] = dict(flat[c], **{kk: fm_[kk] for kk in tie if kk in fm_})
        LWB.write_outputs(root4 / 'batch', st4, rows4)
        lw4 = LDD.load_webapp(root4 / 'batch')
        with (ROOT / LDD.DESCRIPTOR_FILL_EXPECTED['path']).open(encoding='utf-8-sig') as fh:
            rows_d = [r for r in csv.DictReader(fh) if r['case_id'] in set(pick)]
        hvst = LDD.load_harvest(ROOT / 'docs/data/lhs_descriptors_cov_1e09f661d')
        un = LDD.load_union(ROOT / LDD.DEFAULT_UNION_TSV)
        try:
            tv4 = LDD.load_tau_results(res4, lw4)
            o4, _c4, _r4 = LDD.build_handover(rows_d, hvst, union=un, webapp=lw4, webapp_groups='tau', tau=tv4)
            e4 = ''
        except Exception as e:                                           # noqa: BLE001
            tv4, o4, e4 = None, [], f'{type(e).__name__}: {e}'
        chk('④a 양성 — 실 배치 케이스 둘 + baseline 폴더 → load_tau_results · build_handover 통과 · 두 행 세대 칸 g2',
            not e4 and len(o4) == 2 and all(r.get(GEN_COL) == 'g2' for r in o4), e4[:300] or [r.get(GEN_COL) for r in o4])
        if tv4 is not None:
            tvx = json.loads(json.dumps(tv4))
            for c in pick:                                                # 같은 결함 (두 행 다 주 Hertz 칸 = H12 표기)
                tvx['cases'][c]['cells'].update(ion_net_constriction_hertz='mikic_psi_multiply', ion_net_bulk_hertz='sphere_segment')
            try:
                LDD.build_handover(rows_d, hvst, union=un, webapp=lw4, webapp_groups='tau', tau=tvx)
                e5 = '거부하지 않았다'
            except Exception as e:                                       # noqa: BLE001
                e5 = f'{type(e).__name__}: {e}'
            chk('④b ★ 다른 길로 들어온 원천 — 두 행 다 같은 결함 (주 Hertz 칸 = H12 표기) → build_handover 거부 (τ 세대 · 옛: 동질이라 통과)',
                e5.startswith('FillRefusal') and 'τ 세대' in e5, e5[:300])
        else:
            chk('④b (④a 실패로 건너뜀)', False)

        print('⑤ ★ G2RR-02 — 증서 ↔ 가지 · 역할 · 발행값 결합 (실 생산자 → 정지 계약 · 일반 경로 → τ 소비자 → 인계 · Codex probes/acceptance.py)')
        MODES3 = ('hertz', 'physics', 'hertz_h12')
        pub5 = {}
        for lab in CERT_LABELS:
            d, st, f, rid = _publish(app, lab)
            made.append(d)
            prov = ps.read_network_provenance(d)
            left = sorted(n for n in os.listdir(d) if n.startswith('network_conductivity'))
            att = json.load(open(os.path.join(d, ps.ATTEMPT_FILE))) if os.path.exists(os.path.join(d, ps.ATTEMPT_FILE)) else {}
            pub5[lab] = (st, prov.get('provenance_state'), bool(left), att.get('failure_kind'), _why(f))
        bad5 = {k: v[:4] for k, v in pub5.items() if v[:4] != ('failed', 'missing', False, 'candidate_rejected')}
        chk(f'⑤a ★ 정지 경로 — 증서 결합 변이 {len(CERT_LABELS)} 종 (CF → FULL · H12 → H0 · 기하 인자 · 위장 CF · 숫자만 · CF 보존 실패 · CF · 협착-only 증서 '
            f'삭제 · 결합 키 없음) → failed · 활성 세대 없음 · 망 JSON 안 남음 · candidate_rejected (옛: 아홉 다 done · Codex 표 넷 재현) {bad5 or ""}',
            not bad5 and len(pub5) == len(CERT_LABELS))
        why5 = {k: v[4] for k, v in pub5.items()}
        chk('⑤a2 거부 사유 = 정지 계약 ⑨ 의 수치 증서 · 결합 (G2RR-02) — 사유가 보인다',
            all('⑨' in w and 'G2RR-02' in w for w in why5.values()), {k: v[:200] for k, v in why5.items()})
        gen5 = {}
        for lab in ('full_cert_from_cf', 'full_cert_from_h12', 'numbers_only'):
            d, st, f, rid = _publish(app, lab, stop=False)
            made.append(d)
            gen5[lab] = (st, any(ps.NETWORK_RECORD_CHECK_STEP in str(s.get('step')) for s in f), _why(f)[:160])
        chk(f'⑤b ★ 일반 경로 (Stage E 앞 승격) — CF → FULL · H12 → H0 · 숫자만 = failed (승격 전 공용 기록 검사) {gen5}',
            all(v[:2] == ('failed', True) for v in gen5.values()) and len(gen5) == 3)
        f5 = {lab: _force(app, b_d, b_rid, lab, tmp / f'forced5_{lab}') for lab in CERT_LABELS}
        rows5 = {lab: tf.case_row(str(p)) for lab, p in f5.items()}
        bad_r5 = {lab: (tuple((r.get(f'ion_net_status_{m}'), tf.reason_code(r.get(f'ion_net_status_reason_{m}'))) for m in MODES3), r.get(GEN_COL),
                        r.get('tau2_ion_hertz'))
                  for lab, r in rows5.items()
                  if not (all(r.get(f'ion_net_status_{m}') == 'NOT_COMPUTED' and tf.reason_code(r.get(f'ion_net_status_reason_{m}')) == 'invalid_input'
                              for m in MODES3) and r.get(GEN_COL) == 'invalid' and r.get('tau2_ion_hertz') is None)}
        chk(f'⑤c ★ τ 소비자 (tau_flux.case_row) — 디스크에 강제로 남긴 변이 폴더 {len(f5)} (복사 · 투영 · 도장) → 세 모드 NOT_COMPUTED (invalid_input) · '
            f'세대 invalid · 주 tau2 빈칸 (옛: CF → FULL 이 tau2 10.98 OK) {bad_r5 or ""}', not bad_r5 and len(rows5) == len(CERT_LABELS))
        hv5 = {}
        for lab, p in f5.items():
            _tv5, e5_ = _load(f'g2rr_{lab}', {'lhs00_000': p})
            hv5[lab] = e5_
        bad_h5 = {k: (v[:160] or '통과') for k, v in hv5.items() if not (v.startswith('FillRefusal') and 'τ P4' in v and 'G2RR-02' in v)}
        chk(f'⑤d ★ 인계 (load_tau_results) — 같은 강제 폴더 {len(hv5)} → 전부 거부 (τ P4 세대 계약 · 수치 증서 · 결합 G2RR-02 · 옛: 통과) {bad_h5 or ""}',
            not bad_h5 and len(hv5) == len(CERT_LABELS))
        pos5, dpos = {}, {}
        for lab, bed in (('비관통', 'nonthrough'), ('GEN2-01', 'clamp')):
            d, st, f, rid = _publish(app, 'baseline', bed=bed)
            made.append(d)
            dpos[lab] = d
            row = tf.case_row(d)
            tvp, ep = _load(f'pos5_{bed}', {'lhs00_000': d})
            cp = ((tvp or {}).get('cases') or {}).get('lhs00_000', {}).get('cells') or {}
            pos5[lab] = (st, tuple(row.get(f'ion_net_status_{m}') for m in MODES3), row.get(GEN_COL), ep[:200],
                         tuple(cp.get(f'ion_net_status_{m}') for m in MODES3))
        du_cl = json.load(open(os.path.join(dpos['GEN2-01'], 'network_conductivity_dual.json'))) if pos5['GEN2-01'][0] == 'done' else {}
        zr = {k: (r or {}).get('sigma_constr_net_reason') for k, r in (('physics', du_cl.get('physics')),
                                                                         ('hertz_h12', (du_cl.get('hertzian') or {}).get('hertz_h12')))}
        chk('⑤e ★ 양성 — 진짜 비관통 = done · τ 세 모드 NOT_PERCOLATING · 인계 통과 / GEN2-01 (physics · H12 협착-only NOT_COMPUTED zero_resistance · 숫자 없음) = '
            f'done · τ 세 모드 OK · 인계 통과 — 해 없는 가지에 수렴 증서를 요구하지 않는다 {pos5} {zr}',
            pos5['비관통'] == ('done', ('NOT_PERCOLATING',) * 3, 'g2', '', ('NOT_PERCOLATING',) * 3)
            and pos5['GEN2-01'] == ('done', ('OK',) * 3, 'g2', '', ('OK',) * 3)
            and set(zr.values()) == {'zero_resistance_requires_contraction'})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        for d in made:
            shutil.rmtree(d, ignore_errors=True)

    print(f'\ntest_gen2_publication_handover: {PASS}/{PASS + FAIL} PASS')
    return 0 if FAIL == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

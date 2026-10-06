#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LHS ML 인계 배포 v1.3 (최종판) 생성기 — 시험 먼저 (1저자 10-07 *"v1.3 생성기를 Codex 판정과 동시에 미리 준비"*).

v1.3 = 세대 2 망 값 + #1 ML 표 (빈칸 뜻대로) · #2 f 타깃 · 관통 분류 안내 · #5 porosity–σ–CN 재적합 · τ 표시 이름 (수송 tortuosity) ·
새 열 se_isolated_pct (= 100 − top_reachable_pct).  실제 v1.3 자료는 Codex GO + 새 세대 2 194 배치 뒤에만 만든다 — 이 시험은
① 합성 입력 (세대 2 표기로 옮긴 합성 인계표 · 손 오라클) 과 ② 커밋된 v1.2 원천 (세대 1) 의 DRY RUN 으로 생성기 경로를 돈다.

  V0  API 가 있다
  V1  열 명세 — 주 표 = v1.2 주 표 열 + se_isolated_pct + 세대 2 표기 (Hertz) + 완료 압력 · Physics 부록 = v1.2 부록 + 세대 2 표기 · H12 는 주 표에 없다
  V2  빈칸 뜻 규칙 (닫힌 어휘) — mono 없는 상 · 접촉 0 평균 · 비관통 (N/A) · 비관통 T (∞) · 기술 실패 · HOLD · 빈 사유
  V3  빈칸 일관성 — 설명 안 되는 빈칸 · 빈칸이어야 할 칸의 값 · 상태 ↔ 값 모순을 거부 (양방향)
  V4  열 역할 (ML) — 모든 열이 닫힌 역할 표에 있다 · X = 자유 설계 노브 5 · 모르는 열 = 거부
  V5  ML 표 — 빈칸 코드 열 (두 데이터셋 합집합) · 되읽기 = 배포 값 그대로 · 데이터셋 표지 · 관통 분류 열
  V6  se_isolated_pct 항등식 (= 100 − top_reachable_pct · ≤ 100 − percolation_pct)
  V7  #5 재적합 — 합성 법칙 회복 · 고정 지수 (½ · 2) · 비관통 제외 · 결정적 · 입력 부족 거부
  V8  세대 관문 — g2 통과 · inferred_legacy 는 dry-run 만 · 섞임 · H12 를 주 자리에 = 거부
  V9  배치 manifest 관문 — 선언 없음 · inferred_legacy · g2 · 커밋된 v1.2 manifest = 거부
  V10 단계 A 명령 — 생성기 CLI 에 --tau-batch-manifest · --tau-results · se_isolation 묶음 · 압력 기록
  V11 τ 다시 읽기 배선 — load_tau_results(expected_generation='g2') 호출 · 칸 대조 · 거부 전파
  V12 실제 경로 (합성 세대 2 인계표) — 만들기 → check_v13 통과 · 변조 (ML 코드 · se_isolated · 재적합 · 파일) 검출
  V13 실제 경로 거부 — Codex 판정문 없음 · manifest 세대 · τ 다시 읽기 문제 → 산출 없음
  V14 DRY RUN (커밋된 v1.2 = 세대 1) — dry-run 없이 거부 · dry-run 이면 표지 (DRYRUN_ · "DRY RUN — not a release") · docs/data 아래 거부
  V15 CLI — --v13 --dry-run · --v13-check · dry-run 없는 세대 1 거부 (rc ≠ 0 · 폴더 안 만듦)
  V16 발사 봉인 대조 (세대 2 등록 20261007_g2 §3 · §5) — manifest code_hashes ↔ 지금 체크아웃 (다르면 거부 · --allow-seal-diff 명시 승인 · 기록) ·
      handover_code_hashes 다름 = 경고 · ⓪b 다시 읽기 기록 (reread.json) 실패 = 거부 · 단계 A 도 같은 관문 · CLI ·
      ★ 10-07 G2RR2-02 — 다시 읽기 기록이 등록 집합 production194 전부 (기대 = 읽음 · 같음) 가 아니면 거부 (V16n · V16o)

  python3 scripts/test_lhs_release_v13.py
"""
import contextlib
import csv
import io
import json
import math
import os
import random
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import lhs_release_build as LRB          # noqa: E402
import lhs_design_dataset as LDD         # noqa: E402
import tau_flux as TF                    # noqa: E402

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:300]})' if why else ''))
    return cond


def safe(fn, default=None):
    """시험 대상이 없거나 (옛 코드) 예외면 ('ERR', 사유) — 한 시험의 실패가 나머지를 막지 않게."""
    try:
        return fn()
    except (Exception, SystemExit) as e:                                  # noqa: BLE001 — 옛 CLI 는 모르는 인자에 SystemExit
        return ('ERR', f'{type(e).__name__}: {e}') if default is None else default


def is_err(x):
    return isinstance(x, tuple) and len(x) == 2 and x[0] == 'ERR'


def refused(fn, tag=''):
    """fn() 이 ReleaseError (또는 FillRefusal) 로 거부하고 메시지에 tag 가 있으면 True."""
    try:
        fn()
    except Exception as e:                                                # noqa: BLE001
        bad = getattr(LRB, 'ReleaseError', RuntimeError)
        return isinstance(e, (bad, LDD.FillRefusal)) and tag in str(e)
    return False


V12 = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006')
BATCH12 = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8')
REL12 = os.path.join(ROOT, 'docs', 'data', 'lhs_release_20261006_v12')
DATE = '20991231'

#: 세대 2 역할 표기 오라클 (손 칸 — 도우미 상수를 베끼지 않는다 · lhs_release_build selftest ⑳ 와 같은 값)
G2H = {'constriction': 'maxwell_halfspace', 'psi': '', 'area_rule': 'hertz_ccpl22', 'electrode': 'dirichlet_exact', 'bulk': 'cylinder_half_d',
       'area_mode': 'hertz'}
G2P = {'constriction': 'mikic_psi_multiply', 'psi': 'multiply', 'area_rule': 'physics_g2', 'electrode': 'dirichlet_exact',
       'bulk': 'cylinder_half_d', 'area_mode': 'physics'}
G2H12 = {'constriction': 'mikic_psi_multiply', 'psi': 'multiply', 'area_rule': 'hertz_ccpl22', 'electrode': 'dirichlet_exact',
         'bulk': 'sphere_segment', 'area_mode': 'hertz'}
PRESS = {'press_target_mpa': '300.0', 'press_last_loop_mpa': '300.41', 'press_reached': 'True', 'press_log_sha256': 'a' * 64}


def _read_csv(p):
    with open(p, encoding='utf-8', newline='') as f:
        r = csv.reader(f)
        h = next(r)
        return h, [dict(zip(h, row)) for row in r]


def _write_csv(p, head, rows):
    with open(p, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(head)
        for r in rows:
            w.writerow([r.get(c, '') for c in head])


def make_g2_handover_dir(td, mutate=None):
    """합성 세대 2 인계표 묶음 (테스트 전용) — 커밋된 v1.2 인계표 행 (실값) 을 지금 생성기 스키마로 옮긴다:
    τ 열 = tau_flux.column_names() (세 모드) · 표기 = 세대 2 오라클 · H12 = Hertz 값 복사 · se_isolated_pct = 100 − top_reachable_pct ·
    press_* = 합성 기록 · 열 사전 = 지금 생성기 column_dictionary (웹앱 판정 = 커밋된 194 배치) · τ 출처 부록 = 지금 검사 목록.
    ⚠ 숫자는 세대 1 값 그대로다 — 경로 · 관문 시험이지 세대 2 값이 아니다."""
    os.makedirs(td, exist_ok=True)
    tcols = TF.column_names()
    for ds in ('lhs', 'lhsx'):
        head, rows = _read_csv(os.path.join(V12, f'{ds}_handover_v12_20261006.csv'))
        base = [c for c in head if LDD.tau_net_define(c) is None]
        i = base.index('am_ionic_isolated_pct') + 1
        new_head = base[:i] + ['se_isolated_pct'] + base[i:] + tcols + list(PRESS)
        out = []
        for r in rows:
            o = {c: r.get(c, '') for c in base}
            o['se_isolated_pct'] = repr(100.0 - float(r['top_reachable_pct']))
            for m, src, lab in (('hertz', 'hertz', G2H), ('physics', 'physics', G2P), ('hertz_h12', 'hertz', G2H12)):
                for b in ('f_ion_{}', 'f_ion_{}_gap', 'tau2_ion_{}', 'tau_ion_{}', 'ion_net_status_{}', 'ion_net_status_reason_{}',
                          'ion_net_band_rule_{}', 'ion_net_band_frac_{}', 'ion_net_basis_check_{}'):
                    o[b.format(m)] = r.get(b.format(src), '')
                for k, v in lab.items():
                    o[f'ion_net_{k}_{m}'] = v
            for c in ('ion_sigma0_mScm', 'ion_sigma0_T_C', 'phi_basis', 'L_basis'):
                o[c] = r.get(c, '')
            o['ion_net_generation'] = 'g2'
            o.update(PRESS)
            out.append(o)
        if mutate:
            mutate(ds, new_head, out)
        stem = os.path.join(td, f'{ds}_handover_v13_{DATE}')
        _write_csv(stem + '.csv', new_head, out)
        wv = LDD.load_webapp(os.path.join(BATCH12, 'merged', ds))
        with open(stem + '_columns.tsv', 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, ['column', 'source', 'verdict', 'meaning', 'caveat'], delimiter='\t', lineterminator='\n')
            w.writeheader()
            for d in LDD.column_dictionary(new_head, webapp=wv, design_source='(합성)'):
                w.writerow(d)
        with open(os.path.join(V12, f'{ds}_handover_v12_20261006_tau_provenance.tsv'), encoding='utf-8', newline='') as f:
            prov = list(csv.DictReader(f, delimiter='\t'))
        with open(stem + '_tau_provenance.tsv', 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, LDD.TAU_PROVENANCE_COLS, delimiter='\t', lineterminator='\n')
            w.writeheader()
            for p in prov:
                w.writerow(dict(p, same_generation_checks=';'.join(LDD.TAU_SAME_GEN_CHECKS)))
    return td


#: 합성 발사 봉인 (실행기 manifest code_hashes 의 부분집합 · 지금 파일 지문) · 인계 단계 지문 (handover_code_hashes) — 손 목록 (실행기 상수를 베끼지 않는다)
SEAL_FILES = ('scripts/tau_flux.py', 'scripts/network_conductivity.py', 'webapp/pipeline_service.py', 'webapp/app.py')
HANDOVER_FILES = ('scripts/lhs_design_dataset.py', 'scripts/g2_network_reread.py')


def _sha_file(rel):
    return __import__('hashlib').sha256(open(os.path.join(ROOT, rel), 'rb').read()).hexdigest()


#  ⓪b 다시 읽기 기록 (g2_network_reread --launcher-root … --expect-set production194 --json) 의 통과 모양 — 10-07 G2RR2-02 부터 등록 집합 필드 필수
RR_OK = {'schema': 'g2_network_reread/v2', 'expected_generation': 'g2', 'n_fail': 0, 'expected_set': 'production194', 'expected_source': 'registered',
         'expected_n': 194, 'read_n': 194, 'set_equal': True, 'missing': [], 'extra': []}


def make_batch_root(td, gen='g2', code=True, handover=True, alter=None, reread=None):
    """합성 배치 뿌리 — manifest (기대 세대 선언 · 코호트 원천 · 발사 봉인 code_hashes · handover_code_hashes) 만 (τ 다시 읽기는 시험에서 대역).
    code / handover = 지금 체크아웃의 파일 지문 (같다) · alter = {파일: 가짜 지문} (발사 뒤 바뀐 파일 흉내) · reread = ⓪b 다시 읽기 기록 dict (있으면 reread.json)."""
    os.makedirs(td, exist_ok=True)
    man = {'schema': 'network_parallel_launcher/v1', 'stop_after': 'network',
           'plan': {'cohorts': [
               {'name': 'lhs', 'harvest_dir': '/x/docs/data/lhs_descriptors_cov_1e09f661d', 'union': 'docs/data/lhs_union_20260927/lhs130_union.tsv',
                'design': ''},
               {'name': 'lhsx', 'harvest_dir': '/x/docs/data/lhsx_descriptors_cov_1e09f661d',
                'union': 'docs/data/lhs_union_20260927/lhsx64_union.tsv', 'design': 'docs/data/lhsx_design_adapted_20260929.csv'}]}}
    if gen is not None:
        man['expected_network_generation'] = gen
    if code:
        man['code_hashes'] = {rel: _sha_file(rel) for rel in SEAL_FILES}
    if handover:
        man['handover_code_hashes'] = {rel: _sha_file(rel) for rel in HANDOVER_FILES}
    for rel, h in (alter or {}).items():
        man['handover_code_hashes' if rel in HANDOVER_FILES else 'code_hashes'][rel] = h
    with open(os.path.join(td, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(man, f)
    if reread is not None:
        with open(os.path.join(td, 'reread.json'), 'w', encoding='utf-8') as f:
            json.dump(reread, f)
    return td


# ═══ V0 ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V0  API')
API = ('v13_columns', 'v13_blank_reason', 'v13_blank_problems', 'v13_role', 'v13_ml_table', 'v13_ml_decode', 'v13_se_isolated_problems',
       'refit_porosity_sigma_cn', 'refit_from_csv', 'v13_generation_problems', 'v13_manifest_generation', 'v13_handover_argv',
       'v13_reread_tau', 'build_v13', 'check_v13', 'V13_BLANK_CODES', 'v13_seal_drift', 'v13_batch_gate_files')
miss = [a for a in API if not hasattr(LRB, a)]
chk('V0 v1.3 API 가 lhs_release_build 에 있다', not miss, miss)

# ═══ V1 열 명세 ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V1  열 명세')
m_l = safe(lambda: LRB.v13_columns('lhs', 'main'))
m_x = safe(lambda: LRB.v13_columns('lhsx', 'main'))
ph_l = safe(lambda: LRB.v13_columns('lhs', 'physics'))
b12 = [r[0] for r in csv.reader(open(os.path.join(REL12, 'lhs_release_20261006_v12_columns.tsv'), encoding='utf-8'), delimiter='\t')][1:]
b12x = [r[0] for r in csv.reader(open(os.path.join(REL12, 'lhsx_release_20261006_v12_columns.tsv'), encoding='utf-8'), delimiter='\t')][1:]
p12 = [r[0] for r in csv.reader(open(os.path.join(REL12, 'lhs_release_20261006_v12_physics_columns.tsv'), encoding='utf-8'), delimiter='\t')][1:]
ADD = ['se_isolated_pct', 'ion_net_generation', 'ion_net_constriction_hertz', 'ion_net_area_rule_hertz', 'ion_net_electrode_hertz',
       'ion_net_bulk_hertz', 'press_target_mpa', 'press_last_loop_mpa', 'press_reached']
chk('V1a 주 표 (130) = v1.2 주 표 열 (순서 그대로) + se_isolated_pct · 세대 2 표기 (Hertz) · 완료 압력 (끝에)',
    isinstance(m_l, list) and m_l == b12 + ADD, m_l if not isinstance(m_l, list) else [c for c in m_l if c not in b12])
chk('V1b 주 표 (64) = v1.2 주 표 열 + 같은 추가 · H12 · physics 열 없음',
    isinstance(m_x, list) and m_x == b12x + ADD and not any('h12' in c or c.endswith('_physics') for c in m_x), m_x)
chk('V1c Physics 부록 = v1.2 부록 열 + 세대 칸 · Physics 표기 다섯 (협착 · ψ · 면적 규칙 · 전극 · bulk)',
    isinstance(ph_l, list) and ph_l == p12 + ['ion_net_generation', 'ion_net_constriction_physics', 'ion_net_psi_physics',
                                              'ion_net_area_rule_physics', 'ion_net_electrode_physics', 'ion_net_bulk_physics'], ph_l)
chk('V1d 완료 압력 미검사 (--pressure-unverified) 명세는 press_* 를 빼고 나머지 같다',
    safe(lambda: LRB.v13_columns('lhs', 'main', press=False)) == b12 + ADD[:6])

# ═══ V2 빈칸 뜻 규칙 ══════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V2  빈칸 뜻 규칙')
BASE = {'block': 'bimodal', 'percolation_pct': '40.0', 'ion_net_status_hertz': 'OK', 'physical_target_status': 'OK',
        'area_AM_P_AM_P_n': '5', 'am_am_n_contacts': '20', 'ion_net_status_physics': 'OK'}


def br(col, **kv):
    return safe(lambda: LRB.v13_blank_reason(dict(BASE, **kv), col))


cases2 = [
    ('mono_AM_S 의 d_am_p_um', br('d_am_p_um', block='mono_AM_S'), 'NA_PHASE_ABSENT'),
    ('mono_AM_P 의 AM_S_ionic_dead_pct', br('AM_S_ionic_dead_pct', block='mono_AM_P'), 'NA_PHASE_ABSENT'),
    ('mono 의 size_ratio_P_over_S', br('size_ratio_P_over_S', block='mono_AM_P'), 'NA_PHASE_ABSENT'),
    ('mono 의 area_AM_P_AM_S_total', br('area_AM_P_AM_S_total', block='mono_AM_S'), 'NA_PHASE_ABSENT'),
    ('bimodal 의 d_am_p_um = 값', br('d_am_p_um'), None),
    ('AM_P–AM_P 접촉 0 의 평균', br('area_AM_P_AM_P_mean', area_AM_P_AM_P_n='0'), 'NA_ZERO_CONTACTS'),
    ('AM_P–AM_P 접촉 0 의 총합 = 측정된 0 (값)', br('area_AM_P_AM_P_total', area_AM_P_AM_P_n='0'), None),
    ('AM–AM 접촉 0 의 파괴 지수', br('fracture_index_force', am_am_n_contacts='0'), 'NA_ZERO_CONTACTS'),
    ('AM–AM 접촉 0 의 am_am_mean_area', br('am_am_mean_area', am_am_n_contacts='0'), 'NA_ZERO_CONTACTS'),
    ('비관통 se_se_cn_perc', br('se_se_cn_perc', percolation_pct='0.0'), 'NA_NOT_PERCOLATING'),
    ('비관통 기하 τ (tortuosity_SE_wall)', br('tortuosity_SE_wall', percolation_pct='0.0'), 'NA_NOT_PERCOLATING'),
    ('비관통 tau2_ion_hertz = ∞', br('tau2_ion_hertz', ion_net_status_hertz='NOT_PERCOLATING'), 'INF_NOT_PERCOLATING'),
    ('비관통 tau_ion_hertz = ∞', br('tau_ion_hertz', ion_net_status_hertz='NOT_PERCOLATING'), 'INF_NOT_PERCOLATING'),
    ('비관통 f_ion_hertz = 값 (0.0)', br('f_ion_hertz', ion_net_status_hertz='NOT_PERCOLATING'), None),
    ('NOT_COMPUTED 의 f', br('f_ion_hertz', ion_net_status_hertz='NOT_COMPUTED'), 'NOT_COMPUTED'),
    ('BAND_FALLBACK 의 tau2', br('tau2_ion_hertz', ion_net_status_hertz='BAND_FALLBACK'), 'HOLD_BAND_FALLBACK'),
    ('MBCB 의 tau2 = 값', br('tau2_ion_physics', ion_net_status_physics='MODEL_BELOW_CONTINUUM_BOUND'), None),
    ('OK 행 hold_reason_codes 빈칸 = 사유 없음', br('hold_reason_codes'), 'EMPTY_NO_REASON'),
    ('HOLD 행 hold_reason_codes = 값', br('hold_reason_codes', physical_target_status='HOLD'), None),
    ('상태 OK 의 사유 칸 빈칸 = 사유 없음', br('ion_net_status_reason_hertz'), 'EMPTY_NO_REASON'),
    ('NOT_COMPUTED 의 사유 칸 = 값', br('ion_net_status_reason_hertz', ion_net_status_hertz='NOT_COMPUTED'), None),
]
bad2 = [(n, got, want) for n, got, want in cases2 if got != want]
chk(f'V2 빈칸 뜻 {len(cases2)} 경우 (닫힌 어휘 · 값이어야 할 칸 = None)', not bad2, bad2[:4])
codes = safe(lambda: set(LRB.V13_BLANK_CODES), set())
chk('V2b 어휘 = NA_PHASE_ABSENT · NA_ZERO_CONTACTS · NA_NOT_PERCOLATING · INF_NOT_PERCOLATING · NOT_COMPUTED · HOLD_BAND_FALLBACK · EMPTY_NO_REASON',
    codes == {'NA_PHASE_ABSENT', 'NA_ZERO_CONTACTS', 'NA_NOT_PERCOLATING', 'INF_NOT_PERCOLATING', 'NOT_COMPUTED', 'HOLD_BAND_FALLBACK',
              'EMPTY_NO_REASON'}, codes)

# ═══ V3 빈칸 일관성 (양방향) ══════════════════════════════════════════════════════════════════════════════════════════════════════
print('V3  빈칸 일관성')
COLS3 = ['case_id', 'block', 'd_am_p_um', 'coverage_AM_P_hertz_pct', 'percolation_pct', 'f_ion_hertz', 'tau2_ion_hertz', 'ion_net_status_hertz',
         'ion_net_status_reason_hertz', 'physical_target_status', 'hold_reason_codes']
OK3 = [{'case_id': 'a', 'block': 'bimodal', 'd_am_p_um': '9.0', 'coverage_AM_P_hertz_pct': '40.0', 'percolation_pct': '80.0', 'f_ion_hertz': '0.05',
        'tau2_ion_hertz': '5.0', 'ion_net_status_hertz': 'OK', 'ion_net_status_reason_hertz': '', 'physical_target_status': 'OK',
        'hold_reason_codes': ''},
       {'case_id': 'b', 'block': 'mono_AM_S', 'd_am_p_um': '', 'coverage_AM_P_hertz_pct': '', 'percolation_pct': '0.0', 'f_ion_hertz': '0.0',
        'tau2_ion_hertz': '', 'ion_net_status_hertz': 'NOT_PERCOLATING', 'ion_net_status_reason_hertz': '', 'physical_target_status': 'HOLD',
        'hold_reason_codes': 'NEGATIVE_POROSITY'}]
chk('V3a 맞는 표 → 문제 0', safe(lambda: LRB.v13_blank_problems(OK3, COLS3)) == [])


def p3(i, **kv):
    rows = [dict(r) for r in OK3]
    rows[i].update(kv)
    return safe(lambda: LRB.v13_blank_problems(rows, COLS3))


neg3 = [('설명 안 되는 빈칸 (bimodal coverage_AM_P 빈칸)', p3(0, coverage_AM_P_hertz_pct=''), 'a'),
        ('빈칸이어야 할 칸의 값 (mono_AM_S 의 d_am_p_um)', p3(1, d_am_p_um='3.0'), 'b'),
        ('NOT_PERCOLATING 인데 tau2 값', p3(1, tau2_ion_hertz='9.9'), 'b'),
        ('OK 인데 tau2 빈칸', p3(0, tau2_ion_hertz=''), 'a'),
        ('NOT_PERCOLATING 인데 f 빈칸 (0.0 이어야)', p3(1, f_ion_hertz=''), 'b'),
        ('NOT_PERCOLATING 인데 f ≠ 0', p3(1, f_ion_hertz='0.01'), 'b'),
        ('HOLD 인데 사유 빈칸', p3(1, hold_reason_codes=''), 'b')]
bad3 = [n for n, got, case in neg3 if not (isinstance(got, list) and got and any(case in p for p in got))]
chk(f'V3b 반례 {len(neg3)} — 전부 문제로 보고 (그 행 이름과 함께)', not bad3, bad3)

# ═══ V4 열 역할 ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V4  열 역할')
roles = safe(lambda: {c: LRB.v13_role(c) for c in (m_l if isinstance(m_l, list) else [])}, {})
chk('V4a 주 표 열 전부 역할이 있다 (닫힌 표)', bool(roles) and len(roles) == len(m_l if isinstance(m_l, list) else []) and all(roles.values()))
chk('V4b X = 자유 설계 노브 5 개 · f_ion_hertz = 주 타깃 · tau2 · tau = 항등식 유도 (타깃 금지) · 상태 열 · 적격성 · 상수',
    sorted(c for c, r in roles.items() if r == 'X') == sorted(['am_pct', 'ps_frac', 'd_am_p_um', 'd_am_s_um', 'd_se_um'])
    and roles.get('f_ion_hertz') == 'Y_TARGET' and roles.get('tau2_ion_hertz') == 'Y_IDENTITY' and roles.get('tau_ion_hertz') == 'Y_IDENTITY'
    and roles.get('ion_net_status_hertz') == 'STATUS' and roles.get('physical_target_status') == 'FLAG' and roles.get('pressure_MPa') == 'CONST'
    and roles.get('n_SE_measured') == 'RESULT_COUNT' and roles.get('se_isolated_pct') == 'Y', {c: roles.get(c) for c in ('f_ion_hertz', 'tau2_ion_hertz')})
chk('V4c 모르는 열 = 거부 (기본 역할로 흘리지 않는다)', refused(lambda: LRB.v13_role('zz_new_col'), 'zz_new_col'))

# ═══ V5 ML 표 ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V5  ML 표')
COLS5 = ['case_id', 'block', 'am_pct', 'd_am_p_um', 'percolation_pct', 'top_reachable_pct', 'f_ion_hertz', 'tau2_ion_hertz', 'ion_net_status_hertz',
         'ion_net_status_reason_hertz', 'physical_target_status', 'hold_reason_codes']
R5 = {'lhs': [dict(OK3[0], am_pct='80.0', top_reachable_pct='90.0'), dict(OK3[1], am_pct='70.0', top_reachable_pct='20.0')],
      'lhsx': [dict(OK3[0], case_id='x1', am_pct='50.0', top_reachable_pct='99.0', physical_target_status='HOLD', hold_reason_codes='NEGATIVE_POROSITY')]}
ml = safe(lambda: LRB.v13_ml_table({ds: (COLS5, rows) for ds, rows in R5.items()}))
ok5 = isinstance(ml, tuple) and len(ml) == 2 and isinstance(ml[0], dict)
mlt, mld = (ml if ok5 else ({}, []))
mcols = (mlt.get('lhs') or ([], []))[0] if ok5 else []
chk('V5a 열 = case_id · dataset · 배포 열 (빈칸이 있는 열 뒤에 <열>__blank) · 끝에 ion_percolates_hertz · 두 데이터셋 같은 열',
    ok5 and mcols[:2] == ['case_id', 'dataset'] and 'd_am_p_um__blank' in mcols and mcols.index('d_am_p_um__blank') == mcols.index('d_am_p_um') + 1
    and 'tau2_ion_hertz__blank' in mcols and 'am_pct__blank' not in mcols and mcols[-1] == 'ion_percolates_hertz'
    and (mlt.get('lhsx') or ([], []))[0] == mcols, mcols)
rows5 = (mlt.get('lhs') or ([], []))[1] if ok5 else []
b5 = next((r for r in rows5 if r.get('case_id') == 'b'), {})
a5 = next((r for r in rows5 if r.get('case_id') == 'a'), {})
chk('V5b 코드 — mono 없는 상 = NA_PHASE_ABSENT · 비관통 T = INF_NOT_PERCOLATING · f = 0.0 (코드 없음) · OK 행 사유 = EMPTY_NO_REASON · 관통 분류 1/0',
    b5.get('d_am_p_um') == '' and b5.get('d_am_p_um__blank') == 'NA_PHASE_ABSENT' and b5.get('tau2_ion_hertz__blank') == 'INF_NOT_PERCOLATING'
    and b5.get('f_ion_hertz') == '0.0' and 'f_ion_hertz__blank' not in mcols and a5.get('hold_reason_codes__blank') == 'EMPTY_NO_REASON'
    and a5.get('tau2_ion_hertz__blank') == '' and a5.get('ion_percolates_hertz') == '1' and b5.get('ion_percolates_hertz') == '0'
    and b5.get('dataset') == 'lhs', (a5, b5))
dec = safe(lambda: LRB.v13_ml_decode(mcols, rows5))
chk('V5c 되읽기 — ML 표에서 코드 · 표지 · 분류 열을 빼면 배포 열 · 값이 그대로', isinstance(dec, tuple) and dec[0] == COLS5
    and [[r[c] for c in COLS5] for r in dec[1]] == [[r[c] for c in COLS5] for r in R5['lhs']], dec)
roles5 = {d.get('column'): d.get('role') for d in (mld if isinstance(mld, list) else [])}
chk('V5d ML 열 사전 — 열마다 역할 (코드 열 = BLANK_CODE · 분류 = Y_CLASS · dataset = DATASET) · 빈칸 코드 개수',
    roles5.get('d_am_p_um__blank') == 'BLANK_CODE' and roles5.get('ion_percolates_hertz') == 'Y_CLASS' and roles5.get('dataset') == 'DATASET'
    and roles5.get('am_pct') == 'X' and any('NA_PHASE_ABSENT' in str(d.get('blank_codes', '')) for d in (mld if isinstance(mld, list) else [])),
    roles5)
R5b = {'lhs': [dict(OK3[0], am_pct='80.0', top_reachable_pct='90.0', coverage_AM_P_hertz_pct='')]}
chk('V5e 설명 안 되는 빈칸이 있으면 ML 표를 만들지 않는다 (추측으로 코드를 달지 않는다)',
    refused(lambda: LRB.v13_ml_table({'lhs': (COLS5 + ['coverage_AM_P_hertz_pct'], R5b['lhs'])}), 'a'))

# ═══ V6 se_isolated_pct ══════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V6  se_isolated_pct 항등식')
S6 = [{'case_id': 'a', 'top_reachable_pct': '90.0', 'percolation_pct': '85.0', 'se_isolated_pct': repr(10.0)},
      {'case_id': 'b', 'top_reachable_pct': '20.0', 'percolation_pct': '0.0', 'se_isolated_pct': repr(80.0)}]
chk('V6a 맞는 행 → 문제 0', safe(lambda: LRB.v13_se_isolated_problems(S6)) == [])
s6b = safe(lambda: LRB.v13_se_isolated_problems([dict(S6[0], se_isolated_pct='11.0')]))
s6c = safe(lambda: LRB.v13_se_isolated_problems([dict(S6[0], top_reachable_pct='10.0', se_isolated_pct='90.0')]))
s6d = safe(lambda: LRB.v13_se_isolated_problems([{k: v for k, v in S6[0].items() if k != 'se_isolated_pct'}]))
chk('V6b 반례 — 100 − top 아님 · > 100 − percolation · 열 없음 → 문제',
    all(isinstance(x, list) and x for x in (s6b, s6c, s6d)), (s6b, s6c, s6d))

# ═══ V7 재적합 ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V7  porosity–σ–CN 재적합')
rnd = random.Random(7)


def synth_rows(n, alpha, beta, a0, noise=0.0, nonperc=3):
    out = []
    for i in range(n):
        p = rnd.choice([0.0, 0.3, 0.5, 0.7, 1.0])
        rs, rp = rnd.uniform(1.0, 2.5), rnd.uniform(3.0, 6.0)
        phi = rnd.uniform(0.22, 0.75)
        cn = rnd.uniform(2.5, 7.0)
        g = LRB._refit_gate(p, rs if p < 1 else None, rp if p > 0 else None)
        pe = LRB._refit_phi_eff(phi, g)
        lf = a0 + alpha * math.log(pe) + beta * math.log(cn) + rnd.gauss(0.0, noise)
        out.append({'case_id': f's{i:03d}', 'dataset': 'lhs' if i % 3 else 'lhsx', 'ion_net_status_hertz': 'OK', 'f_ion_hertz': repr(math.exp(lf)),
                    'phi_se_mass_conserving': repr(phi), 'porosity_union_exact_pct': repr(100 * (1 - phi / 0.4) if phi < 0.4 else 10.0),
                    'se_se_cn': repr(cn), 'ps_frac': repr(p), 'r_AM_S_um': repr(rs) if p < 1 else '', 'r_AM_P_um': repr(rp) if p > 0 else ''})
    for j in range(nonperc):
        out.append({'case_id': f'n{j}', 'dataset': 'lhs', 'ion_net_status_hertz': 'NOT_PERCOLATING', 'f_ion_hertz': '0.0',
                    'phi_se_mass_conserving': '0.12', 'porosity_union_exact_pct': '20.0', 'se_se_cn': '1.5', 'ps_frac': '0.5', 'r_AM_S_um': '2.0',
                    'r_AM_P_um': '5.0'})
    return out


rows7 = safe(lambda: synth_rows(60, 0.8, 1.6, -3.0, noise=0.0), [])
fit7 = safe(lambda: LRB.refit_porosity_sigma_cn(rows7))
okf = isinstance(fit7, dict) and 'summary' in fit7
fr = (fit7.get('summary') or {}).get('fits', {}).get('free', {}) if okf else {}
lk = (fit7.get('summary') or {}).get('fits', {}).get('locked', {}) if okf else {}
chk('V7a 잡음 없는 합성 법칙 (α 0.8 · β 1.6) — free 적합이 지수를 회복 (1e-6) · R² = 1 · LOOCV ≈ 1',
    okf and abs(fr.get('params', {}).get('alpha', 9) - 0.8) < 1e-6 and abs(fr.get('params', {}).get('beta', 9) - 1.6) < 1e-6
    and abs(fr.get('params', {}).get('a', 9) + 3.0) < 1e-6 and fr.get('r2', 0) > 1 - 1e-9, fr)
chk('V7b locked = 지수 ½ · 2 고정 (등록식 φ_eff^½ · CN²) · 자유 매개변수 1 (a) · LOOCV ≤ R²',
    okf and lk.get('params', {}).get('alpha') == 0.5 and lk.get('params', {}).get('beta') == 2.0 and lk.get('n_free') == 1
    and lk.get('loocv_r2', 9) <= lk.get('r2', -9) + 1e-12, lk)
summ7 = (fit7.get('summary') or {}) if okf else {}
chk('V7c 비관통 3 행은 적합 밖 (사유 NOT_PERCOLATING · 분류 가지) · 표에 행은 남는다 (포함 0)',
    okf and summ7.get('n_fit') == 60 and summ7.get('excluded', {}).get('NOT_PERCOLATING') == 3
    and sum(1 for r in fit7.get('rows', []) if r.get('included') == '0') == 3, summ7.get('excluded'))
rows7n = safe(lambda: synth_rows(80, 0.6, 2.2, -4.0, noise=0.05), [])
f1, f2 = safe(lambda: LRB.refit_porosity_sigma_cn(rows7n)), safe(lambda: LRB.refit_porosity_sigma_cn([dict(r) for r in rows7n]))
chk('V7d 결정적 — 같은 입력 두 번 = 같은 요약 JSON (정렬 키 · repr)', isinstance(f1, dict) and json.dumps(f1, sort_keys=True) == json.dumps(f2, sort_keys=True))
chk('V7e 적합 행 < 5 이면 거부 · 필요한 열이 없으면 거부',
    refused(lambda: LRB.refit_porosity_sigma_cn(rows7[:3]), '') and refused(lambda: LRB.refit_porosity_sigma_cn([{k: v for k, v in r.items()
                                                                                                                     if k != 'se_se_cn'} for r in rows7]), 'se_se_cn'))
chk('V7f 요약 = 식 · 상수 (φc_P 0.200 · φc_S 0.195 · δ 0.040 · r_cut 3.5 · 지수 2 — 등록식 동결값) · 데이터셋별 편향',
    okf and summ7.get('constants', {}).get('phi_c_P') == 0.2 and summ7.get('constants', {}).get('phi_c_S') == 0.195
    and summ7.get('constants', {}).get('delta') == 0.04 and 'lhs' in fr.get('by_dataset', {}) and 'lhsx' in fr.get('by_dataset', {}), summ7.get('constants'))

# ═══ V8 세대 관문 ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V8  세대 관문')


def trow(case, gen, lab_h=G2H, lab_p=G2P, lab_12=G2H12):
    r = {'case_id': case, 'ion_net_generation': gen}
    for m, lab in (('hertz', lab_h), ('physics', lab_p), ('hertz_h12', lab_12)):
        for k, v in (lab or {}).items():
            r[f'ion_net_{k}_{m}'] = v
    return r


G1H = dict(G2H, electrode='virtual_source_legacy')
G1P = {'constriction': 'mikic_psi_divide', 'psi': 'legacy_divide', 'area_rule': 'physics_g1', 'electrode': 'virtual_source_legacy',
       'bulk': 'cylinder_half_d', 'area_mode': 'physics'}
NO12 = {k: '' for k in G2H}
g2rows = [trow('a', 'g2'), trow('b', 'g2')]
legrows = [trow('c', 'inferred_legacy', G1H, G1P, NO12)]
gp = safe(lambda: LRB.v13_generation_problems(g2rows))
chk('V8a 세대 2 행 → (g2, 문제 0)', gp == ('g2', []), gp)
gl = safe(lambda: LRB.v13_generation_problems(legrows))
gld = safe(lambda: LRB.v13_generation_problems(legrows, dry_run=True))
chk('V8b inferred_legacy (세대 1) → 실제 배포는 문제 · dry-run 은 통과 (세대 기록)',
    isinstance(gl, tuple) and not is_err(gl) and gl[1] and gld == ('inferred_legacy', []), (gl, gld))
gm = safe(lambda: LRB.v13_generation_problems(g2rows + legrows, dry_run=True))
chk('V8c 세대 섞임 = dry-run 이어도 문제', isinstance(gm, tuple) and not is_err(gm) and gm[1], gm)
gh = safe(lambda: LRB.v13_generation_problems([trow('d', 'g2', lab_h=G2H12)]))
chk('V8d H12 표기를 주 Hertz 자리에 (G2R-01) = 문제', isinstance(gh, tuple) and not is_err(gh) and gh[1], gh)

# ═══ V9 배치 manifest 관문 ═══════════════════════════════════════════════════════════════════════════════════════════════════════
print('V9  배치 manifest 관문')
with tempfile.TemporaryDirectory() as td9:
    chk('V9a 기대 세대 선언 없는 manifest → 거부', refused(lambda: LRB.v13_manifest_generation(os.path.join(make_batch_root(os.path.join(td9, 'a'), None),
                                                                                                        'manifest.json')), 'expected_network_generation'))
    chk('V9b inferred_legacy 선언 → v1.3 은 거부 (최종판 = 세대 2 만)',
        refused(lambda: LRB.v13_manifest_generation(os.path.join(make_batch_root(os.path.join(td9, 'b'), 'inferred_legacy'), 'manifest.json')), 'g2'))
    chk('V9c g2 선언 → g2', safe(lambda: LRB.v13_manifest_generation(os.path.join(make_batch_root(os.path.join(td9, 'c'), 'g2'), 'manifest.json'))) == 'g2')
chk('V9d 커밋된 v1.2 배치 manifest (11fcf91e8 · 선언 없음) → 거부', refused(lambda: LRB.v13_manifest_generation(os.path.join(BATCH12, 'manifest.json')), ''))

# ═══ V10 단계 A 명령 ═════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V10 단계 A (인계표 생성기 CLI)')
av = safe(lambda: LRB.v13_handover_argv('lhsx', '/R', '/H/lhsx_handover_v13_X.csv', pressure='/R/pressure/lhsx_pressure_record.tsv'))
avu = safe(lambda: LRB.v13_handover_argv('lhs', '/R', '/H/lhs_handover_v13_X.csv', pressure=None))


def _opt(a, k):
    return a[a.index(k) + 1] if isinstance(a, list) and k in a else None


chk('V10a 생성기 CLI — --tau-batch-manifest R/manifest.json · --tau-results R/merged/<ds>/results · --webapp R/merged/<ds> · 묶음 + se_isolation · 압력 기록',
    isinstance(av, list) and _opt(av, '--tau-batch-manifest') == '/R/manifest.json' and _opt(av, '--tau-results') == '/R/merged/lhsx/results'
    and _opt(av, '--webapp') == '/R/merged/lhsx' and set((_opt(av, '--webapp-groups') or '').split(',')) == {
        'contact', 'percolation', 'f1', 'fracture', 'area', 'tau', 'se_isolation'}
    and _opt(av, '--pressure-record') == '/R/pressure/lhsx_pressure_record.tsv' and _opt(av, '--design') == 'docs/data/lhsx_design_adapted_20260929.csv'
    and _opt(av, '--export-handover') == '/H/lhsx_handover_v13_X.csv', av)
chk('V10b 압력 기록 없음 = --pressure-unverified (명시 승인) · 130 은 --design 없음 (기본 설계)',
    isinstance(avu, list) and '--pressure-unverified' in avu and '--pressure-record' not in avu and '--design' not in avu
    and _opt(avu, '--union') == 'docs/data/lhs_union_20260927/lhs130_union.tsv', avu)

#  V10c–e — 단계 A 실행 (subprocess 대역): manifest 관문이 생성기 실행 **전** · 리포 루트에서 · 데이터셋 둘 · 압력 기록 없으면 거부 (명시 승인 없이)
_sp_calls = []


class _FakeRun:
    def __init__(self, rc=0):
        self.returncode, self.stdout, self.stderr = rc, '→ 합성 인계표 (대역)', ''


_orig_run = None
with tempfile.TemporaryDirectory() as td10:
    if hasattr(LRB, 'subprocess'):
        _orig_run = LRB.subprocess.run
        #  생성기 호출 (--export-handover) 만 대역 — 나머지 (git 기록 등) 는 진짜로 돈다
        LRB.subprocess.run = lambda argv, **kw: ((_sp_calls.append((argv, kw.get('cwd'))) or _FakeRun()) if '--export-handover' in argv
                                                 else _orig_run(argv, **kw))
    try:
        b_g2 = make_batch_root(os.path.join(td10, 'b_g2'), 'g2')
        r10c = safe(lambda: LRB.stage_handovers_v13(b_g2, os.path.join(td10, 'h_ok'), DATE, pressure_unverified=True))
        chk('V10c 단계 A — 생성기 두 번 (lhs · lhsx) · 리포 루트에서 · 둘 다 --tau-batch-manifest <배치>/manifest.json · --pressure-unverified',
            not is_err(r10c) and [os.path.basename(c[0][c[0].index('--export-handover') + 1]) for c in _sp_calls]
            == [f'lhs_handover_v13_{DATE}.csv', f'lhsx_handover_v13_{DATE}.csv'] and all(c[1] == ROOT for c in _sp_calls)
            and all(_opt(c[0], '--tau-batch-manifest') == os.path.join(b_g2, 'manifest.json') for c in _sp_calls), (r10c, _sp_calls))
        n0 = len(_sp_calls)
        b_lg = make_batch_root(os.path.join(td10, 'b_lg'), 'inferred_legacy')
        chk('V10d manifest inferred_legacy → 생성기를 부르기 전에 거부', refused(lambda: LRB.stage_handovers_v13(b_lg, os.path.join(td10, 'h_lg'), DATE,
                                                                                                   pressure_unverified=True), 'g2') and len(_sp_calls) == n0)
        chk('V10e 압력 기록이 없고 명시 승인도 없으면 → 거부 (DESC-06)', refused(lambda: LRB.stage_handovers_v13(b_g2, os.path.join(td10, 'h_np'), DATE),
                                                                         'DESC-06') and len(_sp_calls) == n0)
    finally:
        if _orig_run is not None:
            LRB.subprocess.run = _orig_run

# ═══ V11 τ 다시 읽기 배선 ════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V11 τ 다시 읽기 (load_tau_results · 배치 manifest 기대 세대)')
calls = []
_orig = (LDD.load_tau_results, LDD.load_webapp)
TC = TF.column_names()
HROWS = [dict({c: '' for c in TC}, case_id='a', wa_status='done', f_ion_hertz='0.1'), dict({c: '' for c in TC}, case_id='b', wa_status='done')]


def fake_ltr(results_dir, webapp, expected_generation=None):
    calls.append((str(results_dir), expected_generation))
    return {'schema': LDD.TAU_NET_SCHEMA, 'cases': {r['case_id']: {'cells': {c: r[c] for c in TC}} for r in HROWS}}


try:
    LDD.load_tau_results, LDD.load_webapp = fake_ltr, (lambda d, census=None: {'stop_after': 'network', 'status': {}, 'rows': {}})
    p11 = safe(lambda: LRB.v13_reread_tau('lhs', '/R', HROWS, 'g2'))
    chk('V11a load_tau_results(R/merged/lhs/results, expected_generation="g2") 를 부르고 칸이 같으면 문제 0',
        p11 == [] and calls and calls[-1] == (os.path.join('/R', 'merged', 'lhs', 'results'), 'g2'), (p11, calls))
    HROWS2 = [dict(HROWS[0], f_ion_hertz='0.2'), HROWS[1]]
    p11b = safe(lambda: LRB.v13_reread_tau('lhs', '/R', HROWS2, 'g2'))
    chk('V11b 인계표 τ 칸 ≠ 다시 읽은 칸 → 문제 (케이스 · 열)', isinstance(p11b, list) and any('a' in p and 'f_ion_hertz' in p for p in p11b), p11b)

    def boom(*a, **k):
        raise LDD.FillRefusal('τ P4 — 배치 기대 세대 g2 ≠ 레코드 세대 inferred_legacy')
    LDD.load_tau_results = boom
    p11c = safe(lambda: LRB.v13_reread_tau('lhs', '/R', HROWS, 'g2'))
    chk('V11c load_tau_results 거부 (기대 세대 ≠ 레코드) → 문제로 전파 (삼키지 않는다)', isinstance(p11c, list) and any('inferred_legacy' in p for p in p11c), p11c)
finally:
    LDD.load_tau_results, LDD.load_webapp = _orig

# ═══ V12 실제 경로 (합성 세대 2 인계표) ═══════════════════════════════════════════════════════════════════════════════════════════
print('V12 실제 경로 (합성 세대 2 인계표 · τ 다시 읽기 대역)')
_orig_rr = getattr(LRB, 'v13_reread_tau', None)
rr_calls = []
with tempfile.TemporaryDirectory() as td:
    hdir = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    broot = make_batch_root(os.path.join(td, 'batch'), 'g2')
    verdict = os.path.join(td, 'codex_gen2_go.md')
    open(verdict, 'w', encoding='utf-8').write('# GO (합성)\n')
    tfile = os.path.join(td, 'transfer.txt')
    open(tfile, 'w', encoding='utf-8').write('합성 전달 문단 첫 줄 — 판정문 그대로.\n\n둘째 문단.\n')
    out = os.path.join(td, 'release_v13')
    rep = ('ERR', 'not run')
    if _orig_rr is not None:
        LRB.v13_reread_tau = lambda ds, root, rows, gen: rr_calls.append((ds, root, len(rows), gen)) or []
        try:
            rep = safe(lambda: LRB.build_v13(out_dir=out, handover_dir=hdir, batch_root=broot, date=DATE, codex_verdict=verdict,
                                             transfer_text=tfile))
        finally:
            LRB.v13_reread_tau = _orig_rr
    okb = isinstance(rep, dict)
    chk('V12a 만들기 성공 · τ 다시 읽기를 두 데이터셋에 기대 세대 g2 로 불렀다', okb and sorted((c[0], c[3]) for c in rr_calls) == [('lhs', 'g2'), ('lhsx', 'g2')]
        and sorted(c[2] for c in rr_calls) == [64, 130], (rep if not okb else rr_calls))
    names = sorted(os.listdir(out)) if os.path.isdir(out) else []
    want = [f'lhs_release_{DATE}_v13.csv', f'lhs_release_{DATE}_v13_columns.tsv', f'lhsx_release_{DATE}_v13.csv', f'lhs_release_{DATE}_v13_physics.csv',
            f'lhs_mltable_{DATE}_v13.csv', f'lhs_mltable_{DATE}_v13_columns.tsv', 'lhs_v13_refit_porosity_sigma_cn_rows.csv',
            'lhs_v13_refit_porosity_sigma_cn_summary.json', 'README.md', 'v13_build_manifest.json', 'origin', 'previews']
    chk('V12b 산출 — 주 표 · 열 사전 · Physics 부록 · ML 표 · 재적합 (행 · 요약) · README · 빌드 manifest · origin · previews (DRYRUN 표지 없음)',
        all(w in names for w in want) and not any(n.startswith('DRYRUN') for n in names), [w for w in want if w not in names])
    if okb:
        hl, rl = _read_csv(os.path.join(out, f'lhs_release_{DATE}_v13.csv'))
        chk('V12c 주 표 130 × (v1.2 132 + 9) · se_isolated_pct = 100 − top_reachable_pct (전 행) · H12 열 없음',
            len(rl) == 130 and len(hl) == 141 and all(abs(float(r['se_isolated_pct']) - (100 - float(r['top_reachable_pct']))) < 1e-9 for r in rl)
            and not any('h12' in c for c in hl), len(hl))
        prob = safe(lambda: LRB.check_v13(out, hdir))
        chk('V12d check_v13 — 배포 ⊆ 인계표 · ML 표 되읽기 · 빈칸 일관성 · se_isolated · 재적합 재현 · 세대 · sha256 = 문제 0', prob == [], prob)
        man = json.load(open(os.path.join(out, 'v13_build_manifest.json'), encoding='utf-8'))
        chk('V12e 빌드 manifest — dry_run false · 세대 g2 (두 데이터셋) · τ 다시 읽기 수행 · Codex 판정문 · 파일 sha256',
            man.get('dry_run') is False and man.get('generation') == {'lhs': 'g2', 'lhsx': 'g2'} and man.get('tau_reread') == 'performed'
            and man.get('codex_verdict') and isinstance(man.get('files'), dict) and len(man['files']) >= 10, {k: man.get(k) for k in ('dry_run', 'generation')})
        rd = open(os.path.join(out, 'README.md'), encoding='utf-8').read()
        chk('V12f README — v1.3 최종판 · 빈칸 코드 표 (#1) · f_ion_hertz 타깃 · 관통 분류 먼저 (#2) · 재적합 (#5) · 수송 tortuosity · se_isolated_pct · DRY RUN 아님',
            all(k in rd for k in ('v1.3', 'NA_PHASE_ABSENT', 'INF_NOT_PERCOLATING', 'f_ion_hertz', '관통 분류', 'porosity–σ–CN', '수송 tortuosity',
                                  'se_isolated_pct', '제곱근 아님')) and 'DRY RUN' not in rd)
        chk('V12k 전달 문안 (--transfer-text) — README 외부 검토 절에 그대로 (인용) · 빌드 manifest 에 파일 sha256',
            '> 합성 전달 문단 첫 줄 — 판정문 그대로.' in rd and '> 둘째 문단.' in rd
            and (man.get('transfer_text') or {}).get('sha256') == __import__('hashlib').sha256(open(tfile, 'rb').read()).hexdigest(),
            man.get('transfer_text'))

        def tamper(path, old, new, count=1):
            s = open(path, encoding='utf-8').read()
            assert old in s, old
            open(path, 'w', encoding='utf-8', newline='').write(s.replace(old, new, count))
        mlp = os.path.join(out, f'lhs_mltable_{DATE}_v13.csv')
        bak = open(mlp, encoding='utf-8').read()
        tamper(mlp, 'INF_NOT_PERCOLATING', 'NOT_COMPUTED')
        pt = safe(lambda: LRB.check_v13(out, hdir))
        open(mlp, 'w', encoding='utf-8', newline='').write(bak)
        chk('V12g 변조 — ML 표 코드 한 칸 (INF_NOT_PERCOLATING → NOT_COMPUTED) → check_v13 문제', isinstance(pt, list) and pt, pt)
        sp = os.path.join(out, 'lhs_v13_refit_porosity_sigma_cn_summary.json')
        bak = open(sp, encoding='utf-8').read()
        js = json.loads(bak)
        js['fits']['free']['params']['alpha'] = js['fits']['free']['params']['alpha'] + 0.01
        open(sp, 'w', encoding='utf-8').write(json.dumps(js, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
        pt2 = safe(lambda: LRB.check_v13(out, hdir))
        open(sp, 'w', encoding='utf-8', newline='').write(bak)
        chk('V12h 변조 — 재적합 요약 지수 +0.01 → check_v13 문제 (다시 적합한 값과 다르다)', isinstance(pt2, list) and any('재적합' in p or 'refit' in p for p in pt2), pt2)
        os.remove(os.path.join(out, 'README.md'))
        pt3 = safe(lambda: LRB.check_v13(out, hdir))
        chk('V12i 파일 하나 지움 (README) → check_v13 문제 (빌드 manifest 의 파일 목록)', isinstance(pt3, list) and any('README' in p for p in pt3), pt3)
    else:
        for n in ('V12c', 'V12d', 'V12e', 'V12f', 'V12k', 'V12g', 'V12h', 'V12i'):
            chk(f'{n} (만들기 실패로 건너뜀)', False, rep)
    #  V12j — 인계표의 se_isolated_pct 를 (top 은 그대로) 틀리게 → 만들기 거부 (S1 항등식 · 배포 관문)
    hdir2 = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover_bad'),
                                              mutate=lambda ds, h, rows: rows[0].update(se_isolated_pct='99.0') if ds == 'lhs' else None))
    out2 = os.path.join(td, 'release_bad')
    if _orig_rr is not None:
        LRB.v13_reread_tau = lambda *a: []
        try:
            ok12j = refused(lambda: LRB.build_v13(out_dir=out2, handover_dir=hdir2, batch_root=broot, date=DATE, codex_verdict=verdict), 'se_isolated')
        finally:
            LRB.v13_reread_tau = _orig_rr
    else:
        ok12j = False
    chk('V12j 인계표 se_isolated_pct ≠ 100 − top_reachable_pct → 만들기 거부 · 산출 폴더 남지 않음', ok12j and not os.path.exists(out2))

# ═══ V13 실제 경로 거부 ══════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V13 실제 경로 거부')
with tempfile.TemporaryDirectory() as td:
    hdir = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    verdict = os.path.join(td, 'codex.md')
    open(verdict, 'w', encoding='utf-8').write('x\n')
    b_ok, b_leg = make_batch_root(os.path.join(td, 'b_ok'), 'g2'), make_batch_root(os.path.join(td, 'b_leg'), 'inferred_legacy')
    res = {}
    if _orig_rr is not None:
        LRB.v13_reread_tau = lambda *a: []
        try:
            res['verdict'] = refused(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o1'), handover_dir=hdir, batch_root=b_ok, date=DATE, codex_verdict=None),
                                     'Codex')
            res['legacy'] = refused(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o2'), handover_dir=hdir, batch_root=b_leg, date=DATE,
                                                          codex_verdict=verdict), 'g2')
            res['nobatch'] = refused(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o3'), handover_dir=hdir, batch_root=None, date=DATE,
                                                           codex_verdict=verdict), 'batch')
            LRB.v13_reread_tau = lambda *a: ['a: f_ion_hertz 인계표 0.1 ≠ 다시 읽음 0.2']
            res['reread'] = refused(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o4'), handover_dir=hdir, batch_root=b_ok, date=DATE,
                                                          codex_verdict=verdict), 'τ')
        finally:
            LRB.v13_reread_tau = _orig_rr
    chk('V13a Codex 판정문 없음 · manifest inferred_legacy · 배치 뿌리 없음 (τ 다시 읽기 불가) · τ 다시 읽기 문제 → 전부 거부', res == {
        'verdict': True, 'legacy': True, 'nobatch': True, 'reread': True}, res)
    chk('V13b 거부된 실행은 산출 폴더를 남기지 않는다', not any(os.path.exists(os.path.join(td, f'o{i}')) for i in range(1, 5)))

# ═══ V14 DRY RUN (커밋된 v1.2 = 세대 1) ══════════════════════════════════════════════════════════════════════════════════════════
print('V14 DRY RUN (커밋된 v1.2 원천 · 세대 1)')
with tempfile.TemporaryDirectory() as td:
    o_real = os.path.join(td, 'real')
    chk('V14a 세대 1 인계표로 dry-run 없이 → 거부 (세대 · v1.3 = g2) · 폴더 안 만듦',
        refused(lambda: LRB.build_v13(out_dir=o_real, handover_dir=V12, date=DATE, dry_run=False, batch_root=BATCH12,
                                      codex_verdict=os.path.join(ROOT, 'CLAUDE.md')), '') and not os.path.exists(o_real))
    o_dry = os.path.join(td, 'dry')
    rep = safe(lambda: LRB.build_v13(out_dir=o_dry, handover_dir=V12, date=DATE, dry_run=True))
    names = sorted(os.listdir(o_dry)) if os.path.isdir(o_dry) else []
    files = [n for n in names if os.path.isfile(os.path.join(o_dry, n))]
    chk('V14b dry-run — 만들기 성공 · 모든 파일 이름이 DRYRUN_ 로 시작 · origin · previews 도', isinstance(rep, dict) and files and all(n.startswith('DRYRUN_')
        for n in files) and all(n.startswith('DRYRUN_') for d in ('origin', 'previews') for n in (os.listdir(os.path.join(o_dry, d))
                                                                                                    if os.path.isdir(os.path.join(o_dry, d)) else ['x'])),
        rep if not isinstance(rep, dict) else files)
    if isinstance(rep, dict):
        rd = open(os.path.join(o_dry, 'DRYRUN_README.md'), encoding='utf-8').read()
        man = json.load(open(os.path.join(o_dry, 'DRYRUN_v13_build_manifest.json'), encoding='utf-8'))
        chk('V14c 표지 — README 첫 줄 "DRY RUN — not a release" · manifest dry_run true · 세대 inferred_legacy · 빠진 v1.3 열 목록 (se_isolated_pct · 세대 2 표기 · 압력)',
            rd.splitlines()[0].count('DRY RUN — not a release') == 1 and man.get('dry_run') is True
            and man.get('generation') == {'lhs': 'inferred_legacy', 'lhsx': 'inferred_legacy'}
            and all(c in (man.get('missing_columns') or {}).get('lhs', []) for c in ('se_isolated_pct', 'ion_net_electrode_hertz', 'press_reached')),
            (rd.splitlines()[:1], man.get('missing_columns')))
        pd = safe(lambda: LRB.check_v13(o_dry, V12, dry_run=True))
        chk('V14d check_v13 (dry-run) — 배포 ⊆ 인계표 · ML 표 · 빈칸 · 재적합 재현 = 문제 0', pd == [], pd)
        sm = json.load(open(os.path.join(o_dry, 'DRYRUN_lhs_v13_refit_porosity_sigma_cn_summary.json'), encoding='utf-8'))
        chk('V14e 재적합 (세대 1 · DRY RUN) — 관통 행 170 (130 중 106 + 64) · 비관통 24 제외 · 요약 dry_run true',
            sm.get('n_fit') == 170 and sm.get('excluded', {}).get('NOT_PERCOLATING') == 24 and sm.get('dry_run') is True, {k: sm.get(k) for k in ('n_fit', 'excluded')})
        mlh, mlr = _read_csv(os.path.join(o_dry, f'DRYRUN_lhs_mltable_{DATE}_v13.csv'))
        np_ = [r for r in mlr if r.get('ion_net_status_hertz') == 'NOT_PERCOLATING']
        chk('V14f ML 표 (실데이터 세대 1) — 비관통 24 = tau2 INF_NOT_PERCOLATING · 기하 τ NA_NOT_PERCOLATING · 분류 0 · mono 30 = NA_PHASE_ABSENT',
            len(np_) == 24 and all(r['tau2_ion_hertz__blank'] == 'INF_NOT_PERCOLATING' and r['tortuosity_SE_wall__blank'] == 'NA_NOT_PERCOLATING'
                                   and r['ion_percolates_hertz'] == '0' for r in np_)
            and sum(1 for r in mlr if r.get('d_am_p_um__blank') == 'NA_PHASE_ABSENT') == 15
            and sum(1 for r in mlr if r.get('d_am_s_um__blank') == 'NA_PHASE_ABSENT') == 15, len(np_))
    else:
        for n in ('V14c', 'V14d', 'V14e', 'V14f'):
            chk(f'{n} (dry-run 만들기 실패로 건너뜀)', False, rep)
    chk('V14g dry-run 산출을 docs/data 아래로 → 거부 (폴더 안 만듦)',
        refused(lambda: LRB.build_v13(out_dir=os.path.join(ROOT, 'docs', 'data', 'lhs_release_DRYRUN_test_v13'), handover_dir=V12, date=DATE,
                                      dry_run=True), 'docs/data')
        and not os.path.exists(os.path.join(ROOT, 'docs', 'data', 'lhs_release_DRYRUN_test_v13')))

# ═══ V15 CLI ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V15 CLI')
with tempfile.TemporaryDirectory() as td:
    o = os.path.join(td, 'cli_dry')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = safe(lambda: LRB.main(['--v13', '--dry-run', '--handover-dir', V12, '--out-dir', o, '--date', DATE]), 99)
    chk('V15a --v13 --dry-run → rc 0 · 산출', rc == 0 and os.path.isfile(os.path.join(o, 'DRYRUN_README.md')), (rc, buf.getvalue()[-400:]))
    buf2 = io.StringIO()
    with contextlib.redirect_stdout(buf2), contextlib.redirect_stderr(buf2):
        rc2 = safe(lambda: LRB.main(['--v13-check', '--dry-run', '--handover-dir', V12, '--release-dir', o]), 99)
    chk('V15b --v13-check --dry-run → rc 0', rc2 == 0, (rc2, buf2.getvalue()[-400:]))
    o3 = os.path.join(td, 'cli_real')
    buf3 = io.StringIO()
    with contextlib.redirect_stdout(buf3), contextlib.redirect_stderr(buf3):
        rc3 = safe(lambda: LRB.main(['--v13', '--handover-dir', V12, '--out-dir', o3, '--date', DATE]), 99)
    chk('V15c dry-run 없이 세대 1 원천 → rc ≠ 0 · 폴더 안 만듦', rc3 not in (0, 99) and not os.path.exists(o3), (rc3, buf3.getvalue()[-300:]))

# ═══ V16 발사 봉인 대조 (세대 2 등록 20261007_g2 §3 · §5) ═══════════════════════════════════════════════════════════════════════
#   실행기 manifest 의 code_hashes (봉인 29 — 워커 체크아웃에서 잰 값) ↔ v1.3 을 만드는 체크아웃 · handover_code_hashes (생성기 · 다시 읽기 도구) ·
#   ⓪b 다시 읽기 기록 (reread.json n_fail).  봉인 파일이 다르면 거부 (값과 무관한 변경 = --allow-seal-diff 명시 승인 · 기록) · 인계 도구 다름 = 경고 (등록 §3 ⚠).
print('V16 발사 봉인 대조 (code_hashes · handover_code_hashes · ⓪b 다시 읽기 기록)')


def refusal_msg(fn):
    """fn() 이 ReleaseError · FillRefusal 로 거부하면 그 메시지 · 다른 예외면 'OTHER …' · 통과하면 None."""
    try:
        fn()
    except Exception as e:                                                # noqa: BLE001
        bad = getattr(LRB, 'ReleaseError', RuntimeError)
        return str(e) if isinstance(e, (bad, LDD.FillRefusal)) else f'OTHER {type(e).__name__}: {e}'
    return None


with tempfile.TemporaryDirectory() as td:
    b0 = make_batch_root(os.path.join(td, 'b0'))
    d0 = safe(lambda: LRB.v13_seal_drift(os.path.join(b0, 'manifest.json')))
    chk('V16a 발사 기록 = 지금 파일 → 봉인 다름 0 · 인계 도구 다름 0 · 봉인 파일 수 · git HEAD (40 자리)',
        isinstance(d0, dict) and d0.get('sealed') == len(SEAL_FILES) and d0.get('sealed_changed') == [] and d0.get('handover_changed') == []
        and isinstance(d0.get('git_head'), str) and len(d0['git_head']) == 40, d0)
    b1 = make_batch_root(os.path.join(td, 'b1'), handover=False,
                         alter={'webapp/app.py': '0' * 64, 'scripts/nope_missing.py': 'ab' * 32, '/etc/hostname': 'cd' * 32, '../x.py': 'ef' * 32})
    d1 = safe(lambda: LRB.v13_seal_drift(os.path.join(b1, 'manifest.json')))
    chk('V16b 바뀐 봉인 파일 · 없는 파일 · 리포 밖 경로 (절대 · ..) = 다름 (정렬) · handover 기록 없으면 None (모름 — 같다고 하지 않는다)',
        isinstance(d1, dict) and d1.get('sealed_changed') == sorted(['webapp/app.py', 'scripts/nope_missing.py', '/etc/hostname', '../x.py'])
        and d1.get('handover') is None and d1.get('handover_changed') is None, d1)
    b2 = make_batch_root(os.path.join(td, 'b2'), code=False)
    chk('V16c manifest 에 code_hashes 가 없으면 → 거부 (무엇과 대조할지 모른다 · 194 실행기 manifest 아님)',
        refused(lambda: LRB.v13_seal_drift(os.path.join(b2, 'manifest.json')), 'code_hashes'))

    hd = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    ver = os.path.join(td, 'go.md')
    open(ver, 'w', encoding='utf-8').write('# GO (합성)\n')
    r16 = {}
    if _orig_rr is not None and not is_err(hd):
        LRB.v13_reread_tau = lambda *a: []
        try:
            b_app = make_batch_root(os.path.join(td, 'b_app'), alter={'webapp/app.py': '0' * 64})
            r16['app_msg'] = refusal_msg(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o_app'), handover_dir=hd, batch_root=b_app, date=DATE,
                                                               codex_verdict=ver))
            r16['app_nodir'] = not os.path.exists(os.path.join(td, 'o_app'))
            o_ok = os.path.join(td, 'o_app_allowed')
            r16['app_ok'] = safe(lambda: LRB.build_v13(out_dir=o_ok, handover_dir=hd, batch_root=b_app, date=DATE, codex_verdict=ver,
                                                       allow_seal_diff=['webapp/app.py']))
            if isinstance(r16['app_ok'], dict):
                r16['app_man'] = json.load(open(os.path.join(o_ok, 'v13_build_manifest.json'), encoding='utf-8'))
                r16['app_readme'] = open(os.path.join(o_ok, 'README.md'), encoding='utf-8').read()
                r16['app_check'] = safe(lambda: LRB.check_v13(o_ok, hd))
                #  변조 — 빌드 manifest 의 명시 승인 목록을 비우면 check_v13 이 잡는다 (다른 봉인 파일 ⊄ 승인)
                mp_ = os.path.join(o_ok, 'v13_build_manifest.json')
                bak = open(mp_, encoding='utf-8').read()
                mj = json.loads(bak)
                mj['code_identity']['allowed'] = []
                open(mp_, 'w', encoding='utf-8').write(json.dumps(mj, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
                r16['app_tamper'] = safe(lambda: LRB.check_v13(o_ok, hd))
                open(mp_, 'w', encoding='utf-8', newline='').write(bak)
            b_hd = make_batch_root(os.path.join(td, 'b_hd'), alter={'scripts/lhs_design_dataset.py': '1' * 64})
            o_hd = os.path.join(td, 'o_hd')
            r16['hd'] = safe(lambda: LRB.build_v13(out_dir=o_hd, handover_dir=hd, batch_root=b_hd, date=DATE, codex_verdict=ver))
            if isinstance(r16['hd'], dict):
                r16['hd_man'] = json.load(open(os.path.join(o_hd, 'v13_build_manifest.json'), encoding='utf-8'))
                r16['hd_readme'] = open(os.path.join(o_hd, 'README.md'), encoding='utf-8').read()
            b_rf = make_batch_root(os.path.join(td, 'b_rf'), reread=dict(RR_OK, n_fail=1))
            r16['rf_msg'] = refusal_msg(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o_rf'), handover_dir=hd, batch_root=b_rf, date=DATE,
                                                              codex_verdict=ver))
            b_rl = make_batch_root(os.path.join(td, 'b_rl'), reread=dict(RR_OK, expected_generation='inferred_legacy'))
            r16['rl_msg'] = refusal_msg(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o_rl'), handover_dir=hd, batch_root=b_rl, date=DATE,
                                                              codex_verdict=ver))
            b_r0 = make_batch_root(os.path.join(td, 'b_r0'), reread=dict(RR_OK))
            o_r0 = os.path.join(td, 'o_r0')
            r16['r0'] = safe(lambda: LRB.build_v13(out_dir=o_r0, handover_dir=hd, batch_root=b_r0, date=DATE, codex_verdict=ver))
            if isinstance(r16['r0'], dict):
                r16['r0_man'] = json.load(open(os.path.join(o_r0, 'v13_build_manifest.json'), encoding='utf-8'))
                #  check_v13 — 빌드 manifest 의 다시 읽기 기록을 일부 집합으로 바꾸면 문제 (G2RR2-02)
                _mp = os.path.join(o_r0, 'v13_build_manifest.json')
                _mm = json.load(open(_mp, encoding='utf-8'))
                _mm['batch_gate_files']['reread.json'].update(set_equal=False, read_n=193)
                json.dump(_mm, open(_mp, 'w', encoding='utf-8'))
                r16['r0_tamper'] = safe(lambda: LRB.check_v13(o_r0, hd))
            #  ★ 10-07 G2RR2-02 (Codex 세대 2 재검증 2 §3) — n_fail 0 · g2 여도 등록 집합 (생산 194) 을 다 읽은 기록이 아니면 거부
            r16['rs_msg'] = {}
            for tag, rec in (('일부 집합 (193 · 같음 False)', dict(RR_OK, read_n=193, set_equal=False, missing=[['lhs', 'lhs00_055']])),
                             ('시범 집합 pilot3', dict(RR_OK, expected_set='pilot3', expected_n=3, read_n=3)),
                             ('옛 도구 기록 (집합 필드 없음)', {k: v for k, v in RR_OK.items() if k in ('schema', 'expected_generation', 'n_fail')}),
                             ('0 케이스 (기대 0)', dict(RR_OK, expected_n=0, read_n=0))):
                b_rs = make_batch_root(os.path.join(td, f'b_rs{len(r16["rs_msg"])}'), reread=rec)
                o_rs = os.path.join(td, f'o_rs{len(r16["rs_msg"])}')
                r16['rs_msg'][tag] = (refusal_msg(lambda: LRB.build_v13(out_dir=o_rs, handover_dir=hd, batch_root=b_rs, date=DATE, codex_verdict=ver)),
                                      os.path.exists(o_rs))
            o_un = os.path.join(td, 'o_unused')
            r16['unused'] = safe(lambda: LRB.build_v13(out_dir=o_un, handover_dir=hd, batch_root=b0, date=DATE, codex_verdict=ver,
                                                       allow_seal_diff=['webapp/app.py']))
            #  승인 경로 철자 — './webapp/app.py' 도 같은 파일 (정규화) · 승인 기록은 manifest 키 철자로
            o_nm = os.path.join(td, 'o_norm')
            r16['norm'] = safe(lambda: LRB.build_v13(out_dir=o_nm, handover_dir=hd, batch_root=b_app, date=DATE, codex_verdict=ver,
                                                     allow_seal_diff=['./webapp/app.py']))
            if isinstance(r16['norm'], dict):
                r16['norm_ci'] = json.load(open(os.path.join(o_nm, 'v13_build_manifest.json'), encoding='utf-8')).get('code_identity')
            #  CLI — --allow-seal-diff 가 build_v13 까지 간다 (인계표 폴더를 주면 단계 A 없이)
            o_cli = os.path.join(td, 'o_cli')
            bufc = io.StringIO()
            with contextlib.redirect_stdout(bufc), contextlib.redirect_stderr(bufc):
                r16['cli_refuse'] = safe(lambda: LRB.main(['--v13', '--handover-dir', hd, '--batch-root', b_app, '--codex-verdict', ver,
                                                           '--out-dir', o_cli, '--date', DATE]), 99)
                r16['cli_ok'] = safe(lambda: LRB.main(['--v13', '--handover-dir', hd, '--batch-root', b_app, '--codex-verdict', ver,
                                                       '--out-dir', o_cli, '--date', DATE, '--allow-seal-diff', 'webapp/app.py']), 99)
            r16['cli_out'] = os.path.isfile(os.path.join(o_cli, 'README.md'))
        finally:
            LRB.v13_reread_tau = _orig_rr
    am = r16.get('app_msg') or ''
    chk('V16d 봉인 파일 (webapp/app.py) 이 발사 기록과 다르면 → 만들기 거부 (파일 이름 · --allow-seal-diff 안내) · 산출 폴더 없음',
        'webapp/app.py' in am and '--allow-seal-diff' in am and not am.startswith('OTHER') and r16.get('app_nodir') is True, am[:300])
    man16 = r16.get('app_man') or {}
    ci = man16.get('code_identity') or {}
    chk('V16e --allow-seal-diff webapp/app.py (명시 승인) → 만들기 성공 · 빌드 manifest code_identity (다른 파일 · 승인 · 봉인 수) · README 에 승인 기록 · check_v13 문제 0',
        isinstance(r16.get('app_ok'), dict) and ci.get('sealed_changed') == ['webapp/app.py'] and ci.get('allowed') == ['webapp/app.py']
        and ci.get('sealed') == len(SEAL_FILES) and '--allow-seal-diff' in (r16.get('app_readme') or '') and r16.get('app_check') == [],
        (r16.get('app_ok') if not isinstance(r16.get('app_ok'), dict) else ci, r16.get('app_check')))
    chk('V16f 변조 — 빌드 manifest 승인 목록을 비우면 (다른 봉인 파일 ⊄ 승인) → check_v13 문제',
        isinstance(r16.get('app_tamper'), list) and any('webapp/app.py' in p for p in r16['app_tamper']), r16.get('app_tamper'))
    hdm = (r16.get('hd_man') or {}).get('code_identity') or {}
    chk('V16g 인계 생성기 지문 ≠ 발사 기록 (handover_code_hashes) → 만들기는 한다 · 경고 (등록 §3 ⚠ — 커밋을 §9 에) · manifest · README 에 기록',
        isinstance(r16.get('hd'), dict) and hdm.get('handover_changed') == ['scripts/lhs_design_dataset.py']
        and any('handover_code_hashes' in w for w in r16['hd'].get('warnings', [])) and 'handover_code_hashes' in (r16.get('hd_readme') or ''),
        (r16.get('hd') if not isinstance(r16.get('hd'), dict) else hdm))
    rf, rl = r16.get('rf_msg') or '', r16.get('rl_msg') or ''
    chk('V16h ⓪b 다시 읽기 기록 (reread.json) 이 실패 (n_fail 1) · 다른 기대 세대 → 만들기 거부 (등록 §5-3)',
        'reread.json' in rf and not rf.startswith('OTHER') and 'reread.json' in rl and not rl.startswith('OTHER'), (rf[:200], rl[:200]))
    r0m = r16.get('r0_man') or {}
    gf = (r0m.get('batch_gate_files') or {})
    chk('V16i 다시 읽기 기록 통과 (n_fail 0 · g2 · 등록 집합 production194 전부 = 기대 194 · 읽음 194 · 같음) → 만들기 성공 · sha256 · n_fail · 집합 기록 · '
        '감사 기록 (seal_audit.json) 없음 = 경고',
        isinstance(r16.get('r0'), dict) and (gf.get('reread.json') or {}).get('n_fail') == 0
        and {k: (gf.get('reread.json') or {}).get(k) for k in ('expected_set', 'expected_n', 'read_n', 'set_equal')}
        == {'expected_set': 'production194', 'expected_n': 194, 'read_n': 194, 'set_equal': True}
        and (gf.get('reread.json') or {}).get('sha256') == __import__('hashlib').sha256(open(os.path.join(b_r0, 'reread.json'), 'rb').read()).hexdigest()
        and gf.get('seal_audit.json') is None and any('seal_audit.json' in w for w in r16['r0'].get('warnings', [])),
        (r16.get('r0') if not isinstance(r16.get('r0'), dict) else gf))
    rs = r16.get('rs_msg') or {}
    chk('V16n ⓪b 다시 읽기 기록이 n_fail 0 · g2 여도 등록 집합 production194 전부가 아니면 (일부 · pilot3 · 옛 도구 기록 · 0 케이스) → 만들기 거부 · 산출 폴더 없음 (G2RR2-02)',
        len(rs) == 4 and all(m is not None and not m.startswith('OTHER') and 'production194' in m and not made for m, made in rs.values()),
        {k: ((m or '')[:160], made) for k, (m, made) in rs.items()})
    chk('V16o check_v13 — 빌드 manifest 의 다시 읽기 기록을 일부 집합으로 바꾸면 문제 (G2RR2-02)',
        isinstance(r16.get('r0_tamper'), list) and any('G2RR2-02' in p_ for p_ in r16['r0_tamper']), r16.get('r0_tamper'))
    try:
        import run_network_194_parallel as _NP194                         # noqa: E402
        _reg = (getattr(_NP194, 'REGISTERED_ID_SETS', None) or {}).get(getattr(LRB, 'V13_REREAD_SET', None)) or {}
    except Exception as e:                                                # noqa: BLE001
        _reg = {'err': repr(e)}
    chk('V16p 빌드의 등록 집합 이름 · 크기 = 실행기 등록 (REGISTERED_ID_SETS · 다시 읽기 --expect-set 과 같은 표)',
        getattr(LRB, 'V13_REREAD_SET', None) == 'production194' and _reg.get('n') == getattr(LRB, 'V13_REREAD_N', None) == 194, _reg)
    un = r16.get('unused')
    chk('V16j 승인했지만 바뀌지 않은 파일 (--allow-seal-diff webapp/app.py · 봉인 같음) → 만들기는 한다 · 경고 (쓰이지 않은 승인)',
        isinstance(un, dict) and any('--allow-seal-diff' in w and 'webapp/app.py' in w for w in un.get('warnings', [])), un)
    nci = r16.get('norm_ci') or {}
    chk('V16m 승인 경로 철자 정규화 — "./webapp/app.py" = webapp/app.py (만들기 성공 · 승인 기록 = manifest 키 철자)',
        isinstance(r16.get('norm'), dict) and nci.get('allowed') == ['webapp/app.py'] and nci.get('sealed_changed') == ['webapp/app.py'],
        r16.get('norm') if not isinstance(r16.get('norm'), dict) else nci)
    chk('V16k CLI --allow-seal-diff — 없으면 rc ≠ 0 · 있으면 rc 0 · 산출',
        r16.get('cli_refuse') not in (0, 99, None) and r16.get('cli_ok') == 0 and r16.get('cli_out') is True,
        (r16.get('cli_refuse'), r16.get('cli_ok'), bufc.getvalue()[-300:] if 'bufc' in dir() else ''))

#  V16l — 단계 A 도 같은 관문 (생성기 실행 전에) · 승인하면 생성기를 부른다
_sp16 = []
with tempfile.TemporaryDirectory() as td:
    if hasattr(LRB, 'subprocess'):
        _orun = LRB.subprocess.run
        LRB.subprocess.run = lambda argv, **kw: (_sp16.append(argv) or _FakeRun()) if '--export-handover' in argv else _orun(argv, **kw)
        try:
            b_a = make_batch_root(os.path.join(td, 'b_a'), alter={'webapp/app.py': '0' * 64})
            m16l = refusal_msg(lambda: LRB.stage_handovers_v13(b_a, os.path.join(td, 'h1'), DATE, pressure_unverified=True))
            n_before = len(_sp16)
            r16l = safe(lambda: LRB.stage_handovers_v13(b_a, os.path.join(td, 'h2'), DATE, pressure_unverified=True, allow_seal_diff=['webapp/app.py']))
        finally:
            LRB.subprocess.run = _orun
    else:
        m16l, n_before, r16l = None, 0, ('ERR', 'no subprocess')
chk('V16l 단계 A — 봉인 다름이면 생성기를 부르기 전에 거부 · 명시 승인이면 생성기 두 번',
    m16l is not None and 'webapp/app.py' in m16l and n_before == 0 and not is_err(r16l) and len(_sp16) == 2, (m16l, n_before, r16l, len(_sp16)))

print(f'\n{_ok} PASS · {len(_fail)} FAIL')
if _fail:
    for n in _fail:
        print('  -', n)
    sys.exit(1)

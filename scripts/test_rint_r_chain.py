#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② R 런 사슬 `scripts/rint_r_chain.py` 시험 (시험 먼저 · 2026-10-20 · 가짜 러너 · GPU 없음).

정본 = 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3 (보정 사다리 · 식별성 · 확인 · 비단조 · 점 수 ·
허용폭 · origin) · §4 (모서리 넷 · 같은 P 일관 · origin 0.1 W) · §5 (구간 · 정보량 · 판정 · 표지) · §10 (명령 꼴 · 멈춤 목록) ·
설계 v1 §6 (수렴 증서) · §7 (세대 p3ca · 영수증 · LEAN 표).

가짜 러너 = 작은 파이썬 (bash 감쌈) — env (KITS · ARMS | ARM_LIST · CJUNC_RJ · CJUNC_PTFE_JLAW · SDCP_MOD_C · VOX · SIGMA_FIBRE_BULK · …) 를 읽어
**정해 둔 σ(R_j)** (거듭제곱 · 로지스틱) 로 진짜 꼴의 팔 JSON (매니페스트 · `ca_ext` 세 하위 블록 · 수렴 증서) · `run_receipt.json` 을 쓴다.
고장 주입 = 세계 파일 `faults` (rc 2 · 기각 기록 · 증서 실패 · 세대 · 변조 · LEAN · PTFE 셀 · sid 지문 · 잠 …).
★ Z3 (10-20) — 계약 자리 = **정본** (`RealContract` — `run_contract.ca_ext_record_ok` · `sr01_stamp_compare.check_arm`).  face_alpha + 접합
  조합 · 극한 런 (`rj_limit` 'inf' · 'zero') · 팔 고르기 (`ARM_LIST`) · off 격자 sid 지문 (`sid_off`) 이 들어와 가짜 인지 계약을 뺐다.
  가짜 러너는 `-S` (numpy 없음) 라 정본 producer 를 부를 수 없다 → 시험 프로세스가 정본 함수로 만든 **기록 틀** (protocol · 표지 · 진단 표 ·
  한정어 · 부피 기록) 을 세계 파일로 넘기고, 가짜 러너는 런마다 바뀌는 칸 (R_j · 원장 수 · 지문 · σ) 만 채운다 → 팔이 정본 검증기를 지난다.

  python3 scripts/test_rint_r_chain.py              # 전부
  python3 scripts/test_rint_r_chain.py --only L0,S1  # 이름 접두
⚠ PASS 는 사슬 논리의 증거이지 물리 검증이 아니다 (σ 는 가짜 함수다).
"""
import argparse
import contextlib
import copy
import hashlib
import io
import json
import math
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
REG_DOC = ROOT / 'docs' / 'reviews' / 'rint_carbon_additive_registration_R_draft_20261020.md'

SBE_KIT = 'kit_SBE_vgcf100'
DBE_KIT = 'kit_DBE_sdcp1um_vgcf100'
T_S = 1.63e-3                                            # 표적 S/cm (등록 R §0)

RR = None                                                # 사슬 모듈 (없으면 전부 FAIL — 시험 먼저)
TD = None
FX = {}                                                  # 고정물 (러너 · 킷 뿌리 · 계획 · 등록 사본)
SCEN = {}                                                # 시나리오 결과 (한 번 돌려 여러 검사가 읽는다)
CHECKS = []

# ═════════════════════════ 가짜 σ 모형 (가짜 러너와 시험이 같은 원문을 쓴다) ═════════════════════════
MODEL_SRC = r'''
def sigma_of(W, kit, rj, law, c, vox, bulk, unreg, yv):
    """arm 0 · 고장 · 범프 없는 σ (S/cm).  SBE = 모형 × 법칙 배수 × 변이 배수 · DBE = 그 값 × 2.87 × c 배수 × DBE 변이 배수."""
    import math as _m
    R = _m.inf if rj == 'inf' else float(rj)
    m = W['sbe']
    if R == _m.inf:
        s = m['floor']
    elif R == 0.0:
        s = m['ceiling']
    elif m['kind'] == 'power':
        s = m['s_ref'] * (R / m['R_ref']) ** (-m['e'])
    else:
        s = m['f'] + (m['C'] - m['f']) / (1.0 + (R / m['Rc']) ** m['beta'])
    s = s * W.get('law_factor', {}).get(law, 1.0)
    vk = []
    if bulk != 1e4:
        vk.append('FIBRE')
    if unreg != 'cut':
        vk.append('UNREG')
    if abs(vox - 0.15) > 1e-12:
        vk.append('GRID')
    if yv:
        vk.append('SVORDER')
    for k in vk:
        s = s * W.get('var_sbe', {}).get(k, 1.0)
    if rj in W.get('rj_sigma', {}):
        s = W['rj_sigma'][rj]
    s = s * W.get('rj_factor', {}).get(rj, 1.0)
    if 'DBE' in kit:
        s = s * W.get('dbe_scale', 2.87) * W.get('c_factor', {}).get(c, 1.0)
        for k in vk:
            s = s * W.get('var_dbe', {}).get(k, 1.0)
    return s
'''

FAKE_SRC = r'''
import hashlib, json, math, os, sys, time
E = os.environ
W = json.load(open(E['FAKE_WORLD'], encoding='utf-8'))
WD = W['dir']
T = W['tpl']                                   # 정본 기록 틀 (시험 프로세스가 정본 함수로 만들었다 · 이 프로세스는 -S = numpy 없음)
sys.path.insert(0, W['scripts'])
import run_contract as RC
exec(W['model_src'])


def jl(name, rec):
    with open(os.path.join(WD, name), 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, sort_keys=True) + '\n')


def cp_(o):
    return json.loads(json.dumps(o))


cp = os.path.join(WD, 'calls.txt')
n = (int(open(cp).read()) if os.path.exists(cp) else 0) + 1
open(cp, 'w').write(str(n))
SEEN = ('SIGMA_', 'SDCP_', 'PTFE_', 'CJUNC', 'STEP3_', 'P2_')
jl('env.jsonl', {k: E[k] for k in sorted(E) if k.startswith(SEEN) or k in (
    'VOX', 'BRIDGE_UM', 'ARMS', 'ARM_LIST', 'KITS', 'OUTDIR', 'LEAN', 'FIBRE_STAMP', 'MPM_PERIODIC_SIGMA', 'EXPECT_BACKEND',
    'EXPECT_PROTOCOL')})
kit, out = E['KITS'], E['OUTDIR']
#  팔 고르기 — 러너 꼴 (ARM_LIST = 정규 목록 · ARMS 와 동시 = 거부 · 0..N−1 접두 = 거부 · 팔 이름 = origin 번호 · OUTDIR 접미사 강제)
if 'ARM_LIST' in E:
    if 'ARMS' in E:
        print('[fake] ABORT — ARM_LIST 와 ARMS 를 같이 줬다')
        sys.exit(2)
    idx = [int(x) for x in E['ARM_LIST'].split(',')]
    if idx != sorted(set(idx)) or any(not 0 <= i <= 7 for i in idx) or idx == list(range(len(idx))):
        print('[fake] ABORT — ARM_LIST %r' % E['ARM_LIST'])
        sys.exit(2)
else:
    idx = list(range(int(E.get('ARMS', '8'))))
arms = len(idx)
if arms != 8 and ('_arm%d' % arms) not in out:
    out = out + '_arm%d' % arms
if 'ARM_LIST' in E and ('_arml' + '-'.join(map(str, idx))) not in out:
    out = out + '_arml' + '-'.join(map(str, idx))
rj, law, c = E['CJUNC_RJ'], E['CJUNC_PTFE_JLAW'], E.get('SDCP_MOD_C', '')
vox, bulk = float(E['VOX']), float(E['SIGMA_FIBRE_BULK'])
unreg, yv = E['CJUNC_UNREG_LAW'], E.get('SDCP_YIELD_VGCF', '') == '1'
rtol = float(E['STEP3_RTOL'])
backend = E.get('EXPECT_BACKEND', 'gpu')
ctx = {'kit': kit, 'rj': rj, 'law': law, 'c': c, 'arms': arms, 'n': n}


def hit(do):
    for f in W.get('faults', []):
        if f.get('do') != do:
            continue
        ok = True
        for k, v in (f.get('match') or {}).items():
            if k == 'kit_has':
                ok = ok and v in kit
            elif k == 'min_n':
                ok = ok and n >= v
            else:
                ok = ok and str(ctx.get(k)) == str(v)
        if ok:
            return f
    return None


if hit('rc2'):
    print('[fake] ABORT (fault rc2)')
    sys.exit(2)
if hit('sleep'):
    time.sleep(float(hit('sleep').get('s', 1.0)))
is_dbe = 'DBE' in kit
s0 = sigma_of(W, kit, rj, law, c, vox, bulk, unreg, yv)
R = math.inf if rj == 'inf' else float(rj)
if arms == 1 and not is_dbe and W.get('bump_seq') and R not in (0.0, math.inf) \
        and abs(2 * math.log10(R) - round(2 * math.log10(R))) > 1e-9:
    bp = os.path.join(WD, 'bumps.txt')
    k = int(open(bp).read()) if os.path.exists(bp) else 0
    if k < len(W['bump_seq']):
        s0 = s0 * W['bump_seq'][k]
    open(bp, 'w').write(str(k + 1))
if is_dbe and c == '1' and hit('dbe_c_inv'):
    s0 = s0 * 0.80
if not is_dbe and c == '1' and hit('sbe_c_dep'):
    s0 = s0 * (1.0 + 1e-12)
af = W.get('arm_factor_dbe' if is_dbe else 'arm_factor') or [1.0] * 8
os.makedirs(out, exist_ok=True)
H = float(f'{vox / 2:.6f}')
shifts = [(x, y, z) for x in (0.0, H) for y in (0.0, H) for z in (0.0, H)]
#  극한 런 — 러너 꼴 (`run_contract.runner_ca_ext`): 낱말 `inf` = 바닥 (R_j_ohm null + 표지 'inf') · ASCII 10 진 0 = 천장 (0.0 + 'zero')
lim = 'inf' if rj == 'inf' else ('zero' if float(rj) == 0.0 else None)
Rv = None if lim == 'inf' else float(rj)
s_min, tol_ff = float(E['CJUNC_S_MIN_UM']), float(E['CJUNC_TOL_FF_UM'])
if hit('receipt_rtol'):                        # 러너가 다른 rtol 로 돌았다 (영수증 · 매니페스트 · 증서 한 꼴 = 정본 계약은 지나고 사슬 계획 대조만 잡는다)
    rtol = rtol * 0.1
am_s = float(E['SIGMA_AM_S_OVERRIDE']) * (0.01 / 0.0041 if hit('bad_am_s') else 1.0)   # 러너가 다른 σ_AM_S 로 (영수증 = 매니페스트)
CERT = W['cert']
#  원장 수 (가짜 접합 원장 · 정본 검증기의 항등식을 채운다): instance 12 · PTFE 덮임 2 · DBE SDCP 근접 7
N_INST, N_COV = 12, 2
near = 7 if is_dbe else 0
cut = N_COV if law == 'P1' else 0
if lim == 'zero':                              # 천장 — 실현 · 미절단 instance 전부 축약 (R_j 몫 · c 몫 0)
    n_ctr, n_ctr_c, n_edge, n_inf = N_INST - cut, 0, 0, 0
else:
    n_ctr = near if c == '1' else 0            # c = 1 — 근접 instance 축약 (P1 이 먼저 끊은 것과 겹치지 않게 둔다)
    n_ctr_c = n_ctr
    rest = N_INST - n_ctr - cut
    n_edge, n_inf = (0, rest) if lim == 'inf' else (rest, 0)
COUNTS = {'n_instances': N_INST, 'n_edge': n_edge, 'n_contract': n_ctr, 'n_cut_p1': cut, 'n_unrealized': 0, 'n_none_inf': n_inf,
          'n_long': 1, 'n_sdcp_near': near, 'n_contracted_by_c': n_ctr_c, 'n_ptfe_cov': N_COV}


def hx(s):
    return hashlib.blake2b(s.encode(), digest_size=16).hexdigest()


def lean2(kind):
    return {'electronic_wetted': {'status': 'disabled', 'why': 'LEAN 2 (--no-collector)'},
            'electronic_bare': {'status': 'disabled', 'why': 'LEAN 2 (--no-collector)'},
            'ionic': {'status': 'disabled', 'why': 'LEAN 2 (--no-ion)'}}


#  ★ 3판 — 해 상태 (등록 R §5-0): 세계 `states` 규칙 = 조기 반환 영값 (VALID_ZERO_TOPOLOGY · 바닥) · 단락 (ELECTRODE_SHORT · J11 · 천장 /
#    c 1 축약) — payload `_step3_early` 꼴 (σ 0.0 · None · 사유 · 상태 증서 · 전자 not_solvable · 주 영수증 failed)
ST = None
for f in W.get('states', []):
    ok = True
    for k, v in (f.get('match') or {}).items():
        ok = ok and ((v in kit) if k == 'kit_has' else str(ctx.get(k)) == str(v))
    if ok:
        ST = f['state']
        break
REASON = {'zero': 'no_through_component', 'short': 'cjunc_electrode_short'}.get(ST)
SVCF = E.get('CJUNC_SV_CF', '') == '1'


def sv_record():
    """SV 반사실 기록 (증거 투영 꼴 · `ca_ext_svcf.sv_cf_record`) — 세계 `sv_cf` 규칙 (첫 일치) · 기본 = computed 1.2."""
    rule = {'status': 'computed', 'ratio': 1.2}
    for f in W.get('sv_cf', []):
        ok = True
        for k, v in (f.get('match') or {}).items():
            ok = ok and ((v in kit) if k == 'kit_has' else str(ctx.get(k)) == str(v))
        if ok:
            rule = f
            break
    st = rule['status']
    r_ = rule.get('ratio') if st == 'computed' else None
    rec = {'kind': rule.get('kind', 'counterfactual_cut_sv_faces'), 'requested': True, 'threshold': None, 'status': st, 'flag': None,
           'cg_info': (0 if st in ('computed', 'unconverged') else None), 'sv_counterfactual_ratio': r_,
           'ratio_limit': ('inf' if st == 'no_through_without_sv' else None), 'G_full_code': 2.5,
           'G_cut_code': (2.5 / r_ if r_ else (0.0 if st == 'no_through_without_sv' else None)), 'resid': (1e-13 if r_ else None),
           'n_sv_faces_cut': 4, 'conv_cert': None, 'backend_last_solve': None}
    #  ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 1저자 Q1 (다)) 괄호 칸 (투영 꼴) — 규칙 'n_unsplit' (기본 0) · 'status_hi' · 'ratio_hi' · 덩어리 0 =
    #    위 = 아래 (위 끝 기록 None) · 덩어리 > 0 = 위 끝 기록 (같은 꼴)
    nu = int(rule.get('n_unsplit', 0))
    sh = rule.get('status_hi', 'computed') if nu else st
    rh = (rule.get('ratio_hi') if sh == 'computed' else None) if nu else r_
    lh = 'inf' if sh == 'no_through_without_sv' else None
    rec.update(n_unsplit_bridging_components=nu, bracket_rule='lower_keep_upper_remove_fake_v1', status_hi=sh,
               sv_counterfactual_ratio_hi=rh, ratio_limit_hi=lh,
               upper=(None if not nu else {'status': sh, 'sv_counterfactual_ratio': rh, 'ratio_limit': lh,
                                          'cg_info': (0 if sh in ('computed', 'unconverged') else None),
                                          'G_cut_code': (2.5 / rh if rh else (0.0 if sh == 'no_through_without_sv' else None)),
                                          'resid': (1e-13 if rh else None), 'why': None, 'conv_cert': None, 'backend_last_solve': None,
                                          'n_edges_cut': 6, 'n_plate_couplings_cut': 0, 'n_cells_removed': 3}))
    return rec


def manifest(i, si):
    #  격자 지문 — 킷 · 래스터 (vox · SDCP 양보) · origin (팔 번호) 마다 (R_j · c · P 는 래스터를 안 바꾼다) · 소문자 hex 32
    sid = hx('sid|%s|%r|%s|%d' % (kit, vox, yv, i))
    if hit('sid_fp'):                          # 같은 킷 · 같은 래스터 · 같은 origin 인데 다른 격자 (두 블록 다 — 정본 계약은 지난다)
        sid = 'f' * 32
    regfp = hx('reg|' + sid)
    cjp = cp_(T['cj']['%s|%s|%s' % (law, unreg, lim or 'q')])
    if lim is None:
        cjp['R_j_ohm'] = Rv
    cjp['ptfe_stamp'] = E['PTFE_STAMP']
    rc_cj = dict(lean2('cj'), electronic_main={'status': 'applied', 'n_instances': N_INST, 'n_junction_edges': n_edge, 'solved': True,
                                               'fp_registry': regfp})
    if hit('lean_bad'):                        # 주 솔브 실패 영수증 (정본 계약 허용 · LEAN 2 표 = applied | absent_geometry 만)
        rc_cj['electronic_main'] = dict(rc_cj['electronic_main'], status='failed', solved=False, why='fake fault')
    if hit('lean_wetted'):                     # 집전체 솔브에 접합 적용 (LEAN 2 표 밖 — 정본 계약이 먼저 잡는다)
        rc_cj['electronic_wetted'] = {'status': 'applied'}
    #  ★ 3판 — 옛 `sv_dominant` 철회 (RCA-06) → `sv_local_dissipation` (진단) · 반사실 기록 = CJUNC_SV_CF 런만
    solve = {'solved': True, 'short': False, 'n_junction_edges': n_edge, 'n_contracted': n_ctr,
             'dissipation_share': {'junction': (0.4 if n_edge else 0.0), 'va_face': 0.2, 'sv_face': 0.05, 'sdcp_cell': 0.02},
             'sv_local_dissipation': {'kind': 'diagnostic_local_dissipation', 'sv_share': 0.07, 'vv_junction_share': 0.4,
                                      'meaning': 'fake'}}
    if SVCF:
        solve['sv_counterfactual'] = sv_record()
    if REASON:                                 # 조기 반환 해 — 주 솔브 없음 (payload `_step3_early` · `solve_receipt` 꼴)
        rc_cj['electronic_main'] = {'status': 'failed', 'why': REASON, 'n_instances': N_INST, 'n_junction_edges': 0, 'solved': False,
                                    'fp_registry': regfp}
        solve = {'solved': False, 'reason': REASON, 'short': ST == 'short', 'n_contracted': n_ctr, 'n_junction_edges': 0}
    fa_plan = hx('plan_e|' + sid)
    rc_fa = dict(lean2('fa'), electronic_main={'status': 'applied', 'n_rows_used': 5, 'n_cut_used': 1, 'n_isolated_by_cut': 0,
                                               'plate_cross_columns': 0, 'solved': True, 'fp_plan': fa_plan})
    if REASON:
        rc_fa['electronic_main'] = dict(rc_fa['electronic_main'], status='failed', why=REASON, n_rows_used=0, solved=False)
    fa_fp = {'caps': hx('caps|' + kit), 'plan_electronic': fa_plan, 'plan_ionic': None, 'sid_off': sid}
    if hit('sid_off_other'):                   # off 격자 지문 ≠ 접합 원장 지문 (같은 솔브인데) — 정본 계약이 잡는다
        fa_fp['sid_off'] = '0' * 32
    if hit('no_sid_off'):
        fa_fp.pop('sid_off')
    ca = {'schema': T['ca_schema'],
          'ptfe_face': {'protocol': cp_(T['fa']),
                        'evidence': {'capsules': {'n_paths': 2, 'n_pieces': 2, 'n_point_pieces': 0, 'n_segments': 6,
                                                  'volume_um3': T['fa_volume']['capsule_um3']},
                                     'volume': cp_(T['fa_volume']),
                                     'faces': {'electronic': {'n_rows': 5, 'n_cut_rows': 1, 'by_class': {}}, 'ionic': None},
                                     'receipts': rc_fa, 'off_grid_ptfe_point_cells': {'0': 3}, 'fp': fa_fp,
                                     'diagnostics': cp_(T['fa_diag']), 'label': T['fa_label'],
                                     'exempt_assumptions': cp_(T['fa_exempt'])}},
          'cjunc': {'protocol': cjp,
                    'evidence': {'counts': cp_(COUNTS), 'census': {'n_fibres': 4}, 'solve': solve, 'receipts': rc_cj,
                                 'fp': {'registry': regfp, 'sid': sid, 'plan_rows': hx('rows|' + regfp), 'centreline': hx('cl|' + kit),
                                        'membership': hx('mem|' + kit)},
                                 'rejections': [], 'sdcp_mod_c': (None if c == '' else float(c)), 'status': T['cj_status'],
                                 'qualifiers': cp_(T['cj_qual']), 'diagnostics': cp_(T['cj_diag']), 'label': T['cj_label']}}}
    if SVCF:                                   # ★ 3판 — 사슬이 켠 런만 (producer 문턱 = None · 문턱 = 사슬 계획)
        ca['cjunc']['evidence']['sv_counterfactual_request'] = {'threshold': None}
    req = ['cjunc']
    if c != '':
        ca['sdcp_mod'] = {'protocol': cp_(T['sd'][c]),
                          'evidence': {'n_sdcp_near': near, 'n_contracted_by_c': n_ctr_c, 's3_discriminating': near > 0,
                                       'label': T['sd_label']}}
        req = ['cjunc', 'sdcp_mod']
    man = {'schema_version': 3, 'vox_um': vox, 'bridge_um': float(E['BRIDGE_UM']), 'fibre_stamp': 'segment', 'sdcp_stamp': 'sphere',
           'sdcp_sphere_d_um': float(E['SDCP_SPHERE_D']), 'sdcp_yield_to_vgcf': yv, 'sdcp_bridge_um': 0.0, 'ptfe_block_um': 0.0,
           'ptfe_stamp': E['PTFE_STAMP'], 'ptfe_zero_dof': False,
           'sigma_vgcf_S_cm': float('%.6g' % (bulk * math.pi * 0.15 ** 2 / (4.0 * vox * vox))),
           'sigma_vgcf_bulk_S_cm': bulk, 'sigma_vgcf_rule': T['vgcf_rule'],
           'sigma_sdcp_S_cm': float(E['SIGMA_SDCP_OVERRIDE']), 'sigma_ptfe_S_cm': 0.0, 'sigma_ion_se_S_cm': 0.003,
           'sigma_ion_sdcp_S_cm': 0.001, 'sigma_am_s_S_cm': am_s, 'sigma_am_p_S_cm': 0.0041,
           'cam': 'ncm811', 'temp_c': None, 'periodic_xy': False, 'plate_rule': 'p2-occupied-surface-first',
           'sigma_superp_S_cm': 0.0, 'sigma_swcnt_S_cm': 0.0, 'swcnt_ion_block': False, 'dilate_z': 0.0, 'se_source': 'file:se.npy',
           'origin_shift_um': list(shifts[i]), 'ptfe_cells_observed': 0, 'field_requested': False,
           'component_plan': {'electronic': True, 'ionic': False, 'thermal': False, 'pore': False, 'collector': False},
           'components': ({'electronic': {'status': 'not_solvable', 'reason': REASON}} if REASON else
                          {'electronic': {'status': 'complete', 'backend': {'used': backend}}}),
           'backend': ({} if REASON else {'used': backend, 'rtol': rtol}), 'code_sha': 'fake0000', 'input_digest': 'in-' + kit,
           'ca_ext_requested': req, 'ca_ext': ca}
    if REASON:
        man['backend_last_solve'] = {}
    if hit('p2gen'):
        man.pop('ca_ext')
        man.pop('ca_ext_requested')
        man['ptfe_stamp'] = 'centerline'
    if hit('unknown_caext'):
        man.pop('ca_ext')
    if hit('bad_am_s_man'):                    # 매니페스트만 (영수증 ≠ 결과) — 정본 check_arm (receipt_match) 이 잡는다
        man['sigma_am_s_S_cm'] = 0.01
    if hit('ptfe_cells'):
        man['ptfe_cells_observed'] = 5
    man['physics_protocol_id'] = RC.physics_protocol_id(man)
    if hit('stale_id'):
        man['physics_protocol_id'] = 'p3ca-0000000000000000'
    if hit('tamper_caext'):                    # 쓴 뒤 원장 수 변조 (id 는 protocol 만 덮는다 → 정본 검증기의 항등식이 잡는다)
        man['ca_ext']['cjunc']['evidence']['counts']['n_edge'] -= 1
    return man


def cert(si, man):
    ok = not hit('certfail')
    return {'version': CERT['version'], 'rtol_used': rtol, 'rtol_max': CERT['rtol_max'], 'eps_I': CERT['eps_I'],
            'resolve_rtol': max(rtol * 1e-2, 1e-14), 'resolve_rtol_floor': 1e-14, 'resolve_tol': CERT['resolve_tol'],
            'info': 0, 'resid': 3e-13, 'I_bot': 1.0, 'I_top': 1.0, 'imbalance': (2e-7 if ok else 3e-4), 'sigma': si,
            'sigma_resolve': si, 'dsigma_rel': 1e-9, 'resolve_info': 0, 'pass_a': True, 'pass_b': ok, 'pass_c': True, 'ok': ok,
            'iters': 321, 'resolve_iters': 17,
            #  ★ 10-21 증서 v2 — 상태 · ⓓ (구간 [1, 1] ∋ 게시 판 전류 1 · scale = σ)
            'status': CERT['status'], 'pass_d': True, 'target_tol': CERT['target_tol'], 'target_version': CERT['target_version'],
            'target_fp': CERT['target_fp'], 'target_ledger_ok': True, 'target_topology': 'through',
            #  ★ 4판 (Q2-2 · §3-2b ③″) — 세계 'cert_e' = 그 팔 증서의 보장 오차 (구간 [1 − e, 1] ∋ 게시 판 전류 1 · 폭 = 오차 = e ≤ τ)
            'target_lo': 1.0 - float(W.get('cert_e', 0.0)), 'target_hi': 1.0, 'scale': si,
            #  ★ 10-21 (사전 리뷰 PRE-impl-07 · B 픽스처 패치) — 증서 ↔ 런 결합 칸 = 그 팔 매니페스트의 정본 지문 (접합 원장 sid · registry ·
            #    plan_rows · face_alpha 전자 계획) · σ 표 지문 = 킷마다 (가짜)
            **_bind(man)}


def _bind(man):
    ca = man.get('ca_ext') or {}
    cjf = ((ca.get('cjunc') or {}).get('evidence') or {}).get('fp') or {}
    faf = ((ca.get('ptfe_face') or {}).get('evidence') or {}).get('fp') or {}
    return {'bind_version': CERT['bind_version'], 'fp_sid': cjf.get('sid', faf.get('sid_off')), 'fp_sig': hx('sig|' + kit),
            'fp_face_plan': faf.get('plan_electronic'), 'fp_cjunc_registry': cjf.get('registry'),
            'fp_cjunc_rows': cjf.get('plan_rows')}


def early_cert(i, man):
    """조기 반환 해의 상태 증서 (정본 `step3_conv_cert.early_record` 로 만든 틀) — ★ 10-21 (PRE-impl-07 병합) 결합 칸 = 그 팔 매니페스트의
    정본 지문 (솔버 `_cert_bind_kw` 꼴 · 양의 해 증서와 같은 칸)."""
    ce = cp_(T['early_' + ST])
    ce.update(_bind(man))
    return ce


tag = rj.replace('.', 'p').replace('+', '').replace('-', 'm')
for i in idx:
    si = s0 * af[i]
    man_i = manifest(i, si)
    if REASON:
        st = {'sigma_e_eff_S_cm': (0.0 if ST == 'zero' else None), 'reason': REASON, 'vox_um': vox, 'manifest': man_i,
              'conv_cert': early_cert(i, man_i)}
    else:
        st = {'sigma_e_eff_S_cm': si, 'cg_info': 0, 'unconverged': False, 'cg_resid': 3e-13, 'n_dof': 1234, 'vox_um': vox,
              'status': 'complete', 'manifest': man_i, 'conv_cert': cert(si, man_i), 'cg_iters': 321}
    json.dump({'mpm_metrics': {'step3': st}}, open(os.path.join(out, 'p2_%s_sph_fa_cj%s_c%s_a%d.json' % (kit[4:], tag, c, i)), 'w'))
    jl('ledger.jsonl', {'sigma': (si if not REASON else 0.0)})
cj_req = {'R_j_ohm': Rv, 'len_law': E['CJUNC_LEN_LAW'], 'unreg_law': unreg, 's_min_um': s_min, 'tol_ff_um': tol_ff, 'ptfe_jlaw': law}
if lim:
    cj_req['rj_limit'] = lim
req = {'cjunc': cj_req}
if c != '':
    req['sdcp_mod'] = {'c': float(c)}
rec = {'vox_um': vox, 'bridge_um': float(E['BRIDGE_UM']), 'fibre_stamp': 'segment', 'sdcp_stamp': 'sphere',
       'sdcp_sphere_d_um': float(E['SDCP_SPHERE_D']), 'sdcp_yield_to_vgcf': yv, 'ptfe_stamp': E['PTFE_STAMP'], 'periodic_xy': False,
       'arms': arms, 'expect_backend': backend, 'origins': [list(o) for o in RC.expected_origins_for(vox)],
       'sigma_am_s_S_cm': am_s, 'sigma_sdcp_S_cm': float(E['SIGMA_SDCP_OVERRIDE']),
       'sigma_vgcf_bulk_S_cm': bulk, 'sigma_vgcf_rule': T['vgcf_rule'],
       'ca_ext_request': req, 'step3_rtol': rtol, 'code_sha': 'fake0000'}
if 'ARM_LIST' in E:
    rec['arm_list'] = idx
if SVCF:
    rec['sv_counterfactual'] = True
json.dump(rec, open(os.path.join(out, 'run_receipt.json'), 'w'), sort_keys=True)
if hit('rejected'):
    open(os.path.join(out, '.rejected_20261020T000000Z'), 'w').write('reason=seal_broken\n')
if hit('two_json'):
    json.dump({'mpm_metrics': {'step3': st}}, open(os.path.join(out, 'p2_%s_dup_a0.json' % kit[4:]), 'w'))
print('[fake] STEP3 sigma_e_eff = [sealed]')
'''

# ═════════════════════════ 세계 (σ 모형 · 고장) ═════════════════════════
PW_SBE = {'kind': 'power', 's_ref': 2.0e-3, 'R_ref': 1e6, 'e': 0.25, 'floor': 0.3e-3, 'ceiling': 30e-3}
ARM_SMALL = [1.0, 1.0004, 0.9997, 1.0002, 0.9999, 1.0001, 0.9998, 1.0003]
#: ★ 3판 — SBE origin 팔 1 · 2 = arm 0 그대로 (끝 origin 규칙 Q-E 가 기본 세계에서 끝을 밀지 않게 · 밀기 = L21 · U10) · 나머지 팔 = 작은 흔들림
ARM_SBE = [1.0, 1.0, 1.0, 1.0002, 0.9999, 1.0001, 0.9998, 1.0003]
PW = {'sbe': PW_SBE, 'law_factor': {'P0': 1.0, 'P1': 0.95}, 'c_factor': {'0': 0.92, '1': 1.08}, 'dbe_scale': 2.87,
      'arm_factor': ARM_SBE, 'arm_factor_dbe': ARM_SMALL,
      'var_sbe': {'FIBRE': 0.9, 'UNREG': 1.05, 'GRID': 0.97}, 'var_dbe': {'SVORDER': 1.01}}


def record_templates():
    """정본 기록 틀 — 가짜 러너 (-S · numpy 없음) 가 채울 protocol · 표지 · 진단 표 · 한정어 · 부피 기록을 **정본 함수로** 만든다
    (한 번 · 계획의 s_min · tol_ff 로).  접합 protocol = 법칙 × 미등록 면 법칙 × {정량 · 바닥 · 천장} (정량은 R_j 만 가짜가 바꾼다)."""
    if 'tpl' not in FX:
        import ca_ext_cjunc as CW
        import carbon_junction as CJ
        import ptfe_face_alpha as FA
        import run_contract as RCm
        import step3_conv_cert as CCm
        import step3_sigma as S3
        p = FX['plan_obj']
        cj = {}
        for law in CJ.PTFE_JLAWS:
            for unreg in CJ.UNREG_LAWS:
                for lim in (None,) + tuple(CW.RJ_LIMITS):
                    R = {None: 1.0, 'inf': None, 'zero': 0.0}[lim]
                    cj[f'{law}|{unreg}|{lim or "q"}'] = CW.cjunc_protocol_record(
                        R_j_ohm=R, len_law=p['len_law'], unreg_law=unreg, s_min_um=float(p['s_min_um']),
                        tol_ff_um=float(p['tol_ff_um']), ptfe_jlaw=law, ptfe_stamp='face_alpha', rj_limit=lim)
        FX['tpl'] = {'ca_schema': RCm.CA_EXT_SCHEMA, 'cj': cj,
                     'sd': {c: CW.sdcp_mod_protocol_record(c=float(c), tol_sj_um=float(p['tol_ff_um'])) for c in ('0', '1')},
                     'cj_status': CJ.CJUNC_STATUS, 'cj_qual': list(CJ.CJUNC_QUALIFIERS), 'cj_diag': dict(CW.DIAGNOSTICS_V0),
                     'cj_label': CW.LABEL_CJUNC, 'sd_label': CW.LABEL_SDCP,
                     'fa': FA.protocol_record(('electronic', 'ionic'), 'rope'), 'fa_diag': dict(FA.DIAGNOSTICS_V0), 'fa_label': FA.LABEL,
                     'fa_volume': FA.volume_record(0.05, 0.06), 'vgcf_rule': S3.VGCF_SIGMA_RULE,
                     'fa_exempt': dict(FA.EXEMPT_ASSUMPTIONS),
                     #  ★ 3판 — 조기 반환 해의 상태 증서 틀 (정본 함수 · 가짜 러너가 격자 지문만 채운다)
                     **{f'early_{k}': CCm.early_record({'sigma_eff': 0.0, 'n_dof': 1234, 'reason': rs}, zero_graph='cjunc_assembled',
                                                       fp_sid='0' * 32, fp_sig='0' * 32)
                        for k, rs in (('zero', 'no_through_component'), ('short', 'cjunc_electrode_short'))}}
    return FX['tpl']


def world(name, base=None, **kw):
    """세계 파일 → 경로 (이름마다 새 폴더 · 호출 수 · 장부 · env 기록이 그 폴더에 쌓인다)."""
    import step3_conv_cert as CC                           # 증서 봉인 상수 = 정본 (시험 프로세스에서 한 번)
    d = Path(TD) / 'worlds' / name
    assert not d.exists(), f'세계 {name} 두 번'
    d.mkdir(parents=True)
    W = copy.deepcopy(base if base is not None else PW)
    W.update(copy.deepcopy(kw))
    W.update({'dir': str(d), 'scripts': str(SCRIPTS), 'model_src': MODEL_SRC, 'tpl': record_templates(),
              'cert': {'version': CC.CERT_VERSION, 'rtol_max': CC.CERT_RTOL_MAX, 'eps_I': CC.CERT_EPS_I,
                       'resolve_tol': CC.CERT_RESOLVE_TOL, 'target_tol': CC.CERT_TARGET_TOL,
                       'target_version': CC.TARGET_VERSION, 'target_fp': CC.TARGET_FP_RULE, 'status': CC.STATUS_POSITIVE,
                       'bind_version': CC.BIND_VERSION}})
    (d / 'world.json').write_text(json.dumps(W), encoding='utf-8')
    return str(d / 'world.json')


def wdata(wpath):
    return json.loads(Path(wpath).read_text(encoding='utf-8'))


_NS = {}
exec(MODEL_SRC, _NS)
sigma_of = _NS['sigma_of']


def sig_main(W, kit, rj, law, c='0', vox=0.15, bulk=1e4, unreg='cut', yv=False):
    return sigma_of(W, kit, rj, law, c, vox, bulk, unreg, yv)


def n_calls(wpath):
    p = Path(wpath).parent / 'calls.txt'
    return int(p.read_text()) if p.exists() else 0


def env_log(wpath):
    p = Path(wpath).parent / 'env.jsonl'
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()] if p.exists() else []


def ledger(wpath):
    p = Path(wpath).parent / 'ledger.jsonl'
    return [json.loads(x)['sigma'] for x in p.read_text(encoding='utf-8').splitlines()] if p.exists() else []


# ═════════════════════════ 고정물 · 단계 호출 ═════════════════════════
def fixtures():
    FX['runner'] = Path(TD) / 'runner.sh'
    (Path(TD) / 'fake.py').write_text(FAKE_SRC, encoding='utf-8')
    FX['runner'].write_text(f'#!/bin/bash\nexec {sys.executable} -I -S {Path(TD) / "fake.py"} "$@"\n', encoding='utf-8')
    FX['root'] = Path(TD) / 'root'
    for k in (SBE_KIT, DBE_KIT):
        (FX['root'] / k).mkdir(parents=True)
    #  ★ 3판 — R 런 계획 v2 (결과 전 등록 숫자 넷 = 시험 값 · 등록 숫자가 아니다) · S0 단계 1 계획 (정본 함수 make_plan · 정준 바이트)
    plan = {'schema': 'rint-r-plan-v2', 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': 0.6, 'tol_ff_um': 0.05,
            'step3_rtol': 1e-12, 'p2_extra': '--step3-maxiter 60000', 'max_ladder_points': 16, 'calib_rj_ratio_max': 'none',
            'sv_cf_threshold': 2.0, 'sv_cf_scope': 'R_j0'}
    FX['plan_obj'] = plan
    import ca_s0_census as S0m
    s0p, s0b, s0sha = S0m.make_plan(0.05, S0m.R_F_UM, S0m.GAP_TOL_PRODUCTION, {'fixture': 'test_rint_r_chain', 'kit': SBE_KIT})
    FX['s0_obj'], FX['s0_sha'] = s0p, s0sha
    FX['s0'] = Path(TD) / 's0_plan.json'
    FX['s0'].write_bytes(s0b)
    text = REG_DOC.read_text(encoding='utf-8')
    FX['reg_text'] = text

    def reg_with(cell, name, s0cell=f'`{s0sha}`'):
        out = []
        for ln in text.splitlines():
            if ln.startswith('| 계획 해시 |') or ln.startswith('| S0 계획 해시 |'):
                cells = ln.split('|')
                cells[-2] = f' {cell if ln.startswith("| 계획 해시 |") else s0cell} '
                ln = '|'.join(cells)
            out.append(ln)
        p = Path(TD) / name
        p.write_text('\n'.join(out) + '\n', encoding='utf-8')
        return p
    FX['reg_with'] = reg_with
    FX['plan'], FX['plan_sha'], FX['reg_ok'] = plan_set('plan', reg_name='reg_ok.md')
    sha = FX['plan_sha']
    FX['reg_other'] = reg_with('0' * 64, 'reg_other.md')
    FX['reg_unreg'] = reg_with('⬜', 'reg_unreg.md')
    FX['reg_s0_unreg'] = reg_with(f'`{sha}`', 'reg_s0_unreg.md', s0cell='⬜')
    FX['reg_s0_other'] = reg_with(f'`{sha}`', 'reg_s0_other.md', s0cell='`' + '1' * 64 + '`')
    #  ★ PF2 D (10-22 · PRE2-design-02 · 08) — S0 단계 1 보고 (가짜 · census · registry 일곱 파일 지문 = 이 트리 · dirty False) ·
    #    사슬의 git 신원 = 진짜 HEAD · **dirty False** (시험을 고쳐진 작업 트리에서 돌려도 단계가 dirty 로 멈추지 않게 — dirty 판정 자체는 D06 이
    #    임시 git 저장소로 · 단계별 대조는 D01–D05 가 신원을 바꿔 본다) · 파일 지문 = 실제 파일 (사슬 함수 그대로)
    FX['s1'] = s0_report(1, 's1_main')
    FX['git_identity_real'] = RR.git_identity
    RR.git_identity = lambda path, _g=FX['git_identity_real']: dict(_g(path), dirty=False)


def plan_set(name, reg_name=None, **over):
    """계획 한 벌 (기본 계획 + 바꾼 칸) → (계획 경로, sha256, 그 해시를 채운 등록 사본) — 계획마다 등록 사본 하나 (해시가 다르다)."""
    plan = dict(FX['plan_obj'], **over)
    p = Path(TD) / f'{name}.json'
    p.write_text(json.dumps(plan, indent=1, sort_keys=True), encoding='utf-8')
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    return p, sha, FX['reg_with'](f'`{sha}`', reg_name or f'reg_{name}.md')


# ═════════════════════════ ★ PF2 B (10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 1저자 Q2 권고대로) S0 단계 2 보고 ═════════════════════════
#   순서 (등록 R §11 · Q2): S0 단계 1 → ⑥ 숫자 탐침 (SBE · σ 봉인) → 세 숫자 → 계획 하나 봉인 (개정 커밋) → S0 단계 2 (DBE) → R 런.
#   단계 2 보고 (`ca_s0_census` · `s0_stage2_<DBE 킷>.json`) 의 `plan.r_plan.sha256` = 그 인자 커밋이 봉인한 R 계획 · `plan.sha256` = S0 계획.
#   사슬 (사다리 · 예측 · 판정) 이 지금 계획과 **정확히** 대조한다 — 다르면 멈춘다 (탐침 E: 단계 2 뒤 계획 B 를 다시 등록해도 옛 사슬은 CALIBRATED).
S0_STAGE2_OPT = '--s0-stage2-report'


def chain_has(opt):
    """사슬 CLI 에 그 인자가 있나 (고치기 전 판 = 없음 → 시험이 그 인자를 빼고 부른다: 반례가 그 판에서 **돈다** = 옳은 이유의 실패)."""
    main = getattr(RR, 'main', None)
    return callable(main) and opt in getattr(getattr(main, '__code__', None), 'co_consts', ())


def s0_report(stage, name, plan_sha=None, s0_sha=None, kit=None, mutate=None, raw=None):
    """S0 단계 보고 (가짜) → 경로 — 꼴 = `ca_s0_census.census_kit` 보고의 판정 칸 (schema · stage · kit · plan · code).  단계 2 의 plan =
    {sha256 (S0 계획) · source 'commit:<sha>' · r_plan {path · sha256 (R 계획) · s_min · tol_ff · 법칙 · rtol}} (`verify_plan_commit` 의 결합 기록 꼴).
    mutate = 손댄 dict · raw = 그대로 쓸 바이트 (깨진 JSON 반례)."""
    import ca_s0_census as S0m
    p = Path(TD) / f's0rep_{name}.json'
    if raw is not None:
        p.write_bytes(raw)
        return p
    pl = {'sha256': s0_sha or FX['s0_sha'], 'source': 'stage1_computed'}
    if stage == 2:
        pl = {'sha256': s0_sha or FX['s0_sha'], 'source': 'commit:' + 'a' * 40,
              'r_plan': {'path': 'docs/data/rint2_s0_sbe_x/rint_r_plan.json', 'sha256': plan_sha or FX['plan_sha'],
                         's_min_um': 0.6, 'tol_ff_um': 0.05, 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 'step3_rtol': 1e-12,
                         'checked': 'fixture'}}
    rep = {'schema': S0m.SCHEMA, 'stage': stage, 'tool': S0m.TOOL_VERSION,
           'kit': {'name': kit or (SBE_KIT if stage == 1 else DBE_KIT)}, 'plan': pl,
           'code': {'git_head': 'b' * 40, 'git_dirty': False,
                    'file_digests': [{'file': nm, 'sha256': hashlib.sha256((SCRIPTS / nm).read_bytes()).hexdigest()}
                                     for nm in S0_SAME7]}}
    if mutate is not None:
        mutate(rep)
    p.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf-8')
    return p


#: 등록 R §2-1b — S0 단계 1 · 2 · R 런의 census · registry 일곱 파일 (시험 쪽 목록 · 사슬 · S0 상수와 시험 D 가 대조)
S0_SAME7 = ('ca_s0_census.py', 'carbon_junction.py', 'ptfe_face_alpha.py', 'step3_sigma.py', 'mpm_webapp_payload.py',
            'fibre_segment_raster.py', 'sr01_stamp_compare.py')


def s0_stage2_for(plan_path):
    """그 계획을 봉인한 단계 2 보고 (계획마다 하나 · 캐시) → 경로."""
    sha = hashlib.sha256(Path(plan_path).read_bytes()).hexdigest()
    key = ('s0_stage2', sha)
    if key not in FX:
        FX[key] = s0_report(2, f's2_{sha[:16]}', plan_sha=sha)
    return FX[key]


S0_STAGE1_OPT = '--s0-stage1-report'          # ★ PF2 D (10-22 · PRE2-design-08) — census · registry 지문 대조 (등록 R §2-1b)


def s0_args(plan_path=None, s2=None, s1=None):
    """사다리 인자에 S0 단계 2 · 1 보고 (사슬이 그 인자를 알 때만)."""
    out = []
    if chain_has(S0_STAGE2_OPT):
        out += [S0_STAGE2_OPT, s2 or s0_stage2_for(plan_path or FX['plan'])]
    if chain_has(S0_STAGE1_OPT):
        out += [S0_STAGE1_OPT, s1 or FX['s1']]
    return out


@contextlib.contextmanager
def envset(**kv):
    old = {k: os.environ.get(k) for k in kv}
    try:
        for k, v in kv.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = str(v)
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def call(argv, wpath=None, env=None, contract=None):
    """사슬 main 을 프로세스 안에서 → (rc, 화면).  SystemExit 는 rc 로.  ★ Z3 — 계약 = 정본 (`RealContract` · main 기본값) ·
    `contract` 는 사슬 **자신의** 검사층만 보려는 시험 (X09) 에서만 넣는다."""
    kv = dict(env or {})
    kv['FAKE_WORLD'] = wpath
    buf = io.StringIO()
    with envset(**kv), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            rc = RR.main([str(a) for a in argv], contract=contract)
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 2
    return rc, buf.getvalue()


def pass_contract():
    """통과 계약 — 정본 두 검사를 비켜 사슬 자신의 대조 (sid_off · 매니페스트 · LEAN · PTFE 셀) 만 남긴다 (X09 · 변이 대조용)."""
    class PassContract(RR.RealContract):
        def arm_problem(self, path, receipt):
            return None

        def ca_ext_record(self, man):
            return True, None
    return PassContract()


def ladder(tag, wpath, law='P0', variant=None, extra=(), reg=None, max_hours='2', env=None, prefill=False, contract=None,
           plan=None, s0=None, after=None, s2=None, s1=None):
    out = Path(TD) / 'runs' / tag
    if prefill:
        out.mkdir(parents=True)
        (out / 'old.txt').write_text('x')
    argv = ['--stage', 'ladder', '--law', law, '--target', '1.63', '--runner', FX['runner'], '--root', FX['root'],
            '--plan', plan or FX['plan'], '--s0-plan', s0 or FX['s0'], '--registration', reg or FX['reg_ok'], '--max-hours', max_hours,
            '--out', out] + s0_args(plan or FX['plan'], s2, s1)
    if variant:
        argv += ['--variant', variant]
        argv += ['--after-main', after if after is not None else s_main_predict()['out']]   # ★ Q-F — 감도 = 주 판정 단계 뒤
    rc, so = call(argv + list(extra), wpath, env, contract=contract)
    sp = out / 'ladder_summary.json'
    return {'rc': rc, 'out': out, 'so': so, 'sum': json.loads(sp.read_text(encoding='utf-8')) if sp.exists() else None,
            'world': wpath}


def predict(tag, wpath, ladders, variant=None, extra=(), reg=None, max_hours='2', after=None):
    out = Path(TD) / 'runs' / tag
    argv = ['--stage', 'predict', '--ladders', *ladders, '--kit', DBE_KIT, '--runner', FX['runner'], '--root', FX['root'],
            '--registration', reg or FX['reg_ok'], '--max-hours', max_hours, '--out', out]
    if variant:
        argv += ['--variant', variant, '--after-main', after if after is not None else s_main_predict()['out']]
    rc, so = call(argv + list(extra), wpath)
    sp = out / 'predict_summary.json'
    return {'rc': rc, 'out': out, 'so': so, 'sum': json.loads(sp.read_text(encoding='utf-8')) if sp.exists() else None,
            'world': wpath}


def verdict(tag, dirs, extra=(), reg=None):
    out = Path(TD) / 'runs' / tag
    rc, so = call(['--stage', 'verdict', '--runs', *dirs, '--registration', reg or FX['reg_ok'], '--out', out] + list(extra))
    vp, rp = out / 'verdict.json', out / 'verdict_results.json'
    return {'rc': rc, 'out': out, 'so': so, 'v': json.loads(vp.read_text(encoding='utf-8')) if vp.exists() else None,
            'r': json.loads(rp.read_text(encoding='utf-8')) if rp.exists() else None}


def scen(key, fn):
    if key not in SCEN:
        SCEN[key] = fn()
    return SCEN[key]


def stop_code(res):
    s = (res.get('sum') or res.get('v') or {}).get('stop') or {}
    return s.get('code')


def lad(res):
    return (res.get('sum') or {}).get('ladder') or {}


def roles(res):
    return [r['role'] for r in (res.get('sum') or {}).get('runs', [])]


# ═════════════════════════ 시나리오 ═════════════════════════
def s_main(law):
    return scen(f'main_{law}', lambda: ladder(f'main_{law}', world(f'main_{law}'), law=law))


def s_main_predict():
    return scen('main_pred', lambda: predict('main_pred', world('main_pred'), [s_main('P0')['out'], s_main('P1')['out']]))


def s_variant_set(V, base=None, tag=None):
    """감도 변이 V — 변이 사다리 둘 (SVORDER 는 주 사다리) + 변이 예측."""
    tag = tag or V
    def go():
        b = base if base is not None else PW
        if V == 'SVORDER':
            lads = [s_main('P0')['out'], s_main('P1')['out']]
            out = []
        else:
            out = [ladder(f'var_{tag}_{law}', world(f'var_{tag}_{law}', b), law=law, variant=V) for law in ('P0', 'P1')]
            lads = [o['out'] for o in out]
        pr = predict(f'var_{tag}_pred', world(f'var_{tag}_pred', b), lads, variant=V)
        return {'ladders': out, 'pred': pr, 'dirs': [o['out'] for o in out] + [pr['out']]}
    return scen(f'var_{tag}', go)


def main_dirs():
    return [s_main('P0')['out'], s_main('P1')['out'], s_main_predict()['out']]


def s_verdict_main():
    return scen('ver_main', lambda: verdict('ver_main', main_dirs()))


def s_verdict_full():
    def go():
        dirs = list(main_dirs())
        for V in ('FIBRE', 'UNREG', 'GRID', 'SVORDER'):
            dirs += s_variant_set(V)['dirs']
        return verdict('ver_full', dirs)
    return scen('ver_full', go)


# ═════════════════════════ 검사 등록 ═════════════════════════
def check(cid, title):
    def deco(fn):
        CHECKS.append((cid, title, fn))
        return fn
    return deco


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def r0_power(W, law='P0'):
    m = W['sbe']
    s_ref = m['s_ref'] * W.get('law_factor', {}).get(law, 1.0)
    return m['R_ref'] * (s_ref / T_S) ** (1.0 / m['e'])


# ── L 사다리 ──
def eval_L02(res):
    W = wdata(res['world'])
    want = float(f'{r0_power(W):.3g}')
    got = float(lad(res).get('R_j0') or 'nan')
    return got == want, f'R_j,0 {got!r} ↔ 손계산 {want!r}'


def eval_L03(res, law='P0'):
    """§3-2b 끝 규칙 손계산 — 후보 = 참 역상 (거듭제곱이라 ln–ln 보간이 정확) · 끝 = 후보 (확인 런이 바깥) 또는 바깥 실측 이웃 · 바깥 감쌈."""
    W = wdata(res['world'])
    L = lad(res)
    rt = r0_power(W, law)
    e = W['sbe']['e']
    T = {'lo': T_S * 1.02, 'hi': T_S * 0.98}
    true = {'lo': rt * 1.02 ** (-1.0 / e), 'hi': rt * 0.98 ** (-1.0 / e)}
    ends = L.get('ends') or {}
    pts = {k: sig_main(W, SBE_KIT, k, law) for k in L.get('order', []) if k not in ('inf', '0')}
    bad = []
    for side in ('lo', 'hi'):
        en = ends.get(side) or {}
        cand = en.get('candidate')
        if cand is None or rel(float(cand), true[side]) > 1e-9:
            bad.append(f'{side} 후보 {cand} ↔ 참 {true[side]!r}')
            continue
        sc = sig_main(W, SBE_KIT, cand, law)
        out_ok = (sc >= T[side]) if side == 'lo' else (sc <= T[side])
        pool = [float(k) for k, s in pts.items() if ((s >= T[side]) if side == 'lo' else (s <= T[side]))]
        want = float(cand) if out_ok else (max(pool) if side == 'lo' else min(pool))
        got = float(L.get('R_j_lo' if side == 'lo' else 'R_j_hi') or 'nan')
        if got != want or en.get('source') != ('candidate' if out_ok else 'outer_neighbor') or en.get('origin_pushes') != 0:
            bad.append(f'{side} 끝 {got!r} ↔ 손계산 {want!r} ({en.get("source")} · 밀기 {en.get("origin_pushes")})')
        if (side == 'lo' and got > true['lo'] * (1 + 1e-12)) or (side == 'hi' and got < true['hi'] * (1 - 1e-12)):
            bad.append(f'{side} 바깥 감쌈 깨짐 {got!r} · 참 {true[side]!r}')
    ratio = float(L.get('R_j_hi') or 'nan') / float(L.get('R_j_lo') or 'nan')
    if not (isinstance(L.get('R_ratio'), float) and rel(L['R_ratio'], ratio) < 1e-12):
        bad.append(f'R_ratio {L.get("R_ratio")!r} ↔ {ratio!r}')
    return not bad, bad


@check('L01', '정상 사다리 (거듭제곱) — CALIBRATED · 바닥 · 천장 · 1e4 · 1e6 · 1e8 · 반씩 둘 (1e7 · 10^6.5) · 확인 하나 · 끝 확인 둘 (lo · hi 후보)')
def t_L01():
    r = s_main('P0')
    L = lad(r)
    ends = L.get('ends') or {}
    want = ['inf', '0', '10000.0', '1000000.0', '100000000.0', '10000000.0', repr(10 ** 6.5), L.get('R_j0'),
            (ends.get('lo') or {}).get('candidate'), (ends.get('hi') or {}).get('candidate')]
    return (r['rc'] == 0 and r['sum']['status'] == 'CALIBRATED' and L.get('order') == want and L.get('n_bisect') == 2
            and L.get('n_ext') == 0 and L.get('n_runs') == 10 and L.get('states', {}).get('inf') == 'positive',
            (r['rc'], r['sum'] and r['sum'].get('status'), L.get('order'), stop_code(r)))


@check('L02', 'R_j,0 손계산 = R_ref·(s_ref/1.63)^(1/e) 의 유효숫자 3 자리 (2.27e6 · ln–ln 보간이 거듭제곱에서 정확)')
def t_L02():
    return eval_L02(s_main('P0'))


@check('L03', '§3-2b 끝 규칙 (3판 · RCA-01) — 후보 = 참 역상 · 끝 확인 런 → 후보 (바깥) 또는 바깥 실측 이웃 · 참 허용집합을 바깥에서 감싼다 · '
               '역상 R 비 기록')
def t_L03():
    return eval_L03(s_main('P0'))


@check('L04', '끼는 이웃 비 ≤ 10^0.5 · 확인 1 회 통과 · 국소 e ≥ e_min (진단) · 점 수 ≤ 계획 상한 · 상한 없음 (none) = width_ok None')
def t_L04():
    L = lad(s_main('P0'))
    a, b = (float(x) for x in L.get('bracket') or ('nan', 'nan'))
    return (math.log10(b / a) <= 0.5 + 1e-9 and L.get('local_e_ge_emin') is True and [c['ok'] for c in L.get('confirms', [])] == [True]
            and L.get('n_runs', 99) <= FX['plan_obj']['max_ladder_points'] and L.get('ratio_cap') == 'none' and L.get('width_ok') is None,
            (L.get('bracket'), L.get('confirms'), L.get('n_runs'), L.get('width_ok')))


@check('L05', '×100 아래 확장 — 세 점 모두 표적 아래 → 1e2 → 반씩 → R_j,0 = 1e4·(1.2/1.63)^4 의 3 자리 (2.94e3)')
def t_L05():
    W0 = dict(PW, sbe=dict(PW_SBE, s_ref=1.2e-3, R_ref=1e4, floor=0.05e-3, ceiling=10e-3))
    r = scen('L05', lambda: ladder('L05', world('L05', W0)))
    L = lad(r)
    want = float(f'{1e4 * (1.2 / 1.63) ** 4:.3g}')
    return (r['sum']['status'] == 'CALIBRATED' and L.get('n_ext') == 1 and '100.0' in L.get('order', [])
            and float(L.get('R_j0') or 'nan') == want, (L.get('order'), L.get('R_j0'), want))


@check('L06', '×100 위 확장 — R_j,0 = 1e8·(2.5/1.63)^4 의 3 자리 (5.53e8) · 1e10 점')
def t_L06():
    W0 = dict(PW, sbe=dict(PW_SBE, s_ref=2.5e-3, R_ref=1e8, floor=0.05e-3, ceiling=100e-3))
    r = scen('L06', lambda: ladder('L06', world('L06', W0)))
    L = lad(r)
    want = float(f'{1e8 * (2.5 / 1.63) ** 4:.3g}')
    return (r['sum']['status'] == 'CALIBRATED' and L.get('n_ext') == 1 and '10000000000.0' in L.get('order', [])
            and float(L.get('R_j0') or 'nan') == want, (L.get('order'), L.get('R_j0'), want))


@check('L07', '로지스틱 — R_j,0 = 사슬이 고른 끼는 쌍에서 손으로 ln–ln 보간한 값의 3 자리 (독립 계산) · 쌍이 참 근을 낀다')
def t_L07():
    LW = dict(PW, sbe={'kind': 'logistic', 'f': 0.5e-3, 'C': 20e-3, 'Rc': 1e4, 'beta': 0.5, 'floor': 0.5e-3, 'ceiling': 20e-3})
    r = scen('L07', lambda: ladder('L07', world('L07', LW)))
    L = lad(r)
    W = wdata(r['world'])
    ra, rb = (L.get('bracket') or ['nan', 'nan'])
    sa, sb = sig_main(W, SBE_KIT, ra, 'P0'), sig_main(W, SBE_KIT, rb, 'P0')
    t = (math.log(T_S) - math.log(sa)) / (math.log(sb) - math.log(sa))
    want = float(f'{math.exp(math.log(float(ra)) + t * (math.log(float(rb)) - math.log(float(ra)))):.3g}')
    root = 1e4 * ((20e-3 - 0.5e-3) / (T_S - 0.5e-3) - 1.0) ** 2
    return (r['sum']['status'] == 'CALIBRATED' and float(L.get('R_j0') or 'nan') == want and float(ra) < root < float(rb),
            (ra, rb, L.get('R_j0'), want, root))


@check('L08', 'CALIB_IMPOSSIBLE — 천장 1.5 < 1.63 · 런 둘 (바닥 · 천장) 뒤 멈춤 · rc 3')
def t_L08():
    r = scen('L08', lambda: ladder('L08', world('L08', dict(PW, sbe=dict(PW_SBE, ceiling=1.5e-3)))))
    return (r['rc'] == 3 and r['sum']['status'] == 'CALIB_IMPOSSIBLE' and roles(r) == ['floor', 'ceiling'],
            (r['rc'], r['sum'] and r['sum']['status'], roles(r)))


@check('L09', 'CALIB_IMPOSSIBLE — 바닥 2.0 > 1.63')
def t_L09():
    r = scen('L09', lambda: ladder('L09', world('L09', dict(PW, sbe=dict(PW_SBE, floor=2.0e-3, s_ref=40e-3)))))
    return r['sum']['status'] == 'CALIB_IMPOSSIBLE', (r['sum']['status'], stop_code(r))


def run_L10():
    return scen('L10', lambda: ladder('L10', world('L10', dict(PW, sbe=dict(PW_SBE, floor=1.60e-3, s_ref=40e-3)))))


@check('L10', 'CALIB_EDGE — 바닥 1.60 (1.63 의 2 % 안) · 사다리 점 없음')
def t_L10():
    r = run_L10()
    return r['sum']['status'] == 'CALIB_EDGE' and roles(r) == ['floor', 'ceiling'], (r['sum']['status'], roles(r))


def run_L11(tag, **kw):
    W0 = dict(PW, sbe=dict(PW_SBE, s_ref=1.65e-3, e=0.01))
    return ladder(tag, world(tag, W0), **kw)


def eval_L11(r):
    L = lad(r)
    true_ratio = (1.02 / 0.98) ** (1.0 / 0.01)              # 참 역상 R 비 (거듭제곱 e 0.01) = 54.6
    return (r['sum']['status'] == 'CALIBRATED' and L.get('local_e_ge_emin') is False and 'confirm' in roles(r)
            and isinstance(L.get('R_ratio'), float) and L['R_ratio'] >= true_ratio * (1 - 1e-9),
            (r['sum']['status'], L.get('local_e_ge_emin'), L.get('R_ratio'), true_ratio, stop_code(r)))


@check('L11', '3판 e_min = 국소 진단 (RCA-01 · R3-Q3) — 탄성 e = 0.01 < e_min 이어도 멈추지 않는다 · 확인 · 끝 규칙 → CALIBRATED (상한 none) · '
               '역상 R 비 ≥ 참 54.6 · local_e_ge_emin False 기록')
def t_L11():
    return eval_L11(scen('L11', lambda: run_L11('L11')))


@check('L11b', '역상 R 비 상한이 등록되면 (계획 calib_rj_ratio_max 50) — 실제 역상 폭 54.6 이상 > 50 → CALIB_UNIDENTIFIED (§3-2b ④ · 3판 뜻)')
def t_L11b():
    def go():
        p, _sha, reg = plan_set('cap50', calib_rj_ratio_max=50.0)
        return run_L11('L11b', plan=p, reg=reg)
    r = scen('L11b', go)
    L = lad(r)
    return (r['sum']['status'] == 'CALIB_UNIDENTIFIED' and L.get('width_ok') is False and L.get('R_ratio', 0) > 50.0,
            (r['sum']['status'], L.get('width_ok'), L.get('R_ratio'), stop_code(r)))


@check('L12', 'CALIB_UNCONFIRMED — 확인 두 번 다 2 % 넘음 (확인 런 정확히 둘)')
def t_L12():
    r = scen('L12', lambda: ladder('L12', world('L12', dict(PW, bump_seq=[1.05, 0.95]))))
    return (r['sum']['status'] == 'CALIB_UNCONFIRMED' and roles(r).count('confirm') == 2
            and [c['ok'] for c in lad(r).get('confirms', [])] == [False, False], (r['sum']['status'], roles(r)))


@check('L13', '확인 한 번 실패 → 그 점을 넣고 다시 보간 → 둘째 확인 통과 (CALIBRATED · 확인 2) — ★ 3판: 곡률로 (매끈한 로지스틱 β 1.5 · Rc 1e4) · '
               '옛 잡음 범프 (×1.03) 는 끝 런 사이에서 비단조 (τ_mono) 로 잡힌다 = 세계가 단조가 아니다')
def t_L13():
    LW13 = dict(PW, sbe={'kind': 'logistic', 'f': 0.5e-3, 'C': 20e-3, 'Rc': 1e4, 'beta': 1.5, 'floor': 0.5e-3, 'ceiling': 20e-3})
    r = scen('L13', lambda: ladder('L13', world('L13', LW13)))
    L = lad(r)
    return (r['sum']['status'] == 'CALIBRATED' and [c['ok'] for c in L.get('confirms', [])] == [False, True]
            and L['confirms'][0]['rj'] in L.get('order', []), (r['sum']['status'], L.get('confirms')))


def run_L14(tag):
    return ladder(tag, world(tag, dict(PW, rj_factor={'100000000.0': 5.0})))


@check('L14', 'CALIB_NONMONOTONE — 1e8 이 1e6 보다 높다 (ln 차 > τ_mono)')
def t_L14():
    r = scen('L14', lambda: run_L14('L14'))
    return r['sum']['status'] == 'CALIB_NONMONOTONE', (r['sum']['status'], stop_code(r))


@check('L15', '평탄 (τ_mono 안에서 오름) = 기록만 · 비단조로 멈추지 않음')
def t_L15():
    W = dict(PW, sbe=dict(PW_SBE, floor=0.05e-3))         # 바닥 < σ(1e10) = 0.2e-3 (세계 자체가 단조여야 한다)
    W['rj_sigma'] = {'100000000.0': 2.0e-3 * 1.0005}
    r = scen('L15', lambda: ladder('L15', world('L15', W)))
    return (r['sum']['status'] != 'CALIB_NONMONOTONE' and ['1000000.0', '100000000.0'] in lad(r).get('flat_pairs', []),
            (r['sum']['status'], lad(r).get('flat_pairs')))


def run_L16(tag):
    W0 = dict(PW, sbe=dict(PW_SBE, s_ref=10e-3, R_ref=1e8, e=0.05, floor=0.5e-3, ceiling=100e-3))
    if 'cap12' not in FX:
        FX['cap12'] = plan_set('cap12', max_ladder_points=12)
    p, _sha, reg = FX['cap12']
    return ladder(tag, world(tag, W0), plan=p, reg=reg)


@check('L16', 'CALIB_LADDER_EXHAUSTED — 계획 점 수 상한 12 (시험 값) · 런 12 개 (바닥 · 천장 · 셋 · ×100 일곱) 뒤 13 째 요청에서 · 상한 = 계획 칸 '
               '(사슬 기본값 없음)')
def t_L16():
    r = scen('L16', lambda: run_L16('L16'))
    return (r['sum']['status'] == 'CALIB_LADDER_EXHAUSTED' and len(roles(r)) == 12 and n_calls(r['world']) == 12
            and r['sum'].get('constants', {}).get('max_ladder_points') == 12, (r['sum']['status'], len(roles(r))))


@check('L17', 'NOT_COMPUTED — 1e6 점 수렴 증서 실패 → 그 점 NOT_COMPUTED · 사다리 멈춤 (뒤 런 없음)')
def t_L17():
    r = scen('L17', lambda: ladder('L17', world('L17', dict(PW, faults=[{'do': 'certfail', 'match': {'rj': '1000000.0'}}]))))
    return (r['rc'] == 3 and r['sum']['status'] == 'NOT_COMPUTED' and len(roles(r)) == 4 and n_calls(r['world']) == 4,
            (r['sum']['status'], roles(r), stop_code(r)))


@check('L18', 'origin §3-3 통과 — R_j,0 에서 arm 1 · 2 만 (ARM_LIST=1,2 한 런 · ARMS 없음 · a0 다시 안 돎) · 팔 sid 지문 = origin 마다 '
               '(arm 1 ≠ arm 2 인데 SID_GRID 아님) · ln(max/min) ≤ 0.02 · 8 팔 없음 · 표지 없음')
def t_L18():
    return eval_L18(s_main('P0'))


def eval_L18(r):
    o = lad(r).get('origin') or {}
    runs = [x for x in r['sum'].get('runs', []) if x['role'] == 'origin']
    eruns = [x for x in r['sum'].get('runs', []) if x['role'] == 'end_origin']
    ev = [e for e in env_log(r['world']) if 'ARM_LIST' in e]
    ar = (runs[0].get('arms_read') or []) if runs else []
    L = lad(r)
    return (o.get('status') == 'pass' and len(runs) == 1 and 'origin3' not in roles(r) and 'origin8' not in roles(r)
            and r['sum'].get('flags') == [] and len(ev) == 1 + len(eruns) and all(e.get('ARM_LIST') == '1,2' and 'ARMS' not in e for e in ev)
            and [a.get('index') for a in ar] == [1, 2] and not [a for a in ar if a['file'].endswith('_a0.json')]
            and len({a.get('sid_fp') for a in ar}) == 2
            #  ★ Q-E — 끝마다 origin 팔 1 · 2 (끝 R) · 점 수에 안 센다
            and sorted(x['rj'] for x in eruns) == sorted({L.get('R_j_lo'), L.get('R_j_hi')} - {L.get('R_j0')})
            and L.get('n_runs') == len(L.get('order', [])),
            (o, roles(r), ev, [(a.get('index'), a.get('file')) for a in ar], stop_code(r)))


def run_L19(tag):
    return ladder(tag, world(tag, dict(PW, arm_factor=[1.0, 1.02, 0.99, 1.0, 1.0, 1.0, 1.0, 1.0])))


def eval_L19(r):
    o = lad(r).get('origin') or {}
    return (r['sum']['status'] == 'CALIBRATED' and o.get('status') == 'sensitive' and 'origin8' in roles(r)
            and 'CALIB_ORIGIN_SENSITIVE' in r['sum'].get('flags', [])
            and float(lad(r).get('R_j0') or 'nan') == float(f'{r0_power(PW):.3g}'), (o, roles(r), r['sum'].get('flags')))


@check('L19', 'origin §3-3 넘음 (arm 1 +2 % · arm 2 −1 %) → 8 팔 런 · CALIB_ORIGIN_SENSITIVE · R_j,0 는 arm 0 값 그대로')
def t_L19():
    return eval_L19(scen('L19', lambda: run_L19('L19')))


@check('L20', 'P1 법칙 사다리 — 같은 SBE · 법칙 배수 0.95 → R_j,0 = 1.85e6 (법칙 끝마다 따로 보정)')
def t_L20():
    r = s_main('P1')
    want = float(f'{r0_power(PW, "P1"):.3g}')
    return (r['sum']['status'] == 'CALIBRATED' and float(lad(r).get('R_j0') or 'nan') == want
            and all(e.get('CJUNC_PTFE_JLAW') == 'P1' for e in env_log(r['world'])), (lad(r).get('R_j0'), want))


# ── S 멈춤 목록 ──
def stop_case(tag, faults, expect, base=None, **kw):
    r = scen(tag, lambda: ladder(tag, world(tag, dict(base or PW, faults=faults)), **kw))
    return (r['rc'] == 3 and stop_code(r) == expect and r['sum']['status'] == 'STOPPED'
            and isinstance((r['sum'].get('stop') or {}).get('cause'), str), (r['rc'], stop_code(r), r['sum'] and r['sum'].get('stop')))


@check('S01', '출력 폴더가 있고 비어 있지 않음 → OUTDIR_NOT_EMPTY · 러너 0 회 · 그 폴더에 아무것도 안 씀')
def t_S01():
    r = scen('S01', lambda: ladder('S01', world('S01'), prefill=True))
    return (r['rc'] == 3 and n_calls(r['world']) == 0 and sorted(os.listdir(r['out'])) == ['old.txt'] and 'OUTDIR_NOT_EMPTY' in r['so'],
            (r['rc'], os.listdir(r['out']), r['so'][-300:]))


@check('S02', '러너 rc 2 → RUNNER_RC')
def t_S02():
    return stop_case('S02', [{'do': 'rc2', 'match': {'rj': '10000.0'}}], 'RUNNER_RC')


def run_S02():
    t_S02()
    return SCEN['S02']


@check('S03', '.rejected_* 기록 → REJECTED_MARKER')
def t_S03():
    return stop_case('S03', [{'do': 'rejected', 'match': {'rj': '0'}}], 'REJECTED_MARKER')


@check('S04', '팔 JSON 이 같은 번호로 둘 → ARM_JSON_COUNT')
def t_S04():
    return stop_case('S04', [{'do': 'two_json', 'match': {'rj': 'inf'}}], 'ARM_JSON_COUNT')


@check('S05', '러너가 다른 σ_AM_S (0.01 · 영수증 = 매니페스트 → 정본 계약은 지난다) → 사슬 MAN_FIXED 대조 → MANIFEST_MISMATCH')
def t_S05():
    return stop_case('S05', [{'do': 'bad_am_s', 'match': {'rj': '1000000.0'}}], 'MANIFEST_MISMATCH')


@check('S06', '섞인 세대 — p2 팔 (ca_ext 없음 · centerline) → GENERATION')
def t_S06():
    return stop_case('S06', [{'do': 'p2gen', 'match': {'rj': '10000.0'}}], 'GENERATION')


@check('S07', 'unknown:ca_ext (요청 칸 있음 · 블록 없음) → GENERATION')
def t_S07():
    return stop_case('S07', [{'do': 'unknown_caext', 'match': {'rj': '0'}}], 'GENERATION')


@check('S08', '저장 id ≠ 다시 계산한 id → GENERATION')
def t_S08():
    return stop_case('S08', [{'do': 'stale_id', 'match': {'rj': '100000000.0'}}], 'GENERATION')


@check('S09', 'ca_ext 블록 변조 (쓴 뒤 원장 수) → CA_EXT_RECORD (계약 자리)')
def t_S09():
    return stop_case('S09', [{'do': 'tamper_caext', 'match': {'rj': 'inf'}}], 'CA_EXT_RECORD')


@check('S10', '솔브 영수증 ≠ LEAN 2 표 (접합 주 솔브 failed — 정본 계약 허용 · LEAN 2 표 = applied | absent_geometry) → RECEIPT_LEAN')
def t_S10():
    return stop_case('S10', [{'do': 'lean_bad', 'match': {'rj': '10000.0'}}], 'RECEIPT_LEAN')


@check('S11', 'face_alpha 런의 ptfe_cells_observed > 0 → 정본 계약 (ptfe_face 검증기) 이 먼저 잡는다 → CA_EXT_RECORD')
def t_S11():
    return stop_case('S11', [{'do': 'ptfe_cells', 'match': {'rj': '0'}}], 'CA_EXT_RECORD')


@check('S12', 'sid 격자 지문이 같은 킷 · 같은 래스터 · 같은 origin 런 사이에서 다르다 (두 블록 다 · 정본 계약은 지난다) → SID_GRID')
def t_S12():
    return stop_case('S12', [{'do': 'sid_fp', 'match': {'rj': '1000000.0'}}], 'SID_GRID')


@check('S13', 'env 에 SIGMA_VGCF_OVERRIDE → ENV_SIGMA_VGCF_OVERRIDE · 러너 0 회')
def t_S13():
    r = scen('S13', lambda: ladder('S13', world('S13'), env={'SIGMA_VGCF_OVERRIDE': '2.618'}))
    return (r['rc'] == 3 and stop_code(r) == 'ENV_SIGMA_VGCF_OVERRIDE' and n_calls(r['world']) == 0, (r['rc'], stop_code(r)))


@check('S14', '부모 env 오염 (SIGMA_ION_SE · P2_SCR · SIGMA_PTFE · MPM_PERIODIC_SIGMA · EXPECT_PROTOCOL · CJUNC_RJ · ★ ARM_LIST · EXPECT_BACKEND) '
               '→ 지우고 돈다 · 요약에 이름')
def t_S14():
    bad = {'SIGMA_ION_SE': '0.0015', 'P2_SCR': '/tmp/elsewhere', 'SIGMA_PTFE': '1e-16', 'MPM_PERIODIC_SIGMA': '1',
           'EXPECT_PROTOCOL': 'p2-0000', 'CJUNC_RJ': '999', 'ARM_LIST': '3,4', 'EXPECT_BACKEND': 'cpu'}
    r = scen('S14', lambda: ladder('S14', world('S14', dict(PW, sbe=dict(PW_SBE, ceiling=1.5e-3))), env=bad))
    ev = env_log(r['world'])
    leak = [k for e in ev for k in bad if e.get(k) == bad[k]]          # 오염 값이 러너에 닿았다 (사슬이 정한 값 = CJUNC_RJ · EXPECT_BACKEND 는 정상)
    return (len(ev) == 2 and not leak and set(bad) <= set(r['sum'].get('env_scrubbed', [])) and ev[0].get('CJUNC_RJ') == 'inf'
            and all('ARM_LIST' not in e and e.get('EXPECT_BACKEND') == 'gpu' for e in ev),
            (leak, r['sum'].get('env_scrubbed'), [e.get('CJUNC_RJ') for e in ev]))


@check('S15', '계획 해시 ≠ 등록 §2-1 개정값 → PLAN_HASH_MISMATCH · 러너 0 회')
def t_S15():
    r = scen('S15', lambda: ladder('S15', world('S15'), reg=FX['reg_other']))
    return r['rc'] == 3 and stop_code(r) == 'PLAN_HASH_MISMATCH' and n_calls(r['world']) == 0, (r['rc'], stop_code(r))


@check('S16', '등록 §2-1 계획 해시 칸이 아직 ⬜ → PLAN_HASH_UNREGISTERED · 러너 0 회')
def t_S16():
    r = scen('S16', lambda: ladder('S16', world('S16'), reg=FX['reg_unreg']))
    return r['rc'] == 3 and stop_code(r) == 'PLAN_HASH_UNREGISTERED' and n_calls(r['world']) == 0, (r['rc'], stop_code(r))


@check('S17', '시간 상한 — 첫 런이 상한 안에 안 끝남 → TIME_LIMIT')
def t_S17():
    r = scen('S17', lambda: ladder('S17', world('S17', dict(PW, faults=[{'do': 'sleep', 's': 3.0, 'match': {'n': 1}}])),
                                   max_hours='0.0001'))
    return r['rc'] == 3 and stop_code(r) == 'TIME_LIMIT', (r['rc'], stop_code(r))


@check('S18', '러너가 다른 rtol (1e-13 · 영수증 = 매니페스트 = 증서 → 정본 계약 · 증서는 지난다) ≠ 계획 → MANIFEST_MISMATCH')
def t_S18():
    return stop_case('S18', [{'do': 'receipt_rtol', 'match': {'rj': '10000.0'}}], 'MANIFEST_MISMATCH')


@check('S19', '표적 ≠ 등록 (1.64) → NOT_REGISTERED · 러너 0 회 (판정선을 옮기지 않는다)')
def t_S19():
    def go():
        w = world('S19')
        out = Path(TD) / 'runs' / 'S19'
        rc, so = call(['--stage', 'ladder', '--law', 'P0', '--target', '1.64', '--runner', FX['runner'], '--root', FX['root'],
                       '--plan', FX['plan'], '--s0-plan', FX['s0'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out]
                      + s0_args(), w)
        sp = out / 'ladder_summary.json'
        return {'rc': rc, 'so': so, 'world': w, 'sum': json.loads(sp.read_text()) if sp.exists() else None}
    r = scen('S19', go)
    return r['rc'] == 3 and 'NOT_REGISTERED' in r['so'] and n_calls(r['world']) == 0, (r['rc'], r['so'][-200:])


@check('S20', '같은 킷 · 같은 계획 두 번 — 예측에 P0 사다리 둘 → DUPLICATE_RUN · 런 0')
def t_S20():
    def go():
        dup = Path(TD) / 'runs' / 'S20_dupP0'
        shutil.copytree(s_main('P0')['out'], dup)
        return predict('S20', world('S20'), [s_main('P0')['out'], dup])
    r = scen('S20', go)
    return r['rc'] == 3 and stop_code(r) == 'DUPLICATE_RUN' and n_calls(r['world']) == 0, (r['rc'], stop_code(r))


@check('S21', '판정 입력에 같은 폴더 두 번 → DUPLICATE_RUN · 판정 NOT_COMPUTED')
def t_S21():
    r = scen('S21', lambda: verdict('S21', main_dirs() + [s_main('P0')['out']]))
    return (r['rc'] == 3 and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED' and stop_code(r) == 'DUPLICATE_RUN',
            (r['rc'], r['v'] and r['v'].get('stop')))


def tamper_copy(tag):
    """주 세트 사본 → P0 사다리의 확인 런 팔 하나의 σ 를 바꾼다 (sha256 이 달라진다)."""
    base = Path(TD) / 'runs' / tag
    base.mkdir(parents=True)
    dirs = []
    for d in main_dirs():
        dst = base / Path(d).name
        shutil.copytree(d, dst)
        dirs.append(dst)
    s = json.loads((dirs[0] / 'ladder_summary.json').read_text(encoding='utf-8'))
    run = [x for x in s['runs'] if x['role'] == 'confirm'][-1]
    p = dirs[0] / run['outdir'] / run['arms_read'][0]['file']
    d = json.loads(p.read_text(encoding='utf-8'))
    d['mpm_metrics']['step3']['sigma_e_eff_S_cm'] *= 1.001
    d['mpm_metrics']['step3']['conv_cert']['sigma'] *= 1.001
    p.write_text(json.dumps(d), encoding='utf-8')
    return dirs


def run_S22(tag):
    dirs = tamper_copy(tag + '_in')
    return verdict(tag, dirs)


def eval_S22(r):
    return (r['rc'] == 3 and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED' and stop_code(r) == 'INPUT_SHA_MISMATCH',
            (r['rc'], r['v'] and r['v'].get('stop')))


@check('S22', '판정 입력 sha256 ≠ 런 산출 (사다리 확인 팔 변조) → INPUT_SHA_MISMATCH · 판정 NOT_COMPUTED')
def t_S22():
    return eval_S22(scen('S22', lambda: run_S22('S22')))


@check('S23', '멈춤 = 구조화 사유 (code · cause · run) · 화면에 코드 · rc 3')
def t_S23():
    r = run_S02()
    st = r['sum']['stop']
    return (set(st) >= {'code', 'cause', 'run'} and st['run'] and 'RUNNER_RC' in r['so'], st)


@check('S24', '매니페스트만 σ_AM_S 0.01 (영수증 0.0041) → 정본 check_arm (receipt_match) → ARM_CONTRACT')
def t_S24():
    return stop_case('S24', [{'do': 'bad_am_s_man', 'match': {'rj': '1000000.0'}}], 'ARM_CONTRACT')


@check('S25', '집전체 솔브에 접합 적용 (LEAN 2 표 밖) → 정본 계약 (접합 검증기) → CA_EXT_RECORD')
def t_S25():
    return stop_case('S25', [{'do': 'lean_wetted', 'match': {'rj': '10000.0'}}], 'CA_EXT_RECORD')


@check('S26', 'off 격자 sid 지문 ≠ 접합 원장 sid (같은 솔브) → 정본 계약 → CA_EXT_RECORD')
def t_S26():
    return stop_case('S26', [{'do': 'sid_off_other', 'match': {'rj': '1000000.0'}}], 'CA_EXT_RECORD')


@check('S27', 'off 격자 sid 지문 칸 없음 → 정본 계약 (ptfe_face 검증기) → CA_EXT_RECORD')
def t_S27():
    return stop_case('S27', [{'do': 'no_sid_off', 'match': {'rj': '1000000.0'}}], 'CA_EXT_RECORD')


# ── P 예측 ──
@check('P01', '예측 — SBE c no-op 런 둘 · 모서리 12 런 (arm 0) · origin = 네 모서리 × 세 R = 12 (ARM_LIST=1,2 · §4-2 3판 · RCA-02) · '
               '상태 PREDICTED')
def t_P01():
    r = s_main_predict()
    rl = roles(r)
    ev = [e for e in env_log(r['world']) if 'ARM_LIST' in e]
    return (r['rc'] == 0 and r['sum']['status'] == 'PREDICTED' and rl.count('sbe_noop') == 2 and rl.count('corner') == 12
            and rl.count('origin') == 12 and 'origin3' not in rl and 'origin8' not in rl and len(ev) == 12
            and all(e.get('ARM_LIST') == '1,2' and 'ARMS' not in e and 'DBE' in e.get('KITS', '') for e in ev)
            and all(set(o.get('per_R', {})) == {'R_j_lo', 'R_j0', 'R_j_hi'} for o in r['sum'].get('origin', [])),
            (r['rc'], r['sum'] and r['sum']['status'], rl, stop_code(r)))


@check('P01b', 'SV 반사실 (§5-6 SV 행 · 계획 범위 R_j0) — CJUNC_SV_CF=1 은 DBE 모서리 × R_j,0 런 넷에만 (다른 R · origin · SBE no-op 없음) · '
               '팔 증거 요청 {threshold: null} · 영수증 sv_counterfactual True · 팔 기록 sv_cf_status = computed')
def t_P01b():
    r = s_main_predict()
    L = {law: lad(s_main(law)) for law in ('P0', 'P1')}
    on = [e for e in env_log(r['world']) if e.get('CJUNC_SV_CF') == '1']
    want = sorted((law, L[law]['R_j0']) for law in ('P0', 'P1') for _c in ('0', '1'))
    got = sorted((e['CJUNC_PTFE_JLAW'], e['CJUNC_RJ']) for e in on)
    runs = [x for x in r['sum'].get('runs', []) if x.get('sv_cf')]
    ok_arm = True
    for x in runs:
        d = Path(r['out']) / x['outdir']
        a = json.loads((d / x['arms_read'][0]['file']).read_text(encoding='utf-8'))['mpm_metrics']['step3']['manifest']
        rcpt = json.loads((d / 'run_receipt.json').read_text(encoding='utf-8'))
        ok_arm &= (a['ca_ext']['cjunc']['evidence'].get('sv_counterfactual_request') == {'threshold': None}
                   and rcpt.get('sv_counterfactual') is True and x['arms_read'][0].get('sv_cf_status') == 'computed'
                   and x['role'] == 'corner' and x.get('arm_list') is None)
    return (got == want and len(runs) == 4 and ok_arm and all('KITS' in e and 'DBE' in e['KITS'] and 'ARMS' in e for e in on),
            (got, want, [x.get('role') for x in runs]))


@check('P02', 'R_j 는 사다리 요약에서 — 모서리 런의 CJUNC_RJ = 사다리 R_j,lo · R_j,0 · R_j,hi 문자열 그대로 (사람 옮김 없음)')
def t_P02():
    r = s_main_predict()
    want = set()
    for law in ('P0', 'P1'):
        L = lad(s_main(law))
        want |= {(law, L['R_j_lo']), (law, L['R_j0']), (law, L['R_j_hi'])}
    got = {(e['CJUNC_PTFE_JLAW'], e['CJUNC_RJ']) for e in env_log(r['world']) if 'DBE' in e['KITS']}
    return got == want, (sorted(got), sorted(want))


@check('P03', 'SBE c no-op 위반 (c1 비트 다름) → SAME_P_CONSISTENCY · 모서리 런 없음')
def t_P03():
    r = scen('P03', lambda: predict('P03', world('P03', dict(PW, faults=[{'do': 'sbe_c_dep'}])),
                                    [s_main('P0')['out'], s_main('P1')['out']]))
    return (r['rc'] == 3 and stop_code(r) == 'SAME_P_CONSISTENCY' and 'corner' not in roles(r), (r['rc'], stop_code(r), roles(r)))


@check('P04', 'DBE c1 < c0 − τ_mono → SAME_P_CONSISTENCY')
def t_P04():
    r = scen('P04', lambda: predict('P04', world('P04', dict(PW, faults=[{'do': 'dbe_c_inv'}])),
                                    [s_main('P0')['out'], s_main('P1')['out']]))
    return r['rc'] == 3 and stop_code(r) == 'SAME_P_CONSISTENCY', (r['rc'], stop_code(r))


DBE_ORIGIN_ARMS = [1.0, 1.03, 0.98, 1.01, 0.995, 1.0, 1.002, 0.999]


def s_origin_dbe():
    def go():
        p = predict('P05', world('P05', dict(PW, arm_factor_dbe=DBE_ORIGIN_ARMS)), [s_main('P0')['out'], s_main('P1')['out']])
        v = verdict('P05_v', [s_main('P0')['out'], s_main('P1')['out'], p['out']])
        return {'pred': p, 'ver': v}
    return scen('P05', go)


@check('P05', 'origin §4-2 3판 — 넘는 모서리 넷 → 모서리마다 세 R 전부 8 팔 (런 12) · 값 = 그 R 의 8 팔 평균 (판정 결과 손계산)')
def t_P05():
    sc = s_origin_dbe()
    p, v = sc['pred'], sc['ver']
    W = wdata(p['world'])
    mean8 = sum(DBE_ORIGIN_ARMS) / 8.0
    vals = []
    for law in ('P0', 'P1'):
        L = lad(s_main(law))
        for c in ('0', '1'):
            for k in ('R_j_lo', 'R_j0', 'R_j_hi'):
                vals.append(sig_main(W, DBE_KIT, L[k], law, c) * mean8)
    lo, hi = min(vals) * 1e3, max(vals) * 1e3
    got = (v['r'] or {}).get('interval_mScm') or [math.nan, math.nan]
    ok_runs = roles(p).count('origin8') == 12 and all(o['status'] == 'adjusted' for o in p['sum'].get('origin', []))
    return ok_runs and rel(got[0], lo) < 1e-12 and rel(got[1], hi) < 1e-12, (roles(p), got, [lo, hi])


@check('P06', '사다리가 CALIB_* 면 예측 안 함 → LADDER_NOT_CALIBRATED · 런 0')
def t_P06():
    r = scen('P06', lambda: predict('P06', world('P06'), [run_L10()['out'], s_main('P1')['out']]))
    return r['rc'] == 3 and stop_code(r) == 'LADDER_NOT_CALIBRATED' and n_calls(r['world']) == 0, (r['rc'], stop_code(r))


# ── V 판정 ──
def main_corners(W):
    vals = []
    for law in ('P0', 'P1'):
        L = lad(s_main(law))
        for c in ('0', '1'):
            for k in ('R_j_lo', 'R_j0', 'R_j_hi'):
                vals.append(sig_main(W, DBE_KIT, L[k], law, c))
    return vals


@check('V01', '판정 손계산 — 구간 · W · p · S (가짜 함수에서 직접) · PASS_INFORMATIVE (4.68 ∈ I · W ≤ G0/2)')
def t_V01():
    v = s_verdict_main()
    W = wdata(s_main_predict()['world'])
    vals = main_corners(W)
    lo, hi = min(vals) * 1e3, max(vals) * 1e3
    Wd = math.log(hi / lo)
    G0 = math.log(4.68 / 1.8877)
    p = math.log(4.68 / lo) / Wd
    S = 1.0 - abs(math.log(4.68 / math.sqrt(lo * hi))) / G0
    R = v['r'] or {}
    ok = (v['v']['verdict'] == 'PASS_INFORMATIVE' and rel(R['interval_mScm'][0], lo) < 1e-12 and rel(R['interval_mScm'][1], hi) < 1e-12
          and rel(R['W'], Wd) < 1e-12 and rel(R['p'], p) < 1e-12 and rel(R['S'], S) < 1e-12 and Wd <= G0 / 2)
    return ok, (v['v'] and v['v'].get('verdict'), R.get('interval_mScm'), [lo, hi], R.get('W'), Wd)


V02_BLK = ['FIBRE_UNCHECKED', 'GRID_UNCHECKED', 'SVORDER_UNCHECKED', 'UNREG_UNCHECKED']


@check('V02', '감도 넷 안 돌림 → FIBRE · UNREG · GRID · SVORDER _UNCHECKED · §7-1 문장 금지 (판정 이름은 그대로) · ★ 4판 (Q2-4 · §5-5b · ⑰) 문장 = '
               '"계산기 판정 이름 `PASS_INFORMATIVE` · 차단 표지 <넷> — 판정 문장 보류 · 감도 미완료" · 표지마다 사유 (안 돌림) · 감도 미완료 표지')
def t_V02():
    v = s_verdict_main()['v']
    want = set(V02_BLK)
    rs = v.get('blocking_reasons') or {}
    return (want <= set(v['flags']) and v['sentence_allowed'] is False and v['verdict'] == 'PASS_INFORMATIVE'
            and v.get('sentence') == want_sentence('positive', 'PASS_INFORMATIVE', V02_BLK, sens=True)
            and set(rs) == want and all(rs[f] == '안 돌림' for f in want) and v.get('sensitivity_incomplete') is True,
            (v['flags'], v['sentence_allowed'], v.get('sentence'), rs, v.get('sensitivity_incomplete')))


@check('V03', '감도 넷 다 돌림 · 둔감 · SV 반사실 비 1.2 < 문턱 2 → 차단 표지 없음 → §7-1 문장 (판정문 §5-3 문안) 허용 · 보고 범주 '
               'ASSUMED_UNVALIDATED (DIA_UNCHECKED 포함) 는 늘 · ★ 4판 (Q2-6) 한정어 ①–⑱ · 계산기 상태 주석 · 감도 완료 · 사유 없음')
def t_V03():
    v = s_verdict_full()['v']
    cat = (v.get('report_category') or {}).get('ASSUMED_UNVALIDATED') or []
    return (v['verdict'] == 'PASS_INFORMATIVE' and v['flags'] == [] and v.get('blocking_flags') == [] and v['sentence_allowed'] is True
            and isinstance(v.get('sentence'), str) and v['sentence'] in FX['reg_text'] and v['sentence'] == T_PASS
            and any('DIA_UNCHECKED' in x for x in cat) and len(v.get('qualifiers', [])) == 18
            and '계산기 상태' in (v.get('verdict_note') or '') and v.get('sensitivity_incomplete') is False
            and v.get('blocking_reasons') == {},
            (v['verdict'], v['flags'], v['sentence_allowed'], v.get('stop'), len(v.get('qualifiers', []))))


@check('V04', 'GRID 변이에서 DBE ×1.6 → 등급 바뀜 → GRID_SENSITIVE · 문장 금지')
def t_V04():
    def go():
        g = s_variant_set('GRID', base=dict(PW, var_dbe={'GRID': 1.6}), tag='GRIDsens')
        dirs = list(main_dirs())
        for V in ('FIBRE', 'UNREG', 'SVORDER'):
            dirs += s_variant_set(V)['dirs']
        return verdict('V04', dirs + g['dirs'])
    v = scen('V04', go)['v']
    return ('GRID_SENSITIVE' in v['flags'] and v['sentence_allowed'] is False, (v['flags'], v.get('stop')))


def sv_set(tag, rule, extra_world=None):
    """주 사다리 + SV 반사실 규칙 하나 (P1 · c 1 · R_j,0 모서리) 를 넣은 예측 → 판정."""
    def go():
        m = {'kit_has': 'DBE', 'rj': lad(s_main('P1'))['R_j0'], 'c': '1'}
        W = dict(PW, sv_cf=[dict(rule, match=m)], **(extra_world or {}))
        p = predict(tag, world(tag, W), [s_main('P0')['out'], s_main('P1')['out']])
        return verdict(tag + '_v', [s_main('P0')['out'], s_main('P1')['out'], p['out']])
    return scen(tag, go)


@check('V05', 'SV_DEPENDENT (3판 · RCA-06) — 한 모서리의 반사실 비 3.0 > 계획 문턱 2.0 → 차단 표지 · §7-1 문장 금지 (판정 이름은 그대로) · '
               '옛 SV_DOMINANT 없음')
def t_V05():
    v = (sv_set('V05', {'status': 'computed', 'ratio': 3.0})['v'] or {})
    return ('SV_DEPENDENT' in v.get('flags', []) and 'SV_DEPENDENT' in v.get('blocking_flags', []) and v.get('sentence_allowed') is False
            and 'SV_DOMINANT' not in v.get('flags', []) and 'SV_UNCHECKED' not in v.get('flags', []),
            (v.get('flags'), v.get('stop')))


@check('V06', 'SV_UNCHECKED — 한 모서리의 반사실 기록이 비를 싣지 않는 상태 (unconverged) → 못 읽음 = 차단 (§5-6 · 모르는 것을 의존 없음으로 읽지 않는다)')
def t_V06():
    v = (sv_set('V06', {'status': 'unconverged'})['v'] or {})
    return ('SV_UNCHECKED' in v.get('flags', []) and 'SV_DEPENDENT' not in v.get('flags', []) and v.get('sentence_allowed') is False,
            (v.get('flags'), v.get('stop')))


@check('V06b', 'SV 반사실 비 = 문턱 2.0 (같음) → SV_DEPENDENT 아님 (등록 문장 "넘으면") · no_through_without_sv (비 +∞) → SV_DEPENDENT')
def t_V06b():
    v1 = (sv_set('V06b1', {'status': 'computed', 'ratio': 2.0})['v'] or {})
    v2 = (sv_set('V06b2', {'status': 'no_through_without_sv'})['v'] or {})
    return ('SV_DEPENDENT' not in v1.get('flags', ['?']) and 'SV_UNCHECKED' not in v1.get('flags', ['?'])
            and 'SV_DEPENDENT' in v2.get('flags', []), (v1.get('flags'), v2.get('flags'), v1.get('stop'), v2.get('stop')))


@check('V25', '★ 10-22 SV 괄호 걸침 (PRE2-impl-01 · Q1 (다)) — 가짜 러너 기록 (못 가른 덩어리 1 · 아래 끝 1.0 = 덩어리 그대로 · 위 끝 no_through = +∞) '
               '→ 실제 검증기 · chain_view · sv_assess → SV_UNCHECKED (옛 = 표지 없음 · PASS 문장 가능) · SV_DEPENDENT 아님 · §7-1 문장 금지 · '
               '사유 = 걸침 · 모서리 (비 값 없음)')
def t_V25():
    v = (sv_set('V25', {'status': 'computed', 'ratio': 1.0, 'n_unsplit': 1, 'status_hi': 'no_through_without_sv'})['v'] or {})
    why = str((v.get('blocking_reasons') or {}).get('SV_UNCHECKED', ''))
    return ('SV_UNCHECKED' in v.get('flags', []) and 'SV_UNCHECKED' in v.get('blocking_flags', []) and 'SV_DEPENDENT' not in v.get('flags', [])
            and v.get('sentence_allowed') is False and '걸침' in why and 'c1_P1_R_j0' in why and '∞' not in why,
            (v.get('flags'), why, v.get('stop')))


@check('V26', '★ 10-22 SV 괄호가 문턱 아래 (못 가른 덩어리 1 · [1.2, 1.5] · 문턱 2.0) → SV 표지 없음 (위 끝 ≤ 문턱 = 참 비도 문턱 아래)')
def t_V26():
    v = (sv_set('V26', {'status': 'computed', 'ratio': 1.2, 'n_unsplit': 1, 'status_hi': 'computed', 'ratio_hi': 1.5})['v'] or {})
    return ('SV_DEPENDENT' not in v.get('flags', ['?']) and 'SV_UNCHECKED' not in v.get('flags', ['?']) and v.get('stop') is None,
            (v.get('flags'), v.get('stop')))


@check('V27', '★ 10-22 SV 괄호 아래 끝이 문턱을 넘음 (못 가른 덩어리 1 · [3.0, 9.0]) → SV_DEPENDENT (위 끝과 무관) · SV_UNCHECKED 아님')
def t_V27():
    v = (sv_set('V27', {'status': 'computed', 'ratio': 3.0, 'n_unsplit': 1, 'status_hi': 'computed', 'ratio_hi': 9.0})['v'] or {})
    return ('SV_DEPENDENT' in v.get('flags', []) and 'SV_UNCHECKED' not in v.get('flags', ['?']) and v.get('sentence_allowed') is False,
            (v.get('flags'), v.get('stop')))


@check('V07', 'CALIB_ORIGIN_SENSITIVE (P0 사다리 origin 넘음) → 판정 표지 · 문장 금지')
def t_V07():
    def go():
        l0 = scen('L19', lambda: run_L19('L19'))
        p = predict('V07_p', world('V07_p'), [l0['out'], s_main('P1')['out']])
        return verdict('V07', [l0['out'], s_main('P1')['out'], p['out']])
    v = scen('V07', go)['v']
    return ('CALIB_ORIGIN_SENSITIVE' in (v or {}).get('flags', []) and v['sentence_allowed'] is False, (v and v.get('flags')))


@check('V08', '사다리 CALIB_EDGE → 판정 = CALIB_EDGE (예측 폴더 없이 · rc 0 · 등록 결과)')
def t_V08():
    r = scen('V08', lambda: verdict('V08', [run_L10()['out'], s_main('P1')['out']]))
    return (r['rc'] == 0 and (r['v'] or {}).get('verdict') == 'CALIB_EDGE' and r['v']['calib'] == {'P0': 'CALIB_EDGE', 'P1': 'CALIBRATED'},
            (r['rc'], r['v'] and r['v'].get('verdict'), r['v'] and r['v'].get('stop')))


@check('V09', '등급 표 단위 — W 경계 (G0/2 · G0) · FAIL 거리 · 방향 · CONSISTENT_WEAK · UNINFORMATIVE · S (손계산)')
def t_V09():
    G0 = math.log(4.68 / 1.8877)
    g1 = RR.grade(4.0, 4.0 * math.exp(G0 / 2) * 0.999999)
    g2 = RR.grade(4.0, 4.0 * math.exp(G0 / 2) * 1.000001)
    g3 = RR.grade(3.0, 3.0 * math.exp(G0) * 1.000001)
    g4 = RR.grade(2.0, 3.0)
    g5 = RR.grade(5.0, 6.0)
    d4 = math.log(4.68 / 3.0)
    d5 = math.log(5.0 / 4.68)
    S5 = 1.0 - abs(math.log(4.68 / math.sqrt(30.0))) / G0
    ok = (g1['verdict'] == 'PASS_INFORMATIVE' and g2['verdict'] == 'CONSISTENT_WEAK' and g3['verdict'] == 'UNINFORMATIVE'
          and g4['verdict'] == 'FAIL' and g4['direction'] == 'above' and rel(g4['d'], d4) < 1e-12 and rel(g4['d_over_G0'], d4 / G0) < 1e-12
          and g5['verdict'] == 'FAIL' and g5['direction'] == 'below' and rel(g5['d'], d5) < 1e-12 and rel(g5['S'], S5) < 1e-12
          and g5['p'] < 0)
    return ok, (g1['verdict'], g2['verdict'], g3['verdict'], g4, g5)


@check('V10', '다시 판정 (--reverify) = 같은 답 (판정 JSON · 결과 JSON 바이트 같음) · 읽기 전용')
def t_V10():
    v = s_verdict_main()
    before = {p: p.read_bytes() for p in Path(v['out']).iterdir() if p.is_file()}
    rc, so = call(['--stage', 'verdict', '--reverify', v['out'], '--registration', FX['reg_ok']])
    after = {p: p.read_bytes() for p in Path(v['out']).iterdir() if p.is_file()}
    return rc == 0 and 'REVERIFY_SAME' in so and before == after, (rc, so[-300:])


@check('V11', '다시 판정이 판정 뒤 변조를 잡는다 (팔 하나 σ 바꿈 → REVERIFY_DIFF · rc 1)')
def t_V11():
    def go():
        dirs = []
        base = Path(TD) / 'runs' / 'V11_in'
        base.mkdir(parents=True)
        for d in main_dirs():
            dst = base / Path(d).name
            shutil.copytree(d, dst)
            dirs.append(dst)
        v = verdict('V11', dirs)
        s = json.loads((dirs[2] / 'predict_summary.json').read_text(encoding='utf-8'))
        run = [x for x in s['runs'] if x['role'] == 'corner'][0]
        p = dirs[2] / run['outdir'] / run['arms_read'][0]['file']
        d = json.loads(p.read_text(encoding='utf-8'))
        d['mpm_metrics']['step3']['sigma_e_eff_S_cm'] *= 1.01
        d['mpm_metrics']['step3']['conv_cert']['sigma'] *= 1.01
        p.write_text(json.dumps(d), encoding='utf-8')
        rc, so = call(['--stage', 'verdict', '--reverify', v['out'], '--registration', FX['reg_ok']])
        return {'v': v, 'rc': rc, 'so': so}
    r = scen('V11', go)
    return r['v']['rc'] == 0 and r['rc'] == 1 and 'REVERIFY_DIFF' in r['so'], (r['v']['rc'], r['rc'], r['so'][-300:])


def s_show():
    return scen('V12_ver', lambda: verdict('V12_ver', main_dirs(), extra=['--show-results']))


@check('V12', '--show-results 는 판정 단계에서만 (사다리에 주면 인자 오류) · 판정에서 열람 기록 (views.jsonl)')
def t_V12():
    w = world('V12')
    out = Path(TD) / 'runs' / 'V12_lad'
    rc1, _so = call(['--stage', 'ladder', '--law', 'P0', '--target', '1.63', '--runner', FX['runner'], '--root', FX['root'],
                     '--plan', FX['plan'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out, '--show-results']
                    + s0_args(), w)
    v = s_show()
    views = Path(v['out']) / 'views.jsonl'
    return (rc1 == 2 and n_calls(w) == 0 and v['rc'] == 0 and views.exists() and len(views.read_text().splitlines()) == 1,
            (rc1, v['rc'], views.exists()))


@check('V13', '사다리 NOT_COMPUTED (증서 실패) → 판정 = NOT_COMPUTED (등록 결과 · rc 0 · 멈춤 아님 — 실패 팔 sha256 도 기록돼 다시 계산된다)')
def t_V13():
    r = scen('V13', lambda: verdict('V13', [scen('L17', lambda: ladder('L17', world('L17', dict(
        PW, faults=[{'do': 'certfail', 'match': {'rj': '1000000.0'}}]))))['out'], s_main('P1')['out']]))
    v = r['v'] or {}
    return (r['rc'] == 0 and v.get('verdict') == 'NOT_COMPUTED' and v.get('stop') is None
            and v.get('calib') == {'P0': 'NOT_COMPUTED', 'P1': 'CALIBRATED'}, (r['rc'], v.get('verdict'), v.get('stop'), v.get('calib')))


@check('V14', '3판 — 감도 변이 = 주 판정과 같은 판정 함수 (§5-6 · RCA-09): 변이 사다리도 SBE origin (§3-3) · 끝 origin · 변이 예측도 네 모서리 × 세 R + '
               'DBE origin 세 R (§10 런 수 표 3판) · 변이 예측에는 SV 반사실 없음')
def t_V14():
    vs = s_variant_set('FIBRE')
    lads, pr = vs['ladders'], vs['pred']
    bad = [(o['sum']['law'], roles(o)) for o in lads if 'origin' not in roles(o) or (lad(o).get('origin') or {}).get('status') != 'pass']
    rl = roles(pr)
    ev = [e for e in env_log(pr['world']) if e.get('CJUNC_SV_CF') == '1']
    return (not bad and all(o['sum']['status'] == 'CALIBRATED' for o in lads) and pr['sum']['status'] == 'PREDICTED'
            and rl.count('corner') == 12 and rl.count('origin') == 12 and rl.count('sbe_noop') == 2 and not ev,
            (bad, rl, len(ev)))


@check('V15', '판정 코드 ≠ 단계 코드 (지금 사슬 HEAD 가 다르다) → CODE_PIN_MISMATCH · 판정 NOT_COMPUTED')
def t_V15():
    def go():
        dirs = main_dirs()                                  # 단계는 진짜 HEAD 로 먼저 (판정만 다른 HEAD 에서)
        orig = RR.git_identity
        RR.git_identity = lambda path: {'head': 'deadbeef' * 5, 'dirty': False}
        try:
            return verdict('V15', dirs)
        finally:
            RR.git_identity = orig
    r = scen('V15', go)
    return (r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED',
            (r['rc'], stop_code(r)))


@check('V16', '판정 결과에 수렴 증서 ⓒ 값 (런마다 Δσ/σ · §8) · 공개 판정에 §9 격자 문장 = not_computed (이 사슬 밖 · 현 세대 대조)')
def t_V16():
    v = s_verdict_main()
    names = set()
    for d in main_dirs():
        s, = [json.loads(p.read_text(encoding='utf-8')) for p in Path(d).glob('*_summary.json')]
        names |= {f'{Path(d).name}/{x["name"]}' for x in s['runs']}
    cert = (v['r'] or {}).get('certificates_dsigma_rel') or {}
    return (set(cert) == names and all(isinstance(x, list) and x and all(isinstance(y, float) for y in x) for x in cert.values())
            and (v['v'] or {}).get('grid_sentence') == 'not_computed', (len(cert), len(names), (v['v'] or {}).get('grid_sentence')))


# ── X 봉인 · 기타 ──
_NUM = re.compile(r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?')


def leaks(text, values):
    out = []
    for tok in _NUM.findall(text):
        mant = re.sub(r'[eE].*$', '', tok).lstrip('+-').replace('.', '').lstrip('0')
        if len(mant) < 4:
            continue
        x = float(tok)
        for s in values:
            for cand in (s, s * 1e3):
                if cand and abs(x - cand) <= 5e-5 * abs(cand):
                    out.append(tok)
    return out


def public_texts(dirs):
    txt = []
    for d in dirs:
        for p in Path(d).rglob('*'):
            if p.is_file() and (p.suffix == '.log' or p.name in ('ladder_summary.json', 'predict_summary.json', 'verdict.json')):
                txt.append(p.read_text(encoding='utf-8', errors='replace'))
    return txt


@check('X01', '값 봉인 — 사다리 · 예측 · 판정 (show 없이) 의 화면 · 로그 · 공개 JSON 에 σ 숫자 없음 (가짜 러너 장부 대조)')
def t_X01():
    vals = []
    for r in (s_main('P0'), s_main('P1'), s_main_predict()):
        vals += ledger(r['world'])
    v = s_verdict_main()
    texts = [s_main('P0')['so'], s_main('P1')['so'], s_main_predict()['so'], v['so']]
    texts += public_texts([s_main('P0')['out'], s_main('P1')['out'], s_main_predict()['out'], v['out']])
    bad = leaks('\n'.join(texts), vals)
    return len(vals) > 40 and not bad, (len(vals), bad[:6])


@check('X02', '--show-results 는 봉인했던 σ 를 실제로 보여준다 (봉인이 무엇을 숨겼는지의 대조)')
def t_X02():
    v = s_show()
    vals = ledger(s_main_predict()['world'])
    return bool(leaks(v['so'], vals)), (v['so'][-200:],)


@check('X03', '기본 계약 = 정본 함수 위임 (run_contract.ca_ext_record_ok · sr01_stamp_compare.check_arm)')
def t_X03():
    import run_contract as RCm
    import sr01_stamp_compare as SC
    seen = []
    o1, o2 = RCm.ca_ext_record_ok, SC.check_arm
    try:
        RCm.ca_ext_record_ok = lambda man: (seen.append('ca') or (False, 'sentinel'))
        SC.check_arm = lambda path, want, expect_backend=None, receipt=None: (seen.append(('arm', want, expect_backend)) or 'sentinel')
        c = RR.RealContract()
        a = c.ca_ext_record({'x': 1})
        b = c.arm_problem('/nonexistent.json', {'r': 1})
    finally:
        RCm.ca_ext_record_ok, SC.check_arm = o1, o2
    return a == (False, 'sentinel') and b == 'sentinel' and seen == ['ca', ('arm', 'segment', 'gpu')], (a, b, seen)


@check('X04', 'dry-run — 러너 안 부름 · 출력 폴더 없음 · 첫 다섯 런의 env 꼴 (CJUNC_RJ=inf · 0 · 10000.0 · …) · SIGMA_VGCF_OVERRIDE 없음')
def t_X04():
    w = world('X04')
    out = Path(TD) / 'runs' / 'X04'
    rc, so = call(['--stage', 'ladder', '--law', 'P0', '--target', '1.63', '--runner', FX['runner'], '--root', FX['root'],
                   '--plan', FX['plan'], '--s0-plan', FX['s0'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out,
                   '--dry-run'] + s0_args(), w)
    lines = [x for x in so.splitlines() if 'bash ' in x]
    rjs = [re.search(r'CJUNC_RJ=(\S+)', x).group(1) for x in lines if 'CJUNC_RJ=' in x]
    return (rc == 0 and not out.exists() and n_calls(w) == 0 and rjs == ['inf', '0', '10000.0', '1000000.0', '100000000.0']
            and all('PTFE_STAMP=face_alpha' in x and 'SIGMA_FIBRE_BULK=1e4' in x and 'SIGMA_VGCF_OVERRIDE' not in x for x in lines),
            (rc, rjs, lines[:1]))


@check('X05', '등록 문서에 이 도구의 숫자 · 이름 · 문장이 있다 (상수 대조 · 사본 금지의 짝)')
def t_X05():
    t = FX['reg_text']
    need = ['1.63', '4.68', '1.8877', '0.454', '0.908', '1e-3', '10^0.5', '0.02', '0.1 W', 'kit_SBE_vgcf100',
            'kit_DBE_sdcp1um_vgcf100', 'CALIB_IMPOSSIBLE', 'CALIB_EDGE', 'CALIB_UNIDENTIFIED', 'CALIB_UNCONFIRMED',
            'CALIB_NONMONOTONE', 'CALIB_LADDER_EXHAUSTED', 'NOT_COMPUTED', 'PASS_INFORMATIVE', 'CONSISTENT_WEAK', 'UNINFORMATIVE',
            'CALIB_ORIGIN_SENSITIVE', 'DIA_UNCHECKED', RR.SENTENCE_PASS,
            #  ★ 3판 — 상태 · 판정 · 표지 · 문장 · 두 계획 (등록 R §5-0 · §5-5 · §5-6a · §7-1 · §2-1)
            'VALID_ZERO_TOPOLOGY', 'GAP_ENVELOPE_ONLY', 'ASSUMED_UNVALIDATED', 'SV_DEPENDENT', 'SV_UNCHECKED', RR.SENTENCE_GAP,
            RR.SENTENCE_WEAK, 'S0 계획 해시', RR.S0_PLAN_SCHEMA, 'sv_counterfactual_ratio', *RR.BLOCKING_FLAGS]
    miss = [n for n in need if n not in t]
    consts = (RR.TARGET_SBE_MS == 1.63 and RR.EXP_DBE_MS == 4.68 and RR.CUR_GEN_DBE_MS == 1.8877 and RR.CONFIRM_TOL == 0.02
              and RR.TAU_MONO == 1e-3 and RR.NEIGHBOR_LOG10_MAX == 0.5 and not hasattr(RR, 'MAX_LADDER_POINTS')
              and RR.ORIGIN_SBE_MAX == 0.02 and RR.ORIGIN_DBE_FRAC_W == 0.1 and RR.SENS_SHIFT_FRAC_G0 == 0.1
              and RR.LADDER_START_LOG10 == (4.0, 6.0, 8.0) and RR.LADDER_EXT_LOG10 == 2.0 and RR.MAX_CONFIRM == 2
              and abs(RR.E_MIN - 0.02 / math.log(math.sqrt(10.0))) < 1e-15 and abs(RR.G0 - math.log(4.68 / 1.8877)) < 1e-15
              and len(RR.BLOCKING_FLAGS) == 11 and 'DIA_UNCHECKED' not in RR.BLOCKING_FLAGS and len(RR.QUALIFIERS) == 18
              and RR.QUALIFIERS[16:] == ('Q17_sensitivity_incomplete', 'Q18_P_two_ends_only'))
    return not miss and consts, (miss, consts, len(RR.QUALIFIERS))


@check('X05b', '★ 4판 (Q2-4 · Q2-6) 결정표 칸 글자 · ⑰ ⑱ 문장 · 보호 띠 · W₊ · 이름 우선순위가 등록 문서 (4판) 에 그대로 있다 (시험 상수 대조 · 사본 금지의 짝) · '
                '★ RI 4판 정정 — ⑱ · UNINFORMATIVE 문장이 등록에서 하나 (§5-1 = §7-1 ⑱ · §5-5 = §5-5b · 사슬 꼴)')
def t_X05b():
    t = FX['reg_text']
    need = [T_PASS, T_PASS_BLK[0].rstrip(), T_PASS_BLK[1].strip(), T_WEAK, T_UNINF, T_GAP, T_Q18, T_FAIL, T_CALIB, T_NC, T_BLK[0].strip(),
            T_POINT, T_SENS, '⑰', '⑱', 'target_err_bound_rel', 'W₊', '하나라도 `NOT_COMPUTED` 면 판정 전체 = `NOT_COMPUTED`',
            '`<V>_UNCHECKED`']
    miss = [n for n in need if n not in t]
    #  ★ RI (10-21 · 4판 정정) — 옛 §7-1 ⑱ 꼴 ('P 는 두 끝 (P0 · P1) 만 등록했다 — …') 은 이제 철회 표지 (~~ ~~) 안에만 남는다 → 그 낱말을 요구하면
    #    철회 문장으로 통과한다 (거짓 초록).  대신 사슬 꼴 문장이 두 자리 (§5-1 · §7-1 ⑱ / §5-5 표 · §5-5b) 에 다 있는지 센다.
    one = {'Q18': t.count(T_Q18), 'UNINF': t.count(T_UNINF)}
    return not miss and all(n >= 2 for n in one.values()), (miss, one)


@check('X06', '바닥 · 천장 극한 = 러너 env CJUNC_RJ=inf · 0 (런 순서 첫 둘) · 팔 protocol 표지 rj_limit inf · zero (R_j_ohm null · 0.0 · '
               'quantitative False · allow_rj_limits True) · 영수증 요청 같은 꼴 — 사슬이 받아 다음 런으로 간다')
def t_X06():
    r = s_main('P0')
    ev = env_log(r['world'])
    got = []
    for run in (r['sum'] or {}).get('runs', [])[:2]:
        d = Path(r['out']) / run['outdir']
        a = json.loads((d / run['arms_read'][0]['file']).read_text(encoding='utf-8'))
        cjp = a['mpm_metrics']['step3']['manifest']['ca_ext']['cjunc']['protocol']
        rq = json.loads((d / 'run_receipt.json').read_text(encoding='utf-8'))['ca_ext_request']['cjunc']
        got.append((cjp.get('rj_limit'), cjp.get('R_j_ohm'), cjp.get('quantitative'), cjp.get('allow_rj_limits'),
                    rq.get('rj_limit'), rq.get('R_j_ohm')))
    return ([e.get('CJUNC_RJ') for e in ev[:2]] == ['inf', '0'] and roles(r)[:2] == ['floor', 'ceiling'] and len(roles(r)) > 2
            and got == [('inf', None, False, True, 'inf', None), ('zero', 0.0, False, True, 'zero', 0.0)],
            ([e.get('CJUNC_RJ') for e in ev[:3]], got, stop_code(r)))


@check('X07', '극한 표지 = 정본 낱말 (ca_ext_cjunc.RJ_LIMITS) · 사슬이 기대하는 요청 (expected_request) 에 rj_limit · R_j null · 0.0 · 정량 런엔 칸 없음')
def t_X07():
    import ca_ext_cjunc as CW
    mk = getattr(RR, 'LIMIT_MARK', None)
    plan = FX['plan_obj']
    reqs = {}
    for rj in ('inf', '0', '1000000.0'):
        reqs[rj] = RR.expected_request({'rj': rj, 'law': 'P0', 'c': '0', 'variant': None}, plan)['cjunc']
    ok = (isinstance(mk, dict) and set(mk) == {'inf', '0'} and set(mk.values()) == set(CW.RJ_LIMITS)
          and reqs['inf'].get('rj_limit') == mk['inf'] and reqs['inf'].get('R_j_ohm') is None
          and reqs['0'].get('rj_limit') == mk['0'] and reqs['0'].get('R_j_ohm') == 0.0
          and 'rj_limit' not in reqs['1000000.0'] and reqs['1000000.0'].get('R_j_ohm') == 1e6)
    return ok, (mk, reqs)


@check('X08', '러너 backend = 사슬 상수 EXPECT_BACKEND (gpu) — env 로 넘긴다 (부모 셸 값은 지운다) · 정본 check_arm 에도 같은 값')
def t_X08():
    w = world('X08')
    out = Path(TD) / 'runs' / 'X08'
    rc, so = call(['--stage', 'ladder', '--law', 'P0', '--target', '1.63', '--runner', FX['runner'], '--root', FX['root'],
                   '--plan', FX['plan'], '--s0-plan', FX['s0'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out,
                   '--dry-run'] + s0_args(), w, env={'EXPECT_BACKEND': 'cpu'})
    lines = [x for x in so.splitlines() if 'bash ' in x]
    return (rc == 0 and getattr(RR, 'EXPECT_BACKEND', None) == 'gpu' and len(lines) == 5
            and all('EXPECT_BACKEND=gpu' in x and 'EXPECT_BACKEND=cpu' not in x for x in lines), (rc, lines[:1]))


@check('X09', '사슬 자신의 off 격자 대조 — 정본 계약을 비켜도 (통과 계약) sid_off 없음 · ≠ 접합 sid = SID_GRID (계약 뒤 둘째 겹)')
def t_X09():
    rs = []
    for tag, do in (('X09a', 'no_sid_off'), ('X09b', 'sid_off_other')):
        r = scen(tag, lambda tag=tag, do=do: ladder(tag, world(tag, dict(PW, faults=[{'do': do, 'match': {'rj': '1000000.0'}}])),
                                                   contract=pass_contract()))
        rs.append((r['rc'], stop_code(r)))
    return rs == [(3, 'SID_GRID'), (3, 'SID_GRID')], rs


@check('X10', 'CG 반복 수 (주 솔브 · ⓒ 이어 풀기) = 공개 기록 · 화면 (등록 R §11 숫자 탐침 칸 · σ 아님)')
def t_X10():
    r = s_main('P0')
    ar = [a for run in (r['sum'] or {}).get('runs', []) for a in (run.get('arms_read') or [])]
    return (bool(ar) and all(a.get('cg_iters') == 321 and a.get('resolve_iters') == 17 for a in ar)
            and 'CG 반복 321' in r['so'] and '이어 풀기 17' in r['so'], ([(a.get('cg_iters'), a.get('resolve_iters')) for a in ar[:3]],
                                                                     r['so'][-300:]))


# ── U 3판 손 회로 · 판정 함수 (등록 R 3판 · Codex 반례 · 사전 리뷰 · 가짜 러너 없이 사슬 함수를 직접) ──
def _arms_of(arms):
    return list(range(arms)) if isinstance(arms, int) else list(arms)


def ladder_fetch(S_mS, err=0.0, read=1.0):
    """Ladder 의 fetch — S_mS(R [Ω], 팔 번호) [mS/cm] → 팔 기록 (S/cm · 상태 positive).  ★ 4판 (Q2-2 · §3-2b ③″) — err = 그 런 증서의
    보장 오차 (`err_rel` · 사슬 read_run 이 증서에서 다시 계산해 싣는 칸) · read = 판독 배수 (증서 허용 안의 낮은 판독 · 반례)."""
    def fetch(role, key, arms):
        R = RR.rj_float(key)
        return [{'sigma': S_mS(R, i) * 1e-3 * read, 'state': 'positive', 'err_rel': err} for i in _arms_of(arms)]
    return fetch


RCA01_SCALE = 10 ** 4.75


def rca01_S(R, i=0):
    """Codex RCA-01 양의 저항망 SBE — S = 1.597 + 0.0363/(r + 0.1) mS/cm · r = R_j/10^4.75 Ω (origin 무관)."""
    return 1.597 if R == math.inf else 1.597 + 0.0363 / (R / RCA01_SCALE + 0.1)


def rca01_D(R):
    return 3.0 + 1.0 / (R / RCA01_SCALE + 0.1)


#: 사전 리뷰 PRE-design-05 의 기대값 = 등록 규칙 (§3-2b) 의 정확한 출력 (probe_registration_v3.json 'a_rca01')
RCA01_WANT = {'R0': 64000.0, 'R_lo': 10000.0, 'R_hi': 5990349.747386915, 'ratio': 599.0349747386915, 'n_points': 12,
              'e': 0.01885983292807937, 'W': 0.7852375308170946, 'D_lo': 3.009378649805871, 'D_hi': 6.599350001971149,
              'true_lo': 25493.94971213578, 'true_hi': 5097624.112852485, 'cand_lo': 26758.370822762055}


def run_U01():
    lad_ = RR.Ladder(ladder_fetch(rca01_S), max_points=12, ratio_max='none')
    lad_.run()
    lad_.origin()
    st = lad_.st
    R = {k: RR.rj_float(st[k]) for k in ('R_j_lo', 'R_j0', 'R_j_hi')}
    J = RR.judge({('0', 'P0', k): rca01_D(v) for k, v in R.items()})
    return lad_, R, J


def eval_U01():
    lad_, R, J = run_U01()
    st, w = lad_.st, RCA01_WANT
    ok = (R['R_j0'] == w['R0'] and R['R_j_lo'] == w['R_lo'] and rel(R['R_j_hi'], w['R_hi']) < 1e-9
          and rel(st['R_ratio'], w['ratio']) < 1e-9 and st['n_runs'] == w['n_points'] and st['local_e_ge_emin'] is True
          and rel(lad_.sealed['e'], w['e']) < 1e-9
          and st['ends']['lo']['source'] == 'outer_neighbor' and rel(float(st['ends']['lo']['candidate']), w['cand_lo']) < 1e-9
          and st['ends']['hi']['source'] == 'candidate'
          and R['R_j_lo'] <= w['true_lo'] and R['R_j_hi'] >= w['true_hi']                     # 성질 — 참 허용집합 바깥 감쌈
          and J['verdict'] == 'CONSISTENT_WEAK' and rel(J['W'], w['W']) < 1e-9
          and rel(J['interval_mScm'][0], w['D_lo']) < 1e-9 and rel(J['interval_mScm'][1], w['D_hi']) < 1e-9)
    return ok, (R, st.get('R_ratio'), st.get('n_runs'), J.get('verdict'), J.get('W'), st.get('ends'))


@check('U01', 'RCA-01 (§3-2b ⑧ · PRE-design-05) — Codex 양의 저항망: 끝 = 실제 역상 · R_lo 10,000 (후보 26,758 확인 실패 → 바깥 실측 이웃) · '
               'R_hi 5,990,349.75 (후보 확인) · R 비 599.03 · 12 점 · 참 [25,494 · 5,097,624] 바깥 감쌈 · DBE W 0.785238 CONSISTENT_WEAK '
               '(2판 보간 = PASS W 0.419)')
def t_U01():
    return eval_U01()


def rca02_fetch(kit, role, law, c, rj, arms, sv_cf=False):
    """Codex RCA-02 — DBE arm 0 = 3.02 + 1/(r + 0.1) · arm 1–7 = 1.02 + 3.2/(r + 0.1) (r = 1 에서 모두 3.9290909) · SBE no-op = 사다리 값."""
    if kit == SBE_KIT:
        return [{'sigma': 1.63e-3, 'n_sdcp_near': 0, 'state': 'positive'}]
    r = float(rj)
    a0, oth = 3.02 + 1.0 / (r + 0.1), 1.02 + 3.2 / (r + 0.1)
    return [{'sigma': (a0 if i == 0 else oth) * 1e-3, 'state': 'positive', 'n_sdcp_near': 7} for i in _arms_of(arms)]


def eval_U02():
    lads = {law: {'R_j_lo': '0.5', 'R_j0': '1.0', 'R_j_hi': '2.0', 'r0_sigma': 1.63e-3} for law in ('P0', 'P1')}
    pr = RR.Predict(rca02_fetch, lads, None, sv_scope=None)
    pr.run()
    J = RR.judge({k: v * 1e3 for k, v in pr.values().items()})
    ok = (J['verdict'] == 'CONSISTENT_WEAK' and rel(J['interval_mScm'][0], 2.662857142857143) < 1e-12
          and rel(J['interval_mScm'][1], 6.1450000000000005) < 1e-12 and rel(J['W'], 0.8362390828158665) < 1e-12
          and all(o['status'] == 'adjusted' and o['per_R'] == {'R_j_lo': 'over', 'R_j0': 'pass', 'R_j_hi': 'over'} for o in pr.origin))
    return ok, (J.get('verdict'), J.get('interval_mScm'), J.get('W'), pr.origin[:1])


@check('U02', 'RCA-02 (§4-2 3판) — 중앙 (R_j,0) 산포 0 인데 양끝 origin 산포 0.304 · 0.318 > 0.1 W → 모서리마다 세 R 전부 8 팔 평균 → '
               '[2.6629, 6.1450] W 0.8362 CONSISTENT_WEAK (2판 = R_j,0 만 점검 · arm 0 [3.4962, 4.6867] PASS)')
def t_U02():
    return eval_U02()


#: ★ 4판 (Q2-4 · 등록 R 4판 §5-5b 결정표 · §5-1 · §7-1 ⑰ ⑱) — 칸 글자 (시험 상수 · 사슬 상수를 베끼지 않는다 · 등록 문서 대조 = X05b)
T_PASS = ('SBE 측정 한 점으로 각 법칙의 내부 접합 저항을 보정하였다. 사전에 고정한 시나리오와 보정 허용집합의 계산 결과를 이미 알려진 '
          'DBE 측정값과 비교하였다. 모형 종류와 시나리오 방향은 해당 DBE 값 및 기존 빗나감을 알고 선정했으므로, 이 비교는 독립 '
          'holdout 검증이나 접합 물성의 식별이 아니다.')
T_PASS_BLK = ('계산기 판정 이름 `PASS_INFORMATIVE` · 차단 표지 ', ' — 판정 문장 보류')
T_WEAK = '넓은 시나리오 구간 안에 들었다'
T_UNINF = '예측 주장 없음 (구간이 현 세대 빗나감보다 넓다)'
T_GAP = '어느 법칙의 허용집합에도 포함되지 않았으나 전체 envelope 에는 포함'
T_Q18 = 'P 는 두 끝만 등록했다 (사이 감쇠는 모형 밖)'
T_FAIL = '빗나감 d · d/G0 · 방향 · §8 보고 (해석 금지 §8)'
T_CALIB = '판정 없음 — 법칙별 이름 · 사유 · 바닥 · 천장 · e · 끝 후보 보고'
T_NC = '판정 없음 — 사유 (상태 · 멈춤 코드) 보고'
T_BLK = ('(차단 표지 ', ')')
T_POINT = '점 구간'
T_SENS = '감도 미완료'
REG_CALIB6 = ('CALIB_IMPOSSIBLE', 'CALIB_EDGE', 'CALIB_UNIDENTIFIED', 'CALIB_UNCONFIRMED', 'CALIB_NONMONOTONE', 'CALIB_LADDER_EXHAUSTED')


def want_sentence(state, verdict, blocking=(), sens=False):
    """등록 R 4판 §5-5b 결정표의 칸 하나 (시험 쪽 독립 조립) — 차단 표지 목록 = 사전 순 · ' · ' 로 잇는다 · 오른쪽 칸 = 왼쪽 칸 + 공백 + "(차단 표지 <목록>)"
    (PASS = 헤드라인 대신 "계산기 판정 이름 …" ) · GAP = 판정문 §5-3 문안 + ⑱ · 점 구간 · 감도 미완료 (⑰) = 결과 문장 끝에 ' · ' 로 덧붙인다 ·
    CALIB_* · NOT_COMPUTED = 판정 없음 칸 (차단 표지 · 점 · 감도 해당 없음)."""
    if verdict in REG_CALIB6:
        return T_CALIB
    if verdict == 'NOT_COMPUTED':
        return T_NC
    lst = ' · '.join(sorted(set(blocking)))
    base = {'PASS_INFORMATIVE': T_PASS, 'CONSISTENT_WEAK': T_WEAK, 'UNINFORMATIVE': T_UNINF, 'GAP_ENVELOPE_ONLY': T_GAP + ' · ' + T_Q18,
            'FAIL': T_FAIL}[verdict]
    if blocking:
        s = (T_PASS_BLK[0] + lst + T_PASS_BLK[1]) if verdict == 'PASS_INFORMATIVE' else base + ' ' + T_BLK[0] + lst + T_BLK[1]
    else:
        s = base
    if state == 'point':
        s += ' · ' + T_POINT
    if sens:
        s += ' · ' + T_SENS
    return s


def rca08_vals():
    v = {}
    for c in ('0', '1'):
        for rr, a, b in (('R_j_lo', 4.0, 5.4), ('R_j0', 3.9, 5.3), ('R_j_hi', 3.8, 5.2)):
            v[(c, 'P0', rr)], v[(c, 'P1', rr)] = a, b
    return v


def eval_U03():
    J = RR.judge(rca08_vals())
    s = RR.decide_sentence(J['state'], J['verdict'], [])
    ok = (J['verdict'] == 'GAP_ENVELOPE_ONLY' and J['in_law'] == [] and J['in_E'] is True and J['in_U'] is False
          and J['I_law_mScm'] == {'P0': [3.8, 4.0], 'P1': [5.2, 5.4]} and J['direction'] == 'gap' and J['d'] == 0.0
          and rel(J['W'], 0.3513978868378886) < 1e-9 and s == T_GAP + ' · ' + T_Q18 and rel(J['d_to_U'], math.log(5.2 / 4.68)) < 1e-12)
    return ok, (J.get('verdict'), J.get('in_law'), J.get('W'), s)


@check('U03', 'RCA-08 (§5-1 · §5-5 3판) — I_P0 [3.8, 4.0] · I_P1 [5.2, 5.4] · 4.68 = E ∖ U → GAP_ENVELOPE_ONLY (2판 hull W 0.351 = PASS) · '
               '문장 = 판정문 §5-3 GAP 문안 + ★ 4판 ⑱ (§5-1 · §5-5b "P 는 두 끝만 등록했다 (사이 감쇠는 모형 밖)") · 법칙 집합까지 ln 거리 기록')
def t_U03():
    return eval_U03()


def rca09_main():
    v = {}
    for (c, law), (lo, mid, hi) in {('0', 'P0'): (4.45, 4.40, 4.30), ('1', 'P0'): (4.50, 4.45, 4.40), ('0', 'P1'): (4.55, 4.50, 4.45),
                                    ('1', 'P1'): (4.80, 4.55, 4.50)}.items():
        v[(c, law, 'R_j_lo')], v[(c, law, 'R_j0')], v[(c, law, 'R_j_hi')] = lo * 1e-3, mid * 1e-3, hi * 1e-3
    return v


CAL2 = {'P0': 'CALIBRATED', 'P1': 'CALIBRATED'}


def eval_U04(which):
    main = {'statuses': CAL2, 'vals': rca09_main(), 'flags': []}
    if which == 'noop':
        vv = dict(main['vals'])
    else:
        vv = {k: (v if k[2] == 'R_j0' else (7.0e-3 if k[2] == 'R_j_lo' else 3.0e-3)) for k, v in main['vals'].items()}
    var = {'statuses': CAL2, 'vals': vv, 'flags': []}
    pub, res = RR.assemble(main, {'FIBRE': var, 'UNREG': dict(main), 'GRID': dict(main), 'SVORDER': dict(main)}, ([], {}))
    if which == 'noop':
        return (pub['verdict'] == 'PASS_INFORMATIVE' and 'FIBRE_SENSITIVE' not in pub['flags'] and pub['flags'] == []
                and pub['sentence'] == RR.SENTENCE_PASS, (pub['verdict'], pub['flags'], res['judge'].get('W')))
    return (pub['verdict'] == 'PASS_INFORMATIVE' and 'FIBRE_SENSITIVE' in pub['flags'] and pub['sentence_allowed'] is False
            and res['variants']['FIBRE']['verdict'] == 'CONSISTENT_WEAK', (pub['verdict'], pub['flags'], res['variants'].get('FIBRE')))


@check('U04', 'RCA-09 (§5-6 3판) — 같은 판정 함수: 주 판정 (허용폭 포함 [4.30, 4.80] W 0.110 PASS) ↔ 엄밀한 no-op 변이 = PASS 그대로 '
               '(중앙 네 점만 판정하면 W 0.0335 FAIL = 거짓 SENSITIVE) · 표지 없음 · §7-1 문장')
def t_U04():
    return eval_U04('noop')


@check('U04b', 'RCA-09 같은 부류 — 변이가 중앙 네 점은 같고 양끝만 넓다 ([3.0, 7.0]) → 같은 판정 함수 = CONSISTENT_WEAK ≠ PASS → FIBRE_SENSITIVE '
                '(2판 = 중앙 네 점끼리 비교 → 둘 다 FAIL → 놓침)')
def t_U04b():
    return eval_U04('wide')


def eval_U05():
    nb = RR.blocking_of(['DIA_UNCHECKED', 'XYZ_UNCHECKED', 'FOO_SENSITIVE', 'SV_DOMINANT', 'Q9_ptfe_diameter_convention'])
    each = all(RR.blocking_of([f, 'DIA_UNCHECKED']) == [f] for f in RR.BLOCKING_FLAGS)
    s = RR.decide_sentence('positive', 'PASS_INFORMATIVE', RR.blocking_of(['DIA_UNCHECKED']))
    return nb == [] and each and s == T_PASS and len(RR.BLOCKING_FLAGS) == 11, (nb, each, s)


@check('U05', 'RCA-10 (§5-6a) — 차단 표지 = 닫힌 집합 11 · DIA_UNCHECKED · 모르는 *_UNCHECKED · *_SENSITIVE · 옛 SV_DOMINANT = 차단 아님 · '
               '닫힌 집합 이름 하나하나 = 차단 · DIA 만 있으면 PASS 문장 허용')
def t_U05():
    return eval_U05()


def _judge_close(a, b):
    for k in ('verdict', 'state', 'in_law', 'in_U', 'in_E', 'direction', 'p_why', 'S_why'):
        if a[k] != b[k]:
            return False
    for k in ('W', 'p', 'd', 'd_over_G0', 'S', 'd_to_U'):
        x, y = a[k], b[k]
        if (x is None) != (y is None) or (x is not None and not (x == y or (math.isfinite(x) and rel(x, y) < 1e-12))):
            return False
    return True


def eval_U06():
    cases = {'pass': {k: v * 1e3 for k, v in rca09_main().items()}, 'gap': rca08_vals(), 'weak': None}
    cases['weak'] = {k: (v if k[2] != 'R_j_lo' else 7.0) for k, v in cases['pass'].items()}
    bad = []
    for nm, vals in cases.items():
        a = RR.judge(vals)
        b = RR.judge({k: v * 1e-3 for k, v in vals.items()}, x=4.68e-3, ref=1.8877e-3)
        if not _judge_close(a, b):
            bad.append(f'단위 [{nm}] {a["verdict"]} ↔ {b["verdict"]}')
    #  τ_mono = ln σ 차 — 1000 → 999.5 mS/cm 를 절대차 (0.5) 로 재면 거부 · 같은 양 S/cm (0.0005) 는 통과 = 쓰지 않는다 (판정문 RCA-13)
    for scale in (1.0, 1e-3):
        lad_ = RR.Ladder(lambda *a: None, max_points=4)
        lad_.pts = {'1.0': (1.0, 999.5 * scale), '2.0': (2.0, 1000.0 * scale)}
        try:
            lad_._monotone()
        except RR.Stop as e:
            bad.append(f'평탄 ({scale}) 을 비단조로 {e.code}')
        lad_.pts = {'1.0': (1.0, 999.0 * scale), '2.0': (2.0, 1000.0 * scale)}      # ln 차 1.0005e-3 > τ_mono
        try:
            lad_._monotone()
            bad.append(f'비단조 ({scale}) 를 놓침')
        except RR.Stop as e:
            if e.code != 'CALIB_NONMONOTONE':
                bad.append(e.code)
    if not (RR.ln_diff(999.5, 1000.0) == RR.ln_diff(999.5e-3, 1000.0e-3) or rel(RR.ln_diff(999.5, 1000.0), RR.ln_diff(0.9995, 1.0)) < 1e-9):
        bad.append('ln_diff 단위 의존')
    #  0/0 · 점 · 확장 실수 끝 (§5-0 ③ ④ · 예외 없이)
    one = lambda v: {(c, law, rr): v for c in ('0', '1') for law in ('P0', 'P1') for rr in ('R_j_lo', 'R_j0', 'R_j_hi')}   # noqa: E731
    Jp = RR.judge(one(4.68))
    Jf = RR.judge(one(3.0))
    Jz = RR.judge(one(0.0))
    Ji = RR.judge(one(math.inf))
    mix = one(5.0)
    mix[('0', 'P0', 'R_j_hi')] = 0.0
    Jm = RR.judge(mix)
    gz = {k: (0.0 if k[1] == 'P0' else math.inf) for k in one(1.0)}
    Jg = RR.judge(gz)
    tbl = [(Jp, ('PASS_INFORMATIVE', 'point', 0.0, None)), (Jf, ('FAIL', 'point', 0.0, None)),
           (Jz, ('FAIL', 'extended', math.inf, None)), (Ji, ('FAIL', 'extended', math.inf, None)),
           (Jm, ('UNINFORMATIVE', 'extended', math.inf, None)), (Jg, ('GAP_ENVELOPE_ONLY', 'extended', math.inf, None))]
    for J, (v, s, W, p) in tbl:
        if (J['verdict'], J['state'], J['W'], J['p']) != (v, s, W, p):
            bad.append(f'{J["verdict"]}/{J["state"]}/{J["W"]}/{J["p"]} ≠ {v}/{s}/{W}/{p}')
    if not (Jz['d'] == math.inf and Jz['direction'] == 'above' and Ji['d'] == math.inf and Ji['direction'] == 'below'
            and Jz['S'] is None and Jm['S'] is None and Jp['S'] is not None and Jf['p'] is None
            and rel(Jf['d'], math.log(4.68 / 3.0)) < 1e-12):
        bad.append(f'끝 거리 · 방향 · S {Jz["d"]} {Jz["direction"]} {Ji["direction"]} {Jz["S"]}')
    #  ★ 4판 (Q2-3 · §4-2 PRE-design-10) — W 가 +∞ · 0 이면 문턱의 W = W₊ (arm 0 양수 값의 폭 · 없으면 0 = 문턱 0 · 보수 쪽) · 세 origin 상태가
    #    다르면 = 넘음 (3판 = W +∞ → 문턱 +∞ → 늘 통과)
    try:
        dob = (RR.dbe_origin_ok([0.0, 0.0, 0.0], 0.0) == (True, 0.0) and RR.dbe_origin_ok([1.0, 2.0], math.inf)[0] is False
               and RR.dbe_origin_ok([1.0, 2.0], math.inf, w_pos=10.0)[0] is True
               and RR.dbe_origin_ok([1.0, 1.0, 1.0], 0.0, states=['zero', 'positive', 'positive'])[0] is False
               and RR.dbe_origin_ok([3.0, 3.0, 3.0], 0.5, states=['positive'] * 3) == (True, 0.0))
    except TypeError as e:
        dob = False
        bad.append(f'dbe_origin_ok 4판 인자 {e}')
    if not (RR.ln_spread([0.0, 0.0, 0.0]) == 0.0 and RR.ln_spread([0.0, 1.0]) == math.inf and RR.ln_spread([math.inf, math.inf]) == 0.0
            and dob and RR.mean_ext([1.0, math.inf]) == math.inf):
        bad.append('확장 실수 도구')
    return not bad, bad


@check('U06', 'RCA-13 (§5-0 · §3-2) — 단위 불변 (S/cm ↔ mS/cm · 판정 · W · p · d · S) · τ_mono = ln 차 (999.5 → 1000 평탄 · 999 → 1000 비단조 · '
               '두 단위 같음) · 0/0 · 점 구간 (W 0 · p null) · zero 끝 (W +∞ · p · S null · d +∞ 방향 · ★ 4판 단락은 판정에 오지 않는다 — +∞ 값은 '
               '도구만) · gap · 확장 실수 도구 (★ 4판 dbe_origin_ok — W₊ · 상태 다름 = 넘음)')
def t_U06():
    return eval_U06()


U07_BLK = ['SV_DEPENDENT', 'FIBRE_UNCHECKED']                 # 차단 표지 둘 (순서 섞음 — <목록> = 사전 순)
ALLOWED = {('positive', v) for v in ('PASS_INFORMATIVE', 'CONSISTENT_WEAK', 'UNINFORMATIVE', 'GAP_ENVELOPE_ONLY', 'FAIL')} | {
    ('point', 'PASS_INFORMATIVE'), ('point', 'FAIL'), ('extended', 'UNINFORMATIVE'), ('extended', 'GAP_ENVELOPE_ONLY'), ('extended', 'FAIL')} | {
    ('calib', c) for c in REG_CALIB6 + ('NOT_COMPUTED',)}


def eval_U07():
    """★ 4판 (Q2-4 · 등록 R 4판 §5-5b) — 결정표 전수: (상태 4 × 판정 12) × 차단 {없음 · 둘} × 감도 미완료 {아님 · 맞음} → 칸 글자 하나 (등록 표 그대로 ·
    시험 쪽 독립 조립 `want_sentence`) · 짝이 안 맞는 상태 · 이름 = ValueError · 차단 목록에 닫힌 집합 밖 이름 · bool = 구현 결함 (ValueError)."""
    bad, n_ok, n_bad = [], 0, 0
    names = ('PASS_INFORMATIVE', 'CONSISTENT_WEAK', 'UNINFORMATIVE', 'GAP_ENVELOPE_ONLY', 'FAIL') + REG_CALIB6 + ('NOT_COMPUTED',)
    for st in ('positive', 'point', 'extended', 'calib'):
        for v in names:
            for blk in ([], list(U07_BLK)):
                for sens in (False, True):
                    try:
                        got = RR.decide_sentence(st, v, blk, sens_incomplete=sens)
                        if (st, v) not in ALLOWED or got != want_sentence(st, v, blk, sens):
                            bad.append((st, v, blk, sens, got))
                        n_ok += 1
                    except (ValueError, TypeError) as e:
                        if (st, v) in ALLOWED:
                            bad.append((st, v, blk, sens, f'{type(e).__name__}: {e}'))
                        n_bad += 1
    for wrong in (['DIA_UNCHECKED'], ['XYZ_UNCHECKED'], True, False):
        try:
            RR.decide_sentence('positive', 'PASS_INFORMATIVE', wrong)
            bad.append(('닫힌 집합 밖 · bool 을 받았다', wrong))
        except (ValueError, TypeError):
            pass
    return not bad and n_ok == 4 * len(ALLOWED) and n_ok + n_bad == 4 * 12 * 2 * 2, (bad[:4], n_ok, n_bad)


@check('U07', '★ 4판 결정표 (§5-5b · PRE-design-09 · R4-Q7) 전수 — (상태 4 × 판정 12) × 차단 {없음 · 둘} × 감도 미완료 = 칸 글자 하나: PASS = §7-1 헤드라인 · '
               '차단 = "계산기 판정 이름 `PASS_INFORMATIVE` · 차단 표지 <목록> — 판정 문장 보류" · WEAK · UNINF · GAP (+ ⑱) · FAIL = 왼쪽 칸 + '
               '"(차단 표지 <목록>)" · CALIB_* · NOT_COMPUTED = 판정 없음 칸 · 점 구간 · 감도 미완료 (⑰) 덧붙임 · 허용 짝 17 · 짝 밖 · 닫힌 집합 밖 = '
               'ValueError (3판 = 차단 PASS · UNINF · FAIL · CALIB 문장 없음)')
def t_U07():
    return eval_U07()


def eval_U08():
    def rec(st, r):                                    # ★ 10-22 (Q1 (다)) chain_view 꼴 — 못 가른 덩어리 0 = 위 끝 = 아래 끝
        return {'sv_cf': {'status': st, 'ratio': r, 'status_hi': st, 'ratio_hi': r, 'n_unsplit': 0}}
    base = {(c, law, rr): rec('computed', 1.2) for c in ('0', '1') for law in ('P0', 'P1') for rr in ('R_j_lo', 'R_j0', 'R_j_hi')}
    cases = []
    for nm, upd, thr, scope, want in (
            ('비 1.2 < 2', {}, 2.0, 'R_j0', []),
            ('비 = 문턱 (넘지 않음)', {('1', 'P1', 'R_j0'): rec('computed', 2.0)}, 2.0, 'R_j0', []),
            ('비 2.0000001 > 2', {('1', 'P1', 'R_j0'): rec('computed', 2.0000001)}, 2.0, 'R_j0', ['SV_DEPENDENT']),
            ('비 +∞ (위상)', {('0', 'P0', 'R_j0'): rec('no_through_without_sv', math.inf)}, 2.0, 'R_j0', ['SV_DEPENDENT']),
            ('미수렴 (비 없음)', {('0', 'P1', 'R_j0'): rec('unconverged', None)}, 2.0, 'R_j0', ['SV_UNCHECKED']),
            ('기록 없음 (조기 반환 모서리)', {('0', 'P1', 'R_j0'): {'sv_cf': None}}, 2.0, 'R_j0', ['SV_UNCHECKED']),
            ('범위 밖 모서리의 큰 비 (R_j0 범위)', {('1', 'P1', 'R_j_hi'): rec('computed', 9.0)}, 2.0, 'R_j0', []),
            ('범위 all3 — 같은 큰 비', {('1', 'P1', 'R_j_hi'): rec('computed', 9.0)}, 2.0, 'all3', ['SV_DEPENDENT']),
            ('문턱 없음 (null)', {}, None, 'R_j0', ['SV_UNCHECKED'])):
        r = dict(base)
        r.update(upd)
        f, d = RR.sv_assess(r, thr, scope)
        cases.append((nm, sorted(f) == sorted(want), f, len(d['corners'])))
    n_scope = {s: len(RR.sv_assess(base, 2.0, s)[1]['corners']) for s in ('R_j0', 'all3')}
    return all(c[1] for c in cases) and n_scope == {'R_j0': 4, 'all3': 12}, ([c for c in cases if not c[1]], n_scope)


@check('U08', 'SV 반사실 판정 (§5-6 SV 행 · RCA-06) — 비 > 문턱 = SV_DEPENDENT (= 문턱 은 아님 · "넘으면") · 비 +∞ = 의존 · 비 없는 상태 · 기록 없음 · '
               '문턱 null = SV_UNCHECKED · 범위 R_j0 (모서리 넷) ↔ all3 (열둘)')
def t_U08():
    return eval_U08()


def eval_U08b():
    """★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 1저자 Q1 (다) · 등록 R §5-6 SV 행 개정) — 괄호 판정.  모서리마다 아래 끝 (덩어리 그대로) ·
    위 끝 (못 가른 덩어리를 통째로 뺀 판): 아래 > 문턱 = 의존 · (두 끝을 읽고) 위 ≤ 문턱 = 표지 없음 · 그 밖 (걸침 · 못 읽음) = SV_UNCHECKED ·
    비교 = 지금 SV 비교 그대로 (증서 여유 없음 · 두 끝 같게) · 모서리 묶기 = 지금 규칙 그대로 (하나라도 의존 → SV_DEPENDENT · 하나라도
    걸침 · 못 읽음 → SV_UNCHECKED · 둘 다 붙을 수 있다)."""
    def rec(lo, hi, nu=1, st='computed', sh='computed'):
        return {'sv_cf': {'status': st, 'ratio': lo, 'status_hi': sh, 'ratio_hi': hi, 'n_unsplit': nu}}
    base = {(c, law, rr): rec(1.2, 1.2, 0) for c in ('0', '1') for law in ('P0', 'P1') for rr in ('R_j_lo', 'R_j0', 'R_j_hi')}
    k1, k2 = ('1', 'P1', 'R_j0'), ('0', 'P0', 'R_j0')
    cases = []
    for nm, upd, want, det_key in (
            ('괄호 [1.0, ∞] (리뷰어 꼴 · 걸침)', {k1: rec(1.0, math.inf, sh='no_through_without_sv')}, ['SV_UNCHECKED'], 'straddle'),
            ('괄호 [1.2, 1.5] (위 ≤ 문턱)', {k1: rec(1.2, 1.5)}, [], None),
            ('괄호 [1.2, 2.0] (위 = 문턱 · 넘지 않음)', {k1: rec(1.2, 2.0)}, [], None),
            ('괄호 [1.5, 2.0000001] (위가 문턱을 조금 넘음 · 걸침)', {k1: rec(1.5, 2.0000001)}, ['SV_UNCHECKED'], 'straddle'),
            ('괄호 [2.0000001, 9.0] (아래 > 문턱)', {k1: rec(2.0000001, 9.0)}, ['SV_DEPENDENT'], 'dependent'),
            ('괄호 [2.0, 9.0] (아래 = 문턱 · 넘지 않음 → 걸침)', {k1: rec(2.0, 9.0)}, ['SV_UNCHECKED'], 'straddle'),
            ('괄호 [3.0, 위 못 읽음] (아래만으로 의존)', {k1: rec(3.0, None, sh='unconverged')}, ['SV_DEPENDENT'], 'dependent'),
            ('괄호 [1.2, 위 못 읽음 (unconverged)]', {k1: rec(1.2, None, sh='unconverged')}, ['SV_UNCHECKED'], 'unreadable'),
            ('괄호 [아래 못 읽음, 1.5] (지금 방식 = 못 읽음 · 결정 필요 표지)', {k1: rec(None, 1.5, st='unconverged')}, ['SV_UNCHECKED'],
             'unreadable'),
            ('위 끝 칸 없는 옛 꼴 (비 1.2 · ratio_hi 없음) = 못 읽음 (fail-closed)', {k1: {'sv_cf': {'status': 'computed', 'ratio': 1.2}}},
             ['SV_UNCHECKED'], 'unreadable'),
            ('두 모서리 — 하나 의존 [3, 9] · 하나 걸침 [1, ∞] (묶기 = 지금 규칙 · 둘 다)',
             {k1: rec(3.0, 9.0), k2: rec(1.0, math.inf, sh='no_through_without_sv')}, ['SV_DEPENDENT', 'SV_UNCHECKED'], None)):
        r = dict(base)
        r.update(upd)
        f, d = RR.sv_assess(r, 2.0, 'R_j0')
        ok = sorted(f) == sorted(want)
        if det_key is not None:
            ok = ok and 'c1_P1_R_j0' in (d.get(det_key) or [])
        cases.append((nm, ok, f, {k: d.get(k) for k in ('straddle', 'unreadable', 'dependent')}))
    #  사유 (§5-5b) — 걸침 = 괄호 · 모서리 (비 값 없음) · 못 읽음 사유 = 옛 글자 그대로
    f1, d1 = RR.sv_assess({**base, k1: rec(1.0, math.inf, sh='no_through_without_sv')}, 2.0, 'R_j0')
    why = RR.sv_reasons(f1, d1).get('SV_UNCHECKED', '')
    rs_ok = '걸침' in why and 'c1_P1_R_j0' in why and '∞' not in why and 'inf' not in why
    f2, d2 = RR.sv_assess({**base, k1: rec(1.2, None, sh='unconverged')}, 2.0, 'R_j0')
    why2 = RR.sv_reasons(f2, d2).get('SV_UNCHECKED', '')
    rs_ok = rs_ok and why2.startswith('대조 비를 못 읽음') and '걸침' not in why2
    corner = d1.get('corners', {}).get('c1_P1_R_j0', {})
    det_ok = corner.get('ratio') == 1.0 and corner.get('ratio_hi') == math.inf and corner.get('n_unsplit') == 1
    return (all(c[1] for c in cases) and rs_ok and det_ok,
            ([c for c in cases if not c[1]], why, why2, corner))


@check('U08b', '★ 10-22 SV 반사실 괄호 판정 (PRE2-impl-01 · Q1 (다) · §5-6 SV 행 개정) — 아래 > 문턱 = SV_DEPENDENT · 두 끝을 읽고 위 ≤ 문턱 = 없음 · '
               '걸침 (아래 ≤ 문턱 < 위) · 못 읽음 · 옛 꼴 (위 끝 칸 없음) = SV_UNCHECKED · 모서리 묶기 = 하나라도 (둘 다 붙음) · 사유 = 걸침 · 모서리 '
               '(비 값 없음) · 세부 = 두 끝 · 못 가른 덩어리 수')
def t_U08b():
    return eval_U08b()


@check('M41', '★ 10-22 변이: SV 판정 = 아래 끝 하나만 (옛 규칙 · 위 끝 무시) → U08b 가 떨어진다 (변이 전 통과 확인)')
def t_M41():
    def lower_only(recs, threshold, scope):
        rr_scope = ('R_j_lo', 'R_j0', 'R_j_hi') if scope == 'all3' else ('R_j0',)
        out, unread, dep = {}, [], []
        for (c, law, rr), a in sorted(recs.items()):
            if rr not in rr_scope:
                continue
            v = a.get('sv_cf') if isinstance(a, dict) else None
            r_ = (v or {}).get('ratio')
            key = f'c{c}_{law}_{rr}'
            out[key] = {'status': (v or {}).get('status'), 'ratio': r_}
            if not isinstance(r_, float):
                unread.append(key)
            elif threshold is not None and r_ > float(threshold):
                dep.append(key)
        flags = (['SV_UNCHECKED'] if (threshold is None or unread or not out) else []) + (['SV_DEPENDENT'] if dep else [])
        return flags, {'threshold': threshold, 'scope': scope, 'corners': out, 'unreadable': unread, 'dependent': dep, 'straddle': []}
    base_ok, base_why = eval_U08b()
    caught, why = mutant('M41', {'sv_assess': lower_only}, eval_U08b)
    return base_ok and caught, (base_ok, why if base_ok else base_why)


@check('M42', '★ PF2 E (10-22 · 판정문 변이 Ml) 등급 경계 ≤ → < (정보 있음 칸 · 약함 칸 각각) → G01 이 떨어진다 (옛 시험 묶음에서는 살아남았다)')
def t_M42():
    def ml_a(W):
        return 'PASS_INFORMATIVE' if W < RR.GRADE_INFORMATIVE_MAX else 'CONSISTENT_WEAK' if W <= RR.GRADE_WEAK_MAX else 'UNINFORMATIVE'

    def ml_b(W):
        return 'PASS_INFORMATIVE' if W <= RR.GRADE_INFORMATIVE_MAX else 'CONSISTENT_WEAK' if W < RR.GRADE_WEAK_MAX else 'UNINFORMATIVE'
    base_ok, base_why = eval_G01()
    ca, wa = mutant('M42a', {'grade_W': ml_a}, eval_G01)
    cb, wb = mutant('M42b', {'grade_W': ml_b}, eval_G01)
    return base_ok and ca and cb, (base_ok, wa, wb, base_why)


def eval_U15():
    """★ PF2 E (10-22 · 사전 리뷰 2 회차 PRE2-impl-02 옆 자리 · 결정 없음) — 사슬 SV 판정은 한 끝의 이상한 비 (NaN · −∞ · 0 · −0 · 음수 · 빈칸 ·
    bool · 글자 · 목록) 를 '표지 없음' 으로 읽지 않는다 (아래 · 위 끝 어느 쪽이든 → 표지가 늘 붙는다).  읽는 비 = float (bool 아님) · 유한 양수
    또는 +∞ (아래 +∞ = 의존 · 위 +∞ + 아래 ≤ 문턱 = 걸침 — 옛 그대로).  사슬 꼴 (`ca_ext_svcf.chain_view`) 을 거쳐도 같다.
    옛 사슬 = NaN · −∞ · 0 · 음수가 float 라 '읽음' → 아래 NaN + 위 1.5 = 표지 없음 (위 ≤ 문턱)."""
    import ca_ext_svcf as SVCF

    def rec(lo, hi, nu=1):
        return {'sv_cf': {'status': 'computed', 'ratio': lo, 'status_hi': 'computed', 'ratio_hi': hi, 'n_unsplit': nu}}
    base = {(c, law, rr): rec(1.2, 1.2, 0) for c in ('0', '1') for law in ('P0', 'P1') for rr in ('R_j_lo', 'R_j0', 'R_j_hi')}
    k1 = ('1', 'P1', 'R_j0')
    weird = (float('nan'), -math.inf, 0.0, -0.0, -1.0, None, '', True, False, '1.2', [], {})
    f0, _ = RR.sv_assess(base, 2.0, 'R_j0')
    bad = []
    for side in ('lo', 'hi'):
        for w in weird:
            f, _d = RR.sv_assess({**base, k1: (rec(w, 1.5) if side == 'lo' else rec(1.2, w))}, 2.0, 'R_j0')
            if not f:
                bad.append(f'{side}={w!r} → 표지 없음')
    fi_lo, _ = RR.sv_assess({**base, k1: rec(math.inf, 1.5)}, 2.0, 'R_j0')
    fi_hi, _ = RR.sv_assess({**base, k1: rec(1.2, math.inf)}, 2.0, 'R_j0')
    tam = {'status': 'computed', 'sv_counterfactual_ratio': float('nan'), 'ratio_limit': None, 'status_hi': 'computed',
           'sv_counterfactual_ratio_hi': 1.5, 'ratio_limit_hi': None, 'n_unsplit_bridging_components': 1}
    fv, _ = RR.sv_assess({**base, k1: {'sv_cf': SVCF.chain_view(tam)}}, 2.0, 'R_j0')
    return (f0 == [] and not bad and fi_lo == ['SV_DEPENDENT'] and fi_hi == ['SV_UNCHECKED'] and fv != [],
            (f0, bad, fi_lo, fi_hi, fv))


@check('U15', '★ PF2 E (10-22 · PRE2-impl-02) SV 판정 — 아래 · 위 끝 어느 쪽의 NaN · −∞ · 0 · −0 · 음수 · 빈칸 · bool · 글자 · 목록도 "표지 없음" 이 '
               '아니다 (SV_UNCHECKED) · 아래 +∞ = SV_DEPENDENT · 위 +∞ = 걸침 · 정상 [1.2, 1.2] = 없음 · 사슬 꼴 (chain_view) 을 거친 NaN 도')
def t_U15():
    return eval_U15()


def eval_G01():
    """★ PF2 E (10-22 · 사전 리뷰 2 회차 PRE2-design-06 · 결정 없음) — 등급 문턱 = 정확값 G0/2 · G0 (G0 = ln(4.68/1.8877)) · 칼날 양쪽:
    W = G0/2 → PASS · 바로 위 (nextafter) → WEAK · W = G0 → WEAK · 바로 위 → UNINFORMATIVE · 바로 아래 = 아래 등급 그대로 ·
    표시 반올림 0.454 · 0.908 은 정확 문턱 위라 한 등급 아래 (WEAK · UNINFORMATIVE — 판정문 탐침 B)."""
    G0 = math.log(RR.EXP_DBE_MS / RR.CUR_GEN_DBE_MS)
    a, b = RR.GRADE_INFORMATIVE_MAX, RR.GRADE_WEAK_MAX
    want = ((a, 'PASS_INFORMATIVE'), (math.nextafter(a, 0.0), 'PASS_INFORMATIVE'), (math.nextafter(a, math.inf), 'CONSISTENT_WEAK'),
            (b, 'CONSISTENT_WEAK'), (math.nextafter(b, 0.0), 'CONSISTENT_WEAK'), (math.nextafter(b, math.inf), 'UNINFORMATIVE'),
            (0.454, 'CONSISTENT_WEAK'), (0.908, 'UNINFORMATIVE'), (0.0, 'PASS_INFORMATIVE'))
    got = [(w, RR.grade_W(w), v) for w, v in want]
    return (all(g == v for _w, g, v in got) and a == G0 / 2.0 and b == G0 and RR.G0 == G0,
            ([x for x in got if x[1] != x[2]], a, b, G0))


@check('G01', '★ PF2 E (10-22 · PRE2-design-06) 등급 경계 — W = 정확 G0/2 → PASS · nextafter 위 → WEAK · W = 정확 G0 → WEAK · nextafter 위 → '
              'UNINFORMATIVE · 바로 아래 그대로 · 표시 반올림 0.454 → WEAK · 0.908 → UNINFORMATIVE · 문턱 = ln(4.68/1.8877) 의 정확값')
def t_G01():
    return eval_G01()


def predes01_S(R, i):
    """사전 리뷰 PRE-design-01 — arm 0 S = 1.43 + 0.2/r · arm 1–7 S = 1.53 + 0.1/r (r = R/1e6 · r = 1 에서 모두 1.63 · 중앙 산포 ≈ 0)."""
    if R == math.inf:
        return 1.43 if i == 0 else 1.53
    r = max(R / 1e6, 1e-6)
    return (1.43 + 0.2 / r) if i == 0 else (1.53 + 0.1 / r)


def eval_U10():
    lad_ = RR.Ladder(ladder_fetch(predes01_S), max_points=24, ratio_max='none')
    lad_.run()
    lad_.origin()
    st = lad_.st
    T = {'lo': 1.63 * 1.02, 'hi': 1.63 * 0.98}
    bad = []
    for side, key in (('lo', st['R_j_lo']), ('hi', st['R_j_hi'])):
        R = RR.rj_float(key)
        for i in (0, 1, 2):
            s = predes01_S(R, i)
            if (side == 'lo' and s < T['lo']) or (side == 'hi' and s > T['hi']):
                bad.append(f'{side} 끝 {key} 의 arm {i} σ {s:.5f} 가 띠 안 (합집합 바깥 감쌈 깨짐)')
    pushed = sum(int((st['ends'][s_] or {}).get('origin_pushes', 0)) for s_ in ('lo', 'hi'))
    if pushed < 1:
        bad.append('끝 origin 밀기 없음 (arm 0 끝이 arm 1 · 2 의 띠 안인데)')
    if not (st['origin'] or {}).get('status') == 'pass':
        bad.append(f'R_j,0 origin {st["origin"]} (중앙 산포 ≈ 0 = pass 여야 — 중앙 검사만으로는 못 잡는 부류)')
    return not bad, (bad, st['R_j_lo'], st['R_j_hi'], st['ends'])


@check('U10', 'PRE-design-01 (Q-E · P1) — 중앙 (R_j,0) 산포 2.2e-16 · CALIB_ORIGIN_SENSITIVE 안 걸리는데 arm 1 · 2 의 허용집합이 arm 0 보다 넓다 → '
               '끝에서 arm 1 · 2 도 돌려 하나라도 띠 안이면 바깥 실측 이웃으로 → 끝의 세 origin 이 모두 띠 밖 (합집합을 바깥에서 감쌈)')
def t_U10():
    return eval_U10()


# ── ★ 4판 Q2 (1저자 10-21 "권고대로") — 등록 R 4판 규칙 여섯 (시험 먼저 · 기대 = 등록 규칙의 정확한 출력) ──
#  Q2-1 §3-2c 이름 우선순위 ─────────────────────────────────────────────
def eval_U11():
    bad = []
    for c in REG_CALIB6:
        for st in ({'P0': 'NOT_COMPUTED', 'P1': c}, {'P0': c, 'P1': 'NOT_COMPUTED'}):
            if RR.judge_set(st, None) != {'verdict': 'NOT_COMPUTED', 'state': 'calib'}:
                bad.append((st, RR.judge_set(st, None)))
        for st in ({'P0': c, 'P1': 'CALIBRATED'}, {'P0': 'CALIBRATED', 'P1': c}):
            if RR.judge_set(st, None) != {'verdict': c, 'state': 'calib'}:
                bad.append((st, RR.judge_set(st, None)))
    for i, a in enumerate(REG_CALIB6):                      # 둘 다 CALIB_* = 등록 나열 순서의 첫 이름
        for b in REG_CALIB6:
            want = a if i <= REG_CALIB6.index(b) else b
            if RR.judge_set({'P0': a, 'P1': b}, None)['verdict'] != want:
                bad.append((a, b, RR.judge_set({'P0': a, 'P1': b}, None)))
    if RR.judge_set({'P0': 'NOT_COMPUTED', 'P1': 'NOT_COMPUTED'}, None)['verdict'] != 'NOT_COMPUTED':
        bad.append('NC NC')
    return not bad, bad[:4]


@check('U11', '★ 4판 Q2-1 (§3-2c · PRE-design-08) — 두 법칙 이름이 다르면 하나라도 NOT_COMPUTED = 판정 전체 NOT_COMPUTED (상태 먼저) · 아니면 '
               '등록 나열 순서의 첫 CALIB_* · 반례 P0 NOT_COMPUTED · P1 CALIB_EDGE → NOT_COMPUTED (3판 = CALIB_EDGE · CALIB_ORDER 끝)')
def t_U11():
    return eval_U11()


def run_U11b():
    def go():
        #  P1 법칙 배수 0.95 가 바닥에도 걸린다 → 바닥 1.60e-3 / 0.95 (P1 바닥 = 1.60e-3 · 1.63 의 2 % 안 = CALIB_EDGE · L10 의 P1 짝)
        p1 = ladder('U11b_P1', world('U11b_P1', dict(PW, sbe=dict(PW_SBE, floor=1.60e-3 / 0.95, s_ref=40e-3))), law='P1')
        l17 = scen('L17', lambda: ladder('L17', world('L17', dict(PW, faults=[{'do': 'certfail', 'match': {'rj': '1000000.0'}}]))))
        return {'p1': p1, 'v': verdict('U11b_v', [l17['out'], p1['out']])}
    return scen('U11b', go)


@check('U11b', '★ 4판 Q2-1 (사슬) — P0 사다리 NOT_COMPUTED (증서 실패 · L17) + P1 사다리 CALIB_EDGE → 판정 NOT_COMPUTED (rc 0 · 법칙별 이름 늘 보고 · '
                '사유 둘)')
def t_U11b():
    sc = run_U11b()
    v = sc['v']['v'] or {}
    rs = sorted((w.get('law'), w.get('code')) for w in (v.get('reasons') or []))
    return (sc['p1']['sum']['status'] == 'CALIB_EDGE' and sc['v']['rc'] == 0 and v.get('verdict') == 'NOT_COMPUTED'
            and v.get('calib') == {'P0': 'NOT_COMPUTED', 'P1': 'CALIB_EDGE'} and rs == [('P0', 'NOT_COMPUTED'), ('P1', 'CALIB_EDGE')],
            (sc['p1']['sum']['status'], v.get('verdict'), v.get('calib'), rs))


#  Q2-2 §3-2b ③″ 보호 띠 ───────────────────────────────────────────────
def run_U01e(err, S=None, read=1.0, cap=12):
    lad_ = RR.Ladder(ladder_fetch(S or rca01_S, err=err, read=read), max_points=cap, ratio_max='none')
    status = 'CALIBRATED'
    try:
        lad_.run()
        lad_.origin()
    except RR.Stop as e:
        status = e.code
    st = lad_.st
    R = {k: (RR.rj_float(st[k]) if st.get(k) else None) for k in ('R_j_lo', 'R_j0', 'R_j_hi')}
    J = RR.judge({('0', 'P0', k): rca01_D(v) for k, v in R.items()}) if status == 'CALIBRATED' else None
    return lad_, status, R, J


#: 등록 R 4판 §3-2b ⑧ — 증서 보장 오차 e ≥ 3.728e-5 → hi 끝 = 바깥 이웃 1e7 · 비 1,000 · W 0.786487 · 같은 등급 (CONSISTENT_WEAK)
U01E_W = math.log(rca01_D(1e4) / rca01_D(1e7))


def eval_U01e():
    bad = []
    for e, want_hi in ((1e-4, 1e7), (3.8e-5, 1e7), (3.7e-5, RCA01_WANT['R_hi']), (0.0, RCA01_WANT['R_hi'])):
        lad_, status, R, J = run_U01e(e)
        st = lad_.st
        hi_src = (st.get('ends') or {}).get('hi', {}).get('source')
        if status != 'CALIBRATED' or R['R_j_lo'] != 1e4 or R['R_j0'] != RCA01_WANT['R0'] or rel(R['R_j_hi'], want_hi) > 1e-9:
            bad.append((e, status, R, hi_src))
            continue
        if want_hi == 1e7:
            if not (rel(st['R_ratio'], 1000.0) < 1e-12 and J['verdict'] == 'CONSISTENT_WEAK' and rel(J['W'], U01E_W) < 1e-12
                    and abs(J['W'] - 0.786487) < 5e-7 and hi_src == 'outer_neighbor'):
                bad.append((e, st['R_ratio'], J['verdict'], J['W'], hi_src))
        elif not (rel(st['R_ratio'], RCA01_WANT['ratio']) < 1e-9 and J['verdict'] == 'CONSISTENT_WEAK' and rel(J['W'], RCA01_WANT['W']) < 1e-9
                  and hi_src == 'candidate'):
            bad.append((e, st['R_ratio'], J['verdict'], J['W'], hi_src))
    return not bad, bad


@check('U01e', '★ 4판 Q2-2 (§3-2b ③″ ⑧ · PRE-design-12 · R4-Q2 · R4-Q3) — 끝 판정 = 판독 [σ(1 − e), σ(1 + e)] (e = 그 런 증서 보장 오차) 가 띠에 '
                '걸치면 바깥으로: RCA-01 회로 e = 0 · 3.7e-5 → 비 599.03 (후보) · e = 3.8e-5 · 1e-4 (≥ 3.728e-5) → hi 끝 = 바깥 이웃 1e7 · 비 1,000 · '
                'W 0.786487 · CONSISTENT_WEAK (3판 = 띠 없음 · 늘 599.03)')
def t_U01e():
    return eval_U01e()


T_MINUS = 1.63 * 0.98
U12_F = T_MINUS * (1.0 - 5e-5)                              # 등록 R 4판 §3-2b ③″ 반례 — 바닥 F = T⁻(1 − 5e-5) (|F/1.63 − 1| = 0.02005)
U12_TRUE_HI = (0.05 / (T_MINUS - U12_F) - 0.1) * 1e5        # 참 R_hi (S(R) = T⁻) = 6.259e7 Ω


def u12_S(R, i=0):
    """반례 SBE — S = F + 0.05/(r + 0.1) mS/cm · r = R/1e5 Ω (origin 무관)."""
    return U12_F if R == math.inf else U12_F + 0.05 / (R / 1e5 + 0.1)


def eval_U12():
    a = run_U01e(1e-4, S=u12_S, cap=24)                     # 판독 오차 e 1e-4 ≥ 5e-5 → 바닥이 EDGE 띠에 걸친다
    b = run_U01e(4e-5, S=u12_S, cap=24)                     # e 4e-5 < 5e-5 → EDGE 아님
    ok = (a[1] == 'CALIB_EDGE' and a[0].st['n_runs'] == 2 and b[1] != 'CALIB_EDGE' and b[0].st['n_runs'] > 2
          and abs(abs(U12_F / 1.63 - 1.0) - 0.02005) < 1e-5 and abs(U12_TRUE_HI - 6.259e7) < 1e4)
    return ok, (a[1], a[0].st['n_runs'], b[1], b[0].st['n_runs'], U12_TRUE_HI)


@check('U12', '★ 4판 Q2-2 (§3-1 · §3-2b ③″) — EDGE 판정에도 보호 띠: 바닥 F = T⁻(1 − 5e-5) (EDGE 안 걸림 · |F/1.63 − 1| = 0.02005) · 판독 오차 '
               'e = 1e-4 → [F(1 − e), F(1 + e)] 가 EDGE 띠에 걸침 → CALIB_EDGE (바닥 · 천장 두 런 뒤 · 3판 = EDGE 아님 · 사다리 계속) · e = 4e-5 → EDGE 아님')
def t_U12():
    return eval_U12()


def eval_U12b():
    lad_, status, R, _J = run_U01e(4e-5, S=u12_S, read=1.0 - 4e-5, cap=24)
    ok = (status == 'CALIBRATED' and R['R_j_hi'] >= U12_TRUE_HI * (1.0 - 1e-12)) or status == 'CALIB_LADDER_EXHAUSTED'
    return ok, (status, R, U12_TRUE_HI, (lad_.st.get('ends') or {}).get('hi'))


@check('U12b', '★ 4판 Q2-2 (§3-2b ③″ 반례 · 보수 쪽) — 증서 허용 안의 낮은 판독 (σ × (1 − e) · e 4e-5) 에서도 hi 끝은 참 끝 6.259e7 의 바깥 (≥) 이거나 '
                '사다리 소진 (CALIB_LADDER_EXHAUSTED) — 안쪽 끝 (낮은 판독이 "≤ T⁻" 로 읽힌 자리) 을 쓰지 않는다 (3판 = 안쪽 끝)')
def t_U12b():
    return eval_U12b()


def eval_L22():
    """사슬 배선 — read_run 이 증서 (target_lo · target_hi · I_bot) 에서 보장 오차를 다시 계산해 팔 기록 err_rel 로 싣고 · 사다리가 그 값으로 띠를 잰다."""
    e = 9e-5
    w = ladder('L22', world('L22', dict(PW, cert_e=e)))
    edge = ladder('L22e', world('L22e', dict(PW, cert_e=e, sbe=dict(PW_SBE, floor=U12_F * 1e-3))))
    edge0 = ladder('L22z', world('L22z', dict(PW, sbe=dict(PW_SBE, floor=U12_F * 1e-3))))
    ers = (lad(w).get('err_rel') or {})
    pub = [a.get('err_rel') for r in (w['sum'] or {}).get('runs', []) for a in (r.get('arms_read') or [])]
    fin = [v for k, v in ers.items() if k != 'inf']
    ok = (bool(fin) and all(isinstance(v, float) and rel(v, e) < 1e-6 for v in fin) and all(isinstance(v, float) for v in pub)
          and edge['sum']['status'] == 'CALIB_EDGE' and roles(edge) == ['floor', 'ceiling'] and edge0['sum']['status'] != 'CALIB_EDGE'
          and len(roles(edge0)) > 2)
    return ok, (sorted(set(round(v, 12) for v in fin)), pub[:3], edge['sum']['status'], roles(edge), edge0['sum']['status'])


@check('L22', '★ 4판 Q2-2 (사슬 배선 · 가짜 러너) — 증서 보장 오차 9e-5 = 팔 기록 err_rel (증서 구간에서 다시 계산 · 공개 칸) · 사다리 기록 err_rel · '
               '바닥 T⁻(1 − 5e-5) 침대 = 증서 오차 9e-5 면 CALIB_EDGE (두 런) · 0 이면 EDGE 아님')
def t_L22():
    return eval_L22()


#  Q2-3 §4-2 W₊ · 상태 다름 ─────────────────────────────────────────────
def u13_fetch(spec):
    """spec[(c, 법칙)] = (arm 0 σ mS · 상태, origin 팔 1 · 2 σ mS · 상태, 8 팔 런의 팔 1–7 σ mS) — 세 R 같은 값 · SBE no-op = 1.63."""
    def fetch(kit, role, law, c, rj, arms, sv_cf=False):
        if kit == SBE_KIT:
            return [{'sigma': 1.63e-3, 'n_sdcp_near': 0, 'state': 'positive', 'err_rel': 0.0}]
        (a0, s0), (o12, so), o8 = spec[(c, law)]
        out = []
        for i in _arms_of(arms):
            v, st = (a0, s0) if i == 0 else ((o8, 'positive') if isinstance(arms, int) else (o12, so))
            out.append({'sigma': v * 1e-3, 'state': st, 'n_sdcp_near': 7, 'err_rel': 0.0})
        return out
    return fetch


U13_LADS = {law: {'R_j_lo': '0.5', 'R_j0': '1.0', 'R_j_hi': '2.0', 'r0_sigma': 1.63e-3} for law in ('P0', 'P1')}


def run_U13(spec):
    pr = RR.Predict(u13_fetch(spec), U13_LADS, None, sv_scope=None)
    pr.run()
    return pr, RR.judge({k: v * 1e3 for k, v in pr.values().items()})


def eval_U13():
    spec = {('0', 'P0'): ((0.0, 'zero'), (6.0, 'positive'), 6.0), ('1', 'P0'): ((3.0, 'positive'), (3.0, 'positive'), 3.0),
            ('0', 'P1'): ((3.5, 'positive'), (3.5, 'positive'), 3.5), ('1', 'P1'): ((4.0, 'positive'), (4.0, 'positive'), 4.0)}
    pr, J = run_U13(spec)
    org = {f'c{o["c"]}_{o["law"]}': o for o in pr.origin}
    ok = (J['verdict'] == 'CONSISTENT_WEAK' and rel(J['interval_mScm'][0], 3.0) < 1e-12 and rel(J['interval_mScm'][1], 5.25) < 1e-12
          and rel(J['W'], math.log(1.75)) < 1e-12
          and abs(J['W'] - 0.5596) < 5e-5 and org['c0_P0']['status'] == 'adjusted'
          and all(org[k]['status'] == 'pass' for k in ('c1_P0', 'c0_P1', 'c1_P1')))
    return ok, (J.get('verdict'), J.get('interval_mScm'), J.get('W'), {k: (o['status'], o['per_R']) for k, o in org.items()})


@check('U13', '★ 4판 Q2-3 (§4-2 PRE-design-10 ① · R4-Q4) — 한 모서리 · R 의 세 origin 상태가 다르면 = 넘음 (8 팔 평균 · zero 는 0 으로 더함): 등록 반례 '
               'arm 0 {0 (VALID_ZERO) · 3.0 · 3.5 · 4.0} · zero 모서리 arm 1 · 2 = 6.0 → 그 모서리 5.25 → [3.0, 5.25] · W 0.5596 · CONSISTENT_WEAK '
               '(3판 = W +∞ → 문턱 +∞ → 전환 없음 → FAIL)')
def t_U13():
    return eval_U13()


def eval_U13b():
    spec = {('0', 'P0'): ((0.0, 'zero'), (0.0, 'zero'), 0.0), ('1', 'P0'): ((3.0, 'positive'), (3.0, 'positive'), 3.0),
            ('0', 'P1'): ((3.5, 'positive'), (3.5, 'positive'), 3.5), ('1', 'P1'): ((4.0, 'positive'), (4.2, 'positive'), 4.2)}
    pr, J = run_U13(spec)
    org = {f'c{o["c"]}_{o["law"]}': o for o in pr.origin}
    wp = math.log(4.0 / 3.0)
    mean8 = (4.0 + 7 * 4.2) / 8.0
    v = pr.values()
    ok = (rel(pr.sealed.get('W_pos', math.nan), wp) < 1e-12 and pr.sealed['W0'] == math.inf and org['c1_P1']['status'] == 'adjusted'
          and org['c0_P0']['status'] == 'pass' and all(rel(v[('1', 'P1', rr)] * 1e3, mean8) < 1e-12 for rr in RR.RJ_ROLES)
          and math.log(4.2 / 4.0) > 0.1 * wp)
    return ok, (pr.sealed.get('W_pos'), pr.sealed.get('W0'), {k: o['status'] for k, o in org.items()})


@check('U13b', '★ 4판 Q2-3 (§4-2 ②) — 상태는 같은데 W (arm 0 첫 폭) 가 +∞ (다른 모서리의 zero) → 문턱의 W = W₊ (arm 0 양수 값의 폭 ln(4/3)) · '
                'c1 P1 의 origin 산포 ln 1.05 > 0.1 W₊ → 넘음 → 세 R 8 팔 평균 4.175 · zero 모서리 (세 origin 다 zero) = 통과 (3판 = 문턱 +∞ → 통과)')
def t_U13b():
    return eval_U13b()


#  Q2-5 §5-6 변이 표지 ─────────────────────────────────────────────────
def eval_U14():
    main = {'statuses': CAL2, 'vals': rca09_main(), 'flags': []}
    same = lambda **kw: dict(main, **kw)                    # noqa: E731
    cases = {
        'a 변이 예측 NOT_COMPUTED (vals None)': (same(vals=None), 'FIBRE_UNCHECKED', 'FIBRE_SENSITIVE', '변이 판정 NOT_COMPUTED'),
        'b 변이 사다리 NOT_COMPUTED': (same(statuses={'P0': 'NOT_COMPUTED', 'P1': 'CALIBRATED'}, vals=None), 'FIBRE_UNCHECKED',
                                       'FIBRE_SENSITIVE', '변이 판정 NOT_COMPUTED'),
        'c 변이 이름 같음 + 변이 자신의 CALIB_ORIGIN_SENSITIVE': (same(flags=['CALIB_ORIGIN_SENSITIVE']), 'FIBRE_UNCHECKED',
                                                                 'FIBRE_SENSITIVE', '변이 자신의 차단 표지 CALIB_ORIGIN_SENSITIVE'),
        'd 변이 CALIB_EDGE (결과 이름 · 다름)': (same(statuses={'P0': 'CALIB_EDGE', 'P1': 'CALIBRATED'}, vals=None), 'FIBRE_SENSITIVE',
                                                'FIBRE_UNCHECKED', '변이 판정 이름 CALIB_EDGE'),
        'e 변이 이름 다름 + 자신의 CALIB_ORIGIN_SENSITIVE': (same(vals={k: (v if k[2] == 'R_j0' else (7.0e-3 if k[2] == 'R_j_lo' else 3.0e-3))
                                                                     for k, v in main['vals'].items()}, flags=['CALIB_ORIGIN_SENSITIVE']),
                                                          'FIBRE_SENSITIVE', 'FIBRE_UNCHECKED', '변이 판정 이름 CONSISTENT_WEAK'),
    }
    bad = []
    for nm, (var, want, avoid, why) in cases.items():
        pub, _res = RR.assemble(main, {'FIBRE': var, 'UNREG': dict(main), 'GRID': dict(main), 'SVORDER': dict(main)}, ([], {}))
        rs = pub.get('blocking_reasons') or {}
        if not (want in pub['flags'] and avoid not in pub['flags'] and 'CALIB_ORIGIN_SENSITIVE' not in pub['flags']
                and str(rs.get(want, '')).startswith(why) and pub['sentence_allowed'] is False):
            bad.append((nm, pub['flags'], rs, pub.get('variants', {}).get('FIBRE')))
    return not bad, bad


@check('U14', '★ 4판 Q2-5 (§5-6 PRE-design-17 ② ③ ④ ⑤ · R4-Q8) — 변이 NOT_COMPUTED (예측 · 사다리) → <V>_UNCHECKED (3판 = _SENSITIVE) · 변이 이름 같음 + '
               '자신의 CALIB_ORIGIN_SENSITIVE → <V>_UNCHECKED · 결과 이름 다름 (CALIB_* 포함) → <V>_SENSITIVE (② 먼저) · 변이 자신의 표지는 주 표지 '
               '목록에 옮기지 않는다 · 표지마다 사유')
def t_U14():
    return eval_U14()


def run_V18():
    def go():
        dirs = list(main_dirs())
        vl0 = ladder('V18_P0', world('V18_P0', dict(PW, faults=[{'do': 'certfail', 'match': {'rj': '1000000.0'}}])), law='P0',
                     variant='FIBRE')
        vl1 = ladder('V18_P1', world('V18_P1'), law='P1', variant='FIBRE')
        return {'l': [vl0, vl1], 'v': verdict('V18_v', dirs + [vl0['out'], vl1['out']])}
    return scen('V18', go)


@check('V18', '★ 4판 Q2-5 (사슬) — 감도 FIBRE 사다리 P0 가 NOT_COMPUTED (증서 실패) → FIBRE 판정 NOT_COMPUTED → FIBRE_UNCHECKED (FIBRE_SENSITIVE 아님 · '
               '3판 = 이름 다름 → SENSITIVE) · 주 판정 이름 그대로')
def t_V18():
    sc = run_V18()
    v = sc['v']['v'] or {}
    fv = (v.get('variants') or {}).get('FIBRE') or {}
    return (sc['l'][0]['sum']['status'] == 'NOT_COMPUTED' and v.get('verdict') == 'PASS_INFORMATIVE' and 'FIBRE_UNCHECKED' in v.get('flags', [])
            and 'FIBRE_SENSITIVE' not in v.get('flags', []) and fv.get('verdict') == 'NOT_COMPUTED',
            (sc['l'][0]['sum']['status'], v.get('verdict'), v.get('flags'), fv))


#  Q2 가장자리 (보호 띠 연장 · 판정 없음 칸 · 표지마다 사유) — 두 번째 시험 먼저 ───────────────────────
U12C_TP = 1.63 * 1.02                                       # T⁺ (mS/cm)
#: S(1e4) = T⁺(1 + 3e-5) 가 되게 고른 k — 판독 오차 e 1e-4 면 1e4 점이 T⁺ 띠에 걸치고 더 작은 R 실측 점은 아직 없다
U12C_K = (U12C_TP * (1.0 + 3e-5) - 1.597) * (1e4 / RCA01_SCALE + 0.1)


def u12c_S(R, i=0):
    """보호 띠 연장 — RCA-01 꼴 S = 1.597 + k/(r + 0.1) mS/cm (r = R/10^4.75 · origin 무관)."""
    return 1.597 if R == math.inf else 1.597 + U12C_K / (R / RCA01_SCALE + 0.1)


def eval_U12c():
    true_lo = (U12C_K / (U12C_TP - 1.597) - 0.1) * RCA01_SCALE           # 참 R_lo (S = T⁺) ≈ 10,011.9 Ω
    try:
        a = run_U01e(1e-4, S=u12c_S, cap=24)
        b = run_U01e(0.0, S=u12c_S, cap=24)
    except Exception as e:                                  # noqa: BLE001 — 바깥 실측 점이 없을 때 사슬이 죽으면 (max([]) …) 실패
        return False, f'{type(e).__name__}: {e}'
    lad_, status, R, _J = a
    lo = (lad_.st.get('ends') or {}).get('lo') or {}
    ok = (status == 'CALIBRATED' and R['R_j_lo'] == 100.0 and lo.get('source') == 'outer_neighbor' and '100.0' in lad_.st['order']
          and lad_.st['n_ext'] >= 1 and R['R_j_lo'] <= true_lo
          and u12c_S(1e4) * (1.0 - 1e-4) < U12C_TP <= u12c_S(1e4) and u12c_S(1e2) * (1.0 - 1e-4) >= U12C_TP
          and b[1] == 'CALIBRATED' and b[2]['R_j_lo'] == 1e4 and b[0].st['n_ext'] == 0)
    return ok, (status, R, lo.get('source'), lad_.st['n_ext'], b[1], b[2], true_lo)


@check('U12c', '★ 4판 Q2-2 (§3-2b ③″ · 구현 가장자리) — 바깥 실측 점이 보호 띠로 다 걸치면 (1e4 점 σ = T⁺(1 + 3e-5) · e 1e-4 · 더 작은 R 실측 '
                '없음) 사다리 규칙 그대로 같은 쪽 ×100 새 점 (1e2) 을 돌아 끝으로 (③′ 연장 꼴 · 죽지 않는다 · 참 끝 10,011.9 의 바깥) · e = 0 이면 3판 그대로 '
                '(끝 1e4 · 연장 없음)')
def t_U12c():
    return eval_U12c()


@check('V19', '★ 4판 (Q2-4 · §5-5b 같은 레코드 = 같은 문장) — 판정 기록 문장 칸: CALIB_EDGE (V08) = 판정 없음 칸 (법칙별 이름 · 사유 · …) · 등록 결과 '
               'NOT_COMPUTED (V13) = 판정 없음 칸 (사유) · 사슬 멈춤 (S21 DUPLICATE_RUN) = 같은 NOT_COMPUTED 칸 + 사유 = 멈춤 코드 (단계 verdict) · '
               '감도 미완료 칸 = 해당 없음 (null) (3판 = 셋 다 문장 null · 멈춤 사유 없음)')
def t_V19():
    v8 = scen('V08', lambda: verdict('V08', [run_L10()['out'], s_main('P1')['out']]))['v'] or {}
    v13 = scen('V13', lambda: verdict('V13', [scen('L17', lambda: ladder('L17', world('L17', dict(
        PW, faults=[{'do': 'certfail', 'match': {'rj': '1000000.0'}}]))))['out'], s_main('P1')['out']]))['v'] or {}
    s21 = scen('S21', lambda: verdict('S21', main_dirs() + [s_main('P0')['out']]))['v'] or {}
    rs = s21.get('reasons') or []
    ok = (v8.get('verdict') == 'CALIB_EDGE' and v8.get('sentence') == T_CALIB and v8.get('sensitivity_incomplete', 'x') is None
          and v13.get('verdict') == 'NOT_COMPUTED' and v13.get('sentence') == T_NC and v13.get('sensitivity_incomplete', 'x') is None
          and s21.get('verdict') == 'NOT_COMPUTED' and s21.get('sentence') == T_NC and s21.get('blocking_reasons') == {}
          and s21.get('sensitivity_incomplete', 'x') is None and len(rs) == 1 and rs[0].get('stage') == 'verdict'
          and rs[0].get('code') == 'DUPLICATE_RUN')
    return ok, (v8.get('sentence'), v13.get('sentence'), s21.get('sentence'), rs)


@check('V20', '★ 4판 (Q2-4 · §5-5b "표지마다 사유") — SV_DEPENDENT = 대조 비 > 문턱 2.0 (모서리 c1_P1_R_j0 · 비 값은 결과에만) · SV_UNCHECKED = '
               '못 읽음 (모서리) · CALIB_ORIGIN_SENSITIVE = 세 값 (§3-3) · 안 돌린 변이 = 안 돌림 · 차단 표지마다 사유 하나 (빈 칸 없음)')
def t_V20():
    def go7():
        l0 = scen('L19', lambda: run_L19('L19'))
        p = predict('V07_p', world('V07_p'), [l0['out'], s_main('P1')['out']])
        return verdict('V07', [l0['out'], s_main('P1')['out'], p['out']])
    v5 = sv_set('V05', {'status': 'computed', 'ratio': 3.0})['v'] or {}
    v6 = sv_set('V06', {'status': 'unconverged'})['v'] or {}
    v7 = scen('V07', go7)['v'] or {}
    r5, r6, r7 = (v.get('blocking_reasons') or {} for v in (v5, v6, v7))
    full = all(set(r) == set(v.get('blocking_flags') or []) and r and all(isinstance(x, str) and x for x in r.values())
               for r, v in ((r5, v5), (r6, v6), (r7, v7)))
    ok = (full and str(r5.get('SV_DEPENDENT', '')).startswith('대조 비 > 문턱 2.0') and 'c1_P1_R_j0' in r5.get('SV_DEPENDENT', '')
          and '3.0' not in r5.get('SV_DEPENDENT', '') and str(r6.get('SV_UNCHECKED', '')).startswith('대조 비를 못 읽음')
          and 'c1_P1_R_j0' in r6.get('SV_UNCHECKED', '') and str(r7.get('CALIB_ORIGIN_SENSITIVE', '')).startswith('세 값')
          and r5.get('FIBRE_UNCHECKED') == '안 돌림')
    return ok, (r5, r6, r7)


#  ★ RI (10-21 · 등록 R 4판 §5-6 ③ · 1저자 10-21 Q2 범위 = 코드를 등록에 맞춤) — 멈춘 단계 (STOPPED · 등록 결과 이름이 아닌 멈춤) ──────────
#  §5-6 ③ "변이 판정 = `NOT_COMPUTED` (풀이 · 증서 실패 · 단락 · 멈춤) → `<V>_UNCHECKED`" — 감도 변이 단계가 멈추면 그 변이 판정 = NOT_COMPUTED
#  → <V>_UNCHECKED (차단 · PASS 문장은 계속 막힌다) · 주 판정은 그대로 계산한다 (4판 사슬 = 변이 단계 하나가 멈춰도 INPUT_STAGE_STOPPED 로 판정
#  전체 거부).  주 판정 단계의 멈춤 = 판정 전체 NOT_COMPUTED (§5-5 사슬 멈춤 행 · 그대로 · V23).  멈춘 변이 단계도 판정 입력 검사 (계획 ·
#  S0 · 등록 숫자 · 코드 핀 · 주 예측 묶음 · 예측 ↔ 사다리) 는 그대로 받는다 (V24 — 등록이 정하지 않은 자리 = 지금 동작 · 보고).
V21_BLK = ['FIBRE_UNCHECKED', 'GRID_UNCHECKED', 'SVORDER_UNCHECKED', 'UNREG_UNCHECKED']


def run_V21_ladders():
    """FIBRE 변이 사다리 둘 — P0 = 러너 rc 2 (1e4 점 · RUNNER_RC · STOPPED) · P1 = 보정됨 (판정이 원 팔에서 다시 계산)."""
    def go():
        vl0 = ladder('V21_P0', world('V21_P0', dict(PW, faults=[{'do': 'rc2', 'match': {'rj': '10000.0'}}])), law='P0',
                     variant='FIBRE')
        vl1 = ladder('V21_P1', world('V21_P1'), law='P1', variant='FIBRE')
        return [vl0, vl1]
    return scen('V21_l', go)


def run_V22_predict():
    """SVORDER 변이 예측 — 주 사다리 · 주 예측 묶음을 기록한 뒤 첫 DBE 모서리 런에서 러너 rc 2 (RUNNER_RC · STOPPED)."""
    return scen('V22_p', lambda: predict('V22_p', world('V22_p', dict(PW, faults=[{'do': 'rc2', 'match': {'kit_has': 'DBE'}}])),
                                         [s_main('P0')['out'], s_main('P1')['out']], variant='SVORDER'))


def stopped_variant_ok(v, V):
    """멈춘 변이 V 의 판정 기록 — 주 판정을 계산했다 (rc 0 · 멈춤 없음 · 주 숫자 = 변이 없는 주 판정 V01 과 같음) · <V>_UNCHECKED (차단 표지) ·
    <V>_SENSITIVE 아님 (이름 비교 안 함) · 변이 판정 NOT_COMPUTED (돌림 = checked) · 사유 = 변이 판정 NOT_COMPUTED (§5-6 ③) · §7-1 문장 금지 ·
    판정 입력 기록에 그 변이의 멈춘 단계 (STOPPED)."""
    P, R = v['v'] or {}, v['r'] or {}
    main_r = s_verdict_main()['r'] or {}
    pv = (P.get('variants') or {}).get(V) or {}
    rs = P.get('blocking_reasons') or {}
    fl = P.get('flags') or []
    stopped_in = [x for x in P.get('inputs') or [] if isinstance(x, dict) and x.get('variant') == V and x.get('status') == 'STOPPED']
    ok = (v['rc'] == 0 and P.get('stop') is None and P.get('verdict') == 'PASS_INFORMATIVE'
          and f'{V}_UNCHECKED' in fl and f'{V}_UNCHECKED' in (P.get('blocking_flags') or []) and f'{V}_SENSITIVE' not in fl
          and pv.get('checked') is True and pv.get('verdict') == 'NOT_COMPUTED' and pv.get('grade_changed') is None
          and pv.get('flag') == f'{V}_UNCHECKED' and str(rs.get(f'{V}_UNCHECKED', '')).startswith('변이 판정 NOT_COMPUTED')
          and P.get('sentence_allowed') is False and len(stopped_in) >= 1
          and R.get('interval_mScm') is not None and R.get('interval_mScm') == main_r.get('interval_mScm') and R.get('W') == main_r.get('W')
          and ((R.get('variants') or {}).get(V) or {}).get('verdict') == 'NOT_COMPUTED'
          and P.get('sentence') == want_sentence('positive', 'PASS_INFORMATIVE', V21_BLK, sens=True))
    return ok, (v['rc'], P.get('verdict'), (P.get('stop') or {}).get('code'), fl, pv, rs.get(f'{V}_UNCHECKED'), len(stopped_in),
                P.get('sentence'))


def eval_V21(tag):
    lv = run_V21_ladders()
    fix = (lv[0]['rc'] == 3 and (lv[0]['sum'] or {}).get('status') == 'STOPPED' and stop_code(lv[0]) == 'RUNNER_RC'
           and ((lv[0]['sum'] or {}).get('after_main') or {}).get('summary_sha256') and (lv[1]['sum'] or {}).get('status') == 'CALIBRATED')
    ok, why = stopped_variant_ok(verdict(tag, main_dirs() + [x['out'] for x in lv]), 'FIBRE')
    return bool(fix) and ok, (bool(fix), why)


def eval_V22(tag):
    p = run_V22_predict()
    s = p['sum'] or {}
    fix = (p['rc'] == 3 and s.get('status') == 'STOPPED' and stop_code(p) == 'RUNNER_RC' and s.get('ladders')
           and (s.get('after_main') or {}).get('summary_sha256'))
    ok, why = stopped_variant_ok(verdict(tag, main_dirs() + [p['out']]), 'SVORDER')
    return bool(fix) and ok, (bool(fix), why)


@check('V21', '★ RI (§5-6 ③) — 감도 FIBRE 사다리 P0 가 멈춤 (러너 rc 2 · RUNNER_RC · STOPPED) · P1 보정됨 → 판정 = 주 판정 (rc 0 · 주 숫자 같음) + '
               'FIBRE_UNCHECKED (변이 판정 NOT_COMPUTED · 이름 비교 안 함 · 차단) · 문장 = 결정표 오른쪽 칸 · 다시 판정 같음 (4판 사슬 = '
               'INPUT_STAGE_STOPPED 로 판정 전체 거부)')
def t_V21():
    ok, why = eval_V21('V21_v')
    rc, so = call(['--stage', 'verdict', '--reverify', Path(TD) / 'runs' / 'V21_v', '--registration', FX['reg_ok']])
    return ok and rc == 0 and 'REVERIFY_SAME' in so, (why, rc, so[-200:])


@check('V22', '★ RI (§5-6 ③) — 감도 SVORDER 예측이 멈춤 (주 묶음 기록 뒤 · 첫 DBE 모서리 러너 rc 2 · STOPPED) → 판정 = 주 판정 + SVORDER_UNCHECKED '
               '(변이 판정 NOT_COMPUTED · 차단 · 4판 사슬 = INPUT_STAGE_STOPPED)')
def t_V22():
    return eval_V22('V22_v')


def eval_V23(ta, tb):
    t_P03()
    out = []
    for r in (verdict(ta, [run_S02()['out'], s_main('P1')['out']]),
              verdict(tb, [s_main('P0')['out'], s_main('P1')['out'], SCEN['P03']['out']])):
        P = r['v'] or {}
        rs = P.get('reasons') or []
        out.append((r['rc'] == 3 and P.get('verdict') == 'NOT_COMPUTED' and stop_code(r) == 'INPUT_STAGE_STOPPED' and r['r'] is None
                    and P.get('sentence') == T_NC and len(rs) == 1 and rs[0].get('code') == 'INPUT_STAGE_STOPPED',
                    (r['rc'], stop_code(r), P.get('sentence'), rs)))
    return all(o[0] for o in out), [o[1] for o in out]


@check('V23', '★ RI (§5-5 사슬 멈춤 행 · 그대로) — 주 판정 단계의 멈춤은 여전히 판정 전체 NOT_COMPUTED: 주 사다리 P0 멈춤 (S02 · RUNNER_RC) · 주 예측 '
               '멈춤 (P03 · SAME_P_CONSISTENCY) → INPUT_STAGE_STOPPED · rc 3 · 결과 파일 없음 · 문장 = NOT_COMPUTED 칸 · 사유 = 멈춤 코드')
def t_V23():
    return scen('V23', lambda: eval_V23('V23a', 'V23b'))


@check('V24', '★ RI — 멈춘 변이 단계도 판정 입력 검사는 그대로 (4판 사슬은 그 검사 전에 판정 전체를 거부했다): 주 예측 묶음을 기록하기 전에 멈춘 '
               'SVORDER 예측 (F01b · MAIN_NOT_DONE · after_main 없음) → MAIN_BINDING · 판정 NOT_COMPUTED · rc 3 (등록이 정하지 않은 자리 = 지금 동작)')
def t_V24():
    t_F01()
    f = SCEN['F01b']['sum'] or {}
    r = scen('V24', lambda: verdict('V24', main_dirs() + [SCEN['F01b']['out']]))
    P = r['v'] or {}
    return (r['rc'] == 3 and P.get('verdict') == 'NOT_COMPUTED' and stop_code(r) == 'MAIN_BINDING' and r['r'] is None
            and f.get('status') == 'STOPPED' and f.get('variant') == 'SVORDER' and f.get('after_main') is None,
            (r['rc'], stop_code(r), f.get('status'), f.get('after_main')))


# ── Z 해 상태 · C 두 계획 · N 계획 숫자 · F 단계 순서 (가짜 러너) ──
def z_world(tag, states):
    return world(tag, dict(PW, states=states))


@check('Z01', '바닥 VALID_ZERO_TOPOLOGY (조기 반환 · σ 0 · 증서 영값) — 정본 계약 (ca_ext_record_ok · check_arm) 통과 · 사슬이 받아 사다리 계속 · '
               'CALIBRATED · 상태 기록 zero (등록 R §5-0 ② — 2판 = ARM_UNREADABLE · NOT_COMPUTED 멈춤)')
def t_Z01():
    r = scen('Z01', lambda: ladder('Z01', z_world('Z01', [{'match': {'rj': 'inf'}, 'state': 'zero'}])))
    L = lad(r)
    f0 = ((r['sum'] or {}).get('runs') or [{}])[0]
    return (r['rc'] == 0 and r['sum']['status'] == 'CALIBRATED' and L.get('states', {}).get('inf') == 'zero'
            and (f0.get('arms_read') or [{}])[0].get('state') == 'zero' and roles(r)[:2] == ['floor', 'ceiling'],
            (r['rc'], r['sum'] and r['sum']['status'], stop_code(r), L.get('states')))


#: ★ 4판 (10-21 · 1저자 Q1 "권고대로" · 등록 R 4판 §5-0 ①–③ · §4-2 ③ · R4-Q5) — 단락 (ELECTRODE_SHORT) = 생산자 미게시 → 그 런 = NOT_COMPUTED ·
#   사유 = 상태 이름 ELECTRODE_SHORT (+∞ 로 판정에 오지 않는다 · 다른 멈춤 이름 (RUNNER_RC · CA_EXT_RECORD …) 으로 흐리지 않는다)
SHORT = 'ELECTRODE_SHORT'


def stop_rec(res):
    return (res.get('sum') or res.get('v') or {}).get('stop') or {}


def eval_short_stage(r, stage_status_key='status', role=None):
    """단계 하나가 단락 팔에서 등록 결과 NOT_COMPUTED (사유 ELECTRODE_SHORT) 로 끝났나 — 러너 rc 0 (팔은 정본 계약을 지났다) · 멈춘 런 = 그 런."""
    s = r.get('sum') or {}
    st = stop_rec(r)
    runs = s.get('runs') or []
    hit = [x for x in runs if x.get('name') == st.get('run')]
    ok = (r['rc'] == 3 and s.get(stage_status_key) == 'NOT_COMPUTED' and st.get('code') == 'NOT_COMPUTED' and st.get('reason') == SHORT
          and len(hit) == 1 and hit[0].get('rc') == 0 and bool(hit[0].get('arms_read')) and SHORT in str(st.get('cause'))
          and (role is None or hit[0].get('role') == role))
    return ok, (r['rc'], s.get(stage_status_key), st, [(x.get('role'), x.get('rc')) for x in runs][-3:])


def eval_short_verdict(v, stage, law=None):
    """판정 = 등록 결과 NOT_COMPUTED (rc 0 · 멈춤 아님) · 사유 기록 (stage · law · code NOT_COMPUTED · reason ELECTRODE_SHORT) · 결과에 +∞ 구간 없음."""
    p = v.get('v') or {}
    rs = [x for x in (p.get('reasons') or []) if isinstance(x, dict)]
    want = [x for x in rs if x.get('stage') == stage and x.get('law') == law and x.get('code') == 'NOT_COMPUTED' and x.get('reason') == SHORT]
    ok = (v['rc'] == 0 and p.get('verdict') == 'NOT_COMPUTED' and p.get('state') == 'calib' and p.get('stop') is None and len(want) == 1
          and 'interval_mScm' not in (v.get('r') or {}))
    return ok, (v['rc'], p.get('verdict'), p.get('stop'), rs, sorted((v.get('r') or {}))[:6])


@check('Z02', '★ 4판 (Q1 · §5-0 ② · R4-Q5) 천장 ELECTRODE_SHORT (J11 · 생산자 미게시) — 사다리 = NOT_COMPUTED (등록 결과 · 사유 ELECTRODE_SHORT · '
               '바닥 · 천장 두 런 뒤 · 천장 런 rc 0 = 팔은 정본 계약을 지났다) · 판정 (P1 주 사다리와) = NOT_COMPUTED rc 0 · 사유 기록 '
               '(3판 = 받아서 σ +∞ · CALIBRATED)')
def t_Z02():
    r = scen('Z02', lambda: ladder('Z02', z_world('Z02', [{'match': {'rj': '0'}, 'state': 'short'}])))
    ok1, why1 = eval_short_stage(r, role='ceiling')
    v = scen('Z02_v', lambda: verdict('Z02_v', [r['out'], s_main('P1')['out']]))
    ok2, why2 = eval_short_verdict(v, 'ladder', 'P0')
    ok3 = roles(r) == ['floor', 'ceiling'] and '0' not in lad(r).get('states', {}) and (v['v'] or {}).get('calib') == {
        'P0': 'NOT_COMPUTED', 'P1': 'CALIBRATED'}
    return ok1 and ok2 and ok3, (why1, why2, roles(r), lad(r).get('states'))


def z_pred(tag, states):
    def go():
        p = predict(tag, world(tag, dict(PW, states=states)), [s_main('P0')['out'], s_main('P1')['out']])
        return {'pred': p, 'ver': verdict(tag + '_v', [s_main('P0')['out'], s_main('P1')['out'], p['out']])}
    return scen(tag, go)


@check('Z03', 'DBE 모서리 하나 VALID_ZERO_TOPOLOGY (P0 c0 R_j,hi) — 확장 실수 0 그대로 구간에 · W +∞ · 4.68 ∈ U → UNINFORMATIVE · p · S null · '
               '상태 extended · 그 모서리 origin 팔도 0 (산포 0)')
def t_Z03():
    sc = z_pred('Z03', [{'match': {'kit_has': 'DBE', 'law': 'P0', 'c': '0', 'rj': lad(s_main('P0'))['R_j_hi']}, 'state': 'zero'}])
    v, r = sc['ver']['v'] or {}, sc['ver']['r'] or {}
    return (sc['pred']['sum']['status'] == 'PREDICTED' and v.get('verdict') == 'UNINFORMATIVE' and v.get('state') == 'extended'
            and r.get('W') is None and r.get('p') is None and r.get('S') is None and r.get('interval_mScm', [None])[0] == 0.0
            and (r.get('corners_state') or {}).get('c0_P0', {}).get('R_j_hi') == 'zero',
            (v.get('verdict'), v.get('state'), v.get('stop'), r.get('interval_mScm')))


@check('Z04', '★ 4판 (Q1 · §5-0 ③) DBE 모서리 하나 ELECTRODE_SHORT (P1 c1 R_j,0 · c 1 축약) — 예측 = NOT_COMPUTED (등록 결과 · 사유 '
               'ELECTRODE_SHORT · 그 모서리 런에서 멈춤) · 판정 = NOT_COMPUTED rc 0 · 사유 기록 (예측 단계) · +∞ 구간 없음 '
               '(3판 = σ +∞ · UNINFORMATIVE)')
def t_Z04():
    sc = z_pred('Z04', [{'match': {'kit_has': 'DBE', 'law': 'P1', 'c': '1', 'rj': lad(s_main('P1'))['R_j0']}, 'state': 'short'}])
    ok1, why1 = eval_short_stage(sc['pred'], role='corner')
    ok2, why2 = eval_short_verdict(sc['ver'], 'predict')
    return ok1 and ok2, (why1, why2)


@check('Z05', '★ 4판 (Q1 · §4-2 ③) DBE origin 팔 (arm 1 · 2 · P0 c1 R_j,0 · c 1 축약 모서리) 이 ELECTRODE_SHORT — origin 값으로 단락이 오지 '
               '않는다 → 예측 = NOT_COMPUTED (사유 ELECTRODE_SHORT · origin 런에서 멈춤) · 판정 = NOT_COMPUTED rc 0 (3판 = 산포 +∞ → 8 팔 평균)')
def t_Z05():
    sc = z_pred('Z05', [{'match': {'kit_has': 'DBE', 'law': 'P0', 'c': '1', 'rj': lad(s_main('P0'))['R_j0'], 'arms': 2},
                         'state': 'short'}])
    ok1, why1 = eval_short_stage(sc['pred'], role='origin')
    ok2, why2 = eval_short_verdict(sc['ver'], 'predict')
    return ok1 and ok2, (why1, why2)


@check('Z07', '★ 4판 (Q1) 사슬의 등록 풀이 상태 셋 (§5-0) — 생산자 기록 상태 (run_contract.next_gen_state) positive · zero · short → '
               'POSITIVE_SOLVED · VALID_ZERO_TOPOLOGY · NOT_COMPUTED (사유 ELECTRODE_SHORT = 생산자 상태 상수) · 상태 안 섬 (None) = NOT_COMPUTED')
def t_Z07():
    import run_contract as RCm
    import step3_conv_cert as CCm
    f = getattr(RR, 'registration_state', None)
    if not callable(f):
        return False, 'registration_state 없음'
    got = {k: f(k) for k in ('positive', 'zero', 'short', None)}
    want = {'positive': ('POSITIVE_SOLVED', None), 'zero': ('VALID_ZERO_TOPOLOGY', None), 'short': ('NOT_COMPUTED', CCm.STATUS_SHORT),
            None: ('NOT_COMPUTED', None)}
    return (got == want and CCm.STATUS_SHORT == SHORT and set(RCm.NG_STATES) == {'positive', 'zero', 'short'}
            and CCm.STATUS_POSITIVE == 'POSITIVE_SOLVED' and CCm.STATUS_ZERO == 'VALID_ZERO_TOPOLOGY', (got, RCm.NG_STATES))


def s0_variant(tag, mutate=None, raw=None):
    """S0 계획 변이 파일 → 경로 (mutate = 정준 바이트로 다시 쓴 손댄 내용 · raw = 그대로 쓸 바이트)."""
    import ca_s0_census as S0m
    p = Path(TD) / f's0_{tag}.json'
    if raw is not None:
        p.write_bytes(raw)
    else:
        obj = copy.deepcopy(FX['s0_obj'])
        mutate(obj)
        p.write_bytes(S0m.plan_bytes_of(obj))
    return p


def c_case(tag, code, **kw):
    r = scen(tag, lambda: ladder(tag, world(tag), **kw))
    return (r['rc'] == 3 and stop_code(r) == code and n_calls(r['world']) == 0, (r['rc'], stop_code(r), (r['sum'] or {}).get('stop')))


@check('C01', '두 계획 대조 — S0 계획이 정준 바이트가 아님 (같은 내용 · 들여쓰기) → S0_PLAN_INVALID · 러너 0 회')
def t_C01():
    return c_case('C01', 'S0_PLAN_INVALID', s0=s0_variant('C01', raw=json.dumps(FX['s0_obj'], indent=1, sort_keys=True).encode()))


@check('C02', 'S0 계획 식 위반 (tol_ff ≠ min(u, r_f) · 정준 바이트로 다시 써도) → S0_PLAN_INVALID (정본 ca_s0_census.check_plan)')
def t_C02():
    return c_case('C02', 'S0_PLAN_INVALID', s0=s0_variant('C02', mutate=lambda o: o['values_um'].update(tol_ff=0.04)))


@check('C03', '등록 §2-1 | S0 계획 해시 | 칸 ⬜ → S0_PLAN_HASH_UNREGISTERED · 러너 0 회')
def t_C03():
    return c_case('C03', 'S0_PLAN_HASH_UNREGISTERED', reg=FX['reg_s0_unreg'])


@check('C04', 'S0 계획 sha256 ≠ 등록 칸 → S0_PLAN_HASH_MISMATCH')
def t_C04():
    return c_case('C04', 'S0_PLAN_HASH_MISMATCH', reg=FX['reg_s0_other'])


def c_plan(tag, code, **over):
    p, _sha, reg = plan_set(tag, **over)
    return c_case(tag, code, plan=p, reg=reg)


@check('C05', 'R 계획 tol_ff_um 0.04 ≠ S0 values_um.tol_ff 0.05 (같은 float 이어야) → PLAN_CROSS_MISMATCH (§2-1 · §10-2 ⑪)')
def t_C05():
    return c_plan('C05', 'PLAN_CROSS_MISMATCH', tol_ff_um=0.04)


@check('C06', 'R 계획 step3_rtol 1e-13 ≠ §3-5 봉인 CERT_RTOL_MAX 1e-12 → PLAN_CROSS_MISMATCH')
def t_C06():
    return c_plan('C06', 'PLAN_CROSS_MISMATCH', step3_rtol=1e-13)


@check('C07', 'R 계획 len_law len_scaled_v1 ≠ 등록 v0 길이 법칙 (carbon_junction.CJUNC_LEN_LAW) → PLAN_CROSS_MISMATCH')
def t_C07():
    return c_plan('C07', 'PLAN_CROSS_MISMATCH', len_law='len_scaled_v1')


@check('C08', '--s0-plan 없음 → 인자 오류 (rc 2) · 러너 0 회 (두 계획 대조 없이 σ 런 없음)')
def t_C08():
    w = world('C08')
    out = Path(TD) / 'runs' / 'C08'
    rc, _so = call(['--stage', 'ladder', '--law', 'P0', '--runner', FX['runner'], '--root', FX['root'], '--plan', FX['plan'],
                    '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out] + s0_args(), w)
    return rc == 2 and n_calls(w) == 0 and not out.exists(), (rc, n_calls(w))


@check('C09', 'S0 계획 schema 다름 (ca-cjunc-plan-v0) → S0_PLAN_INVALID')
def t_C09():
    return c_case('C09', 'S0_PLAN_INVALID', s0=s0_variant('C09', mutate=lambda o: o.update(schema='ca-cjunc-plan-v0')))


@check('N01', '결과 전 등록 숫자 넷 (점 수 상한 · 역상 R 비 상한 · SV 문턱 · 범위) 중 하나라도 null (⬜) → PLAN_NUMBER_UNREGISTERED · 러너 0 회 '
               '(★ Q-G: SV 문턱이 ⬜ 인 채로 DBE 단계에 못 간다)')
def t_N01():
    rs = [c_plan(f'N01_{k}', 'PLAN_NUMBER_UNREGISTERED', **{k: None}) for k in
          ('max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold', 'sv_cf_scope')]
    return all(x[0] for x in rs), [x[1] for x in rs]


@check('N02', '옛 계획 rint-r-plan-v1 (칸 일곱) → PLAN_INVALID (3판 사슬은 결과 전 등록 숫자 칸 없이 돌지 않는다)')
def t_N02():
    p = Path(TD) / 'plan_v1.json'
    old = {k: v for k, v in FX['plan_obj'].items() if k in ('schema', 'len_law', 'unreg_law', 's_min_um', 'tol_ff_um', 'step3_rtol',
                                                           'p2_extra')}
    old['schema'] = 'rint-r-plan-v1'
    p.write_text(json.dumps(old, indent=1, sort_keys=True), encoding='utf-8')
    reg = FX['reg_with'](f'`{hashlib.sha256(p.read_bytes()).hexdigest()}`', 'reg_plan_v1.md')
    return c_case('N02', 'PLAN_INVALID', plan=p, reg=reg)


@check('N03', '계획 숫자 꼴 — 점 수 0 · True · 역상 비 상한 1.0 · "None" · SV 문턱 0.5 · 범위 R_j_lo → PLAN_INVALID (값을 고치지 않는다)')
def t_N03():
    rs = [c_plan(f'N03_{i}', 'PLAN_INVALID', **{k: v}) for i, (k, v) in enumerate(
        (('max_ladder_points', 0), ('max_ladder_points', True), ('calib_rj_ratio_max', 1.0), ('calib_rj_ratio_max', 'None'),
         ('sv_cf_threshold', 0.5), ('sv_cf_scope', 'R_j_lo')))]
    return all(x[0] for x in rs), [x[1] for x in rs]


def _n_safe(tag, fn):
    """한 꼴의 결과 (멈춤 이름 · 러너 호출) — 잡히지 않은 예외도 그 꼴의 실패로 기록 (한 꼴의 예외가 다른 꼴을 가리지 않게)."""
    try:
        return fn()
    except Exception as e:                                  # noqa: BLE001
        return False, f'{tag}: 잡히지 않은 {type(e).__name__}: {str(e)[:80]}'


def _n_raw_plan(tag, text):
    """계획 바이트 그대로 (중복 칸 꼴) → (경로, sha256, 그 해시를 채운 등록 사본)."""
    p = Path(TD) / f'{tag}.json'
    p.write_bytes(text.encode('utf-8'))
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    return p, sha, FX['reg_with'](f'`{sha}`', f'reg_{tag}.md')


@check('N04', '★ PF2 E (10-22 · PRE2-impl-03) 계획 넘침 — 정수 10**400 (SV 문턱 · s_min · tol_ff · rtol · 역상 비 상한 · 점 수 상한) · -10**400 '
              '(s_min) → PLAN_INVALID (구조화 멈춤 · rc 3 · 러너 0 회 · 옛 = 잡히지 않은 OverflowError · 점 수 상한 = 받음)')
def t_N04():
    cases = [(k, 10 ** 400) for k in ('sv_cf_threshold', 's_min_um', 'tol_ff_um', 'step3_rtol', 'calib_rj_ratio_max', 'max_ladder_points')]
    cases.append(('s_min_um', -10 ** 400))
    rs = [_n_safe(f'N04_{i}', lambda k=k, v=v, i=i: c_plan(f'N04_{i}', 'PLAN_INVALID', **{k: v})) for i, (k, v) in enumerate(cases)]
    return all(x[0] for x in rs), [(cases[i][0], x[1]) for i, x in enumerate(rs) if not x[0]]


@check('N05', '★ PF2 E (10-22 · PRE2-impl-03) 계획 중복 칸 — "sv_cf_threshold": 2.0 … "sv_cf_threshold": 50.0 (사람 = 앞 · 옛 사슬 = 뒤) · 앞에 '
              '덧붙인 꼴 → PLAN_INVALID (rc 3 · 러너 0 회 · 옛 = 마지막 값으로 받음)')
def t_N05():
    base = json.dumps(FX['plan_obj'], indent=1, sort_keys=True)
    tail = base.rstrip().rstrip('}').rstrip() + ',\n "sv_cf_threshold": 50.0\n}'
    head = base.replace('{', '{\n "s_min_um": 0.9,', 1)
    rs = []
    for i, txt in enumerate((tail, head)):
        p, _sha, reg = _n_raw_plan(f'N05_{i}', txt)
        rs.append(_n_safe(f'N05_{i}', lambda p=p, reg=reg, i=i: c_case(f'N05_{i}', 'PLAN_INVALID', plan=p, reg=reg)))
    return all(x[0] for x in rs), [x[1] for x in rs if not x[0]]


@check('N06', '★ PF2 E (10-22 · PRE2-impl-03 같은 부류) S0 보고 중복 칸 — 단계 2 보고에 plan 이 둘 (앞 = 다른 계획 · 뒤 = 이 계획) · 단계 1 보고에 code 가 '
              '둘 (앞 = 다른 지문) → S0_REPORT_MISMATCH (rc 3 · 러너 0 회 · 옛 = 마지막 값으로 받음)')
def t_N06():
    import ca_s0_census as S0m
    good2 = json.loads(Path(s0_stage2_for(FX['plan'])).read_text(encoding='utf-8'))
    bad_plan = dict(good2['plan'], r_plan=dict(good2['plan']['r_plan'], sha256='0' * 64))
    txt2 = '{"plan": ' + json.dumps(bad_plan) + ', ' + json.dumps(good2)[1:]
    good1 = json.loads(Path(FX['s1']).read_text(encoding='utf-8'))
    bad_code = dict(good1['code'], file_digests=[{'file': nm, 'sha256': '0' * 64} for nm in S0_SAME7])
    txt1 = '{"code": ' + json.dumps(bad_code) + ', ' + json.dumps(good1)[1:]
    has1 = chain_has(S0_STAGE1_OPT)
    a = _n_safe('N06a', lambda: c_case('N06a', 'S0_REPORT_MISMATCH', s2=s0_report(2, 'N06a', raw=txt2.encode('utf-8'))))
    b = _n_safe('N06b', lambda: c_case('N06b', 'S0_REPORT_MISMATCH', s1=(s0_report(1, 'N06b', raw=txt1.encode('utf-8')) if has1 else None)))
    return (a[0] and b[0] and has1 and good2.get('schema') == S0m.SCHEMA, (a[1], b[1], has1))


@check('F01', 'Q-F — 감도 변이 사다리 · 예측에 --after-main 이 없다 → MAIN_NOT_DONE · 러너 0 회 (주 판정 단계 뒤에만)')
def t_F01():
    a = c_case('F01a', 'MAIN_NOT_DONE', variant='FIBRE', after='')
    r = scen('F01b', lambda: predict('F01b', world('F01b'), [s_main('P0')['out'], s_main('P1')['out']], variant='SVORDER', after=''))
    return a[0] and r['rc'] == 3 and stop_code(r) == 'MAIN_NOT_DONE' and n_calls(r['world']) == 0, (a[1], stop_code(r))


@check('F02', 'Q-F — --after-main 이 주 예측이 아님 (사다리 폴더 · 멈춘 예측 P03) → MAIN_NOT_DONE · 러너 0 회')
def t_F02():
    a = c_case('F02a', 'MAIN_NOT_DONE', variant='UNREG', after=str(s_main('P0')['out']))
    t_P03()
    b = c_case('F02b', 'MAIN_NOT_DONE', variant='UNREG', after=str(SCEN['P03']['out']))
    return a[0] and b[0], (a[1], b[1])


@check('F03', 'Q-F — 판정: 감도 단계가 묶인 주 예측 (after_main sha256) ≠ 판정 입력의 주 예측 → MAIN_BINDING · 판정 NOT_COMPUTED')
def t_F03():
    def go():
        vs = s_variant_set('FIBRE')
        dst = Path(TD) / 'runs' / 'F03_pred'
        shutil.copytree(vs['pred']['out'], dst)
        sp = dst / 'predict_summary.json'
        s = json.loads(sp.read_text(encoding='utf-8'))
        s['after_main']['summary_sha256'] = '0' * 64
        sp.write_text(json.dumps(s, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
        return verdict('F03', list(main_dirs()) + [o['out'] for o in vs['ladders']] + [dst])
    r = scen('F03', go)
    return (r['rc'] == 3 and stop_code(r) == 'MAIN_BINDING' and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED', (r['rc'], stop_code(r)))


@check('F04', '--after-main 은 --variant 와만 (주 단계에 주면 인자 오류 rc 2)')
def t_F04():
    w = world('F04')
    rc, _so = call(['--stage', 'ladder', '--law', 'P0', '--runner', FX['runner'], '--root', FX['root'], '--plan', FX['plan'],
                    '--s0-plan', FX['s0'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', Path(TD) / 'runs' / 'F04',
                    '--after-main', str(s_main_predict()['out'])] + s0_args(), w)
    return rc == 2 and n_calls(w) == 0, rc


# ── ★ PF2 B (10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 탐침 E · 1저자 Q2 권고대로) 단계 2 보고의 봉인 계획 해시 ↔ 지금 계획 ──
def b_plan_B():
    """탐침 E 의 계획 B (s_min 0.6 → 0.9 · SV 문턱 2.0 → 3.0 · 점 수 16 → 20 · maxiter 60000 → 90000) — 단계 2 뒤 다시 등록 (등록 줄 = B)."""
    return scen('b_planB', lambda: plan_set('planB', s_min_um=0.9, sv_cf_threshold=3.0, max_ladder_points=20,
                                            p2_extra='--step3-maxiter 90000'))


@check('B01', '탐침 E 꼴 — 단계 2 보고가 계획 A 를 봉인했는데 계획 B 를 다시 등록 (등록 줄 · 계획 파일 = B) → S0_REPORT_MISMATCH · 러너 0 회 '
              '(옛 사슬 = CALIBRATED · DBE 를 본 뒤 s_min · SV 문턱 · 점 수를 바꾼 계획도 돌았다)')
def t_B01():
    pB, _shaB, regB = b_plan_B()
    r = scen('B01', lambda: ladder('B01', world('B01'), plan=pB, reg=regB, s2=(s0_stage2_for(FX['plan']) if chain_has(S0_STAGE2_OPT)
                                                                             else None)))
    return (r['rc'] == 3 and stop_code(r) == 'S0_REPORT_MISMATCH' and n_calls(r['world']) == 0
            and (r['sum'] or {}).get('status') == 'STOPPED', (r['rc'], stop_code(r), n_calls(r['world']), (r['sum'] or {}).get('stop')))


@check('B02', '정상 — 같은 계획을 봉인한 단계 2 보고 → 사다리 CALIBRATED · 요약에 단계 2 기록 (보고 경로 · sha256 · 봉인 R 계획 sha256 = 계획 · '
              'S0 계획 sha256 · DBE 킷 · source commit:)')
def t_B02():
    s = s_main('P0')['sum'] or {}
    rec = ((s.get('s0_reports') or {}).get('stage2')) or {}
    p2 = s0_stage2_for(FX['plan'])
    return (s.get('status') == 'CALIBRATED' and rec.get('r_plan_sha256') == FX['plan_sha'] and rec.get('plan_sha256') == FX['s0_sha']
            and rec.get('kit') == DBE_KIT and rec.get('stage') == 2 and str(rec.get('plan_source', '')).startswith('commit:')
            and rec.get('sha256') == hashlib.sha256(Path(p2).read_bytes()).hexdigest() and rec.get('path') == str(Path(p2).resolve()),
            (s.get('status'), rec))


@check('B03', '단계 2 보고의 S0 계획 sha256 ≠ 지금 S0 계획 (R 계획은 같음) → S0_REPORT_MISMATCH · 러너 0 회')
def t_B03():
    p = s0_report(2, 'B03', plan_sha=FX['plan_sha'], s0_sha='1' * 64) if chain_has(S0_STAGE2_OPT) else None
    return c_case('B03', 'S0_REPORT_MISMATCH', s2=p)


@check('B04', '단계 2 보고 꼴 — 파일 없음 · JSON 아님 · NaN · 단계 1 보고 · 다른 schema · 다른 킷 (옛 kit_DBE) · r_plan 없음 · r_plan sha256 '
              '64 hex 아님 · source 가 commit: 아님 · 단계 bool → S0_REPORT_MISMATCH · 러너 0 회 (fail-closed)')
def t_B04():
    has = chain_has(S0_STAGE2_OPT)
    cases = (
        ('없음', lambda: Path(TD) / 'no_such_report.json'),
        ('JSON 아님', lambda: s0_report(2, 'B04b', raw=b'{not json')),
        ('NaN', lambda: s0_report(2, 'B04c', raw=json.dumps({'schema': 'x', 'stage': float('nan')}).encode())),
        ('단계 1', lambda: s0_report(1, 'B04d')),
        ('schema', lambda: s0_report(2, 'B04e', mutate=lambda r: r.update(schema='ca-s0-census-v1'))),
        ('킷', lambda: s0_report(2, 'B04f', kit='kit_DBE')),
        ('r_plan 없음', lambda: s0_report(2, 'B04g', mutate=lambda r: r['plan'].pop('r_plan'))),
        ('r_plan sha256', lambda: s0_report(2, 'B04h', mutate=lambda r: r['plan']['r_plan'].update(sha256=FX['plan_sha'].upper()))),
        ('source', lambda: s0_report(2, 'B04i', mutate=lambda r: r['plan'].update(source='stage1_computed'))),
        ('단계 bool', lambda: s0_report(2, 'B04j', mutate=lambda r: r.update(stage=True))),
    )
    rs = [(nm, c_case(f'B04_{i}', 'S0_REPORT_MISMATCH', s2=(fn() if has else None))) for i, (nm, fn) in enumerate(cases)]
    return all(x[1][0] for x in rs), [(nm, x[1]) for nm, x in rs if not x[0]]


def b_tamper_copy(src, tag, name, fn):
    """단계 폴더 사본 (요약만 손댐 · 팔 JSON 은 그대로) → 경로."""
    dst = Path(TD) / 'runs' / tag
    shutil.copytree(src, dst)
    sp = dst / name
    s = json.loads(sp.read_text(encoding='utf-8'))
    fn(s)
    sp.write_text(json.dumps(s, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    return dst


def _b_set_r(s, v='0' * 64):
    s['s0_reports']['stage2']['r_plan_sha256'] = v


@check('B05', '예측 — 사다리 요약 둘의 단계 2 봉인 R 계획 sha256 이 계획과 다르다 (요약 손댐) → S0_REPORT_MISMATCH · 러너 0 회 · 한 사다리만 '
              '다르면 (두 사다리 기록 다름) → S0_REPORT_MISMATCH')
def t_B05():
    def go():
        a = [b_tamper_copy(s_main(law)['out'], f'B05_{law}', 'ladder_summary.json', _b_set_r) for law in ('P0', 'P1')]
        b = b_tamper_copy(s_main('P1')['out'], 'B05_P1b', 'ladder_summary.json', _b_set_r)
        return (predict('B05', world('B05'), a), predict('B05x', world('B05x'), [s_main('P0')['out'], b]))
    r, rx = scen('B05', go)
    return (r['rc'] == 3 and stop_code(r) == 'S0_REPORT_MISMATCH' and n_calls(r['world']) == 0
            and rx['rc'] == 3 and stop_code(rx) == 'S0_REPORT_MISMATCH' and n_calls(rx['world']) == 0,
            (r['rc'], stop_code(r), rx['rc'], stop_code(rx)))


@check('B06', '판정 — 예측 요약의 단계 2 봉인 R 계획 sha256 손댐 → 판정 NOT_COMPUTED (S0_REPORT_MISMATCH · rc 3) · 손대지 않은 같은 묶음 = '
              '판정 (B 대조가 정상 묶음을 막지 않는다)')
def t_B06():
    def go():
        d = b_tamper_copy(s_main_predict()['out'], 'B06_pred', 'predict_summary.json', _b_set_r)
        return verdict('B06', [s_main('P0')['out'], s_main('P1')['out'], d])
    r = scen('B06', go)
    v0 = s_verdict_main()
    return (r['rc'] == 3 and stop_code(r) == 'S0_REPORT_MISMATCH' and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED'
            and v0['rc'] == 0 and (v0['v'] or {}).get('verdict') == 'PASS_INFORMATIVE', (r['rc'], stop_code(r), v0['rc']))


@check('B07', '사다리 — --s0-stage2-report 없음 → 인자 오류 (rc 2) · 러너 0 회 · 출력 폴더 없음 (단계 2 봉인 대조 없이 σ 런 없음)')
def t_B07():
    w = world('B07')
    out = Path(TD) / 'runs' / 'B07'
    rc, _so = call(['--stage', 'ladder', '--law', 'P0', '--target', '1.63', '--runner', FX['runner'], '--root', FX['root'],
                    '--plan', FX['plan'], '--s0-plan', FX['s0'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out], w)
    return rc == 2 and n_calls(w) == 0 and not out.exists() and chain_has(S0_STAGE2_OPT), (rc, n_calls(w), chain_has(S0_STAGE2_OPT))


@check('B08', 'dry-run 도 대조 — 계획 B (단계 2 = 계획 A) + --dry-run → S0_REPORT_MISMATCH (rc 3 · env 를 찍지 않는다)')
def t_B08():
    pB, _shaB, regB = b_plan_B()
    w = world('B08')
    out = Path(TD) / 'runs' / 'B08'
    rc, so = call(['--stage', 'ladder', '--law', 'P0', '--target', '1.63', '--runner', FX['runner'], '--root', FX['root'],
                   '--plan', pB, '--s0-plan', FX['s0'], '--registration', regB, '--max-hours', '1', '--out', out, '--dry-run']
                  + s0_args(FX['plan']), w)
    return (rc == 3 and 'S0_REPORT_MISMATCH' in so and 'CJUNC_RJ=' not in so and n_calls(w) == 0, (rc, so[-300:]))


@check('B09', '사슬 상수 = S0 보고 schema (ca_s0_census.SCHEMA · 사슬은 numpy 없이 뜬다)')
def t_B09():
    import ca_s0_census as S0m
    return getattr(RR, 'S0_REPORT_SCHEMA', None) == S0m.SCHEMA, (getattr(RR, 'S0_REPORT_SCHEMA', None), S0m.SCHEMA)


# ── ★ PF2 D (10-22 · 사전 리뷰 2 회차 PRE2-design-02 · 08 · 탐침 C · 결정 없음 · 등록 문장 그대로) 같은 판 대조 ──
#    단계 요약 = 코드 파일 지문 (sha256 · 사슬 폴더 · 러너 폴더) + 추적 파일 수정 여부 (git dirty) → 다음 단계 · 판정 계산기가 지금과 대조 ·
#    R 런 ↔ S0 단계 1 · 2 보고의 census · registry 일곱 파일 지문 (등록 R §2-1b).  옛 사슬 = HEAD 만 보고 dirty · 파일을 안 본다.
@contextlib.contextmanager
def d_identity(dirty=True, head=None):
    """사슬 git 신원 바꿔 끼우기 (진짜 HEAD · dirty 만 바꿈 · head 를 주면 그것도) — 끝나면 고정물 신원 (dirty False) 으로."""
    orig = RR.git_identity

    def g(path, _g=FX['git_identity_real']):
        r = dict(_g(path), dirty=dirty)
        if head is not None:
            r['head'] = head
        return r
    RR.git_identity = g
    try:
        yield
    finally:
        RR.git_identity = orig


@contextlib.contextmanager
def d_files(name='rint_r_chain.py', digest='0' * 64):
    """지금 코드 파일 지문 하나 바꿔 끼우기 (같은 HEAD · dirty False 인데 파일 내용이 다른 꼴) — 사슬에 지문 함수가 없으면 아무것도 안 한다
    (옛 사슬 = 지문을 안 봐 그대로 통과 → 시험 실패가 옳은 이유)."""
    orig = getattr(RR, 'code_files', None)
    if orig is not None:
        RR.code_files = lambda base, _f=orig: [dict(x, sha256=digest) if x.get('file') == name else x for x in _f(base)]
    try:
        yield
    finally:
        if orig is not None:
            RR.code_files = orig


def _d_set_files(s, name='rint_r_chain.py', v='0' * 64):
    """요약의 코드 파일 지문 하나 손댐 (옛 사슬 요약 = 칸이 없으면 칸을 만들어 넣는다 · 옛 사슬은 그 칸을 안 본다)."""
    files = (s.get('code') or {}).get('files')
    if not isinstance(files, list) or not files:
        s.setdefault('code', {})['files'] = [{'file': name, 'sha256': v}]
        return
    for x in files:
        if x.get('file') == name:
            x['sha256'] = v


def _d_set_digest(name, v='0' * 64):
    def fn(r):
        for x in r['code']['file_digests']:
            if x['file'] == name:
                x['sha256'] = v
    return fn


@check('D01', '탐침 C 꼴 — 깨끗한 트리로 사다리 둘 + 예측 → 같은 HEAD · dirty (추적 파일 고침) + 판정 문턱 한 줄 (G0/2 → 0.05) 로 판정 → '
              'CODE_PIN_MISMATCH · NOT_COMPUTED · rc 3 (옛 사슬 = rc 0 · CONSISTENT_WEAK · 멈춤 없음) · 같은 단계 · 깨끗한 판정 = PASS_INFORMATIVE')
def t_D01():
    def go():
        dirs = main_dirs()
        old = RR.GRADE_INFORMATIVE_MAX
        RR.GRADE_INFORMATIVE_MAX = 0.05
        try:
            with d_identity(dirty=True):
                return verdict('D01', dirs)
        finally:
            RR.GRADE_INFORMATIVE_MAX = old
    r = scen('D01', go)
    v0 = s_verdict_main()
    return (r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED'
            and v0['rc'] == 0 and (v0['v'] or {}).get('verdict') == 'PASS_INFORMATIVE',
            (r['rc'], stop_code(r), (r['v'] or {}).get('verdict'), v0['rc'], (v0['v'] or {}).get('verdict')))


@check('D02', '같은 HEAD · dirty False 인데 사슬 파일 지문이 다르다 + 판정 문턱 한 줄 → 판정 CODE_PIN_MISMATCH · NOT_COMPUTED · rc 3 '
              '(dirty 만 보면 놓치는 꼴 · 파일 지문 대조)')
def t_D02():
    def go():
        dirs = main_dirs()
        old = RR.GRADE_INFORMATIVE_MAX
        RR.GRADE_INFORMATIVE_MAX = 0.05
        try:
            with d_files('rint_r_chain.py'):
                return verdict('D02', dirs)
        finally:
            RR.GRADE_INFORMATIVE_MAX = old
    r = scen('D02', go)
    return (r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED',
            (r['rc'], stop_code(r), (r['v'] or {}).get('verdict')))


@check('D03', '사다리 — 추적 파일이 고쳐진 트리 (dirty) → CODE_PIN_MISMATCH · rc 3 · 러너 0 회 · 요약에 dirty True 기록')
def t_D03():
    def go():
        with d_identity(dirty=True):
            return ladder('D03', world('D03'))
    r = scen('D03', go)
    c = ((r['sum'] or {}).get('code') or {}).get('chain') or {}
    return (r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and n_calls(r['world']) == 0 and c.get('dirty') is True,
            (r['rc'], stop_code(r), n_calls(r['world']), c))


@check('D04', '예측 — 지금 트리 dirty (사다리 둘 = 깨끗) → CODE_PIN_MISMATCH · rc 3 · 러너 0 회')
def t_D04():
    def go():
        lads = [s_main('P0')['out'], s_main('P1')['out']]
        with d_identity(dirty=True):
            return predict('D04', world('D04'), lads)
    r = scen('D04', go)
    return (r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and n_calls(r['world']) == 0, (r['rc'], stop_code(r), n_calls(r['world'])))


@check('D05', '예측 — 지금 코드 파일 지문 ≠ 사다리 기록 (step3_sigma.py · 같은 HEAD) · 사다리 요약 둘의 지문 손댐 · 한 사다리만 손댐 (둘이 다름) '
              '→ 셋 다 CODE_PIN_MISMATCH · rc 3 · 러너 0 회')
def t_D05():
    def go():
        lads = [s_main('P0')['out'], s_main('P1')['out']]
        with d_files('step3_sigma.py'):
            a = predict('D05a', world('D05a'), lads)
        t = [b_tamper_copy(s_main(law)['out'], f'D05_{law}', 'ladder_summary.json', lambda s: _d_set_files(s, 'carbon_junction.py'))
             for law in ('P0', 'P1')]
        b = predict('D05b', world('D05b'), t)
        c = predict('D05c', world('D05c'), [s_main('P0')['out'], t[1]])
        return a, b, c
    rs = scen('D05', go)
    return (all(r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and n_calls(r['world']) == 0 for r in rs),
            [(r['rc'], stop_code(r), n_calls(r['world'])) for r in rs])


@check('D06', '판정 — 예측 요약의 코드 파일 지문 손댐 · 사다리 요약의 dirty = True 손댐 → 둘 다 판정 CODE_PIN_MISMATCH · NOT_COMPUTED · rc 3')
def t_D06():
    def go():
        d = b_tamper_copy(s_main_predict()['out'], 'D06_pred', 'predict_summary.json', lambda s: _d_set_files(s, 'step3_conv_cert.py'))
        a = verdict('D06a', [s_main('P0')['out'], s_main('P1')['out'], d])
        e = b_tamper_copy(s_main('P1')['out'], 'D06_P1', 'ladder_summary.json',
                          lambda s: s.setdefault('code', {}).setdefault('chain', {}).update(dirty=True))
        b = verdict('D06b', [s_main('P0')['out'], e, s_main_predict()['out']])
        return a, b
    rs = scen('D06', go)
    return (all(r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED' for r in rs),
            [(r['rc'], stop_code(r), (r['v'] or {}).get('verdict')) for r in rs])


@check('D07', 'S0 단계 1 보고의 census · registry 지문 ≠ 지금 (carbon_junction.py) · 옛 다섯 파일 보고 (carbon_junction · ptfe_face_alpha 없음) → '
              'CODE_PIN_MISMATCH · rc 3 · 러너 0 회 · 멈춤 사유에 s_min 다시 고르기 금지 문장 (등록 R §2-1b)')
def t_D07():
    has = chain_has(S0_STAGE1_OPT)

    def old5(r):
        r['code']['file_digests'] = [x for x in r['code']['file_digests'] if x['file'] not in ('carbon_junction.py', 'ptfe_face_alpha.py')]
    a = c_case('D07a', 'CODE_PIN_MISMATCH', s1=(s0_report(1, 'D07a', mutate=_d_set_digest('carbon_junction.py')) if has else None))
    b = c_case('D07b', 'CODE_PIN_MISMATCH', s1=(s0_report(1, 'D07b', mutate=old5) if has else None))
    why = str(((scen('D07a', lambda: None)['sum'] or {}).get('stop') or {}).get('cause'))
    return has and a[0] and b[0] and 's_min' in why, (a[1], b[1], why[-240:])


@check('D08', 'S0 단계 1 보고 꼴 — 파일 없음 · JSON 아님 · 단계 2 보고 · 다른 schema · 다른 킷 (DBE) · source 가 stage1_computed 아님 · '
              '보고가 만든 S0 계획 ≠ 지금 S0 계획 · 단계 bool → S0_REPORT_MISMATCH · rc 3 · 러너 0 회')
def t_D08():
    has = chain_has(S0_STAGE1_OPT)
    cases = (
        ('없음', lambda: Path(TD) / 'no_such_s1.json'),
        ('JSON 아님', lambda: s0_report(1, 'D08b', raw=b'{not json')),
        ('단계 2', lambda: s0_report(2, 'D08c', kit=SBE_KIT)),
        ('schema', lambda: s0_report(1, 'D08d', mutate=lambda r: r.update(schema='ca-s0-census-v1'))),
        ('킷', lambda: s0_report(1, 'D08e', kit=DBE_KIT)),
        ('source', lambda: s0_report(1, 'D08f', mutate=lambda r: r['plan'].update(source='commit:' + 'a' * 40))),
        ('S0 계획', lambda: s0_report(1, 'D08g', s0_sha='1' * 64)),
        ('단계 bool', lambda: s0_report(1, 'D08h', mutate=lambda r: r.update(stage=True))),
    )
    rs = [(nm, c_case(f'D08_{i}', 'S0_REPORT_MISMATCH', s1=(fn() if has else None))) for i, (nm, fn) in enumerate(cases)]
    return has and all(x[1][0] for x in rs), [(nm, x[1]) for nm, x in rs if not x[0]]


@check('D09', 'S0 단계 2 보고의 census · registry 지문 ≠ 지금 (step3_sigma.py) → CODE_PIN_MISMATCH · rc 3 · 러너 0 회')
def t_D09():
    return c_case('D09', 'CODE_PIN_MISMATCH', s2=s0_report(2, 'D09', mutate=_d_set_digest('step3_sigma.py')))


@check('D10', '정상 기록 — 사다리 · 예측 요약 code = git 신원 (dirty False) + 코드 파일 지문 12 (사슬 폴더 = 실제 파일 sha256 · 러너 폴더 · '
              '러너 sha256) · S0 단계 1 기록 (보고 sha256 · 지문 일곱 · S0 계획 sha256) · 기계 이름표 null · 세 단계 지문 같음')
def t_D10():
    s, s1, p = s_main('P0')['sum'] or {}, s_main('P1')['sum'] or {}, s_main_predict()['sum'] or {}
    c = s.get('code') or {}
    files = c.get('files') or []
    want = [{'file': nm, 'sha256': (hashlib.sha256((SCRIPTS / nm).read_bytes()).hexdigest() if (SCRIPTS / nm).is_file() else None)}
            for nm in getattr(RR, 'CODE_FILES', ())]
    rec1 = (s.get('s0_reports') or {}).get('stage1') or {}
    names1 = {x.get('file') for x in rec1.get('file_digests') or []}
    ok = (len(files) == 12 and files == want and all(x['sha256'] for x in files)
          and c.get('runner_sha256') == hashlib.sha256(Path(FX['runner']).read_bytes()).hexdigest()
          and isinstance(c.get('runner_files'), list) and (c.get('chain') or {}).get('dirty') is False
          and rec1.get('sha256') == hashlib.sha256(Path(FX['s1']).read_bytes()).hexdigest() and rec1.get('plan_sha256') == FX['s0_sha']
          and set(S0_SAME7) <= names1 and 'machine' in s and s.get('machine') is None
          and (p.get('code') or {}).get('files') == files and (s1.get('code') or {}).get('files') == files
          and (p.get('s0_reports') or {}).get('stage1') == rec1)
    return ok, (len(files), c.get('runner_sha256'), rec1.get('plan_sha256'), s.get('machine', 'absent'))


@check('D11', '기계 이름표 — 사다리 P0 m1 · P1 m2 · 예측 m3 → 요약 machine 칸 · 판정 = 주 판정과 같은 이름 (이름표는 판정에 안 쓴다 · 코드 지문만) · '
              '틀린 이름표 (IP · 경로 · 점 · 빈칸 · 띄어쓰기) · 판정 단계의 --machine → 인자 오류 rc 2 · 러너 0 회')
def t_D11():
    def go():
        a = ladder('D11_P0', world('D11_P0'), law='P0', extra=['--machine', 'm1'])
        b = ladder('D11_P1', world('D11_P1'), law='P1', extra=['--machine', 'm2'])
        p = predict('D11_pred', world('D11_pred'), [a['out'], b['out']], extra=['--machine', 'm3'])
        v = verdict('D11', [a['out'], b['out'], p['out']])
        bad = []
        for i, lab in enumerate(('10.0.0.1', 'a/b', 'kgy.lab', '', 'kgy one')):
            w = world(f'D11_bad{i}')
            rr = ladder(f'D11_bad{i}', w, extra=['--machine', lab])
            bad.append((lab, rr['rc'], n_calls(w)))
        rv = verdict('D11v', [a['out'], b['out'], p['out']], extra=['--machine', 'm1'])
        return a, b, p, v, bad, rv
    a, b, p, v, bad, rv = scen('D11', go)
    v0 = s_verdict_main()
    return ([(a['sum'] or {}).get('machine'), (b['sum'] or {}).get('machine'), (p['sum'] or {}).get('machine')] == ['m1', 'm2', 'm3']
            and v['rc'] == 0 and (v['v'] or {}).get('verdict') == (v0['v'] or {}).get('verdict') == 'PASS_INFORMATIVE'
            and all(rc == 2 and n == 0 for _l, rc, n in bad) and rv['rc'] == 2,
            ([(x['sum'] or {}).get('machine') for x in (a, b, p)], v['rc'], (v['v'] or {}).get('verdict'), bad, rv['rc']))


@check('D12', '추적 파일 수정 여부 = 실제 git (임시 저장소 · 고정물 신원 아님): 깨끗 → dirty False · 추적 안 된 파일만 → False · 추적 파일 고침 '
              '→ True · code_files = CODE_FILES 이름마다 sha256 (없는 파일 = null)')
def t_D12():
    import subprocess
    g = FX['git_identity_real']
    d = Path(TD) / 'D12_repo'
    d.mkdir()

    def run(*a):
        return subprocess.run(['git', '-C', str(d), *a], capture_output=True, text=True)
    run('init', '-q')
    (d / 'rint_r_chain.py').write_text('x = 1\n', encoding='utf-8')
    run('add', 'rint_r_chain.py')
    run('-c', 'user.email=t@t', '-c', 'user.name=t', '-c', 'commit.gpgsign=false', 'commit', '-q', '-m', 'c')
    clean = g(d / 'rint_r_chain.py')
    (d / 'untracked.txt').write_text('u', encoding='utf-8')
    untracked = g(d / 'rint_r_chain.py')
    (d / 'rint_r_chain.py').write_text('x = 2\n', encoding='utf-8')
    dirty = g(d / 'rint_r_chain.py')
    cf = RR.code_files(d) if hasattr(RR, 'code_files') else None
    want = {'rint_r_chain.py': hashlib.sha256(b'x = 2\n').hexdigest()}
    ok_cf = (isinstance(cf, list) and [x.get('file') for x in cf] == list(getattr(RR, 'CODE_FILES', ()))
             and all(x.get('sha256') == want.get(x.get('file')) for x in cf))
    return (clean.get('dirty') is False and untracked.get('dirty') is False and dirty.get('dirty') is True
            and isinstance(clean.get('head'), str) and len(clean['head']) == 40 and ok_cf,
            (clean, untracked, dirty, 'ok' if ok_cf else cf))


@check('D13', '감도 단계 — --after-main 의 주 예측 요약 코드 파일 지문 ≠ 지금 (손댐) → MAIN_NOT_DONE · rc 3 · 러너 0 회')
def t_D13():
    def go():
        d = b_tamper_copy(s_main_predict()['out'], 'D13_main', 'predict_summary.json', lambda s: _d_set_files(s, 'run_contract.py'))
        return ladder('D13', world('D13'), law='P0', variant='FIBRE', after=d)
    r = scen('D13', go)
    return (r['rc'] == 3 and stop_code(r) == 'MAIN_NOT_DONE' and n_calls(r['world']) == 0, (r['rc'], stop_code(r), n_calls(r['world'])))


@check('D14', '같은 판 파일 목록 — 사슬 S0_SAME_FILES = 등록 R §2-1b 일곱 · CODE_FILES (12) ⊇ 일곱 + 사슬 · 러너 · 증서 · 계약 · SV 증거 · '
              'S0 보고 code.file_digests 가 일곱을 다 싣는다 (ca_s0_census._code_info · 옛 = 다섯)')
def t_D14():
    import ca_s0_census as S0m
    same = tuple(getattr(RR, 'S0_SAME_FILES', ()))
    code = tuple(getattr(RR, 'CODE_FILES', ()))
    names = {x['file'] for x in S0m._code_info()['file_digests']}
    need = set(S0_SAME7) | {'rint_r_chain.py', 'sdcp_gain_vox015_8arm.sh', 'step3_conv_cert.py', 'run_contract.py', 'ca_ext_svcf.py'}
    return (len(same) == 7 and set(same) == set(S0_SAME7) and need <= set(code) and len(set(code)) == len(code) == 12
            and set(S0_SAME7) <= names, (same, code, sorted(names)))


@check('D15', '사다리 — --s0-stage1-report 없음 → 인자 오류 (rc 2) · 러너 0 회 · 출력 폴더 없음 (단계 1 지문 대조 없이 σ 런 없음)')
def t_D15():
    w = world('D15')
    out = Path(TD) / 'runs' / 'D15'
    rc, _so = call(['--stage', 'ladder', '--law', 'P0', '--target', '1.63', '--runner', FX['runner'], '--root', FX['root'],
                    '--plan', FX['plan'], '--s0-plan', FX['s0'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out,
                    S0_STAGE2_OPT, s0_stage2_for(FX['plan'])], w)
    return rc == 2 and n_calls(w) == 0 and not out.exists() and chain_has(S0_STAGE1_OPT), (rc, n_calls(w), chain_has(S0_STAGE1_OPT))


@check('D16', '러너 폴더의 census · registry 파일 (step3_sigma.py) ≠ S0 보고 지문 (사슬 폴더는 같음) → CODE_PIN_MISMATCH · 러너 0 회 · 사유 = 러너 폴더 '
              '(러너가 돌리는 코드 = 러너 폴더 · 그 폴더에 있는 파일만 대조)')
def t_D16():
    def go():
        d = Path(TD) / 'D16_runner'
        d.mkdir()
        r2 = d / 'runner.sh'
        r2.write_text(Path(FX['runner']).read_text(encoding='utf-8'), encoding='utf-8')
        r2.chmod(0o755)
        (d / 'step3_sigma.py').write_text('# 다른 판 (시험 D16)\n', encoding='utf-8')
        old = FX['runner']
        FX['runner'] = r2
        try:
            return ladder('D16', world('D16'))
        finally:
            FX['runner'] = old
    r = scen('D16', go)
    why = str(((r['sum'] or {}).get('stop') or {}).get('cause'))
    return (r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and n_calls(r['world']) == 0 and '러너 폴더' in why,
            (r['rc'], stop_code(r), n_calls(r['world']), why[-160:]))


@check('D17', '판정 — 예측 요약의 러너 폴더 지문 (runner_files) · 러너 sha256 손댐 → 판정 CODE_PIN_MISMATCH · NOT_COMPUTED · rc 3 (키 = 사슬 폴더만이 아니다)')
def t_D17():
    def set_rf(s):
        rf = (s.get('code') or {}).get('runner_files')
        if isinstance(rf, list) and rf:
            rf[0]['sha256'] = '0' * 64
        else:
            s.setdefault('code', {})['runner_files'] = [{'file': 'x', 'sha256': '0' * 64}]

    def go():
        a = b_tamper_copy(s_main_predict()['out'], 'D17_rf', 'predict_summary.json', set_rf)
        b = b_tamper_copy(s_main_predict()['out'], 'D17_rs', 'predict_summary.json',
                          lambda s: s.setdefault('code', {}).update(runner_sha256='0' * 64))
        return tuple(verdict(f'D17{t}', [s_main('P0')['out'], s_main('P1')['out'], d]) for t, d in (('a', a), ('b', b)))
    rs = scen('D17', go)
    return (all(r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED' for r in rs),
            [(r['rc'], stop_code(r)) for r in rs])


@check('D18', '예측 — 사다리 요약 하나가 dirty True 를 기록 (고쳐진 트리에서 돈 사다리 · 지문은 같음) → CODE_PIN_MISMATCH · 러너 0 회 · 어느 순서로 넘겨도')
def t_D18():
    def go():
        x = b_tamper_copy(s_main('P1')['out'], 'D18_P1', 'ladder_summary.json',
                          lambda s: s.setdefault('code', {}).setdefault('chain', {}).update(dirty=True))
        return predict('D18a', world('D18a'), [s_main('P0')['out'], x]), predict('D18b', world('D18b'), [x, s_main('P0')['out']])
    rs = scen('D18', go)
    return (all(r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and n_calls(r['world']) == 0 for r in rs),
            [(r['rc'], stop_code(r), n_calls(r['world'])) for r in rs])


@check('D19', '예측 — 손댄 사다리를 앞에 (뒤 = 깨끗한 사다리 = 지금 코드와 같음) → 두 사다리 코드 다름 = CODE_PIN_MISMATCH · 러너 0 회 '
              '(마지막 사다리만 지금과 대조하면 놓치는 순서)')
def t_D19():
    def go():
        x = b_tamper_copy(s_main('P1')['out'], 'D19_P1', 'ladder_summary.json', lambda s: _d_set_files(s, 'carbon_junction.py'))
        return predict('D19', world('D19'), [x, s_main('P0')['out']])
    r = scen('D19', go)
    return (r['rc'] == 3 and stop_code(r) == 'CODE_PIN_MISMATCH' and n_calls(r['world']) == 0, (r['rc'], stop_code(r), n_calls(r['world'])))


@check('B10', '예측 — 두 사다리의 단계 2 기록이 경로만 다르다 (각각은 봉인 해시 대조 통과) → S0_REPORT_MISMATCH (두 사다리 기록 다름) · 러너 0 회 · '
              '어느 순서로 넘겨도')
def t_B10():
    def go():
        x = b_tamper_copy(s_main('P1')['out'], 'B10_P1', 'ladder_summary.json',
                          lambda s: s['s0_reports']['stage2'].update(path='/elsewhere/s0_stage2_kit_DBE_sdcp1um_vgcf100.json'))
        return predict('B10a', world('B10a'), [s_main('P0')['out'], x]), predict('B10b', world('B10b'), [x, s_main('P0')['out']])
    rs = scen('B10', go)
    return (all(r['rc'] == 3 and stop_code(r) == 'S0_REPORT_MISMATCH' and n_calls(r['world']) == 0 for r in rs),
            [(r['rc'], stop_code(r), n_calls(r['world'])) for r in rs])


@check('B11', '판정 — 예측 요약의 단계 2 기록이 경로만 다르다 (봉인 해시 대조 통과) → S0_REPORT_MISMATCH (단계끼리 기록 다름) · NOT_COMPUTED · rc 3')
def t_B11():
    def go():
        d = b_tamper_copy(s_main_predict()['out'], 'B11_pred', 'predict_summary.json',
                          lambda s: s['s0_reports']['stage2'].update(path='/elsewhere/s0_stage2_kit_DBE_sdcp1um_vgcf100.json'))
        return verdict('B11', [s_main('P0')['out'], s_main('P1')['out'], d])
    r = scen('B11', go)
    return (r['rc'] == 3 and stop_code(r) == 'S0_REPORT_MISMATCH' and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED', (r['rc'], stop_code(r)))


@check('B12', '판정 — 세 단계 요약의 단계 2 봉인 R 계획 sha256 을 같게 손댐 (단계끼리 기록은 같음) → S0_REPORT_MISMATCH (단계마다 같은 함수로 '
              '다시 대조 · 같음 대조만으로는 못 잡는 꼴) · NOT_COMPUTED · rc 3')
def t_B12():
    def go():
        lp = [b_tamper_copy(s_main(law)['out'], f'B12_{law}', 'ladder_summary.json', _b_set_r) for law in ('P0', 'P1')]
        pp = b_tamper_copy(s_main_predict()['out'], 'B12_pred', 'predict_summary.json', _b_set_r)
        return verdict('B12', lp + [pp])
    r = scen('B12', go)
    return (r['rc'] == 3 and stop_code(r) == 'S0_REPORT_MISMATCH' and (r['v'] or {}).get('verdict') == 'NOT_COMPUTED', (r['rc'], stop_code(r)))


@check('N07', '★ PF2 E (PRE2-impl-03) S0 계획 중복 칸 ("gap_tol" 둘 · 등록 S0 줄 = 그 바이트의 sha256) → S0_PLAN_INVALID · 사유 = 중복 칸 '
              '(정준 바이트 검사 앞 · 러너 0 회)')
def t_N07():
    raw = Path(FX['s0']).read_bytes().replace(b'{', b'{"gap_tol":2.0,', 1)
    p = Path(TD) / 's0_plan_dup.json'
    p.write_bytes(raw)
    sha = hashlib.sha256(raw).hexdigest()
    reg = FX['reg_with'](f'`{FX["plan_sha"]}`', 'reg_N07.md', s0cell=f'`{sha}`')
    r = scen('N07', lambda: ladder('N07', world('N07'), s0=p, reg=reg))
    why = str(((r['sum'] or {}).get('stop') or {}).get('cause'))
    return (r['rc'] == 3 and stop_code(r) == 'S0_PLAN_INVALID' and n_calls(r['world']) == 0 and '중복' in why,
            (r['rc'], stop_code(r), why[-160:]))


@check('L21', 'Q-E 배선 (가짜 러너) — SBE origin 팔 1 · 2 가 arm 0 과 조금 다르면 (×1.0004 · ×0.9997) 끝 후보에서 띠 안 → 끝을 바깥 실측 이웃으로 · '
               'end_origin 런 (ARM_LIST=1,2 · 끝 R) · 밀기 기록 · 세 origin 이 끝에서 모두 띠 밖 (모형 손계산)')
def t_L21():
    r = scen('L21', lambda: ladder('L21', world('L21', dict(PW, arm_factor=ARM_SMALL))))
    L = lad(r)
    W = wdata(r['world'])
    af = W['arm_factor']
    T = {'lo': T_S * 1.02, 'hi': T_S * 0.98}
    bad = []
    for side, k in (('lo', L.get('R_j_lo')), ('hi', L.get('R_j_hi'))):
        for i in (0, 1, 2):
            s = sig_main(W, SBE_KIT, k, 'P0') * af[i]
            if (side == 'lo' and s < T['lo']) or (side == 'hi' and s > T['hi']):
                bad.append((side, k, i, s))
    pushes = [((L.get('ends') or {}).get(s) or {}).get('origin_pushes') for s in ('lo', 'hi')]
    er = [x for x in r['sum'].get('runs', []) if x['role'] == 'end_origin']
    return (r['sum']['status'] == 'CALIBRATED' and not bad and sum(pushes) >= 1 and er and all(x.get('arm_list') == [1, 2] for x in er),
            (r['sum']['status'], bad, pushes, [x['rj'] for x in er], stop_code(r)))


@check('V17', 'SV 범위 all3 (계획) — 모서리 열둘 전부 CJUNC_SV_CF=1 · R_j,hi 모서리의 큰 비 (9.0) → SV_DEPENDENT (R_j0 범위면 못 본다 — U08)')
def t_V17():
    def go():
        p, _sha, reg = plan_set('svall3', sv_cf_scope='all3')
        l0 = ladder('V17_P0', world('V17_P0'), law='P0', plan=p, reg=reg)
        l1 = ladder('V17_P1', world('V17_P1'), law='P1', plan=p, reg=reg)
        m = {'kit_has': 'DBE', 'law': 'P1', 'c': '1', 'rj': lad(l1)['R_j_hi']}
        pr = predict('V17_pred', world('V17_pred', dict(PW, sv_cf=[{'match': m, 'status': 'computed', 'ratio': 9.0}])),
                     [l0['out'], l1['out']], reg=reg)
        v = verdict('V17_v', [l0['out'], l1['out'], pr['out']], reg=reg)
        return {'pred': pr, 'v': v}
    sc = scen('V17', go)
    on = [e for e in env_log(sc['pred']['world']) if e.get('CJUNC_SV_CF') == '1']
    v = sc['v']['v'] or {}
    return (len(on) == 12 and 'SV_DEPENDENT' in v.get('flags', []), (len(on), v.get('flags'), v.get('stop')))


# ── M 변이 (시험이 떨어져야 한다) ──
def mutant(name, patch, run_eval):
    old = {k: getattr(RR, k) for k in patch}
    try:
        for k, v in patch.items():
            setattr(RR, k, v)
        ok, why = run_eval()
    except Exception as e:                              # noqa: BLE001 — 변이가 예외로 죽어도 '시험이 떨어졌다' 다
        ok, why = False, f'{type(e).__name__}: {e}'
    finally:
        for k, v in old.items():
            setattr(RR, k, v)
    return (not ok), f'{name} → 대상 검사 {"통과 (변이를 못 잡음)" if ok else "실패 (잡음)"} · {why}'


def lin_interp(Ra, sa, Rb, sb, target):
    t = (target - sa) / (sb - sa)
    return Ra + t * (Rb - Ra)


@check('M01', '변이: 보간을 선형 R (ln 아님) 로 → L02 손계산이 떨어진다')
def t_M01():
    return mutant('M01', {'interp_lnln': lin_interp}, lambda: eval_L02(ladder('M01', world('M01'))))


@check('M02', '변이: ±2 % → ±3 % → L03 (허용폭 양끝) 손계산이 떨어진다')
def t_M02():
    return mutant('M02', {'CONFIRM_TOL': 0.03}, lambda: eval_L03(ladder('M02', world('M02'))))


@check('M03', '변이: origin 규칙 끔 → L19 (8 팔 · 표지) 이 떨어진다')
def t_M03():
    return mutant('M03', {'sbe_origin_ok': lambda vals: (True, 0.0)}, lambda: eval_L19(run_L19('M03')))


@check('M04', '변이: 2판 e_min 빠른 멈춤을 되살림 (국소 e < e_min → CALIB_UNIDENTIFIED) → L11 (3판 = 진단 · CALIBRATED) 이 떨어진다')
def t_M04():
    class LadderEStop(RR.Ladder):
        def _ends(self):
            if self.st['local_e_ge_emin'] is False:
                raise RR.Stop('CALIB_UNIDENTIFIED', 'mutant — 2판 e_min 멈춤')
            return super()._ends()
    return mutant('M04', {'Ladder': LadderEStop}, lambda: eval_L11(run_L11('M04')))


@check('M05', '변이: τ_mono 끔 (∞) → L14 가 CALIB_NONMONOTONE 을 못 낸다')
def t_M05():
    def ev():
        r = run_L14('M05')
        return r['sum']['status'] == 'CALIB_NONMONOTONE', r['sum']['status']
    return mutant('M05', {'TAU_MONO': math.inf}, ev)


@check('M06', '변이: 판정 입력 sha256 대조 끔 → S22 가 INPUT_SHA_MISMATCH 를 못 낸다')
def t_M06():
    return mutant('M06', {'sha_mismatch': lambda path, want: None}, lambda: eval_S22(run_S22('M06')))


@check('M07', '변이: 점 수 상한을 계획 칸 + 1 로 (사슬이 숫자를 고른다) → L16 (계획 12 · 런 정확히 12) 이 떨어진다')
def t_M07():
    def ev():
        r = run_L16('M07')
        return r['sum']['status'] == 'CALIB_LADDER_EXHAUSTED' and len(roles(r)) == 12, (r['sum']['status'], len(roles(r)))
    return mutant('M07', {'ladder_cap': lambda plan: int(plan['max_ladder_points']) + 1}, ev)


def _contract_without(which):
    """기본 계약 (main 이 짓는 RealContract) 에서 정본 검사 하나를 끈 변이 클래스."""
    base = RR.RealContract

    class C(base):
        if which == 'ca':
            def ca_ext_record(self, man):
                return True, None
        else:
            def arm_problem(self, path, receipt):
                return None
    return C


@check('M08', '변이: 정본 ca_ext_record_ok 끔 → S09 (원장 수 변조) 가 CA_EXT_RECORD 를 못 낸다 (정본 계약이 실제로 일한다)')
def t_M08():
    return mutant('M08', {'RealContract': _contract_without('ca')},
                  lambda: stop_case('M08', [{'do': 'tamper_caext', 'match': {'rj': 'inf'}}], 'CA_EXT_RECORD'))


@check('M09', '변이: 정본 check_arm 끔 → S24 (매니페스트만 σ_AM_S) 가 ARM_CONTRACT 를 못 낸다')
def t_M09():
    return mutant('M09', {'RealContract': _contract_without('arm')},
                  lambda: stop_case('M09', [{'do': 'bad_am_s_man', 'match': {'rj': '1000000.0'}}], 'ARM_CONTRACT'))


@check('M10', '변이: sid 무리에서 origin 을 뺌 (옛 키) → L18 (origin 팔 1 · 2 의 다른 지문) 이 떨어진다')
def t_M10():
    return mutant('M10', {'sid_group': lambda kit, variant, origin_idx: RR.variant_raster(kit, variant)},
                  lambda: eval_L18(ladder('M10', world('M10'))))


#  ── 3판 변이 — 끝 규칙 (사전 리뷰 PRE-design-05 의 M1–M4 · 끝 origin 밀기는 끈다 — 밀기 따로 = M21) ──
def _no_push(lad_, side, X, end):
    return end, 0, []


def _end_m1(lad_, side, X):                                  # M1 — 확인 실패한 후보를 그대로 끝으로
    end, ent = RR_ORIG['end_pick'](lad_, side, X)
    return ent['candidate'], ent


def _end_m2(lad_, side, X):                                  # M2 — 확인 실패면 안쪽 이웃 (끼는 이웃 중 띠 안 쪽)
    end, ent = RR_ORIG['end_pick'](lad_, side, X)
    if ent['confirm_ok']:
        return end, ent
    ka, kb = ent['bracket']
    return (kb if side == 'lo' else ka), ent


def _end_old(sides):                                         # M3 · M4 — 2판 보간식 (R_j,0 을 낀 이웃에서 · 그 점을 끝으로 · 확인 결과 무시)
    def f(lad_, side, X):
        if side not in sides:
            return RR_ORIG['end_pick'](lad_, side, X)
        ka, kb = lad_.st['bracket']
        (Ra, sa), (Rb, sb) = lad_.pts[ka], lad_.pts[kb]
        key = RR.rj_key(RR.interp_lnln(Ra, sa, Rb, sb, X))
        if key not in lad_.pts:                              # 끝 σ 를 봉인 칸에 싣기 위해 한 번 돌린다 (끝 선택은 2판 그대로 — 확인 결과를 보지 않는다)
            lad_._get('end_confirm', key)
        return key, {'bracket': [ka, kb], 'candidate': key, 'confirm_reused': None, 'confirm_ok': None, 'source': 'old_interp'}
    return f


RR_ORIG = {}


def end_mutant(name, fn):
    RR_ORIG['end_pick'] = RR.end_pick
    return mutant(name, {'end_pick': fn, 'end_origin_push': _no_push}, eval_U01)


@check('M11', '변이 M1 (끝 = 확인 실패한 후보 26,758) → U01 이 떨어진다 (W 0.4536 PASS 로 줄어든다)')
def t_M11():
    return end_mutant('M11', _end_m1)


@check('M12', '변이 M2 (끝 = 안쪽 이웃 31,622.8 · 비 189.4 · FAIL) → U01 이 떨어진다 (PRE-design-05 — "약 200 · PASS 면 실패" 시험은 통과시켰다)')
def t_M12():
    return end_mutant('M12', _end_m2)


@check('M13', '변이 M3 (hi 끝만 2판 보간 · 비 18.7 · WEAK) → U01 이 떨어진다 (판정 이름만 보면 놓친다 · 끝 값으로 잡는다)')
def t_M13():
    return end_mutant('M13', _end_old(('hi',)))


@check('M14', '변이 M4 (양끝 2판 보간 · 비 8.34 · PASS) → U01 이 떨어진다')
def t_M14():
    return end_mutant('M14', _end_old(('lo', 'hi')))


@check('M15', '변이: DBE origin 을 R_j,0 에서만 (2판) → U02 (RCA-02) 가 떨어진다')
def t_M15():
    return mutant('M15', {'ORIGIN_CHECK_ROLES': ('R_j0',)}, eval_U02)


@check('M16', '변이: 4.68 ∈ U 를 envelope (hull) 로 → U03 (RCA-08 GAP) 이 떨어진다')
def t_M16():
    def hull(I, x):
        return sorted(I) if min(a for a, _b in I.values()) <= x <= max(b for _a, b in I.values()) else []
    return mutant('M16', {'in_law_sets': hull}, eval_U03)


@check('M17', '변이: 판정 함수가 중앙 (R_j,0) 네 점만 (2판 감도 비교) → U04b (양끝만 넓은 변이의 SENSITIVE) 가 떨어진다')
def t_M17():
    orig = RR.judge_set

    def centre_only(statuses, vals):
        return orig(statuses, None if vals is None else {k: v for k, v in vals.items() if k[2] == 'R_j0'})
    return mutant('M17', {'judge_set': centre_only}, lambda: eval_U04('wide'))


@check('M18', '변이: 차단 표지를 와일드카드 (*_SENSITIVE · *_UNCHECKED 꼬리) 로 → U05 (닫힌 집합) 가 떨어진다')
def t_M18():
    def suffix(flags):
        return sorted(f for f in set(flags) if f.endswith('_SENSITIVE') or f.endswith('_UNCHECKED'))
    return mutant('M18', {'blocking_of': suffix}, eval_U05)


@check('M19', '변이: ln 차 대신 절대차 → U06 (단위 불변 · τ_mono) 이 떨어진다')
def t_M19():
    def absdiff(a, b):
        return float(b) - float(a)
    return mutant('M19', {'ln_diff': absdiff}, eval_U06)


@check('M20', '변이: SV 문턱 비교를 ≥ 로 (비 = 문턱 도 의존) → U08 이 떨어진다 (등록 문장 "넘으면")')
def t_M20():
    orig = RR.sv_assess

    def ge(recs, threshold, scope):
        f, d = orig(recs, threshold, scope)
        if threshold is not None and any(isinstance((a.get('sv_cf') or {}).get('ratio'), float)
                                         and (a['sv_cf']['ratio'] >= threshold) for a in recs.values()) and 'SV_DEPENDENT' not in f:
            f = sorted(f + ['SV_DEPENDENT'])
        return f, d
    return mutant('M20', {'sv_assess': ge}, eval_U08)


@check('M21', '변이: 끝 origin 밀기 끔 (Q-E 없음) → U10 (PRE-design-01 합집합 바깥 감쌈) 이 떨어진다')
def t_M21():
    return mutant('M21', {'end_origin_push': _no_push}, eval_U10)


@check('M22', '변이: 조기 반환 해 상태를 받지 않음 (2판 — 양수 σ 만) → Z01 (바닥 영값) 이 떨어진다')
def t_M22():
    def old_state(s3):
        st, why = RC_ORIG['next_gen_state'](s3)
        return (st, why) if st in ('positive', 'legacy') else (None, 'mutant — 2판: 양수 σ 만')
    import run_contract as RCm
    RC_ORIG['next_gen_state'] = RCm.next_gen_state
    old = RR.RC.next_gen_state
    try:
        RR.RC.next_gen_state = old_state
        r = ladder('M22', z_world('M22', [{'match': {'rj': 'inf'}, 'state': 'zero'}]))
        ok = r['rc'] == 0 and r['sum']['status'] == 'CALIBRATED' and lad(r).get('states', {}).get('inf') == 'zero'
    except Exception as e:                                  # noqa: BLE001
        ok = False
        r = {'sum': {'status': f'{type(e).__name__}: {e}'}}
    finally:
        RR.RC.next_gen_state = old
    return (not ok), f'M22 → Z01 꼴 {"통과 (변이를 못 잡음)" if ok else "실패 (잡음)"} · {(r.get("sum") or {}).get("status")}'


RC_ORIG = {}


@check('M27', '★ 4판 (Q1) 변이: 단락 → 등록 풀이 상태 NOT_COMPUTED 를 끔 (short 를 양의 해 자리로 · 3판 짝) → Z02 꼴 (천장 단락) 이 떨어진다 '
              '(NOT_COMPUTED · 사유 ELECTRODE_SHORT 가 아니다)')
def t_M27():
    def ev():
        r = ladder('M27', z_world('M27', [{'match': {'rj': '0'}, 'state': 'short'}]))
        return eval_short_stage(r, role='ceiling')
    rs = dict(getattr(RR, 'REG_STATES'))
    rs['short'] = ('POSITIVE_SOLVED', None)
    return mutant('M27', {'REG_STATES': rs}, ev)


@check('M28', '★ 4판 (Q1) 변이: 예측 단계의 NOT_COMPUTED 를 등록 결과로 받지 않음 (STOPPED · 3판 꼴) → Z04 꼴 (DBE 모서리 단락) 판정이 '
              'INPUT_STAGE_STOPPED 로 흐려진다 = 떨어진다')
def t_M28():
    def ev():
        m = {'kit_has': 'DBE', 'law': 'P1', 'c': '1', 'rj': lad(s_main('P1'))['R_j0']}
        p = predict('M28', world('M28', dict(PW, states=[{'match': m, 'state': 'short'}])), [s_main('P0')['out'], s_main('P1')['out']])
        v = verdict('M28_v', [s_main('P0')['out'], s_main('P1')['out'], p['out']])
        ok1, w1 = eval_short_stage(p, role='corner')
        ok2, w2 = eval_short_verdict(v, 'predict')
        return ok1 and ok2, (w1, w2)
    return mutant('M28', {'PREDICT_OUTCOMES': frozenset()}, ev)


#  ── ★ 4판 Q2 변이 (고친 곳마다 3판 꼴로 한 줄 되돌림 → 새 시험이 떨어져야 한다) ──
@check('M29', '★ 4판 Q2-1 변이: 이름 우선순위를 3판으로 (CALIB_ORDER 끝의 NOT_COMPUTED 가 진다 · min 순서) → U11 이 떨어진다')
def t_M29():
    def old_judge_set(statuses, vals):
        bad = [statuses[law] for law in RR.LAWS if statuses[law] != 'CALIBRATED']
        if bad:
            return {'verdict': min(bad, key=RR.CALIB_ORDER.index), 'state': 'calib'}
        return RR_ORIG['judge_set'](statuses, vals)
    RR_ORIG['judge_set'] = RR.judge_set
    return mutant('M29', {'judge_set': old_judge_set}, eval_U11)


@check('M30', '★ 4판 Q2-2 변이: 끝 판정의 보호 띠 끔 (e 무시 · 3판 outside_band) → U01e (e ≥ 3.728e-5 → 1e7 · 비 1,000) 가 떨어진다')
def t_M30():
    def no_band(s, X, lo, e=0.0):
        return s >= X if lo else s <= X
    return mutant('M30', {'outside_band': no_band}, eval_U01e)


@check('M31', '★ 4판 Q2-2 변이: EDGE 판정의 보호 띠 끔 (3판 |σ/T − 1| ≤ 2 % 만) → U12 (바닥 T⁻(1 − 5e-5) · e 1e-4 → CALIB_EDGE) 가 떨어진다')
def t_M31():
    def no_band_edge(s, e, T, tol=RR.CONFIRM_TOL):
        return abs(s / T - 1.0) <= tol
    return mutant('M31', {'edge_hit': no_band_edge}, eval_U12)


@check('M32', '★ 4판 Q2-3 변이: dbe_origin_ok 를 3판으로 (상태 무시 · W +∞ → 문턱 +∞) → U13 (상태 다름 = 넘음 · [3.0, 5.25]) 이 떨어진다')
def t_M32():
    def old_ok(vals, W0, states=None, w_pos=None):
        sp = RR.ln_spread(vals)
        thr = RR.ORIGIN_DBE_FRAC_W * W0 if W0 != math.inf else math.inf
        return sp <= thr, sp
    return mutant('M32', {'dbe_origin_ok': old_ok}, eval_U13)


@check('M33', '★ 4판 Q2-3 변이: W₊ 대신 W (+∞ 그대로) 를 문턱에 → U13b (W₊ 로 넘음 · 4.175) 가 떨어진다')
def t_M33():
    orig = RR.dbe_origin_ok

    def w_inf(vals, W0, states=None, w_pos=None):
        return orig(vals, W0, states=states, w_pos=(math.inf if W0 == math.inf else w_pos))
    return mutant('M33', {'dbe_origin_ok': w_inf}, eval_U13b)


@check('M34', '★ 4판 Q2-4 변이: 결정표 오른쪽 칸을 3판으로 (차단 표지가 있으면 PASS 문장 없음 · None) → U07 이 떨어진다')
def t_M34():
    orig = RR.decide_sentence

    def old_dec(state, verdict, blocking, sens_incomplete=False):
        s = orig(state, verdict, blocking, sens_incomplete=sens_incomplete)
        return None if (verdict == 'PASS_INFORMATIVE' and blocking) else s
    return mutant('M34', {'decide_sentence': old_dec}, eval_U07)


@check('M35', '★ 4판 Q2-5 변이: 변이 NOT_COMPUTED 를 이름 비교로 (3판 · <V>_SENSITIVE) → U14 가 떨어진다')
def t_M35():
    orig = RR.variant_flag

    def old_flag(V, vJ, J, vflags):
        if vJ['verdict'] == 'NOT_COMPUTED' and vJ['verdict'] != J['verdict']:
            return f'{V}_SENSITIVE', True, f'변이 판정 이름 {vJ["verdict"]}'
        return orig(V, vJ, J, vflags)
    return mutant('M35', {'variant_flag': old_flag}, eval_U14)


@check('M36', '★ 4판 Q2-5 변이: 변이 자신의 CALIB_ORIGIN_SENSITIVE 를 안 봄 → U14 (c) 가 떨어진다')
def t_M36():
    orig = RR.variant_flag

    def no_own(V, vJ, J, vflags):
        return orig(V, vJ, J, [f for f in vflags if f != 'CALIB_ORIGIN_SENSITIVE'])
    return mutant('M36', {'variant_flag': no_own}, eval_U14)


@check('M37', '★ 4판 Q2-6 변이: 한정어 ⑰ ⑱ 없음 (①–⑯) → X05 가 떨어진다')
def t_M37():
    return mutant('M37', {'QUALIFIERS': RR.QUALIFIERS[:16]}, t_X05)


#  ── ★ RI 변이 (§5-6 ③ 멈춘 변이 단계 · 고친 곳마다 한 줄 되돌림 → 새 시험이 떨어져야 한다) ──
@check('M38', '★ RI 변이: 멈춘 단계 거부를 4판 사슬 꼴로 (주 · 변이 가리지 않고 STOPPED = 판정 전체 거부) → V21 · V22 (멈춘 변이 = <V>_UNCHECKED) 가 '
              '떨어진다')
def t_M38():
    def old(s):
        return s.get('status') == 'STOPPED'
    a = mutant('M38a', {'stopped_stage_rejects_verdict': old}, lambda: eval_V21('M38a_v'))
    b = mutant('M38b', {'stopped_stage_rejects_verdict': old}, lambda: eval_V22('M38b_v'))
    return a[0] and b[0], (a[1], b[1])


@check('M39', '★ RI 변이: 주 판정 단계의 멈춤도 거부하지 않음 → V23 (주 사다리 · 주 예측 멈춤 = INPUT_STAGE_STOPPED) 이 떨어진다')
def t_M39():
    return mutant('M39', {'stopped_stage_rejects_verdict': lambda s: False}, lambda: eval_V23('M39a', 'M39b'))


@check('M40', '★ RI 변이: 멈춘 변이 단계를 NOT_COMPUTED 로 두지 않고 원 팔에서 다시 계산 → V21 · V22 가 떨어진다')
def t_M40():
    a = mutant('M40a', {'variant_stage_stopped': lambda s: False}, lambda: eval_V21('M40a_v'))
    b = mutant('M40b', {'variant_stage_stopped': lambda s: False}, lambda: eval_V22('M40b_v'))
    return a[0] and b[0], (a[1], b[1])


@check('M23', '변이: 두 계획 대조 끔 → C05 (tol_ff 다름) 가 PLAN_CROSS_MISMATCH 를 못 낸다')
def t_M23():
    return mutant('M23', {'plans_cross_problems': lambda plan, s0: []},
                  lambda: c_plan('M23', 'PLAN_CROSS_MISMATCH', tol_ff_um=0.04))


@check('M24', '변이: 결과 전 등록 숫자 검사 끔 → N01 (SV 문턱 null) 이 PLAN_NUMBER_UNREGISTERED 를 못 낸다 (Q-G)')
def t_M24():
    return mutant('M24', {'require_plan_numbers': lambda plan: None},
                  lambda: c_plan('M24', 'PLAN_NUMBER_UNREGISTERED', sv_cf_threshold=None))


@check('M25', '변이: 감도 단계의 주 판정 묶음 검사 끔 → F01 (--after-main 없음) 이 MAIN_NOT_DONE 을 못 낸다 (Q-F)')
def t_M25():
    return mutant('M25', {'check_after_main': lambda after_dir, plan_sha, s0_sha, code: None},
                  lambda: c_case('M25', 'MAIN_NOT_DONE', variant='FIBRE', after=''))


def _read_run_state_first():
    """`read_run` 원문에서 해 상태 블록 (`next_gen_state` · 수렴 계약) 을 기록 검사 (세대 · ca_ext) 앞으로 옮긴 사본 (10-21 PRE-impl-07 병합
    이전 순서) — 사슬 모듈 이름공간의 사본에서 컴파일 (Stop · RC · SVCF 는 같은 객체).  자리 글이 정확히 한 번씩 없으면 예외 = M26 실패."""
    import inspect
    src = inspect.getsource(RR.read_run)
    marks = ('        pid = RC.physics_protocol_id(man)\n', '        state, swhy = RC.next_gen_state(s3)\n',
             '        why = contract.arm_problem(p, rcpt)\n')
    if [src.count(m) for m in marks] != [1, 1, 1]:
        raise AssertionError(f'M26 변이 자리 {[src.count(m) for m in marks]} (정확히 한 번씩이어야 한다)')
    a, b, c = (src.index(m) for m in marks)
    if not a < b < c:
        raise AssertionError(f'M26 변이 자리 순서 {(a, b, c)} (기록 → 해 상태 → 팔 계약 이어야 한다)')
    src = src[:a] + src[b:c] + src[a:b] + src[c:]
    g = dict(vars(RR))
    exec(compile(src, str(RR.__file__) + ' [변이 M26]', 'exec'), g)   # noqa: S102 — 시험 전용 변이 (mutant 가 되돌린다)
    return g['read_run']


@check('M26', '변이: 해 상태 (증서 · 증서 ↔ 런 결합) 를 기록 검사 (세대 · ca_ext) 앞으로 (PRE-impl-07 병합 이전 순서) → S07 꼴 (unknown:ca_ext) 이 '
              'GENERATION 을 못 낸다 (옳은 이유 = NOT_COMPUTED · CERT|bind|)')
def t_M26():
    fn = _read_run_state_first()
    seen = {}

    def ev():
        ok, why = stop_case('M26', [{'do': 'unknown_caext', 'match': {'rj': '0'}}], 'GENERATION')
        seen['why'] = why
        return ok, why
    caught, msg = mutant('M26', {'read_run': fn}, ev)
    w = seen.get('why') or ()
    st = w[2] if len(w) > 2 and isinstance(w[2], dict) else {}
    right = len(w) > 1 and w[1] == 'NOT_COMPUTED' and 'CERT|bind|' in str(st.get('cause'))
    return caught and right and RR.read_run is not fn, (msg, w[:2], str(st.get('cause'))[:160])


# ═════════════════════════ 실행 ═════════════════════════
def main(argv=None):
    global RR, TD
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--only', default='', help='쉼표로 이름 접두 (예: L0,S1)')
    ap.add_argument('--keep', action='store_true', help='임시 폴더를 남긴다')
    a = ap.parse_args(argv)
    sel = [x for x in a.only.split(',') if x]
    todo = [c for c in CHECKS if not sel or any(c[0].startswith(s) for s in sel)]
    try:
        import rint_r_chain as _m
        RR = _m
    except ImportError as e:
        for cid, title, _fn in todo:
            print(f'  FAIL  {cid} {title}   (module absent: {e})')
        print(f'\ntest_rint_r_chain: 0/{len(todo)} PASS (module absent)')
        return 1
    TD = tempfile.mkdtemp(prefix='rint_r_chain_t_')
    t0 = time.time()
    ok, fail = 0, []
    try:
        fixtures()
        for cid, title, fn in todo:
            try:
                res, why = fn()
            except Exception as e:                      # noqa: BLE001 — 시험 안의 예외 = 그 검사 실패
                import traceback
                res, why = False, f'{type(e).__name__}: {e} @ {traceback.format_exc().splitlines()[-3].strip()[:200]}'
            if res:
                ok += 1
                print(f'  PASS  {cid} {title}')
            else:
                fail.append(cid)
                print(f'  FAIL  {cid} {title}   {str(why)[:600]}')
    finally:
        if a.keep:
            print(f'  (임시 폴더 남김: {TD})')
        else:
            shutil.rmtree(TD, ignore_errors=True)
    print(f'\ntest_rint_r_chain: {ok}/{len(todo)} PASS ({time.time() - t0:.1f} s)' + (f'   FAILED: {fail}' if fail else ''))
    return 0 if not fail else 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② 개발 탐침 ⑥ (SBE 수치 탐침 · σ 봉인) 준비물 시험 · 시험 먼저 (2026-11-10).

대상 (같은 폴더):
  probe6_read.py   σ 비열람 판독기 (닫힌 허용 칸만 낸다)
  run_probe6.sh    kgy 감시 셸 (러너 출력은 로그 파일로만 · 묶음에 σ 가 든 파일을 넣지 않는다)
  ../KGY_BLOCK.md  1저자가 붙여 넣는 블록 · ../LEDGER_LINE.md  원장 줄 초안

정본 = 개발 탐침 사전 원장 `docs/reviews/rint2_dev_probe_ledger_20261026.md` §2 (규칙 일곱 칸) · 등록 R
`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §10-1 (2) · §11 ⑥.

  python3 docs/reviews/rint2_probe6_prep_20261110/tools/test_probe6_read.py            # 전부
  python3 .../test_probe6_read.py --only T,M        # 이름 접두로 고르기
  python3 .../test_probe6_read.py --no-real         # 실제 러너 묶음 (R) 을 뺀다 (뺀 것은 PASS 로 세지 않는다)
  python3 .../test_probe6_read.py --keep            # 임시 폴더를 남긴다

묶음:
  S  정적: ASCII · Python 3.8 문법 · bash -n · 축 (감시 셸 ↔ 등록 R §10-1 (2) ↔ 원장 줄 초안 ↔ S0 계획 ↔ 코드 상수) · 허용 표에 σ 류 이름 없음 ·
     주소 · 모델 이름 없음 · 게이트 단계
  T  판독기: 합성 출력 폴더 (실제 러너 · payload 가 쓰는 꼴을 본뜸 · σ 류 자리마다 표식 0.00713331… 을 심음):
     허용 칸이 나온다 · 표식이 화면 · JSON · 걸러 낸 로그 어디에도 없다 · 칸 결손 · 미수렴 · 거부 표지 · 빈 폴더 · 두 팔 섞임 · 봉인 깨진 로그 ·
     실패 남은 파일 · 폴더 sha 가 내용에 반응
  M  변이: 판독기 사본을 한 군데씩 망가뜨리면 T 묶음이 잡는다 (잡지 못하면 실패)
  F  감시 셸: 가짜 러너 (git 고정물 저장소 = 핀) : 러너 env = 등록 축 그대로 · 부모 셸의 축 env 를 걷어냄 · umask 022 · 멈춤 조건 ·
     실패 보존 · 묶음에 표식 없음 · 상한 · 신호
  B  블록: KGY_BLOCK.md 의 블록을 그대로 꺼내 가짜 홈에서 끝까지 (fetch → 작업 트리 → nohup → DONE)
  R  실물: 실제 러너 · 실제 payload · 픽스처 킷 (CPU · `scripts/test_rint_r_chain_e2e.py` 의 침대) : 판독기가 실물 꼴을 읽는다 ·
     실물 σ 숫자가 판독기 출력 · 묶음에 없다 · 감시 셸의 실패 경로 (GPU 기대 · CPU 풀이 = 러너가 팔을 옮기지 않는다)
⚠ PASS 는 준비물의 배선 · σ 비열람 · 실패 처리의 증거다.  실침대 반복 수 · 시간 · 메모리는 kgy 런이 잰다 (여기에 킷도 GPU 도 없다).
"""
import argparse
import ast
import contextlib
import glob
import hashlib
import io
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(PREP, '..', '..', '..'))
SCRIPTS = os.path.join(ROOT, 'scripts')
READER = os.path.join(HERE, 'probe6_read.py')
WRAPPER = os.path.join(HERE, 'run_probe6.sh')
BLOCK_MD = os.path.join(PREP, 'KGY_BLOCK.md')
LEDGER_MD = os.path.join(PREP, 'LEDGER_LINE.md')
README_MD = os.path.join(PREP, 'README.md')
REG_DOC = os.path.join(ROOT, 'docs', 'reviews', 'rint_carbon_additive_registration_R_draft_20261020.md')
TOOLS_REL = 'docs/reviews/rint2_probe6_prep_20261110/tools'
RUNNER_REL = 'scripts/sdcp_gain_vox015_8arm.sh'
S0PLAN_REL = 'docs/data/rint2_s0_sbe_20261108/files/sdcp/ca1_s0_sbe_20261106_memfix/cjunc_plan.json'
PREREG_REL = 'docs/reviews/sdcp_gain_prereg_v2_20260816.md'
KIT = 'kit_SBE_vgcf100'
ARM = 'p2_SBE_vgcf100_sph_fa_cj1000000_78c44437_c0_rt1em12_fb10000_a0'
GIT_CFG = ('-c', 'user.email=t@t', '-c', 'user.name=t', '-c', 'commit.gpgsign=false', '-c', 'init.defaultBranch=main')

#: σ 류 자리에 심는 표식: 합성 폴더의 σ · 전류 · 구간 · 저항 · 소산 몫 값은 전부 0.00713331NNN 꼴이다 (%.6g · %.5g 로 찍혀도 71333 이 남는다)
SENT = '71333'
#: 등록 축 (등록 R §10-1 (2) · 1저자 결정값): 시험의 독립 표 (감시 셸 · 원장 줄 초안 · 가짜 러너가 받은 env 를 이것과 대조한다)
AXES = {
    'VOX': '0.15', 'SDCP_SPHERE_D': '0.30', 'PTFE_STAMP': 'face_alpha', 'BRIDGE_UM': '0.48', 'SIGMA_AM_S_OVERRIDE': '0.0041',
    'SIGMA_SDCP_OVERRIDE': '256.6', 'SIGMA_FIBRE_BULK': '1e4', 'CJUNC': '1', 'CJUNC_RJ': '1e6', 'CJUNC_LEN_LAW': 'len_scaled_v0',
    'CJUNC_UNREG_LAW': 'cut', 'CJUNC_S_MIN_UM': '0.0', 'CJUNC_TOL_FF_UM': '0.07381254285530132', 'CJUNC_PTFE_JLAW': 'P0',
    'SDCP_MOD_C': '0', 'STEP3_RTOL': '1e-12', 'EXPECT_BACKEND': 'gpu', 'KITS': KIT, 'ARMS': '1', 'LEAN': '2',
}
MAXITER = '400000'
PIN_FIX = 'e93efb6be' + '0' * 31                             # 합성 핀 (팔의 code_sha 가 그 앞자리)
S0_RUN = 'run_VGCF3_PTFE1_20261023_210442_2904445'

ARGS = None
TD = None
_ok, _fail, _skipped = 0, [], []
CASES = []
OPTIONAL = []                                              # --only 로 이름을 줄 때만 도는 묶음 (게이트 기본 실행에 없다)
WRAPPER_SRC = None                                         # 감시 셸 변이 묶음 (W) 이 핀 저장소에 넣을 사본 (None = 이 폴더의 감시 셸)


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print('  PASS  %s' % name)
    else:
        _fail.append(name)
        print('  FAIL  %s%s' % (name, ('  (%s)' % str(why)[:700]) if why != '' else ''))
    return bool(cond)


def case(tag, optional=False):
    def deco(fn):
        (OPTIONAL if optional else CASES).append((tag, fn))
        return fn
    return deco


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def read_text(p):
    with open(p, encoding='utf-8', errors='replace') as f:
        return f.read()


def write_text(p, s, mode=None):
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)
    if mode is not None:
        os.chmod(p, mode)


def leak_view(text):
    """표식 검사용 보기: 긴 hex 토큰 (sha256 · 커밋 · 지문 = σ 가 숨을 수 없는 꼴) 을 지우고 소수점 · 쉼표를 뺀다."""
    t = re.sub(r'\b[0-9a-f]{12,64}\b', ' ', text)
    return re.sub(r'[.,]', '', t)


def leaks(*texts):
    return [i for i, t in enumerate(texts) if SENT in leak_view(t or '')]


def json_strings(obj):
    """JSON 값 전부를 글로 (키 포함 · 수 = repr): \\u 이스케이프를 푼 뒤에도 표식이 없는지 본다."""
    out = []

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                out.append(str(k))
                walk(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                walk(v)
        else:
            out.append(repr(x))
    walk(obj)
    return '\n'.join(out)


# ═════════════════════════ 합성 출력 폴더 (실제 러너 · payload 가 쓰는 꼴 · 11-10 픽스처 킷 실물에서 본뜸) ═════════════════════════
def sent(i):
    return float('0.00713331%03d' % i)


def s0_plan():
    with open(os.path.join(ROOT, S0PLAN_REL), encoding='utf-8') as f:
        return json.load(f)


def arm_doc():
    """팔 JSON: `mpm_webapp_payload.py` 가 쓰는 꼴 (top → mpm_metrics → step3 → conv_cert · manifest).  σ 류 = 표식."""
    plan = s0_plan()
    inp = plan['source']['inputs_sha256']
    backend = {'fallback_reason': None, 'precond': 'jacobi', 'requested': 'gpu', 'rtol': 1e-12, 'used': 'gpu'}
    cert = {
        'I_bot': sent(1), 'I_top': sent(2), 'bind_version': 'cert-bind-v1', 'dsigma_rel': sent(3) * 1e-7, 'eps_I': 0.0001,
        'fp_cjunc_registry': '788f63feba47842eb099eb8e52c094b0', 'fp_cjunc_rows': '429c242f98e92cbdad134d873fc53a4f',
        'fp_face_plan': '3cef9a48736e742ced142ed2155279b6', 'fp_sid': 'f9d5be7d93f6c3955e49acc77b3e7987',
        'fp_sig': '2698531a89d520f333fec9a74c362169', 'imbalance': 5.8534485478943814e-08, 'info': 0, 'iters': 48211, 'ok': True,
        'pass_a': True, 'pass_b': True, 'pass_c': True, 'pass_d': True, 'resid': 3.3143830439317267e-13,
        'resolve_I_bot': sent(4), 'resolve_I_top': sent(5), 'resolve_info': 0, 'resolve_iters': 913, 'resolve_rtol': 1e-14,
        'resolve_rtol_floor': 1e-14, 'resolve_tol': 0.0001, 'rtol_max': 1e-12, 'rtol_used': 1e-12, 'scale': sent(6) * 100,
        'sigma': sent(7), 'sigma_resolve': sent(8), 'status': 'POSITIVE_SOLVED', 'target_U': sent(9), 'target_W': sent(10),
        'target_err_bound_rel': sent(11) * 1e-7, 'target_flow_bot': sent(12), 'target_flow_top': sent(13),
        'target_fp': 'fsum-bfs-defect-margin-v2', 'target_hi': sent(14), 'target_in_bracket': False,
        'target_kcl_defect_bound': sent(15) * 1e-13, 'target_kcl_raw': sent(16) * 1e-6, 'target_ledger_ok': True,
        'target_ledger_problem': None, 'target_lo': sent(17), 'target_n_dof': 20885118, 'target_n_edges': 61234567,
        'target_n_floating_nodes': 0, 'target_n_plate_bot': 51234, 'target_n_plate_top': 49876,
        'target_n_through_components': 2, 'target_tol': 0.0001, 'target_topology': 'through', 'target_tree_levels': 811,
        'target_version': 'target-cert-v1', 'target_why': None, 'target_width_rel': sent(18) * 1e-11, 'version': 'conv-cert-v2'}
    solve = {'I_bot_code': sent(19), 'P_sum_check_code': sent(20), 'P_total_code': sent(21),
             'dissipation_share': {'other_bulk': sent(22), 'plate': sent(23), 'vv_axial': sent(24), 'vv_junction': sent(25) * 100},
             'n_junction_edges': 117583, 'n_extra_dofs': 1, 'n_through_dof': 20885118, 'short': False, 'solved': True,
             'sv_face_abs_current_over_I': sent(26),
             'sv_local_dissipation': {'kind': 'diagnostic_local_dissipation', 'sv_share': sent(27), 'vv_junction_share': sent(28)}}
    manifest = {
        'backend': dict(backend), 'backend_last_solve': dict(backend), 'bridge_um': 0.48,
        'ca_ext': {'schema': 'ca-ext-v1',
                   'cjunc': {'evidence': {'counts': {'n_instances': 117583, 'n_edge': 117583}, 'solve': solve},
                             'protocol': {'R_j_ohm': 1000000.0, 'len_law': 'len_scaled_v0', 's_min_um': 0.0,
                                          'tol_ff_um': 0.07381254285530132, 'unreg_law': 'cut', 'ptfe_jlaw': 'P0'}}},
        'code_sha': 'e93efb6be',
        'component_plan': {'collector': False, 'electronic': True, 'ionic': False, 'pore': False, 'thermal': False},
        'components': {'electronic': {'backend': dict(backend), 'status': 'complete'},
                       'ionic': {'reason': '--no-ion', 'status': 'disabled'}},
        'input_digest': '7d694e2d81385cc5',
        'input_files': {k: inp[k][:16] for k in ('fibre', 'fibre_dia', 'metrics_json', 'phase', 'scaffold', 'se')},
        'origin_shift_um': [0.0, 0.0, 0.0], 'physics_protocol_id': 'p3ca-34c51e9ca93e3459', 'ptfe_stamp': 'face_alpha',
        'sigma_am_s_S_cm': 0.0041, 'sigma_sdcp_S_cm': 256.6, 'sigma_vgcf_S_cm': float('7133.31'),
        'sigma_vgcf_bulk_S_cm': 10000.0, 'status': 'partial', 'vox_um': 0.15}
    step3 = {
        'cam_preset': {'cam': 'nmc811'}, 'carbon_se_area_um2': 12345.6, 'cg_info': 0, 'cg_iters': 48211,
        'cg_resid': 3.3143830439317267e-13,
        'collector': {'R_bulk_ohm_cm2': sent(29), 'sigma_apparent_S_cm': {'ideal_R0': sent(30), 'SBE_bare_110': sent(31)},
                      'sigma_apparent_pristine_S_cm': {'ideal_R0': sent(32)}},
        'conv_cert': cert, 'dissipation_share': None, 'je_definition': 'am-final-sid-v2', 'k_plates': [0, 483],
        'manifest': manifest, 'n_dof': 20885118, 'n_floating_dropped': 0, 'sigma_e_eff_S_cm': sent(33),
        'sigma_table_S_cm': {'AM_S': 0.0041, 'AM_P': 0.005, 'VGCF': float('7133.31'), 'SDCP': 256.6},
        'trust': 'RELATIVE_v1', 'unconverged': False, 'vox_um': 0.15}
    return {'kind': 'mpm', 'case': KIT, 'particles': [{'id': 0, 'type': 'AM_S', 'x': sent(34), 'y': 1.0, 'z': 2.0, 'r': 0.3}],
            'mesh_triangles': [], 'electronic_field': None,
            'mpm_metrics': {'porosity_mpm_pct': sent(35) * 1000, 'thickness_mpm_um': 72.53, 'step3': step3},
            'mpm_source': {'se': 'se_dump.npy'}}


def receipt_doc():
    return {'arms': 1, 'bridge_um': 0.48,
            'ca_ext_request': {'cjunc': {'R_j_ohm': 1000000.0, 'len_law': 'len_scaled_v0', 'ptfe_jlaw': 'P0', 's_min_um': 0.0,
                                         'tol_ff_um': 0.07381254285530132, 'unreg_law': 'cut'}, 'sdcp_mod': {'c': 0.0}},
            'code_sha': 'e93efb6be', 'expect_backend': 'gpu', 'fibre_stamp': 'segment',
            'origins': [[0.0, 0.0, 0.0], [0.0, 0.0, 0.075]], 'periodic_xy': False, 'ptfe_stamp': 'face_alpha',
            'receipt_digest': '36a935282238', 'sdcp_sphere_d_um': 0.3, 'sdcp_stamp': 'sphere', 'sdcp_yield_to_vgcf': False,
            'sigma_am_s_S_cm': 0.0041, 'sigma_sdcp_S_cm': 256.6, 'sigma_vgcf_bulk_S_cm': 10000.0, 'step3_rtol': 1e-12, 'vox_um': 0.15}


def dset(doc, path, value):
    cur = doc
    keys = path.split('.')
    for k in keys[:-1]:
        cur = cur[k]
    cur[keys[-1]] = value


def ddel(doc, path):
    cur = doc
    keys = path.split('.')
    for k in keys[:-1]:
        cur = cur[k]
    del cur[keys[-1]]


S3 = 'mpm_metrics.step3.'

#: 러너 · payload 화면 (실물 11-10 픽스처 런에서 옮김 · 수만 실침대 크기로): {…} 자리는 runner_log() 가 채운다
LOG_HEAD = '''[p2] ⚠ ARMS=1 ≠ 사전등록 8 — **진단 런**이다.
     OUTDIR 에 _arm1 를 붙여 생산 산출물과 갈라 놓는다.  생산 봉인은 걸지 않는다.
[p2] ★ SDCP **부피-보존 구 스탬프** Ø0.30 µm (점 스탬프가 아니다)
[p2] ★ **다음 세대 S1** — PTFE 면 개구율 face_alpha (셀을 찍지 않는 면 연산자 · Ø0.248 rope = 규약 선택 ·  생산 규약 아님)
[p2] ★ LEAN=2 (σ_e 전용) — 이온·pore-τ·집전체기하 를 전부 끈다 (팔당 솔브 3회 → 1회)
[p2] 런 영수증 → /x/sdcp/ca1_probe6_arm1/run_receipt.json
  [p2] origin 이동 CLI 확인
[p2] 규율 검사 통과
[p2] 미정의 이름 없음 (런 경로 5 파일)
[p2] vox 0.15 · 브리지 0.48 µm 고정 · 섬유 segment · 1 팔 · out /x/sdcp/ca1_probe6_arm1
  [p2] vox 0.15: σ_VGCF 10000 → 7133.31
[p2] ── {arm}  shift=(0 0 0)  σ_VGCF=7133.31
loaded 67,922,681 SE pts from se_dump.npy
  econn: 100.0% AM connected to the collector (0 isolated; 3077 carbon clusters)
  입력 digest 7d694e2d81385cc5 (6 파일) — CDXIJ-10 ③
  STEP3: 섬유 **선분 스탬프** ON — 도체점 1,878,529 · 섬유 50,348개
  STEP3: voxelizing conductive+SE grid (풀해상도 — 이후 전자/이온 CG 솔브, 침묵 수 분 정상)…
  STEP3: AM 접촉 브리지 반경 **고정** 0.48 µm (기본은 1.2·vox = 0.180) — 격자 수렴 시험용
  STEP3: ★ SDCP **부피-보존 구 스탬프** Ø0.3 µm (d/vox = 2.00) — 점 스탬프는 참부피의 0.24배
  STEP3: CG maxiter {maxiter} (기본 30,000) — 조건수가 나쁜 팔을 수렴시키기 위한 것이지 규약 변경이 아니다
  STEP3: CG rtol 1.0e-12 + 수렴 증서 (ⓐ 정지 rtol 상한 · ⓑ 판 전류 불균형 · ⓒ 이어 풀기) — 실패 = 미수렴 (미게시)
  STEP3: ★ S1 face_alpha — 캡슐 경로 1,234 · 조각 1,300 · 선분 47,000 · 부피 비 0.98 (ok) · α 행 전자 18,000 · 이온 — (41s) — 지름 rope = 규약 선택 (DIA_UNCHECKED)
  STEP3: ★ S2 탄소 접합 — instance 117,583 (간선 117,070 · 축약 0 · 미실현 513 · 긴 접촉 30,270 · SDCP 근접 0) · R_j 1e+06 Ω (cut · P0) · S3 c = 0 (1312s) — R_j = 모형 내부 보정값 (재료값 아님)
    STEP3 solve: 20,885,118 dof, plate contacts 51,234/49,876 — CG running (GPU, 수 분 소요 가능)…
'''
LOG_TAIL_OK = '''  STEP3 σ_e_eff = {sig} S/cm  (vox 0.15µm, 20,885,118 dof, resid 3.3e-13, 9876s)
  STEP3 collector scenarios(cycled): bulk {seal2} → {seal2} S/cm  (R_bulk {seal2} Ωcm² {seal2})
  STEP3 collector PRISTINE(시간-일관, panel-e≈): {seal2} S/cm  (위 cycled 세트=aged-접촉 민감도)
  STEP3: --no-collector — 집전체 기하 솔브 2회 건너뜀 (wetted/bare)
  STEP3: --no-ion — 이온 솔브 건너뜀 (σ_e 전용).  σ_ion·τ_full·Track-B 는 이 payload 에 **없다**
  STEP3 carbon–SE 계면 12345.6 µm² (VGCF-촉매 SE분해 화학열화 STEP5 입력)
  STEP3: --no-pore — pore-τ·PNM 건너뜀 (σ_e 전용)
saved {arm}.json  (48.2 MB)  porosity 7.4% · SE/solid 26.0% · thickness 72.5µm · coverage(@0.13/0.26µm) AM_P plastic 52/74% · 30000 AM
[p2] ▸ {arm} 피크 호스트 RSS = 21.4 GB

[p2] ⚠ 킷이 SDCP 기본이 아니다 (kit_SBE_vgcf100) — 계약 봉인을 **돌리지 않는다.**
     이 러너는 팔만 낸다.  봉인·판정은 그 캠페인의 판정기 소관이다
'''
LOG_TAIL_FAIL = '''  ⚠ STEP3 CG not converged (info={maxiter_plain}, resid=2.3e-09) — σ UNRELIABLE
  ⚠ STEP3 수렴 증서 실패 [POSITIVE_SOLVED] (ⓐ False · ⓑ True 불균형 1.23e-05 · ⓒ False Δσ 7.13e-03 · ⓓ False width) — 미수렴 = 미게시
  STEP3 σ_e_eff = {sig} S/cm  (vox 0.15µm, 20,885,118 dof, resid 2.3e-09, 39876s)
  STEP3: --no-collector — 집전체 기하 솔브 2회 건너뜀 (wetted/bare)

✗ STEP3_REQUIRED_INCOMPLETE| electronic unconverged
  최종 파일명을 쓰지 않는다 — 진단본: {arm}.json.failed
[p2] {arm} FAILED
[p2] ABORT — 팔 {arm} 실패.  원인을 고치고 다시 돌릴 것
     수치 증거가 계약을 만족하지 않는다 — SIGMA_E| sigma_e_eff_S_cm=-0.00713331901 (유한한 양수여야 한다)
'''
SEAL = '[봉인 — --show-results 로 열림]'


def runner_log(ok=True, sealed=True, arm=ARM, maxiter=int(MAXITER), sealed_coll=None):
    """sealed = 결과 줄 (σ_e_eff) 의 봉인 · sealed_coll = 집전체 줄 둘의 봉인 (None = sealed 와 같게)."""
    sealed_coll = sealed if sealed_coll is None else sealed_coll
    sig = SEAL if sealed else '0.007133'
    seal2 = '[봉인]' if sealed_coll else '0.00713331 / 0.00713332'
    head = LOG_HEAD.format(arm=arm, maxiter='{:,}'.format(maxiter))
    tail = (LOG_TAIL_OK if ok else LOG_TAIL_FAIL).format(sig=sig, seal2=seal2, arm=arm, maxiter_plain=maxiter)
    return head + tail


def n_lines_until(text, needle):
    """needle 이 처음 나오는 줄의 번호 (1 부터)."""
    for i, ln in enumerate(text.split('\n'), 1):
        if needle in ln:
            return i
    raise AssertionError('no line with %r' % needle)


T0 = 1794000000                                            # 합성 시작 시각 (epoch)


def samples_text(log, t_raster=600, t_solve=2000, t_done=11876, t_end=11900, step=10):
    """감시 셸의 표본 파일: 줄마다 epoch · 경과 · 로그 줄 수 · RSS 합 · RSS 최대 · GPU 사용 · 우리 몫 · GPU 사용률."""
    n_r = n_lines_until(log, 'STEP3: voxelizing')
    n_s = n_lines_until(log, 'STEP3 solve:')
    n_all = len(log.split('\n')) - 1
    rows = ['#epoch\telapsed_s\tlog_lines\trss_sum_kb\trss_max_kb\tgpu_used_mib\tgpu_ours_mib\tgpu_util']
    for t in range(0, t_end + 1, step):
        if t < t_raster:
            nl, rss, gpu, ours = 12, 3000000, 1234, 0
        elif t < t_solve:
            nl, rss, gpu, ours = n_r + 3, 17000000, 1234, 0
        elif t < t_done:
            nl, rss, gpu, ours = n_s, 22444000 if t == t_solve + 500 else 21000000, 9321 if t == t_solve + 700 else 9000, 7777
        else:
            nl, rss, gpu, ours = n_all, 5000000, 1300, 0
        rows.append('%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d' % (T0 + t, t, nl, rss, rss - 9000, gpu, ours, 97 if ours else 3))
    return '\n'.join(rows) + '\n'


def meta_text(**over):
    m = [('probe6_meta_version', '1'), ('pin', PIN_FIX), ('maxiter', MAXITER), ('kit', KIT), ('kit_run', S0_RUN),
         ('kit_run_matches_s0', '1'), ('outdir', '~/sdcp/ca1_probe6_arm1'), ('logdir', '~/p6log'), ('start_epoch', str(T0)),
         ('start_kst', '2026-11-10T15:00:00+0900'), ('end_epoch', str(T0 + 11900)), ('end_kst', '2026-11-10T18:18:20+0900'),
         ('wall_s', '11900'), ('runner_rc', '0'), ('cap_gb', '46'), ('cap_term', '0'), ('aborted', '0'), ('sample_s', '10'),
         ('time_v', '1'), ('umask', '0022'), ('mode_bad', '0'), ('git_lines_before', '0'), ('git_lines_after', '0'),
         ('scrubbed', 'SIGMA_VGCF_OVERRIDE'), ('pythonpath_set', '0'), ('tool_sha256_wrapper', 'b' * 64),
         ('tool_sha256_reader', 'c' * 64), ('runner_sha256', 'd' * 64), ('runner_log_sha256', 'e' * 64),
         ('s0_plan_sha256', '4da9886367799c46b5426177fcba5d6e120f718b6cf7a0a9037032a36e0197bd'), ('kit_run_before', '0'),
         ('kit_run_new', '1')]
    d = dict(m)
    order = [k for k, _v in m]
    for k, v in over.items():
        if v is None:
            d.pop(k, None)
        else:
            if k not in d:
                order.append(k)
            d[k] = str(v)
    return ''.join('%s=%s\n' % (k, d[k]) for k in order if k in d)


ENV_TEXT = '''python=3.8.10
python_impl=CPython
numpy=1.24.4
scipy=1.10.1
cupy=12.3.0
cupy_cuda_runtime=12040
numpy_blas=openblas64_
blas_core=SkylakeX
gpu_name=NVIDIA GeForce RTX 3090
gpu_driver=535.183.01
gpu_mem_total_mib=24576
cuda_version=12.2
kernel=Linux 5.4.0-200-generic
cpu_model=11th Gen Intel(R) Core(TM) i9-11900K @ 3.50GHz
mem_total_kb=65000000
git=2.25.1
bash=5.0.17
'''
#: `/usr/bin/time -v` 기록의 꼴 (줄마다 TAB 으로 시작한다)
TIME_V = ''.join('\t%s\n' % ln for ln in (
    'Command being timed: "bash {arm}.1234.sh"',
    'User time (seconds): 9123.45',
    'System time (seconds): 345.67',
    'Percent of CPU this job got: 98%',
    'Elapsed (wall clock) time (h:mm:ss or m:ss): 3:09:16',
    'Maximum resident set size (kbytes): 22438912',
    'Exit status: 0',
))


def make_case(name, arm=None, receipt=None, log=None, meta=None, extra=None, arm_name=ARM, with_logdir=True,
              failed=None, arm_time=True):
    """합성 시도 하나 → (출력 폴더, 로그 폴더, 킷 런 폴더).  arm = dict | None (None = 팔 파일 없음)."""
    base = os.path.join(TD, name)
    out, lg, run = os.path.join(base, 'sdcp', 'ca1_probe6_arm1'), os.path.join(base, 'p6log'), os.path.join(base, 'kit', S0_RUN)
    for d in (out, run):
        os.makedirs(d)
    if arm is not None:
        with open(os.path.join(out, arm_name + '.json'), 'w', encoding='utf-8') as f:
            json.dump(arm, f)
    if receipt is not False:
        with open(os.path.join(out, 'run_receipt.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(receipt_doc() if receipt is None else receipt, ensure_ascii=False, sort_keys=True))
    for nm, body in (extra or {}).items():
        write_text(os.path.join(out, nm), body)
    if with_logdir:
        os.makedirs(lg)
        lt = runner_log() if log is None else log
        write_text(os.path.join(lg, 'runner.log'), lt)
        write_text(os.path.join(lg, 'samples.tsv'), samples_text(lt) if 'STEP3 solve:' in lt else
                   '#epoch\telapsed_s\tlog_lines\trss_sum_kb\trss_max_kb\tgpu_used_mib\tgpu_ours_mib\tgpu_util\n'
                   '%d\t0\t3\t1000\t900\t1234\t0\t3\n' % T0)
        write_text(os.path.join(lg, 'meta.txt'), meta_text() if meta is None else meta)
        write_text(os.path.join(lg, 'env.txt'), ENV_TEXT)
        write_text(os.path.join(lg, 'time_v.txt'), TIME_V.format(arm=arm_name))
    if arm_time:
        write_text(os.path.join(run, '.peak_rss_%s.txt' % arm_name), TIME_V.format(arm=arm_name))
    for nm, doc in (failed or {}).items():
        with open(os.path.join(run, nm), 'w', encoding='utf-8') as f:
            json.dump(doc, f)
    for d, _ds, fs in os.walk(base):                           # 합성 파일 시각 = 시작 뒤 (판독기가 '이 시도의 새 파일' 로 본다)
        for nm in fs:
            os.utime(os.path.join(d, nm), (T0 + 100, T0 + 100))
    return out, (lg if with_logdir else None), run


class Res(object):
    pass


def load_reader(path):
    """판독기를 모듈로 (프로세스 안 · 빠름): main(argv) → rc."""
    src = read_text(path)
    ns = {'__name__': 'probe6_read_under_test', '__file__': path}
    exec(compile(src, path, 'exec'), ns)                       # noqa: S102 · 시험 대상 코드
    return ns


def run_reader(mod, out, lg=None, run=None, s0=True, extra_args=()):
    argv = ['--outdir', out]
    report = None
    if lg is not None:
        argv += ['--logdir', lg]
        report = os.path.join(lg, 'probe6_report.json')
    else:
        report = os.path.join(os.path.dirname(out), 'report_only.json')
        argv += ['--report', report]
    if run is not None:
        argv += ['--kit-run', run]
    if s0:
        argv += ['--s0-plan', os.path.join(ROOT, S0PLAN_REL)]
    argv += list(extra_args)
    for p in (report, os.path.join(lg, 'runner_filtered.log') if lg else None):
        if p and os.path.exists(p):
            os.remove(p)
    r = Res()
    buf, ebuf = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(ebuf):
            r.rc = mod['main'](argv)
    except SystemExit as e:
        r.rc = e.code if isinstance(e.code, int) else 99
    except Exception as e:                                     # noqa: BLE001 · 판독기는 예외를 밖으로 내면 안 된다
        r.rc = 98
        ebuf.write('EXC %s: %s' % (type(e).__name__, e))
    r.out, r.err = buf.getvalue(), ebuf.getvalue()
    r.report_text = read_text(report) if os.path.exists(report) else ''
    try:
        r.rep = json.loads(r.report_text) if r.report_text else None
    except ValueError:
        r.rep = None
    fl = os.path.join(lg, 'runner_filtered.log') if lg else None
    r.filtered = read_text(fl) if fl and os.path.exists(fl) else ''
    return r


def fld(r, key):
    return ((r.rep or {}).get('fields') or {}).get(key)


def is_missing(v):
    return isinstance(v, dict) and 'missing' in v


def no_leak(r):
    texts = [r.out, r.err, r.report_text, r.filtered, json_strings(r.rep) if r.rep is not None else '']
    return leaks(*texts)


# ═════════════════════════ T: 판독기 (합성 폴더) ═════════════════════════
def suite_T(mod, rec):
    """판독기 검사: rec(name, cond, why).  주 실행 = chk · 변이 실행 = 모으개 (하나라도 실패하면 그 변이는 잡힌 것)."""
    # T01 정상
    out, lg, run = make_case('t01_%d' % len(os.listdir(TD)), arm=arm_doc())
    r = run_reader(mod, out, lg, run)
    want = {'n_dof': 20885118, 'cg_iters': 48211, 'cg_info': 0, 'cg_resid': 3.3143830439317267e-13, 'unconverged': False,
            'cert_status': 'POSITIVE_SOLVED', 'cert_ok': True, 'cert_pass_a': True, 'cert_pass_b': True, 'cert_pass_c': True,
            'cert_pass_d': True, 'cert_imbalance': 5.8534485478943814e-08, 'cert_iters': 48211, 'cert_resolve_iters': 913,
            'cert_resolve_info': 0, 'cert_rtol_used': 1e-12, 'backend_used': 'gpu', 'backend_precond': 'jacobi',
            'backend_rtol': 1e-12, 'electronic_status': 'complete', 'electronic_backend_used': 'gpu'}
    got = {k: fld(r, k) for k in want}
    rec('T01a 정상 폴더: rc 0 · PROBE_OK', r.rc == 0 and (r.rep or {}).get('verdict') == 'PROBE_OK', (r.rc, r.out[-400:], r.err[-300:]))
    rec('T01b 허용 칸 값 (반복 수 · 잔차 · 판 전류 불균형 · 수렴 여부 · 백엔드 · 미지수 수)', got == want,
        {k: (got[k], want[k]) for k in want if got[k] != want[k]})
    rec('T01c 화면에 허용 칸이 보인다 (cg_iters · resolve_iters · imbalance)',
        all(s in r.out for s in ('cg_iters', '48211', 'cert_resolve_iters', '913', 'cert_imbalance', '5.85345e-08')), r.out[:600])
    # T02 σ 표식 0 회 (화면 · JSON 글 · JSON 값 · 걸러 낸 로그)
    lk = no_leak(r)
    rec('T02a σ 표식이 판독기 출력 어디에도 없다 (화면 · 오류 · 보고 JSON · 걸러 낸 로그 · JSON 값)', lk == [] and r.rep is not None, lk)
    rec('T02b 입력 σ_VGCF 줄도 걸러 낸 로그에 없다 · 걸러 낸 로그에 러너 원문 σ 줄 없음',
        'VGCF' not in r.filtered and 'σ' not in r.filtered and r.filtered != '', r.filtered[:300])
    rec('T02c 붙잡아 둔 칸 = 이름만 (dsigma_rel · target_err_bound_rel · target_width_rel)',
        set((r.rep or {}).get('held_back') or []) >= {'conv_cert.dsigma_rel', 'conv_cert.target_err_bound_rel',
                                                      'conv_cert.target_width_rel'}, (r.rep or {}).get('held_back'))
    # T03 로그 · 시간 · 자원
    lg_ = (r.rep or {}).get('log') or {}
    tm = (r.rep or {}).get('timing') or {}
    rs = (r.rep or {}).get('resources') or {}
    rec('T03a 로그 진단: dof · 잔차 · STEP3 초 · maxiter · rtol · 준비 초 · 봉인 표지',
        (lg_.get('solve_n_dof'), lg_.get('done_resid'), lg_.get('done_step3_s'), lg_.get('cg_maxiter'), lg_.get('cg_rtol'),
         lg_.get('face_alpha_prep_s'), lg_.get('cjunc_prep_s'), lg_.get('sealed'), lg_.get('solve_backend'))
        == (20885118, 3.3e-13, 9876, 400000, 1e-12, 41, 1312, True, 'GPU'), lg_)
    rec('T03b 시간: 전체 초 · 러너 rc · CG + 증서 구간 (표본 줄 수로) · 반복당 초 (위 한계)',
        tm.get('wall_s') == 11900 and tm.get('cg_cert_s') == 9880 and tm.get('raster_prep_s') == 1400
        and abs((tm.get('cg_cert_s_per_iter') or 0) - 9880.0 / (48211 + 913)) < 1e-12, tm)
    rec('T03c 자원: 표본 최대 RSS · GPU 최대 · 러너 화면의 팔 RSS · time -v',
        rs.get('rss_sum_max_kb') == 22444000 and rs.get('gpu_used_max_mib') == 9321 and rs.get('gpu_ours_max_mib') == 7777
        and rs.get('runner_peak_rss_gb') == 21.4 and rs.get('time_v_max_rss_kb') == 22438912
        and rs.get('arm_time_v_max_rss_kb') == 22438912 and rs.get('arm_time_v_elapsed_s') == 11356, rs)
    # T04 폴더 요약 sha (독립 계산)
    fo = (r.rep or {}).get('folder') or {}
    rows = sorted((nm, os.path.getsize(os.path.join(out, nm)), sha256_file(os.path.join(out, nm))) for nm in os.listdir(out))
    ind_list = hashlib.sha256(''.join('%s  %d  %s\n' % (h, sz, nm) for nm, sz, h in rows).encode()).hexdigest()
    ind_sum = hashlib.sha256(''.join('%s  %s\n' % (h, nm) for nm, _sz, h in rows).encode()).hexdigest()
    rec('T04a 폴더 요약 sha256 (이름 · 크기 · sha256 목록의 sha256) = 독립 계산', fo.get('listing_sha256') == ind_list, fo)
    rec('T04b 폴더 요약 (sha256sum 꼴 = 사슬 folder_digest 와 같은 식) = 독립 계산 · 파일 수 2',
        fo.get('sha256sum_style') == ind_sum and fo.get('n_files') == 2, fo)
    sh = subprocess.run('cd %s && find . -type f -printf "%%P\\n" | LC_ALL=C sort | xargs sha256sum | sha256sum' % out,
                        shell=True, capture_output=True, text=True)
    rec('T04c sha256sum 꼴 = 셸 한 줄 (find | sort | xargs sha256sum | sha256sum)', sh.stdout.split()[:1] == [fo.get('sha256sum_style')],
        sh.stdout + sh.stderr)
    # T05 폴더 sha 가 내용 변화에 반응
    a2 = arm_doc()
    dset(a2, S3 + 'cg_iters', 48212)
    dset(a2, S3 + 'conv_cert.iters', 48212)
    out2, lg2, run2 = make_case('t05_%d' % len(os.listdir(TD)), arm=a2)
    r2 = run_reader(mod, out2, lg2, run2)
    fo2 = (r2.rep or {}).get('folder') or {}
    rec('T05a 팔 파일 한 글자가 바뀌면 두 요약 sha 가 다 바뀐다',
        r2.rc == 0 and fo2.get('listing_sha256') not in (None, fo.get('listing_sha256'))
        and fo2.get('sha256sum_style') not in (None, fo.get('sha256sum_style')), (fo, fo2))
    os.rename(os.path.join(out2, 'run_receipt.json'), os.path.join(out2, 'run_receipt_x.json'))
    r3 = run_reader(mod, out2, lg2, run2)
    fo3 = (r3.rep or {}).get('folder') or {}
    rec('T05b 파일 이름만 바뀌어도 요약 sha 가 바뀐다 · 영수증 없음 = rc 4',
        fo3.get('listing_sha256') not in (None, fo2.get('listing_sha256')) and r3.rc == 4, (r3.rc, fo3))
    o5, l5, k5 = make_case('t05c_%d' % len(os.listdir(TD)), arm=arm_doc(), extra={'notes.dat': 'x'})
    rr = run_reader(mod, o5, l5, k5)
    rec('T05c 출력 폴더에 모르는 파일: rc 4 (꼴이 다르다 · 읽지 않는다)', rr.rc == 4 and fld(rr, 'cg_iters') == 48211, rr.rc)
    # T06 칸 결손 · 꼴
    for tag, path, val in (('cg_iters 없음', S3 + 'cg_iters', None), ('conv_cert 없음', S3 + 'conv_cert', None),
                           ('cg_iters 글자', S3 + 'cg_iters', '48211'), ('cg_iters bool', S3 + 'cg_iters', True),
                           ('imbalance 글자', S3 + 'conv_cert.imbalance', '5.85e-08'), ('n_dof 음수', S3 + 'n_dof', -5),
                           ('resolve_iters 없음', S3 + 'conv_cert.resolve_iters', None),
                           ('backend 없음', S3 + 'manifest.components', {})):
        a = arm_doc()
        if val is None:
            ddel(a, path)
        else:
            dset(a, path, val)
        o, l_, k = make_case('t06_%d' % len(os.listdir(TD)), arm=a)
        rr = run_reader(mod, o, l_, k)
        rec('T06 칸 결손 · 꼴 (%s): rc 4 · 그 칸 = 없음 + 사유 · 표식 없음' % tag,
            rr.rc == 4 and (rr.rep or {}).get('verdict') == 'PROBE_INCOMPLETE' and no_leak(rr) == []
            and any(is_missing(v) for v in ((rr.rep or {}).get('fields') or {}).values()), (rr.rc, rr.out[-300:]))
    a = arm_doc()
    o, l_, k = make_case('t06n_%d' % len(os.listdir(TD)), arm=a)
    p = glob.glob(os.path.join(o, 'p2_*.json'))[0]
    write_text(p, read_text(p).replace('"cg_resid": 3.3143830439317267e-13', '"cg_resid": NaN'))
    rr = run_reader(mod, o, l_, k)
    rec('T06n 비유한 토큰 (NaN) = 없음 (비유한) · rc 4', rr.rc == 4 and is_missing(fld(rr, 'cg_resid')), (rr.rc, fld(rr, 'cg_resid')))
    write_text(p, read_text(p)[:200])
    rr = run_reader(mod, o, l_, k)
    rec('T06t 잘린 JSON = rc 4 (추정하지 않는다)', rr.rc == 4 and (rr.rep or {}).get('source') in ('none', 'outdir'), (rr.rc, rr.out[-200:]))
    # T07 미수렴
    for tag, edits in (('unconverged True', [(S3 + 'unconverged', True)]),
                       ('cg_info = maxiter', [(S3 + 'cg_info', 400000), (S3 + 'conv_cert.info', 400000),
                                              (S3 + 'cg_iters', 400000), (S3 + 'conv_cert.iters', 400000)]),
                       ('증서 ok False (ⓒ)', [(S3 + 'conv_cert.ok', False), (S3 + 'conv_cert.pass_c', False)]),
                       ('상태 NOT_CERTIFIABLE', [(S3 + 'conv_cert.status', 'NOT_CERTIFIABLE'), (S3 + 'conv_cert.ok', False)])):
        a = arm_doc()
        for path, val in edits:
            dset(a, path, val)
        o, l_, k = make_case('t07_%d' % len(os.listdir(TD)), arm=a)
        rr = run_reader(mod, o, l_, k)
        rec('T07 미수렴 (%s): rc 3 · PROBE_NOT_CONVERGED · 반복 수는 그대로 보고 · 표식 없음' % tag,
            rr.rc == 3 and (rr.rep or {}).get('verdict') == 'PROBE_NOT_CONVERGED' and isinstance(fld(rr, 'cg_iters'), int)
            and no_leak(rr) == [], (rr.rc, rr.out[-300:]))
    # T08 거부 표지
    o, l_, k = make_case('t08_%d' % len(os.listdir(TD)), arm=arm_doc(), extra={'.rejected_20261110T010203Z': 'reason=seal_broken\n'})
    rr = run_reader(mod, o, l_, k)
    rec('T08a 거부 표지 (.rejected_*): rc 5 · PROBE_REJECTED · 팔 칸을 읽지 않는다',
        rr.rc == 5 and (rr.rep or {}).get('verdict') == 'PROBE_REJECTED' and not isinstance(fld(rr, 'cg_iters'), int)
        and no_leak(rr) == [], (rr.rc, fld(rr, 'cg_iters')))
    o, l_, k = make_case('t08b_%d' % len(os.listdir(TD)), arm=arm_doc(), arm_name=ARM.replace('SBE_vgcf100', 'DBE_sdcp1um_vgcf100'))
    rr = run_reader(mod, o, l_, k)
    rec('T08b DBE 팔 이름: rc 5 · 읽지 않는다 (허용 입력 = SBE 만)',
        rr.rc == 5 and not isinstance(fld(rr, 'cg_iters'), int), (rr.rc, fld(rr, 'cg_iters')))
    # T09 빈 폴더 · 없는 폴더
    o, l_, k = make_case('t09_%d' % len(os.listdir(TD)), arm=None, receipt=False)
    rr = run_reader(mod, o, l_, k)
    rec('T09a 빈 폴더: rc 4 · 추정 없음 (칸 전부 없음)', rr.rc == 4 and not isinstance(fld(rr, 'cg_iters'), int)
        and (rr.rep or {}).get('source') == 'none', (rr.rc, rr.out[-200:]))
    rr = run_reader(mod, o + '_nope', l_, k)
    rec('T09b 없는 폴더: rc 4', rr.rc == 4, rr.rc)
    # T10 두 팔 섞임
    o, l_, k = make_case('t10_%d' % len(os.listdir(TD)), arm=arm_doc())
    shutil.copy(os.path.join(o, ARM + '.json'), os.path.join(o, ARM[:-1] + '1.json'))
    rr = run_reader(mod, o, l_, k)
    rec('T10a 팔 파일 둘 (a0 + a1): rc 4 · 어느 팔도 읽지 않는다 · 사유 = 팔이 둘',
        rr.rc == 4 and not isinstance(fld(rr, 'cg_iters'), int) and no_leak(rr) == []
        and any('more than one arm file' in x for x in (rr.rep or {}).get('problems') or []), (rr.rc, fld(rr, 'cg_iters')))
    o, l_, k = make_case('t10b_%d' % len(os.listdir(TD)), arm=arm_doc(), arm_name=ARM[:-1] + '1')
    rr = run_reader(mod, o, l_, k)
    rec('T10b 팔 번호가 0 이 아님 (a1 만): rc 4', rr.rc == 4 and not isinstance(fld(rr, 'cg_iters'), int), rr.rc)
    rc2 = receipt_doc()
    rc2['arms'] = 2
    o, l_, k = make_case('t10c_%d' % len(os.listdir(TD)), arm=arm_doc(), receipt=rc2)
    rr = run_reader(mod, o, l_, k)
    rec('T10c 영수증 팔 수 2: rc 4', rr.rc == 4, rr.rc)
    a = arm_doc()
    dset(a, S3 + 'manifest.origin_shift_um', [0.0, 0.0, 0.075])
    o, l_, k = make_case('t10d_%d' % len(os.listdir(TD)), arm=a)
    rr = run_reader(mod, o, l_, k)
    rec('T10d 팔의 origin 이동이 0 이 아님: rc 4', rr.rc == 4, rr.rc)
    # T11 봉인이 깨진 로그 (--show-results 꼴)
    for tag, kw in (('결과 줄만', dict(sealed=False, sealed_coll=True)), ('집전체 줄만', dict(sealed=True, sealed_coll=False))):
        o, l_, k = make_case('t11_%d' % len(os.listdir(TD)), arm=arm_doc(), log=runner_log(**kw))
        rr = run_reader(mod, o, l_, k)
        rec('T11 로그에 봉인 안 된 σ 줄 (%s): rc 5 · 그 값은 어디에도 옮기지 않는다' % tag,
            rr.rc == 5 and (rr.rep or {}).get('verdict') == 'PROBE_REJECTED' and no_leak(rr) == []
            and '007133' not in leak_view(rr.out + rr.report_text + rr.filtered), (rr.rc, no_leak(rr)))
    # T12 실패 남은 파일 (payload 가 .failed 로 남긴 진단본 · 러너 rc 1)
    af = arm_doc()
    for path, val in ((S3 + 'unconverged', True), (S3 + 'cg_info', 400000), (S3 + 'cg_iters', 400000), (S3 + 'conv_cert.iters', 400000),
                      (S3 + 'conv_cert.info', 400000), (S3 + 'conv_cert.ok', False), (S3 + 'conv_cert.pass_a', False),
                      (S3 + 'conv_cert.resolve_iters', 400000), (S3 + 'conv_cert.resolve_info', 400000),
                      (S3 + 'manifest.components', {'electronic': {'status': 'unconverged'}})):
        dset(af, path, val)
    o, l_, k = make_case('t12_%d' % len(os.listdir(TD)), arm=None, log=runner_log(ok=False), meta=meta_text(runner_rc=1),
                         failed={ARM + '.json.failed': af})
    rr = run_reader(mod, o, l_, k)
    rec('T12a 실패 남은 파일: rc 3 · 출처 = 킷 런 폴더 (.failed) · 반복 수 = maxiter · 표식 없음',
        rr.rc == 3 and (rr.rep or {}).get('source') == 'kit_run_failed' and fld(rr, 'cg_iters') == 400000
        and fld(rr, 'cert_resolve_iters') == 400000 and no_leak(rr) == [], (rr.rc, (rr.rep or {}).get('source'), no_leak(rr)))
    lg12 = (rr.rep or {}).get('log') or {}
    rec('T12b 미수렴 줄 · 증서 실패 줄 = 다시 적은 꼴 (info · 잔차 · ⓐⓑⓒⓓ · 불균형) · Δσ 값은 옮기지 않는다',
        lg12.get('not_converged_info') == 400000 and lg12.get('not_converged_resid') == 2.3e-09
        and lg12.get('cert_fail_pass') == [False, True, False, False] and lg12.get('cert_fail_imbalance') == 1.23e-05
        and '713' not in leak_view(json.dumps(lg12, ensure_ascii=False)), lg12)
    masked = lg12.get('masked_lines') or []
    rec('T12c 실패 줄 = 수 하나를 # 하나로 가린 꼴로만 (SIGMA_E 줄의 값 · 자릿수 없음)',
        any('sigma_e_eff_S_cm=-# (' in m for m in masked) and all(not re.search(r'[0-9]', m) for m in masked), masked[-3:])
    knew = (rr.rep or {}).get('kit_run_new_files') or []
    rec('T12d 킷 런 폴더의 새 파일 = 이름 · 크기 · sha256 (지우지 않는다 · 값은 안 연다)',
        sorted(x.get('name') for x in knew) == sorted(['.peak_rss_%s.txt' % ARM, ARM + '.json.failed'])
        and os.path.exists(os.path.join(k, ARM + '.json.failed')), knew)
    # T13 러너 rc ≠ 0 인데 팔이 수렴 꼴 (옮겨지지 않은 팔) → rc 4
    o, l_, k = make_case('t13_%d' % len(os.listdir(TD)), arm=None, meta=meta_text(runner_rc=1), failed={ARM + '.json': arm_doc()})
    rr = run_reader(mod, o, l_, k)
    rec('T13 러너가 옮기지 않은 팔 (킷 런 폴더): rc 4 (받아들여진 팔이 아니다) · 칸은 보고',
        rr.rc == 4 and (rr.rep or {}).get('source') == 'kit_run_unmoved' and fld(rr, 'cg_iters') == 48211, (rr.rc, (rr.rep or {}).get('source')))
    o, l_, k = make_case('t13c_%d' % len(os.listdir(TD)), arm=None, failed={ARM + '.json': arm_doc()})
    rr = run_reader(mod, o, l_, k)
    rec('T13c 옮기지 않은 팔 · 러너 rc 0 이라고 적혀 있어도: rc 4 (출력 폴더의 팔만 받아들인 팔)',
        rr.rc == 4 and (rr.rep or {}).get('source') == 'kit_run_unmoved', (rr.rc, (rr.rep or {}).get('source')))
    o, l_, k = make_case('t13d_%d' % len(os.listdir(TD)), arm=None, meta=meta_text(runner_rc=1), failed={ARM + '.json.failed': arm_doc()})
    os.utime(os.path.join(k, ARM + '.json.failed'), (T0 - 1000, T0 - 1000))
    rr = run_reader(mod, o, l_, k)
    rec('T13d 시작 전부터 있던 남은 파일 (옛 시도의 것) 은 읽지 않는다: 출처 none · rc 4',
        rr.rc == 4 and (rr.rep or {}).get('source') == 'none' and not isinstance(fld(rr, 'cg_iters'), int), (rr.rc, (rr.rep or {}).get('source')))
    a = arm_doc()
    dset(a, S3 + 'conv_cert.iters', 48000)
    o, l_, k = make_case('t13e_%d' % len(os.listdir(TD)), arm=a)
    rr = run_reader(mod, o, l_, k)
    rec('T13e 팔의 cg_iters ≠ 증서의 반복 수: rc 4', rr.rc == 4 and fld(rr, 'cg_iters') == 48211 and fld(rr, 'cert_iters') == 48000, rr.rc)
    a = arm_doc()
    dset(a, S3 + 'manifest.components.electronic.backend.used', 'cpu')
    o, l_, k = make_case('t13f_%d' % len(os.listdir(TD)), arm=a)
    rr = run_reader(mod, o, l_, k)
    rec('T13f 풀이 백엔드 (cpu) ≠ 영수증 기대 (gpu): rc 4', rr.rc == 4 and fld(rr, 'electronic_backend_used') == 'cpu', rr.rc)
    o, l_, k = make_case('t13b_%d' % len(os.listdir(TD)), arm=arm_doc(), meta=meta_text(runner_rc=1))
    rr = run_reader(mod, o, l_, k)
    rec('T13b 팔은 정상인데 러너 rc 1: rc 4 (PROBE_OK 아님)', rr.rc == 4, rr.rc)
    # T14 로그 폴더 없이 (출력 폴더만) · 로그 폴더는 있는데 파일이 빠짐
    o, _l, k = make_case('t14_%d' % len(os.listdir(TD)), arm=arm_doc(), with_logdir=False)
    rr = run_reader(mod, o, None, None)
    rec('T14a 출력 폴더만: rc 0 · 범위 = outdir_only · 시간 · 자원 = 요청 안 함',
        rr.rc == 0 and (rr.rep or {}).get('scope') == 'outdir_only' and fld(rr, 'cg_iters') == 48211, (rr.rc, (rr.rep or {}).get('scope')))
    for nm in ('meta.txt', 'runner.log', 'samples.tsv'):
        o, l_, k = make_case('t14_%d' % len(os.listdir(TD)), arm=arm_doc())
        os.remove(os.path.join(l_, nm))
        rr = run_reader(mod, o, l_, k)
        rec('T14b 로그 폴더에 %s 없음: rc 4 (없음 + 사유 · 반복 수는 그대로)' % nm, rr.rc == 4 and fld(rr, 'cg_iters') == 48211, rr.rc)
    # T15 닫힌 집합: 모르는 메타 키 · 글자 값에 숨긴 수
    o, l_, k = make_case('t15_%d' % len(os.listdir(TD)), arm=arm_doc(), meta=meta_text(sneaky='0.00713331801', runner_rc='0'))
    rr = run_reader(mod, o, l_, k)
    rec('T15a 메타의 모르는 키는 옮기지 않는다 (값도 이름도)', rr.rc == 0 and no_leak(rr) == [] and 'sneaky' not in rr.report_text, no_leak(rr))
    a = arm_doc()
    dset(a, S3 + 'conv_cert.status', 'POSITIVE_0.00713331802')
    dset(a, S3 + 'manifest.backend_last_solve.precond', '0.00713331803')
    dset(a, S3 + 'manifest.physics_protocol_id', 'p3ca-0.00713331804')
    o, l_, k = make_case('t15b_%d' % len(os.listdir(TD)), arm=a)
    rr = run_reader(mod, o, l_, k)
    rec('T15b 글자 칸 = 닫힌 값 · 꼴만 (모르는 글자는 옮기지 않는다)', rr.rc in (3, 4) and no_leak(rr) == [], (rr.rc, no_leak(rr)))
    a = arm_doc()
    dset(a, S3 + 'manifest.backend_last_solve.fallback_reason', 'OutOfMemoryError: 0.00713331805 bytes')
    o, l_, k = make_case('t15c_%d' % len(os.listdir(TD)), arm=a)
    rr = run_reader(mod, o, l_, k)
    rec('T15c fallback 사유 글 = 있음 표지만', fld(rr, 'backend_fallback') is True and no_leak(rr) == [], (fld(rr, 'backend_fallback'), no_leak(rr)))
    # T16 같은 침대 대조 (S0 계획) · 핀
    a = arm_doc()
    dset(a, S3 + 'manifest.input_files.se', '0' * 16)
    o, l_, k = make_case('t16_%d' % len(os.listdir(TD)), arm=a)
    rr = run_reader(mod, o, l_, k)
    rec('T16a 팔의 입력 지문 ≠ S0 계획 (다른 침대): rc 4', rr.rc == 4 and fld(rr, 'bed_inputs_match_s0') is False, (rr.rc, fld(rr, 'bed_inputs_match_s0')))
    rec('T16b 정상 = 입력 지문 6/6 · tol_ff = S0 계획 · 코드 sha = 핀의 앞자리',
        fld(r, 'bed_inputs_match_s0') is True and fld(r, 'tol_ff_matches_s0') is True and fld(r, 'code_matches_pin') is True,
        (fld(r, 'bed_inputs_match_s0'), fld(r, 'tol_ff_matches_s0'), fld(r, 'code_matches_pin')))
    for tag, edit, mt in (('핀이 다름', None, meta_text(pin='a' * 40)), ('코드 sha 에 +dirty', 'e93efb6be+dirty', None)):
        a = arm_doc()
        if edit:
            dset(a, S3 + 'manifest.code_sha', edit)
        o, l_, k = make_case('t16c_%d' % len(os.listdir(TD)), arm=a, meta=mt)
        rr = run_reader(mod, o, l_, k)
        rec('T16c 팔의 코드 sha ≠ 핀 (%s): rc 4 · code_matches_pin False' % tag,
            rr.rc == 4 and fld(rr, 'code_matches_pin') is False, (rr.rc, fld(rr, 'code_matches_pin')))
    rc3 = receipt_doc()
    rc3['ca_ext_request']['cjunc']['tol_ff_um'] = 0.05
    o, l_, k = make_case('t16d_%d' % len(os.listdir(TD)), arm=arm_doc(), receipt=rc3)
    rr = run_reader(mod, o, l_, k)
    rec('T16d 영수증 tol_ff ≠ S0 계획: rc 4', rr.rc == 4 and fld(rr, 'tol_ff_matches_s0') is False, (rr.rc, fld(rr, 'tol_ff_matches_s0')))
    # T17 링크
    o, l_, k = make_case('t17_%d' % len(os.listdir(TD)), arm=arm_doc())
    os.symlink(os.path.join(o, 'run_receipt.json'), os.path.join(o, 'link.json'))
    rr = run_reader(mod, o, l_, k)
    rec('T17 폴더에 링크: 요약 sha 없음 + 사유 · rc 4', rr.rc == 4 and ((rr.rep or {}).get('folder') or {}).get('listing_sha256') is None, rr.rc)
    # T18 ASCII 출력
    rec('T18 화면 · 보고 JSON = ASCII 만', all(ord(c) < 128 for c in r.out) and all(ord(c) < 128 for c in r.report_text), '')
    # T19 SKIP (캐시된 팔 = 새 풀이 아님)
    o, l_, k = make_case('t19_%d' % len(os.listdir(TD)), arm=arm_doc(), log=runner_log() + '[p2] SKIP (완전) %s\n' % ARM)
    rr = run_reader(mod, o, l_, k)
    rec('T19 러너가 SKIP (옛 팔 재사용): rc 4 (이번 시도의 풀이가 아니다)', rr.rc == 4, rr.rc)
    # T20 영값 위상 · 단락 (조기 반환: CG 가 돌지 않았다)
    a = arm_doc()
    for path in (S3 + 'cg_iters',):
        ddel(a, path)
    for path, val in ((S3 + 'conv_cert', {'version': 'conv-cert-v2', 'status': 'VALID_ZERO_TOPOLOGY', 'ok': True, 'pass_d': None,
                                          'sigma': 0.0, 'reason': 'no_through_component'}),
                      (S3 + 'manifest.components', {'electronic': {'status': 'not_solvable'}})):
        dset(a, path, val)
    o, l_, k = make_case('t20_%d' % len(os.listdir(TD)), arm=a)
    rr = run_reader(mod, o, l_, k)
    rec('T20 영값 위상 (조기 반환): rc 3 · 상태 이름만', rr.rc == 3 and fld(rr, 'cert_status') == 'VALID_ZERO_TOPOLOGY', (rr.rc, fld(rr, 'cert_status')))


@case('T 판독기 (합성 폴더)')
def t_T():
    mod = load_reader(READER)
    suite_T(mod, chk)
    out, lg, run = make_case('t_cli', arm=arm_doc())
    p = subprocess.run([sys.executable, '-I', '-B', READER, '--outdir', out, '--logdir', lg, '--kit-run', run, '--s0-plan',
                        os.path.join(ROOT, S0PLAN_REL)], capture_output=True, text=True)
    chk('T90 명령 줄 (python3 -I -B): rc 0 · 화면에 표식 없음 · 보고 파일 생김',
        p.returncode == 0 and leaks(p.stdout, p.stderr) == [] and os.path.exists(os.path.join(lg, 'probe6_report.json')),
        (p.returncode, p.stdout[-300:], p.stderr[-300:]))
    p = subprocess.run([sys.executable, '-I', '-B', READER], capture_output=True, text=True)
    chk('T91 인자 없음: rc 2', p.returncode == 2, p.returncode)


# ═════════════════════════ M: 변이 (판독기를 한 군데씩 망가뜨리면 T 가 잡는다) ═════════════════════════
MUTANTS = (
    ('σ 칸을 허용 표에 넣음', [("('n_dof', ('n_dof',), 'posint', True),",
                               "('n_dof', ('n_dof',), 'posint', True), ('sig', ('sigma_e_eff_S_cm',), 'num', False),")]),
    ('σ 칸을 허용 표에 넣음 + 탐침선 끔', [("('n_dof', ('n_dof',), 'posint', True),",
                                            "('n_dof', ('n_dof',), 'posint', True), ('sig', ('sigma_e_eff_S_cm',), 'num', False),"),
                                           ("        if v in sealed:", "        if False:")]),
    ('증서 σ 를 허용 표에 넣음 + 탐침선 끔', [("('cert_imbalance', ('conv_cert', 'imbalance'), 'num', True),",
                                               "('cert_imbalance', ('conv_cert', 'imbalance'), 'num', True), ('cs', ('conv_cert', 'sigma'), 'num', False),"),
                                              ("        if v in sealed:", "        if False:")]),
    ('붙잡아 둔 칸을 값으로 냄 + 탐침선 끔', [("('cert_target_tol', ('conv_cert', 'target_tol'), 'num', False),",
                                               "('cert_target_tol', ('conv_cert', 'dsigma_rel'), 'num', False),"),
                                              ("        if v in sealed:", "        if False:")]),
    ('로그 원문을 그대로 옮김', [("    return _MASK_RE.sub('#', line)", "    return line")]),
    ('숫자를 자릿수만큼 가림 (자릿수가 남는다)', [("[0-9]+(?:[.,][0-9]+)*(?:[eE][+-]?[0-9]+)?')", "[0-9]')")]),
    ('봉인 검사 (결과 줄) 를 끔', [("            if not sealed_token(m.group(1)):", "            if False:")]),
    ('봉인 검사 (집전체 줄) 를 끔', [("            if SEAL_PREFIX not in line:", "            if False:")]),
    ('거부 표지를 안 봄', [("if nm.startswith('.rejected_'):", "if nm.startswith('.rejected__never'):")]),
    ('두 팔을 받음', [("if len(arms) > 1:", "if len(arms) > 99:")]),
    ('팔 번호를 안 봄', [("elif m.group(1) != '0':", "elif False:")]),
    ('영수증 팔 수를 안 봄', [("if receipt.get('receipt_arms') not in (1,) and not is_missing(receipt.get('receipt_arms')):", "if False:")]),
    ('모르는 파일을 안 봄', [("    if unknown:", "    if False:")]),
    ('미수렴을 안 봄', [("if f.get('unconverged') is not False:", "if False:")]),
    ('상태를 안 봄', [("if isinstance(st, str) and st != 'POSITIVE_SOLVED':", "if False:")]),
    ('글자 수를 받음 (bool · str → int)', [("if kind == 'int':\n        if isinstance(v, bool) or not isinstance(v, int):",
                                           "if kind == 'int':\n        if False:")]),
    ('비유한을 받음', [("if not math.isfinite(x):", "if False:")]),
    ('러너 rc 를 안 봄', [("elif rc_run != 0:", "elif False:")]),
    ('남은 파일을 받아들인 팔로 셈', [("if source != 'outdir':", "if False:")]),
    ('옛 남은 파일도 읽음', [("if start is None or os.path.getmtime(fp) < start - 2:", "if False:")]),
    ('폴더 요약에 크기를 뺌', [("'%s  %d  %s\\n' % (x['sha256'], x['size'], x['path'])", "'%s  %s\\n' % (x['sha256'], x['path'])")]),
    ('모르는 글자 값을 옮김', [("if not re.fullmatch(pat, v):", "if False:")]),
    ('DBE 팔을 읽음', [("if 'DBE' in nm:", "if 'DBE__never' in nm:")]),
    ('SKIP 을 안 봄', [("if log.get('skip_cached'):", "if False:")]),
    ('origin 을 안 봄', [("if f.get('origin_shift_zero') is not True:", "if False:")]),
    ('침대 대조를 안 봄', [("if f.get('bed_inputs_match_s0') is False:", "if False:")]),
    ('tol_ff 대조를 안 봄', [("if f.get('tol_ff_matches_s0') is False:", "if False:")]),
    ('핀 대조를 안 봄', [("if f.get('code_matches_pin') is False:", "if False:")]),
    ('반복 수 두 자리 대조를 안 봄', [("if f.get('cg_iters') != f.get('cert_iters'):", "if False:")]),
    ('백엔드 기대 대조를 안 봄', [("if isinstance(rb, str) and eb != rb:", "if False:")]),
)


@case('M 변이 (판독기)')
def t_M():
    src = read_text(READER)
    for name, pairs in MUTANTS:
        bad = [old for old, _new in pairs if src.count(old) != 1]
        if bad:
            chk('M 변이 자리 [%s]: 판독기에 정확히 한 번 있어야 한다' % name, False, [(b[:50], src.count(b)) for b in bad])
            continue
        msrc = src
        for old, new in pairs:
            msrc = msrc.replace(old, new)
        mp = os.path.join(TD, 'mut_%d.py' % len(os.listdir(TD)))
        write_text(mp, msrc)
        fails = []
        try:
            mod = load_reader(mp)
            suite_T(mod, lambda n, c, w='': fails.append(n) if not c else None)
        except Exception as e:                                 # noqa: BLE001 · 변이가 판독기를 깨뜨리면 그것도 잡힌 것
            fails.append('EXC %s' % type(e).__name__)
        chk('M 변이 [%s]: T 묶음이 잡는다 (실패 %d)' % (name, len(fails)), len(fails) > 0, '잡지 못함')


# ═════════════════════════ S: 정적 ═════════════════════════
def fenced_blocks(md_text, lang='bash'):
    return re.findall(r'^```%s\n(.*?)^```\s*$' % lang, md_text, re.S | re.M)


def wrapper_axes():
    src = read_text(WRAPPER)
    m = re.search(r'^AXES=\(\n(.*?)^\)\n', src, re.S | re.M)
    toks = re.findall(r'"?([A-Z0-9_]+)=([^"\s]*)"?', m.group(1)) if m else []
    tol = re.search(r'^TOL_FF=(\S+)$', src, re.M)
    kit = re.search(r'^KIT=(\S+)$', src, re.M)
    d = {}
    for k, v in toks:
        d[k] = v.replace('$TOL_FF', tol.group(1) if tol else '?').replace('$KIT', kit.group(1) if kit else '?')
    return d


def reg_probe_names():
    """등록 R §10-1 블록의 (2) 숫자 탐침 명령: env 이름 · 글자 그대로의 값 (<…> 자리는 None)."""
    txt = read_text(REG_DOC)
    i = txt.index('### 10-1. 실제 명령')
    blk = fenced_blocks(txt[i:])[0]
    j = blk.index('# (2) 숫자 탐침')
    cmd = blk[j:blk.index('# (1b) S0 단계 2')]
    lines = [ln for ln in cmd.split('\n') if not ln.lstrip().startswith('#')]
    joined = ' '.join(ln.rstrip('\\').strip() for ln in lines)
    out = {}
    for m in re.finditer(r'([A-Z][A-Z0-9_]*)=("[^"]*"|\S+)', joined):
        v = m.group(2).strip('"')
        out[m.group(1)] = None if '<' in v else v
    return out


@case('S 정적')
def t_S():
    rsrc = open(READER, 'rb').read()
    chk('S01a 판독기 = ASCII 만', all(b < 128 for b in rsrc), '')
    try:
        tree = ast.parse(rsrc.decode('ascii'), feature_version=(3, 8))
        ok38 = True
    except SyntaxError as e:
        tree, ok38 = None, False
        print('    ', e)
    chk('S01b 판독기 = Python 3.8 문법', ok38, '')
    mods = set()
    for n in ast.walk(tree) if tree else []:
        if isinstance(n, ast.Import):
            mods |= {a.name.split('.')[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            mods.add((n.module or '').split('.')[0])
    chk('S01c 판독기 = 표준 라이브러리만 (argparse · hashlib · json · math · os · re · sys)',
        mods <= {'argparse', 'hashlib', 'json', 'math', 'os', 're', 'sys'}, sorted(mods))
    try:
        ast.parse(read_text(__file__), feature_version=(3, 8))
        ok = True
    except SyntaxError:
        ok = False
    chk('S01d 이 시험 = Python 3.8 문법', ok, '')
    wsrc = open(WRAPPER, 'rb').read()
    chk('S02a 감시 셸 = ASCII 만', all(b < 128 for b in wsrc), [i for i, b in enumerate(wsrc) if b >= 128][:5])
    p = subprocess.run(['bash', '-n', WRAPPER], capture_output=True, text=True)
    chk('S02b 감시 셸 bash -n', p.returncode == 0, p.stderr[:300])
    # 축: 감시 셸 ↔ 시험의 독립 표 ↔ 등록 R §10-1 (2) ↔ 코드 상수 ↔ S0 계획
    wa = wrapper_axes()
    chk('S03a 감시 셸의 축 = 등록 축 (이름 · 값)', wa == AXES, {k: (wa.get(k), AXES.get(k)) for k in set(wa) | set(AXES) if wa.get(k) != AXES.get(k)})
    reg = reg_probe_names()
    names_w = set(wa) | {'P2_EXTRA', 'OUTDIR'}
    chk('S03b 축 이름 집합 = 등록 R §10-1 (2) 숫자 탐침 명령의 env 이름 집합', names_w == set(reg), sorted(names_w ^ set(reg)))
    lit = {k: v for k, v in reg.items() if v is not None and k not in ('P2_EXTRA', 'OUTDIR')}
    chk('S03c 등록 R 에 글자로 적힌 값 = 감시 셸 값', all(wa.get(k) == v for k, v in lit.items()),
        {k: (wa.get(k), v) for k, v in lit.items() if wa.get(k) != v})
    cj = re.search(r"^CJUNC_LEN_LAW = '([a-z0-9_]+)'", read_text(os.path.join(SCRIPTS, 'carbon_junction.py')), re.M)
    rt = re.search(r'^CERT_RTOL_MAX = ([0-9.e+-]+)', read_text(os.path.join(SCRIPTS, 'step3_conv_cert.py')), re.M)
    plan = s0_plan()
    chk('S03d 자리표 값의 근거: len_law = 코드 상수 · rtol = 증서 봉인 상한 · tol_ff = S0 계획 values_um.tol_ff (같은 float)',
        cj and wa.get('CJUNC_LEN_LAW') == cj.group(1) and rt and float(wa.get('STEP3_RTOL')) == float(rt.group(1))
        and float(wa.get('CJUNC_TOL_FF_UM')) == plan['values_um']['tol_ff'] and wa.get('CJUNC_TOL_FF_UM') == repr(plan['values_um']['tol_ff']),
        (cj and cj.group(1), rt and rt.group(1), plan['values_um']['tol_ff']))
    chk('S03e s_min = 0 µm 의 근거 줄이 등록 R §2-1b 에 있다 (1저자 11-09) · S0 계획 run_dir_name = 시험 상수',
        bool(re.search(r's_min 개발 단계 선택 = 0 .m \(바닥만\)', read_text(REG_DOC))) and float(wa.get('CJUNC_S_MIN_UM')) == 0.0
        and plan['source']['run_dir_name'] == S0_RUN, plan['source'].get('run_dir_name'))
    chk('S03f 감시 셸에 SIGMA_VGCF_OVERRIDE 축 없음 · --show-results 없음',
        'SIGMA_VGCF_OVERRIDE' not in wa and '--show-results' not in read_text(WRAPPER), '')
    psha = sha256_file(os.path.join(ROOT, S0PLAN_REL))
    chk('S03g 원장 줄 초안이 적은 S0 계획 sha256 (앞 8 · 뒤 6 자리) = 리포의 계획 파일 · 감시 셸의 계획 경로 = 시험 상수',
        ('%s…%s' % (psha[:8], psha[-6:])) in read_text(LEDGER_MD) and ('S0PLAN_REL=%s\n' % S0PLAN_REL) in read_text(WRAPPER), psha)
    # 블록
    bmd = read_text(BLOCK_MD)
    blocks = fenced_blocks(bmd)
    chk('S04a KGY_BLOCK.md = bash 블록 하나', len(blocks) == 1, len(blocks))
    blk = blocks[0] if blocks else ''
    chk('S04b 블록 = ASCII 만 · 느낌표 없음 · TAB 없음', all(ord(c) < 128 for c in blk) and '!' not in blk and '\t' not in blk,
        [c for c in blk if ord(c) >= 128][:5])
    chk('S04c 블록의 핀 자리 = <PIN> 한 번 · 가지 = claude/stoic-knuth-NObVQ · 감시 셸 경로 = 핀 작업 트리 안',
        blk.count('<PIN>') == 1 and 'claude/stoic-knuth-NObVQ' in blk and TOOLS_REL in blk, blk.count('<PIN>'))
    p = subprocess.run(['bash', '-n'], input=blk.replace('<PIN>', 'a' * 40), capture_output=True, text=True)
    chk('S04d 블록 bash -n', p.returncode == 0, p.stderr[:300])
    mi = re.search(r'^MAXITER=([0-9]+)$', blk, re.M)
    chk('S04e 블록의 MAXITER = 원장 줄 초안의 값', bool(mi) and ('--step3-maxiter %s' % mi.group(1)) in read_text(LEDGER_MD), mi and mi.group(1))
    # 원장 줄 초안
    lmd = read_text(LEDGER_MD)
    cmdm = re.search(r'env ((?:[A-Z][A-Z0-9_]*=(?:"[^"]*"|\S+) )+)bash ', lmd)
    led = {}
    for m in re.finditer(r'([A-Z][A-Z0-9_]*)=("[^"]*"|\S+)', cmdm.group(1) if cmdm else ''):
        led[m.group(1)] = m.group(2).strip('"')
    chk('S05a 원장 줄 초안의 명령 = 등록 축 (이름 · 값) + P2_EXTRA + OUTDIR',
        {k: v for k, v in led.items() if k not in ('P2_EXTRA', 'OUTDIR')} == AXES and set(led) == set(AXES) | {'P2_EXTRA', 'OUTDIR'},
        {k: (led.get(k), AXES.get(k)) for k in set(led) | set(AXES) if led.get(k) != AXES.get(k)})
    chk('S05b 원장 줄 초안: 번호 1 · 핀 <PIN> · 기계 kgy · 결과 칸 빈칸', '| 1 |' in lmd and '<PIN>' in lmd and 'kgy' in lmd, '')
    # 허용 표에 σ 류 이름 없음
    mod = load_reader(READER)
    bad_hint = ('sigma', 'I_bot', 'I_top', 'target_lo', 'target_hi', 'target_U', 'target_W', 'flow', 'scale', 'share', 'R_bulk',
                'dsigma', 'err_bound', 'width_rel', 'current', 'P_total', 'P_sum')
    paths = ['.'.join(row[1]) for row in mod['ARM_FIELDS']]
    chk('S06a 허용 표 (ARM_FIELDS) 의 경로에 σ 류 이름 없음', not [p_ for p_ in paths if any(h in p_ for h in bad_hint)],
        [p_ for p_ in paths if any(h in p_ for h in bad_hint)])
    chk('S06b 붙잡아 둔 칸은 허용 표에 없다', not (set(mod['HELD_BACK']) & set('conv_cert.' + p_.split('.')[-1] for p_ in paths if p_.startswith('conv_cert'))), '')
    # 주소 · 모델 이름 없음 · 게이트 단계
    allsrc = ''
    for pth in (READER, WRAPPER, BLOCK_MD, LEDGER_MD, README_MD):
        allsrc += read_text(pth) if os.path.exists(pth) else ''
    chk('S07a 준비물에 IPv4 꼴 · ssh · scp 명령 · 포트 없음',
        not re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', allsrc) and not re.search(r'\b(ssh|scp|sftp)\s+-', allsrc)
        and not re.search(r'\bport\s*[0-9]{2,5}\b', allsrc, re.I), '')
    chk('S07b 준비물에 모델 식별자 없음 (리포 규칙 · `wiki/tools/lint.py` 의 MODEL_ID 와 같은 꼴 + 계열 이름 낱말)',
        not re.search(r'claude-(?:opus|sonnet|haiku|fable)[a-z0-9.\-]*|\b(?:opus|sonnet|haiku|fable)\b', allsrc, re.I), '')
    ca = read_text(os.path.join(SCRIPTS, 'check_all.sh'))
    chk('S08 게이트 단계 한 줄 (check_all.sh)', len(re.findall(r"^run '[^']*probe6[^']*' python3 %s/test_probe6_read\.py\s*$" % re.escape(TOOLS_REL), ca, re.M)) == 1, '')
    chk('S09 README · 블록 · 원장 줄 초안이 있다', all(os.path.exists(p_) for p_ in (README_MD, BLOCK_MD, LEDGER_MD)), '')


# ═════════════════════════ F · B · R 공용: 가짜 홈 · 핀 저장소 · 가짜 nvidia-smi ═════════════════════════
def git(repo, *a, **kw):
    r = subprocess.run(['git', '-C', str(repo)] + list(GIT_CFG) + list(a), capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError('git %s rc %d: %s' % (a[:2], r.returncode, r.stderr[:300]))
    return r.stdout.strip()


FAKE_RUNNER = r'''#!/usr/bin/env bash
# fake runner (test only) - records what it was given, then behaves like the real runner's outputs
D="$PROBE6_FAKE_DIR"
env | LC_ALL=C sort > "$D/runner_env.txt"
pwd -P > "$D/runner_cwd.txt"
umask > "$D/runner_umask.txt"
echo called >> "$D/calls.txt"
RUN="$(cd "$PWD/kit_SBE_vgcf100/latest_run" && pwd -P)"
mkdir -p "$OUTDIR"
cp "$D/receipt.json" "$OUTDIR/run_receipt.json"
cat "$D/log_head.txt"
case "${PROBE6_FAKE_MODE:-ok}" in
  ok)   sleep "${PROBE6_FAKE_SLEEP:-3}"; cp "$D/arm.json" "$OUTDIR/$PROBE6_FAKE_ARM.json"; cat "$D/log_tail_ok.txt"; exit 0;;
  fail) sleep "${PROBE6_FAKE_SLEEP:-2}"; cp "$D/arm_failed.json" "$RUN/$PROBE6_FAKE_ARM.json.failed"; cat "$D/log_tail_fail.txt"; exit 1;;
  hang) ( sleep 300 ) & echo $! > "$D/child.pid"; wait;;
  big)  python3 -c 'import time; b = bytearray(300 * 1024 * 1024); time.sleep(300)';;
esac
'''
FAKE_SMI = r'''#!/usr/bin/env bash
# fake nvidia-smi (test only)
case "$*" in
  *--query-gpu=name,driver_version,memory.total*) echo "Fake GeForce RTX 3090, 535.183.01, 24576";;
  *--query-gpu=memory.used,utilization.gpu*)      echo "2345, 87";;
  *--query-compute-apps*)                         echo "1, 1111";;
  "")                                             echo "| NVIDIA-SMI 535.183.01   Driver Version: 535.183.01   CUDA Version: 12.2 |";;
  *) exit 1;;
esac
'''
FAKE_CUPY = '''__version__ = '0.0.test'


class _Runtime(object):
    @staticmethod
    def runtimeGetVersion():
        return 12040


class cuda(object):
    runtime = _Runtime
'''
#: cupy 대역 (GPU 계산 아님): payload 의 GPU 풀이 가지 (`scripts/step3_sigma.py` 의 `import cupy` 블록) 가 쓰는 이름만 numpy · scipy 로 잇는다.
#: 실제 러너 묶음 (R2 · R3) 이 등록 축 그대로 (GPU 기대 · 폴백 금지) 풀 수 있게 하는 자리다.  그 블록이 다른 cupy 이름을 쓰게 되면
#: payload 가 "GPU 를 못 쓴다" 로 멈추고 R2a 가 그 줄을 보여 준다.
FAKE_CUPY_NP = FAKE_CUPY + '''

import numpy as _np

asarray = _np.asarray


def asnumpy(a):
    return _np.asarray(a)
'''
FAKE_CUPYX = (
    ('cupyx/__init__.py', ''),
    ('cupyx/scipy/__init__.py', ''),
    ('cupyx/scipy/sparse/__init__.py', 'from scipy.sparse import csr_matrix, diags  # noqa: F401\n'),
    ('cupyx/scipy/sparse/linalg/__init__.py', 'from scipy.sparse.linalg import cg  # noqa: F401\n'),
)
#: 가짜 킷의 payload 줄 (생산 킷 꼴: `scripts/mpm_input_from_case.py` 가 `--step3-gpu` 를 늘 넣는다)
FAKE_KIT_SH = '#!/usr/bin/env bash\npython3 "$SCR/mpm_webapp_payload.py" --step3-gpu --out mpm_payload.json\n'


def make_home(name, shim_text=None, np_cupy=False):
    """가짜 홈: dem-venv (activate = PATH 앞에 가짜 python3 · nvidia-smi) · sdcp/kit (S0 계획의 런 폴더 이름) · 가짜 cupy
    (np_cupy = numpy · scipy 로 이은 대역 · 아니면 판 번호만 있는 껍데기)."""
    home = os.path.join(TD, name)
    bind = os.path.join(home, 'dem-venv', 'bin')
    os.makedirs(bind)
    write_text(os.path.join(bind, 'python3'),
               shim_text if shim_text is not None else '#!/usr/bin/env bash\nexec "%s" "$@"\n' % os.path.abspath(sys.executable), 0o755)
    write_text(os.path.join(bind, 'nvidia-smi'), FAKE_SMI, 0o755)
    write_text(os.path.join(bind, 'activate'), 'export VIRTUAL_ENV="%s/dem-venv"\nexport PATH="%s:$PATH"\n' % (home, bind))
    write_text(os.path.join(home, 'fakemods', 'cupy', '__init__.py'), FAKE_CUPY_NP if np_cupy else FAKE_CUPY)
    if np_cupy:
        for rel, body in FAKE_CUPYX:
            write_text(os.path.join(home, 'fakemods', *rel.split('/')), body)
    run = os.path.join(home, 'sdcp', KIT, S0_RUN)
    os.makedirs(run)
    write_text(os.path.join(run, 'se_dump.npy'), 'x')
    write_text(os.path.join(home, 'sdcp', KIT, 'run_mpm.sh'), FAKE_KIT_SH)
    os.symlink(S0_RUN, os.path.join(home, 'sdcp', KIT, 'latest_run'))
    return home


def make_pin_repo(name, real_scripts=False, plan_inputs=None):
    """핀 저장소 (git 고정물): 감시 셸 · 판독기 사본 · S0 계획 · 러너 (가짜 또는 이 리포 scripts/ 사본) → (저장소, 핀 40-hex).
    plan_inputs = S0 계획의 입력 지문 (source.inputs_sha256) 만 이 값으로 바꾼다 (픽스처 침대용 · 나머지 칸은 실제 계획 그대로)."""
    repo = os.path.join(TD, name)
    os.makedirs(os.path.join(repo, TOOLS_REL))
    shutil.copy(WRAPPER_SRC or WRAPPER, os.path.join(repo, TOOLS_REL, 'run_probe6.sh'))
    shutil.copy(READER, os.path.join(repo, TOOLS_REL, 'probe6_read.py'))
    os.makedirs(os.path.dirname(os.path.join(repo, S0PLAN_REL)))
    shutil.copy(os.path.join(ROOT, S0PLAN_REL), os.path.join(repo, S0PLAN_REL))
    if plan_inputs is not None:
        plan = json.loads(read_text(os.path.join(ROOT, S0PLAN_REL)))
        plan['source']['inputs_sha256'] = dict(plan_inputs)
        write_text(os.path.join(repo, S0PLAN_REL), json.dumps(plan, indent=1, sort_keys=True) + '\n')
    if real_scripts:
        shutil.copytree(SCRIPTS, os.path.join(repo, 'scripts'), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        os.makedirs(os.path.dirname(os.path.join(repo, PREREG_REL)), exist_ok=True)
        shutil.copy(os.path.join(ROOT, PREREG_REL), os.path.join(repo, PREREG_REL))
    else:
        write_text(os.path.join(repo, RUNNER_REL), FAKE_RUNNER, 0o755)
    shutil.copy(os.path.join(ROOT, '.gitignore'), os.path.join(repo, '.gitignore'))
    git(repo, 'init', '-q')
    git(repo, 'add', '-A')
    git(repo, 'commit', '-q', '-m', 'fixture')
    return repo, git(repo, 'rev-parse', 'HEAD')


def fake_dir(name, pin, arm_name=ARM):
    """가짜 러너가 읽는 재료: 영수증 · 팔 · 실패 팔 · 로그 조각 (표식이 든 줄 포함).  팔의 code_sha = 핀의 앞 9 자리 (실물과 같은 꼴)."""
    d = os.path.join(TD, name)
    os.makedirs(d)
    a = arm_doc()
    dset(a, S3 + 'manifest.code_sha', pin[:9])
    with open(os.path.join(d, 'arm.json'), 'w', encoding='utf-8') as f:
        json.dump(a, f)
    af = arm_doc()
    for path, val in ((S3 + 'unconverged', True), (S3 + 'cg_info', 400000), (S3 + 'cg_iters', 400000), (S3 + 'conv_cert.iters', 400000),
                      (S3 + 'conv_cert.info', 400000), (S3 + 'conv_cert.ok', False), (S3 + 'conv_cert.pass_a', False),
                      (S3 + 'manifest.components', {'electronic': {'status': 'unconverged'}}), (S3 + 'manifest.code_sha', pin[:9])):
        dset(af, path, val)
    with open(os.path.join(d, 'arm_failed.json'), 'w', encoding='utf-8') as f:
        json.dump(af, f)
    rc_ = receipt_doc()
    rc_['code_sha'] = pin[:9]
    with open(os.path.join(d, 'receipt.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(rc_, sort_keys=True))
    write_text(os.path.join(d, 'log_head.txt'), LOG_HEAD.format(arm=arm_name, maxiter='{:,}'.format(int(MAXITER))))
    write_text(os.path.join(d, 'log_tail_ok.txt'), LOG_TAIL_OK.format(sig=SEAL, seal2='[봉인]', arm=arm_name, maxiter_plain=MAXITER))
    write_text(os.path.join(d, 'log_tail_fail.txt'), LOG_TAIL_FAIL.format(sig=SEAL, seal2='[봉인]', arm=arm_name, maxiter_plain=MAXITER))
    return d


def wrapper_env(home, fake=None, **over):
    """감시 셸을 부르는 env: 부모 셸에 축 env 가 떠 있는 상황을 일부러 만든다 (감시 셸이 걷어내야 한다)."""
    e = {k: v for k, v in os.environ.items() if not k.startswith(('SIGMA_', 'SDCP_', 'PTFE_', 'CJUNC', 'STEP3_', 'MPM_', 'P2_', 'PROBE6_'))
         and k not in ('LEAN', 'VOX', 'ARMS', 'ARM_LIST', 'KITS', 'FIBRE_STAMP', 'BRIDGE_UM', 'OUTDIR', 'EXPECT_PROTOCOL', 'EXPECT_BACKEND',
                       'VIRTUAL_ENV', 'PYTHONPATH')}
    e.update(HOME=home, PATH=os.path.join(home, 'dem-venv', 'bin') + os.pathsep + os.environ.get('PATH', '/usr/bin:/bin'),
             PYTHONPATH=os.path.join(home, 'fakemods'), PYTHONDONTWRITEBYTECODE='1', PROBE6_SAMPLE_S='1')
    if fake:
        e.update(PROBE6_FAKE_DIR=fake, PROBE6_FAKE_ARM=ARM)
    e.update({k: str(v) for k, v in over.items()})
    return e


def run_wrapper(repo, pin, home, tag, env, maxiter=MAXITER, out=None, lg=None, mk_log=True, timeout=180, wrapper=None, umask=None):
    out = out or os.path.join(home, 'sdcp', 'ca1_probe6_%s_arm1' % tag)
    lg = lg or os.path.join(home, 'p6log_%s' % tag)
    if mk_log and not os.path.isdir(lg):
        os.makedirs(lg)
    w = wrapper or os.path.join(repo, TOOLS_REL, 'run_probe6.sh')
    pre = (lambda: os.umask(umask)) if umask is not None else None
    p = subprocess.run(['bash', w, repo, out, lg, pin, maxiter], env=env, capture_output=True, text=True, encoding='utf-8',
                       errors='replace', stdin=subprocess.DEVNULL, timeout=timeout, preexec_fn=pre)
    r = Res()
    r.rc, r.so, r.se, r.out, r.lg = p.returncode, p.stdout or '', p.stderr or '', out, lg
    r.meta = dict(ln.split('=', 1) for ln in read_text(os.path.join(lg, 'meta.txt')).splitlines() if '=' in ln) \
        if os.path.exists(os.path.join(lg, 'meta.txt')) else {}
    rp = os.path.join(lg, 'probe6_report.json')
    r.rep = json.loads(read_text(rp)) if os.path.exists(rp) else None
    return r


def bundle_members(lg):
    tg = os.path.join(lg, 'probe6_bundle.tgz')
    if not os.path.exists(tg):
        return None, {}
    import tarfile
    out = {}
    with tarfile.open(tg, 'r:gz') as t:
        names = t.getnames()
        for m in t.getmembers():
            if m.isfile():
                out[m.name] = t.extractfile(m).read().decode('utf-8', 'replace')
    return names, out


def proc_alive(pid):
    """살아 있는 프로세스인가: 끝났는데 거두어지지 않은 것 (좀비 · 상태 Z) 은 죽은 것으로 센다."""
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    try:
        with open('/proc/%d/stat' % pid) as f:
            return f.read().rsplit(')', 1)[1].split()[0] != 'Z'
    except (OSError, IndexError):
        return False


BUNDLE_ALLOWED = {'probe6_report.json', 'probe6_screen.txt', 'runner_filtered.log', 'env.txt', 'meta.txt', 'command.txt',
                  'samples.tsv', 'status.log', 'time_v.txt', 'arm_time_v.txt', 'probe6_reader.err', 'SHA256SUMS'}


@case('F 감시 셸 (가짜 러너)')
def t_F(pre='f'):
    repo, pin = make_pin_repo(pre + '_pin')
    home = make_home(pre + '_home')
    fd = fake_dir(pre + '_fake', pin)
    # F01 성공 경로 (부모 셸에 축 env · umask 002 를 일부러 둔다)
    env = wrapper_env(home, fd, SIGMA_VGCF_OVERRIDE='7854', LEAN='4', VOX='0.4', P2_EXTRA='--show-results', CJUNC_SV_CF='1',
                      MPM_PERIODIC_SIGMA='1', KITS='kit_DBE_sdcp1um_vgcf100', OUTDIR='/nonexistent/x', ARM_LIST='1,2', P2_ATTEMPT='1')
    r = run_wrapper(repo, pin, home, 'ok', env, umask=0o002)
    chk('F01a 성공 경로: 감시 셸 rc 0 · 러너 rc 0 · 판독 rc 0 (PROBE_OK) · DONE',
        r.rc == 0 and r.meta.get('runner_rc') == '0' and (r.rep or {}).get('verdict') == 'PROBE_OK'
        and os.path.exists(os.path.join(r.lg, 'DONE')), (r.rc, r.so[-900:], r.se[-300:]))
    chk('F01b 화면 (nohup.out 에 갈 글) 에 표식 없음 · 러너 원문 줄 없음 · 허용 칸은 보인다',
        leaks(r.so, r.se) == [] and 'STEP3' not in r.so and '[p2]' not in r.so and 'cg_iters' in r.so and '48211' in r.so, r.so[-600:])
    raw = read_text(os.path.join(r.lg, 'runner.log'))
    chk('F01c 러너 원문 로그는 로그 폴더에만 (표식이 든 줄 포함 · 그대로 보존)', SENT in leak_view(raw) and 'STEP3 solve:' in raw, raw[:200])
    names, members = bundle_members(r.lg)
    chk('F01d 묶음 = 허용된 이름만 (러너 원문 로그 · 팔 JSON · 영수증 없음)',
        names is not None and set(names) <= BUNDLE_ALLOWED and {'probe6_report.json', 'env.txt', 'meta.txt', 'samples.tsv',
                                                                   'runner_filtered.log', 'command.txt'} <= set(names), names)
    chk('F01e 묶음 안 어느 파일에도 표식 없음', leaks(*members.values()) == [], [n for n, t in members.items() if SENT in leak_view(t)])
    shas = dict((ln.split('  ', 1)[1], ln.split('  ', 1)[0]) for ln in members.get('SHA256SUMS', '').splitlines() if '  ' in ln)
    chk('F01f 묶음의 SHA256SUMS = 묶음 안 파일의 실제 sha256',
        bool(shas) and all(hashlib.sha256(members[n].encode('utf-8')).hexdigest() == h for n, h in shas.items() if n in members)
        and set(shas) == set(names) - {'SHA256SUMS'}, shas)
    # F02 러너가 받은 env · cwd · umask
    renv = dict(ln.split('=', 1) for ln in read_text(os.path.join(fd, 'runner_env.txt')).splitlines() if '=' in ln)
    want = dict(AXES, P2_EXTRA='--step3-maxiter ' + MAXITER, OUTDIR=r.out)
    axis_like = {k: v for k, v in renv.items() if k.startswith(('SIGMA_', 'SDCP_', 'PTFE_', 'CJUNC', 'STEP3_', 'MPM_', 'P2_'))
                 or k in ('LEAN', 'VOX', 'ARMS', 'ARM_LIST', 'KITS', 'FIBRE_STAMP', 'BRIDGE_UM', 'OUTDIR', 'EXPECT_PROTOCOL', 'EXPECT_BACKEND')}
    chk('F02a 러너가 받은 축 env = 등록 축 + P2_EXTRA + OUTDIR 뿐 (부모 셸의 SIGMA_VGCF_OVERRIDE · LEAN=4 · --show-results · ARM_LIST … 는 걷힘)',
        axis_like == want, {k: (axis_like.get(k), want.get(k)) for k in set(axis_like) | set(want) if axis_like.get(k) != want.get(k)})
    chk('F02b 걷어낸 이름이 메타에 남는다 (이름만)', set(r.meta.get('scrubbed', '').split()) >= {'SIGMA_VGCF_OVERRIDE', 'LEAN', 'VOX', 'P2_EXTRA', 'ARM_LIST'},
        r.meta.get('scrubbed'))
    chk('F02c 러너 cwd = 킷 뿌리 (~/sdcp) · umask 0022',
        read_text(os.path.join(fd, 'runner_cwd.txt')).strip() == os.path.realpath(os.path.join(home, 'sdcp'))
        and read_text(os.path.join(fd, 'runner_umask.txt')).strip() == '0022', read_text(os.path.join(fd, 'runner_cwd.txt')))
    # F03 실제 파일 · 폴더 모드 (부모 umask 002 였다)
    bad = []
    for base in (r.out, r.lg):
        for d, ds, fs in os.walk(base):
            for nm in ds + fs:
                if os.stat(os.path.join(d, nm)).st_mode & 0o022:
                    bad.append(nm)
    chk('F03 만든 파일 · 폴더에 그룹 · 기타 쓰기 비트 없음 (umask 022) · 메타 mode_bad 0', bad == [] and r.meta.get('mode_bad') == '0'
        and r.meta.get('umask') == '0022', bad[:5])
    chk('F04 메타: 핀 · maxiter · 시작 · 끝 · 전체 초 · 도구 sha256 · 킷 런 = S0 계획의 런 폴더',
        r.meta.get('pin') == pin and r.meta.get('maxiter') == MAXITER and int(r.meta.get('wall_s', -1)) >= 2
        and r.meta.get('tool_sha256_reader') == sha256_file(READER)
        and r.meta.get('tool_sha256_wrapper') == sha256_file(WRAPPER_SRC or WRAPPER)
        and r.meta.get('kit_run') == S0_RUN and r.meta.get('kit_run_matches_s0') == '1', r.meta)
    cmdt = read_text(os.path.join(r.lg, 'command.txt'))
    chk('F05 command.txt = 실제로 돈 명령 (축 전부 · 러너 경로 · cwd)',
        all(('%s=%s' % (k, v)) in cmdt for k, v in AXES.items()) and '--step3-maxiter ' + MAXITER in cmdt and RUNNER_REL in cmdt, cmdt[:300])
    envt = read_text(os.path.join(r.lg, 'env.txt'))
    chk('F06 환경 지문: python · numpy · scipy · cupy · GPU 이름 · 드라이버 · CUDA · BLAS (판만) · 호스트 이름 줄 없음',
        all(re.search(r'^%s=\S' % k, envt, re.M) for k in ('python', 'numpy', 'scipy', 'cupy', 'gpu_name', 'gpu_driver', 'cuda_version',
                                                               'blas_core', 'numpy_blas', 'kernel'))
        and not re.search(r'^(host|hostname|user|ip)=', envt, re.M | re.I), envt)
    tm = (r.rep or {}).get('timing') or {}
    rs = (r.rep or {}).get('resources') or {}
    chk('F07 표본: 줄 수로 잰 CG + 증서 구간 = 1 초 이상 · 전체 초 이하 (가짜 러너가 그 사이에 3 초 잔다) · GPU 최대 (가짜 2345) · RSS 표본 > 0',
        isinstance(tm.get('cg_cert_s'), int) and 1 <= tm.get('cg_cert_s') <= int(r.meta.get('wall_s', 0))
        and rs.get('gpu_used_max_mib') == 2345
        and (rs.get('rss_sum_max_kb') or 0) > 0, (tm, rs))
    # F08 멈춤 조건: 러너를 부르지 않는다
    calls0 = len(read_text(os.path.join(fd, 'calls.txt')).splitlines())
    env2 = wrapper_env(home, fd)
    stops = []

    def stop_case(label, needle, r2):
        """멈춤 하나: rc 2 · 화면의 STOP 줄이 그 사유 (다른 사유로 멈춘 것은 통과가 아니다) · '러너를 띄우지 않았다' 표지."""
        line = [ln for ln in r2.so.splitlines() if 'STOP:' in ln]
        stops.append((label, r2.rc, bool(line) and needle in line[-1] and 'runner not started' in line[-1], (line or [r2.so[-200:]])[-1][-160:]))

    stop_case('출력 폴더가 비어 있지 않음', 'output folder exists and is not empty',
              run_wrapper(repo, pin, home, 'ok', env2, out=r.out, lg=os.path.join(home, 'p6log_s1')))
    stop_case('로그 폴더에 옛 파일', 'log folder is not new', run_wrapper(repo, pin, home, 's2', env2, lg=r.lg))
    stop_case('핀 다름', 'worktree HEAD differs from PIN', run_wrapper(repo, 'b' * 40, home, 's3', env2))
    stop_case('maxiter 가 숫자가 아님', 'MAXITER must be a positive integer', run_wrapper(repo, pin, home, 's4', env2, maxiter='4e5'))
    stop_case('출력 폴더 이름에 _arm1 없음', 'must contain _arm1',
              run_wrapper(repo, pin, home, 's5', env2, out=os.path.join(home, 'sdcp', 'ca1_probe6_plain')))
    stop_case('로그 폴더 없음', 'log folder does not exist', run_wrapper(repo, pin, home, 's6', env2, mk_log=False))
    outside = os.path.join(TD, pre + '_outside', 'run_probe6.sh')     # 시험 대상 감시 셸의 사본을 핀 작업 트리 밖에 둔다 (옆에 판독기도)
    os.makedirs(os.path.dirname(outside))
    shutil.copy(WRAPPER_SRC or WRAPPER, outside)
    shutil.copy(READER, os.path.join(os.path.dirname(outside), 'probe6_read.py'))
    stop_case('핀 작업 트리 밖의 감시 셸 사본', 'not the copy inside the pinned worktree',
              run_wrapper(repo, pin, home, 's7', env2, wrapper=outside))
    write_text(os.path.join(repo, 'untracked_new.py'), 'x = 1\n')
    stop_case('작업 트리에 추적 안 된 파일', 'pinned worktree is not clean', run_wrapper(repo, pin, home, 's8', env2))
    os.remove(os.path.join(repo, 'untracked_new.py'))
    with open(os.path.join(repo, RUNNER_REL), 'a') as f:
        f.write('# edit\n')
    stop_case('추적 파일 고침', 'pinned worktree is not clean', run_wrapper(repo, pin, home, 's9', env2))
    git(repo, 'checkout', '-q', '--', RUNNER_REL)
    os.rename(os.path.join(home, 'sdcp', KIT, 'latest_run'), os.path.join(home, 'sdcp', KIT, 'latest_run_x'))
    os.makedirs(os.path.join(home, 'sdcp', KIT, 'run_other'))
    write_text(os.path.join(home, 'sdcp', KIT, 'run_other', 'se_dump.npy'), 'x')
    os.symlink('run_other', os.path.join(home, 'sdcp', KIT, 'latest_run'))
    stop_case('킷 런 폴더 ≠ S0 계획의 런 폴더', 'not the S0 stage-1 bed', run_wrapper(repo, pin, home, 's10', env2))
    os.remove(os.path.join(home, 'sdcp', KIT, 'latest_run'))
    os.rename(os.path.join(home, 'sdcp', KIT, 'latest_run_x'), os.path.join(home, 'sdcp', KIT, 'latest_run'))
    shutil.rmtree(os.path.join(home, 'sdcp', KIT, 'run_other'))
    e3 = dict(env2)
    e3['PYTHONPATH'] = ''
    stop_case('cupy 를 못 불러옴 (GPU 기대)', 'cupy cannot be imported', run_wrapper(repo, pin, home, 's11', e3))
    kit_sh = os.path.join(home, 'sdcp', KIT, 'run_mpm.sh')
    write_text(kit_sh, FAKE_KIT_SH.replace(' --step3-gpu', ''))
    stop_case('킷 payload 줄에 --step3-gpu 없음 (CPU 로 풀고 러너가 팔을 받지 않는다)', 'no --step3-gpu', run_wrapper(repo, pin, home, 's12', env2))
    for i, flag in enumerate(('--joule-heat', '--save-step4-grid step4_grid.npz')):
        write_text(kit_sh, FAKE_KIT_SH.replace(' --out', ' %s --out' % flag))
        stop_case('킷 payload 줄에 %s (다음 세대 payload 가 입구에서 거부한다)' % flag.split()[0], flag.split()[0],
                  run_wrapper(repo, pin, home, 's13%d' % i, env2))
    write_text(kit_sh, FAKE_KIT_SH)
    calls1 = len(read_text(os.path.join(fd, 'calls.txt')).splitlines())
    chk('F08a 멈춤 조건 %d 가지: 전부 rc 2 · 화면의 STOP 줄 = 그 사유 · "runner not started"' % len(stops),
        len(stops) == 14 and all(rc == 2 and hit for _n, rc, hit, _l in stops), [s for s in stops if not (s[1] == 2 and s[2])])
    chk('F08b 멈춤 = 러너를 부르지 않았다 (호출 수 그대로) · 출력 폴더를 만들지 않았다',
        calls1 == calls0 and not os.path.exists(os.path.join(home, 'sdcp', 'ca1_probe6_s3_arm1')), (calls0, calls1))
    # F09 실패 경로 (러너 rc 1 · 팔 없음 · .failed 남음)
    r = run_wrapper(repo, pin, home, 'fail', wrapper_env(home, fd, PROBE6_FAKE_MODE='fail'))
    names, members = bundle_members(r.lg)
    left = os.path.join(home, 'sdcp', KIT, S0_RUN, ARM + '.json.failed')
    chk('F09a 실패 경로: 감시 셸 rc 1 · 러너 rc 1 · 판독 rc 3 (미수렴) · 묶음은 만든다 · DONE',
        r.rc == 1 and r.meta.get('runner_rc') == '1' and (r.rep or {}).get('rc') == 3 and names is not None
        and os.path.exists(os.path.join(r.lg, 'DONE')), (r.rc, r.meta.get('runner_rc'), (r.rep or {}).get('rc'), r.so[-500:]))
    chk('F09b 실패 보존: 남은 파일 · 출력 폴더 · 원문 로그 그대로 · 묶음 · 화면에 표식 없음',
        os.path.exists(left) and os.path.isdir(r.out) and os.path.exists(os.path.join(r.lg, 'runner.log'))
        and leaks(r.so, r.se, *members.values()) == [], leaks(r.so, r.se, *members.values()))
    cpy = os.path.join(r.lg, 'kit_run_new', ARM + '.json.failed')
    knew = dict((x['name'], x) for x in (r.rep or {}).get('kit_run_new_files') or [])
    chk('F09c 킷 런 폴더의 새 파일 = 로그 폴더에 바이트 사본 (kit_run_new · sha256 같음 · 보고 copy_ok) · 묶음에는 없다',
        os.path.exists(cpy) and sha256_file(cpy) == sha256_file(left) and (knew.get(ARM + '.json.failed') or {}).get('copy_ok') is True
        and not [n for n in (names or []) if 'kit_run' in n], (os.path.exists(cpy), knew))
    old_sha = sha256_file(left)
    r = run_wrapper(repo, pin, home, 'again', wrapper_env(home, fd, PROBE6_FAKE_MODE='fail', PROBE6_FAKE_SLEEP='1'))
    bef = os.path.join(r.lg, 'kit_run_before', ARM + '.json.failed')
    bl = [x.get('name') for x in (r.rep or {}).get('kit_run_before_files') or []]
    chk('F09d 다음 시도: 러너가 같은 이름으로 덮어쓰기 전에 앞 시도의 남은 파일을 사본으로 (kit_run_before · sha256 = 앞 시도의 것)',
        os.path.exists(bef) and sha256_file(bef) == old_sha and ARM + '.json.failed' in bl and r.meta.get('kit_run_before') not in (None, '0'),
        (os.path.exists(bef), bl, r.meta.get('kit_run_before')))
    os.remove(left)
    # F10 상한 (PROBE6_CAP_GB=0 → 첫 표본에서 끝낸다) · 신호
    t0 = time.time()
    r = run_wrapper(repo, pin, home, 'cap', wrapper_env(home, fd, PROBE6_FAKE_MODE='big', PROBE6_CAP_GB='0'))
    chk('F10a 메모리 상한: 러너를 끝내고 기록 (cap_term 1 · 러너 rc ≠ 0) · 30 초 안 · 감시 셸 rc 1 · 묶음',
        r.rc == 1 and r.meta.get('cap_term') == '1' and r.meta.get('runner_rc') not in ('0', None) and time.time() - t0 < 60
        and bundle_members(r.lg)[0] is not None, (r.rc, r.meta, r.so[-400:]))
    out = os.path.join(home, 'sdcp', 'ca1_probe6_sig_arm1')
    lg = os.path.join(home, 'p6log_sig')
    os.makedirs(lg)
    p = subprocess.Popen(['bash', os.path.join(repo, TOOLS_REL, 'run_probe6.sh'), repo, out, lg, pin, MAXITER],
                         env=wrapper_env(home, fd, PROBE6_FAKE_MODE='hang'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         stdin=subprocess.DEVNULL)
    cp = os.path.join(fd, 'child.pid')
    for _ in range(100):
        if os.path.exists(cp) and read_text(cp).strip():
            break
        time.sleep(0.2)
    child = int(read_text(cp).strip()) if os.path.exists(cp) and read_text(cp).strip() else -1
    p.send_signal(signal.SIGTERM)
    try:
        p.wait(timeout=60)
        done = True
    except subprocess.TimeoutExpired:
        p.kill()
        done = False
    time.sleep(0.5)
    alive = proc_alive(child)
    meta = dict(ln.split('=', 1) for ln in read_text(os.path.join(lg, 'meta.txt')).splitlines() if '=' in ln) \
        if os.path.exists(os.path.join(lg, 'meta.txt')) else {}
    wp = read_text(os.path.join(lg, 'watcher.pid')).strip() if os.path.exists(os.path.join(lg, 'watcher.pid')) else ''
    chk('F10b 감시 셸에 TERM: 러너 자식까지 끝낸다 · aborted 1 · rc 1 · watcher.pid = 감시 셸의 pid',
        done and child > 0 and not alive and meta.get('aborted') == '1' and p.returncode == 1 and wp == str(p.pid),
        (done, child, alive, meta.get('aborted'), p.returncode, wp, p.pid))
    if child > 0 and alive:
        os.kill(child, signal.SIGKILL)


# ═════════════════════════ W: 감시 셸 변이 (고를 때만 · `--only W`) ═════════════════════════
#: 감시 셸을 한 군데씩 망가뜨린 사본으로 F 묶음을 통째로 다시 돌린다 (변이 하나에 F 한 번 = 약 25 초 → 게이트 기본 실행에는 넣지 않는다).
WRAPPER_MUTANTS = (
    ('부모 셸의 축 env 를 걷지 않음', [('      unset "$n"\n', '      :\n')]),
    ('등록 축 값 하나를 바꿈 (R_j)', [('CJUNC=1 CJUNC_RJ=1e6 ', 'CJUNC=1 CJUNC_RJ=1e5 ')]),
    ('maxiter 인자를 러너에 넘기지 않음', [('"P2_EXTRA=--step3-maxiter $MAXITER"', '"P2_EXTRA=--step3-maxiter 30000"')]),
    ('러너 원문 로그를 묶음에 넣음', [('for f in probe6_report.json probe6_screen.txt runner_filtered.log',
                                        'for f in runner.log probe6_report.json probe6_screen.txt runner_filtered.log')]),
    ('러너 원문 로그를 화면에 냄', [('say "runner ended - rc $RC, wall $((END - START)) s"',
                                      'say "runner ended - rc $RC, wall $((END - START)) s"; cat "$L/runner.log"')]),
    ('umask 를 고정하지 않음', [('set -u\numask 022\n', 'set -u\n')]),
    ('핀 대조를 하지 않음', [('[ "$HEAD_NOW" = "$PIN" ] || stop "worktree HEAD differs from PIN"', ':')]),
    ('작업 트리 깨끗함을 보지 않음', [('[ -z "$DIRTY" ] || stop', '[ -z "" ] || stop')]),
    ('핀 작업 트리 밖의 사본도 받음', [('[ -n "$TW" ] && [ "$T" = "$TW" ] || stop', '[ -n "$TW" ] || stop')]),
    ('킷 런 폴더 ↔ S0 계획 대조를 하지 않음', [('[ "$(basename "$RUNP")" = "$S0RUN" ] || stop', '[ -n "$S0RUN" ] || stop')]),
    ('킷 payload 줄의 --step3-gpu 를 보지 않음', [("grep -q -e '--step3-gpu' \"$K/run_mpm.sh\" 2>/dev/null \\\n  || stop", 'true \\\n  || stop')]),
    ('킷 payload 줄의 --joule-heat · --save-step4-grid 를 보지 않음', [('  if grep -q -e "$flag" "$K/run_mpm.sh" 2>/dev/null; then',
                                                                      '  if false; then')]),
    ('차 있는 출력 폴더도 받음', [('{ [ -d "$O" ] && [ ! -L "$O" ] && [ -z "$(ls -A "$O" 2>/dev/null)" ]; } || stop', 'true || stop')]),
    ('옛 로그 폴더도 받음', [('  if [ "$(basename "$f")" != nohup.out ]; then', '  if false; then')]),
    ('킷 뿌리로 가지 않고 러너를 띄움', [('cd "$ROOT" || stop "cannot enter the kit root"', ':')]),
    ('신호를 받아도 러너를 끝내지 않음', [('    say "signal received - stopping the runner"\n    kill_tree\n',
                                           '    say "signal received - stopping the runner"\n')]),
    ('메모리 상한에서 러너를 끝내지 않음', [('    say "host RSS cap reached ($((RS / 1048576)) GB >= $CAP GB) - stopping the runner"\n    kill_tree\n',
                                             '    say "host RSS cap reached ($((RS / 1048576)) GB >= $CAP GB) - stopping the runner"\n')]),
    ('킷 런 폴더의 새 파일을 사본으로 두지 않음', [('    mkdir -p "$L/kit_run_new" && cp "$f" "$L/kit_run_new/" && NNEW=$((NNEW + 1))',
                                                    '    NNEW=$((NNEW + 1))')]),
    ('앞 시도의 남은 파일을 사본으로 두지 않음', [('    mkdir -p "$L/kit_run_before" && cp "$f" "$L/kit_run_before/" || stop',
                                                  '    true || stop')]),
    ('cupy 를 못 불러와도 감', [("if grep -q '^cupy=ABSENT' \"$L/env.txt\"; then", 'if false; then')]),
)


@case('W 감시 셸 변이 (고를 때만)', optional=True)
def t_W():
    global chk, WRAPPER_SRC
    src = read_text(WRAPPER)
    real_chk = chk
    for i, (name, pairs) in enumerate(WRAPPER_MUTANTS):
        bad = [old for old, _new in pairs if src.count(old) != 1]
        if bad:
            real_chk('W 변이 자리 [%s]: 감시 셸에 정확히 한 번 있어야 한다' % name, False, [(b[:50], src.count(b)) for b in bad])
            continue
        msrc = src
        for old, new in pairs:
            msrc = msrc.replace(old, new)
        mp = os.path.join(TD, 'wm%d_src' % i, 'run_probe6.sh')
        write_text(mp, msrc)
        fails = []

        def coll(n, c, w=''):
            if not c:
                fails.append(n.split(' ')[0])
            return bool(c)
        chk, WRAPPER_SRC = coll, mp
        try:
            t_F(pre='wm%d' % i)
        except Exception as e:                                 # noqa: BLE001 · 변이가 F 묶음을 깨뜨리면 그것도 잡힌 것
            fails.append('EXC %s' % type(e).__name__)
        finally:
            chk, WRAPPER_SRC = real_chk, None
        real_chk('W 변이 [%s]: F 묶음이 잡는다 (%s)' % (name, ' · '.join(fails) or '-'), len(fails) > 0, '잡지 못함')


# ═════════════════════════ B: KGY 블록 끝까지 ═════════════════════════
@case('B 블록 (KGY_BLOCK.md 그대로)')
def t_B():
    repo, pin = make_pin_repo('b_pin')
    home = make_home('b_home')
    fd = fake_dir('b_fake', pin)
    bare = os.path.join(TD, 'b_origin.git')
    subprocess.run(['git', 'clone', '-q', '--bare', repo, bare], check=True, capture_output=True)
    git(bare, 'branch', 'claude/stoic-knuth-NObVQ', pin)
    subprocess.run(['git', 'clone', '-q', bare, os.path.join(home, 'dem-mt')], check=True, capture_output=True)
    blk = fenced_blocks(read_text(BLOCK_MD))[0].replace('<PIN>', pin)
    env = wrapper_env(home, fd, PROBE6_FAKE_SLEEP='2')
    p = subprocess.run(['bash'], input=blk, env=env, capture_output=True, text=True, cwd=home, timeout=120)
    lgs = glob.glob(os.path.join(home, 'p6log_*'))
    chk('B01 블록: rc 0 · 로그 폴더 하나 · 진행 보는 줄 · 묶음 자리를 화면에 알려 준다',
        p.returncode == 0 and len(lgs) == 1 and 'status.log' in p.stdout and 'probe6_bundle.tgz' in p.stdout, (p.returncode, p.stdout, p.stderr[-300:]))
    lg = lgs[0] if lgs else ''
    for _ in range(300):
        if lg and os.path.exists(os.path.join(lg, 'DONE')):
            break
        time.sleep(0.2)
    done = read_text(os.path.join(lg, 'DONE')) if lg and os.path.exists(os.path.join(lg, 'DONE')) else ''
    rp = os.path.join(lg, 'probe6_report.json')
    rep = json.loads(read_text(rp)) if os.path.exists(rp) else {}
    outs = glob.glob(os.path.join(home, 'sdcp', 'ca1_probe6_*_arm1'))
    chk('B02 블록이 띄운 감시 셸이 끝까지: DONE (러너 rc 0 · 판독 rc 0) · PROBE_OK · 출력 폴더 이름에 _arm1',
        'runner_rc=0' in done and 'report_rc=0' in done and rep.get('verdict') == 'PROBE_OK' and len(outs) == 1, (done, rep.get('verdict'), outs))
    nh = read_text(os.path.join(lg, 'nohup.out')) if lg and os.path.exists(os.path.join(lg, 'nohup.out')) else ''
    names, members = bundle_members(lg) if lg else (None, {})
    chk('B03 nohup.out · 블록 화면 · 묶음에 표식 없음 · 묶음 = 허용된 이름만',
        nh != '' and leaks(nh, p.stdout, p.stderr, *members.values()) == [] and names is not None and set(names) <= BUNDLE_ALLOWED, names)
    wt = glob.glob(os.path.join(home, 'dem-p6-*'))
    chk('B04 블록이 만든 작업 트리 = 핀 · 깨끗함 (런 뒤에도)',
        len(wt) == 1 and git(wt[0], 'rev-parse', 'HEAD') == pin and git(wt[0], 'status', '--porcelain', '--untracked-files=all') == '', wt)
    p2 = subprocess.run(['bash'], input=blk.replace(pin, 'zz'), env=env, capture_output=True, text=True, cwd=home, timeout=60)
    chk('B05 핀이 40 자리 hex 가 아니면 블록이 멈춘다 (rc 2 · 아무것도 만들지 않음)',
        p2.returncode == 2 and len(glob.glob(os.path.join(home, 'p6log_*'))) == 1, (p2.returncode, p2.stdout))
    p3 = subprocess.run(['bash'], input=fenced_blocks(read_text(BLOCK_MD))[0], env=env, capture_output=True, text=True, cwd=home, timeout=60)
    chk('B06 <PIN> 자리를 안 채운 블록 = 같은 STOP 줄로 멈춘다 (rc 2 · bash 문법 오류가 아니다 · 아무것도 만들지 않음)',
        p3.returncode == 2 and 'PIN is not a 40-hex commit' in p3.stdout and 'syntax error' not in p3.stderr
        and len(glob.glob(os.path.join(home, 'p6log_*'))) == 1 and len(glob.glob(os.path.join(home, 'dem-p6-*'))) == 1,
        (p3.returncode, p3.stdout, p3.stderr[-200:]))
    e4 = dict(env)
    shutil.move(os.path.join(home, 'dem-mt'), os.path.join(home, 'dem-mt-moved'))
    p4 = subprocess.run(['bash'], input=blk.replace(pin, 'c' * 40), env=e4, capture_output=True, text=True, cwd=home, timeout=60)
    shutil.move(os.path.join(home, 'dem-mt-moved'), os.path.join(home, 'dem-mt'))
    chk('B07 기준 체크아웃 자리 (BASE) 가 git 저장소가 아니면 블록이 멈춘다 (rc 2 · 그 사유 · 아무것도 만들지 않음)',
        p4.returncode == 2 and 'BASE is not a git checkout' in p4.stdout and len(glob.glob(os.path.join(home, 'p6log_*'))) == 1,
        (p4.returncode, p4.stdout))


# ═════════════════════════ R: 실제 러너 · 실제 payload (픽스처 킷 · CPU) ═════════════════════════
def real_sigma_signatures(arm_path):
    """실물 팔 JSON 에서 σ 류 수 (σ_e · 증서의 σ · 판 전류 · 목표량 구간 · scale · 소산 몫 · 접합 전류 …) 의 유효숫자 8 자리 · 6 자리 표식."""
    with open(arm_path, encoding='utf-8') as f:
        j = json.load(f)
    s3 = j['mpm_metrics']['step3']
    hints = ('sigma_e_eff', 'I_bot', 'I_top', 'target_lo', 'target_hi', 'target_U', 'target_W', 'target_flow', 'scale', 'R_bulk',
             'share', 'P_total', 'P_sum', 'sigma_apparent', 'sigma_resolve', 'ideal_R0')
    vals = []

    def walk(x, key):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, key + '.' + str(k))
        elif isinstance(x, list):
            for v in x:
                walk(v, key)
        elif isinstance(x, float) and x not in (0.0, 1.0) and x == x and any(h in key for h in hints) or \
                (isinstance(x, float) and key.endswith('conv_cert.sigma')):
            vals.append(x)
    walk(s3, 'step3')
    sig8, sig6 = set(), set()
    for v in vals:
        d = re.sub(r'[^0-9]', '', ('%.15e' % abs(v)).split('e')[0])
        if len(d.strip('0')) >= 6:
            sig8.add(d[:8])
            sig6.add(re.sub(r'[^0-9]', '', ('%.5e' % abs(v)).split('e')[0]))
    return vals, sig8, sig6


def real_leaks(sig8, sig6, texts_full, texts_screen):
    bad = [s for s in sig8 if any(s in leak_view(t) for t in texts_full)]
    bad += [s for s in sig6 if any(s in leak_view(t) for t in texts_screen)]
    return bad


@case('R 실물 (실제 러너 · payload · 픽스처 킷)')
def t_R():
    if ARGS.no_real:
        _skipped.append('R (--no-real)')
        print('  SKIP  R 묶음: --no-real (PASS 로 세지 않는다)')
        return
    sys.path.insert(0, SCRIPTS)
    try:
        import test_ca_ext_runner as TR                        # noqa: E402 · 가짜 python3 (규율 관문 둘만 건너뛴다) · 사본 없음
        import test_rint_r_chain_e2e as E2E                    # noqa: E402 · 생산 단위 픽스처 침대 (vox 0.15) · 사본 없음
    except Exception as e:                                     # noqa: BLE001
        chk('R00 실물 묶음 재료 (numpy · scipy · 리포 시험 모듈) 를 불러온다', False, '%s: %s' % (type(e).__name__, e))
        return
    shim = TR.SHIM.replace('__REAL__', os.path.abspath(sys.executable))
    # R1 러너 직접 (EXPECT_BACKEND=cpu: 이 기계에 GPU 없음 · 나머지 축 = 등록 축) → 판독기
    ws = os.path.join(TD, 'r1_ws')
    run = os.path.join(ws, KIT, S0_RUN)
    os.makedirs(run)
    E2E.make_bed(run)
    write_text(os.path.join(ws, KIT, 'run_mpm.sh'), E2E.KIT_SH)
    os.symlink(S0_RUN, os.path.join(ws, KIT, 'latest_run'))
    os.makedirs(os.path.join(ws, '_shim'))
    bind = os.path.join(TD, 'r1_bin')
    write_text(os.path.join(bind, 'python3'), shim, 0o755)
    out = os.path.join(ws, 'ca1_probe6_r1_arm1')
    env = {k: v for k, v in os.environ.items() if not k.startswith(('SIGMA_', 'SDCP_', 'PTFE_', 'CJUNC', 'STEP3_', 'MPM_', 'P2_'))
           and k not in ('LEAN', 'VOX', 'ARMS', 'ARM_LIST', 'KITS', 'FIBRE_STAMP', 'BRIDGE_UM', 'OUTDIR', 'EXPECT_PROTOCOL', 'EXPECT_BACKEND',
                         'VIRTUAL_ENV')}
    env.update(AXES)
    env.update(PATH=bind + os.pathsep + os.environ.get('PATH', ''), MPM_NO_VENV='1', PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
               PYTHONIOENCODING='utf-8', EXPECT_BACKEND='cpu', P2_EXTRA='--step3-maxiter ' + MAXITER, OUTDIR=out,
               SHIM_LOG=os.path.join(ws, '_shim'), P2_SCR=SCRIPTS)
    t0 = int(time.time())
    p = subprocess.run(['bash', os.path.join(SCRIPTS, 'sdcp_gain_vox015_8arm.sh')], cwd=ws, env=env, capture_output=True, text=True,
                       encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL, timeout=900)
    log = (p.stdout or '') + (p.stderr or '')
    arms = glob.glob(os.path.join(out, 'p2_*.json'))
    chk('R1a 실제 러너 (등록 축 · 백엔드만 cpu): rc 0 · 팔 하나 · 이름 = 시험 상수 (블록 · 판독기가 기대하는 꼴)',
        p.returncode == 0 and [os.path.basename(a) for a in arms] == [ARM + '.json'], (p.returncode, log[-700:]))
    if not arms:
        return
    chk('R1b 러너 화면: 결과 σ 는 봉인 표지 · 봉인 · 판정기 원값 덤프 없음 (킷이 SDCP 기본이 아니다)',
        SEAL in log and '계약 봉인을 **돌리지 않는다.**' in log and 'collect-only' not in log, log[-400:])
    vals, sig8, sig6 = real_sigma_signatures(arms[0])
    chk('R1c (시험의 판별력) 실물 팔 JSON 에 σ 류 수가 있다 · 러너 원문 로그에는 그 수가 없다',
        len(vals) >= 10 and real_leaks(sig8, sig6, [log], [log]) == [], (len(vals), real_leaks(sig8, sig6, [log], [log])))
    lg = os.path.join(TD, 'r1_log')
    os.makedirs(lg)
    write_text(os.path.join(lg, 'runner.log'), log)
    nl = len(log.split('\n')) - 1
    write_text(os.path.join(lg, 'samples.tsv'), '#epoch\telapsed_s\tlog_lines\trss_sum_kb\trss_max_kb\tgpu_used_mib\tgpu_ours_mib\tgpu_util\n'
               '%d\t0\t3\t1000\t900\tNA\tNA\tNA\n%d\t5\t%d\t2000\t1900\tNA\tNA\tNA\n' % (t0, t0 + 5, nl))
    head = git(ROOT, 'rev-parse', 'HEAD')
    write_text(os.path.join(lg, 'meta.txt'), meta_text(pin=head, start_epoch=t0, end_epoch=t0 + 5, wall_s=5, time_v=0))
    write_text(os.path.join(lg, 'env.txt'), ENV_TEXT)
    mod = load_reader(READER)
    r = run_reader(mod, out, lg, run, s0=False)
    f = (r.rep or {}).get('fields') or {}
    chk('R1d 판독기가 실물 꼴을 읽는다: 필수 칸 전부 값 (없음 0) · 반복 수 > 0 · 이어 풀기 반복 수 · 상태 POSITIVE_SOLVED · 백엔드 cpu',
        r.rep is not None and isinstance(f.get('cg_iters'), int) and f.get('cg_iters') > 0 and f.get('cg_iters') == f.get('cert_iters')
        and isinstance(f.get('cert_resolve_iters'), int) and f.get('cert_status') == 'POSITIVE_SOLVED' and f.get('cert_ok') is True
        and f.get('electronic_backend_used') == 'cpu' and isinstance(f.get('n_dof'), int)
        and not [k for k in mod['REQUIRED'] if is_missing(f.get(k))], (r.rc, r.out[-700:], r.err[-300:]))
    lg_ = (r.rep or {}).get('log') or {}
    chk('R1e 실물 로그 줄을 읽는다: dof (= 팔 JSON n_dof) · 잔차 · STEP3 초 · maxiter · rtol · 봉인 표지 · 준비 초',
        lg_.get('solve_n_dof') == f.get('n_dof') and lg_.get('done_n_dof') == f.get('n_dof') and isinstance(lg_.get('done_resid'), float)
        and isinstance(lg_.get('done_step3_s'), int) and lg_.get('cg_maxiter') == int(MAXITER) and lg_.get('cg_rtol') == 1e-12
        and lg_.get('sealed') is True and isinstance(lg_.get('face_alpha_prep_s'), int) and isinstance(lg_.get('cjunc_prep_s'), int)
        and lg_.get('arm_tag') == ARM, lg_)
    bad = real_leaks(sig8, sig6, [r.report_text, r.filtered, json_strings(r.rep) if r.rep else ''], [r.out, r.err])
    chk('R1f 실물 σ 류 수 (유효숫자 8 자리 · 화면은 6 자리) 가 판독기 출력 어디에도 없다', bad == [], bad)
    dirty = str(f.get('code_sha', '')).endswith('+dirty')      # 이 리포의 추적 파일을 고친 채 돌리면 payload 가 +dirty 를 싣는다
    chk('R1g 실물: 판독 rc 0 · PROBE_OK (같은 침대 대조는 요청 안 함 = 픽스처 침대)%s' % (' [더러운 트리: rc 4 · 핀 불일치만]' if dirty else ''),
        (r.rc == 4 and f.get('code_matches_pin') is False and len((r.rep or {}).get('problems') or []) == 1) if dirty
        else (r.rc == 0 and (r.rep or {}).get('verdict') == 'PROBE_OK'), (r.rc, (r.rep or {}).get('problems')))
    # R1h 생산 킷 꼴 (payload 줄에 --joule-heat · --save-step4-grid) = 다음 세대 payload 가 입구에서 거부한다 (감시 셸의 멈춤 조건 둘의 근거)
    ws_p = os.path.join(TD, 'r1p_ws')
    run_p = os.path.join(ws_p, KIT, S0_RUN)
    os.makedirs(run_p)
    E2E.make_bed(run_p)
    write_text(os.path.join(ws_p, KIT, 'run_mpm.sh'), E2E.KIT_SH_PROD)
    os.symlink(S0_RUN, os.path.join(ws_p, KIT, 'latest_run'))
    os.makedirs(os.path.join(ws_p, '_shim'))
    env_p = dict(env, OUTDIR=os.path.join(ws_p, 'ca1_probe6_r1p_arm1'), SHIM_LOG=os.path.join(ws_p, '_shim'))
    pp = subprocess.run(['bash', os.path.join(SCRIPTS, 'sdcp_gain_vox015_8arm.sh')], cwd=ws_p, env=env_p, capture_output=True, text=True,
                        encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL, timeout=900)
    log_p = (pp.stdout or '') + (pp.stderr or '')
    hit = sorted(set(re.findall(r'S[12]_(?:CJUNC|FACE_ALPHA)_REFUSED\|(JOULE|STEP4_GRID)\|', log_p)))
    chk('R1h 생산 킷 꼴 (--joule-heat · --save-step4-grid) + 등록 축: payload 가 입구에서 거부 (JOULE · STEP4_GRID) · 러너 rc ≠ 0 · 팔 없음',
        pp.returncode != 0 and set(hit) >= {'JOULE', 'STEP4_GRID'} and not glob.glob(os.path.join(env_p['OUTDIR'], 'p2_*.json'))
        and 'STEP3 solve:' not in log_p, (pp.returncode, hit, log_p[-500:]))
    # R2 감시 셸 + 실제 러너 + 실제 payload, 등록 축 그대로 (GPU 기대 · 폴백 금지).  이 기계에 GPU 가 없어 cupy 자리에 numpy · scipy 대역을 둔다
    #    (payload 의 GPU 풀이 가지가 그대로 돈다 · GPU 계산은 아니다).  S0 계획 = 실제 계획에서 입력 지문만 이 픽스처 침대의 것으로 바꾼 것
    #    (S0 도구 `ca_s0_census.kit_input_record` 가 낸 sha256) → 판독기의 같은 침대 대조가 실제 두 생산자 (S0 도구 ↔ payload) 사이에서 선다
    import ca_s0_census as S0                                  # noqa: E402 · S0 단계 1 도구 (실제 계획의 입력 지문을 낸 함수)
    home = make_home('r2_home', shim_text=shim, np_cupy=True)
    run2 = os.path.join(home, 'sdcp', KIT, S0_RUN)
    os.remove(os.path.join(run2, 'se_dump.npy'))
    E2E.make_bed(run2)
    kit_gpu = E2E.KIT_SH.replace('--n-vox 24', '--step3-gpu --n-vox 24')
    write_text(os.path.join(home, 'sdcp', KIT, 'run_mpm.sh'), kit_gpu)
    rec = S0.kit_input_record(os.path.join(home, 'sdcp', KIT))
    plan_in = dict((k, v['sha256']) for k, v in rec['files'].items())
    repo, pin = make_pin_repo('r2_pin', real_scripts=True, plan_inputs=plan_in)
    os.makedirs(os.path.join(home, '_shim'))
    wenv = wrapper_env(home, None, SHIM_LOG=os.path.join(home, '_shim'), PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    r = run_wrapper(repo, pin, home, 'r2', wenv, timeout=900)
    arm2 = os.path.join(r.out, ARM + '.json')
    raw = read_text(os.path.join(r.lg, 'runner.log')) if os.path.exists(os.path.join(r.lg, 'runner.log')) else ''
    chk('R2a 감시 셸 + 실제 러너 + 실제 payload (등록 축 그대로 · GPU 가지 = cupy 대역): 감시 셸 rc 0 · 러너 rc 0 · 팔이 출력 폴더에 · DONE',
        '--step3-gpu' in kit_gpu and r.rc == 0 and r.meta.get('runner_rc') == '0' and os.path.exists(arm2)
        and os.path.exists(os.path.join(r.lg, 'DONE')), (r.rc, r.meta.get('runner_rc'), raw[-900:], r.so[-400:]))
    if not os.path.exists(arm2):
        return
    f = (r.rep or {}).get('fields') or {}
    chk('R2b 판독 rc 0 · PROBE_OK · 백엔드 요청 = 사용 = gpu · 같은 침대 (S0 도구의 입력 지문 ↔ payload 매니페스트) · 핀 · tol_ff 대조 True',
        (r.rep or {}).get('rc') == 0 and (r.rep or {}).get('verdict') == 'PROBE_OK' and f.get('backend_requested') == 'gpu'
        and f.get('backend_used') == 'gpu' and f.get('electronic_backend_used') == 'gpu' and f.get('bed_inputs_match_s0') is True
        and f.get('code_matches_pin') is True and f.get('tol_ff_matches_s0') is True and f.get('cg_iters') == f.get('cert_iters')
        and isinstance(f.get('cg_iters'), int) and f.get('cg_iters') > 0,
        ((r.rep or {}).get('rc'), (r.rep or {}).get('problems'),
         dict((k, f.get(k)) for k in ('backend_requested', 'backend_used', 'bed_inputs_match_s0', 'code_matches_pin', 'tol_ff_matches_s0', 'cg_iters'))))
    vals, sig8, sig6 = real_sigma_signatures(arm2)
    names, members = bundle_members(r.lg)
    bad = real_leaks(sig8, sig6, list(members.values()) + [json_strings(r.rep) if r.rep else ''], [r.so, r.se])
    chk('R2c 실물 σ 류 수가 감시 셸 화면 · 묶음 어디에도 없다 (묶음 = 허용된 이름만) · 러너 원문 로그에도 없다 (봉인 표지)',
        bad == [] and names is not None and set(names) <= BUNDLE_ALLOWED and len(vals) >= 10 and real_leaks(sig8, sig6, [raw], [raw]) == []
        and SEAL in raw, (bad, names, len(vals)))
    chk('R2d 런 뒤 핀 작업 트리 깨끗함 (git_lines_after 0) · 만든 파일에 그룹 · 기타 쓰기 비트 없음 (mode_bad 0) · 킷 런 폴더에 팔이 남지 않았다',
        r.meta.get('git_lines_after') == '0' and r.meta.get('mode_bad') == '0' and not glob.glob(os.path.join(run2, 'p2_*.json*')),
        (r.meta.get('git_lines_after'), r.meta.get('mode_bad'), glob.glob(os.path.join(run2, 'p2_*.json*'))))
    it_ok = f.get('cg_iters') if isinstance(f.get('cg_iters'), int) else 0
    # R3 같은 홈 · 같은 핀 · maxiter 2 (모이기 전에 한도) = 미수렴 실물: payload 가 .failed 로 남기고 러너가 받지 않는다 → 판독기가 거기서 읽는다
    r3 = run_wrapper(repo, pin, home, 'r3', wenv, maxiter='2', timeout=900)
    left = os.path.join(run2, ARM + '.json.failed')
    f3 = (r3.rep or {}).get('fields') or {}
    raw3 = read_text(os.path.join(r3.lg, 'runner.log')) if os.path.exists(os.path.join(r3.lg, 'runner.log')) else ''
    chk('R3a 한도에 닿음 (maxiter 2 < 수렴에 든 %d 회): 러너 rc 1 · 팔은 출력 폴더에 없고 킷 런 폴더에 .failed · 감시 셸 rc 1 · 묶음 · DONE' % it_ok,
        it_ok > 2 and r3.rc == 1 and r3.meta.get('runner_rc') == '1' and os.path.exists(left)
        and not glob.glob(os.path.join(r3.out, 'p2_*.json')) and os.path.exists(os.path.join(r3.lg, 'DONE'))
        and bundle_members(r3.lg)[0] is not None, (it_ok, r3.rc, r3.meta.get('runner_rc'), raw3[-900:]))
    if os.path.exists(left):
        chk('R3b 판독 rc 3 · PROBE_NOT_CONVERGED · 출처 = 킷 런 폴더의 .failed · 반복 수 = 한도 (2) · 이어 풀기도 한도까지 (2 · info 2) · '
            '미수렴 표지 · 잔차 · 불균형은 값으로',
            (r3.rep or {}).get('rc') == 3 and (r3.rep or {}).get('verdict') == 'PROBE_NOT_CONVERGED'
            and (r3.rep or {}).get('source') == 'kit_run_failed' and f3.get('cg_iters') == 2 and f3.get('cert_iters') == 2
            and f3.get('cg_info') == 2 and f3.get('cert_resolve_iters') == 2 and f3.get('cert_resolve_info') == 2
            and f3.get('unconverged') is True and f3.get('cert_ok') is False and f3.get('electronic_status') == 'unconverged'
            and isinstance(f3.get('cg_resid'), float) and isinstance(f3.get('cert_imbalance'), float),
            ((r3.rep or {}).get('rc'), (r3.rep or {}).get('source'), (r3.rep or {}).get('problems'),
             dict((k, f3.get(k)) for k in ('cg_iters', 'cert_iters', 'cert_resolve_iters', 'cert_resolve_info', 'unconverged', 'cert_ok',
                                           'cert_status', 'electronic_status'))))
        vals3, s8, s6 = real_sigma_signatures(left)
        names3, members3 = bundle_members(r3.lg)
        bad3 = real_leaks(s8, s6, list(members3.values()) + [json_strings(r3.rep) if r3.rep else ''], [r3.so, r3.se])
        lg3 = (r3.rep or {}).get('log') or {}
        masked3 = lg3.get('masked_lines') or []
        chk('R3c 미수렴 팔의 σ 류 수가 감시 셸 화면 · 묶음 어디에도 없다 · 러너의 미수렴 줄 · 증서 실패 줄 = 읽은 수로 다시 적은 칸 (info · 상태 · ⓐ–ⓓ) · '
            'ABORT 줄 = 수를 가린 꼴',
            bad3 == [] and names3 is not None and set(names3) <= BUNDLE_ALLOWED and len(vals3) >= 10 and lg3.get('not_converged_info') == 2
            and lg3.get('cert_fail_status') == 'POSITIVE_SOLVED' and len(lg3.get('cert_fail_pass') or []) == 4
            and lg3['cert_fail_pass'][0] is False and lg3.get('cg_maxiter') == 2 and any('ABORT' in m for m in masked3) and any('unconverged' in m for m in masked3)
            and all(not re.search(r'[0-9]', m) for m in masked3), (bad3, len(vals3), lg3.get('not_converged_info'), masked3[-5:]))
        cpy = os.path.join(r3.lg, 'kit_run_new', ARM + '.json.failed')
        chk('R3d 실패 보존: 남은 .failed 그대로 · 로그 폴더에 바이트 사본 (sha256 같음) · 출력 폴더 그대로 · 작업 트리 깨끗함',
            os.path.exists(cpy) and sha256_file(cpy) == sha256_file(left) and os.path.isdir(r3.out) and r3.meta.get('git_lines_after') == '0',
            (os.path.exists(cpy), r3.meta.get('git_lines_after')))
    # R2e (대조) 같은 실물 팔을 실제 S0 계획 (kgy 침대의 입력 지문) 으로 읽으면 다른 침대로 잡는다.  판독기를 직접 부르므로 맨 끝에 둔다
    mod = load_reader(READER)
    rr = run_reader(mod, r.out, r.lg, run2, s0=True)
    chk('R2e (대조) 같은 팔 + 실제 S0 계획 = 다른 침대: rc 4 · bed_inputs_match_s0 False · 문제는 그 하나',
        rr.rc == 4 and fld(rr, 'bed_inputs_match_s0') is False and len((rr.rep or {}).get('problems') or []) == 1,
        (rr.rc, (rr.rep or {}).get('problems')))
    # R4 GPU 를 못 쓰는 기계 (cupy 는 불러와지지만 풀이 모듈이 없다) + 등록 축: payload 가 CPU 로 내려가지 않고 멈춘다 (--step3-require-gpu)
    home4 = make_home('r4_home', shim_text=shim)
    run4 = os.path.join(home4, 'sdcp', KIT, S0_RUN)
    os.remove(os.path.join(run4, 'se_dump.npy'))
    E2E.make_bed(run4)
    write_text(os.path.join(home4, 'sdcp', KIT, 'run_mpm.sh'), kit_gpu)
    os.makedirs(os.path.join(home4, '_shim'))
    r4 = run_wrapper(repo, pin, home4, 'r4', wrapper_env(home4, None, SHIM_LOG=os.path.join(home4, '_shim'), PYTHONUTF8='1',
                                                        PYTHONIOENCODING='utf-8'), timeout=900)
    raw4 = read_text(os.path.join(r4.lg, 'runner.log')) if os.path.exists(os.path.join(r4.lg, 'runner.log')) else ''
    masked4 = ((r4.rep or {}).get('log') or {}).get('masked_lines') or []
    chk('R4a GPU 를 못 쓴다 + 등록 축: payload 가 풀지 않고 멈춘다 (STEP3 ABORT · CPU 폴백 없음) · 러너 rc 1 · 팔 없음 (출력 폴더 · 킷 런 폴더)',
        r4.rc == 1 and r4.meta.get('runner_rc') == '1' and 'STEP3 ABORT' in raw4 and 'CPU fallback' not in raw4
        and not glob.glob(os.path.join(r4.out, 'p2_*.json')) and not glob.glob(os.path.join(run4, 'p2_*.json*')),
        (r4.rc, r4.meta.get('runner_rc'), raw4[-900:]))
    chk('R4b 판독 rc 4 · 출처 none (읽을 팔이 없다) · 반복 수 칸 = 없음 · 멈춘 줄이 수를 가린 꼴로 보고에 있다 · 묶음',
        (r4.rep or {}).get('rc') == 4 and (r4.rep or {}).get('source') == 'none' and is_missing(((r4.rep or {}).get('fields') or {}).get('cg_iters'))
        and any('ABORT' in m and 'require-gpu' in m for m in masked4) and all(not re.search(r'[0-9]', m) for m in masked4)
        and bundle_members(r4.lg)[0] is not None, ((r4.rep or {}).get('rc'), (r4.rep or {}).get('source'), masked4[-4:]))


def main():
    global ARGS, TD
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--only', default='', help='쉼표로 나눈 이름 접두 (예: T,M)')
    ap.add_argument('--no-real', action='store_true', help='실제 러너 묶음 (R) 을 뺀다: 뺀 것은 PASS 로 세지 않는다')
    ap.add_argument('--keep', action='store_true', help='임시 폴더를 남긴다')
    ARGS = ap.parse_args()
    TD = tempfile.mkdtemp(prefix='probe6_')
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    try:
        for tag, fn in CASES + [(t, f) for t, f in OPTIONAL if any(t.startswith(o) for o in only)]:
            if only and not any(tag.startswith(o) for o in only):
                continue
            print('\n── %s' % tag)
            try:
                fn()
            except Exception as e:                             # noqa: BLE001 · 준비물이 없을 때도 시험 단위로 기록
                chk('%s: 실행' % tag.split()[0], False, '%s: %s' % (type(e).__name__, e))
    finally:
        if ARGS.keep:
            print('\n  (임시 폴더 남김: %s)' % TD)
        else:
            shutil.rmtree(TD, ignore_errors=True)
    print('\n%d PASS · %d FAIL%s' % (_ok, len(_fail), (' · 생략 %s' % ', '.join(_skipped)) if _skipped else ''))
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()

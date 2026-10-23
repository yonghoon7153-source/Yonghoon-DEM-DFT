#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② B6 — payload 의 탄소 접합 (S2 cjunc) · SDCP 접합 수정자 (S3 sdcp_mod) 배선 · 조합 정책 · 러너 · 판정기 (시험 먼저 · 2026-10-20).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §4-2 · §5-2 (스위치) · §6 (수렴) · §7 (세대 · 영수증 · LEAN 표 ·
`p3ca-` · `unknown:ca_ext`) · 등록 R 초안 §3 · §4 · §10 (런 꼴).  1저자 10-20 N1–N18 = 권고대로.

  python3 scripts/test_ca_ext_b6.py                     # 전부 (payload 끝-끝 포함 · 1–2 분)
  python3 scripts/test_ca_ext_b6.py --skip-payload      # payload 끝-끝 (P · B 의 payload 부분) 빼고
  python3 scripts/test_ca_ext_b6.py --only R,P          # 이름 접두로 고르기
  python3 scripts/test_ca_ext_b6.py --old-scripts DIR   # 끔 비트 동일 (DIR = 고치기 전 scripts/ 사본) — B 묶음

묶음:
  R  run_contract — cjunc · sdcp_mod 하위 블록 등록 (생산자 · 소비자 같은 함수) · 요청 칸 `ca_ext_requested` · p3ca id ·
     unknown:ca_ext · 계약 위반 변이 · 영수증 (digest 옛 값 보존 · 요청 ↔ 블록 대조 · rtol) · 러너 요청 검사 · 수렴 증서 · CLI 회계 (규칙 M)
  P  payload 끝-끝 — 접합 · SDCP 수정자 CLI · 입구 거부 (구조화 사유) · 매니페스트 · 영수증 (LEAN 표) · 물리 상식 (Rayleigh) ·
     조합 정책 (★ Z3 10-20 — face_alpha + cjunc = 허용 (옛 B6 임시 거부 뺌 · 조합 규칙 전수 = test_ca_ext_z3 A) · face_alpha + rtol
     = 허용 · cjunc + rtol = 허용) · --expect-physics 의 ca_ext 칸
  B  (--old-scripts) 끔 비트 동일 — payload 매니페스트 (code_sha · exec_env 빼고) · step3 값.  ★ 10-21 (D · 브리프 묶음 5): 경로 차이
     전부를 한 표 `OLD_DIFF_ALLOW` (세대 Z3 · RCA1 — 켠 노브의 새 칸만) 로 판정 · 끈 경우 = 차이 0 · `--expect-identical` (기반 =
     바로 앞 커밋) = 표 없이 차이 0 · B0u = 그 표 · 함수의 합성 단위 시험 (기반 사본 없이).  z3 O 묶음이 같은 표 · 함수를 쓴다.
     ⚠ 기반 사본 옆에 docs/ 가 있어야 한다 (집전체 앵커 CSV — 없으면 대체 값 차이가 이유와 함께 실패).
⚠ PASS 는 배선 · 계약 · 구현의 증거이지 R_j 값 · 판정 (R) 의 물리 검증이 아니다.
"""
import argparse
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

RC = None
CW = None                       # ca_ext_cjunc (구현 전에는 None — 시험 단위로 실패를 기록한다)
ARGS = None
_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    cond = bool(cond)
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return cond


CASES = []


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def deep(x):
    return json.loads(json.dumps(x))


# ═════════════════════════ 공용 — 봉인 코호트 매니페스트 (합성 블록의 바탕) ═════════════════════════
def cohort_manifests(name='w4b_ptfe_off_20260827'):
    import glob
    return [json.load(open(f, encoding='utf-8'))['step3']['manifest']
            for f in sorted(glob.glob(os.path.join(ROOT, 'docs/data', name, 'p2_*.json')))]


CJ_REQ = dict(R_j_ohm=1.0e6, len_law='len_scaled_v0', unreg_law='cut', s_min_um=0.5, tol_ff_um=0.5, ptfe_jlaw='P0')
#: ★ 10-21 (사전 리뷰 PRE-impl-07) — 합성 접합 매니페스트의 지문 칸 (소문자 hex 32 · 증서 결합 `run_contract.cert_binding_problem` 이
#:   이 칸과 대조한다 — `good_cert` 가 같은 값을 싣는다)
CJ_FP = {'registry': 'a' * 32, 'sid': 'b' * 32, 'plan_rows': 'c' * 32}


def cj_manifest(sdcp_c=None, ionic_plan=False, n_inst=3, **over):
    """봉인 코호트 (off · LEAN 2) 매니페스트 하나를 접합 켠 꼴로 바꾼 합성 매니페스트 (계약 단위 시험용).
    블록은 모듈의 기록 함수로 만든다 (사본 없음) — 영수증 · 증거 수는 서로 맞게."""
    req = dict(CJ_REQ, **over)
    m = deep(cohort_manifests()[0])
    m.update(field_requested=False, ptfe_stamp='off', ptfe_stamp_requested='off', ptfe_zero_dof=False, ptfe_cells_observed=0,
             component_plan={'electronic': True, 'ionic': bool(ionic_plan), 'thermal': False, 'pore': False, 'collector': False})
    prot = CW.cjunc_protocol_record(ptfe_stamp=m['ptfe_stamp'], **req)
    nc = n_inst if sdcp_c == 1.0 else 0                       # c = 1 → 근접 instance 전부 축약 (여기서는 전부 근접)
    ns = n_inst if sdcp_c is not None else 0
    counts = {'n_instances': n_inst, 'n_edge': n_inst - nc, 'n_contract': nc, 'n_cut_p1': 0, 'n_unrealized': 0,
              'n_none_inf': 0, 'n_long': 0, 'n_sdcp_near': ns, 'n_contracted_by_c': nc, 'n_ptfe_cov': 0,
              'len_mult_sum_edge': float(n_inst - nc), 'len_mult_max': 1.0}
    fp = dict(CJ_FP)
    solve = {'solved': True, 'n_junction_edges': n_inst - nc, 'n_contracted': nc, 'short': False, 'n_extra_dofs': 2}
    rc = {'electronic_main': {'status': 'applied', 'n_instances': n_inst, 'n_junction_edges': n_inst - nc, 'solved': True,
                              'fp_registry': fp['registry']},
          'electronic_wetted': {'status': 'disabled', 'why': '--no-collector'},
          'electronic_bare': {'status': 'disabled', 'why': '--no-collector'},
          'ionic': ({'status': 'not_requested'} if ionic_plan else {'status': 'disabled', 'why': '--no-ion'})}
    ev = CW.cjunc_evidence_record(counts=counts, census={'n_instances': n_inst}, solve=solve, receipts=rc, fp=fp,
                                  sdcp_mod_c=sdcp_c)
    blk = {'schema': RC.CA_EXT_SCHEMA, 'cjunc': {'protocol': prot, 'evidence': ev}}
    want = ['cjunc']
    if sdcp_c is not None:
        blk['sdcp_mod'] = {'protocol': CW.sdcp_mod_protocol_record(c=sdcp_c, tol_sj_um=req['tol_ff_um']),
                           'evidence': CW.sdcp_mod_evidence_record(n_sdcp_near=ns, n_contracted_by_c=nc)}
        want.append('sdcp_mod')
    m['ca_ext_requested'] = sorted(want)
    m['ca_ext'] = blk
    m['physics_protocol_id'] = RC.physics_protocol_id(m)
    return m


def good_cert(sigma, rtol=1.0e-12, channel='electronic'):
    import step3_conv_cert as CC
    return {'version': CC.CERT_VERSION, 'rtol_used': rtol, 'rtol_max': CC.CERT_RTOL_MAX, 'eps_I': CC.CERT_EPS_I,
            'resolve_rtol': max(rtol * CC.CERT_RESOLVE_FACTOR, CC.CERT_RESOLVE_RTOL_FLOOR),
            'resolve_rtol_floor': CC.CERT_RESOLVE_RTOL_FLOOR, 'resolve_tol': CC.CERT_RESOLVE_TOL, 'info': 0, 'resid': 1e-13,
            'I_bot': 1.0, 'I_top': 1.0, 'imbalance': 1e-9, 'sigma': float(sigma), 'sigma_resolve': float(sigma) * (1 + 1e-12),
            'dsigma_rel': 1e-12, 'resolve_info': 0, 'resolve_I_bot': 1.0, 'resolve_I_top': 1.0,
            'pass_a': True, 'pass_b': True, 'pass_c': True, 'ok': True,
            #  ★ 10-21 증서 v2 (Codex RCA-07 · RCA-13) — 상태 · ⓓ 목표량 증서 (구간 [1, 1] ∋ 게시 판 전류 1 · scale = σ)
            'status': CC.STATUS_POSITIVE, 'pass_d': True, 'target_tol': CC.CERT_TARGET_TOL, 'target_version': CC.TARGET_VERSION,
            'target_fp': CC.TARGET_FP_RULE, 'target_ledger_ok': True, 'target_topology': 'through', 'target_lo': 1.0,
            'target_hi': 1.0, 'scale': float(sigma),
            #  ★ 10-21 (PRE-impl-07) — 증서 ↔ 런 결합 칸 = `cj_manifest` 의 지문 (접합 = 주 전자 솔브만 · face_alpha 없음)
            'bind_version': CC.BIND_VERSION, 'fp_sid': CJ_FP['sid'], 'fp_sig': 'd' * 32, 'fp_face_plan': None,
            'fp_cjunc_registry': (CJ_FP['registry'] if channel == 'electronic' else None),
            'fp_cjunc_rows': (CJ_FP['plan_rows'] if channel == 'electronic' else None)}


# ═════════════════════════ R 묶음 — run_contract ═════════════════════════
@case('R run_contract — cjunc · sdcp_mod 하위 블록 · 요청 칸 · p3ca · unknown:ca_ext · 영수증 · 요청 검사 · 증서 · CLI 회계')
def t_rc():
    subs = getattr(RC, 'CA_EXT_SUBBLOCKS', {})
    chk('R1 하위 블록 등록 — cjunc · sdcp_mod 가 ptfe_face 와 같은 꼴 (모듈 · 검증기 · protocol 정본 키)',
        all(k in subs and subs[k][1] == 'ca_ext_cjunc' for k in ('cjunc', 'sdcp_mod'))
        and subs.get('cjunc', (0, 0, ''))[2] == 'cjunc_block_problem'
        and subs.get('sdcp_mod', (0, 0, ''))[2] == 'sdcp_mod_block_problem', sorted(subs))
    fld = RC.ca_ext_protocol_fields()
    chk('R2 protocol_ext 칸 정본에 접합 · 수정자 칸 (R_j · 법칙 둘 · s_min · tol_ff · P · c)',
        {'ca_ext.cjunc.R_j_ohm', 'ca_ext.cjunc.len_law', 'ca_ext.cjunc.unreg_law', 'ca_ext.cjunc.s_min_um',
         'ca_ext.cjunc.tol_ff_um', 'ca_ext.cjunc.ptfe_jlaw', 'ca_ext.sdcp_mod.c'} <= set(fld))
    m = cj_manifest()
    pid = m['physics_protocol_id']
    chk('R3 접합 + 블록 = p3ca- + 16 hex · protocol_ok · ca_ext_record_ok',
        pid.startswith('p3ca-') and len(pid) == 21 and RC.protocol_ok(m) == (True, None)
        and RC.ca_ext_record_ok(m) == (True, None), (pid, RC.ca_ext_record_ok(m)))
    chk('R4a 요청 칸 있고 블록 없음 → unknown:ca_ext · ca_ext_record_ok 거부',
        RC.physics_protocol_id({k: v for k, v in m.items() if k != 'ca_ext'}) == RC.CA_EXT_UNKNOWN
        and not RC.ca_ext_record_ok({k: v for k, v in m.items() if k != 'ca_ext'})[0])
    chk('R4b 블록 있고 요청 칸 없음 → unknown:ca_ext',
        RC.physics_protocol_id({k: v for k, v in m.items() if k != 'ca_ext_requested'}) == RC.CA_EXT_UNKNOWN)
    m_nob = {k: v for k, v in m.items() if k not in ('ca_ext', 'ca_ext_requested')}
    chk('R4c 둘 다 없음 = 옛 p2 함수 그대로 (코호트 id 와 같은 식)', RC.physics_protocol_id(m_nob).startswith('p2-'))
    for nm, v in (('문자열', 'cjunc'), ('빈 목록', []), ('모르는 이름', ['cjunc', 'mystery']), ('정렬 안 됨', ['sdcp_mod', 'cjunc']),
                  ('중복', ['cjunc', 'cjunc']), ('ptfe_face (요청 = ptfe_stamp)', ['ptfe_face']), ('None', None)):
        mm = dict(m_nob, ca_ext_requested=v)
        chk(f'R5 요청 칸 모양 틀림 [{nm}] (블록 없음) → unknown:ca_ext (조용히 p2 로 내려가지 않는다)',
            RC.physics_protocol_id(mm) == RC.CA_EXT_UNKNOWN and not RC.ca_ext_record_ok(mm)[0], RC.physics_protocol_id(mm))
    m_ev = deep(m)
    m_ev['ca_ext']['cjunc']['evidence']['census']['n_instances'] = 99
    chk('R6a 증거만 바뀜 → id 같음', RC.physics_protocol_id(m_ev) == pid)
    chk('R6b R_j 바뀜 → id 다름', RC.physics_protocol_id(cj_manifest(R_j_ohm=1.0e4)) != pid)
    chk('R6c 미등록 면 법칙 바뀜 (cut → fused) → id 다름', RC.physics_protocol_id(cj_manifest(unreg_law='fused')) != pid)
    m0, m1 = cj_manifest(sdcp_c=0.0), cj_manifest(sdcp_c=1.0)
    chk('R6d SDCP c = 0 · 1 → id 서로 다름 · 둘 다 정상', RC.physics_protocol_id(m0) != RC.physics_protocol_id(m1)
        and RC.ca_ext_record_ok(m0) == (True, None) and RC.ca_ext_record_ok(m1) == (True, None),
        (RC.ca_ext_record_ok(m0), RC.ca_ext_record_ok(m1)))
    chk('R6e 관찰 세대 (p3ca = 현행) · 낮춘 신고 거부', RC.observed_generation(m) == RC.SCHEMA_VERSION
        and RC.schema_of(dict(m, schema_version=2))[0] is None)

    def mut(base, fn):
        x = deep(base)
        fn(x)
        return RC.ca_ext_record_ok(x)[0]
    E = lambda x: x['ca_ext']['cjunc']['evidence']          # noqa: E731
    Pp = lambda x: x['ca_ext']['cjunc']['protocol']         # noqa: E731
    bad = {
        '모델 판 다름': lambda x: Pp(x).update(model='r3-carbon-junction-port-v0'),
        '길이 법칙 다름': lambda x: Pp(x).update(len_law='point_v0'),
        '규칙 판 다름 (port)': lambda x: Pp(x)['rules'].update(port='nearest_v0'),
        'L_par 손으로 바꿈': lambda x: Pp(x).update(L_par_um=0.6),
        'r_port 손으로 바꿈': lambda x: Pp(x).update(r_port_um=0.15),
        'tol_P ≠ tol_ff': lambda x: Pp(x).update(tol_P_um=0.1),
        'R_j = 0 (정량 아님)': lambda x: Pp(x).update(R_j_ohm=0.0),
        'R_j = inf': lambda x: Pp(x).update(R_j_ohm=float('inf')),
        'R_j 문자열': lambda x: Pp(x).update(R_j_ohm='1e6'),
        's_min = None (미등록 · 정량 거부)': lambda x: Pp(x).update(s_min_um=None),
        's_min 음수': lambda x: Pp(x).update(s_min_um=-0.1),
        'P1 (face_alpha 아님)': lambda x: Pp(x).update(ptfe_jlaw='P1'),
        'protocol 의 ptfe_stamp ≠ 매니페스트': lambda x: Pp(x).update(ptfe_stamp='centerline'),
        'ptfe_stamp 만 face_alpha (ptfe_face 블록 없음 · 접합 protocol 은 off)': lambda x: x.update(ptfe_stamp='face_alpha'),
        '점 스탬프': lambda x: x.update(fibre_stamp='point'),
        '주기 xy': lambda x: x.update(periodic_xy=True),
        '필드 요청 (LEAN 4)': lambda x: x.update(field_requested=True),
        '집전체 계획 켬': lambda x: x['component_plan'].update(collector=True),
        '계면 표 (r1) 동시': lambda x: x.update(interface_model='r1'),
        'SDCP 브리지 진단 팔': lambda x: x.update(sdcp_bridge_um=0.3),
        'VGCF 절연 (σ 0)': lambda x: x.update(sigma_vgcf_S_cm=0.0),
        '영수증 키 빠짐': lambda x: E(x)['receipts'].pop('ionic'),
        '주 영수증 missing': lambda x: E(x)['receipts']['electronic_main'].update(status='missing'),
        '주 영수증 모르는 상태': lambda x: E(x)['receipts']['electronic_main'].update(status='mystery'),
        '주 영수증 applied 인데 instance 0': lambda x: E(x)['receipts']['electronic_main'].update(n_instances=0),
        '주 영수증 solved False': lambda x: E(x)['receipts']['electronic_main'].update(solved=False),
        '주 영수증 원장 지문 ≠ 증거': lambda x: E(x)['receipts']['electronic_main'].update(fp_registry='f' * 32),
        'wetted 가 applied (v0 = 집전체 끔)': lambda x: E(x)['receipts'].update(
            electronic_wetted={'status': 'applied', 'n_instances': 3, 'n_junction_edges': 3, 'solved': True,
                               'fp_registry': 'r' * 32}),
        '이온 영수증 applied_without_request': lambda x: E(x)['receipts'].update(ionic={'status': 'applied_without_request'}),
        '이온 계획 끔인데 이온 not_requested': lambda x: E(x)['receipts'].update(ionic={'status': 'not_requested'}),
        'disabled 인데 사유 없음': lambda x: E(x)['receipts'].update(electronic_bare={'status': 'disabled'}),
        '수 합 깨짐 (n_edge +1)': lambda x: E(x)['counts'].update(n_edge=E(x)['counts']['n_edge'] + 1),
        'P0 인데 절단 수 > 0': lambda x: E(x)['counts'].update(n_cut_p1=1, n_edge=E(x)['counts']['n_edge'] - 1),
        '극한 none_inf > 0 (R_j 유한)': lambda x: E(x)['counts'].update(n_none_inf=1, n_edge=E(x)['counts']['n_edge'] - 1),
        '접합 간선 수 ≠ 영수증': lambda x: E(x)['solve'].update(n_junction_edges=0),
        '축약 수 ≠ 원장': lambda x: E(x)['solve'].update(n_contracted=2),
        '단락 상태': lambda x: E(x)['solve'].update(short=True),
        '거부 사유 남음': lambda x: E(x).update(rejections=[{'code': 'self_s_min_missing', 'n': 1}]),
        '진단 표 빠짐': lambda x: E(x).pop('diagnostics'),
        '표지 다름': lambda x: E(x).update(label='탄소 접합'),
        '한정어 빠짐': lambda x: E(x).update(qualifiers=[]),
        '수정자 c 기록 ↔ 블록 없음 불일치': lambda x: E(x).update(sdcp_mod_c=1.0),
        '요청 칸에 sdcp_mod 만 더함 (블록 없음)': lambda x: x.update(ca_ext_requested=['cjunc', 'sdcp_mod']),
    }
    for nm, fn in bad.items():
        chk(f'R7 ca_ext_record_ok 거부 [{nm}]', not mut(m, fn))
    #  ── 수정자 (S3) — S2 없이 = 거부 · 블록 사이 대조 ──
    s1 = cj_manifest(sdcp_c=1.0)
    S = lambda x: x['ca_ext']['sdcp_mod']                   # noqa: E731
    sbad = {
        'S2 블록 없음 (수정자만)': lambda x: (x['ca_ext'].pop('cjunc'), x.update(ca_ext_requested=['sdcp_mod'])),
        'c = 0.5 (정량은 0 · 1 만)': lambda x: S(x)['protocol'].update(c=0.5),
        'tol_sj ≠ 접합 tol_ff': lambda x: S(x)['protocol'].update(tol_sj_um=0.1),
        '근접 수 ≠ 접합 원장': lambda x: S(x)['evidence'].update(n_sdcp_near=1),
        'c = 1 인데 축약 0': lambda x: (S(x)['evidence'].update(n_contracted_by_c=0)),
        '판별 표지 거짓': lambda x: S(x)['evidence'].update(s3_discriminating=False),
        '접합 증거의 c ≠ 수정자 c': lambda x: E(x).update(sdcp_mod_c=0.0),
        '수정자 표지 다름': lambda x: S(x)['evidence'].update(label='SDCP'),
    }
    for nm, fn in sbad.items():
        chk(f'R8 sdcp_mod 거부 [{nm}]', not mut(s1, fn))
    m_fa = deep(m)
    m_fa['ptfe_stamp'] = 'face_alpha'
    m_fa['ca_ext']['ptfe_face'] = {'protocol': {}, 'evidence': {}}
    chk('R9 face_alpha + 접합 — ptfe_face 블록이 빈 꼴 (protocol · 증거 없음) = 거부 (★ Z3 조합은 받지만 각 블록 검증기는 그대로 · '
        '조합 양성 = P15c · test_ca_ext_z3 AP1)', not RC.ca_ext_record_ok(m_fa)[0])
    #  ── 영수증 (러너 ↔ 매니페스트) — 옛 digest 보존 · 요청 대조 · rtol ──
    _rcpts = [json.load(open(os.path.join(ROOT, 'docs/data', d, 'run_receipt.json'), encoding='utf-8'))
              for d in ('w4_ptfe_centerline_20260827', 'w4b_ptfe_off_20260827')]
    import glob
    import hashlib

    def _base_body_digest(r):                       # 고치기 전 함수 본문 그대로 (선택 칸 없음)
        body = {k: r.get(k) for k in sorted(set(RC.RECEIPT_AXES) | set(RC.RECEIPT_META))}
        return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()[:12]
    _all = [json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(ROOT, 'docs/data/**/run_receipt.json'),
                                                                         recursive=True))]
    #  ⚠ 저장된 digest 는 영수증 축이 늘기 전 세대의 것도 있다 (고치기 전 함수로도 27/44 만 재현) — 그래서 불변량은 "선택 칸 없는 영수증의
    #    digest = 고치기 전 본문의 digest" 다 (--old-scripts 면 B 묶음이 고치기 전 **함수** 와 44/44 를 따로 대조한다).
    chk(f'R10 커밋된 영수증 {len(_all)} 개 전부 — 새 함수 digest = 고치기 전 본문 digest (선택 칸 없음 = 옛 OUTDIR 이름 보존)',
        len(_all) >= 40 and all(RC.receipt_digest(r) == _base_body_digest(r) for r in _all),
        [os.path.basename(str(i)) for i, r in enumerate(_all) if RC.receipt_digest(r) != _base_body_digest(r)][:4])
    base = {k: v for k, v in _rcpts[1].items() if k != 'receipt_digest'}
    req = {'cjunc': dict(CJ_REQ)}
    chk('R10b 요청을 실은 영수증은 digest 가 다르다 (OUTDIR 이 갈린다)',
        RC.receipt_digest(dict(base, ca_ext_request=req)) != RC.receipt_digest(base)
        and RC.receipt_digest(dict(base, step3_rtol=1e-12)) != RC.receipt_digest(base))
    rec = dict(base, ca_ext_request=req)
    chk('R11a 요청 ↔ 블록 같음 → receipt_match 통과', RC.receipt_match(rec, m) == (True, None), RC.receipt_match(rec, m))
    chk('R11b 요청 R_j ≠ 블록 R_j → 거부', not RC.receipt_match(dict(base, ca_ext_request={'cjunc': dict(CJ_REQ, R_j_ohm=1e4)}), m)[0])
    chk('R11c 요청 있는데 블록 없음 → 거부', not RC.receipt_match(rec, m_nob)[0])
    chk('R11d 요청 없는 영수증 + 접합 블록 팔 → 거부 (러너가 요청 안 한 실험)', not RC.receipt_match(base, m)[0])
    chk('R11e 수정자 요청 ↔ 블록 c 대조', RC.receipt_match(dict(base, ca_ext_request={'cjunc': dict(CJ_REQ), 'sdcp_mod': {'c': 1.0}}),
                                                     cj_manifest(sdcp_c=1.0))[0]
        and not RC.receipt_match(dict(base, ca_ext_request={'cjunc': dict(CJ_REQ), 'sdcp_mod': {'c': 0.0}}),
                                 cj_manifest(sdcp_c=1.0))[0]
        and not RC.receipt_match(dict(base, ca_ext_request={'cjunc': dict(CJ_REQ)}), cj_manifest(sdcp_c=1.0))[0])
    m_rt = dict(m_nob, backend=dict(m_nob.get('backend') or {}, rtol=1e-12))
    chk('R11f rtol — 선언 ↔ 매니페스트 backend.rtol 같음 통과 · 다르면 거부 · 선언 없는데 팔에 rtol = 거부 · 선언했는데 팔에 없음 = 거부',
        RC.receipt_match(dict(base, step3_rtol=1e-12), m_rt)[0]
        and not RC.receipt_match(dict(base, step3_rtol=1e-10), m_rt)[0]
        and not RC.receipt_match(base, m_rt)[0]
        and not RC.receipt_match(dict(base, step3_rtol=1e-12), m_nob)[0])
    chk('R11g 옛 영수증 + 옛 매니페스트 = 통과 (기존 거동 그대로)', RC.receipt_match(base, m_nob)[0])
    #  ── 러너 발사 전 요청 검사 (선언 축 = 매니페스트 축) ──
    chk('R12a 요청 정상 → 문제 없음', RC.ca_ext_request_problem(req) is None
        and RC.ca_ext_request_problem({'cjunc': dict(CJ_REQ), 'sdcp_mod': {'c': 0.0}}) is None)
    for nm, r in (('모르는 하위 블록', {'cjunc': dict(CJ_REQ), 'mystery': {}}), ('수정자만', {'sdcp_mod': {'c': 1.0}}),
                  ('칸 빠짐', {'cjunc': {k: v for k, v in CJ_REQ.items() if k != 's_min_um'}}),
                  ('모르는 칸', {'cjunc': dict(CJ_REQ, R_j=1.0)}), ('R_j 음수', {'cjunc': dict(CJ_REQ, R_j_ohm=-1.0)}),
                  ('P1', {'cjunc': dict(CJ_REQ, ptfe_jlaw='P1')}), ('c = 0.5', {'cjunc': dict(CJ_REQ), 'sdcp_mod': {'c': 0.5}}),
                  ('dict 아님', ['cjunc'])):
        chk(f'R12b 요청 검사 거부 [{nm}]', RC.ca_ext_request_problem(r) is not None)
    #  ── 수렴 증서 (다음 세대 판정 해의 게시 조건 · 설계 §6) ──
    chk('R13a 증서 정상 → 문제 없음', RC.conv_cert_problem(good_cert(0.05), 0.05, m) is None,
        RC.conv_cert_problem(good_cert(0.05), 0.05, m))
    for nm, fn in (('없음', lambda c: None), ('ok False', lambda c: dict(c, ok=False)),
                   ('ok ↔ pass 모순', lambda c: dict(c, pass_b=False)),
                   ('판 rtol 1e-8 (봉인 상한 밖) 인데 pass_a', lambda c: dict(c, rtol_used=1e-8)),
                   ('불균형 문턱 밖 인데 pass_b', lambda c: dict(c, imbalance=1e-3)),
                   ('이어 풀기 Δσ 문턱 밖 인데 pass_c', lambda c: dict(c, dsigma_rel=1e-3)),
                   ('다른 판본', lambda c: dict(c, version='conv-cert-v0')), ('봉인 상한 손으로', lambda c: dict(c, rtol_max=1e-8)),
                   ('σ ≠ 결과 σ (증서 ↔ 결과 결합)', lambda c: dict(c, sigma=0.06)), ('NaN 불균형', lambda c: dict(c, imbalance=float('nan'))),
                   ('pass 가 문자열', lambda c: dict(c, pass_a='True'))):
        chk(f'R13b 증서 거부 [{nm}]', RC.conv_cert_problem(fn(good_cert(0.05)), 0.05, m) is not None)
    s3 = {'sigma_e_eff_S_cm': 0.05, 'manifest': m, 'conv_cert': good_cert(0.05)}
    chk('R13c 다음 세대 게시 조건 — p3ca + 증서 정상 = 통과 · 증서 없음 = 미게시 · p2 (옛 세대) = 해당 없음 (통과)',
        RC.next_gen_cert_ok(s3)[0] and not RC.next_gen_cert_ok({k: v for k, v in s3.items() if k != 'conv_cert'})[0]
        and RC.next_gen_cert_ok({'sigma_e_eff_S_cm': 0.05, 'manifest': cohort_manifests()[0]})[0])
    s3i = dict(s3, manifest=cj_manifest(ionic_plan=True), sigma_ion_eff_S_cm=0.001)
    s3i['manifest']['components'] = dict(s3i['manifest'].get('components') or {}, ionic={'status': 'complete'})
    chk('R13d 이온을 푼 다음 세대 팔은 이온 증서도 요구 (없으면 미게시 · 있으면 통과)',
        not RC.next_gen_cert_ok(s3i)[0] and RC.next_gen_cert_ok(dict(s3i, ion_conv_cert=good_cert(0.001, channel='ionic')))[0])
    #  ── CLI 회계 (규칙 M) ──
    acct = RC.CLI_ACCOUNTING
    _new = ('--step3-cjunc', '--step3-cjunc-rj', '--step3-cjunc-len-law', '--step3-cjunc-unreg-law',
            '--step3-cjunc-s-min-um', '--step3-cjunc-tol-ff-um', '--step3-cjunc-ptfe-jlaw', '--step3-sdcp-mod-c')
    chk('R14 새 플래그 여덟 = protocol_ext (ca_ext 칸 이름 · 정본 안)',
        all(acct.get(o, (None,))[0] == 'protocol_ext' and acct[o][1] and set(acct[o][1]) <= set(fld) for o in _new),
        [o for o in _new if acct.get(o, (None,))[0] != 'protocol_ext'])
    import check_method_discipline as CMD
    probs, _w = quiet(CMD.check_cli_accounting, verbose=False)
    chk('R15 규칙 M (실물 파서 전수) 문제 0', probs == [], probs[:3])


# ═════════════════════════ P 묶음 — payload 끝-끝 ═════════════════════════
UM_BOX = 1000.0 / ((0.96 - 0.04) / 0.05)
SW0, FLOOR = 0.04, 0.05


def _box(P_um):
    P = np.asarray(P_um, np.float64)
    return np.column_stack([SW0 + P[:, 0] / UM_BOX, SW0 + P[:, 1] / UM_BOX, FLOOR + P[:, 2] / UM_BOX])


def line(a, b, n):
    a = np.asarray(a, np.float64)
    b = np.asarray(b, np.float64)
    return a[None] + np.linspace(0.0, 1.0, n)[:, None] * (b - a)[None]


def make_fixture(d, sdcp=False, ptfe=True):
    """2×2 AM 기둥 (구 셋씩 · r 4 µm) + 조밀 SE 점 + **세로 VGCF 두 가닥이 셀 (24, 24, 12) 중심에서 끝을 맞댄다** (아래 판 ↔ 접합 ↔
    위 판 = 직렬 사슬 · 접합 instance 하나) + PTFE 선 (멀리) + (sdcp) SDCP 점 하나가 접합 옆 셀 (근접 0.55 µm)."""
    rows = ['# type,x,y,z,r  (B6 cjunc 시험 픽스처)']
    for ix in range(2):
        for iy in range(2):
            for k in range(3):
                rows.append('2,%.6f,%.6f,%.6f,%.6f' % (0.020 + 0.008 * ix, 0.020 + 0.008 * iy, 0.004 + 0.0075 * k, 0.004))
    with open(os.path.join(d, 'am.csv'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rows) + '\n')
    g = np.arange(12.0, 36.01, 0.75)
    gz = np.arange(0.3, 23.2, 0.75)
    se = np.array([[x, y, z] for x in g for y in g for z in gz], np.float64)
    blocks = [(_box(se), 1, -1, 0)]
    blocks.append((_box(line((24.5, 24.5, 0.3), (24.5, 24.5, 12.5), 41)), 2, 0, 1))      # V1 (아래 판 → 접합)
    blocks.append((_box(line((24.5, 24.5, 12.5), (24.5, 24.5, 23.2), 37)), 2, 1, 1))     # V2 (접합 → 위 판)
    if ptfe:
        blocks.append((_box(line((12.5, 16.5, 7.5), (36.5, 16.5, 7.5), 97)), 4, 2, 1))
    if sdcp:
        blocks.append((_box(np.array([[24.5, 25.05, 12.5]])), 5, -1, 0))
    pts = np.vstack([b[0] for b in blocks])
    ph = np.concatenate([np.full(len(b[0]), b[1], np.int32) for b in blocks])
    fid = np.concatenate([np.full(len(b[0]), b[2], np.int32) for b in blocks])
    kind = np.concatenate([np.full(len(b[0]), b[3], np.int8) for b in blocks])
    np.save(os.path.join(d, 'se.npy'), pts)
    np.save(os.path.join(d, 'phase.npy'), ph)
    np.save(os.path.join(d, 'fibre.npy'), fid)
    np.save(os.path.join(d, 'fibre_kind.npy'), kind)
    np.save(os.path.join(d, 'fibre_dia.npy'), np.ones(len(pts)))
    return d


LEAN2 = ['--no-step4', '--no-thermal', '--no-trackb', '--no-field', '--no-ion', '--no-pore', '--no-collector']
LEAN3 = [x for x in LEAN2 if x != '--no-ion']
CJ = ['--step3-cjunc', '--step3-cjunc-rj', '1e6', '--step3-cjunc-len-law', 'len_scaled_v0', '--step3-cjunc-unreg-law', 'cut',
      '--step3-cjunc-s-min-um', '0.5', '--step3-cjunc-tol-ff-um', '0.5', '--step3-cjunc-ptfe-jlaw', 'P0']
OFF = ['--ptfe-stamp', 'off']


def cj_with(**repl):
    """CJ 인자에서 값만 바꾼다 (키 = 플래그 이름 꼬리 · 값 None = 그 플래그를 뺀다)."""
    out, i = [], 0
    while i < len(CJ):
        f = CJ[i]
        key = f[len('--step3-cjunc-'):].replace('-', '_') if f.startswith('--step3-cjunc-') else None
        if key is not None and key in repl:
            if repl[key] is not None:
                out += [f, str(repl[key])]
            i += 2
            continue
        out.append(f)
        if key is not None:
            out.append(CJ[i + 1])
            i += 2
        else:
            i += 1
    return out


def run_payload(d, extra, out='p.json', payload=None, drop=()):
    pay = payload or os.path.join(SCRIPTS, 'mpm_webapp_payload.py')
    base = ['--scaffold', 'am.csv', '--se', 'se.npy', '--phase', 'phase.npy', '--fibre', 'fibre.npy',
            '--fibre-dia', 'fibre_dia.npy', '--n-vox', '24', '--step3-vox', '1.0', '--step3-fibre-stamp', 'segment']
    for fl in drop:
        i = base.index(fl)
        del base[i:i + 2]
    cmd = [sys.executable, pay, *base, '--out', out, '--show-results', *extra]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900, cwd=d, stdin=subprocess.DEVNULL)
    log = (r.stdout or '') + (r.stderr or '')
    data = None
    if os.path.exists(os.path.join(d, out)):
        try:
            data = json.load(open(os.path.join(d, out), encoding='utf-8'))
        except Exception:                                  # noqa: BLE001
            data = None
    return r.returncode, log, data


def s3_of(data):
    return ((data or {}).get('mpm_metrics') or {}).get('step3') or {}


def man_of(data):
    return s3_of(data).get('manifest') or {}


def cj_block(data):
    return ((man_of(data).get('ca_ext') or {}).get('cjunc') or {})


@case('P payload 끝-끝 — 접합 · 수정자 · 입구 거부 · 매니페스트 · 영수증 · 조합 정책 · --expect-physics ca_ext 칸')
def t_payload():
    if ARGS.skip_payload:
        print('    (--skip-payload — 건너뜀)')
        return
    td = tempfile.mkdtemp(prefix='b6_')
    try:
        os.makedirs(os.path.join(td, 'sbe'))
        os.makedirs(os.path.join(td, 'dbe'))
        d = make_fixture(os.path.join(td, 'sbe'), sdcp=False)
        dd = make_fixture(os.path.join(td, 'dbe'), sdcp=True)
        #  ── 입구 거부 (구조화 사유 · GPU 전) ──
        refuse = {
            'MISSING (R_j 없음)': (OFF + LEAN2 + cj_with(rj=None), 'MISSING'),
            'MISSING (길이 법칙 없음)': (OFF + LEAN2 + cj_with(len_law=None), 'MISSING'),
            'MISSING (미등록 면 법칙 없음)': (OFF + LEAN2 + cj_with(unreg_law=None), 'MISSING'),
            'MISSING (s_min 없음 · 정량이면 거부)': (OFF + LEAN2 + cj_with(s_min_um=None), 'MISSING'),
            'MISSING (tol_ff 없음 · 기본값 없음)': (OFF + LEAN2 + cj_with(tol_ff_um=None), 'MISSING'),
            'MISSING (PTFE–접합 법칙 없음)': (OFF + LEAN2 + cj_with(ptfe_jlaw=None), 'MISSING'),
            'FLAG_WITHOUT_CJUNC (R_j 만)': (OFF + LEAN2 + ['--step3-cjunc-rj', '1e6'], 'FLAG_WITHOUT_CJUNC'),
            #  ★ Z3 (10-20) — 'FACE_ALPHA_COMBO (face_alpha + 접합)' 거부는 뺐다 (설계 조합 규칙 · 양성 = 아래 P15c)
            'P1_NEEDS_FACE_ALPHA': (OFF + LEAN2 + cj_with(ptfe_jlaw='P1'), 'P1_NEEDS_FACE_ALPHA'),
            'P1_NEEDS_FACE_ALPHA (centerline)': (['--ptfe-stamp', 'centerline'] + LEAN2 + cj_with(ptfe_jlaw='P1'), 'P1_NEEDS_FACE_ALPHA'),
            #  ★ 10-21 (D · 사전 리뷰 PRE-impl-03 ① · 코디네이터 Q-C) — centerline + 접합 = 거부 (P0 도 · 덮인 접점 셀의 포트 옮김이
            #    Rayleigh 를 깬다 · 접합 모듈 쪽 거부 = A · 입구 거부 = 여기 · 러너 = test_ca_ext_runner N6 · MIRROR)
            'PTFE_CENTERLINE (P0)': (['--ptfe-stamp', 'centerline'] + LEAN2 + CJ, 'PTFE_CENTERLINE'),
            'PTFE_CENTERLINE (P1)': (['--ptfe-stamp', 'centerline'] + LEAN2 + cj_with(ptfe_jlaw='P1'), 'PTFE_CENTERLINE'),
            'PERIODIC': (OFF + LEAN2 + CJ + ['--periodic'], 'PERIODIC'),
            'JOULE': (OFF + LEAN2 + CJ + ['--joule-heat'], 'JOULE'),
            'STEP4_GRID': (OFF + LEAN2 + CJ + ['--save-step4-grid', 'g.npz'], 'STEP4_GRID'),
            'RINT': (OFF + LEAN2 + CJ + ['--step3-rint-e', 'AM_S|VGCF=1e-3'], 'RINT'),
            'NO_STEP3': (OFF + LEAN2 + CJ + ['--no-step3'], 'NO_STEP3'),
            'SDCP_BRIDGE (진단 팔)': (OFF + LEAN2 + CJ + ['--step3-sdcp-bridge', '0.3'], 'SDCP_BRIDGE'),
            'VGCF_INSULATING (σ 0)': (OFF + LEAN2 + CJ + ['--sigma-vgcf', '0'], 'VGCF_INSULATING'),
            'FIELD (LEAN 4)': (OFF + [x for x in LEAN2 if x != '--no-field'] + CJ, 'FIELD'),
            'COLLECTOR': (OFF + [x for x in LEAN2 if x != '--no-collector'] + CJ, 'COLLECTOR'),
            'THERMAL': (OFF + [x for x in LEAN2 if x != '--no-thermal'] + CJ, 'THERMAL'),
            'PORE': (OFF + [x for x in LEAN2 if x != '--no-pore'] + CJ, 'PORE'),
            'STEP4': (OFF + [x for x in LEAN2 if x != '--no-step4'] + CJ, 'STEP4'),
            'TRACKB': (OFF + [x for x in LEAN2 if x != '--no-trackb'] + CJ, 'TRACKB'),
            'VALUE (R_j 0)': (OFF + LEAN2 + cj_with(rj='0'), 'VALUE'),
            'VALUE (R_j nan)': (OFF + LEAN2 + cj_with(rj='nan'), 'VALUE'),
            'VALUE (R_j inf)': (OFF + LEAN2 + cj_with(rj='inf'), 'VALUE'),
            'VALUE (s_min 음수)': (OFF + LEAN2 + cj_with(s_min_um='-0.1'), 'VALUE'),
            'VALUE (tol_ff 음수)': (OFF + LEAN2 + cj_with(tol_ff_um='-0.1'), 'VALUE'),
        }
        for i_r, (nm, (extra, code)) in enumerate(refuse.items()):
            rc, log, _d = run_payload(d, extra, out=f'refuse_{i_r}.json')
            chk(f'P-거부 [{nm}] → rc ≠ 0 · S2_CJUNC_REFUSED|{code}|', rc != 0 and f'S2_CJUNC_REFUSED|{code}|' in log,
                (rc, log.strip()[-200:]))
        for nm, drop, code in (('NO_PHASE', ('--phase',), 'NO_PHASE'), ('NO_FIBRE', ('--fibre',), 'NO_FIBRE')):
            ex = OFF + LEAN2 + CJ + (['--step3-fibre-stamp', 'point'] if nm == 'NO_FIBRE' else [])
            rc, log, _d = run_payload(d, ex, out=f'refuse_{nm}.json', drop=drop)
            chk(f'P-거부 [{nm}] → S2_CJUNC_REFUSED|{code}|', rc != 0 and f'S2_CJUNC_REFUSED|{code}|' in log, (rc, log.strip()[-200:]))
        rc, log, _d = run_payload(d, OFF + LEAN2 + CJ + ['--step3-fibre-stamp', 'point'], out='refuse_seg.json')
        chk('P-거부 [SEGMENT (점 스탬프)] → S2_CJUNC_REFUSED|SEGMENT|', rc != 0 and 'S2_CJUNC_REFUSED|SEGMENT|' in log,
            (rc, log.strip()[-200:]))
        rc, log, _d = run_payload(d, OFF + LEAN2 + ['--step3-sdcp-mod-c', '1'], out='refuse_sd.json')
        chk('P-거부 [S3 수정자만 (S2 없이)] → S3_SDCP_MOD_REFUSED|NO_CJUNC|', rc != 0 and 'S3_SDCP_MOD_REFUSED|NO_CJUNC|' in log,
            (rc, log.strip()[-200:]))
        rc, log, _d = run_payload(d, OFF + LEAN2 + CJ + ['--step3-sdcp-mod-c', '0.5'], out='refuse_sd2.json')
        chk('P-거부 [c = 0.5 (정량은 0 · 1)] → rc ≠ 0', rc != 0, (rc, log.strip()[-160:]))
        #  ── 정상 — 접합 LEAN 2 (SBE 꼴 · SDCP 없음) ──
        rc_o, log_o, p_off = run_payload(d, OFF + LEAN2, out='off.json')
        rc_c, log_c, p_cj = run_payload(d, OFF + LEAN2 + CJ, out='cj.json')
        m = man_of(p_cj)
        blk = cj_block(p_cj)
        ev = blk.get('evidence') or {}
        rcp = ev.get('receipts') or {}
        chk('P1 접합 LEAN 2 — rc 0', rc_c == 0, log_c.strip()[-500:])
        chk('P2 매니페스트 — 요청 칸 [cjunc] · 블록 · p3ca id · protocol_ok · ca_ext_record_ok',
            m.get('ca_ext_requested') == ['cjunc'] and (m.get('ca_ext') or {}).get('schema') == RC.CA_EXT_SCHEMA
            and str(m.get('physics_protocol_id', '')).startswith('p3ca-') and RC.protocol_ok(m) == (True, None)
            and RC.ca_ext_record_ok(m) == (True, None), (m.get('physics_protocol_id'), RC.ca_ext_record_ok(m) if m else None))
        pr = blk.get('protocol') or {}
        chk('P3 protocol = CLI 값 (R_j 1e6 · len_scaled_v0 · cut · s_min 0.5 · tol_ff 0.5 · P0 · ptfe off)',
            pr.get('R_j_ohm') == 1e6 and pr.get('len_law') == 'len_scaled_v0' and pr.get('unreg_law') == 'cut'
            and pr.get('s_min_um') == 0.5 and pr.get('tol_ff_um') == 0.5 and pr.get('ptfe_jlaw') == 'P0'
            and pr.get('ptfe_stamp') == 'off', pr)
        chk('P4 영수증 (LEAN 2 표) — 주 applied · wetted/bare disabled · 이온 disabled',
            (rcp.get('electronic_main') or {}).get('status') == 'applied'
            and (rcp.get('electronic_wetted') or {}).get('status') == 'disabled'
            and (rcp.get('electronic_bare') or {}).get('status') == 'disabled'
            and (rcp.get('ionic') or {}).get('status') == 'disabled', rcp)
        cnt = ev.get('counts') or {}
        chk('P5 원장 — instance 1 · 간선 1 · 축약 0 · 풀림 · 접합 간선 1', cnt.get('n_instances') == 1 and cnt.get('n_edge') == 1
            and cnt.get('n_contract') == 0 and (ev.get('solve') or {}).get('solved') is True
            and (ev.get('solve') or {}).get('n_junction_edges') == 1, (cnt, ev.get('solve')))
        sc = s3_of(p_cj)
        chk('P6 진단 미계산 (E2 · v0) — 소산 분담 None · je 없음 · 진단 표', sc.get('dissipation_share') is None
            and all('je' not in q for q in (p_cj or {}).get('particles', [{}]))
            and (ev.get('diagnostics') or {}).get('je') == 'not_computed', ev.get('diagnostics'))
        chk('P7 check_arm (sr01) 이 실제 산출물을 받는다', subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, 'sr01_stamp_compare.py'), '--check-arm', os.path.join(d, 'cj.json'),
             '--stamp', 'segment'], capture_output=True, text=True, timeout=300, cwd=d).returncode == 0)
        #  ── 물리 상식 — 같은 침대 · R_j 사다리 (Rayleigh) ──
        _r2, _l2, p_lo = run_payload(d, OFF + LEAN2 + cj_with(rj='1e2'), out='cj_rj1e2.json')
        _r8, _l8, p_hi = run_payload(d, OFF + LEAN2 + cj_with(rj='1e8'), out='cj_rj1e8.json')
        s_off, s_lo, s_mid, s_hi = (s3_of(p).get('sigma_e_eff_S_cm') or 0.0 for p in (p_off, p_lo, p_cj, p_hi))
        chk('P8 σ_e 순서 — off (융합 = R_j → 0 극한) ≥ R_j 1e2 > 1e6 > 1e8 > 0 (직렬 사슬 · 같은 그래프)',
            rc_o == 0 and _r2 == 0 and _r8 == 0 and s_off >= s_lo * (1 - 1e-9) and s_lo > s_mid > s_hi > 0,
            (s_off, s_lo, s_mid, s_hi))
        chk('P9 R_j 가 다르면 p3ca id 가 다르다 · 같은 R_j 의 두 침대 (SDCP 유무) 는 같은 id',
            man_of(p_lo).get('physics_protocol_id') != m.get('physics_protocol_id'), man_of(p_lo).get('physics_protocol_id'))
        #  ── 수정자 (S3) — DBE 꼴 (SDCP 점 하나가 접합 옆) ──
        _rd, _ld, q_cj = run_payload(dd, OFF + LEAN2 + CJ, out='cj.json')
        _r0, _l0, q_c0 = run_payload(dd, OFF + LEAN2 + CJ + ['--step3-sdcp-mod-c', '0'], out='c0.json')
        _r1, _l1, q_c1 = run_payload(dd, OFF + LEAN2 + CJ + ['--step3-sdcp-mod-c', '1'], out='c1.json')
        _rs0, _ls0, p_c1sbe = run_payload(d, OFF + LEAN2 + CJ + ['--step3-sdcp-mod-c', '1'], out='c1_sbe.json')
        chk('P9b 같은 R_j · 같은 설정의 두 침대 (SDCP 유무) = 같은 p3ca id', _rd == 0
            and man_of(q_cj).get('physics_protocol_id') == m.get('physics_protocol_id'),
            (man_of(q_cj).get('physics_protocol_id'), m.get('physics_protocol_id')))
        sd1 = ((man_of(q_c1).get('ca_ext') or {}).get('sdcp_mod') or {})
        cnt1 = (cj_block(q_c1).get('evidence') or {}).get('counts') or {}
        chk('P10 c = 1 — 요청 칸 [cjunc, sdcp_mod] · 블록 둘 · ca_ext_record_ok · 근접 1 · 축약 1',
            _r1 == 0 and man_of(q_c1).get('ca_ext_requested') == ['cjunc', 'sdcp_mod'] and sd1.get('protocol', {}).get('c') == 1.0
            and RC.ca_ext_record_ok(man_of(q_c1)) == (True, None) and cnt1.get('n_sdcp_near') == 1
            and cnt1.get('n_contract') == 1 and (sd1.get('evidence') or {}).get('n_contracted_by_c') == 1,
            (_r1, _l1.strip()[-300:], cnt1))
        sg0, sg1, sgj = (s3_of(q).get('sigma_e_eff_S_cm') or 0.0 for q in (q_c0, q_c1, q_cj))
        chk('P11 c = 0 = 수정자 없는 접합과 σ 비트 같음 · c = 1 ≥ c = 0 (Rayleigh · 같은 그래프)',
            _r0 == 0 and sg0 == sgj and sg1 >= sg0 * (1 - 1e-12) and sg1 > 0, (sg0, sg1, sgj))
        chk('P12 SBE (SDCP 없음) + c = 1 = 근접 0 · σ 가 수정자 없는 접합과 비트 같음 · 판별 표지 False',
            _rs0 == 0 and s3_of(p_c1sbe).get('sigma_e_eff_S_cm') == s_mid
            and ((man_of(p_c1sbe).get('ca_ext') or {}).get('sdcp_mod') or {}).get('evidence', {}).get('s3_discriminating') is False,
            (s3_of(p_c1sbe).get('sigma_e_eff_S_cm'), s_mid))
        #  ── LEAN 3 — 이온 솔브는 접합과 무관 (요청 = 전자뿐) ──
        _ra, _la, l3_off = run_payload(d, OFF + LEAN3, out='l3_off.json')
        _rb, _lb, l3_cj = run_payload(d, OFF + LEAN3 + CJ, out='l3_cj.json')
        r3 = (cj_block(l3_cj).get('evidence') or {}).get('receipts') or {}
        chk('P13 LEAN 3 — 이온 영수증 not_requested · σ_ion = off 비트 같음 · ca_ext_record_ok',
            _rb == 0 and (r3.get('ionic') or {}).get('status') == 'not_requested'
            and s3_of(l3_cj).get('sigma_ion_eff_S_cm') == s3_of(l3_off).get('sigma_ion_eff_S_cm')
            and RC.ca_ext_record_ok(man_of(l3_cj)) == (True, None), (_rb, _lb.strip()[-300:]))
        #  ── 조합 정책 (다음 세대 판정 꼴 = 허용 · ★ Z3 face_alpha + 접합 = 허용 — 옛 임시 거부 뺌) ──
        rc_fr, log_fr, p_fr = run_payload(d, ['--ptfe-stamp', 'face_alpha', '--step3-rtol', '1e-12'] + LEAN2, out='fa_rtol.json')
        mfr = man_of(p_fr)
        cert = s3_of(p_fr).get('conv_cert') or {}
        chk('P14 face_alpha + --step3-rtol 1e-12 = 허용 — rc 0 · ptfe_face 블록 · p3ca · 증서 ok · backend.rtol 기록 · ca_ext_record_ok',
            rc_fr == 0 and 'ptfe_face' in (mfr.get('ca_ext') or {}) and str(mfr.get('physics_protocol_id', '')).startswith('p3ca-')
            and cert.get('ok') is True and (mfr.get('backend') or {}).get('rtol') == 1e-12
            and RC.ca_ext_record_ok(mfr) == (True, None) and RC.conv_cert_problem(cert, s3_of(p_fr).get('sigma_e_eff_S_cm'), mfr) is None,
            (rc_fr, log_fr.strip()[-300:], cert.get('ok')))
        chk('P14b face_alpha + rtol 팔 = 다음 세대 게시 조건 통과 · rtol 없는 face_alpha 팔 = 미게시 (증서 칸 없음)',
            RC.next_gen_cert_ok(s3_of(p_fr))[0]
            and not RC.next_gen_cert_ok(s3_of(run_payload(d, ['--ptfe-stamp', 'face_alpha'] + LEAN2, out='fa.json')[2]))[0])
        rc_cr, log_cr, p_cr = run_payload(d, OFF + LEAN2 + CJ + ['--step3-rtol', '1e-12'], out='cj_rtol.json')
        mcr = man_of(p_cr)
        cert2 = s3_of(p_cr).get('conv_cert') or {}
        chk('P15 접합 + --step3-rtol 1e-12 = 허용 — rc 0 · cjunc 블록 · p3ca · 증서 ok (σ 결합) · backend.rtol · 게시 조건 통과',
            rc_cr == 0 and 'cjunc' in (mcr.get('ca_ext') or {}) and str(mcr.get('physics_protocol_id', '')).startswith('p3ca-')
            and cert2.get('ok') is True and (mcr.get('backend') or {}).get('rtol') == 1e-12
            and RC.conv_cert_problem(cert2, s3_of(p_cr).get('sigma_e_eff_S_cm'), mcr) is None and RC.next_gen_cert_ok(s3_of(p_cr))[0],
            (rc_cr, log_cr.strip()[-300:], cert2.get('ok')))
        chk('P15b rtol 은 규약 id 밖 (numeric) — 접합 + rtol 의 p3ca id = 접합만의 id',
            mcr.get('physics_protocol_id') == m.get('physics_protocol_id'), (mcr.get('physics_protocol_id'), m.get('physics_protocol_id')))
        rc_fc, log_fc, p_fc = run_payload(d, ['--ptfe-stamp', 'face_alpha'] + LEAN2 + CJ + ['--step3-rtol', '1e-12'], out='fa_cj_rtol.json')
        mfc = man_of(p_fc)
        chk('P15c ★ Z3 face_alpha + 접합 + rtol = 허용 (옛 FACE_ALPHA_COMBO 거부 뺌) — rc 0 · 하위 블록 ptfe_face + cjunc · 요청 칸 [cjunc] · '
            'p3ca · ca_ext_record_ok · 게시 조건 · 접합 protocol 의 ptfe_stamp = face_alpha',
            rc_fc == 0 and sorted(mfc.get('ca_ext') or {}) == ['cjunc', 'ptfe_face', 'schema'] and mfc.get('ca_ext_requested') == ['cjunc']
            and str(mfc.get('physics_protocol_id', '')).startswith('p3ca-') and RC.ca_ext_record_ok(mfc) == (True, None)
            and RC.next_gen_cert_ok(s3_of(p_fc))[0] and (cj_block(p_fc).get('protocol') or {}).get('ptfe_stamp') == 'face_alpha',
            (rc_fc, log_fc.strip()[-300:], RC.ca_ext_record_ok(mfc) if mfc else None))
        #  ── --expect-physics 의 ca_ext 칸 (러너 선언 = 매니페스트 축) ──
        XPB = ('vox_um=1.0,bridge_um=1.2,sigma_vgcf_S_cm=100.0,fibre_stamp=segment,sdcp_stamp=point,sdcp_yield_to_vgcf=False,'
               'periodic_xy=False,ptfe_stamp=off,sigma_ptfe_S_cm=0')
        XCJ = (',ca_ext.cjunc.R_j_ohm=1e6,ca_ext.cjunc.len_law=len_scaled_v0,ca_ext.cjunc.unreg_law=cut,'
               'ca_ext.cjunc.s_min_um=0.5,ca_ext.cjunc.tol_ff_um=0.5,ca_ext.cjunc.ptfe_jlaw=P0')
        rc_x1, log_x1, _p = run_payload(d, OFF + LEAN2 + CJ + ['--expect-physics', XPB + XCJ], out='x1.json')
        chk('P16 선언 = 적용 (ca_ext 칸 포함) → rc 0', rc_x1 == 0, log_x1.strip()[-300:])
        rc_x2, log_x2, _p = run_payload(d, OFF + LEAN2 + CJ + ['--expect-physics', XPB + XCJ.replace('R_j_ohm=1e6', 'R_j_ohm=1e7')],
                                        out='x2.json')
        chk('P17 선언 R_j ≠ 적용 → exit 4 · PROTOCOL_MISMATCH (ca_ext.cjunc.R_j_ohm)', rc_x2 == 4 and 'PROTOCOL_MISMATCH' in log_x2
            and 'ca_ext.cjunc.R_j_ohm' in log_x2, (rc_x2, log_x2.strip()[-300:]))
        rc_x3, log_x3, _p = run_payload(d, OFF + LEAN2 + CJ + ['--expect-physics', XPB + XCJ.replace(',ca_ext.cjunc.s_min_um=0.5', '')],
                                        out='x3.json')
        chk('P18 접합을 켰는데 선언에 s_min 칸이 없다 → 거부 (선언 안 한 축은 검사도 안 된다 · PASL-04 꼴)',
            rc_x3 != 0 and 'CA_EXT_EXPECT|INCOMPLETE|' in log_x3 and 'ca_ext.cjunc.s_min_um' in log_x3, (rc_x3, log_x3.strip()[-300:]))
        rc_x4, log_x4, _p = run_payload(d, OFF + LEAN2 + ['--expect-physics', XPB + XCJ], out='x4.json')
        chk('P19 접합을 안 켰는데 ca_ext.cjunc 칸을 선언 → 거부 (요청 없는 선언)', rc_x4 != 0 and 'CA_EXT_EXPECT|UNREQUESTED|' in log_x4,
            (rc_x4, log_x4.strip()[-300:]))
        rc_x5, log_x5, _p = run_payload(d, OFF + LEAN2 + CJ + ['--expect-physics', XPB + XCJ + ',ca_ext.cjunc.no_such=1'], out='x5.json')
        chk('P20 모르는 ca_ext 칸 선언 → 거부 (정본 밖)', rc_x5 != 0 and 'ca_ext.cjunc.no_such' in log_x5, (rc_x5, log_x5.strip()[-200:]))
        rc_t = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'mpm_webapp_payload.py'), '--selftest-temperature'],
                              capture_output=True, text=True, timeout=300, cwd=td)
        chk('P21 payload --selftest-temperature rc 0', rc_t.returncode == 0, ((rc_t.stdout or '') + (rc_t.stderr or '')).strip()[-300:])
        print(f'    보고 P (픽스처 · vox 1.0) σ_e off {s_off!r} · 접합 R_j 1e2 {s_lo!r} · 1e6 {s_mid!r} · 1e8 {s_hi!r} · '
              f'DBE c0 {sg0!r} · c1 {sg1!r}')
    finally:
        shutil.rmtree(td, ignore_errors=True)


# ═════════════════════════ S 묶음 — 해 상태 (영값 · 단락) · SV 반사실 노브 배선 (★ 10-21 D · 시험 먼저) ═════════════════════════
#  정본 = 등록 R §5-0 (상태 먼저 · zero · short = 확장 실수 끝 · 유한 σ 로 위장하지 않는다) · §5-6 SV 행 (반사실 대조 · 같은 침대 · 같은 R_j ·
#  단자 G 비) · 설계 §4-5 · §6 (상태 분리) · Codex RCA-06 · RCA-13 · 1저자 Q4 · Q7 권고대로.
def _early_cert(reason, zero_graph='cjunc_assembled', fp=None):
    """조기 반환 해의 상태 증서 (정본 `step3_conv_cert.early_record`) — ★ 10-21 (PRE-impl-07 병합) 결합 칸 = 그 런 매니페스트의 접합 지문
    (`fp` · 기본 `CJ_FP` · 솔버 `_cert_bind_kw` 꼴: 격자 = 접합 원장 sid · 접합 원장 · 계획 행 · face_alpha 없음)."""
    import step3_conv_cert as CC
    fp = CJ_FP if fp is None else fp
    return CC.early_record({'sigma_eff': 0.0, 'n_dof': 4, 'reason': reason}, zero_graph=zero_graph, fp_sid=fp['sid'], fp_sig='d' * 32,
                           fp_cjunc_registry=fp['registry'], fp_cjunc_rows=fp['plan_rows'])


def state_manifest(kind, n_inst=3):
    """주 솔브가 조기 반환한 다음 세대 매니페스트 — kind 'zero' = 바닥 (R_j → ∞ · 관통 없음) · 'short' = 천장 (R_j → 0 · J11 단락).
    블록은 모듈의 기록 함수로 만든다 (사본 없음) · 주 영수증 = failed (사유) · 전자 component = not_solvable (payload `_s3mark` 꼴)."""
    m = deep(cohort_manifests()[0])
    m.update(field_requested=False, ptfe_stamp='off', ptfe_stamp_requested='off', ptfe_zero_dof=False, ptfe_cells_observed=0,
             component_plan={'electronic': True, 'ionic': False, 'thermal': False, 'pore': False, 'collector': False})
    short = kind == 'short'
    reason = 'cjunc_electrode_short' if short else 'no_through_component'
    prot = CW.cjunc_protocol_record(ptfe_stamp='off', rj_limit=('zero' if short else 'inf'),
                                    **dict(CJ_REQ, R_j_ohm=(0.0 if short else None)))
    counts = {'n_instances': n_inst, 'n_edge': 0, 'n_contract': (n_inst if short else 0), 'n_cut_p1': 0, 'n_unrealized': 0,
              'n_none_inf': (0 if short else n_inst), 'n_long': 0, 'n_sdcp_near': 0, 'n_contracted_by_c': 0, 'n_ptfe_cov': 0,
              'len_mult_sum_edge': 0.0, 'len_mult_max': 1.0}
    fp = dict(CJ_FP)                                          # ★ 10-21 (PRE-impl-07 병합) — 증서 결합 칸과 같은 지문
    solve = {'solved': False, 'reason': reason, 'short': short, 'n_contracted': counts['n_contract'], 'n_junction_edges': 0}
    rc = {'electronic_main': {'status': 'failed', 'why': reason, 'n_instances': n_inst, 'n_junction_edges': 0, 'solved': False,
                              'fp_registry': fp['registry']},
          'electronic_wetted': {'status': 'disabled', 'why': '--no-collector'},
          'electronic_bare': {'status': 'disabled', 'why': '--no-collector'},
          'ionic': {'status': 'disabled', 'why': '--no-ion'}}
    ev = CW.cjunc_evidence_record(counts=counts, census={'n_instances': n_inst}, solve=solve, receipts=rc, fp=fp, sdcp_mod_c=None)
    m['ca_ext_requested'] = ['cjunc']
    m['ca_ext'] = {'schema': RC.CA_EXT_SCHEMA, 'cjunc': {'protocol': prot, 'evidence': ev}}
    m['components'] = dict(m.get('components') or {}, electronic={'status': 'not_solvable', 'reason': reason})
    m['backend'] = {}
    m['backend_last_solve'] = {}
    m['physics_protocol_id'] = RC.physics_protocol_id(m)
    s3 = {'sigma_e_eff_S_cm': (None if short else 0.0), 'reason': reason, 'vox_um': m.get('vox_um'), 'manifest': m,
          'conv_cert': _early_cert(reason, fp=fp)}
    return s3


def _sv_ratio_of(status, ratio):
    return ratio if status == 'computed' else (float('inf') if status == 'no_through_without_sv' else None)


#: ★ 10-23 — 합성 반사실 기록의 주 해 단자 전류 (G_full · 증거 솔브 기록 `I_bot_code` 와 같은 값)
SV_GF = 2.5
#: ★ 10-23 (사전 공격 리뷰 C1 · 1저자 Q12 (가)) 합성 기록의 증서 위상 수 (간선 · dof · 아래 · 위 판 결합 — `step3_conv_cert.target_bracket` 칸) —
#   생산자 관계 그대로: 아래 끝 = 주 해 − 끊은 다리 면 4 (`_sv_raw` n_sv_faces_cut · 판 결합 수 같다) · 위 끝 = 아래 끝 − 덩어리 셀 간선 6 (n_edges_cut ·
#   판 결합 0 뺌) · dof 는 떠 있는 성분을 버린 만큼 준다
SV_TOPO_MAIN = (40, 30, 3, 2)
SV_TOPO_LO = (36, 30, 3, 2)
SV_TOPO_UP = (30, 27, 3, 2)


def _topo_kw(topo):
    return {} if topo is None else dict(zip(('target_n_edges', 'target_n_dof', 'target_n_plate_bot', 'target_n_plate_top'), topo))


def _fake_pos_cert(G, lo=None, hi=None, topo=None, **over):
    """반사실 · 주 해의 양의 해 증서 꼴 (★ 10-23 · Codex 재검토 RCA2-01 · 04 — `ca_ext_svcf.CERT_PROJ_KEYS` 칸: 게시 판 전류 = 그 끝 G · 목표량 구간
    [G, G] 기본 · 봉인 · 결합 칸 = `cj_manifest` 의 지문 · ★ 10-23 (C1) topo = 증서 위상 수 넷 (없으면 칸 없음))."""
    import step3_conv_cert as CC
    c = {'version': CC.CERT_VERSION, 'status': CC.STATUS_POSITIVE, 'ok': True, 'pass_a': True, 'pass_b': True, 'pass_c': True,
         'pass_d': True, 'I_bot': float(G), 'target_lo': float(G if lo is None else lo), 'target_hi': float(G if hi is None else hi),
         'target_version': CC.TARGET_VERSION, 'target_fp': CC.TARGET_FP_RULE, 'target_tol': CC.CERT_TARGET_TOL,
         'bind_version': CC.BIND_VERSION, 'fp_sid': CJ_FP['sid'], 'fp_sig': 'd' * 32, 'fp_face_plan': None,
         'fp_cjunc_registry': CJ_FP['registry'], 'fp_cjunc_rows': CJ_FP['plan_rows']}
    c.update(_topo_kw(topo))
    c.update(over)
    return c


def _fake_zero_cert(**over):
    """+∞ 끝의 영값 위상 증서 (정본 `step3_conv_cert.early_record` · 결합 칸 = `cj_manifest` 의 지문)."""
    import step3_conv_cert as CC
    c = CC.early_record({'reason': 'no_through_component', 'n_through_dof': 0, 'sigma_eff': 0.0}, zero_graph='cjunc_sv_counterfactual',
                        fp_sid=CJ_FP['sid'], fp_sig='d' * 32, fp_face_plan=None, fp_cjunc_registry=CJ_FP['registry'],
                        fp_cjunc_rows=CJ_FP['plan_rows'])
    c.update(over)
    return c


def _sv_raw(status='computed', ratio=1.25, threshold=None, flag=None, n_unsplit=0, status_hi=None, ratio_hi=None, certs=True):
    """carbon_junction.CjuncSolver.sv_counterfactual 의 기록 꼴 (A · 10-21) — 투영 전 원 기록.  ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 ·
    1저자 Q1 (다)) 괄호 칸 — 못 가른 덩어리 수 (`n_unsplit_bridging_components`) · 위 끝 (`status_hi` · `sv_counterfactual_ratio_hi`) · 위 끝 풀이
    기록 (`upper` · 덩어리 0 = None · 위 = 아래) · 괄호 규칙.
    ★ 10-23 (Codex 재검토 RCA2-01 · 04 · 1저자 Q1 (가)) 기본 = 증서 구간 기록 — 지위 `certified_interval` · 주 해 증서 (G_full 2.5 · 구간 [2.5, 2.5]) ·
    끝마다 증서 (computed = 양의 해 · 게시 판 전류 = G_cut · 관통 없음 = 영값 위상) · 등록 괄호 규칙 (생산자 상수) · 위 끝 제거 수 (성분 = 못 가른
    덩어리 수 · 셀 ≥ 성분) · certs False = 증서 없는 런의 진단 기록."""
    import carbon_junction as _cj

    def _gc(st, r_):
        return SV_GF / r_ if st == 'computed' else (0.0 if st == 'no_through_without_sv' else None)

    def _cc(st, gc, topo):
        if not certs:
            return None
        return _fake_pos_cert(gc, topo=topo) if st == 'computed' else (_fake_zero_cert() if st == 'no_through_without_sv' else None)
    gl = _gc(status, ratio)
    #  ★ 10-23 (사전 공격 리뷰 C5 · 1저자 Q14 (가)) 종류 · 규칙 = 등록된 생산자 이름 (옛 고정물 = 철회된 'counterfactual_cut_sv_faces' = SV 면 전부 ·
    #    다른 양) — 검증기가 이름을 대조한다
    r = {'kind': _cj.CJUNC_SV_CF_KIND, 'rule': _cj.CJUNC_SV_CF_RULE, 'requested': True, 'threshold': threshold, 'n_sv_faces_cut': 4,
         'G_full_code': SV_GF,
         'G_cut_code': gl, 'sv_counterfactual_ratio': _sv_ratio_of(status, ratio),
         'flag': flag, 'cg_info': (0 if status in ('computed', 'unconverged') else None), 'resid': (1e-13 if status == 'computed' else None),
         'conv_cert': _cc(status, gl, SV_TOPO_LO), 'status': status,
         'backend_last_solve': ({'used': 'gpu', 'requested': 'gpu'} if status == 'computed' else None),
         'n_unsplit_bridging_components': n_unsplit,
         'bracket_rule': getattr(_cj, 'CJUNC_SV_CF_BRACKET_RULE', 'lower_keep_unsplit_upper_remove_unsplit_sdcp_cells_v1'),
         'standing': ('certified_interval' if certs else 'diagnostic_uncertified'),
         'conv_cert_full': (_fake_pos_cert(SV_GF, topo=SV_TOPO_MAIN) if certs else None)}
    if n_unsplit:
        sh = status_hi or 'computed'
        rh = _sv_ratio_of(sh, ratio_hi)
        gh = _gc(sh, ratio_hi)
        r['upper'] = {'status': sh, 'sv_counterfactual_ratio': rh, 'cg_info': (0 if sh in ('computed', 'unconverged') else None),
                      'G_cut_code': gh, 'resid': (1e-13 if sh == 'computed' else None), 'conv_cert': _cc(sh, gh, SV_TOPO_UP),
                      'backend_last_solve': None,
                      'n_components_removed': n_unsplit, 'n_edges_cut': 6, 'n_plate_couplings_cut': 0, 'n_cells_removed': max(3, n_unsplit)}
        r['status_hi'], r['sv_counterfactual_ratio_hi'] = sh, rh
    else:
        r['upper'] = None
        r['status_hi'], r['sv_counterfactual_ratio_hi'] = status, r['sv_counterfactual_ratio']
    return r


def _sv_put(x, rec, census=None, ibot=SV_GF):
    """증거에 반사실 투영을 싣고 실제 census · 솔브 기록 `I_bot_code` 를 그 기록에 맞춘다 (★ 10-23 · RCA2-04 — 검증기가 census (못 가른 ⊆ 다리
    놓는 ⊆ 닿는 성분) · 분자 G_full 을 증거와 대조한다).  census = 줄 값 (기본 = 기록의 못 가른 덩어리 수 nu → nu · nu + 1 · nu + 2)."""
    ev = x['ca_ext']['cjunc']['evidence']
    ev['solve']['sv_counterfactual'] = rec
    ev['solve']['I_bot_code'] = ibot
    nu = rec.get('n_unsplit_bridging_components') if isinstance(rec, dict) else 0
    nu = nu if (type(nu) is int and 0 <= nu < 2 ** 62) else 0        # noqa: E721
    ev['census'].update(census if census is not None else
                        {'n_unsplit_bridging_components': nu, 'n_bridging_components': nu + 1, 'n_sdcp_components_touching': nu + 2})
    return x


def _cc_ok(ok=True, status='POSITIVE_SOLVED', **over):
    """반사실 풀이의 수렴 증서 투영 꼴 (`ca_ext_svcf._end_proj` 가 옮기는 칸)."""
    c = {'version': 'conv-cert-v2', 'status': status, 'ok': ok, 'pass_a': True, 'pass_b': True, 'pass_c': True, 'pass_d': bool(ok)}
    c.update(over)
    return c


def t_sv_values(mm, proj, Es):
    """★ PF2 E (10-22 · 사전 리뷰 2 회차 PRE2-impl-02 · 결정 없음) — 검증기가 기록 안 수를 다시 대조한다: computed = G_full · G_cut 유한 양수 ·
    비 = G_full/G_cut (상대 1e-12) · 비 ≥ (1 − τ)/(1 + τ) (증서 폭 꼴 · τ = 증서 ⓓ 보장 상대 오차) · 반사실 증서가 있으면 ok · ⓐ–ⓓ 참 ·
    POSITIVE_SOLVED · no_through = G_cut 0 · G_full 유한 양수 · 위 끝 (A 의 괄호) 도 같은 규칙 · 괄호 아래 ≤ 위 (같은 여유 · 아래 +∞ ⟹ 위 +∞).
    판정문 다섯 꼴 = 넷 (비 ≠ G 비 · 증서 ok False · G_cut None · 비 < 1) + 다섯째 (덩어리 1 · 괄호 칸 없음 = S8l · A 가 닫음)."""
    import math
    try:
        import ca_ext_svcf as SVCF
        import step3_conv_cert as CC
    except Exception as e:                                  # noqa: BLE001
        chk('S8n ca_ext_svcf · step3_conv_cert 를 불러온다', False, f'{type(e).__name__}: {e}')
        return
    tau = CC.CERT_TARGET_TOL
    floor = (1.0 - tau) / (1.0 + tau)
    chk('S8o 증서 폭 상수 — ca_ext_svcf.CERT_TARGET_TOL = step3_conv_cert.CERT_TARGET_TOL · RATIO_FLOOR = (1 − τ)/(1 + τ) · 다시 셈 허용 1e-12',
        getattr(SVCF, 'CERT_TARGET_TOL', None) == tau and getattr(SVCF, 'RATIO_FLOOR', None) == floor
        and getattr(SVCF, 'RATIO_REL_TOL', None) == 1e-12,
        (getattr(SVCF, 'CERT_TARGET_TOL', None), getattr(SVCF, 'RATIO_FLOOR', None), getattr(SVCF, 'RATIO_REL_TOL', None)))
    fl = getattr(SVCF, 'RATIO_FLOOR', floor)
    import carbon_junction as _CJ
    _cst = [(getattr(SVCF, a, None), getattr(_CJ, b, None)) for a, b in
            (('STANDING_CERTIFIED', 'SV_CF_STANDING_CERTIFIED'), ('STANDING_DIAGNOSTIC', 'SV_CF_STANDING_DIAGNOSTIC'),
             ('ZERO_GRAPH_SV_CF', 'SV_CF_ZERO_GRAPH'), ('UNSPLIT_MISMATCH', 'SV_CF_UNSPLIT_MISMATCH'),
             ('SV_CF_KIND', 'CJUNC_SV_CF_KIND'), ('SV_CF_RULE', 'CJUNC_SV_CF_RULE'))]   # ★ 10-23 C5 종류 · 규칙
    chk('S8q 검증기 상수 = 생산자 상수 (★ 10-23 RCA2-01 · 04) — 지위 둘 · 영값 위상 그래프 이름표 · 위 끝 구조화 실패 · 등록 괄호 규칙 = 생산자 규칙 하나 · '
        '(★ 10-23 사전 공격 리뷰 C5) 반사실 종류 · 끊기 규칙 이름',
        all(a is not None and a == b for a, b in _cst)
        and getattr(SVCF, 'BRACKET_RULES', None) == (getattr(_CJ, 'CJUNC_SV_CF_BRACKET_RULE', None),),
        (_cst, getattr(SVCF, 'BRACKET_RULES', None)))

    def ok_of(rec, census=None, ibot=SV_GF, fp=None):
        x = _sv_put(deep(mm), rec, census=census, ibot=ibot)
        if fp:
            Es(x)['fp'].update(fp)
        return RC.ca_ext_record_ok(x)

    def lo_rec(r, **kw):                                     # 덩어리 0 · computed 비 r (G_full 2.5 · G_cut = 2.5/r · 위 = 아래) 의 투영 + 손댐
        p = proj(_sv_raw('computed', r))
        p.update(kw)
        return p

    def br_rec(lo, hi, st='computed', sh='computed', up=None, nu=1, **kw):   # 덩어리 nu · 두 끝 (투영) + 손댐
        p = proj(_sv_raw(st, lo, n_unsplit=nu, status_hi=sh, ratio_hi=hi))
        p.update(kw)
        if up:
            p['upper'].update(up)
        return p

    def nt_rec(**kw):                                        # 덩어리 0 · 관통 없음 (+∞ · 영값 위상 증서) 의 투영 + 손댐
        p = proj(_sv_raw('no_through_without_sv'))
        p.update(kw)
        return p
    _cp = getattr(SVCF, '_cert_proj', lambda c: c)
    nt = dict(status='no_through_without_sv', sv_counterfactual_ratio=None, ratio_limit='inf', G_cut_code=0.0,
              status_hi='no_through_without_sv', sv_counterfactual_ratio_hi=None, ratio_limit_hi='inf')
    r_lo = math.nextafter(fl, 0.0)
    knife = 1.5 * fl
    raw_w = _sv_raw('computed', 1.25)
    raw_w['conv_cert_full'] = _fake_pos_cert(SV_GF, lo=SV_GF * (1.0 - 1e-5), hi=SV_GF * (1.0 + 1e-5), topo=SV_TOPO_MAIN)
    good = {
        '증서 구간 기록 · 비 1.25 (주 해 · 아래 끝 증서 · 결합 칸)': proj(_sv_raw('computed', 1.25)),
        '비 1 − 1e-9 (참 비 1 · 막다른 덩어리의 풀이 잡음 · 증서 폭 안)': proj(_sv_raw('computed', 1.0 - 1e-9)),
        '비 = (1 − τ)/(1 + τ) 정확 (칼날 · 받음)': proj(_sv_raw('computed', fl)),
        'no_through (G_cut 0 · G_full 2.5 · 영값 위상 증서)': proj(_sv_raw('no_through_without_sv')),
        '괄호 [1.5, 1.5 × (1 − 1e-9)] (막다른 덩어리 · 위 = 아래 참 · 증서 폭 안)': br_rec(1.5, 1.5 * (1 - 1e-9)),
        '괄호 [1.5, 1.5 × RATIO_FLOOR] (칼날 · 받음)': br_rec(1.5, knife),
        '괄호 [1.2, 3.4] · 위 끝 증서 ok': br_rec(1.2, 3.4),
        '괄호 [+∞, +∞] (아래 · 위 관통 없음)': br_rec(1.0, None, st='no_through_without_sv', sh='no_through_without_sv'),
        #  ★ 10-23 (RCA2-04 · Q1 (가))
        '진단 기록 (증서 없는 런 · 지위 diagnostic_uncertified · 판정 입력 아님)': proj(_sv_raw('computed', 1.25, certs=False)),
        '주 해 목표량 구간 [2.5(1 − 1e-5), 2.5(1 + 1e-5)] (폭 ≤ τ · 증서 통과)': proj(raw_w),
    }
    for nm, rec in good.items():
        chk(f'S8n 수 대조 정상 받음 [{nm}]', ok_of(rec) == (True, None), ok_of(rec))
    bad = {
        #  판정문 PRE2-impl-02 넷 (다섯째 = S8l '판정문 PRE2-impl-02 다섯째 꼴' · A 가 닫음)
        '판정문 ① 비 1.0 ≠ G_full/G_cut 1.25 (위 끝 칸도 1.0 · 덩어리 0 일관)': lo_rec(1.25, sv_counterfactual_ratio=1.0,
                                                                                      sv_counterfactual_ratio_hi=1.0),
        '판정문 ② computed 인데 반사실 증서 ok False (ⓓ 실패)': lo_rec(1.25, conv_cert=_cc_ok(ok=False)),
        '판정문 ③ computed 인데 G_cut None': lo_rec(1.25, G_cut_code=None),
        '판정문 ④ 비 0.5 < 1 (G_cut 5 = 2 G_full · 비 = G 비 일관)': lo_rec(0.5),
        #  같은 부류 · 꼴
        '비 = RATIO_FLOOR 바로 아래 (nextafter · 칼날 밖)': lo_rec(r_lo),
        '증서 ok True 인데 pass_d False (플래그를 믿지 않는다)': lo_rec(1.25, conv_cert=_cc_ok(ok=True, pass_d=False)),
        '증서 ok True 인데 상태 NOT_CERTIFIABLE': lo_rec(1.25, conv_cert=_cc_ok(ok=True, status='NOT_CERTIFIABLE')),
        '증서 꼴 dict 아님': lo_rec(1.25, conv_cert='ok'),
        'computed 인데 G_cut 0.0': lo_rec(1.25, G_cut_code=0.0),
        'computed 인데 G_cut 음수': lo_rec(1.25, G_cut_code=-2.0),
        'computed 인데 G_cut bool': lo_rec(1.25, G_cut_code=True),
        'computed 인데 G_cut bool True (G_full 1.25 · 비 1.25 = G 비 일관 · 셈 대조로는 안 걸린다)': lo_rec(1.25, G_full_code=1.25,
                                                                                               G_cut_code=True),
        'computed 인데 G_full None': lo_rec(1.25, G_full_code=None),
        'computed 인데 G_full 0.0': lo_rec(1.25, G_full_code=0.0),
        'computed 인데 G_full 음수 (G_cut 도 음수 · 비 = G 비 1.25)': lo_rec(1.25, G_full_code=-2.5, G_cut_code=-2.0),
        'G_full 1e300 · G_cut 1e-300 (G 비 넘침 = +∞ · 비 1.25)': lo_rec(1.25, G_full_code=1e300, G_cut_code=1e-300),
        'no_through 인데 G_cut 1.0 (관통 없음 = 0 이어야)': lo_rec(1.25, **dict(nt, G_cut_code=1.0)),
        'no_through 인데 G_cut None': lo_rec(1.25, **dict(nt, G_cut_code=None)),
        'no_through 인데 G_full None (비 +∞ 의 분자)': lo_rec(1.25, **dict(nt, G_full_code=None)),
        #  위 끝 (A 의 괄호) 같은 규칙
        '위 끝 비 4.0 ≠ G_full/G_cut_hi 3.4 (칸 · 풀이 기록 같이)': br_rec(1.2, 3.4, sv_counterfactual_ratio_hi=4.0,
                                                                         up={'sv_counterfactual_ratio': 4.0}),
        '위 끝 증서 ok False': br_rec(1.2, 3.4, up={'conv_cert': _cc_ok(ok=False)}),
        '위 끝 computed 인데 G_cut None': br_rec(1.2, 3.4, up={'G_cut_code': None}),
        '위 끝 비 0.5 (아래 1.0 · G_cut_hi 5 · 일관)': br_rec(1.0, 0.5),
        '위 끝 no_through 인데 G_cut 1.0': br_rec(1.2, None, sh='no_through_without_sv', up={'G_cut_code': 1.0}),
        #  괄호 아래 ≤ 위
        '괄호 위 1.2 < 아래 3.0 (둘 다 일관 · Rayleigh 위반)': br_rec(3.0, 1.2),
        '괄호 아래 +∞ 인데 위 유한 2.0': br_rec(1.0, 2.0, st='no_through_without_sv'),
        '괄호 위 = 아래 × RATIO_FLOOR 바로 아래 (nextafter)': br_rec(1.5, math.nextafter(knife, 0.0)),
        #  ★ 10-23 (Codex 재검토 RCA2-04 · 판정문 F3 다섯 꼴 + 같은 부류 · 실제 소비자 `run_contract.ca_ext_record_ok`)
        '판정문 F3 ① computed 끝 증서 없음 (증서 구간 기록)': lo_rec(1.25, conv_cert=None),
        '판정문 F3 ② 못 가른 덩어리 2 인데 제거 성분 0': br_rec(1.2, 3.4, nu=2, up={'n_components_removed': 0}),
        '판정문 F3 ③ 임의 괄호 규칙 (비지 않은 낱말)': lo_rec(1.25, bracket_rule='not-the-registered-rule'),
        '판정문 F3 ④ 못 가른 덩어리 수 10^400 (위 끝 기록 · 제거 수도 10^400 = 서로 일관 · 의미 범위 밖)':
            br_rec(1.2, 3.4, n_unsplit_bridging_components=10 ** 400, up={'n_components_removed': 10 ** 400, 'n_cells_removed': 10 ** 400}),
        '판정문 F3 ⑤ 외부 증서 (다른 실제 회로의 통과 증서 — 게시 판 전류 0.4484304932735439)':
            lo_rec(1.25, conv_cert=_cp(_fake_pos_cert(0.4484304932735439))),
        '옛 꼴 괄호 규칙 (lower_keep_upper_remove_fake_v1 — 등록 밖)': lo_rec(1.25, bracket_rule='lower_keep_upper_remove_fake_v1'),
        '외부 증서 (게시 판 전류만 그 끝 G 로 · 목표량 구간 = 다른 회로)': lo_rec(1.25, conv_cert=_cp(_fake_pos_cert(2.0, lo=0.448, hi=0.449))),
        '외부 증서 (결합 칸 = 다른 런 · 격자 지문)': lo_rec(1.25, conv_cert=_cp(_fake_pos_cert(2.0, fp_sid='e' * 32))),
        #  ★ 10-23 (A6 변이 표 A2-c7 생존 → 상주) 게시 판 전류만 다르고 목표량 구간은 그 끝 G 를 담는 증서 (같은 회로의 다른 풀이 증서 꼴)
        '끝 증서 게시 판 전류 ≠ 그 끝 G (목표량 구간은 G 를 담음)':
            lo_rec(1.25, conv_cert=_cp(_fake_pos_cert(2.0 * (1.0 + 1e-9), lo=2.0 * (1.0 - 1e-6), hi=2.0 * (1.0 + 1e-6)))),
        '위 끝 증서 없음': br_rec(1.2, 3.4, up={'conv_cert': None}),
        '주 해 증서 없음 (분자 G_full)': lo_rec(1.25, conv_cert_full=None),
        '주 해 증서 게시 판 전류 ≠ G_full': lo_rec(1.25, conv_cert_full=_cp(_fake_pos_cert(2.6))),
        '주 해 증서 결합 판 없음': lo_rec(1.25, conv_cert_full=_cp(_fake_pos_cert(SV_GF, bind_version=None))),
        '+∞ 끝 영값 위상 증서 없음': nt_rec(conv_cert=None),
        '+∞ 끝 증서 = 양의 해 증서 (위상 증명 아님)': nt_rec(conv_cert=_cp(_fake_pos_cert(2.0))),
        '+∞ 끝 영값 증서 = 다른 그래프의 0 (조립 그래프 · 끊은 반사실 그래프 아님)':
            nt_rec(conv_cert=_cp(_fake_zero_cert(zero_graph='cjunc_assembled'))),
        '지위 칸 없음 (옛 기록)': lo_rec(1.25, standing=None),
        '지위 = 진단 인데 증서가 실려 있다': lo_rec(1.25, standing='diagnostic_uncertified'),
        '판정 근거 칸 변조 [9, 9]': lo_rec(1.25, ratio_cert_interval=[9.0, 9.0]),
        '판정 근거 칸 없음 (옛 투영)': lo_rec(1.25, ratio_cert_interval=None),
        '제거 셀 수 < 성분 수 (못 가른 덩어리 2 · 셀 1)': br_rec(1.2, 3.4, nu=2, up={'n_cells_removed': 1}),
        '제거 셀 수 10^400': br_rec(1.2, 3.4, up={'n_cells_removed': 10 ** 400}),
        '끊은 간선 수 음수': br_rec(1.2, 3.4, up={'n_edges_cut': -1}),
    }
    reasons = {}
    for nm, rec in bad.items():
        got = ok_of(rec)
        chk(f'S8n 수 대조 거부 [{nm}]', not got[0], got)
        reasons[nm] = got[1]
    #  ★ 10-23 (A6 변이 표 — 생존 A2-c7 · c8 · c9 · c10 · c17 → 상주) 일관 변조 — 위 거부 꼴의 판정 근거 칸 (`ratio_cert_interval`) 을 변조한
    #    기록의 증서에서 다시 센 값으로 맞춘다 (그 칸을 함께 고친 변조자) → 그 칸 대조 (`_interval_problem`) 에 기대지 않고 각 검사가 제 문장으로
    #    거부해야 한다 (옛 시험 = 변조 뒤 그 칸이 낡아 칸 대조가 대신 거부 → 끝 증서 게시 판 전류 · 목표량 구간 · 영값 그래프 · 진단 지위 · 지위 칸
    #    검사를 꺼도 통과) · 판정 근거 칸 자체를 바꾼 꼴은 뺀다
    _ci, _en = getattr(SVCF, 'cert_interval', None), getattr(SVCF, '_enc', lambda v: v)
    if callable(_ci):
        cons = {}
        for nm, rec in bad.items():
            if '판정 근거 칸' in nm:
                continue
            r2 = deep(rec)
            lo2, hi2 = _ci(r2)
            r2['ratio_cert_interval'] = [_en(lo2), _en(hi2)]
            cons[nm] = ok_of(r2)
        odd_c = {nm: g for nm, g in cons.items() if g[0] or not (isinstance(g[1], str) and g[1].startswith('CAEXT|cjunc| sv_cf|'))}
        chk(f'S8s 일관 변조 {len(cons)} 꼴 (판정 근거 칸 = 변조한 기록의 증서에서 다시 셈) — 전부 검증기 자신의 문장으로 거부 (칸 대조에 기대지 않음)',
            len(cons) == len(bad) - 2 and not odd_c, odd_c)
    else:
        chk('S8s ca_ext_svcf.cert_interval 이 있다', False, 'cert_interval 없음')
    #  ★ 10-23 (사전 공격 리뷰 C1 · 1저자 Q12 (가)) 끝 증서 ↔ 끊은 그래프 — 실제 소비자 (`run_contract.ca_ext_record_ok`) 경로: 같은 기록의 주 해
    #    증서를 끝 자리에 옮긴 일관 편집 (그 끝 G = G_full · 비 1 · 위 끝 칸 · 판정 근거 칸 다시 셈) → 자기 문장으로 거부 (리뷰 A2 꼴 · 옛 판 = 받음)
    if callable(_ci):
        def _swap(raw, where):
            p = proj(raw)
            end = p if where == 'lower' else p['upper']
            end.update(G_cut_code=SV_GF, sv_counterfactual_ratio=1.0, conv_cert=deep(p['conv_cert_full']))
            if where == 'upper' or p.get('upper') is None:
                p['sv_counterfactual_ratio_hi'] = 1.0
            lo3, hi3 = _ci(p)
            p['ratio_cert_interval'] = [_en(lo3), _en(hi3)]
            return p
        c1 = {'덩어리 0 · 아래 끝 증서 = 주 해 증서 (끊은 다리 면 4)': _swap(_sv_raw('computed', 1.25), 'lower'),
              '덩어리 1 · 아래 끝 증서 = 주 해 증서 (위 끝 [3.4] 그대로)': _swap(_sv_raw('computed', 1.2, n_unsplit=1, ratio_hi=3.4), 'lower'),
              '덩어리 1 · 위 끝 증서 = 주 해 증서 (아래 끝 비 1 · 위 끝 간선 6 뺌)': _swap(_sv_raw('computed', 1.0, n_unsplit=1, ratio_hi=3.4), 'upper')}
        for nm, rec in c1.items():
            got = ok_of(rec)
            chk(f'S8t 끝 증서 = 같은 기록의 주 해 증서 (일관 편집) → 실제 소비자 거부 [{nm}]',
                not got[0] and isinstance(got[1], str) and got[1].startswith('CAEXT|cjunc| sv_cf|') and '사전 공격 리뷰 C1' in got[1], got)
    #  ★ 10-23 (RCA2-04) — 증거 쪽 대조 (실제 census · 솔브 기록 I_bot_code · fp) — 같은 기록 · 다른 증거
    lo1, br1 = proj(_sv_raw('computed', 1.25)), proj(_sv_raw('computed', 1.2, n_unsplit=1, ratio_hi=3.4))
    ev_bad = {
        'census 불일치 (실제 census 못 가른 덩어리 2 · 기록 1)':
            (br1, {'n_unsplit_bridging_components': 2, 'n_bridging_components': 2, 'n_sdcp_components_touching': 3}, SV_GF, None),
        'census 순서 모순 (못 가른 1 > 다리 놓는 0)':
            (br1, {'n_unsplit_bridging_components': 1, 'n_bridging_components': 0, 'n_sdcp_components_touching': 2}, SV_GF, None),
        'census 칸 없음 (못 가른 · 다리 놓는 · 닿는 성분 수)': (lo1, {'n_unsplit_bridging_components': None}, SV_GF, None),
        '솔브 기록 I_bot_code ≠ G_full': (lo1, None, 2.6, None),
        '솔브 기록 I_bot_code 없음': (lo1, None, None, None),
        '증거 fp sid = 다른 런': (lo1, None, SV_GF, {'sid': 'f' * 32}),
    }
    for nm, (rec, cen, ib, fpo) in ev_bad.items():
        got = ok_of(rec, census=cen, ibot=ib, fp=fpo)
        chk(f'S8n 증거 대조 거부 [{nm}]', not got[0], got)
        reasons[nm] = got[1]
    #  ★ 10-23 (A6 변이 표 A2-c15 생존 → 상주) 구간 함수 — +∞ 끝 = 끊은 반사실 그래프의 영값 위상 증서만 (검증기의 영값 증서 검사와 따로 ·
    #    다른 그래프의 0 = 그 끝 못 정함 None · 사슬 = 못 읽음)
    if callable(_ci):
        _z0 = proj(_sv_raw('no_through_without_sv'))
        _z1 = deep(_z0)
        _z1['conv_cert'] = _cp(_fake_zero_cert(zero_graph='cjunc_assembled'))
        chk('S8r 구간 함수 — +∞ 끝 = 끊은 반사실 그래프의 영값 위상 증서 (∞ · ∞) · 같은 기록에 다른 그래프의 0 (조립 그래프) = 못 정함 (None · None)',
            _ci(_z0) == (math.inf, math.inf) and _ci(_z1) == (None, None), (_ci(_z0), _ci(_z1)))
    #  ★ 같은 부류 (10-22 · 변이 ME8 · ME9) — 증서 꼴 · G_cut 꼴 검사를 끄면 뒤의 셈이 예외로 무너지고 계약의 감싸기 (`unverifiable`) 가
    #    대신 거부했다 (받음 · 거부는 같고 사유만 다르다) → 거부 사유 = 검증기 자신의 문장 (`sv_cf|`) 이어야 한다
    odd = {nm: why for nm, why in reasons.items() if not (isinstance(why, str) and why.startswith('CAEXT|cjunc| sv_cf|'))}
    chk('S8n 거부 사유 = 검증기 자신의 문장 (CAEXT|cjunc| sv_cf| …) — 예외 감싸기 (unverifiable) · 다른 검사로 거부된 꼴 없음', not odd, odd)
    ev = getattr(SVCF, '_end_view', None)
    cv = getattr(SVCF, 'chain_view', None)
    if callable(ev) and callable(cv):
        bad_v = [ev('computed', x, None) for x in (float('nan'), -1.0, 0.0, -math.inf, math.inf, True)]
        bad_v += [ev('no_through_without_sv', 5.0, 'inf'), ev('no_through_without_sv', None, None)]
        tam = {'status': 'computed', 'sv_counterfactual_ratio': float('nan'), 'ratio_limit': None, 'status_hi': 'computed',
               'sv_counterfactual_ratio_hi': -2.0, 'ratio_limit_hi': None, 'n_unsplit_bridging_components': 1}
        vt = cv(tam)
        chk('S8p 사슬 꼴 — 한 끝의 비 = 유한 양수 · +∞ (null + "inf") 만 읽음 · NaN · 음수 · 0 · ±∞ (finite 꼴) · bool · inf 꼴의 수 = None '
            '(못 읽음 · 사슬 SV_UNCHECKED) · 정상 1.25 · +∞ 그대로',
            all(v is None for v in bad_v) and vt.get('ratio') is None and vt.get('ratio_hi') is None
            and ev('computed', 1.25, None) == 1.25 and ev('no_through_without_sv', None, 'inf') == math.inf, (bad_v, vt))


def _sv_raw_mm(nu, removed, certs=True):
    """★ 10-23 (Codex 재검토 RCA2-06 F6) 위 끝 구조화 실패의 원 기록 — 생산자 함수 그대로 (`carbon_junction._sv_cf_upper_unsolved` ·
    `_sv_cf_bracket`): census 의 못 가른 덩어리 수 nu ≠ 지문 묶인 원장에서 다시 가른 수 removed → 위 끝을 풀지 않음 (비 · 증서 · backend 없음 ·
    사유) · 아래 끝 = computed 1.25 (증서 구간 · certs False = 진단 기록)."""
    import carbon_junction as _cj
    r = _sv_raw('computed', 1.25, certs=certs)
    r['n_unsplit_bridging_components'] = nu
    up = _cj._sv_cf_upper_unsolved(_cj.SV_CF_UNSPLIT_MISMATCH, n_components=removed,
                                   why=f'못 가른 덩어리 수 census {nu} ≠ 지문 묶인 원장에서 다시 가른 수 {removed} — 위 끝을 풀지 않는다')
    return _cj._sv_cf_bracket(r, up)


def t_sv_mismatch(mm, proj, Es):
    """★ 10-23 (Codex 재검토 RCA2-06 F6 · author 10-23 ratified Q1-Q8) 위 끝 구조화 실패 `unsplit_census_mismatch` (census 의 못 가른 덩어리 수 ≠
    지문 묶인 원장에서 다시 가른 수 · 위 끝을 풀지 않음 · fail-closed) 를 끝-끝 보존한다 — 실제 소비자 `run_contract.ca_ext_record_ok`.
    옛 판: census 0 꼴 = '덩어리 0 인데 위 끝 기록' 으로 게시 거부 (사슬에 닿지 않았다) · census > 0 꼴 = 꼴을 보지 않고 받았다 (풀이 칸이 차
    있어도 · 다시 가른 수 = census 수여도).  고친 판: 꼴 = 다시 가른 수 (0 이상 정수 · int64) ≠ census 수 · 사유 = 비지 않은 글 · 풀이 칸
    (비 · 표지 · G_cut · 잔차 · CG · 증서 · backend · 제거 셀 수) 없음 · 위 끝 칸 = (상태, None, None) → 받음 · 사슬 = SV_UNCHECKED (못 읽음 ·
    진단 기록이면 판정 입력 아님) · 사유에 상태 이름."""
    try:
        import ca_ext_svcf as SVCF
        import rint_r_chain as RRc
    except Exception as e:                                  # noqa: BLE001
        chk('SM0 ca_ext_svcf · rint_r_chain 을 불러온다', False, f'{type(e).__name__}: {e}')
        return
    MM = getattr(SVCF, 'UNSPLIT_MISMATCH', 'unsplit_census_mismatch')
    KNOWN = getattr(SVCF, 'KNOWN_STATUSES', ())
    chk('SM0 상태 목록에 구조화 실패 이름 (기록 · 문서용 목록 · 이것만으로 끝내지 않는다 = SM1–SM4)', MM in KNOWN, KNOWN)

    def ok_of(rec, census=None, ibot=SV_GF):
        return RC.ca_ext_record_ok(_sv_put(deep(mm), rec, census=census, ibot=ibot))

    def chain_of(rec):
        f, d = RRc.sv_assess({('1', 'P1', 'R_j0'): {'sv_cf': SVCF.chain_view(rec)}}, 2.0, 'R_j0')
        return f, d, RRc.sv_reasons(f, d).get('SV_UNCHECKED', '')

    good = {
        'census 0 · 다시 가른 수 1 (QD2 ⑧ 꼴 · 증서 구간)': _sv_raw_mm(0, 1),
        'census 1 · 다시 가른 수 2 (증서 구간)': _sv_raw_mm(1, 2),
        'census 2 · 다시 가른 수 0 (원장에서 덩어리가 사라짐)': _sv_raw_mm(2, 0),
        'census 0 · 다시 가른 수 1 (진단 기록 · 증서 없는 런)': _sv_raw_mm(0, 1, certs=False),
    }
    for nm, raw in good.items():
        rec = proj(raw)
        got = ok_of(rec)
        f, d, why = chain_of(rec)
        lst = 'uncertified' if raw.get('standing') == 'diagnostic_uncertified' else 'unreadable'
        chk(f'SM1 구조화 실패 받음 · 사슬 SV_UNCHECKED · 사유에 상태 이름 [{nm}]',
            got == (True, None) and f == ['SV_UNCHECKED'] and 'c1_P1_R_j0' in (d.get(lst) or []) and f'c1_P1_R_j0 ({MM})' in why,
            (got, f, why))
    _cp = getattr(SVCF, '_cert_proj', lambda c: c)

    def mm_rec(nu=1, removed=2, up=None, **kw):              # 구조화 실패 꼴의 투영 + 손댐 (위 끝 · 기록)
        p = proj(_sv_raw_mm(nu, removed))
        if up:
            p['upper'].update(up)
        p.update(kw)
        return p
    bad = {
        '다시 가른 수 = census 수 (1 · 1 — 상태의 정의와 모순)': mm_rec(1, 1),
        '다시 가른 수 = census 수 (0 · 0)': mm_rec(0, 0),
        '다시 가른 수 없음': mm_rec(up={'n_components_removed': None}),
        '다시 가른 수 bool': mm_rec(up={'n_components_removed': True}),
        '다시 가른 수 음수': mm_rec(up={'n_components_removed': -1}),
        '다시 가른 수 10^400': mm_rec(up={'n_components_removed': 10 ** 400}),
        '사유 없음 (None)': mm_rec(up={'why': None}),
        '사유 빈 글': mm_rec(up={'why': ''}),
        '사유 공백만': mm_rec(up={'why': '   '}),
        '사유 글 아님 (수)': mm_rec(up={'why': 7}),
        '풀이 칸 — 비 2.0': mm_rec(up={'sv_counterfactual_ratio': 2.0}),
        '풀이 칸 — inf 표지': mm_rec(up={'ratio_limit': 'inf'}),
        '풀이 칸 — G_cut 1.0': mm_rec(up={'G_cut_code': 1.0}),
        '풀이 칸 — G_cut 0.0 (관통 없음을 숨김)': mm_rec(up={'G_cut_code': 0.0}),
        '풀이 칸 — 잔차': mm_rec(up={'resid': 1e-13}),
        '풀이 칸 — CG info 0': mm_rec(up={'cg_info': 0}),
        '풀이 칸 — 증서': mm_rec(up={'conv_cert': _cp(_fake_pos_cert(2.0))}),
        '풀이 칸 — backend': mm_rec(up={'backend_last_solve': {'used': 'gpu', 'requested': 'gpu', 'precond': None, 'fallback_reason': None}}),
        '풀이 칸 — 제거 셀 수 3 (풀지 않은 끝)': mm_rec(up={'n_cells_removed': 3}),
        '풀이 칸 — 끊은 간선 수 6': mm_rec(up={'n_edges_cut': 6}),
        '풀이 칸 — 판 결합 끊은 수 0': mm_rec(up={'n_plate_couplings_cut': 0}),
        '풀이 칸 — SV 면 끊은 수 0': mm_rec(up={'n_sv_faces_cut': 0}),
        '위 끝 칸 = 아래 끝 (census 1 · computed 1.25 — 구조화 실패를 위 끝 칸이 숨김)':
            mm_rec(status_hi='computed', sv_counterfactual_ratio_hi=1.25, ratio_limit_hi=None),
        '위 끝 칸 = 아래 끝 (census 0 · computed 1.25)':
            mm_rec(0, 1, status_hi='computed', sv_counterfactual_ratio_hi=1.25, ratio_limit_hi=None),
        '위 끝 칸 상태 unconverged (위 끝 풀이 기록 = 구조화 실패)': mm_rec(status_hi='unconverged'),
        '위 끝 칸 상태 = 구조화 실패 · 위 끝 풀이 기록 상태 unconverged': mm_rec(up={'status': 'unconverged'}),
    }
    reasons = {}
    for nm, rec in bad.items():
        got = ok_of(rec)
        chk(f'SM2 구조화 실패 꼴 거부 [{nm}]', not got[0], got)
        reasons[nm] = got[1]
    odd = {nm: why for nm, why in reasons.items() if not (isinstance(why, str) and why.startswith('CAEXT|cjunc| sv_cf|'))}
    chk('SM2 거부 사유 = 검증기 자신의 문장 (CAEXT|cjunc| sv_cf| …) — 예외 감싸기 (unverifiable) 로 거부된 꼴 없음', not odd, odd)
    #  ── 실제 생산자 기록 → 투영 → 실제 소비자 (`run_contract.ca_ext_record_ok`) → 사슬 (chain_view · sv_assess · sv_reasons) ──
    #     원장 census 의 못 가른 덩어리 수를 계획 전에 변조 (지문 밖) — 위 끝은 지문 묶인 원장으로 다시 가른다
    #     꼴 ① = QD2 ⑧ (덩어리 하나 · census 0) · 꼴 ② = QD4 두 성분 (census 1) · 증서 끔 (진단) · 켬 (증서 구간 · 증거 fp = 그 런의 원장 · 계획 지문)
    try:
        import test_carbon_junction as TCJ
        import carbon_junction as _cjm
        import step3_sigma as _s3
    except Exception as e:                                  # noqa: BLE001
        chk('SM3 test_carbon_junction · carbon_junction · step3_sigma 를 불러온다', False, f'{type(e).__name__}: {e}')
        return
    TCJ.CJ, TCJ.S3 = _cjm, _s3
    forms = (('꼴 ① 덩어리 하나 · census 0 (QD2 ⑧)', [TCJ.QD2_A1, TCJ.QD2_B1], TCJ.QD2_S1, TCJ.QD2_N1, 0, 1),
             ('꼴 ② 두 성분 · census 1 (QD4)', getattr(TCJ, 'QD4_POLYS', None), getattr(TCJ, 'QD4_SDCP', None), getattr(TCJ, 'QD4_N', None), 1, 2))
    for nm, polys, sdcp, n, nu, k in forms:
        if polys is None:
            chk(f'SM3 실제 생산자 [{nm}] — 시험 꼴이 있다 (test_carbon_junction.QD4_*)', False, 'QD4 꼴 없음')
            continue
        for cert in (False, True):
            def _hook(reg, nu=nu):
                reg['census']['n_unsplit_bridging_components'] = nu
            _s, reg, r, cf = TCJ._qd2_run(polys, sdcp, n, reg_hook=_hook, cert=cert)
            if r is None:
                chk(f'SM3 실제 생산자 [{nm} · 증서 {"켬" if cert else "끔"}] — 풀이', False, '풀이 실패')
                continue
            rec = SVCF.sv_cf_record(cf)
            up = rec.get('upper') if isinstance(rec.get('upper'), dict) else {}
            cen = TCJ._qd2_census(r)
            x = _sv_put(deep(mm), rec, census={c: cen[c] for c in SVCF.CENSUS_COPY_KEYS if c in cen}, ibot=r['cjunc'].get('I_bot_code'))
            if cert:
                pl = TCJ.plan(reg, 1e3, sv_counterfactual={'threshold': None})
                Es(x)['fp'].update(sid=reg['fp']['sid'], registry=reg['fp']['registry'], plan_rows=pl['fp_rows'])
                Es(x)['receipts']['electronic_main']['fp_registry'] = reg['fp']['registry']
            got = RC.ca_ext_record_ok(x)
            f, d, why = chain_of(rec)
            lst = 'unreadable' if cert else 'uncertified'
            chk(f'SM3 실제 생산자 → 실제 소비자 → 사슬 [{nm} · 증서 {"켬 (증서 구간)" if cert else "끔 (진단)"}] — 위 끝 = 구조화 실패 (다시 가른 수 '
                f'{k} · census {nu} · 사유 · 풀이 칸 없음) · ca_ext_record_ok 받음 · 사슬 SV_UNCHECKED · 사유에 상태 이름',
                rec.get('n_unsplit_bridging_components') == nu and up.get('status') == MM and up.get('n_components_removed') == k
                and bool(up.get('why')) and rec.get('standing') == ('certified_interval' if cert else 'diagnostic_uncertified')
                and got == (True, None) and f == ['SV_UNCHECKED'] and 'c1_P1_R_j0' in (d.get(lst) or []) and f'c1_P1_R_j0 ({MM})' in why,
                (got, f, why, up))


@case('S 해 상태 (영값 · 단락) · SV 반사실 노브 — 계약 · 러너 · payload (시험 먼저 · 10-21 D)')
def t_states():
    ngs = getattr(RC, 'next_gen_state', None)
    chk('S0 run_contract.next_gen_state 가 있다 (다음 세대 해 상태 → positive · zero · short · legacy)', callable(ngs))
    if not callable(ngs):
        ngs = lambda s3: (None, 'absent')                    # noqa: E731 — 고치기 전: 아래 검사를 시험 단위로 실패시킨다
    m = cj_manifest()
    s3p = {'sigma_e_eff_S_cm': 0.05, 'n_dof': 100, 'cg_info': 0, 'unconverged': False, 'cg_resid': 1e-13, 'manifest': m,
           'conv_cert': good_cert(0.05)}
    z, sh = state_manifest('zero'), state_manifest('short')
    chk('S1a 양의 해 → positive', ngs(s3p) == ('positive', None), ngs(s3p))
    chk('S1b 바닥 영값 위상 (조기 반환 · 증서 VALID_ZERO_TOPOLOGY · σ 0) → zero', ngs(z) == ('zero', None), ngs(z))
    chk('S1c 천장 단락 (J11 · 증서 ELECTRODE_SHORT · σ None) → short', ngs(sh) == ('short', None), ngs(sh))
    chk('S1d 옛 세대 (ca_ext 없음 · 요청 없음) → legacy (이 규칙 밖)',
        ngs({'sigma_e_eff_S_cm': 0.05, 'manifest': cohort_manifests()[0]}) == ('legacy', None))

    def zmut(fn, base=None):
        x = deep(base if base is not None else z)
        fn(x)
        return x
    M = lambda x: x['manifest']                              # noqa: E731
    Ev = lambda x: x['manifest']['ca_ext']['cjunc']['evidence']   # noqa: E731
    bad_zero = {
        'σ 1e-9 (영값 사유인데 0 아님)': lambda x: x.update(sigma_e_eff_S_cm=1e-9),
        'σ None (영값을 비워 둠)': lambda x: x.update(sigma_e_eff_S_cm=None),
        '결과 사유 없음 (증서만 조기 반환)': lambda x: x.pop('reason'),
        '결과 사유 ≠ 증서 사유': lambda x: x.update(reason='all_floating_dropped'),
        '전자 component complete (조기 반환인데 솔브 완료로 적음)': lambda x: M(x)['components'].update(electronic={'status': 'complete'}),
        '증서 ok False': lambda x: x['conv_cert'].update(ok=False),
        '증서 판본 다름': lambda x: x['conv_cert'].update(version='conv-cert-v1'),
        '증서 출처 모름': lambda x: x['conv_cert'].update(zero_source='guess'),
        '증서 지문 hex 아님': lambda x: x['conv_cert'].update(fp_sid='Z' * 32),
        '증서 없음': lambda x: x.pop('conv_cert'),
        '증서 상태 NOT_CERTIFIABLE': lambda x: x.update(conv_cert=_early_cert('degenerate_thin_bed')),
        '증서 상태 모름': lambda x: x['conv_cert'].update(status='MYSTERY'),
        #  ★ 10-21 (PRE-impl-07 병합 · B 결합) — 영값 증서 ↔ 그 런: 다른 침대 격자 · 결합 판 없음 · 접합 지문 다름
        '증서 격자 지문 ≠ 매니페스트 sid (다른 침대의 영값 증서)': lambda x: x['conv_cert'].update(fp_sid='e' * 32),
        '증서 결합 판 없음 (옛 증서)': lambda x: x['conv_cert'].pop('bind_version'),
        '증서 접합 계획 행 지문 ≠ 매니페스트': lambda x: x['conv_cert'].update(fp_cjunc_rows='e' * 32),
    }
    for nm, fn in bad_zero.items():
        st, why = ngs(zmut(fn))
        chk(f'S2 영값 상태 거부 [{nm}] → (None, 사유)', st is None and isinstance(why, str) and why, (st, why))
    bad_short = {
        'σ 0.0 (단락을 유한 σ 로 위장)': lambda x: x.update(sigma_e_eff_S_cm=0.0),
        'σ 1e3 (단락을 유한 σ 로 위장)': lambda x: x.update(sigma_e_eff_S_cm=1e3),
        '증서 ok True': lambda x: x['conv_cert'].update(ok=True),
        '증서 사유가 영값 사유 (상태와 모순)': lambda x: x['conv_cert'].update(reason='no_through_component'),
        '결과 사유 ≠ 증서 사유': lambda x: x.update(reason='no_through_component'),
        '접합 기록 short False': lambda x: Ev(x)['solve'].update(short=False),
        '접합 기록 solved True': lambda x: Ev(x)['solve'].update(solved=True),
        '축약 0 (단락이 생길 수 없다)': lambda x: (Ev(x)['counts'].update(n_contract=0, n_edge=3), M(x)['ca_ext']['cjunc']['protocol']),
        '접합 블록 없음': lambda x: (M(x).pop('ca_ext'), M(x).pop('ca_ext_requested'), M(x).update(ptfe_stamp='face_alpha')),
        '전자 component complete': lambda x: M(x)['components'].update(electronic={'status': 'complete'}),
        '증서 판본 다름': lambda x: x['conv_cert'].update(version='conv-cert-v1'),
        '봉인 상수 손으로 (rtol_max)': lambda x: x['conv_cert'].update(rtol_max=1e-8),
        #  ★ 10-21 (PRE-impl-07 병합 · B 결합을 단락 가지에도) — 단락 증서도 조기 반환 증서 (결합 칸을 싣는다 · `early_record`) — 옛 가지는
        #    격자 지문의 hex32 꼴만 봐 다른 침대의 단락 증서를 받았다 (B 가 영값 · 양의 해에서 막은 것과 같은 부류)
        '증서 격자 지문 ≠ 매니페스트 sid (다른 침대의 단락 증서)': lambda x: x['conv_cert'].update(fp_sid='e' * 32),
        '증서 결합 판 없음 (옛 증서)': lambda x: x['conv_cert'].pop('bind_version'),
        '증서 접합 원장 지문 ≠ 매니페스트': lambda x: x['conv_cert'].update(fp_cjunc_registry='e' * 32),
    }
    for nm, fn in bad_short.items():
        st, why = ngs(zmut(fn, sh))
        chk(f'S3 단락 상태 거부 [{nm}] → (None, 사유)', st is None and isinstance(why, str) and why, (st, why))
    #  ★ 10-21 (PRE-impl-07 병합) — 이온을 계획해 푼 단락 팔: 이온 증서 (채널 ionic · 접합 지문 None) 를 결합까지 본다 (두 인자 호출 = TypeError 였다)
    shi = deep(sh)
    shi['manifest']['component_plan'] = dict(shi['manifest']['component_plan'], ionic=True)
    shi['manifest']['components'] = dict(shi['manifest']['components'], ionic={'status': 'complete'})
    shi['sigma_ion_eff_S_cm'] = 0.001
    shi['ion_conv_cert'] = good_cert(0.001, channel='ionic')
    try:
        r_ok, r_bad = ngs(shi), ngs(dict(shi, ion_conv_cert=dict(good_cert(0.001, channel='ionic'), fp_sid='e' * 32)))
    except Exception as e:                                  # noqa: BLE001 — 고치기 전 (두 인자 호출) 도 시험 단위로
        r_ok = r_bad = (None, f'{type(e).__name__}: {e}')
    chk('S3i 단락 팔 + 이온 계획 — 이온 증서 정상 = short · 이온 증서 격자 지문 ≠ 매니페스트 = 거부 (채널 ionic 결합)',
        r_ok == ('short', None) and r_bad[0] is None and 'CERT|bind|' in str(r_bad[1]), (r_ok, r_bad))
    #  ★ 10-21 (D2 · 옳은 이유) — 위 결합 경우 (영값 셋 · 단락 셋) 의 거부 사유 = 결합 함수 (`CERT|bind|`) · 상태 머리 (STATE|zero| · STATE|short|)
    #    (S2 · S3 은 거부만 본다 — 다른 검사가 우연히 거부해도 통과하므로 결합 자리를 여기서 못 박는다)
    _bind_nm = ('증서 격자 지문 ≠ 매니페스트 sid', '증서 결합 판 없음 (옛 증서)', '증서 접합')
    _bz = [(nm, ngs(zmut(fn))) for nm, fn in bad_zero.items() if nm.startswith(_bind_nm)]
    _bs = [(nm, ngs(zmut(fn, sh))) for nm, fn in bad_short.items() if nm.startswith(_bind_nm)]
    chk('S3b 결합 거부의 사유 — 영값 셋 = STATE|zero| … CERT|bind| · 단락 셋 = STATE|short| CERT|bind| (옳은 이유)',
        len(_bz) == 3 and len(_bs) == 3
        and all(r[0] is None and str(r[1]).startswith('STATE|zero|') and 'CERT|bind|' in str(r[1]) for _n, r in _bz)
        and all(r[0] is None and str(r[1]).startswith('STATE|short| CERT|bind|') for _n, r in _bs),
        [(n, str(r[1])[:90]) for n, r in _bz + _bs])
    bad_pos = {'증서 실패 (ok False)': lambda x: x['conv_cert'].update(ok=False, pass_b=False),
               '증서 없음': lambda x: x.pop('conv_cert'),
               'σ ≠ 증서 σ': lambda x: x.update(sigma_e_eff_S_cm=0.06)}
    for nm, fn in bad_pos.items():
        st, why = ngs(zmut(fn, s3p))
        chk(f'S4 양의 해 거부 [{nm}] → (None, 사유)', st is None and why, (st, why))
    #  ── check_arm (러너가 팔을 OUTDIR 로 옮기기 전 · 캐시 SKIP) — 영값 · 단락 상태 팔을 받는다 · 옛 꼴 · 변조는 거부 ──
    import sr01_stamp_compare as SC
    td = tempfile.mkdtemp(prefix='b6_s_')
    try:
        def arm(s3, nm):
            p = os.path.join(td, nm)
            json.dump({'mpm_metrics': {'step3': s3}}, open(p, 'w', encoding='utf-8'))
            return p
        rz, rs = SC.check_arm(arm(z, 'z.json'), 'segment', expect_backend='gpu'), SC.check_arm(arm(sh, 's.json'), 'segment',
                                                                                              expect_backend='gpu')
        chk('S5a check_arm — 영값 상태 팔 (σ 0 · 증서 VALID_ZERO_TOPOLOGY) 를 받는다 (솔브 없음 = backend 기록 없음 · 정상)', rz is None, rz)
        chk('S5b check_arm — 단락 상태 팔 (σ None · 증서 ELECTRODE_SHORT) 를 받는다', rs is None, rs)
        for nm, fn in (('영값인데 σ 1e-9', bad_zero['σ 1e-9 (영값 사유인데 0 아님)']), ('영값 증서 없음', bad_zero['증서 없음']),
                       ('영값인데 component complete', bad_zero['전자 component complete (조기 반환인데 솔브 완료로 적음)'])):
            r_ = SC.check_arm(arm(zmut(fn), f'zb_{len(nm)}.json'), 'segment', expect_backend='gpu')
            chk(f'S5c check_arm 거부 [{nm}]', isinstance(r_, str) and r_, r_)
        r_ = SC.check_arm(arm(zmut(bad_short['σ 0.0 (단락을 유한 σ 로 위장)'], sh), 'sb.json'), 'segment', expect_backend='gpu')
        chk('S5d check_arm 거부 [단락인데 σ 0.0 — 유한 σ 로 위장]', isinstance(r_, str) and r_, r_)
        old = deep(z)
        old.pop('conv_cert')
        r_ = SC.check_arm(arm(old, 'old.json'), 'segment', expect_backend='gpu')
        chk('S5e check_arm — 증서 없는 영값 팔 (옛 꼴 · 증서 끔) 은 그대로 거부 (σ 0 을 증서 없이 받지 않는다)', isinstance(r_, str) and r_, r_)
        p2 = {'sigma_e_eff_S_cm': 0.0, 'reason': 'no_through_component', 'vox_um': 0.15, 'manifest': cohort_manifests()[0]}
        r_ = SC.check_arm(arm(p2, 'p2.json'), 'segment')
        chk('S5f check_arm — 옛 세대 (p2) σ 0 팔은 그대로 거부 (이 규칙 밖 · 옛 거동)', isinstance(r_, str) and r_, r_)
    finally:
        shutil.rmtree(td, ignore_errors=True)
    #  ── receipt_match — 솔브가 하나도 안 돈 팔 (조기 반환) 의 rtol 결합 ──
    base = {k: v for k, v in json.load(open(os.path.join(ROOT, 'docs/data/w4b_ptfe_off_20260827/run_receipt.json'),
                                            encoding='utf-8')).items() if k != 'receipt_digest'}
    rq_f = {'cjunc': dict(CJ_REQ, R_j_ohm=None, rj_limit='inf')}
    chk('S6a 조기 반환 팔 (솔브 0 · backend.rtol 없음) + 러너 rtol 선언 → receipt_match 통과 (결합할 솔브가 없다)',
        RC.receipt_match(dict(base, ca_ext_request=rq_f, step3_rtol=1e-12), z['manifest'])[0],
        RC.receipt_match(dict(base, ca_ext_request=rq_f, step3_rtol=1e-12), z['manifest']))
    zc = deep(z['manifest'])
    zc['components']['electronic'] = {'status': 'complete', 'backend': {'used': 'gpu'}}
    chk('S6b 솔브가 돈 팔 (component complete) 인데 backend.rtol 없음 → 그대로 거부 (옛 결합)',
        not RC.receipt_match(dict(base, ca_ext_request=rq_f, step3_rtol=1e-12), zc)[0])
    #  ── SV 반사실 노브 — 러너 손잡이 표 · 발사 전 검사 · 영수증 · payload 인자 · 이름 태그 · CLI 회계 ──
    tab = {n: (s, k) for n, s, k in getattr(RC, 'RUNNER_CA_EXT_ENV', ())}
    chk('S7a 러너 손잡이 표에 CJUNC_SV_CF (선언 칸 아님 = 하위 블록 None · 영수증 선택 칸 sv_counterfactual)',
        tab.get('CJUNC_SV_CF') == (None, 'sv_counterfactual'), tab.get('CJUNC_SV_CF'))
    env = {'CJUNC': '1', 'CJUNC_RJ': '1e6', 'CJUNC_LEN_LAW': 'len_scaled_v0', 'CJUNC_UNREG_LAW': 'cut', 'CJUNC_S_MIN_UM': '0.5',
           'CJUNC_TOL_FF_UM': '0.5', 'CJUNC_PTFE_JLAW': 'P0', 'STEP3_RTOL': '1e-12'}
    on = RC.runner_ca_ext(dict(env, CJUNC_SV_CF='1'), lean='2')
    off = RC.runner_ca_ext(dict(env), lean='2')
    chk('S7b CJUNC_SV_CF=1 → 문제 없음 · 영수증 sv_counterfactual True · 요청 칸 (cjunc) = 끈 것과 같다 (반사실은 protocol 밖)',
        on['problems'] == [] and on['receipt'].get('sv_counterfactual') is True
        and on['receipt'].get('ca_ext_request') == off['receipt'].get('ca_ext_request'), on)
    chk('S7c 끔 (비움 · 0) → 영수증에 칸 없음 (옛 영수증 바이트 · 옛 OUTDIR)',
        'sv_counterfactual' not in off['receipt'] and RC.runner_ca_ext(dict(env, CJUNC_SV_CF='0'), lean='2') == off, off['receipt'])
    for nm, e_, code in (('CJUNC 없이', {'CJUNC_SV_CF': '1', 'STEP3_RTOL': '1e-12'}, 'RUNNER_CA_EXT|FLAG_WITHOUT_CJUNC|'),
                         ('값 yes', dict(env, CJUNC_SV_CF='yes'), 'RUNNER_CA_EXT|VALUE|'),
                         ('값 2', dict(env, CJUNC_SV_CF='2'), 'RUNNER_CA_EXT|VALUE|'),
                         ('값 " 1"', dict(env, CJUNC_SV_CF=' 1'), 'RUNNER_CA_EXT|VALUE|')):
        pr = RC.runner_ca_ext(e_, lean='2')['problems']
        chk(f'S7d 발사 전 거부 [{nm}] → {code}', any(p.startswith(code) for p in pr), pr)
    v_on = RC.runner_ca_ext_view(dict(base, **on['receipt'])) if on['problems'] == [] else {}
    v_off = RC.runner_ca_ext_view(dict(base, **off['receipt']))
    chk('S7e payload 인자 · 이름 태그 — 켬 = " --step3-cjunc-sv-cf" 한 번 · 태그 끝 "_svcf" · 선언 (--expect-physics) 은 끈 것과 같다',
        (v_on.get('flags') or '').count(' --step3-cjunc-sv-cf') == 1 and (v_on.get('tag') or '').endswith('_svcf')
        and v_on.get('expect') == v_off.get('expect') and '--step3-cjunc-sv-cf' not in v_off['flags'] and not v_off['tag'].endswith('_svcf'),
        (v_on, v_off))
    r_on, r_off = dict(base, **on['receipt']), dict(base, **off['receipt'])
    chk('S7f 영수증 digest — 켬 ≠ 끔 (OUTDIR 이 갈린다) · 끔 = 칸 없음의 옛 digest', on['problems'] == []
        and RC.receipt_digest(r_on) != RC.receipt_digest(r_off), (RC.receipt_digest(r_on), RC.receipt_digest(r_off)))
    chk('S7g CLI 회계 — --step3-cjunc-sv-cf = solve (σ_e 해를 바꾸지 않는 추가 솔브 · 규약 id 밖)',
        RC.CLI_ACCOUNTING.get('--step3-cjunc-sv-cf') == ('solve', None), RC.CLI_ACCOUNTING.get('--step3-cjunc-sv-cf'))
    #  ── 반사실 기록 (증거) — 투영 꼴 (JSON 유한 · inf 비 = null + 표지 'inf') · 검증기 ──
    #  ★ 10-21 (코디네이터 — 접합 파일 = A 소관 · PRE-impl-04 Q-D) — 투영 · 검증 = D 모듈 `ca_ext_svcf` (끊는 면의 정의에 기대지 않는다:
    #    비 · 상태 · 표지 칸만 · kind = 'counterfactual…' 아무 정의 · 수 칸 = 이름 그대로 옮김) · 계약 자리 = run_contract.ca_ext_record_ok
    try:
        import ca_ext_svcf as SVCF
    except Exception as e:                                  # noqa: BLE001 — 고치기 전 (모듈 없음) 도 시험 단위로 기록
        SVCF = None
        print(f'  ⚠ ca_ext_svcf 를 못 불러온다 ({type(e).__name__}: {e})')
    proj = getattr(SVCF, 'sv_cf_record', None)
    chk('S8a ca_ext_svcf.sv_cf_record (증거 투영 · D 모듈) 가 있다', callable(proj))
    if callable(proj):
        pc, pn = proj(_sv_raw('computed', 1.25)), proj(_sv_raw('no_through_without_sv'))
        chk('S8b 투영 — computed = 비 그대로 (유한) · 표지 없음 · no_through_without_sv = 비 null + ratio_limit "inf" · JSON 유한 (allow_nan False)',
            pc.get('sv_counterfactual_ratio') == 1.25 and pc.get('ratio_limit') is None and pn.get('sv_counterfactual_ratio') is None
            and pn.get('ratio_limit') == 'inf' and json.dumps([pc, pn], allow_nan=False) is not None, (pc, pn))
    else:
        proj = lambda r: r                                   # noqa: E731
    mm = cj_manifest()
    Es = lambda x: x['ca_ext']['cjunc']['evidence']          # noqa: E731
    Es(mm)['sv_counterfactual_request'] = {'threshold': None}
    _sv_put(mm, proj(_sv_raw('computed', 1.25)))
    chk('S8c 요청 + computed 기록 → ca_ext_record_ok 통과 · id = 노브 끈 것과 같다 (반사실은 protocol 밖)',
        RC.ca_ext_record_ok(mm) == (True, None) and RC.physics_protocol_id(mm) == cj_manifest()['physics_protocol_id'],
        RC.ca_ext_record_ok(mm))
    good = {'no_through_without_sv': proj(_sv_raw('no_through_without_sv')), 'unconverged': proj(_sv_raw('unconverged')),
            '문턱 2 · 비 3 · SV_DEPENDENT': proj(_sv_raw('computed', 3.0, threshold=2.0, flag='SV_DEPENDENT'))}
    for nm, rec in good.items():
        x = deep(mm)
        if '문턱' in nm:
            Es(x)['sv_counterfactual_request'] = {'threshold': 2.0}
        _sv_put(x, rec)
        chk(f'S8d 정상 기록 받음 [{nm}]', RC.ca_ext_record_ok(x) == (True, None), RC.ca_ext_record_ok(x))
    S_ = lambda x: Es(x)['solve']['sv_counterfactual']      # noqa: E731
    bad_sv = {
        '요청 있는데 기록 없음 (주 솔브 풀림)': lambda x: Es(x)['solve'].pop('sv_counterfactual'),
        '기록 있는데 요청 없음': lambda x: Es(x).pop('sv_counterfactual_request'),
        '요청 문턱 0.5 (< 1 · 뜻 없음)': lambda x: Es(x).update(sv_counterfactual_request={'threshold': 0.5}),
        '요청 모르는 칸': lambda x: Es(x).update(sv_counterfactual_request={'threshold': None, 'x': 1}),
        '요청 ↔ 기록 문턱 다름': lambda x: S_(x).update(threshold=2.0),
        'computed 인데 비 None': lambda x: S_(x).update(sv_counterfactual_ratio=None),
        'computed 인데 비 음수': lambda x: S_(x).update(sv_counterfactual_ratio=-1.0),
        'computed 인데 비 문자열': lambda x: S_(x).update(sv_counterfactual_ratio='1.25'),
        'computed 인데 inf 표지': lambda x: S_(x).update(ratio_limit='inf'),
        '모르는 상태인데 비가 있다': lambda x: S_(x).update(status='mystery'),
        '종류가 반사실이 아님 (cut_vv)': lambda x: S_(x).update(kind='cut_vv'),
        '종류 없음': lambda x: S_(x).update(kind=None),
        'requested False': lambda x: S_(x).update(requested=False),
        '문턱 없는데 SV_DEPENDENT 표지': lambda x: S_(x).update(flag='SV_DEPENDENT'),
        '모르는 표지': lambda x: S_(x).update(flag='SV_DOMINANT'),
        'no_through 인데 표지 없음': lambda x: S_(x).update(status='no_through_without_sv', sv_counterfactual_ratio=None, ratio_limit=None),
    }
    for nm, fn in bad_sv.items():
        x = deep(mm)
        fn(x)
        chk(f'S8e 반사실 기록 거부 [{nm}]', not RC.ca_ext_record_ok(x)[0], RC.ca_ext_record_ok(x))
    x = deep(mm)
    Es(x)['sv_counterfactual_request'] = {'threshold': 2.0}
    _sv_put(x, proj(_sv_raw('computed', 3.0, threshold=2.0, flag=None)))
    chk('S8f 문턱 2 · 비 3 인데 표지 없음 (문턱 판정과 기록이 갈림) → 거부', not RC.ca_ext_record_ok(x)[0])
    #  ── 정의 무관 (PRE-impl-04 · Q-D) — 끊는 면의 정의 (A 가 바꾼다) 와 그 이름 · 수 칸이 바뀌어도 비 · 상태 · 표지만으로 받는다 ──
    #  ★ 10-23 (사전 공격 리뷰 C1 · 1저자 Q12 (가)) — 정의별 수 칸 이름이 바뀐 꼴 = 증서 없는 런 (진단 기록) 에서만 정의 무관 그대로 받는다 · 증서 구간
    #    기록의 비를 싣는 끝은 끊은 다리 면 수 (n_sv_faces_cut) 로 끝 증서를 끊은 그래프에 묶어야 해서 그 칸이 없으면 거부 (아래 S8h′)
    #  ★ 10-23 (사전 공격 리뷰 C5 · 1저자 Q14 (가)) — 종류 · 규칙 이름은 등록값만 받는다 (옛 '다른 정의의 반사실 = 받음' 꼴 → 아래 S8w 거부)
    agn = {'정의별 수 칸 이름이 바뀜 (n_sv_faces_cut 없음 · n_bridging_faces_cut 3 · 진단 기록)':
           lambda r: (r.pop('n_sv_faces_cut'), r.update(n_bridging_faces_cut=3, standing='diagnostic_uncertified', conv_cert=None,
                                                        conv_cert_full=None)),
           '모르는 상태 · 비 없음 (사슬 = SV_UNCHECKED · 받는다)':
           #  ★ 10-22 (Q1 (다)) — 못 가른 덩어리 0 기록의 위 끝 = 아래 끝 (괄호 칸도 같은 상태로 · 기록 내부 일관)
           lambda r: r.update(status='no_bridging_sv_faces', sv_counterfactual_ratio=None, G_cut_code=None,
                              status_hi='no_bridging_sv_faces', sv_counterfactual_ratio_hi=None)}
    for nm, fn in agn.items():
        raw = _sv_raw('computed', 1.25)
        fn(raw)
        x = deep(mm)
        _sv_put(x, proj(raw))
        chk(f'S8h 정의 무관 받음 [{nm}]', RC.ca_ext_record_ok(x) == (True, None), RC.ca_ext_record_ok(x))
    #  ★ 10-23 (사전 공격 리뷰 C5 · 1저자 Q14 (가)) — 종류 = `carbon_junction.CJUNC_SV_CF_KIND` · 규칙 = `CJUNC_SV_CF_RULE` 만 (이름 대조 · 끊는 면의
    #    뜻에는 기대지 않는다) · 다른 값 = 자기 사유 문장으로 거부 · 증서 구간 · 진단 기록 둘 다
    import carbon_junction as _cjw
    c5 = {'다른 정의 이름 (kind counterfactual_cut_bridging_sv_faces)': (lambda r: r.update(kind='counterfactual_cut_bridging_sv_faces'), 'kind'),
          '옛 정의 이름 (kind counterfactual_cut_sv_faces = SV 면 전부)': (lambda r: r.update(kind='counterfactual_cut_sv_faces'), 'kind'),
          '리뷰 A4 (kind counterfactual_cut_sv_faces_all)': (lambda r: r.update(kind='counterfactual_cut_sv_faces_all'), 'kind'),
          '종류 접두어만 같음 (kind counterfactual)': (lambda r: r.update(kind='counterfactual'), 'kind'),
          '종류 글자 아님 (목록)': (lambda r: r.update(kind=[_cjw.CJUNC_SV_CF_KIND]), 'kind'),
          '리뷰 A4 (rule some_other_rule)': (lambda r: r.update(rule='some_other_rule'), 'rule'),
          '규칙 없음': (lambda r: r.pop('rule'), 'rule'),
          '규칙 None': (lambda r: r.update(rule=None), 'rule'),
          '규칙 = 괄호 규칙 이름': (lambda r: r.update(rule=_cjw.CJUNC_SV_CF_BRACKET_RULE), 'rule')}
    for certs in (True, False):
        for nm, (fn, field) in c5.items():
            raw = _sv_raw('computed', 1.25, certs=certs)
            fn(raw)
            x = deep(mm)
            _sv_put(x, proj(raw))
            got = RC.ca_ext_record_ok(x)
            chk(f'S8w 종류 · 규칙 = 등록 이름만 (10-23 사전 공격 리뷰 C5) → 거부 [{nm} · {"증서 구간" if certs else "진단"}]',
                not got[0] and isinstance(got[1], str) and '사전 공격 리뷰 C5' in got[1] and f'기록 {"종류" if field == "kind" else "규칙"}' in got[1],
                got)
    raw = _sv_raw('computed', 1.25)
    x = deep(mm)
    _sv_put(x, proj(raw))
    chk('S8w′ 등록 종류 · 규칙 (생산자 상수) → 받음 · 투영이 규칙을 옮긴다 (10-23 사전 공격 리뷰 C5)',
        RC.ca_ext_record_ok(x) == (True, None) and proj(raw).get('rule') == _cjw.CJUNC_SV_CF_RULE
        and proj(raw).get('kind') == _cjw.CJUNC_SV_CF_KIND, (RC.ca_ext_record_ok(x), proj(raw).get('rule')))
    raw = _sv_raw('computed', 1.25)
    raw.pop('n_sv_faces_cut')
    raw['n_bridging_faces_cut'] = 3
    x = deep(mm)
    _sv_put(x, proj(raw))
    got = RC.ca_ext_record_ok(x)
    chk('S8h′ 증서 구간 기록 (비를 싣는 끝 computed) 에 끊은 다리 면 수 n_sv_faces_cut 없음 (이름이 바뀜) → 거부 (끝 증서를 끊은 그래프에 묶을 수 없다 · '
        '10-23 사전 공격 리뷰 C1)',
        not got[0] and isinstance(got[1], str) and '사전 공격 리뷰 C1' in got[1] and 'n_sv_faces_cut' in got[1], got)
    raw = _sv_raw('computed', 1.25)
    raw.pop('n_sv_faces_cut')
    raw['n_bridging_faces_cut'] = 3
    pj = proj(raw)
    chk('S8i 투영 — 정의별 수 칸 (n_*) 은 이름 그대로 옮긴다 · 사슬이 읽는 칸 (비 · 상태 · 표지 · 종류) 은 그대로',
        isinstance(pj, dict) and pj.get('n_bridging_faces_cut') == 3 and 'n_sv_faces_cut' not in pj
        and pj.get('sv_counterfactual_ratio') == 1.25 and pj.get('status') == 'computed' and pj.get('flag') is None, pj)
    #  ── ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 02 · 1저자 Q1 (다)) 괄호 칸 — 투영 · 검증기 (위 끝 상태 ↔ 비 꼴 · 못 가른 덩어리 수 ↔ 위 끝 기록) ──
    rb = _sv_raw('computed', 1.0, n_unsplit=1, status_hi='no_through_without_sv')
    pb = proj(rb)
    pbu = pb.get('upper') if isinstance(pb, dict) and isinstance(pb.get('upper'), dict) else {}
    chk('S8j 투영 — 괄호 칸 (위 끝 상태 · 비 (+∞ = null + ratio_limit_hi "inf") · 위 끝 풀이 기록 (아래 끝과 같은 꼴 · +∞ = ratio_limit "inf") · '
        '괄호 규칙 · 못 가른 덩어리 수) · JSON 유한 (allow_nan False)',
        isinstance(pb, dict) and pb.get('status_hi') == 'no_through_without_sv' and pb.get('sv_counterfactual_ratio_hi') is None
        and pb.get('ratio_limit_hi') == 'inf' and pbu.get('status') == 'no_through_without_sv' and pbu.get('sv_counterfactual_ratio') is None
        and pbu.get('ratio_limit') == 'inf' and pbu.get('n_cells_removed') == 3 and pb.get('bracket_rule') == rb['bracket_rule']
        and pb.get('n_unsplit_bridging_components') == 1 and json.dumps(pb, allow_nan=False) is not None, pb)
    good_br = {'덩어리 1 · [1, ∞] (리뷰어 꼴)': rb,
               '덩어리 1 · [1.2, 3.4] (둘 다 computed)': _sv_raw('computed', 1.2, n_unsplit=1, status_hi='computed', ratio_hi=3.4),
               '덩어리 1 · 위 끝 미수렴 (비 없음 = 사슬 못 읽음)': _sv_raw('computed', 1.2, n_unsplit=1, status_hi='unconverged'),
               '덩어리 2 · 아래 끝 미수렴 · 위 끝 +∞': _sv_raw('unconverged', n_unsplit=2, status_hi='no_through_without_sv'),
               '덩어리 0 · 위 = 아래 (no_through)': _sv_raw('no_through_without_sv')}
    for nm, raw in good_br.items():
        x = deep(mm)
        _sv_put(x, proj(raw))
        chk(f'S8k 괄호 정상 기록 받음 [{nm}]', RC.ca_ext_record_ok(x) == (True, None), RC.ca_ext_record_ok(x))

    def _up_set(r, **kw):
        if isinstance(r.get('upper'), dict):
            r['upper'].update(kw)
    bad_br = {      # 덩어리 0 · computed 1.25 (mm 의 투영) 에서 칸 하나씩
        '괄호 칸 없음 (옛 꼴 · status_hi 없음)': lambda r: r.pop('status_hi', None),
        '판정문 PRE2-impl-02 다섯째 꼴 (덩어리 1 · computed · 괄호 칸 없음)':
            lambda r: (r.update(n_unsplit_bridging_components=1), r.pop('status_hi', None), r.pop('upper', None)),
        '덩어리 1 인데 위 끝 기록 없음 (한 번만 풂)': lambda r: r.update(n_unsplit_bridging_components=1),
        '덩어리 0 인데 위 끝 기록 있음': lambda r: r.update(upper={'status': 'computed', 'sv_counterfactual_ratio': 1.25, 'ratio_limit': None}),
        '덩어리 0 인데 위 비 ≠ 아래 비': lambda r: r.update(sv_counterfactual_ratio_hi=2.0),
        '덩어리 0 인데 위 상태 ≠ 아래 상태': lambda r: r.update(status_hi='unconverged', sv_counterfactual_ratio_hi=None),
        '위 끝 상태 빈 낱말': lambda r: r.update(status_hi=''),
        '위 끝 computed 인데 비 None': lambda r: r.update(sv_counterfactual_ratio_hi=None),
        '위 끝 computed 인데 inf 표지': lambda r: r.update(ratio_limit_hi='inf'),
        '위 끝 no_through 인데 inf 표지 없음':
            lambda r: r.update(status_hi='no_through_without_sv', sv_counterfactual_ratio_hi=None, ratio_limit_hi=None),
        '위 끝 비 없는 상태인데 비가 있다': lambda r: r.update(status_hi='unconverged'),
        '못 가른 덩어리 수 bool': lambda r: r.update(n_unsplit_bridging_components=True),
        '못 가른 덩어리 수 음수': lambda r: r.update(n_unsplit_bridging_components=-1),
        '못 가른 덩어리 수 없음': lambda r: r.pop('n_unsplit_bridging_components', None),
        '괄호 규칙 없음': lambda r: r.update(bracket_rule=None),
    }
    for nm, fn in bad_br.items():
        x = deep(mm)
        fn(Es(x)['solve']['sv_counterfactual'])
        chk(f'S8l 괄호 기록 거부 [{nm}]', not RC.ca_ext_record_ok(x)[0], RC.ca_ext_record_ok(x))
    bad_br1 = {     # 덩어리 1 · [1.2, 3.4] 에서 칸 하나씩
        '위 끝 칸 ≠ 위 끝 풀이 기록 (상태)': lambda r: _up_set(r, status='unconverged', sv_counterfactual_ratio=None, ratio_limit=None),
        '위 끝 칸 ≠ 위 끝 풀이 기록 (비)': lambda r: r.update(sv_counterfactual_ratio_hi=4.0),
        '덩어리 1 인데 위 끝 기록이 dict 아님': lambda r: r.update(upper='x'),
        '덩어리 1 인데 위 끝 기록 None': lambda r: r.update(upper=None),
    }
    for nm, fn in bad_br1.items():
        x = deep(mm)
        _sv_put(x, proj(_sv_raw('computed', 1.2, n_unsplit=1, status_hi='computed', ratio_hi=3.4)))
        fn(Es(x)['solve']['sv_counterfactual'])
        chk(f'S8l 괄호 기록 거부 [{nm}]', not RC.ca_ext_record_ok(x)[0], RC.ca_ext_record_ok(x))
    ch = getattr(SVCF, 'chain_view', None)
    v_b = ch(proj(rb)) if callable(ch) else {}
    v_o = ch(proj({k: v for k, v in _sv_raw('computed', 1.25).items() if k not in ('status_hi', 'sv_counterfactual_ratio_hi', 'upper')})) \
        if callable(ch) else {}
    chk('S8m 사슬 꼴 (chain_view) — 아래 끝 · 위 끝 (+∞) · 못 가른 덩어리 수 · 위 끝 칸이 없는 옛 꼴 = 위 끝 None (못 읽음 · fail-closed)',
        v_b.get('ratio') == 1.0 and v_b.get('ratio_hi') == float('inf') and v_b.get('status_hi') == 'no_through_without_sv'
        and v_b.get('n_unsplit') == 1 and v_o.get('ratio') == 1.25 and v_o.get('ratio_hi') is None and 'ratio_hi' in v_o, (v_b, v_o))
    t_sv_values(mm, proj, Es)
    t_sv_mismatch(mm, proj, Es)
    #  ── 조기 반환 해 (주 솔브 안 풀림) — 반사실 기록 없음 = 정상 · 요청만 남는다 ──
    zz = deep(z['manifest'])
    zz['ca_ext']['cjunc']['evidence']['sv_counterfactual_request'] = {'threshold': None}
    chk('S8g 조기 반환 (바닥 · 영값) + 요청 · 기록 없음 → 통과 (주 솔브가 없으면 반사실도 없다)', RC.ca_ext_record_ok(zz) == (True, None),
        RC.ca_ext_record_ok(zz))
    #  ── 영수증 ↔ 매니페스트 (반사실 요청) ──
    rq = {'cjunc': dict(CJ_REQ)}
    chk('S9a 영수증 sv_counterfactual True ↔ 증거 요청 있음 → 통과 · 영수증 칸 없음 ↔ 요청 있음 → 거부 · 영수증 True ↔ 요청 없음 → 거부',
        RC.receipt_match(dict(base, ca_ext_request=rq, sv_counterfactual=True), mm)[0]
        and not RC.receipt_match(dict(base, ca_ext_request=rq), mm)[0]
        and not RC.receipt_match(dict(base, ca_ext_request=rq, sv_counterfactual=True), cj_manifest())[0],
        (RC.receipt_match(dict(base, ca_ext_request=rq, sv_counterfactual=True), mm),
         RC.receipt_match(dict(base, ca_ext_request=rq), mm)))
    #  ── payload 조기 반환 step3 조립 (단락 = σ None · 증서 복사 · 끔 = 옛 dict 그대로) ──
    try:
        import mpm_webapp_payload as PAY
    except Exception as e:                                  # noqa: BLE001
        PAY = None
        print(f'  ⚠ payload 를 못 불러온다 ({type(e).__name__}: {e})')
    f_ = getattr(PAY, '_step3_early', None)
    chk('S10a payload._step3_early (조기 반환 해의 step3 조립 · 한 곳) 가 있다', callable(f_))
    if callable(f_):
        sc_ = _early_cert('cjunc_electrode_short')
        zc_ = _early_cert('no_through_component')
        a1 = f_({'reason': 'cjunc_electrode_short', 'conv_cert': sc_, 'sigma_eff': 0.0}, 0.15)
        a2 = f_({'reason': 'no_through_component', 'conv_cert': zc_, 'sigma_eff': 0.0}, 0.15)
        a3 = f_({'reason': 'no_plate_contact(bot=0,top=1)', 'sigma_eff': 0.0}, 0.15)
        chk('S10b 단락 → σ None (유한 σ 로 위장 안 함) · 증서 복사 · 사유', a1.get('sigma_e_eff_S_cm', 0) is None
            and a1.get('conv_cert') == sc_ and a1.get('conv_cert') is not sc_ and a1.get('reason') == 'cjunc_electrode_short', a1)
        chk('S10c 영값 → σ 0.0 · 증서 복사', a2.get('sigma_e_eff_S_cm') == 0.0 and type(a2.get('sigma_e_eff_S_cm')) is float
            and a2.get('conv_cert') == zc_, a2)
        chk('S10d 증서 끔 (칸 없음) → 옛 dict 그대로 (키 · 값 · 순서 = σ 0.0 · 사유 · vox)',
            list(a3.items()) == [('sigma_e_eff_S_cm', 0.0), ('reason', 'no_plate_contact(bot=0,top=1)'), ('vox_um', 0.15)], a3)


def make_fixture_nofloor(d):
    """b6 픽스처에서 판에 닿는 AM 기둥을 뺀 침대 (가운데 AM 구 하나만 · 떠 있음) — 접합을 끊으면 (바닥 R_j → ∞) 두 판을 잇는 성분이 없다
    = VALID_ZERO_TOPOLOGY (등록 R §5-0 · 바닥 극한)."""
    make_fixture(d, sdcp=False, ptfe=False)
    with open(os.path.join(d, 'am.csv'), 'w', encoding='utf-8') as f:     # 두 줄 (한 줄이면 loadtxt 가 1 차원 배열을 낸다)
        f.write('# type,x,y,z,r  (D 영값 바닥 픽스처 · 떠 있는 AM 구 둘 · 판 · 섬유와 안 닿는다)\n'
                '2,0.016000,0.016000,0.012000,0.002000\n2,0.016000,0.032000,0.012000,0.002000\n')
    return d


def make_fixture_thin_cross(d):
    """★ 4판 (10-21 · 1저자 Q1) 단락 침대 — 두 층 (0–2 µm · vox 1.0) · VGCF V1 (x 방향 · 아래 층 z 0.5) 와 V2 (y 방향 · 위 층 z 1.5) 가 셀
    (24, 24) 기둥에서 엇갈린다 (중심선 거리 1.0 µm · 접합 instance 하나 · 포트 = 셀 중심) · SE 가 두 층을 채운다 (V1 기둥의 위 · V2 기둥의 아래 =
    절연 고체) → V1 = 아래 판 접점 · V2 = 위 판 접점 · 접합을 축약하면 (천장 R_j → 0) 축약 무리가 두 판에 다 닿는다 = J11 단락 · 바닥 (R_j → ∞)
    = 관통 성분 없음 (VALID_ZERO_TOPOLOGY) · 유한 R_j = 양의 해.  AM = 판 · 섬유와 떨어진 작은 구 둘 (격자에 안 찍힌다).  tol_ff = 1.0 µm 로 돌린다."""
    with open(os.path.join(d, 'am.csv'), 'w', encoding='utf-8') as f:
        f.write('# type,x,y,z,r  (Rint ② 4판 Q1 단락 침대)\n2,0.014000,0.014000,0.001000,0.000300\n2,0.034000,0.034000,0.001000,0.000300\n')
    g = np.arange(12.0, 36.01, 0.75)
    gz = np.array([0.25, 0.75, 1.25, 1.75])
    se = np.array([[x, y, z] for x in g for y in g for z in gz], np.float64)
    blocks = [(_box(se), 1, -1, 0),
              (_box(line((12.5, 24.5, 0.5), (36.5, 24.5, 0.5), 97)), 2, 0, 1),        # V1 (아래 층 · x 방향)
              (_box(line((24.5, 12.5, 1.5), (24.5, 36.5, 1.5), 97)), 2, 1, 1)]        # V2 (위 층 · y 방향)
    pts = np.vstack([b[0] for b in blocks])
    np.save(os.path.join(d, 'se.npy'), pts)
    np.save(os.path.join(d, 'phase.npy'), np.concatenate([np.full(len(b[0]), b[1], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre.npy'), np.concatenate([np.full(len(b[0]), b[2], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre_kind.npy'), np.concatenate([np.full(len(b[0]), b[3], np.int8) for b in blocks]))
    np.save(os.path.join(d, 'fibre_dia.npy'), np.ones(len(pts)))
    return d


def make_fixture_sv_unsplit(d, b_start_z):
    """★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · payload 끝-끝 꼴 = 판정문 탐침 `probe2_sv_unsplit_payload.py`) — b6 AM 기둥 줄 그대로 · SE 점은
    섬유에서 먼 x 12–18 µm · VGCF A = (24.5, 24.5) 아래 판 z 0.3 → z 18.5 (위 판에 안 닿음) · B = (26.5, 24.5) z `b_start_z` → 위 판 z 23.2 ·
    SDCP 점 셋 (24.5 · 25.5 · 26.5, 24.5, 12.5) = 셀 (24 · 25 · 26, 24, 12) — A · B 의 z 12 셀을 덮고 둘을 잇는다.  b_start_z 6.5 = 두 섬유가
    같은 덩어리를 지남 (못 가른 덩어리) · 12.5 = B 가 덩어리 안에서 시작 (한 섬유만 지남 · 대조)."""
    with open(os.path.join(d, 'am.csv'), 'w', encoding='utf-8') as f:
        rows = ['# type,x,y,z,r  (Rint ② PF2 Q1 (다) 못 가른 덩어리 침대)']
        for ix in range(2):
            for iy in range(2):
                for k in range(3):
                    rows.append('2,%.6f,%.6f,%.6f,%.6f' % (0.020 + 0.008 * ix, 0.020 + 0.008 * iy, 0.004 + 0.0075 * k, 0.004))
        f.write('\n'.join(rows) + '\n')
    g = np.arange(12.0, 18.01, 0.75)
    gy = np.arange(12.0, 36.01, 0.75)
    gz = np.arange(0.3, 23.2, 0.75)
    se = np.array([[x, y, z] for x in g for y in gy for z in gz], np.float64)
    blocks = [(_box(se), 1, -1, 0),
              (_box(line((24.5, 24.5, 0.3), (24.5, 24.5, 18.5), 73)), 2, 0, 1),
              (_box(line((26.5, 24.5, b_start_z), (26.5, 24.5, 23.2), 69)), 2, 1, 1),
              (_box(np.array([[24.5, 24.5, 12.5], [25.5, 24.5, 12.5], [26.5, 24.5, 12.5]])), 5, -1, 0)]
    pts = np.vstack([b[0] for b in blocks])
    np.save(os.path.join(d, 'se.npy'), pts)
    np.save(os.path.join(d, 'phase.npy'), np.concatenate([np.full(len(b[0]), b[1], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre.npy'), np.concatenate([np.full(len(b[0]), b[2], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre_kind.npy'), np.concatenate([np.full(len(b[0]), b[3], np.int8) for b in blocks]))
    np.save(os.path.join(d, 'fibre_dia.npy'), np.ones(len(pts)))
    return d


@case('SP 해 상태 · SV 반사실 — payload 끝-끝 (시험 먼저 · 10-21 D)')
def t_states_payload():
    if ARGS.skip_payload:
        print('    (--skip-payload — 건너뜀)')
        return
    import step3_conv_cert as CC
    import sr01_stamp_compare as SC
    td = tempfile.mkdtemp(prefix='b6_sp_')
    try:
        os.makedirs(os.path.join(td, 'nf'))
        os.makedirs(os.path.join(td, 'dbe'))
        nf = make_fixture_nofloor(os.path.join(td, 'nf'))
        dd = make_fixture(os.path.join(td, 'dbe'), sdcp=True)
        FLOOR = OFF + LEAN2 + cj_with(rj='inf') + ['--step3-cjunc-rj-limit', 'inf']
        rc_z, log_z, p_z = run_payload(nf, FLOOR + ['--step3-rtol', '1e-12'], out='floor.json')
        s3z = s3_of(p_z)
        cz = s3z.get('conv_cert') or {}
        chk('SP1 바닥 (R_j → ∞) 영값 침대 + rtol — rc 0 · σ 0.0 · 사유 no_through_component · 증서 복사 (VALID_ZERO_TOPOLOGY · early_return)',
            rc_z == 0 and s3z.get('sigma_e_eff_S_cm') == 0.0 and str(s3z.get('reason', '')).startswith('no_through_component')
            and cz.get('status') == CC.STATUS_ZERO and cz.get('zero_source') == 'early_return' and cz.get('ok') is True,
            (rc_z, s3z.get('reason'), cz.get('status'), log_z.strip()[-400:]))
        st_z = getattr(RC, 'next_gen_state', lambda s: (None, 'absent'))(s3z)
        chk('SP2 next_gen_state = zero · ca_ext_record_ok 통과', st_z == ('zero', None)
            and RC.ca_ext_record_ok(man_of(p_z)) == (True, None), (st_z, RC.ca_ext_record_ok(man_of(p_z)) if p_z else None))
        r_ca = SC.check_arm(os.path.join(nf, 'floor.json'), 'segment', expect_backend='cpu') if p_z else 'payload 없음'
        chk('SP3 check_arm (러너가 쓰는 함수) 이 실제 영값 팔을 받는다', r_ca is None, r_ca)
        rc_z0, _l0, p_z0 = run_payload(nf, FLOOR, out='floor_nocert.json')
        _fz = os.path.join(nf, 'floor_nocert.json.failed')
        p_z0f = json.load(open(_fz, encoding='utf-8')) if os.path.exists(_fz) else None
        chk('SP4 증서 끔 (rtol 없음) — 게시 거부 (rc 4 · 최종 파일 없음 · 옛 거동: 증서 없는 σ 0 = 수치 증거 실패) · 진단본 step3 = 옛 꼴 '
            '(증서 칸 없음 · σ 0.0) · next_gen_state 거부',
            rc_z0 == 4 and p_z0 is None and p_z0f is not None and 'conv_cert' not in s3_of(p_z0f)
            and s3_of(p_z0f).get('sigma_e_eff_S_cm') == 0.0
            and getattr(RC, 'next_gen_state', lambda s: (None, 'absent'))(s3_of(p_z0f))[0] is None,
            (rc_z0, sorted(s3_of(p_z0f)) if p_z0f else None, _l0.strip()[-200:]))
        #  ── SV 반사실 노브 (DBE 꼴 — SDCP 점 하나가 섬유 옆) ──
        rc_a, log_a, q_a = run_payload(dd, OFF + LEAN2 + CJ + ['--step3-rtol', '1e-12'], out='cf_off.json')
        rc_b, log_b, q_b = run_payload(dd, OFF + LEAN2 + CJ + ['--step3-rtol', '1e-12', '--step3-cjunc-sv-cf'], out='cf_on.json')
        ea, eb = (cj_block(q_a).get('evidence') or {}), (cj_block(q_b).get('evidence') or {})
        svb = (eb.get('solve') or {}).get('sv_counterfactual') or {}
        #  ★ 10-21 (A 병합) — 기록 종류 = producer 정본 상수 (`carbon_junction.CJUNC_SV_CF_KIND` · A v3 = SV 다리만 끊음 · 옛 글자
        #    'counterfactual_cut_sv_faces' = SV 면 전부 = 다른 양) — 시험이 옛 정의 이름을 박아 두지 않는다
        import carbon_junction as _cjm
        chk('SP5 노브 켬 — rc 0 · 증거 요청 {threshold: None} · 기록 (종류 = producer 상수 · 요청 · 상태 · 문턱 None · 표지 None) · '
            'ca_ext_record_ok',
            rc_b == 0 and eb.get('sv_counterfactual_request') == {'threshold': None}
            and svb.get('kind') == getattr(_cjm, 'CJUNC_SV_CF_KIND', 'counterfactual_cut_sv_faces') and svb.get('requested') is True
            and svb.get('status') in ('computed', 'no_through_without_sv') and svb.get('threshold') is None and svb.get('flag') is None
            and RC.ca_ext_record_ok(man_of(q_b)) == (True, None), (rc_b, svb, log_b.strip()[-400:]))
        chk('SP6 노브 켬 = 주 결과 그대로 — σ 비트 같음 · 증서 같음 · p3ca id 같음 · protocol 같음 · 끈 런에는 요청 · 기록 칸 없음',
            rc_a == 0 and s3_of(q_a).get('sigma_e_eff_S_cm') == s3_of(q_b).get('sigma_e_eff_S_cm')
            and man_of(q_a).get('physics_protocol_id') == man_of(q_b).get('physics_protocol_id')
            and cj_block(q_a).get('protocol') == cj_block(q_b).get('protocol')
            and 'sv_counterfactual_request' not in ea and 'sv_counterfactual' not in (ea.get('solve') or {}),
            (s3_of(q_a).get('sigma_e_eff_S_cm'), s3_of(q_b).get('sigma_e_eff_S_cm')))
        if svb.get('status') == 'computed':
            chk('SP7 computed — 비 유한 ≥ 1 (Rayleigh · SV 면을 끊으면 G 가 줄거나 같다) · 끊은 면 수 int ≥ 0 · backend 기록',
                isinstance(svb.get('sv_counterfactual_ratio'), float) and svb['sv_counterfactual_ratio'] >= 1.0 - 1e-12
                and type(svb.get('n_sv_faces_cut')) is int and (svb.get('backend_last_solve') or {}).get('used') in ('cpu', 'gpu'), svb)
        rc_x, log_x, _p = run_payload(dd, OFF + LEAN2 + ['--step3-cjunc-sv-cf'], out='cf_noc.json')
        chk('SP8 노브만 (접합 없이) → 입구 거부 S2_CJUNC_REFUSED|FLAG_WITHOUT_CJUNC|', rc_x != 0 and 'S2_CJUNC_REFUSED|FLAG_WITHOUT_CJUNC|' in log_x,
            (rc_x, log_x.strip()[-200:]))
        #  ── ★ 4판 (10-21 · 1저자 Q1 "권고대로" · 등록 R 4판 §5-0 ①–③ · R4-Q5) 단락 payload 끝-끝 — 실제 J11 단락 (두 층 엇갈림 침대 · 천장) ──
        #     생산자 계약 = 단락은 게시 안 됨 (σ 값 없음 · `conv_cert_problem` = 게시 불가) · 팔 기록 자체는 온전해야 러너가 옮긴다 (check_arm 이
        #     거부하면 러너 rc 1 → 사슬 RUNNER_RC = 사유가 흐려진다) · 사슬 이름 = NOT_COMPUTED · 사유 ELECTRODE_SHORT (+∞ 아님)
        os.makedirs(os.path.join(td, 'thin'))
        th = make_fixture_thin_cross(os.path.join(td, 'thin'))
        TOL1 = dict(tol_ff_um='1.0')
        rc_s, log_s, p_s = run_payload(th, OFF + LEAN2 + cj_with(rj='0', **TOL1) + ['--step3-cjunc-rj-limit', 'zero', '--step3-rtol', '1e-12'],
                                       out='ceil.json')
        s3s = s3_of(p_s)
        cs = s3s.get('conv_cert') or {}
        cnt_s = (cj_block(p_s).get('evidence') or {}).get('counts') or {}
        chk('SP9 천장 (R_j → 0) · 두 층 엇갈림 침대 · rtol — 실제 J11 단락: rc 0 · σ None (0 도 +∞ 도 아님) · 사유 cjunc_electrode_short · 증서 '
            'ELECTRODE_SHORT (early_return · ok False) · 축약 instance 1 · 전자 not_solvable',
            rc_s == 0 and 'sigma_e_eff_S_cm' in s3s and s3s.get('sigma_e_eff_S_cm') is None
            and str(s3s.get('reason', '')).startswith('cjunc_electrode_short') and cs.get('status') == CC.STATUS_SHORT
            and cs.get('zero_source') == 'early_return' and cs.get('ok') is False and cnt_s.get('n_contract') == 1
            and ((man_of(p_s).get('components') or {}).get('electronic') or {}).get('status') == 'not_solvable',
            (rc_s, s3s.get('sigma_e_eff_S_cm'), s3s.get('reason'), cs.get('status'), cnt_s, log_s.strip()[-400:]))
        ngc_ok, ngc_why = RC.next_gen_cert_ok(s3s) if p_s else (None, None)
        chk('SP10 생산자 계약 — 단락 = 게시 불가 (next_gen_cert_ok 거부 · CERT|status| "게시 가능한 상태는 … 뿐") · 기록은 온전 (next_gen_state = short · '
            'ca_ext_record_ok 통과)',
            ngc_ok is False and 'CERT|status|' in str(ngc_why) and RC.next_gen_state(s3s) == ('short', None)
            and RC.ca_ext_record_ok(man_of(p_s)) == (True, None), (ngc_ok, ngc_why, RC.next_gen_state(s3s)))
        r_cs = SC.check_arm(os.path.join(th, 'ceil.json'), 'segment', expect_backend='cpu') if p_s else 'payload 없음'
        chk('SP11 check_arm (러너가 옮기기 전 · 같은 함수) 이 단락 기록을 받는다 — 거부하면 러너 rc 1 → 사슬 RUNNER_RC (사유가 흐려진다)', r_cs is None, r_cs)
        try:
            import rint_r_chain as RRc
            _rs = RRc.registration_state(RC.next_gen_state(s3s)[0])
        except Exception as e:                              # noqa: BLE001 — 고치기 전 (함수 없음) 도 시험 단위로
            _rs = f'{type(e).__name__}: {e}'
        chk('SP12 사슬 이름 (등록 R 4판 §5-0 풀이 상태 셋) — 이 실제 단락 팔 = NOT_COMPUTED · 사유 ELECTRODE_SHORT (σ +∞ 로 판정에 오지 않는다)',
            _rs == ('NOT_COMPUTED', CC.STATUS_SHORT), _rs)
        rc_f, _lf, p_f = run_payload(th, OFF + LEAN2 + cj_with(rj='inf', **TOL1) + ['--step3-cjunc-rj-limit', 'inf', '--step3-rtol', '1e-12'],
                                     out='floor.json')
        rc_q, _lq, p_q = run_payload(th, OFF + LEAN2 + cj_with(rj='1e6', **TOL1) + ['--step3-rtol', '1e-12'], out='q.json')
        sf, sq = s3_of(p_f), s3_of(p_q)
        chk('SP13 같은 침대 대조 — 바닥 (R_j → ∞) = VALID_ZERO_TOPOLOGY (σ 0.0) · R_j 1e6 = POSITIVE_SOLVED (σ > 0) — 단락은 천장 축약에서만',
            rc_f == 0 and rc_q == 0 and sf.get('sigma_e_eff_S_cm') == 0.0 and (sf.get('conv_cert') or {}).get('status') == CC.STATUS_ZERO
            and isinstance(sq.get('sigma_e_eff_S_cm'), float) and sq['sigma_e_eff_S_cm'] > 0.0
            and (sq.get('conv_cert') or {}).get('status') == CC.STATUS_POSITIVE,
            (rc_f, sf.get('sigma_e_eff_S_cm'), (sf.get('conv_cert') or {}).get('status'), rc_q, sq.get('sigma_e_eff_S_cm')))
        #  ── ★ 10-22 (사전 리뷰 2 회차 PRE2-impl-01 · 1저자 Q1 (다)) 못 가른 덩어리 payload 끝-끝 — 판정문 탐침 꼴 (rtol 1e-12 · 증서 켬) ──
        #     옛 판 = 두 섬유 꼴 비 1.0 · computed · 사슬 표지 없음 ↔ 대조 85.42 · SV_DEPENDENT (주 σ 차이 0.02 %)
        import ca_ext_svcf as _SVc
        import rint_r_chain as _RRc

        def _flags(rec):
            return _RRc.sv_assess({('1', 'P0', 'R_j0'): {'sv_cf': _SVc.chain_view(rec)}}, 2.0, 'R_j0')[0]
        os.makedirs(os.path.join(td, 'svu'))
        os.makedirs(os.path.join(td, 'svc'))
        du = make_fixture_sv_unsplit(os.path.join(td, 'svu'), 6.5)
        dc = make_fixture_sv_unsplit(os.path.join(td, 'svc'), 12.5)
        SVK = OFF + LEAN2 + CJ + ['--step3-rtol', '1e-12']
        rc_u, log_u, q_u = run_payload(du, SVK + ['--step3-cjunc-sv-cf'], out='u_on.json')
        rc_u0, _lu0, q_u0 = run_payload(du, SVK, out='u_off.json')
        rc_c, log_c, q_c = run_payload(dc, SVK + ['--step3-cjunc-sv-cf'], out='c_on.json')
        su = ((cj_block(q_u).get('evidence') or {}).get('solve') or {}).get('sv_counterfactual') or {}
        sc = ((cj_block(q_c).get('evidence') or {}).get('solve') or {}).get('sv_counterfactual') or {}
        uu = su.get('upper') if isinstance(su.get('upper'), dict) else {}
        hi_u = (float('inf') if su.get('ratio_limit_hi') == 'inf' else su.get('sv_counterfactual_ratio_hi'))
        chk('SP14 두 섬유가 같은 덩어리를 지남 (payload · 실제 rasterize · 증서 켬) — rc 0 · 못 가른 덩어리 1 · 아래 끝 = 덩어리 그대로 (끊은 면 0 · '
            '비 1 (1e-12) · computed) · 위 끝 = 덩어리를 뺀 판 (비를 싣는 상태 · 비 > 2) · 위 끝 풀이 기록 (뺀 셀 3 · computed 면 그 풀이의 '
            '증서 ok) · ca_ext_record_ok · next_gen_state = positive',
            rc_u == 0 and su.get('n_unsplit_bridging_components') == 1 and su.get('n_sv_faces_cut') == 0 and su.get('status') == 'computed'
            and isinstance(su.get('sv_counterfactual_ratio'), float) and abs(su['sv_counterfactual_ratio'] - 1.0) <= 1e-12
            and su.get('status_hi') in ('computed', 'no_through_without_sv') and isinstance(hi_u, float) and hi_u > 2.0
            and uu.get('status') == su.get('status_hi') and uu.get('n_cells_removed') == 3
            and ((uu.get('status') != 'computed') or ((uu.get('conv_cert') or {}).get('ok') is True))
            and RC.ca_ext_record_ok(man_of(q_u)) == (True, None) and RC.next_gen_state(s3_of(q_u)) == ('positive', None),
            (rc_u, su, log_u.strip()[-300:]))
        chk('SP15 사슬 판정 (문턱 2 · 실제 chain_view · sv_assess) — 두 섬유 꼴 = SV_UNCHECKED (괄호가 문턱에 걸침 · 옛 = 표지 없음) · 대조 (한 섬유만 '
            '지남) = SV_DEPENDENT · 대조 = 못 가른 덩어리 0 · 다시 풀지 않음 (위 = 아래 · 위 끝 기록 None) · ★ 10-23 지위 증서 구간 · 판정 근거 칸 · '
            '기록의 주 해 증서 = 그 런의 step3 주 증서 (사슬 read_run 대조 칸)',
            _flags(su) == ['SV_UNCHECKED'] and rc_c == 0 and _flags(sc) == ['SV_DEPENDENT']
            and sc.get('n_unsplit_bridging_components') == 0 and 'upper' in sc and sc.get('upper') is None
            and sc.get('status_hi') == sc.get('status') and sc.get('sv_counterfactual_ratio_hi') == sc.get('sv_counterfactual_ratio')
            and sc.get('ratio_limit_hi') == sc.get('ratio_limit') and RC.ca_ext_record_ok(man_of(q_c)) == (True, None)
            #  ★ 10-23 (RCA2-01 · Q1 (가)) — 증서 켠 실제 런 = 지위 증서 구간 · 판정 근거 칸 [아래비, 위비] (대조 = 두 끝 다 유한 · 문턱 2 위)
            and su.get('standing') == 'certified_interval' and sc.get('standing') == 'certified_interval'
            and isinstance(sc.get('ratio_cert_interval'), list) and all(isinstance(v, float) and v > 2.0 for v in sc['ratio_cert_interval'])
            #  사슬 read_run 대조 (기록의 주 해 증서 = 이 런의 step3 주 증서 · 판 · 상태 · 게시 판 전류 · 목표량 구간 · 결합 칸) 를 실제 생산자가 지난다
            and all((sx.get('conv_cert_full') or {}).get(k) == (s3_of(qx).get('conv_cert') or {}).get(k)
                    for sx, qx in ((su, q_u), (sc, q_c)) for k in ('version', 'status', 'I_bot', 'target_lo', 'target_hi') + _SVc.BIND_FIELDS),
            (_flags(su), _flags(sc), sc, log_c.strip()[-300:]))
        #  주 증서의 결합 칸 fp_cjunc_rows = 계획 행 지문 — 노브를 켠 계획은 지문에 요청이 들어간다 (`plan_rows_fp` · 10-21 RCA-06 · 노브 끔 = 옛 꼴)
        #  → 그 칸만 빼고 대조 (증서 수 · 상태 · 판정 칸은 같아야 한다)
        _cc_main = lambda q: {k: v for k, v in (s3_of(q).get('conv_cert') or {}).items() if k != 'fp_cjunc_rows'}   # noqa: E731
        chk('SP16 위 끝 풀이는 주 결과를 바꾸지 않는다 — 두 섬유 침대 노브 켬 ↔ 끔: σ 비트 같음 · 주 증서 같음 (계획 행 지문 결합 칸 하나 빼고) · '
            '매니페스트 backend_last_solve 같음 · p3ca id 같음',
            rc_u0 == 0 and s3_of(q_u).get('sigma_e_eff_S_cm') == s3_of(q_u0).get('sigma_e_eff_S_cm')
            and bool(_cc_main(q_u)) and _cc_main(q_u) == _cc_main(q_u0)
            and man_of(q_u).get('backend_last_solve') == man_of(q_u0).get('backend_last_solve')
            and man_of(q_u).get('physics_protocol_id') == man_of(q_u0).get('physics_protocol_id'),
            (s3_of(q_u).get('sigma_e_eff_S_cm'), s3_of(q_u0).get('sigma_e_eff_S_cm')))
    finally:
        shutil.rmtree(td, ignore_errors=True)


# ═════════════════════════ B 묶음 — 끔 비트 동일 (고치기 전 코드 대조) ═════════════════════════
#: ★ 10-21 (D · 브리프 묶음 5) — `--old-scripts` 대조에서 나와도 되는 칸 (한 곳 · z3 O 묶음도 이 표 · 함수를 쓴다).
#:   한 줄 = (세대, 연산, 경로 정규식 (전체 일치), 경우 표지, 사유) — 연산 '+' 새 칸 · '-' 없어진 칸 · '~' 값 바뀜 ·
#:   경로 = payload step3 를 {'manifest': 매니페스트 (code_sha · exec_env 빼고), 그 밖 step3 칸} 으로 본 점 경로.
#:   경우 표지 = 그 칸이 나와도 되는 켠 노브 (face_alpha · rtol · cjunc) — 노브를 다 끈 경우 (off · centerline · LEAN 3) 에는
#:   어떤 칸도 허용되지 않는다 (끈 경로 비트 같음).  σ · n_dof · CG 결과 칸은 표에 없다 = 언제나 실패.
#:   세대: Z3 = 기반이 ff9d72afe (Z3) 이전일 때 · RCA1 = 기반 47d23baba ↔ a76f59d0d (Codex RCA 수정 1 회차 — B 증서 v2 · S1 부피 ·
#:   A 접합 v2) · RCA2 = a76f59d0d 뒤 B 의 증서 ↔ 런 결합 (PRE-impl-07) · A 의 접합 v3 (PRE-impl-01–06 · Q-A–Q-D).  ⚠ 새 칸을 더하는
#:   묶음은 같은 커밋에서 이 표에 한 줄 (세대 표지) 을 올린다 · 바로 앞 기반과는 `--expect-identical`.
OLD_DIFF_ALLOW = (
    ('Z3', '+', r'manifest\.ca_ext\.ptfe_face\.evidence\.fp\.sid_off', 'face_alpha', 'off 격자 sid 지문 (Z3)'),
    ('Z3', '+', r'(ion_)?cg_iters', 'rtol', 'CG 반복 수 (Z3)'),
    ('Z3', '+', r'(ion_)?conv_cert\.(iters|resolve_iters)', 'rtol', '증서 반복 수 (Z3)'),
    ('RCA1', '+', r'(ion_)?conv_cert\.(status|pass_d|scale|target_[A-Za-z0-9_]+)', 'rtol',
     'B 증서 v2 — 상태 (§5-0) · ⓓ 목표량 증서 (RCA-07 · RCA-13)'),
    ('RCA1', '~', r'(ion_)?conv_cert\.version', 'rtol', 'B 증서 판 conv-cert-v1 → v2'),
    ('RCA1', '+', r'manifest\.ca_ext\.ptfe_face\.evidence\.capsules\.volume_basis', 'face_alpha', 'B S1 캡슐 부피 기준'),
    ('RCA1', '+', r'manifest\.ca_ext\.ptfe_face\.evidence\.exempt_assumptions', 'face_alpha', 'B S1 면제 가정 표'),
    ('RCA1', '+', r'manifest\.ca_ext\.ptfe_face\.evidence\.faces\.[A-Za-z_]+\.alpha_(zero_faces|zero_open_at_refine|refine_K)',
     'face_alpha', 'B S1 α 0 면 진단'),
    ('RCA1', '+', r'manifest\.ca_ext\.ptfe_face\.evidence\.volume\.(capsule_nominal_um3|capsule_union_um3|capsule_union_status|'
                  r'capsule_volume_basis|ratio_basis)', 'face_alpha', 'B S1 캡슐 부피 칸'),
    ('RCA1', '+', r'manifest\.ca_ext\.cjunc\.evidence\.census\.(n_instances_ptfe_partial|n_revisit_(cells|fibres|pairs)|'
                  r'n_self_revisits_path_only|n_subedges(_long|_ptfe_cov|_sdcp_near|_unrealized)?|revisit_s_um|subedge_rule)', 'cjunc',
     'A 접합 v2 census — 가지 · 같은 셀 재방문 (RCA-03) · 분산판 v0 (RCA-05)'),
    ('RCA1', '-', r'manifest\.ca_ext\.cjunc\.evidence\.(census|solve)\.n_self_merged_revisits', 'cjunc', 'A 재방문 합침 철회 (RCA-03)'),
    ('RCA1', '+', r'manifest\.ca_ext\.cjunc\.evidence\.solve\.n_self_revisits_path_only', 'cjunc', 'A 경로로만 본 재방문 수'),
    ('RCA1', '+', r'manifest\.ca_ext\.cjunc\.evidence\.counts\.n_subedges', 'cjunc', 'A 분산판 v0 간선 수'),
    ('RCA1', '~', r'manifest\.ca_ext\.cjunc\.evidence\.(fp\.(plan_rows|registry)|receipts\.[A-Za-z_]+\.fp_registry|qualifiers)',
     'cjunc', 'A 접합 계획 · 원장 지문 · 한정어 (판 v2)'),
    ('RCA1', '-', r'manifest\.ca_ext\.cjunc\.evidence\.solve\.sv_dominant', 'cjunc', 'A SV_DOMINANT 철회 (RCA-06)'),
    ('RCA1', '+', r'manifest\.ca_ext\.cjunc\.evidence\.solve\.sv_local_dissipation', 'cjunc', 'A SV 국소 소산 진단 (RCA-06)'),
    ('RCA1', '~', r'manifest\.ca_ext\.cjunc\.protocol\.(model|schema|rules\.(port|self))', 'cjunc', 'A 접합 규약 판 v2'),
    ('RCA1', '+', r'manifest\.ca_ext\.cjunc\.protocol\.rules\.(branch|cp|dist|order)', 'cjunc',
     'A 접합 규칙 v2 (가지 · 최근접점 · 분산판 · 순서)'),
    ('RCA1', '~', r'manifest\.physics_protocol_id', 'cjunc', 'A 접합 규약 판이 바뀌면 p3ca id 가 바뀐다 (같은 함수로 다시 계산)'),
    #  RCA2 · B — 증서 ↔ 런 결합 (사전 리뷰 PRE-impl-07 · `step3_conv_cert.bind_record` · 판 cert-bind-v1) — 증서를 켠 경우만 · 새 칸만
    ('RCA2', '+', r'(ion_)?conv_cert\.(bind_version|fp_sid|fp_sig|fp_face_plan|fp_cjunc_registry|fp_cjunc_rows)', 'rtol',
     'B 증서 ↔ 런 결합 칸 (PRE-impl-07)'),
    #  RCA2 · A — 접합 v3 (사전 리뷰 PRE-impl-01–06 · 1저자 Q-A–Q-D · 모델 r3-carbon-junction-port-v3) — 접합 경우만 · σ 는 표에 없다
    ('RCA2', '+', r'manifest\.ca_ext\.cjunc\.evidence\.census\.(n_bridging_components|n_closed_paths_joined|n_instances_same_fid_pieces|'
                  r'n_piece_cell_meets|n_ring_pieces|n_sdcp_components_touching|n_seam_alias|n_self_revisits_path_broken|'
                  r'n_sv_faces_cut_rows|n_sv_faces_kept_self|n_unsplit_bridging_components|piece_rule|sv_cf_rule)', 'cjunc',
     'A 접합 v3 census — 조각 = 섬유 · 고리 이음매 · 자기 = 중심선 근접 (Q-A · Q-B) · SV 다리 (Q-D)'),
    ('RCA2', '~', r'manifest\.ca_ext\.cjunc\.evidence\.fp\.(centreline|membership)', 'cjunc',
     'A 접합 v3 원장 입력 지문 (조각 · 덮인 포트 = 옮기지 않음 · Q-A · Q-C)'),
    ('RCA2', '+', r'manifest\.ca_ext\.cjunc\.protocol\.rules\.(piece|sv_cf)', 'cjunc', 'A 접합 규칙 v3 (조각 · SV 반사실 = 다리만)'),
    ('RCA2', '~', r'manifest\.ca_ext\.cjunc\.protocol\.rules\.(self_lc|self_s)', 'cjunc', 'A 자기 접합 규칙 v2 (접합 쌍 · 가장 가까운 점)'),
)
#: 허용이 아니라 이유만 붙이는 칸 (기반 사본의 환경 차이 — 고치는 길: 사본 옆에 docs/ 두기 · 링크)
OLD_DIFF_HINTS = (
    (r'collector\.(anchors_source|pristine_precision)', '기반 사본 옆에 docs/ 가 없다 (집전체 앵커 CSV 를 못 읽어 대체 값) — '
                                                       '<사본>/../docs 를 리포 docs/ 로 링크'),
)


def old_tree_diff(a, b, p=''):
    """두 JSON 꼴 값의 차이 → [(연산, 점 경로)] (경로 순).  양쪽 다 dict 일 때만 내려간다 · 목록 · 값은 통째로 JSON 바이트 비교
    (1 ↔ 1.0 도 다름 · NaN 끼리 같음).  '+' = 새 쪽에만 · '-' = 옛 쪽에만 · '~' = 값 다름."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            q = f'{p}.{k}' if p else str(k)
            if k not in a:
                out.append(('+', q))
            elif k not in b:
                out.append(('-', q))
            else:
                out += old_tree_diff(a[k], b[k], q)
    elif json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
        out.append(('~', p))
    return out


def case_tags(extra):
    """payload 인자 → 켠 노브 표지 집합 (face_alpha · rtol · cjunc) — 허용 목록의 경우 표지와 같은 낱말."""
    ex = list(extra)
    tags = set()
    for i, a in enumerate(ex):
        if a == '--ptfe-stamp' and i + 1 < len(ex) and ex[i + 1] == 'face_alpha':
            tags.add('face_alpha')
        elif a == '--step3-rtol':
            tags.add('rtol')
        elif a == '--step3-cjunc':
            tags.add('cjunc')
    return tags


def old_diff_problems(diffs, tags, expect_identical=False):
    """차이 목록 → (문제 목록, 허용된 칸 [(세대, 연산, 경로)]).  tags = 이 경우에 켠 노브.  expect_identical = 표를 안 쓰고 차이 0 만."""
    import re as _re
    probs, seen = [], []
    for op, path in diffs:
        if expect_identical:
            probs.append(f'{op} {path} (--expect-identical: 차이 0 이어야)')
            continue
        hit = [g for g, o, rx, t, _why in OLD_DIFF_ALLOW if o == op and t in tags and _re.fullmatch(rx, path)]
        if hit:
            seen.append((hit[0], op, path))
            continue
        hint = next((h for rx, h in OLD_DIFF_HINTS if _re.fullmatch(rx, path)), '')
        probs.append(f'{op} {path} (허용 목록 밖{" · " + hint if hint else ""})')
    return probs, seen


def payload_tree(data):
    """payload 결과 → 대조 나무 {'manifest': 매니페스트 (code_sha · exec_env 빼고), 그 밖 step3 칸} (B1 · z3 O2 같은 꼴)."""
    m = dict(man_of(data))
    for k in ('code_sha', 'exec_env'):
        m.pop(k, None)
    t = {k: v for k, v in s3_of(data).items() if k != 'manifest'}
    t['manifest'] = m
    return t


@case('B0u --old-scripts 대조의 경로 차이 · 허용 목록 (합성 · 기반 사본 없이 · ★ 10-21 D 브리프 묶음 5)')
def t_old_allow_unit():
    import re as _re
    f_diff, f_prob = globals().get('old_tree_diff'), globals().get('old_diff_problems')
    f_tags, table = globals().get('case_tags'), globals().get('OLD_DIFF_ALLOW')
    ok = callable(f_diff) and callable(f_prob) and callable(f_tags) and isinstance(table, tuple) and len(table) > 0
    chk('B0u-0 도구 (old_tree_diff · old_diff_problems · case_tags · OLD_DIFF_ALLOW) 가 한 곳 (이 파일 · z3 O 묶음이 import)', ok,
        (callable(f_diff), callable(f_prob), callable(f_tags), type(table).__name__))
    if not ok:
        return
    d = f_diff({'a': {'b': 1, 'c': [1], 'x': 1}, 'd': 2, 'f': {'g': 1}}, {'a': {'b': 1, 'c': [1, 2], 'e': 3, 'x': 1.0}, 'f': 5})
    chk('B0u-1 경로 차이 — 양쪽 dict 일 때만 내려감 · 목록 통째 · 새 칸 + · 없어진 칸 − · 값 ~ (1 ↔ 1.0 도 다름 = 바이트 기준) · 경로 순',
        d == [('~', 'a.c'), ('+', 'a.e'), ('~', 'a.x'), ('-', 'd'), ('~', 'f')], d)
    chk('B0u-2 같은 값 = 차이 없음 (NaN 끼리 · 키 순서 무관)', f_diff({'a': float('nan'), 'b': {'y': 1, 'x': 2}},
                                                                {'b': {'x': 2, 'y': 1}, 'a': float('nan')}) == [])
    off, fa, rt, cj = (f_tags(x) for x in (['--ptfe-stamp', 'off'], ['--ptfe-stamp', 'face_alpha', '--step3-rtol', '1e-12'],
                                           ['--step3-rtol', '1e-12'], ['--step3-cjunc', '--step3-cjunc-rj-ohm', '1e6']))
    chk('B0u-3 경우 표지 — off = 없음 · face_alpha + rtol = 둘 · cjunc', off == set() and fa == {'face_alpha', 'rtol'}
        and rt == {'rtol'} and 'cjunc' in cj and 'face_alpha' not in cj, (off, fa, rt, cj))
    SID = 'manifest.ca_ext.ptfe_face.evidence.fp.sid_off'
    cases = (
        ('Z3 sid_off — face_alpha 경우', [('+', SID)], {'face_alpha'}, 0, 1),
        ('Z3 sid_off — 끈 경우 (off) = 실패', [('+', SID)], set(), 1, 0),
        ('Z3 sid_off — rtol 경우 = 실패 (표지 밖)', [('+', SID)], {'rtol'}, 1, 0),
        ('sid_off 꼬리 붙은 경로 = 실패 (전체 일치)', [('+', SID + '_extra')], {'face_alpha'}, 1, 0),
        ('sid_off 없어짐 (−) = 실패 (연산 다름)', [('-', SID)], {'face_alpha'}, 1, 0),
        ('CG 반복 수 + 증서 반복 수 — rtol', [('+', 'cg_iters'), ('+', 'conv_cert.iters'), ('+', 'ion_conv_cert.resolve_iters')],
         {'rtol'}, 0, 3),
        ('증서 v2 칸 · 판 — rtol', [('+', 'conv_cert.status'), ('+', 'conv_cert.target_lo'), ('~', 'conv_cert.version')], {'rtol'}, 0, 3),
        ('증서 판 없어짐 (−) = 실패', [('-', 'conv_cert.version')], {'rtol'}, 1, 0),
        ('σ 값 바뀜 = 언제나 실패', [('~', 'sigma_e_eff_S_cm')], {'face_alpha', 'rtol', 'cjunc'}, 1, 0),
        ('S1 부피 · 면 α 진단 — face_alpha', [('+', 'manifest.ca_ext.ptfe_face.evidence.volume.capsule_union_um3'),
                                          ('+', 'manifest.ca_ext.ptfe_face.evidence.faces.electronic.alpha_zero_faces')], {'face_alpha'}, 0, 2),
        ('S1 부피 칸 — cjunc 만 켠 경우 = 실패', [('+', 'manifest.ca_ext.ptfe_face.evidence.volume.ratio_basis')], {'cjunc'}, 1, 0),
        ('접합 SV 이름 바뀜 — cjunc', [('-', 'manifest.ca_ext.cjunc.evidence.solve.sv_dominant'),
                                   ('+', 'manifest.ca_ext.cjunc.evidence.solve.sv_local_dissipation')], {'cjunc'}, 0, 2),
        ('p3ca id 바뀜 — cjunc 만 · face_alpha 는 실패', [('~', 'manifest.physics_protocol_id')], {'face_alpha'}, 1, 0),
        ('접합 칸 — 끈 경우 = 실패', [('+', 'manifest.ca_ext.cjunc.evidence.counts.n_subedges')], set(), 1, 0),
    )
    for nm, diffs, tags, n_bad, n_seen in cases:
        probs, seen = f_prob(diffs, tags)
        chk(f'B0u-4 [{nm}] — 문제 {n_bad} · 허용 {n_seen}', len(probs) == n_bad and len(seen) == n_seen, (probs, seen))
    probs, _seen = f_prob([('+', SID)], {'face_alpha'}, expect_identical=True)
    chk('B0u-5 --expect-identical = 허용 목록을 안 쓴다 (허용 칸도 실패)', len(probs) == 1, probs)
    probs, _seen = f_prob([('~', 'collector.anchors_source')], set())
    chk('B0u-6 기반 사본 환경 차이 (docs/ 없음 → 집전체 앵커 대체) = 실패 + 이유 표시 (허용 아님)',
        len(probs) == 1 and 'docs' in probs[0], probs)
    bad_rx = []
    for row in table:
        try:
            _re.compile(row[2])
        except Exception as e:                              # noqa: BLE001 — 표 결함은 실패로 기록
            bad_rx.append((row[2], f'{type(e).__name__}: {e}'))
    chk('B0u-7 표 꼴 — (세대, 연산 ∈ {+,−,~}, 정규식, 경우 표지 ∈ {face_alpha, rtol, cjunc}, 사유) · 정규식 컴파일',
        not bad_rx and all(len(r) == 5 and r[1] in ('+', '-', '~') and r[3] in ('face_alpha', 'rtol', 'cjunc') and r[4] for r in table),
        bad_rx)


@case('B 끔 비트 동일 — 고치기 전 payload 와 대조 (--old-scripts)')
def t_bitid():
    if not ARGS.old_scripts:
        print('    (--old-scripts 없음 — 건너뜀 · 커밋 증거는 그 인자로 돌린 기록)')
        return
    import glob
    import importlib.util
    _spec = importlib.util.spec_from_file_location('run_contract_old', os.path.join(ARGS.old_scripts, 'run_contract.py'))
    _old = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_old)
    _all = [json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(ROOT, 'docs/data/**/run_receipt.json'),
                                                                         recursive=True))]
    chk(f'B0 커밋된 영수증 {len(_all)} 개 — 새 receipt_digest = 고치기 전 함수 (OUTDIR 이름 · 코호트 디렉터리 보존)',
        len(_all) >= 40 and all(RC.receipt_digest(r) == _old.receipt_digest(r) for r in _all))
    _pairs = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'docs/data/**/run_receipt.json'), recursive=True)):
        for p in sorted(glob.glob(os.path.join(os.path.dirname(f), 'p2_*.json')))[:2]:
            _pj = json.load(open(p, encoding='utf-8'))
            _mm = ((_pj.get('step3') or (_pj.get('mpm_metrics') or {}).get('step3') or {}).get('manifest'))
            if isinstance(_mm, dict):
                _pairs.append((json.load(open(f, encoding='utf-8')), _mm))
    chk(f'B0b 커밋된 영수증 ↔ 같은 디렉터리 팔 {len(_pairs)} 짝 — receipt_match 판정이 고치기 전과 같다',
        len(_pairs) > 10 and all(RC.receipt_match(r, m) == _old.receipt_match(r, m) for r, m in _pairs))
    if ARGS.skip_payload:
        return
    td = tempfile.mkdtemp(prefix='b6_b_')
    try:
        os.makedirs(os.path.join(td, 'w'))
        d = make_fixture(os.path.join(td, 'w'), sdcp=True)
        #  ★ 10-21 (D · 브리프 묶음 5) — 옛 판은 Z3 새 칸 (sid_off · cg_iters · iters) 을 새 쪽에서만 빼서 Z3 이전 기반에서만 맞았다.
        #    이제 경로 차이 전부를 한 표 (OLD_DIFF_ALLOW) 로 판정한다: 끈 경우 = 차이 0 · 켠 경우 = 그 노브 표지의 칸만 ·
        #    --expect-identical (바로 앞 기반) = 차이 0.  접합 · face_alpha + rtol 경우를 더했다 (A · B 새 칸이 나오는 자리).
        for nm, extra in (('off LEAN2', OFF + LEAN2), ('centerline LEAN2', ['--ptfe-stamp', 'centerline'] + LEAN2),
                          ('off LEAN3', OFF + LEAN3), ('face_alpha LEAN2', ['--ptfe-stamp', 'face_alpha'] + LEAN2),
                          ('off LEAN2 + rtol 1e-12', OFF + LEAN2 + ['--step3-rtol', '1e-12']),
                          ('off LEAN2 + 접합', OFF + LEAN2 + CJ),
                          ('face_alpha LEAN2 + rtol', ['--ptfe-stamp', 'face_alpha'] + LEAN2 + ['--step3-rtol', '1e-12'])):
            tag = f'{len(nm)}_{sum(map(ord, nm)) % 99991}'
            r_old = run_payload(d, extra, out=f'old_{tag}.json', payload=os.path.join(ARGS.old_scripts, 'mpm_webapp_payload.py'))
            r_new = run_payload(d, extra, out=f'new_{tag}.json')
            diffs = old_tree_diff(payload_tree(r_old[2]), payload_tree(r_new[2]))
            _ident = bool(getattr(ARGS, 'expect_identical', False))
            probs, seen = old_diff_problems(diffs, case_tags(extra), expect_identical=_ident)
            gens = sorted({g for g, _o, _p in seen})
            chk(f'B1 payload [{nm}] — 기반 ↔ 새: 차이가 허용 목록 (경우 표지 {sorted(case_tags(extra)) or "끔"}) 안'
                + (' · --expect-identical = 차이 0' if _ident else f' · 허용된 칸 {len(seen)} (세대 {gens or "-"})'),
                r_old[0] == 0 and r_new[0] == 0 and not probs, (r_old[0], r_new[0], probs[:6]))
    finally:
        shutil.rmtree(td, ignore_errors=True)


def main():
    global RC, CW, ARGS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--old-scripts', default='', help='고치기 전 scripts/ 사본 (B 묶음 · 끔 비트 동일 대조 · 사본 옆에 docs/ 링크)')
    ap.add_argument('--expect-identical', action='store_true',
                    help='B 묶음 — 허용 목록을 쓰지 않고 차이 0 만 통과 (기반 = 바로 앞 커밋 · 끈 · 켠 경우 모두)')
    ap.add_argument('--skip-payload', action='store_true')
    ap.add_argument('--only', default='', help='쉼표로 나눈 이름 접두 (예: R,P)')
    ARGS = ap.parse_args()
    import run_contract as _rc
    RC = _rc
    try:
        import ca_ext_cjunc as _cw
        CW = _cw
    except Exception as e:                                  # noqa: BLE001 — 구현 전 (모듈 없음) 도 시험 단위로 기록
        print(f'  ⚠ ca_ext_cjunc 를 못 불러온다 ({type(e).__name__}: {e})')
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    for tag, fn in CASES:
        if only and not any(tag.startswith(o) for o in only):
            continue
        print(f'\n── {tag}')
        try:
            fn()
        except Exception as e:                              # noqa: BLE001 — 옛 코드 (API 없음) 도 시험 단위로 기록
            chk(f'{tag.split()[0]}: 실행', False, f'{type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()

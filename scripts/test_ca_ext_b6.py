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
  B  (--old-scripts) 끔 비트 동일 — payload 매니페스트 (code_sha · exec_env 빼고) · step3 값 (★ Z3 새 기록 칸 = face_alpha 런의
     `ca_ext.ptfe_face.evidence.fp.sid_off` · rtol 런의 CG 반복 수 `step3.cg_iters` · 증서 `iters` · `resolve_iters` 만 빼고 대조)
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
    fp = {'registry': 'r' * 32, 'sid': 's' * 32, 'plan_rows': 'p' * 32}
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


def good_cert(sigma, rtol=1.0e-12):
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
            'target_hi': 1.0, 'scale': float(sigma)}


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
    chk('R13a 증서 정상 → 문제 없음', RC.conv_cert_problem(good_cert(0.05), 0.05) is None, RC.conv_cert_problem(good_cert(0.05), 0.05))
    for nm, fn in (('없음', lambda c: None), ('ok False', lambda c: dict(c, ok=False)),
                   ('ok ↔ pass 모순', lambda c: dict(c, pass_b=False)),
                   ('판 rtol 1e-8 (봉인 상한 밖) 인데 pass_a', lambda c: dict(c, rtol_used=1e-8)),
                   ('불균형 문턱 밖 인데 pass_b', lambda c: dict(c, imbalance=1e-3)),
                   ('이어 풀기 Δσ 문턱 밖 인데 pass_c', lambda c: dict(c, dsigma_rel=1e-3)),
                   ('다른 판본', lambda c: dict(c, version='conv-cert-v0')), ('봉인 상한 손으로', lambda c: dict(c, rtol_max=1e-8)),
                   ('σ ≠ 결과 σ (증서 ↔ 결과 결합)', lambda c: dict(c, sigma=0.06)), ('NaN 불균형', lambda c: dict(c, imbalance=float('nan'))),
                   ('pass 가 문자열', lambda c: dict(c, pass_a='True'))):
        chk(f'R13b 증서 거부 [{nm}]', RC.conv_cert_problem(fn(good_cert(0.05)), 0.05) is not None)
    s3 = {'sigma_e_eff_S_cm': 0.05, 'manifest': m, 'conv_cert': good_cert(0.05)}
    chk('R13c 다음 세대 게시 조건 — p3ca + 증서 정상 = 통과 · 증서 없음 = 미게시 · p2 (옛 세대) = 해당 없음 (통과)',
        RC.next_gen_cert_ok(s3)[0] and not RC.next_gen_cert_ok({k: v for k, v in s3.items() if k != 'conv_cert'})[0]
        and RC.next_gen_cert_ok({'sigma_e_eff_S_cm': 0.05, 'manifest': cohort_manifests()[0]})[0])
    s3i = dict(s3, manifest=cj_manifest(ionic_plan=True), sigma_ion_eff_S_cm=0.001)
    s3i['manifest']['components'] = dict(s3i['manifest'].get('components') or {}, ionic={'status': 'complete'})
    chk('R13d 이온을 푼 다음 세대 팔은 이온 증서도 요구 (없으면 미게시 · 있으면 통과)',
        not RC.next_gen_cert_ok(s3i)[0] and RC.next_gen_cert_ok(dict(s3i, ion_conv_cert=good_cert(0.001)))[0])
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
            and RC.ca_ext_record_ok(mfr) == (True, None) and RC.conv_cert_problem(cert, s3_of(p_fr).get('sigma_e_eff_S_cm')) is None,
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
            and RC.conv_cert_problem(cert2, s3_of(p_cr).get('sigma_e_eff_S_cm')) is None and RC.next_gen_cert_ok(s3_of(p_cr))[0],
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


# ═════════════════════════ B 묶음 — 끔 비트 동일 (고치기 전 코드 대조) ═════════════════════════
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
        for nm, extra in (('off LEAN2', OFF + LEAN2), ('centerline LEAN2', ['--ptfe-stamp', 'centerline'] + LEAN2),
                          ('off LEAN3', OFF + LEAN3), ('face_alpha LEAN2', ['--ptfe-stamp', 'face_alpha'] + LEAN2),
                          ('off LEAN2 + rtol 1e-12', OFF + LEAN2 + ['--step3-rtol', '1e-12'])):
            r_old = run_payload(d, extra, out=f'old_{nm.replace(" ", "_")}.json',
                                payload=os.path.join(ARGS.old_scripts, 'mpm_webapp_payload.py'))
            r_new = run_payload(d, extra, out=f'new_{nm.replace(" ", "_")}.json')
            m_old = dict(man_of(r_old[2]))
            m_new = dict(man_of(r_new[2]))
            for k in ('code_sha', 'exec_env'):
                m_old.pop(k, None)
                m_new.pop(k, None)
            s_old = {k: v for k, v in s3_of(r_old[2]).items() if k != 'manifest'}
            s_new = {k: v for k, v in s3_of(r_new[2]).items() if k != 'manifest'}
            #  ★ Z3 — 새 기록 칸 (켠 노브에서만 · 그 밖은 바이트 같아야 한다): face_alpha 런의 off 격자 sid 지문 · rtol (증서) 런의 CG 반복 수
            new_flds = []
            _fp = (((m_new.get('ca_ext') or {}).get('ptfe_face') or {}).get('evidence') or {}).get('fp')
            if isinstance(_fp, dict) and 'sid_off' in _fp:
                _fp.pop('sid_off')
                new_flds.append('fp.sid_off')
            for _k in ('cg_iters', 'ion_cg_iters'):
                if _k in s_new:
                    s_new.pop(_k)
                    new_flds.append(_k)
            for _ck in ('conv_cert', 'ion_conv_cert'):
                if isinstance(s_new.get(_ck), dict) and {'iters', 'resolve_iters'} & set(s_new[_ck]):
                    s_new[_ck] = {k: v for k, v in s_new[_ck].items() if k not in ('iters', 'resolve_iters')}
                    new_flds.append(f'{_ck}.iters')
            want_new = {'face_alpha LEAN2': ['fp.sid_off'], 'off LEAN2 + rtol 1e-12': ['cg_iters', 'conv_cert.iters']}.get(nm, [])
            diff = sorted(k for k in set(m_old) | set(m_new) if m_old.get(k) != m_new.get(k))
            chk(f'B1 payload [{nm}] — 매니페스트 (code_sha · exec_env 빼고) 바이트 같음 · id 같음 · step3 값 같음'
                + (f' (새 기록 칸 {want_new} 만 빼고)' if want_new else ' (새 기록 칸 없음)'),
                r_old[0] == 0 and r_new[0] == 0 and json.dumps(m_old, sort_keys=True) == json.dumps(m_new, sort_keys=True)
                and s_old == s_new and new_flds == want_new, (r_old[0], r_new[0], diff[:6], new_flds))
    finally:
        shutil.rmtree(td, ignore_errors=True)


def main():
    global RC, CW, ARGS
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--old-scripts', default='', help='고치기 전 scripts/ 사본 (B 묶음 · 끔 비트 동일 대조)')
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

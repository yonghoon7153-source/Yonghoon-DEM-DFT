#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② B6 — payload 배선: 탄소 접합 (S2 `cjunc`) · SDCP 접합 수정자 (S3 `sdcp_mod`) → 다음 세대 블록 `ca_ext` 의 하위 블록
(2026-10-20 · 기본 끔 · 시험 = `scripts/test_ca_ext_b6.py`).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §4-2 · §5-2 (스위치 · 출력) · §7 (세대 · 영수증 · LEAN 표) ·
등록 R 초안 §2-1 (문턱 식 · L_par · r_port = 0.30 µm 지금 고정 · tol_ff · s_min = S0 단계 1 의 숫자 · 기본값 없음).
기구 = `carbon_junction` (`cjunc_registry` → `cjunc_plan` → `solve_sigma_z(cjunc=plan)`) — 그 API 를 그대로 부르고 그 파일은 고치지 않는다.

  · 요청 = 매니페스트 최상위 `ca_ext_requested` (정렬 목록 · 켰을 때만 · S1 의 요청은 `ptfe_stamp = face_alpha` 그대로)
  · 하위 블록 = {'protocol' (p3ca id 에 들어가는 물리 칸 — 검증기가 이 코드의 정본으로 다시 만들어 대조), 'evidence' (원장 수 · 솔브 기록 ·
    네 솔브 영수증 · 지문 · 진단 표 · 표지)}
  · 검증기 `cjunc_block_problem` · `sdcp_mod_block_problem` = `run_contract.ca_ext_record_ok` 가 producer (게시 전) · `check_arm` ·
    판정기에서 같이 부른다 (사본 없음 · `run_contract.CA_EXT_SUBBLOCKS` 등록)
⛔ 지위 = 기구 · 배선만 — R_j 는 모형 내부 보정값 (재료값 아님) · 정량 판정 = 등록 R 비준 · Codex GO · S0 문턱 개정 뒤.
⛔ face_alpha (S1) + cjunc (S2) 한 런 = 거부 (설계가 조합을 정의하지 않았다 · `solve_sigma_z` 와 같은 규칙) → P1 (덮인 접합 절단) 도
  지금은 닿지 않는다 (P1 = face_alpha 에서만).
"""
import math

import numpy as np

import carbon_junction as CJ

WIRING_VERSION = 'b6-cjunc-payload-v1'
SUB_CJUNC = 'cjunc'
SUB_SDCP = 'sdcp_mod'
#: 문턱 — 식 = 등록 R §2-1 (지금 고정).  r_f = 생산 VGCF Ø0.15 µm (규약 고정 · 설계 §1-2 #3) · L_par = 2(r_fi + r_fj) · r_port = 물리 단위.
R_F_UM = CJ.VGCF_R_UM
L_PAR_UM = 0.30
R_PORT_UM = 0.30
GAP_TOL = 2.0                                  # 폴리라인 끊기 = 선분 스탬프와 같은 규칙 (설계 §1-2 #25)
#: 원장이 읽는 MPM phase — VGCF (중심선 · 멤버십) · PTFE (P-junc 덮임) · SDCP (S3 근접)
ADD_PHASES = (2, 4, 5)
CHANNEL = 'electronic'
SOLVES = ('electronic_main', 'electronic_wetted', 'electronic_bare', 'ionic')   # = run_contract.INTERFACE_SOLVES 키
OK_STATUSES = ('applied', 'absent_geometry', 'failed', 'disabled', 'not_requested')   # run_contract.INTERFACE_OK_STATUSES 부분
#: 러너 · `--expect-physics` 가 선언하는 칸 (= 이 런이 고른 값 · 나머지 protocol 칸은 이 코드의 상수)
REQUEST_KEYS_CJUNC = ('R_j_ohm', 'len_law', 'unreg_law', 's_min_um', 'tol_ff_um', 'ptfe_jlaw')
REQUEST_KEYS_SDCP = ('c',)
SDCP_RULE = "R_j' = R_j,0 (1 - c a_j) · c = 1 = 근접 instance 축약 경로 (union-find · 큰 g 대입 아님)"
#: protocol 정본 키 (규칙 M `protocol_ext` 회계가 이 이름을 센다 · `run_contract.ca_ext_protocol_fields`)
CJUNC_PROTOCOL_KEYS = ('wiring', 'model', 'schema', 'len_law', 'rules', 'R_j_ohm', 'unreg_law', 'ptfe_jlaw', 'ptfe_stamp',
                       'r_f_um', 'tol_ff_um', 'L_par_um', 'r_port_um', 's_min_um', 'gap_tol', 'tol_P_um', 'tol_sj_um',
                       'r_ptfe_um', 'r_sdcp_um', 'rj_reference_plane', 'half_cell_in_edge', 'quantitative', 'allow_rj_limits',
                       'channel')
SDCP_MOD_PROTOCOL_KEYS = ('wiring', 'model', 'c', 'tol_sj_um', 'r_sdcp_um', 'rule')
#: 표지 (설계 §4-6 · §5-6) — 웹앱 템플릿은 매니페스트의 이 문자열을 **읽어** 띄운다 (사본을 두지 않는다)
LABEL_CJUNC = ('탄소 접합 R_j (모형 내부 보정값 · 재료값 아님 · VGCF–VGCF 만 · VGCF–AM · SDCP–VGCF 접점 = 옛 융합 '
               '(SDCP–VGCF 접촉 저항 0 가정))')
LABEL_SDCP = ('SDCP 접점 시나리오 c ∈ {0 · 1} — 재료 예측 아님 · 젖음 효과 없음 ↔ 근접 접합 축약 끝 '
              '(같은 그래프 · SDCP–VGCF 접촉 저항 0 가정)')
#: v0 진단 표 — 면 · 접합 간선 원장을 읽지 않는 진단은 안 낸다 (E2) · 소산 분담 = 원장을 읽는 기록만 (evidence.solve)
DIAGNOSTICS_V0 = {'je': 'not_computed', 'dissipation_share_step3': 'not_computed (원장을 안 읽는다 · E2)',
                  'dissipation_share_ledger': 'evidence.solve.dissipation_share', 'field': 'refused', 'joule': 'refused',
                  'step4_grid': 'refused', 'phi_profile_electronic': 'not_computed'}
#: 원장 · 계획 수 (cjunc_plan 기록 counts) 중 정수 칸
_COUNT_INT = ('n_instances', 'n_edge', 'n_contract', 'n_cut_p1', 'n_unrealized', 'n_none_inf', 'n_long', 'n_sdcp_near',
              'n_contracted_by_c', 'n_ptfe_cov')
#: 솔브 기록 (res['cjunc']) 에서 증거로 옮기는 칸
_SOLVE_KEYS = ('solved', 'reason', 'n_extra_dofs', 'n_contracted', 'n_floating_dropped', 'n_through_dof', 'n_plate_reachable_dof',
               'short', 'tombstones', 'n_unreg_fused', 'n_junction_edges', 'n_self_fused_faces', 'n_self_merged_revisits',
               'P_total_code', 'P_sum_check_code', 'dissipation_share', 'sv_dominant', 'sv_face_abs_current_over_I', 'I_bot_code')


def _jsonable(x):
    """numpy 수 · 배열 · 튜플 → JSON 원형 (float NaN/inf 는 그대로 — payload 의 finite_belt 가 경로째 기록한다)."""
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return [_jsonable(v) for v in x.tolist()]
    if isinstance(x, (bool, np.bool_)):
        return bool(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    return x


def _num(v, name, *, positive=False):
    """선언 수 → float.  None · bool · 문자열 · 비유한 = 거부 (기본값 없음 · 조용한 강제 없음)."""
    if v is None:
        raise ValueError(f'{name} 가 없다 — 기본값 없음 (정량 런은 결과 전 선언 · 등록 R §2-1)')
    if isinstance(v, (bool, np.bool_)) or not isinstance(v, (int, float, np.integer, np.floating)):
        raise ValueError(f'{name} = {v!r} — 실수여야 한다 (bool · 문자열 거부)')
    x = float(v)
    if not math.isfinite(x):
        raise ValueError(f'{name} = {v!r} — 유한해야 한다 (NaN · ±inf 거부)')
    if positive and not x > 0.0:
        raise ValueError(f'{name} = {v!r} — 0 보다 커야 한다 (정량 · 극한 0 · ∞ = 사다리 진단 전용 · 이 배선 밖)')
    if not positive and x < 0.0:
        raise ValueError(f'{name} = {v!r} — 0 이상이어야 한다')
    return x


_RULES = []


def canonical_rules():
    """원장 규칙 판 — `carbon_junction` 이 원장에 적는 그 dict (빈 원장 하나를 만들어 읽는다 · 사본 없음)."""
    if not _RULES:
        reg = CJ.cjunc_registry(np.zeros((1, 1, 1), np.int8), (0.0, 0.0, 0.0), 1.0, np.zeros((0, 3)), np.zeros(0, np.int64),
                                np.zeros(0, np.int64), np.zeros(0, np.int64), r_f_um=R_F_UM, tol_ff_um=0.0, L_par_um=L_PAR_UM,
                                r_port_um=R_PORT_UM, s_min_um=0.0, gap_tol=GAP_TOL)
        _RULES.append(_jsonable(reg['rules']))
    return dict(_RULES[0])


def cjunc_protocol_record(*, R_j_ohm, len_law, unreg_law, s_min_um, tol_ff_um, ptfe_jlaw, ptfe_stamp):
    """`ca_ext.cjunc.protocol` — 물리 칸 (p3ca id 에 들어간다).  선언 값 여섯 + 이 코드의 상수 (모델 판 · 규칙 판 · 고정 문턱).
    정량만 (R_j 유한 > 0 · s_min 등록 · tol_ff 유한 ≥ 0) · face_alpha 와 한 런 = 거부 · P1 = face_alpha 에서만 (→ 지금 거부)."""
    R = _num(R_j_ohm, 'R_j_ohm', positive=True)
    if len_law != CJ.CJUNC_LEN_LAW:
        raise ValueError(f'접합 길이 법칙 {len_law!r} ≠ 이 코드의 {CJ.CJUNC_LEN_LAW!r} (선언 필수 · 옛 판 · 다른 판 섞임 거부)')
    if unreg_law not in CJ.UNREG_LAWS:
        raise ValueError(f'미등록 VV 면 법칙 {unreg_law!r} ∉ {CJ.UNREG_LAWS} (선언 필수 · 자동 fallback 없음 · v2 §3-6)')
    s = _num(s_min_um, 's_min_um')
    t = _num(tol_ff_um, 'tol_ff_um')
    if ptfe_jlaw not in CJ.PTFE_JLAWS:
        raise ValueError(f'PTFE–접합 법칙 {ptfe_jlaw!r} ∉ {CJ.PTFE_JLAWS}')
    if ptfe_stamp not in ('off', 'centerline'):
        raise ValueError(f'ptfe_stamp = {ptfe_stamp!r} — 접합 (S2) 은 off · centerline 에서만 (face_alpha + 접합 = 설계 미정의 조합 · '
                         f'capsule = 예약값)')
    if ptfe_jlaw == 'P1':
        raise ValueError('PTFE–접합 법칙 P1 (덮인 접합 절단) 은 face_alpha 에서만 — face_alpha + 접합 조합이 아직 정의되지 않아 '
                         '지금은 닿지 않는다 (centerline 은 이미 VGCF 셀을 sid 7 로 자른다 · 설계 §4-1)')
    return {'wiring': WIRING_VERSION, 'model': CJ.CJUNC_MODEL_VERSION, 'schema': CJ.CJUNC_SCHEMA, 'len_law': CJ.CJUNC_LEN_LAW,
            'rules': canonical_rules(), 'R_j_ohm': R, 'unreg_law': str(unreg_law), 'ptfe_jlaw': str(ptfe_jlaw),
            'ptfe_stamp': str(ptfe_stamp), 'r_f_um': float(R_F_UM), 'tol_ff_um': t, 'L_par_um': float(L_PAR_UM),
            'r_port_um': float(R_PORT_UM), 's_min_um': s, 'gap_tol': float(GAP_TOL), 'tol_P_um': t, 'tol_sj_um': t,
            'r_ptfe_um': float(CJ.PTFE_R_UM), 'r_sdcp_um': float(CJ.SDCP_R_UM), 'rj_reference_plane': CJ.RJ_REFERENCE_PLANE,
            'half_cell_in_edge': False, 'quantitative': True, 'allow_rj_limits': False, 'channel': CHANNEL}


def sdcp_mod_protocol_record(*, c, tol_sj_um):
    """`ca_ext.sdcp_mod.protocol` — c ∈ {0, 1} (정량 · 시나리오 두 끝) · tol_sj (= 접합 tol_ff · 한 숫자)."""
    cv = _num(c, 'c')
    if cv not in (0.0, 1.0):
        raise ValueError(f'SDCP 수정자 c = {c!r} — 정량 R 런은 {{0, 1}} 만 (시험 격자는 이 배선 밖 · 설계 §5-2)')
    return {'wiring': WIRING_VERSION, 'model': CJ.CJUNC_MODEL_VERSION, 'c': cv, 'tol_sj_um': _num(tol_sj_um, 'tol_sj_um'),
            'r_sdcp_um': float(CJ.SDCP_R_UM), 'rule': SDCP_RULE}


def cjunc_evidence_record(*, counts, census, solve, receipts, fp, sdcp_mod_c, rejections=()):
    """`ca_ext.cjunc.evidence` — 증거 (id 밖 · `cjunc_block_problem` 이 대조)."""
    return {'counts': _jsonable(dict(counts)), 'census': _jsonable(dict(census)), 'solve': _jsonable(dict(solve)),
            'receipts': _jsonable(dict(receipts)), 'fp': _jsonable(dict(fp)), 'rejections': _jsonable(list(rejections)),
            'sdcp_mod_c': (None if sdcp_mod_c is None else float(sdcp_mod_c)), 'status': CJ.CJUNC_STATUS,
            'qualifiers': list(CJ.CJUNC_QUALIFIERS), 'diagnostics': dict(DIAGNOSTICS_V0), 'label': LABEL_CJUNC}


def sdcp_mod_evidence_record(*, n_sdcp_near, n_contracted_by_c):
    """`ca_ext.sdcp_mod.evidence` — 근접 instance 수 · c 가 축약한 수 · 판별 표지 (SDCP 0 침대 = 구성상 no-op)."""
    return {'n_sdcp_near': int(n_sdcp_near), 'n_contracted_by_c': int(n_contracted_by_c),
            's3_discriminating': bool(int(n_sdcp_near) > 0), 'label': LABEL_SDCP}


def payload_prepare(sid, *, lo, vox, pts, phase, fid, kind, cjunc, sdcp_mod=None, ptfe_stamp):
    """payload 한 런의 S2 (+ S3) 준비 — 원장 (기하) → 정량 계획.  cjunc = 선언 dict (`REQUEST_KEYS_CJUNC`) · sdcp_mod = {'c': c} | None.
    거부 사유가 하나라도 있으면 ValueError (조립 전 · CG 0 · payload 가 구조화 사유로 멈춘다)."""
    prot = cjunc_protocol_record(ptfe_stamp=ptfe_stamp, **{k: cjunc.get(k) for k in REQUEST_KEYS_CJUNC})
    sdp = None if sdcp_mod is None else sdcp_mod_protocol_record(c=sdcp_mod.get('c'), tol_sj_um=prot['tol_ff_um'])
    reg = CJ.cjunc_registry(sid, lo, vox, pts, phase, fid, kind, r_f_um=prot['r_f_um'], tol_ff_um=prot['tol_ff_um'],
                            L_par_um=prot['L_par_um'], r_port_um=prot['r_port_um'], s_min_um=prot['s_min_um'],
                            gap_tol=prot['gap_tol'], tol_P_um=prot['tol_P_um'], tol_sj_um=prot['tol_sj_um'],
                            r_ptfe_um=prot['r_ptfe_um'], r_sdcp_um=prot['r_sdcp_um'])
    if _jsonable(reg['rules']) != prot['rules']:
        raise ValueError('원장 규칙 판 ≠ protocol 정본 (carbon_junction 이 이 배선 뒤 바뀌었다 · 다른 판 섞임 거부)')
    _thr = _jsonable(reg['thresholds'])
    for k in ('r_f_um', 'tol_ff_um', 'L_par_um', 'r_port_um', 's_min_um', 'gap_tol', 'tol_P_um', 'tol_sj_um', 'r_ptfe_um', 'r_sdcp_um'):
        if _thr.get(k) != prot[k]:
            raise ValueError(f'원장 문턱 {k} = {_thr.get(k)!r} ≠ protocol {prot[k]!r}')
    plan = CJ.cjunc_plan(reg, prot['R_j_ohm'], unreg_law=prot['unreg_law'], ptfe_stamp=prot['ptfe_stamp'],
                         ptfe_jlaw=prot['ptfe_jlaw'], sdcp_mod=(None if sdp is None else {'c': sdp['c']}), quantitative=True)
    if plan['rejections']:
        raise ValueError('정량 거부 사유 — ' + ' · '.join(f"{x.get('code')}(n={x.get('n')})" for x in plan['rejections']))
    return {'plan': plan, 'protocol': prot, 'sdcp_protocol': sdp,
            'fp': {'registry': reg['fp']['registry'], 'sid': reg['fp']['sid'], 'plan_rows': plan['fp_rows'],
                   'centreline': reg['fp']['centreline'], 'membership': reg['fp']['membership']},
            'counts': _jsonable(plan['record']['counts']), 'census': _jsonable(reg['census'])}


def solve_receipt(res, prep, *, name, disabled_why=None):
    """솔브 한 건의 S2 영수증 (설계 §7 LEAN 표 · 상태 어휘 = run_contract.INTERFACE_OK_STATUSES 부분 · 위반 표지 = missing ·
    applied_without_request).  주 전자 솔브만 요청 (전자 채널) · 집전체 둘 = v0 끔 (disabled) · 이온 = 끈 솔브 disabled · 돈 솔브 not_requested."""
    rec = res.get('cjunc') if isinstance(res, dict) else None
    if name != 'electronic_main':
        if isinstance(rec, dict):
            return {'status': 'applied_without_request', 'why': f'{name} 솔브에 cjunc 기록 — 요청은 주 전자 솔브뿐'}
        if disabled_why is not None:
            return {'status': 'disabled', 'why': str(disabled_why)}
        if name == 'ionic':
            return {'status': 'not_requested'}
        return {'status': 'missing', 'why': f'{name} 솔브가 돌았다 — v0 = --no-collector 필수 (입구 거부를 지나왔다)'}
    if disabled_why is not None:
        return {'status': 'missing', 'why': '주 전자 솔브는 끌 수 없다'}
    if not isinstance(res, dict):
        return {'status': 'missing', 'why': '솔브 결과가 없다'}
    if not isinstance(rec, dict):
        return {'status': 'missing', 'why': '솔브 결과에 cjunc 기록이 없다 — 계획이 이 호출에 전달되지 않았다'}
    fp = prep['fp']['registry']
    _rr = prep['plan']['record']
    if rec.get('fp_registry') != fp or rec.get('R_j_ohm') != _rr.get('R_j_ohm') or rec.get('counts') != _rr.get('counts'):
        return {'status': 'missing', 'why': '솔브가 쓴 계획 (원장 지문 · R_j · 수) ≠ 요청 계획'}
    try:
        n_inst = int(rec.get('n_instances'))
    except (TypeError, ValueError):
        return {'status': 'missing', 'why': f'솔브 기록 n_instances = {rec.get("n_instances")!r}'}
    out = {'n_instances': n_inst, 'n_junction_edges': int(rec.get('n_junction_edges') or 0), 'solved': bool(rec.get('solved') is True),
           'fp_registry': fp}
    if res.get('reason') or rec.get('solved') is not True:
        out.update(status='failed', why=str(res.get('reason') or rec.get('reason') or 'unsolved'))
        return out
    out['status'] = 'applied' if n_inst > 0 else 'absent_geometry'
    return out


def _solve_summary(rec):
    if not isinstance(rec, dict):
        return {'solved': False, 'reason': '주 솔브 cjunc 기록 없음'}
    return _jsonable({k: rec.get(k) for k in _SOLVE_KEYS if k in rec})


def payload_blocks(prep, receipts, res_main):
    """하위 블록 {'cjunc': {protocol, evidence}, ('sdcp_mod': …)} — payload 가 바깥 `ca_ext` 에 schema 와 함께 싣는다."""
    rec = res_main.get('cjunc') if isinstance(res_main, dict) else None
    sdp = prep['sdcp_protocol']
    ev = cjunc_evidence_record(counts=prep['counts'], census=prep['census'], solve=_solve_summary(rec),
                               receipts={k: receipts.get(k) or {'status': 'missing', 'why': '영수증 없음'} for k in SOLVES},
                               fp=dict(prep['fp']), sdcp_mod_c=(None if sdp is None else sdp['c']),
                               rejections=list(prep['plan']['rejections']))
    out = {SUB_CJUNC: {'protocol': dict(prep['protocol']), 'evidence': ev}}
    if sdp is not None:
        out[SUB_SDCP] = {'protocol': dict(sdp),
                         'evidence': sdcp_mod_evidence_record(n_sdcp_near=prep['counts']['n_sdcp_near'],
                                                              n_contracted_by_c=prep['counts']['n_contracted_by_c'])}
    return out


# ═════════════════════════ 검증기 (run_contract.ca_ext_record_ok 가 부른다) ═════════════════════════
def _block(man, sub):
    ca = man.get('ca_ext') if isinstance(man, dict) and isinstance(man.get('ca_ext'), dict) else {}
    b = ca.get(sub)
    if not isinstance(b, dict) or not isinstance(b.get('protocol'), dict) or not isinstance(b.get('evidence'), dict):
        return None
    return b


def _int(v):
    return type(v) is int                                     # noqa: E721 — bool 제외


def _v0_problem(man):
    """v0 런 모양 (설계 §3-3 · §4-3 · §7 LEAN 표) — 소비자 쪽에서 producer 입구 거부의 짝."""
    if man.get('fibre_stamp') != 'segment':
        return f'v0| fibre_stamp = {man.get("fibre_stamp")!r} — 접합 = 선분 스탬프 (연속 중심선) 에서만'
    plan = man.get('component_plan') if isinstance(man.get('component_plan'), dict) else {}
    for k in ('thermal', 'pore', 'collector'):
        if plan.get(k) is not False:
            return f'v0| component_plan.{k} = {plan.get(k)!r} — v0 = LEAN 2 · 3 만 (원장을 안 읽는 솔브 · 진단)'
    if man.get('field_requested') is not False:
        return 'v0| 필드 요청 (LEAN 4) — v0 거부 (|J| 점군이 접합 원장을 안 읽는다)'
    if man.get('periodic_xy') is not False:
        return 'v0| periodic_xy — 정량 모드 거부 (주기 seam 미지원 · J10)'
    if man.get('interface_model') is not None:
        return 'combo| r1 계면 표와 접합 동시 — 거부 (설계 §4-3)'
    _sb = man.get('sdcp_bridge_um')
    if _sb is None or isinstance(_sb, bool) or not isinstance(_sb, (int, float)) or float(_sb) != 0.0:
        return f'combo| SDCP 브리지 진단 팔 (sdcp_bridge_um = {_sb!r}) 과 접합 동시 — 거부 (설계 §4-3)'
    _sv = man.get('sigma_vgcf_S_cm')
    if isinstance(_sv, bool) or not isinstance(_sv, (int, float)) or not math.isfinite(_sv) or _sv <= 0.0:
        return f'combo| σ_VGCF = {_sv!r} — 전자 채널에서 VGCF 가 도체여야 접합이 뜻을 가진다 (조용한 무효 금지)'
    return None


def cjunc_block_problem(man):
    """`ca_ext.cjunc` 계약 → 문제 | None.  protocol = 이 코드의 정본 (선언 여섯만 고른다) · v0 조건 · 네 솔브 영수증 (LEAN 표) ·
    원장 수 항등식 · 솔브 기록 ↔ 영수증 ↔ 원장 결합 · 거부 사유 0 · 수정자 기록 ↔ sdcp_mod 블록 · 진단 표 · 한정어 · 표지."""
    if not isinstance(man, dict):
        return 'manifest 가 dict 가 아니다'
    blk = _block(man, SUB_CJUNC)
    if blk is None:
        return 'shape| cjunc = {protocol, evidence} dict 이어야 한다'
    prot, ev = blk['protocol'], blk['evidence']
    ps = man.get('ptfe_stamp')
    if ps == 'face_alpha' or 'ptfe_face' in (man.get('ca_ext') or {}):
        return ('combo| face_alpha (S1) + cjunc (S2) 한 런 = 설계 미정의 조합 — 거부 (solve_sigma_z 와 같은 규칙 · 1저자 · Codex 결정 전)')
    try:
        want = cjunc_protocol_record(ptfe_stamp=ps, **{k: prot.get(k) for k in REQUEST_KEYS_CJUNC})
    except (ValueError, TypeError) as e:
        return f'protocol| {e}'
    if prot != want:
        return 'protocol| 이 코드의 정본과 다르다 ' + str(sorted(k for k in set(prot) | set(want) if prot.get(k) != want.get(k)))
    why = _v0_problem(man)
    if why:
        return why
    fpd = ev.get('fp') if isinstance(ev.get('fp'), dict) else {}
    if not (isinstance(fpd.get('registry'), str) and fpd['registry']):
        return 'fp| 증거의 원장 지문이 없다'
    cnt = ev.get('counts') if isinstance(ev.get('counts'), dict) else None
    if cnt is None or any(not _int(cnt.get(k)) or cnt.get(k) < 0 for k in _COUNT_INT):
        return f'counts| 원장 수 기록 모양 ({cnt!r})'
    if cnt['n_instances'] != cnt['n_edge'] + cnt['n_contract'] + cnt['n_cut_p1'] + cnt['n_unrealized'] + cnt['n_none_inf']:
        return f'counts| instance 수 ≠ 간선 + 축약 + 절단 + 미실현 + 극한 ({cnt})'
    if cnt['n_none_inf'] != 0:
        return 'counts| R_j = ∞ 극한 instance — 정량 (R_j 유한 > 0) 과 모순'
    if prot['ptfe_jlaw'] == 'P0' and cnt['n_cut_p1'] != 0:
        return 'counts| P0 인데 P1 절단 instance > 0'
    rc = ev.get('receipts')
    if not isinstance(rc, dict) or set(rc) != set(SOLVES):
        return f'receipts| 키 {sorted(rc) if isinstance(rc, dict) else rc!r} ≠ {sorted(SOLVES)}'
    plan = man.get('component_plan') if isinstance(man.get('component_plan'), dict) else {}
    for name in SOLVES:
        r = rc[name]
        if not isinstance(r, dict):
            return f'receipts|{name}| dict 가 아니다'
        st = r.get('status')
        if st in ('missing', 'applied_without_request'):
            return f'receipts|{name}| 위반 표지 {st} ({r.get("why")})'
        if st not in OK_STATUSES:
            return f'receipts|{name}| 모르는 상태 {st!r}'
        if name == 'electronic_main':
            ok_st = ('applied', 'absent_geometry', 'failed')
        elif name == 'ionic':
            ok_st = ('disabled',) if plan.get('ionic') is False else ('not_requested',)
        else:
            ok_st = ('disabled',)
        if st not in ok_st:
            return f'receipts|{name}| 상태 {st} — 이 계획 (LEAN 표) 에서 허용 {ok_st}'
        if st in ('failed', 'disabled') and not r.get('why'):
            return f'receipts|{name}| {st} 인데 사유 없음'
    main = rc['electronic_main']
    solve = ev.get('solve') if isinstance(ev.get('solve'), dict) else None
    if solve is None:
        return 'solve| 주 솔브 기록이 없다'
    if main['status'] in ('applied', 'absent_geometry'):
        n = main.get('n_instances')
        if not _int(n) or (main['status'] == 'applied') != (n > 0) or n != cnt['n_instances']:
            return f'receipts|electronic_main| {main["status"]} 인데 n_instances = {n!r} (원장 {cnt["n_instances"]})'
        if main.get('solved') is not True or solve.get('solved') is not True:
            return f'receipts|electronic_main| {main["status"]} 인데 solved = {main.get("solved")!r} / 기록 {solve.get("solved")!r}'
        if main.get('fp_registry') != fpd['registry']:
            return 'receipts|electronic_main| 솔브가 쓴 원장 지문 ≠ 증거의 원장 지문'
        nj = main.get('n_junction_edges')
        if not _int(nj) or nj != solve.get('n_junction_edges') or nj > cnt['n_edge']:
            return f'solve| 접합 간선 수 {nj!r} ↔ 기록 {solve.get("n_junction_edges")!r} ↔ 계획 간선 {cnt["n_edge"]}'
        if solve.get('n_contracted') != cnt['n_contract']:
            return f'solve| 축약 수 {solve.get("n_contracted")!r} ≠ 원장 {cnt["n_contract"]}'
        if solve.get('short') is not False:
            return f'solve| 단락 상태 {solve.get("short")!r} — 판–판 0 저항 경로는 유한 σ 로 게시하지 않는다 (J11)'
    if ev.get('rejections') != []:
        return f'rejections| 정량 거부 사유가 남았다 {ev.get("rejections")!r}'
    sd = _block(man, SUB_SDCP)
    c_rec = ev.get('sdcp_mod_c')
    if (sd is None) != (c_rec is None):
        return f'sdcp| 접합 증거의 수정자 c = {c_rec!r} ↔ sdcp_mod 블록 {"있음" if sd is not None else "없음"}'
    if sd is not None and sd['protocol'].get('c') != c_rec:
        return f'sdcp| 접합 증거의 c {c_rec!r} ≠ 수정자 블록 c {sd["protocol"].get("c")!r}'
    if c_rec is None and cnt['n_contract'] != 0:
        return 'counts| 수정자 없이 축약 instance > 0 (R_j 유한 > 0 이면 축약 = S3 c = 1 뿐)'
    if ev.get('status') != CJ.CJUNC_STATUS or ev.get('qualifiers') != list(CJ.CJUNC_QUALIFIERS):
        return 'qualifiers| 지위 · 필수 한정어가 producer 상수와 다르다'
    if ev.get('diagnostics') != DIAGNOSTICS_V0:
        return 'diagnostics| v0 진단 표 (je · 소산 분담 미계산 · 필드 · Joule 거부) 가 아니다'
    if ev.get('label') != LABEL_CJUNC:
        return 'label| 표지 문자열이 producer 상수와 다르다'
    return None


def sdcp_mod_block_problem(man):
    """`ca_ext.sdcp_mod` 계약 → 문제 | None.  S2 (cjunc) 블록 없이 = 거부 · protocol 정본 (c ∈ {0, 1} · tol_sj = 접합 tol_ff) ·
    근접 · 축약 수 = 접합 원장 · c = 0 → 축약 0 · c = 1 (P0) → 근접 instance 전부 축약 · 판별 표지 · 표지."""
    if not isinstance(man, dict):
        return 'manifest 가 dict 가 아니다'
    sd = _block(man, SUB_SDCP)
    if sd is None:
        return 'shape| sdcp_mod = {protocol, evidence} dict 이어야 한다'
    cj = _block(man, SUB_CJUNC)
    if cj is None:
        return 'S2| 탄소 접합 (cjunc) 블록 없이 S3 수정자 = 거부 (설계 §5-2)'
    prot, ev = sd['protocol'], sd['evidence']
    try:
        want = sdcp_mod_protocol_record(c=prot.get('c'), tol_sj_um=prot.get('tol_sj_um'))
    except (ValueError, TypeError) as e:
        return f'protocol| {e}'
    if prot != want:
        return 'protocol| 이 코드의 정본과 다르다 ' + str(sorted(k for k in set(prot) | set(want) if prot.get(k) != want.get(k)))
    if prot['tol_sj_um'] != cj['protocol'].get('tol_ff_um'):
        return f'protocol| tol_sj {prot["tol_sj_um"]!r} ≠ 접합 tol_ff {cj["protocol"].get("tol_ff_um")!r} (한 숫자 · 설계 §4-1)'
    cnt = cj['evidence'].get('counts') if isinstance(cj['evidence'].get('counts'), dict) else {}
    n_near, n_ctr = ev.get('n_sdcp_near'), ev.get('n_contracted_by_c')
    if not _int(n_near) or not _int(n_ctr) or n_near < 0 or n_ctr < 0:
        return f'evidence| 근접 · 축약 수 모양 ({n_near!r}, {n_ctr!r})'
    if n_near != cnt.get('n_sdcp_near') or n_ctr != cnt.get('n_contracted_by_c') or n_ctr != cnt.get('n_contract'):
        return (f'evidence| 근접 {n_near} · 축약 {n_ctr} ≠ 접합 원장 (근접 {cnt.get("n_sdcp_near")!r} · c 축약 '
                f'{cnt.get("n_contracted_by_c")!r} · 축약 {cnt.get("n_contract")!r})')
    if prot['c'] == 0.0 and n_ctr != 0:
        return f'evidence| c = 0 인데 축약 {n_ctr}'
    if prot['c'] == 1.0 and cj['protocol'].get('ptfe_jlaw') == 'P0' and n_ctr != n_near:
        return f'evidence| c = 1 (P0) 인데 축약 {n_ctr} ≠ 근접 {n_near} (근접 instance 는 전부 축약 경로)'
    if ev.get('s3_discriminating') is not (n_near > 0):
        return f'evidence| 판별 표지 {ev.get("s3_discriminating")!r} ↔ 근접 {n_near} (SDCP 0 침대 = 구성상 no-op)'
    if ev.get('label') != LABEL_SDCP:
        return 'label| 표지 문자열이 producer 상수와 다르다'
    return None

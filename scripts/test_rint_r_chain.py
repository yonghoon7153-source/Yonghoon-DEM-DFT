#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② R 런 사슬 `scripts/rint_r_chain.py` 시험 (시험 먼저 · 2026-10-20 · 가짜 러너 · GPU 없음).

정본 = 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3 (보정 사다리 · 식별성 · 확인 · 비단조 · 점 수 ·
허용폭 · origin) · §4 (모서리 넷 · 같은 P 일관 · origin 0.1 W) · §5 (구간 · 정보량 · 판정 · 표지) · §10 (명령 꼴 · 멈춤 목록) ·
설계 v1 §6 (수렴 증서) · §7 (세대 p3ca · 영수증 · LEAN 표).

가짜 러너 = 작은 파이썬 (bash 감쌈) — env (KITS · CJUNC_RJ · CJUNC_PTFE_JLAW · SDCP_MOD_C · VOX · SIGMA_FIBRE_BULK · …) 를 읽어 **정해 둔 σ(R_j)**
(거듭제곱 · 로지스틱) 로 진짜 꼴의 팔 JSON (매니페스트 · `ca_ext` 세 하위 블록 · 수렴 증서) · `run_receipt.json` 을 쓴다.  고장 주입 = 세계 파일
`faults` (rc 2 · 기각 기록 · 증서 실패 · 세대 · 변조 · LEAN · PTFE 셀 · sid 지문 · 잠 …).
⚠ `ca_ext_record_ok` · `check_arm` 의 정본은 지금 face_alpha + 접합 조합을 거부한다 (Z1 이 같이 고치는 중) → 이 시험은 계약 자리에
**가짜 인지 계약** (블록 지문 대조) 을 넣는다 · 기본 계약이 정본 함수에 위임하는지는 X03 이 따로 본다.

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
sys.path.insert(0, W['scripts'])
import run_contract as RC
exec(W['model_src'])


def jl(name, rec):
    with open(os.path.join(WD, name), 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, sort_keys=True) + '\n')


cp = os.path.join(WD, 'calls.txt')
n = (int(open(cp).read()) if os.path.exists(cp) else 0) + 1
open(cp, 'w').write(str(n))
SEEN = ('SIGMA_', 'SDCP_', 'PTFE_', 'CJUNC', 'STEP3_', 'P2_')
jl('env.jsonl', {k: E[k] for k in sorted(E) if k.startswith(SEEN) or k in (
    'VOX', 'BRIDGE_UM', 'ARMS', 'KITS', 'OUTDIR', 'LEAN', 'FIBRE_STAMP', 'MPM_PERIODIC_SIGMA', 'EXPECT_BACKEND', 'EXPECT_PROTOCOL')})
kit, arms, out = E['KITS'], int(E['ARMS']), E['OUTDIR']
rj, law, c = E['CJUNC_RJ'], E['CJUNC_PTFE_JLAW'], E.get('SDCP_MOD_C', '')
vox, bulk = float(E['VOX']), float(E['SIGMA_FIBRE_BULK'])
unreg, yv = E['CJUNC_UNREG_LAW'], E.get('SDCP_YIELD_VGCF', '') == '1'
rtol = float(E['STEP3_RTOL'])
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
limit = 'floor' if rj == 'inf' else ('ceiling' if rj == '0' else None)
Rv = None if rj == 'inf' else float(rj)
s_min, tol_ff = float(E['CJUNC_S_MIN_UM']), float(E['CJUNC_TOL_FF_UM'])
CERT = W['cert']


def canon(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def manifest(i, si):
    cjp = {'wiring': 'b6-cjunc-payload-v1', 'model': 'fake-cjunc-v0', 'schema': 'fake', 'len_law': E['CJUNC_LEN_LAW'], 'R_j_ohm': Rv,
           'unreg_law': unreg, 'ptfe_jlaw': law, 'ptfe_stamp': E['PTFE_STAMP'], 'r_f_um': 0.075, 'tol_ff_um': tol_ff, 'L_par_um': 0.3,
           'r_port_um': 0.3, 's_min_um': s_min, 'gap_tol': 2.0, 'tol_P_um': tol_ff, 'tol_sj_um': tol_ff, 'r_ptfe_um': 0.124,
           'r_sdcp_um': 0.15, 'rj_reference_plane': 'model_internal_port_centre', 'half_cell_in_edge': False,
           'quantitative': limit is None, 'allow_rj_limits': limit is not None, 'channel': 'electronic'}
    if limit:
        cjp['rj_limit'] = limit
    rc_ = {'electronic_main': {'status': 'applied', 'n_instances': 12}, 'electronic_wetted': {'status': 'disabled', 'why': 'LEAN 2'},
           'electronic_bare': {'status': 'disabled', 'why': 'LEAN 2'}, 'ionic': {'status': 'disabled', 'why': 'LEAN 2 (--no-ion)'}}
    if hit('lean_bad'):
        rc_['electronic_wetted'] = {'status': 'applied'}
    sid = 'sidfp-%s-%g-%s' % (kit, vox, yv)
    if hit('sid_fp'):
        sid = 'sidfp-OTHER'
    solve = {'solved': True, 'short': False, 'sv_dominant': False,
             'dissipation_share': {'junction': 0.4, 'va_face': 0.2, 'sv_face': 0.05, 'sdcp_cell': 0.02}}
    if hit('sv_dominant'):
        solve['sv_dominant'] = True
    if hit('sv_missing'):
        solve.pop('sv_dominant')
    ca = {'schema': 'ca-ext-v1',
          'ptfe_face': {'protocol': {'operator': 'fake-face', 'channels': ['electronic', 'ionic'], 'dia_law': 'rope'},
                        'evidence': {'receipts': json.loads(json.dumps(rc_)), 'fp': {'caps': 'capfp'}}},
          'cjunc': {'protocol': cjp, 'evidence': {'receipts': rc_, 'fp': {'registry': 'regfp', 'sid': sid},
                                                  'counts': {'n_instances': 12, 'n_edge': 12}, 'solve': solve}}}
    req = ['cjunc']
    if c != '':
        nn = 7 if is_dbe else 0
        ca['sdcp_mod'] = {'protocol': {'c': float(c), 'tol_sj_um': tol_ff},
                          'evidence': {'n_sdcp_near': nn, 'n_contracted_by_c': nn if c == '1' else 0, 's3_discriminating': nn > 0}}
        req = ['cjunc', 'sdcp_mod']
    man = {'schema_version': 3, 'vox_um': vox, 'bridge_um': float(E['BRIDGE_UM']), 'fibre_stamp': 'segment', 'sdcp_stamp': 'sphere',
           'sdcp_sphere_d_um': float(E['SDCP_SPHERE_D']), 'sdcp_yield_to_vgcf': yv, 'sdcp_bridge_um': 0.0, 'ptfe_block_um': 0.0,
           'ptfe_stamp': E['PTFE_STAMP'], 'ptfe_zero_dof': False,
           'sigma_vgcf_S_cm': float('%.6g' % (bulk * math.pi * 0.15 ** 2 / (4.0 * vox * vox))),
           'sigma_sdcp_S_cm': float(E['SIGMA_SDCP_OVERRIDE']), 'sigma_ptfe_S_cm': 0.0, 'sigma_ion_se_S_cm': 0.003,
           'sigma_ion_sdcp_S_cm': 0.001, 'sigma_am_s_S_cm': float(E['SIGMA_AM_S_OVERRIDE']), 'sigma_am_p_S_cm': 0.0041,
           'cam': 'ncm811', 'temp_c': None, 'periodic_xy': False, 'plate_rule': 'p2-occupied-surface-first',
           'sigma_superp_S_cm': 0.0, 'sigma_swcnt_S_cm': 0.0, 'swcnt_ion_block': False, 'dilate_z': 0.0, 'se_source': 'file:se.npy',
           'origin_shift_um': list(shifts[i]), 'ptfe_cells_observed': 0,
           'component_plan': {'electronic': True, 'ionic': False, 'thermal': False, 'pore': False, 'collector': False},
           'components': {'electronic': {'status': 'complete', 'backend': {'used': 'gpu'}}},
           'backend': {'used': 'gpu', 'rtol': rtol}, 'code_sha': 'fake0000', 'input_digest': 'in-' + kit,
           'ca_ext_requested': req, 'ca_ext': ca}
    if hit('p2gen'):
        man.pop('ca_ext')
        man.pop('ca_ext_requested')
        man['ptfe_stamp'] = 'centerline'
    if hit('unknown_caext'):
        man.pop('ca_ext')
    if hit('bad_am_s'):
        man['sigma_am_s_S_cm'] = 0.01
    if hit('ptfe_cells'):
        man['ptfe_cells_observed'] = 5
    man['physics_protocol_id'] = RC.physics_protocol_id(man)
    if hit('stale_id'):
        man['physics_protocol_id'] = 'p3ca-0000000000000000'
    man['_fake_caext_sha'] = hashlib.sha256(canon(man.get('ca_ext')).encode()).hexdigest()
    if hit('tamper_caext'):
        man['ca_ext']['cjunc']['evidence']['counts']['n_edge'] = 11
    return man


def cert(si):
    ok = not hit('certfail')
    return {'version': CERT['version'], 'rtol_used': rtol, 'rtol_max': CERT['rtol_max'], 'eps_I': CERT['eps_I'],
            'resolve_rtol': max(rtol * 1e-2, 1e-14), 'resolve_rtol_floor': 1e-14, 'resolve_tol': CERT['resolve_tol'],
            'info': 0, 'resid': 3e-13, 'I_bot': 1.0, 'I_top': 1.0, 'imbalance': (2e-7 if ok else 3e-4), 'sigma': si,
            'sigma_resolve': si, 'dsigma_rel': 1e-9, 'resolve_info': 0, 'pass_a': True, 'pass_b': ok, 'pass_c': True, 'ok': ok}


tag = rj.replace('.', 'p').replace('+', '').replace('-', 'm')
for i in range(arms):
    si = s0 * af[i]
    st = {'sigma_e_eff_S_cm': si, 'cg_info': 0, 'unconverged': False, 'cg_resid': 3e-13, 'n_dof': 1234, 'vox_um': vox,
          'status': 'complete', 'manifest': manifest(i, si), 'conv_cert': cert(si)}
    json.dump({'mpm_metrics': {'step3': st}}, open(os.path.join(out, 'p2_%s_sph_fa_cj%s_c%s_a%d.json' % (kit[4:], tag, c, i)), 'w'))
    jl('ledger.jsonl', {'sigma': si})
cj_req = {'R_j_ohm': Rv, 'len_law': E['CJUNC_LEN_LAW'], 'unreg_law': unreg, 's_min_um': s_min, 'tol_ff_um': tol_ff, 'ptfe_jlaw': law}
req = {'cjunc': cj_req}
if c != '':
    req['sdcp_mod'] = {'c': float(c)}
rec = {'vox_um': vox, 'bridge_um': float(E['BRIDGE_UM']), 'fibre_stamp': 'segment', 'sdcp_stamp': 'sphere',
       'sdcp_sphere_d_um': float(E['SDCP_SPHERE_D']), 'sdcp_yield_to_vgcf': yv, 'ptfe_stamp': E['PTFE_STAMP'], 'periodic_xy': False,
       'arms': arms, 'expect_backend': 'gpu', 'origins': [list(o) for o in RC.expected_origins_for(vox)],
       'sigma_am_s_S_cm': float(E['SIGMA_AM_S_OVERRIDE']), 'sigma_sdcp_S_cm': float(E['SIGMA_SDCP_OVERRIDE']),
       'ca_ext_request': req, 'step3_rtol': rtol * (10.0 if hit('receipt_rtol') else 1.0), 'code_sha': 'fake0000'}
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
PW = {'sbe': PW_SBE, 'law_factor': {'P0': 1.0, 'P1': 0.95}, 'c_factor': {'0': 0.92, '1': 1.08}, 'dbe_scale': 2.87,
      'arm_factor': ARM_SMALL, 'arm_factor_dbe': ARM_SMALL,
      'var_sbe': {'FIBRE': 0.9, 'UNREG': 1.05, 'GRID': 0.97}, 'var_dbe': {'SVORDER': 1.01}}


def world(name, base=None, **kw):
    """세계 파일 → 경로 (이름마다 새 폴더 · 호출 수 · 장부 · env 기록이 그 폴더에 쌓인다)."""
    import step3_conv_cert as CC                           # 증서 봉인 상수 = 정본 (시험 프로세스에서 한 번)
    d = Path(TD) / 'worlds' / name
    assert not d.exists(), f'세계 {name} 두 번'
    d.mkdir(parents=True)
    W = copy.deepcopy(base if base is not None else PW)
    W.update(copy.deepcopy(kw))
    W.update({'dir': str(d), 'scripts': str(SCRIPTS), 'model_src': MODEL_SRC,
              'cert': {'version': CC.CERT_VERSION, 'rtol_max': CC.CERT_RTOL_MAX, 'eps_I': CC.CERT_EPS_I,
                       'resolve_tol': CC.CERT_RESOLVE_TOL}})
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
    plan = {'schema': 'rint-r-plan-v1', 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': 0.6, 'tol_ff_um': 0.05,
            'step3_rtol': 1e-12, 'p2_extra': '--step3-maxiter 60000'}
    FX['plan_obj'] = plan
    FX['plan'] = Path(TD) / 'plan.json'
    FX['plan'].write_text(json.dumps(plan, indent=1, sort_keys=True), encoding='utf-8')
    sha = hashlib.sha256(FX['plan'].read_bytes()).hexdigest()
    FX['plan_sha'] = sha
    text = REG_DOC.read_text(encoding='utf-8')
    FX['reg_text'] = text

    def reg_with(cell, name):
        out = []
        for ln in text.splitlines():
            if ln.startswith('| 계획 해시 |'):
                cells = ln.split('|')
                cells[-2] = f' {cell} '
                ln = '|'.join(cells)
            out.append(ln)
        p = Path(TD) / name
        p.write_text('\n'.join(out) + '\n', encoding='utf-8')
        return p
    FX['reg_ok'] = reg_with(f'`{sha}`', 'reg_ok.md')
    FX['reg_other'] = reg_with('0' * 64, 'reg_other.md')
    FX['reg_unreg'] = reg_with('⬜', 'reg_unreg.md')


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


def fake_contract():
    class FakeContract(RR.RealContract):
        """가짜 인지 계약 — 블록 지문 (가짜 러너가 쓴 `_fake_caext_sha`) 대조 · check_arm 자리는 통과 (Z1 조합 전)."""

        def arm_problem(self, path, receipt):
            return None

        def ca_ext_record(self, man):
            want = man.get('_fake_caext_sha')
            got = hashlib.sha256(json.dumps(man.get('ca_ext'), sort_keys=True, ensure_ascii=False,
                                            separators=(',', ':')).encode()).hexdigest()
            return (True, None) if want == got else (False, 'CAEXT|fake| 블록이 쓴 뒤 바뀌었다')
    return FakeContract()


def call(argv, wpath=None, env=None):
    """사슬 main 을 프로세스 안에서 → (rc, 화면).  SystemExit 는 rc 로."""
    kv = dict(env or {})
    kv['FAKE_WORLD'] = wpath
    buf = io.StringIO()
    with envset(**kv), contextlib.redirect_stdout(buf):
        try:
            rc = RR.main([str(a) for a in argv], contract=fake_contract())
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 2
    return rc, buf.getvalue()


def ladder(tag, wpath, law='P0', variant=None, extra=(), reg=None, max_hours='2', env=None, prefill=False):
    out = Path(TD) / 'runs' / tag
    if prefill:
        out.mkdir(parents=True)
        (out / 'old.txt').write_text('x')
    argv = ['--stage', 'ladder', '--law', law, '--target', '1.63', '--runner', FX['runner'], '--root', FX['root'],
            '--plan', FX['plan'], '--registration', reg or FX['reg_ok'], '--max-hours', max_hours, '--out', out]
    if variant:
        argv += ['--variant', variant]
    rc, so = call(argv + list(extra), wpath, env)
    sp = out / 'ladder_summary.json'
    return {'rc': rc, 'out': out, 'so': so, 'sum': json.loads(sp.read_text(encoding='utf-8')) if sp.exists() else None,
            'world': wpath}


def predict(tag, wpath, ladders, variant=None, extra=(), reg=None, max_hours='2'):
    out = Path(TD) / 'runs' / tag
    argv = ['--stage', 'predict', '--ladders', *ladders, '--kit', DBE_KIT, '--runner', FX['runner'], '--root', FX['root'],
            '--registration', reg or FX['reg_ok'], '--max-hours', max_hours, '--out', out]
    if variant:
        argv += ['--variant', variant]
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


def eval_L03(res):
    W = wdata(res['world'])
    rt = r0_power(W)
    lo, hi = float(lad(res).get('R_j_lo') or 'nan'), float(lad(res).get('R_j_hi') or 'nan')
    wl, wh = rt * 1.02 ** (-1.0 / W['sbe']['e']), rt * 0.98 ** (-1.0 / W['sbe']['e'])
    return rel(lo, wl) < 1e-9 and rel(hi, wh) < 1e-9, f'lo {lo!r} ↔ {wl!r} · hi {hi!r} ↔ {wh!r}'


@check('L01', '정상 사다리 (거듭제곱) — CALIBRATED · 바닥 · 천장 · 1e4 · 1e6 · 1e8 · 반씩 둘 (1e7 · 10^6.5) · 확인 하나')
def t_L01():
    r = s_main('P0')
    L = lad(r)
    want = ['inf', '0', '10000.0', '1000000.0', '100000000.0', '10000000.0', repr(10 ** 6.5), L.get('R_j0')]
    return (r['rc'] == 0 and r['sum']['status'] == 'CALIBRATED' and L.get('order') == want and L.get('n_bisect') == 2
            and L.get('n_ext') == 0, (r['rc'], r['sum'] and r['sum'].get('status'), L.get('order'), stop_code(r)))


@check('L02', 'R_j,0 손계산 = R_ref·(s_ref/1.63)^(1/e) 의 유효숫자 3 자리 (2.27e6 · ln–ln 보간이 거듭제곱에서 정확)')
def t_L02():
    return eval_L02(s_main('P0'))


@check('L03', 'R_j,lo · R_j,hi 손계산 = 참 근 × 1.02^(−1/e) · 0.98^(−1/e) (보간식 · ±2 %)')
def t_L03():
    return eval_L03(s_main('P0'))


@check('L04', '끼는 이웃 비 ≤ 10^0.5 · 확인 1 회 통과 · 식별 통과 · 점 수 ≤ 12')
def t_L04():
    L = lad(s_main('P0'))
    a, b = (float(x) for x in L.get('bracket') or ('nan', 'nan'))
    return (math.log10(b / a) <= 0.5 + 1e-9 and L.get('identifiable') is True and [c['ok'] for c in L.get('confirms', [])] == [True]
            and L.get('n_runs', 99) <= 12, (L.get('bracket'), L.get('confirms'), L.get('n_runs')))


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


def run_L11(tag):
    W0 = dict(PW, sbe=dict(PW_SBE, s_ref=1.65e-3, e=0.01))
    return ladder(tag, world(tag, W0))


@check('L11', 'CALIB_UNIDENTIFIED — 탄성 e = 0.01 < e_min (0.02/ln√10) · 확인 런 없음')
def t_L11():
    r = scen('L11', lambda: run_L11('L11'))
    return (r['sum']['status'] == 'CALIB_UNIDENTIFIED' and 'confirm' not in roles(r), (r['sum']['status'], roles(r)))


@check('L12', 'CALIB_UNCONFIRMED — 확인 두 번 다 2 % 넘음 (확인 런 정확히 둘)')
def t_L12():
    r = scen('L12', lambda: ladder('L12', world('L12', dict(PW, bump_seq=[1.05, 0.95]))))
    return (r['sum']['status'] == 'CALIB_UNCONFIRMED' and roles(r).count('confirm') == 2
            and [c['ok'] for c in lad(r).get('confirms', [])] == [False, False], (r['sum']['status'], roles(r)))


@check('L13', '확인 한 번 실패 → 그 점을 넣고 다시 보간 → 둘째 확인 통과 (CALIBRATED · 확인 2)')
def t_L13():
    r = scen('L13', lambda: ladder('L13', world('L13', dict(PW, bump_seq=[1.03, 1.0222]))))
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
    W = dict(PW)
    W['rj_sigma'] = {'100000000.0': 2.0e-3 * 1.0005}
    r = scen('L15', lambda: ladder('L15', world('L15', W)))
    return (r['sum']['status'] != 'CALIB_NONMONOTONE' and ['1000000.0', '100000000.0'] in lad(r).get('flat_pairs', []),
            (r['sum']['status'], lad(r).get('flat_pairs')))


def run_L16(tag):
    W0 = dict(PW, sbe=dict(PW_SBE, s_ref=10e-3, R_ref=1e8, e=0.05, floor=0.5e-3, ceiling=100e-3))
    return ladder(tag, world(tag, W0))


@check('L16', 'CALIB_LADDER_EXHAUSTED — 런 12 개 (바닥 · 천장 · 셋 · ×100 일곱) 뒤 13 째 요청에서')
def t_L16():
    r = scen('L16', lambda: run_L16('L16'))
    return (r['sum']['status'] == 'CALIB_LADDER_EXHAUSTED' and len(roles(r)) == 12 and n_calls(r['world']) == 12,
            (r['sum']['status'], len(roles(r))))


@check('L17', 'NOT_COMPUTED — 1e6 점 수렴 증서 실패 → 그 점 NOT_COMPUTED · 사다리 멈춤 (뒤 런 없음)')
def t_L17():
    r = scen('L17', lambda: ladder('L17', world('L17', dict(PW, faults=[{'do': 'certfail', 'match': {'rj': '1000000.0'}}]))))
    return (r['rc'] == 3 and r['sum']['status'] == 'NOT_COMPUTED' and len(roles(r)) == 4 and n_calls(r['world']) == 4,
            (r['sum']['status'], roles(r), stop_code(r)))


@check('L18', 'origin §3-3 통과 — R_j,0 에서 arm 1 · 2 (ARMS 3 한 런) · ln(max/min) ≤ 0.02 · 8 팔 없음 · 표지 없음')
def t_L18():
    r = s_main('P0')
    o = lad(r).get('origin') or {}
    return (o.get('status') == 'pass' and roles(r).count('origin3') == 1 and 'origin8' not in roles(r)
            and r['sum'].get('flags') == [], (o, roles(r), r['sum'].get('flags')))


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


@check('S05', '매니페스트 σ_AM_S 변조 (0.01) → MANIFEST_MISMATCH')
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


@check('S10', '솔브 영수증 ≠ LEAN 2 표 (wetted applied) → RECEIPT_LEAN')
def t_S10():
    return stop_case('S10', [{'do': 'lean_bad', 'match': {'rj': '10000.0'}}], 'RECEIPT_LEAN')


@check('S11', 'face_alpha 런의 ptfe_cells_observed > 0 → PTFE_CELLS_OBSERVED')
def t_S11():
    return stop_case('S11', [{'do': 'ptfe_cells', 'match': {'rj': '0'}}], 'PTFE_CELLS_OBSERVED')


@check('S12', 'sid 격자 지문이 같은 킷 런 사이에서 다르다 → SID_GRID')
def t_S12():
    return stop_case('S12', [{'do': 'sid_fp', 'match': {'rj': '1000000.0'}}], 'SID_GRID')


@check('S13', 'env 에 SIGMA_VGCF_OVERRIDE → ENV_SIGMA_VGCF_OVERRIDE · 러너 0 회')
def t_S13():
    r = scen('S13', lambda: ladder('S13', world('S13'), env={'SIGMA_VGCF_OVERRIDE': '2.618'}))
    return (r['rc'] == 3 and stop_code(r) == 'ENV_SIGMA_VGCF_OVERRIDE' and n_calls(r['world']) == 0, (r['rc'], stop_code(r)))


@check('S14', '부모 env 오염 (SIGMA_ION_SE · P2_SCR · SIGMA_PTFE · MPM_PERIODIC_SIGMA · EXPECT_PROTOCOL · CJUNC_RJ) → 지우고 돈다 · 요약에 이름')
def t_S14():
    bad = {'SIGMA_ION_SE': '0.0015', 'P2_SCR': '/tmp/elsewhere', 'SIGMA_PTFE': '1e-16', 'MPM_PERIODIC_SIGMA': '1',
           'EXPECT_PROTOCOL': 'p2-0000', 'CJUNC_RJ': '999'}
    r = scen('S14', lambda: ladder('S14', world('S14', dict(PW, sbe=dict(PW_SBE, ceiling=1.5e-3))), env=bad))
    ev = env_log(r['world'])
    leak = [k for e in ev for k in bad if k in e and not (k == 'CJUNC_RJ' and e[k] in ('inf', '0'))]
    return (len(ev) == 2 and not leak and set(bad) <= set(r['sum'].get('env_scrubbed', [])) and ev[0].get('CJUNC_RJ') == 'inf',
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


@check('S18', '영수증 step3_rtol ≠ 계획 → MANIFEST_MISMATCH')
def t_S18():
    return stop_case('S18', [{'do': 'receipt_rtol', 'match': {'rj': '10000.0'}}], 'MANIFEST_MISMATCH')


@check('S19', '표적 ≠ 등록 (1.64) → NOT_REGISTERED · 러너 0 회 (판정선을 옮기지 않는다)')
def t_S19():
    def go():
        w = world('S19')
        out = Path(TD) / 'runs' / 'S19'
        rc, so = call(['--stage', 'ladder', '--law', 'P0', '--target', '1.64', '--runner', FX['runner'], '--root', FX['root'],
                       '--plan', FX['plan'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out], w)
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


# ── P 예측 ──
@check('P01', '예측 — SBE c no-op 런 둘 · 모서리 12 런 (arm 0) · origin 넷 (ARMS 3) · 상태 PREDICTED')
def t_P01():
    r = s_main_predict()
    rl = roles(r)
    return (r['rc'] == 0 and r['sum']['status'] == 'PREDICTED' and rl.count('sbe_noop') == 2 and rl.count('corner') == 12
            and rl.count('origin3') == 4 and 'origin8' not in rl, (r['rc'], r['sum'] and r['sum']['status'], rl, stop_code(r)))


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


@check('P05', 'origin §4-2 — 넘는 모서리 넷 → 8 팔 · R_j,0 값 = 8 팔 평균 · lo · hi 같은 로그 차 (판정 결과 손계산)')
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
    ok_runs = roles(p).count('origin8') == 4 and all(o['status'] == 'adjusted' for o in p['sum'].get('origin', []))
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


@check('V02', '감도 넷 안 돌림 → FIBRE · UNREG · GRID · SVORDER _UNCHECKED · §7-1 문장 금지 (판정 이름은 그대로)')
def t_V02():
    v = s_verdict_main()['v']
    want = {'FIBRE_UNCHECKED', 'UNREG_UNCHECKED', 'GRID_UNCHECKED', 'SVORDER_UNCHECKED'}
    return (want <= set(v['flags']) and v['sentence_allowed'] is False and v['verdict'] == 'PASS_INFORMATIVE',
            (v['flags'], v['sentence_allowed']))


@check('V03', '감도 넷 다 돌림 · 둔감 → 표지 없음 → §7-1 문장 허용 · DIA_UNCHECKED 한정어는 늘')
def t_V03():
    v = s_verdict_full()['v']
    return (v['verdict'] == 'PASS_INFORMATIVE' and v['flags'] == [] and v['sentence_allowed'] is True
            and isinstance(v.get('sentence'), str) and v['sentence'] in FX['reg_text'] and 'DIA_UNCHECKED' in v.get('qualifiers', []),
            (v['verdict'], v['flags'], v['sentence_allowed'], v.get('stop')))


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


def sv_set(tag, fault):
    def go():
        p = predict(tag, world(tag, dict(PW, faults=[{'do': fault, 'match': {'kit_has': 'DBE', 'rj': lad(s_main('P1'))['R_j0'],
                                                                              'c': '1'}}])),
                    [s_main('P0')['out'], s_main('P1')['out']])
        return verdict(tag + '_v', [s_main('P0')['out'], s_main('P1')['out'], p['out']])
    return scen(tag, go)


@check('V05', 'SV_DOMINANT — 모서리 하나의 sv_dominant = True → 표지 · 문장 금지')
def t_V05():
    v = sv_set('V05', 'sv_dominant')['v']
    return 'SV_DOMINANT' in (v or {}).get('flags', []), (v and v.get('flags'), v and v.get('stop'))


@check('V06', 'SV 소산 분담 없음 (sv_dominant 칸 없음 = NOT_COMPUTED) → SV_DOMINANT 와 같게')
def t_V06():
    v = sv_set('V06', 'sv_missing')['v']
    return 'SV_DOMINANT' in (v or {}).get('flags', []), (v and v.get('flags'), v and v.get('stop'))


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
                     '--plan', FX['plan'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out, '--show-results'], w)
    v = s_show()
    views = Path(v['out']) / 'views.jsonl'
    return (rc1 == 2 and n_calls(w) == 0 and v['rc'] == 0 and views.exists() and len(views.read_text().splitlines()) == 1,
            (rc1, v['rc'], views.exists()))


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
                   '--plan', FX['plan'], '--registration', FX['reg_ok'], '--max-hours', '1', '--out', out, '--dry-run'], w)
    lines = [x for x in so.splitlines() if 'bash ' in x]
    rjs = [re.search(r'CJUNC_RJ=(\S+)', x).group(1) for x in lines if 'CJUNC_RJ=' in x]
    return (rc == 0 and not out.exists() and n_calls(w) == 0 and rjs == ['inf', '0', '10000.0', '1000000.0', '100000000.0']
            and all('PTFE_STAMP=face_alpha' in x and 'SIGMA_FIBRE_BULK=1e4' in x and 'SIGMA_VGCF_OVERRIDE' not in x for x in lines),
            (rc, rjs, lines[:1]))


@check('X05', '등록 문서에 이 도구의 숫자 · 이름 · 문장이 있다 (상수 대조 · 사본 금지의 짝)')
def t_X05():
    t = FX['reg_text']
    need = ['1.63', '4.68', '1.8877', '0.454', '0.908', '1e-3', '10^0.5', '12', '0.02', '0.1 W', 'kit_SBE_vgcf100',
            'kit_DBE_sdcp1um_vgcf100', 'CALIB_IMPOSSIBLE', 'CALIB_EDGE', 'CALIB_UNIDENTIFIED', 'CALIB_UNCONFIRMED',
            'CALIB_NONMONOTONE', 'CALIB_LADDER_EXHAUSTED', 'NOT_COMPUTED', 'PASS_INFORMATIVE', 'CONSISTENT_WEAK', 'UNINFORMATIVE',
            'CALIB_ORIGIN_SENSITIVE', 'SV_DOMINANT', 'DIA_UNCHECKED', RR.SENTENCE_PASS]
    miss = [n for n in need if n not in t]
    consts = (RR.TARGET_SBE_MS == 1.63 and RR.EXP_DBE_MS == 4.68 and RR.CUR_GEN_DBE_MS == 1.8877 and RR.CONFIRM_TOL == 0.02
              and RR.TAU_MONO == 1e-3 and RR.NEIGHBOR_LOG10_MAX == 0.5 and RR.MAX_LADDER_POINTS == 12
              and RR.ORIGIN_SBE_MAX == 0.02 and RR.ORIGIN_DBE_FRAC_W == 0.1 and RR.SENS_SHIFT_FRAC_G0 == 0.1
              and RR.LADDER_START_LOG10 == (4.0, 6.0, 8.0) and RR.LADDER_EXT_LOG10 == 2.0 and RR.MAX_CONFIRM == 2
              and abs(RR.E_MIN - 0.02 / math.log(math.sqrt(10.0))) < 1e-15 and abs(RR.G0 - math.log(4.68 / 1.8877)) < 1e-15)
    return not miss and consts, (miss, consts)


@check('X06', '바닥 · 천장 극한 = 러너 env CJUNC_RJ=inf · 0 (런 순서 첫 둘) · 극한 팔 표지 rj_limit 대조')
def t_X06():
    ev = env_log(s_main('P0')['world'])
    return [e.get('CJUNC_RJ') for e in ev[:2]] == ['inf', '0'] and roles(s_main('P0'))[:2] == ['floor', 'ceiling'], (
        [e.get('CJUNC_RJ') for e in ev[:3]])


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


@check('M04', '변이: e_min 끔 (0) → L11 이 CALIB_UNIDENTIFIED 를 못 낸다')
def t_M04():
    def ev():
        r = run_L11('M04')
        return r['sum']['status'] == 'CALIB_UNIDENTIFIED', r['sum']['status']
    return mutant('M04', {'E_MIN': 0.0}, ev)


@check('M05', '변이: τ_mono 끔 (∞) → L14 가 CALIB_NONMONOTONE 을 못 낸다')
def t_M05():
    def ev():
        r = run_L14('M05')
        return r['sum']['status'] == 'CALIB_NONMONOTONE', r['sum']['status']
    return mutant('M05', {'TAU_MONO': math.inf}, ev)


@check('M06', '변이: 판정 입력 sha256 대조 끔 → S22 가 INPUT_SHA_MISMATCH 를 못 낸다')
def t_M06():
    return mutant('M06', {'sha_mismatch': lambda path, want: None}, lambda: eval_S22(run_S22('M06')))


@check('M07', '변이: 점 수 상한 12 → 13 → L16 (런 정확히 12) 이 떨어진다')
def t_M07():
    def ev():
        r = run_L16('M07')
        return r['sum']['status'] == 'CALIB_LADDER_EXHAUSTED' and len(roles(r)) == 12, (r['sum']['status'], len(roles(r)))
    return mutant('M07', {'MAX_LADDER_POINTS': 13}, ev)


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

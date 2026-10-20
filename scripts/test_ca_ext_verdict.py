#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② B6 — 판정기 `scripts/sdcp_gain_verdict.py` 의 다음 세대 소비자 검사 (시험 먼저 · 2026-10-20).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §6 (수렴 증서 · 증서 없음 / 실패 = 미게시) · §7 (세대 ·
`ca_ext_record_ok` = producer · check_arm · 판정기가 같은 함수 · 현 세대 p2 ↔ 다음 세대 p3ca 섞임 = 거부).
코호트 = **payload 실물** (`test_ca_ext_b6.make_fixture` · vox 1.0 · origin factorial {0, 0.5}³ · SBE = SDCP 없음 · DBE = SDCP 점 하나)
— 판정기가 읽는 그대로의 팔 JSON.  변조는 그 JSON (읽은 행의 매니페스트 · step3) 에 직접 한다.

  python3 scripts/test_ca_ext_verdict.py                       # 전부
  python3 scripts/test_ca_ext_verdict.py --only V1,V3          # 이름 접두
  python3 scripts/test_ca_ext_verdict.py --old-verdict PATH    # V4 — 옛 세대 코호트의 판정 JSON 을 고치기 전 판정기와 바이트 대조

묶음:
  V0  정상 코호트 양성 — 접합 + rtol 8 origin × 두 침대 → 계약 통과 (require_arms 8) · face_alpha + rtol · 접합 LEAN 3 (이온 증서) 통과
  V1  변조 팔 — 증거 칸 하나 (영수증 상태 · 표지 · 원장 수 · 진단 표 · 단락 · 거부 사유) → HOLD (CAEXT) · 규약 id 는 그대로인 변조
  V2  섞인 코호트 — p2 (끔) 팔이 같은 origin 의 p3ca 자리에 · 두 침대가 서로 다른 세대 → HOLD GENERATION_MIX
  V3  증서 — 칸 없음 · ok False · σ 결합 깨짐 · rtol 없이 돈 접합 · face_alpha 팔 (실물) · LEAN 3 이온 증서 없음 → HOLD NEXTGEN_UNPUBLISHED
  V4  옛 세대 (p2) 코호트 — 커밋된 봉인 코호트 (w4 · w4b) 가 새 사유로 HOLD 되지 않는다 (--old-verdict 면 판정 JSON 바이트 대조)
  V5  CLI `--seal-only` — 변조 · 섞임 · 증서 없음 디렉터리의 봉인 사유가 새 코드 (원값 누설 없음 · 정상 디렉터리는 계약 사유 없음)
⚠ PASS 는 소비자 계약의 증거이지 판정 (R) 의 물리 검증이 아니다.
"""
import argparse
import contextlib
import copy
import glob
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

import test_ca_ext_b6 as B6                            # noqa: E402 — 침대 · payload 호출 (사본 없음)
import run_contract as RC                              # noqa: E402
import sdcp_gain_verdict as V                          # noqa: E402

ARGS = None
TD = None
_ok, _fail = 0, []
CASES = []
NEW_CODES = ('GENERATION_MIX', 'NEXTGEN_UNPUBLISHED', 'CAEXT')


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


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


# ═════════════════════════ 코호트 만들기 (payload 실물) ═════════════════════════
ORIGINS = [(x, y, z) for x in ('0', '0.5') for y in ('0', '0.5') for z in ('0', '0.5')]
RT = ['--step3-rtol', '1e-12']
_BEDS = {}
_DIRS = {}


def make_bed(d, sdcp):
    """b6 픽스처 + 아래 판 ↔ 위 판을 잇는 **곧은 VGCF 한 가닥** (접합 없음 · 접합 사슬에서 6 µm).
    ⚠ 왜: vox 1.0 에서 origin 을 반 셀 (0.5 µm) 옮기면 접합 점 ↔ 가장 가까운 셀 중심이 r_port 0.30 µm 밖이라 instance 가 미실현이 되고
      (실측: origin (0, 0, 0.5) · 간선 0 · 미실현 1) 직렬 사슬만으로는 σ_e = 0 → payload 가 게시를 거부한다 (STEP3_NUMERIC_EVIDENCE).
      판정기 시험은 8 origin 코호트가 필요하므로 병렬 경로 하나를 더한다 (σ 값은 이 시험의 대상이 아니다)."""
    import numpy as np
    B6.make_fixture(d, sdcp=sdcp)
    ld = {k: np.load(os.path.join(d, f'{k}.npy')) for k in ('se', 'phase', 'fibre', 'fibre_kind', 'fibre_dia')}
    ln = B6._box(B6.line((30.5, 24.5, 0.3), (30.5, 24.5, 23.2), 47))
    n = len(ln)
    np.save(os.path.join(d, 'se.npy'), np.vstack([ld['se'], ln]))
    np.save(os.path.join(d, 'phase.npy'), np.concatenate([ld['phase'], np.full(n, 2, ld['phase'].dtype)]))
    np.save(os.path.join(d, 'fibre.npy'), np.concatenate([ld['fibre'], np.full(n, 3, ld['fibre'].dtype)]))
    np.save(os.path.join(d, 'fibre_kind.npy'), np.concatenate([ld['fibre_kind'], np.full(n, 1, ld['fibre_kind'].dtype)]))
    np.save(os.path.join(d, 'fibre_dia.npy'), np.concatenate([ld['fibre_dia'], np.ones(n, ld['fibre_dia'].dtype)]))
    return d


def beds():
    if not _BEDS:
        for bed, sdcp in (('SBE', False), ('DBE', True)):
            d = os.path.join(TD, f'bed_{bed}')
            os.makedirs(d)
            make_bed(d, sdcp=sdcp)
            _BEDS[bed] = d
    return _BEDS


def make_arm(bed, extra, origin, name, dest):
    """payload 한 팔 (실물) → dest/name.  rc ≠ 0 이면 그 사실을 돌려준다 (시험이 판단)."""
    d = beds()[bed]
    rc, log, _p = B6.run_payload(d, list(extra) + ['--step3-origin-shift', *origin], out=name)
    if rc == 0 and os.path.exists(os.path.join(d, name)):
        os.makedirs(dest, exist_ok=True)
        shutil.move(os.path.join(d, name), os.path.join(dest, name))
    return rc, log


def cohort(label, extra, origins=ORIGINS):
    """두 침대 × origin 들 → 디렉터리 (이름 = p2_<침대>_a<i>.json · 판정기의 침대 구분 = 파일 이름의 `_SBE_` · `_DBE_`)."""
    if label in _DIRS:
        return _DIRS[label]
    dest = os.path.join(TD, label)
    bad = []
    for i, o in enumerate(origins):
        for bed in ('SBE', 'DBE'):
            rc, log = make_arm(bed, extra, o, f'p2_{bed}_a{i}.json', dest)
            if rc != 0:
                bad.append((bed, i, rc, log.strip()[-300:]))
    _DIRS[label] = dest if not bad else None
    if bad:
        print(f'    ⚠ 코호트 {label} 를 못 만들었다: {bad[:2]}')
    return _DIRS[label]


CJ_RT = B6.OFF + B6.LEAN2 + B6.CJ + RT


def arms_of(d):
    return quiet(V.collect, d)[1]


def contract(arms, **kw):
    return quiet(V.validate_contract, arms, **kw)


def mutate(arms, bed, idx, fn):
    """arms 사본 — bed 의 idx 번째 행의 매니페스트 · step3 를 깊은 복사해 fn(man, s3) 로 바꾼다 (읽은 행 그대로 · 판정기가 보는 자리)."""
    out = {k: list(v) for k, v in arms.items()}
    r = dict(out[bed][idx])
    s3 = copy.deepcopy(r['_step3'])
    man = s3.get('manifest') if isinstance(s3.get('manifest'), dict) else copy.deepcopy(r['_manifest'])
    fn(man, s3)
    s3['manifest'] = man
    r['_step3'], r['_manifest'] = s3, man
    out[bed][idx] = r
    return out


def code_of(hold):
    return (hold or {}).get('hold_code')


# ═════════════════════════ V0 — 정상 코호트 양성 ═════════════════════════
@case('V0 정상 코호트 양성 — 접합 + rtol (8 origin × 두 침대) · face_alpha + rtol · 접합 LEAN 3')
def t_positive():
    d = cohort('cj_rt', CJ_RT)
    chk('V0a 코호트 16 팔을 만들었다 (payload rc 0)', d is not None and len(glob.glob(os.path.join(d, 'p2_*.json'))) == 16)
    if d is None:
        return
    arms = arms_of(d)
    m = arms['SBE'][0]['_manifest']
    chk('V0b 팔 = p3ca · ca_ext_record_ok · 증서 (다음 세대 게시 조건)',
        str(m.get('physics_protocol_id', '')).startswith('p3ca-') and RC.ca_ext_record_ok(m) == (True, None)
        and all(RC.next_gen_cert_ok(r['_step3'])[0] for k in arms for r in arms[k]), m.get('physics_protocol_id'))
    hold, info = contract(arms, require_arms=8)
    chk('V0c 계약 통과 (validate_contract · require_arms 8) — 새 게이트가 정상 다음 세대 코호트를 막지 않는다',
        hold is None and info.get('n_origin') == 8, (code_of(hold), (hold or {}).get('reason', '')[:300]))
    v = quiet(V.verdict, arms, require_arms=8)
    chk('V0d 판정까지 간다 (계약 사유 HOLD 없음 · 통계 게이트 SE 만 허용 · 값은 보지 않는다)',
        v.get('decision') in ('h0', 'h1', 'BOTH_REJECTED') or code_of(v) == 'SE_EXCEEDED', (v.get('decision'), code_of(v)))
    df = cohort('fa_rt', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2 + RT, origins=ORIGINS[:1])
    hold_f = contract(arms_of(df))[0] if df else {'hold_code': 'NO_COHORT'}
    chk('V0e face_alpha + rtol 두 팔 → 계약 통과 (ptfe_face 블록 · 증서)', df is not None and hold_f is None,
        (code_of(hold_f), (hold_f or {}).get('reason', '')[:300]))
    d3 = cohort('cj_rt_l3', B6.OFF + B6.LEAN3 + B6.CJ + RT, origins=ORIGINS[:1])
    hold_3 = contract(arms_of(d3), require_ionic=True)[0] if d3 else {'hold_code': 'NO_COHORT'}
    chk('V0f 접합 LEAN 3 + rtol 두 팔 → 계약 통과 (require_ionic · 이온 증서)', d3 is not None and hold_3 is None,
        (code_of(hold_3), (hold_3 or {}).get('reason', '')[:300]))


# ═════════════════════════ V1 — 변조 팔 ═════════════════════════
def _ev(man):
    return man['ca_ext']['cjunc']['evidence']


TAMPER = {
    '주 영수증 missing': lambda m, s: _ev(m)['receipts']['electronic_main'].update(status='missing'),
    '표지 다름': lambda m, s: _ev(m).update(label='탄소 접합'),
    '원장 수 합 깨짐 (n_edge + 1)': lambda m, s: _ev(m)['counts'].update(n_edge=_ev(m)['counts']['n_edge'] + 1),
    '진단 표 빠짐': lambda m, s: _ev(m).pop('diagnostics'),
    '단락 상태': lambda m, s: _ev(m)['solve'].update(short=True),
    '이온 영수증 applied_without_request': lambda m, s: _ev(m)['receipts'].update(ionic={'status': 'applied_without_request'}),
    '거부 사유 남음': lambda m, s: _ev(m).update(rejections=[{'code': 'self_s_min_missing', 'n': 1}]),
    '원장 지문 ≠ 솔브 영수증': lambda m, s: _ev(m)['receipts']['electronic_main'].update(fp_registry='f' * 32),
}


@case('V1 변조 팔 — 증거 칸 하나 → HOLD (ca_ext_record_ok · 규약 id 그대로)')
def t_tamper():
    d = _DIRS.get('cj_rt') or cohort('cj_rt', CJ_RT)
    if d is None:
        chk('V1 선행 (코호트)', False)
        return
    arms = arms_of(d)
    for i, (nm, fn) in enumerate(TAMPER.items()):
        bed, idx = ('SBE', 'DBE')[i % 2], i % 8
        a2 = mutate(arms, bed, idx, fn)
        man = a2[bed][idx]['_manifest']
        hold, _info = contract(a2, require_arms=8)
        chk(f'V1 [{nm}] → HOLD CAEXT (규약 id · protocol_ok 그대로 = 이 판정기의 소비자 검사가 잡는다)',
            RC.protocol_ok(man) == (True, None) and code_of(hold) == 'CAEXT' and 'ca_ext' in (hold or {}).get('reason', ''),
            (RC.protocol_ok(man), code_of(hold), (hold or {}).get('reason', '')[:200]))


# ═════════════════════════ V2 — 섞인 코호트 ═════════════════════════
@case('V2 섞인 코호트 — 현 세대 p2 ↔ 다음 세대 p3ca → HOLD GENERATION_MIX')
def t_mix():
    d = _DIRS.get('cj_rt') or cohort('cj_rt', CJ_RT)
    dp = cohort('p2_rt', B6.OFF + B6.LEAN2 + RT, origins=ORIGINS[:1])
    if d is None or dp is None:
        chk('V2 선행 (코호트)', False)
        return
    arms = arms_of(d)
    p2 = arms_of(dp)
    chk('V2a 끔 팔 = p2 세대 (같은 침대 · 같은 origin 0)', str(p2['SBE'][0]['_manifest'].get('physics_protocol_id', '')).startswith('p2-'))
    mix = {k: list(v) for k, v in arms.items()}
    mix['SBE'][0] = dict(p2['SBE'][0], file='p2_SBE_a0.json')
    mix['DBE'][0] = dict(p2['DBE'][0], file='p2_DBE_a0.json')
    hold, _i = contract(mix, require_arms=8)
    chk('V2b p3ca 코호트의 a0 두 팔을 같은 origin 의 p2 팔로 → HOLD GENERATION_MIX (사유에 두 세대 이름)',
        code_of(hold) == 'GENERATION_MIX' and 'p2' in hold.get('reason', '') and 'p3ca' in hold.get('reason', ''),
        (code_of(hold), (hold or {}).get('reason', '')[:240]))
    two = {'SBE': [p2['SBE'][0]], 'DBE': [arms['DBE'][0]]}
    hold2, _i = contract(two)
    chk('V2c 두 침대가 서로 다른 세대 (SBE p2 · DBE p3ca · 같은 origin) → HOLD GENERATION_MIX',
        code_of(hold2) == 'GENERATION_MIX', (code_of(hold2), (hold2 or {}).get('reason', '')[:240]))
    hold3, _i = contract({'SBE': [p2['SBE'][0]], 'DBE': [p2['DBE'][0]]})
    chk('V2d 끔 팔 둘 (p2 만) = 세대 섞임 아님 (새 게이트가 옛 세대를 막지 않는다)',
        code_of(hold3) not in NEW_CODES, (code_of(hold3), (hold3 or {}).get('reason', '')[:200]))


# ═════════════════════════ V3 — 수렴 증서 ═════════════════════════
@case('V3 증서 없음 / 실패 = 미게시 팔 → HOLD NEXTGEN_UNPUBLISHED')
def t_cert():
    d = _DIRS.get('cj_rt') or cohort('cj_rt', CJ_RT)
    if d is None:
        chk('V3 선행 (코호트)', False)
        return
    arms = arms_of(d)
    cert_bad = {
        '증서 칸 없음': lambda m, s: s.pop('conv_cert'),
        '증서 ok False (ⓑ 실패)': lambda m, s: s['conv_cert'].update(ok=False, pass_b=False),
        '증서 σ ≠ 결과 σ (결합 깨짐)': lambda m, s: s['conv_cert'].update(sigma=2.0 * float(s['conv_cert']['sigma'])),
        '증서 ok ↔ pass 모순': lambda m, s: s['conv_cert'].update(pass_c=False),
    }
    for i, (nm, fn) in enumerate(cert_bad.items()):
        a2 = mutate(arms, 'SBE', 3 + i, fn)
        hold, _i = contract(a2, require_arms=8)
        chk(f'V3 [{nm}] → HOLD NEXTGEN_UNPUBLISHED (미게시 팔 1 · 사유에 그 팔)',
            code_of(hold) == 'NEXTGEN_UNPUBLISHED' and f'p2_SBE_a{3 + i}.json' in (hold or {}).get('unpublished', [])
            and (hold or {}).get('n_unpublished') == 1, (code_of(hold), (hold or {}).get('reason', '')[:200]))
    dn = os.path.join(TD, 'cj_nocert')
    rc, log = make_arm('SBE', B6.OFF + B6.LEAN2 + B6.CJ, ORIGINS[0], 'p2_SBE_a0.json', dn)
    if rc == 0:
        a2 = {k: list(v) for k, v in arms.items()}
        a2['SBE'][0] = arms_of(dn)['SBE'][0]
        hold, _i = contract(a2, require_arms=8)
        chk('V3e rtol 없이 돈 접합 팔 (실물 · 증서 칸 없음) 이 섞이면 → HOLD NEXTGEN_UNPUBLISHED',
            code_of(hold) == 'NEXTGEN_UNPUBLISHED' and 'CERT|absent|' in (hold or {}).get('reason', ''),
            (code_of(hold), (hold or {}).get('reason', '')[:200]))
    else:
        chk('V3e rtol 없이 돈 접합 팔 (실물)', False, (rc, log.strip()[-200:]))
    df = _DIRS.get('fa_rt') or cohort('fa_rt', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2 + RT, origins=ORIGINS[:1])
    dfn = os.path.join(TD, 'fa_nocert')
    rc, log = make_arm('DBE', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2, ORIGINS[0], 'p2_DBE_a0.json', dfn)
    if rc == 0 and df:
        af = arms_of(df)
        af['DBE'][0] = arms_of(dfn)['DBE'][0]
        hold, _i = contract(af)
        chk('V3f rtol 없이 돈 face_alpha 팔 (실물) → HOLD NEXTGEN_UNPUBLISHED', code_of(hold) == 'NEXTGEN_UNPUBLISHED',
            (code_of(hold), (hold or {}).get('reason', '')[:200]))
    else:
        chk('V3f rtol 없이 돈 face_alpha 팔 (실물)', False, (rc, log.strip()[-200:]))
    d3 = _DIRS.get('cj_rt_l3') or cohort('cj_rt_l3', B6.OFF + B6.LEAN3 + B6.CJ + RT, origins=ORIGINS[:1])
    if d3:
        a3 = mutate(arms_of(d3), 'DBE', 0, lambda m, s: s.pop('ion_conv_cert'))
        hold, _i = contract(a3, require_ionic=True)
        chk('V3g 이온을 푼 다음 세대 팔 (LEAN 3) 의 이온 증서 없음 → HOLD NEXTGEN_UNPUBLISHED (ionic)',
            code_of(hold) == 'NEXTGEN_UNPUBLISHED' and 'NEXTGEN|ionic|' in (hold or {}).get('reason', ''),
            (code_of(hold), (hold or {}).get('reason', '')[:200]))
    else:
        chk('V3g LEAN 3 코호트', False)


# ═════════════════════════ V4 — 옛 세대 코호트 ═════════════════════════
def _cohort_dirs():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'docs/data/**/p2_*.json'), recursive=True)):
        d = os.path.dirname(f)
        if d not in out:
            out.append(d)
    return out


@case('V4 옛 세대 (p2) 코호트 — 새 사유로 HOLD 되지 않는다 (--old-verdict 면 판정 JSON 바이트 대조)')
def t_old_gen():
    for name in ('w4_ptfe_centerline_20260827', 'w4b_ptfe_off_20260827'):
        arms = arms_of(os.path.join(ROOT, 'docs/data', name))
        v = quiet(V.verdict, arms, require_arms=8)
        chk(f'V4a [{name}] 봉인 코호트 판정이 새 사유 ({"·".join(NEW_CODES)}) 가 아니다 · 모든 팔 p2',
            code_of(v) not in NEW_CODES and all(str(r['_manifest'].get('physics_protocol_id', '')).startswith('p2-')
                                                  for k in arms for r in arms[k]), (v.get('decision'), code_of(v)))
    if not ARGS.old_verdict:
        print('    (--old-verdict 없음 — 바이트 대조 건너뜀)')
        return
    import importlib.util
    spec = importlib.util.spec_from_file_location('sdcp_gain_verdict_old', ARGS.old_verdict)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    dirs = _cohort_dirs()
    diff = []
    for d in dirs:
        a_new = quiet(V.collect, d)[1]
        a_old = quiet(old.collect, d)[1]
        for kw in ({}, {'require_arms': 8}):
            j_new = json.dumps(quiet(V.verdict, a_new, **kw), sort_keys=True, default=str)
            j_old = json.dumps(quiet(old.verdict, a_old, **kw), sort_keys=True, default=str)
            if j_new != j_old:
                diff.append((os.path.relpath(d, ROOT), kw))
    chk(f'V4b 커밋된 팔 디렉터리 {len(dirs)} 개 × (require_arms 없음 · 8) — 판정 JSON 이 고치기 전 판정기와 바이트 같다',
        len(dirs) >= 10 and not diff, diff[:4])


# ═════════════════════════ V5 — CLI --seal-only ═════════════════════════
def _seal(d):
    p = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'sdcp_gain_verdict.py'), '--dir', d, '--seal-only',
                        '--require-arms', '8'], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def _copy_mut(src, label, fname, fn):
    dst = os.path.join(TD, label)
    shutil.copytree(src, dst)
    p = os.path.join(dst, fname)
    data = json.load(open(p, encoding='utf-8'))
    s3 = (data.get('mpm_metrics') or {}).get('step3')
    fn(s3['manifest'], s3)
    json.dump(data, open(p, 'w', encoding='utf-8'))
    return dst


@case('V5 CLI --seal-only — 변조 · 섞임 · 증서 없음의 봉인 사유 (원값 누설 없음)')
def t_cli():
    d = _DIRS.get('cj_rt') or cohort('cj_rt', CJ_RT)
    dp = _DIRS.get('p2_rt') or cohort('p2_rt', B6.OFF + B6.LEAN2 + RT, origins=ORIGINS[:1])
    if d is None or dp is None:
        chk('V5 선행 (코호트)', False)
        return
    rc0, log0 = _seal(d)
    chk('V5a 정상 디렉터리 — 봉인 사유가 계약 (새 코드) 이 아니다 · 비 · h0/h1 을 안 찍는다',
        not any(c in log0 for c in NEW_CODES) and 'ratio' not in log0 and '봉인' in log0, log0[-300:])
    d_t = _copy_mut(d, 'cli_tamper', 'p2_DBE_a2.json', TAMPER['표지 다름'])
    d_c = _copy_mut(d, 'cli_nocert', 'p2_SBE_a5.json', lambda m, s: s.pop('conv_cert'))
    d_m = os.path.join(TD, 'cli_mix')
    shutil.copytree(d, d_m)
    shutil.copy2(os.path.join(dp, 'p2_SBE_a0.json'), os.path.join(d_m, 'p2_SBE_a0.json'))
    for nm, dd, code in (('변조 (표지)', d_t, 'CAEXT'), ('증서 없음', d_c, 'NEXTGEN_UNPUBLISHED'), ('세대 섞임', d_m, 'GENERATION_MIX')):
        rc, log = _seal(dd)
        chk(f'V5 [{nm}] → 봉인 깨짐 (rc 1) · 근거에 `{code}` 사유', rc == 1 and '깨짐' in log
            and (code in log or (code == 'CAEXT' and 'ca_ext 기록' in log)), (rc, log[-300:]))


def main():
    global ARGS, TD
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--old-verdict', default='', help='고치기 전 sdcp_gain_verdict.py 사본 (V4 판정 JSON 바이트 대조)')
    ap.add_argument('--only', default='', help='쉼표로 나눈 이름 접두 (예: V1,V3)')
    ap.add_argument('--keep', action='store_true', help='임시 디렉터리를 남긴다 (진단)')
    ARGS = ap.parse_args()
    TD = tempfile.mkdtemp(prefix='ca_ext_verdict_')
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    try:
        for tag, fn in CASES:
            if only and not any(tag.startswith(o) for o in only):
                continue
            print(f'\n── {tag}')
            try:
                fn()
            except Exception as e:                              # noqa: BLE001 — 옛 코드 (게이트 없음) 도 시험 단위로 기록
                chk(f'{tag.split()[0]}: 실행', False, f'{type(e).__name__}: {e}')
    finally:
        if ARGS.keep:
            print(f'\n  (임시 디렉터리 남김: {TD})')
        else:
            shutil.rmtree(TD, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()

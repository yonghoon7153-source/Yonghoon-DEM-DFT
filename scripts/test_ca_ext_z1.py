#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② 2 일 차 Z1 — 러너 · 판정기 굳히기 (시험 먼저 · 2026-10-20).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §1-2 #1 · #2 (VGCF σ = 두 전극 같은 값 · 직경 보존 ·
Endo 단섬유 1 × 10⁴ S/cm → vox 0.15 에서 7,853.98 S/cm) · §6 (수렴 증서) · §7 (세대 · 영수증 · 네 방어) · 등록 R §10 (멈춤 목록).

  python3 scripts/test_ca_ext_z1.py                        # 전부 (payload · 러너 실물 · 60 s 안 목표)
  python3 scripts/test_ca_ext_z1.py --only Z1,Z4           # 이름 접두
  python3 scripts/test_ca_ext_z1.py --old-scripts DIR      # ZB — 끔 경로: 고치기 전 scripts/ 사본의 run_contract 와 함수 대조

묶음:
  Z1  `SIGMA_FIBRE_BULK` — 손계산 (vox 0.15 · 1e4 → 7,853.98 · vox 0.4 · 100 → 11.0447 · vox 0.125 · 1e4 → 11,309.7) · 러너 발사 전 검사
      (값 · `SIGMA_VGCF_OVERRIDE` 동시 = 거부) · 영수증 선택 칸 · 이름 태그 · payload 기록 (bulk · 식 이름) + 다시 계산 대조 · 러너 실물
  Z2  다음 세대 노브 (`CJUNC=1` · `PTFE_STAMP=face_alpha` · `SDCP_MOD_C`) = `STEP3_RTOL` 필수 — 팔 시작 전 거부 (기본값 없음)
  Z3  `sdcp_anchor_v2_chain.py` — 부모 셸의 다음 세대 노브 env = 거부 (지우지 않는다)
  Z4  `compare_dirs` — `ca_ext` 하위 블록 = 등록 축 (`ca_ext.<하위>` · `ca_ext.<하위>.<칸>`) · 증거 = 결과 · 등록 밖 차이 = HOLD
  Z5  판정기 `--expect-generation` (설계 §7 네 번째 방어) — 코호트 세대 (p2 · p3ca) 를 선언하고 다르면 거부
  ZB  (--old-scripts) 끔 경로 — 고치기 전 run_contract 와 영수증 digest · 발사 전 검사 · 이름 태그 · receipt_match 가 같다
⚠ PASS 는 배선 · 계약의 증거이지 R_j 값 · 판정 (R) 의 물리 검증이 아니다.
"""
import argparse
import contextlib
import glob
import hashlib
import importlib.util
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

import numpy as np                                     # noqa: E402

import test_ca_ext_b6 as B6                            # noqa: E402 — 침대 · payload 호출 (사본 없음)
import test_ca_ext_runner as TR                        # noqa: E402 — 러너 호출 · 가짜 python3 · 설정부 탐침 (사본 없음)
import run_contract as RC                              # noqa: E402
import sdcp_gain_verdict as V                          # noqa: E402

ARGS = None
TD = None
_ok, _fail = 0, []
CASES = []
RT = ['--step3-rtol', '1e-12']
CJ_RT_ENV = dict(TR.CJ_ENV, STEP3_RTOL='1e-12')
#: B6 (d9404ccb2) 의 손잡이 아홉 — 이름 · 순서 그대로 남아야 한다 (Z1 은 새 이름 보탬만)
ORIG9 = ('CJUNC', 'CJUNC_RJ', 'CJUNC_LEN_LAW', 'CJUNC_UNREG_LAW', 'CJUNC_S_MIN_UM', 'CJUNC_TOL_FF_UM', 'CJUNC_PTFE_JLAW',
         'SDCP_MOD_C', 'STEP3_RTOL')


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


def probs(env, **kw):
    """run_contract.runner_ca_ext → 문제 목록 (구조화 사유 문자열)."""
    return RC.runner_ca_ext(env, **kw)['problems']


def has_code(ps, code):
    return any(p.startswith(f'RUNNER_CA_EXT|{code}|') for p in ps)


def _hand(bulk, vox, d=0.15):
    """독립 손계산 — σ_vox = σ_bulk · (π d²/4) / vox² (상대 Ø 1 · 유효숫자 6 자리 = 러너가 payload 에 넘기는 표기)."""
    return f'{bulk * math.pi * d * d / 4.0 / (vox * vox):.6g}'


# ═════════════════════════ Z1 — SIGMA_FIBRE_BULK ═════════════════════════
@case('Z1a 손계산 — step3_sigma.vgcf_sigma_from_bulk (러너 · payload 가 같은 함수) ↔ 독립 식 · 설계 §1-2 #2 값')
def t_hand():
    import step3_sigma as S3
    import additives as AD
    fn = getattr(S3, 'vgcf_sigma_from_bulk', None)
    chk('Z1a0 함수 · 식 이름 · 기준 지름 상수가 있다 (VGCF_DIA_REF_UM = additives.VGCF_D)', callable(fn)
        and isinstance(getattr(S3, 'VGCF_SIGMA_RULE', None), str) and getattr(S3, 'VGCF_DIA_REF_UM', None) == AD.VGCF_D,
        (callable(fn), getattr(S3, 'VGCF_SIGMA_RULE', None), getattr(S3, 'VGCF_DIA_REF_UM', None)))
    if not callable(fn):
        return
    #  침대 꼴: VGCF (상 2 · 상대 Ø 1) + PTFE (상 4 · Ø 분포 — 식에 들어가면 안 된다) + SE (상 1 · Ø 0)
    dia = np.concatenate([np.ones(40), np.linspace(0.3, 2.5, 25), np.zeros(10)])
    ph = np.concatenate([np.full(40, 2), np.full(25, 4), np.full(10, 1)]).astype(np.int32)
    want = {(1e4, 0.15): '7853.98', (100.0, 0.4): '11.0447', (1e4, 0.125): '11309.7', (100.0, 0.15): '78.5398',
            (100.0, 1.0): '1.76715', (1e4, 1.0): '176.715', (1e3, 0.15): '785.398'}
    got = {k: fn(k[0], dia, ph, k[1]) for k in want}
    chk('Z1a1 설계 §1-2 #2 손계산 — vox 0.15 · 1e4 → 7853.98 · vox 0.4 · 100 → 11.0447 (옛 값 재현) · vox 0.125 · 1e4 → 11309.7 · '
        '옛 기본 (100 · vox 0.15) 78.5398 · Endo ÷10 (1e3) 785.398', got == want, got)
    chk('Z1a2 독립 식 σ_bulk·π·0.15²/4/vox² 와 일곱 점 모두 같다 (PTFE · SE 점은 식에 안 들어간다)',
        all(got[k] == _hand(*k) for k in want), {k: (got[k], _hand(*k)) for k in want})
    bad = []
    for nm, (d2, p2) in {'VGCF Ø 비균일': (np.concatenate([np.ones(5), np.full(5, 1.3)]), np.full(10, 2)),
                         'VGCF 없음': (np.ones(10), np.full(10, 4)),
                         '길이 다름': (np.ones(10), np.full(9, 2))}.items():
        try:
            fn(1e4, d2, p2, 0.15)
            bad.append(nm)
        except ValueError:
            pass
    chk('Z1a3 VGCF Ø 비균일 · VGCF 없음 · 길이 다름 = ValueError (러너 옛 판의 ABORT 와 같은 조건 · 조용한 강제 없음)', not bad, bad)
    chk('Z1a4 식 이름이 기준 지름을 말한다 (기록만 봐도 식이 정해진다)', '0.15' in S3.VGCF_SIGMA_RULE and 'diameter' in S3.VGCF_SIGMA_RULE,
        S3.VGCF_SIGMA_RULE)
    bad = []
    for nm, (b, v) in {'넘침 (bulk 1e308 · vox 0.001 → σ inf)': (1e308, 0.001), '언더플로 (bulk 1e-320 · vox 1000 → σ 0)': (1e-320, 1000.0),
                       'bulk nan': (float('nan'), 0.15), 'bulk inf': (float('inf'), 0.15), 'bulk 0': (0.0, 0.15)}.items():
        try:
            bad.append((nm, fn(b, dia, ph, v)))
        except ValueError:
            pass
    chk('Z1a5 결과 σ 가 유한 > 0 이 아니면 (넘침 · 언더플로 · nan · inf · 0) ValueError — "inf" · "0" 문자열을 payload 에 넘기지 않는다',
        not bad, bad)


@case('Z1b 러너 발사 전 검사 — SIGMA_FIBRE_BULK 값 · SIGMA_VGCF_OVERRIDE 동시 = 거부 · 영수증 선택 칸')
def t_runner_contract():
    names = [n for n, _s, _k in RC.RUNNER_CA_EXT_ENV]
    chk('Z1b0 손잡이 표에 SIGMA_FIBRE_BULK (선언 칸 sigma_vgcf_bulk_S_cm) — 기존 아홉은 그대로 (이름 · 순서)',
        ('SIGMA_FIBRE_BULK', None, 'sigma_vgcf_bulk_S_cm') in RC.RUNNER_CA_EXT_ENV and tuple(names[:9]) == ORIG9, names)
    out = RC.runner_ca_ext({'SIGMA_FIBRE_BULK': '1e4'})
    import step3_sigma as S3
    rule = getattr(S3, 'VGCF_SIGMA_RULE', '<없음>')
    chk('Z1b1 SIGMA_FIBRE_BULK=1e4 → 문제 없음 · 영수증 = bulk 10000.0 (float) + 식 이름', out['problems'] == []
        and out['receipt'] == {'sigma_vgcf_bulk_S_cm': 10000.0, 'sigma_vgcf_rule': rule}, out)
    same = [RC.runner_ca_ext({'SIGMA_FIBRE_BULK': v})['receipt'] for v in ('10000', '1E4', '1.0e4', '1e+4', '10000.000')]
    chk('Z1b2 같은 값 다른 표기 (10000 · 1E4 · 1.0e4 · 1e+4 · 10000.000) = 같은 영수증 (정규 float)', all(s == out['receipt'] for s in same),
        same)
    both = probs({'SIGMA_FIBRE_BULK': '1e4'}, sigma_vgcf_override='7853.98')
    chk('Z1b3 SIGMA_FIBRE_BULK + SIGMA_VGCF_OVERRIDE → RUNNER_CA_EXT|SIGMA_VGCF_BOTH| (구조화 사유 · 설계 §7)',
        has_code(both, 'SIGMA_VGCF_BOTH'), both)
    both0 = probs({'SIGMA_FIBRE_BULK': 'nan'}, sigma_vgcf_override='0')
    chk('Z1b4 값이 나빠도 동시 거부는 따로 이름을 댄다 (bulk nan + override 0 → SIGMA_VGCF_BOTH · VALUE 둘 다)',
        has_code(both0, 'SIGMA_VGCF_BOTH') and has_code(both0, 'VALUE'), both0)
    bad = {}
    for v in ('nan', 'inf', '1e999', '-1e4', '0', '0.0', '1e4 ', ' 1e4', '١٠', '1_000', '$HOME', '0x10', '1e4x', '+1e4'):
        ps = probs({'SIGMA_FIBRE_BULK': v})
        if not has_code(ps, 'VALUE'):
            bad[v] = ps
    chk('Z1b5 나쁜 값 열넷 (nan · inf · 넘침 · 음수 · 0 · 공백 · 유니코드 숫자 · 밑줄 · 변수 · 16 진 · 꼬리 글자 · 부호) → VALUE',
        not bad, bad)
    chk('Z1b6 빈 값 = 끔 (옛 영수증 · 문제 없음)', RC.runner_ca_ext({'SIGMA_FIBRE_BULK': ''}) == {'receipt': {}, 'problems': []},
        RC.runner_ca_ext({'SIGMA_FIBRE_BULK': ''}))
    combo = RC.runner_ca_ext(dict(CJ_RT_ENV, SIGMA_FIBRE_BULK='1e4'), lean='2')
    chk('Z1b7 다음 세대 판정 런 꼴 (접합 + rtol + bulk) → 문제 없음 · 영수증 = 요청 · rtol · bulk · 식 이름',
        combo['problems'] == [] and combo['receipt'].get('sigma_vgcf_bulk_S_cm') == 1e4 and 'ca_ext_request' in combo['receipt']
        and combo['receipt'].get('step3_rtol') == 1e-12, combo)


@case('Z1c 이름 태그 · payload 인자 · 영수증 digest — 끔 = 옛 그대로 · 켬 = 옛 팔과 다른 이름')
def t_view():
    import step3_sigma as S3
    rule = getattr(S3, 'VGCF_SIGMA_RULE', 'x')
    rec = {'sigma_vgcf_bulk_S_cm': 1e4, 'sigma_vgcf_rule': rule}
    try:
        v = RC.runner_ca_ext_view(rec)
    except Exception as e:                                   # noqa: BLE001
        v = {'_err': f'{type(e).__name__}: {e}'}
    chk('Z1c1 영수증 (bulk 1e4) → payload 인자 ` --sigma-vgcf-bulk 10000.0` · 태그 `_fb10000` (OUTDIR · 팔 이름) · 값 줄 10000.0',
        v.get('flags') == ' --sigma-vgcf-bulk 10000.0' and v.get('tag') == '_fb10000' and v.get('arm_tag') == '_fb10000'
        and v.get('vgcf_bulk') == '10000.0' and v.get('expect') == '', v)
    off = RC.runner_ca_ext_view({})
    chk('Z1c2 끔 영수증 → 다섯 칸 다 빈 문자열 (옛 조립 그대로)',
        off == {'flags': '', 'expect': '', 'tag': '', 'arm_tag': '', 'vgcf_bulk': ''}, off)
    tags = {b: RC.runner_ca_ext_view({'sigma_vgcf_bulk_S_cm': b, 'sigma_vgcf_rule': rule}).get('tag') for b in (2.5, 25.0, 1e3, 1e20)}
    chk('Z1c3 무손실 태그 — 2.5 → _fb2p5 · 25 → _fb25 · 1e3 → _fb1000 · 1e20 → _fb1e20',
        tags == {2.5: '_fb2p5', 25.0: '_fb25', 1e3: '_fb1000', 1e20: '_fb1e20'}, tags)
    full = RC.runner_ca_ext(dict(CJ_RT_ENV, SIGMA_FIBRE_BULK='1e4'), lean='2')['receipt']
    vf = RC.runner_ca_ext_view(full) if full else {}
    chk('Z1c4 접합 + rtol + bulk → 태그 = _cj… · _rt1em12 · _fb10000 순 · 인자 끝 = --sigma-vgcf-bulk 10000.0',
        bool(re.fullmatch(r'_cj1000000_[0-9a-f]{8}_rt1em12_fb10000', vf.get('tag', '')))
        and vf.get('flags', '').endswith(' --step3-rtol 1e-12 --sigma-vgcf-bulk 10000.0'), vf)
    fa = RC.runner_ca_ext({'SIGMA_FIBRE_BULK': '1e4', 'STEP3_RTOL': '1e-12'}, ptfe_stamp='face_alpha', lean='2')['receipt']
    vfa = RC.runner_ca_ext_view(dict(fa, ptfe_stamp='face_alpha')) if fa else {}
    chk('Z1c5 face_alpha + rtol + bulk → 팔 태그 `_fa_rt1em12_fb10000`', vfa.get('arm_tag') == '_fa_rt1em12_fb10000', vfa)
    base = json.load(open(sorted(glob.glob(os.path.join(ROOT, 'docs/data/**/run_receipt.json'), recursive=True))[0], encoding='utf-8'))
    d0 = RC.receipt_digest(base)
    d1 = RC.receipt_digest(dict(base, **rec))
    chk('Z1c6 digest — bulk 칸이 없으면 그대로 · 있으면 다르다 (옛 OUTDIR · 코호트 이름 보존 · 새 설정은 새 디렉터리)',
        d0 == RC.receipt_digest(dict(base)) and d1 != d0, (d0, d1))
    flag = [o for o, (c, f) in RC.CLI_ACCOUNTING.items() if f and 'sigma_vgcf_bulk_S_cm' in f]
    chk('Z1c7 payload 플래그 `--sigma-vgcf-bulk` = CLI 회계 record (기록 · 규약 해시 밖 — σ 자체는 --sigma-vgcf 가 규약 축)',
        flag == ['--sigma-vgcf-bulk'] and RC.CLI_ACCOUNTING['--sigma-vgcf-bulk'][0] == 'record', flag)
    bad = {}
    for nm, r in {'bulk = True (bool)': {'sigma_vgcf_bulk_S_cm': True, 'sigma_vgcf_rule': rule},
                  'bulk = 문자열 "1e4"': {'sigma_vgcf_bulk_S_cm': '1e4', 'sigma_vgcf_rule': rule},
                  'bulk = nan': {'sigma_vgcf_bulk_S_cm': float('nan'), 'sigma_vgcf_rule': rule},
                  'bulk = 0': {'sigma_vgcf_bulk_S_cm': 0.0, 'sigma_vgcf_rule': rule},
                  '식 이름 없음': {'sigma_vgcf_bulk_S_cm': 1e4},
                  '식 이름 = 빈 문자열': {'sigma_vgcf_bulk_S_cm': 1e4, 'sigma_vgcf_rule': ''},
                  '식 이름 = 수': {'sigma_vgcf_bulk_S_cm': 1e4, 'sigma_vgcf_rule': 3}}.items():
        try:
            bad[nm] = RC.runner_ca_ext_view(r)
        except ValueError:
            pass
    chk('Z1c8 손으로 바뀐 영수증 (bulk = bool · 문자열 · nan · 0 · 식 이름 없음 · 빈 · 수) → 이름 태그를 만들지 않는다 (ValueError · fail-closed)',
        not bad, bad)


@case('Z1d receipt_match — 영수증 bulk · 식 이름 ↔ 매니페스트 (없음 · 다름 · 요청 안 한 기록)')
def t_match():
    import step3_sigma as S3
    rule = getattr(S3, 'VGCF_SIGMA_RULE', 'x')
    rec = {'sigma_vgcf_bulk_S_cm': 1e4, 'sigma_vgcf_rule': rule}
    man_ok = {'sigma_vgcf_bulk_S_cm': 10000.0, 'sigma_vgcf_rule': rule}
    cases = {
        '같음': (rec, man_ok, None),
        '매니페스트에 기록 없음': (rec, {}, 'RCPT|sigma_vgcf_bulk_S_cm|missing|'),
        'bulk 다름 (1e3)': (rec, dict(man_ok, sigma_vgcf_bulk_S_cm=1e3), 'RCPT|sigma_vgcf_bulk_S_cm|differ|'),
        '식 이름 다름': (rec, dict(man_ok, sigma_vgcf_rule=rule + '_v9'), 'RCPT|sigma_vgcf_rule|differ|'),
        '식 이름 없음': (rec, {'sigma_vgcf_bulk_S_cm': 1e4}, 'RCPT|sigma_vgcf_rule|missing|'),
        '요청 안 한 기록 (영수증 끔 · 팔에 bulk)': ({}, man_ok, 'RCPT|sigma_vgcf_bulk_S_cm|unrequested|'),
        'bulk nan': (rec, dict(man_ok, sigma_vgcf_bulk_S_cm=float('nan')), 'RCPT|sigma_vgcf_bulk_S_cm|differ|'),
    }
    for nm, (r, m, want) in cases.items():
        ok, why = RC.receipt_match(r, m)
        chk(f'Z1d [{nm}] → {"통과" if want is None else want}', (ok and why is None) if want is None
            else (not ok and str(why).startswith(want)), (ok, why))


_PAY = {}


def _pay(label, extra, drop=()):
    """b6 침대 (vox 1.0 · SBE 꼴) 에서 payload 한 번 → (rc, 로그, 매니페스트)."""
    if label in _PAY:
        return _PAY[label]
    d = os.path.join(TD, 'pay_bed')
    if not os.path.isdir(d):
        os.makedirs(d)
        B6.make_fixture(d, sdcp=False)
    rc, log, data = B6.run_payload(d, list(extra), out=f'{label}.json', drop=drop)
    _PAY[label] = (rc, log, B6.man_of(data) if data else {})
    return _PAY[label]


@case('Z1e payload — --sigma-vgcf-bulk 기록 (bulk · 식 이름) · 같은 함수로 다시 계산해 --sigma-vgcf 와 대조 · 끔 = 키 없음')
def t_payload():
    import step3_sigma as S3
    rule = getattr(S3, 'VGCF_SIGMA_RULE', 'x')
    L = B6.OFF + B6.LEAN2
    rc, log, m = _pay('fb_ok', L + ['--sigma-vgcf', '176.715', '--sigma-vgcf-bulk', '1e4'])
    rc0, log0, m0 = _pay('fb_off_same_sigma', L + ['--sigma-vgcf', '176.715'])
    chk('Z1e1 bulk 1e4 · σ 176.715 (vox 1.0 손계산) → rc 0 · 매니페스트 σ 176.715 · bulk 10000.0 · 식 이름',
        rc == 0 and m.get('sigma_vgcf_S_cm') == 176.715 and m.get('sigma_vgcf_bulk_S_cm') == 10000.0
        and m.get('sigma_vgcf_rule') == rule, (rc, {k: m.get(k) for k in ('sigma_vgcf_S_cm', 'sigma_vgcf_bulk_S_cm', 'sigma_vgcf_rule')},
                                                log.strip()[-300:]))
    chk('Z1e2 기록은 규약 해시 밖 — 같은 σ 를 bulk 없이 준 런과 physics_protocol_id 같음 (p2) · 끈 런은 bulk · 식 이름 키가 없다',
        rc0 == 0 and str(m.get('physics_protocol_id', '')).startswith('p2-') and m.get('physics_protocol_id') == m0.get('physics_protocol_id')
        and 'sigma_vgcf_bulk_S_cm' not in m0 and 'sigma_vgcf_rule' not in m0, (m.get('physics_protocol_id'), m0.get('physics_protocol_id')))
    refuse = {
        '다시 계산 ≠ --sigma-vgcf (100 ↔ 176.715)': (L + ['--sigma-vgcf', '100', '--sigma-vgcf-bulk', '1e4'], (), 'MISMATCH'),
        '반올림 한 자리 다름 (176.714)': (L + ['--sigma-vgcf', '176.714', '--sigma-vgcf-bulk', '1e4'], (), 'MISMATCH'),
        'bulk nan': (L + ['--sigma-vgcf', '176.715', '--sigma-vgcf-bulk', 'nan'], (), 'VALUE'),
        'bulk 0': (L + ['--sigma-vgcf', '0', '--sigma-vgcf-bulk', '0'], (), 'VALUE'),
        'bulk -1e4 (= 꼴 · argparse 가 음수를 옵션으로 읽지 않게)': (L + ['--sigma-vgcf', '176.715', '--sigma-vgcf-bulk=-1e4'], (), 'VALUE'),
        '--fibre-dia 없음': (L + ['--sigma-vgcf', '176.715', '--sigma-vgcf-bulk', '1e4'], ('--fibre-dia',), 'NO_DIA'),
        '--no-step3': (L + ['--no-step3', '--sigma-vgcf', '176.715', '--sigma-vgcf-bulk', '1e4'], (), 'NO_STEP3'),
    }
    for i, (nm, (extra, drop, code)) in enumerate(refuse.items()):
        rr, lg, mm = _pay(f'fb_refuse_{i}', extra, drop=drop)
        chk(f'Z1e [{nm}] → payload 거부 `SIGMA_VGCF_BULK_REFUSED|{code}|` · 산출물 없음', rr != 0
            and f'SIGMA_VGCF_BULK_REFUSED|{code}|' in lg and not mm, (rr, lg.strip()[-260:]))


_RUN = {}


def _runner(label, env, **kw):
    if label not in _RUN:
        ws = TR.make_ws(label)
        _RUN[label] = TR.run_runner(ws, env, **kw)
    return _RUN[label]


@case('Z1f 러너 실물 — SIGMA_FIBRE_BULK=1e4 → payload 인자 · 영수증 · 팔 이름 · 매니페스트 · check_arm (vox 1.0 침대)')
def t_runner_e2e():
    import step3_sigma as S3
    rule = getattr(S3, 'VGCF_SIGMA_RULE', 'x')
    r0 = _runner('z1_off', {})
    r = _runner('z1_fb', {'SIGMA_FIBRE_BULK': '1e4'})
    chk('Z1f1 끔 · 켬 둘 다 rc 0 · 켬 팔 이름 = p2_<침대>_fb10000_a0 (옛 p2_<침대>_a0 와 다르다)',
        r0.rc == 0 and r.rc == 0 and r.arms == ['p2_DBE_fb10000_a0.json', 'p2_SBE_fb10000_a0.json']
        and r0.arms == ['p2_DBE_a0.json', 'p2_SBE_a0.json'], (r0.rc, r.rc, r.arms, r.log[-700:]))
    s0 = {a: TR.opt(t, '--sigma-vgcf') for a, t in r0.argv.items()}
    s1 = {a: TR.opt(t, '--sigma-vgcf') for a, t in r.argv.items()}
    b1 = {a: TR.opt(t, '--sigma-vgcf-bulk') for a, t in r.argv.items()}
    chk('Z1f2 payload 인자 — 끔 σ 1.76715 (= 손계산 100 · vox 1.0 · 옛 값) · 켬 σ 176.715 (= 손계산 1e4) · 켬에만 --sigma-vgcf-bulk 10000.0',
        set(s0.values()) == {_hand(100.0, 1.0)} and set(s1.values()) == {_hand(1e4, 1.0)} and set(b1.values()) == {'10000.0'}
        and not any(TR.opt(t, '--sigma-vgcf-bulk') for t in r0.argv.values()), (s0, s1, b1))
    dec = {a: TR.expect_decl(t).get('sigma_vgcf_S_cm') for a, t in r.argv.items()}
    chk('Z1f3 --expect-physics 의 sigma_vgcf_S_cm = 176.715 (선언한 σ = 넘긴 σ = 매니페스트 σ)', set(dec.values()) == {'176.715'}, dec)
    rc = r.receipt or {}
    chk('Z1f4 영수증 = bulk 10000.0 + 식 이름 · sigma_vgcf_S_cm (override 칸) 은 없다',
        rc.get('sigma_vgcf_bulk_S_cm') == 1e4 and rc.get('sigma_vgcf_rule') == rule and 'sigma_vgcf_S_cm' not in rc, rc)
    ok_m = []
    for a in r.arms:
        _s3, m = TR.manifest_of(os.path.join(r.outdir, a))
        ok_m.append(m.get('sigma_vgcf_S_cm') == 176.715 and m.get('sigma_vgcf_bulk_S_cm') == 1e4 and m.get('sigma_vgcf_rule') == rule
                    and RC.receipt_match(rc, m) == (True, None) and str(m.get('physics_protocol_id', '')).startswith('p2-'))
    chk('Z1f5 팔 매니페스트 = σ 176.715 · bulk · 식 이름 · receipt_match 통과 · p2 세대 (bulk 만 = 옛 세대 · σ 가 다를 뿐)',
        len(ok_m) == 2 and all(ok_m), ok_m)
    chk('Z1f6 OUTDIR 이름에 _fb10000 · 끔 런과 다른 디렉터리', '_fb10000' in os.path.basename(r.outdir or '')
        and os.path.basename(r.outdir or '') != os.path.basename(r0.outdir or ''), (r.outdir, r0.outdir))
    ws = TR.make_ws('z1_refuse')
    for nm, env, code in (('bulk + SIGMA_VGCF_OVERRIDE', {'SIGMA_FIBRE_BULK': '1e4', 'SIGMA_VGCF_OVERRIDE': '176.715'},
                           'RUNNER_CA_EXT|SIGMA_VGCF_BOTH|'),
                          ('bulk nan', {'SIGMA_FIBRE_BULK': 'nan'}, 'RUNNER_CA_EXT|VALUE|'),
                          ('bulk 0', {'SIGMA_FIBRE_BULK': '0'}, 'RUNNER_CA_EXT|VALUE|')):
        rr = TR.run_runner(ws, env)
        chk(f'Z1f [{nm}] → rc 2 · `{code}` · 새 디렉터리 없음 · payload 미호출', rr.rc == 2 and code in rr.log and not rr.new_dirs
            and not rr.argv, (rr.rc, rr.new_dirs, rr.log.strip()[-300:]))
    #  SKIP 캐시 함정 — 옛 (끔) 팔이 있는 OUTDIR 을 명시해도 옛 팔을 재사용 · 삭제하지 않는다
    if r0.outdir and len(r0.arms) == 2:
        ws2 = TR.make_ws('z1_skip')
        old = os.path.join(ws2, 'old_outdir_arm1')
        os.makedirs(old)
        sha = {}
        for a in r0.arms:
            shutil.copy2(os.path.join(r0.outdir, a), os.path.join(old, a))
            sha[a] = hashlib.sha256(open(os.path.join(old, a), 'rb').read()).hexdigest()
        rs = TR.run_runner(ws2, {'SIGMA_FIBRE_BULK': '1e4', 'OUTDIR': old}, payload_exit=3)
        after = {a: hashlib.sha256(open(os.path.join(old, a), 'rb').read()).hexdigest() if os.path.exists(os.path.join(old, a))
                 else None for a in sha}
        chk('Z1f7 SKIP 함정 — 옛 팔 재사용 안 함 · 두 파일 그대로 · 새 팔은 새 이름 (_fb10000) 으로만',
            'SKIP (완전)' not in rs.log and after == sha and sorted(rs.argv) and all('_fb10000_' in o for o in rs.argv),
            (sorted(rs.argv), after == sha, rs.log[-300:]))


# ═════════════════════════ Z2 — STEP3_RTOL 필수 ═════════════════════════
@case('Z2 다음 세대 노브 (CJUNC=1 · face_alpha · SDCP_MOD_C) = STEP3_RTOL 필수 — 팔 시작 전 거부 · 옛 세대 그대로')
def t_rtol_required():
    need = {
        'CJUNC=1 (값 여섯 다)': (dict(TR.CJ_ENV), {'lean': '2'}),
        'CJUNC=1 + SDCP_MOD_C=1': (dict(TR.CJ_ENV, SDCP_MOD_C='1'), {'lean': '2'}),
        'PTFE_STAMP=face_alpha (LEAN 2)': ({}, {'ptfe_stamp': 'face_alpha', 'lean': '2'}),
        'PTFE_STAMP=face_alpha (LEAN 3)': ({}, {'ptfe_stamp': 'face_alpha', 'lean': '3'}),
        'SDCP_MOD_C 만 (S2 없이)': ({'SDCP_MOD_C': '0'}, {'lean': '2'}),
    }
    for nm, (env, kw) in need.items():
        ps = probs(env, **kw)
        ps_rt = probs(dict(env, STEP3_RTOL='1e-12'), **kw)
        chk(f'Z2 [{nm}] rtol 없음 → RTOL_REQUIRED · rtol 1e-12 → 그 사유 없음', has_code(ps, 'RTOL_REQUIRED')
            and not has_code(ps_rt, 'RTOL_REQUIRED'), (ps, ps_rt))
    free = {
        '끔 (기본)': ({}, {}), 'centerline (현 세대 생산)': ({}, {'ptfe_stamp': 'centerline', 'lean': '2'}),
        'SIGMA_FIBRE_BULK 만 (현 세대 꼴)': ({'SIGMA_FIBRE_BULK': '1e4'}, {'lean': '2'}),
        'CJUNC=0 (끔)': ({'CJUNC': '0'}, {}), 'STEP3_RTOL 만': ({'STEP3_RTOL': '1e-12'}, {}),
    }
    for nm, (env, kw) in free.items():
        ps = probs(env, **kw)
        chk(f'Z2 [{nm}] → RTOL_REQUIRED 없음 (옛 세대 · 끈 노브는 그대로)', not has_code(ps, 'RTOL_REQUIRED'), ps)
    ps = probs(dict(TR.CJ_ENV), lean='2')
    chk('Z2b 사유가 봉인 상한과 "기본값 없음" 을 말한다 (사람이 값을 고른다)', any('RTOL_REQUIRED' in p and '1e-12' in p and '기본값' in p
                                                                       for p in ps), ps)
    ws = TR.make_ws('z2')
    for nm, env in (('접합 (LEAN 2 · 값 여섯) · rtol 없음', dict(TR.CJ_ENV)),
                    ('face_alpha (LEAN 2) · rtol 없음', {'PTFE_STAMP': 'face_alpha'})):
        rr = TR.run_runner(ws, env)
        chk(f'Z2c 러너 실물 [{nm}] → rc 2 · RUNNER_CA_EXT|RTOL_REQUIRED| · 새 디렉터리 없음 · payload 미호출 (GPU 전)',
            rr.rc == 2 and 'RUNNER_CA_EXT|RTOL_REQUIRED|' in rr.log and not rr.new_dirs and not rr.argv,
            (rr.rc, rr.new_dirs, rr.log.strip()[-300:]))


# ═════════════════════════ Z3 — 사슬 env 오염 = 거부 ═════════════════════════
@case('Z3 sdcp_anchor_v2_chain — 부모 셸의 다음 세대 노브 (CJUNC* · SDCP_MOD_C · STEP3_RTOL · SIGMA_FIBRE_BULK) = 거부 (지우지 않는다)')
def t_chain():
    import sdcp_anchor_v2_chain as CH
    td = os.path.join(TD, 'z3')
    os.makedirs(os.path.join(td, 'root', 'kit_SBE'))
    os.makedirs(os.path.join(td, 'root', 'kit_DBE'))
    with open(os.path.join(td, 'fake.py'), 'w', encoding='utf-8') as f:
        f.write(CH.FAKE)
    runner = os.path.join(td, 'runner.sh')
    with open(runner, 'w', encoding='utf-8') as f:
        f.write(f'#!/bin/bash\nexec {sys.executable} -I {os.path.join(td, "fake.py")}\n')
    base = {k: v for k, v in os.environ.items() if not k.startswith(('CJUNC', 'SDCP_', 'STEP3_', 'SIGMA_', 'PTFE_'))}
    base['FAKE_MODE'] = 'normal'

    def go(extra, tag, dry=False):
        ch = CH.Chain(runner, os.path.join(td, 'root'), os.path.join(td, f'out_{tag}'), dry=dry, python_env=dict(base, **extra))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rc_ = ch.go()
            stop = None
        except CH.Stop as e:
            rc_, stop = 3, str(e)
        CH.KITS['DBE'] = 'kit_DBE'
        return rc_, stop, ch

    rc_, stop, ch = go({}, 'clean')
    chk('Z3a 깨끗한 env → 사슬이 돈다 (rc 0 · 런 다섯 · 가짜 러너)', rc_ == 0 and len(ch.summary['runs']) == 5, (rc_, stop))
    bad = {}
    for nm in ('CJUNC', 'CJUNC_RJ', 'CJUNC_LEN_LAW', 'CJUNC_UNREG_LAW', 'CJUNC_S_MIN_UM', 'CJUNC_TOL_FF_UM', 'CJUNC_PTFE_JLAW',
               'CJUNC_BOGUS', 'SDCP_MOD_C', 'STEP3_RTOL', 'SIGMA_FIBRE_BULK'):
        for val in ('1', ''):
            rc_, stop, ch = go({nm: val}, f'{nm}_{len(val)}')
            if not (rc_ == 3 and stop and 'NEXTGEN_ENV' in stop and nm in stop and not ch.summary['runs']
                    and not os.path.exists(os.path.join(td, f'out_{nm}_{len(val)}'))):
                bad[(nm, val)] = (rc_, stop)
    chk('Z3b 부모 env 의 열하나 (값 1 · 빈 값 둘 다) → 러너 부르기 전 멈춤 · 사유 NEXTGEN_ENV + 그 이름 · 런 0 · 출력 폴더 없음',
        not bad, list(bad.items())[:3])
    rc_, stop, ch = go({'CJUNC': '1', 'STEP3_RTOL': '1e-12'}, 'dry', dry=True)
    chk('Z3c dry-run 도 같은 이유로 멈춘다 (찍은 명령이 실제 런과 갈리지 않게)', rc_ == 3 and stop and 'NEXTGEN_ENV' in stop
        and 'CJUNC' in stop and 'STEP3_RTOL' in stop, (rc_, stop))
    rc_, stop, ch = go({'PTFE_STAMP': 'face_alpha', 'SIGMA_ION_SE': '0.0015'}, 'override')
    chk('Z3d 사슬이 덮어쓰는 축 (PTFE_STAMP) · 지우는 축 (SIGMA_ION_*) 은 그대로 (거부 대상 아님 · 옛 동작)', rc_ == 0, (rc_, stop))
    names = getattr(CH, 'NEXTGEN_ENV_NAMES', None)
    chk('Z3e 거부 이름 = run_contract.RUNNER_CA_EXT_ENV 의 이름 전부 (정본 하나 · 사본 없음) + CJUNC 접두',
        names is not None and set(n for n, _s, _k in RC.RUNNER_CA_EXT_ENV) <= set(names), names)


# ═════════════════════════ Z4 — compare_dirs 의 ca_ext ═════════════════════════
_COH = {}


def coh(label, extra):
    """두 침대 (SBE · DBE · vox 1.0 · origin 0) × payload 실물 → 디렉터리 (이름 = p2_<침대>_a0.json · 같은 침대 파일 = 같은 input_digest)."""
    if label in _COH:
        return _COH[label]
    beds = _COH.setdefault('_beds', {})
    if not beds:
        for bed, sdcp in (('SBE', False), ('DBE', True)):
            d = os.path.join(TD, f'coh_bed_{bed}')
            os.makedirs(d)
            B6.make_fixture(d, sdcp=sdcp)
            beds[bed] = d
    dest = os.path.join(TD, f'coh_{label}')
    os.makedirs(dest)
    bad = []
    for bed in ('SBE', 'DBE'):
        name = f'p2_{bed}_a0.json'
        rc, log, _p = B6.run_payload(beds[bed], list(extra) + ['--step3-origin-shift', '0', '0', '0'], out=name)
        if rc != 0 or not os.path.exists(os.path.join(beds[bed], name)):
            bad.append((bed, rc, log.strip()[-240:]))
            continue
        shutil.move(os.path.join(beds[bed], name), os.path.join(dest, name))
    if bad:
        print(f'    ⚠ 코호트 {label} 를 못 만들었다: {bad[:1]}')
    _COH[label] = None if bad else dest
    return _COH[label]


def _cj(**repl):
    return B6.OFF + B6.LEAN2 + B6.cj_with(**repl) + RT


def cmp_(a, b, exp, **kw):
    return quiet(V.compare_dirs, a, b, set(exp), **kw)


@case('Z4 compare_dirs — ca_ext 하위 블록 · 칸 = 등록 축 · 증거 = 결과 · 등록 밖 차이 = HOLD · CLI --expect-differ')
def t_compare():
    A = coh('A_rj1e6', _cj())
    B = coh('B_rj1e4', _cj(rj='1e4'))
    C = coh('C_rj1e4_tol04', _cj(rj='1e4', tol_ff_um='0.4'))
    D = coh('D_p2_rt', B6.OFF + B6.LEAN2 + RT)
    E = coh('E_rj1e6_c1', _cj() + ['--step3-sdcp-mod-c', '1'])
    chk('Z4a0 코호트 다섯 (각 두 팔) 을 만들었다', all((A, B, C, D, E)), [x is not None for x in (A, B, C, D, E)])
    if not all((A, B, C, D, E)):
        return
    ma = V.collect(A)[1]['SBE'][0]['_manifest']
    mb = V.collect(B)[1]['SBE'][0]['_manifest']
    chk('Z4a1 판별력 전제 — A ↔ B 증거 (evidence.solve) 가 실제로 다르다 · 분류 안 된 키 없음 (옛 판: ca_ext · ca_ext_requested)',
        ma['ca_ext']['cjunc']['evidence'] != mb['ca_ext']['cjunc']['evidence'] and V.manifest_unswept_keys(ma, mb) == [],
        V.manifest_unswept_keys(ma, mb))
    c = cmp_(A, B, {'ca_ext.cjunc.R_j_ohm'})
    chk('Z4b R_j 사다리 두 점 (1e6 ↔ 1e4) · --expect-differ ca_ext.cjunc.R_j_ohm → measured (증거 차이 = 결과)',
        c.get('decision') == 'measured', (c.get('decision'), c.get('reason', '')[:300]))
    c = cmp_(A, B, {'ca_ext.cjunc'})
    chk('Z4c 같은 쌍 · 하위 블록 축 ca_ext.cjunc → measured', c.get('decision') == 'measured', (c.get('decision'), c.get('reason', '')[:300]))
    c = cmp_(A, C, {'ca_ext.cjunc.R_j_ohm'})
    chk('Z4d R_j 만 등록했는데 tol_ff 도 다르다 → HOLD (등록 밖 칸 이름 tol_ff_um)', c.get('decision') == 'HOLD'
        and 'tol_ff_um' in c.get('reason', ''), (c.get('decision'), c.get('reason', '')[:300]))
    c = cmp_(A, C, {'ca_ext.cjunc.R_j_ohm', 'ca_ext.cjunc.tol_ff_um'})
    chk('Z4e R_j + tol_ff 등록 → measured (tol_P · tol_sj = 같은 CLI 플래그가 정하는 칸 · CLI 회계 정본)', c.get('decision') == 'measured',
        (c.get('decision'), c.get('reason', '')[:300]))
    c = cmp_(A, A, {'ca_ext.cjunc'})
    chk('Z4f 같은 디렉터리끼리 · ca_ext.cjunc 등록 → HOLD (노브가 안 걸렸다 · 감소율 0 = 실험 없음)', c.get('decision') == 'HOLD'
        and 'ca_ext.cjunc' in c.get('reason', ''), (c.get('decision'), c.get('reason', '')[:300]))
    c = cmp_(D, A, {'ca_ext.cjunc'})
    chk('Z4g 현 세대 (p2 · rtol) ↔ 다음 세대 (접합) · ca_ext.cjunc 등록 → measured (블록 켬 = 등록 축 · 요청 칸 · id = 파생)',
        c.get('decision') == 'measured', (c.get('decision'), c.get('reason', '')[:300]))
    c = cmp_(D, A, {'ca_ext.cjunc.R_j_ohm'})
    chk('Z4h p2 ↔ 접합인데 칸 (R_j) 만 등록 → HOLD (블록이 켜지고 꺼진 것은 하위 블록 축으로만 등록)', c.get('decision') == 'HOLD',
        (c.get('decision'), c.get('reason', '')[:300]))
    c = cmp_(A, E, {'ca_ext.sdcp_mod'})
    chk('Z4i 수정자 c = 1 켬 · ca_ext.sdcp_mod 등록 → measured', c.get('decision') == 'measured', (c.get('decision'), c.get('reason', '')[:300]))
    c = cmp_(A, E, {'ca_ext.cjunc'})
    chk('Z4j 수정자 켬인데 ca_ext.cjunc 만 등록 → HOLD (sdcp_mod = 등록 밖)', c.get('decision') == 'HOLD' and 'sdcp_mod' in c.get('reason', ''),
        (c.get('decision'), c.get('reason', '')[:300]))
    c = cmp_(A, B, {'sdcp_yield_to_vgcf'})
    chk('Z4k 다른 축을 등록했는데 접합 R_j 가 다르다 → HOLD (옛 계약 그대로 · 등록 밖 = HOLD)', c.get('decision') == 'HOLD',
        (c.get('decision'), c.get('reason', '')[:200]))
    cli = [sys.executable, os.path.join(SCRIPTS, 'sdcp_gain_verdict.py'), '--dir', A, '--compare-dir', B, '--expect-differ']
    p = subprocess.run(cli + ['ca_ext.cjunc.R_j_ohm'], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=300)
    chk('Z4l CLI --expect-differ ca_ext.cjunc.R_j_ohm → rc 0 · measured', p.returncode == 0 and 'measured' in p.stdout,
        (p.returncode, (p.stdout + p.stderr)[-300:]))
    for nm in ('ca_ext.bogus', 'ca_ext.cjunc.bogus_key', 'ca_ext'):
        p = subprocess.run(cli + [nm], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=300)
        chk(f'Z4m CLI 모르는 축 `{nm}` → 거부 (rc ≠ 0 · 대조 안 함 · 사유에 그 이름)', p.returncode != 0 and '대조쌍 검증' not in p.stdout
            and nm in (p.stdout + p.stderr), (p.returncode, (p.stdout + p.stderr)[-200:]))
    axes = V.ca_ext_axes() if hasattr(V, 'ca_ext_axes') else ()
    chk('Z4n 축 이름 = run_contract.CA_EXT_SUBBLOCKS (하위 블록) + ca_ext_protocol_fields (칸) — 같은 원천',
        set(axes) == {f'ca_ext.{k}' for k in RC.CA_EXT_SUBBLOCKS} | set(RC.ca_ext_protocol_fields()), sorted(axes)[:6])
    #  순수 함수 대조 (ca_ext_contrast) — 실물 매니페스트 (E = 접합 + 수정자) 를 칸 하나씩 바꿔 본다
    import copy
    me = V.collect(E)[1]['DBE'][0]['_manifest']
    fn = getattr(V, 'ca_ext_contrast', None)

    def _mut(f):
        m = copy.deepcopy(me)
        f(m['ca_ext'])
        return m

    def _tol(b):
        for k in ('tol_ff_um', 'tol_P_um', 'tol_sj_um'):
            b['cjunc']['protocol'][k] = 0.4
        b['sdcp_mod']['protocol']['tol_sj_um'] = 0.4
    mt = _mut(_tol)
    res = {nm: (fn(me, m, exp) if fn else None) for nm, (m, exp) in {
        'tol·하위 블록': (mt, {'ca_ext.cjunc'}), 'tol·칸': (mt, {'ca_ext.cjunc.tol_ff_um'}), 'tol·R_j 만': (mt, {'ca_ext.cjunc.R_j_ohm'}),
        '증거만': (_mut(lambda b: b['cjunc']['evidence']['counts'].update(n_edge=99)), set()),
        'schema': (_mut(lambda b: b.update(schema='ca-ext-v9')), {'ca_ext.cjunc'}),
        '사본 칸 · 최상위 등록': (_mut(lambda b: b['cjunc']['protocol'].update(ptfe_stamp='centerline')), {'ptfe_stamp'}),
        '사본 칸 · 등록 없음': (_mut(lambda b: b['cjunc']['protocol'].update(ptfe_stamp='centerline')), {'sdcp_yield_to_vgcf'})}.items()}
    chk('Z4o ca_ext_contrast — tol_ff 를 바꾸면 (형제 tol_P · tol_sj · sdcp_mod.tol_sj 가 따라 다르다) 하위 블록 축 · tol_ff 칸 축 = 설명됨 · '
        'R_j 칸만 = 등록 밖 넷',
        fn is not None and res['tol·하위 블록'][0] == [] and res['tol·칸'][0] == [] and set(res['tol·R_j 만'][0]) == {
            'ca_ext.cjunc.tol_ff_um', 'ca_ext.cjunc.tol_P_um', 'ca_ext.cjunc.tol_sj_um', 'ca_ext.sdcp_mod.tol_sj_um'},
        {k: res[k] for k in ('tol·하위 블록', 'tol·칸', 'tol·R_j 만')} if fn else None)
    chk('Z4p 증거만 다름 = 차이 아님 (결과) · schema 다름 = 등록해도 위반 · 사본 칸 (cjunc.protocol.ptfe_stamp) = 최상위 ptfe_stamp 를 '
        '등록하면 설명 · 아니면 위반', fn is not None and res['증거만'] == ([], set()) and 'ca_ext.schema' in res['schema'][0]
        and res['사본 칸 · 최상위 등록'][0] == [] and res['사본 칸 · 등록 없음'][0] == ['ca_ext.cjunc.ptfe_stamp'],
        {k: res[k] for k in ('증거만', 'schema', '사본 칸 · 최상위 등록', '사본 칸 · 등록 없음')} if fn else None)
    both = {'ca_ext.cjunc', 'ca_ext.cjunc.R_j_ohm'}
    r2 = fn(me, _mut(lambda b: b['cjunc']['protocol'].update(R_j_ohm=1e4)), both) if fn else None
    c = cmp_(A, B, both)
    chk('Z4q 하위 블록 축과 그 칸을 **같이** 등록 · R_j 만 다름 → 둘 다 "실제로 다름" (거짓 "노브 안 걸림" 없음) · compare_dirs measured',
        r2 is not None and r2[0] == [] and both <= r2[1] and c.get('decision') == 'measured',
        (r2, c.get('decision'), c.get('reason', '')[:200]))


# ═════════════════════════ Z5 — --expect-generation ═════════════════════════
@case('Z5 판정기 --expect-generation — 코호트 세대 (p2 · p3ca) 선언 · 다르면 거부 (설계 §7 네 번째 방어)')
def t_expect_gen():
    A = coh('A_rj1e6', _cj())
    D = coh('D_p2_rt', B6.OFF + B6.LEAN2 + RT)
    if not (A and D):
        chk('Z5 선행 (코호트)', False)
        return
    aA, aD = quiet(V.collect, A)[1], quiet(V.collect, D)[1]

    def vc(arms, g):
        try:
            return quiet(V.validate_contract, arms, expect_generation=g)
        except TypeError as e:
            return {'hold_code': f'TypeError: {e}'}, {}
    cases = [('p3ca 코호트 · 기대 p3ca', aA, 'p3ca', None), ('p3ca 코호트 · 기대 p2', aA, 'p2', 'GENERATION_EXPECT'),
             ('p2 코호트 · 기대 p2', aD, 'p2', None), ('p2 코호트 · 기대 p3ca', aD, 'p3ca', 'GENERATION_EXPECT')]
    for nm, arms, g, want in cases:
        hold, _i = vc(arms, g)
        chk(f'Z5a [{nm}] → {"통과" if want is None else "HOLD " + want}', (hold is None) if want is None
            else ((hold or {}).get('hold_code') == want and g in (hold or {}).get('reason', '')),
            ((hold or {}).get('hold_code'), (hold or {}).get('reason', '')[:240]))
    unk = {k: [dict(r) for r in v] for k, v in aD.items()}
    m2 = dict(unk['SBE'][0]['_manifest'])
    m2.pop('plate_rule', None)
    unk['SBE'][0]['_manifest'] = m2
    hold, _i = vc(unk, 'p2')
    chk('Z5b 규약 id = unknown:* 팔 + 기대 p2 → HOLD GENERATION_EXPECT (세대를 모르는 팔은 기대 세대가 아니다)',
        (hold or {}).get('hold_code') == 'GENERATION_EXPECT' and 'unknown' in (hold or {}).get('reason', ''),
        ((hold or {}).get('hold_code'), (hold or {}).get('reason', '')[:240]))
    hold, _i = vc(aD, None)
    chk('Z5c 기대 없음 (기본) = 옛 동작 — p2 코호트에 새 사유 없음', (hold or {}).get('hold_code') != 'GENERATION_EXPECT',
        ((hold or {}).get('hold_code'),))
    B = coh('B_rj1e4', _cj(rj='1e4'))
    if B:
        try:
            c1 = quiet(V.compare_dirs, A, B, {'ca_ext.cjunc.R_j_ohm'}, expect_generation='p3ca')
            c2 = quiet(V.compare_dirs, A, B, {'ca_ext.cjunc.R_j_ohm'}, expect_generation='p2')
        except TypeError as e:
            c1 = c2 = {'decision': f'TypeError: {e}'}
        chk('Z5d compare_dirs 도 두 디렉터리에 같은 기대 — p3ca 쌍 · 기대 p3ca → measured · 기대 p2 → HOLD GENERATION_EXPECT',
            c1.get('decision') == 'measured' and c2.get('decision') == 'HOLD' and c2.get('hold_code') == 'GENERATION_EXPECT',
            (c1.get('decision'), c2.get('decision'), c2.get('hold_code')))
    vf = os.path.join(SCRIPTS, 'sdcp_gain_verdict.py')

    def run(*args):
        p = subprocess.run([sys.executable, vf, *args], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=300)
        return p.returncode, (p.stdout or '') + (p.stderr or '')
    rc1, lg1 = run('--dir', D, '--seal-only', '--expect-generation', 'p3ca')
    rc2, lg2 = run('--dir', A, '--seal-only', '--expect-generation', 'p3ca')
    chk('Z5e CLI --seal-only --expect-generation p3ca — p2 디렉터리 = 봉인 깨짐 (사유 GENERATION_EXPECT) · p3ca 디렉터리 = 그 사유 없음',
        rc1 == 1 and 'GENERATION_EXPECT' in lg1 and 'GENERATION_EXPECT' not in lg2, (rc1, lg1[-240:], lg2[-200:]))
    rc3, lg3 = run('--dir', D, '--seal-only', '--expect-generation', 'p9')
    rc4, lg4 = run('--dir', D, '--collect-only', '--expect-generation', 'p2')
    rc5, lg5 = run('--scan', TD, '--expect-generation', 'p2')
    chk('Z5f CLI 모르는 세대 (p9) = 거부 · --collect-only · --scan 과 함께 = 거부 (판정이 없는 모드에서 조용한 no-op 금지)',
        rc3 not in (0, 1) and rc4 not in (0, 1) and rc5 not in (0, 1) and 'expect-generation' in lg4 and 'expect-generation' in lg5,
        (rc3, rc4, rc5, lg4[-200:], lg5[-200:]))


# ═════════════════════════ ZB — 끔 경로 (고치기 전 run_contract 와 함수 대조) ═════════════════════════
@case('ZB 끔 경로 — 고치기 전 run_contract (--old-scripts) 와 digest · 발사 전 검사 · 이름 태그 · receipt_match 같음')
def t_old():
    if not ARGS.old_scripts:
        print('    (--old-scripts 없음 — 건너뜀 · 커밋 증거는 그 인자로 돌린 기록)')
        return
    spec = importlib.util.spec_from_file_location('run_contract_old', os.path.join(ARGS.old_scripts, 'run_contract.py'))
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    recs = [json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(ROOT, 'docs/data/**/run_receipt.json'),
                                                                               recursive=True))]
    diff = [i for i, r in enumerate(recs) if RC.receipt_digest(r) != old.receipt_digest(r)]
    chk(f'ZB1 커밋된 영수증 {len(recs)} 개 — receipt_digest 가 고치기 전과 같다', len(recs) >= 40 and not diff, diff[:4])
    envs = [({}, {}), ({}, {'ptfe_stamp': 'centerline', 'lean': '2'}), ({'STEP3_RTOL': '1e-12'}, {}),
            (CJ_RT_ENV, {'lean': '2'}), (dict(CJ_RT_ENV, SDCP_MOD_C='1'), {'lean': '2'}), ({'STEP3_RTOL': '1e-12'}, {'ptfe_stamp': 'face_alpha',
                                                                                                                 'lean': '2'})]
    dif2 = []
    for env, kw in envs:
        n, o = RC.runner_ca_ext(env, **kw), old.runner_ca_ext(env, **kw)
        vn = RC.runner_ca_ext_view(dict(n['receipt'], **({'ptfe_stamp': kw['ptfe_stamp']} if 'ptfe_stamp' in kw else {})))
        vo = old.runner_ca_ext_view(dict(o['receipt'], **({'ptfe_stamp': kw['ptfe_stamp']} if 'ptfe_stamp' in kw else {})))
        if n != o or {k: vn[k] for k in vo} != vo or vn.get('vgcf_bulk') != '':
            dif2.append((env, kw, n, o))
    chk(f'ZB2 bulk 없는 env {len(envs)} 가지 (끔 · centerline · rtol · 접합 + rtol · + c · face_alpha + rtol) — 발사 전 검사 · 영수증 · '
        f'이름 태그 · 인자가 고치기 전과 같다 (새 칸 vgcf_bulk = 빈 문자열)', not dif2, dif2[:2])
    mans = []
    for name in ('w4_ptfe_centerline_20260827', 'w4b_ptfe_off_20260827'):
        rec = json.load(open(os.path.join(ROOT, 'docs/data', name, 'run_receipt.json'), encoding='utf-8'))
        for f in sorted(glob.glob(os.path.join(ROOT, 'docs/data', name, 'p2_*.json'))):
            m = json.load(open(f, encoding='utf-8'))['step3']['manifest']
            mans.append((RC.receipt_match(rec, m) == old.receipt_match(rec, m), RC.physics_protocol_id(m) == old.physics_protocol_id(m)))
    chk(f'ZB3 봉인 코호트 {len(mans)} 팔 — receipt_match · physics_protocol_id 가 고치기 전과 같다', len(mans) == 32
        and all(a and b for a, b in mans), mans[:3])


def main():
    global ARGS, TD
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--old-scripts', default='', help='고치기 전 scripts/ 사본 (ZB 끔 경로 대조)')
    ap.add_argument('--only', default='', help='쉼표로 나눈 이름 접두 (예: Z1,Z4)')
    ap.add_argument('--keep', action='store_true', help='임시 디렉터리를 남긴다 (진단)')
    ARGS = ap.parse_args()
    TD = tempfile.mkdtemp(prefix='ca_ext_z1_')
    TR.TD = TD
    TR.SHIMDIR = os.path.join(TD, '_bin')
    os.makedirs(TR.SHIMDIR)
    os.makedirs(os.path.join(TD, '_probe'))
    with open(os.path.join(TR.SHIMDIR, 'python3'), 'w', encoding='utf-8') as f:
        f.write(TR.SHIM.replace('__REAL__', os.path.realpath(sys.executable)))
    os.chmod(os.path.join(TR.SHIMDIR, 'python3'), 0o755)
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    t0 = time.time()
    try:
        for tag, fn in CASES:
            if only and not any(tag.startswith(o) for o in only):
                continue
            print(f'\n── {tag}')
            t1 = time.time()
            try:
                fn()
            except Exception as e:                              # noqa: BLE001 — 옛 코드 (API 없음) 도 시험 단위로 기록
                chk(f'{tag.split()[0]}: 실행', False, f'{type(e).__name__}: {e}')
            print(f'    ({time.time() - t1:.1f} s)')
    finally:
        if ARGS.keep:
            print(f'\n  (임시 디렉터리 남김: {TD})')
        else:
            shutil.rmtree(TD, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL  ({time.time() - t0:.1f} s)')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()

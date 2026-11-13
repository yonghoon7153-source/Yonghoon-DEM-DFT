#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② 개발 탐침 ⑥ (SBE 수치 탐침 · σ 봉인) 준비물 시험 · 시험 먼저 (2026-11-10 · 내부 반박 리뷰 P6R-01–12 고침 · 두 시도).

대상 (같은 폴더):
  probe6_read.py   σ 비열람 판독기 (닫힌 허용 칸만 낸다)
  run_probe6.sh    kgy 감시 셸 (러너 = 자기 세션 · 프로세스 그룹 · 출력은 로그 파일로만 · 묶음에 σ 가 든 파일을 넣지 않는다)
  ../KGY_BLOCK.md  1저자가 붙여 넣는 블록 (ATTEMPT 1 · 2) · ../LEDGER_LINE.md  원장 줄 초안 (두 줄)

정본 = 개발 탐침 사전 원장 `docs/reviews/rint2_dev_probe_ledger_20261026.md` §2 (규칙 일곱 칸) · §3 (시도 줄) · 등록 R
`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §10-1 (2) · §11 ⑥.

  python3 docs/reviews/rint2_probe6_prep_20261110/tools/test_probe6_read.py            # 전부 (W 빼고)
  python3 .../test_probe6_read.py --only T,M        # 이름 접두로 고르기 (W = 감시 셸 변이 · 고를 때만)
  python3 .../test_probe6_read.py --no-real         # 실제 러너 묶음 (R) 을 뺀다 (뺀 것은 PASS 로 세지 않는다)
  python3 .../test_probe6_read.py --keep            # 임시 폴더를 남긴다
  python3 .../test_probe6_read.py --ledger FILE     # 원장 읽기 시험 (S11) 을 다른 파일로 (원장을 고치기 전 제안 글 확인용)

묶음:
  S  정적: ASCII · Python 3.8 문법 · bash -n · 축 (감시 셸 ↔ 등록 R §10-1 (2) ↔ 원장 줄 초안 ↔ 원장 파일 ↔ 블록 ↔ S0 계획 ↔ 코드 상수) ·
     걷어내기 목록 ↔ 러너가 읽는 env 이름 · 허용 표에 σ 류 이름 없음 · 주소 · 모델 이름 없음 · 게이트 단계 (check_all · kgy 판)
  T  판독기: 합성 출력 폴더 (실제 러너 · payload 가 쓰는 꼴 · σ 류 자리마다 표식 0.00713331… ): 누출 검사 = 구조 (닫힌 허용 목록 ·
     칸마다 꼴 · 팔 값 출처 · 화면 줄 = 보고 값 · 걸러 낸 로그 줄 꼴) + 수 찾기 (σ · 1/σ · 2σ · log σ · 단위 바꿈 · 유효숫자 3 자리 이상 ·
     지수 표기 · 자리 띄움 · float.hex) · 신원 · 등록 값 대조 (증거 없음 = rc 4) · 미수렴 · 가린 줄 · 결과 줄 꼴 바뀜 · 보고 못 씀
  M  변이: 판독기 사본을 한 군데씩 망가뜨리면 T 묶음이 잡는다 (리뷰어 변이 33 포함 · 잡지 못하면 실패)
  F  감시 셸: 가짜 러너 (git 고정물 저장소 = 핀): 등록 축 · 걷어내기 · PYTHONUNBUFFERED · 멈춤 조건 (잠금 · 동시 실행 · 런 전 관문 ·
     --show-results …) · STOPPED / DONE · 실패 보존 · 그룹 kill (TERM 을 무시하는 자식 · 러너만 죽음 = 고아) · 둘째 TERM · 묶음 꼴
  B  블록: KGY_BLOCK.md 의 블록을 그대로 꺼내 가짜 홈에서 (시도 1 → 시도 2 · 멈춤 조건 · 블록이 STOP 줄을 보여 준다)
  R  실물: 실제 러너 · 실제 payload · 픽스처 킷 (CPU · `scripts/test_rint_r_chain_e2e.py` 의 침대): 실물 꼴 · 실물 σ 가 판독기 출력 ·
     묶음에 없다 (양성 대조 포함) · 한도 도달 (시도 1 꼴) 뒤 다음 시도 (시도 2 꼴) · step3 통째 덤프 변이를 잡는다
★ 11-13 (Codex 반박 1/2 고침 묶음 · 1저자 Q4 · 원장 §3 시도 3 · 4 = 탄소 접합 원장 저장본 켬): T30 (판독기 · 저장본 기록 · audit 곁 파일 상태 ·
  목록) · F22 (감시 셸 · 시도 3 = 빈 저장본 짓고 씀 → 시도 4 = 적중 · 앞 조건 · 멈춤 조건 · graft · shallow) · F23 (감시 셸 git 읽기 = 저장소 고르는
  GIT_* 지움 · 대체 객체 끔) · R6 (실제 러너 · payload · 저장본 · 시도 3 → 4) · S16 (감시 셸 · 원장 §3 의 시도 3 · 4 줄)
⚠ PASS 는 준비물의 배선 · σ 비열람 · 실패 처리의 증거다.  실침대 반복 수 · 시간 · 메모리는 kgy 런이 잰다 (여기에 킷도 GPU 도 없다).
"""
import argparse
import ast
import contextlib
import glob
import hashlib
import io
import json
import math
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
LEDGER_FILE = os.path.join(ROOT, 'docs', 'reviews', 'rint2_dev_probe_ledger_20261026.md')
TOOLS_REL = 'docs/reviews/rint2_probe6_prep_20261110/tools'
RUNNER_REL = 'scripts/sdcp_gain_vox015_8arm.sh'
S0PLAN_REL = 'docs/data/rint2_s0_sbe_20261108/files/sdcp/ca1_s0_sbe_20261106_memfix/cjunc_plan.json'
PREREG_REL = 'docs/reviews/sdcp_gain_prereg_v2_20260816.md'
KIT = 'kit_SBE_vgcf100'
ARM = 'p2_SBE_vgcf100_sph_fa_cj1000000_78c44437_c0_rt1em12_fb10000_a0'
GIT_CFG = ('-c', 'user.email=t@t', '-c', 'user.name=t', '-c', 'commit.gpgsign=false', '-c', 'init.defaultBranch=main')
REAL_PS = shutil.which('ps') or '/bin/ps'


_RCM = []


def _rc():
    """run_contract (scripts/ 를 sys.path 에 넣지 않고 파일로 한 번 불러온다)."""
    if not _RCM:
        import importlib.util
        spec = importlib.util.spec_from_file_location('_run_contract_git_env', os.path.join(SCRIPTS, 'run_contract.py'))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _RCM.append(m)
    return _RCM[0]


def _drop_git_env():
    """★ 11-12 2 회차 (Rint ② 코드 묶음 · 재리뷰 RCP2-06) — 이 시험 프로세스와 그 자식 (고정물 git · 감시 셸 · 블록 bash 의 git fetch · worktree add) 은
    부르는 쪽 환경의 저장소 고르는 GIT_* 를 물려받지 않는다 (`run_contract.drop_git_env` 한 곳 · 시험 scripts/test_git_env_isolation.py G6)."""
    return _rc().drop_git_env()


_drop_git_env()

#: σ 류 자리에 심는 표식: 합성 폴더의 σ · 전류 · 구간 · 저항 · 소산 몫 값은 전부 0.00713331NNN 꼴이다
SENT = '71333'
#: 등록 축 (등록 R §10-1 (2) · 1저자 결정값): 시험의 독립 표 (감시 셸 · 원장 줄 초안 · 가짜 러너가 받은 env 를 이것과 대조한다)
AXES = {
    'VOX': '0.15', 'SDCP_SPHERE_D': '0.30', 'PTFE_STAMP': 'face_alpha', 'BRIDGE_UM': '0.48', 'SIGMA_AM_S_OVERRIDE': '0.0041',
    'SIGMA_SDCP_OVERRIDE': '256.6', 'SIGMA_FIBRE_BULK': '1e4', 'CJUNC': '1', 'CJUNC_RJ': '1e6', 'CJUNC_LEN_LAW': 'len_scaled_v0',
    'CJUNC_UNREG_LAW': 'cut', 'CJUNC_S_MIN_UM': '0.0', 'CJUNC_TOL_FF_UM': '0.07381254285530132', 'CJUNC_PTFE_JLAW': 'P0',
    'SDCP_MOD_C': '0', 'STEP3_RTOL': '1e-12', 'EXPECT_BACKEND': 'gpu', 'KITS': KIT, 'ARMS': '1', 'LEAN': '2',
}
#: 두 시도 (1저자 11-10): 시도 1 = 짧은 확인 (한도에 닿아 끝나는 것이 정상) · 시도 2 = 본 한도
ATTEMPT_MAXITER = {1: '30000', 2: '1500000'}
A1, A2 = ATTEMPT_MAXITER[1], ATTEMPT_MAXITER[2]
#: 시도 3 · 4 (11-13 · 원장 §3 · 1저자 Q4): 탄소 접합 원장 저장본 켬 · 한도 = 시도 2 와 같음 · 저장본 = ~/p6_cjstore (고정) · 기대 상태
STORE_ATTEMPTS = {3: '1500000', 4: '1500000'}
ALL_MAXITER = dict(ATTEMPT_MAXITER)
ALL_MAXITER.update(STORE_ATTEMPTS)
STORE_STATUS_T = {3: 'built_written', 4: 'hit'}
STORE_ST = ('hit', 'built_written', 'built_peer_same', 'unreadable_rebuilt', 'built_write_skipped', 'built_write_failed', 'disabled',
            'key_unavailable')
FAKE_KEY = 'ab' * 32
AUDIT_NAME = 'cjstore_audit_' + ARM + '.json'
#: 합성 기본 = 시도 2 꼴 (감시 셸 · 판독기가 시도 번호 ↔ 한도 짝을 본다 · P6R2-04 · 그래서 정직한 꼴의 한도는 등록 값뿐이다)
MAXITER = A2
#: R3 (실물 · 시도 1 꼴 · 한도에 닿음) 만 쓰는 사본 고침 (시험 전용): 짝 표의 시도 1 한도 → 2 (픽스처 침대는 한도 30000 안에서 모인다)
PAIR_PATCH_W = ('  1) WANT_MAX=30000;;\n', '  1) WANT_MAX=2;;\n')
PAIR_PATCH_R = ('ATTEMPT_MAXITER = {1: 30000, ', 'ATTEMPT_MAXITER = {1: 2, ')
PIN_FIX = 'e93efb6be' + '0' * 31                             # 합성 핀 (팔의 code_sha 가 그 앞자리)
S0_RUN = 'run_VGCF3_PTFE1_20261023_210442_2904445'
#: 풀이 코드 (P6R2-03 · 시험의 독립 표): 두 시도의 핀 사이에 이 경로가 바뀌면 시도 2 를 띄우지 않는다.  러너 · payload 가 여는 리포 파일을
#: 실물 러너 + payload (픽스처 침대) 를 strace 로 돌려 셌다 (11-10): scripts/ 밖 = 사전등록 (러너 · 있는지만) · EIS 앵커 표 (payload).
SOLVE_CODE = ('scripts/', 'docs/reviews/rint2_probe6_prep_20261110/tools/', 'docs/data/rint2_s0_sbe_20261108/',
              'docs/data/rint_eis_anchors.csv', 'docs/reviews/sdcp_gain_prereg_v2_20260816.md')

ARGS = None
TD = None
TAG = ''                                                   # 이 시험의 프로세스 표지 (가짜 ps 는 이 표지가 있는 프로세스만 보인다)
_ok, _fail, _skipped = 0, [], []
CASES = []
OPTIONAL = []                                              # --only 로 이름을 줄 때만 도는 묶음 (게이트 기본 실행에 없다)
WRAPPER_SRC = None                                         # 감시 셸 변이 묶음 (W) 이 핀 저장소에 넣을 사본 (None = 이 폴더의 감시 셸)


class _Caught(Exception):
    """변이 실행에서 첫 실패가 나면 그 묶음을 끝낸다 (잡힌 변이는 빨리 끝난다)."""


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


# ═════════════ 누출 검사 (P6R-01 · F7) ①: 수 찾기: σ 와 흔한 변형 (단위 · 1/σ · 2σ · log σ · 자릿수 · 지수 · 자리 띄움 · float.hex) ═════════════
#: 보고에 실린 해시 · 지문 값 (σ 가 숨을 수 없는 꼴) 은 **값으로** 지운다 (꼴로 지우면 긴 숫자열의 σ 도 같이 지워진다 · P6R-01).
SAFE_HEX_KEYS = frozenset(('sha256', 'listing_sha256', 'sha256sum_style', 'receipt_digest', 'receipt_code_sha', 'code_sha',
                           'input_digest', 'protocol_id', 'pin', 'attempt1_pin', 'tool_sha256_wrapper', 'tool_sha256_reader',
                           'runner_sha256', 'runner_log_sha256', 's0_plan_sha256', 'receipt_sha256'))
#: 수 낱말: 앞 글자가 글자 · 숫자 · _ · . 이면 낱말 시작이 아니다 (경로 · 이름 속 숫자는 수가 아니다) · 뒤 글자는 무엇이든 (0.007133S/cm)
_TOK = re.compile(r'(?<![A-Za-z0-9_.])[-+]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][-+]?[0-9]+)?')
#: (이름, 변환, 찾는 유효숫자 하한): σ 그 자체 (어느 단위 · ×10^k) 는 3 자리부터, 1/σ · 2σ 는 4 자리, 로그는 5 자리부터
#: (로그 값의 3 자리 끝수는 정직한 수와 흔히 겹친다 · 수정 리뷰어 변이의 로그 꼴은 %.6f 라 6 자리 이상).
TRANSFORMS = (('x', lambda v: v, 3), ('1/x', lambda v: 1.0 / v, 4), ('2x', lambda v: 2.0 * v, 4),
              ('log10', lambda v: math.log10(abs(v)), 5), ('log10(1e3x)', lambda v: math.log10(abs(v) * 1e3), 5),
              ('ln', lambda v: math.log(abs(v)), 5))


def safe_hex(rep, extra=()):
    out = set(x for x in extra if isinstance(x, str) and x)

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in SAFE_HEX_KEYS and isinstance(v, str):
                    out.add(v)
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(rep or {})
    return sorted((x for x in out if len(x) >= 6), key=len, reverse=True)


def strip_safe(text, safe):
    for s_ in safe:
        text = text.replace(s_, ' ')
    return text


def _mantissa(tok):
    """'0.0071330' → ('7133', True) · '7133' → ('7133', False): 앞뒤 0 을 뺀 유효숫자 (최대 17) · 소수점 / 지수가 있는가."""
    t = tok.lstrip('+-')
    isfloat = ('.' in t) or ('e' in t) or ('E' in t)
    body = re.split('[eE]', t)[0].replace('.', '')
    return body.lstrip('0')[:17].rstrip('0'), isfloat


def _digits(w, sd, trunc):
    if trunc:
        d = ('%.30e' % abs(w)).split('e')[0].replace('.', '')[:sd]
    else:
        d = ('%.*e' % (sd - 1, abs(w))).split('e')[0].replace('.', '')
    return d.rstrip('0')


def leak_targets(sealed):
    """봉인 값 · 변형마다 유효숫자 3–17 자리의 반올림 · 버림 숫자열 (10 의 거듭제곱에 무관 = S/cm · mS/cm · ×1e6 을 한 번에)."""
    tg, stream, hexs = {}, set(), set()
    for i, v in enumerate(sealed):
        if not isinstance(v, float) or not math.isfinite(v) or v == 0.0:
            continue
        for name, fn, sd0 in TRANSFORMS:
            try:
                w = fn(v)
            except (ValueError, ZeroDivisionError, OverflowError):
                continue
            if not math.isfinite(w) or w == 0.0:
                continue
            for sd in range(sd0, 18):
                for tr in (False, True):
                    d = _digits(w, sd, tr)
                    if len(d) >= sd0:
                        tg.setdefault(d, '%s of sealed #%d' % (name, i))
            if name in ('x', '1/x', '2x'):
                d6 = _digits(w, 6, False)
                if len(d6) == 6:
                    stream.add(d6)
                h = float.hex(w)
                if '.' in h:
                    hexs.add(h.split('.')[1].split('p')[0][:8].lower())
    return tg, stream, hexs


def scan_hits(texts, sealed, safe=(), sd_min=3, floats_only=False, stream=False, hexsearch=False):
    """σ 류 값이 글 어디엔가 있는가 → 맞은 곳 목록 (값 자체는 적지 않는다).
    sd_min = 볼 유효숫자 하한 · floats_only = 소수점 / 지수가 있는 수만 · stream = 숫자만 이어 붙인 열에서 6 자리 (자리 띄움) ·
    hexsearch = float.hex 가수 8 자리."""
    tg, st, hx = leak_targets(sealed)
    hits = []
    for i, t in enumerate(texts):
        if not t:
            continue
        u = strip_safe(t, safe)
        for m in _TOK.finditer(u):
            mant, isfloat = _mantissa(m.group(0))
            if len(mant) < sd_min or (floats_only and not isfloat):
                continue
            if mant in tg:
                hits.append('text %d: number with %d significant digits = %s' % (i, len(mant), tg[mant]))
        if stream:
            dig = re.sub(r'[^0-9]', '', u)
            for d6 in st:
                if d6 in dig:
                    hits.append('text %d: 6 sealed digits in the digit stream (spaced digits?)' % i)
                    break
        if hexsearch:
            low = u.lower()
            for h in hx:
                if len(h) >= 8 and h in low:
                    hits.append('text %d: float.hex mantissa of a sealed value' % i)
                    break
    return hits


# ═════════════ 누출 검사 ②: 구조: 보고 JSON 의 키는 닫힌 목록 · 칸마다 정해진 꼴 (step3 통째 덤프 · 새 칸 · 글 칸에 숨긴 수 = 실패) ═════════════
#: 이 표는 판독기 표의 사본이 아니다 (시험이 따로 적는다): 판독기 표에 σ 칸을 더하는 변이는 여기서 걸린다.
CERT_ST = ('POSITIVE_SOLVED', 'VALID_ZERO_TOPOLOGY', 'ELECTRODE_SHORT', 'NOT_CERTIFIABLE')
COMP_ST = ('complete', 'unconverged', 'not_solvable', 'failed', 'disabled', 'skipped', 'missing')
FIELD_SCHEMA = {
    'n_dof': 'posint', 'cg_iters': 'int', 'cg_info': 'sint', 'cg_resid': 'num+', 'unconverged': 'bool',
    'cert_version': ('re', r'conv-cert-v[0-9]{1,3}'), 'cert_status': ('enum', CERT_ST), 'cert_ok': 'bool',
    'cert_pass_a': 'bool', 'cert_pass_b': 'bool', 'cert_pass_c': 'bool', 'cert_pass_d': 'boolnull', 'cert_info': 'sint',
    'cert_resid': 'num+', 'cert_imbalance': 'num+', 'cert_iters': 'int', 'cert_resolve_iters': 'int', 'cert_resolve_info': 'sint',
    'cert_rtol_used': 'rtol', 'cert_rtol_max': 'rtol', 'cert_eps_I': 'rtol', 'cert_resolve_rtol': 'rtol', 'cert_target_tol': 'rtol',
    'backend_requested': ('enum', ('gpu', 'cpu')), 'backend_used': ('enum', ('gpu', 'cpu')), 'backend_precond': ('enum', ('jacobi', 'amg')),
    'backend_rtol': 'rtol', 'electronic_status': ('enum', COMP_ST), 'electronic_backend_used': ('enum', ('gpu', 'cpu')),
    'manifest_status': ('enum', ('complete', 'partial', 'failed')), 'protocol_id': ('re', r'p[0-9a-z]{1,8}-[0-9a-f]{8,64}'),
    'code_sha': ('re', r'[0-9a-f]{7,40}(\+dirty)?'), 'input_digest': ('re', r'[0-9a-f]{16}'),
    'backend_fallback': 'bool', 'origin_shift_zero': 'bool', 'bed_inputs_match_s0': 'bool', 'tol_ff_matches_s0': 'bool',
    'code_matches_pin': 'bool', 'rj_matches_registered': 'bool'}
#: 팔 칸의 출처 (mpm_metrics.step3 아래 경로 · 시험의 독립 표): 값이 있으면 팔의 그 자리 값과 같아야 한다
FIELD_PATHS = {
    'n_dof': ('n_dof',), 'cg_iters': ('cg_iters',), 'cg_info': ('cg_info',), 'cg_resid': ('cg_resid',), 'unconverged': ('unconverged',),
    'cert_version': ('conv_cert', 'version'), 'cert_status': ('conv_cert', 'status'), 'cert_ok': ('conv_cert', 'ok'),
    'cert_pass_a': ('conv_cert', 'pass_a'), 'cert_pass_b': ('conv_cert', 'pass_b'), 'cert_pass_c': ('conv_cert', 'pass_c'),
    'cert_pass_d': ('conv_cert', 'pass_d'), 'cert_info': ('conv_cert', 'info'), 'cert_resid': ('conv_cert', 'resid'),
    'cert_imbalance': ('conv_cert', 'imbalance'), 'cert_iters': ('conv_cert', 'iters'),
    'cert_resolve_iters': ('conv_cert', 'resolve_iters'), 'cert_resolve_info': ('conv_cert', 'resolve_info'),
    'cert_rtol_used': ('conv_cert', 'rtol_used'), 'cert_rtol_max': ('conv_cert', 'rtol_max'), 'cert_eps_I': ('conv_cert', 'eps_I'),
    'cert_resolve_rtol': ('conv_cert', 'resolve_rtol'), 'cert_target_tol': ('conv_cert', 'target_tol'),
    'backend_requested': ('manifest', 'backend_last_solve', 'requested'), 'backend_used': ('manifest', 'backend_last_solve', 'used'),
    'backend_precond': ('manifest', 'backend_last_solve', 'precond'), 'backend_rtol': ('manifest', 'backend_last_solve', 'rtol'),
    'electronic_status': ('manifest', 'components', 'electronic', 'status'),
    'electronic_backend_used': ('manifest', 'components', 'electronic', 'backend', 'used'),
    'manifest_status': ('manifest', 'status'), 'protocol_id': ('manifest', 'physics_protocol_id'),
    'code_sha': ('manifest', 'code_sha'), 'input_digest': ('manifest', 'input_digest')}
RECEIPT_SCHEMA = {
    'receipt_digest': ('re', r'[0-9a-f]{8,64}'), 'receipt_code_sha': ('re', r'[0-9a-f]{7,40}(\+dirty)?'), 'receipt_arms': 'posint',
    'receipt_expect_backend': ('enum', ('gpu', 'cpu')), 'receipt_step3_rtol': 'rtol', 'receipt_vox_um': 'num+',
    'receipt_ptfe_stamp': ('enum', ('off', 'centerline', 'face_alpha')), 'receipt_sha256': 'hex64', 'receipt_has_arm_list': 'bool'}
ENV_KEYS_T = ('python', 'python_impl', 'numpy', 'scipy', 'cupy', 'cupy_cuda_runtime', 'numpy_blas', 'blas_core', 'gpu_name',
              'gpu_driver', 'gpu_mem_total_mib', 'cuda_version', 'kernel', 'os', 'cpu_model', 'nproc', 'mem_total_kb', 'git', 'bash')
ENV_NAMES_T = ('CUDA_VISIBLE_DEVICES', 'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'OPENBLAS_CORETYPE', 'PYTHONUNBUFFERED', 'BASH_ENV')
#: 감시 셸 meta.txt 의 키 (시험의 독립 표): (int | str, 값 꼴)
META_SCHEMA = dict([
    ('probe6_meta_version', ('int', r'[0-9]{1,3}')), ('attempt', ('int', r'[1-4]')), ('pin', ('str', r'[0-9a-f]{40}')),
    ('attempt2_pin', ('str', r'[0-9a-f]{40}')), ('attempt3_pin', ('str', r'[0-9a-f]{40}')), ('code_same_as_attempt3', ('int', r'[01]')),
    ('store', ('str', r'~?[A-Za-z0-9._/+-]{1,300}')),
    ('store_listing_before', ('str', r'(?:[A-Za-z0-9._+-]{1,120}:(?:[0-9a-f]{64}|other)(?:,[A-Za-z0-9._+-]{1,120}:(?:[0-9a-f]{64}|other)){0,15})?')),
    ('store_listing_after', ('str', r'(?:[A-Za-z0-9._+-]{1,120}:(?:[0-9a-f]{64}|other)(?:,[A-Za-z0-9._+-]{1,120}:(?:[0-9a-f]{64}|other)){0,15})?')),
    ('attempt1_pin', ('str', r'[0-9a-f]{40}')), ('code_same_as_attempt1', ('int', r'[01]')),
    ('maxiter', ('int', r'[0-9]{1,9}')), ('expect_rtol', ('str', r'[0-9][0-9.eE+-]{0,11}')), ('expect_backend', ('str', r'gpu|cpu')),
    ('expect_rj', ('str', r'[0-9][0-9.eE+-]{0,11}')), ('pythonpath_removed', ('int', r'[01]')),
    ('kit', ('str', r'kit_SBE_vgcf100')), ('kit_run', ('str', r'[A-Za-z0-9._+-]{1,120}')), ('kit_run_matches_s0', ('int', r'[01]')),
    ('outdir', ('str', r'~?[A-Za-z0-9._/+-]{1,300}')), ('logdir', ('str', r'~?[A-Za-z0-9._/+-]{1,300}')),
    ('start_epoch', ('int', r'[0-9]{9,11}')), ('start_kst', ('str', r'[0-9T:+-]{19,25}')), ('end_epoch', ('int', r'[0-9]{9,11}')),
    ('end_kst', ('str', r'[0-9T:+-]{19,25}')), ('wall_s', ('int', r'[0-9]{1,8}')), ('runner_rc', ('int', r'[0-9]{1,3}')),
    ('solve_started', ('int', r'[01]')), ('orphans', ('int', r'[0-9]{1,6}')), ('orphans_left', ('int', r'[0-9]{1,6}')),
    ('cap_gb', ('int', r'[0-9]{1,4}')), ('cap_term', ('int', r'[01]')), ('aborted', ('int', r'[01]')), ('sample_s', ('int', r'[0-9]{1,4}')),
    ('time_v', ('int', r'[01]')), ('umask', ('str', r'[0-7]{3,4}')), ('mode_bad', ('int', r'[0-9]{1,6}')),
    ('git_lines_before', ('int', r'[0-9]{1,6}')), ('git_lines_after', ('int', r'[0-9]{1,6}')), ('pregate', ('int', r'[01]')),
    ('scrubbed', ('str', r'[A-Z0-9_ ]{0,600}')), ('pythonpath_set', ('int', r'[01]')),
    ('gpu_used_start_mib', ('str', r'[0-9]{1,7}|NA')), ('disk_free_gb_kit', ('str', r'[0-9]{1,9}|NA')),
    ('disk_free_gb_log', ('str', r'[0-9]{1,9}|NA')),
    ('tool_sha256_wrapper', ('str', r'[0-9a-f]{64}')), ('tool_sha256_reader', ('str', r'[0-9a-f]{64}')),
    ('runner_sha256', ('str', r'[0-9a-f]{64}')), ('runner_log_sha256', ('str', r'[0-9a-f]{64}')),
    ('s0_plan_sha256', ('str', r'[0-9a-f]{64}')), ('kit_run_before', ('int', r'[0-9]{1,4}')), ('kit_run_new', ('int', r'[0-9]{1,4}'))]
    + [('env_' + n, ('str', r'unset|empty|set|value:[A-Za-z0-9][A-Za-z0-9,._-]{0,31}')) for n in ENV_NAMES_T])
LOG_SCHEMA = {
    'n_lines': 'int', 'arm_tag': ('re', r'p2_[A-Za-z0-9_]+_a[0-7]'), 'arm_shift_zero': 'bool', 'skip_cached': 'bool',
    'gate_receipt': 'bool', 'gate_discipline': 'bool', 'gate_undefined': 'bool', 'cg_maxiter': 'int|', 'cg_rtol': 'num+|',
    'face_alpha_prep_s': 'int|', 'cjunc_prep_s': 'int|', 'solve_n_dof': 'int|', 'solve_plate_bot': 'int|', 'solve_plate_top': 'int|',
    'solve_backend': ('enum', ('GPU', 'CPU')), 'not_converged_info': 'sint|', 'not_converged_resid': 'num+|',
    'cert_fail_status': ('enum|', CERT_ST), 'cert_fail_pass': 'pass4', 'cert_fail_imbalance': 'num+|', 'sealed': 'bool',
    'done_vox_um': 'num+|', 'done_n_dof': 'int|', 'done_resid': 'num+|', 'done_step3_s': 'int|',
    'runner_peak_tag': ('re|', r'p2_[A-Za-z0-9_]+'), 'runner_peak_rss_gb': 'num+|', 'saved': 'bool', 'masked_lines': 'masked',
    'masked_lines_dropped': 'int'}
TIMING_SCHEMA = dict((k, 'sint') for k in ('wall_s', 'runner_rc', 'step3_stage_s', 'face_alpha_prep_s', 'cjunc_prep_s', 'pre_step3_s',
                                         'raster_prep_s', 'cg_cert_s', 'resolution_s', 'solve_to_end_s'))
TIMING_SCHEMA['cg_cert_s_per_iter'] = 'num+'
RES_SCHEMA = dict((k, 'int') for k in ('n_samples', 'rss_sum_max_kb', 'rss_proc_max_kb', 'gpu_used_max_mib', 'gpu_ours_max_mib',
                                     'gpu_util_max_pct', 'gpu_used_first_mib', 'time_v_max_rss_kb', 'time_v_elapsed_s',
                                     'arm_time_v_max_rss_kb', 'arm_time_v_elapsed_s', 'cap_gb', 'cap_term'))
RES_SCHEMA['runner_peak_rss_gb'] = 'num+'
HELD_BACK_T = ['conv_cert.dsigma_rel', 'conv_cert.target_err_bound_rel', 'conv_cert.target_width_rel', 'conv_cert.target_in_bracket']
TOP_KEYS = frozenset(('schema', 'tool', 'scope', 'held_back', 'folder', 'receipt', 'meta', 'env', 'attempt', 'kit_run_new_files',
                      'kit_run_before_files', 'source', 'arm', 'fields', 's0_plan_sha256', 'log', 'timing', 'resources', 'verdict', 'rc',
                      'problems', 'notes', 'store'))
TOP_REQUIRED = TOP_KEYS - {'arm', 's0_plan_sha256', 'log', 'store'}
#: ★ 11-13 저장본 audit 곁 파일 칸 (판독기의 닫힌 표 · 신원 글만)
STORE_SCHEMA = {'audit_file': ('re', r'cjstore_audit_p2_[A-Za-z0-9_]+_a0\.json'), 'audit_schema': ('re', r'cjstore-audit-v[0-9]{1,3}'),
                'status': ('enum', STORE_ST), 'key': 'hex64', 'file': ('re', r'cjreg_[0-9a-f]{64}\.npz'), 'file_sha256': 'hex64',
                'audit_sha256': 'hex64'}
VERDICT_RC = {'PROBE_OK': 0, 'PROBE_NOT_CONVERGED': 3, 'PROBE_INCOMPLETE': 4, 'PROBE_REJECTED': 5}
_REASON = re.compile(r"[A-Za-z0-9 (),/'_.-]{1,100}")
_SUPSUB_T = '⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉'


def is_missing(v):
    return isinstance(v, dict) and 'missing' in v


def _miss_ok(v):
    return isinstance(v, dict) and list(v) == ['missing'] and isinstance(v['missing'], str) and _REASON.fullmatch(v['missing']) is not None


def _isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))


def has_digit(s):
    return bool(re.search(r'\d', s)) or any(c in _SUPSUB_T for c in s) or bool(re.search(r'0[xX][0-9a-fA-F]', s))


def _kind_ok(kind, v):
    if isinstance(kind, tuple):
        if kind[0] in ('enum', 'enum|'):
            return (v is None and kind[0] == 'enum|') or (isinstance(v, str) and v in kind[1])
        if kind[0] in ('re', 're|'):
            return (v is None and kind[0] == 're|') or (isinstance(v, str) and re.fullmatch(kind[1], v) is not None)
        return False
    if kind.endswith('|'):
        return v is None or _kind_ok(kind[:-1], v)
    if kind == 'posint':
        return isinstance(v, int) and not isinstance(v, bool) and v > 0
    if kind == 'int':
        return isinstance(v, int) and not isinstance(v, bool) and v >= 0
    if kind == 'sint':
        return isinstance(v, int) and not isinstance(v, bool)
    if kind == 'num+':
        return _isnum(v) and float(v) >= 0.0
    if kind == 'rtol':
        return _isnum(v) and 0.0 < float(v) < 1.0
    if kind == 'bool':
        return isinstance(v, bool)
    if kind == 'boolnull':
        return v is None or isinstance(v, bool)
    if kind == 'hex64':
        return isinstance(v, str) and re.fullmatch(r'[0-9a-f]{64}', v) is not None
    if kind == 'pass4':
        return isinstance(v, list) and len(v) == 4 and all(x is None or isinstance(x, bool) for x in v)
    if kind == 'masked':
        return isinstance(v, list) and all(isinstance(x, str) and len(x) <= 240 and not has_digit(x) for x in v)
    return False


def _table_problems(name, d, schema, allow_missing=True, need_all=False):
    P = []
    if not isinstance(d, dict):
        return ['%s is not an object' % name]
    for k, v in d.items():
        if k not in schema:
            P.append('%s: unknown key %s' % (name, k))
        elif not ((allow_missing and _miss_ok(v)) or _kind_ok(schema[k], v)):
            P.append('%s: key %s has an unexpected value shape' % (name, k))
    if need_all:
        P += ['%s: key %s absent' % (name, k) for k in schema if k not in d]
    return P


def report_problems(rep):
    """닫힌 허용 목록 · 칸마다 꼴: 문제 목록 (빈 목록 = 통과)."""
    if not isinstance(rep, dict):
        return ['report is not an object']
    P = ['unknown top key %s' % k for k in rep if k not in TOP_KEYS]
    P += ['top key %s absent' % k for k in TOP_REQUIRED if k not in rep]
    if rep.get('schema') != 'rint2-probe6-report-v2':
        P.append('schema name')
    tool = rep.get('tool')
    if not (isinstance(tool, dict) and set(tool) == {'name', 'sha256'} and tool.get('name') == 'probe6_read.py'
            and _kind_ok('hex64', tool.get('sha256'))):
        P.append('tool block shape')
    if rep.get('scope') not in ('outdir_and_logdir', 'outdir_only'):
        P.append('scope')
    if rep.get('held_back') != HELD_BACK_T:
        P.append('held_back list differs')
    if rep.get('source') not in ('none', 'outdir', 'kit_run_failed', 'kit_run_unmoved'):
        P.append('source')
    if VERDICT_RC.get(rep.get('verdict')) != rep.get('rc') or isinstance(rep.get('rc'), bool):
        P.append('verdict / rc')
    for k in ('problems', 'notes'):
        x = rep.get(k)
        if not (isinstance(x, list) and all(isinstance(s, str) and len(s) <= 400 and all(32 <= ord(c) < 127 for c in s) for s in x)):
            P.append('%s list shape' % k)
    a = rep.get('attempt')
    if not (_miss_ok(a) or (isinstance(a, int) and not isinstance(a, bool) and a in (1, 2, 3, 4))):
        P.append('attempt shape')
    if 'store' in rep:
        P += _table_problems('store', rep['store'], STORE_SCHEMA)
    fo = rep.get('folder')
    if not (isinstance(fo, dict) and set(fo) == {'n_files', 'files', 'listing_sha256', 'sha256sum_style', 'problem', 'path'}):
        P.append('folder block keys')
    else:
        if not (fo['n_files'] is None or _kind_ok('int', fo['n_files'])):
            P.append('folder n_files')
        for h in ('listing_sha256', 'sha256sum_style'):
            if not (fo[h] is None or _kind_ok('hex64', fo[h])):
                P.append('folder %s' % h)
        if not (fo['problem'] is None or (isinstance(fo['problem'], str) and _REASON.fullmatch(fo['problem']))):
            P.append('folder problem text')
        if not (isinstance(fo['path'], str) and re.fullmatch(r'~?[A-Za-z0-9._/+-]{1,400}', fo['path'])):
            P.append('folder path')
        for x in fo['files'] if isinstance(fo['files'], list) else [None]:
            if not (isinstance(x, dict) and set(x) == {'path', 'size', 'sha256'} and isinstance(x['path'], str)
                    and re.fullmatch(r'[A-Za-z0-9._/+-]{1,300}', x['path']) and _kind_ok('int', x['size'])
                    and _kind_ok('hex64', x['sha256'])):
                P.append('folder file entry shape')
    rc_ = rep.get('receipt')
    P += _table_problems('receipt', rc_, RECEIPT_SCHEMA)
    for name, schema in (('meta', None), ('env', None)):
        d = rep.get(name)
        if _miss_ok(d):
            continue
        if not isinstance(d, dict):
            P.append('%s shape' % name)
            continue
        for k, v in d.items():
            if name == 'meta':
                if k not in META_SCHEMA:
                    P.append('meta: unknown key %s' % k)
                    continue
                conv, pat = META_SCHEMA[k]
                if conv == 'int':
                    ok = isinstance(v, int) and not isinstance(v, bool) and re.fullmatch(pat, str(v)) is not None
                else:
                    ok = isinstance(v, str) and re.fullmatch(pat, v) is not None
                if not ok:
                    P.append('meta: key %s value shape' % k)
            else:
                if k not in ENV_KEYS_T or not (isinstance(v, str) and re.fullmatch(r'[A-Za-z0-9 ._:+()/@,#-]{0,120}', v)):
                    P.append('env: key %s or its value' % k)
    for name, keys in (('kit_run_new_files', ({'name', 'size', 'sha256'}, {'name', 'size', 'sha256', 'copy_ok'})),
                       ('kit_run_before_files', ({'name', 'size', 'sha256'},))):
        x = rep.get(name)
        if not isinstance(x, list):
            P.append('%s shape' % name)
            continue
        for e in x:
            if not (isinstance(e, dict) and set(e) in keys and isinstance(e.get('name'), str)
                    and re.fullmatch(r'\.?(?:peak_rss_)?p2_SBE_vgcf100_[A-Za-z0-9_.]{1,200}', e['name'])
                    and _kind_ok('int', e.get('size')) and _kind_ok('hex64', e.get('sha256'))
                    and ('copy_ok' not in e or isinstance(e['copy_ok'], bool))):
                P.append('%s entry shape' % name)
    if 'arm' in rep:
        a = rep['arm']
        if not (isinstance(a, dict) and set(a) == {'file', 'size', 'sha256', 'index'} and isinstance(a['file'], str)
                and re.fullmatch(r'p2_[A-Za-z0-9_]+_a0\.json(\.failed)?', a['file']) and _kind_ok('int', a['size'])
                and _kind_ok('hex64', a['sha256']) and a['index'] == 0):
            P.append('arm block shape')
    if 's0_plan_sha256' in rep and not _kind_ok('hex64', rep['s0_plan_sha256']):
        P.append('s0_plan_sha256 shape')
    P += _table_problems('fields', rep.get('fields'), FIELD_SCHEMA, need_all=True)
    if 'log' in rep and not _miss_ok(rep['log']):
        P += _table_problems('log', rep['log'], LOG_SCHEMA, allow_missing=False)
    P += _table_problems('timing', rep.get('timing'), TIMING_SCHEMA)
    P += _table_problems('resources', rep.get('resources'), RES_SCHEMA)
    return P


def pick(obj, path):
    cur = obj
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return False, None
        cur = cur[k]
    return True, cur


def fields_provenance(rep, arm):
    """값이 있는 팔 칸 = 팔의 그 자리 값 (허용 칸에 σ 를 옮겨 담는 변이 · 경로를 바꾸는 변이를 잡는다)."""
    P = []
    s3 = ((arm or {}).get('mpm_metrics') or {}).get('step3') if isinstance(arm, dict) else None
    if not isinstance(s3, dict):
        return P
    f = rep.get('fields') or {}
    for name, path in FIELD_PATHS.items():
        v = f.get(name)
        if _miss_ok(v) or name not in f:
            continue
        found, av = pick(s3, path)
        if not found:
            P.append('field %s has a value but the arm has no such key' % name)
        elif isinstance(av, bool) or isinstance(v, bool) or av is None or v is None:
            if av is not v:
                P.append('field %s differs from the arm' % name)
        elif _isnum(av) and _isnum(v):
            if float(av) != float(v):
                P.append('field %s differs from the arm' % name)
        elif av != v:
            P.append('field %s differs from the arm' % name)
    return P


def _fmt(v):
    """판독기 화면의 값 꼴 (시험의 독립 구현)."""
    if is_missing(v):
        return 'NONE (%s)' % v['missing']
    if isinstance(v, bool) or v is None:
        return str(v)
    if isinstance(v, float):
        return '%.6g' % v
    return str(v)


_NOKEY = object()


def screen_problems(screen, rep):
    """판독기 화면 줄마다: 아는 꼴 · 아는 키 · 그 값 = 보고의 값 (화면에만 따로 새는 값이 없다)."""
    P = []
    if not isinstance(rep, dict):
        return ['no report']
    fl = rep.get('fields') or {}
    lg = rep.get('log') if isinstance(rep.get('log'), dict) and not is_missing(rep.get('log')) else {}
    tm, rs = rep.get('timing') or {}, rep.get('resources') or {}
    env = rep.get('env') if isinstance(rep.get('env'), dict) and not is_missing(rep.get('env')) else {}
    meta = rep.get('meta') if isinstance(rep.get('meta'), dict) and not is_missing(rep.get('meta')) else {}
    rcp = rep.get('receipt') or {}
    fo = rep.get('folder') or {}
    sec = 'head'
    for ln in screen.splitlines():
        if not ln.startswith('[probe6] '):
            P.append('screen line without the [probe6] prefix')
            continue
        b = ln[len('[probe6] '):]
        if re.fullmatch(r'--- .+ ---', b):
            sec = b
            continue
        m = re.fullmatch(r'verdict (\S+) \(rc (-?\d+)\)   source (\S+)   scope (\S+)   attempt (.+)', b)
        if m:
            if (m.group(1), int(m.group(2)), m.group(3), m.group(4), m.group(5)) != (
                    rep.get('verdict'), rep.get('rc'), rep.get('source'), rep.get('scope'), _fmt(rep.get('attempt'))):
                P.append('verdict line differs from the report')
            continue
        m = re.fullmatch(r'arm (\S+)  size (\d+)  sha256 ([0-9a-f]{64})', b)
        if m:
            a = rep.get('arm') or {}
            if (m.group(1), int(m.group(2)), m.group(3)) != (a.get('file'), a.get('size'), a.get('sha256')):
                P.append('arm line differs from the report')
            continue
        m = re.fullmatch(r'masked_failure_lines\s+= (\d+) \((\d+) dropped from the middle; digits masked; see the report\)', b)
        if m:
            if (int(m.group(1)), int(m.group(2))) != (len(lg.get('masked_lines') or []), lg.get('masked_lines_dropped') or 0):
                P.append('masked line count differs')
            continue
        m = re.fullmatch(r'folder (.*)  files (\S+)', b)
        if m:
            if (m.group(1), m.group(2)) != (str(fo.get('path')), str(fo.get('n_files'))):
                P.append('folder line differs')
            continue
        m = re.fullmatch(r'folder sha256 \(name size sha256 listing\) = (\S+)', b)
        if m:
            if m.group(1) != str(fo.get('listing_sha256')):
                P.append('folder listing sha differs')
            continue
        m = re.fullmatch(r'folder sha256 \(sha256sum style\)\s+= (\S+)', b)
        if m:
            if m.group(1) != str(fo.get('sha256sum_style')):
                P.append('folder sha256sum sha differs')
            continue
        m = re.fullmatch(r'kit run new file (\S+)  size (\d+)  sha256 ([0-9a-f]{64})  copy_ok (\S+)', b)
        if m:
            if not any((x.get('name'), str(x.get('size')), x.get('sha256'), str(x.get('copy_ok'))) == m.groups()
                       for x in rep.get('kit_run_new_files') or []):
                P.append('kit run new file line not in the report')
            continue
        m = re.fullmatch(r'kit run earlier file \(copied before the start\) (\S+)  size (\d+)  sha256 ([0-9a-f]{64})', b)
        if m:
            if not any((x.get('name'), str(x.get('size')), x.get('sha256')) == m.groups() for x in rep.get('kit_run_before_files') or []):
                P.append('kit run earlier file line not in the report')
            continue
        m = re.fullmatch(r'held back \(names only\): (.*)', b)
        if m:
            if m.group(1) != ' '.join(rep.get('held_back') or []):
                P.append('held back line differs')
            continue
        m = re.fullmatch(r'problem: (.*)', b)
        if m:
            if m.group(1) not in [p.encode('ascii', 'replace').decode('ascii') for p in rep.get('problems') or []]:
                P.append('problem line not in the report')
            continue
        m = re.fullmatch(r'READER_CRASH [A-Za-z]+ while writing the report or the filtered log \(no value printed\) - rc 4', b)
        if m:
            continue
        if b.startswith('store audit '):
            st_ = rep.get('store') or {}
            miss_ = {'missing': 'absent'}
            want_ = 'store audit %s  status %s  key %s  file %s  file_sha256 %s' % (
                st_.get('audit_file'), _fmt(st_.get('status', miss_)), _fmt(st_.get('key', miss_)), _fmt(st_.get('file', miss_)),
                _fmt(st_.get('file_sha256', miss_)))
            if b != want_.encode('ascii', 'replace').decode('ascii'):
                P.append('store audit line differs from the report')
            continue
        m = re.fullmatch(r'(\S+)\s+= (.*)', b)
        if m:
            k, val = m.group(1), m.group(2)
            if sec.startswith('--- solver'):
                want = _fmt(fl[k]) if k in fl else _NOKEY
            elif sec.startswith('--- runner log'):
                want = _fmt(lg[k]) if k in lg else _NOKEY
            elif sec.startswith('--- time'):
                want = _fmt(tm[k]) if k in tm else _NOKEY
            elif sec.startswith('--- memory'):
                want = _fmt(rs[k]) if k in rs else _NOKEY
            elif sec.startswith('--- environment'):
                want = str(env[k]) if k in env else (str(meta[k]) if k in meta else _NOKEY)
            elif sec.startswith('--- receipt'):
                want = _fmt(rcp[k]) if k in rcp else _NOKEY
            else:
                want = _NOKEY
            if want is _NOKEY:
                P.append('screen key %s is not a report key of its section' % k)
            elif val != want.encode('ascii', 'replace').decode('ascii'):
                P.append('screen value of %s differs from the report' % k)
            continue
        P.append('screen line of an unknown form')
    return P


def filtered_problems(text, rep):
    """걸러 낸 로그: 줄마다 아는 꼴 · 수는 보고의 값과 같다 · 가린 줄에 숫자 없음."""
    P = []
    lg = rep.get('log') if isinstance(rep, dict) and isinstance(rep.get('log'), dict) and not is_missing(rep.get('log')) else {}

    def same(key, s):
        return s == (repr(lg.get(key)) if isinstance(lg.get(key), float) else str(lg.get(key)))
    for ln in text.splitlines():
        m = re.fullmatch(r'arm_start tag=(\S+) shift_zero=([01])', ln)
        if m:
            ok = m.group(1) == lg.get('arm_tag')
        elif ln in ('skip_cached=1', 'gate_receipt=1', 'gate_discipline=1', 'gate_undefined=1', 'step3_voxelize_start',
                    'payload_saved=1', 'step3_done SEAL_BROKEN (value not copied)', 'collector_line SEAL_BROKEN (value not copied)',
                    'result_line SEAL_BROKEN (value not copied)'):
            ok = True
        elif re.fullmatch(r'(cg_maxiter|cg_rtol|face_alpha_prep_s|cjunc_prep_s|runner_peak_rss_gb)=(.*)', ln):
            k, v = ln.split('=', 1)
            ok = same(k, v)
        elif re.fullmatch(r'masked_dropped=(\d+)', ln):
            ok = int(ln.split('=')[1]) == lg.get('masked_lines_dropped')
        elif ln.startswith('masked: '):
            ok = ln[len('masked: '):] in (lg.get('masked_lines') or []) and not has_digit(ln[len('masked: '):])
        else:
            m1 = re.fullmatch(r'step3_solve n_dof=(\S+) plate_bot=(\S+) plate_top=(\S+) backend=(\S+)', ln)
            m2 = re.fullmatch(r'cg_not_converged info=(\S+) resid=(\S+)', ln)
            m3 = re.fullmatch(r'cert_fail status=(\S+) pass_abcd=(\S+) imbalance=(\S+)', ln)
            m4 = re.fullmatch(r'step3_done n_dof=(\S+) resid=(\S+) step3_s=(\S+) sealed=([01])', ln)
            if m1:
                ok = (same('solve_n_dof', m1.group(1)) and same('solve_plate_bot', m1.group(2)) and same('solve_plate_top', m1.group(3))
                      and same('solve_backend', m1.group(4)))
            elif m2:
                ok = same('not_converged_info', m2.group(1)) and same('not_converged_resid', m2.group(2))
            elif m3:
                ok = (same('cert_fail_status', m3.group(1)) and m3.group(2) == ','.join(str(x) for x in lg.get('cert_fail_pass') or [])
                      and same('cert_fail_imbalance', m3.group(3)))
            elif m4:
                ok = same('done_n_dof', m4.group(1)) and same('done_resid', m4.group(2)) and same('done_step3_s', m4.group(3))
            else:
                ok = False
        if not ok:
            P.append('filtered log line of an unknown form or with a value that is not the report value')
    return P


# ═════════════════════════ 합성 출력 폴더 (실제 러너 · payload 가 쓰는 꼴 · 11-10 픽스처 킷 실물에서 본뜸) ═════════════════════════
def sent(i):
    return float('0.00713331%03d' % i)


#: 합성 폴더의 봉인 값 전부 (σ · 전류 · 구간 · 소산 몫 · 입력 σ_VGCF · 실패 줄의 값): 수 찾기의 과녁
T_SEALED = sorted(set([sent(i) for i in range(1, 40)] + [sent(3) * 1e-7, sent(6) * 100, sent(11) * 1e-7, sent(15) * 1e-13,
                                                          sent(16) * 1e-6, sent(18) * 1e-11, sent(25) * 100, sent(35) * 1000,
                                                          7133.31, -0.00713331901, 7.13331e-03, 0.00713331905]))


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
     CERT|sigma| 증서 σ 7.13331e-03 ≠ 결과 σ 0.00713331905 — 증서가 이 결과의 것이 아니다
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
    """감시 셸 meta.txt 꼴 (기본 = 시도 2 · 한도 1500000 · 시도 1 의 핀 · 풀이 코드 같음).  값 None = 그 줄을 뺀다."""
    m = [('probe6_meta_version', '2'), ('attempt', '2'), ('pin', PIN_FIX), ('attempt1_pin', PIN_FIX), ('code_same_as_attempt1', '1'),
         ('maxiter', MAXITER), ('expect_rtol', '1e-12'), ('expect_backend', 'gpu'), ('expect_rj', '1e6'),
         ('kit', KIT), ('kit_run', S0_RUN), ('kit_run_matches_s0', '1'), ('outdir', '~/sdcp/ca1_probe6_a2_x_arm1'),
         ('logdir', '~/p6log_a2_x'), ('start_epoch', str(T0)), ('start_kst', '2026-11-10T15:00:00+0900'), ('end_epoch', str(T0 + 11900)),
         ('end_kst', '2026-11-10T18:18:20+0900'), ('wall_s', '11900'), ('runner_rc', '0'), ('solve_started', '1'), ('orphans', '0'),
         ('orphans_left', '0'), ('cap_gb', '46'), ('cap_term', '0'), ('aborted', '0'), ('sample_s', '10'), ('time_v', '1'),
         ('umask', '0022'), ('mode_bad', '0'), ('git_lines_before', '0'), ('git_lines_after', '0'), ('pregate', '1'),
         ('scrubbed', 'SIGMA_VGCF_OVERRIDE'), ('pythonpath_set', '0'), ('pythonpath_removed', '0')] + \
        [('env_' + n, 'value:1' if n == 'PYTHONUNBUFFERED' else 'unset') for n in ENV_NAMES_T] + \
        [('gpu_used_start_mib', '1234'), ('disk_free_gb_kit', '100'), ('disk_free_gb_log', '50'),
         ('tool_sha256_wrapper', 'b' * 64), ('tool_sha256_reader', 'c' * 64), ('runner_sha256', 'd' * 64), ('runner_log_sha256', 'e' * 64),
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


def meta_a1(**over):
    """시도 1 꼴 meta (한도 30000 · 시도 2 칸 없음)."""
    base = dict(attempt=1, maxiter=A1, logdir='~/p6log_a1_x', outdir='~/sdcp/ca1_probe6_a1_x_arm1', attempt1_pin=None,
                code_same_as_attempt1=None)
    base.update(over)
    return meta_text(**base)


def failed_arm(limit):
    """한도에 닿은 팔 (payload 가 .failed 로 남기는 꼴): 반복 수 = 한도 · 미수렴 표지 · 성분 상태 unconverged."""
    af = arm_doc()
    for path, val in ((S3 + 'unconverged', True), (S3 + 'cg_info', limit), (S3 + 'cg_iters', limit), (S3 + 'conv_cert.iters', limit),
                      (S3 + 'conv_cert.info', limit), (S3 + 'conv_cert.ok', False), (S3 + 'conv_cert.pass_a', False),
                      (S3 + 'conv_cert.resolve_iters', limit), (S3 + 'conv_cert.resolve_info', limit),
                      (S3 + 'manifest.components', {'electronic': {'status': 'unconverged'}})):
        dset(af, path, val)
    return af


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
        write_text(os.path.join(lg, 'samples.tsv'), samples_text(lt) if ('STEP3 solve:' in lt and 'STEP3: voxelizing' in lt) else
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
    r.paths = (out, lg, run)
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


def leaks(*texts):
    """옛 꼴의 표식 찾기 (다른 시험 · 리뷰 스크립트가 부른다): 표식 0.00713331… 의 다섯 자리가 그대로 있는 글의 번호."""
    return [i for i, t in enumerate(texts) if SENT in re.sub(r'[.,]', '', re.sub(r'\b[0-9a-f]{32,64}\b', ' ', t or ''))]


def _arm_of(r):
    rep = r.rep or {}
    a = rep.get('arm') or {}
    out, _lg, run = getattr(r, 'paths', (None, None, None))
    if not a.get('file'):
        return None
    p = os.path.join(out if rep.get('source') == 'outdir' else (run or ''), a['file'])
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def no_leak(r):
    """판독기 출력의 누출 · 꼴 문제 전부 (빈 목록 = 통과): 구조 (보고 · 화면 · 걸러 낸 로그 · 팔 값 출처) + 수 찾기 (σ 와 변형 ·
    유효숫자 3 자리 이상 · 자리 띄움 · float.hex)."""
    probs = []
    if r.rep is not None:
        probs += ['report: ' + p for p in report_problems(r.rep)]
        probs += ['screen: ' + p for p in screen_problems(r.out, r.rep)]
        probs += ['filtered: ' + p for p in filtered_problems(r.filtered, r.rep)]
        probs += ['provenance: ' + p for p in fields_provenance(r.rep, _arm_of(r))]
    elif r.report_text:
        probs.append('report is not JSON')
    safe = safe_hex(r.rep, extra=(PIN_FIX,))
    probs += ['leak: ' + h for h in scan_hits([r.out, r.err, r.report_text, r.filtered, json_strings(r.rep) if r.rep is not None else ''],
                                              T_SEALED, safe, sd_min=3, stream=True, hexsearch=True)]
    return probs


# ═════════════════════════ T: 판독기 (합성 폴더) ═════════════════════════
def suite_T(mod, rec):
    """판독기 검사: rec(name, cond, why).  주 실행 = chk · 변이 실행 = 모으개 (하나라도 실패하면 그 변이는 잡힌 것)."""
    # T00 수 찾기 · 구조 검사 자체가 판별력이 있는가 (양성 대조: σ 를 흔한 꼴로 적은 글은 잡혀야 하고, 정직한 수는 아니어야 한다)
    sg = sent(33)
    variants = ['%.17g' % sg, '%.6g' % sg, '%.4g' % sg, '%.3g' % sg, '%.4g' % (sg * 1e3), '%.3e' % sg, '%.2e' % sg,
                '%.6g' % (1.0 / sg), '%.6f' % math.log10(sg), '%.9g' % (2 * sg), '%d' % round(sg * 1e6), sg.hex(),
                ' '.join('%.6e' % sg), '%.4gS/cm' % sg, repr(round(sg, 5))]
    missed = [i for i, v in enumerate(variants)
              if not scan_hits(['x = %s' % v], T_SEALED, sd_min=3, stream=True, hexsearch=True)]
    rec('T00a 수 찾기의 양성 대조: σ 를 %d 가지 꼴 (전체 자릿수 · 유효숫자 6 · 4 · 3 · mS/cm · 지수 · 1/σ · log10 · 2σ · ×1e6 정수 · '
        'float.hex · 자리 띄움 · 단위 붙임 · round) 로 적은 글을 모두 잡는다' % len(variants), missed == [], missed)
    honest = 'cg_iters = 48211\ncert_imbalance = 5.85345e-08\nwall_s = 11900\ngpu_driver=535.183.01\nn_dof = 20885118\nrss 22444000'
    rec('T00b 수 찾기의 음성 대조: 정직한 진단 수 (반복 수 · 불균형 · 초 · 판 · dof · RSS) 는 잡지 않는다',
        scan_hits([honest], T_SEALED, sd_min=3, stream=True, hexsearch=True) == [],
        scan_hits([honest], T_SEALED, sd_min=3, stream=True, hexsearch=True))
    dump = {'schema': 'rint2-probe6-report-v2', 'zz_dump': {'sigma': sg}}
    rec('T00c 구조 검사의 양성 대조: 모르는 칸 (step3 덤프 꼴) 이 든 보고 = 문제', any('unknown top key' in p for p in report_problems(dump)),
        report_problems(dump)[:3])
    # T01 정상
    out, lg, run = make_case('t01_%d' % len(os.listdir(TD)), arm=arm_doc())
    r = run_reader(mod, out, lg, run)
    want = {'n_dof': 20885118, 'cg_iters': 48211, 'cg_info': 0, 'cg_resid': 3.3143830439317267e-13, 'unconverged': False,
            'cert_status': 'POSITIVE_SOLVED', 'cert_ok': True, 'cert_pass_a': True, 'cert_pass_b': True, 'cert_pass_c': True,
            'cert_pass_d': True, 'cert_imbalance': 5.8534485478943814e-08, 'cert_iters': 48211, 'cert_resolve_iters': 913,
            'cert_resolve_info': 0, 'cert_rtol_used': 1e-12, 'backend_used': 'gpu', 'backend_precond': 'jacobi',
            'backend_rtol': 1e-12, 'electronic_status': 'complete', 'electronic_backend_used': 'gpu'}
    got = {k: fld(r, k) for k in want}
    rec('T01a 정상 폴더 (시도 2 꼴): rc 0 · PROBE_OK · 시도 번호 2 (meta)', r.rc == 0 and (r.rep or {}).get('verdict') == 'PROBE_OK'
        and (r.rep or {}).get('attempt') == 2, (r.rc, r.out[-400:], r.err[-300:], (r.rep or {}).get('problems')))
    rec('T01b 허용 칸 값 (반복 수 · 잔차 · 판 전류 불균형 · 수렴 여부 · 백엔드 · 미지수 수)', got == want,
        {k: (got[k], want[k]) for k in want if got[k] != want[k]})
    rec('T01c 화면에 허용 칸이 보인다 (cg_iters · resolve_iters · imbalance · 시도)',
        all(s in r.out for s in ('cg_iters', '48211', 'cert_resolve_iters', '913', 'cert_imbalance', '5.85345e-08', 'attempt 2')),
        r.out[:600])
    # T02 σ 누출 없음 (구조 + 수 찾기) · 붙잡아 둔 칸
    lk = no_leak(r)
    rec('T02a σ 누출 · 꼴 문제 없음 (보고 = 닫힌 칸 · 꼴 · 팔 값 출처 / 화면 줄 = 보고 값 / 걸러 낸 로그 꼴 / σ 와 변형 수 찾기)',
        lk == [] and r.rep is not None, lk[:8])
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
        == (20885118, 3.3e-13, 9876, int(A2), 1e-12, 41, 1312, True, 'GPU'), lg_)
    rec('T03b 시간: 전체 초 · 러너 rc · CG + 증서 구간 (표본 줄 수로) · 반복당 초 (위 한계) · 결과 줄이 있으면 풀이→끝 초는 없음',
        tm.get('wall_s') == 11900 and tm.get('cg_cert_s') == 9880 and tm.get('raster_prep_s') == 1400
        and abs((tm.get('cg_cert_s_per_iter') or 0) - 9880.0 / (48211 + 913)) < 1e-12 and is_missing(tm.get('solve_to_end_s')), tm)
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
        rec('T06 칸 결손 · 꼴 (%s): rc 4 · 그 칸 = 없음 + 사유 · 누출 없음' % tag,
            rr.rc == 4 and (rr.rep or {}).get('verdict') == 'PROBE_INCOMPLETE' and no_leak(rr) == []
            and any(is_missing(v) for v in ((rr.rep or {}).get('fields') or {}).values()), (rr.rc, rr.out[-300:], no_leak(rr)[:3]))
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
                       ('cg_info = maxiter', [(S3 + 'cg_info', int(A2)), (S3 + 'conv_cert.info', int(A2)),
                                              (S3 + 'cg_iters', int(A2)), (S3 + 'conv_cert.iters', int(A2))]),
                       ('증서 ok False (ⓒ)', [(S3 + 'conv_cert.ok', False), (S3 + 'conv_cert.pass_c', False)]),
                       ('상태 NOT_CERTIFIABLE', [(S3 + 'conv_cert.status', 'NOT_CERTIFIABLE'), (S3 + 'conv_cert.ok', False)]),
                       ('미수렴 + 잔차 · 불균형 null (payload 가 비유한을 null 로)', [(S3 + 'unconverged', True), (S3 + 'cg_resid', None),
                                                                              (S3 + 'conv_cert.imbalance', None), (S3 + 'conv_cert.ok', False)])):
        a = arm_doc()
        for path, val in edits:
            dset(a, path, val)
        o, l_, k = make_case('t07_%d' % len(os.listdir(TD)), arm=a)
        rr = run_reader(mod, o, l_, k)
        rec('T07 미수렴 (%s): rc 3 · PROBE_NOT_CONVERGED · 반복 수는 그대로 보고 · 누출 없음' % tag,
            rr.rc == 3 and (rr.rep or {}).get('verdict') == 'PROBE_NOT_CONVERGED' and isinstance(fld(rr, 'cg_iters'), int)
            and no_leak(rr) == [], (rr.rc, rr.out[-300:], no_leak(rr)[:3]))
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
    # T11 봉인이 깨진 로그 (--show-results 꼴 · 결과 줄 꼴이 바뀐 것 포함)
    drift = ('  STEP3 σ_e_eff = 0.00713331912 S/cm\n', '  STEP3 σ_e_eff: 0.00713331913 S/cm  (vox 0.15µm, 20,885,118 dof, resid 3.3e-13, 9876s)\n',
             '  STEP3 collector(new format) bulk 0.00713331914 S/cm\n')
    for tag, kw, add in (('결과 줄만', dict(sealed=False, sealed_coll=True), ''), ('집전체 줄만', dict(sealed=True, sealed_coll=False), ''),
                         ('결과 줄 괄호 없음', {}, drift[0]), ('결과 줄 = 대신 :', {}, drift[1]), ('집전체 줄 새 꼴', {}, drift[2])):
        o, l_, k = make_case('t11_%d' % len(os.listdir(TD)), arm=arm_doc(), log=runner_log(**kw) + add)
        rr = run_reader(mod, o, l_, k)
        rec('T11 로그에 봉인 안 된 σ 줄 (%s): rc 5 · 그 값은 어디에도 옮기지 않는다' % tag,
            rr.rc == 5 and (rr.rep or {}).get('verdict') == 'PROBE_REJECTED' and no_leak(rr) == [], (rr.rc, no_leak(rr)[:3]))
    # T12 실패 남은 파일 (payload 가 .failed 로 남긴 진단본 · 러너 rc 1 · 시도 1 이 한도 30000 에 닿은 꼴)
    af = failed_arm(int(A1))
    o, l_, k = make_case('t12_%d' % len(os.listdir(TD)), arm=None, log=runner_log(ok=False, maxiter=int(A1)), meta=meta_a1(runner_rc=1),
                         failed={ARM + '.json.failed': af})
    rr = run_reader(mod, o, l_, k)
    rec('T12a 실패 남은 파일 (시도 1 · 한도 30000): rc 3 · 출처 = 킷 런 폴더 (.failed) · 반복 수 = maxiter · 누출 없음',
        rr.rc == 3 and (rr.rep or {}).get('source') == 'kit_run_failed' and fld(rr, 'cg_iters') == int(A1)
        and fld(rr, 'cert_resolve_iters') == int(A1) and no_leak(rr) == [], (rr.rc, (rr.rep or {}).get('source'), no_leak(rr)[:3],
                                                                            (rr.rep or {}).get('problems')))
    lg12 = (rr.rep or {}).get('log') or {}
    rec('T12b 미수렴 줄 · 증서 실패 줄 = 다시 적은 꼴 (info · 잔차 · ⓐⓑⓒⓓ · 불균형) · Δσ 값은 옮기지 않는다',
        lg12.get('not_converged_info') == int(A1) and lg12.get('not_converged_resid') == 2.3e-09
        and lg12.get('cert_fail_pass') == [False, True, False, False] and lg12.get('cert_fail_imbalance') == 1.23e-05
        and scan_hits([json.dumps(lg12, ensure_ascii=False)], T_SEALED) == [], lg12)
    masked = lg12.get('masked_lines') or []
    rec('T12c 실패 줄 = 수 하나를 # 하나로 가린 꼴로만 (SIGMA_E · CERT 줄의 값 · 지수 · 자릿수 없음)',
        any('sigma_e_eff_S_cm=-# (' in m for m in masked) and any(m.startswith('CERT|sigma|') for m in masked)
        and all(not has_digit(m) for m in masked), masked[-3:])
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
    o, _l, k = make_case('t13g_%d' % len(os.listdir(TD)), arm=a, with_logdir=False)
    rr = run_reader(mod, o, None, None)
    rec('T13g 출력 폴더만 (meta 없음 · 기대값은 영수증뿐) · 풀이 백엔드 (cpu) ≠ 영수증 기대 (gpu): rc 4',
        rr.rc == 4 and fld(rr, 'electronic_backend_used') == 'cpu', rr.rc)
    o, l_, k = make_case('t13b_%d' % len(os.listdir(TD)), arm=arm_doc(), meta=meta_text(runner_rc=1))
    rr = run_reader(mod, o, l_, k)
    rec('T13b 팔은 정상인데 러너 rc 1: rc 4 (PROBE_OK 아님)', rr.rc == 4, rr.rc)
    # T14 로그 폴더 없이 (출력 폴더만) · 로그 폴더는 있는데 파일이 빠짐
    o, _l, k = make_case('t14_%d' % len(os.listdir(TD)), arm=arm_doc(), with_logdir=False)
    rr = run_reader(mod, o, None, None)
    rec('T14a 출력 폴더만: rc 0 · 범위 = outdir_only · 시간 · 자원 = 요청 안 함',
        rr.rc == 0 and (rr.rep or {}).get('scope') == 'outdir_only' and fld(rr, 'cg_iters') == 48211 and no_leak(rr) == [],
        (rr.rc, (rr.rep or {}).get('scope'), no_leak(rr)[:3]))
    for nm in ('meta.txt', 'runner.log', 'samples.tsv'):
        o, l_, k = make_case('t14_%d' % len(os.listdir(TD)), arm=arm_doc())
        os.remove(os.path.join(l_, nm))
        rr = run_reader(mod, o, l_, k)
        rec('T14b 로그 폴더에 %s 없음: rc 4 (없음 + 사유 · 반복 수는 그대로)' % nm, rr.rc == 4 and fld(rr, 'cg_iters') == 48211, rr.rc)
    # T15 닫힌 집합: 모르는 메타 키 · 글자 값에 숨긴 수
    o, l_, k = make_case('t15_%d' % len(os.listdir(TD)), arm=arm_doc(), meta=meta_text(sneaky='0.00713331801', runner_rc='0'))
    rr = run_reader(mod, o, l_, k)
    rec('T15a 메타의 모르는 키는 옮기지 않는다 (값도 이름도)', rr.rc == 0 and no_leak(rr) == [] and 'sneaky' not in rr.report_text, no_leak(rr)[:3])
    a = arm_doc()
    dset(a, S3 + 'conv_cert.status', 'POSITIVE_0.00713331802')
    dset(a, S3 + 'manifest.backend_last_solve.precond', '0.00713331803')
    dset(a, S3 + 'manifest.physics_protocol_id', 'p3ca-0.00713331804')
    o, l_, k = make_case('t15b_%d' % len(os.listdir(TD)), arm=a)
    rr = run_reader(mod, o, l_, k)
    rec('T15b 글자 칸 = 닫힌 값 · 꼴만 (모르는 글자는 옮기지 않는다)', rr.rc in (3, 4) and no_leak(rr) == [], (rr.rc, no_leak(rr)[:3]))
    a = arm_doc()
    dset(a, S3 + 'manifest.backend_last_solve.fallback_reason', 'OutOfMemoryError: 0.00713331805 bytes')
    o, l_, k = make_case('t15c_%d' % len(os.listdir(TD)), arm=a)
    rr = run_reader(mod, o, l_, k)
    rec('T15c fallback 사유 글 = 있음 표지만', fld(rr, 'backend_fallback') is True and no_leak(rr) == [], (fld(rr, 'backend_fallback'), no_leak(rr)[:3]))
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
    # T21 신원 · 등록 값 대조는 "증거 없음" 도 막는다 (P6R-06 · 리뷰어 failopen 꼴): 로그 폴더 + S0 계획이 있으면 rc 4
    fo_cases = (
        ('팔에 input_files 없음 (침대 증거 없음)', lambda a, r_: ddel(a, S3 + 'manifest.input_files'), None, None),
        ('input_files 에 역할 하나 빠짐', lambda a, r_: a['mpm_metrics']['step3']['manifest']['input_files'].pop('fibre_dia'), None, None),
        ('code_sha null (핀 증거 없음)', lambda a, r_: dset(a, S3 + 'manifest.code_sha', None), None, None),
        ('code_sha = <sha>+dirty-unknown', lambda a, r_: dset(a, S3 + 'manifest.code_sha', 'e93efb6be+dirty-unknown'), None, None),
        ('영수증에 ca_ext_request 없음 (tol 증거 없음)', lambda a, r_: r_.pop('ca_ext_request'), None, None),
        ('영수증 cjunc 에 tol_ff_um 만 없음 (tol 증거 없음 · R_j 는 있음)', lambda a, r_: r_['ca_ext_request']['cjunc'].pop('tol_ff_um'), None, None),
        ('영수증 step3_rtol 만 1e-8 (증서 rtol 은 1e-12)', lambda a, r_: r_.__setitem__('step3_rtol', 1e-8), None, None),
        ('증서 rtol_used 만 1e-8 (영수증 rtol 은 1e-12)', lambda a, r_: dset(a, S3 + 'conv_cert.rtol_used', 1e-8), None, None),
        ('meta 에 pin 없음', None, meta_text(pin=None), None),
        ('meta maxiter 1500000 · 로그 CG maxiter 30,000 (P2_EXTRA 가 안 먹음)', None, None, runner_log(maxiter=30000)),
        ('영수증 · 증서 rtol 1e-8 (등록 1e-12 아님)', lambda a, r_: (dset(a, S3 + 'conv_cert.rtol_used', 1e-8), dset(a, S3 + 'manifest.backend_last_solve.rtol', 1e-8),
                                                         r_.__setitem__('step3_rtol', 1e-8)), None, None),
        ('meta aborted=1 · cap_term=1', None, meta_text(aborted=1, cap_term=1), None),
        ('meta git_lines_after=7 (런 뒤 작업 트리 더러움)', None, meta_text(git_lines_after=7), None),
        ('meta kit_run_matches_s0=0', None, meta_text(kit_run_matches_s0=0), None),
        ('영수증에 expect_backend 없음 · cpu 풀이 (meta 기대 = gpu)', lambda a, r_: (dset(a, S3 + 'manifest.components.electronic.backend.used', 'cpu'),
                                                                 dset(a, S3 + 'manifest.backend_last_solve.used', 'cpu'), r_.pop('expect_backend')), None, None),
        ('meta orphans=2 (러너 그룹에 남은 프로세스)', None, meta_text(orphans=2), None),
        ('meta solve_started=0 (풀이 시작 표지 없음 · 기록 모순)', None, meta_text(solve_started=0), None),
        ('meta 에 expect_rtol 없음', None, meta_text(expect_rtol=None), None),
        ('meta 에 expect_backend 없음', None, meta_text(expect_backend=None), None))
    for tag, edit, mt, lgt in fo_cases:
        a, rcp = arm_doc(), receipt_doc()
        if edit:
            edit(a, rcp)
        o, l_, k = make_case('t21_%d' % len(os.listdir(TD)), arm=a, receipt=rcp, meta=mt, log=lgt)
        rr = run_reader(mod, o, l_, k)
        rec('T21 신원 · 등록 값 증거가 없거나 다름 (%s): rc 4 (PROBE_OK 아님) · 누출 없음' % tag, rr.rc == 4 and no_leak(rr) == [],
            (rr.rc, (rr.rep or {}).get('problems'), no_leak(rr)[:3]))
    # T22 가린 줄 = 앞 30 + 뒤 30 (뒤의 진짜 사유가 잘리지 않는다 · 버린 수를 적는다)
    many = ''.join('[p2] ABORT step %d of a long failure\n' % i for i in range(80)) + '[p2] ABORT last reason line\n'
    o, l_, k = make_case('t22_%d' % len(os.listdir(TD)), arm=None, log=runner_log(ok=False) + many, meta=meta_text(runner_rc=1))
    rr = run_reader(mod, o, l_, k)
    m22 = ((rr.rep or {}).get('log') or {}).get('masked_lines') or []
    rec('T22 실패 줄이 많으면 앞 30 + 뒤 30 · 마지막 사유 줄이 남는다 · 버린 수 = 보고 · 화면',
        len(m22) == 60 and m22[-1] == '[p#] ABORT last reason line' and ((rr.rep or {}).get('log') or {}).get('masked_lines_dropped', 0) > 0
        and 'dropped from the middle' in rr.out and no_leak(rr) == [], (len(m22), m22[-1:], no_leak(rr)[:3]))
    # T23 가림 = 유니코드 숫자 · 위 / 아래 첨자 · hex float 도 (실제 러너가 그런 꼴로 찍는 자리는 못 찾았다 · 보강)
    odd = ('     ValueError: sigma ７.１３３３１ｅ－０３ (fullwidth digits)\n     ValueError: sigma 0x1.d37c2a5e0p-8 (hex float)\n'
           '     ValueError: sigma 7.13331×10⁻³ and ⁷¹³³³¹ and ₇₁₃\n')
    o, l_, k = make_case('t23_%d' % len(os.listdir(TD)), arm=None, log=runner_log(ok=False) + odd, meta=meta_text(runner_rc=1))
    rr = run_reader(mod, o, l_, k)
    m23 = ((rr.rep or {}).get('log') or {}).get('masked_lines') or []
    rec('T23 가린 줄에 어떤 숫자도 남지 않는다 (전각 · 첨자 · hex float)', len(m23) >= 3 and all(not has_digit(x) for x in m23),
        [x for x in m23 if has_digit(x)][:3])
    # T24 끝 표지 (결과 줄) 없이 멈춘 시도: 풀이 시작 줄 → 끝 시각 초를 따로 낸다 (반복 수 · 잔차는 한도 줄에서 · P6R-02)
    stopped = LOG_HEAD.format(arm=ARM, maxiter='30,000') + '  ⚠ STEP3 CG not converged (info=30000, resid=4.4e-07) — σ UNRELIABLE\n'
    o, l_, k = make_case('t24_%d' % len(os.listdir(TD)), arm=None, log=stopped, meta=meta_a1(runner_rc=143, aborted=1))
    write_text(os.path.join(l_, 'samples.tsv'), '#epoch\telapsed_s\tlog_lines\trss_sum_kb\trss_max_kb\tgpu_used_mib\tgpu_ours_mib\tgpu_util\n'
               '%d\t0\t3\t1000\t900\t1234\t0\t3\n%d\t2000\t%d\t1000\t900\t1234\t0\t3\n' % (T0, T0 + 2000, len(stopped.split('\n')) - 1))
    for d, _ds, fs in os.walk(os.path.dirname(l_)):
        for nm in fs:
            os.utime(os.path.join(d, nm), (T0 + 100, T0 + 100))
    rr = run_reader(mod, o, l_, k)
    tm24, lg24 = (rr.rep or {}).get('timing') or {}, (rr.rep or {}).get('log') or {}
    rec('T24 결과 줄 없이 멈춤: rc 4 · 풀이 시작 → 끝 초 = 끝 시각 − 풀이 시작 표본 · 한도 줄의 info · 잔차는 읽는다 · σ 없음',
        rr.rc == 4 and tm24.get('solve_to_end_s') == 11900 - 2000 and lg24.get('not_converged_info') == 30000
        and lg24.get('not_converged_resid') == 4.4e-07 and no_leak(rr) == [], (rr.rc, tm24.get('solve_to_end_s'), lg24.get('not_converged_info')))
    # T25 보고 파일을 못 쓰면: 예외 없이 rc 4 · 화면 표는 그대로 · 이유 한 줄 (P6R-12)
    o, l_, k = make_case('t25_%d' % len(os.listdir(TD)), arm=arm_doc())
    rr = run_reader(mod, o, l_, k, extra_args=('--report', os.path.join(l_, 'no_such_dir', 'x.json')))
    rec('T25 보고를 못 씀 (없는 폴더): rc 4 · traceback 없음 · 화면 표 + READER_CRASH 줄',
        rr.rc == 4 and 'READER_CRASH' in rr.out and 'verdict' in rr.out and 'Traceback' not in rr.err + rr.out
        and scan_hits([rr.out, rr.err], T_SEALED) == [], (rr.rc, rr.out[-300:], rr.err[-300:]))
    rec('T25b 정상 폴더 (T01): R_j 대조 = True (팔 이름 cj1000000 · 영수증 R_j_ohm = meta expect_rj 1e6)',
        fld(r, 'rj_matches_registered') is True, fld(r, 'rj_matches_registered'))

    def run_case(tag, arm=None, receipt=None, meta=None, log=None, arm_name=ARM, failed=None, extra=None):
        o_, l2, k2 = make_case('%s_%d' % (tag, len(os.listdir(TD))), arm=arm, receipt=receipt, meta=meta, log=log, arm_name=arm_name,
                               failed=failed, extra=extra)
        return run_reader(mod, o_, l2, k2)

    def conv_arm(iters):
        a_ = arm_doc()
        for path_, v_ in ((S3 + 'cg_iters', iters), (S3 + 'conv_cert.iters', iters)):
            dset(a_, path_, v_)
        return a_
    # T26 시도 번호 ↔ 한도 짝 (P6R2-04 · 1 → 30000 · 2 → 1500000): 어긋나면 rc 4 (PROBE_OK 경로 · 미수렴 경로 둘 다)
    for tag, kw, want_rc in (
            ('시도 2 + 한도 30000 (블록 밖에서 a2 폴더 + 30000)', dict(arm=conv_arm(21234), meta=meta_text(maxiter=A1), log=runner_log(maxiter=int(A1))), 4),
            ('시도 1 + 한도 1500000 (a1 폴더 + 본 한도)', dict(arm=arm_doc(), meta=meta_a1(maxiter=A2), log=runner_log(maxiter=int(A2))), 4),
            ('시도 1 + 한도 400000 · 미수렴 남은 파일 (rc 3 경로)', dict(meta=meta_a1(maxiter=400000, runner_rc=1),
                                                         log=runner_log(ok=False, maxiter=400000),
                                                         failed={ARM + '.json.failed': failed_arm(400000)}), 4),
            ('(대조) 시도 1 + 한도 30000 + 모인 팔 = PROBE_OK', dict(arm=conv_arm(21234), meta=meta_a1(), log=runner_log(maxiter=int(A1))), 0)):
        rr = run_case('t26', **kw)
        rec('T26 짝 (%s): rc %d · 누출 없음' % (tag, want_rc), rr.rc == want_rc and no_leak(rr) == [],
            (rr.rc, (rr.rep or {}).get('problems'), no_leak(rr)[:3]))
    # T27 시도 2 = 시도 1 과 같은 풀이 코드 (P6R2-03): meta 의 attempt1_pin · code_same_as_attempt1 이 없거나 다르면 rc 4 · 시도 1 에 그 칸이 있으면 모순 = rc 4
    for tag, kw, want_rc in (
            ('시도 2 meta 에 attempt1_pin 없음', dict(arm=arm_doc(), meta=meta_text(attempt1_pin=None)), 4),
            ('시도 2 meta 에 code_same_as_attempt1 없음', dict(arm=arm_doc(), meta=meta_text(code_same_as_attempt1=None)), 4),
            ('시도 2 meta code_same_as_attempt1=0', dict(arm=arm_doc(), meta=meta_text(code_same_as_attempt1=0)), 4),
            ('시도 1 meta 에 attempt1_pin (시도 2 칸 · 모순)', dict(arm=conv_arm(21234), meta=meta_a1(attempt1_pin=PIN_FIX),
                                                         log=runner_log(maxiter=int(A1))), 4),
            ('시도 2 미수렴 (rc 3 경로) · attempt1_pin 없음', dict(meta=meta_text(attempt1_pin=None, runner_rc=1), log=runner_log(ok=False),
                                                        failed={ARM + '.json.failed': failed_arm(int(A2))}), 4),
            ('(대조) 시도 2 미수렴 · 시도 2 칸 있음 = rc 3', dict(meta=meta_text(runner_rc=1), log=runner_log(ok=False),
                                                      failed={ARM + '.json.failed': failed_arm(int(A2))}), 3)):
        rr = run_case('t27', **kw)
        rec('T27 시도 1 과 같은 코드 칸 (%s): rc %d · 누출 없음' % (tag, want_rc), rr.rc == want_rc and no_leak(rr) == [],
            (rr.rc, (rr.rep or {}).get('problems'), no_leak(rr)[:3]))
    # T28 시도 1 의 정상 끝 (rc 3) 에도 신원 · 등록 값 · 기록 대조 (P6R2-05 · 리뷰어 a1identity 꼴): 어긋나면 rc 4
    rcp_noarms = receipt_doc()
    rcp_noarms.pop('arms')
    rcp_rj = receipt_doc()
    rcp_rj['ca_ext_request']['cjunc']['R_j_ohm'] = 100000.0
    rcp_tol = receipt_doc()
    rcp_tol['ca_ext_request']['cjunc']['tol_ff_um'] = 0.05

    def a1case(arm_edit=None, receipt=None, meta_over=None, log_maxiter=int(A1), extra=None, arm_name=ARM):
        a_ = failed_arm(int(A1))
        if arm_edit:
            arm_edit(a_)
        mo = dict(runner_rc=1)
        mo.update(meta_over or {})
        return dict(meta=meta_a1(**mo), log=runner_log(ok=False, maxiter=log_maxiter), receipt=receipt, extra=extra,
                    failed={arm_name + '.json.failed': a_})
    for tag, kw, want_rc in (
            ('(대조) 정직한 시도 1 · 한도에 닿음', a1case(), 3),
            ('다른 침대 (입력 지문 다름)', a1case(arm_edit=lambda a_: dset(a_, S3 + 'manifest.input_files.se', '0' * 16)), 4),
            ('깨끗하지 않은 코드 (+dirty)', a1case(arm_edit=lambda a_: dset(a_, S3 + 'manifest.code_sha', 'e93efb6be+dirty')), 4),
            ('다른 핀 (meta pin)', a1case(meta_over=dict(pin='a' * 40)), 4),
            ('로그 maxiter 400000 ↔ meta 30000', a1case(log_maxiter=400000), 4),
            ('meta aborted=1 · cap_term=1 · orphans=2', a1case(meta_over=dict(aborted=1, cap_term=1, orphans=2)), 4),
            ('meta git_lines_after=5 · solve_started=0', a1case(meta_over=dict(git_lines_after=5, solve_started=0)), 4),
            ('meta pythonpath_set=1', a1case(meta_over=dict(pythonpath_set=1)), 4),
            ('meta kit_run_matches_s0=0', a1case(meta_over=dict(kit_run_matches_s0=0)), 4),
            ('영수증 arms 없음', a1case(receipt=rcp_noarms), 4),
            ('영수증 R_j_ohm 1e5 (등록 1e6 아님)', a1case(receipt=rcp_rj), 4),
            ('영수증 tol_ff ≠ S0 계획', a1case(receipt=rcp_tol), 4),
            ('출력 폴더에 모르는 파일 (기록 불완전)', a1case(extra={'notes.dat': 'x'}), 4)):
        rr = run_case('t28', **kw)
        rec('T28 시도 1 의 정상 끝에도 대조 (%s): rc %d · 누출 없음' % (tag, want_rc), rr.rc == want_rc and no_leak(rr) == [],
            (rr.rc, (rr.rep or {}).get('problems'), no_leak(rr)[:3]))
    # T29 PROBE_OK 경로의 남은 셋 (P6R2-05 · 리뷰어 failopen 남은 꼴): 영수증 arms 없음 · 등록점 밖 R_j · PYTHONPATH 가 남은 러너 → rc 4
    for tag, kw in (('영수증 arms 없음', dict(arm=arm_doc(), receipt=rcp_noarms)),
                    ('등록점 밖 R_j 팔 이름 (cj100000)', dict(arm=arm_doc(), arm_name=ARM.replace('cj1000000', 'cj100000'))),
                    ('영수증 R_j_ohm 1e5', dict(arm=arm_doc(), receipt=rcp_rj)),
                    ('meta pythonpath_set=1 (러너에 PYTHONPATH 가 남음)', dict(arm=arm_doc(), meta=meta_text(pythonpath_set=1))),
                    ('meta 에 expect_rj 없음', dict(arm=arm_doc(), meta=meta_text(expect_rj=None)))):
        rr = run_case('t29', **kw)
        rec('T29 PROBE_OK 경로 (%s): rc 4 (PROBE_OK 아님) · 누출 없음' % tag, rr.rc == 4 and no_leak(rr) == [],
            (rr.rc, (rr.rep or {}).get('problems'), no_leak(rr)[:3]))
    # T30 ★ 11-13 시도 3 · 4 (원장 §3 · 탄소 접합 원장 저장본 켬): meta 저장본 칸 · audit 곁 파일 (상태 · 열쇠 · 파일 · sha) · 목록
    fsha = 'cd' * 32
    reg = 'cjreg_%s.npz' % FAKE_KEY

    def audit(status='built_written', file_sha=fsha, key=FAKE_KEY, schema='cjstore-audit-v1'):
        return json.dumps({'schema': schema, 'status': status, 'key': key, 'file': reg, 'file_sha256': file_sha, 'why': None,
                           'bytes': 14, 'seconds_read': None, 'seconds_build': 3.0, 'seconds_write': 0.1,
                           'runtime': {'python': '3.8.10', 'env': {}}}, sort_keys=True)

    def m3(**over):
        base = dict(attempt=3, attempt1_pin=None, code_same_as_attempt1=None, attempt2_pin=PIN_FIX, store='~/p6_cjstore',
                    store_listing_before='', store_listing_after='%s:%s' % (reg, fsha), logdir='~/p6log_a3_x',
                    outdir='~/sdcp/ca1_probe6_a3_x_arm1')
        base.update(over)
        return meta_text(**base)

    def m4(**over):
        base = dict(attempt=4, attempt1_pin=None, code_same_as_attempt1=None, attempt3_pin=PIN_FIX, code_same_as_attempt3=1,
                    store='~/p6_cjstore', store_listing_before='%s:%s' % (reg, fsha), store_listing_after='%s:%s' % (reg, fsha),
                    logdir='~/p6log_a4_x', outdir='~/sdcp/ca1_probe6_a4_x_arm1')
        base.update(over)
        return meta_text(**base)
    ok3 = run_case('t30', arm=arm_doc(), meta=m3(), extra={AUDIT_NAME: audit()})
    st3 = (ok3.rep or {}).get('store') or {}
    rec('T30a 시도 3 (빈 저장본 → 짓고 씀): rc 0 · PROBE_OK · 보고 store = audit 곁 파일 이름 · 상태 built_written · 열쇠 · 파일 · sha · 구조 · 화면 = 보고 · '
        '누출 없음',
        ok3.rc == 0 and st3.get('audit_file') == AUDIT_NAME and st3.get('status') == 'built_written' and st3.get('key') == FAKE_KEY
        and st3.get('file') == reg and st3.get('file_sha256') == fsha and report_problems(ok3.rep) == []
        and screen_problems(ok3.out, ok3.rep) == [] and no_leak(ok3) == [],
        (ok3.rc, (ok3.rep or {}).get('problems'), st3, report_problems(ok3.rep)[:3], screen_problems(ok3.out, ok3.rep)[:3]))
    ok4 = run_case('t30', arm=arm_doc(), meta=m4(), extra={AUDIT_NAME: audit(status='hit')})
    rec('T30b 시도 4 (시도 3 이 남긴 저장본 → 적중): rc 0 · PROBE_OK · 상태 hit · 구조 · 화면 = 보고',
        ok4.rc == 0 and ((ok4.rep or {}).get('store') or {}).get('status') == 'hit' and report_problems(ok4.rep) == []
        and screen_problems(ok4.out, ok4.rep) == [], (ok4.rc, (ok4.rep or {}).get('problems')))
    bad30 = (
        ('시도 3 인데 상태 hit (빈 저장본이 아니었다)', dict(arm=arm_doc(), meta=m3(), extra={AUDIT_NAME: audit(status='hit')})),
        ('시도 3 인데 상태 disabled (런 도중 코드 바뀜 · 저장본을 쓰지 않음)', dict(arm=arm_doc(), meta=m3(), extra={AUDIT_NAME: audit(status='disabled')})),
        ('시도 4 인데 상태 built_written (적중 아님)', dict(arm=arm_doc(), meta=m4(), extra={AUDIT_NAME: audit()})),
        ('시도 3 audit 곁 파일 없음', dict(arm=arm_doc(), meta=m3())),
        ('시도 4 audit 곁 파일 없음', dict(arm=arm_doc(), meta=m4())),
        ('시도 2 에 audit 곁 파일 (저장본은 시도 3 · 4 만)', dict(arm=arm_doc(), extra={AUDIT_NAME: audit()})),
        ('시도 2 meta 에 저장본 칸', dict(arm=arm_doc(), meta=meta_text(store='~/p6_cjstore', store_listing_before='',
                                                                    store_listing_after='%s:%s' % (reg, fsha)))),
        ('시도 1 에 audit 곁 파일', dict(arm=arm_doc(), meta=meta_a1(), log=runner_log(maxiter=int(A1)), extra={AUDIT_NAME: audit()})),
        ('audit 파일 sha ≠ 끝 목록의 sha', dict(arm=arm_doc(), meta=m3(), extra={AUDIT_NAME: audit(file_sha='ef' * 32)})),
        ('audit 파일이 끝 목록에 없음', dict(arm=arm_doc(), meta=m3(store_listing_after='cjreg_%s.npz:%s' % ('01' * 32, fsha)),
                                    extra={AUDIT_NAME: audit()})),
        ('시도 3 시작 목록이 비어 있지 않음', dict(arm=arm_doc(), meta=m3(store_listing_before='%s:%s' % (reg, fsha)), extra={AUDIT_NAME: audit()})),
        ('시도 4 목록이 런 도중 바뀜 (앞 ≠ 끝)', dict(arm=arm_doc(), meta=m4(store_listing_before='%s:%s' % (reg, 'ef' * 32)),
                                          extra={AUDIT_NAME: audit(status='hit')})),
        ('시도 4 시작 목록이 빔', dict(arm=arm_doc(), meta=m4(store_listing_before=''), extra={AUDIT_NAME: audit(status='hit')})),
        ('시도 3 meta 에 저장본 칸 없음', dict(arm=arm_doc(), meta=m3(store=None), extra={AUDIT_NAME: audit()})),
        ('시도 3 meta 에 attempt2_pin 없음', dict(arm=arm_doc(), meta=m3(attempt2_pin=None), extra={AUDIT_NAME: audit()})),
        ('시도 4 meta 에 code_same_as_attempt3 없음', dict(arm=arm_doc(), meta=m4(code_same_as_attempt3=None),
                                                       extra={AUDIT_NAME: audit(status='hit')})),
        ('시도 3 meta 에 attempt1_pin (모순)', dict(arm=arm_doc(), meta=m3(attempt1_pin=PIN_FIX), extra={AUDIT_NAME: audit()})),
        ('시도 3 meta 에 attempt3_pin (모순)', dict(arm=arm_doc(), meta=m3(attempt3_pin=PIN_FIX), extra={AUDIT_NAME: audit()})),
        ('시도 2 meta 에 attempt2_pin (모순)', dict(arm=arm_doc(), meta=meta_text(attempt2_pin=PIN_FIX))),
        ('audit 곁 파일 둘', dict(arm=arm_doc(), meta=m3(), extra={AUDIT_NAME: audit(),
                                                             AUDIT_NAME.replace('_a0.json', 'x_a0.json'): audit()})),
        ('다른 팔의 audit 곁 파일', dict(arm=arm_doc(), meta=m3(), extra={AUDIT_NAME.replace(ARM, ARM.replace('_a0', 'x_a0')): audit()})),
        ('audit 곁 파일이 JSON 아님', dict(arm=arm_doc(), meta=m3(), extra={AUDIT_NAME: 'not json'})))
    res30 = []
    for tag, kw in bad30:
        rr = run_case('t30', **kw)
        res30.append((tag, rr.rc == 4 and no_leak(rr) == [] and report_problems(rr.rep) == [], rr.rc, (rr.rep or {}).get('problems')))
    rec('T30c 저장본 기록이 등록과 다른 %d 꼴 (상태 · 곁 파일 있음 / 없음 · 시도 1 · 2 의 저장본 · 목록 sha · 시작 목록 · 목록 바뀜 · 칸 없음 · 모순 · 둘 · 다른 팔 · '
        'JSON 아님): 모두 rc 4 · 누출 없음 · 보고 구조 통과' % len(bad30),
        all(x[1] for x in res30) and len(res30) == 22, [x for x in res30 if not x[1]])


@case('T 판독기 (합성 폴더)')
def t_T():
    mod = load_reader(READER)
    suite_T(mod, chk)
    out, lg, run = make_case('t_cli', arm=arm_doc())
    p = subprocess.run([sys.executable, '-I', '-B', READER, '--outdir', out, '--logdir', lg, '--kit-run', run, '--s0-plan',
                        os.path.join(ROOT, S0PLAN_REL)], capture_output=True, text=True)
    chk('T90 명령 줄 (python3 -I -B): rc 0 · 화면에 표식 없음 · 보고 파일 생김',
        p.returncode == 0 and scan_hits([p.stdout, p.stderr], T_SEALED) == [] and os.path.exists(os.path.join(lg, 'probe6_report.json')),
        (p.returncode, p.stdout[-300:], p.stderr[-300:]))
    p = subprocess.run([sys.executable, '-I', '-B', READER], capture_output=True, text=True)
    chk('T91 인자 없음: rc 2', p.returncode == 2, p.returncode)


# ═════════════════════════ M: 변이 (판독기를 한 군데씩 망가뜨리면 T 가 잡는다) ═════════════════════════
_BSU = chr(92) + 'u2212'                                     # 판독기 원문의 글자 그대로 (역슬래시 u2212 · 판독기 정규식의 유니코드 빼기)
_A_ARM = "    f = read_table(s3, ARM_FIELDS)\n"
_A_SCR = "    L.append('[probe6] --- solver (arm JSON, closed allowlist) ---')\n"


def _note(expr):
    """리뷰어 변이 꼴 (mut_reader.py): 판독기가 σ 를 글로 바꿔 팔 칸 사이에 끼워 넣는다 (보고 JSON = 묶음으로 간다)."""
    return [(_A_ARM, _A_ARM + "    _sg = s3.get('sigma_e_eff_S_cm')\n    f['zz_note'] = (%s) if isinstance(_sg, float) else None\n" % expr)]


def _note_screen(expr):
    return _note(expr) + [(_A_SCR, _A_SCR + "    L.append('[probe6] zz_note = %s' % rep['fields'].get('zz_note'))\n")]


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
    ('숫자를 자릿수만큼 가림 (자릿수가 남는다)', [(r"\d+(?:[.,]\d+)*(?:[eE][-+" + _BSU + r"]?\d+)?", r"\d")]),
    ('봉인 검사 (결과 줄) 를 끔', [("            if not sealed_token(m.group(1)):", "            if False:")]),
    ('봉인 검사 (집전체 줄) 를 끔', [("            if SEAL_PREFIX not in line:", "            if False:")]),
    ('거부 표지를 안 봄', [("if nm.startswith('.rejected_'):", "if nm.startswith('.rejected__never'):")]),
    ('두 팔을 받음', [("if len(arms) > 1:", "if len(arms) > 99:")]),
    ('팔 번호를 안 봄', [("elif m.group(1) != '0':", "elif False:")]),
    ('영수증 팔 수를 안 봄', [("if receipt.get('receipt_arms') != 1:", "if False:")]),
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
    ('침대 대조를 안 봄', [("if f.get('bed_inputs_match_s0') is False or (idreq and f.get('bed_inputs_match_s0') is not True):", "if False:")]),
    ('tol_ff 대조를 안 봄', [("if f.get('tol_ff_matches_s0') is False or (idreq and f.get('tol_ff_matches_s0') is not True):", "if False:")]),
    ('핀 대조를 안 봄', [("if f.get('code_matches_pin') is False or (idreq and f.get('code_matches_pin') is not True):", "if False:")]),
    ('반복 수 두 자리 대조를 안 봄', [("if f.get('cg_iters') != f.get('cert_iters'):", "if False:")]),
    ('백엔드 기대 대조를 안 봄', [("if isinstance(rb, str) and eb != rb:", "if False:")]),
    # ── 이번 고침의 새 검사 (P6R-06 · 12 · 02) 가 시험에 묶였는가
    ('침대 증거 없음을 받음 (fail-open 으로 되돌림)', [("if f.get('bed_inputs_match_s0') is False or (idreq and f.get('bed_inputs_match_s0') is not True):",
                                                   "if f.get('bed_inputs_match_s0') is False:")]),
    ('tol 증거 없음을 받음', [("if f.get('tol_ff_matches_s0') is False or (idreq and f.get('tol_ff_matches_s0') is not True):",
                             "if f.get('tol_ff_matches_s0') is False:")]),
    ('핀 증거 없음을 받음', [("if f.get('code_matches_pin') is False or (idreq and f.get('code_matches_pin') is not True):",
                            "if f.get('code_matches_pin') is False:")]),
    ('maxiter 대조를 안 봄', [("if not isinstance(m_.get('maxiter'), int) or log.get('cg_maxiter') != m_.get('maxiter'):", "if False:")]),
    ('rtol 대조를 안 봄 (영수증)', [("if xr is None or receipt.get('receipt_step3_rtol') != xr:", "if False:")]),
    ('rtol 대조를 안 봄 (증서)', [("if (rc == RC_OK and cr != xr) or (isinstance(cr, float) and cr != xr):", "if False:")]),
    ('meta 기대 백엔드를 안 봄', [("if not isinstance(xb, str) or rb != xb or (rc == RC_OK and (eb != xb or bu != xb)) or (isinstance(bu, str) and bu != xb):",
                                  "if False:")]),
    ('meta 깨끗함 (aborted · orphans · git …) 을 안 봄', [("                    if m_.get(key) != want:", "                    if False:")]),
    ('null 이면 미완 (미수렴 순서를 되돌림)', [("        elif miss and said_unconverged:", "        elif False:")]),
    ('가린 줄 뒤쪽을 버림 (앞 60 줄만)', [("                tail = (tail + [ml])[-MASK_KEEP:]", "                pass")]),
    ('결과 줄 꼴이 바뀌면 봉인 깨짐을 못 봄', [("        if (RESULT_WORD in line or 'STEP3 collector' in line) and 'S/cm' in line and SEAL_PREFIX not in line:",
                                              "        if False:")]),
    ('보고를 못 쓰면 예외 (rc 1)', [("    except (OSError, ValueError) as e:", "    except ZeroDivisionError as e:")]),
    ('유니코드 숫자를 안 가림', [(r"|\d+(?:[.,]\d+)*(?:[eE][-+" + _BSU + r"]?\d+)?|", r"|[0-9]+(?:[.,][0-9]+)*(?:[eE][-+]?[0-9]+)?|")]),
    ('풀이 시작 → 끝 초를 안 냄', [("            timing['solve_to_end_s'] = end - tmark['solve']", "            timing['solve_to_end_s'] = missing('absent')")]),
    # ── 2 회차 고침의 새 검사 (P6R2-03 · 04 · 05) 가 시험에 묶였는가
    ('짝 (시도 ↔ 한도) 을 안 봄', [("if att not in ATTEMPT_MAXITER or m_.get('maxiter') != ATTEMPT_MAXITER[att]:", "if False:")]),
    ('시도 2 의 attempt1 칸을 안 봄', [("if att == 2 and not (isinstance(m_.get('attempt1_pin'), str) and m_.get('code_same_as_attempt1') == 1):", "if False:")]),
    ('시도 1 의 시도 2 칸 모순을 안 봄', [("if att == 1 and ('attempt1_pin' in m_ or 'code_same_as_attempt1' in m_):", "if False:")]),
    ('rc 3 경로의 대조를 끔 (rc 0 만)', [("        if rc in (RC_OK, RC_NOT_CONVERGED):\n            # identity", "        if rc == RC_OK:\n            # identity")]),
    ('rc 3 에서 기록 문제를 무시 (rc 0 만 4 로)', [("        if incomplete and rc in (RC_OK, RC_NOT_CONVERGED):", "        if incomplete and rc == RC_OK:")]),
    ('R_j 대조를 안 봄', [("if args.logdir and arm_path is not None and f.get('rj_matches_registered') is not True:", "if False:")]),
    # ── 11-13 시도 3 · 4 (저장본) 의 새 검사가 시험에 묶였는가
    ('시도 3 · 4 저장본 상태를 안 봄', [("                    elif store.get('status') != want:", "                    elif False:")]),
    ('저장본 파일 sha 대조를 안 봄', [("                    elif not (isinstance(store.get('file'), str) and after.get(store['file']) == store.get('file_sha256')):",
                                     "                    elif False:")]),
    ('시도 3 빈 저장본 시작을 안 봄', [("                    elif att == 3 and lb != '':", "                    elif False:")]),
    ('시도 4 목록 바뀜을 안 봄', [("                    elif att == 4 and not (lb and lb == la):", "                    elif False:")]),
    ('시도 1 · 2 의 저장본 기록을 안 봄', [("                    if sk or not is_missing(store.get('audit_file')):", "                    if False:")]),
    ('시도 3 · 4 저장본 칸 없음을 받음', [("                    if len(sk) != 3:", "                    if False:")]),
    ('시도 3 의 attempt2 칸을 안 봄', [("                if att == 3 and not isinstance(m_.get('attempt2_pin'), str):", "                if False:")]),
    ('시도 4 의 attempt3 칸을 안 봄', [("                if att == 4 and not (isinstance(m_.get('attempt3_pin'), str) and m_.get('code_same_as_attempt3') == 1):",
                                      "                if False:")]),
    ('다른 시도의 핀 칸 모순을 안 봄', [("                if att != 3 and 'attempt2_pin' in m_ or att != 4 and ('attempt3_pin' in m_ or 'code_same_as_attempt3' in m_):",
                                       "                if False:")]),
    ('시도 3 · 4 의 시도 2 칸 모순을 안 봄', [("                if att in (3, 4) and ('attempt1_pin' in m_ or 'code_same_as_attempt1' in m_):", "                if False:")]),
    ('audit 곁 파일 둘을 받음', [("    if len(audits) > 1:", "    if len(audits) > 99:")]),
    ('다른 팔의 audit 곁 파일을 받음', [("            if arm_path is not None and audits[0] != AUDIT_PREFIX + os.path.basename(arm_path):", "            if False:")]),
    ('JSON 아닌 audit 곁 파일을 받음', [("            incomplete = True\n            probs.append('store audit side file ' + (why or 'is not an object'))",
                                       "            probs.append('store audit side file ' + (why or 'is not an object'))")]),
    ('R_j 팔 이름을 안 봄', [("(float(rj) == xj) and ('_cj%d_' % int(xj)) in os.path.basename(arm_path)", "(float(rj) == xj)")]),
    ('pythonpath_set 을 안 봄', [("('kit_run_matches_s0', 1), ('solve_started', 1), ('pythonpath_set', 0)):", "('kit_run_matches_s0', 1), ('solve_started', 1)):")]),
    ('영수증 arms 없음을 받음', [("if receipt.get('receipt_arms') != 1:", "if receipt.get('receipt_arms') not in (1,) and not is_missing(receipt.get('receipt_arms')):")]),
    # ── 리뷰어 변이 33 (mut_reader.py · 11-10): 같은 꼴 · 같은 자리
    ('리뷰 R01 보고: σ %.17g', _note("'%.17g' % _sg")), ('리뷰 R02 보고: σ %.6g', _note("'%.6g' % _sg")),
    ('리뷰 R03 보고: σ %.5g', _note("'%.5g' % _sg")), ('리뷰 R04 보고: σ %.4g', _note("'%.4g' % _sg")),
    ('리뷰 R05 보고: σ %.3g', _note("'%.3g' % _sg")), ('리뷰 R06 보고: mS/cm %.6g', _note("'%.6g' % (_sg * 1000.0)")),
    ('리뷰 R07 보고: mS/cm %.4g', _note("'%.4g' % (_sg * 1000.0)")), ('리뷰 R08 보고: mS/cm %.3g', _note("'%.3g' % (_sg * 1000.0)")),
    ('리뷰 R09 보고: 지수 %.5e', _note("'%.5e' % _sg")), ('리뷰 R10 보고: 지수 %.3e', _note("'%.3e' % _sg")),
    ('리뷰 R11 보고: 지수 %.2e', _note("'%.2e' % _sg")), ('리뷰 R12 보고: 1/σ %.6g', _note("'%.6g' % (1.0 / _sg)")),
    ('리뷰 R13 보고: log10 σ %.6f', _note("'%.6f' % math.log10(_sg)")), ('리뷰 R14 보고: 2σ %.9g', _note("'%.9g' % (2.0 * _sg)")),
    ('리뷰 R15 보고: round(σ·1e6) 정수', _note("'%d' % round(_sg * 1e6)")), ('리뷰 R16 보고: 자리 띄움', _note("' '.join('%.6e' % _sg)")),
    ('리뷰 R17 보고: float.hex', _note("_sg.hex()")),
    ('리뷰 S01 화면+보고: σ %.6g', _note_screen("'%.6g' % _sg")), ('리뷰 S02 화면+보고: σ %.4g', _note_screen("'%.4g' % _sg")),
    ('리뷰 S03 화면+보고: σ %.3g', _note_screen("'%.3g' % _sg")), ('리뷰 S04 화면+보고: mS/cm %.4g', _note_screen("'%.4g' % (_sg * 1000.0)")),
    ('리뷰 S05 화면+보고: 지수 %.3e', _note_screen("'%.3e' % _sg")),
    ('리뷰 N01 수: σ 그대로', [(_A_ARM, _A_ARM + "    f['zz'] = s3.get('sigma_e_eff_S_cm')\n")]),
    ('리뷰 N02 수: round(σ, 6)', [(_A_ARM, _A_ARM + "    f['zz'] = round(s3.get('sigma_e_eff_S_cm') or 0.0, 6)\n")]),
    ('리뷰 N03 수: round(σ, 5)', [(_A_ARM, _A_ARM + "    f['zz'] = round(s3.get('sigma_e_eff_S_cm') or 0.0, 5)\n")]),
    ('리뷰 N04 수: 증서 I_bot 유효숫자 4', [(_A_ARM, _A_ARM + "    f['zz'] = float('%.4g' % ((s3.get('conv_cert') or {}).get('I_bot') or 0.0))\n")]),
    ('리뷰 N05 수: I_top / I_bot', [(_A_ARM, _A_ARM + "    _c = s3.get('conv_cert') or {}\n    f['zz'] = (_c.get('I_top') or 0.0) / (_c.get('I_bot') or 1.0)\n")]),
    ('리뷰 K01 가림이 앞 세 자리를 남김', [("    return _MASK_RE.sub('#', line)", "    return _MASK_RE.sub(lambda m: m.group(0)[:5], line)")]),
    ('리뷰 K02 가림이 지수만 남김', [("    return _MASK_RE.sub('#', line)",
                                   "    return _MASK_RE.sub(lambda m: '#' + (m.group(0)[m.group(0).lower().find('e'):] if 'e' in m.group(0).lower() else ''), line)")]),
    ('리뷰 K03 가림이 정수부를 남김', [("    return _MASK_RE.sub('#', line)", "    return _MASK_RE.sub(lambda m: m.group(0).split('.')[0] + '#', line)")]),
    ('리뷰 L01 증서 실패 줄 원문을 옮김', [("            flt.append('cert_fail status=%s pass_abcd=%s imbalance=%r'",
                                         "            flt.append(line)\n            flt.append('cert_fail status=%s pass_abcd=%s imbalance=%r'")]),
    ('리뷰 L02 봉인 안 된 결과 줄의 값을 옮김', [("                flt.append('step3_done SEAL_BROKEN (value not copied)')",
                                              "                flt.append('step3_done SEAL_BROKEN ' + m.group(1))")]),
    ('리뷰 L03 봉인 안 된 집전체 줄을 옮김', [("                flt.append('collector_line SEAL_BROKEN (value not copied)')",
                                            "                flt.append('collector_line SEAL_BROKEN ' + line)")]),
)


@case('M 변이 (판독기)')
def t_M():
    src = read_text(READER)

    def stop_at_first(n, c, w=''):
        if not c:
            raise _Caught(n)
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
        caught = ''
        try:
            mod = load_reader(mp)
            suite_T(mod, stop_at_first)
        except _Caught as e:
            caught = str(e).split(' ')[0]
        except Exception as e:                                 # noqa: BLE001 · 변이가 판독기를 깨뜨리면 그것도 잡힌 것
            caught = 'EXC %s' % type(e).__name__
        chk('M 변이 [%s]: T 묶음이 잡는다 (%s)' % (name, caught or '-'), caught != '', '잡지 못함')


# ═════════════════════════ S: 정적 ═════════════════════════
def fenced_blocks(md_text, lang='bash'):
    return re.findall(r'^```%s\n(.*?)^```\s*$' % lang, md_text, re.S | re.M)


def wrapper_axes_ordered():
    """감시 셸의 AXES 배열: (이름, 값) 차례대로 ($TOL_FF · $KIT 은 감시 셸의 값으로)."""
    src = read_text(WRAPPER)
    m = re.search(r'^AXES=\(\n(.*?)^\)\n', src, re.S | re.M)
    toks = re.findall(r'"?([A-Z0-9_]+)=([^"\s]*)"?', m.group(1)) if m else []
    tol = re.search(r'^TOL_FF=(\S+)$', src, re.M)
    kit = re.search(r'^KIT=(\S+)$', src, re.M)
    return [(k, v.replace('$TOL_FF', tol.group(1) if tol else '?').replace('$KIT', kit.group(1) if kit else '?')) for k, v in toks]


def wrapper_axes():
    return dict(wrapper_axes_ordered())


def runner_cmd_line(maxiter, outdir='<O>', w='<W>'):
    """감시 셸이 내는 러너 명령의 글 (command.txt 의 둘째 줄 꼴 · 시험의 독립 구성: BASH_ENV · SHELLOPTS 를 뺀 env (P6R2-06) + 등록 축 차례 +
    P2_EXTRA + OUTDIR + PYTHONUNBUFFERED)."""
    axes = ' '.join('%s=%s' % (k, v) for k, v in wrapper_axes_ordered())
    return 'env -u BASH_ENV -u SHELLOPTS %s P2_EXTRA="--step3-maxiter %s" OUTDIR=%s PYTHONUNBUFFERED=1 bash %s/%s' % (
        axes, maxiter, outdir, w, RUNNER_REL)


def runner_cmd_line_store(maxiter, outdir='<O>', w='<W>', store='~/p6_cjstore'):
    """★ 11-13 시도 3 · 4 의 러너 명령 글 = 시도 1 · 2 꼴 + P2_EXTRA 뒤 CJUNC_STORE (홈을 ~ 로 접은 꼴 · command.txt 와 같은 꼴)."""
    axes = ' '.join('%s=%s' % (k, v) for k, v in wrapper_axes_ordered())
    return 'env -u BASH_ENV -u SHELLOPTS %s P2_EXTRA="--step3-maxiter %s" CJUNC_STORE=%s OUTDIR=%s PYTHONUNBUFFERED=1 bash %s/%s' % (
        axes, maxiter, store, outdir, w, RUNNER_REL)


def watcher_cmd_line(maxiter):
    return 'bash <W>/%s/run_probe6.sh <W> <O> <L> <PIN> %s' % (TOOLS_REL, maxiter)


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


def block_attempt_table(blk):
    return dict((int(a), b) for a, b in re.findall(r'^  ([12])\) MAXITER=([0-9]+);;$', blk, re.M))


def ledger_cmd_lines(text):
    """원장 줄 초안 · 원장 파일의 명령 줄 (네 칸 들여 쓴 `bash <W>/…` · `env …` 줄)."""
    return [ln[4:] for ln in text.split('\n') if ln.startswith('    bash <W>/') or ln.startswith('    env ')]


def ledger_section3(text):
    i = text.find('## 3.')
    j = text.find('## 4.', i + 1)
    return text[i:j] if i >= 0 and j > i else ''


@case('S 정적')
def t_S():
    import fnmatch
    rsrc = open(READER, 'rb').read()
    chk('S01a 판독기 = ASCII 만', all(b < 128 for b in rsrc), '')
    try:
        tree = ast.parse(rsrc.decode('ascii'), feature_version=(3, 8))
        ok38 = True
    except (SyntaxError, UnicodeDecodeError) as e:
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
    wtxt = read_text(WRAPPER)
    cmdl = re.search(r'^CMD=\((.*)\)$', wtxt, re.M)
    chk('S03f 감시 셸이 러너에 주는 env = 등록 축 + P2_EXTRA + OUTDIR + PYTHONUNBUFFERED=1 (SIGMA_VGCF_OVERRIDE · --show-results 없음)',
        'SIGMA_VGCF_OVERRIDE' not in wa and cmdl is not None
        and cmdl.group(1) == '"${AXES[@]}" "P2_EXTRA=--step3-maxiter $MAXITER" "OUTDIR=$O" PYTHONUNBUFFERED=1', cmdl and cmdl.group(1))
    launch = [ln for ln in wtxt.split('\n') if ln.startswith('setsid ') and '$RUNNER' in ln]
    gates = [ln for ln in wtxt.split('\n') if 'PYTHONUTF8=1 python3 "$W/scripts/check_' in ln]
    chk('S03h 러너 · 미리 돌리는 런 전 관문 = env -u BASH_ENV -u SHELLOPTS (RENV) + CMD · 감시 셸 머리에 set +m (작업 제어 끔 · P6R2-06)',
        re.search(r'^RENV=\(env -u BASH_ENV -u SHELLOPTS\)$', wtxt, re.M) is not None and len(launch) == 1
        and '"${RENV[@]}" "${CMD[@]}" bash "$RUNNER"' in launch[0] and len(gates) == 2
        and all(g.startswith('"${RENV[@]}" "${CMD[@]}" PYTHONUTF8=1 python3') for g in gates)
        and re.search(r'^set -u\numask 022\nset \+m', wtxt, re.M) is not None, (launch, gates))
    code_w = re.search(r'^CODE_PATHS=\((.*)\)$', wtxt, re.M)
    chk('S03i 감시 셸의 풀이 코드 목록 (CODE_PATHS) = 시험의 독립 표 (P6R2-03)', code_w is not None and tuple(code_w.group(1).split()) == SOLVE_CODE,
        code_w and code_w.group(1))
    psha = sha256_file(os.path.join(ROOT, S0PLAN_REL))
    chk('S03g 원장 줄 초안이 적은 S0 계획 sha256 (앞 8 · 뒤 6 자리) = 리포의 계획 파일 · 감시 셸의 계획 경로 = 시험 상수',
        ('%s…%s' % (psha[:8], psha[-6:])) in read_text(LEDGER_MD) and ('S0PLAN_REL=%s\n' % S0PLAN_REL) in read_text(WRAPPER), psha)
    # 블록
    bmd = read_text(BLOCK_MD)
    blocks = fenced_blocks(bmd)
    chk('S04a KGY_BLOCK.md = bash 블록 하나', len(blocks) == 1, len(blocks))
    blk = blocks[0] if blocks else ''
    chk('S04b 블록 = ASCII 만 · 느낌표 없음 · TAB 없음 · heredoc 구분자 따옴표', all(ord(c) < 128 for c in blk) and '!' not in blk
        and '\t' not in blk and blk.startswith("bash <<'P6'\n") and blk.rstrip('\n').endswith('\nP6'), [c for c in blk if ord(c) >= 128][:5])
    chk('S04c 블록의 핀 자리 = <PIN> 한 번 · BASE 줄 · 가지 = claude/stoic-knuth-NObVQ · 감시 셸 경로 = 핀 작업 트리 안',
        blk.count('<PIN>') == 1 and 'BASE="$HOME/dem-mt"\n' in blk and 'claude/stoic-knuth-NObVQ' in blk and TOOLS_REL in blk, blk.count('<PIN>'))
    p = subprocess.run(['bash', '-n'], input=blk.replace('<PIN>', 'a' * 40), capture_output=True, text=True)
    chk('S04d 블록 bash -n', p.returncode == 0, p.stderr[:300])
    tab = block_attempt_table(blk)
    lmd = read_text(LEDGER_MD)
    lcmd = ledger_cmd_lines(lmd)
    chk('S04e 블록: ATTEMPT=1 줄 하나 · 시도 표 (1 → 30000 · 2 → 1500000) = 1저자 11-10 결정 · 원장 줄 초안의 두 시도 명령 줄과 같은 값',
        len(re.findall(r'^ATTEMPT=1$', blk, re.M)) == 1 and tab == dict((k, v) for k, v in ATTEMPT_MAXITER.items())
        and all(watcher_cmd_line(v) in lcmd and runner_cmd_line(v) in lcmd for v in ATTEMPT_MAXITER.values()), (tab, lcmd))
    chk('S04f 블록이 감시 셸을 띄우는 줄 = 인자 꼴 <W> <O> <L> <PIN> <MAXITER> · 출력 · 로그 폴더 이름에 시도 번호',
        'setsid nohup bash "$T/run_probe6.sh" "$W" "$O" "$L" "$PIN" "$MAXITER" > "$L/nohup.out" 2>&1 < /dev/null &' in blk
        and 'O="$HOME/sdcp/ca1_probe6_a${ATTEMPT}_${STAMP}_arm1"' in blk and 'L="$HOME/p6log_a${ATTEMPT}_${STAMP}"' in blk, '')
    code_b = re.search(r'^CODE="([^"]*)"$', blk, re.M)
    chk('S04g 블록의 풀이 코드 목록 (CODE) = 시험의 독립 표 = 감시 셸 목록 (P6R2-03) · 블록이 git diff --quiet 로 그 목록만 본다',
        code_b is not None and tuple(code_b.group(1).split()) == SOLVE_CODE and 'diff --quiet "$P1" "$PIN" -- $CODE' in blk,
        code_b and code_b.group(1))
    ig = blk.find('case "$M" in *STOP:*) exit 2;; esac')
    chk('S04h 블록은 STOP 줄을 찍은 뒤 진행 · 멈춤 · "DONE appears" 안내를 찍지 않는다 (STOP 판정이 안내 줄보다 앞 · P6R2-07)',
        ig >= 0 and blk.find('[p6] when done:') > ig and blk.find('[p6] progress:') > ig, ig)
    # 원장 줄 초안
    chk('S05a 원장 줄 초안의 명령 줄 넷 = 감시 셸 두 줄 (30000 · 1500000) + 러너 두 줄 (등록 축 차례 + P2_EXTRA + OUTDIR + PYTHONUNBUFFERED=1)',
        sorted(lcmd) == sorted([watcher_cmd_line(v) for v in ATTEMPT_MAXITER.values()] + [runner_cmd_line(v) for v in ATTEMPT_MAXITER.values()]),
        lcmd)
    led = {}
    for ln in lcmd:
        if ln.startswith('env '):
            for m in re.finditer(r'([A-Z][A-Z0-9_]*)=("[^"]*"|\S+)', ln):
                led[m.group(1)] = m.group(2).strip('"') if m.group(1) != 'P2_EXTRA' else 'x'
    chk('S05b 원장 줄 초안 러너 줄의 env 이름 = 등록 축 + P2_EXTRA + OUTDIR + PYTHONUNBUFFERED · 값 = 등록 축',
        set(led) == set(AXES) | {'P2_EXTRA', 'OUTDIR', 'PYTHONUNBUFFERED'} and all(led[k] == v for k, v in AXES.items()), sorted(set(led) ^ (set(AXES) | {'P2_EXTRA', 'OUTDIR', 'PYTHONUNBUFFERED'})))
    chk('S05c 원장 줄 초안: 줄 둘 (번호 1 · 2) · 핀 <PIN> · 기계 kgy · 결과 칸 빈칸',
        len(re.findall(r'^\| 1 \|', lmd, re.M)) == 1 and len(re.findall(r'^\| 2 \|', lmd, re.M)) == 1 and '<PIN>' in lmd and 'kgy' in lmd, '')
    # 허용 표에 σ 류 이름 없음
    mod = load_reader(READER)
    bad_hint = ('sigma', 'I_bot', 'I_top', 'target_lo', 'target_hi', 'target_U', 'target_W', 'flow', 'scale', 'share', 'R_bulk',
                'dsigma', 'err_bound', 'width_rel', 'current', 'P_total', 'P_sum')
    paths = ['.'.join(row[1]) for row in mod['ARM_FIELDS']]
    chk('S06a 허용 표 (ARM_FIELDS) 의 경로에 σ 류 이름 없음', not [p_ for p_ in paths if any(h in p_ for h in bad_hint)],
        [p_ for p_ in paths if any(h in p_ for h in bad_hint)])
    chk('S06b 붙잡아 둔 칸은 허용 표에 없다 · 시험의 칸 표 (FIELD_SCHEMA) = 판독기 허용 표의 이름 + 대조 칸',
        not (set(mod['HELD_BACK']) & set('conv_cert.' + p_.split('.')[-1] for p_ in paths if p_.startswith('conv_cert')))
        and set(row[0] for row in mod['ARM_FIELDS']) <= set(FIELD_SCHEMA), sorted(set(row[0] for row in mod['ARM_FIELDS']) - set(FIELD_SCHEMA)))
    # 주소 · 모델 이름 없음 · 게이트 단계
    allsrc = ''
    for pth in (READER, WRAPPER, BLOCK_MD, LEDGER_MD, README_MD):
        allsrc += read_text(pth) if os.path.exists(pth) else ''
    chk('S07a 준비물에 IPv4 꼴 · ssh · scp 명령 · 포트 없음',
        not re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', allsrc) and not re.search(r'\b(ssh|scp|sftp)\s+-', allsrc)
        and not re.search(r'\bport\s*[0-9]{2,5}\b', allsrc, re.I), '')
    chk('S07b 준비물에 모델 식별자 없음 (리포 규칙 · `wiki/tools/lint.py` 의 MODEL_ID 와 같은 꼴 + 계열 이름 낱말)',
        not re.search(r'claude-(?:opus|sonnet|haiku|fable)[a-z0-9.\-]*|\b(?:opus|sonnet|haiku|fable)\b', allsrc, re.I), '')
    newtext = read_text(BLOCK_MD) + read_text(LEDGER_MD) + read_text(README_MD) + read_text(READER) + read_text(WRAPPER)
    chk('S07c 준비 폴더 글에 em dash (U+2014) 없음 (지시서 · 새 글)', chr(0x2014) not in newtext, newtext.count(chr(0x2014)))
    ca = read_text(os.path.join(SCRIPTS, 'check_all.sh'))
    chk('S08 게이트 단계 한 줄 (check_all.sh)', len(re.findall(r"^run '[^']*probe6[^']*' python3 %s/test_probe6_read\.py\s*$" % re.escape(TOOLS_REL), ca, re.M)) == 1, '')
    chk('S09 README · 블록 · 원장 줄 초안이 있다', all(os.path.exists(p_) for p_ in (README_MD, BLOCK_MD, LEDGER_MD)), '')
    # S10 걷어내기 목록 ↔ 러너가 env 에서 읽는 이름 (리뷰어 변이: 목록에서 하나를 빼도 시험이 몰랐다 · P6R-10)
    wsrc_t = read_text(WRAPPER)
    m = re.search(r'^\s+(SIGMA_\*\|[^\n]*\))$', wsrc_t, re.M)
    pats = m.group(1).rstrip(')').split('|') if m else []
    rnames = set(re.findall(r'\$\{([A-Z][A-Z0-9_]*)(?::|[-+])', read_text(os.path.join(ROOT, RUNNER_REL))))
    left = sorted(n for n in rnames if not any(fnmatch.fnmatchcase(n, p_) for p_ in pats))
    chk('S10 러너가 env 에서 읽는 이름 (${NAME:- · ${NAME- · ${NAME+) 은 전부 감시 셸의 걷어내기 목록에 걸린다 (밖 = VIRTUAL_ENV 하나 · venv 가 정한다)',
        bool(pats) and left == ['VIRTUAL_ENV'], left)
    # S11 원장 파일 §3 = 두 시도의 줄 · 명령 줄 넷 (본 세션이 원장을 고친 뒤에 통과한다 · --ledger 로 제안 글을 미리 본다)
    lf = ARGS.ledger if (ARGS is not None and ARGS.ledger) else LEDGER_FILE
    sec3 = ledger_section3(read_text(lf)) if os.path.exists(lf) else ''
    s3lines = set(ln[4:] for ln in sec3.split('\n') if ln.startswith('    '))
    need = [watcher_cmd_line(v) for v in ATTEMPT_MAXITER.values()] + [runner_cmd_line(v) for v in ATTEMPT_MAXITER.values()]
    chk('S11 원장 §3 (%s) 에 시도 줄 둘 (| 1 | · | 2 |) · 명령 줄 넷 (감시 셸 30000 · 1500000 · 러너 PYTHONUNBUFFERED=1 포함) 이 네 칸 들여 쓴 줄로 있다'
        % os.path.relpath(lf, ROOT),
        bool(re.search(r'^\| 1 \|', sec3, re.M)) and bool(re.search(r'^\| 2 \|', sec3, re.M)) and all(x in s3lines for x in need),
        [x[:60] for x in need if x not in s3lines])
    kg = read_text(os.path.join(SCRIPTS, 'check_kgy_py38.sh'))
    runs = re.findall(r'^run \S+ .*$', kg, re.M)
    cnt = re.search(r'kgy 판 R 경로 시험 ([0-9]+) 묶음 통과', kg)
    chk('S12 kgy 판 게이트 (check_kgy_py38.sh) 에 이 시험 한 줄 · 끝 문구의 묶음 수 = run 줄 수',
        len([r_ for r_ in runs if (TOOLS_REL + '/test_probe6_read.py') in r_]) == 1 and cnt is not None and int(cnt.group(1)) == len(runs),
        (len(runs), cnt and cnt.group(1)))
    rd = read_text(README_MD)
    i4, i5 = rd.find('## 4.'), rd.find('## 5.')
    s4 = rd[i4:i5] if 0 <= i4 < i5 else ''
    newnums = ('not_converged_info', 'not_converged_resid', 'solve_to_end_s', 'masked_lines_dropped', 'gpu_used_start_mib',
               'disk_free_gb_kit', 'orphans', 'env_', 'attempt1_pin', 'code_same_as_attempt1', 'expect_rj', 'pythonpath_removed',
               'rj_matches_registered', 'attempt2_pin', 'attempt3_pin', 'code_same_as_attempt3', 'store_listing_before',
               'store_listing_after', 'audit_sha256')
    chk('S13 README §4 에 새로 내는 수마다 "σ 를 되짚을 수 없다" 까닭 줄 (이름이 §4 에 있다)', all(n in s4 for n in newnums),
        [n for n in newnums if n not in s4])
    # S14 문서 (P6R2-01 · 03 · 07 · 08): 시도 2 = 풀이를 시작한 시도 1 (solve_started=1) 의 DONE 뒤 (원장 §3 2 번 줄 · 블록 머리 · README §3) ·
    #     README §9 의 정한 것 = 정함 (11-10) · 풀이 코드 목록 (README §9 · 원장 §3) · 블록 "중간에 멈추려면" 의 런 전 관문 줄 · README §7 한계 · 시험 수
    ledt = read_text(lf) if os.path.exists(lf) else ''
    l3 = ledger_section3(ledt)
    row2 = [ln for ln in l3.split('\n') if ln.startswith('| 2 |')]
    bhead = bmd[:bmd.find('```')]
    i3, i4b = rd.find('## 3.'), rd.find('## 4.')
    r3 = [ln for ln in rd[i3:i4b].split('\n') if ln.startswith('| 시도')]
    i7, i8, i9 = rd.find('## 7.'), rd.find('## 8.'), rd.find('## 9.')
    s7, s9 = rd[i7:i8], rd[i9:]
    stopsec = bmd[bmd.find('## 중간에 멈추려면'):]
    probs14 = [n for n, c in (
        ('원장 §3 2 번 줄 solve_started=1', len(row2) == 1 and 'solve_started=1' in row2[0]),
        ('블록 머리 solve_started=1', 'solve_started=1' in bhead),
        ('README §3 시도 칸 solve_started=1', len(r3) == 1 and 'solve_started=1' in r3[0]),
        ('README §9 정함 (11-10)', '정함 (11-10)' in s9 and '본 세션이 정할 것:' not in s9),
        ('README §9 · 원장 §3 풀이 코드 목록', all(('`%s`' % p_) in s9 and ('`%s`' % p_) in l3 for p_ in SOLVE_CODE)),
        ('원장 §3 code_same_as_attempt1 · 끝난 시도 번호 규칙', '`code_same_as_attempt1=1`' in l3 and 'WATCHER_FAILED' in l3
         and '끝난 시도 번호' in l3),
        ('원장 §3 검토 글 2 회차', '2 회차' in l3 and 'P6R2-01–08' in l3),
        ('블록 "중간에 멈추려면" 의 런 전 관문 줄', '런 전 관문' in stopsec and '관문이 끝난 뒤' in stopsec),
        ('README §7 한계 (P6R2-08)', '0.37σ' in s7 and '일부러 계산' in s7),
        ('README §7 옛 시험 수 (269 PASS · 1 FAIL) 없음', '269 PASS · 1 FAIL' not in s7),
        ('README §9 의 명령 줄 넷 = 원장 §3 글자 그대로', all(x in set(ln[4:] for ln in s9.split('\n') if ln.startswith('    ')) for x in need))) if not c]
    chk('S14 문서 (시도 2 앞 조건 solve_started=1 세 곳 · README §9 정함 · 풀이 코드 목록 · 블록 멈춤 안내 · README §7 한계 · 시험 수)', probs14 == [],
        probs14)
    # S16 ★ 11-13 시도 3 · 4 (원장 §3 · 저장본) 와 감시 셸 git 읽기 격리
    wt16 = read_text(WRAPPER)
    rc_ = _rc()
    st_line = [ln for ln in wt16.split('\n') if ln.startswith('if [ -n "$STORE" ]; then CMD=(')]
    cs16 = [ln for ln in wt16.split('\n') if ln.strip().startswith('CJUNC_STORE=*)')]
    chk('S16a 감시 셸: 시도 3 · 4 의 러너 env = 시도 1 · 2 꼴 + P2_EXTRA 뒤 CJUNC_STORE · command.txt 는 CJUNC_STORE 를 홈 ~ 로 접는다 · 짝 표 3 · 4 = 1500000 · '
        '저장본 = ~/p6_cjstore 고정',
        len(st_line) == 1 and '"${AXES[@]}" "P2_EXTRA=--step3-maxiter $MAXITER" "CJUNC_STORE=$STORE" "OUTDIR=$O" PYTHONUNBUFFERED=1' in st_line[0]
        and len(cs16) == 1 and 'homerel' in cs16[0]
        and '  3) WANT_MAX=1500000;;' in wt16 and '  4) WANT_MAX=1500000;;' in wt16 and 'STORE="${HOME%/}/p6_cjstore"' in wt16, st_line)
    hd = wt16.find(rc_.GIT_DROP_SH)
    first_git = wt16.find('git -C')
    chk('S16b 감시 셸 git 읽기 = 봉인용: run_contract.GIT_DROP_SH 글자 그대로 한 줄 · export GIT_NO_REPLACE_OBJECTS=1 · 둘 다 첫 git -C 앞 · graft · shallow 관문 함수',
        wt16.count(rc_.GIT_DROP_SH) == 1 and 0 <= hd < first_git and 0 <= wt16.find('export GIT_NO_REPLACE_OBJECTS=1') < first_git
        and 'history_problem()' in wt16 and '--is-shallow-repository' in wt16 and 'info/grafts' in wt16, (hd, first_git))
    lf16 = ARGS.ledger if (ARGS is not None and ARGS.ledger) else LEDGER_FILE
    sec16 = ledger_section3(read_text(lf16)) if os.path.exists(lf16) else ''
    s16 = set(ln[4:] for ln in sec16.split('\n') if ln.startswith('    '))
    need16 = [watcher_cmd_line(STORE_ATTEMPTS[3]), runner_cmd_line_store(STORE_ATTEMPTS[3])]
    row3 = [ln for ln in sec16.split('\n') if ln.startswith('| 3 |')]
    row4 = [ln for ln in sec16.split('\n') if ln.startswith('| 4 |')]
    chk('S16c 원장 §3 (%s) 에 시도 줄 3 · 4 (한도 1500000 · 결과 칸 결과 0 건) · 시도 3 · 4 의 명령 줄 (감시 셸 · 러너 CJUNC_STORE) 이 네 칸 들여 쓴 줄로 있다'
        % os.path.relpath(lf16, ROOT),
        len(row3) == 1 and len(row4) == 1 and all('1500000' in r_ and '결과 0 건' in r_ for r_ in row3 + row4) and all(x in s16 for x in need16),
        ([x[:70] for x in need16 if x not in s16], row3[:1], row4[:1]))
    # S15 변이 사본은 문법이 성립한다 (W = bash -n · M = compile): 문법이 깨진 사본은 F · T 묶음이 엉뚱한 까닭 (구문 오류) 으로 "잡는다"
    #     (2 회차 고침 중 W 변이 하나가 빈 then 절이라 구문 오류였고 F01a 가 그 까닭으로 잡았다 · 그 꼴을 막는다)
    wsrc15, rsrc15 = read_text(WRAPPER), read_text(READER)
    broken15 = []
    for kind15, base15, muts15 in (('W', wsrc15, WRAPPER_MUTANTS), ('M', rsrc15, MUTANTS)):
        for name15, pairs15 in muts15:
            m15 = base15
            for old15, new15 in pairs15:
                m15 = m15.replace(old15, new15)
            if kind15 == 'W':
                ok15 = subprocess.run(['bash', '-n'], input=m15, capture_output=True, text=True).returncode == 0
            else:
                try:
                    compile(m15, 'mutant.py', 'exec')
                    ok15 = True
                except SyntaxError:
                    ok15 = False
            if not ok15:
                broken15.append('%s: %s' % (kind15, name15))
    chk('S15 변이 사본 (W %d · M %d) 은 모두 문법이 성립한다 (W = bash -n · M = compile · 깨진 사본은 엉뚱한 까닭으로 잡힌다)'
        % (len(WRAPPER_MUTANTS), len(MUTANTS)), broken15 == [], broken15)


# ═════════════════════════ F · B · R 공용: 가짜 홈 · 핀 저장소 · 가짜 nvidia-smi · 가짜 ps ═════════════════════════
def git(repo, *a, **kw):
    kw.setdefault('env', _rc().git_fixture_env())          # ★ 3 회차 (재확인 2 RCP3-04) — 고정물 git = 전역 · 시스템 설정 끊기 (G7c)
    r = subprocess.run(['git', '-C', str(repo)] + list(GIT_CFG) + list(a), capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError('git %s rc %d: %s' % (a[:2], r.returncode, r.stderr[:300]))
    return r.stdout.strip()


FAKE_RUNNER = r'''#!/usr/bin/env bash
# fake runner (test only) - records what it was given, then behaves like the real runner's outputs
# its pre-run gate commands (read by the watcher; the real runner runs them, this one does not):
#   if ! PYTHONUTF8=1 python3 "$SCR/check_method_discipline.py" >"$_DISC_LOG" 2>&1; then
#   PYTHONUTF8=1 python3 "$SCR/check_undefined_names.py" "$SCR/mpm_webapp_payload.py" "$SCR/step3_sigma.py" >/dev/null 2>&1
D="$PROBE6_FAKE_DIR"
env | LC_ALL=C sort > "$D/runner_env.txt"
fake_store() {   # CJUNC_STORE set: the registry file (made once, 0444) and the arm audit side file next to the arm (status)
  local f st
  f="$CJUNC_STORE/cjreg_@FAKE_KEY@.npz"
  if [ -f "$f" ]; then st=hit; else printf 'fake registry\n' > "$f"; chmod 0444 "$f"; st=built_written; fi
  printf '{"schema": "cjstore-audit-v1", "status": "%s", "key": "@FAKE_KEY@", "file": "cjreg_@FAKE_KEY@.npz", "file_sha256": "%s", "why": null, "bytes": 14}\n' \
    "$st" "$(sha256sum "$f" | awk '{print $1}')" > "$OUTDIR/cjstore_audit_$PROBE6_FAKE_ARM.json"
  echo "$st" >> "$D/store_status.txt"
}
pwd -P > "$D/runner_cwd.txt"
umask > "$D/runner_umask.txt"
echo called >> "$D/calls.txt"
echo "$$" > "$D/runner.pid"
RUN="$(cd "$PWD/kit_SBE_vgcf100/latest_run" && pwd -P)"
mkdir -p "$OUTDIR"
cp "$D/receipt.json" "$OUTDIR/run_receipt.json"
M="${P2_EXTRA##* }"
MF="$(python3 -c 'import sys; print("{:,}".format(int(sys.argv[1])))' "$M" 2>/dev/null)"
if [ "${PROBE6_FAKE_MODE:-ok}" = nosolve ]; then    # the payload stops before the solve line (GPU memory, cupy ...): no STEP3 solve line
  echo "  STEP3: voxelizing conductive+SE grid (stand-in)"
  echo "  STEP3 ABORT - the payload stopped before the solve line (stand-in)"
  exit 1
fi
sed -e "s/@MAXITER_FMT@/$MF/" "$D/log_head.txt"
echo "fake runner stderr line PROBE6_STDERR_MARK" >&2
case "${PROBE6_FAKE_MODE:-ok}" in
  ok)    sleep "${PROBE6_FAKE_SLEEP:-3}"; if [ -n "${CJUNC_STORE:-}" ]; then fake_store; fi
         cp "$D/arm.json" "$OUTDIR/$PROBE6_FAKE_ARM.json"; cat "$D/log_tail_ok.txt"; exit 0;;
  dirty) touch "$(cd "$(dirname "$0")/.." && pwd -P)/untracked_by_runner.txt"
         sleep 1; cp "$D/arm.json" "$OUTDIR/$PROBE6_FAKE_ARM.json"; cat "$D/log_tail_ok.txt"; exit 0;;
  fail)  sleep "${PROBE6_FAKE_SLEEP:-2}"; cp "$D/arm_failed.json" "$RUN/$PROBE6_FAKE_ARM.json.failed"
         sed -e "s/@MAXITER@/$M/" "$D/log_tail_fail.txt"; exit 1;;
  hang)  ( sleep 300 ) & echo $! > "$D/child.pid"; wait;;
  stubborn) ( trap '' TERM; while :; do sleep 1; done ) & echo $! > "$D/child.pid"; wait;;
  tree)  ( trap '' TERM; exec sleep 25 ) & echo $! > "$D/child.pid"
         sleep 1; cp "$D/arm.json" "$OUTDIR/$PROBE6_FAKE_ARM.json"; cat "$D/log_tail_ok.txt"; exit 0;;
  unbuf) python3 -c 'import sys, time; sys.stdout.write(open(sys.argv[1], encoding="utf-8").read()); time.sleep(300)' "$D/log_unbuf.txt";;
  big)   python3 -c 'import time; b = bytearray(50 * 1024 * 1024); time.sleep(40)';;
esac
'''
FAKE_RUNNER = FAKE_RUNNER.replace('@FAKE_KEY@', FAKE_KEY)
#: 가짜 러너의 런 전 관문 둘 (핀 저장소의 scripts/ · 진짜 관문의 자리 · env PROBE6_FAKE_GATE 로 실패 · 지연)
FAKE_GATE = r'''import os
import sys
import time
w = os.environ.get('PROBE6_FAKE_GATE', '')
if w == 'sleep':
    time.sleep(6)
d = os.environ.get('PROBE6_FAKE_DIR')
if d:
    with open(os.path.join(d, 'gate_%s_argv.txt' % os.path.basename(sys.argv[0])[:-3]), 'w') as f:
        f.write('\n'.join(sys.argv[1:]) + '\n')
print('fake gate %s' % os.path.basename(sys.argv[0]))
sys.exit(1 if w == '@NAME@' else 0)
'''
FAKE_SMI = r'''#!/usr/bin/env bash
# fake nvidia-smi (test only): queries during the run fail when the file smi_fail exists in the fake dir
case "$*" in
  *--query-gpu=name,driver_version,memory.total*) echo "Fake GeForce RTX 3090, 535.183.01, 24576";;
  *--query-gpu=memory.used,utilization.gpu*)
    if [ -e "${PROBE6_FAKE_DIR:-/nonexistent}/smi_fail" ]; then exit 1; fi; echo "2345, 87";;
  *--query-compute-apps*)
    if [ -e "${PROBE6_FAKE_DIR:-/nonexistent}/smi_fail" ]; then exit 1; fi; echo "1, 1111";;
  "")                                             echo "| NVIDIA-SMI 535.183.01   Driver Version: 535.183.01   CUDA Version: 12.2 |";;
  *) exit 1;;
esac
'''
#: 가짜 ps (시험 전용): 진짜 ps 를 부르고 이 시험의 프로세스 (env 에 PROBE6_TEST_TAG) 만 남긴다: 본 트리의 게이트가 같은 기계에서
#: 실제 러너 · payload 를 돌려도 동시 실행 가드 (F2) 가 그것을 보지 않게.  ps_fail 이 있으면 -e 꼴 (표본) 이 실패한다.
FAKE_PS = r'''#!/usr/bin/env bash
case " $* " in *" -e "*) if [ -e "${PROBE6_FAKE_DIR:-/nonexistent}/ps_fail" ]; then exit 1; fi;; esac
out="$("@REAL_PS@" "$@")" || exit $?
printf '%s\n' "$out" | while read -r pid rest; do
  case "$pid" in ''|*[!0-9]*) continue;; esac
  if tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -qx "PROBE6_TEST_TAG=@TAG@"; then printf '%s %s\n' "$pid" "$rest"; fi
done
exit 0
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
    #  ★ 11-12 (Rint ② Q11) — 생산 GPU 길이 Jacobi 전처리를 벡터 곱 연산자 (`LinearOperator`) 로 넘긴다 → 대역도 그 이름을 잇는다 (scipy 의 같은 이름)
    ('cupyx/scipy/sparse/linalg/__init__.py', 'from scipy.sparse.linalg import cg, LinearOperator  # noqa: F401\n'),
)
#: 가짜 킷의 payload 줄 (생산 킷 꼴: `scripts/mpm_input_from_case.py` 가 `--step3-gpu` 를 늘 넣는다)
FAKE_KIT_SH = '#!/usr/bin/env bash\npython3 "$SCR/mpm_webapp_payload.py" --step3-gpu --out mpm_payload.json\n'
#: 가짜 GNU time -v (시험 전용): 명령을 돌린 뒤 time -v 꼴 기록을 쓴다 (GNU time 처럼 명령 줄 전체를 적는다 = 홈 경로가 든다)
FAKE_TIME = r'''#!/usr/bin/env bash
[ "$1" = -v ] && shift
out=/dev/null
if [ "$1" = -o ]; then out="$2"; shift 2; fi
"$@"
rc=$?
{
  printf '\tCommand being timed: "%s"\n' "$*"
  printf '\tUser time (seconds): 0.01\n'
  printf '\tMaximum resident set size (kbytes): 12345\n'
  printf '\tElapsed (wall clock) time (h:mm:ss or m:ss): 0:03.01\n'
  printf '\tExit status: %d\n' "$rc"
} > "$out"
exit $rc
'''
#: 감시 셸 · 블록이 쓰는 python3 (가짜 venv): 판독기를 부를 때 PROBE6_FAKE_READER_SLEEP 초 잔다 (끝 기록 중 신호 시험)
PY_SHIM = '#!/usr/bin/env bash\ncase "$*" in *probe6_read.py*) if [ -n "${PROBE6_FAKE_READER_SLEEP:-}" ]; then sleep "$PROBE6_FAKE_READER_SLEEP"; fi;; esac\nexec "%s" "$@"\n'


def make_home(name, shim_text=None, np_cupy=False):
    """가짜 홈: dem-venv (activate = PATH 앞에 가짜 python3 · nvidia-smi · ps) · sdcp/kit (S0 계획의 런 폴더 이름) · 가짜 cupy.
    가짜 cupy 는 venv 의 python3 가 스스로 찾는다 (진짜 venv 의 site-packages 꼴 · 감시 셸은 PYTHONPATH 를 걷어낸다 · P6R2-05) ·
    PROBE6_NO_FAKEMODS=1 이면 못 찾는다 (cupy 를 못 불러오는 기계 꼴)."""
    home = os.path.join(TD, name)
    bind = os.path.join(home, 'dem-venv', 'bin')
    os.makedirs(bind)
    shim = shim_text if shim_text is not None else PY_SHIM % os.path.abspath(sys.executable)
    assert shim.startswith('#!/usr/bin/env bash\n'), shim[:40]
    shim = shim.replace('#!/usr/bin/env bash\n', '#!/usr/bin/env bash\nif [ -z "${PROBE6_NO_FAKEMODS:-}" ]; then export PYTHONPATH="%s"; fi\n'
                        % os.path.join(home, 'fakemods'), 1)
    write_text(os.path.join(bind, 'python3'), shim, 0o755)
    write_text(os.path.join(bind, 'nvidia-smi'), FAKE_SMI, 0o755)
    write_text(os.path.join(bind, 'ps'), FAKE_PS.replace('@REAL_PS@', REAL_PS).replace('@TAG@', TAG), 0o755)
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


def make_pin_repo(name, real_scripts=False, plan_inputs=None, plan_tol=None, runner_text=None, wrapper_patch=None, reader_patch=None):
    """핀 저장소 (git 고정물): 감시 셸 · 판독기 사본 · S0 계획 · 러너 (가짜 또는 이 리포 scripts/ 사본) → (저장소, 핀 40-hex).
    plan_inputs · plan_tol = S0 계획의 입력 지문 · tol_ff 만 바꾼다 · wrapper_patch · reader_patch = (옛 글, 새 글) 감시 셸 · 판독기 사본 고침
    (시험 전용)."""
    repo = os.path.join(TD, name)
    os.makedirs(os.path.join(repo, TOOLS_REL))
    wsrc = read_text(WRAPPER_SRC or WRAPPER)
    if wrapper_patch:
        assert wsrc.count(wrapper_patch[0]) == 1, wrapper_patch[0]
        wsrc = wsrc.replace(wrapper_patch[0], wrapper_patch[1])
    write_text(os.path.join(repo, TOOLS_REL, 'run_probe6.sh'), wsrc)
    rsrc = read_text(READER)
    if reader_patch:
        assert rsrc.count(reader_patch[0]) == 1, reader_patch[0]
        rsrc = rsrc.replace(reader_patch[0], reader_patch[1])
    write_text(os.path.join(repo, TOOLS_REL, 'probe6_read.py'), rsrc)
    os.makedirs(os.path.dirname(os.path.join(repo, S0PLAN_REL)))
    shutil.copy(os.path.join(ROOT, S0PLAN_REL), os.path.join(repo, S0PLAN_REL))
    if plan_inputs is not None or plan_tol is not None:
        plan = json.loads(read_text(os.path.join(ROOT, S0PLAN_REL)))
        if plan_inputs is not None:
            plan['source']['inputs_sha256'] = dict(plan_inputs)
        if plan_tol is not None:
            plan['values_um']['tol_ff'] = plan_tol
        write_text(os.path.join(repo, S0PLAN_REL), json.dumps(plan, indent=1, sort_keys=True) + '\n')
    if real_scripts:
        shutil.copytree(SCRIPTS, os.path.join(repo, 'scripts'), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        os.makedirs(os.path.dirname(os.path.join(repo, PREREG_REL)), exist_ok=True)
        shutil.copy(os.path.join(ROOT, PREREG_REL), os.path.join(repo, PREREG_REL))
    else:
        write_text(os.path.join(repo, RUNNER_REL), runner_text if runner_text is not None else FAKE_RUNNER, 0o755)
        for nm, key in (('check_method_discipline.py', 'discipline'), ('check_undefined_names.py', 'undefined')):
            write_text(os.path.join(repo, 'scripts', nm), FAKE_GATE.replace('@NAME@', key))
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
    af = failed_arm(int(A1))                                      # 시도 1 이 한도 30000 에 닿은 꼴
    dset(af, S3 + 'manifest.code_sha', pin[:9])
    with open(os.path.join(d, 'arm_failed.json'), 'w', encoding='utf-8') as f:
        json.dump(af, f)
    rc_ = receipt_doc()
    rc_['code_sha'] = pin[:9]
    with open(os.path.join(d, 'receipt.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(rc_, sort_keys=True))
    write_text(os.path.join(d, 'log_head.txt'), LOG_HEAD.replace('{maxiter}', '@MAXITER_FMT@').format(arm=arm_name))
    write_text(os.path.join(d, 'log_tail_ok.txt'), LOG_TAIL_OK.format(sig=SEAL, seal2='[봉인]', arm=arm_name, maxiter_plain=MAXITER))
    write_text(os.path.join(d, 'log_tail_fail.txt'), LOG_TAIL_FAIL.replace('{maxiter_plain}', '@MAXITER@').format(sig=SEAL, seal2='[봉인]', arm=arm_name))
    write_text(os.path.join(d, 'log_unbuf.txt'), '  ⚠ STEP3 CG not converged (info=30000, resid=4.4e-07) — σ UNRELIABLE\n')
    return d


_ENV_DROP = ('LEAN', 'VOX', 'ARMS', 'ARM_LIST', 'KITS', 'FIBRE_STAMP', 'BRIDGE_UM', 'OUTDIR', 'EXPECT_PROTOCOL', 'EXPECT_BACKEND',
             'VIRTUAL_ENV', 'PYTHONPATH', 'PYTHONVERBOSE', 'PYTHONUNBUFFERED') + ENV_NAMES_T


def wrapper_env(home, fake=None, **over):
    """감시 셸을 부르는 env: PYTHONUNBUFFERED · PYTHONPATH 를 일부러 뺀다 (감시 셸이 러너에 PYTHONUNBUFFERED 를 주고 PYTHONPATH 는 걷는다 ·
    가짜 cupy 는 venv 의 python3 가 찾는다) · 이 시험의 표지 (PROBE6_TEST_TAG)."""
    e = {k: v for k, v in os.environ.items() if not k.startswith(('SIGMA_', 'SDCP_', 'PTFE_', 'CJUNC', 'STEP3_', 'MPM_', 'P2_', 'PROBE6_'))
         and k not in _ENV_DROP and k not in ('SHELLOPTS', 'BASHOPTS')}
    e.update(HOME=home, PATH=os.path.join(home, 'dem-venv', 'bin') + os.pathsep + os.environ.get('PATH', '/usr/bin:/bin'),
             PYTHONDONTWRITEBYTECODE='1', PROBE6_SAMPLE_S='1', PROBE6_TEST_TAG=TAG)
    if fake:
        e.update(PROBE6_FAKE_DIR=fake, PROBE6_FAKE_ARM=ARM)
    e.update({k: str(v) for k, v in over.items()})
    return e


def run_wrapper(repo, pin, home, tag, env, maxiter=None, out=None, lg=None, mk_log=True, timeout=180, wrapper=None, umask=None,
                attempt=1):
    """maxiter 기본 = 그 시도 번호의 등록 한도 (1 → 30000 · 2 → 1500000 · 3 · 4 → 1500000)."""
    maxiter = ALL_MAXITER[attempt] if maxiter is None else maxiter
    out = out or os.path.join(home, 'sdcp', 'ca1_probe6_a%d_%s_arm1' % (attempt, tag))
    lg = lg or os.path.join(home, 'p6log_a%d_%s' % (attempt, tag))
    if mk_log and not os.path.isdir(lg):
        os.makedirs(lg)
    w = wrapper or os.path.join(repo, TOOLS_REL, 'run_probe6.sh')
    pre = (lambda: os.umask(umask)) if umask is not None else None
    t0 = time.time()
    p = subprocess.run(['bash', w, repo, out, lg, pin, maxiter], env=env, capture_output=True, text=True, encoding='utf-8',
                       errors='replace', stdin=subprocess.DEVNULL, timeout=timeout, preexec_fn=pre)
    r = Res()
    r.rc, r.so, r.se, r.out, r.lg, r.dt = p.returncode, p.stdout or '', p.stderr or '', out, lg, time.time() - t0
    r.meta = read_meta(lg)
    rp = os.path.join(lg, 'probe6_report.json')
    r.rep = json.loads(read_text(rp)) if os.path.exists(rp) else None
    return r


def read_meta(lg):
    p = os.path.join(lg, 'meta.txt')
    return dict(ln.split('=', 1) for ln in read_text(p).splitlines() if '=' in ln) if os.path.exists(p) else {}


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


def read_pid(p):
    try:
        return int(read_text(p).strip())
    except (OSError, ValueError):
        return -1


BUNDLE_ALLOWED = {'probe6_report.json', 'probe6_screen.txt', 'runner_filtered.log', 'env.txt', 'meta.txt', 'command.txt',
                  'samples.tsv', 'status.log', 'time_v.txt', 'arm_time_v.txt', 'probe6_reader.err', 'SHA256SUMS'}
BUNDLE_NEED = {'probe6_report.json', 'probe6_screen.txt', 'env.txt', 'meta.txt', 'command.txt', 'samples.tsv', 'status.log', 'SHA256SUMS'}
_TIMEV_OK = re.compile(r'\s*(Maximum resident set size \(kbytes\): [0-9]+|Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): [0-9:.]+'
                       r'|Exit status: [0-9]+)')


def bundle_problems(lg, sealed, home, sd_min=4):
    """묶음의 꼴 (허용된 이름 · 파일마다 닫힌 꼴 · SHA256SUMS = 실제) + 수 찾기 (σ 와 변형 · 소수 · 유효숫자 sd_min 이상) + 홈 경로 없음."""
    names, members = bundle_members(lg)
    if names is None:
        return ['no bundle']
    P = []
    if not set(names) <= BUNDLE_ALLOWED:
        P.append('bundle names outside the allowlist: %s' % sorted(set(names) - BUNDLE_ALLOWED))
    if not BUNDLE_NEED <= set(names):
        P.append('bundle lacks %s' % sorted(BUNDLE_NEED - set(names)))
    shas = dict((ln.split('  ', 1)[1], ln.split('  ', 1)[0]) for ln in members.get('SHA256SUMS', '').splitlines() if '  ' in ln)
    if set(shas) != set(names) - {'SHA256SUMS'} or any(hashlib.sha256(members[n].encode('utf-8')).hexdigest() != h
                                                       for n, h in shas.items() if n in members):
        P.append('SHA256SUMS differs from the bundle members')
    try:
        rep = json.loads(members.get('probe6_report.json', ''))
    except ValueError:
        rep = None
        P.append('report is not JSON')
    if rep is not None:
        P += ['report: ' + x for x in report_problems(rep)]
        P += ['screen: ' + x for x in screen_problems(members.get('probe6_screen.txt', ''), rep)]
        P += ['filtered: ' + x for x in filtered_problems(members.get('runner_filtered.log', ''), rep)]
    for ln in members.get('meta.txt', '').splitlines():
        k, _s, v = ln.partition('=')
        if k not in META_SCHEMA or re.fullmatch(META_SCHEMA[k][1], v) is None:
            P.append('meta line %s' % k[:40])
    for ln in members.get('env.txt', '').splitlines():
        k, _s, v = ln.partition('=')
        if k not in ENV_KEYS_T or re.fullmatch(r'[A-Za-z0-9 ._:+()/@,#-]{0,120}', v) is None:
            P.append('env line %s' % k[:40])
    for ln in members.get('samples.tsv', '').splitlines()[1:]:
        if re.fullmatch(r'[0-9]+(\t(?:[0-9]+|NA)){7}', ln) is None:
            P.append('samples line shape')
            break
    if any(not ln.startswith('[probe6] ') for ln in members.get('status.log', '').splitlines()):
        P.append('status.log line without the [probe6] prefix')
    cl = members.get('command.txt', '').splitlines()
    if len(cl) != 2 or not cl[0].startswith('# cwd: ') or not cl[1].startswith('env '):
        P.append('command.txt shape')
    for nm in ('time_v.txt', 'arm_time_v.txt'):
        if any(_TIMEV_OK.fullmatch(ln) is None for ln in members.get(nm, '').splitlines()):
            P.append('%s has a line other than max RSS / elapsed / exit status' % nm)
    if members.get('probe6_reader.err', '') != '':
        P.append('probe6_reader.err is not empty')
    if any(home in t for t in members.values()):
        P.append('a bundle member holds the home absolute path')
    meta = dict(ln.split('=', 1) for ln in members.get('meta.txt', '').splitlines() if '=' in ln)
    safe = safe_hex(rep, extra=list(shas.values()) + [v for k, v in meta.items() if k.endswith('sha256') or k.startswith('tool_sha256')
                                                       or k == 'pin'] + [PIN_FIX])
    P += ['leak: ' + h for h in scan_hits(list(members.values()), sealed, safe, sd_min=sd_min, floats_only=True)]
    return P


def stop_line(r):
    line = [ln for ln in r.so.splitlines() if 'STOP:' in ln]
    return line[-1] if line else ''


def safe_kill(pid):
    """이 시험이 띄운 프로세스만 끝낸다: 번호 > 1 · 자기 / 부모 아님 · 살아 있음 · env 에 이 시험의 표지 (PROBE6_TEST_TAG) → SIGKILL."""
    if not isinstance(pid, int) or pid <= 1 or pid in (os.getpid(), os.getppid()) or not proc_alive(pid):
        return False
    try:
        with open('/proc/%d/environ' % pid, 'rb') as f:
            if ('PROBE6_TEST_TAG=%s' % TAG).encode() not in f.read().split(b'\0'):
                return False
        os.kill(pid, signal.SIGKILL)
    except OSError:
        return False
    return True


#: 합성 로그 폴더 (시도 번호 검사 · P6R2-01 · 02): 감시 셸 · 블록이 보는 표지 · meta · status.log 의 꼴만
START_LINE = '[probe6] 2026-11-10T00:00:00Z runner started - maxiter 30000, host RSS cap 40 GB, sampling every 10 s\n'
WF_LINE = '[probe6] 2026-11-10T00:00:00Z WATCHER FAILED (rc 1) after the runner started - stopping the runner group\n'


def lf_done(attempt, pin, solve=1):
    return {'DONE': 'runner_rc=1 report_rc=3 attempt=%d orphans=0\n' % attempt,
            'meta.txt': 'probe6_meta_version=2\nattempt=%d\npin=%s\nsolve_started=%d\n' % (attempt, pin, solve)}


LF_WF_START = {'WATCHER_FAILED': 'rc=1\nrunner_started=1\n', 'status.log': START_LINE + WF_LINE}
LF_WF_NOSTART = {'WATCHER_FAILED': 'rc=1\nrunner_started=1\n', 'status.log': WF_LINE}
LF_STOPPED = {'STOPPED': 'reason=stand-in\nrunner_started=0\n', 'nohup.out': ''}


def log_folder(home, name, files):
    d = os.path.join(home, name)
    os.makedirs(d)
    for nm, body in files.items():
        write_text(os.path.join(d, nm), body)
    return d


@case('F 감시 셸 (가짜 러너)')
def t_F(pre='f'):
    repo, pin = make_pin_repo(pre + '_pin')
    home = make_home(pre + '_home')            # 멈춤 조건 (F08) → 시도 1 (F09) → 시도 2 (F09d) 의 홈
    fd = fake_dir(pre + '_fake', pin)
    bash_env = os.path.join(TD, pre + '_bashenv.sh')
    write_text(bash_env, '# BASH_ENV of the test (sourced by every non-interactive bash; does nothing)\n')
    # F01 성공 경로 (시도 1 · 한도 30000 · 따로 홈: 끝난 시도 1 은 같은 홈의 다음 시도 1 을 막는다 · P6R2-02)
    #     부모 셸에 축 env · 걷어내기 목록의 이름꼴 · PYTHONVERBOSE · PYTHONPATH (가짜) · BASH_ENV · umask 002 를 일부러 둔다
    h1 = make_home(pre + '_home_ok')
    lock1 = os.path.join(h1, '.probe6.lock')
    env = wrapper_env(h1, fd, SIGMA_VGCF_OVERRIDE='7854', LEAN='4', VOX='0.4', P2_EXTRA='--show-results', CJUNC_SV_CF='1',
                      MPM_PERIODIC_SIGMA='1', KITS='kit_DBE_sdcp1um_vgcf100', OUTDIR='/nonexistent/x', ARM_LIST='1,2', P2_ATTEMPT='1',
                      FIBRE_STAMP='point', SDCP_YIELD_VGCF='1', PTFE_BLOCK_UM='0.1', EXPECT_PROTOCOL='p9', STEP3_X='1',
                      PYTHONVERBOSE='1', CUDA_VISIBLE_DEVICES='0', OPENBLAS_CORETYPE='SkylakeX', BASH_ENV=bash_env,
                      PYTHONPATH=os.path.join(h1, 'decoy_pythonpath'))
    r = run_wrapper(repo, pin, h1, 'ok', env, umask=0o002)
    chk('F01a 성공 경로: 감시 셸 rc 0 · 러너 rc 0 · 판독 rc 0 (PROBE_OK) · DONE · STOPPED / WATCHER_FAILED 없음 · watcher.pid 지움 · 잠금 풂',
        r.rc == 0 and r.meta.get('runner_rc') == '0' and (r.rep or {}).get('verdict') == 'PROBE_OK'
        and os.path.exists(os.path.join(r.lg, 'DONE')) and not os.path.exists(os.path.join(r.lg, 'STOPPED'))
        and not os.path.exists(os.path.join(r.lg, 'WATCHER_FAILED')) and not os.path.exists(os.path.join(r.lg, 'watcher.pid'))
        and not os.path.exists(lock1), (r.rc, r.so[-900:], r.se[-300:], (r.rep or {}).get('problems')))
    f01b = [n for n, c in (('prefix', all(ln.startswith('[probe6] ') for ln in r.so.splitlines())), ('stderr', r.se == ''),
                           ('no STEP3 line', re.search(r'STEP3[ :]', r.so) is None), ('no [p2]', '[p2]' not in r.so),
                           ('cg_iters', 'cg_iters' in r.so and '48211' in r.so),
                           ('scan', scan_hits([r.so], T_SEALED, sd_min=4, floats_only=True) == [])) if not c]
    chk('F01b 화면 (nohup.out 에 갈 글) = [probe6] 줄만 · 러너 원문 줄 없음 · 허용 칸은 보인다 · σ 류 수 없음', f01b == [],
        (f01b, r.se[-300:], [ln for ln in r.so.splitlines() if not ln.startswith('[probe6] ') or 'STEP3' in ln][:5],
         scan_hits([r.so], T_SEALED, sd_min=4, floats_only=True)[:3]))
    raw = read_text(os.path.join(r.lg, 'runner.log'))
    wer = read_text(os.path.join(r.lg, 'watcher.err')) if os.path.exists(os.path.join(r.lg, 'watcher.err')) else ''
    chk('F01c 러너 원문 (stdout · stderr) 은 로그 폴더의 runner.log 에만 (감시 셸 화면 · watcher.err 에 없다)',
        '7133.31' in raw and 'STEP3 solve:' in raw and 'PROBE6_STDERR_MARK' in raw and 'PROBE6_STDERR_MARK' not in wer + r.so + r.se,
        (raw[:200], wer[-200:]))
    bp = bundle_problems(r.lg, T_SEALED, h1)
    names, members = bundle_members(r.lg)
    chk('F01d 묶음: 허용된 이름만 · 파일마다 닫힌 꼴 · SHA256SUMS = 실제 · σ 류 수 · 홈 경로 없음', bp == [], bp[:6])
    st_now = read_text(os.path.join(r.lg, 'status.log'))
    st_b = members.get('status.log', '')
    tail = st_now[len(st_b):].splitlines() if st_now.startswith(st_b) else ['(not a prefix)']
    chk('F01e 묶음의 status.log = 묶기 직전 사본 (그 뒤 줄 = 묶음 · DONE 두 줄뿐) · SHA256SUMS 와 어긋남 없음',
        len(tail) == 2 and ' bundle ' in tail[0] and ' DONE runner_rc=0 report_rc=0 attempt=1' in tail[1], tail)
    chk('F01f 묶음의 time_v.txt = 세 줄 (최대 RSS · 경과 · 종료 코드) · 명령 줄 · 홈 경로 없음',
        'time_v.txt' not in members or (len(members['time_v.txt'].splitlines()) == 3 and 'Command' not in members['time_v.txt']),
        members.get('time_v.txt', '')[:300])
    chk('F01g 판독기는 -I 로 돈다: 부모 셸의 PYTHONVERBOSE 가 판독기에 닿지 않는다 (probe6_reader.err 빈 파일)',
        os.path.exists(os.path.join(r.lg, 'probe6_reader.err')) and read_text(os.path.join(r.lg, 'probe6_reader.err')) == '', '')
    # F02 러너가 받은 env · cwd · umask · 런 전 관문
    renv = dict(ln.split('=', 1) for ln in read_text(os.path.join(fd, 'runner_env.txt')).splitlines() if '=' in ln)
    want = dict(AXES, P2_EXTRA='--step3-maxiter ' + A1, OUTDIR=r.out)
    axis_like = {k: v for k, v in renv.items() if k.startswith(('SIGMA_', 'SDCP_', 'PTFE_', 'CJUNC', 'STEP3_', 'MPM_', 'P2_'))
                 or k in ('LEAN', 'VOX', 'ARMS', 'ARM_LIST', 'KITS', 'FIBRE_STAMP', 'BRIDGE_UM', 'OUTDIR', 'EXPECT_PROTOCOL', 'EXPECT_BACKEND')}
    chk('F02a 러너가 받은 축 env = 등록 축 + P2_EXTRA + OUTDIR 뿐 (부모 셸의 SIGMA_VGCF_OVERRIDE · LEAN=4 · FIBRE_STAMP · SDCP_YIELD_VGCF · '
        'PTFE_BLOCK_UM · EXPECT_PROTOCOL · STEP3_X … 는 걷힘)',
        axis_like == want, {k: (axis_like.get(k), want.get(k)) for k in set(axis_like) | set(want) if axis_like.get(k) != want.get(k)})
    chk('F02b 러너에 PYTHONUNBUFFERED=1 (부모 셸에 없었다) · meta env_PYTHONUNBUFFERED = value:1',
        renv.get('PYTHONUNBUFFERED') == '1' and r.meta.get('env_PYTHONUNBUFFERED') == 'value:1', (renv.get('PYTHONUNBUFFERED'), r.meta.get('env_PYTHONUNBUFFERED')))
    chk('F02c 걷어낸 이름이 메타에 남는다 (이름만)',
        set(r.meta.get('scrubbed', '').split()) >= {'SIGMA_VGCF_OVERRIDE', 'LEAN', 'VOX', 'P2_EXTRA', 'ARM_LIST', 'FIBRE_STAMP',
                                                    'SDCP_YIELD_VGCF', 'PTFE_BLOCK_UM', 'EXPECT_PROTOCOL', 'STEP3_X'}, r.meta.get('scrubbed'))
    chk('F02d 러너 cwd = 킷 뿌리 (~/sdcp) · umask 0022',
        read_text(os.path.join(fd, 'runner_cwd.txt')).strip() == os.path.realpath(os.path.join(h1, 'sdcp'))
        and read_text(os.path.join(fd, 'runner_umask.txt')).strip() == '0022', read_text(os.path.join(fd, 'runner_cwd.txt')))
    ua = read_text(os.path.join(fd, 'gate_check_undefined_names_argv.txt')).split() if os.path.exists(
        os.path.join(fd, 'gate_check_undefined_names_argv.txt')) else []
    chk('F02e 러너의 런 전 관문 둘을 러너 시작 전에 같은 꼴로 돌렸다 (미정의 이름 검사의 파일 = 러너 글에 적힌 파일) · meta pregate 1',
        ua == [os.path.join(repo, 'scripts', 'mpm_webapp_payload.py'), os.path.join(repo, 'scripts', 'step3_sigma.py')]
        and os.path.exists(os.path.join(fd, 'gate_check_method_discipline_argv.txt')) and r.meta.get('pregate') == '1', ua)
    chk('F02f 러너 env 에 PYTHONPATH · BASH_ENV · SHELLOPTS 가 없다 (부모 셸에 PYTHONPATH · BASH_ENV 가 있었다 · 감시 셸이 PYTHONPATH 를 걷고 '
        'env -u BASH_ENV -u SHELLOPTS 로 띄운다 · P6R2-05 · 06) · meta pythonpath_removed 1 · pythonpath_set 0 · env_BASH_ENV = set (부모 셸 기록)',
        not [k for k in ('PYTHONPATH', 'BASH_ENV', 'SHELLOPTS') if k in renv] and r.meta.get('pythonpath_removed') == '1'
        and r.meta.get('pythonpath_set') == '0' and r.meta.get('env_BASH_ENV') == 'set',
        ([k for k in ('PYTHONPATH', 'BASH_ENV', 'SHELLOPTS') if k in renv], r.meta.get('pythonpath_removed'), r.meta.get('pythonpath_set')))
    # F03 실제 파일 · 폴더 모드 (부모 umask 002 였다)
    bad = []
    for base in (r.out, r.lg):
        for d, ds, fs in os.walk(base):
            for nm in ds + fs:
                if os.stat(os.path.join(d, nm)).st_mode & 0o022:
                    bad.append(nm)
    chk('F03 만든 파일 · 폴더에 그룹 · 기타 쓰기 비트 없음 (umask 022) · 메타 mode_bad 0', bad == [] and r.meta.get('mode_bad') == '0'
        and r.meta.get('umask') == '0022', bad[:5])
    chk('F04a 메타: 판 2 · 시도 1 · 핀 · maxiter (시도 1 = 30000) · 기대 rtol · 백엔드 · R_j · 시작 · 끝 · 전체 초 · 도구 sha256 · 킷 런 = S0 계획의 런 폴더 · '
        '풀이 시작 1 · 고아 0 · 시도 2 칸 없음',
        r.meta.get('probe6_meta_version') == '2' and r.meta.get('attempt') == '1' and r.meta.get('pin') == pin
        and r.meta.get('maxiter') == A1 and r.meta.get('expect_rtol') == '1e-12' and r.meta.get('expect_backend') == 'gpu'
        and r.meta.get('expect_rj') == '1e6'
        and int(r.meta.get('wall_s', -1)) >= 2 and r.meta.get('tool_sha256_reader') == sha256_file(READER)
        and r.meta.get('tool_sha256_wrapper') == sha256_file(os.path.join(repo, TOOLS_REL, 'run_probe6.sh'))
        and r.meta.get('kit_run') == S0_RUN and r.meta.get('kit_run_matches_s0') == '1' and r.meta.get('solve_started') == '1'
        and r.meta.get('orphans') == '0' and r.meta.get('orphans_left') == '0' and (r.rep or {}).get('attempt') == 1
        and 'attempt1_pin' not in r.meta and 'code_same_as_attempt1' not in r.meta, r.meta)
    chk('F04b 메타의 폴더 = 홈을 ~ 로 접은 꼴 · env 이름 여섯 = 있음 / 없음 / 짧은 값 (값 전체는 짧은 이름 · 숫자일 때만) · GPU · 디스크',
        r.meta.get('outdir') == '~/sdcp/ca1_probe6_a1_ok_arm1' and r.meta.get('logdir') == '~/p6log_a1_ok'
        and r.meta.get('env_CUDA_VISIBLE_DEVICES') == 'value:0' and r.meta.get('env_OPENBLAS_CORETYPE') == 'value:SkylakeX'
        and r.meta.get('env_BASH_ENV') == 'set' and r.meta.get('env_OMP_NUM_THREADS') == 'unset'
        and r.meta.get('env_OPENBLAS_NUM_THREADS') == 'unset' and r.meta.get('gpu_used_start_mib') == '2345'
        and re.fullmatch(r'[0-9]+', r.meta.get('disk_free_gb_kit', '')) and re.fullmatch(r'[0-9]+', r.meta.get('disk_free_gb_log', '')),
        dict((k, r.meta.get(k)) for k in ('outdir', 'logdir', 'env_CUDA_VISIBLE_DEVICES', 'env_BASH_ENV', 'gpu_used_start_mib', 'disk_free_gb_kit')))
    cmdt = read_text(os.path.join(r.lg, 'command.txt')).splitlines()
    want_cmd = runner_cmd_line(A1, outdir='~/sdcp/ca1_probe6_a1_ok_arm1', w=repo)
    chk('F05 command.txt = 실제로 돈 명령 = 원장 줄 초안의 러너 줄 꼴 (<O> · <W> · maxiter 자리만 채움) · cwd 줄',
        len(cmdt) == 2 and cmdt[0] == '# cwd: ~/sdcp' and cmdt[1] == want_cmd, (cmdt, want_cmd))
    envt = read_text(os.path.join(r.lg, 'env.txt'))
    chk('F06 환경 지문: python · numpy · scipy · cupy · GPU 이름 · 드라이버 · CUDA · BLAS (판만) · 호스트 이름 줄 없음',
        all(re.search(r'^%s=\S' % k, envt, re.M) for k in ('python', 'numpy', 'scipy', 'cupy', 'gpu_name', 'gpu_driver', 'cuda_version',
                                                               'numpy_blas', 'kernel'))
        and not re.search(r'^(host|hostname|user|ip)=', envt, re.M | re.I), envt)
    tm = (r.rep or {}).get('timing') or {}
    rs = (r.rep or {}).get('resources') or {}
    pl = [ln for ln in st_now.splitlines() if ' pre-launch: ' in ln]
    chk('F07 표본: CG + 증서 구간 1 초 이상 · 전체 초 이하 · GPU 최대 (가짜 2345) · RSS 표본 > 0 · 발사 전 줄 (GPU 사용 · 디스크 여유)',
        isinstance(tm.get('cg_cert_s'), int) and 1 <= tm.get('cg_cert_s') <= int(r.meta.get('wall_s', 0))
        and rs.get('gpu_used_max_mib') == 2345 and (rs.get('rss_sum_max_kb') or 0) > 0 and len(pl) == 1
        and 'attempt 1, GPU memory in use 2345 MiB of 24576 MiB, disk free' in pl[0], (tm, rs, pl))
    # F08 멈춤 조건: 러너를 부르지 않는다 · 로그 폴더를 받은 뒤의 멈춤은 STOPPED 표지
    calls0 = len(read_text(os.path.join(fd, 'calls.txt')).splitlines())
    env2 = wrapper_env(home, fd)
    lock = os.path.join(home, '.probe6.lock')
    stops = []

    def stop_case(label, needle, r2, marker=True):
        line = stop_line(r2)
        stp = os.path.join(r2.lg, 'STOPPED')
        mk = read_text(stp) if os.path.exists(stp) else ''
        okm = (('reason=' in mk and 'runner_started=0' in mk and needle in mk) if marker else not os.path.exists(stp))
        stops.append((label, r2.rc, bool(line) and needle in line and 'runner not started' in line and okm, line[-170:] or r2.so[-170:]))

    f01_files = sorted(os.listdir(r.lg))
    stop_case('출력 폴더가 비어 있지 않음', 'output folder exists and is not empty',
              run_wrapper(repo, pin, home, 'ok', env2, out=r.out, lg=os.path.join(home, 'p6log_a1_s1')))
    stop_case('로그 폴더에 옛 파일 (앞 시도의 폴더 · 아무것도 쓰지 않는다)', 'log folder is not new', run_wrapper(repo, pin, home, 's2', env2, lg=r.lg),
              marker=False)
    stop_case('핀 다름', 'worktree HEAD differs from PIN', run_wrapper(repo, 'b' * 40, home, 's3', env2))
    stop_case('maxiter 가 숫자가 아님', 'MAXITER must be a positive integer', run_wrapper(repo, pin, home, 's4', env2, maxiter='4e5'))
    stop_case('출력 폴더 이름에 시도 번호 · _arm1 없음', 'output folder name must be',
              run_wrapper(repo, pin, home, 's5', env2, out=os.path.join(home, 'sdcp', 'ca1_probe6_plain')))
    stop_case('로그 폴더 없음', 'log folder does not exist', run_wrapper(repo, pin, home, 's6', env2, mk_log=False), marker=False)
    outside = os.path.join(TD, pre + '_outside', 'run_probe6.sh')     # 시험 대상 감시 셸의 사본을 핀 작업 트리 밖에 둔다 (옆에 판독기도)
    os.makedirs(os.path.dirname(outside))
    shutil.copy(os.path.join(repo, TOOLS_REL, 'run_probe6.sh'), outside)
    shutil.copy(READER, os.path.join(os.path.dirname(outside), 'probe6_read.py'))
    stop_case('핀 작업 트리 밖의 감시 셸 사본', 'not the copy inside the pinned worktree', run_wrapper(repo, pin, home, 's7', env2, wrapper=outside))
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
    stop_case('cupy 를 못 불러옴 (GPU 기대)', 'cupy cannot be imported', run_wrapper(repo, pin, home, 's11', dict(env2, PROBE6_NO_FAKEMODS='1')))
    kit_sh = os.path.join(home, 'sdcp', KIT, 'run_mpm.sh')
    write_text(kit_sh, FAKE_KIT_SH.replace(' --step3-gpu', ''))
    stop_case('킷 payload 줄에 --step3-gpu 없음 (CPU 로 풀고 러너가 팔을 받지 않는다)', 'no --step3-gpu', run_wrapper(repo, pin, home, 's12', env2))
    for i, flag in enumerate(('--joule-heat', '--save-step4-grid step4_grid.npz', '--show-results')):
        write_text(kit_sh, FAKE_KIT_SH.replace(' --out', ' %s --out' % flag))
        stop_case('킷 payload 줄에 %s' % flag.split()[0], flag.split()[0], run_wrapper(repo, pin, home, 's13%d' % i, env2))
    write_text(kit_sh, FAKE_KIT_SH)
    os.makedirs(lock)
    write_text(os.path.join(lock, 'owner'), 'pid=1\nlogdir=~/p6log_a1_other\n')
    stop_case('잠금이 이미 있다 (다른 감시 셸 · 죽은 감시 셸이 남긴 것)', 'holds the lock', run_wrapper(repo, pin, home, 's14', env2))
    lock_kept = os.path.isdir(lock) and read_text(os.path.join(lock, 'owner')).startswith('pid=1')
    shutil.rmtree(lock)
    for i, arg in enumerate(('mpm_webapp_payload.py', 'sdcp_gain_vox015_8arm.sh')):
        bz = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)', '/x/scripts/' + arg], env=dict(env2),
                              stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.3)
        stop_case('이 계정에서 %s 가 돌고 있다' % arg, 'already runs under this account', run_wrapper(repo, pin, home, 's15%d' % i, env2))
        bz.kill()
        bz.wait()
    for i, gate in enumerate(('discipline', 'undefined')):
        stop_case('러너의 런 전 관문 (%s) 이 실패' % gate, "the runner's own pre-run gate fails",
                  run_wrapper(repo, pin, home, 's16%d' % i, dict(env2, PROBE6_FAKE_GATE=gate)))
    stop_case('경로에 허용 밖 글자 (공백)', 'path must be absolute',
              run_wrapper(repo, pin, home, 's17', env2, out=os.path.join(home, 'sdcp', 'ca1_probe6_a1_x y_arm1')))
    stop_case('로그 폴더 이름에 시도 번호 없음', 'log folder name must start with p6log_a1_',
              run_wrapper(repo, pin, home, 's18', env2, lg=os.path.join(home, 'p6log_s18')))
    stop_case('출력 폴더 · 로그 폴더의 시도 번호가 다름', 'same attempt number',
              run_wrapper(repo, pin, home, 's19', env2, out=os.path.join(home, 'sdcp', 'ca1_probe6_a2_s19_arm1')))
    repo_t, pin_t = make_pin_repo(pre + '_pin_tol', plan_tol=0.05)
    fd_t = fake_dir(pre + '_fake_tol', pin_t)
    stop_case('S0 계획의 tol_ff ≠ 등록 명령 값', 'tol_ff differs', run_wrapper(repo_t, pin_t, home, 's20', wrapper_env(home, fd_t)))
    repo_g, pin_g = make_pin_repo(pre + '_pin_gate', runner_text=FAKE_RUNNER.replace('check_method_discipline.py', 'other_check.py'))
    fd_g = fake_dir(pre + '_fake_gate', pin_g)
    stop_case('러너 글에서 런 전 관문 명령을 못 읽음', "cannot read the runner's pre-run gate commands",
              run_wrapper(repo_g, pin_g, home, 's21', wrapper_env(home, fd_g)))
    # 러너 시작 전 TERM (런 전 관문이 도는 동안)
    lg22 = os.path.join(home, 'p6log_a1_s22')
    os.makedirs(lg22)
    p = subprocess.Popen(['bash', os.path.join(repo, TOOLS_REL, 'run_probe6.sh'), repo, os.path.join(home, 'sdcp', 'ca1_probe6_a1_s22_arm1'),
                          lg22, pin, A1], env=dict(env2, PROBE6_FAKE_GATE='sleep'), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         stdin=subprocess.DEVNULL, text=True)
    for _ in range(100):
        if os.path.exists(os.path.join(lg22, 'pregate_discipline.log')):
            break
        time.sleep(0.1)
    time.sleep(0.5)
    p.send_signal(signal.SIGTERM)
    so, se = p.communicate(timeout=60)
    r22 = Res()
    r22.rc, r22.so, r22.lg = p.returncode, so, lg22
    stop_case('러너 시작 전 TERM', 'signal received before the runner started', r22)
    # 감시 셸이 러너 시작 전에 뜻밖에 끝남 (set -u 위반 = 고친 사본 · 시험 전용) → STOPPED · 잠금 풂
    repo_u, pin_u = make_pin_repo(pre + '_pin_unexp', wrapper_patch=('command -v setsid >/dev/null 2>&1 || stop',
                                                                     ': "$PROBE6_UNDEFINED_FOR_TEST"\ncommand -v setsid >/dev/null 2>&1 || stop'))
    fd_u = fake_dir(pre + '_fake_unexp', pin_u)
    r23 = run_wrapper(repo_u, pin_u, home, 's23', wrapper_env(home, fd_u))
    stp = read_text(os.path.join(r23.lg, 'STOPPED')) if os.path.exists(os.path.join(r23.lg, 'STOPPED')) else ''
    stops.append(('감시 셸이 러너 시작 전에 뜻밖에 끝남', 2 if r23.rc != 0 else 0,
                  'the watcher ended unexpectedly' in stp and 'runner_started=0' in stp and not os.path.exists(lock)
                  and 'runner not started' in stop_line(r23), stop_line(r23)[-170:]))
    # 이번 고침의 멈춤 (P6R2-04 짝 · 로그 폴더 자리 · P6R2-01 시도 2 앞 조건): 이 홈에는 멈춘 시도 1 폴더뿐이다
    stop_case('시도 1 · 한도 1500000 (짝이 아님 · P6R2-04)', 'attempt 1 runs with maxiter 30000', run_wrapper(repo, pin, home, 's24', env2, maxiter=A2))
    stop_case('시도 2 · 한도 30000 (짝이 아님 · P6R2-04)', 'attempt 2 runs with maxiter 1500000',
              run_wrapper(repo, pin, home, 's25', env2, maxiter=A1, attempt=2))
    stop_case('로그 폴더가 홈 바로 밑이 아님 (앞 시도를 못 본다)', 'log folder must be directly in the home folder',
              run_wrapper(repo, pin, home, 's26', env2, lg=os.path.join(home, 'sub', 'p6log_a1_s26')))
    stop_case('시도 2 인데 끝난 시도 1 이 없음 (멈춘 시도 1 폴더뿐 · P6R2-01)', 'attempt 2 needs exactly one',
              run_wrapper(repo, pin, home, 's27', env2, attempt=2))
    calls1 = len(read_text(os.path.join(fd, 'calls.txt')).splitlines())
    n_calls_t = sum(len(read_text(os.path.join(x, 'calls.txt')).splitlines()) for x in (fd_t, fd_g, fd_u) if os.path.exists(os.path.join(x, 'calls.txt')))
    chk('F08a 멈춤 조건 %d 가지: 전부 rc 2 · 화면의 STOP 줄 = 그 사유 · "runner not started" · 로그 폴더를 받은 뒤면 STOPPED (사유 · runner_started=0)'
        % len(stops), len(stops) == 31 and all(rc == 2 and hit for _n, rc, hit, _l in stops), [s for s in stops if not (s[1] == 2 and s[2])])
    chk('F08b 멈춤 = 러너를 부르지 않았다 (호출 수 그대로) · 앞 시도의 로그 폴더는 그대로 · 잠금은 남이 쥔 것이면 그대로 둔다',
        calls1 == calls0 and n_calls_t == 0 and sorted(os.listdir(r.lg)) == f01_files and lock_kept
        and not os.path.exists(os.path.join(home, 'sdcp', 'ca1_probe6_a1_s3_arm1')), (calls0, calls1, n_calls_t, lock_kept))
    # F19 끝난 시도 번호 · 시도 2 앞 조건 (P6R2-01 · 02 · 원장의 감시 셸 줄을 손으로 부른 꼴): 합성 로그 폴더 (홈마다 따로)
    stops19 = []
    cases19 = (
        ('시도 1 이 끝남 (DONE · solve_started=1) → 시도 1 다시', [('p6log_a1_20991231T000001Z', lf_done(1, pin))], 1, 'attempt 1 already ran to the end'),
        ('시도 1 = WATCHER_FAILED · 러너 시작 줄 있음 → 시도 1 다시', [('p6log_a1_20991231T000001Z', LF_WF_START)], 1, 'attempt 1 already ran to the end'),
        ('시도 2 가 끝남 (DONE · solve_started=1) → 시도 1', [('p6log_a2_20991231T000001Z', lf_done(2, pin))], 1, 'attempt 1 does not run after attempt 2'),
        ('시도 2 가 끝남 → 시도 2 다시', [('p6log_a1_20991231T000001Z', lf_done(1, pin)), ('p6log_a2_20991231T000002Z', lf_done(2, pin))], 2,
         'attempt 2 already ran to the end'),
        ('시도 2 = WATCHER_FAILED · 러너 시작 줄 있음 → 시도 2 다시', [('p6log_a1_20991231T000001Z', lf_done(1, pin)),
                                                         ('p6log_a2_20991231T000002Z', LF_WF_START)], 2, 'attempt 2 already ran to the end'),
        ('시도 1 = DONE · solve_started=0 뿐 → 시도 2', [('p6log_a1_20991231T000001Z', lf_done(1, pin, solve=0))], 2, 'attempt 2 needs exactly one'),
        ('시도 1 = WATCHER_FAILED 뿐 (끝난 시도지만 DONE 아님) → 시도 2', [('p6log_a1_20991231T000001Z', LF_WF_START)], 2, 'attempt 2 needs exactly one'),
        ('끝난 시도 1 이 둘 → 시도 2', [('p6log_a1_20991231T000001Z', lf_done(1, pin)), ('p6log_a1_20991231T000002Z', lf_done(1, pin))], 2,
         'attempt 2 needs exactly one'),
        ('끝 표지 없는 앞 로그 폴더 (감시 셸이 아직 돌거나 죽음)', [('p6log_a1_20991231T000001Z', {'nohup.out': ''})], 1, 'has no end marker'))
    for i, (label, folders, att, needle) in enumerate(cases19):
        h = make_home('%s_h19_%d' % (pre, i))
        for nm, files in folders:
            log_folder(h, nm, files)
        r19 = run_wrapper(repo, pin, h, 'f19', wrapper_env(h, fd), attempt=att)
        line = stop_line(r19)
        mk = read_text(os.path.join(r19.lg, 'STOPPED')) if os.path.exists(os.path.join(r19.lg, 'STOPPED')) else ''
        stops19.append((label, r19.rc == 2 and needle in line and 'runner not started' in line and needle in mk
                        and not os.path.exists(os.path.join(h, '.probe6.lock')), line[-200:] or r19.so[-200:]))
    calls2 = len(read_text(os.path.join(fd, 'calls.txt')).splitlines())
    chk('F19a 앞 시도 %d 꼴: 끝난 번호 (DONE · solve_started=1 · WATCHER_FAILED + 러너 시작 줄) 다시 · a2 뒤 시도 1 · 시도 2 앞 조건 (끝난 시도 1 '
        '= DONE · solve_started=1 하나) · 끝 표지 없음 = 감시 셸 STOP (STOPPED · 잠금 풂) · 러너 호출 0' % len(stops19),
        len(stops19) == 9 and all(ok for _l, ok, _w in stops19) and calls2 == calls1, [s for s in stops19 if not s[1]])
    h = make_home(pre + '_h19ok')
    for nm, files in (('p6log_a1_20991231T000001Z', LF_STOPPED), ('p6log_a1_20991231T000002Z', lf_done(1, pin, solve=0)),
                      ('p6log_a1_20991231T000003Z', LF_WF_NOSTART), ('p6log_a2_20991231T000004Z', LF_STOPPED)):
        log_folder(h, nm, files)
    r = run_wrapper(repo, pin, h, 'f19ok', wrapper_env(h, fd, PROBE6_FAKE_SLEEP='1'))
    chk('F19b 세지 않는 앞 폴더 (STOPPED · DONE 의 solve_started=0 · 러너 시작 줄 없는 WATCHER_FAILED · 멈춘 a2) 만 있으면 시도 1 이 돈다 (DONE · 원장 §3)',
        r.rc == 0 and os.path.exists(os.path.join(r.lg, 'DONE')) and (r.rep or {}).get('verdict') == 'PROBE_OK', (r.rc, stop_line(r), r.so[-300:]))
    # F20 시도 2 의 풀이 코드 = 시도 1 의 것 (P6R2-03): 고정물 저장소에 커밋 셋 (풀이 코드 바뀜 · 원장 글만 바뀜 · 남남 커밋)
    repo2, pa = make_pin_repo(pre + '_pin2')

    def commit_on(base, relpath, text, msg):
        git(repo2, 'checkout', '-q', '--detach', base)
        write_text(os.path.join(repo2, relpath), text, 0o755 if relpath.endswith('.sh') else None)
        git(repo2, 'add', '-A')
        git(repo2, 'commit', '-q', '-m', msg)
        return git(repo2, 'rev-parse', 'HEAD')
    pb = commit_on(pa, RUNNER_REL, read_text(os.path.join(repo2, RUNNER_REL)) + '# changed solve code\n', 'runner change')
    pc = commit_on(pa, 'docs/reviews/rint2_dev_probe_ledger_20261026.md', '# attempt 1 result line (ledger only)\n', 'ledger line')
    po = git(repo2, 'commit-tree', '-m', 'unrelated history', pa + '^{tree}')
    res20 = []
    for label, p1, p2, needle in (('러너 (scripts/) 가 바뀐 핀', pa, pb, 'the solve code changed'),
                                  ('시도 1 의 핀이 이 핀의 앞 커밋이 아님 (남남 · 트리는 같음)', po, pa, 'not this PIN or an earlier commit')):
        git(repo2, 'checkout', '-q', '--detach', p2)
        h = make_home('%s_h20_%d' % (pre, len(res20)))
        log_folder(h, 'p6log_a1_20991231T000001Z', lf_done(1, p1))
        r20 = run_wrapper(repo2, p2, h, 'f20', wrapper_env(h, fake_dir('%s_fake20_%d' % (pre, len(res20)), p2)), attempt=2)
        line = stop_line(r20)
        res20.append((label, r20.rc == 2 and needle in line and 'runner not started' in line
                      and (needle != 'the solve code changed' or RUNNER_REL in line), line[-220:] or r20.so[-200:]))
    chk('F20a 시도 2 의 핀과 시도 1 의 핀 사이에 풀이 코드가 바뀜 → STOP (바뀐 파일 이름을 찍음) · 시도 1 의 핀이 앞 커밋이 아님 → STOP',
        all(ok for _l, ok, _w in res20), res20)
    git(repo2, 'checkout', '-q', '--detach', pc)
    h = make_home(pre + '_h20ok')
    log_folder(h, 'p6log_a1_20991231T000001Z', lf_done(1, pa))
    r = run_wrapper(repo2, pc, h, 'f20ok', wrapper_env(h, fake_dir(pre + '_fake20ok', pc), PROBE6_FAKE_SLEEP='1'), attempt=2)
    chk('F20b 원장 글만 바뀐 뒤 커밋 (풀이 코드 같음) → 시도 2 가 돈다 · meta attempt1_pin = 시도 1 의 핀 · code_same_as_attempt1=1 · 한도 1500000 · PROBE_OK',
        r.rc == 0 and os.path.exists(os.path.join(r.lg, 'DONE')) and r.meta.get('attempt1_pin') == pa and r.meta.get('code_same_as_attempt1') == '1'
        and r.meta.get('maxiter') == A2 and r.meta.get('attempt') == '2' and (r.rep or {}).get('verdict') == 'PROBE_OK',
        (r.rc, stop_line(r), dict((k, r.meta.get(k)) for k in ('attempt1_pin', 'code_same_as_attempt1', 'maxiter')), (r.rep or {}).get('problems')))
    # F21 작업 제어가 켜진 채 뜬 감시 셸 (P6R2-06): SHELLOPTS 의 monitor · BASH_ENV 의 set -m → set +m · 러너는 자기 세션의 우두머리 · 러너가 끝난 뒤 DONE
    bash_env_m = os.path.join(TD, pre + '_bashenv_m.sh')
    write_text(bash_env_m, 'set -m\n')
    for i, (label, extra) in enumerate((('SHELLOPTS 에 monitor', {'SHELLOPTS': 'braceexpand:hashall:interactive-comments:monitor'}),
                                        ('BASH_ENV 에 set -m', {'BASH_ENV': bash_env_m}))):
        h = make_home('%s_h21_%d' % (pre, i))
        fdj = fake_dir('%s_fake21_%d' % (pre, i), pin)
        r = run_wrapper(repo, pin, h, 'f21', wrapper_env(h, fdj, PROBE6_FAKE_SLEEP='4', **extra))
        rp = read_pid(os.path.join(fdj, 'runner.pid'))
        alive_after = proc_alive(rp) if rp > 1 else None
        renv_j = dict(ln.split('=', 1) for ln in read_text(os.path.join(fdj, 'runner_env.txt')).splitlines() if '=' in ln) \
            if os.path.exists(os.path.join(fdj, 'runner_env.txt')) else {}
        chk('F21%s 작업 제어가 켜진 채 뜬 감시 셸 (%s): 러너가 끝난 뒤 DONE (wall ≥ 4 s) · PROBE_OK · DONE 뒤 러너 없음 · 러너 env 에 SHELLOPTS · BASH_ENV 없음'
            % ('ab'[i], label),
            r.rc == 0 and os.path.exists(os.path.join(r.lg, 'DONE')) and int(r.meta.get('wall_s', -1)) >= 4
            and (r.rep or {}).get('verdict') == 'PROBE_OK' and alive_after is False and 'SHELLOPTS' not in renv_j and 'BASH_ENV' not in renv_j,
            (r.rc, r.meta.get('wall_s'), (r.rep or {}).get('verdict'), alive_after, r.so[-300:]))
        safe_kill(rp)
    repo_m, pin_m = make_pin_repo(pre + '_pin_jobctl', wrapper_patch=('RUNNER_STARTED=1\nsetsid ', 'RUNNER_STARTED=1\nset -m\nsetsid '))
    fdm = fake_dir(pre + '_fake_jobctl', pin_m)
    h = make_home(pre + '_h21m')
    r = run_wrapper(repo_m, pin_m, h, 'f21m', wrapper_env(h, fdm, PROBE6_FAKE_SLEEP='4'))
    wf = read_text(os.path.join(r.lg, 'WATCHER_FAILED')) if os.path.exists(os.path.join(r.lg, 'WATCHER_FAILED')) else ''
    st21 = read_text(os.path.join(r.lg, 'status.log')) if os.path.exists(os.path.join(r.lg, 'status.log')) else ''
    chk('F21c (둘째 겹) 띄우기 바로 앞에서 작업 제어를 켠 사본 (시험 전용): 러너가 자기 세션의 우두머리가 아님 → WATCHER_FAILED (사유 · runner_started=1) · '
        'DONE 없음 · 잠금 남김 · 러너 시작 줄은 있다 (끝난 시도로 센다)',
        'runner_started=1' in wf and 'session' in wf and not os.path.exists(os.path.join(r.lg, 'DONE'))
        and os.path.isdir(os.path.join(h, '.probe6.lock')) and ' runner started - maxiter ' in st21, (r.rc, wf, st21[-500:]))
    safe_kill(read_pid(os.path.join(fdm, 'runner.pid')))
    # F22 ★ 11-13 시도 3 · 4 (원장 §3 · 탄소 접합 원장 저장본 켬): 시도 3 = 빈 저장본 → 짓고 씀 · 시도 4 = 시도 3 이 남긴 저장본 → 적중
    h22 = make_home(pre + '_h22')
    for nm, files in (('p6log_a1_20991231T000001Z', lf_done(1, pin)), ('p6log_a2_20991231T000002Z', lf_done(2, pin))):
        log_folder(h22, nm, files)
    fd22 = fake_dir(pre + '_fake22', pin)
    r3 = run_wrapper(repo, pin, h22, 'f22', wrapper_env(h22, fd22, PROBE6_FAKE_SLEEP='1'), attempt=3)
    store22 = os.path.join(h22, 'p6_cjstore')
    regf = os.path.join(store22, 'cjreg_%s.npz' % FAKE_KEY)
    rsha = sha256_file(regf) if os.path.exists(regf) else None
    renv22 = dict(ln.split('=', 1) for ln in read_text(os.path.join(fd22, 'runner_env.txt')).splitlines() if '=' in ln) \
        if os.path.exists(os.path.join(fd22, 'runner_env.txt')) else {}
    cmd22 = read_text(os.path.join(r3.lg, 'command.txt')).splitlines() if os.path.exists(os.path.join(r3.lg, 'command.txt')) else []
    st3 = ((r3.rep or {}).get('store') or {})
    bp3 = bundle_problems(r3.lg, T_SEALED, h22)
    chk('F22a 시도 3 (끝난 시도 2 뒤 · 저장본 없음): 감시 셸 rc 0 · PROBE_OK · 저장본 폴더를 만들었다 (0755) · 러너 env CJUNC_STORE = ~/p6_cjstore 의 실제 경로 · '
        'command.txt = 원장 꼴 (CJUNC_STORE 를 ~ 로 접음 · 홈 경로 없음) · meta attempt 3 · attempt2_pin · 저장본 목록 (앞 빔 · 끝 = 짓고 쓴 파일) · '
        '보고 상태 built_written · 묶음 꼴',
        r3.rc == 0 and (r3.rep or {}).get('verdict') == 'PROBE_OK' and os.path.isdir(store22)
        and (os.stat(store22).st_mode & 0o777) == 0o755 and renv22.get('CJUNC_STORE') == os.path.join(h22, 'p6_cjstore')
        and len(cmd22) == 2 and cmd22[1] == runner_cmd_line_store(STORE_ATTEMPTS[3], outdir='~/sdcp/ca1_probe6_a3_f22_arm1', w=repo)
        and r3.meta.get('attempt') == '3' and r3.meta.get('attempt2_pin') == pin and r3.meta.get('store') == '~/p6_cjstore'
        and r3.meta.get('store_listing_before') == '' and r3.meta.get('store_listing_after') == 'cjreg_%s.npz:%s' % (FAKE_KEY, rsha)
        and st3.get('status') == 'built_written' and 'attempt1_pin' not in r3.meta and bp3 == [],
        (r3.rc, stop_line(r3), (r3.rep or {}).get('problems'), renv22.get('CJUNC_STORE'), cmd22[1:], bp3[:4],
         dict((k, r3.meta.get(k)) for k in ('attempt', 'attempt2_pin', 'store', 'store_listing_before', 'store_listing_after'))))
    r4 = run_wrapper(repo, pin, h22, 'f22b', wrapper_env(h22, fd22, PROBE6_FAKE_SLEEP='1'), attempt=4)
    st4 = ((r4.rep or {}).get('store') or {})
    chk('F22b 시도 4 (같은 홈 · 끝난 시도 3 뒤): 감시 셸 rc 0 · PROBE_OK · 상태 hit · meta attempt3_pin · code_same_as_attempt3=1 · 저장본 목록 앞 = 끝 = 시도 3 의 끝 · '
        '가짜 러너가 본 상태 차례 = built_written → hit · 저장본 파일 그대로',
        r4.rc == 0 and (r4.rep or {}).get('verdict') == 'PROBE_OK' and st4.get('status') == 'hit' and r4.meta.get('attempt3_pin') == pin
        and r4.meta.get('code_same_as_attempt3') == '1' and r4.meta.get('store_listing_before') == r3.meta.get('store_listing_after')
        and r4.meta.get('store_listing_after') == r3.meta.get('store_listing_after')
        and os.path.exists(os.path.join(fd22, 'store_status.txt')) and read_text(os.path.join(fd22, 'store_status.txt')).split() == ['built_written', 'hit']
        and rsha is not None and sha256_file(regf) == rsha,
        (r4.rc, stop_line(r4), (r4.rep or {}).get('problems'), st4))
    stops22 = []

    def stop22(label, att, needle, folders, prep=None, env_over=None, maxiter=None, rp=None):
        h = make_home('%s_h22s_%d' % (pre, len(stops22)))
        for nm, files in folders:
            log_folder(h, nm, files)
        if prep:
            prep(h)
        fdx = fake_dir('%s_fake22s_%d' % (pre, len(stops22)), (rp or (repo, pin))[1])
        r_ = run_wrapper((rp or (repo, pin))[0], (rp or (repo, pin))[1], h, 'f22s', wrapper_env(h, fdx, **(env_over or {})), attempt=att,
                         maxiter=maxiter)
        line = stop_line(r_)
        called = os.path.exists(os.path.join(fdx, 'calls.txt'))
        stops22.append((label, r_.rc == 2 and needle in line and 'runner not started' in line and not called, line[-220:] or r_.so[-220:]))
    a1, a2 = ('p6log_a1_20991231T000001Z', lf_done(1, pin)), ('p6log_a2_20991231T000002Z', lf_done(2, pin))

    def a3done(listing):
        d_ = lf_done(3, pin)
        d_['meta.txt'] += 'store_listing_after=%s\n' % listing
        return ('p6log_a3_20991231T000003Z', d_)
    good_list = 'cjreg_%s.npz:%s' % (FAKE_KEY, hashlib.sha256(b'fake registry\n').hexdigest())

    def put_store(h, body=b'fake registry\n'):
        os.makedirs(os.path.join(h, 'p6_cjstore'))
        with open(os.path.join(h, 'p6_cjstore', 'cjreg_%s.npz' % FAKE_KEY), 'wb') as fh:
            fh.write(body)
    stop22('시도 3 · 끝난 시도 2 없음', 3, 'attempt 3 needs exactly one attempt-2', [a1])
    stop22('시도 3 · 저장본에 남은 파일', 3, 'attempt 3 needs an absent or empty store folder', [a1, a2], prep=put_store)
    stop22('시도 3 · 저장본이 심볼릭 링크', 3, 'symbolic link', [a1, a2],
           prep=lambda h: (os.makedirs(os.path.join(h, 'real_store')), os.symlink(os.path.join(h, 'real_store'), os.path.join(h, 'p6_cjstore'))))
    stop22('시도 3 · 한도 30000 (짝 아님)', 3, 'registered pairs', [a1, a2], maxiter=A1)
    stop22('시도 3 · 끝난 시도 4 뒤', 3, 'attempt 3 does not run after attempt 4', [a1, a2, ('p6log_a4_20991231T000009Z', lf_done(4, pin))])
    stop22('시도 2 · 끝난 시도 3 뒤', 2, 'attempt 2 does not run after attempt 3', [a1, a3done(good_list)])
    stop22('시도 4 · 끝난 시도 3 없음', 4, 'attempt 4 needs exactly one attempt-3', [a1, a2])
    stop22('시도 4 · 저장본 없음', 4, 'attempt 4 needs the store folder', [a1, a2, a3done(good_list)])
    stop22('시도 4 · 저장본이 시도 3 이 남긴 것과 다름', 4, 'differs from what attempt 3 left', [a1, a2, a3done(good_list)],
           prep=lambda h: put_store(h, b'other registry\n'))
    stop22('시도 4 · 시도 3 meta 에 저장본 목록 없음', 4, 'no store listing', [a1, a2, ('p6log_a3_20991231T000003Z', lf_done(3, pin))],
           prep=put_store)
    stop22('시도 3 · GIT_GRAFT_FILE 이 걸림', 3, 'GIT_GRAFT_FILE', [a1, a2], env_over={'GIT_GRAFT_FILE': os.path.join(TD, 'no_graft')})
    sh_repo = os.path.join(TD, pre + '_pin_shallow')
    subprocess.run(['git', 'clone', '-q', '--depth', '1', 'file://' + repo2, sh_repo], check=True, capture_output=True,
                   env=_rc().git_fixture_env())
    stop22('시도 3 · 핀 작업 트리가 얕은 복제 (커밋 여럿인 저장소의 depth 1)', 3, 'shallow clone', [a1, a2], rp=(sh_repo, git(sh_repo, 'rev-parse', 'HEAD')))
    calls22 = len(read_text(os.path.join(fd22, 'calls.txt')).splitlines()) if os.path.exists(os.path.join(fd22, 'calls.txt')) else 0
    chk('F22c 시도 3 · 4 멈춤 %d 꼴 (앞 시도 · 저장본 남음 · 링크 · 짝 · 뒤 시도 끝남 · 시도 4 앞 조건 · 저장본 없음 · 다름 · 목록 없음 · graft · shallow): '
        '전부 rc 2 · 그 사유 · 러너 호출 0' % len(stops22),
        len(stops22) == 12 and all(ok for _l, ok, _w in stops22) and calls22 == 2, [x for x in stops22 if not x[1]])
    git(repo2, 'checkout', '-q', '--detach', pb)
    h = make_home(pre + '_h22code')
    for nm, files in (('p6log_a1_20991231T000001Z', lf_done(1, pa)), ('p6log_a2_20991231T000002Z', lf_done(2, pa))):
        log_folder(h, nm, files)
    d3 = lf_done(3, pa)
    d3['meta.txt'] += 'store_listing_after=%s\n' % good_list
    log_folder(h, 'p6log_a3_20991231T000003Z', d3)
    put_store(h)
    r_ = run_wrapper(repo2, pb, h, 'f22code', wrapper_env(h, fake_dir(pre + '_fake22code', pb)), attempt=4)
    chk('F22d 시도 3 의 핀과 시도 4 의 핀 사이에 풀이 코드가 바뀜 → STOP (바뀐 파일 이름) · 러너 시작 안 함',
        r_.rc == 2 and 'the solve code changed between the attempt-3 pin' in stop_line(r_) and RUNNER_REL in stop_line(r_), stop_line(r_) or r_.so[-300:])
    # F23 ★ 11-13 감시 셸의 git 읽기 = 봉인용 (Codex 반박 1/2 §3): 부르는 쪽 GIT_DIR (남의 저장소) 를 지운다 · 러너에 GIT_NO_REPLACE_OBJECTS=1
    vic, vpin = make_pin_repo(pre + '_victim')
    h = make_home(pre + '_h23')
    fd23 = fake_dir(pre + '_fake23', pin)
    r_ = run_wrapper(repo, pin, h, 'f23', wrapper_env(h, fd23, PROBE6_FAKE_SLEEP='1', GIT_DIR=os.path.join(vic, '.git'),
                                                       GIT_WORK_TREE=vic))
    renv23 = dict(ln.split('=', 1) for ln in read_text(os.path.join(fd23, 'runner_env.txt')).splitlines() if '=' in ln) \
        if os.path.exists(os.path.join(fd23, 'runner_env.txt')) else {}
    chk('F23 부르는 쪽 GIT_DIR · GIT_WORK_TREE = 남의 저장소: 감시 셸이 지우고 핀 작업 트리를 읽는다 (rc 0 · PROBE_OK · git_lines_after 0) · 러너 env 에 GIT_DIR · '
        'GIT_WORK_TREE 없음 · GIT_NO_REPLACE_OBJECTS=1 · 남의 저장소 HEAD 그대로',
        r_.rc == 0 and (r_.rep or {}).get('verdict') == 'PROBE_OK' and 'GIT_DIR' not in renv23 and 'GIT_WORK_TREE' not in renv23
        and renv23.get('GIT_NO_REPLACE_OBJECTS') == '1' and git(vic, 'rev-parse', 'HEAD') == vpin,
        (r_.rc, stop_line(r_), r_.so[-300:]))
    # F09 실패 경로 (러너 rc 1 · 팔 없음 · .failed 남음 = 시도 1 이 한도에 닿은 꼴)
    r = run_wrapper(repo, pin, home, 'fail', wrapper_env(home, fd, PROBE6_FAKE_MODE='fail'))
    left = os.path.join(home, 'sdcp', KIT, S0_RUN, ARM + '.json.failed')
    bp = bundle_problems(r.lg, T_SEALED, home)
    chk('F09a 실패 경로 (시도 1 이 한도에 닿음): 감시 셸 rc 1 · 러너 rc 1 · 판독 rc 3 (미수렴) · 정상 끝 = DONE · 묶음 꼴 · 누출 없음',
        r.rc == 1 and r.meta.get('runner_rc') == '1' and (r.rep or {}).get('rc') == 3 and bp == []
        and 'runner_rc=1 report_rc=3 attempt=1' in read_text(os.path.join(r.lg, 'DONE')),
        (r.rc, r.meta.get('runner_rc'), (r.rep or {}).get('rc'), bp[:4], (r.rep or {}).get('problems')))
    chk('F09b 실패 보존: 남은 파일 · 출력 폴더 · 원문 로그 그대로 · 화면에 σ 류 수 없음',
        os.path.exists(left) and os.path.isdir(r.out) and os.path.exists(os.path.join(r.lg, 'runner.log'))
        and scan_hits([r.so, r.se], T_SEALED, sd_min=4, floats_only=True) == [], '')
    cpy = os.path.join(r.lg, 'kit_run_new', ARM + '.json.failed')
    knew = dict((x['name'], x) for x in (r.rep or {}).get('kit_run_new_files') or [])
    names, _m = bundle_members(r.lg)
    chk('F09c 킷 런 폴더의 새 파일 = 로그 폴더에 바이트 사본 (kit_run_new · sha256 같음 · 보고 copy_ok) · 묶음에는 없다',
        os.path.exists(cpy) and sha256_file(cpy) == sha256_file(left) and (knew.get(ARM + '.json.failed') or {}).get('copy_ok') is True
        and not [n for n in (names or []) if 'kit_run' in n], (os.path.exists(cpy), knew))
    doc = json.loads(read_text(left))
    doc['zz_earlier_attempt'] = 1                                       # 앞 시도의 남은 파일 ≠ 이번 시도가 쓸 것 (덮기 전 사본인지 가른다)
    write_text(left, json.dumps(doc))
    old_sha = sha256_file(left)
    os.utime(left, (time.time() - 30, time.time() - 30))
    unmoved = os.path.join(home, 'sdcp', KIT, S0_RUN, ARM + '.json')
    shutil.copy(os.path.join(fd, 'arm.json'), unmoved)                  # 앞 시도가 옮기지 못한 팔 (같은 이름 · 다음 시도가 덮을 자리)
    os.utime(unmoved, (time.time() - 30, time.time() - 30))
    um_sha = sha256_file(unmoved)
    # F09d 다음 시도 = 시도 2 (같은 홈 · 시도 1 = 위 F09 · 한도 1500000 · 시도 1 의 핀 = 이 핀)
    r = run_wrapper(repo, pin, home, 'again', wrapper_env(home, fd, PROBE6_FAKE_MODE='fail', PROBE6_FAKE_SLEEP='1'), attempt=2)
    bl = dict((x.get('name'), x.get('sha256')) for x in (r.rep or {}).get('kit_run_before_files') or [])
    bef = os.path.join(r.lg, 'kit_run_before')
    renv2 = dict(ln.split('=', 1) for ln in read_text(os.path.join(fd, 'runner_env.txt')).splitlines() if '=' in ln)
    chk('F09d 시도 2: 러너가 같은 이름으로 덮어쓰기 전에 앞 시도의 남은 파일 (.failed · 옮겨지지 않은 .json) 을 사본으로 (kit_run_before · sha256 = 앞 것)',
        os.path.exists(os.path.join(bef, ARM + '.json.failed')) and sha256_file(os.path.join(bef, ARM + '.json.failed')) == old_sha
        and os.path.exists(os.path.join(bef, ARM + '.json')) and sha256_file(os.path.join(bef, ARM + '.json')) == um_sha
        and bl.get(ARM + '.json.failed') == old_sha and r.meta.get('kit_run_before') == '2', (sorted(bl), r.meta.get('kit_run_before')))
    chk('F09e 시도 2 의 판독기는 앞 시도의 팔을 읽지 않는다 (출처 = 이 시도의 .failed · 옮겨지지 않은 옛 .json 은 새 파일 아님) · 판독 rc 3 · '
        'meta attempt 2 · maxiter 1500000 (러너 P2_EXTRA 도) · attempt1_pin = 시도 1 의 핀 · code_same_as_attempt1=1',
        (r.rep or {}).get('source') == 'kit_run_failed' and ARM + '.json' not in [x.get('name') for x in (r.rep or {}).get('kit_run_new_files') or []]
        and (r.rep or {}).get('rc') == 3 and r.meta.get('attempt') == '2' and r.meta.get('maxiter') == A2
        and renv2.get('P2_EXTRA') == '--step3-maxiter ' + A2 and r.meta.get('attempt1_pin') == pin and r.meta.get('code_same_as_attempt1') == '1',
        ((r.rep or {}).get('source'), (r.rep or {}).get('rc'), (r.rep or {}).get('problems'), stop_line(r),
         dict((k, r.meta.get(k)) for k in ('attempt', 'maxiter', 'attempt1_pin', 'code_same_as_attempt1'))))
    os.remove(left)
    os.remove(unmoved)
    # F10 상한 (PROBE6_CAP_GB=0 → 첫 표본에서 끝낸다) · 시도 1 마다 따로 홈 (끝난 시도 1 이 같은 홈의 다음 시도 1 을 막는다)
    hc = make_home(pre + '_home_cap')
    t0 = time.time()
    r = run_wrapper(repo, pin, hc, 'cap', wrapper_env(hc, fd, PROBE6_FAKE_MODE='big', PROBE6_CAP_GB='0'))
    chk('F10 메모리 상한: 러너 그룹을 끝내고 기록 (cap_term 1 · 러너 rc ≠ 0) · 30 초 안 · 감시 셸 rc 1 · 판독 rc 4 · 묶음 · DONE',
        r.rc == 1 and r.meta.get('cap_term') == '1' and r.meta.get('runner_rc') not in ('0', None) and time.time() - t0 < 30
        and (r.rep or {}).get('rc') == 4 and bundle_members(r.lg)[0] is not None and os.path.exists(os.path.join(r.lg, 'DONE')),
        (r.rc, r.meta.get('cap_term'), time.time() - t0, r.so[-400:]))

    def term_run(tag, mode, extra=None, wait_line=None, second=False):
        hh = make_home('%s_home_%s' % (pre, tag))
        out = os.path.join(hh, 'sdcp', 'ca1_probe6_a1_%s_arm1' % tag)
        lg = os.path.join(hh, 'p6log_a1_%s' % tag)
        os.makedirs(lg)
        for nm in ('child.pid', 'runner.pid'):
            if os.path.exists(os.path.join(fd, nm)):
                os.remove(os.path.join(fd, nm))
        p = subprocess.Popen(['bash', os.path.join(repo, TOOLS_REL, 'run_probe6.sh'), repo, out, lg, pin, A1],
                             env=wrapper_env(hh, fd, PROBE6_FAKE_MODE=mode, **(extra or {})), stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True)
        for _ in range(300):
            st = read_text(os.path.join(lg, 'status.log')) if os.path.exists(os.path.join(lg, 'status.log')) else ''
            if (wait_line or 'runner started') in st and (mode not in ('hang', 'stubborn') or os.path.exists(os.path.join(fd, 'child.pid'))):
                break
            time.sleep(0.1)
        if mode == 'unbuf':                                    # 러너가 flush 없이 찍은 줄을 기다린다 (최대 10 초 · 버퍼에 갇히면 끝내 안 나온다)
            for _ in range(100):
                rl = os.path.join(lg, 'runner.log')
                if os.path.exists(rl) and 'CG not converged' in read_text(rl):
                    break
                time.sleep(0.1)
        time.sleep(1.0)
        p.send_signal(signal.SIGTERM)
        if second:
            for _ in range(200):
                st = read_text(os.path.join(lg, 'status.log')) if os.path.exists(os.path.join(lg, 'status.log')) else ''
                if 'runner ended' in st:
                    break
                time.sleep(0.1)
            time.sleep(1.0)
            try:
                p.send_signal(signal.SIGTERM)
            except OSError:
                pass
        try:
            so, _se = p.communicate(timeout=90)
        except subprocess.TimeoutExpired:
            p.kill()
            so, _se = p.communicate()
        r2 = Res()
        r2.rc, r2.so, r2.lg, r2.out, r2.home = p.returncode, so or '', lg, out, hh
        r2.meta = read_meta(lg)
        rp = os.path.join(lg, 'probe6_report.json')
        r2.rep = json.loads(read_text(rp)) if os.path.exists(rp) else None
        r2.child, r2.runner = read_pid(os.path.join(fd, 'child.pid')), read_pid(os.path.join(fd, 'runner.pid'))
        return r2

    # F11 감시 셸에 TERM · TERM 을 무시하는 자식 (그룹 TERM → 10 초 → KILL)
    r = term_run('stub', 'stubborn')
    time.sleep(0.5)
    chk('F11 감시 셸에 TERM: TERM 을 무시하는 자식까지 그룹째 끝낸다 (KILL) · aborted 1 · 고아 0 · rc 1 · DONE · watcher.pid 지움 · 잠금 풂 · 판독 rc 4',
        r.child > 0 and not proc_alive(r.child) and r.meta.get('aborted') == '1' and r.meta.get('orphans') == '0'
        and r.meta.get('orphans_left') == '0' and r.rc == 1 and os.path.exists(os.path.join(r.lg, 'DONE'))
        and not os.path.exists(os.path.join(r.lg, 'watcher.pid')) and not os.path.exists(os.path.join(r.home, '.probe6.lock'))
        and (r.rep or {}).get('rc') == 4,
        (r.child, proc_alive(r.child) if r.child > 0 else None, r.meta.get('aborted'), r.meta.get('orphans'), r.rc, r.so[-300:]))
    safe_kill(r.child)
    # F12 러너 맨 위만 끝나고 그룹에 남은 자식 (러너가 정상 끝인데 자식이 남음 = 고아)
    ht = make_home(pre + '_home_tree')
    r = run_wrapper(repo, pin, ht, 'tree', wrapper_env(ht, fd, PROBE6_FAKE_MODE='tree'))
    child = read_pid(os.path.join(fd, 'child.pid'))
    dn = read_text(os.path.join(r.lg, 'DONE')) if os.path.exists(os.path.join(r.lg, 'DONE')) else ''
    chk('F12 러너가 끝난 뒤 그룹에 남은 자식: 세어 (orphans 1) 끝내고 (남은 것 0) · DONE 은 그 뒤 (orphans=1) · 판독 rc 4 (PROBE_OK 아님)',
        child > 0 and not proc_alive(child) and r.meta.get('orphans') == '1' and r.meta.get('orphans_left') == '0'
        and 'orphans=1' in dn and (r.rep or {}).get('rc') == 4, (child, r.meta.get('orphans'), r.meta.get('orphans_left'), dn, (r.rep or {}).get('rc')))
    safe_kill(child)
    # F13 일찍 멈춤: 러너가 flush 없이 찍은 한도 줄이 runner.log 에 남는다 (PYTHONUNBUFFERED=1) → 판독기가 info · 잔차 · 풀이 시작 → 끝 초를 낸다
    r = term_run('unbuf', 'unbuf', wait_line='runner started')
    raw = read_text(os.path.join(r.lg, 'runner.log')) if os.path.exists(os.path.join(r.lg, 'runner.log')) else ''
    lg_ = (r.rep or {}).get('log') or {}
    tm = (r.rep or {}).get('timing') or {}
    chk('F13 일찍 멈춤: flush 없이 찍힌 미수렴 줄이 남는다 · 판독 = info 30000 · 잔차 4.4e-07 · 풀이 시작 → 끝 초 (int) · 반복 수 칸 없음 · rc 4',
        'CG not converged (info=30000' in raw and lg_.get('not_converged_info') == 30000 and lg_.get('not_converged_resid') == 4.4e-07
        and isinstance(tm.get('solve_to_end_s'), int) and tm.get('solve_to_end_s') >= 0 and (r.rep or {}).get('rc') == 4
        and is_missing(((r.rep or {}).get('fields') or {}).get('cg_iters')), (raw[-200:], lg_.get('not_converged_info'), tm.get('solve_to_end_s')))
    # F14 러너가 핀 작업 트리를 더럽힘 → git_lines_after ≥ 1 · PROBE_OK 아님
    hd = make_home(pre + '_home_dirty')
    r = run_wrapper(repo, pin, hd, 'dirty', wrapper_env(hd, fd, PROBE6_FAKE_MODE='dirty'))
    chk('F14 런 뒤 핀 작업 트리가 더러움: meta git_lines_after ≥ 1 · 판독 rc 4 (meta git_lines_after 문제)',
        r.meta.get('git_lines_after') not in (None, '0') and (r.rep or {}).get('rc') == 4
        and any('git_lines_after' in x for x in (r.rep or {}).get('problems') or []), (r.meta.get('git_lines_after'), (r.rep or {}).get('problems')))
    if os.path.exists(os.path.join(repo, 'untracked_by_runner.txt')):
        os.remove(os.path.join(repo, 'untracked_by_runner.txt'))
    # F15 둘째 TERM 이 끝 기록 (판독기) 중에 와도 보고 · 묶음 · DONE 이 남는다
    r = term_run('twice', 'hang', extra={'PROBE6_FAKE_READER_SLEEP': '4'}, second=True)
    st = read_text(os.path.join(r.lg, 'status.log')) if os.path.exists(os.path.join(r.lg, 'status.log')) else ''
    chk('F15 둘째 TERM (끝 기록 중): 미룬다 · 보고 · 묶음 · DONE 이 남는다 · "held until the record was complete" 줄',
        os.path.exists(os.path.join(r.lg, 'DONE')) and r.rep is not None and bundle_members(r.lg)[0] is not None
        and 'held until the record was complete' in st and r.meta.get('aborted') == '1', (r.rc, st[-500:]))
    # F16 ps · nvidia-smi 가 실패해도 멈춤이 된다 (그룹 kill = /proc)
    write_text(os.path.join(fd, 'ps_fail'), '1')
    write_text(os.path.join(fd, 'smi_fail'), '1')
    r = term_run('psfail', 'hang')
    os.remove(os.path.join(fd, 'ps_fail'))
    os.remove(os.path.join(fd, 'smi_fail'))
    time.sleep(0.3)
    chk('F16 표본의 ps · nvidia-smi 가 실패해도: TERM 으로 러너 그룹을 끝낸다 · DONE · GPU 칸 = NA',
        r.child > 0 and not proc_alive(r.child) and os.path.exists(os.path.join(r.lg, 'DONE')) and r.meta.get('aborted') == '1'
        and '\tNA\tNA\tNA' in read_text(os.path.join(r.lg, 'samples.tsv')), (r.child, r.rc, r.so[-300:]))
    safe_kill(r.child)
    # F17 감시 셸이 러너 시작 뒤에 뜻밖에 끝남 (고친 사본 · 시험 전용) → 러너 그룹을 끝내고 WATCHER_FAILED · 잠금은 남긴다
    repo_x, pin_x = make_pin_repo(pre + '_pin_fail', wrapper_patch=('RPID=$!\n', 'RPID=$!\nsleep 2\n: "$PROBE6_UNDEFINED_FOR_TEST"\n'))
    fd_x = fake_dir(pre + '_fake_fail', pin_x)
    hx = make_home(pre + '_home_wfail')
    rx = run_wrapper(repo_x, pin_x, hx, 'wfail', wrapper_env(hx, fd_x, PROBE6_FAKE_MODE='hang'), timeout=120)
    ch = read_pid(os.path.join(fd_x, 'child.pid'))
    time.sleep(0.3)
    chk('F17 러너 시작 뒤 감시 셸이 뜻밖에 끝남: 러너 그룹 끝 · WATCHER_FAILED (runner_started=1) · DONE · STOPPED 없음 · 잠금 남음 (사람이 본다)',
        os.path.exists(os.path.join(rx.lg, 'WATCHER_FAILED')) and 'runner_started=1' in read_text(os.path.join(rx.lg, 'WATCHER_FAILED'))
        and not os.path.exists(os.path.join(rx.lg, 'DONE')) and not os.path.exists(os.path.join(rx.lg, 'STOPPED'))
        and os.path.isdir(os.path.join(hx, '.probe6.lock')) and ch > 0 and not proc_alive(ch) and 'WATCHER FAILED' in rx.so, (rx.rc, ch, rx.so[-300:]))
    safe_kill(ch)
    # F18 time -v 기록 (이 컨테이너에 /usr/bin/time 이 없어 가짜 time 을 쓰는 사본 · 시험 전용): 명령 줄 · 홈 경로는 묶음에 가지 않는다 (P6R-08)
    ftime = os.path.join(TD, pre + '_faketime.sh')
    write_text(ftime, FAKE_TIME, 0o755)
    repo_v, pin_v = make_pin_repo(pre + '_pin_timev', wrapper_patch=(
        'if [ -x /usr/bin/time ]; then\n  TV=1\n  TIMEV=(/usr/bin/time -v -o "$L/time_v.txt")',
        'if [ -x "${PROBE6_FAKE_TIME:-/nonexistent}" ]; then\n  TV=1\n  TIMEV=("$PROBE6_FAKE_TIME" -v -o "$L/time_v.txt")'))
    fd_v = fake_dir(pre + '_fake_timev', pin_v)
    hv = make_home(pre + '_home_timev')
    rv = run_wrapper(repo_v, pin_v, hv, 'timev', wrapper_env(hv, fd_v, PROBE6_FAKE_TIME=ftime))
    raw_tv = read_text(os.path.join(rv.lg, 'time_v.txt')) if os.path.exists(os.path.join(rv.lg, 'time_v.txt')) else ''
    _n, mem_v = bundle_members(rv.lg)
    bpv = bundle_problems(rv.lg, T_SEALED, hv)
    chk('F18 time -v 기록: 로그 폴더의 원본은 명령 줄 (홈 경로 포함) 그대로 · 묶음의 time_v.txt = 세 줄 (최대 RSS · 경과 · 종료 코드) · 묶음 꼴 통과 · 판독 rc 0',
        hv in raw_tv and 'Command being timed' in raw_tv and len(mem_v.get('time_v.txt', '').splitlines()) == 3
        and 'Command' not in mem_v.get('time_v.txt', '') and bpv == [] and rv.meta.get('time_v') == '1' and (rv.rep or {}).get('rc') == 0
        and ((rv.rep or {}).get('resources') or {}).get('time_v_max_rss_kb') == 12345, (rv.rc, bpv[:4], mem_v.get('time_v.txt', '')[:300]))


# ═════════════════════════ W: 감시 셸 변이 (고를 때만 · `--only W`) ═════════════════════════
#: 감시 셸을 한 군데씩 망가뜨린 사본으로 F 묶음을 다시 돌린다 (첫 실패에서 그 변이를 끝낸다).  지은이 변이 · 리뷰어 변이 13 (11-10 · mut_wrapper.py ·
#: 같은 뜻 · 고친 감시 셸의 자리) · 이번 고침의 새 검사 (F1 · F2 · F3 · F5 · F9 · F13).
_SCRUB = 'SIGMA_*|SDCP_*|PTFE_*|CJUNC*|STEP3_*|MPM_*|P2_*|LEAN|VOX|ARMS|ARM_LIST|KITS|FIBRE_STAMP|BRIDGE_UM|OUTDIR|EXPECT_PROTOCOL|EXPECT_BACKEND)'
WRAPPER_MUTANTS = (
    ('부모 셸의 축 env 를 걷지 않음', [('      unset "$n"\n', '      :\n')]),
    ('등록 축 값 하나를 바꿈 (R_j)', [('CJUNC=1 CJUNC_RJ=1e6 ', 'CJUNC=1 CJUNC_RJ=1e5 ')]),
    ('maxiter 인자를 러너에 넘기지 않음', [('"P2_EXTRA=--step3-maxiter $MAXITER"', '"P2_EXTRA=--step3-maxiter 400000"')]),
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
    ('킷 payload 줄의 --joule-heat · --save-step4-grid · --show-results 를 보지 않음', [('  if grep -q -e "$flag" "$K/run_mpm.sh" 2>/dev/null; then',
                                                                                     '  if false; then')]),
    ('차 있는 출력 폴더도 받음', [('{ [ -d "$O" ] && [ ! -L "$O" ] && [ -z "$(ls -A "$O" 2>/dev/null)" ]; } || stop', 'true || stop')]),
    ('옛 로그 폴더도 받음', [('  if [ "$(basename "$f")" != nohup.out ]; then', '  if false; then')]),
    ('킷 뿌리로 가지 않고 러너를 띄움', [('cd "$ROOT" || stop "cannot enter the kit root"', ':')]),
    ('신호를 받아도 러너 그룹을 끝내지 않음', [('      say "signal received - stopping the runner group"\n      group_stop\n',
                                                '      say "signal received - stopping the runner group"\n')]),
    ('메모리 상한에서 러너 그룹을 끝내지 않음', [('    say "host RSS cap reached ($((RS / 1048576)) GB >= $CAP GB) - stopping the runner group"\n    group_stop\n',
                                                  '    say "host RSS cap reached ($((RS / 1048576)) GB >= $CAP GB) - stopping the runner group"\n')]),
    ('킷 런 폴더의 새 파일을 사본으로 두지 않음', [('    mkdir -p "$L/kit_run_new" && cp "$f" "$L/kit_run_new/" && NNEW=$((NNEW + 1))',
                                                    '    NNEW=$((NNEW + 1))')]),
    ('앞 시도의 남은 파일을 사본으로 두지 않음', [('    mkdir -p "$L/kit_run_before" && cp "$f" "$L/kit_run_before/" || stop',
                                                  '    true || stop')]),
    ('cupy 를 못 불러와도 감', [("if grep -q '^cupy=ABSENT' \"$L/env.txt\"; then", 'if false; then')]),
    # 리뷰어 13 (P6R-10 · 고친 감시 셸의 같은 자리)
    ('리뷰 stderr 를 runner.log 로 돌리지 않음', [('bash "$RUNNER" > "$L/runner.log" 2>&1 < /dev/null &', 'bash "$RUNNER" > "$L/runner.log" < /dev/null &')]),
    ('리뷰 걷어내기 목록에서 FIBRE_STAMP 빠짐', [(_SCRUB, _SCRUB.replace('FIBRE_STAMP|', ''))]),
    ('리뷰 걷어내기 목록에서 SDCP_* 빠짐', [(_SCRUB, _SCRUB.replace('SDCP_*|', ''))]),
    ('리뷰 걷어내기 목록에서 PTFE_* 빠짐', [(_SCRUB, _SCRUB.replace('PTFE_*|', ''))]),
    ('리뷰 걷어내기 목록에서 EXPECT_PROTOCOL 빠짐', [(_SCRUB, _SCRUB.replace('EXPECT_PROTOCOL|', ''))]),
    ('리뷰 S0 계획 tol_ff 를 명령 값과 대조하지 않음', [('[ "$S0TOL" = "$TOL_FF" ] || stop', '[ -n "$S0TOL" ] || stop')]),
    ('리뷰 경로 글자 검사를 뺌', [('  okpath "$p" || stop', '  true || stop')]),
    ('리뷰 판독기를 -I 없이', [('python3 -I -B "$READER" --outdir', 'python3 -B "$READER" --outdir')]),
    ('리뷰 그룹 멈춤이 TERM 만 (KILL 없음)', [('  if [ "$(group_count)" -gt 0 ]; then kill -KILL -- "-$RPID" 2>/dev/null; sleep 1; fi\n', '  :\n')]),
    ('리뷰 상한 검사가 표본 RSS 를 안 봄', [('[ $((RS / 1048576)) -ge "$CAP" ]; then', '[ $((0 / 1048576)) -ge "$CAP" ] && [ "$CAP" -gt 0 ]; then')]),
    ('리뷰 앞 시도의 .json (옮겨지지 않은 팔) 을 사본으로 두지 않음', [('for f in "$RUNP"/p2_SBE_vgcf100_*.json "$RUNP"/p2_SBE_vgcf100_*.json.failed',
                                                                    'for f in "$RUNP"/p2_SBE_vgcf100_*.json.failed')]),
    ('리뷰 런 뒤 git 상태를 안 봄 (늘 0)', [('GIT_AFTER="$(git -C "$W" status --porcelain --untracked-files=all 2>/dev/null | grep -c .)"', 'GIT_AFTER=0')]),
    ('리뷰 meta 폴더를 절대 경로로', [('  echo "outdir=$(homerel "$O")"', '  echo "outdir=$O"')]),
    # 이번 고침의 새 검사
    ('러너를 자기 세션 · 그룹으로 띄우지 않음', [('setsid ${TIMEV[@]+"${TIMEV[@]}"} "${RENV[@]}"', '${TIMEV[@]+"${TIMEV[@]}"} "${RENV[@]}"')]),
    ('러너가 끝난 뒤 그룹에 남은 것을 세지 않음', [('ORPH="$(group_count)"', 'ORPH=0')]),
    ('잠금을 잡지 않음', [('if mkdir "$LOCK" 2>/dev/null; then', 'if true; then')]),
    ('잠금을 풀지 않음', [('    rmdir "$LOCK" 2>/dev/null\n', '    :\n')]),
    ('동시 실행 가드를 뺌', [('[ "$BUSY" = 0 ] || stop', 'true || stop')]),
    ('러너의 런 전 관문을 미리 돌리지 않음', [('"${RENV[@]}" "${CMD[@]}" PYTHONUTF8=1 python3 "$W/scripts/check_method_discipline.py"', 'true')]),
    ('PYTHONUNBUFFERED 를 러너에 주지 않음', [('"OUTDIR=$O" PYTHONUNBUFFERED=1)', '"OUTDIR=$O")')]),
    ('STOPPED 표지를 쓰지 않음', [("    printf 'reason=%s\\nrunner_started=0\\n' \"$*\" > \"$L/STOPPED\"\n", '    :\n')]),
    ('끝나도 watcher.pid 를 두고 감', [('rm -f "$L/watcher.pid"\nFINISHED=1\n', 'FINISHED=1\n')]),
    ('끝 기록 중 TERM 을 미루지 않음 (기본 동작)', [("trap 'LATE_SIG=$((LATE_SIG + 1))' TERM INT HUP", 'trap - TERM INT HUP')]),
    ('시도 번호를 출력 폴더와 대조하지 않음', [('  "ca1_probe6_a${ATTEMPT}_"*_arm1) ;;', '  ca1_probe6_a*_arm1) ;;')]),
    ('meta 에 시도 번호를 적지 않음', [('  echo "attempt=$ATTEMPT"\n', '')]),
    ('발사 전 GPU · 디스크 줄을 찍지 않음', [('say "pre-launch: attempt $ATTEMPT, GPU memory in use $GU0 MiB of $GM MiB, disk free $DFK GB (kit root) and $DFL GB (log folder)"',
                                         ':')]),
    ('env 이름 기록을 뺌', [("  printf '%s\\n' \"$ENVREC\"\n", '')]),
    ('뜻밖의 끝에서 표지를 안 씀', [('trap on_exit EXIT\n', '')]),
    ('묶음의 time -v 기록을 거르지 않음 (명령 줄 · 홈 경로)', [
        ("      grep -E '^[[:space:]]*(Maximum resident set size \\(kbytes\\)|Elapsed \\(wall clock\\) time \\(h:mm:ss or m:ss\\)|Exit status): ' \"$L/$f\" > \"$STG/$f\"",
         '      cp "$L/$f" "$STG/$f"')]),
    ('묶음의 status.log 를 사본 없이 (묶은 뒤 줄이 붙는 원본)', [
        ('  for f in probe6_report.json probe6_screen.txt runner_filtered.log env.txt meta.txt command.txt samples.tsv status.log probe6_reader.err; do',
         '  ln -s "$L/status.log" "$STG/status.log"; MEMBERS="$MEMBERS status.log"\n'
         '  for f in probe6_report.json probe6_screen.txt runner_filtered.log env.txt meta.txt command.txt samples.tsv probe6_reader.err; do')]),
    # 2 회차 고침의 새 검사 (P6R2-01 · 02 · 03 · 04 · 05 · 06)
    ('set +m 을 뺌 (작업 제어 켠 채)', [('set +m   # job control off', '#et +m   # job control off')]),
    ('러너 env 의 BASH_ENV · SHELLOPTS 를 걷지 않음', [('RENV=(env -u BASH_ENV -u SHELLOPTS)', 'RENV=(env)')]),
    ('러너가 세션 우두머리인지 안 봄', [('if ! runner_leads_session; then', 'if false; then')]),
    ('PYTHONPATH 를 걷지 않음', [('if [ -n "${PYTHONPATH+x}" ]; then PPR=1; unset PYTHONPATH; fi', 'if [ -n "${PYTHONPATH+x}" ]; then PPR=1; fi')]),
    ('시도 번호 ↔ 한도 짝을 안 봄', [('[ "$MAXITER" = "$WANT_MAX" ] || stop', '[ -n "$WANT_MAX" ] || stop')]),
    ('로그 폴더 자리 (홈 바로 밑) 를 안 봄', [('[ -n "$LP" ] && [ "$LP" = "$HP" ] || stop', '[ -n "$LP" ] || stop')]),
    ('끝 표지 없는 앞 폴더를 안 봄', [('  stop "earlier log folder $(homerel "$d") has no end marker', '  : "earlier log folder $(homerel "$d") has no end marker')]),
    ('끝난 시도 번호를 안 봄', [('  if finished "$d"; then\n    stop "attempt $ATTEMPT already ran', '  if false; then\n    stop "attempt $ATTEMPT already ran')]),
    ('시도 1 의 끝난 a2 폴더를 안 봄', [('    if [ -d "$d" ] && finished "$d"; then stop "attempt 2 already ran to the end in $(homerel "$d") - attempt 1',
                                       '    if [ -d "$d" ] && false; then stop "attempt 2 already ran to the end in $(homerel "$d") - attempt 1')]),
    ('시도 2 앞 조건 (끝난 시도 1 하나) 을 안 봄', [('[ "$N1" = 1 ] || stop', '[ -n "$N1" ] || stop')]),
    ('시도 2 앞 조건에서 solve_started=1 을 안 봄', [("    if [ -f \"$d/DONE\" ] && grep -qx 'solve_started=1' \"$d/meta.txt\" 2>/dev/null; then\n      N1=",
                                                   "    if [ -f \"$d/DONE\" ]; then\n      N1=")]),
    ('풀이 코드 대조를 안 함', [('  git -C "$W" diff --quiet "$P1" "$PIN" -- "${CODE_PATHS[@]}" 2>/dev/null\n', '  true\n')]),
    ('시도 1 핀이 앞 커밋인지 안 봄', [('git -C "$W" merge-base --is-ancestor "$P1" "$PIN" 2>/dev/null; }', 'true; }')]),
    ('meta 에 attempt1 칸을 안 적음', [('    echo "attempt1_pin=$P1"\n    echo "code_same_as_attempt1=1"\n', '    :\n')]),
    ('meta 에 expect_rj 를 안 적음', [('  echo "expect_rj=$EXP_RJ"\n', '')]),
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
        caught = ''

        def coll(n, c, w=''):
            if not c:
                raise _Caught(n.split(' ')[0])
            return True
        chk, WRAPPER_SRC = coll, mp
        t0 = time.time()
        try:
            t_F(pre='wm%d' % i)
        except _Caught as e:
            caught = str(e)
        except Exception as e:                                 # noqa: BLE001 · 변이가 F 묶음을 깨뜨리면 그것도 잡힌 것
            caught = 'EXC %s' % type(e).__name__
        finally:
            chk, WRAPPER_SRC = real_chk, None
            sweep_tagged()
        real_chk('W 변이 [%s]: F 묶음이 잡는다 (%s · %.0f s)' % (name, caught or '-', time.time() - t0), caught != '', '잡지 못함')


# ═════════════════════════ B: KGY 블록 끝까지 (시도 1 → 시도 2) ═════════════════════════
def run_block(home, env, blk, timeout=240):
    p = subprocess.run(['bash'], input=blk, env=env, capture_output=True, text=True, cwd=home, timeout=timeout)
    return p


def wait_marker(lg, n=600):
    for _ in range(n):
        if any(os.path.exists(os.path.join(lg, m)) for m in ('DONE', 'STOPPED', 'WATCHER_FAILED')):
            return True
        time.sleep(0.2)
    return False


@case('B 블록 (KGY_BLOCK.md 그대로 · 시도 1 → 시도 2)')
def t_B():
    repo, pin = make_pin_repo('b_pin')
    home = make_home('b_home')
    fd = fake_dir('b_fake', pin)
    bare = os.path.join(TD, 'b_origin.git')
    subprocess.run(['git', 'clone', '-q', '--bare', repo, bare], check=True, capture_output=True, env=_rc().git_fixture_env())   # ★ 3 회차 (RCP3-04)
    git(bare, 'branch', 'claude/stoic-knuth-NObVQ', pin)
    subprocess.run(['git', 'clone', '-q', bare, os.path.join(home, 'dem-mt')], check=True, capture_output=True, env=_rc().git_fixture_env())
    blk0 = fenced_blocks(read_text(BLOCK_MD))[0]
    blk1 = blk0.replace('<PIN>', pin)
    blk2 = blk1.replace('\nATTEMPT=1\n', '\nATTEMPT=2\n')
    env = wrapper_env(home, fd, PROBE6_FAKE_SLEEP='2')
    n_lg = lambda: len(glob.glob(os.path.join(home, 'p6log_*')))   # noqa: E731
    n_wt = lambda: len(glob.glob(os.path.join(home, 'dem-p6-*')))   # noqa: E731
    bstops = []

    def bstop(label, needle, p, nl, nw):
        line = [ln for ln in p.stdout.splitlines() if 'STOP:' in ln]
        bstops.append((label, p.returncode == 2 and bool(line) and needle in line[-1] and 'syntax error' not in p.stderr
                       and n_lg() == nl and n_wt() == nw, (p.returncode, (line or [p.stdout[-200:]])[-1][-170:], p.stderr[-150:])))
    bstop('PIN 이 40 자리 hex 아님', 'PIN is not a 40-hex commit', run_block(home, env, blk1.replace(pin, 'zz')), 0, 0)
    bstop('<PIN> 을 안 채움 (bash 문법 오류가 아니다)', 'PIN is not a 40-hex commit', run_block(home, env, blk0), 0, 0)
    bstop('ATTEMPT 가 1 · 2 가 아님', 'ATTEMPT must be 1 or 2', run_block(home, env, blk1.replace('\nATTEMPT=1\n', '\nATTEMPT=3\n')), 0, 0)
    shutil.move(os.path.join(home, 'dem-mt'), os.path.join(home, 'dem-mt-moved'))
    bstop('BASE 가 git 저장소가 아님', 'BASE is not a git checkout', run_block(home, env, blk1), 0, 0)
    shutil.move(os.path.join(home, 'dem-mt-moved'), os.path.join(home, 'dem-mt'))
    git(bare, 'branch', '-f', 'claude/stoic-knuth-NObVQ', git(bare, 'commit-tree', '-p', pin, '-m', 'later', pin + '^{tree}'))
    bstop('PIN 이 가지 끝 (fetch 뒤 FETCH_HEAD) 이 아님', 'is not the tip of', run_block(home, env, blk1), 0, 0)
    git(bare, 'branch', '-f', 'claude/stoic-knuth-NObVQ', pin)
    bstop('시도 2 인데 시도 1 의 DONE 폴더가 없음', 'attempt 2 needs exactly one', run_block(home, env, blk2), 0, 0)
    # 감시 셸이 띄운 뒤 멈춤 (킷 payload 줄에 --show-results) → 블록이 그 STOP 줄을 보여 준다 · 안내 줄은 찍지 않는다 · 같은 블록을 다시 붙일 수 있다
    kit_sh = os.path.join(home, 'sdcp', KIT, 'run_mpm.sh')
    write_text(kit_sh, FAKE_KIT_SH.replace(' --out', ' --show-results --out'))
    p = run_block(home, env, blk1)
    lgs = glob.glob(os.path.join(home, 'p6log_a1_*'))
    ok_s = (p.returncode == 2 and 'watcher launched' in p.stdout.splitlines()[0] if p.stdout else False)
    chk('B01 감시 셸이 띄운 뒤 STOP: 블록 첫 줄 "watcher launched" · 블록이 그 STOP 줄을 찍는다 · rc 2 · 로그 폴더에 STOPPED · 러너 호출 0 · '
        'STOP 뒤 진행 · 멈춤 · "DONE appears" 안내 없음 (P6R2-07)',
        ok_s and any('STOP:' in ln and '--show-results' in ln and 'runner not started' in ln for ln in p.stdout.splitlines())
        and len(lgs) == 1 and os.path.exists(os.path.join(lgs[0], 'STOPPED')) and not os.path.exists(os.path.join(fd, 'calls.txt'))
        and 'DONE appears' not in p.stdout and 'stop early' not in p.stdout and 'progress:' not in p.stdout,
        (p.returncode, p.stdout[-600:], p.stderr[-200:]))
    write_text(kit_sh, FAKE_KIT_SH)
    os.makedirs(os.path.join(home, 'p6log_a1_19990101T000000Z'))
    write_text(os.path.join(home, 'p6log_a1_19990101T000000Z', 'nohup.out'), '')
    bstop('앞 로그 폴더에 끝 표지 (DONE · STOPPED · WATCHER_FAILED) 가 없음', 'has no end marker', run_block(home, env, blk1), 2, 1)
    shutil.rmtree(os.path.join(home, 'p6log_a1_19990101T000000Z'))
    # 끝난 시도 번호 · 시도 2 앞 조건 · 풀이 코드 (P6R2-01 · 02 · 03): 합성 로그 폴더 (멈춤 뒤 지운다 · 시험 전용)
    for label, folders, blk, needle in (
            ('시도 1 이 끝남 (DONE · solve_started=1) → 시도 1 블록 다시', [('p6log_a1_20991231T000001Z', lf_done(1, pin))], blk1,
             'attempt 1 already ran to the end'),
            ('시도 1 = WATCHER_FAILED · 러너 시작 줄 있음 → 시도 1 블록', [('p6log_a1_20991231T000001Z', LF_WF_START)], blk1, 'attempt 1 already ran to the end'),
            ('시도 2 가 끝남 → 시도 1 블록', [('p6log_a2_20991231T000001Z', lf_done(2, pin))], blk1, 'attempt 1 does not run after attempt 2'),
            ('시도 2 가 끝남 → 시도 2 블록 다시', [('p6log_a1_20991231T000001Z', lf_done(1, pin)), ('p6log_a2_20991231T000002Z', lf_done(2, pin))], blk2,
             'attempt 2 already ran to the end'),
            ('시도 1 = DONE · solve_started=0 뿐 (풀이 0) → 시도 2 블록', [('p6log_a1_20991231T000001Z', lf_done(1, pin, solve=0))], blk2,
             'attempt 2 needs exactly one'),
            ('끝난 시도 1 이 둘 → 시도 2 블록', [('p6log_a1_20991231T000001Z', lf_done(1, pin)), ('p6log_a1_20991231T000002Z', lf_done(1, pin))], blk2,
             'attempt 2 needs exactly one'),
            ('시도 1 의 핀이 이 PIN 의 앞 커밋이 아님', [('p6log_a1_20991231T000001Z', lf_done(1, 'f' * 40))], blk2, 'not this PIN or an earlier commit')):
        made = [log_folder(home, nm, files) for nm, files in folders]
        nl, nw = n_lg(), n_wt()
        bstop(label, needle, run_block(home, env, blk), nl, nw)
        for d in made:
            shutil.rmtree(d)
    # 풀이 코드가 바뀐 PIN (P6R2-03): 가지 끝 = 러너를 고친 뒤 커밋 · 시도 1 의 핀 = 그 앞 커밋 → 시도 2 블록이 멈추고 바뀐 파일을 찍는다
    git(repo, 'checkout', '-q', '--detach', pin)
    write_text(os.path.join(repo, RUNNER_REL), read_text(os.path.join(repo, RUNNER_REL)) + '# changed solve code\n', 0o755)
    git(repo, 'commit', '-q', '-am', 'runner change')
    pin_b = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'push', '-q', '-f', bare, 'HEAD:refs/heads/claude/stoic-knuth-NObVQ')
    made = log_folder(home, 'p6log_a1_20991231T000001Z', lf_done(1, pin))
    nl, nw = n_lg(), n_wt()
    pb = run_block(home, env, blk0.replace('<PIN>', pin_b).replace('\nATTEMPT=1\n', '\nATTEMPT=2\n'))
    bstop('시도 1 핀 ↔ 이 PIN 사이에 풀이 코드 (scripts/) 가 바뀜 → 시도 2 블록', 'the solve code changed', pb, nl, nw)
    bstops[-1] = bstops[-1][:1] + (bstops[-1][1] and RUNNER_REL in pb.stdout,) + bstops[-1][2:]
    shutil.rmtree(made)
    git(bare, 'branch', '-f', 'claude/stoic-knuth-NObVQ', pin)
    git(repo, 'checkout', '-q', '--detach', pin)
    chk('B02 블록 멈춤 %d 가지: rc 2 · 그 사유 · 폴더 · 작업 트리를 더 만들지 않는다 · bash 문법 오류 없음' % len(bstops),
        len(bstops) == 15 and all(ok for _l, ok, _w in bstops), [b for b in bstops if not b[1]])
    # 시도 1 (한도에 닿음 = 러너 rc 1 · 판독 rc 3 · 정상 끝)
    p = run_block(home, wrapper_env(home, fd, PROBE6_FAKE_MODE='fail', PROBE6_FAKE_SLEEP='2'), blk1)
    lg1 = sorted(set(glob.glob(os.path.join(home, 'p6log_a1_*'))) - set(lgs))
    lg1 = lg1[0] if lg1 else ''
    done1 = wait_marker(lg1) if lg1 else False
    chk('B03 시도 1: 블록 rc 0 · 첫 줄 watcher launched · runner started 줄 · 발사 전 줄 (GPU · 디스크) · DONE = runner_rc=1 report_rc=3 attempt=1',
        p.returncode == 0 and [ln for ln in p.stdout.splitlines() if not ln.startswith('[p6] reusing worktree')][0].startswith('[p6] watcher launched')
        and 'runner started - maxiter 30000' in p.stdout
        and 'pre-launch: attempt 1, GPU memory in use' in p.stdout and done1
        and read_text(os.path.join(lg1, 'DONE')).startswith('runner_rc=1 report_rc=3 attempt=1'), (p.returncode, p.stdout[-700:], p.stderr[-200:]))
    m1 = read_meta(lg1) if lg1 else {}
    rep1 = json.loads(read_text(os.path.join(lg1, 'probe6_report.json'))) if lg1 and os.path.exists(os.path.join(lg1, 'probe6_report.json')) else {}
    cmd1 = read_text(os.path.join(lg1, 'command.txt')) if lg1 else ''
    chk('B04 시도 1 의 번호 · 한도: meta attempt 1 · maxiter 30000 · command.txt --step3-maxiter 30000 · 보고 attempt 1 · 출력 폴더 ca1_probe6_a1_*_arm1',
        m1.get('attempt') == '1' and m1.get('maxiter') == '30000' and 'P2_EXTRA="--step3-maxiter 30000"' in cmd1 and rep1.get('attempt') == 1
        and re.fullmatch(r'~/sdcp/ca1_probe6_a1_[0-9]{8}T[0-9]{6}Z_arm1', m1.get('outdir', '')) is not None, (m1, cmd1[-200:]))
    left = os.path.join(home, 'sdcp', KIT, S0_RUN, ARM + '.json.failed')
    c1 = os.path.join(lg1, 'kit_run_new', ARM + '.json.failed')
    s1 = sha256_file(left) if os.path.exists(left) else None
    chk('B05 시도 1 의 남은 파일 (.failed) = 시도 1 로그 폴더에 바이트 사본 (sha256 = 보고) · 시도 2 가 쓰기 전',
        s1 is not None and os.path.exists(c1) and sha256_file(c1) == s1
        and [x.get('sha256') for x in rep1.get('kit_run_new_files') or [] if x.get('name') == ARM + '.json.failed'] == [s1], (s1,))
    b1_sha = sha256_file(os.path.join(lg1, 'probe6_bundle.tgz')) if lg1 and os.path.exists(os.path.join(lg1, 'probe6_bundle.tgz')) else None
    lg1_files = sorted(os.listdir(lg1)) if lg1 else []
    if os.path.exists(left):
        os.utime(left, (time.time() - 30, time.time() - 30))         # kgy 에서 두 시도 사이는 분 단위 (판독기의 "이 시도의 새 파일" 2 초 여유)
    # 끝난 시도 1 의 블록을 다시 붙임 (화면 다시 실행 · P6R2-02) → 멈춤 · 아무것도 쓰지 않는다
    nl, nw = n_lg(), n_wt()
    p11 = run_block(home, env, blk1)
    l11 = [ln for ln in p11.stdout.splitlines() if 'STOP:' in ln]
    chk('B11 끝난 시도 1 의 블록을 다시 붙임: rc 2 · "attempt 1 already ran to the end" · 로그 폴더 · 작업 트리를 더 만들지 않는다 · 러너 호출 그대로',
        p11.returncode == 2 and bool(l11) and 'attempt 1 already ran to the end' in l11[-1] and n_lg() == nl and n_wt() == nw,
        (p11.returncode, p11.stdout[-300:]))
    # 시도 2 (ATTEMPT=2 · 한도 1500000 · 풀이를 시작한 시도 1 의 DONE 뒤)
    p2 = run_block(home, wrapper_env(home, fd, PROBE6_FAKE_SLEEP='2'), blk2)
    lg2 = glob.glob(os.path.join(home, 'p6log_a2_*'))
    lg2 = lg2[0] if len(lg2) == 1 else ''
    done2 = wait_marker(lg2) if lg2 else False
    m2 = read_meta(lg2) if lg2 else {}
    rep2 = json.loads(read_text(os.path.join(lg2, 'probe6_report.json'))) if lg2 and os.path.exists(os.path.join(lg2, 'probe6_report.json')) else {}
    chk('B06 시도 2: 블록 rc 0 · DONE = runner_rc=0 report_rc=0 attempt=2 · meta attempt 2 · maxiter 1500000 · attempt1_pin = 시도 1 의 핀 · '
        'code_same_as_attempt1=1 · 출처 = 시도 2 출력 폴더의 팔',
        p2.returncode == 0 and done2 and read_text(os.path.join(lg2, 'DONE')).startswith('runner_rc=0 report_rc=0 attempt=2')
        and m2.get('attempt') == '2' and m2.get('maxiter') == '1500000' and rep2.get('source') == 'outdir' and rep2.get('verdict') == 'PROBE_OK'
        and m2.get('attempt1_pin') == pin and m2.get('code_same_as_attempt1') == '1'
        and re.fullmatch(r'~/sdcp/ca1_probe6_a2_[0-9]{8}T[0-9]{6}Z_arm1', m2.get('outdir', '')) is not None,
        (p2.returncode, p2.stdout[-500:], m2.get('attempt'), m2.get('maxiter'), rep2.get('problems')))
    bf = [x for x in rep2.get('kit_run_before_files') or [] if x.get('name') == ARM + '.json.failed']
    chk('B07 시도 1 의 남은 파일: 시도 2 가 시작 전에 사본 (kit_run_before · sha256 = 시도 1 의 것) · 시도 2 판독기는 그것을 읽지 않는다 (새 파일 아님)',
        bool(bf) and bf[0].get('sha256') == s1 and sha256_file(os.path.join(lg2, 'kit_run_before', ARM + '.json.failed')) == s1
        and ARM + '.json.failed' not in [x.get('name') for x in rep2.get('kit_run_new_files') or []], (bf, rep2.get('kit_run_new_files')))
    chk('B08 시도 1 의 로그 폴더 · 묶음은 시도 2 뒤에도 그대로 (파일 목록 · 묶음 sha256)',
        lg1 != '' and sorted(os.listdir(lg1)) == lg1_files and b1_sha is not None and sha256_file(os.path.join(lg1, 'probe6_bundle.tgz')) == b1_sha, '')
    nh = ''.join(read_text(os.path.join(x, 'nohup.out')) for x in (lg1, lg2) if x and os.path.exists(os.path.join(x, 'nohup.out')))
    bps = bundle_problems(lg1, T_SEALED, home) + bundle_problems(lg2, T_SEALED, home)
    chk('B09 nohup.out · 블록 화면 = [probe6] / [p6] 줄만 · 두 시도의 묶음 꼴 · σ 류 수 없음',
        nh != '' and all(ln.startswith('[probe6] ') for ln in nh.splitlines()) and all(ln.startswith(('[p6] ', '[probe6] ')) for ln in (p.stdout + p2.stdout).splitlines())
        and bps == [] and scan_hits([nh, p.stdout, p.stderr, p2.stdout, p2.stderr], T_SEALED, sd_min=4, floats_only=True) == [], bps[:4])
    wt = glob.glob(os.path.join(home, 'dem-p6-*'))
    chk('B10 블록이 만든 작업 트리 = 핀 · 깨끗함 (두 시도 뒤에도) · 잠금 없음',
        len(wt) == 1 and git(wt[0], 'rev-parse', 'HEAD') == pin and git(wt[0], 'status', '--porcelain', '--untracked-files=all') == ''
        and not os.path.exists(os.path.join(home, '.probe6.lock')), wt)
    # 끝난 시도 2 · 1 의 블록을 다시 붙임 (P6R2-02) → 둘 다 멈춤
    nl, nw = n_lg(), n_wt()
    p12a, p12b = run_block(home, env, blk2), run_block(home, env, blk1)
    l12 = [[ln for ln in q.stdout.splitlines() if 'STOP:' in ln] for q in (p12a, p12b)]
    chk('B12 시도 2 뒤 시도 2 · 시도 1 블록을 다시 붙임: 둘 다 rc 2 (attempt 2 already ran · 시도 1 = 끝남 또는 a2 폴더) · 더 만든 것 없음',
        p12a.returncode == 2 and p12b.returncode == 2 and all(l12) and 'attempt 2 already ran to the end' in l12[0][-1]
        and ('attempt 1 already ran to the end' in l12[1][-1] or 'attempt 1 does not run after attempt 2' in l12[1][-1]) and n_lg() == nl and n_wt() == nw,
        (p12a.stdout[-200:], p12b.stdout[-200:]))
    # 풀이 0 인 시도 1 (P6R2-01): DONE · solve_started=0 뒤 시도 2 블록 = 멈춤 · 같은 번호 (시도 1) 는 다시 된다 · 원장 글만 바뀐 PIN 의 시도 2 는 돈다 (P6R2-03)
    h2 = make_home('b2_home')
    fd2 = fake_dir('b2_fake', pin)
    bare2 = os.path.join(TD, 'b2_origin.git')
    subprocess.run(['git', 'clone', '-q', '--bare', repo, bare2], check=True, capture_output=True, env=_rc().git_fixture_env())   # ★ 3 회차 (RCP3-04)
    git(bare2, 'branch', '-f', 'claude/stoic-knuth-NObVQ', pin)
    subprocess.run(['git', 'clone', '-q', bare2, os.path.join(h2, 'dem-mt')], check=True, capture_output=True, env=_rc().git_fixture_env())
    q1 = run_block(h2, wrapper_env(h2, fd2, PROBE6_FAKE_MODE='nosolve'), blk1)
    la = glob.glob(os.path.join(h2, 'p6log_a1_*'))
    da = wait_marker(la[0]) if len(la) == 1 else False
    ma = read_meta(la[0]) if len(la) == 1 else {}
    q2 = run_block(h2, wrapper_env(h2, fd2), blk2)
    lq2 = [ln for ln in q2.stdout.splitlines() if 'STOP:' in ln]
    time.sleep(1.1)                                                  # 새 블록 = 새 시각 이름 (초 단위)
    q3 = run_block(h2, wrapper_env(h2, fd2, PROBE6_FAKE_MODE='fail', PROBE6_FAKE_SLEEP='1'), blk1)
    lb = sorted(set(glob.glob(os.path.join(h2, 'p6log_a1_*'))) - set(la))
    db = wait_marker(lb[0]) if len(lb) == 1 else False
    chk('B13 풀이 0 인 시도 1 (payload 가 풀이 줄 전에 멈춤): DONE · solve_started=0 → 시도 2 블록 = rc 2 (attempt 2 needs exactly one) · '
        '시도 1 블록을 다시 붙이면 돈다 (같은 번호 · 원장 §3)',
        q1.returncode == 0 and da and ma.get('solve_started') == '0' and q2.returncode == 2 and bool(lq2) and 'attempt 2 needs exactly one' in lq2[-1]
        and q3.returncode == 0 and db and read_meta(lb[0]).get('solve_started') == '1' if len(lb) == 1 else False,
        (q1.returncode, ma.get('solve_started'), q2.returncode, lq2[-1:], q3.returncode, q3.stdout[-300:]))
    git(repo, 'checkout', '-q', '--detach', pin)
    write_text(os.path.join(repo, 'docs', 'reviews', 'rint2_dev_probe_ledger_20261026.md'), '# attempt 1 result line (ledger only)\n')
    git(repo, 'add', '-A')
    git(repo, 'commit', '-q', '-m', 'ledger line of attempt 1')
    pin_c = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'push', '-q', '-f', bare2, 'HEAD:refs/heads/claude/stoic-knuth-NObVQ')
    git(repo, 'checkout', '-q', '--detach', pin)
    if os.path.exists(os.path.join(h2, 'sdcp', KIT, S0_RUN, ARM + '.json.failed')):
        os.utime(os.path.join(h2, 'sdcp', KIT, S0_RUN, ARM + '.json.failed'), (time.time() - 30, time.time() - 30))
    q4 = run_block(h2, wrapper_env(h2, fake_dir('b2_fake_c', pin_c), PROBE6_FAKE_SLEEP='1'),
                   blk0.replace('<PIN>', pin_c).replace('\nATTEMPT=1\n', '\nATTEMPT=2\n'))
    lc = glob.glob(os.path.join(h2, 'p6log_a2_*'))
    dc = wait_marker(lc[0]) if len(lc) == 1 else False
    mc = read_meta(lc[0]) if len(lc) == 1 else {}
    repc = json.loads(read_text(os.path.join(lc[0], 'probe6_report.json'))) if dc and os.path.exists(os.path.join(lc[0], 'probe6_report.json')) else {}
    chk('B14 시도 1 뒤 원장 글만 바뀐 커밋 (풀이 코드 같음) 을 PIN 으로 시도 2: 블록 rc 0 · DONE · meta pin = 새 PIN · attempt1_pin = 시도 1 의 핀 · '
        'code_same_as_attempt1=1 · PROBE_OK',
        q4.returncode == 0 and dc and mc.get('pin') == pin_c and mc.get('attempt1_pin') == pin and mc.get('code_same_as_attempt1') == '1'
        and repc.get('verdict') == 'PROBE_OK', (q4.returncode, q4.stdout[-400:], dict((k, mc.get(k)) for k in ('pin', 'attempt1_pin', 'code_same_as_attempt1')),
                                               repc.get('problems')))


# ═════════════════════════ R: 실제 러너 · 실제 payload (픽스처 킷 · CPU) ═════════════════════════
def real_sigma_values(arm_path):
    """실물 팔 JSON 의 σ 류 수 (σ_e · 증서의 σ · 판 전류 · 목표량 구간 · scale · 소산 몫 · 접합 전류 …): 수 찾기의 과녁."""
    with open(arm_path, encoding='utf-8') as f:
        j = json.load(f)
    s3 = j['mpm_metrics']['step3']
    hints = ('sigma_e_eff', 'I_bot', 'I_top', 'target_lo', 'target_hi', 'target_U', 'target_W', 'target_flow', 'scale', 'R_bulk',
             'share', 'P_total', 'P_sum', 'sigma_apparent', 'sigma_resolve', 'ideal_R0', 'dsigma', 'err_bound', 'width_rel', 'current')
    vals = []

    def walk(x, key):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, key + '.' + str(k))
        elif isinstance(x, list):
            for v in x:
                walk(v, key)
        elif isinstance(x, float) and math.isfinite(x) and x not in (0.0, 1.0) and (any(h in key for h in hints) or key.endswith('conv_cert.sigma')):
            vals.append(x)
    walk(s3, 'step3')
    return vals


def real_hits(vals, texts):
    """실물: 유효숫자 7 자리 이상 소수 (우연히 맞을 확률이 작은 쪽) 로 σ 와 변형을 찾는다."""
    return scan_hits(texts, vals, sd_min=7, floats_only=True, stream=False, hexsearch=True)


@case('R 실물 (실제 러너 · payload · 픽스처 킷)')
def t_R():
    if ARGS is not None and ARGS.no_real:
        _skipped.append('R (--no-real)')
        print('  SKIP  R 묶음: --no-real (PASS 로 세지 않는다)')
        return
    sys.path.insert(0, SCRIPTS)
    try:
        import test_ca_ext_runner as TR                        # noqa: E402 · 가짜 python3 (규율 관문 둘만 건너뛴다) · 사본 없음
        import test_rint_r_chain_e2e as E2E                    # noqa: E402 · 생산 단위 픽스처 침대 (vox 0.15) · 사본 없음
        import ca_s0_census as S0                              # noqa: E402 · S0 단계 1 도구 (실제 계획의 입력 지문을 낸 함수)
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
    out = os.path.join(ws, 'ca1_probe6_a1_r1_arm1')
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
    vals = real_sigma_values(arms[0])
    chk('R1c (시험의 판별력) 실물 팔 JSON 에 σ 류 수가 10 개 넘게 있다 · 그 하나를 흔한 꼴로 적은 글은 수 찾기가 잡는다 (양성 대조) · 러너 원문 로그에는 없다',
        len(vals) >= 10 and all(real_hits(vals, [fm % vals[0]]) for fm in ('x %.17g', 'x %.9g', 'x %.7e')) and real_hits(vals, [log]) == [],
        (len(vals), real_hits(vals, [log])[:3]))
    lg = os.path.join(TD, 'r1_log')
    os.makedirs(lg)
    write_text(os.path.join(lg, 'runner.log'), log)
    nl = len(log.split('\n')) - 1
    write_text(os.path.join(lg, 'samples.tsv'), '#epoch\telapsed_s\tlog_lines\trss_sum_kb\trss_max_kb\tgpu_used_mib\tgpu_ours_mib\tgpu_util\n'
               '%d\t0\t3\t1000\t900\tNA\tNA\tNA\n%d\t5\t%d\t2000\t1900\tNA\tNA\tNA\n' % (t0, t0 + 5, nl))
    head = git(ROOT, 'rev-parse', 'HEAD')
    write_text(os.path.join(lg, 'meta.txt'), meta_text(pin=head, start_epoch=t0, end_epoch=t0 + 5, wall_s=5, time_v=0, expect_backend='cpu'))
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
    struct = report_problems(r.rep) + screen_problems(r.out, r.rep) + filtered_problems(r.filtered, r.rep) + fields_provenance(r.rep, _arm_of(r))
    bad = real_hits(vals, [r.out, r.err, r.report_text, r.filtered, json_strings(r.rep) if r.rep else ''])
    chk('R1f 실물: 판독기 출력의 구조 검사 (닫힌 칸 · 화면 = 보고 · 걸러 낸 로그 꼴 · 팔 값 출처) 통과 · σ 류 수 (유효숫자 7 이상) 가 어디에도 없다',
        struct == [] and bad == [], (struct[:4], bad[:3]))
    dirty = str(f.get('code_sha', '')).endswith('+dirty')      # 이 리포의 추적 파일을 고친 채 돌리면 payload 가 +dirty 를 싣는다
    chk('R1g 실물: 판독 rc 0 · PROBE_OK (같은 침대 대조는 요청 안 함 = 픽스처 침대)%s' % (' [더러운 트리: rc 4 · 핀 불일치만]' if dirty else ''),
        (r.rc == 4 and f.get('code_matches_pin') is False) if dirty else (r.rc == 0 and (r.rep or {}).get('verdict') == 'PROBE_OK'),
        (r.rc, (r.rep or {}).get('problems')))
    # R1x (변이 · 실물) step3 블록을 통째로 보고에 싣는 판독기 = 구조 검사 · 수 찾기가 잡는다
    msrc = read_text(READER).replace("    f = read_table(s3, ARM_FIELDS)\n", "    f = read_table(s3, ARM_FIELDS)\n    f['zz_dump'] = s3\n")
    mp = os.path.join(TD, 'r1x_reader.py')
    write_text(mp, msrc)
    rx = run_reader(load_reader(mp), out, lg, run, s0=False)
    chk('R1x (변이) step3 통째 덤프를 싣는 판독기: 구조 검사가 모르는 칸으로 잡고 수 찾기가 실물 σ 를 찾는다',
        rx.rep is not None and any('unknown key zz_dump' in x for x in report_problems(rx.rep))
        and real_hits(vals, [rx.report_text]) != [], (rx.rc, report_problems(rx.rep or {})[:3]))
    # R1h 생산 킷 꼴 (payload 줄에 --joule-heat · --save-step4-grid) = 다음 세대 payload 가 입구에서 거부한다 (감시 셸의 멈춤 조건의 근거)
    ws_p = os.path.join(TD, 'r1p_ws')
    run_p = os.path.join(ws_p, KIT, S0_RUN)
    os.makedirs(run_p)
    E2E.make_bed(run_p)
    write_text(os.path.join(ws_p, KIT, 'run_mpm.sh'), E2E.KIT_SH_PROD)
    os.symlink(S0_RUN, os.path.join(ws_p, KIT, 'latest_run'))
    os.makedirs(os.path.join(ws_p, '_shim'))
    env_p = dict(env, OUTDIR=os.path.join(ws_p, 'ca1_probe6_a1_r1p_arm1'), SHIM_LOG=os.path.join(ws_p, '_shim'))
    pp = subprocess.run(['bash', os.path.join(SCRIPTS, 'sdcp_gain_vox015_8arm.sh')], cwd=ws_p, env=env_p, capture_output=True, text=True,
                        encoding='utf-8', errors='replace', stdin=subprocess.DEVNULL, timeout=900)
    log_p = (pp.stdout or '') + (pp.stderr or '')
    hit = sorted(set(re.findall(r'S[12]_(?:CJUNC|FACE_ALPHA)_REFUSED\|(JOULE|STEP4_GRID)\|', log_p)))
    chk('R1h 생산 킷 꼴 (--joule-heat · --save-step4-grid) + 등록 축: payload 가 입구에서 거부 (JOULE · STEP4_GRID) · 러너 rc ≠ 0 · 팔 없음',
        pp.returncode != 0 and set(hit) >= {'JOULE', 'STEP4_GRID'} and not glob.glob(os.path.join(env_p['OUTDIR'], 'p2_*.json'))
        and 'STEP3 solve:' not in log_p, (pp.returncode, hit, log_p[-500:]))
    # R2 감시 셸 + 실제 러너 + 실제 payload, 등록 축 그대로 (GPU 기대 · 폴백 금지 · cupy 자리에 numpy · scipy 대역 · GPU 계산은 아니다)
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
    chk('R2a 감시 셸 + 실제 러너 + 실제 payload (등록 축 그대로 · GPU 가지 = cupy 대역 · 런 전 관문 미리 · PYTHONUNBUFFERED=1): rc 0 · 러너 rc 0 · 팔이 출력 폴더에 · DONE',
        '--step3-gpu' in kit_gpu and r.rc == 0 and r.meta.get('runner_rc') == '0' and os.path.exists(arm2)
        and os.path.exists(os.path.join(r.lg, 'DONE')) and r.meta.get('pregate') == '1', (r.rc, r.meta.get('runner_rc'), raw[-900:], r.so[-400:]))
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
    vals = real_sigma_values(arm2)
    names, members = bundle_members(r.lg)
    bp = bundle_problems(r.lg, vals, home, sd_min=7)
    chk('R2c 실물 묶음: 허용된 이름 · 파일마다 닫힌 꼴 · σ 류 수 (유효숫자 7 이상) 없음 · 감시 셸 화면에도 · 러너 원문 로그에도 없다 (봉인 표지)',
        bp == [] and len(vals) >= 10 and real_hits(vals, [r.so, r.se, raw]) == [] and SEAL in raw, (bp[:4], len(vals)))
    chk('R2d 런 뒤 핀 작업 트리 깨끗함 (git_lines_after 0) · 만든 파일에 그룹 · 기타 쓰기 비트 없음 (mode_bad 0) · 킷 런 폴더에 팔이 남지 않았다',
        r.meta.get('git_lines_after') == '0' and r.meta.get('mode_bad') == '0' and not glob.glob(os.path.join(run2, 'p2_*.json*')),
        (r.meta.get('git_lines_after'), r.meta.get('mode_bad'), glob.glob(os.path.join(run2, 'p2_*.json*'))))
    it_ok = f.get('cg_iters') if isinstance(f.get('cg_iters'), int) else 0
    repo_r2, pin_r2, run_r2 = repo, pin, run2                  # R2e · R4 = 정직한 사본 (짝 표를 고치지 않은 것)
    # R3 시도 1 꼴 (한도에 닿음): 픽스처 침대는 한도 30000 안에서 모인다 → 감시 셸 · 판독기의 짝 표만 "시도 1 → 2" 로 고친 사본 (시험 전용) ·
    #    새 홈 (R2 의 시도 1 이 끝나 같은 홈의 시도 1 은 멈춘다 · P6R2-02) · 같은 침대 (픽스처 침대는 결정적이다) = 미수렴 실물: payload 가 .failed 로
    #    남기고 러너가 받지 않는다
    home = make_home('r3_home', shim_text=shim, np_cupy=True)
    run2 = os.path.join(home, 'sdcp', KIT, S0_RUN)
    os.remove(os.path.join(run2, 'se_dump.npy'))
    E2E.make_bed(run2)
    write_text(os.path.join(home, 'sdcp', KIT, 'run_mpm.sh'), kit_gpu)
    rec3 = S0.kit_input_record(os.path.join(home, 'sdcp', KIT))
    repo, pin = make_pin_repo('r3_pin', real_scripts=True, plan_inputs=dict((k, v['sha256']) for k, v in rec3['files'].items()),
                              wrapper_patch=PAIR_PATCH_W, reader_patch=PAIR_PATCH_R)
    os.makedirs(os.path.join(home, '_shim'))
    wenv = wrapper_env(home, None, SHIM_LOG=os.path.join(home, '_shim'), PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    r3 = run_wrapper(repo, pin, home, 'r3', wenv, maxiter='2', timeout=900)
    left = os.path.join(run2, ARM + '.json.failed')
    f3 = (r3.rep or {}).get('fields') or {}
    raw3 = read_text(os.path.join(r3.lg, 'runner.log')) if os.path.exists(os.path.join(r3.lg, 'runner.log')) else ''
    chk('R3a 한도에 닿음 (maxiter 2 < 수렴에 든 %d 회): 러너 rc 1 · 팔은 출력 폴더에 없고 킷 런 폴더에 .failed · 감시 셸 rc 1 · 정상 끝 = DONE · 묶음' % it_ok,
        it_ok > 2 and r3.rc == 1 and r3.meta.get('runner_rc') == '1' and os.path.exists(left)
        and not glob.glob(os.path.join(r3.out, 'p2_*.json')) and os.path.exists(os.path.join(r3.lg, 'DONE'))
        and bundle_members(r3.lg)[0] is not None, (it_ok, r3.rc, r3.meta.get('runner_rc'), raw3[-900:]))
    s3sha = sha256_file(left) if os.path.exists(left) else None
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
        vals3 = real_sigma_values(left)
        bp3 = bundle_problems(r3.lg, vals3, home, sd_min=7)
        lg3 = (r3.rep or {}).get('log') or {}
        masked3 = lg3.get('masked_lines') or []
        chk('R3c 미수렴 팔의 σ 류 수가 감시 셸 화면 · 묶음 어디에도 없다 (묶음 꼴 통과) · 미수렴 줄 · 증서 실패 줄 = 읽은 수로 다시 적은 칸 · ABORT 줄 = 수를 가린 꼴',
            bp3 == [] and len(vals3) >= 10 and real_hits(vals3, [r3.so, r3.se]) == [] and lg3.get('not_converged_info') == 2
            and lg3.get('cert_fail_status') == 'POSITIVE_SOLVED' and len(lg3.get('cert_fail_pass') or []) == 4
            and lg3['cert_fail_pass'][0] is False and lg3.get('cg_maxiter') == 2 and any('ABORT' in m for m in masked3)
            and any('unconverged' in m for m in masked3) and all(not has_digit(m) for m in masked3), (bp3[:4], lg3.get('not_converged_info'), masked3[-5:]))
        cpy = os.path.join(r3.lg, 'kit_run_new', ARM + '.json.failed')
        chk('R3d 실패 보존: 남은 .failed 그대로 · 로그 폴더에 바이트 사본 (sha256 같음) · 출력 폴더 그대로 · 작업 트리 깨끗함',
            os.path.exists(cpy) and sha256_file(cpy) == s3sha and os.path.isdir(r3.out) and r3.meta.get('git_lines_after') == '0',
            (os.path.exists(cpy), r3.meta.get('git_lines_after')))
        os.utime(left, (time.time() - 30, time.time() - 30))         # kgy 에서 두 시도 사이는 분 단위 (판독기의 "이 시도의 새 파일" 2 초 여유)
    # R5 시도 2 꼴: 시도 1 꼴 (R3) 의 남은 파일이 킷 런 폴더에 있는 채 같은 홈 · 같은 침대 · 같은 사본에서 다음 시도 (새 출력 · 로그 폴더 · 본 한도 ·
    #    시도 1 의 핀 = 이 핀 · 풀이 코드 같음)
    r5 = run_wrapper(repo, pin, home, 'r5', wenv, timeout=900, attempt=2)
    f5 = (r5.rep or {}).get('fields') or {}
    raw5 = read_text(os.path.join(r5.lg, 'runner.log')) if os.path.exists(os.path.join(r5.lg, 'runner.log')) else ''
    bf5 = dict((x.get('name'), x.get('sha256')) for x in (r5.rep or {}).get('kit_run_before_files') or [])
    chk('R5a 시도 2 꼴 (시도 1 의 .failed 가 남은 채): SKIP · 멈춤 없이 새로 푼다 (러너 rc 0 · STEP3 solve 줄 · SKIP 줄 없음) · 판독 rc 0 · 출처 = 시도 2 출력 폴더 · '
        '반복 수 = R2 와 같음 (같은 침대) · meta attempt1_pin = 이 핀 · code_same_as_attempt1=1',
        r5.rc == 0 and r5.meta.get('runner_rc') == '0' and 'STEP3 solve:' in raw5 and '[p2] SKIP' not in raw5 and (r5.rep or {}).get('rc') == 0
        and (r5.rep or {}).get('source') == 'outdir' and f5.get('cg_iters') == it_ok and r5.meta.get('attempt') == '2'
        and r5.meta.get('attempt1_pin') == pin and r5.meta.get('code_same_as_attempt1') == '1', (r5.rc, (r5.rep or {}).get('problems'), raw5[-400:]))
    chk('R5b 시도 1 의 남은 .failed: 시도 2 가 시작 전에 바이트 사본 (kit_run_before · sha256 = 시도 1 로그 폴더의 사본) · 시도 2 판독기는 그것을 새 파일로 읽지 않는다',
        s3sha is not None and bf5.get(ARM + '.json.failed') == s3sha and ARM + '.json.failed' not in [
            x.get('name') for x in (r5.rep or {}).get('kit_run_new_files') or []], (s3sha, bf5))
    # R6 ★ 11-13 시도 3 · 4 (원장 §3 · 실제 러너 · payload · 탄소 접합 원장 저장본): R5 (끝난 시도 2) 뒤 같은 홈 · 같은 사본 · 같은 침대 →
    #    시도 3 (저장본 없음 → 감시 셸이 만듦 → payload 가 짓고 씀) → 시도 4 (그 저장본 → 적중)
    r6 = run_wrapper(repo, pin, home, 'r6', wenv, timeout=900, attempt=3)
    st6 = (r6.rep or {}).get('store') or {}
    f6 = (r6.rep or {}).get('fields') or {}
    store6 = os.path.join(home, 'p6_cjstore')
    regs6 = sorted(os.listdir(store6)) if os.path.isdir(store6) else []
    reg6 = os.path.join(store6, regs6[0]) if len(regs6) == 1 else None
    arm6 = os.path.join(r6.out, ARM + '.json')
    chk('R6a 시도 3 (실물): 감시 셸 rc 0 · 판독 rc 0 · 저장본 상태 built_written · 저장본 파일 하나 (cjreg_<64 hex>.npz · 0444) · meta 끝 목록 = 그 파일의 sha256 · '
        'audit 곁 파일 = 출력 폴더 (러너가 옮김) · 반복 수 = R2 와 같음 (같은 침대)',
        r6.rc == 0 and (r6.rep or {}).get('rc') == 0 and st6.get('status') == 'built_written' and reg6 is not None
        and re.fullmatch(r'cjreg_[0-9a-f]{64}\.npz', regs6[0]) is not None and (os.stat(reg6).st_mode & 0o777) == 0o444
        and r6.meta.get('store_listing_after') == '%s:%s' % (regs6[0], sha256_file(reg6)) and st6.get('file') == regs6[0]
        and os.path.exists(os.path.join(r6.out, AUDIT_NAME)) and f6.get('cg_iters') == it_ok,
        (r6.rc, stop_line(r6), (r6.rep or {}).get('problems'), st6, regs6, f6.get('cg_iters'), it_ok))
    r7 = run_wrapper(repo, pin, home, 'r7', wenv, timeout=900, attempt=4)
    st7 = (r7.rep or {}).get('store') or {}
    f7 = (r7.rep or {}).get('fields') or {}
    arm7 = os.path.join(r7.out, ARM + '.json')
    vals6 = real_sigma_values(arm6) if os.path.exists(arm6) else []
    bp7 = bundle_problems(r7.lg, vals6, home, sd_min=7) if vals6 else ['no arm 6']
    chk('R6b 시도 4 (실물 · 같은 저장본): 감시 셸 rc 0 · 판독 rc 0 · 상태 hit · 같은 파일 · meta 앞 목록 = 끝 목록 = 시도 3 의 끝 · 반복 수 = 시도 3 · 팔 JSON 바이트 = 시도 3 '
        '(저장본 적중이 결과를 바꾸지 않는다 · 이 CPU 대역 산술) · 묶음 꼴 · σ 없음',
        r7.rc == 0 and (r7.rep or {}).get('rc') == 0 and st7.get('status') == 'hit' and st7.get('file') == st6.get('file')
        and r7.meta.get('store_listing_before') == r6.meta.get('store_listing_after') == r7.meta.get('store_listing_after')
        and f7.get('cg_iters') == f6.get('cg_iters') and os.path.exists(arm6) and os.path.exists(arm7)
        and sha256_file(arm6) == sha256_file(arm7) and bp7 == [],
        (r7.rc, stop_line(r7), (r7.rep or {}).get('problems'), st7, f7.get('cg_iters'), bp7[:4]))
    # R2e (대조) 같은 실물 팔을 실제 S0 계획 (kgy 침대의 입력 지문) 으로 읽으면 다른 침대로 잡는다
    mod = load_reader(READER)
    rr = run_reader(mod, r.out, r.lg, run_r2, s0=True)
    chk('R2e (대조) 같은 팔 + 실제 S0 계획 = 다른 침대: rc 4 · bed_inputs_match_s0 False',
        rr.rc == 4 and fld(rr, 'bed_inputs_match_s0') is False, (rr.rc, (rr.rep or {}).get('problems')))
    # R4 GPU 를 못 쓰는 기계 (cupy 는 불러와지지만 풀이 모듈이 없다) + 등록 축: payload 가 CPU 로 내려가지 않고 멈춘다 (--step3-require-gpu)
    home4 = make_home('r4_home', shim_text=shim)
    run4 = os.path.join(home4, 'sdcp', KIT, S0_RUN)
    os.remove(os.path.join(run4, 'se_dump.npy'))
    E2E.make_bed(run4)
    write_text(os.path.join(home4, 'sdcp', KIT, 'run_mpm.sh'), kit_gpu)
    os.makedirs(os.path.join(home4, '_shim'))
    r4 = run_wrapper(repo_r2, pin_r2, home4, 'r4', wrapper_env(home4, None, SHIM_LOG=os.path.join(home4, '_shim'), PYTHONUTF8='1',
                                                        PYTHONIOENCODING='utf-8'), timeout=900)
    raw4 = read_text(os.path.join(r4.lg, 'runner.log')) if os.path.exists(os.path.join(r4.lg, 'runner.log')) else ''
    masked4 = ((r4.rep or {}).get('log') or {}).get('masked_lines') or []
    chk('R4a GPU 를 못 쓴다 + 등록 축: payload 가 풀지 않고 멈춘다 (STEP3 ABORT · CPU 폴백 없음) · 러너 rc 1 · 팔 없음 (출력 폴더 · 킷 런 폴더)',
        r4.rc == 1 and r4.meta.get('runner_rc') == '1' and 'STEP3 ABORT' in raw4 and 'CPU fallback' not in raw4
        and not glob.glob(os.path.join(r4.out, 'p2_*.json')) and not glob.glob(os.path.join(run4, 'p2_*.json*')),
        (r4.rc, r4.meta.get('runner_rc'), raw4[-900:]))
    chk('R4b 판독 rc 4 · 출처 none (읽을 팔이 없다) · 반복 수 칸 = 없음 · 멈춘 줄이 수를 가린 꼴로 보고에 있다 · 묶음',
        (r4.rep or {}).get('rc') == 4 and (r4.rep or {}).get('source') == 'none' and is_missing(((r4.rep or {}).get('fields') or {}).get('cg_iters'))
        and any('ABORT' in m and 'require-gpu' in m for m in masked4) and all(not has_digit(m) for m in masked4)
        and bundle_members(r4.lg)[0] is not None, ((r4.rep or {}).get('rc'), (r4.rep or {}).get('source'), masked4[-4:]))


def sweep_tagged():
    """이 시험의 표지가 있는 프로세스를 끝낸다 (변이 · 실패가 남긴 sleep 따위)."""
    me = os.getpid()
    for d in glob.glob('/proc/[0-9]*'):
        try:
            pid = int(os.path.basename(d))
            if pid == me:
                continue
            with open(os.path.join(d, 'environ'), 'rb') as f:
                if ('PROBE6_TEST_TAG=%s' % TAG).encode() in f.read().split(b'\0'):
                    os.kill(pid, signal.SIGKILL)
        except (OSError, ValueError):
            continue


def main():
    global ARGS, TD, TAG
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--only', default='', help='쉼표로 나눈 이름 접두 (예: T,M)')
    ap.add_argument('--no-real', action='store_true', help='실제 러너 묶음 (R) 을 뺀다: 뺀 것은 PASS 로 세지 않는다')
    ap.add_argument('--keep', action='store_true', help='임시 폴더를 남긴다')
    ap.add_argument('--ledger', default='', help='원장 읽기 시험 (S11) 이 읽을 파일 (기본 = 리포의 개발 탐침 원장)')
    ARGS = ap.parse_args()
    TD = tempfile.mkdtemp(prefix='probe6_')
    TAG = 'p6t%d' % os.getpid()
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    t0 = time.time()
    try:
        for tag, fn in CASES + [(t, f) for t, f in OPTIONAL if any(t.startswith(o) for o in only)]:
            if only and not any(tag.startswith(o) for o in only):
                continue
            print('\n── %s' % tag)
            t1 = time.time()
            try:
                fn()
            except Exception as e:                             # noqa: BLE001 · 준비물이 없을 때도 시험 단위로 기록
                chk('%s: 실행' % tag.split()[0], False, '%s: %s' % (type(e).__name__, e))
            finally:
                sweep_tagged()
            print('   (%.0f s)' % (time.time() - t1))
    finally:
        sweep_tagged()
        if ARGS.keep:
            print('\n  (임시 폴더 남김: %s)' % TD)
        else:
            shutil.rmtree(TD, ignore_errors=True)
    print('\n%d PASS · %d FAIL%s (%.0f s)' % (_ok, len(_fail), (' · 생략 %s' % ', '.join(_skipped)) if _skipped else '', time.time() - t0))
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② R 사슬 — 예측 12 단위 합성 끝-끝 + 기계 사이 이동 대조 (실제 러너 · 실제 payload · 아주 작은 픽스처 킷 · CPU · GPU 없음 · 2026-11-11).

근거 = 계획 `docs/reviews/rint2_siteq_remaining_plan_20261110.md` §4-4 (가) (나) · §10 의 3 번 (1저자 11-10 Q5 = 리포 시험을 먼저) · 판정문
`docs/reviews/codex_review_rint2_rr_round2_20261105.md` (작은 producer 자료로 전체 단위 집합 → 합치기 → 원장 판정 → 다시 판정을 한 번 잇는다 · 옮길 때는
허용하는 경로 이동과 같아야 할 바이트를 나눠 확인) · 설계 `docs/reviews/rint2_rr_fix_evidence_20261023/q9_predict_units_design.md` §3 · §4 · §8.
**시험만** — 사슬 · 러너 · payload · 물리는 바꾸지 않는다.  틀 = `scripts/test_rint_r_chain_e2e.py` (E18) 을 import (픽스처 킷 · git 고정물 체크아웃 · 가짜
python3 심 = 규율 관문 둘만 건너뜀 · payload 는 진짜로 돈다).  값 (σ) 은 읽어 견주기만 하고 화면에 쓰지 않는다 ("같다 / 다르다" 만).

  python3 scripts/test_rint_r_chain_e2e12.py                   # 전부 (실제 러너 100 회쯤 · 몇 분)
  python3 scripts/test_rint_r_chain_e2e12.py --keep            # 임시 폴더를 남긴다
  python3 scripts/test_rint_r_chain_e2e12.py --reuse <폴더>    # (개발용) 남긴 임시 폴더에서 끝난 단계를 건너뛴다

꼴 = 원장 공유 선택지 메모의 권고안 (**1저자 비준 전**): 기계마다 자기 바탕 폴더 (코드 체크아웃 사본 · 킷 사본 · 계획 · 등록 사본) · 원장 git 저장소는 한
번에 한 기계에만 있다 (쓰는 차례 = 가진 기계 · 넘길 때 = `git bundle` → 받는 쪽은 clone 또는 `pull --ff-only` · 보낸 쪽 사본은 세워 둔다) · 시도 폴더 ·
사다리 폴더는 바이트 그대로 복사해 옮긴다.  컨테이너 안 세 바탕 (이름표 kgy · gabia · v100 = 계획 허용 목록 값) 사이에서 돈다 — 실제 두 기계 · 실제 킷 ·
GPU · 네트워크 전송은 보지 않는다.

묶음 (사례):
  D1  생산 — 원장 시작 · 사다리 P0 (kgy) ∥ P1 (gabia) 를 겹쳐 돌림: kgy 가 P0 을 시작한 뒤 원장을 gabia 로 넘기고 (kgy 사본 = 세워 둠), 끝난 kgy 사슬은
      결과 줄을 쓰지 못한다 (rc 3) → 원장이 돌아온 뒤 `--stage recover --ledger` 가 결과 줄을 쓴다 (늦은 결과 줄 · 겹쳐 돌리기의 관찰)
  D2  길 1 — 한 기계 예측 (따로 원장 = 사다리 뒤에서 갈라 낸 사본 · 원장 하나 = 경로 하나) → 원장 판정 → 다시 판정 (따로 프로세스)
  D3  길 2 — 12 단위 (이름 = 계획 §4-2 표 · 기계 이름표 kgy · gabia · v100 돌아가며 · 원장 이어달리기 · 사다리 폴더를 그 기계로 복사) · 한 단위는 결과 전
      멈춤 (payload 전 실패) 뒤 다른 기계가 이어받음 · 한 단위는 자원 멈춤 뒤 같은 기계 · 같은 바탕에서 재실행 · 한 단위는 동시 실행 꼴 (시작 뒤 원장을
      넘김 → 늦은 결과 줄 = recover) → 시도 폴더를 kgy 로 복사 → 합치기 (넘침 없음) → 원장 판정 → 다시 판정 (따로 프로세스)
  D4  같음 — 두 길의 공개 칸 (상태 · 검사 · origin · 런 요청 칸 · 팔 공개 칸) · 판정 (이름 · 상태 · 표지) · 판정 결과 JSON (증서 칸 키의 예측 폴더 이름만
      다름) · 팔 JSON 바이트 (같은 체크아웃 = 같음 · 다른 체크아웃 = 픽스처 한 칸만 다름)
  D5  음성 대조 — 단위 하나 빠짐 (UNIT_MISSING) · 넘침 없는 다시 계산에 남는 넘침 점 시도 (UNIT_EXTRA) · 채택 시도 폴더 사본의 한 바이트 (ATTEMPT_LEDGER_
      MISMATCH · 폴더 요약 sha) · 출처 칸 (환경 같음 단위) 이 다른 단위 (UNIT_PROVENANCE_MISMATCH) · 풀기 전 관문 (--add) 의 같은 꼴
  D6  이동 대조 — 사다리 · 단위 시도 폴더 전부 · 원장 (묶음) 을 다른 바탕 (gabia) 으로 옮겨 합치기 · 원장 판정 · 다시 판정 (따로 프로세스) · 판정 폴더만
      옮김 · 옮긴 시도 폴더의 recover · 결과 전 시도 폴더를 빼고 옮김 · 같은 항목 폴더 둘 · 재실행의 기계 · 바탕 · 갈라진 원장 (두 사본에 각각 씀)
  D7  넘침 경로 — 판정 문턱 대역 (시험이 origin 넘침 판정을 한 모서리에서 뒤집는다 · 픽스처에는 실물 넘침이 없다) → 첫 합치기 EXPANSION_NEEDED (rc 4 ·
      결정 기록) → 넘침 점 셋 (실제 러너 origin8) → 끝 합치기 → 원장 판정
⚠ PASS = 교차 경로 (단위 집합 → 합치기 → 원장 판정 → 다시 판정) 와 이동 규칙이 실물 producer 출력에서 이어진다는 증거이지 R_j 값 · 판정의 물리 검증이
   아니다 (픽스처 σ 는 의미 없다).
"""
import argparse
import json
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
import run_contract as _RCG                                # noqa: E402 — ★ 11-12 같은 부류 (재리뷰 RCP2-06 · 본 세션 결정 11-12 밤) 이 시험 프로세스와 그 자식 (git ·
_RCG.drop_git_env()                                        #   payload · 러너) 은 부르는 쪽 환경의 GIT_* 를 물려받지 않는다 (scripts/test_git_env_isolation.py G6)

import test_rint_r_chain_e2e as E                           # noqa: E402 — 끝-끝 틀 (픽스처 · 고정물 체크아웃 · 사슬 부르기) · 사본 없음

RR, TR = E.RR, E.TR
MAXH = E.E2E_MAXH
MACHS = ('kgy', 'gabia', 'v100')                           # 계획 exec_policy.allowed_machines 의 값 (E.make_plan_and_reg) = 바탕 폴더 이름
#: 단위 이름 = 계획 §4-2 표 차례 (법칙 → c → R 역할) · 사슬 `UNIT_RE` · `unit_name`
UNIT_TABLE = [RR.unit_name(c, law, rr) for law in RR.LAWS for c in RR.CS for rr in RR.RJ_ROLES]
#: 도는 차례 = 표의 첫 단위 (다시 계산이 맨 먼저 요청하는 P0_c0_R_j_lo) 를 맨 끝에 — 그 앞의 이른 합치기가 첫 요청에서 UNIT_MISSING 으로 끝난다 (싸다)
UNIT_EXEC = UNIT_TABLE[1:] + UNIT_TABLE[:1]
PRE_STOP_UNIT = UNIT_EXEC[1]                               # 결과 전 멈춤 (payload 전 실패) 뒤 다른 기계가 이어받는 단위
RES_UNIT = UNIT_EXEC[2]                                    # 결과 뒤 자원 멈춤 (첫 풀이 끝 표지 뒤 MemoryError) 뒤 같은 기계 · 같은 바탕에서 재실행하는 단위
LATE_UNIT = UNIT_EXEC[3]                                   # 동시 실행 꼴 — 시작 기록 뒤 원장을 다음 기계로 넘기는 단위 (결과 줄 = 원장이 돌아온 뒤 recover)
LEDGER_NAME = RR.LEDGER_FILE
RUN_KEYS = ('name', 'role', 'kit', 'law', 'c', 'rj', 'arms', 'arm_list', 'variant', 'sv_cf', 'rc')
ARM_KEYS_NO_SHA = tuple(k for k in RR.ARM_PUBLIC if k != 'sha256')

#: 자원 멈춤 흉내 (시험 심이 감싸개 대신 부른다 · 생산 코드에 그런 스위치는 없다 · 신호 없음) — payload 가 첫 풀이 끝 표지를 쓴 뒤 증서 계산 자리에서 런 로그에
#: 자원 낱말 (MemoryError) 한 줄을 남기고 곧바로 끝난다 (os._exit · 진단본 · 팔 payload 를 쓰지 못한다 = 프로세스가 통째로 죽은 꼴) → 러너 rc ≠ 0 → 사슬
#: 원인 resource (재실행 자격).  ⚠ 파이썬 예외로 올리면 실물 payload 가 그것을 잡아 진단본 (`.unchecked/<팔>.json.failed`) 을 쓴다 = 검사 실패 흔적 = 재실행
#: 자격 False (등록 R §10-5 아 ⑨ 의 한정 그대로 · 이 시험을 만들 때 관찰)
FAULT_DRIVER = r'''
import os, runpy, sys
wrapper = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(wrapper)))
import step3_conv_cert as CC
def _oom(*a, **k):
    sys.stderr.write('MemoryError: e2e12 resource stop after the first-result marker\n')
    sys.stderr.flush()
    os._exit(1)
CC.certify = _oom
sys.argv = [wrapper] + sys.argv[2:]
runpy.run_path(wrapper, run_name='__main__')
'''

ARGS = None
SUF = ''                                                   # (개발용 --redo) 다시 도는 음성 대조의 출력 폴더 꼬리
W = {}                                                     # 세계 (바탕 · 번호 · 경로 · 끝난 단계) — --keep 이면 world.json 으로 남긴다
T = {}                                                     # 단계별 걸린 시간 (s)
BG = {}                                                    # 뒤에서 도는 사슬 프로세스 {이름: (Popen, 결과 파일, 로그)}
_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:1200]})' if why != '' else ''))
    return bool(cond)


# ═════════════════════════ 뒤에서 도는 사슬 (따로 프로세스 · 신호 없음) ═════════════════════════
#  단계 목록을 차례로 (사슬 main · 화면을 모아 결과 파일에) · over = 판정 문턱 대역 (D7 — origin 넘침 판정을 첫 모서리 (법칙 P0 · c 0) 에서 뒤집는다 ·
#  생산 코드에 그런 스위치는 없다) · 단계마다 here (사슬 폴더) · env 를 바꿀 수 있다 · {이름} = 앞 단계 화면에서 잡은 값 (ATTEMPT_ADDED n=…)
SEQ_DRIVER = r'''
import contextlib, io, json, os, re, sys, time
from pathlib import Path
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
sys.path.insert(0, cfg['scripts'])
import rint_r_chain as RR
RR.EXPECT_BACKEND = 'cpu'
if cfg.get('over'):
    _cnt = {'i': 0}
    _nf, _ok = RR.Predict.noop_first, RR.dbe_origin_ok
    def _nf2(self):
        _cnt['i'] = 0
        return _nf(self)
    def _ok2(*a, **k):
        i = _cnt['i']
        _cnt['i'] += 1
        r = _ok(*a, **k)
        return (False, r[1]) if i < 3 else r
    RR.Predict.noop_first, RR.dbe_origin_ok = _nf2, _ok2
cap, out = {}, []
for st in cfg['steps']:
    RR.HERE = Path(st.get('here') or cfg['here'])
    os.environ.clear()
    os.environ.update(st.get('env') or cfg['env'])
    argv = [str(x).format(**cap) for x in st['argv']]
    buf = io.StringIO()
    t0 = time.time()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            rc = RR.main(argv)
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 2
    so = buf.getvalue()
    if st.get('capture'):
        m = re.search(r'ATTEMPT_ADDED n=(\d+)', so)
        cap[st['capture']] = m.group(1) if m else 'none'
    out.append({'tag': st['tag'], 'rc': rc, 'so': so, 'seconds': round(time.time() - t0, 1), 'argv': argv})
    with open(cfg['result'] + '.tmp', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False)
    os.replace(cfg['result'] + '.tmp', cfg['result'])
    if 'want' in st and rc != st['want']:
        break
'''


def bg_start(name, m, steps, over=False):
    """뒤에서 사슬 단계들을 돈다 (새 인터프리터 · m = 기본 바탕) → BG[name]."""
    drv = os.path.join(E.TD, 'seq_driver.py')
    if not os.path.exists(drv):
        with open(drv, 'w', encoding='utf-8') as f:
            f.write(SEQ_DRIVER)
    res = os.path.join(E.TD, f'bg_{name}.json')
    cfg = os.path.join(E.TD, f'bg_{name}.cfg.json')
    with open(cfg, 'w', encoding='utf-8') as f:
        json.dump({'scripts': E.SCRIPTS, 'here': m['sd'], 'env': E.proc_env(m['root']), 'steps': steps, 'result': res, 'over': bool(over)}, f,
                  ensure_ascii=False)
    log = open(os.path.join(E.TD, f'bg_{name}.log'), 'w', encoding='utf-8')
    pr = subprocess.Popen([sys.executable, '-I', drv, cfg], cwd=m['root'], stdout=log, stderr=subprocess.STDOUT)
    BG[name] = (pr, res, log, time.time())


def bg_wait(name, timeout=2400):
    """뒤 프로세스가 끝나기를 기다린다 (신호를 보내지 않는다) → {단계 이름: {rc · so · seconds}} (못 끝남 · 결과 없음 = {})."""
    if name not in BG:                                     # (개발용 --reuse) 앞 실행이 남긴 결과 파일
        try:
            return {x['tag']: x for x in json.load(open(os.path.join(E.TD, f'bg_{name}.json'), encoding='utf-8'))}
        except (OSError, ValueError):
            return {}
    pr, res, log, t0 = BG[name]
    try:
        pr.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        pr.wait()                                          # 사슬 자신의 시간 상한 (--max-hours) 이 끝낸다 — 죽이지 않는다
    log.close()
    T[f'bg_{name}'] = round(time.time() - t0, 1)
    try:
        return {x['tag']: x for x in json.load(open(res, encoding='utf-8'))}
    except (OSError, ValueError):
        return {}


def step_env(m):
    return {'here': m['sd'], 'env': E.proc_env(m['root'])}


def wait_started(name, led, n, folder, timeout=300):
    """뒤 사슬 (BG[name]) 이 시도 n 의 시작 기록을 커밋하고 첫 러너를 띄울 때까지 기다린다 (그 뒤로 사슬은 끝날 때까지 원장을 건드리지 않는다) → 됐는가."""
    t_end = time.time() + timeout
    gd = os.path.join(folder, 'groups')
    while time.time() < t_end and BG[name][0].poll() is None:
        if (any(x.get('kind') == 'start' and x.get('n') == n for x in led_lines(led))
                and os.path.isdir(gd) and any(x.endswith('.launch.json') for x in os.listdir(gd))):
            return True
        time.sleep(0.1)
    return False


# ═════════════════════════ 도우미 ═════════════════════════
def jload(p):
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def call(m, argv):
    """사슬 main 을 이 프로세스 안에서 (그 기계의 체크아웃 = 사슬 폴더 · 킷 뿌리 · CPU) → (rc, 화면)."""
    return E.e2e_call(m['root'], m['sd'], argv)


def git(repo, *a):
    return E._git(repo, *a)


def led_lines(led):
    """원장 줄 (커밋된 판 = HEAD 의 원장 파일 — 덧붙이는 중인 작업 파일을 읽지 않는다)."""
    return [json.loads(x) for x in git(led, 'show', f'HEAD:{LEDGER_NAME}').splitlines()]


def led_result(led, n):
    return ([x for x in led_lines(led) if x.get('kind') == 'result' and x.get('n') == n] or [None])[0]


def stop_code(s):
    return ((s or {}).get('stop') or {}).get('code')


def ship(src, dst):
    """폴더를 바이트 그대로 다른 자리로 (기계 사이 옮김 흉내) → 두 쪽 폴더 요약이 같은가 (시험 쪽 독립 계산)."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copytree(src, dst, symlinks=True)
    return E.tree_digest(src) == E.tree_digest(dst)


def relay(src, dst, led_key='ledger'):
    """원장 이어달리기 — src 의 원장 저장소를 git 묶음으로 떠서 dst 로: dst 에 세워 둔 사본이 있으면 되살려 `pull --ff-only` · 없으면 clone · src 의 사본은
    세워 둔다 (이름을 바꿔 사슬이 쓰지 못하게 — 한 번에 한 기계만 원장을 쓴다) → 묶음 경로."""
    W['relay_n'] = W.get('relay_n', 0) + 1
    bd = os.path.join(E.TD, 'relay')
    os.makedirs(bd, exist_ok=True)
    b = os.path.join(bd, f'{W["relay_n"]:02d}_{src["name"]}_to_{dst["name"]}.bundle')
    br = git(src[led_key], 'symbolic-ref', '--short', 'HEAD')
    git(src[led_key], 'bundle', 'create', b, '--all')
    os.rename(src[led_key], src[led_key] + '.parked')
    if os.path.isdir(dst[led_key] + '.parked'):
        os.rename(dst[led_key] + '.parked', dst[led_key])
        git(dst[led_key], 'pull', '-q', '--ff-only', b, br)
    else:
        git(os.path.dirname(dst[led_key]), 'clone', '-q', b, dst[led_key])
    return b


def holder():
    return W['M'][W['holder']]


def take(m):
    """원장을 m 으로 (이미 가졌으면 그대로)."""
    if W['holder'] != m['name']:
        relay(holder(), m)
        W['holder'] = m['name']


def a_add(m, target, led=None, label=None, resume=None):
    return ['--stage', 'ledger', '--ledger', led or m['ledger'], '--add', '--ledger-target', target, '--machine', label or m['label'],
            '--plan', m['plan'], '--runner', m['runner'], '--root', m['root']] + (['--resume', str(resume)] if resume is not None else [])


def add(m, target, **kw):
    rc, so = call(m, a_add(m, target, **kw))
    x = re.search(r'ATTEMPT_ADDED n=(\d+)', so)
    return rc, (int(x.group(1)) if x else None), so


def a_ladder(m, law, n, led=None):
    return ['--stage', 'ladder', '--law', law, '--target', str(RR.TARGET_SBE_MS), '--runner', m['runner'], '--root', m['root'], '--plan', m['plan'],
            '--s0-plan', m['s0_plan'], '--registration', m['reg'], '--max-hours', MAXH, '--out', m['lad'][law], '--machine', m['label'],
            '--s0-stage2-report', m['s0r2'], '--s0-stage1-report', m['s0r1'], '--ledger', led or m['ledger'], '--attempt', str(n)]


def lads_of(m):
    return [os.path.join(m['lad'][law], f'attempt_{W["lad_n"][law]}') for law in RR.LAWS]


def a_pred(m, out, extra, label=None):
    return ['--stage', 'predict', '--ladders'] + lads_of(m) + ['--runner', m['runner'], '--root', m['root'], '--registration', m['reg'],
                                                               '--max-hours', MAXH, '--out', out, '--machine', label or m['label']] + list(extra)


def a_merge(m, out, paths, led=None, expand=None):
    return a_pred(m, out, ['--ledger', led or m['ledger'], '--merge'] + list(paths) + (['--expand', expand] if expand else []))


def a_verdict(m, pred, out, led=None):
    return ['--stage', 'verdict', '--runs'] + lads_of(m) + [pred, '--root', m['root'], '--registration', m['reg'], '--ledger', led or m['ledger'],
                                                            '--out', out]


def a_reverify(m, vdir, out):
    return ['--stage', 'verdict', '--reverify', vdir, '--root', m['root'], '--out', out]


def merge_paths(m):
    """그 기계에서 합칠 시도 폴더 바탕 — 자기 단위 바탕 + 다른 기계에서 받은 사본 바탕."""
    return [p for p in [m['units']] + [m['inbox'][x] for x in MACHS if x != m['name']] if os.path.isdir(p)]


def proj_runs(s, arm_keys=RR.ARM_PUBLIC):
    """요약의 런 → 요청 칸 · rc · 팔 공개 칸 (경로 · 기계 · 시간 · 출처 칸은 뺀다)."""
    return [dict({k: r.get(k) for k in RUN_KEYS}, arms=[{k: a.get(k) for k in arm_keys} for a in r.get('arms_read') or []])
            for r in (s or {}).get('runs') or []]


def arm_paths(folder, s):
    return [os.path.join(folder, r['outdir'], a['file']) for r in (s or {}).get('runs') or [] for a in r.get('arms_read') or []]


def save_world():
    with open(os.path.join(E.TD, 'world.json'), 'w', encoding='utf-8') as f:
        json.dump(W, f, ensure_ascii=False, indent=1)


def phase(name):
    """단계 꾸밈 — 끝난 단계 (--reuse) 는 건너뛴다 · 걸린 시간을 적는다."""
    def deco(fn):
        def run():
            if name in W.get('done', []):
                print(f'    ({name} — 남긴 세계에서 건너뜀)')
                return
            t0 = time.time()
            fn()
            T[name] = round(time.time() - t0, 1)
            W.setdefault('done', []).append(name)
            save_world()
        return run
    return deco


# ═════════════════════════ 세계 (세 바탕 + 한 기계 비교 바탕) ═════════════════════════
def make_machine(name, ws0, files, label=None, code_of=None):
    """바탕 하나 = 그 기계의 홈: 코드 체크아웃 사본 (고정물 저장소를 바이트 그대로 — 절대 경로만 다르다 · code_of = 다른 바탕의 체크아웃을 같이 쓴다) ·
    킷 사본 (sdcp/) · 계획 · S0 계획 · S0 보고 · 등록 사본 (바이트 그대로)."""
    home = os.path.join(E.TD, name)
    code = code_of['code'] if code_of else os.path.join(home, 'dem-ca1')
    if not code_of:
        shutil.copytree(E.CODEREPO['repo'], code, symlinks=True)
    root = os.path.join(home, 'sdcp')
    shutil.copytree(ws0, root, symlinks=True)
    for k, src in files.items():
        shutil.copy2(src, os.path.join(root, os.path.basename(src)))
    m = {'name': name, 'label': label or name, 'home': home, 'code': code, 'sd': os.path.join(code, 'scripts'),
         'runner': os.path.join(code, 'scripts', 'sdcp_gain_vox015_8arm.sh'), 'root': root,
         'ledger': os.path.join(root, 'ca1_ledger'), 'lad': {law: os.path.join(root, f'ca1_ladder_{law}') for law in RR.LAWS},
         'units': os.path.join(root, 'ca1_units'), 'inbox': {x: os.path.join(root, f'ca1_units_from_{x}') for x in MACHS if x != name}}
    m.update({k: os.path.join(root, os.path.basename(src)) for k, src in files.items()})
    return m


@phase('setup')
def p_setup():
    ws0 = E.make_root('w0')
    pp, sp, rp = E.make_plan_and_reg(ws0)
    E.code_repo()
    W['coderepo'] = {'repo': E.CODEREPO['repo'], 'sd': E.CODEREPO['sd']}
    files = {'plan': pp, 's0_plan': sp, 'reg': rp, 's0r2': os.path.join(E.TD, 's0_stage2.json'), 's0r1': os.path.join(E.TD, 's0_stage1.json')}
    W['M'] = {x: make_machine(x, ws0, files) for x in MACHS}
    #  한 기계 비교 바탕 (길 1) — kgy 이름표 · kgy 체크아웃을 같이 쓴다 (팔 JSON 바이트 대조 = 같은 체크아웃) · 킷 · 원장 · 출력은 따로
    W['M']['one'] = make_machine('one', ws0, files, label='kgy', code_of=W['M']['kgy'])
    W['plan_sha'] = E._sha(pp)


# ═════════════════════════ D1 생산 — 원장 · 사다리 둘 (겹쳐 돌림 · 늦은 결과 줄) ═════════════════════════
@phase('ladders')
def p_ladders():
    kgy, gabia = W['M']['kgy'], W['M']['gabia']
    os.makedirs(kgy['ledger'])
    subprocess.run(['git', 'init', '-q', kgy['ledger']], check=True, capture_output=True)
    rc0, _so = call(kgy, ['--stage', 'ledger', '--ledger', kgy['ledger'], '--init', '--plan', kgy['plan']])
    W['holder'] = 'kgy'
    rc1, n1, so1 = add(kgy, 'ladder:P0')
    bg_start('ladP0', kgy, [{'tag': 'ladder', 'argv': a_ladder(kgy, 'P0', n1)}])
    #  kgy 사슬이 시작 기록을 커밋하고 첫 러너를 띄울 때까지 (그 뒤로 사슬은 끝날 때까지 원장을 건드리지 않는다)
    f0 = os.path.join(kgy['lad']['P0'], f'attempt_{n1}')
    started = wait_started('ladP0', kgy['ledger'], n1, f0)
    take(gabia)                                            # kgy 사슬이 도는 동안 원장을 gabia 로 (kgy 사본 = 세워 둠)
    rc2, n2, so2 = add(gabia, 'ladder:P1')
    rc3, so3 = call(gabia, a_ladder(gabia, 'P1', n2))
    bg = bg_wait('ladP0').get('ladder') or {}
    f1 = os.path.join(gabia['lad']['P1'], f'attempt_{n2}')
    s0, s1 = jload(os.path.join(f0, 'ladder_summary.json')) or {}, jload(os.path.join(f1, 'ladder_summary.json')) or {}
    late_before = led_result(gabia['ledger'], n1)
    take(kgy)                                              # 원장이 kgy 로 돌아온다 (빨리 감기) → 늦은 결과 줄
    rc4, so4 = call(kgy, ['--stage', 'recover', '--out', f0, '--ledger', kgy['ledger']])
    r0, r1 = led_result(kgy['ledger'], n1) or {}, led_result(kgy['ledger'], n2) or {}
    kinds = [(x.get('kind'), x.get('n')) for x in led_lines(kgy['ledger'])]
    W['lad_n'] = {'P0': n1, 'P1': n2}
    W['lad_home'] = {'P0': 'kgy', 'P1': 'gabia'}
    print(f'    보고 D1 — 원장 rc {[rc0, rc1, rc2]} · 사다리 P0 (kgy · 뒤 프로세스) rc {bg.get("rc")} · {s0.get("status")} (런 {len(s0.get("runs") or [])} · '
          f'{bg.get("seconds")} s) · P1 (gabia) rc {rc3} · {s1.get("status")} (런 {len(s1.get("runs") or [])}) · recover rc {rc4} · 원장 줄 {kinds}')
    chk('D1a 생산 — 원장 --init · --add 둘 rc 0 · 사다리 P0 (kgy) · P1 (gabia) = CALIBRATED · 마지막 런 = sbe_noop (사다리 끝 no-op) · P1 결과 줄 = '
        'completed · by chain · 폴더 요약 sha = 시험 쪽 독립 계산',
        [rc0, rc1, rc2, rc3] == [0, 0, 0, 0] and started and s0.get('status') == 'CALIBRATED' and s1.get('status') == 'CALIBRATED'
        and all(((s.get('runs') or [{}])[-1]).get('role') == 'sbe_noop' for s in (s0, s1))
        and r1.get('status') == 'completed' and r1.get('by') == 'chain' and r1.get('folder_sha256') == E.tree_digest(f1),
        (rc0, rc1, rc2, rc3, started, s0.get('status'), s1.get('status'), r1, so1[-200:], so2[-200:], so3[-400:]))
    chk('D1b 겹쳐 돌리기 (관찰) — kgy 가 P0 을 시작 (시작 기록 커밋) 한 뒤 원장을 gabia 로 넘겼다 (kgy 사본 = 세워 둠): 끝난 kgy 사슬 = rc 3 (결과 줄을 쓰지 '
        '못함 · 요약 CALIBRATED 는 남음) · 넘겨받은 원장에 P0 결과 줄 없음 · 원장이 돌아온 뒤 --stage recover --ledger rc 0 → 결과 줄 completed · 결과 뒤 · by '
        'recover · 폴더 요약 sha = 독립 계산 · 원장 줄 차례 = 머리 · P0 항목 · P0 시작 · P1 항목 · P1 시작 · P1 결과 · P0 결과 (한 줄 역사 · 덧붙이기만)',
        bg.get('rc') == 3 and late_before is None and rc4 == 0 and r0.get('status') == 'completed' and r0.get('side') == 'post'
        and r0.get('by') == 'recover' and r0.get('folder_sha256') == E.tree_digest(f0)
        and kinds == [('header', None), ('entry', n1), ('start', n1), ('entry', n2), ('start', n2), ('result', n2), ('result', n1)],
        (bg.get('rc'), (bg.get('so') or '')[-500:], late_before, rc4, so4[-400:], r0, kinds))
    #  사다리 폴더를 다른 바탕으로 (바이트 그대로) — 단위 · 합치기 · 판정이 그 기계에서 입력으로 받는다
    ok = []
    for law, src_m, n in (('P0', kgy, n1), ('P1', gabia, n2)):
        src = os.path.join(src_m['lad'][law], f'attempt_{n}')
        for x in MACHS + ('one',):
            if x != src_m['name']:
                ok.append(ship(src, os.path.join(W['M'][x]['lad'][law], f'attempt_{n}')))
    W['ship_lad_ok'] = all(ok)


# ═════════════════════════ D2 길 1 — 한 기계 예측 (따로 원장) → 원장 판정 (뒤에서) ═════════════════════════
@phase('one_start')
def p_one_start():
    kgy, one = W['M']['kgy'], W['M']['one']
    git(os.path.dirname(one['ledger']), 'clone', '-q', kgy['ledger'], one['ledger'])   # 사다리 둘 뒤에서 갈라 낸 원장 사본 (원장 하나 = 경로 하나)
    rc, n, so = add(one, 'predict')
    base = os.path.join(one['root'], 'ca1_predict')
    W['one'] = {'n': n, 'add_rc': rc, 'pred': os.path.join(base, f'attempt_{n}'), 'verdict': os.path.join(one['root'], 'ca1_verdict'), 'so': so[-300:]}
    bg_start('one', one, [{'tag': 'predict', 'want': 0, 'argv': a_pred(one, base, ['--ledger', one['ledger'], '--attempt', str(n)])},
                          {'tag': 'verdict', 'argv': a_verdict(one, W['one']['pred'], W['one']['verdict'])}])


# ═════════════════════════ D3 길 2 — 12 단위 (세 바탕 · 원장 이어달리기) → 합치기 → 원장 판정 ═════════════════════════
def run_unit(m, name, env=None, base=None, resume=None, led=None):
    """단위 시도 하나 (그 기계 · --add → 시도) → {add_rc · n · rc · folder · so} · env = 그 시도 동안만 둘 환경 변수 (시험 심의 고장 흉내)."""
    rca, n, soa = add(m, f'unit:{name}', resume=resume, led=led)
    if n is None:
        return {'add_rc': rca, 'n': None, 'rc': None, 'folder': None, 'so': soa[-400:]}
    base = base or m['units']
    os.environ.update(env or {})
    try:
        rcu, sou = call(m, a_pred(m, base, ['--ledger', led or m['ledger'], '--attempt', str(n), '--unit', name]))
    finally:
        for k in (env or {}):
            os.environ.pop(k, None)
    return {'add_rc': rca, 'n': n, 'rc': rcu, 'folder': os.path.join(base, f'attempt_{n}'), 'so': soa[-200:] + sou[-400:]}


def run_unit_late(m, name, nxt):
    """단위 시도 하나를 동시 실행 꼴로 — --add (이 프로세스) → 시도 (뒤 프로세스) → 시작 기록이 커밋되고 첫 러너가 뜬 뒤 원장을 다음 기계 nxt 로 넘긴다
    (이 기계 사본 = 세워 둠) → 끝난 사슬은 결과 줄을 쓰지 못한다 (rc 3 · 단위 요약은 남는다) → 결과 줄 = 원장이 이 기계로 돌아온 뒤 `late_recover`."""
    rca, n, soa = add(m, f'unit:{name}')
    if n is None:
        return {'add_rc': rca, 'n': None, 'rc': None, 'folder': None, 'so': soa[-400:]}
    folder = os.path.join(m['units'], f'attempt_{n}')
    bg_start('unit_late', m, [{'tag': 'unit', 'argv': a_pred(m, m['units'], ['--ledger', m['ledger'], '--attempt', str(n), '--unit', name])}])
    started = wait_started('unit_late', m['ledger'], n, folder)
    take(nxt)                                              # 단위가 도는 동안 원장을 다음 기계로 (이 기계 사본 = 세워 둠)
    bg = bg_wait('unit_late').get('unit') or {}
    W['late'] = {'unit': name, 'm': m['name'], 'n': n, 'folder': folder, 'started': started, 'rc': bg.get('rc'),
                 'gone': led_result(nxt['ledger'], n) is None, 'so': (bg.get('so') or '')[-500:]}
    return {'add_rc': rca, 'n': n, 'rc': bg.get('rc'), 'folder': folder, 'so': soa[-200:] + (bg.get('so') or '')[-400:]}


def late_recover(m):
    """원장이 그 기계로 돌아왔다 → 동시 실행 꼴로 돈 단위의 늦은 결과 줄 (`--stage recover --ledger`)."""
    lt = W['late']
    lt['before'] = led_result(m['ledger'], lt['n'])        # 돌아온 원장에 그 결과 줄이 아직 없다
    lt['rc_recover'], so = call(m, ['--stage', 'recover', '--out', lt['folder'], '--ledger', m['ledger']])
    lt['so_recover'] = so[-400:]


def note(m, name, r, kind):
    """끝난 단위 시도를 적고, 다른 기계에서 돈 것이면 시도 폴더를 kgy 로 바이트 그대로 옮긴다 (합치기는 kgy 에서) → kgy 쪽 경로."""
    kgy = W['M']['kgy']
    if r['folder'] is None:                                # --add 가 거부됐다 (시도 없음) — 적기만 한다 (단언이 잡는다)
        W['att'].append({'n': None, 'unit': name, 'm': m['name'], 'folder': None, 'kgy': None, 'kind': kind, 'shipped': False})
        return None, False
    fk = r['folder'] if m['name'] == 'kgy' else os.path.join(kgy['inbox'][m['name']], os.path.basename(r['folder']))
    ok = True if fk == r['folder'] else (os.path.isdir(r['folder']) and ship(r['folder'], fk))
    W['att'].append({'n': r['n'], 'unit': name, 'm': m['name'], 'folder': r['folder'], 'kgy': fk, 'kind': kind, 'shipped': ok})
    return fk, ok


def early_merge():
    """끝 단위 전의 이른 합치기 (음성 대조 — 단위 하나 빠짐) + 그 시점 원장 사본 (D5 출처 대조용)."""
    kgy = W['M']['kgy']
    take(kgy)
    out = os.path.join(kgy['root'], 'ca1_merge_early')
    rc, so = call(kgy, a_merge(kgy, out, merge_paths(kgy)))
    s = jload(os.path.join(out, 'predict_summary.json')) or {}
    W['early'] = {'rc': rc, 'status': s.get('status'), 'code': stop_code(s), 'run': (s.get('stop') or {}).get('run'), 'n_runs': len(s.get('runs') or []),
                  'so': so[-600:]}
    W['fork11'] = os.path.join(kgy['root'], 'ca1_ledger_fork11')
    git(kgy['root'], 'clone', '-q', kgy['ledger'], W['fork11'])


def res_fork_obs(m, name, r0):
    """재실행의 기계 · 바탕 규칙 관찰 — 그 기계 원장의 사본에서만 (주 원장에 거부 항목을 남기지 않는다): 다른 기계 이름표의 재실행 항목 · 다른 바탕의 재실행
    시도 · 그 거부 뒤 원 바탕의 재실행 시도."""
    fk = os.path.join(m['root'], 'ca1_ledger_resfork')
    git(m['root'], 'clone', '-q', m['ledger'], fk)
    h0 = git(fk, 'rev-parse', 'HEAD')
    other = [x for x in MACHS if x != m['label']][0]
    rcl, nl, sol = add(m, f'unit:{name}', led=fk, label=other, resume=r0['n'])
    kept = git(fk, 'rev-parse', 'HEAD') == h0
    w = run_unit(m, name, base=os.path.join(m['root'], 'ca1_units_other'), resume=r0['n'], led=fk)
    rw = led_result(fk, w['n']) if w['n'] else None
    b = run_unit(m, name, resume=r0['n'], led=fk)
    rb = led_result(fk, b['n']) if b['n'] else None
    rej = jload(os.path.join(b['folder'] or '/nonexistent', 'rejected.json')) or {}
    if b['folder'] and os.path.isdir(b['folder']):
        shutil.rmtree(b['folder'])                         # 원장 사본의 시도 흔적을 주 바탕에 남기지 않는다
    W['res_fork'] = {'label': (rcl, nl, kept, sol[-300:]), 'wrong': (w['add_rc'], w['rc'], rw), 'back': (b['add_rc'], b['rc'], rb, str(rej.get('cause'))[:300])}


@phase('units')
def p_units():
    M = W['M']
    W['units'], W['att'] = {}, []
    drv = os.path.join(E.TD, 'fault_driver.py')
    with open(drv, 'w', encoding='utf-8') as f:
        f.write(FAULT_DRIVER)
    for i, name in enumerate(UNIT_EXEC):
        m = M[MACHS[i % len(MACHS)]]
        if i == len(UNIT_EXEC) - 1:
            early_merge()
        if name == PRE_STOP_UNIT:                          # 결과 전 멈춤 — 앞 차례 기계에서 payload 가 풀이 전에 실패 (시험 심이 payload 줄에서 rc 7)
            pm = M[MACHS[(i - 1) % len(MACHS)]]
            take(pm)
            r = run_unit(pm, name, env={'SHIM_PAYLOAD_EXIT': '7'})
            note(pm, name, r, 'pre')
            W['pre'] = dict(r, m=pm['name'])
        take(m)
        if 'late' in W and W['late']['m'] == m['name'] and 'rc_recover' not in W['late']:
            late_recover(m)                                # 원장이 그 기계로 돌아온 첫 차례 — 늦은 결과 줄
        chain = []
        if name == RES_UNIT:                               # 결과 뒤 자원 멈춤 (표지 뒤 MemoryError) → 같은 기계 · 같은 바탕에서 재실행
            r0 = run_unit(m, name, env={'SHIM_DELAY_DRIVER': drv})
            note(m, name, r0, 'stopped')
            chain.append(r0['n'])
            W['res'] = dict(r0, m=m['name'])
            res_fork_obs(m, name, r0)
            r = run_unit(m, name, resume=r0['n'])
        elif name == LATE_UNIT:                            # 동시 실행 꼴 — 시작 뒤 원장을 다음 차례 기계로 넘긴다 (결과 줄은 원장이 돌아온 뒤)
            r = run_unit_late(m, name, M[MACHS[(i + 1) % len(MACHS)]])
        else:
            r = run_unit(m, name)
        fk, ok = note(m, name, r, 'done')
        W['units'][name] = dict(r, m=m['name'], kgy=fk, shipped=ok, chain=chain + [r['n']])
    take(M['kgy'])


@phase('merge')
def p_merge():
    kgy = W['M']['kgy']
    out = os.path.join(kgy['root'], 'ca1_predict')
    t0 = time.time()
    rc, so = call(kgy, a_merge(kgy, out, merge_paths(kgy)))
    T['merge_only'] = round(time.time() - t0, 1)
    W['merge'] = {'out': out, 'rc': rc, 'so': so[-800:]}
    vd = os.path.join(kgy['root'], 'ca1_verdict')
    rcv, sov = call(kgy, a_verdict(kgy, out, vd))
    W['verdict'] = {'out': vd, 'rc': rcv, 'so': sov[-800:]}


def unit_label(name):
    return W['M'][W['units'][name]['m']]['label']


def t_units():
    M = W['M']
    kgy = M['kgy']
    bad = []
    for name in UNIT_TABLE:
        u = W['units'].get(name) or {}
        s = jload(os.path.join(u.get('folder') or '/nonexistent', 'unit_summary.json')) or {}
        rl = led_result(kgy['ledger'], u.get('n')) or {}
        ok = (u.get('add_rc') == 0 and u.get('rc') == (3 if name == LATE_UNIT else 0) and s.get('status') == 'UNIT_DONE'
              and s.get('machine') == unit_label(name)
              and [(x.get('name'), x.get('role'), x.get('rc')) for x in s.get('runs') or []] == [('U01_corner', 'corner', 0), ('U02_origin', 'origin', 0)]
              and rl.get('status') == 'completed' and rl.get('side') == 'post' and u.get('shipped') is True
              and rl.get('folder_sha256') == E.tree_digest(u['kgy']))
        if not ok:
            bad.append((name, u.get('add_rc'), u.get('rc'), s.get('status'), s.get('machine'), rl.get('status'), u.get('shipped'), u.get('so')))
    labels = [unit_label(n) for n in UNIT_EXEC]
    print(f'    보고 D3 — 단위 {len(W["units"])} (도는 차례 기계 {labels}) · 단위 시도 {len(W["att"])} · 원장 이어달리기 {W.get("relay_n")} 번 · 결과 전 멈춤 '
          f'시도 {W["pre"]["n"]} ({W["pre"]["m"]}) → 채택 {W["units"][PRE_STOP_UNIT]["n"]} ({W["units"][PRE_STOP_UNIT]["m"]}) · 자원 멈춤 시도 {W["res"]["n"]} '
          f'({W["res"]["m"]}) → 재실행 {W["units"][RES_UNIT]["n"]}')
    chk('D3a 12 단위 (이름 = 계획 §4-2 표 · 기계 이름표 kgy · gabia · v100 돌아가며 · 단위마다 그 기계의 체크아웃 · 킷 · 사다리 폴더 사본 · 원장 = 이어달리기) — '
        '--add rc 0 · 시도 rc 0 (동시 실행 꼴로 돈 단위 하나만 rc 3 = D3h) · UNIT_DONE · 런 = U01_corner · U02_origin (rc 0) · 요약 기계 = 이름표 · 결과 줄 '
        'completed · 결과 뒤 · 폴더 요약 sha = kgy 로 옮긴 사본의 독립 계산 (옮긴 바이트 = 원 바이트) · 사다리 폴더 사본 = 원 바이트',
        not bad and len(W['units']) == 12 and sorted(W['units']) == sorted(UNIT_TABLE) and W.get('ship_lad_ok') is True
        and sorted(set(labels)) == sorted(MACHS) and all(a['shipped'] for a in W['att']), (bad[:2], W.get('ship_lad_ok')))
    pre = W['pre']
    sp = jload(os.path.join(pre['folder'], 'unit_summary.json')) or {}
    rp = led_result(kgy['ledger'], pre['n']) or {}
    chk('D3b 결과 전 멈춤 뒤 다른 기계가 이어받음 — 그 단위 첫 시도 (kgy · payload 가 풀이 전에 rc 7) = 시도 rc 3 · STOPPED RUNNER_RC · 결과 줄 stopped · 결과 전 · '
        '재실행 자격 False (표지 · payload 없음) → 같은 단위 새 항목 (gabia) --add rc 0 (채택 전) · 완주',
        pre['add_rc'] == 0 and pre['rc'] == 3 and sp.get('status') == 'STOPPED' and stop_code(sp) == 'RUNNER_RC' and rp.get('status') == 'stopped'
        and rp.get('side') == 'pre' and rp.get('resume_ok') is False and W['units'][PRE_STOP_UNIT]['m'] != pre['m']
        and W['units'][PRE_STOP_UNIT]['chain'] == [pre['n'] + 1], (pre, sp.get('status'), stop_code(sp), rp))
    res, u = W['res'], W['units'][RES_UNIT]
    sr = jload(os.path.join(res['folder'], 'unit_summary.json')) or {}
    rr = led_result(kgy['ledger'], res['n']) or {}
    s2 = jload(os.path.join(u['folder'], 'unit_summary.json')) or {}
    rs = s2.get('resume') or {}
    chk('D3g 결과 뒤 자원 멈춤 뒤 재실행 (같은 기계 · 같은 바탕) — 그 단위 첫 시도 (v100 · 첫 풀이 끝 표지 뒤 payload 가 진단본 없이 끝남 · 런 로그에 '
        'MemoryError) = 시도 rc 3 · STOPPED RUNNER_RC · 결과 줄 stopped · 결과 뒤 · 원인 resource · 재실행 자격 True → --add --resume rc 0 · 재실행 시도 rc 0 · '
        'UNIT_DONE · resume 칸 (원 시도 · 복사 0 · 새로 = U01_corner · 결정성 가정) · 재실행 사슬 = [멈춘 시도, 재실행]',
        res['add_rc'] == 0 and res['rc'] == 3 and sr.get('status') == 'STOPPED' and stop_code(sr) == 'RUNNER_RC' and rr.get('status') == 'stopped'
        and rr.get('side') == 'post' and rr.get('cause') == 'resource' and rr.get('resume_ok') is True and u['add_rc'] == 0 and u['rc'] == 0
        and rs.get('from') == res['n'] and rs.get('copied') == [] and rs.get('rerun') == 'U01_corner' and rs.get('determinism') == 'assumed'
        and u['chain'] == [res['n'], u['n']], (res, rr, rs, u.get('so')))
    lines = led_lines(kgy['ledger'])
    lt = W.get('late') or {}
    rl = led_result(kgy['ledger'], lt.get('n')) or {}
    ls = jload(os.path.join(lt.get('folder') or '/nonexistent', 'unit_summary.json')) or {}
    order = [(x.get('kind'), x.get('n')) for x in lines]
    between = ([n for k, n in order[order.index(('start', lt['n'])) + 1:order.index(('result', lt['n']))] if k == 'result']
               if ('start', lt.get('n')) in order and ('result', lt.get('n')) in order else [])
    chk('D3h 단위 하나를 동시 실행 꼴로 (시작 기록이 커밋된 뒤 원장을 다음 기계로 넘김 · 이 기계 사본 = 세워 둠) — 끝난 단위 사슬 = rc 3 (결과 줄을 쓰지 못함 · '
        '단위 요약 UNIT_DONE 은 남음) · 넘겨받은 원장 · 돌아온 원장에 그 결과 줄 없음 · 그 사이 다른 두 기계의 단위가 원장에 들어가 끝남 (결과 줄 둘) · 원장이 '
        '돌아온 뒤 --stage recover --ledger rc 0 → 결과 줄 completed · 결과 뒤 · by recover · 폴더 요약 sha = 독립 계산 (합치기 D3d 가 그 단위를 채택한다)',
        lt.get('started') is True and lt.get('rc') == 3 and ls.get('status') == 'UNIT_DONE' and lt.get('gone') is True and 'before' in lt
        and lt['before'] is None and lt.get('rc_recover') == 0 and rl.get('status') == 'completed' and rl.get('side') == 'post'
        and rl.get('by') == 'recover' and rl.get('folder_sha256') == E.tree_digest(lt['folder']) and len(between) == 2,
        ({k: lt.get(k) for k in ('unit', 'm', 'n', 'started', 'rc', 'gone', 'before', 'rc_recover', 'so_recover')}, rl, between, (lt.get('so') or '')[-300:]))
    n_commits = int(git(kgy['ledger'], 'rev-list', '--count', 'HEAD'))
    merges = git(kgy['ledger'], 'rev-list', '--merges', 'HEAD')
    kinds = [x['kind'] for x in lines]
    n_att = 2 + len(W['att'])
    chk('D3c 원장 (이어달리기 뒤 kgy) — 한 줄 역사: 커밋 수 = 원장 줄 수 · 병합 커밋 없음 · 항목 = 사다리 2 + 단위 시도 14 (완주 12 · 결과 전 멈춤 1 · 자원 멈춤 '
        '1) · 시작 기록 · 결과 줄 = 항목 수 · 시작 기록의 바탕 = 그 시도를 돈 기계 바탕의 절대 경로 (kgy · gabia · v100 이 섞여 있다)',
        n_commits == len(lines) and merges == '' and len(W['att']) == 14 and kinds.count('entry') == n_att and kinds.count('start') == n_att
        and kinds.count('result') == n_att
        and all(os.path.realpath(x['base']) == os.path.realpath(os.path.dirname(a['folder']))
                for a in W['att'] for x in lines if x['kind'] == 'start' and x['n'] == a['n']),
        (n_commits, len(lines), merges[:60], kinds.count('entry'), kinds.count('start'), kinds.count('result')))
    f = W['res_fork']
    print(f'    보고 D6 (재실행의 기계 · 바탕 · 원장 사본에서) — 다른 이름표 --add rc {f["label"][0]} · 다른 바탕 시도 rc {f["wrong"][1]} '
          f'({((f["wrong"][2] or {}).get("stop") or {}).get("code")}) · 그 뒤 원 바탕 시도 rc {f["back"][1]} ({((f["back"][2] or {}).get("stop") or {}).get("code")})')
    chk('D6i 이동 (거부 · 재실행은 같은 기계 · 같은 바탕에서만 · 원장 사본에서 관찰) — 다른 기계 이름표의 재실행 항목 = --add rc 3 RESUME_NOT_ALLOWED (원장 '
        '무변경) · 다른 바탕 (--out) 의 재실행 시도 = rc 3 · 결과 줄 rejected · 결과 전 · RESUME_NOT_ALLOWED (원천 = 그 바탕의 재실행 사슬 끝 시도 폴더가 없다) · '
        '그 거부 뒤 원 바탕의 재실행 시도도 = rc 3 · rejected · RESUME_NOT_ALLOWED (앞 거부 시도의 폴더가 같은 바탕에 없다 — 관찰)',
        f['label'][0] == 3 and f['label'][1] is None and f['label'][2] is True and 'RESUME_NOT_ALLOWED' in f['label'][3]
        and f['wrong'][0] == 0 and f['wrong'][1] == 3 and (f['wrong'][2] or {}).get('status') == 'rejected' and (f['wrong'][2] or {}).get('side') == 'pre'
        and ((f['wrong'][2] or {}).get('stop') or {}).get('code') == 'RESUME_NOT_ALLOWED'
        and f['back'][0] == 0 and f['back'][1] == 3 and (f['back'][2] or {}).get('status') == 'rejected'
        and ((f['back'][2] or {}).get('stop') or {}).get('code') == 'RESUME_NOT_ALLOWED' and '같은 바탕' in f['back'][3], f)


def t_merge():
    M = W['M']
    kgy = M['kgy']
    ms = jload(os.path.join(W['merge']['out'], 'predict_summary.json')) or {}
    mg = ms.get('merge') or {}
    runs = ms.get('runs') or []
    names = [x.get('name') for x in runs]
    want_names = [f'P{i:02d}_corner' for i in range(1, 13)] + [f'P{i:02d}_origin' for i in range(13, 25)]
    outs_ok = all(isinstance(x.get('outdir'), str) and x['outdir'].startswith('units/unit-') and os.path.isdir(os.path.join(W['merge']['out'], x['outdir']))
                  for x in runs)
    mach = {t: (u or {}).get('machine') for t, u in (mg.get('units') or {}).items()}
    want_mach = {f'unit:{n}': unit_label(n) for n in UNIT_TABLE}
    att = {t: ((u or {}).get('attempt'), (u or {}).get('chain')) for t, u in (mg.get('units') or {}).items()}
    un = [(x.get('target'), x.get('attempt'), x.get('run'), x.get('why')) for x in mg.get('unused_runs') or []]
    want_un = sorted([(f'unit:{PRE_STOP_UNIT}', W['pre']['n'], 'U01_corner', 'not_adopted'),
                      (f'unit:{RES_UNIT}', W['res']['n'], 'U01_corner', 'replaced_by_resume')])
    n_copy = len(mg.get('attempts') or [])
    print(f'    보고 D3 — 합치기 rc {W["merge"]["rc"]} · {ms.get("status")} · 런 {len(runs)} · 사본 시도 {n_copy} · 남은 런 기록 {un} · {T.get("merge_only")} s')
    chk('D3d 합치기 (kgy · 다른 기계의 시도 폴더는 옮긴 사본) — rc 0 · PREDICTED · 런 24 · 런 이름 = 사슬 차례 (P01–P12_corner · P13–P24_origin) · 런 폴더 = '
        'units/unit-<단위>/attempt_<n>/… · 단위마다 채택 · 재실행 사슬 = 그 단위의 시도 (재실행한 단위 = 사슬 끝) · 기계 = 그 시도의 이름표 · 결정 기록 없음 '
        '(넘침 없음) · 사본 = 시도 14 · 남은 런 기록 = 결과 전 멈춘 시도의 런 (not_adopted) · 재실행이 대신한 멈춘 런 (replaced_by_resume) 둘뿐 (멈춤 아님)',
        W['merge']['rc'] == 0 and ms.get('status') == 'PREDICTED' and names == want_names and outs_ok and mach == want_mach
        and att == {f'unit:{n}': (W['units'][n]['n'], W['units'][n]['chain']) for n in UNIT_TABLE} and mg.get('expansion') is None
        and n_copy == len(W['att']) and sorted(un) == want_un,
        (W['merge']['rc'], ms.get('status'), stop_code(ms), names[:3], outs_ok, mach == want_mach, n_copy, un, W['merge']['so'][-500:]))
    v = jload(os.path.join(W['verdict']['out'], 'verdict.json')) or {}
    tg = ((v.get('ledger') or {}).get('targets') or {})
    want_tg = dict({f'unit:{n}': W['units'][n]['n'] for n in UNIT_TABLE}, **{f'ladder:{law}': W['lad_n'][law] for law in RR.LAWS})
    print(f'    보고 D3 — 판정 rc {W["verdict"]["rc"]} · {v.get("verdict")} (상태 {v.get("state")}) · 표지 {v.get("flags")} · 팔 {len(v.get("arms") or [])}')
    chk('D3e 원장 판정 (합친 예측 · kgy) — rc 0 · 등록 판정 이름 (멈춤 아님) · 원장 채택 = 사다리 둘 + 단위 12 (그 번호) · 합친 예측의 원장 대조 기록 '
        '(ledger.merged) · 원장 커밋 = 원장 HEAD · 결과 JSON 0600',
        W['verdict']['rc'] == 0 and v.get('stop') is None and v.get('verdict') not in (None, 'NOT_COMPUTED')
        and {k: (x or {}).get('effective') for k, x in tg.items()} == want_tg
        and list(((v.get('ledger') or {}).get('merged') or {})) == [os.path.realpath(W['merge']['out'])]
        and (v.get('ledger') or {}).get('commit') == git(kgy['ledger'], 'rev-parse', 'HEAD')
        and (os.stat(os.path.join(W['verdict']['out'], 'verdict_results.json')).st_mode & 0o777) == 0o600,
        (W['verdict']['rc'], v.get('verdict'), v.get('stop'), W['verdict']['so'][-500:]))


def t_one():
    one = W['M']['one']
    bg = bg_wait('one')
    s = jload(os.path.join(W['one']['pred'], 'predict_summary.json')) or {}
    v = jload(os.path.join(W['one']['verdict'], 'verdict.json')) or {}
    rl = led_result(one['ledger'], W['one']['n']) or {}
    tg = ((v.get('ledger') or {}).get('targets') or {})
    print(f'    보고 D2 — 한 기계 예측 rc {(bg.get("predict") or {}).get("rc")} · {s.get("status")} (런 {len(s.get("runs") or [])} · '
          f'{(bg.get("predict") or {}).get("seconds")} s) · 판정 rc {(bg.get("verdict") or {}).get("rc")} · {v.get("verdict")} '
          f'({(bg.get("verdict") or {}).get("seconds")} s)')
    return chk('D2a 길 1 (한 기계 예측 · 따로 원장 = 사다리 둘 뒤에서 갈라 낸 사본 · 사다리 폴더는 옮긴 사본 · 뒤 프로세스) — --add predict rc 0 · 예측 rc 0 · '
               'PREDICTED · 런 24 (DBE 만 · no-op 런 요청 없음) · 결과 줄 completed · 원장 판정 rc 0 · 등록 판정 이름 · 채택 = 사다리 둘 + 예측',
               W['one']['add_rc'] == 0 and (bg.get('predict') or {}).get('rc') == 0 and s.get('status') == 'PREDICTED' and len(s.get('runs') or []) == 24
               and all(x.get('kit') == RR.DBE_KIT for x in s.get('runs') or []) and rl.get('status') == 'completed'
               and (bg.get('verdict') or {}).get('rc') == 0 and v.get('stop') is None and v.get('verdict') not in (None, 'NOT_COMPUTED')
               and {k: (x or {}).get('effective') for k, x in tg.items()} == dict({'predict': W['one']['n']},
                                                                                  **{f'ladder:{law}': W['lad_n'][law] for law in RR.LAWS}),
               (W['one'], {k: (x.get('rc'), x.get('so', '')[-500:]) for k, x in bg.items()}, s.get('status'), stop_code(s), v.get('verdict'), v.get('stop')))


# ═════════════════════════ D4 같음 — 한 번에 돈 예측 ↔ 12 단위 → 합치기 ═════════════════════════
def cert_norm(res, pred_name):
    """판정 결과 JSON 의 증서 칸 키 `<예측 폴더 이름>/<런 이름>` 에서 예측 폴더 이름을 한 낱말로 (두 길의 폴더 이름이 다르다) → 사본."""
    out = dict(res or {})
    out['certificates_dsigma_rel'] = {('PRED/' + k[len(pred_name) + 1:] if k.startswith(pred_name + '/') else k): v
                                      for k, v in ((res or {}).get('certificates_dsigma_rel') or {}).items()}
    return out


def res_bytes(d):
    p = os.path.join(d, 'verdict_results.json')
    return open(p, 'rb').read() if os.path.exists(p) else None


def t_same():
    s1 = jload(os.path.join(W['one']['pred'], 'predict_summary.json')) or {}
    s2 = jload(os.path.join(W['merge']['out'], 'predict_summary.json')) or {}
    diff = [k for k, a, b in (('status', s1.get('status'), s2.get('status')), ('checks', s1.get('checks'), s2.get('checks')),
                              ('origin', s1.get('origin'), s2.get('origin')), ('stop', s1.get('stop'), s2.get('stop')),
                              ('sv_cf', s1.get('sv_cf'), s2.get('sv_cf')), ('runs', proj_runs(s1, ARM_KEYS_NO_SHA), proj_runs(s2, ARM_KEYS_NO_SHA)))
            if a != b]
    chk('D4a 같음 (공개 칸 · Q9 §4) — 한 번에 돈 예측 ↔ 12 단위 → 합치기: 상태 · 검사 (no-op · same_p · 단조) · origin 결정 · 멈춤 없음 · SV 범위 · 런 24 의 '
        '요청 칸 (이름 · 역할 · 킷 · 법칙 · c · R_j · 팔 · 변이 · SV) · rc · 팔 공개 칸 (sha256 뺀 전부 — 상태 · 반복 수 · 잔차 · 증서 통과 · 격자 지문 …) 같음',
        not diff and bool(s1) and bool(s2) and s2.get('status') == 'PREDICTED', diff)
    #  팔 JSON 바이트 — 같은 요청의 팔을 두 길에서 견준다: 같은 체크아웃 (kgy 단위 ↔ kgy 체크아웃의 한 기계 예측) = 바이트 같음 · 다른 체크아웃 (gabia ·
    #    v100 단위) = 다른 칸이 픽스처의 한 칸뿐 (고정물 체크아웃에 docs/data 의 CSV 가 없어 payload 가 그 경로를 문구에 적는다 · 생산 체크아웃에는 있다)
    a1 = {(r['role'], r['law'], r['c'], r['rj'], a['index']): os.path.join(W['one']['pred'], r['outdir'], a['file'])
          for r in s1.get('runs') or [] for a in r.get('arms_read') or []}
    odd, by_m = [], {}
    for r in s2.get('runs') or []:
        mach = (W['units'].get(str((r.get('source') or {}).get('target'))[5:]) or {}).get('m')
        for a in r.get('arms_read') or []:
            p1, p2 = a1.get((r['role'], r['law'], r['c'], r['rj'], a['index'])), os.path.join(W['merge']['out'], r['outdir'], a['file'])
            if p1 is None or not os.path.isfile(p2):
                odd.append((r.get('name'), a.get('index'), 'no pair'))
                continue
            b1, b2 = open(p1, 'rb').read(), open(p2, 'rb').read()
            by_m.setdefault(mach, [0, 0])[0 if b1 == b2 else 1] += 1
            if b1 != b2:
                d = E._json_diff(json.loads(b1.decode('utf-8')), json.loads(b2.decode('utf-8')))
                if mach == 'kgy' or d != ['mpm_metrics.step3.collector.anchors_source']:
                    odd.append((r.get('name'), a.get('index'), mach, d[:4]))
    print(f'    보고 D4 — 팔 JSON 바이트 (두 길의 같은 요청 · 기계별 [같음, 다름]) {by_m}')
    chk('D4b 같음 (팔 JSON) — 팔 36 개 모두 짝이 있다 · kgy 에서 돈 단위의 팔 = 한 기계 예측 (같은 체크아웃) 의 팔과 바이트 같음 · 다른 바탕 (gabia · v100) 에서 '
        '돈 단위의 팔 = 다른 칸이 collector.anchors_source 하나뿐 (픽스처 체크아웃의 절대 경로 문구 · 값 · 증서 · 매니페스트 같음)',
        not odd and sum(a + b for a, b in by_m.values()) == 36 and by_m.get('kgy', [0, 1])[1] == 0, (odd[:3], by_m))
    v1, v2 = jload(os.path.join(W['one']['verdict'], 'verdict.json')) or {}, jload(os.path.join(W['verdict']['out'], 'verdict.json')) or {}
    rb1, rb2 = res_bytes(W['one']['verdict']) or b'', res_bytes(W['verdict']['out']) or b''
    r1, r2 = (json.loads(b.decode('utf-8')) if b else {} for b in (rb1, rb2))
    n1, n2 = os.path.basename(W['one']['pred']), os.path.basename(W['merge']['out'])
    top = sorted(k for k in set(r1) | set(r2) if r1.get(k) != r2.get(k))
    vdiff = sorted(k for k in set(v1) | set(v2) if v1.get(k) != v2.get(k))
    print(f'    보고 D4 — 판정 JSON 의 다른 칸 {vdiff} · 결과 JSON 의 다른 칸 {top} (증서 칸 키의 예측 폴더 이름 {n1!r} ↔ {n2!r})')
    chk('D4c 같음 (판정 · Q9 §4) — 판정 이름 · 상태 · 표지 · 차단 표지 · 문장 허용 · 사다리 이름 같음 · 판정 결과 JSON = 증서 칸 키의 예측 폴더 이름만 맞추면 '
        '값까지 같음 (그대로는 그 칸 하나만 다름 = 설계 §3-2 의 키 꼴 <예측 폴더 이름>/<런 이름>) · 판정 JSON 의 다른 칸 = 경로 · 원장 · 입력 기록뿐 (등록 '
        '사본은 경로만 다름)',
        bool(r1) and all(v1.get(k) == v2.get(k) for k in ('verdict', 'state', 'flags', 'blocking_flags', 'sentence_allowed', 'calib', 'reasons', 'bed'))
        and cert_norm(r1, n1) == cert_norm(r2, n2) and top == ['certificates_dsigma_rel'] and rb1 != rb2
        and set(vdiff) <= {'inputs', 'arms', 'ledger', 'input_dirs', 'ledger_input', 'registration'} and 'inputs' in vdiff
        and {k: v for k, v in (v1.get('registration') or {}).items() if k != 'path'}
        == {k: v for k, v in (v2.get('registration') or {}).items() if k != 'path'},
        (v1.get('verdict'), v2.get('verdict'), top, vdiff))


@phase('checks_main')
def p_checks_main():
    t_units()
    t_merge()


@phase('checks_same')
def p_checks_same():
    if t_one():
        t_same()


# ═════════════════════════ D7 넘침 경로 (뒤에서 · 판정 문턱 대역) ═════════════════════════
OVER_POINTS = [RR.unit_name('0', 'P0', rr) for rr in RR.RJ_ROLES]     # 대역이 넘침으로 뒤집는 모서리 (법칙 P0 · c 0) 의 세 R


@phase('over_start')
def p_over_start():
    kgy = W['M']['kgy']
    fo = os.path.join(kgy['root'], 'ca1_ledger_over')      # 단위 12 개가 끝난 원장의 사본 (넘침 사례만의 원장 — 주 원장에 넘침 점 항목을 넣지 않는다)
    git(kgy['root'], 'clone', '-q', kgy['ledger'], fo)
    m1 = os.path.join(kgy['root'], 'ca1_over_merge1')
    dec = os.path.join(m1, 'expansion.json')
    pb = os.path.join(kgy['root'], 'ca1_points')
    out, vd = os.path.join(kgy['root'], 'ca1_over_predict'), os.path.join(kgy['root'], 'ca1_over_verdict')
    steps = [{'tag': 'merge1', 'want': 4, 'argv': a_merge(kgy, m1, merge_paths(kgy), led=fo)}]
    for i, nm in enumerate(OVER_POINTS):
        steps.append({'tag': f'add{i}', 'want': 0, 'capture': f'n{i}', 'argv': a_add(kgy, f'point:{nm}', led=fo)})
        steps.append({'tag': f'point{i}', 'want': 0,
                      'argv': a_pred(kgy, pb, ['--ledger', fo, '--attempt', '{n%d}' % i, '--point', nm, '--expand', dec])})
    steps += [{'tag': 'merge2', 'want': 0, 'argv': a_merge(kgy, out, merge_paths(kgy) + [pb], led=fo, expand=dec)},
              {'tag': 'verdict', 'want': 0, 'argv': a_verdict(kgy, out, vd, led=fo)},
              {'tag': 'reverify', 'argv': a_reverify(kgy, vd, os.path.join(kgy['root'], 'ca1_over_reverify'))}]
    W['over'] = {'ledger': fo, 'merge1': m1, 'dec': dec, 'points': pb, 'out': out, 'verdict': vd, 'head0': git(fo, 'rev-parse', 'HEAD')}
    bg_start('over', kgy, steps, over=True)


def t_over():
    kgy = W['M']['kgy']
    o = W['over']
    bg = bg_wait('over')
    rc = {k: (bg.get(k) or {}).get('rc') for k in ['merge1'] + [f'point{i}' for i in range(3)] + ['merge2', 'verdict', 'reverify']}
    ms1 = jload(os.path.join(o['merge1'], 'merge_summary.json')) or {}
    dec = jload(o['dec']) or {}
    want_att = sorted([[f'unit:{n}', k, (led_result(kgy['ledger'], k) or {}).get('folder_sha256')] for n in UNIT_TABLE for k in W['units'][n]['chain']])
    print(f'    보고 D7 — 뒤 프로세스 rc {rc} · 시간 (s) {[(k, (bg.get(k) or {}).get("seconds")) for k in rc]} · 넘침 점 {dec.get("points")}')
    chk('D7a 넘침 (판정 문턱 대역 · 실물 넘침 아님) 첫 합치기 — rc 4 · merge_summary 상태 EXPANSION_NEEDED (멈춤 아님 · predict_summary 없음) · 런 24 · 이른 단조 '
        '기록 4 · 결정 기록 expansion.json (rint-r-expansion-v1 · 점 = 그 모서리의 세 R · overflow · 단위 채택 시도 sha 집합 = 단위 12 의 채택 사슬 [대상 · 번호 · '
        '폴더 요약 sha] (재실행한 단위 = 두 줄) · 원장 커밋 = 그때 원장 HEAD · 사다리 요약 sha · 계획 sha)',
        rc['merge1'] == 4 and ms1.get('status') == 'EXPANSION_NEEDED' and ms1.get('stop') is None
        and not os.path.exists(os.path.join(o['merge1'], 'predict_summary.json')) and len(ms1.get('runs') or []) == 24
        and len((ms1.get('checks') or {}).get('r_monotone_early') or []) == 4 and dec.get('schema') == 'rint-r-expansion-v1'
        and dec.get('points') == OVER_POINTS and dec.get('overflow') == [['0', 'P0', rr] for rr in RR.RJ_ROLES] and dec.get('attempts') == want_att
        and len(want_att) == 13 and (dec.get('ledger') or {}).get('commit') == o['head0'] and dec.get('plan_sha256') == W['plan_sha']
        and dec.get('ladders') == {law: E._sha(os.path.join(lads_of(kgy)[i], 'ladder_summary.json')) for i, law in enumerate(RR.LAWS)},
        (rc, ms1.get('status'), sorted(dec), (bg.get('merge1') or {}).get('so', '')[-500:]))
    pts = []
    for i, nm in enumerate(OVER_POINTS):
        x = re.search(r'ATTEMPT_ADDED n=(\d+)', (bg.get(f'add{i}') or {}).get('so', ''))
        n = int(x.group(1)) if x else None
        ps = jload(os.path.join(o['points'], f'attempt_{n}', 'point_summary.json')) or {}
        pts.append((nm, n, rc[f'point{i}'], ps.get('status'), [(r.get('name'), r.get('role'), r.get('arms'), r.get('rc')) for r in ps.get('runs') or []],
                    (ps.get('expansion') or {}).get('sha256') == E._sha(o['dec']) if os.path.exists(o['dec']) else None))
    chk('D7b 넘침 점 셋 (실제 러너 origin8 · 결정 기록 인용 · 원장 시도) — --add rc 0 · 시도 rc 0 · POINT_DONE · 런 = U01_origin8 (8 팔 · rc 0) · 인용한 결정 기록 '
        'sha = 결정 기록 파일',
        all(p[2] == 0 and p[3] == 'POINT_DONE' and p[4] == [('U01_origin8', 'origin8', 8, 0)] and p[5] is True for p in pts), pts)
    ms2 = jload(os.path.join(o['out'], 'predict_summary.json')) or {}
    runs = ms2.get('runs') or []
    org = [(x.get('c'), x.get('law'), x.get('status')) for x in ms2.get('origin') or []]
    v = jload(os.path.join(o['verdict'], 'verdict.json')) or {}
    rep = jload(os.path.join(kgy['root'], 'ca1_over_reverify', 'reverify_report.json')) or {}
    chk('D7c 끝 합치기 (--expand) → 원장 판정 → 다시 판정 (같은 프로세스 · 같은 대역) — 합치기 rc 0 · PREDICTED · 런 27 (모서리 12 · origin 12 · origin8 3 = '
        'P25–P27_origin8) · origin 결정 = 그 모서리 adjusted · 나머지 pass · merge.expansion sha = 결정 기록 · 채택 = 단위 12 + 넘침 점 3 · 판정 rc 0 · 등록 판정 '
        '이름 · 다시 판정 rc 0 REVERIFY_SAME',
        rc['merge2'] == 0 and ms2.get('status') == 'PREDICTED' and len(runs) == 27
        and [x.get('name') for x in runs[24:]] == ['P25_origin8', 'P26_origin8', 'P27_origin8']
        and org == [('0', 'P0', 'adjusted'), ('1', 'P0', 'pass'), ('0', 'P1', 'pass'), ('1', 'P1', 'pass')]
        and ((ms2.get('merge') or {}).get('expansion') or {}).get('sha256') == E._sha(o['dec'])
        and sorted((ms2.get('merge') or {}).get('units') or {}) == sorted([f'unit:{n}' for n in UNIT_TABLE] + [f'point:{n}' for n in OVER_POINTS])
        and rc['verdict'] == 0 and v.get('stop') is None and v.get('verdict') not in (None, 'NOT_COMPUTED')
        and rc['reverify'] == 0 and rep.get('result') == 'REVERIFY_SAME',
        (rc, ms2.get('status'), stop_code(ms2), len(runs), org, v.get('verdict'), v.get('stop'), rep.get('result'),
         {k: (bg.get(k) or {}).get('so', '')[-300:] for k in ('merge2', 'verdict', 'reverify')}))
    n_extra()


# ═════════════════════════ D5 음성 대조 ═════════════════════════
def merge_try(m, tag, paths, led):
    out = os.path.join(m['root'], f'ca1_neg_{tag}{SUF}')
    rc, so = call(m, a_merge(m, out, paths, led=led))
    s = jload(os.path.join(out, 'predict_summary.json')) or {}
    return {'rc': rc, 'status': s.get('status'), 'code': stop_code(s), 'run': (s.get('stop') or {}).get('run'),
            'cause': str((s.get('stop') or {}).get('cause')), 'n_runs': len(s.get('runs') or []), 'so': so[-400:]}


def n_extra():
    """음성 (단위 하나 더) — 넘침 사례의 원장 · 시도 폴더 (넘침 점 시도 셋 포함) 를 대역 없이 (넘침 없는 다시 계산) · 결정 기록 없이 합친다."""
    kgy, o = W['M']['kgy'], W['over']
    g = merge_try(kgy, 'extra', merge_paths(kgy) + [o['points']], o['ledger'])
    chk('D5b 음성 (단위 하나 더 = 요청되지 않은 채택 시도) — 넘침 점 시도 셋이 있는 원장 · 폴더를 결정 기록 없이 · 넘침 없는 다시 계산으로 합침 → rc 3 · STOPPED '
        'UNIT_EXTRA (다시 계산은 끝까지 갔다 = 런 24 · 채택된 넘침 점 시도가 남았다)',
        g['rc'] == 3 and g['status'] == 'STOPPED' and g['code'] == 'UNIT_EXTRA' and g['n_runs'] == 24 and 'point:' in g['cause'], g)


def n_negatives(redo=False):
    M = W['M']
    kgy = M['kgy']
    e = W['early']
    if redo:                                               # (개발용) 이른 합치기를 그 시점 원장 사본 · 그때 있던 시도 폴더로 다시
        e = merge_try(kgy, 'early', [a['kgy'] for a in W['att'] if a['unit'] != UNIT_TABLE[0]], W['fork11'])
    chk('D5a 음성 (단위 하나 빠짐) — 끝 단위 (P0_c0_R_j_lo = 다시 계산이 맨 먼저 요청하는 단위) 를 돌기 전에 합치기 → rc 3 · STOPPED UNIT_MISSING (런 '
        'P01_corner · 런 기록 0 · 판정 입력 아님)',
        e['rc'] == 3 and e['status'] == 'STOPPED' and e['code'] == 'UNIT_MISSING' and e['run'] == 'P01_corner' and e['n_runs'] == 0, e)
    #  원장 사본 (단위 12 개 끝 · 읽기만 하는 음성 대조용)
    f12 = os.path.join(kgy['root'], f'ca1_ledger_fork12{SUF}')
    git(kgy['root'], 'clone', '-q', kgy['ledger'], f12)
    h12 = git(f12, 'rev-parse', 'HEAD')
    #  채택 시도 폴더의 한 바이트를 결과 줄 뒤에 바꿈 — 맨 먼저 요청되는 단위 (v100 에서 돌아 kgy 로 옮긴 시도 폴더) 를 **따로 뜬 사본** 에서 바꾼다:
    #  같은 때 뒤에서 도는 넘침 사례 (D7) 가 kgy 의 시도 폴더를 읽고 있다 — 함께 쓰는 폴더를 바꾸면 그 합치기가 (옳게) 거부한다 (11-11 kgy 판 실측).
    u = W['units'][UNIT_TABLE[0]]
    want = (led_result(f12, u['n']) or {}).get('folder_sha256')
    priv = os.path.join(kgy['root'], f'ca1_neg_byte_in{SUF}', os.path.basename(u['kgy']))
    same0 = ship(u['kgy'], priv) and E.tree_digest(priv) == want
    su = jload(os.path.join(priv, 'unit_summary.json')) or {}
    armf = arm_paths(priv, su)[0]
    raw = open(armf, 'rb').read()
    with open(armf, 'ab') as f:
        f.write(b' ')
    g = merge_try(kgy, 'byte', [a['kgy'] for a in W['att'] if a['kgy'] and a['kgy'] != u['kgy']] + [priv], f12)
    with open(armf, 'wb') as f:
        f.write(raw)
    back = E.tree_digest(priv) == want and E.tree_digest(u['kgy']) == want
    chk('D5c 음성 (채택 시도 폴더의 한 바이트를 결과 뒤에 바꿈 · 옮긴 시도 폴더를 따로 뜬 사본에서) — 팔 JSON 끝에 공백 하나 → 합치기 rc 3 · STOPPED '
        'ATTEMPT_LEDGER_MISMATCH (폴더 요약 sha ≠ 원장 결과 줄 · 그 단위 첫 요청 P01_corner · 런 기록 0) · 바꾸기 전 · 되돌린 뒤의 폴더 요약 = 결과 줄 · 원 폴더는 '
        '그대로',
        same0 and g['rc'] == 3 and g['status'] == 'STOPPED' and g['code'] == 'ATTEMPT_LEDGER_MISMATCH' and g['run'] == 'P01_corner' and g['n_runs'] == 0
        and '폴더 요약 sha' in g['cause'] and back, (same0, g, back))
    #  풀기 전 관문 (정직한 흐름의 첫 줄) — 이미 채택된 단위의 새 항목 · 계획 봉인 판과 다른 환경
    rca, na, soa = add(kgy, f'unit:{UNIT_TABLE[1]}', led=f12)
    fg = os.path.join(kgy['root'], f'ca1_ledger_fork11_gate{SUF}')
    git(kgy['root'], 'clone', '-q', W['fork11'], fg)
    hg = git(fg, 'rev-parse', 'HEAD')
    env0 = RR.env_record
    rec0 = env0()
    RR.env_record = lambda: dict(rec0, unit=dict(rec0['unit'], numpy=str(rec0['unit']['numpy']) + '.e2e12'))
    try:
        rce, ne, soe = add(kgy, f'unit:{UNIT_TABLE[0]}', led=fg)
    finally:
        RR.env_record = env0
    chk('D5d 풀기 전 관문 (--add · 러너 없음 · 원장 무변경) — 이미 채택된 단위의 새 항목 = rc 3 ATTEMPT_AFTER_ADOPTED · 환경 같음 단위 (numpy 판) 가 계획 봉인 '
        '판과 다른 셸의 항목 = rc 3 CODE_PIN_MISMATCH',
        rca == 3 and na is None and 'ATTEMPT_AFTER_ADOPTED' in soa and git(f12, 'rev-parse', 'HEAD') == h12
        and rce == 3 and ne is None and 'CODE_PIN_MISMATCH' in soe and git(fg, 'rev-parse', 'HEAD') == hg, (rca, soa[-300:], rce, soe[-300:]))


def n_provenance():
    """음성 (출처 칸이 다른 단위) — 단위 11 개가 끝난 시점의 원장 사본에 끝 단위를 gabia 에서 한 번 더 돌리되, 결과 줄을 쓰기 직전에 그 단위 요약의 환경 같음
    단위 (numpy 판) 를 바꾼다 (단위 단계의 풀기 전 관문이 뚫린 꼴 흉내 · 원장 결과 줄 · 폴더 요약은 바뀐 폴더와 맞다) → 합치기."""
    M = W['M']
    gabia = M['gabia']
    name = UNIT_TABLE[0]
    f11 = os.path.join(gabia['root'], f'ca1_ledger_fork11{SUF}')
    git(gabia['root'], 'clone', '-q', W['fork11'], f11)
    old = RR.attempt_close

    def close(att, s):
        p = os.path.join(str(att.folder), 'unit_summary.json')
        j = jload(p)
        j['code']['env']['unit']['numpy'] = str(j['code']['env']['unit']['numpy']) + '.e2e12'
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(j, f, ensure_ascii=False)
        return old(att, s)
    RR.attempt_close = close
    try:
        r = run_unit(gabia, name, base=os.path.join(gabia['root'], f'ca1_units_prov{SUF}'), led=f11)
    finally:
        RR.attempt_close = old
    rl = led_result(f11, r['n']) or {}
    W['prov'] = {'ledger': f11, 'folder': r['folder'], 'n': r['n']}
    paths = [a['moved'] for a in W['moved']['att'] if a['unit'] != name] + [r['folder']]
    g = merge_try(gabia, 'prov', paths, f11)
    chk('D5e 음성 (출처 칸이 다른 단위 — 환경 같음 단위) — 그 단위 요약의 numpy 판만 다른 시도 (결과 줄 completed · 폴더 요약 sha = 바뀐 폴더) → 합치기 rc 3 · '
        'STOPPED UNIT_PROVENANCE_MISMATCH (출처 칸 code · 그 단위 첫 요청 P01_corner · 런 기록 0)',
        r['add_rc'] == 0 and r['rc'] == 0 and rl.get('status') == 'completed' and rl.get('folder_sha256') == E.tree_digest(r['folder'])
        and g['rc'] == 3 and g['status'] == 'STOPPED' and g['code'] == 'UNIT_PROVENANCE_MISMATCH' and g['run'] == 'P01_corner' and g['n_runs'] == 0
        and "['code']" in g['cause'], (r, rl.get('status'), g))


def n_diverged():
    """이동 (거부 · 갈라진 원장) — 음성 D5e 가 남긴 곁가지 (단위 11 개 시점의 원장 사본에 gabia 가 끝 단위를 따로 돌린 것 = 한 원장의 두 사본에 두 기계가 각각 쓴
    꼴: 같은 항목 번호가 두 사본에서 다른 시도다) 를 주 원장과 섞는다 — 빨리 감기 (git 의 동작 · 사슬 아님) · 주 원장 + 곁가지에서 돈 시도 폴더 · 곁가지 원장 +
    주 원장의 시도 폴더."""
    M = W['M']
    gabia, mv, pv = M['gabia'], W['moved'], W['prov']
    name = UNIT_TABLE[0]
    tmp = os.path.join(gabia['root'], f'ca1_ledger_div{SUF}')
    git(gabia['root'], 'clone', '-q', mv['ledger'], tmp)
    br, h0 = git(tmp, 'symbolic-ref', '--short', 'HEAD'), git(tmp, 'rev-parse', 'HEAD')
    r = subprocess.run(['git', '-C', tmp, *E.GIT_CFG, 'pull', '-q', '--ff-only', pv['ledger'], br], capture_output=True)
    ff = (r.returncode != 0, git(tmp, 'rev-parse', 'HEAD') == h0)
    ga = merge_try(gabia, 'div_a', [a['moved'] for a in mv['att'] if a['unit'] != name] + [pv['folder']], mv['ledger'])
    gb = merge_try(gabia, 'div_b', [a['moved'] for a in mv['att']], pv['ledger'])
    chk('D6j 이동 (거부 · 갈라진 원장 = 한 원장의 두 사본에 두 기계가 각각 씀 · 같은 항목 번호가 두 사본에서 다른 시도) — 한쪽 사본을 다른 쪽으로 빨리 감기 '
        '(`git pull --ff-only`) = 거부 · 사본 그대로 (git 의 동작) · 주 원장 + 곁가지에서 돈 시도 폴더 = 합치기 rc 3 ATTEMPT_LEDGER_MISMATCH (시도 폴더의 '
        'attempt.json ≠ 원장 항목 · 런 기록 0) · 곁가지 원장 + 주 원장의 시도 폴더 = 같은 거부',
        ff == (True, True) and all(g['rc'] == 3 and g['status'] == 'STOPPED' and g['code'] == 'ATTEMPT_LEDGER_MISMATCH' and g['n_runs'] == 0
                                   and 'attempt.json' in g['cause'] and '원장 항목' in g['cause'] for g in (ga, gb)),
        (ff, r.stderr.decode('utf-8', 'replace')[:200], ga, gb))


@phase('negatives')
def p_negatives():
    n_negatives()


@phase('provenance')
def p_provenance():
    n_provenance()
    n_diverged()


# ═════════════════════════ D6 이동 대조 — 다른 바탕 (gabia) 으로 옮겨 합치기 · 원장 판정 · 다시 판정 ═════════════════════════
def n_moved_neg():
    """이동 (거부) — 옮긴 시도 폴더의 recover · 결과 전 멈춘 시도 폴더를 빼고 옮김 · 같은 항목의 폴더 둘."""
    M = W['M']
    gabia, mv = M['gabia'], W['moved']
    h0 = git(mv['ledger'], 'rev-parse', 'HEAD')
    rcr, sor = call(gabia, ['--stage', 'recover', '--out', gabia['inbox']['kgy'], '--ledger', mv['ledger']])
    rco, soo = call(gabia, ['--stage', 'recover', '--out', gabia['units'], '--ledger', mv['ledger']])
    chk('D6d 이동 (거부) — 옮긴 시도 폴더 (kgy 에서 돈 시도의 gabia 사본) 에 --stage recover --ledger = rc 3 (시작 기록의 바탕 ≠ 이 폴더의 바탕 · 결과 줄 · 원장 '
        '무변경) · 그 기계에서 돈 시도 폴더 (제자리) = rc 0 (할 일 없음 · 원장 무변경)',
        rcr == 3 and '시작 기록의 바탕' in sor and rco == 0 and git(mv['ledger'], 'rev-parse', 'HEAD') == h0, (rcr, sor[-300:], rco, soo[-300:]))
    paths = [a['moved'] for a in mv['att']]
    g1 = merge_try(gabia, 'nopre', [a['moved'] for a in mv['att'] if a['kind'] != 'pre'], mv['ledger'])
    kgy_done = [a for a in mv['att'] if a['m'] == 'kgy' and a['kind'] == 'done'][0]
    g2 = merge_try(gabia, 'dup', paths + [kgy_done['folder']], mv['ledger'])
    chk('D6e 이동 (거부) — 결과 전 멈춘 시도 폴더를 빼고 옮김 = 합치기 rc 3 ATTEMPT_LEDGER_MISMATCH (그 단위가 처음 요청될 때 P05_corner · 엄격: 폴더 없는 '
        '시도) · 같은 항목의 폴더 둘 (옮긴 사본 + 원본 경로를 함께 줌) = rc 3 ATTEMPT_LEDGER_MISMATCH (한 항목 = 폴더 하나)',
        g1['rc'] == 3 and g1['code'] == 'ATTEMPT_LEDGER_MISMATCH' and g1['run'] == 'P05_corner' and '없다' in g1['cause']
        and g2['rc'] == 3 and g2['code'] == 'ATTEMPT_LEDGER_MISMATCH' and '둘' in g2['cause'], (g1, g2))


@phase('moved')
def p_moved():
    M = W['M']
    kgy, gabia = M['kgy'], M['gabia']
    mv = {'att': [], 'ship_ok': True}
    for a in W['att']:                                     # 단위 시도 폴더 전부를 gabia 바탕으로 (자기 것 = 그 자리 · 남의 것 = 원 자리에서 바이트 복사)
        dst = a['folder'] if a['m'] == 'gabia' else os.path.join(gabia['inbox'][a['m']], os.path.basename(a['folder']))
        if dst != a['folder']:
            mv['ship_ok'] = ship(a['folder'], dst) and mv['ship_ok']
        mv['att'].append(dict(a, moved=dst))
    mv['ledger'] = os.path.join(gabia['root'], 'ca1_ledger_moved')
    shutil.copytree(kgy['ledger'], mv['ledger'], symlinks=True)       # 원장 저장소 = 폴더째 바이트 그대로 (.git 포함)
    #  합친 폴더 이름 = 길 1 의 예측 시도 폴더 이름 (attempt_<n>) — 판정 결과의 증서 칸 키 <예측 폴더 이름>/<런 이름> 까지 같게
    mv['out'] = os.path.join(gabia['root'], 'ca1_predict_moved', os.path.basename(W['one']['pred']))
    mv['verdict'] = os.path.join(gabia['root'], 'ca1_verdict_moved')
    W['moved'] = mv
    paths = [a['moved'] for a in mv['att']]
    rc, so = call(gabia, a_merge(gabia, mv['out'], paths, led=mv['ledger']))
    rcv, sov = call(gabia, a_verdict(gabia, mv['out'], mv['verdict'], led=mv['ledger']))
    ms = jload(os.path.join(mv['out'], 'predict_summary.json')) or {}
    s_k = jload(os.path.join(W['merge']['out'], 'predict_summary.json')) or {}
    v, v_k = jload(os.path.join(mv['verdict'], 'verdict.json')) or {}, jload(os.path.join(W['verdict']['out'], 'verdict.json')) or {}
    rb = {k: res_bytes(d) for k, d in (('moved', mv['verdict']), ('kgy', W['verdict']['out']), ('one', W['one']['verdict']))}
    same_pub = all(ms.get(k) == s_k.get(k) for k in ('status', 'checks', 'origin', 'stop', 'sv_cf', 'bed')) and proj_runs(ms) == proj_runs(s_k)
    pdiff = sorted(k for k in set(ms) | set(s_k) if ms.get(k) != s_k.get(k))
    vdiff = sorted(k for k in set(v) | set(v_k) if v.get(k) != v_k.get(k))
    print(f'    보고 D6 — gabia 로 옮긴 합치기 rc {rc} · {ms.get("status")} · 판정 rc {rcv} · {v.get("verdict")} · 합친 요약의 다른 칸 (kgy 합치기 대비) {pdiff} · '
          f'판정 JSON 의 다른 칸 {vdiff}')
    chk('D6a 이동 (허용) — 사다리 시도 폴더 둘 · 단위 시도 폴더 14 (결과 전 멈춘 시도 · 자원 멈춤 시도 포함) · 원장 저장소 (폴더째) 를 바이트 그대로 gabia 바탕 '
        '(다른 절대 경로 · 다른 체크아웃 · 다른 킷 사본) 으로 → 합치기 rc 0 PREDICTED · 원장 판정 rc 0 · kgy 합치기와 공개 칸 (상태 · 검사 · origin · 침대 지문 · '
        '런 요청 칸 · rc · 팔 공개 칸 = sha256 포함) 같음 · 판정 이름 · 상태 · 표지 같음',
        mv['ship_ok'] and len(paths) == 14 and rc == 0 and ms.get('status') == 'PREDICTED' and rcv == 0 and v.get('stop') is None and same_pub
        and all(v.get(k) == v_k.get(k) for k in ('verdict', 'state', 'flags', 'blocking_flags', 'sentence_allowed', 'calib', 'bed')),
        (mv['ship_ok'], rc, ms.get('status'), stop_code(ms), rcv, v.get('stop'), same_pub, so[-400:], sov[-400:]))
    chk('D6b 같아야 하는 바이트 — 옮긴 판정의 결과 JSON = 길 1 (한 기계 예측 · 예측 폴더 이름이 같다) 의 결과 JSON 과 바이트 같음 · kgy 합치기 판정의 결과 JSON 과는 '
        '증서 칸 키의 예측 폴더 이름만 다름 · 판정 JSON · 합친 요약에서 다른 칸 = 경로 · 원장 · 입력 · 봉인 원천 기록뿐 (판정 이름 · 검사 · 값 칸 아님)',
        rb['moved'] is not None and rb['moved'] == rb['one'] and rb['moved'] != rb['kgy']
        and cert_norm(json.loads(rb['moved'].decode('utf-8')), os.path.basename(mv['out']))
        == cert_norm(json.loads(rb['kgy'].decode('utf-8')), os.path.basename(W['merge']['out']))
        and set(vdiff) <= {'inputs', 'arms', 'ledger', 'input_dirs', 'ledger_input', 'registration'}
        and set(pdiff) <= {'code', 'ladders', 'merge', 'registration', 'runs', 's0_reports', 'sv_graph_source', 'machine', 'env_scrubbed'},
        (rb['moved'] == rb['one'], rb['moved'] != rb['kgy'], vdiff, pdiff))
    #  코드 · 킷 = 기계마다 자기 사본 (절대 경로 다름) — 코드 키 · 침대 지문은 같다
    c_k, c_g = s_k.get('code') or {}, ms.get('code') or {}
    chk('D6c 이동 (허용) — 코드 체크아웃 · 킷은 기계마다 자기 사본: 요약의 러너 절대 경로는 다르고 코드 키 (HEAD · 저장소 상대 경로 · 코드 파일 지문 · 환경 같음 '
        '단위) · 침대 지문 (킷 원 입력) 은 같다',
        c_k.get('runner_path') != c_g.get('runner_path') and RR.code_key(c_k) == RR.code_key(c_g) and ms.get('bed') == s_k.get('bed')
        and bool(ms.get('bed')), (c_k.get('runner_path'), c_g.get('runner_path')))
    #  합친 예측 폴더째 옮김 — 합친 런의 outdir = 합친 폴더 기준 상대 경로 · 시도 사본이 그 안에 있다 → 옮긴 폴더로 새 원장 판정
    cp = os.path.join(gabia['root'], 'ca1_predict_copied', os.path.basename(W['merge']['out']))
    ok = ship(W['merge']['out'], cp)
    vc = os.path.join(gabia['root'], 'ca1_verdict_copied')
    rcc, soc = call(gabia, a_verdict(gabia, cp, vc, led=mv['ledger']))
    chk('D6h 이동 (허용) — kgy 의 합친 예측 폴더를 폴더째 gabia 로 (바이트 그대로 · 폴더 이름 그대로) → 그 폴더로 새 원장 판정 rc 0 · 결과 JSON = kgy 판정의 결과 '
        'JSON 과 바이트 같음 (합친 런의 outdir 이 합친 폴더 기준 상대 경로 · 시도 사본 · 결정 기록 · 원장 묶음이 폴더 안)',
        ok and rcc == 0 and res_bytes(vc) is not None and res_bytes(vc) == rb['kgy'], (ok, rcc, soc[-400:]))
    W['moved_obs'] = {'vdiff': vdiff, 'pdiff': pdiff}
    n_moved_neg()


# ═════════════════════════ 다시 판정 (따로 프로세스) — 길 2 · 길 1 · 옮긴 판정 ═════════════════════════
@phase('reverify_start')
def p_reverify_start():
    M = W['M']
    kgy, one, gabia = M['kgy'], M['one'], M['gabia']
    W['rev'] = {'path2': (W['verdict']['out'], os.path.join(kgy['root'], 'ca1_reverify')),
                'path1': (W['one']['verdict'], os.path.join(one['root'], 'ca1_reverify')),
                'moved': (W['moved']['verdict'], os.path.join(gabia['root'], 'ca1_reverify_moved'))}
    W['rev_digest'] = {k: E.dir_digest(v[0]) for k, v in W['rev'].items()}
    steps = [dict(step_env(m), tag=k, argv=a_reverify(m, W['rev'][k][0], W['rev'][k][1])) for k, m in (('moved', gabia), ('path1', one), ('path2', kgy))]
    bg_start('rev', kgy, steps)


def t_reverify():
    bg = bg_wait('rev')
    got = {}
    for k, (vd, out) in W['rev'].items():
        rep = jload(os.path.join(out, 'reverify_report.json')) or {}
        got[k] = ((bg.get(k) or {}).get('rc'), 'REVERIFY_SAME' in (bg.get(k) or {}).get('so', ''), rep.get('result'), rep.get('grade_differ'),
                  rep.get('public_keys_differ'), rep.get('results_differ'), rep.get('env_fields_differ'), E.dir_digest(vd) == W['rev_digest'][k])
    want = (0, True, 'REVERIFY_SAME', False, [], False, [], True)
    print(f'    보고 다시 판정 (따로 프로세스 · 새 인터프리터) — 시간 (s) {[(k, (bg.get(k) or {}).get("seconds")) for k in ("moved", "path1", "path2")]}')
    chk('D3f 길 2 다시 판정 (따로 프로세스 · kgy · 합친 예측의 원장 판정) — rc 0 · REVERIFY_SAME · 보고 (등급 다름 False · 다른 공개 · 결과 칸 없음 · 다른 환경 칸 '
        '없음) · 판정 폴더 바이트 그대로', got.get('path2') == want, (got.get('path2'), (bg.get('path2') or {}).get('so', '')[-400:]))
    chk('D2b 길 1 다시 판정 (따로 프로세스 · 한 기계 예측의 원장 판정) — rc 0 · REVERIFY_SAME · 판정 폴더 바이트 그대로',
        got.get('path1') == want, (got.get('path1'), (bg.get('path1') or {}).get('so', '')[-400:]))
    chk('D6f 옮긴 판정의 다시 판정 (따로 프로세스 · gabia · 그 바탕의 입력 · 원장 사본 · 킷 사본) — rc 0 · REVERIFY_SAME · 판정 폴더 바이트 그대로',
        got.get('moved') == want, (got.get('moved'), (bg.get('moved') or {}).get('so', '')[-400:]))


@phase('verdict_moved_alone')
def p_verdict_moved_alone():
    """판정 폴더만 옮김 — 판정 JSON 은 입력 폴더 · 원장 · 등록 사본의 절대 경로를 싣는다: 그 경로가 없는 곳 (입력을 둔 바탕을 치워 흉내) 의 다시 판정."""
    M = W['M']
    gabia, v100 = M['gabia'], M['v100']
    dst = os.path.join(v100['root'], 'ca1_verdict_from_gabia')
    ok = ship(W['moved']['verdict'], dst)
    d0 = E.dir_digest(dst)
    off = gabia['home'] + '.off'
    os.rename(gabia['home'], off)                          # gabia 바탕이 없는 기계 흉내 (끝나면 되돌린다)
    try:
        rc, so = call(v100, a_reverify(v100, dst, os.path.join(v100['root'], 'ca1_reverify_from_gabia')))
    finally:
        os.rename(off, gabia['home'])
    rep = jload(os.path.join(v100['root'], 'ca1_reverify_from_gabia', 'reverify_report.json')) or {}
    v0 = jload(os.path.join(dst, 'verdict.json')) or {}
    rc2, so2 = call(v100, a_reverify(v100, dst, os.path.join(v100['root'], 'ca1_reverify_from_gabia2')))
    chk('D6g 이동 (묶임) — 판정 폴더만 다른 바탕 (v100) 으로 옮기고 입력을 둔 바탕 (gabia) 이 없는 곳에서 다시 판정 = rc 1 REVERIFY_DIFF (다시 계산 = 멈춤 '
        'ATTEMPT_LEDGER_MISMATCH — 판정 JSON 이 원장 · 입력 폴더의 절대 경로를 싣는다 · 원 판정 이름 = 저장본 · 판정 폴더 바이트 그대로) · 입력 바탕이 그 '
        '경로에 다시 있으면 같은 폴더의 다시 판정 = rc 0 REVERIFY_SAME',
        ok and rc == 1 and rep.get('result') == 'REVERIFY_DIFF' and (rep.get('recomputed') or {}).get('stop_code') == 'ATTEMPT_LEDGER_MISMATCH'
        and (rep.get('original') or {}).get('verdict') == v0.get('verdict') and E.dir_digest(dst) == d0 and rc2 == 0 and 'REVERIFY_SAME' in so2,
        (ok, rc, so[-300:], rep.get('recomputed'), rc2, so2[-300:]))


@phase('checks_tail')
def p_checks_tail():
    t_over()
    p_reverify_start()
    t_reverify()
    p_verdict_moved_alone()


PHASES = [('D1', (p_setup, p_ladders)), ('D2', (p_one_start,)), ('D3', (p_units, p_merge, p_checks_main)), ('D4', (p_checks_same,)),
          ('D7', (p_over_start,)), ('D5', (p_negatives,)), ('D6', (p_moved, p_provenance)), ('끝', (p_checks_tail,))]


def main():
    global ARGS, SUF
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--keep', action='store_true', help='임시 폴더를 남긴다')
    ap.add_argument('--reuse', default=None, help='(개발용) 남긴 임시 폴더 — 끝난 단계를 건너뛴다')
    ap.add_argument('--upto', default=None, help='(개발용) 이 묶음까지만 (D1 … D7)')
    ap.add_argument('--redo', default=None, help='(개발용 · --reuse 와) 끝까지 간 세계에서 음성 대조 (D5a–D5e · D6d · D6e · D6j) 만 다시 — 출력 폴더 꼬리 (변이 확인)')
    ARGS = ap.parse_args()
    if ARGS.reuse:
        E.TD = os.path.abspath(ARGS.reuse)
        W.update(jload(os.path.join(E.TD, 'world.json')) or {})
        E.CODEREPO.update(W.get('coderepo') or {})
    else:
        E.TD = tempfile.mkdtemp(prefix='rint_r_chain_e2e12_')
    TR.TD = os.path.join(E.TD, 'tr')
    TR.SHIMDIR = os.path.join(TR.TD, '_bin')
    os.makedirs(TR.SHIMDIR, exist_ok=True)
    with open(os.path.join(TR.SHIMDIR, 'python3'), 'w', encoding='utf-8') as f:
        f.write(TR.SHIM.replace('__REAL__', os.path.abspath(sys.executable)))
    os.chmod(os.path.join(TR.SHIMDIR, 'python3'), 0o755)
    t0 = time.time()
    phases = PHASES
    if ARGS.redo:
        SUF = '_' + ARGS.redo
        phases = [('음성 대조 다시', (lambda: n_negatives(redo=True), n_extra, n_moved_neg, n_provenance, n_diverged))]
    try:
        for tag, fns in phases:
            print(f'\n── {tag}')
            try:
                for fn in fns:
                    fn()
            except Exception as e:                         # noqa: BLE001 — 시험 안의 예외 = 그 묶음 실패
                import traceback
                chk(f'{tag} 예외 없이', False, f'{type(e).__name__}: {e} @ {traceback.format_exc().splitlines()[-3].strip()[:300]}')
                break
            if ARGS.upto == tag:
                break
    finally:
        for name in list(BG):
            if BG[name][0].poll() is None:
                bg_wait(name)
        if ARGS.keep or ARGS.reuse:
            if not ARGS.redo:
                save_world()
            print(f'  (임시 폴더 남김: {E.TD})')
        else:
            shutil.rmtree(E.TD, ignore_errors=True)
    print(f'\n  단계별 시간 (s): {T}')
    print(f'\ntest_rint_r_chain_e2e12: {_ok} PASS · {len(_fail)} FAIL ({time.time() - t0:.1f} s)')
    for n in _fail:
        print(f'  - {n}')
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())

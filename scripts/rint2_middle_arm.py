#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② 부록 팔 (① DBE · σ_SDCP 0 · ② PTFE 0.5 · SDCP 0) 실행기 — 등록 `docs/reviews/rint2_middle_arm_ptfe05_sdcp0_registration_20261124.md` §2 · §4 · §8.

봉인 사슬 `scripts/rint_r_chain.py` 를 경로로 불러 (해시한 바이트 그대로 실행 · sha256 앞 16 자리 = `CHAIN_SHA_PREFIX` · 파일은 고치지 않는다) 그 함수를
그대로 쓴다 — 사본 없음:
  · 런 env = `Runner._prepare` → `Runner.env_delta` → `runner_env_delta` (고정 칸 = `ENV_FIXED` · 계획 칸 = `plan_env`) · DBE 킷 = `DBE_KIT`
  · R_j,0 = 예측 단계가 사다리를 읽는 함수 `load_ladders` (요약 · R_j,0 확인 팔 · no-op 런을 원 팔에서 다시 읽고 등록 계획 해시 · S0 보고 · 코드를 대조)
  · 칸의 런 = 봉인 단위와 같은 런 차례 `unit_runs` (모서리 arm 0 · SV 반사실 범위 `Predict._sv_on` · origin 팔 `ORIGIN_ARMS`) · 이름 앞자리 `UNIT_PREFIX`
  · 띄우기 = `Runner.run` (`_execute` → `run_in_group` (새 프로세스 그룹 · 종료 확인) → `read_run` (팔 계약 전부) → `arms_read_record`)
  · 비교 = `read_run` · `arm_band` (두 런 다 그 런 증서 구간 · 같은 함수) · `r_monotone_problem` (사슬의 단조 모순 규칙)
check-mono = 등록 §4 구조 확인 · ★ 등록 개정 1 (1저자 11-24 · Codex SBD S4b) — 고정 기하 벌크 전도 대조 (DBE 기하 · σ_SDCP 정상 → 0):
  팔마다 MONO_VIOLATION = σ_lo(①) > σ_hi(DBE) (도구 결함 → 멈춤 · 보고 · rc 1) · 점값 역전 + 구간 겹침 = MONO_UNDETERMINED (보고만) · 그 밖 PASS ·
  PATH_CUT (사슬 해 상태 zero = VALID_ZERO_TOPOLOGY · 판에 닿는 경로 끊김 · 팔 JSON 증서 · 성분 기록 대조) 의 0 = 정상 통과 · SOLVE_FAILED (read_run 멈춤
  NOT_COMPUTED · 구조화 사유 없음) · NOT_COMPUTED (사유 ELECTRODE_SHORT · 판독 전 멈춘 런 · 읽지 않은 팔) = 결손 MISSING (비교 안 함 · 0 으로 세지 않음) ·
  짝 (같은 P · R_j,0 · 격자 원점 · 경계 · env 조립) 이 하나라도 다르면 비교 거부 (사유 · 칸 기록) · 칸 기록 (--record · 리포 밖) = 판정 · 결손 사유 · 두 띠.
run = 판독 NOT_COMPUTED (등록 결과) 뒤에도 다음 런을 돈다 (런마다 read 칸) · 그 밖 멈춤 = 칸 멈춤.
등록과 다른 칸 (봉인 R 단위 env 대비 · 같은 법칙 · 같은 R_j,0 · c '0' · 같은 OUTDIR 로 잰다):
  arm 1 = `SIGMA_SDCP_OVERRIDE` '256.6' → '0' 하나 (킷 = DBE 그대로) · arm 2 = `KITS` (새 킷 이름 · --kit2) 하나.  그 밖 칸이 하나라도 다르면 거부.
arm 1 의 팔 판독 = 사슬 `read_run` 그대로 — 매니페스트 기대값 `MAN_FIXED['sigma_sdcp_S_cm']` 한 칸만 등록 값 0 으로 (이 프로세스의 모듈 객체 · 끝나면 되돌림 ·
`expect_sdcp_sigma`) · 같은 sid 지문 무리 (`sid_reg`) 를 DBE 와 나눠 써서 격자 (기하) 가 같음을 사슬 검사 `SID_GRID` 가 본다.

  python3 scripts/rint2_middle_arm.py plan --ladders <P0 사다리 시도 폴더> <P1 사다리 시도 폴더> --plan <R 계획> --registration <봉인 등록 R> \\
      [--kit2 kit_DBE_ptfe05_sdcp0_vgcf100] [--root ~/sdcp] [--out <OUT>] [--arm 1|2] [--law P0|P1] [--ladder-check full|summary]
  python3 scripts/rint2_middle_arm.py run --arm 1 --law P0 --ladders … --plan … --registration … --root ~/sdcp --machine kgy \\
      --out <새 폴더> [--cjunc-store <저장본>] [--max-hours H]
  python3 scripts/rint2_middle_arm.py run --arm 2 --law P0 --kit2 kit_DBE_ptfe05_sdcp0_vgcf100 …
  python3 scripts/rint2_middle_arm.py check-mono --dbe <봉인 R 단위 시도 폴더 (P0_c0_R_j0)> --arm1 <arm 1 런 폴더> --record <리포 밖 새 JSON>

값 봉인: 결과 σ 는 러너의 팔 JSON 과 check-mono 칸 기록 (--record · 리포 밖 · 띠) 에만 있다 — 화면 · 매니페스트 (`middle_arm_manifest.json`) 에는 쓰지
않는다 (check-mono 화면 = 팔마다 판정 낱말만).  화면의 SIGMA_* = 등록 입력값 (env · 사슬 --dry-run 과 같은 꼴) 이지 결과가 아니다.
rc: 0 = 끝 (check-mono PASS · NO_VIOLATION) · 1 = check-mono MONO_VIOLATION · 2 = 인자 오류 · 3 = 거부 · 멈춤 · check-mono NO_COMPARISON.
⚠ 한정: R 원장 밖 (등록 §6) — 시도 원장 · 재실행 · recover 꼴이 없다 · SV 끝 그래프 봉인 원천 (`RunnerGraphSource`) 을 돌리지 않는다 (SV 귀속 = 미확인 기록) ·
등록 §3 새 침대 점검 (압밀 표지 · 상별 점 수 · 두께 · 기공률) 은 이 도구가 하지 않는다 (킷 입력 지문만 기록).
Python 3.8 (kgy · gabia 실행 환경) 에서 돈다.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import json
import math
import os
import re
import shlex
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = 'rint2_middle_arm'
SCHEMA = 'rint2-middle-arm-v1'
REG_DOC = 'docs/reviews/rint2_middle_arm_ptfe05_sdcp0_registration_20261124.md'
CHAIN_PATH = HERE / 'rint_r_chain.py'
CHAIN_SHA_PREFIX = '5fbc1c3417f17eba'          # 봉인 사슬 (등록 머리 · 봉인 사본과 같은 바이트)
MANIFEST = 'middle_arm_manifest.json'
CELL_C = '0'                                    # 등록 §2 — 두 팔 다 c = 0
CELL_ROLE = 'R_j0'                              # 등록 §2 — 법칙마다 R_j,0 하나
ARM_CHOICES = (1, 2)
#: 등록 §2 — 팔마다 봉인 R 단위 env 를 바꾸는 칸 (이것뿐 · 값까지 등록)
ARM_OVERRIDE = {1: {'SIGMA_SDCP_OVERRIDE': '0'}, 2: {}}
#: 등록 §2 — 봉인 R 단위 env 와 달라도 되는 칸 (① = σ_SDCP · ② = 킷 이름) · 그 밖 칸이 다르면 거부
ARM_DIFF_KEYS = {1: ('SIGMA_SDCP_OVERRIDE',), 2: ('KITS',)}
#: 등록 §2 — 봉인 R 단위 요청과 달라도 되는 요청 칸 (② = 킷)
ARM_REQ_DIFF = {1: (), 2: ('kit',)}
ARM1_SIGMA_SDCP = 0.0                           # arm 1 매니페스트 기대값 (env '0' 의 수)
KIT_RE = re.compile(r'kit_[A-Za-z0-9][A-Za-z0-9_.-]*')
MAX_HOURS_DEFAULT = None                        # None = 계획 exec_policy.max_hours (봉인 값)

_CHAIN = {}


class Refuse(Exception):
    """거부 — code (사슬 멈춤 이름 또는 이 도구의 이름) · why (σ 없는 문장)."""

    def __init__(self, code, why):
        super().__init__(f'{code}: {why}')
        self.code, self.why = str(code), str(why)


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def _path(x):
    """인자 경로 — 따옴표로 막힌 '~' 도 펼친다 (그 밖 그대로)."""
    return Path(os.path.expanduser(str(x)))


def say(msg=''):
    print(msg, flush=True)


# ═════════════════════════ 봉인 사슬 불러오기 ═════════════════════════
def load_chain(path=None, want_prefix=CHAIN_SHA_PREFIX):
    """봉인 사슬 모듈 — 파일 바이트를 해시하고 (앞 16 자리 = 봉인) **그 바이트**를 실행한다 (해시 뒤 바뀐 파일을 읽지 않는다) · sys.modules
    'rint_r_chain' 에 둔다 (같은 프로세스 안 다른 import 가 같은 객체를 받게) · 같은 바이트면 다시 실행하지 않는다."""
    p = Path(path) if path is not None else CHAIN_PATH
    try:
        raw = p.read_bytes()
    except OSError as e:
        raise Refuse('CHAIN_UNREADABLE', f'{p}: {type(e).__name__}')
    sha = hashlib.sha256(raw).hexdigest()
    if not sha.startswith(want_prefix):
        raise Refuse('CHAIN_SHA_MISMATCH', f'{p.name} sha256 {sha[:16]}… ≠ 봉인 {want_prefix}… (사슬 파일은 바이트 그대로여야 · 등록 머리)')
    key = (str(p.resolve()), sha)
    if key in _CHAIN:
        return _CHAIN[key]
    spec = importlib.util.spec_from_file_location('rint_r_chain', str(p))
    mod = importlib.util.module_from_spec(spec)
    old = sys.modules.get('rint_r_chain')
    sys.modules['rint_r_chain'] = mod
    try:
        exec(compile(raw, str(p), 'exec'), mod.__dict__)        # noqa: S102 — 해시한 바이트 그대로 (importlib 가 파일을 다시 읽지 않게)
    except BaseException:
        if old is None:
            sys.modules.pop('rint_r_chain', None)
        else:
            sys.modules['rint_r_chain'] = old
        raise
    mod.MIDDLE_ARM_CHAIN_SHA256 = sha
    _CHAIN[key] = mod
    return mod


def chain_sha(CH):
    return getattr(CH, 'MIDDLE_ARM_CHAIN_SHA256', None)


def _stop(CH, e, where):
    """사슬 Stop → Refuse (이름 그대로 · 사유 = 사슬 문장 · σ 는 사슬이 이미 가렸다)."""
    return Refuse(e.code, f'{where} — {e.cause}' + (f' (런 {e.run})' if getattr(e, 'run', None) else ''))


def _call(CH, where, fn, *a, **k):
    """사슬 함수 하나 — Stop · 예외 = Refuse (조용히 넘어가지 않는다)."""
    try:
        return fn(*a, **k)
    except Refuse:
        raise
    except CH.Stop as e:
        raise _stop(CH, e, where)
    except Exception as e:                                  # noqa: BLE001 — 꼴 틀린 입력 = 거부 (이름 · 사유)
        raise Refuse('UNREADABLE', f'{where} — {type(e).__name__}: {str(e)[:240]}')


# ═════════════════════════ R_j,0 (사다리) ═════════════════════════
def ladders_full(CH, dirs, registration):
    """예측 단계와 같은 사다리 읽기 (`load_ladders` · 변이 없음 · 정본 계약) → {mode, lads, plan, plan_sha, code, s0reps, files}.
    lads[법칙]['r0_sigma'] (R_j,0 확인 팔 σ) 는 쓰지도 보이지도 않는다."""
    if not registration:
        raise Refuse('NO_REGISTRATION', '--registration <봉인 등록 R> 이 필요하다 (사다리 다시 읽기 = 예측 단계 load_ladders · 등록 계획 해시 줄)')
    if len(dirs or []) != 2:
        raise Refuse('LADDER_SET', f'--ladders 는 사다리 시도 폴더 둘 (P0 · P1) · 받은 {len(dirs or [])}')
    sid_reg = {}
    lads, plan, plan_sha, code, _s0rec, _after, s0reps = _call(
        CH, '사다리 읽기 (사슬 load_ladders)', CH.load_ladders, [str(_path(d)) for d in dirs], None, str(_path(registration)), CH.RealContract(),
        sid_reg)
    return {'mode': 'full', 'lads': lads, 'plan': plan, 'plan_sha': plan_sha, 'code': code, 's0reps': s0reps,
            'files': ladder_files(lads)}


def ladders_summary(CH, dirs):
    """dry-run (plan) 전용 — 사다리 요약만 읽는다 (사슬 `read_summary` · `plan_record_or_stop` · `noop_record_problem` · `rj_key`).
    `load_ladders` 앞머리의 꼴 대조와 같은 칸이고, 원 팔 (R_j,0 확인 팔 · no-op 런) · 등록 계획 해시 · S0 보고 · 코드 핀은 다시 읽지 않는다 → run 은 늘 full."""
    if len(dirs or []) != 2:
        raise Refuse('LADDER_SET', f'--ladders 는 사다리 시도 폴더 둘 (P0 · P1) · 받은 {len(dirs or [])}')
    out, plan, plan_sha, seen = {}, None, None, set()
    for d in dirs:
        rd = Path(d).resolve()
        if rd in seen:
            raise Refuse('DUPLICATE_RUN', f'같은 사다리 폴더 두 번 {rd}')
        seen.add(rd)
        s, sha = CH.read_summary(rd, 'ladder_summary.json')
        if s is None:
            raise Refuse('LADDER_SET', f'{rd}: ladder_summary.json 이 없거나 못 읽는다 (일반 파일 · UTF-8 JSON 객체)')
        if s.get('stage') != 'ladder' or s.get('tool') != CH.TOOL or s.get('schema') != CH.SCHEMA:
            raise Refuse('LADDER_SET', f'{rd.name}: 이 사슬 ({CH.TOOL} · {CH.SCHEMA}) 의 사다리 요약이 아니다')
        if s.get('status') != 'CALIBRATED':
            raise Refuse('LADDER_NOT_CALIBRATED', f'{rd.name}: 사다리 상태 {s.get("status")!r} (CALIBRATED 여야)')
        if s.get('variant') is not None:
            raise Refuse('LADDER_SET', f'{rd.name}: 사다리 변이 {s.get("variant")!r} (주 사다리 = 변이 없음)')
        law = s.get('law')
        if law not in CH.LAWS or law in out:
            raise Refuse('LADDER_SET', f'{rd.name}: 법칙 {law!r} (둘 = {list(CH.LAWS)} 하나씩)')
        p = s.get('plan') if isinstance(s.get('plan'), dict) else {}
        _call(CH, f'{rd.name} 계획 기록', CH.plan_record_or_stop, p.get('content'), rd.name)
        if plan_sha is not None and p.get('sha256') != plan_sha:
            raise Refuse('PLAN_HASH_MISMATCH', '두 사다리의 계획이 다르다')
        L = s.get('ladder') if isinstance(s.get('ladder'), dict) else {}
        k0 = L.get('R_j0')
        if not rj_key_ok(CH, k0):
            raise Refuse('LADDER_SET', f'{rd.name}: R_j,0 {k0!r} — 유한 양수 R_j 키 (사슬 rj_key 꼴) 여야')
        why = CH.noop_record_problem(s.get('noop'), law, k0)
        if why:
            raise Refuse('LADDER_SET', f'{rd.name}: {why}')
        out[law] = {'dir': str(rd), 'summary_sha256': sha, 'variant': None, 'R_j0': k0, 'R_j_lo': L.get('R_j_lo'),
                    'R_j_hi': L.get('R_j_hi'), 'noop': dict(s['noop'])}
        plan, plan_sha = p.get('content'), p.get('sha256')
    if sorted(out) != sorted(CH.LAWS):
        raise Refuse('LADDER_SET', f'사다리 법칙 {sorted(out)} ≠ {list(CH.LAWS)}')
    return {'mode': 'summary', 'lads': out, 'plan': plan, 'plan_sha': plan_sha, 'code': None, 's0reps': None, 'files': ladder_files(out)}


def rj_key_ok(CH, k):
    """R_j,0 키 = 사슬 꼴 (`rj_key(rj_float(k)) == k`) · 유한 양수 (극한 'inf' · '0' 아님)."""
    if not isinstance(k, str) or k in CH.LIMIT_MARK:
        return False
    try:
        x = CH.rj_float(k)
        return math.isfinite(x) and x > 0 and CH.rj_key(x) == k
    except (TypeError, ValueError, OverflowError):
        return False


def ladder_files(lads):
    """사다리 R_j,0 출처 — 법칙마다 요약 파일 · sha256 · R_j,0 (σ 칸 없음)."""
    return {law: {'dir': v['dir'], 'summary_file': str(Path(v['dir']) / 'ladder_summary.json'), 'summary_sha256': v['summary_sha256'],
                  'R_j0': v['R_j0']} for law, v in sorted(lads.items())}


def load_ladders_for(CH, mode, dirs, registration):
    if mode == 'full':
        return ladders_full(CH, dirs, registration)
    if mode == 'summary':
        return ladders_summary(CH, dirs)
    raise Refuse('USAGE', f'--ladder-check {mode!r}')


# ═════════════════════════ 칸 (팔 · 법칙) 의 런 · env ═════════════════════════
def resolve_kit(CH, arm, kit2):
    """arm 1 = DBE 킷 그대로 (--kit2 금지) · arm 2 = 새 킷 이름 (등록 §2 · 러너 KITS 한 낱말 · DBE · SBE 킷 아님)."""
    if arm == 1:
        if kit2 is not None:
            raise Refuse('NOT_REGISTERED', 'arm 1 = DBE 킷 그대로 (등록 §2) — --kit2 를 주지 않는다')
        return CH.DBE_KIT
    if arm != 2:
        raise Refuse('NOT_REGISTERED', f'arm {arm!r} (등록 = 1 · 2)')
    if not (isinstance(kit2, str) and KIT_RE.fullmatch(kit2)):
        raise Refuse('NOT_REGISTERED', f'arm 2 의 --kit2 {kit2!r} — kit_<영문 · 숫자 · _ . -> 한 낱말 (러너 KITS)')
    if kit2 in (CH.DBE_KIT, CH.SBE_KIT):
        raise Refuse('NOT_REGISTERED', f'arm 2 의 --kit2 {kit2} = 봉인 R 킷 — 새 킷 (PTFE 0.5 · SDCP 0) 이어야 (등록 §2)')
    return kit2


def apply_override(env, override, arm):
    """등록 override 를 env 에 — 키 · 값 = `ARM_OVERRIDE[arm]` 정확히 · 있는 칸을 바꾸기만 (새 칸 덧붙임 = 거부)."""
    reg = ARM_OVERRIDE.get(arm)
    if reg is None:
        raise Refuse('NOT_REGISTERED', f'arm {arm!r}')
    bad = sorted(k for k, v in override.items() if reg.get(k) != v)
    if bad or set(override) != set(reg):
        raise Refuse('UNKNOWN_OVERRIDE', f'arm {arm} override {sorted(override)} ≠ 등록 {sorted(reg)} (값까지 · 등록 밖 칸 {bad})')
    miss = sorted(k for k in override if k not in env)
    if miss:
        raise Refuse('UNKNOWN_OVERRIDE', f'override {miss} 가 사슬 env 에 없는 칸 — 바꾸기만 (덧붙임 아님)')
    out = dict(env)
    out.update(override)
    return out


def env_diff(ref, mid):
    """두 env → {칸: {'r_unit': 봉인 R 단위 값 | None, 'arm': 이 팔 값 | None}} (다른 칸만)."""
    return {k: {'r_unit': ref.get(k), 'arm': mid.get(k)} for k in sorted(set(ref) | set(mid)) if ref.get(k) != mid.get(k)}


def diff_problem(CH, diff, arm, kit):
    """env 차이 → 사유 | None — 칸 집합 = `ARM_DIFF_KEYS[arm]` 정확히 · ① 값 = 등록 override · ② = DBE 킷 → 새 킷."""
    want = set(ARM_DIFF_KEYS[arm])
    if set(diff) != want:
        return (f'봉인 R 단위 env 와 다른 칸 {sorted(diff)} ≠ 등록 {sorted(want)} — 등록 밖 칸 '
                f'{sorted(set(diff) - want)} · 빠진 칸 {sorted(want - set(diff))}')
    if arm == 1:
        d = diff['SIGMA_SDCP_OVERRIDE']
        if d['arm'] != ARM_OVERRIDE[1]['SIGMA_SDCP_OVERRIDE'] or d['r_unit'] != CH.ENV_FIXED['SIGMA_SDCP_OVERRIDE']:
            return f'SIGMA_SDCP_OVERRIDE {d} ≠ 봉인 {CH.ENV_FIXED["SIGMA_SDCP_OVERRIDE"]!r} → 등록 {ARM_OVERRIDE[1]["SIGMA_SDCP_OVERRIDE"]!r}'
    if arm == 2 and diff['KITS'] != {'r_unit': CH.DBE_KIT, 'arm': kit}:
        return f'KITS {diff["KITS"]} ≠ {CH.DBE_KIT} → {kit}'
    return None


_MR = {}


def middle_runner_class(CH):
    """봉인 `Runner` 그대로 + 등록 override (env_delta 끝 · `apply_override` 가 등록 칸만 받는다)."""
    if id(CH) not in _MR:
        class MiddleRunner(CH.Runner):
            def __init__(self, *a, arm=None, **k):
                super().__init__(*a, **k)
                self.arm = arm

            def env_delta(self, req, outdir):
                return apply_override(super().env_delta(req, outdir), ARM_OVERRIDE[self.arm], self.arm)
        _MR[id(CH)] = MiddleRunner
    return _MR[id(CH)]


class _CallRecorder:
    """`unit_runs` 의 rn 자리 — 봉인 단위가 낼 런 요청을 받아 적기만 한다 (러너 없음)."""

    def __init__(self):
        self.calls = []

    def run(self, kit, role, law, c, rj, arms, sv_cf=False):
        self.calls.append({'kit': kit, 'role': role, 'law': law, 'c': c, 'rj': rj, 'arms': arms, 'sv_cf': bool(sv_cf)})


def unit_calls(CH, lads, plan, law):
    """봉인 단위 <법칙>_c0_R_j0 의 런 요청 차례 — 사슬 `unit_runs` (no-op 기록 확인 · 모서리 arm 0 · SV 반사실 = `Predict._sv_on` · origin 팔)."""
    rec = _CallRecorder()
    pr = CH.Predict(None, lads, None, sv_scope=plan['sv_cf_scope'])
    u = {'kind': 'unit', 'name': CH.unit_name(CELL_C, law, CELL_ROLE), 'law': law, 'c': CELL_C, 'rj_role': CELL_ROLE}
    _call(CH, f'봉인 단위 {u["name"]} 런 차례 (사슬 unit_runs)', CH.unit_runs, pr, rec, 'unit', u, lads)
    k0 = lads[law][CELL_ROLE]
    if not rec.calls:
        raise Refuse('UNIT_RUNS', f'사슬 unit_runs 가 {u["name"]} 에 런을 내지 않았다')
    for cl in rec.calls:
        if cl['kit'] != CH.DBE_KIT or cl['law'] != law or cl['c'] != CELL_C or cl['rj'] != k0:
            raise Refuse('UNIT_RUNS', f'사슬 unit_runs 런 {cl["role"]} = 킷 {cl["kit"]} · {cl["law"]} · c {cl["c"]!r} · R_j {cl["rj"]} '
                                      f'(봉인 단위 = {CH.DBE_KIT} · {law} · c 0 · R_j,0)')
    return rec.calls, u['name']


def build_cell(CH, arm, law, kit2, plan, lads, runner, root, out, machine=None, cjunc_store=None, parent_env=None):
    """칸 하나 (팔 · 법칙 · c 0 · R_j,0) → 런마다 이 팔의 요청 · env + 봉인 R 단위 env 와의 차이 (같은 out · 같은 이름 = 같은 OUTDIR).
    차이 칸이 등록과 다르면 거부 (러너 전)."""
    if law not in CH.LAWS:
        raise Refuse('NOT_REGISTERED', f'법칙 {law!r} (= {list(CH.LAWS)})')
    kit = resolve_kit(CH, arm, kit2)
    calls, uname = unit_calls(CH, lads, plan, law)
    kw = dict(dry=True, parent_env=parent_env, prefix=CH.UNIT_PREFIX, machine=machine, cjunc_store=cjunc_store)
    ref = CH.Runner(runner, root, out, plan, None, 0.0, None, **kw)
    mid = middle_runner_class(CH)(runner, root, out, plan, None, 0.0, None, arm=arm, **kw)
    runs = []
    for cl in calls:
        rname, rreq, rout, renv = _call(CH, '봉인 R 단위 요청', ref._prepare, cl['kit'], cl['role'], cl['law'], cl['c'], cl['rj'], cl['arms'], cl['sv_cf'])
        mname, mreq, mout, menv = _call(CH, f'arm {arm} 요청', mid._prepare, kit, cl['role'], cl['law'], cl['c'], cl['rj'], cl['arms'], cl['sv_cf'])
        if (rname, rout) != (mname, mout):
            raise Refuse('ENV_DIFF', f'런 이름 · 폴더 {mname} · {mout} ≠ 봉인 단위 {rname} · {rout}')
        dreq = sorted(k for k in set(rreq) | set(mreq) if rreq.get(k) != mreq.get(k))
        if dreq != sorted(ARM_REQ_DIFF[arm]):
            raise Refuse('ENV_DIFF', f'{mname}: 요청 칸 차이 {dreq} ≠ 등록 {sorted(ARM_REQ_DIFF[arm])}')
        diff = env_diff(renv, menv)
        why = diff_problem(CH, diff, arm, kit)
        if why:
            raise Refuse('ENV_DIFF', f'{mname}: {why}')
        runs.append({'name': mname, 'req': mreq, 'outdir': mout, 'env': menv, 'env_diff': diff, 'call': cl})
    return {'arm': arm, 'law': law, 'kit': kit, 'rj': lads[law][CELL_ROLE], 'unit': uname, 'runs': runs, 'scrubbed': list(mid.scrubbed)}


@contextlib.contextmanager
def expect_sdcp_sigma(CH, value):
    """arm 1 판독 — 사슬 `read_run` 의 매니페스트 기대값 중 `MAN_FIXED['sigma_sdcp_S_cm']` 한 칸만 등록 값으로 (이 프로세스의 모듈 객체 ·
    파일 무변경 · 끝나면 되돌린다) · None = 그대로."""
    if value is None:
        yield
        return
    old = CH.MAN_FIXED
    new = dict(old)
    new['sigma_sdcp_S_cm'] = float(value)
    CH.MAN_FIXED = new
    try:
        yield
    finally:
        CH.MAN_FIXED = old


def cmd_line(CH, root, runner, env):
    return f'(cwd {root}) env ' + ' '.join(f'{k}={shlex.quote(str(env[k]))}' for k in sorted(env)) + f' bash {shlex.quote(str(runner))}'


def _diff_text(diff):
    return ' · '.join(f'{k} {v["r_unit"]} → {v["arm"]}' for k, v in sorted(diff.items()))


# ═════════════════════════ plan (dry-run) ═════════════════════════
def _common(CH, a):
    """plan · run 공통 — 금지 env · 계획 (사슬 load_plan · 결과 전 등록 숫자) · 사다리 (R_j,0) · 계획 = 사다리 계획."""
    _call(CH, 'env', CH.env_forbidden_or_stop)
    plan, plan_sha = _call(CH, '계획 (사슬 load_plan)', CH.load_plan, a.plan)
    _call(CH, '계획 등록 숫자', CH.require_plan_numbers, plan)
    L = load_ladders_for(CH, a.ladder_check, a.ladders, a.registration)
    if L['plan_sha'] != plan_sha:
        raise Refuse('PLAN_HASH_MISMATCH', f'--plan sha256 {plan_sha[:16]}… ≠ 사다리 계획 {str(L["plan_sha"])[:16]}… (봉인 R 계획이어야)')
    return plan, plan_sha, L


def cmd_plan(a):
    CH = load_chain()
    plan, plan_sha, L = _common(CH, a)
    runner = _path(a.runner).resolve() if a.runner else (HERE / CH.RUNNER_NAME)
    root, out = _path(a.root), _path(a.out)
    if a.cjunc_store is not None:
        why = CH.cjunc_store_dir_problem(a.cjunc_store)
        if why:
            raise Refuse('NOT_REGISTERED', f'--cjunc-store {a.cjunc_store}: {why}')
    say(f'부록 팔 plan (러너를 부르지 않는다) — 사슬 rint_r_chain.py sha256 {chain_sha(CH)[:16]}… · 계획 {plan_sha[:16]}… · '
        f'사다리 읽기 {L["mode"]}' + (' (요약만 · dry-run 전용 · run = full)' if L['mode'] == 'summary' else ' (사슬 load_ladders)'))
    for law, f in L['files'].items():
        say(f'  사다리 {law} R_j,0 = {CH.disp_rj(f["R_j0"])} ← {f["summary_file"]} (sha256 {f["summary_sha256"][:16]}…)')
    if a.arm == 2 and a.kit2 is None:
        raise Refuse('NOT_REGISTERED', '--arm 2 는 --kit2 (새 킷 이름) 가 필요하다')
    arms = [a.arm] if a.arm else list(ARM_CHOICES)
    laws = [a.law] if a.law else list(CH.LAWS)
    n = 0
    for arm in arms:
        if arm == 2 and a.kit2 is None:
            say('[칸] arm 2 — --kit2 (새 킷 이름) 없음 → 건너뜀')
            continue
        for law in laws:
            cell = build_cell(CH, arm, law, a.kit2 if arm == 2 else None, plan, L['lads'], runner, root, out, machine=a.machine,
                              cjunc_store=a.cjunc_store)
            n += 1
            ov = ' · '.join(f'{k}={v}' for k, v in ARM_OVERRIDE[arm].items()) or '없음'
            say(f'[칸] arm {arm} · {law} · c {CELL_C} · R_j,0 {CH.disp_rj(cell["rj"])} · 킷 {cell["kit"]} · override {ov} · 봉인 R 단위 {cell["unit"]}')
            for r in cell['runs']:
                q = r['req']
                say(f'  {r["name"]} ({q["role"]} · 팔 {CH.arm_indices(q)}{" · SV 반사실 켬" if q["sv_cf"] else ""}) — 봉인 R 단위 env 와 다른 칸: '
                    f'{_diff_text(r["env_diff"])}')
                say('    ' + cmd_line(CH, root, runner, r['env']))
            if cell['scrubbed']:
                say(f'  부모 셸에서 지울 env (사슬 Runner 규칙): {cell["scrubbed"]}')
    say(f'plan = {n} 칸 · env 차이 = 등록 칸뿐 (arm 1 {list(ARM_DIFF_KEYS[1])} · arm 2 {list(ARM_DIFF_KEYS[2])}) · OUTDIR = run 의 --out 아래 같은 이름')
    return 0


# ═════════════════════════ run ═════════════════════════
def run_preflight(CH, arm, kit, plan, L, runner, root):
    """러너 전 — 킷 · 러너 있음 · 지금 코드 = 깨끗한 git (사슬 `code_record` · `code_dirty_problem`) · 코드 파일 지문 = 사다리 기록 (봉인 R 코드) ·
    환경 = 계획 봉인 판 (`env_seal_problem`) · arm 1 침대 = S0 단계 2 보고의 DBE 침대 (`bed_problem`) · arm 2 = 새 킷 입력 지문 기록 (`kit_bed`)."""
    for p in (Path(root) / kit, Path(runner)):
        if not p.exists():
            raise Refuse('KIT_MISSING', f'{p}')
    code = _call(CH, '코드 기록', CH.code_record, str(runner))
    why = CH.code_dirty_problem(code)
    if why:
        raise Refuse('CODE_PIN_MISMATCH', f'지금 코드 — {why}')
    lc = L.get('code') if isinstance(L.get('code'), dict) else {}
    diff = [k for k in ('files', 'runner_files', 'runner_sha256') if code.get(k) != lc.get(k)]
    if diff:
        names = CH.code_diff_names(code.get('files'), lc.get('files')) if 'files' in diff else []
        raise Refuse('CODE_PIN_MISMATCH', f'코드 파일 지문 {diff} ≠ 사다리 기록 (봉인 R 코드 · {names}) — 봉인 R 과 같은 코드 파일로 돌릴 것')
    why = CH.env_seal_problem(code, plan)
    if why:
        raise Refuse('CODE_PIN_MISMATCH', why)
    s2 = ((L.get('s0reps') or {}).get('stage2') or {}) if isinstance(L.get('s0reps'), dict) else {}
    if arm == 1:
        bed = _call(CH, 'DBE 침대 = S0 단계 2 (사슬 bed_problem)', CH.bed_problem, L.get('s0reps'), str(root), (CH.DBE_KIT,))
        bed_diff = []
    else:
        got = _call(CH, f'{kit} 입력 지문 (사슬 kit_bed)', CH.kit_bed, str(root), kit)
        bed = {kit: got}
        bed_diff = CH._bed_diff(CH.bed_view(s2.get('inputs')), got)
    return {'code': code, 'bed': bed, 'bed_diff_vs_dbe': bed_diff}


def _run_record(CH, rn, plan_run, out):
    """런 하나의 매니페스트 줄 — 사슬 런 기록 (요청 · rc · 시간 · arms_read = ARM_PUBLIC (σ 없음) 또는 파일 신원) + env 차이 · 그룹 기록 · 팔 파일 sha256."""
    recs = [r for r in rn.records if r.get('name') == plan_run['name']]
    rec = dict(recs[-1]) if recs else {k: plan_run['req'].get(k) for k in CH.REQ_KEYS}
    rec.setdefault('outdir', plan_run['outdir'].name)
    rec['env'] = dict(plan_run['env'])
    rec['env_diff'] = dict(plan_run['env_diff'])
    rec['arm_indices'] = CH.arm_indices(plan_run['req'])
    lp = Path(out) / CH.GROUPS_DIR / f'{plan_run["name"]}.launch.json'
    if lp.exists():
        L, er, bound = CH.group_pair(lp)
        rec['group'] = {'started_utc': (L or {}).get('started_utc'), 'ended_utc': (er or {}).get('ended_utc'),
                        'confirmed': (er or {}).get('confirmed'), 'bound': bool(bound)}
    else:
        rec['group'] = None
    od = Path(out) / rec['outdir']
    rec['arm_files'] = CH.arm_file_shas(od) if od.is_dir() else []
    return rec


def _write_manifest(CH, out, man):
    CH.write_summary(Path(out) / MANIFEST, man)


def cmd_run(a):
    out = _path(a.out)
    if os.path.lexists(str(out)):
        raise Refuse('OUTDIR_EXISTS', f'{out} 가 이미 있다 — 런마다 새 --out (그 폴더에는 아무것도 쓰지 않는다)')
    if a.ladder_check != 'full':
        raise Refuse('USAGE', 'run 의 사다리 읽기 = full (사슬 load_ladders) 뿐')
    CH = load_chain()
    plan, plan_sha, L = _common(CH, a)
    if a.machine is None or not CH.MACHINE_RE.fullmatch(str(a.machine)) or a.machine not in plan['exec_policy']['allowed_machines']:
        raise Refuse('MACHINE_NOT_ALLOWED', f'--machine {a.machine!r} ∉ 계획 exec_policy.allowed_machines {plan["exec_policy"]["allowed_machines"]} '
                                            f'(봉인 R 이 돈 기계 · 등록 §6)')
    mh = plan['exec_policy']['max_hours'] if a.max_hours is None else a.max_hours
    if not (isinstance(mh, (int, float)) and not isinstance(mh, bool) and math.isfinite(mh) and mh > 0):
        raise Refuse('USAGE', f'--max-hours {mh!r} (유한 > 0)')
    if a.cjunc_store is not None:
        why = CH.cjunc_store_dir_problem(a.cjunc_store)
        if why:
            raise Refuse('NOT_REGISTERED', f'--cjunc-store {a.cjunc_store}: {why}')
    runner = _path(a.runner).resolve() if a.runner else (HERE / CH.RUNNER_NAME).resolve()
    root = _path(a.root).resolve()
    cell = build_cell(CH, a.arm, a.law, a.kit2, plan, L['lads'], runner, root, out.resolve(), machine=a.machine, cjunc_store=a.cjunc_store)
    pre = run_preflight(CH, a.arm, cell['kit'], plan, L, runner, root)
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.mkdir(str(out))
    except FileExistsError:
        raise Refuse('OUTDIR_EXISTS', f'{out} 가 그사이 생겼다')
    out = out.resolve()
    reg = _path(a.registration)
    man = {'tool': TOOL, 'schema': SCHEMA, 'registration_doc': REG_DOC, 'status': 'RUNNING', 'stop': None,
           'arm': a.arm, 'law': a.law, 'c': CELL_C, 'rj_role': CELL_ROLE, 'rj': cell['rj'], 'kit': cell['kit'], 'unit': cell['unit'],
           'override': dict(ARM_OVERRIDE[a.arm]),
           'chain': {'file': str(Path(CH.__file__).resolve()), 'sha256': chain_sha(CH)},
           'driver': {'file': str(Path(__file__).resolve()), 'sha256': _sha256(__file__)},
           'plan': {'file': str(Path(a.plan).resolve()), 'sha256': plan_sha},
           'registration_R': {'file': str(reg.resolve()), 'sha256': _sha256(reg) if reg.is_file() else None},
           'ladders': L['files'], 'ladder_check': L['mode'],
           'runner': {'file': str(runner), 'sha256': _sha256(runner)}, 'root': str(root), 'machine': a.machine, 'max_hours': mh,
           'cjunc_store': a.cjunc_store, 'code': pre['code'], 'bed': pre['bed'], 'bed_diff_vs_dbe': pre['bed_diff_vs_dbe'],
           'env_scrubbed': cell['scrubbed'], 'value_seal': 'σ = 러너 팔 JSON 에만 (이 기록 · 화면에 없음)',
           'start_utc': _utc(), 'end_utc': None,
           'runs': [dict({k: r['req'].get(k) for k in CH.REQ_KEYS}, outdir=r['outdir'].name, env=r['env'], env_diff=r['env_diff'],
                         arm_indices=CH.arm_indices(r['req']), rc=None, arms_read=[], read={'status': 'not_run'}) for r in cell['runs']]}
    _write_manifest(CH, out, man)
    say(f'부록 팔 run — arm {a.arm} · {a.law} · c {CELL_C} · R_j,0 {CH.disp_rj(cell["rj"])} · 킷 {cell["kit"]} · override '
        f'{dict(ARM_OVERRIDE[a.arm]) or "없음"} · out {out}')
    say(f'  사슬 sha256 {chain_sha(CH)[:16]}… · 코드 파일 지문 = 사다리 기록 · 환경 = 계획 봉인 판 · 침대 '
        + ('= S0 단계 2 (DBE)' if a.arm == 1 else f'{cell["kit"]} 입력 지문 기록 (DBE 와 다른 역할 {pre["bed_diff_vs_dbe"]})'))
    rn = middle_runner_class(CH)(runner, root, out, plan, None, time.time() + float(mh) * 3600.0, CH.RealContract(),
                                 prefix=CH.UNIT_PREFIX, machine=a.machine, cjunc_store=a.cjunc_store, arm=a.arm)
    rn.sid_reg = {}
    rn.s0_grid = CH.s0_grid_seed(L.get('s0reps')) if a.arm == 1 else None        # arm 1 = DBE 침대 · arm 0 sid = S0 off 격자 지문
    rn.s0_census = CH.s0_census_seed(L.get('s0reps')) if a.arm == 1 else None    # arm 1 = DBE 봉인 SV census (기하)
    rn.graph_src = None                                                          # SV 끝 그래프 봉인 원천 없음 = 귀속 미확인 (기록)
    status, rc, n_nc = 'RUNNING', 3, 0
    try:
        with expect_sdcp_sigma(CH, ARM1_SIGMA_SDCP if a.arm == 1 else None):
            for i, pr in enumerate(cell['runs']):
                cl = pr['call']
                read = {'status': 'stopped', 'stop': None}
                try:
                    rn.run(cell['kit'], cl['role'], cl['law'], cl['c'], cl['rj'], cl['arms'], cl['sv_cf'])
                    read = {'status': 'ok'}
                except CH.Stop as e:
                    last = rn.records[-1] if rn.records else {}
                    #  등록 결과 NOT_COMPUTED (러너 rc 0 · 그룹 확인 · 팔 판독에서 증서 · 수렴 실패 · 단락) = 이 런의 결손 — 다음 런을 돈다 (등록 개정 1 ②) ·
                    #    그 밖 멈춤 (러너 · 시간 · 그룹 · 계약 · 기록) = 칸 멈춤
                    if e.code == 'NOT_COMPUTED' and last.get('name') == pr['name'] and CH.rc_success(last.get('rc')):
                        read = {'status': 'not_computed', 'state': stop_state(CH, e), 'stop': e.record()}
                        n_nc += 1
                        CH.print_stop(e)
                    else:
                        read = {'status': 'stopped', 'stop': e.record()}
                        raise
                finally:
                    man['runs'][i] = _run_record(CH, rn, pr, out)
                    man['runs'][i]['read'] = read
                    _write_manifest(CH, out, man)
                if rn.records[-1].get('name') != pr['name']:
                    raise Refuse('ENV_DIFF', f'런 이름 {rn.records[-1].get("name")} ≠ 계획 {pr["name"]}')
        status, rc = 'DONE', 0
    except CH.Stop as e:
        status, man['stop'] = 'STOPPED', e.record()
        CH.print_stop(e)
    except Refuse as e:
        status, man['stop'] = 'STOPPED', {'code': e.code, 'cause': e.why}
        say(f'거부 [{e.code}] {e.why}')
    except BaseException as e:
        status, man['stop'] = 'INTERRUPTED', {'code': type(e).__name__, 'cause': str(e)[:300]}
        raise
    finally:
        man['status'], man['end_utc'] = status, _utc()
        _write_manifest(CH, out, man)
    say(f'run = {status} · 런 {len(rn.records)}/{len(cell["runs"])} · 판독 NOT_COMPUTED (등록 결과 · 결손) {n_nc} · 매니페스트 {out / MANIFEST}')
    return rc


# ═════════════════════════ check-mono (등록 §4 구조 확인 · 등록 개정 1 · 1저자 11-24 · Codex SBD S4b) ═════════════════════════
#: 팔 상태 — 계산됨 = POSITIVE (사슬 해 상태 positive) · PATH_CUT (사슬 해 상태 zero = VALID_ZERO_TOPOLOGY · 판에 닿는 경로가 끊겨 σ 0 · 팔 JSON 증서 ·
#:   성분 기록 대조) · 결손 = SOLVE_FAILED (사슬 read_run 멈춤 NOT_COMPUTED · 구조화 사유 없음 = 증서 · 수렴 실패) · NOT_COMPUTED (사유 ELECTRODE_SHORT ·
#:   판독 전 멈춘 런 · 같은 런의 앞 팔에서 멈춰 읽지 않은 팔 · 봉인 R 단위에 없는 런)
ARM_POS, ARM_CUT, ARM_FAIL, ARM_NC = 'POSITIVE', 'PATH_CUT', 'SOLVE_FAILED', 'NOT_COMPUTED'
COMPUTED = (ARM_POS, ARM_CUT)
#: 팔 판정 — 결손이 있으면 비교하지 않는다 (MISSING · 사유) · 두 쪽 계산됨 = 두 런 증서 띠 (사슬 arm_band · 같은 함수)
V_PASS, V_UNDET, V_VIOL, V_MISS = 'PASS', 'MONO_UNDETERMINED', 'MONO_VIOLATION', 'MISSING'
OVERALL_RC = {'PASS': 0, 'NO_VIOLATION': 0, V_VIOL: 1, 'NO_COMPARISON': 3}
MONO_SCHEMA = 'rint2-middle-arm-mono-v1'
MONO_LABEL = '고정 기하 벌크 전도 대조 (DBE 기하 · σ_SDCP 정상 → 0)'
MONO_RULE = ('등록 개정 1 (1저자 11-24 · Codex SBD S4b) — 띠 = 사슬 arm_band (두 런 같은 함수 · σ_lo = scale·target_lo · σ_hi = scale·target_hi) · '
             '위반 MONO_VIOLATION = σ_lo(①) > σ_hi(DBE) (도구 결함 → 멈춤 · 보고) · 점값 역전 + 구간 겹침 = MONO_UNDETERMINED (보고만) · '
             'PATH_CUT 0 = 정상 통과 · SOLVE_FAILED · NOT_COMPUTED = 결손 (비교 안 함) · 짝 (P · R_j,0 · 격자 원점 · 경계 · env 조립) 다름 = 비교 거부')
RECORD_SEAL = 'σ 띠 = 값 — 이 칸 기록은 리포 밖에 둔다 (등록 §5 · R 판정 12-05 전 리포 기록 금지 · 화면에는 판정만)'
_STOP_ARM_RE = re.compile(r'p2_\S*?_a(\d+)\.json: ')
_SIDE = {'dbe': 'DBE', 'arm1': '①'}


def read_unit_summary(CH, d):
    """봉인 R 단위 시도 폴더 → (요약, sha256) — 사슬 `read_summary` · `unit_summary_problem` (자기 대조) · UNIT_DONE 또는 NOT_COMPUTED (등록 결과 · 결손은
    결손대로) · 변이 없음 · c 0 · R_j,0."""
    s, sha = CH.read_summary(Path(d), CH.UNIT_SUMMARY['unit'])
    if s is None:
        raise Refuse('UNIT_SUMMARY', f'{d}: {CH.UNIT_SUMMARY["unit"]} 이 없거나 못 읽는다 (봉인 R 단위 시도 폴더 attempt_<n> 이어야)')
    u = s.get('unit') if isinstance(s.get('unit'), dict) else {}
    at = s.get('attempt') if isinstance(s.get('attempt'), dict) else {}
    want = _call(CH, 'R 단위 요약 출처 칸 (사슬 merge_want)', CH.merge_want, s)
    why = _call(CH, 'R 단위 요약', CH.unit_summary_problem, s, 'unit', u.get('target'), at.get('n'), {'machine': s.get('machine')}, want)
    if why:
        raise Refuse('UNIT_SUMMARY', f'{d}: {why}')
    ok_nc = s.get('status') == 'NOT_COMPUTED' and (s.get('stop') or {}).get('code') == 'NOT_COMPUTED'
    if not (s.get('status') == CH.UNIT_DONE['unit'] or ok_nc) or s.get('variant') is not None:
        raise Refuse('UNIT_SUMMARY', f'{d}: 상태 {s.get("status")!r} · 변이 {s.get("variant")!r} (UNIT_DONE · 등록 결과 NOT_COMPUTED · 변이 없음)')
    if u.get('law') not in CH.LAWS or u.get('c') != CELL_C or u.get('rj_role') != CELL_ROLE:
        raise Refuse('UNIT_SUMMARY', f'{d}: 단위 {u.get("name")!r} — DBE c 0 · R_j,0 단위여야 (등록 §4 "DBE c0 같은 칸")')
    _call(CH, 'R 단위 계획 기록', CH.plan_record_or_stop, (s.get('plan') or {}).get('content'), 'R 단위')
    return s, sha


def read_manifest(CH, d):
    s, sha = CH.read_summary(Path(d), MANIFEST)
    if s is None:
        raise Refuse('MANIFEST', f'{d}: {MANIFEST} 이 없거나 못 읽는다')
    if s.get('tool') != TOOL or s.get('schema') != SCHEMA:
        raise Refuse('MANIFEST', f'{d}: 이 도구 ({TOOL} · {SCHEMA}) 의 매니페스트가 아니다')
    if s.get('status') not in ('DONE', 'STOPPED'):
        raise Refuse('MANIFEST', f'{d}: 상태 {s.get("status")!r} (DONE · STOPPED 이어야 — RUNNING · INTERRUPTED = 끝나지 않은 · 끊긴 런)')
    if s.get('arm') != 1 or s.get('kit') != CH.DBE_KIT or s.get('override') != ARM_OVERRIDE[1]:
        raise Refuse('MANIFEST', f'{d}: arm {s.get("arm")!r} · 킷 {s.get("kit")!r} · override {s.get("override")!r} — check-mono = arm 1 (DBE · σ_SDCP 0)')
    if (s.get('chain') or {}).get('sha256') != chain_sha(CH):
        raise Refuse('MANIFEST', f'{d}: 런의 사슬 sha256 {str((s.get("chain") or {}).get("sha256"))[:16]}… ≠ 지금 사슬 {chain_sha(CH)[:16]}…')
    return s, sha


_PAIR_KEYS = ('name', 'role', 'kit', 'law', 'c', 'rj', 'arms', 'arm_list', 'variant', 'sv_cf')
#: env 조립 대조 밖 칸 — 실행 자리 (저장본 폴더 = 원장 캐시 · 물리 아님 · 결과 비트 같음이 그 모듈의 계약) · OUTDIR 은 같은 값으로 다시 조립해 대조한다
_ENV_LOCATION_KEYS = ('CJUNC_STORE',)


def env_pair_problem(CH, plan, r):
    """① 런 하나의 env 기록 ↔ 사슬 `runner_env_delta` (그 런 요청 · R 단위 계획 · 같은 OUTDIR) → 사유 | None — 차이 = 등록 override 한 칸뿐이어야."""
    env = r.get('env')
    if not isinstance(env, dict) or not isinstance(env.get('OUTDIR'), str):
        return f'런 {r.get("name")}: env 기록이 없다'
    req = {k: r.get(k) for k in CH.REQ_KEYS}
    try:
        ref = CH.runner_env_delta(plan, None, req, env['OUTDIR'])
    except Exception as e:                                  # noqa: BLE001 — 다시 조립 못 함 = 짝 확인 못 함 = 거부
        return f'런 {r.get("name")}: 봉인 R 단위 env 를 다시 조립하지 못했다 ({type(e).__name__}: {str(e)[:120]})'
    a = {k: v for k, v in ref.items() if k not in _ENV_LOCATION_KEYS}
    b = {k: v for k, v in env.items() if k not in _ENV_LOCATION_KEYS}
    why = diff_problem(CH, env_diff(a, b), 1, CH.DBE_KIT)
    return f'런 {r.get("name")}: env 조립 ≠ 봉인 R 단위 env + 등록 override — {why}' if why else None


def pair_problem(CH, su, man):
    """짝 조건 (등록 개정 1 ③) — 같은 P · 같은 R_j,0 (그 P 법칙의 봉인 값 · 같은 사다리 요약) · 같은 계획 · 같은 런 차례 (요청 칸 · 팔 번호 = 격자 원점) ·
    같은 침대 (DBE 킷 원 입력 · 설정 = 경계 · 기하) · 같은 env 조립 → 사유 | None.  (원점 shift · sid 격자 · S0 off 격자 지문 · vox · 브리지 · 판 경계 칸은 두 쪽
    다 사슬 read_run 이 같은 sid_reg 로 다시 본다.)"""
    law = (su.get('unit') or {}).get('law')
    if man.get('law') != law or man.get('c') != CELL_C or man.get('rj_role') != CELL_ROLE:
        return f'법칙 · c · 역할 {man.get("law")} · {man.get("c")!r} · {man.get("rj_role")} ≠ R 단위 {law} · 0 · R_j0'
    lad = su.get('ladders') if isinstance(su.get('ladders'), dict) else {}
    if man.get('rj') != (lad.get(law) or {}).get('R_j0'):
        return f'R_j,0 {man.get("rj")} ≠ R 단위 사다리 R_j,0 {(lad.get(law) or {}).get("R_j0")}'
    ml = man.get('ladders') if isinstance(man.get('ladders'), dict) else {}
    for L in CH.LAWS:
        if (ml.get(L) or {}).get('summary_sha256') != (lad.get(L) or {}).get('summary_sha256'):
            return f'{L} 사다리 요약 sha256 ≠ R 단위가 읽은 사다리 (같은 봉인 사다리여야)'
    if (man.get('plan') or {}).get('sha256') != (su.get('plan') or {}).get('sha256'):
        return '계획 sha256 ≠ R 단위 계획'
    du, mu = list(su.get('runs') or []), list(man.get('runs') or [])
    if not mu or len(du) > len(mu) or (len(du) < len(mu) and su.get('status') != 'NOT_COMPUTED'):
        return f'런 수 R 단위 {len(du)} · arm 1 {len(mu)} (UNIT_DONE = 같은 수 · NOT_COMPUTED 단위 = 앞 런만)'
    for x, y in zip(du, mu):
        if tuple(repr(x.get(k)) for k in _PAIR_KEYS) != tuple(repr(y.get(k)) for k in _PAIR_KEYS):
            return f'런 {y.get("name")} 요청 칸 (이름 · 역할 · 킷 · 법칙 · c · R_j · 팔 · 고르기 · 변이 · SV) ≠ R 단위 {x.get("name")}'
    mb = (man.get('bed') or {}).get(CH.DBE_KIT) if isinstance(man.get('bed'), dict) else None
    sb = (su.get('bed') or {}).get(CH.DBE_KIT) if isinstance(su.get('bed'), dict) else None
    if mb is None or mb != sb:
        return '침대 지문 (DBE 킷 원 입력 · 설정 = 경계 · 기하) ≠ R 단위 침대'
    plan = (su.get('plan') or {}).get('content')
    for r in mu:
        why = env_pair_problem(CH, plan, r)
        if why:
            return why
    return None


def stop_state(CH, e):
    """사슬 read_run 의 Stop NOT_COMPUTED → 결손 상태 — 구조화 사유 ELECTRODE_SHORT = NOT_COMPUTED (생산자 미게시 · 풀이 없음) · 사유 없음 = SOLVE_FAILED."""
    return ARM_NC if e.reason == CH.SHORT_STATUS else ARM_FAIL


def zero_confirm(CH, base, rec, r, side):
    """PATH_CUT — 판독 zero 인 팔의 JSON 증서 · 성분 기록 (사슬 read_run 이 next_gen_state 로 대조한 칸) 을 다시 열어 영값 위상 출처를 싣는다 → 칸."""
    p = Path(base) / str(rec.get('outdir')) / str(r.get('file'))
    try:
        payload = json.loads(p.read_bytes().decode('utf-8'))
    except (OSError, UnicodeDecodeError, ValueError) as e:
        raise Refuse('PATH_CUT_UNCONFIRMED', f'{side} {p.name}: 팔 JSON 을 못 읽는다 ({type(e).__name__})')
    s3 = CH.RC.step3_of(payload) if isinstance(payload, dict) else None
    s3 = s3 if isinstance(s3, dict) else {}
    cert = s3.get('conv_cert') if isinstance(s3.get('conv_cert'), dict) else {}
    man = s3.get('manifest') if isinstance(s3.get('manifest'), dict) else {}
    comp = ((man.get('components') or {}).get('electronic') or {}).get('status') if isinstance(man.get('components'), dict) else None
    z = {'status': cert.get('status'), 'zero_source': cert.get('zero_source'), 'zero_graph': cert.get('zero_graph'), 'reason': cert.get('reason'),
         'component': comp}
    if z['status'] != CH.REG_STATES['zero'][0] or z['zero_source'] not in ('early_return', 'matrix_graph') or comp not in ('not_solvable', 'complete'):
        raise Refuse('PATH_CUT_UNCONFIRMED', f'{side} {p.name}: 판독 = zero 인데 증서 · 성분 기록 {z} — VALID_ZERO_TOPOLOGY (판에 닿는 경로 끊김) 로 확인되지 않는다')
    return z


def run_arms(CH, base, rec, plan, contract, sid_reg, s0_grid, s0_census, side, sdcp=None, seen=None):
    """런 기록 하나 → {팔 번호: {'state', 'rec', 'why'[, 'zero']}} — 사슬 read_run (팔 계약 전부 · 기록 sha256) · 해 상태 positive = POSITIVE · zero = PATH_CUT
    (증서 · 성분 기록 대조) · read_run 멈춤 NOT_COMPUTED = SOLVE_FAILED | NOT_COMPUTED (`stop_state` · 그 팔 = 사유의 팔 파일 · 같은 런 다른 팔 = 읽지 않음) ·
    판독 전 멈춘 런 = NOT_COMPUTED · 그 밖 멈춤 = 비교 거부 (Refuse) · seen = 그 런의 판독 기록 (① 매니페스트 read · R 단위 상태) — 다시 읽기와 다르면 REPLAY_MISMATCH."""
    nm = rec.get('name')
    if not isinstance(nm, str) or 'arms' not in rec or CH.request_fields_problem(rec) or not isinstance(rec.get('kit'), str):
        raise Refuse('RUN_RECORD', f'{side} 런 기록 {nm!r} 꼴 ({CH.request_fields_problem(rec)})')
    if rec.get('outdir') != CH.record_outdir(rec):
        raise Refuse('RUN_RECORD', f'{side} 런 {nm} 폴더 {rec.get("outdir")!r} ≠ 생산자 이름 {CH.record_outdir(rec)!r}')
    req = {k: rec.get(k) for k in CH.REQ_KEYS}
    idx = CH.arm_indices(req)
    kind, kwhy = CH.arms_read_kind(rec.get('arms_read'), rec)
    sst = (seen or {}).get('status')
    if kind == 'empty':
        if sst in ('ok', 'not_computed'):
            raise Refuse('REPLAY_MISMATCH', f'{side} 런 {nm}: 판독 기록 {sst} 인데 팔 기록이 비었다')
        why = f'{side} 런 {nm} 판독 전 멈춤 · 팔 없음 (rc {rec.get("rc")!r} · 그룹 원인 {rec.get("group_cause")!r})'
        return {i: {'state': ARM_NC, 'rec': None, 'why': why} for i in idx}
    if kind not in ('verified', 'file_ids'):
        raise Refuse('RUN_RECORD', f'{side} 런 {nm} arms_read = {kind} ({kwhy})')
    if not CH.rc_success(rec.get('rc')) or [x.get('index') for x in rec['arms_read']] != idx:
        raise Refuse('RUN_RECORD', f'{side} 런 {nm}: rc {rec.get("rc")!r} · 팔 파일 {[x.get("index") for x in rec["arms_read"]]} ≠ 요청 팔 {idx}')
    try:
        with expect_sdcp_sigma(CH, sdcp):
            recs = CH.read_run(Path(base) / rec['outdir'], req, plan, contract, sid_reg, want_sha=[x['sha256'] for x in rec['arms_read']],
                               s0_grid=s0_grid, s0_census=s0_census)
    except CH.Stop as e:
        if e.code != 'NOT_COMPUTED':
            raise _stop(CH, e, f'{side} 런 {nm} 다시 읽기 (사슬 read_run · 비교 거부)')
        sp = (seen or {}).get('stop') if isinstance((seen or {}).get('stop'), dict) else {}
        if kind == 'verified' or (seen is not None and (sst != 'not_computed' or (sp.get('code'), sp.get('reason')) != (e.code, e.reason))):
            raise Refuse('REPLAY_MISMATCH', f'{side} 런 {nm}: 판독 기록 ({kind} · {sst} · {sp.get("code")} · {sp.get("reason")}) ≠ 다시 읽기 '
                                            f'({e.code} · {e.reason})')
        st = stop_state(CH, e)
        m = _STOP_ARM_RE.match(e.cause or '')
        j = int(m.group(1)) if m and int(m.group(1)) in idx else None
        out = {}
        for i in idx:
            if j is None or i == j:
                out[i] = {'state': st, 'rec': None, 'why': f'{side} {e.code}' + (f' ({e.reason})' if e.reason else '') + f' — {e.cause[:200]}'}
            else:
                out[i] = {'state': ARM_NC, 'rec': None, 'why': f'{side} 런 {nm} 판독이 a{j} 에서 멈춤 (사슬 read_run 은 첫 멈춤에서 선다 · 이 팔은 읽지 않았다)'}
        return out
    if kind == 'file_ids' or (seen is not None and sst != 'ok'):
        raise Refuse('REPLAY_MISMATCH', f'{side} 런 {nm}: 판독 기록 ({kind} · {sst}) = 판독 실패 · 다시 읽기 = 성공')
    out = {}
    for r in recs:
        i = r.get('index')
        if r.get('state') == 'positive':
            out[i] = {'state': ARM_POS, 'rec': r, 'why': None}
        elif r.get('state') == 'zero':
            out[i] = {'state': ARM_CUT, 'rec': r, 'why': None, 'zero': zero_confirm(CH, base, rec, r, side)}
        else:
            raise Refuse('ARM_STATE', f'{side} 런 {nm} a{i}: 사슬 기록 상태 {r.get("state")!r}')
    if sorted(out) != idx:
        raise Refuse('RUN_RECORD', f'{side} 런 {nm}: 판독 팔 {sorted(out)} ≠ 요청 팔 {idx}')
    return out


def _side_view(CH, where, e):
    """팔 한 쪽 → {'state', 'band' (사슬 arm_band · 계산됨만), 'why'[, 'zero', 'sid_fp']} — 상태 이름 ↔ 사슬 기록 상태가 어긋나면 거부."""
    st, r = e.get('state'), e.get('rec')
    if st in COMPUTED:
        want = 'positive' if st == ARM_POS else 'zero'
        if not isinstance(r, dict) or r.get('state') != want:
            raise Refuse('ARM_STATE', f'{where}: 상태 {st} ↔ 사슬 기록 상태 {r.get("state") if isinstance(r, dict) else r!r}')
        out = {'state': st, 'band': _call(CH, f'{where} 띠 (사슬 arm_band)', CH.arm_band, r), 'why': e.get('why'), 'sid_fp': r.get('sid_fp')}
        if e.get('zero') is not None:
            out['zero'] = e['zero']
        return out
    if st in (ARM_FAIL, ARM_NC):
        return {'state': st, 'band': None, 'why': e.get('why')}
    raise Refuse('ARM_STATE', f'{where}: 상태 {st!r}')


def mono_row(CH, nm, i, d, m):
    """팔 하나 판정 — 결손 = MISSING (사유 · 비교 안 함) · 위반 = 사슬 r_monotone_problem (순서 = SDCP 셀 저항: DBE 유한 < ① ∞ · 모순 = σ_lo(①) > σ_hi(DBE)) ·
    점값 σ(①) > σ(DBE) 인데 구간 겹침 = MONO_UNDETERMINED · 그 밖 PASS (PATH_CUT 0 포함)."""
    ds, ms = _side_view(CH, f'{nm} a{i} DBE', d), _side_view(CH, f'{nm} a{i} ①', m)
    missing = {k: s['state'] for k, s in (('dbe', ds), ('arm1', ms)) if s['state'] not in COMPUTED} or None
    if missing:
        verdict = V_MISS
    elif CH.r_monotone_problem([(0, 'DBE', ds['band']), (1, 'arm1', ms['band'])]) is not None:
        verdict = V_VIOL
    elif Fraction(m['rec']['sigma']) > Fraction(d['rec']['sigma']):
        verdict = V_UNDET
    else:
        verdict = V_PASS
    return {'run': nm, 'arm': i, 'verdict': verdict, 'missing': missing, 'dbe': ds, 'arm1': ms}


def mono_compare(CH, dbe, a1):
    """{런 이름: {'role', 'idx', 'arms': {팔 번호: 팔 칸}}} 둘 (DBE · ①) → 팔마다 판정 줄 [{'run', 'arm', 'verdict', 'missing', 'dbe', 'arm1'}] (런 이름 · 팔 순)."""
    if sorted(dbe) != sorted(a1):
        raise Refuse('RUN_SET', f'런 {sorted(a1)} ≠ R 단위 {sorted(dbe)}')
    rows = []
    for nm in sorted(dbe):
        d, m = dbe[nm], a1[nm]
        idx = list(d.get('idx') or [])
        if d.get('role') != m.get('role') or idx != list(m.get('idx') or []) or sorted(d.get('arms') or {}) != idx or sorted(m.get('arms') or {}) != idx:
            raise Refuse('RUN_SET', f'런 {nm}: 역할 · 팔 번호가 다르다')
        for i in idx:
            rows.append(mono_row(CH, nm, i, d['arms'][i], m['arms'][i]))
    return rows


def mono_overall(rows):
    """판정 줄 → (전체, 셈) — 위반 하나라도 = MONO_VIOLATION · 다 PASS = PASS · 비교된 팔 없음 = NO_COMPARISON · 그 밖 = NO_VIOLATION."""
    cnt = {k: sum(1 for r in rows if r['verdict'] == k) for k in (V_PASS, V_UNDET, V_VIOL, V_MISS)}
    if cnt[V_VIOL]:
        return V_VIOL, cnt
    if rows and cnt[V_PASS] == len(rows):
        return 'PASS', cnt
    if cnt[V_PASS] + cnt[V_UNDET] == 0:
        return 'NO_COMPARISON', cnt
    return 'NO_VIOLATION', cnt


def record_path(x):
    """칸 기록 자리 — 새 파일 · 리포 밖 (σ 띠 = 값 · 등록 §5) → 경로.  거부 (쓰기 전): 이 실행기의 리포 (HERE 의 부모) 안 · 다른 git 작업 트리 안 (조상 폴더에
    .git — 봉인 체크아웃 · 리포 사본에 값이 들어가 커밋되지 않게) · 있는 파일."""
    rp = _path(x).resolve()
    repo = HERE.parent.resolve()
    if rp == repo or repo in rp.parents:
        raise Refuse('RECORD_IN_REPO', f'{rp} — 칸 기록에는 σ 띠 (값) 가 실린다 · 리포 밖에 둘 것 ({RECORD_SEAL})')
    git = next((p for p in rp.parents if os.path.lexists(str(p / '.git'))), None)
    if git is not None:
        raise Refuse('RECORD_IN_REPO', f'{rp} — git 작업 트리 {git} 안 · 칸 기록 (σ 띠 = 값) 은 git 밖에 둘 것 ({RECORD_SEAL})')
    if os.path.lexists(str(rp)):
        raise Refuse('RECORD_EXISTS', f'{rp} 가 이미 있다 — 칸 기록은 새 파일')
    return rp


def _band_json(b):
    if b is None:
        return None
    return {'lo': float(b[0]), 'hi': float(b[1]), 'lo_exact': str(b[0]), 'hi_exact': str(b[1])}


def _side_json(s):
    out = {'state': s['state'], 'band': _band_json(s.get('band')), 'why': s.get('why')}
    for k in ('zero', 'sid_fp'):
        if k in s:
            out[k] = s[k]
    return out


def write_record(CH, rp, head, rows=None, overall=None, counts=None, refused=None):
    obj = dict(head, tool=TOOL, schema=MONO_SCHEMA, rule=MONO_RULE, label=MONO_LABEL, value_seal=RECORD_SEAL, utc=_utc(), chain_sha256=chain_sha(CH),
               pairing=({'ok': True} if refused is None else {'ok': False, 'code': refused.code, 'why': refused.why}),
               arms=[{'run': r['run'], 'arm': r['arm'], 'verdict': r['verdict'], 'missing': r['missing'], 'dbe': _side_json(r['dbe']),
                      'arm1': _side_json(r['arm1'])} for r in (rows or [])],
               overall=('REFUSED' if refused is not None else overall), counts=counts)
    rp.parent.mkdir(parents=True, exist_ok=True)
    CH.write_json_atomic(rp, CH._clean(obj))


def _verdict_text(r):
    if r['verdict'] != V_MISS:
        return r['verdict']
    return 'MISSING — ' + ' · '.join(f'{_SIDE[k]} {v}' for k, v in r['missing'].items())


def cmd_check_mono(a):
    CH = load_chain()
    rp = record_path(a.record)
    head = {'unit': None, 'law': None, 'rj': None, 'dbe_dir': str(_path(a.dbe).resolve()), 'arm1_dir': str(_path(a.arm1).resolve()),
            'dbe_summary_sha256': None, 'arm1_manifest_sha256': None}
    try:
        su, su_sha = read_unit_summary(CH, a.dbe)
        head.update(unit=(su.get('unit') or {}).get('name'), law=(su.get('unit') or {}).get('law'), dbe_summary_sha256=su_sha)
        man, man_sha = read_manifest(CH, a.arm1)
        head.update(rj=man.get('rj'), arm1_manifest_sha256=man_sha)
        why = pair_problem(CH, su, man)
        if why:
            raise Refuse('PAIR_MISMATCH', f'arm 1 런 ↔ R 단위 {head["unit"]}: {why}')
        plan = su['plan']['content']
        s0reps = su.get('s0_reports')
        s0_grid, s0_census = CH.s0_grid_seed(s0reps), CH.s0_census_seed(s0reps)
        sid_reg = {}                               # DBE 와 arm 1 이 같이 쓴다 — 같은 킷 · 래스터 · origin 의 sid 지문이 다르면 SID_GRID (격자 · 경계 같음)
        contract = CH.RealContract()
        stop_run = (su.get('stop') or {}).get('run') if su.get('status') == 'NOT_COMPUTED' else None
        dbe, a1 = {}, {}
        for r in su.get('runs') or []:
            seen = ({'status': 'not_computed', 'stop': su.get('stop')} if r.get('name') == stop_run else {'status': 'ok'})
            dbe[r['name']] = {'role': r.get('role'), 'idx': CH.arm_indices({k: r.get(k) for k in CH.REQ_KEYS}),
                              'arms': run_arms(CH, _path(a.dbe), r, plan, contract, sid_reg, s0_grid, s0_census, 'DBE', seen=seen)}
        for r in man.get('runs') or []:
            seen = r.get('read') if isinstance(r.get('read'), dict) else {'status': None}
            a1[r['name']] = {'role': r.get('role'), 'idx': CH.arm_indices({k: r.get(k) for k in CH.REQ_KEYS}),
                             'arms': run_arms(CH, _path(a.arm1), r, plan, contract, sid_reg, s0_grid, s0_census, '①', sdcp=ARM1_SIGMA_SDCP, seen=seen)}
            if r['name'] not in dbe:                # 봉인 R 단위 NOT_COMPUTED — 멈춘 런 뒤 런 = 그 단위에 없다 (결손)
                dbe[r['name']] = {'role': r.get('role'), 'idx': a1[r['name']]['idx'],
                                  'arms': {i: {'state': ARM_NC, 'rec': None, 'why': f'DBE 봉인 R 단위에 런 {r["name"]} 기록이 없다 (단위 NOT_COMPUTED · '
                                                                                    f'{stop_run} 에서 멈춤)'} for i in a1[r['name']]['idx']}}
        rows = mono_compare(CH, dbe, a1)
    except Refuse as e:
        write_record(CH, rp, head, refused=e)
        raise
    ov, cnt = mono_overall(rows)
    write_record(CH, rp, head, rows, ov, cnt)
    say(f'check-mono {head["unit"]} — {MONO_LABEL} · σ_e(①) ≤ σ_e(DBE) (두 런 증서 띠 · 등록 개정 1) · 칸 기록 → {rp}')
    for r in rows:
        say(f'  {r["run"]} arm {r["arm"]}: {_verdict_text(r)}')
    if ov == 'PASS':
        say(f'overall: PASS ({cnt[V_PASS]}/{len(rows)})')
    else:
        say(f'overall: {ov} (' + ' · '.join(f'{k} {v}' for k, v in cnt.items()) + ')'
            + (' — 도구 결함 의심 · 멈춤 · 보고 (등록 §4)' if ov == V_VIOL else ''))
    return OVERALL_RC[ov]


# ═════════════════════════ CLI ═════════════════════════
def _parser():
    ap = argparse.ArgumentParser(description='Rint ② 부록 팔 실행기 (봉인 사슬 함수 재사용 · 등록 ' + REG_DOC + ')')
    sub = ap.add_subparsers(dest='cmd')

    def common(p, run):
        p.add_argument('--ladders', nargs='+', required=True, help='봉인 사다리 시도 폴더 둘 (P0 · P1 · ladder_summary.json)')
        p.add_argument('--plan', required=True, help='봉인 R 계획 JSON (sha256 = 사다리 계획)')
        p.add_argument('--registration', default=None, help='봉인 등록 R (사슬 load_ladders 의 계획 해시 줄 · full 읽기에 필수)')
        p.add_argument('--kit2', default=None, help='arm 2 = 새 킷 이름 (PTFE 0.5 · SDCP 0) · arm 1 = 주지 않는다')
        p.add_argument('--runner', default=None, help='러너 (기본 = 사슬 폴더의 sdcp_gain_vox015_8arm.sh)')
        p.add_argument('--cjunc-store', default=None, help='탄소 접합 원장 저장본 폴더 (사슬 Runner 와 같은 뜻 · 선택)')
        p.add_argument('--machine', default=None, required=run, help='기계 이름표 (run = 계획 allowed_machines 안)')
        if run:
            p.add_argument('--arm', type=int, choices=ARM_CHOICES, required=True)
            p.add_argument('--law', choices=('P0', 'P1'), required=True)
            p.add_argument('--root', required=True, help='킷 뿌리 = 러너 작업 폴더')
            p.add_argument('--out', required=True, help='새 출력 폴더 (있으면 거부)')
            p.add_argument('--max-hours', type=float, default=MAX_HOURS_DEFAULT, help='시간 상한 (기본 = 계획 exec_policy.max_hours)')
            p.set_defaults(ladder_check='full')
        else:
            p.add_argument('--arm', type=int, choices=ARM_CHOICES, default=None, help='한 팔만 (기본 둘)')
            p.add_argument('--law', choices=('P0', 'P1'), default=None, help='한 법칙만 (기본 둘)')
            p.add_argument('--root', default='.', help='킷 뿌리 (명령 줄 표시용)')
            p.add_argument('--out', default='<OUT>', help='run 의 --out (OUTDIR 표시용)')
            p.add_argument('--ladder-check', choices=('full', 'summary'), default='full',
                           help='full = 사슬 load_ladders (원 팔 다시 읽기 · --registration) · summary = 요약만 (dry-run 전용)')
    common(sub.add_parser('plan', help='dry-run — 칸마다 env 와 봉인 R 단위 env 차이 · 명령 (러너 없음)'), False)
    common(sub.add_parser('run', help='칸 하나 실행 (사슬 Runner · 매니페스트)'), True)
    cm = sub.add_parser('check-mono', help='arm 1 ≤ DBE (두 런 증서 띠) 팔마다 PASS · MONO_UNDETERMINED · MONO_VIOLATION · MISSING')
    cm.add_argument('--dbe', required=True, help='봉인 R 단위 시도 폴더 (unit_summary.json · <법칙>_c0_R_j0)')
    cm.add_argument('--arm1', required=True, help='arm 1 run 의 --out 폴더 (middle_arm_manifest.json)')
    cm.add_argument('--record', required=True, help='칸 기록 JSON (새 파일 · 리포 밖 — 팔마다 판정 · 결손 사유 · 두 띠 (값) · 화면에는 판정만)')
    return ap


def main(argv=None):
    ap = _parser()
    a = ap.parse_args(argv)
    if a.cmd is None:
        ap.print_help()
        return 2
    try:
        if a.cmd == 'plan':
            return cmd_plan(a)
        if a.cmd == 'run':
            return cmd_run(a)
        return cmd_check_mono(a)
    except Refuse as e:
        say(f'거부 [{e.code}] {e.why}')
        return 3


if __name__ == '__main__':
    sys.exit(main())

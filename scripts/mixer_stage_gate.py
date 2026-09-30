#!/usr/bin/env python3
"""mixer_stage_gate.py — 믹서 고-Bo **강성 축** 캠페인의 발사 단계 관문 (2026-09-30 · 코드 선행조건 2 단계 piece 1 · 5).

`dem_scripts/mixer_20260921/launch_highbo.sh` 의 새 단계 **dev-e0 · dev-rot · confirm-first · confirm-rest** 가 부른다.  결정 (정책 · 등록
코호트 · 폴더 계약 · 디스크 · 선행 기록 · 증서 · 승인) 은 여기서, 발사 (러너 · 봉인 · sbatch · scontrol) 는 런처 bash 가 한다.
옛 단계 (first · rest · all — 고-Bo LH 확장) 는 이 모듈을 쓰지 않는다 (의미 그대로).

사전등록 = docs/reviews/mixer_highbo_stiffness_prereg_20260929.md (v2.5).  구현한 문장 (인용):
  §8-2 ② "DEV-ONLY 7 런 (… ① E0 5 런 (E0_ref ×3 · E0_ref2 · E0_ref@dt/2 · 회전 없음) → 1 % 계약 · 정규화 · 완주 진단 (M 미열람 · 허용목록
         투영) → ② 통과 시에만 LC_ref · LH_ref 회전 2 런 · E0 진단 실패 시 회전 보류 … NP 프로브 = E0_ref 첫 시드를 NP 5/10/20 으로 1 h 씩
         (같은 덱 · 처리량만 · 확인 자료 전용 금지) · DEV 권한으로 확인 셀 실행 불가 (정책 dev 단계 분리 …)"
  §8-2 ④ "확인 18 런을 한 번에 제출 — 첫 holdout 시드 블록 (6 런 …) 은 즉시 · 나머지 두 시드 블록 (12 런) 은 sbatch --hold (처음부터 held …) …
         launch_policy.json 을 first-seed-block(6) → rest(12) 단계로 개정 (id · sha256 봉인) — 기존 first/rest 정책 ID 를 재사용하지 않는다."
  §8-2 ⑤ "… launch_highbo.sh rest 관문 → 통과면 관문이 scontrol release 를 낸다 (사람이 손으로 풀지 않는다 · 수동 편차는 기록) · 실패면 전체 HOLD.
         관문은 release 순간뿐 아니라 실제 시작 직전 (러너 시작 스크립트) 에 봉인 · 유효 승인 증서를 다시 대조한다.  해제 증거 = seed × arm × E
         18 칸 manifest + job ID + 덱 · 바이너리 · 도구 · policy 해시 + E0 경로 · "처음부터 held" 조회 증거 · 반례 (제출 일부 실패 · 오래된 증서 ·
         다른 seed/E · E0 누락 · release 재시도 · 대기 중 파일 변경) 셀프테스트."
  §6    "soft 진단 범위 = 7.37 % (v2.6 · 옛 5.8) … soft 범위 null 이면 확인 soft 발사 거부" · 세 상태 (기술 / 원 1 % / 권위) 분리 · arm × E × 검사 허용/거부표.
  Codex 9 차 §6-2 "DEV 목록 밖 arm/seed/단계 요청 거부; DEV 증서가 확인/rest 발사 권한으로 쓰이지 않음".

부명령 (런처가 부른다 · rc 0 = 통과):
  policy     <정책> <단계>                                  정책 v2 · 단계 인자 = 등록 코호트 (정확히) → JSON
  prepare    <단계> <OUT> --policy P                        dev-e0: NP 프로브 폴더 셋을 기준 셀 (E0_ref_s32452843) 에서 만든다 (없을 때만)
  preflight  <단계> <OUT> --policy P --np N --cohort-json J --out-json X [--e0-record R]
                                                            폴더 계약 · fresh · 덱 코호트 JSON · 디스크 추정 · (dev-rot) E0 PASS 기록 → 발사 계획 TSV
  seal-extra <OUT> <런> --preflight X                       봉인 (launch_record.json) 에 더할 필드 JSON
  manifest   <OUT> --preflight X                            (confirm-first) 18 칸 manifest · 처음부터 held 조회 → <OUT>/confirm_manifest.json
  rest-gate  <OUT> <증서 폴더> --policy P --cohort-json J    (confirm-rest) manifest · 코호트 · held 상태 · 증서 6 → 승인 12 → 풀 job id
  release-record <OUT> --ids "…" --rc N                     (confirm-rest) scontrol release 결과 · 풀린 뒤 상태 기록
  --selftest

⚠ 새 단계는 SLURM 판 전용 (§8-1 "ibb 같은 바이너리 · 같은 MPI launcher · 같은 rank 수 NP") — 런처가 강제한다.
⚠ rest-gate 는 판독기 (numpy) 를 쓴다 — numpy 가 있는 python3 에서 (ibb myenv).  나머지 부명령은 표준 라이브러리 + mixer_deck_diff 뿐.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import mixer_deck_diff as dd          # noqa: E402  이름 · 등록 코호트 · 덱 계약의 단일 출처 (표준 라이브러리만)

LAUNCH_DIR = os.path.join(ROOT, 'dem_scripts', 'mixer_20260921')
STL_REF_DIR = os.path.join(ROOT, 'dem_scripts', 'mixer_20260919')
POLICY_V1, POLICY_V2 = 'mixer_highbo_launch_policy/1', 'mixer_highbo_launch_policy/2'
LEGACY_STAGES = ('first', 'rest', 'all')
NEW_STAGES = ('dev-e0', 'dev-rot', 'confirm-first', 'confirm-rest')
STAGE_COHORT = {'dev-e0': 'dev-e0', 'dev-rot': 'dev-rot', 'confirm-first': 'confirm', 'confirm-rest': 'confirm'}
#: §6 v2.4 "soft 진단 범위 = 5.8 %" — check_contact_validity.SOFT_RANGE_PCT 와 같아야 한다 (셀프테스트가 대조 · 이 파일은 numpy 없이 돈다)
SOFT_RANGE_PCT = 7.37   # ★ v2.6 (09-30 밤 · 1저자 비준) = 1 % × 20^(2/3) · check_contact_validity.SOFT_RANGE_PCT 와 같아야 한다
REG_N_EXPECTED = dd.GEN_ARGS['n_total']                  # gen_all.sh N_TOTAL · README §6 "n_expected (gen.log 의 N = 100,000)"
REG_R_CONTAINER = 0.013138                                # 모체 §2-3 · README §6 "r_container (0.013138)"
READER_REG = dict(cells=16, x_cells=4, n_min=20, axis='x', r_container=0.013138)   # 모체 §2-3 판독 칸 · 규약 (관문 REG 와 같다)
FILES = ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')
TIME_RE = re.compile(r'(?:([1-9][0-9]*|0)-)?([0-9]{1,2}):([0-5][0-9]):([0-5][0-9])')
DISK_MARGIN = 1.10                                        # 필요 × 1.10 ≤ 가용 이어야 발사 (piece 5 — 문서화된 거부 문턱)
FLOAT_FIELD_BYTES = 12                                    # dump custom 기본 %g 최악 폭: '-1.23457e-05'
RESTART_BYTES_PER_ATOM = 400                              # 체크포인트 a.bin · b.bin · settled.bin (보수 · 원자당)
E0_DIAG_SCHEMA = 'mixer_dev_e0_diag/1'
E0_DIAG_REG = dict(max_ovl=0.01, c_dmax_pp=0.1, c_sr2_rel=0.01, eps_pct=1e-9, eps_rel=1e-12)   # §4 a · b · c 통과선 (등록)
#: ★ v2.6 (09-30 밤 · 1저자 비준 "권고하는걸로") — 검사의 역할.  gate = verdict · dev-rot 관문에 들어감 · report = 값 · pass 를 기록만 (통과선은 그대로).
#:   b · c 가 보고 전용인 근거 = DEV7 (×14) 실측: b 는 스냅샷 최대의 **주인 교체** (+0.0026 %p) 로 깨졌고 · c 는 dt/2 가 궤적을 바꿔 두 실현을 비교한다.
E0_DIAG_ROLE = dict(complete='gate', technical='gate', a='gate', b='report', c='report')
MANIFEST_SCHEMA = 'mixer_confirm_manifest/1'
APPROVAL_SCHEMA = 'mixer_highbo_release_approval/1'
APPROVAL_FILE = 'release_approval.json'
LAUNCH_SCHEMA = 'mixer_highbo_launch_record/1'


class GateError(Exception):
    pass


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def sha_or_none(p):
    try:
        return sha_file(p)
    except OSError:
        return None


def _utc():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def _load_json(p, what):
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise GateError(f'{what} 이 없다: {p}')
    except (OSError, ValueError, UnicodeDecodeError) as e:
        raise GateError(f'{what} 을 읽을 수 없다 ({p}: {type(e).__name__}: {e})')


def _write_json_atomic(p, obj, excl=False):
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')
    if excl and os.path.exists(p):
        os.remove(tmp)
        raise GateError(f'{p} 가 이미 있다 — 덮지 않는다')
    os.replace(tmp, p)


# ══ 정책 v2 ══════════════════════════════════════════════════════════════════════════════════════════════════════
def _classify(n):
    """이름 하나의 성격 (거부 문구용) — holdout seed · DEV seed · 확인 꼬리표 · 셀 아님."""
    try:
        c_ = dd.parse_run(n)
    except ValueError:
        return f'{n} (셀 이름 아님)'
    kind = 'holdout seed' if c_['seed'] in dd.HOLDOUT_SEEDS else ('DEV seed' if c_['seed'] in dd.DEV_SEEDS else '등록 밖 seed')
    extra = ' · 확인 셀' if n in dd.COHORTS['confirm'] else (' · DEV 셀' if n in dd.COHORTS['dev-e0'] + dd.COHORTS['dev-rot'] else '')
    return f'{n} ({kind}{extra})'


def _same_list(got, want, what):
    if not isinstance(got, list) or any(not isinstance(x, str) for x in got):
        raise GateError(f'{what} 가 이름 목록이 아니다 ({got!r})')
    if list(got) != list(want):
        extra = [x for x in got if x not in want]
        miss = [x for x in want if x not in got]
        raise GateError(f'{what} ≠ 등록 코호트 — 등록 밖 {[_classify(x) for x in extra]} · 빠짐 {miss}'
                        + (' · 순서가 다르다' if not extra and not miss else '') + ' (mixer_deck_diff.COHORTS · 사전등록 §2 · §8-2)')


def _time_ok(t, what):
    if not (isinstance(t, str) and TIME_RE.fullmatch(t)):
        raise GateError(f'{what} = {t!r} — SLURM 시간 형식 (D-HH:MM:SS 또는 HH:MM:SS) 이 아니다')
    return t


def load_policy(path):
    """정책 파일 → dict.  v1 (옛 · first/rest/all 만) 과 v2 (+ 새 단계) 를 받는다.  모양이 아니면 GateError (발사 0)."""
    d = _load_json(path, '발사 정책 파일')
    if not isinstance(d, dict):
        raise GateError(f'발사 정책 파일이 JSON 객체가 아니다 ({path})')
    sc, pid, st = d.get('schema'), d.get('policy_id'), d.get('allowed_stages')
    if sc not in (POLICY_V1, POLICY_V2):
        raise GateError(f'발사 정책 스키마 {sc!r} — {POLICY_V1} · {POLICY_V2} 만')
    if not (isinstance(pid, str) and pid.strip()):
        raise GateError('발사 정책 policy_id 가 없다')
    known = LEGACY_STAGES if sc == POLICY_V1 else LEGACY_STAGES + NEW_STAGES
    if not (isinstance(st, list) and st and all(isinstance(x, str) and x in known for x in st) and len(set(st)) == len(st)):
        raise GateError(f'발사 정책 allowed_stages {st!r} — {list(known)} 의 부분집합 (중복 없이)')
    return d


def stage_params(pol, stage):
    """새 단계의 정책 인자 → dict.  **등록 코호트와 정확히 같아야** 한다 (holdout seed 를 DEV 에 · DEV 셀을 확인에 · 이름 추가/누락 = 거부).
    soft 범위 (confirm-first) 는 등록값 (v2.6 7.37) 만 — null · 다른 값이면 거부 (§6 "soft 범위 null 이면 확인 soft 발사 거부")."""
    if stage not in NEW_STAGES:
        raise GateError(f'새 단계가 아니다: {stage!r} — {list(NEW_STAGES)}')
    if pol.get('schema') != POLICY_V2:
        raise GateError(f'단계 {stage} 는 정책 v2 ({POLICY_V2}) 에서만 — 이 정책은 {pol.get("schema")!r}')
    if stage not in pol.get('allowed_stages', []):
        raise GateError(f'발사 정책 {pol.get("policy_id")} 은 stage \'{stage}\' 를 허용하지 않는다 (허용: {pol.get("allowed_stages")}) — '
                        '정책을 바꾸려면 파일을 고쳐 커밋하고 사전등록에 적는다 (봉인에 id · sha256 이 남는다)')
    try:
        dd.cohort_guard()
    except ValueError as e:
        raise GateError(str(e))
    sp = (pol.get('stages') or {}).get(stage)
    if not isinstance(sp, dict):
        raise GateError(f'발사 정책에 stages.{stage} 인자가 없다')
    out = dict(stage=stage, cohort=STAGE_COHORT[stage])
    if stage == 'dev-e0':
        _same_list(sp.get('runs'), dd.DEV_E0, 'stages.dev-e0.runs')
        npb = sp.get('np_probe')
        want = dict(base=dd.NP_PROBE['base'], nps=list(dd.NP_PROBE['nps']), time=dd.NP_PROBE['time'])
        if npb != want:
            raise GateError(f'stages.dev-e0.np_probe {npb!r} ≠ 등록 {want} (§8-2 ② "E0_ref 첫 시드를 NP 5/10/20 으로 1 h 씩")')
        out.update(runs=list(dd.DEV_E0), probes=list(dd.DEV_PROBES), np_probe=want, time=_time_ok(sp.get('time'), 'stages.dev-e0.time'))
    elif stage == 'dev-rot':
        _same_list(sp.get('runs'), dd.DEV_ROT, 'stages.dev-rot.runs')
        if sp.get('requires') != 'dev-e0':
            raise GateError('stages.dev-rot.requires ≠ "dev-e0" — 회전 2 런은 E0 진단 PASS 기록 뒤에만 (§8-2 ②)')
        out.update(runs=list(dd.DEV_ROT), requires='dev-e0', time=_time_ok(sp.get('time'), 'stages.dev-rot.time'))
    elif stage == 'confirm-first':
        _same_list(sp.get('first'), dd.CONFIRM_FIRST, 'stages.confirm-first.first')
        _same_list(sp.get('held'), dd.CONFIRM_REST, 'stages.confirm-first.held')
        sr = sp.get('soft_range_pct')
        if sr is None:
            raise GateError('stages.confirm-first.soft_range_pct 가 null — soft 진단 범위 미정이면 확인 soft 발사 거부 (§6 · Codex 9 차 Q6)')
        if isinstance(sr, bool) or not isinstance(sr, (int, float)) or float(sr) != SOFT_RANGE_PCT:
            raise GateError(f'stages.confirm-first.soft_range_pct {sr!r} ≠ 등록 {SOFT_RANGE_PCT} % (올리거나 내리지 않는다 · §6)')
        out.update(runs=list(dd.CONFIRM_FIRST) + list(dd.CONFIRM_REST), first=list(dd.CONFIRM_FIRST), held=list(dd.CONFIRM_REST),
                   soft_range_pct=SOFT_RANGE_PCT, time=_time_ok(sp.get('time'), 'stages.confirm-first.time'))
    else:
        _same_list(sp.get('release'), dd.CONFIRM_REST, 'stages.confirm-rest.release')
        out.update(runs=list(dd.CONFIRM_REST), release=list(dd.CONFIRM_REST))
    return out


def plan_rows(sp, np_main):
    """단계 → 발사 계획 [dict(name, np, time, hold, kind)] (순서 = 제출 순서)."""
    st = sp['stage']
    rows = []
    if st == 'dev-e0':
        for n, k in zip(dd.DEV_PROBES, dd.NP_PROBE['nps']):
            rows.append(dict(name=n, np=int(k), time=dd.NP_PROBE['time'], hold=0, kind='probe'))
        rows += [dict(name=n, np=int(np_main), time=sp['time'], hold=0, kind='dev') for n in dd.DEV_E0]
    elif st == 'dev-rot':
        rows = [dict(name=n, np=int(np_main), time=sp['time'], hold=0, kind='dev') for n in dd.DEV_ROT]
    elif st == 'confirm-first':
        rows = ([dict(name=n, np=int(np_main), time=sp['time'], hold=0, kind='first') for n in dd.CONFIRM_FIRST]
                + [dict(name=n, np=int(np_main), time=sp['time'], hold=1, kind='held') for n in dd.CONFIRM_REST])
    else:
        raise GateError(f'단계 {st} 는 발사 계획이 없다 (confirm-rest 는 release 만)')
    return rows


# ══ 폴더 계약 · fresh · 디스크 (piece 5) ═════════════════════════════════════════════════════════════════════════════
def folder_problems(d, name):
    """셀 폴더 계약 (README §6 "런 폴더로 옮길 때: in.mixer + STL 셋 + n_expected + r_container · 봉인은 deck_meta.json 의 deck_sha256 과 대조")
    + 덱 계약 (mixer_deck_diff.cell_deck_problems — 재생성 바이트 동일 · deck_meta)."""
    pr = []
    if not os.path.isdir(d):
        return [f'{name}: 폴더 없음 ({d})']
    for f in ('Drum.stl', 'Front.stl', 'Back.stl'):
        a, b = os.path.join(d, f), os.path.join(STL_REF_DIR, f)
        if sha_or_none(a) is None or sha_or_none(a) != sha_or_none(b):
            pr.append(f'{name}: {f} ≠ 캠페인 원본 ({STL_REF_DIR})')
    try:
        ne = int(open(os.path.join(d, 'n_expected'), encoding='utf-8').read().strip())
    except (OSError, ValueError):
        ne = None
    if ne != REG_N_EXPECTED:
        pr.append(f'{name}: n_expected {ne!r} ≠ {REG_N_EXPECTED}')
    try:
        rc = float(open(os.path.join(d, 'r_container'), encoding='utf-8').read().strip())
    except (OSError, ValueError):
        rc = None
    if rc != REG_R_CONTAINER:
        pr.append(f'{name}: r_container {rc!r} ≠ {REG_R_CONTAINER}')
    pr += dd.cell_deck_problems(d, name)[0]
    return pr


def fresh(d):
    """한 번도 안 뜬 (제출도 안 된) 런 = log.lmp · pid · jobid · job_start*.json 이 모두 없다."""
    return not any(os.path.exists(os.path.join(d, f)) for f in ('log.lmp', 'pid', 'jobid', 'job_start.json')) \
        and not glob.glob(os.path.join(glob.escape(d), 'job_start.refused.*.json'))


def disk_estimate(deck_text, n_atoms):
    """덱 → 쓸 디스크 상한 (piece 5 — E0 덤프 프레임 385 (soft) → 867 (×14) → 1,227 (×28) · 덤프 간격 1000 step 고정 규칙).
    프레임 = run 합 // 덤프 간격 (판독기 계획 격자와 같은 셈) · 프레임 바이트 = 원자 × (열별 최악 폭 + 구분자) + 머리 ·
    최악 폭: id = 원자 수 자릿수 · type ≤ 2 · mol 11 · 실수 %g 12 ('-1.23457e-05') · 체크포인트 원자당 400 B × 3 파일."""
    runs = [int(x) for x in re.findall(r'^run\s+(\d+)', deck_text, re.M)]
    m = re.search(r'^dump\s+\S+\s+all\s+custom\s+(\d+)\s+\S+\s+(.+)$', deck_text, re.M)
    if not runs or not m:
        raise GateError('덱에서 run · dump custom 을 못 읽었다 (디스크 추정 불가)')
    every, cols = int(m.group(1)), m.group(2).split('#')[0].split()
    width = {'id': len(str(int(n_atoms))), 'type': 2, 'mol': 11}
    line = sum(width.get(c, FLOAT_FIELD_BYTES) for c in cols) + len(cols)          # 구분자 (열 − 1) + 줄바꿈 1
    frames = sum(runs) // every
    fb = int(n_atoms) * line + 512
    rb = 3 * int(n_atoms) * RESTART_BYTES_PER_ATOM
    return dict(frames=frames, dump_every=every, columns=cols, line_bytes_max=line, frame_bytes_max=fb,
                dump_bytes=frames * fb, restart_bytes=rb, total_bytes=frames * fb + rb)


def df_avail(path):
    """`df -P -B1 <path>` 의 가용 바이트 (없거나 못 읽으면 None — 거부)."""
    try:
        p = subprocess.run(['df', '-P', '-B1', path], capture_output=True, text=True, timeout=60)
        if p.returncode != 0:
            return None
        return int(p.stdout.strip().split('\n')[-1].split()[3])
    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
        return None


# ══ E0 진단 PASS 기록 (dev-rot 관문 · §8-2 ②) ═════════════════════════════════════════════════════════════════════
def e0_record_tools():
    """E0 진단 기록이 봉인하는 도구 sha256 (생산자 mixer_smoke_blind · 검사기 · 판독기 · 덱 비교기) — 기록 = 지금 리포 도구여야 한다."""
    return {k: sha_or_none(os.path.join(HERE, f)) for k, f in (('smoke_blind', 'mixer_smoke_blind.py'),
                                                               ('checker', 'check_contact_validity.py'),
                                                               ('reader', 'measure_mixing_index.py'),
                                                               ('deckdiff', 'mixer_deck_diff.py'))}


def verify_e0_record(out, path, np_now):
    """dev-rot 이 여는 조건 = **봉인된 E0 진단 PASS 기록** (mixer_smoke_blind.py --e0-diag 이 쓴다) 이 지금 폴더와 이어진다 → 문제 목록.

    필수 필드: schema · verdict "PASS" · checks 다섯 (E0_DIAG_ROLE) 이 {pass: JSON bool · role} 모양 · **관문 검사 (complete · technical · a) 는 pass true** ·
    보고 검사 (b · c · v2.6) 는 값 · pass 를 기록만 · registered = E0_DIAG_REG · reader = READER_REG · runs = DEV E0 다섯 정확히 · 런마다 dir (realpath) ·
    deck · 발사 봉인 · job_start · log.lmp 의 sha256 = 지금 파일 · 봉인 stage dev-e0 · 봉인 np = 기록 np · complete · contact.status (E0_ref 셋 =
    CONTRACT_MET (§4 a) · ref2 · dt/2 = 기술적으로 관측 가능 (CONTRACT_MET · CONTRACT_NOT_MET)) · np = 지금 NP (블록 NP 통일) · tools = 지금 리포 도구
    sha256 · 봉인 파일 (vault) sha256."""
    pr = []
    try:
        rec = _load_json(path, 'E0 진단 기록')
    except GateError as e:
        return [str(e)]
    if not isinstance(rec, dict):
        return ['E0 진단 기록이 JSON 객체가 아니다']
    if rec.get('schema') != E0_DIAG_SCHEMA:
        pr.append(f'E0 진단 기록 스키마 {rec.get("schema")!r} ≠ {E0_DIAG_SCHEMA}')
    if rec.get('verdict') != 'PASS':
        pr.append(f'E0 진단 verdict = {rec.get("verdict")!r} (PASS 가 아니면 회전 보류 — §8-2 ②)')
    ch = rec.get('checks') if isinstance(rec.get('checks'), dict) else {}
    for k, role in E0_DIAG_ROLE.items():
        v = ch.get(k)
        if not (isinstance(v, dict) and isinstance(v.get('pass'), bool) and v.get('role') == role):
            pr.append(f'E0 진단 checks.{k} 가 없거나 모양이 다르다 (pass 는 JSON bool · role {role!r} 필수 · '
                      f'{json.dumps(v, ensure_ascii=False)[:80]})')
        elif role == 'gate' and v['pass'] is not True:
            pr.append(f'E0 진단 checks.{k}.pass ≠ true (관문 검사 · {json.dumps(v, ensure_ascii=False)[:80]})')
    if rec.get('registered') != E0_DIAG_REG:
        pr.append(f'E0 진단 registered {rec.get("registered")!r} ≠ 등록 {E0_DIAG_REG}')
    if rec.get('reader') != READER_REG:
        pr.append(f'E0 진단 reader 규약 {rec.get("reader")!r} ≠ 등록 {READER_REG}')
    np_r = rec.get('np')
    if not (isinstance(np_r, int) and not isinstance(np_r, bool)) or np_r != int(np_now):
        pr.append(f'E0 진단 np {np_r!r} ≠ 지금 NP {np_now} — 블록 NP 통일 (Codex 8 차 Q6 "블록 내부 NP 통일")')
    tl = rec.get('tools')
    if tl != e0_record_tools():
        pr.append('E0 진단 도구 sha256 ≠ 지금 리포 도구 (기록 뒤 도구가 바뀌었다 — 지금 도구로 다시 만든다)')
    runs = rec.get('runs') if isinstance(rec.get('runs'), dict) else {}
    if sorted(runs) != sorted(dd.DEV_E0):
        pr.append(f'E0 진단 runs {sorted(runs)} ≠ DEV E0 다섯 {sorted(dd.DEV_E0)}')
    for n in dd.DEV_E0:
        r = runs.get(n) if isinstance(runs.get(n), dict) else {}
        d = os.path.join(out, n)
        if not r:
            continue
        if os.path.realpath(str(r.get('dir'))) != os.path.realpath(d):
            pr.append(f'{n}: 기록의 dir {r.get("dir")!r} ≠ 이 OUT 의 {d}')
        for key, f in (('deck_sha256', 'in.mixer'), ('launch_record_sha256', 'launch_record.json'),
                       ('job_start_sha256', 'job_start.json'), ('log_sha256', 'log.lmp')):
            got = sha_or_none(os.path.join(d, f))
            if got is None or r.get(key) != got:
                pr.append(f'{n}: 기록의 {key} ≠ 지금 {f} (없거나 바뀜)')
        try:
            lr = json.load(open(os.path.join(d, 'launch_record.json'), encoding='utf-8'))
        except (OSError, ValueError):
            lr = {}
        if lr.get('stage') != 'dev-e0' or (lr.get('slurm') or {}).get('np') != np_r:
            pr.append(f'{n}: 발사 봉인 stage {lr.get("stage")!r} · np {(lr.get("slurm") or {}).get("np")!r} ≠ dev-e0 · {np_r!r}')
        if r.get('complete') is not True:
            pr.append(f'{n}: 완주 아님')
        st_n = (r.get('contact') or {}).get('status')
        if n in dd.DEV_E0[:3]:                                     # a (관문) — E0_ref 세 seed 는 원 1 % 계약 통과
            if st_n != 'CONTRACT_MET':
                pr.append(f'{n}: 접촉 상태 {st_n!r} ≠ CONTRACT_MET (§4 a)')
        elif st_n not in ('CONTRACT_MET', 'CONTRACT_NOT_MET'):     # ref2 · dt/2 (b · c 보고 전용 · v2.6) — 기술적으로 관측 가능해야 한다
            pr.append(f'{n}: 접촉 상태 {st_n!r} — 기술 실패 · 모르는 상태 (ref2 · dt/2 는 b · c 보고 전용이지만 technical 은 관문)')
    vt = rec.get('vault') if isinstance(rec.get('vault'), dict) else {}
    if not vt.get('file') or sha_or_none(str(vt.get('file'))) != vt.get('sha256'):
        pr.append('E0 진단 봉인 파일 (vault) 이 없거나 sha256 이 다르다')
    return pr


# ══ 증서 (confirm-rest) — mixer_smoke_blind.py 가 쓴 허용목록 투영을 **지금 폴더**에 다시 잇는다 ══════════════════════════════
def _level_of(name):
    return dd.parse_cell(name)['level']


def _sb():
    """증서 형식 · 관문표의 단일 출처 = mixer_smoke_blind (numpy) — rest-gate 에서만 늦게 불러온다."""
    import mixer_smoke_blind as sb_
    return sb_


def _seal(d):
    try:
        lr = json.load(open(os.path.join(d, 'launch_record.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return None
    return lr if isinstance(lr, dict) else None


def verify_contact(d, name, c, bins, pr):
    """증서의 contact 블록 (mixer_smoke_blind.contact_block) → 상태 문자열 (문제는 pr 에)."""
    import measure_mixing_index as mi                    # numpy — 이 관문만
    lv = _level_of(name)
    if not isinstance(c, dict) or c.get('schema') != _sb().CONTACT_CERT_SCHEMA:
        pr.append(f'{name}: contact 블록 없음 · 스키마 ≠ {_sb().CONTACT_CERT_SCHEMA}')
        return None
    lr = _seal(d) or {}
    want = dict(run=name, level=lv, bins=bins, soft_range_pct=SOFT_RANGE_PCT if lv == 'soft' else None,
                checker_sha256=sha_or_none(os.path.join(HERE, 'check_contact_validity.py')),
                deck_sha256=(lr.get('sha256') or {}).get('in.mixer'), launch_record_sha256=sha_or_none(os.path.join(d, 'launch_record.json')),
                expect_deck_sha256=hashlib.sha256(dd.cell_expected_deck(name).encode('utf-8')).hexdigest())
    off = [k for k, v in want.items() if c.get(k) != v]
    off += [f'{k} (기준 파일 없음)' for k in ('checker_sha256', 'deck_sha256', 'launch_record_sha256') if want[k] is None]
    if off:
        pr.append(f'{name}: contact 출처가 지금 폴더 · 봉인 · 도구 · 등록과 다르다 {off}')
    if sha_or_none(os.path.join(d, 'in.mixer')) != want['deck_sha256']:
        pr.append(f'{name}: in.mixer 가 발사 봉인 뒤 바뀌었다')
    bad = mi.verify_frames(os.path.join(d, 'post'), c.get('frames'))
    if not (c.get('frames') or {}).get('files') or bad:
        pr.append(f'{name}: contact 가 본 프레임을 지금 폴더에서 다시 해시하면 어긋난다 {bad[:3]}')
    st = (c.get('status') or {}).get('status') if isinstance(c.get('status'), dict) else None
    return st


def verify_rot_cert(out, name, cert, pr):
    """회전 팔 증서 (bin 0 스모크 + contact · 허용목록) → 상태 문자열."""
    import measure_mixing_index as mi
    d = os.path.join(out, name)
    c_ = dd.parse_cell(name)
    if not (isinstance(cert, list) and len(cert) == 1 and isinstance(cert[0], dict)):
        pr.append(f'{name}: 증서 모양 — [허용목록 투영 하나] 가 아니다')
        return None
    e = cert[0]
    if sorted(e) != sorted(_sb().ROT_CERT_KEYS):
        pr.append(f'{name}: 증서 키 {sorted(e)} ≠ 허용목록 {sorted(_sb().ROT_CERT_KEYS)} (M-맹검 투영만 받는다)')
        return None
    if os.path.basename(os.path.normpath(str(e.get('run')))) != name:
        pr.append(f'{name}: 증서 run = {e.get("run")!r} (다른 런 · 다른 seed/E)')
    pv = e.get('provenance') if isinstance(e.get('provenance'), dict) else {}
    lr = _seal(d) or {}
    if pv.get('schema') != 'mixing_provenance/1' or pv.get('args') != READER_REG:
        pr.append(f'{name}: 판독 출처 스키마 · 규약 {pv.get("args")!r} ≠ 등록 {READER_REG}')
    if pv.get('tool_sha256') != sha_or_none(os.path.join(HERE, 'measure_mixing_index.py')):
        pr.append(f'{name}: 판독기 sha256 ≠ 지금 리포 판독기')
    ru = pv.get('run') if isinstance(pv.get('run'), dict) else {}
    if ru.get('name') != name or ru.get('deck_sha256') != (lr.get('sha256') or {}).get('in.mixer'):
        pr.append(f'{name}: 판독 출처 run · 덱 ≠ 발사 봉인')
    if ru.get('launch_record_sha256') != sha_or_none(os.path.join(d, 'launch_record.json')):
        pr.append(f'{name}: 증서가 본 발사 봉인 sha256 ≠ 지금 봉인 (오래된 증서 · 다른 발사)')
    bad = mi.verify_frames(os.path.join(d, 'post'), ru.get('frames'))
    if bad:
        pr.append(f'{name}: 판독 프레임을 다시 해시하면 어긋난다 {bad[:3]}')
    e0 = f'E0_{c_["level"]}_s{c_["seed"]}'
    rf = pv.get('ref') if isinstance(pv.get('ref'), dict) else {}
    e0d = os.path.join(out, e0)
    if rf.get('name') != e0 or rf.get('deck_sha256') != sha_or_none(os.path.join(e0d, 'in.mixer')) \
            or mi.verify_frames(os.path.join(e0d, 'post'), rf.get('frames')):
        pr.append(f'{name}: E0 기준 ≠ {e0} (같은 seed · 같은 강성) · 덱 · 프레임')
    #  판독 계획 · t₀ 는 증서가 아니라 **덱에서** 다시 낸다 (Codex 6 차 tampered_certificate_narrows_bin0 — 증서 필드를 믿지 않는다)
    try:
        plan = mi.deck_plan(os.path.join(d, 'in.mixer'))
        t0 = mi.planned_t0(plan)
    except (OSError, ValueError, AttributeError) as ex:
        pr.append(f'{name}: 덱 계획을 못 읽었다 ({ex})')
        return None
    if e.get('t0_step') != t0 or not isinstance(e.get('plan'), dict) or any(
            e['plan'].get(k) != plan[k] for k in ('steps_per_rev', 'dump_every', 'steps_total')):
        pr.append(f'{name}: 증서 plan · t0_step ≠ 덱에서 다시 낸 값 (증서 필드를 손대면 창이 바뀐다)')
    w = mi.bin_window_files(os.path.join(d, 'post'), t0, plan['steps_per_rev'], plan['dump_every'], plan['steps_total'], (0,))
    if w['dup'] or w['off'] or w['miss']:
        pr.append(f'{name}: bin 0 창 입력 집합 — 중복 {w["dup"][:3]} · 격자 밖 {w["off"][:3]} · 결손 {w["miss"][:3]} (HBR5-02)')
    cf = sorted([int(a), os.path.basename(str(b)), str(h)] for a, b, h in (ru.get('frames') or {}).get('files') or [] if int(a) in w['lattice'])
    now = sorted([s, os.path.basename(ps[0]), sha_file(ps[0])] for s, ps in w['cur'].items() if len(ps) == 1)
    if cf != now or not now:
        pr.append(f'{name}: bin 0 파일 (step · 이름 · sha256) ≠ 증서가 판독한 파일 ({len(now)} / {len(cf)})')
    sm = e.get('smoke') if isinstance(e.get('smoke'), dict) else {}
    if not (sm.get('complete') is True and sm.get('tech_smoke') == [] and isinstance(sm.get('qc_repr'), dict)
            and sm['qc_repr'].get('pass') is True):
        pr.append(f'{name}: bin 0 스모크 기술 실패 (complete · tech_smoke · qc_repr.pass) — 수준과 무관하게 거부')
    return verify_contact(d, name, e.get('contact'), [0], pr)


def verify_e0_cert(out, name, cert, pr):
    """E0 증서 (contact · 완주) → 상태 문자열."""
    d = os.path.join(out, name)
    if not (isinstance(cert, list) and len(cert) == 1 and isinstance(cert[0], dict)):
        pr.append(f'{name}: 증서 모양 — [E0 계약 증서 하나] 가 아니다')
        return None
    e = cert[0]
    if sorted(e) != sorted(_sb().E0_CERT_KEYS) or e.get('kind') != _sb().E0_CERT_KIND:
        pr.append(f'{name}: E0 증서 키 {sorted(e)} · kind {e.get("kind")!r} ≠ 허용목록 {sorted(_sb().E0_CERT_KEYS)} · {_sb().E0_CERT_KIND}')
        return None
    if e.get('run') != name:
        pr.append(f'{name}: E0 증서 run = {e.get("run")!r}')
    cp = e.get('completion') if isinstance(e.get('completion'), dict) else {}
    tot = sum(int(x) for x in re.findall(r'^run\s+(\d+)', open(os.path.join(d, 'in.mixer'), encoding='utf-8').read(), re.M))
    if not (cp.get('complete') is True and cp.get('basis') == 'last_step' and cp.get('run_total') == tot
            and cp.get('log_sha256') == sha_or_none(os.path.join(d, 'log.lmp'))):
        pr.append(f'{name}: E0 완주 (log 마지막 thermo step = run 합 {tot}) · log sha256 = 지금 파일 이 아니다')
    return verify_contact(d, name, e.get('contact'), None, pr)


# ══ confirm-first manifest · confirm-rest 관문 · 승인 ══════════════════════════════════════════════════════════════
def squeue_states(ids):
    """squeue -h -j <ids> -o %i|%T|%r → {id: (상태, 사유)} · 원문."""
    if not ids:
        return {}, ''
    try:
        p = subprocess.run(['squeue', '-h', '-j', ','.join(ids), '-o', '%i|%T|%r'], capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return {}, f'(squeue 실패: {e})'
    st = {}
    for ln in p.stdout.splitlines():
        parts = ln.strip().split('|')
        if len(parts) == 3:
            st[parts[0]] = (parts[1], parts[2])
    return st, p.stdout


def _is_held(sr):
    return bool(sr) and sr[0] == 'PENDING' and sr[1] in ('JobHeldUser', 'JobHeldAdmin')


def tool_shas():
    fs = dict(launcher=os.path.join(LAUNCH_DIR, 'launch_highbo.sh'), start_check=os.path.join(LAUNCH_DIR, 'start_check.py'),
              stage_gate=os.path.abspath(__file__), deckdiff=os.path.join(HERE, 'mixer_deck_diff.py'),
              reader=os.path.join(HERE, 'measure_mixing_index.py'), checker=os.path.join(HERE, 'check_contact_validity.py'),
              smoke_blind=os.path.join(HERE, 'mixer_smoke_blind.py'))
    return {k: sha_or_none(v) for k, v in fs.items()}


def write_manifest(out, pre_path):
    """confirm-first 제출 뒤 — seed × arm × E 18 칸 manifest (job ID · 덱 · 봉인 · E0 경로 · 도구 · 정책 해시 · 처음부터 held 조회)."""
    pre = _load_json(pre_path, 'preflight 기록')
    cells, ids_held, ids_first = [], [], []
    for r in pre['rows']:
        d = os.path.join(out, r['name'])
        c_ = dd.parse_cell(r['name'])
        jid = open(os.path.join(d, 'jobid'), encoding='utf-8').read().strip() if os.path.isfile(os.path.join(d, 'jobid')) else None
        lr = _seal(d)
        cells.append(dict(run=r['name'], seed=c_['seed'], arm=c_['arm'], level=c_['level'], block=r['kind'], jobid=jid,
                          launch_record_sha256=sha_or_none(os.path.join(d, 'launch_record.json')) if jid else None,
                          deck_sha256=((lr or {}).get('sha256') or {}).get('in.mixer') if jid else None,
                          lmp_sha256=(lr or {}).get('lmp_sha256') if jid else None,
                          e0=os.path.realpath(os.path.join(out, f'E0_{c_["level"]}_s{c_["seed"]}'))))
        if jid:
            (ids_held if r['hold'] else ids_first).append(jid)
    st, raw = squeue_states(ids_held + ids_first)
    held_ok = len(ids_held) == 12 and all(_is_held(st.get(i)) for i in ids_held) and all(
        st.get(i) is None or not _is_held(st.get(i)) for i in ids_first)
    complete = len(cells) == 18 and all(c['jobid'] and c['launch_record_sha256'] for c in cells)
    man = dict(schema=MANIFEST_SCHEMA, time_utc=_utc(), out=os.path.realpath(out), policy=pre['policy'], np=pre['np'],
               soft_range_pct=SOFT_RANGE_PCT, preflight=dict(path=os.path.realpath(pre_path), sha256=sha_file(pre_path)),
               cells=cells, complete=bool(complete), failed_at=next((c['run'] for c in cells if not c['jobid']), None),
               held_query=dict(cmd=f'squeue -h -j {",".join(ids_held + ids_first)} -o %i|%T|%r', output=raw,
                               per_job={k: list(v) for k, v in st.items()}, held_ok=bool(held_ok)),
               tools=tool_shas())
    p = os.path.join(out, 'confirm_manifest.json')
    if os.path.exists(p):
        os.replace(p, os.path.join(out, f'confirm_manifest.superseded.{_utc()}.json'))
    _write_json_atomic(p, man)
    return man


def approval_record(out, name, man_path, certs, pol_path):
    """held 런 하나의 승인 증서 — 시작 대조 (start_check.py approval_problems) 가 job 시작 직전에 다시 본다."""
    d = os.path.join(out, name)
    return dict(schema=APPROVAL_SCHEMA, run=name, stage='confirm-rest', verdict='PASS',
                launch_record_sha256=sha_file(os.path.join(d, 'launch_record.json')),
                manifest=dict(path=os.path.realpath(man_path), sha256=sha_file(man_path)),
                certificates=[dict(run=n, path=os.path.realpath(p), sha256=sha_file(p)) for n, p in certs],
                policy=dict(path=os.path.realpath(pol_path), sha256=sha_file(pol_path)),
                gate_tool_sha256=sha_file(os.path.abspath(__file__)))


def rest_gate(out, certdir, pol_path, cohort_json):
    """confirm-rest 관문 → (문제 목록, 풀 job id 목록).  통과면 held 12 런에 승인 증서를 쓴다 (이미 있으면 같은지 대조 — 다르면 거부)."""
    pr = []
    man_path = os.path.join(out, 'confirm_manifest.json')
    try:
        man = _load_json(man_path, 'confirm manifest')
    except GateError as e:
        return [str(e)], []
    if man.get('schema') != MANIFEST_SCHEMA or man.get('complete') is not True:
        pr.append(f'manifest 가 완전하지 않다 (schema {man.get("schema")!r} · complete {man.get("complete")!r} · 실패 {man.get("failed_at")!r}) — '
                  '제출 일부 실패는 사람이 판단 (rest 해제 없음)')
    if (man.get('held_query') or {}).get('held_ok') is not True:
        pr.append('manifest 의 "처음부터 held" 조회 증거가 서지 않았다 (held_ok ≠ true)')
    pol_sha = sha_or_none(pol_path)
    if (man.get('policy') or {}).get('sha256') != pol_sha:
        pr.append('정책 파일 sha256 ≠ confirm-first 때 (캠페인 중 정책이 바뀌었다)')
    cells = {c.get('run'): c for c in man.get('cells') or [] if isinstance(c, dict)}
    if sorted(cells) != sorted(dd.COHORTS['confirm']):
        pr.append(f'manifest 칸 {len(cells)} ≠ 등록 18')
    try:
        cj = _load_json(cohort_json, '덱 코호트 JSON')
        if cj.get('cohort') != 'confirm' or cj.get('verdict') != 'PASS':
            pr.append(f'덱 코호트 (confirm) ≠ PASS ({cj.get("verdict")!r})')
    except GateError as e:
        pr.append(str(e))
    held = list(dd.CONFIRM_REST)
    held_ids = []
    st, _raw = squeue_states([str((cells.get(n) or {}).get('jobid')) for n in held if (cells.get(n) or {}).get('jobid')])
    for n in dd.COHORTS['confirm']:
        c = cells.get(n) or {}
        d = os.path.join(out, n)
        if not c.get('launch_record_sha256') or sha_or_none(os.path.join(d, 'launch_record.json')) != c.get('launch_record_sha256'):
            pr.append(f'{n}: 발사 봉인이 manifest 때와 다르다 (다시 봉인됐거나 없음)')
        lr = _seal(d) or {}
        for f in FILES:
            if sha_or_none(os.path.join(d, f)) != (lr.get('sha256') or {}).get(f):
                pr.append(f'{n}: {f} 가 봉인 뒤 바뀌었다 (대기 중 파일 변경)')
    for n in held:
        c = cells.get(n) or {}
        d = os.path.join(out, n)
        jid = str(c.get('jobid'))
        try:
            jf = open(os.path.join(d, 'jobid'), encoding='utf-8').read().strip()
        except OSError:
            jf = None
        if jf != jid:
            pr.append(f'{n}: jobid 파일 {jf!r} ≠ manifest {jid!r}')
        started = (any(os.path.exists(os.path.join(d, f)) for f in ('log.lmp', 'job_start.json'))
                   or bool(glob.glob(os.path.join(glob.escape(d), 'job_start.refused.*.json'))))
        if os.path.isfile(os.path.join(d, APPROVAL_FILE)):
            #  앞선 confirm-rest 가 승인했다 (release 재시도) — 승인 내용은 아래에서 같은지 대조 · 아직 held 면 다시 풀 대상 · 풀렸으면 정상 (시작했어도)
            if _is_held(st.get(jid)):
                held_ids.append(jid)
            continue
        if started:
            pr.append(f'{n}: 승인 없이 이미 시작됐다 (log · job_start) — 관문 없이 풀렸다 (수동 release 편차) · 사람이 판단')
        elif not _is_held(st.get(jid)):
            pr.append(f'{n}: job {jid} 가 held 가 아니다 ({st.get(jid)}) — 관문 없이 풀렸다 (수동 편차 기록) · 사람이 판단')
        else:
            held_ids.append(jid)
    certs = []
    for n in dd.CONFIRM_FIRST:
        cp = os.path.join(certdir, f'{n}.json')
        try:
            cert = _load_json(cp, f'{n} 증서')
        except GateError as e:
            pr.append(str(e) + ' (E0 누락 · 증서 누락)')
            continue
        sub = []
        stt = (verify_e0_cert if n.startswith('E0_') else verify_rot_cert)(out, n, cert, sub)
        pr += sub
        ok, why = _sb().gate_decision(_level_of(n), stt)
        if not ok:
            pr.append(f'{n}: 상태 {stt} → 거부 ({why})')
        certs.append((n, cp))
    if pr:
        return pr, []
    for n in held:
        ap = approval_record(out, n, man_path, certs, pol_path)
        p = os.path.join(out, n, APPROVAL_FILE)
        if os.path.exists(p):
            old = _load_json(p, f'{n} 승인 증서')
            if {k: v for k, v in old.items() if k != 'time_utc'} != ap:
                pr.append(f'{n}: 승인 증서가 이미 있고 지금 관문의 것과 다르다 (다른 증서 · 봉인) — 덮지 않는다 · 사람이 판단')
            continue
        _write_json_atomic(p, dict(ap, time_utc=_utc()), excl=True)
    return pr, (held_ids if not pr else [])


def release_record(out, ids, rc):
    st, raw = squeue_states(ids)
    p = os.path.join(out, 'confirm_release.jsonl')
    with open(p, 'a', encoding='utf-8') as f:
        f.write(json.dumps(dict(time_utc=_utc(), ids=ids, scontrol_rc=int(rc), after=dict(output=raw, per_job={k: list(v) for k, v in st.items()}),
                                still_held=[i for i in ids if _is_held(st.get(i))]), ensure_ascii=False) + '\n')
    return [i for i in ids if _is_held(st.get(i))]


# ══ 부명령 ════════════════════════════════════════════════════════════════════════════════════════════════════════
def cmd_policy(a):
    pol = load_policy(a.policy_file)
    print(json.dumps(stage_params(pol, a.stage), ensure_ascii=False))
    return 0


def cmd_prepare(a):
    pol = load_policy(a.policy)
    sp = stage_params(pol, a.stage)
    if a.stage != 'dev-e0':
        return 0
    base = os.path.join(a.out, dd.NP_PROBE['base'])
    for n in dd.DEV_PROBES:
        d = os.path.join(a.out, n)
        if os.path.exists(d):
            continue
        if not os.path.isfile(os.path.join(base, 'in.mixer')):
            raise GateError(f'NP 프로브 기준 셀 {base} 에 in.mixer 가 없다')
        os.makedirs(d)
        for f in FILES + ('n_expected', 'r_container', 'deck_meta.json'):
            if os.path.isfile(os.path.join(base, f)):
                shutil.copy2(os.path.join(base, f), os.path.join(d, f))
        print(f'   NP 프로브 폴더 {n} ← {dd.NP_PROBE["base"]} (같은 덱 · 처리량만)')
    return 0 if sp else 1


def cmd_preflight(a):
    pol = load_policy(a.policy)
    sp = stage_params(pol, a.stage)
    rows = plan_rows(sp, a.np)
    pr = []
    try:
        cj = _load_json(a.cohort_json, '덱 코호트 JSON (mixer_deck_diff --cohort --json)')
    except GateError as e:
        cj = {}
        pr.append(str(e))
    if cj and (cj.get('cohort') != sp['cohort'] or cj.get('verdict') != 'PASS'):
        pr.append(f'덱 코호트 {cj.get("cohort")!r} · {cj.get("verdict")!r} ≠ {sp["cohort"]} · PASS')
    tot, per = 0, {}
    for r in rows:
        d = os.path.join(a.out, r['name'])
        pr += folder_problems(d, r['name'])
        if not fresh(d):
            pr.append(f'{r["name"]}: 이미 log.lmp / pid / jobid / job_start 가 있다 — 새 단계는 모든 런이 아직 안 떴을 때만 (재개 없음 · §8-1 fresh)')
        info = (cj.get('dirs') or {}).get(r['name']) or {}
        r['expected_sha256'] = info.get('expected_sha256')
        if r['expected_sha256'] is None or info.get('problems'):
            pr.append(f'{r["name"]}: 덱 코호트 JSON 에 이 셀이 없거나 문제가 있다')
        try:
            est = disk_estimate(open(os.path.join(d, 'in.mixer'), encoding='utf-8').read(), REG_N_EXPECTED)
        except (OSError, GateError) as e:
            est = None
            pr.append(f'{r["name"]}: 디스크 추정 불가 ({e})')
        r['disk'] = est
        per[r['name']] = est
        tot += est['total_bytes'] if est else 0
    avail = df_avail(a.out)
    need = int(math.ceil(tot * DISK_MARGIN))
    disk = dict(required_bytes=tot, margin=DISK_MARGIN, required_with_margin=need, available_bytes=avail,
                ok=bool(avail is not None and need <= avail), rule='필요 × 1.10 ≤ df 가용 (df -P -B1 <OUT>) — 아니면 발사 0',
                frames={n: (e or {}).get('frames') for n, e in per.items()})
    if not disk['ok']:
        pr.append(f'디스크: 필요 {tot / 1e9:.2f} GB × {DISK_MARGIN} = {need / 1e9:.2f} GB > 가용 '
                  f'{"미상" if avail is None else f"{avail / 1e9:.2f} GB"} — 발사 0 (프레임 {disk["frames"]})')
    e0rec = None
    if a.stage == 'dev-rot':
        if not a.e0_record:
            pr.append('dev-rot 은 E0 진단 PASS 기록 경로가 필요하다 (launch_highbo.sh dev-rot <기록>)')
        else:
            pr += verify_e0_record(a.out, a.e0_record, a.np)
            e0rec = dict(path=os.path.realpath(a.e0_record), sha256=sha_or_none(a.e0_record))
    pre = dict(schema='mixer_stage_preflight/1', stage=a.stage, time_utc=_utc(), out=os.path.realpath(a.out), np=int(a.np),
               policy=dict(path=os.path.realpath(a.policy), sha256=sha_file(a.policy), policy_id=pol.get('policy_id')),
               params=sp, rows=rows, disk=disk, e0_record=e0rec,
               cohort_json=dict(path=os.path.realpath(a.cohort_json), sha256=sha_or_none(a.cohort_json)),
               problems=pr, verdict='PASS' if not pr else 'FAIL', tools=tool_shas())
    _write_json_atomic(a.out_json, pre)
    for r in rows:
        print(f'{r["name"]}\t{r["np"]}\t{r["time"]}\t{r["hold"]}\t{r["kind"]}')
    if pr:
        sys.stderr.write('⛔ 새 단계 관문 (preflight) 불합격 — 발사 0\n' + ''.join(f'   ✗ {p}\n' for p in pr))
        return 1
    sys.stderr.write(f'   ✓ preflight {a.stage}: {len(rows)} 런 · 디스크 필요 {tot / 1e9:.2f} GB (×{DISK_MARGIN}) ≤ 가용 {avail / 1e9:.2f} GB · '
                     f'기록 {a.out_json}\n')
    return 0


def cmd_seal_extra(a):
    pre = _load_json(a.preflight, 'preflight 기록')
    if pre.get('verdict') != 'PASS':
        raise GateError('preflight 가 PASS 가 아니다 — 봉인하지 않는다')
    row = next((r for r in pre['rows'] if r['name'] == a.run), None)
    if row is None:
        raise GateError(f'{a.run} 은 이 단계 ({pre["stage"]}) 의 발사 계획에 없다')
    c_ = dd.parse_run(a.run)
    ex = dict(stage_gate=dict(tool=os.path.abspath(__file__), tool_sha256=sha_file(os.path.abspath(__file__)), stage=pre['stage'],
                              preflight=dict(path=os.path.realpath(a.preflight), sha256=sha_file(a.preflight))),
              gate_deckdiff=dict(script=os.path.realpath(dd.__file__), script_sha256=sha_file(dd.__file__),
                                 argv=['--runs', pre['out'], '--cohort', pre['params']['cohort']], cohort_json=pre['cohort_json'],
                                 expect_deck_sha256=row['expected_sha256'], expect_deck_source=f'mixer_deck_diff.cell_expected_deck({a.run!r})', rc=0),
              cell={k: c_[k] for k in ('name', 'arm', 'level', 'stiffen_se', 'hold_bo_pairwise', 'dt_factor', 'revolutions', 'seed', 'probe_np')},
              manifest=dict(stage=pre['stage'], runs=[r['name'] for r in pre['rows']]), block=row['kind'], np_block=pre['np'],
              disk_estimate=row['disk'])
    if row['kind'] == 'probe':
        ex['probe'] = dict(np=row['np'], time=row['time'], purpose='NP 프로브 — 처리량만 · 확인 자료 · E0 진단 전용 금지 (§8-2 ②)')
    if pre['stage'] == 'dev-rot':
        ex['requires'] = [dict(kind='dev_e0_diag', path=pre['e0_record']['path'], sha256=pre['e0_record']['sha256'])]
    if row['hold']:
        ex['approval'] = dict(file=APPROVAL_FILE, schema=APPROVAL_SCHEMA, gate='launch_highbo.sh confirm-rest')
    if pre['stage'].startswith('confirm'):
        ex['soft_range_pct'] = SOFT_RANGE_PCT
    print(json.dumps(ex, ensure_ascii=False))
    return 0


def cmd_manifest(a):
    man = write_manifest(a.out, a.preflight)
    print(f'   manifest → {os.path.join(a.out, "confirm_manifest.json")} · 완전 {man["complete"]} · 처음부터 held {man["held_query"]["held_ok"]}')
    return 0 if man['complete'] and man['held_query']['held_ok'] else 1


def cmd_rest_gate(a):
    pol = load_policy(a.policy)
    stage_params(pol, 'confirm-rest')
    pr, ids = rest_gate(a.out, a.certdir, a.policy, a.cohort_json)
    if pr:
        sys.stderr.write('⛔ confirm-rest 관문 불합격 — release 0 (전체 HOLD)\n' + ''.join(f'   ✗ {p}\n' for p in pr))
        return 1
    print(' '.join(ids))
    return 0


def cmd_release_record(a):
    ids = a.ids.split()
    left = release_record(a.out, ids, a.rc)
    if a.rc != 0 or left:
        sys.stderr.write(f'⚠ release 미완 — scontrol rc {a.rc} · 아직 held {left} (다시 launch_highbo.sh confirm-rest — 승인 증서는 같으면 그대로 쓴다)\n')
        return 1
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='믹서 강성 축 발사 단계 관문 (launch_highbo.sh 새 단계)')
    ap.add_argument('--selftest', action='store_true')
    sub = ap.add_subparsers(dest='cmd')
    p = sub.add_parser('policy')
    p.add_argument('policy_file')
    p.add_argument('stage')
    p = sub.add_parser('prepare')
    p.add_argument('stage')
    p.add_argument('out')
    p.add_argument('--policy', required=True)
    p = sub.add_parser('preflight')
    p.add_argument('stage')
    p.add_argument('out')
    p.add_argument('--policy', required=True)
    p.add_argument('--np', type=int, required=True)
    p.add_argument('--cohort-json', required=True)
    p.add_argument('--out-json', required=True)
    p.add_argument('--e0-record', default=None)
    p = sub.add_parser('seal-extra')
    p.add_argument('out')
    p.add_argument('run')
    p.add_argument('--preflight', required=True)
    p = sub.add_parser('manifest')
    p.add_argument('out')
    p.add_argument('--preflight', required=True)
    p = sub.add_parser('rest-gate')
    p.add_argument('out')
    p.add_argument('certdir')
    p.add_argument('--policy', required=True)
    p.add_argument('--cohort-json', required=True)
    p = sub.add_parser('release-record')
    p.add_argument('out')
    p.add_argument('--ids', required=True)
    p.add_argument('--rc', type=int, required=True)
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    fn = dict(policy=cmd_policy, prepare=cmd_prepare, preflight=cmd_preflight, **{'seal-extra': cmd_seal_extra}, manifest=cmd_manifest,
              **{'rest-gate': cmd_rest_gate, 'release-record': cmd_release_record}).get(a.cmd)
    if fn is None:
        ap.print_help()
        return 2
    try:
        return fn(a)
    except GateError as e:
        sys.stderr.write(f'⛔ {e} — 발사 0\n')
        return 2


# ══ 합성 고정물 (셀프테스트 · dem_scripts/mixer_20260921/test_launcher.sh 전용 — 실제 런에 쓰지 않는다) ══════════════════════════════
def _fx_cell(out, name):
    """셀 폴더 = 이름에서 재생성한 등록 덱 · 캠페인 STL · n_expected · r_container · (경화 · dt 셀) 생성기 deck_meta.json (README §6 계약 그대로)."""
    c_ = dd.parse_run(name)
    d = os.path.join(out, name)
    os.makedirs(d, exist_ok=True)
    t = dd.cell_expected_deck(name)
    with open(os.path.join(d, 'in.mixer'), 'w', encoding='utf-8') as f:
        f.write(t)
    for f_ in ('Drum.stl', 'Front.stl', 'Back.stl'):
        shutil.copyfile(os.path.join(STL_REF_DIR, f_), os.path.join(d, f_))
    with open(os.path.join(d, 'n_expected'), 'w', encoding='utf-8') as f:
        f.write(f'{REG_N_EXPECTED}\n')
    with open(os.path.join(d, 'r_container'), 'w', encoding='utf-8') as f:
        f.write(f'{REG_R_CONTAINER:.6f}\n')
    if c_['stiffen_se'] != 1.0 or c_['dt_factor'] != 1.0:
        g = dd._gen
        p = g.plan(dd.GEN_ARGS['n_total'], cgf=dd.GEN_ARGS['cgf'], stiffen_se=c_['stiffen_se'])
        rpm = g.resolve_rpm(p['R'], g.FR_ANCHOR, None, False)
        with open(os.path.join(d, 'deck_meta.json'), 'w', encoding='utf-8') as f:
            json.dump(g.deck_meta(p, rpm, c_['revolutions'], c_['seed'], c_['arm'], t, argv=['(fixture)'],
                                  hold_bo_pairwise=c_['hold_bo_pairwise'], dt_factor=c_['dt_factor']), f, ensure_ascii=False)
    return d


def _fx_seal(out, name, stage, np_=20, **extra):
    """발사 봉인 흉내 (핵심 필드 · slurm) — 이 파일의 셀프테스트 전용 (test_launcher 는 런처의 진짜 봉인을 쓴다)."""
    d = os.path.join(out, name)
    rec = dict(schema=LAUNCH_SCHEMA, run=name, seed=int(name.rsplit('_s', 1)[1]), stage=stage, backend='slurm',
               lmp_sha256='a' * 64, lmp_realpath='/x/lmp_mpi', sha256={f: sha_file(os.path.join(d, f)) for f in FILES},
               slurm=dict(np=np_, runner='run_lh.sbatch', runner_sha256='b' * 64, start_check_sha256='c' * 64))
    rec.update(extra)
    _write_json_atomic(os.path.join(d, 'launch_record.json'), rec)
    return rec


def _fx_rot_frames(out, name):
    """회전 셀 bin 0 계획 격자에 합성 덤프 (내용 = 이름 · step — 판독하지 않는다 · 출처 해시만)."""
    import measure_mixing_index as mi
    d = os.path.join(out, name)
    os.makedirs(os.path.join(d, 'post'), exist_ok=True)
    pl = mi.deck_plan(os.path.join(d, 'in.mixer'))
    t0 = mi.planned_t0(pl)
    lat = mi.bin_window_files(os.path.join(d, 'post'), t0, pl['steps_per_rev'], pl['dump_every'], pl['steps_total'], (0,))['lattice']
    for s_ in sorted(lat):
        with open(os.path.join(d, 'post', f'mix_{s_}.liggghts'), 'w', encoding='utf-8') as f:
            f.write(f'fixture {name} {s_}\n')
    return sorted(lat)


def _fx_e0_done(out, name):
    """E0 셀 = 계획 t₀ 합성 덤프 + 완주 로그 (마지막 thermo step = run 합 — log_completion 의 규칙)."""
    import measure_mixing_index as mi
    d = os.path.join(out, name)
    os.makedirs(os.path.join(d, 'post'), exist_ok=True)
    pl = mi.deck_plan(os.path.join(d, 'in.mixer'))
    t0 = mi.planned_t0(pl)
    with open(os.path.join(d, 'post', f'mix_{t0}.liggghts'), 'w', encoding='utf-8') as f:
        f.write(f'fixture {name} {t0}\n')
    with open(os.path.join(d, 'log.lmp'), 'w', encoding='utf-8') as f:
        f.write(f'LIGGGHTS (fixture)\n   Step Atoms KinEng c_rke Volume\n{t0:12d} 100000 0 0 0\n{pl["steps_total"]:12d} 100000 0 0 0\n')
    return t0


def _fx_fake_analyse(run_dir, ref_dir, r_container, cells=8, x_cells=2, n_min=20, axis='x'):
    """판독기 대역 — 출처 블록은 **진짜** (provenance_block · 지금 폴더의 bin 0 파일) · 값은 합성 (증서 생산 · 관문 시험용)."""
    import measure_mixing_index as mi
    pl = mi.deck_plan(os.path.join(run_dir, 'in.mixer'))
    t0 = mi.planned_t0(pl)
    w = mi.bin_window_files(os.path.join(run_dir, 'post'), t0, pl['steps_per_rev'], pl['dump_every'], pl['steps_total'], (0,))
    used = sorted((s_, ps[0]) for s_, ps in w['cur'].items())
    rpl = mi.deck_plan(os.path.join(ref_dir, 'in.mixer'))
    rt0 = mi.planned_t0(rpl)
    prov = mi.provenance_block(run_dir, ref_dir, dict(cells=int(cells), x_cells=int(x_cells), n_min=int(n_min), axis=str(axis),
                                                      r_container=float(r_container)),
                               used, [(rt0, os.path.join(ref_dir, 'post', f'mix_{rt0}.liggghts'))])
    return dict(run=run_dir, ref=ref_dir, provenance=prov, plan=pl, t0_step=t0, S0=0.1, SR=0.01, M_final=0.5,
                smoke=dict(bin=0, complete=True, tech_smoke=[], qc_repr={'pass': True}, M_mean=0.3), interim=None)


def _fx_fake_cw(status_of, x_pct=None):
    """검사기 대역 — 본 프레임 = 지금 폴더 (회전 = bins 창 · E0 = 계획 t₀) · 상태 = status_of(이름)."""
    def f(run_dir, n_expected=None, bins=None, soft_range_pct=None, **kw):
        import measure_mixing_index as mi
        name = os.path.basename(os.path.normpath(run_dir))
        st_ = status_of(name)
        pl = mi.deck_plan(os.path.join(run_dir, 'in.mixer'))
        t0 = mi.planned_t0(pl)
        if bins is not None:
            w = mi.bin_window_files(os.path.join(run_dir, 'post'), t0, pl['steps_per_rev'], pl['dump_every'], pl['steps_total'], bins)
            fr = sorted((s_, ps[0]) for s_, ps in w['cur'].items())
        else:
            fr = [(t0, os.path.join(run_dir, 'post', f'mix_{t0}.liggghts'))]
        xp = (x_pct or {}).get(name, {'CONTRACT_MET': 0.8, 'CONTRACT_NOT_MET': 4.0, 'OUT_OF_RANGE': 7.0}.get(st_, 2.0))
        status = dict(schema='mixer_contact_status/1', status=st_, technical='FAIL' if st_ == 'TECH_FAIL' else 'OK',
                      original_1pct=None if st_ == 'TECH_FAIL' else ('MET' if st_ == 'CONTRACT_MET' else 'NOT_MET'),
                      soft_range=(None if soft_range_pct is None else ('OUT_OF_RANGE' if st_ == 'OUT_OF_RANGE' else 'WITHIN')),
                      soft_range_pct=soft_range_pct, x_lo_pct=xp, x_hi_pct=xp, why=[], max_ovl=0.01, soft_range_eps=1e-9,
                      wall_basis='static')
        return dict(verdict='PASS' if st_ == 'CONTRACT_MET' else ('TECH' if st_ == 'TECH_FAIL' else 'REJECT'), status=status,
                    bins=sorted(bins) if bins is not None else None, window=(fr[0][0], fr[-1][0]), n_frames=len(fr),
                    phase_status='static' if bins is None else 'receipt', frames_evaluated=[[int(a), b] for a, b in fr], tech=[], reject=[])
    return f


def _fx_default_status(n):
    return 'CONTRACT_MET' if dd.parse_cell(n)['level'] != 'soft' else 'CONTRACT_NOT_MET'


def _fx_certs(out, certdir, status=None, names=None):
    """확인 첫 seed 6 셀의 증서를 **진짜 생산자** (mixer_smoke_blind.run_contract_cert) 로 만든다 — 판독기 · 검사기만 대역 (값 합성 · 출처 진짜)."""
    import contextlib
    import io
    sb = _sb()
    real_a, real_c = sb.mi.analyse, sb.cv.check_window
    st = dict(status or {})
    sb.mi.analyse = _fx_fake_analyse
    sb.cv.check_window = _fx_fake_cw(lambda n: st.get(n, _fx_default_status(n)))
    os.makedirs(certdir, exist_ok=True)
    try:
        for n in (names or dd.CONFIRM_FIRST):
            c_ = dd.parse_cell(n)
            ref = os.path.join(out, f'E0_{c_["level"]}_s{c_["seed"]}') if c_['arm'] != 'E0' else None
            with contextlib.redirect_stdout(io.StringIO()):
                rc, s_ = sb.run_contract_cert(os.path.join(out, n), ref, os.path.join(certdir, f'{n}.json'))
            if rc != 0:
                raise GateError(f'고정물 증서 실패 {n}: {s_}')
    finally:
        sb.mi.analyse, sb.cv.check_window = real_a, real_c


def _fx_e0_record(out, record, x_pct=None, s2=None, status=None):
    """DEV E0 다섯의 진단 기록을 **진짜 생산자** (mixer_smoke_blind.e0_diag) 로 — 검사기 · S_R² 만 대역 (status = 이름 → 상태 덮어쓰기)."""
    import contextlib
    import io
    sb = _sb()
    real_c, real_s = sb.cv.check_window, sb.mi.e0_t0_stats
    xs, st_over = dict(x_pct or {}), dict(status or {})
    sb.cv.check_window = _fx_fake_cw(lambda n: st_over.get(n) or ('CONTRACT_MET' if xs.get(n, 0.8) <= 1.0 else 'CONTRACT_NOT_MET'), x_pct=xs)
    s2v = dict(s2 or {})

    def fake_s(ref_dir, r_container, **kw):
        import measure_mixing_index as mi
        n = os.path.basename(os.path.normpath(ref_dir))
        pl = mi.deck_plan(os.path.join(ref_dir, 'in.mixer'))
        t0 = mi.planned_t0(pl)
        return t0, os.path.join(ref_dir, 'post', f'mix_{t0}.liggghts'), dict(s2=s2v.get(n, 0.0100))
    sb.mi.e0_t0_stats = fake_s
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            rc, rec = sb.e0_diag(out, record)
    finally:
        sb.cv.check_window, sb.mi.e0_t0_stats = real_c, real_s
    return rc, rec


def _fx_start_check():
    """시작 대조기 (dem_scripts/mixer_20260921/start_check.py — 표준 라이브러리 · job 안에서 돈다) 를 모듈로."""
    import importlib.util
    sp = importlib.util.spec_from_file_location('mixer_start_check', os.path.join(LAUNCH_DIR, 'start_check.py'))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


# ══ 셀프테스트 ══════════════════════════════════════════════════════════════════════════════════════════════════════
def selftest():
    import contextlib
    import copy
    import io
    import tempfile
    fails, n_ok = [], [0]

    def chk(name, cond):
        print(('  ✓ ' if cond else '  ✗ ') + name)
        if cond:
            n_ok[0] += 1
        else:
            fails.append(name)

    def okx(fn):
        try:
            return bool(fn())
        except Exception as e:                                                    # noqa: BLE001
            print(f'        ({type(e).__name__}: {str(e)[:160]})')
            return False

    def refuses(fn, *need):
        try:
            fn()
        except GateError as e:
            ok_ = all(w in str(e) for w in need)
            if not ok_:
                print(f'        (거부 문구: {str(e)[:160]})')
            return ok_
        return False

    repo_pol = os.path.join(LAUNCH_DIR, 'launch_policy.json')

    def pol_v2(**over):
        p = copy.deepcopy(load_policy(repo_pol))
        p['allowed_stages'] = list(dict.fromkeys(p['allowed_stages'] + ['confirm-first', 'confirm-rest']))
        for k, v in over.items():
            st_, key = k.split('__')
            p['stages'][st_.replace('_', '-')][key] = v
        return p

    #  S① 정책 — 리포 정책 = v2 · 새 policy_id · dev 두 단계 허용 · 확인 두 단계는 정의만 (허용 아님) · 옛 first · rest 그대로
    def _s1():
        p = load_policy(repo_pol)
        return (p['schema'] == POLICY_V2 and p['policy_id'] != 'Q8-2026-09-29-first-smoke-rest'
                and set(p['allowed_stages']) == {'first', 'rest', 'dev-e0', 'dev-rot'}
                and stage_params(p, 'dev-e0')['runs'] == list(dd.DEV_E0) and stage_params(p, 'dev-rot')['requires'] == 'dev-e0'
                and refuses(lambda: stage_params(p, 'confirm-first'), '허용하지 않는다')
                and refuses(lambda: stage_params(p, 'confirm-rest'), '허용하지 않는다')
                and stage_params(pol_v2(), 'confirm-first')['soft_range_pct'] == 7.37)
    chk('S① 리포 정책 = v2 · 새 policy_id (옛 Q8 first/rest id 재사용 안 함 §8-2 ④) · dev-e0 · dev-rot 허용 · confirm-first/rest 는 정의만 (Codex GO 전 거부) · '
        '옛 first · rest 는 허용 그대로', okx(_s1))

    #  S② DEV 단계는 확인 셀 · holdout seed 를 못 받는다 / 확인 단계는 DEV 덱을 못 받는다 / soft 범위 null · 다른 값 거부
    def _s2():
        p = pol_v2()
        bad = []
        c1 = copy.deepcopy(p)
        c1['stages']['dev-e0']['runs'] = list(dd.DEV_E0) + ['E0_ref_s15485863']
        bad.append(refuses(lambda: stage_params(c1, 'dev-e0'), 'holdout seed'))
        c2 = copy.deepcopy(p)
        c2['stages']['dev-rot']['runs'] = ['LC_ref_r8_s15485863', 'LH_ref_r2_s32452843']
        bad.append(refuses(lambda: stage_params(c2, 'dev-rot'), '확인 셀'))
        c3 = copy.deepcopy(p)
        c3['stages']['confirm-first']['first'] = list(dd.CONFIRM_FIRST[:-1]) + ['LC_ref_r2_s32452843']
        bad.append(refuses(lambda: stage_params(c3, 'confirm-first'), 'DEV'))
        c4 = copy.deepcopy(p)
        c4['stages']['confirm-first']['soft_range_pct'] = None
        bad.append(refuses(lambda: stage_params(c4, 'confirm-first'), 'null'))
        c5 = copy.deepcopy(p)
        c5['stages']['confirm-first']['soft_range_pct'] = 6.0
        bad.append(refuses(lambda: stage_params(c5, 'confirm-first'), f'{SOFT_RANGE_PCT:g}'))
        c6 = copy.deepcopy(p)
        c6['stages']['dev-e0']['np_probe'] = dict(base='E0_ref_s32452843', nps=[5, 10, 20, 40], time='01:00:00')
        bad.append(refuses(lambda: stage_params(c6, 'dev-e0'), 'np_probe'))
        c7 = copy.deepcopy(p)
        c7['stages']['confirm-rest']['release'] = list(dd.CONFIRM_REST[1:])
        bad.append(refuses(lambda: stage_params(c7, 'confirm-rest'), '빠짐'))
        c8 = copy.deepcopy(p)
        c8['stages']['dev-rot']['requires'] = None
        bad.append(refuses(lambda: stage_params(c8, 'dev-rot'), 'requires'))
        c9 = copy.deepcopy(p)
        c9['stages']['dev-e0']['time'] = '1 day'
        bad.append(refuses(lambda: stage_params(c9, 'dev-e0'), 'SLURM 시간'))
        v1 = dict(schema=POLICY_V1, policy_id='x', allowed_stages=['first', 'rest'])
        bad.append(refuses(lambda: stage_params(v1, 'dev-e0'), 'v2'))
        return all(bad) and len(bad) == 10
    chk('S② ★ 요청 거부 (Codex 9 차 §6-2) — dev-e0 에 holdout seed · dev-rot 에 확인 셀 · confirm-first 에 DEV 셀 · soft 범위 null · 6.0 · 프로브 NP 추가 · '
        'release 빠짐 · requires 없음 · 시간 형식 · v1 정책의 새 단계 → 10/10 거부 (문구가 원인을 짚는다)', okx(_s2))

    #  S③ 모양 — 정책 파일 자체
    def _s3():
        with tempfile.TemporaryDirectory() as td:
            ok_ = []
            for body, need in (('{"schema": "x"}', '스키마'), ('[]', '객체'),
                               (json.dumps(dict(schema=POLICY_V1, policy_id='x', allowed_stages=['dev-e0'])), 'allowed_stages'),
                               (json.dumps(dict(schema=POLICY_V2, policy_id='', allowed_stages=['first'])), 'policy_id'),
                               (json.dumps(dict(schema=POLICY_V2, policy_id='x', allowed_stages=['first', 'first'])), 'allowed_stages')):
                pth = os.path.join(td, 'p.json')
                open(pth, 'w').write(body)
                ok_.append(refuses(lambda: load_policy(pth), need))
            ok_.append(refuses(lambda: load_policy(os.path.join(td, 'none.json')), '없다'))
            return all(ok_)
    chk('S③ 정책 파일 모양 — 스키마 · 비객체 · v1 에 새 단계 · 빈 policy_id · 중복 단계 · 파일 없음 → 거부 (fail-closed)', okx(_s3))

    #  S④ 발사 계획
    def _s4():
        e0 = plan_rows(stage_params(pol_v2(), 'dev-e0'), 20)
        rot = plan_rows(stage_params(pol_v2(), 'dev-rot'), 10)
        cf = plan_rows(stage_params(pol_v2(), 'confirm-first'), 5)
        return ([(r['name'], r['np'], r['time'], r['hold'], r['kind']) for r in e0[:3]]
                == [(f'npprobe{k}_E0_ref_s32452843', k, '01:00:00', 0, 'probe') for k in (5, 10, 20)]
                and [r['name'] for r in e0[3:]] == list(dd.DEV_E0) and all(r['np'] == 20 and r['kind'] == 'dev' for r in e0[3:])
                and [r['name'] for r in rot] == list(dd.DEV_ROT) and all(r['np'] == 10 for r in rot)
                and [r['hold'] for r in cf] == [0] * 6 + [1] * 12 and [r['name'] for r in cf[:6]] == list(dd.CONFIRM_FIRST)
                and all(r['np'] == 5 for r in cf) and len({r['time'] for r in cf}) == 1
                and refuses(lambda: plan_rows(stage_params(pol_v2(), 'confirm-rest'), 5), 'release'))
    chk('S④ 발사 계획 — dev-e0 = NP 프로브 셋 (5 · 10 · 20 · 1 h · 처리량만) 먼저 + E0 다섯 (환경 NP) · dev-rot 둘 · confirm-first = 첫 seed 6 즉시 + '
        '나머지 12 held (한 NP · 한 시간) · confirm-rest 는 발사 계획 없음 (release 만)', okx(_s4))

    #  S⑤ 디스크 (piece 5) — E0 프레임 385 → 867 (×14) → 1,227 (×28) · dt/2 867
    def _s5():
        e = {n: disk_estimate(dd.cell_expected_deck(n), REG_N_EXPECTED)
             for n in ('E0_soft_s32452843', 'E0_ref_s32452843', 'E0_ref2_s32452843', 'E0_ref_dthalf_s32452843', 'LC_ref_r2_s32452843',
                       'LH_ref_r8_s15485863')}
        fr = {n: v['frames'] for n, v in e.items()}
        line = e['E0_ref_s32452843']['line_bytes_max']
        want_line = 6 + 2 + 10 * FLOAT_FIELD_BYTES + 12                         # id 6 자리 · type 2 · 실수 10 열 · 구분자 12
        return (fr['E0_soft_s32452843'] == 385 and fr['E0_ref_s32452843'] == 1037 and fr['E0_ref2_s32452843'] == 1467
                and fr['E0_ref_dthalf_s32452843'] == 1037 and line == want_line
                and e['E0_ref_s32452843']['columns'] == ['id', 'type', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy', 'fz', 'radius']
                and 1.4e10 < e['E0_ref_s32452843']['dump_bytes'] < 1.5e10 and fr['LC_ref_r2_s32452843'] > 200
                and e['E0_ref2_s32452843']['total_bytes'] > e['E0_ref_s32452843']['total_bytes'])
    chk('S⑤ ★ 디스크 추정 (piece 5 · v2.6) — E0 프레임 soft 385 → ×20 1,037 → ×40 1,467 · dt/2 1,037 (덤프 간격 1000 고정 규칙 · 옛 ×14 867 · ×28 1,227) · '
        '한 줄 최악 폭 = id 6 + type 2 + 실수 10 × 12 (%g) + 구분자 · E0_ref 한 런 ≈ 14.5 GB (필요 × 1.10 ≤ df 가용이어야 발사)', okx(_s5))

    #  S⑥ 폴더 계약 · fresh
    def _s6():
        with tempfile.TemporaryDirectory() as td:
            n = 'E0_ref_s32452843'
            d = _fx_cell(td, n)
            ok0 = folder_problems(d, n) == [] and fresh(d)
            res = {}
            open(os.path.join(d, 'Back.stl'), 'a').write('\n')
            res['stl'] = folder_problems(d, n)
            shutil.copyfile(os.path.join(STL_REF_DIR, 'Back.stl'), os.path.join(d, 'Back.stl'))
            open(os.path.join(d, 'n_expected'), 'w').write('99999\n')
            res['n'] = folder_problems(d, n)
            open(os.path.join(d, 'n_expected'), 'w').write('100000\n')
            open(os.path.join(d, 'r_container'), 'w').write('0.02\n')
            res['r'] = folder_problems(d, n)
            open(os.path.join(d, 'r_container'), 'w').write('0.013138\n')
            os.remove(os.path.join(d, 'deck_meta.json'))
            res['meta'] = folder_problems(d, n)
            open(os.path.join(d, 'jobid'), 'w').write('7\n')
            return ok0 and all(res.values()) and not fresh(d) and folder_problems(os.path.join(td, 'nope'), 'nope')
    chk('S⑥ 셀 폴더 계약 (README §6) — 재생성 덱 · 캠페인 STL · n_expected 100000 · r_container 0.013138 · 경화 셀 deck_meta → 문제 0 · STL · n · r · meta '
        '하나씩 어긋나면 문제 · jobid 있으면 fresh 아님 · 폴더 없음', okx(_s6))

    #  S⑦ E0 진단 PASS 기록 — 진짜 생산자 (mixer_smoke_blind.e0_diag · 검사기 · S_R² 대역) 가 쓴 기록을 verify_e0_record 가 잇는다
    def _dev_out(td):
        for n in dd.DEV_E0:
            _fx_cell(td, n)
            _fx_seal(td, n, 'dev-e0', 20)
            _fx_e0_done(td, n)
            open(os.path.join(td, n, 'job_start.json'), 'w').write('{"schema": "mixer_highbo_job_start/1", "ok": true}\n')
        return td

    def _s7():
        with tempfile.TemporaryDirectory() as td:
            _dev_out(td)
            rp = os.path.join(td, 'dev_e0_diag.json')
            rc, rec = _fx_e0_record(td, rp)
            p0 = verify_e0_record(td, rp, 20)
            if rc != 0 or p0:
                print(f'        rc {rc} · {p0[:3]} · checks {rec.get("checks")}')
                return False
            res = {}
            res['np'] = verify_e0_record(td, rp, 10)
            j = json.load(open(rp))
            j2 = copy.deepcopy(j)
            j2['checks']['c']['pass'] = 'true'
            open(rp + '.b', 'w').write(json.dumps(j2))
            res['str_true'] = verify_e0_record(td, rp + '.b', 20)
            j3 = copy.deepcopy(j)
            j3['runs'].pop('E0_ref2_s32452843')
            open(rp + '.c', 'w').write(json.dumps(j3))
            res['runs'] = verify_e0_record(td, rp + '.c', 20)
            j4 = copy.deepcopy(j)
            j4['tools']['checker'] = '0' * 64
            open(rp + '.d', 'w').write(json.dumps(j4))
            res['tools'] = verify_e0_record(td, rp + '.d', 20)
            lg = os.path.join(td, 'E0_ref_s49979687', 'log.lmp')
            keep = open(lg).read()
            open(lg, 'a').write('# 기록 뒤 바뀜\n')
            res['log'] = verify_e0_record(td, rp, 20)
            open(lg, 'w').write(keep)
            _fx_seal(td, 'E0_ref_s67867967', 'first', 20)
            res['seal'] = verify_e0_record(td, rp, 20)
            _fx_seal(td, 'E0_ref_s67867967', 'dev-e0', 20)
            #  ★ v2.6 (09-30 밤 · 1저자 비준 "권고하는걸로") — b · c 는 **보고 전용** (값 · pass 는 기록 · 관문 아님 · 통과선 불변).  반례 먼저: 옛 판은
            #    DEV7 실측 모양 (b = 최대 주인 교체 +0.0026 %p · c = 두 실현의 |Δx| 0.24 %p · S_R² 10 %) 으로 a 가 통과해도 회전을 막았다.
            rc2, rec2 = _fx_e0_record(td, rp + '.f', x_pct={'E0_ref2_s32452843': 0.95, 'E0_ref_s32452843': 0.6})    # b: ref2 > ref (증가)
            res['b_report'] = (rc2 == 0 and rec2.get('verdict') == 'PASS' and rec2['checks']['b']['pass'] is False
                               and rec2['checks']['b'].get('role') == 'report' and verify_e0_record(td, rp + '.f', 20) == [])
            rc3, rec3 = _fx_e0_record(td, rp + '.g', s2={'E0_ref_s32452843': 0.0100, 'E0_ref_dthalf_s32452843': 0.0102})   # c: S_R² 2 %
            res['c_report'] = (rc3 == 0 and rec3.get('verdict') == 'PASS' and rec3['checks']['c']['pass'] is False
                               and rec3['checks']['c'].get('role') == 'report' and verify_e0_record(td, rp + '.g', 20) == [])
            rc5, rec5 = _fx_e0_record(td, rp + '.i', x_pct={'E0_ref_s32452843': 0.7319, 'E0_ref2_s32452843': 0.7345,
                                                           'E0_ref_dthalf_s32452843': 0.9725},
                                      s2={'E0_ref_s32452843': 0.0100, 'E0_ref_dthalf_s32452843': 0.0110})             # DEV7 모양 · a 통과
            res['dev7_shape'] = (rc5 == 0 and rec5.get('verdict') == 'PASS' and rec5['checks']['b']['pass'] is False
                                 and rec5['checks']['c']['pass'] is False and verify_e0_record(td, rp + '.i', 20) == [])
            rc6, rec6 = _fx_e0_record(td, rp + '.j', x_pct={'E0_ref2_s32452843': 1.3})        # ref2 1 % 초과 = b 보고 (기술 실패 아님)
            res['ref2_notmet_report'] = rc6 == 0 and verify_e0_record(td, rp + '.j', 20) == []
            rc7, rec7 = _fx_e0_record(td, rp + '.k', status={'E0_ref2_s32452843': 'TECH_FAIL'})  # ref2 기술 실패 = technical → FAIL
            res['ref2_tech'] = (rc7 != 0 and rec7['checks']['technical']['pass'] is False and verify_e0_record(td, rp + '.k', 20) != [])
            j5 = copy.deepcopy(j)
            j5['checks'].pop('b')
            open(rp + '.l', 'w').write(json.dumps(j5))
            res['b_missing'] = verify_e0_record(td, rp + '.l', 20)                            # 보고 필드가 빠진 기록 = 불완전 → 거부
            rc4, rec4 = _fx_e0_record(td, rp + '.h', x_pct={'E0_ref_s49979687': 1.2})                                # a: 1 % 초과
            res['a'] = [] if rc4 == 0 else ['a 실패'] if rec4['checks']['a']['pass'] is False else []
            res['fail_verdict'] = verify_e0_record(td, rp + '.h', 20)
            print('        ' + ' · '.join(f'{k}:{v if isinstance(v, bool) else len(v)}' for k, v in res.items()))
            return all(res.values()) and rec['verdict'] == 'PASS' and rec['np'] == 20
    chk('S⑦ ★ E0 진단 PASS 기록 (dev-rot 관문) — 진짜 생산자가 쓴 PASS 기록은 이어진다 · 반례 전부 거부: 다른 NP (블록 통일) · pass 가 "true" 문자열 · '
        'runs 빠짐 · 도구 sha 다름 · 기록 뒤 log 변경 · 봉인 stage ≠ dev-e0 · a (1 % 초과) · ref2 기술 실패 · b 보고 필드 누락 → 거부 / '
        '★ v2.6: b (ref2 > ref) · c (S_R² 2 %) · DEV7 모양 (b · c 동시) · ref2 1 % 초과는 **보고 전용** (pass false · role report 로 기록 · PASS)',
        okx(_s7))

    #  S⑧ 승인 증서 ↔ 시작 대조 (start_check.approval_problems) — 같은 형식 (쓰는 쪽 = 이 모듈 · 읽는 쪽 = job 안의 표준 라이브러리)
    def _s8():
        sc = _fx_start_check()
        with tempfile.TemporaryDirectory() as td:
            n = 'LC_ref_r8_s86028121'
            _fx_cell(td, n)
            _fx_seal(td, n, 'confirm-first', 5, approval=dict(file=APPROVAL_FILE, schema=APPROVAL_SCHEMA))
            man, pol, cert = (os.path.join(td, x) for x in ('confirm_manifest.json', 'pol.json', 'c.json'))
            for p_ in (man, pol, cert):
                open(p_, 'w').write('{}\n')
            ap = approval_record(td, n, man, [('LC_ref_r8_s15485863', cert)], pol)
            d = os.path.join(td, n)
            _write_json_atomic(os.path.join(d, APPROVAL_FILE), dict(ap, time_utc=_utc()))
            spec = json.load(open(os.path.join(d, 'launch_record.json')))['approval']
            lp = os.path.join(d, 'launch_record.json')
            ok0 = sc.approval_problems(d, lp, spec) == [] and sc.seal_problems(json.load(open(lp))) == []
            res = {}
            open(cert, 'w').write('{"바뀜": 1}\n')
            res['cert'] = sc.approval_problems(d, lp, spec)
            open(cert, 'w').write('{}\n')
            _fx_seal(td, n, 'confirm-first', 5, approval=dict(file=APPROVAL_FILE, schema=APPROVAL_SCHEMA), note='다시 봉인')
            res['reseal'] = sc.approval_problems(d, lp, spec)
            _fx_seal(td, n, 'confirm-first', 5, approval=dict(file=APPROVAL_FILE, schema=APPROVAL_SCHEMA))
            os.remove(os.path.join(d, APPROVAL_FILE))
            res['none'] = sc.approval_problems(d, lp, spec)
            bad = json.load(open(lp))
            bad['approval'] = dict(file='x.json', schema=APPROVAL_SCHEMA)
            res['shape'] = sc.seal_problems(bad)
            bad['approval'] = dict(file=APPROVAL_FILE, schema=APPROVAL_SCHEMA)
            bad['requires'] = [dict(kind='dev_e0_diag', path='rel/path.json', sha256='f' * 64)]
            res['req_shape'] = sc.seal_problems(bad)
            return ok0 and all(res.values()) and sc.APPROVAL_SCHEMA == APPROVAL_SCHEMA and sc.APPROVAL_FILE == APPROVAL_FILE
    chk('S⑧ ★ 승인 증서 ↔ 시작 대조 (§8-2 ⑤ "실제 시작 직전 … 유효 승인 증서를 다시 대조") — 이 모듈이 쓴 승인을 start_check 가 받는다 · 승인 뒤 증서 변경 · '
        '다시 봉인 · 승인 없음 (수동 release) · 봉인 approval · requires 모양 틀림 → 거부 · 두 파일의 스키마 문자열이 같다', okx(_s8))

    #  S⑨ confirm-rest 관문 — 진짜 생산자 증서 · 합성 manifest · squeue 대역
    def _confirm_out(td, held_state=('PENDING', 'JobHeldUser')):
        for i, n in enumerate(dd.COHORTS['confirm']):
            _fx_cell(td, n)
            held = n in dd.CONFIRM_REST
            _fx_seal(td, n, 'confirm-first', 5, **({'approval': dict(file=APPROVAL_FILE, schema=APPROVAL_SCHEMA)} if held else {}))
            open(os.path.join(td, n, 'jobid'), 'w').write(f'{900 + i}\n')
        for n in dd.CONFIRM_FIRST:
            if n.startswith('E0_'):
                _fx_e0_done(td, n)
            else:
                _fx_rot_frames(td, n)
        pre = dict(rows=[dict(name=r['name'], hold=r['hold'], kind=r['kind']) for r in plan_rows(stage_params(pol_v2(), 'confirm-first'), 5)],
                   policy=dict(path=os.path.join(td, 'pol.json'), sha256=None), np=5)
        pol = os.path.join(td, 'pol.json')
        open(pol, 'w').write(json.dumps(pol_v2()))
        pre['policy']['sha256'] = sha_file(pol)
        pp = os.path.join(td, 'pre.json')
        _write_json_atomic(pp, pre)
        return pp, pol

    def _states_for(td, held_state):
        ids = {open(os.path.join(td, n, 'jobid')).read().strip(): n for n in dd.COHORTS['confirm']}

        def f(q):
            return ({i: (held_state if ids.get(i) in dd.CONFIRM_REST else ('RUNNING', 'None')) for i in q if i in ids}, 'fake')
        return f

    def _s9():
        global squeue_states
        real_sq = squeue_states
        res = {}
        try:
            with tempfile.TemporaryDirectory() as td:
                pp, pol = _confirm_out(td)
                squeue_states = _states_for(td, ('PENDING', 'JobHeldUser'))
                man = write_manifest(td, pp)
                cj = os.path.join(td, 'cohort.json')
                json.dump(dd.check_cohort(td, 'confirm'), open(cj, 'w'))
                certs = os.path.join(td, 'certs')
                _fx_certs(td, certs)
                pr, ids = rest_gate(td, certs, pol, cj)
                ok0 = (man['complete'] and man['held_query']['held_ok'] and not pr and len(ids) == 12
                       and all(os.path.isfile(os.path.join(td, n, APPROVAL_FILE)) for n in dd.CONFIRM_REST))
                if not ok0:
                    print(f'        정상 경로 실패: {pr[:4]} · ids {len(ids)}')
                sc = _fx_start_check()
                n0 = dd.CONFIRM_REST[0]
                ok_sc = sc.approval_problems(os.path.join(td, n0), os.path.join(td, n0, 'launch_record.json'),
                                             dict(file=APPROVAL_FILE, schema=APPROVAL_SCHEMA)) == []
                pr2, ids2 = rest_gate(td, certs, pol, cj)                               # release 재시도 — 승인 같으면 그대로 · 다시 풀 대상
                res['retry_ok'] = ['ok'] if (not pr2 and len(ids2) == 12) else []

                def mut(label, fn, undo, need):
                    fn()
                    try:
                        for n_ in dd.CONFIRM_REST:                                    # 앞선 승인이 있으면 '같은가' 대조가 섞이므로 지운다
                            p_ = os.path.join(td, n_, APPROVAL_FILE)
                            if os.path.exists(p_):
                                os.remove(p_)
                        pr_, ids_ = rest_gate(td, certs, pol, cj)
                        res[label] = pr_ if (pr_ and not ids_ and any(need in x for x in pr_)) else []
                        if not res[label]:
                            print(f'        반례 {label} 이 안 걸렸다: {pr_[:3]}')
                    finally:
                        undo()
                c0 = os.path.join(certs, 'LC_ref_r8_s15485863.json')
                keep = open(c0).read()
                #  오래된 증서 — 첫 seed 런이 증서 뒤 다시 봉인됐다
                lp0 = os.path.join(td, 'LC_ref_r8_s15485863', 'launch_record.json')
                keep_lp = open(lp0).read()
                mut('stale', lambda: _fx_seal(td, 'LC_ref_r8_s15485863', 'confirm-first', 5, note='다시'),
                    lambda: open(lp0, 'w').write(keep_lp), '오래된 증서')
                #  다른 seed/E — 두 번째 seed 의 셀 이름을 가진 증서로 바꿔치기
                mut('other', lambda: open(c0, 'w').write(keep.replace('LC_ref_r8_s15485863', 'LC_ref_r8_s86028121')),
                    lambda: open(c0, 'w').write(keep), '다른 런')
                #  E0 누락
                e0c = os.path.join(certs, 'E0_ref_s15485863.json')
                keep_e0 = open(e0c).read()
                mut('e0_missing', lambda: os.remove(e0c), lambda: open(e0c, 'w').write(keep_e0), 'E0 누락')
                #  soft 기술 실패 · ref 1 % 미달 (증서를 진짜 생산자로 다시)
                mut('soft_tech', lambda: _fx_certs(td, certs, status={'LH_soft_r8_s15485863': 'TECH_FAIL'}, names=['LH_soft_r8_s15485863']),
                    lambda: _fx_certs(td, certs, names=['LH_soft_r8_s15485863']), 'TECH_FAIL')
                mut('ref_notmet', lambda: _fx_certs(td, certs, status={'E0_ref_s15485863': 'CONTRACT_NOT_MET'}, names=['E0_ref_s15485863']),
                    lambda: _fx_certs(td, certs, names=['E0_ref_s15485863']), 'HOLD')
                #  held 가 관문 없이 풀렸다
                mut('released', lambda: globals().__setitem__('squeue_states', _states_for(td, ('PENDING', 'Priority'))),
                    lambda: globals().__setitem__('squeue_states', _states_for(td, ('PENDING', 'JobHeldUser'))), 'held 가 아니다')
                #  대기 중 파일 변경 — held 런의 덱
                dk = os.path.join(td, dd.CONFIRM_REST[3], 'in.mixer')
                keep_dk = open(dk).read()
                mut('file_changed', lambda: open(dk, 'a').write('# 대기 중 수정\n'), lambda: open(dk, 'w').write(keep_dk), '대기 중 파일 변경')
                #  manifest 불완전 (제출 일부 실패)
                mp = os.path.join(td, 'confirm_manifest.json')
                keep_m = open(mp).read()
                mut('partial', lambda: open(mp, 'w').write(keep_m.replace('"complete": true', '"complete": false')),
                    lambda: open(mp, 'w').write(keep_m), 'manifest 가 완전하지 않다')
                #  soft OUT_OF_RANGE 는 통과 (§6)
                _fx_certs(td, certs, status={'LC_soft_r8_s15485863': 'OUT_OF_RANGE'}, names=['LC_soft_r8_s15485863'])
                for n_ in dd.CONFIRM_REST:
                    if os.path.exists(os.path.join(td, n_, APPROVAL_FILE)):
                        os.remove(os.path.join(td, n_, APPROVAL_FILE))
                pr3, ids3 = rest_gate(td, certs, pol, cj)
                res['oor_pass'] = ['ok'] if (not pr3 and len(ids3) == 12) else []
                #  승인이 이미 있고 다르다 (다른 증서) — 덮지 않는다
                _fx_certs(td, certs, names=['LC_soft_r8_s15485863'])
                pr4, _ = rest_gate(td, certs, pol, cj)
                res['approval_diff'] = pr4 if any('승인 증서가 이미 있고' in x for x in pr4) else []
                print('        ' + ' · '.join(f'{k}:{"✓" if v else "✗"}' for k, v in res.items()))
                return ok0 and ok_sc and all(res.values())
        finally:
            squeue_states = real_sq
    chk('S⑨ ★ confirm-rest 관문 (§8-2 ⑤ 해제 증거 반례) — 정상: 진짜 생산자 증서 6 → 승인 12 · start_check 가 받는다 · release 재시도 (승인 같으면 그대로) / '
        '반례 거부: 오래된 증서 (다시 봉인) · 다른 seed 증서 · E0 누락 · soft TECH_FAIL · ref CONTRACT_NOT_MET · 관문 없이 풀린 held · 대기 중 덱 변경 · '
        'manifest 불완전 (제출 일부 실패) / soft OUT_OF_RANGE 는 통과 · 이미 있는 승인과 다르면 덮지 않는다', okx(_s9))

    #  S⑩ 등록값 대조 — soft 범위 · 판독 규약 · 스키마 문자열이 다른 파일과 같다
    def _s10():
        sb = _sb()
        src = open(os.path.join(LAUNCH_DIR, 'launch_highbo.sh'), encoding='utf-8').read()
        g = re.search(r"^REG = (\{[^\n]*\})", src, re.M)
        leg = eval(g.group(1)) if g else None                                     # noqa: S307 — 리포 파일의 리터럴 한 줄
        sc = _fx_start_check()
        return (SOFT_RANGE_PCT == sb.cv.SOFT_RANGE_PCT == 7.37 and READER_REG == dict(sb.REG) and leg == READER_REG
                and LAUNCH_SCHEMA == sb.cv.LAUNCH_SCHEMA == sc.LAUNCH_SCHEMA and APPROVAL_SCHEMA == sc.APPROVAL_SCHEMA
                and REG_N_EXPECTED == 100000 and REG_R_CONTAINER == READER_REG['r_container'])
    chk('S⑩ 등록값 한 벌 — soft 범위 5.8 (검사기 = 관문) · 판독 규약 (관문 = 맹검 래퍼 = 옛 rest 관문 REG) · 봉인 · 승인 스키마 (관문 = 시작 대조기) · '
        'n_expected · r_container', okx(_s10))
    print()
    if fails:
        print(f'mixer_stage_gate selftest: {n_ok[0]}/{n_ok[0] + len(fails)} — ✗ {len(fails)} 건 실패')
        return 1
    print(f'mixer_stage_gate selftest: {n_ok[0]}/{n_ok[0]} PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())

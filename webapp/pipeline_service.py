#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 분석 파이프라인의 **단계 계약 · provenance · 프로세스간 lock**.

`docs/codex_dem_webapp_code_review_20260807.md` Phase B (F-02 / F-03 / F-05) 대응.
app.py 의 라우트에서 분리해 **한 곳에서만** 정의한다 (리뷰 F-17: 같은 순서를 네 곳이
각자 구현해 drift 가 이미 발생했다).

═══ F-02: baseline 과 Stage E 의 계산 세대가 섞이던 문제 ════════════════════════
옛 흐름은 이랬다:
  ① network 산출물 백업 → ② results/ 통째로 삭제 → ③ run_pipeline() 이 network 를
  **다시 풀고** 그 새 결과로 **Stage E 를 만든다** → ④ 옛 network 파일을 그 위에 복원
  → ⑤ 옛 baseline 키를 full_metrics 에 머지하고 "network SKIPPED" 를 찍고 return.
결과: `full_metrics.json` 안에서 **baseline σ = 옛 network**, **Stage E = 방금 새로 푼
network 기준**.  수치가 우연히 같으면 숨지만 solver 를 고친 뒤 재분석하면 provenance 가
깨진다.  게다가 "생략" 이라면서 실제로는 매번 solver 를 돌려 OOM 위험도 그대로였다.

여기서 고정하는 계약:
  • preserve 경로 → **network subprocess 호출 0회**.
  • 보존 산출물을 **Stage E 보다 먼저** 복원한다 → Stage E 는 항상 화면에 실제로 남는
    baseline 을 보고 계산한다.
  • network 산출물에는 `network_provenance.json` 으로 run_id 를 새기고, Stage E 직후
    `stage_e_parent_network_run_id` 를 full_metrics 에 새겨 **둘의 일치를 검증**한다.

═══ F-05: parse 이후 실패가 전부 성공으로 보고되던 문제 ═════════════════════════
옛 run_pipeline 은 parse 만 검사하고 나머지는 rc 를 로그에 넣은 뒤 무조건 success 를
반환했다.  여기서는 단계마다 `required` 와 `expects` (기대 산출물)를 선언하고,
필수 단계가 nonzero 이거나 기대 산출물이 없으면 **failed**, 선택 단계만 실패하면
**partial** 로 내린다.  `done` 은 필수 단계가 전부 성공했을 때만이다.

═══ F-03: OOM 방지 lock 이 프로세스 로컬이던 문제 ═══════════════════════════════
`threading.Semaphore(1)` 은 module-global 이라 Gunicorn workers=2 에서 서로를 모른다.
게다가 정상 경로의 solver 호출은 애초에 그 lock 밖이었다 (force 여부와 무관하게
run_pipeline 안에서 돌고, wrapper 의 lock 블록은 solver 가 파일을 못 썼을 때만 도달하는
사실상 죽은 코드였다).  여기서는 **파일 lock** 으로 바꿔 worker 를 가로질러 직렬화한다.
⚠ 이것은 한 호스트 안에서만 유효하다 — 다중 호스트로 가면 Redis/DB lease 가 필요하다.
"""
from __future__ import annotations

import contextlib
import errno
import glob
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

#: network solver 가 만드는 산출물 일체 (하나라도 빠지면 Physics 컬럼이 사라진다).
NETWORK_ARTIFACT_GLOBS = (
    'network_conductivity.json',
    'network_conductivity_dual.json',
    'network_conductivity_hertzian.json',
    'network_conductivity_physics.json',
    # ★ RC4-03 (Codex 4회차): 'network_summary.csv' 는 여기 **있으면 안 된다** —
    #   그 파일은 network solver 가 아니라 **analyze_contacts.py 가** 쓴다
    #   (analyze_contacts.py:295, 무조건 실행되는 경로).  glob 에 들어 있으면
    #     ① stash 경로: contact 가 쓴 새 summary 를 치웠다가 solver 가 안 만드니
    #        성공 시 drop_stash 로 **지워버린다** (내가 stash 를 넣으며 만든 실데이터 손상)
    #     ② preserve 경로: snapshot 의 **옛** summary 가 새 contact summary 를 덮는다
    #   → contact 단계의 필수 산출물로 옮겼다.
    'network_raw_*',
    'network_provenance.json',
)

#: ★ 보존이 **의미를 가지려면 반드시 있어야 하는** baseline 산출물 (CB-02).
#:   옛 구현은 NETWORK_ARTIFACT_GLOBS 중 **하나라도** 있으면 스냅샷을 만들었는데,
#:   force 경로가 solver 실패에도 도장(`network_provenance.json`)을 남기므로
#:   **실패 도장 하나만으로 스냅샷이 생겨** 다음 기본 재분석이 preserve 를 골랐다.
#:   → solver 0회 + baseline 없음 + status='done' 으로 **영구 false-done**.
#:   (Codex 교차검증 CB-02 에서 동적 재현됨.)
NETWORK_BASELINE_REQUIRED = 'network_conductivity.json'

#: network 산출물의 세대를 식별하는 파일 (**게시된 active baseline** 을 가리킨다).
PROVENANCE_FILE = 'network_provenance.json'

#: 가장 최근 **시도** (성공/실패 모두).  active 와 분리한다 — RR2-01.
ATTEMPT_FILE = 'network_attempt.json'

_LOCK_NAME = 'dem_network_solver.lock'

#: ★ RC4-02 (Codex 4회차): Stage E 가 `full_metrics.json` 에 쓰는 **관리 대상 키 전부**.
#:   옛 격리는 이름에 `_stage_e` 가 들어간 키만 걷어내서, 아래 비격리 키들이 남아
#:   partial 실행(보정값 하나만 쓰고 끝)이 옛 metadata 와 섞인 채 성공이 됐다.
#:   실측 예: 25 ℃ 재실행 뒤에도 옛 60 ℃ `stage_e_temperature_provenance` 가 남았다.
#:
#:   ⚠ `thermal_sigma_full_mScm[_physics]` 는 **격리하지 않는다** — Stage E 가 치유하긴
#:     하지만 baseline network 산출물이기도 해서, 걷어내면 baseline 을 지우게 된다.
#:     (그 이중 소유 자체가 최종형 manifest 에서 정리해야 할 대상이다.)
def is_stage_e_key(k: str) -> bool:
    return ('_stage_e' in k or k.startswith('stage_e_')
            or k in ('fracture_aware_method_full', 'validation_flags'))


#: ★ RC5-01 (Codex 5회차): Stage E 성공 판정이 `any('_stage_e' in k)` 였다.  그래서
#:   `garbage_stage_e: null` **한 개**만 있어도 새 parent/run/code-SHA 가 success 로
#:   도장됐다 (Codex 동적 재현: garbage/null 둘 다 success, partial 실행이 안 닫힘).
#:
#:   → **exact schema** 로 바꾼다.  아래는 `run_network_full_corrections.run_one()` 이
#:   정상 종료마다 **무조건** 쓰는 최소 집합이다 (전부 함수 최상위 4칸 들여쓰기 =
#:   조건부 아님을 코드에서 확인).  loss 3필드·temperature provenance·thermal baseline
#:   heal 은 조건부라 여기 넣지 않는다.
#:
#:   ⚠ 이것은 **중간형**이다.  최종형은 Stage E 스크립트가 per-run manifest(schema
#:   version + 6-record 행렬 + digest)를 쓰고 앱이 그것을 검증하는 것 — 지금처럼 앱이
#:   키 목록을 추측하면 스크립트가 바뀔 때 drift 한다.  그 전까지는 이 집합을 정본으로
#:   두고, `run_one` 이 키를 늘리면 여기도 같이 늘린다.
STAGE_E_REQUIRED_KEYS = (
    'sigma_full_mScm_stage_e',
    'sigma_full_mScm_stage_e_physics',
    'electronic_sigma_full_mScm_stage_e',
    'electronic_sigma_full_mScm_stage_e_physics',
    'thermal_sigma_full_mScm_stage_e',
    'thermal_sigma_full_mScm_stage_e_physics',
    'stage_e_source',
    'stage_e_factors_used',
    'stage_e_fracture_stage_counts',
    'fracture_aware_method_full',
    'validation_flags',
)


#: 11-키 중 **유한한 수** 이어야 하는 여섯 (H/P × ionic/electronic/thermal).
STAGE_E_NUMERIC_KEYS = STAGE_E_REQUIRED_KEYS[:6]

#: **매핑(dict)** 이어야 하는 것들.  `stage_e_source='not-a-map'` 같은 손상을 잡는다.
STAGE_E_MAPPING_KEYS = ('stage_e_source', 'stage_e_factors_used',
                        'stage_e_fracture_stage_counts', 'validation_flags')

#: 비어 있지 않은 **문자열** 이어야 하는 것.
STAGE_E_STRING_KEYS = ('fracture_aware_method_full',)


def stage_e_missing_keys(full_metrics, null_ok_keys=()):
    """정상 Stage E 레코드의 **결손·손상** 목록 (빈 튜플이면 건전).

    ⚠ 값이 `None` 이면 **없는 것으로 본다** — 키 존재만 보면 partial 이 안 닫힌다.
      (진짜 0 은 `0.0` 이라 통과한다.)

    ★ RC6-01 (Codex 6회차): 옛 구현은 `is None` 만 봐서 **손상 레코드를 완전으로**
      판정했다.  Codex 재현 그대로:
          sigma_full_mScm_stage_e = NaN      → 통과했다
          stage_e_source = 'not-a-map'       → 통과했다
          validation_flags = []              → 통과했다
      → 타입·유한성까지 본다.  숫자 여섯은 **finite number**, 매핑 넷은 **dict**,
        method 는 **비어 있지 않은 문자열**.  (bool 은 int 의 서브클래스라 명시 배제 —
        `sigma=True` 가 숫자로 통과하면 안 된다.)

    ★ `null_ok_keys`: network 가 **정당하게** `valid_null/valid_zero` 를 낸 채널
      (열망 미퍼콜 등).  그 채널의 Stage E 값이 None 인 것은 **결손이 아니라 정합**이다.
      이것이 Codex 가 지적한 "network 는 valid_null 을 정상으로 보는데 Stage E 는 결손으로
      본다" 는 계약 충돌의 해소다 — 상류 상태를 알고 있을 때만 완화한다.
    """
    if not isinstance(full_metrics, dict):
        return STAGE_E_REQUIRED_KEYS
    bad, ok_null = [], set(null_ok_keys or ())
    for k in STAGE_E_REQUIRED_KEYS:
        v = full_metrics.get(k)
        if v is None:
            if k not in ok_null:
                bad.append(k)
            continue
        if k in STAGE_E_NUMERIC_KEYS:
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                bad.append(f'{k}:타입({type(v).__name__})')
            elif not math.isfinite(v):
                bad.append(f'{k}:비유한({v})')
        elif k in STAGE_E_MAPPING_KEYS:
            if not isinstance(v, dict):
                bad.append(f'{k}:매핑아님({type(v).__name__})')
        elif k in STAGE_E_STRING_KEYS:
            if not isinstance(v, str) or not v.strip():
                bad.append(f'{k}:빈문자열/타입')
    return tuple(bad)



def new_run_id() -> str:
    """세대 ID.  시간 접두사를 붙여 정렬하면 시간순이 된다."""
    return time.strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8]


def code_sha(root=None) -> str:
    """현재 코드의 git SHA (없으면 'unknown').  결과가 어느 코드에서 나왔는지 고정용."""
    root = root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        out = subprocess.run(['git', '-C', root, 'rev-parse', 'HEAD'],
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip() if out.returncode == 0 else 'unknown'
    except Exception:
        return 'unknown'


def file_digest(path, chunk=1 << 20) -> str:
    """입력 파일 해시 — 같은 입력인지 판정용 (재현성 계약)."""
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while True:
                b = f.read(chunk)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()[:16]
    except OSError:
        return ''


# ─────────────────────────────── 프로세스간 lock ───────────────────────────────

class LockUnavailable(RuntimeError):
    """network lock 을 못 잡았다 — solver 를 **실행하지 않는다** (CB-03)."""


@contextlib.contextmanager
def network_lock(timeout=None, lock_dir=None, require=True):
    """network solver 직렬화 — **프로세스를 가로질러** 동작하는 파일 lock.

    threading.Semaphore 는 Gunicorn workers=2 에서 서로를 모른다 (F-03).
    POSIX 는 fcntl.flock, Windows 는 msvcrt.locking 을 쓴다.

    ★ CB-03 (Codex 교차검증): 옛 구현은 lock 을 **못 잡아도 그냥 yield** 했고 호출부가
      그 값을 무시해 solver 를 그대로 돌렸다 = **fail-open**.  OOM 방지라는 목적 자체가
      무너진다.  이제 기본이 `require=True` 이고 **획득 실패 시 LockUnavailable 을
      던진다** — 호출부는 그것을 단계 실패로 기록하고 solver 를 실행하지 않는다.
      (Windows msvcrt 는 무기한 대기가 없으므로 non-blocking 재시도 + 실제 timeout.)
      `require=False` 는 진단·테스트 전용.
    """
    path = os.path.join(lock_dir or tempfile.gettempdir(), _LOCK_NAME)
    fh = open(path, 'a+b')
    acquired = False
    mode = None
    try:
        try:
            import fcntl
            mode = 'flock'
            if timeout is None:
                fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
                acquired = True
            else:
                deadline = time.time() + timeout
                while True:
                    try:
                        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                        acquired = True
                        break
                    except OSError:
                        if time.time() >= deadline:
                            break
                        time.sleep(0.5)
        except ImportError:
            try:
                import msvcrt
                mode = 'msvcrt'
                deadline = time.time() + (timeout if timeout is not None else 3600.0)
                while True:
                    try:
                        msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
                        acquired = True
                        break
                    except OSError:
                        if time.time() >= deadline:
                            break
                        time.sleep(0.5)
            except ImportError:
                mode = None
        if not acquired and require:
            raise LockUnavailable(
                f'network lock 미획득 (backend={mode or "없음"}, path={path}). '
                'solver 를 실행하지 않는다 — 동시 실행은 OOM 위험이다.')
        yield acquired
    finally:
        if acquired:
            try:
                import fcntl
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
            except ImportError:
                try:
                    import msvcrt
                    fh.seek(0)
                    msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
                except Exception:
                    pass
        fh.close()


# ───────────────────────────── network 산출물 세대 ─────────────────────────────

def snapshot_network(results_dir, case_id=''):
    """보존할 **성공한** network 세대를 임시 디렉터리로 스냅샷.  없으면 None.

    results_dir 을 지우기 **전에** 호출한다.  복원은 Stage E **전에** 한다 —
    그래야 Stage E 가 실제로 남을 baseline 을 보고 계산한다 (F-02).

    ★ CB-02 (Codex 교차검증에서 동적 재현): 보존 자격을 **두 가지로 좁힌다**.
      ① baseline 파일(`network_conductivity.json`)이 실제로 있어야 한다.
      ② 도장이 있으면 `solver_status == 'success'` 여야 한다.
    옛 구현은 glob 중 하나만 맞아도 스냅샷을 만들었고, force 경로가 **실패에도 도장을
    남기므로** 실패 도장 하나로 스냅샷이 생겨 다음 기본 재분석이 preserve 를 골랐다
    → solver 0회 · baseline 없음 · status='done' 인 **영구 false-done**.
    (도장 이전 legacy 산출물은 ①만 만족하면 보존을 허용한다 — 그 시절엔 성공한
     산출물만 남았으므로.)
    """
    if not os.path.exists(os.path.join(results_dir, NETWORK_BASELINE_REQUIRED)):
        return None
    prov = read_network_provenance(results_dir)
    if prov.get('provenance_state') == 'invalid':
        return None                       # ★ RV-06: 검증 불가 → fail-closed (legacy 아님)
    if prov.get('network_run_id') and prov.get('solver_status') != 'success':
        return None                       # 실패한 세대는 보존하지 않는다 → solver 재실행
    items = []
    for pat in NETWORK_ARTIFACT_GLOBS:
        items += glob.glob(os.path.join(results_dir, pat))
    if not items:
        return None
    tmp = tempfile.mkdtemp(prefix=f'net_bk_{case_id}_')
    for src in items:
        dst = os.path.join(tmp, os.path.relpath(src, results_dir))
        os.makedirs(os.path.dirname(dst) or tmp, exist_ok=True)
        (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, dst)
    return tmp


def restore_network(snapshot_dir, results_dir):
    """스냅샷을 되돌린다.  → 복원한 항목 수."""
    if not snapshot_dir or not os.path.isdir(snapshot_dir):
        return 0
    os.makedirs(results_dir, exist_ok=True)
    n = 0
    for name in os.listdir(snapshot_dir):
        src, dst = os.path.join(snapshot_dir, name), os.path.join(results_dir, name)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        n += 1
    return n


def stamp_network_provenance(results_dir, run_id, inputs=None, solver_status='success',
                             argv=None):
    """network 산출물에 세대 도장을 찍는다.

    ★ CB-07 (Codex): 결과를 **실제로 바꾸는** 인자가 빠져 있었다 — `type_map`, `scale`,
      `contact_mode`.  code_sha 와 입력 digest 만으로는 같은 결과를 재현할 수 없다.
      argv 로 받아 함께 남긴다.
    """
    prov = {'network_run_id': run_id, 'code_sha': code_sha(),
            'stamped_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'solver_status': solver_status,
            'solver': 'network_conductivity.py',
            'argv': dict(argv or {}),
            'units_contract': 'sim_to_real_v1',
            'input_digests': inputs or {}}
    atomic_write_json(os.path.join(results_dir, PROVENANCE_FILE), prov)
    return prov


def read_network_provenance(results_dir):
    """network 산출물의 세대.  도장이 없으면(옛 산출물) run_id=None."""
    path = os.path.join(results_dir, PROVENANCE_FILE)
    if not os.path.exists(path):
        return {'network_run_id': None, 'code_sha': None, 'solver_status': 'unknown',
                'provenance_state': 'missing',
                'note': 'pre-provenance artifact (도장 이전 세대)'}
    try:
        d = json.load(open(path))
        d.setdefault('provenance_state', 'valid')
        return d
    except (OSError, ValueError) as e:
        # ★ RV-06: 파일이 **있는데 못 읽는** 것은 '도장 이전' 이 아니라 **검증 불가**다.
        #   옛 코드는 둘을 같은 fallback 으로 돌려 손상 도장을 legacy 로 오인 → preserve.
        return {'network_run_id': None, 'code_sha': None, 'solver_status': 'unreadable',
                'provenance_state': 'invalid', 'note': f'provenance 손상: {e}'}


def stash_network(results_dir, case_id=''):
    """기존 network 산출물을 **옆으로 치운다** → solver 가 빈 자리에 쓴다.  → stash dir | None

    ★ RR2-02 (Codex 2회차): `fresh=(mtime_ns, size)` 는 인과 증거가 아니다.
      metadata-only touch 만으로 통과하고(내용 불변인데 success), 반대로 결정론적 solver 가
      byte-identical 결과를 다시 써도 stale 로 **거부**한다(가용성 문제).
      해시도 단독으로는 안 된다 — 정상 재계산이 같은 해시를 내면 구별할 수 없다.

    그래서 판정을 stat/해시 비교가 아니라 **인과**로 바꾼다: lock 안에서 기존 산출물을
    치우고 빈 자리에 실행시키면, 실행 후 파일이 **존재한다는 사실 자체**가 "이번 실행이
    만들었다" 는 증거다.  실패하면 치워둔 것을 되돌려 **이전 성공 세대를 그대로 보존**한다.
    (최종형인 per-run 임시 디렉터리 + manifest + atomic publish 로 가는 중간 단계이고,
     Codex 가 제안한 그 중간형이다.)
    """
    items = []
    for pat in NETWORK_ARTIFACT_GLOBS:
        items += glob.glob(os.path.join(results_dir, pat))
    if not items:
        return None
    st = tempfile.mkdtemp(prefix=f'net_stash_{case_id}_')
    for src in items:
        shutil.move(src, os.path.join(st, os.path.basename(src)))
    return st


def restore_stash(stash_dir, results_dir):
    """치워둔 산출물을 되돌린다 (실행 실패 시).  → 되돌린 개수."""
    if not stash_dir or not os.path.isdir(stash_dir):
        return 0
    n = 0
    for name in os.listdir(stash_dir):
        dst = os.path.join(results_dir, name)
        if os.path.exists(dst):
            (shutil.rmtree if os.path.isdir(dst) else os.remove)(dst)
        shutil.move(os.path.join(stash_dir, name), dst)
        n += 1
    shutil.rmtree(stash_dir, ignore_errors=True)
    return n


def drop_stash(stash_dir):
    """치워둔 것을 버린다 (실행 성공 시)."""
    if stash_dir:
        shutil.rmtree(stash_dir, ignore_errors=True)


#: Stage E 실패 시도 기록 — active 필드가 아니라 별도 파일 (RC5-02, network 와 같은 규약).
STAGE_E_ATTEMPT_FILE = 'stage_e_attempt.json'

#: ★ raw thermal 은 `is_stage_e_key()` 가 **일부러 제외**한다 — Stage E 가 baseline 으로
#:   읽기 때문에 실행 전에 걷어내면 입력을 지우게 된다.  그런데 Stage E 는 그 값을
#:   heal(덮어쓰기)하기도 해서, 실패했을 때 **되돌리지 않으면 network 산출물이 오염된 채
#:   남는다** (Codex RC5-02 실측: thermal 777 로 바뀐 것이 실패 후에도 남았다).
#:   ⇒ 격리는 안 하되 **snapshot/rollback 대상에는 넣는다**.
RAW_THERMAL_KEYS = ('thermal_sigma_full_mScm', 'thermal_sigma_full_mScm_physics')


#: thermal 채널 상태 → 이것이 **네트워크 단계 실패**인가.
#:   ★ RC5-03 근본수정: "값이 없다" 를 한 덩어리로 보면 안 된다.  열망이 퍼콜하지 않아
#:     κ 가 없는 것은 **물리적으로 옳은 답**이고, 솔버가 예외로 죽은 것은 **실패**다.
#:     옛 코드는 둘을 구분할 수 없어 (둘 다 "키 없음") 상위가 판단할 근거가 없었다.
#:     이제 solver 가 `thermal_status` 를 항상 남기므로 여기서 갈라 준다.
_THERMAL_OK_STATES = frozenset({'computed', 'valid_zero', 'valid_null'})
_THERMAL_FAIL_STATES = frozenset({'failed'})


def thermal_channel_verdict(net_data):
    """→ ('ok'|'fail'|'unknown', reason).  network JSON 의 thermal 채널 판정.

    'unknown' = 옛 산출물(상태 필드가 없는 세대).  **실패로 취급하지 않는다** — 옛
    데이터를 소급해서 실패로 만들면 재분석 없이는 못 고치는 케이스가 무더기로 생긴다.
    대신 그 사실을 그대로 돌려주어 호출부가 라벨을 붙일 수 있게 한다.
    """
    if not isinstance(net_data, dict):
        return 'unknown', 'network 결과 없음'
    st = net_data.get('thermal_status')
    if st is None:
        return 'unknown', '옛 세대 산출물 (thermal_status 이전)'
    if st in _THERMAL_FAIL_STATES:
        return 'fail', net_data.get('thermal_status_reason') or st
    if st in _THERMAL_OK_STATES:
        return 'ok', net_data.get('thermal_status_reason') or st
    return 'unknown', f'알 수 없는 상태: {st}'


def network_content_verdict(results_dir, modes=('hertzian', 'physics'), strict=True):
    """새로 만든 network 산출물의 **내용**을 판정한다 → (ok, reason).

    ★ RC6-02 (Codex 6회차): 옛 게이트는 `run_stage` 의 **파일 존재**만 보고 stash 를
      버린 뒤 active 를 success 로 찍었고, thermal 판정은 **그 뒤에** 했다.  그래서
      required 단계가 실패했는데도 active provenance 는 success 이고 **옛 완전 세대는
      이미 버려진** 상태가 재현됐다 (실측: σ 999 게시 · stash 없음).
      → 내용 검증을 `run_stage(verify=…)` 로 **게이트 안**으로 옮긴다.  실패하면
        기존 `restore_stash` 경로가 그대로 옛 세대를 되살린다.

    ★ RC6-03: legacy(=hertzian 복사본) 하나만 보면 **Physics 실패가 H 성공에 가린다**.
      두 mode 파일을 각각 본다.

    strict=True (새로 만든 파일) 면 `unknown` 도 실패로 본다 — 방금 우리 solver 가
    만든 파일에 상태가 없다는 것은 schema 위반이다.  옛 세대를 읽을 때(preserve)는
    strict=False 로 두어 **소급 실패**를 만들지 않는다.
    """
    bad, seen = [], []
    for mode in modes:
        p = os.path.join(results_dir, f'network_conductivity_{mode}.json')
        if not os.path.exists(p):
            bad.append(f'{mode}: 파일 없음')
            continue
        try:
            with open(p) as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            bad.append(f'{mode}: 읽기 실패 ({type(e).__name__})')
            continue
        seen.append(mode)
        v, why = thermal_channel_verdict(data)
        if v == 'fail' or (strict and v == 'unknown'):
            bad.append(f'{mode}.thermal={v} ({why})')
    if not seen:
        bad.append('per-mode 산출물이 하나도 없다')
    return (not bad), ('; '.join(bad) if bad else 'ok: ' + ', '.join(seen))


#: ★ RC6-07 (Codex 6회차, Windows 실측): 자식 프로세스의 출력 인코딩을 계약하지 않으면
#:   **Windows 기본 CP949 에서 solver 가 첫 non-ASCII 로그에 죽는다**.
#:     UnicodeEncodeError: 'cp949' codec can't encode character '\u2014'
#:     network_conductivity.py:1092  →  rc=1, network JSON 0개
#:   같은 입력을 `PYTHONUTF8=1` 로 돌리면 rc=0 에 네 파일이 다 나온다.  우리 solver 는
#:   212 종의 non-ASCII (─ ★ ⚠ σ …) 를 21 곳에서 print 한다 — ASCII 로 줄이는 것은
#:   현실적이지 않으므로 **인코딩을 계약**한다.
#:   ⚠ 자식만 UTF-8 로 바꾸고 부모 decode 를 기본값(CP949)으로 두면 안 된다 — 양쪽을 함께.
def utf8_subprocess_kwargs(env=None):
    """subprocess 공통 인자 — 자식 stdio 를 UTF-8 로, 부모 decode 도 UTF-8 로 고정한다."""
    e = dict(env if env is not None else os.environ)
    e['PYTHONUTF8'] = '1'
    e['PYTHONIOENCODING'] = 'utf-8'
    return {'text': True, 'encoding': 'utf-8', 'errors': 'replace', 'env': e}


def snapshot_keys(d, keys):
    """{key: {'present': bool, 'value': v}} — **없었다는 사실**까지 보존한다.

    단순히 값만 저장하면 "원래 없던 키" 를 복원할 때 `None` 으로 되살려 놓게 된다.
    없던 것은 없는 상태로 되돌려야 정확한 rollback 이다.
    """
    d = d if isinstance(d, dict) else {}
    return {k: ({'present': True, 'value': d[k]} if k in d else {'present': False})
            for k in keys}


def restore_keys(d, snap):
    """`snapshot_keys` 의 기록대로 정확히 되돌린다 (없었으면 삭제)."""
    for k, rec in (snap or {}).items():
        if rec.get('present'):
            d[k] = rec.get('value')
        else:
            d.pop(k, None)
    return d


def record_stage_e_attempt(results_dir, parent_run_id, reason='', restored=True):
    """Stage E **실패 시도**를 active 필드와 분리해 남긴다 (RC5-02).

    옛 코드는 `stage_e_status` / `stage_e_attempt_parent_network_run_id` 를 active
    full_metrics 에 썼다.  실패 시도의 흔적이 게시된 세대의 필드를 차지하는 것은
    network 쪽에서 이미 RR2-01 로 고친 것과 같은 문제다.
    """
    atomic_write_json(os.path.join(results_dir, STAGE_E_ATTEMPT_FILE), {
        'stage_e_attempt_parent_network_run_id': parent_run_id,
        'status': 'failed', 'reason': reason,
        'previous_generation_restored': bool(restored),
        'code_sha': code_sha(),
        'attempted_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
    })


def record_network_attempt(results_dir, run_id, status, reason='', argv=None):
    """**실패 시도**를 active provenance 와 **분리해** 기록한다 (RR2-01).

    옛 코드는 실패에도 `network_provenance.json` 을 새 run_id 로 덮어써서, 실패 시도의 ID 가
    `full_metrics.network_run_id` 와 `stage_e_parent_network_run_id` 까지 차지했다 —
    게시된 baseline 은 옛 성공 세대인데 ID 는 실패 시도를 가리키는 모순.
    이제 active 도장은 **성공했을 때만** 갱신하고, 시도는 이 별도 파일에 남긴다.
    """
    atomic_write_json(os.path.join(results_dir, ATTEMPT_FILE), {
        'network_attempt_run_id': run_id, 'solver_status': status,
        'reason': reason, 'code_sha': code_sha(),
        'attempted_at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'argv': dict(argv or {}),
    })


#: `os.replace` 재시도 (Windows).  대기시간 0.02·0.04·0.08·0.16·0.32 s = 총 0.62 s.
_REPLACE_RETRIES = 5
_REPLACE_BACKOFF = 0.02


def _replace_retry(tmp, path, retries=_REPLACE_RETRIES, sleep=None):
    """`os.replace` — Windows 의 일시적 대상파일 점유에만 제한 재시도한다.

    ★ Codex 가 **다른 워크스트림(DFT 대시보드)에서 실측**한 것을 이쪽에 옮긴 것이다:
      Windows 12 프로세스 × 100 건 × 10 회에서 `os.replace()` 가
      `PermissionError [WinError 5]` 로 간헐 실패해 **992/1000** 만 저장됐다.
      락은 정상이었다(임계구역 동시성 1) — 백신·인덱서 같은 **외부 handle** 이 대상
      파일을 잠깐 여는 것이라 우리 락으로는 막을 수 없다.  POSIX 의 rename 은 이런
      이유로 실패하지 않으므로 이 재시도는 리눅스에선 사실상 no-op 이다.

    ⚠ 재시도는 **PermissionError/EACCES 에만** 건다.  다른 OSError(경로 없음, 다른
      파일시스템 등)는 재시도해도 낫지 않고 진짜 버그를 숨기므로 즉시 올린다.
    """
    for attempt in range(retries + 1):
        try:
            os.replace(tmp, path)
            return attempt
        except PermissionError:
            if attempt >= retries:
                raise
        except OSError as e:
            if e.errno != errno.EACCES or attempt >= retries:
                raise
        (sleep or time.sleep)(_REPLACE_BACKOFF * (2 ** attempt))
    raise AssertionError('unreachable')            # pragma: no cover


def atomic_write_json(path, obj):
    """같은 디렉터리 temp → fsync → os.replace(재시도).  부분 쓰기/truncate 를 막는다 (F-10)."""
    d = os.path.dirname(path) or '.'
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix='.tmp_', suffix='.json')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(obj, f, indent=2, default=str)
            f.flush()
            os.fsync(f.fileno())
        _replace_retry(tmp, path)
    except Exception:
        with contextlib.suppress(OSError):
            os.unlink(tmp)
        raise


# ─────────────────────────────── 단계 계약 ───────────────────────────────

class StageOutcome(dict):
    """한 단계의 결과.  dict 이므로 기존 analysis_log 소비자와 그대로 호환된다."""

    @property
    def ok(self):
        return bool(self.get('ok'))


#: 기본 실행기.  ★ 모듈 속성으로 두는 이유: 기본값을 def 시점에 바인딩하면 테스트가
#: 파이프라인 **전체**(run_pipeline)를 가짜 subprocess 로 돌릴 수 없다 — Codex 요청 T1
#: ("contact rc=1 이면 pipeline failed")은 개별 단계가 아니라 전체 경로를 태워야 한다.
_RUNNER = subprocess.run


def _stat_sig(results_dir, patterns):
    """기대 산출물들의 (경로 → (mtime_ns, size)) 지문.  신선도 판정용."""
    sig = {}
    for rel in patterns:
        for p in glob.glob(os.path.join(results_dir, rel)):
            try:
                s = os.stat(p)
                sig[p] = (s.st_mtime_ns, s.st_size)
            except OSError:
                pass
    return sig


def run_stage(name, cmd, *, cwd=None, required=False, expects=(), results_dir=None,
              runner=None, fresh=False, verify=None):
    """subprocess 한 단계를 계약과 함께 실행한다.

    required : 실패하면 파이프라인 전체가 failed
    expects  : 이 단계가 만들어야 하는 파일들 (results_dir 기준 상대경로).
               rc 가 0 이어도 이게 없으면 실패로 본다 — network CLI 는 물리망이
               없을 때 **파일을 안 쓰고도 exit 0** 이 될 수 있다 (리뷰 F-05/F-12).
    fresh    : ★ RV-02.  expects 의 **존재**만 보면, results 를 지우지 않는 경로
               (retry/batch)에서 solver 가 rc=0 으로 아무것도 안 써도 **옛 산출물이
               새 성공 세대로 재도장**된다 (Codex 재검증에서 동적 재현).  fresh=True 면
               실행 전후의 (mtime_ns, size) 지문을 비교해 **실제로 새로 쓰였는지**를 본다.
    verify   : ★ RV-01.  파일 존재만으로는 증거가 안 되는 단계용 (Stage E 는 별도 파일이
               아니라 full_metrics.json **안의 키**를 만든다).  `verify(results_dir)` 가
               False 를 돌리면 실패로 본다.
    runner   : 테스트에서 가짜 실행기를 주입하기 위한 훅.
    """
    before = _stat_sig(results_dir, expects) if (fresh and results_dir) else None
    try:
        res = (runner or _RUNNER)(cmd, capture_output=True, timeout=None, cwd=cwd,
                                  **utf8_subprocess_kwargs())
        rc, out, err = res.returncode, res.stdout, res.stderr
    except Exception as e:                       # noqa: BLE001 — 실행 자체 실패도 단계 실패
        rc, out, err = 1, '', f'{type(e).__name__}: {e}'
    missing, stale, verify_failed = [], [], False
    if results_dir:
        for rel in expects:
            hits = glob.glob(os.path.join(results_dir, rel))
            if not hits:
                missing.append(rel)
        if fresh and before is not None:
            after = _stat_sig(results_dir, expects)
            # ★ RC6-05 (Codex 6회차): 옛 판정은 **전체 dict** 를 한 번에 비교해서
            #   `after == before` 일 때만 stale 로 봤다 → 네 산출물 중 **하나만** 새로
            #   써도 통과하고, 나머지 셋은 옛 것인 채로 새 성공 세대로 도장됐다
            #   (Codex 동적 재현: ok=True, unchanged_old 3개).
            #   → **파일별**로 본다: 실행 전에 있던 파일 중 지문이 그대로인 것은 전부
            #     stale 이다.  (실행 전에 없던 파일은 새로 생긴 것이므로 신선하다.)
            stale = sorted(os.path.basename(k) for k, v in before.items()
                           if after.get(k) == v)
    if verify is not None:
        try:
            verify_failed = not bool(verify(results_dir))
        except Exception:                                   # noqa: BLE001
            verify_failed = True
    ok = (rc == 0) and not missing and not stale and not verify_failed
    return StageOutcome(step=name, stdout=out, stderr=err, rc=rc, ok=ok,
                        required=required, missing_outputs=missing,
                        stale_outputs=stale, verify_failed=verify_failed)


def summarize(stages):
    """단계들 → (status, 실패 목록).  status ∈ {done, partial, failed}.

    옛 코드는 무조건 success 였다 (F-05): full_metrics 가 없어도 케이스가 done 이 됐다.
    """
    hard = [s for s in stages if s.get('required') and not s.get('ok')]
    soft = [s for s in stages if not s.get('required') and not s.get('ok')]
    if hard:
        return 'failed', hard
    return ('partial' if soft else 'done'), soft

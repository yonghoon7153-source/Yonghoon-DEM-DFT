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
import glob
import hashlib
import json
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
    'network_summary.csv',
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

#: network 산출물의 세대를 식별하는 파일.
PROVENANCE_FILE = 'network_provenance.json'

_LOCK_NAME = 'dem_network_solver.lock'


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


def stamp_network_provenance(results_dir, run_id, inputs=None, solver_status='success'):
    """network 산출물에 세대 도장을 찍는다."""
    prov = {'network_run_id': run_id, 'code_sha': code_sha(),
            'stamped_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'solver_status': solver_status,
            'input_digests': inputs or {}}
    atomic_write_json(os.path.join(results_dir, PROVENANCE_FILE), prov)
    return prov


def read_network_provenance(results_dir):
    """network 산출물의 세대.  도장이 없으면(옛 산출물) run_id=None."""
    try:
        with open(os.path.join(results_dir, PROVENANCE_FILE)) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {'network_run_id': None, 'code_sha': None, 'solver_status': 'unknown',
                'note': 'pre-provenance artifact (도장 이전 세대)'}


def atomic_write_json(path, obj):
    """같은 디렉터리 temp → fsync → os.replace.  부분 쓰기/truncate 를 막는다 (F-10)."""
    d = os.path.dirname(path) or '.'
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix='.tmp_', suffix='.json')
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(obj, f, indent=2, default=str)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
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


def run_stage(name, cmd, *, cwd=None, required=False, expects=(), results_dir=None,
              runner=None):
    """subprocess 한 단계를 계약과 함께 실행한다.

    required : 실패하면 파이프라인 전체가 failed
    expects  : 이 단계가 만들어야 하는 파일들 (results_dir 기준 상대경로).
               rc 가 0 이어도 이게 없으면 실패로 본다 — network CLI 는 물리망이
               없을 때 **파일을 안 쓰고도 exit 0** 이 될 수 있다 (리뷰 F-05/F-12).
    runner   : 테스트에서 가짜 실행기를 주입하기 위한 훅.
    """
    try:
        res = (runner or _RUNNER)(cmd, capture_output=True, text=True, timeout=None, cwd=cwd)
        rc, out, err = res.returncode, res.stdout, res.stderr
    except Exception as e:                       # noqa: BLE001 — 실행 자체 실패도 단계 실패
        rc, out, err = 1, '', f'{type(e).__name__}: {e}'
    missing = []
    if results_dir:
        for rel in expects:
            hits = glob.glob(os.path.join(results_dir, rel))
            if not hits:
                missing.append(rel)
    ok = (rc == 0) and not missing
    return StageOutcome(step=name, stdout=out, stderr=err, rc=rc, ok=ok,
                        required=required, missing_outputs=missing)


def summarize(stages):
    """단계들 → (status, 실패 목록).  status ∈ {done, partial, failed}.

    옛 코드는 무조건 success 였다 (F-05): full_metrics 가 없어도 케이스가 done 이 됐다.
    """
    hard = [s for s in stages if s.get('required') and not s.get('ok')]
    soft = [s for s in stages if not s.get('required') and not s.get('ok')]
    if hard:
        return 'failed', hard
    return ('partial' if soft else 'done'), soft

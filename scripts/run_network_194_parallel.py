#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""194 건 (LHS 130 + lhsx 64) 망 배치 병렬 실행기 — 동적 큐 · 레인 K (기본 20) · 레인당 1 코어.

1저자 10-05 밤 지시: *"1코어 20개로 20개"* — 하나씩이 아니라 20 건을 동시에, 케이스마다 단일 스레드.

무엇을 하나
───────────────────────────────────────────────────────────────────────────────
  • 케이스마다 **기존 배치 CLI 를 그대로 한 번** 부른다 (규율 ① — 새 계산 경로 없음):
        python3 scripts/lhs_webapp_batch.py --stop-after network --case <c> --harvest-dir <수확> --cohort <코호트>
                --work <ROOT>/cases/<c>/work --out-dir <ROOT>/cases/<c>/out
    같은 프레임 관문 (sha · 프레임 1 · 중복 · type_map) 과 망 정지 계약은 전부 그 배치 · 웹앱 쪽 그대로다.
  • 동적 큐 — 비용 (수확 JSON `contact_scan.n_rows_last` = 접촉 행 수 · 10-01 coverage 배치 경과와 상관 0.97) 큰 순.
    빈 레인이 다음 케이스를 집는다 (정적 분할이 아니다 — 느린 케이스가 다른 레인을 놀리지 않는다).
  • 케이스마다 경과 (s) · 최대 RSS (`os.wait4` — 그 케이스 프로세스와 기다린 자식 프로세스 중 **가장 큰 하나**) · user/sys CPU 를
    `cases/<c>/worker.json` 과 `cases/<c>/log.txt` 끝 줄에 남긴다 (시도마다 · 다시 돌려도 기록이 쌓인다).
  • merge — 케이스별 `out/status.json` · `out/metrics_flat.csv` → 코호트별 한 폴더 `<ROOT>/merged/{lhs,lhsx}/`.
    **배치 자신의 writer** (`lhs_webapp_batch.write_outputs`) 로 쓴다 ⇒ 순차 배치 한 번과 같은 모양 (selftest ⑧ 이 바이트로 대조) ·
    인계 생성기 `lhs_design_dataset.load_webapp` 이 그대로 읽는다 (selftest ⑨).  τ 관문 (`tau_flux.py`) 용 `results/<case>` 링크 —
    결과가 없는 케이스도 빈 폴더로 둔다 (τ 표에서 행이 빠지지 않는다 · NOT_COMPUTED 로 남는다).
  • 실패는 숨기지 않는다 — 워커가 죽어 케이스 기록이 없으면 merge 가 status 'failed' 기록 (사유 = 워커 rc · 신호 · 로그 경로) 을 만든다.
    done · partial 이 아닌 케이스가 하나라도 있으면 rc 1 · 구조 이상 (다른 케이스 기록 · 세대 섞임 · 스키마) 이면 rc 2 (merged 를 쓰지 않는다).

설정 (전부 `manifest.json` 에 남는다)
───────────────────────────────────────────────────────────────────────────────
  ① 스레드 — OMP · MKL · OPENBLAS · NUMEXPR · VECLIB_MAXIMUM = 1 (지시 "1 코어").  BLAS 스레드 수는 합산 순서를 바꿔 마지막 자리가
     달라질 수 있다 — 예전 순차 배치 (스레드 기본값) 와 비트 대조할 때 이것을 같이 적는다.
  ② network lock — 웹앱은 network solver 를 **기계 전체에서 하나씩** 돌린다 (`pipeline_service.network_lock` · 파일 lock 이
     `tempfile.gettempdir()` = TMPDIR 에 있다 · OOM 방지 · CB-03).  그대로 두면 20 레인이어도 망 단계는 하나씩 돈다 (지시와 어긋난다)
     ⇒ 기본 `--network-lock per-case` = 케이스마다 TMPDIR 을 따로 준다 (lock 이 케이스 안에서만 잡힌다).  OOM 방지는 대신
     메모리 예산 입장 관문 (아래 ⑤) 이 맡는다.  `--network-lock shared` = 웹앱 직렬화 그대로 (망 단계가 하나씩).
  ③ cwd = 케이스 폴더 — 피복 단계가 **실행 위치 기준** 추적 파일
     (`docs/figures/physics_regime/coverage_hertz_vs_physics_summary.csv` · 원장 LHS-27) 을 덮어쓴다.  20 개가 같은 파일을 동시에
     쓰지 않게 · 리포가 더러워져 runs[].dirty 가 거짓 신호가 되지 않게 케이스 폴더에서 돌린다 (그 줄 말고는 망 경로에 실행 위치 상대
     경로가 없다 — 10-05 grep: parse · analyze_contacts[_bimodal] · coverage · network_conductivity · dem_analysis_core ·
     plastic_coverage · se_material · 웹앱 모듈).  경로 인자는 전부 절대 경로로 넘긴다.
  ④ pyc — `app.run_pipeline` 은 부를 때마다 `scripts/__pycache__/*.pyc` 를 지운다.  여럿이 동시에 지우면 한쪽이 FileNotFoundError 로
     죽는다 ⇒ 워커는 PYTHONDONTWRITEBYTECODE=1 로 띄우고 (새 pyc 를 안 만든다) 발사 전에 한 번 지운다.
  ⑤ 메모리 — 케이스 추정 = MEM_BASE_MB + MEM_PER_KCONTACT_MB × 접촉 천 개 (real_14 · 106,563 접촉 실측 최대 RSS 549 MB 에서 잡은
     **보수 추정** · WSL 실측으로 고칠 것 — 끝에 실측/추정 비를 찍는다).  예산 (`--mem-budget-gb`, 기본 = 발사 시 MemAvailable − 2 GB) 안에서만
     새 케이스를 띄운다 (돌고 있는 것이 없으면 늘 하나는 띄운다) · 앞 케이스가 예산에 안 맞으면 뒤에서 맞는 것을 먼저 띄우되 (backfill)
     앞 케이스가 레인 수만큼 완료를 기다렸으면 backfill 을 멈춘다 (굶김 방지).  `--min-free-gb` = 실측 MemAvailable 바닥 (두 번째 관문).
     `--mem-budget-gb 0` = 예산 끔 (순수 K 레인).

사용 (WSL · 리포 체크아웃 · 봉인 커밋 detached — 예전 배치와 같은 `~/dem-audit`)
───────────────────────────────────────────────────────────────────────────────
  P=~/Yonghoon-DEM-DFT/venv/bin/python
  $P scripts/run_network_194_parallel.py run --root ~/net194_<sha> --dry-run       # 사전 점검 · 계획만 (아무것도 안 쓴다)
  $P scripts/run_network_194_parallel.py run --root ~/net194_pilot -j 2 --case lhsx_040 --case lhs00_055   # 시범 (가장 큰 + 작은)
  $P scripts/run_network_194_parallel.py run --root ~/net194_<sha>                 # 194 건 · 20 레인
  $P scripts/run_network_194_parallel.py status --root ~/net194_<sha>              # 진행 (다른 터미널)
  $P scripts/run_network_194_parallel.py retry --root ~/net194_<sha> -j 8          # done · partial 아닌 케이스만 다시 (기록 보존)
  $P scripts/run_network_194_parallel.py merge --root ~/net194_<sha>               # run · retry 끝에 자동 — 다시 묶기
  $P scripts/run_network_194_parallel.py --selftest
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import csv
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.dont_write_bytecode = True          # ④ — 이 프로세스도 scripts/__pycache__ 에 pyc 를 만들지 않는다
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import lhs_harvest_batch as HB          # noqa: E402  (코호트 · 경로 치환 · 같은 step 메시 — 배치와 같은 함수)
import lhs_webapp_batch as LWB          # noqa: E402  (KEEP_STATUS · SCHEMA · write_outputs — merge 는 배치의 writer 로 쓴다)

SCHEMA = 'network_parallel_launcher/v1'
WORKER_SCHEMA = 'network_parallel_worker/v1'
BATCH = ROOT / 'scripts' / 'lhs_webapp_batch.py'
KEEP = tuple(LWB.KEEP_STATUS)           # ('done', 'partial') — 배치 · 인계 생성기 (WA_OK_STATUS) 와 같은 집합
STOP = 'network'

#: 코호트 — 10-01 접촉 단계 배치 (`d1ec42fba`) · 5번 coverage 배치 (`1e09f661d`) 와 같은 수확 · 코호트 (같은 프레임 sha 의 기준).
#:   union · design 은 인계표 생성기 후속 명령에만 쓴다 (v1.1 README 와 같은 인자).
COHORT_SPECS = {
    'lhs': dict(harvest='docs/data/lhs_descriptors_cov_1e09f661d', cohort='docs/data/area_s2_cohort.tsv', expect_n=130,
                union='docs/data/lhs_union_20260927/lhs130_union.tsv', design=''),
    'lhsx': dict(harvest='docs/data/lhsx_descriptors_cov_1e09f661d', cohort='docs/data/lhsx_descriptors_20260925/_cohort.tsv',
                 expect_n=64, union='docs/data/lhs_union_20260927/lhsx64_union.tsv',
                 design='docs/data/lhsx_design_adapted_20260929.csv'),
}
#: 인계 v1.2 의 웹앱 묶음 — network 배치는 다섯 묶음을 다 낸다 (`lhs_design_dataset.WA_STAGE_GROUPS['network']` · RGL-03).
HANDOVER_GROUPS = 'contact,percolation,f1,fracture,area'

THREAD_ENV = {'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1',
              'NUMEXPR_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'}

#: ⑤ 메모리 · 시간 추정 — real_14 (접촉 106,563 · 원자 33,289) 를 `stop_after='network'` 로 돌린 실측 (10-05 · 이 세션 컨테이너):
#:   `wsl_network_smoke.py` 자식 (단일 스레드 env) = 경과 73.4 s · 최대 RSS 550 MB · 결과 폴더 67 MB
#:   (같은 날 BLAS 기본 스레드 · 다른 작업과 경쟁한 실행 = 294 s · 549 MB — 시간은 경쟁 탓 · 메모리는 같다).
#:   ⚠ 추정은 입장 관문과 계획 출력에만 쓴다 (값에 영향 없음) — WSL 실측 (worker.json · progress.tsv) 으로 고칠 것.
MEM_BASE_MB = 150.0
MEM_PER_KCONTACT_MB = 4.5               # 150 + 4.5 × 106.6 = 630 MB (실측 550 — 15 % 여유)
TIME_PER_KCONTACT_S = 0.7               # 73.4 s / 106.6 k (컨테이너 · 단일 스레드 · 경쟁 없음 — WSL 실측으로 고칠 것)
DISK_PER_CONTACT_B = 700                # 67 MB / 106.6 k ≈ 630 B (atoms.csv · contacts.csv · *_analyzed.csv 가 대부분)

#: 해시로 남기는 코드 — σ 를 바꿀 수 있는 모듈 (`seal_s3_prerun.NUMERIC_MODULES`) + 망 경로 · 배치 · 소비자.
CODE_FILES = (
    'scripts/network_conductivity.py', 'scripts/plastic_coverage.py', 'scripts/audit_constriction_deleted.py',
    'scripts/extract_se_network_diagnostics.py', 'scripts/dem_analysis_core.py', 'scripts/analyze_contacts.py',
    'scripts/analyze_contacts_bimodal.py', 'scripts/coverage_physics_vs_hertzian.py', 'scripts/parse_liggghts.py',
    'scripts/se_material.py', 'scripts/metrics_json.py', 'scripts/tau_flux.py', 'scripts/lhs_webapp_batch.py',
    'scripts/lhs_harvest_batch.py', 'scripts/lhs_descriptor_harvest.py', 'webapp/app.py', 'webapp/pipeline_service.py',
    'webapp/export_master_csv.py', 'webapp/type_map_resolve.py')
LHS27_FILE = 'docs/figures/physics_regime/coverage_hertz_vs_physics_summary.csv'


class LaunchError(RuntimeError):
    """사전 점검 · 계획 실패 — 아무것도 띄우지 않는다."""


# ─────────────────────────────────── 작은 도구 ───────────────────────────────────
def now_iso():
    return time.strftime('%Y-%m-%dT%H:%M:%S')


def _abs(p) -> Path:
    p = Path(str(p)).expanduser()
    return (p if p.is_absolute() else ROOT / p).resolve()


def write_json(path: Path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name('.' + path.name + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def read_json(path: Path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def sha256_file(p: Path):
    try:
        h = hashlib.sha256()
        with open(p, 'rb') as fh:
            for b in iter(lambda: fh.read(1 << 20), b''):
                h.update(b)
        return h.hexdigest()
    except OSError:
        return None


def code_hashes():
    return {rel: sha256_file(ROOT / rel) for rel in CODE_FILES}


def git_info():
    def g(*a):
        try:
            return subprocess.run(['git', '-C', str(ROOT), *a], capture_output=True, text=True, timeout=30).stdout
        except Exception:                                   # noqa: BLE001
            return ''
    sha = g('rev-parse', 'HEAD').strip()
    #  ⚠ strip() 을 먼저 하면 첫 줄의 선행 공백 (상태 칸) 이 지워져 경로 첫 글자를 먹는다 (seal_s3_prerun 의 같은 결함) — 줄만 나눈다
    porcelain = [ln for ln in g('status', '--porcelain', '--untracked-files=no').splitlines() if ln.strip()]
    return dict(sha=sha, short=sha[:9], branch=g('rev-parse', '--abbrev-ref', 'HEAD').strip(),
                dirty=bool(porcelain), porcelain=porcelain)


def meminfo():
    """/proc/meminfo → 바이트 (Linux · WSL).  없으면 빈 dict."""
    d = {}
    try:
        with open('/proc/meminfo', encoding='ascii', errors='replace') as fh:
            for ln in fh:
                k, _, v = ln.partition(':')
                parts = v.split()
                if parts and parts[0].isdigit():
                    d[k.strip()] = int(parts[0]) * (1024 if len(parts) > 1 and parts[1].lower() == 'kb' else 1)
    except OSError:
        pass
    return d


def gib(b):
    return None if b is None else round(b / 2 ** 30, 2)


def cpu_info():
    n = os.cpu_count()
    try:
        aff = len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        aff = n
    return dict(cpu_count=n, cpu_affinity=aff)


def est_mem_mb(contacts: int) -> float:
    return MEM_BASE_MB + MEM_PER_KCONTACT_MB * contacts / 1000.0


def est_time_s(contacts: int) -> float:
    return TIME_PER_KCONTACT_S * contacts / 1000.0


def worker_env(case_dir: Path, lock_mode: str) -> dict:
    env = dict(os.environ)
    env.update(THREAD_ENV)
    env['PYTHONDONTWRITEBYTECODE'] = '1'                 # ④
    env['PYTHONUNBUFFERED'] = '1'                        # 로그가 바로 보이게
    env.setdefault('MPLBACKEND', 'Agg')
    if lock_mode == 'per-case':
        env['TMPDIR'] = str(case_dir / 'tmp')            # ② — network lock 파일이 이 케이스 안에 생긴다
    return env


def purge_pyc(scripts_dir: Path, dry=False) -> int:
    """④ — run_pipeline 이 지우는 것과 같은 glob (`scripts/__pycache__/*.pyc`) 을 발사 전에 한 번 지운다."""
    hits = sorted((scripts_dir / '__pycache__').glob('*.pyc'))
    if not dry:
        for p in hits:
            with contextlib.suppress(FileNotFoundError):
                p.unlink()
    return len(hits)


@contextlib.contextmanager
def root_lock(root: Path):
    """같은 ROOT 에 실행기 둘이 붙지 않게 (run · retry · merge)."""
    import fcntl
    root.mkdir(parents=True, exist_ok=True)
    fh = open(root / '.launcher.lock', 'a+')
    try:
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise LaunchError(f'{root} 를 다른 실행기가 쓰고 있다 (.launcher.lock) — 끝난 뒤 다시')
        yield
    finally:
        with contextlib.suppress(OSError):
            import fcntl as _f
            _f.flock(fh.fileno(), _f.LOCK_UN)
        fh.close()


def pid_alive(pid: int, case: str) -> bool:
    """그 pid 가 살아 있고 명령줄에 케이스 이름이 있는가 (retry 가 아직 도는 고아 워커를 다시 띄우지 않게)."""
    try:
        os.kill(int(pid), 0)
    except (ProcessLookupError, ValueError, TypeError):
        return False
    except PermissionError:
        return True
    try:
        cmd = Path(f'/proc/{int(pid)}/cmdline').read_bytes().replace(b'\0', b' ').decode('utf-8', 'replace')
        return case in cmd
    except OSError:
        return True


# ─────────────────────────────────── 계획 ───────────────────────────────────
def cohort_specs(args) -> dict:
    specs = {k: dict(v) for k, v in COHORT_SPECS.items()}
    for name in specs:
        for key in ('harvest', 'cohort'):
            v = getattr(args, f'{name}_{key}', None)
            if v:
                specs[name][key] = v
    return specs


def build_plan(cohorts, specs, case_filter=(), order='cost') -> dict:
    """→ {'cohorts': [...], 'queue': [{case, cohort, contacts, est_mem_mb, est_time_s}, …]} — 결정적 (같은 입력 = 같은 순서)."""
    out_c, queue, seen = [], [], {}
    want = set(case_filter or ())
    for name in cohorts:
        if name not in specs:
            raise LaunchError(f'모르는 코호트 {name!r} — {sorted(specs)}')
        sp = specs[name]
        hdir, coh = _abs(sp['harvest']), _abs(sp['cohort'])
        if not hdir.is_dir():
            raise LaunchError(f'{name}: 수확 폴더가 없다 — {hdir}')
        if not coh.is_file():
            raise LaunchError(f'{name}: 코호트 TSV 가 없다 — {coh}')
        #  케이스 목록 = 배치와 같은 규칙 (`lhs_webapp_batch.run_batch` — 수확 폴더의 *.json · '_' 로 시작하면 케이스가 아니다)
        cases = sorted(p.stem for p in hdir.glob('*.json') if not p.name.startswith('_'))
        n_sel = 0
        for c in cases:
            if want and c not in want:
                continue
            if c in seen:
                raise LaunchError(f'케이스 {c} 가 두 코호트에 있다 ({seen[c]} · {name})')
            seen[c] = name
            h = read_json(hdir / f'{c}.json') or {}
            k = (h.get('contact_scan') or {}).get('n_rows_last')
            if not isinstance(k, int) or k <= 0:              # 옛 수확 — 입자 수로 대신 (비용 순서에만 쓴다)
                k = int(sum((h.get('phase_counts') or {}).values()) or 0)
            queue.append(dict(case=c, cohort=name, contacts=int(k),
                              est_mem_mb=round(est_mem_mb(k), 1), est_time_s=round(est_time_s(k), 1)))
            n_sel += 1
        out_c.append(dict(name=name, harvest_dir=str(hdir), cohort=str(coh), n_harvest=len(cases), n_selected=n_sel,
                          expect_n=sp.get('expect_n'), union=sp.get('union', ''), design=sp.get('design', '')))
    miss = sorted(want - set(seen))
    if miss:
        raise LaunchError(f'--case 가 어느 수확 폴더에도 없다: {miss}')
    if not queue:
        raise LaunchError('돌릴 케이스가 없다')
    if order == 'cost':
        queue.sort(key=lambda e: (-e['contacts'], e['case']))
    else:
        queue.sort(key=lambda e: e['case'])
    return dict(cohorts=out_c, queue=queue, order=order)


def case_dir(root: Path, case: str) -> Path:
    return root / 'cases' / case


def case_cmd(python, worker_script, cspec, case, cdir: Path, root_from='', root_to='') -> list:
    cmd = [str(python), str(worker_script), '--stop-after', STOP, '--case', case,
           '--harvest-dir', cspec['harvest_dir'], '--cohort', cspec['cohort'],
           '--work', str(cdir / 'work'), '--out-dir', str(cdir / 'out')]
    if root_from:
        cmd += ['--root-from', root_from, '--root-to', root_to or '']
    return cmd


def raw_problems(plan, root_from='', root_to='') -> list:
    """원자료 실재 · 같은 step 메시 — 배치가 케이스마다 REFUSED 로 남길 것을 발사 전에 센다 (sha 는 배치가 본다 · 비싸다)."""
    out = []
    for cs in plan['cohorts']:
        rows = {r['case']: r for r in HB.read_cohort(Path(cs['cohort']))}
        for e in plan['queue']:
            if e['cohort'] != cs['name']:
                continue
            r = rows.get(e['case'])
            if r is None:
                out.append((e['case'], '봉인 코호트에 없다'))
                continue
            for k, col in (('atom', 'atom_file'), ('contact', 'contact_file'), ('deck', 'deck')):
                p = HB.remap((r.get(col) or '').strip(), root_from, root_to)
                if not (r.get(col) or '').strip() or not p.is_file():
                    out.append((e['case'], f'{k} 파일 없음: {p}'))
            a = HB.remap((r.get('atom_file') or '').strip(), root_from, root_to)
            if a.is_file():
                mesh, _pick, why = HB.pick_mesh(a)
                if mesh is None:
                    out.append((e['case'], f'같은 step 메시 없음 — {why}'))
    return out


def python_versions(python) -> dict:
    code = ('import json, sys\nv = {"python": sys.version.split()[0], "executable": sys.executable}\n'
            'for m in ("numpy", "scipy", "pandas"):\n'
            '    try:\n        v[m] = __import__(m).__version__\n'
            '    except Exception as e:\n        v[m] = "MISSING " + type(e).__name__\n'
            'print(json.dumps(v))')
    try:
        r = subprocess.run([str(python), '-c', code], capture_output=True, text=True, timeout=120,
                           env=dict(os.environ, **THREAD_ENV, PYTHONDONTWRITEBYTECODE='1'))
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:                                  # noqa: BLE001
        return dict(error=f'{type(e).__name__}: {e}')


def app_supports_network() -> bool:
    """정적 확인 — 웹앱 `PIPELINE_STOP_AFTER` 에 'network' 가 있는가 (없으면 194 건이 전부 ValueError 로 failed)."""
    try:
        src = (ROOT / 'webapp' / 'app.py').read_text(encoding='utf-8')
    except OSError:
        return False
    m = re.search(r'^PIPELINE_STOP_AFTER\s*=\s*\(([^)]*)\)', src, re.M)
    return bool(m and "'network'" in m.group(1))


def preflight(args, plan, root: Path, budget_mb) -> dict:
    """CPU · 메모리 · 디스크 · git · 원자료 · 의존 — 경고 (warn) 와 중단 (stop) 을 나눠 돌려준다."""
    warn, stop = [], []
    cpu = cpu_info()
    mi = meminfo()
    lanes = args.lanes
    q = plan['queue']
    first = q[:lanes]
    if cpu['cpu_affinity'] and lanes > cpu['cpu_affinity']:
        warn.append(f'레인 {lanes} > 쓸 수 있는 CPU {cpu["cpu_affinity"]} — 레인당 1 코어가 아니다 (과다 구독)')
    avail = mi.get('MemAvailable')
    first_mb = sum(e['est_mem_mb'] for e in first)
    if avail is not None and first_mb > avail / 2 ** 20:
        warn.append(f'처음 {len(first)} 건 (큐 앞 = 가장 큰 침대) 의 메모리 추정 합 {first_mb / 1024:.1f} GB > MemAvailable '
                    f'{gib(avail)} GB — 예산 관문이 동시 수를 줄인다 (추정은 real_14 기준 · WSL 시범으로 고칠 것)')
    if args.mem_budget_gb is not None and args.mem_budget_gb <= 0:
        warn.append('메모리 예산 끔 (--mem-budget-gb 0) — 큰 침대 20 개가 한꺼번에 돌 수 있다 (OOM 이면 그 케이스는 failed · 다시 retry)')
    git = git_info()
    if git['dirty'] and not args.allow_dirty:
        hint = ' (LHS-27 부산물 — `git checkout -- ' + LHS27_FILE + '` 로 되돌린다)' if any(
            ln[3:].strip() == LHS27_FILE for ln in git['porcelain']) else ''
        stop.append(f'추적 파일이 바뀌어 있다 {git["porcelain"][:5]}{hint} — 봉인 커밋에서 돌릴 것 (진짜 의도면 --allow-dirty · 기록된다)')
    if not git['sha']:
        warn.append('git sha 를 못 읽었다 — 세대 대조 (merge) 가 약해진다')
    for cs in plan['cohorts']:
        if not args.case and cs['expect_n'] and cs['n_harvest'] != cs['expect_n']:
            warn.append(f'{cs["name"]}: 수확 JSON {cs["n_harvest"]} 건 ≠ 기대 {cs["expect_n"]} 건')
    if not app_supports_network():
        stop.append("webapp/app.py 의 PIPELINE_STOP_AFTER 에 'network' 가 없다 — 이 코드로는 망 정지 배치를 돌릴 수 없다")
    probs = raw_problems(plan, args.root_from, args.root_to)
    if probs and not args.allow_missing_raw:
        stop.append(f'원자료 · 메시 문제 {len(probs)} 건 (예: {probs[:3]}) — 경로 치환 (--root-from/--root-to) 확인 · '
                    '그래도 돌리려면 --allow-missing-raw (그 케이스는 배치가 REFUSED 로 남긴다)')
    elif probs:
        warn.append(f'원자료 · 메시 문제 {len(probs)} 건 — 그 케이스는 REFUSED 로 남는다 (--allow-missing-raw)')
    disk_need = sum(e['contacts'] for e in q) * DISK_PER_CONTACT_B
    probe = root if root.exists() else root.parent
    while not probe.exists() and probe != probe.parent:
        probe = probe.parent
    try:
        free = shutil.disk_usage(probe).free
    except OSError:
        free = None
    if free is not None and disk_need * 1.2 > free:
        warn.append(f'디스크 여유 {gib(free)} GB < 결과 추정 {gib(disk_need)} GB × 1.2 (케이스 결과 폴더 ≈ {DISK_PER_CONTACT_B} B/접촉)')
    if args.network_lock == 'shared' and lanes > 1:
        warn.append('--network-lock shared — 망 단계는 기계 전체에서 하나씩 돈다 (레인은 접촉 · 피복 단계만 겹친다)')
    tot_s = sum(e['est_time_s'] for e in q)
    eff = max(1, min(lanes, cpu['cpu_affinity'] or lanes))
    return dict(cpu=cpu, mem=dict(MemTotal_GB=gib(mi.get('MemTotal')), MemAvailable_GB=gib(avail),
                                  SwapTotal_GB=gib(mi.get('SwapTotal')), SwapFree_GB=gib(mi.get('SwapFree'))),
                lanes=lanes, mem_budget_mb=budget_mb, first_lanes_est_mem_GB=round(first_mb / 1024, 2),
                est_mem_largest_mb=max(e['est_mem_mb'] for e in q), disk_free_GB=gib(free), disk_need_GB=gib(disk_need),
                est_serial_h=round(tot_s / 3600, 2), est_makespan_h=round(max(tot_s / eff, max(e['est_time_s'] for e in q)) / 3600, 2),
                git=git, raw_problems=probs[:50], n_raw_problems=len(probs), warn=warn, stop=stop)


def print_preflight(pf, plan, args, root):
    p = print
    p(f'══ 사전 점검 — ROOT {root}')
    p(f'  CPU {pf["cpu"]["cpu_count"]} (쓸 수 있는 {pf["cpu"]["cpu_affinity"]}) · 레인 {pf["lanes"]} · 스레드/레인 1 '
      f'({", ".join(f"{k}=1" for k in THREAD_ENV)})')
    m = pf['mem']
    p(f'  메모리 MemTotal {m["MemTotal_GB"]} GB · MemAvailable {m["MemAvailable_GB"]} GB · Swap {m["SwapFree_GB"]}/{m["SwapTotal_GB"]} GB')
    bud = pf['mem_budget_mb']
    p(f'  메모리 예산 {"끔" if not bud else f"{bud / 1024:.1f} GB"} · 실측 바닥 --min-free-gb {args.min_free_gb} · '
      f'큐 앞 {min(pf["lanes"], len(plan["queue"]))} 건 추정 합 {pf["first_lanes_est_mem_GB"]} GB · 가장 큰 침대 추정 '
      f'{pf["est_mem_largest_mb"] / 1024:.2f} GB  (⚠ 케이스 최대 메모리는 아직 모른다 — real_14 549 MB @ 106,563 접촉에서 잡은 추정 · '
      f'시범 · 본 실행의 worker.json 실측으로 고칠 것)')
    p(f'  디스크 여유 {pf["disk_free_GB"]} GB · 결과 추정 {pf["disk_need_GB"]} GB')
    p(f'  시간 추정 (컨테이너 real_14 기준 · 거칠다): 직렬 {pf["est_serial_h"]} h · 이 레인 수 {pf["est_makespan_h"]} h — 케이스별 실측 초는 progress.tsv')
    g = pf['git']
    p(f'  코드 {g["short"]} ({g["branch"]}) dirty={g["dirty"]}' + (f' {g["porcelain"][:3]}' if g['dirty'] else ''))
    p(f'  network lock = {args.network_lock}  (per-case = 케이스마다 TMPDIR — 망 단계도 동시에 · shared = 웹앱처럼 하나씩)')
    for cs in plan['cohorts']:
        p(f'  코호트 {cs["name"]}: 수확 {cs["n_harvest"]} 건 (선택 {cs["n_selected"]}) · {cs["harvest_dir"]} · 코호트 {cs["cohort"]}')
    p(f'  원자료 · 메시 문제 {pf["n_raw_problems"]} 건')
    p('  ⚠ Codex RGLR 3차 재검증 (10-05): 194 생산 실행 · 인계 = HOLD (RGLR2-01·02·03 수정 → 저자 승인 재봉인 뒤).  '
      '이 실행기는 그 판정을 대신하지 않는다 — 어느 코드에서 돌았는지는 manifest.json 이 증명한다.')
    for w in pf['warn']:
        p(f'  ⚠ {w}')
    for s in pf['stop']:
        p(f'  ⛔ {s}')


# ─────────────────────────────────── 실행 (동적 큐) ───────────────────────────────────
class _Lane:
    __slots__ = ('entry', 'case', 'cdir', 'popen', 'pid', 't0', 'start_iso', 'log', 'cmd', 'attempt', 'env_note')


def _attempt_no(cdir: Path) -> int:
    w = read_json(cdir / 'worker.json') or {}
    return len(w.get('attempts') or []) + 1


def _case_outcome(cdir: Path, case: str):
    st = read_json(cdir / 'out' / 'status.json')
    if not isinstance(st, dict):
        return None, None
    rec = (st.get('cases') or {}).get(case)
    return (rec or {}).get('status'), rec


def _sig_name(rc):
    if rc is None or rc >= 0:
        return None
    try:
        return signal.Signals(-rc).name
    except ValueError:
        return f'SIG{-rc}'


def run_queue(root: Path, manifest: dict, todo: list, lanes: int, run_no: int, *, budget_mb=None, min_free_gb=0.0,
              poll=0.5, out=print) -> dict:
    """동적 큐 — 빈 레인이 다음 케이스를 집는다 (예산 · 실측 바닥 관문).  → 이번 실행 요약 dict."""
    python, wscript = manifest['python'], manifest['worker_script']
    lock_mode = manifest['network_lock']
    rf, rt = manifest.get('root_from') or '', manifest.get('root_to') or ''
    cspec = {c['name']: c for c in manifest['plan']['cohorts']}
    t_launch = time.monotonic()
    pending = collections.deque(todo)
    running: dict = {}
    done_n, n_total = 0, len(todo)
    counts = collections.Counter()
    throttle = dict(events=0, budget_events=0, backfills=0, max_concurrent=0)
    throttled = [False]
    head_wait = [0]
    cost_total = sum(e['contacts'] for e in todo) or 1
    cost_done = [0]
    progress = root / 'progress.tsv'
    if not progress.exists():
        progress.write_text('\t'.join(('case', 'cohort', 'attempt', 'run', 'outcome', 'rc', 'signal', 'wall_s', 'peak_rss_mb',
                                       'est_mem_mb', 'user_s', 'sys_s', 'contacts', 'start', 'end')) + '\n', encoding='utf-8')

    def est_running():
        return sum(l.entry['est_mem_mb'] for l in running.values())

    def start(e):
        nonlocal done_n
        ln = _Lane()
        ln.entry, ln.case = e, e['case']
        ln.cdir = case_dir(root, e['case'])
        for sub in ('work', 'out', 'tmp'):
            (ln.cdir / sub).mkdir(parents=True, exist_ok=True)
        ln.attempt = _attempt_no(ln.cdir)
        ln.cmd = case_cmd(python, wscript, cspec[e['cohort']], e['case'], ln.cdir, rf, rt)
        env = worker_env(ln.cdir, lock_mode)
        ln.env_note = {k: env.get(k) for k in (*THREAD_ENV, 'TMPDIR', 'PYTHONDONTWRITEBYTECODE')}
        ln.log = open(ln.cdir / 'log.txt', 'ab')
        ln.start_iso = now_iso()
        ln.log.write((f'===== attempt {ln.attempt} (run {run_no}) start {ln.start_iso} · cwd {ln.cdir} · lock {lock_mode}\n'
                      f'===== cmd: {shlex.join(ln.cmd)}\n').encode('utf-8'))
        ln.log.flush()
        ln.t0 = time.monotonic()
        #  ③ cwd = 케이스 폴더 · 새 세션 (중단 시 그 케이스의 프로세스 묶음을 통째로 끈다 — 솔버 자식 포함)
        try:
            ln.popen = subprocess.Popen(ln.cmd, cwd=str(ln.cdir), env=env, stdin=subprocess.DEVNULL, stdout=ln.log,
                                        stderr=subprocess.STDOUT, start_new_session=True)
        except OSError as e:                                 # 워커를 못 띄웠다 — 기록하고 다음 케이스로 (실행기는 서지 않는다)
            ln.log.write(f'===== LAUNCH_ERROR {type(e).__name__}: {e}\n'.encode('utf-8'))
            ln.log.close()
            w = read_json(ln.cdir / 'worker.json') or dict(schema=WORKER_SCHEMA, case=ln.case, cohort=ln.entry['cohort'], attempts=[])
            w.setdefault('attempts', []).append(dict(attempt=ln.attempt, run=run_no, cmd=ln.cmd, cwd=str(ln.cdir), start=ln.start_iso,
                                                     end=now_iso(), rc=None, signal=None, outcome='LAUNCH_ERROR',
                                                     why=f'{type(e).__name__}: {e}', est_mem_mb=ln.entry['est_mem_mb'],
                                                     contacts=ln.entry['contacts']))
            write_json(ln.cdir / 'worker.json', w)
            done_n += 1
            counts['LAUNCH_ERROR'] += 1
            out(f'[{done_n}/{n_total}] {ln.case} LAUNCH_ERROR — {type(e).__name__}: {e}', flush=True)
            return
        ln.pid = ln.popen.pid
        write_json(ln.cdir / 'worker.pid.json', dict(pid=ln.pid, case=ln.case, attempt=ln.attempt, run=run_no, start=ln.start_iso))
        running[ln.case] = ln
        throttle['max_concurrent'] = max(throttle['max_concurrent'], len(running))

    def finalize(ln, status, ru, interrupted=False):
        nonlocal done_n
        rc = os.waitstatus_to_exitcode(status)
        ln.popen.returncode = rc                     # Popen 이 다시 기다리지 않게 (wait4 로 이미 거뒀다)
        t1 = time.monotonic()
        wall = round(t1 - ln.t0, 2)
        peak_kb = int(ru.ru_maxrss)                  # Linux = KB · 이 프로세스와 기다린 자식 중 최대 (트리 합이 아니다)
        outcome, rec = _case_outcome(ln.cdir, ln.case)
        if interrupted:
            outcome_s = 'interrupted'
        elif outcome is None:
            outcome_s = 'NO_RECORD'                  # 워커가 케이스 기록을 못 쓰고 끝났다 (죽음 · 신호 · 관문 전 예외)
        else:
            outcome_s = outcome
        att = dict(attempt=ln.attempt, run=run_no, cmd=ln.cmd, cwd=str(ln.cdir), lock_mode=lock_mode, env=ln.env_note,
                   start=ln.start_iso, end=now_iso(), t_start_s=round(ln.t0 - t_launch, 3), t_end_s=round(t1 - t_launch, 3),
                   wall_s=wall, rc=rc, signal=_sig_name(rc), peak_rss_kb=peak_kb, peak_rss_mb=round(peak_kb / 1024, 1),
                   est_mem_mb=ln.entry['est_mem_mb'], contacts=ln.entry['contacts'],
                   user_s=round(ru.ru_utime, 2), sys_s=round(ru.ru_stime, 2), outcome=outcome_s,
                   batch_elapsed_s=(rec or {}).get('elapsed_s'), why=(rec or {}).get('why'),
                   failed_stages=(rec or {}).get('failed_stages'), network_run_id=(rec or {}).get('network_run_id'))
        w = read_json(ln.cdir / 'worker.json') or dict(schema=WORKER_SCHEMA, case=ln.case, cohort=ln.entry['cohort'], attempts=[])
        w.setdefault('attempts', []).append(att)
        write_json(ln.cdir / 'worker.json', w)
        try:
            ln.log.write((f'===== attempt {ln.attempt} end {att["end"]} · outcome {outcome_s} · rc {rc}'
                          f'{" (" + att["signal"] + ")" if att["signal"] else ""} · wall {wall:.1f} s · peak RSS {peak_kb / 1024:.0f} MB · '
                          f'user {att["user_s"]:.1f} s · sys {att["sys_s"]:.1f} s\n').encode('utf-8'))
        finally:
            ln.log.close()
        with contextlib.suppress(FileNotFoundError):
            (ln.cdir / 'worker.pid.json').unlink()
        with open(progress, 'a', encoding='utf-8') as fh:
            fh.write('\t'.join(str(x) for x in (ln.case, ln.entry['cohort'], ln.attempt, run_no, outcome_s, rc, att['signal'] or '',
                                                wall, att['peak_rss_mb'], ln.entry['est_mem_mb'], att['user_s'], att['sys_s'],
                                                ln.entry['contacts'], att['start'], att['end'])) + '\n')
        done_n += 1
        counts[outcome_s] += 1
        cost_done[0] += ln.entry['contacts']
        el = time.monotonic() - t_launch
        eta = (el / cost_done[0] * (cost_total - cost_done[0])) if cost_done[0] else 0
        out(f'[{done_n}/{n_total}] {ln.case} {outcome_s} rc={rc}{" (" + att["signal"] + ")" if att["signal"] else ""} · '
            f'{wall:.0f} s · RSS {peak_kb / 1024:.0f} MB (추정 {ln.entry["est_mem_mb"]:.0f}) · 도는 중 {len(running)} · '
            f'경과 {el / 3600:.2f} h · 남은 추정 ≈ {eta / 3600:.2f} h (접촉 수 비례)'
            + (f' · {att["why"]}' if att['why'] and outcome_s not in KEEP else ''), flush=True)

    def admit():
        if not pending:
            return None
        if running and min_free_gb > 0:
            av = meminfo().get('MemAvailable')
            if av is not None and av < min_free_gb * 2 ** 30:
                if not throttled[0]:
                    throttle['events'] += 1
                    out(f'  ⏸ MemAvailable {gib(av)} GB < --min-free-gb {min_free_gb} — 새 케이스를 기다린다 (도는 중 {len(running)})',
                        flush=True)
                throttled[0] = True
                return None
        throttled[0] = False
        if not running or not budget_mb:
            return pending.popleft()
        if est_running() + pending[0]['est_mem_mb'] <= budget_mb:
            head_wait[0] = 0
            return pending.popleft()
        if head_wait[0] < lanes:                                 # backfill — 앞 케이스가 레인 수만큼 기다리기 전까지만
            for i, e in enumerate(pending):
                if est_running() + e['est_mem_mb'] <= budget_mb:
                    del pending[i]
                    throttle['backfills'] += 1
                    return e
        throttle['budget_events'] += 1
        return None

    def kill_all(why):
        out(f'⛔ {why} — 도는 케이스 {len(running)} 개를 끈다 (프로세스 묶음 SIGTERM → 20 s → SIGKILL)', flush=True)
        for ln in running.values():
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(ln.pid, signal.SIGTERM)
        deadline = time.monotonic() + 20
        while running and time.monotonic() < deadline:
            for case, ln in list(running.items()):
                pid, st, ru = os.wait4(ln.pid, os.WNOHANG)
                if pid:
                    del running[case]
                    finalize(ln, st, ru, interrupted=True)
            time.sleep(0.2)
        for case, ln in list(running.items()):
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(ln.pid, signal.SIGKILL)
            _pid, st, ru = os.wait4(ln.pid, 0)
            del running[case]
            finalize(ln, st, ru, interrupted=True)

    def _term(_s, _f):
        raise KeyboardInterrupt
    old_term = signal.signal(signal.SIGTERM, _term)
    interrupted = False
    try:
        while pending or running:
            while len(running) < lanes:
                e = admit()
                if e is None:
                    break
                start(e)
            reaped = False
            for case, ln in list(running.items()):
                pid, st, ru = os.wait4(ln.pid, os.WNOHANG)
                if pid:
                    del running[case]
                    finalize(ln, st, ru)
                    reaped = True
                    if pending and budget_mb and est_running() + pending[0]['est_mem_mb'] > budget_mb:
                        head_wait[0] += 1
            if not reaped:
                time.sleep(poll)
    except KeyboardInterrupt:
        interrupted = True
        kill_all('중단 (Ctrl-C · SIGTERM)')
    finally:
        signal.signal(signal.SIGTERM, old_term)
    return dict(run=run_no, n=n_total, finished=done_n, not_started=[e['case'] for e in pending], outcomes=dict(counts),
                interrupted=interrupted, wall_h=round((time.monotonic() - t_launch) / 3600, 3), **throttle)


# ─────────────────────────────────── merge ───────────────────────────────────
def _synth_failed(case, cdir: Path, wrec: dict | None, why0: str) -> dict:
    """워커가 케이스 기록을 못 남겼다 — 조용히 빠지지 않게 'failed' 기록을 만든다 (배치 어휘 그대로)."""
    att = ((wrec or {}).get('attempts') or [None])[-1] or {}
    why = why0
    if att:
        why = (f'워커가 케이스 기록 없이 끝났다 — rc {att.get("rc")}'
               + (f' ({att.get("signal")})' if att.get('signal') else '')
               + f' · 경과 {att.get("wall_s")} s · 최대 RSS {att.get("peak_rss_mb")} MB · 로그 {cdir / "log.txt"}')
    return dict(case=case, when=att.get('start') or '', stop_after=STOP, status='failed', failed_stages=['worker: no case record'],
                why=why, elapsed_s=att.get('wall_s'), parallel_synthesized=True)


def merge(root: Path, *, allow_mixed=False, out=print) -> int:
    """케이스별 산출 → `<root>/merged/<코호트>/` (status.json · metrics_flat.csv · results/ · parallel_cases.tsv) + merge_report.json.

    rc 0 = 전 케이스 done · partial · 이상 없음 / 1 = 실패 · 이상 있음 (merged 는 쓴다 — 실패는 기록으로 남는다) /
    2 = 구조 이상 (남의 케이스 기록 · 스키마 · 정지점 · 세대 섞임) → merged 를 바꾸지 않는다.
    """
    man = read_json(root / 'manifest.json')
    if not isinstance(man, dict) or man.get('schema') != SCHEMA:
        out(f'⛔ {root}/manifest.json 이 없거나 스키마가 다르다 — 이 실행기가 만든 ROOT 가 아니다')
        return 2
    git_sha = (man.get('git') or {}).get('sha') or ''
    structural, mixed, anomalies, failures = [], [], [], []
    tmp_root = root / '.merged_tmp'
    if tmp_root.exists():
        shutil.rmtree(tmp_root)
    report = dict(schema=SCHEMA + '#merge', merged_at=now_iso(), git_sha=git_sha, cohorts={},
                  code_changed_since_launch=sorted(k for k, v in code_hashes().items() if v != (man.get('code_hashes') or {}).get(k)))
    runs_recs = [read_json(p) or {} for p in sorted((root / 'runs').glob('run_*.json'))]
    changed_during = sorted({f for r in runs_recs for f in (r.get('code_changed_during_run') or [])})
    if changed_during:
        mixed.append(f'실행 중 코드가 바뀌었다: {changed_during}')
    for cs in man['plan']['cohorts']:
        name = cs['name']
        cases = sorted(e['case'] for e in man['plan']['queue'] if e['cohort'] == name)
        md = tmp_root / name
        (md / 'results').mkdir(parents=True)
        status = dict(schema=LWB.SCHEMA, cases={}, stop_after=STOP, harvest_dir=cs['harvest_dir'], cohort=cs['cohort'], runs=[])
        rows, tsv = {}, []
        cnt = collections.Counter()
        for c in cases:
            cdir = case_dir(root, c)
            wrec = read_json(cdir / 'worker.json')
            st = read_json(cdir / 'out' / 'status.json')
            rec = None
            if isinstance(st, dict):
                if st.get('schema') != LWB.SCHEMA:
                    structural.append(f'{c}: out/status.json schema {st.get("schema")!r} ≠ {LWB.SCHEMA}')
                if st.get('stop_after') != STOP:
                    structural.append(f'{c}: out/status.json stop_after {st.get("stop_after")!r} ≠ {STOP!r}')
                if str(st.get('harvest_dir')) != cs['harvest_dir'] or str(st.get('cohort')) != cs['cohort']:
                    structural.append(f'{c}: 수확 · 코호트 경로가 계획과 다르다 ({st.get("harvest_dir")} · {st.get("cohort")})')
                foreign = sorted(set(st.get('cases') or {}) - {c})
                if foreign:
                    structural.append(f'{c}: 케이스 폴더의 status.json 에 다른 케이스 기록 {foreign} — 두 번 셀 수 있다')
                rec = (st.get('cases') or {}).get(c)
                for r in st.get('runs') or []:
                    r2 = dict(r)
                    r2['case'] = c
                    status['runs'].append(r2)
                    if git_sha and r.get('git_sha') != git_sha:
                        mixed.append(f'{c}: 워커 코드 {str(r.get("git_sha"))[:9]} ≠ 발사 코드 {git_sha[:9]}')
            elif (cdir / 'out' / 'status.json').exists():
                anomalies.append(f'{c}: out/status.json 을 읽을 수 없다 (깨짐)')
            if rec is None:
                why0 = '발사되지 않았다 (중단 · 예산 대기 중 끝남)' if not wrec else ''
                rec = _synth_failed(c, cdir, wrec, why0)
                anomalies.append(f'{c}: 케이스 기록 없음 → failed 로 기록 ({rec["why"][:120]})')
            status['cases'][c] = rec
            s = rec.get('status') or 'UNKNOWN'
            cnt[s] += 1
            att = ((wrec or {}).get('attempts') or [None])[-1] or {}
            if att and s in KEEP and att.get('rc') not in (0, None):
                anomalies.append(f'{c}: 케이스는 {s} 인데 워커 rc {att.get("rc")} — 기록 뒤에 죽었다 (값은 기록 그대로)')
            if s not in KEEP:
                failures.append(dict(case=c, cohort=name, status=s, why=(rec.get('why') or '')[:300],
                                     failed_stages=rec.get('failed_stages') or []))
            mf = cdir / 'out' / 'metrics_flat.csv'
            if mf.exists():
                with open(mf, encoding='utf-8', newline='') as fh:
                    rr = list(csv.DictReader(fh))
                if len(rr) > 1 or any(r.get('case') != c for r in rr):
                    structural.append(f'{c}: out/metrics_flat.csv 에 다른 행 {[r.get("case") for r in rr]}')
                elif rr:
                    rows[c] = dict(rr[0])          # 빈 칸 ('') 도 그대로 — 머리 열 집합이 순차 배치와 같게 (selftest ⑧)
            #  τ 관문용 링크 — 결과가 없는 케이스도 빈 폴더 (tau_flux 가 NOT_COMPUTED 행을 낸다 · 빠지지 않는다)
            src = cdir / 'work' / 'results' / c
            dst = md / 'results' / c
            if src.is_dir():
                os.symlink(os.path.relpath(src, md / 'results'), dst)
            else:
                dst.mkdir()
                (dst / '_NO_RESULTS.txt').write_text(f'{c}: 케이스 결과 폴더가 없다 ({src}) — 상태 {s}\n', encoding='utf-8')
            tsv.append((c, name, s, '|'.join(map(str, rec.get('failed_stages') or [])), rec.get('network_run_id') or '',
                        len((wrec or {}).get('attempts') or []), att.get('rc', ''), att.get('signal') or '', att.get('wall_s', ''),
                        rec.get('elapsed_s', ''), att.get('peak_rss_mb', ''), att.get('est_mem_mb', ''), att.get('user_s', ''),
                        att.get('sys_s', ''), att.get('contacts', ''), str(cdir / 'log.txt')))
        status['parallel'] = dict(launcher=SCHEMA, manifest=str(root / 'manifest.json'), git_sha=git_sha,
                                  lanes=man.get('lanes'), network_lock=man.get('network_lock'), thread_env=THREAD_ENV,
                                  merged_at=report['merged_at'], n_cases=len(cases), counts=dict(cnt))
        LWB.write_outputs(md, status, rows)                     # 배치 자신의 writer (같은 직렬화 · 같은 열 규칙)
        with open(md / 'parallel_cases.tsv', 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh, delimiter='\t', lineterminator='\n')
            w.writerow(('case', 'cohort', 'status', 'failed_stages', 'network_run_id', 'attempts', 'rc', 'signal', 'wall_s',
                        'batch_elapsed_s', 'peak_rss_mb', 'est_mem_mb', 'user_s', 'sys_s', 'contacts', 'log'))
            w.writerows(tsv)
        walls = sorted(float(t[8]) for t in tsv if t[8] not in ('', None))
        rss = sorted(float(t[10]) for t in tsv if t[10] not in ('', None))
        ratio = sorted(float(t[10]) / float(t[11]) for t in tsv if t[10] not in ('', None) and t[11] not in ('', None, 0))

        def q(v, f):
            return round(v[min(len(v) - 1, int(f * len(v)))], 1) if v else None
        report['cohorts'][name] = dict(n=len(cases), counts=dict(cnt), n_rows=len(rows), wall_s=dict(median=q(walls, .5), p90=q(walls, .9),
                                       max=(walls[-1] if walls else None), sum=round(sum(walls), 1)),
                                       peak_rss_mb=dict(median=q(rss, .5), max=(rss[-1] if rss else None)),
                                       rss_over_est=dict(median=(round(q(ratio, .5), 3) if ratio else None),
                                                         max=(round(ratio[-1], 3) if ratio else None)))
    report.update(structural=structural, mixed_generation=mixed, anomalies=anomalies, failures=failures)
    if structural or (mixed and not allow_mixed):
        shutil.rmtree(tmp_root, ignore_errors=True)
        write_json(root / 'merge_report_REFUSED.json', report)
        out('⛔ merge 거부 — merged/ 를 바꾸지 않았다 (merge_report_REFUSED.json)')
        for s in structural[:20]:
            out(f'   구조: {s}')
        for s in mixed[:20]:
            out(f'   세대: {s}' + ('' if allow_mixed else '  (진짜 의도면 --allow-mixed-generation · 기록된다)'))
        return 2
    report['allow_mixed_generation'] = bool(allow_mixed and mixed)
    write_json(tmp_root / 'merge_report.json', report)
    final = root / 'merged'
    if final.exists():
        shutil.rmtree(final)
    os.replace(tmp_root, final)
    with contextlib.suppress(FileNotFoundError):
        (root / 'merge_report_REFUSED.json').unlink()
    print_merge_summary(root, report, man, out=out)
    return 0 if not failures and not anomalies and not mixed else 1


def print_merge_summary(root: Path, report: dict, man: dict, out=print):
    out(f'══ merge — {root / "merged"}')
    for name, r in report['cohorts'].items():
        out(f'  {name}: {r["n"]} 건 {r["counts"]} · 행 {r["n_rows"]} · 경과 중앙 {r["wall_s"]["median"]} s · p90 {r["wall_s"]["p90"]} s · '
            f'최대 {r["wall_s"]["max"]} s · 합 {r["wall_s"]["sum"]} s · 최대 RSS 중앙 {r["peak_rss_mb"]["median"]} MB · '
            f'최대 {r["peak_rss_mb"]["max"]} MB · 실측/추정 중앙 {r["rss_over_est"]["median"]} · 최대 {r["rss_over_est"]["max"]}')
    mi = meminfo()
    mx = max((r['peak_rss_mb']['max'] or 0) for r in report['cohorts'].values()) if report['cohorts'] else 0
    if mx and mi.get('MemTotal'):
        k = int(max(1, (mi['MemTotal'] / 2 ** 20 - 2048) // (mx + 100)))
        out(f'  메모리로 본 동시 상한 ≈ {k} 레인 (MemTotal {gib(mi["MemTotal"])} GB − 2 GB · 최대 케이스 {mx:.0f} MB + 부모 100 MB 가정)')
    for f in report['failures'][:40]:
        out(f'  ✗ {f["case"]} ({f["cohort"]}) {f["status"]} · {f["failed_stages"]} · {f["why"][:160]}')
    for a in report['anomalies'][:40]:
        out(f'  ⚠ {a}')
    for m in report['mixed_generation'][:10]:
        out(f'  ⚠ 세대: {m}')
    if report['code_changed_since_launch']:
        out(f'  ⚠ 발사 뒤 바뀐 코드 파일 (지금 트리 기준 — 실행 중 변경이면 위 세대 줄에 나온다): {report["code_changed_since_launch"]}')
    print_followups(root, man, out=out)


def print_followups(root: Path, man: dict, out=print):
    sha = ((man.get('git') or {}).get('short')) or 'SHA'
    d = time.strftime('%Y%m%d')
    names = [c['name'] for c in man['plan']['cohorts']]
    by = {c['name']: c for c in man['plan']['cohorts']}
    out('━━ 다음 명령 (리포 루트에서 · 그대로 복사) ━━')
    out(f'cd {shlex.quote(str(ROOT))}')
    out(f'mkdir -p {shlex.quote(str(root / "tau"))} {shlex.quote(str(root / "handover"))}')
    out('# ① τ 관문 — 모든 케이스 폴더 (실패 케이스도 NOT_COMPUTED 행으로 남는다 · 빠지지 않는다)')
    for n in names:
        out(f'python3 scripts/tau_flux.py {shlex.quote(str(root / "merged" / n / "results"))}/* '
            f'--tsv {shlex.quote(str(root / "tau" / f"{n}_tau_flux.tsv"))} --json {shlex.quote(str(root / "tau" / f"{n}_tau_flux.json"))}')
    out(f'# ② 인계 v1.2 — 생성기 (망 배치 = 접촉 단계 다섯 묶음 {HANDOVER_GROUPS} · RGL-03).  ⚠ τ (f · tau2 · tau) 는 아직 생성기 묶음이 아니다 —')
    out('#    v1.2 = 이 표 + ① 의 τ TSV (case 열로 잇기 = 남은 코드 단계 · Codex 뒤).  LW (④b) 열은 생성기가 명시 제외한다 (frame_unverified).')
    for n in names:
        c = by[n]
        extra = (f' --design {shlex.quote(c["design"])}' if c.get('design') else '')
        out(f'python3 scripts/lhs_design_dataset.py --export-handover {shlex.quote(str(root / "handover" / f"{n}_handover_v12_{d}.csv"))}'
            f'{extra} --harvest {shlex.quote(c["harvest_dir"])} --union {shlex.quote(c.get("union") or "")} '
            f'--webapp {shlex.quote(str(root / "merged" / n))} --webapp-groups {HANDOVER_GROUPS}')
    out('# ③ 보낼 묶음 (케이스 결과 원본 · 작업 폴더는 넣지 않는다)')
    out(f'(cd {shlex.quote(str(root))} && tar czf ~/net194_{sha}_{d}.tar.gz manifest.json runs progress.tsv merged/merge_report.json '
        'merged/*/status.json merged/*/metrics_flat.csv merged/*/parallel_cases.tsv tau handover cases/*/worker.json cases/*/log.txt)')


# ─────────────────────────────────── 명령 ───────────────────────────────────
def _guard_posix():
    if os.name != 'posix' or not hasattr(os, 'wait4'):
        raise LaunchError('이 실행기는 Linux/WSL 전용이다 (os.wait4 · 프로세스 묶음)')


def cmd_run(args) -> int:
    _guard_posix()
    root = Path(args.root).expanduser().resolve()
    if root.exists() and any(root.iterdir()):
        print(f'⛔ ROOT {root} 가 비어 있지 않다 — 새 ROOT 를 쓸 것 (이어서 돌리려면 retry · 다시 묶으려면 merge)', file=sys.stderr)
        return 2
    worker = Path(args.worker_script).resolve() if args.worker_script else BATCH
    plan = build_plan(args.cohorts.split(','), cohort_specs(args), args.case, args.order)
    mi = meminfo()
    if args.mem_budget_gb is None:
        budget_mb = (max(1.0, mi['MemAvailable'] / 2 ** 20 - args.mem_reserve_gb * 1024) if mi.get('MemAvailable') else None)
    else:
        budget_mb = args.mem_budget_gb * 1024 if args.mem_budget_gb > 0 else None
    pf = preflight(args, plan, root, budget_mb)
    print_preflight(pf, plan, args, root)
    q = plan['queue']
    print(f'══ 계획 — {len(q)} 건 · 순서 {plan["order"]} (접촉 수 큰 순 · 같으면 이름) · 레인 {args.lanes}')
    for i, e in enumerate(q[:5] + (q[-2:] if len(q) > 7 else [])):
        print(f'  {e["case"]:>10s} ({e["cohort"]}) 접촉 {e["contacts"]:>7d} · 추정 {e["est_mem_mb"]:.0f} MB · {e["est_time_s"]:.0f} s')
    cs0 = {c['name']: c for c in plan['cohorts']}
    ex = q[0]
    print('  케이스 명령 예:', shlex.join(case_cmd(args.python, worker, cs0[ex['cohort']], ex['case'], case_dir(root, ex['case']),
                                                args.root_from, args.root_to)))
    print(f'  cwd = 케이스 폴더 · env + {THREAD_ENV} · PYTHONDONTWRITEBYTECODE=1'
          + (' · TMPDIR = <케이스>/tmp' if args.network_lock == 'per-case' else ''))
    if worker != BATCH:
        print(f'  ⚠ 워커 대체 (시험용) — {worker}')
    if pf['stop']:
        print('⛔ 사전 점검 중단 — 위 ⛔ 를 해결할 것 (아무것도 띄우지 않았다)', file=sys.stderr)
        return 2
    n_pyc = purge_pyc(ROOT / 'scripts', dry=args.dry_run)
    if args.dry_run:
        print(f'══ --dry-run — 아무것도 쓰지 않았다 (scripts/__pycache__ pyc {n_pyc} 개는 본 실행 때 지운다)')
        return 0
    if not args.skip_batch_selftest:
        r = subprocess.run([str(args.python), str(BATCH), '--selftest'], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        if r.returncode != 0:
            print('⛔ lhs_webapp_batch --selftest 실패 — 띄우지 않는다\n' + (r.stdout or '')[-2000:], file=sys.stderr)
            return 2
        print('  lhs_webapp_batch --selftest 통과')
    root.mkdir(parents=True, exist_ok=True)
    with root_lock(root):
        man = dict(schema=SCHEMA, created=now_iso(), argv=sys.argv, repo_root=str(ROOT), python=str(args.python),
                   python_versions=python_versions(args.python), worker_script=str(worker), worker_override=(worker != BATCH),
                   stop_after=STOP, lanes=args.lanes, network_lock=args.network_lock, thread_env=THREAD_ENV,
                   mem_budget_mb=budget_mb, mem_reserve_gb=args.mem_reserve_gb, min_free_gb=args.min_free_gb,
                   mem_model=dict(base_mb=MEM_BASE_MB, per_kcontact_mb=MEM_PER_KCONTACT_MB, time_per_kcontact_s=TIME_PER_KCONTACT_S),
                   root_from=args.root_from, root_to=args.root_to, allow_dirty=args.allow_dirty,
                   allow_missing_raw=args.allow_missing_raw, pyc_purged=n_pyc, git=pf['git'], code_hashes=code_hashes(),
                   preflight={k: v for k, v in pf.items() if k != 'git'}, plan=plan, retries=[])
        write_json(root / 'manifest.json', man)
        rc = _run_and_merge(root, man, plan['queue'], args.lanes, budget_mb, args.min_free_gb, args.no_merge, run_label='run')
    return rc


def _run_and_merge(root, man, todo, lanes, budget_mb, min_free_gb, no_merge, run_label, allow_mixed=False) -> int:
    run_no = len(list((root / 'runs').glob('run_*.json'))) + 1
    h0 = code_hashes()
    t0 = now_iso()
    res = run_queue(root, man, todo, lanes, run_no, budget_mb=budget_mb, min_free_gb=min_free_gb)
    h1 = code_hashes()
    res.update(kind=run_label, started=t0, ended=now_iso(), lanes=lanes, mem_budget_mb=budget_mb, min_free_gb=min_free_gb,
               code_changed_during_run=sorted(k for k in h1 if h1[k] != h0.get(k)), git_sha_end=git_info()['sha'])
    write_json(root / 'runs' / f'run_{run_no:03d}.json', res)
    print(f'══ 실행 {run_no} 끝 — {res["outcomes"]} · {res["wall_h"]} h · 최대 동시 {res["max_concurrent"]} · '
          f'예산 대기 {res["budget_events"]} · backfill {res["backfills"]} · 메모리 바닥 대기 {res["events"]}'
          + (' · ⛔ 중단됨' if res['interrupted'] else ''))
    if res['code_changed_during_run']:
        print(f'⚠ 실행 중 코드 파일이 바뀌었다: {res["code_changed_during_run"]} — merge 는 세대 섞임으로 거부한다')
    if no_merge or res['interrupted']:
        if res['interrupted']:
            print('  중단된 실행은 자동 merge 하지 않는다 — retry 로 마저 돌리거나 merge 로 지금 상태를 묶는다')
        return 130 if res['interrupted'] else (0 if all(k in KEEP for k in res['outcomes']) else 1)
    return merge(root, allow_mixed=allow_mixed)


def _load_root(root: Path) -> dict:
    man = read_json(root / 'manifest.json')
    if not isinstance(man, dict) or man.get('schema') != SCHEMA:
        raise LaunchError(f'{root}/manifest.json 이 없거나 이 실행기의 것이 아니다')
    return man


def cmd_retry(args) -> int:
    _guard_posix()
    root = Path(args.root).expanduser().resolve()
    man = _load_root(root)
    g = git_info()
    if g['sha'] != (man.get('git') or {}).get('sha') and not args.allow_mixed_generation:
        print(f'⛔ 지금 코드 {g["short"]} ≠ 발사 코드 {man["git"]["short"]} — 섞인 세대가 된다 (진짜 의도면 --allow-mixed-generation)',
              file=sys.stderr)
        return 2
    want = set(args.case or ())
    todo, skip = [], []
    for e in man['plan']['queue']:
        if want and e['case'] not in want:
            continue
        cdir = case_dir(root, e['case'])
        pidrec = read_json(cdir / 'worker.pid.json')
        if pidrec and pid_alive(pidrec.get('pid'), e['case']):
            skip.append((e['case'], f'아직 도는 워커 pid {pidrec.get("pid")}'))
            continue
        s, _rec = _case_outcome(cdir, e['case'])
        if s in KEEP:
            continue
        todo.append(e)
    for c, why in skip:
        print(f'  건너뜀 {c}: {why}')
    print(f'══ retry — 다시 돌릴 케이스 {len(todo)} 건 (done · partial 아닌 것) · 레인 {args.lanes}')
    if not todo:
        return merge(root, allow_mixed=args.allow_mixed_generation) if not args.no_merge else 0
    mi = meminfo()
    if args.mem_budget_gb is None:
        budget_mb = (max(1.0, mi['MemAvailable'] / 2 ** 20 - args.mem_reserve_gb * 1024) if mi.get('MemAvailable') else None)
    else:
        budget_mb = args.mem_budget_gb * 1024 if args.mem_budget_gb > 0 else None
    print(f'  CPU {cpu_info()} · MemAvailable {gib(mi.get("MemAvailable"))} GB · 예산 {budget_mb and round(budget_mb / 1024, 1)} GB')
    purge_pyc(ROOT / 'scripts')
    with root_lock(root):
        man.setdefault('retries', []).append(dict(at=now_iso(), argv=sys.argv, lanes=args.lanes, cases=[e['case'] for e in todo],
                                                  git_sha=g['sha'], dirty=g['dirty']))
        write_json(root / 'manifest.json', man)
        rc = _run_and_merge(root, man, todo, args.lanes, budget_mb, args.min_free_gb, args.no_merge, run_label='retry',
                            allow_mixed=args.allow_mixed_generation)
    return rc


def cmd_merge(args) -> int:
    root = Path(args.root).expanduser().resolve()
    _load_root(root)
    with root_lock(root):
        return merge(root, allow_mixed=args.allow_mixed_generation)


def cmd_status(args) -> int:
    root = Path(args.root).expanduser().resolve()
    man = _load_root(root)
    cnt, running = collections.Counter(), []
    for e in man['plan']['queue']:
        cdir = case_dir(root, e['case'])
        pidrec = read_json(cdir / 'worker.pid.json')
        if pidrec and pid_alive(pidrec.get('pid'), e['case']):
            running.append(e['case'])
            cnt['running'] += 1
            continue
        s, _rec = _case_outcome(cdir, e['case'])
        w = read_json(cdir / 'worker.json')
        cnt[s or ('NO_RECORD' if w else 'pending')] += 1
    mi = meminfo()
    print(f'{root}: {dict(cnt)} · 도는 중 {running[:20]} · MemAvailable {gib(mi.get("MemAvailable"))} GB')
    return 0


def _parse(argv=None):
    ap = argparse.ArgumentParser(description='194 건 망 배치 병렬 실행기 (동적 큐 · 레인당 1 코어)')
    ap.add_argument('--selftest', action='store_true', help='가짜 워커로 계획 · 큐 · 기록 · merge 를 시험한다 (실제 파이프라인 없음)')
    sub = ap.add_subparsers(dest='cmd')

    def common_run(p):
        p.add_argument('-j', '--lanes', type=int, default=20, help='동시 케이스 수 (기본 20 · 1저자 "1코어 20개")')
        p.add_argument('--mem-budget-gb', type=float, default=None,
                       help='메모리 예산 (GB) — 추정 합이 넘으면 새 케이스를 기다린다 (기본 = MemAvailable − --mem-reserve-gb · 0 = 끔)')
        p.add_argument('--mem-reserve-gb', type=float, default=2.0, help='기본 예산에서 남겨 둘 메모리 (GB)')
        p.add_argument('--min-free-gb', type=float, default=1.0, help='실측 MemAvailable 이 이보다 작으면 새 케이스를 띄우지 않는다 (0 = 끔)')
        p.add_argument('--no-merge', action='store_true', help='끝나도 merge 하지 않는다')

    r = sub.add_parser('run', help='새 ROOT 에서 실행 (비어 있지 않으면 거부)')
    r.add_argument('--root', required=True)
    common_run(r)
    r.add_argument('--cohorts', default='lhs,lhsx', help='코호트 (쉼표) — lhs = 130 · lhsx = 64')
    r.add_argument('--case', action='append', default=[], help='이 케이스만 (여러 번 · 시범)')
    r.add_argument('--order', choices=['cost', 'name'], default='cost', help='큐 순서 — cost = 접촉 수 큰 순 (기본)')
    r.add_argument('--network-lock', choices=['per-case', 'shared'], default='per-case',
                   help='per-case = 케이스마다 TMPDIR (망 단계도 동시에 · 기본) · shared = 웹앱 lock 그대로 (망 단계는 하나씩)')
    r.add_argument('--python', default=sys.executable, help='워커 인터프리터 (기본 = 이 실행기를 돌린 것)')
    r.add_argument('--root-from', default='', help='코호트 경로 접두사 (lhs_webapp_batch 와 같은 뜻)')
    r.add_argument('--root-to', default='', help='실제 경로 접두사')
    for n in COHORT_SPECS:
        r.add_argument(f'--{n}-harvest', default='', help=f'{n} 수확 폴더 (기본 {COHORT_SPECS[n]["harvest"]})')
        r.add_argument(f'--{n}-cohort', default='', help=f'{n} 코호트 TSV (기본 {COHORT_SPECS[n]["cohort"]})')
    r.add_argument('--dry-run', action='store_true', help='사전 점검 · 계획 · 명령만 찍는다 (아무것도 안 쓴다)')
    r.add_argument('--allow-dirty', action='store_true', help='추적 파일이 바뀐 트리에서도 돈다 (manifest 에 남는다)')
    r.add_argument('--allow-missing-raw', action='store_true', help='원자료 · 메시가 없는 케이스가 있어도 돈다 (REFUSED 로 남는다)')
    r.add_argument('--skip-batch-selftest', action='store_true', help='발사 전 lhs_webapp_batch --selftest 를 건너뛴다')
    r.add_argument('--worker-script', default='', help=argparse.SUPPRESS)        # selftest 전용 (manifest 에 남는다)

    t = sub.add_parser('retry', help='done · partial 아닌 케이스만 같은 ROOT 에서 다시 (기록 보존)')
    t.add_argument('--root', required=True)
    common_run(t)
    t.add_argument('--case', action='append', default=[], help='이 케이스만')
    t.add_argument('--allow-mixed-generation', action='store_true', help='코드가 발사 때와 달라도 (기록된다)')

    m = sub.add_parser('merge', help='케이스별 산출을 코호트별 한 폴더로 (다시) 묶는다')
    m.add_argument('--root', required=True)
    m.add_argument('--allow-mixed-generation', action='store_true', help='워커 코드 sha 가 섞여도 묶는다 (기록된다)')

    s = sub.add_parser('status', help='진행 상황')
    s.add_argument('--root', required=True)
    return ap.parse_args(argv)


def main(argv=None) -> int:
    a = _parse(argv)
    if a.selftest:
        return _selftest()
    try:
        if a.cmd == 'run':
            return cmd_run(a)
        if a.cmd == 'retry':
            return cmd_retry(a)
        if a.cmd == 'merge':
            return cmd_merge(a)
        if a.cmd == 'status':
            return cmd_status(a)
    except LaunchError as e:
        print(f'⛔ {e}', file=sys.stderr)
        return 2
    _parse(['-h'])
    return 2


# ─────────────────────────────────── selftest ───────────────────────────────────
#: 가짜 워커 — **진짜 `lhs_webapp_batch.run_batch`** (스테이징 · sha · 프레임 관문 · status · metrics writer) 에 가짜 웹앱 의존만 넣는다.
#:   케이스마다 동작은 NP194_FAKE_PLAN (JSON) 이 정한다: ok · fail · crash (SIGKILL) · hang · sleep · alloc_mb · child_alloc_mb · extra · none_key.
FAKE_WORKER = r'''
import json, os, signal, subprocess, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.environ['NP194_REPO'], 'scripts'))
import lhs_webapp_batch as LWB
PLAN = json.load(open(os.environ['NP194_FAKE_PLAN']))
ENVK = ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS',
        'TMPDIR', 'PYTHONDONTWRITEBYTECODE')
def touch(n):
    b = bytearray(n << 20)
    for i in range(0, len(b), 4096):
        b[i] = 1
    return b
class FakeA:
    @staticmethod
    def detect_mode(case_dir):
        return 'bimodal'
    @staticmethod
    def run_pipeline(case, mode, tm, scale, figures=True, auto_db=True, **kw):
        b = PLAN.get(case) or {}
        rd = os.path.join(os.environ['WEBAPP_RESULTS_FOLDER'], case)
        os.makedirs(rd, exist_ok=True)
        e = {k: os.environ.get(k) for k in ENVK}
        e.update(cwd=os.getcwd(), stop_after=kw.get('stop_after'), figures=figures, auto_db=auto_db)
        json.dump(e, open(os.path.join(rd, '_env.json'), 'w'))
        if b.get('sleep'):
            time.sleep(b['sleep'])
        keep = touch(b['alloc_mb']) if b.get('alloc_mb') else None
        if b.get('child_alloc_mb'):
            subprocess.run([sys.executable, '-c', 'b = bytearray(%d << 20)\nfor i in range(0, len(b), 4096): b[i] = 1\n'
                            % b['child_alloc_mb']], check=True)
        if b.get('mode') == 'crash':
            os.kill(os.getpid(), signal.SIGKILL)
        if b.get('mode') == 'hang':
            time.sleep(3600)
        fm = {'se_se_cn': b.get('cn', 4.25), 'percolation_pct': b.get('perc', 97.0), 'porosity': 12.5}
        fm.update(b.get('extra') or {})
        if b.get('none_key'):
            fm['nullable_key'] = None
        json.dump(fm, open(os.path.join(rd, 'full_metrics.json'), 'w'))
        json.dump({'hertzian': {'sigma_full': 0.004}, 'physics': {'sigma_full': 0.004}},
                  open(os.path.join(rd, 'network_conductivity_dual.json'), 'w'))
        del keep
        st = 'failed' if b.get('mode') == 'fail' else 'done'
        return {'status': st, 'success': st != 'failed',
                'failed_stages': (['Network stop contract (stop_after=network)'] if st == 'failed' else []),
                'network_run_id': (None if st == 'failed' else 'RUN-' + case), 'log': [{'step': 'Parse', 'rc': 0, 'ok': True}]}
class FakeTMR:
    @staticmethod
    def resolve_from_files(deck_p, atom_p):
        return {1: 'AM_P', 2: 'AM_S', 3: 'SE'}, [], []
    @staticmethod
    def format_map(m):
        return ','.join(f'{t}:{m[t]}' for t in sorted(m))
class FakeEM:
    @staticmethod
    def row_for(rd):
        d = json.load(open(os.path.join(rd, 'full_metrics.json')))
        return {'case': os.path.basename(rd), **d}
sys.exit(LWB.run_batch(LWB._parse(sys.argv[1:]), (FakeA, FakeTMR, FakeEM)))
'''


def _selftest() -> int:
    fails = []

    def chk(name, ok, why=''):
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok or not why else f'  — {why}'))
        if not ok:
            fails.append(name)

    tmp = Path(tempfile.mkdtemp(prefix='np194_')).resolve()
    env_keep = {k: os.environ.get(k) for k in ('NP194_REPO', 'NP194_FAKE_PLAN', 'TMPDIR')}
    try:
        # ── 합성 코호트 두 개 (lhs · lhsx) — 진짜 배치 관문을 통과하는 원자료 · 수확 JSON (lhs_webapp_batch selftest 와 같은 모양) ──
        _CHD = 'ITEM: ENTRIES c_cpl[7] c_cpl[8] c_cpl[9] c_cpl[22] c_cpl[23]\n'
        C_OK = 'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ENTRIES\n2\n' + _CHD + '1 2 0 0.1 0.01\n2 3 1 0.1 0.02\n'
        A_OK = 'ITEM: TIMESTEP\n100\nITEM: ATOMS id type\n1 1\n2 2\n3 3\n'
        cases = {'lhs': ['lhs99_000', 'lhs99_001', 'lhs99_002', 'lhs99_003', 'lhs99_004', 'lhs99_005'],
                 'lhsx': ['lhsx_900', 'lhsx_901', 'lhsx_902']}
        contacts = {'lhs99_000': 500, 'lhs99_001': 900, 'lhs99_002': 300, 'lhs99_003': 700, 'lhs99_004': 900, 'lhs99_005': 100,
                    'lhsx_900': 800, 'lhsx_901': 50, 'lhsx_902': 600}
        specs = {}
        for fam, cl in cases.items():
            hd = tmp / 'data' / f'{fam}_harvest'
            hd.mkdir(parents=True)
            rows = []
            for c in cl:
                post = tmp / 'raw' / c / 'post'
                post.mkdir(parents=True)
                (post / 'atom_100.liggghts').write_text(A_OK)
                (post / 'contact_100.liggghts').write_text(C_OK)
                (post / 'mesh_100.stl').write_text(f'solid {c}\nendsolid\n')
                deck = tmp / 'raw' / c / f'input_{c}.liggghts'
                deck.write_text(f'# deck {c}\n')
                hj = dict(case=c, timestep=100, type_map={'1': 'AM_P', '2': 'AM_S', '3': 'SE'},
                          contact_scan=dict(n_rows_last=contacts[c]),
                          raw={k: dict(path=p.name, sha256=HB.sha256_of(p)) for k, p in
                               (('atom', post / 'atom_100.liggghts'), ('contact', post / 'contact_100.liggghts'),
                                ('mesh', post / 'mesh_100.stl'), ('deck', deck))})
                (hd / f'{c}.json').write_text(json.dumps(hj), encoding='utf-8')
                rows.append(f'{c}\tRAW_OK\t3\t{deck}\t{post / "atom_100.liggghts"}\t{post / "contact_100.liggghts"}\n')
            (hd / '_batch_summary.json').write_text('{}', encoding='utf-8')
            coh = tmp / 'data' / f'{fam}_cohort.tsv'
            coh.write_text('# 합성 코호트 (selftest)\ncase\tstatus\tn_types\tdeck\tatom_file\tcontact_file\n' + ''.join(rows),
                           encoding='utf-8')
            specs[fam] = dict(harvest=str(hd), cohort=str(coh), expect_n=len(cl), union='', design='')
        fake = tmp / 'fake_worker.py'
        fake.write_text(FAKE_WORKER, encoding='utf-8')
        plan_p = tmp / 'fake_plan.json'

        def set_plan(p):
            plan_p.write_text(json.dumps(p), encoding='utf-8')
        behav = {'lhs99_000': dict(sleep=0.6), 'lhs99_001': dict(mode='crash'), 'lhs99_002': dict(mode='fail'),
                 'lhs99_003': dict(alloc_mb=160, extra={'only_here': 1.5}), 'lhs99_004': dict(child_alloc_mb=220, none_key=True),
                 'lhs99_005': dict(sleep=0.3), 'lhsx_900': dict(sleep=0.5, extra={'x_only': 'a,b "q"'}), 'lhsx_901': {},
                 'lhsx_902': dict(sleep=0.2)}
        set_plan(behav)
        os.environ['NP194_REPO'] = str(ROOT)
        os.environ['NP194_FAKE_PLAN'] = str(plan_p)

        def args_for(root, *extra):
            argv = ['run', '--root', str(root), '--worker-script', str(fake), '--allow-dirty', '--skip-batch-selftest',
                    '--lhs-harvest', specs['lhs']['harvest'], '--lhs-cohort', specs['lhs']['cohort'],
                    '--lhsx-harvest', specs['lhsx']['harvest'], '--lhsx-cohort', specs['lhsx']['cohort'], *extra]
            return argv

        # ① 계획 — 결정적 · 전수 한 번 · 비용 큰 순 (같으면 이름)
        a1 = _parse(args_for(tmp / 'r_plan'))
        p1 = build_plan(['lhs', 'lhsx'], cohort_specs(a1))
        p2 = build_plan(['lhs', 'lhsx'], cohort_specs(a1))
        names = [e['case'] for e in p1['queue']]
        allc = sorted(c for cl in cases.values() for c in cl)
        chk('① 계획이 결정적 (두 번 같다) · 전 케이스 정확히 한 번 · 접촉 큰 순 (같으면 이름)',
            p1 == p2 and sorted(names) == allc and len(names) == len(set(names))
            and names[:3] == ['lhs99_001', 'lhs99_004', 'lhsx_900'], repr(names))
        chk('① --case 필터 · 없는 케이스는 계획 거부', _raises(lambda: build_plan(['lhs'], cohort_specs(a1), ['nope_000']), LaunchError)
            and [e['case'] for e in build_plan(['lhs', 'lhsx'], cohort_specs(a1), ['lhsx_901'])['queue']] == ['lhsx_901'])

        # ② 비어 있지 않은 ROOT 는 거부 (아무것도 안 쓴다)
        busy = tmp / 'busy'
        busy.mkdir()
        (busy / 'old.txt').write_text('x')
        rc2 = main(args_for(busy))
        chk('② 비어 있지 않은 ROOT → rc 2 · manifest 없음', rc2 == 2 and not (busy / 'manifest.json').exists())

        # ③ --dry-run — ROOT 를 만들지 않는다
        dry = tmp / 'dry'
        rc3 = main(args_for(dry, '--dry-run'))
        chk('③ --dry-run → rc 0 · ROOT 를 만들지 않는다', rc3 == 0 and not dry.exists())

        # ④–⑦ 본 실행 — 레인 3 · 가짜 워커 (crash 1 · fail 1 · 메모리 둘)
        R = tmp / 'run1'
        t0 = time.monotonic()
        rc4 = main(args_for(R, '-j', '3', '--mem-budget-gb', '0', '--min-free-gb', '0'))
        wall = time.monotonic() - t0
        man = read_json(R / 'manifest.json') or {}
        wk = {c: read_json(case_dir(R, c) / 'worker.json') or {} for c in allc}
        last = {c: ((w.get('attempts') or [{}])[-1]) for c, w in wk.items()}
        chk(f'④ 실패가 있으면 rc 1 (조용히 초록이 아니다) · 실행 {wall:.1f} s', rc4 == 1, f'rc={rc4}')
        chk('④ 케이스마다 worker.json — rc · 경과 · 최대 RSS (KB) · user/sys',
            all(isinstance(l.get('rc'), int) and l.get('wall_s', -1) > 0 and l.get('peak_rss_kb', 0) > 0
                and 'user_s' in l and 'sys_s' in l for l in last.values()), repr({c: (l.get('rc'), l.get('peak_rss_kb')) for c, l in last.items()}))
        chk('④ crash (SIGKILL) 케이스 = rc −9 · signal SIGKILL · outcome NO_RECORD',
            last['lhs99_001'].get('rc') == -9 and last['lhs99_001'].get('signal') == 'SIGKILL'
            and last['lhs99_001'].get('outcome') == 'NO_RECORD', repr(last['lhs99_001']))
        rss = {c: l.get('peak_rss_mb', 0) for c, l in last.items()}
        base = max(v for c, v in rss.items() if c not in ('lhs99_003', 'lhs99_004'))
        chk(f'④ 최대 RSS 는 케이스별 (누적 아님) — 160 MB 할당 {rss["lhs99_003"]:.0f} · 자식 220 MB {rss["lhs99_004"]:.0f} · 나머지 최대 {base:.0f}',
            rss['lhs99_003'] >= 150 and rss['lhs99_004'] >= 210 and base < 140)
        iv = sorted((l['t_start_s'], l['t_end_s']) for l in last.values())
        mx = max(sum(1 for s, e in iv if s <= t < e) for t, _ in iv)
        chk(f'⑤ 동적 큐 — 동시 실행 최대 {mx} (≥ 2 · ≤ 레인 3)', 2 <= mx <= 3)
        envs = {c: read_json(case_dir(R, c) / 'work' / 'results' / c / '_env.json') for c in allc if c != 'lhs99_001'}
        ok6 = all(e and all(e.get(k) == '1' for k in THREAD_ENV) and e.get('PYTHONDONTWRITEBYTECODE') == '1'
                  and e.get('TMPDIR') == str(case_dir(R, c) / 'tmp') and e.get('cwd') == str(case_dir(R, c))
                  and e.get('stop_after') == 'network' and e.get('figures') is False and e.get('auto_db') is False
                  for c, e in envs.items())
        chk('⑥ 워커 환경 — 스레드 다섯 = 1 · PYTHONDONTWRITEBYTECODE · TMPDIR = 케이스/tmp · cwd = 케이스 폴더 · stop_after network · 그림/DB 끔',
            ok6, repr(next(iter(envs.values()))))
        ms = {f: read_json(R / 'merged' / f / 'status.json') or {} for f in cases}
        chk('⑦ merged 코호트별 status — schema · stop_after network · 케이스 집합 = 계획 (정확히)',
            all(ms[f].get('schema') == LWB.SCHEMA and ms[f].get('stop_after') == 'network'
                and sorted(ms[f].get('cases') or {}) == sorted(cases[f]) for f in cases))
        r_crash = (ms['lhs'].get('cases') or {}).get('lhs99_001') or {}
        chk('⑦ ★ 죽은 워커 케이스가 빠지지 않는다 — status failed · 사유에 rc −9 (SIGKILL) · 합성 표지',
            r_crash.get('status') == 'failed' and 'SIGKILL' in str(r_crash.get('why')) and r_crash.get('parallel_synthesized') is True,
            repr(r_crash))
        rep = read_json(R / 'merged' / 'merge_report.json') or {}
        chk('⑦ merge_report — 실패 둘 (crash · fail) 이 실패 목록에 · 구조 이상 0',
            sorted(f['case'] for f in rep.get('failures') or []) == ['lhs99_001', 'lhs99_002'] and not rep.get('structural'),
            repr(rep.get('failures')))

        # ⑧ 같은 케이스를 순차 배치 한 번 (같은 가짜 워커 · crash 제외) 으로 돌린 산출과 바이트 대조
        seq_out, seq_work = tmp / 'seq_out', tmp / 'seq_work'
        argv = [sys.executable, str(fake), '--stop-after', 'network', '--harvest-dir', specs['lhs']['harvest'],
                '--cohort', specs['lhs']['cohort'], '--work', str(seq_work), '--out-dir', str(seq_out)]
        for c in cases['lhs']:
            if c != 'lhs99_001':
                argv += ['--case', c]
        subprocess.run(argv, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True)
        a_csv = (R / 'merged' / 'lhs' / 'metrics_flat.csv').read_bytes()
        b_csv = (seq_out / 'metrics_flat.csv').read_bytes() if (seq_out / 'metrics_flat.csv').exists() else b''
        chk('⑧ ★ merged metrics_flat.csv = 순차 배치 한 번의 metrics_flat.csv (바이트 · 열 순서 · 빈 칸 · 따옴표)', a_csv == b_csv and len(a_csv) > 0,
            f'{len(a_csv)} B vs {len(b_csv)} B')
        seq_st = read_json(seq_out / 'status.json') or {}

        def strip_t(rec):
            return {k: v for k, v in (rec or {}).items() if k not in ('when', 'elapsed_s')}
        same_rec = all(strip_t(ms['lhs']['cases'][c]) == strip_t((seq_st.get('cases') or {}).get(c))
                       for c in cases['lhs'] if c != 'lhs99_001')
        chk('⑧ status 케이스 기록 = 순차 배치 (시각 · 경과 빼고)', same_rec)

        # ⑨ 인계 생성기의 실제 읽기 함수가 merged 를 받는다
        import lhs_design_dataset as LDD
        try:
            wv = LDD.load_webapp(R / 'merged' / 'lhs')
            ok9 = (wv.get('stop_after') == 'network' and sorted(wv['status']) == sorted(cases['lhs'])
                   and sorted(wv['rows']) == sorted(c for c in cases['lhs'] if c != 'lhs99_001'))
            why9 = f"{wv.get('stop_after')} · {sorted(wv['rows'])}"
        except Exception as e:                              # noqa: BLE001
            ok9, why9 = False, f'{type(e).__name__}: {e}'
        chk('⑨ lhs_design_dataset.load_webapp(merged) — 거부 없음 · stop_after network · 상태 전 케이스 · 행 = 기록 있는 케이스', ok9, why9)

        # ⑩ τ 관문 입력 — results/<case> 가 전 케이스에 있다 (없는 케이스 = 빈 폴더 → NOT_COMPUTED 행)
        import tau_flux as TF
        trs = {c: TF.case_row(str(R / 'merged' / 'lhs' / 'results' / c)) for c in cases['lhs']}
        chk('⑩ τ 관문 — merged/lhs/results/<case> 전 케이스 · case 이름 = 폴더 이름 · 죽은 케이스도 행 (NOT_COMPUTED)',
            all(trs[c]['case'] == c for c in trs) and trs['lhs99_001'].get('ion_net_status_hertz') == 'NOT_COMPUTED'
            and (R / 'merged' / 'lhs' / 'results' / 'lhs99_000').is_symlink(), repr(trs['lhs99_001'].get('ion_net_status_hertz')))

        # ⑪ 세대 섞임 — 한 케이스의 워커 코드 sha 를 바꾸면 merge 거부 (rc 2 · merged 그대로) · 허용하면 rc 1 + 기록
        stp = case_dir(R, 'lhs99_000') / 'out' / 'status.json'
        st0 = stp.read_text(encoding='utf-8')
        st = json.loads(st0)
        st['runs'][-1]['git_sha'] = 'f' * 40
        stp.write_text(json.dumps(st), encoding='utf-8')
        before = (R / 'merged' / 'lhs' / 'status.json').read_bytes()
        rc11 = merge(R, out=lambda *a, **k: None)
        chk('⑪ ★ 워커 코드 sha 가 다르면 merge 거부 (rc 2) · merged 는 그대로 · 거부 보고 파일',
            rc11 == 2 and (R / 'merged' / 'lhs' / 'status.json').read_bytes() == before and (R / 'merge_report_REFUSED.json').exists())
        rc11b = merge(R, allow_mixed=True, out=lambda *a, **k: None)
        rep11 = read_json(R / 'merged' / 'merge_report.json') or {}
        chk('⑪ --allow-mixed-generation → rc 1 · 섞임이 보고에 남는다', rc11b == 1 and rep11.get('mixed_generation')
            and rep11.get('allow_mixed_generation') is True)
        stp.write_text(st0, encoding='utf-8')

        # ⑫ 남의 케이스 기록 — 케이스 폴더 status.json 에 다른 케이스가 있으면 구조 이상 (rc 2)
        st = json.loads(st0)
        st['cases']['lhs99_005'] = dict(case='lhs99_005', status='done')
        stp.write_text(json.dumps(st), encoding='utf-8')
        rc12 = merge(R, out=lambda *a, **k: None)
        rep12 = read_json(R / 'merge_report_REFUSED.json') or {}
        chk('⑫ ★ 케이스 폴더에 다른 케이스 기록 → merge 거부 (두 번 세지 않는다)', rc12 == 2
            and any('다른 케이스' in s for s in rep12.get('structural') or []))
        stp.write_text(st0, encoding='utf-8')

        # ⑬ retry — 실패 · 죽은 케이스만 다시 (기록이 쌓인다) → 전부 done · merge rc 0
        behav2 = dict(behav)
        behav2['lhs99_001'] = {}
        behav2['lhs99_002'] = {}
        set_plan(behav2)
        rc13 = main(['retry', '--root', str(R), '-j', '2', '--mem-budget-gb', '0', '--min-free-gb', '0'])
        wk13 = {c: read_json(case_dir(R, c) / 'worker.json') or {} for c in allc}
        n_att = {c: len(w.get('attempts') or []) for c, w in wk13.items()}
        ms13 = read_json(R / 'merged' / 'lhs' / 'status.json') or {}
        chk('⑬ retry — 실패 둘만 다시 (시도 2) · 나머지 그대로 (시도 1) · merge rc 0 · 전부 done',
            rc13 == 0 and n_att['lhs99_001'] == 2 and n_att['lhs99_002'] == 2
            and all(n_att[c] == 1 for c in allc if c not in ('lhs99_001', 'lhs99_002'))
            and all((ms13.get('cases') or {}).get(c, {}).get('status') == 'done' for c in cases['lhs']), repr((rc13, n_att)))
        set_plan(behav)

        # ⑭ shared lock — TMPDIR 을 바꾸지 않는다
        os.environ['TMPDIR'] = str(tmp / 'shared_tmp')
        (tmp / 'shared_tmp').mkdir()
        R14 = tmp / 'run_shared'
        main(args_for(R14, '-j', '2', '--case', 'lhsx_901', '--network-lock', 'shared', '--mem-budget-gb', '0', '--min-free-gb', '0'))
        e14 = read_json(case_dir(R14, 'lhsx_901') / 'work' / 'results' / 'lhsx_901' / '_env.json') or {}
        chk('⑭ --network-lock shared → 워커 TMPDIR = 실행기의 TMPDIR (웹앱 lock 공유)', e14.get('TMPDIR') == str(tmp / 'shared_tmp'),
            repr(e14.get('TMPDIR')))
        if env_keep['TMPDIR'] is None:
            os.environ.pop('TMPDIR', None)
        else:
            os.environ['TMPDIR'] = env_keep['TMPDIR']

        # ⑮ 중단 — 실행기에 SIGINT → 도는 워커 (프로세스 묶음) 를 끄고 'interrupted' 로 기록 · 고아 없음 · merge 는 그 케이스를 failed 로
        set_plan({'lhsx_900': dict(mode='hang'), 'lhsx_902': dict(mode='hang')})
        R15 = tmp / 'run_int'
        p = subprocess.Popen([sys.executable, str(Path(__file__).resolve())] + args_for(
            R15, '-j', '2', '--cohorts', 'lhsx', '--case', 'lhsx_900', '--case', 'lhsx_902', '--mem-budget-gb', '0', '--min-free-gb', '0'),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        pids, deadline = {}, time.monotonic() + 60
        while time.monotonic() < deadline and len(pids) < 2:
            for c in ('lhsx_900', 'lhsx_902'):
                pr = read_json(case_dir(R15, c) / 'worker.pid.json')
                if pr and (case_dir(R15, c) / 'work' / 'results' / c / '_env.json').exists():
                    pids[c] = pr['pid']
            time.sleep(0.2)
        os.kill(p.pid, signal.SIGINT)
        rc15 = p.wait(timeout=90)
        alive = [c for c, pid in pids.items() if pid_alive(pid, c)]
        o15 = {c: ((read_json(case_dir(R15, c) / 'worker.json') or {}).get('attempts') or [{}])[-1].get('outcome') for c in pids}
        chk(f'⑮ ★ 중단 — rc 130 · 두 워커 interrupted · 살아 있는 워커 0 ({len(pids)} 개 관측)',
            rc15 == 130 and len(pids) == 2 and not alive and set(o15.values()) == {'interrupted'}, repr((rc15, o15, alive)))
        rc15m = merge(R15, out=lambda *a, **k: None)
        ms15 = read_json(R15 / 'merged' / 'lhsx' / 'status.json') or {}
        chk('⑮ 중단 뒤 merge → rc 1 · 두 케이스 failed (빠지지 않는다)', rc15m == 1
            and all((ms15.get('cases') or {}).get(c, {}).get('status') == 'failed' for c in ('lhsx_900', 'lhsx_902')))
        set_plan(behav)

        # ⑯ 메모리 관문 — 실측 바닥을 터무니없이 높이면 한 번에 하나 (돌고 있는 게 없으면 늘 하나는 띄운다) · 대기 기록
        R16 = tmp / 'run_mem'
        main(args_for(R16, '-j', '3', '--cohorts', 'lhsx', '--mem-budget-gb', '0', '--min-free-gb', '1000000'))
        run16 = read_json(R16 / 'runs' / 'run_001.json') or {}
        chk('⑯ --min-free-gb 바닥 → 최대 동시 1 · 대기 기록 · 전부 끝남',
            run16.get('max_concurrent') == 1 and run16.get('events', 0) >= 1 and run16.get('finished') == 3, repr(run16))
        # ⑰ 메모리 예산 — 추정 합이 예산을 넘으면 기다린다 (backfill 은 작은 것 먼저 · 앞 케이스 굶김 방지)
        R17 = tmp / 'run_budget'
        budget_gb = (est_mem_mb(800) + est_mem_mb(600)) / 1024 * 0.999          # lhsx_900 + lhsx_902 는 함께 못 든다
        main(args_for(R17, '-j', '3', '--cohorts', 'lhsx', '--mem-budget-gb', f'{budget_gb:.6f}', '--min-free-gb', '0'))
        w17 = {c: ((read_json(case_dir(R17, c) / 'worker.json') or {}).get('attempts') or [{}])[-1] for c in cases['lhsx']}
        a, b = w17['lhsx_900'], w17['lhsx_902']
        overlap = a.get('t_start_s', 0) < b.get('t_end_s', 0) and b.get('t_start_s', 0) < a.get('t_end_s', 0)
        run17 = read_json(R17 / 'runs' / 'run_001.json') or {}
        chk('⑰ 메모리 예산 — 함께 못 드는 두 케이스는 겹치지 않는다 · 작은 케이스는 backfill · 전부 끝남',
            not overlap and run17.get('finished') == 3 and run17.get('backfills', 0) >= 1, repr((overlap, run17)))

        # ⑱ pyc 정리 — 같은 glob (scripts/__pycache__/*.pyc) 만 지운다 · dry 는 세기만
        sd = tmp / 'fake_scripts'
        (sd / '__pycache__').mkdir(parents=True)
        for n in ('a.cpython-311.pyc', 'b.cpython-311.pyc'):
            (sd / '__pycache__' / n).write_bytes(b'x')
        (sd / '__pycache__' / 'keep.txt').write_text('x')
        n_dry = purge_pyc(sd, dry=True)
        n_real = purge_pyc(sd)
        chk('⑱ pyc 정리 — dry 는 세기만 (2) · 본 정리 2 개 · 다른 파일은 그대로',
            n_dry == 2 and n_real == 2 and not list((sd / '__pycache__').glob('*.pyc')) and (sd / '__pycache__' / 'keep.txt').exists())
        # ⑲ manifest — 재현에 필요한 것
        chk('⑲ manifest — git · 코드 해시 · 스레드 · lock · 레인 · 계획 큐 · 워커 대체 표지',
            man.get('schema') == SCHEMA and man.get('git', {}).get('sha') and man.get('code_hashes', {}).get('webapp/app.py')
            and man.get('thread_env') == THREAD_ENV and man.get('network_lock') == 'per-case' and man.get('lanes') == 3
            and len(man.get('plan', {}).get('queue') or []) == len(allc) and man.get('worker_override') is True)
    finally:
        for k, v in env_keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{"✓ 전부 통과" if not fails else f"✗ {len(fails)} 건 실패"}')
    return 0 if not fails else 1


def _raises(fn, exc) -> bool:
    try:
        fn()
    except exc:
        return True
    except Exception:                                       # noqa: BLE001
        return False
    return False


if __name__ == '__main__':
    sys.exit(main())

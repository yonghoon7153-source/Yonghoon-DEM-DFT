#!/usr/bin/env python3
"""SLURM 으로 띄운 LH 의 **시작 대조** — 러너 (run_lh.sbatch) 가 LIGGGHTS 를 부르기 **직전**에 돈다 (2026-09-28).

왜: 1저자 결정 (09-28) 으로 LH 를 ibb SLURM (20 코어 × 3) 에서 돌린다.  로컬 발사는 봉인 (launch_record.json) 바로 뒤에 exec
  해서 틈이 없다 (Codex Q5 "실행 직전").  SLURM 은 제출과 시작 사이에 **대기열 틈**이 있어 그 사이 덱 · STL · 바이너리 · 러너가
  바뀔 수 있다.  ⇒ job 이 시작하면 봉인을 **다시** 대조하고, 하나라도 다르면 LIGGGHTS 를 부르지 않는다 (exit 3).
  통과 기록 = <런>/job_start.json — 검사기 (scripts/check_contact_validity.py launch_binding) 가 SLURM 봉인이면 이것까지 이어 본다.
  거부 기록 = <런>/job_start.refused.<job id>.json (통과 기록을 **덮지 않는다** — 두 번째 시작이 첫 실행의 증거를 지우지 않게).

대조 (전부 서야 통과):
  봉인 스키마 · backend = slurm · 바이너리 (러너가 부를 절대경로) realpath = 봉인 · sha256 = 봉인 ·
  in.mixer · Drum/Front/Back.stl sha256 = 봉인 · **실행 중인 러너 자신** (SLURM 이 제출 때 복사해 둔 사본 = 러너의 "$0") sha256 =
  봉인의 러너 sha256 · 이 대조기 자신의 sha256 = 봉인 · SLURM_NTASKS = 봉인 np (SLURM 밖이면 거부) ·
  log.lmp · job_start.json 이 아직 없다 (두 번 뜨지 않는다).

사용 (러너 안 — launch_highbo.sh 가 쓴다):  python3 start_check.py <런 폴더> <바이너리 절대경로> "$SELF"
셀프테스트: dem_scripts/mixer_20260921/test_launcher.sh HS③–③h (가짜 mpirun · 가짜 바이너리로 러너를 실제로 돌린다).
표준 라이브러리만 쓴다 (ibb 의 어느 python3 에서도 돈다).
"""
import hashlib
import json
import os
import platform
import socket
import sys
import time
from datetime import datetime, timezone

SCHEMA = 'mixer_highbo_job_start/1'
LAUNCH_SCHEMA = 'mixer_highbo_launch_record/1'
FILES = ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _sha_or_none(p):
    try:
        return sha(p)
    except OSError:
        return None


def check(d, lmp, runner, env):
    """→ (기록 dict, 사유 목록).  사유가 비어야 통과."""
    why = []
    lp = os.path.join(d, 'launch_record.json')
    try:
        with open(lp, encoding='utf-8') as f:
            lr = json.load(f)
    except (OSError, ValueError) as e:
        lr = None
        why.append(f'봉인 (launch_record.json) 을 읽을 수 없다 ({type(e).__name__})')
    if not isinstance(lr, dict):
        lr = {}
    if lr and lr.get('schema') != LAUNCH_SCHEMA:
        why.append(f'봉인 스키마 {lr.get("schema")!r} ≠ {LAUNCH_SCHEMA}')
    if lr and lr.get('backend') != 'slurm':
        why.append(f'봉인 backend = {lr.get("backend")!r} (slurm 이어야 — 이 대조기는 SLURM 러너 전용)')
    sl = lr.get('slurm') if isinstance(lr.get('slurm'), dict) else {}
    lmp_real = os.path.realpath(lmp)
    lmp_sha = _sha_or_none(lmp)
    if lr and lmp_real != lr.get('lmp_realpath'):
        why.append(f'바이너리 경로 {lmp_real} ≠ 봉인 {lr.get("lmp_realpath")}')
    if lr and (lmp_sha is None or lmp_sha != lr.get('lmp_sha256')):
        why.append(f'바이너리 sha256 {str(lmp_sha)[:12]}… ≠ 봉인 {str(lr.get("lmp_sha256"))[:12]}… (제출 뒤 다시 빌드됐거나 다른 파일)')
    want = lr.get('sha256') if isinstance(lr.get('sha256'), dict) else {}
    got = {f: _sha_or_none(os.path.join(d, f)) for f in FILES}
    changed = [f for f in FILES if got[f] is None or got[f] != want.get(f)]
    if lr and changed:
        why.append(f'제출 뒤 바뀌었거나 없는 파일 {changed}')
    run_sha = _sha_or_none(runner)
    if lr and (run_sha is None or run_sha != sl.get('runner_sha256')):
        why.append(f'실행 중인 러너 sha256 {str(run_sha)[:12]}… ≠ 봉인한 러너 {str(sl.get("runner_sha256"))[:12]}… (제출 뒤 러너 수정)')
    me = _sha_or_none(os.path.abspath(__file__))
    if lr and me != sl.get('start_check_sha256'):
        why.append(f'이 시작 대조기 sha256 {str(me)[:12]}… ≠ 봉인 {str(sl.get("start_check_sha256"))[:12]}…')
    nt = env.get('SLURM_NTASKS')
    try:
        nt_i = int(nt) if nt is not None else None
    except ValueError:
        nt_i = None
    if nt_i is None:
        why.append('SLURM_NTASKS 없음 — SLURM job 밖에서 러너를 돌렸다 (sbatch 로만)')
    elif lr and nt_i != sl.get('np'):
        why.append(f'SLURM_NTASKS {nt_i} ≠ 봉인 np {sl.get("np")} (#SBATCH -n ↔ mpirun -np 짝)')
    for f in ('log.lmp', 'job_start.json'):
        if os.path.exists(os.path.join(d, f)):
            why.append(f'{f} 가 이미 있다 — 이 런은 이미 시작됐다 (두 번 뜨지 않는다 · 재개는 resume 절차로)')
    now = time.time()
    rec = {
        'schema': SCHEMA, 'ok': not why, 'reasons': why,
        'run': os.path.basename(os.path.normpath(d)),
        'time_local': datetime.fromtimestamp(now).astimezone().isoformat(timespec='seconds'),
        'time_utc': datetime.fromtimestamp(now, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'hostname': socket.gethostname(), 'platform': platform.platform(),
        'slurm_job_id': env.get('SLURM_JOB_ID'), 'slurm_ntasks': nt_i,
        'slurm_nodelist': env.get('SLURM_JOB_NODELIST') or env.get('SLURM_NODELIST'),
        'lmp_path': lmp, 'lmp_realpath': lmp_real, 'lmp_sha256': lmp_sha,
        'runner_executed': runner, 'runner_sha256_executed': run_sha,
        'start_check_sha256': me,
        'launch_record_sha256': _sha_or_none(lp),
        'sha256': got,
    }
    return rec, why


def main(argv, env=None):
    env = os.environ if env is None else env
    if len(argv) != 3:
        print('사용: python3 start_check.py <런 폴더> <바이너리 절대경로> <실행 중인 러너 ($0)>', file=sys.stderr)
        return 2
    d, lmp, runner = argv
    rec, why = check(d, lmp, runner, env)
    name = 'job_start.json' if not why else f'job_start.refused.{env.get("SLURM_JOB_ID") or int(time.time())}.json'
    tmp = os.path.join(d, '.' + name + '.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
        f.write('\n')
    os.replace(tmp, os.path.join(d, name))
    if why:
        print('⛔ 시작 대조 실패 — LIGGGHTS 를 부르지 않는다 (' + name + ')')
        for w in why:
            print('   ✗ ' + w)
        return 3
    print(f'✓ 시작 대조 통과 — {rec["run"]} · job {rec["slurm_job_id"]} · ntasks {rec["slurm_ntasks"]} · '
          f'lmp {rec["lmp_sha256"][:12]}… · 러너 {rec["runner_sha256_executed"][:12]}… → job_start.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))

"""One author-operated PRECAL_N0 development wave on the approved B deployment."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tarfile
import time

base = runpy.run_path(str(Path(__file__).with_name('mixer_e0_pilot_ibb.py')))
need, sha, put, read, ref = (base[k] for k in ('need', 'sha', 'put', 'read', 'ref'))
CASE = 'PRECAL_N0'
WALL = '2-00:00:00'
PIN_B = '8231f395cda98fed8dbbf5422ccda003b11a8da9'
A_B_RETURN = '6f7f407479af6282b9c8d4e83afa86645d4fda1506b29801be2165dcc2965737'
DECK_SHA = 'adbbc8fa8f46730779fbf4f028f95a7aaf90c27ef2697c0dbe21a9ae1b5c6de3'


def rotation_deck(raw):
    need(hashlib.sha256(raw).hexdigest() == DECK_SHA, 'rotation deck identity')
    text = '\n'.join(line for line in raw.decode('utf-8').splitlines() if not line.lstrip().startswith('#'))
    need('dump dmp all custom 32976 post/mix_*.liggghts' in text and
         text.count('%.17g') == 10 and 'run 6595382' in text, 'rotation contract')


def authority():
    return dict(author_action='GO_N0_ONCE', allowed_to_submit=[CASE], execution_authorized=True,
                label='DEVELOPMENT_DATA_ONLY', previous_job='366423',
                development_qualification_accepted=True, paper_qualification=False,
                e0_W9_at_T9=False, known_limitation='MXE0-02', automatic_retry=False)


def wall_limits(qos, assoc, part, user):
    seconds = base['wall_seconds']
    q = [line.rstrip().split('|') for line in qos.splitlines() if line.strip()]
    need(len(q) == 1 and len(q[0]) >= 2 and q[0][0] == 'cpu-60' and
         (not q[0][1] or seconds(q[0][1]) >= seconds(WALL)), 'N0 QoS wall')
    rows = [line.split('|') for line in assoc.splitlines()]
    need(any(len(r) >= 3 and r[0] == user and 'cpu-60' in r[1].split(',') and
             seconds(r[2]) >= seconds(WALL) for r in rows), 'N0 association wall')
    fields = dict(re.findall(r'(\w+)=([^\s]+)', part))
    need(fields.get('State') == 'UP' and seconds(fields.get('MaxTime', '')) >= seconds(WALL),
         'N0 partition wall')


def frames_ok(names):
    expected = {'mix_%d.liggghts' % (i * 32976) for i in range(1, 235)}
    return len(names) == len(expected) and set(names) == expected


def completed(acct, jid, end):
    row = base['terminal'](acct, jid)
    return bool(row and row['state'] == 'COMPLETED' and row['exit_code'] == '0:0'
                and end and end.get('job_id') == jid and type(end.get('returncode')) is int
                and end['returncode'] == 0)


def prepare(root, binary, mpi, prefix):
    manifest = base['verify_deployment'](root)
    need(manifest['source_pin'] == PIN_B and manifest['approved_return_sha256'] == A_B_RETURN,
         'approved B identity')
    here = root / 'B' / base['F8']
    inputs = here / 'planned_assets' / CASE
    rotation_deck((inputs / 'in.mixer').read_bytes())
    folder = here / 'approvals' / CASE
    case = here / 'cases' / CASE
    folder.mkdir(parents=True)
    case.mkdir(parents=True)
    authority_file = root / 'control/n0_author_go.json'
    put(authority_file, authority())
    for name in ('in.mixer', 'deck_meta.json', 'Drum.stl', 'Front.stl', 'Back.stl'):
        shutil.copyfile(inputs / name, case / name)
    put(here / 'campaign_policy.json', base['policy'](str(here), sha(authority_file)))
    put(folder / 'policy.json', dict(policy_id='N0_DEVELOPMENT_20261118',
                                     execution_authorized=True, allowed_to_submit=[CASE]))
    put(folder / 'qualification.json', authority())
    put(folder / 'mxd2r_disposition.json', dict(wave=[CASE], previous_job='366423',
                                               scope='single development rotation'))
    paths = [root / 'B' / base['safe_rel'](r['path']) for r in manifest['files']]
    paths.extend(case.iterdir())
    python = Path(sys.executable).resolve(strict=True)
    paths.extend([python, Path(__file__).resolve(), Path(__file__).with_name('mixer_e0_pilot_ibb.py'),
                  root / 'control/rotation_pin.json', root / 'control/runtime_reference.json',
                  root / 'control/AB_RECEIPT.json', root / 'B_manifest.json'])
    put(folder / 'source_manifest.json', {'files': [ref(p) for p in paths]})
    # Collect the same baseline live-CPU, storage/inode, quota and pre-run runtime receipts as E0.
    # Separately record the development acceptance for this N0 only.
    user = os.environ['USER']
    wall_dir = root / 'evidence/n0_wall'
    query = base['capture']
    qos, _ = query(wall_dir, 'qos', ['sacctmgr', '-n', '-P', 'show', 'qos', 'cpu-60',
                                     'format=Name,MaxWall'])
    assoc, _ = query(wall_dir, 'assoc', ['sacctmgr', '-n', '-P', 'show', 'assoc', 'user=' + user,
                                        'format=User,QOS,MaxWall'])
    part, _ = query(wall_dir, 'partition', ['scontrol', 'show', 'partition', 'cpu', '-o'])
    wall_limits(qos, assoc, part, user)
    live = base['preflight'](root, binary, mpi, prefix)
    live.update(qualification_accepted=True, qualification_scope='E0_DEVELOPMENT_ONLY',
                e0_W9_at_T9=False, previous_job='366423')
    live_path = root / 'evidence/n0_live_preflight.json'
    put(live_path, live)
    approval = dict(schema='mixer_first8_execution_approval/1', execution_authorized=True,
                    gate='MAP_CASE_GO', case=CASE, np=20, case_dir=str(case),
                    author_choices_confirmed=True, approved_concurrency=1, wave_release=[CASE],
                    runner_reviewed=True, walltime_approved=True, source_root=str(root / 'B'),
                    source_pin=PIN_B, minimum_free_bytes=base['FREE_BYTES'],
                    minimum_free_inodes=base['FREE_INODES'], author_go=ref(authority_file),
                    campaign_policy=ref(here / 'campaign_policy.json'), binary=ref(binary),
                    mpi_launcher=ref(mpi), qualification=ref(folder / 'qualification.json'),
                    mxd2r_disposition=ref(folder / 'mxd2r_disposition.json'), policy=ref(folder / 'policy.json'),
                    source_manifest=ref(folder / 'source_manifest.json'), live_preflight=ref(live_path))
    approval['runner_bindings'] = dict(python=str(python), job_start=str(here / 'job_start.py.txt'),
                                       stdout=str(case / 'slurm.stdout'), stderr=str(case / 'slurm.stderr'),
                                       walltime=WALL)
    submit = here / 'submit_one.py.txt'
    ap = folder / 'approval.json'
    runner = folder / 'runner.sbatch'
    runner.write_text(runpy.run_path(str(submit))['canonical_runner'](approval, str(ap)), encoding='utf-8')
    approval['runner'] = ref(runner)
    put(ap, approval)
    return submit, ap


def account(jid):
    cmd = base['command'](['sacct', '-n', '-P', '-j', jid, '--format=JobIDRaw,State,ExitCode,Elapsed,Start,End'])
    need(cmd.returncode == 0, 'sacct failed')
    return cmd.stdout


def monitor(case, jid):
    deadline = time.monotonic() + 4 * 86400
    missing_since = None
    while time.monotonic() < deadline:
        queue = base['command'](['squeue', '-h', '-j', jid, '-o', '%T'])
        need(queue.returncode == 0 or base['squeue_reports_absent'](queue), 'squeue query failed')
        if not queue.stdout.strip():
            acct = account(jid)
            if base['terminal'](acct, jid):
                return acct
            if missing_since is None:
                missing_since = time.monotonic()
            need(time.monotonic() - missing_since < 600, 'terminal accounting unavailable')
        else:
            missing_since = None
        print('JOB_ID=' + jid, 'QUEUE=' + queue.stdout.strip(),
              'FRAMES=' + str(sum(1 for _ in (case / 'post').glob('mix_*.liggghts'))), flush=True)
        time.sleep(45)
    raise ValueError('monitor time limit; operator may use collect-only after termination')


def collect(root, case, jid, acct, binary, mpi, prefix):
    terminal = base['terminal'](acct, jid)
    need(terminal is not None, 'job is not accounted terminal')
    attempt = 'collection_%d' % time.time_ns()
    runtime_match = None
    runtime_error = None
    try:
        runtime_match = base['runtime'](root, binary, mpi, prefix, attempt + '_post')['matches']
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        runtime_error = str(error)
    end = read(case / 'job_end.json') if (case / 'job_end.json').is_file() else None
    names = [p.name for p in (case / 'post').glob('mix_*.liggghts')]
    frames = frames_ok(names)
    ready = bool(completed(acct, jid, end) and frames and runtime_match)
    result = root.parent / attempt
    result.mkdir()
    record = dict(label='DEVELOPMENT_DATA_ONLY', case=CASE, job_id=jid, scheduler=terminal,
                  runner_rc=end.get('returncode') if end else None, frame_count=len(names),
                  exact_frame_names=frames, post_runtime_matches=runtime_match,
                  post_runtime_error=runtime_error, post_runtime_collected_unix=time.time(),
                  job_end_unix=end.get('end_unix') if end else None, return_ready=ready)
    put(root / 'evidence' / (attempt + '.json'), record)
    with tarfile.open(result / 'n0_full_result.tar.gz', 'x:gz', compresslevel=1) as tar:
        for p in sorted(case.rglob('*')):
            need(not p.is_symlink() and (p.is_dir() or p.is_file()), 'nonregular result member')
            if p.is_file():
                tar.add(p, arcname=CASE + '/' + p.relative_to(case).as_posix(), recursive=False)
    with tarfile.open(result / 'n0_report.tar.gz', 'x:gz', compresslevel=1) as tar:
        for name in ('control/rotation_pin.json', 'control/n0_author_go.json', 'B_manifest.json', 'evidence'):
            tar.add(root / name, arcname=name)
        here = root / 'B' / base['F8']
        for name in ('campaign_policy.json', 'admission', 'approvals'):
            tar.add(here / name, arcname=name)
    with (result / 'SHA256SUMS').open('x', encoding='ascii') as sums:
        for name in ('n0_report.tar.gz', 'n0_full_result.tar.gz'):
            sums.write(sha(result / name) + '  ' + name + '\n')
    # Only the first completed archive attempt gets the immutable return pointer.
    put(root.parent / 'return.json', dict(directory=attempt, **record))
    print('RUNNER_RC=%s FRAME_COUNT=%d RETURN_READY=%s' %
          (record['runner_rc'], len(names), str(ready).upper()), flush=True)
    return 0 if ready else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('GO_N0_ONCE', 'collect'))
    parser.add_argument('--root', type=Path, required=True)
    for key in ('binary', 'mpi', 'prefix'):
        parser.add_argument('--' + key, type=Path, required=True)
    args = parser.parse_args()
    root, binary, mpi, prefix = [p.resolve(strict=True) for p in (args.root, args.binary, args.mpi, args.prefix)]
    need(sys.platform.startswith('linux'), 'Linux host required')
    need(not any(k.startswith(('SBATCH_', 'SLURM_', 'SALLOC_', 'SRUN_')) for k in os.environ),
         'inherited scheduler options/allocation')
    keep = {k: os.environ[k] for k in ('PATH', 'HOME', 'USER', 'LOGNAME', 'LANG', 'LC_ALL', 'TMPDIR') if k in os.environ}
    os.environ.clear()
    os.environ.update(keep)
    pin = read(root / 'control/rotation_pin.json')
    need(re.fullmatch('[0-9a-f]{40}', pin['commit']) and
         sha(__file__) == pin['controller_sha256'] and
         sha(Path(__file__).with_name('mixer_e0_pilot_ibb.py')) == pin['helper_sha256'], 'controller pins')
    case = root / 'B' / base['F8'] / 'cases' / CASE
    if args.mode == 'GO_N0_ONCE':
        put(root / 'evidence/one_attempt.json', authority())
        submit, ap = prepare(root, binary, mpi, prefix)
        reply = base['command']([sys.executable, '-I', '-B', str(submit), str(ap)], 90)
        put(root / 'evidence/n0_submit.json', dict(rc=reply.returncode, stdout=reply.stdout, stderr=reply.stderr))
        print('SUBMIT_RC=%s' % reply.returncode, flush=True)
        need(reply.returncode == 0, 'submission failed/uncertain; inspect receipt')
    receipt = read(case / 'submission.receipt.json')
    jid = str(receipt['job_id'])
    need(receipt.get('case') == CASE and receipt['state'] == 'SUBMITTED' and re.fullmatch('[1-9][0-9]*', jid),
         'no confirmed N0 job ID')
    print('JOB_ID=' + jid, flush=True)
    acct = monitor(case, jid) if args.mode == 'GO_N0_ONCE' else account(jid)
    return collect(root, case, jid, acct, binary, mpi, prefix)


if __name__ == '__main__':
    raise SystemExit(main())


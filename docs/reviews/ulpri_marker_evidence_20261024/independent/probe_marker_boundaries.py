#!/usr/bin/env python3
"""Independent synthetic arm-CLI marker probes. Never invokes LIGGGHTS or MPI."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
repo, out = args.repo.resolve(), args.output.resolve()
out.mkdir(parents=True)
kit = repo / 'docs/data/ps45_unload_20261009'
sys.dont_write_bytecode = True
sys.path.insert(0, str(kit))
import ul_reader as u
import make_unload_decks as mk

P = u.ul_lib.load_params()
results = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def initial(name):
    root = out / name
    root.mkdir()
    ds, trace = u._ut_trace_arm(str(root), P, 4)
    u._fake_restored(str(root), u.B73)
    u._w(str(root / u.B73 / 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
    return root, Path(ds), trace


def read_cli(name, root, d, expected, expected_rho=None):
    inputs = [d / f'ul_{n}.csv' for n in ('events', 'windows', 'steps')]
    inputs += [d / 'run_manifest.txt'] + list((d / 'restart').glob('state_*.in'))
    before = {str(p.relative_to(d)): sha(p) for p in inputs}
    run = u.read_run(str(d), P)
    cmd = [sys.executable, '-I', '-B', str(kit / 'ul_reader.py'), 'arm', str(root), u.B73, 'UT']
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    (root / 'cli.log').write_text(proc.stdout + proc.stderr)
    verdict = json.loads((d / 'arm_verdict.json').read_text())
    unchanged = before == {str(p.relative_to(d)): sha(p) for p in inputs}
    if expected == 'reject':
        valid = (run['resume_auth'] == [] and run['n_superseded_rows'] == 0
                 and bool(run['problems']) and verdict['primary_status'] == 'UNIDENTIFIED'
                 and verdict['rho_pct'] is None and verdict['rank_eligible'] is False)
    else:
        valid = (bool(run['resume_auth']) and not run['problems']
                 and verdict['primary_status'] == 'OK' and verdict['rank_eligible'] is True
                 and (expected_rho is None or verdict['rho_pct'] == expected_rho))
    result = {'name': name, 'expected': expected, 'pass': valid and unchanged and proc.returncode == 0,
              'resume_auth': run['resume_auth'], 'superseded_rows': run['n_superseded_rows'],
              'problems': run['problems'], 'primary_status': verdict['primary_status'],
              'rho_pct': verdict['rho_pct'], 'rank_eligible': verdict['rank_eligible'],
              'csv_manifest_state_unchanged': unchanged, 'cli_rc': proc.returncode,
              'input_sha256': before, 'expected_rho_pct': expected_rho}
    results.append(result)
    return result


def stale(name, event=None, k='1.49', manifest_append=None):
    root, d, _ = initial(name)
    step = u._hold_resume(str(d), P, old_nw=2, auth=True, kr=1)
    if event is not None:
        path = d / 'ul_events.csv'
        with path.open(newline='') as f:
            rows = list(csv.DictReader(f))
        extra = dict(next(r for r in rows if r['event'] == 'RESUME'))
        extra.update(event=event, k=k)
        rows.append(extra)
        with path.open('w', newline='') as f:
            writer = csv.DictWriter(f, P['records']['events_cols'], lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    if manifest_append is not None:
        path = d / 'run_manifest.txt'
        path.write_bytes(path.read_bytes() + manifest_append.replace('{step}', str(step)).encode())
    return root, d


for boundary in range(4):
    for newline_name, newline in [('lf', b'\n'), ('crlf', b'\r\n'), ('cr', b'\r')]:
        name = f'positive_k{boundary}_{newline_name}'
        root, d, trace = initial(name)
        plain = u.arm_verdict(str(d), u.B73, 'UT', P, root=str(root))
        row = dict(zip(P['records']['steps_cols'], trace['steps'][boundary]))
        step = int(row['step'])
        state = {'ul_rstep': step, 'ul_k': boundary, 'ul_phase': 0 if boundary < 2 else 1,
                 'ul_modeB': int(boundary > 0), 'ul_pz': float(row['plate_z']), 'ul_lift': float(row['lift']),
                 'ul_ncross': max(0, boundary - 2), 'ul_xk': -1 if boundary < 2 else 2,
                 'ul_lk0': 11, 'ul_Pbar': float(row['Pbar']), 'ul_kind': row['kind']}

        def observe(k, w, phase, s):
            return {'P': {None: .16, 0: .16, 1: .0012, 2: .0008, 3: .0006, 4: .0004}.get(k, .0002),
                    'Kt': 1e-7, 'Kr': 1e-8, 'Kti': 1e-7, 'nc': 1, 'na': 160417, 'lk': 11}

        resumed = mk.deck_sim(mk.render(u.B73, 'UT', P), observe, step, state=state, cli={'ul_resume': '1'})
        for kind in ('windows', 'steps', 'events'):
            cols = P['records'][kind + '_cols']
            step_index = cols.index('step')
            rows = [r for r in trace[kind] if int(r[step_index]) <= step] + resumed[kind]
            raw = ','.join(cols) + '\n' + ''.join(','.join(r) + '\n' for r in rows)
            (d / f'ul_{kind}.csv').write_bytes(raw.encode().replace(b'\n', newline))
        manifest = (f'bed={u.B73}\njob=UT\nresume=1\ngate=RESUME\nstart=a2\nresume_from={step}\n'
                    'stage=UT screen=screen_a2.txt rc=0 check=PASS\nreader_arm_rc=0\nend=a2 fails=0 reader_rc=0\n')
        (d / 'run_manifest.txt').write_bytes(manifest.encode().replace(b'\n', newline))
        state_text = ''.join(f'variable {k} {"string" if isinstance(v, str) else "equal"} {v}\n' for k, v in state.items())
        (d / 'restart' / f'state_unload_{step}.in').write_bytes(state_text.encode().replace(b'\n', newline))
        read_cli(name, root, d, 'accept', plain['rho_pct'])

for char in (' ', '\t', '\u00a0', '\u2003', '\u202f', '\x1f'):
    for side in ('prefix', 'suffix'):
        for k in ('1', '1.49'):
            name = f'event_{ord(char):04x}_{side}_{k.replace(".", "p")}'
            marker = char + 'RESUME' if side == 'prefix' else 'RESUME' + char
            root, d = stale(name, event=marker, k=k)
            read_cli(name, root, d, 'reject')

for separator in ('\x0b', '\x0c', '\x1c', '\x1d', '\x1e', '\x85', '\u2028', '\u2029'):
    for position, extra in [('prefix', separator + 'resume_from={step}.49\n'),
                            ('after_key', 'resume_from={step}' + separator + '#tail\n'),
                            ('between_text_key', 'note=old' + separator + 'resume_from={step}.49\n')]:
        name = f'manifest_{ord(separator):04x}_{position}'
        root, d = stale(name, manifest_append=extra)
        read_cli(name, root, d, 'reject')

for event in ('UNKNOWN', 'resume'):
    name = 'unchanged_unrelated_event_' + event
    root, d = stale(name, event=event)
    read_cli(name, root, d, 'accept')

report = {'scope': 'Synthetic actual arm CLI; no physical qualification or launch',
          'reader_sha256': sha(kit / 'ul_reader.py'), 'case_count': len(results),
          'passed': sum(r['pass'] for r in results), 'status': 'PASS' if all(r['pass'] for r in results) else 'FAIL',
          'synthetic': True, 'physical_runs': 0, 'cases': results}
(out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ('status', 'case_count', 'passed', 'reader_sha256')}))
raise SystemExit(0 if report['status'] == 'PASS' else 1)

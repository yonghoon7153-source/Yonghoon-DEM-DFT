#!/usr/bin/env python3
"""Synthetic marker-integrity regressions through the actual ULPR arm CLI.

Only a new --out directory is written. No LIGGGHTS, MPI, Git writes or real
restart is performed. The exact reader SHA and separate case observations are
recorded; rc=0 from the arm CLI is never treated as an acceptance verdict.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    kit = repo / 'docs/data/ps45_unload_20261009'
    out.mkdir(parents=True, exist_ok=False)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(kit))
    u = importlib.import_module('ul_reader')
    mk = importlib.import_module('make_unload_decks')
    assert Path(u.__file__).resolve() == kit / 'ul_reader.py'
    P = u.ul_lib.load_params()
    reader_hash = digest(kit / 'ul_reader.py')
    cases = []

    def new_trace(root):
        root.mkdir()
        d, trace = u._ut_trace_arm(str(root), P, 4)
        u._fake_restored(str(root), u.B73)
        u._w(str(root / u.B73 / 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
        return Path(d), trace

    def capture(name, root, expected, boundary, expected_rho, expected_dropped):
        d = root / u.B73 / 'UT'
        paths = [d / f'ul_{part}.csv' for part in ('events', 'windows', 'steps')]
        paths += [d / 'run_manifest.txt', *sorted((d / 'restart').glob('state_unload_*.in'))]
        before = {p.relative_to(root).as_posix(): digest(p) for p in paths}
        read = u.read_run(str(d), P)
        command = [sys.executable, '-I', '-X', 'utf8', '-B', str(kit / 'ul_reader.py'),
                   'arm', str(root), u.B73, 'UT']
        completed = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', timeout=30)
        (root / 'cli.log').write_text(completed.stdout + completed.stderr, encoding='utf-8')
        verdict = json.loads((d / 'arm_verdict.json').read_text(encoding='utf-8'))
        after = {p.relative_to(root).as_posix(): digest(p) for p in paths}
        accepted = (read['resume_auth'] == [tuple(boundary)] and not read['problems']
                    and read['n_superseded_rows'] == expected_dropped
                    and verdict['primary_status'] == 'OK' and verdict['rank_eligible'] is True
                    and verdict['rho_pct'] == expected_rho)
        rejected = (read['resume_auth'] == [] and bool(read['problems'])
                    and read['n_superseded_rows'] == 0
                    and verdict['primary_status'] == 'UNIDENTIFIED'
                    and verdict['rho_pct'] is None and verdict['rank_eligible'] is False)
        row = {'case': name, 'expected': expected, 'boundary': boundary,
               'resume_auth': read['resume_auth'], 'n_superseded_rows': read['n_superseded_rows'],
               'problems': read['problems'], 'primary_status': verdict['primary_status'],
               'rho_pct': verdict['rho_pct'], 'rank_eligible': verdict['rank_eligible'],
               'input_hashes_before': before, 'input_hashes_after': after,
               'input_bytes_unchanged': before == after, 'cli_rc': completed.returncode,
               'expected_rho': expected_rho if expected == 'accept' else None,
               'pass': completed.returncode == 0 and before == after
                       and (accepted if expected == 'accept' else rejected)}
        cases.append(row)
        print(f'{"PASS" if row["pass"] else "FAIL"} {name}: {row["primary_status"]}, '
              f'auth={row["resume_auth"]}, removed={row["n_superseded_rows"]}', flush=True)

    # A deck-flow fixture with stale rows from the interrupted attempt. This is
    # the same physical-observation fixture for each lexical mutation.
    base = out / '_stale_template'
    d, trace = new_trace(base)
    plain = u.arm_verdict(str(d), u.B73, 'UT', P, root=str(base))
    assert plain['primary_status'] == 'OK'
    rho = plain['rho_pct']
    step = u._hold_resume(str(d), P, old_nw=2, auth=True, kr=1)
    template_inputs = {p.relative_to(base).as_posix(): digest(p) for p in base.rglob('*') if p.is_file()}

    def stale_case(name, edit=None, expected='reject'):
        root = out / name
        shutil.copytree(base, root)
        arm = root / u.B73 / 'UT'
        if edit:
            edit(arm)
        capture(name, root, expected, [1, step], rho, 5)

    def add_event(d, marker):
        p = d / 'ul_events.csv'
        rows = list(csv.DictReader(p.read_text(encoding='utf-8').splitlines()))
        row = dict(next(r for r in rows if r['event'] == 'RESUME'))
        row.update(event=marker, k='1.49')
        rows.append(row)
        columns = P['records']['events_cols']
        p.write_text(','.join(columns) + '\n' + ''.join(','.join(r[c] for c in columns) + '\n'
                                                       for r in rows), encoding='utf-8')

    stale_case('normal_stale_control', expected='accept')
    markers = [('literal_fractional', 'RESUME'), ('event_trailing_space', 'RESUME '),
               ('event_leading_space', ' RESUME'), ('event_trailing_tab', 'RESUME\t'),
               ('event_leading_tab', '\tRESUME'), ('event_trailing_nbsp', 'RESUME\u00a0'),
               ('event_leading_nbsp', '\u00a0RESUME'), ('event_trailing_emspace', 'RESUME\u2003'),
               ('event_leading_emspace', '\u2003RESUME'), ('event_both_spaces', ' RESUME ')]
    for name, marker in markers:
        stale_case(name, lambda arm, token=marker: add_event(arm, token))

    separators = [('vt', '\x0b'), ('ff', '\x0c'), ('fs', '\x1c'), ('gs', '\x1d'),
                  ('rs', '\x1e'), ('nel', '\x85'), ('ls', '\u2028'), ('ps', '\u2029')]
    for label, sep in separators:
        texts = {'front': f'{sep}resume_from={step}.49\n',
                 'after_key': f'resume_from={step}{sep}note=old\n',
                 'embedded': f'note=old{sep}resume_from={step}.49\n'}
        for position, text in texts.items():
            def append_manifest(arm, raw=text.encode('utf-8')):
                p = arm / 'run_manifest.txt'
                p.write_bytes(p.read_bytes() + raw)
            stale_case(f'manifest_{label}_{position}', append_manifest)

    for name, ending in [('lf', b'\n'), ('crlf', b'\r\n'), ('cr', b'\r')]:
        def replace_endings(arm, newline=ending):
            paths = [arm / 'run_manifest.txt', *sorted((arm / 'restart').glob('state_unload_*.in'))]
            for p in paths:
                p.write_bytes(p.read_bytes().replace(b'\n', newline))
        stale_case(f'normal_{name}_line_endings', replace_endings, 'accept')

    def remove_bad_again(arm):
        p = arm / 'ul_events.csv'
        original = p.read_bytes()
        add_event(arm, 'RESUME ')
        p.write_bytes(original)
    stale_case('removed_bad_row_control', remove_bad_again, 'accept')

    # True producer-deck simulated continuations at each permitted boundary,
    # compared numerically with their uninterrupted synthetic trace.
    for kr in range(4):
        root = out / f'normal_k{kr}'
        d, uninterrupted = new_trace(root)
        plain = u.arm_verdict(str(d), u.B73, 'UT', P, root=str(root))
        columns = P['records']['steps_cols']
        row = dict(zip(columns, uninterrupted['steps'][kr]))
        sr = int(row['step'])
        state = {'ul_rstep': sr, 'ul_k': kr, 'ul_phase': 0 if kr < 2 else 1,
                 'ul_modeB': int(kr > 0), 'ul_pz': float(row['plate_z']), 'ul_lift': float(row['lift']),
                 'ul_ncross': max(0, kr - 2), 'ul_xk': -1 if kr < 2 else 2, 'ul_lk0': 11,
                 'ul_Pbar': float(row['Pbar']), 'ul_kind': row['kind']}
        def observe(k, w, phase, sim_step):
            return {'P': {None: .16, 0: .16, 1: .0012, 2: .0008, 3: .0006, 4: .0004}.get(k, .0002),
                    'Kt': 1e-7, 'Kr': 1e-8, 'Kti': 1e-7, 'nc': 1, 'na': 160417, 'lk': 11}
        continued = mk.deck_sim(mk.render(u.B73, 'UT', P), observe, sr, state=state, cli={'ul_resume': '1'})
        assert continued['result'] == 'RM_STOP'
        for part in ('windows', 'steps', 'events'):
            cc = P['records'][part + '_cols']
            index = cc.index('step')
            rows = [x for x in uninterrupted[part] if int(x[index]) <= sr] + continued[part]
            (d / f'ul_{part}.csv').write_text(','.join(cc) + '\n' + ''.join(','.join(x) + '\n' for x in rows), encoding='utf-8')
        (d / 'run_manifest.txt').write_text(
            f'bed={u.B73}\njob=UT\nresume=0\ngate=ALLOW\nstart=a1\nend=a1 fails=1 reader_rc=0\n'
            f'resume=1\ngate=RESUME\nstart=a2\nresume_from={sr}\nstage=UT screen=screen_a2.txt rc=0 check=PASS\n'
            'reader_arm_rc=0\nend=a2 fails=0 reader_rc=0\n', encoding='utf-8')
        (d / 'restart' / f'state_unload_{sr}.in').write_text(''.join(
            f'variable {key} {"string" if isinstance(value, str) else "equal"} {value}\n'
            for key, value in state.items()), encoding='utf-8')
        capture(f'normal_k{kr}', root, 'accept', [kr, sr], plain['rho_pct'], 0)

    assert digest(kit / 'ul_reader.py') == reader_hash
    assert template_inputs == {p.relative_to(base).as_posix(): digest(p) for p in base.rglob('*') if p.is_file()}
    report = {'schema': 'ulpri_marker_cli_regressions_v1', 'synthetic': True,
              'reader_sha256': reader_hash, 'harness_sha256': digest(Path(__file__)),
              'case_count': len(cases), 'passed': sum(r['pass'] for r in cases),
              'positive_count': sum(r['expected'] == 'accept' for r in cases),
              'negative_count': sum(r['expected'] == 'reject' for r in cases),
              'status': 'PASS' if all(r['pass'] for r in cases) else 'FAIL',
              'physical_runs': 0, 'cases': cases}
    (out / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('status', 'case_count', 'passed', 'positive_count', 'negative_count')}))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())

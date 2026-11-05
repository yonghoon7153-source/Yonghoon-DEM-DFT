"""Document-scoped static evidence. Generates fixed deck bytes in memory only.

No prepare validator, DEM, source CLI, full gate, or tests are run. The command
parser and timeline arithmetic below are independent of saved audit/annotation
and the project's readback implementation. Output is evidence JSON, never decks.
"""
import decimal
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / 'input'
OUTPUT = ROOT / 'task/damping_static/static_probe.json'
sys.path.insert(0, str(INPUT / 'scripts'))
import mixer_precal_prepare as prepare

D = decimal.Decimal


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    return {p.relative_to(INPUT).as_posix(): sha(p)
            for p in sorted(INPUT.rglob('*')) if p.is_file()}


before = snapshot()
attempted_forbidden = []


def guard(event, args):
    # Generation is allowed only to read source. Deny execution/network and
    # filesystem writes while the source-to-bytes reconstruction is in flight.
    forbidden = event in ('subprocess.Popen', 'os.system', 'os.spawn',
                          'socket.connect', 'socket.bind', 'os.mkdir', 'os.remove',
                          'os.rmdir', 'os.rename')
    if event == 'open':
        mode, flags = args[1], args[2]
        forbidden = bool(isinstance(mode, str) and any(x in mode for x in 'wax+'))
        forbidden |= bool(isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        # Only this probe's final JSON write is authorized, after generation.
        if forbidden and str(args[0]).replace('\\', '/') == str(OUTPUT).replace('\\', '/') and not generating:
            forbidden = False
    if forbidden:
        attempted_forbidden.append({'event': event, 'args': repr(args)})
        raise RuntimeError('Static probe denied side effect: ' + event)


generating = True
sys.addaudithook(guard)


def commands(deck):
    pending = ''
    first = None
    rows = []
    for lineno, physical in enumerate(deck.decode('utf-8').splitlines(), 1):
        # All generated # occurrences outside quoted strings are comments.
        lexer = shlex.shlex(physical, posix=True)
        lexer.whitespace_split = True
        lexer.commenters = '#'
        tokens = list(lexer)
        if not tokens:
            continue
        first = first if first is not None else lineno
        more = tokens[-1] == '&'
        if more:
            tokens.pop()
        pending += (' ' if pending else '') + shlex.join(tokens)
        if not more:
            values = shlex.split(pending)
            rows.append({'line_start': first, 'line_end': lineno,
                         'tokens': values, 'command': ' '.join(values)})
            pending, first = '', None
    assert not pending, 'unterminated continuation'
    return rows


records = []
for case_id in prepare.CASE_IDS:
    # _generate only: do not rerun PRE8 readback, regression, or full gate.
    item = prepare._generate(case_id)
    deck, meta = item['deck'], item['meta']
    cmds = commands(deck)
    fixes, active, runs, unfixes, restarts = [], {}, [], [], []
    step = 0
    for row in cmds:
        t = row['tokens']
        if t[0] == 'fix':
            info = dict(line=row['line_start'], command=row['command'],
                        id=t[1], group=t[2], style=t[3])
            fixes.append(info)
            active[t[1]] = info
        elif t[0] == 'unfix':
            removed = active.pop(t[1])
            unfixes.append(dict(line=row['line_start'], command=row['command'],
                                step=step, removed_style=removed['style']))
        elif t[0] == 'run':
            assert len(t) == 2 and t[1].isdigit(), t
            count = int(t[1])
            runs.append(dict(line=row['line_start'], command=row['command'], steps=count,
                             before=step, after=step + count,
                             active_rotation=[v['id'] for v in active.values() if v['style'] == 'move/mesh'],
                             active_viscous=[v['id'] for v in active.values() if v['style'].startswith('viscous')],
                             active_insertion=[v['id'] for v in active.values() if v['style'] == 'insert/pack']))
            step += count
        elif t[0] == 'write_restart':
            restarts.append(dict(line=row['line_start'], command=row['command'], step=step))
    dt = D(next(r['tokens'][1] for r in cmds if r['tokens'][0] == 'timestep'))
    dump = next(r for r in cmds if r['tokens'][:2] == ['dump', 'dmp'])
    interval = int(dump['tokens'][4])
    assert len(runs) == 4
    settle_steps = runs[1]['steps'] + runs[2]['steps']
    t0 = settle_steps // interval * interval
    boundary = restarts[0]['step']
    for row in runs:
        row.update(duration_seconds=str(row['steps'] * dt),
                   before_seconds=str(row['before'] * dt), after_seconds=str(row['after'] * dt))
    controls = [r for r in cmds if r['tokens'][0] in (
        'include', 'jump', 'if', 'label', 'python', 'reset_timestep', 'read_restart', 'read_data', 'variable')]
    candidate_commands = [r for r in cmds if any(
        word in r['command'].lower() for word in ('viscous', 'servo', 'halt', 'pressure', 'stress', 'aveforce'))]
    properties = {}
    for row in cmds:
        t = row['tokens']
        if len(t) > 4 and t[0] == 'fix' and t[3] == 'property/global':
            properties[t[4]] = {'line': row['line_start'], 'command': row['command'], 'values': t[7:] if t[5] == 'peratomtypepair' else t[6:]}
    evidence = [dict(line=r['line_start'], command=r['command']) for r in cmds
                if r['tokens'][0] in ('units', 'timestep', 'pair_style', 'dump', 'dump_modify', 'thermo_style', 'compute')]
    records.append(dict(
        case_id=case_id, role=item['role'], deck_sha256=hashlib.sha256(deck).hexdigest(), deck_bytes=len(deck),
        metadata_sha_binding_matches=meta['deck_sha256'] == hashlib.sha256(deck).hexdigest(),
        fix_inventory=fixes, run_timeline=runs, unfix_timeline=unfixes,
        settled_restart_boundaries=restarts, pressure_or_stop_candidates=candidate_commands,
        dynamic_or_external_control_commands=controls,
        properties=properties, evidence_commands=evidence,
        time=dict(dt_printed_seconds=str(dt), dt_rule_seconds=meta['dt']['rule_s'],
                  inserted_steps=runs[0]['steps'], settling_run_steps=settle_steps,
                  settling_duration_seconds=str(settle_steps * dt),
                  t0_planned_step=t0, t0_planned_seconds=str(t0 * dt),
                  t0_formula='floor((run2 + run3) / dump_interval) * dump_interval',
                  settled_write_restart_step=boundary, settled_write_restart_seconds=str(boundary * dt),
                  t0_to_settled_gap_steps=boundary - t0, t0_to_settled_gap_seconds=str((boundary - t0) * dt),
                  rotation_run_steps=runs[3]['steps'], rotation_duration_seconds=str(runs[3]['steps'] * dt),
                  final_planned_step=step, final_planned_seconds=str(step * dt),
                  dump_interval_steps=interval, dump_interval_seconds=str(interval * dt)),
        metadata_crosscheck=dict(t0_planned_matches=meta['steps']['t0_planned'] == t0,
                                 dt_matches=D(meta['dt']['deck_txt']) == dt,
                                 run_steps_matches=meta['steps']['run'] == runs[3]['steps'],
                                 fill_steps_matches=meta['steps']['fill'] == runs[1]['steps'] == runs[2]['steps']),
        surface_gamma=meta.get('adhesion_rule', {}).get('gamma'),
        surface_gamma_wall=meta.get('adhesion_rule', {}).get('gamma_wall'),
        viscosity_coefficient=None,
        interpretation='Static planned values only; not observed particles, runtime state, dump existence, actual stop, or execution authorization.'))

generating = False
# Compare saved claims only after independent reconstruction above.
draft = INPUT / 'docs/reviews/mixer_damping_applicability_draft_20261105'
audit = json.loads((draft / 'mixer_static_audit.json').read_text(encoding='utf-8'))
annotations = json.loads((draft / 'annotation_draft.json').read_text(encoding='utf-8'))
audit_by_id = {r['case_id']: r for r in audit['records']}
annotation_by_id = {r['case_id']: r for r in annotations['case_static_annotations']}
comparisons = []
for r in records:
    a, n = audit_by_id[r['case_id']], annotation_by_id[r['case_id']]
    tm = r['time']
    comparisons.append(dict(case_id=r['case_id'],
        audit_sha_matches=a['deck_sha256'] == r['deck_sha256'],
        annotation_sha_matches=n['deck_sha256'] == r['deck_sha256'],
        audit_size_matches=a['deck_bytes'] == r['deck_bytes'],
        audit_fix_inventory_matches=[x['command'] for x in a['fix_inventory']] == [x['command'] for x in r['fix_inventory']],
        audit_run_steps_match=[x['steps'] for x in a['run_timeline']] == [x['steps'] for x in r['run_timeline']],
        audit_run_boundaries_match=[(x['cumulative_before'], x['cumulative_after']) for x in a['run_timeline']] == [(x['before'], x['after']) for x in r['run_timeline']],
        audit_t0_matches=a['planned_observation_t0_step'] == tm['t0_planned_step'],
        audit_restarts_match=[x['after_completed_steps'] for x in a['settled_restart_boundaries']] == [x['step'] for x in r['settled_restart_boundaries']],
        audit_dump_interval_matches=a['dump_every_steps'] == tm['dump_interval_steps'],
        annotation_time_markers_match=n['planned_time_markers'] == dict(
            observation_t0_step=tm['t0_planned_step'], settled_write_restart_steps=[tm['settled_write_restart_step']],
            fixed_run_end_step=tm['final_planned_step'], dump_every_steps=tm['dump_interval_steps'])))

after = snapshot()
result = dict(
    schema='independent_mixer_damping_static_probe/1', pin=(INPUT / 'PIN.txt').read_text().strip(),
    python=sys.version, execution_flags=dict(isolated=sys.flags.isolated, dont_write_bytecode=sys.flags.dont_write_bytecode),
    scope='new damping draft documentation only; independent in-memory fixed-first8 command and timing reconstruction',
    source_sha256={p: before[p] for p in ('scripts/mixer_precal_prepare.py', 'scripts/make_mixer_deck.py', 'scripts/mixer_deck_readback.py', 'scripts/mixer_deck_diff.py')},
    source_sha_matches_saved_audit={p: before[p] == s for p, s in audit['source_sha256'].items()},
    input_snapshot_unchanged=before == after, checked_input_files=len(before),
    in_memory_cases=len(records), disk_decks_written=0, simulation_runs=0, raw_dumps_read=0,
    validator_or_full_gate_runs=0, host_access=False, execution_authorized=False,
    forbidden_side_effect_attempts=attempted_forbidden, comparisons=comparisons, records=records)
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(output=str(OUTPUT), cases=len(records), source_unchanged=before == after,
                     comparisons_all_pass=all(v for row in comparisons for k, v in row.items() if k != 'case_id'),
                     forbidden_side_effect_attempts=attempted_forbidden), ensure_ascii=False))

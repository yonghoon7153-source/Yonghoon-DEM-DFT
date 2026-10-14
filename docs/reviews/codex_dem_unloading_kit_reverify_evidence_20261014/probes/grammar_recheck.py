"""Independent offline scalar-deck review. No DEM/MPI/remote execution.

The previous review's bounded command interpreter is reused, but its per-dump
clock bug is replaced by one chronological output scheduler. Particle commands,
read_restart, and include remain stubs: native grammar and restored physics are
NOT certified by this model. All supplied observations are explicitly synthetic.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("previous_deck_control", ROOT / "legacy_probes/deck_control.py")
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)


def output_run(model, n):
    """output.cpp:224-254,335-359: common setup time; chronological due times."""
    start, end = model.step, model.step + n
    for name, d in model.dumps.items():
        write = (d['every'] and start % d['every'] == 0 and d['last'] != start)
        write = write or (d['first'] and d['last'] < 0)
        if write:
            model.dump_outputs.append((name, start, model.moving, 'setup'))
            d['last'] = start
        d['next'] = int(model.evaluate('v_' + d['var'])) if d['var'] else (start // d['every'] + 1) * d['every']
        if d['next'] <= start:
            raise ValueError('Dump every variable returned a bad timestep')
    while model.dumps and min(d['next'] for d in model.dumps.values()) <= end:
        model.step = min(d['next'] for d in model.dumps.values())
        for name, d in model.dumps.items():
            if d['next'] != model.step:
                continue
            if d['last'] != model.step:
                model.dump_outputs.append((name, model.step, model.moving, 'regular'))
                d['last'] = model.step
            d['next'] = int(model.evaluate('v_' + d['var'])) if d['var'] else model.step + d['every']
            if d['next'] <= model.step:
                raise ValueError('Dump every variable returned a bad timestep')
    model.step = end


class DeckControl(previous.DeckControl):
    def command(self, line):
        words = previous.shlex.split(line, comments=True, posix=True)
        if words and words[0] == 'run':
            n = int(float(self.substitute(words[1])))
            output_run(self, n)
            if not self.moving and n:
                self.obs.update(self.observer(int(self.value('ul_k')), int(self.value('ul_w')) + 1))
            self.snapshot('run', n=n, moving=self.moving, observations=dict(self.obs))
            return
        if words and words[0] == 'undump':
            del self.dumps[words[1]]
            return
        return super().command(line)


class Clock:
    def __init__(self, step=0):
        self.step, self.moving = step, False
        self.dumps, self.dump_outputs = {}, []
        self.offset = 0

    def evaluate(self, expr):
        if expr == 'v_next':
            return (math.floor(self.step / 10) + 1) * 10
        if expr == 'v_bad':
            return self.step
        if expr == 'v_offset':
            return self.step + self.offset
        raise AssertionError(expr)

    def add(self, name, every=10, var=None, first=False):
        self.dumps[name] = dict(every=0 if var else every, var=var, first=first, last=-1)


def scheduler_checks():
    c = Clock()
    for name in ('atom', 'wall', 'pair'):
        c.add(name, var='next')
    output_run(c, 20)
    assert all([x[1] for x in c.dump_outputs if x[0] == name] == [10, 20] for name in c.dumps)
    parallel = list(c.dump_outputs)
    output_run(c, 0)
    assert c.dump_outputs == parallel
    c = Clock(10)
    c.add('mesh')
    output_run(c, 0)
    output_run(c, 0)
    assert len(c.dump_outputs) == 1
    c.add('newmesh')
    output_run(c, 0)
    assert c.dump_outputs[-1] == ('newmesh', 10, False, 'setup')
    c.add('first', var='next', first=True)
    output_run(c, 0)
    assert c.dump_outputs[-1] == ('first', 10, False, 'setup')
    c = Clock(3)
    c.add('mesh')
    output_run(c, 0)
    assert c.dump_outputs == []
    c.add('bad', var='bad')
    rejected = False
    try:
        output_run(c, 0)
    except ValueError:
        rejected = True
    assert rejected
    c = Clock()
    c.offset = 1000
    c.add('atom', var='offset')
    output_run(c, 5)
    c.offset = 10
    output_run(c, 10)
    assert [x[1] for x in c.dump_outputs] == [15]
    return {'status': 'PASS', 'scope': 'reference scheduler unit checks, not a binary run',
            'three_dump_ids_same_schedule': parallel,
            'checks': ['shared setup timestamp', 'variable setup suppression', 'reevaluation each setup',
                       'reevaluation after scheduled output', 'fixed aligned setup once',
                       'new dump resets last_dump', 'first yes exception',
                       'unaligned fixed setup suppression', 'nonfuture schedule rejected']}


def trace_summary(c):
    return {'result': c.value('ul_result'), 'k': c.value('ul_k'), 'w': c.value('ul_w'),
            'budget': c.value('ul_wmax'),
            'events': [x for x in c.trace if x['what'] == 'event'],
            'moves': [x for x in c.trace if x['what'] == 'run' and x['moving']],
            'dump_outputs': c.dump_outputs}


def production_checks(kit):
    path = kit / 'decks/ps_7_3_r45/in.U_UB.liggghts'
    normal = DeckControl(path, lambda k, w: {'P': {0: .1, 1: .0025, 2: .0009, 3: .0007}.get(k, .0006), 'nc': 0 if k >= 5 else 1})
    normal.prepare()
    normal.run()
    result = {'normal': trace_summary(normal), 'cases': {}, 'gravity_budgets': []}
    for name, contacts, high_ke in (
        ('early_recontact', {4}, False),
        ('late_declaration', {4, 8, 9, 10}, True),
        ('recontact_at_budget', {4, 8, 9, 10, 12}, True),
        ('recontact_after_budget', {4, 8, 9, 10, 13}, True),
    ):
        def observer(k, w, contacts=contacts, high_ke=high_ke):
            return dict(P=1e-8 if w in contacts else 0., nc=1 if w in contacts else 0,
                        Kt=2e-5 if high_ke else 1e-8)
        c = DeckControl(path, observer)
        previous.separation_state(c)
        c.run(until=lambda t: t.value('ul_result') != 'RUNNING' or any(x['what'] == 'run' and x['moving'] for x in t.trace))
        result['cases'][name] = trace_summary(c)
    for bed in ('ps_0_10_r45', 'ps_3_7_r45', 'ps_5_5_r45', 'ps_7_3_r45', 'ps_10_0_r45'):
        for arm in ('UB', 'UVa', 'UVb', 'UT3'):
            c = DeckControl(kit / f'decks/{bed}/in.G_{arm}.liggghts', lambda k, w: dict(P=.005, nc=1))
            previous.separation_state(c)
            c.vars['ul_phase'] = ('equal', '0')
            c.run(until=lambda t: any(x['what'] == 'restart' for x in t.trace))
            result['gravity_budgets'].append(dict(bed=bed, arm=arm,
                first=[c.value('ul_k0min'), c.value('ul_k0max')],
                later=[c.value('ul_wmin0'), c.value('ul_wmax0')], steady_exit_w=c.value('ul_w')))
    result['normal_nonmesh_movement_dump'] = [x for x in normal.dump_outputs if x[0] != 'ul_dm' and x[2]]
    result['normal_nonmesh_setup_dump'] = [x for x in normal.dump_outputs if x[0] != 'ul_dm' and x[3] == 'setup']
    sets = {name: [x[1] for x in normal.dump_outputs if x[0] == name] for name in ('ul_da', 'ul_dw', 'ul_dc')}
    result['normal_atom_wall_pair_schedule_equal'] = sets['ul_da'] == sets['ul_dw'] == sets['ul_dc']
    return result


def module_at(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def scalar_fix_accesses(text):
    """Bounded static ave/time check for this fixture; C++ rules cited below."""
    fixes, problems = {}, []
    for line_no, line in enumerate(text.splitlines(), 1):
        w = previous.shlex.split(line, comments=True, posix=True)
        if len(w) >= 8 and w[:1] == ['fix'] and w[3] == 'ave/time':
            inputs = []
            for token in w[7:]:
                if not token.startswith(('v_', 'c_', 'f_')):
                    break
                inputs.append(token)
            fixes[w[1]] = {'line': line_no, 'inputs': inputs,
                           'mode': w[w.index('mode') + 1] if 'mode' in w else 'scalar'}
        if len(w) >= 4 and w[:1] == ['variable'] and w[2] == 'equal':
            for fix_id, index in re.findall(r'\bf_(\w+)(?:\[(\d+)\])?', ' '.join(w[3:])):
                f = fixes.get(fix_id)
                if f and f['mode'] == 'scalar' and len(f['inputs']) == 1 and index:
                    problems.append({'line': line_no, 'expression': ' '.join(w[3:]),
                                     'definition_line': f['line'], 'fix_id': fix_id,
                                     'input_count': 1, 'native_type': 'global scalar',
                                     'native_expected_access': 'f_' + fix_id,
                                     'native_error': 'Mismatched fix in variable formula'})
    return problems


def grammar_fixture_checks(kit):
    history = kit / 'history_test'
    rh = module_at('grammar_reader_review', history / 'read_history.py')
    gh = module_at('grammar_generator_review', history / 'make_history_decks.py')
    params = rh.load_params(str(history / 'history_params.json'))
    text = (history / 'in.hist_grammar.liggghts').read_text(encoding='utf-8')
    expect = rh.grammar_expect(params)
    E = expect['GA']
    simulations = {}
    for name, deck in [('actual', text),
                       ('scalar_access_in_memory_only', text.replace('f_gr_av[1]', 'f_gr_av')),
                       ('impossible_index_in_memory_only', text.replace('f_gr_av[1]', 'f_gr_av[999]'))]:
        sim = gh.grammar_sim(deck, E['start'], E['z0'],
                             cli={'out': 'OUT', 'gr_state': 'FRESH', 'gr_resume': '0'},
                             includes={'FRESH': '# empty state\n'})
        simulations[name] = {'static_access_problems': scalar_fix_accesses(deck),
                             'producer_model_errors': sim['errors'],
                             'producer_model_screen': sim['screen'],
                             'producer_model_atom_dumps': sim['dumps'].get('gr_da')}
    variants = {}
    with tempfile.TemporaryDirectory(prefix='grammar_review_', dir=ROOT / 'evidence') as tmp:
        for name in ('good', 'ga_rc_failure_with_all_artifacts', 'p_rc_failure_with_all_artifacts',
                     'missing_wall_end', 'header_time_wrong', 'mesh_not_restored',
                     'state_wrong', 'extra_movement_atom_dump'):
            run = Path(tmp) / name
            rh.synth_gram_run(str(run), params)
            if name == 'ga_rc_failure_with_all_artifacts':
                (run / 'GA/rc').write_text('1\n', encoding='utf-8')
            elif name == 'p_rc_failure_with_all_artifacts':
                (run / 'P/rc').write_text('1\n', encoding='utf-8')
            elif name == 'missing_wall_end':
                (run / 'GA/probe/wall_3200.dump').unlink()
            elif name == 'header_time_wrong':
                p = run / 'GA/probe/atom_3200.dump'
                p.write_text(p.read_text(encoding='utf-8').replace('3200', '3199', 1), encoding='utf-8')
            elif name == 'mesh_not_restored':
                p = run / 'GB/probe/mesh_4300.stl'
                p.write_text(p.read_text(encoding='utf-8').replace('0.03002', '0.03'), encoding='utf-8')
            elif name == 'state_wrong':
                p = run / 'GA/restart/state_g_4300.in'
                p.write_text(p.read_text(encoding='utf-8').replace('gr_k equal 2', 'gr_k equal 1'), encoding='utf-8')
            elif name == 'extra_movement_atom_dump':
                p = run / 'GA/probe/atom_2100.dump'
                (run / 'GA/probe/atom_2600.dump').write_text(
                    p.read_text(encoding='utf-8').replace('2100', '2600', 1), encoding='utf-8')
            v = rh.grammar_info(str(run), params)
            variants[name] = {'status': v['status'], 'exit_code': v['exit_code'],
                              'false_checks': [k for k, x in v['checks'].items() if x is not True],
                              'problems': v['problems']}
    return {'scope': 'static C++ type contract plus synthetic file-to-reader tests; no native execution',
            'upstream_type_contract': ['fix_ave_time.cpp:861 default SCALAR',
                                       'fix_ave_time.cpp:350-368 one input scalar; multiple vector',
                                       'variable.cpp:1182,1198,1315 scalar vs indexed access'],
            'native_blocker': scalar_fix_accesses(text),
            'producer_model_blind_spot': simulations, 'reader_variants': variants}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--kit', type=Path)
    p.add_argument('--out', type=Path, default=ROOT / 'evidence/grammar_scheduler.json')
    a = p.parse_args()
    result = {'scope': 'offline scalar review; no physical/numerical or binary grammar certification',
              'scheduler': scheduler_checks()}
    if a.kit:
        result['kit'] = str(a.kit.resolve())
        result['production'] = production_checks(a.kit)
        if (a.kit / 'history_test/in.hist_grammar.liggghts').exists():
            result['grammar_fixture'] = grammar_fixture_checks(a.kit)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'output': str(a.out), 'scheduler': result['scheduler']['status'],
                      'production': {k: {a: v for a, v in x.items() if a not in ('dump_outputs', 'moves', 'events')}
                                     for k, x in result.get('production', {}).get('cases', {}).items()}}, indent=2))


if __name__ == '__main__':
    main()

"""Synthetic, offline execution of the committed deck's scalar control flow.

NO LIGGGHTS, particle simulation, scheduler, subprocess, or source edits.
Physics commands are stubs; run supplies explicitly declared observations.
The native parser's quote-delayed substitutions are modeled for if/print.
The equations/branches come from the deck, not a rewritten state machine.
"""
import json
import math
import re
import shlex
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'source/docs/data/ps45_unload_20261009'


class DeckControl:
    def __init__(self, path, observer):
        self.path = path
        self.lines = path.read_text(encoding='utf-8').splitlines()
        self.labels = {line.split()[1]: i for i, line in enumerate(self.lines) if line.startswith('label ')}
        self.vars = {'out': ('string', '/synthetic'), 'plate_stl': ('string', '/synthetic/plate'),
                     'ckpt': ('string', '/synthetic/restart'), 'ul_base': ('string', '/synthetic/base'),
                     'ul_state': ('string', '/synthetic/state'), 'ul_S2max': ('equal', '1e-5')}
        self.step = 0
        self.atomcount = 160417
        self.observer = observer
        self.obs = dict(P=.1, Kt=1e-8, Kr=1e-8, Kti=1e-8, nc=1, leak=0)
        self.pc = 0
        self.moving = False
        self.trace = []
        self.prints = []
        self.dumps = {}
        self.dump_outputs = []

    def value(self, name):
        style, expression = self.vars[name]
        return expression if style != 'equal' else self.evaluate(expression)

    def substitute(self, string):
        def rep(m):
            v = self.value(m.group(1))
            return format(float(v), '.15g') if isinstance(v, (int, float, bool)) else v
        return re.sub(r'\$\{(\w+)\}', rep, string)

    def evaluate(self, expr):
        expr = self.substitute(expr)
        for i, key in enumerate(('P', 'Kt', 'Kr'), 1):
            expr = expr.replace('f_ul_av[%d]' % i, repr(self.obs[key]))
        expr = re.sub(r'count\(ul_t1,ul_c1\)', repr(self.obs['nc']), expr)
        expr = re.sub(r'count\(ul_t[23],ul_c[23]\)', '0', expr)
        expr = expr.replace('count(all,ul_bel)', repr(self.obs['leak']))
        expr = expr.replace('count(all,ul_abv)', '0')
        expr = re.sub(r'\bstep\b', str(self.step), expr)
        expr = re.sub(r'\batoms\b', str(self.atomcount), expr)
        expr = re.sub(r'\bke\b', repr(self.obs['Kti']), expr)
        expr = expr.replace('&&', ' and ').replace('||', ' or ')
        return eval(expr, {'__builtins__': {}, 'abs': abs, 'floor': math.floor})

    def snapshot(self, what, **extra):
        out = {x: self.value(x) for x in ('ul_k', 'ul_w', 'ul_phase', 'ul_modeB', 'ul_postw', 'ul_sepn', 'ul_okn') if x in self.vars}
        out.update(what=what, step=self.step, **extra)
        self.trace.append(out)

    def command(self, line):
        words = shlex.split(line, comments=True, posix=True)
        if not words:
            return
        cmd = words[0]
        if cmd == 'if':
            condition = bool(self.evaluate(words[1]))
            end = words.index('else') if 'else' in words else len(words)
            chosen = words[3:end] if condition else words[end + 1:]
            for nested in chosen:
                self.command(nested)
            return
        if cmd == 'print':
            expanded = self.substitute(words[1])
            self.prints.append(expanded)
            if len(words) > 3 and words[2] == 'append' and words[3].endswith('/ul_events.csv'):
                self.snapshot('event', text=expanded)
            return
        words = [self.substitute(w) for w in words]
        if cmd == 'variable':
            _, name, style, *values = words
            if style == 'index' and name in self.vars:
                return
            self.vars[name] = (style, values[0])
        elif cmd == 'jump':
            assert words[1] == 'SELF'
            self.pc = self.labels[words[2]] + 1
        elif cmd == 'fix' and words[1] == 'ul_mv':
            self.moving = True
        elif cmd == 'unfix' and words[1] == 'ul_mv':
            self.moving = False
        elif cmd == 'run':
            n = int(float(words[1]))
            start = self.step
            for name, d in self.dumps.items():
                # output.cpp 229-249: variable periods suppress ordinary setup writes.
                if (d['every'] and start % d['every'] == 0 and d['last'] != start) or (d['first'] and d['last'] < 0):
                    self.dump_outputs.append((name, start, self.moving, 'setup'))
                    d['last'] = start
                nxt = self.evaluate('v_' + d['var']) if d['var'] else (start // d['every'] + 1) * d['every']
                while nxt <= start + n:
                    self.step = nxt
                    self.dump_outputs.append((name, nxt, self.moving, 'regular'))
                    d['last'] = nxt
                    nxt = self.evaluate('v_' + d['var']) if d['var'] else nxt + d['every']
            self.step = start + n
            if not self.moving and n:
                k = int(self.value('ul_k'))
                w = int(self.value('ul_w')) + 1
                self.obs.update(self.observer(k, w))
            self.snapshot('run', n=n, moving=self.moving, observations=dict(self.obs))
        elif cmd == 'dump':
            self.dumps[words[1]] = dict(every=int(float(words[4])), var=None, first=False, last=-1)
        elif cmd == 'dump_modify':
            d = self.dumps[words[1]]
            if 'every' in words:
                var = words[words.index('every') + 1]
                assert var.startswith('v_')
                d.update(every=0, var=var[2:])
            if 'first' in words:
                d['first'] = words[words.index('first') + 1] == 'yes'
        elif cmd == 'include':
            pass  # supplied baseline and resume values are explicitly synthetic
        elif cmd == 'read_restart':
            pass
        elif cmd == 'quit':
            raise RuntimeError('deck quit: ' + str(self.prints[-1:]))
        elif cmd == 'write_restart':
            self.snapshot('restart', filename=words[1])

    def prepare(self):
        # Initialize all model/parameter/observer definitions before start.
        stop = next(i for i, x in enumerate(self.lines) if x.startswith(('# >>> block start', '# >>> block g_start')))
        for i in range(stop):
            self.command(self.lines[i])
        self.pc = stop
        self.step = int(self.value('ul_s0'))
        self.atomcount = int(self.value('ul_atoms0'))

    def run(self, until=None, max_commands=100000):
        for _ in range(max_commands):
            if self.pc >= len(self.lines) or (until and until(self)):
                return
            line = self.lines[self.pc]
            self.pc += 1
            self.command(line)
        raise RuntimeError('synthetic command bound reached')


# v_name expressions are only used by output schedules in this bounded model.
_evaluate = DeckControl.evaluate
def evaluate(self, expr):
    expr = re.sub(r'\bv_(\w+)\b', lambda m: '(' + self.vars[m.group(1)][1] + ')', expr)
    return _evaluate(self, expr)
DeckControl.evaluate = evaluate


def separation_state(c):
    c.prepare()
    data = dict(ul_k=5, ul_phase=2, ul_modeB=1, ul_pz=.1115, ul_h0=.111052,
                ul_lift=.000448, ul_ncross=2, ul_xk=2, ul_Pbar=0, ul_postw=0,
                ul_steady=0, ul_dz=.00005, ul_n=5000, ul_lk0=0)
    for name, value in data.items():
        c.vars[name] = ('equal', str(value))
    for name, value in dict(ul_kind='B', ul_why='none', ul_result='RUNNING').items():
        c.vars[name] = ('string', value)
    c.pc = c.labels['ul_hold_start'] + 1


def main():
    path = KIT / 'decks/ps_7_3_r45/in.U_UB.liggghts'
    result = {'basis': str(path.relative_to(ROOT)), 'scope': 'offline scalar-control interpreter; no physical simulation'}
    normal = DeckControl(path, lambda k,w: {'P': {.0: .1, 1: .0025, 2: .0009, 3: .0007}.get(k, .0006), 'nc': 0 if k >= 5 else 1})
    normal.prepare()
    normal.run()
    result['normal'] = {'events': [x for x in normal.trace if x['what'] == 'event'],
                        'final': normal.value('ul_result'),
                        'nonmesh_move_dumps': [x for x in normal.dump_outputs if x[0] != 'ul_dm' and x[2]],
                        'nonmesh_setup_dumps': [x for x in normal.dump_outputs if x[0] != 'ul_dm' and x[3] == 'setup']}
    # At w=4 recontact, S1/S2 have been stable for >=2 windows.
    # The remaining budget is eight windows; script ends the hold immediately.
    recontact = DeckControl(path, lambda k,w: dict(P=1e-8 if w == 4 else 0., nc=1 if w == 4 else 0))
    separation_state(recontact)
    recontact.run(until=lambda c: any(x['what'] == 'run' and x['moving'] for x in c.trace))
    result['recontact_steady'] = {'expected': 'Stay at the same k and height to attempt re-separation within the remaining budget.',
        'actual': recontact.trace, 'remaining_budget': recontact.value('ul_wmax') - 4}
    # Prevent generic steady end using high (but guard-safe) KE, then a late
    # declaration/re-declaration exposes POST bypass of the 12-window budget.
    over = DeckControl(path, lambda k,w: dict(P=1e-8 if w in (4, 8, 9, 10) else 0., Kt=2e-5, nc=1 if w in (4, 8, 9, 10) else 0))
    separation_state(over)
    over.run(until=lambda c: c.value('ul_result') != 'RUNNING')
    result['post_budget'] = {'expected': 'No successful completion beyond the same 12-window hold budget after recontact.',
        'actual': over.trace, 'final': over.value('ul_result'), 'windows': over.value('ul_w'), 'budget': over.value('ul_wmax')}
    grav = []
    for arm in ('UB', 'UVa', 'UVb', 'UT3'):
        g = DeckControl(KIT / f'decks/ps_7_3_r45/in.G_{arm}.liggghts', lambda k,w: dict(P=.005, nc=1))
        separation_state(g)
        g.vars['ul_phase'] = ('equal', '0')
        g.run(until=lambda c: any(x['what'] == 'restart' for x in c.trace))
        grav.append({'arm': arm, 'initial_hold_min': g.value('ul_k0min'), 'initial_hold_max': g.value('ul_k0max'),
                     'later_hold_min': g.value('ul_wmin0'), 'later_hold_max': g.value('ul_wmax0'),
                     'first_later_steady_hold_windows': g.value('ul_w')})
    result['gravity_budgets'] = grav
    # Explicit last-two-window pressure and k=0 mode exception.
    avg = DeckControl(path, lambda k,w: dict(P=[.00242, .00244, .00246][min(w-1,2)], nc=1))
    avg.prepare()
    avg.run(until=lambda c: any(x['what'] == 'event' and x['text'].startswith('HOLD0_DONE,') for x in c.trace))
    result['last_two_mean_k0'] = dict(Pbar=avg.value('ul_Pbar'), expected=(.00244+.00246)/2,
                                    modeB=avg.value('ul_modeB'), expected_modeB=0)
    caps = []
    for lift in (.01595, .016):
        cap = DeckControl(path, lambda k,w: dict(P=.005, nc=1))
        separation_state(cap)
        cap.vars['ul_lift'] = ('equal', repr(lift))
        cap.vars['ul_step'] = ('equal', str(cap.step))
        cap.pc = cap.labels['ul_next'] + 1
        cap.run(until=lambda c: c.value('ul_result') != 'RUNNING' or any(x['what']=='run' for x in c.trace))
        caps.append(dict(lift=lift, result=cap.value('ul_result'), movement=any(x['what']=='run' and x['moving'] for x in cap.trace)))
    result['lift_cap'] = caps
    (ROOT / 'evidence/deck_control.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'normal': result['normal'], 'recontact_steady_moves_at_w': 4,
                      'post_budget_windows': result['post_budget']['windows'],
                      'post_budget_result': result['post_budget']['final'], 'gravity_budgets': grav,
                      'last_two_mean_k0': result['last_two_mean_k0'], 'lift_cap': caps}, indent=2))


if __name__ == '__main__':
    main()

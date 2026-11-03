"""Independent, no-shell/no-simulator probes of the pinned embedded Python.

Only writes to phase_review. Symbolic control-flow checks below are not LIGGGHTS
simulation: their branch outcomes are supplied inputs and no forces are computed.
"""
from pathlib import Path
import ast
import contextlib
import hashlib
import importlib.util
import io
import json

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OUT = PACKAGE_ROOT / 'phase_review'
REPO = PACKAGE_ROOT / 'source' / 'repo'
SRC = REPO / 'scripts' / 'resume_ckpt.sh'
source = SRC.read_text(encoding='utf-8')
embedded = source.split("deckcheck(){ python3 - \"$@\" <<'PY'\n", 1)[1].split('\nPY\n}', 1)[0]
tree = ast.parse(embedded)
# Keep exactly the source's definitions/constants; do not run its CLI dispatcher.
safe = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom,
        ast.Assign, ast.AnnAssign, ast.FunctionDef, ast.ClassDef))]
ns = {'__name__': 'deckcheck_under_review'}
exec(compile(ast.Module(body=safe, type_ignores=[]), str(SRC), 'exec'), ns)

def invoke(name, *args):
    text = io.StringIO()
    with contextlib.redirect_stdout(text):
        value = ns[name](*args)
    return value, text.getvalue()

records = []
def record(name, ok, **data):
    records.append(dict(name=name, ok=bool(ok), **data))
    print(('PASS ' if ok else 'FAIL ') + name)

def write(name, text):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')
    return str(p)

ck = 'restart_kg50_d07_b50/restart_compress_1000000.bin'
mainpath = REPO / 'docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts'
if mainpath.is_file():
    spec = importlib.util.spec_from_file_location('pinned_test_helpers', REPO / 'scripts/test_resume_ckpt.py')
    helpers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helpers)
    main_text = mainpath.read_text(encoding='utf-8')
    raw_text = helpers.qb_raw(main_text, helpers.C50, ck, order='r075')
    source_kind = 'actual pinned b50 main + synthetic r075-style helper output'
else:
    main_text = '''units si
variable target_press equal 0.3
run 1
run 200000
run 1
run 200000
restart 200000 restart_kg50_d07_b50/restart_compress_*.bin
label loop_press
run 5000
variable current_press equal step
print "Current Pressure: ${current_press} MPa (Target: ${target_press})"
if "${current_press} < ${target_press}" then "jump SELF loop_press"
restart 0
run 100000
'''
    raw_text = ('units si\nvariable target_press equal 0.3\nread_restart ' + ck + '\n' +
                main_text[main_text.index('restart 200000'):])
    source_kind = 'minimal synthetic main and resume; actual b50 fixture absent'

mp = write('base/main.liggghts', main_text)
rp = write('base/resume.liggghts', raw_text)
M, lp = ns['q3b_lp'](mp, ck, 1000000)
record('source identity', hashlib.sha256(SRC.read_bytes()).hexdigest() ==
       '66006239ec58043f963fa885f9db545c63614d279bfb6cac1665a2eae9884c6d', source_kind=source_kind,
       sha256=hashlib.sha256(SRC.read_bytes()).hexdigest())
record('actual-case arithmetic', isinstance(lp, dict) and [lp[k] for k in ('E','N','p','r')] ==
       [400002,5000,4998,2], result=lp)
rc, output = invoke('q3b_fix', mp, rp, ck, '1000000', str(OUT / 'base'))
probs, notes = ns['check'](mp, rp, ck, 1000000, str(OUT / 'base'))
record('rewrite then complete static checker', rc == 0 and not probs, rc=rc, output=output, problems=probs)
R = ns['deck'](rp)
read_at = next(i for i,l in enumerate(R) if l.startswith('read_restart '))
run_at = next(i for i in range(read_at+1,len(R)) if R[i].startswith('run '))
suffix = R[run_at:]

def symbolic(commands, decisions, initial=1000000):
    """Follow emitted commands with supplied symbolic code-pressure values.

    The threshold 0.30 represents 300 MPa at SCALE_STRESS=1e9 Pa. No value
    supplied here is a measured pressure or a force-computation result.
    """
    labels = {ns['words'](l)[1]:i for i,l in enumerate(commands) if l.startswith('label ')}
    step, pc, di, events = initial, 0, 0, []
    for _ in range(200):
        if pc >= len(commands):
            return events + [('end',step)]
        w = ns['words'](commands[pc])
        pc += 1
        if w[0] == 'run':
            step += int(w[1]); events.append(('run_end',step,int(w[1])))
        elif w[:2] == ['restart','0']:
            return events + [('relax',step)]
        elif w[0] == 'jump':
            events.append(('jump',w[2],step)); pc = labels[w[2]]+1
        elif w[0] == 'if':
            # The only conditional encountered in the suffix is exact '<'.
            assert w[1] == '${current_press} < ${target_press}', w
            p = decisions[di]; di += 1
            below = p < 0.3
            events.append(('judgment',step,p,below))
            cmd = ns['words'](w[3] if below else (w[5] if len(w)>5 else ''))
            if cmd and cmd[0] == 'jump':
                events.append(('jump',cmd[2],step)); pc = labels[cmd[2]]+1
            elif cmd and cmd[0] == 'quit':
                return events + [('quit',step)]
    raise AssertionError('unexpected control-flow cycle')

for name, values, judgments in [
    ('below then below then equal',[0.1,0.299,0.3],[1000002,1005002,1010002]),
    ('first equal',[0.3],[1000002]),
    ('first above',[0.301],[1000002]),
    ('below then above',[0.299,0.301],[1000002,1005002])]:
    events = symbolic(suffix, values)
    actual = [e[1] for e in events if e[0]=='judgment']
    record('main branch '+name, actual==judgments and events[-1]==('relax',judgments[-1]), events=events)

for ts in [1,2,3,1999,2000,5000,5001,5002,5003,100000]:
    trial = str(OUT / ('trial_%d.liggghts'%ts))
    rc, cut = invoke('cut_trial_q3b',mp,rp,ck,'1000000',str(ts),trial)
    rc2, count = invoke('trial_steps',trial)
    T = ns['deck'](trial)
    ir = next(i for i,l in enumerate(T) if l.startswith('run '))
    calls = [int(ns['words'](l)[1]) for l in T[ir:] if l.startswith('run ')]
    expected = [ts] if ts<=2 else [2,min(ts-2,5000)]
    ev_low = symbolic(T[ir:],[0.299])
    ev_equal = symbolic(T[ir:],[0.3])
    ev_high = symbolic(T[ir:],[0.301])
    end = 1000000+sum(expected)
    correct = rc==rc2==0 and calls==expected and ev_low[-1]==('end',end)
    if ts>2:
        correct = correct and ev_equal[-1]==ev_high[-1]==('quit',1000002) and end>1000002
    else:
        correct = correct and not any(e[0]=='judgment' for e in ev_equal)
    record('trial budget %d'%ts,correct,cut=cut,count=count,calls=calls,
           below=ev_low,equal=ev_equal,above=ev_high,expected_end=end)

for s0 in [600000,800000,1000000,1200000,1400000,2000000,10000000]:
    ck2 = ck.replace('1000000',str(s0))
    _, ph = ns['q3b_lp'](mp,ck2,s0)
    record('later/source checkpoint phase %d'%s0,isinstance(ph,dict) and ph['r']==2 and ph['p']==4998,
           r=ph['r'] if isinstance(ph,dict) else ph)

# Independent numerical phase sweep: shift the immediately-pre-loop 200000 run
# across all 5000 residues, then compare the implementation to integer arithmetic.
ia = next(i for i,l in enumerate(M) if l.startswith('restart 200000') and 'compress' in l)
prior = max(i for i in range(ia) if M[i].startswith('run '))
base_n = int(M[prior].split()[1])
bad = []
for shift in range(5000):
    mm = list(M); mm[prior] = 'run %d'%(base_n+shift)
    ph = ns['loop_phase'](mm,ia,1000000)
    E = 400002+shift
    residue = (1000000-E)%5000
    valid = (isinstance(ph,str) and '위상 0' in ph) if residue==0 else (
        isinstance(ph,dict) and ph['E']==E and ph['p']==residue and ph['r']==5000-residue)
    if not valid: bad.append(dict(shift=shift,result=ph))
record('exhaustive 5000 phase residues',not bad,failures=bad)

negative = [
    ('nonmultiple checkpoint',M,ia,1000001),
    ('checkpoint not in loop',M,ia,400000),
    ('missing restart zero',[l for l in M if l!='restart 0'],ia,1000000),
]
for name,mm,j,s0 in negative:
    ph = ns['loop_phase'](mm,j,s0)
    record('refuse '+name,isinstance(ph,str),result=ph)

good_text = Path(rp).read_text(encoding='utf-8')
first_if = 'if "${current_press} < ${target_press}" then "jump SELF loop_press"'
mutations = [
    ('residual one',good_text.replace('run 2\n','run 1\n',1)),
    ('residual three',good_text.replace('run 2\n','run 3\n',1)),
    ('residual full chunk',good_text.replace('run 2\n','run 5000\n',1)),
    ('main loop shortened',good_text.replace('run 5000\n','run 2\n',1)),
    ('skip jump missing',good_text.replace('jump SELF q3b_done_loop_press\n','',1)),
    ('skip label missing',good_text.replace('label q3b_done_loop_press\n','',1)),
    ('wrong skip target',good_text.replace('jump SELF q3b_done_loop_press\n','jump SELF loop_press\n',1)),
    ('first equality repeats',good_text.replace(first_if,first_if.replace(' < ',' <= '),1)),
    ('first threshold inverted',good_text.replace(first_if,first_if.replace(' < ',' > '),1)),
    ('all threshold equality repeats',good_text.replace(' < ${target_press}',' <= ${target_press}')),
    ('extra step before skip',good_text.replace('jump SELF q3b_done_loop_press\n','run 1\njump SELF q3b_done_loop_press\n',1)),
    ('skip label moved past unfix',good_text.replace('label q3b_done_loop_press\n','',1).replace('unfix move_press\n','unfix move_press\nlabel q3b_done_loop_press\n',1)),
]
for i,(name,mutant) in enumerate(mutations):
    assert mutant != good_text,name
    mutpath = write('mutant_%02d.liggghts'%i,mutant)
    probs,_ = ns['check'](mp,mutpath,ck,1000000,str(OUT/'base'))
    before = Path(mutpath).read_bytes()
    rc, rejection = invoke('q3b_fix',mp,mutpath,ck,'1000000',str(OUT/'base'))
    trialpath = str(OUT/('mutant_%02d_trial.liggghts'%i))
    rc2, reason = invoke('cut_trial_q3b',mp,mutpath,ck,'1000000','2000',trialpath)
    record('reject rewrite mutation '+name,bool(probs) and rc==rc2==1 and
           Path(mutpath).read_bytes()==before and not Path(trialpath).exists(),
           problems=probs,fix_rejection=rejection,cut_rejection=reason)

write('results.json',json.dumps(dict(source_kind=source_kind,
    pressure_note='Branch inputs are symbolic code-pressure values: 0.30 represents 300 MPa at SCALE_STRESS=1e9 Pa. Quoted deck print strings are preserved verbatim, including their original MPa label.',
    records=records),ensure_ascii=False,indent=2)+'\n')
passed = sum(r['ok'] for r in records)
print('%d/%d checks passed; no simulator, scheduler, WSL, or shell runner invoked.'%(passed,len(records)))
raise SystemExit(0 if passed==len(records) else 1)

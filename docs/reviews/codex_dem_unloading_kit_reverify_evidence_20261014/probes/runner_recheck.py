"""Independent offline restoration -> next-job gate probes; no DEM or shell.

The positive fixture is constructed here, not by the production selftest helper.
Each case is an isolated copy. Production source is imported but never edited.
"""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'source/docs/data/ps45_unload_20261009'
sys.path.insert(0, str(KIT))
import ul_lib as L
import ul_reader as R

P = L.load_params()
BED = R.B73
B = P['beds'][BED]
S0 = B['s0']
END = S0 + P['windows']['R_steps']
EVIDENCE = ROOT / 'evidence'
EVIDENCE.mkdir(exist_ok=True)
RUN = Path(tempfile.mkdtemp(prefix='runner_cases_', dir=EVIDENCE))


def put(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def js(path, obj):
    put(path, json.dumps(obj, ensure_ascii=False, indent=2))


def baseline(root):
    j = root / BED / 'RJ'
    g1, g3 = B['g1'].split(), B['g3'].split()
    resets = ''.join(f'Resetting {k} state of Fix {f} Style {s} from restart file info\n'
                     for f, s, ks in R.EXPECTED_RESETS for k in ks)
    head = 'Step Atoms KinEng ul_erot ul_Ps pressMPa CPU\n'
    scr = ('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n' + resets + head +
           f'{g1[0]} {g1[1]} {g1[2]} 1e-08 {g1[4]} {g1[4]} 0\n' +
           'Loop time of 0 on 6 procs for 0 steps\n' + head +
           f'{g1[0]} {g1[1]} {g1[2]} 1e-08 {g1[4]} {g1[4]} 0\n' +
           f'{g3[0]} {g3[1]} {g3[2]} 1e-08 {g3[4]} {g3[4]} 1\n' +
           'Loop time of 1 on 6 procs for 2000 steps\nUL_R_DONE\n')
    put(j / 'R/screen.txt', scr)
    put(root / BED / 'in' / B['orig_log'], scr)
    for stage, kind, marker in (('Ut0', 'Ut0', 'UL_SUMMARY arm=Ut0 result=DONE'),
                                ('UN', 'UNread', 'UL_UN_DONE')):
        put(j / stage / 'screen.txt',
            'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n'
            'Loop time of 1 on 6 procs for 100 steps\n' + marker + '\n')
        put(j / stage / 'run_check.txt', f'{kind} screen.txt PASS rc=0 procs=6\n')
    put(j / 'R/run_check.txt', 'R screen.txt PASS rc=0 procs=6\n')
    js(j / 'g0.json', {'status': 'PASS', 'violations': []})
    put(j / 'run_manifest.txt', f'bed={BED}\njob=RJ\nresume=0\ngate=ALLOW\nstart=x\n'
        'stage=G0 rc=0\nstage=Ut0 screen=screen.txt rc=0 check=PASS\n'
        'stage=R screen=screen.txt rc=0 check=PASS\nstage=UNread screen=screen.txt rc=0 check=PASS\n'
        'reader_restore_rc=0\nreader_kebase_rc=0\nend=x fails=0 reader_rc=0\n')
    acols = ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz']
    atoms = [dict(zip(acols, [i, 3, i*.001, .002, .003, .0005, 1e-6, 0, 0])) for i in range(1, 4)]
    ccols = [f'c_cpl[{i}]' for i in range(1, 27)]
    contact = dict(zip(ccols, [.001,.01,.01,.0015,.01,.01,1,2,0,-.5,0,0,-.5,0,0,0,.01,0,0,0,0,1e-8,1e-5,.00125,.01,.01]))
    for base in (root / BED / 'in', j / 'R/g2'):
        base.mkdir(parents=True, exist_ok=True)
        L.write_custom(str(base / f'atom_{S0}.liggghts'), S0, acols, atoms)
        L.write_local(str(base / f'contact_{S0}.liggghts'), S0, ccols, [contact])
        put(base / f'mesh_{S0}.stl', 'solid fixture\nendsolid fixture\n')
    hist = []
    for atom in atoms:
        a = dict(atom, mass=1e-6, omegax=0, omegay=0, omegaz=0, fx=0, fy=0, fz=0)
        a.update({f'f_history_zwall_bot[{i}]': (2e-5 if atom['id'] == 1 and i == 1 else 0) for i in range(1, 5)})
        hist.append(a)
    zero = [{**a, **{f'f_history_zwall_bot[{i}]': 0 for i in range(1, 5)}} for a in hist]
    for rel, step, cols, rows in [('R/obs/pre_bot.dump', S0, R.HIST_PRE_COLS, hist),
                                (f'R/obs/post_atom_{S0}.dump', S0, R.HIST_POST_COLS, hist),
                                ('R/obs/end_pre_bot.dump', END, R.HIST_PRE_COLS, hist),
                                ('UN/obs/un_pre_bot.dump', END, R.HIST_PRE_COLS, zero)]:
        path = j / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        L.write_custom(str(path), step, list(cols), rows)
    # Complete UK evidence provides a genuine production-generated S2 baseline.
    uk = j/'UK'
    put(uk/'screen.txt', 'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\n'
        'Loop time of 1 on 6 procs for 15000 steps\nUL_SUMMARY arm=UK result=DONE\n')
    put(uk/'run_check.txt', 'UK screen.txt PASS rc=0 procs=6\n')
    put(uk/'ul_summary.txt', f'result=DONE\narm=UK\nbed={BED}\n')
    put(uk/'ul_events.csv', ','.join(P['records']['events_cols']) + f'\nSTART,0,{S0},{B["h0"]},0,s0\n')
    rows = [f'UK,{BED},0,{w},4,{S0+P["windows"]["W0"]*w},{B["h0"]},0,0.16,2e-07,{rot},0,-1,-1,-1,400,160417,11,2e-07'
            for w, rot in ((1, 3e-8), (2, 1e-8), (3, 2e-8))]
    put(uk/'ul_windows.csv', ','.join(P['records']['windows_cols']) + '\n' + '\n'.join(rows) + '\n')
    k = R.kebase(str(root), BED, P)
    assert k['s2_limit'] is not None and not k['problems'], k
    return j


GOOD = json.loads((ROOT / 'evidence/history_reread.json').read_text(encoding='utf-8'))
TEMPLATE = RUN / 'template'
baseline(TEMPLATE)
results = {}


def replace(path, old, new):
    text = path.read_text(encoding='utf-8')
    assert old in text, (str(path), old)
    put(path, text.replace(old, new))


def dump_mutate(path, col, row, value):
    lines = path.read_text(encoding='utf-8').splitlines()
    hi = next(i for i, x in enumerate(lines) if x.startswith('ITEM: ATOMS '))
    cols = lines[hi].split()[2:]
    fields = lines[hi + 1 + row].split()
    fields[cols.index(col)] = str(value)
    lines[hi + 1 + row] = ' '.join(fields)
    put(path, '\n'.join(lines) + '\n')


def case(name, mutate=None, hist_mutate=None, expected=None):
    root = RUN / name
    shutil.copytree(TEMPLATE, root)
    j = root / BED / 'RJ'
    if mutate:
        mutate(j)
    hv = copy.deepcopy(GOOD)
    if hist_mutate:
        hist_mutate(hv)
    js(root / 'history.json', hv)
    verdict = R.restore_verdict(str(root), BED, 'RJ', str(root / 'history.json'), P)
    js(j / 'restore_verdict.json', verdict)
    gate = R.gate(str(root), BED, 'UB', P)
    result = {'restore': verdict['status'], 'next_UB_allowed': gate[0], 'gate_reason': gate[1], 'checks': verdict['checks']}
    if expected is not None:
        result['expected'] = {'restore': expected[0], 'next_UB_allowed': expected[1]}
        result['matches_expected'] = (verdict['status'], gate[0]) == expected
    results[name] = result
    return result


case('baseline', expected=('RESTORED', True))
case('truncated_pre_post', lambda j: [replace(j/p, 'ITEM: NUMBER OF ATOMS\n3\n', 'ITEM: NUMBER OF ATOMS\n20\n')
                                    for p in ('R/obs/pre_bot.dump', f'R/obs/post_atom_{S0}.dump')], expected=('UNCONFIRMED', False))
case('nan_pre', lambda j: dump_mutate(j/'R/obs/pre_bot.dump', 'f_history_zwall_bot[1]', 1, 'nan'), expected=('UNCONFIRMED', False))
case('duplicate_post', lambda j: dump_mutate(j/f'R/obs/post_atom_{S0}.dump', 'id', 1, 1), expected=('UNCONFIRMED', False))
case('un_wrong_id', lambda j: dump_mutate(j/'UN/obs/un_pre_bot.dump', 'id', 0, 999), expected=('UNCONFIRMED', False))
for obs, rel, step in [('pre', 'R/obs/pre_bot.dump', S0), ('post', f'R/obs/post_atom_{S0}.dump', S0),
                       ('end', 'R/obs/end_pre_bot.dump', END), ('un', 'UN/obs/un_pre_bot.dump', END)]:
    case(f'{obs}_wrong_step', lambda j, rel=rel, step=step: replace(j/rel, f'ITEM: TIMESTEP\n{step}\n', f'ITEM: TIMESTEP\n{step+1}\n'),
         expected=('UNCONFIRMED', False))
for stage, kind in [('Ut0', 'Ut0'), ('R', 'R'), ('UN', 'UNread')]:
    case(f'{stage}_receipt_fail', lambda j, stage=stage, kind=kind: put(j/stage/'run_check.txt', f'{kind} screen.txt FAIL rc=1\n'),
         expected=('SYNTAX_FAIL', False))
    case(f'{stage}_screen_error', lambda j, stage=stage: put(j/stage/'screen.txt', (j/stage/'screen.txt').read_text()+'ERROR: synthetic late failure\n'),
         expected=('SYNTAX_FAIL', False))
case('G0_fail', lambda j: js(j/'g0.json', {'status': 'FAIL', 'violations': ['synthetic']}), expected=('VALUE_MISMATCH', False))
case('manifest_fails1', lambda j: replace(j/'run_manifest.txt', 'end=x fails=0', 'end=x fails=1'), expected=('RESTORED', False))
case('manifest_no_end', lambda j: replace(j/'run_manifest.txt', 'end=x fails=0 reader_rc=0\n', ''), expected=('RESTORED', False))
case('missing_SYN', hist_mutate=lambda h: h['info'].pop('syn'), expected=('UNCONFIRMED', False))
case('SYN_wrong_sign', hist_mutate=lambda h: h['info']['syn'].update(plate_fn_sign=1), expected=('UNCONFIRMED', False))
case('SYN_fail', hist_mutate=lambda h: h['info']['syn'].update(status='FAIL'), expected=('UNCONFIRMED', False))
case('force_timing_missing', hist_mutate=lambda h: h['info'].pop('force_timing'), expected=('UNCONFIRMED', False))
case('wrong_history_schema', hist_mutate=lambda h: h.update(schema='other'), expected=('UNCONFIRMED', False))
# Additional receipt-integrity checks beyond the original counterexamples.
case('manifest_reader_rc1', lambda j: replace(j/'run_manifest.txt', 'end=x fails=0 reader_rc=0', 'end=x fails=0 reader_rc=1'))
case('manifest_G0_rc1', lambda j: replace(j/'run_manifest.txt', 'stage=G0 rc=0', 'stage=G0 rc=1'))
case('fractional_un_id', lambda j: dump_mutate(j/'UN/obs/un_pre_bot.dump', 'id', 0, 1.5))
case('receipt_screen_mismatch', lambda j: replace(j/'UN/run_check.txt', 'UNread screen.txt PASS rc=0 procs=6', 'UNread nonexistent.txt PASS rc=0 procs=4'))

# Reachable process-level receipt case: the unchanged restore CLI publishes its
# JSON before stdout is flushed. A closed output pipe makes the command fail,
# while the runner's separate reader rc does not increment its LMP FAILS count.
# No fake status is injected: the CLI creates the RESTORED JSON itself.
root = RUN / 'actual_restore_cli_closed_stdout'
shutil.copytree(TEMPLATE, root)
# This is our own generated fixture; ensure the final baseline is newly emitted
# by the real kebase CLI after restore, as in the actual RJ runner.
(root/BED/'ul_base.in').unlink()
js(root/'history.json', GOOD)
cmd = [sys.executable, '-X', 'utf8', '-B', '-I', str(KIT/'ul_reader.py'),
       'restore', str(root), BED, '--hist', str(root/'history.json')]
with (root/'stderr.txt').open('wb') as err:
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=err)
    proc.stdout.close()
    cli_rc = proc.wait(timeout=30)
j = root/BED/'RJ'
verdict = json.loads((j/'restore_verdict.json').read_text(encoding='utf-8'))
replace(j/'run_manifest.txt', 'reader_restore_rc=0', f'reader_restore_rc={cli_rc}')
ke_cmd = [sys.executable, '-X', 'utf8', '-B', '-I', str(KIT/'ul_reader.py'), 'kebase', str(root), BED]
with (root/'kebase_stderr.txt').open('wb') as err:
    proc = subprocess.Popen(ke_cmd, stdout=subprocess.PIPE, stderr=err)
    proc.stdout.close()
    ke_rc = proc.wait(timeout=30)
replace(j/'run_manifest.txt', 'reader_kebase_rc=0', f'reader_kebase_rc={ke_rc}')
# run_unload.sh:222 explicitly replaces any failing kebase rc by aggregate RRC=2.
aggregate_rc = 2 if ke_rc != 0 else cli_rc
replace(j/'run_manifest.txt', 'end=x fails=0 reader_rc=0', f'end=x fails=0 reader_rc={aggregate_rc}')
gate = R.gate(str(root), BED, 'UB', P)
results['actual_restore_cli_closed_stdout'] = {
    'restore': verdict['status'], 'next_UB_allowed': gate[0], 'gate_reason': gate[1],
    'cli_rc': cli_rc, 'kebase_cli_rc': ke_rc, 'runner_aggregate_rc_by_source': aggregate_rc,
    'argv': cmd, 'stderr': (root/'stderr.txt').read_text(encoding='utf-8', errors='replace'),
    'manifest_origin': 'Same reader_<cmd>_rc and end fails=0 reader_rc=<rc> fields the runner emits after reader failure; LMP stages unchanged.',
    'ke_base_scope': 'Complete valid UK evidence; real kebase CLI newly emits ul_base.in after restore, then fails flushing stdout.',
    'ke_base_text': (root/BED/'ul_base.in').read_text(encoding='utf-8')}
assert cli_rc != 0 and verdict['status'] == 'RESTORED', 'Expected process failure after receipt publication did not occur'

summary = {k: {key: val for key, val in v.items() if key != 'checks'} for k, v in results.items()}
output = {'pin': 'a30fe150e21f66aea2f1c360593e1cd781689b14', 'run_dir': str(RUN),
          'source_sha256': {f: hashlib.sha256((KIT/f).read_bytes()).hexdigest() for f in ('ul_reader.py', 'ul_gates.py', 'run_unload.sh')},
          'results': results, 'summary': summary}
js(EVIDENCE/'runner_recheck.json', output)
print(json.dumps({'run_dir':str(RUN), 'summary':summary}, ensure_ascii=False, indent=2))
assert all(v.get('matches_expected', True) for v in results.values()), 'Original regression or positive control failed'

"""CPU only: extract and execute production Python, never Bash/DEM/scheduler.

The oracle's lexical counterexamples concern supported preparation transforms;
this probe does not pretend to simulate LIGGGHTS physics.
"""
from pathlib import Path
import contextlib, hashlib, io, json, subprocess, sys

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[1] / 'repo'
SOURCE = REPO / 'scripts/resume_ckpt.sh'
raw = SOURCE.read_bytes()
source = raw.decode('utf-8').replace('\r\n', '\n')
start = source.index('import difflib, os, re, sys\n')
stop = source.index('\nPY', start)
program = source[start:stop]
(OUT / 'extracted_deckcheck.py').write_text(program, encoding='utf-8')
ns = {}
exec(compile(program[:program.index("if len(sys.argv) == 3 and sys.argv[1] == '--strip-comments':")], str(SOURCE) + ':embedded_python', 'exec'), ns)

results = {'source_sha256': hashlib.sha256(raw).hexdigest(), 'python': sys.version,
           'scope': 'unmodified embedded Python only; no Bash, SLURM, LIGGGHTS or WSL', 'cases': []}

def case(name, main, resume, ckpt='restart_settling_50.bin', s0=50, *, expected=None, metadata=None, files=None, ts=10):
    folder = OUT / 'cases' / name
    folder.mkdir(parents=True, exist_ok=True)
    for filename, value in (files or {}).items():
        (folder / filename).write_text(value, encoding='utf-8')
    mainpath, respath = folder / 'main.liggghts', folder / 'resume.liggghts'
    mainpath.write_text(main, encoding='utf-8')
    respath.write_text(resume, encoding='utf-8')
    args = [sys.executable, '-I', '-X', 'utf8', str(OUT / 'extracted_deckcheck.py'), str(mainpath), str(respath), ckpt, str(s0), str(folder)]
    cp = subprocess.run(args, capture_output=True, encoding='utf-8', env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'})
    probs, notes = ns['check'](str(mainpath), str(respath), ckpt, s0, str(folder))
    assert cp.returncode == bool(probs), (name, cp.stdout, cp.stderr)
    (folder / 'static_stdout.txt').write_text(cp.stdout, encoding='utf-8')
    cutpath = folder / 'trial.liggghts'
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        cutrc = ns['cut_trial'](str(respath), str(ts), str(cutpath))
    cutout = stdout.getvalue()
    trialrc, trialout = None, None
    if cutrc == 0:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            trialrc = ns['trial_steps'](str(cutpath))
        trialout = stdout.getvalue()
    row = {'name': name, 'expected': expected, 'static_rc': cp.returncode, 'problems': probs, 'notes': notes,
           'cut_rc': cutrc, 'cut_stdout': cutout, 'trial_rc': trialrc, 'trial_stdout': trialout,
           'command': args, 'trial_steps_requested': ts, 'metadata': metadata or {}}
    results['cases'].append(row)
    print(name, 'static_rc', cp.returncode, 'cut_rc', cutrc, 'trial_rc', trialrc)
    return row

base_m = 'units si\nvariable dt equal 1e-6\ntimestep ${dt}\nrestart 10 restart_settling_*.bin\nrun 100\nprint "done"\n'
base_r = 'units si\nread_restart restart_settling_50.bin\nvariable dt equal 1e-6\ntimestep ${dt}\nrestart 10 restart_settling_*.bin\nrun 50\nprint "done"\n'
case('baseline', base_m, base_r, expected='accept')

# Ordered subsequence is insufficient: a deleted reaching definition can change
# an eager ${dt} substitution while final variable and timestep strings agree.
case('drop_intermediate_variable_definition',
     base_m.replace('variable dt equal 1e-6\ntimestep ${dt}',
                    'variable dt equal 1e-6\nvariable dt equal 2e-6\ntimestep ${dt}\nvariable dt equal 1e-6'),
     base_r.replace('timestep ${dt}', 'timestep ${dt}\nvariable dt equal 1e-6'),
     expected='reject changed timestep', metadata={'main_timestep': 2e-6, 'resume_timestep': 1e-6})

# No skipped line is needed: equal-style step is reevaluated at the new S0.
case('runtime_dependent_eager_variable',
     base_m.replace('variable dt equal 1e-6', 'variable dt equal 1e-6*(step+1)'),
     base_r.replace('variable dt equal 1e-6', 'variable dt equal 1e-6*(step+1)'),
     expected='reject indeterminate dynamic setup substitution',
     metadata={'main_evaluation_step': 0, 'resume_evaluation_step': 50, 'main_timestep': 1e-6, 'resume_timestep': 51e-6})

for suffix in ['velocity all set 1 0 0', 'set group all density 1', 'delete_atoms group all', 'include extra.in']:
    case('suffix_' + suffix.split()[0], base_m, base_r.replace('print "done"', suffix + '\nprint "done"'), expected='reject')
for tail in [' every 10 "velocity all set 1 0 0"', ' pre no', ' post no', ' start 0', ' stop 100', ' upto']:
    case('resume_first_run_' + tail.split()[0], base_m, base_r.replace('run 50', 'run 50' + tail), expected='reject')
    case('main_first_run_' + tail.split()[0], base_m.replace('run 100', 'run 100' + tail), base_r, expected='reject')
case('continued_first_run', base_m, base_r.replace('run 50', 'run &\n50'), expected='reject')
case('changed_timestep_literal', base_m, base_r.replace('timestep ${dt}', 'timestep 2e-6'), expected='reject')
case('missing_variable', base_m, base_r.replace('variable dt equal 1e-6\n', ''), expected='reject')

for name, ckpt in [('compress_named', 'restart_compress_50.bin'), ('compress_renamed', 'restart_other_50.bin')]:
    case(name,
         'units si\nrestart 10 ' + ckpt.replace('50', '*') + '\nlabel compress\nrun 100\njump SELF compress\n',
         'units si\nread_restart ' + ckpt + '\nrestart 10 ' + ckpt.replace('50', '*') + '\nlabel compress\nrun 100\njump SELF compress\n',
         ckpt, expected='reject')

# Path mismatch and mesh content are pre-declared bounded limitations.
case('checkpoint_basename_alias', base_m.replace('restart_settling_*.bin', 'original/restart_settling_*.bin'),
     base_r.replace('read_restart restart_settling_50.bin', 'read_restart different/restart_settling_50.bin').replace(
         'restart 10 restart_settling_*.bin', 'restart 10 original/restart_settling_*.bin'),
     'different/restart_settling_50.bin', expected='known bounded acceptance: checkpoint identified by basename')

# Apply the same independently designed defect to the received D2 pair, copying
# both into evidence. These are synthetic derivatives, never the actual run.
d2 = REPO / 'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942'
d2m = (d2 / 'input_kg50_d2_b50.liggghts').read_text(encoding='utf-8')
d2r = (d2 / 'input_kg50_d2_b50_r4.liggghts').read_text(encoding='utf-8')
d2ck = 'restart_kg50_d2_b50/restart_settling_20001.bin'
case('d2_received_baseline', d2m, d2r, d2ck, 20001, expected='accept received original fixture', ts=2000)
gravity = 'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0'
mg = 'variable g_probe equal 98.1\nvariable g_probe equal 196.2\nfix gravi all gravity ${g_probe} vector 0.0 0.0 -1.0\nvariable g_probe equal 98.1'
rg = mg.replace('variable g_probe equal 196.2\n', '')
assert d2m.count(gravity) == d2r.count(gravity) == 1
case('d2_drop_intermediate_variable_definition', d2m.replace(gravity, mg), d2r.replace(gravity, rg), d2ck, 20001,
     expected='reject changed consumed gravity value', metadata={'main_gravity': 196.2, 'resume_gravity': 98.1, 'synthetic_derivative': True}, ts=2000)
dyn = 'variable g_probe equal 98.1*(step+1)\nfix gravi all gravity ${g_probe} vector 0.0 0.0 -1.0'
case('d2_runtime_dependent_eager_variable', d2m.replace(gravity, dyn), d2r.replace(gravity, dyn), d2ck, 20001,
     expected='reject indeterminate dynamic setup substitution', metadata={'main_evaluation_step': 1, 'resume_evaluation_step': 20001,
     'main_gravity': 196.2, 'resume_gravity': 1962196.2, 'synthetic_derivative': True}, ts=2000)

# Recheck archived reviewer inputs unchanged, copied only to the evidence tree.
old = REPO / 'docs/reviews/codex_kg50_resume_recheck_20261028/independent/deck'
main07 = (REPO / 'docs/data/kg50_decks_20261026_v2/kg50_d07_b40/input_kg50_d07_b40.liggghts').read_text(encoding='utf-8')
ck07 = 'restart_kg50_d07_b40/restart_settling_20001.bin'
for name in ['baseline', 'suffix_velocity', 'suffix_density', 'suffix_delete', 'suffix_include',
             'first_run_every', 'duplicate_loop_label', 'missing_target_variable']:
    case('archived_' + name, main07, (old / (name + '.liggghts')).read_text(encoding='utf-8'), ck07, 20001,
         expected='accept' if name == 'baseline' else 'reject', ts=2000)
for name in ['after_settling_baseline', 'after_settling_first_long_changed_300000', 'after_settling_damp_mismatch']:
    case('archived_' + name, main07, (old / (name + '.liggghts')).read_text(encoding='utf-8'),
         'restart_kg50_d07_b40/restart_after_settling.bin', 200001,
         expected='accept' if name.endswith('_baseline') else 'reject', ts=2000)
r075 = REPO / 'docs/data/pure_se_r075_20260927'
case('archived_compress_r075', (r075 / 'input_pse_r075_a.liggghts').read_text(encoding='utf-8'),
     (r075 / 'input_pse_r075_a_r30.liggghts').read_text(encoding='utf-8'),
     'restart_pse_r075_a/restart_compress_1500000.bin', 1500000, expected='reject',
     files={'plate_pse_r075_a_r30.stl': ''}, ts=2000)

case('parser_nbsp', base_m, base_r.replace('timestep ${dt}', 'timestep\u00a0${dt}'),
     expected='known parser mismatch: static accepts; no engine execution')
case('parser_continuation_no_separator', base_m, base_r.replace('timestep ${dt}', 'timestep&\n${dt}'),
     expected='known parser mismatch: static accepts; no engine execution')
mesh_m = base_m + 'fix top all mesh/surface file original.stl type 1\n'
mesh_r = base_r + 'fix top all mesh/surface file replacement.stl type 1\n'
case('mesh_empty_existing_file', mesh_m, mesh_r, expected='known bounded acceptance: file existence only',
     files={'replacement.stl': ''})

(OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')

"""Execute the pin's unmodified embedded Python CLI; no shell or DEM execution.

Run: python -I -X utf8 -B reproduce_deck.py
Output is confined to this script's directory. Product files are only read.
The raw trial truncator is reproduced only for plain one-line run fixtures;
its exact source line is recorded and prefixes are compared byte-for-byte.
"""
from pathlib import Path
import hashlib, json, re, subprocess, sys, types

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
REPO = ROOT / 'repo'
SOURCE = REPO / 'scripts/resume_ckpt.sh'
EXPECTED_SHA = 'e59c43e688b2b9a6c23a337ceee2b28214ed3f6c76bd69b7f2402f926336dae8'
raw = SOURCE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA
body = raw.split(b"<<'PY'\n", 1)[1].split(b'\nPY\n', 1)[0]
CHECKER = OUT / 'pinned_embedded_cli.py'
CHECKER.write_bytes(body)

t = types.ModuleType('pinned_test_fixtures')
t.__file__ = str(REPO / 'scripts/test_resume_ckpt.py')
exec(compile(Path(t.__file__).read_text(encoding='utf-8'), t.__file__, 'exec'), t.__dict__)
BASE = t.with_tmpl(t.res_good())
assert BASE.count('run 180000\n') == 1

def cli(*args):
    p = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', str(CHECKER), *map(str, args)],
                       capture_output=True, encoding='utf-8', cwd=OUT, timeout=20)
    return {'argv': [str(x) for x in args], 'rc': p.returncode,
            'stdout': p.stdout, 'stderr': p.stderr}

def trial_prefix(text):
    """Literal raw-awk behavior for these ASCII plain-line run fixtures only."""
    acc = []
    for line in text.splitlines(keepends=True):
        w = line.split()
        if len(w) >= 2 and w[0] == 'run' and w[1].isascii() and w[1].isdigit() and int(w[1]) > 1:
            acc.append('run %d\n' % min(2000, int(w[1])))
            return ''.join(acc)
        acc.append(line)
    raise AssertionError('missing first long run')

variants = {
    'baseline': BASE,
    'suffix_velocity': BASE.replace('run 180000\n', 'run 180000\nvelocity all set 1.0 0.0 0.0\n', 1),
    'suffix_density': BASE.replace('run 180000\n', 'run 180000\nset group all density 1.0\n', 1),
    'suffix_delete': BASE.replace('run 180000\n', 'run 180000\ndelete_atoms group all\n', 1),
    'suffix_include': BASE.replace('run 180000\n', 'run 180000\ninclude extra.in\n', 1),
    'first_run_every': BASE.replace('run 180000\n', 'run 180000 every 1000 "velocity all set 1.0 0.0 0.0"\n', 1),
    'first_run_pre_no': BASE.replace('run 180000\n', 'run 180000 pre no\n', 1),
    'first_run_upto_wrong': BASE.replace('run 180000\n', 'run 180000 upto\n', 1),
    'first_run_upto_right': BASE.replace('run 180000\n', 'run 200001 upto\n', 1),
    'duplicate_loop_label': BASE.replace('run 180000\n', 'label loop_press\nrun 180000\n', 1),
    'missing_target_variable': re.sub(r'(?m)^variable target_press[^\n]*\n', '', BASE),
    'missing_compute_control': re.sub(r'(?m)^compute zmax[^\n]*\n', '', BASE),
    'changed_timestep_control': BASE.replace('timestep       ${dt}', 'timestep       2.0e-6', 1),
}
# Accommodate the frozen deck's actual spacing, but ensure the negative control changes it.
variants['changed_timestep_control'] = re.sub(r'(?m)^timestep\s+[^\n]+', 'timestep 2.0e-6', BASE, count=1)

records = []
baseprefix = trial_prefix(BASE)
for name, text in variants.items():
    path = OUT / (name + '.liggghts'); path.write_bytes(text.encode())
    rec = {'case': name, 'check': cli(t.MAIN, path, t.CKPT, 20001, OUT)}
    pre = trial_prefix(text)
    pp = OUT / (name + '_trial.liggghts'); pp.write_bytes(pre.encode())
    rec.update(trial_prefix_same_as_baseline=(pre == baseprefix),
               trial_prefix_sha256=hashlib.sha256(pre.encode()).hexdigest(),
               trial_steps=cli('--trial-steps', pp))
    records.append(rec)

fixes = {
    'one_short': BASE.replace('run 180000\n', 'run 179999\n', 1),
    'two_short': BASE.replace('run 180000\n', 'run 179998\n', 1),
    'one_short_with_physics_mismatch': re.sub(r'(?m)^timestep\s+[^\n]+', 'timestep 2.0e-6', BASE.replace('run 180000\n', 'run 179999\n', 1), count=1),
    'one_short_with_suffix_velocity': BASE.replace('run 180000\n', 'run 179999\nvelocity all set 1.0 0.0 0.0\n', 1),
}
fix_records = []
for name, text in fixes.items():
    p = OUT / ('fix_' + name + '.liggghts'); old = text.encode(); p.write_bytes(old)
    result = cli('--fix-run', t.MAIN, p, t.CKPT, 20001, OUT)
    new = p.read_bytes()
    fix_records.append({'case': name, 'result': result, 'changed': old != new,
                        'only_one_run_step_change': new == old.replace(b'run 179999\n', b'run 180000\n', 1),
                        'recheck': cli(t.MAIN, p, t.CKPT, 20001, OUT)})

strip_records = []
for name, content in {
    'safe': b'# whole comment\r\n\t# second\nprint "a # b" # inline comment\r\nrun 1\n',
    'continuation_comment': b'run &\n# interposed comment\n2000\n',
}.items():
    d = OUT / ('strip_' + name); d.mkdir(exist_ok=True)
    p = d / 'input_test.liggghts'; p.write_bytes(content)
    result = cli('--strip-comments', d)
    strip_records.append({'case': name, 'result': result, 'before_hex': content.hex(),
                          'after_hex': p.read_bytes().hex(), 'changed': content != p.read_bytes()})

after_records = []
for name, text in {'baseline': t.res_after(tmpl=True),
                   'first_long_changed_300000': t.res_after('stab300000', tmpl=True),
                   'damp_mismatch': t.res_after('damp_settle', tmpl=True)}.items():
    p = OUT / ('after_settling_' + name + '.liggghts'); p.write_bytes(text.encode())
    after_records.append({'case': name, 'result': cli(t.MAIN, p, t.CKPT_AS, 200001, OUT)})

# Supplied actual pure-SE R075 original/resume deck pair, not a fabricated model.
lm = REPO / 'docs/data/pure_se_r075_20260927/input_pse_r075_a.liggghts'
lr = REPO / 'docs/data/pure_se_r075_20260927/input_pse_r075_a_r30.liggghts'
(OUT / 'plate_pse_r075_a_r30.stl').write_bytes(b'')  # existing checker tests mere existence, no DEM is run
loop_result = cli(lm, lr, 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000, OUT)
before_loop = lm.read_text(encoding='utf-8').split('label loop_press')[0]
assert 'reset_timestep' not in before_loop and 'read_restart' not in before_loop
pre_runs = [int(m.group(1)) for m in re.finditer(r'(?m)^\s*run\s+([0-9]+)\s*$', before_loop)]
assert pre_runs == [1, 200000, 1, 200000]
loop_start = sum(pre_runs); checkpoint = 1500000; chunk = 5000
phase = (checkpoint-loop_start) % chunk
remaining = chunk-phase if phase else chunk
loop_record = {'result': loop_result, 'original_run_prefix': pre_runs,
               'loop_start': loop_start, 'checkpoint': checkpoint, 'chunk': chunk,
               'position_within_original_loop_run': phase,
               'remaining_to_original_next_pressure_check': remaining,
               'original_next_pressure_check': checkpoint+remaining,
               'resume_next_pressure_check': checkpoint+chunk,
               'extra_steps_before_check': chunk-remaining,
               'limitation': 'Step arithmetic + actual static CLI only; no DEM pressure/trajectory was simulated.'}
rp = OUT / 'loop_first_numeric_remaining2.liggghts'
rp.write_text(re.sub(r'(?m)^(\s*run\s+)5000\s*$', r'\g<1>2', lr.read_text(encoding='utf-8'), count=1), encoding='utf-8')
loop_record['first_numeric_remaining2_candidate'] = cli(lm, rp, 'restart_pse_r075_a/restart_compress_1500000.bin', 1500000, OUT)
loop_record['remaining2_candidate_limit'] = 'This numeric-only change is NOT a complete correct resume deck: later iterations must remain 5000, so the actual fix needs a distinct initial partial-iteration path.'

result = {'source': str(SOURCE), 'source_sha256': EXPECTED_SHA,
          'embedded_bytes_sha256': hashlib.sha256(body).hexdigest(),
          'trial_cutter_source': next(s for s in raw.decode().splitlines() if "awk -v t=$TS" in s),
          'static_cases': records, 'fix_run_cases': fix_records, 'strip_comment_cases': strip_records,
          'after_settling_cases': after_records, 'supplied_compress_loop_case': loop_record,
          'limits': ['No Bash, SLURM, MPI, LIGGGHTS, or real checkpoint execution.',
                     'Trial prefix uses literal one-line ASCII truncator semantics, not a different parser for general decks.',
                     'All production bytes are unchanged; extracted embedded Python body is byte-for-byte identical.']}
(OUT / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
for r in records:
    print('%-30s static_rc=%d prefix_equal=%s trial_steps_rc=%d' % (r['case'], r['check']['rc'], r['trial_prefix_same_as_baseline'], r['trial_steps']['rc']))
for r in fix_records:
    print('FIX %-26s rc=%d changed=%s' % (r['case'], r['result']['rc'], r['changed']))
for r in strip_records:
    print('STRIP %-24s rc=%d changed=%s' % (r['case'], r['result']['rc'], r['changed']))
for r in after_records:
    print('AFTER %-24s rc=%d' % (r['case'], r['result']['rc']))
print('LOOP static_rc=%d old_next=%d new_next=%d delayed_steps=%d' % (loop_result['rc'], checkpoint+remaining, checkpoint+chunk, chunk-remaining))

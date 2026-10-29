"""CPU-only launch-boundary evidence; no Bash, scheduler, MPI, or LIGGGHTS.

Runs the unmodified embedded Python functions from the reviewed wrapper.  The
three grep checks are independently transcribed as regular-expression/string
predicates.  This does not assert that a shell or a real scheduler was executed.
"""
import contextlib
import hashlib
import io
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
REPO = BASE / 'repo'
OUT = Path(__file__).resolve().parent
TOOL = REPO / 'scripts/resume_ckpt.sh'
source = TOOL.read_text(encoding='utf-8')
embedded = source.split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0]
defs = embedded.split("if len(sys.argv) == 3 and sys.argv[1] == '--strip-comments':", 1)[0]
ns = {'__name__': 'reviewed_embedded_functions'}
exec(compile(defs, str(TOOL) + ' [exact embedded definitions]', 'exec'), ns)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def call(fn, *args):
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        result = ns[fn](*map(str, args))
    return result, capture.getvalue()

case, sfx, np = 'kg50_d2_b50', 'r56', 56
fixture = OUT / 'runner_suffix'
fixture.mkdir(exist_ok=True)
ckpt = f'restart_{case}/restart_settling_20001.bin'
(fixture / f'restart_{case}').mkdir(exist_ok=True)
(fixture / ckpt).write_bytes(b'CPU fixture checkpoint placeholder; not a DEM restart\n')
source_main = REPO / f'docs/data/kg50_decks_20261027_v3_b50/{case}/input_{case}.liggghts'
main = fixture / f'input_{case}.liggghts'
main.write_bytes(source_main.read_bytes())
supplied = REPO / f'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/input_{case}_r4.liggghts'
res = fixture / f'input_{case}_{sfx}.liggghts'
res.write_bytes(supplied.read_bytes())
good_problems, good_notes = ns['check'](str(main), str(res), ckpt, 20001, str(fixture))
assert good_problems == [], good_problems
trial = fixture / f'input_{case}_{sfx}t.liggghts'
cut_rc, cut_out = call('cut_trial', res, 2000, trial)
assert cut_rc == 0
steps_rc, steps_out = call('trial_steps', trial)
assert steps_rc == 0

# A normal-looking runner with one additional filename suffix passes the exact
# substring gate at resume_ckpt.sh:1151.  Its two actual -in targets exist.
runner = fixture / f'run_{case}_{sfx}.sh'
runner_text = (f'#!/bin/bash\n#SBATCH --job-name={case}_{sfx}\n'
               f'#SBATCH --output=logs/output_{case}_{sfx}_%j.out\n'
               f'#SBATCH -n {np}\n#SBATCH --time=5-00:00:00\n'
               f'cd /logical/review/root/{case}\n'
               f'mpirun --oversubscribe --bind-to none -np {np} lmp_mpi '
               f'-in input_{case}_{sfx}.liggghts.bak\n')
runner.write_text(runner_text, encoding='utf-8', newline='\n')
trial_runner_text = runner_text.replace(f'{case}_{sfx}', f'{case}_{sfx}t')
trial_runner_text = re.sub(r'^#SBATCH --time=.*', '#SBATCH --time=01:00:00', trial_runner_text, flags=re.M)
trial_runner = fixture / f'run_{case}_{sfx}t.sh'
trial_runner.write_text(trial_runner_text, encoding='utf-8', newline='\n')
runner_predicates = {
    'SBATCH_n_exact_line': bool(re.search(rf'^#SBATCH -n {np}$', runner_text, re.M)),
    'main_mpirun_substring': f'--oversubscribe --bind-to none -np {np} lmp_mpi' in runner_text,
    'trial_in_substring': f'-np {np} lmp_mpi -in input_{case}_{sfx}t.liggghts' in trial_runner_text,
}
assert all(runner_predicates.values())
actual_main = fixture / f'input_{case}_{sfx}.liggghts.bak'
actual_trial = fixture / f'input_{case}_{sfx}t.liggghts.bak'
lines = res.read_text(encoding='utf-8').splitlines(keepends=True)
index = next(i for i, line in enumerate(lines) if re.match(r'^run 180000\b', line))
lines.insert(index + 1, 'velocity all set 1.0 0.0 0.0\n')
actual_main.write_text(''.join(lines), encoding='utf-8', newline='\n')
bad_problems, bad_notes = ns['check'](str(main), str(actual_main), ckpt, 20001, str(fixture))
assert bad_problems and any('velocity all set' in p for p in bad_problems)
bad_cut_rc, bad_cut_out = call('cut_trial', actual_main, 2000, actual_trial)
assert bad_cut_rc == 0 and actual_trial.read_bytes() == trial.read_bytes()
manifest = {res.name: sha(res), runner.name: sha(runner)}
assert all(sha(fixture / name) == digest for name, digest in manifest.items())
(fixture / 'main_inputs.sha256').write_text(''.join(f'{digest}  /logical/review/root/{case}/{name}\n' for name, digest in manifest.items()), encoding='utf-8')

# Checkpoint bytes are recorded separately, but not covered by main_inputs.
ck_before = sha(fixture / ckpt)
(fixture / ckpt).write_bytes(b'Different CPU checkpoint placeholder after trial\n')
ck_after = sha(fixture / ckpt)
manifest_still_matches = all(sha(fixture / name) == digest for name, digest in manifest.items())
assert ck_before != ck_after and manifest_still_matches

# qre's escaped literal case/SFX plus fixed alternatives, transcribed from
# :1073,1080.  This is not a live squeue or grep result.
queue_pattern = re.compile(re.escape(case) + r'(_ins|_' + re.escape(sfx) + r't?|_r[0-9]+t?)?')
queue_names = {name: bool(queue_pattern.fullmatch(name)) for name in
               (case, case + '_ins', case + '_r56', case + '_r56t', case + '_r4', case + '_r4t', case + '_other')}

# fin is a numeric-token grammar, not a floating-point finiteness predicate.
fin = re.compile(r'^[-+]?([0-9]+[.]?[0-9]*|[.][0-9]+)([eE][-+]?[0-9]+)?$')
numeric_tokens = {tok: {'fin_regex': bool(fin.fullmatch(tok)), 'python_float': str(float(tok))}
                  for tok in ('0.0955', 'nan', '+nan', 'inf', '1e9999')}

results = {
    'tool_sha256': sha(TOOL),
    'execution_scope': {'exact_embedded_python': 'EXECUTED', 'grep_sed_sha_predicates': 'INDEPENDENT_PYTHON_TRANSCRIPTION',
                        'bash_fake_scheduler': 'NOT_EXECUTED', 'slurm_mpi_liggghts': 'NOT_EXECUTED'},
    'runner_suffix_false_green': {
        'checked_deck_problems': good_problems,
        'checked_deck_notes': good_notes,
        'checked_cut': {'rc': cut_rc, 'stdout': cut_out},
        'checked_trial_steps': {'rc': steps_rc, 'stdout': steps_out},
        'runner_gate_predicates': runner_predicates,
        'checked_deck': res.name,
        'actual_main_in': actual_main.name,
        'checked_trial': trial.name,
        'actual_trial_in': actual_trial.name,
        'actual_main_if_checked_problems': bad_problems,
        'actual_trial_identical_to_checked_trial': sha(actual_trial) == sha(trial),
        'manifest_matches': manifest_still_matches,
        'actual_main_covered_by_manifest': actual_main.name in manifest,
        'new_main_submission_observed': False,
        'interpretation': 'Exact Python static validation passes checked input. The shell predicates also pass, but actual main runner selects an unchecked .bak deck with changed suffix behavior. Trial .bak is byte-identical to the validated trial. This is a source-path proof, not a Bash/scheduler execution.',
    },
    'checkpoint_receipt_gap': {'before_sha': ck_before, 'after_sha': ck_after, 'main_manifest_still_matches': manifest_still_matches,
                               'classification': 'receipt/integrity limitation; no P1 claimed from file mutation alone'},
    'queue_name_scope': queue_names,
    'numeric_token_grammar': numeric_tokens,
}
(OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'checked_static_problem_count': len(good_problems), 'actual_static_problem_count': len(bad_problems),
                  'runner_predicates': runner_predicates, 'trial_bytes_equal': sha(actual_trial) == sha(trial),
                  'manifest_matches': manifest_still_matches, 'bash_executed': False}, ensure_ascii=False, indent=2))

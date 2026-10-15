"""Independent grammar prerequisites audit. Synthetic fixtures only; no simulator.

The target history reader's fixture helper creates the positive control, then
independent mutations distinguish the raw reader from the cached-JSON gate.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[1]
KIT = BASE / 'source/docs/data/ps45_unload_20261009'
HIST = KIT / 'history_test'
ap = argparse.ArgumentParser()
ap.add_argument('--run-id', default='cases', help='Unique suffix for evidence/grammar_<run-id>; use a new value on rerun.')
opts = ap.parse_args()
if not opts.run_id.replace('_', '').replace('-', '').isalnum():
    ap.error('--run-id must contain letters, numbers, underscores or hyphens')
OUT = BASE / ('evidence/grammar_' + opts.run_id)
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(KIT))
import ul_reader as ur

spec = importlib.util.spec_from_file_location('grammar_target_history', HIST / 'read_history.py')
rh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rh)
P = rh.load_params()
LMP_SHA = hashlib.sha256(b'NOT A BINARY: synthetic grammar audit identity').hexdigest()
results = {}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_case(name):
    # Do not erase existing evidence on rerun.
    rd = OUT / name
    if rd.exists():
        raise RuntimeError(f'Refusing to overwrite existing case {rd}')
    rd.mkdir()
    rh.synth_gram_run(str(rd), P)
    kp = rd / 'kit_metadata'
    kp.mkdir()
    shutil.copy2(HIST / 'SHA256SUMS', kp / 'SHA256SUMS')
    for stage, deck in ur.GRAMMAR_STAGES:
        for filename in (deck, 'plate_hist.stl'):
            shutil.copy2(HIST / filename, rd / stage / filename)
        write(rd / stage / 'deck.txt', deck + '\n')
    write(rd / 'run_manifest.txt',
          f'mode=gram\nend=synthetic\nkit={kp}\nsums_sha256={digest(kp / "SHA256SUMS")}\nlmp_sha256={LMP_SHA}\n')
    v = rh.grammar_info(str(rd), P)
    if v['status'] != 'PASS':
        raise AssertionError(v)
    vp = rd / 'grammar_verdict.json'
    write(vp, json.dumps(v, ensure_ascii=False, indent=2))
    return rd, vp, v


def record(name, expected_gate, mutate=None, lmp_sha=LMP_SHA, raw_expected=None):
    rd, vp, v = make_case(name)
    if mutate:
        mutate(rd, vp, v)
    ok, problems, receipt = ur.grammar_prereq(str(vp), lmp_sha)
    raw = rh.grammar_info(str(rd), P)
    good = ok == expected_gate and (raw_expected is None or raw['status'] == raw_expected)
    results[name] = dict(expected_gate=expected_gate, gate=ok,
                         problems=problems, raw_status=raw['status'], raw_problems=raw['problems'],
                         expected_raw=raw_expected, expectation_satisfied=good,
                         verdict_sha256=digest(vp), case_dir=str(rd))


def json_edit(rd, vp, v, change):
    change(v)
    write(vp, json.dumps(v, ensure_ascii=False, indent=2))


record('positive_actual_reader', True, raw_expected='PASS')
record('other_binary', False, lmp_sha='0' * 64, raw_expected='PASS')
record('missing_check', False, lambda r, p, v: json_edit(r, p, v, lambda d: d['checks'].pop('GB_restart_state')))
record('boolean_exit_code', False, lambda r, p, v: json_edit(r, p, v, lambda d: d.update(exit_code=False)))
record('check_integer_one', False, lambda r, p, v: json_edit(r, p, v, lambda d: d['checks'].update(GA_tech=1)))
record('check_false', False, lambda r, p, v: json_edit(r, p, v, lambda d: d['checks'].update(GA_tech=False)))
record('wrong_run_dir', False, lambda r, p, v: json_edit(r, p, v, lambda d: d.update(run_dir=str(r.parent))))
record('bad_ga_rc', False, lambda r, p, v: write(r / 'GA/rc', '1\n'), raw_expected='FAIL')
record('missing_manifest_end', False,
       lambda r, p, v: write(r / 'run_manifest.txt', (r / 'run_manifest.txt').read_text(encoding='utf-8').replace('end=synthetic\n', '')))
record('wrong_grammar_deck', False, lambda r, p, v: write(r / 'GA/in.hist_grammar.liggghts', '# wrong deck\n'))
record('wrong_plate', False, lambda r, p, v: write(r / 'GB/plate_hist.stl', 'solid wrong\nendsolid\n'))
record('wrong_deck_name', False, lambda r, p, v: write(r / 'GB/deck.txt', 'in.hist_syntax_probe.liggghts\n'))
record('raw_ga_error_cached_pass', True,
       lambda r, p, v: write(r / 'GA/screen.out', (r / 'GA/screen.out').read_text(encoding='utf-8') + '\nERROR: independent injected raw error\n'), raw_expected='FAIL')
record('raw_gb_mesh_wrong_cached_pass', True,
       lambda r, p, v: write(r / f'GB/probe/mesh_{rh.grammar_expect(P)["GB"]["start"]}.stl',
                             'solid changed\n vertex 0 0 99\nendsolid\n'), raw_expected='FAIL')
record('raw_gb_screen_missing_cached_pass', True, lambda r, p, v: (r / 'GB/screen.out').unlink(), raw_expected='FAIL')
record('raw_gb_state_wrong_cached_pass', True,
       lambda r, p, v: write(r / f'GB/restart/state_g_{rh.grammar_expect(P)["GB"]["ends"][-1]}.in',
                             'variable gr_rstep equal 0\nvariable gr_k equal 0\nvariable gr_pz equal 0\n'), raw_expected='FAIL')


def script_hash_change(rd, vp, v):
    sums = rd / 'kit_metadata/SHA256SUMS'
    text = sums.read_text(encoding='utf-8')
    changed = []
    for line in text.splitlines():
        words = line.split()
        changed.append('0' * 64 + '  ' + words[1] if len(words) == 2 and words[1] in ('read_history.py', 'run_history.sh') else line)
    write(sums, '\n'.join(changed) + '\n')
    manifest = rd / 'run_manifest.txt'
    lines = manifest.read_text(encoding='utf-8').splitlines()
    write(manifest, '\n'.join(f'sums_sha256={digest(sums)}' if l.startswith('sums_sha256=') else l for l in lines) + '\n')


record('different_reader_runner_seal', True, script_hash_change, raw_expected='PASS')

sh = shutil.which('bash')
shell = {'path': sh, 'ran_simulator': False}
if sh:
    try:
        p = subprocess.run([sh, '--noprofile', '--norc', '-c', 'exit 0'], capture_output=True, text=True, timeout=15)
        shell.update(rc=p.returncode, stdout=p.stdout, stderr=p.stderr)
    except Exception as e:
        shell['exception'] = repr(e)

summary = {'pin': 'eaecfba2a2dfbff6f13222f6afeb01d8ebeb5a84',
           'synthetic_only': True, 'lmp_sha_is_synthetic': True,
           'target_calls': ['read_history.grammar_info', 'ul_reader.grammar_prereq'],
           'results': results, 'shell_smoke': shell,
           'all_expectations_satisfied': all(v['expectation_satisfied'] for v in results.values()),
           'case_count': len(results),
           'interpretation': 'Cached PASS is trusted; raw-log drift and runner/reader hash changes are intentionally outside grammar_prereq validation. These cases do not establish an actual simulator PASS.'}
write(BASE / 'evidence/grammar_provenance.json', json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(summary, ensure_ascii=False, indent=2))
sys.exit(0 if summary['all_expectations_satisfied'] else 1)

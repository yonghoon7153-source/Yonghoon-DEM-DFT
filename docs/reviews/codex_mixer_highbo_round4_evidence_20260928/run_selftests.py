import json, os, pathlib, subprocess, sys
root = pathlib.Path(__file__).resolve().parent
env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
results = []
for name in ('measure_bed_aspect', 'check_contact_validity', 'measure_mixing_index', 'mixer_deck_diff', 'mixer_restart_phase_test', 'make_mixer_deck'):
    p = subprocess.run([sys.executable, str(root/'scripts'/f'{name}.py'), '--selftest'], cwd=root, env=env, capture_output=True, text=True, encoding='utf-8', timeout=180)
    results.append(dict(script=name, rc=p.returncode, stdout=p.stdout, stderr=p.stderr))
    print(name, p.returncode, p.stdout[-450:], p.stderr[-1000:], flush=True)
(root/'selftests_output.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
raise SystemExit(any(x['rc'] for x in results))

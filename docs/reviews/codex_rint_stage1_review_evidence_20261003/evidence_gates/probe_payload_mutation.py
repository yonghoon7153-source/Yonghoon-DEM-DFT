"""Real producer probe: OFF, ON, and only main electronic rint keyword removed."""
import ast
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'
OUT = ROOT / 'evidence_gates' / 'payload_mutation'
sys.path.insert(0, str(SOURCE / 'scripts'))


def mutated_child(target=1980):
    import mpm_webapp_payload as payload
    path = SOURCE / 'scripts/mpm_webapp_payload.py'
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    changed = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and node.lineno == target:
            original = [x.arg for x in node.keywords]
            node.keywords = [x for x in node.keywords if x.arg != 'rint']
            assert len(original) == len(node.keywords) + 1, original
            changed.append(node.lineno)
    assert changed == [target], changed
    print(f'MUTATION: remove only rint keyword from real solve at source line {target}', flush=True)
    exec(compile(tree, str(path), 'exec'), payload.__dict__)
    payload.main()


def run_arm(item):
    name, cmd = item
    start = time.perf_counter()
    r = subprocess.run(cmd, cwd=SOURCE, capture_output=True, text=True,
                       encoding='utf-8', errors='replace', timeout=300)
    elapsed = time.perf_counter() - start
    (OUT / f'{name}.stdout.txt').write_text(r.stdout, encoding='utf-8')
    (OUT / f'{name}.stderr.txt').write_text(r.stderr, encoding='utf-8')
    res = {'exit': r.returncode, 'seconds': elapsed, 'command': cmd}
    p = OUT / f'{name}.json'
    if p.exists():
        import check_method_discipline as discipline
        payload = json.loads(p.read_text(encoding='utf-8'))
        s3 = payload['mpm_metrics']['step3']
        man = s3['manifest']
        errs, warns = [], []
        discipline.smoke_assert_payload(str(p), name, errs, warns, expect={
            'electronic': 'complete', 'thermal': 'disabled',
            'collector_geom': 'disabled' if '--no-collector' in cmd else 'complete',
            'ionic': 'disabled', 'pore': 'disabled', 'pnm': 'disabled'})
        res.update(sigma_e=s3.get('sigma_e_eff_S_cm'),
                   interface_model=man.get('interface_model'),
                   table=man.get('interface_rint_e_ohm_cm2'),
                   faces=man.get('interface_faces'), collector=s3.get('collector_geometric'),
                   J_smoke_assert_errors=errs, J_smoke_assert_warnings=warns)
    print(name, json.dumps(res, ensure_ascii=False), flush=True)
    return name, res


if __name__ == '__main__':
    if '--mutant-child' in sys.argv:
        sys.argv.remove('--mutant-child')
        target = 1980
        if '--mutation-line' in sys.argv:
            at = sys.argv.index('--mutation-line')
            target = int(sys.argv[at + 1])
            del sys.argv[at:at+2]
        mutated_child(target)
        raise SystemExit(0)
    import check_method_discipline as discipline
    OUT.mkdir(exist_ok=True)
    am, se, ph, fid, dia = discipline._smoke_fixture(str(OUT))
    flags = ['--scaffold', am, '--se', se, '--n-vox', discipline._SMOKE_NVOX,
             '--step3-vox', discipline._SMOKE_VOX, '--no-ion', '--no-pore',
             '--no-thermal', '--no-trackb', '--no-field', '--no-collector', '--no-step4']
    rint = ['--step3-rint-e', 'AM_S|AM_S=0.001']
    commands = {
        'off': [sys.executable, '-u', str(SOURCE / 'scripts/mpm_webapp_payload.py'), *flags,
                '--out', str(OUT / 'off.json')],
        'on': [sys.executable, '-u', str(SOURCE / 'scripts/mpm_webapp_payload.py'), *flags, *rint,
               '--out', str(OUT / 'on.json')],
        'mutant_on': [sys.executable, '-u', str(Path(__file__)), '--mutant-child', *flags, *rint,
                      '--out', str(OUT / 'mutant_on.json')],
    }
    collector_flags = [f for f in flags if f != '--no-collector']
    for name, target in [('on_collector', None), ('mutant_wetted', 2252), ('mutant_bare', 2255)]:
        if target:
            prefix = [str(Path(__file__)), '--mutant-child', '--mutation-line', str(target)]
        else:
            prefix = [str(SOURCE / 'scripts/mpm_webapp_payload.py')]
        commands[name] = [sys.executable, '-u', *prefix, *collector_flags, *rint,
                          '--out', str(OUT / f'{name}.json')]
    commands['ion_disabled'] = [sys.executable, '-u', str(SOURCE / 'scripts/mpm_webapp_payload.py'),
                               *flags, '--step3-rint-i', 'SDCP|SE=0.001',
                               '--out', str(OUT / 'ion_disabled.json')]
    commands['zero_table'] = [sys.executable, '-u', str(SOURCE / 'scripts/mpm_webapp_payload.py'),
                             *flags, '--step3-rint-e', 'AM_S|AM_S=0',
                             '--out', str(OUT / 'zero_table.json')]
    if '--extended-only' in sys.argv:
        commands = {k: v for k, v in commands.items() if k not in ('off', 'on', 'mutant_on')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = dict(pool.map(run_arm, commands.items()))
    results['source_sha256'] = hashlib.sha256((SOURCE / 'scripts/mpm_webapp_payload.py').read_bytes()).hexdigest()
    summary_name = 'summary_extended.json' if '--extended-only' in sys.argv else 'summary.json'
    (OUT / summary_name).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')

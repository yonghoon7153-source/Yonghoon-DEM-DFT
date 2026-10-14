"""Offline review reproduction; no native DEM, shell runner, Git or network calls."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

def verify_sources():
    checks = []
    for manifest, folder in [('source_manifest.json', 'source'), ('upstream_manifest.json', 'upstream')]:
        m = json.loads((ROOT / manifest).read_text(encoding='utf-8'))
        failures = []
        for rec in m['files']:
            data = (ROOT / folder / rec['path']).read_bytes()
            if hashlib.sha256(data).hexdigest() != rec['sha256']:
                failures.append(rec['path'])
            if rec.get('blob_sha'):
                git_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                if git_blob != rec['blob_sha']:
                    failures.append(rec['path'] + ' [git blob]')
        checks.append({'manifest': manifest, 'pin': m['pin'], 'count': len(m['files']), 'failures': failures})
        assert not failures, failures
    return checks

def main():
    (ROOT / 'evidence').mkdir(exist_ok=True)
    out = {'source_checks_before': verify_sources(), 'runs': []}
    names = ['history_actual', 'history_restore', 'reader_adversarial', 'reader_continuation',
             'observer_adversarial', 'deck_control', 'kit_byte_checks']
    for name in names:
        t = time.monotonic()
        args = [sys.executable, '-X', 'utf8', '-B', str(ROOT / 'probes' / (name + '.py'))]
        p = subprocess.run(args, cwd=ROOT, capture_output=True, encoding='utf-8', timeout=90)
        log = ROOT / 'evidence' / ('reproduce_' + name + '.log')
        log.write_text(p.stdout + '\nSTDERR\n' + p.stderr, encoding='utf-8')
        out['runs'].append({'probe': name, 'rc': p.returncode, 'seconds': round(time.monotonic()-t, 3),
                            'log': log.relative_to(ROOT).as_posix()})
        print(name, p.returncode)
        if p.returncode:
            print(p.stderr)
            raise RuntimeError(name)
    out['source_checks_after'] = verify_sources()
    out['native_simulation_executed'] = False
    out['shell_runner_executed_by_this_script'] = False
    (ROOT / 'evidence/final_reproduction.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Source bytes unchanged; all seven offline probes completed.')

if __name__ == '__main__':
    main()

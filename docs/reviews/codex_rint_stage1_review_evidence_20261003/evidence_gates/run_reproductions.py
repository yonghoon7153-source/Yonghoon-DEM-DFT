"""Review-only replay harness. Does not modify production sources."""
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

import numpy
import scipy

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'
OUT = ROOT / 'evidence_gates'
PROBES = 'docs/reviews/codex_rint_stage1_request_20261003'
COMMANDS = {
    'selftest_rint': ['scripts/step3_sigma.py', '--selftest-rint'],
    'probe_p1_pid_inherit': [f'{PROBES}/probe_p1_pid_inherit.py'],
    'probe_p21_face_area': [f'{PROBES}/probe_p21_face_area.py'],
    'probe_p22_cli': [f'{PROBES}/probe_p22_cli.py'],
}


def run_one(item):
    name, args = item
    start = time.perf_counter()
    result = subprocess.run([sys.executable, '-u', *args], cwd=SOURCE,
                            text=True, encoding='utf-8', errors='replace',
                            capture_output=True, timeout=1200)
    elapsed = time.perf_counter() - start
    (OUT / f'{name}.stdout.txt').write_text(result.stdout, encoding='utf-8')
    (OUT / f'{name}.stderr.txt').write_text(result.stderr, encoding='utf-8')
    record = {'command': [sys.executable, '-u', *args], 'cwd': str(SOURCE),
              'exit': result.returncode, 'seconds': elapsed}
    print(name, json.dumps(record), flush=True)
    return name, record


if __name__ == '__main__':
    metadata = {
        'utc_start': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'platform': platform.platform(), 'python': sys.version,
        'numpy': numpy.__version__, 'scipy': scipy.__version__,
        'PYTHONPATH': os.environ.get('PYTHONPATH'),
        'source_sha256': {str(p.relative_to(SOURCE)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted((SOURCE / 'scripts').glob('*.py'))},
    }
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        metadata['runs'] = dict(pool.map(run_one, COMMANDS.items()))
    (OUT / 'reproduction_metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')

    reference = (SOURCE / PROBES / 'probe_outputs.txt').read_text(encoding='utf-8')
    supplement = (ROOT / 'inputs/supplement_log.txt').read_text(encoding='utf-8')
    comparisons = {}
    for name in COMMANDS:
        replay = (OUT / f'{name}.stdout.txt').read_text(encoding='utf-8')
        significant = [line for line in replay.splitlines()
                       if line.strip() and 'STEP3 solve:' not in line]
        comparisons[name] = {
            'nonempty_lines': len(significant),
            'missing_from_reference': [line for line in significant if line not in reference],
            'missing_from_supplement': [line for line in significant if line not in supplement],
        }
    (OUT / 'reproduction_comparison.json').write_text(json.dumps(comparisons, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(comparisons, ensure_ascii=False, indent=2), flush=True)

"""Capture additional audit logs and timings, including existing rule J baseline."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence_gates'
COMMANDS = {
    'contract_edges': [sys.executable, '-u', str(OUT / 'probe_contract_edges.py')],
    'rule_J_baseline': [sys.executable, '-u', '-c',
                        'import check_method_discipline as d; e,w=d.check_entrypoint_smoke(); '
                        'print(repr((e,w))); raise SystemExit(bool(e))'],
    'rule_J_mutant': [sys.executable, '-u', '-c',
                      'import check_method_discipline as d; '
                      f'e,w=d.check_entrypoint_smoke(payload={str(OUT / "mutated_payload_entrypoint.py")!r}); '
                      'print(repr((e,w))); raise SystemExit(bool(e))'],
    'check_arm_mutant': [sys.executable, '-u', str(ROOT / 'source/scripts/sr01_stamp_compare.py'),
                         '--check-arm', str(OUT / 'payload_mutation/mutant_on.json'), '--stamp', 'point'],
}
if '--mutant-only' in sys.argv:
    COMMANDS.pop('rule_J_baseline')


def run(item):
    name, command = item
    start = time.perf_counter()
    res = subprocess.run(command, cwd=ROOT / 'source', capture_output=True, text=True,
                         encoding='utf-8', errors='replace', timeout=500)
    elapsed = time.perf_counter() - start
    (OUT / f'{name}.stdout.txt').write_text(res.stdout, encoding='utf-8')
    (OUT / f'{name}.stderr.txt').write_text(res.stderr, encoding='utf-8')
    record = dict(command=command, exit=res.returncode, seconds=elapsed)
    print(name, json.dumps(record), res.stdout[-1500:])
    return name, record


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    records = dict(pool.map(run, COMMANDS.items()))
(OUT / ('extra_mutant_metadata.json' if '--mutant-only' in sys.argv else 'extra_metadata.json')).write_text(
    json.dumps(records, indent=2), encoding='utf-8')

"""Copy our reproduction outputs and tools into the evidence folder's _repro_ours_20261020/.

usage: python3 -I copy_repro.py <scratch_import_dir> <dest_repro_dir>
"""
import shutil
import sys
from pathlib import Path


def main():
    s, d = Path(sys.argv[1]), Path(sys.argv[2])
    r, t = s / 'repro', s / 'tools'
    plan = []
    for n in ('current_boundary.log', 'current_boundary.json', 'baseline_boundary.log', 'baseline_boundary.json',
              'current_receipt_selftest.log', 'current_receipt_selftest.json', 'actual_receipt.log',
              'actual_receipt.json', 'actual_receipt_ours.json'):
        plan.append((r / 'out' / n, d / 'out' / n))
    for m in ('core', 'axis', 'mutants', 'failclosed'):
        plan.append((r / 'codex_probes/evidence/s02' / f'{m}.json', d / 's02_probe' / f'{m}.json'))
        plan.append((r / 'codex_probes/evidence/s02' / f'{m}.log', d / 's02_probe' / f'{m}.log'))
        plan.append((r / 'codex_probes' / f'{m}.stdout', d / 's02_probe' / f'{m}.stdout'))
    plan.append((r / 'codex_probes/probe_path_changes.diff', d / 'probe_path_changes.diff'))
    plan.append((r / 's06_nooracle/s06_nooracle.json', d / 's06_nooracle.json'))
    plan.append((r / 'scope_ours.json', d / 'scope_ours.json'))
    plan.append((r / 'tree_cmp.json', d / 'tree_cmp.json'))
    for n in ('inspect_zip.py', 'check_contents.py', 'classify.py', 'tree_cmp.py', 'scope_ours.py', 'run_ours.py',
              'run_baseline_exec.py', 'make_probe_copy.py', 's06_nooracle.py', 'cmp_receipt.py', 'assemble.py',
              'results_ours.py', 'copy_repro.py'):
        plan.append((t / n, d / 'tools' / n))
    for a, b in plan:
        b.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(a, b)
        assert a.read_bytes() == b.read_bytes()
    print('copied', len(plan))


if __name__ == '__main__':
    main()

"""Negative control in a disposable synthetic source copy; no real CLI."""
import pathlib
import subprocess
import sys
import tempfile

here = pathlib.Path(__file__).resolve().parent
source = (here / 'pressure_inventory.sh').read_text()
needle = 'if stamp(before) != stamp(os.fstat(fd)):'
if source.count(needle) != 1:
    raise SystemExit('unexpected source shape')
with tempfile.TemporaryDirectory(prefix='a01-mutant-') as tmp:
    root = pathlib.Path(tmp)
    (root / 'pressure_inventory.sh').write_text(source.replace(needle, 'if False:'))
    (root / 'test_ancestor_diagnostics.py').write_bytes((here / 'test_ancestor_diagnostics.py').read_bytes())
    child = subprocess.run([sys.executable, '-I', '-B', str(root / 'test_ancestor_diagnostics.py')],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30)
    print(child.stdout, end='')
    print('expected_mutant_rc=1 observed_mutant_rc=%d' % child.returncode)
    if child.returncode != 1 or '0 != 2' not in child.stdout or 'FAILED (failures=1)' not in child.stdout:
        raise SystemExit('negative control did not detect removed ancestor guard')

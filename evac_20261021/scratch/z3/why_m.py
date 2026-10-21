"""Print the 'why' strings of the chain-test mutant checks M08-M10 (diagnostic only)."""
import shutil
import sys
import tempfile

sys.path.insert(0, sys.argv[1])
import test_rint_r_chain as T  # noqa: E402
import rint_r_chain as RR  # noqa: E402

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='whym_')
try:
    T.fixtures()
    for fn in (T.t_M08, T.t_M09, T.t_M10, T.t_X09):
        ok, why = fn()
        print(fn.__name__, ok, str(why)[:400])
finally:
    shutil.rmtree(T.TD, ignore_errors=True)

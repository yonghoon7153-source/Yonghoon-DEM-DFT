"""pa14 probe lib — test module as library (honest producer outputs via real chain + fake runner)."""
import os, sys, tempfile, copy, json, shutil, io, contextlib
from pathlib import Path
SCR = Path('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14')
SRC = Path(os.environ.get('PA14_SRC', '/home/user/pa14/scripts'))
sys.path.insert(0, str(SRC))
import rint_r_chain as RR          # noqa: E402
import test_rint_r_chain as T      # noqa: E402
T.RR = RR
T.TD = tempfile.mkdtemp(prefix='pa14_', dir=str(SCR / 'tmp'))
T.fixtures()


def row(folder, s):
    try:
        fl = RR.result_fields(folder, s)
        prob = RR.stop_record_problem(s, folder)
        return [fl['cause'], fl['resume_ok'], None if prob is None else prob[:150]]
    except Exception as e:      # noqa: BLE001
        return f'EXC {type(e).__name__}: {str(e)[:150]}'

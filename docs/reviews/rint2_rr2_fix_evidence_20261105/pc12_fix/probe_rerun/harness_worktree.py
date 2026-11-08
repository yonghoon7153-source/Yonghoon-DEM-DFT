"""공통 하네스 — 리포 모듈을 읽기 전용으로 불러온다 (sys.path) · 임시 폴더 = 이 scratch 아래."""
import sys, os, json, tempfile, time, shutil, io, contextlib, hashlib
from pathlib import Path
sys.path.insert(0, '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-ad1a0fe809e58dc47/scripts')
import rint_r_chain as RR
import test_rint_r_chain as T
SCR = Path('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pc12_fix_work/probes/work')

def setup(full=False):
    T.RR = RR
    T.TD = tempfile.mkdtemp(prefix='pa12_', dir=str(SCR))
    if full:
        T.fixtures()
    return T.TD

def mkfolder(tag):
    f = Path(T.TD) / 'syn' / tag / 'attempt_1'
    f.mkdir(parents=True)
    return f

def rf(f, s):
    try:
        g = RR.result_fields(f, s)
        return [g['status'], g['side'], g['cause'], g['resume_ok']]
    except RR.Stop as e:
        return f'Stop {e.code}: {e.cause[:160]}'
    except Exception as e:
        return f'EXC {type(e).__name__}: {e}'

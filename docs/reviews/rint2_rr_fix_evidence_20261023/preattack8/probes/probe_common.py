"""Shared harness for preattack-8 probes — imports the target tree's test module and builds its fixtures (fake runner, git fixture repo,
plan, registration copy) exactly as test_rint_r_chain.main() does.  Usage: python3 -I <probe>.py <tree>  (tree = checkout of 7b51e591e)."""
import os
import sys
import tempfile
from pathlib import Path


def setup(tree):
    tree = Path(tree).resolve()
    sys.path.insert(0, str(tree / 'scripts'))
    os.chdir(str(tree))
    import rint_r_chain as RR                                  # noqa: E402
    import test_rint_r_chain as T                              # noqa: E402
    T.RR = RR
    T.TD = tempfile.mkdtemp(prefix='pa8_')
    T.fixtures()
    return RR, T

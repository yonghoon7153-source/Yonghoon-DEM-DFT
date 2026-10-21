"""Driver — run a worktree test with the scratch implementation modules pre-loaded (impl/*.py · each module name = file stem).
usage: python3 drv.py [--impl DIR] [--mods a,b] -- [test.py] <test args...>"""
import importlib.util
import os
import runpy
import sys

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee'
IMPL = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/impl'
MODS = ['step3_sigma', 'carbon_junction', 'ca_ext_cjunc', 'ca_s0_census']
args = sys.argv[1:]
while args and args[0] in ('--impl', '--mods'):
    if args[0] == '--impl':
        IMPL = args[1]
    else:
        MODS = [m for m in args[1].split(',') if m]
    args = args[2:]
if args and args[0] == '--':
    args = args[1:]
test = WT + '/scripts/test_carbon_junction.py'
if args and args[0].endswith('.py'):
    test = args[0] if os.path.isabs(args[0]) else os.path.join(WT, args[0])
    args = args[1:]
sys.path.insert(0, WT + '/scripts')
for name in MODS:
    path = os.path.join(IMPL, name + '.py')
    if not os.path.exists(path):
        continue
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
sys.argv = [test] + args
runpy.run_path(test, run_name='__main__')

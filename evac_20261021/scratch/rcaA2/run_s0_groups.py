"""Run selected groups of test_ca_s0_census.py (non-e2e) — optional impl preload (--impl DIR) · groups as args (t_plan_commit …)."""
import importlib.util
import os
import sys

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee'
args = sys.argv[1:]
impl = None
if args and args[0] == '--impl':
    impl = args[1]
    args = args[2:]
sys.path.insert(0, WT + '/scripts')
if impl:
    for name in ('step3_sigma', 'carbon_junction', 'ca_ext_cjunc', 'ca_s0_census'):
        p = os.path.join(impl, name + '.py')
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location(name, p)
            m = importlib.util.module_from_spec(spec)
            sys.modules[name] = m
            spec.loader.exec_module(m)
spec = importlib.util.spec_from_file_location('tcs0', WT + '/scripts/test_ca_s0_census.py')
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
for g in args:
    print('──', g)
    T.run(g, getattr(T, g))
print(f'\n{T._ok} PASS · {len(T._fail)} FAIL')
for f in T._fail:
    print('FAIL:', f)
sys.exit(1 if T._fail else 0)

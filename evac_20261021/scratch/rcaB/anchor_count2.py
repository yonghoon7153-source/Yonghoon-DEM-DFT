"""Count every T18 mutation anchor (from the test file's MUTANTS) in given module files (each must be exactly 1).

usage: python3 -I anchor_count2.py <test file> <step3_conv_cert.py> <run_contract.py>
"""
import importlib.util
import sys

tf, cc, rc = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('tsc_probe', tf)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
src = {'step3_conv_cert': open(cc, encoding='utf-8').read(), 'run_contract': open(rc, encoding='utf-8').read()}
bad = 0
for nm, mod, pairs, run, want in m.MUTANTS:
    for old, _new in pairs:
        n = src[mod].count(old)
        bad += n != 1
        print(f'{n}  {mod:16s} {nm}')
print('anchors not exactly once:', bad, '/', sum(len(x[2]) for x in m.MUTANTS))

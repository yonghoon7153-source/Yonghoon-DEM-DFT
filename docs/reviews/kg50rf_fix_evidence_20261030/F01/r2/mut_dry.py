# dry check of mutate_r2.py: every mutant builds (exactly-once match · exact revert) — no tests run
import sys
TOOL = sys.argv[1]
src = open('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01r2/mutate_r2.py', encoding='utf-8').read()
cut = src.index("os.makedirs(os.path.join(OUT, 'logs')")
sys.argv = ['x', TOOL, '/dev/null', '/dev/null']
ns = {'__name__': 'x'}
exec(compile(src[:cut], 'mutate_r2', 'exec'), ns)
for m in ns['MUT']:
    t = ns['make'](m)
    print(m[0], 'ok', len(t) - len(ns['SRC']))

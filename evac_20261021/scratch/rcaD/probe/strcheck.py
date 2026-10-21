import sys, os, re, ast
W = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82'
B = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaD/base_a76'
src = open(os.path.join(B, 'scripts', 'mpm_webapp_payload.py'), encoding='utf-8').read()
tree = ast.parse(src)
found = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and getattr(node.func, 'id', None) == '_s3mark' and len(node.args) >= 3:
        a0, a1, a2 = node.args[:3]
        if isinstance(a1, ast.Constant) and a1.value == 'disabled' and isinstance(a2, ast.Constant):
            found.append((a0.value, a2.value))
sys.path.insert(0, os.path.join(W, 'scripts'))
import mpm_webapp_payload as P
want = {'collector_geom': P._DIS_COLLECTOR, 'ionic': P._DIS_ION, 'thermal': P._DIS_THERMAL, 'pore': P._DIS_PORE, 'pnm': P._DIS_PNM}
for comp, s in found:
    print(comp, s == want.get(comp), repr(s)[:60])

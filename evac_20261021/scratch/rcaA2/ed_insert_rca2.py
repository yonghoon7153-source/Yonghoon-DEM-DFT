p = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts/test_carbon_junction.py'
blk = open('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/rca2_block.py',
           encoding='utf-8').read()
s = open(p, encoding='utf-8').read()
mark = '# ═════════════════════════ FP — 지문 재현 (RINT-23'
assert s.count(mark) == 1
assert "@case('GAP')" not in s
s = s.replace(mark, blk.rstrip('\n') + '\n\n\n' + mark)
open(p, 'w', encoding='utf-8').write(s)
print('ok')

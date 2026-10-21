"""Count occurrences of the review's 24 mutation substrings in the new generator (scratch)."""
import importlib.util
import os
import sys

spec = importlib.util.spec_from_file_location('pm', '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2/probe_mutations.py')
src_pm = open(spec.origin, encoding='utf-8').read()
start = src_pm.index('MUT = [')
end = src_pm.index(']\nres = []')
ns = {}
exec(src_pm[start:end + 1], ns)
NEW = open(sys.argv[1], encoding='utf-8').read()
for name, old, new in ns['MUT']:
    print(f'{name:30s} occurrences in new generator: {NEW.count(old)}')

#!/usr/bin/env python3
"""recheck 10-21: how many of the 24 original mutation anchors still occur exactly once in gen/mmd_FIX.py"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen', sys.argv[1] if len(sys.argv) > 1 else 'mmd_FIX.py'), encoding='utf-8').read()
spec = importlib.util.spec_from_file_location('pm', os.path.join(HERE, sys.argv[2] if len(sys.argv) > 2 else 'probe_mutations.py'))
txt = open(os.path.join(HERE, sys.argv[2] if len(sys.argv) > 2 else 'probe_mutations.py'), encoding='utf-8').read()
start = txt.index('MUT = [')
end = txt.index('\n]\n', start) + 3
ns = {}
exec(txt[start:end], ns)
for name, old, new in ns['MUT']:
    print(f'{name:30s} {src.count(old)}')

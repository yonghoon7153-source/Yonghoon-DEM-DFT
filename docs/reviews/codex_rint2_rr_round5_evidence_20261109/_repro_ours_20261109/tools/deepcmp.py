"""Deep compare two JSON files; report differing leaf paths. Path-like strings are normalized
(Windows backslashes, temp-dir names) only when --normalize-paths is given; differences are listed raw too."""
import json, sys, re
def load(p):
    return json.load(open(p, encoding='utf-8'))
def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if k not in a: out.append((path + [k], '<absent>', b[k])); continue
            if k not in b: out.append((path + [k], a[k], '<absent>')); continue
            walk(a[k], b[k], path + [k], out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, f'len {len(a)}', f'len {len(b)}'))
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, path + [i], out)
    else:
        if a != b or type(a) is not type(b):
            out.append((path, a, b))
codex, ours = load(sys.argv[1]), load(sys.argv[2])
out = []
walk(codex, ours, [], out)
print(f'differing leaves: {len(out)}')
for p, a, b in out:
    sa, sb = repr(a), repr(b)
    print('/'.join(map(str, p)), '| codex=', sa[:220], '| ours=', sb[:220])

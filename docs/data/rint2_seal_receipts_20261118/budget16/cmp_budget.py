import json, sys
d = {n: json.load(open(f'{sys.argv[1]}/out{n}.json')) for n in (12, 13, 16)}
def leaves(o, p=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f'{p}.{k}' if p else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f'{p}[{i}]')
    else:
        yield p, o
L = {n: dict(leaves(d[n])) for n in d}
changed = [k for k in L[12] if L[12][k] != L[16].get(k) or L[12][k] != L[13].get(k)]
print('leaves', len(L[12]), 'changed', len(changed))
for k in changed:
    print(k, '|', L[12][k], '|', L[13].get(k), '|', L[16].get(k))

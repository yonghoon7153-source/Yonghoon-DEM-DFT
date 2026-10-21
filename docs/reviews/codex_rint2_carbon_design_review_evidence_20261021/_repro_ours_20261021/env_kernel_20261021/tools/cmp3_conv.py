import json, sys, math
paths = {'codex': sys.argv[1], 'ours': sys.argv[2], 'envcodex': sys.argv[3]}
def flat(d, p=''):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items(): out.update(flat(v, f'{p}.{k}' if p else k))
    elif isinstance(d, list):
        for i, v in enumerate(d): out.update(flat(v, f'{p}[{i}]'))
    else: out[p] = d
    return out
F = {k: flat(json.load(open(v, encoding='utf-8'))) for k, v in paths.items()}
keys = sorted(set(F['codex']) | set(F['ours']) | set(F['envcodex']))
def same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        if a == b: return 'eq'
        if math.isfinite(a) and math.isfinite(b) and abs(a-b) <= 1e-12*max(abs(a),abs(b)): return 'ulp'
        return 'diff'
    return 'eq' if a == b else 'diff'
cnt = {'ours_vs_codex': {}, 'env_vs_codex': {}, 'env_vs_ours': {}}
rows = []
for k in keys:
    c, o, e = F['codex'].get(k), F['ours'].get(k), F['envcodex'].get(k)
    a, b, d = same(o, c), same(e, c), same(e, o)
    for name, r in (('ours_vs_codex', a), ('env_vs_codex', b), ('env_vs_ours', d)):
        cnt[name][r] = cnt[name].get(r, 0) + 1
    if 'diff' in (a, b) or any(s in k for s in ('pass', 'ok', 'imbalance', 'rel_err', 'relative', 'iterations', 'info')):
        rows.append((k, c, o, e, a, b))
print(json.dumps(cnt))
for r in rows:
    if r[4] == 'diff' or r[5] == 'diff' or any(s in r[0] for s in ('pass_', '.ok', 'ok"', 'imbalance')):
        print(f'{r[0]} | codex={r[1]} | ours={r[2]} | envcodex={r[3]} | o/c={r[4]} e/c={r[5]}')

"""Run check_doc_refs.scan_text on one document only (pre-check; the full checker is the gate)."""
import importlib.util
import os
import sys

sys.dont_write_bytecode = True
root = sys.argv[1]
rel = sys.argv[2]
spec = importlib.util.spec_from_file_location('cdr', os.path.join(root, 'scripts', 'check_doc_refs.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
shas = m.known_shas(root)
shorts = {s[:8] for s in shas} | {s[:7] for s in shas}
resolve = m.Resolver(shas)
exc, stale = m.load_sha_exceptions(root, resolve)
allow, allow_bad, allow_soft = m.load_allowlist(root)
txt = open(os.path.join(root, rel), encoding='utf-8').read()
got = m.scan_text(txt, root, shas, shorts, resolve, exc, rel)
print('commits', len(shas))
for k in ('missing', 'bad_sha', 'cross', 'unsure'):
    v = got[k]
    if k == 'missing':
        v = [x for x in v if x not in allow]
    print(k, len(v), sorted(set(v))[:40])

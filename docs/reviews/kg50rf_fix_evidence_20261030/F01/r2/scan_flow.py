# flow / state-changing commands in the 12 real kg50 main decks, relative to the two checkpoints (settling restart · after_settling write_restart)
import glob, os, sys
WT = sys.argv[1]
TOOL = os.path.join(WT, 'scripts/resume_ckpt.sh')
s = open(TOOL, encoding='utf-8').read()
a = s.index("<<'PY'\n") + len("<<'PY'\n")
src = s[a:s.index("\nif len(sys.argv) == 3 and sys.argv[1] == '--strip-comments':", a)]
ns = {}
exec(compile(src, '<deck>', 'exec'), ns)
os.chdir(WT)
FL = {'label', 'jump', 'clear', 'next', 'include', 'python', 'partition', 'print'}
for m in sorted(glob.glob('docs/data/kg50_decks_2026102[67]_*/kg50_*/input_kg50_*.liggghts')):
    if m.endswith('_insert.liggghts'):
        continue
    L = ns['deck'](m)
    iw = [i for i, l in enumerate(L) if l.startswith('write_restart') and 'after_settling' in l]
    ir = [i for i, l in enumerate(L) if l.split()[0] == 'restart']
    hits = []
    for i, l in enumerate(L):
        w = ns['words'](l) or ['']
        cs = [w] + ns['nested'](w)
        names = sorted(set(x[0] for x in cs if x and x[0] in FL - {'print'}))
        if names:
            hits.append((i, names, l[:70]))
        if w[0] == 'run' and 'every' in w:
            hits.append((i, ['run-every'], l[:70]))
    print(os.path.basename(m), 'n', len(L), 'restart@', ir, 'write_restart(after_settling)@', iw)
    for h in hits:
        print('    ', h)

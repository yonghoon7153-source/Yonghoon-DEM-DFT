# where does '$' appear in the real kg50 decks (by command and word position)?  uses the tool's own deck()/words()
import glob, os, sys, collections
WT = sys.argv[1]
TOOL = os.path.join(WT, 'scripts/resume_ckpt.sh')
s = open(TOOL, encoding='utf-8').read()
a = s.index("<<'PY'\n") + len("<<'PY'\n")
src = s[a:s.index("\nif len(sys.argv) == 3 and sys.argv[1] == '--strip-comments':", a)]
ns = {}
exec(compile(src, '<deck>', 'exec'), ns)
os.chdir(WT)
fs = sorted(set(glob.glob('docs/data/kg50_*/**/*.liggghts', recursive=True)))
pos = collections.Counter()
ex = {}
for f in fs:
    for l in ns['deck'](f):
        w = ns['words'](l)
        if not w:
            continue
        for k, t in enumerate(w):
            if '$' in t:
                key = (w[0], k)
                pos[key] += 1
                ex.setdefault(key, (f, l))
for key, n in sorted(pos.items()):
    print(key, n, '|', ex[key][1][:110])

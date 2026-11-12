import sys, difflib
a = open(sys.argv[1], encoding='utf-8').read().split('\n')
b = open(sys.argv[2], encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
out = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    out.append(f"=== {tag} old {i1+1}-{i2} -> new {j1+1}-{j2}")
    if tag == 'insert':
        for j in range(j1, j2):
            out.append(f"[NEW {j+1}] {b[j]}")
        continue
    if tag == 'delete':
        for i in range(i1, i2):
            out.append(f"[DEL {i+1}] {a[i]}")
        continue
    # replace: pair lines greedily by similarity
    olds = list(range(i1, i2)); news = list(range(j1, j2))
    if len(olds) == len(news):
        pairs = list(zip(olds, news))
        extra_old = []; extra_new = []
    else:
        pairs = []; used = set()
        for j in news:
            best = None; bs = 0
            for i in olds:
                if i in used: continue
                r = difflib.SequenceMatcher(None, a[i], b[j], autojunk=False).quick_ratio()
                if r > bs: bs, best = r, i
            if best is not None and bs > 0.5:
                pairs.append((best, j)); used.add(best)
        paired_new = {j for _, j in pairs}
        extra_old = [i for i in olds if i not in used]
        extra_new = [j for j in news if j not in paired_new]
    for i, j in pairs:
        ta = a[i].split(' '); tb = b[j].split(' ')
        s2 = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
        segs = []
        for t2, x1, x2, y1, y2 in s2.get_opcodes():
            if t2 == 'equal':
                continue
            ctx_l = ' '.join(ta[max(0, x1-6):x1])
            ctx_r = ' '.join(ta[x2:x2+6])
            segs.append(f"   …{ctx_l} [-{' '.join(ta[x1:x2])}-] {{+{' '.join(tb[y1:y2])}+}} {ctx_r}…")
        out.append(f"[MOD old {i+1} -> new {j+1}] ({len(segs)} segs)")
        out.extend(segs)
    for i in extra_old:
        out.append(f"[DEL {i+1}] {a[i]}")
    for j in extra_new:
        out.append(f"[NEW {j+1}] {b[j]}")
print('\n'.join(out))

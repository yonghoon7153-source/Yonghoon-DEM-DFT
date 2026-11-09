import itertools
from collections import Counter
A,I,B='above','in','below'   # vs window [10,13] %
def crosses(seq):
    if I in seq: return True
    return any({seq[i],seq[i+1]}=={A,B} for i in range(len(seq)-1))
def full_seq(base, ext):
    # extension only if last base point (0.60 GPa) is below window
    return base + (ext if base[-1]==B else ())
res=Counter(); noncross_kinds=Counter(); multi_cross=0; n=0
for base in itertools.product([A,I,B],repeat=8):
    exts = list(itertools.product([A,I,B],repeat=2)) if base[-1]==B else [()]
    for ext in exts:
        s=full_seq(base,ext); n+=1
        if crosses(s):
            # count number of distinct crossing locations (in-points or adjacent splits)
            locs=sum(1 for x in s if x==I)+sum(1 for i in range(len(s)-1) if {s[i],s[i+1]}=={A,B})
            if locs>1: multi_cross+=1
        else:
            noncross_kinds['all-above' if all(x==A for x in s) else 'all-below' if all(x==B for x in s) else 'MIXED']+=1
print('sequences',n,'non-crossing kinds',dict(noncross_kinds),'crossing with >1 location',multi_cross)
# monotone-increasing (porosity rises with sigma_y) sequences only: below* in* above*
mono=[s for s in itertools.product([B,I,A],repeat=8) if list(s)==sorted(s,key=[B,I,A].index)]
print('monotone sequences',len(mono),'with >1 in-point',sum(1 for s in mono if s.count(I)>1))
# (4-i)/(4-ii)/(4-iii)
def cls(real,soft): return '4-i' if real else ('4-ii' if soft else '4-iii')
print({(r,s):cls(r,s) for r in (True,False) for s in (True,False)})

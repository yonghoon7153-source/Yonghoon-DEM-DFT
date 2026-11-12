import re, sys
for p in sys.argv[1:]:
    L=open(p,encoding='utf-8').read().split('\n')
    i=0;bad=[]
    cnt=lambda s: len(re.findall(r'(?<!\\)\|', s))
    while i<len(L):
        if L[i].startswith('|'):
            j=i
            while j<len(L) and L[j].startswith('|'): j+=1
            h=cnt(L[i])
            bad+=[(k+1,cnt(L[k]),h) for k in range(i,j) if cnt(L[k])!=h]
            i=j
        else: i+=1
    print(p, 'bad rows', bad[:5])

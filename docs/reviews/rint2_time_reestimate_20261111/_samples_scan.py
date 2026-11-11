#!/usr/bin/env python3
# 읽기 전용 · 표준 라이브러리 · samples.tsv 구간 요약 (값 σ 없음)
import sys, statistics as st
def load(p):
    rows=[]
    for ln in open(p):
        if ln.startswith('#') or not ln.strip(): continue
        f=ln.rstrip('\n').split('\t')
        rows.append(dict(epoch=int(f[0]),el=int(f[1]),ll=int(f[2]),rss=int(f[3]),rssp=int(f[4]),
                         gused=int(f[5]),gours=f[6],gutil=int(f[7]) if f[7] not in ('NA','') else None))
    return rows
def seg(rows,a,b):
    return [r for r in rows if a<=r['el']<b]
def summ(name,rs):
    if not rs:
        print(name,'no samples'); return
    gu=[r['gutil'] for r in rs if r['gutil'] is not None]
    print('%-34s n=%4d el=%6d..%6d gutil mean=%.1f min=%d max=%d  gused min=%d max=%d  rss min=%.1f max=%.1f GB(kB/1e6)'%(
        name,len(rs),rs[0]['el'],rs[-1]['el'],st.mean(gu),min(gu),max(gu),
        min(r['gused'] for r in rs),max(r['gused'] for r in rs),
        min(r['rss'] for r in rs)/1e6,max(r['rss'] for r in rs)/1e6))
for p in sys.argv[1:]:
    rows=load(p)
    print('==',p,'rows',len(rows))
    # 전이점: log_lines 변화 · gpu_used 큰 변화 · gutil 100 구간의 처음/끝
    prev=None
    for r in rows:
        if prev is not None:
            if r['ll']!=prev['ll']:
                print('  log_lines %d->%d at el=%d (prev el=%d)'%(prev['ll'],r['ll'],r['el'],prev['el']))
            if abs(r['gused']-prev['gused'])>=500:
                print('  gpu_used %d->%d at el=%d (prev el=%d)'%(prev['gused'],r['gused'],r['el'],prev['el']))
        prev=r
    hi=[r for r in rows if r['gutil'] is not None and r['gutil']>=97]
    if hi:
        print('  gutil>=97: first el=%d last el=%d count=%d'%(hi[0]['el'],hi[-1]['el'],len(hi)))
        # 연속 구간
        runs=[];cur=[hi[0]]
        idx={id(r):i for i,r in enumerate(rows)}
        for a,b in zip(hi,hi[1:]):
            if idx[id(b)]==idx[id(a)]+1: cur.append(b)
            else: runs.append(cur);cur=[b]
        runs.append(cur)
        for ru in runs:
            if len(ru)>=3: print('    run el=%d..%d n=%d'%(ru[0]['el'],ru[-1]['el'],len(ru)))
    lo_in=[r for r in rows if hi and hi[0]['el']<r['el']<hi[-1]['el'] and r['gutil'] is not None and r['gutil']<97]
    print('  samples with gutil<97 inside the solve span:',len(lo_in),[ (r['el'],r['gutil']) for r in lo_in][:40])
    if hi:
        s0=hi[0]['el']; s1=hi[-1]['el']
        summ('  prep (0..solve start)',seg(rows,0,s0))
        summ('  solve span',seg(rows,s0,s1+1))
        summ('  after solve span',seg(rows,s1+1,10**9))

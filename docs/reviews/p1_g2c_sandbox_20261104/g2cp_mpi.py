"""MPI evidence checks for the fixed NP2/4 G2c-prime development sandbox."""
import math
import re

ARMS = ('A','A2','B','B2','C','BW','BR','CW','CR')
GRIDS = {1:(1,1,1),2:(2,1,1),4:(2,2,1)}
BOUNDARY_REL = 1e-12

def check_log(text, np):
    errors=[]
    loops=re.findall(r'^Loop time of .*? on ([0-9]+) procs\b.*$',text,re.M)
    grids=re.findall(r'^\s*([0-9]+) by ([0-9]+) by ([0-9]+) MPI processor grid\s*$',text,re.M)
    if not loops or any(int(k)!=np for k in loops):errors.append('loop_procs')
    if len(grids)!=1 or tuple(map(int,grids[0]))!=GRIDS[np]:errors.append('processor_grid')
    if re.search(r'^ERROR\b',text,re.M):errors.append('engine_error')
    return errors

def check_identity(text, logs):
    rows=[line.split(None,1) for line in text.splitlines() if line.strip()]
    values={}
    for row in rows:values.setdefault(row[0],[]).append(row[1] if len(row)==2 else '')
    why=[];raw=values.get('np')
    if raw is None:np=1
    elif len(raw)!=1 or raw[0] not in ('2','4'):np=1;why.append('invalid_or_duplicate_np')
    else:np=int(raw[0])
    if raw is not None and values.get('procs_grid')!=[' '.join(map(str,GRIDS[np]))]:why.append('grid_identity')
    for arm in ARMS:
        if arm not in logs:why.append(arm+':missing_log')
        else:why.extend(arm+':'+e for e in check_log(logs[arm],np))
    return {'ok':not why,'np':np,'mode':'MPI' if raw is not None else 'SERIAL','grid':GRIDS[np],'why':why}

def owner(x, box, np):
    if np not in (2,4):raise ValueError('unsupported NP')
    result=[];ambiguous=False
    for d,p in enumerate(GRIDS[np][:2]):
        lo,hi=box[d];v=x[d];length=hi-lo
        if not all(math.isfinite(t) for t in (lo,hi,v)) or length<=0 or v<lo or v>hi:raise ValueError('invalid coordinate/box')
        if any(abs(v-(lo+length*k/p))<=BOUNDARY_REL*length for k in range(1,p)):ambiguous=True
        result.append(min(p-1,int((v-lo)/length*p)))
    return None if ambiguous else tuple(result)

def classify(pairs, atoms, np):
    groups={'same':[],'rank_boundary':[],'periodic':[],'ambiguous':[]}
    for key,row in pairs['by_key'].items():
        if row['v'][8]!=0:groups['periodic'].append(key);continue
        a,b=key
        oa=owner(atoms['by_id'][a][1][:3],atoms['box'],np)
        ob=owner(atoms['by_id'][b][1][:3],atoms['box'],np)
        groups['ambiguous' if oa is None or ob is None else 'same' if oa==ob else 'rank_boundary'].append(key)
    return groups

def pred_ma3p(c, an, atoms, np, cmp_groups, group_names):
    if not all(x.get('ok') for x in (c,an,atoms)):return {'status':'계산 못 함','why':['invalid dumps']}
    if set(c['by_key'])!=set(an['by_key']):return {'status':'틀림','why':['C/A pair set mismatch']}
    groups=classify(an,atoms,np);C,N=c['by_key'],an['by_key']
    force=['force','force_normal','force_tangential']
    other=[g for g in group_names if g not in force+['torque']]
    differs=lambda keys,names:sum(any(cmp_groups(C,N,[k],names).values()) for k in keys)
    counts={k:len(v) for k,v in groups.items()}
    observations={'same_all_differ':differs(groups['same'],group_names),
                  'all_nonforce_differ':differs(list(C),other),
                  'rank_force_differ':differs(groups['rank_boundary'],force),
                  'periodic_force_differ':differs(groups['periodic'],force)}
    why=[]
    if observations['same_all_differ']:why.append('(a) same-owner rows differ')
    if observations['all_nonforce_differ']:why.append('(b) non-force rows differ')
    if observations['rank_force_differ']!=counts['rank_boundary']:why.append('(c) rank-boundary force not different for every pair')
    if observations['periodic_force_differ']!=counts['periodic']:why.append('(d) periodic force not different for every pair')
    return {'status':'틀림' if why else '해당 없음' if not counts['rank_boundary'] else '맞음',
            'why':why,'counts':counts,'n_rb':counts['rank_boundary'],'observations':observations,
            'boundary_rel':BOUNDARY_REL,'scope':'same_np_development_only'}

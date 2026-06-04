#!/usr/bin/env python3
"""σ_thermal Stage T1 — push LOOCV higher (untried levers).

Current: 14 Ridge features, LOOCV 0.90 (n=82) / 0.849 (n=90).
Try every remaining lever to push higher:

  1. α fine sweep (0.01 ~ 0.2)
  2. Add NEW engineered features (cross-products, ratios of top features)
  3. Try ALL ~75 structural features in greedy (not just the 14)
  4. Polynomial / interaction terms on porosity (top feature)
  5. log(κ) vs sqrt(κ) vs κ target transform
"""
import sys, json, glob
from pathlib import Path
from collections import Counter
import numpy as np
from numpy.linalg import solve

sys.path.insert(0, 'scripts')
import generate_comparison_plots as gcp

KAPPA_MAX = 50.0; KAPPA_MIN = 0.05
EXCL = gcp._EXCLUDED_NAMES_EL
TARGET_LEAK = ('thermal_sigma', 'sigma_full_mScm', 'electronic_sigma_full_mScm',
               'stage_e_le_baseline_kappa')


def load():
    cases = []; seen = set()
    for base in ('webapp/archive', 'webapp/results'):
        for f in sorted(glob.glob(f'{base}/**/full_metrics.json', recursive=True)):
            nm = Path(f).parent.name
            if not nm.startswith('input_') or nm in seen: continue
            seen.add(nm)
            try: d = json.load(open(f))
            except: continue
            kappa = d.get('thermal_sigma_full_mScm_stage_e_physics') or 0
            if not (KAPPA_MIN <= kappa <= KAPPA_MAX): continue
            if nm in EXCL: continue
            d['_name'] = nm; d['_kappa'] = float(kappa)
            cases.append(d)
    return cases


def _gn(d, k):
    if '.' not in k: return d.get(k)
    v = d
    for p in k.split('.'):
        if isinstance(v, dict): v = v.get(p)
        else: return None
    return v


def farr(cases, k):
    out = [(_gn(c, k) if isinstance(_gn(c, k), (int, float)) and np.isfinite(_gn(c, k)) else np.nan)
           for c in cases]
    a = np.array(out, float)
    if np.any(~np.isfinite(a)): a = np.where(np.isfinite(a), a, np.nanmedian(a))
    return a


def loocv(X, y, alpha=0.05):
    k = X.shape[1]
    X_ = np.column_stack([np.ones(len(y)), X])
    I = np.eye(k+1); I[0,0]=0
    try: coef = solve(X_.T@X_+alpha*I, X_.T@y)
    except: return None
    ss = float(np.sum((y-y.mean())**2))
    sse = 0.0
    for j in range(len(y)):
        m=np.ones(len(y),bool); m[j]=False; Xm=X_[m]
        try:
            cm=solve(Xm.T@Xm+alpha*I, Xm.T@y[m]); sse+=(y[j]-X_[j]@cm)**2
        except: pass
    return 1-sse/ss if ss>0 else 0


def build14(cases):
    cols=[]
    for fk, dl in gcp._THERMAL_T1_FEATURES:
        v=farr(cases,fk)
        if dl:
            v=np.where(v>0,v,np.nanmin(v[v>0]) if np.any(v>0) else 1e-6); cols.append(np.log(v))
        else: cols.append(v)
    return np.column_stack(cols)


def main():
    cases=load(); n=len(cases)
    print(f"\nCorpus: {n}")
    y=np.log(np.array([c['_kappa'] for c in cases]))
    X14=build14(cases)
    base=loocv(X14,y,0.05)
    print(f"Baseline 14-feat α=0.05: LOOCV={base:.4f}\n")

    # ─── 1. α fine sweep ───
    print("="*80)
    print("  1. α fine sweep")
    print("="*80)
    best_a, best_al = base, 0.05
    for a in [0.005,0.01,0.02,0.03,0.05,0.07,0.1,0.15,0.2,0.3]:
        l=loocv(X14,y,a)
        flag=' ⭐' if l>=0.9 else (' ←best' if l>best_a else '')
        if l>best_a: best_a=l; best_al=a
        print(f"  α={a:>5.3f}: LOOCV={l:.4f}{flag}")
    print(f"  → best α={best_al} LOOCV={best_a:.4f}\n")

    # ─── 2. Engineered cross/ratio features on top-5 ───
    print("="*80)
    print("  2. Cross-products & ratios of top features (added to 14)")
    print("="*80)
    top=['porosity','se_se_cn','R_brug_over_full_physics','tortuosity_median','gb_density_mean']
    tv={t:farr(cases,t) for t in top}
    add_best=base; add_name=None
    for i,a_ in enumerate(top):
        for b_ in top[i+1:]:
            for op,sym in [(lambda x,z:x*z,'×'),(lambda x,z:x/np.where(z==0,1e-9,z),'/')]:
                newf=op(tv[a_],tv[b_])
                if not np.all(np.isfinite(newf)): continue
                Xn=np.column_stack([X14,newf])
                l=loocv(Xn,y,best_al)
                if l>add_best+0.003:
                    print(f"  +({a_} {sym} {b_}): LOOCV={l:.4f}")
                    if l>add_best: add_best=l; add_name=f'{a_}{sym}{b_}'
    print(f"  → best add: {add_name} LOOCV={add_best:.4f}\n")

    # ─── 3. FULL greedy on all ~75 structural features ───
    print("="*80)
    print("  3. Full greedy on ALL structural features (15 steps)")
    print("="*80)
    common=Counter()
    for c in cases:
        for k,v in c.items():
            if k.startswith('_'): continue
            if isinstance(v,(int,float)): common[k]+=1
            elif isinstance(v,dict):
                for sk,sv in v.items():
                    if isinstance(sv,(int,float)): common[f'{k}.{sk}']+=1
    cand={}
    for k,ct in common.items():
        if ct/n<0.9 or any(p in k for p in TARGET_LEAK): continue
        v=farr(cases,k)
        if np.std(v)<1e-12: continue
        # both raw and log if positive
        cand[k]=v
        if np.min(v)>0: cand[f'log({k})']=np.log(v)
    print(f"  candidates: {len(cand)}")
    items=list(cand.items()); sel=[]; sarr=[]; best=-np.inf
    for step in range(15):
        bi,bl=None,-np.inf
        for i,(nm,arr) in enumerate(items):
            if i in [s[0] for s in sel]: continue
            l=loocv(np.column_stack(sarr+[arr]),y,best_al)
            if l and l>bl: bl=l; bi=i
        if bi is None: break
        sel.append((bi,items[bi][0])); sarr.append(items[bi][1])
        flag=' ⭐' if bl>=0.9 else ''
        print(f"  {step+1:2d}. +{items[bi][0][:45]:45s} LOOCV={bl:.4f}{flag}")
        if bl>best: best=bl
        if step>=5 and bl-best<0.002 and step>8: break
    print(f"  → full-greedy best: {best:.4f}\n")

    # ─── 4. porosity polynomial ───
    print("="*80)
    print("  4. porosity poly + interaction (top feature)")
    print("="*80)
    por=farr(cases,'porosity')
    for extra,lbl in [(por**2,'por²'),(np.log(np.maximum(por,1e-6)),'log(por)'),
                       (por*tv['se_se_cn'],'por×CN'),(np.sqrt(np.maximum(por,0)),'√por')]:
        Xn=np.column_stack([X14,extra])
        l=loocv(Xn,y,best_al)
        flag=' ★' if l>base+0.005 else ''
        print(f"  +{lbl:12s}: LOOCV={l:.4f}{flag}")
    print()

    # ─── 5. target transform ───
    print("="*80)
    print("  5. Target transform (log vs sqrt vs raw κ)")
    print("="*80)
    kap=np.array([c['_kappa'] for c in cases])
    for ty,tlbl in [(np.log(kap),'log κ (current)'),(np.sqrt(kap),'√κ'),(kap,'raw κ')]:
        l=loocv(X14,ty,best_al)
        print(f"  {tlbl:18s}: LOOCV={l:.4f}")
    print()

    print("="*80)
    print(f"  SUMMARY — baseline {base:.4f}")
    print("="*80)
    print(f"  1. α tune:        {best_a:.4f} (α={best_al})")
    print(f"  2. cross/ratio:   {add_best:.4f}")
    print(f"  3. full greedy:   {best:.4f}")
    print(f"  Best achievable:  {max(best_a,add_best,best):.4f}")


if __name__=='__main__':
    main()

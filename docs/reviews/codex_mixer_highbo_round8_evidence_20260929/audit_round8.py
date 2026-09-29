"""Document pinning, deterministic arithmetic, and logical counterexamples.

No DEM, MPI, scheduler, shell subprocess, real campaign data, or production edit.
Pinned generator calls return text in memory; no runnable deck is written.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import re
import sys
from datetime import datetime, timedelta

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
checks=[]
def check(name,ok):
    if not ok: raise AssertionError(name)
    checks.append(name)

raw=(ROOT/'bundle_original.md').read_bytes()
lf=raw.replace(b'\r\n',b'\n')
text=lf.decode('utf-8-sig')
(ROOT/'bundle_lf.md').write_bytes(text.encode('utf-8'))
start=text.index('# 믹서 고-Bo 확장 `LH` — D-1')
end=text.index('\n---\n\n# PART 3',start)
body_raw=text[start:end].encode('utf-8')
body_lf=body_raw.rstrip(b'\n')+b'\n'
old_claim='4a9ec2234784a9a083695b5a87dcfab1ce65f37e1edae404354121e665f512be'
new_claim='ab20ef775f3e6bdb660f82f36a15b18a3c7cb0d0f85a6881d840b1b2171dff44'
variants={'raw_between_markers':body_raw,'LF_one_final_newline':body_lf,
          'LF_no_final_newline':body_raw.rstrip(b'\n'),
          'CRLF_one_final_newline':body_lf.replace(b'\n',b'\r\n')}
variant_hashes={k:sha(v) for k,v in variants.items()}
matches=[k for k,v in variant_hashes.items() if v==new_claim]
check('v2.2 stated hash matches an explicitly recorded extraction',len(matches)>0)
selected=variants[matches[0]]
(ROOT/'prereg_v22_extracted.md').write_bytes(selected)
check('v2.1 hash is not the extracted v2.2 hash',sha(selected)!=old_claim)
line_map={}
for i,line in enumerate(text.splitlines(),1):
    if line.startswith('## ') or line.startswith('### ') or line.startswith('**Q'):
        line_map[str(i)]=line
pin=dict(bundle_sha256=sha(raw),bundle_bytes=len(raw),LF_sha256=sha(text.encode()),
         extracted_sha256=sha(selected),extracted_lines=len(selected.splitlines()),
         extracted_starts_at_bundle_line=text[:start].count('\n')+1,
         v21_stated_hash=old_claim,v22_stated_hash=new_claim,extraction_hashes=variant_hashes,
         selected_extraction=matches[0],line_map=line_map)

src=ROOT/'baseline/make_mixer_deck.py'
b=src.read_bytes()
blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
check('baseline exact Git blob',blob=='033fac54d73566ac1dad54f24cc28b9d0510ccbc')
spec=importlib.util.spec_from_file_location('baseline_mixer',src)
g=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
p=g.plan(100000,cgf=151.4)
names=tuple(g.TYPES)+('WALL',)
lc=g.ced_matrix('LC',p['d'])
lh=g.ced_matrix('LH',p['d'])
changes=[]
for i in range(3):
    for j in range(i,4):
        if lc[i][j]!=lh[i][j]:
            changes.append(dict(pair=names[i]+'--'+names[j],LC_CED_J_m3=lc[i][j],
                LH_CED_J_m3=lh[i][j],LH_over_LC_CED=lh[i][j]/lc[i][j],
                LH_over_LC_small_overlap_F0=(lh[i][j]/lc[i][j])**3))
check('LC AM-AM is not zero', all(lc[i][j]>0 for i,j in ((0,0),(0,1),(1,1))))
check('five B pairs differ',len(changes)==5)
check('both AM-wall entries differ',lc[0][3]!=lh[0][3] and lc[1][3]!=lh[1][3])

# Actual baseline deck() is called in memory only, with the same phase set,
# seed, Fr, N and CGF; compares 2-turn vs 8-turn sampling, not actual dynamics.
rpm=math.sqrt(.0827*9.81/p['R'])*60/(2*math.pi)
prefix={}
for turns in (2,8):
    s=g.deck(p,rpm=rpm,revolutions=turns,seed=32452843,arm='LC')
    de=int(re.search(r'^dump dmp all custom (\d+)',s,re.M).group(1))
    runs=[int(v) for v in re.findall(r'^run (\d+)',s,re.M)]
    dt=float(re.search(r'^timestep\s+([^\s]+)',s,re.M).group(1))
    period=float(re.search(r'^fix mvD.* period ([^\s]+)',s,re.M).group(1))
    fill=runs[-2]
    t0=(2*fill//de)*de
    spr=period/dt
    count0=sum(0<=int(math.floor(k*de/spr+1e-9))<1 for k in range(1,300))
    prefix[str(turns)]=dict(turns=turns,N=100000,CGF=151.4,Fr=.0827,rpm=rpm,
        emitted_dt_s=dt,period_s=period,dump_every_steps=de,run_steps=runs,
        planned_t0_step=t0,rotation_starts_at_step=sum(runs[:-1]),
        bin0_frames_excluding_t0=count0,approx_frames_per_turn=spr/de,
        deck_sha256=sha(s.encode()))
check('changing only turns changes observation lattice',prefix['2']['dump_every_steps']!=prefix['8']['dump_every_steps'])
check('turns can change normalization frame',prefix['2']['planned_t0_step']!=prefix['8']['planned_t0_step'])

# Synthetic response tables: no assertion they are actual mixer trajectories.
single=.14
refined=.091
threshold=dict(base_d=single,refined_d=refined,shift=single-refined,
    diagnostic_cutoff=.05,screen_pass=abs(single-refined)<=.05,
    base_MID_pass=single>=.1,refined_MID_pass=refined>=.1)
check('.05 screen can pass with changed MID classification',threshold['screen_pass'] and threshold['base_MID_pass'] and not threshold['refined_MID_pass'])
joint=dict(d_base=.18,d_E28=.131,d_dt_half=.131,d_E28_dt_half=.082)
joint['r']=joint['d_base']-joint['d_E28']
joint['t']=joint['d_base']-joint['d_dt_half']
joint['joint_shift']=joint['d_base']-joint['d_E28_dt_half']
check('two one-factor screens pass, joint .05 bound fails',abs(joint['r'])<.05 and abs(joint['t'])<.05 and abs(joint['joint_shift'])>.05)
one_seed=dict(development_r=.001,other_possible_seed_r=[.100,.100],
              ensemble_three_mean_r=(.001+.100+.100)/3)
check('one-seed pass is not ensemble certification',abs(one_seed['development_r'])<.05 and one_seed['ensemble_three_mean_r']>.05)
unqualified_fallback=dict(d14=.18,d28=.11,d56=.01,
    initial_change=.18-.11,next_unmeasured_change=.11-.01)
check('single fallback can remain beyond cutoff',unqualified_fallback['initial_change']>.05 and unqualified_fallback['next_unmeasured_change']>.05)
rank=dict(np20=dict(d14=.18,d28=.175),np10=dict(d14=.18,d28=.10))
check('rank transport not implied by within-rank control',abs(rank['np20']['d14']-rank['np20']['d28'])<.05 and abs(rank['np10']['d14']-rank['np10']['d28'])>.05)

# Budget arithmetic only. Given per-run wall hours are author's assumptions,
# not remeasured. E0, development, waiting, gating, I/O and retry costs excluded.
cost=[]
launch=datetime(2026,10,2)
for soft,ref in ((41,92),(45,100)):
    slot_hours=6*soft+6*ref
    hours=slot_hours/3
    cost.append(dict(soft_run_hours=soft,ref_run_hours=ref,long_runs=12,
        long_run_slot_hours=slot_hours,long_run_core_hours=20*slot_hours,
        ideal_capacity_lower_bound_hours=hours,days=hours/24,
        earliest_bound_from_oct02_midnight=(launch+timedelta(hours=hours)).isoformat()))
check('even lower cost exceeds the widest Oct02-to-Oct11 budget',cost[0]['ideal_capacity_lower_bound_hours']>240)
post=dict(slot_hours=2*(92+130+185),core_hours=20*2*(92+130+185))
post['capacity_bound_hours']=post['slot_hours']/3
post['capacity_bound_days']=post['capacity_bound_hours']/24

# Re-evaluate the same synthetic packet under the two live paragraphs.
decisions=dict(input=dict(r=.06,t=.01),
    paragraph_197_198='change E to 28 then launch confirmation',
    paragraph_192_193_205='keep completed E14 cohort and disclose; any new E is a new campaign')
check('both policy branches remain in submitted body',
    '넘으면 확인 런 전에 수준을 고친다' in text and '확인 18 런 **뒤**에 돌린다' in text)

out=dict(scope='document extraction, baseline arithmetic and synthetic countermodels; no simulations',
    pin=pin,baseline=dict(commit='18787ab98a13361c37b2343bd07ae276142d0953',
       generator_git_blob=blob,generator_sha256=sha(b)),
    B_intervention=changes,short_long_observation=prefix,
    screen_vs_MID=threshold,joint_screen_counterexample=joint,
    one_seed_counterexample=one_seed,unqualified_fallback=unqualified_fallback,
    rank_countermodel=rank,budget_bounds=cost,postcheck_cost=post,
    conflicting_policies=decisions,assertions=dict(passed=len(checks),failed=0,names=checks))
(ROOT/'audit_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='pin'},ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in pin.items() if k!='line_map'},ensure_ascii=False,indent=2))

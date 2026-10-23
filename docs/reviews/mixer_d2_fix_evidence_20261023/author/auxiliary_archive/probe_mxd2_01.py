#!/usr/bin/env python3
import importlib.util,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'scripts'))
import mixer_deck_readback as rb
import mixer_deck_diff as dd
import mixer_smoke_blind as sb
spec=importlib.util.spec_from_file_location('baseline_generator',BASE/'baseline/make_mixer_deck.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def arm(name,coated):
 x=1.0 if coated else .3
 return g.register_arm(name,g.gm_arm({'AM_P':x,'AM_S':x,'SE':1.0},gamma_wall=g.gm_wall_from_ncm(.3),bo_se=.73,rho_uncoated_ncm=.3))
u=arm('GMUNCOATED',False);c=arm('GMCOATED',True)
ps=g.plan(100000,cgf=151.4,dens_gen='lab20261014')
ph=g.plan(100000,cgf=151.4,dens_gen='lab20261014',stiffen_se=20)
rpm=g.resolve_rpm(ps['R'])
soft=g.deck(ps,rpm,2,arm=u)
ref=g.deck(ph,rpm,2,arm=u,hold_bo_pairwise=True)
coat=g.deck(ph,rpm,2,arm=c,hold_bo_pairwise=True)
A=rb.read_deck(soft,label='soft');B=rb.read_deck(ref,label='ref')
rr=rb.compare('E',A,B)
rows={}
for allow in ('A','B','U','E','EB'):
 r=dd.diff_decks(ref,coat,allow=allow)
 rows[allow]={k:r.get(k) for k in ('verdict','outside','missing','non_ced_diffs','e_rule','u_rule') if r.get(k) is not None}
old_counts=sb._expected_counts({'stiffen_se':20})
lab_counts={i+1:int(ph['n'][t]) for i,t in enumerate(g.TYPES)}
out={'source_baseline':'7799a2ff64ba462b42ce05edd3e63b7c2854d557','readback_lab_E':{'verdict':rr['verdict'],'failures':rr['failures']},'coated_pair_diffs':rows,'smoke_counts':{'current':old_counts,'actual_lab_plan':lab_counts},'density_table_actual':{'soft':A['templates'],'ref':B['templates']},'note':'Local synthetic deck generation only; no LIGGGHTS, experiment, new registration, or launch.'}
assert rr['verdict']=='FAIL'
assert all(x['verdict']=='FAIL' for x in rows.values())
assert old_counts != lab_counts
p=BASE/'mxd2-01-probe.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))

#!/usr/bin/env python3
"""Independent synthetic-deck attacks; no simulator, network, git mutation or launch."""
import argparse
import copy
import hashlib
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def logical(text):
    rows, buffer = [], ''
    for raw in text.splitlines():
        code = raw.partition('#')[0].rstrip()
        continued = code.endswith('&')
        buffer += ' ' + (code[:-1] if continued else code)
        if not continued:
            if buffer.split():
                rows.append(buffer.split())
            buffer = ''
    assert not buffer.strip()
    return rows


def render(rows):
    return '\n'.join(' '.join(row) for row in rows) + '\n'


def rebound(text, meta):
    result = copy.deepcopy(meta)
    raw = text.encode('utf-8')
    result.update(deck_sha256=hashlib.sha256(raw).hexdigest(), deck_bytes=len(raw))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    repo = args.repo.resolve(strict=True)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(repo / 'scripts'))
    import make_mixer_deck as gen
    import mixer_deck_readback as rb
    import mixer_deck_diff as dd
    import mixer_smoke_blind as smoke
    source_files = ['make_mixer_deck.py', 'mixer_deck_readback.py', 'mixer_deck_diff.py', 'mixer_smoke_blind.py', 'test_mixer_d2_consumers.py']
    hashes = {name: hashlib.sha256((repo/'scripts'/name).read_bytes()).hexdigest() for name in source_files}
    rows = []

    def fixture(phases=('AM_P','AM_S','SE'), generation='lab20261014', stiff=20.,
                rho=.25, coated=False, layered=True):
        old_phases = gen.TYPES
        try:
            gen.set_phases(phases)
            gamma = {p: 1. if coated or p=='SE' else rho for p in phases}
            arm = gen.gm_arm(gamma, gamma_wall=.0256*rho, bo_se=1.125,
                             layered=layered, rho_uncoated_ncm=rho)
            gen.register_arm('INDEPENDENT_ATTACK', arm)
            plan = gen.plan(100003, cgf=125., stiffen_se=stiff, dens_gen=generation)
            rpm = gen.resolve_rpm(plan['R'])
            text = gen.deck(plan,rpm,2,seed=49979687,arm='INDEPENDENT_ATTACK',hold_bo_pairwise=True)
            meta = gen.deck_meta(plan,rpm,2,49979687,'INDEPENDENT_ATTACK',text,hold_bo_pairwise=True)
            return text, meta, {str(i+1):int(plan['n'][p]) for i,p in enumerate(phases)}
        finally:
            gen.ARMS.pop('INDEPENDENT_ATTACK',None)
            gen.set_phases(old_phases)

    def check(label, text, meta, expected, pair=None, note=''):
        calls = [('readback',lambda:rb.read_d2(text,meta)), ('plan',lambda:smoke.d2_plan_check(text,meta))]
        if pair is not None:
            calls.append(('pair',lambda:dd.diff_d2_decks(text,pair[0],meta,pair[1])))
        case = {'label':label,'expected':expected,'note':note,'calls':{}}
        for name,fn in calls:
            try:
                result=fn();verdict=result.get('verdict')
                actual={'verdict':verdict,'failures':result.get('failures'),
                        'registered':result.get('registered'),'execution_authorized':result.get('execution_authorized'),
                        'expected_counts':result.get('expected_counts')}
                actual['matches_expectation'] = expected is None or verdict==expected
                actual['authority_boundary'] = result.get('registered') is None and result.get('execution_authorized') is False
            except Exception as exc:
                actual={'verdict':'EXCEPTION','exception':repr(exc),'matches_expectation':False,'authority_boundary':False}
            case['calls'][name]=actual
        rows.append(case)
        if expected=='FAIL' and any(v['verdict']=='PASS' for v in case['calls'].values()):
            folder=out/'survivors'/label;folder.mkdir(parents=True)
            (folder/'reference.in').write_text(text)
            (folder/'reference_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
            if pair:
                (folder/'new.in').write_text(pair[0]);(folder/'new_meta.json').write_text(json.dumps(pair[1],ensure_ascii=False,indent=2)+'\n')

    for phases,generation,stiff,rho,layered in itertools.product(
            [('AM_P','AM_S','SE'),('AM_P','SE')],['gen1','lab20261014'],[1.,20.],[.25,1.,3.],[False,True]):
        a,am,counts=fixture(phases,generation,stiff,rho,False,layered)
        b,bm,_=fixture(phases,generation,stiff,rho,True,layered)
        label='positive_'+str(len(rows))
        check(label,a,am,'PASS',(b,bm))
        for key in ('readback','plan'):
            rows[-1]['calls'][key]['counts_match_independent_fixture']=rows[-1]['calls'][key]['expected_counts']==counts

    a,am,counts=fixture();b,bm,_=fixture(coated=True)
    ac,bc=logical(a),logical(b)
    aa,bb=render(ac),render(bc)
    check('comments_removed_normal',aa,rebound(aa,am),'PASS',(bb,rebound(bb,bm)))
    check('stale_hash',aa,am,'FAIL',(bb,bm))

    def common(label, mutate, expected='FAIL', note=''):
        x,y=copy.deepcopy(ac),copy.deepcopy(bc)
        mutate(x);mutate(y)
        assert x!=ac and y!=bc,label+' mutation was a no-op'
        ta,tb=render(x),render(y)
        check(label,ta,rebound(ta,am),expected,(tb,rebound(tb,bm)),note)

    def replace_token(rows,predicate,index,value):
        targets=[r for r in rows if predicate(r)]
        assert targets
        for r in targets:
            r[index] = value(r[index]) if callable(value) else value

    gravity=lambda r:len(r)>3 and r[:1]==['fix'] and r[3]=='gravity'
    template=lambda r:len(r)>3 and r[:1]==['fix'] and r[3]=='particletemplate/sphere'
    ced=lambda r:len(r)>4 and r[:1]==['fix'] and r[4]=='cohesionEnergyDensity'
    for name,value in [('wrong','1'),('nan','nan'),('infinity','inf'),('unicode','９.８１'),('underscore','9.8_1')]:
        common('gravity_'+name,lambda x,v=value:replace_token(x,gravity,4,v))
    common('gravity_unknown_group',lambda x:replace_token(x,gravity,2,'no_such_group'))
    def gravity_se_only(x):
        replace_token(x,gravity,2,'onlySE')
        index=next(i for i,r in enumerate(x) if gravity(r))
        x.insert(index,['group','onlySE','type','3'])
    common('gravity_SE_only',gravity_se_only)
    common('gravity_wrong_vector',lambda x:replace_token(x,gravity,8,'1'))
    def unfix_before_run(x, predicate):
        identity=next(r[1] for r in x if predicate(r))
        index=next(i for i,r in enumerate(x) if r[0]=='run')
        x.insert(index,['unfix',identity])
    common('unfix_gravity_before_run',lambda x:unfix_before_run(x,gravity))
    common('unfix_CED_before_run',lambda x:unfix_before_run(x,ced))
    common('density_wrong_same_both',lambda x:replace_token(x,lambda r:template(r) and '1640' in r,radius_density_index(ac, 'density'),'2000'))
    for name,convert in [('unicode',lambda v:v.translate(str.maketrans('0123456789','０１２３４５６７８９'))),
                         ('underscore',lambda v:v[:-1]+'_'+v[-1])]:
        common('density_'+name,lambda x,f=convert:replace_token(x,template,radius_density_index(ac,'density'),f))
    common('radius_wrong',lambda x:replace_token(x,template,radius_density_index(ac,'radius'),lambda v:str(float(v)*1.1)))
    common('radius_nan',lambda x:replace_token(x,template,radius_density_index(ac,'radius'),'nan'))
    for name,value in [('nan','nan'),('unicode','１'),('negative','-1')]:
        common('ced_'+name,lambda x,v=value:replace_token(x,ced,7,v))
    for name,predicate in [('gravity',gravity),('ced',ced),('create_box',lambda r:r[0]=='create_box'),
                           ('distribution',lambda r:len(r)>3 and r[3]=='particledistribution/discrete')]:
        common('duplicate_'+name,lambda x,p=predicate:x.append(copy.deepcopy(next(r for r in x if p(r)))))
    for name,token,value in [('count','particles_in_region',lambda v:str(int(v)+100)),
                            ('count_unicode','particles_in_region',lambda v:v.translate(str.maketrans('0123456789','０１２３４５６７８９')))]:
        common('insert_'+name,lambda x,t=token,v=value:replace_token(x,lambda r:t in r,next(r.index(t)+1 for r in ac if t in r),v))
    common('second_insert_seed',lambda x:replace_token(x,lambda r:len(r)>3 and r[3]=='insert/pack' and r[1]=='insB',5,'67867967'),
           None,'Observation only: independently assess whether single meta.seed promises binding of all actual insertion seeds.')
    geo=next(i for i,r in enumerate(ac) if r[:3]==['region','reg','block'])
    one=copy.deepcopy(ac);one[geo][3]=str(float(one[geo][3])*1.1)
    ta=render(one)
    case={'label':'one_sided_geometry','expected':'FAIL','calls':{}}
    result=dd.diff_d2_decks(ta,bb,rebound(ta,am),rebound(bb,bm))
    case['calls']['pair']={'verdict':result['verdict'],'failures':result['failures'],'matches_expectation':result['verdict']=='FAIL'};rows.append(case)
    common('common_geometry_unregistered',lambda x:replace_token(x,lambda r:r[:3]==['region','reg','block'],3,lambda v:str(float(v)*1.1)),
           None,'No concrete D2 geometry registration is supplied; equal physical geometry alone is not declared invalid by this audit.')

    for label,mut in [('bo_wrong',lambda m:m['adhesion_rule'].update(bo_se=9.)),
                      ('bo_nan',lambda m:m['adhesion_rule'].update(bo_se=float('nan'))),
                      ('density_generation_wrong',lambda m:m.update(dens_gen='gen1')),
                      ('seed_wrong',lambda m:m.update(seed=67867967)),
                      ('count_wrong',lambda m:m.update(n_atoms_planned=100004)),
                      ('revolutions_nan',lambda m:m.update(revolutions=float('nan'))),
                      ('unknown_field',lambda m:m.update(unknown=1))]:
        mm=copy.deepcopy(am);mut(mm);check('meta_'+label,a,mm,'FAIL')

    p=gen.plan(100000,cgf=151.4,stiffen_se=20.)
    rpm=gen.resolve_rpm(p['R'])
    lc=gen.deck(p,rpm,2,arm='LC',hold_bo_pairwise=True)
    lh=gen.deck(p,rpm,2,arm='LH',hold_bo_pairwise=True)
    old=dd.diff_decks(lc,lh,allow='B')
    rows.append({'label':'legacy_B','expected':'PASS','calls':{'pair':{'verdict':old['verdict'],'matches_expectation':old['verdict']=='PASS'}}})
    for allow in ('A','B','U','E','EB'):
        result=dd.diff_decks(a,b,allow=allow)
        rows.append({'label':'D2_rejected_by_legacy_'+allow,'expected':'FAIL','calls':{'pair':{'verdict':result['verdict'],'matches_expectation':result['verdict']=='FAIL'}}})

    failed=[r['label']+':'+k for r in rows for k,v in r['calls'].items() if not v['matches_expectation'] or v.get('counts_match_independent_fixture') is False]
    result={'source_hashes':hashes,'cases':rows,'failed_expectations':failed,'case_count':len(rows),
            'call_count':sum(len(r['calls']) for r in rows),'scope':'synthetic source/deck tests only; no physical simulation, registration or launch authority'}
    (out/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},ensure_ascii=False,indent=2))
    return int(bool(failed))


def radius_density_index(rows,key):
    row=next(r for r in rows if len(r)>3 and r[3]=='particletemplate/sphere')
    return row.index(key)+2


if __name__=='__main__':
    raise SystemExit(main())

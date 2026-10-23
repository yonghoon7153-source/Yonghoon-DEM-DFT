#!/usr/bin/env python3
"""Independent MXD2 generator attack review; no simulator is executed.

python -I reproduce.py --repo /path/to/repo --patch /path/to/generator.patch --out /tmp/review
The source repository is only read. Scratch files and every emitted deck go under --out.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def parse(text):
    rows = [line.split('#', 1)[0].split() for line in text.replace('&\n', ' ').splitlines()]
    fixes = [t for t in rows if t and t[0] == 'fix']
    def prop(k):
        return next(t for t in fixes if len(t) > 4 and t[4] == k)
    e = list(map(float, prop('youngsModulus')[6:]))
    nu = list(map(float, prop('poissonsRatio')[6:]))
    t = prop('cohesionEnergyDensity')
    n = int(t[6])
    vals = list(map(float, t[7:]))
    assert len(vals) == n*n
    c = [vals[i*n:(i+1)*n] for i in range(n)]
    radii, densities = {}, {}
    for t in fixes:
        if 'particletemplate/sphere' in t:
            i = int(t[t.index('atom_type')+1])-1
            radii[i] = float(t[t.index('radius')+2])
            densities[i] = float(t[t.index('density')+2])
    g = float(next(t for t in fixes if 'gravity' in t)[4])
    pairs = {}
    for i in range(n):
        for j in range(i, n):
            if i == j == n-1:
                assert c[i][j] == 0
                continue
            r = radii[i]
            rs = r if j == n-1 else r*radii[j]/(r+radii[j])
            rmin = r if j == n-1 else min(r, radii[j])
            es = 1/((1-nu[i]**2)/e[i]+(1-nu[j]**2)/e[j])
            A = (4/3)*es*math.sqrt(rs)
            B = 2*math.pi*rs*c[i][j]
            f0 = B**3/A**2
            delta0 = (B/A)**2
            pairs[(i,j)] = dict(F0=f0, delta0_over_r=delta0/rmin, Rstar=rs, Estar=es, CED=c[i][j])
            assert c[i][j] == c[j][i]
    weight = 4/3*math.pi*radii[2]**3*densities[2]*g
    return dict(g=g, radii=radii, densities=densities, pairs=pairs, bo=pairs[(2,2)]['F0']/weight,
                e=e, nu=nu, c=c)


def arm(m, rho=0.3, coating=False, bo=0.73, **kw):
    ga = 1.0 if coating else rho
    return m.gm_arm({'AM_P':ga, 'AM_S':ga, 'SE':1.0}, gamma_wall=m.gm_wall_from_ncm(rho),
                    bo_se=bo, rho_uncoated_ncm=rho, **kw)


def emit(m, rho=.3, coating=False, bo=.73, gen='lab20261014', cgf=151.4, stiff=20., a=None, p=None):
    name = 'INDEPENDENT'
    m.ARMS.pop(name, None)
    m.register_arm(name, arm(m, rho, coating, bo) if a is None else a)
    try:
        p = m.plan(100000, cgf=cgf, dens_gen=gen, stiffen_se=stiff) if p is None else p
        rpm = m.resolve_rpm(p['R'])
        text = m.deck(p, rpm, 2, arm=name, hold_bo_pairwise=True)
        meta = m.deck_meta(p, rpm, 2, 32452843, name, text, hold_bo_pairwise=True)
        return text, meta
    finally:
        m.ARMS.pop(name, None)


def outcome(call):
    try:
        value = call()
        return {'kind':'accepted', 'type':type(value).__name__}
    except BaseException as e:
        return {'kind':'controlled_rejection' if isinstance(e, (SystemExit, argparse.ArgumentTypeError)) else 'uncontrolled_exception',
                'type':type(e).__name__, 'message':str(e)[:300]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--patch', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    snap = out/'snapshot'
    (snap/'scripts').mkdir(parents=True, exist_ok=True)
    for name in ('make_mixer_deck.py','additives.py'):
        shutil.copyfile(args.repo/'scripts'/name, snap/'scripts'/name)
    if args.patch:
        subprocess.run(['patch','--batch','-p1','--directory',str(snap),'--input',str(args.patch.resolve())], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    src = snap/'scripts/make_mixer_deck.py'
    code = src.read_text()
    m = module(src, 'review_generator')
    result = {'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(), 'normal':{}, 'input':{}, 'mutations':{}, 'observations':{}}
    max_bo_error = max_pair_error = max_overlap = 0.0
    count = 0
    for gen, cgf, stiff, rho, coating, bo in itertools.product(
            ('gen1','lab20261014'), (75.7,151.4,302.8), (1.,20.), (.03,.3,1.,10.), (False,True), (.73,12.5)):
        text, meta = emit(m, rho, coating, bo, gen, cgf, stiff)
        p = parse(text)
        assert p['g'] == 9.81
        assert meta['schema'] == 'mixer_deck_meta/2' and meta['registered'] is None
        assert meta['adhesion_rule']['bo_se'] == bo
        assert meta['deck_sha256'] == hashlib.sha256(text.encode()).hexdigest()
        expected_density = 2000. if gen == 'gen1' else 1640.
        assert p['densities'][2] == expected_density
        max_bo_error = max(max_bo_error, abs(p['bo']/bo-1))
        gam = [1. if coating else rho, 1. if coating else rho, 1., .0256*rho]
        for (i,j), row in p['pairs'].items():
            expected_ratio = math.sqrt(gam[i])*math.sqrt(gam[j])*row['Rstar']/(p['radii'][2]/2)
            observed_ratio = row['F0']/p['pairs'][(2,2)]['F0']
            max_pair_error = max(max_pair_error, abs(observed_ratio/expected_ratio-1))
            max_overlap = max(max_overlap, row['delta0_over_r'])
            assert row['delta0_over_r'] <= .01*(1+2e-5)
        count += 1
    assert max_bo_error < 2e-5 and max_pair_error < 3e-5
    result['normal'] = dict(decks=count, physical_pair_checks=9*count, max_relative_Bo_error=max_bo_error,
                            max_relative_pair_rule_error=max_pair_error, max_delta0_over_r=max_overlap)

    numeric_bad = {'nan':float('nan'), 'inf':float('inf'), 'neg_inf':-float('inf'), 'zero':0.,
                   'negative':-1., 'boolean':True, 'string':'0.3', 'subnormal':1e-310,
                   'huge_integer':10**1000, 'none':None, 'list':[], 'empty_dict':{}}
    for key, value in numeric_bad.items():
        result['input']['bo_'+key] = outcome(lambda v=value: emit(m, bo=v))
        result['input']['rho_'+key] = outcome(lambda v=value: emit(m, rho=v))
    for key, value in {'empty':{}, 'partial':{'AM_P':.3}, 'mixed_key':{'AM_P':.3, 'AM_S':.3, 7:1.},
                       'list':[], 'none':None}.items():
        result['input']['gamma_'+key] = outcome(lambda v=value: emit(m, a=m.gm_arm(v, gamma_wall=.00768, bo_se=.73, rho_uncoated_ncm=.3)))
    for key, value in {'empty':{}, 'partial':{'rule':'geomean','_gm_valid':True}, 'list':[], 'none':None}.items():
        result['input']['arm_'+key] = outcome(lambda v=value: emit(m, a=v) if v is not None else m.register_arm('STRUCTNULL', v))
    result['input']['mixed_ceiling'] = outcome(lambda:emit(m, rho=10., bo=800.))
    result['input']['no_density_generation'] = outcome(lambda:emit(m, gen=None))
    result['input']['unbound_wall'] = outcome(lambda:emit(m, a=m.gm_arm({'AM_P':.3,'AM_S':.3,'SE':1.}, gamma_wall=.00768, bo_se=.73)))
    result['input']['rho_gamma_mismatch'] = outcome(lambda:emit(m, a=m.gm_arm({'AM_P':.3,'AM_S':.5,'SE':1.}, gamma_wall=.00768, bo_se=.73, rho_uncoated_ncm=.3)))
    for s in ('', ' ', 'NaN','inf','1e999','0_3','０.３',' 0.3','0.3 ','0.3\n','0x1','1e-310'):
        result['input']['cli_'+repr(s)] = outcome(lambda t=s:m._gm_cli_number(t))
    cli_bad = ('', 'AM_P=.3', 'AM_P=.3,AM_S=.3,AM_P=.3', 'AM_P=NaN,AM_S=.3',
               'AM_P=inf,AM_S=.3', 'AM_P=1e999,AM_S=.3', 'AM_P=0_3,AM_S=.3',
               'AM_P=０.３,AM_S=.3', 'AM_P= .3,AM_S=.3', 'AM_P=.3,AM_S=.3,',
               'AM_P=.3,AM_S=.3,SE=2', 'AM_P=1e-310,AM_S=1e-310')
    result['cli_input'] = []
    for i,value in enumerate(cli_bad):
        folder=out/'cli_bad'/str(i)
        proc=subprocess.run([sys.executable,'-I',str(src),'--gm-gamma',value,'--gm-wall-ncm','.3',
                             '--gm-bo-se','.73','--dens-gen','lab20261014','--n-total','100000',
                             '--cgf','151.4','--out',str(folder)],capture_output=True,text=True)
        result['cli_input'].append({'gamma':value,'rc':proc.returncode,'emitted':(folder/'in.mixer').exists(),
                                    'traceback':'Traceback' in proc.stderr})
        assert proc.returncode != 0 and not (folder/'in.mixer').exists() and 'Traceback' not in proc.stderr
    for i, (flag,value) in enumerate(itertools.product(('--gm-wall-ncm','--gm-bo-se'),
            ('nan','inf','1e999','1e-310','0_3','０.３',' 0.3','', '0','-1'))):
        folder=out/'cli_bad_scalar'/str(i)
        vals={'--gm-wall-ncm':'.3','--gm-bo-se':'.73'}
        vals[flag]=value
        proc=subprocess.run([sys.executable,'-I',str(src),'--gm-gamma','AM_P=.3,AM_S=.3',
                             '--gm-wall-ncm',vals['--gm-wall-ncm'],'--gm-bo-se',vals['--gm-bo-se'],
                             '--dens-gen','lab20261014','--n-total','100000','--cgf','151.4',
                             '--out',str(folder)],capture_output=True,text=True)
        result['cli_input'].append({'flag':flag,'value':value,'rc':proc.returncode,
                                    'emitted':(folder/'in.mixer').exists(),'traceback':'Traceback' in proc.stderr})
        assert proc.returncode != 0 and not (folder/'in.mixer').exists() and 'Traceback' not in proc.stderr

    # Existing public set_phases allows AM_P + SE without AM_S; both versions are exercised.
    result['observations']['active_phases_regression'] = {}
    for label,path in [('original',args.repo/'scripts/make_mixer_deck.py'),('patched',src)]:
        other=module(path,'active_'+label)
        other.set_phases(('AM_P','SE'))
        def two_phase():
            a=other.gm_arm({'AM_P':.3,'SE':1.},gamma_wall=other.gm_wall_from_ncm(.3),bo_se=.73,rho_uncoated_ncm=.3)
            n=other.register_arm('TWOPHASE',a)
            p=other.plan(100000,cgf=151.4,dens_gen='lab20261014')
            t=other.deck(p,other.resolve_rpm(p['R']),2,arm=n)
            (out/('two_phase_'+label+'.in.mixer')).write_text(t)
            return t
        result['observations']['active_phases_regression'][label]=outcome(two_phase)

    # Test both constructor and post-construction mutation through actual production entrypoints.
    desc_bad = ['independent review\nprint "DESC_EXECUTES"\n#',
                'independent review\rprint "DESC_EXECUTES"\r#',
                'independent review\r\nprint "DESC_EXECUTES"\r\n#', 7, [], {}, True]
    desc_results = []
    for value in desc_bad:
        construction=outcome(lambda v=value:emit(m,a=arm(m,desc=v)))
        a=arm(m); a['desc']=value
        m.register_arm('DESCMUTATE',a)
        p=m.plan(100000,cgf=151.4,dens_gen='lab20261014',stiffen_se=20.)
        rpm=m.resolve_rpm(p['R'])
        d=outcome(lambda:m.deck(p,rpm,2,arm='DESCMUTATE',hold_bo_pairwise=True))
        md=outcome(lambda:m.deck_meta(p,rpm,2,32452843,'DESCMUTATE','',hold_bo_pairwise=True))
        m.ARMS.pop('DESCMUTATE')
        desc_results.append({'value':repr(value),'constructor':construction,'deck_mutation':d,'meta_mutation':md})
        assert all(x['kind']=='controlled_rejection' for x in (construction,d,md))
    for value in ('', 'ordinary description', '설명 · 한 줄', 'trailing ampersand &'):
        t,md=emit(m,a=arm(m,desc=value))
        assert md['arm_desc']==value
    result['observations']['description_input']=desc_results

    # Full emission and parsing for both coated/uncoated AM_P+SE, where SE is now type 2.
    active_results=[]
    m.set_phases(('AM_P','SE'))
    for rho,coating in itertools.product((.03,.3,1.,10.),(False,True)):
        ga=1. if coating else rho
        a=m.gm_arm({'AM_P':ga,'SE':1.},gamma_wall=m.gm_wall_from_ncm(rho),bo_se=.73,rho_uncoated_ncm=rho)
        t,md=emit(m,a=a)
        assert md['types']=={'1':'AM_P','2':'SE','3':'WALL'}
        ls=[line.split('#',1)[0].split() for line in t.replace('&\n',' ').splitlines()]
        def prop(name):return next(x for x in ls if len(x)>4 and x[0]=='fix' and x[4]==name)
        E=list(map(float,prop('youngsModulus')[6:]));nu=list(map(float,prop('poissonsRatio')[6:]))
        ced=list(map(float,prop('cohesionEnergyDensity')[7:]))[4]
        tpl=next(x for x in ls if 'particletemplate/sphere' in x and x[x.index('atom_type')+1]=='2')
        rad=float(tpl[tpl.index('radius')+2]);den=float(tpl[tpl.index('density')+2])
        g=float(next(x for x in ls if len(x)>4 and x[0]=='fix' and x[3]=='gravity')[4])
        es=E[1]/(2*(1-nu[1]**2));rs=rad/2
        f0=(2*math.pi*rs*ced)**3/((4/3)*es*math.sqrt(rs))**2
        bo=f0/(4/3*math.pi*rad**3*den*g)
        assert abs(bo/.73-1)<2e-5
        active_results.append({'rho':rho,'coating':coating,'SE_Bo':bo,'deck_bytes':len(t.encode())})
    m.set_phases(('AM_P','AM_S','SE'))
    result['observations']['active_phase_numeric']=active_results

    # Mutated density identity still yields deck and meta despite the declared generation.
    plan = m.plan(100000, cgf=151.4, dens_gen='lab20261014', stiffen_se=20.)
    plan['dens'] = dict(m.DENS_GENERATIONS['gen1'])
    text, meta = emit(m, p=plan)
    (out/'density_identity.in.mixer').write_text(text)
    result['observations']['density_identity'] = {'label':meta['dens_gen'], 'meta_SE_g_cm3':meta['dens_g_cm3']['SE'],
                                                 'printed_SE_kg_m3':parse(text)['densities'][2]}

    # Stable arm name + wrong serialized text can produce self-consistent hash but incorrect identity.
    old, old_meta = emit(m, bo=.73)
    a = arm(m, bo=12.5)
    m.register_arm('METASWAP', a)
    p = m.plan(100000,cgf=151.4,dens_gen='lab20261014',stiffen_se=20.)
    meta = m.deck_meta(p,m.resolve_rpm(p['R']),2,32452843,'METASWAP',old,hold_bo_pairwise=True)
    m.ARMS.pop('METASWAP')
    result['observations']['metadata_text_mismatch'] = {'printed_Bo':parse(old)['bo'], 'meta_Bo':meta['adhesion_rule']['bo_se'],
                                                        'hash_matches_text':meta['deck_sha256']==hashlib.sha256(old.encode()).hexdigest()}

    # Resolve the limiting unloaded contact from printed values; quantify a single static SE load separately.
    text,_=emit(m, rho=1., bo=1., stiff=1.)
    p=parse(text)
    limiting=max(p['pairs'],key=lambda k:p['pairs'][k]['delta0_over_r'])
    bo_limit=(.01/p['pairs'][limiting]['delta0_over_r'])**1.5
    bo_near=bo_limit*(1-2e-5)
    text,_=emit(m,rho=1.,bo=bo_near,stiff=1.)
    (out/'near_ceiling.in.mixer').write_text(text)
    p=parse(text)
    row=p['pairs'][(2,2)]
    radius=p['radii'][2]
    A=4/3*row['Estar']*math.sqrt(row['Rstar'])
    B=2*math.pi*row['Rstar']*row['CED']
    W=4/3*math.pi*radius**3*p['densities'][2]*p['g']
    lo=(B/A)**2; hi=radius
    for _ in range(100):
        mid=(lo+hi)/2
        if A*mid**1.5-B*mid-W>0: hi=mid
        else: lo=mid
    result['observations']['static_contact_scope']={'bo':bo_near,'limiting_pair':str(limiting),
        'SE_SE_unloaded_delta_over_r':row['delta0_over_r'],'SE_SE_one_weight_delta_over_r':(lo+hi)/2/radius}

    substitutions = {
      'gravity_1':('fix             gravi all gravity 9.81 vector','fix             gravi all gravity 1.0 vector'),
      'gravity_1_d2_only':('fix             gravi all gravity 9.81 vector',"fix             gravi all gravity {1.0 if ARMS[arm].get('rule') == 'geomean' else 9.81} vector"),
      'radius_half':("f'radius constant {d[_t]/2:.6g}'", "f'radius constant {d[_t]/4:.6g}'"),
      'force_gen1_density':("(DENS if dens is None else dens)[mat_se]", "DENS[mat_se]"),
      'meta_bo_constant':("gamma_wall=a_['gamma_wall'], bo_se=a_['bo_se'],", "gamma_wall=a_['gamma_wall'], bo_se=BO_BASE,"),
      'mixed_ceiling_removed':("ov = pair_overlap(M[i][j], ti, tj, d, E)", "ov = 0.0 if ti != tj and WALL not in (ti, tj) else pair_overlap(M[i][j], ti, tj, d, E)"),
      'schema_old':("meta.update(schema='mixer_deck_meta/2', registered=None,", "meta.update(schema='mixer_deck_meta/1', registered=None,"),
      'register_name_match':("not _ARM_NAME_RE.fullmatch(name)", "not _ARM_NAME_RE.match(name)"),
      'wall_cli_float':("'--gm-wall-ncm', type=_gm_cli_number", "'--gm-wall-ncm', type=float"),
      'bo_cli_float':("'--gm-bo-se', type=_gm_cli_number", "'--gm-bo-se', type=float"),
      'gravity_parser_hardcoded':("radius**3 * density * gravity_magnitude", "radius**3 * density * 9.81"),
      'active_pair_old':("if not (all(v == rho for v in ncm) or all(v == 1.0 for v in ncm)):",
                         "if (g.get('AM_P'), g.get('AM_S')) not in ((rho, rho), (1.0, 1.0)):"),
      'desc_guard_removed':("    if not isinstance(desc, str) or '\\n' in desc or '\\r' in desc:\n        raise SystemExit('⛔ D2 결합 규칙: 설명은 줄바꿈 없는 문자열이어야 한다 (덱 명령 주입 거부)')\n", ""),
      'desc_cr_guard_removed':("or '\\n' in desc or '\\r' in desc:","or '\\n' in desc:"),
    }
    for name, (before,after) in substitutions.items():
        assert code.count(before)==1, (name,code.count(before))
        folder=out/'mutants'/name
        folder.mkdir(parents=True,exist_ok=True)
        dst=folder/'make_mixer_deck.py'
        dst.write_text(code.replace(before,after))
        shutil.copyfile(snap/'scripts/additives.py',folder/'additives.py')
        proc=subprocess.run([sys.executable,'-I',str(dst),'--selftest'],capture_output=True,text=True)
        (folder/'selftest.log').write_text(proc.stdout+proc.stderr)
        failed=[line.strip() for line in proc.stdout.splitlines() if 'FAIL' in line]
        result['mutations'][name]={'selftest_rc':proc.returncode,'failed':failed}
        if name.startswith('gravity_1'):
            mm=module(dst,'gravity_mutant')
            text, meta=emit(mm)
            (folder/'in.mixer').write_text(text)
            pp=parse(text)
            result['mutations'][name].update(printed_gravity=pp['g'],actual_Bo_from_printed_SI=pp['bo'],meta_Bo=meta['adhesion_rule']['bo_se'])
        if name in ('wall_cli_float','bo_cli_float'):
            ga='AM_P=3,AM_S=3' if name=='wall_cli_float' else 'AM_P=.3,AM_S=.3'
            wall='0_3' if name=='wall_cli_float' else '.3'
            bo='.73' if name=='wall_cli_float' else '0_73'
            dd=folder/'emitted'
            proc=subprocess.run([sys.executable,'-I',str(dst),'--gm-gamma',ga,'--gm-wall-ncm',wall,
                                 '--gm-bo-se',bo,'--dens-gen','lab20261014','--n-total','100000',
                                 '--cgf','151.4','--out',str(dd)],capture_output=True,text=True)
            result['mutations'][name].update(cli_rc=proc.returncode,emitted=(dd/'in.mixer').exists(),raw_wall=wall,raw_bo=bo)
    (out/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'normal':result['normal'],'mutations':result['mutations'],'observations':result['observations'],
                      'uncontrolled_inputs':{k:v for k,v in result['input'].items() if v['kind']=='uncontrolled_exception'}},
                     ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())

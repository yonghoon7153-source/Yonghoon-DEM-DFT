"""Independent R01/R04 boundary, label, input hierarchy and numeric sweeps.

Small resistor graphs/producer records only; no DEM or 214 production runs.
"""
from pathlib import Path
import contextlib
import copy
import io
import json
import math
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '1'
os.environ['TMP'] = os.environ['TEMP'] = str(ROOT/'tmp')
sys.path[:0] = [str(ROOT/'source/scripts'), str(ROOT/'source/webapp'),
               str(WORK/'lhs_coverage_review_20260930/deps'), str(WORK/'gen2_network_reverify3_20261007/deps')]
import network_conductivity as nc
import tau_flux as tf

OUT = {'pin':'77d8fd44545c33cd10ab18fc250c7ad3023833ea', 'failures':[]}

def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return fn(*a, **kw)

def safe(fn, *a, **kw):
    try:
        return {'value':fn(*a, **kw), 'error':None}
    except Exception as e:
        return {'value':None, 'error':type(e).__name__+': '+str(e)}

def check(ok, category, detail):
    if not ok:
        OUT['failures'].append({'category':category, 'detail':detail})

def circuit(plate_z=.75, **kw):
    n = dict(nodes={0,1,2}, bottom={0}, top={2}, scale=1., plate_z=plate_z, box_x=1., box_y=1.,
             edges=[dict(id1=a, id2=b, R_total=.25, R_bulk=.1, R_constriction=.15) for a,b in ((0,1),(1,2))])
    n.update(kw)
    return n

def bound(cert, branch, mode='hertz'):
    c=copy.deepcopy(cert)
    c.update(channel='ionic', role=tf.CERT_ROLE[mode], contact_mode='physics' if mode=='physics' else 'hertzian', sigma_bulk_S_cm=.003)
    return c

def direct(c, branch, st=None, reason=None, mode='hertz', q=None, sd=None):
    raw=(c['I_bottom']/c['delta_V'])*c['geometry']['plate_z']*c['geometry']['scale']/(c['geometry']['box_x']*c['geometry']['box_y']*c['geometry']['scale']**2)
    q=round(raw,8) if q is None else q
    sd=round(raw*.003*1000,6) if sd is None else sd
    return tf._cert_published_problem(mode, branch, {'sigma_grain_S_cm':.003,tf.CERT_BRANCH_REASON_KEY[branch]:reason}, q,sd,st or c['status'],c)

# Exact 3-node branches at adjacent floating point values, plus retention at q>1.5.
boundary=[]
for branch,base in (('full',.75),('bulk_only',.3),('constriction_only',.45)):
    for label,pz in [('below',math.nextafter(base,0.)),('equal',base),('above',math.nextafter(base,math.inf)),('far',base*4)]:
        n=circuit(pz)
        result=quiet(nc.solve_network,n,mode=branch)
        c=bound(n['solve_info'][branch],branch)
        T,A,why=nc._geometry_TA(c['geometry'])
        raw=c['I_bottom']*T/A
        if branch=='full' and raw>1.5:
            c.update(status='computed',reason=None)
            verdict=direct(c,branch,'computed',None)
            good=result==(None,None) and isinstance(verdict,str) and 'L214R-R01' in verdict and 'L214R-R04' not in verdict
        else:
            verdict=direct(c,branch,c['status'],c.get('reason'))
            good=result[1]==raw and verdict is None
        row=dict(branch=branch,where=label,raw=raw,saved=round(raw,8),producer=result,
                 producer_status=n['solve_info'][branch]['status'],verdict=verdict)
        boundary.append(row);check(good,'boundary',row)
OUT['boundary']=boundary

# Vary units, geometry and positive resistances: compare producer exact order vs consumer.
normal=[]
for branch in ('full','bulk_only','constriction_only'):
    for scale,box_x,box_y in [(1.,1.,1.),(.1,2.,3.),(10.,.5,2.),(1e-50,1e25,1e25),(1e50,1e-25,1e-25)]:
        for want in (.001,.4,1.4,1.6,20.):
            # G = 2, 5, 10/3 in the independent circuit; plate sets q away from a rounding boundary.
            g={'full':2.,'bulk_only':5.,'constriction_only':1/.3}[branch]
            pz=want*(box_x*box_y*scale)/g
            n=circuit(pz,scale=scale,box_x=box_x,box_y=box_y)
            result=quiet(nc.solve_network,n,mode=branch)
            c=bound(n['solve_info'][branch],branch)
            T,A,why=nc._geometry_TA(c['geometry'])
            raw=(c['I_bottom']/c['delta_V'])*T/A
            if branch=='full' and raw>1.5:
                c.update(status='computed',reason=None)
                verdict=direct(c,branch,'computed',None)
                ok=result==(None,None) and isinstance(verdict,str) and 'L214R-R01' in verdict
            else:
                verdict=direct(c,branch,c['status'],c.get('reason'))
                ok=result[1]==raw and verdict is None
            row=dict(branch=branch,geometry=c['geometry'],raw=raw,producer=result,verdict=verdict)
            normal.append(row);check(ok,'geometry_normal',row)
OUT['geometry_normal']=normal

# Exhaustive labels at exact equality and next float above, all three mode identities.
labels=[]
states=['computed','model_over_conduction',None,'not_computed','valid_zero',True,'COMPUTED']
reasons=[None,'q_gt_1p5','',False,0,'full_over_conduction',[],{}]
for mode in ('hertz','physics','hertz_h12'):
    for branch,base in [('full',.75),('bulk_only',.3),('constriction_only',.45)]:
        for pz in (base,math.nextafter(base,math.inf)):
            n=circuit(pz);quiet(nc.solve_network,n,mode=branch)
            original=bound(n['solve_info'][branch],branch,mode)
            for state in states:
                for reason in reasons:
                    c=copy.deepcopy(original);c.update(status=state,reason=reason)
                    raw=c['I_bottom']*pz
                    expected=('model_over_conduction','q_gt_1p5') if branch!='full' and raw>1.5 else ('computed',None)
                    should_pass=not(branch=='full' and raw>1.5) and (state,reason)==expected
                    got=safe(direct,c,branch,state,reason,mode)
                    row=dict(mode=mode,branch=branch,raw=raw,state=state,reason=reason,expected=should_pass,result=got)
                    labels.append(row)
                    check(got['error'] is None and (got['value'] is None)==should_pass,'labels',row)
OUT['labels']={'count':len(labels),'accepted':sum(x['result']['value'] is None and x['result']['error'] is None for x in labels),'cases':labels}

# Fresh producer record with uneven contacts and a temperature, not a submitted fixture.
atoms={i:dict(type=1,x=0.,y=0.,z=float(i-1),radius=1.) for i in range(1,22)}
contacts=[dict(id1=i,id2=i+1,contact_area=.5+(i%3)*.03,delta=.2+(i%4)*.01) for i in range(1,21)]
dual={cm:quiet(nc._run_all_networks,atoms,contacts,[1],[],{1:'SE'},1.,20.,3.,3.,None,
               contact_mode=cm,temp_c=60.,ea_ion_ev=.3) for cm in ('hertzian','physics')}
dual=json.loads(json.dumps(dual))
ledger=dict(thickness_um=20.,thickness_mass_conserving_um=20.,phi_se_mass_conserving=21*4*math.pi/3/(20*9))
baseline=tf.ion_columns(dual,ledger,100.)
con=tf.network_generation_contract(dual)
check(con['generation']=='g2' and not con['problems'],'fresh_normal',con)
OUT['fresh_normal']={'contract':con,'row':baseline,'record':dual}

# Single-leaf record corruptions: technical rejection may occur before certificate binding.
types=[None,math.nan,math.inf,-math.inf,10**400,True,False,'1',[],{},0.,-1.]
mutants=[]
for mode in ('hertz','physics','hertz_h12'):
    for field in ('sigma_full','sigma_full_mScm','sigma_grain_S_cm','percolating_fraction'):
        for val in types:
            d=copy.deepcopy(dual);rec=tf.mode_record(d,mode);rec[field]=val
            ion=safe(tf.ion_record_problem,rec)
            gen=safe(tf.network_generation_contract,d)
            row=safe(tf.ion_columns,d,ledger,100.)
            result=dict(mode=mode,field=field,value=repr(val),ion=ion,generation=gen,
                        status=row['value'].get('ion_net_status_'+mode) if row['value'] else None,
                        f=row['value'].get('f_ion_'+mode) if row['value'] else None,error=row['error'])
            mutants.append(result)
            check(not ion['error'] and not gen['error'] and not row['error'] and ion['value'] is not None
                  and result['status']=='NOT_COMPUTED' and result['f'] is None,'input_types',result)
OUT['input_types']={'count':len(mutants),'cases':mutants}

# Diagnostic numeric values and published certificates must also fail closed.
diagnostic=[]
for mode in ('hertz','physics','hertz_h12'):
    for branch,qk,dk,sk,rk,ck in tf.CERT_BRANCH_KEYS:
        for field in ([qk,dk] if branch!='full' else []):
            for val in types:
                d=copy.deepcopy(dual);rec=tf.mode_record(d,mode);rec[field]=val
                binding=safe(tf.certificate_binding_problems,mode,rec)
                row=safe(tf.ion_columns,d,ledger,100.)
                item=dict(mode=mode,branch=branch,field=field,value=repr(val),binding=binding,
                          status=row['value'].get('ion_net_status_'+mode) if row['value'] else None,error=row['error'])
                diagnostic.append(item)
                check(not binding['error'] and bool(binding['value']) and not row['error'] and item['status']=='NOT_COMPUTED','diagnostic_values',item)
        for field in ('I_bottom','I_top','delta_V','g_to_q','sigma_bulk_S_cm'):
            for val in types[:10]:
                d=copy.deepcopy(dual);rec=tf.mode_record(d,mode);rec[ck][field]=val
                binding=safe(tf.certificate_binding_problems,mode,rec)
                row=safe(tf.ion_columns,d,ledger,100.)
                item=dict(mode=mode,branch=branch,field=ck+'.'+field,value=repr(val),binding=binding,
                          status=row['value'].get('ion_net_status_'+mode) if row['value'] else None,error=row['error'])
                diagnostic.append(item)
                check(not binding['error'] and bool(binding['value']) and not row['error'] and item['status']=='NOT_COMPUTED','published_certificate_types',item)
OUT['diagnostic_types']={'count':len(diagnostic),'cases':diagnostic}

# Invalid geometry is rejected before empty-input/no-through classification.
geo=[]
for field in ('plate_z','box_x','box_y','scale'):
    for val in types+[1e200,1e-200]:
        n=circuit();n[field]=val;n.update(bottom=set(),top=set(),edges=[])
        solve=safe(quiet,nc.solve_network,n,mode='full')
        cert=n.get('solve_info',{}).get('full',{})
        parsed=safe(nc._geometry_TA,dict((k,n[k]) for k in ('plate_z','box_x','box_y','scale')))
        expected_invalid=bool(parsed['error'] or parsed['value'][2])
        g2q=cert.get('g_to_q')
        expected_invalid=expected_invalid or nc._cert_num(g2q) is None or g2q<=0
        row=dict(field=field,value=repr(val),geometry=parsed,solve=solve,status=cert.get('status'),reason=cert.get('reason'))
        geo.append(row)
        check(not solve['error'] and not parsed['error'] and solve['value']==(None,None)
              and (cert.get('reason')=='invalid_geometry' if expected_invalid else cert.get('status')=='no_input'),'input_hierarchy',row)
OUT['input_hierarchy']={'count':len(geo),'cases':geo}

# Guard diagnostics cannot override the raw certified q in a restored FULL value.
guard=[]
n=circuit(1.);quiet(nc.solve_network,n,mode='full');c0=bound(n['solve_info']['full'],'full');c0.update(status='computed',reason=None)
for field in ('q_withheld','q_guard_max','guard_policy','sum_g'):
    for val in [None,0.,1.5,100.,math.nan,math.inf,True,'fake','DELETE']:
        c=copy.deepcopy(c0)
        if val=='DELETE':c.pop(field,None)
        else:c[field]=val
        got=safe(direct,c,'full','computed',None)
        row=dict(field=field,value=repr(val),result=got);guard.append(row)
        check(got['error'] is None and isinstance(got['value'],str) and 'L214R-R01' in got['value'],'guard_diagnostics',row)
OUT['guard_diagnostics']={'count':len(guard),'cases':guard}

target=ROOT/'evidence/rr_numeric_independent.json'
target.write_text(json.dumps(OUT,ensure_ascii=False,indent=2,allow_nan=True),encoding='utf8')
summary={'path':str(target),'boundary':len(boundary),'geometry_normal':len(normal),'labels':len(labels),
         'input_types':len(mutants),'diagnostic_types':len(diagnostic),'input_hierarchy':len(geo),'guard_diagnostics':len(guard),'failures':OUT['failures']}
print(json.dumps(summary,ensure_ascii=False))
sys.exit(bool(OUT['failures']))

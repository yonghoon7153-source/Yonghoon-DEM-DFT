"""Independent read-only adversarial record checks for L214R.

Starts from actual tiny-network producer records saved by the previous independent
probe, not from implementation-owned test fixtures. No production simulations.
"""
from pathlib import Path
import copy
import hashlib
import json
import math
import os
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
SOURCE = ROOT/'source'
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '1'
os.environ['TMP'] = os.environ['TEMP'] = str(ROOT/'tmp')
sys.path[:0] = [str(SOURCE/'scripts'), str(SOURCE/'webapp'), str(WORK/'lhs_coverage_review_20260930/deps'), str(WORK/'gen2_network_reverify3_20261007/deps')]
import network_conductivity as nc
import tau_flux as tf
import pipeline_service as ps
import lhs_release_build as rb

def safe(fn, *args, **kwargs):
    try:
        return dict(value=fn(*args, **kwargs), error=None)
    except Exception as e:
        return dict(value=None, error=f'{type(e).__name__}: {e}')

prior = json.loads((ROOT/'evidence/numeric_probes.json').read_text(encoding='utf8'))
normal = {m: prior['normal_synthetic_base_comparison'][m]['new'] for m in ('hertzian','physics')}
model = prior['records']['valid_synthetic']['record']
normal_ledger = dict(thickness_um=20., thickness_mass_conserving_um=20., phi_se_mass_conserving=21*4*math.pi/3/180)
model_ledger = dict(normal_ledger, phi_se_mass_conserving=normal_ledger['phi_se_mass_conserving']*9)

def check(dual, ledger=normal_ledger, label='case'):
    folder = ROOT/'tmp'/f'numeric_{label}'
    folder.mkdir(exist_ok=True)
    for name, obj in [('network_conductivity_dual.json',dual),('network_conductivity.json',dual['hertzian']),('network_conductivity_hertzian.json',dual['hertzian']),('network_conductivity_physics.json',dual['physics'])]:
        (folder/name).write_text(json.dumps(obj), encoding='utf8')
    return dict(ion={m:safe(tf.ion_record_problem,rec) for m,rec in dual.items()},
                binding={m:safe(tf.certificate_binding_problems, 'hertz' if m=='hertzian' else m,rec) for m,rec in dual.items()},
                generation=safe(tf.network_generation_contract,dual),
                channels={m:{ch:safe(ps.channel_verdict,rec,ch,'hertz' if m=='hertzian' else m) for ch in ('ionic','electronic','thermal')} for m,rec in dual.items()},
                content=safe(ps.network_content_verdict,str(folder)),record=safe(ps.network_record_verdict,str(folder)),
                tau=safe(tf.ion_columns,dual,ledger,100.))

def main():
    out = {'pin':'60ba39e224aff48a030dccfe750342f3bf9db61f','normal_control':check(normal,label='normal')}
    # Restore a real solver's withheld FULL q, without changing currents, geometry,
    # convergence, attempts, or guard diagnostic fields. Only publication labels
    # and published scalar outputs change. This cannot be emitted by the producer.
    d=copy.deepcopy(normal)
    r=copy.deepcopy(model)
    c=r['solve_certificate_full']
    q=c['q_withheld']
    edits={
        'sigma_full':round(q,8),
        'sigma_full_mScm':round(q*r['sigma_grain_S_cm']*1000,6),
        'sigma_full_status':'computed','sigma_full_reason':None,'ionic_status':'computed','ionic_status_reason':None}
    r.update(edits)
    if isinstance(r.get('channel_policy_status'),dict):
        r['channel_policy_status']['ion']='computed'
    c['status']='computed'
    c['reason']=None
    d['physics']=r
    # Use original matching-geometry hertzian counterpart retained in previous
    # probe's real producer output? Reconstruct it from normal immutable producer
    # through a geometric identity: all certificate geometry entries must match.
    # Instead test one mode only at contract level and mirror original q2 source
    # production with the original producer's own tiny chain (same as old probe).
    atoms={i:{'type':1,'x':0.,'y':0.,'z':float(i-1),'radius':1.} for i in range(1,22)}
    contacts=[{'id1':i,'id2':i+1,'contact_area':.5,'delta':.2} for i in range(1,21)]
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        h=nc._run_all_networks(atoms,contacts,[1],[],{1:'SE'},1.,20.,1.,1.,None,contact_mode='hertzian')
    d['hertzian']=json.loads(json.dumps(h))
    out['restored_withheld_full']={'edits':edits,'certificate_edits':{'status':'computed','reason':None},'q_withheld':q,'record':r,'result':check(d,model_ledger,'restored')}

    # Same counterexample in primary Hertz H0: use box .7 so its actual certified
    # q is over the fixed 1.5 guard. No numerical certificate field is modified.
    with contextlib.redirect_stdout(io.StringIO()):
        hd={cm:nc._run_all_networks(atoms,contacts,[1],[],{1:'SE'},1.,20.,.7,.7,None,contact_mode=cm) for cm in ('hertzian','physics')}
    hd=json.loads(json.dumps(hd))
    hledger=dict(model_ledger,phi_se_mass_conserving=model_ledger['phi_se_mass_conserving']/.49)
    before=check(hd,hledger,'h0_before')
    before_row=before['tau']['value']
    hr=hd['hertzian']; hc=hr['solve_certificate_full']; hq=hc['q_withheld']
    h_edits={'sigma_full':round(hq,8),'sigma_full_mScm':round(hq*hr['sigma_grain_S_cm']*1000,6),
             'sigma_full_status':'computed','sigma_full_reason':None,'ionic_status':'computed','ionic_status_reason':None}
    hr.update(h_edits); hc.update(status='computed',reason=None)
    after=check(hd,hledger,'h0_after')
    after_row=after['tau']['value']
    out['restored_primary_H0']={'q_withheld':hq,'edits':h_edits,'certificate_edits':{'status':'computed','reason':None},
                              'before':before,'after':after,'record':hr,
                              'before_release_hold':safe(rb.v13_primary_model_limit_problems,[{k:tf._cell(v) for k,v in before_row.items()}]),
                              'after_release_hold':safe(rb.v13_primary_model_limit_problems,[{k:tf._cell(v) for k,v in after_row.items()}])}
    edges=[]
    for label in ('q1p5','q1p5_nextdown','q1p5_nextup','q2'):
        sol=next(s for s in prior['solves'] if s['label']==label)
        cert=copy.deepcopy(sol['solve_info'])
        qraw=cert.get('q_withheld') if cert.get('q_withheld') is not None else sol['result'][1]
        original_status=cert['status']
        cert.update(status='computed',reason=None,channel='ionic',role='H0',contact_mode='hertzian',sigma_bulk_S_cm=.003)
        edges.append(dict(label=label,raw_q=qraw,published_q=round(qraw,8),producer_status=original_status,
                          published_check=safe(tf._cert_published_problem,'hertz','full',{'sigma_grain_S_cm':.003},round(qraw,8),round(qraw*.003*1000,6),'computed',cert)))
    out['full_guard_rounding_boundary']=edges
    out['N4_thermal_numeric_mismatch']={}
    for lab,val in [('times10',normal['physics']['thermal_sigma_full_mScm']*10),('nan',math.nan)]:
        d4=copy.deepcopy(normal)
        d4['physics']['thermal_sigma_full_mScm']=val
        out['N4_thermal_numeric_mismatch'][lab]=check(d4,label=f'n4_{lab}')

    # N5: turn the diagnostic CF branch into an honest no-value failure first,
    # then compare None with NaN/infinities/huge integers in its I_bottom slot.
    n5={}
    for lab,v in [('null',None),('nan',math.nan),('posinf',math.inf),('neginf',-math.inf),('bigint',10**400),('bool',True),('string','not-a-number')]:
        nd=copy.deepcopy(normal)
        r=nd['physics']
        r.update(sigma_bulk_net=None,sigma_bulk_net_mScm=None,sigma_bulk_net_status='not_computed',sigma_bulk_net_reason='zero_resistance_requires_contraction')
        cc=r['solve_certificate_bulk_net']
        cc.update(status='not_computed',reason='zero_resistance_requires_contraction',I_bottom=v,I_top=None,attempts=[])
        n5[lab]=check(nd,label=f'n5_{lab}')
    out['N5_unpublished_current']=n5

    # K1 known display getter behavior, K2 known temperature big-int exception.
    out['known_K']={'K1_metrics':safe(tf.tau2_from_metrics,{'phi_se':.3,'sigma_full_mScm':1e-310}),
                    'K1_direct':safe(tf.tau2_value,1e308,3.,1e-3),
                    'K2_temperature':safe(tf.tau2_from_metrics,{'phi_se':.3,'sigma_full_mScm':.1,'temperature_provenance':{'sigma_ion_T_factor':10**400,'T_C':60.,'Ea_ion_eV':.3,'T_ref_C':25.}})}
    archive=SOURCE/'docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz'
    with tarfile.open(archive,'r:gz') as tfp:
        for member in tfp.getmembers():
            if member.isfile() and member.name.endswith('/network_conductivity_dual.json'):
                legacy=json.load(tfp.extractfile(member))
                if all(legacy.get(m,{}).get('sigma_full_status')=='valid_zero' for m in ('hertzian','physics')):
                    case=member.name.rsplit('/',1)[0]
                    fm=json.load(tfp.extractfile(case+'/full_metrics.json'))
                    for m in ('hertzian','physics'): legacy[m]['sigma_grain_S_cm']=1e306
                    out['known_K']['K3_legacy_zero_meta']=dict(source_member=member.name,
                        ion={m:safe(tf.ion_record_problem,legacy[m]) for m in ('hertzian','physics')},
                        row=safe(tf.ion_columns,legacy,fm,fm['percolation_pct']))
                    break
    # Fresh independent type/value sweep of all adoption records across branches.
    mutations=[]
    for mode in ('hertzian','physics'):
        for branch in ('full','bulk_net','constr_net'):
            ck='solve_certificate_'+branch
            for field,vals in {
                'I_bottom':[math.nan,math.inf,10**400,0.,-1.,True,'1'],
                'I_top':[math.nan,math.inf,10**400,0.,1.,True,'-1'],
                'residual_rel':[math.nan,math.inf,10**400,-1.,1.000001e-6,True],
                'conservation_rel':[math.nan,math.inf,10**400,-1.,1.000001e-6,True],
                'krylov_info':[0,1,True,math.nan,10**400],
                'error':['',False,0,'error'],
                'outcome':['exception','not_converged','parallel_bound',None],
                'method':['cg','unknown',None]}.items():
                for v in vals:
                    rec=copy.deepcopy(normal[mode])
                    rec[ck]['attempts'][-1][field]=v
                    got=safe(tf.certificate_binding_problems,'hertz' if mode=='hertzian' else mode,rec)
                    mutations.append(dict(mode=mode,branch=branch,field=field,value=repr(v),result=got))
    out['adopted_attempt_sweep']={'count':len(mutations),'accepted':[x for x in mutations if x['result']['value']==[]],
                                 'exceptions':[x for x in mutations if x['result']['error'] is not None],'all':mutations}

    # Finite extremes in ledger: every value-carrying row must have positive finite
    # f, tau2, tau, independently of its OK/MBCB category.
    sweeps=[]
    vals=[5e-324,1e-310,1e-200,1e-100,1.,1e100,1e200,1e308,10**400,math.nan,math.inf,True]
    for field in normal_ledger:
        for v in vals:
            led=dict(normal_ledger,**{field:v})
            res=safe(tf.ion_columns,normal,led,100.)
            bad=[]
            if res['error'] is None:
                for m in ('hertz','hertz_h12','physics'):
                    row=res['value']
                    if row[f'ion_net_status_{m}'] in ('OK','MODEL_BELOW_CONTINUUM_BOUND'):
                        for col in (f'f_ion_{m}',f'f_ion_{m}_gap',f'tau2_ion_{m}',f'tau_ion_{m}'):
                            if not (isinstance(row[col],(int,float)) and math.isfinite(row[col]) and row[col]>0): bad.append(col)
            sweeps.append(dict(field=field,value=repr(v),bad_values=bad,result=res))
    out['ledger_sweep']={'count':len(sweeps),'failures':[x for x in sweeps if x['result']['error'] or x['bad_values']],'all':sweeps}
    target=ROOT/'evidence/numeric_adversarial.json'
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=True),encoding='utf8')
    print(json.dumps({'path':str(target),'H0_q':hq,'H0_before':before_row['ion_net_status_hertz'],'H0_after':after_row['ion_net_status_hertz'],
                      'H0_after_f':after_row['f_ion_hertz'],'H0_after_flag':after_row['full_model_limit_hertz'],
                      'H0_after_record':after['record'],'H0_after_release_hold':out['restored_primary_H0']['after_release_hold'],
                      'adoption_accepted':out['adopted_attempt_sweep']['accepted'],'adoption_exceptions':out['adopted_attempt_sweep']['exceptions'],'ledger_failures':out['ledger_sweep']['failures'],'known_K':out['known_K']},ensure_ascii=False))

if __name__=='__main__': main()

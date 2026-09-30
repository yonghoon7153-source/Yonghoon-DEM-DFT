#!/usr/bin/env python3
"""Independent read-only review. No DEM, MPI, scheduler or network invocation.
Writes only synthetic fixtures and evidence below this review directory.
"""
from pathlib import Path
import argparse, contextlib, hashlib, io, json, math, os, re, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'source'
SUB = ROOT / 'submitted'
DECKS = SUB / 'docs/data/mixer_highbo_dev_decks_20260930_v26'
sys.path.insert(0, str(SRC / 'scripts'))
OUT = ROOT / 'evidence'
OUT.mkdir(exist_ok=True)
RESULT = {}

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def blob(p):
    b = Path(p).read_bytes()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def deck(p):
    text = Path(p).read_text(encoding='utf-8')
    lines = re.sub(r'&[ \t]*\r?\n', ' ', text)
    lines = [x.split('#', 1)[0].split() for x in lines.splitlines()]
    props = {}
    for tokens in lines:
        if 'property/global' in tokens:
            j = tokens.index('property/global')
            name, shape = tokens[j+1:j+3]
            start = j+3 if shape == 'peratomtype' else j+4
            if name in ('youngsModulus', 'poissonsRatio', 'cohesionEnergyDensity'):
                props[name] = list(map(float, tokens[start:]))
    props['commands'] = lines
    props['text'] = text
    props['sha256'] = digest(p)
    return props

def estar(d, i, j):
    E, nu = d['youngsModulus'], d['poissonsRatio']
    return 1/((1-nu[i]**2)/E[i] + (1-nu[j]**2)/E[j])

def maths():
    pins=json.loads((SRC/'SOURCE_PINS.json').read_text(encoding='utf-8'))
    RESULT['source_pins']=[dict(p,observed_blob=blob(SRC/p['path']),matches=blob(SRC/p['path'])==p['git_blob']) for p in pins]
    assert all(p['matches'] for p in RESULT['source_pins'])
    hashcheck = []
    for line in (DECKS/'SHA256SUMS').read_text().splitlines():
        h, p = line.split(None, 1)
        hashcheck.append({'path':p, 'matches':digest(DECKS/p)==h})
    assert all(x['matches'] for x in hashcheck)
    RESULT['bundle_hashes'] = hashcheck
    maps = {p.parent.name:deck(p) for p in DECKS.rglob('in.mixer')}
    RESULT['deck_count'] = len(maps)
    ratios = {}
    for arm in ('LC','LH'):
        old = maps[f'{arm}_soft_r2_s32452843']
        for name, factor in [('ref',20),('ref2',40)]:
            new = maps[f'{arm}_{name}_r2_s32452843']
            rows = []
            for i in range(4):
                for j in range(i,4):
                    er = estar(new,i,j)/estar(old,i,j)
                    c0,c1 = old['cohesionEnergyDensity'][i*4+j],new['cohesionEnergyDensity'][i*4+j]
                    cr = c1/c0 if c0 else None
                    f0 = cr**3/er**2 if cr is not None else None
                    assert (abs(f0-1)<3e-5 if f0 is not None else c1==0)
                    assert new['cohesionEnergyDensity'][i*4+j]==new['cohesionEnergyDensity'][j*4+i]
                    rows.append(dict(pair=f'{i+1}-{j+1}', estar_ratio=er, ced_ratio_expected=er**(2/3),
                                     ced_soft=c0, ced_new=c1, ced_ratio_printed=cr, f0_ratio=f0))
            ratios[f'{arm}_{factor}'] = rows
    RESULT['pair_ratios'] = ratios
    RESULT['b_changed_pairs'] = {}
    for level in ('soft','ref','ref2'):
        a,b = (maps[f'{arm}_{level}_r2_s32452843']['cohesionEnergyDensity'] for arm in ('LC','LH'))
        changed = [(i+1,j+1) for i in range(4) for j in range(i,4) if a[4*i+j]!=b[4*i+j]]
        assert changed==[(1,1),(1,2),(1,4),(2,2),(2,4)]
        RESULT['b_changed_pairs'][level] = changed
    RESULT['e0_zero'] = {n:all(v==0 for v in d['cohesionEnergyDensity']) for n,d in maps.items() if n.startswith('E0')}
    assert all(RESULT['e0_zero'].values())
    import mixer_deck_diff as dd
    import mixer_deck_readback as rb
    paths={p.parent.name:p for p in DECKS.rglob('in.mixer')}
    RESULT['regenerated_deck_text_matches']={n:dd.cell_expected_deck(n)==p.read_text(encoding='utf-8') for n,p in paths.items()}
    assert all(RESULT['regenerated_deck_text_matches'].values())
    # The submitted report supplies comparison identities, not expected verdicts.
    submitted_tables=json.loads((DECKS/'readback.json').read_text(encoding='utf-8'))['tables']
    rerun=[]
    for table in submitted_tables:
        old,new=table['old'],table['new']
        obj=rb.compare(table['kind'],rb.load(str(paths[old])),rb.load(str(paths[new])))
        rerun.append({'kind':table['kind'],'old':old,'new':new,'verdict':obj['verdict'],'failures':obj['failures']})
    RESULT['readback_tables_rerun']=rerun
    assert len(rerun)==13 and all(x['verdict']=='PASS' for x in rerun)
    soft = maps['LC_soft_r2_s32452843']
    def es(f,i,j):
        obj = dict(soft, youngsModulus=[1.037e9,1.037e9,1e7*f,1.48e9])
        return estar(obj,i,j)
    RESULT['reported_max_forecast_conditional'] = {
        'naive_SESE_1_018':1.018*(14/20)**(2/3),
        'SEwall_1_018':1.018*(es(14,2,3)/es(20,2,3))**(2/3),
        'AMSE_1_014':1.014*(es(14,0,2)/es(20,0,2))**(2/3),
        'runtime_rayleigh_assumption':math.sqrt(20/14),
        'not_observed':True}
    RESULT['variance_claim'] = {'iid_normal_1024_RSE':math.sqrt(2/1023),
                               'two_independent_variances_relative_SD_first_order':math.sqrt(4/1023),
                               'ten_percent_over_difference_SD':.10/math.sqrt(4/1023)}
    RESULT['owner_switch_counterexample'] = {'before':[.715,.701], 'after':[.594,.734],
        'AM_P_SE_growth_pct':100*(.734/.701-1), 'logic':'If every component maximum decreases, max cannot increase; owner switching alone is not sufficient.'}
    # Same S0 and shared SR within each level: shift only normalization.
    s0, slc, slh, sr_a, sr_b = .20,.17,.18,.15,.165
    d_a,d_b = (slh-slc)/(s0-sr_a),(slh-slc)/(s0-sr_b)
    RESULT['sr2_counterexample'] = dict(s0=s0,slc=slc,slh=slh,sr_before=sr_a,sr_after=sr_b,
                                      sr_relative_change=sr_b/sr_a-1,contrast_before=d_a,contrast_after=d_b,shift=d_b-d_a)
    # Source-grounded distribution algebra; no native engine is run.
    d = maps['E0_ref_s32452843']
    weights, masses = [], []
    for ts in d['commands']:
        if 'particletemplate/sphere' in ts:
            rho=float(ts[ts.index('density')+2]); radius=float(ts[ts.index('radius')+2])
            masses.append(rho*radius**3)
        if 'particledistribution/discrete' in ts:
            j=ts.index('particledistribution/discrete'); T=int(ts[j+2])
            weights=[float(ts[j+4+2*i]) for i in range(T)]
    w=[a/b for a,b in zip(weights,masses)]; w=[a/sum(w) for a in w]
    RESULT['mpi_expected_from_printed_deck'] = {'number_fractions':w,'ideal_counts':[100000*a for a in w]}
    # A legal rank allocation: twenty ranks each request 5000; possible outcomes include exact plan.
    nr=[5000]*20
    floor_counts=[math.floor(5000*a) for a in w]
    gap=5000-sum(floor_counts)
    target=[176,859,98965]
    extra=[t-20*b for t,b in zip(target,floor_counts)]
    assert min(extra)>=0 and sum(extra)==20*gap
    RESULT['mpi_NP20_exact_plan_possible']={'local_floor':floor_counts,'local_gap':gap,'aggregate_extra':extra,
        'all_remainders_positive':all(5000*a%1>0 for a in w),'target':target}
    RESULT['mpi_NP1_not_unique']={'floor':[math.floor(100000*a) for a in w],
                                'gap':100000-sum(math.floor(100000*a) for a in w)}
    RESULT['upstream_source_blobs'] = {p.name:blob(p) for p in (SRC/'upstream/src').glob('*.cpp')}

def boundaries():
    import numpy as np
    import check_contact_validity as cv
    import measure_mixing_index as mi
    import mixer_stage_gate as sg
    import mixer_deck_diff as dd
    import mixer_smoke_blind as sb
    txt=(DECKS/'decks/E0_ref_s32452843/in.mixer').read_text(encoding='utf-8')
    RESULT['count_tolerances']={str(n):cv.count_tolerance(txt,n) for n in (1,20,0,True)}
    lc=(DECKS/'decks/LC_ref_r2_s32452843/in.mixer').read_text(encoding='utf-8')
    RESULT['lc_count_tolerance']=cv.count_tolerance(lc,20)
    # New global soft range ignores pair identity, despite AM-AM being unchanged in E.
    w=dict(pp_max=.02,pp_max_types='1-1',pp_max_by_pair={'1-1':.02},wall_max=0.,phase_status='static',
           max_ovl=.01,tech=[],reject=['2% overlap'],reject_overlap=['2% overlap'])
    RESULT['soft_AMAM_2pct']=cv.contract_status(w,7.37)
    assert RESULT['soft_AMAM_2pct']['soft_range']=='WITHIN'
    # Evaluate the real statistics function: one retained cell -> NaN.
    D={k:np.zeros(20) for k in ('x','y','z')}
    D.update(radius=np.full(20,1e-5),type=np.full(20,3))
    cs=mi.cell_stats(D,.013138,cells=16,x_cells=4,n_min=20,axis='x')
    assert math.isnan(cs['s2'])
    RESULT['finite_cloud_undefined_variance']={'used':cs['used'],'s2':None,'is_nan':math.isnan(cs['s2'])}
    # Boundary fixture only: contacts and SR acquisition stubbed; actual producer and verifier execute.
    with tempfile.TemporaryDirectory(prefix='synthetic_gate_',dir=OUT) as td:
        for n in dd.DEV_E0:
            sg._fx_cell(td,n); sg._fx_seal(td,n,'dev-e0'); sg._fx_e0_done(td,n)
            (Path(td)/n/'job_start.json').write_text('{"synthetic_only":true}\n',encoding='utf-8')
        recpath=str(Path(td)/'e0_diag.json')
        variants={'finite_baseline':{},'c_threshold_fail':{'E0_ref_dthalf_s32452843':.011},
                  'undefined_reference':{'E0_ref_s32452843':float('nan')},
                  'undefined_dthalf':{'E0_ref_dthalf_s32452843':float('nan')}}
        got={}
        for label,stats in variants.items():
            rc,rec=sg._fx_e0_record(td,recpath,s2=stats)
            errors=sg.verify_e0_record(td,recpath,20)
            got[label]={'rc':rc,'verdict':rec['verdict'],'checks':rec['checks'],'verify_errors':errors}
        RESULT['e0_diag_real_producer_boundary']=got
        rc,rec=sg._fx_e0_record(td,recpath)
        for k in ('b','c'):
            rec['checks'][k]={'pass':False,'role':'report'}
        Path(recpath).write_text(json.dumps(rec),encoding='utf-8')
        RESULT['report_values_removed_verifier']=sg.verify_e0_record(td,recpath,20)
        assert got['finite_baseline']['verdict']=='PASS' and not got['finite_baseline']['verify_errors']
        assert got['undefined_reference']['verdict']=='PASS' and not got['undefined_reference']['verify_errors']
        assert not RESULT['report_values_removed_verifier']

def selftests():
    results={}
    for name in ('make_mixer_deck','mixer_deck_diff','mixer_deck_readback','check_contact_validity','mixer_smoke_blind','mixer_stage_gate'):
        p=subprocess.run([sys.executable,str(SRC/'scripts'/f'{name}.py'),'--selftest'],cwd=SRC,
                         capture_output=True,text=True,encoding='utf-8',env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1'),timeout=180)
        (OUT/f'{name}_selftest.log').write_text(p.stdout+'\nSTDERR\n'+p.stderr,encoding='utf-8')
        results[name]={'rc':p.returncode,'tail':(p.stdout+p.stderr).splitlines()[-4:]}
    RESULT['selftests']=results

def lf_selftests():
    results={}
    for name in ('mixer_deck_diff','mixer_stage_gate','mixer_smoke_blind'):
        p=subprocess.run([sys.executable,str(ROOT/'selftest_lf.py'),str(SRC/'scripts'/f'{name}.py')],cwd=SRC,
                         capture_output=True,text=True,encoding='utf-8',timeout=180)
        (OUT/f'{name}_selftest_lf.log').write_text(p.stdout+'\nSTDERR\n'+p.stderr,encoding='utf-8')
        results[name]={'rc':p.returncode,'tail':(p.stdout+p.stderr).splitlines()[-2:]}
    RESULT['selftests_Linux_newline_emulation']=results

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--selftests',action='store_true');ap.add_argument('--lf-selftests',action='store_true');a=ap.parse_args()
    maths();boundaries()
    if a.selftests:selftests()
    elif (OUT/'audit_results.json').is_file():
        old=json.loads((OUT/'audit_results.json').read_text(encoding='utf-8'))
        RESULT['selftests']=old.get('selftests',{})
    if a.lf_selftests:lf_selftests()
    (OUT/'audit_results.json').write_text(json.dumps(RESULT,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({k:RESULT[k] for k in ('deck_count','reported_max_forecast_conditional','mpi_NP20_exact_plan_possible','selftests_Linux_newline_emulation') if k in RESULT},ensure_ascii=False,indent=2))

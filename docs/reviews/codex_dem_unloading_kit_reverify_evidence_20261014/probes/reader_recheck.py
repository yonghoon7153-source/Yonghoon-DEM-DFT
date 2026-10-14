"""Read-only source audit through actual reader/observer functions; no DEM.

Production fixture serializers only write disposable evidence, never source.
Expectations/mutations here are independently chosen. Source functions, result
repr, complete verdicts and retained fixture roots are recorded for inspection.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy
import csv
import hashlib
import inspect
import json
import math
import sys
import tempfile

R = Path(__file__).resolve().parents[1]
K = R / 'source/docs/data/ps45_unload_20261009'
sys.path.insert(0, str(K))
import ul_reader as u
import ul_observers as o

P = u.ul_lib.load_params()
B = u.B73
E = R / 'evidence/reader_cases' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
E.mkdir(parents=True)
(E/'tmp').mkdir()
tempfile.tempdir=str(E/'tmp')
RESULT = {'fixture_root': str(E), 'source': {}, 'cases': {}}
for name in ('ul_reader.py', 'ul_observers.py', 'ul_s3.py', 'ul_lib.py'):
    RESULT['source'][name] = hashlib.sha256((K / name).read_bytes()).hexdigest()
RESULT['functions'] = {name: {'file': Path(inspect.getsourcefile(fn)).name, 'line': inspect.getsourcelines(fn)[1], 'signature': str(inspect.signature(fn))}
                       for name, fn in [('arm_verdict', u.arm_verdict), ('report', u.report), ('gate', u.gate),
                                        ('separation', u.separation), ('_s3_at', u._s3_at), ('kebase', u.kebase),
                                        ('_continuation', u._continuation), ('eps_sphere', o.eps_sphere)]}


def write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def base_steps(lifts=None, pressures=None):
    lifts = [.2, .25, .3, .35] if lifts is None else lifts
    pressures = [1.2, .8, .6, .4] if pressures is None else pressures
    st = u._ladder(lifts, pressures)
    for i, row in enumerate(st[1:], 1):
        row['kind'] = 'A' if i == 1 else 'B'
        row.pop('n_move', None)
    return st


def make(case, job='UB', steps=None, events=None, summary='TIMEOUT', full=True):
    root = E / case
    half = job in ('UT', 'UVb')
    spec = {'W': 10000 if half else 5000, 'dt': 5e-7 if half else 1e-6,
            'steps': copy.deepcopy(steps if steps is not None else base_steps()), 'full_frames': full,
            'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')] if events is None else events,
            'summary': summary}
    d = Path(u._mk_arm(str(root), B, job, spec, P))
    return root, d, spec


def av(root, d, job='UB'):
    try:
        return u.arm_verdict(str(d), B, job, P, root=str(root))
    except Exception as ex:
        return {'primary_status':'__EXCEPTION__','exception':repr(ex),'function':'arm_verdict'}


def save(name, actual, expected, passed, functions='arm_verdict'):
    RESULT['cases'][name] = {'functions': functions, 'expected': expected, 'pass': bool(passed),
                             'actual_repr': repr(actual), 'actual': actual}


def csv_mutate(path, mutate):
    with path.open(encoding='utf-8', newline='') as f:
        rd = csv.DictReader(f)
        cols, rows = list(rd.fieldnames), list(rd)
    mutate(rows)
    with path.open('w', encoding='utf-8', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        wr.writeheader()
        wr.writerows(rows)


def atom_edit(path, mutate):
    lines = path.read_text(encoding='utf-8').splitlines()
    idx = next(i for i, x in enumerate(lines) if x.startswith('ITEM: ATOMS'))
    cols = lines[idx].split()[2:]
    rows = [dict(zip(cols, ln.split())) for ln in lines[idx+1:]]
    mutate(rows)
    write(path, '\n'.join(lines[:idx+1] + [' '.join(row[c] for c in cols) for row in rows]) + '\n')


# Independent positive control is retained before every one-field mutation.
root, d, spec = make('positive')
v = av(root, d)
rho = .2026077873428664
save('positive_timeout', v, 'Valid measurement survives auxiliary TIMEOUT',
     v['primary_status'] == 'OK' and abs(v['rho_pct']-rho) < 1e-12 and v['trajectory_status'] == 'TIMEOUT')

for mut in ('unsteady', 'nan', 's3', 'wrong_kind', 'wrong_phase', 'missing', 'no_wall_contact'):
    st = base_steps()
    if mut == 'unsteady':
        for row in st[3:]: row.update(steady=False, nw=12)
    elif mut == 'nan':
        for row in st[3:]: row['Pbar'] = 'nan'
    elif mut == 's3': st[4]['s3'] = 'bad'
    elif mut == 'wrong_kind': st[3]['kind'] = 'A'
    elif mut == 'wrong_phase': st[4]['phase'] = 2
    elif mut == 'no_wall_contact':
        for row in st[3:]: row['wall'] = [[]]*row['nw']
    root, d, spec = make('confirmation_'+mut, 'UT', st, summary='RM_STOP')
    if mut == 'missing': csv_mutate(d/'ul_steps.csv', lambda rows: rows.pop(3))
    make('confirmation_'+mut, 'UB')
    u._fake_restored(str(root), B)
    write(root/B/'ul_base.in', 'variable ul_S2max equal 1e-05\n')
    v = av(root, d, 'UT')
    sel, gate = u.selection_state(str(root), P), u.gate(str(root), B, 'UVa', P)
    valid = mut == 'no_wall_contact'
    save('confirmation_'+mut, {'verdict':v, 'selection':sel, 'UVa_gate':gate},
         'OK and next UVa permitted' if valid else 'UNIDENTIFIED, no UVa submission',
         v['primary_status'] == ('OK' if valid else 'UNIDENTIFIED') and bool(gate[0]) == valid,
         'arm_verdict -> selection_state -> gate')

for tag, lifts, ps, ev, expected in (
    ('first_A', [.2,.25,.3], [.8,.6,.4], [('CROSS',1,'first'),('RM',3,'ncross2')], [0,.2]),
    ('first_B', [.2,.25,.3,.35], [1.2,.8,.6,.4], None, [.2,.25]),
    ('multiple', [.2,.25,.3,.35,.4,.45,.5], [.8,.6,.4,1.2,.7,1.3,.5], [('CROSS',1,'first'),('RM',3,'ncross2')], [0,.5]),
    ('old_false_separation', [.2,.25,.3,.35,.4], [.8,.6,.4,1.2,.7], [('CROSS',1,'first'),('RM',3,'ncross2')], [0,.4]),
):
    root,d,_ = make('union_'+tag, steps=base_steps(lifts,ps),events=ev)
    v=av(root,d)
    ok=v['primary_status']=='OK' and all(abs(a-b)<1e-12 for a,b in zip(v['union_bracket_um'],expected))
    actual={'verdict':v}
    if tag=='old_false_separation':
        other=u.BEDS[0]
        od=u._mk_arm(str(root),other,'UB',dict(spec,steps=base_steps(),W=5000,dt=1e-6,events=[('CROSS',2,'first'),('RM',4,'ncross2')]),P)
        ov=u.arm_verdict(od,other,'UB',P,root=str(root))
        pair=next(x for x in u.pair_table({other:ov,B:v}) if x['a']==other and x['b']==B)
        actual.update(other_verdict=ov,pair=pair)
        ok=ok and pair['relation']=='OVERLAP'
    save('union_'+tag,actual,'Complete outer union '+repr(expected)+'; includes first bracket',ok,'arm_verdict -> pair_table')
st=base_steps([.2,.25,.3,.35,.4,.45],[1.2,.8,.6,.4,.3,.2]);st[5]['Pbar']='nan'
root,d,_=make('union_nonfinite',steps=st);v=av(root,d)
save('union_nonfinite',v,'Keep primary OK, outer union NOT_COMPUTED',v['primary_status']=='OK' and v['union_bracket_um'] is None)

for mut in ('nan_atom','bad_finite_force','wrong_wall_step','wrong_atom_contact_step','duplicate_atom_id','fractional_atom_id','missing_column','malformed_csv','missing_k'):
    root,d,_=make('parsing_'+mut)
    run=u.read_run(str(d),P);end=run['steps'][2]['step'];ap=d/'dump'/f'atom_{end}.dump'
    if mut=='nan_atom': atom_edit(ap,lambda rows: rows[0].update(fz='nan'))
    elif mut=='bad_finite_force': atom_edit(ap,lambda rows: rows[0].update(fz='0.001'))
    elif mut=='wrong_wall_step': u._restep(str(d/'dump'/f'wall_{end}.dump'),end-100000)
    elif mut=='wrong_atom_contact_step':
        u._restep(str(ap),end-100000);u._restep(str(d/'dump'/f'contact_{end}.dump'),end-100000)
    elif mut=='duplicate_atom_id': atom_edit(ap,lambda rows: rows[1].update(id=rows[0]['id']))
    elif mut=='fractional_atom_id': atom_edit(ap,lambda rows: rows[1].update(id='2.5'))
    elif mut=='missing_column': write(ap,ap.read_text().replace('ITEM: ATOMS id ','ITEM: ATOMS not_id '))
    elif mut=='malformed_csv':
        rows=(d/'ul_steps.csv').read_text().splitlines();rows[4]+=',extra';write(d/'ul_steps.csv','\n'.join(rows)+'\n')
    elif mut=='missing_k': csv_mutate(d/'ul_steps.csv',lambda rows:rows.pop(3))
    v=av(root,d)
    save('parsing_'+mut,v,'UNIDENTIFIED, no salvaging broken observations',v['primary_status']=='UNIDENTIFIED')

# Adjacent record-integrity probe: a duplicate is not a technical resume.
root,d,_=make('duplicate_without_resume','UT',summary='RM_STOP')
make('duplicate_without_resume','UB')
u._fake_restored(str(root),B)
write(root/B/'ul_base.in','variable ul_S2max equal 1e-05\n')
csv_mutate(d/'ul_steps.csv',lambda rows: rows.insert(3,dict(rows[3],steady='0')))
v=av(root,d,'UT');sel=u.selection_state(str(root),P);gt=u.gate(str(root),B,'UVa',P)
save('duplicate_without_resume',{'verdict':v,'selection':sel,'UVa_gate':gt,'resume_events':u.read_run(str(d),P)['resume_steps']},
     'UNIDENTIFIED unless an authorized RESUME explicitly supersedes the record',v['primary_status']=='UNIDENTIFIED' and not gt[0],'arm_verdict -> selection_state -> gate')

def sep_case(tag,walls,nw,ev=None,prev_zero=False,phase=2):
    st=base_steps()
    if prev_zero:st[-1]['wall']=['default']*3+[[]]
    st.append({'lift_um':.4,'P':0.,'steady':True,'nw':nw,'kind':'B','phase':phase,'modeB':1,'wall':walls})
    ev=[('CROSS',2,'first'),('RM',4,'ncross2')]+([('SEPARATED',5,'w2'),('POST_DONE',5,'w5')] if ev is None else ev)
    root,d,_=make('separation_'+tag,steps=st,events=ev,summary='DONE')
    return root,d,av(root,d)

for tag,walls,nw,ev,prev_zero,expected in (
    ('positive',[[]]*5,5,None,False,'DONE'),
    ('recontact',[[],[],[],[],[-1.]],5,None,False,'SEP_INCOMPLETE'),
    ('missing',[[],[],[],[],'missing'],5,None,False,'SEP_INCOMPLETE'),
    ('wrong_event',[[]]*5,5,[('SEPARATED',5,'w3'),('POST_DONE',5,'w5')],False,'SEP_INCOMPLETE'),
    ('no_events',[[]]*5,5,[],False,'SEP_INCOMPLETE'),
    ('move_reset',[[]]*5,5,None,True,'DONE'),
    ('late_declare',[[-1.]]*11+[[]]*5,16,[('SEPARATED',5,'w13'),('POST_DONE',5,'w16')],False,'SEP_INCOMPLETE'),
    ('last_budget_declare',[[-1.]]*10+[[]]*5,15,[('SEPARATED',5,'w12'),('POST_DONE',5,'w15')],False,'DONE'),
    ('resep_same_step',[[],[],[-1.]]+[[]]*5,8,[('SEPARATED',5,'w2'),('SEPARATED',5,'w5'),('POST_DONE',5,'w8')],False,'DONE'),
):
    root,d,v=sep_case(tag,walls,nw,ev,prev_zero)
    save('separation_'+tag,v,'Primary OK, trajectory '+expected,v['primary_status']=='OK' and v['trajectory_status']==expected)
st=[{'state':'ZERO','step':x,'k':3,'phase':1} for x in (1,2,3)]
sp=u.separation(st)
save('separation_confirm_only',sp,'No declaration in CONFIRM',sp['declared_index'] is None,'separation')
root,d,_=sep_case('missing_csv_window',[[]]*6,6,[('SEPARATED',5,'w2'),('POST_DONE',5,'w6')])
csv_mutate(d/'ul_windows.csv',lambda rows:rows.__setitem__(slice(None),[r for r in rows if not (r['k']=='5' and r['w']=='3')]))
v=av(root,d)
save('separation_missing_csv_window',{'verdict':v,'remaining_windows':[w for w in u.read_run(str(d),P)['windows'] if w['k']==5]},
     'Missing required post-separation window -> SEP_INCOMPLETE',v['trajectory_status']=='SEP_INCOMPLETE')

def continuation_case(tag,layout='hash'):
    case='continuation_'+tag
    root,_,_=make(case)
    uts=base_steps([.2,.4,.45,.5,.55],[5.,1.2,.8,.6,.4])
    uts[2]['kind']='A'
    ev=[('CROSS',3,'first'),('RM',5,'ncross2')]
    _,ut,spec=make(case,'UT',uts,ev,'RM_STOP')
    make(case,'UVb',uts,ev)
    cs=[{'lift_um':.60,'P':0.,'steady':True,'nw':5,'kind':'B','phase':2,'modeB':1,'wall':[[]]*5,'surface':[120.]*5}]
    d=Path(u._mk_utc(str(root),B,spec,cs,P,events=[('SEPARATED',6,'w2'),('POST_DONE',6,'w5')],layout=layout))
    return root,ut,d

for tag in ('positive','parent_screen_tamper','parent_atom_tamper','manifest_digest','copy','gap','missing_resume','missing_first_window'):
    root,ut,d=continuation_case(tag,tag if tag in ('copy','gap') else 'hash')
    if tag=='parent_screen_tamper': write(ut/'screen.txt',(ut/'screen.txt').read_text()+'# changed\n')
    elif tag=='parent_atom_tamper':
        stp=u.read_run(str(ut),P)['steps'][3]['step'];p=ut/'dump'/f'atom_{stp}.dump';write(p,p.read_text()+'\n')
    elif tag=='manifest_digest':
        p=d/'parent_UT.sha256';write(p,p.read_text()+'\n')
    elif tag=='missing_resume': csv_mutate(d/'ul_events.csv',lambda rows:rows.__setitem__(slice(None),[x for x in rows if x['event']!='RESUME']))
    elif tag=='missing_first_window': csv_mutate(d/'ul_windows.csv',lambda rows:rows.pop(0))
    vv=av(root,d,'UTc');rep=u.report(str(root),P);e=rep['beds'][B]
    good=tag=='positive'
    ok=rep['selection']['tuple']=='t3' and e['primary_status']=='OK' and abs(e['rho_pct']-.3827035983143033)<1e-12
    ok=ok and vv['continuation']['status']==('OK' if good else 'FAIL') and e['trajectory_status']==('DONE' if good else 'SEP_INCOMPLETE')
    save('continuation_'+tag,{'UTc':vv,'report':rep},'UT primary retained; '+('valid DONE auxiliary' if good else 'continuation rejected, auxiliary incomplete'),ok,'arm_verdict -> report')

# Valid native UK shape (independently built, all expected execution metadata).
def make_uk(tag,mut=None):
    root=E/('uk_'+tag);d=root/B/'RJ/UK';s0=P['beds'][B]['s0'];h0=P['beds'][B]['h0'];W=P['windows']['W0']
    cols=P['records']['windows_cols'];rows=[]
    for w,rot in [(1,3e-8),(2,1e-8),(3,2e-8)]:
        row={c:'0' for c in cols};row.update(arm='UK',bed=B,k='0',w=str(w),phase='4',step=str(s0+w*W),plate_z=str(h0),lift='0',ke_rot_avg=str(rot));rows.append(row)
    if mut=='one':rows=rows[:1];rows[0].update(step='1',ke_rot_avg='0.001')
    elif mut=='two':rows.pop()
    elif mut=='duplicate':rows[2]=dict(rows[1])
    elif mut=='gap':rows[2]['step']=str(s0+4*W)
    elif mut=='move':rows[1]['lift']='0.0001';rows[1]['plate_z']=str(h0+.0001)
    elif mut=='nan':rows[1]['ke_rot_avg']='nan'
    text=','.join(cols)+'\n'+'\n'.join(','.join(r[c] for c in cols) for r in rows)+'\n';write(d/'ul_windows.csv',text)
    start=s0+1 if mut=='wrong_start' else s0
    write(d/'ul_events.csv',','.join(P['records']['events_cols'])+f'\nSTART,0,{start},{h0},0,s0\nNOMOVE_DONE,0,{s0+3*W},{h0},0,w3\n')
    write(d/'ul_summary.txt',f'result=DONE\narm=UK\nbed={B}\n')
    write(d/'screen.txt',f'LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)\nLoop time of 1 on 6 procs for {3*W} steps with 160417 atoms\nUL_SUMMARY arm=UK bed={B} result=DONE step={s0+3*W} k=0\n'+('ERROR: test\n' if mut=='tech' else ''))
    write(d/'run_check.txt','UK screen.txt '+('FAIL rc=1\n' if mut=='tech' else 'PASS rc=0 procs=6\n'))
    return root,d

for mut in (None,'one','two','duplicate','gap','move','nan','wrong_start','tech'):
    root,d=make_uk(mut or 'positive',mut);v=u.kebase(str(root),B,P,write=True);exists=(root/B/'ul_base.in').exists()
    ok=(abs(v['s2_limit']-2.24e-6)<1e-18 and exists) if mut is None else v['s2_limit'] is None and not exists
    save('uk_'+(mut or 'positive'),{'result':v,'base_file_exists':exists},'S2=2.24e-6' if mut is None else 'No S2 baseline file',ok,'kebase')

# The actual S3 reader receives actual-arm gravity, using free-fall data.
root,d,_=make('gravity')
stp=u.read_run(str(d),P)['steps'][2]['step'];pz=u.read_run(str(d),P)['steps'][2]['plate_z']
atoms=[dict(a,fz=-a['mass']*P['g_aux']) for a in u._chain_atoms([1,2,3,4,5],pz)]
u.ul_lib.write_custom(str(d/'dump'/f'atom_{stp}.dump'),stp,u.ATOM_COLS,atoms)
u.ul_lib.write_local(str(d/'dump'/f'contact_{stp}.dump'),stp,u.CPL_COLS,[])
vals={j:u._s3_at(str(d),stp,pz,{1,2,3,4,5},u._arm_g(j,P)) for j in ('UB','UTc','G_UB','G_UVa','G_UVb','G_UT3')}
save('gravity_actual_arm',vals,'Ordinary R=1e-6 PASS; all G_* R=1 FAIL',
     vals['UB']['status']=='PASS' and all(vals[j]['status']=='FAIL' for j in vals if j.startswith('G_')),'_arm_g -> _s3_at')

# Auxiliary report path with full S0 frames; expected formula calculated here.
root,d,_=make('aux_positive')
make('aux_positive','UT',summary='RM_STOP');make('aux_positive','UVa')
v=av(root,d);rep=u.report(str(root),P)
C=105*4*math.pi*.0005**3/3/.0025;h0=P['beds'][B]['h0'];hM=h0+.225/1000
expected_w=.5*(.16+.0012)*1e6*.0025*.0002*1e-6+.5*(.0012+.001)*1e6*.0025*.000025*1e-6
save('aux_full_report',{'verdict':v,'report':rep,'expected_C':C,'expected_W_J':expected_w},
     'Full S0 epsilon sealed; W from S0 to M, same final report',abs(v['eps']['C_all_m']-C)<1e-16 and abs(v['w_proxy_J']-expected_w)<1e-18 and rep['beds'][B]['eps']==v['eps'] and rep['beds'][B]['w_proxy_J']==v['w_proxy_J'],'arm_verdict -> report')
for mut in ('lost_id','radius_changed','pre_cross_unsteady'):
    st=base_steps()
    if mut=='pre_cross_unsteady':st=base_steps([.1,.2,.25,.3,.35],[3.,1.2,.8,.6,.4]);st[1]['steady']=False
    root,d,_=make('aux_'+mut,steps=st)
    if mut!='pre_cross_unsteady':
        stp=u.read_run(str(d),P)['steps'][2]['step'];p=d/'dump'/f'atom_{stp}.dump'
        if mut=='lost_id':
            atom_edit(p,lambda rows:rows.pop());u._patch_count(str(p),104)
        else:atom_edit(p,lambda rows:rows[-1].update(radius='0.0006'))
    v=av(root,d)
    ok=v['primary_status']=='OK'
    if mut=='pre_cross_unsteady':ok=ok and v['w_proxy_J'] is None
    else:ok=ok and v['eps']['endpoints'][1]['status']=='NOT_COMPUTED' and abs(v['eps']['C_all_m']-C)<1e-16
    save('aux_'+mut,v,'Primary retained; affected auxiliary NOT_COMPUTED with fixed C_all',ok)

RESULT['summary']={'n_cases':len(RESULT['cases']),'n_pass':sum(c['pass'] for c in RESULT['cases'].values()),
                   'failed_expectations':[n for n,c in RESULT['cases'].items() if not c['pass']]}
dest=R/'evidence/reader_recheck.json';write(dest,json.dumps(RESULT,ensure_ascii=False,indent=2))
print(json.dumps(RESULT['summary'],ensure_ascii=False,indent=2))
print('evidence='+str(dest))

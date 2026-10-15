"""Independent file -> real reader/selection/gate checks. Synthetic data, no DEM.

Uses submitted fixture serializers for valid atoms, contacts and thermo only;
resume layouts and adversarial expectations are chosen here independently.
All retained writes stay in evidence/resume_cases_<timestamp>.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy
import csv
import hashlib
import json
import shutil
import sys
import tempfile

R = Path(__file__).resolve().parents[1]
K = R / 'source/docs/data/ps45_unload_20261009'
sys.path.insert(0, str(K))
import ul_reader as u
import make_unload_decks as mk

P = u.ul_lib.load_params()
B = u.B73
E = R / ('evidence/resume_cases_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ'))
E.mkdir(parents=True)
(E / 'tmp').mkdir()
tempfile.tempdir = str(E / 'tmp')
OUT = {'source_pin': 'eaecfba2a2dfbff6f13222f6afeb01d8ebeb5a84', 'fixture_root': str(E),
       'source_sha256': {n: hashlib.sha256((K/n).read_bytes()).hexdigest() for n in ('ul_reader.py', 'run_unload.sh', 'make_unload_decks.py')},
       'cases': {}}


def write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def table(path):
    with Path(path).open(encoding='utf-8', newline='') as f:
        rd = csv.DictReader(f)
        return list(rd.fieldnames), list(rd)


def put(path, cols, rows):
    with Path(path).open('w', encoding='utf-8', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        wr.writeheader()
        wr.writerows(rows)


def edit(path, fn):
    cols, rows = table(path)
    fn(rows)
    put(path, cols, rows)


def steps(lifts=None):
    out=u._ladder([.2,.25,.3,.35] if lifts is None else lifts, [1.2,.8,.6,.4])
    for i,r in enumerate(out[1:],1):
        r['kind']='A' if i==1 else 'B'
        r.pop('n_move',None)  # Serializer computes actual A/B move duration.
    return out


def make(case, job='UT', st=None, summary='RM_STOP', ev=None, deck=True, W=None):
    root = E / case
    half = job in ('UT', 'UVb', 'UT3', 'UTc')
    W = W or (10000 if half else 5000)
    kind = {'UB':'U_UB','UVa':'U_UVa','UVb':'U_UVb','UT3':'U_UT3'}.get(job,job)
    spec = {'W': W, 'dt': 5e-7 if half else 1e-6, 'steps': copy.deepcopy(st or steps()),
            'summary': summary, 'events': ev or [('CROSS',2,'first'),('RM',4,'ncross2')], 'full_frames': True}
    if deck:
        spec['deck'] = mk.render(B, kind, P)
    d = Path(u._mk_arm(str(root), B, job, spec, P))
    return root, d, spec


def chain(root, d, job='UT'):
    v = u.arm_verdict(str(d), B, job, P, root=str(root))
    raw = u.read_run(str(d), P)
    s = u.selection_state(str(root), P)
    g = u.gate(str(root), B, 'UVa', P)
    return {'verdict': v, 'read_run': {n:raw[n] for n in ('problems','n_superseded_rows','resume_steps','resume_auth')},
            'selection': s, 'UVa_gate': g}


def full(case):
    make(case, 'UB', summary='TIMEOUT')
    root,d,sp = make(case)
    u._fake_restored(str(root), B)
    write(root/B/'ul_base.in', 'variable ul_S2max equal 1e-05\n')
    return root,d,sp


def save(name, actual, expect, passed):
    OUT['cases'][name] = {'expected':expect, 'pass':bool(passed), 'actual':actual}


def is_ok(a):
    return a['verdict']['primary_status']=='OK' and abs(a['verdict']['rho_pct']-.2026077873428664)<1e-12 and a['UVa_gate'][0]


def is_bad(a):
    return a['verdict']['primary_status']=='UNIDENTIFIED' and a['verdict']['rho_pct'] is None and not a['UVa_gate'][0]


def resume(d, mode='both', kr=1, repeat=1, duplicated_event=False):
    """Actual serializer ordering: all stale k+1 windows precede stale step.
    One manifest resume_from only; repeat>1 models unauthorized extra rewinds.
    """
    tabs = {n:table(d/f'ul_{n}.csv') for n in ('windows','steps','events')}
    rowk = next(r for r in tabs['steps'][1] if int(r['k'])==kr)
    sr = int(rowk['step'])
    for n in ('windows','steps'):
        cols, rows = tabs[n]
        prefix = [r for r in rows if int(r['step'])<=sr]
        suffix = [r for r in rows if int(r['step'])>sr]
        stale = [dict(r) for r in suffix if int(r['k'])==kr+1]
        if mode=='clean': stale=[]
        if mode=='windows_only' and n=='steps': stale=[]
        if mode=='windows_only' and n=='windows': stale=stale[:2]
        for r in stale:
            r['Ps_avg' if n=='windows' else 'Pbar']='9.999'
        put(d/f'ul_{n}.csv', cols, prefix + stale*repeat + suffix)
    cols, rows = tabs['events']
    prefix = [r for r in rows if int(r['step'])<=sr]
    suffix = [r for r in rows if int(r['step'])>sr]
    res = dict(zip(cols,['RESUME',str(kr),str(sr),rowk['plate_z'],rowk['lift'],'state']))
    stale = [dict(suffix[0])] if suffix and mode!='clean' else []
    seq=[]
    for _ in range(repeat): seq += stale+[dict(res)]
    if duplicated_event: seq.insert(1,dict(res))
    put(d/'ul_events.csv',cols,prefix+seq+suffix)
    write(d/'restart'/f'restart_unload_{sr}.bin','SYNTHETIC CHECKPOINT PLACEHOLDER\n')
    write(d/'restart'/f'state_unload_{sr}.in',f'variable ul_rstep equal {sr}\nvariable ul_k equal {kr}\nvariable ul_phase equal 0\nvariable ul_modeB equal 1\n'
          f'variable ul_pz equal {rowk["plate_z"]}\nvariable ul_lift equal {rowk["lift"]}\nvariable ul_ncross equal 0\nvariable ul_xk equal -1\n'
          f'variable ul_lk0 equal 0\nvariable ul_Pbar equal {rowk["Pbar"]}\nvariable ul_kind string {rowk["kind"]}\n')
    write(d/'run_manifest.txt',f'bed={B}\njob=UT\nresume=0\ngate=ALLOW\nstart=a1\nstage=UT screen=screen.txt rc=1 check=FAIL\nend=a1 fails=1 reader_rc=0\n'
          f'bed={B}\njob=UT\nresume=1\ngate=RESUME\nstart=a2\nresume_from={sr}\nstage=UT screen=screen_a2.txt rc=0 check=PASS\nend=a2 fails=0 reader_rc=0\n')
    return sr


for mode in ('fresh','clean','windows_only','both'):
    root,d,sp=full('positive_'+mode)
    if mode!='fresh': resume(d,mode)
    a=chain(root,d)
    save('positive_'+mode,a,'Normal file layout keeps primary and permits UVa',is_ok(a))

for mutation in ('no_resume_duplicate_step','no_resume_duplicate_window','missing_manifest','missing_event','wrong_event_k','wrong_state_k','wrong_state_step','missing_state','missing_retained_checkpoint','wrong_first_new_k','stale_k_at_boundary'):
    root,d,sp=full(mutation)
    if mutation.startswith('no_resume'):
        name='steps' if mutation.endswith('step') else 'windows'
        edit(d/f'ul_{name}.csv', lambda rows: rows.insert(3,dict(rows[3],**({'steady':'0'} if name=='steps' else {'Ps_avg':'9.999'}))))
    else:
        sr=resume(d)
        if mutation=='missing_manifest': write(d/'run_manifest.txt',(d/'run_manifest.txt').read_text().replace(f'resume_from={sr}\n',''))
        if mutation=='missing_event': edit(d/'ul_events.csv',lambda rows: rows.__setitem__(slice(None),[r for r in rows if r['event']!='RESUME']))
        if mutation=='wrong_event_k': edit(d/'ul_events.csv',lambda rows: next(r for r in rows if r['event']=='RESUME').update(k='0'))
        if mutation=='wrong_state_k': write(d/'restart'/f'state_unload_{sr}.in',f'variable ul_rstep equal {sr}\nvariable ul_k equal 0\n')
        if mutation=='wrong_state_step': write(d/'restart'/f'state_unload_{sr}.in',f'variable ul_rstep equal {sr+1}\nvariable ul_k equal 1\n')
        if mutation=='missing_state': (d/'restart'/f'state_unload_{sr}.in').unlink()
        if mutation=='missing_retained_checkpoint': edit(d/'ul_steps.csv',lambda rows: rows.__setitem__(slice(None),[r for r in rows if int(r['step'])!=sr]))
        if mutation=='wrong_first_new_k':
            def change(rows):
                found=[i for i,r in enumerate(rows) if r['k']=='2']
                rows[found[-1]]['k']='3'
            edit(d/'ul_steps.csv',change)
        if mutation=='stale_k_at_boundary':
            def change(rows):
                next(r for r in rows if r['k']=='2')['k']='1'
            edit(d/'ul_steps.csv',change)
    a=chain(root,d)
    save(mutation,a,'Invalid record cannot authorize primary/UVa',is_bad(a))

for mutation in ('one_event_two_rollbacks','one_auth_two_rollbacks','duplicate_event_only','fractional_resume_event_k','fractional_confirmation_k'):
    root,d,sp=full(mutation)
    if mutation in ('one_event_two_rollbacks','one_auth_two_rollbacks'):
        resume(d,repeat=2)
        if mutation=='one_event_two_rollbacks':
            def delete_second_event(rows):
                inds=[i for i,r in enumerate(rows) if r['event']=='RESUME']
                rows.pop(inds[-1])
            edit(d/'ul_events.csv',delete_second_event)
    elif mutation=='duplicate_event_only': resume(d,duplicated_event=True)
    elif mutation=='fractional_resume_event_k':
        resume(d)
        edit(d/'ul_events.csv',lambda rows: next(r for r in rows if r['event']=='RESUME').update(k='1.4'))
    elif mutation=='fractional_confirmation_k':
        edit(d/'ul_steps.csv',lambda rows: next(r for r in rows if r['k']=='3').update(k='3.4'))
    a=chain(root,d)
    save(mutation,a,'Malformed/extra resume boundary must not silently normalize records',is_bad(a))

# Coherent alternate completed holds: an interrupted old attempt can have fully
# written its k+1 CSV before its new checkpoint/state is written. On retry the
# restored trajectory may complete that hold in a different number of windows.
# These are synthetic record-layout controls, not evidence of actual DEM drift.
def production_trace(nw):
    def obs(k,w,phase,step):
        pd={None:.16,0:.16,1:.0012,2:.0008,3:.0006,4:.0004}.get(k,.0002)
        if k==2 and w<=nw-3:
            pd+=(nw-2-w)*.0001
        return {'P':pd,'Kt':1e-7,'Kr':1e-8,'Kti':1e-7,'nc':1,'na':160417,'lk':11}
    return mk.deck_sim(mk.render(B,'UT',P),obs,P['beds'][B]['s0'],cli={'ul_resume':'0'})


def put_trace(d,trace):
    for n in ('windows','steps','events'):
        cols=P['records'][n+'_cols']
        put(d/f'ul_{n}.csv',cols,[dict(zip(cols,row)) for row in trace[n]])


for nw in (4,5):
    name=f'resume_completed_hold_{nw}_windows'
    oldroot,oldd,oldsp=full(name+'_old')
    put_trace(oldd,production_trace(4))
    oldtabs={n:table(oldd/f'ul_{n}.csv') for n in ('windows','steps','events')}
    make(name,'UB',summary='TIMEOUT')
    st=steps();st[2]['nw']=nw
    root,d,sp=make(name,st=st)
    trace=production_trace(nw)
    put_trace(d,trace)
    tracek2=[dict(zip(P['records']['windows_cols'],row)) for row in trace['windows'] if row[2]=='2']
    trace_step2=next(dict(zip(P['records']['steps_cols'],row)) for row in trace['steps'] if row[2]=='2')
    save(f'producer_completed_hold_{nw}_windows',{'k2_windows':tracek2,'k2_step':trace_step2,'result':trace['result']},
         'Actual generated deck control flow emits this completed hold from concrete window observations',
         len(tracek2)==nw and int(trace_step2['n_windows'])==nw and trace_step2['steady']=='1' and trace['result']=='RM_STOP')
    u._fake_restored(str(root),B);write(root/B/'ul_base.in','variable ul_S2max equal 1e-05\n')
    before=chain(root,d)
    save(f'fresh_completed_hold_{nw}_windows',before,'Fresh successful control before resume-layout mutation',is_ok(before))
    sr=resume(d,mode='clean')
    for n in ('windows','steps'):
        cols,rows=table(d/f'ul_{n}.csv')
        stale=[dict(r) for r in oldtabs[n][1] if r['k']=='2']
        put(d/f'ul_{n}.csv',cols,[r for r in rows if int(r['step'])<=sr]+stale+[r for r in rows if int(r['step'])>sr])
    # First-attempt dump files persist on disk; keep all old frames not replaced
    # by the second attempt. This avoids a serializer-only missing-frame artifact.
    for p in (oldd/'dump').iterdir():
        if not (d/'dump'/p.name).exists(): shutil.copyfile(p,d/'dump'/p.name)
    cols,rows=table(d/'ul_events.csv')
    at=next(i for i,r in enumerate(rows) if r['event']=='RESUME')
    rows[at:at]=[dict(r) for r in oldtabs['events'][1] if r['event']=='CROSS']
    put(d/'ul_events.csv',cols,rows)
    a=chain(root,d)
    save(name,a,'Authorized restart with coherent completed hold records; changed hold duration is exploratory',is_ok(a))

# UTc: parent RM belongs to a different folder; no local resume_from expected.
for mut in ('positive_utc','utc_missing_resume','utc_wrong_resume_k'):
    root,d,sp=full(mut)
    cont=[{'lift_um':.4,'P':0.,'steady':True,'nw':5,'kind':'B','phase':2,'modeB':1,'n_move':0,'wall':[[]]*5}]
    utc=Path(u._mk_utc(str(root),B,sp,cont,P,events=[('SEPARATED',5,'w2'),('POST_DONE',5,'w5')]))
    write(utc/'deck.liggghts',mk.render(B,'U_UT3',P))
    if mut=='utc_missing_resume': edit(utc/'ul_events.csv',lambda rows: rows.__setitem__(slice(None),[r for r in rows if r['event']!='RESUME']))
    if mut=='utc_wrong_resume_k': edit(utc/'ul_events.csv',lambda rows: next(r for r in rows if r['event']=='RESUME').update(k='3'))
    v=u.arm_verdict(str(utc),B,'UTc',P,root=str(root))
    ok=(v['primary_status']=='OK' and v['trajectory_status']=='DONE' and v['continuation']['status']=='OK') if mut=='positive_utc' else v['continuation']['status']=='FAIL'
    save(mut,v,'UTc valid parent resumes without local auth; missing/mismatched parent boundary rejected',ok)

# Q5: actual arm with primary already established, followed by separation.
for mut in ('sep_positive','sep_no_deck','sep_missing_w3','sep_shifted_w3','sep_gap_new_declaration','sep_declare_w12','sep_wrong_deck_W'):
    st=steps()
    n=15 if mut=='sep_declare_w12' else (8 if mut=='sep_gap_new_declaration' else 6)
    wall=([[-1.]]*10+[[]]*5) if mut=='sep_declare_w12' else [[]]*n
    if mut=='sep_gap_new_declaration': wall[2]=[-1.]
    st.append({'lift_um':.4,'P':0.,'steady':True,'nw':n,'kind':'B','phase':2,'modeB':1,'n_move':0,'wall':wall})
    sw,pw=(12,15) if mut=='sep_declare_w12' else ((5,8) if mut=='sep_gap_new_declaration' else (2,5 if mut!='sep_missing_w3' else 6))
    ev=[('CROSS',2,'first'),('RM',4,'ncross2'),('SEPARATED',5,f'w{sw}'),('POST_DONE',5,f'w{pw}')]
    if mut=='sep_gap_new_declaration': ev[2:2]=[('SEPARATED',5,'w2'),('RECONTACT',5,'w3')]
    root,d,sp=make(mut,'UB',st,'DONE',ev,deck=mut!='sep_no_deck')
    if mut=='sep_gap_new_declaration':
        _,ws=table(d/'ul_windows.csv')
        rcstep=next(r['step'] for r in ws if r['k']=='5' and r['w']=='3')
        edit(d/'ul_events.csv',lambda rows: next(r for r in rows if r['event']=='RECONTACT').update(step=rcstep,detail='n1'))
        def phase_rows(rows):
            for r in rows:
                if r['k']=='5' and (r['w']=='3' or int(r['w'])>=6): r['phase']='3'
        edit(d/'ul_windows.csv',phase_rows)
    if mut in ('sep_missing_w3','sep_gap_new_declaration'):
        edit(d/'ul_windows.csv',lambda rows: rows.__setitem__(slice(None),[r for r in rows if not(r['k']=='5' and r['w']=='3')]))
    if mut=='sep_shifted_w3':
        box={}
        def change(rows):
            r=next(r for r in rows if r['k']=='5' and r['w']=='3'); box['old']=int(r['step']);r['step']=str(box['old']+1000)
        edit(d/'ul_windows.csv',change)
        op=d/'dump'/f'wall_{box["old"]}.dump';np=d/'dump'/f'wall_{box["old"]+1000}.dump'
        op.rename(np);u._restep(str(np),box['old']+1000)
    if mut=='sep_wrong_deck_W': write(d/'deck.liggghts',(d/'deck.liggghts').read_text().replace('variable ul_W equal 5000','variable ul_W equal 4000'))
    v=u.arm_verdict(str(d),B,'UB',P,root=str(root))
    bad=mut in ('sep_missing_w3','sep_shifted_w3','sep_wrong_deck_W')
    save(mut,{'verdict':v,'W':u._arm_wsteps(str(d),'UB',P)},'Primary preserved; final separation matches contiguous windows and events',v['primary_status']=='OK' and v['trajectory_status']==('SEP_INCOMPLETE' if bad else 'DONE'))

# Both deck and registered fallback must select the same physical arm W.
ws={}
for job in ('UB','UT','UVa','UVb','UT3','UTc','G_UB','G_UVa','G_UVb','G_UT3'):
    expected=10000 if job in ('UT','UVb','UT3','UTc','G_UVb','G_UT3') else 5000
    ws[job]={'fallback':u._arm_wsteps(str(E/'absent'),job,P),'expected':expected}
save('registered_W_fallbacks',ws,'Registered arm W for UTc and gravity mapping',all(x['fallback']==x['expected'] for x in ws.values()))

OUT['summary']={'cases':len(OUT['cases']),'passed':sum(c['pass'] for c in OUT['cases'].values()),
                'failed_expectations':[n for n,c in OUT['cases'].items() if not c['pass']]}
write(R/'evidence/resume_recheck.json',json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(OUT['summary'],ensure_ascii=False))
print(str(E))

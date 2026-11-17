"""Embedded fixture evaluator: all code/data dependencies supplied by builder."""
CHECKS=('P_tech','RT1_exists','RT2_exists','RT1_args','RT2_args','RT1_tech','RT2_tech',
        'RT1_marker','RT2_marker','RT1_resets','RT2_resets','bind_sha','bind_path',
        'post_list','pair_read','atom_read','step','pairs','g2cp','hist_value')

def _value(path):
    raw=C.text(path)
    return raw.strip() if raw is not None else None

def _same(a,b):
    try:return Path(a).resolve(strict=True)==Path(b).resolve(strict=True)
    except (OSError,RuntimeError,TypeError):return False

def producer_history(run,rt,atom_ids):
    path=Path(run)/'P/producer'/f"pair_{CONTRACT['ul_s0']}.dump"
    try:
        lines=path.read_text(encoding='ascii').splitlines()
        if len(lines)<9 or lines[0]!='ITEM: TIMESTEP' or lines[2]!='ITEM: NUMBER OF ENTRIES':return False
        # Guard exact lexical IDs before the preserved history parser converts floats.
        for line in lines[9:]:
            if not line.strip():continue
            tokens=line.split()
            if len(tokens)!=7:return False
            for token in tokens:N._finite(token)
            a,b=N._id(tokens[0]),N._id(tokens[1])
            if a not in atom_ids or b not in atom_ids or a==b or tokens[2] not in ('0','1','0.0','1.0'):return False
        d=H.read_dump(path,'local',CONTRACT['pair_cols'])
        if not d['ok'] or d['step']!=CONTRACT['ul_s0']:return False
        source,_,problems=H.local_map(d,'pair',atom_ids,CONTRACT)
        if problems or not source or source.keys()!=rt.keys():return False
        tol=CONTRACT['tolerances']
        return all(H._close(source[k][j+1],rt[k][22+j],tol['post_rel'],tol['post_abs']) for k in source for j in range(3))
    except (OSError,ValueError,ArithmeticError,UnicodeError):return False

def evaluate_fixture(run):
    run=Path(run);step=CONTRACT['ul_s0'];count=CONTRACT['ul_atoms0']
    checks={name:False for name in CHECKS}
    checks['P_tech']=_value(run/'P/rc')=='0' and (run/'P/fixture.bin').is_file()
    screens={s:C.screen_info(C.text(run/s/'screen.out')) for s in ('RT1','RT2')}
    for s in ('RT1','RT2'):
        checks[s+'_exists']=(run/s).is_dir() and _value(run/s/'deck.txt')=='in.hist_'+s.lower()+'.liggghts'
        ck=run/('P/fixture.bin' if s=='RT1' else 'RT1/rt.bin')
        checks[s+'_args']=_value(run/s/'np.txt')=='6' and _same(_value(run/s/'ckpt.txt'),ck)
        checks[s+'_tech']=_value(run/s/'rc')=='0' and screens[s]['technical']
        checks[s+'_marker']=[x for x in screens[s]['markers'] if x.startswith('UL_RT_DONE')]==[f'UL_RT_DONE bed=hist_rt step={step}']
        checks[s+'_resets']=screens[s]['resets_ok']
    binding=B.check_binding(run,log_name='log.liggghts',require_ckpt=True)
    # One strict binding validator: both checks include syntax/duplicate failures.
    checks['bind_sha']=checks['bind_path']=binding['status']=='PASS'
    checks['post_list']=all(C.post_list(run/s/'post',step) for s in ('RT1','RT2'))
    pairs=[N.read_contacts(run/s/'post'/f'rt_pair_{step}.dump') for s in ('RT1','RT2')]
    atoms=[C.read_atoms(run/s/'post'/f'rt_atom_{step}.dump',count) for s in ('RT1','RT2')]
    checks['pair_read']=all(p['status']=='PASS' for p in pairs)
    checks['atom_read']=all(a['ok'] for a in atoms) and atoms[0]['rows'].keys()==atoms[1]['rows'].keys()
    checks['step']=all(p.get('step')==step for p in pairs+atoms)
    checks['pairs']=all(p['rows'] for p in pairs)
    numeric=N.g2cp_compare(run/'RT2/post'/f'rt_pair_{step}.dump',run/'RT1/post'/f'rt_pair_{step}.dump',expected_step=step)
    checks['g2cp']=numeric['status']=='PASS'
    checks['hist_value']=checks['pair_read'] and checks['atom_read'] and producer_history(run,pairs[0]['rows'],set(atoms[0]['rows']))
    ok=all(v is True for v in checks.values())
    return {'schema':'ps45_unload_rt_grammar_verdict_v1','run_dir':str(run.absolute()),
            'status':'PASS' if ok else 'FAIL','exit_code':0 if ok else 2,'checks':checks,
            'numeric':numeric,'binding':binding,'physical_qualification':False,
            'scope':'RT grammar/fixture only; no production or physical GO'}

def fixture_main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('run',type=Path);a=p.parse_args()
    result=evaluate_fixture(a.run);print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    return result['exit_code']

if __name__=='__main__':raise SystemExit(fixture_main())

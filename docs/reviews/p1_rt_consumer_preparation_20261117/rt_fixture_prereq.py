"""Candidate fixture provenance/reread check; never grants operational GO."""
import hashlib,json,re,types
from pathlib import Path
REQUIRED=('mode','end','kit','sums_sha256','lmp_sha256')
STAGES=(('P','in.hist_producer.liggghts'),('RT1','in.hist_rt1.liggghts'),('RT2','in.hist_rt2.liggghts'))
FILES=tuple(deck for _,deck in STAGES)+('plate_hist.stl','read_rt_grammar.py','rt_fixture_contract.json')
def sha(data):return hashlib.sha256(data).hexdigest()
def check(verdict_path,lmp_sha,expected):
    result={'ok':False,'operational_go':False,'errors':[],'reread':None};errors=result['errors']
    try:
        path=Path(verdict_path);run=path.parent.resolve(strict=True);v=json.loads(path.read_bytes())
        if set(expected)!=set(FILES) or any(not isinstance(x,str) or not re.fullmatch('[0-9a-f]{64}',x) for x in expected.values()):raise ValueError('expected candidate source identities')
        if not isinstance(lmp_sha,str) or not re.fullmatch('[0-9a-f]{64}',lmp_sha):raise ValueError('binary identity')
        if not isinstance(v,dict) or not isinstance(v.get('run_dir'),str) or Path(v['run_dir']).resolve()!=run:raise ValueError('verdict location')
        records={}
        for line in (run/'run_manifest.txt').read_text(encoding='utf8').splitlines():
            key,sep,value=line.partition('=')
            if key not in REQUIRED:continue
            if not sep or key in records or not value:raise ValueError('missing/duplicate manifest record')
            records[key]=value
        if set(records)!=set(REQUIRED) or records['mode']!='rt_grammar' or records['lmp_sha256']!=lmp_sha:raise ValueError('manifest identity/mode/end')
        kit=Path(records['kit'])
        if not kit.is_absolute():raise ValueError('absolute candidate kit required')
        sums=(kit/'RT_CANDIDATE_SHA256SUMS').read_bytes()
        if sha(sums)!=records['sums_sha256']:raise ValueError('candidate list hash')
        listed={}
        for line in sums.decode('ascii').splitlines():
            h,name=line.split('  ',1)
            if name in listed or name not in FILES or not re.fullmatch('[0-9a-f]{64}',h):raise ValueError('candidate list')
            listed[name]=h
        if listed!=expected:raise ValueError('candidate expected list mismatch')
        blobs={name:(kit/name).read_bytes() for name in FILES}
        if any(sha(blobs[n])!=expected[n] for n in FILES):raise ValueError('candidate source hash')
        for stage,deck in STAGES:
            d=run/stage
            if (d/'rc').read_text().strip()!='0' or (d/'deck.txt').read_text().strip()!=deck:raise ValueError('stage rc/deck')
            for name in (deck,'plate_hist.stl'):
                if sha((d/name).read_bytes())!=expected[name]:raise ValueError('stage source copy')
        # Execute exactly the validated reader bytes; no later reread/import race.
        module=types.ModuleType('verified_rt_fixture')
        exec(compile(blobs['read_rt_grammar.py'],'<validated-rt-fixture>','exec'),module.__dict__)
        if module.CONTRACT!=json.loads(blobs['rt_fixture_contract.json']):raise ValueError('embedded contract mismatch')
        checks=v.get('checks')
        if (v.get('schema')!='ps45_unload_rt_grammar_verdict_v1' or v.get('status')!='PASS'
            or type(v.get('exit_code')) is not int or v['exit_code']!=0 or not isinstance(checks,dict)
            or set(checks)!=set(module.CHECKS) or any(x is not True for x in checks.values())):raise ValueError('stored verdict not twenty true')
        fresh=module.evaluate_fixture(run)
        result['reread']={'status':fresh['status'],'exit_code':fresh['exit_code'],'checks':fresh['checks']}
        if fresh['schema']!=v['schema'] or fresh['status']!='PASS' or fresh['exit_code']!=0 or fresh['checks']!=checks:raise ValueError('raw fixture reread disagrees')
        result['ok']=True
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,SyntaxError) as error:errors.append(str(error))
    return result

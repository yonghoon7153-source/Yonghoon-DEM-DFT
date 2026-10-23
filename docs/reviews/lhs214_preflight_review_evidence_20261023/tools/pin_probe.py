import contextlib
import json
import os
import sys
from pathlib import Path

ROOT=Path(os.environ.get('REPO_ROOT', Path(__file__).resolve().parents[4])).expanduser().resolve()
OUT=Path(os.environ.get('EVIDENCE_OUT', Path.cwd() / 'lhs214-reproduction')).expanduser().resolve()
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0,str(ROOT/'scripts'))
import supp20_input_receipt as S
import run_network_194_parallel as N

original=N.preflight_receipt_checks
done=False
def wrapped(path,*args,**kwargs):
    global done
    initial=original(path,*args,**kwargs)
    if done or not initial.get('checks') or not all(c['ok'] for c in initial['checks']):
        return initial
    done=True
    p=Path(path)
    old=p.read_bytes()
    rec=json.loads(old)
    pin=rec['git']['sha']
    assert len(pin)==40
    out={}
    cases={'normal':pin,'trailing_LF':pin+'\n','trailing_CRLF':pin+'\r\n',
           'wrong_last_digit':pin[:-1]+('0' if pin[-1]!='0' else '1'),
           'trailing_space':pin+' ','trailing_NUL':pin+'\x00'}
    try:
        for name,sha in cases.items():
            rec['git']['sha']=sha
            p.write_text(json.dumps(rec))
            got=original(p,expect_set='supp20',approved_sha=pin)
            out[name]={'git_sha':sha,'approved_sha':pin,
                       'bad':[c['id'] for c in got['checks'] if not c['ok']],
                       'checks':got['checks']}
            (OUT/('pin_'+name+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
        log=initial['log']['path']
        (OUT/'pin_normal.log').write_bytes(Path(log).read_bytes())
    finally:
        p.write_bytes(old)
    (OUT/'pin-probe.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    return initial

N.preflight_receipt_checks=wrapped
try:
    with (OUT/'pin-probe-selftest.log').open('w') as f,contextlib.redirect_stdout(f):
        rc=S._selftest()
finally:
    N.preflight_receipt_checks=original
assert done
print(json.dumps({'selftest_rc':rc,'cases':{k:v['bad'] for k,v in json.loads((OUT/'pin-probe.json').read_text()).items()}},indent=2))

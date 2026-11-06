"""In-memory BAN8 midpoint mutants; leaves the supplied source unchanged."""
from pathlib import Path
import contextlib
import inspect
import io
import json
import sys

repo = Path(__file__).resolve().parent.parent / 'received' / 'repo'
sys.path.insert(0, str(repo / 'scripts'))
import carbon_junction as cj
import test_carbon_junction as test

original = cj._divide_runs_idx
source = inspect.getsource(original)
old = 't = (j + 0.5) * L / k'
assert source.count(old)==1
out=[]
for tag,new in [('M3_start','t = j * L / k'), ('B01_quarter','t = (j + 0.25) * L / k')]:
    test._ok=0
    test._fail.clear()
    ns = dict(original.__globals__)
    exec(compile(source.replace(old,new),str(repo/'scripts'/'carbon_junction.py'),'exec'),ns)
    cj._divide_runs_idx = ns['_divide_runs_idx']
    log=io.StringIO()
    sys.argv=['test_carbon_junction.py','--only','BAN8']
    try:
        with contextlib.redirect_stdout(log):
            rc=test.main()
    finally:
        cj._divide_runs_idx=original
    text=log.getvalue()
    (Path(__file__).parent/f'{tag}.log').write_text(text,encoding='utf-8')
    failures=[line.strip() for line in text.splitlines() if line.strip().startswith('FAIL  ')]
    out.append({'mutant':tag,'rc':rc,'failures':failures,
                'eq8_check_failure':any('BAN8 ④' in x for x in failures),
                'geometry_midpoint_failure':any('BAN8 ⑨' in x for x in failures)})
print(json.dumps(out,ensure_ascii=False,indent=2))
assert all(x['rc']!=0 and x['geometry_midpoint_failure'] for x in out)

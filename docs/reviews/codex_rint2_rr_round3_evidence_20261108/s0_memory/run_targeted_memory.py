"""Rerun only supplied synthetic SELF-155/CP-ORD tests, with explicit archived baseline modules.
No field data, S0 CLI, host or external process launched. Module payload/solver calls are tiny synthetic test fixtures.
"""
import contextlib
import hashlib
import importlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

root=Path(__file__).resolve().parent
scratch=root/'tmp'
scratch.mkdir(exist_ok=True)
tempfile.tempdir=str(scratch)
repo=Path(sys.argv[1]).resolve()
old=Path(sys.argv[2]).resolve()
sys.path.insert(0,str(repo/'scripts'))
tc=importlib.import_module('test_carbon_junction')
tc.CJ=importlib.import_module('carbon_junction')
tc.S3=importlib.import_module('step3_sigma')
sp=importlib.util.spec_from_file_location('carbon_junction_ref_review',old)
base=importlib.util.module_from_spec(sp)
sp.loader.exec_module(base)
tc._REF_CJ.update(m=base,why='',blob_sha256=hashlib.sha256(old.read_bytes()).hexdigest())
tags={'CP-ORD','PSRCH','PEQ','PREG','PS0','PTIE','PEDGE','PMEM','PMUT'}
before=tc._ok
with (root/'targeted_memory.log').open('w',encoding='utf-8') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
    for tag,fn in tc.CASES:
        if tag in tags:
            print('TAG',tag,flush=True)
            try: fn()
            except Exception:
                import traceback
                traceback.print_exc()
                tc.chk(tag+' exception',False)
summary={'passed':tc._ok-before,'failed':len(tc._fail),'failures':tc._fail,'tags':sorted(tags),
         'baseline_file':str(old),'baseline_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),
         'basis':'supplied resident synthetic tests, independently executed; explicit raw pinned old module injected to avoid absent git object store'}
if len(sys.argv)>3:
    os0=Path(sys.argv[3]).resolve()
    ts=importlib.import_module('test_ca_s0_census')
    sp=importlib.util.spec_from_file_location('ca_s0_census_ref_review',os0)
    bs=importlib.util.module_from_spec(sp);sp.loader.exec_module(bs)
    ts._REF_S0.update(m=bs,why='')
    with (root/'targeted_s0_memory.log').open('w',encoding='utf-8') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
        try: ts.t_mem()
        except Exception:
            import traceback
            traceback.print_exc()
            ts.chk('M exception',False)
    summary['s0']={'passed':ts._ok,'failed':len(ts._fail),'failures':ts._fail,
                   'baseline_file':str(os0),'baseline_sha256':hashlib.sha256(os0.read_bytes()).hexdigest()}
(root/'targeted_memory_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
sys.exit(bool(tc._fail or summary.get('s0',{}).get('failed')))

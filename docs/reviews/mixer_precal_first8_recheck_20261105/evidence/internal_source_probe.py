#!/usr/bin/env python3
"""Bounded independent PRE8-02 source-loading probes; scratch copies only."""
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

REPO = Path('/workspace/nonrint-1104/mixer/scripts')
OUT = Path('/workspace/nonrint-1105/pre8-fix')
NAMES = ('mixer_precal_observe', 'mixer_precal_prepare', 'mixer_contact_reader',
         'measure_mixing_index', 'measure_bed_aspect', 'make_mixer_deck',
         'mixer_deck_readback', 'mixer_deck_diff', 'make_mixer_resume',
         'test_mixer_precal_observe')


def copied(folder):
    folder.mkdir()
    for name in NAMES:
        shutil.copyfile(REPO/(name+'.py'), folder/(name+'.py'))
    return folder


def child(folder, body):
    code = 'import sys,json,hashlib,os\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nROOT=Path(sys.argv[1])\n' + body
    run = subprocess.run([sys.executable, '-I', '-B', '-c', code, str(folder)],
                         capture_output=True, text=True, timeout=30)
    return {'rc': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr,
            'data': json.loads(run.stdout) if run.returncode == 0 else None}


FIXTURE = '''
import test_mixer_precal_observe as T
O=T.O
f=T.DiskContract();f.setUp()
run,B=f.make_run('e0')
'''


report = {'scope': 'PRE8-02 loading/source binding only; three independent scratch probe groups; unit fixture mocks preparation binding only; no research data, no full suite',
          'python': platform.python_version(),
          'source_sha256': {n+'.py': hashlib.sha256((REPO/(n+'.py')).read_bytes()).hexdigest() for n in NAMES},
          'probes': {}}
with tempfile.TemporaryDirectory(dir=str(OUT), prefix='independent-source-') as directory:
    root=Path(directory)
    one=copied(root/'post_import')
    old=child(one,FIXTURE+'''
p=ROOT/'measure_mixing_index.py'
old_sha=hashlib.sha256(p.read_bytes()).hexdigest()
p.write_bytes(p.read_bytes()+b'\\ndef cell_stats(*args, **kwargs):\\n    raise ValueError("INDEPENDENT_PRE8_STALE_SENTINEL")\\n')
new_sha=hashlib.sha256(p.read_bytes()).hexdigest()
r=f.invoke(run,B)
print(json.dumps({'status':r['status'],'reasons':r['reasons'],'no_values':r['contact'] is None and r['mixing'] is None,
 'old_sha':old_sha,'new_sha':new_sha,'recorded_sha':r['provenance']['module_sha256']['measure_mixing_index']['sha256']}))
f.doCleanups()
''')
    fresh=child(one,FIXTURE+'''
r=f.invoke(run,B)
print(json.dumps({'status':r['status'],'reasons':r['reasons'],'no_values':r['contact'] is None and r['mixing'] is None,
 'recorded_sha':r['provenance']['module_sha256']['measure_mixing_index']['sha256']}))
f.doCleanups()
''')
    report['probes']['post_import_sentinel_and_fresh_process']={'loaded':old,'fresh':fresh}

    two=copied(root/'stale_pyc')
    stale=child(two, '''
import py_compile
p=ROOT/'measure_mixing_index.py'
p.write_bytes(p.read_bytes()+b'\\nSOURCE_PROBE="OLD"\\n_original_cell_stats=cell_stats\\ndef cell_stats(*args,**kwargs):\\n    return dict(_original_cell_stats(*args,**kwargs), source_probe=SOURCE_PROBE)\\n')
stamp=p.stat()
py_compile.compile(str(p), doraise=True, invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
p.write_bytes(p.read_bytes().replace(b'SOURCE_PROBE="OLD"',b'SOURCE_PROBE="NEW"'))
os.utime(str(p),ns=(stamp.st_atime_ns,stamp.st_mtime_ns))
import measure_mixing_index as stale
canonical_before=sys.modules['measure_mixing_index']
'''+FIXTURE+'''
r=f.invoke(run,B)
print(json.dumps({'status':r['status'],'reasons':r['reasons'],'canonical_marker':stale.SOURCE_PROBE,
 'private_marker':O.mixing.SOURCE_PROBE,'metric_marker':r['mixing']['grids'][0]['t0_stats']['source_probe'] if r['mixing'] else None,
 'canonical_unchanged':sys.modules['measure_mixing_index'] is canonical_before,
 'different_module_objects':O.mixing is not canonical_before,
 'recorded_current_source':r['provenance']['module_sha256']['measure_mixing_index']['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()}))
f.doCleanups()
''')
    report['probes']['stale_timestamp_pyc_and_canonical_module']=stale

    three=copied(root/'bootstrap_syntax_failure')
    boot=child(three, '''
p=ROOT/'measure_mixing_index.py';p.write_bytes(p.read_bytes()+b'\\nBROKEN_SOURCE = (\\n')
import mixer_precal_observe as O
r=O.analyse_run('PRECAL_E0', ROOT/'not-read')
print(json.dumps({'status':r['status'],'reasons':r['reasons'],'no_values':r['contact'] is None and r['mixing'] is None,
 'bootstrap_error_present':O._BOOT_ERROR is not None}))
''')
    report['probes']['bootstrap_compile_failure']=boot

a=old['data'];b=fresh['data'];c=stale['data'];d=boot['data']
report['passed']=(all(x['rc']==0 for x in (old,fresh,stale,boot)) and
 a['status']=='TECH' and a['no_values'] and a['recorded_sha']==a['old_sha'] and
 b['status']=='TECH' and b['no_values'] and b['recorded_sha']==a['new_sha'] and
 any('INDEPENDENT_PRE8_STALE_SENTINEL' in r for r in b['reasons']) and
 c['status']=='OK' and c['canonical_marker']=='OLD' and c['private_marker']==c['metric_marker']=='NEW' and
 c['canonical_unchanged'] and c['different_module_objects'] and c['recorded_current_source'] and
 d['status']=='TECH' and d['no_values'] and d['bootstrap_error_present'])
report['read_only_review']=['private dependency imports, including from-import/lazy paths, use captured raw-byte registry',
 'observer self-code comparison states compile equivalence, not unique historical source text',
 'generator builtins open for its own source returns captured bytes, not disk; reviewed, not independently executed here',
 'entry and return checks compare current source to captured bytes; provenance uses fixed digest table, not canonical sys.modules']
(OUT/'internal_source_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'probe_groups':len(report['probes']),'report':str(OUT/'internal_source_review.json')},indent=2))
sys.exit(0 if report['passed'] else 1)

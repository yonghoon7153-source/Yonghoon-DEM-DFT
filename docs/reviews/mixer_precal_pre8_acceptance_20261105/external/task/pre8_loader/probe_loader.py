"""Independent bounded PRE8-02 source-loading probes. Scratch source copies only.

Observation fixtures mock validate_case alone; real 3-atom parsing/contact/cell_stats
and source verification. Static generator/readback probes have no mocks and do not
write generated decks, launch any job, or claim 100000-particle observation success.
"""
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

OUT = Path(__file__).resolve().parent
INPUT = OUT.parents[1] / 'input'
SCRIPTS = INPUT / 'scripts'
NAMES = ('mixer_precal_observe', 'mixer_precal_prepare', 'mixer_contact_reader',
         'measure_mixing_index', 'measure_bed_aspect', 'make_mixer_deck',
         'mixer_deck_readback', 'mixer_deck_diff', 'make_mixer_resume',
         'test_mixer_precal_observe')

def hashes():
    return {n+'.py': hashlib.sha256((SCRIPTS/(n+'.py')).read_bytes()).hexdigest() for n in NAMES}

def copied(root, name):
    folder = root/name
    folder.mkdir()
    for module in NAMES:
        shutil.copyfile(SCRIPTS/(module+'.py'), folder/(module+'.py'))
    return folder

PREFIX = '''import sys, json, os, hashlib
from pathlib import Path
ROOT=Path(sys.argv[1])
sys.path.insert(0,str(ROOT))
import tempfile
(ROOT/'tmp').mkdir(exist_ok=True)
tempfile.tempdir=str(ROOT/'tmp')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def compact(r):
    return {'status':r['status'],'reasons':r['reasons'],
            'no_values':all(r[k] is None for k in ('contact','mixing','counts','reference_counts')),
            'recorded_sha':{n:v['sha256'] for n,v in r['provenance']['module_sha256'].items()}}
'''
FIXTURE = '''import test_mixer_precal_observe as T
O=T.O
f=T.DiskContract(); f.setUp()
run,B=f.make_run('e0')
'''

def child(folder, name, body):
    path=folder/(name+'_child.py')
    path.write_text(PREFIX+body,encoding='utf-8')
    proc=subprocess.run([sys.executable,'-I','-B','-X','utf8',str(path),str(folder)],
                        text=True,capture_output=True,timeout=60)
    record={'rc':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}
    try: record['data']=json.loads(proc.stdout)
    except ValueError: record['data']=None
    return record

report = {'pin':(INPUT/'PIN.txt').read_text().strip(), 'python':platform.python_version(),
          'executable':sys.executable, 'flags':'-I -B -X utf8; scratch sys.path explicit',
          'scope':'PRE8-02 only, small synthetic fixtures and in-memory static generation; no DEM, research, full gate, deployment, registration, or ledger closure',
          'mock_boundary':'Fixture invoke patches validate_case only. Actual contact, cell_stats, readback and source loader run. Profile callbacks schedule scratch disk mutations without changing calculation results.',
          'source_before':hashes(), 'probes':{}}
checks={}

def add(name, result, predicate):
    report['probes'][name]=result
    try: checks[name]=result['rc']==0 and bool(predicate(result['data']))
    except Exception: checks[name]=False

with tempfile.TemporaryDirectory(prefix='loader-scratch-',dir=OUT) as temporary:
    root=Path(temporary)
    one=copied(root,'post_import')
    old=child(one,'loaded',FIXTURE+'''
p=ROOT/'measure_mixing_index.py'
original=p.read_bytes(); old_sha=sha(p)
token=b"def cell_stats(D, r_container, cells=8, x_cells=2, n_min=20, axis='x'):\\n"
assert original.count(token)==1
p.write_bytes(original.replace(token,token+b"    raise ValueError('INDEPENDENT_PRE8_SOURCE_SENTINEL')\\n",1))
r=f.invoke(run,B)
out=compact(r); out.update(old_sha=old_sha,new_sha=sha(p))
print(json.dumps(out)); f.doCleanups()
''')
    add('original_external_sentinel_after_import',old,lambda d:d['status']=='TECH' and d['no_values'] and d['recorded_sha']['measure_mixing_index']==d['old_sha'] and any('bound source changed: measure_mixing_index' in s for s in d['reasons']))
    fresh=child(one,'fresh',FIXTURE+'''
r=f.invoke(run,B);out=compact(r);out['current_sha']=sha(ROOT/'measure_mixing_index.py')
print(json.dumps(out));f.doCleanups()
''')
    add('fresh_process_executes_sentinel',fresh,lambda d:d['status']=='TECH' and d['no_values'] and d['recorded_sha']['measure_mixing_index']==d['current_sha']==old['data']['new_sha'] and d['reasons']==['INDEPENDENT_PRE8_SOURCE_SENTINEL'])

    two=copied(root,'stale_pyc')
    stale=child(two,'stale', '''import py_compile
p=ROOT/'measure_mixing_index.py'
p.write_bytes(p.read_bytes()+b'\\nSOURCE_PROBE="OLD"\\n_original_stats=cell_stats\\ndef cell_stats(*a,**k):\\n    return dict(_original_stats(*a,**k), source_probe=SOURCE_PROBE)\\n')
st=p.stat();py_compile.compile(str(p),doraise=True,invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
p.write_bytes(p.read_bytes().replace(b'SOURCE_PROBE="OLD"',b'SOURCE_PROBE="NEW"'))
os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns))
import measure_mixing_index as stale
assert p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns
'''+FIXTURE+'''
r=f.invoke(run,B);out=compact(r)
out.update(canonical_marker=stale.SOURCE_PROBE,private_marker=O.mixing.SOURCE_PROBE,
 metric_marker=r['mixing']['grids'][0]['t0_stats']['source_probe'] if r['mixing'] else None,
 canonical_unchanged=sys.modules['measure_mixing_index'] is stale,
 distinct=O.mixing is not stale,current_sha=sha(p))
print(json.dumps(out));f.doCleanups()
''')
    add('same_mtime_size_pyc_and_stale_sys_modules',stale,lambda d:d['status']=='OK' and d['canonical_marker']=='OLD' and d['private_marker']==d['metric_marker']=='NEW' and d['canonical_unchanged'] and d['distinct'] and d['recorded_sha']['measure_mixing_index']==d['current_sha'])

    three=copied(root,'canonical_poison')
    poisoned=child(three,'poisoned','''import types
names=('mixer_precal_prepare','mixer_contact_reader','measure_mixing_index','measure_bed_aspect','make_mixer_deck','mixer_deck_readback','mixer_deck_diff','make_mixer_resume')
poison={n:types.ModuleType(n) for n in names}
sys.modules.update(poison)
'''+FIXTURE+'''
aliases=[O.preparation.gen is O._REGISTRY['make_mixer_deck'],
 O.preparation.diff.logical_commands is O._REGISTRY['make_mixer_resume'].logical_commands,
 O.contact.deck_plan is O.mixing.deck_plan,
 O.contact.frames is O.bed.frames,
 O.mixing.frames is O.bed.frames,
 O.frames is O.bed.frames]
r=f.invoke(run,B)
# Real generator and positive pair readback execute diff_d2_decks' lazy import.
a=O.preparation._generate('PRECAL_R1_B1_U')
b=O.preparation._generate('PRECAL_R1_B1_C')
pair=O.preparation.diff.diff_d2_decks(a['deck'],b['deck'],a['meta'],b['meta'])
out=compact(r);out.update(aliases=aliases,lazy_pair_verdict=pair['verdict'],
 lazy_pair_failures=pair['failures'],canonical_untouched=all(sys.modules[n] is poison[n] for n in names),
 private_distinct=all(O._REGISTRY[n] is not poison[n] for n in names))
print(json.dumps(out));f.doCleanups()
''')
    add('internal_aliases_and_actual_lazy_import_with_poisoned_modules',poisoned,lambda d:d['status']=='OK' and all(d['aliases']) and d['lazy_pair_verdict']=='PASS' and d['canonical_untouched'] and d['private_distinct'])

    four=copied(root,'generator_reread')
    generator=child(four,'generator',FIXTURE+'''
p=ROOT/'make_mixer_deck.py';original=p.read_bytes();old_sha=sha(p)
before=O.preparation._generate('PRECAL_E0')
p.write_bytes(original+b'\\n# independent source read ABA\\n')
try:
 during=O.preparation._generate('PRECAL_E0')
 during_disk_sha=sha(p)
 refused=f.invoke(run,B)
finally:
 p.write_bytes(original)
after=O.preparation._generate('PRECAL_E0')
accepted=f.invoke(run,B)
print(json.dumps({'before_generator_sha':before['meta']['generator_sha256'],
 'during_generator_sha':during['meta']['generator_sha256'],'after_generator_sha':after['meta']['generator_sha256'],
 'old_sha':old_sha,'during_disk_sha':during_disk_sha,
 'same_generated_deck':before['deck']==during['deck']==after['deck'],
 'same_meta':before['meta']==during['meta']==after['meta'],
 'refused':compact(refused),'accepted':compact(accepted)}));f.doCleanups()
''')
    add('actual_generator_self_read_uses_captured_bytes_during_disk_change',generator,lambda d:d['before_generator_sha']==d['during_generator_sha']==d['after_generator_sha']==d['old_sha']!=d['during_disk_sha'] and d['same_generated_deck'] and d['same_meta'] and d['refused']['status']=='TECH' and d['refused']['no_values'] and d['accepted']['status']=='OK')

    for mutation in ('delete_prepare','syntax_contact','runtime_contact'):
        folder=copied(root,'bootstrap_'+mutation)
        setup={
          'delete_prepare':"(ROOT/'mixer_precal_prepare.py').unlink()\n",
          'syntax_contact':"p=ROOT/'mixer_contact_reader.py';p.write_bytes(p.read_bytes()+b'\\nBROKEN = (\\n')\n",
          'runtime_contact':"p=ROOT/'mixer_contact_reader.py';p.write_bytes(p.read_bytes()+b'\\nraise RuntimeError(\"INDEPENDENT_BOOT_RUNTIME\")\\n')\n"}[mutation]
        got=child(folder,'bootstrap',setup+'''import mixer_precal_observe as O
r=O.analyse_run('PRECAL_E0',ROOT/'not_read')
out=compact(r);out['bootstrap_error']=O._BOOT_ERROR
out['contact_bound']=hasattr(O,'contact')
print(json.dumps(out))
''')
        add('bootstrap_'+mutation,got,lambda d:d['status']=='TECH' and d['no_values'] and bool(d['bootstrap_error']) and not d['contact_bound'])

    for changed in ('semantic','comment'):
        folder=copied(root,'observer_pyc_'+changed)
        edit=("p.write_bytes(raw.replace(b\"SCHEMA = 'mixer_precal_observe/1'\", b\"SCHEMA = 'mixer_precal_observe/9'\",1))" if changed=='semantic' else "p.write_bytes(raw.replace(b'# Capture the executing module code',b'# Capture THE executing module code',1))")
        got=child(folder,'observer','''import py_compile
p=ROOT/'mixer_precal_observe.py';raw=p.read_bytes();st=p.stat()
py_compile.compile(str(p),doraise=True,invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
'''+edit+'''
os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns))
assert p.stat().st_size==st.st_size and p.stat().st_mtime_ns==st.st_mtime_ns
import mixer_precal_observe as O
'''+('''r=O.analyse_run('PRECAL_E0',ROOT/'not_read')
out=compact(r);out.update(current_sha=sha(p),old_sha=hashlib.sha256(raw).hexdigest(),bootstrap_error=O._BOOT_ERROR)
print(json.dumps(out))
''' if changed=='semantic' else '''import test_mixer_precal_observe as T
f=T.DiskContract();f.setUp();run,B=f.make_run('e0')
from unittest import mock
with mock.patch.object(O,'validate_case',side_effect=lambda case,deck,meta:meta):
 r=O.analyse_run(B['case_id'],run)
out=compact(r);out.update(current_sha=sha(p),old_sha=hashlib.sha256(raw).hexdigest(),bootstrap_error=O._BOOT_ERROR)
print(json.dumps(out));f.doCleanups()
'''))
        if changed=='semantic':
            add('observer_stale_pyc_semantic_change_fails_equivalence',got,lambda d:d['status']=='TECH' and d['no_values'] and 'do not compile' in d['bootstrap_error'])
        else:
            add('observer_comment_only_bytes_compile_equivalence_boundary',got,lambda d:d['status']=='OK' and d['bootstrap_error'] is None and d['recorded_sha']['mixer_precal_observe']==d['current_sha']!=d['old_sha'])

    for where in ('after_load','during_metrics'):
        folder=copied(root,where)
        got=child(folder,'timed',FIXTURE+'''
p=ROOT/'measure_mixing_index.py';original=p.read_bytes();fired=[]
target=O._load.__code__
event_name='return'
'''+("target=O.mixing.cell_stats.__code__;event_name='call'\n" if where=='during_metrics' else '')+'''
def callback(frame,event,arg):
 if event==event_name and frame.f_code is target and not fired:
  fired.append(True);p.write_bytes(original+b'\\n# scheduled source change\\n')
sys.setprofile(callback)
try:r=f.invoke(run,B)
finally:sys.setprofile(None)
out=compact(r);out['fired']=bool(fired)
print(json.dumps(out));f.doCleanups()
''')
        add('dependency_change_'+where,got,lambda d:d['fired'] and d['status']=='TECH' and d['no_values'] and any('bound source changed' in s for s in d['reasons']))

report['checks']=checks
report['probe_count']=len(checks)
report['source_after']=hashes()
report['input_sources_unchanged']=report['source_before']==report['source_after']
report['passed']=all(checks.values()) and report['input_sources_unchanged']
(OUT/'probe_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':report['passed'],'probes':report['probe_count'],'checks':checks,'input_sources_unchanged':report['input_sources_unchanged']},indent=2))
sys.exit(0 if report['passed'] else 1)

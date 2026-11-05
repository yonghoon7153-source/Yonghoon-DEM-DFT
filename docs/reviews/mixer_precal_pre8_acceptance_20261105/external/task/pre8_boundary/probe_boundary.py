"""Independent bounded PRE8 observer/entry/cleanup probes; copied sources only."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
from unittest import mock

ROOT = Path(__file__).resolve().parent
INPUT = ROOT.parents[1] / 'input'
SOURCE = INPUT / 'scripts'
NAMES = ('mixer_precal_observe', 'mixer_precal_prepare', 'mixer_contact_reader',
         'measure_mixing_index', 'measure_bed_aspect', 'make_mixer_deck',
         'mixer_deck_readback', 'mixer_deck_diff', 'make_mixer_resume',
         'test_mixer_precal_observe')
RESULTS = []
INITIAL = {n: hashlib.sha256((SOURCE/(n+'.py')).read_bytes()).hexdigest() for n in NAMES}

def copy_sources(directory):
    for n in NAMES:
        shutil.copyfile(SOURCE/(n+'.py'), directory/(n+'.py'))

def child(name, body, flags=()):
    with tempfile.TemporaryDirectory(prefix=name+'_', dir=ROOT) as tmp:
        directory = Path(tmp)
        copy_sources(directory)
        code = """import contextlib,io,json,sys,types,hashlib,tempfile
from pathlib import Path
from unittest import mock
root=Path(sys.argv[1]);sys.path.insert(0,str(root));tempfile.tempdir=str(root)
""" + body
        proc = subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8', *flags,
                               '-c', code, str(directory)], capture_output=True,
                              text=True, encoding='utf-8', timeout=45)
        if proc.returncode:
            raise AssertionError((name, proc.returncode, proc.stdout, proc.stderr))
        data = json.loads(proc.stdout)
        assert not list(directory.rglob('*.pyc')), name
        RESULTS.append(dict(name=name, result='PASS', observations=data,
                            child_rc=proc.returncode, stderr=proc.stderr))

child('self_equivalent_comment', r'''
p=root/'mixer_precal_observe.py';original=p.read_bytes()
changed=original.replace(b'# Capture the executing module code before any research-module import.',
                         b'# Different comment, same compiled module code, retained line count.')
assert changed!=original;p.write_bytes(changed)
O=types.ModuleType('observer_original_code');O.__file__=str(p)
exec(compile(original,str(p),'exec',dont_inherit=True,optimize=sys.flags.optimize),O.__dict__)
assert O._BOOT_ERROR is None,O._BOOT_ERROR
import test_mixer_precal_observe as T
T.O=O;fixture=T.DiskContract();fixture.setUp()
try:
    run,B=fixture.make_run('e0');got=fixture.invoke(run,B)
    assert got['status']=='OK',got
    recorded=got['provenance']['module_sha256']['mixer_precal_observe']['sha256']
    assert recorded==hashlib.sha256(changed).hexdigest()
    assert recorded!=hashlib.sha256(original).hexdigest()
    print(json.dumps(dict(status=got['status'],historical_bytes_differ=True,
                          compiled_equivalence_passed=True,recorded_hash=recorded)))
finally:fixture.doCleanups()
''')

child('self_non_equivalent_code', r'''
p=root/'mixer_precal_observe.py';original=p.read_bytes()
p.write_bytes(original+b'\nOBSERVER_BOUNDARY_SENTINEL=991\n')
O=types.ModuleType('observer_original_code');O.__file__=str(p)
exec(compile(original,str(p),'exec',dont_inherit=True,optimize=sys.flags.optimize),O.__dict__)
assert O._BOOT_ERROR and not hasattr(O,'contact')
got=O.analyse_run('PRECAL_E0',root/'absent')
assert got['status']=='TECH' and all(got[k] is None for k in ('contact','mixing','counts','reference_counts'))
out=io.StringIO()
with contextlib.redirect_stdout(out):rc=O.main(['--case','PRECAL_E0','--run',str(root/'absent')])
parsed=json.loads(out.getvalue());assert rc==2 and parsed==got
print(json.dumps(dict(status=got['status'],reasons=got['reasons'],main_rc=rc,
                      no_contact_class_available=True,partial_hashes=len(got['provenance']['module_sha256']))))
''')

child('self_deleted_before_boot', r'''
p=root/'mixer_precal_observe.py';original=p.read_bytes();p.unlink()
O=types.ModuleType('observer_original_code');O.__file__=str(p)
exec(compile(original,str(p),'exec',dont_inherit=True,optimize=sys.flags.optimize),O.__dict__)
got=O.analyse_run('PRECAL_E0',root/'absent')
assert got['status']=='TECH' and all(got[k] is None for k in ('contact','mixing','counts','reference_counts'))
print(json.dumps(dict(status=got['status'],reasons=got['reasons'],
                      partial_hashes=len(got['provenance']['module_sha256']))))
''')

for failure in ('missing_dependency', 'syntax_dependency'):
    with tempfile.TemporaryDirectory(prefix=failure+'_', dir=ROOT) as tmp:
        directory=Path(tmp);copy_sources(directory)
        dependency=directory/'mixer_precal_prepare.py'
        if failure=='missing_dependency':dependency.unlink()
        else:dependency.write_bytes(dependency.read_bytes()+b'\nif (\n')
        proc=subprocess.run([sys.executable,'-I','-B','-X','utf8',
                             str(directory/'mixer_precal_observe.py'),
                             '--case','PRECAL_E0','--run',str(directory/'absent')],
                            capture_output=True,text=True,encoding='utf-8',timeout=45)
        got=json.loads(proc.stdout)
        assert proc.returncode==2 and got['status']=='TECH' and not proc.stderr
        assert all(got[k] is None for k in ('contact','mixing','counts','reference_counts'))
        assert not list(directory.rglob('*.pyc'))
        RESULTS.append(dict(name=failure+'_actual_cli', result='PASS', child_rc=proc.returncode,
                            observations=dict(status=got['status'],reasons=got['reasons'],
                              partial_hashes=len(got['provenance']['module_sha256'])),stderr=proc.stderr))

child('repeated_calls_and_generator_cleanup', r'''
import test_mixer_precal_observe as T
O=T.O;fixture=T.DiskContract();fixture.setUp()
try:
    run,B=fixture.make_run('e0');statuses=[]
    statuses.append(fixture.invoke(run,B)['status'])
    meta=run/'deck_meta.json';raw=meta.read_bytes();meta.write_bytes(b'{"x":1,"x":2}')
    statuses.append(fixture.invoke(run,B)['status']);meta.write_bytes(raw)
    statuses.append(fixture.invoke(run,B)['status'])
    self_path=root/'mixer_precal_observe.py';raw_self=self_path.read_bytes()
    self_path.write_bytes(raw_self+b'\n# post-import change\n')
    changed=fixture.invoke(run,B);statuses.append(changed['status'])
    assert all(changed[k] is None for k in ('contact','mixing','counts','reference_counts'))
    self_path.write_bytes(raw_self);statuses.append(fixture.invoke(run,B)['status'])
    assert statuses==['OK','TECH','OK','TECH','OK'],statuses
    gen=O.preparation.gen;original_types=gen.TYPES;original_arms=dict(gen.ARMS)
    outputs=[]
    for case in ('PRECAL_R1_B1_U','PRECAL_R1_B1_C','PRECAL_E0','PRECAL_R1_B1_U'):
        prepared=O.preparation.prepare_case(case)
        outputs.append(hashlib.sha256(prepared['deck']).hexdigest())
        assert gen.TYPES is original_types and gen.ARMS==original_arms
    assert outputs[0]==outputs[-1]
    with mock.patch.object(gen,'deck_meta',side_effect=ValueError('cleanup boundary sentinel')):
        try:O.preparation.prepare_case('PRECAL_R1_B1_U')
        except ValueError as exc:assert str(exc)=='cleanup boundary sentinel'
        else:raise AssertionError('expected injected failure')
    assert gen.TYPES is original_types and gen.ARMS==original_arms
    post=O.preparation.prepare_case('PRECAL_R1_B1_U')
    assert hashlib.sha256(post['deck']).hexdigest()==outputs[0]
    assert gen.TYPES is original_types and gen.ARMS==original_arms
    print(json.dumps(dict(status_sequence=statuses,source_binding_records=len(O._BOUND_DIGESTS),
                          repeated_prepare_identical=True,successful_and_failed_cleanup=True)))
finally:fixture.doCleanups()
''')

child('optimized_observer_entry', r'''
import test_mixer_precal_observe as T
O=T.O
if O._BOOT_ERROR is not None:raise RuntimeError(O._BOOT_ERROR)
fixture=T.DiskContract();fixture.setUp()
try:
    run,B=fixture.make_run('e0');got=fixture.invoke(run,B)
    if got['status']!='OK':raise RuntimeError(str(got))
    print(json.dumps(dict(status=got['status'],optimization=sys.flags.optimize,
                          source_binding_records=len(got['provenance']['module_sha256']))))
finally:fixture.doCleanups()
''',flags=('-O',))

FINAL = {n: hashlib.sha256((SOURCE/(n+'.py')).read_bytes()).hexdigest() for n in NAMES}
assert INITIAL==FINAL
output=dict(pin=(INPUT/'PIN.txt').read_text().strip(),python=sys.version,
            scope='Independent source self-equivalence, bootstrap CLI, repeat-call and cleanup boundaries only',
            probes=RESULTS,probe_groups=len(RESULTS),input_source_hashes_unchanged=INITIAL==FINAL,
            source_sha256=INITIAL,
            limitations=['Three-particle fixture mocks only validate_case; real tiny E0 metrics are exercised.',
                         'Generator exception is an explicit in-memory injection to verify cleanup only.',
                         'Equivalent comment source acceptance is the documented compiled-code boundary, not a new defect.',
                         'No actual research run, DEM, host access, full gate, P1 rerun or positive100000 path.'])
(ROOT/'results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(probe_groups=len(RESULTS),all_passed=True,input_unchanged=True,output=str(ROOT/'results.json'))))

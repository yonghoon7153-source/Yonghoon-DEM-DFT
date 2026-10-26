"""Synthetic oracle checks only; no production dump/runner execution."""
import argparse
import contextlib
import io
from unittest import mock
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import statistics
import sys
import tempfile

sys.dont_write_bytecode = True
EXPECTED = {'ul_lib.py': '23a79392352e01631c6d1f6aaecdb31fc8a53be518ee6f27b815896e161727e6',
            'ul_gates.py': 'c8d45a9cf75f0806e612d810942d23adea4b40feaa5f31f7d279eb8386358de6'}

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--oracle-dir', type=Path, required=True)
    ap.add_argument('--binding-fixtures', type=Path, required=True)
    args = ap.parse_args()
    for name, sha in EXPECTED.items():
        assert hashlib.sha256((args.oracle_dir/name).read_bytes()).hexdigest() == sha
    load('ul_lib', args.oracle_dir/'ul_lib.py')
    gate = load('oracle_ul_gates', args.oracle_dir/'ul_gates.py')
    diag = load('diagnostic', Path(__file__).with_name('diagnose_g2c.py'))
    outcomes = []
    with tempfile.TemporaryDirectory(prefix='g2c-oracle-') as td:
        original, test = Path(td)/'o.dump', Path(td)/'t.dump'
        def base(n=3):
            rows = []
            for k in range(n):
                v = [0.001*(c+1) for c in range(26)]
                v[6:9] = [2*k+1, 2*k+2, 0]
                v[9:18] = [(k+1)*(c+1) for c in range(9)]
                rows.append(v)
            return rows
        def write(path, rows, step=3200000):
            text = ['ITEM: TIMESTEP', str(step), 'ITEM: NUMBER OF ENTRIES', str(len(rows)),
                    'ITEM: BOX BOUNDS pp pp ff', '-1 2', '-2 3', '-3 4', 'ITEM: ENTRIES '+' '.join(diag.COLUMNS)]
            text += [' '.join(map(repr, row)) for row in rows]
            path.write_text('\n'.join(text)+'\n')
        def parity(name, orig, trial):
            write(original, orig); write(test, trial)
            result = diag.analyze(original, test)
            oracle = gate.g2c_compare(str(test), str(original), expected_step=3200000)
            assert result['reproduced_pair_mismatches'] == oracle['n_mismatch'], (name,result,oracle)
            assert result['n_orig'] == oracle['n_orig'] and result['n_test'] == oracle['n_test']
            assert result['discriminating_frac'] == oracle['discriminating_frac']
            _, normalized, _, _ = gate._contacts(str(original), (0.05,0.05))
            vals = [gate._cmpvals(v,(0.05,0.05)) for v in normalized.values()]
            assert result['original_abs_medians'] == [statistics.median(abs(v[c]) for v in vals) for c in range(20)]
            assert sum(x['first_fail'] for x in result['components']) == oracle['n_mismatch']
            outcomes.append({'case':name,'status':'PASS','oracle_pair_mismatches':oracle['n_mismatch']})
            return result
        parity('identical', base(), base())
        for c, field in enumerate(diag.COMPONENTS):
            orig = base(); trial = copy.deepcopy(orig); trial[0][field-1] += 0.0001 if c in diag.PERIODIC else 0.5
            r = parity(f'single_column_{field}',orig,trial)
            assert r['components'][c]['first_fail']==1 and r['components'][c]['any_fail']==1
            assert sum(x['any_fail'] for x in r['components'])==1
        orig=base(); trial=copy.deepcopy(orig)
        trial[0][0] += 0.0001; trial[0][9] += 0.5; trial[0][13] += 0.5; trial[0][22] += 0.5
        r=parity('multiple_families_first_vs_any',orig,trial)
        assert r['reproduced_pair_mismatches']==1 and sum(x['any_fail'] for x in r['components'])==4
        trial=copy.deepcopy(orig)
        for row in trial:
            row[:6]=row[3:6]+row[:3];row[6],row[7]=row[7],row[6];row[9:18]=[-v for v in row[9:18]]
        r=parity('orientation_reversal',orig,trial);assert r['orientation']['pair_orientation_changed']==3
        trial=copy.deepcopy(orig)
        for row in trial:
            for field in [1,2,4,5,24,25]:row[field-1]+=0.05
        r=parity('periodic_images_default_not_header_box',orig,trial);assert r['reproduced_pair_mismatches']==0
        for n,values in [(3,[-7,-1,3]),(4,[-7,-1,3,9])]:
            orig=base(n)
            for row,value in zip(orig,values):
                for c in range(9,18):row[c]=value
            trial=copy.deepcopy(orig);trial[0][9]+=0.00002
            parity(f'full_abs_medians_{n}',orig,trial)
        for label,b in [('equal',100001.0),('below',math.nextafter(100001.0,-math.inf)),('above',math.nextafter(100001.0,math.inf))]:
            orig=base(1);orig[0][9]=100000.;trial=copy.deepcopy(orig);trial[0][9]=b
            r=parity('strict_threshold_'+label,orig,trial)
            assert r['reproduced_pair_mismatches']==int(label=='above')
        orig=base();trial=copy.deepcopy(orig);trial[0][9]=0;trial[1][10]=-orig[1][10]
        r=parity('force_zero_sign',orig,trial)
        assert r['force_zero_sign'][0]['nonzero_to_zero']==1 and r['force_zero_sign'][1]['nonzero_sign_flip']==1
        orig=base(3)
        for row in orig:row[9]=0.0
        trial=copy.deepcopy(orig);trial[0][9]=1e-200
        r=parity('zero_median_no_tolerance_floor',orig,trial)
        assert r['original_abs_medians'][6]==0 and r['components'][6]['zero_threshold_fail']==1
        orig=base(1);orig[0][6]=2**53;orig[0][7]=2**53-1
        parity('largest_exact_ids',orig,orig)
        # Diagnostic deliberately refuses unexpected shape/ID/duplicate changes.
        invalids={
            'missing_column':lambda s:s.replace('c_cpl[26]','wrong'),
            'reordered_columns':lambda s:s.replace('c_cpl[1] c_cpl[2]','c_cpl[2] c_cpl[1]'),
            'nonfinite':lambda s:s.replace('0.001 ', 'nan ',1),
            'wrong_step':lambda s:s.replace('3200000','3200001',1),
            'wrong_count':lambda s:s.replace('NUMBER OF ENTRIES\n3','NUMBER OF ENTRIES\n4'),
            'extra_frame':lambda s:s+'ITEM: TIMESTEP\n3200000\n',
            'bad_bounds':lambda s:s.replace('-1 2','2 2'),
            'tilt_header':lambda s:s.replace('BOX BOUNDS pp pp ff','BOX BOUNDS xy xz yz'),
            'row_cap':lambda s:s.replace('NUMBER OF ENTRIES\n3','NUMBER OF ENTRIES\n600001'),
            'line_cap':lambda s:s.replace('0.001 ', '9'*8193+' ',1),
            'triclinic_record':lambda s:s.replace('-1 2','-1 2 0'),
            'rounded_fraction_id':lambda s:s.replace(' 1 2 0 ', ' 1.0000000000000001 2 0 ',1),
            'oversized_id':lambda s:s.replace(' 1 2 0 ',' 9007199254740993 2 0 ',1),
        }
        for name,mutate in invalids.items():
            write(original,base());write(test,base());test.write_text(mutate(test.read_text()))
            try:diag.analyze(original,test)
            except (ValueError,UnicodeError):outcomes.append({'case':name,'status':'REFUSED_AS_REQUIRED'})
            else:raise AssertionError(name)
        for name,o,t in [('original_duplicate',base()+[base()[0]],base()),('test_duplicate',base(),base()+[base()[0]]),('missing_pair',base(),base()[:2]),('extra_pair',base(),base(4))]:
            write(original,o);write(test,t)
            try:diag.analyze(original,test)
            except ValueError:outcomes.append({'case':name,'status':'REFUSED_AS_REQUIRED'})
            else:raise AssertionError(name)
    with tempfile.TemporaryDirectory(prefix='g2c-endguard-') as td:
        original,test=Path(td)/'o.dump',Path(td)/'t.dump'
        write(original,base());write(test,base())
        for expected,label in [('0'*64,'original_hash_refusal'),(hashlib.sha256(original.read_bytes()).hexdigest(),'original_size_refusal')]:
            try:diag.analyze(original,test,expected)
            except ValueError:outcomes.append({'case':label,'status':'REFUSED_AS_REQUIRED'})
            else:raise AssertionError(label)
        real_stat=diag.os.stat;observations=[0]
        def changed_stat(path,*args,**kwargs):
            stat=real_stat(path,*args,**kwargs)
            if str(path)==str(original):
                observations[0]+=1
                if observations[0]==2:
                    from types import SimpleNamespace
                    return SimpleNamespace(st_dev=stat.st_dev,st_ino=stat.st_ino,st_size=stat.st_size,
                                           st_mtime_ns=stat.st_mtime_ns+1,st_ctime_ns=stat.st_ctime_ns)
            return stat
        with mock.patch.object(diag.os,'stat',side_effect=changed_stat):
            try:diag.analyze(original,test)
            except ValueError as error:
                assert 'complete analysis' in str(error)
                outcomes.append({'case':'original_change_after_stream_detected','status':'REFUSED_AS_REQUIRED'})
            else:raise AssertionError('end stability')
    with tempfile.TemporaryDirectory(prefix='g2c-binding-') as td:
        job, kit = Path(td)/'job', Path(td)/'kit'
        job.mkdir(); kit.mkdir()
        for name in ['ul_lib.py','ul_gates.py','ul_reader.py','SHA256SUMS']:
            (kit/name).write_bytes((args.oracle_dir/name).read_bytes())
        manifest = (args.binding_fixtures/'run_manifest.user-relayed.txt').read_bytes()
        verdict = (args.binding_fixtures/'restore_verdict.user-relayed.json').read_bytes()
        (job/'run_manifest.txt').write_bytes(manifest)
        (job/'restore_verdict.json').write_bytes(verdict)
        bound = diag.bind_job(job,kit)
        assert bound['job_id']=='323957'
        outcomes.append({'case':'binding_semantic_normalized_relay','status':'PASS'})
        for name,changed in [
            ('wrong_job',manifest.replace(b'323957',b'323958')),
            ('wrong_pin',manifest.replace(diag.PIN.encode(),b'0'*40)),
            ('wrong_reader_rc',manifest.replace(b'reader_restore_rc=2',b'reader_restore_rc=0')),
            ('duplicate_manifest_field',manifest+b'job=RJ\n'),
            ('failed_stage',manifest.replace(b'stage=G0 rc=0',b'stage=G0 rc=1')),
        ]:
            (job/'run_manifest.txt').write_bytes(changed)
            try:diag.bind_job(job,kit)
            except ValueError:outcomes.append({'case':name,'status':'REFUSED_AS_REQUIRED'})
            else:raise AssertionError(name)
        (job/'run_manifest.txt').write_bytes(manifest)
        for name,changed in [
            ('wrong_recorded_mismatch',verdict.replace(b'545583',b'545584')),
            ('duplicate_verdict_field',verdict.replace(b'"bed":',b'"bed":"ps_7_3_r45", "bed":',1)),
        ]:
            (job/'restore_verdict.json').write_bytes(changed)
            try:diag.bind_job(job,kit)
            except ValueError:outcomes.append({'case':name,'status':'REFUSED_AS_REQUIRED'})
            else:raise AssertionError(name)
        (job/'restore_verdict.json').write_bytes(verdict)
        for name in ['ul_lib.py','ul_gates.py','ul_reader.py','SHA256SUMS']:
            original=(kit/name).read_bytes();(kit/name).write_bytes(original+b'\n')
            try:diag.bind_job(job,kit)
            except ValueError:outcomes.append({'case':'changed_binding_'+name,'status':'REFUSED_AS_REQUIRED'})
            else:raise AssertionError(name)
            (kit/name).write_bytes(original)
    with tempfile.TemporaryDirectory(prefix='g2c-limits-') as td:
        large=Path(td)/'large.dump'
        large.write_bytes(b'x' * 10)
        with mock.patch.object(diag,'MAX_FILE_BYTES',5):
            try:list(diag.rows(large,{}))
            except ValueError:outcomes.append({'case':'file_cap_before_parse','status':'REFUSED_AS_REQUIRED'})
            else:raise AssertionError('file cap')
    fake=dict(n_orig=562605,n_test=562605,reproduced_pair_mismatches=1,discriminating_frac=1.0,
              provenance={},components=['MUST_NOT_LEAK'],families={},force_zero_sign={})
    with mock.patch.object(diag,'bind_job',return_value={}),mock.patch.object(diag,'analyze',return_value=fake):
        result=diag.main()
        assert 'components' not in result and 'families' not in result and 'force_zero_sign' not in result
        with contextlib.redirect_stdout(io.StringIO()) as output:
            rc=diag.cli()
        assert rc==2 and json.loads(output.getvalue())['diagnostic_status']=='PARITY_DISCREPANCY_NOT_A_VERDICT'
        outcomes.append({'case':'parity_discrepancy_suppresses_breakdown_and_rc2','status':'PASS'})
    print(json.dumps({'status':'PASS','checks':len(outcomes),'oracle_pin':diag.PIN,'oracle_sha256':EXPECTED,
                      'diagnostic_sha256':hashlib.sha256(Path(diag.__file__).read_bytes()).hexdigest(),
                      'scope':'small synthetic fixtures; no actual dump/probe/simulation', 'cases':outcomes},indent=2))

if __name__=='__main__':main()

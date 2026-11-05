"""Independent local, synthetic Q3/Q4 probes. Never modifies received bundle.

Preparation binding alone is explicitly mocked, matching the submitted 3-atom
fixture. Contact, cell_stats, raw readers and hash verification are real.
The callback in run_with_event schedules a filesystem change at _load's return;
it neither changes function results nor skips code under review.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest import mock

ROOT = Path(__file__).resolve().parent
RECEIVED = ROOT.parent / 'received'
PIN = 'uncommitted PRE8 fix; use received_source_sha256 for exact source identity'
FILES = ['mixer_precal_observe.py', 'test_mixer_precal_observe.py',
         'mixer_precal_prepare.py', 'mixer_contact_reader.py',
         'measure_mixing_index.py', 'measure_bed_aspect.py',
         'make_mixer_deck.py', 'mixer_deck_readback.py',
         'mixer_deck_diff.py', 'make_mixer_resume.py']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_fixture(scripts):
    spec = importlib.util.spec_from_file_location('review_fixture', scripts/'test_mixer_precal_observe.py')
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    return fixture


def compact(result):
    return dict(status=result['status'], reasons=result['reasons'],
                has_contact=result['contact'] is not None,
                has_mixing=result['mixing'] is not None,
                counts=result['counts'])


def run_with_event(O, fixture, run, B, callback=None):
    fired = []
    def profile(frame, event, arg):
        if event == 'return' and frame.f_code is O._load.__code__ and not fired:
            fired.append(True)
            callback()
    try:
        if callback:
            sys.setprofile(profile)
        return fixture.invoke(run, B)
    finally:
        sys.setprofile(None)


def main():
    before = {f:sha(RECEIVED/'scripts'/f) for f in FILES}
    results = dict(pin=PIN, python=sys.version,
                   mock_scope='validate_case only; no contact/cell_stats/hash/parser mocks',
                   received_source_sha256=before, probes={})
    with tempfile.TemporaryDirectory(prefix='q34_', dir=ROOT) as tmp:
        scripts = Path(tmp)/'scripts'
        scripts.mkdir()
        for f in FILES:
            shutil.copyfile(RECEIVED/'scripts'/f, scripts/f)
        F = load_fixture(scripts)
        O = F.O
        fixture = F.DiskContract()
        fixture.root = Path(tmp)/'runs'
        fixture.root.mkdir()

        run,B = fixture.make_run('control')
        result = run_with_event(O,fixture,run,B)
        assert result['status'] == 'OK', result
        results['probes']['control'] = compact(result)

        run,B = fixture.make_run('optional_file_created')
        result = run_with_event(O,fixture,run,B,lambda:(run/'n_expected').write_text('999\n'))
        record = compact(result)
        record.update(final_n_expected=(run/'n_expected').read_text().strip(),
                      n_expected_in_hashes=str(run/'n_expected') in result['provenance']['input_sha256'])
        results['probes']['optional_n_expected_created_after_load'] = record
        assert result['status'] == 'TECH' and result['contact'] is None and result['mixing'] is None, result
        # The same final files are refused without further modification.
        rerun = run_with_event(O,fixture,run,B)
        assert rerun['status'] == 'TECH', rerun
        results['probes']['same_files_next_invocation'] = compact(rerun)

        run,B = fixture.make_run('listing_changed')
        result = run_with_event(O,fixture,run,B,lambda:fixture.dump(run,201,F.data()))
        assert result['status'] == 'TECH' and result['contact'] is None, result
        results['probes']['post_listing_added_after_load'] = compact(result)

        mixing_path = scripts/'measure_mixing_index.py'
        original = mixing_path.read_bytes()
        run,B = fixture.make_run('dependency_changed_midrun')
        result = run_with_event(O,fixture,run,B,lambda:mixing_path.write_bytes(original+b'\n# probe mutation\n'))
        assert result['status'] == 'TECH' and result['contact'] is None, result
        results['probes']['dependency_changed_after_load'] = compact(result)
        mixing_path.write_bytes(original)

        # The interpreter has original cell_stats already loaded. Change only
        # its file before analyse_run's initial provenance capture.
        token = b"def cell_stats(D, r_container, cells=8, x_cells=2, n_min=20, axis='x'):\n"
        assert token in original
        replacement = token+b"    raise ValueError('Q34_STALE_MODULE_SENTINEL')\n"
        mixing_path.write_bytes(original.replace(token,replacement,1))
        run,B = fixture.make_run('stale_loaded_dependency')
        result = run_with_event(O,fixture,run,B)
        module_record = result['provenance']['module_sha256']['measure_mixing_index']
        results['probes']['dependency_changed_after_import_before_entry'] = dict(
            **compact(result), original_sha256=hashlib.sha256(original).hexdigest(),
            current_file_sha256=sha(mixing_path), recorded_sha256=module_record['sha256'],
            recorded_source_contains_raising_sentinel=False)
        assert result['status'] == 'TECH' and result['contact'] is None and result['mixing'] is None and module_record['sha256'] == hashlib.sha256(original).hexdigest() and module_record['sha256'] != sha(mixing_path), result

        # A fresh process loads the exact bytes claimed by the previous result.
        child = """import importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('fresh',Path(sys.argv[1])/'test_mixer_precal_observe.py')
F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
fixture=F.DiskContract();run=Path(sys.argv[2]);B=json.loads((run/'deck_meta.json').read_text())
result=fixture.invoke(run,B)
print(json.dumps(dict(status=result['status'],reasons=result['reasons'],has_contact=result['contact'] is not None,has_mixing=result['mixing'] is not None)))
"""
        p = subprocess.run([sys.executable,'-I','-X','utf8','-B','-c',child,str(scripts),str(run)],capture_output=True,text=True,check=True)
        fresh = json.loads(p.stdout)
        assert fresh['status'] == 'TECH' and fresh['reasons'] == ['Q34_STALE_MODULE_SENTINEL'], fresh
        results['probes']['fresh_process_same_recorded_source'] = fresh
        mixing_path.write_bytes(original)

        # Direct qualification counters and preserved inventory; input order is
        # immaterial, while a per-ID reassignment must be refused.
        D = F.data(3)
        shuffled = {k:v[[2,0,1]] for k,v in D.items()}
        got = O.qualify_arrays([D,shuffled],F.binding(13))
        assert got['initial_missing'] == 10 and got['observed_by_type'] == {'1':1,'2':1,'3':1}
        results['probes']['D13_reordered_same_inventory_at_missing10'] = got
        changed = {k:v.copy() for k,v in D.items()}
        changed['type'] = changed['type'][[1,0,2]]
        try:
            O.qualify_arrays([D,changed],F.binding())
        except O.Tech as e:
            results['probes']['D13_same_totals_changed_ID_type'] = dict(status='TECH',reason=str(e))
        else:
            raise AssertionError('per-ID type reassignment not refused')
    results['received_unchanged'] = before == {f:sha(RECEIVED/'scripts'/f) for f in FILES}
    assert results['received_unchanged']
    (ROOT/'probe_results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()

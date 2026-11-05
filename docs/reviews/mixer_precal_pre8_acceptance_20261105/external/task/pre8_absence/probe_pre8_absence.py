"""Independent PRE8-01 recheck; synthetic files only, received bundle immutable.

Run using Python -I -B -X utf8. A profiler injects filesystem events when real
functions return; no observer/parser/metric/hash result is mocked. Only the
submitted unit fixture's validate_case boundary remains explicitly mocked.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import platform
import shutil
import sys
import tempfile

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent.parent / 'input'
PIN = 'ec484c2719d6a444214ddc9c48fe683a7735688b'
NAMES = ('mixer_precal_observe', 'test_mixer_precal_observe',
         'mixer_precal_prepare', 'mixer_contact_reader', 'measure_mixing_index',
         'measure_bed_aspect', 'make_mixer_deck', 'mixer_deck_readback',
         'mixer_deck_diff', 'make_mixer_resume')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert (INPUT / 'PIN.txt').read_text().strip() == PIN
    scratch = HERE / 'scratch'
    scratch.mkdir(exist_ok=True)
    tempfile.tempdir = str(scratch)
    before = {n: sha(INPUT / 'scripts' / (n+'.py')) for n in NAMES}
    out = dict(pin=PIN, python=sys.version, platform=platform.platform(),
               isolated=sys.flags.isolated, dont_write_bytecode=sys.dont_write_bytecode,
               received_source_sha256=before,
               scope='Synthetic PRE8-01 filesystem binding only; no DEM/host/fullgate/research',
               mock_scope='validate_case only via submitted DiskContract.invoke; all metrics/readers/hash checks real',
               event_injection='sys.setprofile on real _load, contact.frame_quantities, mixing.cell_stats return; no result replacement',
               cases=[], skipped=[])
    with tempfile.TemporaryDirectory(prefix='pre8_') as tmp:
        root = Path(tmp)
        scripts = root/'scripts'; scripts.mkdir()
        for n in NAMES:
            shutil.copyfile(INPUT/'scripts'/(n+'.py'), scripts/(n+'.py'))
        sys.path.insert(0, str(scripts))
        spec = importlib.util.spec_from_file_location('review_fixture', scripts/'test_mixer_precal_observe.py')
        F = importlib.util.module_from_spec(spec); spec.loader.exec_module(F)
        O = F.O
        import numpy as np
        import scipy
        out['numpy'] = np.__version__; out['scipy'] = scipy.__version__
        fixture = F.DiskContract(); fixture.root = root/'runs'; fixture.root.mkdir()
        link = root/'link_capability'
        try:
            link.symlink_to(root/'does_not_exist')
            assert link.is_symlink() and not link.exists()
            link.unlink()
            symlink_ok = True
            out['symlink_capability'] = 'available; actual dangling symlink cases executed'
        except OSError as exc:
            symlink_ok = False
            out['symlink_capability'] = dict(status='unavailable', error=str(exc), winerror=getattr(exc,'winerror',None))

        def data48(mixed):
            D = F.data(48)
            # Two 24-atom cells for each configured grid, at x=0. In own t0
            # both AM atoms share cell A; in reference/later they split 1/1.
            D['x'][:] = 0.; D['z'][:] = .19
            D['y'][:24] = -.27; D['y'][24:] = .27
            if mixed:
                D['y'][1], D['y'][24] = D['y'][24], D['y'][1]
            # Spread within cells without changing bins or atom identity.
            for indices in (np.flatnonzero(D['y'] < 0),np.flatnonzero(D['y'] > 0)):
                D['y'][indices] += np.arange(len(indices)) * .0001
            return D

        def setup(tag, context, initial='absent'):
            if context == 'e0':
                run,B = fixture.make_run(tag)
                ref = None; target = run
            else:
                run,B = fixture.make_run(tag+'_u','U',48)
                ref,R = fixture.make_run(tag+'_ref','E0',48)
                fixture.dump(run,200,data48(False))
                for step in (400,450,500,550): fixture.dump(run,step,data48(True))
                fixture.dump(ref,200,data48(True))
                target = run if context == 'rotating_run' else ref
            ne = target/'n_expected'
            if initial == 'valid': ne.write_text(str(B['n_planned'])+'\n')
            elif initial == 'wrong': ne.write_text('999\n')
            elif initial == 'dangling_symlink': ne.symlink_to(target/'missing_target')
            return run,B,ref,target

        def record(tag,context,when='none',action='none',initial='absent',want='TECH',reuse=None):
            if 'symlink' in action or 'symlink' in initial:
                if not symlink_ok:
                    out['skipped'].append(dict(name=tag,reason='OS symlink privilege unavailable'))
                    return
            run,B,ref,target=setup(tag,context,initial) if reuse is None else reuse
            path=target/'n_expected'
            fired=[]; metric_calls=[]
            def mutate():
                if action == 'create_valid': path.write_text(str(B['n_planned'])+'\n')
                elif action == 'create_wrong': path.write_text('999\n')
                elif action == 'create_dangling_symlink': path.symlink_to(target/'missing_target')
                elif action == 'delete': path.unlink()
                elif action == 'rewrite_wrong': path.write_text('999\n')
                elif action == 'rewrite_valid_format': path.write_text(str(B['n_planned'])+'  \n')
                elif action in ('replace_changed_bytes','replace_same_bytes'):
                    raw=path.read_bytes()
                    replacement=target/'replacement.tmp'
                    replacement.write_bytes(raw if action == 'replace_same_bytes' else raw+b' ')
                    replacement.replace(path)
                elif action == 'replace_dangling_symlink':
                    path.unlink(); path.symlink_to(target/'missing_target')
                elif action == 'unrelated_file': (target/'unrelated_review_note.txt').write_text('unrelated')
                else: raise AssertionError(action)
            def profile(frame,event,arg):
                if event != 'return': return
                if frame.f_code in (O.contact.frame_quantities.__code__,O.mixing.cell_stats.__code__):
                    metric_calls.append(frame.f_code.co_name)
                if fired or when == 'none': return
                hit = (when == 'after_load' and frame.f_code is O._load.__code__
                       and Path(frame.f_locals['directory']) == target)
                hit |= when == 'contact_return' and frame.f_code is O.contact.frame_quantities.__code__
                hit |= when == 'mixing_return' and frame.f_code is O.mixing.cell_stats.__code__
                if hit:
                    fired.append(dict(function=frame.f_code.co_name,line=frame.f_lineno))
                    mutate()
            try:
                sys.setprofile(profile)
                result=fixture.invoke(run,B,ref)
            finally: sys.setprofile(None)
            got=dict(name=tag,context=context,timing=when,action=action,initial=initial,
                     expected=want,status=result['status'],reasons=result['reasons'],
                     contact_present=result['contact'] is not None,mixing_present=result['mixing'] is not None,
                     counts=result['counts'],reference_counts=result['reference_counts'],
                     events=fired,metric_call_count=len(metric_calls),
                     n_expected_in_hashes=str(path) in result['provenance']['input_sha256'],
                     snapshot_present=result['provenance']['optional_presence_snapshot'].get(str(path)),
                     final_present=O._present(path))
            if result['status'] == 'OK' and context != 'e0':
                got['grids']=[dict(grid=g['grid'],S0=g['S0'],SR=g['SR'],M_mean=g['M_mean']) for g in result['mixing']['grids']]
            got['pass'] = result['status'] == want and (when == 'none' or len(fired) == 1)
            if want == 'TECH':
                got['pass'] &= all(result[k] is None for k in ('contact','mixing','counts','reference_counts'))
            else:
                got['pass'] &= all(result[k] is not None for k in ('contact','mixing','counts'))
            out['cases'].append(got)
            return result

        # Exact previous external 3-atom event, followed by unchanged-file rerun.
        original_tag = 'original_3atom_create999_after_load'
        record(original_tag,'e0','after_load','create_wrong')
        original_run = fixture.root/original_tag
        record('original_3atom_same_final_files_next_invocation','e0',initial='wrong',
               reuse=(original_run,F.binding(),None,original_run))
        for context in ('e0','rotating_run','rotating_reference'):
            for initial in ('absent','valid','wrong','dangling_symlink'):
                record(context+'_initial_'+initial,context,initial=initial,
                       want='OK' if initial in ('absent','valid') else 'TECH')
            for when in ('after_load','contact_return','mixing_return'):
                for action in ('create_valid','create_wrong','create_dangling_symlink'):
                    record(context+'_'+when+'_'+action,context,when,action)
                for action in ('delete','rewrite_wrong','rewrite_valid_format','replace_changed_bytes','replace_dangling_symlink'):
                    record(context+'_'+when+'_'+action,context,when,action,initial='valid')
            # Original review requested content hashes for previously present files.
            # A same-byte regular-file replacement remains the same bound input.
            record(context+'_same_bytes_replacement_boundary',context,'contact_return','replace_same_bytes',initial='valid',want='OK')
            record(context+'_unrelated_file_boundary',context,'contact_return','unrelated_file',want='OK')
    out['received_unchanged'] = before == {n:sha(INPUT/'scripts'/(n+'.py')) for n in NAMES}
    out['executed_count'] = len(out['cases'])
    out['passed_count'] = sum(c['pass'] for c in out['cases'])
    out['skipped_count'] = len(out['skipped'])
    out['all_passed'] = out['received_unchanged'] and all(c['pass'] for c in out['cases'])
    (HERE/'probe_results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({k:out[k] for k in ('pin','python','numpy','scipy','executed_count','passed_count','skipped_count','received_unchanged','all_passed','symlink_capability')},indent=2))
    if not out['all_passed']:
        print(json.dumps([c for c in out['cases'] if not c['pass']],indent=2,ensure_ascii=False))
        raise SystemExit(1)


if __name__ == '__main__': main()

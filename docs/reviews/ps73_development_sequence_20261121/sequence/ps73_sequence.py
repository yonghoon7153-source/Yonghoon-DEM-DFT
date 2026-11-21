"""Read-only development progression for the single registered 7:3 bed.

CLI: python3 -I -B ps73_sequence.py WORK_ROOT SEALED_KIT RECEIPTS.json
RECEIPTS is an arm-keyed map from the controller (scheduler + worker records).
There is no submit, cancel, resume, overwrite or publication command here.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import re
import sys
from pathlib import Path, PurePosixPath

BED = 'ps_7_3_r45'
KIT_SUM = '26bdbdc05ba3f6c71a0b042ebd13adb64b38271c1889a894898a4ccf55322f1d'
ORIGIN = {
    'RJ/run_manifest.txt': 'd4647c1654acf8d225b2b24f64c5e0d8246328f299c057ff3c033b6e6944b5e1',
    'RJ/restore_verdict.json': 'b049a3707aede899f4c6badc7176eb63246da8986dea58459dbea4aae45e73e6',
    'ul_base.in': '016f0402edba632864ef0a0423a5aaf8360a7eac2054e0b5b4191917648ce272',
}
ARMS = ('UB', 'UT', 'UC', 'UVa', 'UVb', 'UTc')
CHOICES = {'t1':'UB', 't2':'UVa', 't3':'UT3', 't4':'UVb'}
GRAVITY = {'G_' + name for name in CHOICES.values()}


class Halt(Exception):
    """Contains only a fixed machine-readable reason, never file text."""


def require(check, reason):
    if not check:
        raise Halt(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = dict(pairs)
    require(len(pairs) == len(result), 'DUPLICATE_JSON_KEY')
    return result


def json_read(raw):
    return json.loads(raw, object_pairs_hook=unique)


def regular(path):
    require(path.is_file() and not path.is_symlink(), 'REQUIRED_REGULAR_FILE_MISSING')
    return path.read_bytes()


def receipt(folder, arm, info):
    require(isinstance(info, dict) and info.get('arm') == arm, 'WRONG_RECEIPT')
    number = str(info.get('job_id'))
    require(re.fullmatch(r'[1-9][0-9]*', number) and info.get('state') == 'COMPLETED'
            and info.get('exit_code') == '0:0' and type(info.get('runner_rc')) is int
            and info['runner_rc'] == 0 and info.get('technical_ok') is True, 'JOB_NOT_SUCCESSFUL')
    manifest = regular(folder / 'run_manifest.txt')
    verdict = regular(folder / 'arm_verdict.json')
    require(digest(manifest) == info.get('manifest_sha256')
            and digest(verdict) == info.get('verdict_sha256'), 'JOB_OUTPUT_IDENTITY_CHANGED')
    lines = manifest.decode('utf-8').splitlines()
    for field, value in [('job',arm), ('bed',BED), ('reader_arm_rc','0')]:
        require([line for line in lines if line.startswith(field+'=')] == [field+'='+value], 'MANIFEST_FIELD')
    slurm = [line.split() for line in lines if line.startswith('slurm_job=')]
    require(len(slurm) == 1 and slurm[0][0] == 'slurm_job='+number and slurm[0].count('slurm_ntasks=6') == 1,
            'MANIFEST_JOB_ID')
    endings = [line for line in lines if line.startswith('end=')]
    require(len(endings) == 1 and lines[-1] == endings[0]
            and re.fullmatch(r'end=\S+ fails=0 reader_rc=0', endings[0]), 'INCOMPLETE_MANIFEST')
    data = json_read(verdict)
    require(isinstance(data, dict) and data.get('job') == arm and data.get('bed') == BED, 'WRONG_SAVED_VERDICT')
    return data


def control_ok(run, params):
    """UC is a stationary control. Do not require a crossing from a stationary plate."""
    spec = params['beds'][BED]
    first, period = spec['s0'], params['windows']['W0']
    span = params['windows']['uc_steps_dt0']
    last = first + span
    summary = run.get('summary') or {}
    if (span % period or run.get('problems') or run.get('steps')
            or (summary.get('arm'), summary.get('bed'), summary.get('result'), summary.get('step'))
            != ('UC', BED, 'DONE', str(last))):
        return False
    if [(e.get('event'), e.get('step')) for e in run['events']] != [('START',first), ('NOMOVE_DONE',last)]:
        return False
    rows = run['windows']
    if len(rows) != span // period:
        return False
    for i, w in enumerate(rows, 1):
        if (w.get('arm'),w.get('bed'),w.get('k'),w.get('phase'),w.get('w'),w.get('step')) != (
                'UC',BED,0,4,i,first + i*period):
            return False
        if (w.get('lift') != 0.0 or w.get('plate_z') is None or not math.isfinite(w['plate_z'])
                or abs(w['plate_z']-spec['h0']) > 1e-12):
            return False
        for key in ('Ps_avg', 'ke_tr_avg', 'ke_rot_avg'):
            if w.get(key) is None or not math.isfinite(w[key]):
                return False
    return True


def verify_kit(kit):
    raw = regular(kit / 'A5_SHA256SUMS')
    require(digest(raw) == KIT_SUM, 'WRONG_KIT')
    for line in raw.decode('ascii').splitlines():
        expected, name = line.split('  ', 1)
        local = PurePosixPath(name)
        require(not local.is_absolute() and '..' not in local.parts, 'INVALID_KIT_MEMBER')
        require(digest(regular(kit / name)) == expected, 'KIT_FILE_CHANGED')


class Originals:
    def __init__(self, root, kit, receipts):
        self.root, self.kit = Path(root).resolve(), Path(kit).resolve()
        self.bed = self.root / BED
        require(self.bed.is_dir() and not self.bed.is_symlink(), 'BED_MISSING')
        verify_kit(self.kit)
        for name, expected in ORIGIN.items():
            require(digest(regular(self.bed / name)) == expected, 'RJ_OR_BASELINE_CHANGED')
        # A dedicated fresh process is used by the site controller. Fail closed if
        # a caller already imported a dependency from a different kit.
        modules = {p.stem for p in self.kit.glob('*.py')}
        for name in modules.intersection(sys.modules):
            source = getattr(sys.modules[name], '__file__', None)
            require(source is not None and Path(source).resolve() == self.kit / (name+'.py'), 'MIXED_READER')
        sys.path.insert(0, str(self.kit))
        spec = importlib.util.spec_from_file_location('ps73_a5_adapter', str(self.kit / 'rt_restore_a5.py'))
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        require(adapter.job_restored(self.root,BED,'RJ',self.kit), 'A5_ADMISSION_FAILED')
        self.old = adapter.legacy_reader(self.kit)
        self.params = self.old.ul_lib.load_params(str(self.kit / 'unload_params.json'))
        # Same substitution as the sealed rt_dispatch_a5 gate.
        self.old._job_restored = lambda root, bed, job: (adapter.job_restored(root,bed,job,self.kit),'A5 admission')
        # Reuse each on-site reread within this single decision, including when
        # the frozen selection_state, gate and t3 report consult the same arm.
        self.cache = {}
        read = self.old._arm_v
        def read_once(root, bed, job, params):
            require(Path(root) == self.root and bed == BED and params is self.params, 'READER_CONTEXT')
            if job not in self.cache:
                self.cache[job] = read(str(root),bed,job,params)
            return self.cache[job]
        self.old._arm_v = read_once
        self.receipts = receipts
        require(isinstance(receipts,dict), 'INVALID_RECEIPTS')
        names = set(ARMS) | GRAVITY | {'UT3'}
        self.present = {p.name for p in self.bed.iterdir() if p.name in names}
        for child in self.bed.iterdir():
            # Old/renamed job directories preserve real attempts. Their existence
            # needs explicit disposition before creating any arm with that name.
            if child.is_dir() and any(child.name.startswith(a+'_') or child.name.startswith(a+'.') for a in names):
                raise Halt('PRIOR_ATTEMPT_NEEDS_REVIEW')
            if child.name.endswith('.report.tgz') and child.name[:-11] in names:
                require(child.name[:-11] in self.present,'ORPHAN_ARM_REPORT')
        require(self.present == set(receipts), 'UNRECEIPTED_OR_MISSING_ARM')
        ids = [str(r.get('job_id')) for r in receipts.values() if isinstance(r,dict)]
        require(len(set(ids)) == len(receipts), 'DUPLICATE_OR_MISSING_JOB_ID')

    def check_arm(self, arm):
        d = self.bed / arm
        require(d.is_dir() and not d.is_symlink(), 'ARM_DIRECTORY')
        saved = receipt(d,arm,self.receipts[arm])
        v = self.old._arm_v(str(self.root),BED,arm,self.params)
        require(isinstance(v,dict) and v.get('job') == arm and v.get('bed') == BED, 'ORIGINAL_REREAD_FAILED')
        require(all(v.get(k) == saved.get(k) for k in ('primary_status','rho_pct','trajectory_status')),
                'SAVED_AND_REREAD_DISAGREE')
        require(not v.get('resume_tail'), 'AMBIGUOUS_ATTEMPT')
        if arm == 'UC':
            require(control_ok(self.old.read_run(str(d), self.params),self.params), 'INCOMPLETE_NO_MOVE_CONTROL')
        else:
            require(self.old._valid_rho(v), 'REGISTERED_ENDPOINT_INVALID')
            if arm != 'UTc':
                events, problems = self.old._csv(str(d / 'ul_events.csv'), self.params['records']['events_cols'])
                require(not problems and events, 'ENDPOINT_EVENTS_MISSING')
                marks = [e['event'] for e in events]
                require(marks[0] == 'START' and all(marks.count(m) == 1 for m in ('START','CROSS','RM'))
                        and marks.index('CROSS') < marks.index('RM')
                        and 'RESUME' not in marks and 'GUARD' not in marks, 'ENDPOINT_EVENTS_INCOMPLETE')
            # A retained primary endpoint can legitimately coexist with an
            # incomplete post-separation trajectory (§13-2). A technical abort
            # or undocumented stop is never a completed arm for auto-progression.
            summary = self.old.ul_lib.read_kv(str(d / 'ul_summary.txt'))
            allowed = {'DONE', 'SEP_INCOMPLETE', 'LIFT_CAP'}
            if arm == 'UT':
                allowed.add('RM_STOP')
            require(summary.get('result') in allowed, 'RUN_NOT_COMPLETED')

    def allows(self, arm):
        ok, _ = self.old.gate(str(self.root),BED,arm,self.params)
        return ok is True

    def rm_pair(self, arm):
        run = self.old.read_run(str(self.bed / arm),self.params)
        rm = [e.get('step') for e in run['events'] if e.get('event') == 'RM']
        if len(rm) != 1 or type(rm[0]) is not int or rm[0] < 0:
            return False
        folder = self.bed / arm / 'restart'
        files = list(folder.glob('restart_RM_*.bin'))
        state = folder / ('state_RM_%d.in' % rm[0])
        return (len(files) == 1 and files[0].name == 'restart_RM_%d.bin' % rm[0]
                and all(f.is_file() and not f.is_symlink() and f.stat().st_size > 0 for f in (files[0],state)))

    def selection(self):
        return self.old.selection_state(str(self.root),self.params)

    def combined_ok(self):
        entry = self.old._t3_entry(str(self.root),self.params)
        return bool(entry and entry.get('primary_source') == 'UT' and entry.get('aux_source') == 'UTc')


def result(status, reason, completed, arm=None, row=None):
    return {'status':status, 'reason':reason, 'next_arm':arm, 'tuple':row,
            'completed':list(completed)}


def plan(state):
    done = []
    def step(arm, row=None):
        if arm in state.present:
            state.check_arm(arm)
            done.append(arm)
            return None
        require(set(done) == state.present, 'OUT_OF_ORDER_OR_UNREGISTERED_ARM')
        require(state.allows(arm), 'REGISTERED_GATE_REFUSED')
        return result('READY','REGISTERED_NEXT_ARM',done,arm,row)
    try:
        for arm in ('UB','UT','UC'):
            ready = step(arm)
            if ready:
                return ready
        selection = state.selection()
        if selection.get('stage') == 'need_UV':
            require(selection.get('next') in (['UVa'],['UVb']), 'AMBIGUOUS_UV')
            arm = selection['next'][0]
            require(arm not in state.present, 'UNUSABLE_UV_OUTPUT')
            return step(arm)
        require(selection.get('stage') == 'resolved', 'SELECTION_UNRESOLVED')
        row = selection.get('tuple')
        require(row in CHOICES and selection.get('arm') == CHOICES[row], 'INVALID_SELECTION_ROW')
        uv = 'UVa' if row in ('t1','t2') else 'UVb'
        require(uv in state.present, 'SELECTED_UV_MISSING')
        step(uv)
        if row == 't3':
            require(state.rm_pair('UT'), 'UT_RM_PAIR_UNAVAILABLE')
            ready = step('UTc',row)
            if ready:
                return ready
            require(state.combined_ok(), 'UT_PARENT_AUXILIARY_MISMATCH')
        require(set(done) == state.present, 'OUT_OF_ORDER_OR_UNREGISTERED_ARM')
        report = result('REVIEW','PS73_PRIMARY_REVIEW',done,row=row)
        report.update(gravity_status='DEFERRED_C12_AMENDMENT', gravity_candidate='G_'+CHOICES[row],
                      gravity_parent='UT' if row == 't3' else CHOICES[row])
        return report
    except Halt as e:
        return result('STOP',str(e),done)


def recommend(root, kit, receipts):
    try:
        return plan(Originals(root,kit,receipts))
    except Halt as e:
        return result('STOP',str(e),[])
    except (OSError, ValueError, TypeError, KeyError, IndexError, AttributeError, ImportError, OverflowError, RuntimeError):
        return result('STOP','ORIGINAL_REREAD_OR_INPUT_ERROR',[])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    parser.add_argument('kit',type=Path)
    parser.add_argument('receipts',type=Path)
    args = parser.parse_args()
    try:
        out = recommend(args.root,args.kit,json_read(regular(args.receipts)))
    except (OSError,ValueError,Halt):
        out = result('STOP','INVALID_RECEIPTS',[])
    print(json.dumps(out,ensure_ascii=True,allow_nan=False))
    return 2 if out['status'] == 'STOP' else 0


if __name__ == '__main__':
    sys.exit(main())

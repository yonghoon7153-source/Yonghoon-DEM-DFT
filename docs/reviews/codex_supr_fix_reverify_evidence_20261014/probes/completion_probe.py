"""Offline SUPR-02 receipt boundary probes; production/raw OS checks mocked only.

Run with bundled python -X utf8 -B. Outputs live outside source/.
"""
import contextlib
import copy
import hashlib
import io
import json
import sys
from pathlib import Path
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'source' / 'scripts'))
import supp20_input_receipt as S

NP = S.NP
PIN = 'df647d4e31224e1a270dae01dd41f91af3048361'
OUT = BASE / 'evidence' / 'completion_probe'
OUT.mkdir(parents=True, exist_ok=True)
RESULTS = []


def git_clean():
    return dict(sha=PIN, short=PIN[:9], branch='HEAD', dirty=False, porcelain=[])


def fake_preflight(args, plan, root, budget):
    """Only environmental preflight evidence is synthetic; real plan/digest/output/receipt."""
    obs = NP.production_observation_problem(dict(plan=plan, observe_imports=args.observe_imports))
    return dict(cpu=dict(cpu_count=20, cpu_affinity=20),
                mem=dict(MemTotal_GB=128, MemAvailable_GB=120, SwapFree_GB=0, SwapTotal_GB=0),
                lanes=args.lanes, mem_budget_mb=120 * 1024,
                first_lanes_est_mem_GB=1, est_mem_largest_mb=1024,
                disk_free_GB=1000, disk_need_GB=1, est_serial_h=1, est_makespan_h=0.1,
                git=git_clean(), n_raw_problems=0, raw_problems=[], warn=[], stop=[obs] if obs else [],
                generation=dict(generation=NP.CURRENT_GENERATION, problems=[], modes={}, error=''),
                dependency_closure=dict(files=list(NP.CODE_FILES), errors=[]),
                lazy_census=dict(n_lazy=0, unclassified=[], stale=[]), fork_census=[],
                input_digest=NP.plan_input_digest(plan))


def run(tag, observe=True, extra=(), pf_edit=None, after_error=None):
    folder = OUT / tag
    folder.mkdir(exist_ok=True)
    rp = folder / 'receipt.json'
    if rp.exists():
        raise RuntimeError(f'Preserve evidence; use a fresh output directory: {rp}')
    argv = ['run', '--root', str(folder / 'unused_root'), '--cohorts', 'lhss', '--dry-run',
            *(['--observe-imports'] if observe else []), '--preflight-receipt', str(rp), *extra]
    screen = io.StringIO()
    cmd_run = NP.cmd_run

    def pf(*a, **k):
        value = fake_preflight(*a, **k)
        if pf_edit:
            pf_edit(value)
        return value

    def command(*a, **k):
        rc = cmd_run(*a, **k)
        if after_error:
            raise after_error('synthetic exception after completion marker')
        return rc

    raised = None
    with patch.object(NP, '_guard_posix', lambda: None), patch.object(NP, 'preflight', pf), \
         patch.object(NP, 'git_info', git_clean), patch.object(NP, 'meminfo', lambda: {}), \
         patch.object(NP, 'cmd_run', command), contextlib.redirect_stdout(screen), contextlib.redirect_stderr(screen):
        try:
            rc = NP.main(argv)
        except BaseException as ex:
            raised = type(ex).__name__
            rc = None
    (folder / 'screen.log').write_bytes(screen.getvalue().encode('utf-8'))
    return rp, dict(producer_rc=rc, raised=raised, root_created=(folder / 'unused_root').exists())


def check(tag, rp, expect_bad=None, integration=False, extra=None):
    try:
        value = NP.preflight_receipt_checks(rp, expect_set='supp20', approved_sha=PIN)
        bad = sorted(c['id'] for c in value['checks'] if not c['ok'])
        row = dict(tag=tag, bad=bad, passed=not bad, expected_bad=expect_bad,
                   expected=expect_bad is None or set(bad) == set(expect_bad))
        if integration:
            result = S.receipt(preflight_receipt=str(rp), approved_sha=PIN)
            row.update(integration_rc=result['rc'], integration_bad=sorted(c['id'] for c in result['checks'] if not c['ok']))
    except BaseException as ex:
        row = dict(tag=tag, verifier_exception=f'{type(ex).__name__}: {ex}', expected=False)
    row.update(extra or {})
    RESULTS.append(row)
    return row


def mutate(src, tag, edit_record=None, edit_log=None, bind=True, alternate_bytes=None):
    folder = OUT / tag
    folder.mkdir(exist_ok=True)
    record = json.loads(src.read_text(encoding='utf-8'))
    data = Path(record['log']['path']).read_bytes()
    if edit_log:
        data = edit_log(data.decode('utf-8')).encode('utf-8')
    if alternate_bytes is not None:
        data = alternate_bytes
    lp = folder / 'receipt.log'
    lp.write_bytes(data)
    record['log']['path'] = str(lp)
    if bind:
        record['log'].update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    if edit_record:
        edit_record(record)
    rp = folder / 'receipt.json'
    rp.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    return rp


def run_all():
    normal, info = run('normal')
    check('normal', normal, [], integration=True, extra=info)
    for tag, ed, bad in [
        ('completed_false', lambda r: r.update(completed=False), ['P3']),
        ('completed_missing', lambda r: r.pop('completed'), ['P3']),
        ('completed_integer', lambda r: r.update(completed=1), ['P3']),
        ('exit_false', lambda r: r.update(exit_code=False), ['P3']),
        ('exit_string', lambda r: r.update(exit_code='0'), ['P3']),
        ('exit_float', lambda r: r.update(exit_code=0.0), ['P3']),
        ('exit_nonzero', lambda r: r.update(exit_code=2), ['P3']),
        ('exit_missing', lambda r: r.pop('exit_code'), ['P3']),
        ('exception', lambda r: r.update(exception='RuntimeError: x'), ['P3']),
        ('stop', lambda r: r.update(stop=['blocked']), ['P3']),
        ('stop_missing', lambda r: r.pop('stop'), ['P3']),
        ('aborted', lambda r: r.update(aborted='blocked'), ['P3']),
        ('observe_record_false', lambda r: r.update(observe_imports=False), ['P4']),
        ('observe_args_false', lambda r: r['args'].update(observe_imports=False), ['P4', 'P6']),
        ('argv_remove_observe', lambda r: r['argv'].remove('--observe-imports'), ['P4', 'P6']),
        ('check_ok_integer', lambda r: r['checks']['fork_census'].update(ok=1), ['P5']),
        ('check_missing', lambda r: r['checks'].pop('dependency_closure'), ['P5']),
        ('runner_metadata_missing', lambda r: r.pop('runner'), []),
        ('runner_hash_changed', lambda r: r['runner'].update(sha256='0'*64), []),
    ]:
        check(tag, mutate(normal, tag, ed), bad)
    marker = NP.PREFLIGHT_COMPLETE_MARK
    drop_marker = lambda t: t[:t.index(marker)]
    drop_ticks = lambda t: '\n'.join(ln for ln in t.split('\n') if not any(ln.strip().startswith(lbl) for _, lbl in NP.PREFLIGHT_TICKS))
    for tag, edit, bind, bad in [
        ('truncated_marker_unbound', drop_marker, False, ['P1', 'P3']),
        ('truncated_marker_rebound', drop_marker, True, ['P3']),
        ('missing_prereq_unbound', drop_ticks, False, ['P1', 'P5']),
        ('missing_prereq_rebound', drop_ticks, True, ['P5']),
        ('duplicate_marker', lambda t: t + marker + '\n', True, ['P3']),
        ('after_marker', lambda t: t + 'unconsumed result\n', True, ['P3']),
        ('missing_digest', lambda t: '\n'.join(ln for ln in t.split('\n') if NP.INPUT_DIGEST_LINE not in ln), True, ['P2']),
        ('log_stop', lambda t: t.replace(marker, '⛔ synthetic stop\n' + marker), True, ['P3']),
        ('log_append_unbound', lambda t: t + ' ', False, ['P1']),
    ]:
        check(tag, mutate(normal, tag, edit_log=edit, bind=bind), bad, integration=tag in ('truncated_marker_rebound', 'missing_prereq_rebound'))
    off, info = run('observation_off', observe=False)
    check('observation_off', off, ['P3', 'P4'], integration=True, extra=info)
    cut_stop = lambda t: '\n'.join(t.split('\n')[:next(i for i, ln in enumerate(t.split('\n')) if '⛔' in ln)]) + '\n'
    check('off_truncated_prefix', mutate(off, 'off_truncated_prefix', edit_log=cut_stop), ['P3', 'P4'])
    for key in ('dependency_closure', 'lazy_census', 'fork_census'):
        tag = 'producer_missing_' + key
        rp, info = run(tag, pf_edit=lambda p, k=key: p.pop(k))
        check(tag, rp, ['P5'], extra=info)
    for error in (RuntimeError, KeyboardInterrupt, SystemExit):
        tag = 'exception_after_marker_' + error.__name__
        rp, info = run(tag, after_error=error)
        check(tag, rp, ['P3'], extra=info)
    rp, info = run('launch_error', extra=['--cohorts', 'unknown'])
    check('launch_error', rp, extra=info)
    # A relocated original pair remains usable after the original absolute path disappears.
    moved = mutate(normal, 'relocated', edit_record=lambda r: r['log'].update(path='/original/host/receipt.log'))
    check('relocated_pair', moved, [])
    # All receipt-only fields claimed as run data should be preserved by the producer.
    record = json.loads(normal.read_text(encoding='utf-8'))
    RESULTS.append(dict(tag='producer_required_fields', expected=all(k in record for k in
        ('runner', 'argv', 'args', 'root', 'git', 'input_digest', 'checks', 'completed', 'exit_code', 'log', 'started', 'ended')),
        runner_sha256=record['runner']['sha256'], captured_end=Path(record['log']['path']).read_text(encoding='utf-8').splitlines()[-1]))
    (OUT / 'results.json').write_text(json.dumps(dict(pin=PIN, environment='Windows exported source; synthetic preflight environment; real plan/digest/print/receipt/verifier',
        cases=RESULTS), ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(dict(cases=len(RESULTS), unexpected=[r for r in RESULTS if not r.get('expected')], results=str(OUT / 'results.json')), ensure_ascii=False))
    for row in RESULTS:
        print(row['tag'], row.get('bad'), row.get('producer_rc'), row.get('raised'), row.get('integration_rc'))


if __name__ == '__main__':
    run_all()

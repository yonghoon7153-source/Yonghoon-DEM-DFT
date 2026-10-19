"""Independent L214R consumer seam tests; small synthetic fixtures only.

Uses the submitted release fixture helpers (all nonselected rows/audit synthetic).
One row comes from the actual producer/publisher/P0-P4 chain retained by the
documented old-probe derivative. The real build/check/re-read functions run.
The source provision adapter supplies synthetic unselected rows; selected row
is read anew by original load_tau_results on every requested build re-read.
No production data, source files, Git state, or approval records are altered.
"""
from pathlib import Path
import ast
import atexit
import contextlib
import copy
import csv
import hashlib
import io
import json
import logging
import os
import shutil
import sys
import time

REVIEW = Path(__file__).resolve().parents[1]
WS = REVIEW.parent
SOURCE = REVIEW / 'source'
EV = REVIEW / 'evidence'
for p in (WS / 'lhs_coverage_review_20260930/deps', WS / 'gen2_network_reverify3_20261007/deps', SOURCE / 'scripts', SOURCE / 'webapp'):
    sys.path.insert(0, str(p))
os.environ['PYTHONPATH'] = os.pathsep.join([str(WS / 'lhs_coverage_review_20260930/deps'), str(WS / 'gen2_network_reverify3_20261007/deps')])
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '1'
os.environ['TMP'] = os.environ['TEMP'] = str(REVIEW / 'tmp')
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'

import tau_flux as tf
import lhs_release_build as RB
import lhs_design_dataset as DD
import pipeline_service as ps
import g2_network_reread as RR

ROOT = EV / ('consumer_adversarial_' + str(time.time_ns()))
ROOT.mkdir()
logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def save(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding='utf-8')

def call(fn, *args, **kw):
    try:
        return dict(value=fn(*args, **kw), exception=None)
    except Exception as e:
        return dict(value=None, exception=f'{type(e).__name__}: {e}')

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def readcsv(p):
    with Path(p).open(encoding='utf-8', newline='') as f:
        dr = csv.DictReader(f)
        return list(dr.fieldnames), list(dr)

def writecsv(p, cols, rows):
    with Path(p).open('w', encoding='utf-8', newline='') as f:
        dw = csv.DictWriter(f, fieldnames=cols, lineterminator='\n')
        dw.writeheader()
        dw.writerows(rows)

def release_probe(report, target_name='ml_physics', source_mutator=None, minimal=False):
    helper_path = SOURCE / 'scripts/test_lhs_release_v13.py'
    tree = ast.parse(helper_path.read_text(encoding='utf-8'))
    end = next(i for i, n in enumerate(tree.body) if isinstance(n, ast.FunctionDef) and n.name == 'stage13')
    env = {'__file__': str(helper_path), '__name__': 'consumer_independent_helpers'}
    exec(compile(ast.Module(body=tree.body[:end+1], type_ignores=[]), str(helper_path), 'exec'), env)
    atexit.unregister(env['_supp_cleanup'])
    cases = load(EV / 'consumers_probe.json')['handover']['cases']
    cid = cases[target_name]['case_id']
    target = next(r for r in load(EV / 'consumers_handover_rows.json') if r['case_id'] == cid)
    # Independent source copy means earlier evidence remains unchanged.
    source_root = ROOT / 'batch/merged/lhs'
    shutil.copytree(EV / 'consumers_fixtures/handover_results', source_root / 'results')
    shutil.copytree(EV / 'consumers_fixtures/handover_batch', source_root, dirs_exist_ok=True)
    if source_mutator:
        source_mutator(source_root / 'results' / cid, report)
        row_now = tf.case_row(source_root / 'results' / cid)
        target = dict(target, **{c: tf._cell(row_now.get(c)) for c in tf.column_names()})
    wb = DD.load_webapp(source_root)
    if source_mutator:
        tau_now = DD.load_tau_results(source_root / 'results', wb, expected_generation='g2')
        with (SOURCE / DD.DESCRIPTOR_FILL_EXPECTED['path']).open(encoding='utf-8-sig') as fh:
            design_now = [r for r in csv.DictReader(fh) if r['case_id'] == cid]
        harvested_now = DD.load_harvest(SOURCE / 'docs/data/lhs_descriptors_cov_1e09f661d')
        union_now = DD.load_union(SOURCE / DD.DEFAULT_UNION_TSV)
        hand_now, cols_now, hand_report = DD.build_handover(design_now, harvested_now, union=union_now,
            webapp=wb, webapp_groups='tau', tau=tau_now)
        target = next(r for r in hand_now if r['case_id'] == cid)
        report['actual_handover'] = dict(row=target, report=hand_report)
    actual_rr = RR.reread_case(source_root / 'results' / cid, 'g2', ps, tf)
    def mutate(ds, cols, rows):
        if ds == 'lhs':
            row = next(r for r in rows if r['case_id'] == cid)
            row.update({c: target[c] for c in tf.column_names()})
    handover = env['make_g2_handover_dir'](str(ROOT / 'handover'), mutate=mutate)
    batch = env['make_batch_root'](str(ROOT / 'batch'))
    gp = Path(batch) / 'reread.json'
    gate = load(gp)
    next(r for r in gate['cases'] if r['case'] == cid).update(checks=actual_rr['checks'], statuses=actual_rr['statuses'], row_cells=actual_rr['row_cells'])
    save(gp, gate)
    verdict = ROOT / 'TEST_ONLY_NOT_GO.txt'
    verdict.write_text('Synthetic review fixture only. Not an approval or production release.\n', encoding='utf-8')
    real_rr = RB.v13_reread_tau
    source_load = DD.load_tau_results
    observations = []
    def rr_adapter(ds, batch_root, rows, expected):
        old_load, old_web = DD.load_tau_results, DD.load_webapp
        def provide(*a, **kw):
            cells = {r['case_id']: {'cells': {c: r.get(c, '') for c in tf.column_names()}} for r in rows}
            if ds == 'lhs':
                # This original function executes real P0-P4 on the retained source.
                actual_tau = source_load(source_root / 'results', wb, expected_generation='g2')
                cells[cid] = actual_tau['cases'][cid]
            return {'schema': DD.TAU_NET_SCHEMA, 'cases': cells}
        DD.load_tau_results = provide
        DD.load_webapp = lambda *a, **kw: {'stop_after': 'network'}
        try:
            ans = real_rr(ds, batch_root, rows, expected)
            observations.append(dict(dataset=ds, problems=ans))
            return ans
        finally:
            DD.load_tau_results, DD.load_webapp = old_load, old_web
    RB.v13_reread_tau = rr_adapter
    def build(out):
        return env['build13'](out_dir=str(ROOT / out), handover_dir=handover, batch_root=batch,
                              date='20991231', codex_verdict=str(verdict))
    try:
        baseline = call(build, 'output')
        report['release_baseline'] = baseline
        report['release_baseline_check'] = call(RB.check_v13, str(ROOT / 'output'), handover)
        report['selected_reread'] = actual_rr
        hp = Path(RB._v13_handover(handover, 'lhs'))
        cols, rows = readcsv(hp)
        original = hp.read_bytes()
        selected = next(r for r in rows if r['case_id'] == cid)
        report['selected'] = dict(case=cid, status=selected['ion_net_status_hertz'], f=selected['f_ion_hertz'],
                                   tau2=selected['tau2_ion_hertz'], tau=selected['tau_ion_hertz'])
        if minimal:
            report['reread_observations'] = observations
            return
        report['k8_fresh_build_mutations'] = {}
        for field in ('tau2_ion_hertz', 'tau_ion_hertz'):
            for val in ('inf', 'nan', '-1.0', 'garbage'):
                rs = copy.deepcopy(rows)
                row = next(r for r in rs if r['case_id'] == cid)
                row[field] = val
                writecsv(hp, cols, rs)
                report['k8_fresh_build_mutations'][field + '=' + val] = dict(
                    blank_gate=RB.v13_blank_problems([row], ['case_id', field, 'f_ion_hertz', 'ion_net_status_hertz']),
                    build=call(build, 'bad_' + field + '_' + val),
                    existing_release_check=call(RB.check_v13, str(ROOT / 'output'), handover))
        hp.write_bytes(original)
        report['k8_restored_check'] = call(RB.check_v13, str(ROOT / 'output'), handover)
        # A single canonical-source edit without touching gate records or release.
        fp = source_root / 'results' / cid / 'full_metrics.json'
        fb = fp.read_bytes()
        fm = json.loads(fb)
        fm['thickness_um'] = 1e308
        save(fp, fm)
        before_gate = sha(gp)
        report['source_only_stale_gate'] = dict(
            change='Only selected full_metrics.json thickness_um -> 1e308; no artifact, manifest, gate, or handover writes.',
            stop=call(ps.network_stop_verdict, str(fp.parent), fm['network_run_id']),
            reread=call(RR.reread_case, fp.parent, 'g2', ps, tf),
            build=call(build, 'bad_source_only'),
            existing_release_check=call(RB.check_v13, str(ROOT / 'output'), handover),
            gate_sha_before=before_gate, gate_sha_after=sha(gp))
        fp.write_bytes(fb)
        # K5 real case_row error, introduced in one metadata field only. This
        # deliberately malformed shape is not a normal producer output.
        fm = json.loads(fb)
        fm['network_run_id'] = []
        save(fp, fm)
        save(ROOT / 'k5_previous_reread.json', actual_rr)
        cli_output = ROOT / 'k5_cli_reread.json'
        fp.write_bytes(fb)
        old_rc = call(RR.main, ['--case-dir', str(fp.parent), '--expect-generation', 'g2', '--json', str(cli_output)])
        old_sha = sha(cli_output)
        save(fp, fm)
        report['k5_case_row_exception'] = dict(
            change='Only selected full_metrics.json network_run_id -> []; deliberately malformed metadata shape.',
            case_row=call(tf.case_row, fp.parent),
            reread_case=call(RR.reread_case, fp.parent, 'g2', ps, tf),
            build=call(build, 'bad_case_row'),
            existing_release_check=call(RB.check_v13, str(ROOT / 'output'), handover),
            cli_before=old_rc,
            cli_after=call(RR.main, ['--case-dir', str(fp.parent), '--expect-generation', 'g2', '--json', str(cli_output)]),
            previous_output_sha=old_sha, current_output_sha=sha(cli_output))
        fp.write_bytes(fb)
        report['final_restored_check'] = call(RB.check_v13, str(ROOT / 'output'), handover)
    finally:
        RB.v13_reread_tau = real_rr
    report['reread_observations'] = observations

def stop_probe(report):
    source = EV / 'consumers_fixtures/ml_physics'
    cd = ROOT / 'stop_fields'
    shutil.copytree(source, cd)
    fp = cd / 'full_metrics.json'
    original = fp.read_bytes()
    baseline = load(fp)
    rid = baseline['network_run_id']
    report['stop_baseline'] = call(ps.network_stop_verdict, str(cd), rid)
    report['stop_big_integer'] = {}
    for field in ps.NETWORK_STOP_LEDGER_KEYS:
        fm = copy.deepcopy(baseline)
        fm[field] = 10**400
        save(fp, fm)
        report['stop_big_integer'][field] = dict(stop=call(ps.network_stop_verdict, str(cd), rid),
                                                reread=call(RR.reread_case, cd, 'g2', ps, tf))
    fp.write_bytes(original)
    report['stop_number_types'] = {repr(v): call(ps._stop_num, v) for v in (True, False, None, '1', 1, 1.0, 10**400, float('nan'), float('inf'))}

if __name__ == '__main__':
    report = dict(scope=__doc__, root=str(ROOT))
    with (ROOT / 'run.log').open('w', encoding='utf-8') as log:
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            stop_probe(report)
            release_probe(report)
    save(EV / 'consumer_adversarial.json', report)
    print(json.dumps({k:v for k,v in report.items() if k in ('root', 'release_baseline', 'release_baseline_check', 'selected', 'final_restored_check')}, ensure_ascii=False, indent=2))

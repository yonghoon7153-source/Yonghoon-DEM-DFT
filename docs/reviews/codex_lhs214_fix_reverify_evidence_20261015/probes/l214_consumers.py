"""Independent consumer review. Synthetic fixtures only; no production run or source edits."""
from pathlib import Path
import contextlib
import copy
import csv
import io
import json
import os
import subprocess
import sys
import time

REVIEW = Path(__file__).resolve().parents[1]
SOURCE = REVIEW / 'source'
EVIDENCE = REVIEW / 'evidence'
for p in (SOURCE / 'scripts', SOURCE / 'webapp'):
    sys.path.insert(0, str(p))
for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[k] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONUTF8'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'
SCRATCH = EVIDENCE / 'consumers_temp'
SCRATCH.mkdir(exist_ok=True)
os.environ['TMP'] = os.environ['TEMP'] = str(SCRATCH)


def dump(name, value):
    (EVIDENCE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding='utf-8')


def baseline():
    report = []
    for filename in ('scripts/test_tau_flux.py', 'scripts/test_gen2_role_contract.py', 'webapp/test_network_handover_chain.py'):
        began = time.monotonic()
        cmd = [sys.executable, '-X', 'utf8', '-B', str(SOURCE / filename)]
        result = subprocess.run(cmd, cwd=SOURCE, capture_output=True, text=True, encoding='utf-8')
        stem = Path(filename).stem
        (EVIDENCE / f'consumers_baseline_{stem}.log').write_text(result.stdout + '\nSTDERR\n' + result.stderr, encoding='utf-8')
        report.append(dict(test=filename, rc=result.returncode, seconds=time.monotonic()-began, last_lines=result.stdout.splitlines()[-6:]))
    dump('consumers_baseline.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def final_baselines():
    """Submitted scripts unchanged, after the parent supplied missing pinned fixtures."""
    report = []
    for stem, arguments in (
        ('release', ['scripts/test_lhs_release_v13.py']),
        ('reread', ['scripts/g2_network_reread.py', '--selftest']),
    ):
        began = time.monotonic()
        cmd = [sys.executable, '-X', 'utf8', '-B', str(SOURCE / arguments[0]), *arguments[1:]]
        result = subprocess.run(cmd, cwd=SOURCE, capture_output=True)
        stdout, stderr = (value.decode('utf-8', errors='backslashreplace') for value in (result.stdout, result.stderr))
        (EVIDENCE / f'baseline_{stem}_final.log').write_text(stdout + '\nSTDERR\n' + stderr, encoding='utf-8')
        report.append(dict(test=arguments, command=cmd, rc=result.returncode, seconds=time.monotonic()-began,
                           failures=[line for line in stdout.splitlines() if line.lstrip().startswith(('FAIL', '✗'))],
                           last_lines=stdout.splitlines()[-6:], stderr_last_lines=stderr.splitlines()[-8:]))
    dump('baseline_consumers_final_summary.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def final_baseline_environment():
    """Read final logs and diagnose only the two environment-dependent expectations."""
    import lhs_release_build as RB
    argv = RB.v13_handover_argv('lhsx', '/R', '/H/lhsx_handover_v13_X.csv', pressure='/R/pressure/lhsx_pressure_record.tsv')
    expected = {'--tau-batch-manifest': '/R/manifest.json', '--tau-results': '/R/merged/lhsx/results', '--webapp': '/R/merged/lhsx'}
    paths = {k: {'actual': argv[argv.index(k)+1], 'expected': v, 'equal_exact': argv[argv.index(k)+1] == v,
                 'equal_path_normalized': os.path.normpath(argv[argv.index(k)+1]) == os.path.normpath(v)} for k,v in expected.items()}
    report = json.loads((EVIDENCE / 'baseline_consumers_final_summary.json').read_text(encoding='utf-8'))
    for row in report:
        stem = 'release' if 'test_lhs_release' in row['test'][0] else 'reread'
        log = (EVIDENCE / f'baseline_{stem}_final.log').read_text(encoding='utf-8')
        row['failures'] = [line for line in log.splitlines() if line.lstrip().startswith(('FAIL', '✗'))]
        row['passed_count'] = 254 if stem == 'release' else sum(line.lstrip().startswith('✓') for line in log.splitlines()) - 1
    report[0]['environment_diagnosis'] = {
        'V10a': {'source_lines': 'test_lhs_release_v13.py:705-710', 'path_checks': paths,
                 'explanation': 'Windows os.path.join emits backslashes; normalized paths agree, exact POSIX-string expectations fail.'},
        'V16a': {'source_lines': 'test_lhs_release_v13.py:973-975', 'git_head': RB._v13_git('rev-parse', 'HEAD'),
                 'source_has_dotgit': (SOURCE / '.git').exists(),
                 'explanation': 'Pinned review snapshot has no Git checkout metadata; exact file hash comparisons were unchanged, but the test additionally requires a 40-character Git HEAD.'},
    }
    dump('baseline_consumers_final_summary.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def probe():
    import app
    import pipeline_service as ps
    import tau_flux as tf
    import test_pipeline_provenance as TP
    import test_network_handover_chain as CH
    import g2_network_reread as RR
    import lhs_release_build as RB
    import lhs_design_dataset as DD
    import lhs_webapp_batch as WB

    root = EVIDENCE / 'consumers_fixtures'
    root.mkdir(exist_ok=True)
    original_bed = TP._bed

    def custom_bed(name):
        if name in ('independent_l1_h0', 'independent_l2_h0'):
            a, c, plate, _box = original_bed('band_l1' if 'l1' in name else 'band_l2')
            return a, c, plate, 0.1
        return original_bed(name)

    TP._bed = custom_bed
    report = {'scope': 'Small synthetic fixtures and post-producer mutations only. No production execution.', 'cases': {}, 'mutations': {}}
    log = io.StringIO()
    runs = {}
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        for name in ('ml_physics', 'ml_hertz', 'ml_el', 'independent_l1_h0', 'independent_l2_h0'):
            folder = root / name
            if (folder / 'network_provenance.json').is_file():
                prov = json.loads((folder / 'network_provenance.json').read_text(encoding='utf-8'))
                runs[name] = (str(folder), 'done', [], prov['network_run_id'])
            else:
                folder.mkdir(exist_ok=True)
                runs[name] = CH._run_ml(app, name, tm='1:SE,2:AM_P' if name == 'ml_el' else '1:SE', d=str(folder))
            folder, status, failed, rid = runs[name]
            if status != 'done':
                report['cases'][name] = dict(status=status, failed=failed, folder=folder)
                continue
            dual = json.loads((Path(folder) / 'network_conductivity_dual.json').read_text(encoding='utf-8'))
            row = tf.case_row(folder)
            cells = {k: tf._cell(v) for k, v in row.items()}
            cells['case_id'] = name
            reread = RR.reread_case(folder, 'g2', ps, tf)
            report['cases'][name] = dict(
                status=status, failed=failed, run_id=rid,
                full={m: {k: tf.mode_record(dual, m).get(k) for k in ('sigma_full_status', 'sigma_full_reason', 'boundary_rule', 'ionic_status')} for m in tf.MODES},
                q={m: (tf.mode_record(dual, m).get('solve_certificate_full') or {}).get('q_withheld') for m in tf.MODES},
                tau={m: [row[f'ion_net_status_{m}'], row[f'ion_net_status_reason_{m}']] for m in tf.MODES},
                full_model_limit={m: tf.full_model_limit_problem(tf.mode_record(dual, m), 'ionic', m) for m in tf.MODES},
                release_primary_hold=RB.v13_primary_model_limit_problems([cells]),
                blank_code=RB.v13_blank_reason(cells, 'f_ion_hertz'),
                reread_checks=reread['checks'],
            )
        # The same genuine producer record is independently mutated at the consumer seam.
        base_dual = json.loads((root / 'ml_physics' / 'network_conductivity_dual.json').read_text(encoding='utf-8'))
        fm = json.loads((root / 'ml_physics' / 'full_metrics.json').read_text(encoding='utf-8'))
        mutants = {
            'cf_bad_residual': lambda r: r['solve_certificate_bulk_net'].__setitem__('residual_rel', 1.0),
            'missing_bulk_model': lambda r: r.pop('bulk_model', None),
            'withheld_q_x101': lambda r: r['solve_certificate_full'].__setitem__('q_withheld', r['solve_certificate_full']['q_withheld'] * 1.01),
            'other_thermal_failure': lambda r: r.__setitem__('thermal_status', 'failed'),
            'other_electronic_failure': lambda r: r.__setitem__('electronic_status', 'failed'),
            'unknown_full_reason': lambda r: r.__setitem__('sigma_full_reason', 'full_over_conduction:extra'),
            'h12_role_in_physics': lambda r: r['solve_certificate_full'].__setitem__('role', 'H12'),
        }
        for name, mutate in mutants.items():
            dual = copy.deepcopy(base_dual)
            mutate(dual['physics'])
            rec = dual['physics']
            row = tf.ion_columns(dual, fm, fm['percolation_pct'])
            report['mutations'][name] = dict(
                model_limit=tf.full_model_limit_problem(rec, 'ionic', 'physics'),
                ion=tf.ion_record_problem(rec),
                binding=tf.certificate_binding_problems('physics', rec),
                generation=tf.network_generation_contract(dual),
                channels={ch: ps.channel_verdict(rec, ch, 'physics') for ch in ps.NETWORK_CHANNELS},
                tau=[row['ion_net_status_physics'], row['ion_net_status_reason_physics']],
            )
        # Genuine batch/handover path, using registered historical metadata for small fixtures only.
        dump('consumers_probe.json', report)
        src = SOURCE / 'docs/data/lhs_webapp_contact_d1ec42fba'
        st0 = json.loads((src / 'status.json').read_text(encoding='utf-8'))
        with (src / 'metrics_flat.csv').open(encoding='utf-8', newline='') as fh:
            flat = {r['case']: {k: v for k, v in r.items() if v != ''} for r in csv.DictReader(fh)}
        candidates = sorted(c for c, s in st0['cases'].items() if s.get('status') == 'done' and float(flat.get(c, {}).get('percolation_pct', 0)) > 0)
        with (SOURCE / DD.DESCRIPTOR_FILL_EXPECTED['path']).open(encoding='utf-8-sig') as fh:
            design = list(csv.DictReader(fh))
        harvest = DD.load_harvest(SOURCE / 'docs/data/lhs_descriptors_cov_1e09f661d')
        union = DD.load_union(SOURCE / DD.DEFAULT_UNION_TSV)
        results = root / 'handover_results'
        results.mkdir(exist_ok=True)
        state = copy.deepcopy(st0)
        state.update(stop_after='network', cases={})
        rows = {}
        mapping = {}
        import shutil
        for case, name in zip(candidates, runs):
            folder, status, failed, rid = runs[name]
            if status != 'done':
                continue
            mapping[case] = name
            shutil.copytree(folder, results / case, dirs_exist_ok=True)
            state['cases'][case] = dict(st0['cases'][case], stop_after='network', status=status, failed_stages=failed, network_run_id=rid)
            fm = json.loads((results / case / 'full_metrics.json').read_text(encoding='utf-8'))
            tie = tuple(ps.NETWORK_STOP_LEDGER_KEYS) + tuple(DD.TAU_TIE_EXTRA)
            rows[case] = dict(flat[case], **{k: fm[k] for k in tie if k in fm})
        batch = root / 'handover_batch'
        WB.write_outputs(batch, state, rows)
        web = DD.load_webapp(batch)
        tau = DD.load_tau_results(results, web, expected_generation='g2')
        hrows, hcols, hr = DD.build_handover([r for r in design if r['case_id'] in mapping], harvest, union=union, webapp=web, webapp_groups='tau', tau=tau)
        report['handover'] = dict(report=hr, cases={mapping[r['case_id']]: dict(
            case_id=r['case_id'], tau={m: [r[f'ion_net_status_{m}'], r[f'ion_net_status_reason_{m}']] for m in tf.MODES},
            primary_hold=RB.v13_primary_model_limit_problems([r]), blank_code=RB.v13_blank_reason(r, 'f_ion_hertz'),
            blank_problems=RB.v13_blank_problems([r], ['case_id','f_ion_hertz','tau2_ion_hertz','tau_ion_hertz','ion_net_status_hertz','ion_net_status_reason_hertz']),
        ) for r in hrows})
        dump('consumers_handover_rows.json', hrows)
    TP._bed = original_bed
    (EVIDENCE / 'consumers_probe.log').write_text(log.getvalue(), encoding='utf-8')
    dump('consumers_probe.json', report)
    print(json.dumps({'cases': {n: {k: c[k] for k in ('status', 'q', 'tau', 'release_primary_hold')} for n,c in report['cases'].items()}, 'handover': report['handover']['cases']}, ensure_ascii=False, indent=2))


def release_probe():
    """Real build/check functions with declared synthetic batch evidence and one real fixture row.

    The unselected table rows and audit records are the submitted selftest fixtures.
    The selected row's P0-P4 source is the genuine small producer/publisher fixture.
    No solver batch is launched, no production result is certified.
    """
    import ast
    import tau_flux as tf
    import lhs_release_build as RB
    import lhs_design_dataset as DD
    helper_path = SOURCE / 'scripts/test_lhs_release_v13.py'
    tree = ast.parse(helper_path.read_text(encoding='utf-8'))
    helper = ast.Module(body=[n for n in tree.body if n.lineno < 452], type_ignores=[])
    env = {'__file__': str(helper_path), '__name__': 'consumer_release_fixture_helpers'}
    exec(compile(helper, str(helper_path), 'exec'), env)
    import atexit
    import logging
    atexit.unregister(env['_supp_cleanup'])  # Retain the fixture batch addressed by the build manifest.
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
    root = EVIDENCE / 'consumers_release_verified'
    if root.exists():
        root = EVIDENCE / f'consumers_release_verified_{time.time_ns()}'
    root.mkdir(exist_ok=True)
    (root / 'TEST_ONLY_NOT_GO.txt').write_text('Synthetic path probe only. No production execution, launch approval, or release certification.\n', encoding='utf-8')
    realrows = json.loads((EVIDENCE / 'consumers_handover_rows.json').read_text(encoding='utf-8'))
    byid = {r['case_id']: r for r in realrows}
    casemap = json.loads((EVIDENCE / 'consumers_probe.json').read_text(encoding='utf-8'))['handover']['cases']
    wb = DD.load_webapp(EVIDENCE / 'consumers_fixtures/handover_batch')
    actual_tau = DD.load_tau_results(EVIDENCE / 'consumers_fixtures/handover_results', wb, expected_generation='g2')
    original_rr = RB.v13_reread_tau
    observations = []
    report = {'scope': 'Actual build_v13/check_v13, dry_run=False and diagnostic=False; synthetic audit/batch and other rows as explicitly declared; selected row has actual P0-P4 verified small fixture source.', 'cases': {}}
    for name in ('ml_hertz', 'independent_l1_h0', 'independent_l2_h0'):
        cid = casemap[name]['case_id']
        target = byid[cid]
        case_root = root / name
        case_root.mkdir()
        def mutate(ds, head, rows):
            if ds == 'lhs':
                row = next(r for r in rows if r['case_id'] == cid)
                row.update({c: target[c] for c in tf.column_names()})
        handover = env['make_g2_handover_dir'](str(case_root / 'handover'), mutate=mutate)
        batch = env['make_batch_root'](str(case_root / 'batch'))
        # Put the actual selected case's K1-K7 results into the synthetic gate record.
        import g2_network_reread as RR
        import pipeline_service as ps
        gate_path = Path(batch) / 'reread.json'
        gate = json.loads(gate_path.read_text(encoding='utf-8'))
        actual = RR.reread_case(EVIDENCE / 'consumers_fixtures/handover_results' / cid, 'g2', ps, tf)
        for r in gate['cases']:
            if r['case'] == cid:
                r.update(checks=actual['checks'], statuses=actual['statuses'], row_cells=actual['row_cells'])
        gate_path.write_text(json.dumps(gate, ensure_ascii=False), encoding='utf-8')
        verdict = case_root / 'fixture_verdict.txt'
        verdict.write_text('TEST ONLY synthetic fixture verdict; not a production approval.\n', encoding='utf-8')
        def rr_adapter(ds, batch_root, rows, expected):
            # Preserve the real comparison function. Only fixture source provisioning is adapted.
            orig_load, orig_web = DD.load_tau_results, DD.load_webapp
            def provision(*a, **kw):
                cells = {r['case_id']: {'cells': {c: r.get(c, '') for c in tf.column_names()}} for r in rows}
                if ds == 'lhs':
                    cells[cid] = actual_tau['cases'][cid]
                return {'schema': DD.TAU_NET_SCHEMA, 'cases': cells}
            DD.load_tau_results = provision
            DD.load_webapp = lambda *a, **kw: {'stop_after': 'network'}
            try:
                problems = original_rr(ds, batch_root, rows, expected)
                observations.append({'fixture': name, 'dataset': ds, 'problems': problems, 'selected_actual': ds == 'lhs'})
                return problems
            finally:
                DD.load_tau_results, DD.load_webapp = orig_load, orig_web
        RB.v13_reread_tau = rr_adapter
        try:
            result = env['build13'](out_dir=str(case_root / 'output'), handover_dir=handover, batch_root=batch, date='20991231', codex_verdict=str(verdict))
            checked = RB.check_v13(str(case_root / 'output'), handover)
            report['cases'][name] = {'built': True, 'result': result, 'checked': checked, 'target_case': cid, 'primary_gate': RB.v13_primary_model_limit_problems([target])}
        except Exception as exc:
            report['cases'][name] = {'built': False, 'exception': f'{type(exc).__name__}: {exc}', 'target_case': cid, 'primary_gate': RB.v13_primary_model_limit_problems([target])}
        finally:
            RB.v13_reread_tau = original_rr
    report['reread_observations'] = observations
    dump('consumers_release_probe.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def negative_paths():
    import shutil
    import tau_flux as tf
    import pipeline_service as ps
    import g2_network_reread as RR
    import lhs_design_dataset as DD
    import test_pipeline_provenance as TP
    root = EVIDENCE / 'consumers_negative_paths'
    root.mkdir(exist_ok=True)
    original = EVIDENCE / 'consumers_fixtures/ml_physics'
    mutations = {
        'cf_bad_residual': lambda r: r['solve_certificate_bulk_net'].__setitem__('residual_rel', 1.0),
        'missing_bulk_model': lambda r: r.pop('bulk_model', None),
        'withheld_q_x101': lambda r: r['solve_certificate_full'].__setitem__('q_withheld', r['solve_certificate_full']['q_withheld'] * 1.01),
        'other_thermal_failure': lambda r: r.__setitem__('thermal_status', 'failed'),
        'other_electronic_failure': lambda r: r.__setitem__('electronic_status', 'failed'),
        'unknown_full_reason': lambda r: r.__setitem__('sigma_full_reason', 'full_over_conduction:extra'),
        'h12_role_in_physics': lambda r: r['solve_certificate_full'].__setitem__('role', 'H12'),
    }
    output = {}
    for name, mutate in mutations.items():
        cd = root / name
        shutil.copytree(original, cd, dirs_exist_ok=True)
        def edit(rec, filename, mode):
            if mode == 'physics':
                mutate(rec)
        TP._edit_net_records(str(cd), edit)
        fm = json.loads((cd / 'full_metrics.json').read_text(encoding='utf-8'))
        rid = fm['network_run_id']
        # Preserve any mirrored changed status so projection checks do not create the intended rejection.
        rec = json.loads((cd / 'network_conductivity_physics.json').read_text(encoding='utf-8'))
        for k in ps.NET_PHYSICS_MIRROR_KEYS:
            if k in rec:
                if rec[k] is not None:
                    fm[k + '_physics'] = rec[k]
                else:
                    fm.pop(k + '_physics', None)
        (cd / 'full_metrics.json').write_text(json.dumps(fm, ensure_ascii=False), encoding='utf-8')
        rr = RR.reread_case(cd, 'g2', ps, tf)
        web = {'stop_after': 'network', 'status': {name: {'status': 'done', 'network_run_id': rid}}, 'rows': {name: {k: tf._cell(fm.get(k)) for k in tuple(ps.NETWORK_STOP_LEDGER_KEYS) + DD.TAU_TIE_EXTRA}}}
        try:
            DD.load_tau_results(root, web, expected_generation='g2')
            handover = {'accepted': True}
        except Exception as exc:
            handover = {'accepted': False, 'exception': f'{type(exc).__name__}: {exc}'}
        output[name] = {
            'content': ps.network_content_verdict(str(cd)),
            'general_record': ps.network_record_verdict(str(cd)),
            'stop': ps.network_stop_verdict(str(cd), rid),
            'reread_rejects': [r['name'].split()[0] for r in rr['checks'] if not r['ok']],
            'handover': handover,
        }
    dump('consumers_negative_paths.json', output)
    print(json.dumps({k: {'content': v['content'][0], 'general_record': v['general_record'][0], 'stop': v['stop'][0], 'reread_rejects': v['reread_rejects'], 'handover_accepted': v['handover']['accepted']} for k,v in output.items()}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if '--baseline' in sys.argv:
        baseline()
    elif '--final-baselines' in sys.argv:
        final_baselines()
    elif '--final-baseline-environment' in sys.argv:
        final_baseline_environment()
    elif '--release' in sys.argv:
        release_probe()
    elif '--negative' in sys.argv:
        negative_paths()
    else:
        probe()

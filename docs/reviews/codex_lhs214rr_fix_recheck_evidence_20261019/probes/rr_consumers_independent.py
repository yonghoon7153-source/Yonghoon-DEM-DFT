"""R04 independent full-consumer mutants against fresh genuine producer output.

Reuse only this review's successful release fixture. Original source is read-only.
Four label mutations, all numerical leaves untouched. Preserve old release gate
to exercise fresh source reread independently, then replace gate with actual
reread and exercise batch rejection. Scratch changes are restored in finally.
The 213 unselected release rows and batch/audit remain declared synthetic.
"""
from pathlib import Path
import contextlib
import copy
import json
import logging
import rr_consumers_run as R
import tau_flux as tf
import pipeline_service as ps
import g2_network_reread as RR
import lhs_design_dataset as DD
import lhs_release_build as RB
import app

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def save(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

def call(fn, *a, **kw):
    try:
        return {'value': fn(*a, **kw), 'exception': None}
    except Exception as e:
        return {'value': None, 'exception': f'{type(e).__name__}: {e}'}

def differences(a, b, prefix=''):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            p = prefix + '.' + k if prefix else k
            if k not in a or k not in b:
                out.append({'path': p, 'before': a.get(k), 'after': b.get(k)})
            else:
                out += differences(a[k], b[k], p)
        return out
    return [] if a == b else [{'path': prefix, 'before': a, 'after': b}]

def main():
    base = load(R.EV / 'baseline.json')
    out = Path(base['release_baseline']['value']['out_dir'])
    root = out.parent
    handover, batch = root / 'handover', root / 'batch'
    source_root = batch / 'merged/lhs'
    cid = base['selected']['case']
    cd = source_root / 'results' / cid
    names = ['network_conductivity_dual.json', 'network_conductivity_hertzian.json', 'network_conductivity_physics.json', 'network_conductivity.json', 'full_metrics.json']
    originals = {n: (cd / n).read_bytes() for n in names}
    gate_path = batch / 'reread.json'
    gate_bytes = gate_path.read_bytes()
    release_manifest = load(out / 'v13_build_manifest.json')
    supp_root = release_manifest['supp_batch']['batch_gate']['batch_root']
    web = DD.load_webapp(source_root)
    genuine_load = DD.load_tau_results
    genuine_reread = RB.v13_reread_tau
    logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
    report = {'scope': __doc__, 'fixture_root': str(root), 'baseline': base['release_baseline'], 'variants': {}}

    def rr_adapter(ds, batch_root, rows, expected):
        old_load, old_web = DD.load_tau_results, DD.load_webapp
        def provide(*a, **kw):
            cells = {r['case_id']: {'cells': {c: r.get(c, '') for c in tf.column_names()}} for r in rows}
            if ds == 'lhs':
                cells[cid] = genuine_load(source_root / 'results', web, expected_generation='g2')['cases'][cid]
            return {'schema': DD.TAU_NET_SCHEMA, 'cases': cells}
        DD.load_tau_results = provide
        DD.load_webapp = lambda *a, **kw: {'stop_after': 'network'}
        try:
            return genuine_reread(ds, batch_root, rows, expected)
        finally:
            DD.load_tau_results, DD.load_webapp = old_load, old_web

    def build(name):
        return call(RB.build_v13, out_dir=str(root / name), handover_dir=str(handover), batch_root=str(batch),
                    supp_batch_root=supp_root, date='20991231', codex_verdict=str(root / 'TEST_ONLY_NOT_GO.txt'))

    RB.v13_reread_tau = rr_adapter
    try:
        for name, mode, branch, reason_only in (
            ('h0_cf_flip', 'hertz', 'bulk_only', False),
            ('physics_constr_flip', 'physics', 'constriction_only', False),
            ('h12_cf_reason', 'hertz_h12', 'bulk_only', True),
            ('h0_full_reason', 'hertz', 'full', True),
        ):
            for n, b in originals.items():
                (cd / n).write_bytes(b)
            gate_path.write_bytes(gate_bytes)
            du = load(cd / names[0])
            before_du = copy.deepcopy(du)
            rec = tf.mode_record(du, mode)
            _, qk, dk, sk, rk, ck = next(b for b in tf.CERT_BRANCH_KEYS if b[0] == branch)
            st = rec[sk]
            rsn = None if st == 'model_over_conduction' else 'q_gt_1p5'
            rec[rk], rec[ck]['reason'] = rsn, rsn
            if not reason_only:
                target = 'computed' if st == 'model_over_conduction' else 'model_over_conduction'
                rec[sk], rec[ck]['status'] = target, target
            save(cd / names[0], du)
            save(cd / names[1], du['hertzian'])
            save(cd / names[2], du['physics'])
            save(cd / names[3], du['hertzian'])
            fm = load(cd / names[4])
            h, p = du['hertzian'], du['physics']
            projection = {k: h[k] for k in ps.NET_MERGE_KEYS if h.get(k) is not None}
            projection.update({f'{k}_physics': p[k] for k in ps.NET_PHYSICS_MIRROR_KEYS if p.get(k) is not None})
            projection.update({k: p[k] for k in ps.NET_PHYSICS_TAILED_KEYS if p.get(k) is not None})
            for k in ps.NET_MERGE_KEYS:
                if k in projection:
                    fm[k] = projection[k]
                else:
                    fm.pop(k, None)
            save(cd / names[4], fm)
            actual = RR.reread_case(cd, 'g2', ps, tf)
            row = tf.case_row(cd)
            diffs = differences(before_du, du)
            projection_check = app._network_projection(str(cd), fm['network_run_id'])
            item = {'mutations': diffs,
                    'numerical_leaves_unchanged': all(d['path'].split('.')[-1].endswith(('status', 'reason')) for d in diffs),
                    'content': call(ps.network_content_verdict, str(cd)),
                    'record': call(ps.network_record_verdict, str(cd)),
                    'stop': call(ps.network_stop_verdict, str(cd), fm['network_run_id']),
                    'publication_general': call(app._network_candidate_checks, str(cd), fm['network_run_id'], projection_check, False),
                    'publication_stop_path': call(app._network_candidate_checks, str(cd), fm['network_run_id'], projection_check, True),
                    'reread': actual, 'row': row,
                    'load_tau_results': call(genuine_load, source_root / 'results', web, expected_generation='g2'),
                    'existing_release_check_with_unchanged_gate': call(RB.check_v13, str(out), str(handover)),
                    'fresh_build_stale_gate': build('r04_' + name + '_source')}
            gate = json.loads(gate_bytes)
            next(r for r in gate['cases'] if r['case'] == cid).update(checks=actual['checks'], statuses=actual['statuses'], row_cells=actual['row_cells'])
            save(gate_path, gate)
            item['batch_gate'] = call(RB.v13_batch_gate_problems, str(batch))
            item['fresh_build_actual_gate'] = build('r04_' + name + '_gate')
            item['outputs_absent'] = all(not (root / ('r04_' + name + '_' + s)).exists() for s in ('source', 'gate'))
            report['variants'][name] = item
    finally:
        for n, b in originals.items():
            (cd / n).write_bytes(b)
        gate_path.write_bytes(gate_bytes)
        RB.v13_reread_tau = genuine_reread
    report['restored_existing_release_check'] = call(RB.check_v13, str(out), str(handover))
    R.save('independent_r04.json', report)
    print(json.dumps({k: {'record': v['record']['value'][0], 'stop': v['stop']['value'][0],
                         'load': v['load_tau_results']['exception'], 'fresh_source': v['fresh_build_stale_gate']['exception'],
                         'fresh_gate': v['fresh_build_actual_gate']['exception'], 'outputs_absent': v['outputs_absent']}
                      for k, v in report['variants'].items()}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    with (R.EV / 'independent_r04_stdout.log').open('w', encoding='utf-8') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        main()
    print('Independent R04 consumer mutations completed.')

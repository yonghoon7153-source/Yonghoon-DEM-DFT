"""Extend independent numeric H0 resurrection through actual stop/reread/build.

The genuine producer ml_hertz fixture supplies every number. Only H0 publication
values/statuses are restored from its withheld q; current/geometry/attempts and
q_guard diagnostics are unchanged. The ionic power share is copied from that
same producer record's thermal H0 share (identical resistor ratios here); its
status and full_metrics projection are made consistent, explicitly enumerated.
The source-copy fixture and synthetic unselected release rows are not production.
"""
import contextlib
import copy
import json
import consumer_adversarial as C

def differences(a, b, prefix=''):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            p = prefix + '.' + k if prefix else k
            if k not in a or k not in b:
                out.append(dict(path=p, before=a.get(k), after=b.get(k)))
            else:
                out += differences(a[k], b[k], p)
    elif a != b:
        out.append(dict(path=prefix, before=a, after=b))
    return out

def mutate(cd, report):
    paths = ('network_conductivity_dual.json', 'network_conductivity_hertzian.json', 'network_conductivity.json', 'full_metrics.json')
    originals = {n:C.load(cd/n) for n in paths}
    dual = copy.deepcopy(originals[paths[0]])
    rec = dual['hertzian']
    cert = rec['solve_certificate_full']
    numeric_before = copy.deepcopy(cert)
    q = cert['q_withheld']
    report['before'] = dict(stop=C.call(C.ps.network_stop_verdict, str(cd), originals['full_metrics.json']['network_run_id']),
                           row=C.tf.case_row(cd), q=q)
    rec.update(sigma_full=round(q, 8), sigma_full_mScm=round(q*rec['sigma_grain_S_cm']*1000, 6),
               sigma_full_status='computed', sigma_full_reason=None, ionic_status='computed', ionic_status_reason=None)
    cert.update(status='computed', reason=None)
    def write_projection():
        C.save(cd/'network_conductivity_dual.json', dual)
        C.save(cd/'network_conductivity_hertzian.json', rec)
        C.save(cd/'network_conductivity.json', rec)
        fm = copy.deepcopy(originals['full_metrics.json'])
        for k in C.ps.NET_MERGE_KEYS:
            if k in rec:
                if rec[k] is None:
                    fm.pop(k, None)
                else:
                    fm[k] = rec[k]
        C.save(cd/'full_metrics.json', fm)
        return fm
    fm = write_projection()
    report['numeric_only_stop'] = C.call(C.ps.network_stop_verdict, str(cd), fm['network_run_id'])
    rec['constriction_power_share_ion_hertz'] = rec['constriction_power_share_th_hertz']
    rec['constriction_power_share_ion_hertz_status'] = 'computed'
    fm = write_projection()
    num_after = copy.deepcopy(cert)
    for obj in (numeric_before, num_after):
        obj.pop('status', None)
        obj.pop('reason', None)
    report['after'] = dict(content=C.call(C.ps.network_content_verdict, str(cd)),
                          record=C.call(C.ps.network_record_verdict, str(cd)),
                          stop=C.call(C.ps.network_stop_verdict, str(cd), fm['network_run_id']),
                          row=C.tf.case_row(cd),
                          certificate_numeric_unchanged=numeric_before == num_after,
                          power_source=rec['constriction_power_share_th_hertz'])
    report['mutations'] = {n:differences(originals[n], C.load(cd/n)) for n in paths}
    # Normal batch projection must follow the candidate before P3 sees it.
    # This is an explicit metadata update, not a waiver of P0-P4 or their checks.
    import lhs_webapp_batch as WB
    batch_dir = cd.parent.parent
    state = C.load(batch_dir/'status.json')
    _, flat = C.readcsv(batch_dir/'metrics_flat.csv')
    brows = {r['case']:{k:v for k,v in r.items() if v != ''} for r in flat}
    before_flat = copy.deepcopy(brows[cd.name])
    for k in tuple(C.ps.NETWORK_STOP_LEDGER_KEYS) + tuple(C.DD.TAU_TIE_EXTRA):
        if k in fm:
            brows[cd.name][k] = fm[k]
        else:
            brows[cd.name].pop(k, None)
    WB.write_outputs(batch_dir, state, brows)
    report['batch_projection_changes'] = differences(before_flat, brows[cd.name])

report = dict(scope=__doc__, root=str(C.ROOT))
with (C.ROOT/'run.log').open('w', encoding='utf-8') as log:
    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        C.release_probe(report, target_name='ml_hertz', source_mutator=mutate, minimal=True)
C.save(C.EV/'consumer_h0_resurrection.json', report)
print(json.dumps({k:report[k] for k in ('root', 'numeric_only_stop', 'after', 'release_baseline', 'release_baseline_check', 'selected')}, ensure_ascii=False, indent=2))

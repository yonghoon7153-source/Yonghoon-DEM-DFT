"""Reviewer-owned ZIP/data inspection. Never imports or executes received code."""
import csv
import base64
import hashlib
import io
import json
import re
import stat
import sys
import zipfile
from decimal import Decimal as D, getcontext
from pathlib import PurePosixPath

ARCHIVE = r'C:/Users/Administrator/Downloads/BMIN_R2_NATIVE150_RESULT_FOR_REVIEW_20261006.zip'

def digest_stream(f):
    h = hashlib.sha256()
    n = 0
    while True:
        b = f.read(1024 * 1024)
        if not b:
            return n, h.hexdigest()
        n += len(b)
        h.update(b)

def js(z, name):
    return json.loads(z.read(name).decode('utf-8-sig'))

def compact(v, limit=5):
    if isinstance(v, dict):
        return {k: compact(x, limit) for k, x in v.items()}
    if isinstance(v, list):
        if len(v) > limit:
            return {'count': len(v), 'first': compact(v[:2], limit), 'last': compact(v[-1:], limit)}
        return [compact(x, limit) for x in v]
    return v

def integrity(z):
    info = z.infolist()
    names = [x.filename for x in info]
    errors = []
    folded = set()
    for x in info:
        p = PurePosixPath(x.filename)
        key = x.filename.replace('\\', '/').casefold()
        if key in folded:
            errors.append(['duplicate_or_case_collision', x.filename])
        folded.add(key)
        if p.is_absolute() or '..' in p.parts or '\\' in x.filename or ':' in x.filename:
            errors.append(['unsafe_path', x.filename])
        if stat.S_ISLNK(x.external_attr >> 16):
            errors.append(['symlink', x.filename])
    m = js(z, 'PACKAGE_MANIFEST.json')
    expected = {x['entry']: x for x in m['files']}
    if len(expected) != len(m['files']):
        errors.append(['manifest_duplicate'])
    if set(names) != set(expected) | {'PACKAGE_MANIFEST.json'}:
        errors.append(['exact_set'])
    checked = 0
    total = 0
    for name, entry in expected.items():
        with z.open(name) as f:
            n, h = digest_stream(f)
        if (n, h) != (entry['bytes'], entry['sha256']):
            errors.append(['member_identity', name, n, h])
        total += n
        checked += 1
    with open(ARCHIVE, 'rb') as f:
        n, h = digest_stream(f)
    mb = z.read('PACKAGE_MANIFEST.json')
    return {'archive': {'bytes': n, 'sha256': h}, 'manifest': {'bytes': len(mb), 'sha256': hashlib.sha256(mb).hexdigest()}, 'payload_checked': checked, 'decompressed_payload_bytes': total, 'crc': 'Checked by zipfile on reading every member to EOF', 'errors': errors}

def inspect(z):
    out = {}
    for name in ['run/DIAGNOSTIC_RESULT.json', 'delivery/SELECTED_SOURCES_BEFORE.json', 'source/CONTRACT.json', 'source/CODE_MANIFEST.json']:
        out[name] = compact(js(z, name))
    out['csv_headers'] = {}
    for name in z.namelist():
        if name.endswith('.csv') and name.startswith(('run/tables/', 'baseline/')):
            with z.open(name) as f:
                stream = io.TextIOWrapper(f, encoding='utf-8-sig', newline='')
                rows = csv.reader(stream)
                out['csv_headers'][name] = [next(rows, None) for _ in range(3)]
    return out

def evidence(z):
    m = {x['entry']: x for x in js(z, 'PACKAGE_MANIFEST.json')['files']}
    errors = []
    checks = []
    def ck(label, ok):
        checks.append(label)
        if not ok:
            errors.append(label)
    def pinned(name, r):
        ck('pin:' + name, (m[name]['bytes'], m[name]['sha256']) == (r['bytes'], r['sha256']))
    c = js(z, 'source/CONTRACT.json')
    a = js(z, 'authorization/bmin640_001.json')
    rel = js(z, 'authorization/VALIDATION_RELEASE.json')
    pstart = js(z, 'parent/PARENT_START.json')
    state = js(z, 'run/NATIVE_STATE.json')
    diag = js(z, 'run/DIAGNOSTIC_RESULT.json')
    for r in js(z, 'source/CODE_MANIFEST.json')['files']:
        pinned('source/' + r['file'], r)
    ck('accepted_code_manifest', m['source/CODE_MANIFEST.json']['sha256'] == '4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25')
    ck('staged_java', z.read('run/Bmin640Candidate.java') == z.read('source/src/Bmin640Candidate.java'))
    pinned('run/Bmin640Candidate.class', js(z, 'run/CLASS_IDENTITY.json'))
    pinned('authorization/USER_DECISION.json', a['user_decision'])
    pinned('authorization/VALIDATION_RELEASE.json', a['validation_release'])
    pinned('authorization/bmin640_001.json', pstart['approval'])
    pinned('authorization/VALIDATION_RELEASE.json', pstart['release'])
    ck('approval_commands_budgets', a['commands'] == c['commands'] and a['budgets_seconds'] == c['budgets_seconds'])
    ck('approval_policy_scope', a['approved'] is True and a['allow_policy_changes'] is False and a['effective_policy_unverified_accepted'] is True)
    for name, r in c['baseline_files'].items():
        pinned('baseline/' + name, r)
    for r in c['external_source_pins']:
        pinned('external_dependencies/' + r['path'].rsplit('/', 1)[-1], r)
    for name, r in diag['tables_manifest'].items():
        pinned('run/tables/' + name, r)
    before = js(z, 'delivery/SELECTED_SOURCES_BEFORE.json')
    ck('selected_before_unique', len(before) == len({r['entry'] for r in before}))
    for r in before:
        pinned(r['entry'], r)
    for phase in ('compile', 'batch'):
        reservation = js(z, 'run/' + phase + '_RESERVATION.json')
        ret = js(z, 'run/' + phase + '_RETURN.json')
        ck(phase + '_argv_cwd', reservation['argv'] == c['commands'][phase] and reservation['cwd'] == c['run_root'])
        ck(phase + '_state_return', state[phase] == ret)
        ck(phase + '_terminal', ret['rc'] == 0 and ret['cleanup'] == 'PASS' and ret['remaining_owned'] == [] and ret['unattributed_comsol'] == [] and ret['handles_closed'] and ret['ownership_verified'] and not ret['recording_errors'] and not ret['cleanup_errors'])
    ck('attempts', state['native_attempts'] == {'compile': 1, 'batch': 1})
    ck('native_state_terminal', state['status'] == 'NATIVE_RETURN_READY' and state['errors'] == [])
    for k in ('preservation', 'policy_preservation', 'process_cleanup'):
        ck(k, state[k] == 'PASS' and diag[k] == 'PASS')
    policy = js(z, 'run/POLICY_BEFORE.json')
    ck('policy_authorized_pin', policy['default'] == a['default_prefs_identity'] and policy['changes_authorized'] is False and len(policy['security']) == 16)
    bnd = js(z, 'parent/FINAL_BOUNDARY.json')
    local = js(z, 'parent/PARENT_LOCAL_DECISION.json')
    post = json.loads(z.read('delivery/USER_FINAL_CONSOLE_TRANSCRIPT.txt').decode('utf-8-sig').splitlines()[0])
    pinned('parent/PARENT_TRANSCRIPT.txt', bnd['transcript'])
    pinned('parent/PARENT_LOCAL_DECISION.json', bnd['local_decision'])
    pinned('parent/FINAL_BOUNDARY.json', post['boundary'])
    ck('parent_native_return_binding', local['native_return'] == js(z, 'parent/NATIVE_PARENT_RETURN.json'))
    ck('parent_analysis_return_binding', local['analysis_return'] == js(z, 'parent/ANALYSIS_PARENT_RETURN.json'))
    ck('parent_postwrite_fields', local['fields'] == bnd['fields'] == post['fields'])
    ck('parent_no_record_errors', bnd['errors'] == [] and post['record_errors'] == [] and post['within_limits'] is True)
    ck('parent_boundary_scope', post['raw_host_rc'] is None and bnd['raw_host_rc'] is None and post['host_boundary'] == 'SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT')
    ck('parent_chronology', local['native_return']['start_seconds'] < local['native_return']['end_seconds'] < local['analysis_return']['start_seconds'] < local['analysis_return']['end_seconds'] < bnd['elapsed_seconds'] == post['pre_write_seconds'] < post['snapshot_seconds'] < c['budgets_seconds']['overall'])
    ck('analysis_budget', local['analysis_return']['elapsed_seconds'] < c['budgets_seconds']['analysis'])
    ck('delivery_parent_budget', post['delivery_elapsed_seconds'] < c['budgets_seconds']['delivery'])
    ck('resource_disk', js(z, 'run/RESOURCES.json')['free_disk_bytes'] >= 15 * 2**30)
    ck('MPH_record_identity', js(z, 'run/OUTPUT_MPH_IDENTITY.json') == js(z, 'delivery/MPH_PRESERVATION_IDENTITY.json')['observed'])
    known_reviews = {
        'BMIN_R2_RETRY3_SUPPLEMENT_REVIEW_20261006.zip': '105c84ae203a0d480521d0086f945a2ed20892b95c274067e8895c3142428d76',
        'BMIN150_DEPLOYMENT_PREFLIGHT_REVIEW_20261006.zip': '062f224d08db003f5cda3a69fc48f4081e0377fac694a1ddb63a5a122948e1a3',
        'BMIN150_DEPLOYMENT_PREFLIGHT_FOR_REVIEW_20261006.zip': '8800035eb5ed427ea66d98d8dab8406fff189edceb9d86732706fbd323e70640',
        'BMIN_R2_LIMITED_VALIDATION_RETRY3_RESULT_20261005.zip': 'ed0138b90cf2dc4e42f22ec18d8719ff56906780f74b4139850d604b096bb470',
    }
    for name, h in known_reviews.items():
        ck('prior_review:' + name, m['review_evidence/' + name]['sha256'] == h)
    # Check every nested review archive's CRC without executing contents.
    nested = {}
    for name in known_reviews:
        with zipfile.ZipFile(io.BytesIO(z.read('review_evidence/' + name))) as nz:
            bad = nz.testzip()
            ck('nested_crc:' + name, bad is None)
            nested[name] = len(nz.namelist())
    # Independent inspection of the native solver section and emitted CSV bytes.
    batch = z.read('run/batch.log').decode('utf-8-sig')
    ck('batch_no_fatal', re.search(r'/\*{3,}\s*Error\s*\*{3,}/|Error running java class|OutOfMemoryError|Exception in thread|Security preference .*does not allow', batch, re.I) is None)
    opens = list(re.finditer(r'^<---- Time-Dependent Solver.*$', batch, re.M))
    closes = list(re.finditer(r'^----- Time-Dependent Solver.*-+>\s*$', batch, re.M))
    ck('one_transient_solver', len(opens) == len(closes) == 1)
    section = batch[opens[0].end():closes[0].start()]
    steps = re.findall(r'^\s*(\d+)\s+([0-9.eE+\-]+)\s+([0-9.eE+\-]+)\s+out\s+', section, re.M)
    ck('native_steps', len(steps) == 2447 and [int(r[0]) for r in steps] == list(range(2447)) and D(steps[-1][1]) == 150)
    guard_rows = list(csv.DictReader(io.StringIO(z.read('run/tables/electrolyte_guard.csv').decode('utf-8-sig'))))
    stored = [D(r['time_s']) for r in guard_rows]
    ck('stored_time_native_rounding', len(steps) == len(stored) and all(abs(D(s[1])-t) <= D(1).scaleb(D(s[1]).as_tuple().exponent)/2 for s,t in zip(steps,stored)))
    ck('stored_step_caps', all(0 < b-a <= (D('.000125') if a < D('.1') else D('.1')) * (1+D('1e-9')) + D('1e-12') for a,b in zip(stored,stored[1:])))
    ck('stored_threshold_zero', all(D(r['threshold_mol_m3']) == 0 for r in guard_rows))
    ck('no_protective_stop', 'Stop condition fulfilled' not in batch)
    ck('no_post_end_integration', re.search(r'^\s*\d+\s+[0-9.eE+\-]+\s+[0-9.eE+\-]+\s+out\s+', batch[closes[0].end():], re.M) is None)
    dofs = re.findall(r'Number of degrees of freedom solved for: (\d+) \(plus (\d+) internal DOFs\)\.', section)
    ck('transient_dof', dofs == [('156925', '12')])
    table_names = []
    significant = []
    fatal = []
    with z.open('run/batch_console.log') as f:
        for line in f:
            if line.startswith(b'AUDIT_TABLE_BASE64='):
                name, b64 = line.strip().split(b'=', 1)[1].split(b'|', 1)
                name = name.decode('ascii')
                raw = base64.b64decode(b64, validate=True)
                table_names.append(name)
                ck('console_table:' + name, (len(raw), hashlib.sha256(raw).hexdigest()) == (m['run/tables/' + name]['bytes'], m['run/tables/' + name]['sha256']))
            else:
                s = line.decode('utf-8-sig')
                if any(v in s for v in ['AXES_PHYSICAL_', 'AXES_PARTICLE=', 'AXES_ACTUAL_MESH=', 'BMIN640_PRODUCER_COMPLETE', 'PREFLIGHT_SOLVER_RETURNED=', 'ELECTROLYTE_COUPLING=']):
                    significant.append(s.strip())
                if re.search(r'Error running java class|OutOfMemoryError|Exception in thread|Security preference .*does not allow', s, re.I):
                    fatal.append(s.strip())
    ck('console_tables_unique', len(table_names) == len(set(table_names)) == 35)
    ck('console_tables_exact_set', set(table_names) == set(diag['tables_manifest']))
    ck('console_no_fatal', not fatal)
    ck('mesh_readback', all(significant.count(line) == 1 for line in c['mesh_readback_required']))
    ck('producer_complete', significant.count('BMIN640_PRODUCER_COMPLETE') == 1 and significant.count('PREFLIGHT_SOLVER_RETURNED=true; physical checks separate') == 1)
    return {'checks': len(checks), 'errors': errors, 'selected_before_members': len(before), 'emitted_csv_count': len(table_names), 'native_steps': len(steps), 'transient_dof': dofs, 'native_significant_lines': significant, 'parent_boundary': bnd, 'post_write_snapshot_seconds': post['snapshot_seconds'], 'nested_zip_counts': nested, 'run_file_count_excludes_events': len([n for n in m if n.startswith('run/') and '_event_' not in n]), 'note': 'Native preservation/cleanup are accepted from saved records and source behavior, not current host observation. Post-packaging source-after file absent.'}

def numeric(z):
    getcontext().prec = 50
    errors = []
    c = js(z, 'source/CONTRACT.json')
    diag = js(z, 'run/DIAGNOSTIC_RESULT.json')
    def ck(label, ok):
        if not ok:
            errors.append(label)
    def rows(name):
        with z.open(name) as f:
            yield from csv.DictReader(io.TextIOWrapper(f, encoding='utf-8-sig', newline=''))
    def series(name):
        out = {}
        last = None
        for row in rows(name):
            v = {k: D(x) for k, x in row.items()}
            t = v['time_s']
            if last is not None and t <= last:
                raise ValueError('duplicate/time order: ' + name)
            if not all(x.is_finite() for x in v.values()):
                raise ValueError('nonfinite: ' + name)
            out[t] = v
            last = t
        return out
    names = ['preflight_global.csv', 'preflight_boundary1.csv', 'preflight_boundary4.csv', 'electrolyte_guard.csv', 'preflight_MinLine_ce.csv', 'preflight_MaxLine_ce.csv']
    cur = {n: series('run/tables/' + n) for n in names}
    old = {n: series('baseline/' + n) for n in names}
    ts = list(cur[names[0]])
    bs = list(old[names[0]])
    ck('current_table_times', all(list(v) == ts for v in cur.values()))
    ck('baseline_table_times', all(list(v) == bs for v in old.values()))
    ck('stored_2447_0_150', len(ts) == 2447 and ts[0] == 0 and ts[-1] == 150)
    requested = [D(x) for x in c['requested_times_s']]
    primary = [D(120) + D(i) / 10 for i in range(301)]
    outside = [t for t in requested if t < 120]
    auxiliary = sorted((set(ts) & set(bs)) - set(primary))
    auxiliary = [t for t in auxiliary if 120 <= t <= 150]
    ck('requested_coverage', len(requested) == len(set(requested)) == 1637 and set(requested).issubset(ts) and set(requested).issubset(bs))
    ck('primary_exact_301', [D(x) for x in c['primary_comparison_times_s']] == primary and set(primary).issubset(ts) and set(primary).issubset(bs))
    def maximum(values):
        d, t, idx = max(values, key=lambda v: abs(v[0]))
        return {'absolute': str(abs(d)), 'signed_delta': str(d), 'time_s': str(t), 'index': idx}
    results = {}
    li_keys = ['Li_N_mol_m2', 'Li_P_mol_m2', 'Li_electrolyte_mol_m2']
    def li(data, t):
        return sum(data['preflight_global.csv'][t][k] for k in li_keys)
    def voltage(data, t):
        return data['preflight_boundary4.csv'][t]['phis_V'] - data['preflight_boundary1.csv'][t]['phis_V']
    for label, chosen in [('primary', primary), ('outside_observation', outside)]:
        out = {'voltage_V': maximum((voltage(cur, t)-voltage(old, t), t, None) for t in chosen), 'total_Li_mol_m2': maximum((li(cur, t)-li(old, t), t, None) for t in chosen)}
        for col in ['ce_min_all_mol_m3', 'ce_min_d1_mol_m3', 'ce_min_d2_mol_m3', 'ce_min_d3_mol_m3']:
            out[col] = maximum((cur['electrolyte_guard.csv'][t][col]-old['electrolyte_guard.csv'][t][col], t, None) for t in chosen)
        for s in ('MinLine', 'MaxLine'):
            n = 'preflight_' + s + '_ce.csv'
            out['ce_' + s] = maximum((cur[n][t]['ce_mol_m3']-old[n][t]['ce_mol_m3'], t, None) for t in chosen)
        results[label] = out
    total0 = li(cur, D(0))
    drift = max(abs((li(cur, t)-total0)/total0) for t in ts)
    residual = max(abs(voltage(cur, t)-sum(cur['preflight_boundary4.csv'][t][k]-cur['preflight_boundary1.csv'][t][k] for k in ['Eeq_V','etamid_V','phil_V'])) for t in ts)
    ck('Li_drift_report', drift == D(diag['numeric']['maximum_Li_relative_drift']))
    ck('voltage_residual_report', residual == D(diag['numeric']['maximum_voltage_identity_V']))
    guards = ['electrolyte_guard', 'ocp_guard', 'surface_guard']
    ck('no_active_guards', all(cur['electrolyte_guard.csv'][t][g] == 0 for t in ts for g in guards))
    ck('ce_positive', all(cur['electrolyte_guard.csv'][t]['ce_min_all_mol_m3'] > 0 for t in ts))
    ck('minimum_same_operator', all(abs(v['ce_min_all_mol_m3'] - min(v['ce_min_d1_mol_m3'], v['ce_min_d2_mol_m3'], v['ce_min_d3_mol_m3'])) <= D(c['limits']['minimum_consistency_mol_m3']) for v in cur['electrolyte_guard.csv'].values()))
    initial = {k: str(abs(cur['preflight_global.csv'][D(0)][k] - old['preflight_global.csv'][D(0)][k])) for k in li_keys}
    ck('initial_Li', all(D(v) <= D('1e-9') for v in initial.values()))
    counts = {}
    for electrode, domain in [('N',1),('P',3)]:
        coords = [D(x) for x in c['coordinates'][electrode]]
        by_source = []
        for prefix, expected_times in [('run/tables/', ts), ('baseline/', bs)]:
            extracted = {}
            group_times = []
            prior = None
            count = 0
            idx = 0
            for raw in rows(prefix + 'axes_profile_' + electrode + '.csv'):
                t = D(raw['time_s'])
                if t != prior:
                    if prior is not None and idx != 241:
                        raise ValueError('profile group size')
                    if prior is not None and t <= prior:
                        raise ValueError('profile time order')
                    group_times.append(t)
                    idx = 0
                    prior = t
                v = [D(raw[k]) for k in raw]
                if not all(x.is_finite() for x in v) or idx >= 241:
                    raise ValueError('profile numeric/count')
                if abs(D(raw['coordinate_m'])-coords[idx]) > D(c['limits']['coordinate_m']) or D(raw['domain_id']) != domain:
                    raise ValueError('profile coordinate/domain')
                x = D(raw['x_surface'])
                lo,hi = (D(0),D('.98')) if domain == 1 else (D('.2228930343076256'),D('.983245033354389'))
                if not (lo <= x <= hi and 0 < x < 1):
                    raise ValueError('profile surface/OCP bounds')
                if t in requested:
                    extracted.setdefault(t, []).append(x)
                count += 1
                idx += 1
            ck(prefix + electrode + '_profile_group_times', group_times == expected_times and idx == 241)
            counts[prefix + electrode] = count
            by_source.append(extracted)
        for label, chosen in [('primary', primary), ('outside_observation', outside)]:
            results[label]['surface_x_' + electrode] = maximum((by_source[0][t][i]-by_source[1][t][i], t, i) for t in chosen for i in range(241))
    for label, reported in [('primary','primary'),('outside_observation','outside_window_observation')]:
        for k, v in results[label].items():
            r = diag['numeric']['windows'][reported][k]
            ck(label + '_reported_' + k, D(v['absolute']) == D(r['maximum_absolute']) and D(v['time_s']) == D(r['time_s']) and v['index'] == r['coordinate_index'])
    settings = {r['key']:r['actual_value'] for r in rows('run/tables/axes_runtime_settings.csv')}
    settings0 = {r['key']:r['actual_value'] for r in rows('baseline/axes_runtime_settings.csv')}
    ck('runtime_keys', set(settings) == set(settings0))
    ck('runtime_invariance', all(settings[k] == settings0[k] for k in settings if k != 'study_tlist'))
    ck('tlist_exact_prefix', settings['study_tlist'].split() == c['requested_times_s'] == settings0['study_tlist'].split()[:1637])
    return {'errors':errors, 'current_times': len(ts), 'baseline_times': len(bs), 'requested': len(requested), 'primary_times':len(primary), 'auxiliary_times':len(auxiliary), 'outside_observation_times':len(outside), 'profile_rows':counts, 'maxima':results, 'Li_drift':str(drift), 'voltage_identity_residual_V':str(residual), 'initial_Li_deltas':initial, 'runtime_setting_count':len(settings), 'received_analyzer_executed':False}

with zipfile.ZipFile(ARCHIVE) as z:
    mode = sys.argv[1]
    if mode == 'integrity':
        result = integrity(z)
    elif mode == 'inspect':
        result = inspect(z)
    elif mode == 'read':
        result = {n: compact(js(z, n)) if n.endswith('.json') else z.read(n).decode('utf-8-sig') for n in sys.argv[2:]}
    elif mode == 'evidence':
        result = evidence(z)
    elif mode == 'numeric':
        result = numeric(z)
    else:
        raise ValueError(mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))

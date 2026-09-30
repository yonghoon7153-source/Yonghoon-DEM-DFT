"""Recipient-authored data arithmetic only. Does not import any received code."""
import base64, csv, hashlib, json, re
from decimal import Decimal as D, getcontext
from pathlib import Path

getcontext().prec = 50
ROOT = Path(__file__).resolve().parent
R = ROOT / 'received'
T = R / 'run/tables'
C = json.loads((R / 'candidate/CONTRACT.json').read_text(encoding='utf-8-sig'))
checks = []
def check(label, ok):
    checks.append({'check': label, 'pass': bool(ok)})
    if not ok:
        raise ValueError(label)
def read_csv(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames and len(set(reader.fieldnames)) == len(reader.fieldnames)
        for row in reader:
            assert None not in row and None not in row.values(), str(p)
            yield row
def timed(p):
    out = {}
    last = None
    for raw in read_csv(p):
        row = {k: D(v) for k, v in raw.items()}
        assert all(v.is_finite() for v in row.values()), str(p)
        t = row['time_s']
        assert last is None or t > last, str(p)
        out[t] = row
        last = t
    assert out and next(iter(out)) == 0
    return out
def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

names = ['electrolyte_guard.csv', 'preflight_global.csv', 'preflight_boundary1.csv',
         'preflight_boundary4.csv', 'preflight_MinLine_ce.csv', 'preflight_MaxLine_ce.csv']
data = {n: timed(T / n) for n in names}
base = {n: timed(R / 'baseline' / n) for n in names[:4]}
g, gl, bn, bp, mn, mx = [data[n] for n in names]
times = list(g)
check('all six time-series: identical ordered 1237 stored times, 0 to 30',
      len(times) == 1237 and times[0] == 0 and times[-1] == 30 and all(list(x) == times for x in data.values()))
baseline_times = list(base[names[0]])
check('four baseline time-series: identical 987 times, 0 to 5',
      len(baseline_times) == 987 and baseline_times[-1] == 5 and all(list(x) == baseline_times for x in base.values()))
requested = {D(t) for t in C['requested_times_s']}
requested_old = {D(t) for t in C['baseline_requested_times_s']}
common = sorted(set(times) & set(baseline_times))
check('437 requested times present; 187 baseline requests; exact prefix intersection 987',
      len(requested) == 437 and len(requested_old) == 187 and requested <= set(times)
      and requested_old <= set(baseline_times) and common == baseline_times
      and [t for t in times if t <= 5] == baseline_times)
check('stored intervals within declared cap', all(
      b - a <= (D('.000125') if a < D('.1') else D('.1')) * (D(1)+D('1e-9')) + D('1e-12')
      for a, b in zip(times, times[1:])))
guard_keys = ['electrolyte_guard', 'ocp_guard', 'surface_guard']
check('threshold zero and all three guard values zero at every stored time',
      all(v['threshold_mol_m3'] == 0 and all(v[k] == 0 for k in guard_keys) for v in g.values()))
check('global OCP guard and surface extrema in declared ranges at all stored times',
      all(v['ocp_guard']==0 and 0<v['xsurf_N_min']<=v['xsurf_N_max']<=D('.98')
          and D('.2228930343076256')<=v['xsurf_P_min']<=v['xsurf_P_max']<=D('.983245033354389') for v in gl.values()))
min_consistency = max(abs(v['ce_min_all_mol_m3'] - min(v[f'ce_min_d{i}_mol_m3'] for i in (1,2,3))) for v in g.values())
check('minimum coupling agrees with minimum of three domain operators', min_consistency <= D('1e-9'))
minline_difference = max(abs(g[t]['ce_min_all_mol_m3'] - mn[t]['ce_mol_m3']) for t in times)
check('minimum and maximum line values ordered and positive', all(D(0) < mn[t]['ce_mol_m3'] <= mx[t]['ce_mol_m3'] for t in times))
voltage = {t: bp[t]['phis_V'] - bn[t]['phis_V'] for t in times}
bvoltage = {t: base[names[3]][t]['phis_V'] - base[names[2]][t]['phis_V'] for t in baseline_times}
dv = max(abs(voltage[t] - bvoltage[t]) for t in common)
check('0-5s exact common voltage difference <= 1mV', dv <= D('.001'))
vdiff = max(abs(voltage[t] - sum(bp[t][k] - bn[t][k] for k in ['Eeq_V','etamid_V','phil_V'])) for t in times)
check('voltage decomposition identity residual <= 1e-8V', vdiff <= D('1e-8'))
li_keys = ['Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2']
li0diff = {k: abs(gl[D(0)][k] - base[names[1]][D(0)][k]) for k in li_keys}
check('initial Li each component absolute difference <= 1e-9 mol/m2', all(x <= D('1e-9') for x in li0diff.values()))
li = {t: sum(gl[t][k] for k in li_keys) for t in times}
lidrift = max(abs((x-li[D(0)])/li[D(0)]) for x in li.values())
check('Li relative drift <= 1e-6', lidrift <= D('1e-6'))

profiles = {}
for electrode, domain in [('N',1), ('P',3)]:
    coords = [D(x) for x in C['coordinates'][electrode]]
    check(f'{electrode}: 241 distinct ordered contract coordinates', len(coords) == len(set(coords)) == 241 and coords == sorted(coords))
    old = {}
    summaries = {}
    for which, p in [('baseline',R/'baseline'/f'axes_profile_{electrode}.csv'), ('target',T/f'axes_profile_{electrode}.csv')]:
        seen = []
        idx = 0
        count = 0
        max_delta = D(0)
        min_x, max_x = D(1), D(0)
        last = None
        for raw in read_csv(p):
            v = {k:D(x) for k,x in raw.items()}
            assert all(x.is_finite() for x in v.values())
            t = v['time_s']
            if t != last:
                assert last is None or idx == 241
                assert last is None or t > last
                seen.append(t); idx = 0; last = t
                if which == 'baseline': old[t] = []
            assert idx < 241 and v['domain_id'] == domain and abs(v['coordinate_m']-coords[idx]) <= D('1e-15')
            x = v['x_surface']
            lo, hi = (D(0),D('.98')) if domain == 1 else (D('.2228930343076256'),D('.983245033354389'))
            assert lo <= x <= hi and 0 < x < 1
            min_x, max_x = min(min_x,x), max(max_x,x)
            if which == 'baseline': old[t].append(x)
            elif t in old: max_delta = max(max_delta, abs(x-old[t][idx]))
            if which == 'target' and t in [D(0),D(5),D(10),D(20),D(30)]:
                summaries.setdefault(str(t), []).append(x)
            idx += 1; count += 1
        check(f'{electrode} {which}: full ordered time x coordinate product, finite, domain and OCP range',
              seen == (baseline_times if which == 'baseline' else times) and idx == 241 and count == len(seen)*241)
        if which == 'target':
            check(f'{electrode}: surface comparison <= 1e-4', max_delta <= D('1e-4'))
            profiles[electrode] = {'target_rows': count, 'baseline_rows': len(baseline_times)*241,
                'max_surface_absolute_difference':max_delta,'minimum_surface_x':min_x,'maximum_surface_x':max_x,
                'selected_surface_ranges':{t:{'min':min(v),'max':max(v)} for t,v in summaries.items()}}

settings = {r['key']:r['actual_value'] for r in read_csv(T/'axes_runtime_settings.csv')}
check('runtime readback equals all required settings', all(settings[k] == v for k,v in C['runtime_settings_required'].items()))
check('actual study tlist equals exact requested set in order', [D(x) for x in settings['study_tlist'].split()] == sorted(requested))
binding = list(read_csv(T/'guard_binding.csv'))
check('guard expression, stepbefore/stepafter, active mode and threshold readback', binding == [{
    'electrolyte_expression':C['guard_expression'],'stop_storage':'stepbefore_stepafter',
    'active':'on','terminate_on':'true','threshold_SI':'0.0'}])
unit_arrays = {'eguard':['s']+['mol/m^3']*5+['1']*3,
    'nglobal':['s']+['mol/m^2']*3+['1']*7+['A/m^2']*3,
    'point1':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],
    'point4':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],
    'MinLinece':['s','mol/m^3'],'MaxLinece':['s','mol/m^3'],'profiletimes':['s'],
    'profileN':['s','m','1','1','V','V','V','1'],'profileP':['s','m','1','1','V','V','V','1']}
unit_count = 0
for tag, u in unit_arrays.items():
    for phase in (['inferred','configured','evaluated'] if tag=='eguard' else ['configured','evaluated']):
        arr = u.copy()
        if phase != 'configured':
            for i in ([6,7,8] if tag == 'eguard' else [10] if tag == 'nglobal' else [7] if tag in ['profileN','profileP'] else []): arr[i]=''
        text = '['+', '.join(arr)+']'
        check(f'units {tag} {phase}', list(read_csv(T/f'units_{tag}_{phase}.csv')) == [{'tag':tag,'phase':phase,'expected':text,'actual':text}])
        unit_count += 1

embedded = {}
console_markers = []
fatal = []
with (R/'run/batch_console.log').open(encoding='utf-8-sig') as f:
    for line in f:
        if line.startswith('AUDIT_TABLE_BASE64='):
            name, value = line.strip().split('=',1)[1].split('|',1)
            assert re.fullmatch(r'[A-Za-z0-9_]+\.csv',name) and name not in embedded
            raw = base64.b64decode(value,validate=True)
            h = hashlib.sha256(raw).hexdigest()
            assert (T/name).stat().st_size == len(raw) and sha(T/name) == h
            embedded[name] = {'bytes':len(raw),'sha256':h}
        else:
            if re.search(r'Error running java class|OutOfMemoryError|Exception in thread|Security preference .*does not allow|/\*{3,}\s*Error',line,re.I): fatal.append(line[:500])
            if line.strip(): console_markers.append(line.strip())
check('all 35 extracted tables bound to native console base64, no extra table files', len(embedded)==35 and set(embedded)=={p.name for p in T.iterdir() if p.is_file()})
check('native console no fatal pattern and producer/solver completion once', not fatal and console_markers.count('NORMAL30_PRODUCER_COMPLETE')==1 and console_markers.count('PREFLIGHT_SOLVER_RETURNED=true; physical checks separate')==1)
for tag, selection in [('minguardall','[1, 2, 3]'),('minguard1','[1]'),('minguard2','[2]'),('minguard3','[3]')]:
    check(f'coupling {tag}: actual domain/dimension/lagrange readback',console_markers.count(f'ELECTROLYTE_COUPLING={tag}|dimension=1|entities={selection}|points=lagrange|lagrange=5')==1)
mesh_markers=['AXES_PHYSICAL_MESH_DOMAIN=1|numelem=120','AXES_PHYSICAL_MESH_DOMAIN=2|numelem=60',
    'AXES_PHYSICAL_MESH_DOMAIN=3|numelem=120','AXES_PARTICLE=pce1|Nel=320|Nord=1|Distribution=CubicRoot',
    'AXES_PARTICLE=pce2|Nel=320|Nord=1|Distribution=CubicRoot','AXES_ACTUAL_MESH=mesh1|edges=300|vertices=301',
    'PREFLIGHT_SOLVE_BEGIN=0..30 seconds; NO full protocol or sweep']
check('native console confirms 300 physical and320/320 particle and fresh30s solve label',all(console_markers.count(x)==1 for x in mesh_markers))
log = (R/'run/batch.log').read_text(encoding='utf-8-sig')
steps = re.findall(r'^\s*(\d+)\s+([0-9.eE+\-]+)\s+([0-9.eE+\-]+)\s+out\s+',log,re.M)
check('native 1237 step IDs and rounded times match exact saved times', len(steps)==len(times) and all(int(s[0])==i and abs(D(s[1])-t)<=D(1).scaleb(D(s[1]).as_tuple().exponent)/2 for i,(s,t) in enumerate(zip(steps,times))))
check('single time-dependent solver completed, no stop/fatal error',len(re.findall(r'^<---- Time-Dependent Solver',log,re.M))==1 and len(re.findall(r'^----- Time-Dependent Solver',log,re.M))==1 and log.count('Time-stepping completed.')==1 and 'Stop condition fulfilled' not in log and not re.search(r'/\*{3,}\s*Error|Exception in thread|OutOfMemoryError',log))
check('no steps after time-stepping completion',not re.search(r'^\s*\d+\s+[0-9.eE+\-]+\s+[0-9.eE+\-]+\s+out\s+',log.split('Time-stepping completed.',1)[1],re.M))
selected = {str(t):{'voltage_V':voltage[t],'ce_min_mol_m3':g[t]['ce_min_all_mol_m3'],
    'ce_max_mol_m3':mx[t]['ce_mol_m3'],'xavg_N':gl[t]['xavg_N'],'xavg_P':gl[t]['xavg_P'],
    **{k:gl[t][k] for k in ['xsurf_N_min','xsurf_N_max','xsurf_P_min','xsurf_P_max']}}
    for t in [D(0),D(5),D(10),D(20),D(30)]}
result = {'scope':'Independent Decimal50 CSV arithmetic and log decoding. No supplied code executed.',
    'status':'PASS','checks':checks,'stored_times':len(times),'requested_times':len(requested),'common_prefix_times':len(common),
    'profile_rows_total':sum(p['target_rows'] for p in profiles.values()),'max_voltage_difference_V':dv,
    'max_surface_difference':max(x['max_surface_absolute_difference'] for x in profiles.values()),
    'initial_Li_component_differences_mol_m2':li0diff,'maximum_relative_Li_drift':lidrift,
    'max_voltage_identity_residual_V':vdiff,'minimum_operator_consistency_mol_m3':min_consistency,
    'minimum_line_vs_coupling_max_difference_mol_m3':minline_difference,'profiles':profiles,'selected_times':selected,
    'native_core_report':[x.strip() for x in log.splitlines() if 'cores in total' in x],
    'native_solution_times':[x.strip() for x in log.splitlines() if x.startswith('Solution time:')],
    'native_last_step':steps[-1], 'embedded_table_identities':embedded,'unit_records':unit_count}
(ROOT/'NUMERIC_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','embedded_table_identities','profiles']},indent=2,default=str))

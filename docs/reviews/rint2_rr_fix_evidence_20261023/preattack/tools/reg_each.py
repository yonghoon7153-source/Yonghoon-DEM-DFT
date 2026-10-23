import json, sys, os, importlib.util
ev = sys.argv[1]
spec = importlib.util.spec_from_file_location('reg', os.path.join(ev, 'registration', 'probe_registration_current.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
out = {}
for name in ('rca01', 'endpoint_sweep', 'guard_padding', 'plan_validation', 'sbe_origin_union', 'dbe_origin', 'logic',
             'dbe_nonmonotone', 'sv_origin_scope', 'budget'):
    try:
        r = getattr(m, name)()
        s = '...'
        if name in ('dbe_nonmonotone', 'plan_validation', 'budget', 'endpoint_sweep', 'dbe_origin'):
            s = r
        if name == 'sv_origin_scope':
            s = {k: r[k] for k in ('fetch_counts', 'sv_enabled_counts', 'adjusted_values')}
        if name == 'logic':
            s = {'noop': r['noop']['verdict'], 'gap': r['gap']['verdict'], 'zeros': r['zero_scale_invariance']}
        if name == 'rca01':
            s = [{k: x[k] for k in ('err', 'verdict', 'W', 'end_R')} for x in r]
        if name == 'guard_padding':
            s = {k: r[k] for k in ('padding_factor', 'n_runs', 'reported_hi_R')}
        out[name] = {'ok': True, 'summary': s}
    except Exception as e:
        out[name] = {'ok': False, 'exc': type(e).__name__, 'msg': str(e)[:400]}
print(json.dumps(out, ensure_ascii=False, indent=1, default=str, sort_keys=True))

# Pending: post `find_and_rerun_stage_e.py --all` UI refresh

**Date queued:** 2026-05-13
**Trigger:** user accidentally ran `python3 scripts/find_and_rerun_stage_e.py --all`
(all 78 cases under `webapp/archive/`) to fix missing Stage E fields in
`input_6mAh_real40_4` — which surfaced because that case's
`full_metrics.json` predated the Physics-Stage E pipeline.

## What the script does

For each of 78 cases:
  1. Reads `atoms.csv`, `contacts.csv`, `meta.json`, `input_params.json`.
  2. Recomputes Stage E factors (Lawn fracture × Cronau / Trevisanello
     / Wang grain corrections).
  3. Writes the following keys into `full_metrics.json` — overwriting
     stale entries:
     - `sigma_full_mScm_stage_e`, `electronic_sigma_full_mScm_stage_e`,
       `thermal_sigma_full_mScm_stage_e`
     - `sigma_full_mScm_stage_e_physics`,
       `electronic_sigma_full_mScm_stage_e_physics`,
       `thermal_sigma_full_mScm_stage_e_physics`
     - `stage_e_factors_used`  (audit trail of all factors per channel)
     - `stage_e_source`        (`solver` | `fallback_weighted_factor`
       | `baseline_no_correction`)

## When the run completes — checklist

```bash
# 1. Verify all cases now carry Stage E keys (should print 78 0)
find webapp/archive -name full_metrics.json -exec \
  python3 -c "
import sys, json
for p in sys.argv[1:]:
    d = json.load(open(p))
    missing = [k for k in (
        'sigma_full_mScm_stage_e',
        'sigma_full_mScm_stage_e_physics',
        'electronic_sigma_full_mScm_stage_e',
        'electronic_sigma_full_mScm_stage_e_physics',
        'thermal_sigma_full_mScm_stage_e',
        'thermal_sigma_full_mScm_stage_e_physics',
        'stage_e_factors_used',
    ) if d.get(k) is None]
    if missing:
        print('MISSING in', p, ':', missing)
print('done')
" {} +
```

```bash
# 2. Invalidate webapp's mtime cache so report pages re-render
rm -f docs/db/.mtime_cache.json
# (the cache is keyed by full_metrics.json mtime; deleting forces
#  next request to recompute Stage E section)
```

```bash
# 3. Restart Flask (if running) so any module-level caches reset
pkill -f 'flask run' 2>/dev/null
pkill -f 'webapp/app.py' 2>/dev/null
# then restart with the user's usual launcher
```

```bash
# 4. Open the case that originally triggered this — should now show
#    Stage E final values for σ_ionic / σ_e / κ in BOTH Hertzian and
#    Physics columns, with no "n/a" Trevisanello/Wang labels.
explorer.exe "webapp/archive/후막(6mAh)/input_6mAh_real40_4"
# or visit:  http://localhost:8080/case/input_6mAh_real40_4
```

```bash
# 5. Re-run the downstream 82-case porosity validation if any cases
#    had their porosity/thickness re-derived (Stage E does not touch
#    these, so this is a sanity check only):
python3 scripts/collect_porosity_cases.py \
    webapp/archive/particulate \
    "webapp/archive/박막(1mAh)" \
    "webapp/archive/후막(6mAh)" \
    "webapp/archive/후막(8mAh)"
diff all_dem_porosity.csv all_dem_porosity.prev.csv 2>/dev/null \
    && echo "✓ porosity unchanged (expected — Stage E doesn't touch ε)"
```

```bash
# 6. Spot-check a few representative cases manually:
for c in input_8mAh_9 input_1mAh_5 input_particulate_4 input_6mAh_real40_4; do
  echo "=== $c ==="
  python3 -c "
import json, glob
p = glob.glob('webapp/archive/**/$c/full_metrics.json', recursive=True)[0]
d = json.load(open(p))
for k in ('sigma_full_mScm','sigma_full_mScm_stage_e',
         'sigma_full_mScm_stage_e_physics',
         'electronic_sigma_full_mScm_stage_e_physics',
         'thermal_sigma_full_mScm_stage_e_physics'):
    print(f'  {k:50s} {d.get(k)}')
"
done
```

## Expected outcome

After the --all run + cache invalidation:

- **All 78 case reports** will display populated Stage E rows for
  σ_ionic (Cronau), σ_e (Trev × Lawn), κ (Wang × Lawn) in both
  Hertzian and Physics columns.
- For r_SE ≥ 0.5 µm cases (Cronau factor 1.00), σ_ionic Stage E
  equals baseline (passthrough); flag `stage_e_source = 'baseline_no_correction'`.
- For cases with r_AM_P/r_AM_S available, Trevisanello/Wang factors
  fill instead of "n/a".
- Cases where solver returned a non-physical value will route through
  Layer 6 Bruggeman fallback automatically.

## Related code paths

- Driver:    `scripts/find_and_rerun_stage_e.py`
- Worker:    `scripts/run_network_full_corrections.py`
- Renderer:  `webapp/app.py::inject_stage_e_rows`  (lines 366–520)
- mtime DB:  `docs/db/.mtime_cache.json` (purge to force re-render)

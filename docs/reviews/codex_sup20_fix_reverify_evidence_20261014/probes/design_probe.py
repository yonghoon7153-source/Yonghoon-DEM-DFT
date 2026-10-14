"""Read-only numerical/data-contract audit at b429c3c1d; no DEM/network runs.

Only writes review evidence and temporary output under this review folder.
Independent geometry uses SI insertion volume 3.34e-13 m3 and r in microns.
"""
from pathlib import Path
import collections
import copy
import csv
import hashlib
import io
import json
import math
import sys
import tarfile
import tempfile

R = Path(__file__).resolve().parents[1]
S = R / 'source'
sys.path.insert(0, str(S / 'scripts'))
import lhss_design_adapter as A
import lhs_release_build as B
import lhs_design_dataset as D


def rows(path):
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        out = list(reader)
        return list(reader.fieldnames), out


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent(row):
    # Physical volume = 50 um * 50 um * 133.6 um; density AM 4800, SE 2000.
    # This is the same geometry stated by V_INS=3.34e-4 in scaled deck units,
    # calculated here directly in SI without calling either adapter or generator.
    pdd, wp, ws = [float(row[k]) for k in ('pdd_SE', 'w_AM_P', 'w_AM_S')]
    wam, vf = 1 - pdd, float(row['volfrac'])
    phi = (wam / 4800) / (wam / 4800 + pdd / 2000)
    v = 3.34e-13 * vf
    count = lambda f, r: v * f / (4 * math.pi / 3 * (float(r) * 1e-6) ** 3)
    kind = row['kind']
    ps = wp / (wp + ws) if kind == 'bimodal' else (1.0 if kind == 'mono_AM_P' else 0.0)
    if kind == 'bimodal':
        np, ns = count(phi * ps, row['rP_um']), count(phi * (1 - ps), row['rS_um'])
        dp, ds = 2 * float(row['rP_um']), 2 * float(row['rS_um'])
    elif kind == 'mono_AM_P':
        np, ns = count(phi, row['rP_um']), 0.0
        dp, ds = 2 * float(row['rP_um']), None
    else:
        np, ns = 0.0, count(phi, row['rP_um'])
        dp, ds = None, 2 * float(row['rP_um'])
    nse = count(1 - phi, row['rSE_um'])
    phi_ref = (.85 / 4800) / (.85 / 4800 + .15 / 2000)
    loading = 2 * vf * phi / (.222984 * phi_ref)
    dmax=max(x for x in (dp,ds) if x is not None)
    o = dict(case_id=row['id'], block=kind, am_pct=100 * wam, ps_frac=ps,
             ps_label=f'{round(10*ps)}:{10-round(10*ps)}',
             d_am_p_um=dp, d_am_s_um=ds, d_se_um=2 * float(row['rSE_um']),
             rve_um=50.0, pressure_MPa=300.0, e_se_gpa=1.35, d_am_max_um=dmax,
             r_AM_P_um=None if dp is None else dp/2,
             r_AM_S_um=None if ds is None else ds/2, r_SE_um=float(row['rSE_um']),
             size_ratio_P_over_S=dp/ds if dp is not None and ds is not None else None,
             size_ratio_AM_over_SE=dmax/(2*float(row['rSE_um'])),
             n_am_p_est=np, n_am_s_est=ns, n_se_est=nse, n_total_est=np+ns+nse,
             rve_over_d_am_max=50/dmax, loading_mAh_cm2=2.0 if pdd <= .30 else None,
             lhss_phi_AM_solid=phi)
    for key in ('stratum','ntype','kind','pdd_SE','w_AM_P','w_AM_S','rSE_lo_um','rSE_truncated',
                'volfrac','lhs_cell','seed','loading_rule','loading_mAh_cm2','ins_scale','cap_adjust','gap_dist'):
        o['lhss_'+key]=row[key]
    return o, loading


def refusal(fn):
    try:
        result = fn()
        return dict(refused=False, result=result)
    except Exception as e:
        return dict(refused=True, type=type(e).__name__, message=str(e))


design = S / 'docs/data/lhs_supp_design_20261006.csv'
adapted = S / 'docs/data/lhss_design_adapted_20261012.csv'
dc, dr = rows(design)
ac, ar = rows(adapted)
supp = [r for r in dr if r['block'] == 'supp']
byid = {r['case_id']: r for r in ar}
numeric_keys = ('am_pct', 'ps_frac', 'd_am_p_um', 'd_am_s_um', 'd_se_um',
                'n_am_p_est', 'n_am_s_est', 'n_se_est', 'n_total_est', 'loading_mAh_cm2')
per_case, mismatches = [], []
for r in supp:
    z, loading = independent(r)
    o = byid[r['id']]
    errors = {}
    assert set(z)==set(ac), (set(z)-set(ac),set(ac)-set(z))
    for k in ac:
        if z[k] is None:
            if o[k] != '':
                mismatches.append([r['id'], k, z[k], o[k]])
        else:
            try:
                err = abs(float(o[k])-float(z[k]))
            except ValueError:
                if o[k]!=z[k]:
                    mismatches.append([r['id'], k, z[k], o[k]])
                continue
            errors[k] = err
            if err > 1e-9 * max(1, abs(float(z[k]))):
                mismatches.append([r['id'], k, z[k], o[k]])
    per_case.append(dict(case_id=r['id'], kind=r['kind'], rule=r['loading_rule'],
                         abs_errors=errors,
                         integer_n_am_error=abs(z['n_am_p_est']+z['n_am_s_est']-int(r['n_AM_est'])),
                         integer_n_se_error=abs(z['n_se_est']-int(r['n_SE_est'])),
                         rounded_loading_error=abs(loading-float(r['loading_mAh_cm2']))))

with tempfile.TemporaryDirectory(dir=R/'tmp') as td:
    output = Path(td)/'regenerated.csv'
    A.write(A.adapt(str(design)), str(output))
    repro = dict(equal_bytes=output.read_bytes()==adapted.read_bytes(), output_sha256=sha(output))

tgz = S / 'docs/data/lhs_supp_runs_20261006/lhss_harvest_20261011_r2.tgz'
with tarfile.open(tgz, 'r:gz') as t:
    members = t.getmembers()
    union = A.union_from_text(t.extractfile(A.R2_MEMBER).read().decode('utf-8'))
    union_result = refusal(lambda: A.check_union(A.adapt(str(design)), union))
    archive = dict(sha256=sha(tgz), member_count=len(members),
                   union_rows=len(union), union_case_ids=sorted(union),
                   union_lx_values=sorted({r['lx_um'] for r in union.values()}),
                   union_check=union_result)

defs = D.column_dictionary(ac, design_source='docs/data/lhss_design_adapted_20261012.csv')
defs = {r['column']: r for r in defs}
mono_dict_counterexamples = []
for r in ar:
    p, s = float(r['lhss_w_AM_P']), float(r['lhss_w_AM_S'])
    if abs(p/(p+s)-float(r['ps_frac'])) > 1e-12:
        mono_dict_counterexamples.append({k:r[k] for k in ('case_id','block','ps_frac','lhss_w_AM_P','lhss_w_AM_S')})

# Use real design schemas, generated by production column_dictionary. No mock.
all_dicts = {'lhss':defs}
for ds, rel in [('lhs','docs/data/lhs_design_20260818.csv'),('lhsx','docs/data/lhsx_design_adapted_20260929.csv')]:
    cols, rr = rows(S/rel)
    all_dicts[ds] = {r['column']:r for r in D.column_dictionary(cols, design_source=rel)}

def differences(dicts):
    return B.v13_combined_problems({}, dicts)

tail_changed = copy.deepcopy(all_dicts)
tail_changed['lhss']['am_pct']['meaning'] = tail_changed['lhss']['am_pct']['meaning'].split(' · 원천 = ')[0] + ' · 원천 = another/design.csv'
meaning_changed = copy.deepcopy(all_dicts)
meaning_changed['lhss']['am_pct']['meaning'] = 'WRONG volume percent · 원천 = docs/data/lhss_design_adapted_20261012.csv'
caveat_changed = copy.deepcopy(all_dicts)
caveat_changed['lhss']['am_pct']['caveat'] = 'different caveat'
source_changed = copy.deepcopy(all_dicts)
source_changed['lhss']['am_pct']['source'] = 'other'
definition_cross = dict(actual=differences(all_dicts), path_only=differences(tail_changed),
                       definition_body=differences(meaning_changed), caveat=differences(caveat_changed),
                       source=differences(source_changed),
                       shared_all_three=sorted(set.intersection(*(set(d) for d in all_dicts.values()))))

bc = ['case_id','am_pct','loading_mAh_cm2']
fixed = next(r for r in ar if r['loading_mAh_cm2'])
free = next(r for r in ar if not r['loading_mAh_cm2'])
value_mutations = {value:B.v13_blank_problems([dict(fixed, loading_mAh_cm2=value)],bc)
                   for value in ['2.0','99','-1','NaN','junk','']}
blank = dict(actual=B.v13_blank_problems(ar,bc),
             fixed_case=fixed['case_id'],fixed_value_mutations=value_mutations,
             free_nonblank=B.v13_blank_problems([dict(free,loading_mAh_cm2='2.0')],bc),
             threshold_cases=[dict(am_pct=am,code=B.v13_blank_reason(dict(case_id='boundary_probe',am_pct=str(am)), 'loading_mAh_cm2'))
                              for am in [69.999998,69.999999,69.9999995,70,70.000001]],
             actual_distance_from_boundary=min(abs(float(r['am_pct'])-70) for r in ar),
             role=B.v13_role('loading_mAh_cm2'))

# Preserve real preexisting 194 input values and compare the ordinary and new
# wrapper fit. There is no real supp20 g2 input; do not invent scientific values.
release_dir=S/'docs/data/lhs_release_20261006_v12'
paths={ds:str(release_dir/f'{ds}_release_20261006_v12.csv') for ds in ('lhs','lhsx')}
fit0=B.refit_from_csv(paths,dry_run=True)
fit1=B.v13_refit(paths,dry_run=True)
refit=dict(real_source_generation='v1.2 / g1; diagnostic algorithm check only',
           normal_vs_wrapper_equal=fit0==fit1,
           n_total=fit1['summary']['n_total'],n_fit=fit1['summary']['n_fit'],
           n_fit_by_dataset=fit1['summary']['n_fit_by_dataset'],excluded=fit1['summary']['excluded'],
           fits=fit1['summary']['fits'],
           has_reference_without_supp='reference_without_supp' in fit1['summary'],
           supp20_actual_fit_available=False)

evidence=dict(pin='b429c3c1df0956d2721861d89cc29a2d56f2b581',
              source_design=dict(sha256=sha(design),expected_sha256=A.DESIGN_SHA256,rows=len(dr),columns=len(dc),
                                 supp_rows=len(supp),thick_rows=sum(r['block']=='thick' for r in dr)),
              adapted=dict(sha256=sha(adapted),rows=len(ar),columns=len(ac),unique_ids=len(byid),
                           kinds=dict(collections.Counter(r['block'] for r in ar)),
                           rules=dict(collections.Counter(r['lhss_loading_rule'] for r in ar)),
                           main_loading=dict(collections.Counter(r['loading_mAh_cm2'] for r in ar)),
                           am_range=[min(float(r['am_pct']) for r in ar),max(float(r['am_pct']) for r in ar)],
                           regeneration=repro),
              independent=dict(mismatches=mismatches,per_case=per_case,
                               maximum_integer_count_error=max(max(p['integer_n_am_error'],p['integer_n_se_error']) for p in per_case),
                               maximum_loading_roundoff=max(p['rounded_loading_error'] for p in per_case)),
              r2_archive=archive,
              new_dictionary_mono_counterexamples=mono_dict_counterexamples,
              new_dictionary_claims={k:defs[k] for k in ['lhss_w_AM_P','lhss_w_AM_S','lhss_loading_rule','loading_mAh_cm2']},
              definition_cross=definition_cross,loading_blank_contract=blank,refit=refit)
(R/'evidence/design_probe.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in evidence.items() if k not in ['new_dictionary_claims','independent']},ensure_ascii=False,indent=2))
print('Independent recalculation mismatches:',mismatches)
print('Maximum integer count error:',evidence['independent']['maximum_integer_count_error'])
print('Maximum loading roundoff:',evidence['independent']['maximum_loading_roundoff'])
assert not mismatches
assert repro['equal_bytes']
assert not blank['actual']
assert not definition_cross['actual']
assert not definition_cross['path_only']
assert definition_cross['definition_body'] and definition_cross['caveat'] and definition_cross['source']
assert fit0==fit1

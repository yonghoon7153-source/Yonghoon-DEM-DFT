"""Read-only arithmetic audit of stored non-mixer chart data. No solvers."""
import csv
import hashlib
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

V3 = Path(__file__).resolve().parents[1]
SRC = V3 / 'sources_code'
FIG = V3 / 'input/repo/docs/seminar_20261013/figs_v3'

def rows(path, delim=',', skip=0):
    with path.open(encoding='utf-8-sig', newline='') as f:
        data = list(csv.DictReader(f, delimiter=delim))
    return data[skip:]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

ps = ['0:10', '3:7', '5:5', '7:3', '10:0']
report = {}
summary = json.loads((SRC / 'docs/report_20261021/summary.json').read_text())
por = rows(FIG / 'F_poro.csv')
raw_por = rows(SRC / 'docs/data/ps45_r45_union_20260929/r45_union_summary.tsv', '\t')
raw_por = {r['P_S']: float(r['porosity_union_exact_pct']) for r in raw_por}
report['porosity'] = [dict(composition=p, chart=float(r['porosity union (%)']), G1=summary['G1'][p]['union'], stored_union=raw_por[p]) for p, r in zip(ps, por)]
assert all(x['chart'] == x['G1'] == round(x['stored_union'], 2) for x in report['porosity'])

tau = rows(SRC / 'docs/data/ps45_r45_network_g2_20261007/transport_tortuosity_g2.csv', skip=2)
sig = rows(SRC / 'docs/data/ps45_r45_network_g2_20261007/deck_p14p15_20261012/p15_sigmaLi_hertz_s0_1p5.csv', skip=1)
trans = rows(FIG / 'F_trans.csv')
report['transport'] = []
for p, t, s, r in zip(ps, tau, sig, trans):
    tv = float(t['Transport tortuosity (Hertz)'])
    sv = float(s['σLi+'])
    assert float(r['transport tortuosity (Hertz)']) == round(tv, 4)
    assert float(r['sigma_ion (mS/cm, sigma0 = 1.5)']) == round(sv, 4)
    report['transport'].append(dict(composition=p, raw_T=tv, raw_sigma_mScm=sv, chart_T=float(r['transport tortuosity (Hertz)']), chart_sigma=float(r['sigma_ion (mS/cm, sigma0 = 1.5)'])))

arms = [json.loads(p.read_text()) for p in (SRC / 'docs/data/phase_a_rep100_20260930/pa100').glob('*/arms/*.json')]
primary = [a for a in arms if a['role'] == 'primary']
groups = defaultdict(list)
bykey = {}
for a in primary:
    groups[a['vox'], a['vgcf_wt']].append(1000 * a['sigma_e'])
    bykey[a['vox'], a['origin'], a['vgcf_wt']] = a['sigma_e']
vg = rows(FIG / 'F_vgcf.csv')
report['vgcf'] = {'n_all': len(arms), 'n_primary': len(primary), 'n_other': len(arms)-len(primary), 'means': []}
for r in vg:
    key = float(r['voxel (um)']), float(r['VGCF wt%'])
    mean = statistics.mean(groups[key])
    chart = float(r['sigma_e mean (mS/cm)'])
    report['vgcf']['means'].append(dict(voxel_um=key[0], wt=key[1], n=len(groups[key]), raw_mean_mScm=mean, chart_mScm=chart, matches_two_decimals=chart == round(mean, 2)))
report['vgcf']['adjacent_comparisons'] = sum(bykey[v,o,w+1] > bykey[v,o,w] for v in (0.15,0.2,0.25) for o in range(8) for w in (1,2,3))
report['vgcf']['minimum_adjacent_gain_pct'] = min((bykey[v,o,w+1]/bykey[v,o,w]-1)*100 for v in (0.15,0.2,0.25) for o in range(8) for w in (1,2,3))
report['vgcf']['qc_replay_max_relative_pct'] = max(abs(a['sigma_e']/bykey[a['vox'],a['origin'],a['vgcf_wt']]-1)*100 for a in arms if a['role'] != 'primary')
report['vgcf']['generation_resolution'] = {'chart_source': 'phase_a_104arms_20260921 (VGCF E = 10 GPa original campaign)', 'recomputed_raw_source': 'phase_a_rep100_20260930/pa100 (VGCF E = 100 GPa replication)', 'evidence': 'notes/sources/report_make_figs.py:139-147; prior pinned phase_a_rep100 README:4'}
original = json.loads((V3 / 'notes/sources/phase_a_original_primary96.json').read_text())
original_groups = defaultdict(list)
for item in original['files']:
    a = item['raw']
    assert a['role'] == 'primary'
    original_groups[a['vox'], a['vgcf_wt']].append(1000 * a['sigma_e'])
report['vgcf']['original_independently_recomputed_means'] = []
for r in vg:
    key = float(r['voxel (um)']), float(r['VGCF wt%'])
    original_mean = statistics.mean(original_groups[key])
    chart = float(r['sigma_e mean (mS/cm)'])
    assert len(original_groups[key]) == 8
    assert chart == round(original_mean, 2)
    report['vgcf']['original_independently_recomputed_means'].append(dict(voxel_um=key[0], wt=key[1], n=8, raw_mean_mScm=original_mean, chart_mScm=chart, matches_two_decimals=True))

pl = json.loads((SRC / 'docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json').read_text())
fl = rows(FIG / 'F_load.csv')
report['load'] = []
for p, r in zip(ps, fl):
    c = pl['cases'][p]
    denominator = sum(x['load_mpa'] for x in c['cuts'])
    shares = {g: sum(x['load_mpa'] * x['share_group_pct'][g] for x in c['cuts']) / denominator for g in ('AM–AM','AM–SE','SE–SE')}
    assert all(abs(shares[g] - c['contribution_sigma_zz_pct'][g]) < 1e-12 for g in shares)
    actual = dict(zip(shares, [float(r['AM-AM (%)']),float(r['AM-SE (%)']),float(r['SE-SE (%)'])]))
    assert all(abs(shares[g] - actual[g]) <= .00050001 for g in shares)
    report['load'].append(dict(composition=p,n_planes=len(c['cuts']),weighted=shares,unweighted=c['share_group_mean_over_cuts_pct'],mean_MPa=denominator/len(c['cuts']),chart=actual,chart_sum=sum(actual.values())))
report['ranks'] = {'porosity_ascending': sorted(ps,key=raw_por.get), 'load_ascending': sorted(ps,key=lambda p:pl['cases'][p]['contribution_sigma_zz_pct']['AM–AM'])}

release = SRC / 'docs/data/lhs_release_20261006_v12'
r130 = rows(release / 'lhs_release_20261006_v12.csv')
r64 = rows(release / 'lhsx_release_20261006_v12.csv')
ds = rows(FIG / 'F_dataset.csv')
assert len(ds) == len(r130) + len(r64) == 194
report['dataset'] = {}
for name, src, chart in [('130',r130,ds[:130]), ('64',r64,ds[130:])]:
    tau_values=[]; missing=[]; mismatch=[]
    for i,(a,b) in enumerate(zip(src,chart)):
        se=100*float(a['se_of_solid_vol'])
        t=float(a['tortuosity_SE_wall']) if a['tortuosity_SE_wall'] else math.nan
        ct=float(b['geometric tortuosity (blank = non-percolating)'])
        if se!=float(b['SE fraction of solid (vol%)']) or not ((math.isnan(t) and math.isnan(ct)) or t==ct): mismatch.append(i)
        if name=='130' and float(a['porosity_union_exact_pct'])!=float(b['porosity union (%)']): mismatch.append(i)
        if math.isfinite(t): tau_values.append(t)
        else: missing.append({'row':i+2,'case_id':a['case_id'],'se_pct':se,'source_tau':a['tortuosity_SE_wall'],'percolation_pct':a['percolation_pct']})
    assert not mismatch
    report['dataset'][name]={'rows':len(src),'finite_tau':len(tau_values),'nonfinite_tau':len(missing),'tau_range':[min(tau_values),max(tau_values)],'mismatches':mismatch,'nonfinite':missing,'se_range':[min(float(a['se_of_solid_vol'])*100 for a in src),max(float(a['se_of_solid_vol'])*100 for a in src)]}

lim = rows(FIG / 'F_limits.csv')
raw_e = rows(SRC / 'docs/data/ps45_sigmae_factor_off_20261013/factor_off_electronic.tsv','\t')
report['limits']={'csv':lim,'factor_off':[],'grid_source':'CLAUDE.md:167-168; claims.json CL-24 raw public points','model_measurement_source':'docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md:3,9,21-22'}
for a,b in zip(raw_e,[r for r in lim if r['panel']=='ps45_sigma_e']):
    value=float(a['main_sigma_ref_mScm'])
    assert round(value,3)==float(b['y1'])
    report['limits']['factor_off'].append(dict(composition=a['P_S'],raw_mScm=value,chart_mScm=float(b['y1'])))

ppt = json.loads((V3 / 'evidence/pptx.json').read_text())
report['embedded_matches'] = {}
for name, page in [('F_poro',3),('F_trans',4),('F_vgcf',7),('F_limits',8),('F_load',9),('F_dataset',10)]:
    sha=digest(FIG/(name+'.png'))
    matches=[m['path'] for m in ppt['slides'][page-1]['media'] if m['sha256']==sha]
    assert len(matches)==1
    report['embedded_matches'][name]={'slide':page,'sha256':sha,'embedded_path':matches[0]}

serialized = json.dumps(report,ensure_ascii=False,indent=2)
if '--save' in sys.argv:
    destination = V3 / 'evidence/charts_arithmetic.json'
    destination.write_text(serialized + '\n', encoding='utf-8')
    print(str(destination))
else:
    print(serialized)
